(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-3eso-u10-done", NSEC = 8;

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
     unitat 10
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
      if (k === "poly") it[1].forEach(function (p) { xs.push(p[0]); ys.push(p[1]); });
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
      if (k === "poly") g += '<polygon class="gp ' + (it[2] || "") + '" points="' + pts(it[1]) + '"/>';
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

  /* "= 7,5" si té com a molt 3 decimals, "≈ 8,57" si no */
  function eq(v) { return Math.abs(v * 1000 - Math.round(v * 1000)) < 1e-6 ? "=" + nf(v) : "\\approx " + d2(v); }
  function rnd(v, d) { var p = Math.pow(10, d || 2); return Math.round(v * p) / p; }
  function rd(I, k) { var s = I[k].value.trim(); if (s === "" || s === "?") return null; var v = numIn(s); return v === null || v <= 0 ? NaN : v; }

  /* ---------- figures de la unitat ---------- */
  /* tres paral·leles (y = 0, d1, d1 + d2) tallades per dues secants (com tales() de fig10.py) */
  function talesFig(d1, d2, ar, as, labs, hot, p) {
    p = p == null ? 2.2 : p;
    var Y = [0, d1, d1 + d2], tr = 1 / Math.tan(ar * PI / 180), ts = 1 / Math.tan(as * PI / 180);
    var R = Y.map(function (y) { return [y * tr, y]; }), S = Y.map(function (y) { return [p + y * ts, y]; });
    var x0 = Math.min(R[0][0], R[2][0], S[0][0], S[2][0]) - 1.2, x1 = Math.max(R[0][0], R[2][0], S[0][0], S[2][0]) + 1.2, e = 0.7, it = [];
    Y.forEach(function (y) { it.push(["seg", [x0, y], [x1, y], "par"]); });
    it.push(["seg", [-e * tr, -e], [(Y[2] + e) * tr, Y[2] + e], "tv"], ["seg", [p - e * ts, -e], [p + (Y[2] + e) * ts, Y[2] + e], "tv"]);
    var SG = { AB: [R[0], R[1]], BC: [R[1], R[2]], A1B1: [S[0], S[1]], B1C1: [S[1], S[2]] };
    (hot || "").split(",").forEach(function (h) { if (SG[h]) it.push(["seg", SG[h][0], SG[h][1], "hl"]); });
    R.concat(S).forEach(function (P) { it.push(["dot", P]); });
    ["A", "B", "C"].forEach(function (n, i) { it.push(T_(R[i], n, { dx: -9, dy: -5, a: "end" }), T_(S[i], n + "′", { dx: 9, dy: -5, a: "start" })); });
    if (labs) Object.keys(labs).forEach(function (k) {
      var g = SG[k], sd = k.charAt(0) === "A" && k.length > 2 || k === "B1C1" ? 1 : -1;
      it.push(T_(mid(g[0], g[1]), labs[k], { dx: sd * 10, a: sd > 0 ? "start" : "end", cls: (hot || "").split(",").indexOf(k) >= 0 ? "hot" : "" }));
    });
    return it;
  }
  /* triangle ABC (A dalt) amb B′C′ ∥ BC a la fracció t des d'A (com tpos() de fig10.py) */
  function tposFig(AB, AC, ang, t, labs, hot) {
    var a1 = 28 * PI / 180, a2 = ang * PI / 180 - a1, A = [0, 0];
    var B = [-AB * Math.sin(a1), -AB * Math.cos(a1)], C = [AC * Math.sin(a2), -AC * Math.cos(a2)];
    var B1 = [B[0] * t, B[1] * t], C1 = [C[0] * t, C[1] * t];
    var it = [["poly", [A, B, C], "gf"], ["poly", [A, B1, C1], "tr"], ["seg", B1, C1, "hl"], ["seg", B, C, "hl2"]];
    [A, B, C, B1, C1].forEach(function (P) { it.push(["dot", P]); });
    it.push(T_(A, "A", { dy: -8 }), T_(B, "B", { dx: -8, a: "end", dy: 8 }), T_(C, "C", { dx: 8, a: "start", dy: 8 }), T_(B1, "B′", { dx: -8, a: "end" }), T_(C1, "C′", { dx: 8, a: "start" }));
    var pos = { AB1: [A, B1, -1], B1B: [B1, B, -1], AC1: [A, C1, 1], C1C: [C1, C, 1], B1C1: [B1, C1, 0], BC: [B, C, 0] };
    if (labs) Object.keys(labs).forEach(function (k) {
      var q = pos[k], o = { dx: q[2] * 10, a: q[2] < 0 ? "end" : q[2] > 0 ? "start" : "middle", dy: k === "BC" ? 16 : k === "B1C1" ? -5 : 4 };
      if (hot === k) o.cls = "hot";
      it.push(T_(mid(q[0], q[1]), labs[k], o));
    });
    return it;
  }
  /* pal i edifici amb les ombres (com shadow() de fig10.py) */
  function shadowFig(h1, s1, h2, s2, l, hot) {
    var g = Math.max(s1, 1) + 1.2, x2 = s1 + g;
    return [["seg", [-0.6, 0], [x2 + s2 + 0.8, 0], "axis"], ["poly", [[0, 0], [0, h1], [s1, 0]], "tr"], ["ra", [0, 0], [1, 0], [0, 1]],
      ["poly", [[x2, 0], [x2, h2], [x2 + s2, 0]], "gf"], ["ra", [x2, 0], [x2 + 1, 0], [x2, 1]], ["seg", [0, 0], [0, h1], "wall"], ["seg", [x2, 0], [x2, h2], "wall"],
      ["seg", [0, h1], [s1, 0], "ray"], ["seg", [x2, h2], [x2 + s2, 0], "ray"],
      T_([0, h1 / 2], l[0], { dx: -8, a: "end", cls: hot === 0 ? "hot" : "" }), T_([s1 / 2, 0], l[1], { dy: 15, cls: hot === 1 ? "hot" : "" }),
      T_([x2, h2 / 2], l[2], { dx: -8, a: "end", cls: hot === 2 ? "hot" : "" }), T_([x2 + s2 / 2, 0], l[3], { dy: 15, cls: hot === 3 ? "hot" : "" })];
  }
  /* divisió d'AB (longitud L) en parts proporcionals a «parts»; step = quants passos de la construcció es dibuixen */
  function divFig(L, parts, step) {
    var tot = parts.reduce(function (s, k) { return s + k; }, 0), a = 32 * PI / 180, u = L * 0.95 / tot, A = [0, 0], B = [L, 0], it = [], acc = 0, Pk = [];
    parts.forEach(function (k) { acc += k; Pk.push([acc * u * Math.cos(a), acc * u * Math.sin(a)]); });
    it.push(["seg", A, B, "hl"]);
    if (step >= 1) it.push(["seg", A, [Pk[Pk.length - 1][0] * 1.08, Pk[Pk.length - 1][1] * 1.08], "tv"]);
    if (step >= 2) for (var j = 1; j <= tot; j++) it.push(["dot", [j * u * Math.cos(a), j * u * Math.sin(a)], "sm"]);
    if (step >= 3) it.push(["seg", Pk[Pk.length - 1], B, "par"]);
    acc = 0;
    if (step >= 4) parts.slice(0, -1).forEach(function (k, i) { acc += k; var X = [L * acc / tot, 0]; it.push(["seg", Pk[i], X, "par"], ["dot", X]); });
    it.push(["dot", A], ["dot", B], T_(A, "A", { dx: -8, a: "end" }), T_(B, "B", { dx: 8, a: "start" }));
    if (step >= 4) { acc = 0; parts.forEach(function (k) { var x0 = L * acc / tot; acc += k; it.push(T_([(x0 + L * acc / tot) / 2, 0], lab(L * k / tot), { dy: 16 })); }); }
    return it;
  }
  /* triangle de costats a (base BC), b (CA) i c (AB) */
  function triSides(a, b, c, X, cls, labs) {
    var B = [X, 0], C = [X + a, 0], xA = (a * a + c * c - b * b) / (2 * a), A = [X + xA, Math.sqrt(Math.max(c * c - xA * xA, 0))];
    var it = [["poly", [A, B, C], cls]];
    if (labs) it.push(T_(mid(B, C), labs[0], { dy: 15 }), T_(mid(C, A), labs[1], { dx: 9, a: "start" }), T_(mid(A, B), labs[2], { dx: -9, a: "end" }));
    return it;
  }
  function ok3(s) { s = s.slice().sort(function (x, y) { return x - y; }); return s[2] < s[0] + s[1] - 1e-9; }

  /* ---------- 10.1 calculadora de proporcions ---------- */
  function quartSteps(v) {
    var miss = ["a", "b", "c", "d"].filter(function (k) { return v[k] == null; })[0], a = v.a, b = v.b, c = v.c, d = v.d, x;
    var P = "\\dfrac{" + (a == null ? "x" : nf(a)) + "}{" + (b == null ? "x" : nf(b)) + "}=\\dfrac{" + (c == null ? "x" : nf(c)) + "}{" + (d == null ? "x" : nf(d)) + "}";
    var rows = [tex(P)];
    if (miss === "a" || miss === "d") { var k1 = miss === "a" ? d : a, num = b * c; x = num / k1; rows.push(tex(nf(k1) + "\\cdot x=" + nf(b) + "\\cdot" + nf(c) + "=" + nf(num) + "\\ \\Rightarrow\\ x=\\dfrac{" + nf(num) + "}{" + nf(k1) + "}" + eq(x))); }
    else { var k2 = miss === "b" ? c : b, num2 = a * d; x = num2 / k2; rows.push(tex(nf(k2) + "\\cdot x=" + nf(a) + "\\cdot" + nf(d) + "=" + nf(num2) + "\\ \\Rightarrow\\ x=\\dfrac{" + nf(num2) + "}{" + nf(k2) + "}" + eq(x))); }
    return { rows: rows, v: x, miss: miss };
  }
  function segBars(vals, names) {
    var it = [], y = 0, m = Math.max.apply(null, vals);
    vals.forEach(function (v, i) { var l = v / m * 8; it.push(["seg", [0, y], [l, y], "hl"], ["dot", [0, y]], ["dot", [l, y]], T_([0, y], names[i], { dx: -8, a: "end" }), T_([l / 2, y], lab(v), { dy: -7 })); y -= 1.1; });
    return G(it, { W: 280, maxh: 200, pad: 30 });
  }
  function wQuart() {
    var w = document.getElementById("w-quart"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), g = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      out.innerHTML = g.innerHTML = info.innerHTML = "";
      var v = {}, bad = false, blanks = 0;
      ["a", "b", "c", "d"].forEach(function (k) { v[k] = rd(I, k); if (v[k] === null) blanks++; else if (isNaN(v[k])) bad = true; });
      if (bad) { info.innerHTML = warn(u("num")); return; }
      if (blanks === 0) {
        var l = v.a * v.d, r = v.b * v.c, yes = Math.abs(l - r) < 1e-9;
        out.innerHTML = rows2html([tex(nf(v.a) + "\\cdot" + nf(v.d) + "=" + nf(l) + "\\qquad " + nf(v.b) + "\\cdot" + nf(v.c) + "=" + nf(r)),
          yes ? '<span class="ok">✓ ' + T(L3("Són proporcionals (el producte dels extrems és igual al dels mitjans).", "Son proporcionales (el producto de los extremos es igual al de los medios).", "They are proportional (product of extremes = product of means).")) + "</span>"
              : '<span class="ko">✗ ' + T(L3("No són proporcionals.", "No son proporcionales.", "They are not proportional.")) + "</span>"]);
        g.innerHTML = segBars([v.a, v.b, v.c, v.d], ["a", "b", "c", "d"]);
        return;
      }
      if (blanks !== 1) { info.innerHTML = warn(T(L3("Escriu tres valors i deixa en blanc el que vols calcular (o escriu-ne quatre per a comprovar si són proporcionals).", "Escribe tres valores y deja en blanco el que quieres calcular (o escribe cuatro para comprobar si son proporcionales).", "Type three values and leave blank the one you want (or type all four to check whether they're proportional)."))); return; }
      var r_ = quartSteps(v); v[r_.miss] = r_.v;
      out.innerHTML = rows2html([T(L3("Multipliquem en creu i aïllem la x:", "Multiplicamos en cruz y despejamos la x:", "Cross-multiply and solve for x:"))].concat(r_.rows));
      g.innerHTML = segBars([v.a, v.b, v.c, v.d], ["a", "b", "c", "d"]);
    }
    ["a", "b", "c", "d"].forEach(function (k) { I[k].addEventListener("input", paint); });
    quickBind(w, function (q) { I.a.value = q[0]; I.b.value = q[1]; I.c.value = q[2]; I.d.value = q[3]; paint(); });
    onLang(paint);
  }

  /* ---------- 10.2 teorema de Tales ---------- */
  function wTales() {
    var w = document.getElementById("w-tales"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var q1 = +I.d1.value, q2 = +I.d2.value, ga = +I.ga.value, gb = +I.gb.value;
      showRv(w, "d1", "d_1", q1); showRv(w, "d2", "d_2", q2);
      var e = w.querySelector(".gav"); if (e) e.innerHTML = tex("\\hat a=" + ga + "^\\circ"); e = w.querySelector(".gbv"); if (e) e.innerHTML = tex("\\hat b=" + gb + "^\\circ");
      var sa = Math.sin(ga * PI / 180), sb = Math.sin(gb * PI / 180), AB = q1 / sa, BC = q2 / sa, A1 = q1 / sb, B1 = q2 / sb;
      out.innerHTML = G(talesFig(q1, q2, ga, gb, { AB: lab(AB), BC: lab(BC), A1B1: lab(A1), B1C1: lab(B1) }, "", 2.6), { W: 320, maxh: 280, pad: 30 }) + gcol([
        T(L3("Mesures sobre la secant a:", "Medidas sobre la secante a:", "Lengths on line a:")) + " " + tex("\\overline{AB}\\approx" + d2(AB) + ",\\ \\ \\overline{BC}\\approx" + d2(BC)),
        T(L3("Mesures sobre la secant b:", "Medidas sobre la secante b:", "Lengths on line b:")) + " " + tex("\\overline{A'B'}\\approx" + d2(A1) + ",\\ \\ \\overline{B'C'}\\approx" + d2(B1)),
        '<span class="big">' + tex("\\dfrac{\\overline{AB}}{\\overline{BC}}\\approx" + d2(AB / BC) + "\\qquad\\dfrac{\\overline{A'B'}}{\\overline{B'C'}}\\approx" + d2(A1 / B1)) + "</span>",
        tex("\\dfrac{\\overline{AB}}{\\overline{A'B'}}\\approx" + d2(AB / A1) + "\\qquad\\dfrac{\\overline{BC}}{\\overline{B'C'}}\\approx" + d2(BC / B1)),
        "💡 " + T(L3("Canvia la inclinació de les secants: els segments canvien, però les raons es mantenen iguals.", "Cambia la inclinación de las secantes: los segmentos cambian, pero las razones se mantienen iguales.", "Change the slope of the lines: the segments change, but the ratios stay equal."))]);
    }
    ["d1", "d2", "ga", "gb"].forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 10.3 divisió d'un segment ---------- */
  function partsIn(s) {
    var a = String(s).replace(/[;:]/g, ",").split(/[,\s]+/).filter(Boolean).map(numIn);
    return a.length >= 2 && a.length <= 8 && a.every(function (v) { return v !== null && v > 0 && isInt(v) && v <= 12; }) ? a : null;
  }
  function wDiv() {
    var w = document.getElementById("w-div"); if (!w) return;
    var I = inputs(w), g = w.querySelector(".gout"), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), mode = "eq", step = 4;
    var STEPS = [L3("Segment AB.", "Segmento AB.", "Segment AB."), L3("1. Traça una semirecta auxiliar des d'A.", "1. Traza una semirrecta auxiliar desde A.", "1. Draw an auxiliary ray from A."),
      L3("2. Marca-hi amb el compàs {n} segments iguals.", "2. Marca en ella con el compás {n} segmentos iguales.", "2. Mark {n} equal segments on it with the compasses."),
      L3("3. Uneix l'última marca amb B.", "3. Une la última marca con B.", "3. Join the last mark to B."),
      L3("4. Traça paral·leles per les marques: tallen AB en les parts buscades.", "4. Traza paralelas por las marcas: cortan AB en las partes buscadas.", "4. Draw parallels through the marks: they cut AB into the required parts.")];
    function paint() {
      g.innerHTML = out.innerHTML = info.innerHTML = "";
      w.querySelector(".eqonly").closest("label").style.display = mode === "eq" ? "" : "none";
      w.querySelector(".pronly").closest("label").style.display = mode === "pr" ? "" : "none";
      var L = numIn(I.L.value), parts;
      if (L === null || L <= 0 || L > 100) { info.innerHTML = warn(u("num")); return; }
      if (mode === "eq") { var n = numIn(I.n.value); if (n === null || !isInt(n) || n < 2 || n > 12) { info.innerHTML = warn(T(L3("El nombre de parts ha de ser un enter entre 2 i 12.", "El número de partes debe ser un entero entre 2 y 12.", "The number of parts must be a whole number from 2 to 12."))); return; } parts = []; for (var i = 0; i < n; i++) parts.push(1); }
      else { parts = partsIn(I.k.value); if (!parts) { info.innerHTML = warn(T(L3("Escriu entre 2 i 8 nombres enters (fins a 12) separats per comes: 2, 3, 4.", "Escribe entre 2 y 8 números enteros (hasta 12) separados por comas: 2, 3, 4.", "Type 2 to 8 whole numbers (up to 12) separated by commas: 2, 3, 4."))); return; } }
      var tot = parts.reduce(function (s, k) { return s + k; }, 0);
      g.innerHTML = G(divFig(L, parts, step), { W: 340, maxh: 230, pad: 26 });
      var rows = ["<strong>" + fill(T(STEPS[step]), { n: tot }) + "</strong>"];
      if (step === 4) {
        if (mode === "eq") rows.push(tex("\\dfrac{" + nf(L) + "}{" + tot + "}" + eq(L / tot)));
        else rows.push(tex("\\dfrac{" + nf(L) + "}{" + parts.join("+") + "}=\\dfrac{" + nf(L) + "}{" + tot + "}" + eq(L / tot)) + "<br>" + parts.map(function (k) { return tex(k + "\\cdot" + (Math.abs(L / tot * 1000 - Math.round(L / tot * 1000)) < 1e-6 ? nf(L / tot) : "\\tfrac{" + nf(L) + "}{" + tot + "}") + eq(k * L / tot)); }).join(" &nbsp; "));
      }
      out.innerHTML = rows2html(rows);
    }
    segBind(w, function (k) { mode = k; step = 4; paint(); });
    ["L", "n", "k"].forEach(function (k) { I[k].addEventListener("input", function () { step = 4; paint(); }); });
    w.querySelector('[data-a="step"]').addEventListener("click", function () { step = (step + 1) % 5; paint(); });
    onLang(paint);
  }

  /* ---------- 10.4 triangles en posició de Tales ---------- */
  function wTpos() {
    var w = document.getElementById("w-tpos"); if (!w) return;
    var S = sliders(w), I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      var t = +S.t.value, a = numIn(I.AB.value), b = numIn(I.AC.value), c = numIn(I.BC.value);
      showRv(w, "t", "k", t); info.innerHTML = "";
      if ([a, b, c].some(function (v) { return v === null || v <= 0; })) { info.innerHTML = warn(u("num")); out.innerHTML = ""; return; }
      if (!ok3([a, b, c])) { info.innerHTML = warn(T(L3("Amb aquests costats no hi ha triangle: el més llarg ha de ser menor que la suma dels altres dos.", "Con estos lados no hay triángulo: el más largo debe ser menor que la suma de los otros dos.", "These sides don't make a triangle: the longest must be shorter than the sum of the other two."))); out.innerHTML = ""; return; }
      var ang = Math.acos((a * a + b * b - c * c) / (2 * a * b)) * 180 / PI;
      out.innerHTML = G(tposFig(a, b, ang, t, { AB1: lab(a * t), B1B: lab(a * (1 - t)), AC1: lab(b * t), C1C: lab(b * (1 - t)), B1C1: lab(c * t), BC: lab(c) }), { W: 280, maxh: 260, pad: 34 }) + gcol([
        tex("\\dfrac{\\overline{AB'}}{\\overline{AB}}=\\dfrac{" + n4(a * t) + "}{" + nf(a) + "}" + eq(t)),
        tex("\\dfrac{\\overline{AC'}}{\\overline{AC}}=\\dfrac{" + n4(b * t) + "}{" + nf(b) + "}" + eq(t)),
        tex("\\dfrac{\\overline{B'C'}}{\\overline{BC}}=\\dfrac{" + n4(c * t) + "}{" + nf(c) + "}" + eq(t)),
        '<span class="ko">' + tex("\\dfrac{\\overline{AB'}}{\\overline{B'B}}" + eq(t / (1 - t))) + "</span> " + T(L3("≠ les altres: no serveix per al costat paral·lel!", "≠ las otras: ¡no sirve para el lado paralelo!", "≠ the others: it doesn't work for the parallel side!"))]);
    }
    S.t.addEventListener("input", paint); ["AB", "AC", "BC"].forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 10.5 figures semblants ---------- */
  var SHAPES = {
    L: { p: [[0, 0], [4, 0], [4, 1], [1.5, 1], [1.5, 3], [0, 3]], A: 4 * 1 + 1.5 * 2 },
    T: { p: [[0, 0], [4, 0], [1, 3]], A: 6 },
    R: { p: [[0, 0], [3, 0], [3, 2], [0, 2]], A: 6 }
  };
  function perim(p) { var s = 0; p.forEach(function (P, i) { var Q = p[(i + 1) % p.length]; s += Math.hypot(Q[0] - P[0], Q[1] - P[1]); }); return s; }
  function wSem() {
    var w = document.getElementById("w-sem"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), shape = "L";
    function paint() {
      var k = +I.k.value, F = SHAPES[shape], p = F.p, gap = 1.2, W0 = Math.max.apply(null, p.map(function (q) { return q[0]; }));
      showRv(w, "k", "k", k);
      var Q = p.map(function (q) { return [q[0] * k + W0 + gap, q[1] * k]; }), P0 = perim(p), it = [["poly", p, "gf"], ["poly", Q, "tr"]];
      it.push(T_([W0 / 2, 0], "F", { dy: 15 }), T_([W0 + gap + W0 * k / 2, 0], "F′", { dy: 15 }));
      out.innerHTML = G(it, { W: 340, maxh: 240, pad: 22 }) + gcol([
        T(L3("Raó de semblança:", "Razón de semejanza:", "Scale factor:")) + " " + tex("k=" + nf(k)) + " → " + T(k > 1 ? L3("ampliació", "ampliación", "enlargement") : k < 1 ? L3("reducció", "reducción", "reduction") : L3("figures iguals", "figuras iguales", "congruent figures")),
        T(L3("Perímetres:", "Perímetros:", "Perimeters:")) + " " + tex("P\\approx" + d2(P0) + ",\\ \\ P'\\approx" + d2(P0 * k) + "\\ \\Rightarrow\\ \\dfrac{P'}{P}=" + nf(k)),
        T(L3("Àrees:", "Áreas:", "Areas:")) + " " + tex("A=" + nf(F.A) + ",\\ \\ A'=" + n4(F.A * k * k) + "\\ \\Rightarrow\\ \\dfrac{A'}{A}=" + n4(k * k) + "=k^2")]);
    }
    segBind(w, function (s) { shape = s; paint(); });
    I.k.addEventListener("input", paint);
    onLang(paint);
  }

  /* ---------- 10.6 criteris de semblança ---------- */
  function simCheck(s1, s2) {
    var a = s1.slice().sort(function (x, y) { return x - y; }), b = s2.slice().sort(function (x, y) { return x - y; });
    var r = [b[0] / a[0], b[1] / a[1], b[2] / a[2]], yes = Math.abs(r[0] - r[1]) < 1e-9 && Math.abs(r[1] - r[2]) < 1e-9;
    var row = tex("\\dfrac{" + nf(b[0]) + "}{" + nf(a[0]) + "}" + eq(r[0]) + "\\qquad\\dfrac{" + nf(b[1]) + "}{" + nf(a[1]) + "}" + eq(r[1]) + "\\qquad\\dfrac{" + nf(b[2]) + "}{" + nf(a[2]) + "}" + eq(r[2]));
    return { yes: yes, k: r[0], row: row, a: a, b: b };
  }
  function wCrit() {
    var w = document.getElementById("w-crit"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), g = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      out.innerHTML = g.innerHTML = info.innerHTML = "";
      var s1 = ["a", "b", "c"].map(function (k) { return numIn(I[k].value); }), s2 = ["d", "e", "f"].map(function (k) { return numIn(I[k].value); });
      if (s1.concat(s2).some(function (v) { return v === null || v <= 0; })) { info.innerHTML = warn(u("num")); return; }
      if (!ok3(s1) || !ok3(s2)) { info.innerHTML = warn(T(L3("Algun dels dos no és un triangle: el costat més llarg ha de ser menor que la suma dels altres dos.", "Alguno de los dos no es un triángulo: el lado más largo debe ser menor que la suma de los otros dos.", "One of them isn't a triangle: the longest side must be shorter than the sum of the other two."))); return; }
      var r = simCheck(s1, s2);
      out.innerHTML = rows2html([T(L3("Ordenem els costats i els dividim en el mateix ordre:", "Ordenamos los lados y los dividimos en el mismo orden:", "Sort the sides and divide them in the same order:")) + " " + tex("(" + r.a.map(nf).join(",\\ ") + ")\\ \\to\\ (" + r.b.map(nf).join(",\\ ") + ")"), r.row,
        r.yes ? '<span class="ok">✓ ' + fill(T(L3("Són semblants (criteri dels costats), amb raó k = {k}.", "Son semejantes (criterio de los lados), con razón k = {k}.", "They are similar (SSS), with k = {k}.")), { k: lab(r.k) }) + "</span>" : '<span class="ko">✗ ' + T(L3("Les raons no coincideixen: no són semblants.", "Las razones no coinciden: no son semejantes.", "The ratios differ: they are not similar.")) + "</span>"]);
      var m = Math.max(r.a[2], r.b[2]), f = 6 / m;
      var A = r.a.map(function (v) { return v * f; }), B = r.b.map(function (v) { return v * f; });
      g.innerHTML = G(triSides(A[2], A[1], A[0], 0, "gf", r.a.slice().reverse().map(lab)).concat(triSides(B[2], B[1], B[0], A[2] + 1, "tr", r.b.slice().reverse().map(lab))), { W: 340, maxh: 200, pad: 24 });
    }
    ["a", "b", "c", "d", "e", "f"].forEach(function (k) { I[k].addEventListener("input", paint); });
    quickBind(w, function (q) { ["a", "b", "c", "d", "e", "f"].forEach(function (k, i) { I[k].value = q[i]; }); paint(); });
    onLang(paint);
  }

  /* ---------- 10.7 ombres ---------- */
  function wOmbra() {
    var w = document.getElementById("w-ombra"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var h = +I.h.value, s = +I.s.value, S = +I.S.value, H = h * S / s;
      showRv(w, "h", "h", h); showRv(w, "s", "s", s); showRv(w, "S", "S", S);
      var f = 1; if (H > 40) f = 40 / H;
      out.innerHTML = G(shadowFig(h, s, H * f, S * f, [lab(h) + " m", lab(s) + " m", "H", lab(S) + " m"], 2), { W: 330, maxh: 240, pad: 30 }) + gcol([
        T(L3("Els rajos són paral·lels: els dos triangles són semblants.", "Los rayos son paralelos: los dos triángulos son semejantes.", "The rays are parallel: the two triangles are similar.")),
        tex("\\dfrac{H}{" + nf(S) + "}=\\dfrac{" + nf(h) + "}{" + nf(s) + "}\\ \\Rightarrow\\ H=\\dfrac{" + nf(h) + "\\cdot" + nf(S) + "}{" + nf(s) + "}" + eq(H) + "\\ \\text{m}"),
        f < 1 ? "<em>" + T(L3("(El dibuix de l'edifici no està a escala.)", "(El dibujo del edificio no está a escala.)", "(The building isn't drawn to scale.)")) + "</em>" : ""]);
    }
    ["h", "s", "S"].forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 10.8 escales i k, k², k³ ---------- */
  /* longitud en cm escrita amb la millor unitat */
  function lenTxt(cm) {
    if (cm >= 100000) return nf(cm / 100000) + "\\ \\text{km}";
    if (cm >= 100) return nf(cm / 100) + "\\ \\text{m}";
    return nf(cm) + "\\ \\text{cm}";
  }
  function wEscala() {
    var w = document.getElementById("w-escala"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), info = w.querySelector(".info"), mode = "r";
    function lbl(k, on) { I[k].closest("label").style.opacity = on ? "1" : ".55"; I[k].readOnly = !on; }
    function paint() {
      out.innerHTML = info.innerHTML = "";
      lbl("n", mode !== "e"); lbl("p", mode !== "p"); lbl("r", mode !== "r");
      var n = numIn(I.n.value), p = numIn(I.p.value), r = numIn(I.r.value);
      if (mode === "r") {
        if (n === null || p === null || n <= 0 || p <= 0) { info.innerHTML = warn(u("num")); return; }
        var cm = p * n; I.r.value = lab(cm / 100000);
        out.innerHTML = rows2html([tex(nf(p) + "\\ \\text{cm}\\cdot" + nf(n) + "=" + nf(cm) + "\\ \\text{cm}=" + lenTxt(cm)), T(L3("Cada cm del plànol són {n} cm reals.", "Cada cm del plano son {n} cm reales.", "Each cm on the map is {n} real cm.")).replace("{n}", lab(n))]);
      } else if (mode === "p") {
        if (n === null || r === null || n <= 0 || r <= 0) { info.innerHTML = warn(u("num")); return; }
        var rc = r * 100000, pc = rc / n; I.p.value = lab(pc);
        out.innerHTML = rows2html([tex(nf(r) + "\\ \\text{km}=" + nf(rc) + "\\ \\text{cm}"), tex(nf(rc) + ":" + nf(n) + eq(pc) + "\\ \\text{cm}")]);
      } else {
        if (p === null || r === null || p <= 0 || r <= 0) { info.innerHTML = warn(u("num")); return; }
        var rc2 = r * 100000, n2 = rc2 / p; I.n.value = lab(n2);
        out.innerHTML = rows2html([tex(nf(r) + "\\ \\text{km}=" + nf(rc2) + "\\ \\text{cm}"), tex("\\dfrac{" + nf(p) + "}{" + nf(rc2) + "}=\\dfrac{1}{" + nf(n2) + "}\\ \\Rightarrow\\ " + T(L3("\\text{escala }", "\\text{escala }", "\\text{scale }")) + "1:" + nf(n2))]);
      }
    }
    segBind(w, function (k) { mode = k; paint(); });
    ["n", "p", "r"].forEach(function (k) { I[k].addEventListener("input", function () { if (!I[k].readOnly) paint(); }); });
    onLang(paint);
  }
  /* cub de k × k × k cubets en perspectiva isomètrica */
  function cubeK(k) {
    var it = [], c = Math.cos(PI / 6), s = 0.5;
    function P(x, y, z) { return [(x - y) * c, (x + y) * s + z]; }
    var i, j;
    for (i = 0; i < k; i++) for (j = 0; j < k; j++) {
      it.push(["poly", [P(i, 0, j), P(i + 1, 0, j), P(i + 1, 0, j + 1), P(i, 0, j + 1)], "cube"]);
      it.push(["poly", [P(0, i, j), P(0, i + 1, j), P(0, i + 1, j + 1), P(0, i, j + 1)], "cube c3"]);
      it.push(["poly", [P(i, j, k), P(i + 1, j, k), P(i + 1, j + 1, k), P(i, j + 1, k)], "cube c2"]);
    }
    return it.map(function (q) { q[1] = q[1].map(function (p) { return [-p[0], p[1]]; }); return q; });
  }
  function wK() {
    var w = document.getElementById("w-k"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var k = +I.k.value; showRv(w, "k", "k", k);
      out.innerHTML = G(cubeK(1), { W: 90, maxh: 90, pad: 14 }) + G(cubeK(k), { W: 230, maxh: 230, pad: 14 }) + gcol([
        T(L3("Aresta:", "Arista:", "Edge:")) + " " + tex("1\\ \\to\\ " + k) + " " + T(L3("(per k)", "(por k)", "(times k)")),
        T(L3("Àrea d'una cara:", "Área de una cara:", "Area of a face:")) + " " + tex("1\\ \\to\\ " + k + "^2=" + k * k) + " " + T(L3("quadrets (per k²)", "cuadraditos (por k²)", "small squares (times k²)")),
        T(L3("Volum:", "Volumen:", "Volume:")) + " " + tex("1\\ \\to\\ " + k + "^3=" + k * k * k) + " " + T(L3("cubets (per k³)", "cubitos (por k³)", "small cubes (times k³)"))]);
    }
    I.k.addEventListener("input", paint);
    onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function optsTxt(right, wrongs) {
    var all = [right].concat(wrongs), order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return all[i]; }), ans: order.indexOf(0) };
  }
  function numQ(v) { return { num: v, tol: tolOf(v) }; }
  function ret(o, q, s) { o.q = q; o.s = s; return o; }
  function $n(v) { return "$" + nf(v) + "$"; }
  /* tres valors enters amb quart proporcional amb com a molt 2 decimals */
  function nice4() { var a, b, c, x; do { a = rint(2, 12); b = rint(2, 15); c = rint(2, 20); x = b * c / a; } while (a === b || Math.abs(x * 100 - Math.round(x * 100)) > 1e-9 || x > 60); return [a, b, c, x]; }
  var YES = L3("Sí, són semblants", "Sí, son semejantes", "Yes, they are similar"), NO = L3("No són semblants", "No son semejantes", "They are not similar");
  var GEN = {
    quart: function () {
      var v = nice4(), pos = rint(0, 3), vals = [v[0], v[1], v[2], v[3]], ans;
      /* la incògnita pot anar a qualsevol lloc: a/b = c/x, x/b = c/d… */
      var o = { a: vals[0], b: vals[1], c: vals[2], d: vals[3] }, key = ["a", "b", "c", "d"][pos]; ans = o[key]; o[key] = null;
      var r = quartSteps(o);
      function f(k) { return o[k] == null ? "x" : nf(o[k]); }
      return ret(numQ(ans), function () { return T(L3("Calcula x:", "Calcula x:", "Find x:")) + " $\\dfrac{" + f("a") + "}{" + f("b") + "}=\\dfrac{" + f("c") + "}{" + f("d") + "}$"; }, function () { return r.rows.join(" "); });
    },
    tales: function () {
      var v = nice4(), a = v[0], b = v[1], c = v[2], x = v[3], t = rint(0, 3), labs, hot, prop;
      /* a/b = c/x amb a = AB, b = BC, c = A′B′, x = B′C′ (o bé girat) */
      if (t === 0) { labs = { AB: nf(a).replace("\\dc ", ","), BC: lab(b), A1B1: lab(c), B1C1: "x" }; hot = "B1C1"; prop = "\\dfrac{" + nf(a) + "}{" + nf(b) + "}=\\dfrac{" + nf(c) + "}{x}"; }
      else if (t === 1) { labs = { AB: lab(c), BC: "x", A1B1: lab(a), B1C1: lab(b) }; hot = "BC"; prop = "\\dfrac{" + nf(c) + "}{x}=\\dfrac{" + nf(a) + "}{" + nf(b) + "}"; }
      else if (t === 2) { labs = { AB: lab(a), BC: lab(b), A1B1: lab(c), B1C1: "x" }; hot = "B1C1"; prop = "\\dfrac{" + nf(a) + "}{" + nf(c) + "}=\\dfrac{" + nf(b) + "}{x}"; }
      else { labs = { AB: "x", BC: lab(c), A1B1: lab(b), B1C1: lab(a) }; hot = "AB"; x = b * c / a; prop = "\\dfrac{x}{" + nf(c) + "}=\\dfrac{" + nf(b) + "}{" + nf(a) + "}"; }
      var y1 = 2 + Math.random(), y2 = y1 * (t === 3 ? a / b : b / a);
      y2 = Math.max(1.2, Math.min(y2, 5));
      return ret(numQ(x), function () { return T(L3("Les rectes morades són paral·leles. Calcula x.", "Las rectas moradas son paralelas. Calcula x.", "The purple lines are parallel. Find x.")) + G(talesFig(y1, y2, 62, 80, labs, hot, 2.4), { W: 270, maxh: 220, pad: 34 }); },
        function () { return tex(prop + "\\ \\Rightarrow\\ x" + eq(x)); });
    },
    div: function () {
      var parts, L, tot, u_;
      do { var n = rint(2, 3); parts = []; for (var i = 0; i < n; i++) parts.push(rint(1, 6)); tot = parts.reduce(function (s, k) { return s + k; }, 0); u_ = pick([0.5, 1, 1.5, 2, 2.5, 3, 4]); L = tot * u_; } while (L > 60 || parts[0] === parts[1]);
      var j = rint(0, parts.length - 1), names = L3("primera", "primera", "first"), ord = [L3("primera", "primera", "first"), L3("segona", "segunda", "second"), L3("tercera", "tercera", "third")][j];
      return ret(numQ(parts[j] * u_), function () { return fill(T(L3("Dividim un segment de {L} cm en parts proporcionals a {p}. Quant fa la {o} part?", "Dividimos un segmento de {L} cm en partes proporcionales a {p}. ¿Cuánto mide la {o} parte?", "A {L} cm segment is divided into parts proportional to {p}. How long is the {o} part?")), { L: $n(L), p: "$" + parts.join(",\\ ") + "$", o: T(ord) }); },
        function () { return tex("\\dfrac{" + nf(L) + "}{" + parts.join("+") + "}=" + nf(u_) + "\\qquad " + parts[j] + "\\cdot" + nf(u_) + "=" + nf(parts[j] * u_)); });
    },
    tpos: function () {
      var t = rint(0, 2), AB1 = rint(2, 9), B1B = rint(2, 9), AB = AB1 + B1B, BC, x, labs, hot, rows;
      do { BC = rint(4, 18); x = AB1 * BC / AB; } while (Math.abs(x * 100 - Math.round(x * 100)) > 1e-9);
      if (t === 0) { labs = { AB1: lab(AB1), B1B: lab(B1B), BC: lab(BC), B1C1: "x" }; hot = "B1C1"; rows = tex("\\overline{AB}=" + AB1 + "+" + B1B + "=" + AB + "\\qquad\\dfrac{" + AB1 + "}{" + AB + "}=\\dfrac{x}{" + BC + "}\\ \\Rightarrow\\ x" + eq(x)); }
      else if (t === 1) { var v = x; x = BC; labs = { AB1: lab(AB1), B1B: lab(B1B), B1C1: lab(v), BC: "x" }; hot = "BC"; rows = tex("\\overline{AB}=" + AB1 + "+" + B1B + "=" + AB + "\\qquad\\dfrac{" + AB1 + "}{" + AB + "}=\\dfrac{" + nf(v) + "}{x}\\ \\Rightarrow\\ x" + eq(x)); }
      else { var AC1 = rint(2, 12); x = AC1 * B1B / AB1; if (Math.abs(x * 100 - Math.round(x * 100)) > 1e-9) { AC1 = AB1 * rint(1, 3); x = AC1 * B1B / AB1; } labs = { AB1: lab(AB1), B1B: lab(B1B), AC1: lab(AC1), C1C: "x" }; hot = "C1C"; rows = tex("\\dfrac{" + AB1 + "}{" + B1B + "}=\\dfrac{" + AC1 + "}{x}\\ \\Rightarrow\\ x" + eq(x)); }
      var tt = AB1 / AB;
      return ret(numQ(x), function () { return T(L3("En el triangle, B′C′ ∥ BC. Calcula x.", "En el triángulo, B′C′ ∥ BC. Calcula x.", "In the triangle, B′C′ ∥ BC. Find x.")) + G(tposFig(6, 6.6, 50, Math.max(0.3, Math.min(tt, 0.75)), labs, hot), { W: 250, maxh: 220, pad: 34 }); }, function () { return rows; });
    },
    sem: function () {
      var t = rint(0, 2), a = rint(2, 9), b = a + rint(1, 6), k = pick([0.5, 1.5, 2, 2.5, 3, 4]);
      if (t === 0) return ret(numQ(b * k), function () { return fill(T(L3("Un rectangle de {a} cm × {b} cm és semblant a un altre que té el costat menut de {c} cm. Quant fa el costat gran?", "Un rectángulo de {a} cm × {b} cm es semejante a otro que tiene el lado pequeño de {c} cm. ¿Cuánto mide el lado grande?", "An {a} cm × {b} cm rectangle is similar to another whose short side is {c} cm. How long is its long side?")), { a: $n(a), b: $n(b), c: $n(a * k) }); },
        function () { return tex("k=\\dfrac{" + nf(a * k) + "}{" + a + "}=" + nf(k) + "\\qquad " + b + "\\cdot" + nf(k) + "=" + nf(b * k)); });
      var A = rint(3, 30);
      if (t === 1) return ret(numQ(A * k * k), function () { return fill(T(L3("Una figura té {A} cm² d'àrea. Quina àrea té una figura semblant amb raó de semblança {k}?", "Una figura tiene {A} cm² de área. ¿Qué área tiene una figura semejante con razón de semejanza {k}?", "A shape has an area of {A} cm². What is the area of a similar shape with scale factor {k}?")), { A: $n(A), k: $n(k) }); },
        function () { return tex("A'=" + A + "\\cdot" + nf(k) + "^2=" + A + "\\cdot" + nf(k * k) + "=" + nf(A * k * k)); });
      var P = rint(8, 40);
      return ret(numQ(k), function () { return fill(T(L3("Dos figures semblants tenen perímetres de {p} cm i {q} cm. Quina és la raó de semblança de la segona respecte de la primera?", "Dos figuras semejantes tienen perímetros de {p} cm y {q} cm. ¿Cuál es la razón de semejanza de la segunda respecto de la primera?", "Two similar shapes have perimeters of {p} cm and {q} cm. What is the scale factor from the first to the second?")), { p: $n(P), q: $n(P * k) }); },
        function () { return tex("k=\\dfrac{P'}{P}=\\dfrac{" + nf(P * k) + "}{" + P + "}=" + nf(k)); });
    },
    crit: function () {
      var t = rint(0, 1), yes = rint(0, 1) === 1, q, s;
      if (t === 0) {
        var a; do { a = [rint(2, 9), rint(2, 9), rint(2, 9)]; } while (!ok3(a) || a[0] === a[1] && a[1] === a[2]);
        var k = pick([1.5, 2, 2.5, 3, 0.5]), b = a.map(function (v) { return v * k; });
        if (!yes) { var i = rint(0, 2); b[i] += pick([-1, 1]) * (b[i] > 2 ? 1 : 0.5); if (!ok3(b)) b[i] = a[i] * k + 0.5; }
        var r = simCheck(a, b); yes = r.yes;
        b = shuffle(b.slice());
        q = function () { return fill(T(L3("Són semblants els triangles de costats {a} i {b}?", "¿Son semejantes los triángulos de lados {a} y {b}?", "Are the triangles with sides {a} and {b} similar?")), { a: "$" + a.map(nf).join(",\\ ") + "$", b: "$" + b.map(nf).join(",\\ ") + "$" }); };
        s = function () { return r.row; };
      } else {
        var A1 = rint(3, 10) * 5, B1 = rint(3, 10) * 5; if (A1 + B1 > 160) B1 = 160 - A1 - 5 * rint(1, 3); var C1 = 180 - A1 - B1;
        var two = yes ? shuffle([A1, B1, C1]).slice(0, 2) : [A1, C1 + pick([-10, 10, 5])];
        if (!yes && (two[1] <= 0 || A1 + two[1] >= 180)) two[1] = C1 - 5;
        q = function () { return fill(T(L3("Un triangle té dos angles de {a} i {b}. Un altre en té dos de {c} i {d}. Són semblants?", "Un triángulo tiene dos ángulos de {a} y {b}. Otro tiene dos de {c} y {d}. ¿Son semejantes?", "One triangle has two angles of {a} and {b}. Another has two of {c} and {d}. Are they similar?")), { a: "$" + A1 + "^\\circ$", b: "$" + B1 + "^\\circ$", c: "$" + two[0] + "^\\circ$", d: "$" + two[1] + "^\\circ$" }); };
        s = function () { var x2 = 180 - two[0] - two[1]; return tex(A1 + "^\\circ,\\ " + B1 + "^\\circ,\\ " + C1 + "^\\circ\\qquad " + two[0] + "^\\circ,\\ " + two[1] + "^\\circ,\\ " + x2 + "^\\circ"); };
        var x3 = [two[0], two[1], 180 - two[0] - two[1]].sort(), y3 = [A1, B1, C1].sort(); yes = x3.join() === y3.join();
      }
      var o = optsTxt(yes ? YES : NO, [yes ? NO : YES]);
      return ret({ opts: o.opts, ans: o.ans }, q, s);
    },
    ombra: function () {
      var t = rint(0, 2), h = pick([1, 1.2, 1.5, 1.6, 1.8, 2]), s = pick([0.5, 0.8, 1, 1.2, 1.5, 2, 2.4, 3]), S = rint(4, 30), H = h * S / s, v, q, sol;
      if (t === 0) { v = H; q = L3("Un pal de {h} m fa una ombra de {s} m. Al mateix moment, un edifici fa una ombra de {S} m. Quina altura té l'edifici (en m)?", "Un palo de {h} m da una sombra de {s} m. En el mismo momento, un edificio da una sombra de {S} m. ¿Qué altura tiene el edificio (en m)?", "A {h} m stick casts a {s} m shadow. At the same moment a building casts a {S} m shadow. How tall is the building (in m)?"); sol = "\\dfrac{H}{" + nf(S) + "}=\\dfrac{" + nf(h) + "}{" + nf(s) + "}\\ \\Rightarrow\\ H" + eq(H); }
      else if (t === 1) { H = rint(4, 25); v = S = H * s / h; q = L3("Una persona de {h} m fa una ombra de {s} m. Quina ombra fa al mateix moment un arbre de {H} m (en m)?", "Una persona de {h} m da una sombra de {s} m. ¿Qué sombra da en el mismo momento un árbol de {H} m (en m)?", "A {h} m tall person casts a {s} m shadow. What shadow does an {H} m tree cast at the same moment (in m)?"); sol = "\\dfrac{S}{" + nf(H) + "}=\\dfrac{" + nf(s) + "}{" + nf(h) + "}\\ \\Rightarrow\\ S" + eq(S); }
      else { var e = pick([1.5, 1.6, 1.7]), dm = pick([1, 1.2, 1.5, 2]), D = rint(4, 15); v = H = e * D / dm; q = L3("Els ulls d'una persona estan a {e} m de terra. Veu la punta d'un arbre en un mirall que està a terra, a {d} m d'ella i a {D} m de l'arbre. Quina altura té l'arbre (en m)?", "Los ojos de una persona están a {e} m del suelo. Ve la punta de un árbol en un espejo que está en el suelo, a {d} m de ella y a {D} m del árbol. ¿Qué altura tiene el árbol (en m)?", "A person's eyes are {e} m above the ground. They see the top of a tree in a mirror on the ground {d} m from them and {D} m from the tree. How tall is the tree (in m)?"); sol = "\\dfrac{H}{" + D + "}=\\dfrac{" + nf(e) + "}{" + nf(dm) + "}\\ \\Rightarrow\\ H" + eq(H);
        return ret(numQ(v), function () { return fill(T(q), { e: $n(e), d: $n(dm), D: $n(D) }); }, function () { return tex(sol); }); }
      return ret(numQ(v), function () { return fill(T(q), { h: $n(h), s: $n(s), S: $n(S), H: $n(H) }); }, function () { return tex(sol); });
    },
    escala: function () {
      var t = rint(0, 2), n = pick([50, 100, 200, 500, 1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000]), p, cm;
      var unit = n >= 25000 ? "km" : "m", f = unit === "km" ? 100000 : 100;
      if (t === 0) { p = rint(2, 40) / 2; cm = p * n; return ret(numQ(cm / f), function () { return fill(T(L3("En un plànol a escala {e}, una distància fa {p} cm. Quina és la distància real (en {u})?", "En un plano a escala {e}, una distancia mide {p} cm. ¿Cuál es la distancia real (en {u})?", "On a {e} map a distance is {p} cm. What is the real distance (in {u})?")), { e: "$1:" + nf(n) + "$", p: $n(p), u: unit }); }, function () { return tex(nf(p) + "\\cdot" + nf(n) + "=" + nf(cm) + "\\ \\text{cm}=" + nf(cm / f) + "\\ \\text{" + unit + "}"); }); }
      if (t === 1) { p = rint(2, 40) / 2; cm = p * n; return ret(numQ(p), function () { return fill(T(L3("Dos punts estan a {r} {u} en la realitat. A quina distància estan (en cm) en un plànol a escala {e}?", "Dos puntos están a {r} {u} en la realidad. ¿A qué distancia están (en cm) en un plano a escala {e}?", "Two points are {r} {u} apart in reality. How far apart are they (in cm) on a {e} map?")), { r: $n(cm / f), u: unit, e: "$1:" + nf(n) + "$" }); }, function () { return tex(nf(cm / f) + "\\ \\text{" + unit + "}=" + nf(cm) + "\\ \\text{cm}\\qquad " + nf(cm) + ":" + nf(n) + "=" + nf(p)); }); }
      p = rint(1, 12); cm = p * n;
      return ret(numQ(n), function () { return fill(T(L3("En un mapa, {p} cm representen {r} {u}. Quina és l'escala? Escriu el nombre n de 1 : n.", "En un mapa, {p} cm representan {r} {u}. ¿Cuál es la escala? Escribe el número n de 1 : n.", "On a map, {p} cm stand for {r} {u}. What is the scale? Type the number n in 1 : n.")), { p: $n(p), r: $n(cm / f), u: unit }); }, function () { return tex(nf(cm / f) + "\\ \\text{" + unit + "}=" + nf(cm) + "\\ \\text{cm}\\qquad\\dfrac{" + p + "}{" + nf(cm) + "}=\\dfrac{1}{" + nf(n) + "}"); });
    },
    k23: function () {
      var t = rint(0, 3), k = pick([2, 3, 4, 5, 0.5, 1.5]), v;
      if (t === 0) { var A = rint(2, 40); v = A * k * k; return ret(numQ(v), function () { return fill(T(L3("Ampliem una figura de {A} cm² amb raó {k}. Quina àrea té la nova (en cm²)?", "Ampliamos una figura de {A} cm² con razón {k}. ¿Qué área tiene la nueva (en cm²)?", "A {A} cm² shape is scaled by {k}. What is the new area (in cm²)?")), { A: $n(A), k: $n(k) }); }, function () { return tex(A + "\\cdot" + nf(k) + "^2=" + nf(v)); }); }
      if (t === 1) { var V = rint(2, 30); v = V * k * k * k; return ret(numQ(v), function () { return fill(T(L3("Un cos té {V} cm³ de volum. Quin volum té un cos semblant amb raó {k} (en cm³)?", "Un cuerpo tiene {V} cm³ de volumen. ¿Qué volumen tiene un cuerpo semejante con razón {k} (en cm³)?", "A solid has a volume of {V} cm³. What is the volume of a similar solid with factor {k} (in cm³)?")), { V: $n(V), k: $n(k) }); }, function () { return tex(V + "\\cdot" + nf(k) + "^3=" + V + "\\cdot" + nf(k * k * k) + "=" + nf(v)); }); }
      if (t === 2) { var n = pick([2, 3, 4, 5, 10]); return ret(numQ(n * n), function () { return fill(T(L3("Si multipliquem per {n} totes les longituds d'una figura, per quant queda multiplicada l'àrea?", "Si multiplicamos por {n} todas las longitudes de una figura, ¿por cuánto queda multiplicada el área?", "If every length of a shape is multiplied by {n}, what is the area multiplied by?")), { n: $n(n) }); }, function () { return tex(n + "^2=" + n * n); }); }
      var m = pick([2, 3, 4, 5]); return ret(numQ(m * m * m), function () { return fill(T(L3("Dos cubs tenen arestes de 1 cm i {m} cm. Quantes vegades cap el menut dins del gran?", "Dos cubos tienen aristas de 1 cm y {m} cm. ¿Cuántas veces cabe el pequeño dentro del grande?", "Two cubes have edges of 1 cm and {m} cm. How many times does the small one fit into the big one?")), { m: $n(m) }); }, function () { return tex(m + "^3=" + m * m * m); });
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
  window.FM10 = { G: G, GEN: GEN, numIn: numIn, quartSteps: quartSteps, simCheck: simCheck, talesFig: talesFig };

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

  var TITLES = { va: "Proporcionalitat. Teorema de Tales · FentMates", es: "Proporcionalidad. Teorema de Tales · FentMates", en: "Proportionality. Thales' theorem · FentMates" };
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
    wQuart(); wTales(); wDiv(); wTpos(); wSem(); wCrit(); wOmbra(); wEscala(); wK();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
