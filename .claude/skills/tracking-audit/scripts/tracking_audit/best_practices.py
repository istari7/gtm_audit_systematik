"""GTM container configuration vs best practice.

Each check returns:
  area, check, status (pass | warn | fail | info | n/a), impact (High | Medium | Low),
  evidence (from the container JSON), recommendation, why (business reason)

Checks are judged with business context: an ecommerce brand is held to ecommerce measurement
standards, Shopify brands are expected to track checkout/purchase through Shopify Customer Events
(GTM does not run on Shopify checkout), and nice-to-haves (sGTM, dynamic remarketing) are
recommendations, not failures, unless spend signals justify them.
"""

import json
import re

from . import signatures as sig
from .container import Decoder

PAGE_EVENTS = {"gtm.js", "gtm.dom", "gtm.load", "gtm.init", "gtm.init_consent"}
ADS_FUNCS = {"__awct", "__sp", "__flc", "__fls", "__awcc"}
REQUIRED_ECOM = ["view_item", "add_to_cart", "begin_checkout", "purchase"]
RECOMMENDED_ECOM = ["view_item_list", "select_item", "view_cart", "remove_from_cart", "add_shipping_info",
                    "add_payment_info"]
WEIGHT = {"High": 3, "Medium": 2, "Low": 1}


def _macro_refs(obj, out: set):
    if isinstance(obj, list):
        if len(obj) == 2 and obj[0] == "macro" and isinstance(obj[1], int):
            out.add(obj[1])
        for x in obj:
            _macro_refs(x, out)
    elif isinstance(obj, dict):
        for v in obj.values():
            _macro_refs(v, out)


