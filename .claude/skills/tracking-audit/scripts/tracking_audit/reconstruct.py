"""Rebuild a GTM workspace export (exportFormatVersion 2) from a compiled gtm.js container.

The published container keeps tags, variables (macros), conditions (predicates) and firing rules,
but drops names (unless "include tag name" is on), folders, notes and custom-template source. This
reconstructs:

  tag[]             type, parameters, paused, priority, firing option, consent settings,
                    firingTriggerId / blockingTriggerId, setup/teardown sequencing
  trigger[]         one per distinct compiled rule: type from its event condition
                    (Page View, Click, Custom Event…) + remaining conditions as filters
  variable[]        user-defined variables with their parameters
  builtInVariable[] built-ins referenced ({{Event}}, {{Page Path}}, {{Click Classes}}…)

Listener plumbing (__cl, __lcl, __hl, __sdl, __evl, __tl…) is folded into trigger types. Custom
templates are referenced by type only — their source isn't in the published container, so tags
using them won't import until the template is added. Everything else is importable in principle;
treat the result as an analysis aid, not a backup.
"""

import json
from datetime import datetime, timezone

from . import signatures as sig
from .container import _meta_name

BUILTIN_MACROS = {  # function -> (builtInVariable type, display name)
    "__e": ("EVENT", "Event"),
    "__ctv": ("CONTAINER_VERSION", "Container Version"),
    "__cid": ("CONTAINER_ID", "Container ID"),
    "__dbg": ("DEBUG_MODE", "Debug Mode"),
    "__r": ("RANDOM_NUMBER", "Random Number"),
    "__hid": ("HTML_ID", "HTML ID"),
}
URL_BUILTINS = {None: ("PAGE_URL", "Page URL"), "URL": ("PAGE_URL", "Page URL"),
                "PATH": ("PAGE_PATH", "Page Path"), "HOST": ("PAGE_HOSTNAME", "Page Hostname")}
AEV_BUILTINS = {"ELEMENT": ("CLICK_ELEMENT", "Click Element"), "CLASSES": ("CLICK_CLASSES", "Click Classes"),
                "ID": ("CLICK_ID", "Click ID"), "TARGET": ("CLICK_TARGET", "Click Target"),
                "URL": ("CLICK_URL", "Click URL"), "TEXT": ("CLICK_TEXT", "Click Text")}
EVENT_TRIGGER_TYPES = {
    "gtm.js": "PAGEVIEW", "gtm.dom": "DOM_READY", "gtm.load": "WINDOW_LOADED",
    "gtm.init": "INIT", "gtm.init_consent": "CONSENT_INIT",
    "gtm.click": "CLICK", "gtm.linkClick": "LINK_CLICK", "gtm.formSubmit": "FORM_SUBMISSION",
    "gtm.historyChange": "HISTORY_CHANGE", "gtm.historyChange-v2": "HISTORY_CHANGE",
    "gtm.timer": "TIMER", "gtm.scrollDepth": "SCROLL_DEPTH", "gtm.elementVisibility": "ELEMENT_VISIBILITY",
    "gtm.video": "YOUTUBE_VIDEO", "gtm.pageError": "JS_ERROR",
}
TRIGGER_LABELS = {"PAGEVIEW": "Page View", "DOM_READY": "DOM Ready", "WINDOW_LOADED": "Window Loaded",
                  "INIT": "Initialization", "CONSENT_INIT": "Consent Initialization", "CLICK": "All Elements Click",
                  "LINK_CLICK": "Link Click", "FORM_SUBMISSION": "Form Submission", "HISTORY_CHANGE": "History Change",
                  "TIMER": "Timer", "SCROLL_DEPTH": "Scroll Depth", "ELEMENT_VISIBILITY": "Element Visibility",
                  "YOUTUBE_VIDEO": "YouTube Video", "JS_ERROR": "JavaScript Error", "CUSTOM_EVENT": "Custom Event"}
COND_TYPES = {"_eq": "EQUALS", "_cn": "CONTAINS", "_re": "MATCH_REGEX", "_sw": "STARTS_WITH", "_ew": "ENDS_WITH",
              "_css": "CSS_SELECTOR", "_lt": "LESS", "_le": "LESS_OR_EQUALS", "_gt": "GREATER",
              "_ge": "GREATER_OR_EQUALS"}
