"""Deployment-source attribution: which integration actually sent each tracking hit.

On Shopify the same platform can be fed by several routes — a native app integration (Google & YouTube,
Facebook & Instagram, TikTok, Pinterest, Microsoft…), a custom pixel, GTM (itself loaded by the theme or an
app embed), an app embed / app proxy, or code hard-coded in the theme. What to check (and what to
recommend) depends on the route, so every hit is attributed by, in order:

1. Platform markers inside the hit (Meta `a=shopify_web_pixel`, TikTok `"partner":"Shopify"`, Pinterest
   `np=shopify-web-pixel`) — applied in platforms.py.
2. The requesting frame: Shopify custom-pixel sandboxes are `/web-pixels@…/custom/web-pixel-<id>@…`.
3. The Chrome initiator chain captured via CDP (`raw/initiators.json`): the call stack is scanned for the
   managing source (GTM container, Shopify Web Pixels Manager, app embed / proxy, theme asset), skipping
   wrapper scripts that patch fetch/sendBeacon, then walked up to whoever loaded that script.
4. No initiator record on a Shopify page = request from a sandboxed web worker = native app pixel.
"""

import re
from urllib.parse import parse_qs, urlparse

from .network import base_domain

APP_FOR_PLATFORM = {"GA4": "Google & YouTube", "Google Ads": "Google & YouTube", "Meta": "Meta (Facebook & Instagram)",
                    "TikTok": "TikTok", "Pinterest": "Pinterest", "Microsoft Ads": "Microsoft Ads", "Klaviyo": "Klaviyo"}
# Where each platform's library is loaded from (the "inheritance" root for its hits).
LIBRARIES = {
    "GA4": lambda pid: [f"gtag/js?id={pid}", f"gtag/destination?id={pid}"],
    "Google Ads": lambda pid: [f"gtag/js?id={pid}", f"destination?id={pid}"],
    "Meta": lambda pid: [f"signals/config/{pid}", "fbevents.js"],
    "TikTok": lambda pid: [f"sdkid={pid}", "analytics.tiktok.com/i18n/pixel/events.js"],
    "Pinterest": lambda pid: ["s.pinimg.com/ct/core.js"],
    "Microsoft Ads": lambda pid: ["bat.bing.com/bat.js"],
    "Klaviyo": lambda pid: ["static.klaviyo.com/onsite/js/"],
}
WEAK = ("Theme HTML", "Site script", "Script:", "Unattributed", "Shopify app embed")
# Libraries that load/flush pixels themselves — never the "source", keep walking.
PASS_THROUGH = re.compile(r"googletagmanager\.com/gtag/|connect\.facebook\.net|analytics\.tiktok\.com|s\.pinimg\.com|"
                          r"bat\.bing\.com/bat\.js|static\.klaviyo\.com|googleadservices|doubleclick\.net", re.I)


def category(label: str) -> str:
    """Coarse bucket used to detect multi-source deployments."""
    if label.startswith(("Shopify app embed", "Shopify app proxy")):
        return label.split(":")[0]
    for key in ("GTM", "Shopify app", "Shopify native app pixel", "Shopify custom pixel", "Theme", "Site script"):
        if label.startswith(key):
            return {"Shopify native app pixel": "Shopify app", "Site script": "Theme"}.get(key, key)
    return "Other"


