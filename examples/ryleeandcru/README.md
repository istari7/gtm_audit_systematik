# Tracking & Martech Audit — Rylee + Cru

**Site:** https://ryleeandcru.com  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Shopify Customer Events (app pixels)  
**Consent platform:** Enzuzo  

---

## 1. Executive Summary

Tag management: **Shopify Customer Events (app pixels)**. GA4 property: `G-HBWSELGGYD`. Tracking platforms (GA4 + ad pixels) score **98/100** on the events they actually received. The audit raised **0 P1**, **1 P2** and **3 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P2 | Governance | GTM container GTM-5FWVZL4K is referenced but not published |
| P3 | Consent | Ad pixels fire on load (no banner shown to this visitor) |
| P3 | Tracking · Microsoft Ads | Needs attention: Microsoft Ads — First-party ID cookie set |
| P3 | Tracking · Stack | Needs attention: Stack — Third-party request volume |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** fully native — the Google & YouTube, Facebook & Instagram, TikTok, Pinterest and Microsoft apps, plus AppLovin (app pixel) and the Klaviyo app embed. Every platform is fed by exactly one route. The Enzuzo CMP shows no banner to US visitors, and a "Do Not Sell / Your Privacy Choices" link is present.
- **What's working:** tracking 98/100 — the cleanest multi-channel setup in the batch.
- **Loose ends:** a Shopify custom pixel loads GTM-5FWVZL4K, which is empty or unpublished (404); Microsoft UET doesn't set its first-party cookies. The store's bot protection can block automated cart adds.
- **Pitch angle:** growth rather than repair (CAPI match quality, attribution, creative testing). Clarify what the abandoned GTM was meant for.
- _Capture: US network, Oct 5 2026, fresh browser, consent accepted → reload → PDP → add to cart → cart. Outside-in only (no account access)._
<!-- ANALYST_NOTES_END -->

---

## 3. Next Steps — Analyst Checks & Discovery Questions

_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks below take minutes from the outside, and the questions are for the discovery conversation._

**Analyst checks (no account access needed)**

- [ ] **Consent:** Visit from an EU/UK VPN: does a banner appear, and do ad pixels wait for consent? — _Browser via EU VPN + DevTools → Network_

**Discovery questions for the prospect**

- **Purchase tracking:** Do GA4 revenue and Google Ads / Meta purchase counts reconcile with Shopify orders (a gap above ~10% usually means a tracking problem)?
- **Meta:** Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), and what Event Match Quality do Purchase events get?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?
- **GTM:** A GTM container loads but has no live tags — was it meant to take over from the apps, or can it be removed?
- **Email / SMS:** Are browse- and cart-abandonment flows live in Klaviyo, and are Viewed Product / Added to Cart metrics recording?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### No GTM container — Google tag / Shopify app setup review

