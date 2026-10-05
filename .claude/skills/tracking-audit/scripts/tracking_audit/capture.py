"""Playwright capture: intercept every network request across a scripted visit.

Visit sequence per brand (each request is tagged with the phase it fired in):
  initial  -> homepage load, before any consent interaction
  consent  -> consent banner accepted (selector / button text / CMP JS API)
  reload   -> tab reloaded with consent granted; GTM containers are captured here
  pdp      -> first product page found on the homepage (ecommerce events)
  atc      -> add-to-cart clicked on the product page

Outputs into <out>/<slug>/ (default outputs/<slug>/):
  containers/<ID>.js     raw container script exactly as served
  containers/<ID>.json   decoded container JSON (resource/runtime/permissions/...)
  raw/network.json       every request: phase, url, method, type, status, post body, failure
  raw/capture.json       visit metadata, consent result, per-phase page snapshots
  raw/page.html          homepage HTML after the consented reload
"""

import asyncio
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urljoin

from playwright.async_api import async_playwright

from . import signatures as sig
from .container import extract_data, container_id_from

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
BLOCK_TITLE = re.compile(
    r"just a moment|attention required|access denied|verify you are human|"
    r"pardon our interruption|are you a robot|request blocked|security check",
    re.I,
)
# Secret-shaped strings third-party widgets sometimes embed in public pages: never write them to disk.
SECRET_RX = re.compile(r"(sk_live_|AKIA|ghp_|gho_|xox[baprs]-|shpat_|shpss_)[0-9A-Za-z_-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")


def redact(text: str) -> str:
    return SECRET_RX.sub(lambda m: (m.group(1) or "-----BEGIN ") + "REDACTED", text) if text else text


MAX_POST = 60000  # pixel POST bodies (Meta cd[]/pmd[], TikTok JSON) carry dedupe IDs late in the body

# Page snapshot (dataLayer, google_tag_manager keys, Shopify, consent state). Shared with the
# Playwright-MCP fallback, which pastes the same function into browser_evaluate.
SNAPSHOT_JS = (Path(__file__).resolve().parent.parent / "snapshot.js").read_text(encoding="utf-8")


BANNER_RX = r"cookie|consent|privacy|gdpr|ccpa|tracking technolog|do not sell|personal (data|information)"
BANNER_JS = """
() => {
  const rx = /%s/i;
  const visible = (el, cs, r) => cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.05 && r.width > 150 && r.height > 30;
  const out = [];
  const seen = new Set();
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    if (!visible(el, cs, r) || r.bottom < 0 || r.top > innerHeight) continue;
    const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
    if (!t || t.length > 2500 || !rx.test(t) || seen.has(t)) continue;
    seen.add(t);
    out.push({tag: el.tagName.toLowerCase(), id: el.id || null,
              cls: (el.getAttribute('class') || '').slice(0, 120) || null, text: t.slice(0, 220),
              rect: [r.x, r.y, r.width, r.height].map(Math.round)});
    if (out.length >= 5) break;
  }
  const cmp_iframes = [...document.querySelectorAll('iframe')]
    .filter(f => { const r = f.getBoundingClientRect(); return r.width > 150 && r.height > 30; })
    .map(f => f.src || f.id || f.name)
    .filter(s => /consent|cookie|privacy|cmp|onetrust|didomi|usercentrics|sourcepoint|trustarc|ketch|osano/i.test(s || ''))
    .slice(0, 5);
  return {candidates: out, cmp_iframes};
}
""" % BANNER_RX
ACCEPT_IN_BANNER_JS = """
() => {
  const rx = /%s/i;
  const yes = /accept|allow|agree|got it|^ok(ay)?$|consent|continue|understand|i'?m ok/i;
  const no = /reject|decline|deny|refuse|manage|setting|preference|customi[sz]e|learn|more info|policy|necessary only|only necessary/i;
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
    const t = (el.innerText || '').trim();
    if (!t || t.length > 2500 || !rx.test(t) || el.getBoundingClientRect().width < 150) continue;
    const ctrls = [...el.querySelectorAll('button, a, [role=button], input[type=button], input[type=submit], div[tabindex], span[tabindex]')]
      .filter(c => { const r = c.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
    const label = c => (c.innerText || c.value || c.getAttribute('aria-label') || '').replace(/\\s+/g, ' ').trim();
    const pick = ctrls.find(c => /accept all|allow all|agree to all/i.test(label(c)))
              || ctrls.find(c => yes.test(label(c)) && !no.test(label(c)));
    if (pick) { pick.click(); return label(pick).slice(0, 60) || '(unlabelled control)'; }
  }
  return null;
}
""" % BANNER_RX


