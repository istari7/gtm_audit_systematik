"""Render audit.json into a client-ready README.md, plus the root index."""

import json
import re
from pathlib import Path

from . import signatures as sig

NOTES_START = "<!-- ANALYST_NOTES_START -->"
NOTES_END = "<!-- ANALYST_NOTES_END -->"
CATEGORY_LABELS = {
    "tms": "Tag management", "analytics": "Analytics", "advertising": "Advertising",
    "affiliate": "Affiliate / influencer", "attribution": "Attribution", "session-replay": "Session replay / UX",
    "experimentation": "Personalisation / testing / search", "email-sms": "Email / SMS / CRM",
    "reviews-loyalty": "Reviews / UGC / loyalty", "support": "Support / chat", "consent": "Consent",
    "platform": "Commerce platform", "payments": "Payments / BNPL", "ecommerce-app": "Ecommerce apps",
    "media": "Media", "monitoring": "Monitoring",
}
PHASE_ORDER = ["initial", "consent", "reload", "pdp", "atc"]


def cell(v, limit=140) -> str:
    if v is None or v == "" or v == []:
        return "—"
    if isinstance(v, (list, tuple, set)):
        v = ", ".join(str(x) for x in v)
    elif isinstance(v, dict):
        v = json.dumps(v, ensure_ascii=False)
    s = re.sub(r"\s+", " ", str(v)).replace("|", "\\|")
    return s if len(s) <= limit else s[: limit - 1] + "…"


def code(v) -> str:
    return "—" if not v else ", ".join(f"`{x}`" for x in (v if isinstance(v, (list, set, tuple)) else [v]))


def table(headers: list[str], rows: list[list]) -> list[str]:
    if not rows:
        return ["_None detected._", ""]
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out + [""]


SECTION_ORDER = [
    "Executive Summary", "Analyst Notes", "Next Steps", "GTM Container Audit", "Tracking Platform Audit", "Container Deep Dive", "Google Tag Settings",
    "Measurement & Conversion IDs", "Ecommerce Tracking", "Consent & Privacy", "Event Flow by Visit Phase",
    "Shopify Customer Events", "Tag Management & Infrastructure", "Platform Inventory", "Findings & Recommendations",
    "Method & Files", "Appendix",
]


def _reorder(md: str) -> str:
    """Order sections GTM-container-first and renumber them."""
    parts = re.split(r"(?m)^(?=## )", md)
    head, sections = parts[0], parts[1:]

    def key(sec: str):
        title = re.sub(r"^## (?:[\d.]+\s+)?", "", sec.splitlines()[0])
        for i, name in enumerate(SECTION_ORDER):
            if title.startswith(name):
                return i, title
        return len(SECTION_ORDER), title

    sections.sort(key=lambda s: key(s)[0])  # stable: container sub-sections keep their order
    out, n, deep = [head], 0, 0
    for sec in sections:
        idx, title = key(sec)
        body = sec.split("\n", 1)[1] if "\n" in sec else ""
        name = SECTION_ORDER[idx] if idx < len(SECTION_ORDER) else ""
        if name in ("Container Deep Dive", "Google Tag Settings"):
            if deep == 0:
                n += 1
                out.append(f"## {n}. Container Inventory & Settings\n\n")
            deep += 1
            out.append(f"### {n}.{deep} {title}\n{body}")
        elif name == "Appendix":
            out.append(f"## {title}\n{body}")
        else:
            n += 1
            out.append(f"## {n}. {title}\n{body}")
    return "".join(out)


def capture_geo(audit: dict) -> str:
    """Hints about where the capture ran from (affects geo-targeted banners, markets and blocked vendors)."""
    hints = set()
    for c in audit["containers"]:
        for f in c.get("gtag_features", []):
            tld = (f.get("settings") or {}).get("foreignTldMacroResult")
            if tld:
                hints.add(f"Google served {tld}")
    final = audit["brand"].get("final_url") or ""
    m = re.search(r"/(en|fr|de|es)-([a-z]{2,3})(/|$)", final)
    if m:
        hints.add(f"store redirected to /{m.group(1)}-{m.group(2)} market")
    return "; ".join(sorted(hints))


