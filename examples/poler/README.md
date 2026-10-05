# Tracking & Martech Audit — Poler

**Site:** https://poler.com  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Google Tag Manager (GTM-WTVHJNR)  
**Consent platform:** None detected  

---

## 1. Executive Summary

Tag management: **Google Tag Manager (GTM-WTVHJNR)**. GA4 property: `G-YBG65XL6PS`. Container `GTM-WTVHJNR` scores **80/100** against best practice (1 failed, 1 warning checks). Tracking platforms (GA4 + ad pixels) score **72/100** on the events they actually received. The audit raised **4 P1**, **5 P2** and **4 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P1 | Consent | No consent banner or US opt-out mechanism |
| P1 | GTM · Ecommerce | Not met: No purchase tags tied to Shopify thank-you / checkout URLs — GTM-WTVHJNR |
| P1 | Tracking · GA4 | Not met: GA4 — One implementation per property |
| P1 | Tracking · GA4 | Not met: GA4 — Page view sent once per load |
| P2 | Tracking · GA4 | Needs attention: GA4 — Add to cart event sent (add_to_cart) |
| P2 | Tracking · GA4 | Needs attention: GA4 — Single deployment route |
| P2 | Tracking · Google Ads | Needs attention: Google Ads — Single deployment route |
| P2 | Tracking · Meta | Needs attention: Meta — event_id on standard events (CAPI dedupe) |
| P2 | Tracking · Meta | Needs attention: Meta — Single deployment route |
| P3 | GTM · Google Ads | Needs attention: Enhanced conversions configured — GTM-WTVHJNR |
| P3 | Tracking · Google Ads | Needs attention: Google Ads — Dynamic remarketing sends product IDs |
| P3 | Tracking · Meta | Needs attention: Meta — Single Meta pixel |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** GA4 and Meta run through **native apps**, but each has a second route: GA4 via custom pixel #100204730, and Meta via a theme inline script with a second pixel ID (360270341980016). Google Ads is split between GTM-WTVHJNR (3 tags) and the Google app.
- **Revenue signal at risk:** GTM's only Ads purchase conversion fires on the old thank-you page, which storefront GTM no longer reaches. Unless the Google app also reports purchases, Ads bids without purchase data.
- **Also:** GA4 double-counts page views; the theme-coded Meta pixel sends no event_id (no CAPI dedupe) and duplicates AddToCart; no product IDs reach Google Ads; no consent banner or US opt-out link.
- **Pitch angle:** "make Google Ads see your purchases again" — confirm purchase conversions, move everything to the native apps, remove the theme pixel and the custom-pixel GA4.
- _Capture: US network, Oct 5 2026, fresh browser, consent accepted → reload → PDP → add to cart → cart. Outside-in only (no account access)._
<!-- ANALYST_NOTES_END -->

---

## 3. Next Steps — Analyst Checks & Discovery Questions

_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks below take minutes from the outside, and the questions are for the discovery conversation._

**Analyst checks (no account access needed)**

- [ ] **Ecommerce:** Add one product to cart and confirm each platform records ONE add-to-cart (Meta fired twice in the capture) — _Tag Assistant / Meta Pixel Helper / TikTok Pixel Helper + DevTools → Network_
- [ ] **Ecommerce:** Cart add redirects to /cart — manually confirm add_to_cart reaches GA4 and the ad pixels — _Tag Assistant / Meta Pixel Helper / TikTok Pixel Helper + DevTools → Network_
- [ ] **Meta:** Confirm the hard-coded Meta snippet in the theme (view source) — it runs alongside other routes (Shopify app: Meta (Facebook & Instagram), Theme inline script) — _View source / DevTools → Network → Initiator_
- [ ] **Consent:** Visit from an EU/UK VPN: does a banner appear, and do ad pixels wait for consent? — _Browser via EU VPN + DevTools → Network_
- [ ] **Consent:** Check the footer for a 'Your Privacy Choices / Do Not Sell or Share' link (none found on the homepage HTML) — _Site footer, privacy policy_

**Discovery questions for the prospect**

