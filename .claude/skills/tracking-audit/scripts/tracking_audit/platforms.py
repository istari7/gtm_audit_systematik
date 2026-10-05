"""Platform-level tracking evaluation: GA4, Google Ads, Meta, TikTok, Pinterest, Microsoft Ads, Klaviyo, others.

Works from the raw network log (every hit, with POST bodies) + page snapshots + cookie names, independent
of how the tags were deployed (GTM, Shopify app pixel, custom pixel, hard-coded). For each platform it
extracts the events actually sent per visit phase and the data they carried, then scores them against
best practice with the same check structure as best_practices.py:

  area (= platform), check, status, impact, evidence, recommendation, why

Phases: initial (pre-consent) · reload (post-consent page load) · pdp (product page) · atc (after add-to-cart).
"""

import json
import re
from collections import Counter, defaultdict
from urllib.parse import parse_qsl, unquote, urlparse

from .best_practices import score
from .network import SANDBOX_RX, _hit_lines, _is_ga4_hit, classify
from .sources import SourceResolver, category, significant_routes

ECOM_SITE_EVENTS = {"view_item", "add_to_cart"}
TRUNCATED_AT = 6000
META_STANDARD = {"PageView", "ViewContent", "AddToCart", "InitiateCheckout", "AddPaymentInfo", "Purchase", "Search",
                 "Lead", "CompleteRegistration", "AddToWishlist", "Subscribe"}
FP_COOKIES = {
    "GA4": ["_ga"], "Google Ads": ["_gcl_au", "_gcl_aw"], "Meta": ["_fbp", "_fbc"], "TikTok": ["_ttp"],
    "Pinterest": ["_epik", "_pin_unauth"], "Microsoft Ads": ["_uetsid", "_uetvid"], "Klaviyo": ["__kla_id"],
    "Snapchat": ["_scid"], "Reddit": ["_rdt_uuid"],
}


def _q(url: str) -> dict:
    return dict(parse_qsl(urlparse(url).query, keep_blank_values=True))