SKIP_TAG_KEYS = {"function", "tag_id", "priority", "metadata", "once_per_event", "once_per_load", "consent",
                 "setup_tags", "teardown_tags", "paused", "vtp_originalTagType"}


class Reconstructor:
    def __init__(self, data: dict, public_id: str):
        self.data, self.public_id = data, public_id
        r = data["resource"]
        self.macros, self.tags = r.get("macros", []), r.get("tags", [])
        self.predicates, self.rules = r.get("predicates", []), r.get("rules", [])
        self.builtins: dict[str, str] = {}
        self.var_names = self._name_macros()

    # ── variables ────────────────────────────────────────────────────────────
    def _builtin_for(self, m: dict):
        fn = m.get("function")
        if fn in BUILTIN_MACROS:
            return BUILTIN_MACROS[fn]
        if fn == "__u" and not m.get("vtp_queryKey") and (m.get("vtp_component") in URL_BUILTINS):
            return URL_BUILTINS[m.get("vtp_component")]
        if fn == "__f" and not m.get("vtp_component"):
            return ("REFERRER", "Referrer")
        if fn == "__aev" and m.get("vtp_varType") in AEV_BUILTINS and not m.get("vtp_attribute"):
            return AEV_BUILTINS[m["vtp_varType"]]
        return None

    def _name_macros(self) -> list[str]:
        names, used = [], set()
        for i, m in enumerate(self.macros):
            b = self._builtin_for(m)
            if b:
                self.builtins[b[0]] = b[1]
                names.append(b[1])
                continue
            fn = m.get("function", "?")
            base = _meta_name(m) or {
                "__v": f"DLV - {m.get('vtp_name')}", "__k": f"Cookie - {m.get('vtp_name')}",
                "__j": f"JS - {m.get('vtp_name')}", "__c": f"Constant - {str(m.get('vtp_value'))[:40]}",
                "__u": f"URL - {m.get('vtp_component') or 'URL'}{' ' + str(m.get('vtp_queryKey')) if m.get('vtp_queryKey') else ''}",
                "__aev": f"Auto-Event - {m.get('vtp_varType')}{' ' + str(m.get('vtp_attribute')) if m.get('vtp_attribute') else ''}",
                "__d": f"DOM - {m.get('vtp_elementSelector') or m.get('vtp_elementId')}",
            }.get(fn) or f"{sig.MACRO_TYPES.get(fn, fn.strip('_'))} {i}"
            name, n = base, 2
            while name in used or name in self.builtins.values():
                name, n = f"{base} ({n})", n + 1
            used.add(name)
            names.append(name)
        return names

    # ── value encoding -> export parameters ──────────────────────────────────
    def text(self, v) -> str:
        """Resolve a compiled value to the template string GTM would show."""
        if isinstance(v, list) and v:
            op = v[0]
            if op == "macro":
                return "{{" + self.var_names[v[1]] + "}}"
            if op == "escape":
                return self.text(v[1])
            if op == "template":
                return "".join(self.text(x) for x in v[1:])
            if op == "tag":
                return self._tag_name(v[1])
            return json.dumps(v)
        if isinstance(v, bool):
            return "true" if v else "false"
        return "" if v is None else str(v)

    def param(self, key: str | None, v) -> dict:
        p: dict = {"key": key} if key is not None else {}
        if isinstance(v, list) and v and v[0] == "list":
            return {**p, "type": "LIST", "list": [self.param(None, x) for x in v[1:]]}
        if isinstance(v, list) and v and v[0] == "map":
            items = v[1:]
            return {**p, "type": "MAP", "map": [self.param(self.text(items[i]), items[i + 1])
                                                for i in range(0, len(items) - 1, 2)]}
        if isinstance(v, bool):
            return {**p, "type": "BOOLEAN", "value": "true" if v else "false"}
        if isinstance(v, int):
            return {**p, "type": "INTEGER", "value": str(v)}
        return {**p, "type": "TEMPLATE", "value": self.text(v)}

    def params(self, obj: dict, skip=()) -> list[dict]:
        return [self.param(k[4:], v) for k, v in obj.items() if k.startswith("vtp_") and k not in skip]

    # ── triggers ─────────────────────────────────────────────────────────────
    def _event_of(self, pi: int):
        p = self.predicates[pi]
        a0 = p.get("arg0")
        if isinstance(a0, list) and a0[:1] == ["macro"] and self.macros[a0[1]].get("function") == "__e":
            return p
        return None

    def _condition(self, pi: int, negate=False) -> dict:
        p = self.predicates[pi]
        cond = {"type": COND_TYPES.get(p.get("function"), p.get("function", "").upper()),
                "parameter": [self.param("arg0", p.get("arg0")), self.param("arg1", p.get("arg1"))]}
        if p.get("ignore_case"):
            cond["parameter"].append({"type": "BOOLEAN", "key": "ignore_case", "value": "true"})
        if negate or p.get("negate"):
            cond["parameter"].append({"type": "BOOLEAN", "key": "negate", "value": "true"})
        return cond

    def build_triggers(self):
        triggers, by_key, fire, block = [], {}, {}, {}
        for rule in self.rules:
            parts = {"if": [], "unless": [], "add": [], "block": []}
            for part in rule:
                parts.setdefault(part[0], []).extend(part[1:])
            key = (tuple(sorted(parts["if"])), tuple(sorted(parts["unless"])))
            if key not in by_key:
                tid = str(len(triggers) + 1)
                by_key[key] = tid
                event_preds = [pi for pi in parts["if"] if self._event_of(pi)]
                other = [pi for pi in parts["if"] if pi not in event_preds]
                ttype, custom, event_name = "CUSTOM_EVENT", [], None
                if event_preds:
                    ev = self.predicates[event_preds[0]]
                    event_name = ev.get("arg1")
                    if ev.get("function") == "_eq" and event_name in EVENT_TRIGGER_TYPES:
                        ttype = EVENT_TRIGGER_TYPES[event_name]
                    else:
                        custom = [self._condition(event_preds[0])]
                    other += event_preds[1:]
                trig = {"accountId": "0", "containerId": "0", "triggerId": tid,
                        "name": f"{TRIGGER_LABELS.get(ttype, ttype)}"
                                + (f" - {event_name}" if ttype == "CUSTOM_EVENT" and event_name else "")
                                + (" (filtered)" if other or parts["unless"] else "") + f" #{tid}",
                        "type": ttype}
                if custom:
                    trig["customEventFilter"] = custom
                filters = [self._condition(pi) for pi in other] + [self._condition(pi, True) for pi in parts["unless"]]
                if filters:
                    trig["filter"] = filters
                if not parts["if"] and not parts["unless"]:
                    trig["type"], trig["name"] = "ALWAYS", f"Always #{tid}"
                triggers.append(trig)
            tid = by_key[key]
            for t in parts["add"]:
                fire.setdefault(t, []).append(tid)
            for t in parts["block"]:
                block.setdefault(t, []).append(tid)
        return triggers, fire, block

    # ── tags ─────────────────────────────────────────────────────────────────
    def _tag_name(self, idx: int) -> str:
        t = self.tags[idx] if isinstance(idx, int) and idx < len(self.tags) else {}
        fn = t.get("function", "?")
        orig = f"__{t.get('vtp_originalTagType')}" if fn == "__paused" else fn
        label = sig.TAG_TYPES.get(orig, "Custom Template" if orig.startswith("__cvt_") else orig.strip("_"))
        if _meta_name(t):
            return _meta_name(t)
        hint = None
        for k in ("vtp_eventName", "vtp_tagId", "vtp_conversionLabel", "vtp_activityTag", "vtp_event_type",
                  "vtp_eventType", "vtp_event", "vtp_pixelId", "vtp_pixel_id"):
            v = t.get(k)
            if isinstance(v, (str, int)) and str(v):
                hint = str(v)[:40]
                break
        if not hint and orig == "__html":
            from .container import _vendors_in_text
            vendors = _vendors_in_text(str(t.get("vtp_html", "")))
            hint = vendors[0] if vendors else None
        return f"{label}{' - ' + hint if hint else ''} #{t.get('tag_id', idx)}"

    def _sequence(self, v):
        names = []
        if isinstance(v, list):
            for x in v[1:] if v[:1] == ["list"] else v:
                if isinstance(x, list) and x[:1] == ["tag"]:
                    names.append({"tagName": self._tag_name(x[1]),
                                  **({"stopOnSetupFailure": bool(x[2])} if len(x) > 2 else {})})
        return names

    def build(self) -> dict:
        triggers, fire, block = self.build_triggers()
        tags, templates = [], set()
        for i, t in enumerate(self.tags):
            fn = t.get("function", "?")
            if fn in sig.LISTENER_FUNCTIONS:
                continue
            paused = fn == "__paused"
            ttype = (t.get("vtp_originalTagType") if paused else fn.lstrip("_")) or "unknown"
            if ttype.startswith("cvt_"):
                templates.add(ttype)
            rec = {"accountId": "0", "containerId": "0", "tagId": str(t.get("tag_id", i)),
                   "name": self._tag_name(i), "type": ttype, "parameter": self.params(t, SKIP_TAG_KEYS),
                   "firingTriggerId": fire.get(i, []),
                   "tagFiringOption": "ONCE_PER_LOAD" if t.get("once_per_load") else
                                      "ONCE_PER_EVENT" if t.get("once_per_event") else "UNLIMITED"}
            if block.get(i):
                rec["blockingTriggerId"] = block[i]
            if paused:
                rec["paused"] = True
            if t.get("priority") is not None:
                rec["priority"] = {"type": "INTEGER", "value": str(t["priority"])}
            consent = t.get("consent")
            if isinstance(consent, list) and consent[:1] == ["list"] and len(consent) > 1:
                rec["consentSettings"] = {"consentStatus": "NEEDED", "consentType": {
                    "type": "LIST", "list": [{"type": "TEMPLATE", "value": self.text(c)} for c in consent[1:]]}}
            if t.get("setup_tags"):
                rec["setupTag"] = self._sequence(t["setup_tags"])
            if t.get("teardown_tags"):
                rec["teardownTag"] = self._sequence(t["teardown_tags"])
            if not rec["firingTriggerId"] and not paused:
                rec["notes"] = "No firing trigger in the published container (orphan or sequenced only)."
            tags.append(rec)

        variables = []
        for i, m in enumerate(self.macros):
            if self._builtin_for(m):
                continue
            variables.append({"accountId": "0", "containerId": "0", "variableId": str(i + 1),
                              "name": self.var_names[i], "type": m.get("function", "?").lstrip("_"),
                              "parameter": self.params(m)})

        version = self.data["resource"].get("version") or (self.data.get("blob") or {}).get("1") or "0"
        return {
            "exportFormatVersion": 2,
            "exportTime": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "containerVersion": {
                "path": f"accounts/0/containers/0/versions/{version}",
                "accountId": "0", "containerId": "0", "containerVersionId": str(version),
                "name": f"Reconstructed from published {self.public_id} v{version}",
                "description": "Reconstructed from the public gtm.js by the tracking-audit skill. Names, folders and "
                               "notes are not published and were generated; custom template source is not included.",
                "container": {"accountId": "0", "containerId": "0", "name": f"{self.public_id} (reconstructed)",
                              "publicId": self.public_id, "usageContext": ["WEB"]},
                "tag": tags,
                "trigger": triggers,
                "variable": variables,
                "builtInVariable": [{"accountId": "0", "containerId": "0", "type": k, "name": v}
                                    for k, v in sorted(self.builtins.items())],
            },
            "reconstruction": {
                "custom_templates_missing_source": sorted(templates),
                "listener_tags_folded": sum(1 for t in self.tags if t.get("function") in sig.LISTENER_FUNCTIONS),
                "counts": {"tags": len(tags), "triggers": len(triggers), "variables": len(variables),
                           "built_in_variables": len(self.builtins)},
            },
        }


def reconstruct(data: dict, public_id: str) -> dict:
    return Reconstructor(data, public_id).build()
