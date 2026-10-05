# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A tracking & martech audit workspace used for **prospecting**: audits are run on
brands we have **no account access to**, purely from the outside. Each audited brand gets one folder under
`outputs/` (`outputs/<slug>/`) with a client-ready `README.md`. Brand folders and `outputs/AUDIT_INDEX.md` are
**generated output**; `examples/` holds finished sample audits (same layout, render with `--out examples`); the root `README.md` is hand-written how-to docs (never write brand data into it). The tooling lives in
project skills under `.claude/skills/`:

- `tracking-audit` — orchestrator (owns all code in `.claude/skills/tracking-audit/scripts/`)
- `tracking-capture` → `tracking-parse` → `tracking-report` — the three steps it invokes

To audit brands, use the `tracking-audit` skill (it calls the others). The audit covers the GTM container
(configuration vs best practice) **and** the tracking platforms themselves — GA4, Google Ads, Meta, TikTok,
Pinterest, Microsoft Ads, Klaviyo, other pixels — plus consent/privacy, judged by business impact.

## Commands

Run everything from the repo root (Python 3.11 + `playwright`; Chrome channel preferred, bundled Chromium fallback):

```
python .claude/skills/tracking-audit/scripts/audit.py run [brands...] [--fresh] [--parallel 3] [--no-pdp] [--headless] [--dwell 5000]
python .claude/skills/tracking-audit/scripts/audit.py capture|parse|report [brands...]
python .claude/skills/tracking-audit/scripts/audit.py index        # writes outputs/AUDIT_INDEX.md
python .claude/skills/tracking-audit/scripts/audit.py fetch GTM-XXXX [G-XXXX AW-XXXX] --brand <slug>
python .claude/skills/tracking-audit/scripts/audit.py ingest <url> --brand <slug> --requests reqs.txt [--consent "..."] [--snapshot snap.json]
python .claude/skills/tracking-audit/scripts/audit.py resolve <slug> --note "how the review flag was verified"
```

- Output root is `outputs/` (`--out <dir>` to change). Brands are URLs, `slug=url`, or omitted (falls back to the repo-root `brands.txt`). Slug = domain label (`www.explorescientific.ca` → `explorescientific`).
- `run` = capture + parse + report + index. Capture takes ~1–2 min/brand; run batches with `run_in_background`.
- After changing any rule/report code, re-run only `parse` then `report` (and `index`) — no re-capture needed.
  Cookie-based checks need data from a capture made with the current code (`raw/capture.json → cookies_after`).
- There is no test suite. Validate changes by running `parse` + `report` on one or two brands and reading the output.

## Architecture (pipeline, per `outputs/<slug>/`: `raw/` → `audit.json` → `README.md`)

**Capture** (`capture.py`) — Playwright in **one persistent Chrome profile** (`.browser-profile/`, gitignored), one tab
per brand, per-page request/response hooks (includes iframes such as Shopify web-pixel sandboxes). Visit phases tag every
request: `initial` (pre-consent) → `consent` (accept banner: CMP selectors → button text → CMP JS APIs → banner scan) →
`reload` (tab reloaded with consent; containers captured here) → `pdp` (most-linked product) → `atc` (add to cart).
Any script body containing GTM's `var data = {"resource": …}` literal is saved as a container (catches first-party /
sGTM / app loaders). Also writes screenshots per phase, page snapshots (`snapshot.js`, shared with the MCP fallback), cookie names,
the **CDP initiator chain** per request (`raw/initiators.json`), and an automatic coverage review
(`review.needs_review`). After add-to-cart it opens `/cart` so batched hits flush. `--fresh` clears a brand's
cookies/storage.

**Parse** (`__main__.parse_brand`) builds `audit.json` from five analysers:
- `container.py` — JSON-decodes the container (`resource.tags/macros/predicates/rules`, `permissions`, `blob`), resolves
  value encodings (`["macro",i]`, `["template",…]`, `["map",…]`), rebuilds firing triggers, infers custom-template vendors
  from permissions, summarises gtag.js (`G-/AW-/GT-`) features.
