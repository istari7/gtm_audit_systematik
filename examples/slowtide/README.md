# Tracking & Martech Audit — Slowtide

**Site:** https://slowtide.co  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Shopify Customer Events (app pixels)  
**Consent platform:** Shopify Privacy Banner  

---

## 1. Executive Summary

Tag management: **Shopify Customer Events (app pixels)**. GA4 property: `G-SQ90CKK1QF`. Tracking platforms (GA4 + ad pixels) score **99/100** on the events they actually received. The audit raised **0 P1**, **0 P2** and **1 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P3 | Tracking · Stack | Needs attention: Stack — Third-party request volume |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** fully native — the Google & YouTube, Facebook & Instagram and Pinterest apps plus the Klaviyo app embed, all behind the Shopify privacy banner.
- **What's working:** tracking 99/100. The banner is shown and respected, and each platform receives single-source events with product, value and currency.
- **Note:** consent didn't persist from homepage to product page in one capture (the re-run kept it), so a quick manual check of the banner's persistence is worthwhile.
- **Pitch angle:** growth (server-side quality, attribution, LTV); no tracking repair needed.
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
| ✅ | Low | Measurement | GA4 enhanced measurement | 7 enhanced-measurement feature(s) on G-SQ90CKK1QF. | — |
| ✅ | Low | Measurement | Google Signals | Enabled. | — |
| ℹ️ | Medium | Measurement | Tag management approach | No GTM container. Tags are deployed via Shopify app pixels (Google & YouTube, Klaviyo, Meta (Facebook & Instagram), Pinterest, TikTok). | Fine for a lean channel mix. Move to GTM (or a Shopify custom pixel + GTM) once the brand needs custom events, more ad platforms or consent orchestration beyond the apps. |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **99/100** (✅ 30 · ⚠️ 1 · ❌ 0).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 100 | 10 | 0 | 0 | Shopify app: Google & YouTube ×18 | reload: user_engagement×2, page_view×1; pdp: scroll×2, user_engagement×2, page_view×1, view_item×1; atc: scroll×1, add_to_cart×1, user_engagement×3, page_view×1, view_cart×1 |
| Google Ads | 100 | 5 | 0 | 0 | Shopify app: Google & YouTube ×22; Theme HTML (hard-coded) ×4; Unattributed ×2 | reload: page_view×7; pdp: page_view×5, view_item×4; atc: add_to_cart×4, page_view×5 |
| Meta | 100 | 7 | 0 | 0 | Shopify app: Meta (Facebook & Instagram) ×8 | reload: PageView×1; pdp: PageView×1, ViewContent×1; atc: SubscribedButtonClick×2, AddToCart×1, PageView×1 |
| Pinterest | 100 | 6 | 0 | 0 | Shopify app: Pinterest ×10 | reload: init×1, PageVisit×1; pdp: init×1, PageVisit×2; atc: AddToCart×1, init×1, PageVisit×1 |
| Klaviyo | 100 | 2 | 0 | 0 | Shopify app embed: klaviyo-email-marketing-sms ×96 | initial: (onsite.js loaded)×24; reload: (onsite.js loaded)×24; pdp: (onsite.js loaded)×24; atc: (onsite.js loaded)×24 |

