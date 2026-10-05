# Tracking & Martech Audit — Royal Aruba Aloe USA

**Site:** https://arubaaloe.com/en-en  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Google Tag Manager (GTM-K6FVJ4PB)  
**Consent platform:** None detected  

---

## 1. Executive Summary

Tag management: **Google Tag Manager (GTM-K6FVJ4PB)**. GA4 property: `G-W7K2V61PS4`. Container `GTM-K6FVJ4PB` scores **85/100** against best practice (1 failed, 3 warning checks). Tracking platforms (GA4 + ad pixels) score **91/100** on the events they actually received. The audit raised **3 P1**, **2 P2** and **6 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P1 | Advertising | Google tag loaded with an invalid ID (AW-Not_set) |
| P1 | GTM · Measurement | Not met: GA4 sent from one source only — GTM-K6FVJ4PB |
| P1 | Tracking · GA4 | Not met: GA4 — Page view sent once per load |
| P2 | Analytics | Same GA4 property in a Shopify app pixel and GTM |
| P2 | GTM · Ecommerce | Needs attention: GA4 ecommerce funnel coverage — GTM-K6FVJ4PB |
| P3 | Consent | 1 tracking script(s) held until consent |
| P3 | Consent | No consent banner shown to this (US) visitor |
| P3 | GTM · Measurement | Needs attention: Measurement ID in a variable, not hard-coded — GTM-K6FVJ4PB |
| P3 | GTM · Governance | Needs attention: No unused variables — GTM-K6FVJ4PB |
| P3 | Tracking · Meta | Needs attention: Meta — Add to cart sent once per cart add |
| P3 | Tracking · Stack | Needs attention: Stack — Third-party request volume |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** GA4 and Google Ads run through the **native Google & YouTube app**, Meta through the **native Facebook & Instagram app**, Klaviyo through its app embed. On top of that, the Anowave GTM app deploys **GTM-K6FVJ4PB**, a lean, well-built container (score 85) with full GA4 ecommerce and an Ads purchase conversion with value, order ID and enhanced conversions.
- **Biggest issue — two GA4 implementations:** the app and GTM both send to G-W7K2V61PS4, so every page view counts twice. Sessions and engagement are inflated and conversion rates understated.
- **Also:** a Google tag loads with the placeholder ID `AW-Not set`, so those hits go nowhere, and Meta AddToCart fired twice for one cart add.
- **Pitch angle:** "your reporting double-counts traffic" — pick one GA4 owner (the GTM build is richer; turn GA4 off in the Google app), fix the placeholder ID, add a US opt-out link. Quick, visible wins.
- _Capture: US network, Oct 5 2026, fresh browser, consent accepted → reload → PDP → add to cart → cart. Outside-in only (no account access)._
<!-- ANALYST_NOTES_END -->

---

## 3. Next Steps — Analyst Checks & Discovery Questions

_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks below take minutes from the outside, and the questions are for the discovery conversation._

**Analyst checks (no account access needed)**

- [ ] **Ecommerce:** Add one product to cart and confirm each platform records ONE add-to-cart (Meta fired twice in the capture) — _Tag Assistant / Meta Pixel Helper / TikTok Pixel Helper + DevTools → Network_
- [ ] **Google tag:** Find which route loads the placeholder ID (AW-Not_set) — search page source / Shopify app scripts for it — _View source + DevTools → Network (initiator column)_
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

