# Tracking & Martech Audit — Retrospekt

**Site:** https://retrospekt.com  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Shopify Customer Events (app pixels)  
**Consent platform:** Shopify Privacy Banner  

---

## 1. Executive Summary

Tag management: **Shopify Customer Events (app pixels)**. GA4 property: `G-62SGN31TXD`. Tracking platforms (GA4 + ad pixels) score **95/100** on the events they actually received. The audit raised **1 P1**, **2 P2** and **1 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P1 | Tracking · Microsoft Ads | Not met: Microsoft Ads — Page view sent once per load |
| P2 | Data quality | Tracking requests failing |
| P2 | Tracking · Microsoft Ads | Needs attention: Microsoft Ads — Single deployment route |
| P3 | Consent | Ad pixels fire on load (no banner shown to this visitor) |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** fully native app integrations (Google & YouTube, Facebook & Instagram, TikTok, Pinterest, Microsoft) plus the Klaviyo theme snippet. The one exception is Microsoft UET, which also runs from a theme inline script.
- **What's working:** tracking 95/100, with clean product-level events on GA4, Google Ads, Meta, TikTok and Pinterest.
- **Issues:** Microsoft counts each page view twice (native app + theme snippet); the Impact affiliate request returns HTTP 400. An earlier capture saw add-to-cart fire twice on every platform; it didn't recur this run, so it's on the analyst checklist.
- **Pitch angle:** small fixes — remove the theme UET snippet and repair Impact — then growth work on top of a sound base.
- _Capture: US network, Oct 5 2026, fresh browser, consent accepted → reload → PDP → add to cart → cart. Outside-in only (no account access)._
<!-- ANALYST_NOTES_END -->

---

## 3. Next Steps — Analyst Checks & Discovery Questions

_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks below take minutes from the outside, and the questions are for the discovery conversation._

**Analyst checks (no account access needed)**

- [ ] **Microsoft Ads:** Confirm the hard-coded Microsoft Ads snippet in the theme (view source) — it runs alongside other routes (Shopify app: Microsoft Ads, Theme inline script) — _View source / DevTools → Network → Initiator_
- [ ] **Consent:** Visit from an EU/UK VPN: does a banner appear, and do ad pixels wait for consent? — _Browser via EU VPN + DevTools → Network_
- [ ] **Consent:** Check the footer for a 'Your Privacy Choices / Do Not Sell or Share' link (none found on the homepage HTML) — _Site footer, privacy policy_

**Discovery questions for the prospect**

- **Purchase tracking:** Do GA4 revenue and Google Ads / Meta purchase counts reconcile with Shopify orders (a gap above ~10% usually means a tracking problem)?
- **Ownership:** Microsoft Ads are fed by more than one route (Microsoft Ads: Shopify app, Theme). Who manages each, and which one is meant to be the source of truth?
- **Meta:** Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), and what Event Match Quality do Purchase events get?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?
- **Vendors:** Is Impact still an active partner? Its tracking requests fail.
- **Email / SMS:** Are browse- and cart-abandonment flows live in Klaviyo, and are Viewed Product / Added to Cart metrics recording?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### No GTM container — Google tag / Shopify app setup review