_No GTM container is deployed, so there is no container to score; these checks review the Google tag and app-based setup instead._

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ✅ | Medium | Google Ads | Enhanced conversions (user-provided data) | User-provided data collection is on. | — |
| ✅ | Low | Measurement | GA4 enhanced measurement | 7 enhanced-measurement feature(s) on G-HBWSELGGYD. | — |
| ✅ | Low | Measurement | Google Signals | Enabled. | — |
| ℹ️ | Medium | Measurement | Tag management approach | No GTM container. Tags are deployed via Shopify app pixels (AppLovin, Google & YouTube, Klaviyo, Meta (Facebook & Instagram), Microsoft Ads, Pinterest, TikTok). | Fine for a lean channel mix. Move to GTM (or a Shopify custom pixel + GTM) once the brand needs custom events, more ad platforms or consent orchestration beyond the apps. |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **98/100** (✅ 40 · ⚠️ 2 · ❌ 0).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 100 | 10 | 0 | 0 | Shopify app: Google & YouTube ×16 | initial: page_view×1, (none)×1; reload: user_engagement×2, page_view×1; pdp: user_engagement×2, page_view×1, view_item×1; atc: scroll×1, add_to_cart×1, user_engagement×3, page_view×1, view_cart×1 |
| Google Ads | 100 | 5 | 0 | 0 | Shopify app: Google & YouTube ×122 | initial: gtag.config×3, page_view×26; reload: page_view×26, gtag.config×3; pdp: page_view×21, view_item×4; atc: form_start×3, form_submit×3, add_to_cart×4, page_view×26, gtag.config×3 |
| Meta | 100 | 7 | 0 | 0 | Shopify app: Meta (Facebook & Instagram) ×8 | initial: PageView×2; reload: PageView×1; pdp: PageView×1, ViewContent×1; atc: SubscribedButtonClick×1, AddToCart×1, PageView×1 |
| TikTok | 100 | 7 | 0 | 0 | Shopify app: TikTok ×7 | initial: Pageview×1, LandingPageView×1; reload: Pageview×1; pdp: Pageview×1, ViewContent×1; atc: AddToCart×1, Pageview×1 |
| Pinterest | 100 | 6 | 0 | 0 | Shopify app: Pinterest ×10 | initial: init×1, PageVisit×1; reload: init×1, PageVisit×1; pdp: init×1, PageVisit×2; atc: AddToCart×1, init×1, PageVisit×1 |
| Microsoft Ads | 86 | 3 | 1 | 0 | Shopify app: Microsoft Ads ×8 | initial: pageLoad×1, home×1; reload: pageLoad×1, home×1; pdp: pageLoad×1, view_item×1; atc: add_to_cart×1, pageLoad×1 |
| Klaviyo | 100 | 2 | 0 | 0 | Shopify app embed: klaviyo-email-marketing-sms ×184 | initial: (onsite.js loaded)×46; reload: (onsite.js loaded)×46; pdp: (onsite.js loaded)×46; atc: (onsite.js loaded)×46 |
| AppLovin | — | 0 | 0 | 0 | Shopify native app pixel (sandboxed) ×25 | initial: (request)×10; reload: (request)×3; pdp: (request)×4; atc: (request)×6 |