class ContainerChecks:
    def __init__(self, data: dict, analysis: dict, audit: dict):
        self.d = Decoder(data)
        self.data, self.c, self.audit = data, analysis, audit
        self.net = audit["network"]
        self.platform = audit["brand"].get("platform") or ""
        self.shopify = self.platform == "Shopify"
        self.ecommerce = self.shopify or bool(audit["capture"].get("pdp_url")) or bool(analysis["events"]["ecommerce"])
        self.active = [(i, t) for i, t in enumerate(self.d.tags)
                       if t.get("function") not in sig.LISTENER_FUNCTIONS and t.get("function") != "__paused"]
        self.fmap = self.d.firing_map()
        self.checks: list[dict] = []

    def add(self, area, check, status, impact, evidence, rec="", why=""):
        self.checks.append({"area": area, "check": check, "status": status, "impact": impact,
                            "evidence": evidence, "recommendation": rec, "why": why})

    def p(self, t: dict) -> dict:
        return self.d.params(t)

    def by_fn(self, *fns):
        return [(i, t) for i, t in self.active if t.get("function") in fns]

    # ── Measurement foundation ───────────────────────────────────────────────
    def foundation(self):
        gt = self.by_fn("__googtag")
        ga4_tags = [(i, t) for i, t in gt if str(self.p(t).get("tagId", "")).startswith(("G-", "{{"))]
        ga4_events = self.by_fn("__gaawe")
        net_ga4 = set(self.net["ga4"])
        if not ga4_tags and not ga4_events:
            outside = sorted(net_ga4)
            self.add("Measurement", "GA4 managed in GTM", "info" if outside else "fail", "High",
                     f"No GA4 Google tag or GA4 event tags in the container. GA4 hits observed: {', '.join(outside) or 'none'}.",
                     "Keep one owner for GA4. If GA4 comes from the Shopify Google & YouTube app, leave GTM out of GA4 "
                     "to avoid double counting; otherwise implement GA4 in GTM." if outside else "Implement GA4.",
                     "GA4 is the system of record for traffic and revenue reporting.")
            return
        ids = sorted({str(self.p(t).get("tagId")) for _, t in ga4_tags})
        self.add("Measurement", "Single GA4 Google tag", "pass" if len(ids) <= 1 else "warn", "Medium",
                 f"GA4 Google tag IDs: {', '.join(ids) or 'none (events only)'}.",
                 "" if len(ids) <= 1 else "Confirm every GA4 property is intentional (roll-up / agency); remove leftovers.",
                 "Multiple properties split reporting and inflate collection costs.")
        app_ids = {i for p in self.net["web_pixels"] if p.get("app") == "Google & YouTube" for i in p["google_ids"]}
        gtm_ids = set(ids) | {str(self.p(t).get("measurementIdOverride")) for _, t in ga4_events}
        both = sorted(app_ids & gtm_ids)
        pv = {tid: g["page_views"].get("reload", 0) for tid, g in self.net["ga4"].items()}
        self.add("Measurement", "GA4 sent from one source only", "fail" if both else "pass", "High",
                 f"{', '.join(both)} is configured in GTM and in the Shopify Google & YouTube app"
                 + (f"; page_view hits per page load: {', '.join(f'{k}×{v}' for k, v in pv.items() if k in both)}." if both else ".")
                 if both else "No GA4 property is shared between GTM and a Shopify app.",
                 "Pick one owner: disable GA4 in the Shopify app (keep Ads/Merchant Center there) or remove the GTM GA4 tags."
                 if both else "", "Double tagging inflates sessions, page views and revenue, and breaks conversion rates.")
        early = {"gtm.init", "gtm.init_consent", "gtm.js"}
        late = [f"#{t.get('tag_id')}" for i, t in ga4_tags if not (self.fmap[i]["events"] & early)]
        if ga4_tags:
            self.add("Measurement", "Google tag fires on Initialization / All Pages", "warn" if late else "pass", "Medium",
                     "Late-firing Google tag(s): " + ", ".join(late) if late else "Google tag fires on Initialization or Page View.",
                     "Fire the Google tag on the Initialization – All Pages trigger so config/consent are set before events."
                     if late else "", "Late configuration drops early events and session attribution.")
        hard = [f"#{t.get('tag_id')}" for _, t in ga4_events
                if re.fullmatch(r"G-[A-Z0-9]+", str(self.p(t).get("measurementIdOverride", "")))]
        if ga4_events:
            self.add("Measurement", "Measurement ID in a variable, not hard-coded", "warn" if len(hard) > 3 else "pass", "Low",
                     f"{len(hard)} of {len(ga4_events)} GA4 event tags hard-code the measurement ID.",
                     "Reference a Constant / Lookup Table variable so the ID changes in one place." if len(hard) > 3 else "",
                     "Hard-coded IDs make property migrations and staging setups error-prone.")

    # ── Ecommerce data quality ───────────────────────────────────────────────
    def ecommerce_checks(self):
        if not self.ecommerce:
            self.add("Ecommerce", "Ecommerce tracking", "n/a", "Low", "Not an ecommerce site.")
            return
        ga4_events = self.by_fn("__gaawe")
        configured = {}
        for i, t in ga4_events:
            name = self.p(t).get("eventName")
            names = {name} if isinstance(name, str) and "{{" not in name else self.fmap[i]["events"]
            for n in names:
                configured.setdefault(n, []).append((i, t))
        app_google = any(p.get("app") == "Google & YouTube" for p in self.net["web_pixels"])
        net_events = {e for g in self.net["ga4"].values() for ph in g["events"].values() for e in ph}
        missing_req = [e for e in REQUIRED_ECOM if e not in configured]
        missing_rec = [e for e in RECOMMENDED_ECOM if e not in configured]
        if not ga4_events:
            self.add("Ecommerce", "GA4 ecommerce events in GTM", "info" if app_google else "fail", "High",
                     "No GA4 event tags in GTM." + (" GA4 ecommerce is sent by the Shopify Google & YouTube app."
                                                     if app_google else ""),
                     "" if app_google else "Implement the GA4 ecommerce funnel (view_item → purchase) from the dataLayer.",
                     "Funnel and revenue reporting, audience building and ROAS all depend on these events.")
        else:
            purchase_note = ""
            if "purchase" in missing_req and self.shopify:
                missing_req.remove("purchase")
                purchase_note = (" `purchase` is not in GTM — expected on Shopify (checkout runs outside GTM); "
                                 "confirm a Customer Events pixel or app sends it.")
            observed = sorted(e for e in net_events if e in REQUIRED_ECOM + RECOMMENDED_ECOM)
            gtm_core = [e for e in REQUIRED_ECOM if e in configured]
            source = "Shopify Google & YouTube app" if app_google else "a non-GTM source"
            configured_txt = ", ".join(sorted(e for e in configured if e in REQUIRED_ECOM + RECOMMENDED_ECOM)) or "none"
            if len(gtm_core) < 2 and (app_google or observed):
                # GTM is not the ecommerce owner; the app is. That's a valid setup.
                self.add("Ecommerce", "GA4 ecommerce funnel coverage", "info", "High",
                         f"Configured in GTM: {configured_txt}. GA4 ecommerce is owned by {source} "
                         f"(observed: {', '.join(observed) or 'none during the visit'}).{purchase_note}",
                         "Keep one owner for GA4 ecommerce; don't build a parallel GTM implementation unless replacing the app.",
                         "Two owners double-count revenue and events.")
            else:
                unseen = [e for e in missing_req if e not in net_events]
                split = [e for e in missing_req if e in net_events]
                status = ("fail" if len(unseen) >= 2 else
                          "warn" if unseen or split or len(missing_rec) > 3 else "pass")
                self.add("Ecommerce", "GA4 ecommerce funnel coverage", status, "High",
                         f"Configured in GTM: {configured_txt}. Missing core: {', '.join(missing_req) or 'none'}; "
                         f"missing recommended: {', '.join(missing_rec) or 'none'}."
                         + (f" Split ownership: {', '.join(split)} is sent by {source}, not GTM." if split else "")
                         + purchase_note,
                         ("Move the whole funnel to one owner (GTM or the app) and remove the other's GA4 events."
                          if split else "Add the missing funnel events with items[] from the dataLayer." if status != "pass" else ""),
                         "Gaps or split ownership break funnel reports and double-count shared events.")
            lookalikes = sorted(n for n in configured if isinstance(n, str) and n not in REQUIRED_ECOM + RECOMMENDED_ECOM
                                and any(e in n for e in REQUIRED_ECOM + RECOMMENDED_ECOM))
            if lookalikes:
                self.add("Ecommerce", "Custom event names don't shadow GA4 standard events", "warn", "Medium",
                         f"Custom GA4 events named like standard ecommerce events: {', '.join(lookalikes[:8])}.",
                         "Use the standard event name with a parameter (e.g. add_to_cart + placement=lp001) so it lands "
                         "in GA4 ecommerce reports and Ads key events.",
                         "Non-standard names fragment reporting and aren't used by GA4 ecommerce or Ads bidding.")
            ecom_tags = [(i, t) for e, lst in configured.items() if e in REQUIRED_ECOM + RECOMMENDED_ECOM for i, t in lst]
            no_items = []
            for i, t in ecom_tags:
                p = self.p(t)
                blob = json.dumps(p)
                if not (p.get("sendEcommerceData") or "items" in blob):
                    no_items.append(f"{p.get('eventName')} #{t.get('tag_id')}")
            if ecom_tags:
                self.add("Ecommerce", "Ecommerce events carry items[]", "fail" if no_items else "pass", "High",
                         "Without items: " + ", ".join(sorted(set(no_items))) if no_items else
                         "All ecommerce event tags send items (dataLayer ecommerce object or items parameter).",
                         "Enable 'Send Ecommerce data' (dataLayer) or map the items parameter on every ecommerce tag."
                         if no_items else "", "No items = no product / category revenue reporting in GA4.")
            for i, t in configured.get("purchase", []):
                blob = json.dumps(self.p(t))
                miss = [k for k in ("transaction_id", "value", "currency")
                        if k not in blob and not self.p(t).get("sendEcommerceData")]
                self.add("Ecommerce", "Purchase has transaction_id, value, currency", "fail" if miss else "pass", "High",
                         f"purchase tag #{t.get('tag_id')} missing: {', '.join(miss)}" if miss else
                         f"purchase tag #{t.get('tag_id')} sends transaction_id / value / currency.",
                         "Pass transaction_id (dedupe), value and currency on purchase." if miss else "",
                         "Revenue accuracy and duplicate-order protection.")
                break
        if self.audit["capture"].get("pdp_url") and "view_item" not in net_events and self.net["ga4"]:
            self.add("Ecommerce", "view_item observed on a product page", "fail", "High",
                     f"No GA4 view_item hit on {self.audit['capture']['pdp_url']}.",
                     "Verify the view_item trigger / dataLayer push on product templates.",
                     "Product-level reporting and remarketing audiences rely on view_item.")
        dom = [v for v in self.c["variables"] if v["type"] in ("DOM Element", "Custom JavaScript")
               and re.search(r"querySelector|innerText|textContent|getElementsBy|\$\(", v.get("code_preview", "") + v["label"])]
        if dom:
            self.add("Ecommerce", "Data sourced from the dataLayer, not page scraping", "warn", "Medium",
                     f"{len(dom)} variable(s) scrape the DOM: " + ", ".join(v["label"] for v in dom[:6]),
                     "Move these values into dataLayer pushes from the theme / app.",
                     "DOM scraping breaks silently on theme changes, corrupting revenue and product data.")

    # ── Google Ads ───────────────────────────────────────────────────────────
    def google_ads(self):
        ads = self.by_fn(*ADS_FUNCS)
        if not ads:
            return
        linker = self.by_fn("__gclidw")
        self.add("Google Ads", "Conversion Linker present", "pass" if linker else "fail", "High",
                 f"{len(ads)} Ads/Floodlight tag(s); conversion linker tags: {len(linker)}.",
                 "" if linker else "Add a Conversion Linker tag on All Pages.",
                 "Without it, ad clicks aren't stored first-party and conversions go unattributed (esp. Safari/iOS).")
        conv = self.by_fn("__awct")
        for i, t in conv:
            p = self.p(t)
            ev = self.fmap[i]["events"]
            if not ({"purchase", "checkout_completed"} & ev or "purchase" in str(p.get("conversionLabel", "")).lower()
                    or p.get("conversionValue") or p.get("orderId")):
                continue
            miss = [k for k, label in (("conversionValue", "value"), ("currencyCode", "currency"), ("orderId", "transaction ID"))
                    if not p.get(k)]
            self.add("Google Ads", "Purchase conversion passes value, currency, order ID", "warn" if miss else "pass", "High",
                     f"Ads conversion #{t.get('tag_id')} ({p.get('conversionId')}) missing: {', '.join(miss)}" if miss else
                     f"Ads conversion #{t.get('tag_id')} passes value, currency and order ID.",
                     "Map value/currency/transaction_id from the dataLayer." if miss else "",
                     "Value-based bidding (tROAS) needs revenue; order ID prevents duplicate conversions.")
            break
        ec = bool(self.by_fn("__awec", "__awud")) or any(
            self.p(t).get("enableEnhancedConversion") or self.p(t).get("enableNewCustomerReporting") or
            "user_data" in json.dumps(self.p(t)) for _, t in conv)
        if conv:
            self.add("Google Ads", "Enhanced conversions configured", "pass" if ec else "warn", "Medium",
                     "User-provided data configured on Ads conversions." if ec else
                     "No user-provided data (enhanced conversions) on Ads conversion tags.",
                     "" if ec else "Enable enhanced conversions (hashed email/phone from the dataLayer) on purchase.",
                     "Typically recovers a meaningful share of conversions lost to cookie restrictions.")
        ids = sorted({str(self.p(t).get("conversionId")) for _, t in ads if self.p(t).get("conversionId")})
        if len(ids) > 1:
            self.add("Google Ads", "Single Google Ads account", "warn", "Medium",
                     f"Conversion IDs: {', '.join(ids)}.",
                     "Confirm each account is live and owned; remove agency / legacy accounts.",
                     "Stale accounts leak conversion data to third parties and confuse attribution.")
        rmkt = self.by_fn("__sp")
        if self.ecommerce:
            dyn = any("items" in json.dumps(self.p(t)) or self.p(t).get("customParamsFormat") == "DATALAYER" or
                      self.p(t).get("enableDynamicRemarketing") for _, t in rmkt)
            self.add("Google Ads", "Dynamic remarketing (product feed)", "pass" if dyn else "info", "Low",
                     "Remarketing passes product data." if dyn else
                     f"{len(rmkt)} remarketing tag(s), no product-level parameters detected.",
                     "" if dyn else "If running Shopping / PMax, send items with ecommerce events for dynamic remarketing.",
                     "Product-level audiences lift Shopping / PMax performance.")

    # ── Paid social & other pixels ───────────────────────────────────────────
    def paid_social(self):
        html = [t for t in self.c["custom_html"] if not t["paused"]]
        for vendor in ("Meta Pixel", "TikTok Pixel", "Pinterest Tag", "Snapchat Pixel", "Reddit Pixel", "Microsoft Ads (UET)"):
            in_html = [t for t in html if vendor in t["vendors"] or vendor in t["html_ids"]]
            in_tpl = [t for t in self.c["templates"] if t["vendor"] == vendor and t["instances"]]
            if not in_html and not in_tpl:
                continue
            self.add("Paid social & pixels", f"{vendor}: implemented via template", "warn" if in_html else "pass",
                     "Low", f"{len(in_html)} Custom HTML tag(s), {sum(t['instances'] for t in in_tpl)} template tag(s).",
                     "Move to the vendor's Community Template (permissions-scoped, consent-aware)." if in_html else "",
                     "Templates are safer, auditable and respect consent settings.")
            if vendor == "Meta Pixel":
                blob = " ".join(t["html_preview"] for t in in_html) + json.dumps([self.p(self.d.tags[t["index"]])
                                                                                for t in self.c["tags"] if t["function"] in
                                                                                {x["id"] for x in in_tpl}])
                full_html = " ".join(str(self.p(self.d.tags[t["index"]]).get("html", "")) for t in in_html)
                has_eid = bool(re.search(r"eventID|event_id|eventId", blob + full_html))
                self.add("Paid social & pixels", "Meta events carry event_id (CAPI dedupe)",
                         "pass" if has_eid else "warn", "Medium",
                         "event_id found on Meta events." if has_eid else "No event_id on Meta browser events.",
                         "" if has_eid else "Pass a shared event_id from the dataLayer so browser + Conversions API events dedupe.",
                         "Without dedupe, CAPI + pixel double-count purchases and distort Meta optimisation.")
                app_meta = any(p.get("app") == "Meta (Facebook & Instagram)" for p in self.net["web_pixels"])
                if app_meta:
                    self.add("Paid social & pixels", "Meta pixel has a single source", "fail", "High",
                             "Meta pixel fires from GTM and the Shopify Facebook & Instagram app.",
                             "Keep the Shopify app (it includes CAPI) and remove the GTM Meta tags, or vice versa.",
                             "Duplicate pixels double-count events and inflate reported ROAS.")

    # ── Consent ──────────────────────────────────────────────────────────────
    def consent(self):
        cc = self.c["consent"]
        cmp = self.net["consent"]["cmp_detected"]
        writes = bool(cc["consent_templates"])
        init_consent = any("gtm.init_consent" in self.fmap[i]["events"] for i, _ in self.active)
        dl = [e for evs in self.net.get("data_layer_events", {}).values() for e in evs]
        outside = "gtag:consent:default" in dl
        if not (writes or init_consent) and outside:
            self.add("Consent", "Consent Mode defaults set before tags fire", "pass", "High",
                     "Consent Mode default" + (" + update" if "gtag:consent:update" in dl else "")
                     + " is set via gtag outside GTM (theme / CMP / Shopify app) before the container loads.",
                     "", "Required for EU/UK traffic; keeps Google modelling conversions for users who decline.")
            return self._consent_tag_checks(cc, cmp)
        self.add("Consent", "Consent Mode defaults set in GTM",
                 "pass" if writes or init_consent else ("warn" if cmp else "info"), "High" if cmp else "Medium",
                 ("Consent template(s): " + ", ".join(cc["consent_templates"]) if writes else
                  "Consent Initialization trigger used." if init_consent else
                  "No consent template or Consent Initialization trigger in the container, and no gtag consent "
                  "default seen in the dataLayer."),
                 "" if writes or init_consent else
                 "Set Consent Mode v2 defaults on Consent Initialization (CMP template) and update on choice.",
                 "Required for EU/UK traffic; keeps Google modelling conversions for users who decline.")
        self._consent_tag_checks(cc, cmp)

    def _consent_tag_checks(self, cc, cmp):
        marketing = [t for t in self.c["tags"] if not t["paused"] and (
            t["function"] in ADS_FUNCS or t["function"] == "__html" and any(
                v in t.get("vendors", []) for v in ("Meta Pixel", "TikTok Pixel", "Pinterest Tag", "Snapchat Pixel")))]
        gated = [t for t in marketing if t["consent_required"]]
        if marketing and cmp:
            share = len(gated) / len(marketing)
            self.add("Consent", "Marketing tags require ad_storage consent",
                     "pass" if share > 0.8 else "warn", "Medium",
                     f"{len(gated)} of {len(marketing)} marketing tags have additional consent checks.",
                     "Add 'Require additional consent: ad_storage' to non-Google marketing tags." if share <= 0.8 else "",
                     "Non-Google tags don't read Consent Mode; without checks they fire regardless of the user's choice.")

    # ── Hygiene, governance, performance ─────────────────────────────────────
    def hygiene(self):
        n = self.c["counts"]
        self.add("Governance", "Paused tags cleaned up", "pass" if n["paused_tags"] <= 5 else "warn", "Low",
                 f"{n['paused_tags']} paused tag(s).", "Delete paused tags no longer needed." if n["paused_tags"] > 5 else "",
                 "Dead tags slow audits and risk being re-enabled by mistake.")
        self.add("Governance", "No orphan tags", "pass" if not n["orphan_tags"] else "warn", "Low",
                 f"{n['orphan_tags']} active tag(s) without a firing trigger.",
                 "Delete or attach a trigger." if n["orphan_tags"] else "", "Orphans are config debt.")
        share = n["custom_html"] / n["active_tags"] if n["active_tags"] else 0
        self.add("Governance", "Limited Custom HTML", "pass" if n["custom_html"] <= 5 and share <= 0.3 else "warn",
                 "Medium", f"{n['custom_html']} active Custom HTML tag(s) ({share:.0%} of active tags).",
                 "Replace with templates where one exists." if n["custom_html"] > 5 or share > 0.3 else "",
                 "Custom HTML runs unrestricted JS: security, performance and consent risk.")
        risky = [t for t in self.c["custom_html"] if not t["paused"] and
                 (set(t["risk"]) & {"document.write", "eval("} or re.search(r"src=\\?[\"']http://", t["html_preview"]))]
        if risky:
            self.add("Governance", "Custom HTML free of unsafe patterns", "warn", "Medium",
                     f"{len(risky)} tag(s) use document.write / eval / http:// scripts: "
                     + ", ".join(f"#{t['tag_id']}" for t in risky[:8]),
                     "Rewrite without document.write/eval; load scripts over HTTPS.",
                     "These patterns block rendering and widen the XSS surface.")
        refs: set = set()
        _macro_refs(self.data["resource"].get("tags", []), refs)
        _macro_refs(self.data["resource"].get("predicates", []), refs)
        for _ in range(3):
            before = len(refs)
            for idx in list(refs):
                if idx < len(self.d.macros):
                    _macro_refs(self.d.macros[idx], refs)
            if len(refs) == before:
                break
        unused = [self.d.macro_labels[i] for i, m in enumerate(self.d.macros)
                  if i not in refs and m.get("function") not in ("__e", "__cid", "__ctv", "__dbg", "__u", "__r", "__f")]
        self.add("Governance", "No unused variables", "pass" if len(unused) <= 5 else "warn", "Low",
                 f"{len(unused)} variable(s) not referenced by any tag, trigger or variable"
                 + (": " + ", ".join(unused[:8]) if unused else "."),
                 "Remove unused variables." if len(unused) > 5 else "", "Clutter hides what actually drives data.")
        self.add("Governance", "Custom JavaScript variables kept lean",
                 "pass" if n["custom_js_variables"] <= 20 else "warn", "Low",
                 f"{n['custom_js_variables']} Custom JavaScript variable(s).",
                 "Push values into the dataLayer instead of computing them in GTM." if n["custom_js_variables"] > 20 else "",
                 "Each runs on every evaluation; heavy use slows the page and is brittle.")
        sig_of = {}
        for i, t in self.active:
            key = json.dumps({k: v for k, v in t.items() if k not in ("tag_id", "priority", "metadata")}, sort_keys=True)
            key += json.dumps(sorted(self.fmap[i]["fire"]))
            sig_of.setdefault(key, []).append(t.get("tag_id"))
        dups = [ids for ids in sig_of.values() if len(ids) > 1]
        self.add("Governance", "No duplicate tags", "fail" if dups else "pass", "High" if dups else "Low",
                 "Identical tags (same config + triggers): " + "; ".join(", ".join(f"#{x}" for x in d) for d in dups[:5])
                 if dups else "No identical tags.", "Delete the duplicates." if dups else "",
                 "Duplicate tags double-send events and conversions.")
        ua = [t for t in self.c["tags"] if t["function"] == "__ua"]
        if ua or self.c["measurement"]["ua"]:
            self.add("Governance", "Universal Analytics removed", "warn", "Low",
                     f"{len(ua)} UA tag(s) ({sum(not t['paused'] for t in ua)} active); UA IDs {', '.join(self.c['measurement']['ua'])}.",
                     "Delete UA tags, GA Settings variables and UA triggers.", "UA stopped processing in July 2024.")
        page = [t for i, t in self.active if self.fmap[i]["events"] & PAGE_EVENTS and
                all(len(f.split(" AND ")) == 1 for f in self.fmap[i]["fire"])]
        self.add("Performance", "Tags firing on every page kept small", "pass" if len(page) <= 20 else "warn", "Medium",
                 f"{len(page)} tag(s) fire on every page load without filters; container {self.c.get('size_kb', '?')} KB.",
                 "Scope non-essential tags to the pages that need them." if len(page) > 20 else "",
                 "Every always-on tag adds main-thread work, hurting Core Web Vitals and conversion rate.")
        names = sum(1 for t in self.c["tags"] if t["name"])
        self.add("Governance", "Tag names published (naming convention auditable)", "info", "Low",
                 f"{names} of {len(self.c['tags'])} tags publish their names." if names else
                 "Tag names are not published in the container (normal); naming convention can't be audited from outside.")

    def shopify_checkout(self):
        """Shopify Checkout Extensibility: storefront GTM does not load on checkout / thank-you pages."""
        if not self.shopify:
            return
        where = self.net.get("deployments", {}).get(self.c["id"], ["page"])
        if "Shopify custom pixel (sandbox)" in where:
            return
        rx = re.compile(r"thank[_-]?you|/checkouts?/|/orders/|order[_-]?status|Thank You Page", re.I)
        legacy = [t for t in self.c["tags"] if not t["paused"] and any(rx.search(f) for f in t["fires_on"])]
        if not legacy:
            return
        conv = [t for t in legacy if t["function"] in ADS_FUNCS or t["function"] in ("__html", "__gaawe")
                or t["function"].startswith("__cvt_")]
        self.add("Ecommerce", "No purchase tags tied to Shopify thank-you / checkout URLs", "fail" if conv else "warn",
                 "High",
                 f"{len(legacy)} active tag(s) fire on checkout / thank-you URLs or events: "
                 + "; ".join(f"{t['type']} #{t['tag_id']}" + (f" ({t['ids'].get('conversionId')})" if t['ids'].get('conversionId') else "")
                             for t in legacy[:6])
                 + ". This container loads on the storefront, and with Checkout Extensibility it no longer runs on checkout "
                 "or thank-you pages, so these tags most likely never fire.",
                 "Move purchase conversions to Shopify Customer Events (app pixel or a custom pixel subscribing to "
                 "checkout_completed), then confirm Google Ads / Meta purchase conversions are recording.",
                 "Missing purchase conversions starve bidding algorithms and understate ROAS.")

    def deployment(self):
        where = self.net.get("deployments", {}).get(self.c["id"], [])
        if "Shopify custom pixel (sandbox)" not in where:
            return
        listeners = self.c["counts"]["listeners"]
        self.add("Deployment", "GTM in Shopify custom pixel: DOM-based triggers avoided",
                 "warn" if listeners else "pass", "Medium",
                 f"Container runs inside the Shopify Customer Events sandbox; {listeners} click/scroll/visibility/form "
                 "listener(s) configured" + (" — these cannot see the storefront DOM and never fire." if listeners else "."),
                 "Drive events from Shopify standard events (analytics.subscribe) pushed to the dataLayer, not DOM listeners."
                 if listeners else "", "Sandboxed GTM has no access to the page; DOM triggers silently do nothing.")
        loc = any(g.get("sandbox_page_location") for g in self.net["ga4"].values())
        self.add("Deployment", "Custom pixel overrides page_location", "fail" if loc else "pass", "High",
                 "GA4 hits from the sandbox report the web-pixels sandbox URL as page_location." if loc else
                 "No sandbox URLs observed in page_location.",
                 "Set page_location/page_title/page_referrer from event.context.document in the pixel." if loc else "",
                 "Wrong page_location breaks every page, landing-page and attribution report.")

    def server_side(self):
        if not self.net["sgtm_endpoints"]:
            return
        has_url = any("server_container_url" in json.dumps(self.p(t)) or "transport_url" in json.dumps(self.p(t))
                      for _, t in self.by_fn("__googtag"))
        self.add("Infrastructure", "Server-side tagging wired in the Google tag", "pass" if has_url else "info", "Low",
                 f"First-party endpoints: {', '.join(self.net['sgtm_endpoints'][:3])}; server_container_url in Google tag: "
                 f"{'yes' if has_url else 'not found (may be set in a loader / Stape)'}.", "",
                 "First-party collection extends cookie life and resists ad blockers.")

    def run(self) -> list[dict]:
        if not self.c["counts"]["tags"]:
            where = ", ".join(self.net.get("deployments", {}).get(self.c["id"], [])) or "page"
            self.add("Governance", "Container has tags", "fail", "Medium",
                     f"{self.c['id']} v{self.c.get('version')} is published with 0 tags, 0 triggers and 0 variables, "
                     f"and still loads on every page ({where}).",
                     "Remove the container snippet / custom pixel, or finish the implementation it was created for.",
                     "An empty container is an abandoned setup: page weight with no data, and confusion about who owns tracking.")
            return self.checks
        for step in (self.foundation, self.ecommerce_checks, self.google_ads, self.paid_social, self.consent,
                     self.hygiene, self.shopify_checkout, self.deployment, self.server_side):
            try:
                step()
            except Exception as e:  # one bad check must not sink the audit
                self.add("Internal", step.__name__, "info", "Low", f"check error: {e}")
        return self.checks


