# Tracking & Martech Audit System

A fast, outside-in audit of a website's tracking setup — Google Tag Manager, GA4, Google Ads, Meta, TikTok,
Pinterest, Microsoft Ads, Klaviyo and consent — built for **prospecting**: it needs no access to the brand's
accounts. It drives a real browser through the site, records every tracking request, works out *which
integration sent it*, decodes the GTM container, and writes a client-ready report per brand with scorecards,
findings, analyst checks and discovery questions.

It is a first pass that speeds up the analyst, not a replacement: anything that needs account access or a
judgement call is handed over as a checklist item or a question for the prospect.

## Requirements

- Python 3.11+ and Playwright: `pip install playwright` then `playwright install chromium`
  (Google Chrome is used when installed — it is less likely to be bot-blocked).
- Windows, macOS or Linux. Run from a **US network** unless you are deliberately auditing another region —
  consent banners, store markets and blocked vendors change with the visitor's country.
- Optional: [Claude Code](https://claude.com/claude-code) to run the whole process through the bundled skills.

## Run an audit

**With Claude Code** — ask for it in plain words or use the skill:

```
/tracking-audit https://brand-one.com brand-two.com
```

The `tracking-audit` skill runs capture → parse → report, verifies each capture, falls back to a manual
browser session for bot-protected sites, and writes the analyst notes.

**From the command line** (run from the repo root):

```
# full pipeline for the brands listed in brands.txt (one URL per line, or slug=url)
python .claude/skills/tracking-audit/scripts/audit.py run --fresh

# or name brands directly
python .claude/skills/tracking-audit/scripts/audit.py run brand-one.com https://www.brand-two.com --fresh
```

| Command | What it does |
|---|---|
| `run [brands]` | capture + parse + report + index |
| `capture [brands]` | browser visit only (writes `raw/`, `containers/`, `screenshots/`) |
| `parse [brands]` | rebuild `audit.json` from the capture (no new visit) |
| `report [brands]` | re-render `outputs/<brand>/README.md` (keeps the Analyst Notes block) |
| `index` | rebuild `outputs/AUDIT_INDEX.md`, the summary table of all audited brands |
| `fetch GTM-XXXX --brand <slug>` | download a container directly (also `G-`, `AW-` IDs) |
| `ingest <url> --brand <slug> --requests reqs.txt` | import a manual Playwright-MCP session (bot-wall fallback) |
| `resolve <slug> --note "..."` | mark a flagged capture as manually verified |

Useful flags: `--fresh` (clear the brand's cookies/consent in the shared browser profile for a true first
visit), `--parallel 3`, `--no-pdp` (skip product page + add to cart), `--headless`, `--dwell 5000`.

Every command writes to `outputs/<slug>/`; pass `--out <dir>` to use another root (e.g. `--out examples` to
re-render the sample audits). A batch of ~10 brands takes about 15 minutes. After changing scoring rules, re-run only `parse` and `report`.

## What happens during a capture

One persistent Chrome profile (`.browser-profile/`, never committed) visits each site in phases, tagging every
request with the phase it fired in:

1. **initial** — homepage, before any consent interaction
2. **consent** — accepts the banner (known CMP buttons → "Accept all" text → CMP APIs → banner scan)
3. **reload** — reloads with consent granted; GTM / Google-tag containers are captured here
4. **pdp** — most-linked product page
5. **atc** — add to cart, then the cart page (flushes delayed pixel hits)

Alongside the requests it records the Chrome **initiator chain** (which script loaded which), screenshots
per phase, dataLayer / Shopify / consent snapshots, and first-party cookie *names*.

## What the report covers

| Section | Source |
|---|---|
| **GTM container audit** — configuration vs best practice, scored and weighted by business impact | Decoded container JSON |
| **Tracking platform audit** — GA4, Google Ads, Meta, TikTok, Pinterest, Microsoft Ads, Klaviyo: duplicates, missing ecommerce events, product / value / currency, CAPI event_id, enhanced conversions, consent signals, first-party cookies | Hits each platform received |
| **Deployed via** — which route sent each platform's hits: native Shopify app, custom pixel, GTM (and what loaded it), app embed / proxy, theme code | Hit markers, pixel sandbox frames, initiator chain |
| **Next steps** — analyst checks doable without access + discovery questions for the prospect | Generated from all of the above |
| Container inventory, reconstructed GTM export, consent, event flow, platform inventory, findings P1–P3 | — |

On Shopify the same platform is often fed by several routes (e.g. the Google & YouTube app *and* GTM *and* a
custom pixel). The audit judges each platform against its actual route — a native app integration already
includes server-side events and Shopify consent handling, a GTM or theme copy alongside it usually means
double counting.

## Output per brand

```
outputs/<slug>/
  README.md                         the report (Analyst Notes block is preserved on re-render)
  audit.json                        structured analysis behind the report
  containers/<ID>.json / .js        decoded + raw GTM / Google-tag containers
  containers/GTM-<ID>.export.json   reconstructed GTM workspace export (generated names)
  raw/network.json                  every request: phase, url, status, POST body
  raw/initiators.json               Chrome initiator chain per request
  raw/capture.json                  visit log, consent result, snapshots, cookie names
  screenshots/                      01_initial … 05_atc (capture verification)
```

`outputs/AUDIT_INDEX.md` lists every audited brand with its scores and top issue.

`examples/` holds finished sample audits of 11 Shopify brands (October 2026) in the same layout, with
their own `AUDIT_INDEX.md` and `brands.txt`.

## Limitations

- One product page and one add-to-cart per site; checkout and purchase are never observed (no test orders).
- Server-side containers are only visible through their client-side traffic; GTM workspace drafts, ad-account
  settings and platform UIs are out of reach — those become discovery questions.
- Some stores block automated add-to-cart or the whole visit; use the manual fallback (`tracking-capture`
  skill) and say so in the notes.

## Extending

New vendors, ID patterns and consent selectors go in `signatures.py`; container checks in `best_practices.py`;
platform checks in `platforms.py`; deployment attribution in `sources.py`; analyst checks / discovery questions
in `analyst_checks.py`. See `CLAUDE.md` for the architecture.