### `GTM-K6FVJ4PB` — score 85/100 (✅ 14 · ⚠️ 3 · ❌ 1)

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ❌ | High | Measurement | GA4 sent from one source only | G-W7K2V61PS4 is configured in GTM and in the Shopify Google & YouTube app; page_view hits per page load: G-W7K2V61PS4×2. | Pick one owner: disable GA4 in the Shopify app (keep Ads/Merchant Center there) or remove the GTM GA4 tags. |
| ⚠️ | High | Ecommerce | GA4 ecommerce funnel coverage | Configured in GTM: begin_checkout, purchase, remove_from_cart, select_item, view_cart, view_item, view_item_list. Missing core: add_to_cart; missing recommended: add_shipping_info, add_payment_info. Split ownership: add… | Move the whole funnel to one owner (GTM or the app) and remove the other's GA4 events. |
| ⚠️ | Low | Measurement | Measurement ID in a variable, not hard-coded | 12 of 12 GA4 event tags hard-code the measurement ID. | Reference a Constant / Lookup Table variable so the ID changes in one place. |
| ⚠️ | Low | Governance | No unused variables | 6 variable(s) not referenced by any tag, trigger or variable: DLV - ecommerce.payment_type, DLV - ecommerce.shipping_tier, DLV - ecommerce.aw_feed_label, DLV - ecommerce.user_data.user_id, DLV - ecommerce.enhanced_conve… | Remove unused variables. |
| ✅ | High | Ecommerce | Ecommerce events carry items[] | All ecommerce event tags send items (dataLayer ecommerce object or items parameter). | — |
| ✅ | High | Ecommerce | Purchase has transaction_id, value, currency | purchase tag #51 sends transaction_id / value / currency. | — |
| ✅ | High | Google Ads | Conversion Linker present | 2 Ads/Floodlight tag(s); conversion linker tags: 1. | — |
| ✅ | High | Google Ads | Purchase conversion passes value, currency, order ID | Ads conversion #54 passes value, currency and order ID. | — |
| ✅ | High | Consent | Consent Mode defaults set before tags fire | Consent Mode default + update is set via gtag outside GTM (theme / CMP / Shopify app) before the container loads. | — |
| ✅ | Medium | Measurement | Single GA4 Google tag | GA4 Google tag IDs: G-W7K2V61PS4. | — |
| ✅ | Medium | Measurement | Google tag fires on Initialization / All Pages | Google tag fires on Initialization or Page View. | — |
| ✅ | Medium | Google Ads | Enhanced conversions configured | User-provided data configured on Ads conversions. | — |
| ✅ | Medium | Governance | Limited Custom HTML | 1 active Custom HTML tag(s) (6% of active tags). | — |
| ✅ | Medium | Performance | Tags firing on every page kept small | 4 tag(s) fire on every page load without filters; container 467.2 KB. | — |
| ✅ | Low | Governance | Paused tags cleaned up | 0 paused tag(s). | — |
| ✅ | Low | Governance | No orphan tags | 0 active tag(s) without a firing trigger. | — |
| ✅ | Low | Governance | Custom JavaScript variables kept lean | 0 Custom JavaScript variable(s). | — |
| ✅ | Low | Governance | No duplicate tags | No identical tags. | — |
| ℹ️ | Low | Google Ads | Dynamic remarketing (product feed) | 1 remarketing tag(s), no product-level parameters detected. | If running Shopping / PMax, send items with ecommerce events for dynamic remarketing. |
| ℹ️ | Low | Governance | Tag names published (naming convention auditable) | Tag names are not published in the container (normal); naming convention can't be audited from outside. | — |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **91/100** (✅ 22 · ⚠️ 2 · ❌ 1).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 86 | 9 | 0 | 1 | Shopify app: Google & YouTube ×26; GTM GTM-K6FVJ4PB ×1 | initial: (none)×1, page_view×2; reload: user_engagement×2, page_view×2; pdp: scroll×3, user_engagement×2, page_view×2, view_item×3; atc: view_cart×5, add_to_cart×1, user_engagement×2, page_view×2 |
| Google Ads | 100 | 4 | 0 | 0 | Shopify app: Google & YouTube ×4; GTM GTM-K6FVJ4PB ×3; Theme HTML (hard-coded) ×1 | initial: page_view×1; reload: page_view×1; pdp: page_view×1, conversion×3, remarketing×1; atc: page_view×1 |
| Meta | 93 | 6 | 1 | 0 | Shopify app: Meta (Facebook & Instagram) ×9 | initial: PageView×1; reload: PageView×1; pdp: PageView×1, ViewContent×1; atc: SubscribedButtonClick×1, AddToCart×2, PageView×1, ViewCart×1 |
| Klaviyo | 100 | 2 | 0 | 0 | Shopify app embed: klaviyo-email-marketing-sms ×112 | initial: (onsite.js loaded)×29; reload: (onsite.js loaded)×30; pdp: (onsite.js loaded)×30; atc: (onsite.js loaded)×23 |

