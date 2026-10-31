(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-3eso-u9-done", NSEC = 8;

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
     unitat 9: perímetres i àrees. Teorema de Pitàgores
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

  /* triangle rectangle amb els quadrats dels tres costats (com tri_sq de build.py) */
  function triSq(a, b, grid) {
    var A = [a, 0], B = [0, b], it = [["poly", [[0, 0], [a, 0], [a, -a], [0, -a]], "q0"], ["poly", [[0, 0], [0, b], [-b, b], [-b, 0]], "q1"], ["poly", [A, B, [b, a + b], [a + b, a]], "q2"]], i;
    if (grid) {
      for (i = 1; i < a; i++) { it.push(["seg", [i, 0], [i, -a], "gl"]); it.push(["seg", [0, -i], [a, -i], "gl"]); }
      for (i = 1; i < b; i++) { it.push(["seg", [0, i], [-b, i], "gl"]); it.push(["seg", [-i, 0], [-i, b], "gl"]); }
    }
    var c = Math.hypot(a, b);
    it.push(["poly", [[0, 0], A, B], "tr"], ["ra", [0, 0], A, B],
      T_([a / 2, -a / 2], lab(a * a), { cls: "big" }), T_([-b / 2, b / 2], lab(b * b), { cls: "big" }), T_([(a + b) / 2, (a + b) / 2], (isInt(c * c) ? "" : "≈") + lab(c * c), { cls: "big" }),
      T_([a / 2, 0], "a", { dy: -6 }), T_([0, b / 2], "b", { dx: 8, a: "start" }), T_(off(A, B, 0.14 * Math.min(a, b)), "c", { cls: "hy" }));
    return it;
  }
  /* giny: quadrats sobre els costats */
  function wPit() {
    var w = document.getElementById("w-pit"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var a = +I.a.value, b = +I.b.value, c2 = a * a + b * b, c = Math.sqrt(c2);
      showRv(w, "a", "a", a); showRv(w, "b", "b", b);
      out.innerHTML = G(triSq(a, b, isInt(a) && isInt(b)), { W: 300, maxh: 300 }) + gcol([
        T(L3("Àrees dels quadrats dels catets:", "Áreas de los cuadrados de los catetos:", "Areas of the squares on the legs:")) + " " + tex("a^2=" + n4(a * a) + ",\\ \\ b^2=" + n4(b * b)),
        T(L3("Àrea del quadrat de la hipotenusa:", "Área del cuadrado de la hipotenusa:", "Area of the square on the hypotenuse:")) + " " + tex("c^2=a^2+b^2=" + n4(c2)),
        '<span class="big">' + tex("c=" + rt(c2)) + "</span>"]);
    }
    [I.a, I.b].forEach(function (s) { s.addEventListener("input", paint); });
    quickBind(w, function (v) { I.a.value = v[0]; I.b.value = v[1]; paint(); });
    onLang(paint);
  }
  /* giny: demostració per recol·locació */
  function wProof() {
    var w = document.getElementById("w-proof"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), mode = "0";
    function paint() {
      var a = +I.a.value, b = +I.b.value, s = a + b, it;
      showRv(w, "a", "a", a); showRv(w, "b", "b", b);
      var sq = ["poly", [[0, 0], [s, 0], [s, s], [0, s]], "frame"];
      if (mode === "0") {
        var P1 = [a, 0], P2 = [s, a], P3 = [b, s], P4 = [0, b];
        it = [sq, ["poly", [P1, P2, P3, P4], "q2"], ["poly", [[0, 0], P1, P4], "tr"], ["poly", [[s, 0], P2, P1], "tr"], ["poly", [[s, s], P3, P2], "tr"], ["poly", [[0, s], P4, P3], "tr"], T_([s / 2, s / 2], "c²", { cls: "big" })];
      } else {
        it = [sq, ["poly", [[0, 0], [a, 0], [a, a], [0, a]], "q0"], ["poly", [[a, a], [s, a], [s, s], [a, s]], "q1"],
          ["poly", [[a, 0], [s, 0], [a, a]], "tr"], ["poly", [[s, 0], [s, a], [a, a]], "tr"], ["poly", [[0, a], [a, a], [0, s]], "tr"], ["poly", [[a, a], [a, s], [0, s]], "tr"],
          T_([a / 2, a / 2], "a²", { cls: "big" }), T_([a + b / 2, a + b / 2], "b²", { cls: "big" })];
      }
      it.push(T_([a / 2, 0], "a", { dy: 15 }), T_([a + b / 2, 0], "b", { dy: 15 }), T_([0, b / 2], mode === "0" ? "b" : "a", { dx: -8, a: "end" }));
      var tri = a * b / 2;
      out.innerHTML = G(it, { W: 260, maxh: 260 }) + gcol([
        T(L3("Àrea del quadrat gran:", "Área del cuadrado grande:", "Area of the big square:")) + " " + tex("(a+b)^2=" + n4(s * s)),
        T(L3("Els quatre triangles:", "Los cuatro triángulos:", "The four triangles:")) + " " + tex("4\\cdot\\dfrac{a\\cdot b}{2}=" + n4(4 * tri)),
        T(L3("Zona lliure:", "Zona libre:", "Free region:")) + " " + tex((mode === "0" ? "c^2" : "a^2+b^2") + "=" + n4(s * s) + "-" + n4(4 * tri) + "=" + n4(s * s - 4 * tri)),
        "💡 " + T(L3("Canvia de disposició: la zona lliure sempre té la mateixa àrea.", "Cambia de disposición: la zona libre siempre tiene la misma área.", "Switch layouts: the free region always has the same area."))]);
    }
    segBind(w, function (k) { mode = k; paint(); });
    [I.a, I.b].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }
  /* triangle rectangle amb mesures (per a la calculadora) */
  function rtFig(a, b, la, lb, lc, hot) {
    return G([["poly", [[0, 0], [a, 0], [0, b]], "tr"], ["ra", [0, 0], [a, 0], [0, b]], T_([a / 2, 0], la, { dy: 15, cls: hot === "a" ? "hot" : "" }), T_([0, b / 2], lb, { dx: -8, a: "end", cls: hot === "b" ? "hot" : "" }),
      T_(off([a, 0], [0, b], -0.06 * (a + b)), lc, { a: "start", cls: hot === "c" ? "hot" : "hy" })], { W: 260, maxh: 200, pad: 44 });
  }
  /* càlcul d'un costat (passos) */
  function pythSteps(a, b, c) {
    var rows = [], miss = a == null ? "a" : b == null ? "b" : "c";
    if (miss === "c") { var c2 = a * a + b * b; rows.push(tex("c=\\sqrt{a^2+b^2}=\\sqrt{" + nf(a) + "^2+" + nf(b) + "^2}=\\sqrt{" + n4(a * a) + "+" + n4(b * b) + "}=" + rt(c2))); return { rows: rows, v: Math.sqrt(c2), miss: miss }; }
    var k = miss === "a" ? b : a, d = c * c - k * k;
    rows.push(tex(miss + "=\\sqrt{c^2-" + (miss === "a" ? "b" : "a") + "^2}=\\sqrt{" + nf(c) + "^2-" + nf(k) + "^2}=\\sqrt{" + n4(c * c) + "-" + n4(k * k) + "}=" + rt(d)));
    return { rows: rows, v: Math.sqrt(d), miss: miss };
  }
  function wPcalc() {
    var w = document.getElementById("w-pcalc"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), g = w.querySelector(".gout"), info = w.querySelector(".info");
    function rd(k) { var s = I[k].value.trim(); if (s === "" || s === "?") return null; var v = numIn(s); return v === null || v <= 0 ? NaN : v; }
    function paint() {
      out.innerHTML = g.innerHTML = info.innerHTML = "";
      var a = rd("a"), b = rd("b"), c = rd("c"), blanks = [a, b, c].filter(function (v) { return v === null; }).length;
      if ([a, b, c].some(function (v) { return v !== null && isNaN(v); })) { info.innerHTML = warn(u("num")); return; }
      if (blanks !== 1) { info.innerHTML = warn(T(L3("Escriu dos costats i deixa en blanc el que vols calcular.", "Escribe dos lados y deja en blanco el que quieres calcular.", "Type two sides and leave blank the one you want to find."))); return; }
      if (c !== null && ((a !== null && a >= c) || (b !== null && b >= c))) { info.innerHTML = warn(T(L3("La hipotenusa ha de ser el costat més llarg.", "La hipotenusa debe ser el lado más largo.", "The hypotenuse must be the longest side."))); return; }
      var r = pythSteps(a, b, c), A = a == null ? r.v : a, B = b == null ? r.v : b;
      out.innerHTML = rows2html([T(L3(r.miss === "c" ? "Busquem la hipotenusa: sumem els quadrats dels catets." : "Busquem un catet: al quadrat de la hipotenusa li restem el de l'altre catet.", r.miss === "c" ? "Buscamos la hipotenusa: sumamos los cuadrados de los catetos." : "Buscamos un cateto: al cuadrado de la hipotenusa le restamos el del otro cateto.", r.miss === "c" ? "We want the hypotenuse: add the squares of the legs." : "We want a leg: subtract the square of the other leg from the square of the hypotenuse."))].concat(r.rows));
      g.innerHTML = rtFig(A, B, "a = " + lab(A), "b = " + lab(B), "c = " + lab(c == null ? r.v : c), r.miss);
    }
    ["a", "b", "c"].forEach(function (k) { I[k].addEventListener("input", paint); });
    quickBind(w, function (v) { I.a.value = v[0]; I.b.value = v[1]; I.c.value = v[2]; paint(); });
    onLang(paint);
  }

  /* ---------- classificació de triangles ---------- */
  function tri3(a, b, c, mark) {
    var xA = (c * c + b * b - a * a) / (2 * c), yA = Math.sqrt(Math.max(b * b - xA * xA, 0)), P = [xA, yA], it = [["poly", [[0, 0], [c, 0], P], "tr"]];
    if (mark === "r") it.push(["ra", P, [0, 0], [c, 0]]);
    else it.push(["arc", P, 0.16 * c, Math.atan2(-yA, -xA) * 180 / PI, Math.atan2(-yA, c - xA) * 180 / PI, "ang"]);
    it.push(T_([c / 2, 0], lab(c), { dy: 15 }), T_(off([0, 0], P, 0.08 * c), lab(b)), T_(off(P, [c, 0], 0.08 * c), lab(a)));
    return it;
  }
  var KIND = [L3("acutangle", "acutángulo", "acute"), L3("rectangle", "rectángulo", "right"), L3("obtusangle", "obtusángulo", "obtuse")];
  function classify(s) {
    var t = s.slice().sort(function (p, q) { return p - q; }), a = t[0], b = t[1], c = t[2], L = c * c, Rr = a * a + b * b;
    var k = Math.abs(L - Rr) < 1e-9 ? 1 : L < Rr ? 0 : 2;
    return { a: a, b: b, c: c, k: k, ok: c < a + b, row: tex(nf(c) + "^2=" + n4(L) + "\\qquad " + nf(a) + "^2+" + nf(b) + "^2=" + n4(a * a) + "+" + n4(b * b) + "=" + n4(Rr)) + " → " + tex(n4(L) + (k === 1 ? "=" : k === 0 ? "<" : ">") + n4(Rr)) };
  }
  function wClass() {
    var w = document.getElementById("w-class"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), g = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      out.innerHTML = g.innerHTML = info.innerHTML = "";
      var v = ["a", "b", "c"].map(function (k) { return numIn(I[k].value); });
      if (v.some(function (x) { return x === null || x <= 0; })) { info.innerHTML = warn(u("num")); return; }
      var C = classify(v);
      if (!C.ok) { out.innerHTML = rows2html([fill(T(L3("El costat més llarg, {c}, no és menor que la suma dels altres dos, {s}: <strong>no hi ha cap triangle</strong> amb aquests costats.", "El lado más largo, {c}, no es menor que la suma de los otros dos, {s}: <strong>no existe ningún triángulo</strong> con esos lados.", "The longest side, {c}, isn't less than the sum of the other two, {s}: <strong>no triangle</strong> has these sides.")), { c: tex(nf(C.c)), s: tex(nf(C.a) + "+" + nf(C.b) + "=" + nf(C.a + C.b)) })]); return; }
      out.innerHTML = rows2html([fill(T(L3("El costat més llarg és {c}. Comparem el seu quadrat amb la suma dels quadrats dels altres dos:", "El lado más largo es {c}. Comparamos su cuadrado con la suma de los cuadrados de los otros dos:", "The longest side is {c}. Compare its square with the sum of the squares of the other two:")), { c: tex("c=" + nf(C.c)) }), C.row,
        '<span class="big">' + T(L3("Triangle ", "Triángulo ", "")) + "<strong>" + T(KIND[C.k]) + "</strong>" + T(L3("", "", " triangle")) + "</span>"]);
      g.innerHTML = G(tri3(C.a, C.b, C.c, C.k === 1 ? "r" : "x"), { W: 300, maxh: 200 });
    }
    ["a", "b", "c"].forEach(function (k) { I[k].addEventListener("input", paint); });
    quickBind(w, function (v) { I.a.value = v[0]; I.b.value = v[1]; I.c.value = v[2]; paint(); });
    onLang(paint);
  }

  /* ---------- Pitàgores en figures planes ---------- */
  /* cada figura: noms dels lliscadors, validació, dibuix i passos. p, q, r són els valors dels lliscadors */
  var APL = {
    rect: { k: ["b", "h"], f: function (b, h) { var d2_ = b * b + h * h;
      return { it: [["poly", [[0, 0], [b, 0], [b, h], [0, h]], "gf"], ["poly", [[0, 0], [b, 0], [b, h]], "tr"], ["ra", [b, 0], [0, 0], [b, h]], T_([b / 2, 0], "b = " + lab(b), { dy: 15 }), T_([b, h / 2], "h = " + lab(h), { dx: 8, a: "start" }), T_(off([0, 0], [b, h], 0.06 * (b + h)), "d", { cls: "hot" })],
        rows: [T(L3("La diagonal és la hipotenusa d'un triangle de catets la base i l'altura:", "La diagonal es la hipotenusa de un triángulo de catetos la base y la altura:", "The diagonal is the hypotenuse of a triangle whose legs are the base and the height:")), tex("d=\\sqrt{b^2+h^2}=\\sqrt{" + n4(b * b) + "+" + n4(h * h) + "}=" + rt(d2_))], v: Math.sqrt(d2_) }; } },
    sq: { k: ["l"], f: function (l) { return { it: [["poly", [[0, 0], [l, 0], [l, l], [0, l]], "gf"], ["poly", [[0, 0], [l, 0], [l, l]], "tr"], ["ra", [l, 0], [0, 0], [l, l]], T_([l / 2, 0], "l = " + lab(l), { dy: 15 }), T_([l, l / 2], "l", { dx: 8, a: "start" }), T_(off([0, 0], [l, l], 0.12 * l), "d", { cls: "hot" })],
        rows: [T(L3("La diagonal és la hipotenusa d'un triangle de catets iguals al costat:", "La diagonal es la hipotenusa de un triángulo de catetos iguales al lado:", "The diagonal is the hypotenuse of a triangle whose legs are both the side:")), tex("d=\\sqrt{l^2+l^2}=\\sqrt{2\\cdot" + n4(l * l) + "}=" + rt(2 * l * l))], v: Math.SQRT2 * l }; } },
    iso: { k: ["l", "b"], bad: function (l, b) { return b >= 2 * l ? L3("La base ha de ser menor que la suma dels dos costats iguals.", "La base debe ser menor que la suma de los dos lados iguales.", "The base must be shorter than the two equal sides together.") : null; },
      f: function (l, b) { var hb = b / 2, h = Math.sqrt(l * l - hb * hb);
      return { it: [["poly", [[-hb, 0], [hb, 0], [0, h]], "gf"], ["poly", [[0, 0], [hb, 0], [0, h]], "tr"], ["seg", [0, 0], [0, h], "d"], ["ra", [0, 0], [hb, 0], [0, h]], T_([hb / 2, 0], lab(hb), { dy: 15 }), T_([0, h / 2], "h", { dx: -8, a: "end", cls: "hot" }), T_(off([hb, 0], [0, h], -0.1 * l), "l = " + lab(l), { a: "start" })],
        rows: [T(L3("L'altura divideix la base en dues meitats. Triangle: hipotenusa el costat, catets mitja base i l'altura.", "La altura divide la base en dos mitades. Triángulo: hipotenusa el lado, catetos media base y la altura.", "The height splits the base in half. Triangle: hypotenuse the side, legs half the base and the height.")), tex("h=\\sqrt{l^2-\\left(\\tfrac b2\\right)^2}=\\sqrt{" + n4(l * l) + "-" + n4(hb * hb) + "}=" + rt(l * l - hb * hb))], v: h }; } },
    eq: { k: ["l"], f: function (l) { var hb = l / 2, h = Math.sqrt(l * l - hb * hb);
      return { it: [["poly", [[-hb, 0], [hb, 0], [0, h]], "gf"], ["poly", [[0, 0], [hb, 0], [0, h]], "tr"], ["seg", [0, 0], [0, h], "d"], ["ra", [0, 0], [hb, 0], [0, h]], T_([hb / 2, 0], lab(hb), { dy: 15 }), T_([0, h / 2], "h", { dx: -8, a: "end", cls: "hot" }), T_(off([hb, 0], [0, h], -0.1 * l), "l = " + lab(l), { a: "start" })],
        rows: [T(L3("L'altura divideix el costat de baix en dues meitats:", "La altura divide el lado de abajo en dos mitades:", "The height splits the bottom side in half:")), tex("h=\\sqrt{l^2-\\left(\\tfrac l2\\right)^2}=\\sqrt{" + n4(l * l) + "-" + n4(hb * hb) + "}=" + rt(l * l - hb * hb))], v: h }; } },
    rom: { k: ["D", "d"], f: function (D, d) { var x = D / 2, y = d / 2;
      return { it: [["poly", [[-x, 0], [0, y], [x, 0], [0, -y]], "gf"], ["seg", [-x, 0], [x, 0], "d"], ["seg", [0, -y], [0, y], "d"], ["poly", [[0, 0], [x, 0], [0, y]], "tr"], ["ra", [0, 0], [x, 0], [0, y]], T_([x / 2, 0], lab(x), { dy: 15 }), T_([0, y / 2], lab(y), { dx: -6, a: "end" }), T_(off([x, 0], [0, y], -0.08 * (x + y)), "l", { a: "start", cls: "hot" })],
        rows: [T(L3("Les diagonals es tallen per la meitat i perpendicularment:", "Las diagonales se cortan por la mitad y perpendicularmente:", "The diagonals bisect each other at right angles:")), tex("l=\\sqrt{\\left(\\tfrac D2\\right)^2+\\left(\\tfrac d2\\right)^2}=\\sqrt{" + n4(x * x) + "+" + n4(y * y) + "}=" + rt(x * x + y * y))], v: Math.hypot(x, y) }; } },
    trap: { k: ["B", "b", "c"], bad: function (B, b, c) { return B <= b ? L3("La base gran B ha de ser més llarga que la base menuda b.", "La base mayor B debe ser más larga que la base menor b.", "The long base B must be longer than the short base b.") : c <= (B - b) / 2 ? L3("El costat c és massa curt per a unir les dues bases.", "El lado c es demasiado corto para unir las dos bases.", "Side c is too short to join the two bases.") : null; },
      f: function (B, b, c) { var e = (B - b) / 2, h = Math.sqrt(c * c - e * e), X0 = -B / 2;
      return { it: [["poly", [[X0, 0], [B / 2, 0], [b / 2, h], [-b / 2, h]], "gf"], ["poly", [[b / 2, 0], [B / 2, 0], [b / 2, h]], "tr"], ["seg", [b / 2, 0], [b / 2, h], "d"], ["ra", [b / 2, 0], [B / 2, 0], [b / 2, h]],
          T_([0, 0], "B = " + lab(B), { dy: 15 }), T_([0, h], "b = " + lab(b), { dy: -7 }), T_([b / 2 + e / 2, 0], lab(e), { dy: -6 }), T_([b / 2, h / 2], "h", { dx: -8, a: "end", cls: "hot" }), T_(off([B / 2, 0], [b / 2, h], -0.05 * B), "c = " + lab(c), { a: "start" })],
        rows: [T(L3("En traçar les altures, a cada costat de la base gran sobra un tros de ", "Al trazar las alturas, a cada lado de la base mayor sobra un trozo de ", "Drawing the heights leaves a piece on each side of the long base of ")) + tex("\\tfrac{B-b}{2}=" + n4(e)) + ":", tex("h=\\sqrt{c^2-\\left(\\tfrac{B-b}2\\right)^2}=\\sqrt{" + n4(c * c) + "-" + n4(e * e) + "}=" + rt(c * c - e * e))], v: h }; } }
  };
  function wApl() {
    var w = document.getElementById("w-apl"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), kind = "rect", keys = ["p", "q", "r"];
    function paint() {
      var F = APL[kind], vals = F.k.map(function (_, i) { return +I[keys[i]].value; });
      keys.forEach(function (k, i) { showRange(w, k, i < F.k.length); if (i < F.k.length) showRv(w, k, F.k[i], vals[i]); });
      info.innerHTML = "";
      var bad = F.bad && F.bad.apply(null, vals);
      if (bad) { out.innerHTML = ""; info.innerHTML = warn(T(bad)); return; }
      var r = F.f.apply(null, vals);
      out.innerHTML = G(r.it, { W: 320, maxh: 230, pad: 46 }) + gcol(r.rows);
    }
    segBind(w, function (k) { kind = k; paint(); });
    keys.forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- distància entre dos punts ---------- */
  function cplot(A, B) {
    var x0 = Math.min(A[0], B[0], 0) - 1, x1 = Math.max(A[0], B[0], 0) + 1, y0 = Math.min(A[1], B[1], 0) - 1, y1 = Math.max(A[1], B[1], 0) + 1, it = [], k;
    for (k = Math.ceil(x0); k <= x1; k++) it.push(["seg", [k, y0], [k, y1], "gl"]);
    for (k = Math.ceil(y0); k <= y1; k++) it.push(["seg", [x0, k], [x1, k], "gl"]);
    it.push(["seg", [x0, 0], [x1, 0], "axis"], ["seg", [0, y0], [0, y1], "axis"]);
    var C = [B[0], A[1]];
    if (A[0] !== B[0] && A[1] !== B[1]) it.push(["poly", [A, C, B], "tr"], ["ra", C, A, B]);
    it.push(["seg", A, B, "hl"], ["dot", A, "pa"], ["dot", B, "pa"], T_(A, "A(" + lab(A[0]) + "; " + lab(A[1]) + ")", { dy: A[1] > B[1] ? -9 : 17 }), T_(B, "B(" + lab(B[0]) + "; " + lab(B[1]) + ")", { dy: B[1] >= A[1] ? -9 : 17 }));
    if (A[0] !== B[0]) it.push(T_(mid(A, C), lab(Math.abs(B[0] - A[0])), { dy: A[1] <= B[1] ? 15 : -7 }));
    if (A[1] !== B[1]) it.push(T_(mid(C, B), lab(Math.abs(B[1] - A[1])), { dx: B[0] >= A[0] ? 8 : -8, a: B[0] >= A[0] ? "start" : "end" }));
    return G(it, { W: 300, maxh: 280, pad: 24 });
  }
  function distSteps(A, B) {
    var dx = B[0] - A[0], dy = B[1] - A[1];
    return tex("d=\\sqrt{(" + nf(B[0]) + "-" + nfp(A[0]) + ")^2+(" + nf(B[1]) + "-" + nfp(A[1]) + ")^2}=\\sqrt{" + nfp(dx) + "^2+" + nfp(dy) + "^2}=\\sqrt{" + n4(dx * dx) + "+" + n4(dy * dy) + "}=" + rt(dx * dx + dy * dy));
  }
  function wDist() {
    var w = document.getElementById("w-dist"); if (!w) return;
    var I = inputs(w), out = w.querySelector(".hsteps"), g = w.querySelector(".gout"), info = w.querySelector(".info");
    function paint() {
      out.innerHTML = g.innerHTML = info.innerHTML = "";
      var A = pairIn(I.p.value), B = pairIn(I.q.value);
      if (!A || !B) { info.innerHTML = warn(u("pair")); return; }
      if (Math.max(Math.abs(A[0]), Math.abs(A[1]), Math.abs(B[0]), Math.abs(B[1])) > 40) { info.innerHTML = warn(T(L3("Fes servir coordenades entre −40 i 40.", "Usa coordenadas entre −40 y 40.", "Use coordinates between −40 and 40."))); return; }
      out.innerHTML = rows2html([T(L3("Catets: diferència de les x i diferència de les y.", "Catetos: diferencia de las x y diferencia de las y.", "Legs: difference of the x's and difference of the y's.")), distSteps(A, B)]);
      g.innerHTML = cplot(A, B);
    }
    [I.p, I.q].forEach(function (x) { x.addEventListener("input", paint); });
    quickBind(w, function (v) { I.p.value = v[0]; I.q.value = v[1]; paint(); });
    onLang(paint);
  }

  /* ---------- àrees de polígons ---------- */
  var AREA = {
    sq: { k: ["l"], f: function (l) { return { it: [["poly", [[0, 0], [l, 0], [l, l], [0, l]], "gf"], T_([l / 2, 0], "l = " + lab(l), { dy: 15 })],
        A: [tex("A=l^2=" + nf(l) + "^2=" + n4(l * l))], P: [tex("P=4\\cdot" + nf(l) + "=" + n4(4 * l))], a: l * l, p: 4 * l }; } },
    re: { k: ["b", "h"], f: function (b, h) { return { it: [["poly", [[0, 0], [b, 0], [b, h], [0, h]], "gf"], T_([b / 2, 0], "b = " + lab(b), { dy: 15 }), T_([b, h / 2], "h = " + lab(h), { dx: 8, a: "start" })],
        A: [tex("A=b\\cdot h=" + nf(b) + "\\cdot" + nf(h) + "=" + n4(b * h))], P: [tex("P=2\\cdot" + nf(b) + "+2\\cdot" + nf(h) + "=" + n4(2 * b + 2 * h))], a: b * h, p: 2 * (b + h) }; } },
    ro: { k: ["b", "h", "c"], bad: function (b, h, c) { return c < h ? L3("El costat oblic c no pot ser més curt que l'altura.", "El lado oblicuo c no puede ser más corto que la altura.", "The slanted side c can't be shorter than the height.") : null; },
      f: function (b, h, c) { var e = Math.sqrt(c * c - h * h);
      return { it: [["poly", [[0, 0], [b, 0], [b + e, h], [e, h]], "gf"], ["seg", [e, 0], [e, h], "d"], ["ra", [e, 0], [e + 1, 0], [e, h]], T_([b / 2, 0], "b = " + lab(b), { dy: 15 }), T_([e, h / 2], "h = " + lab(h), { dx: 6, a: "start" }), T_(off([b, 0], [b + e, h], -0.04 * b), "c = " + lab(c), { a: "start" })],
        A: [tex("A=b\\cdot h=" + nf(b) + "\\cdot" + nf(h) + "=" + n4(b * h))], P: [tex("P=2\\cdot" + nf(b) + "+2\\cdot" + nf(c) + "=" + n4(2 * b + 2 * c))], a: b * h, p: 2 * (b + c) }; } },
    rb: { k: ["D", "d"], f: function (D, d) { var x = D / 2, y = d / 2, l2 = x * x + y * y;
      return { it: [["poly", [[-x, 0], [0, y], [x, 0], [0, -y]], "gf"], ["seg", [-x, 0], [x, 0], "d"], ["seg", [0, -y], [0, y], "d"], T_([-x / 2, 0], "D = " + lab(D), { dy: -6 }), T_([0, -y / 2], "d = " + lab(d), { dx: 6, a: "start" })],
        A: [tex("A=\\dfrac{D\\cdot d}{2}=\\dfrac{" + nf(D) + "\\cdot" + nf(d) + "}{2}=" + n4(D * d / 2))], P: [T(L3("Costat, amb Pitàgores:", "Lado, con Pitágoras:", "Side, by Pythagoras:")) + " " + tex("l=\\sqrt{" + n4(x) + "^2+" + n4(y) + "^2}=" + rt(l2)), tex("P=4\\,l" + ap(4 * Math.sqrt(l2)))], a: D * d / 2, p: 4 * Math.sqrt(l2) }; } },
    tp: { k: ["B", "b", "h"], bad: function (B, b) { return B < b ? L3("La base gran B no pot ser més curta que la base menuda b.", "La base mayor B no puede ser más corta que la base menor b.", "The long base B can't be shorter than the short base b.") : null; },
      f: function (B, b, h) { var e = (B - b) / 2, c2 = e * e + h * h, c = Math.sqrt(c2);
      return { it: [["poly", [[-B / 2, 0], [B / 2, 0], [b / 2, h], [-b / 2, h]], "gf"], ["seg", [b / 2, 0], [b / 2, h], "d"], ["ra", [b / 2, 0], [b / 2 + 1, 0], [b / 2, h]], T_([0, 0], "B = " + lab(B), { dy: 15 }), T_([0, h], "b = " + lab(b), { dy: -7 }), T_([b / 2, h / 2], "h = " + lab(h), { dx: -6, a: "end" })],
        A: [tex("A=\\dfrac{(B+b)\\cdot h}{2}=\\dfrac{(" + nf(B) + "+" + nf(b) + ")\\cdot" + nf(h) + "}{2}=" + n4((B + b) * h / 2))],
        P: [T(L3("Costats oblics, amb Pitàgores:", "Lados oblicuos, con Pitágoras:", "Slanted sides, by Pythagoras:")) + " " + tex("c=\\sqrt{" + n4(e) + "^2+" + nf(h) + "^2}=" + rt(c2)), tex("P=B+b+2c" + ap(B + b + 2 * c))], a: (B + b) * h / 2, p: B + b + 2 * c }; } },
    tr: { k: ["b", "h"], f: function (b, h) { var x = b / 2, l2 = x * x + h * h;
      return { it: [["poly", [[-x, 0], [x, 0], [0, h]], "gf"], ["seg", [0, 0], [0, h], "d"], ["ra", [0, 0], [x, 0], [0, h]], T_([0, 0], "b = " + lab(b), { dy: 15 }), T_([0, h / 2], "h = " + lab(h), { dx: 6, a: "start" })],
        A: [tex("A=\\dfrac{b\\cdot h}{2}=\\dfrac{" + nf(b) + "\\cdot" + nf(h) + "}{2}=" + n4(b * h / 2))], P: [T(L3("Costats iguals, amb Pitàgores:", "Lados iguales, con Pitágoras:", "Equal sides, by Pythagoras:")) + " " + tex("l=\\sqrt{" + n4(x) + "^2+" + nf(h) + "^2}=" + rt(l2)), tex("P=b+2l" + ap(b + 2 * Math.sqrt(l2)))], a: b * h / 2, p: b + 2 * Math.sqrt(l2) }; } }
  };
  function wArea() {
    var w = document.getElementById("w-area"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), kind = "sq", keys = ["p", "q", "r"];
    function paint() {
      var F = AREA[kind], vals = F.k.map(function (_, i) { return +I[keys[i]].value; });
      keys.forEach(function (k, i) { showRange(w, k, i < F.k.length); if (i < F.k.length) showRv(w, k, F.k[i], vals[i]); });
      info.innerHTML = "";
      var bad = F.bad && F.bad.apply(null, vals);
      if (bad) { out.innerHTML = ""; info.innerHTML = warn(T(bad)); return; }
      var r = F.f.apply(null, vals);
      out.innerHTML = G(r.it, { W: 320, maxh: 220, pad: 46 }) + gcol(["<b>" + T(L3("Àrea", "Área", "Area")) + "</b>"].concat(r.A, ["<b>" + T(L3("Perímetre", "Perímetro", "Perimeter")) + "</b>"], r.P));
    }
    segBind(w, function (k) { kind = k; paint(); });
    keys.forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- polígons regulars ---------- */
  var PNAME = { 3: L3("triangle equilàter", "triángulo equilátero", "equilateral triangle"), 4: L3("quadrat", "cuadrado", "square"), 5: L3("pentàgon", "pentágono", "pentagon"), 6: L3("hexàgon", "hexágono", "hexagon"), 7: L3("heptàgon", "heptágono", "heptagon"), 8: L3("octàgon", "octógono", "octagon"), 9: L3("enneàgon", "eneágono", "nonagon"), 10: L3("decàgon", "decágono", "decagon") };
  function regV(n, r) { var rot = -90 - 180 / n, V = []; for (var k = 0; k < n; k++) V.push(pol([0, 0], r, rot + 360 * k / n)); return V; }
  function regData(n, l) { return { r: l / (2 * Math.sin(PI / n)), a: l / (2 * Math.tan(PI / n)) }; }
  function wReg() {
    var w = document.getElementById("w-reg"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var n = +I.n.value, l = +I.l.value, d = regData(n, l), r = Math.round(d.r * 100) / 100, V = regV(n, d.r), M = mid(V[0], V[1]), it = [["poly", V, "gf"]];
      showRv(w, "n", "n", n); showRv(w, "l", "l", l);
      V.forEach(function (P) { it.push(["seg", [0, 0], P, "gl"]); });
      it.push(["poly", [[0, 0], M, V[1]], "tr"], ["seg", [0, 0], M, "d"], ["ra", M, V[1], [0, 0]], ["dot", [0, 0]], T_(mid(M, V[1]), lab(l / 2), { dy: 15 }), T_(mid([0, 0], M), "a", { dx: -7, a: "end", cls: "hot" }), T_(off([0, 0], V[1], -0.08 * d.r), "r", { a: "start" }));
      var hx = n === 6, a2 = r * r - l * l / 4, a = Math.sqrt(a2), P = n * l;
      out.innerHTML = G(it, { W: 260, maxh: 260 }) + gcol([
        "<b>" + T(L3("Polígon", "Polígono", "Polygon")) + ":</b> " + T(PNAME[n]) + " " + T(L3("regular", "regular", "")),
        hx ? T(L3("En l'hexàgon el radi és igual al costat: ", "En el hexágono el radio es igual al lado: ", "In a hexagon the radius equals the side: ")) + tex("r=l=" + nf(l))
           : T(L3("El radi d'aquest polígon mesura ", "El radio de este polígono mide ", "This polygon's radius is ")) + tex("r\\approx " + d2(r)) + T(L3(" (normalment te'l donen o el mesures).", " (normalmente te lo dan o lo mides).", " (usually it's given or measured).")),
        T(L3("Apotema, amb Pitàgores:", "Apotema, con Pitágoras:", "Apothem, by Pythagoras:")) + " " + tex("a=\\sqrt{r^2-\\left(\\tfrac l2\\right)^2}=\\sqrt{" + n4(r * r) + "-" + n4(l * l / 4) + "}" + ap(a)),
        tex("P=" + n + "\\cdot" + nf(l) + "=" + n4(P)) + " &nbsp; " + tex("A=\\dfrac{P\\cdot a}{2}" + ap(P * a / 2))]);
    }
    [I.n, I.l].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- circumferència i cercle ---------- */
  function wCirc() {
    var w = document.getElementById("w-circ"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var r = +I.r.value, n = +I.n.value, L = 2 * PI * r, Ar = L * n / 360;
      showRv(w, "r", "r", r); showRv(w, "n", "n", n);
      var it = [["circ", [0, 0], r, "gc"]];
      if (n > 0 && n < 360) it.push(["seg", [0, 0], pol([0, 0], r, 0), ""], ["seg", [0, 0], pol([0, 0], r, n), ""], ["arc", [0, 0], r, 0, n, "hl"], ["arc", [0, 0], 0.22 * r, 0, n, "ang"], T_(pol([0, 0], 0.38 * r, n / 2), n + "°"));
      else if (n === 360) it.push(["arc", [0, 0], r, 0, 359.99, "hl"]);
      it.push(["dot", [0, 0]], T_(pol([0, 0], r / 2, -90), "r = " + lab(r), { dx: 4, a: "start" }), ["seg", [0, 0], [0, -r], "d"]);
      out.innerHTML = G(it, { W: 240, maxh: 240 }) + gcol([
        T(L3("Longitud de la circumferència:", "Longitud de la circunferencia:", "Circumference:")) + " " + tex("L=2\\pi r=2\\pi\\cdot" + nf(r) + "=" + n4(2 * r) + "\\pi\\approx " + d2(L)),
        T(L3("Arc de ", "Arco de ", "Arc of ")) + tex(n + "^\\circ") + ": " + tex("L_{\\text{arc}}=\\dfrac{2\\pi r\\cdot n}{360}=\\dfrac{2\\pi\\cdot" + nf(r) + "\\cdot" + n + "}{360}\\approx " + d2(Ar)),
        "💡 " + fill(T(L3("L'arc és la fracció {f} de la circumferència.", "El arco es la fracción {f} de la circunferencia.", "The arc is the fraction {f} of the circle.")), { f: tex("\\frac{" + n + "}{360}") })]);
    }
    [I.r, I.n].forEach(function (s) { s.addEventListener("input", paint); });
    onLang(paint);
  }
  /* giny: del cercle al «rectangle» */
  function wPizza() {
    var w = document.getElementById("w-pizza"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout");
    function paint() {
      var n = +I.n.value, th = 360 / n, hw = Math.sin(th / 2 * PI / 180), ch = Math.cos(th / 2 * PI / 180), it1 = [], it2 = [], k;
      showRv(w, "n", "n", n);
      for (k = 0; k < n; k++) it1.push(["sect", [0, 0], 1, 90 - th / 2 + k * th, 90 + th / 2 + k * th, k % 2 ? "q1" : "q0"]);
      for (k = 0; k < n / 2; k++) {
        it2.push(["sect", [2 * k * hw, 0], 1, 90 - th / 2, 90 + th / 2, "q0"]);
        it2.push(["sect", [2 * k * hw + hw, ch], 1, 270 - th / 2, 270 + th / 2, "q1"]);
      }
      var base = n * hw;
      it2.push(T_([base / 2 - hw / 2, 0], "≈ πr", { dy: 15 }), T_([-hw, ch / 2], "r", { dx: -6, a: "end" }));
      out.innerHTML = G(it1, { W: 150, maxh: 150 }) + G(it2, { W: 330, maxh: 170 }) + gcol([
        fill(T(L3("Amb {n} sectors, la base fa {b}, i πr = {p}.", "Con {n} sectores, la base mide {b}, y πr = {p}.", "With {n} sectors the base is {b}, and πr = {p}.")), { n: n, b: tex("\\approx " + d2(base) + "\\,r"), p: tex("3\\dc 14\\,r") }),
        T(L3("Com més sectors, més s'assembla a un rectangle d'àrea ", "Cuantos más sectores, más se parece a un rectángulo de área ", "The more sectors, the closer it gets to a rectangle with area ")) + tex("\\pi r\\cdot r=\\pi r^2") + "."]);
    }
    I.n.addEventListener("input", paint);
    onLang(paint);
  }
  var CMODE = {
    c: { k: ["R"], f: function (R) { return { it: [["circ", [0, 0], R, "sh"], ["seg", [0, 0], [R, 0], ""], ["dot", [0, 0]], T_([R / 2, 0], "r = " + lab(R), { dy: -6 })],
        rows: [tex("A=\\pi r^2=\\pi\\cdot" + nf(R) + "^2=" + n4(R * R) + "\\pi\\approx " + d2(PI * R * R))] }; } },
    s: { k: ["R", "n"], f: function (R, n) { return { it: [["circ", [0, 0], R, "gc"], ["sect", [0, 0], R, 0, n, "sh"], ["arc", [0, 0], 0.22 * R, 0, n, "ang"], ["dot", [0, 0]], T_(pol([0, 0], 0.4 * R, n / 2), n + "°"), T_([R / 2, 0], "r = " + lab(R), { dy: 15 })],
        rows: [tex("A=\\dfrac{\\pi r^2\\cdot n}{360}=\\dfrac{\\pi\\cdot" + nf(R) + "^2\\cdot" + n + "}{360}\\approx " + d2(PI * R * R * n / 360))] }; } },
    k: { k: ["R", "r"], bad: function (R, r) { return r >= R ? L3("El radi menut r ha de ser menor que R.", "El radio menor r debe ser menor que R.", "The small radius r must be less than R.") : null; },
      f: function (R, r) { return { it: [["circ", [0, 0], R, "sh"], ["circ", [0, 0], r, "hole"], ["circ", [0, 0], r, "gc"], ["seg", [0, 0], pol([0, 0], R, 30), ""], ["seg", [0, 0], pol([0, 0], r, 150), "d"], ["dot", [0, 0]], T_(pol([0, 0], (R + r) / 2, 40), "R"), T_(pol([0, 0], r / 2, 165), "r")],
        rows: [tex("A=\\pi\\left(R^2-r^2\\right)=\\pi\\left(" + n4(R * R) + "-" + n4(r * r) + "\\right)=" + n4(R * R - r * r) + "\\pi\\approx " + d2(PI * (R * R - r * r)))] }; } },
    t: { k: ["R", "r", "n"], bad: function (R, r) { return r >= R ? L3("El radi menut r ha de ser menor que R.", "El radio menor r debe ser menor que R.", "The small radius r must be less than R.") : null; },
      f: function (R, r, n) { return { it: [["circ", [0, 0], R, "gc"], ["circ", [0, 0], r, "gc"], ["sect", [0, 0], R, 0, n, "sh"], ["sect", [0, 0], r, 0, n, "hole"], ["dot", [0, 0]], T_(pol([0, 0], (R + r) / 2, n / 2), n + "°"), T_([(R + r) / 2, 0], "R − r", { dy: 15 })],
        rows: [tex("A=\\dfrac{\\pi\\left(R^2-r^2\\right)\\cdot n}{360}=\\dfrac{\\pi\\cdot" + n4(R * R - r * r) + "\\cdot" + n + "}{360}\\approx " + d2(PI * (R * R - r * r) * n / 360))] }; } }
  };
  function wCirca() {
    var w = document.getElementById("w-circa"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), info = w.querySelector(".info"), mode = "c", keys = ["R", "r", "n"];
    function paint() {
      var F = CMODE[mode], vals = F.k.map(function (k) { return +I[k].value; });
      keys.forEach(function (k) { var on = F.k.indexOf(k) >= 0; showRange(w, k, on); if (on) showRv(w, k, mode === "c" && k === "R" ? "r" : k, +I[k].value); });
      info.innerHTML = "";
      var bad = F.bad && F.bad.apply(null, vals);
      if (bad) { out.innerHTML = ""; info.innerHTML = warn(T(bad)); return; }
      var r = F.f.apply(null, vals);
      out.innerHTML = G(r.it, { W: 240, maxh: 240 }) + gcol(r.rows);
    }
    segBind(w, function (k) { mode = k; paint(); });
    keys.forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- figures compostes ---------- */
  var COMP = {
    fin: { k: ["a", "b"], f: function (a, b) { var A = a * b + PI * a * a / 8, P = a + 2 * b + PI * a / 2;
      return { it: [["poly", [[0, 0], [a, 0], [a, b], [0, b]], "sh"], ["sect", [a / 2, b], a / 2, 0, 180, "sh"], ["seg", [0, b], [a, b], "d"], T_([a / 2, 0], "a = " + lab(a), { dy: 15 }), T_([a, b / 2], "b = " + lab(b), { dx: 8, a: "start" })],
        rows: [T(L3("Rectangle + semicercle de radi ", "Rectángulo + semicírculo de radio ", "Rectangle + semicircle of radius ")) + tex("\\tfrac a2=" + n4(a / 2)) + ":", tex("A=" + nf(a) + "\\cdot" + nf(b) + "+\\dfrac{\\pi\\cdot" + n4(a / 2) + "^2}{2}\\approx " + d2(A)), tex("P=" + nf(a) + "+2\\cdot" + nf(b) + "+\\dfrac{2\\pi\\cdot" + n4(a / 2) + "}{2}\\approx " + d2(P))], A: A }; } },
    forat: { k: ["a"], f: function (a) { var A = a * a - PI * a * a / 4;
      return { it: [["poly", [[0, 0], [a, 0], [a, a], [0, a]], "sh"], ["circ", [a / 2, a / 2], a / 2, "hole"], ["circ", [a / 2, a / 2], a / 2, "gc"], ["dot", [a / 2, a / 2]], T_([a / 2, 0], "a = " + lab(a), { dy: 15 })],
        rows: [T(L3("Quadrat menys el cercle inscrit (de radi ", "Cuadrado menos el círculo inscrito (de radio ", "Square minus the inscribed disc (radius ")) + tex("\\tfrac a2") + "):", tex("A=" + nf(a) + "^2-\\pi\\cdot" + n4(a / 2) + "^2\\approx " + d2(A))], A: A }; } },
    fulla: { k: ["a"], f: function (a) { var A = 2 * (PI * a * a / 4 - a * a / 2);
      return { it: [["poly", [[0, 0], [a, 0], [a, a], [0, a]], "gf"], ["lens", [a, 0], [0, a], a, "sh"], ["arc", [0, 0], a, 0, 90, ""], ["arc", [a, a], a, 180, 270, ""], ["seg", [a, 0], [0, a], "d"], T_([a / 2, 0], "a = " + lab(a), { dy: 15 })],
        rows: [T(L3("Dues vegades (quart de cercle − mig quadrat):", "Dos veces (cuarto de círculo − medio cuadrado):", "Twice (quarter disc − half square):")), tex("A=2\\left(\\dfrac{\\pi\\cdot" + nf(a) + "^2}{4}-\\dfrac{" + nf(a) + "^2}{2}\\right)\\approx " + d2(A)), tex("P=2\\cdot\\dfrac{2\\pi\\cdot" + nf(a) + "}{4}=\\pi\\cdot" + nf(a) + "\\approx " + d2(PI * a))], A: A }; } },
    cami: { k: ["a", "b", "c"], f: function (a, b, c) { var A = (a + 2 * c) * (b + 2 * c) - a * b;
      return { it: [["poly", [[-c, -c], [a + c, -c], [a + c, b + c], [-c, b + c]], "sh"], ["poly", [[0, 0], [a, 0], [a, b], [0, b]], "lawn"], T_([a / 2, b / 2], lab(a) + " × " + lab(b)), T_([a + c / 2, b / 2], "c", { a: "middle" })],
        rows: [T(L3("Rectangle exterior menys el jardí:", "Rectángulo exterior menos el jardín:", "Outer rectangle minus the garden:")), tex("A=(" + nf(a) + "+2\\cdot" + nf(c) + ")(" + nf(b) + "+2\\cdot" + nf(c) + ")-" + nf(a) + "\\cdot" + nf(b) + "=" + n4(A))], A: A }; } }
  };
  function wComp() {
    var w = document.getElementById("w-comp"); if (!w) return;
    var I = sliders(w), out = w.querySelector(".gout"), mode = "fin", keys = ["a", "b", "c"];
    function paint() {
      var F = COMP[mode], vals = F.k.map(function (k) { return +I[k].value; });
      keys.forEach(function (k) { var on = F.k.indexOf(k) >= 0; showRange(w, k, on); if (on) showRv(w, k, k, +I[k].value); });
      var r = F.f.apply(null, vals);
      out.innerHTML = G(r.it, { W: 300, maxh: 240, pad: 46 }) + gcol(r.rows);
    }
    segBind(w, function (k) { mode = k; paint(); });
    keys.forEach(function (k) { I[k].addEventListener("input", paint); });
    onLang(paint);
  }

  /* ---------- entrenadors ---------- */
  var TRIPLES = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [9, 40, 41]];
  function triple() { var t = pick(TRIPLES), k = t[2] > 20 ? 1 : pick([1, 1, 2, 3]); return t.map(function (v) { return v * k; }); }
  function optsTxt(right, wrongs) {
    var all = [right].concat(wrongs), order = shuffle(all.map(function (_, i) { return i; }));
    return { opts: order.map(function (i) { return all[i]; }), ans: order.indexOf(0) };
  }
  function numQ(v, pi) { return { num: v, tol: tolOf(v, pi) }; }
  function ret(o, q, s) { o.q = q; o.s = s; return o; }
  var GEN = {
    hip: function () {
      var a, b; if (rint(0, 1)) { var t = triple(); a = t[0]; b = t[1]; } else { a = rint(2, 12); b = rint(2, 12); }
      if (rint(0, 1)) { var x = a; a = b; b = x; }
      var r = pythSteps(a, b, null);
      return ret(numQ(r.v), function () { return fill(T(L3("Els catets d'un triangle rectangle mesuren {a} cm i {b} cm. Quant mesura la hipotenusa?", "Los catetos de un triángulo rectángulo miden {a} cm y {b} cm. ¿Cuánto mide la hipotenusa?", "The legs of a right triangle are {a} cm and {b} cm. How long is the hypotenuse?")), { a: "$" + nf(a) + "$", b: "$" + nf(b) + "$" }) + rtFig(a, b, lab(a), lab(b), "?", "c"); },
        function () { return r.rows.join(""); });
    },
    cat: function () {
      var a, c; if (rint(0, 1)) { var t = triple(); a = t[rint(0, 1)]; c = t[2]; } else { c = rint(6, 20); a = rint(2, c - 1); }
      var r = pythSteps(a, null, c), b = r.v;
      return ret(numQ(b), function () { return fill(T(L3("La hipotenusa d'un triangle rectangle mesura {c} m i un catet, {a} m. Quant mesura l'altre catet?", "La hipotenusa de un triángulo rectángulo mide {c} m y un cateto, {a} m. ¿Cuánto mide el otro cateto?", "The hypotenuse of a right triangle is {c} m and one leg is {a} m. How long is the other leg?")), { a: "$" + nf(a) + "$", c: "$" + nf(c) + "$" }) + rtFig(a, b, lab(a), "?", lab(c), "b"); },
        function () { return r.rows.join(""); });
    },
    "class": function () {
      var s, k = rint(0, 2), C;
      do {
        if (k === 1) s = triple();
        else { s = [rint(2, 15), rint(2, 15), rint(2, 15)]; }
        C = classify(s);
      } while (!C.ok || C.k !== k || (k !== 1 && Math.abs(C.c * C.c - C.a * C.a - C.b * C.b) < 4));
      s = shuffle(s);
      var o = optsTxt(KIND[k], KIND.filter(function (_, i) { return i !== k; }));
      return ret({ opts: o.opts, ans: o.ans }, function () { return fill(T(L3("Com és, segons els angles, el triangle de costats {s}?", "¿Cómo es, según sus ángulos, el triángulo de lados {s}?", "What kind of triangle (by its angles) has sides {s}?")), { s: "$" + s.join(",\\ ") + "$" }); },
        function () { return C.row + " → <strong>" + T(KIND[k]) + "</strong>"; });
    },
    apl: function () {
      var kind = pick(["rect", "sq", "iso", "eq", "rom", "trap"]), F = APL[kind], v, bad;
      do {
        if (kind === "rect") v = [rint(3, 16), rint(2, 12)];
        else if (kind === "sq" || kind === "eq") v = [rint(2, 15)];
        else if (kind === "iso") v = [rint(5, 15), 2 * rint(2, 8)];
        else if (kind === "rom") v = [2 * rint(3, 10), 2 * rint(2, 8)];
        else v = [2 * rint(6, 12), 2 * rint(2, 5), rint(4, 12)];
        bad = F.bad && F.bad.apply(null, v);
      } while (bad);
      var r = F.f.apply(null, v), what = { rect: L3("la diagonal del rectangle", "la diagonal del rectángulo", "the rectangle's diagonal"), sq: L3("la diagonal del quadrat", "la diagonal del cuadrado", "the square's diagonal"), iso: L3("l'altura del triangle isòsceles", "la altura del triángulo isósceles", "the isosceles triangle's height"), eq: L3("l'altura del triangle equilàter", "la altura del triángulo equilátero", "the equilateral triangle's height"), rom: L3("el costat del rombe", "el lado del rombo", "the rhombus's side"), trap: L3("l'altura del trapezi isòsceles", "la altura del trapecio isósceles", "the isosceles trapezium's height") }[kind];
      return ret(numQ(r.v), function () { return fill(T(L3("Calcula {w} (mesures en cm).", "Calcula {w} (medidas en cm).", "Find {w} (lengths in cm).")), { w: T(what) }) + G(r.it, { W: 260, maxh: 170, pad: 46 }); }, function () { return r.rows.join(" "); });
    },
    dist: function () {
      var A = [rint(-6, 6), rint(-6, 6)], B; do { B = [rint(-6, 6), rint(-6, 6)]; } while (B[0] === A[0] || B[1] === A[1]);
      var d = Math.hypot(B[0] - A[0], B[1] - A[1]);
      return ret(numQ(d), function () { return fill(T(L3("Calcula la distància entre els punts {A} i {B}.", "Calcula la distancia entre los puntos {A} y {B}.", "Find the distance between the points {A} and {B}.")), { A: "$A(" + nf(A[0]) + ",\\," + nf(A[1]) + ")$", B: "$B(" + nf(B[0]) + ",\\," + nf(B[1]) + ")$" }); },
        function () { return distSteps(A, B) + cplot(A, B); });
    },
    area: function () {
      var kind = pick(["sq", "re", "ro", "rb", "tp", "tr"]), F = AREA[kind], v;
      if (kind === "sq") v = [rint(2, 15)]; else if (kind === "re") v = [rint(3, 16), rint(2, 12)]; else if (kind === "ro") { var h = rint(2, 8); v = [rint(4, 14), h, h + rint(1, 4)]; }
      else if (kind === "rb") v = [rint(4, 20), rint(2, 14)]; else if (kind === "tp") { var b = rint(2, 10); v = [b + rint(2, 10), b, rint(2, 10)]; } else v = [rint(3, 16), rint(2, 12)];
      var r = F.f.apply(null, v), name = { sq: L3("del quadrat", "del cuadrado", "of the square"), re: L3("del rectangle", "del rectángulo", "of the rectangle"), ro: L3("del romboide", "del romboide", "of the parallelogram"), rb: L3("del rombe", "del rombo", "of the rhombus"), tp: L3("del trapezi", "del trapecio", "of the trapezium"), tr: L3("del triangle", "del triángulo", "of the triangle") }[kind];
      return ret(numQ(r.a), function () { return fill(T(L3("Calcula l'àrea {n} (mesures en cm, resultat en cm²).", "Calcula el área {n} (medidas en cm, resultado en cm²).", "Find the area {n} (lengths in cm, answer in cm²).")), { n: T(name) }) + G(r.it, { W: 260, maxh: 160, pad: 46 }); }, function () { return r.A.join(" "); });
    },
    reg: function () {
      var t = rint(0, 2), n, l, a, r_;
      if (t === 0) { n = pick([5, 6, 8, 10]); l = rint(4, 12); a = Math.round(regData(n, l).a * 10) / 10; var A0 = n * l * a / 2;
        return ret(numQ(A0), function () { return fill(T(L3("Un {p} regular té {l} cm de costat i {a} cm d'apotema. Quina és la seua àrea (en cm²)?", "Un {p} regular tiene {l} cm de lado y {a} cm de apotema. ¿Cuál es su área (en cm²)?", "A regular {p} has {l} cm sides and a {a} cm apothem. What is its area (in cm²)?")), { p: T(PNAME[n]), l: "$" + nf(l) + "$", a: "$" + nf(a) + "$" }); },
          function () { return tex("P=" + n + "\\cdot" + nf(l) + "=" + nf(n * l) + "\\qquad A=\\dfrac{P\\cdot a}{2}=\\dfrac{" + nf(n * l) + "\\cdot" + nf(a) + "}{2}" + ap(A0)); }); }
      if (t === 1) { l = rint(2, 12); var a2 = l * l - l * l / 4, A1 = 6 * l * Math.sqrt(a2) / 2;
        return ret(numQ(A1), function () { return fill(T(L3("Calcula l'àrea d'un hexàgon regular de {l} cm de costat (en cm²).", "Calcula el área de un hexágono regular de {l} cm de lado (en cm²).", "Find the area of a regular hexagon with {l} cm sides (in cm²).")), { l: "$" + nf(l) + "$" }); },
          function () { return tex("r=l=" + nf(l) + "\\qquad a=\\sqrt{" + nf(l) + "^2-" + n4(l / 2) + "^2}" + ap(Math.sqrt(a2))) + "<br>" + tex("A=\\dfrac{" + nf(6 * l) + "\\cdot a}{2}" + ap(A1)); }); }
      n = pick([5, 7, 8, 9, 10]); l = rint(4, 12); r_ = Math.round(regData(n, l).r * 100) / 100; var a3 = Math.sqrt(r_ * r_ - l * l / 4);
      return ret(numQ(a3), function () { return fill(T(L3("Un {p} regular té {l} cm de costat i {r} cm de radi. Quant mesura l'apotema?", "Un {p} regular tiene {l} cm de lado y {r} cm de radio. ¿Cuánto mide la apotema?", "A regular {p} has {l} cm sides and a {r} cm radius. How long is its apothem?")), { p: T(PNAME[n]), l: "$" + nf(l) + "$", r: "$" + nf(r_) + "$" }); },
        function () { return tex("a=\\sqrt{r^2-\\left(\\tfrac l2\\right)^2}=\\sqrt{" + n4(r_ * r_) + "-" + n4(l * l / 4) + "}" + ap(a3)); });
    },
    circ: function () {
      var t = rint(0, 3), r = rint(2, 15), n = pick([30, 45, 60, 72, 90, 120, 135, 150, 210, 240, 270]);
      if (t === 0) return ret(numQ(2 * PI * r, true), function () { return fill(T(L3("Calcula la longitud d'una circumferència de {r} cm de radi.", "Calcula la longitud de una circunferencia de {r} cm de radio.", "Find the circumference of a circle with a {r} cm radius.")), { r: "$" + r + "$" }); }, function () { return tex("L=2\\pi\\cdot" + r + "=" + 2 * r + "\\pi\\approx " + d2(2 * PI * r)); });
      if (t === 1) return ret(numQ(PI * 2 * r, true), function () { return fill(T(L3("Una roda fa {d} cm de diàmetre. Quina distància recorre en una volta?", "Una rueda mide {d} cm de diámetro. ¿Qué distancia recorre en una vuelta?", "A wheel is {d} cm across. How far does it travel in one turn?")), { d: "$" + 2 * r + "$" }); }, function () { return tex("L=\\pi d=" + 2 * r + "\\pi\\approx " + d2(2 * PI * r)); });
      if (t === 2) { var La = 2 * PI * r * n / 360; return ret(numQ(La, true), function () { return fill(T(L3("Calcula la longitud d'un arc de {n} en una circumferència de {r} cm de radi.", "Calcula la longitud de un arco de {n} en una circunferencia de {r} cm de radio.", "Find the length of a {n} arc in a circle with a {r} cm radius.")), { n: "$" + n + "^\\circ$", r: "$" + r + "$" }); }, function () { return tex("L_{\\text{arc}}=\\dfrac{2\\pi\\cdot" + r + "\\cdot" + n + "}{360}\\approx " + d2(La)); }); }
      var L = Math.round(2 * PI * r * 100) / 100;
      return ret(numQ(L / (2 * PI)), function () { return fill(T(L3("Una circumferència fa {L} cm de longitud. Quant mesura el radi?", "Una circunferencia mide {L} cm de longitud. ¿Cuánto mide el radio?", "A circle has a circumference of {L} cm. How long is its radius?")), { L: "$" + d2(L) + "$" }); }, function () { return tex("2\\pi r=" + d2(L) + "\\Rightarrow r=\\dfrac{" + d2(L) + "}{2\\pi}\\approx " + d2(L / (2 * PI))); });
    },
    circa: function () {
      var t = rint(0, 3), R = rint(3, 15), r = rint(1, R - 1), n = pick([30, 45, 60, 90, 120, 135, 150, 240]), v;
      if (t === 0) { var d = rint(0, 1); v = PI * R * R; return ret(numQ(v, true), function () { return d ? fill(T(L3("Calcula l'àrea d'un cercle de {d} cm de diàmetre.", "Calcula el área de un círculo de {d} cm de diámetro.", "Find the area of a disc {d} cm across.")), { d: "$" + 2 * R + "$" }) : fill(T(L3("Calcula l'àrea d'un cercle de {r} cm de radi.", "Calcula el área de un círculo de {r} cm de radio.", "Find the area of a disc with a {r} cm radius.")), { r: "$" + R + "$" }); }, function () { return (d ? tex("r=" + R) + ". " : "") + tex("A=\\pi\\cdot" + R + "^2=" + R * R + "\\pi\\approx " + d2(v)); }); }
      if (t === 1) { v = PI * R * R * n / 360; return ret(numQ(v, true), function () { return fill(T(L3("Calcula l'àrea d'un sector circular de {n} i {r} cm de radi.", "Calcula el área de un sector circular de {n} y {r} cm de radio.", "Find the area of a {n} sector with a {r} cm radius.")), { n: "$" + n + "^\\circ$", r: "$" + R + "$" }); }, function () { return tex("A=\\dfrac{\\pi\\cdot" + R + "^2\\cdot" + n + "}{360}\\approx " + d2(v)); }); }
      if (t === 2) { v = PI * (R * R - r * r); return ret(numQ(v, true), function () { return fill(T(L3("Calcula l'àrea d'una corona circular de radis {R} cm i {r} cm.", "Calcula el área de una corona circular de radios {R} cm y {r} cm.", "Find the area of an annulus with radii {R} cm and {r} cm.")), { R: "$" + R + "$", r: "$" + r + "$" }); }, function () { return tex("A=\\pi\\left(" + R + "^2-" + r + "^2\\right)=" + (R * R - r * r) + "\\pi\\approx " + d2(v)); }); }
      v = PI * (R * R - r * r) * n / 360;
      return ret(numQ(v, true), function () { return fill(T(L3("Calcula l'àrea d'un trapezi circular de radis {R} cm i {r} cm i amplitud {n}.", "Calcula el área de un trapecio circular de radios {R} cm y {r} cm y amplitud {n}.", "Find the area of an annular sector with radii {R} cm and {r} cm and angle {n}.")), { R: "$" + R + "$", r: "$" + r + "$", n: "$" + n + "^\\circ$" }); }, function () { return tex("A=\\dfrac{\\pi\\left(" + R + "^2-" + r + "^2\\right)\\cdot" + n + "}{360}\\approx " + d2(v)); });
    },
    comp: function () {
      var mode = pick(["fin", "forat", "fulla", "cami"]), F = COMP[mode], v;
      if (mode === "fin") v = [2 * rint(1, 6), rint(2, 12)]; else if (mode === "forat" || mode === "fulla") v = [rint(2, 12)]; else v = [rint(6, 20), rint(4, 12), pick([0.5, 1, 1.5, 2])];
      var r = F.f.apply(null, v);
      return ret(numQ(r.A, true), function () { return T(L3("Calcula l'àrea de la zona ombrejada (mesures en m, resultat en m²).", "Calcula el área de la zona sombreada (medidas en m, resultado en m²).", "Find the shaded area (lengths in m, answer in m²).")) + (mode === "cami" ? " " + fill(T(L3("El camí fa {c} m d'amplària.", "El camino mide {c} m de ancho.", "The path is {c} m wide.")), { c: "$" + nf(v[2]) + "$" }) : "") + G(r.it, { W: 260, maxh: 170, pad: 46 }); },
        function () { return r.rows.slice(0, 2).join(" "); });
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
  window.FM9 = { G: G, classify: classify, pythSteps: pythSteps, APL: APL, AREA: AREA, CMODE: CMODE, COMP: COMP, regData: regData, GEN: GEN, numIn: numIn, pairIn: pairIn };

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

  var TITLES = { va: "Perímetres i àrees. Teorema de Pitàgores · FentMates", es: "Perímetros y áreas. Teorema de Pitágoras · FentMates", en: "Perimeters and areas. Pythagoras' theorem · FentMates" };
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
    wPit(); wProof(); wPcalc(); wClass(); wApl(); wDist(); wArea(); wReg(); wCirc(); wPizza(); wCirca(); wComp();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