class BrandCapture:
    def __init__(self, slug: str, url: str, out_root: Path):
        self.slug, self.url = slug, url
        self.out = out_root / slug
        self.phase = "initial"
        self.requests: list[dict] = []
        self._by_req: dict = {}
        self.containers: dict[str, dict] = {}
        self._body_tasks: list[asyncio.Task] = []
        self.snapshots: dict[str, dict] = {}
        self.log: list[str] = []
        self.initiators: list[dict] = []  # CDP: which script / document caused each request
        self.meta: dict = {"slug": slug, "url": url}

    def say(self, msg: str):
        line = f"[{self.slug}] {msg}"
        print(line, flush=True)
        self.log.append(msg)

    # ── network hooks ────────────────────────────────────────────────────────
    def on_request(self, req):
        try:
            post = req.post_data if req.method == "POST" else None
        except Exception:
            post = "<binary>"
        try:
            frame_url = req.frame.url if req.frame else None
        except Exception:
            frame_url = None
        rec = {
            "phase": self.phase,
            "t": round(time.time(), 3),
            "url": req.url[:4000],
            "method": req.method,
            "type": req.resource_type,
            "status": None,
            "failure": None,
            "post": (post or "")[:MAX_POST] or None,
            "frame": frame_url if frame_url and frame_url != req.url else None,
        }
        self._by_req[req] = rec
        self.requests.append(rec)

    def on_response(self, resp):
        rec = self._by_req.get(resp.request)
        if rec is not None:
            rec["status"] = resp.status
        url = resp.url
        ctype = (resp.headers or {}).get("content-type", "")
        if resp.request.resource_type == "script" or "javascript" in ctype or "gtm.js" in url or "gtag/js" in url:
            self._body_tasks.append(asyncio.ensure_future(self._read_body(resp)))

    def on_failed(self, req):
        rec = self._by_req.get(req)
        if rec is not None:
            try:
                rec["failure"] = req.failure or "failed"
            except Exception:
                rec["failure"] = "failed"

    def on_cdp_request(self, params):
        try:
            init = params.get("initiator") or {}
            urls, stack = [], init.get("stack")
            while stack and len(urls) < 15:  # whole async stack: wrappers (fetch/beacon patches) sit on top
                for cf in stack.get("callFrames", []):
                    u = cf.get("url")
                    if u and (not urls or urls[-1] != u[:600]):
                        urls.append(u[:600])
                stack = stack.get("parent")
            by = init.get("url") or (urls[0] if urls else "")
            self.initiators.append({"url": params["request"]["url"][:1500], "type": init.get("type"), "by": by[:1500],
                                    "stack": list(dict.fromkeys(urls))[:15], "doc": (params.get("documentURL") or "")[:300],
                                    "phase": self.phase})
        except Exception:
            pass

    async def _read_body(self, resp):
        try:
            if resp.status >= 300:
                return
            body = await asyncio.wait_for(resp.text(), timeout=20)
        except Exception:  # incl. timeout: streaming / never-ending responses
            return
        if "var data" not in body or '"resource"' not in body:
            return
        data = extract_data(body)
        if not data:
            return
        cid = container_id_from(data, resp.url)
        prev = self.containers.get(cid)
        # Keep the post-consent copy when the same container loads in several phases.
        if prev and prev["phase"] == "reload":
            return
        host = urlparse(resp.url).hostname or ""
        self.containers[cid] = {
            "id": cid,
            "url": resp.url,
            "phase": self.phase,
            "first_party_loader": "googletagmanager.com" not in host,
            "body": body,
            "data": data,
        }
        if not prev:
            self.say(f"container {cid} captured ({round(len(body) / 1024)} KB) from {host} [{self.phase}]")

    async def drain(self, timeout: float = 30):
        while self._body_tasks:
            tasks, self._body_tasks = self._body_tasks, []
            done, pending = await asyncio.wait(tasks, timeout=timeout)
            for t in pending:
                t.cancel()

    # ── page helpers ─────────────────────────────────────────────────────────
    async def settle(self, page, dwell_ms: int):
        try:
            await page.wait_for_load_state("networkidle", timeout=12000)
        except Exception:
            pass
        await page.wait_for_timeout(dwell_ms)

    async def scroll(self, page):
        try:
            for frac in (0.25, 0.5, 0.75, 1.0):
                await page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {frac})")
                await page.wait_for_timeout(700)
            await page.evaluate("window.scrollTo(0, 0)")
        except Exception:
            pass

    async def snapshot(self, page, label: str):
        try:
            self.snapshots[label] = await asyncio.wait_for(page.evaluate(SNAPSHOT_JS), timeout=20)
        except Exception as e:
            self.snapshots[label] = {"error": str(e)}

    async def wait_out_bot_wall(self, page) -> bool:
        """Returns True if the page still looks like a bot challenge."""
        for _ in range(12):
            try:
                title = await page.title()
            except Exception:
                title = ""
            if not BLOCK_TITLE.search(title or ""):
                return False
            await page.wait_for_timeout(2500)
        return True

    async def accept_consent(self, page) -> dict:
        result = {"accepted": False, "method": None, "detail": None}
        await page.wait_for_timeout(1500)
        # 1. Known CMP selectors (all frames; CSS pierces open shadow roots).
        for frame in page.frames:
            for selector in sig.CONSENT_SELECTORS:
                try:
                    loc = frame.locator(selector).first
                    if await loc.count() and await loc.is_visible():
                        await loc.click(timeout=4000)
                        return {"accepted": True, "method": "selector", "detail": selector}
                except Exception:
                    continue
        # 2. Visible buttons/links whose whole label reads like "Accept all"; then any element with
        #    that exact text (banners often use <a> without href or <div>/<span>, which have no role).
        for frame in page.frames:
            for kind in ("button", "link", "text"):
                try:
                    loc = (frame.get_by_text(sig.CONSENT_BUTTON_TEXT) if kind == "text"
                           else frame.get_by_role(kind, name=sig.CONSENT_BUTTON_TEXT))
                    n = await loc.count()
                    for i in range(min(n, 5)):
                        el = loc.nth(i)
                        if await el.is_visible():
                            label = ((await el.inner_text()).strip()
                                     or (await el.get_attribute("aria-label") or "")).strip()[:60]
                            await el.click(timeout=4000)
                            return {"accepted": True, "method": "button_text", "detail": f"{kind}: {label}"}
                except Exception:
                    continue
        # 3. CMP JavaScript APIs (banner may be hidden for this geo but the CMP is loaded).
        for name, js in sig.CONSENT_JS:
            try:
                if await page.evaluate(f"() => {{ try {{ return !!({js}); }} catch (e) {{ return false; }} }}"):
                    return {"accepted": True, "method": "js_api", "detail": f"{name} (no visible banner)"}
            except Exception:
                continue
        return result

    async def dismiss_popups(self, page):
        try:
            await page.keyboard.press("Escape")
            for sel in ("[aria-label*='close' i]:visible", "button.needsclick.klaviyo-close-form",
                        "[data-testid='closeIcon']", "#attentive_overlay button[aria-label*='Dismiss' i]"):
                loc = page.locator(sel).first
                if await loc.count() and await loc.is_visible():
                    await loc.click(timeout=1500)
                    await page.wait_for_timeout(400)
        except Exception:
            pass

    async def find_product_url(self, page) -> str | None:
        """Pick a representative product: the product URL linked most often (cards link image + title),
        skipping add-ons, gift cards, protection plans and the like."""
        try:
            hrefs = await page.eval_on_selector_all(
                "a[href*='/products/'], a[href*='/product/'], a[href*='/p/']",
                "els => els.filter(e => e.offsetParent !== null).map(e => e.getAttribute('href')).filter(Boolean)",
            )
        except Exception:
            return None
        skip = re.compile(r"gift-?card|add-?on|/products/add-|existing-order|warranty|protection|insurance|route|"
                          r"sample|donat|shipping|e-?gift|engraving|personaliz", re.I)
        site_host = urlparse(page.url).hostname
        counts: dict[str, int] = {}
        for h in hrefs:
            full = urljoin(page.url, h).split("#")[0].split("?")[0]
            if urlparse(full).hostname == site_host and not skip.search(full):
                counts[full] = counts.get(full, 0) + 1
        if not counts:
            return None
        order = list(counts)
        return max(order, key=lambda u: (counts[u], -order.index(u)))

    async def add_to_cart(self, page) -> str | None:
        for sel in ("form[action*='/cart/add'] button[type='submit']", "button[name='add']",
                    "[data-testid*='add-to-cart' i]", "button[id*='AddToCart' i]",
                    "button:has-text('Add to cart')", "button:has-text('Add to bag')"):
            try:
                loc = page.locator(sel).first
                if await loc.count() and await loc.is_visible() and await loc.is_enabled():
                    await loc.click(timeout=4000)
                    return sel
            except Exception:
                continue
        return None

    async def direct_fetch(self, context, cid: str):
        try:
            resp = await context.request.get(f"https://www.googletagmanager.com/gtm.js?id={cid}", timeout=20000)
            if resp.status == 404:
                self.meta.setdefault("unpublished_containers", []).append(cid)
                self.say(f"container {cid} is referenced but returns 404 (not published)")
            if resp.ok:
                body = await resp.text()
                data = extract_data(body)
                if data:
                    self.containers[cid] = {
                        "id": cid, "url": resp.url, "phase": "direct_fetch",
                        "first_party_loader": False, "body": body, "data": data,
                    }
                    self.say(f"container {cid} fetched directly ({round(len(body) / 1024)} KB)")
        except Exception as e:
            self.say(f"direct fetch {cid} failed: {e}")

    # ── screenshots, banner checks, coverage review ──────────────────────────
    async def shot(self, page, name: str):
        sdir = self.out / "screenshots"
        sdir.mkdir(parents=True, exist_ok=True)
        try:
            await page.screenshot(path=str(sdir / f"{name}.png"), timeout=15000)
            self.meta.setdefault("screenshots", []).append(f"screenshots/{name}.png")
        except Exception as e:
            self.say(f"screenshot {name} failed: {e}")

    async def banner_check(self, page, label: str) -> dict:
        """Visible fixed/sticky elements (or CMP iframes) that read like a cookie/consent banner."""
        try:
            res = await asyncio.wait_for(page.evaluate(BANNER_JS), timeout=20)
        except Exception as e:
            res = {"candidates": [], "cmp_iframes": [], "error": str(e)}
        self.meta.setdefault("banner_checks", {})[label] = res
        if res.get("candidates") or res.get("cmp_iframes"):
            first = (res["candidates"] or [{"text": res["cmp_iframes"][0]}])[0]
            self.say(f"banner-like element visible [{label}]: {first.get('text', '')[:90]}")
        return res

    async def consent_lost(self, page) -> bool:
        """True if consent was granted earlier but this page shows a banner again or Shopify consent is empty."""
        if not (self.meta.get("consent") or {}).get("accepted"):
            return False
        banner = await self.banner_check(page, f"check_{self.phase}")
        try:
            state = await asyncio.wait_for(page.evaluate(
                "() => { try { const c = window.Shopify && Shopify.customerPrivacy && Shopify.customerPrivacy.currentVisitorConsent"
                " ? Shopify.customerPrivacy.currentVisitorConsent() : null; return c ? (c.marketing || '') : null; }"
                " catch (e) { return null; } }"), timeout=10)
        except Exception:
            state = None
        return bool(banner.get("candidates")) or state == ""

    async def accept_in_banner(self, page) -> str | None:
        """Click the most 'accept'-looking control inside a detected banner element."""
        try:
            return await asyncio.wait_for(page.evaluate(ACCEPT_IN_BANNER_JS), timeout=20)
        except Exception:
            return None

    def review_coverage(self):
        """An ecommerce site always runs analytics + ad tracking. If we saw none after consent,
        the capture (not the site) is presumed broken and must be checked by hand."""
        from .network import classify, _is_ga4_hit

        post = [r for r in self.requests if r["phase"] in ("reload", "pdp", "atc")]
        cats = {}
        for r in post:
            vendor, cat = ("Google Analytics 4", "analytics") if _is_ga4_hit(r["url"]) else classify(r["url"])
            if cat:
                cats.setdefault(cat, set()).add(vendor)
        shop = any((s or {}).get("shopify") for s in self.snapshots.values() if isinstance(s, dict))
        ecommerce = shop or bool(self.meta.get("pdp_url"))
        reasons = []
        if self.meta.get("bot_wall"):
            reasons.append("bot challenge did not clear")
        if len(self.requests) < 80:
            reasons.append(f"only {len(self.requests)} requests captured")
        if not cats.get("analytics") and not cats.get("attribution"):
            reasons.append("no analytics requests after consent")
        if ecommerce and not cats.get("advertising"):
            reasons.append("no advertising pixels after consent on an ecommerce site")
        if (self.meta.get("banner_checks") or {}).get("reload", {}).get("candidates"):
            reasons.append("consent/cookie banner still visible after accept + reload")
        if self.meta.get("consent_not_persisting"):
            reasons.append("consent did not persist to the product page (Shopify consent empty after re-accept)")
        live = {c for c, v in self.containers.items() if v["phase"] != "direct_fetch"}
        never_ran = sorted(c for c in self.containers if c.startswith("GTM-") and c not in live)
        if never_ran:
            reasons.append(f"GTM container(s) {', '.join(never_ran)} referenced but never loaded in the browser "
                           "(consent-gated or broken)")
        self.meta["review"] = {
            "needs_review": bool(reasons),
            "reasons": reasons,
            "ecommerce": ecommerce,
            "post_consent_categories": {k: sorted(v) for k, v in cats.items()},
        }
        if reasons:
            self.say("REVIEW NEEDED: " + "; ".join(reasons))

    # ── main flow ────────────────────────────────────────────────────────────
    async def run(self, context, dwell_ms: int, pdp: bool, fresh: bool):
        """`context` is the shared persistent profile: cookies / consent / bot-check clearance survive
        across brands and runs. Traffic is recorded per page (incl. its iframes), so brands captured in
        parallel tabs don't mix."""
        self.out.mkdir(parents=True, exist_ok=True)
        site = re.escape(".".join((urlparse(self.url).hostname or "").split(".")[-2:]))
        if fresh:
            await context.clear_cookies(domain=re.compile(rf"(^|\.){site}$"))
        stored = [c["name"] for c in await context.cookies() if re.search(rf"(^|\.){site}$", c["domain"].lstrip("."))]
        self.meta["profile"] = {"fresh": fresh, "returning_visit": bool(stored), "stored_cookies": stored[:40]}
        if stored:
            self.say(f"returning visit: {len(stored)} stored cookie(s) from the persistent profile "
                     "(pre-consent phase reflects stored consent; use --fresh for a first-visit capture)")
        page = await context.new_page()
        page.on("dialog", lambda d: asyncio.ensure_future(d.dismiss()))  # alerts / beforeunload would block
        page.set_default_timeout(30000)
        page.on("request", self.on_request)
        page.on("response", self.on_response)
        page.on("requestfailed", self.on_failed)
        # Request initiator chain (Chrome DevTools Protocol): lets parse attribute every hit to what loaded it
        # (GTM, Shopify app embed, theme code, custom pixel). Requests from sandboxed web workers (Shopify app
        # pixels) never show up here — that absence is itself a signal.
        try:
            cdp = await context.new_cdp_session(page)
            await cdp.send("Network.enable")
            cdp.on("Network.requestWillBeSent", self.on_cdp_request)
        except Exception as e:
            self.say(f"initiator capture unavailable: {e}")
        html = ""
        self.meta["started"] = datetime.now(timezone.utc).isoformat()
        try:
            if fresh:
                # Cookies are cleared above; storage needs the origin loaded first.
                try:
                    await page.goto(self.url, wait_until="domcontentloaded", timeout=60000)
                    await page.evaluate("() => { try { localStorage.clear(); sessionStorage.clear(); } catch (e) {} }")
                except Exception:
                    pass
                await self.drain()
                self.requests.clear()
                self._by_req.clear()
                self.containers.clear()
            self.phase = "initial"
            self.say(f"loading {self.url}")
            try:
                await page.goto(self.url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                self.say(f"navigation warning: {e}")
            self.meta["bot_wall"] = await self.wait_out_bot_wall(page)
            if self.meta["bot_wall"]:
                self.say("BLOCKED: bot challenge did not clear - use the Playwright MCP fallback (see tracking-capture skill)")
            await self.settle(page, dwell_ms)
            await self.snapshot(page, "initial")
            self.meta["final_url"] = page.url
            await self.shot(page, "01_initial")
            initial_banner = await self.banner_check(page, "initial")

            self.phase = "consent"
            consent = await self.accept_consent(page)
            # Explicit second pass: a banner-like element is on screen but no known control matched.
            if (not consent["accepted"] or consent["method"] == "js_api") and initial_banner["candidates"]:
                hit = await self.accept_in_banner(page)
                if hit:
                    consent = {"accepted": True, "method": "banner_scan", "detail": hit}
            self.meta["consent"] = consent
            self.say(f"consent: {consent['method'] or 'no banner/CMP found'}"
                     + (f" ({consent['detail']})" if consent.get("detail") else ""))
            await page.wait_for_timeout(3000)
            await self.shot(page, "02_after_consent")
            await self.banner_check(page, "after_consent")

            # Reload with consent granted: containers + post-consent tag firing.
            self.phase = "reload"
            try:
                await page.reload(wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                self.say(f"reload warning: {e}")
            await self.settle(page, dwell_ms)
            await self.dismiss_popups(page)
            await page.evaluate("window.scrollTo(0, 0)")
            await self.shot(page, "03_reload")
            await self.banner_check(page, "reload")
            await self.scroll(page)
            await page.wait_for_timeout(1500)
            await self.snapshot(page, "reload")
            try:
                html = await page.content()
            except Exception:
                html = ""

            if pdp:
                product = await self.find_product_url(page)
                self.meta["pdp_url"] = product
                if product:
                    self.phase = "pdp"
                    self.say(f"product page {product}")
                    try:
                        await page.goto(product, wait_until="domcontentloaded", timeout=60000)
                    except Exception as e:
                        self.say(f"pdp warning: {e}")
                    await self.settle(page, dwell_ms)
                    if await self.consent_lost(page):
                        # Banner back / Shopify consent empty on the PDP: re-accept and reload so product events fire.
                        again = await self.accept_consent(page)
                        if not again["accepted"]:
                            hit = await self.accept_in_banner(page)
                            again = {"accepted": bool(hit), "method": "banner_scan", "detail": hit}
                        self.say(f"consent lost on product page - re-accepted: {again.get('method')} ({again.get('detail')})")
                        self.meta["consent_reaccepted_pdp"] = again
                        await page.wait_for_timeout(2000)
                        try:
                            await page.reload(wait_until="domcontentloaded", timeout=60000)
                        except Exception:
                            pass
                        await self.settle(page, dwell_ms)
                        if await self.consent_lost(page):
                            self.meta["consent_not_persisting"] = True
                    await self.dismiss_popups(page)
                    await self.shot(page, "04_pdp")
                    await self.scroll(page)
                    await self.snapshot(page, "pdp")
                    self.phase = "atc"
                    clicked = await self.add_to_cart(page)
                    self.meta["atc_selector"] = clicked
                    if clicked:
                        self.say("add-to-cart clicked")
                        await page.wait_for_timeout(dwell_ms + 3000)
                        await self.shot(page, "05_atc")
                        await self.snapshot(page, "atc")
                        # Open the cart: page unload flushes batched pixel/GA4 hits (add_to_cart can be sent late)
                        # and the cart page adds view_cart. Still tagged phase "atc".
                        try:
                            cart = urljoin(page.url, "/cart")
                            if "/cart" not in page.url:
                                await page.goto(cart, wait_until="domcontentloaded", timeout=45000)
                            await self.settle(page, dwell_ms)
                        except Exception as e:
                            self.say(f"cart page warning: {e}")
                else:
                    self.say("no product link found on homepage")

            await self.drain()

            # First-party cookie names (never values) set by the visit: click-ID / identity storage checks.
            try:
                self.meta["cookies_after"] = sorted({c["name"] for c in await context.cookies([page.url or self.url])})[:300]
            except Exception:
                pass

            # Fallback: any container ID referenced but not captured -> fetch it directly.
            seen_ids = set(sig.GOOGLE_ID_RE["gtm"].findall(html))
            for snap in self.snapshots.values():
                seen_ids |= {k for k in snap.get("google_tag_manager_keys") or [] if k.startswith("GTM-")}
            for r in self.requests:
                m = re.search(r"[?&]id=(GTM-[A-Z0-9]+)", r["url"])
                if m:
                    seen_ids.add(m.group(1))
            for cid in sorted(seen_ids - set(self.containers)):
                await self.direct_fetch(context, cid)
        finally:
            await self.drain()
            await page.close()

        self.meta["finished"] = datetime.now(timezone.utc).isoformat()
        self.review_coverage()
        self.write(html)

    def write(self, html: str):
        cdir, rdir = self.out / "containers", self.out / "raw"
        cdir.mkdir(exist_ok=True)
        rdir.mkdir(exist_ok=True)
        for cid, c in self.containers.items():
            cid = re.sub(r"[^\w.-]+", "_", cid)
            (cdir / f"{cid}.js").write_text(c["body"], encoding="utf-8")
            (cdir / f"{cid}.json").write_text(json.dumps(c["data"], indent=1, ensure_ascii=False), encoding="utf-8")
        (rdir / "network.json").write_text(redact(json.dumps(self.requests, indent=1, ensure_ascii=False)), encoding="utf-8")
        (rdir / "initiators.json").write_text(json.dumps(self.initiators, indent=0, ensure_ascii=False), encoding="utf-8")
        if html:
            (rdir / "page.html").write_text(redact(html), encoding="utf-8")
        capture = {
            **self.meta,
            "containers": [
                {k: v for k, v in c.items() if k not in ("body", "data")} | {"size_kb": round(len(c["body"].encode()) / 1024, 1)}
                for c in self.containers.values()
            ],
            "request_count": len(self.requests),
            "snapshots": self.snapshots,
            "log": self.log,
        }
        (rdir / "capture.json").write_text(json.dumps(capture, indent=1, ensure_ascii=False), encoding="utf-8")
        self.say(f"saved {len(self.requests)} requests, {len(self.containers)} container(s) -> {self.out}")


PROFILE_DIR = ".browser-profile"


async def _launch_persistent(p, profile: Path, headless: bool):
    """One persistent Chrome profile for every audit: cookies, consent choices and bot-check clearance
    are stored on disk and reused, so banners don't have to be re-accepted on every run."""
    profile.mkdir(parents=True, exist_ok=True)
    kwargs = dict(
        headless=headless, args=["--disable-blink-features=AutomationControlled"],
        user_agent=UA, viewport={"width": 1440, "height": 900}, locale="en-US",
        timezone_id="America/Los_Angeles",
    )
    try:
        return await p.chromium.launch_persistent_context(str(profile), channel="chrome", **kwargs)
    except Exception:
        return await p.chromium.launch_persistent_context(str(profile), **kwargs)


async def capture_all(brands: list[tuple[str, str]], out_root: Path, headless=False,
                      dwell_ms=5000, pdp=True, parallel=3, fresh=False, profile: Path | None = None):
    sem = asyncio.Semaphore(max(1, parallel))
    profile = profile or Path(PROFILE_DIR).resolve()
    async with async_playwright() as p:
        context = await _launch_persistent(p, profile, headless)
        await context.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        print(f"browser profile: {profile}", flush=True)

        async def one(slug, url):
            async with sem:
                cap = BrandCapture(slug, url, out_root)
                try:
                    await asyncio.wait_for(cap.run(context, dwell_ms, pdp, fresh), timeout=600)
                except asyncio.TimeoutError:
                    cap.say("TIMEOUT after 10 min - writing partial capture (flagged for review)")
                    cap.meta["error"] = "timeout"
                    cap.review_coverage()
                    cap.meta["review"]["needs_review"] = True
                    cap.meta["review"]["reasons"].append("capture timed out (partial data)")
                    cap.write("")
                except Exception as e:
                    cap.say(f"ERROR {e}")
                    cap.meta["error"] = str(e)
                    cap.write("")

        await asyncio.gather(*(one(s, u) for s, u in brands))
        try:  # closing the last tab of a persistent Chrome profile can already shut the browser down
            await context.close()
        except Exception:
            pass
