"""Rule-based findings over the combined container + network analysis."""

import re

from . import signatures as sig

P1, P2, P3 = "P1", "P2", "P3"


def build_findings(audit: dict) -> list[dict]:
    net = audit["network"]
    containers = audit["containers"]
    cap = audit["capture"]
    out: list[dict] = []

    def add(sev, area, title, detail, rec):
        out.append({"severity": sev, "area": area, "title": title, "detail": detail, "recommendation": rec})

    vendors = net["vendors"]
    ad_vendors = sorted(k for k, v in vendors.items() if v["category"] == "advertising")
    consent = net["consent"]
    gtm = [c for c in containers if c["kind"] == "gtm"]

    # ── Capture quality ──────────────────────────────────────────────────────
    review = cap.get("review") or {}
    if review.get("needs_review") and not cap.get("review_resolved"):
        add(P1, "Capture", "Capture flagged for manual verification",
            "Automated coverage check: " + "; ".join(review["reasons"]) + ". Ecommerce sites always run analytics "
            "and ad tracking, so missing tracking is treated as a capture gap until verified.",
            "Review the screenshots and re-capture via the Playwright MCP fallback (tracking-capture skill), accepting "
            "the consent banner manually.")
    gated = [g for g in net["consent"].get("gated_scripts", []) if g["vendor"]]
    if gated:
        add(P3, "Consent", f"{len(gated)} tracking script(s) held until consent",
            "Parked as non-executable until the CMP grants consent: "
            + ", ".join(sorted({f"{g['vendor']} ({g['category']})" for g in gated})) + ".",
            "Positive if intentional; make sure the banner is actually shown to the visitors it applies to, "
            "otherwise these tags never fire.")

    # ── Consent & privacy ────────────────────────────────────────────────────
    has_cmp = bool(consent["cmp_detected"]) or consent["shopify_customer_privacy"]
    geo_cmp = consent.get("geo_targeted_cmp") or []
    opt_out = consent.get("us_opt_out_link")
    if not consent["cmp_detected"] and ad_vendors:
        if geo_cmp or opt_out:
            add(P3, "Consent", "No consent banner shown to this (US) visitor",
                f"{len(ad_vendors)} ad platform(s) fire without a banner — normal for US opt-out. "
                + (f"Geo-targeted CMP present in the page: {', '.join(geo_cmp)}. " if geo_cmp else "")
                + ("A US opt-out link (Do Not Sell / Your Privacy Choices) is present." if opt_out else
                   "No US opt-out link (Do Not Sell / Your Privacy Choices) found."),
                "Confirm EU/UK visitors get an opt-in banner and that the US opt-out link + GPC actually suppress "
                "ad pixels (Shopify Customer Privacy sale_of_data).")
        else:
            add(P1, "Consent", "No consent banner or US opt-out mechanism",
                f"{len(ad_vendors)} advertising platform(s) fire ({', '.join(ad_vendors[:8])}); no CMP, no geo-targeted "
                "banner markup and no 'Do Not Sell or Share' / 'Your Privacy Choices' link were found.",
                "Enable Shopify's privacy banner (or a CMP) with region rules: opt-in for EU/UK, opt-out link + GPC for "
                "US state privacy laws (CCPA/CPRA and others).")
    pre = consent["tracking_vendors_before_consent"]
    returning = (cap.get("profile") or {}).get("returning_visit")
    if consent["cmp_detected"] and pre and not returning:
        pre_ads = [v for v in pre if vendors.get(v, {}).get("category") == "advertising"]
        shown = (consent.get("banner_action") or {}).get("method") in ("selector", "button_text", "banner_scan")
        if pre_ads and shown:
            add(P2, "Consent", "Ad pixels fire before the visible consent banner is answered",
                f"A consent banner ({', '.join(consent['cmp_detected'])}) was shown, yet these fired on first load before "
                f"it was answered: {', '.join(pre_ads)}. The banner implies opt-in, but tags don't wait for it.",
                "Hold marketing tags until consent (Consent Mode default 'denied' + CMP-gated triggers), or switch the "
                "banner to an opt-out notice for US visitors if that is the intended model.")
        elif pre_ads:
            add(P3, "Consent", "Ad pixels fire on load (no banner shown to this visitor)",
                f"{', '.join(consent['cmp_detected'])} is present but showed no banner to this US visitor; "
                f"{', '.join(pre_ads)} fired on load — consistent with a US opt-out model.",
                "Confirm EU/UK visitors get an opt-in banner and US opt-out (Do Not Sell / GPC) suppresses these pixels.")
    post = {g for v in net["ga4"].values() for ph, s in v["gcs"].items() if ph in ("reload", "pdp", "atc") for g in s}
    if consent.get("banner_action", {}) and consent["banner_action"].get("accepted") and post and post <= {"G100"}:
        add(P1, "Consent", "Consent accepted but Google tags still report 'denied'",
            f"After accepting the banner and reloading, GA4 hits still carried gcs={', '.join(sorted(post))}.",
            "Fix the CMP → Consent Mode update sync (consent update command / template trigger order).")
    # GA4 / ad-platform event quality is scored in platforms.py.
    # ── Google tag hygiene ───────────────────────────────────────────────────
    ua_live = [t for c in containers for t in c["tags"] if t["function"] == "__ua" and not t["paused"]]
    if ua_live or "Universal Analytics" in vendors:
        add(P2, "Analytics", "Universal Analytics still deployed",
            f"{len(ua_live)} active UA tag(s) in GTM" + (" and UA requests on the network" if "Universal Analytics" in vendors else "")
            + ". UA stopped processing data in July 2024.",
            "Delete UA tags, GA Settings variables and UA-only triggers.")
    for c in containers:
        if c["kind"] == "gtag" and not re.fullmatch(r"(G|GT|AW|DC)-[A-Z0-9]{4,}", c["id"]):
            add(P1, "Advertising" if c["id"].startswith("AW") else "Analytics",
                f"Google tag loaded with an invalid ID ({c['id']})",
                f"gtag.js was requested for `{c['id']}` — a tag is configured with a placeholder / unset ID, so "
                "its hits go nowhere.",
                "Find the tag (GTM Google Tag / Ads tag or theme snippet) using this ID and set the real ID or remove it.")
        for aw in c["measurement"]["google_ads"]:
            num = aw.split("/")[0][3:]
            if num.startswith("0") or (num.isdigit() and not 9 <= len(num) <= 11):
                add(P1, "Advertising", f"Malformed Google Ads conversion ID {aw.split('/')[0]}",
                    f"{c['id']} sends conversions to `{aw}`, which is not a valid Ads conversion ID format.",
                    "Correct the conversion ID (check the leading digit) and verify conversions in Google Ads.")

    # ── Broken / failing vendors ─────────────────────────────────────────────
    failing = sorted({f["vendor"] for f in net["failures"] if not f.get("environment")})
    if failing:
        add(P2, "Data quality", "Tracking requests failing",
            f"Requests failed or returned errors for: {', '.join(failing)}.",
            "Check each failing endpoint (blocked domain, retired pixel, wrong ID) and remove or fix the tag.")

    # ── Governance / tag sprawl ──────────────────────────────────────────────
    if len(gtm) > 1:
        add(P2, "Governance", f"{len(gtm)} GTM containers on the site",
            f"Containers: {', '.join(c['id'] for c in gtm)}.",
            "Consolidate where possible or document ownership; multiple containers cause duplicate firing and drift.")
    for cid in cap.get("unpublished_containers") or []:
        add(P2, "Governance", f"GTM container {cid} is referenced but not published",
            f"The site requests {cid}, but googletagmanager.com returns 404, so the container is unpublished or deleted. "
            "Any tags expected from it never fire.",
            "Remove the snippet (theme or Shopify custom pixel), or publish the container if it's meant to be live.")

    # Container hygiene / config quality is scored in best_practices.py.

    # ── Tags outside GTM ─────────────────────────────────────────────────────
    gtm_ga4 = {x for c in containers for x in c["measurement"]["ga4"]} | {c["id"] for c in containers if c["kind"] == "gtag"}
    outside = sorted(set(net["ga4"]) - gtm_ga4)
    if gtm and outside:
        add(P3, "Governance", "GA4 data sent outside GTM",
            f"{', '.join(outside)} received hits but is not configured in any captured GTM container "
            "(likely a Shopify app pixel, hard-coded gtag, or sGTM-only routing).",
            "Decide on one owner for each GA4 property to avoid double counting.")
    app_google = {i for p in net["web_pixels"] for i in p["google_ids"] if i.startswith("G-")}
    both = sorted(app_google & {x for c in containers for x in c["measurement"]["ga4"]})
    if both:
        add(P2, "Analytics", "Same GA4 property in a Shopify app pixel and GTM",
            f"{', '.join(both)} is configured both in the Shopify Google & YouTube app and in GTM.",
            "Keep a single source per property or events will double count.")

    if net["sgtm_endpoints"]:
        add(P3, "Infrastructure", "Server-side tagging detected",
            f"First-party collection endpoints: {', '.join(net['sgtm_endpoints'][:5])}.",
            "Positive: verify the server container forwards consent state and that client + server tags do not double send.")

    order = {P1: 0, P2: 1, P3: 2}
    out.sort(key=lambda f: order[f["severity"]])
    return out