class SourceResolver:
    def __init__(self, initiators: list[dict], web_pixels: list[dict], site_host: str, shopify: bool, html: str = ""):
        # Shopify app embeds render inside <!-- BEGIN app block: shopify://apps/<app>/blocks/... --> comments; script
        # tags they inject look like hard-coded theme HTML to the initiator chain, so map them back to the app.
        self.app_blocks = [(m.group(1), m.group(2)) for m in re.finditer(
            r"<!-- BEGIN app block: shopify://apps/([^/]+)/blocks/[^>]*?-->(.*?)<!-- END app block -->", html or "", re.S)]
        self.by_url: dict[str, dict] = {}
        for rec in initiators or []:
            self.by_url.setdefault(rec["url"], rec)
        self.custom_ids = {str(p["id"]) for p in web_pixels if p.get("type") == "CUSTOM"}
        self.apps = {p.get("app") for p in web_pixels if p.get("type") == "APP" and p.get("app")}
        self.site_host = site_host or ""
        self.shopify = shopify
        self._cache: dict[str, str] = {}

    def app_block_for(self, needle: str | None) -> str | None:
        if not needle or len(needle) < 6:
            return None
        for app, text in self.app_blocks:
            if needle in text:
                return f"Shopify app embed: {app}"
        return None

    def _block_for_url(self, url: str) -> str | None:
        p = urlparse(url)
        return self.app_block_for((p.hostname or "") + p.path) or (self.app_block_for(p.path) if len(p.path) > 12 else None)

    def has_initiators(self) -> bool:
        return bool(self.by_url)

    def label(self, u: str) -> str | None:
        if not u:
            return None
        p = urlparse(u)
        host, path = (p.hostname or "").lower(), p.path
        if "googletagmanager.com" in host and path.endswith("/gtm.js"):
            cid = parse_qs(p.query).get("id", ["?"])[0]
            return f"GTM {cid}"
        if re.search(r"/wpm/|web-pixels-manager|/wpm@", u):
            return "Shopify native app pixel (Web Pixels Manager)"
        m = re.search(r"cdn\.shopify\.com/extensions/[0-9a-f-]+/([a-z0-9-]+?)(?:-\d+(?:\.\d+)*)?/", u)
        if m:
            return f"Shopify app embed: {m.group(1)}"
        m = re.match(r"/a/([a-z0-9_-]+)/", path)
        if m and base_domain(host) == base_domain(self.site_host):
            return f"Shopify app proxy: {m.group(1)}"
        if re.search(r"/cdn/shop/t/\d+/|/s/files/.+/t/\d+/assets/", u):
            return "Theme script"
        return None

    RANK = {"GTM": 0, "Shopify native app pixel": 1, "Shopify app proxy": 2, "Shopify app embed": 3, "Theme script": 4}

    def _rank(self, label: str) -> int:
        return next((v for k, v in self.RANK.items() if label.startswith(k)), 9)

    def _resolve(self, rec: dict, depth: int) -> str:
        urls = [rec.get("by") or ""] + list(rec.get("stack") or [])
        labelled = [(u, self.label(u)) for u in urls]
        labelled = [(u, lab) for u, lab in labelled if lab]
        if labelled:
            # Strongest source wins: wrapper app embeds that patch fetch/sendBeacon sit on top of the stack.
            u, lab = min(labelled, key=lambda x: self._rank(x[1]))
            if lab.startswith("GTM ") and depth < 6:  # note who loaded the container
                loader = self._loader_of(u, depth + 1)
                if loader and not loader.startswith(("Theme HTML", "Theme inline", "Unattributed", "Script:")):
                    lab += f" (loaded by {loader})"
            return lab
        if rec.get("type") == "parser":
            doc = rec.get("doc") or rec.get("by") or ""
            if not doc or base_domain(urlparse(doc).hostname or "") == base_domain(self.site_host):
                return self._block_for_url(rec.get("url") or "") or "Theme HTML (hard-coded)"
            # Created by a third-party iframe (e.g. Google Ads remarketing frame): attribute to whoever made it.
            if doc in self.by_url and depth < 6:
                return self._resolve(self.by_url[doc], depth + 1)
            return f"Script: {urlparse(doc).hostname}"
        # Walk up: who loaded the script at the top of the stack (skipping pass-through libraries / wrappers)
        for u in urls:
            if u and u != rec.get("url") and u in self.by_url and depth < 6:
                parent = self._resolve(self.by_url[u], depth + 1)
                if parent and not parent.startswith("Unattributed"):
                    return parent
        top = next((u for u in urls if u and not PASS_THROUGH.search(u)), urls[0] if urls else "")
        if top and base_domain(urlparse(top).hostname or "") == base_domain(self.site_host):
            path = urlparse(top).path
            if "/cdn/shop" in top:
                return "Theme script"
            return "Theme inline script" if not path.endswith(".js") else f"Site script: {path[:40]}"
        return f"Script: {urlparse(top).hostname}" if top else "Unattributed"

    def _loader_of(self, url: str, depth: int) -> str | None:
        rec = self.by_url.get(url)
        return self._resolve(rec, depth) if rec else None

    def library_source(self, platform: str | None, pid: str | None) -> str | None:
        """Source of the request that loaded this platform's library (for this ID when the URL carries it)."""
        if platform not in LIBRARIES:
            return None
        key = ("lib", platform, pid)
        if key in self._cache:
            return self._cache[key]
        found = []
        for pat in LIBRARIES[platform](pid or "") if pid else LIBRARIES[platform](""):
            if not pat or pat.endswith("="):
                continue
            recs = [rec for url, rec in self.by_url.items() if pat in url]
            if recs:
                found = recs
                break
        labels = [self._resolve(rec, 0) for rec in found[:5]]
        labels = [lab for lab in labels if lab]
        res = min(labels, key=self._rank) if labels else None
        if res and res.startswith("Shopify native app pixel"):
            app = APP_FOR_PLATFORM.get(platform)
            res = f"Shopify app: {app}" if app in self.apps else res
        self._cache[key] = res
        return res

    def for_request(self, r: dict, platform: str | None = None, pid: str | None = None) -> str:
        frame = r.get("frame") or ""
        m = re.search(r"/(custom|app)/web-pixel-([\w-]+)@", frame)
        if m:
            kind, fid = m.groups()
            if kind == "custom":
                return "Shopify custom pixel" + ("" if fid == "shopify-custom-pixel" else f" #{fid}")
            return f"Shopify app: {APP_FOR_PLATFORM.get(platform, 'app pixel')}"
        key = (r["url"], platform, pid)
        if key in self._cache:
            return self._cache[key]
        rec = self.by_url.get(r["url"])
        app = APP_FOR_PLATFORM.get(platform)
        if rec is None:
            if self.shopify and self.has_initiators():
                res = f"Shopify app: {app}" if app in self.apps else "Shopify native app pixel (sandboxed)"
            else:
                res = self.library_source(platform, pid) or "Unattributed"
        else:
            res = self._resolve(rec, 0)
            if res.startswith(WEAK):  # hit's own stack is inconclusive -> inherit from the library loader
                lib = self.library_source(platform, pid)
                if lib:
                    res = lib
            if res.startswith("Shopify native app pixel") and app in self.apps:
                res = f"Shopify app: {app}"
            if res.startswith(("Theme HTML", "Theme inline")):  # inline code inside an app block = that app
                res = self.app_block_for(pid) or res
        self._cache[key] = res
        return res


def significant_routes(counter) -> set:
    """Route categories that carry a meaningful share of a platform's hits (ignores stray 1-2 hit noise)."""
    total = sum(counter.values()) or 1
    loaders = {m.group(1) for label in counter for m in [re.search(r"\(loaded by (.+)\)$", label)] if m}
    cats = {}
    for label, n in counter.items():
        c = "GTM" if label in loaders else category(label)  # "Elevar proxy" that loads GTM = the GTM route
        cats[c] = cats.get(c, 0) + n
    return {c for c, n in cats.items() if c != "Other" and n >= 4 and n / total >= 0.15}
