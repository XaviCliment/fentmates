(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-a-u10-done", NSEC = 6;

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
     unitat 10 (4t ESO A): estadística bidimensional
     ====================================================================== */
  function eqr(v) { var r = Math.round(v * 100) / 100; return (near(r, v) ? "=" : "\\approx ") + nf(r); }
  function numsIn(raw) {
    var parts = String(raw).replace(/[−–]/g, "-").trim().split(/[\s;]+/).filter(function (s) { return s.length; });
    var out = parts.map(numIn); return out.some(function (v) { return v === null; }) ? null : out;
  }
  function sum(a) { return a.reduce(function (s, x) { return s + x; }, 0); }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function r2(v) { return Math.round(v * 100) / 100; }
  function sg(v) { return v < 0 ? "-" + nf(-v) : "+" + nf(v); }
  function lineTex(m, n) { m = r2(m); n = r2(n); return "y=" + (near(m, 1) ? "" : near(m, -1) ? "-" : nf(m)) + "x" + (near(n, 0) ? "" : sg(n)); }
  function tbl(head, rows, cls) {
    return '<div class="tbl-wrap"><table class="data c ' + (cls || "") + '"><thead><tr>' + head.map(function (h) { return "<th>" + h + "</th>"; }).join("") + "</tr></thead><tbody>"
      + rows.map(function (r) { return "<tr>" + r.map(function (c) { return "<td>" + c + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table></div>";
  }
  /* paràmetres bidimensionals */
  function biOf(x, y) {
    var N = x.length, sx = 0, sy = 0, sx2 = 0, sy2 = 0, sxy = 0;
    for (var i = 0; i < N; i++) { sx += x[i]; sy += y[i]; sx2 += x[i] * x[i]; sy2 += y[i] * y[i]; sxy += x[i] * y[i]; }
    var mx = sx / N, my = sy / N, vx = sx2 / N - mx * mx, vy = sy2 / N - my * my, c = sxy / N - mx * my;
    if (Math.abs(vx) < 1e-10) vx = 0; if (Math.abs(vy) < 1e-10) vy = 0; if (Math.abs(c) < 1e-10) c = 0;
    var r = vx > 0 && vy > 0 ? Math.max(-1, Math.min(1, c / Math.sqrt(vx * vy))) : NaN;
    return { N: N, sx: sx, sy: sy, sx2: sx2, sy2: sy2, sxy: sxy, mx: mx, my: my, vx: vx, vy: vy, c: c, r: r };
  }
  function rlOf(S) { var m = S.c / S.vx; return { m: m, n: S.my - m * S.mx }; }
  function rWords(r) {
    if (!isFinite(r)) return T(L3("No es pot calcular r: una de les variables no varia.", "No se puede calcular r: una de las variables no varía.", "r can't be worked out: one of the variables doesn't vary."));
    var a = Math.abs(r);
    if (a > 0.9999) return T(r > 0 ? L3("positiva perfecta (relació funcional)", "positiva perfecta (relación funcional)", "perfect positive (functional relationship)") : L3("negativa perfecta (relació funcional)", "negativa perfecta (relación funcional)", "perfect negative (functional relationship)"));
    if (a < 0.1) return T(L3("pràcticament nul·la", "prácticamente nula", "practically zero"));
    var k = a >= 0.8 ? 0 : a >= 0.5 ? 1 : 2;
    var P = [L3("positiva i forta", "positiva y fuerte", "strong positive"), L3("positiva moderada", "positiva moderada", "moderate positive"), L3("positiva i feble", "positiva y débil", "weak positive")];
    var N_ = [L3("negativa i forta", "negativa y fuerte", "strong negative"), L3("negativa moderada", "negativa moderada", "moderate negative"), L3("negativa i feble", "negativa y débil", "weak negative")];
    return T((r > 0 ? P : N_)[k]);
  }
  function corrTxt(r) { return T(L3("Correlació", "Correlación", "Correlation")) + " <b>" + rWords(r) + "</b>"; }

  /* ---------- núvols de punts (còpia de nuvol() de comu.py) ---------- */
  function nstep(lo, hi) { var span = hi - lo, st = Math.pow(10, Math.floor(Math.log10(span / 5))), ks = [1, 2, 5, 10]; for (var i = 0; i < 4; i++) if (span / (st * ks[i]) <= 6) return st * ks[i]; return st * 10; }
  function autoR(vals, extra) {
    var a = Math.min.apply(null, vals.concat(extra || [])), b = Math.max.apply(null, vals.concat(extra || []));
    if (b - a < 1e-9) { a -= 1; b += 1; }
    var pad = (b - a) * 0.08, lo = a - pad, hi = b + pad, st = nstep(lo, hi);
    lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st) * st;
    if (a >= 0 && lo < 0) lo = 0; if (a >= 0 && lo > 0 && lo <= 2 * st) lo = 0;
    return [lo, hi, st];
  }
  function numL(v) { var r = Math.round(v * 1000) / 1000; return String(r).replace("-", "−").replace(".", lang === "en" ? "." : ","); }
  /* o: xr, yr ([mín, màx, pas]), axes, means, reg, line ([m, n]), res (errors fins a line), est ([x, y]), hl, W, H, rad */
  function cloud(pts, o) {
    o = o || {};
    var W = o.W || 340, H = o.H || 250, ML = 40, MR = 14, MT = 14, MB = 32;
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var xr = o.xr || autoR(xs.length ? xs : [0, 10], o.est ? [o.est[0]] : null), yr = o.yr || autoR(ys.length ? ys : [0, 10], o.est ? [o.est[1]] : null);
    function X(v) { return ML + (v - xr[0]) / (xr[1] - xr[0]) * (W - ML - MR); }
    function Y(v) { return H - MB - (v - yr[0]) / (yr[1] - yr[0]) * (H - MT - MB); }
    var g = "", v, f = function (n) { return n.toFixed(1); };
    for (v = xr[0]; v <= xr[1] + 1e-9; v += xr[2]) g += '<line class="grid" x1="' + f(X(v)) + '" y1="' + MT + '" x2="' + f(X(v)) + '" y2="' + (H - MB) + '"/><text class="tk" x="' + f(X(v)) + '" y="' + (H - MB + 15) + '" text-anchor="middle">' + numL(v) + "</text>";
    for (v = yr[0]; v <= yr[1] + 1e-9; v += yr[2]) g += '<line class="grid" x1="' + ML + '" y1="' + f(Y(v)) + '" x2="' + (W - MR) + '" y2="' + f(Y(v)) + '"/><text class="tk" x="' + (ML - 5) + '" y="' + f(Y(v) + 4) + '" text-anchor="end">' + numL(v) + "</text>";
    g += '<line class="ax" x1="' + ML + '" y1="' + (H - MB) + '" x2="' + (W - MR) + '" y2="' + (H - MB) + '"/><line class="ax" x1="' + ML + '" y1="' + MT + '" x2="' + ML + '" y2="' + (H - MB) + '"/>';
    if (o.axes) g += '<text class="tk ax-t" x="' + (W - MR) + '" y="' + (H - MB - 6) + '" text-anchor="end">' + esc(o.axes[0]) + '</text><text class="tk ax-t" x="' + (ML + 6) + '" y="' + (MT + 11) + '">' + esc(o.axes[1]) + "</text>";
    var S = pts.length > 1 ? biOf(xs, ys) : null;
    function seg(m, n, cls) {
      var a = xr[0], b = xr[1];
      if (m) { var c1 = (yr[0] - n) / m, c2 = (yr[1] - n) / m; a = Math.max(a, Math.min(c1, c2)); b = Math.min(b, Math.max(c1, c2)); }
      else if (n < yr[0] || n > yr[1]) return "";
      return b > a ? '<line class="' + cls + '" x1="' + f(X(a)) + '" y1="' + f(Y(m * a + n)) + '" x2="' + f(X(b)) + '" y2="' + f(Y(m * b + n)) + '"/>' : "";
    }
    if (o.means && S) g += '<line class="meanl" x1="' + f(X(S.mx)) + '" y1="' + MT + '" x2="' + f(X(S.mx)) + '" y2="' + (H - MB) + '"/><line class="meanl" x1="' + ML + '" y1="' + f(Y(S.my)) + '" x2="' + (W - MR) + '" y2="' + f(Y(S.my)) + '"/>';
    if (o.line) {
      if (o.res) pts.forEach(function (p) { var yh = o.line[0] * p[0] + o.line[1], yc = Math.max(yr[0], Math.min(yr[1], yh)); g += '<line class="res" x1="' + f(X(p[0])) + '" y1="' + f(Y(p[1])) + '" x2="' + f(X(p[0])) + '" y2="' + f(Y(yc)) + '"/>'; });
      g += seg(o.line[0], o.line[1], "eyel");
    }
    if (o.reg && S && S.vx > 0) { var R = rlOf(S); g += seg(R.m, R.n, "regl"); }
    if (o.est) g += '<line class="estl" x1="' + f(X(o.est[0])) + '" y1="' + (H - MB) + '" x2="' + f(X(o.est[0])) + '" y2="' + f(Y(o.est[1])) + '"/><line class="estl" x1="' + f(X(o.est[0])) + '" y1="' + f(Y(o.est[1])) + '" x2="' + ML + '" y2="' + f(Y(o.est[1])) + '"/>';
    pts.forEach(function (p, i) { g += '<circle class="pt' + (o.hl === i ? " hl" : "") + '" data-i="' + i + '" cx="' + f(X(p[0])) + '" cy="' + f(Y(p[1])) + '" r="' + (o.rad || 4.5) + '"/>'; });
    if (o.means && S) g += '<circle class="cg" cx="' + f(X(S.mx)) + '" cy="' + f(Y(S.my)) + '" r="5.5"/>';
    if (o.est && o.est[1] >= yr[0] && o.est[1] <= yr[1]) g += '<circle class="est" cx="' + f(X(o.est[0])) + '" cy="' + f(Y(o.est[1])) + '" r="6"/>';
    return { svg: '<svg class="sgraf nv" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="núvol de punts">' + g + "</svg>", inner: g, W: W, H: H,
      inv: function (px, py) { return [xr[0] + (px - ML) / (W - ML - MR) * (xr[1] - xr[0]), yr[0] + (H - MB - py) / (H - MT - MB) * (yr[1] - yr[0])]; },
      inside: function (px, py) { return px >= ML && px <= W - MR && py >= MT && py <= H - MB; } };
  }
  /* núvol de n punts (escala 0-10) amb coeficient de correlació exactament r */
  function rng(seed) { var s = seed >>> 0 || 1; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  function normals(n, rand) { var out = []; while (out.length < n) { var a = rand() || 1e-9, b = rand(); out.push(Math.sqrt(-2 * Math.log(a)) * Math.cos(2 * Math.PI * b)); } return out; }
  function stdz(a) { var n = a.length, m = sum(a) / n, s2 = sum(a.map(function (v) { return (v - m) * (v - m); })) / n; return a.map(function (v) { return (v - m) / Math.sqrt(s2); }); }
  function cloudR(n, r, seed, k) {
    var rand = rng(seed), z1 = stdz(normals(n, rand)), z2 = normals(n, rand);
    var d = sum(z1.map(function (v, i) { return v * z2[i]; })) / n; z2 = stdz(z2.map(function (v, i) { return v - d * z1[i]; }));
    k = k || 1.5;
    return z1.map(function (a, i) { return [5 + k * a, 5 + k * (r * a + Math.sqrt(Math.max(0, 1 - r * r)) * z2[i])]; })
      .filter(function (p) { return p[0] >= 0 && p[0] <= 10 && p[1] >= 0 && p[1] <= 10; });
  }
  /* parelles escrites en dos camps x i y */
  function pairsIn(I) {
    var x = numsIn(I.x.value), y = numsIn(I.y.value);
    if (!x || !y || x.length < 2) return { err: T(L3("Escriu almenys dues dades en X i en Y, separades per espais.", "Escribe al menos dos datos en X y en Y, separados por espacios.", "Type at least two values in X and in Y, separated by spaces.")) };
    if (x.length !== y.length) return { err: fill(T(L3("Hi ha {a} dades en X i {b} en Y: n'hi ha d'haver les mateixes.", "Hay {a} datos en X y {b} en Y: tiene que haber los mismos.", "There are {a} values in X and {b} in Y: there must be the same number.")), { a: x.length, b: y.length }) };
    if (x.length > 40) return { err: T(L3("Com a molt 40 parelles.", "Como mucho 40 parejas.", "At most 40 pairs.")) };
    return { x: x, y: y };
  }
  /* conjunts de dades dels apunts */
  var HX = [1, 2, 2, 3, 3, 4, 5, 5, 6, 7], HY = [3, 3, 5, 4, 6, 6, 7, 8, 8, 9];
  var EX = [1, 2, 3, 4, 5], EY = [2, 3, 5, 4, 6], PX = [1, 2, 3, 4, 5], PY = [50, 44, 40, 32, 24];
  var GX = [14, 18, 20, 23, 25, 28, 30, 32], GY = [20, 35, 40, 60, 65, 80, 95, 105];
  var DXa = [2, 3, 5, 6, 9], DYa = [8, 8, 6, 4, 2], QX = [1, 2, 4, 5, 8], QY = [3, 5, 4, 7, 6];
  var WX = [1, 2, 3, 4, 5, 6, 7, 8], WY = [4, 7, 2, 6, 3, 8, 4, 5];
  var PRE = { ex: [EX, EY], pr: [PX, PY], h10: [HX, HY], gel: [GX, GY], feb: [WX, WY], a: [HX, HY], b: [DXa, DYa], c: [QX, QY] };
  function lst(a) { return a.map(function (v) { return lang === "en" ? String(v) : String(v).replace(".", ","); }).join(" "); }
  /* botons de dades predefinides: en escriure, es passa a «les meues» */
  function presetPairs(w, I, cb) {
    var cur = w.querySelector('.seg button[aria-pressed="true"]'), pre = cur ? cur.dataset.k : "own";
    function put() { if (PRE[pre]) { I.x.value = lst(PRE[pre][0]); I.y.value = lst(PRE[pre][1]); } }
    segBind(w, function (k) { pre = k; put(); cb(); });
    [I.x, I.y].forEach(function (i) { i.addEventListener("input", function () { if (pre !== "own") { pre = "own"; setSeg(w, 0, "own"); } cb(); }); });
    put();
    return function () { put(); };
  }
  function axesOf(pre) {
    return { ex: [T(L3("hores", "horas", "hours")), T(L3("nota", "nota", "mark"))], h10: [T(L3("hores", "horas", "hours")), T(L3("nota", "nota", "mark"))],
      pr: ["€", T(L3("unitats", "unidades", "units"))], gel: ["°C", T(L3("gelats", "helados", "ice creams"))] }[pre] || ["X", "Y"];
  }

  /* ---------- 10.1 taula de doble entrada ---------- */
  function wDbl() {
    var w = document.getElementById("w-dbl"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".tout"), info = w.querySelector(".info");
    function paint() {
      var P = pairsIn(I); if (P.err) { out.innerHTML = ""; info.innerHTML = warn(P.err); return; }
      info.innerHTML = "";
      var ux = P.x.filter(function (v, i, a) { return a.indexOf(v) === i; }).sort(function (a, b) { return a - b; });
      var uy = P.y.filter(function (v, i, a) { return a.indexOf(v) === i; }).sort(function (a, b) { return a - b; });
      if (ux.length > 10 || uy.length > 10) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Massa valors diferents per a una taula de doble entrada (com a molt 10 en cada variable).", "Demasiados valores diferentes para una tabla de doble entrada (como mucho 10 en cada variable).", "Too many different values for a two-way table (at most 10 for each variable)."))); return; }
      var M_ = {}; P.x.forEach(function (a, i) { var k = a + "|" + P.y[i]; M_[k] = (M_[k] || 0) + 1; });
      var rows = ux.map(function (a) {
        var t = 0, r = [tex(nf(a))];
        uy.forEach(function (b) { var f = M_[a + "|" + b] || 0; t += f; r.push(tex(String(f))); });
        r.push(tex("\\mathbf{" + t + "}")); return r;
      });
      rows.push([tex("f_y")].concat(uy.map(function (b) { return tex("\\mathbf{" + P.y.filter(function (v) { return v === b; }).length + "}"); }), [tex("\\mathbf{" + P.x.length + "}")]));
      out.innerHTML = tbl(['<span class="dg">' + tex("X\\backslash Y") + "</span>"].concat(uy.map(function (b) { return tex(nf(b)); }), [tex("f_x")]), rows, "freq dbl")
        + '<p class="hint-s">' + fill(T(L3("{n} parelles. La darrera columna és la distribució de X i la darrera fila, la de Y.", "{n} parejas. La última columna es la distribución de X y la última fila, la de Y.", "{n} pairs. The last column is the distribution of X and the last row that of Y.")), { n: P.x.length }) + "</p>";
    }
    [I.x, I.y].forEach(function (i) { i.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 10.2 núvol de punts amb el centre de gravetat ---------- */
  function wCloud() {
    var w = document.getElementById("w-cloud"); if (!w) return;
    var box = w.querySelector(".cl-wrap"), info = w.querySelector(".info"), pts, G;
    function ex() { pts = HX.map(function (a, i) { return [a, HY[i]]; }); }
    ex();
    function paint() {
      G = cloud(pts, { xr: [0, 10, 1], yr: [0, 10, 1], means: true });
      box.innerHTML = G.svg;
      var svg = box.querySelector("svg");
      svg.addEventListener("click", function (ev) {
        var t = ev.target;
        if (t.classList && t.classList.contains("pt")) { pts.splice(+t.getAttribute("data-i"), 1); paint(); return; }
        var r = svg.getBoundingClientRect(), px = (ev.clientX - r.left) * G.W / r.width, py = (ev.clientY - r.top) * G.H / r.height;
        if (!G.inside(px, py) || pts.length >= 40) return;
        var q = G.inv(px, py); pts.push([Math.round(q[0] * 2) / 2, Math.round(q[1] * 2) / 2]); paint();
      });
      if (pts.length < 1) { info.innerHTML = T(L3("Toca el pla per a afegir punts.", "Toca el plano para añadir puntos.", "Tap the grid to add points.")); return; }
      var S = biOf(pts.map(function (p) { return p[0]; }), pts.map(function (p) { return p[1]; }));
      info.innerHTML = '<div class="hsteps">' + rows2html([
        tex("N=" + pts.length) + ". " + T(L3("Punts: ", "Puntos: ", "Points: ")) + tex(pts.map(function (p) { return "(" + nf(p[0]) + "," + nf(p[1]) + ")"; }).join(",\\ ")),
        tex("\\bar x=\\frac{" + nf(S.sx) + "}{" + S.N + "}" + eqr(S.mx) + "\\qquad \\bar y=\\frac{" + nf(S.sy) + "}{" + S.N + "}" + eqr(S.my)),
        "<b>" + T(L3("Centre de gravetat", "Centro de gravedad", "Centre of gravity")) + "</b>: " + tex("(" + nf(r2(S.mx)) + ",\\ " + nf(r2(S.my)) + ")")]) + "</div>";
    }
    w.querySelector('[data-a="ex"]').addEventListener("click", function () { ex(); paint(); });
    w.querySelector('[data-a="clear"]').addEventListener("click", function () { pts = []; paint(); });
    onLang(paint);
  }

  /* ---------- 10.3 el núvol segons la correlació ---------- */
  function wSlide() {
    var w = document.getElementById("w-slide"); if (!w) return;
    var S = sliders(w), box = w.querySelector(".cl-wrap"), info = w.querySelector(".info");
    function paint() {
      var r = +S.r.value;
      showRv(w, "r", "r", r);
      box.innerHTML = cloud(cloudR(40, r, 7, 1.6), { xr: [0, 10, 1], yr: [0, 10, 1], rad: 3.8 }).svg;
      info.innerHTML = corrTxt(r) + (Math.abs(r) > 0.9999 ? "" : ". " + T(Math.abs(r) >= 0.8 ? L3("Els punts estan molt a prop d'una recta.", "Los puntos están muy cerca de una recta.", "The points are very close to a line.") : Math.abs(r) >= 0.5 ? L3("Es veu la tendència, però els punts estan escampats.", "Se ve la tendencia, pero los puntos están dispersos.", "The trend is visible, but the points are scattered.") : L3("Costa veure-hi cap tendència.", "Cuesta ver alguna tendencia.", "It's hard to see any trend.")))
        + '<p class="hint-s">' + T(L3("El nombre r és el coeficient de correlació, que aprendràs a calcular en l'apartat 10.4.", "El número r es el coeficiente de correlación, que aprenderás a calcular en el apartado 10.4.", "The number r is the correlation coefficient, which you'll learn to calculate in section 10.4.")) + "</p>";
    }
    S.r.addEventListener("input", paint); onLang(paint);
  }

  /* ---------- 10.4 coeficient de correlació pas a pas ---------- */
  function stepsCov(P) {
    var S = biOf(P.x, P.y), N = S.N, rows = P.x.map(function (a, i) { var b = P.y[i]; return [tex(nf(a)), tex(nf(b)), tex(nf(a * a)), tex(nf(b * b)), tex(nf(a * b))]; });
    rows.push([tex("\\textstyle\\sum=" + nf(S.sx)), tex("\\textstyle\\sum=" + nf(S.sy)), tex("\\textstyle\\sum=" + nf(S.sx2)), tex("\\textstyle\\sum=" + nf(S.sy2)), tex("\\textstyle\\sum=" + nf(S.sxy))]);
    var st = [
      "<b>" + T(L3("Mitjanes", "Medias", "Means")) + "</b>: " + tex("\\bar x=\\frac{" + nf(S.sx) + "}{" + N + "}" + eqr(S.mx) + "\\qquad\\bar y=\\frac{" + nf(S.sy) + "}{" + N + "}" + eqr(S.my)),
      "<b>" + T(L3("Desviacions típiques", "Desviaciones típicas", "Standard deviations")) + "</b>: " + tex("\\sigma_x=\\sqrt{\\frac{" + nf(S.sx2) + "}{" + N + "}-" + nfp(r2(S.mx)) + "^2}" + eqr(Math.sqrt(S.vx)) + "\\qquad\\sigma_y=\\sqrt{\\frac{" + nf(S.sy2) + "}{" + N + "}-" + nfp(r2(S.my)) + "^2}" + eqr(Math.sqrt(S.vy))),
      "<b>" + T(L3("Covariància", "Covarianza", "Covariance")) + "</b>: " + tex("\\sigma_{xy}=\\frac{" + nf(S.sxy) + "}{" + N + "}-" + nfp(r2(S.mx)) + "\\cdot " + nfp(r2(S.my)) + eqr(S.c))
    ];
    if (isFinite(S.r)) st.push("<b>" + T(L3("Coeficient de correlació", "Coeficiente de correlación", "Correlation coefficient")) + "</b>: " + tex("r=\\frac{\\sigma_{xy}}{\\sigma_x\\cdot\\sigma_y}=\\frac{" + nf(r2(S.c)) + "}{" + nf(r2(Math.sqrt(S.vx))) + "\\cdot " + nf(r2(Math.sqrt(S.vy))) + "}" + eqr(S.r)));
    st.push(corrTxt(S.r));
    return { S: S, html: tbl([tex("x_i"), tex("y_i"), tex("x_i^2"), tex("y_i^2"), tex("x_i\\cdot y_i")], rows, "freq") + '<div class="hsteps">' + rows2html(st) + "</div>" };
  }
  function wCov() {
    var w = document.getElementById("w-cov"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".tout"), info = w.querySelector(".info");
    function paint() {
      var P = pairsIn(I); if (P.err) { out.innerHTML = ""; info.innerHTML = warn(P.err); return; }
      info.innerHTML = "";
      var K = stepsCov(P), pre = w.querySelector('.seg button[aria-pressed="true"]');
      out.innerHTML = K.html + cloud(P.x.map(function (a, i) { return [a, P.y[i]]; }), { means: true, axes: axesOf(pre && pre.dataset.k) }).svg
        + '<p class="hint-s">' + T(L3("Els passos intermedis estan arrodonits, però els resultats es calculen amb tots els decimals.", "Los pasos intermedios están redondeados, pero los resultados se calculan con todos los decimales.", "Intermediate steps are rounded, but the results are computed with all the decimals.")) + "</p>";
    }
    var relang = presetPairs(w, I, paint);
    onLang(function () { relang(); paint(); });
  }
  function wGuess() {
    var w = document.getElementById("w-guess"); if (!w) return;
    var box = w.querySelector(".cl-wrap"), ob = w.querySelector(".gopts"), info = w.querySelector(".info"), sc = w.querySelector(".dscore");
    var OPTS = [-0.95, -0.7, -0.3, 0, 0.3, 0.7, 0.95], seed = 11, cur = 0.7, ok = 0, tot = 0, done = null;
    function fresh() { seed = (seed * 7 + 13) % 100003; cur = pick(OPTS); done = null; paint(); }
    function paint() {
      box.innerHTML = cloud(cloudR(30, cur, seed), { xr: [0, 10, 2], yr: [0, 10, 2], rad: 3.8 }).svg;
      ob.innerHTML = "";
      OPTS.forEach(function (o) {
        var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.innerHTML = tex("r=" + nf(o));
        if (done !== null) { b.disabled = true; if (o === cur) b.classList.add("right"); else if (o === done) b.classList.add("wrong"); }
        b.addEventListener("click", function () { if (done !== null) return; done = o; tot++; if (o === cur) ok++; paint(); });
        ob.appendChild(b);
      });
      sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      info.innerHTML = done === null ? "" : (done === cur ? '<span class="ok">✓ ' + u("right") + "</span> " : '<span class="ko">✗ ' + u("wrong") + "</span> ") + fill(T(L3("El núvol té {r}: correlació {w}.", "La nube tiene {r}: correlación {w}.", "The cloud has {r}: {w} correlation.")), { r: tex("r=" + nf(cur)), w: rWords(cur) });
    }
    w.querySelector('[data-a="new"]').addEventListener("click", fresh);
    onLang(paint);
  }

  /* ---------- 10.5 recta a ull i recta de regressió ---------- */
  function sse(xs, ys, m, n) { return sum(xs.map(function (x, i) { var e = ys[i] - (m * x + n); return e * e; })); }
  function wEye() {
    var w = document.getElementById("w-eye"); if (!w) return;
    var S = sliders(w), box = w.querySelector(".cl-wrap"), info = w.querySelector(".info"), pre = "a", show = false;
    segBind(w, function (k) { pre = k; show = false; paint(); });
    function paint() {
      var d = PRE[pre], m = +S.m.value, n = +S.n.value, B = biOf(d[0], d[1]), R = rlOf(B);
      showRv(w, "m", "m", m); showRv(w, "n", "n", n);
      var pts = d[0].map(function (a, i) { return [a, d[1][i]]; });
      box.innerHTML = cloud(pts, { xr: [0, 10, 1], yr: [0, 10, 1], means: true, line: [m, n], res: true, reg: show }).svg;
      var e1 = sse(d[0], d[1], m, n), e0 = sse(d[0], d[1], R.m, R.n), ratio = e0 > 0 ? e1 / e0 : 1;
      var verdict = ratio < 1.1 ? L3("Molt bé! La teua recta és quasi tan bona com la de regressió.", "¡Muy bien! Tu recta es casi tan buena como la de regresión.", "Great! Your line is almost as good as the regression line.")
        : ratio < 2 ? L3("No està malament. Prova d'acostar-la més als punts.", "No está mal. Prueba a acercarla más a los puntos.", "Not bad. Try to bring it closer to the points.")
        : L3("Encara està lluny. Fes que passe pel centre de gravetat i que seguisca el núvol.", "Todavía está lejos. Haz que pase por el centro de gravedad y que siga la nube.", "Still far off. Make it pass through the centre of gravity and follow the cloud.");
      info.innerHTML = '<div class="hsteps">' + rows2html([
        T(L3("La teua recta", "Tu recta", "Your line")) + ": " + tex(lineTex(m, n)) + ". " + T(L3("Suma dels quadrats dels errors", "Suma de los cuadrados de los errores", "Sum of squared errors")) + ": " + tex(nf(r2(e1))),
        show ? T(L3("Recta de regressió", "Recta de regresión", "Regression line")) + ": " + tex(lineTex(R.m, R.n)) + ". " + T(L3("Suma dels quadrats dels errors", "Suma de los cuadrados de los errores", "Sum of squared errors")) + ": " + tex(nf(r2(e0))) + " " + T(L3("(la més xicoteta possible)", "(la más pequeña posible)", "(the smallest possible)")) : T(L3("El centre de gravetat és ", "El centro de gravedad es ", "The centre of gravity is ")) + tex("(" + nf(r2(B.mx)) + ",\\ " + nf(r2(B.my)) + ")"),
        T(verdict)]) + "</div>";
    }
    w.querySelector('[data-a="show"]').addEventListener("click", function () { show = !show; paint(); });
    S.m.addEventListener("input", paint); S.n.addEventListener("input", paint);
    onLang(paint);
  }
  function stepsReg(S) {
    var R = rlOf(S), mx = r2(S.mx), my = r2(S.my);
    return [
      tex("\\bar x" + eqr(S.mx) + "\\qquad \\bar y" + eqr(S.my) + "\\qquad \\sigma_x^2" + eqr(S.vx) + "\\qquad \\sigma_{xy}" + eqr(S.c)),
      "<b>" + T(L3("Pendent", "Pendiente", "Gradient")) + "</b>: " + tex("m=\\frac{\\sigma_{xy}}{\\sigma_x^2}=\\frac{" + nf(r2(S.c)) + "}{" + nf(r2(S.vx)) + "}" + eqr(R.m)),
      "<b>" + T(L3("Recta", "Recta", "Line")) + "</b>: " + tex("y" + sg(-my) + "=" + nf(r2(R.m)) + "\\,(x" + sg(-mx) + ")\\ \\Rightarrow\\ \\boxed{" + lineTex(R.m, R.n) + "}"),
      tex("r" + eqr(S.r)) + ": " + corrTxt(S.r)
    ];
  }
  function wReg() {
    var w = document.getElementById("w-reg"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".tout"), info = w.querySelector(".info");
    function paint() {
      var P = pairsIn(I); if (P.err) { out.innerHTML = ""; info.innerHTML = warn(P.err); return; }
      var S = biOf(P.x, P.y);
      if (!(S.vx > 0)) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Totes les x són iguals: no hi ha recta de regressió.", "Todas las x son iguales: no hay recta de regresión.", "All the x values are equal: there's no regression line."))); return; }
      info.innerHTML = "";
      var pre = w.querySelector('.seg button[aria-pressed="true"]');
      out.innerHTML = '<div class="hsteps">' + rows2html(stepsReg(S)) + "</div>" + cloud(P.x.map(function (a, i) { return [a, P.y[i]]; }), { means: true, reg: true, axes: axesOf(pre && pre.dataset.k) }).svg;
    }
    var relang = presetPairs(w, I, paint);
    onLang(function () { relang(); paint(); });
  }

  /* ---------- 10.6 estimacions ---------- */
  var EST_R = { ex: [0, 12, 0.1, 3.5], gel: [5, 45, 0.5, 27], feb: [0, 12, 0.1, 4.5] };
  function verdictOf(r, x0, xs) {
    var a = Math.min.apply(null, xs), b = Math.max.apply(null, xs), span = b - a, out = x0 < a || x0 > b, far = x0 < a - 0.2 * span || x0 > b + 0.2 * span;
    if (Math.abs(r) < 0.5) return { k: 0, t: L3("No és fiable: la correlació és feble.", "No es fiable: la correlación es débil.", "Not reliable: the correlation is weak.") };
    if (far) return { k: 0, t: L3("No és fiable: x₀ està molt lluny de les dades (extrapolació).", "No es fiable: x₀ está muy lejos de los datos (extrapolación).", "Not reliable: x₀ is far from the data (extrapolation).") };
    if (out) return { k: 1, t: L3("Poc fiable: x₀ està fora de les dades, encara que a prop (extrapolació).", "Poco fiable: x₀ está fuera de los datos, aunque cerca (extrapolación).", "Not very reliable: x₀ is outside the data, although close (extrapolation).") };
    if (Math.abs(r) < 0.8) return { k: 1, t: L3("Aproximada: x₀ està dins de les dades, però la correlació només és moderada.", "Aproximada: x₀ está dentro de los datos, pero la correlación solo es moderada.", "Rough: x₀ is inside the data, but the correlation is only moderate.") };
    return { k: 2, t: L3("Fiable: la correlació és forta i x₀ està dins de les dades (interpolació).", "Fiable: la correlación es fuerte y x₀ está dentro de los datos (interpolación).", "Reliable: the correlation is strong and x₀ is inside the data (interpolation).") };
  }
  function wEst() {
    var w = document.getElementById("w-est"); if (!w) return;
    var S = sliders(w), out = w.querySelector(".tout"), info = w.querySelector(".info"), pre = "ex";
    function setR() { var c = EST_R[pre]; S.x0.min = c[0]; S.x0.max = c[1]; S.x0.step = c[2]; S.x0.value = c[3]; }
    segBind(w, function (k) { pre = k; setR(); paint(); });
    function paint() {
      var d = PRE[pre], x0 = +S.x0.value, B = biOf(d[0], d[1]), R = rlOf(B), y0 = R.m * x0 + R.n, V = verdictOf(B.r, x0, d[0]);
      showRv(w, "x0", "x_0", x0);
      var c = EST_R[pre];
      out.innerHTML = '<div class="hsteps">' + rows2html([
        T(L3("Recta de regressió", "Recta de regresión", "Regression line")) + ": " + tex(lineTex(R.m, R.n)) + ", " + tex("r" + eqr(B.r)) + ". " + fill(T(L3("Dades de x: de {a} a {b}.", "Datos de x: de {a} a {b}.", "x data: from {a} to {b}.")), { a: tex(nf(Math.min.apply(null, d[0]))), b: tex(nf(Math.max.apply(null, d[0]))) }),
        "<b>" + T(L3("Estimació", "Estimación", "Estimate")) + "</b>: " + tex("\\hat y=" + nf(r2(R.m)) + "\\cdot " + nfp(x0) + sg(r2(R.n)) + eqr(y0)),
        '<b class="' + (V.k === 2 ? "ok" : V.k === 1 ? "" : "ko") + '">' + T(V.t) + "</b>"]) + "</div>"
        + cloud(d[0].map(function (a, i) { return [a, d[1][i]]; }), { reg: true, est: [x0, y0], xr: autoR(d[0].concat([c[0], c[1]])), axes: axesOf(pre) }).svg;
      info.innerHTML = "";
    }
    S.x0.addEventListener("input", paint);
    setR(); onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function optsTxt(right, wrongs) {
    var all = [right].concat(wrongs), order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return all[i]; }), ans: order.indexOf(0) };
  }
  function ret(o, q, s) { o.q = q; o.s = s; return o; }
  function numQ(v, tol) { return { num: v, tol: tol || 1e-6 }; }
  function $(s) { return "$" + s + "$"; }
  function rlist(n, a, b) { var o = []; for (var i = 0; i < n; i++) o.push(rint(a, b)); return o; }
  var RELO = [L3("Funcional", "Funcional", "Functional"), L3("Estadística", "Estadística", "Statistical"), L3("Cap relació", "Ninguna relación", "No relationship")];
  var RELS = [
    [L3("El costat d'un quadrat i la seua àrea.", "El lado de un cuadrado y su área.", "The side of a square and its area."), 0],
    [L3("Els litres de gasolina que posem i el preu que paguem.", "Los litros de gasolina que echamos y el precio que pagamos.", "The litres of petrol we buy and the price we pay."), 0],
    [L3("El radi d'una circumferència i la seua longitud.", "El radio de una circunferencia y su longitud.", "The radius of a circle and its circumference."), 0],
    [L3("Les hores que treballa una persona que cobra 12 € l'hora i el que guanya.", "Las horas que trabaja una persona que cobra 12 € la hora y lo que gana.", "The hours worked by someone paid €12 an hour and what they earn."), 0],
    [L3("L'alçada i el pes de les persones.", "La altura y el peso de las personas.", "People's height and weight."), 1],
    [L3("Les hores d'estudi i la nota d'un examen.", "Las horas de estudio y la nota de un examen.", "Hours of study and a test mark."), 1],
    [L3("La temperatura i els gelats venuts.", "La temperatura y los helados vendidos.", "Temperature and ice creams sold."), 1],
    [L3("L'edat d'un cotxe i el seu preu de segona mà.", "La edad de un coche y su precio de segunda mano.", "The age of a car and its second-hand price."), 1],
    [L3("Les hores d'entrenament i el temps en una cursa.", "Las horas de entrenamiento y el tiempo en una carrera.", "Hours of training and the time in a race."), 1],
    [L3("El número de calçat i la nota de matemàtiques.", "El número de calzado y la nota de matemáticas.", "Shoe size and maths mark."), 2],
    [L3("El mes de naixement i l'alçada.", "El mes de nacimiento y la altura.", "Month of birth and height."), 2],
    [L3("L'última xifra del telèfon i el nombre de germans.", "La última cifra del teléfono y el número de hermanos.", "The last digit of your phone number and your number of siblings."), 2]
  ];
  var TIPO = [L3("Positiva i forta", "Positiva y fuerte", "Strong positive"), L3("Positiva i feble", "Positiva y débil", "Weak positive"), L3("Nul·la", "Nula", "Zero"), L3("Negativa i feble", "Negativa y débil", "Weak negative"), L3("Negativa i forta", "Negativa y fuerte", "Strong negative")];
  var TIPR = [0.93, 0.55, 0.03, -0.55, -0.93];
  var SENO = [L3("Positiva", "Positiva", "Positive"), L3("Negativa", "Negativa", "Negative"), L3("Nul·la", "Nula", "Zero")];
  var SENS = [
    [L3("Temperatura i consum d'aigua.", "Temperatura y consumo de agua.", "Temperature and water use."), 0],
    [L3("Alçada d'una persona i llargària del seu peu.", "Altura de una persona y longitud de su pie.", "A person's height and the length of their foot."), 0],
    [L3("Hores d'entrenament i gols marcats en la temporada.", "Horas de entrenamiento y goles marcados en la temporada.", "Hours of training and goals scored in the season."), 0],
    [L3("Quilòmetres recorreguts i gasolina gastada.", "Kilómetros recorridos y gasolina gastada.", "Kilometres driven and petrol used."), 0],
    [L3("Preu d'un producte i unitats venudes.", "Precio de un producto y unidades vendidas.", "The price of a product and units sold."), 1],
    [L3("Altitud d'una muntanya i temperatura al cim.", "Altitud de una montaña y temperatura en la cima.", "The altitude of a mountain and the temperature at the top."), 1],
    [L3("Hores davant de pantalles i hores de son.", "Horas delante de pantallas y horas de sueño.", "Screen time and hours of sleep."), 1],
    [L3("Edat d'un cotxe i el seu preu.", "Edad de un coche y su precio.", "The age of a car and its price."), 1],
    [L3("Nombre de faltes d'ortografia i nota d'una redacció.", "Número de faltas de ortografía y nota de una redacción.", "Number of spelling mistakes and the mark for an essay."), 1],
    [L3("Número del DNI i nota de matemàtiques.", "Número del DNI y nota de matemáticas.", "ID-card number and maths mark."), 2],
    [L3("Dia de naixement i pes.", "Día de nacimiento y peso.", "Day of birth and weight."), 2]
  ];
  var RINT = [L3("Positiva i forta", "Positiva y fuerte", "Strong positive"), L3("Positiva moderada", "Positiva moderada", "Moderate positive"), L3("Positiva i feble", "Positiva y débil", "Weak positive"),
    L3("Negativa i forta", "Negativa y fuerte", "Strong negative"), L3("Negativa moderada", "Negativa moderada", "Moderate negative"), L3("Negativa i feble", "Negativa y débil", "Weak negative"), L3("Pràcticament nul·la", "Prácticamente nula", "Practically zero")];
  function rintClass(r) { var a = Math.abs(r); if (a < 0.1) return 6; return (r > 0 ? 0 : 3) + (a >= 0.8 ? 0 : a >= 0.5 ? 1 : 2); }
  function cleanSet(n, lo, hi) {
    for (var t = 0; t < 300; t++) {
      var x = rlist(n, lo, hi), y = rlist(n, lo, hi);
      if (sum(x) % n === 0 && sum(y) % n === 0 && x.some(function (v) { return v !== x[0]; })) return [x, y];
    }
    return [[1, 2, 3, 4, 5], [2, 3, 5, 4, 6]];
  }
  var GEN = {
    rel: function () {
      var v = pick(RELS);
      return ret({ opts: RELO, ans: v[1] }, function () { return T(v[0]); },
        function () { return T([L3("Hi ha una fórmula que dona exactament una variable a partir de l'altra.", "Hay una fórmula que da exactamente una variable a partir de la otra.", "There's a formula that gives one variable exactly from the other."), L3("Hi ha una tendència, però no una fórmula exacta.", "Hay una tendencia, pero no una fórmula exacta.", "There's a trend, but no exact formula."), L3("Una variable no ens diu res de l'altra.", "Una variable no nos dice nada de la otra.", "One variable tells us nothing about the other.")][v[1]]); });
    },
    cg: function () {
      var n = rint(4, 5), d = cleanSet(n, 0, 12), S = biOf(d[0], d[1]);
      var pts = d[0].map(function (a, i) { return "(" + a + "," + d[1][i] + ")"; }).join(",\\ ");
      return ret({ pair: [S.mx, S.my] }, function () { return fill(T(L3("Calcula el centre de gravetat de {p}.", "Calcula el centro de gravedad de {p}.", "Find the centre of gravity of {p}.")), { p: $(pts) }); },
        function () { return tex("\\bar x=\\frac{" + d[0].join("+") + "}{" + n + "}=" + nf(S.mx) + ",\\quad \\bar y=\\frac{" + d[1].join("+") + "}{" + n + "}=" + nf(S.my)) + " → " + tex("(" + nf(S.mx) + ",\\ " + nf(S.my) + ")"); });
    },
    tipus: function () {
      var k = rint(0, 4), seed = rint(1, 99999);
      return ret({ opts: TIPO, ans: k }, function () { return T(L3("Com és la correlació d'aquest núvol?", "¿Cómo es la correlación de esta nube?", "What is the correlation in this cloud like?")) + cloud(cloudR(30, TIPR[k], seed), { xr: [0, 10, 2], yr: [0, 10, 2], rad: 3.6, W: 280, H: 210 }).svg; },
        function () { return fill(T(L3("El núvol té {r}: correlació {w}.", "La nube tiene {r}: correlación {w}.", "The cloud has {r}: {w} correlation.")), { r: tex("r=" + nf(TIPR[k])), w: T(TIPO[k]).toLowerCase() }); });
    },
    sentit: function () {
      var v = pick(SENS);
      return ret({ opts: SENO, ans: v[1] }, function () { return T(v[0]); },
        function () { return T([L3("Quan una creix, l'altra també tendeix a créixer.", "Cuando una crece, la otra también tiende a crecer.", "When one increases, the other tends to increase too."), L3("Quan una creix, l'altra tendeix a decréixer.", "Cuando una crece, la otra tiende a decrecer.", "When one increases, the other tends to decrease."), L3("Les variables no tenen relació.", "Las variables no tienen relación.", "The variables aren't related.")][v[1]]); });
    },
    cov: function () {
      var n = rint(4, 6), d = cleanSet(n, 1, 10), S = biOf(d[0], d[1]);
      return ret(numQ(r2(S.c), 0.006), function () { return fill(T(L3("Una distribució té {n}, {sxy}, {mx} i {my}. Calcula la covariància (arrodoneix a les centèsimes si cal).", "Una distribución tiene {n}, {sxy}, {mx} y {my}. Calcula la covarianza (redondea a las centésimas si hace falta).", "A distribution has {n}, {sxy}, {mx} and {my}. Find the covariance (round to hundredths if needed).")), { n: $("N=" + n), sxy: $("\\sum x_iy_i=" + S.sxy), mx: $("\\bar x=" + nf(S.mx)), my: $("\\bar y=" + nf(S.my)) }); },
        function () { return tex("\\sigma_{xy}=\\frac{" + S.sxy + "}{" + n + "}-" + nfp(S.mx) + "\\cdot " + nfp(S.my) + eqr(S.sxy / n) + "-" + nf(S.mx * S.my) + eqr(S.c)); });
    },
    rcalc: function () {
      var sx = pick([1, 1.5, 2, 2.5, 3, 4, 5]), sy = pick([1, 2, 3, 4, 5, 6, 8]), rr = rint(-95, 95) / 100, c = Math.round(rr * sx * sy * 10) / 10;
      if (c === 0) c = 0.5; var r = c / (sx * sy);
      if (Math.abs(r) > 1) { c = Math.round(0.9 * sx * sy * 10) / 10 * (c < 0 ? -1 : 1); r = c / (sx * sy); }
      return ret(numQ(r2(r), 0.006), function () { return fill(T(L3("Sabem que {c}, {sx} i {sy}. Calcula el coeficient de correlació (arrodoneix a les centèsimes).", "Sabemos que {c}, {sx} y {sy}. Calcula el coeficiente de correlación (redondea a las centésimas).", "We know that {c}, {sx} and {sy}. Find the correlation coefficient (round to hundredths).")), { c: $("\\sigma_{xy}=" + nf(c)), sx: $("\\sigma_x=" + nf(sx)), sy: $("\\sigma_y=" + nf(sy)) }); },
        function () { return tex("r=\\frac{" + nf(c) + "}{" + nf(sx) + "\\cdot " + nf(sy) + "}=\\frac{" + nf(c) + "}{" + nf(sx * sy) + "}" + eqr(r)) + ": " + rWords(r); });
    },
    rint: function () {
      var r = pick([1, -1]) * pick([0.97, 0.91, 0.86, 0.82, 0.75, 0.66, 0.58, 0.52, 0.42, 0.33, 0.24, 0.05]), k = rintClass(r);
      var wr = shuffle([0, 1, 2, 3, 4, 5, 6].filter(function (i) { return i !== k; })).slice(0, 3);
      var o = optsTxt(RINT[k], wr.map(function (i) { return RINT[i]; }));
      return ret({ opts: o.opts, ans: o.ans }, function () { return fill(T(L3("Entre dues variables s'ha obtingut {r}. Com és la correlació?", "Entre dos variables se ha obtenido {r}. ¿Cómo es la correlación?", "Two variables gave {r}. What is the correlation like?")), { r: $("r=" + nf(r)) }); },
        function () { return T(L3("El signe diu el sentit i |r|, la força: ", "El signo dice el sentido y |r|, la fuerza: ", "The sign gives the direction and |r| the strength: ")) + T(RINT[k]).toLowerCase() + "."; });
    },
    recta: function () {
      var vx = pick([2, 4, 5, 8, 10]), m = rnz(-15, 15) / 5, c = m * vx, mx = rint(1, 9), my = rint(2, 20), n = my - m * mx, md = rint(0, 1);
      return ret(numQ(md ? r2(n) : r2(m), 0.006), function () { return fill(T(md ? L3("Amb {mx}, {my}, {vx} i {c}, quina és l'ordenada en l'origen n de la recta de regressió y = mx + n?", "Con {mx}, {my}, {vx} y {c}, ¿cuál es la ordenada en el origen n de la recta de regresión y = mx + n?", "With {mx}, {my}, {vx} and {c}, what is the y-intercept n of the regression line y = mx + n?")
          : L3("Amb {mx}, {my}, {vx} i {c}, quin és el pendent m de la recta de regressió?", "Con {mx}, {my}, {vx} y {c}, ¿cuál es la pendiente m de la recta de regresión?", "With {mx}, {my}, {vx} and {c}, what is the gradient m of the regression line?")),
          { mx: $("\\bar x=" + mx), my: $("\\bar y=" + my), vx: $("\\sigma_x^2=" + vx), c: $("\\sigma_{xy}=" + nf(c)) }); },
        function () { return tex("m=\\frac{" + nf(c) + "}{" + vx + "}=" + nf(m)) + "; " + tex("y-" + my + "=" + nf(m) + "\\,(x-" + mx + ")\\ \\Rightarrow\\ " + lineTex(m, n)); });
    },
    est: function () {
      var m = rnz(-30, 30) / 10, n = rint(-20, 60) / 2, x0 = rint(2, 30) / 2, y0 = m * x0 + n;
      return ret(numQ(r2(y0), 0.006), function () { return fill(T(L3("La recta de regressió és {l}. Estima el valor de y per a {x}.", "La recta de regresión es {l}. Estima el valor de y para {x}.", "The regression line is {l}. Estimate the value of y for {x}.")), { l: $(lineTex(m, n)), x: $("x=" + nf(x0)) }); },
        function () { return tex("\\hat y=" + nf(m) + "\\cdot " + nfp(x0) + sg(n) + eqr(y0)); });
    },
    fiab: function () {
      var c = rint(0, 2), a = rint(1, 5) * 2, b = a + rint(3, 8) * 2, r, x0;
      if (c === 0) { r = pick([1, -1]) * pick([0.86, 0.91, 0.95, 0.98]); x0 = rint(a + 1, b - 1); }
      else if (c === 1) { r = pick([1, -1]) * pick([0.12, 0.25, 0.31, 0.38, 0.44]); x0 = rint(a + 1, b - 1); }
      else { r = pick([1, -1]) * pick([0.86, 0.91, 0.95, 0.98]); x0 = b + rint(4, 10) * (b - a) / 2; }
      var O = [L3("Sí, és fiable", "Sí, es fiable", "Yes, it's reliable"), L3("No: la correlació és feble", "No: la correlación es débil", "No: the correlation is weak"), L3("No: és massa lluny de les dades", "No: está demasiado lejos de los datos", "No: it's too far from the data")];
      return ret({ opts: O, ans: c }, function () { return fill(T(L3("Tenim {r} i les dades de x van de {a} a {b}. És fiable estimar y per a {x}?", "Tenemos {r} y los datos de x van de {a} a {b}. ¿Es fiable estimar y para {x}?", "We have {r} and the x data go from {a} to {b}. Is it reliable to estimate y for {x}?")), { r: $("r=" + nf(r)), a: $(String(a)), b: $(String(b)), x: $("x=" + nf(x0)) }); },
        function () { return T([L3("|r| és pròxim a 1 i x està dins de les dades.", "|r| está cerca de 1 y x está dentro de los datos.", "|r| is close to 1 and x is inside the data."), L3("|r| és menor que 0,5: la recta no representa bé les dades.", "|r| es menor que 0,5: la recta no representa bien los datos.", "|r| is less than 0.5: the line doesn't represent the data well."), L3("Encara que r és alt, x està molt fora de l'interval de les dades (extrapolació).", "Aunque r es alto, x está muy fuera del intervalo de los datos (extrapolación).", "Although r is high, x is far outside the range of the data (extrapolation).")][c]); });
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
        if (q.pair) {
          var pv = pairIn(inp.value); if (pv === null) { info.innerHTML = warn(u("pair")); return; }
          good = Math.abs(pv[0] - q.pair[0]) < 0.006 && Math.abs(pv[1] - q.pair[1]) < 0.006;
        } else {
          var v = numIn(String(inp.value).replace("%", "")); if (v === null) { info.innerHTML = warn(u("num")); return; }
          good = Math.abs(v - q.num) <= (q.tol || 1e-6);
        }
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
  window.FM410 = { GEN: GEN, biOf: biOf, rlOf: rlOf, cloud: cloud, cloudR: cloudR, rWords: rWords, verdictOf: verdictOf, lineTex: lineTex };


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

  var TITLES = { va: "Estadística bidimensional · FentMates", es: "Estadística bidimensional · FentMates", en: "Bivariate Statistics · FentMates" };
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
    [wDbl, wCloud, wSlide, wCov, wGuess, wEye, wReg, wEst].forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(e); } });
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
