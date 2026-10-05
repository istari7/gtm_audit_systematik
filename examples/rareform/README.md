# Tracking & Martech Audit — Rareform

**Site:** https://www.rareform.com  
**Audit date:** 2026-10-05  
**Platform:** Shopify  
**Tag management:** Google Tag Manager (GTM-PTRFZ24)  
**Consent platform:** None detected  

---

## 1. Executive Summary

Tag management: **Google Tag Manager (GTM-PTRFZ24)**. GA4 property: `G-LRG2JKS805`. Container `GTM-PTRFZ24` scores **75/100** against best practice (1 failed, 10 warning checks). Tracking platforms (GA4 + ad pixels) score **93/100** on the events they actually received. The audit raised **1 P1**, **2 P2** and **13 P3** findings.

| Priority | Area | Finding |
|---|---|---|
| P1 | GTM · Ecommerce | Not met: No purchase tags tied to Shopify thank-you / checkout URLs — GTM-PTRFZ24 |
| P2 | GTM · Ecommerce | Needs attention: GA4 ecommerce funnel coverage — GTM-PTRFZ24 |
| P2 | Tracking · Snapchat | Needs attention: Snapchat — Single deployment route |
| P3 | Consent | No consent banner shown to this (US) visitor |
| P3 | GTM · Measurement | Needs attention: Google tag fires on Initialization / All Pages — GTM-PTRFZ24 |
| P3 | GTM · Measurement | Needs attention: Measurement ID in a variable, not hard-coded — GTM-PTRFZ24 |
| P3 | GTM · Paid social & pixels | Needs attention: Meta Pixel: implemented via template — GTM-PTRFZ24 |
| P3 | GTM · Paid social & pixels | Needs attention: TikTok Pixel: implemented via template — GTM-PTRFZ24 |
| P3 | GTM · Governance | Needs attention: Paused tags cleaned up — GTM-PTRFZ24 |
| P3 | GTM · Governance | Needs attention: Limited Custom HTML — GTM-PTRFZ24 |
| P3 | GTM · Governance | Needs attention: No unused variables — GTM-PTRFZ24 |
| P3 | GTM · Governance | Needs attention: Custom JavaScript variables kept lean — GTM-PTRFZ24 |

---

## 2. Analyst Notes

<!-- ANALYST_NOTES_START -->
- **Setup:** an **Elevar-driven** stack. Elevar's app proxy loads GTM-PTRFZ24 (score 75), which sends GA4, Google Ads, Meta and TikTok. There are no native ad apps; Klaviyo uses its app embed, and Snapchat runs from a theme inline script.
- **What's working:** single-route, product-level events for Google Ads, Meta and TikTok (event_id present); dataLayer-driven ecommerce.
- **To verify:** GA4 begin_checkout/purchase tags are paused, and an Elevar tag is tied to thank-you URLs, so confirm purchases reach GA4 and Ads through Elevar's checkout pixel / server-side. GA4 view_item / add_to_cart carry no value, and there are no Consent Mode signals.
- **Maintenance debt:** 19 Custom HTML tags, 47 Custom JS variables and 81 unused variables. Pitch angle: purchase-path verification plus a container clean-up.
- _Capture: US network, Oct 5 2026, fresh browser, consent accepted → reload → PDP → add to cart → cart. Outside-in only (no account access)._
<!-- ANALYST_NOTES_END -->

---

## 3. Next Steps — Analyst Checks & Discovery Questions

_Prospecting audit: we have no access to the brand's accounts. This is a fast first pass — the checks below take minutes from the outside, and the questions are for the discovery conversation._

**Analyst checks (no account access needed)**

- [ ] **Consent:** Visit from an EU/UK VPN: does a banner appear, and do ad pixels wait for consent? — _Browser via EU VPN + DevTools → Network_

**Discovery questions for the prospect**

- **Purchase tracking:** Since Shopify's checkout upgrade (Checkout Extensibility), do Google Ads / GTM purchase conversions still match Shopify orders? Some purchase tags here are tied to the old thank-you page.
- **Meta:** Meta runs through GTM / theme code, not the native Shopify app — is the Conversions API sent server-side anywhere (Elevar, Stape, a CAPI gateway)?
- **Google Ads:** Which conversion action is primary for purchases — the Google & YouTube app, a GTM tag or a GA4 import — and is enhanced conversions on?
- **TikTok:** TikTok runs outside the native Shopify app — is the Events API connected for purchases?
- **Consent:** Do you sell into the EU/UK or Quebec, and how is consent handled for those visitors?
- **Email / SMS:** Are browse- and cart-abandonment flows live in Klaviyo, and are Viewed Product / Added to Cart metrics recording?

---

## 4. GTM Container Audit — Configuration vs Best Practice

Each check compares the live container configuration (decoded from the published container JSON) with current best practice, weighted by business impact. Score = impact-weighted share of checks passed (warnings count half).

### `GTM-PTRFZ24` — score 75/100 (✅ 11 · ⚠️ 10 · ❌ 1)