- `reconstruct.py` — writes `containers/GTM-<ID>.export.json` in GTM export format (names generated; template source not published).
- `network.py` — vendor classification (`signatures.VENDORS`), IDs, GA4 hit parsing, sGTM / Shopify custom-pixel
  deployment detection, CMP detection (network, clicked banner, HTML markers), US opt-out link, failures (connection-level
  errors flagged `environment` — often the capture network, not the site).
- `best_practices.py` — **GTM container scorecard** (measurement, ecommerce, Google Ads, paid social, consent, Shopify
  checkout, custom-pixel deployment, governance). Brands without GTM get a Google-tag/app review and no score.
- `sources.py` — **deployment attribution** ("inheritance"): which route sent each hit — native Shopify app
  (hit markers like Meta `a=shopify_web_pixel`, TikTok `partner:Shopify`, Pinterest `np=shopify-web-pixel`, or no
  initiator = sandboxed app worker), custom pixel (`/custom/web-pixel-<id>@` frame), GTM (+ what loaded it), app
  embed / proxy, theme. Per-hit stack (ranked, skipping fetch-wrapper scripts), else the platform library's
  loader (`gtag/js?id=`, `fbevents.js`, `events.js?sdkid=`...). `significant_routes` ignores stray beacons.
- `platforms.py` — **tracking platform scorecard** from the hits each platform actually received (duplicates, ecommerce
  events + params, CAPI event_id, enhanced conversions, consent signals, first-party cookies).
- `analyst_checks.py` — the report's **Next Steps**: `analyst` checks doable without access (manual add-to-cart
  with tag debuggers, EU-VPN visit, view-source) and `question` items: discovery questions for the prospect
  (purchase reconciliation, route ownership, CAPI / enhanced conversions, consent regions).
- `findings.py` — consent/privacy, capture, Google-tag hygiene, governance rules. Failed/warn checks from both scorecards
  are also turned into findings (fail+High → P1; fail or warn+High → P2; else P3).

**Report** (`report.py`) renders sections then `_reorder()`s them container-first and renumbers. The block between
`<!-- ANALYST_NOTES_START -->` / `<!-- ANALYST_NOTES_END -->` is preserved across re-renders — it is the only part
written by hand (the analyst pass in `tracking-report`). `render_index` builds the `outputs/AUDIT_INDEX.md` table.

Extending: new vendors / ID patterns / consent selectors go in `signatures.py`; new checks go in `best_practices.py`
(container) or `platforms.py` (platform), using the shared `add(area, check, status, impact, evidence, rec, why)` shape.

## Rules that matter for audit quality

- The audit is a **speed-up for a human analyst, not a replacement**, and we never have account access. Anything that
  needs platform UIs, a test order or an ownership call becomes a discovery question (or an outside-in analyst
  check) in `analyst_checks.py`; never guess, never tell the reader to "check the Google Ads UI".
- Judge every platform by its **deployment route** (`audit.json -> platforms.<P>.sources`): native Shopify app vs
  GTM vs theme vs custom pixel changes what is expected (native Meta app = CAPI built in) and what to recommend.

- **An ecommerce site always runs analytics + ad tracking.** If a capture shows none, the capture failed (missed
  banner, consent-gated GTM, bot wall) — fix it via the Playwright MCP fallback in `tracking-capture`, then `resolve`.
- Geo changes results (banners, store markets, blocked vendors). Run from a **US network**; note the capture location.
- Reports lead with the GTM container and platform scorecards; screenshots are supplemental verification only.
- Shopify context: storefront GTM does not run on checkout/thank-you (Checkout Extensibility) — purchase tracking belongs
  in Customer Events; app-owned GA4 ecommerce is a valid setup, not a GTM failure.
- Verify every P1 against `outputs/<slug>/raw/network.json` / the container JSON before writing Analyst Notes; keep recommendations
  proportionate to a lean DTC brand (don't push sGTM by default).