### GA4 — 86/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ❌ | High | Page view sent once per load | Duplicates on one page load: G-W7K2V61PS4×2 (from Shopify app: Google & YouTube) | Remove the second source (app vs GTM vs hard-coded / custom pixel). |
| ✅ | Low | Single GA4 property | GA4 property: G-W7K2V61PS4. | — |
| ✅ | High | One implementation per property | G-W7K2V61PS4 <- GTM GTM-K6FVJ4PB, Shopify app: Google & YouTube | — |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (3×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (1×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: scroll, user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x26; GTM GTM-K6FVJ4PB x1. | — |

### Google Ads — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 1 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x4; GTM GTM-K6FVJ4PB x3; Theme HTML (hard-coded) x1. | — |

### Meta — 93/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | Add to cart sent once per cart add | Sent 2× to 2466451116920362 for a single cart add. | Find the second trigger (app + theme script, or two listeners) and keep one. |
| ✅ | Low | Single Meta pixel | Meta pixel: 2466451116920362. | — |
| ✅ | High | Page view sent once per load | 2466451116920362×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (2×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 7 of 7 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Meta (Facebook & Instagram) x9. | — |

### Klaviyo — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Medium | Onsite tracking (klaviyo.js) loaded | klaviyo.js loads. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: __kla_id. | — |
| ℹ️ | Medium | Viewed Product tracked (browse abandonment) | No Viewed Product event (only identified profiles are tracked — anonymous visitors expected to show none). | Confirm Viewed Product is enabled in the Klaviyo Shopify integration. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app embed: klaviyo-email-marketing-sms x112. | — |

### Stack — 75/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Low | Third-party request volume | 1131 third-party requests across the visit (20 identified platforms). | Audit apps/pixels that don't earn their weight. |
| ✅ | Low | Session-replay tools | 1: Contentsquare. | — |
| ℹ️ | Low | Ad platforms in use | 5: Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel, TikTok Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Container Deep Dive — `GTM-K6FVJ4PB`

| Tag type | Active | Paused |
|---|---|---|
| GA4 Event | 12 | 0 |
| Google Ads Remarketing | 1 | 0 |
| Google Tag (GA4/Ads config) | 1 | 0 |
| Google Ads Conversion | 1 | 0 |
| Conversion Linker | 1 | 0 |
| Custom Template | 1 | 0 |
| Custom HTML | 1 | 0 |

**Custom templates:**

| Template | Vendor (inferred) | Tags using it | Injects |
|---|---|---|---|
| `__cvt_T9BM6` | — | 1 | https://t.contentsquare.net/* |

**Custom HTML tags:**

| Tag | Status | Vendors / IDs | Fires on | Preview |
|---|---|---|---|---|
| #55 | active | Contentsquare | {{Event}} equals "gtm.js" | <script data-gtmsrc="https://t.contentsquare.net/uxa/89921e32aee86.js" type="text/gtmscri… |

<details><summary>All active tags with firing conditions</summary>

| Tag | Type | IDs / event | Fires on | Consent |
|---|---|---|---|---|
| #40 | GA4 Event | view_cart | {{Event}} equals "add_to_cart" | — |
| #41 | GA4 Event | remove_from_cart | {{Event}} equals "remove_from_cart" | — |
| #42 | GA4 Event | add_to_wishlist | {{Event}} equals "add_to_wishlist" | — |
| #43 | GA4 Event | add_to_compare | {{Event}} equals "add_to_compare" | — |
| #44 | GA4 Event | view_item | {{Event}} equals "view_item" | — |
| #45 | GA4 Event | view_item_list | {{Event}} equals "view_item_list" | — |
| #46 | GA4 Event | select_item | {{Event}} equals "select_item" | — |
| #47 | GA4 Event | view_promotion | {{Event}} equals "view_promotion" | — |
| #48 | GA4 Event | select_promotion | {{Event}} equals "select_promotion" | — |
| #49 | GA4 Event | begin_checkout | {{Event}} equals "begin_checkout" | — |
| #50 | GA4 Event | view_cart | {{Event}} equals "view_cart" | — |
| #51 | GA4 Event | purchase | {{Event}} equals "purchase" | — |
| #52 | Google Ads Remarketing | {"conversionId": "Not set", "conversionLabel": "Not set"} | {{Event}} equals "fireRemarketingTag" | — |
| #53 | Google Tag (GA4/Ads config) | {"tagId": "G-W7K2V61PS4"} | {{Event}} equals "gtm.init" | — |
| #54 | Google Ads Conversion | {"conversionId": "Not set", "conversionLabel": "Not set"} | {{Event}} equals "purchase" | — |
| #56 | Conversion Linker | {} | {{Event}} equals "gtm.init" | — |
| #58 | Custom Template | {} | {{Event}} equals "gtm.js" | — |

</details>

**Reconstructed export:** `containers/GTM-K6FVJ4PB.export.json` — 18 tags, 15 triggers, 23 variables; template source missing for cvt_T9BM6

**Custom dataLayer events used as triggers (13):** `add_to_cart`, `add_to_compare`, `add_to_wishlist`, `begin_checkout`, `fireRemarketingTag`, `purchase`, `remove_from_cart`, `select_item`, `select_promotion`, `view_cart`, `view_item`, `view_item_list`, `view_promotion`

---

### 6.2 Google Tag Settings — `AW-Not_set`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Remarketing / conversion page view | {"containerId": "{{Container ID #1}}"} |
| Google Ads destination | {"destinationId": "{{Container ID #1}}", "enableVariablesInDestinationId": false} |

---

### 6.3 Google Tag Settings — `G-W7K2V61PS4`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| __ogt_ga_send | {"value": true} |
| Unwanted referrals list | {"includeConditions": ["myshopify\\.com"]} |
| Custom session timeout | {"sessionMinutes": 30, "sessionHours": 0} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Product settings | {"instanceDestinationId": "G-W7K2V61PS4", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-W7K2V61PS4"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced measurement: form interactions | {"includeParams": true, "instanceDestinationId": "G-W7K2V61PS4"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-W7K2V61PS4"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-W7K2V61PS4"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-W7K2V61PS4"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-W7K2V61PS4"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-W7K2V61PS4"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-W7K2V61PS4"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-W7K2V61PS4", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-W7K2V61PS4", "sessionDuration": 0} |

---

### 6.4 Google Tag Settings — `GT-5DCDJ5B`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| __dest_mc | {"ignoreDupeGtagConfigCalls": true, "destinationId": "MC-0DLZZ21F1B", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "MC-0DLZZ21F1B"} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| GA4 | `G-W7K2V61PS4` | GTM-K6FVJ4PB (container) |
| Google Ads | `AW-Not set`, `AW-Not set/Not set` | GTM-K6FVJ4PB (container) |
| Meta Pixel | `2466451116920362` | network |
| TikTok Pixel | `D49KTTRC77U6GUHHPNM0` | network |
| Google Analytics 4 | `G-W7K2V61PS4` | network |
| Klaviyo | `SDuShc` | network |
| Shopify app pixel: Klaviyo | {"accountID": "270971"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shopId": "arubaaloe-2.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: Klaviyo | {"accountID": "W7TqgQ", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `G-W7K2V61PS4`, `GTM-K6FVJ4PB` | Shopify web pixel |
| Shopify app pixel: unknown app | {"businessId": "D0F0B6F379C715BE37F5CDD9", "environment": "production", "debug": "false"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"subdomain": "arubaaloe-2"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"siteId": "wMUCLHeHk1zTKubk"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shop": "arubaaloe-2.myshopify.com", "collect_url": "https://collect.bogos.io/collect", "product_bundles_data": "[]"} | Shopify web pixel |
| Shopify app pixel: TikTok | {"pixelCode": "D49KTTRC77U6GUHHPNM0"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"webPixelName": "Judge.me"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"botID": "79x5wrcwy3st2vp4", "octaneDomain": "https://app.octaneai.com", "octaneNewDomain": "https://app2.octaneai.com… | Shopify web pixel |
| Shopify app pixel: unknown app | {"accountID": "arubaaloe-2.myshopify.com", "environment": "production", "apiURL": "https://api.quizkitapp.com"} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `G-W7K2V61PS4` | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "2466451116920362", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Klaviyo | `SDuShc` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://arubaaloe.com/en-en/products/spcalo12oz · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item_list` | ✅ | — |
| `select_item` | ✅ | — |
| `view_item` | ✅ | ✅ |
| `add_to_cart` | ✅ | ✅ |
| `remove_from_cart` | ✅ | — |
| `view_cart` | ✅ | ✅ |
| `begin_checkout` | ✅ | — |
| `purchase` | ✅ | — |
| `view_promotion` | ✅ | — |
| `select_promotion` | ✅ | — |
| `add_to_wishlist` | ✅ | — |

_Checkout and purchase events cannot be observed without placing an order; container configuration is listed instead._

---

## 9. Consent & Privacy

| Check | Result |
|---|---|
| CMP detected | None |
| Banner action taken by audit | js_api — Shopify Customer Privacy (no visible banner) |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "yes", "analytics": "yes", "preferences": "yes", "sale_of_data": "yes"} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": true}, "analytics_storage": {"default": true, "update": true}, "ad_user_data": {"default": true, "update": true}, "ad_personalization": {"default": true, "update": true}, "security_storage": {"default": false, "update": true}, "functionality_storage": {"de… |
| Tracking vendors firing before consent | Campaign Manager 360 / Floodlight, Contentsquare, Google Ads, Google Analytics 4, Google Merchant Center, Meta Pixel, TikTok Pixel |
| Scripts held until consent (text/plain, data-consent…) | (inline) [ignore], Shopify CDN [ignore] |
| Banner still visible after accept + reload | no |

_Returning visit: the persistent browser profile already held this site's cookies/consent, so the `initial` phase reflects stored consent, not a first visit (re-run with `--fresh` for that)._

**Consent configuration inside GTM:**

| Container | Consent types referenced | Consent templates | Tags with extra consent checks | CMP hints |
|---|---|---|---|---|
| `GTM-K6FVJ4PB` | — | — | 0 / 18 | — |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-W7K2V61PS4` | initial | (no event name)×1, page_view×2 | `G111` |
| GA4 `G-W7K2V61PS4` | reload | user_engagement×2, page_view×2 | `G111` |
| GA4 `G-W7K2V61PS4` | pdp | scroll×3, user_engagement×2, page_view×2, view_item×3 | `G111` |
| GA4 `G-W7K2V61PS4` | atc | view_cart×5, add_to_cart×1, user_engagement×2, page_view×2 | `G111` |
| Meta `2466451116920362` | atc | PageView×1, ViewCart×1 | — |

**dataLayer pushes observed:**

- `initial`: gtag:consent:default, gtag:consent:update, cookieConsentEssentialGranted, cookieConsentAnalyticsGranted, cookieConsentMarketingGranted, cookieConsentPersonalization, cookieConsentPreferencesGranted, cookieConsentUserdata, gtm.js, gtm.dom, visitor_info, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-W7K2V61PS4, gtag:c…
- `reload`: gtag:consent:default, gtag:consent:update, cookieConsentEssentialGranted, cookieConsentAnalyticsGranted, cookieConsentMarketingGranted, cookieConsentPersonalization, cookieConsentPreferencesGranted, cookieConsentUserdata, gtm.js, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-W7K2V61PS4, gtag:config:GT-5DCDJ5B, gtag:…
- `pdp`: gtag:consent:default, gtag:consent:update, cookieConsentEssentialGranted, cookieConsentAnalyticsGranted, cookieConsentMarketingGranted, cookieConsentPersonalization, cookieConsentPreferencesGranted, cookieConsentUserdata, gtm.js, view_item, fireRemarketingTag, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-W7K2V61PS4…
- `atc`: gtag:consent:default, gtag:consent:update, cookieConsentEssentialGranted, cookieConsentAnalyticsGranted, cookieConsentMarketingGranted, cookieConsentPersonalization, cookieConsentPreferencesGranted, cookieConsentUserdata, gtm.js, view_item, fireRemarketingTag, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-W7K2V61PS4…

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 2140930113 | APP | Klaviyo | — | {"accountID": "270971"} |
| 2073722945 | APP | — | ANALYTICS, MARKETING | {"shopId": "arubaaloe-2.myshopify.com"} |
| 1884094529 | APP | Klaviyo | ANALYTICS, MARKETING | {"accountID": "W7TqgQ", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} |
| 1736048705 | APP | Google & YouTube | ANALYTICS | {"accountId":"GTM-K6FVJ4PB","shopId":"1863936","measurementId":"G-W7K2V61PS4","enableServerSideTracking":"{\"enable\":0… |
| 1563230273 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"businessId": "D0F0B6F379C715BE37F5CDD9", "environment": "production", "debug": "false"} |
| 1523875905 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"subdomain": "arubaaloe-2"} |
| 1523679297 | APP | — | ANALYTICS | {"siteId": "wMUCLHeHk1zTKubk"} |
| 1520664641 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"shop": "arubaaloe-2.myshopify.com", "collect_url": "https://collect.bogos.io/collect", "product_bundles_data": "[]"} |
| 1443201089 | APP | TikTok | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixelCode": "D49KTTRC77U6GUHHPNM0"} |
| 765231169 | APP | — | ANALYTICS | {"webPixelName": "Judge.me"} |
| 613253185 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"botID": "79x5wrcwy3st2vp4", "octaneDomain": "https://app.octaneai.com", "octaneNewDomain": "https://app2.octaneai.com… |
| 613220417 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"accountID": "arubaaloe-2.myshopify.com", "environment": "production", "apiURL": "https://api.quizkitapp.com"} |
| 321454145 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"G-W7K2V61PS4\",\"GT-5DCDJ5B\"],\"target_country\":\"US\",\"gtag_events\":[{\"type\":\… |
| 131661889 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "2466451116920362", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} |
| 126746689 | CUSTOM | — | ANALYTICS, MARKETING | — |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `GTM-K6FVJ4PB` | GTM | 3 | 467.2 KB | reload | googletagmanager.com | 18 | 0 | 29 | 15 |
| `AW-Not_set` | GTAG | 1 | None KB | — | googletagmanager.com | 4 | 0 | 5 | 3 |
| `G-W7K2V61PS4` | GTAG | 2 | 573.5 KB | reload | googletagmanager.com | 20 | 0 | 6 | 4 |
| `GT-5DCDJ5B` | GTAG | 1 | 434.9 KB | reload | googletagmanager.com | 7 | 0 | 4 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `AW-Not set`, `G-W7K2V61PS4`, `GT-5DCDJ5B`, `GTM-K6FVJ4PB`
- GTM IDs referenced in page HTML: `GTM-K6FVJ4PB`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Tag Manager | `GTM-K6FVJ4PB` | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |
| Google tag (gtag.js) | — | 16 | initial:4, reload:4, pdp:4, atc:4 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-W7K2V61PS4` | 24 | initial:3, reload:4, pdp:9, atc:8 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 2 | initial:1, atc:1 | 0 |
| Google Ads | — | 8 | initial:1, reload:1, pdp:5, atc:1 | 0 |
| Google Merchant Center | — | 7 | initial:1, reload:2, pdp:2, atc:2 | 0 |
| Meta Pixel | `2466451116920362` | 17 | initial:3, reload:3, pdp:4, atc:7 | 0 |
| TikTok Pixel | `D49KTTRC77U6GUHHPNM0` | 8 | initial:2, reload:2, pdp:2, atc:2 | 0 |

### Session replay / UX

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Contentsquare | — | 18 | initial:5, reload:4, pdp:5, atc:4 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Klaviyo | `SDuShc` | 131 | initial:34, reload:38, pdp:33, atc:26 | 0 |
| Privy | — | 6 | initial:2, reload:2, pdp:2 | ⚠️ 3 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Judge.me | — | 30 | initial:8, reload:8, pdp:8, atc:6 | 0 |
| Trustpilot | — | 30 | initial:12, reload:12, pdp:6 | 0 |

### Support / chat

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Gorgias | — | 84 | initial:28, reload:28, pdp:28 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 8 | initial:2, reload:1, pdp:4, atc:1 | 0 |
| Shopify | — | 53 | initial:12, consent:1, reload:6, pdp:16, atc:18 | 0 |
| Shopify Analytics (Monorail) | — | 51 | initial:2, consent:1, reload:1, pdp:11, atc:36 | 0 |
| Shopify CDN | — | 491 | initial:131, reload:115, pdp:175, atc:70 | 0 |

### Payments / BNPL

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| PayPal | — | 11 | atc:11 | 0 |

### Monitoring

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Bugsnag | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`tiktok.nfcube.com` (14), `api-discounty.hengam.io` (7), `media.9gtb.com` (6), `p16-common-sign.tiktokcdn-eu.com` (6), `d2wy8f7a9ursnm.cloudfront.net` (5), `cdn.nfcube.com` (5), `play.google.com` (5), `sapi.negate.io` (4), `static-fg.aov.ai` (4), `static-utils.aov.ai` (4), `anowave.ai` (4), `slide.upcart.app` (3), `pc-quiz.s3.us-east-2.amazonaws.com` (3), `backinstock.useamp.com` (3), `extensions.shopifycdn.com` (3), `d3k81ch9hvuctc.cloudfront.net` (3), `pay.google.com` (3), `www.googletagmanager.com` (1)

</details>

---

## 14. Findings & Recommendations

### P1 — Fix now

**[Advertising] Google tag loaded with an invalid ID (AW-Not_set)**  
gtag.js was requested for `AW-Not_set` — a tag is configured with a placeholder / unset ID, so its hits go nowhere.  
_Recommendation:_ Find the tag (GTM Google Tag / Ads tag or theme snippet) using this ID and set the real ID or remove it.

**[GTM · Measurement] Not met: GA4 sent from one source only — GTM-K6FVJ4PB**  
G-W7K2V61PS4 is configured in GTM and in the Shopify Google & YouTube app; page_view hits per page load: G-W7K2V61PS4×2. Why it matters: Double tagging inflates sessions, page views and revenue, and breaks conversion rates.  
_Recommendation:_ Pick one owner: disable GA4 in the Shopify app (keep Ads/Merchant Center there) or remove the GTM GA4 tags.

**[Tracking · GA4] Not met: GA4 — Page view sent once per load**  
Duplicates on one page load: G-W7K2V61PS4×2 (from Shopify app: Google & YouTube) Why it matters: Double page views inflate traffic and deflate conversion rates; for ad pixels they distort optimisation.  
_Recommendation:_ Remove the second source (app vs GTM vs hard-coded / custom pixel).

### P2 — Address within 30 days

**[Analytics] Same GA4 property in a Shopify app pixel and GTM**  
G-W7K2V61PS4 is configured both in the Shopify Google & YouTube app and in GTM.  
_Recommendation:_ Keep a single source per property or events will double count.

**[GTM · Ecommerce] Needs attention: GA4 ecommerce funnel coverage — GTM-K6FVJ4PB**  
Configured in GTM: begin_checkout, purchase, remove_from_cart, select_item, view_cart, view_item, view_item_list. Missing core: add_to_cart; missing recommended: add_shipping_info, add_payment_info. Split ownership: add_to_cart is sent by Shopify Google & YouTube app, not GTM. Why it matters: Gaps or split ownership break funnel reports and double-count shared events.  
_Recommendation:_ Move the whole funnel to one owner (GTM or the app) and remove the other's GA4 events.

### P3 — Clean-up / informational

**[Consent] 1 tracking script(s) held until consent**  
Parked as non-executable until the CMP grants consent: Shopify CDN (ignore).  
_Recommendation:_ Positive if intentional; make sure the banner is actually shown to the visitors it applies to, otherwise these tags never fire.

**[Consent] No consent banner shown to this (US) visitor**  
5 ad platform(s) fire without a banner — normal for US opt-out. Geo-targeted CMP present in the page: Anowave Cookie Consent (Shopify app). No US opt-out link (Do Not Sell / Your Privacy Choices) found.  
_Recommendation:_ Confirm EU/UK visitors get an opt-in banner and that the US opt-out link + GPC actually suppress ad pixels (Shopify Customer Privacy sale_of_data).

**[GTM · Measurement] Needs attention: Measurement ID in a variable, not hard-coded — GTM-K6FVJ4PB**  
12 of 12 GA4 event tags hard-code the measurement ID. Why it matters: Hard-coded IDs make property migrations and staging setups error-prone.  
_Recommendation:_ Reference a Constant / Lookup Table variable so the ID changes in one place.

**[GTM · Governance] Needs attention: No unused variables — GTM-K6FVJ4PB**  
6 variable(s) not referenced by any tag, trigger or variable: DLV - ecommerce.payment_type, DLV - ecommerce.shipping_tier, DLV - ecommerce.aw_feed_label, DLV - ecommerce.user_data.user_id, DLV - ecommerce.enhanced_conversion_data, User-Provided Data #23 Why it matters: Clutter hides what actually drives data.  
_Recommendation:_ Remove unused variables.

**[Tracking · Meta] Needs attention: Meta — Add to cart sent once per cart add**  
Sent 2× to 2466451116920362 for a single cart add. Why it matters: Double add-to-cart events inflate funnel rates and remarketing audience signals.  
_Recommendation:_ Find the second trigger (app + theme script, or two listeners) and keep one.

**[Tracking · Stack] Needs attention: Stack — Third-party request volume**  
1131 third-party requests across the visit (20 identified platforms). Why it matters: Tag weight slows pages, which costs conversion rate.  
_Recommendation:_ Audit apps/pixels that don't earn their weight.

<details><summary>Failed requests</summary>

| Vendor | Phase | Status / error | URL |
|---|---|---|---|
| Privy | initial | net::ERR_FAILED (likely capture network) | https://api.privy.com/businesses/D0F0B6F379C715BE37F5CDD9/campaigns.json?s=j&l=https%3A%2F%2Farubaa… |
| Privy | reload | net::ERR_FAILED (likely capture network) | https://api.privy.com/businesses/D0F0B6F379C715BE37F5CDD9/campaigns.json?s=j&l=https%3A%2F%2Farubaa… |
| Privy | pdp | net::ERR_FAILED (likely capture network) | https://api.privy.com/businesses/D0F0B6F379C715BE37F5CDD9/campaigns.json?s=j&l=https%3A%2F%2Farubaa… |

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

_Limitations: one product page per site, no checkout/purchase; server-side containers are only visible through their client-side traffic. Consent banners and pixels can vary by visitor country; connection-level errors (resets, SSL, ORB) are shown but not treated as site faults, as they often come from the capture network. Capture location signals: store redirected to /en-en market_

## Appendix — Capture Verification

_Supplemental: confirms the capture saw the site as a consenting visitor would._

- Coverage check: ✅ passed
- Returning visit: the persistent browser profile already held this site's consent, so `initial` reflects stored consent (re-run with `--fresh` for a first-visit view).
- Consent action: js_api — Shopify Customer Privacy (no visible banner)
- Screenshots: [01_initial](screenshots/01_initial.png) · [02_after_consent](screenshots/02_after_consent.png) · [03_reload](screenshots/03_reload.png) · [04_pdp](screenshots/04_pdp.png) · [05_atc](screenshots/05_atc.png)
