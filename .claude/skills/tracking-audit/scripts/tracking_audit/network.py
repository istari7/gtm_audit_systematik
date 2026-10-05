"""Analyse intercepted network traffic: vendors, IDs, GA4/Meta/TikTok hits, consent, sGTM."""

import json
import re
from collections import Counter, defaultdict
from urllib.parse import parse_qsl, urlparse

from . import signatures as sig

GOOGLE_HOSTS = ("google-analytics.com", "analytics.google.com", "googletagmanager.com", "doubleclick.net",
                "google.com", "googleadservices.com", "googlesyndication.com", "gstatic.com", "googleapis.com")
IGNORED_FAILURES = ("ERR_ABORTED", "NS_BINDING_ABORTED", "ERR_BLOCKED_BY_CLIENT", "ERR_CACHE_MISS")
TID_VENDORS = {"Google Analytics 4", "Universal Analytics", "Google tag", "Google Tag Manager"}
PHASES = ["initial", "consent", "reload", "pdp", "atc", "direct_fetch"]


def base_domain(host: str) -> str:
    parts = (host or "").lower().split(".")
    if len(parts) >= 3 and parts[-2] in ("co", "com", "org", "net") and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def classify(url: str) -> tuple[str | None, str | None]:
    u = urlparse(url)
    host = (u.hostname or "").lower()
    hp = host + u.path.lower()
    for pattern, vendor, cat in sig.VENDORS:
        p = pattern.lower()
        if ("/" in p and p in hp) or ("/" not in p and p in host):
            return vendor, cat
    return None, None


def _is_ga4_hit(url: str) -> bool:
    u = urlparse(url)
    return ("/g/collect" in u.path or u.path.endswith("/collect")) and "tid=G-" in url


def _hit_lines(rec: dict) -> list[dict]:
    """GA4 hits: URL query holds shared params; POST body holds one event per line."""
    base = dict(parse_qsl(urlparse(rec["url"]).query, keep_blank_values=True))
    body = rec.get("post") or ""
    lines = [l for l in body.split("\r\n") if l] if body and "en=" in body else []
    if not lines:
        return [base]
    out = []
    for l in lines:
        ev = dict(base)
        ev.update(dict(parse_qsl(l, keep_blank_values=True)))
        out.append(ev)
    return out


def parse_web_pixels(html: str) -> list[dict]:
    """Shopify Customer Events config hard-coded in the page (app + custom pixels)."""
    i = html.find("webPixelsConfigList")
    if i < 0:
        return []
    j = html.find("[", i)
    if j < 0:
        return []
    try:
        arr, _ = json.JSONDecoder().raw_decode(html, j)
    except ValueError:
        # Some themes HTML-escape the inline JSON.
        try:
            arr, _ = json.JSONDecoder().raw_decode(html.replace("&quot;", '"'), j)
        except ValueError:
            return []
    pixels = []
    for p in arr if isinstance(arr, list) else []:
        cfg_raw = p.get("configuration") or ""
        try:
            cfg = json.loads(cfg_raw) if isinstance(cfg_raw, str) and cfg_raw.startswith("{") else cfg_raw
        except ValueError:
            cfg = cfg_raw
        text = cfg_raw if isinstance(cfg_raw, str) else json.dumps(cfg_raw)
        ids = sorted({x for rx in sig.GOOGLE_ID_RE.values() for x in rx.findall(text)})
        pixels.append({
            "id": p.get("id"),
            "type": p.get("type"),
            "api_client_id": p.get("apiClientId"),
            "runtime": p.get("runtimeContext"),
            "purposes": p.get("privacyPurposes"),
            "app": _guess_pixel_app(cfg, text),
            "google_ids": ids,
            "configuration": cfg if len(text) < 600 else text[:600] + "…",
        })
    return pixels


PIXEL_APP_KEYWORDS = [
    ("facebook", "Meta (Facebook & Instagram)"), ("pixelcode", "TikTok"), ("tiktok", "TikTok"),
    ("snapchat", "Snapchat"), ("reddit", "Reddit"), ("adscale", "AdScale"), ("global-e", "Global-e"),
    ("triplewhale", "Triple Whale"), ("triple-whale", "Triple Whale"), ("elevar", "Elevar"), ("northbeam", "Northbeam"),
    ("littledata", "Littledata"), ("attentive", "Attentive"), ("postscript", "Postscript"), ("yotpo", "Yotpo"),
    ("okendo", "Okendo"), ("criteo", "Criteo"), ("impact", "Impact"), ("polar", "Polar Analytics"),
    ("microsoft", "Microsoft Ads"), ("bing", "Microsoft Ads"), ("klaviyo", "Klaviyo"), ("pinterest", "Pinterest"),
    ("applovin", "AppLovin"), ("axon", "AppLovin"),
]


