# Tracking & Martech Audit — Camera Ready Cosmetics

**Site:** https://camerareadycosmetics.com  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Google Tag Manager (GTM-KFDVZH)  
**Consent platform:** Consent banner (CMP not identified)  

---

## 1. Executive Summary

Tag management: **Google Tag Manager (GTM-KFDVZH)**. GA4 properties: `G-238B3Z6CBM`, `G-5E5T774K31`, `G-TJRR5S4PVS`. Container `GTM-KFDVZH` scores **90/100** against best practice (0 failed, 4 warning checks). Tracking platforms (GA4 + ad pixels) score **89/100** on the events they actually received. The audit raised **2 P1**, **4 P2** and **5 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P1 | Tracking · GA4 | Not met: GA4 — One implementation per property |
| P1 | Tracking · GA4 | Not met: GA4 — Page view sent once per load |
| P2 | Consent | Ad pixels fire before the visible consent banner is answered |
| P2 | Analytics | Universal Analytics still deployed |
| P2 | GTM · Ecommerce | Needs attention: GA4 ecommerce funnel coverage — GTM-KFDVZH |
| P2 | Tracking · GA4 | Needs attention: GA4 — Single deployment route |
| P3 | GTM · Measurement | Needs attention: Measurement ID in a variable, not hard-coded — GTM-KFDVZH |
| P3 | GTM · Governance | Needs attention: No unused variables — GTM-KFDVZH |
| P3 | Tracking · GA4 | Needs attention: GA4 — Single GA4 property |
| P3 | Tracking · Microsoft Ads | Needs attention: Microsoft Ads — Product IDs for dynamic remarketing |
| P3 | Tracking · Stack | Needs attention: Stack — Third-party request volume |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** the ad platforms all run through **native Shopify apps** (Google & YouTube, Facebook & Instagram, TikTok, Pinterest). GA4 is the outlier: G-TJRR5S4PVS is fed by the Google app **and** custom pixel #94732473, while GTM-KFDVZH (score 90) sends Analyzify-driven ecommerce to a third property, G-5E5T774K31.
- **Biggest issue — GA4 data trust:** three properties, two double-counting page views on every load. Reporting depends on which property someone opens.
- **Also:** five active Universal Analytics tags in GTM (dead since July 2024); a consent banner is shown, but ad pixels fire before it's answered; Microsoft UET (loaded through the consent app's embed) sends no product IDs.
- **Pitch angle:** "one source of truth for GA4" — consolidate to one property and route, delete UA, and make the banner actually gate pixels (or switch to a US opt-out notice).
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
- **Ownership:** GA4 are fed by more than one route (GA4: Shopify app, Shopify custom pixel). Who manages each, and which one is meant to be the source of truth?
- **GA4:** Are all of these GA4 properties still in use (any agency or legacy accounts)? G-238B3Z6CBM, G-5E5T774K31, G-TJRR5S4PVS.
- **Meta:** Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), and what Event Match Quality do Purchase events get?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### `GTM-KFDVZH` — score 90/100 (✅ 12 · ⚠️ 4 · ❌ 0)

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ⚠️ | High | Ecommerce | GA4 ecommerce funnel coverage | Configured in GTM: add_to_cart, purchase, view_item. Missing core: begin_checkout; missing recommended: view_item_list, select_item, view_cart, remove_from_cart, add_shipping_info, add_payment_info. | Add the missing funnel events with items[] from the dataLayer. |
| ⚠️ | Low | Measurement | Measurement ID in a variable, not hard-coded | 4 of 4 GA4 event tags hard-code the measurement ID. | Reference a Constant / Lookup Table variable so the ID changes in one place. |
| ⚠️ | Low | Governance | No unused variables | 19 variable(s) not referenced by any tag, trigger or variable: DLV - productName, DLV - productId, DLV - productBrand, DLV - productCategory, DLV - productVariantTitle, DLV - productPrice, DLV - productQuantity, DLV - p… | Remove unused variables. |
| ⚠️ | Low | Governance | Universal Analytics removed | 5 UA tag(s) (5 active); UA IDs UA-2180997-3. | Delete UA tags, GA Settings variables and UA triggers. |
| ✅ | High | Measurement | GA4 sent from one source only | No GA4 property is shared between GTM and a Shopify app. | — |
| ✅ | High | Ecommerce | Ecommerce events carry items[] | All ecommerce event tags send items (dataLayer ecommerce object or items parameter). | — |
| ✅ | High | Ecommerce | Purchase has transaction_id, value, currency | purchase tag #66 sends transaction_id / value / currency. | — |
| ✅ | High | Consent | Consent Mode defaults set before tags fire | Consent Mode default is set via gtag outside GTM (theme / CMP / Shopify app) before the container loads. | — |
| ✅ | Medium | Measurement | Single GA4 Google tag | GA4 Google tag IDs: G-5E5T774K31. | — |
| ✅ | Medium | Measurement | Google tag fires on Initialization / All Pages | Google tag fires on Initialization or Page View. | — |
| ✅ | Medium | Governance | Limited Custom HTML | 0 active Custom HTML tag(s) (0% of active tags). | — |
| ✅ | Medium | Performance | Tags firing on every page kept small | 2 tag(s) fire on every page load without filters; container 498.1 KB. | — |
| ✅ | Low | Governance | Paused tags cleaned up | 1 paused tag(s). | — |
| ✅ | Low | Governance | No orphan tags | 0 active tag(s) without a firing trigger. | — |
| ✅ | Low | Governance | Custom JavaScript variables kept lean | 0 Custom JavaScript variable(s). | — |
| ✅ | Low | Governance | No duplicate tags | No identical tags. | — |
| ℹ️ | Low | Governance | Tag names published (naming convention auditable) | Tag names are not published in the container (normal); naming convention can't be audited from outside. | — |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **89/100** (✅ 36 · ⚠️ 4 · ❌ 2).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 66 | 7 | 2 | 2 | Shopify app: Google & YouTube ×49; Shopify custom pixel #94732473 ×14 | initial: page_view×4, (none)×3, scroll×1; reload: user_engagement×6, page_view×5, scroll×4; pdp: user_engagement×6, view_item×3, page_view×4, product_page_view_sessions×2, scroll×3; atc: add_to_cart×3, scroll×5, user_engagement×6, page_view×4, view_cart×2, in… |
| Google Ads | 100 | 5 | 0 | 0 | Shopify app: Google & YouTube ×67 | initial: page_view×7, gtag.config×6; reload: page_view×6, gtag.config×3; pdp: page_view×7, view_item×4, gtag.config×6; atc: form_start×3, form_submit×3, page_view×12, add_to_cart×4, gtag.config×6 |
| Meta | 100 | 7 | 0 | 0 | Shopify app: Meta (Facebook & Instagram) ×10 | initial: PageView×2; reload: PageView×1; pdp: PageView×2, ViewContent×2; atc: SubscribedButtonClick×1, AddToCart×1, PageView×1 |
| TikTok | 100 | 7 | 0 | 0 | Shopify app: TikTok ×6 | initial: Pageview×1; reload: Pageview×1; pdp: Pageview×1, ViewContent×1; atc: AddToCart×1, Pageview×1 |
| Pinterest | 100 | 6 | 0 | 0 | Shopify app: Pinterest ×11 | initial: PageVisit×2, init×1; reload: init×1, PageVisit×1; pdp: init×1, PageVisit×2; atc: AddToCart×1, init×1, PageVisit×1 |
| Microsoft Ads | 94 | 4 | 1 | 0 | Shopify app embed: gdpr-cookie-consent ×4 | reload: ?×1, pageLoad×1; atc: ?×1, pageLoad×1 |

