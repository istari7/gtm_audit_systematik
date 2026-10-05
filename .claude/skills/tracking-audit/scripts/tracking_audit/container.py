"""Decode a compiled GTM / gtag container.

gtm.js embeds its whole configuration as a JSON literal:

    var data = {"resource": {"version", "macros", "tags", "predicates", "rules"},
                "runtime": [...], "permissions": {...}, "blob": {"1": version, "10": id, ...}, ...}

Rather than regex-scraping the minified script, we JSON-decode that literal and
rebuild tags, variables (macros), triggers (rules + predicates), custom
templates and hard-coded IDs from it.
"""

import json
import re
from urllib.parse import parse_qs, urlparse

from . import signatures as sig

_DATA_RE = re.compile(r"var data\s*=\s*")


def extract_data(js_text: str) -> dict | None:
    for m in _DATA_RE.finditer(js_text):
        try:
            data, _ = json.JSONDecoder().raw_decode(js_text, m.end())
        except ValueError:
            continue
        if isinstance(data, dict) and isinstance(data.get("resource"), dict):
            return data
    return None


def container_id_from(data: dict, url: str = "") -> str:
    blob = data.get("blob") or {}
    cid = blob.get("10")
    if isinstance(cid, str) and re.match(r"^(GTM|G|AW|DC|GT)-", cid):
        return cid.split("|")[0]  # gtag containers list aliases: "G-XXXX|GT-YYYY"
    q = parse_qs(urlparse(url).query)
    if q.get("id"):
        return q["id"][0]
    ids = sig.GOOGLE_ID_RE["gtm"].findall(json.dumps(blob))
    return ids[0] if ids else "UNKNOWN"


class Decoder:
    def __init__(self, data: dict):
        self.data = data
        r = data["resource"]
        self.macros = r.get("macros", [])
        self.tags = r.get("tags", [])
        self.predicates = r.get("predicates", [])
        self.rules = r.get("rules", [])
        self.macro_labels = [self._macro_label(i, m) for i, m in enumerate(self.macros)]

    # ── values ────────────────────────────────────────────────────────────────
    def _macro_label(self, i: int, m: dict) -> str:
        fn = m.get("function", "?")
        name = _meta_name(m)
        if name:
            return name
        if fn == "__v":
            return f"DLV - {m.get('vtp_name')}"
        if fn == "__e":
            return "Event"
        if fn == "__u":
            return f"URL - {(m.get('vtp_component') or 'URL').title()}"
        if fn == "__k":
            return f"Cookie - {m.get('vtp_name')}"
        if fn == "__j":
            return f"JS - {m.get('vtp_name')}"
        if fn == "__aev":
            return f"Auto-Event - {m.get('vtp_varType')}"
        if fn == "__d":
            return f"DOM - {m.get('vtp_elementSelector') or m.get('vtp_elementId')}"
        if fn == "__c":
            return f"Constant - {str(m.get('vtp_value'))[:60]}"
        return f"{sig.MACRO_TYPES.get(fn, fn)} #{i}"

    def value(self, v, as_label=True):
        """Resolve GTM value encoding to a readable string / structure."""
        if not isinstance(v, list) or not v:
            return v
        op = v[0]
        if op == "macro" and len(v) > 1 and isinstance(v[1], int):
            m = self.macros[v[1]] if v[1] < len(self.macros) else {}
            if m.get("function") == "__c" and not isinstance(m.get("vtp_value"), list):
                return m.get("vtp_value")
            return "{{" + self.macro_labels[v[1]] + "}}" if v[1] < len(self.macro_labels) else "{{?}}"
        if op == "escape":
            return self.value(v[1])
        if op == "template":
            return "".join(str(self.value(x)) for x in v[1:])
        if op == "list":
            return [self.value(x) for x in v[1:]]
        if op == "map":
            items = v[1:]
            return {str(self.value(items[i])): self.value(items[i + 1]) for i in range(0, len(items) - 1, 2)}
        if op == "tag" and len(v) > 1:
            return f"<tag {v[1]}>"
        if isinstance(op, str):
            return [op] + [self.value(x) for x in v[1:]]
        return [self.value(x) for x in v]

    def params(self, obj: dict) -> dict:
        return {k[4:]: self.value(val) for k, val in obj.items() if k.startswith("vtp_")}

    # ── triggers ──────────────────────────────────────────────────────────────
    def predicate_text(self, i: int) -> str:
        p = self.predicates[i]
        lhs = self.value(p.get("arg0"))
        op = sig.PREDICATE_OPS.get(p.get("function"), p.get("function"))
        neg = "NOT " if p.get("negate") else ""
        return f"{lhs} {neg}{op} {json.dumps(self.value(p.get('arg1')))}"

    def event_of_predicate(self, i: int) -> str | None:
        p = self.predicates[i]
        a0 = p.get("arg0")
        if p.get("function") == "_eq" and isinstance(a0, list) and a0[:1] == ["macro"]:
            idx = a0[1]
            if idx < len(self.macros) and self.macros[idx].get("function") == "__e":
                return p.get("arg1") if isinstance(p.get("arg1"), str) else None
        return None

    def firing_map(self):
        """tag index -> {'fire': [condition strings], 'block': [...], 'events': set()}"""
        out = {i: {"fire": [], "block": [], "events": set()} for i in range(len(self.tags))}
        for rule in self.rules:
            ifs, unless, add, block = [], [], [], []
            for part in rule:
                kind, idxs = part[0], part[1:]
                {"if": ifs, "unless": unless, "add": add, "block": block}.get(kind, []).extend(idxs)
            conds = list(dict.fromkeys([self.predicate_text(i) for i in ifs]
                                       + [f"NOT({self.predicate_text(i)})" for i in unless]))
            text = " AND ".join(conds) or "(always)"
            events = {e for e in (self.event_of_predicate(i) for i in ifs) if e}
            for t in add:
                if t in out:
                    out[t]["fire"].append(text)
                    out[t]["events"] |= events
            for t in block:
                if t in out:
                    out[t]["block"].append(text)
        return out

    def all_events(self) -> list[str]:
        evs = {e for i in range(len(self.predicates)) if (e := self.event_of_predicate(i))}
        return sorted(evs)