def _guess_pixel_app(cfg, text: str) -> str | None:
    t = text.lower()
    if "google_tag_ids" in t or re.search(r"\b(G|AW|GT)-[A-Z0-9]{6,}", text):
        return "Google & YouTube"
    for kw, app in PIXEL_APP_KEYWORDS:
        if kw in t:
            return app
    if isinstance(cfg, dict):
        if re.fullmatch(r"[A-Za-z0-9]{6}", str(cfg.get("accountID") or cfg.get("accountId") or "")):
            return "Klaviyo"
        if re.fullmatch(r"\d{12,14}", str(cfg.get("tagID") or cfg.get("tagId") or "")):
            return "Pinterest"
        if re.fullmatch(r"\d{14,16}", str(cfg.get("pixel_id") or cfg.get("pixelId") or "")):
            return "Meta (Facebook & Instagram)"
    return None


_SCRIPT_TAG = re.compile(r"<script\b([^>]*)>", re.I)
_ATTR = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')


def gated_scripts(html: str) -> list[dict]:
    """Scripts parked until consent: type=text/plain|text/template (+ data-consent / data-cookieconsent /
    optanon-category-* / data-category). These only execute after the CMP flips them."""
    out = []
    for m in _SCRIPT_TAG.finditer(html):
        attrs = {k.lower(): v for k, v in _ATTR.findall(m.group(1))}
        typ = attrs.get("type", "").lower()
        if typ not in ("text/plain", "text/template", "text/x-template") and not attrs.get("data-cookieconsent"):
            continue
        category = (attrs.get("data-consent") or attrs.get("data-cookieconsent") or attrs.get("data-category")
                    or next((c for c in attrs.get("class", "").split() if c.startswith("optanon-category")), None))
        if not category:
            continue
        src = attrs.get("src") or attrs.get("data-src") or ""
        vendor = classify(src)[0] if src else None
        out.append({"category": category, "src": src[:200] or "(inline)", "vendor": vendor})
    return out[:60]


# Connection-level errors are often the capture network (regional blocks, ad-blocking DNS, ORB), not the
# site. Kept in the report, but not turned into findings. HTTP errors and DNS failures are real.
ENV_FAILURES = ("ERR_CONNECTION_RESET", "ERR_SSL_PROTOCOL_ERROR", "ERR_CONNECTION_CLOSED", "ERR_TIMED_OUT",
                "ERR_BLOCKED_BY_ORB", "ERR_FAILED", "ERR_CONNECTION_REFUSED", "ERR_HTTP2_PROTOCOL_ERROR",
                "ERR_TOO_MANY_REDIRECTS")  # last: cookie-sync redirect loops (ad-tech noise)
# CMP markup present in the page even when no banner is shown to this visitor (geo-targeted banners).
HTML_CMPS = [("consent-cookie-directive", "Anowave Cookie Consent (Shopify app)"), ("shopify-pc__banner", "Shopify Privacy Banner"),
             ("otSDKStub", "OneTrust"), ("consent.cookiebot.com", "Cookiebot"), ("osano.js", "Osano"), ("consentmo", "Consentmo"),
             ("pandectes", "Pandectes"), ("enzuzo", "Enzuzo"), ("cookieyes", "CookieYes"), ("termly", "Termly")]
OPT_OUT_RX = re.compile(r"do not sell|your privacy choices|opt[- ]out of (?:the )?(?:sale|sharing)|limit the use of my", re.I)
SANDBOX_RX = re.compile(r"/web-pixels@|/wpm@|web-pixel-sandbox", re.I)
BANNER_CMPS = [("consent-cookie-directive", "Anowave Cookie Consent (Shopify app)"), ("onetrust", "OneTrust"),
               ("Cybot", "Cookiebot"), ("osano", "Osano"), ("didomi", "Didomi"), ("shopify-pc", "Shopify Privacy Banner"),
               ("cky", "CookieYes"), ("termly", "Termly"), ("iubenda", "iubenda"), ("ketch", "Ketch")]


