# Tracking & Martech Audit — Explore Scientific

**Site:** https://www.explorescientific.ca/  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Shopify Customer Events (app pixels)  
**Consent platform:** Consentmo  

---

## 1. Executive Summary

Tag management: **Shopify Customer Events (app pixels)**. GA4 property: `G-ZQRWE8Y3J6`. Tracking platforms (GA4 + ad pixels) score **94/100** on the events they actually received. The audit raised **0 P1**, **1 P2** and **4 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P2 | Tracking · Meta | Needs attention: Meta — Single deployment route |
| P3 | Consent | 1 tracking script(s) held until consent |
| P3 | Consent | Ad pixels fire on load (no banner shown to this visitor) |
| P3 | Tracking · Meta | Needs attention: Meta — Single Meta pixel |
| P3 | Tracking · Stack | Needs attention: Stack — Third-party request volume |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** native Shopify apps for GA4 and Google Ads (two Ads accounts: AW-499347928 and AW-948911666) and for Meta, plus Criteo through an app pixel. Meta *also* runs from a Shopify custom pixel feeding a second pixel ID, so Meta has two routes.
- **What's working:** tracking 94/100; GA4 and Google Ads are clean and single-source.
- **To clarify:** whether the second Meta pixel (custom pixel) and the second Google Ads account are intentional; Consentmo shows no banner to US visitors (fine for the US, but this is the Canadian store, so Quebec/EU handling matters).
- **Pitch angle:** light-touch — tidy up account sprawl and confirm consent for Canadian traffic. Lowest-risk setup in the batch.
- _Capture: US network, Oct 5 2026, fresh browser, consent accepted → reload → PDP → add to cart → cart. Outside-in only (no account access)._
<!-- ANALYST_NOTES_END -->

---

## 3. Next Steps — Analyst Checks & Discovery Questions

_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks below take minutes from the outside, and the questions are for the discovery conversation._

**Analyst checks (no account access needed)**

- [ ] **Consent:** Visit from an EU/UK VPN: does a banner appear, and do ad pixels wait for consent? — _Browser via EU VPN + DevTools → Network_
- [ ] **Consent:** Check the footer for a 'Your Privacy Choices / Do Not Sell or Share' link (none found on the homepage HTML) — _Site footer, privacy policy_

**Discovery questions for the prospect**

- **Purchase tracking:** Do GA4 revenue and Google Ads / Meta purchase counts reconcile with Shopify orders (a gap above ~10% usually means a tracking problem)?
- **Ownership:** Meta are fed by more than one route (Meta: Shopify app, Shopify custom pixel). Who manages each, and which one is meant to be the source of truth?
- **Meta:** Are all of these Meta pixels still in use (any agency or legacy accounts)? 181579185960224, 197085518345990.
- **Meta:** Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), and what Event Match Quality do Purchase events get?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### No GTM container — Google tag / Shopify app setup review

_No GTM container is deployed, so there is no container to score; these checks review the Google tag and app-based setup instead._

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ✅ | Medium | Google Ads | Enhanced conversions (user-provided data) | User-provided data collection is on. | — |
| ℹ️ | Medium | Measurement | Tag management approach | No GTM container. Tags are deployed via Shopify app pixels (Google & YouTube, Meta (Facebook & Instagram)). | Fine for a lean channel mix. Move to GTM (or a Shopify custom pixel + GTM) once the brand needs custom events, more ad platforms or consent orchestration beyond the apps. |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **94/100** (✅ 21 · ⚠️ 3 · ❌ 0).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 100 | 10 | 0 | 0 | Shopify app: Google & YouTube ×14 | initial: page_view×2, (none)×2; reload: user_engagement×1, page_view×1; pdp: user_engagement×1, page_view×1, view_item×1; atc: add_to_cart×1, page_view×1, shopping_cart×1, view_cart×1, user_engagement×1 |
| Google Ads | 100 | 5 | 0 | 0 | Shopify app: Google & YouTube ×41 | initial: page_view×10; reload: page_view×6; pdp: page_view×6, view_item×4; atc: form_start×3, form_submit×3, add_to_cart×3, page_view×6 |
| Meta | 87 | 6 | 2 | 0 | Shopify custom pixel ×7; Shopify app: Meta (Facebook & Instagram) ×7 | initial: PageView×3; reload: PageView×2; pdp: PageView×2, ViewContent×2; atc: SubscribedButtonClick×1, AddToCart×2, PageView×2 |
| Criteo | — | 0 | 0 | 0 | Shopify native app pixel (sandboxed) ×13 | initial: (request)×4; reload: (request)×3; pdp: (request)×3; atc: (request)×3 |