|  | Impact | Area | Check | Evidence | Recommendation |
|---|---|---|---|---|---|
| ❌ | High | Ecommerce | No purchase tags tied to Shopify thank-you / checkout URLs | 1 active tag(s) fire on checkout / thank-you URLs or events: Custom HTML #549. This container loads on the storefront, and with Checkout Extensibility it no longer runs on checkout or thank-you pages, so these tags most… | Move purchase conversions to Shopify Customer Events (app pixel or a custom pixel subscribing to checkout_completed), then confirm Google Ads / Meta purchase conversions are recor… |
| ⚠️ | High | Ecommerce | GA4 ecommerce funnel coverage | Configured in GTM: add_to_cart, remove_from_cart, select_item, view_cart, view_item, view_item_list. Missing core: begin_checkout; missing recommended: add_shipping_info, add_payment_info. `purchase` is not in GTM — exp… | Add the missing funnel events with items[] from the dataLayer. |
| ⚠️ | Medium | Measurement | Google tag fires on Initialization / All Pages | Late-firing Google tag(s): #295 | Fire the Google tag on the Initialization – All Pages trigger so config/consent are set before events. |
| ⚠️ | Medium | Governance | Limited Custom HTML | 19 active Custom HTML tag(s) (44% of active tags). | Replace with templates where one exists. |
| ⚠️ | Low | Measurement | Measurement ID in a variable, not hard-coded | 12 of 12 GA4 event tags hard-code the measurement ID. | Reference a Constant / Lookup Table variable so the ID changes in one place. |
| ⚠️ | Low | Paid social & pixels | Meta Pixel: implemented via template | 2 Custom HTML tag(s), 0 template tag(s). | Move to the vendor's Community Template (permissions-scoped, consent-aware). |
| ⚠️ | Low | Paid social & pixels | TikTok Pixel: implemented via template | 1 Custom HTML tag(s), 0 template tag(s). | Move to the vendor's Community Template (permissions-scoped, consent-aware). |
| ⚠️ | Low | Governance | Paused tags cleaned up | 6 paused tag(s). | Delete paused tags no longer needed. |
| ⚠️ | Low | Governance | No unused variables | 81 variable(s) not referenced by any tag, trigger or variable: Custom JavaScript #94, __cvt_32699077_188 #95, DLV - ecommerce.detail.products.0.brand, DLV - ecommerce.detail.products.0.compare_at_price, DLV - ecommerce.… | Remove unused variables. |
| ⚠️ | Low | Governance | Custom JavaScript variables kept lean | 47 Custom JavaScript variable(s). | Push values into the dataLayer instead of computing them in GTM. |
| ⚠️ | Low | Governance | Universal Analytics removed | 0 UA tag(s) (0 active); UA IDs UA-34408006-1. | Delete UA tags, GA Settings variables and UA triggers. |
| ✅ | High | Measurement | GA4 sent from one source only | No GA4 property is shared between GTM and a Shopify app. | — |
| ✅ | High | Ecommerce | Ecommerce events carry items[] | All ecommerce event tags send items (dataLayer ecommerce object or items parameter). | — |
| ✅ | High | Google Ads | Conversion Linker present | 8 Ads/Floodlight tag(s); conversion linker tags: 1. | — |
| ✅ | High | Google Ads | Purchase conversion passes value, currency, order ID | Ads conversion #483 passes value, currency and order ID. | — |
| ✅ | Medium | Measurement | Single GA4 Google tag | GA4 Google tag IDs: G-LRG2JKS805. | — |
| ✅ | Medium | Google Ads | Enhanced conversions configured | User-provided data configured on Ads conversions. | — |
| ✅ | Medium | Paid social & pixels | Meta events carry event_id (CAPI dedupe) | event_id found on Meta events. | — |
| ✅ | Medium | Performance | Tags firing on every page kept small | 4 tag(s) fire on every page load without filters; container 561.8 KB. | — |
| ✅ | Low | Google Ads | Dynamic remarketing (product feed) | Remarketing passes product data. | — |
| ✅ | Low | Governance | No orphan tags | 0 active tag(s) without a firing trigger. | — |
| ✅ | Low | Governance | No duplicate tags | No identical tags. | — |
| ℹ️ | Medium | Consent | Consent Mode defaults set in GTM | No consent template or Consent Initialization trigger in the container, and no gtag consent default seen in the dataLayer. | Set Consent Mode v2 defaults on Consent Initialization (CMP template) and update on choice. |
| ℹ️ | Low | Governance | Tag names published (naming convention auditable) | 22 of 49 tags publish their names. | — |

---

## 5. Tracking Platform Audit — GA4 & Ad Platforms

Each platform is judged on the events it actually received during the visit (page view → product view → add to cart), whatever deployed it (GTM, Shopify app, custom pixel, hard-coded). Overall tracking score: **93/100** (✅ 30 · ⚠️ 5 · ❌ 0).

| Platform | Score | ✅ | ⚠️ | ❌ | Deployed via (hits) | Events seen (phase: event×n) |
|---|---|---|---|---|---|---|
| GA4 | 86 | 7 | 3 | 0 | Shopify app proxy: elevar ×16; GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar) ×3; Shopify native app pixel (sandboxed) ×1 | initial: page_view×1, (none)×1; reload: user_engagement×2, page_view×1; pdp: scroll×2, user_engagement×2, page_view×1, view_item×1; atc: scroll×1, add_to_cart×1, timer_20secs×1, user_engagement×3, page_view×1, view_cart×1 |
| Google Ads | 100 | 5 | 0 | 0 | GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar) ×27; Shopify app proxy: elevar ×27; Shopify native app pixel (sandboxed) ×2 | initial: page_view×2, remarketing×4, gtag.config×3, user_id_update×1; reload: page_view×2, gtag.config×3, user_id_update×1, remarketing×4; pdp: page_view×2, gtag.config×3, view_item×4, user_id_update×1, remarketing×4; atc: add_to_cart×4, conversion×4, page_vi… |
| Meta | 100 | 8 | 0 | 0 | GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar) ×7 | initial: PageView×1; reload: PageView×1; pdp: PageView×1, ViewContent×1; atc: SubscribedButtonClick×1, AddToCart×1, PageView×1 |
| TikTok | 100 | 7 | 0 | 0 | GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar) ×8 | initial: LandingPageView×1, Pageview×1; reload: Pageview×1; pdp: Pageview×1, ViewContent×1; atc: AddToCart×1, Pageview×1 |
| Klaviyo | 100 | 2 | 0 | 0 | Shopify app embed: klaviyo-email-marketing-sms ×120 | initial: (onsite.js loaded)×30; reload: (onsite.js loaded)×30; pdp: (onsite.js loaded)×30; atc: (onsite.js loaded)×30 |
| Snapchat | 50 | 0 | 1 | 0 | Theme inline script ×18; Shopify app proxy: elevar ×4; Shopify native app pixel (sandboxed) ×2 | initial: (request)×9; reload: (request)×5; pdp: (request)×5; atc: (request)×5 |

