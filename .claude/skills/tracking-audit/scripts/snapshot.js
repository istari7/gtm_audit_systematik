() => {
  const safe = (v, depth) => {
    if (depth > 6) return '[depth]';
    if (v === null || ['string','number','boolean'].includes(typeof v)) return typeof v === 'string' ? v.slice(0, 500) : v;
    if (typeof v === 'function' || (typeof Node !== 'undefined' && v instanceof Node)) return undefined;
    if (Array.isArray(v) || (v && typeof v.length === 'number' && typeof v !== 'string' && Object.prototype.toString.call(v) === '[object Arguments]')) {
      return Array.from(v).slice(0, 50).map(x => safe(x, depth + 1));
    }
    if (typeof v === 'object') {
      const o = {};
      for (const k of Object.keys(v).slice(0, 80)) { const s = safe(v[k], depth + 1); if (s !== undefined) o[k] = s; }
      return o;
    }
    return undefined;
  };
  const gtm = window.google_tag_manager ? Object.keys(window.google_tag_manager).filter(k => /^(GTM|G|AW|DC|GT)-/.test(k)) : [];
  const dl = Array.isArray(window.dataLayer) ? window.dataLayer.slice(0, 300).map(e => safe(e, 0)) : null;
  const meta = n => { const m = document.querySelector(`meta[property="${n}"],meta[name="${n}"]`); return m ? m.content : null; };
  const S = window.Shopify;
  let shopifyConsent = null;
  try { shopifyConsent = S && S.customerPrivacy && S.customerPrivacy.currentVisitorConsent ? S.customerPrivacy.currentVisitorConsent() : null; } catch (e) {}
  let gcsDefault = null;
  try {
    const gtd = window.google_tag_data && window.google_tag_data.ics && window.google_tag_data.ics.entries;
    if (gtd) { gcsDefault = {}; for (const k of Object.keys(gtd)) gcsDefault[k] = { default: gtd[k].default, update: gtd[k].update }; }
  } catch (e) {}
  return {
    url: location.href,
    title: document.title,
    site_name: meta('og:site_name'),
    description: meta('description') || meta('og:description'),
    google_tag_manager_keys: gtm,
    data_layer: dl,
    consent_state: gcsDefault,
    shopify: S ? {
      shop: S.shop || null,
      theme: S.theme ? { name: S.theme.name || null, id: S.theme.id || null, schema_name: S.theme.schema_name || null } : null,
      currency: S.currency ? S.currency.active : null,
      country: S.country || null,
      customer_privacy_api: !!(S.customerPrivacy),
      visitor_consent: shopifyConsent,
    } : null,
    shopify_analytics_meta: window.ShopifyAnalytics && window.ShopifyAnalytics.meta ? safe(window.ShopifyAnalytics.meta, 0) : null,
    globals: ['fbq','ttq','pintrk','snaptr','rdt','twq','uetq','_learnq','klaviyo','gtag','ga','analytics','amplitude','mixpanel','heap','hj','clarity','TriplePixel','OneTrust','Cookiebot','Osano','Didomi','UC_UI','Shopify','dataLayer','utag','_satellite','optimizely','attentive','Rebuy','yotpo']
      .filter(k => typeof window[k] !== 'undefined'),
  };
}
