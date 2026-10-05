"""Next steps for a prospecting audit: what the automated capture can't settle on its own.

These audits are run on prospects — we have no access to their GA4, ad accounts, GTM workspace or Shopify
admin. The tool is a fast first pass for the analyst, not a replacement, so open questions are handed over as:

  kind="analyst"   checks the analyst can do from the outside (browser, tag debugger extensions, EU VPN,
                   view-source) in a few minutes;
  kind="question"  discovery questions for the prospect conversation, phrased from what we observed.

Each item: {kind, area, item, where, reason}. Items are generated from the findings, the platform scorecards
and each platform's deployment route (native Shopify app vs GTM vs theme vs custom pixel).
"""

from collections import Counter

from .sources import significant_routes

DEBUGGERS = "Tag Assistant / Meta Pixel Helper / TikTok Pixel Helper + DevTools → Network"


def build_checklist(audit: dict) -> list[dict]:
    net, cap, pf = audit["network"], audit["capture"], audit.get("platforms") or {}
    shopify = audit["brand"].get("platform") == "Shopify"
    ecommerce = shopify or bool(cap.get("pdp_url"))
    items: list[dict] = []
    seen = set()

    def add(kind, area, item, where="", reason=""):
        if item not in seen:
            seen.add(item)
            items.append({"kind": kind, "area": area, "item": item, "where": where, "reason": reason})

    def checks(platform):
        return pf.get(platform, {}).get("checks", []) if isinstance(pf.get(platform), dict) else []

    def routes(platform):
        return sorted(significant_routes(Counter(pf.get(platform, {}).get("sources") or {})))

    def top_sources(platform, n=3):
        src = Counter(pf.get(platform, {}).get("sources") or {})
        return ", ".join(k for k, _ in src.most_common(n))

    # ── Analyst checks (no account access needed) ─────────────────────────────────────────────
    review = cap.get("review") or {}
    if review.get("needs_review") and not cap.get("review_resolved"):
        add("analyst", "Capture", "Re-check the site manually — the automated capture was flagged: " + "; ".join(review["reasons"]),
            DEBUGGERS)
    dup_atc = sorted({c["area"] for p in pf.values() if isinstance(p, dict) for c in p.get("checks", [])
                      if c["check"] == "Add to cart sent once per cart add" and c["status"] == "warn"})
    if dup_atc:
        add("analyst", "Ecommerce", f"Add one product to cart and confirm each platform records ONE add-to-cart "
            f"({', '.join(dup_atc)} fired twice in the capture)", DEBUGGERS)
    adds = [s for s in net.get("atc_cart_add_status") or [] if isinstance(s, int)]
    if cap.get("pdp_url") and adds and all(s in (401, 403, 429) for s in adds):
        add("analyst", "Ecommerce", "Add-to-cart was blocked for the automated browser — test add to cart manually", DEBUGGERS)
    elif cap.get("pdp_url") and adds and all(300 <= s < 400 for s in adds):
        add("analyst", "Ecommerce", "Cart add redirects to /cart — manually confirm add_to_cart reaches GA4 and the ad pixels",
            DEBUGGERS)
    for f in audit["findings"]:
        if "invalid ID" in f["title"]:
            add("analyst", "Google tag", f"Find which route loads the placeholder ID ({f['title'].split('(')[-1].rstrip(')')}) — "
                "search page source / Shopify app scripts for it", "View source + DevTools → Network (initiator column)")
    for platform in ("GA4", "Google Ads", "Meta", "TikTok", "Pinterest", "Microsoft Ads"):
        r = routes(platform)
        if "Theme" in r:
            add("analyst", platform, f"Confirm the hard-coded {platform} snippet in the theme (view source) — it runs alongside "
                f"other routes ({top_sources(platform)})", "View source / DevTools → Network → Initiator")
    if ecommerce:
        add("analyst", "Consent", "Visit from an EU/UK VPN: does a banner appear, and do ad pixels wait for consent?",
            "Browser via EU VPN + DevTools → Network")
    if not net["consent"].get("us_opt_out_link"):
        add("analyst", "Consent", "Check the footer for a 'Your Privacy Choices / Do Not Sell or Share' link (none found on "
            "the homepage HTML)", "Site footer, privacy policy")

    # ── Discovery questions for the prospect ──────────────────────────────────────────────────
    if any("thank-you / checkout" in f["title"] for f in audit["findings"]):
        add("question", "Purchase tracking", "Since Shopify's checkout upgrade (Checkout Extensibility), do Google Ads / GTM "
            "purchase conversions still match Shopify orders? Some purchase tags here are tied to the old thank-you page.",
            reason="purchase tags on thank-you URLs")
    elif ecommerce:
        add("question", "Purchase tracking", "Do GA4 revenue and Google Ads / Meta purchase counts reconcile with Shopify "
            "orders (a gap above ~10% usually means a tracking problem)?")
    multi = [p for p in ("GA4", "Google Ads", "Meta", "TikTok", "Pinterest", "Microsoft Ads") if len(routes(p)) > 1]
    if multi:
        add("question", "Ownership", f"{', '.join(multi)} are fed by more than one route "
            f"({'; '.join(f'{p}: ' + ', '.join(routes(p)) for p in multi)}). Who manages each, and which one is meant to "
            "be the source of truth?", reason="multiple deployment routes")
    for platform, label in (("GA4", "GA4 properties"), ("Google Ads", "Google Ads accounts"), ("Meta", "Meta pixels"),
                            ("Microsoft Ads", "UET tags"), ("TikTok", "TikTok pixels"), ("Pinterest", "Pinterest tags")):
        for c in checks(platform):
            if c["check"].startswith("Single ") and c["status"] == "warn" and "receive data" in c["evidence"]:
                add("question", platform, f"Are all of these {label} still in use (any agency or legacy accounts)? "
                    + c["evidence"].split(":", 1)[-1].strip(), reason="multiple IDs")
    meta_src = " ".join((pf.get("Meta") or {}).get("sources", {}) or [])
    if pf.get("Meta"):
        if "Shopify app: Meta" in meta_src:
            add("question", "Meta", "Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), "
                "and what Event Match Quality do Purchase events get?")
        else:
            add("question", "Meta", "Meta runs through GTM / theme code, not the native Shopify app — is the Conversions API "
                "sent server-side anywhere (Elevar, Stape, a CAPI gateway)?")
    if pf.get("Google Ads"):
        add("question", "Google Ads", "Which conversion action is primary for purchases — the Google & YouTube app, a GTM "
            "tag or a GA4 import — and is enhanced conversions on?")
    if pf.get("TikTok") and "Shopify app: TikTok" not in " ".join((pf.get("TikTok") or {}).get("sources", {}) or []):
        add("question", "TikTok", "TikTok runs outside the native Shopify app — is the Events API connected for purchases?")
    if net["consent"].get("geo_targeted_cmp") or net["consent"]["cmp_detected"] or ecommerce:
        add("question", "Consent", "Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?")
    for f in audit["findings"]:
        if "not published" in f["title"] or "Container has tags" in f["title"]:
            add("question", "GTM", "A GTM container loads but has no live tags — was it meant to take over from the apps, or "
                "can it be removed?", reason=f["title"])
        if "requests failing" in f["title"]:
            add("question", "Vendors", f"Is {f['detail'].split(':', 1)[-1].strip().rstrip('.')} still an active partner? Its "
                "tracking requests fail.", reason=f["title"])
    if pf.get("Klaviyo"):
        add("question", "Email / SMS", "Are browse- and cart-abandonment flows live in Klaviyo, and are Viewed Product / "
            "Added to Cart metrics recording?")
    return items