def _meta_name(obj: dict) -> str | None:
    md = obj.get("metadata")
    if isinstance(md, list) and md[:1] == ["map"]:
        for i in range(1, len(md) - 1, 2):
            if md[i] == "name" and isinstance(md[i + 1], str):
                return md[i + 1]
    return None


def _template_vendor(perm: dict) -> tuple[str | None, list[str]]:
    urls = (perm.get("inject_script") or {}).get("urls", []) + (perm.get("send_pixel") or {}).get("urls", [])
    keys = [k.get("key", "") for k in (perm.get("access_globals") or {}).get("keys", [])]
    keys += (perm.get("get_cookies") or {}).get("cookieNames", [])
    consent_writes = [c for c in (perm.get("access_consent") or {}).get("consentTypes", []) if c.get("write")]
    if consent_writes:
        return "Consent Mode (CMP integration)", urls
    joined = " ".join(urls).lower()
    for hint, vendor in sig.TEMPLATE_HINTS:
        if "." in hint and hint.lower() in joined:
            return vendor, urls
    for k in keys:  # first global the template touches is the most telling
        kl = k.lower()
        for hint, vendor in sig.TEMPLATE_HINTS:
            h = hint.lower()
            if kl == h or kl.startswith(h + ".") or kl.startswith(h + "_") or (len(h) > 4 and h in kl):
                return vendor, urls
    return None, urls


def _ids_in_text(text: str) -> dict[str, list[str]]:
    found: dict[str, set] = {}
    for vendor, rx in sig.CODE_ID_PATTERNS:
        for m in rx.findall(text):
            found.setdefault(vendor, set()).add(m)
    return {k: sorted(v) for k, v in found.items()}


def _vendors_in_text(text: str) -> list[str]:
    low = text.lower()
    hits = set()
    for pattern, vendor, _cat in sig.VENDORS:
        if pattern.lower() in low:
            hits.add(vendor)
    return sorted(hits)


ID_PARAM_KEYS = {
    "tagId", "measurementId", "measurementIdOverride", "trackingId", "conversionId", "conversionLabel",
    "advertiserId", "groupTag", "activityTag", "pixelId", "pixel_id", "pixelID", "id", "partnerId",
    "hotjar_site_id", "uetqTagId", "accountId", "companyId", "company_id", "siteId", "projectId",
}