- **Purchase tracking:** Since Shopify's checkout upgrade (Checkout Extensibility), do Google Ads / GTM purchase conversions still match Shopify orders? Some purchase tags here are tied to the old thank-you page.
- **Ownership:** GA4, Google Ads, Meta are fed by more than one route (GA4: Shopify app, Shopify custom pixel; Google Ads: GTM, Shopify app; Meta: Shopify app, Theme). Who manages each, and which one is meant to be the source of truth?
- **Meta:** Are all of these Meta pixels still in use (any agency or legacy accounts)? 360270341980016, 364039191513066.
- **Meta:** Is the Facebook & Instagram app's data sharing set to 'Maximum' (Conversions API on), and what Event Match Quality do Purchase events get?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?
- **Email / SMS:** Are browse- and cart-abandonment flows live in Klaviyo, and are Viewed Product / Added to Cart metrics recording?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### `GTM-WTVHJNR` — score 80/100 (✅ 9 · ⚠️ 1 · ❌ 1)

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ❌ | High | Ecommerce | No purchase tags tied to Shopify thank-you / checkout URLs | 1 active tag(s) fire on checkout / thank-you URLs or events: Google Ads Conversion #4 (554155084). This container loads on the storefront, and with Checkout Extensibility it no longer runs on checkout or thank-you pages… | Move purchase conversions to Shopify Customer Events (app pixel or a custom pixel subscribing to checkout_completed), then confirm Google Ads / Meta purchase conversions are recor… |
| ⚠️ | Medium | Google Ads | Enhanced conversions configured | No user-provided data (enhanced conversions) on Ads conversion tags. | Enable enhanced conversions (hashed email/phone from the dataLayer) on purchase. |
| ✅ | High | Google Ads | Conversion Linker present | 2 Ads/Floodlight tag(s); conversion linker tags: 1. | — |
| ✅ | High | Consent | Consent Mode defaults set before tags fire | Consent Mode default is set via gtag outside GTM (theme / CMP / Shopify app) before the container loads. | — |
| ✅ | Medium | Governance | Limited Custom HTML | 0 active Custom HTML tag(s) (0% of active tags). | — |
| ✅ | Medium | Performance | Tags firing on every page kept small | 2 tag(s) fire on every page load without filters; container 425.8 KB. | — |
| ✅ | Low | Governance | Paused tags cleaned up | 0 paused tag(s). | — |
| ✅ | Low | Governance | No orphan tags | 0 active tag(s) without a firing trigger. | — |
| ✅ | Low | Governance | No unused variables | 0 variable(s) not referenced by any tag, trigger or variable. | — |
| ✅ | Low | Governance | Custom JavaScript variables kept lean | 0 Custom JavaScript variable(s). | — |
| ✅ | Low | Governance | No duplicate tags | No identical tags. | — |
| ℹ️ | High | Measurement | GA4 managed in GTM | No GA4 Google tag or GA4 event tags in the container. GA4 hits observed: G-YBG65XL6PS. | Keep one owner for GA4. If GA4 comes from the Shopify Google & YouTube app, leave GTM out of GA4 to avoid double counting; otherwise implement GA4 in GTM. |
| ℹ️ | High | Ecommerce | GA4 ecommerce events in GTM | No GA4 event tags in GTM. GA4 ecommerce is sent by the Shopify Google & YouTube app. | — |
| ℹ️ | Low | Google Ads | Dynamic remarketing (product feed) | 1 remarketing tag(s), no product-level parameters detected. | If running Shopping / PMax, send items with ecommerce events for dynamic remarketing. |
| ℹ️ | Low | Governance | Tag names published (naming convention auditable) | Tag names are not published in the container (normal); naming convention can't be audited from outside. | — |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **72/100** (✅ 17 · ⚠️ 8 · ❌ 2).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 61 | 6 | 2 | 2 | Shopify app: Google & YouTube ×12; Shopify custom pixel #100204730 ×6 | initial: user_engagement×2, page_view×2; reload: user_engagement×2, page_view×2; pdp: user_engagement×2, page_view×2, view_item×1; atc: user_engagement×2, page_view×2, view_cart×1 |
| Google Ads | 77 | 4 | 2 | 0 | GTM GTM-WTVHJNR ×16; Shopify app: Google & YouTube ×10 | initial: page_view×1, remarketing×4; reload: page_view×1, remarketing×4; pdp: page_view×1, remarketing×4; atc: form_start×3, form_submit×3, page_view×1, remarketing×4 |
| Meta | 74 | 4 | 4 | 0 | Shopify app: Meta (Facebook & Instagram) ×13; Theme inline script ×4 | initial: PageView×4; reload: PageView×2; pdp: PageView×2, ViewContent×2; atc: SubscribedButtonClick×2, AddToCart×3, PageView×2 |
| Klaviyo | 100 | 2 | 0 | 0 | Theme inline script ×48 | initial: (onsite.js loaded)×12; reload: (onsite.js loaded)×12; pdp: (onsite.js loaded)×12; atc: (onsite.js loaded)×12 |