### GA4 — 86/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Medium | Product view event carries items, value, currency | view_item sent (1×); missing: value. | Add value to view_item. |
| ⚠️ | Medium | Add to cart event carries items, value, currency | add_to_cart sent (1×); missing: value. | Add value to add_to_cart. |
| ⚠️ | Medium | Consent Mode signals on hits | No gcs parameter on any GA4 hit. | Implement Consent Mode v2 (default + update). |
| ✅ | Low | Single GA4 property | GA4 property: G-LRG2JKS805. | — |
| ✅ | High | One implementation per property | G-LRG2JKS805 <- Shopify app proxy: elevar, GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar), Shopify native app pixel (sandboxed) | — |
| ✅ | High | Page view sent once per load | G-LRG2JKS805×1 on one page load. | — |
| ✅ | High | page_location is the real page URL | page_location values are storefront URLs. | — |
| ✅ | Medium | Add to cart sent once per cart add | add_to_cart sent once per destination. | — |
| ✅ | Low | Engagement / enhanced measurement events | Seen: scroll, user_engagement. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ga. | — |
| ℹ️ | Low | Deployment route | Sent via: Shopify app proxy: elevar x16; GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar) x3; Shopify native app pixel (sandboxed) x1. Native Shopify app not used for this platform - the app would add server-side e… | — |

### Google Ads — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Google Ads account | Google Ads account: AW-991876766. | — |
| ✅ | Medium | Enhanced conversions enabled | User-provided data collection is configured. | — |
| ✅ | Medium | Dynamic remarketing sends product IDs | Product IDs present on product-page / cart hits. | — |
| ✅ | Low | Add-to-cart signal reaches Google Ads | 22 Ads hit(s) after add-to-cart. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _gcl_au. | — |
| ℹ️ | Low | Deployment route | Sent via: GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar) x27; Shopify app proxy: elevar x27; Shopify native app pixel (sandboxed) x2. Native Shopify app not used for this platform - the app would add server-side … | — |

### Meta — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single Meta pixel | Meta pixel: 769735243115963. | — |
| ✅ | High | Page view sent once per load | 769735243115963×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | High | event_id on standard events (CAPI dedupe) | 6 of 6 standard events (AddToCart, PageView, ViewContent) carry event_id. | — |
| ✅ | Low | Advanced matching | Hashed user data seen on events. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _fbp. | — |
| ℹ️ | Low | Deployment route | Sent via: GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar) x7. Native Shopify app not used for this platform - the app would add server-side events (CAPI / Events API) and Shopify consent handling. | — |

### TikTok — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Low | Single TikTok pixel | TikTok pixel: CBON3P3C77U9ABNNULLG. | — |
| ✅ | High | Page view sent once per load | CBON3P3C77U9ABNNULLG×1 on one page load. | — |
| ✅ | Medium | Product view event carries content_ids, value, currency | ViewContent sent (1×) with product, value and currency. | — |
| ✅ | Medium | Add to cart sent once per cart add | AddToCart sent once per destination. | — |
| ✅ | Medium | Add to cart event carries content_ids, value, currency | AddToCart sent (1×) with product, value and currency. | — |
| ✅ | Medium | event_id for Events API dedupe | event_id present. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: _ttp. | — |
| ℹ️ | Low | Deployment route | Sent via: GTM GTM-PTRFZ24 (loaded by Shopify app proxy: elevar) x8. Native Shopify app not used for this platform - the app would add server-side events (CAPI / Events API) and Shopify consent handling. | — |

### Klaviyo — 100/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ✅ | Medium | Onsite tracking (klaviyo.js) loaded | klaviyo.js loads. | — |
| ✅ | Medium | First-party ID cookie set | Cookies after the visit: __kla_id. | — |
| ℹ️ | Medium | Viewed Product tracked (browse abandonment) | No Viewed Product event (only identified profiles are tracked — anonymous visitors expected to show none). | Confirm Viewed Product is enabled in the Klaviyo Shopify integration. |
| ℹ️ | Low | Deployment route | Sent via: Shopify app embed: klaviyo-email-marketing-sms x120. | — |

### Snapchat — 50/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | High | Single deployment route | Hits come from 2 routes: Theme inline script x18; Shopify app proxy: elevar x4; Shopify native app pixel (sandboxed) x2. | Consolidate to one deployment route per platform. |
| ℹ️ | Low | Pixel active | 24 hit(s): (request)×24. | — |

### Stack — 75/100

|  | Impact | Check | Evidence | Recommendation |
|---|---|---|---|---|
| ⚠️ | Low | Third-party request volume | 1148 third-party requests across the visit (20 identified platforms). | Audit apps/pixels that don't earn their weight. |
| ✅ | Low | Session-replay tools | 1: Microsoft Clarity. | — |
| ℹ️ | Low | Ad platforms in use | 6: Campaign Manager 360 / Floodlight, Google Ads, Meta Pixel, Snapchat Pixel, Tapad, TikTok Pixel. | — |

---

## 6. Container Inventory & Settings

### 6.1 Container Deep Dive — `GTM-PTRFZ24`

| Tag type | Active | Paused |
|---|---|---|
| Custom HTML | 19 | 1 |
| GA4 Event | 12 | 4 |
| Google Ads Remarketing | 7 | 0 |
| Custom Template | 2 | 0 |
| Google Ads Conversion | 1 | 1 |
| Google Tag (GA4/Ads config) | 1 | 0 |
| Conversion Linker | 1 | 0 |

