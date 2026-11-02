(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u7-done", NSEC = 9;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc",
      bad: "No entenc la fórmula. Escriu-la amb la x, per exemple: x^2-3x+1, 2x+5, 12/x o sqrt(x+4).",
      badx: "Escriu un valor de x (un nombre).", num: "Escriu un nombre (pots fer servir coma decimal o una fracció com 5/2).",
      pair: "Escriu el punt com (2, −3) o bé 2; −3.", sx: "Escriu l'angle com 12° 30' 15'' o bé 12 30 15.", sol: "Solució:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro",
      bad: "No entiendo la fórmula. Escríbela con la x, por ejemplo: x^2-3x+1, 2x+5, 12/x o sqrt(x+4).",
      badx: "Escribe un valor de x (un número).", num: "Escribe un número (puedes usar coma decimal o una fracción como 5/2).",
      pair: "Escribe el punto como (2, −3) o bien 2; −3.", sx: "Escribe el ángulo como 12° 30' 15'' o bien 12 30 15.", sol: "Solución:" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Score", right: "Correct!", wrong: "Not correct.", theme: "Switch between light and dark mode",
      bad: "I can't read the formula. Write it in x, for example: x^2-3x+1, 2x+5, 12/x or sqrt(x+4).",
      badx: "Type a value of x (a number).", num: "Type a number (decimals or a fraction like 5/2 are fine).",
      pair: "Type the point as (2, −3) or 2; −3.", sx: "Type the angle as 12° 30' 15'' or 12 30 15.", sol: "Solution:" }
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


  /* ======================================================================
     unitat 7 (1r ESO): geometria bàsica del pla
     ====================================================================== */
  function isInt(v) { return Math.abs(v - Math.round(v)) < 1e-9; }
  function d2(v) { return (Math.round(v * 100) / 100).toFixed(2).replace(".", "\\dc "); }
  function lab(v) { var s = String(Math.round(v * 100) / 100); return lang === "en" ? s : s.replace(".", ","); }
  function pol(C, r, a) { return [C[0] + r * Math.cos(a * Math.PI / 180), C[1] + r * Math.sin(a * Math.PI / 180)]; }
  function mid(A, B, f) { f = f == null ? 0.5 : f; return [A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f]; }
  function dist(A, B) { return Math.hypot(B[0] - A[0], B[1] - A[1]); }
  function dirn(V, P) { return Math.atan2(P[1] - V[1], P[0] - V[0]) * 180 / Math.PI; }
  function angAt(V, A, B) { var d = Math.abs(dirn(V, A) - dirn(V, B)) % 360; return Math.min(d, 360 - d); }
  /* arc ple de l'angle convex AVB */
  function amark(V, A, B, R, cls) {
    var a0 = dirn(V, A), a1 = dirn(V, B);
    if (((a1 - a0) % 360 + 360) % 360 > 180) { var t = a0; a0 = a1; a1 = t; }
    if (a1 < a0) a1 += 360;
    return ["sect", V, R || 0.4, a0, a1, cls || "af"];
  }
  function reg(n, r, rot) { r = r || 1; rot = rot == null ? -90 - 180 / n : rot; var V = []; for (var k = 0; k < n; k++) V.push(pol([0, 0], r, rot + 360 * k / n)); return V; }
  /* tros de la recta que passa per P amb direcció u dins del rectangle bx = [x0, y0, x1, y1] */
  function clipLine(P, u, bx) {
    var t0 = -Infinity, t1 = Infinity;
    [[u[0], P[0], bx[0], bx[2]], [u[1], P[1], bx[1], bx[3]]].forEach(function (c) {
      if (Math.abs(c[0]) < 1e-12) { if (c[1] < c[2] || c[1] > c[3]) { t0 = 1; t1 = 0; } return; }
      var a = (c[2] - c[1]) / c[0], b = (c[3] - c[1]) / c[0];
      t0 = Math.max(t0, Math.min(a, b)); t1 = Math.min(t1, Math.max(a, b));
    });
    return t0 > t1 ? null : [[P[0] + u[0] * t0, P[1] + u[1] * t0], [P[0] + u[0] * t1, P[1] + u[1] * t1]];
  }
  function inter(P, u, Q, v) { var d = u[0] * v[1] - u[1] * v[0]; if (Math.abs(d) < 1e-12) return null; var t = ((Q[0] - P[0]) * v[1] - (Q[1] - P[1]) * v[0]) / d; return [P[0] + u[0] * t, P[1] + u[1] * t]; }
  function deg(v) { return isInt(v) ? nf(Math.round(v)) + "^\\circ" : "\\approx " + d2(v) + "^\\circ"; }

  /* ---------- sistema sexagesimal (tot en segons) ---------- */
  function dmsOf(t) { t = Math.round(t); return [Math.floor(t / 3600), Math.floor(t % 3600 / 60), t % 60]; }
  function sxT(t) {
    var d = dmsOf(t), out = [];
    if (d[0] || (!d[1] && !d[2])) out.push(d[0] + "^\\circ");
    if (d[1]) out.push(d[1] + "'");
    if (d[2]) out.push(d[2] + "''");
    return out.join("\\,");
  }
  function sxIn(raw) {
    var s = String(raw).replace(/º/g, "°").replace(/[″"]/g, "''").replace(/[′´’]/g, "'").replace(/,/g, " ").trim();
    if (!s) return null;
    var re = /(\d+(?:\.\d+)?)\s*(°|''|')?/g, m, parts = [], rest = s.replace(re, "").replace(/\s+/g, "");
    if (rest) return null;
    while ((m = re.exec(s))) parts.push([parseFloat(m[1]), m[2] || ""]);
    if (!parts.length || parts.length > 3) return null;
    var unit = { "°": 3600, "'": 60, "''": 1 }, tot = 0, seq = [3600, 60, 1], used = {};
    var anyU = parts.some(function (p) { return p[1]; });
    for (var i = 0; i < parts.length; i++) {
      var f = anyU ? unit[parts[i][1]] : seq[i];
      if (!f || used[f]) return null; used[f] = 1; tot += parts[i][0] * f;
    }
    return tot;
  }
  function sxOk(raw) {
    /* forma complexa ben escrita: minuts i segons < 60 */
    var s = String(raw).replace(/º/g, "°").replace(/[″"]/g, "''").replace(/[′´’]/g, "'");
    var mm = s.match(/(\d+)\s*'(?!')/), ss = s.match(/(\d+)\s*''/);
    if (!/[°']/.test(s)) { var p = s.trim().split(/[\s,]+/); mm = p[1] ? [0, p[1]] : null; ss = p[2] ? [0, p[2]] : null; }
    return !(mm && +mm[1] >= 60) && !(ss && +ss[1] >= 60);
  }

  /* ---------- figures geomètriques (SVG) ----------
     ["poly", pts, cls] · ["seg", A, B, cls] · ["ln", A, B, cls, ends] (fletxa a B: "e", a tots dos: "b") · ["ra", V, A, B] · ["tick", A, B, n]
     ["txt", P, text, {dx, dy, a, cls}] · ["circ", C, r, cls] · ["sect", C, r, a0, a1, cls] · ["arc", C, r, a0, a1, cls] · ["dot", P, cls] */
  function G(items, o) {
    o = o || {}; var W = o.W || 300, pad = o.pad || 18, maxh = o.maxh || 260, xs = [], ys = [];
    items.forEach(function (it) {
      var k = it[0];
      if (k === "poly") it[1].forEach(function (p) { xs.push(p[0]); ys.push(p[1]); });
      else if (k === "seg" || k === "ln") { xs.push(it[1][0], it[2][0]); ys.push(it[1][1], it[2][1]); }
      else if (k === "circ") { xs.push(it[1][0] - it[2], it[1][0] + it[2]); ys.push(it[1][1] - it[2], it[1][1] + it[2]); }
      else if (k === "sect" || k === "arc") {
        for (var j = 0; j <= 40; j++) { var P = pol(it[1], it[2], it[3] + (it[4] - it[3]) * j / 40); xs.push(P[0]); ys.push(P[1]); }
        if (k === "sect") { xs.push(it[1][0]); ys.push(it[1][1]); }
      } else if (k === "dot" || k === "txt") { xs.push(it[1][0]); ys.push(it[1][1]); }
    });
    if (o.box) { xs.push(o.box[0], o.box[2]); ys.push(o.box[1], o.box[3]); }
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var s = Math.min((W - 2 * pad) / Math.max(x1 - x0, 1e-9), (maxh - 2 * pad) / Math.max(y1 - y0, 1e-9));
    var Wd = Math.round((x1 - x0) * s + 2 * pad), H = Math.round((y1 - y0) * s + 2 * pad);
    function X(v) { return +((v - x0) * s + pad).toFixed(1); }
    function Y(v) { return +(H - ((v - y0) * s + pad)).toFixed(1); }
    function pts(a) { return a.map(function (p) { return X(p[0]) + "," + Y(p[1]); }).join(" "); }
    function arcTo(C, r, a0, a1) { var B = pol(C, r, a1), big = ((a1 - a0) % 360 + 360) % 360 > 180 ? 1 : 0, rr = +(r * s).toFixed(1); return "A" + rr + " " + rr + " 0 " + big + " 0 " + X(B[0]) + " " + Y(B[1]); }
    function head(P0, P1, cls) {
      var ux = X(P1[0]) - X(P0[0]), uy = Y(P1[1]) - Y(P0[1]), n = Math.hypot(ux, uy) || 1, tx = X(P1[0]), ty = Y(P1[1]); ux /= n; uy /= n;
      return '<polygon class="gah ' + cls + '" points="' + tx + "," + ty + " " + (tx - 9 * ux - 4 * uy).toFixed(1) + "," + (ty - 9 * uy + 4 * ux).toFixed(1) + " " + (tx - 9 * ux + 4 * uy).toFixed(1) + "," + (ty - 9 * uy - 4 * ux).toFixed(1) + '"/>';
    }
    var g = "", t = "";
    items.forEach(function (it) {
      var k = it[0], c;
      if (k === "poly") g += '<polygon class="gp ' + (it[2] || "") + '" points="' + pts(it[1]) + '"/>';
      else if (k === "seg" || k === "ln") {
        g += '<line class="gs ' + (it[3] || "") + '" x1="' + X(it[1][0]) + '" y1="' + Y(it[1][1]) + '" x2="' + X(it[2][0]) + '" y2="' + Y(it[2][1]) + '"/>';
        if (k === "ln") { var e = it[4] == null ? "b" : it[4]; if (e) g += head(it[1], it[2], it[3] || ""); if (e === "b") g += head(it[2], it[1], it[3] || ""); }
      } else if (k === "ra") {
        var V = it[1], q = 9 / s;
        var u = [it[2], it[3]].map(function (P) { var dx = P[0] - V[0], dy = P[1] - V[1], n = Math.hypot(dx, dy); return [dx / n * q, dy / n * q]; });
        g += '<polyline class="gra" points="' + pts([[V[0] + u[0][0], V[1] + u[0][1]], [V[0] + u[0][0] + u[1][0], V[1] + u[0][1] + u[1][1]], [V[0] + u[1][0], V[1] + u[1][1]]]) + '"/>';
      } else if (k === "tick") {
        var ux = X(it[2][0]) - X(it[1][0]), uy = Y(it[2][1]) - Y(it[1][1]), nn = Math.hypot(ux, uy) || 1, mx = (X(it[1][0]) + X(it[2][0])) / 2, my = (Y(it[1][1]) + Y(it[2][1])) / 2; ux /= nn; uy /= nn;
        for (var j = 0; j < it[3]; j++) { var of = (j - (it[3] - 1) / 2) * 4, cx = mx + of * ux, cy = my + of * uy; g += '<line class="gtk" x1="' + (cx - 5 * uy).toFixed(1) + '" y1="' + (cy + 5 * ux).toFixed(1) + '" x2="' + (cx + 5 * uy).toFixed(1) + '" y2="' + (cy - 5 * ux).toFixed(1) + '"/>'; }
      } else if (k === "circ") g += '<circle class="gp ' + (it[3] || "") + '" cx="' + X(it[1][0]) + '" cy="' + Y(it[1][1]) + '" r="' + (it[2] * s).toFixed(1) + '"/>';
      else if (k === "sect") {
        if (it[4] - it[3] >= 359.99) g += '<circle class="gp ' + (it[5] || "") + '" cx="' + X(it[1][0]) + '" cy="' + Y(it[1][1]) + '" r="' + (it[2] * s).toFixed(1) + '"/>';
        else { c = pol(it[1], it[2], it[3]); g += '<path class="gp ' + (it[5] || "") + '" d="M' + X(it[1][0]) + " " + Y(it[1][1]) + "L" + X(c[0]) + " " + Y(c[1]) + arcTo(it[1], it[2], it[3], it[4]) + 'Z"/>'; }
      }
      else if (k === "arc") { c = pol(it[1], it[2], it[3]); g += '<path class="garc ' + (it[5] || "") + '" d="M' + X(c[0]) + " " + Y(c[1]) + arcTo(it[1], it[2], it[3], it[4]) + '"/>'; }
      else if (k === "dot") g += '<circle class="gd ' + (it[2] || "") + '" cx="' + X(it[1][0]) + '" cy="' + Y(it[1][1]) + '" r="3.5"/>';
      else if (k === "txt") { var op = it[3] || {}; t += '<text class="gt ' + (op.cls || "") + '" x="' + (X(it[1][0]) + (op.dx || 0)).toFixed(1) + '" y="' + (Y(it[1][1]) + (op.dy == null ? 4 : op.dy)).toFixed(1) + '" text-anchor="' + (op.a || "middle") + '">' + it[2] + "</text>"; }
    });
    return '<svg class="gfig" viewBox="0 0 ' + Wd + " " + H + '" style="max-width:' + Wd + 'px" role="img" aria-label="figura">' + g + t + "</svg>";
  }
  function T_(P, s, o) { return ["txt", P, s, o || {}]; }
  function lb(P, s, dx, dy, cls) { return ["txt", P, s, { dx: dx || 0, dy: dy == null ? -12 : dy, cls: cls || "" }]; }
  function vnames(V, names, k) {
    var cx = 0, cy = 0; V.forEach(function (p) { cx += p[0] / V.length; cy += p[1] / V.length; });
    return V.map(function (P, i) { var dx = P[0] - cx, dy = P[1] - cy, d = Math.hypot(dx, dy) || 1; return T_([P[0] + dx / d * (k || 0.3), P[1] + dy / d * (k || 0.3)], names[i]); });
  }

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

  var W_ = {
    recta: L3("recta", "recta", "line"), semi: L3("semirecta", "semirrecta", "ray"), seg: L3("segment", "segmento", "segment"),
    sec: L3("secants", "secantes", "intersecting"), par: L3("paral·leles", "paralelas", "parallel"), perp: L3("perpendiculars", "perpendiculares", "perpendicular"), coin: L3("coincidents", "coincidentes", "coincident")
  };
  var ANGK = [L3("nul", "nulo", "zero"), L3("agut", "agudo", "acute"), L3("recte", "recto", "right"), L3("obtús", "obtuso", "obtuse"), L3("pla", "llano", "straight"), L3("còncau", "cóncavo", "reflex"), L3("complet", "completo", "full")];
  function angKind(a) { return a === 0 ? 0 : a < 90 ? 1 : a === 90 ? 2 : a < 180 ? 3 : a === 180 ? 4 : a < 360 ? 5 : 6; }
  function angItems(V, a0, a, r, R, cls) {
    var it = [];
    if (a >= 360) it.push(["circ", V, R, cls || "af"]);
    else if (a === 90) it.push(["poly", [V, pol(V, R * 0.8, a0), pol(pol(V, R * 0.8, a0), R * 0.8, a0 + 90), pol(V, R * 0.8, a0 + 90)], cls || "af"]);
    else if (a > 0) it.push(["sect", V, R, a0, a0 + a, cls || "af"]);
    it.push(["ln", V, pol(V, r, a0), "", "e"]);
    if (a > 0 && a < 360) it.push(["ln", V, pol(V, r, a0 + a), "", "e"]);
    it.push(["dot", V]);
    return it;
  }

  /* ---------- 7.1 recta, semirecta i segment ---------- */
  var ELEM = {
    r: { it: function () { return [["ln", [-0.4, 0.2], [4.4, 1.8], "", "b"], ["dot", [0.8, 0.6]], lb([0.8, 0.6], "A"), ["dot", [3, 1.33]], lb([3, 1.33], "B")]; },
      t: L3("La <strong>recta</strong> $AB$ no té ni principi ni final: continua indefinidament pels dos costats (per això té dues fletxes). No es pot mesurar.", "La <strong>recta</strong> $AB$ no tiene ni principio ni final: continúa indefinidamente por los dos lados (por eso tiene dos flechas). No se puede medir.", "<strong>Line</strong> $AB$ has no beginning and no end: it goes on forever both ways (hence the two arrows). It can't be measured.") },
    s: { it: function () { return [["ln", [0.8, 0.6], [4.4, 1.8], "", "e"], ["dot", [0.8, 0.6]], lb([0.8, 0.6], "O"), ["dot", [3, 1.33]], lb([3, 1.33], "A")]; },
      t: L3("La <strong>semirecta</strong> comença en l'origen $O$ i continua indefinidament cap a un costat (una fletxa). Tampoc no es pot mesurar.", "La <strong>semirrecta</strong> empieza en el origen $O$ y continúa indefinidamente hacia un lado (una flecha). Tampoco se puede medir.", "The <strong>ray</strong> starts at $O$ and goes on forever in one direction (one arrow). It can't be measured either.") },
    g: { it: function () { return [["seg", [0.8, 0.6], [3, 1.33], "hl"], ["dot", [0.8, 0.6]], lb([0.8, 0.6], "A"), ["dot", [3, 1.33]], lb([3, 1.33], "B"), ["txt", [-0.4, 0.2], " "], ["txt", [4.4, 1.8], " "]]; },
      t: L3("El <strong>segment</strong> $\\overline{AB}$ té dos extrems, $A$ i $B$. Té una longitud que es pot mesurar amb el regle.", "El <strong>segmento</strong> $\\overline{AB}$ tiene dos extremos, $A$ y $B$. Tiene una longitud que se puede medir con la regla.", "<strong>Segment</strong> $\\overline{AB}$ has two endpoints, $A$ and $B$. Its length can be measured with a ruler.") },
    a: { it: function () { return [["ln", [-0.4, 0.2], [4.4, 1.8], "d", "b"], ["dot", [0.4, 0.47]], lb([0.4, 0.47], "A"), ["dot", [2, 1]], lb([2, 1], "B"), ["dot", [3.6, 1.53]], lb([3.6, 1.53], "C"), ["dot", [2.6, 0.2], "pa"], lb([2.6, 0.2], "D", 0, 16)]; },
      t: L3("$A$, $B$ i $C$ estan <strong>alineats</strong> (sobre la mateixa recta). $D$ no està alineat amb ells.", "$A$, $B$ y $C$ están <strong>alineados</strong> (sobre la misma recta). $D$ no está alineado con ellos.", "$A$, $B$ and $C$ are <strong>collinear</strong> (on the same line). $D$ is not on that line.") }
  };
  function wElem() {
    var w = document.getElementById("w-elem"); if (!w) return;
    var out = w.querySelector(".gout"), k = "r";
    function paint() { out.innerHTML = G(ELEM[k].it(), { W: 300, maxh: 150, pad: 22 }) + gcol([rtex(T(ELEM[k].t))]); }
    segs(w, [function (v) { k = v; paint(); }]); onLang(paint);
  }
  function wNpts() {
    var w = document.getElementById("w-npts"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var n = +sl.n.value, V = [], it = [], i, j;
      showRv(w, "n", "n", n);
      for (i = 0; i < n; i++) V.push(pol([0, 0], 1.5 + 0.25 * Math.sin(i * 2.3), 90 + 360 * i / n + 9 * Math.cos(i * 1.7)));
      for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) { var u = [V[j][0] - V[i][0], V[j][1] - V[i][1]], c = clipLine(V[i], u, [-2.2, -2.2, 2.2, 2.2]); if (c) it.push(["seg", c[0], c[1], "thin"]); }
      V.forEach(function (P, i) { it.push(["dot", P, "pa"]); it.push(T_(mid([0, 0], P, 1.17), String.fromCharCode(65 + i))); });
      var r = [tex("\\dfrac{" + n + "\\cdot" + (n - 1) + "}{2}=\\dfrac{" + n * (n - 1) + "}{2}=" + n * (n - 1) / 2),
        fill(T(L3("Amb {n} punts no alineats tres a tres hi ha <strong>{r} rectes</strong>: de cada punt n'ixen {m} (una cap a cada un dels altres) i cada recta es compta dues vegades.", "Con {n} puntos no alineados tres a tres hay <strong>{r} rectas</strong>: de cada punto salen {m} (una hacia cada uno de los otros) y cada recta se cuenta dos veces.", "With {n} points, no three collinear, there are <strong>{r} lines</strong>: {m} leave each point (one to each of the others) and each line is counted twice.")), { n: n, r: n * (n - 1) / 2, m: n - 1 })];
      out.innerHTML = G(it, { W: 260, maxh: 260, pad: 8, box: [-2.2, -2.2, 2.2, 2.2] }) + gcol(r);
    }
    sl.n.addEventListener("input", paint); onLang(paint);
  }

  /* ---------- 7.2 posicions relatives i mediatriu ---------- */
  var BX = [-4, -2.6, 4, 2.6];
  function posOf(a, d) {
    a = ((a % 180) + 180) % 180;
    if (a === 0) return d === 0 ? "coin" : "par";
    return a === 90 ? "perp" : "sec";
  }
  function twoLines(a, d, la, lb_) {
    var r = clipLine([0, 0], [1, 0], BX), s = clipLine([0, d], [Math.cos(a * Math.PI / 180), Math.sin(a * Math.PI / 180)], BX), k = posOf(a, d);
    var it = [["ln", r[0], r[1], "", "b"], ["ln", s[0], s[1], k === "coin" ? "hl dd" : "hl", "b"]];
    if (la !== false) it.push(T_([3.7, 0], "r", { dy: 16 }), T_(s[1], "s", { dx: s[1][0] > 3.5 ? -10 : 10, dy: s[1][1] > 2.4 ? 14 : -6, cls: "hy" }));
    if (k === "sec" || k === "perp") {
      var P = inter([0, 0], [1, 0], [0, d], [Math.cos(a * Math.PI / 180), Math.sin(a * Math.PI / 180)]);
      if (k === "perp") it.push(["ra", P, [P[0] + 1, 0], [P[0], 1]]); else it.push(amark(P, [P[0] + 1, 0], pol(P, 1, a), 0.5));
      it.push(["dot", P, "pa"]);
    }
    return it;
  }
  function wPos() {
    var w = document.getElementById("w-pos"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var a = +sl.a.value, d = +sl.d.value, k = posOf(a, d), am = Math.min(a % 180, 180 - a % 180);
      showRv(w, "a", "\\alpha", a, "^\\circ"); showRv(w, "d", "d", d);
      var txt = { sec: L3("Les rectes són <strong>secants</strong>: es tallen en un punt i formen angles de {a} i {b}.", "Las rectas son <strong>secantes</strong>: se cortan en un punto y forman ángulos de {a} y {b}.", "The lines <strong>intersect</strong>: they cross at one point, making angles of {a} and {b}."),
        perp: L3("Les rectes són <strong>perpendiculars</strong>: es tallen formant quatre angles rectes. $r\\perp s$", "Las rectas son <strong>perpendiculares</strong>: se cortan formando cuatro ángulos rectos. $r\\perp s$", "The lines are <strong>perpendicular</strong>: they cross making four right angles. $r\\perp s$"),
        par: L3("Les rectes són <strong>paral·leles</strong>: tenen la mateixa direcció i no es tallen mai. $r\\parallel s$", "Las rectas son <strong>paralelas</strong>: tienen la misma dirección y no se cortan nunca. $r\\parallel s$", "The lines are <strong>parallel</strong>: same direction, they never meet. $r\\parallel s$"),
        coin: L3("Les rectes són <strong>coincidents</strong>: són la mateixa recta.", "Las rectas son <strong>coincidentes</strong>: son la misma recta.", "The lines are <strong>coincident</strong>: they are the same line.") }[k];
      out.innerHTML = G(twoLines(a, d), { W: 300, maxh: 200, pad: 8, box: BX }) + gcol([rtex(fill(T(txt), { a: "$" + am + "^\\circ$", b: "$" + (180 - am) + "^\\circ$" }))]);
    }
    [sl.a, sl.d].forEach(function (i) { i.addEventListener("input", paint); });
    quickBind(w, function (v) { sl.a.value = v[0]; sl.d.value = v[1]; paint(); });
    onLang(paint);
  }
  function wMedi() {
    var w = document.getElementById("w-medi"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout"), mode = "m";
    function paint() {
      var p = +sl.p.value, A = [-2, 0], B = [2, 0], P = [mode === "m" ? 0 : 0.9, p], pa = dist(P, A), pb = dist(P, B);
      showRv(w, "p", "y_P", p);
      var it = [["seg", A, B], ["ln", [0, -3], [0, 4.2], "hl", "b"], ["ra", [0, 0], [1, 0], [0, 1]], ["tick", A, [0, 0], 1], ["tick", [0, 0], B, 1], ["seg", P, A, "ch"], ["seg", P, B, "ch2"],
        ["dot", A], lb(A, "A", -8, 16), ["dot", B], lb(B, "B", 8, 16), ["dot", P, "pa"], lb(P, "P", 12, 0), T_([0, 4], "m", { dx: 10, cls: "hy" }),
        T_(mid(P, A), lab(pa), { dx: -14, dy: -4, cls: "c1" }), T_(mid(P, B), lab(pb), { dx: 14, dy: -4, cls: "c2" })];
      var eq = Math.abs(pa - pb) < 1e-9;
      out.innerHTML = G(it, { W: 260, maxh: 240, pad: 18, box: [-2.6, -3, 2.6, 4.2] }) + gcol([tex("PA" + (eq ? "=" : "\\ne") + "PB"),
        eq ? rtex(T(L3("P està sobre la mediatriu: està a la mateixa distància de $A$ i de $B$.", "P está sobre la mediatriz: está a la misma distancia de $A$ y de $B$.", "P is on the perpendicular bisector: it's the same distance from $A$ and $B$.")))
          : rtex(T(L3("P no està sobre la mediatriu: està més a prop de $B$ que de $A$.", "P no está sobre la mediatriz: está más cerca de $B$ que de $A$.", "P isn't on the bisector: it's closer to $B$ than to $A$.")))]);
    }
    sl.p.addEventListener("input", paint); segs(w, [function (v) { mode = v; paint(); }]); onLang(paint);
  }

  /* ---------- 7.3 angles ---------- */
  function wAng() {
    var w = document.getElementById("w-ang"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout"), bis = false;
    function paint() {
      var a = +sl.a.value, k = angKind(a);
      showRv(w, "a", "\\alpha", a, "^\\circ");
      var it = angItems([0, 0], 0, a, 2, 0.6), rows = [];
      if (bis && a > 0 && a < 360) { it.push(["ln", [0, 0], pol([0, 0], 2.2, a / 2), "hl", "e"], ["sect", [0, 0], 0.9, 0, a / 2, "af2"]); }
      it.push(["txt", [-2.2, -2.2], " "], ["txt", [2.2, 2.2], " "]);
      rows.push(fill(T(L3("Un angle de {a} és <strong>{k}</strong>.", "Un ángulo de {a} es <strong>{k}</strong>.", "An angle of {a} is <strong>{k}</strong>.")), { a: tex(a + "^\\circ"), k: T(ANGK[k]) }));
      if (a > 0 && a < 360) rows.push(a <= 180 ? T(L3("És convex (no passa de 180°).", "Es convexo (no pasa de 180°).", "It's convex (not more than 180°).")) : T(L3("És còncau (passa de 180°).", "Es cóncavo (pasa de 180°).", "It's reflex (more than 180°).")));
      if (bis && a > 0 && a < 360) rows.push(fill(T(L3("La bisectriu el dividix en dos angles de {h}.", "La bisectriz lo divide en dos ángulos de {h}.", "The bisector splits it into two angles of {h}.")), { h: tex((a / 2 === Math.floor(a / 2) ? a / 2 : sxT(a * 1800)) + (isInt(a / 2) ? "^\\circ" : "")) }));
      out.innerHTML = G(it, { W: 240, maxh: 240, pad: 10 }) + gcol(rows);
    }
    sl.a.addEventListener("input", paint);
    segs(w, [function (v) { bis = v === "b"; paint(); }]);
    quickBind(w, function (v) { sl.a.value = v[0]; paint(); });
    onLang(paint);
  }

  /* ---------- 7.4 sistema sexagesimal ---------- */
  function rdInt(i) { var v = intIn(i.value); return v; }
  function toSecSteps(d, m, s) {
    var t = d * 3600 + m * 60 + s;
    return [tex(d + "^\\circ\\," + m + "'\\," + s + "''=" + d + "\\cdot3600''+" + m + "\\cdot60''+" + s + "''=" + d * 3600 + "''+" + m * 60 + "''+" + s + "''=" + t + "''"),
      tex(d + "^\\circ\\," + m + "'=" + d + "\\cdot60'+" + m + "'=" + (d * 60 + m) + "'") + (s ? " " + T(L3("(i sobren " + s + "″)", "(y sobran " + s + "″)", "(plus " + s + "″)")) : ""),
      tex("\\approx " + d2(t / 3600) + "^\\circ")];
  }
  function toCplxSteps(n, unit) {
    var rows = [];
    if (unit === "s") {
      var mm = Math.floor(n / 60), ss = n % 60, dd = Math.floor(mm / 60), m2 = mm % 60;
      rows.push(tex(n + "'':60=" + mm + "'\\ \\ \\text{" + T(L3("i sobren", "y sobran", "remainder")) + "}\\ " + ss + "''"));
      if (mm >= 60) rows.push(tex(mm + "':60=" + dd + "^\\circ\\ \\ \\text{" + T(L3("i sobren", "y sobran", "remainder")) + "}\\ " + m2 + "'"));
      rows.push(tex(n + "''=\\boxed{" + sxT(n) + "}"));
    } else {
      rows.push(tex(n + "':60=" + Math.floor(n / 60) + "^\\circ\\ \\ \\text{" + T(L3("i sobren", "y sobran", "remainder")) + "}\\ " + n % 60 + "'"));
      rows.push(tex(n + "'=\\boxed{" + sxT(n * 60) + "}"));
    }
    return rows;
  }
  function wSexa() {
    var w = document.getElementById("w-sexa"); if (!w) return;
    var ii = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), mode = "c", unit = "s";
    var rc = w.querySelector(".sx-c"), ri = w.querySelector(".sx-i");
    function paint() {
      rc.style.display = mode === "c" ? "" : "none"; ri.style.display = mode === "i" ? "" : "none"; info.innerHTML = "";
      if (mode === "c") {
        var d = rdInt(ii.d), m = rdInt(ii.m), s = rdInt(ii.s);
        if (d === null || m === null || s === null) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu nombres naturals.", "Escribe números naturales.", "Type whole numbers."))); return; }
        out.innerHTML = rows2html(toSecSteps(d, m, s)) + (m >= 60 || s >= 60 ? '<div class="hrow">' + warn(T(L3("Compte: en forma complexa, els minuts i els segons han de ser més menuts que 60.", "Cuidado: en forma compleja, los minutos y los segundos deben ser menores que 60.", "Careful: in compound form, minutes and seconds must be under 60."))) + "</div>" : "");
      } else {
        var n = rdInt(ii.n);
        if (n === null) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu un nombre natural.", "Escribe un número natural.", "Type a whole number."))); return; }
        out.innerHTML = rows2html(toCplxSteps(n, unit));
      }
    }
    segs(w, [function (v) { mode = v; paint(); }, function (v) { unit = v; paint(); }]);
    Object.keys(ii).forEach(function (k) { ii[k].addEventListener("input", paint); });
    onLang(paint);
  }
  /* operacions en columna */
  function colTex(rows, line) {
    return "\\begin{array}{rrrr}" + rows.map(function (r, i) { return r.join(" & ") + (i === rows.length - 1 ? "" : i === line ? "\\\\ \\hline " : "\\\\"); }).join("") + "\\end{array}";
  }
  function dmsRow(sg, d, m, s) { return [sg, d + "^\\circ", m + "'", s + "''"]; }
  function sxAdd(A, B) {
    var a = dmsOf(A), b = dmsOf(B), d = a[0] + b[0], m = a[1] + b[1], s = a[2] + b[2], r = [tex(colTex([dmsRow("", a[0], a[1], a[2]), dmsRow("+", b[0], b[1], b[2]), dmsRow("", d, m, s)], 1))];
    if (s >= 60) { r.push(tex(s + "''=" + Math.floor(s / 60) + "'\\," + s % 60 + "''") + " → " + tex(d + "^\\circ\\," + (m + Math.floor(s / 60)) + "'\\," + s % 60 + "''")); m += Math.floor(s / 60); s %= 60; }
    if (m >= 60) { r.push(tex(m + "'=" + Math.floor(m / 60) + "^\\circ\\," + m % 60 + "'") + " → " + tex((d + Math.floor(m / 60)) + "^\\circ\\," + m % 60 + "'\\," + s + "''")); }
    r.push(tex("=\\boxed{" + sxT(A + B) + "}"));
    return r;
  }
  function sxSub(A, B) {
    var a = dmsOf(A), b = dmsOf(B), r = [], d = a[0], m = a[1], s = a[2], ch = false;
    if (s < b[2]) { s += 60; m -= 1; ch = true; }
    if (m < b[1]) { m += 60; d -= 1; ch = true; }
    if (ch) r.push(T(L3("Convertim unitats per a poder restar:", "Convertimos unidades para poder restar:", "Borrow so we can subtract:")) + " " + tex(sxT(A) + "=" + d + "^\\circ\\," + m + "'\\," + s + "''"));
    r.push(tex(colTex([dmsRow("", d, m, s), dmsRow("-", b[0], b[1], b[2]), dmsRow("", d - b[0], m - b[1], s - b[2])], 1)));
    r.push(tex("=\\boxed{" + sxT(A - B) + "}"));
    return r;
  }
  function sxMul(A, k) {
    var a = dmsOf(A), d = a[0] * k, m = a[1] * k, s = a[2] * k, r = [tex("(" + sxT(A) + ")\\cdot" + k + "=" + d + "^\\circ\\," + m + "'\\," + s + "''")];
    if (s >= 60) { m += Math.floor(s / 60); s %= 60; r.push(tex("=" + d + "^\\circ\\," + m + "'\\," + s + "''")); }
    if (m >= 60) { d += Math.floor(m / 60); m %= 60; r.push(tex("=" + d + "^\\circ\\," + m + "'\\," + s + "''")); }
    r.push(tex("=\\boxed{" + sxT(A * k) + "}"));
    return r;
  }
  function sxDiv(A, k) {
    var a = dmsOf(A), r = [], rr = T(L3("i sobren", "y sobran", "remainder"));
    var qd = Math.floor(a[0] / k), rd = a[0] % k, m = a[1] + rd * 60, qm = Math.floor(m / k), rm = m % k, s = a[2] + rm * 60, qs = Math.floor(s / k), rs = s % k;
    r.push(tex(a[0] + "^\\circ:" + k + "=" + qd + "^\\circ\\ \\text{" + rr + "}\\ " + rd + "^\\circ=" + rd * 60 + "'"));
    r.push(tex("(" + rd * 60 + "'+" + a[1] + "'):" + k + "=" + m + "':" + k + "=" + qm + "'\\ \\text{" + rr + "}\\ " + rm + "'=" + rm * 60 + "''"));
    r.push(tex("(" + rm * 60 + "''+" + a[2] + "''):" + k + "=" + s + "'':" + k + "=" + qs + "''" + (rs ? "\\ \\text{" + rr + "}\\ " + rs + "''" : "")));
    r.push(tex("(" + sxT(A) + "):" + k + (rs ? "\\approx" : "=") + "\\boxed{" + sxT(qd * 3600 + qm * 60 + qs) + "}"));
    return r;
  }
  function wSexop() {
    var w = document.getElementById("w-sexop"); if (!w) return;
    var ii = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), op = "+";
    var rb = w.querySelector(".op-b"), rn = w.querySelector(".op-n");
    function paint() {
      rb.style.display = op === "+" || op === "-" ? "" : "none"; rn.style.display = op === "*" || op === "/" ? "" : "none"; info.innerHTML = "";
      var v = ["d1", "m1", "s1", "d2", "m2", "s2", "k"].map(function (k) { return rdInt(ii[k]); });
      if (v.slice(0, 3).some(function (x) { return x === null; }) || ((op === "+" || op === "-") && v.slice(3, 6).some(function (x) { return x === null; })) || ((op === "*" || op === "/") && !v[6])) {
        out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu nombres naturals (i un nombre més gran que 0 per a multiplicar o dividir).", "Escribe números naturales (y un número mayor que 0 para multiplicar o dividir).", "Type whole numbers (and a number above 0 to multiply or divide by)."))); return;
      }
      var A = v[0] * 3600 + v[1] * 60 + v[2], B = v[3] * 3600 + v[4] * 60 + v[5];
      if (op === "-" && B > A) { out.innerHTML = ""; info.innerHTML = warn(T(L3("El segon angle és més gran que el primer: no es pot restar.", "El segundo ángulo es mayor que el primero: no se puede restar.", "The second angle is bigger than the first: can't subtract."))); return; }
      out.innerHTML = rows2html(op === "+" ? sxAdd(A, B) : op === "-" ? sxSub(A, B) : op === "*" ? sxMul(A, v[6]) : sxDiv(A, v[6]));
    }
    segs(w, [function (v) { op = v; paint(); }]);
    Object.keys(ii).forEach(function (k) { ii[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 7.5 relacions entre angles ---------- */
  function pairItems(a, tot) {
    var it = [["sect", [0, 0], 0.55, 0, a, "af"], ["sect", [0, 0], 0.75, a, tot, "af2"], ["ln", [0, 0], [1.9, 0], "", "e"], ["ln", [0, 0], pol([0, 0], 1.9, a), "", "e"], ["ln", [0, 0], pol([0, 0], 1.9, tot), "", "e"], ["dot", [0, 0]],
      T_(pol([0, 0], 0.95, a / 2), "α", { cls: "hot" }), T_(pol([0, 0], 1.12, (a + tot) / 2), "β", { cls: "hot" })];
    if (tot === 90) it.push(["ra", [0, 0], [1, 0], [0, 1]]);
    return it;
  }
  function wComp() {
    var w = document.getElementById("w-comp"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout"), mode = "c";
    function paint() {
      var a = +sl.a.value, tot = mode === "c" ? 90 : 180;
      showRv(w, "a", "\\alpha", a, "^\\circ");
      if (a >= tot) { out.innerHTML = G(angItems([0, 0], 0, a, 1.9, 0.55).concat([["txt", [-1.9, -0.2], " "], ["txt", [1.9, 1.9], " "]]), { W: 220, maxh: 180, pad: 10 }) + gcol([rtex(fill(T(L3("Un angle de {a} no té complementari: només en tenen els angles aguts.", "Un ángulo de {a} no tiene complementario: solo lo tienen los ángulos agudos.", "An angle of {a} has no complement: only acute angles do.")), { a: "$" + a + "^\\circ$" }))]); return; }
      out.innerHTML = G(pairItems(a, tot).concat([["txt", [-1.9, -0.2], " "], ["txt", [1.9, 1.9], " "]]), { W: 220, maxh: 180, pad: 10 }) +
        gcol([tex("\\beta=" + tot + "^\\circ-" + a + "^\\circ=" + (tot - a) + "^\\circ"), rtex(fill(T(mode === "c" ? L3("$\\alpha$ i $\\beta$ són complementaris: sumen {t}.", "$\\alpha$ y $\\beta$ son complementarios: suman {t}.", "$\\alpha$ and $\\beta$ are complementary: they add up to {t}.") : L3("$\\alpha$ i $\\beta$ són suplementaris (i adjacents): sumen {t}.", "$\\alpha$ y $\\beta$ son suplementarios (y adyacentes): suman {t}.", "$\\alpha$ and $\\beta$ are supplementary (a linear pair): they add up to {t}.")), { t: "$" + tot + "^\\circ$" }))]);
    }
    sl.a.addEventListener("input", paint); segs(w, [function (v) { mode = v; paint(); }]); onLang(paint);
  }
  var PGRP = { t: null, c: [[1, 5], [2, 6], [3, 7], [4, 8]], i: [[1, 7], [2, 8]], e: [[3, 5], [4, 6]], o: [[1, 3], [2, 4], [5, 7], [6, 8]] };
  function parItems(a, hl, nums, given, ask) {
    var h = 1.6, X1 = h / Math.tan(a * Math.PI / 180), P1 = [0, 0], P2 = [X1, h];
    var it = [["ln", [Math.min(-2, X1 - 2), 0], [Math.max(2, X1 + 2), 0], "", "b"], ["ln", [Math.min(-2, X1 - 2), h], [Math.max(2, X1 + 2), h], "", "b"], ["ln", pol(P1, 1.25, 180 + a), pol(P2, 1.25, a), "", "b"]];
    [[P1, 0], [P2, 4]].forEach(function (pp) {
      [[0, a], [a, 180], [180, 180 + a], [180 + a, 360]].forEach(function (r, k) {
        var n = pp[1] + k + 1, cls = k % 2 === 0 ? "af" : "af2", on = !hl || hl.indexOf(n) >= 0;
        if (!on) cls = "af0";
        if (given || ask) cls = n === given ? "af" : n === ask ? "af2" : "af0";
        it.push(["sect", pp[0], k % 2 === 0 ? 0.42 : 0.32, r[0], r[1], cls]);
        if (nums) it.push(T_(pol(pp[0], 0.7, (r[0] + r[1]) / 2), String(n), { cls: on ? "hot" : "" }));
        else if (n === given) it.push(T_(pol(pp[0], 0.78, (r[0] + r[1]) / 2), (k % 2 === 0 ? a : 180 - a) + "°", { cls: "hot" }));
        else if (n === ask) it.push(T_(pol(pp[0], 0.7, (r[0] + r[1]) / 2), "x", { cls: "hot" }));
      });
    });
    it.push(["dot", P1], ["dot", P2], T_([Math.min(-2, X1 - 2), h], "r", { dy: -8 }), T_([Math.min(-2, X1 - 2), 0], "s", { dy: -8 }));
    return it;
  }
  function parVal(a, n) { return (n - 1) % 2 === 0 ? a : 180 - a; }
  function wPar() {
    var w = document.getElementById("w-par"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout"), g = "t";
    var GN = { c: L3("Corresponents", "Correspondientes", "Corresponding"), i: L3("Alterns interns", "Alternos internos", "Alternate interior"), e: L3("Alterns externs", "Alternos externos", "Alternate exterior"), o: L3("Oposats pel vèrtex", "Opuestos por el vértice", "Vertically opposite") };
    function paint() {
      var a = +sl.a.value, hl = null, rows = [];
      showRv(w, "a", "\\alpha", a, "^\\circ");
      if (g !== "t") { hl = []; PGRP[g].forEach(function (p) { hl = hl.concat(p); }); rows.push("<strong>" + T(GN[g]) + ":</strong> " + PGRP[g].map(function (p) { return tex("\\hat" + p[0] + "=\\hat" + p[1] + "=" + parVal(a, p[0]) + "^\\circ"); }).join(", ")); }
      else {
        rows.push(tex("\\hat1=\\hat3=\\hat5=\\hat7=" + a + "^\\circ"), tex("\\hat2=\\hat4=\\hat6=\\hat8=180^\\circ-" + a + "^\\circ=" + (180 - a) + "^\\circ"));
        if (a === 90) rows.push(T(L3("La secant és perpendicular a les paral·leles: els 8 angles són rectes.", "La secante es perpendicular a las paralelas: los 8 ángulos son rectos.", "The transversal is perpendicular to the parallels: all 8 angles are right angles.")));
      }
      out.innerHTML = G(parItems(a, hl, true), { W: 320, maxh: 200, pad: 12 }) + gcol(rows);
    }
    sl.a.addEventListener("input", paint); segs(w, [function (v) { g = v; paint(); }]); onLang(paint);
  }

  /* ---------- 7.6 polígons i diagonals ---------- */
  var PN = { 3: L3("triangle", "triángulo", "triangle"), 4: L3("quadrilàter", "cuadrilátero", "quadrilateral"), 5: L3("pentàgon", "pentágono", "pentagon"), 6: L3("hexàgon", "hexágono", "hexagon"), 7: L3("heptàgon", "heptágono", "heptagon"), 8: L3("octàgon", "octógono", "octagon"), 9: L3("enneàgon", "eneágono", "nonagon"), 10: L3("decàgon", "decágono", "decagon"), 11: L3("endecàgon", "endecágono", "hendecagon"), 12: L3("dodecàgon", "dodecágono", "dodecagon") };
  function wDiag() {
    var w = document.getElementById("w-diag"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout"), all = false;
    function paint() {
      var n = +sl.n.value, V = reg(n, 1.6), it = [["poly", V, "gf"]], i, j;
      showRv(w, "n", "n", n);
      for (i = 0; i < n; i++) for (j = i + 2; j < n; j++) { if (i === 0 && j === n - 1) continue; if (all || i === 0) it.push(["seg", V[i], V[j], i === 0 ? "hl" : "d"]); }
      V.forEach(function (P, k) { it.push(["dot", P, k === 0 ? "pa" : ""]); });
      out.innerHTML = G(it, { W: 230, maxh: 230, pad: 12 }) + gcol([fill(T(L3("<strong>{N}</strong>: {n} costats i {n} vèrtexs.", "<strong>{N}</strong>: {n} lados y {n} vértices.", "<strong>{N}</strong>: {n} sides and {n} vertices.")), { N: T(PN[n]).charAt(0).toUpperCase() + T(PN[n]).slice(1), n: n }),
        fill(T(L3("Diagonals des de cada vèrtex: {a}", "Diagonales desde cada vértice: {a}", "Diagonals from each vertex: {a}")), { a: tex(n + "-3=" + (n - 3)) }),
        fill(T(L3("Diagonals en total: {a}", "Diagonales en total: {a}", "Diagonals in all: {a}")), { a: tex("\\dfrac{" + n + "\\cdot" + (n - 3) + "}{2}=" + n * (n - 3) / 2) })]);
    }
    sl.n.addEventListener("input", paint); segs(w, [function (v) { all = v === "t"; paint(); }]); onLang(paint);
  }

  /* ---------- 7.7 triangles ---------- */
  var SIDEK = [L3("equilàter", "equilátero", "equilateral"), L3("isòsceles", "isósceles", "isosceles"), L3("escalé", "escaleno", "scalene")];
  var TANGK = [L3("acutangle", "acutángulo", "acute"), L3("rectangle", "rectángulo", "right"), L3("obtusangle", "obtusángulo", "obtuse")];
  function sideKind(a, b, c) { return a === b && b === c ? 0 : a === b || b === c || a === c ? 1 : 2; }
  function angKindT(A) { var m = Math.max.apply(null, A); return Math.abs(m - 90) < 1e-6 ? 1 : m > 90 ? 2 : 0; }
  /* triangle amb els angles A (en el vèrtex A) i B sobre una base de longitud L */
  function triFromAngles(A, B, Lb) {
    Lb = Lb || 4; var P = inter([0, 0], [Math.cos(A * Math.PI / 180), Math.sin(A * Math.PI / 180)], [Lb, 0], [Math.cos((180 - B) * Math.PI / 180), Math.sin((180 - B) * Math.PI / 180)]);
    return [[0, 0], [Lb, 0], P];
  }
  function triFromSides(a, b, c) {
    /* c = AB a la base, b = AC, a = BC */
    var x = (b * b + c * c - a * a) / (2 * c), y = Math.sqrt(Math.max(0, b * b - x * x));
    return [[0, 0], [c, 0], [x, y]];
  }
  function triAngles(V) { return [angAt(V[0], V[1], V[2]), angAt(V[1], V[2], V[0]), angAt(V[2], V[0], V[1])]; }
  function triItems(V, opts) {
    opts = opts || {}; var it = [["poly", V, "gf"]], Ag = triAngles(V), names = opts.names || ["A", "B", "C"];
    [0, 1, 2].forEach(function (i) {
      var P = V[i], Q = V[(i + 1) % 3], R = V[(i + 2) % 3];
      if (Math.abs(Ag[i] - 90) < 1e-6) it.push(["ra", P, Q, R]); else if (opts.marks !== false) it.push(amark(P, Q, R, 0.45, ["af", "af2", "af3"][i]));
    });
    if (opts.ticks) {
      var s = [dist(V[0], V[1]), dist(V[1], V[2]), dist(V[2], V[0])];
      [0, 1, 2].forEach(function (i) { var eq = s.filter(function (x) { return Math.abs(x - s[i]) < 1e-9; }).length; if (eq > 1) it.push(["tick", V[i], V[(i + 1) % 3], 1]); });
    }
    return it.concat(vnames(V, names, 0.32));
  }
  function wTsum() {
    var w = document.getElementById("w-tsum"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var a = +sl.a.value, b = +sl.b.value, c = 180 - a - b;
      showRv(w, "a", "\\hat A", a, "^\\circ"); showRv(w, "b", "\\hat B", b, "^\\circ");
      if (c <= 0) { out.innerHTML = gcol([warn(fill(T(L3("No hi ha cap triangle: {a} i {b} ja sumen {s}, i els tres angles han de sumar 180°.", "No hay ningún triángulo: {a} y {b} ya suman {s}, y los tres ángulos deben sumar 180°.", "There's no triangle: {a} and {b} already add up to {s}, and all three must make 180°.")), { a: a + "°", b: b + "°", s: (a + b) + "°" }))]); return; }
      var V = triFromAngles(a, b, 4);
      out.innerHTML = G(triItems(V), { W: 280, maxh: 200, pad: 22 }) + gcol([tex("\\hat C=180^\\circ-(" + a + "^\\circ+" + b + "^\\circ)=180^\\circ-" + (a + b) + "^\\circ=" + c + "^\\circ"),
        fill(T(L3("El triangle és <strong>{k}</strong>.", "El triángulo es <strong>{k}</strong>.", "The triangle is <strong>{k}</strong>.")), { k: T(TANGK[angKindT([a, b, c])]) + (a === b || b === c || a === c ? (a === b && b === c ? ", " + T(SIDEK[0]) : ", " + T(SIDEK[1])) : "") })]);
    }
    [sl.a, sl.b].forEach(function (i) { i.addEventListener("input", paint); }); onLang(paint);
  }
  function wTri() {
    var w = document.getElementById("w-tri"); if (!w) return;
    var ii = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = "";
      var a = numIn(ii.a.value), b = numIn(ii.b.value), c = numIn(ii.c.value);
      if (a === null || b === null || c === null || a <= 0 || b <= 0 || c <= 0) { out.innerHTML = ""; info.innerHTML = warn(T(L3("Escriu tres longituds positives.", "Escribe tres longitudes positivas.", "Type three positive lengths."))); return; }
      var s = [a, b, c].sort(function (x, y) { return x - y; }), ok = s[2] < s[0] + s[1] - 1e-9;
      var r1 = tex(nf(s[2]) + (ok ? "<" : "\\ge ") + nf(s[0]) + "+" + nf(s[1]) + "=" + nf(s[0] + s[1]));
      if (!ok) { out.innerHTML = gcol([r1, warn(T(L3("El costat més llarg no és més menut que la suma dels altres dos: <strong>no es pot construir</strong> el triangle.", "El lado más largo no es menor que la suma de los otros dos: <strong>no se puede construir</strong> el triángulo.", "The longest side isn't less than the sum of the other two: the triangle <strong>can't be built</strong>.")))]); return; }
      var V = triFromSides(a, b, c), Ag = triAngles(V), sk = sideKind(a, b, c), ak = angKindT(Ag.map(function (x) { return Math.round(x * 1e6) / 1e6; }));
      var it = triItems(V, { ticks: true }).concat([T_(mid(V[0], V[1]), "c = " + lab(c), { dy: 16 }), T_(mid(V[1], V[2]), "a = " + lab(a), { dx: 8, a: "start", dy: 0 }), T_(mid(V[2], V[0]), "b = " + lab(b), { dx: -8, a: "end", dy: 0 })]);
      out.innerHTML = G(it, { W: 290, maxh: 220, pad: 40 }) + gcol([r1 + " ✓ " + T(L3("Sí que es pot construir.", "Sí se puede construir.", "It can be built.")),
        fill(T(L3("Segons els costats és <strong>{s}</strong>; segons els angles, <strong>{a}</strong>.", "Según sus lados es <strong>{s}</strong>; según sus ángulos, <strong>{a}</strong>.", "By its sides it's <strong>{s}</strong>; by its angles, <strong>{a}</strong>.")), { s: T(SIDEK[sk]), a: T(TANGK[ak]) }),
        T(L3("Angles (mesurats sobre el dibuix):", "Ángulos (medidos sobre el dibujo):", "Angles (measured on the drawing):")) + " " + tex("\\hat A" + deg(Ag[0]).replace(/^(\d)/, "=$1") + ",\\ \\hat B" + deg(Ag[1]).replace(/^(\d)/, "=$1") + ",\\ \\hat C" + deg(Ag[2]).replace(/^(\d)/, "=$1"))]);
    }
    Object.keys(ii).forEach(function (k) { ii[k].addEventListener("input", paint); });
    quickBind(w, function (v) { ii.a.value = v[0]; ii.b.value = v[1]; ii.c.value = v[2]; paint(); });
    onLang(paint);
  }
  function foot(P, A, B) { var u = [B[0] - A[0], B[1] - A[1]], t = ((P[0] - A[0]) * u[0] + (P[1] - A[1]) * u[1]) / (u[0] * u[0] + u[1] * u[1]); return [A[0] + u[0] * t, A[1] + u[1] * t]; }
  function notable(V, k) {
    var A = V[0], B = V[1], C = V[2], it = [], P, bx = [-1.6, -1.8, 6.6, 4.8];
    function full(Q, u, cls) { var c = clipLine(Q, u, bx); if (c) it.push(["seg", c[0], c[1], cls]); }
    if (k === "m") {
      [[A, B], [B, C], [C, A]].forEach(function (s) { var M = mid(s[0], s[1]); full(M, [-(s[1][1] - s[0][1]), s[1][0] - s[0][0]], "hl"); it.push(["dot", M], ["ra", M, s[1], pol(M, 1, dirn(s[0], s[1]) + 90)]); });
      P = inter(mid(A, B), [-(B[1] - A[1]), B[0] - A[0]], mid(B, C), [-(C[1] - B[1]), C[0] - B[0]]);
      if (P && P[1] - dist(P, A) > bx[1] - 0.6 && P[1] + dist(P, A) < bx[3] + 0.6 && Math.abs(P[0] - 2.5) + dist(P, A) < 4.8) it.push(["circ", P, dist(P, A), "gc dd"]);
    } else if (k === "b") {
      V.forEach(function (Q, i) {
        var R = V[(i + 1) % 3], S = V[(i + 2) % 3], u1 = [(R[0] - Q[0]) / dist(Q, R), (R[1] - Q[1]) / dist(Q, R)], u2 = [(S[0] - Q[0]) / dist(Q, S), (S[1] - Q[1]) / dist(Q, S)], u = [u1[0] + u2[0], u1[1] + u2[1]];
        var X = inter(Q, u, R, [S[0] - R[0], S[1] - R[1]]); it.push(["seg", Q, X, "hl"]);
      });
      var a = dist(B, C), b = dist(C, A), c = dist(A, B), p = a + b + c;
      P = [(a * A[0] + b * B[0] + c * C[0]) / p, (a * A[1] + b * B[1] + c * C[1]) / p];
      it.push(["circ", P, Math.abs(P[1]), "gc dd"]);
    } else if (k === "h") {
      V.forEach(function (Q, i) {
        var R = V[(i + 1) % 3], S = V[(i + 2) % 3], F = foot(Q, R, S), t = ((F[0] - R[0]) * (S[0] - R[0]) + (F[1] - R[1]) * (S[1] - R[1])) / Math.pow(dist(R, S), 2);
        if (t < 0 || t > 1) it.push(["seg", t < 0 ? R : S, F, "d"]);
        if (dist(Q, F) > 1e-9) { full(Q, [F[0] - Q[0], F[1] - Q[1]], "thin"); it.push(["seg", Q, F, "hl"]); if (dist(F, R) > 1e-9 && dist(F, S) > 1e-9) it.push(["ra", F, Q, dist(F, R) > dist(F, S) ? R : S]); }
      });
      var u = [-(C[1] - B[1]), C[0] - B[0]], v = [-(C[1] - A[1]), C[0] - A[0]];
      P = inter(A, u, B, v);
    } else {
      V.forEach(function (Q, i) { var M = mid(V[(i + 1) % 3], V[(i + 2) % 3]); it.push(["seg", Q, M, "hl"], ["dot", M]); });
      P = [(A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3];
    }
    it.unshift(["poly", V, "gf"]);
    var inside = P && P[0] > bx[0] && P[0] < bx[2] && P[1] > bx[1] && P[1] < bx[3];
    if (inside) it.push(["dot", P, "pa"], T_(P, { m: "O", b: "I", h: "H", g: "G" }[k], { dx: 12, dy: -6, cls: "hot" }));
    return { it: it.concat(vnames(V, ["A", "B", "C"], 0.35)), P: P, inside: inside, bx: bx };
  }
  function wNotable() {
    var w = document.getElementById("w-notable"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout"), k = "m";
    var NM = { m: L3("<strong>Circumcentre</strong> $O$: centre de la circumferència que passa pels tres vèrtexs.", "<strong>Circuncentro</strong> $O$: centro de la circunferencia que pasa por los tres vértices.", "<strong>Circumcentre</strong> $O$: centre of the circle through the three vertices."),
      b: L3("<strong>Incentre</strong> $I$: centre de la circumferència inscrita, tangent als tres costats.", "<strong>Incentro</strong> $I$: centro de la circunferencia inscrita, tangente a los tres lados.", "<strong>Incentre</strong> $I$: centre of the inscribed circle, touching all three sides."),
      h: L3("<strong>Ortocentre</strong> $H$: punt on es tallen les tres altures (o les seues prolongacions).", "<strong>Ortocentro</strong> $H$: punto donde se cortan las tres alturas (o sus prolongaciones).", "<strong>Orthocentre</strong> $H$: where the three altitudes (or their extensions) meet."),
      g: L3("<strong>Baricentre</strong> $G$: punt on es tallen les tres mitjanes; és el centre de gravetat del triangle.", "<strong>Baricentro</strong> $G$: punto donde se cortan las tres medianas; es el centro de gravedad del triángulo.", "<strong>Centroid</strong> $G$: where the three medians meet; it's the triangle's centre of gravity.") };
    function paint() {
      var cx = +sl.cx.value, V = [[0, 0], [5, 0], [cx, 3.2]], N = notable(V, k), Ag = triAngles(V), ak = angKindT(Ag.map(function (x) { return Math.round(x * 1000) / 1000; }));
      showRv(w, "cx", "x_C", cx);
      var where = !N.P ? "" : !N.inside ? T(L3("El punt queda molt lluny, fora del dibuix.", "El punto queda muy lejos, fuera del dibujo.", "The point is very far away, off the drawing.")) :
        (function () { var P = N.P, s = function (A, B) { return (B[0] - A[0]) * (P[1] - A[1]) - (B[1] - A[1]) * (P[0] - A[0]); }, d = [s(V[0], V[1]), s(V[1], V[2]), s(V[2], V[0])];
          var on = d.some(function (x) { return Math.abs(x) < 1e-6; }), inn = d.every(function (x) { return x > 1e-6; });
          return on ? T(L3("El punt queda <strong>sobre un costat</strong> (o en un vèrtex).", "El punto queda <strong>sobre un lado</strong> (o en un vértice).", "The point lies <strong>on a side</strong> (or at a vertex).")) : inn ? T(L3("El punt queda <strong>dins</strong> del triangle.", "El punto queda <strong>dentro</strong> del triángulo.", "The point is <strong>inside</strong> the triangle.")) : T(L3("El punt queda <strong>fora</strong> del triangle.", "El punto queda <strong>fuera</strong> del triángulo.", "The point is <strong>outside</strong> the triangle.")); })();
      out.innerHTML = G(N.it, { W: 300, maxh: 260, pad: 10, box: N.bx }) + gcol([rtex(T(NM[k])), fill(T(L3("Triangle <strong>{a}</strong>.", "Triángulo <strong>{a}</strong>.", "<strong>{a}</strong> triangle.")), { a: T(TANGK[ak]) }) + " " + where]);
    }
    sl.cx.addEventListener("input", paint); segs(w, [function (v) { k = v; paint(); }]); onLang(paint);
  }

  /* ---------- 7.8 quadrilàters ---------- */
  var QD = {
    q: { V: [[0, 0], [2, 0], [2, 2], [0, 2]], n: L3("Quadrat", "Cuadrado", "Square"), p: L3("Paral·lelogram: 4 costats iguals, 4 angles rectes. Diagonals iguals i perpendiculars, que es tallen pel punt mitjà.", "Paralelogramo: 4 lados iguales, 4 ángulos rectos. Diagonales iguales y perpendiculares, que se cortan por el punto medio.", "Parallelogram: 4 equal sides, 4 right angles. Equal, perpendicular diagonals that bisect each other.") },
    r: { V: [[0, 0], [3, 0], [3, 1.8], [0, 1.8]], n: L3("Rectangle", "Rectángulo", "Rectangle"), p: L3("Paral·lelogram: costats oposats iguals, 4 angles rectes. Diagonals iguals (no perpendiculars), que es tallen pel punt mitjà.", "Paralelogramo: lados opuestos iguales, 4 ángulos rectos. Diagonales iguales (no perpendiculares), que se cortan por el punto medio.", "Parallelogram: opposite sides equal, 4 right angles. Equal (not perpendicular) diagonals that bisect each other.") },
    b: { V: [[0, 0], [1.6, -1.1], [3.2, 0], [1.6, 1.1]], n: L3("Rombe", "Rombo", "Rhombus"), p: L3("Paral·lelogram: 4 costats iguals, angles oposats iguals (no rectes). Diagonals perpendiculars (no iguals), que es tallen pel punt mitjà.", "Paralelogramo: 4 lados iguales, ángulos opuestos iguales (no rectos). Diagonales perpendiculares (no iguales), que se cortan por el punto medio.", "Parallelogram: 4 equal sides, opposite angles equal (not right). Perpendicular (unequal) diagonals that bisect each other.") },
    o: { V: [[0, 0], [2.6, 0], [3.5, 1.6], [0.9, 1.6]], n: L3("Romboide", "Romboide", "Parallelogram (rhomboid)"), p: L3("Paral·lelogram: costats oposats iguals i angles oposats iguals. Les diagonals es tallen pel punt mitjà, però no són iguals ni perpendiculars.", "Paralelogramo: lados opuestos iguales y ángulos opuestos iguales. Las diagonales se cortan por el punto medio, pero no son iguales ni perpendiculares.", "Parallelogram: opposite sides and opposite angles equal. The diagonals bisect each other but are neither equal nor perpendicular.") },
    tr: { V: [[0, 0], [3.2, 0], [2.0, 1.8], [0, 1.8]], n: L3("Trapezi rectangle", "Trapecio rectángulo", "Right trapezium"), p: L3("Trapezi: només dues bases paral·leles. Té dos angles rectes.", "Trapecio: solo dos bases paralelas. Tiene dos ángulos rectos.", "Trapezium: only two parallel bases. It has two right angles.") },
    ti: { V: [[0, 0], [3.4, 0], [2.5, 1.7], [0.9, 1.7]], n: L3("Trapezi isòsceles", "Trapecio isósceles", "Isosceles trapezium"), p: L3("Trapezi: només dues bases paral·leles. Els costats no paral·lels són iguals, els angles de cada base són iguals i les diagonals també.", "Trapecio: solo dos bases paralelas. Los lados no paralelos son iguales, los ángulos de cada base son iguales y las diagonales también.", "Trapezium: only two parallel bases. The non-parallel sides are equal, so are the angles at each base, and so are the diagonals.") },
    te: { V: [[0, 0], [3.4, 0], [2.8, 1.7], [0.4, 1.7]], n: L3("Trapezi escalé", "Trapecio escaleno", "Scalene trapezium"), p: L3("Trapezi: només dues bases paral·leles. Els costats no paral·lels són desiguals i no té angles rectes.", "Trapecio: solo dos bases paralelas. Los lados no paralelos son desiguales y no tiene ángulos rectos.", "Trapezium: only two parallel bases. The other two sides are unequal and there are no right angles.") },
    tz: { V: [[0, 0], [2.8, 0.3], [3.4, 2.0], [0.6, 1.4]], n: L3("Trapezoide", "Trapezoide", "Trapezoid (irregular)"), p: L3("No té cap parell de costats paral·lels.", "No tiene ningún par de lados paralelos.", "No pair of parallel sides.") }
  };
  function quadItems(k, diag) {
    var V = QD[k].V, n = 4, it = [["poly", V, "gf"]], s = [], i, grp = {}, t = 1;
    for (i = 0; i < n; i++) s.push(Math.round(dist(V[i], V[(i + 1) % n]) * 1e6) / 1e6);
    s.forEach(function (x, i) { (grp[x] = grp[x] || []).push(i); });
    Object.keys(grp).forEach(function (x) { if (grp[x].length > 1) { grp[x].forEach(function (i) { it.push(["tick", V[i], V[(i + 1) % n], t]); }); t++; } });
    for (i = 0; i < n; i++) if (Math.abs(angAt(V[i], V[(i + 3) % n], V[(i + 1) % n]) - 90) < 1e-6) it.push(["ra", V[i], V[(i + 3) % n], V[(i + 1) % n]]);
    if (diag) { it.push(["seg", V[0], V[2], "hl"], ["seg", V[1], V[3], "hl"]); var P = inter(V[0], [V[2][0] - V[0][0], V[2][1] - V[0][1]], V[1], [V[3][0] - V[1][0], V[3][1] - V[1][1]]); if (P) it.push(["dot", P, "pa"]); }
    return it;
  }
  function wQuad() {
    var w = document.getElementById("w-quad"); if (!w) return;
    var out = w.querySelector(".gout"), k = "q", d = false;
    function paint() {
      var V = QD[k].V, A = V.map(function (P, i) { return angAt(P, V[(i + 3) % 4], V[(i + 1) % 4]); });
      out.innerHTML = G(quadItems(k, d).concat(vnames(V, ["A", "B", "C", "D"], 0.25)), { W: 240, maxh: 180, pad: 20 }) + gcol(["<strong>" + T(QD[k].n) + "</strong>. " + T(QD[k].p),
        tex("\\hat A+\\hat B+\\hat C+\\hat D\\approx" + A.map(function (x) { return Math.round(x); }).join("^\\circ+") + "^\\circ=360^\\circ")]);
    }
    segs(w, [function (v) { k = v; paint(); }, function (v) { d = v === "d"; paint(); }]); onLang(paint);
  }

  /* ---------- 7.9 angles dels polígons regulars ---------- */
  function wPoly() {
    var w = document.getElementById("w-poly"); if (!w) return;
    var sl = sliders(w), out = w.querySelector(".gout"), m = "t";
    function paint() {
      var n = +sl.n.value, V = reg(n, 1.6), it = [["poly", V, "gf"]], S = (n - 2) * 180, j;
      showRv(w, "n", "n", n);
      if (m === "t") { for (j = 2; j < n - 1; j++) it.push(["seg", V[0], V[j], "hl"]); for (j = 1; j < n - 1; j++) it.push(T_([(V[0][0] + V[j][0] + V[j + 1][0]) / 3, (V[0][1] + V[j][1] + V[j + 1][1]) / 3], String(j), { cls: "hot" })); }
      else if (m === "c") { V.forEach(function (P) { it.push(["seg", [0, 0], P, "thin"]); }); it.push(["sect", [0, 0], 0.5, dirn([0, 0], V[0]), dirn([0, 0], V[0]) + 360 / n, "af"], ["seg", [0, 0], V[0], "hl"], ["seg", [0, 0], V[1], "hl"], ["dot", [0, 0]], amark(V[1], V[0], V[2], 0.4, "af2")); }
      else { var M = mid(V[0], V[1]); it.push(["circ", [0, 0], 1.6, "gc dd"], ["seg", [0, 0], V[1], "hl"], ["seg", [0, 0], M, "ch"], ["ra", M, V[1], [0, 0]], ["dot", [0, 0]], T_([0, 0], "O", { dy: -8 }), T_(mid([0, 0], V[1]), "r", { dx: 8, cls: "hot" }), T_(mid([0, 0], M), "a", { dx: -9, cls: "hot" })); }
      var inn = S / n, rows = [fill(T(L3("<strong>{N} regular</strong> ({n} costats)", "<strong>{N} regular</strong> ({n} lados)", "<strong>Regular {N}</strong> ({n} sides)")), { N: lang === "en" ? T(PN[n]) : T(PN[n]).charAt(0).toUpperCase() + T(PN[n]).slice(1), n: n }),
        T(L3("Suma dels angles:", "Suma de los ángulos:", "Angle sum:")) + " " + tex("(" + n + "-2)\\cdot180^\\circ=" + (n - 2) + "\\cdot180^\\circ=" + S + "^\\circ"),
        T(L3("Cada angle interior:", "Cada ángulo interior:", "Each interior angle:")) + " " + tex("\\dfrac{" + S + "^\\circ}{" + n + "}" + (isInt(inn) ? "=" + inn + "^\\circ" : "\\approx " + d2(inn) + "^\\circ")),
        T(L3("Angle central:", "Ángulo central:", "Central angle:")) + " " + tex("\\dfrac{360^\\circ}{" + n + "}" + (isInt(360 / n) ? "=" + 360 / n + "^\\circ" : "\\approx " + d2(360 / n) + "^\\circ"))];
      if (m === "t") rows.splice(1, 0, fill(T(L3("Les diagonals d'un vèrtex el dividixen en {t} triangles.", "Las diagonales de un vértice lo dividen en {t} triángulos.", "The diagonals from one vertex split it into {t} triangles.")), { t: n - 2 }));
      if (isInt(360 / inn)) rows.push("✔ " + fill(T(L3("Es pot fer un mosaic amb aquests polígons: {k} angles de {a} fan 360°.", "Se puede hacer un mosaico con estos polígonos: {k} ángulos de {a} suman 360°.", "These polygons tile the plane: {k} angles of {a} make 360°.")), { k: 360 / inn, a: inn + "°" }));
      out.innerHTML = G(it, { W: 230, maxh: 230, pad: 14 }) + gcol(rows);
    }
    sl.n.addEventListener("input", paint); segs(w, [function (v) { m = v; paint(); }]); onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function optsTxt(right, wrongs) {
    var all = [right].concat(wrongs), order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return all[i]; }), ans: order.indexOf(0) };
  }
  function ret(o, q, s) { o.q = q; o.s = s; return o; }
  function numQ(v, tol) { return { num: v, tol: tol || 1e-6 }; }
  function sxQ(t) { return { sx: t }; }
  function rsx(withSec) { return rint(1, 170) * 3600 + rint(1, 59) * 60 + (withSec ? rint(1, 59) : 0); }
  var GEN = {
    elem: function () {
      var k = pick(["r", "s", "g"]), a = rint(-30, 30), it, sw = rint(0, 1);
      var A = pol([0, 0], 1, a + 180), B = pol([0, 0], 1, a), F = pol([0, 0], 2.2, a + 180), E = pol([0, 0], 2.2, a);
      if (sw) { var t = A; A = B; B = t; t = F; F = E; E = t; }
      it = k === "r" ? [["ln", F, E, "", "b"]] : k === "s" ? [["ln", A, E, "", "e"]] : [["seg", A, B, ""], T_(F, " "), T_(E, " ")];
      it.push(["dot", A], T_(A, "A", { dy: -10 }), ["dot", B], T_(B, "B", { dy: -10 }));
      var R = { r: W_.recta, s: W_.semi, g: W_.seg }, o = optsTxt(R[k], ["r", "s", "g"].filter(function (x) { return x !== k; }).map(function (x) { return R[x]; }));
      return ret(o, function () { return T(L3("Què és aquesta figura?", "¿Qué es esta figura?", "What is this figure?")) + G(it, { W: 240, maxh: 110, pad: 16 }); },
        function () { return "<strong>" + T(R[k]) + "</strong>: " + T(k === "r" ? L3("no té principi ni final (dues fletxes).", "no tiene principio ni final (dos flechas).", "no beginning or end (two arrows).") : k === "s" ? L3("té origen però no té final (una fletxa).", "tiene origen pero no final (una flecha).", "it has a start but no end (one arrow).") : L3("té dos extrems.", "tiene dos extremos.", "it has two endpoints.")); });
    },
    pos: function () {
      var k = pick(["sec", "par", "perp"]), base = rint(-40, 40), a, d;
      if (k === "par") { a = 0; d = pick([-1.6, -1, 1, 1.6]); } else if (k === "perp") { a = 90; d = rint(-1, 1) * 0.5; } else { a = pick([25, 35, 50, 60, 120, 135, 150]); d = rint(-1, 1) * 0.5; }
      var it = twoLines(a, d, false).filter(function (x) { return x[0] !== "ra" && x[0] !== "sect" && x[0] !== "dot"; }).map(function (x) {
        function rot(P) { var c = Math.cos(base * Math.PI / 180), s = Math.sin(base * Math.PI / 180); return [P[0] * c - P[1] * s, P[0] * s + P[1] * c]; }
        return x[0] === "ln" ? ["ln", rot(x[1]), rot(x[2]), "", "b"] : x;
      });
      if (k === "perp") { var c = Math.cos(base * Math.PI / 180), s = Math.sin(base * Math.PI / 180); it.push(["ra", [0, 0], [c, s], [-s, c]]); }
      var o = optsTxt(W_[k], ["sec", "par", "perp"].filter(function (x) { return x !== k; }).map(function (x) { return W_[x]; }));
      return ret(o, function () { return T(L3("Com són aquestes dues rectes?", "¿Cómo son estas dos rectas?", "How are these two lines related?")) + G(it, { W: 260, maxh: 170, pad: 8 }); },
        function () { return "<strong>" + T(W_[k]) + "</strong>"; });
    },
    cls: function () {
      var k = rint(1, 5), a = [0, rint(5, 85), 90, rint(95, 175), 180, rint(190, 350)][k], fig = rint(0, 1);
      var o = optsTxt(ANGK[k], shuffle([1, 2, 3, 4, 5].filter(function (x) { return x !== k; })).slice(0, 3).map(function (x) { return ANGK[x]; }));
      return ret(o, function () { return fig ? T(L3("Com és aquest angle?", "¿Cómo es este ángulo?", "What type of angle is this?")) + G(angItems([0, 0], rint(0, 3) * 15, a, 1.8, 0.5).concat([T_([-1.9, -1.9], " "), T_([1.9, 1.9], " ")]), { W: 170, maxh: 170, pad: 8 }) : fill(T(L3("Com és un angle de {a}?", "¿Cómo es un ángulo de {a}?", "What type of angle is {a}?")), { a: "$" + a + "^\\circ$" }); },
        function () { return fill(T(L3("{a} és <strong>{k}</strong>.", "{a} es <strong>{k}</strong>.", "{a} is <strong>{k}</strong>.")), { a: tex(a + "^\\circ"), k: T(ANGK[k]) }); });
    },
    sxs: function () {
      var d = rint(0, 45), m = rint(1, 59), s = rint(0, 59), t = d * 3600 + m * 60 + s;
      return ret(numQ(t), function () { return fill(T(L3("Expressa en segons: {a}", "Expresa en segundos: {a}", "Write in seconds: {a}")), { a: "$" + d + "^\\circ\\," + m + "'\\," + s + "''$" }); }, function () { return toSecSteps(d, m, s)[0]; });
    },
    sxc: function () {
      var u = rint(0, 2) ? "s" : "m", n = u === "s" ? rint(3700, 40000) : rint(70, 900);
      return ret(sxQ(u === "s" ? n : n * 60), function () { return fill(T(L3("Passa a forma complexa: {a}", "Pasa a forma compleja: {a}", "Write in compound form: {a}")), { a: "$" + n + (u === "s" ? "''" : "'") + "$" }); }, function () { return toCplxSteps(n, u).join("<br>"); });
    },
    sxop: function () {
      var op = pick(["+", "-", "*", "/"]), A, B, k, R, st;
      if (op === "+") { A = rsx(rint(0, 1)); B = rsx(rint(0, 1)); R = A + B; st = function () { return sxAdd(A, B).join("<br>"); }; }
      else if (op === "-") { A = rsx(rint(0, 1)); B = rsx(rint(0, 1)); if (B > A) { var t = A; A = B; B = t; } if (A === B) A += 3600; R = A - B; st = function () { return sxSub(A, B).join("<br>"); }; }
      else if (op === "*") { k = rint(2, 6); A = rint(5, 50) * 3600 + rint(1, 59) * 60 + rint(0, 59); R = A * k; st = function () { return sxMul(A, k).join("<br>"); }; }
      else { k = rint(2, 6); R = rint(5, 50) * 3600 + rint(0, 59) * 60 + rint(0, 59); A = R * k; st = function () { return sxDiv(A, k).join("<br>"); }; }
      var qt = op === "+" ? sxT(A) + "+" + sxT(B) : op === "-" ? sxT(A) + "-" + sxT(B) : op === "*" ? "(" + sxT(A) + ")\\cdot" + k : "(" + sxT(A) + "):" + k;
      return ret(sxQ(R), function () { return fill(T(L3("Calcula: {a}", "Calcula: {a}", "Work out: {a}")), { a: "$" + qt + "$" }); }, st);
    },
    cs: function () {
      var c = rint(0, 1), wm = rint(0, 1), tot = c ? 90 : 180, a = (c ? rint(5, 85) : rint(5, 175)) * 3600 + (wm ? rint(1, 59) * 60 : 0);
      return ret(sxQ(tot * 3600 - a), function () { return fill(T(c ? L3("Calcula el complementari de {a}.", "Calcula el complementario de {a}.", "Find the complement of {a}.") : L3("Calcula el suplementari de {a}.", "Calcula el suplementario de {a}.", "Find the supplement of {a}.")), { a: "$" + sxT(a) + "$" }); },
        function () { return tex(tot + "^\\circ-" + sxT(a) + (wm ? "=" + (tot - 1) + "^\\circ\\,60'-" + sxT(a) : "") + "=" + sxT(tot * 3600 - a)); });
    },
    par: function () {
      var a = pick([35, 40, 50, 55, 60, 65, 70, 75, 110, 115, 120, 130]), g = rint(1, 8), x; do { x = rint(1, 8); } while (x === g);
      var v = parVal(a, x), gv = parVal(a, g);
      return ret(numQ(v), function () { return T(L3("Les rectes $r$ i $s$ són paral·leles. Quant mesura l'angle $x$?", "Las rectas $r$ y $s$ son paralelas. ¿Cuánto mide el ángulo $x$?", "Lines $r$ and $s$ are parallel. How big is angle $x$?")) + G(parItems(a, null, false, g, x), { W: 280, maxh: 170, pad: 12 }); },
        function () { return (v === gv ? T(L3("És igual que l'angle conegut", "Es igual que el ángulo conocido", "It equals the known angle")) + ": " + tex("x=" + v + "^\\circ") : T(L3("És el suplementari de l'angle conegut", "Es el suplementario del ángulo conocido", "It's the supplement of the known angle")) + ": " + tex("x=180^\\circ-" + gv + "^\\circ=" + v + "^\\circ")); });
    },
    pname: function () {
      var t = rint(0, 1), n = rint(3, 12);
      if (t === 0) {
        var o = optsTxt(PN[n], shuffle(Object.keys(PN).filter(function (x) { return +x !== n; })).slice(0, 3).map(function (x) { return PN[x]; }));
        return ret(o, function () { return fill(T(L3("Com s'anomena el polígon de {n} costats?", "¿Cómo se llama el polígono de {n} lados?", "What's the name of the {n}-sided polygon?")), { n: n }); }, function () { return "<strong>" + T(PN[n]) + "</strong>"; });
      }
      n = rint(4, 12); var d = n * (n - 3) / 2, wr = shuffle([n * (n - 3), n - 3, n * (n - 1) / 2, d + n, Math.max(1, d - n)].filter(function (x, i, a) { return x !== d && a.indexOf(x) === i; })).slice(0, 3);
      var o2 = optsTxt(L3(String(d), String(d), String(d)), wr.map(function (x) { return L3(String(x), String(x), String(x)); }));
      return ret(o2, function () { return fill(T(L3("Quantes diagonals té un {p}?", "¿Cuántas diagonales tiene un {p}?", "How many diagonals does a {p} have?")), { p: T(PN[n]) }); }, function () { return tex("\\dfrac{" + n + "\\cdot" + (n - 3) + "}{2}=" + d); });
    },
    tang: function () {
      var t = rint(0, 3), a, b, c;
      if (t === 0) { do { a = rint(20, 110); b = rint(20, 110); } while (a + b > 165); c = 180 - a - b;
        return ret(numQ(c), function () { return fill(T(L3("Dos angles d'un triangle fan {a} i {b}. Quant fa el tercer?", "Dos ángulos de un triángulo miden {a} y {b}. ¿Cuánto mide el tercero?", "Two angles of a triangle are {a} and {b}. What's the third?")), { a: "$" + a + "^\\circ$", b: "$" + b + "^\\circ$" }) + G(triItems(triFromAngles(a, b, 4), { names: ["", "", ""] }).concat([T_(pol([0, 0], 0.85, a / 2), a + "°", { cls: "hot" }), T_(pol([4, 0], 0.85, 180 - b / 2), b + "°", { cls: "hot" })]), { W: 220, maxh: 140, pad: 14 }); },
          function () { return tex("180^\\circ-(" + a + "^\\circ+" + b + "^\\circ)=" + c + "^\\circ"); }); }
      if (t === 1) { a = rint(20, 70);
        return ret(numQ(90 - a), function () { return fill(T(L3("Un angle agut d'un triangle rectangle fa {a}. Quant fa l'altre angle agut?", "Un ángulo agudo de un triángulo rectángulo mide {a}. ¿Cuánto mide el otro ángulo agudo?", "One acute angle of a right triangle is {a}. What's the other acute angle?")), { a: "$" + a + "^\\circ$" }); }, function () { return tex("90^\\circ-" + a + "^\\circ=" + (90 - a) + "^\\circ"); }); }
      if (t === 2) { a = 2 * rint(10, 80);
        return ret(numQ((180 - a) / 2), function () { return fill(T(L3("En un triangle isòsceles, l'angle desigual fa {a}. Quant fa cadascun dels altres dos?", "En un triángulo isósceles, el ángulo desigual mide {a}. ¿Cuánto mide cada uno de los otros dos?", "In an isosceles triangle the odd angle is {a}. How big is each of the other two?")), { a: "$" + a + "^\\circ$" }); }, function () { return tex("(180^\\circ-" + a + "^\\circ):2=" + (180 - a) / 2 + "^\\circ"); }); }
      a = rint(20, 80);
      return ret(numQ(180 - 2 * a), function () { return fill(T(L3("En un triangle isòsceles, cada angle de la base fa {a}. Quant fa l'angle desigual?", "En un triángulo isósceles, cada ángulo de la base mide {a}. ¿Cuánto mide el ángulo desigual?", "In an isosceles triangle each base angle is {a}. What's the odd angle?")), { a: "$" + a + "^\\circ$" }); }, function () { return tex("180^\\circ-2\\cdot" + a + "^\\circ=" + (180 - 2 * a) + "^\\circ"); });
    },
    tcls: function () {
      var t = rint(0, 2);
      if (t === 0) {
        var k = rint(0, 2), a = rint(3, 12), b = a, c = a;
        if (k === 1) { do { c = rint(2, 2 * a - 1); } while (c === a); } else if (k === 2) { do { b = rint(3, 12); c = rint(3, 12); } while (b === a || c === a || b === c || Math.max(a, b, c) * 2 >= a + b + c); }
        var s = shuffle([a, b, c]), o = optsTxt(SIDEK[k], SIDEK.filter(function (_, i) { return i !== k; }));
        return ret(o, function () { return fill(T(L3("Com és, segons els costats, un triangle de costats {s} cm?", "¿Cómo es, según sus lados, un triángulo de lados {s} cm?", "What kind of triangle (by its sides) has sides {s} cm?")), { s: "$" + s.join(",\\ ") + "$" }); }, function () { return "<strong>" + T(SIDEK[k]) + "</strong>"; });
      }
      if (t === 1) {
        var A, B, C, kk = rint(0, 2);
        do { A = rint(15, 120); B = rint(15, 120); C = 180 - A - B; } while (C < 10 || angKindT([A, B, C]) !== kk && kk !== 1);
        if (kk === 1) { A = 90; B = rint(15, 75); C = 90 - B; }
        var ang = shuffle([A, B, C]), o1 = optsTxt(TANGK[kk], TANGK.filter(function (_, i) { return i !== kk; }));
        return ret(o1, function () { return fill(T(L3("Els angles d'un triangle fan {s}. Com és segons els angles?", "Los ángulos de un triángulo miden {s}. ¿Cómo es según sus ángulos?", "A triangle's angles are {s}. What type is it by its angles?")), { s: "$" + ang.join("^\\circ,\\ ") + "^\\circ$" }); }, function () { return "<strong>" + T(TANGK[kk]) + "</strong>"; });
      }
      var S; do { S = [rint(2, 12), rint(2, 12), rint(2, 12)]; } while (S[0] === S[1] && S[1] === S[2]);
      var srt = S.slice().sort(function (x, y) { return x - y; }), ok = srt[2] < srt[0] + srt[1];
      var YN = [L3("Sí", "Sí", "Yes"), L3("No", "No", "No")], o2 = optsTxt(YN[ok ? 0 : 1], [YN[ok ? 1 : 0]]);
      return ret(o2, function () { return fill(T(L3("Es pot construir un triangle amb costats de {s} cm?", "¿Se puede construir un triángulo con lados de {s} cm?", "Can a triangle be built with sides of {s} cm?")), { s: "$" + S.join(",\\ ") + "$" }); },
        function () { return tex(srt[2] + (ok ? "<" : "\\ge ") + srt[0] + "+" + srt[1] + "=" + (srt[0] + srt[1])) + " → <strong>" + T(YN[ok ? 0 : 1]) + "</strong>"; });
    },
    quad: function () {
      var P = [["q", L3("Té els 4 costats iguals i els 4 angles rectes.", "Tiene los 4 lados iguales y los 4 ángulos rectos.", "It has 4 equal sides and 4 right angles.")],
        ["r", L3("És un paral·lelogram amb els 4 angles rectes, però no té els 4 costats iguals.", "Es un paralelogramo con los 4 ángulos rectos, pero no tiene los 4 lados iguales.", "It's a parallelogram with 4 right angles, but its 4 sides aren't all equal.")],
        ["b", L3("Té els 4 costats iguals, però els angles no són rectes.", "Tiene los 4 lados iguales, pero los ángulos no son rectos.", "It has 4 equal sides, but its angles aren't right angles.")],
        ["o", L3("Els costats oposats són paral·lels i iguals, però no té angles rectes ni els 4 costats iguals.", "Los lados opuestos son paralelos e iguales, pero no tiene ángulos rectos ni los 4 lados iguales.", "Opposite sides are parallel and equal, but no right angles and not all sides equal.")],
        ["tr", L3("Només té dos costats paral·lels i dos angles rectes.", "Solo tiene dos lados paralelos y dos ángulos rectos.", "Only two sides are parallel and it has two right angles.")],
        ["ti", L3("Només té dos costats paral·lels i els altres dos són iguals.", "Solo tiene dos lados paralelos y los otros dos son iguales.", "Only two sides are parallel and the other two are equal.")],
        ["tz", L3("No té cap parell de costats paral·lels.", "No tiene ningún par de lados paralelos.", "No pair of sides is parallel.")]], p = pick(P), fig = rint(0, 1);
      var o = optsTxt(QD[p[0]].n, shuffle(P.filter(function (x) { return x[0] !== p[0]; })).slice(0, 3).map(function (x) { return QD[x[0]].n; }));
      return ret(o, function () { return fig ? T(L3("Quin quadrilàter és?", "¿Qué cuadrilátero es?", "Which quadrilateral is it?")) + G(quadItems(p[0], false), { W: 200, maxh: 130, pad: 12 }) : T(L3("Quin quadrilàter és?", "¿Qué cuadrilátero es?", "Which quadrilateral is it?")) + " " + T(p[1]); },
        function () { return "<strong>" + T(QD[p[0]].n) + "</strong>. " + T(QD[p[0]].p); });
    },
    qang: function () {
      var t = rint(0, 2), a, b, c, d;
      if (t === 0) { do { a = rint(50, 140); b = rint(50, 140); c = rint(50, 140); d = 360 - a - b - c; } while (d < 30 || d > 170);
        return ret(numQ(d), function () { return fill(T(L3("Tres angles d'un quadrilàter fan {a}, {b} i {c}. Quant fa el quart?", "Tres ángulos de un cuadrilátero miden {a}, {b} y {c}. ¿Cuánto mide el cuarto?", "Three angles of a quadrilateral are {a}, {b} and {c}. What's the fourth?")), { a: "$" + a + "^\\circ$", b: "$" + b + "^\\circ$", c: "$" + c + "^\\circ$" }); }, function () { return tex("360^\\circ-(" + a + "^\\circ+" + b + "^\\circ+" + c + "^\\circ)=" + d + "^\\circ"); }); }
      a = rint(30, 80); var nm = t === 1 ? pick([L3("rombe", "rombo", "rhombus"), L3("romboide", "romboide", "parallelogram")]) : L3("trapezi isòsceles", "trapecio isósceles", "isosceles trapezium");
      return ret(numQ(180 - a), function () { return fill(T(L3("Un angle agut d'un {q} fa {a}. Quant fa cadascun dels angles obtusos?", "Un ángulo agudo de un {q} mide {a}. ¿Cuánto mide cada uno de los ángulos obtusos?", "An acute angle of a {q} is {a}. How big is each obtuse angle?")), { q: T(nm), a: "$" + a + "^\\circ$" }); },
        function () { return tex("(360^\\circ-2\\cdot" + a + "^\\circ):2=" + (180 - a) + "^\\circ"); });
    },
    poly: function () {
      var t = rint(0, 3), n = pick([5, 6, 8, 9, 10, 12, 15, 18, 20]), S = (n - 2) * 180;
      if (t === 0) return ret(numQ(S), function () { return fill(T(L3("Quant sumen els angles interiors d'un polígon de {n} costats?", "¿Cuánto suman los ángulos interiores de un polígono de {n} lados?", "What do the interior angles of a {n}-sided polygon add up to?")), { n: n }); }, function () { return tex("(" + n + "-2)\\cdot180^\\circ=" + S + "^\\circ"); });
      if (t === 1) return ret(numQ(S / n), function () { return fill(T(L3("Quant fa cada angle interior d'un polígon regular de {n} costats?", "¿Cuánto mide cada ángulo interior de un polígono regular de {n} lados?", "How big is each interior angle of a regular {n}-sided polygon?")), { n: n }); }, function () { return tex("\\dfrac{(" + n + "-2)\\cdot180^\\circ}{" + n + "}=\\dfrac{" + S + "^\\circ}{" + n + "}=" + S / n + "^\\circ"); });
      if (t === 2) return ret(numQ(360 / n), function () { return fill(T(L3("Quant fa l'angle central d'un polígon regular de {n} costats?", "¿Cuánto mide el ángulo central de un polígono regular de {n} lados?", "How big is the central angle of a regular {n}-sided polygon?")), { n: n }); }, function () { return tex("360^\\circ:" + n + "=" + 360 / n + "^\\circ"); });
      return ret(numQ(n), function () { return fill(T(L3("Cada angle interior d'un polígon regular fa {a}. Quants costats té?", "Cada ángulo interior de un polígono regular mide {a}. ¿Cuántos lados tiene?", "Each interior angle of a regular polygon is {a}. How many sides does it have?")), { a: "$" + S / n + "^\\circ$" }); },
        function () { return T(L3("Angle central", "Ángulo central", "Central angle")) + ": " + tex("180^\\circ-" + S / n + "^\\circ=" + 360 / n + "^\\circ") + "; " + tex("n=360:" + 360 / n + "=" + n); });
    }
  };

  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore"), ob = w.querySelector(".dopts");
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
        if (q.sx != null) {
          var t = sxIn(inp.value); if (t === null) { info.innerHTML = warn(u("sx")); return; }
          good = Math.abs(t - q.sx) < 1e-6 && sxOk(inp.value);
        } else {
          var v = numIn(inp.value); if (v === null) { info.innerHTML = warn(u("num")); return; }
          good = Math.abs(v - q.num) <= (q.tol || 1e-6);
        }
      }
      done = true; tot++; res = { good: good, pick: j }; if (good) ok++;
      paint();
    }
    function fresh() { q = GEN[kind](); done = false; if (inp) inp.value = ""; info.innerHTML = ""; paint(); }
    var cb = w.querySelector('[data-a="check"]'); if (cb) cb.addEventListener("click", function () { check(); });
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); if (inp) inp.focus(); });
    if (inp) inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }
  window.FM17 = { G: G, GEN: GEN, sxIn: sxIn, sxOk: sxOk, sxT: sxT, sxAdd: sxAdd, sxSub: sxSub, sxMul: sxMul, sxDiv: sxDiv, notable: notable, triFromSides: triFromSides, triAngles: triAngles, numIn: numIn };

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

  var TITLES = { va: "Geometria bàsica del pla · FentMates", es: "Geometría básica del plano · FentMates", en: "Basic plane geometry · FentMates" };
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
    wElem(); wNpts(); wPos(); wMedi(); wAng(); wSexa(); wSexop(); wComp(); wPar(); wDiag(); wTsum(); wTri(); wNotable(); wQuad(); wPoly();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