_No GTM container is deployed, so there is no container to score; these checks review the Google tag and app-based setup instead._

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ✅ | Low | Measurement | GA4 enhanced measurement | 7 enhanced-measurement feature(s) on G-62SGN31TXD. | — |
| ✅ | Low | Measurement | Google Signals | Enabled. | — |
| ℹ️ | Medium | Measurement | Tag management approach | No GTM container. Tags are deployed via Shopify app pixels (Google & YouTube, Meta (Facebook & Instagram), Microsoft Ads, Pinterest, TikTok). | Fine for a lean channel mix. Move to GTM (or a Shopify custom pixel + GTM) once the brand needs custom events, more ad platforms or consent orchestration beyond the apps. |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **95/100** (✅ 41 · ⚠️ 1 · ❌ 1).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 100 | 10 | 0 | 0 | Shopify app: Google & YouTube ×17 | initial: page_view×1, (none)×1; reload: user_engagement×2, page_view×1; pdp: scroll×3, user_engagement×2, page_view×1, view_item×1; atc: add_to_cart×1, user_engagement×2, page_view×1, view_cart×1 |
| Google Ads | 100 | 5 | 0 | 0 | Shopify app: Google & YouTube ×26; Theme HTML (hard-coded) ×5; Unattributed ×4 | initial: page_view×4; reload: page_view×7; pdp: page_view×5, view_item×4; atc: form_start×3, form_submit×3, add_to_cart×4, page_view×5 |
| Meta | 100 | 7 | 0 | 0 | Shopify app: Meta (Facebook & Instagram) ×7 | initial: PageView×1; reload: PageView×1; pdp: PageView×1, ViewContent×1; atc: SubscribedButtonClick×1, AddToCart×1, PageView×1 |
| TikTok | 100 | 7 | 0 | 0 | Shopify app: TikTok ×7 | initial: Pageview×1, LandingPageView×1; reload: Pageview×1; pdp: Pageview×1, ViewContent×1; atc: AddToCart×1, Pageview×1 |
| Pinterest | 100 | 6 | 0 | 0 | Shopify app: Pinterest ×10 | initial: init×1, PageVisit×1; reload: init×1, PageVisit×1; pdp: init×1, PageVisit×2; atc: AddToCart×1, init×1, PageVisit×1 |
| Microsoft Ads | 55 | 3 | 1 | 1 | Shopify app: Microsoft Ads ×8; Theme inline script ×8 | initial: pageLoad×2, home×1, ?×1; reload: pageLoad×2, home×1, ?×1; pdp: pageLoad×2, view_item×1, ?×1; atc: add_to_cart×1, pageLoad×2, ?×1 |
| Klaviyo | 100 | 2 | 0 | 0 | Theme inline script ×48 | initial: (onsite.js loaded)×12; reload: (onsite.js loaded)×12; pdp: (onsite.js loaded)×12; atc: (onsite.js loaded)×12 |

### GA4 — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single GA4 property | GA4 property: G-62SGN31TXD. | — |
| ✅ | High | One implementation per property | G-62SGN31TXD <- Shopify app: Google & YouTube | — |
| ✅ | High | Page view sent once per load | G-62SGN31TXD×1 on one page load. | — |
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
| ✅ | Low | Single Google Ads account | Google Ads account: AW-949987678. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 15 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Google & YouTube x26; Theme HTML (hard-coded) x5; Unattributed x4. | — |

### Meta — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Meta pixel | Meta pixel: 751595061945779. | — |
| ✅ | High | Page view sent once per load | 751595061945779×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 6 of 6 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Meta (Facebook & Instagram) x7. | — |

### TikTok — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single TikTok pixel | TikTok pixel: CUGJ67RC77U0K1FAIJR0. | — |
| ✅ | High | Page view sent once per load | CUGJ67RC77U0K1FAIJR0×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | event_id for Events API dedupe | event_id present. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ttp. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: TikTok x7. | — |

### Pinterest — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Pinterest tag | Pinterest tag: 2612786138681. | — |
| ✅ | High | Page view sent once per load | 2612786138681×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | PageVisit sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _pin_unauth. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app: Pinterest x10. | — |

### Microsoft Ads — 55/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ❌ | High | Page view sent once per load | Duplicates on one page load: 187000140×2 (from Shopify app: Microsoft Ads, Theme inline script) | Remove the second source (app vs GTM vs hard-coded / custom pixel). |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Shopify app: Microsoft Ads x8; Theme inline script x8. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | Low | Single UET tag | UET tag: 187000140. | — |
| ✅ | Low | Product IDs for dynamic remarketing | ecomm_prodid / items present. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _uetsid, _uetvid. | — |
| ℹ️ | Low | UET Consent Mode signal | No UET consent (asc) parameter. | Enable UET Consent Mode if serving EU/UK traffic. |

### Klaviyo — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Medium | Onsite tracking (klaviyo.js) loaded | klaviyo.js loads. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: __kla_id. | — |
| ℹ️ | Medium | Viewed Product tracked (browse abandonment) | No Viewed Product event (only identified profiles are tracked — anonymous visitors expected to show none). | Confirm Viewed Product is enabled in the Klaviyo Shopify integration. |
| ℹ️ | Low | Deployment route | Sent via: Theme inline script x48. | — |