def render(audit: dict, previous_readme: str | None = None) -> str:
    b, net, cap, containers, findings = audit["brand"], audit["network"], audit["capture"], audit["containers"], audit["findings"]
    gtm = [c for c in containers if c["kind"] == "gtm"]
    sev = {s: [f for f in findings if f["severity"] == s] for s in ("P1", "P2", "P3")}
    L: list[str] = []

    tms = []
    if gtm:
        tms.append("Google Tag Manager (" + ", ".join(c["id"] for c in gtm) + ")")
    for v in ("Tealium iQ", "Adobe Launch", "Ensighten"):
        if v in net["vendors"]:
            tms.append(v)
    if net["sgtm_endpoints"]:
        tms.append("server-side tagging")
    if not tms and net["web_pixels"]:
        tms.append("Shopify Customer Events (app pixels)")
    tms_text = " + ".join(tms) or "No tag manager detected"

    L += [
        f"# Tracking & Martech Audit — {b['name']}",
        "",
        f"**Site:** {b['url']}  ",
        f"**Audit date:** {b['audit_date']}  ",
        f"**Platform:** {b.get('platform') or 'Unknown'}  ",
        f"**Tag management:** {tms_text}  ",
        f"**Consent platform:** {', '.join(net['consent']['cmp_detected']) or 'None detected'}  ",
        "",
        "---",
        "",
        "## 1. Executive Summary",
        "",
    ]
    ga4_ids = sorted(set(net["ga4"]) | {x for c in containers for x in c["measurement"]["ga4"]})
    L += [
        f"Tag management: **{tms_text}**. "
        + (f"GA4 propert{'y' if len(ga4_ids) == 1 else 'ies'}: {code(ga4_ids)}. " if ga4_ids else "No GA4 property detected. ")
        + "".join(f"Container `{cid}` scores **{r['score']}/100** against best practice "
                  f"({r['fail']} failed, {r['warn']} warning checks). "
                  for cid, r in (audit.get("best_practices") or {}).items() if r.get("score") is not None)
        + (f"Tracking platforms (GA4 + ad pixels) score **{(audit.get('platforms') or {}).get('_overall', {}).get('score')}/100** "
           "on the events they actually received. " if (audit.get("platforms") or {}).get("_overall") else "")
        + f"The audit raised **{len(sev['P1'])} P1**, **{len(sev['P2'])} P2** and **{len(sev['P3'])} P3** findings.",
        "",
    ]
    if findings:
        L += table(["Priority", "Area", "Finding"],
                   [[f["severity"], f["area"], cell(f["title"], 120)] for f in findings[:12]])
    L += ["---", ""]

    # Analyst notes (preserved across re-renders)
    notes = "_Pending analyst review — run the tracking-report skill's analyst pass._"
    if previous_readme and NOTES_START in previous_readme and NOTES_END in previous_readme:
        notes = previous_readme.split(NOTES_START, 1)[1].split(NOTES_END, 1)[0].strip() or notes
    L += ["## 2. Analyst Notes", "", NOTES_START, notes, NOTES_END, "", "---", ""]

    # Next steps: what the automated pass hands to the analyst (no account access — prospecting)
    todo = audit.get("analyst_checklist") or []
    if todo:
        L += ["## Next Steps — Analyst Checks & Discovery Questions", "",
              "_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks "
              "below take minutes from the outside, and the questions are for the discovery conversation._", ""]
        checks_ = [t for t in todo if t.get("kind") == "analyst"]
        questions = [t for t in todo if t.get("kind") == "question"]
        if checks_:
            L += ["**Analyst checks (no account access needed)**", ""]
            L += [f"- [ ] **{t['area']}:** {t['item']}" + (f" — _{t['where']}_" if t.get("where") else "") for t in checks_]
            L.append("")
        if questions:
            L += ["**Discovery questions for the prospect**", ""]
            L += [f"- **{t['area']}:** {t['item']}" for t in questions]
            L.append("")
        L += ["---", ""]

    # GTM container configuration vs best practice
    bp = audit.get("best_practices") or {}
    if bp:
        icon = {"pass": "✅", "warn": "⚠️", "fail": "❌", "info": "ℹ️", "n/a": "—"}
        L += ["## 3. GTM Container Audit — Configuration vs Best Practice", "",
              "Each check compares the live container configuration (decoded from the published container JSON) "
              "with current best practice, weighted by business impact. Score = impact-weighted share of checks "
              "passed (warnings count half).", ""]
        for cid, res in bp.items():
            if cid == "(no GTM)":
                L += ["### No GTM container — Google tag / Shopify app setup review", "",
                      "_No GTM container is deployed, so there is no container to score; these checks review the "
                      "Google tag and app-based setup instead._", ""]
            else:
                L += [f"### `{cid}` — score {res['score'] if res['score'] is not None else '—'}/100 "
                      f"(✅ {res['pass']} · ⚠️ {res['warn']} · ❌ {res['fail']})", ""]
            order = {"fail": 0, "warn": 1, "pass": 2, "info": 3, "n/a": 4}
            imp = {"High": 0, "Medium": 1, "Low": 2}
            rows = [[icon.get(c["status"], c["status"]), c["impact"], c["area"], c["check"], cell(c["evidence"], 220),
                     cell(c["recommendation"], 180)]
                    for c in sorted(res["checks"], key=lambda c: (order.get(c["status"], 9), imp.get(c["impact"], 9)))]
            L += table(["", "Impact", "Area", "Check", "Evidence", "Recommendation"], rows)
        L += ["---", ""]


    # Tracking platform audit: GA4 + ad platforms + email, from the hits actually sent
    pf = {k: v for k, v in (audit.get("platforms") or {}).items() if not k.startswith("_")}
    if pf:
        icon = {"pass": "✅", "warn": "⚠️", "fail": "❌", "info": "ℹ️", "n/a": "—"}
        ov = (audit.get("platforms") or {}).get("_overall") or {}
        L += ["## Tracking Platform Audit — GA4 & Ad Platforms", "",
              "Each platform is judged on the events it actually received during the visit (page view → product view → "
              "add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). "
              f"Overall tracking score: **{ov.get('score', '—')}/100** (✅ {ov.get('pass', 0)} · ⚠️ {ov.get('warn', 0)} · ❌ {ov.get('fail', 0)}).", ""]
        L += table(["Platform", "Score", "✅", "⚠️", "❌", "Deployed via (hits)", "Events seen (phase: event×n)"],
                   [[name, f"{r['score']}" if r.get("score") is not None else "—", str(r["pass"]), str(r["warn"]), str(r["fail"]),
                     cell("; ".join(f"{k} ×{v}" for k, v in sorted((r.get("sources") or {}).items(), key=lambda kv: -kv[1])[:3]), 160),
                     cell("; ".join(f"{ph}: " + ", ".join(f"{e}×{n}" for e, n in evs.items())
                                    for ph, evs in r.get("events_by_phase", {}).items()), 260)]
                    for name, r in pf.items() if name not in ("Stack", "Internal")])
        order = {"fail": 0, "warn": 1, "pass": 2, "info": 3, "n/a": 4}
        for name, r in pf.items():
            L += [f"### {name}" + (f" — {r['score']}/100" if r.get("score") is not None else ""), ""]
            L += table(["", "Impact", "Check", "Evidence", "Recommendation"],
                       [[icon.get(c["status"], c["status"]), c["impact"], c["check"], cell(c["evidence"], 220),
                         cell(c["recommendation"], 160)] for c in sorted(r["checks"], key=lambda c: order.get(c["status"], 9))])
        L += ["---", ""]

    # 3. Tag management & infrastructure
    L += ["## 3. Tag Management & Infrastructure", ""]
    rows = []
    for c in containers:
        rows.append([f"`{c['id']}`", c["kind"].upper(), cell(c.get("version")), f"{c.get('size_kb', '—')} KB",
                     cell(c.get("phase")), "first-party loader" if c.get("first_party_loader") else "googletagmanager.com",
                     str(c["counts"]["active_tags"]), str(c["counts"]["paused_tags"]),
                     str(c["counts"]["variables"]), str(c["counts"]["triggers"])])
    L += table(["Container", "Kind", "Version", "Size", "Captured", "Served from", "Active tags", "Paused",
                "Variables", "Triggers"], rows)
    extra = []
    if net["runtime_tag_ids"]:
        extra.append(f"- Google tag IDs live in `window.google_tag_manager`: {code(net['runtime_tag_ids'])}")
    if net["sgtm_endpoints"]:
        extra.append(f"- First-party / server-side endpoints: {code(net['sgtm_endpoints'][:6])}")
    if net["html_ids"].get("gtm"):
        extra.append(f"- GTM IDs referenced in page HTML: {code(net['html_ids']['gtm'])}")
    L += (extra + [""]) if extra else []
    L += ["---", ""]

    # 4. Platform inventory
    L += ["## 4. Platform Inventory (observed on the network)", ""]
    by_cat: dict[str, list] = {}
    for name, v in net["vendors"].items():
        by_cat.setdefault(v["category"], []).append((name, v))
    for cat in CATEGORY_LABELS:
        if cat not in by_cat:
            continue
        L += [f"### {CATEGORY_LABELS[cat]}", ""]
        rows = []
        for name, v in sorted(by_cat[cat]):
            phases = ", ".join(f"{p}:{v['phases'][p]}" for p in PHASE_ORDER if v["phases"].get(p))
            rows.append([name, code(v["ids"][:6]), str(v["requests"]), phases,
                         "⚠️ " + str(v["failures"]) if v["failures"] else "0"])
        L += table(["Platform", "IDs", "Requests", "By phase", "Failed"], rows)
    if net["unknown_hosts"]:
        L += ["<details><summary>Unclassified third-party hosts</summary>", "",
              ", ".join(f"`{h}` ({n})" for h, n in net["unknown_hosts"][:30]), "", "</details>", ""]
    L += ["---", ""]

    # 5. Measurement IDs
    L += ["## 5. Measurement & Conversion IDs", ""]
    rows = []
    for c in containers:
        m = c["measurement"]
        for k, label in (("ga4", "GA4"), ("google_ads", "Google Ads"), ("floodlight", "Floodlight"), ("ua", "Universal Analytics")):
            if m[k]:
                rows.append([label, code(m[k][:10]), f"{c['id']} (container)"])
        if m["other"]:
            rows.append(["Other tags", cell(m["other"][:12], 400), f"{c['id']} (container)"])
    for name, v in net["vendors"].items():
        if v["ids"] and v["category"] in sig.TRACKING_CATEGORIES | {"email-sms"}:
            rows.append([name, code(v["ids"][:8]), "network"])
    for p in net["web_pixels"]:
        if p["type"] == "APP":
            rows.append([f"Shopify app pixel: {p['app'] or 'unknown app'}",
                         code(p["google_ids"]) if p["google_ids"] else cell(p["configuration"], 120), "Shopify web pixel"])
    for vendor, ids in net["html_code_ids"].items():
        rows.append([vendor, code(ids), "hard-coded in page HTML"])
    L += table(["Platform", "IDs", "Source"], rows) + ["---", ""]

    # 6. GA4 & pixel event flow
    L += ["## 6. Event Flow by Visit Phase", "",
          "Phases: `initial` = first load before consent · `reload` = after consent + reload · "
          "`pdp` = product page · `atc` = after add-to-cart.", ""]
    rows = []
    for tid, g in net["ga4"].items():
        for ph in PHASE_ORDER:
            if g["events"].get(ph):
                rows.append([f"GA4 `{tid}`", ph, cell(", ".join(f"{e}×{n}" for e, n in g["events"][ph].items()), 220),
                             code(g["gcs"].get(ph, []))])
    for name, tree in (("Meta", net["meta_pixel"]), ("TikTok", net["tiktok"]), ("Google Ads", net["google_ads"])):
        for pid, phases in tree.items():
            for ph in PHASE_ORDER:
                if phases.get(ph):
                    rows.append([f"{name} `{pid}`", ph, cell(", ".join(f"{e}×{n}" for e, n in phases[ph].items()), 220), "—"])
    L += table(["Destination", "Phase", "Events (count)", "Consent state (gcs)"], rows)
    dl = net["data_layer_events"]
    if dl:
        L += ["**dataLayer pushes observed:**", ""]
        for ph in PHASE_ORDER:
            if dl.get(ph):
                uniq = list(dict.fromkeys(dl[ph]))
                L.append(f"- `{ph}`: " + cell(", ".join(uniq), 400))
        L.append("")
    L += ["---", ""]

    # 7. Ecommerce
    L += ["## 7. Ecommerce Tracking", ""]
    seen = {e for g in net["ga4"].values() for evs in g["events"].values() for e in evs}
    configured = {e for c in containers for e in c["events"]["ecommerce"]} | {e for c in containers for e in c["ga4_events"]}
    rows = [[f"`{e}`", "✅" if e in configured else "—", "✅" if e in seen else "—"] for e in sig.ECOM_EVENTS
            if e in configured or e in seen or e in ("view_item", "add_to_cart", "begin_checkout", "purchase")]
    L += [f"Product page visited: {cap.get('pdp_url') or '—'} · add-to-cart clicked: {'yes' if cap.get('atc_selector') else 'no'}", ""]
    L += table(["GA4 event", "Configured in container", "Observed on network"], rows)
    L += ["_Checkout and purchase events cannot be observed without placing an order; container configuration is listed instead._",
          "", "---", ""]

    # 8. Consent
    cs = net["consent"]
    ba = cs.get("banner_action") or {}
    L += ["## 8. Consent & Privacy", ""]
    L += table(["Check", "Result"], [
        ["CMP detected", cell(cs["cmp_detected"]) if cs["cmp_detected"] else "None"],
        ["Banner action taken by audit", f"{ba.get('method') or 'no banner found'}" + (f" — {cell(ba.get('detail'), 80)}" if ba.get("detail") else "")],
        ["Shopify Customer Privacy API", "Loaded" if cs["shopify_customer_privacy"] else "—"],
        ["Shopify visitor consent (after accept)", cell(cs.get("shopify_visitor_consent"))],
        ["Google consent state (window.google_tag_data)", cell(cs.get("google_consent_state"), 300)],
        ["Tracking vendors firing before consent", cell(cs["tracking_vendors_before_consent"], 400)],
        ["Scripts held until consent (text/plain, data-consent…)",
         cell(sorted({f"{g['vendor'] or g['src']} [{g['category']}]" for g in cs.get("gated_scripts", [])}), 400)],
        ["Banner still visible after accept + reload",
         "yes — " + cell((cap.get("banner_checks") or {}).get("reload", {}).get("candidates", [{}])[0].get("text"), 120)
         if (cap.get("banner_checks") or {}).get("reload", {}).get("candidates") else "no"],
    ])
    prof = cap.get("profile") or {}
    if prof.get("returning_visit"):
        L += ["_Returning visit: the persistent browser profile already held this site's cookies/consent, so the "
              "`initial` phase reflects stored consent, not a first visit (re-run with `--fresh` for that)._", ""]
    rows = []
    for c in gtm:
        cc = c["consent"]
        rows.append([f"`{c['id']}`", cell(cc["consent_types_referenced"]), cell(cc["consent_templates"]),
                     f"{cc['tags_with_additional_consent']} / {cc['active_tags']}", cell(cc["cmp_hints"])])
    if rows:
        L += ["**Consent configuration inside GTM:**", ""]
        L += table(["Container", "Consent types referenced", "Consent templates", "Tags with extra consent checks", "CMP hints"], rows)
    L += ["---", ""]

    # 9. Container deep dive
    for i, c in enumerate(containers, 1):
        if c["kind"] == "gtag":
            L += [f"## 9.{i} Google Tag Settings — `{c['id']}`", "",
                  "gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).", ""]
            L += table(["Feature", "Settings"], [[f["label"], cell(f["settings"], 160)] for f in c.get("gtag_features", [])])
            L += ["---", ""]
            continue
        L += [f"## 9.{i} Container Deep Dive — `{c['id']}`", ""]
        L += table(["Tag type", "Active", "Paused"],
                   [[t, str(n["active"]), str(n["paused"])] for t, n in c["tag_types"].items()])
        if c["templates"]:
            L += ["**Custom templates:**", ""]
            L += table(["Template", "Vendor (inferred)", "Tags using it", "Injects"],
                       [[f"`{t['id']}`", cell(t["vendor"]), str(t["instances"]), cell(t["injects"], 120)] for t in c["templates"]])
        if c["custom_html"]:
            L += ["**Custom HTML tags:**", ""]
            L += table(["Tag", "Status", "Vendors / IDs", "Fires on", "Preview"],
                       [[cell(t["name"] or f"#{t['tag_id']}"), "paused" if t["paused"] else "active",
                         cell(t["vendors"] + [f"{k}: {', '.join(v)}" for k, v in t["html_ids"].items()], 120),
                         cell(t["fires_on"][:1], 90), cell(t["html_preview"], 90)] for t in c["custom_html"][:40]])
        key_tags = [t for t in c["tags"] if not t["paused"] and t["function"] not in ("__html",)][:60]
        if key_tags:
            L += ["<details><summary>All active tags with firing conditions</summary>", ""]
            L += table(["Tag", "Type", "IDs / event", "Fires on", "Consent"],
                       [[cell(t["name"] or f"#{t['tag_id']}"), t["type"],
                         cell(t.get("ga4_event") or t["ids"], 80), cell(t["fires_on"][:2], 160),
                         cell(t["consent_required"])] for t in key_tags])
            L += ["</details>", ""]
        rc = c.get("reconstruction")
        if rc:
            L += [f"**Reconstructed export:** `containers/{c['id']}.export.json` — {rc['counts']['tags']} tags, "
                  f"{rc['counts']['triggers']} triggers, {rc['counts']['variables']} variables"
                  + (f"; template source missing for {', '.join(rc['custom_templates_missing_source'])}"
                     if rc['custom_templates_missing_source'] else ""), ""]
        if c["events"]["custom"]:
            L += [f"**Custom dataLayer events used as triggers ({len(c['events']['custom'])}):** "
                  + cell(", ".join(f"`{e}`" for e in c["events"]["custom"]), 1500), ""]
        if c["listeners"]:
            L += ["**Auto-event listeners:** " + cell(sorted({l["type"] for l in c["listeners"]})), ""]
        L += ["---", ""]

    # 10. Shopify web pixels
    if net["web_pixels"]:
        L += ["## 10. Shopify Customer Events (Web Pixels)", ""]
        L += table(["Pixel ID", "Type", "App (inferred)", "Purposes", "Config"],
                   [[cell(p["id"]), cell(p["type"]), cell(p["app"]), cell(p["purposes"]), cell(p["configuration"], 120)]
                    for p in net["web_pixels"]])
        L += ["---", ""]

    # 11. Findings
    L += ["## 11. Findings & Recommendations", ""]
    names = {"P1": "P1 — Fix now", "P2": "P2 — Address within 30 days", "P3": "P3 — Clean-up / informational"}
    for s in ("P1", "P2", "P3"):
        if not sev[s]:
            continue
        L += [f"### {names[s]}", ""]
        for f in sev[s]:
            L += [f"**[{f['area']}] {f['title']}**  ", f"{f['detail']}  ", f"_Recommendation:_ {f['recommendation']}", ""]
    if not findings:
        L += ["_No automated findings._", ""]
    if net["failures"]:
        L += ["<details><summary>Failed requests</summary>", ""]
        L += table(["Vendor", "Phase", "Status / error", "URL"],
                   [[f["vendor"], f["phase"], cell(f["status"] or f["failure"]) + (" (likely capture network)" if f.get("environment") else ""),
                     cell(f["url"], 100)] for f in net["failures"][:30]])
        L += ["</details>", ""]
    L += ["---", ""]

    # 12. Method
    L += ["## 12. Method & Files", "",
          "Captured with Playwright (real Chromium, fresh profile) intercepting every request in all frames. "
          "Visit: homepage → consent accepted → tab reloaded → first product page → add to cart. GTM containers "
          "are captured from the consented reload and decoded from the container's embedded JSON (tags, triggers, "
          "variables, templates, permissions) rather than regex scraping.", "",
          "| File | Contents |", "|---|---|",
          "| `containers/<ID>.json` | Decoded container JSON as served (resource, runtime, permissions) |",
          "| `containers/<ID>.js` | Raw container script |",
          "| `containers/GTM-<ID>.export.json` | Reconstructed GTM workspace export (tags, triggers, variables) — names "
          "are generated where the container doesn't publish them; custom-template source not included |",
          "| `audit.json` | Full structured analysis behind this report |",
          "| `raw/network.json` | Every intercepted request with phase, status and payload |",
          "| `raw/capture.json` | Visit log, consent result, page snapshots (dataLayer, Shopify, consent state) |",
          "",
          "_Limitations: one product page per site, no checkout/purchase; server-side containers are only visible "
          "through their client-side traffic. Consent banners and pixels can vary by visitor country; connection-level "
          "errors (resets, SSL, ORB) are shown but not treated as site faults, as they often come from the capture "
          f"network.{' Capture location signals: ' + capture_geo(audit) if capture_geo(audit) else ''}_",
          ""]

    # Appendix: capture verification (supplemental)
    review = cap.get("review") or {}
    L += ["## Appendix — Capture Verification", "",
          "_Supplemental: confirms the capture saw the site as a consenting visitor would._", ""]
    if review:
        status = (("✅ verified" if cap.get("review_resolved") else "⚠️ needs manual verification")
                  if review.get("needs_review") else "✅ passed")
        L.append(f"- Coverage check: {status}" + (f" — {cell(review['reasons'], 300)}" if review.get("reasons") else "")
                 + (f" (resolution: {cap['review_resolved']})" if cap.get("review_resolved") else ""))
    if (cap.get("profile") or {}).get("returning_visit"):
        L.append("- Returning visit: the persistent browser profile already held this site's consent, so `initial` "
                 "reflects stored consent (re-run with `--fresh` for a first-visit view).")
    ba = net["consent"].get("banner_action") or {}
    L.append(f"- Consent action: {ba.get('method') or 'none'}" + (f" — {cell(ba.get('detail'), 80)}" if ba.get("detail") else ""))
    shots = cap.get("screenshots") or []
    if shots:
        L.append("- Screenshots: " + " · ".join(f"[{Path(x).stem}]({x})" for x in shots))
    L.append("")
    return _reorder("\n".join(L))


