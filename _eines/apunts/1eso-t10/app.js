(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u10-done", NSEC = 9;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc",
      bad: "No entenc la fórmula. Escriu-la amb la x, per exemple: x^2-3x+1, 2x+5, 12/x o sqrt(x+4).",
      badx: "Escriu un valor de x (un nombre).", num: "Escriu un nombre (pots fer servir coma decimal o una fracció com 5/2).",
      pair: "Escriu el punt com (2, −3) o bé 2; −3.", sol: "Solució:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro",
      bad: "No entiendo la fórmula. Escríbela con la x, por ejemplo: x^2-3x+1, 2x+5, 12/x o sqrt(x+4).",
      badx: "Escribe un valor de x (un número).", num: "Escribe un número (puedes usar coma decimal o una fracción como 5/2).",
      pair: "Escribe el punto como (2, −3) o bien 2; −3.", sol: "Solución:" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode",
      bad: "I can't read the formula. Write it in x, for example: x^2-3x+1, 2x+5, 12/x or sqrt(x+4).",
      badx: "Type a value of x (a number).", num: "Type a number (decimals or a fraction like 5/2 are fine).",
      pair: "Type the point as (2, −3) or 2; −3.", sol: "Solution:" }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function T(o) { return o[lang] || o.va; }
  function L3(va, es, en) { return { va: va, es: es, en: en }; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return k in o ? o[k] : m; }); }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var MACROS = { "\\dc": "\\htmlClass{dc}{{,}}", "\\tri": "\\htmlClass{lva}{\\text{#1}}\\htmlClass{les}{\\text{#2}}\\htmlClass{len}{\\text{#3}}" };
  var KOPT = { throwOnError: false, strict: "ignore", macros: MACROS, trust: function (c) { return c.command === "\\htmlClass"; } };
  function tex(s, display) {
    try { return window.katex.renderToString(display ? s : "\\displaystyle " + s, { throwOnError: false, strict: "ignore", displayMode: !!display, macros: MACROS, trust: KOPT.trust }); } catch (e) { return s; }
  }
  function rtex(s) { return s.replace(/\$([^$]+)\$/g, function (_, m) { return tex(m); }); }
  function segBind(w, cb) {
    var bs = w.querySelectorAll(".seg button");
    bs.forEach(function (b) { b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); cb(b.dataset.k); }); });
  }
  function warn(s) { return '<span class="warn">' + s + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function rnz(a, b) { var k; do { k = rint(a, b); } while (k === 0); return k; }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = rint(0, i), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function inputs(w) { var o = {}; w.querySelectorAll(".tin[data-k]").forEach(function (i) { o[i.dataset.k] = i; }); return o; }
  function quickBind(w, cb) { w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { cb(b.dataset.b.split("|"), b); }); }); }
  function rows2html(rows) { return rows.map(function (x) { return '<div class="hrow">' + x + "</div>"; }).join(""); }

  /* ---------- nombres ---------- */
  var INF = Infinity;
  function near(a, b) { return Math.abs(a - b) < 1e-9; }
  /* nombre en TeX amb coma decimal (com a molt 3 decimals) */
  function nf(v) {
    if (v === INF) return "+\\infty"; if (v === -INF) return "-\\infty";
    var r = Math.round(v * 1000) / 1000; if (near(r, 0)) r = 0;
    return String(r).replace(".", "\\dc ");
  }
  function nfp(v) { return v < 0 ? "(" + nf(v) + ")" : nf(v); }
  /* nombre escrit per l'alumne: "−3", "2,5", "5/2" */
  function numIn(raw) {
    var s = String(raw).replace(/[−–]/g, "-").replace(/\s+/g, "").replace(",", ".");
    var m = s.match(/^(-?\d+(?:\.\d+)?)(?:\/(\d+(?:\.\d+)?))?$/);
    if (!m) return null;
    var v = parseFloat(m[1]); if (m[2]) { if (+m[2] === 0) return null; v /= parseFloat(m[2]); }
    return v;
  }
  function pairIn(raw) {
    var s = String(raw).replace(/[−–]/g, "-").replace(/[()\s]/g, "");
    var parts = s.indexOf(";") >= 0 ? s.split(";") : s.split(/,(?!\d)/);
    if (parts.length !== 2) { var m = s.match(/^(-?\d+),(-?\d+)$/); if (m) parts = [m[1], m[2]]; else return null; }
    var a = numIn(parts[0]), b = numIn(parts[1]);
    return a === null || b === null ? null : [a, b];
  }


  function isInt(v) { return Math.abs(v - Math.round(v)) < 1e-9; }
  function d2(v) { return (Math.round(v * 100) / 100).toFixed(2).replace(".", "\\dc "); }
  function lab(v) { var s = String(Math.round(v * 100) / 100); return lang === "en" ? s : s.replace(".", ","); }

  /* ---------- lectura dels controls ---------- */
  function sliders(w) { var o = {}; w.querySelectorAll('input[type="range"]').forEach(function (i) { o[i.dataset.k] = i; }); return o; }
  function showRv(w, k, name, v, unit) { var e = w.querySelector("." + k + "v"); if (e) e.innerHTML = tex(name + "=" + nf(v) + (unit || "")); }
  function gcol(rows) { return '<div class="gcol">' + rows.map(function (r) { return "<p>" + r + "</p>"; }).join("") + "</div>"; }
  /* cada grup .seg del giny té el seu valor: segs(w, [cb0, cb1]) */
  function segs(w, cbs) {
    var val = [];
    w.querySelectorAll(".seg").forEach(function (g, i) {
      var bs = g.querySelectorAll("button");
      bs.forEach(function (b) {
        if (b.getAttribute("aria-pressed") === "true") val[i] = b.dataset.k;
        b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); val[i] = b.dataset.k; if (cbs[i]) cbs[i](b.dataset.k); });
      });
    });
    return val;
  }
  function setSeg(w, i, k) { var g = w.querySelectorAll(".seg")[i]; if (g) g.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.k === k)); }); }
  function intIn(raw) { var v = numIn(raw); return v === null || v < 0 || !isInt(v) ? null : Math.round(v); }


  /* ======================================================================
     unitat 10 (1r ESO): estadística
     ====================================================================== */
  /* ---------- nombres ---------- */
  function tk(v) { var r = Math.round(v * 100) / 100; return String(r).replace("-", "−").replace(".", lang === "en" ? "." : ","); }
  /* nombre en TeX arrodonit a 2 decimals: «= 1,45» si és exacte, «≈ 1,33» si no */
  function eqr(v) { var r = Math.round(v * 100) / 100; return (near(r, v) ? "=" : "\\approx ") + nf(r); }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function numsIn(raw) {
    var parts = String(raw).replace(/[−–]/g, "-").trim().split(/[\s;]+/).filter(function (s) { return s.length; });
    var out = parts.map(numIn); return out.some(function (v) { return v === null; }) ? null : out;
  }
  /* llista de dades: nombres o paraules separats per espais (o per comes, si són paraules) */
  function tokensIn(raw) {
    var out = [];
    String(raw).replace(/[−–]/g, "-").trim().split(/[\s;]+/).forEach(function (t) {
      if (!t) return;
      if (numIn(t) !== null) out.push(t); else t.split(",").forEach(function (w) { if (w) out.push(w); });
    });
    return out;
  }
  function dataIn(raw) {
    var t = tokensIn(raw); if (!t.length) return null;
    var nums = t.map(numIn), isNum = nums.every(function (v) { return v !== null; });
    return { num: isNum, vals: isNum ? nums : t.map(function (w) { return w.toLowerCase(); }) };
  }
  /* [{v, f}] ordenat (els nombres de menor a major; les paraules, per ordre d'aparició) */
  function countOf(d) {
    var m = {}, keys = [];
    d.vals.forEach(function (v) { var k = String(v); if (!(k in m)) { m[k] = { v: v, f: 0 }; keys.push(k); } m[k].f++; });
    var out = keys.map(function (k) { return m[k]; });
    if (d.num) out.sort(function (a, b) { return a.v - b.v; });
    return out;
  }
  function sum(a) { return a.reduce(function (s, x) { return s + x; }, 0); }
  function meanOf(a) { return sum(a) / a.length; }
  function sorted(a) { return a.slice().sort(function (x, y) { return x - y; }); }
  function medianOf(a) { var s = sorted(a), n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; }
  function modesOf(a) { var c = countOf({ num: true, vals: a }), m = Math.max.apply(null, c.map(function (o) { return o.f; })); return c.filter(function (o) { return o.f === m; }).map(function (o) { return o.v; }); }
  function rangeOf(a) { return Math.max.apply(null, a) - Math.min.apply(null, a); }
  function dmOf(a) { var m = meanOf(a); return sum(a.map(function (x) { return Math.abs(x - m); })) / a.length; }
  function expand(X, F) { var out = []; X.forEach(function (x, i) { for (var k = 0; k < F[i]; k++) out.push(x); }); return out; }
  function listTex(a) { return a.map(function (x) { return nf(x); }).join(",\\ "); }
  function tbl(head, rows, cls) {
    return '<div class="tbl-wrap"><table class="data c ' + (cls || "") + '"><thead><tr>' + head.map(function (h) { return "<th>" + h + "</th>"; }).join("") + "</tr></thead><tbody>"
      + rows.map(function (r) { return "<tr>" + r.map(function (c) { return "<td>" + c + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table></div>";
  }
  var TOTAL = L3("Total", "Total", "Total");

  /* ---------- gràfics estadístics (SVG); comu.py en té còpies ---------- */
  function nice(top) { var c = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000]; for (var i = 0; i < c.length; i++) if (top / c[i] <= 8) return c[i]; return 2000; }
  function tally(n) {
    var out = "", x = 2;
    for (var g = 0; g < n; g += 5) {
      var k = Math.min(5, n - g), x0 = x;
      for (var j = 0; j < Math.min(k, 4); j++) { out += '<line x1="' + x + '" y1="3" x2="' + x + '" y2="17"/>'; x += 5; }
      if (k === 5) out += '<line x1="' + (x0 - 3) + '" y1="14" x2="' + (x0 + 18) + '" y2="6"/>';
      x += 7;
    }
    x = Math.max(x, 10);
    return '<svg class="tally" viewBox="0 0 ' + x + ' 20" width="' + x + '" height="20" aria-label="' + n + '">' + out + "</svg>";
  }
  function axesY(L0, R0, T0, h, W, top, st, y0, Y) {
    var g = "";
    for (var k = y0; k <= top + 1e-9; k += st) g += '<line class="grid" x1="' + L0 + '" y1="' + Y(k).toFixed(1) + '" x2="' + (W - R0) + '" y2="' + Y(k).toFixed(1) + '"/><text class="tk" x="' + (L0 - 5) + '" y="' + (Y(k) + 4).toFixed(1) + '" text-anchor="end">' + tk(k) + "</text>";
    return g + '<line class="ax" x1="' + L0 + '" y1="' + (T0 + h) + '" x2="' + (W - R0) + '" y2="' + (T0 + h) + '"/><line class="ax" x1="' + L0 + '" y1="' + (T0 - 6) + '" x2="' + L0 + '" y2="' + (T0 + h) + '"/>';
  }
  function axT(o, W, R0, H, L0, T0) {
    return (o.yl ? '<text class="tk ax-t" x="' + (L0 + 4) + '" y="' + (T0 - 6) + '">' + o.yl + "</text>" : "") + (o.xl ? '<text class="tk ax-t" x="' + (W - R0) + '" y="' + (H - 2) + '" text-anchor="end">' + o.xl + "</text>" : "");
  }
  /* o: { cats, vals, kind: bar|poly|both, yl, xl, hl, W, H } */
  function barres(o) {
    var W = o.W || 300, H = o.H || 190, n = o.cats.length, top = Math.max.apply(null, o.vals.concat([1])), st = nice(top);
    top = Math.ceil(top / st) * st;
    var L0 = 34, R0 = 10, T0 = 16, B0 = 30, w = W - L0 - R0, h = H - T0 - B0, kind = o.kind || "bar";
    function X(i) { return L0 + w * (i + 0.5) / n; }
    function Y(v) { return T0 + h - h * v / top; }
    var g = axesY(L0, R0, T0, h, W, top, st, 0, Y), bw = Math.min(34, w / n * 0.6);
    o.cats.forEach(function (c, i) {
      var v = o.vals[i];
      if (kind !== "poly") g += '<rect class="bar b' + (o.multi ? i % 4 : 0) + (o.hl === i ? " hl" : "") + '" x="' + (X(i) - bw / 2).toFixed(1) + '" y="' + Y(v).toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + (T0 + h - Y(v)).toFixed(1) + '"/>';
      g += '<text class="tk xl" x="' + X(i).toFixed(1) + '" y="' + (T0 + h + 14) + '" text-anchor="middle">' + esc(c) + "</text>";
    });
    if (kind !== "bar") {
      g += '<polyline class="fpoly" points="' + o.vals.map(function (v, i) { return X(i).toFixed(1) + "," + Y(v).toFixed(1); }).join(" ") + '"/>';
      o.vals.forEach(function (v, i) { g += '<circle class="fdot" cx="' + X(i).toFixed(1) + '" cy="' + Y(v).toFixed(1) + '" r="4"/>'; });
    }
    return '<svg class="sgraf stat" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="diagrama">' + g + axT(o, W, R0, H, L0, T0) + "</svg>";
  }
  /* o: { edges, vals, poly, yl, xl } */
  function hist(o) {
    var E = o.edges, a = E[0], b = E[E.length - 1], W = o.W || 300, H = o.H || 190, top = Math.max.apply(null, o.vals.concat([1])), st = nice(top);
    top = Math.ceil(top / st) * st;
    var L0 = 34, R0 = 14, T0 = 16, B0 = 30, w = W - L0 - R0 - 16, h = H - T0 - B0;
    function X(x) { return L0 + 8 + w * (x - a) / (b - a); }
    function Y(v) { return T0 + h - h * v / top; }
    var g = axesY(L0, R0, T0, h, W, top, st, 0, Y), every = Math.ceil(E.length / 9);
    o.vals.forEach(function (v, i) { g += '<rect class="bar hist b' + (i % 4) + '" x="' + X(E[i]).toFixed(1) + '" y="' + Y(v).toFixed(1) + '" width="' + (X(E[i + 1]) - X(E[i])).toFixed(1) + '" height="' + (T0 + h - Y(v)).toFixed(1) + '"/>'; });
    E.forEach(function (e, i) { if (i % every === 0) g += '<text class="tk xl" x="' + X(e).toFixed(1) + '" y="' + (T0 + h + 14) + '" text-anchor="middle">' + tk(e) + "</text>"; });
    if (o.poly) {
      var d = E[1] - E[0], P = [[a - d / 2, 0]].concat(o.vals.map(function (v, i) { return [(E[i] + E[i + 1]) / 2, v]; })).concat([[b + d / 2, 0]]);
      var lim = 8 * (b - a) / w;
      P = P.map(function (p) { return [Math.max(Math.min(p[0], b + lim), a - lim), p[1]]; });
      g += '<polyline class="fpoly" points="' + P.map(function (p) { return X(p[0]).toFixed(1) + "," + Y(p[1]).toFixed(1); }).join(" ") + '"/>';
      P.slice(1, -1).forEach(function (p) { g += '<circle class="fdot" cx="' + X(p[0]).toFixed(1) + '" cy="' + Y(p[1]).toFixed(1) + '" r="3.5"/>'; });
    }
    return '<svg class="sgraf stat" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="histograma">' + g + axT(o, W, R0, H, L0, T0) + "</svg>";
  }
  /* o: { cats, vals, angles } */
  function sectors(o) {
    var R = o.R || 78, W = o.W || 300, N = sum(o.vals), cx = R + 8, cy = R + 8, g = "", a0 = -90;
    o.vals.forEach(function (v, i) {
      var a1 = a0 + 360 * v / N, r0 = a0 * Math.PI / 180, r1 = a1 * Math.PI / 180;
      if (v === N) g += '<circle class="sec s' + (i % 6) + '" cx="' + cx + '" cy="' + cy + '" r="' + R + '"/>';
      else if (v) g += '<path class="sec s' + (i % 6) + '" d="M' + cx + " " + cy + "L" + (cx + R * Math.cos(r0)).toFixed(1) + " " + (cy + R * Math.sin(r0)).toFixed(1) + "A" + R + " " + R + " 0 " + (a1 - a0 > 180 ? 1 : 0) + " 1 " + (cx + R * Math.cos(r1)).toFixed(1) + " " + (cy + R * Math.sin(r1)).toFixed(1) + 'Z"/>';
      if (o.angles && v && a1 - a0 >= 18) {
        var am = (a0 + a1) / 2 * Math.PI / 180;
        g += '<text class="slab" x="' + (cx + R * 0.64 * Math.cos(am)).toFixed(1) + '" y="' + (cy + R * 0.64 * Math.sin(am) + 4).toFixed(1) + '" text-anchor="middle">' + tk(360 * v / N) + "°</text>";
      }
      a0 = a1;
    });
    var lx = 2 * R + 28, ly = Math.max(cy - 11 * o.cats.length, 6);
    o.cats.forEach(function (c, i) { g += '<rect class="sec s' + (i % 6) + '" x="' + lx + '" y="' + (ly + 22 * i) + '" width="13" height="13" rx="3"/><text class="lg" x="' + (lx + 19) + '" y="' + (ly + 22 * i + 11) + '">' + esc(c) + "</text>"; });
    return '<svg class="sgraf stat pie" viewBox="0 0 ' + W + " " + Math.max(2 * R + 16, ly + 22 * o.cats.length) + '" role="img" aria-label="diagrama de sectors">' + g + "</svg>";
  }
  /* o: { cats, vals, unit, icon } */
  function picto(o) {
    var rh = 30, g = "", maxk = 0;
    o.cats.forEach(function (c, i) {
      var y = 8 + rh * i, q = o.vals[i] / o.unit, k = 0;
      g += '<text class="lg" x="4" y="' + (y + 18) + '">' + esc(c) + "</text>";
      while (q > 1e-9) {
        var part = Math.min(q, 1), x = 92 + 26 * k;
        if (part > 0.999) g += '<text class="pic" x="' + x + '" y="' + (y + 20) + '">' + o.icon + "</text>";
        else g += '<svg x="' + x + '" y="' + y + '" width="' + (part * 22).toFixed(1) + '" height="28" overflow="hidden"><text class="pic" x="0" y="20">' + o.icon + "</text></svg>";
        q -= part; k++;
      }
      maxk = Math.max(maxk, k);
    });
    var W = Math.max(300, 100 + 26 * maxk);
    return '<svg class="sgraf stat picto" viewBox="0 0 ' + W + " " + (rh * o.cats.length + 12) + '" role="img" aria-label="pictograma">' + g + "</svg>";
  }
  /* o: { data, lo, hi, step, mean, med, dev } diagrama de punts */
  function dots(o) {
    var W = o.W || 300, L0 = 16, R0 = 16, w = W - L0 - R0, lo = o.lo, hi = o.hi, cnt = {}, pts = [];
    function X(v) { return L0 + w * (v - lo) / (hi - lo); }
    o.data.forEach(function (d) { cnt[d] = (cnt[d] || 0) + 1; pts.push([d, cnt[d]]); });
    var top = 0; for (var k in cnt) top = Math.max(top, cnt[k]);
    var H = 46 + 15 * top + (o.dev ? 12 * o.data.length : 0), base = H - 32;
    var g = '<line class="ax" x1="' + (L0 - 6) + '" y1="' + base + '" x2="' + (W - R0 + 6) + '" y2="' + base + '"/>';
    var st = o.step || nice(hi - lo) / 2 || 1, every = Math.ceil((hi - lo) / st / 12);
    for (var i = 0, v = lo; v <= hi + 1e-9; v += st, i++) {
      g += '<line class="ax" x1="' + X(v).toFixed(1) + '" y1="' + (base - 3) + '" x2="' + X(v).toFixed(1) + '" y2="' + (base + 3) + '"/>';
      if (i % every === 0) g += '<text class="tk" x="' + X(v).toFixed(1) + '" y="' + (base + 15) + '" text-anchor="middle">' + tk(v) + "</text>";
    }
    pts.forEach(function (p) { g += '<circle class="ddot" cx="' + X(p[0]).toFixed(1) + '" cy="' + (base - 9 - 15 * (p[1] - 1)) + '" r="6"/>'; });
    if (o.dev && o.mean != null) {
      var y = base - 15 * top - 12;
      sorted(o.data).forEach(function (d, j) { var yy = y - 12 * j; g += '<line class="dev" x1="' + X(o.mean).toFixed(1) + '" y1="' + yy + '" x2="' + X(d).toFixed(1) + '" y2="' + yy + '"/><circle class="ddot sm" cx="' + X(d).toFixed(1) + '" cy="' + yy + '" r="3"/>'; });
    }
    if (o.med != null) g += '<line class="medl" x1="' + X(o.med).toFixed(1) + '" y1="8" x2="' + X(o.med).toFixed(1) + '" y2="' + base + '"/>';
    if (o.mean != null) g += '<path class="fulc" d="M' + X(o.mean).toFixed(1) + " " + (base + 2) + 'l-8 13h16z"/>';
    return '<svg class="sgraf stat dots" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="diagrama de punts">' + g + "</svg>";
  }
  function dotsAuto(data, extra) {
    var lo = Math.min.apply(null, data), hi = Math.max.apply(null, data), st = nice(Math.max(hi - lo, 1)) / 2;
    if (st < 1) st = 1;
    lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st) * st; if (hi === lo) { lo -= st; hi += st; }
    var o = { data: data, lo: lo, hi: hi, step: st }; for (var k in extra) o[k] = extra[k];
    return dots(o);
  }

  /* ---------- dades dels exemples ---------- */
  var GERM = [1, 2, 0, 1, 1, 3, 2, 1, 0, 2, 1, 1, 4, 0, 2, 1, 3, 1, 2, 1];
  var FRUW = { va: ["poma", "plàtan", "taronja", "maduixa", "pera"], es: ["manzana", "plátano", "naranja", "fresa", "pera"], en: ["apple", "banana", "orange", "strawberry", "pear"] };
  var FRUF = [8, 6, 5, 4, 2];
  var FRUO = [0, 1, 0, 2, 3, 0, 1, 4, 0, 2, 1, 3, 0, 1, 2, 0, 3, 1, 4, 0, 2, 1, 3, 0, 2];
  var NOTX = [4, 5, 6, 7, 8, 9, 10], NOTF = [2, 5, 6, 5, 4, 2, 1];
  var NOTL = [6, 7, 5, 8, 6, 4, 7, 9, 5, 6, 8, 7, 5, 6, 10, 7, 6, 8, 5, 9, 6, 4, 7, 8, 5];
  var ALT = [152, 147, 158, 150, 143, 161, 155, 149, 151, 146, 157, 153, 163, 150, 148, 154, 159, 141, 152, 156, 145, 151, 160, 149, 153, 144, 158, 147, 162, 150];
  var TRAW = { va: ["Caminant", "Autobús", "Cotxe", "Bici"], es: ["Andando", "Autobús", "Coche", "Bici"], en: ["Walking", "Bus", "Car", "Bike"] }, TRAF = [10, 6, 5, 3];
  function fruList() { return FRUO.map(function (i) { return FRUW[lang][i]; }).join(" "); }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  /* ---------- 10.2 el dau ---------- */
  function wDice() {
    var w = document.getElementById("w-dice"); if (!w) return;
    var out = w.querySelector(".gout"), info = w.querySelector(".info"), C = [0, 0, 0, 0, 0, 0], last = null;
    var FACE = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"];
    function paint() {
      var N = sum(C);
      var rows = C.map(function (f, i) { return [String(i + 1), tex(String(f)), N ? tex(nf(Math.round(f / N * 1000) / 1000)) : "—", N ? tex(nf(Math.round(f / N * 1000) / 10) + "\\ \\%") : "—"]; });
      rows.push(["<strong>" + T(TOTAL) + "</strong>", tex("N=" + N), N ? tex("1") : "—", N ? tex("100\\ \\%") : "—"]);
      out.innerHTML = '<div class="gcol">' + (last ? '<p class="die">' + last.map(function (k) { return FACE[k]; }).join(" ") + "</p>" : "")
        + tbl([T(L3("Cara", "Cara", "Face")), tex("f_i"), tex("h_i"), "%"], rows, "freq") + "</div>"
        + barres({ cats: ["1", "2", "3", "4", "5", "6"], vals: C, yl: T(L3("Freqüència", "Frecuencia", "Frequency")) });
      info.innerHTML = N >= 300 ? T(L3("Amb molts llançaments, totes les freqüències relatives s'acosten a ", "Con muchos lanzamientos, todas las frecuencias relativas se acercan a ", "With many rolls, all the relative frequencies get close to ")) + tex("\\frac16\\approx0\\dc 167") + "." : N ? "" : T(L3("Encara no has llançat el dau.", "Todavía no has lanzado el dado.", "You haven't rolled the die yet."));
    }
    w.querySelectorAll("[data-a]").forEach(function (b) {
      b.addEventListener("click", function () {
        var n = +b.dataset.a;
        if (!n) { C = [0, 0, 0, 0, 0, 0]; last = null; paint(); return; }
        last = [];
        for (var i = 0; i < n; i++) { var k = Math.floor(Math.random() * 6); C[k]++; if (i < 12) last.push(k); }
        paint();
      });
    });
    onLang(paint);
  }

  /* ---------- 10.3 laboratori de dades ---------- */
  function freqTable(d) {
    var c = countOf(d), N = d.vals.length, F = 0, rows = c.map(function (o) {
      F += o.f;
      var h = o.f / N, r = [d.num ? tex(nf(o.v)) : esc(cap(String(o.v))), tally(o.f), tex(String(o.f))];
      if (d.num) r.push(tex(String(F)));
      r.push(tex("\\frac{" + o.f + "}{" + N + "}" + eqr(h)), tex(nf(Math.round(h * 1000) / 10) + "\\ \\%"));
      return r;
    });
    var tot = ["<strong>" + T(TOTAL) + "</strong>", "", tex("N=" + N)]; if (d.num) tot.push(""); tot.push(tex("1"), tex("100\\ \\%"));
    rows.push(tot);
    var head = [tex("x_i"), T(L3("Recompte", "Recuento", "Tally")), tex("f_i")]; if (d.num) head.push(tex("F_i")); head.push(tex("h_i"), "%");
    return tbl(head, rows, "freq");
  }
  function wTally() {
    var w = document.getElementById("w-tally"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".tout"), info = w.querySelector(".info"), pre = "germ";
    function fill_() { I.d.value = pre === "germ" ? GERM.join(" ") : pre === "fru" ? fruList() : pre === "not" ? NOTL.join(" ") : I.d.value; }
    segs(w, [function (k) { pre = k; if (k === "own") { I.d.value = ""; I.d.focus(); } fill_(); paint(); }]);
    function paint() {
      var d = dataIn(I.d.value);
      if (!d) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu algunes dades separades per espais: 3 5 5 2 o roig blau roig.", "Escribe algunos datos separados por espacios: 3 5 5 2 o rojo azul rojo.", "Type some data separated by spaces: 3 5 5 2 or red blue red."))); return; }
      if (d.vals.length > 200) { info.innerHTML = warn(T(L3("Com a molt 200 dades.", "Como mucho 200 datos.", "At most 200 values."))); return; }
      var c = countOf(d);
      if (c.length > 15) { info.innerHTML = warn(T(L3("Hi ha massa valors diferents: agrupa'ls en intervals (com en l'exemple de les alçades).", "Hay demasiados valores diferentes: agrúpalos en intervalos (como en el ejemplo de las alturas).", "Too many different values: group them into intervals (like the heights example)."))); return; }
      info.innerHTML = "";
      out.innerHTML = '<p class="hint-s">' + fill(T(L3("Variable {t} · {n} dades · {k} valors diferents", "Variable {t} · {n} datos · {k} valores diferentes", "{t} variable · {n} values · {k} different values")),
        { t: T(d.num ? L3("quantitativa", "cuantitativa", "quantitative") : L3("qualitativa", "cualitativa", "qualitative")), n: d.vals.length, k: c.length }) + "</p>" + freqTable(d);
    }
    I.d.addEventListener("input", function () { if (pre !== "own") { pre = "own"; setSeg(w, 0, "own"); } paint(); });
    fill_();
    onLang(function () { if (pre === "fru") fill_(); paint(); });
  }

  /* ---------- valors i freqüències (10.4, 10.5, 10.7) ---------- */
  function tabIn(I, numOnly) {
    var X = tokensIn(I.x.value), F = numsIn(I.f.value);
    if (!X.length || !F || !F.length) return { err: T(L3("Escriu els valors i les freqüències separats per espais.", "Escribe los valores y las frecuencias separados por espacios.", "Type the values and the frequencies separated by spaces.")) };
    if (X.length !== F.length) return { err: T(L3("Hi ha d'haver tants valors com freqüències.", "Tiene que haber tantos valores como frecuencias.", "There must be as many values as frequencies.")) };
    if (F.some(function (f) { return f < 0 || !isInt(f); })) return { err: T(L3("Les freqüències absolutes són nombres naturals.", "Las frecuencias absolutas son números naturales.", "Absolute frequencies are whole numbers.")) };
    if (X.length > 12) return { err: T(L3("Com a molt 12 valors.", "Como mucho 12 valores.", "At most 12 values.")) };
    if (sum(F) === 0) return { err: T(L3("Alguna freqüència ha de ser més gran que 0.", "Alguna frecuencia tiene que ser mayor que 0.", "Some frequency must be greater than 0.")) };
    var nums = X.map(numIn), isNum = nums.every(function (v) { return v !== null; });
    if (numOnly && !isNum) return { err: T(L3("Per a calcular la mitjana, els valors han de ser nombres.", "Para calcular la media, los valores tienen que ser números.", "To work out the mean, the values must be numbers.")) };
    return { X: isNum ? nums : X, labels: X.map(function (x, i) { return isNum ? tk(nums[i]) : x; }), F: F, num: isNum };
  }
  function presetTab(w, I, P, cb) {
    var pre = Object.keys(P)[0];
    function put() { var p = P[pre]; if (!p) return; I.x.value = typeof p.x === "function" ? p.x() : p.x; I.f.value = p.f; }
    segs(w, [function (k) { pre = k; if (k === "own") { I.x.value = ""; I.f.value = ""; I.x.focus(); } put(); cb(); }].concat([].slice.call(arguments, 4)));
    [I.x, I.f].forEach(function (i) { i.addEventListener("input", function () { if (pre !== "own") { pre = "own"; setSeg(w, 0, "own"); } cb(); }); });
    put();
    return function () { if (P[pre] && typeof P[pre].x === "function") put(); };
  }
  var PRE_G = { germ: { x: "0 1 2 3 4", f: "3 9 5 2 1" }, fru: { x: function () { return FRUW[lang].map(cap).join(" "); }, f: FRUF.join(" ") } };
  function wChart() {
    var w = document.getElementById("w-chart"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), kind = "bar";
    var relang = presetTab(w, I, PRE_G, paint, function (k) { kind = k; paint(); });
    function paint() {
      var t = tabIn(I); if (t.err) { out.innerHTML = ""; info.innerHTML = warn(t.err); return; }
      info.innerHTML = !t.num && kind !== "bar" ? warn(T(L3("Compte: amb una variable qualitativa els valors no tenen ordre, i el polígon de freqüències no té gaire sentit.", "Cuidado: con una variable cualitativa los valores no tienen orden, y el polígono de frecuencias no tiene mucho sentido.", "Careful: with a qualitative variable the values have no order, so a frequency polygon doesn't make much sense."))) : "";
      out.innerHTML = barres({ cats: t.labels, vals: t.F, kind: kind, multi: !t.num, yl: T(L3("Freqüència", "Frecuencia", "Frequency")) })
        + gcol([fill(T(L3("Hi ha {n} dades. La barra més alta és la de {v}.", "Hay {n} datos. La barra más alta es la de {v}.", "There are {n} values. The tallest bar is {v}.")), { n: sum(t.F), v: "<b>" + esc(t.labels[t.F.indexOf(Math.max.apply(null, t.F))]) + "</b>" })]);
    }
    onLang(function () { relang(); paint(); });
  }
  function wHist() {
    var w = document.getElementById("w-hist"); if (!w) return;
    var out = w.querySelector(".gout"), info = w.querySelector(".info"), amp = 5, poly = false;
    segs(w, [function (k) { amp = +k; paint(); }, function (k) { poly = k === "1"; paint(); }]);
    function paint() {
      var a = Math.floor(Math.min.apply(null, ALT) / amp) * amp, b = Math.floor(Math.max.apply(null, ALT) / amp) * amp + amp, E = [], V = [];
      for (var x = a; x <= b + 1e-9; x += amp) E.push(x);
      for (var i = 0; i < E.length - 1; i++) V.push(ALT.filter(function (h) { return h >= E[i] && h < E[i + 1]; }).length);
      out.innerHTML = hist({ edges: E, vals: V, poly: poly, yl: T(L3("Nre. d'alumnes", "N.º de alumnos", "Students")), xl: "cm" })
        + gcol([fill(T(L3("{k} intervals d'amplària {a} cm, de {x0} a {x1} cm.", "{k} intervalos de anchura {a} cm, de {x0} a {x1} cm.", "{k} intervals of width {a} cm, from {x0} to {x1} cm.")), { k: V.length, a: amp, x0: a, x1: b })]);
      info.innerHTML = amp === 2 ? T(L3("Amb intervals tan estrets, moltes barres són baixes i el gràfic es veu dentat.", "Con intervalos tan estrechos, muchas barras son bajas y el gráfico se ve dentado.", "With such narrow intervals many bars are short and the chart looks jagged.")) :
        amp === 10 ? T(L3("Amb intervals tan amples, es perd informació: només hi ha poques barres.", "Con intervalos tan anchos, se pierde información: solo hay pocas barras.", "With such wide intervals we lose information: there are only a few bars.")) : "";
    }
    onLang(paint);
  }

  /* ---------- 10.5 sectors i pictogrames ---------- */
  var PRE_P = { tra: { x: function () { return TRAW[lang].join(" "); }, f: TRAF.join(" ") }, fru: PRE_G.fru };
  function wPie() {
    var w = document.getElementById("w-pie"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), kind = "pie";
    var relang = presetTab(w, I, PRE_P, paint, function (k) { kind = k; paint(); });
    function paint() {
      var t = tabIn(I); if (t.err) { out.innerHTML = ""; info.innerHTML = warn(t.err); return; }
      info.innerHTML = "";
      var N = sum(t.F), labs = t.labels;
      if (kind === "pie") {
        var each = 360 / N;
        var rows = t.F.map(function (f, i) { return [esc(labs[i]), tex(String(f)), tex("\\frac{" + f + "}{" + N + "}\\cdot360^\\circ" + eqr(f / N * 360) + "^\\circ")]; });
        rows.push(["<strong>" + T(TOTAL) + "</strong>", tex(String(N)), tex("360^\\circ")]);
        out.innerHTML = sectors({ cats: labs, vals: t.F, angles: true })
          + '<div class="fullw">' + tbl([T(L3("Valor", "Valor", "Value")), tex("f_i"), T(L3("Angle", "Ángulo", "Angle"))], rows, "freq")
          + "<p>" + (isInt(each) ? fill(T(L3("Cada dada val {a}.", "Cada dato vale {a}.", "Each value is worth {a}.")), { a: tex("360^\\circ:" + N + "=" + each + "^\\circ") }) : "") + "</p></div>";
      } else {
        var mx = Math.max.apply(null, t.F), unit = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000].filter(function (u) { return mx / u <= 8; })[0] || 1000;
        var icon = PRE_P.tra.f === I.f.value && /bus|autob/i.test(I.x.value) ? "🧍" : /poma|manzana|apple/i.test(I.x.value) ? "🍎" : "⭐";
        out.innerHTML = picto({ cats: labs, vals: t.F, unit: unit, icon: icon })
          + gcol([fill(T(L3("Cada {i} val {u}. Un tros d'icona val la part corresponent.", "Cada {i} vale {u}. Un trozo de icono vale la parte correspondiente.", "Each {i} stands for {u}. Part of an icon stands for that part.")), { i: icon, u: unit })]);
      }
    }
    onLang(function () { relang(); paint(); });
  }

  /* ---------- 10.6 moda, mitjana i mediana ---------- */
  function paramsHtml(a) {
    var s = sorted(a), n = a.length, m = meanOf(a), me = medianOf(a), mo = modesOf(a), c = countOf({ num: true, vals: a });
    var mid = n % 2 ? [(n - 1) / 2] : [n / 2 - 1, n / 2];
    var sl = s.map(function (x, i) { return mid.indexOf(i) >= 0 ? "\\boxed{" + nf(x) + "}" : nf(x); }).join(",\\ ");
    var moTxt = c.length === n && n > 1 ? T(L3("totes les dades apareixen una vegada: <b>no hi ha moda</b>.", "todos los datos aparecen una vez: <b>no hay moda</b>.", "every value appears once: <b>there is no mode</b>.")) :
      fill(T(L3("el valor que més es repeteix ({f} vegades): {m}.", "el valor que más se repite ({f} veces): {m}.", "the most repeated value ({f} times): {m}.")), { f: c.filter(function (o) { return o.v === mo[0]; })[0].f, m: tex("Mo=" + mo.map(nf).join(",\\ ")) });
    return rows2html([
      "<b>" + T(L3("Moda", "Moda", "Mode")) + "</b>: " + moTxt,
      "<b>" + T(L3("Mitjana", "Media", "Mean")) + "</b>: " + tex("\\bar x=\\frac{" + a.map(nfp).join("+") + "}{" + n + "}=\\frac{" + nf(sum(a)) + "}{" + n + "}" + eqr(m)),
      "<b>" + T(L3("Mediana", "Mediana", "Median")) + "</b>: " + T(L3("ordenem", "ordenamos", "in order")) + " " + tex(sl) + ". "
        + (n % 2 ? fill(T(L3("Hi ha {n} dades (senar): la central és la {k}a. ", "Hay {n} datos (impar): el central es el {k}.º. ", "There are {n} values (odd): the middle one is number {k}. ")), { n: n, k: (n + 1) / 2 }) + tex("Me=" + nf(me))
          : fill(T(L3("Hi ha {n} dades (parell): les centrals són la {a}a i la {b}a. ", "Hay {n} datos (par): los centrales son el {a}.º y el {b}.º. ", "There are {n} values (even): the middle ones are numbers {a} and {b}. ")), { n: n, a: n / 2, b: n / 2 + 1 }) + tex("Me=\\frac{" + nfp(s[n / 2 - 1]) + "+" + nfp(s[n / 2]) + "}{2}=" + nf(me)))
    ]);
  }
  function wParams() {
    var w = document.getElementById("w-params"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      var a = numsIn(I.d.value);
      if (!a || !a.length) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu nombres separats per espais: 4 7 7 10.", "Escribe números separados por espacios: 4 7 7 10.", "Type numbers separated by spaces: 4 7 7 10."))); return; }
      if (a.length > 30) { info.innerHTML = warn(T(L3("Com a molt 30 dades.", "Como mucho 30 datos.", "At most 30 values."))); return; }
      info.innerHTML = "";
      out.innerHTML = '<div class="hsteps">' + paramsHtml(a) + "</div>" + dotsAuto(a, { mean: meanOf(a), med: medianOf(a) })
        + '<p class="hint-s">' + T(L3("Triangle: mitjana (punt d'equilibri). Línia: mediana.", "Triángulo: media (punto de equilibrio). Línea: mediana.", "Triangle: mean (balance point). Line: median.")) + "</p>";
    }
    I.d.addEventListener("input", paint);
    onLang(paint);
  }
  function wBalance() {
    var w = document.getElementById("w-balance"); if (!w) return;
    var S = sliders(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      var a = [0, 1, 2, 3, 4].map(function (i) { var v = +S["v" + i].value; showRv(w, "v" + i, "x_" + (i + 1), v); return v; });
      var m = meanOf(a), me = medianOf(a);
      out.innerHTML = dots({ data: a, lo: 0, hi: 20, step: 1, mean: m, med: me })
        + gcol([tex("\\bar x=\\frac{" + nf(sum(a)) + "}{5}" + eqr(m)), tex("Me=" + nf(me))]);
      info.innerHTML = Math.abs(m - me) >= 3 ? T(L3("Hi ha una dada molt allunyada de les altres: la mitjana s'hi acosta, però la mediana quasi no es mou.", "Hay un dato muy alejado de los demás: la media se acerca a él, pero la mediana casi no se mueve.", "One value is far from the others: the mean moves towards it, but the median hardly moves.")) : "";
    }
    w.querySelectorAll('input[type="range"]').forEach(function (r) { r.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 10.7 taula de freqüències ---------- */
  var PRE_T = { germ: { x: "0 1 2 3 4", f: "3 9 5 2 1" }, not: { x: NOTX.join(" "), f: NOTF.join(" ") } };
  function tmeanHtml(X, F) {
    var N = sum(F), S = 0, Fi = 0, rows = [], acc = [];
    X.forEach(function (x, i) { Fi += F[i]; acc.push(Fi); S += x * F[i]; rows.push([tex(nf(x)), tex(String(F[i])), tex(String(Fi)), tex(nf(x * F[i]))]); });
    rows.push(["<strong>" + T(TOTAL) + "</strong>", tex("N=" + N), "", tex("\\textstyle\\sum=" + nf(S))]);
    function at(pos) { for (var i = 0; i < acc.length; i++) if (acc[i] >= pos) return X[i]; }
    var mf = Math.max.apply(null, F), mo = X.filter(function (x, i) { return F[i] === mf; });
    var med = N % 2 ? at((N + 1) / 2) : (at(N / 2) + at(N / 2 + 1)) / 2;
    return tbl([tex("x_i"), tex("f_i"), tex("F_i"), tex("x_i\\cdot f_i")], rows, "freq") + '<div class="hsteps">' + rows2html([
      "<b>" + T(L3("Mitjana", "Media", "Mean")) + "</b>: " + tex("\\bar x=\\frac{" + nf(S) + "}{" + N + "}" + eqr(S / N)),
      "<b>" + T(L3("Mediana", "Mediana", "Median")) + "</b>: " + (N % 2 ? fill(T(L3("la dada central és la {k}a: ", "el dato central es el {k}.º: ", "the middle value is number {k}: ")), { k: (N + 1) / 2 }) + tex("Me=" + nf(med))
        : fill(T(L3("les centrals són la {a}a i la {b}a, que valen {x} i {y}: ", "los centrales son el {a}.º y el {b}.º, que valen {x} y {y}: ", "the middle ones are numbers {a} and {b}, equal to {x} and {y}: ")), { a: N / 2, b: N / 2 + 1, x: tex(nf(at(N / 2))), y: tex(nf(at(N / 2 + 1))) }) + tex("Me=" + nf(med))),
      "<b>" + T(L3("Moda", "Moda", "Mode")) + "</b>: " + fill(T(L3("la freqüència més gran és {f}: ", "la frecuencia más grande es {f}: ", "the largest frequency is {f}: ")), { f: mf }) + tex("Mo=" + mo.map(nf).join(",\\ "))
    ]) + "</div>";
  }
  function wTmean() {
    var w = document.getElementById("w-tmean"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".tout"), info = w.querySelector(".info");
    presetTab(w, I, PRE_T, paint);
    function paint() {
      var t = tabIn(I, true); if (t.err) { out.innerHTML = ""; info.innerHTML = warn(t.err); return; }
      var X = t.X.slice(), F = t.F.slice(), ord = X.map(function (_, i) { return i; }).sort(function (a, b) { return X[a] - X[b]; });
      info.innerHTML = ""; out.innerHTML = tmeanHtml(ord.map(function (i) { return X[i]; }), ord.map(function (i) { return F[i]; }));
    }
    onLang(paint);
  }

  /* ---------- 10.8 dispersió ---------- */
  function dispHtml(a, nm) {
    var m = meanOf(a), d = a.map(function (x) { return Math.abs(x - m); });
    return "<b>" + nm + "</b>: " + tex("\\bar x=\\frac{" + nf(sum(a)) + "}{" + a.length + "}" + eqr(m)) + "; "
      + T(L3("rang", "rango", "range")) + " " + tex(nf(Math.max.apply(null, a)) + "-" + nfp(Math.min.apply(null, a)) + "=" + nf(rangeOf(a))) + "; "
      + tex((lang === "en" ? "MD" : "DM") + "=\\frac{" + d.map(function (x) { return nf(Math.round(x * 100) / 100); }).join("+") + "}{" + a.length + "}" + eqr(dmOf(a)));
  }
  function wDisp() {
    var w = document.getElementById("w-disp"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".tout"), info = w.querySelector(".info");
    function paint() {
      var A = numsIn(I.a.value), B = numsIn(I.b.value);
      if (!A || !B || !A.length || !B.length) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu dos grups de nombres separats per espais.", "Escribe dos grupos de números separados por espacios.", "Type two sets of numbers separated by spaces."))); return; }
      if (A.length > 12 || B.length > 12) { info.innerHTML = warn(T(L3("Com a molt 12 dades en cada grup.", "Como mucho 12 datos en cada grupo.", "At most 12 values in each set."))); return; }
      var all = A.concat(B), lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), st = Math.max(1, nice(Math.max(hi - lo, 1)) / 2);
      lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st) * st; if (hi === lo) { lo -= st; hi += st; }
      var dA = dmOf(A), dB = dmOf(B);
      out.innerHTML = '<div class="figs"><figure>' + dots({ data: A, lo: lo, hi: hi, step: st, mean: meanOf(A), dev: true }) + "<figcaption>A</figcaption></figure><figure>"
        + dots({ data: B, lo: lo, hi: hi, step: st, mean: meanOf(B), dev: true }) + "<figcaption>B</figcaption></figure></div>"
        + '<div class="hsteps">' + rows2html([dispHtml(A, "A"), dispHtml(B, "B"),
          near(dA, dB) ? T(L3("Els dos grups tenen la mateixa desviació mitjana.", "Los dos grupos tienen la misma desviación media.", "Both sets have the same mean deviation."))
            : fill(T(L3("El grup {g} té menys desviació mitjana: les seues dades estan més a prop de la mitjana (és més regular).", "El grupo {g} tiene menos desviación media: sus datos están más cerca de la media (es más regular).", "Set {g} has the smaller mean deviation: its values are closer to the mean (it's more consistent).")), { g: "<b>" + (dA < dB ? "A" : "B") + "</b>" })]) + "</div>";
      info.innerHTML = "";
    }
    [I.a, I.b].forEach(function (i) { i.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 10.9 quina nota necessite? ---------- */
  function wTarget() {
    var w = document.getElementById("w-target"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".tout"), info = w.querySelector(".info");
    function paint() {
      var a = numsIn(I.d.value), m = numIn(I.m.value), k = numIn(I.k.value);
      if (!a || !a.length || m === null || k === null || k < 1 || !isInt(k)) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu les notes separades per espais, la mitjana que vols i quants exàmens queden (1, 2…).", "Escribe las notas separadas por espacios, la media que quieres y cuántos exámenes quedan (1, 2…).", "Type the marks separated by spaces, the mean you want and how many tests are left (1, 2…)."))); return; }
      var n = a.length, S = sum(a), need = m * (n + k), x = (need - S) / k;
      var rows = [
        fill(T(L3("Suma que necessites amb {t} exàmens: ", "Suma que necesitas con {t} exámenes: ", "Sum you need with {t} tests: ")), { t: n + k }) + tex(nf(m) + "\\cdot" + (n + k) + "=" + nf(need)),
        T(L3("Suma que ja tens: ", "Suma que ya tienes: ", "Sum you already have: ")) + tex(a.map(nfp).join("+") + "=" + nf(S)),
        T(L3("Et falten: ", "Te faltan: ", "You still need: ")) + tex(nf(need) + "-" + nfp(S) + "=" + nf(need - S)) + (k > 1 ? "; " + fill(T(L3("en cada un dels {k} exàmens: ", "en cada uno de los {k} exámenes: ", "in each of the {k} tests: ")), { k: k }) + tex("\\frac{" + nf(need - S) + "}{" + k + "}" + eqr(x)) : "")
      ];
      out.innerHTML = '<div class="hsteps">' + rows2html(rows) + "</div>";
      info.innerHTML = x > 10 + 1e-9 ? warn(T(L3("Necessitaries més d'un 10: amb aquests exàmens no és possible.", "Necesitarías más de un 10: con estos exámenes no es posible.", "You'd need more than 10: it isn't possible with these tests.")))
        : x <= 0 ? '<span class="ok">' + T(L3("Ja la tens assegurada, encara que tragues un 0!", "¡Ya la tienes asegurada, aunque saques un 0!", "You've already got it, even with a 0!")) + "</span>"
        : '<span class="ok">' + fill(T(L3("Necessites com a mínim un {x}.", "Necesitas como mínimo un {x}.", "You need at least {x}.")), { x: tex(nf(Math.ceil(x * 100) / 100)) }) + "</span>";
    }
    [I.d, I.m, I.k].forEach(function (i) { i.addEventListener("input", paint); });
    onLang(function () { if (lang === "en") I.m.value = I.m.value.replace(",", "."); else I.m.value = I.m.value.replace(".", ","); paint(); });
  }

  /* ---------- entrenadors ---------- */
  function optsTxt(right, wrongs) {
    var all = [right].concat(wrongs), order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return all[i]; }), ans: order.indexOf(0) };
  }
  function ret(o, q, s) { o.q = q; o.s = s; return o; }
  function numQ(v, tol) { return { num: v, tol: tol || 1e-6 }; }
  function same(o) { return { va: o, es: o, en: o }; }
  function $(s) { return "$" + s + "$"; }
  function rlist(n, a, b) { var o = []; for (var i = 0; i < n; i++) o.push(rint(a, b)); return o; }
  var TYP = [L3("Qualitativa", "Cualitativa", "Qualitative"), L3("Quantitativa discreta", "Cuantitativa discreta", "Discrete quantitative"), L3("Quantitativa contínua", "Cuantitativa continua", "Continuous quantitative")];
  var VARS = [
    [L3("color dels ulls", "color de los ojos", "eye colour"), 0], [L3("esport preferit", "deporte preferido", "favourite sport"), 0], [L3("mes de naixement", "mes de nacimiento", "month of birth"), 0],
    [L3("marca de les sabatilles", "marca de las zapatillas", "trainer brand"), 0], [L3("grup de música preferit", "grupo de música preferido", "favourite band"), 0], [L3("mitjà de transport per a vindre a l'institut", "medio de transporte para venir al instituto", "how you get to school"), 0],
    [L3("talla de samarreta (S, M, L)", "talla de camiseta (S, M, L)", "T-shirt size (S, M, L)"), 0], [L3("nombre de germans", "número de hermanos", "number of siblings"), 1], [L3("gols marcats en un partit", "goles marcados en un partido", "goals scored in a match"), 1],
    [L3("nombre de llibres llegits en un any", "número de libros leídos en un año", "number of books read in a year"), 1], [L3("nombre de mascotes", "número de mascotas", "number of pets"), 1], [L3("alumnes que hi ha en cada classe", "alumnos que hay en cada clase", "students in each class"), 1],
    [L3("nombre de missatges rebuts en un dia", "número de mensajes recibidos en un día", "messages received in a day"), 1], [L3("alçada", "altura", "height"), 2], [L3("pes", "peso", "weight"), 2],
    [L3("temps que tardes a arribar a l'institut", "tiempo que tardas en llegar al instituto", "time it takes you to get to school"), 2], [L3("temperatura màxima d'un dia", "temperatura máxima de un día", "maximum temperature of a day"), 2],
    [L3("litres d'aigua que beus en un dia", "litros de agua que bebes en un día", "litres of water you drink in a day"), 2], [L3("longitud de la mà", "longitud de la mano", "length of your hand"), 2], [L3("temps que dorms cada nit", "tiempo que duermes cada noche", "time you sleep each night"), 2]
  ];
  var POB = [
    [L3("Per a saber l'alçada mitjana de l'alumnat d'un institut, es mesuren 40 alumnes triats a l'atzar.", "Para saber la altura media del alumnado de un instituto, se miden 40 alumnos elegidos al azar.", "To find the mean height of a school's students, 40 students chosen at random are measured."), 1],
    [L3("Per a fer la llista de classe, el tutor pregunta la data de naixement a tots els seus alumnes.", "Para hacer la lista de clase, el tutor pregunta la fecha de nacimiento a todos sus alumnos.", "To make the class list, the tutor asks all his students for their date of birth."), 0],
    [L3("Per a saber quant duren les piles d'una fàbrica, se'n proven 100 d'una producció de 50 000.", "Para saber cuánto duran las pilas de una fábrica, se prueban 100 de una producción de 50 000.", "To find how long a factory's batteries last, 100 out of 50,000 are tested."), 1],
    [L3("En unes eleccions, voten totes les persones del cens.", "En unas elecciones, votan todas las personas del censo.", "In an election, everyone on the electoral roll votes."), 0],
    [L3("Una empresa d'enquestes pregunta a 1 000 persones a qui votaran.", "Una empresa de encuestas pregunta a 1 000 personas a quién votarán.", "A polling company asks 1,000 people who they will vote for."), 1],
    [L3("El metge de l'institut revisa la vista de tots els alumnes de 1r d'ESO.", "El médico del instituto revisa la vista de todos los alumnos de 1.º de ESO.", "The school doctor checks the eyesight of every Year 7 student."), 0],
    [L3("Per a controlar la qualitat de l'aigua d'un riu, se n'agafen 10 pots en diferents llocs.", "Para controlar la calidad del agua de un río, se cogen 10 botes en diferentes lugares.", "To check the quality of a river's water, 10 jars are filled at different places."), 1],
    [L3("Un professor calcula la nota mitjana de l'examen amb les notes de tots els seus alumnes.", "Un profesor calcula la nota media del examen con las notas de todos sus alumnos.", "A teacher works out the mean test mark using every one of his students' marks."), 0]
  ];
  var POBO = [L3("Tota la població", "Toda la población", "The whole population"), L3("Una mostra", "Una muestra", "A sample")];
  function sTable(X, F) { return tex("\\begin{array}{c|" + X.map(function () { return "c"; }).join("") + "}x_i&" + X.map(nf).join("&") + "\\\\\\hline f_i&" + F.join("&") + "\\end{array}"); }
  function cleanMean(n, a, b) {
    for (var t = 0; t < 200; t++) { var o = rlist(n - 1, a, b), m = rint(a + 1, b - 1), last = n * m - sum(o); if (last >= a && last <= b) { o.push(last); return shuffle(o); } }
    return [a, b];
  }
  var GEN = {
    tipus: function () {
      var v = pick(VARS);
      return ret({ opts: TYP, ans: v[1] }, function () { return fill(T(L3("Variable: «{v}».", "Variable: «{v}».", "Variable: “{v}”.")), { v: T(v[0]) }); },
        function () { return T([L3("Els valors no són nombres: és qualitativa.", "Los valores no son números: es cualitativa.", "The values aren't numbers: it's qualitative."), L3("És un nombre que es compta: quantitativa discreta.", "Es un número que se cuenta: cuantitativa discreta.", "It's a number you count: discrete quantitative."), L3("És un nombre que es mesura: quantitativa contínua.", "Es un número que se mide: cuantitativa continua.", "It's a number you measure: continuous quantitative.")][v[1]]); });
    },
    pobmos: function () {
      var v = pick(POB);
      return ret({ opts: POBO, ans: v[1] }, function () { return T(v[0]) + " " + T(L3("S'estudia tota la població o una mostra?", "¿Se estudia toda la población o una muestra?", "Is the whole population studied, or a sample?")); },
        function () { return T(v[1] ? L3("Només s'estudia una part dels individus: és una mostra.", "Solo se estudia una parte de los individuos: es una muestra.", "Only some of the individuals are studied: it's a sample.") : L3("S'estudien tots els individus: és tota la població.", "Se estudian todos los individuos: es toda la población.", "Every individual is studied: it's the whole population.")); });
    },
    freq: function () {
      var a = rlist(rint(14, 20), 0, 5), v = pick(a), f = a.filter(function (x) { return x === v; }).length;
      return ret(numQ(f), function () { return fill(T(L3("Dades: {d}. Quina és la freqüència absoluta del {v}?", "Datos: {d}. ¿Cuál es la frecuencia absoluta del {v}?", "Data: {d}. What is the absolute frequency of {v}?")), { d: $(listTex(a)), v: $(v) }); },
        function () { return fill(T(L3("El {v} apareix {f} vegades: ", "El {v} aparece {f} veces: ", "{v} appears {f} times: ")), { v: tex(String(v)), f: f }) + tex("f=" + f); });
    },
    rel: function () {
      var N = pick([20, 25, 40, 50]), f = rint(1, N / 2), pct = rint(0, 1), h = f / N;
      return ret(numQ(pct ? 100 * h : h, 1e-6), function () { return fill(T(pct ? L3("En {N} dades, un valor apareix {f} vegades. Quin percentatge representa? (escriu només el nombre)", "En {N} datos, un valor aparece {f} veces. ¿Qué porcentaje representa? (escribe solo el número)", "In {N} values, one value appears {f} times. What percentage is that? (type just the number)") : L3("En {N} dades, un valor apareix {f} vegades. Quina és la seua freqüència relativa (en decimal)?", "En {N} datos, un valor aparece {f} veces. ¿Cuál es su frecuencia relativa (en decimal)?", "In {N} values, one value appears {f} times. What is its relative frequency (as a decimal)?")), { N: N, f: f }); },
        function () { return tex("h=\\frac{" + f + "}{" + N + "}=" + nf(h)) + (pct ? " → " + tex(nf(100 * h) + "\\ \\%") : ""); });
    },
    acum: function () {
      var X = [0, 1, 2, 3, 4], F = X.map(function () { return rint(1, 8); }), N = sum(F), k = rint(1, 3), md = rint(0, 2), acc = 0, Fk;
      F.forEach(function (f, i) { acc += f; if (i === k) Fk = acc; });
      var v = md === 0 ? Fk : md === 1 ? N - Fk : N;
      return ret(numQ(v), function () {
        return sTable(X, F) + "<br>" + T([L3("Quantes dades són menors o iguals que {k}?", "¿Cuántos datos son menores o iguales que {k}?", "How many values are less than or equal to {k}?"), L3("Quantes dades són més grans que {k}?", "¿Cuántos datos son mayores que {k}?", "How many values are greater than {k}?"), L3("Quantes dades hi ha en total?", "¿Cuántos datos hay en total?", "How many values are there altogether?")][md]).replace("{k}", tex(String(k)));
      }, function () {
        var s = F.slice(0, k + 1).join("+");
        return md === 0 ? tex("F=" + s + "=" + Fk) : md === 1 ? tex("N-F=" + N + "-" + Fk + "=" + (N - Fk)) : tex("N=" + F.join("+") + "=" + N);
      });
    },
    readbar: function () {
      var X = ["0", "1", "2", "3", "4", "5"].slice(0, rint(4, 6)), F = X.map(function () { return rint(1, 9); }), md = rint(0, 2), i = rint(0, X.length - 1), j;
      do { j = rint(0, X.length - 1); } while (j === i);
      var v = md === 0 ? F[i] : md === 1 ? sum(F) : Math.abs(F[i] - F[j]);
      return ret(numQ(v), function () {
        return T([L3("Quina és la freqüència del valor {a}?", "¿Cuál es la frecuencia del valor {a}?", "What is the frequency of the value {a}?"), L3("Quantes dades hi ha en total?", "¿Cuántos datos hay en total?", "How many values are there altogether?"), L3("Quina diferència hi ha entre les freqüències de {a} i {b}?", "¿Qué diferencia hay entre las frecuencias de {a} y {b}?", "What is the difference between the frequencies of {a} and {b}?")][md]).replace("{a}", tex(X[i])).replace("{b}", tex(X[j]))
          + barres({ cats: X, vals: F, W: 260, H: 170, hl: md === 1 ? null : i });
      }, function () { return md === 0 ? T(L3("L'altura de la barra és ", "La altura de la barra es ", "The bar's height is ")) + tex(String(F[i])) : md === 1 ? tex("N=" + F.join("+") + "=" + v) : tex("|" + F[i] + "-" + F[j] + "|=" + v); });
    },
    angle: function () {
      var N = pick([12, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120]), f = rint(1, Math.floor(N * 0.6)), a = f / N * 360;
      return ret(numQ(a), function () { return fill(T(L3("En un diagrama de sectors de {N} dades, quants graus té el sector d'un valor amb {f}?", "En un diagrama de sectores de {N} datos, ¿cuántos grados tiene el sector de un valor con {f}?", "In a pie chart of {N} values, how many degrees is the slice of a value with {f}?")), { N: N, f: $("f=" + f) }); },
        function () { return tex("\\frac{" + f + "}{" + N + "}\\cdot360^\\circ=" + nf(a) + "^\\circ"); });
    },
    pieread: function () {
      var N = pick([20, 24, 30, 36, 40, 60, 72, 90, 120, 180]), f = rint(1, Math.floor(N * 0.6)), a = f / N * 360;
      return ret(numQ(f), function () { return fill(T(L3("S'ha preguntat a {N} persones. Quantes persones representa un sector de {a}?", "Se ha preguntado a {N} personas. ¿Cuántas personas representa un sector de {a}?", "{N} people were asked. How many people does a slice of {a} represent?")), { N: N, a: $(nf(a) + "^\\circ") }); },
        function () { return tex("\\frac{" + nf(a) + "}{360}\\cdot" + N + "=" + f); });
    },
    mitjana: function () {
      var n = rint(4, 7), a = rint(0, 2) ? cleanMean(n, 1, 10) : rlist(n, 1, 12), m = meanOf(a);
      return ret(numQ(m, 0.006), function () { return fill(T(L3("Calcula la mitjana de {d} (si cal, arrodoneix a les centèsimes).", "Calcula la media de {d} (si hace falta, redondea a las centésimas).", "Find the mean of {d} (round to hundredths if needed).")), { d: $(listTex(a)) }); },
        function () { return tex("\\bar x=\\frac{" + a.join("+") + "}{" + n + "}=\\frac{" + sum(a) + "}{" + n + "}" + eqr(m)); });
    },
    mediana: function () {
      var n = rint(5, 8), a = rlist(n, 1, 20), s = sorted(a), me = medianOf(a);
      return ret(numQ(me), function () { return fill(T(L3("Calcula la mediana de {d}.", "Calcula la mediana de {d}.", "Find the median of {d}.")), { d: $(listTex(a)) }); },
        function () {
          var mid = n % 2 ? [(n - 1) / 2] : [n / 2 - 1, n / 2];
          return T(L3("Ordenem: ", "Ordenamos: ", "In order: ")) + tex(s.map(function (x, i) { return mid.indexOf(i) >= 0 ? "\\boxed{" + x + "}" : String(x); }).join(",\\ ")) + " → "
            + tex(n % 2 ? "Me=" + me : "Me=\\frac{" + s[n / 2 - 1] + "+" + s[n / 2] + "}{2}=" + nf(me));
        });
    },
    moda: function () {
      var a, mo;
      do { a = rlist(rint(7, 10), 1, 9); mo = modesOf(a); } while (mo.length !== 1);
      var others = shuffle(a.filter(function (x) { return x !== mo[0]; }).filter(function (x, i, s) { return s.indexOf(x) === i; })).slice(0, 2);
      var c = a.filter(function (x) { return x === mo[0]; }).length;
      return ret({ opts: [same($(String(mo[0])))].concat(others.map(function (x) { return same($(String(x))); })) }, function () { return fill(T(L3("Quina és la moda de {d}?", "¿Cuál es la moda de {d}?", "What is the mode of {d}?")), { d: $(listTex(a)) }); },
        function () { return fill(T(L3("El {m} apareix {c} vegades, més que cap altre.", "El {m} aparece {c} veces, más que ningún otro.", "{m} appears {c} times, more than any other.")), { m: tex(String(mo[0])), c: c }); });
    },
    rang: function () {
      var a = rlist(rint(5, 8), -8, 20);
      return ret(numQ(rangeOf(a)), function () { return fill(T(L3("Calcula el rang de {d}.", "Calcula el rango de {d}.", "Find the range of {d}.")), { d: $(listTex(a)) }); },
        function () { var M = Math.max.apply(null, a), m = Math.min.apply(null, a); return tex(nf(M) + "-" + nfp(m) + "=" + nf(M - m)); });
    },
    dm: function () {
      var a = cleanMean(rint(4, 5), 1, 12), m = meanOf(a), d = a.map(function (x) { return Math.abs(x - m); }), v = dmOf(a);
      return ret(numQ(v, 0.006), function () { return fill(T(L3("Calcula la desviació mitjana de {d} (la mitjana és {m}).", "Calcula la desviación media de {d} (la media es {m}).", "Find the mean deviation of {d} (the mean is {m}).")), { d: $(listTex(a)), m: $(nf(m)) }); },
        function () { return tex((lang === "en" ? "MD" : "DM") + "=\\frac{" + d.join("+") + "}{" + a.length + "}=\\frac{" + sum(d) + "}{" + a.length + "}" + eqr(v)); });
    },
    tmean: function () {
      var k = rint(3, 4), x0 = rint(0, 5), X = [], F = [];
      for (var i = 0; i < k; i++) { X.push(x0 + i); F.push(rint(1, 8)); }
      var N = sum(F), S = sum(X.map(function (x, i) { return x * F[i]; }));
      return ret(numQ(S / N, 0.006), function () { return T(L3("Calcula la mitjana (arrodoneix a les centèsimes si cal):", "Calcula la media (redondea a las centésimas si hace falta):", "Find the mean (round to hundredths if needed):")) + "<br>" + sTable(X, F); },
        function () { return tex("\\bar x=\\frac{" + X.map(function (x, i) { return x + "\\cdot" + F[i]; }).join("+") + "}{" + N + "}=\\frac{" + S + "}{" + N + "}" + eqr(S / N)); });
    },
    falta: function () {
      var n = rint(3, 5), a = cleanMean(n, 2, 10), m = meanOf(a), j = rint(0, n - 1), x = a[j], rest = a.filter(function (_, i) { return i !== j; });
      return ret(numQ(x), function () { return fill(T(L3("La mitjana de {n} nombres és {m}. Si {k} d'ells són {d}, quin és l'altre?", "La media de {n} números es {m}. Si {k} de ellos son {d}, ¿cuál es el otro?", "The mean of {n} numbers is {m}. If {k} of them are {d}, what is the other one?")), { n: n, m: $(nf(m)), k: n - 1, d: $(listTex(rest)) }); },
        function () { return tex(nf(m) + "\\cdot" + n + "=" + nf(m * n)) + "; " + tex(nf(m * n) + "-(" + rest.join("+") + ")=" + nf(x)); });
    }
  };

  function wDrill(w) {
    var kind = w.dataset.kind, q, done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore"), ob = w.querySelector(".dopts");
    function gen() { q = GEN[kind](); if (q.opts && q.ans == null) { var o = optsTxt(q.opts[0], q.opts.slice(1)); q.opts = o.opts; q.ans = o.ans; } }
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (ob) {
        ob.innerHTML = "";
        q.opts.forEach(function (o, j) {
          var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.innerHTML = rtex(T(o));
          if (done) { b.disabled = true; if (j === q.ans) b.classList.add("right"); else if (j === res.pick) b.classList.add("wrong"); }
          b.addEventListener("click", function () { check(j); }); ob.appendChild(b);
        });
      }
      if (done) info.innerHTML = (res.good ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u("wrong") + "</span>") + '<div class="dsol">' + u("sol") + " " + q.s() + "</div>";
    }
    function check(j) {
      if (done) return;
      var good;
      if (q.opts) good = j === q.ans;
      else {
        var v = numIn(String(inp.value).replace("%", "")); if (v === null) { info.innerHTML = warn(u("num")); return; }
        good = Math.abs(v - q.num) <= (q.tol || 1e-6);
      }
      done = true; tot++; res = { good: good, pick: j }; if (good) ok++;
      paint();
    }
    function fresh() { gen(); done = false; if (inp) inp.value = ""; info.innerHTML = ""; paint(); }
    var cb = w.querySelector('[data-a="check"]'); if (cb) cb.addEventListener("click", function () { check(); });
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); if (inp) inp.focus(); });
    if (inp) inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    gen(); onLang(paint);
  }
  window.FM110 = { GEN: GEN, meanOf: meanOf, medianOf: medianOf, modesOf: modesOf, rangeOf: rangeOf, dmOf: dmOf, dataIn: dataIn, countOf: countOf, tokensIn: tokensIn, barres: barres, sectors: sectors, hist: hist, dots: dots, picto: picto };


  /* ---------- qüestionari ---------- */
  var QUIZ = [
/*QUIZ*/
  ];

  var answers = {};
  function wQuiz() {
    var box = document.getElementById("quiz-box"), score = document.getElementById("quiz-score");
    if (!box) return;
    function render() {
      box.innerHTML = ""; var ok = 0, done = 0;
      QUIZ.forEach(function (q, i) {
        var d = document.createElement("div"); d.className = "q";
        d.innerHTML = '<p class="qt">' + (i + 1) + ". " + rtex(q.q[lang]) + '</p><div class="opts"></div><div class="fb"></div>';
        var opts = d.querySelector(".opts"), fb = d.querySelector(".fb");
        q.o.forEach(function (o, j) {
          var b = document.createElement("button"); b.type = "button"; b.innerHTML = rtex(o[lang] || o.va);
          if (answers[i] != null) {
            b.disabled = true;
            if (j === q.a) b.classList.add("right"); else if (j === answers[i]) b.classList.add("wrong");
          }
          b.addEventListener("click", function () { answers[i] = j; render(); });
          opts.appendChild(b);
        });
        if (answers[i] != null) { done++; if (answers[i] === q.a) ok++; fb.innerHTML = "<strong>" + (answers[i] === q.a ? "✓ " + u("right") : "✗ " + u("wrong")) + "</strong> " + rtex(q.e[lang]); }
        box.appendChild(d);
      });
      score.textContent = done ? u("score") + ": " + ok + " / " + QUIZ.length : "";
    }
    document.getElementById("quiz-reset").addEventListener("click", function () { answers = {}; render(); });
    onLang(render);
  }

  /* ---------- passos ---------- */
  function wSteps() {
    document.querySelectorAll(".steps").forEach(function (s) {
      var steps = [].slice.call(s.children).filter(function (c) { return c.classList.contains("step"); });
      if (steps.length < 2) return;
      s.classList.add("js");
      var shown = 1, ctl = document.createElement("div"); ctl.className = "steps-ctl";
      var bn = document.createElement("button"), ba = document.createElement("button"), cnt = document.createElement("span");
      bn.type = ba.type = "button"; bn.className = "btn primary"; ba.className = "btn"; cnt.className = "step-count";
      ctl.appendChild(bn); ctl.appendChild(ba); ctl.appendChild(cnt); s.after(ctl);
      function upd() {
        steps.forEach(function (st, i) { st.classList.toggle("hidden", i >= shown); });
        bn.textContent = u("next") + " →"; bn.disabled = shown >= steps.length;
        ba.textContent = shown >= steps.length ? u("reset") : u("all");
        cnt.textContent = u("step") + " " + shown + " " + u("of") + " " + steps.length;
      }
      bn.addEventListener("click", function () { if (shown < steps.length) { shown++; upd(); steps[shown - 1].scrollIntoView({ block: "nearest", behavior: "smooth" }); } });
      ba.addEventListener("click", function () { shown = shown >= steps.length ? 1 : steps.length; upd(); });
      onLang(upd);
    });
  }

  /* ---------- índex, progrés i seccions estudiades ---------- */
  function wNav() {
    var links = [].slice.call(document.querySelectorAll("#toc-list a")), secs = links.map(function (a) { return document.querySelector(a.getAttribute("href")); });
    var bar = document.getElementById("progress"), top = document.getElementById("to-top");
    function onScroll() {
      var h = document.documentElement, max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? h.scrollTop / max * 100 : 0) + "%";
      top.classList.toggle("show", h.scrollTop > 800);
      var y = window.scrollY + 140, idx = 0;
      secs.forEach(function (s, i) { if (s && s.offsetTop <= y) idx = i; });
      links.forEach(function (a, i) { a.classList.toggle("active", i === idx); });
    }
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
    top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
    var done = {}; try { done = JSON.parse(store(UNIT_KEY) || "{}") || {}; } catch (e) {}
    var heads = document.querySelectorAll("section.unit[id^='s'] .sec-head");
    heads.forEach(function (hd) {
      var id = hd.parentNode.id, b = document.createElement("button"); b.type = "button"; b.className = "done-btn";
      function upd() { b.setAttribute("aria-pressed", String(!!done[id])); b.textContent = (done[id] ? "✓ " + u("studied") : "○ " + u("mark")); }
      b.addEventListener("click", function () { done[id] = !done[id]; store(UNIT_KEY, JSON.stringify(done)); upd(); meter(); });
      hd.appendChild(b); onLang(upd);
    });
    function meter() {
      var n = 0; links.forEach(function (a) { var id = a.getAttribute("href").slice(1); a.classList.toggle("done", !!done[id]); if (done[id]) n++; });
      document.getElementById("meter").style.width = (n / NSEC * 100) + "%"; document.getElementById("meter-n").textContent = n;
    }
    meter();
    var d = document.getElementById("toc-d");
    var mq = window.matchMedia("(max-width: 960px)");
    d.open = !mq.matches;
    if (mq.addEventListener) mq.addEventListener("change", function () { d.open = !mq.matches; });
    links.forEach(function (a) { a.addEventListener("click", function () { if (window.matchMedia("(max-width: 960px)").matches) d.open = false; }); });
  }

  /* ---------- idioma i tema ---------- */
  var ICON = {
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
  };
  function curTheme() { var t = root.getAttribute("data-theme"); return t || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"); }
  function wChrome() {
    var tb = document.getElementById("theme-btn");
    function paintTheme() { tb.innerHTML = curTheme() === "dark" ? ICON.sun : ICON.moon; tb.setAttribute("aria-label", u("theme")); }
    tb.addEventListener("click", function () { var n = curTheme() === "dark" ? "light" : "dark"; root.setAttribute("data-theme", n); store("theme", n); paintTheme(); });
    var btns = document.querySelectorAll("[data-setlang]");
    function paintLang() { btns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.setlang === lang)); }); }
    btns.forEach(function (b) { b.addEventListener("click", function () { setLang(b.dataset.setlang); }); });
    onLang(function () { paintTheme(); paintLang(); });
  }

  var TITLES = { va: "Estadística · FentMates", es: "Estadística · FentMates", en: "Statistics · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }

  function init() {
    document.title = TITLES[lang];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }],
        ignoredClasses: ["widget"], throwOnError: false, strict: "ignore", macros: KOPT.macros, trust: KOPT.trust
      });
    }
    wChrome(); wSteps(); wNav();
    wDice(); wTally(); wChart(); wHist(); wPie(); wParams(); wBalance(); wTmean(); wDisp(); wTarget();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
