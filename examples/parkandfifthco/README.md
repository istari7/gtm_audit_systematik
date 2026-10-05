# Tracking & Martech Audit — Park & Fifth Clothing Co

**Site:** https://parkandfifthco.com  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Google Tag Manager (GTM-PWXWHZZ)  
**Consent platform:** None detected  

---

## 1. Executive Summary

Tag management: **Google Tag Manager (GTM-PWXWHZZ)**. GA4 property: `G-1NHWMSMD59`. Container `GTM-PWXWHZZ` scores **79/100** against best practice (1 failed, 1 warning checks). Tracking platforms (GA4 + ad pixels) score **80/100** on the events they actually received. The audit raised **6 P1**, **3 P2** and **5 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P1 | Consent | No consent banner or US opt-out mechanism |
| P1 | GTM · Deployment | Not met: Custom pixel overrides page_location — GTM-PWXWHZZ |
| P1 | Tracking · GA4 | Not met: GA4 — One implementation per property |
| P1 | Tracking · GA4 | Not met: GA4 — Page view sent once per load |
| P1 | Tracking · GA4 | Not met: GA4 — page_location is the real page URL |
| P1 | Tracking · Microsoft Ads | Not met: Microsoft Ads — Page view sent once per load |
| P2 | Tracking · GA4 | Needs attention: GA4 — Single deployment route |
| P2 | Tracking · Google Ads | Needs attention: Google Ads — Single deployment route |
| P2 | Tracking · Microsoft Ads | Needs attention: Microsoft Ads — Single deployment route |
| P3 | Governance | GA4 data sent outside GTM |
| P3 | GTM · Governance | Needs attention: No unused variables — GTM-PWXWHZZ |
| P3 | Tracking · Google Ads | Needs attention: Google Ads — Dynamic remarketing sends product IDs |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** Meta, TikTok, Pinterest and Klaviyo are clean native app integrations. GA4 G-1NHWMSMD59 comes from the Google app **and** custom pixel #21037220 (which also runs GTM-PWXWHZZ); Google Ads comes from that custom pixel plus hard-coded theme code; Microsoft UET comes from the native app **and** a theme inline script (two UET IDs).
- **Biggest issue — GA4 is unreliable:** three page views per page load, and custom-pixel hits record the `web-pixels@…` sandbox URL as the page, polluting every page and landing-page report.
- **Also:** Microsoft counts page loads twice; Google Ads hits carry no product IDs (no dynamic remarketing); no consent banner or US opt-out link.
- **Pitch angle:** "your GA4 overstates traffic about 3×" — remove the custom-pixel GA4 (or fix page_location), drop the duplicate UET and theme snippets, and add privacy basics. High-impact, low-effort.
- _Capture: US network, Oct 5 2026, fresh browser, consent accepted → reload → PDP → add to cart → cart. Outside-in only (no account access)._
<!-- ANALYST_NOTES_END -->

---

## 3. Next Steps — Analyst Checks & Discovery Questions

_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks below take minutes from the outside, and the questions are for the discovery conversation._

**Analyst checks (no account access needed)**