class Hits:
    """Normalised events per platform: list of {phase, event, id, params:dict, raw}."""

    def __init__(self, requests: list[dict], resolver=None):
        self.ev = defaultdict(list)
        self.resolver = resolver
        self._r = None
        for r in requests:
            try:
                self._one(r)
            except Exception:
                continue

    def add(self, platform, phase, event, pid=None, source=None, **params):
        if source is None:
            source = self.resolver.for_request(self._r, platform, pid) if self.resolver else "Unattributed"
        self.ev[platform].append({"phase": phase, "event": event, "id": pid, "source": source, "params": params})

    def _one(self, r):
        self._r = r
        url, body, ph = r["url"], r.get("post") or "", r.get("phase")
        host = (urlparse(url).hostname or "").lower()
        path = urlparse(url).path
        if _is_ga4_hit(url):
            for e in _hit_lines(r):
                self.add("GA4", ph, e.get("en") or "(none)", e.get("tid"),
                         items="pr1" in e, currency=bool(e.get("cu")), value=bool(e.get("epn.value") or e.get("ep.value")),
                         gcs=e.get("gcs"), dl=e.get("dl", ""), sandbox=bool(SANDBOX_RX.search(r.get("frame") or "")),
                         user_data=bool(e.get("em") or e.get("ecid") or e.get("_eu") and "em" in e.get("_eu", "")),
                         transaction_id=bool(e.get("ep.transaction_id")))
            return
        if "facebook.com" in host and path.startswith("/tr"):
            truncated = len(body) == TRUNCATED_AT  # body cut at the old 6000-char capture limit: eid may be missing
            for src, is_body in ((_q(url), False), (dict(parse_qsl(body)) if "ev=" in body else {}, True)):
                if src.get("ev"):
                    keys = " ".join(src)
                    agent = src.get("a") or ""
                    marker = ("Shopify app: Meta (Facebook & Instagram)" if agent == "shopify_web_pixel" else
                              "Shopify custom pixel" if agent == "shopify_custom_pixel" else None)
                    self.add("Meta", ph, src["ev"], src.get("id"), source=marker,
                             eid=bool(src.get("eid")) if not (is_body and truncated) else None,
                             content_ids="cd[content_ids]" in keys or "cd[contents]" in keys,
                             value="cd[value]" in keys, currency="cd[currency]" in keys,
                             advanced_matching="ud[" in keys)
            return
        if "analytics.tiktok.com" in host and body:
            codes = re.findall(r'"pixel_code"\s*:\s*"([A-Z0-9]+)"', body) or re.findall(r'"code"\s*:\s*"([A-Z0-9]{15,})"', body)
            for evn in re.findall(r'"event"\s*:\s*"([^"]+)"', body):
                self.add("TikTok", ph, evn, codes[0] if codes else None,
                         source="Shopify app: TikTok" if re.search(r'"partner"\s*:\s*"Shopify"', body) else None,
                         eid=bool(re.search(r'"event_id"\s*:\s*"[^"]+"', body)),
                         content_ids=bool(re.search(r'"content_id"|"contents"', body)),
                         value=bool(re.search(r'"(value|price)"', body)), currency='"currency"' in body,
                         advanced_matching=bool(re.search(r'"(email|phone_number|sha256_email)"\s*:\s*"[^"]+"', body)))
            return
        if "ct.pinterest.com" in host:
            q = _q(url)
            if body and ("ed=" in body or "event=" in body):  # Shopify app pixel POSTs form-encoded events
                q.update(dict(parse_qsl(body, keep_blank_values=True)))
            ed = unquote(q.get("ed", "")) + unquote(q.get("pd", ""))
            if q.get("event") or "/v3" in path:
                self.add("Pinterest", ph, q.get("event", "pagevisit"), q.get("tid"),
                         source="Shopify app: Pinterest" if "shopify-web-pixel" in ed else None,
                         eid=bool(re.search(r'"event_?id"', ed, re.I)) or bool(q.get("eid")),
                         content_ids="product_id" in ed or "line_items" in ed,
                         value='"value"' in ed or '"product_price"' in ed,
                         currency="currency" in ed, advanced_matching="em" in unquote(q.get("pd", "")))
            return
        if host.startswith("bat.bing.") and "/action/" in path:
            q = _q(url)
            evn = q.get("ea") or q.get("evt") or "?"
            self.add("Microsoft Ads", ph, evn, q.get("ti"), consent=q.get("asc"),
                     content_ids=bool(q.get("prodid") or q.get("ecomm_prodid") or "items" in url),
                     value=bool(q.get("gv") or q.get("ev")), currency=bool(q.get("gc")), pagetype=q.get("pagetype"))
            return
        if any(h in host for h in ("googleadservices.com", "googleads.g.doubleclick.net")) or \
           (host.endswith("google.com") and ("/rmkt/" in path or "/pagead/" in path or "/ccm/" in path)):
            m = re.search(r"/(?:1p-)?(?:conversion|viewthroughconversion|rmkt/collect|user-list)/(\d+)", path)
            q = _q(url)
            data = unquote(q.get("data", ""))
            evn = q.get("en") or (re.search(r"event=([^;]+)", data).group(1) if "event=" in data else None) \
                or ("conversion" if q.get("label") else "remarketing")
            self.add("Google Ads", ph, evn, f"AW-{m.group(1)}" if m else None, label=q.get("label"),
                     content_ids="ecomm_prodid" in data or "item_id" in data or "pr1" in url or "items" in data,
                     value=bool(q.get("value")), currency=bool(q.get("currency_code")),
                     user_data="em=" in url or "&em" in body, gcs=q.get("gcs"))
            return
        if "klaviyo.com" in host:
            if "/client/events" in path and body:
                for name in re.findall(r'"name"\s*:\s*"([^"]+)"', body):
                    if name[0].isupper():
                        self.add("Klaviyo", ph, name, None)
            elif "/onsite/js/" in path:
                self.add("Klaviyo", ph, "(onsite.js loaded)", _q(url).get("company_id"))
            return
        vendor, cat = classify(url)
        if vendor in ("Snapchat Pixel", "Reddit Pixel", "X (Twitter) Pixel", "AppLovin", "Criteo", "The Trade Desk"):
            name = vendor.replace(" Pixel", "")
            evn = None
            for pat in (r'"event_type"\s*:\s*"([^"]+)"', r'"event"\s*:\s*"([^"]+)"', r"[?&]event=([^&]+)", r"[?&]ev=([^&]+)"):
                mm = re.search(pat, url + "\n" + body)
                if mm:
                    evn = unquote(mm.group(1))
                    break
            self.add(name, ph, evn or "(request)", None)


