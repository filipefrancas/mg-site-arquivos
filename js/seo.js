/* MG Peças – SEO no navegador (dados estruturados e títulos)
   Carregado no fim de todas as páginas pelo "Código do selo" do Rodapé.
   1. Produto: JSON-LD Product (nome completo, código MG, OEM, aplicação, foto, marca; nota das avaliações do ML se AVAL).
      Sem offers/preço: a MG não vende pelo site.
   2. Listas (home, categorias, busca): tira os Product que o tema gera com preço "0".
   3. Produto: o H1 volta a ter código + nome + carro (o GTM "MG site - produto e lista" separa em selo / título / subtítulo;
      aqui o selo e o subtítulo entram dentro do H1, com a mesma aparência).
   4. Catálogo e Avaliações: o título do bloco vira H2 (fica 1 H1 por página, o do tema). */
(function () {
  if (window.__mgSeo) return;
  window.__mgSeo = 1;
  /* VER = commit dos dados de avaliações (o mesmo do avaliacoes.js) */
  var VER = 'c1a7ec4622eccc27737edb123c312625d5d34733';
  var DADOS_PROD = 'https://cdn.jsdelivr.net/gh/filipefrancas/mg-site-arquivos@' + VER + '/dados/avaliacoes_produtos.json';
  /* AVAL = põe a nota das avaliações (Mercado Livre) no JSON-LD do produto. Ver LEIA-ME antes de ligar. */
  var AVAL = false; /* Filipe 27/10: sem estrelas do ML para o Google (no site as avaliações continuam) */
  var MARCA = { '@type': 'Brand', name: 'MG Peças Automotivas' };
  var COD = /\bMG-?[A-Z]?\d+[A-Z]?\b/i;

  function meta(p) { var e = document.querySelector('meta[property="' + p + '"],meta[name="' + p + '"]'); return e ? e.content : ''; }
  function txt(e) { return (e && e.textContent || '').replace(/\s+/g, ' ').trim(); }
  function ld(o, id) {
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    if (id) s.id = id;
    s.textContent = JSON.stringify(o);
    document.head.appendChild(s);
  }
  function lds() {
    return [].map.call(document.querySelectorAll('script[type="application/ld+json"]'), function (s) {
      try { return { el: s, j: JSON.parse(s.textContent) }; } catch (e) { return { el: s, j: null }; }
    });
  }

  /* ---------- 2. listas: Product com preço 0 ---------- */
  function limpaListas() {
    lds().forEach(function (x) {
      var j = x.j;
      if (j && j['@type'] === 'Product' && j.offers && String(j.offers.price) === '0') x.el.remove();
    });
  }

  /* ---------- 1. produto: JSON-LD ---------- */
  function produtoLd(nota) {
    var nome = meta('og:title') || txt(document.querySelector('.js-product-name'));
    var c = (nome.match(/\s[-–]\s(MG[A-Z0-9-]+)\s*$/i) || nome.match(COD) || [])[1] || (nome.match(COD) || [''])[0];
    c = c.toUpperCase();
    var url = (document.querySelector('link[rel="canonical"]') || {}).href || location.href.split('?')[0];
    var desc = document.querySelector('.js-product-description');
    var oem = '';
    var carros = [];
    if (desc) {
      [].forEach.call(desc.querySelectorAll('p'), function (p) {
        var t = txt(p);
        if (!oem && /OEM|originais?/i.test(t) && t.indexOf(':') > 0) oem = t.slice(t.indexOf(':') + 1).trim();
      });
      [].forEach.call(desc.querySelectorAll('tbody tr'), function (tr) {
        var td = [].map.call(tr.querySelectorAll('td'), txt).filter(Boolean);
        if (td.length) carros.push({ '@type': 'Car', name: td.join(' ') });
      });
    }
    var imgs = [];
    var og = meta('og:image:secure_url') || meta('og:image').replace(/^http:/, 'https:');
    if (og) imgs.push(og.replace(/-\d+-0\.webp$/, '-1024-1024.webp'));
    var cats = [];
    lds().forEach(function (x) {
      var b = x.j && x.j.breadcrumb;
      if (b && b.itemListElement) b.itemListElement.forEach(function (i, k, L) { if (i.position > 1 && k < L.length - 1) cats.push(i.name); });
    });
    var p = {
      '@context': 'https://schema.org',
      '@type': 'Product',
      '@id': url + '#produto',
      name: nome,
      url: url,
      sku: c,
      mpn: c,
      brand: MARCA,
      manufacturer: { '@type': 'Organization', name: 'MG Peças Automotivas', url: 'https://mgpecasautomotivas.com.br/' },
      description: meta('description') || meta('og:description'),
      image: imgs
    };
    if (cats.length) p.category = cats.join(' > ');
    if (oem) p.additionalProperty = [{ '@type': 'PropertyValue', name: 'Código original (OEM)', value: oem }];
    if (carros.length) p.isAccessoryOrSparePartFor = carros;
    if (nota && nota.n > 0 && nota.media) {
      p.aggregateRating = { '@type': 'AggregateRating', ratingValue: Math.round(nota.media * 10) / 10, bestRating: 5, worstRating: 1, reviewCount: nota.n };
      var rev = (nota.itens || []).filter(function (a) { return a.autor && a.texto; }).slice(0, 5).map(function (a) {
        return { '@type': 'Review', author: { '@type': 'Person', name: a.autor }, reviewBody: a.texto,
          reviewRating: { '@type': 'Rating', ratingValue: a.estrelas || 5, bestRating: 5, worstRating: 1 } };
      });
      if (rev.length) p.review = rev;
    }
    var velho = document.getElementById('mg-ld-produto');
    if (velho) velho.remove();
    ld(p, 'mg-ld-produto');
    return c;
  }

  function produto() {
    var c = produtoLd(null);
    if (!AVAL || !c || !window.fetch) return;
    fetch(DADOS_PROD).then(function (r) { return r.ok ? r.json() : {}; }).then(function (P) {
      var nota = P && P[c];
      if (nota) produtoLd(nota);
    }).catch(function () {});
  }

  /* ---------- 3. produto: H1 completo ---------- */
  function h1Produto() {
    var h = document.querySelector('h1.js-product-name[data-mg]');
    if (!h || h.dataset.mgSeo) return !!h;
    h.dataset.mgSeo = '1';
    var b = h.previousElementSibling, s = h.nextElementSibling;
    if (!(b && b.classList.contains('mg-badge'))) b = null;
    if (!(s && s.classList.contains('mg-sub'))) s = null;
    var antes = [b, s].map(estilo);
    var depoisDeS = s ? s.nextElementSibling : null;
    var gapSub = s ? top(s) - fundo(h) : 0, gapFim = s && depoisDeS ? top(depoisDeS) - fundo(s) : 0;
    var titulo = document.createElement('span');
    titulo.className = 'mg-h1-tit';
    while (h.firstChild) titulo.appendChild(h.firstChild);
    if (b) { h.appendChild(b); h.appendChild(document.createTextNode(' ')); }
    h.appendChild(titulo);
    if (s) { h.appendChild(document.createTextNode(' ')); h.appendChild(s); }
    /* o que o selo e o subtítulo herdavam do lugar antigo continua igual (dentro do H1 herdariam a fonte do título) */
    [b, s].forEach(function (e, i) {
      if (!e) return;
      var d = estilo(e);
      HERDA.forEach(function (k) { if (d[k] !== antes[i][k]) e.style.setProperty(k, antes[i][k]); });
    });
    /* espaçamento: as margens do subtítulo agora ficam dentro do H1; repõe as distâncias medidas antes */
    if (s) {
      s.style.marginTop = (parseFloat(getComputedStyle(s).marginTop) + gapSub - (top(s) - fundo(titulo))) + 'px';
      s.style.marginBottom = '0px';
      if (depoisDeS) {
        h.style.marginBottom = gapFim + 'px';
        var dif = gapFim - (top(depoisDeS) - fundo(s));
        if (Math.abs(dif) > 0.5) h.style.marginBottom = (gapFim + dif) + 'px';
      }
    }
    return true;
  }
  function top(e) { return e.getBoundingClientRect().top; }
  function fundo(e) { return e.getBoundingClientRect().bottom; }
  var HERDA = ['font-family', 'font-weight', 'font-size', 'font-style', 'line-height', 'letter-spacing', 'word-spacing', 'text-transform', 'color', 'text-align', 'white-space'];
  function estilo(e) {
    var o = {};
    if (!e) return o;
    var cs = getComputedStyle(e);
    HERDA.forEach(function (k) { o[k] = cs.getPropertyValue(k); });
    return o;
  }

  /* ---------- 4. 2º H1 vira H2 ---------- */
  function rebaixa(sel) {
    [].forEach.call(document.querySelectorAll(sel), function (h) {
      var n = document.createElement('h2');
      for (var i = 0; i < h.attributes.length; i++) n.setAttribute(h.attributes[i].name, h.attributes[i].value);
      n.classList.add('mg-h1');
      while (h.firstChild) n.appendChild(h.firstChild);
      h.parentNode.replaceChild(n, h);
    });
  }

  function css() {
    var s = document.createElement('style');
    s.id = 'mg-seo-css';
    s.textContent = [
      /* selo e subtítulo dentro do H1 do produto: mesma aparência de quando ficavam fora */
      'h1.js-product-name .mg-badge{display:table}',
      'h1.js-product-name .mg-h1-tit,h1.js-product-name .mg-sub{display:block}',
      /* títulos de bloco que eram H1 */
      'h2.mg-h1{font-family:"Barlow Condensed","Sora",sans-serif!important;font-weight:800!important}',
      '.mgcat h2.mg-h1{font-size:44px}',
      '@media (max-width:900px){.mgcat h2.mg-h1{font-size:36px}}',
      '@media (max-width:480px){.mgcat h2.mg-h1{font-size:30px}}',
      '.mgav-hero h2.mg-h1{font-size:52px;line-height:1;color:#fff;text-transform:uppercase}',
      '@media (max-width:991px){.mgav-hero h2.mg-h1{font-size:42px}}',
      '@media (max-width:640px){.mgav-hero h2.mg-h1{font-size:34px}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  function vigia(fn, ms) {
    if (fn()) return;
    var mo = new MutationObserver(function () { if (fn()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
    setTimeout(function () { mo.disconnect(); }, ms || 15000);
  }

  function inicia() {
    css();
    var ehProduto = !!document.querySelector('.js-product-name') && /^\/produtos\/[^/]+\/?$/.test(location.pathname);
    if (ehProduto) {
      produto();
      vigia(h1Produto);
    } else {
      limpaListas();
    }
    var p = location.pathname;
    if (/^\/catalogo\/?$/.test(p)) vigia(function () { rebaixa('.mgcat h1'); return false; }, 8000);
    if (/^\/avaliacoes\/?$/.test(p)) vigia(function () { var h = document.querySelector('.mgav-hero h1'); if (h) rebaixa('.mgav-hero h1'); return !!h; });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inicia); else inicia();
})();