def evaluate_gtag_only(audit: dict) -> list[dict]:
    """Brands with no GTM container: judge the Google-tag / Shopify-app setup instead."""
    out = []
    net = audit["network"]
    gtags = [c for c in audit["containers"] if c["kind"] == "gtag"]
    feats = {f["function"]: f for c in gtags for f in c.get("gtag_features", [])}

    def add(area, check, status, impact, evidence, rec="", why=""):
        out.append({"area": area, "check": check, "status": status, "impact": impact, "evidence": evidence,
                    "recommendation": rec, "why": why})

    apps = sorted({p["app"] for p in net["web_pixels"] if p.get("app")})
    add("Measurement", "Tag management approach", "info", "Medium",
        "No GTM container. Tags are deployed via " + (f"Shopify app pixels ({', '.join(apps)})" if apps else
                                                      "hard-coded / app scripts") + ".",
        "Fine for a lean channel mix. Move to GTM (or a Shopify custom pixel + GTM) once the brand needs custom "
        "events, more ad platforms or consent orchestration beyond the apps.",
        "A TMS lowers the cost of adding/changing tracking without theme deploys.")
    ga = next((c for c in gtags if c["id"].startswith("G-")), None)
    if ga:
        em = [f for k, f in feats.items() if k.startswith("__ccd_em_")]
        add("Measurement", "GA4 enhanced measurement", "pass" if em else "warn", "Low",
            f"{len(em)} enhanced-measurement feature(s) on {ga['id']}.")
        sigs = feats.get("__ogt_google_signals")
        add("Measurement", "Google Signals", "pass" if sigs and "ENABLED" in json.dumps(sigs["settings"]) else "info",
            "Low", "Enabled." if sigs else "Not enabled.", "", "Cross-device reporting and remarketing audiences.")
    if any(c["id"].startswith("AW-") for c in gtags):
        upd = "__ogt_1p_data_v2" in feats or "__ccd_add_1p_data" in feats
        add("Google Ads", "Enhanced conversions (user-provided data)", "pass" if upd else "warn", "Medium",
            "User-provided data collection is on." if upd else "User-provided data collection not enabled in the Google tag.",
            "" if upd else "Enable enhanced conversions in Google Ads / the Google & YouTube app.",
            "Recovers conversions lost to cookie restrictions.")
    return out


def score(checks: list[dict]) -> dict:
    scored = [c for c in checks if c["status"] in ("pass", "warn", "fail")]
    total = sum(WEIGHT[c["impact"]] for c in scored)
    got = sum(WEIGHT[c["impact"]] * (1 if c["status"] == "pass" else 0.5 if c["status"] == "warn" else 0) for c in scored)
    return {"score": round(100 * got / total) if total else None, "pass": sum(c["status"] == "pass" for c in checks),
            "warn": sum(c["status"] == "warn" for c in checks), "fail": sum(c["status"] == "fail" for c in checks)}


def evaluate(audit: dict, container_data: dict[str, dict]) -> dict:
    result = {}
    for c in audit["containers"]:
        if c["kind"] != "gtm" or c["id"] not in container_data:
            continue
        checks = ContainerChecks(container_data[c["id"]], c, audit).run()
        result[c["id"]] = {"checks": checks, **score(checks)}
        if not c["counts"]["tags"]:
            result[c["id"]]["score"] = None  # empty container: nothing to score
    if not result:
        checks = evaluate_gtag_only(audit)
        result["(no GTM)"] = {"checks": checks, **score(checks), "score": None}  # nothing to score
    return result