- [ ] **Google Ads:** Confirm the hard-coded Google Ads snippet in the theme (view source) — it runs alongside other routes (Theme HTML (hard-coded), Shopify custom pixel #21037220, Theme script) — _View source / DevTools → Network → Initiator_
- [ ] **Microsoft Ads:** Confirm the hard-coded Microsoft Ads snippet in the theme (view source) — it runs alongside other routes (Theme inline script, Shopify app: Microsoft Ads) — _View source / DevTools → Network → Initiator_
- [ ] **Consent:** Visit from an EU/UK VPN: does a banner appear, and do ad pixels wait for consent? — _Browser via EU VPN + DevTools → Network_
- [ ] **Consent:** Check the footer for a 'Your Privacy Choices / Do Not Sell or Share' link (none found on the homepage HTML) — _Site footer, privacy policy_

**Discovery questions for the prospect**

- **Purchase tracking:** Do GA4 revenue and Google Ads / Meta purchase counts reconcile with Shopify orders (a gap above ~10% usually means a tracking problem)?
- **Ownership:** GA4, Google Ads, Microsoft Ads are fed by more than one route (GA4: Shopify app, Shopify custom pixel; Google Ads: Shopify custom pixel, Theme; Microsoft Ads: Shopify app, Theme). Who manages each, and which one is meant to be the source of truth?
- **Microsoft Ads:** Are all of these UET tags still in use (any agency or legacy accounts)? 343239094, 343240572.
- **Meta:** Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), and what Event Match Quality do Purchase events get?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?
- **Email / SMS:** Are browse- and cart-abandonment flows live in Klaviyo, and are Viewed Product / Added to Cart metrics recording?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### `GTM-PWXWHZZ` — score 79/100 (✅ 8 · ⚠️ 1 · ❌ 1)

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ❌ | High | Deployment | Custom pixel overrides page_location | GA4 hits from the sandbox report the web-pixels sandbox URL as page_location. | Set page_location/page_title/page_referrer from event.context.document in the pixel. |
| ⚠️ | Low | Governance | No unused variables | 6 variable(s) not referenced by any tag, trigger or variable: DLV - pinterest_quantity, DLV - pinterest_eventData, DLV - pinterest_orderValue, DLV - event, DLV - pinterest_order_id, DLV - pinterest_currency | Remove unused variables. |
| ✅ | High | Consent | Consent Mode defaults set before tags fire | Consent Mode default is set via gtag outside GTM (theme / CMP / Shopify app) before the container loads. | — |
| ✅ | Medium | Governance | Limited Custom HTML | 0 active Custom HTML tag(s) (0% of active tags). | — |
| ✅ | Medium | Performance | Tags firing on every page kept small | 0 tag(s) fire on every page load without filters; container 346.0 KB. | — |
| ✅ | Medium | Deployment | GTM in Shopify custom pixel: DOM-based triggers avoided | Container runs inside the Shopify Customer Events sandbox; 0 click/scroll/visibility/form listener(s) configured. | — |
| ✅ | Low | Governance | Paused tags cleaned up | 2 paused tag(s). | — |
| ✅ | Low | Governance | No orphan tags | 0 active tag(s) without a firing trigger. | — |
| ✅ | Low | Governance | Custom JavaScript variables kept lean | 2 Custom JavaScript variable(s). | — |
| ✅ | Low | Governance | No duplicate tags | No identical tags. | — |
| ℹ️ | High | Measurement | GA4 managed in GTM | No GA4 Google tag or GA4 event tags in the container. GA4 hits observed: G-1NHWMSMD59. | Keep one owner for GA4. If GA4 comes from the Shopify Google & YouTube app, leave GTM out of GA4 to avoid double counting; otherwise implement GA4 in GTM. |
| ℹ️ | High | Ecommerce | GA4 ecommerce events in GTM | No GA4 event tags in GTM. GA4 ecommerce is sent by the Shopify Google & YouTube app. | — |
| ℹ️ | Low | Governance | Tag names published (naming convention auditable) | Tag names are not published in the container (normal); naming convention can't be audited from outside. | — |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **80/100** (✅ 37 · ⚠️ 6 · ❌ 4).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 56 | 7 | 1 | 3 | Shopify app: Google & YouTube ×21; Shopify custom pixel #21037220 ×9; Theme HTML (hard-coded) ×5 | initial: user_engagement×2, page_view×3, scroll×2; reload: user_engagement×2, page_view×3, scroll×2; pdp: user_engagement×2, page_view×3, product_page×3, scroll×2, view_item×1, form_start×1; atc: add_to_cart×1, user_engagement×2, page_view×3, scroll×2, view_c… |
| Google Ads | 77 | 4 | 2 | 0 | Theme HTML (hard-coded) ×17; Shopify custom pixel #21037220 ×16; Theme script ×1 | initial: gtag.config×6, page_view×2; reload: gtag.config×6, page_view×2; pdp: gtag.config×6, page_view×2, form_start×3; atc: gtag.config×6, page_view×2 |
| Meta | 100 | 7 | 0 | 0 | Shopify app: Meta (Facebook & Instagram) ×6 | initial: PageView×1; reload: PageView×1; pdp: PageView×1, ViewContent×1; atc: AddToCart×1, PageView×1 |
| TikTok | 100 | 7 | 0 | 0 | Shopify app: TikTok ×6 | initial: Pageview×1; reload: Pageview×1; pdp: Pageview×1, ViewContent×1; atc: AddToCart×1, Pageview×1 |
| Pinterest | 100 | 6 | 0 | 0 | Shopify app: Pinterest ×10 | initial: init×1, PageVisit×1; reload: init×1, PageVisit×1; pdp: init×1, PageVisit×2; atc: AddToCart×1, init×1, PageVisit×1 |
| Microsoft Ads | 54 | 3 | 2 | 1 | Theme inline script ×17; Shopify app: Microsoft Ads ×6 | initial: pageLoad×4, ?×2; reload: ?×2, pageLoad×3; pdp: ?×2, pageLoad×3, view_item×1; atc: add_to_cart×1, ?×2, pageLoad×3 |
| Klaviyo | 100 | 2 | 0 | 0 | Shopify app embed: klaviyo-email-marketing-sms ×110 | initial: (onsite.js loaded)×35; reload: (onsite.js loaded)×30; pdp: (onsite.js loaded)×22; atc: (onsite.js loaded)×23 |