### GA4 — 66/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ❌ | High | One implementation per property | G-TJRR5S4PVS <- Shopify app: Google & YouTube x15, Shopify custom pixel #94732473 x14 | Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM carries a richer setup (then switch GA4 off in the app). |
| ❌ | High | Page view sent once per load | Duplicates on one page load: G-238B3Z6CBM×2 (from Shopify app: Google & YouTube); G-TJRR5S4PVS×2 (from Shopify app: Google & YouTube, Shopify custom pixel #94732473) | Remove the second source (app vs GTM vs hard-coded / custom pixel). |
| ⚠️ | Medium | Single GA4 property | 3 GA4 propertys receive data: G-238B3Z6CBM, G-5E5T774K31, G-TJRR5S4PVS. | Confirm each is owned and in use; retire leftovers from agencies or old accounts. |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Shopify app: Google & YouTube x49; Shopify custom pixel #94732473 x14. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (3×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (3×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: scroll, user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |

### Google Ads — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Google Ads account | Google Ads account: AW-1070638518. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 28 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x67. | — |

### Meta — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Meta pixel | Meta pixel: 1256977304325263. | — |
| ✅ | High | Page view sent once per load | 1256977304325263×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 9 of 9 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Meta (Facebook & Instagram) x10. | — |

### TikTok — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single TikTok pixel | TikTok pixel: CHM4OTRC77U2H86LKPL0. | — |
| ✅ | High | Page view sent once per load | CHM4OTRC77U2H86LKPL0×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | event_id for Events API dedupe | event_id present. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ttp. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: TikTok x6. | — |

### Pinterest — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Pinterest tag | Pinterest tag: 2616682135507. | — |
| ✅ | High | Page view sent once per load | 2616682135507×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | PageVisit sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _pin_unauth. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Pinterest x11. | — |

### Microsoft Ads — 94/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Low | Product IDs for dynamic remarketing | No product IDs on UET hits from product pages. | Send ecomm_prodid + ecomm_pagetype (Shopping / dynamic remarketing). |
| ✅ | Low | Single UET tag | UET tag: 20018977. | — |
| ✅ | High | Page view sent once per load | 20018977×1 on one page load. | — |
| ✅ | Low | UET Consent Mode signal | asc=G. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _uetsid, _uetvid. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app embed: gdpr-cookie-consent x4. | — |

### Stack — 50/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Low | Third-party request volume | 1374 third-party requests across the visit (22 identified platforms). | Audit apps/pixels that don't earn their weight. |
| ℹ️ | Low | Session-replay tools | 0: none. | — |
| ℹ️ | Low | Ad platforms in use | 7: Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Container Deep Dive — `GTM-KFDVZH`

| Tag type | Active | Paused |
|---|---|---|
| Universal Analytics | 5 | 0 |
| GA4 Event | 4 | 0 |
| Google Tag (GA4/Ads config) | 1 | 1 |
| Conversion Linker | 1 | 0 |

<details><summary>All active tags with firing conditions</summary>

| Tag | Type | IDs / event | Fires on | Consent |
|---|---|---|---|---|
| #6 | Universal Analytics | {} | {{DLV - gtm.elementClasses}} contains "banner_image" AND {{Event}} equals "gtm.click" | — |
| #7 | Universal Analytics | {} | {{Event}} equals "gtm.click" AND {{DLV - gtm.elementId}} contains "slap" | — |
| #8 | Universal Analytics | {} | {{Event}} equals "gtm.linkClick" AND {{DLV - gtm.triggers}} matches regex "(^$\|((^\|,)2563652_9($\|,)))" | — |
| #43 | Universal Analytics | {"trackingId": "UA-2180997-3"} | {{Event}} equals "gtm.load" AND NOT({{Undefined Value #8}} equals "false") | — |
| #47 | Universal Analytics | {"trackingId": "UA-2180997-3"} | {{Event}} equals "gtm.click" AND {{DLV - gtm.elementClasses}} matches regex "add bold_clone\|fa fa\\-shopping\\-cart" | — |
| #49 | Conversion Linker | {} | {{Event}} equals "gtm.js" | — |
| #63 | Google Tag (GA4/Ads config) | {"tagId": "G-5E5T774K31"} | {{Event}} equals "gtm.js" | — |
| #64 | GA4 Event | view_item | {{Event}} equals "analyzify_productDetail" | — |
| #66 | GA4 Event | purchase | {{Event}} equals "analyzify_purchase" | — |
| #137 | GA4 Event | add_to_cart | {{Event}} equals "add_to_cart" | — |
| #143 | GA4 Event | alt_product_addtocart | {{Event}} equals "gtm.click" AND {{DLV - gtm.elementClasses}} contains "refer_addtocart" | — |

</details>

**Reconstructed export:** `containers/GTM-KFDVZH.export.json` — 12 tags, 10 triggers, 44 variables

**Custom dataLayer events used as triggers (3):** `add_to_cart`, `analyzify_productDetail`, `analyzify_purchase`

**Auto-event listeners:** Click (all elements), Click (just links)

---

### 6.2 Google Tag Settings — `AW-1070638518`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-1070638518"} |
| User-provided data collection (enhanced conversions) | {"lastNameValue": "Shopify.checkout.billing_address.last_name", "phoneValue": "Shopify.checkout.phone", "autoPhoneEnabled": true, "manualEmailEnabled": true, "… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-1070638518"} |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-1070638518"} |
| __ccd_enable_cm | {"instanceDestinationId": "AW-1070638518"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":2,\"args\":[{\"booleanExpressio… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "AW-1070638518", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "AW-1070638518"} |

---

### 6.3 Google Tag Settings — `G-238B3Z6CBM`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Internal traffic rules | {"instanceOrder": 0, "paramValue": "internal", "ruleResult": false} |
| Unwanted referrals list | {"includeConditions": ["checkout\\.shopify\\.com", "camerareadycosmetics\\.com", "paypal\\.com", "shop\\.app", "klarna\\.com", "klarnapayments\\.com"]} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Product settings | {"instanceDestinationId": "G-238B3Z6CBM", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-238B3Z6CBM"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced conversions settings | {"instanceDestinationId": "G-238B3Z6CBM"} |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-238B3Z6CBM"} |
| Enhanced measurement: form interactions | {"includeParams": true, "instanceDestinationId": "G-238B3Z6CBM"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-238B3Z6CBM"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-238B3Z6CBM"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-238B3Z6CBM"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-238B3Z6CBM"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-238B3Z6CBM"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| User-provided data attached to hits | {"acceptAutomatic": false, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":3,\"args\":[{\"booleanExpressi… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-238B3Z6CBM"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-238B3Z6CBM"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-238B3Z6CBM", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-238B3Z6CBM", "sessionDuration": 0} |

---

### 6.4 Google Tag Settings — `G-5E5T774K31`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Unwanted referrals list | {"includeConditions": ["checkout\\.shopify\\.com", "checkout\\.myshopify\\.com", "camera\\-ready\\-cosmetics\\.myshopify\\.com", "camerareadycosmetics\\.com", … |
| Internal traffic rules | {"instanceOrder": 0, "paramValue": "internal", "ruleResult": false} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Product settings | {"instanceDestinationId": "G-5E5T774K31", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-5E5T774K31"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced conversions settings | {"instanceDestinationId": "G-5E5T774K31"} |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-5E5T774K31"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-5E5T774K31"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-5E5T774K31"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-5E5T774K31"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-5E5T774K31"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-5E5T774K31"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| User-provided data attached to hits | {"acceptAutomatic": false, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":3,\"args\":[{\"booleanExpressi… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-5E5T774K31"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-5E5T774K31"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-5E5T774K31", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-5E5T774K31", "sessionDuration": 0} |

---

### 6.5 Google Tag Settings — `G-TJRR5S4PVS`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| __ogt_ga_send | {"value": false} |
| Internal traffic rules | {"instanceOrder": 0, "paramValue": "internal", "ruleResult": false} |
| Unwanted referrals list | {"includeConditions": ["myshopify\\.com", "camerareadycosmetics\\.com", "paypal\\.com", "camera\\-ready\\-cosmetics\\.myshopify\\.com", "checkout\\.myshopify\\… |
| Custom session timeout | {"sessionMinutes": 30, "sessionHours": 0} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Product settings | {"instanceDestinationId": "G-TJRR5S4PVS", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-TJRR5S4PVS"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced conversions settings | {"instanceDestinationId": "G-TJRR5S4PVS"} |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-TJRR5S4PVS"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-TJRR5S4PVS"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-TJRR5S4PVS"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-TJRR5S4PVS"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-TJRR5S4PVS"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Create-event rules | {"eventName": "banner_image_click", "isCopy": true, "instanceDestinationId": "G-TJRR5S4PVS", "precompiledRule": {"new_event_name": "banner_image_click", "merge… |
| Create-event rules | {"eventName": "checkout_complete", "isCopy": true, "instanceDestinationId": "G-TJRR5S4PVS", "precompiledRule": {"new_event_name": "checkout_complete", "merge_s… |
| Create-event rules | {"eventName": "in_cart_page_sessions", "isCopy": true, "instanceDestinationId": "G-TJRR5S4PVS", "precompiledRule": {"new_event_name": "in_cart_page_sessions", … |
| Create-event rules | {"eventName": "product_page_view_sessions", "isCopy": true, "instanceDestinationId": "G-TJRR5S4PVS", "precompiledRule": {"new_event_name": "product_page_view_s… |
| Create-event rules | {"eventName": "in_checkout_sessions", "isCopy": true, "instanceDestinationId": "G-TJRR5S4PVS", "precompiledRule": {"new_event_name": "in_checkout_sessions", "m… |
| Create-event rules | {"eventName": "newsletter_sign_up", "isCopy": true, "instanceDestinationId": "G-TJRR5S4PVS", "precompiledRule": {"new_event_name": "newsletter_sign_up", "merge… |
| User-provided data attached to hits | {"acceptAutomatic": false, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":3,\"args\":[{\"booleanExpressi… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-TJRR5S4PVS"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-TJRR5S4PVS"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-TJRR5S4PVS", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-TJRR5S4PVS", "sessionDuration": 0} |

---

### 6.6 Google Tag Settings — `GT-5MXQJPGV`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| __dest_mc | {"ignoreDupeGtagConfigCalls": true, "destinationId": "MC-F55EGMPPH3", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "MC-F55EGMPPH3"} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| GA4 | `G-5E5T774K31` | GTM-KFDVZH (container) |
| Universal Analytics | `UA-2180997-3` | GTM-KFDVZH (container) |
| Google Ads | `AW-1070638518` | network |
| Meta Pixel | `1256977304325263` | network |
| Microsoft Ads (UET) | `20018977` | network |
| Pinterest Tag | `2616682135507` | network |
| TikTok Pixel | `CHM4OTRC77U2H86LKPL0` | network |
| Google Analytics 4 | `G-238B3Z6CBM`, `G-5E5T774K31`, `G-TJRR5S4PVS` | network |
| Shopify app pixel: unknown app | {"product_bundles_data": "[]", "shop": "camera-ready-cosmetics.myshopify.com", "collect_url": "https://collect.bogos.io… | Shopify web pixel |
| Shopify app pixel: unknown app | {"subscriberKey": "r0shd-hi1o6x2g2al3w9bno-qqy8v"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"webPixelName": "Judge.me"} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `AW-1070638518`, `G-238B3Z6CBM`, `GTM-KFDVZH` | Shopify web pixel |
| Shopify app pixel: TikTok | {"pixelCode": "CHM4OTRC77U2H86LKPL0"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"site_id": "fd24c4ab-51b7-4031-b9f7-4732355ca8e4", "analytics_endpoint": "https://na.shgcdn3.com"} | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "1256977304325263", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"apiURL": "https://api.omnisend.com", "appURL": "https://app.omnisend.com", "brandID": "6480a1fae756cf8a95f16bc5", "tr… | Shopify web pixel |
| Shopify app pixel: Pinterest | {"tagID": "2616682135507"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shop_id": "camera-ready-cosmetics.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Google tag | `AW-1070638518` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://camerareadycosmetics.com/products/ben-nye-final-seal-matte-sealer · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item` | ✅ | ✅ |
| `add_to_cart` | ✅ | ✅ |
| `view_cart` | — | ✅ |
| `begin_checkout` | — | — |
| `purchase` | ✅ | — |

_Checkout and purchase events cannot be observed without placing an order; container configuration is listed instead._

---

## 9. Consent & Privacy

| Check | Result |
|---|---|
| CMP detected | Consent banner (CMP not identified) |
| Banner action taken by audit | button_text — button: Ok |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "", "analytics": "", "preferences": "", "sale_of_data": ""} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}, "security_storage": {"default": true, "update": null}, "functionality_storage": {"def… |
| Tracking vendors firing before consent | Campaign Manager 360 / Floodlight, Google Ads, Google Analytics, Google Analytics 4, Google Merchant Center, Meta Pixel, Pinterest Tag, TikTok Pixel, Universal Analytics |
| Scripts held until consent (text/plain, data-consent…) | — |
| Banner still visible after accept + reload | no |

**Consent configuration inside GTM:**

| Container | Consent types referenced | Consent templates | Tags with extra consent checks | CMP hints |
|---|---|---|---|---|
| `GTM-KFDVZH` | — | — | 0 / 11 | — |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-TJRR5S4PVS` | initial | page_view×2, (no event name)×1, scroll×1 | `G111` |
| GA4 `G-TJRR5S4PVS` | reload | user_engagement×2, page_view×2, scroll×2 | `G111` |
| GA4 `G-TJRR5S4PVS` | pdp | user_engagement×2, view_item×1, page_view×2, product_page_view_sessions×2, scroll×1 | `G111` |
| GA4 `G-TJRR5S4PVS` | atc | scroll×3, add_to_cart×1, user_engagement×2, page_view×2, in_cart_page_sessions×2, view_cart×1 | `G111` |
| GA4 `G-5E5T774K31` | initial | page_view×1, (no event name)×1 | `G111` |
| GA4 `G-5E5T774K31` | reload | user_engagement×2, page_view×1, scroll×1 | `G111` |
| GA4 `G-5E5T774K31` | pdp | user_engagement×2, view_item×1, page_view×1, scroll×1 | `G111` |
| GA4 `G-5E5T774K31` | atc | add_to_cart×1, user_engagement×2, page_view×1, scroll×1 | `G111` |
| GA4 `G-238B3Z6CBM` | initial | page_view×1, (no event name)×1 | `G111` |
| GA4 `G-238B3Z6CBM` | reload | user_engagement×2, page_view×2, scroll×1 | `G111` |
| GA4 `G-238B3Z6CBM` | pdp | user_engagement×2, page_view×1, view_item×1, scroll×1 | `G111` |
| GA4 `G-238B3Z6CBM` | atc | add_to_cart×1, user_engagement×2, page_view×1, view_cart×1, scroll×1 | `G111` |
| Meta `1256977304325263` | atc | PageView×1 | — |
| Google Ads `AW-1070638518` | initial | yfvXCPai8aYaELbLwv4D×3, gtag.config×2 | — |
| Google Ads `AW-1070638518` | reload | yfvXCPai8aYaELbLwv4D×3, gtag.config×1 | — |
| Google Ads `AW-1070638518` | pdp | yfvXCPai8aYaELbLwv4D×3, RGRPCPmi8aYaELbLwv4D×3, gtag.config×2 | — |
| Google Ads `AW-1070638518` | atc | form_start×1, form_submit×1, page_view×1, OApBCP-i8aYaELbLwv4D×3, yfvXCPai8aYaELbLwv4D×3, gtag.config×2 | — |

**dataLayer pushes observed:**

- `initial`: ga4kit_info, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-238B3Z6CBM, gtag:config:AW-1070638518, gtag:config:GT-5MXQJPGV, gtag:config:GTM-KFDVZH, gtag:event:page_view, Pandectes_Consent_Update, gtag:config:G-5E5T774K31, gtag:config:G-TJRR5S4PVS, gtm.dom, gtm.load
- `reload`: ga4kit_info, gtag:set, gtag:consent:default, gtag:js, gtag:config:G-238B3Z6CBM, gtag:config:G-5E5T774K31, gtag:config:G-TJRR5S4PVS, gtag:config:AW-1070638518, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:GT-5MXQJPGV, gtag:config:GTM-KFDVZH, gtm.scrollDepth, gtag:event:page_view, gtm.dom, Pandectes_Consent_Update, gtm.click, gtm.load
- `pdp`: ga4kit_info, analyzify_productDetail, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-238B3Z6CBM, gtag:config:AW-1070638518, gtag:config:GT-5MXQJPGV, gtag:config:GTM-KFDVZH, gtag:event:page_view, gtag:event:view_item, Pandectes_Consent_Update, gtag:config:G-5E5T774K31, gtag:config:G-TJRR5S4PVS, g…
- `atc`: ga4kit_info, analyzify_productDetail, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-238B3Z6CBM, gtag:config:AW-1070638518, gtag:config:GT-5MXQJPGV, gtag:config:GTM-KFDVZH, gtag:event:page_view, gtag:event:view_item, Pandectes_Consent_Update, gtag:config:G-5E5T774K31, gtag:config:G-TJRR5S4PVS, g…

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 2729803961 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"product_bundles_data": "[]", "shop": "camera-ready-cosmetics.myshopify.com", "collect_url": "https://collect.bogos.io… |
| 2321744057 | APP | — | ANALYTICS, PREFERENCES | {"subscriberKey": "r0shd-hi1o6x2g2al3w9bno-qqy8v"} |
| 887685305 | APP | — | ANALYTICS | {"webPixelName": "Judge.me"} |
| 384762041 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"G-238B3Z6CBM\",\"AW-1070638518\",\"GT-5MXQJPGV\",\"GTM-KFDVZH\"],\"target_country\":\… |
| 380502201 | APP | TikTok | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixelCode": "CHM4OTRC77U2H86LKPL0"} |
| 244908217 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"site_id": "fd24c4ab-51b7-4031-b9f7-4732355ca8e4", "analytics_endpoint": "https://na.shgcdn3.com"} |
| 211681465 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "1256977304325263", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} |
| 156598457 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"apiURL": "https://api.omnisend.com", "appURL": "https://app.omnisend.com", "brandID": "6480a1fae756cf8a95f16bc5", "tr… |
| 41975993 | APP | Pinterest | ANALYTICS, MARKETING, SALE_OF_DATA | {"tagID": "2616682135507"} |
| 32047289 | APP | — | ANALYTICS | {"shop_id": "camera-ready-cosmetics.myshopify.com"} |
| 94732473 | CUSTOM | — | ANALYTICS | — |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `GTM-KFDVZH` | GTM | 46 | 498.1 KB | reload | googletagmanager.com | 11 | 1 | 50 | 10 |
| `AW-1070638518` | GTAG | 3 | 482.3 KB | reload | googletagmanager.com | 12 | 0 | 4 | 4 |
| `G-238B3Z6CBM` | GTAG | 4 | 595.4 KB | reload | googletagmanager.com | 24 | 0 | 7 | 4 |
| `G-5E5T774K31` | GTAG | 26 | 567.9 KB | reload | googletagmanager.com | 23 | 0 | 7 | 4 |
| `G-TJRR5S4PVS` | GTAG | 7 | 583.1 KB | reload | googletagmanager.com | 30 | 0 | 7 | 4 |
| `GT-5MXQJPGV` | GTAG | 1 | 434.9 KB | reload | googletagmanager.com | 7 | 0 | 4 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `AW-1070638518`, `G-238B3Z6CBM`, `G-5E5T774K31`, `G-TJRR5S4PVS`, `GT-5MXQJPGV`, `GTM-KFDVZH`
- GTM IDs referenced in page HTML: `GTM-KFDVZH`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google tag (gtag.js) | — | 45 | initial:12, reload:11, pdp:11, atc:11 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |
| Google Analytics 4 | `G-238B3Z6CBM`, `G-5E5T774K31`, `G-TJRR5S4PVS` | 63 | initial:8, reload:15, pdp:18, atc:22 | 0 |
| Universal Analytics | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 2 | initial:1, atc:1 | 0 |
| Google Ads | `AW-1070638518` | 67 | initial:13, reload:9, pdp:17, atc:28 | 0 |
| Google Merchant Center | — | 7 | initial:1, reload:2, pdp:2, atc:2 | 0 |
| Meta Pixel | `1256977304325263` | 18 | initial:4, reload:3, pdp:6, atc:5 | 0 |
| Microsoft Ads (UET) | `20018977` | 18 | reload:9, pdp:2, atc:7 | 0 |
| Pinterest Tag | `2616682135507` | 15 | initial:4, reload:3, pdp:4, atc:4 | 0 |
| TikTok Pixel | `CHM4OTRC77U2H86LKPL0` | 14 | initial:3, reload:3, pdp:4, atc:4 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Omnisend | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Judge.me | — | 5 | initial:1, reload:2, pdp:2 | 0 |

### Support / chat

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Gorgias | — | 130 | consent:34, reload:28, pdp:28, atc:40 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 1 | initial:1 | 0 |
| Shopify | — | 38 | initial:8, reload:5, pdp:12, atc:13 | 0 |
| Shopify Analytics (Monorail) | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |
| Shopify CDN | — | 344 | initial:76, consent:2, reload:92, pdp:85, atc:89 | 0 |

### Payments / BNPL

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Afterpay | — | 3 | pdp:3 | 0 |
| Square | — | 4 | pdp:4 | 0 |

### Monitoring

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Sentry | — | 6 | initial:1, reload:1, pdp:2, atc:2 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`edge.personalizer.io` (164), `storefront.personalizer.io` (49), `amaicdn.com` (20), `omnisnippet1.com` (16), `cdn.addsauce.com` (12), `news.google.com` (8), `api-brokenlinkmanager.seoant.com` (8), `play.google.com` (8), `review-images.judgeme.com` (8), `beacon.kendall.ai` (7), `forms.soundestlink.com` (7), `fonts.soundestlink.com` (7), `shop.orderdeadline.com` (6), `app.addsauce.com` (6), `media.9gtb.com` (6), `h.online-metrix.net` (6), `addsauce-static-alt.b-cdn.net` (6), `camera-ready-cosmetics.myshopify.com` (5), `na.shgcdn3.com` (4), `limits.minmaxify.com` (4), `cdn.bogos.io` (4), `s3.amazonaws.com` (4), `a.pandect.es` (4), `app.utterbond.com` (4), `extensions.shopifycdn.com` (4), `storage.googleapis.com` (4), `customer-first-focus.b-cdn.net` (3), `h64.online-metrix.net` (3), `snapppt.com` (2), `formsv2.soundestlink.com` (2)

</details>

---

## 14. Findings & Recommendations

### P1 — Fix now

**[Tracking · GA4] Not met: GA4 — One implementation per property**  
G-TJRR5S4PVS <- Shopify app: Google & YouTube x15, Shopify custom pixel #94732473 x14 Why it matters: Two implementations double-count events and revenue.  
_Recommendation:_ Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM carries a richer setup (then switch GA4 off in the app).

**[Tracking · GA4] Not met: GA4 — Page view sent once per load**  
Duplicates on one page load: G-238B3Z6CBM×2 (from Shopify app: Google & YouTube); G-TJRR5S4PVS×2 (from Shopify app: Google & YouTube, Shopify custom pixel #94732473) Why it matters: Double page views inflate traffic and deflate conversion rates; for ad pixels they distort optimisation.  
_Recommendation:_ Remove the second source (app vs GTM vs hard-coded / custom pixel).

### P2 — Address within 30 days

**[Consent] Ad pixels fire before the visible consent banner is answered**  
A consent banner (Consent banner (CMP not identified)) was shown, yet these fired on first load before it was answered: Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel, Pinterest Tag, TikTok Pixel. The banner implies opt-in, but tags don't wait for it.  
_Recommendation:_ Hold marketing tags until consent (Consent Mode default 'denied' + CMP-gated triggers), or switch the banner to an opt-out notice for US visitors if that is the intended model.

**[Analytics] Universal Analytics still deployed**  
5 active UA tag(s) in GTM and UA requests on the network. UA stopped processing data in July 2024.  
_Recommendation:_ Delete UA tags, GA Settings variables and UA-only triggers.

**[GTM · Ecommerce] Needs attention: GA4 ecommerce funnel coverage — GTM-KFDVZH**  
Configured in GTM: add_to_cart, purchase, view_item. Missing core: begin_checkout; missing recommended: view_item_list, select_item, view_cart, remove_from_cart, add_shipping_info, add_payment_info. Why it matters: Gaps or split ownership break funnel reports and double-count shared events.  
_Recommendation:_ Add the missing funnel events with items[] from the dataLayer.

**[Tracking · GA4] Needs attention: GA4 — Single deployment route**  
Hits come from 2 routes: Shopify app: Google & YouTube x49; Shopify custom pixel #94732473 x14. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

### P3 — Clean-up / informational

**[GTM · Measurement] Needs attention: Measurement ID in a variable, not hard-coded — GTM-KFDVZH**  
4 of 4 GA4 event tags hard-code the measurement ID. Why it matters: Hard-coded IDs make property migrations and staging setups error-prone.  
_Recommendation:_ Reference a Constant / Lookup Table variable so the ID changes in one place.

**[GTM · Governance] Needs attention: No unused variables — GTM-KFDVZH**  
19 variable(s) not referenced by any tag, trigger or variable: DLV - productName, DLV - productId, DLV - productBrand, DLV - productCategory, DLV - productVariantTitle, DLV - productPrice, DLV - productQuantity, DLV - payment_type Why it matters: Clutter hides what actually drives data.  
_Recommendation:_ Remove unused variables.

**[Tracking · GA4] Needs attention: GA4 — Single GA4 property**  
3 GA4 propertys receive data: G-238B3Z6CBM, G-5E5T774K31, G-TJRR5S4PVS. Why it matters: Extra IDs split audiences and send customer data to accounts nobody watches.  
_Recommendation:_ Confirm each is owned and in use; retire leftovers from agencies or old accounts.

**[Tracking · Microsoft Ads] Needs attention: Microsoft Ads — Product IDs for dynamic remarketing**  
No product IDs on UET hits from product pages.  
_Recommendation:_ Send ecomm_prodid + ecomm_pagetype (Shopping / dynamic remarketing).

**[Tracking · Stack] Needs attention: Stack — Third-party request volume**  
1374 third-party requests across the visit (22 identified platforms). Why it matters: Tag weight slows pages, which costs conversion rate.  
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
- Consent action: button_text — button: Ok
- Screenshots: [01_initial](screenshots/01_initial.png) · [02_after_consent](screenshots/02_after_consent.png) · [03_reload](screenshots/03_reload.png) · [04_pdp](screenshots/04_pdp.png) · [05_atc](screenshots/05_atc.png)
