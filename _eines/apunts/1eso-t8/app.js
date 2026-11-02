(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u8-done", NSEC = 9;

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
     unitat 8 (1r ESO): àrees i perímetres
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

  /* ---------- nombres per a àrees (π ≈ 3,14) ---------- */
  var P3 = 3.14;
  /* nombre amb fins a 4 decimals */
  function n4(v) { var r = Math.round(v * 10000) / 10000; if (near(r, 0)) r = 0; return String(r).replace(".", "\\dc "); }
  /* "= 78,5" si el resultat té com a molt 4 decimals, "≈ 8,60" si no */
  function ap(v) { return Math.abs(Math.round(v * 10000) / 10000 - v) < 1e-9 ? "=" + n4(v) : "\\approx " + d2(v); }
  /* nombres molt grans o molt menuts (canvis d'unitats), amb espai de milers */
  function dn(v) {
    var s = (+v.toPrecision(12)).toFixed(16).replace(/0+$/, "").replace(/\.$/, ""), p = s.split("."), i = p[0];
    if (i.replace("-", "").length > 4) i = i.replace(/\B(?=(\d{3})+(?!\d))/g, "\\,");
    return i + (p[1] ? "\\dc " + p[1] : "");
  }
  function off(A, B, d) { var M = mid(A, B), dx = B[0] - A[0], dy = B[1] - A[1], n = Math.hypot(dx, dy) || 1; return [M[0] - dy / n * d, M[1] + dx / n * d]; }
  function showRange(w, k, on) { var i = w.querySelector('input[data-k="' + k + '"]'); if (i) i.closest("label").style.display = on ? "" : "none"; }
  function cm(s) { return "\\ \\text{" + s + "}"; }
  var TA = L3("Àrea", "Área", "Area"), TP = L3("Perímetre", "Perímetro", "Perimeter");
  function hA() { return "<b>" + T(TA) + "</b>"; }
  function hP() { return "<b>" + T(TP) + "</b>"; }

  /* ---------- 8.1 quadrícula: àrea i perímetre comptant ---------- */
  function cellPer(on) {
    var p = 0; Object.keys(on).forEach(function (k) { var c = k.split(",").map(Number); [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(function (d) { if (!on[(c[0] + d[0]) + "," + (c[1] + d[1])]) p++; }); }); return p;
  }
  function polyomino(n, NX, NY) {
    var on = {}, cs = [[Math.floor(NX / 2), Math.floor(NY / 2)]]; on[cs[0].join(",")] = 1;
    var guard = 0;
    while (cs.length < n && guard++ < 500) {
      var c = pick(cs), d = pick([[1, 0], [-1, 0], [0, 1], [0, -1]]), x = c[0] + d[0], y = c[1] + d[1];
      if (x < 0 || y < 0 || x >= NX || y >= NY || on[x + "," + y]) continue;
      on[x + "," + y] = 1; cs.push([x, y]);
    }
    return on;
  }
  /* figura de caselles com a elements de G() */
  function cellItems(on, NX, NY) {
    var it = [], x, y;
    Object.keys(on).forEach(function (k) { var c = k.split(",").map(Number); it.push(["poly", [[c[0], c[1]], [c[0] + 1, c[1]], [c[0] + 1, c[1] + 1], [c[0], c[1] + 1]], "gf"]); });
    for (x = 0; x <= NX; x++) it.push(["seg", [x, 0], [x, NY], "gl"]);
    for (y = 0; y <= NY; y++) it.push(["seg", [0, y], [NX, y], "gl"]);
    return it;
  }
  function wGrid() {
    var w = document.getElementById("w-grid"); if (!w) return;
    var NX = 10, NY = 7, S = 28, on = polyomino(7, NX, NY), out = w.querySelector(".gout");
    function paint() {
      var g = "", e = "", x, y, n = Object.keys(on).length, p = cellPer(on);
      for (x = 0; x < NX; x++) for (y = 0; y < NY; y++) {
        var k = x + "," + y;
        g += '<rect class="gcell' + (on[k] ? " on" : "") + '" data-c="' + k + '" x="' + (6 + x * S) + '" y="' + (6 + y * S) + '" width="' + S + '" height="' + S + '"/>';
        if (on[k]) {
          var X0 = 6 + x * S, Y0 = 6 + y * S;
          if (!on[x + "," + (y - 1)]) e += '<line class="gedge" x1="' + X0 + '" y1="' + Y0 + '" x2="' + (X0 + S) + '" y2="' + Y0 + '"/>';
          if (!on[x + "," + (y + 1)]) e += '<line class="gedge" x1="' + X0 + '" y1="' + (Y0 + S) + '" x2="' + (X0 + S) + '" y2="' + (Y0 + S) + '"/>';
          if (!on[(x - 1) + "," + y]) e += '<line class="gedge" x1="' + X0 + '" y1="' + Y0 + '" x2="' + X0 + '" y2="' + (Y0 + S) + '"/>';
          if (!on[(x + 1) + "," + y]) e += '<line class="gedge" x1="' + (X0 + S) + '" y1="' + Y0 + '" x2="' + (X0 + S) + '" y2="' + (Y0 + S) + '"/>';
        }
      }
      var W = NX * S + 12, H = NY * S + 12;
      out.innerHTML = '<svg class="gfig w-grid-svg" viewBox="0 0 ' + W + " " + H + '" style="max-width:' + W + 'px" role="img" aria-label="quadrícula">' + g + e + "</svg>" +
        gcol([hA() + ": " + fill(T(L3("{n} quadrets pintats", "{n} cuadraditos pintados", "{n} shaded squares")), { n: n }) + " → " + tex("A=" + n + cm("cm") + "^2"),
          hP() + ": " + fill(T(L3("{p} costats de quadret en el contorn (en taronja)", "{p} lados de cuadradito en el contorno (en naranja)", "{p} square sides on the boundary (in orange)")), { p: p }) + " → " + tex("P=" + p + cm("cm")),
          n ? "💡 " + T(L3("Prova de canviar la forma sense canviar el nombre de quadrets: l'àrea es manté, però el perímetre canvia.", "Prueba a cambiar la forma sin cambiar el número de cuadraditos: el área se mantiene, pero el perímetro cambia.", "Try changing the shape without changing the number of squares: the area stays the same, but the perimeter changes.")) : ""]);
    }
    out.addEventListener("click", function (ev) {
      var r = ev.target.closest && ev.target.closest("rect[data-c]"); if (!r) return;
      var k = r.getAttribute("data-c"); if (on[k]) delete on[k]; else on[k] = 1; paint();
    });
    w.querySelector('[data-a="rnd"]').addEventListener("click", function () { on = polyomino(rint(5, 14), NX, NY); paint(); });
    w.querySelector('[data-a="rect"]').addEventListener("click", function () {
      var b = rint(2, 8), h = rint(2, 6), x0 = rint(0, NX - b), y0 = rint(0, NY - h), x, y; on = {};
      for (x = 0; x < b; x++) for (y = 0; y < h; y++) on[(x0 + x) + "," + (y0 + y)] = 1; paint();
    });
    w.querySelector('[data-a="clr"]').addEventListener("click", function () { on = {}; paint(); });
    onLang(paint);
  }

  /* ---------- 8.1 canvi d'unitats ---------- */
  var UL = ["km", "hm", "dam", "m", "dm", "cm", "mm"];
  function uname(i, k) { return UL[i] + (k === 2 ? "^2" : ""); }
  function convRows(v, i, j, k) {
    var st = j - i, f = Math.pow(10, k * Math.abs(st)), r = st >= 0 ? v * f : v / f, chain = "\\text{" + UL[i] + "}" + (k === 2 ? "^2" : ""), s;
    for (s = 1; s <= Math.abs(st); s++) chain += "\\xrightarrow{" + (st > 0 ? "\\times" : ":") + (k === 2 ? "100" : "10") + "}\\text{" + UL[i + (st > 0 ? s : -s)] + "}" + (k === 2 ? "^2" : "");
    var rows = [];
    if (st === 0) rows.push(T(L3("És la mateixa unitat.", "Es la misma unidad.", "It's the same unit.")));
    else {
      rows.push(fill(T(L3("{n} pas(sos) cap a una unitat més {g}: {o} per {f}.", "{n} paso(s) hacia una unidad más {g}: {o} por {f}.", "{n} step(s) to a {g} unit: {o} by {f}.")),
        { n: Math.abs(st), g: T(st > 0 ? L3("menuda", "pequeña", "smaller") : L3("gran", "grande", "bigger")), o: T(st > 0 ? L3("multipliquem", "multiplicamos", "multiply") : L3("dividim", "dividimos", "divide")), f: tex(dn(f)) }));
      rows.push(tex(chain));
      rows.push(fill(T(L3("La coma es desplaça {c} llocs cap a la {d}.", "La coma se desplaza {c} lugares hacia la {d}.", "The decimal point moves {c} places to the {d}.")),
        { c: k * Math.abs(st), d: T(st > 0 ? L3("dreta", "derecha", "right") : L3("esquerra", "izquierda", "left")) }));
    }
    rows.push(tex(dn(v) + "\\ \\text{" + UL[i] + "}" + (k === 2 ? "^2" : "") + (st === 0 ? "" : (st > 0 ? "\\cdot " : ":") + dn(f)) + "=\\boxed{" + dn(r) + "\\ \\text{" + UL[j] + "}" + (k === 2 ? "^2" : "") + "}"));
    if (k === 2 && (j === 1 || j === 2 || j === 3)) rows.push("🌾 " + tex(dn(r) + "\\ \\text{" + UL[j] + "}^2=" + dn(r) + "\\ \\text{" + ["", "ha", "a", "ca"][j] + "}"));
    return { rows: rows, r: r };
  }
  function wConv() {
    var w = document.getElementById("w-conv"); if (!w) return;
    var inp = inputs(w).v, out = w.querySelector(".hsteps"), info = w.querySelector(".info"), val;
    function labels() {
      var k = val[0] === "s" ? 2 : 1, AG = ["", " (ha)", " (a)", ""];
      w.querySelectorAll(".seg").forEach(function (g, gi) { if (gi > 0) g.querySelectorAll("button").forEach(function (b) { var i = +b.dataset.k; b.innerHTML = UL[i] + (k === 2 ? "²" + AG[i] : ""); }); });
    }
    function paint() {
      labels(); info.innerHTML = "";
      var v = numIn(inp.value); if (v === null || v < 0) { out.innerHTML = ""; info.innerHTML = warn(u("num")); return; }
      out.innerHTML = rows2html(convRows(v, +val[1], +val[2], val[0] === "s" ? 2 : 1).rows);
    }
    val = segs(w, [paint, paint, paint]);
    inp.addEventListener("input", paint);
    onLang(paint);
  }

  /* ---------- 8.2 perímetre dels polígons regulars ---------- */
  var PN = { 3: L3("triangle equilàter", "triángulo equilátero", "equilateral triangle"), 4: L3("quadrat", "cuadrado", "square"), 5: L3("pentàgon regular", "pentágono regular", "regular pentagon"), 6: L3("hexàgon regular", "hexágono regular", "regular hexagon"),
    7: L3("heptàgon regular", "heptágono regular", "regular heptagon"), 8: L3("octàgon regular", "octógono regular", "regular octagon"), 9: L3("enneàgon regular", "eneágono regular", "regular nonagon"), 10: L3("decàgon regular", "decágono regular", "regular decagon") };
  function regItems(n, l, tri) {
    var r = l / (2 * Math.sin(Math.PI / n)), V = reg(n, r), it = [["poly", V, "gf"]], i;
    if (tri) for (i = 0; i < n; i++) it.push(["poly", [[0, 0], V[i], V[(i + 1) % n]], i ? "tl" : "tr"]);
    else for (i = 0; i < n; i++) it.push(["tick", V[i], V[(i + 1) % n], 1]);
    return { it: it, V: V, r: r };
  }
  function wPer() {
    var w = document.getElementById("w-per"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var n = +I.n.value, l = +I.l.value, R = regItems(n, l, false), P = n * l;
      showRv(w, "n", "n", n); showRv(w, "l", "l", l);
      R.it.push(T_(off(R.V[0], R.V[1], -0.28 * R.r), "l = " + lab(l)));
      out.innerHTML = G(R.it, { W: 230, maxh: 220, pad: 26 }) + gcol(["<b>" + T(PN[n]).charAt(0).toUpperCase() + T(PN[n]).slice(1) + "</b>: " + fill(T(L3("{n} costats iguals", "{n} lados iguales", "{n} equal sides")), { n: n }),
        hP() + ": " + tex("P=n\\cdot l=" + n + "\\cdot" + nf(l) + "=" + n4(P)),
        T(L3("Al revés:", "Al revés:", "The other way round:")) + " " + tex("l=P:n=" + n4(P) + ":" + n + "=" + nf(l))]);
    }
    [I.n, I.l].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 8.3 rectangles en la quadrícula ---------- */
  function wRect() {
    var w = document.getElementById("w-rect"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var b = +I.b.value, h = +I.h.value, it = [["poly", [[0, 0], [b, 0], [b, h], [0, h]], "gf"]], x, y;
      showRv(w, "b", "b", b); showRv(w, "h", "h", h);
      for (x = 1; x < b; x++) it.push(["seg", [x, 0], [x, h], "gl"]);
      for (y = 1; y < h; y++) it.push(["seg", [0, y], [b, y], "gl"]);
      it.push(["poly", [[0, h - 1], [b, h - 1], [b, h], [0, h]], "tr"], T_([b / 2, 0], "b = " + b + " cm", { dy: 16 }), T_([b, h / 2], "h = " + h + " cm", { dx: 8, a: "start" }));
      var rows = [fill(T(L3("{h} files de {b} quadrets (una fila, en taronja):", "{h} filas de {b} cuadraditos (una fila, en naranja):", "{h} rows of {b} squares (one row in orange):")), { h: h, b: b }),
        hA() + ": " + tex("A=b\\cdot h=" + b + "\\cdot" + h + "=" + b * h + cm("cm") + "^2"),
        hP() + ": " + tex("P=2\\cdot" + b + "+2\\cdot" + h + "=" + (2 * b + 2 * h) + cm("cm"))];
      if (b === h) rows.push("⬛ " + T(L3("És un quadrat:", "Es un cuadrado:", "It's a square:")) + " " + tex("A=l^2=" + b + "^2=" + b * b + cm("cm") + "^2"));
      out.innerHTML = G(it, { W: 300, maxh: 230, pad: 40 }) + gcol(rows);
    }
    [I.b, I.h].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 8.4 romboide i triangle: movem el vèrtex ---------- */
  function shearItems(m, b, h, e) {
    var it = [], x0 = Math.min(0, e), x1 = Math.max(b, m === "ro" ? b + e : e);
    it.push(["seg", [x0 - 0.3, 0], [x1 + 0.3, 0], "thin"], ["seg", [x0 - 0.3, h], [x1 + 0.3, h], "thin dd"]);
    if (m === "ro") it.push(["poly", [[0, 0], [b, 0], [b + e, h], [e, h]], "gf"]); else it.push(["poly", [[0, 0], [b, 0], [e, h]], "gf"]);
    it.push(["seg", [e, 0], [e, h], "d"], ["ra", [e, 0], [e + 1, 0], [e, h]], ["dot", [e, h], "pa"], T_([b / 2, 0], "b = " + b, { dy: 16 }), T_([e, h / 2], "h = " + h, { dx: 6, a: "start", cls: "hot" }));
    return it;
  }
  function wShear() {
    var w = document.getElementById("w-shear"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), m = "ro";
    function paint() {
      var b = +I.b.value, h = +I.h.value, e = +I.e.value, A = m === "ro" ? b * h : b * h / 2;
      showRv(w, "b", "b", b); showRv(w, "h", "h", h); showRv(w, "e", "x", e);
      var side = m === "ro" ? 2 * b + 2 * Math.hypot(e, h) : b + Math.hypot(e, h) + Math.hypot(b - e, h);
      var rows = [hA() + ": " + tex(m === "ro" ? "A=b\\cdot h=" + b + "\\cdot" + h + "=" + A : "A=\\dfrac{b\\cdot h}{2}=\\dfrac{" + b + "\\cdot" + h + "}{2}=" + n4(A)),
        "✔ " + T(L3("Mou el vèrtex (control x): la base i l'altura no canvien, i l'àrea tampoc.", "Mueve el vértice (control x): la base y la altura no cambian, y el área tampoco.", "Move the vertex (slider x): the base and height don't change, and neither does the area.")),
        "📏 " + T(L3("El perímetre, en canvi, sí que canvia:", "El perímetro, en cambio, sí que cambia:", "The perimeter, however, does change:")) + " " + tex("P\\approx " + d2(side))];
      if (m === "tr" && (e < 0 || e > b)) rows.push("⚠️ " + T(L3("Ara el triangle és obtusangle: l'altura cau fora, sobre la prolongació de la base.", "Ahora el triángulo es obtusángulo: la altura cae fuera, sobre la prolongación de la base.", "Now the triangle is obtuse: the height falls outside, on the extended base.")));
      if (m === "ro" && e === 0) rows.push("▭ " + T(L3("Amb x = 0 el romboide és un rectangle.", "Con x = 0 el romboide es un rectángulo.", "With x = 0 the parallelogram is a rectangle.")));
      if (m === "tr" && (e === 0 || e === b)) rows.push("◺ " + T(L3("Ara és un triangle rectangle: l'altura és un catet.", "Ahora es un triángulo rectángulo: la altura es un cateto.", "Now it's a right triangle: the height is a leg.")));
      out.innerHTML = G(shearItems(m, b, h, e), { W: 360, maxh: 220, pad: 30, box: [-3, 0, 18, 8] }) + gcol(rows);
    }
    segs(w, [function (v) { m = v; paint(); }]);
    [I.b, I.h, I.e].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 8.5 rombe i trapezi ---------- */
  function rbItems(D, d, c) {
    var x = D / 2, y = d / 2, it = [];
    if (c) it.push(["poly", [[-x, -y], [x, -y], [x, y], [-x, y]], "frame"], ["poly", [[-x, 0], [0, -y], [-x, -y]], "tl"], ["poly", [[x, 0], [0, -y], [x, -y]], "tl"], ["poly", [[x, 0], [0, y], [x, y]], "tl"], ["poly", [[-x, 0], [0, y], [-x, y]], "tl"]);
    it.push(["poly", [[-x, 0], [0, y], [x, 0], [0, -y]], "gf"], ["seg", [-x, 0], [x, 0], "d"], ["seg", [0, -y], [0, y], "d"], T_([-x / 2, 0], "D = " + D, { dy: -6 }), T_([0, -y / 2], "d = " + d, { dx: 6, a: "start" }));
    return it;
  }
  function tpItems(B, b, h, c) {
    var e = (B - b) / 2, it = [["poly", [[0, 0], [B, 0], [e + b, h], [e, h]], "gf"]];
    if (c) it.push(["poly", [[B, 0], [B + b, 0], [B + b + e, h], [e + b, h]], "tl"], T_([B + b / 2, 0], "b", { dy: 16 }), T_([e + b + B / 2, h], "B", { dy: -7 }));
    it.push(["seg", [e, 0], [e, h], "d"], ["ra", [e, 0], [e + 1, 0], [e, h]], T_([B / 2, 0], "B = " + B, { dy: 16 }), T_([e + b / 2, h], "b = " + b, { dy: -7 }), T_([e, h / 2], "h = " + h, { dx: 6, a: "start" }));
    return it;
  }
  function wArea() {
    var w = document.getElementById("w-area"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), k = "rb", c = false;
    function paint() {
      var p = +I.p.value, q = +I.q.value, r = +I.r.value, rows; info.innerHTML = "";
      showRange(w, "r", k === "tp");
      if (k === "rb") {
        showRv(w, "p", "D", p); showRv(w, "q", "d", q);
        rows = [hA() + ": " + tex("A=\\dfrac{D\\cdot d}{2}=\\dfrac{" + p + "\\cdot" + q + "}{2}=" + n4(p * q / 2))];
        if (c) rows.push(fill(T(L3("El rectangle de les diagonals fa {a}. El rombe n'és la meitat: els 4 triangles de fora són iguals als 4 de dins.", "El rectángulo de las diagonales mide {a}. El rombo es la mitad: los 4 triángulos de fuera son iguales a los 4 de dentro.", "The rectangle of the diagonals is {a}. The rhombus is half of it: the 4 triangles outside match the 4 inside.")), { a: tex(p + "\\cdot" + q + "=" + p * q) }));
        out.innerHTML = G(rbItems(p, q, c), { W: 280, maxh: 220, pad: 30 }) + gcol(rows);
        return;
      }
      showRv(w, "p", "B", p); showRv(w, "q", "b", q); showRv(w, "r", "h", r);
      if (q > p) { out.innerHTML = ""; info.innerHTML = warn(T(L3("La base menor b no pot ser més llarga que la base major B.", "La base menor b no puede ser más larga que la base mayor B.", "The short base b can't be longer than the long base B."))); return; }
      rows = [hA() + ": " + tex("A=\\dfrac{(B+b)\\cdot h}{2}=\\dfrac{(" + p + "+" + q + ")\\cdot" + r + "}{2}=\\dfrac{" + (p + q) * r + "}{2}=" + n4((p + q) * r / 2))];
      if (c) rows.push(fill(T(L3("Amb dos trapezis iguals fem un romboide de base {s} i altura {h}: {a}. El trapezi n'és la meitat.", "Con dos trapecios iguales hacemos un romboide de base {s} y altura {h}: {a}. El trapecio es la mitad.", "Two equal trapeziums make a parallelogram with base {s} and height {h}: {a}. The trapezium is half of it.")),
        { s: tex("B+b=" + (p + q)), h: tex(r), a: tex("A=" + (p + q) + "\\cdot" + r + "=" + (p + q) * r) }));
      out.innerHTML = G(tpItems(p, q, r, c), { W: c ? 340 : 260, maxh: 200, pad: 34 }) + gcol(rows);
    }
    segs(w, [function (v) { k = v; paint(); }, function (v) { c = v === "c"; paint(); }]);
    [I.p, I.q, I.r].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 8.6 polígons regulars ---------- */
  function apo(n, l) { return Math.round(l / (2 * Math.tan(Math.PI / n)) * 100) / 100; }
  function wReg() {
    var w = document.getElementById("w-reg"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var n = +I.n.value, l = +I.l.value, a = apo(n, l), R = regItems(n, l, true), M = mid(R.V[0], R.V[1]), P = n * l;
      showRv(w, "n", "n", n); showRv(w, "l", "l", l);
      R.it.push(["seg", [0, 0], M, "hl"], ["ra", M, R.V[1], [0, 0]], ["dot", [0, 0]], T_(mid([0, 0], M), "a", { dx: -7, a: "end", cls: "hot" }), T_(M, "l", { dy: 15 }));
      out.innerHTML = G(R.it, { W: 240, maxh: 240, pad: 22 }) + gcol(["<b>" + T(PN[n]).charAt(0).toUpperCase() + T(PN[n]).slice(1) + "</b>: " + fill(T(L3("{n} triangles iguals de base l i altura a", "{n} triángulos iguales de base l y altura a", "{n} equal triangles with base l and height a")), { n: n }),
        T(L3("Apotema (mesurada):", "Apotema (medida):", "Apothem (measured):")) + " " + tex("a\\approx " + n4(a)),
        hP() + ": " + tex("P=" + n + "\\cdot" + nf(l) + "=" + n4(P)),
        hA() + ": " + tex("A=\\dfrac{P\\cdot a}{2}=\\dfrac{" + n4(P) + "\\cdot" + n4(a) + "}{2}" + ap(P * a / 2))]);
    }
    [I.n, I.l].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 8.7 la roda: longitud de la circumferència ---------- */
  function wPi() {
    var w = document.getElementById("w-pi"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var d = +I.d.value, t = +I.t.value, r = d / 2, L = Math.PI * d, x = t * L, C = [x, r], k, it = [];
      showRv(w, "d", "d", d); var tv = w.querySelector(".tv"); if (tv) tv.innerHTML = tex(T(L3("\\text{volta}", "\\text{vuelta}", "\\text{turn}")) + "=" + Math.round(t * 100) + "\\%");
      it.push(["seg", [-0.3 * d, 0], [L + 0.3 * d, 0], "thin"]);
      for (k = 1; k <= 3; k++) it.push(["seg", [k * d, -0.12 * d], [k * d, 0.12 * d], "tickd"], T_([k * d, 0], (k > 1 ? k : "") + "d", { dy: 18, cls: "sm" }));
      it.push(["seg", [L, -0.2 * d], [L, 0.2 * d], "hl"], T_([L, 0], "π·d", { dy: 30, cls: "hot" }));
      if (t > 0) it.push(["seg", [0, 0], [x, 0], "roll"]);
      it.push(["circ", C, r, "wheel"]);
      if (t > 0 && t < 1) it.push(["arc", C, r, -90 - 360 * t, -90, "hl"]);
      else if (t >= 1) it.push(["circ", C, r, "gc"], ["arc", C, r, -90, 269.9, "hl"]);
      var Pm = pol(C, r, -90 - 360 * t);
      it.push(["seg", C, Pm, ""], ["dot", C], ["dot", Pm, "pa"], ["dot", [0, 0]]);
      out.innerHTML = G(it, { W: 360, maxh: 200, pad: 26, box: [-0.3 * d, 0, L + 0.3 * d, d] }) + gcol([
        T(L3("Marquem un punt de la roda i la fem rodar una volta sencera. La distància que avança és la longitud de la circumferència.", "Marcamos un punto de la rueda y la hacemos rodar una vuelta entera. La distancia que avanza es la longitud de la circunferencia.", "Mark a point on the wheel and roll it one full turn. The distance it moves is the length of its circle.")),
        T(L3("Una volta és una mica més de 3 diàmetres:", "Una vuelta es un poco más de 3 diámetros:", "One turn is a little more than 3 diameters:")) + " " + tex("L=\\pi\\cdot d\\approx3\\dc 14\\cdot" + nf(d) + ap(P3 * d) + cm("cm")),
        t > 0 ? fill(T(L3("Ara ha avançat {x}.", "Ahora ha avanzado {x}.", "So far it has moved {x}.")), { x: tex("\\approx " + d2(P3 * d * t) + cm("cm")) }) : ""]);
    }
    [I.d, I.t].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }
  function wCirc() {
    var w = document.getElementById("w-circ"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var r = +I.r.value, n = +I.n.value, L = 2 * P3 * r, La = L * n / 360;
      showRv(w, "r", "r", r); showRv(w, "n", "n", n);
      var it = [["circ", [0, 0], r, "gc"]];
      if (n < 360) it.push(["seg", [0, 0], pol([0, 0], r, 0), ""], ["seg", [0, 0], pol([0, 0], r, n), ""], ["arc", [0, 0], r, 0, n, "hl"], ["arc", [0, 0], 0.22 * r, 0, n, "ang"], T_(pol([0, 0], 0.4 * r, n / 2), n + "°"));
      else it.push(["arc", [0, 0], r, 0, 359.9, "hl"]);
      it.push(["dot", [0, 0]], ["seg", [0, 0], [0, -r], "d"], T_([0, -r / 2], "r = " + lab(r), { dx: 5, a: "start" }));
      out.innerHTML = G(it, { W: 230, maxh: 230 }) + gcol([
        T(L3("Circumferència:", "Circunferencia:", "Circle:")) + " " + tex("L=2\\cdot\\pi\\cdot r=2\\cdot3\\dc 14\\cdot" + nf(r) + ap(L)),
        T(L3("Arc de ", "Arco de ", "Arc of ")) + tex(n + "^\\circ") + ": " + tex("L_{\\text{arc}}=\\dfrac{2\\cdot\\pi\\cdot r\\cdot n}{360}=\\dfrac{" + n4(L) + "\\cdot" + n + "}{360}" + ap(La)),
        "💡 " + fill(T(L3("L'arc és la fracció {f} de la circumferència.", "El arco es la fracción {f} de la circunferencia.", "The arc is the fraction {f} of the circle.")), { f: tex("\\frac{" + n + "}{360}") })]);
    }
    [I.r, I.n].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 8.8 cercle: del cercle al rectangle i figures circulars ---------- */
  function wPizza() {
    var w = document.getElementById("w-pizza"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var n = +I.n.value, th = 360 / n, hw = Math.sin(th / 2 * Math.PI / 180), ch = Math.cos(th / 2 * Math.PI / 180), it1 = [], it2 = [], k;
      showRv(w, "n", "n", n);
      for (k = 0; k < n; k++) it1.push(["sect", [0, 0], 1, 90 - th / 2 + k * th, 90 + th / 2 + k * th, k % 2 ? "q1" : "q0"]);
      for (k = 0; k < n / 2; k++) { it2.push(["sect", [2 * k * hw, 0], 1, 90 - th / 2, 90 + th / 2, "q0"]); it2.push(["sect", [2 * k * hw + hw, ch], 1, 270 - th / 2, 270 + th / 2, "q1"]); }
      it2.push(T_([n * hw / 2 - hw / 2, 0], "≈ π · r", { dy: 15 }), T_([-hw, ch / 2], "r", { dx: -6, a: "end" }));
      out.innerHTML = G(it1, { W: 150, maxh: 150 }) + G(it2, { W: 330, maxh: 170 }) + gcol([
        fill(T(L3("Amb {n} sectors, la figura ja s'assembla a un rectangle d'altura r i base la meitat de la circumferència, π·r.", "Con {n} sectores, la figura ya se parece a un rectángulo de altura r y base la mitad de la circunferencia, π·r.", "With {n} sectors the shape already looks like a rectangle of height r whose base is half the circle, π·r.")), { n: n }),
        T(L3("Com més sectors, més s'hi assembla. La seua àrea és ", "Cuantos más sectores, más se parece. Su área es ", "The more sectors, the closer it gets. Its area is ")) + tex("\\pi\\cdot r\\cdot r=\\pi\\cdot r^2") + "."]);
    }
    I.n.addEventListener("input", paint);
    onLang(paint);
  }
  var CMODE = {
    c: { k: ["R"], f: function (R) { return { it: [["circ", [0, 0], R, "sh"], ["seg", [0, 0], [R, 0], ""], ["dot", [0, 0]], T_([R / 2, 0], "r = " + lab(R), { dy: -6 })],
        rows: [tex("A=\\pi\\cdot r^2=3\\dc 14\\cdot" + nf(R) + "^2=3\\dc 14\\cdot" + n4(R * R) + ap(P3 * R * R)), tex("L=2\\cdot\\pi\\cdot r" + ap(2 * P3 * R))] }; } },
    s: { k: ["R", "n"], f: function (R, n) { return { it: [["circ", [0, 0], R, "gc"], ["sect", [0, 0], R, 0, n, "sh"], ["arc", [0, 0], 0.22 * R, 0, n, "ang"], ["dot", [0, 0]], T_(pol([0, 0], 0.42 * R, n / 2), n + "°"), T_([R / 2, 0], "r = " + lab(R), { dy: 15 })],
        rows: [tex("A=\\dfrac{\\pi\\cdot r^2\\cdot n}{360}=\\dfrac{3\\dc 14\\cdot" + n4(R * R) + "\\cdot" + n + "}{360}" + ap(P3 * R * R * n / 360)),
          n === 180 ? "◓ " + T(L3("És un semicercle: la meitat del cercle.", "Es un semicírculo: la mitad del círculo.", "It's a semicircle: half the disc.")) : n === 90 ? "◔ " + T(L3("És un quart de cercle.", "Es un cuarto de círculo.", "It's a quarter disc.")) : ""] }; } },
    k: { k: ["R", "r"], bad: function (R, r) { return r >= R ? L3("El radi menut r ha de ser menor que R.", "El radio menor r debe ser menor que R.", "The small radius r must be less than R.") : null; },
      f: function (R, r) { return { it: [["circ", [0, 0], R, "sh"], ["circ", [0, 0], r, "hole"], ["circ", [0, 0], r, "gc"], ["seg", [0, 0], pol([0, 0], R, 30), ""], ["seg", [0, 0], pol([0, 0], r, 150), "d"], ["dot", [0, 0]], T_(pol([0, 0], (R + r) / 2, 40), "R"), T_(pol([0, 0], r / 2, 165), "r")],
        rows: [tex("A=\\pi\\cdot R^2-\\pi\\cdot r^2=3\\dc 14\\cdot" + n4(R * R) + "-3\\dc 14\\cdot" + n4(r * r)), tex("A" + ap(P3 * R * R) + "-" + n4(Math.round(P3 * r * r * 10000) / 10000) + ap(P3 * (R * R - r * r)))] }; } }
  };
  function wCirca() {
    var w = document.getElementById("w-circa"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), mode = "c", keys = ["R", "r", "n"];
    function paint() {
      var F = CMODE[mode], vals = F.k.map(function (k) { return +I[k].value; });
      keys.forEach(function (k) { var on = F.k.indexOf(k) >= 0; showRange(w, k, on); if (on) showRv(w, k, mode !== "k" && k === "R" ? "r" : k, +I[k].value); });
      info.innerHTML = "";
      var bad = F.bad && F.bad.apply(null, vals);
      if (bad) { out.innerHTML = ""; info.innerHTML = warn(T(bad)); return; }
      var r = F.f.apply(null, vals);
      out.innerHTML = G(r.it, { W: 230, maxh: 230 }) + gcol(r.rows);
    }
    segs(w, [function (k) { mode = k; paint(); }]);
    keys.forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 8.9 figures compostes ---------- */
  var COMP = {
    L: { k: ["a", "b", "c"], bad: function (a, b, c) { return c >= a || c >= b ? L3("El quadrat que llevem (c) ha de ser més menut que a i que b.", "El cuadrado que quitamos (c) debe ser más pequeño que a y que b.", "The square we remove (c) must be smaller than a and b.") : null; },
      f: function (a, b, c) { var A = a * b - c * c, P = 2 * a + 2 * b;
        return { it: [["poly", [[0, 0], [a, 0], [a, b - c], [a - c, b - c], [a - c, b], [0, b]], "sh"], ["poly", [[a - c, b - c], [a, b - c], [a, b], [a - c, b]], "frame dd"], T_([a / 2, 0], "a = " + a, { dy: 16 }), T_([0, b / 2], "b = " + b, { dx: -7, a: "end" }), T_([a - c / 2, b - c], "c = " + c, { dy: 15 })],
          rows: [T(L3("Completem fins al rectangle a × b i restem el quadrat c × c:", "Completamos hasta el rectángulo a × b y restamos el cuadrado c × c:", "Complete it to the a × b rectangle and subtract the c × c square:")), tex("A=" + a + "\\cdot" + b + "-" + c + "^2=" + (a * b) + "-" + c * c + "=" + A),
            tex("P=2\\cdot" + a + "+2\\cdot" + b + "=" + P) + " — " + T(L3("els dos costats que es perden es recuperen dins!", "¡los dos lados que se pierden se recuperan dentro!", "the two sides we lose come back inside!"))], A: A, P: P }; } },
    casa: { k: ["a", "b", "c"], f: function (a, b, c) { var A = a * b + a * c / 2;
        return { it: [["poly", [[0, 0], [a, 0], [a, b], [0, b]], "sh"], ["poly", [[0, b], [a, b], [a / 2, b + c], [0, b]], "sh"], ["seg", [0, b], [a, b], "d"], ["seg", [a / 2, b], [a / 2, b + c], "d"], T_([a / 2, 0], "a = " + a, { dy: 16 }), T_([a, b / 2], "b = " + b, { dx: 8, a: "start" }), T_([a / 2, b + c / 2], "c = " + c, { dx: 6, a: "start" })],
          rows: [T(L3("Rectangle + triangle:", "Rectángulo + triángulo:", "Rectangle + triangle:")), tex("A=" + a + "\\cdot" + b + "+\\dfrac{" + a + "\\cdot" + c + "}{2}=" + a * b + "+" + n4(a * c / 2) + "=" + n4(A))], A: A }; } },
    fin: { k: ["a", "b"], f: function (a, b) { var A = a * b + P3 * a * a / 8, P = a + 2 * b + P3 * a / 2;
        return { it: [["poly", [[0, 0], [a, 0], [a, b], [0, b]], "sh"], ["sect", [a / 2, b], a / 2, 0, 180, "sh"], ["seg", [0, b], [a, b], "d"], T_([a / 2, 0], "a = " + a, { dy: 16 }), T_([a, b / 2], "b = " + b, { dx: 8, a: "start" })],
          rows: [T(L3("Rectangle + semicercle de radi ", "Rectángulo + semicírculo de radio ", "Rectangle + semicircle with radius ")) + tex("\\tfrac a2=" + n4(a / 2)) + ":",
            tex("A=" + a + "\\cdot" + b + "+\\dfrac{3\\dc 14\\cdot" + n4(a / 2) + "^2}{2}" + ap(A)),
            tex("P=" + a + "+2\\cdot" + b + "+\\dfrac{2\\cdot3\\dc 14\\cdot" + n4(a / 2) + "}{2}" + ap(P)) + " " + T(L3("(el diàmetre de dalt no és del contorn)", "(el diámetro de arriba no es del contorno)", "(the top diameter isn't part of the boundary)"))], A: A, P: P }; } },
    pista: { k: ["a", "b"], f: function (a, b) { var A = a * b + P3 * b * b / 4, P = 2 * a + P3 * b;
        return { it: [["poly", [[0, 0], [a, 0], [a, b], [0, b]], "sh"], ["sect", [a, b / 2], b / 2, -90, 90, "sh"], ["sect", [0, b / 2], b / 2, 90, 270, "sh"], ["seg", [0, 0], [0, b], "d"], ["seg", [a, 0], [a, b], "d"], T_([a / 2, 0], "a = " + a, { dy: 16 }), T_([a, b / 2], "b = " + b, { dx: -6, a: "end" })],
          rows: [T(L3("Rectangle + dos semicercles (un cercle sencer de radi ", "Rectángulo + dos semicírculos (un círculo entero de radio ", "Rectangle + two semicircles (a whole disc with radius ")) + tex("\\tfrac b2=" + n4(b / 2)) + "):",
            tex("A=" + a + "\\cdot" + b + "+3\\dc 14\\cdot" + n4(b / 2) + "^2" + ap(A)), tex("P=2\\cdot" + a + "+3\\dc 14\\cdot" + b + ap(P))], A: A, P: P }; } },
    forat: { k: ["a"], f: function (a) { var A = a * a - P3 * a * a / 4;
        return { it: [["poly", [[0, 0], [a, 0], [a, a], [0, a]], "sh"], ["circ", [a / 2, a / 2], a / 2, "hole"], ["circ", [a / 2, a / 2], a / 2, "gc"], ["dot", [a / 2, a / 2]], T_([a / 2, 0], "a = " + a, { dy: 16 })],
          rows: [T(L3("Quadrat menys el cercle de dins (de radi ", "Cuadrado menos el círculo de dentro (de radio ", "Square minus the disc inside (radius ")) + tex("\\tfrac a2=" + n4(a / 2)) + "):", tex("A=" + a + "^2-3\\dc 14\\cdot" + n4(a / 2) + "^2" + ap(A))], A: A }; } },
    cami: { k: ["a", "b", "c"], f: function (a, b, c) { var A = (a + 2 * c) * (b + 2 * c) - a * b;
        return { it: [["poly", [[-c, -c], [a + c, -c], [a + c, b + c], [-c, b + c]], "sh"], ["poly", [[0, 0], [a, 0], [a, b], [0, b]], "lawn"], T_([a / 2, b / 2], a + " × " + b), T_([a + c / 2, b / 2], "c", { a: "middle" })],
          rows: [T(L3("Rectangle exterior menys el jardí:", "Rectángulo exterior menos el jardín:", "Outer rectangle minus the garden:")), tex("A=(" + a + "+2\\cdot" + c + ")\\cdot(" + b + "+2\\cdot" + c + ")-" + a + "\\cdot" + b + "=" + (a + 2 * c) * (b + 2 * c) + "-" + a * b + "=" + A)], A: A }; } }
  };
  function wComp() {
    var w = document.getElementById("w-comp"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), mode = "L", keys = ["a", "b", "c"];
    function paint() {
      var F = COMP[mode], vals = F.k.map(function (k) { return +I[k].value; });
      keys.forEach(function (k) { var on = F.k.indexOf(k) >= 0; showRange(w, k, on); if (on) showRv(w, k, k, +I[k].value); });
      info.innerHTML = "";
      var bad = F.bad && F.bad.apply(null, vals);
      if (bad) { out.innerHTML = ""; info.innerHTML = warn(T(bad)); return; }
      var r = F.f.apply(null, vals);
      out.innerHTML = G(r.it, { W: 300, maxh: 230, pad: 40 }) + gcol(r.rows);
    }
    segs(w, [function (k) { mode = k; paint(); }]);
    keys.forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  function optsTxt(right, wrongs) {
    var all = [right].concat(wrongs), order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return all[i]; }), ans: order.indexOf(0) };
  }
  function ret(o, q, s) { o.q = q; o.s = s; return o; }
  function numQ(v, tol) { return { num: v, tol: tol || 1e-6 }; }
  /* resultats exactes (com a molt 2 decimals) i resultats amb π (s'accepta 3,14 o la tecla π) */
  function qn(v) { return numQ(v, 0.006); }
  function qp(v) { return numQ(v, Math.max(0.011, 0.0006 * Math.abs(v))); }
  function $(s) { return "$" + s + "$"; }
  function half() { return rint(0, 2) ? rint(2, 15) : rint(4, 25) / 2; }
  function FG(it, W, h) { return G(it, { W: W || 260, maxh: h || 160, pad: 40 }); }
  var GEN = {
    quad: function () {
      var NX = 7, NY = 5, on = polyomino(rint(5, 12), NX, NY), n = Object.keys(on).length, p = cellPer(on), t = rint(0, 1);
      return ret(numQ(t ? p : n), function () { return T(t ? L3("Quin és el perímetre d'aquesta figura, en cm? (cada quadret fa 1 cm de costat)", "¿Cuál es el perímetro de esta figura, en cm? (cada cuadradito mide 1 cm de lado)", "What is the perimeter of this shape, in cm? (each square has 1 cm sides)")
          : L3("Quina és l'àrea d'aquesta figura, en cm²? (cada quadret és 1 cm²)", "¿Cuál es el área de esta figura, en cm²? (cada cuadradito es 1 cm²)", "What is the area of this shape, in cm²? (each square is 1 cm²)")) + G(cellItems(on, NX, NY), { W: 220, maxh: 170, pad: 8 }); },
        function () { return t ? fill(T(L3("Hi ha {p} costats de quadret en el contorn: {r}.", "Hay {p} lados de cuadradito en el contorno: {r}.", "There are {p} square sides on the boundary: {r}.")), { p: p, r: tex("P=" + p + cm("cm")) })
          : fill(T(L3("Hi ha {n} quadrets pintats: {r}.", "Hay {n} cuadraditos pintados: {r}.", "There are {n} shaded squares: {r}.")), { n: n, r: tex("A=" + n + cm("cm") + "^2") }); });
    },
    conv: function () {
      var k = rint(1, 2), i, j; do { i = rint(0, 6); j = rint(0, 6); } while (i === j || Math.abs(i - j) > (k === 2 ? 3 : 4));
      var v = pick([3.5, 12, 0.8, 250, 4.25, 7, 65, 1.2, 3000, 45, 0.06, 18.5, 900, 2.75]), R = convRows(v, i, j, k);
      return ret(numQ(R.r, Math.abs(R.r) * 1e-9 + 1e-15), function () { return fill(T(L3("Expressa {v} en {u}.", "Expresa {v} en {u}.", "Write {v} in {u}.")), { v: $(dn(v) + "\\ \\text{" + uname(i, k).replace("^2", "}^2\\text{") + "}"), u: $("\\text{" + uname(j, k).replace("^2", "}^2\\text{") + "}") }); },
        function () { return R.rows.join("<br>"); });
    },
    per: function () {
      var t = rint(0, 5), b, h, n, l, a, c, P;
      if (t === 0) { b = half(); h = half(); P = 2 * b + 2 * h;
        return ret(qn(P), function () { return fill(T(L3("Quin és el perímetre d'un rectangle de {b} cm × {h} cm?", "¿Cuál es el perímetro de un rectángulo de {b} cm × {h} cm?", "What is the perimeter of a {b} cm × {h} cm rectangle?")), { b: $(nf(b)), h: $(nf(h)) }); }, function () { return tex("P=2\\cdot" + nf(b) + "+2\\cdot" + nf(h) + "=" + n4(P) + cm("cm")); }); }
      if (t === 1) { n = rint(3, 10); l = half(); P = n * l;
        return ret(qn(P), function () { return fill(T(L3("Quin és el perímetre d'un {p} de {l} cm de costat?", "¿Cuál es el perímetro de un {p} de {l} cm de lado?", "What is the perimeter of a {p} with {l} cm sides?")), { p: T(PN[n]), l: $(nf(l)) }); }, function () { return tex("P=" + n + "\\cdot" + nf(l) + "=" + n4(P) + cm("cm")); }); }
      if (t === 2) { do { a = rint(3, 15); b = rint(3, 15); c = rint(3, 15); } while (a + b <= c || a + c <= b || b + c <= a); P = a + b + c;
        return ret(qn(P), function () { return fill(T(L3("Els costats d'un triangle fan {a}, {b} i {c} cm. Quin és el perímetre?", "Los lados de un triángulo miden {a}, {b} y {c} cm. ¿Cuál es el perímetro?", "A triangle's sides are {a}, {b} and {c} cm. What is its perimeter?")), { a: $(a), b: $(b), c: $(c) }); }, function () { return tex("P=" + a + "+" + b + "+" + c + "=" + P + cm("cm")); }); }
      if (t === 3) { n = rint(3, 10); l = half(); P = n * l;
        return ret(qn(l), function () { return fill(T(L3("Un {p} té {P} cm de perímetre. Quant fa cada costat?", "Un {p} tiene {P} cm de perímetro. ¿Cuánto mide cada lado?", "A {p} has a {P} cm perimeter. How long is each side?")), { p: T(PN[n]), P: $(n4(P)) }); }, function () { return tex("l=P:n=" + n4(P) + ":" + n + "=" + nf(l) + cm("cm")); }); }
      if (t === 4) { b = rint(3, 20); h = rint(2, 15); P = 2 * b + 2 * h;
        return ret(qn(h), function () { return fill(T(L3("Un rectangle té {P} cm de perímetre i {b} cm de base. Quant fa l'altura?", "Un rectángulo tiene {P} cm de perímetro y {b} cm de base. ¿Cuánto mide la altura?", "A rectangle has a {P} cm perimeter and a {b} cm base. How tall is it?")), { P: $(P), b: $(b) }); }, function () { return tex("(" + P + "-2\\cdot" + b + "):2=" + (P - 2 * b) + ":2=" + h + cm("cm")); }); }
      b = rint(1, 4) + pick([0, 0.5, 0.2, 0.8]); h = rint(20, 95); P = 2 * b * 100 + 2 * h;
      return ret(qn(P), function () { return fill(T(L3("Quin és el perímetre, en cm, d'un rectangle de {b} m × {h} cm?", "¿Cuál es el perímetro, en cm, de un rectángulo de {b} m × {h} cm?", "What is the perimeter, in cm, of a {b} m × {h} cm rectangle?")), { b: $(nf(b)), h: $(h) }); },
        function () { return tex(nf(b) + cm("m") + "=" + n4(b * 100) + cm("cm")) + "; " + tex("P=2\\cdot" + n4(b * 100) + "+2\\cdot" + h + "=" + n4(P) + cm("cm")); });
    },
    rect: function () {
      var t = rint(0, 4), b, h, l, A;
      if (t === 0) { b = half(); h = rint(2, 12); A = b * h;
        return ret(qn(A), function () { return fill(T(L3("Quina és l'àrea d'un rectangle de {b} m × {h} m (en m²)?", "¿Cuál es el área de un rectángulo de {b} m × {h} m (en m²)?", "What is the area of a {b} m × {h} m rectangle (in m²)?")), { b: $(nf(b)), h: $(h) }); }, function () { return tex("A=" + nf(b) + "\\cdot" + h + "=" + n4(A) + cm("m") + "^2"); }); }
      if (t === 1) { l = half(); A = l * l;
        return ret(qn(A), function () { return fill(T(L3("Quina és l'àrea d'un quadrat de {l} cm de costat (en cm²)?", "¿Cuál es el área de un cuadrado de {l} cm de lado (en cm²)?", "What is the area of a square with {l} cm sides (in cm²)?")), { l: $(nf(l)) }); }, function () { return tex("A=" + nf(l) + "^2=" + n4(A) + cm("cm") + "^2"); }); }
      if (t === 2) { b = rint(3, 15); h = rint(2, 12); A = b * h;
        return ret(qn(h), function () { return fill(T(L3("Un rectangle té {A} cm² d'àrea i {b} cm de base. Quant fa l'altura?", "Un rectángulo tiene {A} cm² de área y {b} cm de base. ¿Cuánto mide la altura?", "A rectangle has an area of {A} cm² and a {b} cm base. How tall is it?")), { A: $(A), b: $(b) }); }, function () { return tex("h=A:b=" + A + ":" + b + "=" + h + cm("cm")); }); }
      if (t === 3) { l = rint(2, 15); A = l * l;
        return ret(qn(l), function () { return fill(T(L3("Un quadrat té {A} m² d'àrea. Quant fa el costat?", "Un cuadrado tiene {A} m² de área. ¿Cuánto mide el lado?", "A square has an area of {A} m². How long is its side?")), { A: $(A) }); }, function () { return tex(l + "^2=" + A + "\\ \\Rightarrow\\ l=\\sqrt{" + A + "}=" + l + cm("m")); }); }
      l = rint(2, 15); A = l * l;
      return ret(qn(A), function () { return fill(T(L3("Un quadrat té {P} cm de perímetre. Quina és la seua àrea (en cm²)?", "Un cuadrado tiene {P} cm de perímetro. ¿Cuál es su área (en cm²)?", "A square has a {P} cm perimeter. What is its area (in cm²)?")), { P: $(4 * l) }); }, function () { return tex("l=" + 4 * l + ":4=" + l + "\\qquad A=" + l + "^2=" + A + cm("cm") + "^2"); });
    },
    tri: function () {
      var t = rint(0, 3), b = rint(3, 14), h = rint(2, 10), e, A;
      if (t === 0) { e = rint(1, 5); A = b * h;
        return ret(qn(A), function () { return T(L3("Calcula l'àrea del romboide (mesures en cm, resultat en cm²).", "Calcula el área del romboide (medidas en cm, resultado en cm²).", "Find the area of the parallelogram (lengths in cm, answer in cm²).")) + FG(shearItems("ro", b, h, e)); }, function () { return tex("A=b\\cdot h=" + b + "\\cdot" + h + "=" + A + cm("cm") + "^2"); }); }
      if (t === 1) { e = pick([rint(1, b - 1), -rint(1, 4), b + rint(1, 4)]); A = b * h / 2;
        return ret(qn(A), function () { return T(L3("Calcula l'àrea del triangle (mesures en cm, resultat en cm²).", "Calcula el área del triángulo (medidas en cm, resultado en cm²).", "Find the area of the triangle (lengths in cm, answer in cm²).")) + FG(shearItems("tr", b, h, e)); }, function () { return tex("A=\\dfrac{b\\cdot h}{2}=\\dfrac{" + b + "\\cdot" + h + "}{2}=" + n4(A) + cm("cm") + "^2") + (e < 0 || e > b ? " " + T(L3("(l'altura cau fora del triangle)", "(la altura cae fuera del triángulo)", "(the height falls outside the triangle)")) : ""); }); }
      if (t === 2) { A = b * h / 2;
        return ret(qn(A), function () { return fill(T(L3("Els catets d'un triangle rectangle fan {b} cm i {h} cm. Quina és la seua àrea (en cm²)?", "Los catetos de un triángulo rectángulo miden {b} cm y {h} cm. ¿Cuál es su área (en cm²)?", "The legs of a right triangle are {b} cm and {h} cm. What is its area (in cm²)?")), { b: $(b), h: $(h) }); }, function () { return tex("A=\\dfrac{" + b + "\\cdot" + h + "}{2}=" + n4(A) + cm("cm") + "^2"); }); }
      A = b * h / 2;
      return ret(qn(h), function () { return fill(T(L3("Un triangle té {A} cm² d'àrea i {b} cm de base. Quant fa l'altura?", "Un triángulo tiene {A} cm² de área y {b} cm de base. ¿Cuánto mide la altura?", "A triangle has an area of {A} cm² and a {b} cm base. How tall is it?")), { A: $(n4(A)), b: $(b) }); },
        function () { return tex("b\\cdot h=2\\cdot" + n4(A) + "=" + b * h + "\\ \\Rightarrow\\ h=" + b * h + ":" + b + "=" + h + cm("cm")); });
    },
    rbtp: function () {
      var t = rint(0, 3), D = rint(4, 16), d = rint(2, D - 1), B = rint(5, 16), b = rint(2, B - 1), h = rint(2, 10), A;
      if (t === 0) { A = D * d / 2;
        return ret(qn(A), function () { return T(L3("Calcula l'àrea del rombe (mesures en cm, resultat en cm²).", "Calcula el área del rombo (medidas en cm, resultado en cm²).", "Find the area of the rhombus (lengths in cm, answer in cm²).")) + FG(rbItems(D, d, false)); }, function () { return tex("A=\\dfrac{D\\cdot d}{2}=\\dfrac{" + D + "\\cdot" + d + "}{2}=" + n4(A) + cm("cm") + "^2"); }); }
      if (t === 1) { A = (B + b) * h / 2;
        return ret(qn(A), function () { return T(L3("Calcula l'àrea del trapezi (mesures en cm, resultat en cm²).", "Calcula el área del trapecio (medidas en cm, resultado en cm²).", "Find the area of the trapezium (lengths in cm, answer in cm²).")) + FG(tpItems(B, b, h, false)); }, function () { return tex("A=\\dfrac{(" + B + "+" + b + ")\\cdot" + h + "}{2}=\\dfrac{" + (B + b) * h + "}{2}=" + n4(A) + cm("cm") + "^2"); }); }
      if (t === 2) { A = D * d / 2;
        return ret(qn(d), function () { return fill(T(L3("Un rombe té {A} cm² d'àrea i la diagonal major fa {D} cm. Quant fa la menor?", "Un rombo tiene {A} cm² de área y la diagonal mayor mide {D} cm. ¿Cuánto mide la menor?", "A rhombus has an area of {A} cm² and its long diagonal is {D} cm. How long is the short one?")), { A: $(n4(A)), D: $(D) }); },
          function () { return tex("D\\cdot d=2\\cdot" + n4(A) + "=" + D * d + "\\ \\Rightarrow\\ d=" + D * d + ":" + D + "=" + d + cm("cm")); }); }
      A = (B + b) * h / 2;
      return ret(qn(h), function () { return fill(T(L3("Un trapezi té {A} cm² d'àrea i les bases fan {B} cm i {b} cm. Quant fa l'altura?", "Un trapecio tiene {A} cm² de área y las bases miden {B} cm y {b} cm. ¿Cuánto mide la altura?", "A trapezium has an area of {A} cm² and bases of {B} cm and {b} cm. How tall is it?")), { A: $(n4(A)), B: $(B), b: $(b) }); },
        function () { return tex("(" + B + "+" + b + ")\\cdot h=2\\cdot" + n4(A) + "\\ \\Rightarrow\\ " + (B + b) + "\\cdot h=" + (B + b) * h + "\\ \\Rightarrow\\ h=" + h + cm("cm")); });
    },
    reg: function () {
      var t = rint(0, 3), n = pick([5, 6, 8, 10]), l = rint(3, 12), a = Math.round(apo(n, l) * 10) / 10, P = n * l, A = P * a / 2;
      if (t === 0 || t === 1) return ret(qn(A), function () { return fill(T(L3("Un {p} té {l} cm de costat i {a} cm d'apotema. Quina és la seua àrea (en cm²)?", "Un {p} tiene {l} cm de lado y {a} cm de apotema. ¿Cuál es su área (en cm²)?", "A {p} has {l} cm sides and a {a} cm apothem. What is its area (in cm²)?")), { p: T(PN[n]), l: $(l), a: $(nf(a)) }); },
        function () { return tex("P=" + n + "\\cdot" + l + "=" + P + "\\qquad A=\\dfrac{P\\cdot a}{2}=\\dfrac{" + P + "\\cdot" + nf(a) + "}{2}=" + n4(A) + cm("cm") + "^2"); });
      if (t === 2) return ret(qn(a), function () { return fill(T(L3("Un {p} té {P} cm de perímetre i {A} cm² d'àrea. Quant fa l'apotema?", "Un {p} tiene {P} cm de perímetro y {A} cm² de área. ¿Cuánto mide la apotema?", "A {p} has a {P} cm perimeter and an area of {A} cm². How long is its apothem?")), { p: T(PN[n]), P: $(P), A: $(n4(A)) }); },
        function () { return tex("P\\cdot a=2\\cdot" + n4(A) + "=" + n4(2 * A) + "\\ \\Rightarrow\\ a=" + n4(2 * A) + ":" + P + "=" + nf(a) + cm("cm")); });
      return ret(qn(l), function () { return fill(T(L3("Un {p} té {P} cm de perímetre. Quant fa el costat?", "Un {p} tiene {P} cm de perímetro. ¿Cuánto mide el lado?", "A {p} has a {P} cm perimeter. How long is its side?")), { p: T(PN[n]), P: $(P) }); }, function () { return tex("l=" + P + ":" + n + "=" + l + cm("cm")); });
    },
    circ: function () {
      var t = rint(0, 3), r = rint(2, 15), n = pick([30, 45, 60, 90, 120, 180, 270]), L = 2 * P3 * r;
      if (t === 0) return ret(qp(L), function () { return fill(T(L3("Calcula la longitud d'una circumferència de {r} cm de radi (π ≈ 3,14).", "Calcula la longitud de una circunferencia de {r} cm de radio (π ≈ 3,14).", "Find the length of a circle with a {r} cm radius (π ≈ 3.14).")), { r: $(r) }); }, function () { return tex("L=2\\cdot3\\dc 14\\cdot" + r + ap(L) + cm("cm")); });
      if (t === 1) return ret(qp(L), function () { return fill(T(L3("Una roda fa {d} cm de diàmetre. Quants cm avança en una volta? (π ≈ 3,14)", "Una rueda mide {d} cm de diámetro. ¿Cuántos cm avanza en una vuelta? (π ≈ 3,14)", "A wheel is {d} cm across. How many cm does it move in one turn? (π ≈ 3.14)")), { d: $(2 * r) }); }, function () { return tex("L=\\pi\\cdot d=3\\dc 14\\cdot" + 2 * r + ap(L) + cm("cm")); });
      if (t === 2) { var La = L * n / 360; return ret(qp(La), function () { return fill(T(L3("Calcula la longitud d'un arc de {n} en una circumferència de {r} cm de radi (π ≈ 3,14).", "Calcula la longitud de un arco de {n} en una circunferencia de {r} cm de radio (π ≈ 3,14).", "Find the length of a {n} arc of a circle with a {r} cm radius (π ≈ 3.14).")), { n: $(n + "^\\circ"), r: $(r) }); },
        function () { return tex("L_{\\text{arc}}=\\dfrac{2\\cdot3\\dc 14\\cdot" + r + "\\cdot" + n + "}{360}=\\dfrac{" + n4(L) + "\\cdot" + n + "}{360}" + ap(La) + cm("cm")); }); }
      return ret(qn(r), function () { return fill(T(L3("Una circumferència fa {L} cm de longitud. Quant fa el radi? (π ≈ 3,14)", "Una circunferencia mide {L} cm de longitud. ¿Cuánto mide el radio? (π ≈ 3,14)", "A circle is {L} cm long. How long is its radius? (π ≈ 3.14)")), { L: $(n4(L)) }); },
        function () { return tex("d=" + n4(L) + ":3\\dc 14=" + 2 * r + "\\qquad r=" + 2 * r + ":2=" + r + cm("cm")); });
    },
    circa: function () {
      var t = rint(0, 4), R = rint(2, 12), r = rint(1, R - 1), n = pick([30, 45, 60, 72, 120, 135, 150, 240]), v;
      if (t === 0) { v = P3 * R * R; return ret(qp(v), function () { return fill(T(L3("Calcula l'àrea d'un cercle de {r} cm de radi (π ≈ 3,14).", "Calcula el área de un círculo de {r} cm de radio (π ≈ 3,14).", "Find the area of a disc with a {r} cm radius (π ≈ 3.14).")), { r: $(R) }); }, function () { return tex("A=3\\dc 14\\cdot" + R + "^2=3\\dc 14\\cdot" + R * R + ap(v) + cm("cm") + "^2"); }); }
      if (t === 1) { v = P3 * R * R; return ret(qp(v), function () { return fill(T(L3("Calcula l'àrea d'un cercle de {d} cm de diàmetre (π ≈ 3,14).", "Calcula el área de un círculo de {d} cm de diámetro (π ≈ 3,14).", "Find the area of a disc {d} cm across (π ≈ 3.14).")), { d: $(2 * R) }); }, function () { return tex("r=" + 2 * R + ":2=" + R + "\\qquad A=3\\dc 14\\cdot" + R + "^2" + ap(v) + cm("cm") + "^2"); }); }
      if (t === 2) { var q = rint(0, 1); v = P3 * R * R / (q ? 4 : 2);
        return ret(qp(v), function () { return fill(T(q ? L3("Calcula l'àrea d'un quart de cercle de {r} cm de radi (π ≈ 3,14).", "Calcula el área de un cuarto de círculo de {r} cm de radio (π ≈ 3,14).", "Find the area of a quarter disc with a {r} cm radius (π ≈ 3.14).") : L3("Calcula l'àrea d'un semicercle de {r} cm de radi (π ≈ 3,14).", "Calcula el área de un semicírculo de {r} cm de radio (π ≈ 3,14).", "Find the area of a semicircle with a {r} cm radius (π ≈ 3.14).")), { r: $(R) }); },
          function () { return tex("A=\\dfrac{3\\dc 14\\cdot" + R + "^2}{" + (q ? 4 : 2) + "}" + ap(v) + cm("cm") + "^2"); }); }
      if (t === 3) { v = P3 * R * R * n / 360; return ret(qp(v), function () { return fill(T(L3("Calcula l'àrea d'un sector circular de {n} i {r} cm de radi (π ≈ 3,14).", "Calcula el área de un sector circular de {n} y {r} cm de radio (π ≈ 3,14).", "Find the area of a {n} sector with a {r} cm radius (π ≈ 3.14).")), { n: $(n + "^\\circ"), r: $(R) }); },
        function () { return tex("A=\\dfrac{3\\dc 14\\cdot" + R + "^2\\cdot" + n + "}{360}" + ap(v) + cm("cm") + "^2"); }); }
      v = P3 * (R * R - r * r);
      return ret(qp(v), function () { return fill(T(L3("Calcula l'àrea d'una corona circular de radis {R} cm i {r} cm (π ≈ 3,14).", "Calcula el área de una corona circular de radios {R} cm y {r} cm (π ≈ 3,14).", "Find the area of a ring with radii {R} cm and {r} cm (π ≈ 3.14).")), { R: $(R), r: $(r) }); },
        function () { return tex("A=3\\dc 14\\cdot" + R + "^2-3\\dc 14\\cdot" + r + "^2=3\\dc 14\\cdot" + (R * R - r * r) + ap(v) + cm("cm") + "^2"); });
    },
    comp: function () {
      var mode = pick(["L", "casa", "fin", "pista", "forat", "cami"]), F = COMP[mode], v, per;
      do {
        if (mode === "L") v = [rint(5, 12), rint(4, 10), rint(1, 3)];
        else if (mode === "casa") v = [2 * rint(2, 6), rint(3, 8), rint(2, 5)];
        else if (mode === "fin" || mode === "pista") v = [rint(4, 12), 2 * rint(1, 4)];
        else if (mode === "forat") v = [2 * rint(1, 6)];
        else v = [rint(6, 14), rint(4, 10), rint(1, 2)];
      } while (F.bad && F.bad.apply(null, v));
      var r = F.f.apply(null, v); per = r.P != null && rint(0, 2) === 0;
      var exact = mode === "L" || mode === "casa" || mode === "cami";
      return ret(per ? (exact ? qn(r.P) : qp(r.P)) : (exact ? qn(r.A) : qp(r.A)), function () {
        return T(per ? L3("Calcula el perímetre de la figura (mesures en m, π ≈ 3,14).", "Calcula el perímetro de la figura (medidas en m, π ≈ 3,14).", "Find the perimeter of the shape (lengths in m, π ≈ 3.14).") : L3("Calcula l'àrea de la zona acolorida (mesures en m, resultat en m², π ≈ 3,14).", "Calcula el área de la zona coloreada (medidas en m, resultado en m², π ≈ 3,14).", "Find the coloured area (lengths in m, answer in m², π ≈ 3.14)."))
          + (mode === "cami" ? " " + fill(T(L3("El camí fa {c} m d'amplària.", "El camino mide {c} m de ancho.", "The path is {c} m wide.")), { c: $(v[2]) }) : "") + FG(r.it, 260, 170); },
        function () { return r.rows.join(" "); });
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
  window.FM18 = { G: G, GEN: GEN, convRows: convRows, cellPer: cellPer, polyomino: polyomino, COMP: COMP, CMODE: CMODE, apo: apo, numIn: numIn };

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

  var TITLES = { va: "Àrees i perímetres · FentMates", es: "Áreas y perímetros · FentMates", en: "Area and perimeter · FentMates" };
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
    wGrid(); wConv(); wPer(); wRect(); wShear(); wArea(); wReg(); wPi(); wCirc(); wPizza(); wCirca(); wComp();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