### GA4 — 56/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ❌ | High | One implementation per property | G-1NHWMSMD59 <- Shopify app: Google & YouTube x21, Shopify custom pixel #21037220 x9, Theme HTML (hard-coded) x5 | Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM carries a richer setup (then switch GA4 off in the app). |
| ❌ | High | Page view sent once per load | Duplicates on one page load: G-1NHWMSMD59×3 (from Shopify app: Google & YouTube, Shopify custom pixel #21037220, Theme HTML (hard-coded)) | Remove the second source (app vs GTM vs hard-coded / custom pixel). |
| ❌ | High | page_location is the real page URL | Sandbox URL recorded as page_location for G-1NHWMSMD59. | In the custom pixel set page_location/page_title from event.context.document. |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Shopify app: Google & YouTube x21; Shopify custom pixel #21037220 x9; Theme HTML (hard-coded) x5. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | Low | Single GA4 property | GA4 property: G-1NHWMSMD59. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (1×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: scroll, user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |

### Google Ads — 77/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | Dynamic remarketing sends product IDs | No product IDs on Ads hits from the product page or cart. | Send items (id matching the Merchant Center feed) with view_item / add_to_cart. |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Theme HTML (hard-coded) x17; Shopify custom pixel #21037220 x16; Theme script x1; Shopify app: Google & YouTube x1. | Consolidate to one deployment route per platform. |
| ✅ | Low | Single Google Ads account | Google Ads account: AW-683612000. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 8 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |

### Meta — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Meta pixel | Meta pixel: 1440135562842987. | — |
| ✅ | High | Page view sent once per load | 1440135562842987×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 6 of 6 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Meta (Facebook & Instagram) x6. | — |

### TikTok — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single TikTok pixel | TikTok pixel: C8TQU8I0VTGU7LHNSGO0. | — |
| ✅ | High | Page view sent once per load | C8TQU8I0VTGU7LHNSGO0×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | event_id for Events API dedupe | event_id present. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ttp. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: TikTok x6. | — |

### Pinterest — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Pinterest tag | Pinterest tag: 2614154625030. | — |
| ✅ | High | Page view sent once per load | 2614154625030×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | PageVisit sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _pin_unauth. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Pinterest x10. | — |

### Microsoft Ads — 54/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ❌ | High | Page view sent once per load | Duplicates on one page load: 343240572×2 (from Shopify app: Microsoft Ads, Theme inline script) | Remove the second source (app vs GTM vs hard-coded / custom pixel). |
| ⚠️ | Medium | Single UET tag | 2 UET tags receive data: 343239094, 343240572. | Confirm each is owned and in use; retire leftovers from agencies or old accounts. |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Theme inline script x17; Shopify app: Microsoft Ads x6. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | Low | Product IDs for dynamic remarketing | ecomm_prodid / items present. | — |
| ✅ | Low | UET Consent Mode signal | asc=G. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _uetsid, _uetvid. | — |

### Klaviyo — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Medium | Onsite tracking (klaviyo.js) loaded | klaviyo.js loads. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: __kla_id. | — |
| ℹ️ | Medium | Viewed Product tracked (browse abandonment) | No Viewed Product event (only identified profiles are tracked — anonymous visitors expected to show none). | Confirm Viewed Product is enabled in the Klaviyo Shopify integration. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app embed: klaviyo-email-marketing-sms x110. | — |

### Stack — 75/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Low | Third-party request volume | 1391 third-party requests across the visit (19 identified platforms). | Audit apps/pixels that don't earn their weight. |
| ✅ | Low | Session-replay tools | 1: Microsoft Clarity. | — |
| ℹ️ | Low | Ad platforms in use | 6: Campaign Manager 360 / Floodlight, Google Ads, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Container Deep Dive — `GTM-PWXWHZZ`

| Tag type | Active | Paused |
|---|---|---|
| Google Tag (GA4/Ads config) | 0 | 1 |
| Custom HTML | 0 | 1 |
| Pinterest Tag | 1 | 0 |

**Custom HTML tags:**

| Tag | Status | Vendors / IDs | Fires on | Preview |
|---|---|---|---|---|
| #17 | paused | — | {{Event}} equals "product_added_to_cart" | — |

<details><summary>All active tags with firing conditions</summary>

| Tag | Type | IDs / event | Fires on | Consent |
|---|---|---|---|---|
| #24 | Pinterest Tag | {"tagId": "2614154625030"} | {{Event}} equals "checkout_completed" AND {{Custom JavaScript #2}} contains "Swatch" | — |

</details>

**Reconstructed export:** `containers/GTM-PWXWHZZ.export.json` — 3 tags, 7 triggers, 13 variables

**Custom dataLayer events used as triggers (5):** `checkout_completed`, `collection_viewed`, `product_added_to_cart`, `product_viewed`, `search_submitted`

---

### 6.2 Google Tag Settings — `AW-683612000`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Cross-domain measurement | {"rules": ["^parkandfifthco\\.com$"]} |
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-683612000"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": true, "manualPhoneEnabled": false, "manualAddressEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSe… |
| Product settings | {"instanceDestinationId": "G-1NHWMSMD59", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-1NHWMSMD59"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced conversions settings | {"instanceDestinationId": "G-1NHWMSMD59"} |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-1NHWMSMD59"} |
| Enhanced measurement: form interactions | {"includeParams": true, "instanceDestinationId": "G-1NHWMSMD59"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-1NHWMSMD59"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-1NHWMSMD59"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-1NHWMSMD59"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-1NHWMSMD59"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-1NHWMSMD59"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Create-event rules | {"eventName": "appointment_booking_pageview", "isCopy": false, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "appointment_book… |
| Create-event rules | {"eventName": "appointment_booking_pageview", "isCopy": false, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "appointment_book… |
| Create-event rules | {"eventName": "product_page", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "product_page", "merge_source_even… |
| Create-event rules | {"eventName": "collection_view", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "collection_view", "merge_sourc… |
| Create-event rules | {"eventName": "view_product", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "view_product", "merge_source_even… |
| Create-event rules | {"eventName": "purchase", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "purchase", "merge_source_event_params… |
| Create-event rules | {"eventName": "add_to_cart", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "add_to_cart", "merge_source_event_… |
| Create-event rules | {"eventName": "contact", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "contact", "merge_source_event_params":… |
| Create-event rules | {"eventName": "colour_pallette", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "colour_pallette", "merge_sourc… |
| Create-event rules | {"eventName": "bridal_shop", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "bridal_shop", "merge_source_event_… |
| Create-event rules | {"eventName": "in_stock", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "in_stock", "merge_source_event_params… |
| Create-event rules | {"eventName": "made_to_order", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "made_to_order", "merge_source_ev… |
| Create-event rules | {"eventName": "park_and_fifth_co_cart", "isCopy": true, "instanceDestinationId": "G-1NHWMSMD59", "precompiledRule": {"new_event_name": "park_and_fifth_co_cart"… |
| User-provided data attached to hits | {"acceptAutomatic": false, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":3,\"args\":[{\"booleanExpressi… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-683612000"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-683612000"} |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-1NHWMSMD59"} |
| __ccd_enable_cm | {"instanceDestinationId": "AW-683612000"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-1NHWMSMD59"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "AW-683612000", "enableVariablesInDestinationId": false} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-1NHWMSMD59", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-1NHWMSMD59", "sessionDuration": 0} |
| Remarketing / conversion page view | {"containerId": "AW-683612000"} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| Other tags | Pinterest Tag: 2614154625030, Pinterest Tag: tagId=2614154625030 | GTM-PWXWHZZ (container) |
| Google Ads | `AW-683612000` | network |
| Meta Pixel | `1440135562842987` | network |
| Microsoft Ads (UET) | `343239094`, `343240572` | network |
| Pinterest Tag | `2614154625030` | network |
| TikTok Pixel | `C8TQU8I0VTGU7LHNSGO0` | network |
| Google Analytics 4 | `G-1NHWMSMD59` | network |
| Klaviyo | `JyznY6` | network |
| Microsoft Clarity | `uet` | network |
| Shopify app pixel: unknown app | {"shopUrl": "park-fifth-clothing-co.myshopify.com", "appNameSignature": "GLOBO PREORDER PIXEL"} | Shopify web pixel |
| Shopify app pixel: Microsoft Ads | {"ti": "343240572", "endpoint": "https://bat.bing.com/action/0"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"advertiserId": "101869", "shopDomain": "park-fifth-clothing-co.myshopify.com", "appVersion": "shopifyApp_5.4.1", "ori… | Shopify web pixel |
| Shopify app pixel: unknown app | {"accountID": "123"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"webhookEndpoint": "https://webhooks.fivetran.com/internal/75c5d981-20a7-4e95-bcb5-02e40011d839", "includedEvents": "u… | Shopify web pixel |
| Shopify app pixel: unknown app | {"myshopifyDomain": "park-fifth-clothing-co.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `AW-683612000`, `G-1NHWMSMD59` | Shopify web pixel |
| Shopify app pixel: TikTok | {"pixelCode": "C8TQU8I0VTGU7LHNSGO0"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"site_id": "3c16414c-7d50-4f6e-9525-fce6cd89862a", "analytics_endpoint": "https://na.shgcdn3.com"} | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "1440135562842987", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} | Shopify web pixel |
| Shopify app pixel: Pinterest | {"tagID": "2614154625030"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Google tag | `AW-683612000` | hard-coded in page HTML |
| Klaviyo | `JyznY6` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://parkandfifthco.com/en-us/products/jameson-set-oxford-chiffon · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item` | — | ✅ |
| `add_to_cart` | ✅ | ✅ |
| `view_cart` | — | ✅ |
| `begin_checkout` | — | — |
| `purchase` | ✅ | — |

_Checkout and purchase events cannot be observed without placing an order; container configuration is listed instead._

---

## 9. Consent & Privacy

| Check | Result |
|---|---|
| CMP detected | None |
| Banner action taken by audit | js_api — Shopify Customer Privacy (no visible banner) |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "", "analytics": "", "preferences": "", "sale_of_data": ""} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}} |
| Tracking vendors firing before consent | Campaign Manager 360 / Floodlight, Google Ads, Google Analytics 4, Meta Pixel, Microsoft Ads (UET), Microsoft Clarity, Pinterest Tag, TikTok Pixel |
| Scripts held until consent (text/plain, data-consent…) | — |
| Banner still visible after accept + reload | no |

**Consent configuration inside GTM:**

| Container | Consent types referenced | Consent templates | Tags with extra consent checks | CMP hints |
|---|---|---|---|---|
| `GTM-PWXWHZZ` | — | — | 0 / 1 | — |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-1NHWMSMD59` | initial | user_engagement×2, page_view×3, scroll×2 | `G111` |
| GA4 `G-1NHWMSMD59` | reload | user_engagement×2, page_view×3, scroll×2 | `G111` |
| GA4 `G-1NHWMSMD59` | pdp | user_engagement×2, page_view×3, product_page×3, scroll×2, view_item×1, form_start×1 | `G111` |
| GA4 `G-1NHWMSMD59` | atc | add_to_cart×1, user_engagement×2, page_view×3, scroll×2, view_cart×1 | `G111` |
| Meta `1440135562842987` | reload | PageView×1 | — |
| Meta `1440135562842987` | atc | PageView×1 | — |
| Google Ads `AW-683612000` | initial | gtag.config×2 | — |
| Google Ads `AW-683612000` | reload | gtag.config×2 | — |
| Google Ads `AW-683612000` | pdp | gtag.config×2, form_start×1 | — |
| Google Ads `AW-683612000` | atc | gtag.config×2 | — |

**dataLayer pushes observed:**

- `initial`: gtag:js, gtag:config:AW-683612000, gtm.scrollDepth, gtm.dom, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:event:page_view, gtm.load
- `reload`: gtag:js, gtag:config:AW-683612000, gtm.scrollDepth, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtm.dom, gtag:event:page_view, gtm.load
- `pdp`: gtag:js, gtag:config:AW-683612000, gtm.scrollDepth, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:event:page_view, gtag:event:view_item, gtm.formInteract, gtm.dom, gtm.load
- `atc`: gtag:js, gtag:config:AW-683612000, gtm.scrollDepth, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:event:page_view, gtag:event:view_item, gtm.formInteract, gtm.dom, gtm.load, gtag:event:add_to_cart

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 1453686948 | APP | — | ANALYTICS, MARKETING, PREFERENCES, SALE_OF_DATA | {"shopUrl": "park-fifth-clothing-co.myshopify.com", "appNameSignature": "GLOBO PREORDER PIXEL"} |
| 1370194084 | APP | Microsoft Ads | ANALYTICS, MARKETING, SALE_OF_DATA | {"ti": "343240572", "endpoint": "https://bat.bing.com/action/0"} |
| 1365541028 | APP | — | ANALYTICS, MARKETING | {"advertiserId": "101869", "shopDomain": "park-fifth-clothing-co.myshopify.com", "appVersion": "shopifyApp_5.4.1", "ori… |
| 1363738788 | APP | — | ANALYTICS | {"accountID": "123"} |
| 1348468900 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"webhookEndpoint": "https://webhooks.fivetran.com/internal/75c5d981-20a7-4e95-bcb5-02e40011d839", "includedEvents": "u… |
| 866189476 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"myshopifyDomain": "park-fifth-clothing-co.myshopify.com"} |
| 663158948 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"AW-683612000\"],\"target_country\":\"CA\",\"gtag_events\":[{\"type\":\"begin_checkout… |
| 525926564 | APP | TikTok | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixelCode": "C8TQU8I0VTGU7LHNSGO0"} |
| 387317924 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"site_id": "3c16414c-7d50-4f6e-9525-fce6cd89862a", "analytics_endpoint": "https://na.shgcdn3.com"} |
| 244777124 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "1440135562842987", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} |
| 120455332 | APP | Pinterest | ANALYTICS, MARKETING, SALE_OF_DATA | {"tagID": "2614154625030"} |
| 21037220 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 214630564 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 221937828 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `GTM-PWXWHZZ` | GTM | 9 | 346.0 KB | reload | googletagmanager.com | 1 | 2 | 18 | 7 |
| `AW-683612000` | GTAG | 6 | 623.5 KB | reload | googletagmanager.com | 45 | 0 | 6 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `AW-683612000`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Tag Manager | `GTM-PWXWHZZ` | 5 | initial:2, reload:1, pdp:1, atc:1 | 0 |
| Google tag (gtag.js) | — | 8 | initial:2, reload:2, pdp:2, atc:2 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-1NHWMSMD59` | 35 | initial:7, reload:7, pdp:12, atc:9 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 2 | initial:1, pdp:1 | 0 |
| Google Ads | `AW-683612000` | 35 | initial:8, reload:8, pdp:11, atc:8 | 0 |
| Meta Pixel | `1440135562842987` | 14 | initial:3, reload:3, pdp:4, atc:4 | 0 |
| Microsoft Ads (UET) | `343239094`, `343240572` | 47 | initial:12, reload:11, pdp:12, atc:12 | 0 |
| Pinterest Tag | `2614154625030` | 14 | initial:3, reload:3, pdp:4, atc:4 | 0 |
| TikTok Pixel | `C8TQU8I0VTGU7LHNSGO0` | 14 | initial:3, reload:3, pdp:4, atc:4 | 0 |

### Session replay / UX

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Microsoft Clarity | `uet` | 38 | initial:6, reload:13, pdp:6, atc:13 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Klaviyo | `JyznY6` | 132 | initial:42, reload:37, pdp:26, atc:27 | 0 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Yotpo | — | 53 | initial:9, consent:1, reload:11, pdp:22, atc:10 | 0 |

### Support / chat

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Gorgias | — | 116 | initial:29, reload:29, pdp:29, atc:29 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 1 | initial:1 | 0 |
| Shopify | — | 44 | initial:9, consent:1, reload:8, pdp:17, atc:9 | 0 |
| Shopify Analytics (Monorail) | — | 4 | initial:1, consent:1, pdp:1, atc:1 | 0 |
| Shopify CDN | — | 315 | initial:99, reload:72, pdp:72, atc:72 | 0 |

### Payments / BNPL

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Sezzle | — | 10 | initial:2, reload:2, pdp:3, atc:3 | 0 |

### Monitoring

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Bugsnag | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`s-pc.webyze.com` (73), `static.webyze.com` (52), `cdn.appmate.io` (50), `i.shgcdn.com` (47), `a.shgcdn2.com` (13), `shopify-cdn.getredo.com` (12), `instafeed.nfcube.com` (10), `bzrcdn.openai.com` (9), `media.9gtb.com` (8), `creditsyard.com` (8), `webhooks.fivetran.com` (7), `na.shgcdn3.com` (6), `cdn.nfcube.com` (6), `scontent.cdninstagram.com` (6), `d2wy8f7a9ursnm.cloudfront.net` (5), `country-service.shopifycloud.com` (5), `form.jotform.com` (5), `bzr.openai.com` (5), `cdn.jotfor.ms` (4), `storm.spicegems.org` (4), `egw-app.herokuapp.com` (4), `s3.amazonaws.com` (4), `dr4qe3ddw9y32.cloudfront.net` (4), `lantern.roeyecdn.com` (4), `lantern.roeye.com` (4), `app.pixelpop.co` (4), `d3k81ch9hvuctc.cloudfront.net` (2), `a.globo.io` (2), `fonts.cdnfonts.com` (2), `analytics-ipv6.tiktokw.us` (1)

</details>

---

## 14. Findings & Recommendations

### P1 — Fix now

**[Consent] No consent banner or US opt-out mechanism**  
6 advertising platform(s) fire (Campaign Manager 360 / Floodlight, Google Ads, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel); no CMP, no geo-targeted banner markup and no 'Do Not Sell or Share' / 'Your Privacy Choices' link were found.  
_Recommendation:_ Enable Shopify's privacy banner (or a CMP) with region rules: opt-in for EU/UK, opt-out link + GPC for US state privacy laws (CCPA/CPRA and others).

**[GTM · Deployment] Not met: Custom pixel overrides page_location — GTM-PWXWHZZ**  
GA4 hits from the sandbox report the web-pixels sandbox URL as page_location. Why it matters: Wrong page_location breaks every page, landing-page and attribution report.  
_Recommendation:_ Set page_location/page_title/page_referrer from event.context.document in the pixel.

**[Tracking · GA4] Not met: GA4 — One implementation per property**  
G-1NHWMSMD59 <- Shopify app: Google & YouTube x21, Shopify custom pixel #21037220 x9, Theme HTML (hard-coded) x5 Why it matters: Two implementations double-count events and revenue.  
_Recommendation:_ Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM carries a richer setup (then switch GA4 off in the app).

**[Tracking · GA4] Not met: GA4 — Page view sent once per load**  
Duplicates on one page load: G-1NHWMSMD59×3 (from Shopify app: Google & YouTube, Shopify custom pixel #21037220, Theme HTML (hard-coded)) Why it matters: Double page views inflate traffic and deflate conversion rates; for ad pixels they distort optimisation.  
_Recommendation:_ Remove the second source (app vs GTM vs hard-coded / custom pixel).

**[Tracking · GA4] Not met: GA4 — page_location is the real page URL**  
Sandbox URL recorded as page_location for G-1NHWMSMD59. Why it matters: Wrong page_location breaks page, landing-page and channel reports.  
_Recommendation:_ In the custom pixel set page_location/page_title from event.context.document.

**[Tracking · Microsoft Ads] Not met: Microsoft Ads — Page view sent once per load**  
Duplicates on one page load: 343240572×2 (from Shopify app: Microsoft Ads, Theme inline script) Why it matters: Double page views inflate traffic and deflate conversion rates; for ad pixels they distort optimisation.  
_Recommendation:_ Remove the second source (app vs GTM vs hard-coded / custom pixel).

### P2 — Address within 30 days

**[Tracking · GA4] Needs attention: GA4 — Single deployment route**  
Hits come from 2 routes: Shopify app: Google & YouTube x21; Shopify custom pixel #21037220 x9; Theme HTML (hard-coded) x5. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

**[Tracking · Google Ads] Needs attention: Google Ads — Single deployment route**  
Hits come from 2 routes: Theme HTML (hard-coded) x17; Shopify custom pixel #21037220 x16; Theme script x1; Shopify app: Google & YouTube x1. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ Consolidate to one deployment route per platform.

**[Tracking · Microsoft Ads] Needs attention: Microsoft Ads — Single deployment route**  
Hits come from 2 routes: Theme inline script x17; Shopify app: Microsoft Ads x6. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

### P3 — Clean-up / informational

**[Governance] GA4 data sent outside GTM**  
G-1NHWMSMD59 received hits but is not configured in any captured GTM container (likely a Shopify app pixel, hard-coded gtag, or sGTM-only routing).  
_Recommendation:_ Decide on one owner for each GA4 property to avoid double counting.

**[GTM · Governance] Needs attention: No unused variables — GTM-PWXWHZZ**  
6 variable(s) not referenced by any tag, trigger or variable: DLV - pinterest_quantity, DLV - pinterest_eventData, DLV - pinterest_orderValue, DLV - event, DLV - pinterest_order_id, DLV - pinterest_currency Why it matters: Clutter hides what actually drives data.  
_Recommendation:_ Remove unused variables.

**[Tracking · Google Ads] Needs attention: Google Ads — Dynamic remarketing sends product IDs**  
No product IDs on Ads hits from the product page or cart. Why it matters: Dynamic remarketing and PMax product audiences need product IDs that match the feed.  
_Recommendation:_ Send items (id matching the Merchant Center feed) with view_item / add_to_cart.

**[Tracking · Microsoft Ads] Needs attention: Microsoft Ads — Single UET tag**  
2 UET tags receive data: 343239094, 343240572. Why it matters: Extra IDs split audiences and send customer data to accounts nobody watches.  
_Recommendation:_ Confirm each is owned and in use; retire leftovers from agencies or old accounts.

**[Tracking · Stack] Needs attention: Stack — Third-party request volume**  
1391 third-party requests across the visit (19 identified platforms). Why it matters: Tag weight slows pages, which costs conversion rate.  
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

_Limitations: one product page per site, no checkout/purchase; server-side containers are only visible through their client-side traffic. Consent banners and pixels can vary by visitor country; connection-level errors (resets, SSL, ORB) are shown but not treated as site faults, as they often come from the capture network. Capture location signals: store redirected to /en-us market_

## Appendix — Capture Verification

_Supplemental: confirms the capture saw the site as a consenting visitor would._

- Coverage check: ✅ passed
- Consent action: js_api — Shopify Customer Privacy (no visible banner)
- Screenshots: [01_initial](screenshots/01_initial.png) · [02_after_consent](screenshots/02_after_consent.png) · [03_reload](screenshots/03_reload.png) · [04_pdp](screenshots/04_pdp.png) · [05_atc](screenshots/05_atc.png)
