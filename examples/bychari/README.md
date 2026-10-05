# Tracking & Martech Audit — BYCHARI

**Site:** https://bychari.com/  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Shopify Customer Events (app pixels)  
**Consent platform:** None detected  

---

## 1. Executive Summary

Tag management: **Shopify Customer Events (app pixels)**. GA4 property: `G-TZ5Q98C1Z6`. Tracking platforms (GA4 + ad pixels) score **100/100** on the events they actually received. The audit raised **1 P1**, **0 P2** and **0 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P1 | Consent | No consent banner or US opt-out mechanism |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** fully native — the Google & YouTube app (GA4 + Ads with enhanced conversions), Facebook & Instagram app, Pinterest app and Klaviyo app embed. There is no GTM, and every platform is fed by exactly one route.
- **What's working:** tracking 100/100 — clean, single-source, product-level events everywhere. This is the reference setup for a lean Shopify brand.
- **Gap — privacy:** six ad platforms fire with no consent banner, no geo-targeted CMP and no US "Your Privacy Choices" link, which is exposure under US state privacy laws and for EU orders via Global-e.
- **Pitch angle:** compliance hardening (Shopify privacy banner with region rules + opt-out link), then growth work (server-side / CAPI quality, attribution). Not a tracking rebuild.
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
- **Meta:** Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), and what Event Match Quality do Purchase events get?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?
- **Email / SMS:** Are browse- and cart-abandonment flows live in Klaviyo, and are Viewed Product / Added to Cart metrics recording?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### No GTM container — Google tag / Shopify app setup review

_No GTM container is deployed, so there is no container to score; these checks review the Google tag and app-based setup instead._

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ✅ | Medium | Google Ads | Enhanced conversions (user-provided data) | User-provided data collection is on. | — |
| ✅ | Low | Measurement | GA4 enhanced measurement | 7 enhanced-measurement feature(s) on G-TZ5Q98C1Z6. | — |
| ✅ | Low | Measurement | Google Signals | Enabled. | — |
| ℹ️ | Medium | Measurement | Tag management approach | No GTM container. Tags are deployed via Shopify app pixels (AdScale, Global-e, Google & YouTube, Klaviyo, Meta (Facebook & Instagram), Pinterest). | Fine for a lean channel mix. Move to GTM (or a Shopify custom pixel + GTM) once the brand needs custom events, more ad platforms or consent orchestration beyond the apps. |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **100/100** (✅ 31 · ⚠️ 0 · ❌ 0).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 100 | 10 | 0 | 0 | Shopify app: Google & YouTube ×17 | initial: page_view×1, (none)×1; reload: user_engagement×2, page_view×1; pdp: scroll×3, user_engagement×2, page_view×1, view_item×1; atc: add_to_cart×1, user_engagement×2, page_view×1, scroll×1 |
| Google Ads | 100 | 5 | 0 | 0 | Shopify app: Google & YouTube ×42 | initial: page_view×5; reload: page_view×5; pdp: page_view×5, view_item×4; atc: form_start×3, form_submit×3, add_to_cart×4, page_view×13 |
| Meta | 100 | 7 | 0 | 0 | Shopify app: Meta (Facebook & Instagram) ×7 | initial: PageView×1; reload: PageView×1; pdp: PageView×1, ViewContent×1; atc: SubscribedButtonClick×1, AddToCart×1, PageView×1 |
| Pinterest | 100 | 6 | 0 | 0 | Shopify app: Pinterest ×10 | initial: init×1, PageVisit×1; reload: init×1, PageVisit×1; pdp: init×1, PageVisit×2; atc: AddToCart×1, init×1, PageVisit×1 |
| Klaviyo | 100 | 2 | 0 | 0 | Shopify app embed: klaviyo-email-marketing-sms ×48 | initial: (onsite.js loaded)×12; reload: (onsite.js loaded)×12; pdp: (onsite.js loaded)×12; atc: (onsite.js loaded)×12 |