def analyze(data: dict, cid: str, meta: dict | None = None) -> dict:
    d = Decoder(data)
    fmap = d.firing_map()
    perms = data.get("permissions") or {}
    raw = json.dumps(data["resource"])

    tags, listeners, html_tags, templates_used = [], [], [], {}
    for i, t in enumerate(d.tags):
        fn = t.get("function", "?")
        p = d.params(t)
        f = fmap[i]
        if fn in sig.LISTENER_FUNCTIONS:
            listeners.append({"type": sig.LISTENER_FUNCTIONS[fn], "function": fn,
                              "conditions": f["fire"][:3], "params": _short(p)})
            continue
        paused = fn == "__paused"
        orig = f"__{p.get('originalTagType')}" if paused else fn
        rec = {
            "index": i,
            "tag_id": t.get("tag_id"),
            "name": _meta_name(t),
            "function": orig,
            "type": sig.TAG_TYPES.get(orig, "Custom Template" if orig.startswith("__cvt_") else orig),
            "paused": paused,
            "consent_required": d.value(t.get("consent")) or [],
            "fires_on": f["fire"],
            "blocked_by": f["block"],
            "events": sorted(f["events"]),
            "orphan": not paused and not f["fire"] and not t.get("setup_tags") and t.get("tag_id") is not None,
            "ids": {k: v for k, v in p.items() if k in ID_PARAM_KEYS and isinstance(v, (str, int)) and v != ""},
        }
        if orig == "__gaawe":
            rec["ga4_event"] = p.get("eventName")
        if orig == "__html":
            html = str(p.get("html") or "")
            rec["html_size"] = len(html)
            rec["vendors"] = _vendors_in_text(html)
            rec["html_ids"] = _ids_in_text(html)
            rec["html_preview"] = re.sub(r"\s+", " ", html)[:240]
            rec["risk"] = [w for w in ("document.write", "eval(", "innerHTML", "localStorage", "XMLHttpRequest", "fetch(")
                           if w in html]
            html_tags.append(rec)
        if orig.startswith("__cvt_"):
            templates_used.setdefault(orig, 0)
            templates_used[orig] += 1
        tags.append(rec)

    templates = []
    for name, perm in perms.items():
        if not name.startswith("__cvt_"):
            continue
        vendor, urls = _template_vendor(perm)
        templates.append({"id": name, "vendor": vendor, "instances": templates_used.get(name, 0),
                          "injects": urls, "permissions": sorted(perm.keys())})

    # Variables
    variables = []
    for i, m in enumerate(d.macros):
        fn = m.get("function", "?")
        v = {"index": i, "label": d.macro_labels[i], "type": sig.MACRO_TYPES.get(fn, fn)}
        if fn == "__jsm":
            js = str(d.value(m.get("vtp_javascript")) or "")
            v["code_preview"] = re.sub(r"\s+", " ", js)[:200]
        if fn == "__c":
            v["value"] = d.value(m.get("vtp_value"))
        variables.append(v)

    # Hard-coded IDs anywhere in the container resource
    google_ids = {k: sorted(set(rx.findall(raw))) for k, rx in sig.GOOGLE_ID_RE.items()}
    google_ids["gtm"] = [x for x in google_ids["gtm"] if x != cid]
    measurement = _measurement_ids(tags, d)

    # Consent configuration
    consent_templates = [t for t in templates if "access_consent" in t["permissions"]]
    active = [t for t in tags if not t["paused"]]
    with_consent = [t for t in active if t["consent_required"]]
    consent = {
        "consent_types_referenced": [c for c in sig.CONSENT_TYPES if c in raw],
        "consent_templates": [t["id"] for t in consent_templates],
        "tags_with_additional_consent": len(with_consent),
        "active_tags": len(active),
        "cmp_hints": sorted({t["vendor"] for t in templates if t["vendor"] in
                             ("OneTrust", "Cookiebot", "Shopify Customer Privacy", "Consent Mode (CMP integration)")}),
    }

    type_counts: dict[str, dict] = {}
    for t in tags:
        c = type_counts.setdefault(t["type"], {"active": 0, "paused": 0})
        c["paused" if t["paused"] else "active"] += 1

    events = d.all_events()
    blob = data.get("blob") or {}
    features = []
    if not cid.startswith("GTM-"):
        for t in tags:
            fn = t["function"]
            if fn.endswith(("_first", "_last")) or not (fn in sig.GTAG_FEATURES or fn.startswith(("__ccd_", "__ogt_", "__dest_"))):
                continue
            settings = {k: v for k, v in d.params(d.tags[t["index"]]).items() if v not in ("", None, [], {})}
            features.append({"function": fn, "label": sig.GTAG_FEATURES.get(fn, fn), "settings": _short(settings)})
    return {
        "id": cid,
        "kind": "gtm" if cid.startswith("GTM-") else "gtag",
        "version": data["resource"].get("version") or blob.get("1"),
        **(meta or {}),
        "counts": {
            "tags": len(tags),
            "active_tags": len(active),
            "paused_tags": sum(t["paused"] for t in tags),
            "custom_html": sum(t["function"] == "__html" and not t["paused"] for t in tags),
            "custom_templates": len(templates),
            "orphan_tags": sum(t["orphan"] for t in tags),
            "listeners": len(listeners),
            "variables": len(d.macros),
            "custom_js_variables": sum(1 for m in d.macros if m.get("function") == "__jsm"),
            "triggers": len(d.rules),
            "predicates": len(d.predicates),
        },
        "tag_types": dict(sorted(type_counts.items(), key=lambda kv: -sum(kv[1].values()))),
        "tags": tags,
        "gtag_features": features,
        "custom_html": html_tags,
        "templates": templates,
        "listeners": listeners,
        "variables": variables,
        "events": {
            "all": events,
            "custom": [e for e in events if not e.startswith("gtm.")],
            "ecommerce": [e for e in sig.ECOM_EVENTS if e in events or f'"{e}"' in raw],
        },
        "ga4_events": sorted({t["ga4_event"] for t in tags if t.get("ga4_event") and not t["paused"]
                              and isinstance(t["ga4_event"], str)}),
        "google_ids": google_ids,
        "measurement": measurement,
        "consent": consent,
        "vendors": sorted({v for t in html_tags if not t["paused"] for v in t["vendors"]}
                          | {t["vendor"] for t in templates if t["vendor"] and t["instances"]}),
    }


