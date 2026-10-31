(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-3eso-u11-done", NSEC = 8;

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


  /* ======================================================================
     unitat 11
     ====================================================================== */
  function isInt(v) { return Math.abs(v - Math.round(v)) < 1e-9; }
  /* nombre amb fins a 4 decimals (per als quadrats: 1,4² = 1,96) */
  function n4(v) { var r = Math.round(v * 10000) / 10000; if (near(r, 0)) r = 0; return String(r).replace(".", "\\dc "); }
  function d2(v) { return (Math.round(v * 100) / 100).toFixed(2).replace(".", "\\dc "); }
  /* "= 5" si és exacte, "≈ 8,60" si no */
  function ap(v) { return isInt(v) ? "=" + nf(Math.round(v)) : "\\approx " + d2(v); }
  function rt(v) { return "\\sqrt{" + n4(v) + "}" + ap(Math.sqrt(v)); }
  function lab(v) { var s = String(Math.round(v * 100) / 100); return lang === "en" ? s : s.replace(".", ","); }
  function pol(C, r, a) { return [C[0] + r * Math.cos(a * Math.PI / 180), C[1] + r * Math.sin(a * Math.PI / 180)]; }
  function mid(A, B, f) { f = f == null ? 0.5 : f; return [A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f]; }
  /* punt mitjà de AB desplaçat d cap a l'esquerra (mirant d'A a B) */
  function off(A, B, d) { var M = mid(A, B), dx = B[0] - A[0], dy = B[1] - A[1], n = Math.hypot(dx, dy); return [M[0] - dy / n * d, M[1] + dx / n * d]; }
  var PI = Math.PI;
  function tolOf(v, pi) { return pi ? Math.max(0.011, 0.0006 * Math.abs(v)) : 0.011; }

  /* ---------- figures geomètriques (SVG) ----------
     ["poly", pts, cls] · ["seg", A, B, cls] · ["ra", V, A, B] · ["txt", P, text, {dx, dy, a, cls}]
     ["circ", C, r, cls] · ["sect", C, r, a0, a1, cls] · ["arc", C, r, a0, a1, cls] · ["lens", A, B, r, cls] · ["dot", P, cls] */
  function G(items, o) {
    o = o || {}; var W = o.W || 300, pad = o.pad || 18, maxh = o.maxh || 260, xs = [], ys = [];
    items.forEach(function (it) {
      var k = it[0];
      if (k === "poly" || k === "pl") it[1].forEach(function (p) { xs.push(p[0]); ys.push(p[1]); });
      else if (k === "seg") { xs.push(it[1][0], it[2][0]); ys.push(it[1][1], it[2][1]); }
      else if (k === "circ") { xs.push(it[1][0] - it[2], it[1][0] + it[2]); ys.push(it[1][1] - it[2], it[1][1] + it[2]); }
      else if (k === "sect" || k === "arc") {
        for (var j = 0; j <= 40; j++) { var P = pol(it[1], it[2], it[3] + (it[4] - it[3]) * j / 40); xs.push(P[0]); ys.push(P[1]); }
        if (k === "sect") { xs.push(it[1][0]); ys.push(it[1][1]); }
      } else if (k === "dot" || k === "txt") { xs.push(it[1][0]); ys.push(it[1][1]); }
    });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var s = Math.min((W - 2 * pad) / Math.max(x1 - x0, 1e-9), (maxh - 2 * pad) / Math.max(y1 - y0, 1e-9));
    var Wd = Math.round((x1 - x0) * s + 2 * pad), H = Math.round((y1 - y0) * s + 2 * pad);
    function X(v) { return +((v - x0) * s + pad).toFixed(1); }
    function Y(v) { return +(H - ((v - y0) * s + pad)).toFixed(1); }
    function pts(a) { return a.map(function (p) { return X(p[0]) + "," + Y(p[1]); }).join(" "); }
    function arcTo(C, r, a0, a1) { var B = pol(C, r, a1), big = ((a1 - a0) % 360 + 360) % 360 > 180 ? 1 : 0, rr = +(r * s).toFixed(1); return "A" + rr + " " + rr + " 0 " + big + " 0 " + X(B[0]) + " " + Y(B[1]); }
    var g = "", t = "";
    items.forEach(function (it) {
      var k = it[0], c;
      if (k === "pl") g += '<polyline class="gs ' + (it[2] || "") + '" fill="none" points="' + pts(it[1]) + '"/>';
      else if (k === "poly") g += '<polygon class="gp ' + (it[2] || "") + '" points="' + pts(it[1]) + '"/>';
      else if (k === "seg") g += '<line class="gs ' + (it[3] || "") + '" x1="' + X(it[1][0]) + '" y1="' + Y(it[1][1]) + '" x2="' + X(it[2][0]) + '" y2="' + Y(it[2][1]) + '"/>';
      else if (k === "ra") {
        var V = it[1], q = 9 / s;
        var u = [it[2], it[3]].map(function (P) { var dx = P[0] - V[0], dy = P[1] - V[1], n = Math.hypot(dx, dy); return [dx / n * q, dy / n * q]; });
        g += '<polyline class="gra" points="' + pts([[V[0] + u[0][0], V[1] + u[0][1]], [V[0] + u[0][0] + u[1][0], V[1] + u[0][1] + u[1][1]], [V[0] + u[1][0], V[1] + u[1][1]]]) + '"/>';
      } else if (k === "circ") g += '<circle class="gp ' + (it[3] || "") + '" cx="' + X(it[1][0]) + '" cy="' + Y(it[1][1]) + '" r="' + (it[2] * s).toFixed(1) + '"/>';
      else if (k === "sect") { c = pol(it[1], it[2], it[3]); g += '<path class="gp ' + (it[5] || "") + '" d="M' + X(it[1][0]) + " " + Y(it[1][1]) + "L" + X(c[0]) + " " + Y(c[1]) + arcTo(it[1], it[2], it[3], it[4]) + 'Z"/>'; }
      else if (k === "arc") { c = pol(it[1], it[2], it[3]); g += '<path class="garc ' + (it[5] || "") + '" d="M' + X(c[0]) + " " + Y(c[1]) + arcTo(it[1], it[2], it[3], it[4]) + '"/>'; }
      else if (k === "lens") { var rr = (it[3] * s).toFixed(1); g += '<path class="gp ' + (it[4] || "") + '" d="M' + X(it[1][0]) + " " + Y(it[1][1]) + "A" + rr + " " + rr + " 0 0 1 " + X(it[2][0]) + " " + Y(it[2][1]) + "A" + rr + " " + rr + " 0 0 1 " + X(it[1][0]) + " " + Y(it[1][1]) + 'Z"/>'; }
      else if (k === "dot") g += '<circle class="gd ' + (it[2] || "") + '" cx="' + X(it[1][0]) + '" cy="' + Y(it[1][1]) + '" r="3.5"/>';
      else if (k === "txt") { var op = it[3] || {}; t += '<text class="gt ' + (op.cls || "") + '" x="' + (X(it[1][0]) + (op.dx || 0)).toFixed(1) + '" y="' + (Y(it[1][1]) + (op.dy == null ? 4 : op.dy)).toFixed(1) + '" text-anchor="' + (op.a || "middle") + '">' + it[2] + "</text>"; }
    });
    return '<svg class="gfig" viewBox="0 0 ' + Wd + " " + H + '" style="max-width:' + Wd + 'px" role="img" aria-label="figura">' + g + t + "</svg>";
  }
  function T_(P, s, o) { return ["txt", P, s, o || {}]; }

  /* ---------- lectura dels controls ---------- */
  function sliders(w) { var o = {}; w.querySelectorAll('input[type="range"]').forEach(function (i) { o[i.dataset.k] = i; }); return o; }
  function showRv(w, k, name, v) { var e = w.querySelector("." + k + "v"); if (e) e.innerHTML = tex(name + "=" + nf(v)); }
  function showRange(w, k, on) { var i = w.querySelector('input[data-k="' + k + '"]'); if (i) i.closest("label").style.display = on ? "" : "none"; }
  function gcol(rows) { return '<div class="gcol">' + rows.map(function (r) { return "<p>" + r + "</p>"; }).join("") + "</div>"; }

  function eq(v) { return Math.abs(v * 1000 - Math.round(v * 1000)) < 1e-6 ? "=" + nf(v) : "\\approx " + d2(v); }
  /* nombre per a substituir en una fórmula: exacte si té pocs decimals, si no arrodonit */
  function fm(v) { return Math.abs(v * 1000 - Math.round(v * 1000)) < 1e-6 ? nf(v) : d2(v); }
  function $n(v) { return "$" + nf(v) + "$"; }
  /* "= 15π ≈ 47,12" */
  function piv(k) { return (near(k, 1) ? "" : nf(k)) + "\\pi\\approx " + d2(k * PI); }

  /* ======================================================================
     cossos en perspectiva (còpia de solids.py)
     ====================================================================== */
  var V3 = { th: -28, ph: 22 };
  function proj(p, th, ph) {
    var t = th * PI / 180, f = ph * PI / 180, d = p[0] * Math.sin(t) + p[1] * Math.cos(t);
    return [p[0] * Math.cos(t) - p[1] * Math.sin(t), p[2] * Math.cos(f) + d * Math.sin(f)];
  }
  function towards(th, ph) { var t = th * PI / 180, f = ph * PI / 180; return [-Math.cos(f) * Math.sin(t), -Math.cos(f) * Math.cos(t), Math.sin(f)]; }
  function vsub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function vdot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function vcross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function vcen(P) { var c = [0, 0, 0]; P.forEach(function (p) { c[0] += p[0]; c[1] += p[1]; c[2] += p[2]; }); return [c[0] / P.length, c[1] / P.length, c[2] / P.length]; }
  function hullFaces(V) {
    var faces = [], seen = {}, n = V.length, i, j, k;
    for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) for (k = j + 1; k < n; k++) {
      var nn = vcross(vsub(V[j], V[i]), vsub(V[k], V[i])); if (vdot(nn, nn) < 1e-12) continue;
      var s = V.map(function (p) { return vdot(nn, vsub(p, V[i])); }), mx = Math.max.apply(null, s), mn = Math.min.apply(null, s);
      if (mx > 1e-7 && mn < -1e-7) continue;
      var f = []; s.forEach(function (v, q) { if (Math.abs(v) <= 1e-7) f.push(q); });
      var key = f.join(","); if (seen[key]) continue; seen[key] = 1;
      var c = vcen(f.map(function (q) { return V[q]; })), L = Math.sqrt(vdot(nn, nn)), u = [nn[0] / L, nn[1] / L, nn[2] / L], a = vsub(V[f[0]], c), b = vcross(u, a);
      f.sort(function (p, q) { var dp = vsub(V[p], c), dq = vsub(V[q], c); return Math.atan2(vdot(dp, b), vdot(dp, a)) - Math.atan2(vdot(dq, b), vdot(dq, a)); });
      faces.push(f);
    }
    return faces;
  }
  function polyhedron(V, th, ph, F) {
    F = F || hullFaces(V); var c = vcen(V), w = towards(th, ph), front = [], E = {}, it = [];
    F.forEach(function (f) { var P = f.map(function (q) { return V[q]; }), n = vcross(vsub(P[1], P[0]), vsub(P[2], P[0])); if (vdot(n, vsub(vcen(P), c)) < 0) n = n.map(function (x) { return -x; }); front.push(vdot(n, w) > 1e-9); });
    F.forEach(function (f, fi) { f.forEach(function (a, i) { var b = f[(i + 1) % f.length], key = Math.min(a, b) + "," + Math.max(a, b); (E[key] = E[key] || []).push(front[fi]); }); });
    var P2 = V.map(function (p) { return proj(p, th, ph); });
    F.forEach(function (f, fi) { if (front[fi]) it.push(["poly", f.map(function (q) { return P2[q]; }), "fr"]); });
    Object.keys(E).forEach(function (k) { var ab = k.split(",").map(Number); if (!E[k].some(Boolean)) it.push(["seg", P2[ab[0]], P2[ab[1]], "hid"]); });
    Object.keys(E).forEach(function (k) { var ab = k.split(",").map(Number); if (E[k].some(Boolean)) it.push(["seg", P2[ab[0]], P2[ab[1]], "ed"]); });
    return { it: it, P: P2, F: F, E: Object.keys(E).length };
  }
  function ngon(n, R, z) { var rot = -90 - 180 / n, V = []; for (var k = 0; k < n; k++) { var a = (rot + 360 * k / n) * PI / 180; V.push([R * Math.cos(a), R * Math.sin(a), z]); } return V; }
  function circum(n, l) { return l / (2 * Math.sin(PI / n)); }
  function apot(n, l) { return l / (2 * Math.tan(PI / n)); }
  function prismV(n, l, h) { var R = circum(n, l); return ngon(n, R, 0).concat(ngon(n, R, h)); }
  function pyramidV(n, l, h) { return ngon(n, circum(n, l), 0).concat([[0, 0, h]]); }
  function cuboidV(a, b, c) { var V = []; [0, c].forEach(function (z) { [0, b].forEach(function (y) { [0, a].forEach(function (x) { V.push([x, y, z]); }); }); }); return V; }
  var PHI = (1 + Math.sqrt(5)) / 2;
  function platonic(name) {
    var V = [], s = [-1, 1];
    if (name === "tetra") V = ngon(3, 2 * Math.SQRT2 / Math.sqrt(3), -0.8).concat([[0, 0, -0.8 + 2 * Math.SQRT2 * Math.sqrt(2 / 3)]]);
    else if (name === "cub") s.forEach(function (x) { s.forEach(function (y) { s.forEach(function (z) { V.push([x, y, z]); }); }); });
    else if (name === "octa") V = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
    else if (name === "ico") s.forEach(function (a) { [-PHI, PHI].forEach(function (b) { V.push([0, a, b], [a, b, 0], [b, 0, a]); }); });
    else {
      s.forEach(function (x) { s.forEach(function (y) { s.forEach(function (z) { V.push([x, y, z]); }); }); });
      [-1 / PHI, 1 / PHI].forEach(function (a) { [-PHI, PHI].forEach(function (b) { V.push([0, a, b], [a, b, 0], [b, 0, a]); }); });
    }
    return V;
  }
  function ell(r, b, cy, t0, t1, n) { n = n || 48; var o = []; for (var k = 0; k <= n; k++) { var t = t0 + (t1 - t0) * k / n; o.push([r * Math.cos(t), cy + b * Math.sin(t)]); } return o; }
  function cylinderD(r, h, ph, y0, top) {
    y0 = y0 || 0; var f = ph * PI / 180, b = r * Math.sin(f), H = h * Math.cos(f);
    var front = ell(r, b, y0, PI, 2 * PI), back = ell(r, b, y0, 0, PI), topf = ell(r, b, y0 + H, PI, 2 * PI);
    var side = [[-r, y0 + H]].concat(front, [[r, y0 + H]], topf.slice().reverse());
    var it = [["poly", side, "fr"], ["pl", back, "hid"], ["pl", front, "ed"], ["seg", [-r, y0], [-r, y0 + H], "ed"], ["seg", [r, y0], [r, y0 + H], "ed"]];
    if (top !== false) it.push(["poly", ell(r, b, y0 + H, 0, 2 * PI), "top"]);
    return it;
  }
  function coneD(r, h, ph, y0, down) {
    y0 = y0 || 0; var f = ph * PI / 180, b = r * Math.sin(f), H = h * Math.cos(f);
    if (down) { /* vèrtex cap avall (cucurutxo): la base és dalt i es veu sencera */
      var t1 = H > b ? Math.asin(b / H) : PI / 2, A = [0, y0 - H];
      var vis = ell(r, b, y0, -t1, PI + t1);
      return [["poly", [A].concat(vis.slice().reverse()), "fr"], ["seg", A, [r * Math.cos(t1), y0 - b * Math.sin(t1)], "ed"], ["seg", A, [-r * Math.cos(t1), y0 - b * Math.sin(t1)], "ed"], ["poly", ell(r, b, y0, 0, 2 * PI), "top"]];
    }
    var t0 = H > b ? Math.asin(b / H) : PI / 2, Ap = [0, y0 + H];
    var v = ell(r, b, y0, PI - t0, 2 * PI + t0), hd = ell(r, b, y0, t0, PI - t0);
    return [["poly", [Ap].concat(v), "fr"], ["pl", hd, "hid"], ["pl", v, "ed"], ["seg", Ap, v[0], "ed"], ["seg", Ap, v[v.length - 1], "ed"]];
  }
  function sphereD(r, ph, y0, half) {
    y0 = y0 || 0; var f = ph * PI / 180, b = r * Math.sin(f), front = ell(r, b, y0, PI, 2 * PI), back = ell(r, b, y0, 0, PI);
    if (half) { var dome = ell(r, r, y0, 0, PI); return [["poly", dome.concat(front.slice(1, -1)), "fr"], ["pl", dome, "ed"], ["pl", front, "ed"], ["pl", back, "hid"]]; }
    return [["circ", [0, y0], r, "fr"], ["pl", back, "hid"], ["pl", front, "ed"]];
  }
  function shiftIt(it, dx, dy) {
    function S(p) { return [p[0] + dx, p[1] + dy]; }
    return it.map(function (e) {
      var k = e[0];
      if (k === "poly" || k === "pl") return [k, e[1].map(S)].concat(e.slice(2));
      if (k === "seg") return [k, S(e[1]), S(e[2])].concat(e.slice(3));
      return [k, S(e[1])].concat(e.slice(2));
    });
  }
  /* desenvolupaments */
  function netPrism(n, l, h) {
    var it = [], k, a = apot(n, l), R = circum(n, l);
    for (k = 0; k < n; k++) it.push(["poly", [[k * l, 0], [(k + 1) * l, 0], [(k + 1) * l, h], [k * l, h]], "nf"]);
    [[0, -1], [h, 1]].forEach(function (q) {
      var C = [l / 2, q[0] + q[1] * a], rot = q[1] < 0 ? 90 + 180 / n : -90 - 180 / n, P = [];
      for (k = 0; k < n; k++) { var t = (rot + 360 * k / n) * PI / 180; P.push([C[0] + R * Math.cos(t), C[1] + R * Math.sin(t)]); }
      it.push(["poly", P, "bs"]);
    });
    return it;
  }
  function netPyr(n, l, ap) {
    var R = circum(n, l), a = apot(n, l), B = ngon(n, R, 0).map(function (p) { return [p[0], p[1]]; }), it = [["poly", B, "bs"]];
    B.forEach(function (P, k) { var Q = B[(k + 1) % n], M = mid(P, Q), d = Math.hypot(M[0], M[1]); it.push(["poly", [P, Q, [M[0] / d * (a + ap), M[1] / d * (a + ap)]], "nf"]); });
    return it;
  }

  /* dibuix amb rotació (arrossegant): o.draw(th, ph) torna l'SVG */
  function rot3d(box, draw) {
    var st = { th: V3.th, ph: V3.ph }, drag = null;
    box.classList.add("w3d");
    function paint() { draw(st.th, st.ph); }
    box.addEventListener("pointerdown", function (e) { if (!e.target.closest("svg")) return; drag = [e.clientX, e.clientY, st.th, st.ph]; try { box.setPointerCapture(e.pointerId); } catch (x) {} e.preventDefault(); });
    box.addEventListener("pointermove", function (e) { if (!drag) return; st.th = drag[2] - (e.clientX - drag[0]) * 0.6; st.ph = Math.max(-60, Math.min(80, drag[3] + (e.clientY - drag[1]) * 0.5)); paint(); });
    ["pointerup", "pointercancel"].forEach(function (k) { box.addEventListener(k, function () { drag = null; }); });
    return { paint: paint, st: st };
  }

  /* ---------- 11.1 poliedres ---------- */
  var PNAME = { 3: L3("triangular", "triangular", "triangular"), 4: L3("quadrangular", "cuadrangular", "square"), 5: L3("pentagonal", "pentagonal", "pentagonal"), 6: L3("hexagonal", "hexagonal", "hexagonal"), 7: L3("heptagonal", "heptagonal", "heptagonal"), 8: L3("octogonal", "octogonal", "octagonal") };
  var SOLIDS = {
    tetra: function () { return platonic("tetra"); }, cub: function () { return platonic("cub"); }, octa: function () { return platonic("octa"); },
    dodeca: function () { return platonic("dodeca"); }, ico: function () { return platonic("ico"); },
    p5: function () { return prismV(5, 1.4, 2.2); }, y6: function () { return pyramidV(6, 1.2, 2.4); }
  };
  function wPoly() {
    var w = document.getElementById("w-poly"); if (!w) return;
    var out = w.querySelector(".gout"), kind = "cub", R;
    function draw(th, ph) {
      var V = SOLIDS[kind](), r = polyhedron(V, th, ph), C = r.F.length, Vn = V.length, A = r.E;
      out.innerHTML = G(r.it, { W: 260, maxh: 240, pad: 16 }) + gcol([
        T(L3("Cares:", "Caras:", "Faces:")) + " " + tex("C=" + C), T(L3("Vèrtexs:", "Vértices:", "Vertices:")) + " " + tex("V=" + Vn), T(L3("Arestes:", "Aristas:", "Edges:")) + " " + tex("A=" + A),
        '<span class="big">' + tex("C+V=" + C + "+" + Vn + "=" + (C + Vn) + "=" + A + "+2\\ \\checkmark") + "</span>"]);
    }
    R = rot3d(out, draw);
    segBind(w, function (k) { kind = k; R.paint(); });
    onLang(R.paint);
  }

  /* ---------- 11.2 prismes ---------- */
  function prismData(n, l, h) {
    var a = apot(n, l), P = n * l, Ab = P * a / 2, AL = P * h;
    var rows = [], at;
    if (n === 4) { at = "A_{\\text{base}}=" + nf(l) + "^2=" + n4(l * l); Ab = l * l; }
    else if (n === 6) at = "a_b=\\sqrt{" + nf(l) + "^2-" + n4(l / 2) + "^2}" + eq(a) + "\\qquad A_{\\text{base}}=\\dfrac{" + nf(P) + "\\cdot" + fm(a) + "}{2}" + eq(Ab);
    else if (n === 3) at = "h_b=\\sqrt{" + nf(l) + "^2-" + n4(l / 2) + "^2}" + eq(l * Math.sqrt(3) / 2) + "\\qquad A_{\\text{base}}=\\dfrac{" + nf(l) + "\\cdot" + fm(l * Math.sqrt(3) / 2) + "}{2}" + eq(Ab);
    else at = "a_b=\\dfrac{l}{2\\tan(180^\\circ/" + n + ")}" + eq(a) + "\\qquad A_{\\text{base}}=\\dfrac{" + nf(P) + "\\cdot" + fm(a) + "}{2}" + eq(Ab);
    rows.push(tex("P_{\\text{base}}=" + n + "\\cdot" + nf(l) + "=" + nf(P) + "\\qquad A_L=P\\cdot h=" + nf(P) + "\\cdot" + nf(h) + "=" + nf(AL)));
    rows.push(tex(at));
    rows.push(tex("A_T=A_L+2A_{\\text{base}}" + eq(AL + 2 * Ab)) + " " + T(L3("unitats²", "unidades²", "square units")));
    return { rows: rows, AT: AL + 2 * Ab, AL: AL, Ab: Ab, V: Ab * h };
  }
  function wPrism() {
    var w = document.getElementById("w-prism"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), hs = w.querySelector(".hsteps"), R;
    function draw(th, ph) {
      var n = +I.n.value, l = +I.l.value, h = +I.h.value; showRv(w, "n", "n", n); showRv(w, "l", "l", l); showRv(w, "h", "h", h);
      var d = prismData(n, l, h);
      out.innerHTML = G(polyhedron(prismV(n, l, h), th, ph).it, { W: 220, maxh: 230, pad: 14 }) + G(netPrism(n, l, h), { W: 300, maxh: 260, pad: 10 });
      hs.innerHTML = rows2html(["<strong>" + T(L3("Prisma {p} regular", "Prisma {p} regular", "Regular {p} prism")).replace("{p}", T(PNAME[n])) + "</strong>"].concat(d.rows));
    }
    R = rot3d(out, draw);
    ["n", "l", "h"].forEach(function (k) { I[k].addEventListener("input", R.paint); });
    onLang(R.paint);
  }

  /* ---------- 11.3 piràmides ---------- */
  function pyrData(n, l, h) {
    var a = apot(n, l), ap = Math.sqrt(h * h + a * a), P = n * l, Ab = n === 4 ? l * l : P * a / 2, AL = P * ap / 2;
    return { a: a, ap: ap, P: P, Ab: Ab, AL: AL, AT: AL + Ab, rows: [
      tex("a_b" + (n === 4 ? "=\\dfrac{" + nf(l) + "}{2}" : n === 6 ? "=\\sqrt{" + nf(l) + "^2-" + n4(l / 2) + "^2}" : "") + eq(a) + "\\qquad a_p=\\sqrt{h^2+a_b^2}=\\sqrt{" + nf(h) + "^2+" + d2(a) + "^2}" + eq(ap)),
      tex("A_L=\\dfrac{P\\cdot a_p}{2}=\\dfrac{" + nf(P) + "\\cdot" + fm(ap) + "}{2}" + eq(AL) + "\\qquad A_{\\text{base}}" + eq(Ab)),
      tex("A_T=A_L+A_{\\text{base}}" + eq(AL + Ab))] };
  }
  function wPyr() {
    var w = document.getElementById("w-pyr"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), hs = w.querySelector(".hsteps"), R;
    function draw(th, ph) {
      var n = +I.n.value, l = +I.l.value, h = +I.h.value; showRv(w, "n", "n", n); showRv(w, "l", "l", l); showRv(w, "h", "h", h);
      var d = pyrData(n, l, h), r = polyhedron(pyramidV(n, l, h), th, ph), O = proj([0, 0, 0], th, ph), Ap = r.P[n];
      var k = 0, best = -1e9; for (var i = 0; i < n; i++) { var m = mid(r.P[i], r.P[(i + 1) % n]); if (m[0] > best) { best = m[0]; k = i; } }
      var M = mid(r.P[k], r.P[(k + 1) % n]);
      var it = r.it.concat([["seg", O, Ap, "ax"], ["seg", O, M, "ax"], ["seg", M, Ap, "ax2"], ["dot", O], T_(mid(O, Ap), "h", { dx: -7, a: "end", cls: "ax" }), T_(mid(M, Ap), "aₚ", { dx: 8, a: "start", cls: "ax2" })]);
      out.innerHTML = G(it, { W: 220, maxh: 230, pad: 14 }) + G(netPyr(n, l, d.ap), { W: 260, maxh: 260, pad: 10 });
      hs.innerHTML = rows2html(["<strong>" + T(L3("Piràmide {p} regular", "Pirámide {p} regular", "Regular {p} pyramid")).replace("{p}", T(PNAME[n])) + "</strong>"].concat(d.rows));
    }
    R = rot3d(out, draw);
    ["n", "l", "h"].forEach(function (k) { I[k].addEventListener("input", R.paint); });
    onLang(R.paint);
  }

  /* ---------- 11.4 cilindre i con ---------- */
  function wRev() {
    var w = document.getElementById("w-rev"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), hs = w.querySelector(".hsteps"), mode = "cil";
    function paint() {
      var r = +I.r.value, h = +I.h.value; showRv(w, "r", "r", r); showRv(w, "h", "h", h);
      var f = Math.min(1, 6 / Math.max(r * 2, h)), it, net, rows;
      if (mode === "cil") {
        it = cylinderD(r * f, h * f, 22).concat([["seg", [0, 0], [r * f, 0], "ax"], T_([r * f / 2, 0], "r", { dy: -5, cls: "ax" }), T_([r * f, h * f * 0.46], "h", { dx: 8, a: "start" })]);
        var L = 2 * PI * r; net = [["poly", [[0, 0], [L, 0], [L, h], [0, h]], "nf"], ["circ", [L / 2, -r], r, "bs"], ["circ", [L / 2, h + r], r, "bs"], T_([L / 2, 0], "2πr ≈ " + lab(L), { dy: -6 }), T_([L, h / 2], "h", { dx: 6, a: "start" })];
        rows = [tex("A_L=2\\pi r h=2\\pi\\cdot" + nf(r) + "\\cdot" + nf(h) + "=" + piv(2 * r * h)), tex("A_{\\text{bases}}=2\\pi r^2=2\\pi\\cdot" + nf(r) + "^2=" + piv(2 * r * r)), tex("A_T=" + piv(2 * r * h + 2 * r * r))];
      } else {
        var g = Math.sqrt(r * r + h * h), ang = 360 * r / g;
        it = coneD(r * f, h * f, 22).concat([["seg", [0, 0], [r * f, 0], "ax"], ["seg", [0, 0], [0, h * f * Math.cos(22 * PI / 180)], "ax"], T_([r * f / 2, 0], "r", { dy: -5, cls: "ax" }), T_([0, h * f * 0.45], "h", { dx: -6, a: "end", cls: "ax" }), T_(mid([r * f, 0], [0, h * f * Math.cos(22 * PI / 180)]), "g", { dx: 8, a: "start" })]);
        net = [["sect", [0, 0], g, 270 - ang / 2, 270 + ang / 2, "nf"], ["circ", [0, -g - r], r, "bs"], T_([0, -g / 2], "g", { dx: 6, a: "start" })];
        rows = [tex("g=\\sqrt{h^2+r^2}=\\sqrt{" + n4(h * h) + "+" + n4(r * r) + "}" + eq(g)), tex("A_L=\\pi r g=\\pi\\cdot" + nf(r) + "\\cdot" + d2(g) + "\\approx " + d2(PI * r * g)), tex("A_{\\text{base}}=\\pi r^2=" + piv(r * r)), tex("A_T\\approx " + d2(PI * r * g + PI * r * r)),
          T(L3("Angle del sector:", "Ángulo del sector:", "Sector angle:")) + " " + tex("360^\\circ\\cdot\\dfrac{r}{g}\\approx " + d2(ang) + "^\\circ")];
      }
      out.innerHTML = G(it, { W: 200, maxh: 230, pad: 18 }) + G(net, { W: 260, maxh: 260, pad: 16 });
      hs.innerHTML = rows2html(rows);
    }
    segBind(w, function (k) { mode = k; paint(); });
    ["r", "h"].forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 11.6 unitats ---------- */
  var UNITS = [["km³", 1e9], ["hm³", 1e6], ["dam³", 1e3], ["m³", 1], ["dm³", 1e-3], ["cm³", 1e-6], ["mm³", 1e-9], ["kL", 1], ["hL", 0.1], ["daL", 0.01], ["L", 1e-3], ["dL", 1e-4], ["cL", 1e-5], ["mL", 1e-6]];
  function fmtBig(v) {
    if (v === 0) return "0";
    var r = Math.round(v * 1e9) / 1e9;
    if (Math.abs(r) >= 1e15 || (Math.abs(r) < 1e-9)) return v.toExponential(3).replace(".", "\\dc ").replace("e+", "\\cdot10^{").replace("e-", "\\cdot10^{-") + "}";
    var s = String(r); if (/e/.test(s)) s = r.toFixed(9).replace(/0+$/, "");
    var p = s.split("."), ip = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, "\\,");
    return ip + (p[1] ? "\\dc " + p[1] : "");
  }
  function wUnits() {
    var w = document.getElementById("w-units"); if (!w) return;
    var I = inputs(w), fr = w.querySelector('select[data-k="from"]'), to = w.querySelector('select[data-k="to"]'), out = w.querySelector(".hsteps"), info = w.querySelector(".info");
    UNITS.forEach(function (u_, i) { fr.add(new Option(u_[0], i)); to.add(new Option(u_[0], i)); });
    fr.value = 3; to.value = 10;
    function paint() {
      out.innerHTML = info.innerHTML = "";
      var v = numIn(I.v.value); if (v === null) { info.innerHTML = warn(u("num")); return; }
      var a = UNITS[+fr.value], b = UNITS[+to.value], r = v * a[1] / b[1];
      var t = (a[0].indexOf("³") >= 0) !== (b[0].indexOf("³") >= 0) ? T(L3("Recorda: 1 dm³ = 1 L, 1 cm³ = 1 mL i 1 m³ = 1000 L.", "Recuerda: 1 dm³ = 1 L, 1 cm³ = 1 mL y 1 m³ = 1000 L.", "Remember: 1 dm³ = 1 L, 1 cm³ = 1 mL and 1 m³ = 1000 L.")) : (a[0].indexOf("³") >= 0 ? T(L3("Entre unitats de volum consecutives es multiplica o es divideix per 1000.", "Entre unidades de volumen consecutivas se multiplica o se divide por 1000.", "Between consecutive volume units multiply or divide by 1000.")) : T(L3("Entre unitats de capacitat consecutives es multiplica o es divideix per 10.", "Entre unidades de capacidad consecutivas se multiplica o se divide por 10.", "Between consecutive capacity units multiply or divide by 10.")));
      out.innerHTML = rows2html(['<span class="big">' + tex(fmtBig(v) + "\\ \\text{" + a[0].replace("³", "}^3\\text{") + "}=" + fmtBig(r) + "\\ \\text{" + b[0].replace("³", "}^3\\text{") + "}") + "</span>", t]);
    }
    I.v.addEventListener("input", paint); fr.addEventListener("change", paint); to.addEventListener("change", paint);
    onLang(paint);
  }

  /* ---------- 11.6 Cavalieri ---------- */
  function wCav() {
    var w = document.getElementById("w-cav"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function stack(x0, sh, curve) {
      var it = [], n = 12, r = 1, b = 0.28, th = 0.32;
      for (var i = 0; i < n; i++) {
        var t = i / (n - 1), dx = curve ? sh * 2.2 * Math.sin(t * PI) : sh * 2.2 * t, y = i * th, c = x0 + dx;
        var e = ell(r, b, y, PI, 2 * PI).map(function (p) { return [p[0] + c, p[1]]; }), e2 = ell(r, b, y + th, PI, 2 * PI).map(function (p) { return [p[0] + c, p[1]]; });
        it.push(["poly", e.concat(e2.slice().reverse()), "coin"]);
        if (i === n - 1) it.push(["poly", ell(r, b, y + th, 0, 2 * PI).map(function (p) { return [p[0] + c, p[1]]; }), "coin"]);
      }
      return it;
    }
    function paint() {
      var s = +I.s.value; showRv(w, "s", "s", s);
      out.innerHTML = G(stack(0, 0, false).concat(stack(3.4, s, false), stack(7.8 + s * 2.2, s, true)), { W: 360, maxh: 200, pad: 14 }) + gcol([
        T(L3("Les tres piles tenen 12 monedes iguals: a cada altura, la secció és un cercle de la mateixa àrea.", "Las tres pilas tienen 12 monedas iguales: a cada altura, la sección es un círculo de la misma área.", "All three stacks have 12 equal coins: at every height the cross-section is a disc with the same area.")),
        "<strong>" + T(L3("Tenen el mateix volum, encara que la forma canvie.", "Tienen el mismo volumen, aunque la forma cambie.", "They have the same volume, even though the shape changes.")) + "</strong>"]);
    }
    I.s.addEventListener("input", paint);
    onLang(paint);
  }

  /* ---------- 11.7 omplir el prisma amb piràmides ---------- */
  function wFill() {
    var w = document.getElementById("w-fill"); if (!w) return;
    var out = w.querySelector(".gout"), mode = "pyr", k = 0;
    function water(level, isCyl) {
      if (!level) return [];
      var hh = 3 * level / 3, ph = 22;
      if (isCyl) return cylinderD(1.4, hh, ph).filter(function (e) { return e[0] === "poly"; }).map(function (e) { return ["poly", e[1], "water"]; });
      var r = polyhedron(prismV(4, 2.4, hh), V3.th, ph);
      return r.it.filter(function (e) { return e[0] === "poly"; }).map(function (e) { return ["poly", e[1], "water"]; });
    }
    function paint() {
      var isC = mode === "con", A, B;
      if (isC) { A = coneD(1.4, 3, 22); B = water(k, true).concat(cylinderD(1.4, 3, 22, 0, false).filter(function (e) { return e[0] !== "poly"; })).concat([["pl", ell(1.4, 1.4 * Math.sin(22 * PI / 180), 3 * Math.cos(22 * PI / 180), 0, 2 * PI), "ed"]]); }
      else { A = polyhedron(pyramidV(4, 2.4, 3), V3.th, 22).it; B = water(k, false).concat(polyhedron(prismV(4, 2.4, 3), V3.th, 22).it.filter(function (e) { return e[0] !== "poly"; })); }
      out.innerHTML = G(A, { W: 150, maxh: 170, pad: 14 }) + G(B, { W: 150, maxh: 170, pad: 14 }) + gcol([
        fill(T(L3("Abocades: {k} de 3", "Vertidas: {k} de 3", "Poured: {k} of 3")), { k: k }),
        tex("V=" + (k === 0 ? "0" : k === 3 ? (isC ? "\\pi r^2h" : "A_{\\text{base}}\\cdot h") : "\\dfrac{" + k + "}{3}\\," + (isC ? "\\pi r^2h" : "A_{\\text{base}}\\cdot h"))),
        k === 3 ? "<strong>" + T(isC ? L3("Ple! El con és un terç del cilindre.", "¡Lleno! El cono es un tercio del cilindro.", "Full! The cone is a third of the cylinder.") : L3("Ple! La piràmide és un terç del prisma.", "¡Lleno! La pirámide es un tercio del prisma.", "Full! The pyramid is a third of the prism.")) + "</strong>" : ""]);
      w.querySelector('[data-a="pour"]').disabled = k >= 3;
    }
    segBind(w, function (m) { mode = m; k = 0; var b = w.querySelector('[data-a="pour"]'); b.innerHTML = T(m === "con" ? L3("Aboca un con ple", "Vierte un cono lleno", "Pour a full cone") : L3("Aboca una piràmide plena", "Vierte una pirámide llena", "Pour a full pyramid")); paint(); });
    w.querySelector('[data-a="pour"]').addEventListener("click", function () { if (k < 3) k++; paint(); });
    w.querySelector('[data-a="empty"]').addEventListener("click", function () { k = 0; paint(); });
    onLang(paint);
  }

  /* ---------- 11.7 calculadora de volums ---------- */
  function wVol() {
    var w = document.getElementById("w-vol"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), hs = w.querySelector(".hsteps"), mode = "pr", R;
    function draw(th, ph) {
      var n = +I.n.value, l = +I.l.value, h = +I.h.value, it, rows, nm = mode === "ci" || mode === "co" || mode === "es" ? "r" : "l";
      showRange(w, "n", mode === "pr" || mode === "py"); showRange(w, "h", mode !== "es");
      showRv(w, "n", "n", n); showRv(w, "l", nm, l); showRv(w, "h", "h", h);
      var f = Math.min(1, 6 / Math.max(2 * l, h));
      if (mode === "pr" || mode === "py") {
        var d = prismData(n, l, h);
        it = polyhedron(mode === "pr" ? prismV(n, l * f, h * f) : pyramidV(n, l * f, h * f), th, ph).it;
        rows = [tex("A_{\\text{base}}" + eq(d.Ab)), mode === "pr" ? tex("V=A_{\\text{base}}\\cdot h=" + d2(d.Ab) + "\\cdot" + nf(h) + eq(d.Ab * h)) : tex("V=\\dfrac{A_{\\text{base}}\\cdot h}{3}=\\dfrac{" + d2(d.Ab) + "\\cdot" + nf(h) + "}{3}" + eq(d.Ab * h / 3))];
      } else if (mode === "ci") { it = cylinderD(l * f, h * f, ph); rows = [tex("V=\\pi r^2h=\\pi\\cdot" + nf(l) + "^2\\cdot" + nf(h) + "=" + piv(l * l * h))]; }
      else if (mode === "co") { it = coneD(l * f, h * f, ph); rows = [tex("V=\\dfrac{\\pi r^2h}{3}=\\dfrac{\\pi\\cdot" + nf(l) + "^2\\cdot" + nf(h) + "}{3}=" + piv(l * l * h / 3))]; }
      else { it = sphereD(l * f, ph); rows = [tex("V=\\dfrac43\\pi r^3=\\dfrac43\\pi\\cdot" + nf(l) + "^3=" + piv(4 * l * l * l / 3))]; }
      out.innerHTML = G(it, { W: 220, maxh: 230, pad: 16 });
      hs.innerHTML = rows2html(rows.concat([T(L3("(en unitats cúbiques: si les mesures són en cm, el volum és en cm³)", "(en unidades cúbicas: si las medidas son en cm, el volumen es en cm³)", "(in cubic units: if lengths are in cm, the volume is in cm³)"))]));
    }
    R = rot3d(out, draw);
    segBind(w, function (k) { mode = k; R.paint(); });
    ["n", "l", "h"].forEach(function (k) { I[k].addEventListener("input", R.paint); });
    onLang(R.paint);
  }

  /* ---------- 11.8 cossos compostos ---------- */
  var COMP = {
    sitja: { la: "r", lb: "h", f: function (a, b) { var hc = a; return { V: PI * a * a * b + PI * a * a * hc / 3, rows: [tex("V=\\pi r^2h+\\dfrac{\\pi r^2\\cdot r}{3}=" + piv(a * a * b) + "+" + piv(a * a * a / 3)), tex("V=" + piv(a * a * b + a * a * a / 3))], d: function (s) { return cylinderD(a * s, b * s, 22, 0, false).concat(shiftIt(coneD(a * s, a * s, 22), 0, b * s * Math.cos(22 * PI / 180))); }, txt: L3("Cilindre de radi r i altura h amb una teulada cònica d'altura igual al radi.", "Cilindro de radio r y altura h con un tejado cónico de altura igual al radio.", "Cylinder with radius r and height h with a conical roof as tall as the radius.") }; } },
    caps: { la: "r", lb: "h", f: function (a, b) { return { V: PI * a * a * b + 4 / 3 * PI * a * a * a, rows: [tex("V=\\pi r^2h+\\dfrac43\\pi r^3=" + piv(a * a * b) + "+" + piv(4 * a * a * a / 3)), tex("V=" + piv(a * a * b + 4 * a * a * a / 3)), tex("A=2\\pi r h+4\\pi r^2=" + piv(2 * a * b + 4 * a * a))], d: function (s) { var r = a * s, H = b * s * Math.cos(22 * PI / 180), bb = r * Math.sin(22 * PI / 180); var top = ell(r, r, H, 0, PI), bot = ell(r, r, 0, PI, 2 * PI); var o = top.concat(bot); return [["poly", o, "fr"], ["pl", ell(r, bb, 0, PI, 2 * PI), "ed"], ["pl", ell(r, bb, H, PI, 2 * PI), "ed"], ["pl", o.concat([o[0]]), "ed"]]; }, txt: L3("Cilindre de radi r i llargària h amb una semiesfera a cada extrem.", "Cilindro de radio r y longitud h con una semiesfera en cada extremo.", "Cylinder with radius r and length h with a hemisphere at each end.") }; } },
    gelat: { la: "r", lb: "h", f: function (a, b) { return { V: PI * a * a * b / 3 + 2 / 3 * PI * a * a * a, rows: [tex("V=\\dfrac{\\pi r^2h}{3}+\\dfrac12\\cdot\\dfrac43\\pi r^3=" + piv(a * a * b / 3) + "+" + piv(2 * a * a * a / 3)), tex("V=" + piv(a * a * b / 3 + 2 * a * a * a / 3))], d: function (s) { return coneD(a * s, b * s, 22, 0, true).concat(sphereD(a * s, 22, 0, true)); }, txt: L3("Con de radi r i altura h (cap avall) amb una semiesfera de gelat al damunt.", "Cono de radio r y altura h (hacia abajo) con una semiesfera de helado encima.", "Cone with radius r and height h (pointing down) with a hemisphere of ice cream on top.") }; } },
    forat: { la: "r", lb: "a", f: function (a, b) { var r = Math.min(a, b / 2 - 0.25); return { r: r, V: b * b * b - PI * r * r * b, rows: [tex("V=a^3-\\pi r^2a=" + n4(b * b * b) + "-" + piv(r * r * b)), tex("V\\approx " + d2(b * b * b - PI * r * r * b))], d: function (s) { var A = b * s, rr = r * s, it = polyhedron(cuboidV(A, A, A), V3.th, 22).it, P = proj([A / 2, 0, A / 2], V3.th, 22); var c = []; for (var k = 0; k <= 48; k++) { var t = 2 * PI * k / 48; c.push(proj([A / 2 + rr * Math.cos(t), 0, A / 2 + rr * Math.sin(t)], V3.th, 22)); } return it.concat([["poly", c, "top"]]); }, txt: L3("Cub d'aresta a travessat per un forat cilíndric de radi r.", "Cubo de arista a atravesado por un agujero cilíndrico de radio r.", "Cube with edge a pierced by a cylindrical hole of radius r.") }; } }
  };
  function wComp() {
    var w = document.getElementById("w-comp"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), hs = w.querySelector(".hsteps"), mode = "sitja";
    function paint() {
      var C = COMP[mode], a = +I.a.value, b = +I.b.value, r = C.f(a, b);
      showRv(w, "a", C.la, mode === "forat" ? r.r : a); showRv(w, "b", C.lb, b);
      var s = 5 / Math.max(2 * a, b + (mode === "sitja" ? a : mode === "caps" ? 2 * a : mode === "gelat" ? a : 0));
      out.innerHTML = G(r.d(s), { W: 220, maxh: 230, pad: 16 });
      hs.innerHTML = rows2html([T(C.f(a, b).txt)].concat(r.rows));
    }
    segBind(w, function (k) { mode = k; paint(); });
    ["a", "b"].forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function numQ(v, pi) { return { num: v, tol: tolOf(v, pi) }; }
  function ret(o, q, s) { o.q = q; o.s = s; return o; }
  var GEN = {
    euler: function () {
      var t = rint(0, 2), kind = rint(0, 1), n = rint(3, 12), C, V, A, name;
      if (kind) { C = n + 2; V = 2 * n; A = 3 * n; name = L3("un prisma", "un prisma", "a prism"); } else { C = n + 1; V = n + 1; A = 2 * n; name = L3("una piràmide", "una pirámide", "a pyramid"); }
      if (rint(0, 2) === 0) { var p = pick([["tetra", 4, 4, 6], ["cub", 6, 8, 12], ["octa", 8, 6, 12], ["dodeca", 12, 20, 30], ["ico", 20, 12, 30]]); C = p[1]; V = p[2]; A = p[3]; }
      var giv = [["C", C], ["V", V], ["A", A]], ask = giv[t];
      var known = giv.filter(function (_, i) { return i !== t; });
      return ret(numQ(ask[1]), function () { return fill(T(L3("Un poliedre convex té {a} i {b}. Quant val {c}?", "Un poliedro convexo tiene {a} y {b}. ¿Cuánto vale {c}?", "A convex polyhedron has {a} and {b}. What is {c}?")), { a: "$" + known[0][0] + "=" + known[0][1] + "$", b: "$" + known[1][0] + "=" + known[1][1] + "$", c: "$" + ask[0] + "$" }); },
        function () { return tex("C+V=A+2\\ \\Rightarrow\\ " + ask[0] + "=" + ask[1]) + " (" + tex(C + "+" + V + "=" + A + "+2") + ")"; });
    },
    diag: function () {
      var a, b, c; if (rint(0, 1)) { var q = pick([[1, 2, 2, 3], [2, 3, 6, 7], [1, 4, 8, 9], [2, 6, 9, 11], [4, 4, 7, 9], [3, 4, 12, 13], [2, 10, 11, 15], [6, 6, 7, 11]]); a = q[0]; b = q[1]; c = q[2]; } else { a = rint(2, 12); b = rint(2, 12); c = rint(2, 15); }
      var D = Math.sqrt(a * a + b * b + c * c);
      return ret(numQ(D), function () { return fill(T(L3("Calcula la diagonal d'un ortoedre d'arestes {a}, {b} i {c} cm.", "Calcula la diagonal de un ortoedro de aristas {a}, {b} y {c} cm.", "Find the diagonal of a cuboid with edges {a}, {b} and {c} cm.")), { a: $n(a), b: $n(b), c: $n(c) }) + G(polyhedron(cuboidV(a, b, c), V3.th, V3.ph).it, { W: 200, maxh: 150, pad: 12 }); },
        function () { return tex("D=\\sqrt{" + a * a + "+" + b * b + "+" + c * c + "}=\\sqrt{" + (a * a + b * b + c * c) + "}" + eq(D)); });
    },
    prisma: function () {
      var t = rint(0, 2);
      if (t === 0) { var a = rint(2, 12), b = rint(2, 12), c = rint(2, 12), A = 2 * (a * b + a * c + b * c); return ret(numQ(A), function () { return fill(T(L3("Calcula l'àrea total d'un ortoedre de {a} × {b} × {c} cm (en cm²).", "Calcula el área total de un ortoedro de {a} × {b} × {c} cm (en cm²).", "Find the total surface area of an {a} × {b} × {c} cm cuboid (in cm²).")), { a: $n(a), b: $n(b), c: $n(c) }); }, function () { return tex("A=2(" + a + "\\cdot" + b + "+" + a + "\\cdot" + c + "+" + b + "\\cdot" + c + ")=" + A); }); }
      var n = t === 1 ? 4 : pick([3, 6]), l = rint(2, 10), h = rint(3, 15), d = prismData(n, l, h);
      return ret(numQ(d.AT), function () { return fill(T(L3("Calcula l'àrea total d'un prisma {p} regular de {l} cm d'aresta de la base i {h} cm d'altura (en cm²).", "Calcula el área total de un prisma {p} regular de {l} cm de arista de la base y {h} cm de altura (en cm²).", "Find the total surface area of a regular {p} prism with {l} cm base edges and {h} cm height (in cm²).")), { p: T(PNAME[n]), l: $n(l), h: $n(h) }); }, function () { return d.rows.join(" "); });
    },
    piramide: function () {
      var n = pick([4, 4, 6, 3]), l = 2 * rint(1, 6), h = rint(2, 12), d = pyrData(n, l, h);
      if (n === 4 && rint(0, 1)) { var q = pick([[6, 4], [10, 12], [16, 6], [12, 8], [14, 24], [18, 12], [10, 6]]); l = q[0]; h = q[1]; d = pyrData(4, l, h); }
      return ret(numQ(d.AT), function () { return fill(T(L3("Calcula l'àrea total d'una piràmide {p} regular de {l} cm d'aresta de la base i {h} cm d'altura (en cm²).", "Calcula el área total de una pirámide {p} regular de {l} cm de arista de la base y {h} cm de altura (en cm²).", "Find the total surface area of a regular {p} pyramid with {l} cm base edges and {h} cm height (in cm²).")), { p: T(PNAME[n]), l: $n(l), h: $n(h) }); }, function () { return d.rows.join(" "); });
    },
    cilindre: function () {
      var r = rint(1, 10), h = rint(2, 20), t = rint(0, 1), v = t ? 2 * PI * r * h : 2 * PI * r * h + 2 * PI * r * r;
      return ret(numQ(v, true), function () { return fill(T(t ? L3("Calcula l'àrea lateral d'un cilindre de {r} cm de radi i {h} cm d'altura (en cm²).", "Calcula el área lateral de un cilindro de {r} cm de radio y {h} cm de altura (en cm²).", "Find the lateral area of a cylinder with a {r} cm radius and {h} cm height (in cm²).") : L3("Calcula l'àrea total d'un cilindre de {r} cm de radi i {h} cm d'altura (en cm²).", "Calcula el área total de un cilindro de {r} cm de radio y {h} cm de altura (en cm²).", "Find the total area of a cylinder with a {r} cm radius and {h} cm height (in cm²).")), { r: $n(r), h: $n(h) }); },
        function () { return tex("A_L=2\\pi\\cdot" + r + "\\cdot" + h + "=" + piv(2 * r * h)) + (t ? "" : " " + tex("A_T=" + 2 * r * h + "\\pi+" + 2 * r * r + "\\pi=" + piv(2 * r * h + 2 * r * r))); });
    },
    con: function () {
      var q = rint(0, 1) ? pick([[3, 4, 5], [5, 12, 13], [6, 8, 10], [8, 15, 17], [9, 12, 15], [7, 24, 25]]) : null, r, h, g;
      if (q) { r = q[0]; h = q[1]; g = q[2]; } else { r = rint(1, 9); h = rint(2, 15); g = Math.sqrt(r * r + h * h); }
      var v = PI * r * g + PI * r * r;
      return ret(numQ(v, true), function () { return fill(T(L3("Calcula l'àrea total d'un con de {r} cm de radi i {h} cm d'altura (en cm²).", "Calcula el área total de un cono de {r} cm de radio y {h} cm de altura (en cm²).", "Find the total area of a cone with a {r} cm radius and {h} cm height (in cm²).")), { r: $n(r), h: $n(h) }); },
        function () { return tex("g=\\sqrt{" + h * h + "+" + r * r + "}" + eq(g) + "\\qquad A_T=\\pi\\cdot" + r + "\\cdot" + d2(g) + "+\\pi\\cdot" + r + "^2\\approx " + d2(v)); });
    },
    esfera: function () {
      var t = rint(0, 1), r = rint(1, 15), v = 4 * PI * r * r;
      return ret(numQ(v, true), function () { return t ? fill(T(L3("Calcula l'àrea d'una esfera de {d} cm de diàmetre (en cm²).", "Calcula el área de una esfera de {d} cm de diámetro (en cm²).", "Find the area of a sphere {d} cm across (in cm²).")), { d: $n(2 * r) }) : fill(T(L3("Calcula l'àrea d'una esfera de {r} cm de radi (en cm²).", "Calcula el área de una esfera de {r} cm de radio (en cm²).", "Find the area of a sphere with a {r} cm radius (in cm²).")), { r: $n(r) }); },
        function () { return (t ? tex("r=" + r) + ". " : "") + tex("A=4\\pi\\cdot" + r + "^2=" + piv(4 * r * r)); });
    },
    unitats: function () {
      var cases = [["m³", "L", 1000], ["dm³", "L", 1], ["cm³", "mL", 1], ["L", "cm³", 1000], ["m³", "dm³", 1000], ["cm³", "dm³", 0.001], ["mL", "L", 0.001], ["hL", "m³", 0.1], ["L", "m³", 0.001], ["dm³", "cm³", 1000], ["cL", "cm³", 10], ["m³", "cm³", 1e6]];
      var c = pick(cases), v = pick([0.5, 1.2, 2.5, 3, 4.75, 12, 25, 150, 750, 2400]), r = v * c[2];
      return ret({ num: r, tol: Math.max(1e-9, Math.abs(r) * 1e-6) }, function () { return fill(T(L3("Expressa {v} {a} en {b}.", "Expresa {v} {a} en {b}.", "Write {v} {a} in {b}.")), { v: $n(v), a: c[0], b: c[1] }); }, function () { return tex(fmtBig(v) + "\\ \\text{" + c[0].replace("³", "}^3\\text{") + "}=" + fmtBig(r) + "\\ \\text{" + c[1].replace("³", "}^3\\text{") + "}"); });
    },
    vprisma: function () {
      var t = rint(0, 3);
      if (t === 0) { var a = rint(2, 12), b = rint(2, 12), c = rint(2, 12); return ret(numQ(a * b * c), function () { return fill(T(L3("Calcula el volum d'un ortoedre de {a} × {b} × {c} cm (en cm³).", "Calcula el volumen de un ortoedro de {a} × {b} × {c} cm (en cm³).", "Find the volume of an {a} × {b} × {c} cm cuboid (in cm³).")), { a: $n(a), b: $n(b), c: $n(c) }); }, function () { return tex("V=" + a + "\\cdot" + b + "\\cdot" + c + "=" + a * b * c); }); }
      if (t === 1) { var r = rint(1, 10), h = rint(2, 20); return ret(numQ(PI * r * r * h, true), function () { return fill(T(L3("Calcula el volum d'un cilindre de {r} cm de radi i {h} cm d'altura (en cm³).", "Calcula el volumen de un cilindro de {r} cm de radio y {h} cm de altura (en cm³).", "Find the volume of a cylinder with a {r} cm radius and {h} cm height (in cm³).")), { r: $n(r), h: $n(h) }); }, function () { return tex("V=\\pi\\cdot" + r + "^2\\cdot" + h + "=" + piv(r * r * h)); }); }
      if (t === 2) { var p = rint(2, 9), q = rint(2, 9), H = rint(3, 15); return ret(numQ(p * q * H / 2), function () { return fill(T(L3("Un prisma té de base un triangle rectangle de catets {p} cm i {q} cm i fa {h} cm d'altura. Quin volum té (en cm³)?", "Un prisma tiene de base un triángulo rectángulo de catetos {p} cm y {q} cm y mide {h} cm de altura. ¿Qué volumen tiene (en cm³)?", "A prism has a right-triangle base with {p} cm and {q} cm legs and is {h} cm tall. What is its volume (in cm³)?")), { p: $n(p), q: $n(q), h: $n(H) }); }, function () { return tex("V=\\dfrac{" + p + "\\cdot" + q + "}{2}\\cdot" + H + "=" + nf(p * q * H / 2)); }); }
      var n = pick([3, 6]), l = rint(2, 10), h2 = rint(3, 15), d = prismData(n, l, h2);
      return ret(numQ(d.V), function () { return fill(T(L3("Calcula el volum d'un prisma {p} regular de {l} cm d'aresta de la base i {h} cm d'altura (en cm³).", "Calcula el volumen de un prisma {p} regular de {l} cm de arista de la base y {h} cm de altura (en cm³).", "Find the volume of a regular {p} prism with {l} cm base edges and {h} cm height (in cm³).")), { p: T(PNAME[n]), l: $n(l), h: $n(h2) }); }, function () { return d.rows[1] + " " + tex("V=A_{\\text{base}}\\cdot h" + eq(d.V)); });
    },
    vpir: function () {
      var t = rint(0, 2);
      if (t === 0) { var l = rint(2, 12), h = rint(3, 15); return ret(numQ(l * l * h / 3), function () { return fill(T(L3("Calcula el volum d'una piràmide quadrangular de {l} cm d'aresta de la base i {h} cm d'altura (en cm³).", "Calcula el volumen de una pirámide cuadrangular de {l} cm de arista de la base y {h} cm de altura (en cm³).", "Find the volume of a square pyramid with {l} cm base edges and {h} cm height (in cm³).")), { l: $n(l), h: $n(h) }); }, function () { return tex("V=\\dfrac{" + l + "^2\\cdot" + h + "}{3}" + eq(l * l * h / 3)); }); }
      if (t === 1) { var r = rint(1, 10), h2 = rint(2, 20); return ret(numQ(PI * r * r * h2 / 3, true), function () { return fill(T(L3("Calcula el volum d'un con de {r} cm de radi i {h} cm d'altura (en cm³).", "Calcula el volumen de un cono de {r} cm de radio y {h} cm de altura (en cm³).", "Find the volume of a cone with a {r} cm radius and {h} cm height (in cm³).")), { r: $n(r), h: $n(h2) }); }, function () { return tex("V=\\dfrac{\\pi\\cdot" + r + "^2\\cdot" + h2 + "}{3}=" + piv(r * r * h2 / 3)); }); }
      var q = pick([[3, 5, 4], [5, 13, 12], [6, 10, 8], [8, 17, 15], [9, 15, 12]]);
      return ret(numQ(PI * q[0] * q[0] * q[2] / 3, true), function () { return fill(T(L3("Un con té {g} cm de generatriu i {r} cm de radi. Calcula'n el volum (en cm³).", "Un cono tiene {g} cm de generatriz y {r} cm de radio. Calcula su volumen (en cm³).", "A cone has a {g} cm slant height and a {r} cm radius. Find its volume (in cm³).")), { g: $n(q[1]), r: $n(q[0]) }); },
        function () { return tex("h=\\sqrt{" + q[1] * q[1] + "-" + q[0] * q[0] + "}=" + q[2] + "\\qquad V=\\dfrac{\\pi\\cdot" + q[0] + "^2\\cdot" + q[2] + "}{3}=" + piv(q[0] * q[0] * q[2] / 3)); });
    },
    vesf: function () {
      var t = rint(0, 2), r = rint(1, 12), v = 4 / 3 * PI * r * r * r;
      if (t === 2) return ret(numQ(v / 2, true), function () { return fill(T(L3("Calcula el volum d'una semiesfera de {r} cm de radi (en cm³).", "Calcula el volumen de una semiesfera de {r} cm de radio (en cm³).", "Find the volume of a hemisphere with a {r} cm radius (in cm³).")), { r: $n(r) }); }, function () { return tex("V=\\dfrac12\\cdot\\dfrac43\\pi\\cdot" + r + "^3=" + piv(2 * r * r * r / 3)); });
      return ret(numQ(v, true), function () { return t ? fill(T(L3("Calcula el volum d'una esfera de {d} cm de diàmetre (en cm³).", "Calcula el volumen de una esfera de {d} cm de diámetro (en cm³).", "Find the volume of a sphere {d} cm across (in cm³).")), { d: $n(2 * r) }) : fill(T(L3("Calcula el volum d'una esfera de {r} cm de radi (en cm³).", "Calcula el volumen de una esfera de {r} cm de radio (en cm³).", "Find the volume of a sphere with a {r} cm radius (in cm³).")), { r: $n(r) }); },
        function () { return (t ? tex("r=" + r) + ". " : "") + tex("V=\\dfrac43\\pi\\cdot" + r + "^3=" + piv(4 * r * r * r / 3)); });
    },
    comp: function () {
      var mode = pick(["sitja", "caps", "gelat", "forat"]), a = rint(1, 5), b = rint(3, 12);
      if (mode === "forat") { b = rint(4, 12); a = rint(1, Math.floor(b / 2) - 1 || 1); }
      var r = COMP[mode].f(a, b), names = { sitja: ["r", "h"], caps: ["r", "h"], gelat: ["r", "h"], forat: ["r", "a"] }[mode];
      return ret(numQ(r.V, true), function () { return T(r.txt) + " " + fill(T(L3("Si {p} = {a} cm i {q} = {b} cm, quin volum té (en cm³)?", "Si {p} = {a} cm y {q} = {b} cm, ¿qué volumen tiene (en cm³)?", "If {p} = {a} cm and {q} = {b} cm, what is its volume (in cm³)?")), { p: names[0], q: names[1], a: $n(mode === "forat" ? r.r : a), b: $n(b) }) + G(r.d(4 / Math.max(2 * a, b + a)), { W: 170, maxh: 160, pad: 12 }); }, function () { return r.rows.join(" "); });
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
        var v = numIn(inp.value); if (v === null) { info.innerHTML = warn(u("num")); return; }
        good = Math.abs(v - q.num) <= (q.tol || 1e-6);
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
  window.FM11 = { G: G, GEN: GEN, numIn: numIn, polyhedron: polyhedron, platonic: platonic, prismData: prismData, pyrData: pyrData, COMP: COMP };

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

  var TITLES = { va: "Cossos geomètrics · FentMates", es: "Cuerpos geométricos · FentMates", en: "Solids · FentMates" };
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
    wPoly(); wPrism(); wPyr(); wRev(); wUnits(); wCav(); wFill(); wVol(); wComp();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