### GA4 — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single GA4 property | GA4 property: G-TZ5Q98C1Z6. | — |
| ✅ | High | One implementation per property | G-TZ5Q98C1Z6 <- Shopify app: Google & YouTube | — |
| ✅ | High | Page view sent once per load | G-TZ5Q98C1Z6×1 on one page load. | — |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (1×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: scroll, user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x17. | — |

### Google Ads — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Google Ads account | Google Ads account: AW-829377681. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 23 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x42. | — |

### Meta — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Meta pixel | Meta pixel: 167292997187425. | — |
| ✅ | High | Page view sent once per load | 167292997187425×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 6 of 6 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Meta (Facebook & Instagram) x7. | — |

### Pinterest — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Pinterest tag | Pinterest tag: 2619449262943. | — |
| ✅ | High | Page view sent once per load | 2619449262943×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | PageVisit sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _pin_unauth. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Pinterest x10. | — |

### Klaviyo — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Medium | Onsite tracking (klaviyo.js) loaded | klaviyo.js loads. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: __kla_id. | — |
| ℹ️ | Medium | Viewed Product tracked (browse abandonment) | No Viewed Product event (only identified profiles are tracked — anonymous visitors expected to show none). | Confirm Viewed Product is enabled in the Klaviyo Shopify integration. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app embed: klaviyo-email-marketing-sms x48. | — |

### Stack — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Third-party request volume | 824 third-party requests across the visit (24 identified platforms). | — |
| ℹ️ | Low | Session-replay tools | 0: none. | — |
| ℹ️ | Low | Ad platforms in use | 6: AdScale, Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel, Pinterest Tag. | — |

---

## 6. Container Inventory & Settings

### 6.1 Google Tag Settings — `AW-829377681`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-829377681"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-829377681"} |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-829377681"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "deferPageView": false, "includeParams": true, "instanceDestinationId": "AW-829377681"} |
| Google Ads conversion marking | {"conversionRules": [{"matchingRules": "{\"type\":2,\"args\":[{\"booleanExpressionValue\":{\"type\":1,\"args\":[{\"booleanExpressionValue\":{\"type\":6,\"args\… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "AW-829377681", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "AW-829377681"} |

---

### 6.2 Google Tag Settings — `G-TZ5Q98C1Z6`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Product settings | {"instanceDestinationId": "G-TZ5Q98C1Z6", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced conversions settings | {"instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Enhanced measurement: form interactions | {"includeParams": true, "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Enhanced measurement: site search | {"searchQueryParams": "q", "includeParams": true, "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| User-provided data attached to hits | {"acceptAutomatic": false, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":3,\"args\":[{\"booleanExpressi… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-TZ5Q98C1Z6"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-TZ5Q98C1Z6"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-TZ5Q98C1Z6", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-TZ5Q98C1Z6", "sessionDuration": 0} |

---

### 6.3 Google Tag Settings — `GT-M3SM9GTN`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| __dest_mc | {"ignoreDupeGtagConfigCalls": true, "destinationId": "MC-JSH24TEY7P", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "MC-JSH24TEY7P"} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| Google Ads | `AW-829377681` | network |
| Meta Pixel | `167292997187425` | network |
| Pinterest Tag | `2619449262943` | network |
| Google Analytics 4 | `G-TZ5Q98C1Z6` | network |
| Klaviyo | `VxNjpR` | network |
| Shopify app pixel: Klaviyo | {"accountID": "VxNjpR", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} | Shopify web pixel |
| Shopify app pixel: AdScale | {"accountID": "AdScaleWepPixel", "adscaleShopHost": "bychari"} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `AW-829377681`, `G-TZ5Q98C1Z6` | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "167292997187425", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} | Shopify web pixel |
| Shopify app pixel: Global-e | {"accountId": "Global-e", "merchantId": "60000098", "baseApiUrl": "https://checkout-service.global-e.com/api/v1", "site… | Shopify web pixel |
| Shopify app pixel: unknown app | {"accountID": "clu2q49zg0000l708zuk5zkc0", "popupIds": "[]"} | Shopify web pixel |
| Shopify app pixel: Pinterest | {"tagID": "2619449262943"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Klaviyo | `VxNjpR` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://bychari.com/products/keepsake-box · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item` | — | ✅ |
| `add_to_cart` | — | ✅ |
| `begin_checkout` | — | — |
| `purchase` | — | — |

_Checkout and purchase events cannot be observed without placing an order; container configuration is listed instead._

---

## 9. Consent & Privacy

| Check | Result |
|---|---|
| CMP detected | None |
| Banner action taken by audit | js_api — Shopify Customer Privacy (no visible banner) |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "yes", "analytics": "yes", "preferences": "yes", "sale_of_data": "yes"} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}} |
| Tracking vendors firing before consent | AdScale, Amplitude, Campaign Manager 360 / Floodlight, Google Ads, Google Analytics 4, Google Merchant Center, Meta Pixel, Pinterest Tag, PostHog |
| Scripts held until consent (text/plain, data-consent…) | — |
| Banner still visible after accept + reload | no |

_Returning visit: the persistent browser profile already held this site's cookies/consent, so the `initial` phase reflects stored consent, not a first visit (re-run with `--fresh` for that)._

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-TZ5Q98C1Z6` | initial | page_view×1, (no event name)×1 | `G111` |
| GA4 `G-TZ5Q98C1Z6` | reload | user_engagement×2, page_view×1 | `G111` |
| GA4 `G-TZ5Q98C1Z6` | pdp | scroll×3, user_engagement×2, page_view×1, view_item×1 | `G111` |
| GA4 `G-TZ5Q98C1Z6` | atc | add_to_cart×1, user_engagement×2, page_view×1, scroll×1 | `G111` |
| Google Ads `AW-829377681` | initial | HFZUCN7H6sYZEJGZvYsD×3 | — |
| Google Ads `AW-829377681` | reload | HFZUCN7H6sYZEJGZvYsD×3 | — |
| Google Ads `AW-829377681` | pdp | HFZUCN7H6sYZEJGZvYsD×3, P-sgCOHH6sYZEJGZvYsD×3 | — |
| Google Ads `AW-829377681` | atc | form_start×1, form_submit×1, 4G6SCOfH6sYZEJGZvYsD×3, GDvzCPKq5MYZEJGZvYsD×6, HFZUCN7H6sYZEJGZvYsD×3 | — |

**dataLayer pushes observed:**

- `initial`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:AW-829377681, gtag:config:GT-M3SM9GTN, gtag:config:G-TZ5Q98C1Z6, gtag:event:page_view, gtm.dom, gtm.load
- `reload`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:AW-829377681, gtag:config:GT-M3SM9GTN, gtag:config:G-TZ5Q98C1Z6, gtm.dom, gtag:event:page_view, gtm.load, gtm.scrollDepth
- `pdp`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:AW-829377681, gtag:config:GT-M3SM9GTN, gtag:config:G-TZ5Q98C1Z6, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load, gtm.scrollDepth
- `atc`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:AW-829377681, gtag:config:GT-M3SM9GTN, gtag:config:G-TZ5Q98C1Z6, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load, gtm.scrollDepth, gtm.formSubmit, gtag:event:add_to_cart

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 2053963839 | APP | Klaviyo | ANALYTICS, MARKETING | {"accountID": "VxNjpR", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} |
| 1653669951 | APP | AdScale | ANALYTICS, MARKETING, SALE_OF_DATA | {"accountID": "AdScaleWepPixel", "adscaleShopHost": "bychari"} |
| 334856255 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"AW-829377681\",\"GT-M3SM9GTN\",\"G-TZ5Q98C1Z6\"],\"target_country\":\"US\",\"gtag_eve… |
| 89784383 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "167292997187425", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} |
| 88375359 | APP | Global-e | SALE_OF_DATA | {"accountId": "Global-e", "merchantId": "60000098", "baseApiUrl": "https://checkout-service.global-e.com/api/v1", "site… |
| 61276223 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"accountID": "clu2q49zg0000l708zuk5zkc0", "popupIds": "[]"} |
| 38666303 | APP | Pinterest | ANALYTICS, MARKETING, SALE_OF_DATA | {"tagID": "2619449262943"} |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `AW-829377681` | GTAG | 2 | 492.0 KB | reload | googletagmanager.com | 12 | 0 | 4 | 4 |
| `G-TZ5Q98C1Z6` | GTAG | 2 | 590.4 KB | reload | googletagmanager.com | 22 | 0 | 6 | 4 |
| `GT-M3SM9GTN` | GTAG | 1 | 434.9 KB | reload | googletagmanager.com | 7 | 0 | 4 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `AW-829377681`, `G-TZ5Q98C1Z6`, `GT-M3SM9GTN`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google tag (gtag.js) | — | 20 | initial:5, reload:5, pdp:5, atc:5 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Amplitude | — | 18 | initial:5, reload:4, pdp:3, atc:6 | 0 |
| Google Analytics 4 | `G-TZ5Q98C1Z6` | 17 | initial:2, reload:3, pdp:7, atc:5 | 0 |
| PostHog | — | 38 | initial:9, reload:9, pdp:9, atc:11 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| AdScale | — | 4 | initial:1, reload:1, pdp:1, atc:1 | ⚠️ 1 |
| Campaign Manager 360 / Floodlight | — | 2 | initial:1, atc:1 | 0 |
| Google Ads | `AW-829377681` | 42 | initial:5, reload:5, pdp:9, atc:23 | 0 |
| Google Merchant Center | — | 7 | initial:1, reload:2, pdp:2, atc:2 | 0 |
| Meta Pixel | `167292997187425` | 15 | initial:3, reload:3, pdp:4, atc:5 | 0 |
| Pinterest Tag | `2619449262943` | 15 | initial:4, reload:3, pdp:4, atc:4 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Klaviyo | `VxNjpR` | 53 | initial:13, reload:13, pdp:14, atc:13 | 0 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Foursixty | — | 3 | pdp:3 | ⚠️ 1 |

### Support / chat

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Gorgias | — | 127 | initial:46, reload:27, pdp:27, atc:27 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 5 | initial:2, reload:1, pdp:1, atc:1 | 0 |
| Shopify | — | 44 | initial:12, consent:1, reload:7, pdp:14, atc:10 | 0 |
| Shopify Analytics (Monorail) | — | 4 | initial:1, consent:1, pdp:1, atc:1 | 0 |
| Shopify CDN | — | 97 | initial:25, reload:24, pdp:24, atc:24 | 0 |

### Payments / BNPL

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Afterpay | — | 4 | pdp:4 | 0 |
| Square | — | 4 | pdp:4 | 0 |

### Ecommerce apps

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Accessibly | — | 25 | initial:7, reload:6, pdp:6, atc:6 | 0 |
| Global-e | — | 17 | initial:5, reload:4, pdp:4, atc:4 | 0 |
| Ground | — | 5 | initial:2, reload:1, pdp:1, atc:1 | 0 |
| Route | — | 42 | initial:7, consent:1, reload:8, pdp:5, atc:21 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`static.shopmy.us` (4), `api.appmate.io` (4), `storage.googleapis.com` (4), `d3bt4yq3k408c5.cloudfront.net` (4), `trafficguardapp.com` (1)

</details>

---

## 14. Findings & Recommendations

### P1 — Fix now

**[Consent] No consent banner or US opt-out mechanism**  
6 advertising platform(s) fire (AdScale, Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel, Pinterest Tag); no CMP, no geo-targeted banner markup and no 'Do Not Sell or Share' / 'Your Privacy Choices' link were found.  
_Recommendation:_ Enable Shopify's privacy banner (or a CMP) with region rules: opt-in for EU/UK, opt-out link + GPC for US state privacy laws (CCPA/CPRA and others).

<details><summary>Failed requests</summary>

| Vendor | Phase | Status / error | URL |
|---|---|---|---|
| Foursixty | pdp | net::ERR_FAILED (likely capture network) | https://foursixty.com/api/v2/bychari/timeline/?pagination_type=cursor&page_size=10&format=json&page… |
| AdScale | pdp | net::ERR_CONNECTION_CLOSED (likely capture network) | https://cdn.adscale.com/static/ecom_js/bychari/add_item_to_cart.js?ver=20260322&shop=bychari.myshop… |

</details>

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
- Returning visit: the persistent browser profile already held this site's consent, so `initial` reflects stored consent (re-run with `--fresh` for a first-visit view).
- Consent action: js_api — Shopify Customer Privacy (no visible banner)
- Screenshots: [01_initial](screenshots/01_initial.png) · [02_after_consent](screenshots/02_after_consent.png) · [03_reload](screenshots/03_reload.png) · [04_pdp](screenshots/04_pdp.png) · [05_atc](screenshots/05_atc.png)