### GA4 — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single GA4 property | GA4 property: G-SQ90CKK1QF. | — |
| ✅ | High | One implementation per property | G-SQ90CKK1QF <- Shopify app: Google & YouTube | — |
| ✅ | High | Page view sent once per load | G-SQ90CKK1QF×1 on one page load. | — |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (1×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: scroll, user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x18. | — |

### Google Ads — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Google Ads account | Google Ads account: AW-950743222. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 9 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x22; Theme HTML (hard-coded) x4; Unattributed x2. | — |

### Meta — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Meta pixel | Meta pixel: 149668365633703. | — |
| ✅ | High | Page view sent once per load | 149668365633703×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 6 of 6 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Meta (Facebook & Instagram) x8. | — |

### Pinterest — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Pinterest tag | Pinterest tag: 2612774016007. | — |
| ✅ | High | Page view sent once per load | 2612774016007×1 on one page load. | — |
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
| ℹ️ | Low | Deployment route | Sent via: Shopify app embed: klaviyo-email-marketing-sms x96. | — |

### Stack — 50/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Low | Third-party request volume | 1047 third-party requests across the visit (19 identified platforms). | Audit apps/pixels that don't earn their weight. |
| ℹ️ | Low | Session-replay tools | 0: none. | — |
| ℹ️ | Low | Ad platforms in use | 6: Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel, Pinterest Tag, TikTok Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Google Tag Settings — `G-SQ90CKK1QF`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-950743222"} |
| DMA (EU Digital Markets Act) settings | {"delegationMode": "ON", "dmaDefault": "DENIED"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": true, "manualPhoneEnabled": false, "manualAddressEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSe… |
| Product settings | {"instanceDestinationId": "G-SQ90CKK1QF", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-SQ90CKK1QF"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced conversions settings | {"instanceDestinationId": "G-SQ90CKK1QF"} |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-SQ90CKK1QF"} |
| Enhanced measurement: form interactions | {"includeParams": true, "instanceDestinationId": "G-SQ90CKK1QF"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-SQ90CKK1QF"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-SQ90CKK1QF"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-SQ90CKK1QF"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-SQ90CKK1QF"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-SQ90CKK1QF"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| User-provided data attached to hits | {"acceptAutomatic": false, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":3,\"args\":[{\"booleanExpressi… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-950743222"} |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-SQ90CKK1QF"} |
| __ccd_enable_cm | {"instanceDestinationId": "AW-950743222"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-SQ90CKK1QF"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":2,\"args\":[{\"booleanExpressio… |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-SQ90CKK1QF", "enableVariablesInDestinationId": false} |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "AW-950743222", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-SQ90CKK1QF", "sessionDuration": 0} |
| Remarketing / conversion page view | {"containerId": "AW-950743222"} |

---

### 6.2 Google Tag Settings — `GT-WF3BRKNB`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| __dest_mc | {"ignoreDupeGtagConfigCalls": true, "destinationId": "MC-MH92TWQQW4", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "MC-MH92TWQQW4"} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| Google Ads | `AW-950743222` | network |
| Meta Pixel | `149668365633703` | network |
| Pinterest Tag | `2612774016007` | network |
| TikTok Pixel | `CMS36LJC77U667VELM70` | network |
| Google Analytics 4 | `G-SQ90CKK1QF` | network |
| Klaviyo | `N4WxA4` | network |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `AW-950743222`, `G-SQ90CKK1QF` | Shopify web pixel |
| Shopify app pixel: unknown app | {"widgetId": "zmyni7sdqbm3u7m", "baseRequestUrl": "https://shopify-server.getredo.com/widgets", "splitEnabled": "false"… | Shopify web pixel |
| Shopify app pixel: Klaviyo | {"accountID": "N4WxA4", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"myshopifyDomain": "slowtide.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: TikTok | {"pixelCode": "CMS36LJC77U667VELM70"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"masterTagID": "92097", "merchantID": "97652", "appPath": "https://daedalus.shareasale.com", "storeID": "NaN", "xTypeM… | Shopify web pixel |
| Shopify app pixel: unknown app | {"shopDomain": "slowtide.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "149668365633703", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} | Shopify web pixel |
| Shopify app pixel: Pinterest | {"tagID": "2612774016007"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Klaviyo | `N4WxA4` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://slowtide.co/products/gatsby-towel-bundle-2-2-sequoia · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item` | — | ✅ |
| `add_to_cart` | — | ✅ |
| `view_cart` | — | ✅ |
| `begin_checkout` | — | — |
| `purchase` | — | — |

_Checkout and purchase events cannot be observed without placing an order; container configuration is listed instead._

---

## 9. Consent & Privacy

| Check | Result |
|---|---|
| CMP detected | Shopify Privacy Banner |
| Banner action taken by audit | banner_scan — Accept |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "", "analytics": "", "preferences": "", "sale_of_data": ""} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}} |
| Tracking vendors firing before consent | Impact, ShareASale |
| Scripts held until consent (text/plain, data-consent…) | — |
| Banner still visible after accept + reload | no |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-SQ90CKK1QF` | consent | page_view×1, (no event name)×1 | `G111` |
| GA4 `G-SQ90CKK1QF` | reload | user_engagement×2, page_view×1 | `G111` |
| GA4 `G-SQ90CKK1QF` | pdp | scroll×2, user_engagement×2, page_view×1, view_item×1 | `G111` |
| GA4 `G-SQ90CKK1QF` | atc | scroll×1, add_to_cart×1, user_engagement×3, page_view×1, view_cart×1 | `G111` |
| Meta `149668365633703` | consent | PageView×1 | — |
| Meta `149668365633703` | reload | PageView×1 | — |
| Meta `149668365633703` | atc | PageView×1 | — |
| Google Ads `AW-950743222` | consent | 2QYuCO29s_obELbhrMUD×2 | — |
| Google Ads `AW-950743222` | reload | 2QYuCO29s_obELbhrMUD×4 | — |
| Google Ads `AW-950743222` | pdp | 2QYuCO29s_obELbhrMUD×3, CcrECPC9s_obELbhrMUD×3 | — |
| Google Ads `AW-950743222` | atc | HK_PCOq9s_obELbhrMUD×3, 2QYuCO29s_obELbhrMUD×3 | — |

**dataLayer pushes observed:**

- `reload`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-SQ90CKK1QF, gtag:config:GT-WF3BRKNB, gtag:event:page_view, gtm.dom, gtm.load, gtm.scrollDepth
- `pdp`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-SQ90CKK1QF, gtag:config:GT-WF3BRKNB, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load, gtm.scrollDepth
- `atc`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-SQ90CKK1QF, gtag:config:GT-WF3BRKNB, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load, gtm.scrollDepth, gtm.formSubmit, gtag:event:add_to_cart

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 2239103094 | APP | — | ANALYTICS | {} |
| 1763606646 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"G-SQ90CKK1QF\",\"GT-WF3BRKNB\"],\"target_country\":\"US\",\"gtag_events\":[{\"type\":… |
| 1241776246 | APP | — | ANALYTICS, MARKETING | {"widgetId": "zmyni7sdqbm3u7m", "baseRequestUrl": "https://shopify-server.getredo.com/widgets", "splitEnabled": "false"… |
| 1241350262 | APP | Klaviyo | ANALYTICS, MARKETING | {"accountID": "N4WxA4", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} |
| 462454902 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"myshopifyDomain": "slowtide.myshopify.com"} |
| 286982262 | APP | TikTok | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixelCode": "CMS36LJC77U667VELM70"} |
| 166166646 | APP | — | ANALYTICS, MARKETING | {"masterTagID": "92097", "merchantID": "97652", "appPath": "https://daedalus.shareasale.com", "storeID": "NaN", "xTypeM… |
| 158859382 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"shopDomain": "slowtide.myshopify.com"} |
| 122650742 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "149668365633703", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} |
| 40173686 | APP | Pinterest | ANALYTICS, MARKETING, SALE_OF_DATA | {"tagID": "2612774016007"} |
| 28868726 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 98238582 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `G-SQ90CKK1QF` | GTAG | 5 | 599.9 KB | reload | googletagmanager.com | 31 | 0 | 6 | 5 |
| `GT-WF3BRKNB` | GTAG | 1 | 434.9 KB | reload | googletagmanager.com | 7 | 0 | 4 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `G-SQ90CKK1QF`, `GT-WF3BRKNB`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google tag (gtag.js) | — | 12 | consent:3, reload:3, pdp:3, atc:3 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-SQ90CKK1QF` | 18 | consent:2, reload:3, pdp:6, atc:7 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 1 | consent:1 | 0 |
| Google Ads | `AW-950743222` | 28 | consent:3, reload:7, pdp:9, atc:9 | 0 |
| Google Merchant Center | — | 8 | consent:1, reload:2, pdp:2, atc:3 | 0 |
| Meta Pixel | `149668365633703` | 16 | consent:3, reload:3, pdp:4, atc:6 | 0 |
| Pinterest Tag | `2612774016007` | 14 | consent:3, reload:3, pdp:4, atc:4 | 0 |
| TikTok Pixel | `CMS36LJC77U667VELM70` | 8 | consent:2, reload:2, pdp:2, atc:2 | 0 |

### Affiliate / influencer

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Awin | — | 4 | consent:1, reload:1, pdp:1, atc:1 | 0 |
| Impact | — | 171 | initial:39, reload:39, pdp:53, atc:40 | 0 |
| ShareASale | — | 8 | initial:2, reload:2, pdp:2, atc:2 | 0 |

### Personalisation / testing / search

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Rebuy | — | 50 | initial:12, consent:2, reload:12, pdp:14, atc:10 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Klaviyo | `N4WxA4` | 108 | initial:27, reload:27, pdp:27, atc:27 | 0 |

### Consent

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shopify Privacy Banner | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 9 | initial:3, reload:1, pdp:1, atc:4 | 0 |
| Shopify | — | 67 | initial:7, consent:3, reload:10, pdp:26, atc:21 | 0 |
| Shopify Analytics (Monorail) | — | 27 | initial:3, consent:1, reload:2, pdp:2, atc:19 | 0 |
| Shopify CDN | — | 161 | initial:35, reload:35, pdp:37, atc:54 | 0 |

### Payments / BNPL

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| PayPal | — | 8 | atc:8 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`shopify-extension.getredo.com` (117), `backend.alia-prod.com` (30), `files.alia-prod.com` (19), `shopify-cdn.getredo.com` (14), `widget.reviews.io` (12), `assets.reviews.io` (11), `instafeed.nfcube.com` (10), `apay-us.amazon.com` (8), `cdn.nfcube.com` (6), `api.reviews.io` (6), `shopify-server.getredo.com` (6), `cdn.acsbapp.com` (5), `play.google.com` (5), `backinstock.useamp.com` (4), `acsbapp.com` (4), `d19ayerf5ehaab.cloudfront.net` (4), `api.nfcube.com` (4), `id-shop.govx.com` (4), `extensions.shopifycdn.com` (4), `slowtide.myshopify.com` (4), `d1ce7ar9ygqaw4.cloudfront.net` (4), `lantern.roeyecdn.com` (4), `lantern.roeye.com` (4), `scontent.cdninstagram.com` (4), `pay.google.com` (3), `static-na.payments-amazon.com` (1), `m.media-amazon.com` (1)

</details>

---

## 14. Findings & Recommendations

### P3 — Clean-up / informational

**[Tracking · Stack] Needs attention: Stack — Third-party request volume**  
1047 third-party requests across the visit (19 identified platforms). Why it matters: Tag weight slows pages, which costs conversion rate.  
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
- Consent action: banner_scan — Accept
- Screenshots: [01_initial](screenshots/01_initial.png) · [02_after_consent](screenshots/02_after_consent.png) · [03_reload](screenshots/03_reload.png) · [04_pdp](screenshots/04_pdp.png) · [05_atc](screenshots/05_atc.png)