### GA4 — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single GA4 property | GA4 property: G-HBWSELGGYD. | — |
| ✅ | High | One implementation per property | G-HBWSELGGYD <- Shopify app: Google & YouTube | — |
| ✅ | High | Page view sent once per load | G-HBWSELGGYD×1 on one page load. | — |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (1×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: scroll, user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x16. | — |

### Google Ads — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Google Ads account | Google Ads account: AW-815119061. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 39 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x122. | — |

### Meta — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Meta pixel | Meta pixel: 151449808873131. | — |
| ✅ | High | Page view sent once per load | 151449808873131×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 7 of 7 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Meta (Facebook & Instagram) x8. | — |

### TikTok — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single TikTok pixel | TikTok pixel: CA8LEBRC77U9DD756IEG. | — |
| ✅ | High | Page view sent once per load | CA8LEBRC77U9DD756IEG×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | event_id for Events API dedupe | event_id present. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ttp. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: TikTok x7. | — |

### Pinterest — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Pinterest tag | Pinterest tag: 2617319882662. | — |
| ✅ | High | Page view sent once per load | 2617319882662×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | PageVisit sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _pin_unauth. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Pinterest x10. | — |

### Microsoft Ads — 86/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | First-party ID cookie set | Cookies after the visit: none of _uetsid, _uetvid. | Check the tag/app is allowed to set first-party cookies (consent, ITP, cookie flags). |
| ✅ | Low | Single UET tag | UET tag: 187125881. | — |
| ✅ | High | Page view sent once per load | 187125881×1 on one page load. | — |
| ✅ | Low | Product IDs for dynamic remarketing | ecomm_prodid / items present. | — |
| ℹ️ | Low | UET Consent Mode signal | No UET consent (asc) parameter. | Enable UET Consent Mode if serving EU/UK traffic. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Microsoft Ads x8. | — |

### Klaviyo — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Medium | Onsite tracking (klaviyo.js) loaded | klaviyo.js loads. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: __kla_id. | — |
| ℹ️ | Medium | Viewed Product tracked (browse abandonment) | No Viewed Product event (only identified profiles are tracked — anonymous visitors expected to show none). | Confirm Viewed Product is enabled in the Klaviyo Shopify integration. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app embed: klaviyo-email-marketing-sms x184. | — |

### AppLovin

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ℹ️ | Low | Pixel active | 25 hit(s): (request)×25. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify native app pixel (sandboxed) x25. | — |

### Stack — 50/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Low | Third-party request volume | 1624 third-party requests across the visit (25 identified platforms). | Audit apps/pixels that don't earn their weight. |
| ℹ️ | Low | Session-replay tools | 0: none. | — |
| ℹ️ | Low | Ad platforms in use | 7: AppLovin, Campaign Manager 360 / Floodlight, Google Ads, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Google Tag Settings — `AW-815119061`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-815119061"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-815119061"} |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-815119061"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "AW-815119061"} |
| Google Ads conversion marking | {"conversionRules": [{"matchingRules": "{\"type\":2,\"args\":[{\"booleanExpressionValue\":{\"type\":1,\"args\":[{\"booleanExpressionValue\":{\"type\":6,\"args\… |
| __ccd_enable_cm | {"instanceDestinationId": "AW-815119061"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":2,\"args\":[{\"booleanExpressio… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "AW-815119061", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "AW-815119061"} |

---

### 6.2 Google Tag Settings — `G-HBWSELGGYD`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| __ogt_ga_send | {"value": true} |
| Internal traffic rules | {"instanceOrder": 0, "paramValue": "internal", "ruleResult": false} |
| Unwanted referrals list | {"includeConditions": ["ryleeandcru\\.com", "paypal\\.com", "shopify\\.com", "checkout\\.shopify\\.com"]} |
| Custom session timeout | {"sessionMinutes": 30, "sessionHours": 0} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Product settings | {"instanceDestinationId": "G-HBWSELGGYD", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-HBWSELGGYD"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-HBWSELGGYD"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-HBWSELGGYD"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-HBWSELGGYD"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-HBWSELGGYD"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-HBWSELGGYD"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-HBWSELGGYD"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Create-event rules | {"eventName": "started_order", "isCopy": true, "instanceDestinationId": "G-HBWSELGGYD", "precompiledRule": {"new_event_name": "started_order", "merge_source_ev… |
| Create-event rules | {"eventName": "ua_add_to_cart", "isCopy": true, "instanceDestinationId": "G-HBWSELGGYD", "precompiledRule": {"new_event_name": "ua_add_to_cart", "merge_source_… |
| Create-event rules | {"eventName": "lookbook_view", "isCopy": true, "instanceDestinationId": "G-HBWSELGGYD", "precompiledRule": {"new_event_name": "lookbook_view", "merge_source_ev… |
| Create-event rules | {"eventName": "journal_share", "isCopy": true, "instanceDestinationId": "G-HBWSELGGYD", "precompiledRule": {"new_event_name": "journal_share", "merge_source_ev… |
| Create-event rules | {"eventName": "email_sign_up", "isCopy": true, "instanceDestinationId": "G-HBWSELGGYD", "precompiledRule": {"new_event_name": "email_sign_up", "merge_source_ev… |
| Create-event rules | {"eventName": "purchase_completed", "isCopy": true, "instanceDestinationId": "G-HBWSELGGYD", "precompiledRule": {"new_event_name": "purchase_completed", "merge… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-HBWSELGGYD"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-HBWSELGGYD"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-HBWSELGGYD", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-HBWSELGGYD", "sessionDuration": 0} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| Google Ads | `AW-815119061` | network |
| Meta Pixel | `151449808873131` | network |
| Microsoft Ads (UET) | `187125881` | network |
| Pinterest Tag | `2617319882662` | network |
| TikTok Pixel | `CA8LEBRC77U9DD756IEG` | network |
| Google Analytics 4 | `G-HBWSELGGYD` | network |
| Klaviyo | `Hr9LBd` | network |
| Shopify app pixel: unknown app | {"organizationId": "fc093029-f892-4c55-b186-3a737b718d6f", "entitySlug": "rylee-cru", "ingestUrl": "https://edge.outers… | Shopify web pixel |
| Shopify app pixel: unknown app | {"pixel_id": "QDWw6Z9zLBrpxMpvGLL2bU"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"octaneDomain": "https://app.octaneai.com", "octaneNewDomain": "https://app2.octaneai.com", "botID": "ihzgbdmz36sdpquq… | Shopify web pixel |
| Shopify app pixel: unknown app | {"subscriberId": "c783cb8b-a6b8-47d8-97ed-6117f515f94d", "pixelEventTrackingEnabled": "false", "pixelReviewsEventsEnabl… | Shopify web pixel |
| Shopify app pixel: unknown app | {"accountID": "9f0aa460-9f99-47e9-abfd-37c9dd01afb2", "customCartAddEventNames": ","} | Shopify web pixel |
| Shopify app pixel: AppLovin | {"eventKey": "d06ef54e-7e49-414f-ae47-5ce8be7c03f4", "name": "ryleeandcru - Axon Pixel"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Shopify app pixel: unknown app | {"dummy": "shopify-requires-a-setting", "mparticleKey": "us2-fb96263cc4b14544936e9afdcbdc77cf"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"accountID": "2834", "pixelToken": "e54x728ui8hl1q73fidoux4nn8m4zcpm", "sentryDsn": "https://f8803489a339de9179bc2a439… | Shopify web pixel |
| Shopify app pixel: unknown app | {"storeId": "694c8e15-9a66-46b1-8231-9c057a1f928b"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"extension": "rylee-cru"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"advertiserId": "60493", "shopDomain": "ryleeandcru.myshopify.com", "appVersion": "shopifyApp_5.3.0", "originalNetwork… | Shopify web pixel |
| Shopify app pixel: unknown app | {"brandID": "sr35u4uoru1t", "trackingURL": "https://track.proxima.ai/shopify"} | Shopify web pixel |
| Shopify app pixel: Klaviyo | {"accountID": "Hr9LBd", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"account_ID": "317496", "google_analytics_tracking_tag": "1", "measurement_id": "2", "api_secret": "3", "shop_settings… | Shopify web pixel |
| Shopify app pixel: unknown app | {"accountID": "auto-installed"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"debug": "false"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"accountID": "shopify-6763685", "endpoint": "https://connect.nosto.com"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shopID": "6763685"} | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "151449808873131", "pixel_type": "facebook_pixel"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"workspaceId":"ws-rylee-cru-m9n0bwa6_","accessToken":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzM3NjEyNTYyMDA… | Shopify web pixel |
| Shopify app pixel: unknown app | {"shopId": "ryleeandcru.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `AW-815119061`, `G-HBWSELGGYD` | Shopify web pixel |
| Shopify app pixel: TikTok | {"pixelCode": "CA8LEBRC77U9DD756IEG"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shop": "ryleeandcru.myshopify.com", "shopliftUrl": "https://events.shoplift.ai/api/events"} | Shopify web pixel |
| Shopify app pixel: Microsoft Ads | {"ti": "187125881", "endpoint": "https://bat.bing.com/action/0"} | Shopify web pixel |
| Shopify app pixel: Pinterest | {"tagID": "2617319882662"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Klaviyo | `Hr9LBd` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://ryleeandcru.com/products/ribbed-long-sleeve-rosewood · add-to-cart clicked: yes

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
| CMP detected | Enzuzo |
| Banner action taken by audit | js_api — Shopify Customer Privacy (no visible banner) |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "yes", "analytics": "yes", "preferences": "yes", "sale_of_data": ""} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}} |
| Tracking vendors firing before consent | AppLovin, Awin, Campaign Manager 360 / Floodlight, Google Ads, Google Analytics 4, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel |
| Scripts held until consent (text/plain, data-consent…) | https://play.gotolstoy.com/widget-v2/widget.brand-mcp.js [ignore], https://play.gotolstoy.com/widget-v2/widget.js [ignore], https://widget.gotolstoy.com/we/widget.js [ignore] |
| Banner still visible after accept + reload | no |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-HBWSELGGYD` | initial | page_view×1, (no event name)×1 | `G111` |
| GA4 `G-HBWSELGGYD` | reload | user_engagement×2, page_view×1 | `G111` |
| GA4 `G-HBWSELGGYD` | pdp | user_engagement×2, page_view×1, view_item×1 | `G111` |
| GA4 `G-HBWSELGGYD` | atc | scroll×1, add_to_cart×1, user_engagement×3, page_view×1, view_cart×1 | `G111` |
| Google Ads `AW-815119061` | initial | gtag.config×1, h5VLCOLU76gaENX11oQD×15, L-AUCPP4_7EBENX11oQD×3 | — |
| Google Ads `AW-815119061` | reload | h5VLCOLU76gaENX11oQD×15, L-AUCPP4_7EBENX11oQD×3, gtag.config×1 | — |
| Google Ads `AW-815119061` | pdp | h5VLCOLU76gaENX11oQD×12, L-AUCPP4_7EBENX11oQD×3, VBMRCPn4_7EBENX11oQD×3 | — |
| Google Ads `AW-815119061` | atc | form_start×1, form_submit×1, 7qveCO_6_7EBENX11oQD×3, h5VLCOLU76gaENX11oQD×15, L-AUCPP4_7EBENX11oQD×3, gtag.config×1 | — |

**dataLayer pushes observed:**

- `initial`: gtag:consent:update, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-HBWSELGGYD, gtag:config:AW-815119061, gtag:event:page_view, gtm.dom, gtm.load
- `reload`: gtag:consent:update, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-HBWSELGGYD, gtag:config:AW-815119061, gtm.dom, gtag:event:page_view, gtm.load
- `pdp`: gtag:consent:update, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-HBWSELGGYD, gtag:config:AW-815119061, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load, gtm.scrollDepth
- `atc`: gtag:consent:update, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-HBWSELGGYD, gtag:config:AW-815119061, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load, gtm.scrollDepth, gtm.formSubmit, gtag:event:add_to_cart

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 2801500207 | APP | — | ANALYTICS, MARKETING | {"organizationId": "fc093029-f892-4c55-b186-3a737b718d6f", "entitySlug": "rylee-cru", "ingestUrl": "https://edge.outers… |
| 2795798575 | APP | — | ANALYTICS, MARKETING | {"pixel_id": "QDWw6Z9zLBrpxMpvGLL2bU"} |
| 2794848303 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"octaneDomain": "https://app.octaneai.com", "octaneNewDomain": "https://app2.octaneai.com", "botID": "ihzgbdmz36sdpquq… |
| 2782461999 | APP | — | ANALYTICS | {"subscriberId": "c783cb8b-a6b8-47d8-97ed-6117f515f94d", "pixelEventTrackingEnabled": "false", "pixelReviewsEventsEnabl… |
| 2762571823 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"accountID": "9f0aa460-9f99-47e9-abfd-37c9dd01afb2", "customCartAddEventNames": ","} |
| 2733342767 | APP | AppLovin | ANALYTICS, MARKETING, SALE_OF_DATA | {"eventKey": "d06ef54e-7e49-414f-ae47-5ce8be7c03f4", "name": "ryleeandcru - Axon Pixel"} |
| 2601713711 | APP | — | ANALYTICS | {} |
| 2566389807 | APP | — | ANALYTICS, MARKETING | {"dummy": "shopify-requires-a-setting", "mparticleKey": "us2-fb96263cc4b14544936e9afdcbdc77cf"} |
| 2314731567 | APP | — | ANALYTICS, MARKETING | {"accountID": "2834", "pixelToken": "e54x728ui8hl1q73fidoux4nn8m4zcpm", "sentryDsn": "https://f8803489a339de9179bc2a439… |
| 2285174831 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"storeId": "694c8e15-9a66-46b1-8231-9c057a1f928b"} |
| 2118254639 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"extension": "rylee-cru"} |
| 2114551855 | APP | — | ANALYTICS, MARKETING | {"advertiserId": "60493", "shopDomain": "ryleeandcru.myshopify.com", "appVersion": "shopifyApp_5.3.0", "originalNetwork… |
| 1893728303 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"brandID": "sr35u4uoru1t", "trackingURL": "https://track.proxima.ai/shopify"} |
| 1422098479 | APP | Klaviyo | ANALYTICS, MARKETING | {"accountID": "Hr9LBd", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} |
| 1271398447 | APP | — | — | {"account_ID": "317496", "google_analytics_tracking_tag": "1", "measurement_id": "2", "api_secret": "3", "shop_settings… |
| 1090682927 | APP | — | ANALYTICS | {"accountID": "auto-installed"} |
| 838860847 | APP | — | ANALYTICS | {"debug": "false"} |
| 761135151 | APP | — | ANALYTICS, MARKETING | {"accountID": "shopify-6763685", "endpoint": "https://connect.nosto.com"} |
| 601784367 | APP | — | ANALYTICS | {"shopID": "6763685"} |
| 572063791 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "151449808873131", "pixel_type": "facebook_pixel"} |
| 557908015 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"workspaceId":"ws-rylee-cru-m9n0bwa6_","accessToken":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzM3NjEyNTYyMDA… |
| 524746799 | APP | — | ANALYTICS, MARKETING | {"shopId": "ryleeandcru.myshopify.com"} |
| 430800943 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"G-HBWSELGGYD\",\"AW-815119061\"],\"target_country\":\"US\",\"gtag_events\":[{\"type\"… |
| 330465327 | APP | TikTok | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixelCode": "CA8LEBRC77U9DD756IEG"} |
| 229572655 | APP | — | ANALYTICS | {"shop": "ryleeandcru.myshopify.com", "shopliftUrl": "https://events.shoplift.ai/api/events"} |
| 108855343 | APP | Microsoft Ads | ANALYTICS, MARKETING, SALE_OF_DATA | {"ti": "187125881", "endpoint": "https://bat.bing.com/action/0"} |
| 44138543 | APP | Pinterest | ANALYTICS, MARKETING, SALE_OF_DATA | {"tagID": "2617319882662"} |
| 65011759 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 98926639 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 100204591 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 110198831 | CUSTOM | — | — | — |
| 126943279 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 144179247 | CUSTOM | — | — | — |
| 145129519 | CUSTOM | — | — | — |
| 155090991 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 163610671 | CUSTOM | — | MARKETING, SALE_OF_DATA | — |
| 177274927 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 179372079 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `AW-815119061` | GTAG | 2 | 491.6 KB | reload | googletagmanager.com | 14 | 0 | 4 | 4 |
| `G-HBWSELGGYD` | GTAG | 2 | 574.8 KB | reload | googletagmanager.com | 28 | 0 | 7 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `AW-815119061`, `G-HBWSELGGYD`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Tag Manager | `GTM-5FWVZL4K` | 3 | initial:1, reload:1, atc:1 | ⚠️ 3 |
| Google tag (gtag.js) | — | 15 | initial:4, reload:4, pdp:3, atc:4 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-HBWSELGGYD` | 14 | initial:2, reload:3, pdp:3, atc:6 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| AppLovin | — | 25 | initial:10, consent:2, reload:3, pdp:4, atc:6 | ⚠️ 1 |
| Campaign Manager 360 / Floodlight | — | 2 | initial:1, pdp:1 | 0 |
| Google Ads | `AW-815119061` | 122 | initial:29, reload:29, pdp:25, atc:39 | 0 |
| Meta Pixel | `151449808873131` | 22 | initial:6, reload:5, pdp:4, atc:7 | 0 |
| Microsoft Ads (UET) | `187125881` | 8 | initial:2, reload:2, pdp:2, atc:2 | 0 |
| Pinterest Tag | `2617319882662` | 14 | initial:3, reload:3, pdp:4, atc:4 | 0 |
| TikTok Pixel | `CA8LEBRC77U9DD756IEG` | 15 | initial:4, reload:3, pdp:4, atc:4 | 0 |

### Affiliate / influencer

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Awin | — | 3 | initial:1, reload:1, atc:1 | 0 |

### Personalisation / testing / search

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Rebuy | — | 43 | initial:12, reload:10, pdp:11, atc:10 | 0 |
| Shoplift | — | 11 | initial:1, consent:2, reload:1, pdp:3, atc:4 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Klaviyo | `Hr9LBd` | 204 | initial:51, reload:51, pdp:51, atc:51 | 0 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Foursixty | — | 5 | initial:2, reload:3 | 0 |
| Okendo | — | 53 | initial:2, reload:2, pdp:46, atc:3 | 0 |

### Support / chat

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Richpanel | — | 16 | initial:4, reload:4, pdp:4, atc:4 | 0 |

### Consent

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Enzuzo | — | 8 | initial:2, reload:2, pdp:2, atc:2 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 7 | initial:3, reload:1, pdp:1, atc:2 | 0 |
| Shopify | — | 65 | initial:8, consent:2, reload:14, pdp:15, atc:26 | 0 |
| Shopify Analytics (Monorail) | — | 45 | initial:4, consent:1, reload:4, pdp:4, atc:32 | 0 |
| Shopify CDN | — | 332 | initial:78, consent:4, reload:82, pdp:87, atc:81 | 0 |

### Payments / BNPL

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| PayPal | — | 12 | atc:12 | 0 |

### Monitoring

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Datadog | — | 4 | initial:1, consent:1, reload:1, atc:1 | 0 |
| Sentry | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`cdn.gotolstoy.com` (48), `web-analytics.dashfi.net` (34), `play.gotolstoy.com` (28), `h2.aisiteanalytics.com` (24), `backend.alia-prod.com` (23), `hsr.heatmapcore.com` (18), `oirt.aggle.net` (15), `scontent.cdninstagram.com` (15), `cf-apilb.gotolstoy.com` (14), `dashboard.heatmap.com` (14), `data.getangler.ai` (14), `api.config-security.com` (13), `web-pixel-ingestor.pdqprod.link` (13), `cm.g.doubleclick.net` (11), `srevents.heatmapcore.com` (11), `widget.gotolstoy.com` (10), `files.alia-prod.com` (10), `idx.liadm.com` (10), `visits.heatmapcore.com` (9), `checkout-clarity-events.pdqprod.link` (9), `track.getgobot.com` (8), `c.heatmap.com` (8), `static.getangler.ai` (8), `cdn-bundler.nice-team.net` (8), `pdq-scripts.pdqprod.link` (8), `js.dashfi.net` (7), `mm-uxrv.com` (7), `lantern.roeyecdn.com` (7), `lantern.roeye.com` (7), `track.proxima.ai` (7)

</details>

---

## 14. Findings & Recommendations

### P2 — Address within 30 days

**[Governance] GTM container GTM-5FWVZL4K is referenced but not published**  
The site requests GTM-5FWVZL4K, but googletagmanager.com returns 404, so the container is unpublished or deleted. Any tags expected from it never fire.  
_Recommendation:_ Remove the snippet (theme or Shopify custom pixel), or publish the container if it's meant to be live.

### P3 — Clean-up / informational

**[Consent] Ad pixels fire on load (no banner shown to this visitor)**  
Enzuzo is present but showed no banner to this US visitor; AppLovin, Campaign Manager 360 / Floodlight, Google Ads, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel fired on load — consistent with a US opt-out model.  
_Recommendation:_ Confirm EU/UK visitors get an opt-in banner and US opt-out (Do Not Sell / GPC) suppresses these pixels.

**[Tracking · Microsoft Ads] Needs attention: Microsoft Ads — First-party ID cookie set**  
Cookies after the visit: none of _uetsid, _uetvid. Why it matters: First-party IDs keep attribution and audiences working as third-party cookies disappear.  
_Recommendation:_ Check the tag/app is allowed to set first-party cookies (consent, ITP, cookie flags).

**[Tracking · Stack] Needs attention: Stack — Third-party request volume**  
1624 third-party requests across the visit (25 identified platforms). Why it matters: Tag weight slows pages, which costs conversion rate.  
_Recommendation:_ Audit apps/pixels that don't earn their weight.

<details><summary>Failed requests</summary>

| Vendor | Phase | Status / error | URL |
|---|---|---|---|
| Google Tag Manager | initial | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://www.googletagmanager.com/gtm.js?id=GTM-5FWVZL4K |
| AppLovin | consent | net::ERR_TOO_MANY_REDIRECTS (likely capture network) | https://b.applovin.com/v1/gcm/match?google_error=2 |
| Google Tag Manager | reload | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://www.googletagmanager.com/gtm.js?id=GTM-5FWVZL4K |
| Google Tag Manager | atc | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://www.googletagmanager.com/gtm.js?id=GTM-5FWVZL4K |

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
- Consent action: js_api — Shopify Customer Privacy (no visible banner)
- Screenshots: [01_initial](screenshots/01_initial.png) · [02_after_consent](screenshots/02_after_consent.png) · [03_reload](screenshots/03_reload.png) · [04_pdp](screenshots/04_pdp.png) · [05_atc](screenshots/05_atc.png)
