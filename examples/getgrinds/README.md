# Tracking & Martech Audit — Grinds Coffee Pouches

**Site:** https://www.getgrinds.com/  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Google Tag Manager (GTM-5S6NX9)  
**Consent platform:** None detected  

---

## 1. Executive Summary

Tag management: **Google Tag Manager (GTM-5S6NX9)**. GA4 properties: `G-3F0KB1R8FY`, `G-8T9FVLXPLP`. Container `GTM-5S6NX9` scores **79/100** against best practice (1 failed, 4 warning checks). Tracking platforms (GA4 + ad pixels) score **88/100** on the events they actually received. The audit raised **2 P1**, **3 P2** and **8 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P1 | GTM · Ecommerce | Not met: No purchase tags tied to Shopify thank-you / checkout URLs — GTM-5S6NX9 |
| P1 | Tracking · GA4 | Not met: GA4 — One implementation per property |
| P2 | Analytics | Universal Analytics still deployed |
| P2 | Tracking · Google Ads | Needs attention: Google Ads — Single deployment route |
| P2 | Tracking · Microsoft Ads | Needs attention: Microsoft Ads — Single deployment route |
| P3 | Consent | No consent banner shown to this (US) visitor |
| P3 | GTM · Measurement | Needs attention: Measurement ID in a variable, not hard-coded — GTM-5S6NX9 |
| P3 | GTM · Ecommerce | Needs attention: Custom event names don't shadow GA4 standard events — GTM-5S6NX9 |
| P3 | GTM · Governance | Needs attention: No unused variables — GTM-5S6NX9 |
| P3 | Tracking · GA4 | Needs attention: GA4 — Single GA4 property |
| P3 | Tracking · Google Ads | Needs attention: Google Ads — Single Google Ads account |
| P3 | Tracking · Microsoft Ads | Needs attention: Microsoft Ads — Single UET tag |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** native apps for GA4, Meta, TikTok and Klaviyo. Google Ads is fed by **three routes**: GTM-5S6NX9, custom pixel #17858631 and the Google app. Microsoft Ads comes from custom pixel #19890247 **and** a theme inline script, with two UET IDs.
- **Biggest issue — silent revenue loss:** GTM's DemandJump `addTrans` purchase tag fires on `/thank_you`, which storefront GTM no longer reaches since Shopify's checkout upgrade, so that revenue attribution is dead. A legacy `conversion.js` is also hard-coded on the cart page.
- **Also:** GA4 G-8T9FVLXPLP is fed by both the app and a custom pixel; two Google Ads accounts and two UET tags receive data; UA tags are still active; landing-page click events are named `lp00x_add_to_cart` instead of GA4's standard event.
- **Pitch angle:** "your ad platforms get tracking from three places at once" — consolidate Google Ads and Microsoft to one route each, rebuild purchase tracking on Shopify Customer Events, and retire legacy tags.
- _Capture: US network, Oct 5 2026, fresh browser, consent accepted → reload → PDP → add to cart → cart. Outside-in only (no account access)._
<!-- ANALYST_NOTES_END -->

---

## 3. Next Steps — Analyst Checks & Discovery Questions

_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks below take minutes from the outside, and the questions are for the discovery conversation._

**Analyst checks (no account access needed)**

