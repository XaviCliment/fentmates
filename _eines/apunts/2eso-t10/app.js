(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2eso-u10-done", NSEC = 8;

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
     unitat 10 (2n ESO): funcions (feta a partir de la unitat 9 de 1r ESO)
     ====================================================================== */
  /* ---------- nombres i fórmules ---------- */
  function tk(v) { var r = Math.round(v * 100) / 100; return String(r).replace("-", "−").replace(".", lang === "en" ? "." : ","); }
  /* punt en TeX: amb punt i coma si hi ha decimals (en anglés, sempre coma) */
  function ptx(x, y) { return "(" + nf(x) + (lang !== "en" && (!isInt(x) || !isInt(y)) ? ";" : ",") + "\\ " + nf(y) + ")"; }
  function ptt(P) { return "(" + tk(P[0]) + (lang !== "en" && (!isInt(P[0]) || !isInt(P[1])) ? "; " : ", ") + tk(P[1]) + ")"; }
  /* y = mx + n en TeX */
  function eqTex(m, n, v) {
    v = v || "x"; var s;
    if (near(m, 0)) s = nf(n);
    else {
      s = near(m, 1) ? v : near(m, -1) ? "-" + v : nf(m) + v;
      if (!near(n, 0)) s += (n > 0 ? "+" : "-") + nf(Math.abs(n));
    }
    return "y=" + s;
  }
  function niceStep(r, k) { k = k || 8; var raw = r / k, p = Math.pow(10, Math.floor(Math.log10(raw))), c = [1, 2, 5, 10]; for (var i = 0; i < c.length; i++) if (c[i] * p >= raw) return c[i] * p; return 10 * p; }
  function numsIn(raw) {
    var parts = String(raw).replace(/[−–]/g, "-").trim().split(/[\s;]+/).filter(function (s) { return s.length; });
    var out = parts.map(numIn); return out.some(function (v) { return v === null; }) ? null : out;
  }
  function ptsIn(raw) {
    var m = String(raw).match(/\(([^()]*)\)/g); if (!m) return null;
    var out = m.map(function (s) { return pairIn(s); });
    return out.some(function (p) { return p === null; }) ? null : out;
  }
  function at(P, x) { for (var i = 0; i < P.length - 1; i++) if (x >= P[i][0] - 1e-9 && x <= P[i + 1][0] + 1e-9) return P[i][1] + (P[i + 1][1] - P[i][1]) * (x - P[i][0]) / (P[i + 1][0] - P[i][0]); return NaN; }
  function segAt(P, x) { for (var i = 0; i < P.length - 1; i++) if (x <= P[i + 1][0] + 1e-9) return i; return P.length - 2; }

  /* ---------- pla cartesià (SVG); comu.py en té una còpia (pla()) ----------
     o: { win:[x0,x1,y0,y1], W, H, xs, ys, gx, gy, xl, yl, quad, arrows, polys:[[V, cls]], fns:[[m, n, cls, a, b]],
          curves:[[P, cls]], proj:[[x, y]], pts:[[x, y, etiqueta, cls, dx, dy]], labs:[[x, y, text, cls]], vline: x, clk } */
  function pla(o) {
    var x0 = o.win[0], x1 = o.win[1], y0 = o.win[2], y1 = o.win[3], W = o.W || 300, H = o.H || Math.round(W * (y1 - y0) / (x1 - x0));
    var xs = o.xs || 1, ys = o.ys || 1, gx = o.gx || xs, gy = o.gy || ys, k, g = "";
    function sx(v) { return +((v - x0) / (x1 - x0) * W).toFixed(1); }
    function sy(v) { return +(H - (v - y0) / (y1 - y0) * H).toFixed(1); }
    for (k = Math.ceil(x0 / gx - 1e-9); k * gx <= x1 + 1e-9; k++) g += '<line class="grid" x1="' + sx(k * gx) + '" y1="0" x2="' + sx(k * gx) + '" y2="' + H + '"/>';
    for (k = Math.ceil(y0 / gy - 1e-9); k * gy <= y1 + 1e-9; k++) g += '<line class="grid" x1="0" y1="' + sy(k * gy) + '" x2="' + W + '" y2="' + sy(k * gy) + '"/>';
    var ax = Math.min(Math.max(0, y0), y1), ay = Math.min(Math.max(0, x0), x1);
    g += '<line class="ax" x1="0" y1="' + sy(ax) + '" x2="' + W + '" y2="' + sy(ax) + '"/><line class="ax" x1="' + sx(ay) + '" y1="0" x2="' + sx(ay) + '" y2="' + H + '"/>';
    if (o.arrows !== false) g += '<path class="axh" d="M' + W + " " + sy(ax) + 'l-8 -4v8z"/><path class="axh" d="M' + sx(ay) + ' 0l-4 8h8z"/>';
    for (k = Math.ceil(x0 / xs - 1e-9); k * xs < x1 - 1e-9; k++) if (k && k * xs > x0 + 1e-9) g += '<text class="tk" x="' + sx(k * xs) + '" y="' + (sy(ax) + 13) + '" text-anchor="middle">' + tk(k * xs) + "</text>";
    for (k = Math.ceil(y0 / ys - 1e-9); k * ys < y1 - 1e-9; k++) if (k && k * ys > y0 + 1e-9) g += '<text class="tk" x="' + (sx(ay) - 5) + '" y="' + (sy(k * ys) + 4) + '" text-anchor="end">' + tk(k * ys) + "</text>";
    g += '<text class="tk" x="' + (sx(ay) - 5) + '" y="' + (sy(ax) + 13) + '" text-anchor="end">0</text>';
    g += '<text class="tk ax-l" x="' + (W - 6) + '" y="' + (sy(ax) - 8) + '" text-anchor="end">' + (o.xl || "x") + '</text><text class="tk ax-l" x="' + (sx(ay) + 8) + '" y="13">' + (o.yl == null ? "y" : o.yl) + "</text>";
    if (o.quad) [["I", 0.75, 0.82], ["II", 0.25, 0.82], ["III", 0.25, 0.18], ["IV", 0.75, 0.18]].forEach(function (q) { g += '<text class="qd" x="' + (q[1] * W).toFixed(1) + '" y="' + (H - q[2] * H + 8).toFixed(1) + '" text-anchor="middle">' + q[0] + "</text>"; });
    (o.polys || []).forEach(function (p) { g += '<polygon class="pg ' + p[1] + '" points="' + p[0].map(function (P) { return sx(P[0]) + "," + sy(P[1]); }).join(" ") + '"/>'; });
    (o.fns || []).forEach(function (f) {
      var m = f[0], n = f[1], lo = f[3] == null ? x0 : Math.max(f[3], x0), hi = f[4] == null ? x1 : Math.min(f[4], x1);
      if (!near(m, 0)) {
        var xa = (y0 - n) / m, xb = (y1 - n) / m;
        lo = Math.max(lo, Math.min(xa, xb)); hi = Math.min(hi, Math.max(xa, xb));
      } else if (n < y0 || n > y1) return;
      if (lo < hi) g += '<line class="cv ' + f[2] + '" x1="' + sx(lo) + '" y1="' + sy(m * lo + n) + '" x2="' + sx(hi) + '" y2="' + sy(m * hi + n) + '"/>';
    });
    (o.curves || []).forEach(function (c) { g += '<polyline class="cv ' + c[1] + '" points="' + c[0].map(function (P) { return sx(P[0]) + "," + sy(P[1]); }).join(" ") + '"/>'; });
    if (o.vline != null) g += '<line class="cursor" x1="' + sx(o.vline) + '" y1="0" x2="' + sx(o.vline) + '" y2="' + H + '"/>';
    (o.proj || []).forEach(function (P) { g += '<line class="guide" x1="' + sx(P[0]) + '" y1="' + sy(P[1]) + '" x2="' + sx(P[0]) + '" y2="' + sy(ax) + '"/><line class="guide" x1="' + sx(P[0]) + '" y1="' + sy(P[1]) + '" x2="' + sx(ay) + '" y2="' + sy(P[1]) + '"/>'; });
    (o.pts || []).forEach(function (p) {
      var dx = p[4] == null ? 7 : p[4], dy = p[5] == null ? -8 : p[5];
      g += '<circle class="pt ' + (p[3] || "p0") + '" cx="' + sx(p[0]) + '" cy="' + sy(p[1]) + '" r="5"/>';
      if (p[2]) g += '<text class="plab" x="' + (sx(p[0]) + dx).toFixed(1) + '" y="' + (sy(p[1]) + dy).toFixed(1) + '" text-anchor="' + (dx < 0 ? "end" : "start") + '">' + p[2] + "</text>";
    });
    (o.labs || []).forEach(function (p) { g += '<text class="plab ' + (p[3] || "") + '" x="' + sx(p[0]) + '" y="' + sy(p[1]) + '" text-anchor="middle">' + p[2] + "</text>"; });
    return '<svg class="sgraf' + (o.clk ? " clk" : "") + (o.cls ? " " + o.cls : "") + '" viewBox="-14 -6 ' + (W + 22) + " " + (H + 24) + '" data-g="' + [x0, x1, y0, y1, W, H].join(",") + '" role="img" aria-label="pla cartesià">' + g + "</svg>";
  }
  /* coordenades (de la gràfica) del lloc on s'ha tocat */
  function pickAt(svg, e) {
    var d = svg.dataset.g.split(",").map(Number), r = svg.getBoundingClientRect(), s = r.width / (d[4] + 22);
    var px = (e.clientX - r.left) / s - 14, py = (e.clientY - r.top) / s - 6;
    return [d[0] + px / d[4] * (d[1] - d[0]), d[3] - py / d[5] * (d[3] - d[2])];
  }
  function onPick(box, cb) {
    var svg = box.querySelector("svg.sgraf.clk"); if (!svg) return;
    svg.addEventListener("click", function (e) { var P = pickAt(svg, e); cb([Math.round(P[0]), Math.round(P[1])], P); });
  }

  /* ---------- 9.1 coordenades ---------- */
  var QN = { I: L3("quadrant I", "cuadrante I", "quadrant I"), II: L3("quadrant II", "cuadrante II", "quadrant II"), III: L3("quadrant III", "cuadrante III", "quadrant III"), IV: L3("quadrant IV", "cuadrante IV", "quadrant IV"),
    X: L3("eix X", "eje X", "x-axis"), Y: L3("eix Y", "eje Y", "y-axis"), O: L3("origen", "origen", "origin") };
  function quadOf(x, y) { return near(x, 0) && near(y, 0) ? "O" : near(y, 0) ? "X" : near(x, 0) ? "Y" : x > 0 ? (y > 0 ? "I" : "IV") : (y > 0 ? "II" : "III"); }
  function whereTxt(x, y) {
    var q = quadOf(x, y), s = { I: "(+,\\ +)", II: "(-,\\ +)", III: "(-,\\ -)", IV: "(+,\\ -)" }[q];
    return q === "O" ? T(L3("És l'origen de coordenades.", "Es el origen de coordenadas.", "It's the origin.")) :
      q === "X" ? T(L3("Està sobre l'eix X (l'ordenada és 0).", "Está sobre el eje X (la ordenada es 0).", "It's on the x-axis (y-coordinate 0).")) :
      q === "Y" ? T(L3("Està sobre l'eix Y (l'abscissa és 0).", "Está sobre el eje Y (la abscisa es 0).", "It's on the y-axis (x-coordinate 0).")) :
      fill(T(L3("Està en el {q}: signes {s}.", "Está en el {q}: signos {s}.", "It's in {q}: signs {s}.")), { q: "<b>" + T(QN[q]) + "</b>", s: tex(s) });
  }
  function moveTxt(x, y) {
    var a = Math.abs(x), b = Math.abs(y);
    var h = near(x, 0) ? T(L3("no ens movem en horitzontal", "no nos movemos en horizontal", "no horizontal move")) :
      fill(T(x > 0 ? L3("{a} cap a la dreta", "{a} hacia la derecha", "{a} to the right") : L3("{a} cap a l'esquerra", "{a} hacia la izquierda", "{a} to the left")), { a: tk(a) });
    var v = near(y, 0) ? T(L3("no ens movem en vertical", "no nos movemos en vertical", "no vertical move")) :
      fill(T(y > 0 ? L3("{b} cap amunt", "{b} hacia arriba", "{b} up") : L3("{b} cap avall", "{b} hacia abajo", "{b} down")), { b: tk(b) });
    return { h: h, v: v };
  }
  /* ---------- 10.2 de la taula al gràfic ---------- */
  var TPRE = {
    tmp: { x: "0 4 8 12 16 20 24", y: "6 4 9 17 19 12 7", j: "1", xl: "h", yl: "°C" },
    ent: { x: "1 2 3 4 5", y: "8 16 24 32 40", j: "0", xl: L3("entrades", "entradas", "tickets"), yl: "€" },
    pis: { x: "0 1 2 3 4 5", y: "80 65 50 35 20 5", j: "1", xl: "h", yl: "cm" }
  };
  function wTable() {
    var w = document.getElementById("w-table"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), pre = "tmp", join = "1";
    function fixDec(s) { return lang === "en" ? s.replace(/,/g, ".") : s; }
    segs(w, [function (k) { pre = k; if (TPRE[k]) { I.x.value = TPRE[k].x; I.y.value = fixDec(TPRE[k].y); join = TPRE[k].j; setSeg(w, 1, join); } paint(); }, function (k) { join = k; paint(); }]);
    function paint() {
      var X = numsIn(I.x.value), Y = numsIn(I.y.value);
      if (!X || !Y || !X.length) { info.innerHTML = warn(T(L3("Escriu els valors separats per espais: 0 1 2 3.", "Escribe los valores separados por espacios: 0 1 2 3.", "Type the values separated by spaces: 0 1 2 3."))); return; }
      if (X.length !== Y.length) { info.innerHTML = warn(T(L3("Hi ha d'haver tants valors de x com de y.", "Tiene que haber tantos valores de x como de y.", "There must be as many x values as y values."))); return; }
      if (X.length > 15) { info.innerHTML = warn(T(L3("Com a molt 15 parells.", "Como mucho 15 parejas.", "At most 15 pairs."))); return; }
      var P = X.map(function (x, i) { return [x, Y[i]]; }).sort(function (a, b) { return a[0] - b[0]; });
      var nofn = false; for (var i = 1; i < P.length; i++) if (near(P[i][0], P[i - 1][0]) && !near(P[i][1], P[i - 1][1])) nofn = true;
      var xa = Math.min.apply(null, [0].concat(X)), xb = Math.max.apply(null, [0].concat(X)), ya = Math.min.apply(null, [0].concat(Y)), yb = Math.max.apply(null, [0].concat(Y));
      var sx_ = niceStep(xb - xa || 1, 8), sy_ = niceStep(yb - ya || 1, 7);
      var win = [xa - (xa < 0 ? sx_ * 0.6 : 0), xb + sx_ * 0.6, ya - (ya < 0 ? sy_ * 0.6 : 0), yb + sy_ * 0.6];
      var p = TPRE[pre] || {}, xl = p.xl ? (typeof p.xl === "string" ? p.xl : T(p.xl)) : "x", yl = p.yl || "y";
      out.innerHTML = pla({ win: win, W: 300, H: 240, xs: sx_, ys: sy_, xl: xl, yl: yl, curves: join === "1" && !nofn ? [[P, "c0"]] : [], pts: P.map(function (Q) { return [Q[0], Q[1], null, "p0"]; }) })
        + gcol([T(L3("Punts:", "Puntos:", "Points:")) + " " + P.map(function (Q) { return tex(ptx(Q[0], Q[1])); }).join(", ")]);
      info.innerHTML = nofn ? warn(T(L3("Hi ha un valor de x amb dos valors de y diferents: aquesta relació no és una funció.", "Hay un valor de x con dos valores de y diferentes: esta relación no es una función.", "One x value has two different y values: this relation isn't a function."))) : "";
    }
    [I.x, I.y].forEach(function (i) { i.addEventListener("input", function () { if (pre !== "own") { pre = "own"; setSeg(w, 0, "own"); } paint(); }); });
    onLang(function () { if (TPRE[pre]) I.y.value = fixDec(TPRE[pre].y); paint(); });
  }

  /* ---------- 10.8 un gràfic, una història ---------- */
  var UP = L3("puja", "sube", "rises"), DOWN = L3("baixa", "baja", "falls"), FLAT = L3("es manté igual", "se mantiene igual", "stays the same");
  var STORIES = {
    exc: { P: [[0, 0], [2, 8], [3, 8], [4, 12], [6, 0]], xl: "t (h)", yl: "d (km)", ys: 2, ux: "h", uy: "km", name: L3("distància", "distancia", "distance"),
      t: [L3("Júlia s'allunya de casa: 4 km cada hora.", "Júlia se aleja de casa: 4 km cada hora.", "Júlia rides away from home: 4 km an hour."), L3("Està parada (descansa).", "Está parada (descansa).", "She has stopped (resting)."),
        L3("S'allunya altra vegada: 4 km cada hora.", "Se aleja otra vez: 4 km cada hora.", "She rides away again: 4 km an hour."), L3("Torna cap a casa, més de pressa: 6 km cada hora.", "Vuelve hacia casa, más deprisa: 6 km cada hora.", "She heads home, faster: 6 km an hour.")] },
    bany: { P: [[0, 0], [8, 32], [9, 40], [24, 40], [25, 32], [33, 0]], xl: "t (min)", yl: "h (cm)", xs: 4, gx: 2, ys: 8, gy: 4, ux: "min", uy: "cm", name: L3("altura de l'aigua", "altura del agua", "water height"),
      t: [L3("S'ompli la banyera.", "Se llena la bañera.", "The bath is filling."), L3("Algú s'hi fica dins: l'aigua puja de colp.", "Alguien se mete dentro: el agua sube de golpe.", "Someone gets in: the water jumps up."), L3("S'està banyant: l'altura no canvia.", "Se está bañando: la altura no cambia.", "Bath time: the height doesn't change."),
        L3("Ix de la banyera: l'aigua baixa de colp.", "Sale de la bañera: el agua baja de golpe.", "They get out: the water drops."), L3("Es buida la banyera.", "Se vacía la bañera.", "The bath is emptying.")] },
    tmp: { P: [[0, 6], [4, 4], [8, 9], [12, 17], [16, 19], [20, 12], [24, 7]], xl: "h", yl: "°C", xs: 4, gx: 2, ys: 4, gy: 2, ux: "h", uy: "°C", name: L3("temperatura", "temperatura", "temperature"), t: null },
    glo: { P: [[0, 0], [10, 300], [20, 300], [30, 500], [45, 0]], xl: "t (min)", yl: "h (m)", xs: 10, gx: 5, ys: 100, gy: 50, ux: "min", uy: "m", name: L3("altura del globus", "altura del globo", "balloon height"),
      t: [L3("El globus puja: 30 m cada minut.", "El globo sube: 30 m cada minuto.", "The balloon rises: 30 m a minute."), L3("Es manté a 300 m d'altura.", "Se mantiene a 300 m de altura.", "It stays at 300 m."), L3("Torna a pujar, ara més a poc a poc: 20 m cada minut.", "Vuelve a subir, ahora más despacio: 20 m cada minuto.", "It rises again, more slowly: 20 m a minute."), L3("Baixa fins a terra.", "Baja hasta el suelo.", "It comes down to the ground.")] }
  };
  function wStory() {
    var w = document.getElementById("w-story"); if (!w) return;
    var S = sliders(w), out = w.querySelector(".gout"), st = "exc", sl = S.t;
    segs(w, [function (k) { st = k; var P = STORIES[k].P, X = P[P.length - 1][0]; sl.max = X; sl.step = X > 10 ? 0.5 : 0.1; sl.value = X / 4; paint(); }]);
    function paint() {
      var s = STORIES[st], P = s.P, t = +sl.value, y = at(P, t), i = segAt(P, t), d = P[i + 1][1] - P[i][1], X = P[P.length - 1][0], Y = Math.max.apply(null, P.map(function (Q) { return Q[1]; }));
      var cls = d > 0 ? "u" : d < 0 ? "w" : "f", curves = [], mx = 0;
      for (var j = 0; j < P.length - 1; j++) { var dd = P[j + 1][1] - P[j][1]; curves.push([[P[j], P[j + 1]], dd > 0 ? "up" : dd < 0 ? "down" : "flat"]); }
      P.forEach(function (Q, k) { if (Q[1] > P[mx][1]) mx = k; });
      var tt = Math.round(t * 10) / 10;
      showRv(w, "t", "t", tt, "\\ \\text{" + s.ux + "}");
      out.innerHTML = pla({ win: [0, X * 1.14, 0, Y * 1.15], W: 300, H: 230, xs: s.xs || 1, gx: s.gx, ys: s.ys, gy: s.gy, xl: s.xl, yl: s.yl, curves: curves, vline: t, pts: [[t, y, null, "p0"]] })
        + gcol([fill(T(L3("Per a {t}, la {n} és {y}.", "Para {t}, la {n} es {y}.", "At {t}, the {n} is {y}.")), { t: tex("t=" + nf(tt) + "\\ \\text{" + s.ux + "}"), n: T(s.name), y: tex(nf(Math.round(y * 10) / 10) + "\\ \\text{" + s.uy + "}") }),
          '<span class="key k' + cls + '"></span>' + (s.t ? T(s.t[i]) : fill(T(L3("La {n} {v}.", "La {n} {v}.", "The {n} {v}.")), { n: T(s.name), v: T(d > 0 ? UP : d < 0 ? DOWN : FLAT) }))
          + " " + T(d > 0 ? L3("(creixent)", "(creciente)", "(increasing)") : d < 0 ? L3("(decreixent)", "(decreciente)", "(decreasing)") : L3("(constant)", "(constante)", "(constant)")),
          fill(T(L3("Màxim: {p}.", "Máximo: {p}.", "Maximum: {p}.")), { p: tex(ptx(P[mx][0], P[mx][1])) })]);
    }
    sl.addEventListener("input", paint); onLang(paint);
  }

  /* ---------- 10.4 i 10.6 rectes ---------- */
  function lineInfo(m, n) {
    var r = [];
    r.push(near(m, 0) ? fill(T(L3("{m}: és una funció constant (recta horitzontal).", "{m}: es una función constante (recta horizontal).", "{m}: it's a constant function (horizontal line).")), { m: tex("m=0") })
      : fill(T(m > 0 ? L3("{m} > 0: és creixent. Cada vegada que x augmenta 1, y augmenta {a}.", "{m} > 0: es creciente. Cada vez que x aumenta 1, y aumenta {a}.", "{m} > 0: it's increasing. Each time x goes up by 1, y goes up by {a}.")
        : L3("{m} < 0: és decreixent. Cada vegada que x augmenta 1, y disminueix {a}.", "{m} < 0: es decreciente. Cada vez que x aumenta 1, y disminuye {a}.", "{m} < 0: it's decreasing. Each time x goes up by 1, y goes down by {a}.")), { m: tex("m=" + nf(m)), a: tex(nf(Math.abs(m))) }));
    if (n != null) r.push(fill(T(L3("{n}: talla l'eix Y en {p}.", "{n}: corta el eje Y en {p}.", "{n}: it crosses the y-axis at {p}.")), { n: tex("n=" + nf(n)), p: tex(ptx(0, n)) }));
    return r;
  }
  function stepTri(m, n, x) { return [[[x, m * x + n], [x + 1, m * x + n], [x + 1, m * (x + 1) + n]], "c1 stp"]; }
  function tvTex(X, f) { return tex("\\begin{array}{c|" + X.map(function () { return "c"; }).join("") + "}x&" + X.join("&") + "\\\\\\hline y&" + X.map(function (x) { return nf(f(x)); }).join("&") + "\\end{array}"); }
  function wM() {
    var w = document.getElementById("w-m"); if (!w) return;
    var S = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var m = +S.m.value, X = [-2, -1, 0, 1, 2];
      showRv(w, "m", "m", m);
      out.innerHTML = pla({ win: [-5, 5, -7, 7], W: 280, fns: [[m, 0, "c0"]], curves: near(m, 0) ? [] : [stepTri(m, 0, 1)], pts: X.map(function (x) { return [x, m * x, null, "p0"]; }) })
        + gcol([tex(eqTex(m, 0)), tvTex(X, function (x) { return m * x; })].concat(lineInfo(m, null)).concat([T(L3("Passa per l'origen (0, 0).", "Pasa por el origen (0, 0).", "It goes through the origin (0, 0)."))]));
    }
    S.m.addEventListener("input", paint); onLang(paint);
  }
  function wMN() {
    var w = document.getElementById("w-mn"); if (!w) return;
    var S = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var m = +S.m.value, n = +S.n.value, X = [-2, -1, 0, 1, 2];
      showRv(w, "m", "m", m); showRv(w, "n", "n", n);
      out.innerHTML = pla({ win: [-6, 6, -8, 8], W: 280, fns: [[m, 0, "c2 dsh"], [m, n, "c0"]], curves: near(m, 0) ? [] : [stepTri(m, n, 0)], pts: [[0, n, null, "p1"]].concat(X.filter(function (x) { return x; }).map(function (x) { return [x, m * x + n, null, "p0"]; })) })
        + gcol([tex(eqTex(m, n)), tvTex(X, function (x) { return m * x + n; })].concat(lineInfo(m, n))
          .concat(['<span class="key k2"></span>' + fill(T(L3("La recta {r} és paral·lela i passa per l'origen.", "La recta {r} es paralela y pasa por el origen.", "The line {r} is parallel and goes through the origin.")), { r: tex(eqTex(m, 0)) })]));
    }
    [S.m, S.n].forEach(function (s) { s.addEventListener("input", paint); }); onLang(paint);
  }

  /* ---------- 10.8 dues tarifes ---------- */
  function wTwo() {
    var w = document.getElementById("w-two"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function cheaper(na, ma, nb, mb, x) { var a = na + ma * x, b = nb + mb * x; return near(a, b) ? "=" : a < b ? "A" : "B"; }
    function conclusion(na, ma, nb, mb, xs) {
      if (near(ma, mb) && near(na, nb)) return T(L3("Les dues tarifes són iguals.", "Las dos tarifas son iguales.", "Both plans are the same."));
      if (xs === null || xs <= 0) return fill(T(L3("Les rectes no es tallen per a x > 0: la tarifa {c} sempre és més barata.", "Las rectas no se cortan para x > 0: la tarifa {c} siempre es más barata.", "The lines don't cross for x > 0: plan {c} is always cheaper.")), { c: "<b>" + cheaper(na, ma, nb, mb, 1) + "</b>" });
      var yv = na + ma * xs;
      return fill(T(L3("Costen el mateix per a {x} ({y}). Abans és més barata la {b}; després, la {a}.", "Cuestan lo mismo para {x} ({y}). Antes es más barata la {b}; después, la {a}.", "They cost the same for {x} ({y}). Before that, {b} is cheaper; after that, {a}.")),
        { x: tex("x" + (isInt(xs * 100) ? "=" + nf(xs) : "\\approx " + d2(xs))), y: tex("y" + (isInt(yv * 100) ? "=" + nf(yv) : "\\approx " + d2(yv))), b: "<b>" + cheaper(na, ma, nb, mb, xs / 2) + "</b>", a: "<b>" + cheaper(na, ma, nb, mb, xs * 2) + "</b>" });
    }
    function paint() {
      var na = numIn(I.na.value), ma = numIn(I.ma.value), nb = numIn(I.nb.value), mb = numIn(I.mb.value);
      if ([na, ma, nb, mb].some(function (v) { return v === null || v < 0; })) { info.innerHTML = warn(T(L3("Escriu nombres positius o zero.", "Escribe números positivos o cero.", "Type positive numbers or zero."))); return; }
      info.innerHTML = "";
      var xs = near(ma, mb) ? null : (nb - na) / (ma - mb), X = xs !== null && xs > 0 ? Math.max(4, Math.ceil(xs * 1.8)) : 10;
      var Ymax = Math.max(na + ma * X, nb + mb * X, 1), sx_ = niceStep(X, 8), sy_ = niceStep(Ymax, 6);
      var pts = xs !== null && xs > 0 ? [[xs, na + ma * xs, null, "cut"]] : [];
      out.innerHTML = pla({ win: [0, X * 1.06, 0, Ymax * 1.12], W: 300, H: 230, xs: sx_, ys: sy_, fns: [[ma, na, "c0", 0], [mb, nb, "c1", 0]], pts: pts, proj: pts.map(function (p) { return [p[0], p[1]]; }) })
        + gcol(['<span class="key k0"></span>' + tex("A:\\ " + eqTex(ma, na)), '<span class="key k1"></span>' + tex("B:\\ " + eqTex(mb, nb)), conclusion(na, ma, nb, mb, xs)]);
    }
    ["na", "ma", "nb", "mb"].forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- 10.1 prova de la recta vertical ---------- */
  var CIRC = []; for (var ca = 0; ca <= 360; ca += 10) CIRC.push([3 * Math.cos(ca * Math.PI / 180), 3 * Math.sin(ca * Math.PI / 180)]);
  var VCURVES = [
    { f: true, P: [[-4.5, -2], [-2.5, 2], [-0.5, 0.5], [2, 3], [4.5, -1.5]] },
    { f: false, P: CIRC },
    { f: true, P: [[-4.5, -3], [4.5, 3]] },
    { f: false, P: [[2.5, 3], [-2.5, 3], [-2.5, 0], [2.5, 0], [2.5, -3], [-2.5, -3]] }
  ];
  /* punts on la recta vertical x talla una línia poligonal */
  function vHits(P, x) {
    var ys = [];
    function add(y) { if (!ys.some(function (v) { return Math.abs(v - y) < 1e-6; })) ys.push(y); }
    for (var i = 0; i < P.length - 1; i++) {
      var a = P[i], b = P[i + 1];
      if (near(a[0], b[0])) { if (near(a[0], x)) { add(a[1]); add(b[1]); } continue; }
      var lo = Math.min(a[0], b[0]), hi = Math.max(a[0], b[0]);
      if (x >= lo - 1e-9 && x <= hi + 1e-9) add(a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]));
    }
    return ys;
  }
  function wVline() {
    var w = document.getElementById("w-vline"); if (!w) return;
    var S = sliders(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), cur = VCURVES[0];
    segs(w, [function (k) { cur = VCURVES[+k]; paint(); }]);
    function paint() {
      var x = +S.x.value, ys = vHits(cur.P, x);
      showRv(w, "x", "x", Math.round(x * 10) / 10);
      out.innerHTML = pla({ win: [-5, 5, -4, 4], W: 300, H: 240, curves: [[cur.P, "c0"]], vline: x, pts: ys.map(function (y) { return [x, y, null, ys.length > 1 ? "bad" : "cut"]; }) });
      var msg = fill(T(L3("La recta vertical {x} talla el gràfic en <b>{n}</b> punt(s).", "La recta vertical {x} corta la gráfica en <b>{n}</b> punto(s).", "The vertical line {x} meets the graph at <b>{n}</b> point(s).")), { x: tex("x=" + nf(Math.round(x * 10) / 10)), n: ys.length });
      if (ys.length > 1) msg += " " + fill(T(L3("Per a aquest valor de {x} hi ha {n} valors de {y}: <b>no és una funció</b>.", "Para este valor de {x} hay {n} valores de {y}: <b>no es una función</b>.", "This value of {x} has {n} values of {y}: <b>it is not a function</b>.")), { x: tex("x"), y: tex("y"), n: ys.length });
      else msg += " " + T(cur.f ? L3("Mou la recta: mai no el talla en més d'un punt, així que <b>és una funció</b>.", "Mueve la recta: nunca la corta en más de un punto, así que <b>es una función</b>.", "Move the line: it never meets the graph more than once, so <b>it is a function</b>.")
        : L3("Mou la recta i busca un lloc on el talle en dos punts…", "Mueve la recta y busca un lugar donde la corte en dos puntos…", "Move the line and look for a place where it meets the graph twice…"));
      info.innerHTML = msg;
    }
    S.x.addEventListener("input", paint); onLang(paint);
  }

  /* ---------- 10.3 expressions: lectura, valor i TeX (el lector de 3eso-t7) ---------- */
  function lex(s) {
    s = s.replace(/[−–]/g, "-").replace(/[·×]/g, "*").replace(/÷/g, "/").replace(/²/g, "^2").replace(/³/g, "^3").replace(/\s+/g, "").toLowerCase();
    var out = [], i = 0, m;
    while (i < s.length) {
      var r = s.slice(i);
      if ((m = r.match(/^\d+(?:[.,]\d+)?/))) { out.push({ t: "n", v: parseFloat(m[0].replace(",", ".")) }); i += m[0].length; }
      else if ((m = r.match(/^(sqrt|arrel|raiz|raíz|√)/))) { out.push({ t: "f" }); i += m[0].length; }
      else if (r[0] === "x") { out.push({ t: "x" }); i++; }
      else if ("+-*/^()".indexOf(r[0]) >= 0) { out.push({ t: r[0] }); i++; }
      else return null;
    }
    return out;
  }
  function parseExpr(raw) {
    var tk_ = lex(raw); if (!tk_ || !tk_.length) return null;
    var i = 0;
    function peek() { return tk_[i] ? tk_[i].t : null; }
    function expr() { var a = term(); while (peek() === "+" || peek() === "-") { var op = tk_[i++].t; a = { t: op, a: a, b: term() }; } return a; }
    function term() {
      var a = unary();
      for (;;) {
        var p = peek();
        if (p === "*" || p === "/") { i++; a = { t: p, a: a, b: unary() }; }
        else if (p === "n" || p === "x" || p === "(" || p === "f") a = { t: "*", a: a, b: power(), imp: true };
        else return a;
      }
    }
    function unary() { if (peek() === "-") { i++; return { t: "neg", a: unary() }; } if (peek() === "+") { i++; return unary(); } return power(); }
    function power() { var a = atom(); if (peek() === "^") { i++; a = { t: "^", a: a, b: unary() }; } return a; }
    function atom() {
      var k = tk_[i++]; if (!k) throw 0;
      if (k.t === "n") return { t: "n", v: k.v };
      if (k.t === "x") return { t: "x" };
      if (k.t === "(") { var e = expr(); if (peek() !== ")") throw 0; i++; return { t: "()", a: e }; }
      if (k.t === "f") { var b = power(); return { t: "sqrt", a: b.t === "()" ? b.a : b }; }
      throw 0;
    }
    try { var e = expr(); return i === tk_.length ? e : null; } catch (err) { return null; }
  }
  function ev(e, x) {
    switch (e.t) {
      case "n": return e.v; case "x": return x; case "()": return ev(e.a, x); case "neg": return -ev(e.a, x);
      case "+": return ev(e.a, x) + ev(e.b, x); case "-": return ev(e.a, x) - ev(e.b, x);
      case "*": return ev(e.a, x) * ev(e.b, x);
      case "/": var d = ev(e.b, x); return Math.abs(d) < 1e-12 ? NaN : ev(e.a, x) / d;
      case "^": return Math.pow(ev(e.a, x), ev(e.b, x));
      case "sqrt": var r = ev(e.a, x); return r < -1e-12 ? NaN : Math.sqrt(Math.max(r, 0));
    }
    return NaN;
  }
  /* TeX; amb sub !== undefined, la x es canvia pel valor (entre parèntesis si és negatiu) */
  function etex(e, sub) {
    function leaf(n) { return n.t === "n" || n.t === "x" || n.t === "()" || n.t === "sqrt"; }
    function startsNum(n) { while (n.t === "*" || n.t === "^" || n.t === "/") n = n.a; return n.t === "n" || (n.t === "x" && sub !== undefined); }
    switch (e.t) {
      case "n": return nf(e.v);
      case "x": return sub === undefined ? "x" : nfp(sub);
      case "()": return "\\left(" + etex(e.a, sub) + "\\right)";
      case "neg": return "-" + (e.a.t === "+" || e.a.t === "-" ? "(" + etex(e.a, sub) + ")" : etex(e.a, sub));
      case "+": return etex(e.a, sub) + "+" + etex(e.b, sub);
      case "-": return etex(e.a, sub) + "-" + (e.b.t === "+" || e.b.t === "-" ? "(" + etex(e.b, sub) + ")" : etex(e.b, sub));
      case "*":
        var A = etex(e.a, sub), B = etex(e.b, sub);
        if (e.a.t === "+" || e.a.t === "-") A = "(" + A + ")";
        if (e.b.t === "+" || e.b.t === "-" || e.b.t === "neg") B = "(" + B + ")";
        return A + (e.imp && !startsNum(e.b) ? "" : "\\cdot ") + B;
      case "/": return "\\dfrac{" + etex(e.a.t === "()" ? e.a.a : e.a, sub) + "}{" + etex(e.b.t === "()" ? e.b.a : e.b, sub) + "}";
      case "^":
        var base = etex(e.a, sub);
        if (!leaf(e.a) || (e.a.t === "x" && sub !== undefined && sub < 0) || (e.a.t === "n" && e.a.v < 0)) base = "(" + base.replace(/^\(|\)$/g, "") + ")";
        return base + "^{" + etex(e.b.t === "()" ? e.b.a : e.b, sub) + "}";
      case "sqrt": return "\\sqrt{" + etex(e.a, sub) + "}";
    }
    return "";
  }
  /* ---------- 10.3 taula de valors i gràfic d'una equació ---------- */
  function wPlot() {
    var w = document.getElementById("w-plot"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      info.innerHTML = ""; out.innerHTML = "";
      var e = parseExpr(I.f.value); if (!e) { info.innerHTML = warn(u("bad")); return; }
      var a = numIn(I.a.value), b = numIn(I.b.value);
      if (a === null || b === null || b <= a || b - a > 20) { info.innerHTML = warn(T(L3("Tria un interval de x vàlid (com a molt 20 unitats): per exemple, de −3 a 3.", "Elige un intervalo de x válido (como mucho 20 unidades): por ejemplo, de −3 a 3.", "Choose a valid x range (at most 20 units): for example, from −3 to 3."))); return; }
      var xs = [], st = b - a > 10 ? 2 : 1; for (var x = Math.ceil(a); x <= b + 1e-9; x += st) xs.push(x);
      var ys = xs.map(function (x) { return ev(e, x); }), ok = ys.filter(isFinite);
      var lo = Math.min.apply(null, ok.concat([0])), hi = Math.max.apply(null, ok.concat([0]));
      if (hi - lo > 40) { var md = ok.length ? ok[Math.floor(ok.length / 2)] : 0; lo = Math.max(lo, md - 20); hi = Math.min(hi, md + 20); }
      var X0 = Math.min(a, 0) - 0.6, X1 = Math.max(b, 0) + 0.6, Y0 = Math.floor(lo) - 1, Y1 = Math.ceil(hi) + 1;
      /* corba: trossos sense forats ni salts */
      var curves = [], seg_ = [], N = 240;
      for (var k = 0; k <= N; k++) {
        var xx = a + (b - a) * k / N, yy = ev(e, xx);
        if (!isFinite(yy) || yy < Y0 - (Y1 - Y0) || yy > Y1 + (Y1 - Y0)) { if (seg_.length > 1) curves.push([seg_, "c0"]); seg_ = []; continue; }
        seg_.push([xx, Math.max(Y0 - 1, Math.min(Y1 + 1, yy))]);
      }
      if (seg_.length > 1) curves.push([seg_, "c0"]);
      var tbl = '<div class="tbl-wrap"><table class="data tv"><tbody><tr><th>' + tex("x") + "</th>" + xs.map(function (x) { return "<td>" + tex(nf(x)) + "</td>"; }).join("") + "</tr><tr><th>" + tex("y") + "</th>" + ys.map(function (y) { return "<td>" + (isFinite(y) ? tex(nf(y)) : "—") + "</td>"; }).join("") + "</tr></tbody></table></div>";
      var sxs = niceStep(X1 - X0, 8), sys = niceStep(Y1 - Y0, 8);
      out.innerHTML = '<div class="gcol"><p>' + tex("y=" + etex(e)) + "</p>" + tbl + "</div>"
        + pla({ win: [X0, X1, Y0, Y1], W: 300, H: 260, xs: sxs, ys: sys, curves: curves, pts: xs.map(function (x, i) { return isFinite(ys[i]) && ys[i] >= Y0 && ys[i] <= Y1 ? [x, ys[i], null, "p0"] : null; }).filter(Boolean) });
      /* recta? */
      var y0 = ev(e, 0), y1 = ev(e, 1), y2 = ev(e, 2.5), y3 = ev(e, -1.7), isLin = [y0, y1, y2, y3].every(isFinite) && near(y2 - y0, 2.5 * (y1 - y0)) && near(y3 - y0, -1.7 * (y1 - y0));
      var xa = xs.length ? xs[Math.min(1, xs.length - 1)] : a, sv = ev(e, xa);
      var msg = isFinite(sv) ? fill(T(L3("Per exemple, per a {x}: {s}.", "Por ejemplo, para {x}: {s}.", "For example, for {x}: {s}.")), { x: tex("x=" + nf(xa)), s: tex("y=" + etex(e, xa) + "=" + nf(sv)) }) : "";
      msg += " " + (isLin ? fill(T(L3("Els punts estan alineats: el gràfic és una recta de pendent {m}.", "Los puntos están alineados: la gráfica es una recta de pendiente {m}.", "The points line up: the graph is a straight line with slope {m}.")), { m: tex("m=" + nf(y1 - y0)) })
        : T(L3("Els punts no estan alineats: el gràfic és una corba.", "Los puntos no están alineados: la gráfica es una curva.", "The points don't line up: the graph is a curve.")));
      if (ys.some(function (y) { return !isFinite(y); })) msg += " " + T(L3("Hi ha valors de x sense imatge (no es pot dividir entre 0).", "Hay valores de x sin imagen (no se puede dividir entre 0).", "Some values of x have no image (you can't divide by 0)."));
      info.innerHTML = "💡 " + msg;
    }
    [I.f, I.a, I.b].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.f.value = v[0]; I.a.value = v[1]; I.b.value = v[2]; paint(); });
    onLang(paint);
  }

  /* ---------- 10.5 pendent entre dos punts ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  /* quocient p/q en TeX (fracció irreductible si p i q són enters) */
  function fracTex(p, q) {
    if (near(q, 0)) return "";
    if (isInt(p) && isInt(q)) {
      var g = gcd(Math.round(p), Math.round(q)), a = Math.round(p) / g, b = Math.round(q) / g;
      if (b < 0) { a = -a; b = -b; }
      return b === 1 ? String(a) : (a < 0 ? "-" : "") + "\\dfrac{" + Math.abs(a) + "}{" + b + "}";
    }
    return nf(p / q);
  }
  /* «dy/dx = fracció simplificada», sense repetir la fracció si ja és irreductible */
  function qTex(p, q) { var raw = "\\dfrac{" + nf(p) + "}{" + nf(q) + "}", s = fracTex(p, q); return raw + (s !== raw ? "=" + s : ""); }
  /* nombre en TeX com a fracció de denominador petit si cal (0,666… → 2/3) */
  function fracOf(m) { for (var q = 2; q <= 12; q++) if (isInt(m * q)) return fracTex(Math.round(m * q), q); return nf(m); }
  function wSlope() {
    var w = document.getElementById("w-slope"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      var A = pairIn(I.a.value), B = pairIn(I.b.value);
      if (!A || !B) { info.innerHTML = warn(u("pair")); return; }
      if (near(A[0], B[0]) && near(A[1], B[1])) { info.innerHTML = warn(T(L3("Escriu dos punts diferents.", "Escribe dos puntos distintos.", "Type two different points."))); return; }
      info.innerHTML = "";
      var xa = Math.min(A[0], B[0], 0), xb = Math.max(A[0], B[0], 0), ya = Math.min(A[1], B[1], 0), yb = Math.max(A[1], B[1], 0);
      var px = Math.max(1, (xb - xa) * 0.25), py = Math.max(1, (yb - ya) * 0.25), win = [xa - px, xb + px, ya - py, yb + py];
      var o = { win: win, W: 300, H: 260, xs: niceStep(win[1] - win[0], 9), ys: niceStep(win[3] - win[2], 8), pts: [[A[0], A[1], "A", "p0"], [B[0], B[1], "B", "p0"]] }, rows = [];
      if (near(A[0], B[0])) {
        o.curves = [[[[A[0], win[2]], [A[0], win[3]]], "c0"]];
        rows.push(fill(T(L3("Els dos punts tenen la mateixa x: la recta és vertical ({e}), no té pendent i no és una funció.", "Los dos puntos tienen la misma x: la recta es vertical ({e}), no tiene pendiente y no es una función.", "Both points have the same x: the line is vertical ({e}), has no slope and is not a function.")), { e: tex("x=" + nf(A[0])) }));
      } else {
        var dx = B[0] - A[0], dy = B[1] - A[1], m = dy / dx, n = A[1] - m * A[0];
        o.fns = [[m, n, "c0"]];
        o.curves = [[[A, [B[0], A[1]], B], "c1 stp"]];
        o.labs = [[(A[0] + B[0]) / 2, A[1] + (dy >= 0 ? -1 : 1) * (win[3] - win[2]) * 0.06, (dx > 0 ? "+" : "−") + tk(Math.abs(dx)), "l1"], [B[0] + (win[1] - win[0]) * 0.06, (A[1] + B[1]) / 2, (dy >= 0 ? "+" : "−") + tk(Math.abs(dy)), "l1"]];
        var mt = fracTex(dy, dx), raw = "\\dfrac{" + nf(dy) + "}{" + nf(dx) + "}";
        rows.push(tex("m=\\dfrac{" + nf(B[1]) + "-" + nfp(A[1]) + "}{" + nf(B[0]) + "-" + nfp(A[0]) + "}=" + raw + (mt !== raw ? "=" + mt : "") + (mt.indexOf("dfrac") < 0 ? "" : "\\approx " + nf(m))));
        rows.push(near(m, 0) ? T(L3("m = 0: la recta és horitzontal (funció constant).", "m = 0: la recta es horizontal (función constante).", "m = 0: the line is horizontal (constant function)."))
          : T(m > 0 ? L3("m > 0: la recta puja (funció creixent).", "m > 0: la recta sube (función creciente).", "m > 0: the line goes up (increasing function).") : L3("m < 0: la recta baixa (funció decreixent).", "m < 0: la recta baja (función decreciente).", "m < 0: the line goes down (decreasing function).")));
        if (isInt(m * 12) && isInt(n * 12)) rows.push(T(L3("Equació de la recta:", "Ecuación de la recta:", "Equation of the line:")) + " " + tex(eqTexF(m, n)));
      }
      out.innerHTML = pla(o) + gcol(rows);
    }
    [I.a, I.b].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.a.value = v[0]; I.b.value = v[1]; paint(); });
    onLang(paint);
  }
  /* y = mx + n en TeX amb fraccions */
  function eqTexF(m, n) {
    if (isInt(m) && isInt(n)) return eqTex(m, n);
    var s, ms = fracOf(m);
    if (near(m, 0)) s = fracOf(n);
    else {
      s = near(m, 1) ? "x" : near(m, -1) ? "-x" : ms + "x";
      if (!near(n, 0)) s += (n > 0 ? "+" : "-") + fracOf(Math.abs(n));
    }
    return "y=" + s;
  }

  /* ---------- 10.7 recta horitzontal o vertical ---------- */
  function wConst() {
    var w = document.getElementById("w-const"); if (!w) return;
    var S = sliders(w), out = w.querySelector(".gout"), md = "h";
    segs(w, [function (k) { md = k; paint(); }]);
    function paint() {
      var k = +S.k.value, X = [-2, -1, 0, 1, 2];
      showRv(w, "k", "k", k);
      if (md === "h") {
        out.innerHTML = pla({ win: [-5, 5, -5, 5], W: 280, fns: [[0, k, "c0"]], pts: X.map(function (x) { return [x, k, null, "p0"]; }).concat([[0, k, null, "p1"]]) })
          + gcol([tex("y=" + nf(k)), tvTex(X, function () { return k; }),
            fill(T(L3("Funció constant: per a qualsevol x, {y}. El pendent és {m} i talla l'eix Y en {p}.", "Función constante: para cualquier x, {y}. La pendiente es {m} y corta el eje Y en {p}.", "Constant function: for any x, {y}. The slope is {m} and it crosses the y-axis at {p}.")), { y: tex("y=" + nf(k)), m: tex("m=0"), p: tex(ptx(0, k)) })]);
      } else {
        out.innerHTML = pla({ win: [-5, 5, -5, 5], W: 280, curves: [[[[k, -5], [k, 5]], "c1"]], pts: [[k, -3, null, "bad"], [k, 1, null, "bad"], [k, 3.5, null, "bad"]] })
          + gcol([tex("x=" + nf(k)), fill(T(L3("Recta vertical: tots els punts tenen {x}. A aquest valor de x li corresponen infinits valors de y: <b>no és una funció</b>.", "Recta vertical: todos los puntos tienen {x}. A este valor de x le corresponden infinitos valores de y: <b>no es una función</b>.", "Vertical line: every point has {x}. That value of x is paired with infinitely many values of y: <b>it is not a function</b>.")), { x: tex("x=" + nf(k)) })]);
      }
    }
    S.k.addEventListener("input", paint); onLang(paint);
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
  function rpt() { var x, y; do { x = rint(-5, 5); y = rint(-5, 5); } while (x === 0 && y === 0); return [x, y]; }
  function mini(P) { return pla({ win: [0, 6.6, 0, 9.5], W: 150, H: 100, xs: 2, ys: 4, gx: 1, gy: 2, xl: "t", yl: "d", curves: [[P, "c0"]] }); }
  var MATCH = [
    { P: [[0, 0], [2, 4], [4, 4], [6, 0]], t: L3("Va a la botiga, s'hi queda una estona i torna a casa.", "Va a la tienda, se queda un rato y vuelve a casa.", "Goes to the shop, stays a while and comes back home.") },
    { P: [[0, 0], [6, 8]], t: L3("Ix de casa i camina sempre a la mateixa velocitat, sense parar.", "Sale de casa y camina siempre a la misma velocidad, sin parar.", "Leaves home and walks at a steady speed without stopping.") },
    { P: [[0, 0], [2, 4], [4, 4], [6, 8]], t: L3("Ix de casa, para a descansar i després continua allunyant-se.", "Sale de casa, para a descansar y después sigue alejándose.", "Leaves home, stops for a rest and then keeps going.") },
    { P: [[0, 0], [1, 6], [6, 0]], t: L3("Va corrent fins al parc i torna a casa caminant a poc a poc.", "Va corriendo hasta el parque y vuelve a casa caminando despacio.", "Runs to the park and walks slowly back home.") },
    { P: [[0, 0], [4, 2], [6, 8]], t: L3("Ix de casa caminant a poc a poc i després agafa l'autobús.", "Sale de casa caminando despacio y después coge el autobús.", "Leaves home walking slowly and then catches the bus.") },
    { P: [[0, 8], [6, 0]], t: L3("Està a 8 km de casa i torna sense parar.", "Está a 8 km de casa y vuelve sin parar.", "Is 8 km from home and comes back without stopping.") }
  ];
  /* problemes: cadascun torna { v: resposta, q: enunciat, s: solució } */
  var PROBS = [
    function () {
      var n = pick([2, 2.5, 3, 3.5, 4]), m = pick([0.8, 1, 1.2, 1.5]), x = rint(3, 20), y = Math.round((m * x + n) * 100) / 100;
      if (rint(0, 1)) return { v: x, q: fill(T(L3("Un taxi cobra {n} € de baixada de bandera i {m} € per km. Si un viatge ha costat {y} €, quants km s'han fet?", "Un taxi cobra {n} € de bajada de bandera y {m} € por km. Si un viaje ha costado {y} €, ¿cuántos km se han hecho?", "A taxi charges a €{n} pick-up fee and €{m} per km. If a ride cost €{y}, how many km was it?")), { n: tk(n), m: tk(m), y: tk(y) }),
        s: tex(eqTex(m, n) + "\\qquad " + nf(m) + "x+" + nf(n) + "=" + nf(y) + "\\ \\Rightarrow\\ x=\\dfrac{" + nf(y) + "-" + nf(n) + "}{" + nf(m) + "}=" + x + "\\ \\text{km}") };
      return { v: y, q: fill(T(L3("Un taxi cobra {n} € de baixada de bandera i {m} € per km. Quant costa un viatge de {x} km?", "Un taxi cobra {n} € de bajada de bandera y {m} € por km. ¿Cuánto cuesta un viaje de {x} km?", "A taxi charges a €{n} pick-up fee and €{m} per km. How much is a {x} km ride?")), { n: tk(n), m: tk(m), x: x }),
        s: tex(eqTex(m, n) + "\\qquad x=" + x + ":\\ y=" + nf(m) + "\\cdot" + x + "+" + nf(n) + "=" + nf(y) + "\\ \\text{€}") };
    },
    function () {
      var a = pick([10, 15, 20, 25, 30]), h = pick([1, 2, 2.5, 3]), x = rint(1, Math.floor(a / h) - 1), y = a - h * x;
      if (rint(0, 1)) return { v: a / h, q: fill(T(L3("Una espelma fa {a} cm i es crema {h} cm cada hora. Quantes hores tardarà a acabar-se?", "Una vela mide {a} cm y se quema {h} cm cada hora. ¿Cuántas horas tardará en acabarse?", "A candle is {a} cm tall and burns {h} cm an hour. How many hours until it's used up?")), { a: a, h: tk(h) }),
        s: tex(eqTex(-h, a) + "\\qquad -" + nf(h) + "x+" + a + "=0\\ \\Rightarrow\\ x=\\dfrac{" + a + "}{" + nf(h) + "}=" + nf(a / h) + "\\ \\text{h}") };
      return { v: y, q: fill(T(L3("Una espelma fa {a} cm i es crema {h} cm cada hora. Quant farà al cap de {x} h?", "Una vela mide {a} cm y se quema {h} cm cada hora. ¿Cuánto medirá al cabo de {x} h?", "A candle is {a} cm tall and burns {h} cm an hour. How tall is it after {x} h?")), { a: a, h: tk(h), x: x }),
        s: tex(eqTex(-h, a) + "\\qquad x=" + x + ":\\ y=-" + nf(h) + "\\cdot" + x + "+" + a + "=" + nf(y) + "\\ \\text{cm}") };
    },
    function () {
      var n = pick([20, 30, 40, 50]), m = pick([15, 20, 25, 30, 35]), x = rint(2, 9), y = m * x + n;
      if (rint(0, 1)) return { v: x, q: fill(T(L3("Un gimnàs cobra {n} € de matrícula i {m} € al mes. Si en total hem pagat {y} €, quants mesos hi hem anat?", "Un gimnasio cobra {n} € de matrícula y {m} € al mes. Si en total hemos pagado {y} €, ¿cuántos meses hemos ido?", "A gym charges a €{n} joining fee and €{m} a month. If we've paid €{y} in total, how many months have we been going?")), { n: n, m: m, y: y }),
        s: tex(eqTex(m, n) + "\\qquad " + m + "x+" + n + "=" + y + "\\ \\Rightarrow\\ x=\\dfrac{" + (y - n) + "}{" + m + "}=" + x) };
      return { v: y, q: fill(T(L3("Un gimnàs cobra {n} € de matrícula i {m} € al mes. Quant paguem en total si hi anem {x} mesos?", "Un gimnasio cobra {n} € de matrícula y {m} € al mes. ¿Cuánto pagamos en total si vamos {x} meses?", "A gym charges a €{n} joining fee and €{m} a month. How much do we pay in total for {x} months?")), { n: n, m: m, x: x }),
        s: tex(eqTex(m, n) + "\\qquad x=" + x + ":\\ y=" + m + "\\cdot" + x + "+" + n + "=" + y + "\\ \\text{€}") };
    },
    function () {
      var a = pick([200, 300, 400, 500, 600]), r = pick([10, 20, 25, 40, 50]), x = rint(1, a / r - 1), y = a - r * x;
      if (rint(0, 1)) return { v: a / r, q: fill(T(L3("Un dipòsit té {a} L i se'n buiden {r} L cada minut. Quants minuts tarda a buidar-se?", "Un depósito tiene {a} L y se vacían {r} L cada minuto. ¿Cuántos minutos tarda en vaciarse?", "A tank holds {a} L and {r} L drain out every minute. How many minutes until it's empty?")), { a: a, r: r }),
        s: tex(eqTex(-r, a) + "\\qquad -" + r + "x+" + a + "=0\\ \\Rightarrow\\ x=\\dfrac{" + a + "}{" + r + "}=" + nf(a / r) + "\\ \\text{min}") };
      return { v: y, q: fill(T(L3("Un dipòsit té {a} L i se'n buiden {r} L cada minut. Quanta aigua queda als {x} minuts?", "Un depósito tiene {a} L y se vacían {r} L cada minuto. ¿Cuánta agua queda a los {x} minutos?", "A tank holds {a} L and {r} L drain out every minute. How much is left after {x} minutes?")), { a: a, r: r, x: x }),
        s: tex(eqTex(-r, a) + "\\qquad x=" + x + ":\\ y=-" + r + "\\cdot" + x + "+" + a + "=" + y + "\\ \\text{L}") };
    },
    function () {
      var p = pick([5, 6, 8, 10, 12, 15]), b = pick([3, 4, 5, 6]), x = rint(2, 8), y = p * x + b;
      return { v: y, q: fill(T(L3("Una entrada val {p} € per persona i l'aparcament, {b} € per cotxe. Quant paga una família de {x} persones que va en un cotxe?", "Una entrada vale {p} € por persona y el aparcamiento, {b} € por coche. ¿Cuánto paga una familia de {x} personas que va en un coche?", "A ticket is €{p} per person and parking is €{b} per car. How much does a family of {x} pay if they come in one car?")), { p: p, b: b, x: x }),
        s: tex(eqTex(p, b) + "\\qquad x=" + x + ":\\ y=" + p + "\\cdot" + x + "+" + b + "=" + y + "\\ \\text{€}") };
    }
  ];
  /* les opcions es donen amb la correcta en primer lloc; wDrill les barreja (llevat que ja porten ans) */
  var GEN = {
    read: function () {
      var P = rpt(), nm = pick(["A", "B", "P", "Q", "R"]);
      return ret({ pair: P }, function () { return fill(T(L3("Quines són les coordenades del punt {n}?", "¿Cuáles son las coordenadas del punto {n}?", "What are the coordinates of point {n}?")), { n: $(nm) }) + pla({ win: [-6, 6, -6, 6], W: 260, pts: [[P[0], P[1], nm, "p0"]] }); },
        function () { var mv = moveTxt(P[0], P[1]); return tex(nm + ptx(P[0], P[1])) + ": " + mv.h + ", " + mv.v + "."; });
    },
    place: function () {
      var P = rpt();
      return ret({ click: P }, function (G) {
        var good = G && near(G[0], P[0]) && near(G[1], P[1]);
        return fill(T(L3("Situa el punt {p}.", "Sitúa el punto {p}.", "Plot the point {p}.")), { p: $(ptx(P[0], P[1])) })
          + pla({ win: [-6, 6, -6, 6], W: 260, clk: !G, pts: G ? [[G[0], G[1], null, good ? "good" : "bad"]].concat(good ? [] : [[P[0], P[1], null, "good"]]) : [], proj: G ? [P] : [] });
      }, function () { var mv = moveTxt(P[0], P[1]); return T(L3("Des de l'origen", "Desde el origen", "From the origin")) + ": " + mv.h + ", " + mv.v + "."; });
    },
    quad: function () {
      var P = rint(0, 4) ? [rnz(-9, 9), rnz(-9, 9)] : pick([[rnz(-9, 9), 0], [0, rnz(-9, 9)]]), q = quadOf(P[0], P[1]), keys = ["I", "II", "III", "IV", "X", "Y"];
      return ret({ opts: keys.map(function (k) { return QN[k]; }), ans: keys.indexOf(q) }, function () { return fill(T(L3("On està el punt {p}?", "¿Dónde está el punto {p}?", "Where is the point {p}?")), { p: $(ptx(P[0], P[1])) }); },
        function () { return whereTxt(P[0], P[1]); });
    },
    dist: function () {
      var hz = rint(0, 1), c = rint(-6, 6), a = rint(-7, 6), b; do { b = rint(-7, 7); } while (b === a);
      var A = hz ? [a, c] : [c, a], B = hz ? [b, c] : [c, b], d = Math.abs(b - a), hi = Math.max(a, b), lo = Math.min(a, b);
      return ret(numQ(d), function () { return fill(T(L3("Quina distància hi ha entre {A} i {B}?", "¿Qué distancia hay entre {A} y {B}?", "How far apart are {A} and {B}?")), { A: $(ptx(A[0], A[1])), B: $(ptx(B[0], B[1])) }); },
        function () { return T(hz ? L3("Tenen la mateixa y: restem les abscisses.", "Tienen la misma y: restamos las abscisas.", "Same y: subtract the x-coordinates.") : L3("Tenen la mateixa x: restem les ordenades.", "Tienen la misma x: restamos las ordenadas.", "Same x: subtract the y-coordinates.")) + " " + tex(nf(hi) + "-" + nfp(lo) + "=" + d); });
    },
    tab: function () {
      var m = rint(1, 6), n = rint(-5, 9), x = rint(-4, 8), y = m * x + n;
      return ret(numQ(y), function () { return fill(T(L3("Quin valor té y per a {x} en la funció {f}?", "¿Qué valor tiene y para {x} en la función {f}?", "What is y when {x} for the function {f}?")), { x: $("x=" + x), f: $(eqTex(m, n)) }); },
        function () { return tex("y=" + (m === 1 ? "" : m + "\\cdot") + nfp(x) + (n ? (n > 0 ? "+" : "-") + Math.abs(n) : "") + "=" + y); });
    },
    formula: function () {
      var F = [];
      function add(m, n) { if (!F.some(function (f) { return f[0] === m && f[1] === n; })) F.push([m, n]); }
      var m = rint(1, 5), n = rnz(-4, 6); if (rint(0, 2) === 0) n = 0; if (rint(0, 3) === 0) m = -1;
      add(m, n); add(m, n + m); add(n === 0 ? m + 1 : m + n, 0); add(m + 1, n - 1); add(-m, n); add(m, -n);
      F = F.slice(0, 4); while (F.length < 4) add(rint(1, 6), rint(-5, 5));
      var X = [0, 1, 2, 3];
      return ret({ opts: F.map(function (f) { return same($(eqTex(f[0], f[1]))); }) }, function () { return T(L3("Quina fórmula correspon a aquesta taula?", "¿Qué fórmula corresponde a esta tabla?", "Which formula matches this table?")) + " " + tex("\\begin{array}{c|cccc}x&" + X.join("&") + "\\\\\\hline y&" + X.map(function (x) { return m * x + n; }).join("&") + "\\end{array}", true); },
        function () { return fill(T(L3("Per a x = 0 dona {n} i cada vegada que x augmenta 1, y {c} {a}: {f}.", "Para x = 0 da {n} y cada vez que x aumenta 1, y {c} {a}: {f}.", "x = 0 gives {n} and each time x goes up by 1, y {c} {a}: {f}.")), { n: n, c: T(m > 0 ? L3("augmenta", "aumenta", "goes up by") : L3("disminueix", "disminuye", "goes down by")), a: Math.abs(m), f: tex(eqTex(m, n)) }); });
    },
    readg: function () {
      var P = [], y = rint(0, 6), mxv = 0;
      for (var x = 0; x <= 6; x++) { if (x) y = Math.max(0, Math.min(8, y + pick([-2, -1, 0, 1, 2, 3]))); P.push([x, y]); }
      P.forEach(function (Q) { mxv = Math.max(mxv, Q[1]); });
      var xa = rint(0, 6), ya = P[xa][1], G = pla({ win: [0, 6.6, 0, 9.4], W: 260, H: 200, curves: [[P, "c0"]] });
      if (rint(0, 3) === 0) return ret(numQ(mxv), function () { return T(L3("Quin és el valor màxim de y en aquest gràfic?", "¿Cuál es el valor máximo de y en esta gráfica?", "What is the maximum value of y on this graph?")) + G; },
        function () { return fill(T(L3("El punt més alt està a l'altura {y}.", "El punto más alto está a la altura {y}.", "The highest point is at height {y}.")), { y: tex("y=" + mxv) }); });
      return ret(numQ(ya), function () { return fill(T(L3("Quin valor té y quan {x}?", "¿Qué valor tiene y cuando {x}?", "What is y when {x}?")), { x: $("x=" + xa) }) + G; },
        function () { return fill(T(L3("Des de {x} pugem fins al gràfic: {p}.", "Desde {x} subimos hasta la gráfica: {p}.", "From {x} go up to the graph: {p}.")), { x: tex("x=" + xa), p: tex(ptx(xa, ya)) }); });
    },
    match: function () {
      var idx = shuffle(MATCH.map(function (_, i) { return i; })).slice(0, 3), R = MATCH[idx[0]];
      return ret({ opts: idx.map(function (i) { return same(mini(MATCH[i].P)); }) }, function () { return T(R.t) + " " + T(L3("(distància a casa en funció del temps)", "(distancia a casa en función del tiempo)", "(distance from home against time)")); },
        function () { return T(L3("Recorda: puja = s'allunya, horitzontal = parat, baixa = torna; com més inclinat, més de pressa.", "Recuerda: sube = se aleja, horizontal = parado, baja = vuelve; cuanto más inclinada, más deprisa.", "Remember: up = moving away, flat = stopped, down = coming back; steeper = faster.")); });
    },
    img0: function () {
      var m = pick([-3, -2, -1, 2, 3, 4, 5, 0.5, 1.5, 2.5, -0.5]), x = isInt(m) ? rint(-6, 6) : 2 * rint(-4, 4), y = m * x;
      return ret(numQ(y), function () { return fill(T(L3("Quin valor té y per a {x} en {f}?", "¿Qué valor tiene y para {x} en {f}?", "What is y when {x} for {f}?")), { x: $("x=" + x), f: $(eqTex(m, 0)) }); },
        function () { return tex("y=" + nf(m) + "\\cdot" + nfp(x) + "=" + nf(y)); });
    },
    m0: function () {
      var m = pick([-3, -2, -1, 2, 3, 4, 0.5, 1.5, 2.5, -0.5, -1.5]), x; do { x = rint(-6, 6); } while (!x || !isInt(m * x));
      var y = m * x;
      return ret(numQ(m), function () { return fill(T(L3("Una recta passa per l'origen i pel punt {p}. Quant val el pendent m?", "Una recta pasa por el origen y por el punto {p}. ¿Cuánto vale la pendiente m?", "A line goes through the origin and the point {p}. What is its slope m?")), { p: $(ptx(x, y)) }); },
        function () { return tex("m=\\dfrac{y}{x}=\\dfrac{" + nf(y) + "}{" + nf(x) + "}=" + nf(m)) + " → " + tex(eqTex(m, 0)); });
    },
    eq: function () {
      var m = pick([-3, -2, -1, -0.5, 0.5, 1, 2, 3]), n = rint(-4, 4), W = [];
      function add(a, b) { if (!(near(a, m) && near(b, n)) && !W.some(function (f) { return near(f[0], a) && near(f[1], b); })) W.push([a, b]); }
      if (n) add(m, -n); add(-m, n); if (n && isInt(m)) add(n, m); add(m + (m > 0 ? 1 : -1), n); add(m, n + 1);
      W = W.slice(0, 3);
      return ret({ opts: [[m, n]].concat(W).map(function (f) { return same($(eqTex(f[0], f[1]))); }) }, function () { return T(L3("Quina és la fórmula d'aquesta recta?", "¿Cuál es la fórmula de esta recta?", "What is the formula of this line?")) + pla({ win: [-6, 6, -6, 6], W: 260, fns: [[m, n, "c0"]], pts: [[0, n, null, "p1"]] }); },
        function () { return fill(T(L3("Talla l'eix Y en {p} ({n}) i, per cada 1 que avança, {c} {a} ({m}): {f}.", "Corta el eje Y en {p} ({n}) y, por cada 1 que avanza, {c} {a} ({m}): {f}.", "It crosses the y-axis at {p} ({n}) and, for every 1 across, goes {c} {a} ({m}): {f}.")),
          { p: tex(ptx(0, n)), n: tex("n=" + n), c: T(m > 0 ? L3("puja", "sube", "up") : L3("baixa", "baja", "down")), a: tex(nf(Math.abs(m))), m: tex("m=" + nf(m)), f: tex(eqTex(m, n)) }); });
    },
    /* ---------- entrenadors nous de 2n ESO ---------- */
    isfn: function () {
      var YES = L3("Sí, és una funció", "Sí, es una función", "Yes, it's a function"), NO = L3("No és una funció", "No es una función", "It's not a function");
      var j;
      var kind = rint(0, 5), P, f, why, G, tbl = null;
      if (kind === 0) { var y = rint(-2, 2); P = []; for (var x = -4; x <= 4; x += 2) { P.push([x, y]); y = Math.max(-3, Math.min(3, y + pick([-2, -1, 1, 2]))); } f = true; }
      else if (kind === 1) { var m = pick([-1.5, -1, -0.5, 0.5, 1, 2]), n = rint(-2, 2); P = [[-4, m * -4 + n], [4, m * 4 + n]]; f = true; }
      else if (kind === 2) { var r = pick([1.5, 2, 2.5, 3]), cx = rint(-1, 1), cy = rint(-1, 1); P = []; for (var a = 0; a <= 360; a += 15) P.push([cx + r * Math.cos(a * Math.PI / 180), cy + r * 0.9 * Math.sin(a * Math.PI / 180)]); f = false; }
      else if (kind === 3) { P = []; for (var t = -2; t <= 2.001; t += 0.25) P.push([t * t - 2, t * 1.4]); f = false; }
      else if (kind === 4) { var xr = rint(-3, 3); P = [[xr, -3.5], [xr, 3.5]]; f = false; }
      else {
        var X = [1, 2, 3, 4, 5], Y = X.map(function () { return rint(-5, 9); });
        f = rint(0, 1) === 0;
        if (!f) { var j = rint(1, 4); X[j] = X[j - 1]; while (Y[j] === Y[j - 1]) Y[j] = rint(-5, 9); }
        tbl = X;
        why = f ? fill(T(L3("Cap valor de {x} es repeteix: a cada {x} li correspon un sol valor de {y}.", "Ningún valor de {x} se repite: a cada {x} le corresponde un solo valor de {y}.", "No value of {x} is repeated: each {x} has a single value of {y}.")), { x: tex("x"), y: tex("y") })
          : fill(T(L3("El valor {v} apareix amb dos valors de {y} diferents.", "El valor {v} aparece con dos valores de {y} distintos.", "The value {v} appears with two different values of {y}.")), { v: tex("x=" + X[j]), y: tex("y") });
        return ret({ opts: [YES, NO], ans: f ? 0 : 1 }, function () { return T(L3("Aquesta taula és d'una funció?", "¿Esta tabla es de una función?", "Is this table a function?")) + " " + tex("\\begin{array}{c|ccccc}x&" + X.join("&") + "\\\\\\hline y&" + Y.join("&") + "\\end{array}", true); }, function () { return why; });
      }
      G = pla({ win: [-5, 5, -4, 4], W: 260, H: 210, curves: [[P, "c0"]] });
      why = f ? T(L3("Qualsevol recta vertical el talla, com a molt, en un punt.", "Cualquier recta vertical la corta, como mucho, en un punto.", "Any vertical line meets it at one point at most."))
        : T(L3("Hi ha rectes verticals que el tallen en més d'un punt: una x amb diverses y.", "Hay rectas verticales que la cortan en más de un punto: una x con varias y.", "Some vertical lines meet it at more than one point: one x with several values of y."));
      return ret({ opts: [YES, NO], ans: f ? 0 : 1 }, function () { return T(L3("Aquest gràfic és d'una funció?", "¿Esta gráfica es de una función?", "Is this graph a function?")) + G; }, function () { return why; });
    },
    gap: function () {
      var m = rnz(-4, 5), n = rint(-6, 9), s = rint(-2, 2), X = [s, s + 1, s + 2, s + 3, s + 4], j = rint(1, 4), v = m * X[j] + n;
      return ret(numQ(v), function () { return T(L3("La taula és d'una funció de la forma y = mx + n. Quin nombre falta?", "La tabla es de una función de la forma y = mx + n. ¿Qué número falta?", "The table comes from a function of the form y = mx + n. Which number is missing?")) + " " + tex("\\begin{array}{c|ccccc}x&" + X.join("&") + "\\\\\\hline y&" + X.map(function (x, i) { return i === j ? "?" : nf(m * x + n); }).join("&") + "\\end{array}", true); },
        function () { return fill(T(L3("Cada vegada que x augmenta 1, y {c} {a}: és {f}. Per a {x}, {y}.", "Cada vez que x aumenta 1, y {c} {a}: es {f}. Para {x}, {y}.", "Each time x goes up by 1, y {c} {a}: it's {f}. For {x}, {y}.")),
          { c: T(m > 0 ? L3("augmenta", "aumenta", "goes up by") : L3("disminueix", "disminuye", "goes down by")), a: Math.abs(m), f: tex(eqTex(m, n)), x: tex("x=" + X[j]), y: tex("y=" + nf(v)) }); });
    },
    belongs: function () {
      var m = rnz(-4, 4), n = rint(-6, 6), x = rint(-4, 5), y = m * x + n, ok = rint(0, 1) === 0, yy = ok ? y : y + pick([-3, -2, -1, 1, 2, 3]);
      return ret({ opts: [L3("Sí", "Sí", "Yes"), L3("No", "No", "No")], ans: ok ? 0 : 1 }, function () { return fill(T(L3("El punt {p} és del gràfic de {f}?", "¿El punto {p} es de la gráfica de {f}?", "Is the point {p} on the graph of {f}?")), { p: $(ptx(x, yy)), f: $(eqTex(m, n)) }); },
        function () { return tex("x=" + x + ":\\ y=" + (m === 1 ? "" : m === -1 ? "-" : m + "\\cdot") + nfp(x) + (n ? (n > 0 ? "+" : "-") + Math.abs(n) : "") + "=" + y) + " " + (ok ? "= " + tex(nf(yy)) + " ✓" : "≠ " + tex(nf(yy)) + " ✗"); });
    },
    pre: function () {
      var m = rnz(-5, 5), n = rint(-8, 8), x = rint(-6, 8), y = m * x + n;
      return ret(numQ(x), function () { return fill(T(L3("Per a quin valor de x la funció {f} val {y}?", "¿Para qué valor de x la función {f} vale {y}?", "For which value of x is {f} equal to {y}?")), { f: $(eqTex(m, n)), y: $(nf(y)) }); },
        function () { return tex(eqTex(m, n).slice(2) + "=" + y + "\\ \\Rightarrow\\ " + (m === 1 ? "" : m === -1 ? "-" : m) + "x=" + nf(y - n) + "\\ \\Rightarrow\\ x=" + (Math.abs(m) === 1 ? "" : "\\dfrac{" + nf(y - n) + "}{" + m + "}=") + nf(x)); });
    },
    img: function () {
      if (rint(0, 1)) return GEN.img1();
      var a = pick([1, 1, 2, -1, 3]), c = rint(-5, 5), x = rint(-4, 4), y = a * x * x + c;
      var ft = "y=" + (a === 1 ? "" : a === -1 ? "-" : a) + "x^2" + (c ? (c > 0 ? "+" : "-") + Math.abs(c) : "");
      return ret(numQ(y), function () { return fill(T(L3("Quin valor té y per a {x} en {f}?", "¿Qué valor tiene y para {x} en {f}?", "What is y when {x} for {f}?")), { x: $("x=" + x), f: $(ft) }); },
        function () { return tex("y=" + (a === 1 ? "" : a === -1 ? "-" : a + "\\cdot") + nfp(x) + "^2" + (c ? (c > 0 ? "+" : "-") + Math.abs(c) : "") + "=" + (a === 1 ? "" : a === -1 ? "-" : a + "\\cdot") + (x * x) + (c ? (c > 0 ? "+" : "-") + Math.abs(c) : "") + "=" + y) + (x < 0 ? " " + T(L3("(un negatiu al quadrat és positiu)", "(un negativo al cuadrado es positivo)", "(a negative number squared is positive)")) : ""); });
    },
    slope2: function () {
      var A, B; do { A = [rint(-5, 5), rint(-5, 5)]; B = [rint(-5, 5), rint(-5, 5)]; } while (A[0] === B[0] || !isInt(12 * (B[1] - A[1]) / (B[0] - A[0])) || Math.abs((B[1] - A[1]) / (B[0] - A[0])) > 6);
      var dx = B[0] - A[0], dy = B[1] - A[1];
      return ret(numQ(dy / dx, 0.006), function () { return fill(T(L3("Quin és el pendent de la recta que passa per {A} i {B}?", "¿Cuál es la pendiente de la recta que pasa por {A} y {B}?", "What is the slope of the line through {A} and {B}?")), { A: $(ptx(A[0], A[1])), B: $(ptx(B[0], B[1])) }) + " " + T(L3("(Pots respondre amb una fracció, com 2/3.)", "(Puedes responder con una fracción, como 2/3.)", "(You can answer with a fraction, like 2/3.)")); },
        function () { return tex("m=\\dfrac{" + B[1] + "-" + nfp(A[1]) + "}{" + B[0] + "-" + nfp(A[0]) + "}=" + qTex(dy, dx)); });
    },
    slopeg: function () {
      var c = pick([[1, 1], [2, 1], [3, 1], [-1, 1], [-2, 1], [-3, 1], [1, 2], [-1, 2], [2, 3], [-2, 3], [3, 2], [-3, 2], [0, 1]]), p = c[0], q = c[1], m = p / q;
      var x0 = q === 3 ? -3 : -2, y0 = rint(-2, 2), n = y0 - m * x0, A = [x0, y0], B = [x0 + q * (q === 1 ? 2 : 1), y0 + p * (q === 1 ? 2 : 1)];
      if (Math.abs(B[1]) > 5) { B = [x0 + q, y0 + p]; }
      var G = pla({ win: [-5, 5, -5, 5], W: 260, fns: [[m, n, "c0"]], pts: [[A[0], A[1], null, "p0"], [B[0], B[1], null, "p0"]] });
      return ret(numQ(m, 0.006), function () { return T(L3("Quin és el pendent d'aquesta recta? (Els punts marcats estan en la quadrícula.)", "¿Cuál es la pendiente de esta recta? (Los puntos marcados están en la cuadrícula.)", "What is the slope of this line? (The marked points are on the grid.)")) + G; },
        function () { var dx = B[0] - A[0], dy = B[1] - A[1]; return fill(T(L3("De {A} a {B} avancem {dx} i {v} {dy}: {m}.", "De {A} a {B} avanzamos {dx} y {v} {dy}: {m}.", "From {A} to {B} we go {dx} across and {v} {dy}: {m}.")), { A: tex(ptx(A[0], A[1])), B: tex(ptx(B[0], B[1])), dx: dx, dy: Math.abs(dy), v: T(dy >= 0 ? L3("pugem", "subimos", "up") : L3("baixem", "bajamos", "down")), m: tex("m=" + qTex(dy, dx)) }); });
    },
    img1: function () {
      var m = rnz(-4, 4), n = rnz(-6, 6), x = rint(-5, 5), y = m * x + n;
      return ret(numQ(y), function () { return fill(T(L3("Quin valor té y per a {x} en {f}?", "¿Qué valor tiene y para {x} en {f}?", "What is y when {x} for {f}?")), { x: $("x=" + x), f: $(eqTex(m, n)) }); },
        function () { return tex("y=" + m + "\\cdot" + nfp(x) + (n > 0 ? "+" : "-") + Math.abs(n) + "=" + nf(m * x) + (n > 0 ? "+" : "-") + Math.abs(n) + "=" + y); });
    },
    eqpm: function () {
      var m = rnz(-4, 4), a = rnz(-4, 4), n = rint(-6, 8), b = m * a + n;
      return ret(numQ(n), function () { return fill(T(L3("Una recta té pendent {m} i passa per {P}. Quant val n en {f}?", "Una recta tiene pendiente {m} y pasa por {P}. ¿Cuánto vale n en {f}?", "A line has slope {m} and goes through {P}. What is n in {f}?")), { m: $("m=" + m), P: $(ptx(a, b)), f: $("y=" + (m === 1 ? "" : m === -1 ? "-" : m) + "x+n") }); },
        function () { return tex(b + "=" + m + "\\cdot" + nfp(a) + "+n\\ \\Rightarrow\\ " + b + "=" + (m * a) + "+n\\ \\Rightarrow\\ n=" + n) + " → " + tex(eqTex(m, n)); });
    },
    kind: function () {
      var K = [L3("De proporcionalitat", "De proporcionalidad", "Direct proportion"), L3("Lineal (amb n ≠ 0)", "Lineal (con n ≠ 0)", "Linear (with n ≠ 0)"), L3("Constant", "Constante", "Constant"), L3("Cap d'aquestes", "Ninguna de estas", "None of these")];
      var t = rint(0, 3), f, why;
      if (t === 0) { var m = pick([2, 3, -4, -1, 5, 0.5, -2.5]); f = pick([eqTex(m, 0), "y=\\dfrac{x}{" + rint(2, 5) + "}"]); why = L3("És de la forma y = mx: recta que passa per l'origen.", "Es de la forma y = mx: recta que pasa por el origen.", "It has the form y = mx: a line through the origin."); }
      else if (t === 1) { var m1 = rnz(-4, 4), n1 = rnz(-7, 7); f = pick([eqTex(m1, n1), "y=" + n1 + (m1 > 0 ? "+" : "-") + (Math.abs(m1) === 1 ? "" : Math.abs(m1)) + "x"]); why = L3("És de la forma y = mx + n amb n ≠ 0: recta que no passa per l'origen.", "Es de la forma y = mx + n con n ≠ 0: recta que no pasa por el origen.", "It has the form y = mx + n with n ≠ 0: a line that misses the origin."); }
      else if (t === 2) { f = "y=" + rnz(-9, 9); why = L3("La y val sempre el mateix: recta horitzontal (m = 0).", "La y vale siempre lo mismo: recta horizontal (m = 0).", "y is always the same: a horizontal line (m = 0)."); }
      else { f = pick(["y=x^2", "y=x^2-" + rint(1, 5), "y=\\dfrac{" + rint(2, 12) + "}{x}", "y=2x^2+1", "y=x^3"]); why = L3("La x està elevada al quadrat (o al cub) o dividint: el gràfic no és una recta.", "La x está elevada al cuadrado (o al cubo) o dividiendo: la gráfica no es una recta.", "x is squared (or cubed) or dividing: the graph isn't a straight line."); }
      return ret({ opts: K, ans: t }, function () { return fill(T(L3("De quin tipus és la funció {f}?", "¿De qué tipo es la función {f}?", "What type of function is {f}?")), { f: $(f) }); }, function () { return T(why); });
    },
    /* el problema es genera amb una llavor: en canviar d'idioma es torna a escriure amb els mateixos nombres */
    prob: function () {
      var p = pick(PROBS), seed = Math.random(), r, rl = null;
      function make() {
        var sr = Math.random, s = seed;
        Math.random = function () { s = (s * 9301 + 49297) % 233280 / 233280; return s; };
        try { r = p(); } finally { Math.random = sr; }
        rl = lang;
      }
      make();
      return ret(numQ(r.v, 0.006), function () { if (rl !== lang) make(); return r.q; }, function () { if (rl !== lang) make(); return r.s; });
    }
  };

  function wDrill(w) {
    var kind = w.dataset.kind, q, done = false, res = 0, ok = 0, tot = 0, G = null;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore"), ob = w.querySelector(".dopts");
    function gen() { q = GEN[kind](); if (q.opts && q.ans == null) { var o = optsTxt(q.opts[0], q.opts.slice(1)); q.opts = o.opts; q.ans = o.ans; } }
    function paint() {
      dq.innerHTML = rtex(q.q(G)); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (q.click && !done) onPick(dq, function (P) { G = P; check(); });
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
      else if (q.click) good = near(G[0], q.click[0]) && near(G[1], q.click[1]);
      else if (q.pair) {
        var P = pairIn(inp.value); if (!P) { info.innerHTML = warn(u("pair")); return; }
        good = near(P[0], q.pair[0]) && near(P[1], q.pair[1]);
      } else {
        var v = numIn(inp.value); if (v === null) { info.innerHTML = warn(u("num")); return; }
        good = Math.abs(v - q.num) <= (q.tol || 1e-6);
      }
      done = true; tot++; res = { good: good, pick: j }; if (good) ok++;
      paint();
    }
    function fresh() { gen(); done = false; G = null; if (inp) inp.value = ""; info.innerHTML = ""; paint(); }
    var cb = w.querySelector('[data-a="check"]'); if (cb) cb.addEventListener("click", function () { check(); });
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); if (inp) inp.focus(); });
    if (inp) inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    gen(); onLang(paint);
  }
  window.FM210 = { pla: pla, GEN: GEN, STORIES: STORIES, MATCH: MATCH, PROBS: PROBS, eqTex: eqTex, eqTexF: eqTexF, fracTex: fracTex, at: at, vHits: vHits, VCURVES: VCURVES, parseExpr: parseExpr, ev: ev, etex: etex, pairIn: pairIn, numsIn: numsIn };

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

  var TITLES = { va: "Funcions · FentMates", es: "Funciones · FentMates", en: "Functions · FentMates" };
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
    wVline(); wTable(); wPlot(); wM(); wSlope(); wMN(); wConst(); wStory(); wTwo();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