def analyze_network(requests: list[dict], capture: dict, html: str) -> dict:
    final_url = capture.get("final_url") or capture.get("url") or ""
    site_host = urlparse(final_url).hostname or ""
    site_base = base_domain(site_host)

    vendors: dict[str, dict] = {}
    unknown = Counter()
    ga4 = defaultdict(lambda: {"endpoints": set(), "events": defaultdict(Counter), "gcs": defaultdict(set),
                               "gcd": set(), "page_views": Counter(), "hits": 0, "sandbox_hits": 0,
                               "sandbox_page_location": 0, "sources": Counter()})
    meta_events = defaultdict(lambda: defaultdict(Counter))
    tiktok_events = defaultdict(lambda: defaultdict(Counter))
    ads_hits = defaultdict(lambda: defaultdict(Counter))
    sgtm_endpoints = set()
    failures = []
    first_party = third_party = 0

    for r in requests:
        url = r["url"]
        if url.startswith(("data:", "blob:", "chrome-extension:")):
            continue
        host = (urlparse(url).hostname or "").lower()
        is_first = base_domain(host) == site_base
        first_party += is_first
        third_party += not is_first
        vendor, cat = classify(url)
        phase = r.get("phase", "?")
        hay = url + "\n" + (r.get("post") or "")

        if _is_ga4_hit(url):
            vendor, cat = "Google Analytics 4", "analytics"
            if not any(host.endswith(g) for g in GOOGLE_HOSTS):
                sgtm_endpoints.add(f"{host}{urlparse(url).path}")
            for ev in _hit_lines(r):
                tid = ev.get("tid")
                if not tid:
                    continue
                g = ga4[tid]
                g["hits"] += 1
                g["endpoints"].add(host)
                in_sandbox = SANDBOX_RX.search(r.get("frame") or "") is not None
                g["sandbox_hits"] += in_sandbox
                g["sandbox_page_location"] += bool(SANDBOX_RX.search(ev.get("dl") or ""))
                g["sources"]["Shopify custom pixel sandbox" if in_sandbox else "page"] += 1
                en = ev.get("en") or "(no event name)"
                g["events"][phase][en] += 1
                if ev.get("gcs"):
                    g["gcs"][phase].add(ev["gcs"])
                if ev.get("gcd"):
                    g["gcd"].add(ev["gcd"])
                if en == "page_view":
                    g["page_views"][phase] += 1

        if vendor == "Meta Pixel" and "facebook.com/tr" in url:
            q = dict(parse_qsl(urlparse(url).query))
            if q.get("id"):
                meta_events[q["id"]][phase][q.get("ev", "?")] += 1
        if vendor == "TikTok Pixel" and r.get("post"):
            code = re.search(r'"pixel_code"\s*:\s*"([A-Z0-9]+)"', r["post"])
            evn = re.search(r'"event"\s*:\s*"([^"]+)"', r["post"])
            if code:
                tiktok_events[code.group(1)][phase][evn.group(1) if evn else "?"] += 1
        if vendor == "Google Ads":
            m = re.search(r"/(?:conversion|viewthroughconversion)/(\d+)", url)
            if m:
                q = dict(parse_qsl(urlparse(url).query))
                ads_hits[f"AW-{m.group(1)}"][phase][q.get("label") or q.get("en") or "remarketing"] += 1

        if vendor is None:
            if not is_first and not host.endswith(sig.NOISE_HOSTS) and not host.startswith("www.google."):
                unknown[host] += 1
            # First-party GTM loaders / sGTM paths (custom loader, Stape, etc.)
            if is_first and re.search(r"[?&]id=(GTM|G)-", url):
                sgtm_endpoints.add(f"{host}{urlparse(url).path}")
            continue

        v = vendors.setdefault(vendor, {"category": cat, "requests": 0, "phases": Counter(), "ids": set(),
                                        "hosts": set(), "failures": 0, "first_party": False})
        v["requests"] += 1
        v["phases"][phase] += 1
        v["hosts"].add(host)
        v["first_party"] |= is_first
        for pv, _kind, rx in sig.ID_PATTERNS:
            if pv == vendor or (pv in TID_VENDORS and vendor in TID_VENDORS | {"Google Analytics 4"}):
                for m in rx.findall(hay):
                    v["ids"].add(f"AW-{m}" if vendor == "Google Ads" and m.isdigit() else m)

        status = r.get("status")
        fail = r.get("failure")
        if (fail and not any(x in str(fail) for x in IGNORED_FAILURES)) or (status and status >= 400):
            v["failures"] += 1
            env = bool(fail) and not status and any(x in str(fail) for x in ENV_FAILURES)
            failures.append({"vendor": vendor, "url": url[:200], "status": status, "failure": fail, "phase": phase,
                             "environment": env})

    # Consent
    snaps = capture.get("snapshots") or {}
    cmp = sorted({k for k, v in vendors.items() if v["category"] == "consent"})
    ba = capture.get("consent") or {}
    if ba.get("method") in ("selector", "button_text", "banner_scan") and ba.get("accepted"):
        sel = str(ba.get("detail") or "")
        label = next((name for hint, name in BANNER_CMPS if hint in sel), None)
        if label or not cmp:
            cmp = sorted(set(cmp) | {label or "Consent banner (CMP not identified)"})
    # Where each container ran: page vs Shopify Customer Events sandbox (custom pixel).
    deployments = {}
    for r in requests:
        m = re.search(r"(?:gtm\.js|gtag/js)\?id=((?:GTM|G|AW|GT|DC)-[A-Za-z0-9_-]+)", r["url"])
        if m:
            where = "Shopify custom pixel (sandbox)" if SANDBOX_RX.search(r.get("frame") or "") else "page"
            deployments.setdefault(m.group(1), set()).add(where)
    shop_snap = next((s.get("shopify") for s in snaps.values() if isinstance(s, dict) and s.get("shopify")), None)
    pre_consent = sorted(k for k, v in vendors.items()
                         if v["category"] in sig.TRACKING_CATEGORIES and v["phases"].get("initial"))
    consent_state = next((s.get("consent_state") for k in ("reload", "initial") if (s := snaps.get(k)) and s.get("consent_state")), None)

    # Containers / tag IDs visible in the page runtime
    gtm_keys = sorted({k for s in snaps.values() if isinstance(s, dict) for k in s.get("google_tag_manager_keys") or []})
    html_ids = {k: sorted(set(rx.findall(html))) for k, rx in sig.GOOGLE_ID_RE.items()} if html else {}
    code_ids = {}
    for vendor_name, rx in sig.CODE_ID_PATTERNS:
        found = sorted(set(rx.findall(html or "")))
        if found and vendor_name != "Microsoft Ads (UET)":
            code_ids[vendor_name] = found[:10]

    # Data layer pushes observed
    dl_events = {}
    for phase, s in snaps.items():
        if not isinstance(s, dict) or not s.get("data_layer"):
            continue
        evs = []
        for e in s["data_layer"]:
            if isinstance(e, dict) and e.get("event"):
                evs.append(str(e["event"]))
            elif isinstance(e, list) and e and isinstance(e[0], str):
                evs.append(f"gtag:{e[0]}" + (f":{e[1]}" if len(e) > 1 and isinstance(e[1], str) else ""))
        dl_events[phase] = evs

    def _fmt_counter_tree(tree):
        return {k: {ph: dict(c) for ph, c in phases.items()} for k, phases in tree.items()}

    platform = "Shopify" if shop_snap or any(v in vendors for v in ("Shopify CDN", "Shopify Web Pixels Manager")) else None
    if not platform and html:
        if "wp-content" in html:
            platform = "WordPress / WooCommerce" if "woocommerce" in html.lower() else "WordPress"
        elif "static.bigcommerce" in html or "bigcommerce" in html.lower():
            platform = "BigCommerce"
        elif "demandware" in html or "/on/demandware.static" in html:
            platform = "Salesforce Commerce Cloud"
        elif "Magento" in html or "mage/" in html:
            platform = "Magento / Adobe Commerce"

    return {
        "site_host": site_host,
        "platform": platform,
        "shopify": shop_snap,
        "web_pixels": parse_web_pixels(html or ""),
        "totals": {"requests": len(requests), "first_party": first_party, "third_party": third_party,
                   "vendors": len(vendors), "failed": len(failures)},
        "vendors": {k: {**v, "phases": dict(v["phases"]), "ids": sorted(v["ids"]), "hosts": sorted(v["hosts"])}
                    for k, v in sorted(vendors.items(), key=lambda kv: (kv[1]["category"], kv[0]))},
        "unknown_hosts": unknown.most_common(40),
        "ga4": {tid: {"hits": g["hits"], "endpoints": sorted(g["endpoints"]),
                      "events": {ph: dict(c) for ph, c in g["events"].items()},
                      "gcs": {ph: sorted(s) for ph, s in g["gcs"].items()},
                      "gcd": sorted(g["gcd"])[:5],
                      "page_views": dict(g["page_views"]), "sources": dict(g["sources"]),
                      "sandbox_page_location": g["sandbox_page_location"]} for tid, g in ga4.items()},
        "meta_pixel": _fmt_counter_tree(meta_events),
        "tiktok": _fmt_counter_tree(tiktok_events),
        "google_ads": _fmt_counter_tree(ads_hits),
        "sgtm_endpoints": sorted(sgtm_endpoints),
        "atc_cart_add_status": [r.get("status") for r in requests if r.get("phase") == "atc" and "/cart/add" in r["url"]],
        "deployments": {k: sorted(v) for k, v in deployments.items()},
        "failures": failures[:60],
        "consent": {
            "cmp_detected": cmp,
            "banner_action": capture.get("consent"),
            "shopify_customer_privacy": bool(shop_snap and shop_snap.get("customer_privacy_api")),
            "shopify_visitor_consent": shop_snap.get("visitor_consent") if shop_snap else None,
            "google_consent_state": consent_state,
            "tracking_vendors_before_consent": pre_consent,
            "gated_scripts": gated_scripts(html or ""),
            "us_opt_out_link": bool(OPT_OUT_RX.search(html or "")),
            "geo_targeted_cmp": sorted({name for marker, name in HTML_CMPS if marker in (html or "")} - set(cmp)),
        },
        "runtime_tag_ids": gtm_keys,
        "html_ids": html_ids,
        "html_code_ids": code_ids,
        "data_layer_events": dl_events,
    }