- [ ] **Microsoft Ads:** Confirm the hard-coded Microsoft Ads snippet in the theme (view source) — it runs alongside other routes (Shopify custom pixel #19890247, Theme inline script) — _View source / DevTools → Network → Initiator_
- [ ] **Consent:** Visit from an EU/UK VPN: does a banner appear, and do ad pixels wait for consent? — _Browser via EU VPN + DevTools → Network_

**Discovery questions for the prospect**

- **Purchase tracking:** Since Shopify's checkout upgrade (Checkout Extensibility), do Google Ads / GTM purchase conversions still match Shopify orders? Some purchase tags here are tied to the old thank-you page.
- **Ownership:** Google Ads, Microsoft Ads are fed by more than one route (Google Ads: GTM, Shopify app, Shopify custom pixel; Microsoft Ads: Shopify custom pixel, Theme). Who manages each, and which one is meant to be the source of truth?
- **GA4:** Are all of these GA4 properties still in use (any agency or legacy accounts)? G-3F0KB1R8FY, G-8T9FVLXPLP.
- **Google Ads:** Are all of these Google Ads accounts still in use (any agency or legacy accounts)? AW-1025544380, AW-656475018.
- **Microsoft Ads:** Are all of these UET tags still in use (any agency or legacy accounts)? 26022148, 5695791.
- **Meta:** Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), and what Event Match Quality do Purchase events get?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?
- **Email / SMS:** Are browse- and cart-abandonment flows live in Klaviyo, and are Viewed Product / Added to Cart metrics recording?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### `GTM-5S6NX9` — score 79/100 (✅ 10 · ⚠️ 4 · ❌ 1)

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ❌ | High | Ecommerce | No purchase tags tied to Shopify thank-you / checkout URLs | 1 active tag(s) fire on checkout / thank-you URLs or events: Custom HTML #13. This container loads on the storefront, and with Checkout Extensibility it no longer runs on checkout or thank-you pages, so these tags most … | Move purchase conversions to Shopify Customer Events (app pixel or a custom pixel subscribing to checkout_completed), then confirm Google Ads / Meta purchase conversions are recor… |
| ⚠️ | Medium | Ecommerce | Custom event names don't shadow GA4 standard events | Custom GA4 events named like standard ecommerce events: lp001_add_to_cart, lp002_add_to_cart, lp003_add_to_cart, lp004_add_to_cart. | Use the standard event name with a parameter (e.g. add_to_cart + placement=lp001) so it lands in GA4 ecommerce reports and Ads key events. |
| ⚠️ | Low | Measurement | Measurement ID in a variable, not hard-coded | 11 of 11 GA4 event tags hard-code the measurement ID. | Reference a Constant / Lookup Table variable so the ID changes in one place. |
| ⚠️ | Low | Governance | No unused variables | 9 variable(s) not referenced by any tag, trigger or variable: GA Settings (UA) #16, DLV - gtm.elementClasses, DLV - gtm.elementTarget, DLV - gtm.elementUrl, Auto-Event - TEXT, DLV - gtm.scrollUnits, DLV - gtm.scrollDire… | Remove unused variables. |
| ⚠️ | Low | Governance | Universal Analytics removed | 2 UA tag(s) (2 active); UA IDs UA-15100644-1, {{URL - Url}}. | Delete UA tags, GA Settings variables and UA triggers. |
| ✅ | High | Measurement | GA4 sent from one source only | No GA4 property is shared between GTM and a Shopify app. | — |
| ✅ | High | Consent | Consent Mode defaults set before tags fire | Consent Mode default is set via gtag outside GTM (theme / CMP / Shopify app) before the container loads. | — |
| ✅ | Medium | Measurement | Single GA4 Google tag | GA4 Google tag IDs: G-8T9FVLXPLP. | — |
| ✅ | Medium | Measurement | Google tag fires on Initialization / All Pages | Google tag fires on Initialization or Page View. | — |
| ✅ | Medium | Governance | Limited Custom HTML | 2 active Custom HTML tag(s) (12% of active tags). | — |
| ✅ | Medium | Performance | Tags firing on every page kept small | 2 tag(s) fire on every page load without filters; container 437.7 KB. | — |
| ✅ | Low | Governance | Paused tags cleaned up | 0 paused tag(s). | — |
| ✅ | Low | Governance | No orphan tags | 0 active tag(s) without a firing trigger. | — |
| ✅ | Low | Governance | Custom JavaScript variables kept lean | 0 Custom JavaScript variable(s). | — |
| ✅ | Low | Governance | No duplicate tags | No identical tags. | — |
| ℹ️ | High | Ecommerce | GA4 ecommerce funnel coverage | Configured in GTM: none. GA4 ecommerce is owned by Shopify Google & YouTube app (observed: add_to_cart, view_cart, view_item). `purchase` is not in GTM — expected on Shopify (checkout runs outside GTM); confirm a Custom… | Keep one owner for GA4 ecommerce; don't build a parallel GTM implementation unless replacing the app. |
| ℹ️ | Low | Governance | Tag names published (naming convention auditable) | Tag names are not published in the container (normal); naming convention can't be audited from outside. | — |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **88/100** (✅ 32 · ⚠️ 6 · ❌ 1).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 82 | 8 | 1 | 1 | Shopify app: Google & YouTube ×52; Shopify custom pixel #50724935 ×8; GTM GTM-5S6NX9 ×1 | initial: page_view×4, (none)×2; reload: user_engagement×4, page_view×2; pdp: scroll_rate×20, user_engagement×4, scroll×2, page_view×2, view_item×2; atc: scroll_rate×8, add_to_cart×2, user_engagement×4, page_view×2, view_cart×2 |
| Google Ads | 79 | 4 | 2 | 0 | GTM GTM-5S6NX9 ×41; Shopify custom pixel #17858631 ×20; Shopify app: Google & YouTube ×14 | initial: gtag.config×12, page_view×4, remarketing×5; reload: gtag.config×9, page_view×3, remarketing×4; pdp: remarketing×4, gtag.config×9, page_view×3; atc: form_start×6, form_submit×6, remarketing×4, gtag.config×9, page_view×3 |
| Meta | 100 | 7 | 0 | 0 | Shopify app: Meta (Facebook & Instagram) ×8 | initial: PageView×2; reload: PageView×1; pdp: PageView×1, ViewContent×1; atc: SubscribedButtonClick×1, AddToCart×1, PageView×1 |
| TikTok | 100 | 7 | 0 | 0 | Shopify app: TikTok ×8 | initial: Pageview×2, LandingPageView×1; reload: Pageview×1; pdp: Pageview×1, ViewContent×1; atc: AddToCart×1, Pageview×1 |
| Microsoft Ads | 73 | 2 | 3 | 0 | Shopify custom pixel #19890247 ×9; Theme inline script ×8 | initial: ?×3, pageLoad×2; reload: ?×2, pageLoad×2; pdp: ?×2, pageLoad×2; atc: ?×2, pageLoad×2 |
| Klaviyo | 100 | 2 | 0 | 0 | Shopify app embed: klaviyo-email-marketing-sms ×139 | initial: (onsite.js loaded)×34; reload: (onsite.js loaded)×35; pdp: (onsite.js loaded)×35; atc: (onsite.js loaded)×35 |

