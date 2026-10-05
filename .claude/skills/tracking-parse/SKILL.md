---
name: tracking-parse
description: Decode captured GTM / gtag containers (embedded JSON - tags, triggers, variables, custom templates, hard-coded IDs, consent settings), score the container vs best practice, evaluate GA4 / Google Ads / Meta / TikTok / Pinterest / Microsoft Ads / Klaviyo from the hits they received, and write outputs/<brand>/audit.json with findings. Step 2 of the tracking-audit skill; also use to answer questions about what a container does.
---

# GTM Parse

```
python .claude/skills/tracking-audit/scripts/audit.py parse <brands...>
```

Needs `outputs/<slug>/containers/*.json` and `outputs/<slug>/raw/` from tracking-capture. Writes `outputs/<slug>/audit.json`.
Safe to re-run any time (e.g. after editing rules in `scripts/tracking_audit/findings.py`).

## How containers are decoded (no regex scraping)

`gtm.js` embeds its configuration as a JSON literal `var data = {...}`, saved verbatim as
`containers/<ID>.json`:

| Key | Meaning |
|---|---|
| `resource.tags[]` | Tags. `function` = type (`__html`, `__gaawe`, `__awct`, `__cvt_<id>` template, `__paused` + `vtp_originalTagType`), `vtp_*` = settings, `consent` = extra consent checks, `metadata` may hold the tag name |
| `resource.macros[]` | Variables (`__v` dataLayer, `__jsm` custom JS, `__c` constant, `__u` URL, `__k` cookie, `__smm` lookup …) |
| `resource.predicates[]` | Conditions: `{function: _eq/_cn/_re/_sw/_css…, arg0: ["macro", i], arg1}` |
| `resource.rules[]` | Triggers: `[["if", p…], ["unless", p…], ["add", tag…], ["block", tag…]]` |
| `permissions` | Per custom template: injected script URLs, globals, cookies, consent access → vendor inference |
| `blob["10"]` / `blob["1"]` | Container ID / version |

Values are encoded (`["macro", i]`, `["template", …]`, `["map", k, v…]`, `["list", …]`, `["escape", v…]`);
`container.Decoder.value()` resolves them, inlining constant variables so IDs behind `{{Constant}}`
variables are recovered. Listener "tags" (`__cl`, `__lcl`, `__hl`, `__sdl`, `__evl`, `__tg`…)
are reported as trigger plumbing, not tags. gtag.js containers (`G-`, `AW-`, `GT-`) are summarised
as Google-tag features (enhanced measurement, Signals, user-provided data, regional settings…).

## Reconstructed container (`containers/GTM-<ID>.export.json`)

`reconstruct.py` rebuilds a GTM workspace export (`exportFormatVersion: 2`) from the published
container. One trigger is created per distinct compiled rule. Its type comes from the event
condition (`gtm.js` → Page View, `gtm.click` → All Elements Click, `gtm.linkClick` → Link Click,
anything else → Custom Event), and the remaining conditions become filters. Tags carry their
parameters, firing and blocking triggers, paused state, priority, firing option, consent settings
and setup/teardown. Variables are rebuilt and built-ins are restored by name (`{{Event}}`,
`{{Page Path}}`, `{{Click Classes}}` …).

Not recoverable from a published container: real names (unless the container publishes them),
folders, notes, and custom-template source. Generated names look like `GA4 Event - add_to_cart #40`.
Use the export to read or diff a container. It can be imported into a scratch workspace once any
custom templates are added, but it is not a backup of the original.

To regenerate it alone, re-run `parse`.

## Best-practice evaluation (`best_practices.py`) — the core of the audit

Each GTM container is scored (impact-weighted, warnings count half) on:

| Area | Checks |
|---|---|
| Measurement | single GA4 Google tag; GA4 sent from one source only (not GTM + Shopify app); Google tag on Initialization / All Pages; measurement ID in a variable |
| Ecommerce | funnel coverage (ownership-aware: Shopify app vs GTM, split ownership); items[] on ecommerce events; purchase transaction_id/value/currency; custom names shadowing standard events; DOM scraping vs dataLayer; no purchase tags tied to Shopify thank-you/checkout URLs (Checkout Extensibility) |
| Google Ads | conversion linker; purchase conversion value/currency/order ID; enhanced conversions; single account; dynamic remarketing |
| Paid social | pixels via templates vs Custom HTML; Meta event_id for CAPI dedupe; single Meta source |
| Consent | Consent Mode defaults (in GTM or via gtag before GTM); marketing tags require ad_storage |
| Deployment | GTM in a Shopify custom pixel: no DOM listeners, page_location overridden |
| Governance / performance | paused / orphan / duplicate tags; Custom HTML share and unsafe patterns; unused variables; Custom JS count; UA leftovers; always-on tag count |

Business context is applied: Shopify brands are expected to track purchase via Customer Events;
app-owned GA4 ecommerce is valid (not a GTM failure); sGTM / dynamic remarketing are suggestions.
Failed / warning checks also become P1–P3 findings. Brands without GTM get a Google-tag / app review
and no score.