class PlatformChecks:
    def __init__(self, audit: dict, requests: list[dict], initiators: list[dict] | None = None, html: str = ""):
        self.audit, self.net, self.cap = audit, audit["network"], audit["capture"]
        shopify = audit["brand"].get("platform") == "Shopify"
        self.resolver = SourceResolver(initiators or [], self.net["web_pixels"], self.net["site_host"], shopify, html)
        self.h = Hits(requests, self.resolver)
        self.cookies = set(self.cap.get("cookies_after") or [])
        self.ecommerce = (audit["brand"].get("platform") == "Shopify") or bool(self.cap.get("pdp_url"))
        self.pdp = bool(self.cap.get("pdp_url"))
        adds = [s for s in self.net.get("atc_cart_add_status") or [] if isinstance(s, int)]
        self.atc_ok = bool(adds) and any(200 <= s < 300 for s in adds)
        self.atc_redirect = bool(adds) and all(300 <= s < 400 for s in adds)
        self.results: dict[str, list] = {}

    def add(self, platform, check, status, impact, evidence, rec="", why=""):
        self.results.setdefault(platform, []).append({"area": platform, "check": check, "status": status, "impact": impact,
                                                      "evidence": evidence, "recommendation": rec, "why": why})

    def events(self, platform, phase=None, name=None):
        return [e for e in self.h.ev.get(platform, []) if (phase is None or e["phase"] == phase)
                and (name is None or e["event"].lower() in {n.lower() for n in ([name] if isinstance(name, str) else name)})]

    def cookie_check(self, platform):
        names = FP_COOKIES.get(platform, [])
        if not names or not self.cap.get("cookies_after"):
            return
        found = [n for n in names if n in self.cookies]
        self.add(platform, "First-party ID cookie set", "pass" if found else "warn", "Medium",
                 f"Cookies after the visit: {', '.join(found) or 'none of ' + ', '.join(names)}.",
                 "" if found else "Check the tag/app is allowed to set first-party cookies (consent, ITP, cookie flags).",
                 "First-party IDs keep attribution and audiences working as third-party cookies disappear.")

    def ecommerce_event(self, platform, view_names, atc_names, needs=("content_ids", "value", "currency")):
        """view_item / add_to_cart equivalents: present + carry product, value, currency."""
        if not self.ecommerce:
            return
        for label, names, phase, gate in (("Product view", view_names, "pdp", self.pdp),
                                          ("Add to cart", atc_names, "atc", self.atc_ok or self.atc_redirect)):
            if not gate:
                continue
            evs = self.events(platform, phase, names)
            if not evs:
                status = "warn" if (phase == "atc" and self.atc_redirect) else "fail"
                self.add(platform, f"{label} event sent ({'/'.join(names[:2])})", status, "High",
                         f"No {'/'.join(names)} event in the {phase} phase"
                         + (" (cart add redirected — verify in the platform's debugger)." if status == "warn" else "."),
                         f"Send {names[0]} on {'product pages' if phase == 'pdp' else 'every cart add (incl. drawer/AJAX carts)'}.",
                         "Product-level events drive dynamic ads, retargeting audiences and value-based optimisation.")
                continue
            if phase == "atc":
                per_id = Counter(e["id"] for e in evs)
                dup = {k: v for k, v in per_id.items() if v > 1}
                self.add(platform, "Add to cart sent once per cart add", "warn" if dup else "pass", "Medium",
                         ("Sent " + ", ".join(f"{v}× to {k or platform}" for k, v in dup.items()) + " for a single cart add.")
                         if dup else f"{evs[0]['event']} sent once per destination.",
                         "Find the second trigger (app + theme script, or two listeners) and keep one." if dup else "",
                         "Double add-to-cart events inflate funnel rates and remarketing audience signals.")
            miss = [n for n in needs if not any(e["params"].get(n) for e in evs)]
            self.add(platform, f"{label} event carries {', '.join(needs)}", "warn" if miss else "pass", "Medium",
                     f"{evs[0]['event']} sent ({len(evs)}×)" + (f"; missing: {', '.join(miss)}." if miss else " with product, value and currency."),
                     f"Add {', '.join(miss)} to {evs[0]['event']}." if miss else "",
                     "Without product IDs and value the platform can't run catalogue ads or optimise for revenue.")

    def duplicate_check(self, platform, pv_names):
        pv = self.events(platform, "reload", pv_names)
        per_id = Counter(e["id"] for e in pv)
        dups = {k: v for k, v in per_id.items() if v > 1}
        if per_id:
            srcs = {k: sorted({e["source"] for e in pv if e["id"] == k}) for k in dups}
            self.add(platform, "Page view sent once per load", "fail" if dups else "pass", "High",
                     ("Duplicates on one page load: " + "; ".join(f"{k}×{v} (from {', '.join(srcs[k])})" for k, v in dups.items()))
                     if dups else
                     f"{', '.join(f'{k}×{v}' for k, v in per_id.items())} on one page load.",
                     "Remove the second source (app vs GTM vs hard-coded / custom pixel)." if dups else "",
                     "Double page views inflate traffic and deflate conversion rates; for ad pixels they distort optimisation.")

    def ids_check(self, platform, label="ID"):
        ids = sorted({e["id"] for e in self.h.ev.get(platform, []) if e["id"]})
        if len(ids) > 1:
            self.add(platform, f"Single {label}", "warn", "Medium", f"{len(ids)} {label}s receive data: {', '.join(ids)}.",
                     "Confirm each is owned and in use; retire leftovers from agencies or old accounts.",
                     "Extra IDs split audiences and send customer data to accounts nobody watches.")
        elif ids:
            self.add(platform, f"Single {label}", "pass", "Low", f"{label}: {ids[0]}.")
        return ids

    # ── platforms ────────────────────────────────────────────────────────────
    def ga4(self):
        evs = self.h.ev.get("GA4", [])
        if not evs:
            if self.net["vendors"]:
                self.add("GA4", "GA4 collecting data", "fail", "High", "No GA4 hits observed during the visit.",
                         "Install GA4 (Shopify Google & YouTube app or GTM).", "GA4 is the free system of record for traffic and revenue.")
            return
        ids = self.ids_check("GA4", "GA4 property")
        by_id = defaultdict(Counter)
        for e in evs:
            if e["id"]:
                by_id[e["id"]][e["source"]] += 1
        multi = {t: c for t, c in by_id.items() if len(significant_routes(c)) > 1}
        self.add("GA4", "One implementation per property", "fail" if multi else "pass", "High",
                 ("; ".join(f"{t} <- " + ", ".join(f"{src} x{n}" for src, n in c.most_common()) for t, c in multi.items()))
                 if multi else "; ".join(f"{t} <- {', '.join(c)}" for t, c in by_id.items()),
                 "Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM "
                 "carries a richer setup (then switch GA4 off in the app)." if multi else "",
                 "Two implementations double-count events and revenue.")
        self.duplicate_check("GA4", "page_view")
        bad_dl = sorted({e["id"] for e in evs if SANDBOX_RX.search(e["params"]["dl"] or "")})
        self.add("GA4", "page_location is the real page URL", "fail" if bad_dl else "pass", "High",
                 f"Sandbox URL recorded as page_location for {', '.join(bad_dl)}." if bad_dl else "page_location values are storefront URLs.",
                 "In the custom pixel set page_location/page_title from event.context.document." if bad_dl else "",
                 "Wrong page_location breaks page, landing-page and channel reports.")
        self.ecommerce_event("GA4", ["view_item"], ["add_to_cart"], needs=("items", "value", "currency"))
        gcs = {e["params"]["gcs"] for e in evs if e["params"].get("gcs")}
        self.add("GA4", "Consent Mode signals on hits", "pass" if gcs else "warn", "Medium",
                 f"gcs states seen: {', '.join(sorted(gcs))}." if gcs else "No gcs parameter on any GA4 hit.",
                 "" if gcs else "Implement Consent Mode v2 (default + update).",
                 "Needed for EU/UK traffic and for Google's conversion modelling.")
        engaged = {e["event"] for e in evs} & {"user_engagement", "scroll"}
        self.add("GA4", "Engagement / enhanced measurement events", "pass" if engaged else "info", "Low",
                 f"Seen: {', '.join(sorted(engaged)) or 'none'}.")
        self.cookie_check("GA4")

    def google_ads(self):
        evs = self.h.ev.get("Google Ads", [])
        if not evs:
            return
        self.ids_check("Google Ads", "Google Ads account")
        feats = {f["function"] for c in self.audit["containers"] for f in c.get("gtag_features", [])}
        ec = any(e["params"].get("user_data") for e in evs) or bool({"__ogt_1p_data_v2", "__ccd_add_1p_data"} & feats) or \
            any(t["function"] in ("__awec", "__awud") for c in self.audit["containers"] for t in c.get("tags", []))
        self.add("Google Ads", "Enhanced conversions enabled", "pass" if ec else "warn", "Medium",
                 "User-provided data collection is configured." if ec else "No enhanced-conversions configuration or user data seen.",
                 "" if ec else "Turn on enhanced conversions (Google & YouTube app setting or GTM user-provided data).",
                 "Recovers conversions lost to cookie restrictions and improves bidding.")
        dyn = any(e["params"].get("content_ids") for e in evs if e["phase"] in ("pdp", "atc"))
        if self.ecommerce and self.pdp:
            self.add("Google Ads", "Dynamic remarketing sends product IDs", "pass" if dyn else "warn", "Medium",
                     "Product IDs present on product-page / cart hits." if dyn else "No product IDs on Ads hits from the product page or cart.",
                     "" if dyn else "Send items (id matching the Merchant Center feed) with view_item / add_to_cart.",
                     "Dynamic remarketing and PMax product audiences need product IDs that match the feed.")
        if self.ecommerce and (self.atc_ok or self.atc_redirect):
            atc = [e for e in evs if e["phase"] == "atc"]
            self.add("Google Ads", "Add-to-cart signal reaches Google Ads", "pass" if atc else "info", "Low",
                     f"{len(atc)} Ads hit(s) after add-to-cart." if atc else "No Ads hit after add-to-cart.",
                     "" if atc else "Optional: send add_to_cart for remarketing audiences / secondary conversion.")
        self.cookie_check("Google Ads")

    def meta(self):
        evs = self.h.ev.get("Meta", [])
        if not evs:
            if "Meta Pixel" in self.net["vendors"]:
                self.add("Meta", "Meta events observed", "info", "Low",
                         "Meta pixel script loads but no /tr events were captured (may be sent via Conversions API only).")
            return
        self.ids_check("Meta", "Meta pixel")
        self.duplicate_check("Meta", "PageView")
        self.ecommerce_event("Meta", ["ViewContent"], ["AddToCart"])
        std = [e for e in evs if e["event"] in META_STANDARD and e["params"]["eid"] is not None]
        with_eid = sum(1 for e in std if e["params"]["eid"])
        self.add("Meta", "event_id on standard events (CAPI dedupe)",
                 "info" if not std else "pass" if with_eid == len(std) else "warn" if with_eid else "fail", "High",
                 f"{with_eid} of {len(std)} standard events ({', '.join(sorted({e['event'] for e in std}))}) carry event_id."
                 + (" Missing on events from: " + ", ".join(sorted({e["source"] for e in std if not e["params"]["eid"]})) + "."
                    if with_eid < len(std) else ""),
                 "" if std and with_eid == len(std) else "Send a shared event_id with every standard event and its Conversions API twin.",
                 "Without event_id, pixel + Conversions API events double-count and Meta's optimisation degrades.")
        am = any(e["params"]["advanced_matching"] for e in evs)
        self.add("Meta", "Advanced matching", "pass" if am else "info", "Low",
                 "Hashed user data seen on events." if am else "No advanced-matching data (normal for anonymous visitors).",
                 "" if am else "Enable automatic advanced matching so logged-in / checkout users are matched.")
        self.cookie_check("Meta")

    def tiktok(self):
        evs = self.h.ev.get("TikTok", [])
        if not evs:
            return
        self.ids_check("TikTok", "TikTok pixel")
        self.duplicate_check("TikTok", ["Pageview", "PageView"])
        self.ecommerce_event("TikTok", ["ViewContent"], ["AddToCart"])
        eid = any(e["params"]["eid"] for e in evs)
        self.add("TikTok", "event_id for Events API dedupe", "pass" if eid else "warn", "Medium",
                 "event_id present." if eid else "No event_id on browser events.",
                 "" if eid else "Pass event_id so browser and Events API events dedupe.",
                 "Prevents double-counted conversions when Events API is on.")
        self.cookie_check("TikTok")

    def pinterest(self):
        evs = self.h.ev.get("Pinterest", [])
        if not evs:
            return
        self.ids_check("Pinterest", "Pinterest tag")
        self.duplicate_check("Pinterest", "pagevisit")
        self.ecommerce_event("Pinterest", ["pagevisit"], ["addtocart"])
        self.cookie_check("Pinterest")

    def microsoft(self):
        evs = self.h.ev.get("Microsoft Ads", [])
        if not evs:
            return
        self.ids_check("Microsoft Ads", "UET tag")
        self.duplicate_check("Microsoft Ads", "pageLoad")
        if self.ecommerce and self.pdp:
            prod = any(e["params"]["content_ids"] for e in evs if e["phase"] in ("pdp", "atc"))
            self.add("Microsoft Ads", "Product IDs for dynamic remarketing", "pass" if prod else "warn", "Low",
                     "ecomm_prodid / items present." if prod else "No product IDs on UET hits from product pages.",
                     "" if prod else "Send ecomm_prodid + ecomm_pagetype (Shopping / dynamic remarketing).")
        consent = {e["params"].get("consent") for e in evs if e["params"].get("consent")}
        self.add("Microsoft Ads", "UET Consent Mode signal", "pass" if consent else "info", "Low",
                 f"asc={', '.join(sorted(consent))}." if consent else "No UET consent (asc) parameter.",
                 "" if consent else "Enable UET Consent Mode if serving EU/UK traffic.")
        self.cookie_check("Microsoft Ads")

    def klaviyo(self):
        evs = self.h.ev.get("Klaviyo", [])
        if not evs and "Klaviyo" not in self.net["vendors"]:
            return
        onsite = any(e["event"] == "(onsite.js loaded)" for e in evs)
        self.add("Klaviyo", "Onsite tracking (klaviyo.js) loaded", "pass" if onsite or evs else "warn", "Medium",
                 "klaviyo.js loads." if onsite else "Klaviyo requests seen but onsite.js not identified.")
        if self.ecommerce and self.pdp:
            viewed = [e for e in evs if e["event"] == "Viewed Product"]
            self.add("Klaviyo", "Viewed Product tracked (browse abandonment)", "pass" if viewed else "info", "Medium",
                     f"Viewed Product sent {len(viewed)}×." if viewed else
                     "No Viewed Product event (only identified profiles are tracked — anonymous visitors expected to show none).",
                     "" if viewed else "Confirm Viewed Product is enabled in the Klaviyo Shopify integration.",
                     "Browse- and cart-abandonment flows are among the highest-ROI email/SMS flows.")
        self.cookie_check("Klaviyo")

    def others(self):
        for name in ("Snapchat", "Reddit", "X (Twitter)", "AppLovin", "Criteo", "The Trade Desk"):
            evs = self.h.ev.get(name, [])
            if evs:
                names = Counter(e["event"] for e in evs)
                self.add(name, "Pixel active", "info", "Low",
                         f"{sum(names.values())} hit(s): " + ", ".join(f"{k}×{v}" for k, v in names.most_common(6)) + ".")

    def deployment(self):
        shopify = self.audit["brand"].get("platform") == "Shopify"
        native = {"GA4", "Google Ads", "Meta", "TikTok", "Pinterest", "Microsoft Ads"}
        for platform, evs in self.h.ev.items():
            if not evs or (platform not in self.results and platform not in native):
                continue
            src = Counter(e["source"] for e in evs)
            cats = significant_routes(src)
            evidence = "; ".join(f"{k} x{v}" for k, v in src.most_common())
            if len(cats) > 1:
                rec = ("On Shopify, keep the native app integration (server-side events, consent API, maintained by the "
                       "platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't."
                       if shopify and "Shopify app" in cats else "Consolidate to one deployment route per platform.")
                self.add(platform, "Single deployment route", "warn", "High", f"Hits come from {len(cats)} routes: {evidence}.",
                         rec, "Parallel routes double-count, drift apart, and make consent handling inconsistent.")
            else:
                note = ""
                if shopify and platform in native and cats and cats <= {"GTM", "Theme"}:
                    note = (" Native Shopify app not used for this platform - the app would add server-side events "
                            "(CAPI / Events API) and Shopify consent handling.")
                self.add(platform, "Deployment route", "info", "Low", f"Sent via: {evidence}.{note}")

    def stack(self):
        v = self.net["vendors"]
        replay = sorted(k for k, x in v.items() if x["category"] == "session-replay")
        ads = sorted(k for k, x in v.items() if x["category"] == "advertising")
        self.add("Stack", "Session-replay tools", "warn" if len(replay) > 1 else "pass" if replay else "info", "Low",
                 f"{len(replay)}: {', '.join(replay) or 'none'}.",
                 "Keep one session-replay tool." if len(replay) > 1 else "",
                 "Each replay tool records the full DOM — performance cost and PII exposure.")
        self.add("Stack", "Ad platforms in use", "info", "Low", f"{len(ads)}: {', '.join(ads)}.")
        third = self.net["totals"]["third_party"]
        self.add("Stack", "Third-party request volume", "warn" if third > 1000 else "pass", "Low",
                 f"{third} third-party requests across the visit ({self.net['totals']['vendors']} identified platforms).",
                 "Audit apps/pixels that don't earn their weight." if third > 1000 else "",
                 "Tag weight slows pages, which costs conversion rate.")

    def run(self) -> dict:
        for step in (self.ga4, self.google_ads, self.meta, self.tiktok, self.pinterest, self.microsoft,
                     self.klaviyo, self.others, self.deployment, self.stack):
            try:
                step()
            except Exception as e:
                self.add("Internal", step.__name__, "info", "Low", f"check error: {e}")
        out = {}
        for platform, checks in self.results.items():
            evs = self.h.ev.get(platform, [])
            out[platform] = {
                "checks": checks, **score(checks),
                "sources": dict(Counter(e["source"] for e in evs)),
                "events_by_phase": {ph: dict(Counter(e["event"] for e in evs if e["phase"] == ph))
                                    for ph in ("initial", "reload", "pdp", "atc") if any(e["phase"] == ph for e in evs)},
            }
        all_checks = [c for p in out.values() for c in p["checks"]]
        out["_overall"] = score(all_checks)
        return out


def evaluate_platforms(audit: dict, requests: list[dict], initiators: list[dict] | None = None, html: str = "") -> dict:
    return PlatformChecks(audit, requests, initiators, html).run()