def render_index(root: Path, slugs: list[str] | None = None) -> str:
    audits = []
    for p in sorted(root.glob("*/audit.json")):
        if slugs and p.parent.name not in slugs:
            continue
        try:
            audits.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    L = ["# Tracking & Martech Audits", "",
         "One folder per brand. Open `<brand>/README.md` for the report.",
         "Generated by `audit.py index`. See the repo-root README.md for how to run audits.", "",
         "| Brand | Platform | Tag management | GTM container score | Tracking score | GA4 | CMP | P1 | P2 | P3 | Top issue |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in audits:
        b, net, f = a["brand"], a["network"], a["findings"]
        gtm = ", ".join(c["id"] for c in a["containers"] if c["kind"] == "gtm") or ("sGTM" if net["sgtm_endpoints"] else "—")
        top = next((x["title"] for x in f if x["severity"] == "P1"), f[0]["title"] if f else "—")
        n = lambda s: str(sum(x["severity"] == s for x in f))
        scores = [f"{r['score']}/100" if r.get("score") is not None else ("empty" if cid.startswith("GTM-") else "n/a (no GTM)")
                  for cid, r in (a.get("best_practices") or {}).items()]
        cmp = net["consent"]["cmp_detected"] or [f"{x} (geo-targeted)" for x in net["consent"].get("geo_targeted_cmp", [])]
        tscore = ((a.get("platforms") or {}).get("_overall") or {}).get("score")
        L.append(f"| [{b['name']}]({b['slug']}/README.md) | {cell(b.get('platform'))} | {gtm} | {cell(scores)} | "
                 f"{str(tscore) + '/100' if tscore is not None else '—'} | "
                 f"{cell(sorted(net['ga4']), 60)} | {cell(cmp, 50) if cmp else 'None'} | "
                 f"{n('P1')} | {n('P2')} | {n('P3')} | {cell(top, 90)} |")
    L += ["", f"_{len(audits)} brand(s). Generated by the tracking-audit skill._", ""]
    return "\n".join(L)