def _measurement_ids(tags: list[dict], d: Decoder) -> dict:
    """Destination IDs configured by tags (resolved through constant variables)."""
    out: dict[str, set] = {"ga4": set(), "google_ads": set(), "floodlight": set(), "ua": set(), "other": set()}
    for t in tags:
        if t["paused"]:
            continue
        ids = t["ids"]
        fn = t["function"]
        tid = ids.get("tagId") or ids.get("measurementId") or ids.get("measurementIdOverride")
        if isinstance(tid, str):
            for part in (x.strip() for x in tid.split(",")):
                if "{{" in part:
                    if fn != "__gaawe":
                        out["other"].add(f"{t['type']}: dynamic {part}")
                elif part.startswith("G-"):
                    out["ga4"].add(part)
                elif part.startswith("AW-"):
                    out["google_ads"].add(part)
                elif part.startswith("DC-"):
                    out["floodlight"].add(part)
                elif part:
                    out["other"].add(f"{t['type']}: {part}")
        if fn in ("__awct", "__sp") and ids.get("conversionId"):
            label = ids.get("conversionLabel")
            out["google_ads"].add(f"AW-{ids['conversionId']}" + (f"/{label}" if fn == "__awct" and label else ""))
        if fn in ("__flc", "__fls") and ids.get("advertiserId"):
            out["floodlight"].add(f"DC-{ids['advertiserId']}")
        if fn == "__ua" and ids.get("trackingId"):
            out["ua"].add(str(ids["trackingId"]))
        if fn.startswith("__cvt_") or fn in ("__baut", "__pntr", "__bzi", "__hjtc"):
            for k, v in ids.items():
                if k not in ("tagId",) or fn in ("__baut", "__pntr", "__bzi", "__hjtc"):
                    out["other"].add(f"{t['type']}: {k}={v}")
        for vendor, vals in (t.get("html_ids") or {}).items():
            for v in vals:
                if vendor == "Google tag":
                    (out["ga4"] if v.startswith("G-") else out["google_ads"] if v.startswith("AW-") else out["other"]).add(v)
                else:
                    out["other"].add(f"{vendor}: {v}")
    # UA via GA Settings variables
    for m in d.macros:
        if m.get("function") == "__gas" and isinstance(d.value(m.get("vtp_trackingId")), str):
            out["ua"].add(d.value(m.get("vtp_trackingId")))
    return {k: sorted(v) for k, v in out.items()}


def _short(p: dict) -> dict:
    return {k: (v if not isinstance(v, str) else v[:120]) for k, v in list(p.items())[:8]}