## Deployment attribution (`sources.py`)

Every platform hit gets a `source`, the route that sent it: `Shopify app: <app>` (native integration), `Shopify custom
pixel #<id>`, `GTM GTM-XXXX (loaded by ...)`, `Shopify app embed / proxy: <handle>`, `Theme inline script / Theme HTML`.
Order: hit markers (Meta `a=shopify_web_pixel|shopify_custom_pixel`, TikTok `"partner":"Shopify"`, Pinterest
`np=shopify-web-pixel`) -> custom-pixel frame URL -> ranked labels on the hit's own CDP stack (GTM > Web Pixels Manager
> app proxy > app embed > theme; fetch-wrapper app embeds lose) -> the loader of the platform's library
(`gtag/js?id=<ID>`, `signals/config/<pixel>` / `fbevents.js`, `events.js?sdkid=`, `bat.js`, `core.js`, `klaviyo.js`)
-> no initiator record on Shopify = native app pixel in a sandboxed worker. `platforms.<P>.sources` holds counts;
`significant_routes` (>=4 hits and >=15%) decides multi-route warnings.

## Tracking platform audit (`platforms.py`)

`Hits` normalises every platform hit in `raw/network.json` into `{phase, event, id, params}` (GA4
`/g/collect` lines incl. `pr1`/`cu`/`epn.value`/`gcs`/`dl`; Meta `/tr` incl. `eid`, `cd[...]`, `ud[...]`;
TikTok JSON bodies; Pinterest `ed`/`pd`; UET `ea`/`evt`/`prodid`/`asc`; Google Ads conversion / rmkt
`data=` + `em`; Klaviyo client events). `PlatformChecks` then scores per platform:

| Platform | Checks |
|---|---|
| GA4 | single property; one implementation per property (page vs Shopify custom pixel); page_view once per load; real page_location; view_item / add_to_cart sent with items+value+currency; Consent Mode `gcs`; engagement events; `_ga` cookie |
| Google Ads | single account; enhanced conversions; product IDs for dynamic remarketing; add-to-cart signal; `_gcl_au` |
| Meta | single pixel; PageView once per load; ViewContent / AddToCart with content_ids+value+currency; event_id on standard events (CAPI dedupe); advanced matching; `_fbp` |
| TikTok / Pinterest / Microsoft Ads | single ID; page view once; product view / add to cart with params; event_id (TikTok); product IDs + consent `asc` (UET); first-party cookies |
| Klaviyo | onsite.js; Viewed Product (info only — anonymous visitors aren't tracked) |
| Others / Stack | Snapchat, Reddit, X, AppLovin, Criteo, TTD activity; session-replay tool count; third-party request volume |

Ecommerce checks only apply when a PDP was visited / the cart add happened (redirect cart adds → "verify",
not fail). Failed / warning checks become findings prefixed `Tracking · <platform>`. `audit.json → platforms`
holds per-platform `checks`, `score`, `events_by_phase` and `_overall`.

## Network analysis

`raw/network.json` → vendors by category (+ IDs, request count per phase, failures), GA4 hits
(POST bodies split per event: `en`, `gcs`, page_view counts per phase), Meta / TikTok / Google
Ads events, sGTM / first-party endpoints, CMP detection, tracking that fired before consent,
Shopify web-pixel config (`webPixelsConfigList` hard-coded in the HTML), IDs hard-coded in HTML.

## Findings rules (`findings.py`)

P1: bot-blocked capture, no CMP while ad pixels fire, consent accepted but gcs still denied,
duplicate GA4 page_view / Meta PageView per load, no GA4, malformed Ads conversion ID,
`view_item` / `add_to_cart` missing on PDP / ATC. P2: ad pixels before consent (with CMP), no
Consent Mode, multiple GA4 properties / Meta pixels / GTM containers, UA still deployed,
failing vendor requests, heavy Custom HTML, >150 tags, same GA4 property in Shopify app + GTM.
P3: paused / orphan tags, large container, GA4 outside GTM, sGTM detected, no consent config in GTM.

To add a vendor, edit `VENDORS` / `ID_PATTERNS` in `signatures.py`; to add a rule, add an `add(...)`
in `build_findings`. Re-run parse + report.

## Answering questions about a container

```
python -c "import json; a=json.load(open('outputs/<slug>/audit.json',encoding='utf-8')); c=a['containers'][0]; [print(t['type'], t['name'] or t['tag_id'], t['ids'] or t.get('ga4_event'), '|', t['fires_on'][:1]) for t in c['tags'] if not t['paused']]"
```

Useful fields per container in `audit.json`: `counts`, `tag_types`, `tags[]` (fires_on, blocked_by,
events, consent_required, ids, orphan), `custom_html[]` (vendors, html_ids, risk, preview),
`templates[]` (vendor, injects), `variables[]`, `events.custom`, `ga4_events`, `measurement`,
`consent`, `gtag_features`.