### GA4 — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single GA4 property | GA4 property: G-ZQRWE8Y3J6. | — |
| ✅ | High | One implementation per property | G-ZQRWE8Y3J6 <- Shopify app: Google & YouTube | — |
| ✅ | High | Page view sent once per load | G-ZQRWE8Y3J6×1 on one page load. | — |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (1×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x14. | — |

### Google Ads — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Google Ads account | Google Ads account: AW-948911666. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 15 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x41. | — |

### Meta — 87/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | Single Meta pixel | 2 Meta pixels receive data: 181579185960224, 197085518345990. | Confirm each is owned and in use; retire leftovers from agencies or old accounts. |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Shopify custom pixel x7; Shopify app: Meta (Facebook & Instagram) x7. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | High | Page view sent once per load | 197085518345990×1, 181579185960224×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (2×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 13 of 13 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |

### Criteo

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ℹ️ | Low | Pixel active | 13 hit(s): (request)×13. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify native app pixel (sandboxed) x13. | — |

### Stack — 50/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Low | Third-party request volume | 1511 third-party requests across the visit (18 identified platforms). | Audit apps/pixels that don't earn their weight. |
| ℹ️ | Low | Session-replay tools | 0: none. | — |
| ℹ️ | Low | Ad platforms in use | 5: Campaign Manager 360 / Floodlight, Criteo, Google Ads, Google Merchant Center, Meta Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Google Tag Settings — `AW-499347928`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Remarketing / conversion page view | {"containerId": "{{Container ID #1}}"} |
| Google Ads destination | {"destinationId": "{{Container ID #1}}", "enableVariablesInDestinationId": false} |

---

### 6.2 Google Tag Settings — `AW-948911666`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-948911666"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Product settings | {"instanceDestinationId": "G-ZQRWE8Y3J6", "isChinaVipRegionMacroResult": 0} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Create-event rules | {"eventName": "shopping_cart", "isCopy": true, "instanceDestinationId": "G-ZQRWE8Y3J6", "precompiledRule": {"new_event_name": "shopping_cart", "merge_source_ev… |
| Create-event rules | {"eventName": "purchase", "isCopy": true, "instanceDestinationId": "G-ZQRWE8Y3J6", "precompiledRule": {"new_event_name": "purchase", "merge_source_event_params… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-948911666"} |
| Create-event rules | {"eventName": "checkout", "isCopy": true, "instanceDestinationId": "G-ZQRWE8Y3J6", "precompiledRule": {"new_event_name": "checkout", "merge_source_event_params… |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-948911666"} |
| Create-event rules | {"eventName": "product", "isCopy": true, "instanceDestinationId": "G-ZQRWE8Y3J6", "precompiledRule": {"new_event_name": "product", "merge_source_event_params":… |
| __ccd_enable_cm | {"instanceDestinationId": "AW-948911666"} |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-ZQRWE8Y3J6"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-ZQRWE8Y3J6"} |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "AW-948911666", "enableVariablesInDestinationId": false} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-ZQRWE8Y3J6", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "AW-948911666"} |
| Google tag configuration | {"trackingId": "G-ZQRWE8Y3J6", "sessionDuration": 0} |

---

### 6.3 Google Tag Settings — `GT-PB66HB5`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| __dest_mc | {"ignoreDupeGtagConfigCalls": true, "destinationId": "MC-JVXJW3N5VF", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "MC-JVXJW3N5VF"} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| Google Ads | `AW-499347928`, `AW-948911666` | network |
| Meta Pixel | `181579185960224`, `197085518345990` | network |
| Google Analytics 4 | `G-ZQRWE8Y3J6` | network |
| Shopify app pixel: unknown app | {"shopId": "273856", "env": "production", "metaData": "[]"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shop": "robert-price.myshopify.com", "collect_url": "https://collect.bogos.io/collect"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"webPixelName": "Judge.me"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"partnerId": "55061", "environment": "prod", "countryCode": "US", "logLevel": "none"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"masterTagID": "68352", "merchantID": "102148", "appPath": "https://daedalus.shareasale.com", "storeID": "102148", "xT… | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `AW-499347928`, `AW-948911666`, `G-ZQRWE8Y3J6` | Shopify web pixel |
| Shopify app pixel: unknown app | {"apiURL": "https://api.omnisend.com", "appURL": "https://app.omnisend.com", "brandID": "5cd9d46e8653ed3e50c968f0", "tr… | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "197085518345990", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |

---

## 8. Ecommerce Tracking

Product page visited: https://explorescientific.ca/products/10-inch-dobsonian-reflector-telescope · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item` | — | ✅ |
| `add_to_cart` | — | ✅ |
| `view_cart` | — | ✅ |
| `begin_checkout` | — | — |
| `purchase` | ✅ | — |

_Checkout and purchase events cannot be observed without placing an order; container configuration is listed instead._

---

## 9. Consent & Privacy

| Check | Result |
|---|---|
| CMP detected | Consentmo |
| Banner action taken by audit | js_api — Shopify Customer Privacy (no visible banner) |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "", "analytics": "", "preferences": "", "sale_of_data": ""} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}} |
| Tracking vendors firing before consent | Awin, Campaign Manager 360 / Floodlight, Criteo, Google Ads, Google Analytics 4, Google Merchant Center, Meta Pixel, ShareASale |
| Scripts held until consent (text/plain, data-consent…) | (inline) [ignore], Shopify CDN [ignore] |
| Banner still visible after accept + reload | no |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-ZQRWE8Y3J6` | initial | page_view×2, (no event name)×2 | `G111` |
| GA4 `G-ZQRWE8Y3J6` | reload | user_engagement×1, page_view×1 | `G111` |
| GA4 `G-ZQRWE8Y3J6` | pdp | user_engagement×1, page_view×1, view_item×1 | `G111` |
| GA4 `G-ZQRWE8Y3J6` | atc | add_to_cart×1, page_view×1, shopping_cart×1, view_cart×1, user_engagement×1 | `G111` |
| Meta `181579185960224` | initial | PageView×2 | — |
| Meta `181579185960224` | reload | PageView×1 | — |
| Meta `181579185960224` | pdp | PageView×1, ViewContent×1 | — |
| Meta `181579185960224` | atc | AddToCart×1, PageView×1 | — |
| Google Ads `AW-948911666` | initial | V_VICMiS7ooCELL8vMQD×5 | — |
| Google Ads `AW-948911666` | reload | V_VICMiS7ooCELL8vMQD×3 | — |
| Google Ads `AW-948911666` | pdp | V_VICMiS7ooCELL8vMQD×3, ff77CM6S7ooCELL8vMQD×3 | — |
| Google Ads `AW-948911666` | atc | form_start×1, form_submit×1, 0meXCNGS7ooCELL8vMQD×3, V_VICMiS7ooCELL8vMQD×3 | — |

**dataLayer pushes observed:**

- `initial`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:AW-948911666, gtag:config:GT-PB66HB5, gtag:config:AW-499347928, gtag:event:page_view, gtm.dom, gtm.load
- `reload`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:AW-948911666, gtag:config:GT-PB66HB5, gtag:config:AW-499347928, gtag:event:page_view, gtm.dom, gtm.load
- `pdp`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:AW-948911666, gtag:config:GT-PB66HB5, gtag:config:AW-499347928, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load
- `atc`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:AW-948911666, gtag:config:GT-PB66HB5, gtag:config:AW-499347928, gtm.dom, gtag:event:page_view, gtag:event:view_cart, gtm.load

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 2204237996 | APP | — | — | {"shopId": "273856", "env": "production", "metaData": "[]"} |
| 1140818092 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"shop": "robert-price.myshopify.com", "collect_url": "https://collect.bogos.io/collect"} |
| 1036386476 | APP | — | ANALYTICS | {"webPixelName": "Judge.me"} |
| 643104940 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"partnerId": "55061", "environment": "prod", "countryCode": "US", "logLevel": "none"} |
| 572850348 | APP | — | ANALYTICS, MARKETING | {"masterTagID": "68352", "merchantID": "102148", "appPath": "https://daedalus.shareasale.com", "storeID": "102148", "xT… |
| 484212908 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"AW-948911666\",\"GT-PB66HB5\",\"AW-499347928\"],\"target_country\":\"US\",\"gtag_even… |
| 256082092 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"apiURL": "https://api.omnisend.com", "appURL": "https://app.omnisend.com", "brandID": "5cd9d46e8653ed3e50c968f0", "tr… |
| 246546604 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "197085518345990", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} |
| 44859564 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 61276332 | CUSTOM | — | MARKETING | — |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `AW-499347928` | GTAG | 1 | 422.8 KB | reload | googletagmanager.com | 4 | 0 | 5 | 3 |
| `AW-948911666` | GTAG | 3 | 572.8 KB | reload | googletagmanager.com | 24 | 0 | 6 | 4 |
| `GT-PB66HB5` | GTAG | 1 | 434.9 KB | reload | googletagmanager.com | 7 | 0 | 4 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `AW-499347928`, `AW-948911666`, `GT-PB66HB5`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google tag (gtag.js) | — | 22 | initial:7, reload:5, pdp:5, atc:5 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-ZQRWE8Y3J6` | 13 | initial:4, reload:2, pdp:2, atc:5 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 3 | initial:2, atc:1 | 0 |
| Criteo | — | 13 | initial:4, reload:3, pdp:3, atc:3 | 0 |
| Google Ads | `AW-499347928`, `AW-948911666` | 41 | initial:10, reload:6, pdp:10, atc:15 | 0 |
| Google Merchant Center | — | 9 | initial:2, reload:2, pdp:2, atc:3 | 0 |
| Meta Pixel | `181579185960224`, `197085518345990` | 31 | initial:8, reload:6, pdp:8, atc:9 | 0 |

### Affiliate / influencer

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Awin | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |
| ShareASale | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Omnisend | — | 5 | initial:2, reload:1, pdp:1, atc:1 | 0 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Judge.me | — | 25 | initial:10, reload:11, pdp:4 | 0 |

### Consent

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Consentmo | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 8 | initial:2, reload:1, pdp:1, atc:4 | 0 |
| Shopify | — | 39 | initial:6, consent:1, reload:5, pdp:10, atc:17 | 0 |
| Shopify Analytics (Monorail) | — | 24 | initial:2, consent:1, reload:3, pdp:3, atc:15 | 0 |
| Shopify CDN | — | 528 | initial:129, reload:129, pdp:175, atc:95 | 0 |

### Payments / BNPL

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| PayPal | — | 7 | atc:7 | 0 |

### Monitoring

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Sentry | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`www.chatbase.co` (317), `review-images.judgeme.com` (34), `d1hcrjcdtouu7e.cloudfront.net` (32), `omnisnippet1.com` (21), `assets.appherolab.com` (12), `analytics.ahrefs.com` (8), `cdn.giveaway.ninja` (8), `www.googletagmanager.com` (7), `forms.soundestlink.com` (6), `fonts.soundestlink.com` (6), `explorescientific.com` (5), `fonts.cdnfonts.com` (5), `cdn.nfcube.com` (4), `cdncozyvideogalleryn.addons.business` (4), `cdn.bogos.io` (4), `backend.chatbase.co` (4), `api.giveaway.ninja` (4), `cdn.robinpro.gallery` (4), `id-shop.govx.com` (4), `extensions.shopifycdn.com` (3)

</details>

---

## 14. Findings & Recommendations

### P2 — Address within 30 days

**[Tracking · Meta] Needs attention: Meta — Single deployment route**  
Hits come from 2 routes: Shopify custom pixel x7; Shopify app: Meta (Facebook & Instagram) x7. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

### P3 — Clean-up / informational

**[Consent] 1 tracking script(s) held until consent**  
Parked as non-executable until the CMP grants consent: Shopify CDN (ignore).  
_Recommendation:_ Positive if intentional; make sure the banner is actually shown to the visitors it applies to, otherwise these tags never fire.

**[Consent] Ad pixels fire on load (no banner shown to this visitor)**  
Consentmo is present but showed no banner to this US visitor; Campaign Manager 360 / Floodlight, Criteo, Google Ads, Google Merchant Center, Meta Pixel fired on load — consistent with a US opt-out model.  
_Recommendation:_ Confirm EU/UK visitors get an opt-in banner and US opt-out (Do Not Sell / GPC) suppresses these pixels.

**[Tracking · Meta] Needs attention: Meta — Single Meta pixel**  
2 Meta pixels receive data: 181579185960224, 197085518345990. Why it matters: Extra IDs split audiences and send customer data to accounts nobody watches.  
_Recommendation:_ Confirm each is owned and in use; retire leftovers from agencies or old accounts.

**[Tracking · Stack] Needs attention: Stack — Third-party request volume**  
1511 third-party requests across the visit (18 identified platforms). Why it matters: Tag weight slows pages, which costs conversion rate.  
_Recommendation:_ Audit apps/pixels that don't earn their weight.

---

## 15. Method & Files

Captured with Playwright (real Chromium, fresh profile) intercepting every request in all frames. Visit: homepage → consent accepted → tab reloaded → first product page → add to cart. GTM containers are captured from the consented reload and decoded from the container's embedded JSON (tags, triggers, variables, templates, permissions) rather than regex scraping.

| File | Contents |
|---|---|
| `containers/<ID>.json` | Decoded container JSON as served (resource, runtime, permissions) |
| `containers/<ID>.js` | Raw container script |
| `containers/GTM-<ID>.export.json` | Reconstructed GTM workspace export (tags, triggers, variables) — names are generated where the container doesn't publish them; custom-template source not included |
| `audit.json` | Full structured analysis behind this report |
| `raw/network.json` | Every intercepted request with phase, status and payload |
| `raw/capture.json` | Visit log, consent result, page snapshots (dataLayer, Shopify, consent state) |

_Limitations: one product page per site, no checkout/purchase; server-side containers are only visible through their client-side traffic. Consent banners and pixels can vary by visitor country; connection-level errors (resets, SSL, ORB) are shown but not treated as site faults, as they often come from the capture network._

## Appendix — Capture Verification

_Supplemental: confirms the capture saw the site as a consenting visitor would._

- Coverage check: ✅ passed
- Consent action: js_api — Shopify Customer Privacy (no visible banner)
- Screenshots: [01_initial](screenshots/01_initial.png) · [02_after_consent](screenshots/02_after_consent.png) · [03_reload](screenshots/03_reload.png) · [04_pdp](screenshots/04_pdp.png) · [05_atc](screenshots/05_atc.png)