### GA4 — 82/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ❌ | High | One implementation per property | G-8T9FVLXPLP <- Shopify app: Google & YouTube x34, Shopify custom pixel #50724935 x8, GTM GTM-5S6NX9 x1 | Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM carries a richer setup (then switch GA4 off in the app). |
| ⚠️ | Medium | Single GA4 property | 2 GA4 propertys receive data: G-3F0KB1R8FY, G-8T9FVLXPLP. | Confirm each is owned and in use; retire leftovers from agencies or old accounts. |
| ✅ | High | Page view sent once per load | G-3F0KB1R8FY×1, G-8T9FVLXPLP×1 on one page load. | — |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (2×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: scroll, user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x52; Shopify custom pixel #50724935 x8; GTM GTM-5S6NX9 x1. | — |

### Google Ads — 79/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | Single Google Ads account | 2 Google Ads accounts receive data: AW-1025544380, AW-656475018. | Confirm each is owned and in use; retire leftovers from agencies or old accounts. |
| ⚠️ | High | Single deployment route | Hits come from 3 routes: GTM GTM-5S6NX9 x41; Shopify custom pixel #17858631 x20; Shopify app: Google & YouTube x14; Theme HTML (hard-coded) x6. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 28 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |

### Meta — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Meta pixel | Meta pixel: 396472740546012. | — |
| ✅ | High | Page view sent once per load | 396472740546012×1 on one page load. | — |
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
| ✅ | Low | Single TikTok pixel | TikTok pixel: CPCCI03C77U544412G90. | — |
| ✅ | High | Page view sent once per load | CPCCI03C77U544412G90×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | event_id for Events API dedupe | event_id present. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ttp. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: TikTok x8. | — |

### Microsoft Ads — 73/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | Single UET tag | 2 UET tags receive data: 26022148, 5695791. | Confirm each is owned and in use; retire leftovers from agencies or old accounts. |
| ⚠️ | Low | Product IDs for dynamic remarketing | No product IDs on UET hits from product pages. | Send ecomm_prodid + ecomm_pagetype (Shopping / dynamic remarketing). |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Shopify custom pixel #19890247 x9; Theme inline script x8. | Consolidate to one deployment route per platform. |
| ✅ | High | Page view sent once per load | 5695791×1, 26022148×1 on one page load. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _uetsid, _uetvid. | — |
| ℹ️ | Low | UET Consent Mode signal | No UET consent (asc) parameter. | Enable UET Consent Mode if serving EU/UK traffic. |

### Klaviyo — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Medium | Onsite tracking (klaviyo.js) loaded | klaviyo.js loads. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: __kla_id. | — |
| ℹ️ | Medium | Viewed Product tracked (browse abandonment) | No Viewed Product event (only identified profiles are tracked — anonymous visitors expected to show none). | Confirm Viewed Product is enabled in the Klaviyo Shopify integration. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app embed: klaviyo-email-marketing-sms x139. | — |

### Stack — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Session-replay tools | 1: Hotjar. | — |
| ✅ | Low | Third-party request volume | 927 third-party requests across the visit (22 identified platforms). | — |
| ℹ️ | Low | Ad platforms in use | 5: Campaign Manager 360 / Floodlight, Google Ads, Meta Pixel, Microsoft Ads (UET), TikTok Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Container Deep Dive — `GTM-5S6NX9`

| Tag type | Active | Paused |
|---|---|---|
| GA4 Event | 11 | 0 |
| Custom HTML | 2 | 0 |
| Universal Analytics | 2 | 0 |
| Google Tag (GA4/Ads config) | 1 | 0 |

**Custom HTML tags:**

| Tag | Status | Vendors / IDs | Fires on | Preview |
|---|---|---|---|---|
| #13 | active | — | {{Event}} equals "gtm.load" AND {{URL - Url}} contains "/thank_you" |  <script type="text/gtmscript">window.djpush("addTrans","{{DLV - shopify_transaction.tran… |
| #12 | active | — | {{Event}} equals "gtm.js" |  <script type="text/gtmscript">(function(a,e,f,g,b,c,d){a[b]\|\|(a.DemandJumpAnalytics=a.… |

<details><summary>All active tags with firing conditions</summary>

| Tag | Type | IDs / event | Fires on | Consent |
|---|---|---|---|---|
| #1 | Universal Analytics | {} | {{URL - Url}} equals "https://www.getgrinds.com/pages/contact-us" AND {{Event}} equals "gtm.js" | — |
| #10 | Universal Analytics | {"trackingId": "UA-15100644-1"} | {{DLV - gtm.elementId}} equals "flavor-add-to-cart" AND {{Event}} equals "gtm.click" | — |
| #31 | Google Tag (GA4/Ads config) | {"tagId": "G-8T9FVLXPLP"} | {{Event}} equals "gtm.js" | — |
| #33 | GA4 Event | scroll_rate | {{Event}} equals "gtm.scrollDepth" AND {{DLV - gtm.triggers}} matches regex "(^$\|((^\|,)2644042_32($\|,)))" | — |
| #35 | GA4 Event | lp002_hero_cta | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-rid=\"c59a1021-814b-4429-b7f4-1e0fc004e672\"], [data-rid=\"c59a1021-814b-442… | — |
| #37 | GA4 Event | lp002_top_sticky_cta | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-rid=\"b8b16f9a-682f-4541-b9bc-2e3699bccb31\"], [data-rid=\"b8b16f9a-682f-454… | — |
| #39 | GA4 Event | lp002_add_to_cart | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-rid=\"7bcc22ee-6796-4ef3-a02a-14d2def7708d\"], [data-rid=\"7bcc22ee-6796-4ef… | — |
| #43 | GA4 Event | lp001_add_to_cart | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-rid=\"6c31e8e9-1f94-4019-b76c-3fa4f5a11551\"], [data-rid=\"6c31e8e9-1f94-401… | — |
| #44 | GA4 Event | lp001_hero_cta | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-rid=\"860a4750-7663-47c5-960a-249f8cd334f2\"], [data-rid=\"860a4750-7663-47c… | — |
| #45 | GA4 Event | lp001_top_sticky_cta | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-rid=\"62260af1-0783-4162-8275-7179e103f0c6\"], [data-rid=\"62260af1-0783-416… | — |
| #47 | GA4 Event | lp003_add_to_cart | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-pdp-atc-btn=\"lp003\"], [data-pdp-atc-btn=\"lp003\"] *" | — |
| #49 | GA4 Event | lp003_top_sticky_cta | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-sticky-cta=\"lp003\"], [data-sticky-cta=\"lp003\"] *" | — |
| #50 | GA4 Event | lp004_add_to_cart | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-pdp-atc-btn=\"lp004\"], [data-pdp-atc-btn=\"lp004\"] *" | — |
| #53 | GA4 Event | lp004_top_sticky_cta | {{Event}} equals "gtm.click" AND {{DLV - gtm.element}} matches CSS selector "[data-sticky-cta=\"lp004\"], [data-sticky-cta=\"lp004\"] *" | — |

</details>

**Reconstructed export:** `containers/GTM-5S6NX9.export.json` — 16 tags, 16 triggers, 22 variables

**Auto-event listeners:** Click (all elements), Scroll Depth

---

### 6.2 Google Tag Settings — `AW-1025544380`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-1025544380"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-1025544380"} |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-1025544380"} |
| __ccd_enable_cm | {"instanceDestinationId": "AW-1025544380"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "AW-1025544380", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "AW-1025544380"} |

---

### 6.3 Google Tag Settings — `AW-656475018`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-656475018"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": false, "isManualEnabled": false, "isEnabled": true, "isAutoCollectPiiEnabledFlag": true} |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-656475018"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "AW-656475018", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "AW-656475018"} |

---

### 6.4 Google Tag Settings — `G-3F0KB1R8FY`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Product settings | {"instanceDestinationId": "G-3F0KB1R8FY", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-3F0KB1R8FY"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced conversions settings | {"instanceDestinationId": "G-3F0KB1R8FY"} |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-3F0KB1R8FY"} |
| Enhanced measurement: form interactions | {"includeParams": true, "instanceDestinationId": "G-3F0KB1R8FY"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-3F0KB1R8FY"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-3F0KB1R8FY"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-3F0KB1R8FY"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-3F0KB1R8FY"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-3F0KB1R8FY"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| User-provided data attached to hits | {"acceptAutomatic": false, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":3,\"args\":[{\"booleanExpressi… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-3F0KB1R8FY"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-3F0KB1R8FY"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-3F0KB1R8FY", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-3F0KB1R8FY", "sessionDuration": 0} |

---

### 6.5 Google Tag Settings — `G-8T9FVLXPLP`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| __ogt_ga_send | {"value": true} |
| Unwanted referrals list | {"includeConditions": ["shopify\\.com"]} |
| Custom session timeout | {"sessionMinutes": 30, "sessionHours": 0} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Product settings | {"instanceDestinationId": "G-8T9FVLXPLP", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "LIMITED_EXTERNAL", "instanceDestinationId": "G-8T9FVLXPLP"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Create-event rules | {"eventName": "place_an_order", "isCopy": true, "instanceDestinationId": "G-8T9FVLXPLP", "precompiledRule": {"new_event_name": "place_an_order", "merge_source_… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-8T9FVLXPLP"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-8T9FVLXPLP"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-8T9FVLXPLP", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-8T9FVLXPLP", "sessionDuration": 0} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| GA4 | `G-8T9FVLXPLP` | GTM-5S6NX9 (container) |
| Universal Analytics | `UA-15100644-1`, `{{URL - Url}}` | GTM-5S6NX9 (container) |
| Google Ads | `AW-1025544380`, `AW-656475018` | network |
| Meta Pixel | `396472740546012` | network |
| Microsoft Ads (UET) | `26022148`, `5695791` | network |
| TikTok Pixel | `CPCCI03C77U544412G90` | network |
| Google Analytics 4 | `G-3F0KB1R8FY`, `G-8T9FVLXPLP` | network |
| Klaviyo | `d3YDZ5` | network |
| Hotjar | `2904192` | network |
| Shopify app pixel: unknown app | {"storeId": "3d6701f7-78e6-44ea-a43d-217ebaa795a9"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"webhookEndpoint": "https://webhooks.fivetran.com/internal/82a6a5ca-0fe0-4760-8ce8-f8b213dbd50f", "includedEvents": "u… | Shopify web pixel |
| Shopify app pixel: TikTok | {"pixelCode": "CPCCI03C77U544412G90"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"accountID": "1220658", "workspaceId": "9f383823-3343-474d-bd57-2b332eed6dd2", "projectId": "79ceecb6-e26a-4316-a922-5… | Shopify web pixel |
| Shopify app pixel: Klaviyo | {"accountID": "d3YDZ5", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shopId": "getgrinds.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shopId": "1360", "acornSiteToken": "L8Dryken"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `G-3F0KB1R8FY` | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "396472740546012", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"myshopifyDomain": "getgrinds.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Google tag | `AW-1025544380`, `AW-656475018` | hard-coded in page HTML |
| Klaviyo | `d3YDZ5` | hard-coded in page HTML |
| Hotjar | `2904192` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://www.getgrinds.com/products/zero-pouches-caramel-apple · add-to-cart clicked: yes

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
| CMP detected | None |
| Banner action taken by audit | js_api — Shopify Customer Privacy (no visible banner) |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "yes", "analytics": "yes", "preferences": "yes", "sale_of_data": "yes"} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}} |
| Tracking vendors firing before consent | Campaign Manager 360 / Floodlight, Google Ads, Google Analytics 4, Hotjar, Meta Pixel, Microsoft Ads (UET), TikTok Pixel |
| Scripts held until consent (text/plain, data-consent…) | — |
| Banner still visible after accept + reload | no |

_Returning visit: the persistent browser profile already held this site's cookies/consent, so the `initial` phase reflects stored consent, not a first visit (re-run with `--fresh` for that)._

**Consent configuration inside GTM:**

| Container | Consent types referenced | Consent templates | Tags with extra consent checks | CMP hints |
|---|---|---|---|---|
| `GTM-5S6NX9` | — | — | 0 / 16 | — |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-3F0KB1R8FY` | initial | page_view×3, (no event name)×1 | `G111` |
| GA4 `G-3F0KB1R8FY` | reload | user_engagement×2, page_view×1 | `G111` |
| GA4 `G-3F0KB1R8FY` | pdp | scroll×2, user_engagement×2, page_view×1, view_item×1 | `G111` |
| GA4 `G-3F0KB1R8FY` | atc | add_to_cart×1, user_engagement×2, page_view×1, view_cart×1 | `G111` |
| GA4 `G-8T9FVLXPLP` | initial | page_view×1, (no event name)×1 | `G111` |
| GA4 `G-8T9FVLXPLP` | consent | scroll_rate×1 | `G111` |
| GA4 `G-8T9FVLXPLP` | reload | user_engagement×2, page_view×1 | `G111` |
| GA4 `G-8T9FVLXPLP` | pdp | scroll_rate×20, user_engagement×2, view_item×1, page_view×1 | `G111` |
| GA4 `G-8T9FVLXPLP` | atc | scroll_rate×8, add_to_cart×1, user_engagement×2, view_cart×1, page_view×1 | `G111` |
| Google Ads `AW-1025544380` | initial | gtag.config×3, remarketing×1 | — |
| Google Ads `AW-1025544380` | reload | gtag.config×2, remarketing×1 | — |
| Google Ads `AW-1025544380` | pdp | remarketing×1, gtag.config×2 | — |
| Google Ads `AW-1025544380` | atc | form_start×1, form_submit×1, remarketing×1, gtag.config×2 | — |
| Google Ads `AW-656475018` | initial | gtag.config×1 | — |
| Google Ads `AW-656475018` | reload | gtag.config×1 | — |
| Google Ads `AW-656475018` | pdp | gtag.config×1 | — |
| Google Ads `AW-656475018` | atc | form_start×1, form_submit×1, gtag.config×1 | — |

**dataLayer pushes observed:**

- `initial`: gtag:js, gtag:config:AW-656475018, gtag:config:AW-1025544380, gtm.js, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:G-3F0KB1R8FY, gtm.dom, gtag:event:page_view
- `reload`: gtag:js, gtag:config:AW-656475018, gtag:config:AW-1025544380, gtm.js, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:G-3F0KB1R8FY, gtag:event:page_view, gtm.dom, gtm.scrollDepth, gtm.load
- `pdp`: gtag:js, gtag:config:AW-656475018, gtag:config:AW-1025544380, gtm.js, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:G-3F0KB1R8FY, gtag:event:page_view, gtag:event:view_item, gtm.dom
- `atc`: gtag:js, gtag:config:AW-656475018, gtag:config:AW-1025544380, gtm.js, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:G-3F0KB1R8FY, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.click, gtm.formSubmit, gtm.load, gtm.scrollDepth, gtag:event:add_to_cart

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 2265317447 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"storeId": "3d6701f7-78e6-44ea-a43d-217ebaa795a9"} |
| 2151317575 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"webhookEndpoint": "https://webhooks.fivetran.com/internal/82a6a5ca-0fe0-4760-8ce8-f8b213dbd50f", "includedEvents": "u… |
| 2151252039 | APP | TikTok | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixelCode": "CPCCI03C77U544412G90"} |
| 1435893831 | APP | — | ANALYTICS | {"accountID": "1220658", "workspaceId": "9f383823-3343-474d-bd57-2b332eed6dd2", "projectId": "79ceecb6-e26a-4316-a922-5… |
| 1291681863 | APP | Klaviyo | ANALYTICS, MARKETING | {"accountID": "d3YDZ5", "webPixelConfig": "eyJlbmFibGVBZGRlZFRvQ2FydEV2ZW50cyI6IHRydWV9"} |
| 545095751 | APP | — | ANALYTICS, MARKETING | {"shopId": "getgrinds.myshopify.com"} |
| 389611591 | APP | — | MARKETING | {"shopId": "1360", "acornSiteToken": "L8Dryken"} |
| 381157447 | APP | — | ANALYTICS | {} |
| 234356807 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"G-3F0KB1R8FY\"],\"gtag_events\":[{\"type\":\"begin_checkout\",\"action_label\":\"G-3F… |
| 145096775 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "396472740546012", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} |
| 2916423 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"myshopifyDomain": "getgrinds.myshopify.com"} |
| 17858631 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 19824711 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 19857479 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 19890247 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 19923015 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 19955783 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 19988551 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 25985095 | CUSTOM | — | ANALYTICS, MARKETING, SALE_OF_DATA | — |
| 50724935 | CUSTOM | — | ANALYTICS | — |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `GTM-5S6NX9` | GTM | 7 | 437.7 KB | reload | googletagmanager.com | 16 | 0 | 28 | 16 |
| `AW-1025544380` | GTAG | 3 | 481.1 KB | reload | googletagmanager.com | 11 | 0 | 4 | 4 |
| `AW-656475018` | GTAG | 2 | 476.7 KB | reload | googletagmanager.com | 9 | 0 | 4 | 4 |
| `G-3F0KB1R8FY` | GTAG | 1 | 590.4 KB | reload | googletagmanager.com | 22 | 0 | 6 | 4 |
| `G-8T9FVLXPLP` | GTAG | 2 | 529.9 KB | reload | googletagmanager.com | 16 | 0 | 6 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `AW-1025544380`, `AW-656475018`, `G-3F0KB1R8FY`, `G-8T9FVLXPLP`, `GTM-5S6NX9`
- GTM IDs referenced in page HTML: `GTM-5S6NX9`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Tag Manager | `GTM-5S6NX9` | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |
| Google tag (gtag.js) | — | 32 | initial:8, reload:8, pdp:8, atc:8 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-3F0KB1R8FY`, `G-8T9FVLXPLP` | 35 | initial:6, consent:1, reload:6, pdp:11, atc:11 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 5 | initial:3, atc:2 | 0 |
| Google Ads | `AW-1025544380`, `AW-656475018` | 81 | initial:21, reload:16, pdp:16, atc:28 | 0 |
| Meta Pixel | `396472740546012` | 16 | initial:4, reload:3, pdp:4, atc:5 | 0 |
| Microsoft Ads (UET) | `26022148`, `5695791` | 49 | initial:12, reload:13, pdp:12, atc:12 | 0 |
| TikTok Pixel | `CPCCI03C77U544412G90` | 16 | initial:5, reload:3, pdp:4, atc:4 | 0 |

### Affiliate / influencer

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Rakuten Advertising | — | 3 | consent:1, reload:1, atc:1 | 0 |

### Session replay / UX

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Hotjar | `2904192` | 8 | initial:2, reload:2, pdp:2, atc:2 | 0 |

### Personalisation / testing / search

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| VWO | — | 12 | initial:3, reload:3, pdp:3, atc:3 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Justuno | — | 27 | consent:9, reload:5, pdp:3, atc:10 | ⚠️ 3 |
| Klaviyo | `d3YDZ5` | 165 | initial:40, reload:43, pdp:41, atc:41 | 0 |
| Postscript | — | 9 | initial:1, consent:1, reload:2, pdp:1, atc:4 | ⚠️ 6 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Yotpo | — | 46 | initial:9, reload:7, pdp:21, atc:9 | ⚠️ 4 |

### Support / chat

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Zendesk | — | 26 | initial:7, reload:6, pdp:6, atc:7 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 5 | initial:2, reload:1, pdp:1, atc:1 | 0 |
| Shopify | — | 41 | initial:12, consent:1, reload:8, pdp:9, atc:11 | 0 |
| Shopify Analytics (Monorail) | — | 18 | initial:5, consent:1, reload:4, pdp:4, atc:4 | 0 |
| Shopify CDN | — | 126 | initial:29, consent:3, reload:33, pdp:29, atc:32 | 0 |

### Ecommerce apps

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Recharge | — | 3 | consent:1, reload:1, atc:1 | 0 |
| Skio | — | 8 | initial:2, reload:2, pdp:2, atc:2 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`backend.alia-prod.com` (31), `files.alia-prod.com` (12), `api.config-security.com` (9), `d2jjzw81hqbuqv.cloudfront.net` (8), `cdn.demandjump.com` (8), `data.replo.app` (8), `webhooks.fivetran.com` (7), `jointrybe.com` (6), `api.whaledb.io` (5), `p.yotpoapi.com` (5), `staticxx.s3.amazonaws.com` (4), `limits.minmaxify.com` (4), `conf.config-security.com` (4), `whale.camera` (4), `static.bogos.io` (4), `cdn-cookie.avada.io` (4), `getgrinds.myshopify.com` (4), `www.talkable.com` (4), `s3-us-west-2.amazonaws.com` (4), `cdn.savedby.io` (4), `firebasestorage.googleapis.com` (4), `motivate.shopapps.site` (3), `id-shop.govx.com` (3), `superbump.herokuapp.com` (3), `backinstock.useamp.com` (3), `i5.govx.net` (3), `analytics-ipv6.tiktokw.us` (2), `getgrinds.s3.us-east-2.amazonaws.com` (1)

</details>

---

## 14. Findings & Recommendations

### P1 — Fix now

**[GTM · Ecommerce] Not met: No purchase tags tied to Shopify thank-you / checkout URLs — GTM-5S6NX9**  
1 active tag(s) fire on checkout / thank-you URLs or events: Custom HTML #13. This container loads on the storefront, and with Checkout Extensibility it no longer runs on checkout or thank-you pages, so these tags most likely never fire. Why it matters: Missing purchase conversions starve bidding algorithms and understate ROAS.  
_Recommendation:_ Move purchase conversions to Shopify Customer Events (app pixel or a custom pixel subscribing to checkout_completed), then confirm Google Ads / Meta purchase conversions are recording.

**[Tracking · GA4] Not met: GA4 — One implementation per property**  
G-8T9FVLXPLP <- Shopify app: Google & YouTube x34, Shopify custom pixel #50724935 x8, GTM GTM-5S6NX9 x1 Why it matters: Two implementations double-count events and revenue.  
_Recommendation:_ Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM carries a richer setup (then switch GA4 off in the app).

### P2 — Address within 30 days

**[Analytics] Universal Analytics still deployed**  
2 active UA tag(s) in GTM. UA stopped processing data in July 2024.  
_Recommendation:_ Delete UA tags, GA Settings variables and UA-only triggers.

**[Tracking · Google Ads] Needs attention: Google Ads — Single deployment route**  
Hits come from 3 routes: GTM GTM-5S6NX9 x41; Shopify custom pixel #17858631 x20; Shopify app: Google & YouTube x14; Theme HTML (hard-coded) x6. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

**[Tracking · Microsoft Ads] Needs attention: Microsoft Ads — Single deployment route**  
Hits come from 2 routes: Shopify custom pixel #19890247 x9; Theme inline script x8. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ Consolidate to one deployment route per platform.

### P3 — Clean-up / informational

**[Consent] No consent banner shown to this (US) visitor**  
5 ad platform(s) fire without a banner — normal for US opt-out. A US opt-out link (Do Not Sell / Your Privacy Choices) is present.  
_Recommendation:_ Confirm EU/UK visitors get an opt-in banner and that the US opt-out link + GPC actually suppress ad pixels (Shopify Customer Privacy sale_of_data).

**[GTM · Measurement] Needs attention: Measurement ID in a variable, not hard-coded — GTM-5S6NX9**  
11 of 11 GA4 event tags hard-code the measurement ID. Why it matters: Hard-coded IDs make property migrations and staging setups error-prone.  
_Recommendation:_ Reference a Constant / Lookup Table variable so the ID changes in one place.

**[GTM · Ecommerce] Needs attention: Custom event names don't shadow GA4 standard events — GTM-5S6NX9**  
Custom GA4 events named like standard ecommerce events: lp001_add_to_cart, lp002_add_to_cart, lp003_add_to_cart, lp004_add_to_cart. Why it matters: Non-standard names fragment reporting and aren't used by GA4 ecommerce or Ads bidding.  
_Recommendation:_ Use the standard event name with a parameter (e.g. add_to_cart + placement=lp001) so it lands in GA4 ecommerce reports and Ads key events.

**[GTM · Governance] Needs attention: No unused variables — GTM-5S6NX9**  
9 variable(s) not referenced by any tag, trigger or variable: GA Settings (UA) #16, DLV - gtm.elementClasses, DLV - gtm.elementTarget, DLV - gtm.elementUrl, Auto-Event - TEXT, DLV - gtm.scrollUnits, DLV - gtm.scrollDirection, DLV - gtm.visibleRatio Why it matters: Clutter hides what actually drives data.  
_Recommendation:_ Remove unused variables.

**[Tracking · GA4] Needs attention: GA4 — Single GA4 property**  
2 GA4 propertys receive data: G-3F0KB1R8FY, G-8T9FVLXPLP. Why it matters: Extra IDs split audiences and send customer data to accounts nobody watches.  
_Recommendation:_ Confirm each is owned and in use; retire leftovers from agencies or old accounts.

**[Tracking · Google Ads] Needs attention: Google Ads — Single Google Ads account**  
2 Google Ads accounts receive data: AW-1025544380, AW-656475018. Why it matters: Extra IDs split audiences and send customer data to accounts nobody watches.  
_Recommendation:_ Confirm each is owned and in use; retire leftovers from agencies or old accounts.

**[Tracking · Microsoft Ads] Needs attention: Microsoft Ads — Single UET tag**  
2 UET tags receive data: 26022148, 5695791. Why it matters: Extra IDs split audiences and send customer data to accounts nobody watches.  
_Recommendation:_ Confirm each is owned and in use; retire leftovers from agencies or old accounts.

**[Tracking · Microsoft Ads] Needs attention: Microsoft Ads — Product IDs for dynamic remarketing**  
No product IDs on UET hits from product pages.  
_Recommendation:_ Send ecomm_prodid + ecomm_pagetype (Shopping / dynamic remarketing).

<details><summary>Failed requests</summary>

| Vendor | Phase | Status / error | URL |
|---|---|---|---|
| Yotpo | initial | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://staticw2.yotpo.com//widget.js?lang=en |
| Postscript | initial | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=1360&src=sdkAppEmbed |
| Justuno | consent | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://my.justuno.com/ajax/account_config_4.1.html?callback=jsonCallback&m=0&id=80E3A949-7B86-4BDB… |
| Justuno | consent | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://my.justuno.com/ajax/account_config_4.1.html?callback=jsonCallback&m=0&id=80E3A949-7B86-4BDB… |
| Yotpo | reload | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://staticw2.yotpo.com//widget.js?lang=en |
| Postscript | reload | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=1360&src=sdkAppEmbed |
| Justuno | pdp | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://my.justuno.com/ajax/account_config_4.1.html?callback=jsonCallback&m=0&id=80E3A949-7B86-4BDB… |
| Yotpo | pdp | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://staticw2.yotpo.com//widget.js?lang=en |
| Postscript | pdp | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=1360&src=sdkAppEmbed |
| Postscript | atc | net::ERR_FAILED (likely capture network) | https://sdk-api.postscript.io/p/L8Dryken/sdk-config |
| Yotpo | atc | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://staticw2.yotpo.com//widget.js?lang=en |
| Postscript | atc | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=1360&src=sdkAppEmbed |
| Postscript | atc | net::ERR_FAILED (likely capture network) | https://sdk-api.postscript.io/p/L8Dryken/sdk-config |

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