### GA4 — 61/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ❌ | High | One implementation per property | G-YBG65XL6PS <- Shopify app: Google & YouTube x12, Shopify custom pixel #100204730 x6 | Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM carries a richer setup (then switch GA4 off in the app). |
| ❌ | High | Page view sent once per load | Duplicates on one page load: G-YBG65XL6PS×2 (from Shopify app: Google & YouTube, Shopify custom pixel #100204730) | Remove the second source (app vs GTM vs hard-coded / custom pixel). |
| ⚠️ | High | Add to cart event sent (add_to_cart) | No add_to_cart event in the atc phase (cart add redirected — verify in the platform's debugger). | Send add_to_cart on every cart add (incl. drawer/AJAX carts). |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Shopify app: Google & YouTube x12; Shopify custom pixel #100204730 x6. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | Low | Single GA4 property | GA4 property: G-YBG65XL6PS. | — |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Product view event carries items, value, currency | view_item sent (1×) with product, value and currency. | — |
| ✅ | Medium | Consent Mode signals on hits | gcs states seen: G111. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |

### Google Ads — 77/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | Dynamic remarketing sends product IDs | No product IDs on Ads hits from the product page or cart. | Send items (id matching the Merchant Center feed) with view_item / add_to_cart. |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: GTM GTM-WTVHJNR x16; Shopify app: Google & YouTube x10. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | Low | Single Google Ads account | Google Ads account: AW-554155084. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 11 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |

### Meta — 74/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | Single Meta pixel | 2 Meta pixels receive data: 360270341980016, 364039191513066. | Confirm each is owned and in use; retire leftovers from agencies or old accounts. |
| ⚠️ | Medium | Add to cart sent once per cart add | Sent 2× to 360270341980016 for a single cart add. | Find the second trigger (app + theme script, or two listeners) and keep one. |
| ⚠️ | High | event_id on standard events (CAPI dedupe) | 9 of 15 standard events (AddToCart, PageView, ViewContent) carry event_id. Missing on events from: Shopify app: Meta (Facebook & Instagram), Theme inline script. | Send a shared event_id with every standard event and its Conversions API twin. |
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Shopify app: Meta (Facebook & Instagram) x13; Theme inline script x4. | On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless… |
| ✅ | High | Page view sent once per load | 364039191513066×1, 360270341980016×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (2×) with product, value and currency. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (3×) with product, value and currency. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Advanced matching | No advanced-matching data (normal for anonymous visitors). | Enable automatic advanced matching so logged-in / checkout users are matched. |

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
| ✅ | Low | Third-party request volume | 389 third-party requests across the visit (14 identified platforms). | — |
| ℹ️ | Low | Session-replay tools | 0: none. | — |
| ℹ️ | Low | Ad platforms in use | 4: Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Container Deep Dive — `GTM-WTVHJNR`

| Tag type | Active | Paused |
|---|---|---|
| Conversion Linker | 1 | 0 |
| Google Ads Conversion | 1 | 0 |
| Google Ads Remarketing | 1 | 0 |

<details><summary>All active tags with firing conditions</summary>

| Tag | Type | IDs / event | Fires on | Consent |
|---|---|---|---|---|
| #3 | Conversion Linker | {} | {{Event}} equals "gtm.js" | — |
| #4 | Google Ads Conversion | {"conversionId": "554155084", "conversionLabel": "yNSyCLjukeMBEMz4nogC"} | {{URL - Url}} contains "thank_you" AND {{Event}} equals "Thank You Page" | — |
| #5 | Google Ads Remarketing | {"conversionId": "554155084"} | {{Event}} equals "gtm.js" | — |

</details>

**Reconstructed export:** `containers/GTM-WTVHJNR.export.json` — 3 tags, 2 triggers, 1 variables

**Custom dataLayer events used as triggers (1):** `Thank You Page`

---

### 6.2 Google Tag Settings — `AW-554155084`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| Ads data terms of service | {"instanceDestinationId": "AW-554155084"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": false, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "… |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-554155084"} |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-554155084"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Google Ads destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "AW-554155084", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "AW-554155084"} |

---

### 6.3 Google Tag Settings — `G-YBG65XL6PS`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| __ogt_ga_send | {"value": true} |
| Unwanted referrals list | {"includeConditions": ["poler\\.com"]} |
| Custom session timeout | {"sessionMinutes": 30, "sessionHours": 0} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Product settings | {"instanceDestinationId": "G-YBG65XL6PS", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-YBG65XL6PS"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-YBG65XL6PS"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-YBG65XL6PS"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": true, "destinationId": "G-YBG65XL6PS", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-YBG65XL6PS", "sessionDuration": 0} |

---

### 6.4 Google Tag Settings — `GT-WBZN4FN`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| __dest_mc | {"ignoreDupeGtagConfigCalls": true, "destinationId": "MC-R9RJLXG8JF", "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "MC-R9RJLXG8JF"} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| Google Ads | `AW-554155084`, `AW-554155084/yNSyCLjukeMBEMz4nogC` | GTM-WTVHJNR (container) |
| Google Ads | `AW-554155084` | network |
| Meta Pixel | `360270341980016`, `364039191513066` | network |
| Google Analytics 4 | `G-YBG65XL6PS` | network |
| Klaviyo | `NFpRJM` | network |
| Shopify app pixel: unknown app | {"shopId": "10910"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"webPixelName": "Judge.me"} | Shopify web pixel |
| Shopify app pixel: Google & YouTube | {"config": "{\"pixel_id\":\"GT-WBZN4FN\",\"target_country\":\"US\",\"gtag_events\":[{\"type\":\"purchase\",\"action_lab… | Shopify web pixel |
| Shopify app pixel: Meta (Facebook & Instagram) | {"pixel_id": "360270341980016", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} | Shopify web pixel |
| Shopify app pixel: unknown app | {"subdomain": "polerstuff"} | Shopify web pixel |
| Shopify app pixel: unknown app | {} | Shopify web pixel |
| Meta Pixel | `364039191513066` | hard-coded in page HTML |
| Google tag | `G-YBG65XL6PS` | hard-coded in page HTML |
| Klaviyo | `NFpRJM` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://poler.com/collections/spring-25spring/products/243mcv0109 · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item` | — | ✅ |
| `add_to_cart` | — | — |
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
| Shopify visitor consent (after accept) | {"marketing": "", "analytics": "", "preferences": "", "sale_of_data": ""} |
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": true, "update": null}, "analytics_storage": {"default": true, "update": null}, "ad_user_data": {"default": true, "update": null}, "ad_personalization": {"default": true, "update": null}} |
| Tracking vendors firing before consent | Campaign Manager 360 / Floodlight, Google Ads, Google Analytics 4, Google Merchant Center, Meta Pixel |
| Scripts held until consent (text/plain, data-consent…) | — |
| Banner still visible after accept + reload | no |

**Consent configuration inside GTM:**

| Container | Consent types referenced | Consent templates | Tags with extra consent checks | CMP hints |
|---|---|---|---|---|
| `GTM-WTVHJNR` | — | — | 0 / 3 | — |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-YBG65XL6PS` | initial | user_engagement×2, page_view×2 | `G111` |
| GA4 `G-YBG65XL6PS` | reload | user_engagement×2, page_view×2 | `G111` |
| GA4 `G-YBG65XL6PS` | pdp | user_engagement×2, page_view×2, view_item×1 | `G111` |
| GA4 `G-YBG65XL6PS` | atc | user_engagement×2, page_view×2, view_cart×1 | `G111` |
| Meta `364039191513066` | initial | PageView×2 | — |
| Meta `364039191513066` | reload | PageView×1 | — |
| Meta `364039191513066` | atc | PageView×1 | — |
| Google Ads `AW-554155084` | initial | remarketing×1 | — |
| Google Ads `AW-554155084` | reload | remarketing×1 | — |
| Google Ads `AW-554155084` | pdp | remarketing×1 | — |
| Google Ads `AW-554155084` | atc | form_start×1, form_submit×1, remarketing×1 | — |

**dataLayer pushes observed:**

- `initial`: gtag:js, gtag:config:G-YBG65XL6PS, gtm.js, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:GT-WBZN4FN, gtag:event:page_view, gtm.dom, gtm.load
- `reload`: gtag:js, gtag:config:G-YBG65XL6PS, gtm.js, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:GT-WBZN4FN, gtag:event:page_view, gtm.dom, gtm.load
- `pdp`: gtag:js, gtag:config:G-YBG65XL6PS, gtm.js, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:GT-WBZN4FN, gtag:event:page_view, gtag:event:view_item, gtm.dom, gtm.load
- `atc`: gtag:js, gtag:config:G-YBG65XL6PS, gtm.js, gtag:consent:default, gtag:set, gtag:policy:internal_sw_allowed, gtag:policy:inject_cmp_banner, gtag:set:developer_id.dYmNjMT, gtag:config:GT-WBZN4FN, gtag:event:page_view, gtm.dom, gtm.load

---

## 11. Shopify Customer Events (Web Pixels)

| Pixel ID | Type | App (inferred) | Purposes | Config |
|---|---|---|---|---|
| 1235714234 | APP | — | MARKETING | {"shopId": "10910"} |
| 1009483962 | APP | — | ANALYTICS | {"webPixelName": "Judge.me"} |
| 601030842 | APP | Google & YouTube | — | {"config": "{\"pixel_id\":\"GT-WBZN4FN\",\"target_country\":\"US\",\"gtag_events\":[{\"type\":\"purchase\",\"action_lab… |
| 277381306 | APP | Meta (Facebook & Instagram) | ANALYTICS, MARKETING, SALE_OF_DATA | {"pixel_id": "360270341980016", "pixel_type": "facebook_pixel", "metaapp_system_user_token": "-"} |
| 124125370 | APP | — | ANALYTICS, MARKETING, SALE_OF_DATA | {"subdomain": "polerstuff"} |
| 100204730 | CUSTOM | — | ANALYTICS | — |
| shopify-app-pixel | APP | — | ANALYTICS, MARKETING | {} |
| shopify-custom-pixel | CUSTOM | — | ANALYTICS, MARKETING | — |

---

## 12. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `GTM-WTVHJNR` | GTM | 2 | 425.8 KB | atc | googletagmanager.com | 3 | 0 | 7 | 2 |
| `AW-554155084` | GTAG | 3 | 480.8 KB | reload | googletagmanager.com | 10 | 0 | 4 | 4 |
| `G-YBG65XL6PS` | GTAG | 2 | 518.9 KB | reload | googletagmanager.com | 15 | 0 | 6 | 4 |
| `GT-WBZN4FN` | GTAG | 1 | 434.9 KB | reload | googletagmanager.com | 7 | 0 | 4 | 4 |

- Google tag IDs live in `window.google_tag_manager`: `AW-554155084`, `G-YBG65XL6PS`, `GT-WBZN4FN`, `GTM-WTVHJNR`
- GTM IDs referenced in page HTML: `GTM-WTVHJNR`

---

## 13. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Tag Manager | `GTM-WTVHJNR` | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |
| Google tag (gtag.js) | — | 17 | initial:4, reload:5, pdp:4, atc:4 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-YBG65XL6PS` | 16 | initial:4, reload:4, pdp:4, atc:4 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 1 | initial:1 | 0 |
| Google Ads | `AW-554155084` | 26 | initial:5, reload:5, pdp:5, atc:11 | 0 |
| Google Merchant Center | — | 7 | initial:1, reload:2, pdp:2, atc:2 | 0 |
| Meta Pixel | `360270341980016`, `364039191513066` | 31 | initial:8, reload:6, pdp:7, atc:10 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Klaviyo | `NFpRJM` | 50 | initial:13, reload:13, pdp:12, atc:12 | 0 |
| Postscript | — | 4 | initial:1, reload:1, pdp:1, atc:1 | ⚠️ 4 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Judge.me | — | 2 | pdp:2 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 10 | initial:3, reload:2, pdp:4, atc:1 | 0 |
| Shopify | — | 39 | initial:9, consent:1, reload:5, pdp:16, atc:8 | 0 |
| Shopify Analytics (Monorail) | — | 12 | initial:1, consent:1, pdp:10 | 0 |
| Shopify CDN | — | 138 | initial:26, reload:26, pdp:60, atc:26 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`cdn.notify-me.io` (8), `www.googletagmanager.com` (4), `pbid.pro-market.net` (4), `gifts.good-apps.co` (4)

</details>

---

## 14. Findings & Recommendations

### P1 — Fix now

**[Consent] No consent banner or US opt-out mechanism**  
4 advertising platform(s) fire (Campaign Manager 360 / Floodlight, Google Ads, Google Merchant Center, Meta Pixel); no CMP, no geo-targeted banner markup and no 'Do Not Sell or Share' / 'Your Privacy Choices' link were found.  
_Recommendation:_ Enable Shopify's privacy banner (or a CMP) with region rules: opt-in for EU/UK, opt-out link + GPC for US state privacy laws (CCPA/CPRA and others).

**[GTM · Ecommerce] Not met: No purchase tags tied to Shopify thank-you / checkout URLs — GTM-WTVHJNR**  
1 active tag(s) fire on checkout / thank-you URLs or events: Google Ads Conversion #4 (554155084). This container loads on the storefront, and with Checkout Extensibility it no longer runs on checkout or thank-you pages, so these tags most likely never fire. Why it matters: Missing purchase conversions starve bidding algorithms and understate ROAS.  
_Recommendation:_ Move purchase conversions to Shopify Customer Events (app pixel or a custom pixel subscribing to checkout_completed), then confirm Google Ads / Meta purchase conversions are recording.

**[Tracking · GA4] Not met: GA4 — One implementation per property**  
G-YBG65XL6PS <- Shopify app: Google & YouTube x12, Shopify custom pixel #100204730 x6 Why it matters: Two implementations double-count events and revenue.  
_Recommendation:_ Keep one implementation per property - on Shopify usually the Google & YouTube app, unless GTM carries a richer setup (then switch GA4 off in the app).

**[Tracking · GA4] Not met: GA4 — Page view sent once per load**  
Duplicates on one page load: G-YBG65XL6PS×2 (from Shopify app: Google & YouTube, Shopify custom pixel #100204730) Why it matters: Double page views inflate traffic and deflate conversion rates; for ad pixels they distort optimisation.  
_Recommendation:_ Remove the second source (app vs GTM vs hard-coded / custom pixel).

### P2 — Address within 30 days

**[Tracking · GA4] Needs attention: GA4 — Add to cart event sent (add_to_cart)**  
No add_to_cart event in the atc phase (cart add redirected — verify in the platform's debugger). Why it matters: Product-level events drive dynamic ads, retargeting audiences and value-based optimisation.  
_Recommendation:_ Send add_to_cart on every cart add (incl. drawer/AJAX carts).

**[Tracking · GA4] Needs attention: GA4 — Single deployment route**  
Hits come from 2 routes: Shopify app: Google & YouTube x12; Shopify custom pixel #100204730 x6. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

**[Tracking · Google Ads] Needs attention: Google Ads — Single deployment route**  
Hits come from 2 routes: GTM GTM-WTVHJNR x16; Shopify app: Google & YouTube x10. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

**[Tracking · Meta] Needs attention: Meta — event_id on standard events (CAPI dedupe)**  
9 of 15 standard events (AddToCart, PageView, ViewContent) carry event_id. Missing on events from: Shopify app: Meta (Facebook & Instagram), Theme inline script. Why it matters: Without event_id, pixel + Conversions API events double-count and Meta's optimisation degrades.  
_Recommendation:_ Send a shared event_id with every standard event and its Conversions API twin.

**[Tracking · Meta] Needs attention: Meta — Single deployment route**  
Hits come from 2 routes: Shopify app: Meta (Facebook & Instagram) x13; Theme inline script x4. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ On Shopify, keep the native app integration (server-side events, consent API, maintained by the platform) and remove the GTM / theme / custom-pixel copy unless it adds something the app can't.

### P3 — Clean-up / informational

**[GTM · Google Ads] Needs attention: Enhanced conversions configured — GTM-WTVHJNR**  
No user-provided data (enhanced conversions) on Ads conversion tags. Why it matters: Typically recovers a meaningful share of conversions lost to cookie restrictions.  
_Recommendation:_ Enable enhanced conversions (hashed email/phone from the dataLayer) on purchase.

**[Tracking · Google Ads] Needs attention: Google Ads — Dynamic remarketing sends product IDs**  
No product IDs on Ads hits from the product page or cart. Why it matters: Dynamic remarketing and PMax product audiences need product IDs that match the feed.  
_Recommendation:_ Send items (id matching the Merchant Center feed) with view_item / add_to_cart.

**[Tracking · Meta] Needs attention: Meta — Single Meta pixel**  
2 Meta pixels receive data: 360270341980016, 364039191513066. Why it matters: Extra IDs split audiences and send customer data to accounts nobody watches.  
_Recommendation:_ Confirm each is owned and in use; retire leftovers from agencies or old accounts.

**[Tracking · Meta] Needs attention: Meta — Add to cart sent once per cart add**  
Sent 2× to 360270341980016 for a single cart add. Why it matters: Double add-to-cart events inflate funnel rates and remarketing audience signals.  
_Recommendation:_ Find the second trigger (app + theme script, or two listeners) and keep one.

<details><summary>Failed requests</summary>

| Vendor | Phase | Status / error | URL |
|---|---|---|---|
| Postscript | initial | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=10910 |
| Postscript | reload | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=10910 |
| Postscript | pdp | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=10910 |
| Postscript | atc | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=10910 |

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
