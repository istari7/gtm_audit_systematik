---
name: tracking-capture
description: Capture a site's tracking with Playwright in a persistent browser profile - intercept all network requests, screenshot every phase, detect and accept the consent banner, reload the tab and download the GTM / gtag container JSON, then verify coverage. Step 1 of the tracking-audit skill; also use alone to re-capture a brand or when a site blocks automation (Playwright MCP fallback).
---

# GTM Capture

```
python .claude/skills/tracking-audit/scripts/audit.py capture <brands...> [--parallel 3] [--dwell 5000] [--no-pdp] [--fresh] [--headless]
```

Run from the audits root. Use `run_in_background` for more than a couple of brands and wait for
the notification (~1–2 min per brand, 3 in parallel).

## Persistent browser profile

All captures share one on-disk Chrome profile: `.browser-profile/` in the audits root (gitignored).
Cookies, consent choices and bot-check clearance are kept between brands and between runs, so a
banner accepted once stays accepted. Each brand gets its own tab, and only that tab's traffic
(including its iframes) is recorded.

- First visit to a site: `initial` is a true pre-consent load.
- Later runs: `capture.json → profile.returning_visit = true`. The `initial` phase then reflects
  **stored** consent, and the "fired before consent" rule is skipped.
- Need a real first-visit / pre-consent check again → `--fresh`, which clears that brand's cookies
  and storage before the visit.
- Only one process can use the profile at a time. Don't run two captures in parallel; use `--parallel` instead.
- Headed Chrome by default (falls back to bundled Chromium). It's less likely to be blocked than `--headless`.

## What the script does (per brand)

| Phase | Action | Screenshot |
|---|---|---|
| `initial` | Load the homepage and wait for network idle | `screenshots/01_initial.png` + banner scan |
| `consent` | Accept consent, in order: (1) known CMP selectors in all frames (OneTrust, Cookiebot, Osano, Didomi, Usercentrics, Ketch, CookieYes, Shopify banner, Anowave, Pandectes, Consentmo, Termly, iubenda…); (2) any visible button / link / element whose whole text reads "Accept all / Allow all / I agree / Got it…"; (3) CMP JS APIs (`OneTrust.AllowAll()`, `Shopify.customerPrivacy.setTrackingConsent`, …); (4) **banner scan**: if a fixed/sticky element mentioning cookies/consent/privacy was on screen and nothing above matched, click the most "accept"-like control inside it | `02_after_consent.png` + banner scan |
| `reload` | **Reload the tab** with consent granted, scroll and dwell. Containers are captured here | `03_reload.png` + banner scan |
| `pdp` | Most-linked product page (skips gift cards, add-ons, protection plans) | `04_pdp.png` |
| `atc` | Click add to cart | `05_atc.png` |

A container is captured from any script response that contains GTM's `var data = {"resource": …}`
literal. That covers first-party, sGTM and Shopify-app loaders as well as `googletagmanager.com`.
The post-consent copy is kept. A `GTM-` ID that is referenced but never loaded is fetched directly
and marked `direct_fetch`.

### Coverage check (automatic → `capture.json → review`)

**Rule: an ecommerce site does not run without analytics and ad tracking.** If none is seen, the
capture failed, not the site. A brand gets `review.needs_review = true` when any of these hold:

- the bot challenge did not clear, or fewer than 80 requests were captured
- no analytics requests after consent
- no advertising pixels after consent on an ecommerce site
- a cookie/consent banner is still visible after accept + reload
- a GTM container is referenced but never loaded in the browser (consent-gated or broken)

## Verify every brand (mandatory, do not skip)

1. Print the status of all brands:
   ```
   python -c "import json,glob; [print(f.split('\\')[0].split('/')[0], c.get('consent',{}).get('method'), c.get('consent',{}).get('detail'), [x['id'] for x in c['containers']], c.get('review',{}).get('reasons')) for f in glob.glob('*/raw/capture.json') for c in [json.load(open(f,encoding='utf-8'))]]"
   ```
2. **Look at the screenshots** with the Read tool for every brand: at least `01_initial.png` and
   `03_reload.png`, and `02_after_consent.png` whenever the consent method is not `selector` or
   `button_text`. Check:
   - Is a cookie/consent banner, region popup or "are you human" wall visible in 01? Was it gone
     in 03? If it was still there, consent was missed.
   - Did an email/SMS popup or age gate cover the page? Popups don't block tracking, but age gates do.
   - Does 01 show the real site, not a block page, a blank page or a different country store?
3. Act on what you find:

| Situation | Action |
|---|---|
| Banner visible in 03, or `review` says no analytics / no ads | Playwright MCP fallback below, accepting manually. Also add the banner's accept selector to `CONSENT_SELECTORS` in `scripts/tracking_audit/signatures.py` so the next run catches it |
| Bot wall / block page in 01 | MCP fallback; ask the user to solve the challenge in the opened window if needed |
| Flag is a false positive (e.g. tracking proven to run only server-side / via the sGTM endpoint) | `audit.py resolve <slug> --note "<evidence>"` |
| GTM ID in HTML but no container | `audit.py fetch GTM-XXXX --brand <slug>` |
| No PDP / no `/cart/add` request in `atc` on an ecommerce site | Note in Analyst Notes that the ecommerce checks are incomplete |

Consent outcomes: `selector` / `button_text` / `banner_scan` mean a banner was clicked. `js_api … (no visible banner)`
means a CMP is loaded but showed no banner to a US visitor (confirm with screenshot 01). `null` means no CMP was found.

## Playwright MCP fallback (bot walls, banners the script missed)

Use the `mcp__plugin_playwright_playwright__*` tools (load them with ToolSearch first).

1. `browser_navigate` to the brand URL. `browser_take_screenshot` → save to `outputs/<slug>/screenshots/mcp_01_initial.png`.
2. `browser_snapshot` → find the banner's accept control → `browser_click`. Note how you did it,
   for example "Anowave 'Allow all' link".
3. `browser_network_requests` → save the output to a temp file `<slug>_reqs.txt`.
4. **Reload the tab**: `browser_navigate` to the same URL again, wait ~8 s, press End to scroll,
   then `browser_take_screenshot` → `outputs/<slug>/screenshots/mcp_03_reload.png`. Confirm the banner is gone.
5. `browser_network_requests` → append a line `--- reload ---`, then the output, to the same file.
6. `browser_evaluate` with the function in `.claude/skills/tracking-audit/scripts/snapshot.js` (paste
   its contents) → save the JSON result to `<slug>_snap.json`.
7. Ingest, download the containers and mark the brand resolved:
   ```
   python .claude/skills/tracking-audit/scripts/audit.py ingest <url> --brand <slug> --requests <slug>_reqs.txt --consent "<how>" --snapshot <slug>_snap.json
   python .claude/skills/tracking-audit/scripts/audit.py fetch GTM-XXXX --brand <slug>
   python .claude/skills/tracking-audit/scripts/audit.py resolve <slug> --note "MCP re-capture: <how consent was accepted>"
   ```
   Take container IDs from `gtm.js?id=` / `gtag/js?id=` requests or the snapshot's `google_tag_manager_keys`.
8. `browser_close`, then run tracking-parse for that brand.

MCP-ingested captures have no POST bodies, so GA4 event names and `gcs` come only from URLs. Say
so in the Analyst Notes.