### Stack — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Third-party request volume | 953 third-party requests across the visit (19 identified platforms). | — |
| ℹ️ | Low | Session-replay tools | 0: none. | — |
| ℹ️ | Low | Ad platforms in use | 7: Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Google Tag Settings — `G-62SGN31TXD`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-949987678"} |
| __ogt_cps | {"cpsMode": "ALL"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": true, "manualPhoneEnabled": false, "manualAddressEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSe… |
| Product settings | {"instanceDestinationId": "G-62SGN31TXD", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-62SGN31TXD"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-62SGN31TXD"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-62SGN31TXD"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-62SGN31TXD"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-62SGN31TXD"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-62SGN31TXD"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-62SGN31TXD"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-949987678"} |
| Create-event rules | {"eventName": "add_payment_info", "isCopy": true, "instanceDestinationId": "G-62SGN31TXD", "precompiledRule": {"new_event_name": "add_payment_info", "merge_sou… |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-949987678"} |
| Create-event rules | {"eventName": "begin_checkout", "isCopy": true, "instanceDestinationId": "G-62SGN31TXD", "precompiledRule": {"new_event_name": "begin_checkout", "merge_source_… |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "deferPageView": true, "includeParams": true, "instanceDestinationId": "AW-949987678"} |
| Create-event rules | {"eventName": "purchase", "isCopy": true, "instanceDestinationId": "G-62SGN31TXD", "precompiledRule": {"new_event_name": "purchase", "merge_source_event_params… |
| __ccd_enable_cm | {"instanceDestinationId": "AW-949987678"} |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-62SGN31TXD"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":2,\"args\":[{\"booleanExpressio… |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-62SGN31TXD"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| GA4 destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "G-62SGN31TXD", "enableVariablesInDestinationId": false} |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "AW-949987678", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-62SGN31TXD", "sessionDuration": 0} |
| Remarketing / conversion page view | {"containerId": "AW-949987678"} |

---

### 6.2 Google Tag Settings — `GT-TNP5LSF`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| __dest_mc | {"ignoreDupeGtagConfigCalls": true, "destinationId": "MC-J3274TWV6C", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "MC-J3274TWV6C"} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| Google Ads | `AW-949987678` | network |
| Meta Pixel | `751595061945779` | network |
| Microsoft Ads (UET) | `187000140` | network |
| Pinterest Tag | `2612786138681` | network |
| TikTok Pixel | `CUGJ67RC77U0K1FAIJR0` | network |
| Google Analytics 4 | `G-62SGN31TXD` | network |
| Klaviyo | `XynJP5` | network |
| Shopify app pixel: unknown app | {"shopId": "retrospekt.myshopify.com"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shop": "retrospekt.myshopify.com", "cookie_duration": "3888000", "first_touch_or_last": "last_touch", "goaffpro_ident… | Shopify web pixel |
| Shopify app pixel: unknown app | {"mailchimp_store_id": "store_65haubnk7idqcdu5g4al", "mailchimp_user_id": "123856894", "mailchimp_list_id": "be2e738a95… | Shopify web pixel |
| Shopify app pixel: Microsoft Ads | {"ti": "187000140", "endpoint": "https://bat.bing.com/action/0"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"shopId": "4592", "env": "production", "metaData": "[]"} | Shopify web pixel |
| Shopify app pixel: TikTok | {"pixelCode": "CUGJ67RC77U0K1FAIJR0"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"campaignID": "27548", "externalExecutionURL": "https://engine.saasler.com/api/v1/webhook_executions/35b82364e2cf3b91d… | Shopify web pixel |
| Shopify app pixel: Google & YouTube | `AW-949987678`, `G-62SGN31TXD` | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "751595061945779", "pixel_type": "facebook_pixel"} | Shopify web pixel |
| Shopify app pixel: Pinterest | {"tagID": "2612786138681"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Klaviyo | `XynJP5` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://retrospekt.com/products/retro-orange-headphones · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item` | — | ✅ |
| `add_to_cart` | — | ✅ |
| `view_cart` | — | ✅ |
| `begin_checkout` | ✅ | — |
| `add_payment_info` | ✅ | — |
| `purchase` | ✅ | — |

_Checkout and purchase events cannot be observed without placing an order; container configuration is listed instead._

---

## 9. Consent & Privacy

| Check | Result |
|---|---|
| CMP detected | Shopify Privacy Banner |
| Banner action taken by audit | js_api — Shopify Customer Privacy (no visible banner) |
| Shopify Customer Privacy API | Loaded |
| Shopify visitor consent (after accept) | {"marketing": "", "analytics": "", "preferences": "", "sale_of_data": ""} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}} |
| Tracking vendors firing before consent | Campaign Manager 360 / Floodlight, Google Ads, Google Analytics 4, Google Merchant Center, Impact, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel |
| Scripts held until consent (text/plain, data-consent…) | — |
| Banner still visible after accept + reload | no |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-62SGN31TXD` | initial | page_view×1, (no event name)×1 | `G111` |
| GA4 `G-62SGN31TXD` | reload | user_engagement×2, page_view×1 | `G111` |
| GA4 `G-62SGN31TXD` | pdp | scroll×3, user_engagement×2, page_view×1, view_item×1 | `G111` |
| GA4 `G-62SGN31TXD` | atc | add_to_cart×1, user_engagement×2, page_view×1, view_cart×1 | `G111` |
| Meta `751595061945779` | atc | PageView×1 | — |
| Google Ads `AW-949987678` | initial | qn7NCM-x_aUBEN7S_sQD×3 | — |
| Google Ads `AW-949987678` | reload | qn7NCM-x_aUBEN7S_sQD×3 | — |
| Google Ads `AW-949987678` | pdp | qn7NCM-x_aUBEN7S_sQD×3, 4tJbCNWx_aUBEN7S_sQD×3 | — |
| Google Ads `AW-949987678` | atc | form_start×1, form_submit×1, aunpCNix_aUBEN7S_sQD×3, qn7NCM-x_aUBEN7S_sQD×3 | — |

**dataLayer pushes observed:**

- `initial`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-62SGN31TXD, gtag:config:GT-TNP5LSF, gtag:event:page_view, gtm.dom, gtm.load
- `reload`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-62SGN31TXD, gtag:config:GT-TNP5LSF, gtag:event:page_view, gtm.dom, gtm.load, gtm.scrollDepth
- `pdp`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-62SGN31TXD, gtag:config:GT-TNP5LSF, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load, gtm.scrollDepth
- `atc`: gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:js, gtag:config:G-62SGN31TXD, gtag:config:GT-TNP5LSF, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load, gtm.scrollDepth, gtm.formSubmit, gtag:event:add_to_cart

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 2503540815 | APP | — | ANALYTICS, MARKETING | {"shopId": "retrospekt.myshopify.com"} |
| 2198437967 | APP | — | — | {} |
| 1785397327 | APP | — | ANALYTICS, MARKETING | {"shop": "retrospekt.myshopify.com", "cookie_duration": "3888000", "first_touch_or_last": "last_touch", "goaffpro_ident… |
| 1758855247 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"mailchimp_store_id": "store_65haubnk7idqcdu5g4al", "mailchimp_user_id": "123856894", "mailchimp_list_id": "be2e738a95… |
| 1428193359 | APP | Microsoft Ads | ANALYTICS, MARKETING, SALE_OF_DATA | {"ti": "187000140", "endpoint": "https://bat.bing.com/action/0"} |
| 1160904783 | APP | — | — | {"shopId": "4592", "env": "production", "metaData": "[]"} |
| 538607695 | APP | TikTok | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixelCode": "CUGJ67RC77U0K1FAIJR0"} |
| 343113807 | APP | — | — | {"campaignID": "27548", "externalExecutionURL": "https://engine.saasler.com/api/v1/webhook_executions/35b82364e2cf3b91d… |
| 337215567 | APP | Google & YouTube | — | {"config":"{\"google_tag_ids\":[\"G-62SGN31TXD\",\"GT-TNP5LSF\"],\"target_country\":\"US\",\"gtag_events\":[{\"type\":\… |
| 127336527 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "751595061945779", "pixel_type": "facebook_pixel"} |
| 42795087 | APP | Pinterest | ANALYTICS, MARKETING, SALE_OF_DATA | {"tagID": "2612786138681"} |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `G-62SGN31TXD` | GTAG | 4 | 610.8 KB | reload | googletagmanager.com | 33 | 0 | 6 | 5 |
| `GT-TNP5LSF` | GTAG | 1 | 434.9 KB | reload | googletagmanager.com | 7 | 0 | 4 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `G-62SGN31TXD`, `GT-TNP5LSF`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google tag (gtag.js) | — | 12 | initial:3, reload:3, pdp:3, atc:3 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-62SGN31TXD` | 15 | initial:2, reload:3, pdp:6, atc:4 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 2 | initial:1, atc:1 | 0 |
| Google Ads | `AW-949987678` | 35 | initial:4, reload:7, pdp:9, atc:15 | 0 |
| Google Merchant Center | — | 7 | initial:1, reload:2, pdp:2, atc:2 | 0 |
| Meta Pixel | `751595061945779` | 15 | initial:3, reload:3, pdp:4, atc:5 | 0 |
| Microsoft Ads (UET) | `187000140` | 23 | initial:5, reload:6, pdp:6, atc:6 | 0 |
| Pinterest Tag | `2612786138681` | 14 | initial:3, reload:3, pdp:4, atc:4 | 0 |
| TikTok Pixel | `CUGJ67RC77U0K1FAIJR0` | 15 | initial:4, reload:3, pdp:4, atc:4 | 0 |

### Affiliate / influencer

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Impact | — | 4 | initial:1, reload:1, pdp:1, atc:1 | ⚠️ 4 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Klaviyo | `XynJP5` | 52 | initial:13, reload:13, pdp:13, atc:13 | 0 |
| Mailchimp | — | 10 | initial:2, reload:2, pdp:3, atc:3 | 0 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Loox | — | 25 | initial:9, reload:9, pdp:6, atc:1 | 0 |

### Consent

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shopify Privacy Banner | — | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 18 | initial:4, reload:5, pdp:6, atc:3 | 0 |
| Shopify | — | 123 | initial:22, consent:1, reload:38, pdp:38, atc:24 | 0 |
| Shopify Analytics (Monorail) | — | 27 | initial:4, consent:1, reload:7, pdp:12, atc:3 | 0 |
| Shopify CDN | — | 463 | initial:104, reload:147, pdp:117, atc:95 | ⚠️ 1 |

### Monitoring

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Bugsnag | — | 1 | pdp:1 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`mcjs.prd.a.intuit.com` (40), `api.config-security.com` (13), `forms.shopifyapps.com` (7), `api.whaledb.io` (6), `conf.config-security.com` (4), `retrospekt.myshopify.com` (4), `cdn.nfcube.com` (4), `phpstack-1035961-3646380.cloudwaysapps.com` (4), `newassets.hcaptcha.com` (3), `analytics-ipv6.tiktokw.us` (1), `js.hcaptcha.com` (1), `4375bd3388d8.w.hcaptcha.com` (1), `9e83fefb9a49.w.hcaptcha.com` (1), `api.hcaptcha.com` (1), `d2wy8f7a9ursnm.cloudfront.net` (1), `g86t03bsah.us-east-1.aws.clickhouse.cloud` (1)

</details>

---

## 14. Findings & Recommendations

### P1 — Fix now

**[Tracking · Microsoft Ads] Not met: Microsoft Ads — Page view sent once per load**  
Duplicates on one page load: 187000140×2 (from Shopify app: Microsoft Ads, Theme inline script) Why it matters: Double page views inflate traffic and deflate conversion rates; for ad pixels they distort optimisation.  
_Recommendation:_ Remove the second source (app vs GTM vs hard-coded / custom pixel).

### P2 — Address within 30 days

**[Data quality] Tracking requests failing**  
Requests failed or returned errors for: Impact.  
_Recommendation:_ Check each failing endpoint (blocked domain, retired pixel, wrong ID) and remove or fix the tag.

**[Tracking · Microsoft Ads] Needs attention: Microsoft Ads — Single deployment route**  
Hits come from 2 routes: Shopify app: Microsoft Ads x8; Theme inline script x8. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

### P3 — Clean-up / informational

**[Consent] Ad pixels fire on load (no banner shown to this visitor)**  
Shopify Privacy Banner is present but showed no banner to this US visitor; Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel, Microsoft Ads (UET), Pinterest Tag, TikTok Pixel fired on load — consistent with a US opt-out model.  
_Recommendation:_ Confirm EU/UK visitors get an opt-in banner and US opt-out (Do Not Sell / GPC) suppresses these pixels.

<details><summary>Failed requests</summary>

| Vendor | Phase | Status / error | URL |
|---|---|---|---|
| Impact | initial | 400 | https://trkapi.impact.com/PageLoad |
| Impact | reload | 400 | https://trkapi.impact.com/PageLoad |
| Impact | pdp | 400 | https://trkapi.impact.com/PageLoad |
| Impact | atc | 400 | https://trkapi.impact.com/PageLoad |
| Shopify CDN | atc | net::ERR_CONNECTION_CLOSED (likely capture network) | https://cdn.shopify.com/proxy/43e06839dde60019e80d2eb3a3288a5b80c4aca575f2351728408796074b48b3/d163… |

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
