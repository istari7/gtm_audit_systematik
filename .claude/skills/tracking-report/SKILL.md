---
name: tracking-report
description: Render the client-ready outputs/<brand>/README.md from audit.json (GTM container configuration vs best practice first), run the analyst pass (verify P1s against the container JSON and network evidence, write business-focused Analyst Notes), and rebuild outputs/AUDIT_INDEX.md (the root README is static how-to docs). Step 3 of the tracking-audit skill.
---

# GTM Report

```
python .claude/skills/tracking-audit/scripts/audit.py report <brands...>
python .claude/skills/tracking-audit/scripts/audit.py index
```

`report` regenerates `outputs/<slug>/README.md` from `audit.json`, **except** the block between
`<!-- ANALYST_NOTES_START -->` and `<!-- ANALYST_NOTES_END -->`, which is preserved.
Never hand-edit other sections — fix the data/rules (`best_practices.py`, `findings.py`) and re-render.

## Report structure (container-first)

1. Executive summary — tag management, GA4, container score, P1/P2/P3 table
2. Analyst Notes
3. **GTM Container Audit — configuration vs best practice** (scorecard per container: status, impact,
   evidence from the container JSON, recommendation)
4. **Tracking Platform Audit — GA4 & ad platforms** (overall tracking score, per-platform score table with
   events seen per phase, then per-platform checks)
4. Container inventory & settings — tag types, templates, Custom HTML, tags + firing triggers,
   reconstructed export; Google-tag (gtag.js) settings
5. Measurement & conversion IDs · Ecommerce · Consent · Event flow (network validation)
6. Shopify web pixels · Tag management infrastructure · Platform inventory
7. Findings P1/P2/P3 · Method & files
8. Appendix — capture verification (coverage check, consent action, screenshot links). Supplemental only.

## Next Steps (generated): prospecting, no account access

`analyst_checks.py` writes a **Next Steps** section after the notes, in two parts:
- **Analyst checks (no access needed)**: minutes of outside-in work: manual add-to-cart with Tag Assistant /
  Pixel Helpers, EU-VPN visit, view-source to confirm a hard-coded snippet, footer opt-out link.
- **Discovery questions for the prospect**: purchase reconciliation vs Shopify orders, who owns each deployment
  route, unused IDs, Meta CAPI / data sharing, primary Google Ads conversion + enhanced conversions, EU/Quebec
  consent, abandoned GTM containers, failing partners, Klaviyo flows.

The audit is a speed-up, not a replacement, and we never have account access: do not try to prove things that
need platform UIs; add a rule in `analyst_checks.py` that turns them into a check or a question.

## Analyst pass (per brand)

The audit's value is the **container configuration judged against best practice and business
impact**. Notes should read like a consultant's view of the setup, not a list of network traffic.

1. Read `audit.json` → `best_practices` (failed / warning checks), `findings`, `containers[]` (tags,
   `fires_on`, templates, custom HTML), `network.ga4` (`sources`, `page_views`), `network.web_pixels`.
2. Verify every **P1** before it goes in the notes:
   - Duplicate GA4 / split ownership → confirm in `raw/network.json` that two hits go to the same `tid`
     on one load, and say where each comes from (page vs Shopify custom pixel vs app).
   - `add_to_cart` missing → was there a `/cart/add` request in the `atc` phase? Redirect (302) adds are
     "verify", not fact.
   - Thank-you / checkout tags → confirm the container loads on the storefront (not a custom pixel).
   - Failures marked "likely capture network" are not site faults.
3. Write 4–7 bullets between the markers:
   - **Setup** — how tracking is built, from `platforms.<P>.sources` (native Shopify app vs GTM, and what loads
     it, vs custom pixel vs theme), and which platforms are fed by more than one route.
   - **What's working** — briefly, so the client sees credit where due.
   - **Platform health** — one line on GA4 and each paid channel (e.g. "Meta: ViewContent/AddToCart fine,
     no event_id → CAPI double counting"; "Pinterest: no add-to-cart").
   - **Top 2–3 issues by business impact** — revenue attribution, bidding signal, compliance, data trust;
     name the tag / ID and the consequence.
   - **Fix order** — the 2–3 actions that move the needle most; skip nice-to-haves for small brands
     (e.g. don't push sGTM on a lean DTC stack).
   - Any capture caveat (MCP fallback, geo).
   - Don't spend time proving things that need account access — point to the Next Steps item (analyst check or discovery question) instead.
4. `audit.py index` once all brands are done (updates `outputs/AUDIT_INDEX.md`; never put brand data in the root `README.md`).

Screenshots are for verifying the capture only — don't cite them as findings.