**Custom templates:**

| Template | Vendor (inferred) | Tags using it | Injects |
|---|---|---|---|
| `__cvt_32699077_188` | Elevar | 0 | — |
| `__cvt_32699077_260` | Elevar | 1 | https://monitoring.getelevar.com/* |
| `__cvt_32699077_283` | Elevar | 1 | — |

**Custom HTML tags:**

| Tag | Status | Vendors / IDs | Fires on | Preview |
|---|---|---|---|---|
| #310 | active | Meta Pixel, Meta Pixel: 769735243115963 | {{Event}} equals "dl_user_data" |  <script type="text/gtmscript">!function(b,e,f,g,a,c,d){b.fbq\|\|(a=b.fbq=function(){a.ca… |
| Facebook - Initiate Checkout | active | — | {{Event}} equals "dl_begin_checkout" | <script type="text/gtmscript">fbq("trackSingle","769735243115963","InitiateCheckout",{con… |
| Facebook - Add to Cart | active | — | {{Event}} equals "dl_add_to_cart" | <script type="text/gtmscript">fbq("trackSingle","769735243115963","AddToCart",{content_id… |
| Facebook - Add Payment Info | active | — | {{Event}} equals "dl_add_payment_info" | <script type="text/gtmscript">fbq("trackSingle","769735243115963","AddPaymentInfo",{conte… |
| Facebook - Product View | active | — | {{Event}} equals "dl_view_item" | <script type="text/gtmscript">fbq("trackSingle","769735243115963","ViewContent",{content_… |
| Facebook - Purchase | active | Elevar, Meta Pixel, Meta Pixel: 769735243115963 | {{Event}} equals "dl_purchase" |  <script type="text/gtmscript">!function(b,e,f,g,a,c,d){b.fbq\|\|(a=b.fbq=function(){a.ca… |
| #493 | active | TikTok Pixel | {{Event}} equals "gtm.js" | <script type="text/gtmscript">!function(d,g,e){d.TiktokAnalyticsObject=e;var a=d[e]=d[e]\… |
| #494 | paused | — | {{Event}} equals "dl_user_data" | — |
| Facebook - Email Signup | active | — | {{DLV - lead_type}} contains "email" AND {{Event}} equals "dl_subscribe" | <script type="text/gtmscript">fbq("trackSingle","769735243115963","Lead",{},{eventID:"{{D… |
| #480 | active | — | {{Event}} equals "gtm.js" | <script type="text/gtmscript">(function(){window.dataLayer=window.dataLayer\|\|[];window.… |
| TikTok - Page View | active | — | {{Event}} equals "dl_user_data" | <script type="text/gtmscript">{{DLV - user_properties.customer_email}}&&ttq.identify({ext… |
| TikTok - Add to Cart | active | — | {{Event}} equals "dl_add_to_cart" | <script type="text/gtmscript">{{DLV - user_properties.customer_email}}&&ttq.identify({ext… |
| TikTok - Complete Payment | active | — | {{Event}} equals "dl_purchase" | <script type="text/gtmscript">ttq.identify({external_id:"{{DLV - user_properties.customer… |
| TikTok - Product View | active | — | {{Event}} equals "dl_view_item" | <script type="text/gtmscript">{{DLV - user_properties.customer_email}}&&ttq.identify({ext… |
| TikTok - Initiate Checkout | active | — | {{Event}} equals "dl_begin_checkout" | <script type="text/gtmscript">{{DLV - user_properties.customer_email}}&&ttq.identify({ext… |
| TikTok - Collection View | active | — | {{Event}} equals "dl_view_item_list" | <script type="text/gtmscript">{{DLV - user_properties.customer_email}}&&ttq.identify({ext… |
| TikTok - Place An Order | active | — | {{Event}} equals "dl_purchase" | <script type="text/gtmscript">ttq.identify({external_id:"{{DLV - user_properties.customer… |
| #506 | active | — | {{Event}} equals "dl_view_search_results" | <script type="text/gtmscript">{{DLV - user_properties.customer_email}}&&ttq.identify({ext… |
| Facebook - SMS Signup | active | — | {{Event}} equals "dl_subscribe" AND {{DLV - lead_type}} contains "phone" | <script type="text/gtmscript">fbq("trackSingleCustom","769735243115963","SMSSignup",{},{e… |
| #549 | active | Elevar | {{Event}} equals "dl_user_data" AND {{URL - Path}} matches regex "thank_you\|thank-you\|\… | <script type="text/gtmscript">window.elevar_userdata_eventid={{DLV - event_id}};</script>  |

<details><summary>All active tags with firing conditions</summary>

| Tag | Type | IDs / event | Fires on | Consent |
|---|---|---|---|---|
| Google Ads Remarketing - Pageview | Google Ads Remarketing | {"conversionId": "991876766"} | {{Event}} equals "gtm.load" | — |
| #295 | Google Tag (GA4/Ads config) | {"tagId": "G-LRG2JKS805"} | {{Event}} equals "dl_user_data" | — |
| #296 | GA4 Event | sign_up | {{Event}} equals "dl_sign_up" | — |
| #298 | Custom Template | {} | {{Event}} equals "gtm.timer" AND {{DLV - gtm.triggers}} matches regex "(^$\|((^\|,)32699077_219($\|,)))" | — |
| #312 | GA4 Event | select_item | {{Event}} equals "dl_select_item" | — |
| #315 | GA4 Event | email_signup | {{DLV - lead_type}} contains "email" AND {{Event}} equals "dl_subscribe" | — |
| Google Ads Remarketing - View Item List | Google Ads Remarketing | {"conversionId": "991876766"} | {{Event}} equals "dl_view_item_list" | — |
| Google Ads Remarketing - Add to Cart | Google Ads Remarketing | {"conversionId": "991876766"} | {{Event}} equals "dl_add_to_cart" | — |
| #342 | Custom Template | {} | {{Event}} matches regex ".*" | — |
| #345 | GA4 Event | search_results | {{Event}} equals "dl_view_search_results" | — |
| #348 | Conversion Linker | {} | {{Event}} equals "gtm.js" | — |
| Google Ads Remarketing - View Item | Google Ads Remarketing | {"conversionId": "991876766"} | {{Event}} equals "dl_view_item" | — |
| #356 | GA4 Event | login | {{Event}} equals "dl_login" | — |
| #359 | GA4 Event | view_item_list | {{Event}} equals "dl_view_item_list", {{Event}} equals "dl_view_search_results" | — |
| Google Ads Remarketing - Purchase | Google Ads Remarketing | {"conversionId": "991876766"} | {{Event}} equals "dl_purchase" | — |
| Google Ads Remarketing - Search Results | Google Ads Remarketing | {"conversionId": "991876766"} | {{Event}} equals "dl_view_search_results" | — |
| #366 | GA4 Event | remove_from_cart | {{Event}} equals "dl_remove_from_cart" | — |
| Google Ads Remarketing - Cart Page | Google Ads Remarketing | {"conversionId": "991876766"} | {{Event}} equals "dl_view_cart" | — |
| #369 | GA4 Event | add_to_cart | {{Event}} equals "dl_add_to_cart" | — |
| #370 | GA4 Event | view_cart | {{Event}} equals "dl_view_cart" | — |
| #371 | GA4 Event | view_item | {{Event}} equals "dl_view_item" | — |
| Google Ads Conversion - Purchase 2 | Google Ads Conversion | {"conversionId": "991876766", "conversionLabel": "rCzYCJ7ns8QBEJ6t-9gD"} | {{Event}} equals "dl_purchase" | — |
| #508 | GA4 Event | timer_20secs | {{Event}} equals "gtm.timer" AND {{DLV - gtm.triggers}} matches regex "(^$\|((^\|,)32699077_507($\|,)))" | — |
| #517 | GA4 Event | sms_signup | {{Event}} equals "dl_subscribe" AND {{DLV - lead_type}} contains "phone" | — |

</details>

**Reconstructed export:** `containers/GTM-PTRFZ24.export.json` — 49 tags, 27 triggers, 170 variables; template source missing for cvt_32699077_260, cvt_32699077_283

**Custom dataLayer events used as triggers (15):** `dl_add_payment_info`, `dl_add_shipping_info`, `dl_add_to_cart`, `dl_begin_checkout`, `dl_login`, `dl_purchase`, `dl_remove_from_cart`, `dl_select_item`, `dl_sign_up`, `dl_subscribe`, `dl_user_data`, `dl_view_cart`, `dl_view_item`, `dl_view_item_list`, `dl_view_search_results`

**Auto-event listeners:** Click (all elements), Element Visibility, Scroll Depth, Timer, YouTube Video

---

### 6.2 Google Tag Settings — `AW-991876766`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Ads data terms of service | {"instanceDestinationId": "AW-991876766"} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "autoAddressEnabled": true, … |
| Automatic user-provided data detection | {"instanceDestinationId": "AW-991876766"} |
| Enhanced measurement: form interactions | {"includeParams": false, "instanceDestinationId": "AW-991876766"} |
| __ccd_enable_cm | {"instanceDestinationId": "AW-991876766"} |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":2,\"args\":[{\"booleanExpressio… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Google Ads destination | {"destinationId": "AW-991876766", "ignoreDupeGtagConfigCalls": false, "enableVariablesInDestinationId": false} |
| Remarketing / conversion page view | {"containerId": "AW-991876766"} |

---

### 6.3 Google Tag Settings — `G-LRG2JKS805`

gtag.js container compiled from the Google tag / GA4 admin settings (not editable in GTM).

| Feature | Settings |
|---|---|
| Automatic events | {"enableOutboundClick": true, "enableScroll": true, "enableDownload": true, "enableHistoryEvents": true, "enableForm": true, "enableVideo": true, "enablePageVi… |
| __ogt_defer_custom_events | {"isDeferred": true} |
| User-provided data collection (enhanced conversions) | {"isAutoEnabled": true, "isManualEnabled": false, "autoPhoneEnabled": true, "autoCollectExclusionSelectors": [{"exclusionSelector": ""}], "isEnabled": true, "a… |
| Product settings | {"instanceDestinationId": "G-LRG2JKS805", "isChinaVipRegionMacroResult": 0} |
| Google Signals | {"googleSignals": "ENABLED", "instanceDestinationId": "G-LRG2JKS805"} |
| Regional data collection settings | {"settingsTable": [{"redactFieldGroup": "DEVICE_AND_GEO", "disallowAllRegions": false, "disallowedRegions": ""}, {"redactFieldGroup": "GOOGLE_SIGNALS", "disall… |
| Enhanced conversions settings | {"instanceDestinationId": "G-LRG2JKS805"} |
| Enhanced measurement: file downloads | {"includeParams": true, "instanceDestinationId": "G-LRG2JKS805"} |
| Enhanced measurement: outbound clicks | {"includeParams": true, "instanceDestinationId": "G-LRG2JKS805"} |
| Enhanced measurement: page changes (history events) | {"historyEvents": true, "includeParams": true, "instanceDestinationId": "G-LRG2JKS805"} |
| Enhanced measurement: scrolls | {"includeParams": true, "instanceDestinationId": "G-LRG2JKS805"} |
| Enhanced measurement: site search | {"searchQueryParams": "q,s,search,query,keyword", "includeParams": true, "instanceDestinationId": "G-LRG2JKS805"} |
| Enhanced measurement: video engagement | {"includeParams": true, "instanceDestinationId": "G-LRG2JKS805"} |
| Key events (conversion marking rules) | {"conversionRules": [{"matchingRules": "{\"type\":5,\"args\":[{\"stringValue\":\"purchase\"},{\"contextValue\":{\"namespaceType\":1,\"keyParts\":[\"eventName\"… |
| Create-event rules | {"eventName": "plp_viewed_product", "isCopy": true, "instanceDestinationId": "G-LRG2JKS805", "precompiledRule": {"new_event_name": "plp_viewed_product", "merge… |
| User-provided data attached to hits | {"acceptAutomatic": false, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":3,\"args\":[{\"booleanExpressi… |
| User-provided data attached to hits | {"acceptAutomatic": true, "acceptCode": true, "acceptManualSelector": true, "acceptUserData": true, "matchingRules": "{\"type\":1,\"args\":[{\"booleanExpressio… |
| Automatic PII redaction (URL/email) | {"redactEmail": false, "instanceDestinationId": "G-LRG2JKS805"} |
| GA4 <-> Google Ads link | {"instanceDestinationId": "G-LRG2JKS805"} |
| GA4 destination | {"ignoreDupeGtagConfigCalls": false, "destinationId": "G-LRG2JKS805", "enableVariablesInDestinationId": false} |
| Google tag configuration | {"trackingId": "G-LRG2JKS805", "sessionDuration": 0} |

---

## 7. Measurement & Conversion IDs

| Platform | IDs | Source |
|---|---|---|
| GA4 | `G-LRG2JKS805` | GTM-PTRFZ24 (container) |
| Google Ads | `AW-991876766`, `AW-991876766/rCzYCJ7ns8QBEJ6t-9gD` | GTM-PTRFZ24 (container) |
| Universal Analytics | `UA-34408006-1` | GTM-PTRFZ24 (container) |
| Other tags | Meta Pixel: 769735243115963 | GTM-PTRFZ24 (container) |
| Google Ads | `AW-991876766` | network |
| Meta Pixel | `769735243115963` | network |
| Snapchat Pixel | `82a2c7d2-f335-45c7-b646-bd7867a0a69a` | network |
| TikTok Pixel | `CBON3P3C77U9ABNNULLG` | network |
| Google Analytics 4 | `G-LRG2JKS805` | network |
| Klaviyo | `kL74Vq` | network |
| Microsoft Clarity | `fvcxwnmojr` | network |
| Meta Pixel | `769735243115963` | hard-coded in page HTML |
| Klaviyo | `kL74Vq` | hard-coded in page HTML |
| Microsoft Clarity | `fvcxwnmojr` | hard-coded in page HTML |

---

## 8. Ecommerce Tracking

Product page visited: https://www.rareform.com/products/mystery-blake-keychain · add-to-cart clicked: yes

| GA4 event | Configured in container | Observed on network |
|---|---|---|
| `view_item_list` | ✅ | — |
| `select_item` | ✅ | — |
| `view_item` | ✅ | ✅ |
| `add_to_cart` | ✅ | ✅ |
| `remove_from_cart` | ✅ | — |
| `view_cart` | ✅ | ✅ |
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
| Google consent state (window.google_tag_data) | {"ad_storage": {"default": null, "update": null}, "analytics_storage": {"default": null, "update": null}, "ad_user_data": {"default": null, "update": null}, "ad_personalization": {"default": null, "update": null}} |
| Tracking vendors firing before consent | Campaign Manager 360 / Floodlight, Google Ads, Google Analytics 4, Meta Pixel, Microsoft Clarity, Snapchat Pixel, Tapad, TikTok Pixel |
| Scripts held until consent (text/plain, data-consent…) | — |
| Banner still visible after accept + reload | no |

**Consent configuration inside GTM:**

| Container | Consent types referenced | Consent templates | Tags with extra consent checks | CMP hints |
|---|---|---|---|---|
| `GTM-PTRFZ24` | — | — | 0 / 43 | — |

---

## 10. Event Flow by Visit Phase

Phases: `initial` = first load before consent · `reload` = after consent + reload · `pdp` = product page · `atc` = after add-to-cart.

| Destination | Phase | Events (count) | Consent state (gcs) |
|---|---|---|---|
| GA4 `G-LRG2JKS805` | initial | page_view×1, (no event name)×1 | — |
| GA4 `G-LRG2JKS805` | consent | timer_20secs×1 | — |
| GA4 `G-LRG2JKS805` | reload | user_engagement×2, page_view×1 | — |
| GA4 `G-LRG2JKS805` | pdp | scroll×2, user_engagement×2, page_view×1, view_item×1 | — |
| GA4 `G-LRG2JKS805` | atc | scroll×1, add_to_cart×1, timer_20secs×1, user_engagement×3, page_view×1, view_cart×1 | — |
| TikTok `CBON3P3C77U9ABNNULLG` | initial | ?×1 | — |
| TikTok `CBON3P3C77U9ABNNULLG` | reload | ?×4 | — |
| TikTok `CBON3P3C77U9ABNNULLG` | pdp | ?×2 | — |
| TikTok `CBON3P3C77U9ABNNULLG` | atc | ?×6 | — |
| Google Ads `AW-991876766` | initial | remarketing×1, gtag.config×1 | — |
| Google Ads `AW-991876766` | reload | gtag.config×1, remarketing×1 | — |
| Google Ads `AW-991876766` | pdp | gtag.config×1, view_item×1, remarketing×1 | — |
| Google Ads `AW-991876766` | atc | add_to_cart×1, vnKYCL2r-eYcEJ6t-9gD×3, gtag.config×1, view_cart×1, remarketing×1 | — |

**dataLayer pushes observed:**

- `initial`: gtm.js, gtm.dom, gtm.timer, gtm.load, dl_user_data, gtag:js, gtag:config:AW-991876766
- `reload`: gtm.js, dl_user_data, gtag:js, gtag:config:AW-991876766, gtm.dom, gtm.timer, gtm.load, gtm.scrollDepth
- `pdp`: gtm.js, dl_user_data, gtag:js, gtag:config:AW-991876766, gtm.dom, dl_view_item, gtm.timer, gtm.load, gtm.scrollDepth
- `atc`: gtm.js, dl_user_data, gtag:js, gtag:config:AW-991876766, gtm.dom, dl_view_item, gtm.timer, gtm.load, gtm.scrollDepth, gtm.click, dl_add_to_cart, gtag:event:conversion

---

## 11. Tag Management & Infrastructure

| Container | Kind | Version | Size | Captured | Served from | Active tags | Paused | Variables | Triggers |
|---|---|---|---|---|---|---|---|---|---|
| `GTM-PTRFZ24` | GTM | 21 | 561.8 KB | reload | googletagmanager.com | 43 | 6 | 178 | 27 |
| `AW-991876766` | GTAG | 1 | 480.6 KB | reload | googletagmanager.com | 11 | 0 | 4 | 4 |
| `G-LRG2JKS805` | GTAG | 2 | 575.3 KB | reload | googletagmanager.com | 23 | 0 | 7 | 5 |

- Google tag IDs live in `window.google_tag_manager`: `AW-991876766`, `G-LRG2JKS805`, `GTM-PTRFZ24`
- GTM IDs referenced in page HTML: `GTM-PTRFZ24`

---

## 12. Platform Inventory (observed on the network)

### Tag management

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Tag Manager | `GTM-PTRFZ24` | 4 | initial:1, reload:1, pdp:1, atc:1 | 0 |
| Google tag (gtag.js) | — | 11 | initial:2, reload:3, pdp:3, atc:3 | 0 |

### Analytics

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Google Analytics 4 | `G-LRG2JKS805` | 20 | initial:2, consent:1, reload:3, pdp:6, atc:8 | 0 |

### Advertising

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Campaign Manager 360 / Floodlight | — | 3 | initial:2, atc:1 | 0 |
| Google Ads | `AW-991876766` | 56 | initial:10, reload:10, pdp:14, atc:22 | 0 |
| Meta Pixel | `769735243115963` | 15 | initial:3, reload:3, pdp:4, atc:5 | 0 |
| Snapchat Pixel | `82a2c7d2-f335-45c7-b646-bd7867a0a69a` | 24 | initial:9, reload:5, pdp:5, atc:5 | 0 |
| Tapad | — | 1 | initial:1 | 0 |
| TikTok Pixel | `CBON3P3C77U9ABNNULLG` | 37 | initial:6, consent:1, reload:9, pdp:8, atc:13 | 0 |

### Session replay / UX

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Microsoft Clarity | `fvcxwnmojr` | 34 | initial:8, consent:1, reload:8, pdp:8, atc:9 | 0 |

### Personalisation / testing / search

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Rebuy | — | 124 | initial:35, consent:3, reload:32, pdp:32, atc:22 | 0 |

### Email / SMS / CRM

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Klaviyo | `kL74Vq` | 139 | initial:34, reload:35, pdp:35, atc:35 | 0 |
| Postscript | — | 16 | initial:4, reload:4, pdp:4, atc:4 | ⚠️ 4 |

### Reviews / UGC / loyalty

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Judge.me | — | 2 | pdp:2 | 0 |

### Support / chat

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Gorgias | — | 8 | initial:2, reload:2, pdp:2, atc:2 | 0 |

### Commerce platform

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| Shop Pay | — | 8 | initial:2, reload:1, pdp:4, atc:1 | 0 |
| Shopify | — | 26 | initial:5, reload:2, pdp:9, atc:10 | 0 |
| Shopify Analytics (Monorail) | — | 6 | initial:1, consent:1, pdp:2, atc:2 | 0 |
| Shopify CDN | — | 408 | initial:99, reload:96, pdp:130, atc:83 | 0 |

### Payments / BNPL

| Platform | IDs | Requests | By phase | Failed |
|---|---|---|---|---|
| PayPal | — | 10 | atc:10 | 0 |

<details><summary>Unclassified third-party hosts</summary>

`d1y4yqugo2tfyu.cloudfront.net` (16), `api.config-security.com` (14), `rareform.myshopify.com` (14), `api-c0.pscrpt.com` (12), `sapi.negate.io` (8), `content.9gtb.com` (8), `cdn.zigpoll.com` (8), `review-images.judgeme.com` (8), `play.google.com` (5), `conf.config-security.com` (4), `static.bogos.io` (4), `popups.pscrpt.com` (4), `intg.snapchat.com` (4), `ext.spinwheelapp.com` (4), `api.zigpoll.com` (4), `extensions.shopifycdn.com` (4), `pay.google.com` (3), `api.country.is` (2), `nr.pspt.store` (2), `api.pscrpt.com` (1), `www.googletagmanager.com` (1), `analytics-ipv6.tiktokw.us` (1)

</details>

---

## 13. Findings & Recommendations

### P1 — Fix now

**[GTM · Ecommerce] Not met: No purchase tags tied to Shopify thank-you / checkout URLs — GTM-PTRFZ24**  
1 active tag(s) fire on checkout / thank-you URLs or events: Custom HTML #549. This container loads on the storefront, and with Checkout Extensibility it no longer runs on checkout or thank-you pages, so these tags most likely never fire. Why it matters: Missing purchase conversions starve bidding algorithms and understate ROAS.  
_Recommendation:_ Move purchase conversions to Shopify Customer Events (app pixel or a custom pixel subscribing to checkout_completed), then confirm Google Ads / Meta purchase conversions are recording.

### P2 — Address within 30 days

**[GTM · Ecommerce] Needs attention: GA4 ecommerce funnel coverage — GTM-PTRFZ24**  
Configured in GTM: add_to_cart, remove_from_cart, select_item, view_cart, view_item, view_item_list. Missing core: begin_checkout; missing recommended: add_shipping_info, add_payment_info. `purchase` is not in GTM — expected on Shopify (checkout runs outside GTM); confirm a Customer Events pixel or app sends it. Why it matters: Gaps or split ownership break funnel reports and double-count shared events.  
_Recommendation:_ Add the missing funnel events with items[] from the dataLayer.

**[Tracking · Snapchat] Needs attention: Snapchat — Single deployment route**  
Hits come from 2 routes: Theme inline script x18; Shopify app proxy: elevar x4; Shopify native app pixel (sandboxed) x2. Why it matters: Parallel routes double-count, drift apart, and make consent handling inconsistent.  
_Recommendation:_ Consolidate to one deployment route per platform.

### P3 — Clean-up / informational

**[Consent] No consent banner shown to this (US) visitor**  
6 ad platform(s) fire without a banner — normal for US opt-out. A US opt-out link (Do Not Sell / Your Privacy Choices) is present.  
_Recommendation:_ Confirm EU/UK visitors get an opt-in banner and that the US opt-out link + GPC actually suppress ad pixels (Shopify Customer Privacy sale_of_data).

**[GTM · Measurement] Needs attention: Google tag fires on Initialization / All Pages — GTM-PTRFZ24**  
Late-firing Google tag(s): #295 Why it matters: Late configuration drops early events and session attribution.  
_Recommendation:_ Fire the Google tag on the Initialization – All Pages trigger so config/consent are set before events.

**[GTM · Measurement] Needs attention: Measurement ID in a variable, not hard-coded — GTM-PTRFZ24**  
12 of 12 GA4 event tags hard-code the measurement ID. Why it matters: Hard-coded IDs make property migrations and staging setups error-prone.  
_Recommendation:_ Reference a Constant / Lookup Table variable so the ID changes in one place.

**[GTM · Paid social & pixels] Needs attention: Meta Pixel: implemented via template — GTM-PTRFZ24**  
2 Custom HTML tag(s), 0 template tag(s). Why it matters: Templates are safer, auditable and respect consent settings.  
_Recommendation:_ Move to the vendor's Community Template (permissions-scoped, consent-aware).

**[GTM · Paid social & pixels] Needs attention: TikTok Pixel: implemented via template — GTM-PTRFZ24**  
1 Custom HTML tag(s), 0 template tag(s). Why it matters: Templates are safer, auditable and respect consent settings.  
_Recommendation:_ Move to the vendor's Community Template (permissions-scoped, consent-aware).

**[GTM · Governance] Needs attention: Paused tags cleaned up — GTM-PTRFZ24**  
6 paused tag(s). Why it matters: Dead tags slow audits and risk being re-enabled by mistake.  
_Recommendation:_ Delete paused tags no longer needed.

**[GTM · Governance] Needs attention: Limited Custom HTML — GTM-PTRFZ24**  
19 active Custom HTML tag(s) (44% of active tags). Why it matters: Custom HTML runs unrestricted JS: security, performance and consent risk.  
_Recommendation:_ Replace with templates where one exists.

**[GTM · Governance] Needs attention: No unused variables — GTM-PTRFZ24**  
81 variable(s) not referenced by any tag, trigger or variable: Custom JavaScript #94, __cvt_32699077_188 #95, DLV - ecommerce.detail.products.0.brand, DLV - ecommerce.detail.products.0.compare_at_price, DLV - ecommerce.purchase.actionField.tax, __cvt_32699077_188 #99, DLV - ecommerce.detail.products.0.image, DLV - marketing.utm_campaign Why it matters: Clutter hides what actually drives data.  
_Recommendation:_ Remove unused variables.

**[GTM · Governance] Needs attention: Custom JavaScript variables kept lean — GTM-PTRFZ24**  
47 Custom JavaScript variable(s). Why it matters: Each runs on every evaluation; heavy use slows the page and is brittle.  
_Recommendation:_ Push values into the dataLayer instead of computing them in GTM.

**[Tracking · GA4] Needs attention: GA4 — Product view event carries items, value, currency**  
view_item sent (1×); missing: value. Why it matters: Without product IDs and value the platform can't run catalogue ads or optimise for revenue.  
_Recommendation:_ Add value to view_item.

**[Tracking · GA4] Needs attention: GA4 — Add to cart event carries items, value, currency**  
add_to_cart sent (1×); missing: value. Why it matters: Without product IDs and value the platform can't run catalogue ads or optimise for revenue.  
_Recommendation:_ Add value to add_to_cart.

**[Tracking · GA4] Needs attention: GA4 — Consent Mode signals on hits**  
No gcs parameter on any GA4 hit. Why it matters: Needed for EU/UK traffic and for Google's conversion modelling.  
_Recommendation:_ Implement Consent Mode v2 (default + update).

**[Tracking · Stack] Needs attention: Stack — Third-party request volume**  
1148 third-party requests across the visit (20 identified platforms). Why it matters: Tag weight slows pages, which costs conversion rate.  
_Recommendation:_ Audit apps/pixels that don't earn their weight.

<details><summary>Failed requests</summary>

| Vendor | Phase | Status / error | URL |
|---|---|---|---|
| Postscript | initial | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=12982 |
| Postscript | reload | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=12982 |
| Postscript | pdp | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=12982 |
| Postscript | atc | net::ERR_BLOCKED_BY_ORB (likely capture network) | https://sdk.postscript.io/sdk.bundle.js?shopId=12982 |

</details>

---

## 14. Method & Files

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
