---
name: tracking-audit
description: Run a full tracking & martech audit (GTM container config, GA4, Google Ads, Meta, TikTok, Pinterest, Microsoft Ads, Klaviyo, consent) for one or more brand websites and write one folder per brand (decoded GTM container JSON, network capture, client-ready README). Use when the user says "audit these brands/URLs", "/tracking-audit", "run the GTM / tracking audit", or gives a list of sites to audit. Orchestrates the tracking-capture, tracking-parse and tracking-report skills.
---

# Tracking & Martech Audit (orchestrator)

**Scope — two scorecards per brand, judged by business impact** (revenue attribution, bidding signal,
compliance, data trust, maintenance cost):

1. **GTM container configuration vs best practice** (`best_practices.py`) — how the container is built.
2. **Tracking platform audit** (`platforms.py`) — what GA4, Google Ads, Meta, TikTok, Pinterest,
   Microsoft Ads, Klaviyo and other pixels actually received during the visit (page view → product view →
   add to cart): duplicates, missing events, product/value/currency params, CAPI event_id, enhanced
   conversions, consent signals, first-party ID cookies — regardless of whether GTM, a Shopify app,
   a custom pixel or hard-coded script sent it.

Consent / privacy and stack hygiene run alongside. Screenshots are supplemental capture verification only.

**Used for prospecting, with no access to the brand's accounts; it's a fast first pass for the analyst, not a replacement.** Anything that needs platform access, a test
order, a non-US visit or an ownership call goes into the report's **Next Steps** (outside-in analyst checks + discovery questions for the prospect) rather than
being guessed or over-automated.

Audits live sites by driving a real browser with Playwright, intercepting every network
request, accepting the consent banner, **reloading the tab** to capture the GTM container
with consent granted, decoding the container's embedded JSON, and producing a report.

All code lives in `scripts/` next to this file. Always run from the repo root (containing `brands.txt`).
Everything is written to `outputs/<slug>/` (index: `outputs/AUDIT_INDEX.md`); `--out <dir>` overrides. `examples/`
holds finished sample audits; don't write new audits there:

```
python .claude/skills/tracking-audit/scripts/audit.py <command> [brands...]
```

## Inputs

- Brands = URLs (`bychari.com`, `https://www.getgrinds.com/`), `slug=url` to force a folder name,
  or nothing (falls back to `brands.txt`, one entry per line).
- Folder name = the domain's brand label: `www.explorescientific.ca` → `outputs/explorescientific/`,
  `arubaaloe.com/en-en` → `outputs/arubaaloe/`.
- Append any new brand the user names to `brands.txt` so re-runs pick it up.

## Steps

Run these in order. Each step is its own skill — invoke it with the Skill tool and follow it.
Pass the same brand list to every step.

1. **Capture** → `tracking-capture` skill.
   Playwright visit per brand in a **persistent browser profile** (`.browser-profile/`, so consent
   and cookies are remembered): homepage → accept consent → reload tab → product page → add to
   cart, with a screenshot at each phase. Saves `containers/<ID>.json` (+ `.js`), `screenshots/`
   and `raw/`. Then **look at the screenshots for every brand** and clear every `needs_review` flag
   with the Playwright MCP fallback or `resolve`.
   **Hard rule: an ecommerce site always runs analytics and ad tracking.** If a capture shows none,
   the capture is wrong. Fix it before reporting; never report "no tracking" as a finding.
2. **Parse** → `tracking-parse` skill.
   Decodes each container (tags, triggers, variables, templates, IDs, consent config) and the
   network capture into `outputs/<brand>/audit.json` with rule-based findings. It also reconstructs each GTM
   container as a GTM workspace export at `containers/GTM-<ID>.export.json`.
3. **Report** → `tracking-report` skill.
   Renders `outputs/<brand>/README.md`, does the analyst pass (verify P1s, write Analyst Notes), and
   rebuilds `outputs/AUDIT_INDEX.md` (the root `README.md` is static how-to docs).

Shortcut when nothing needs manual attention: `audit.py run <brands>` does capture + parse +
report + index in one go — still do the tracking-capture verification and the tracking-report analyst pass
afterwards.

## Output per brand

```
outputs/<slug>/
  README.md              client-ready audit
  audit.json             structured analysis (source of truth for the README)
  containers/<ID>.json   decoded container JSON as served (GTM-…, G-…, AW-…, GT-…)
  containers/<ID>.js     raw container script
  containers/GTM-<ID>.export.json  reconstructed GTM workspace export (tags/triggers/variables)
  screenshots/           01_initial, 02_after_consent, 03_reload, 04_pdp, 05_atc
  raw/network.json       every request: phase, url, method, status, POST body, failure
  raw/capture.json       visit log, consent result, page snapshots (dataLayer, Shopify, consent)
  raw/page.html          homepage HTML after the consented reload
```

## Finish

Reply with a short table: brand · tag management · GTM container score · tracking score · P1 count · top issue, plus
any brand that needed the MCP fallback or still has gaps. Don't paste reports into chat.
