(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-u8-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt", pc: "si", rest: "en la resta",
      bad: "No entenc l'expressió: revisa-la.", notPoly: "Escriu un polinomi (per exemple, 3x^2-2x+1).", aBad: "Escriu nombres per a a i b, amb a < b.",
      condBad: "Per a la condició, escriu dos nombres: F(x₀) = y₀.", term: "Integrem terme a terme", prim: "Primitiva", cond: "Imposem la condició", sol: "Solució",
      fam: "Família de primitives", slope: "Pendent de la tangent en", same: "és el mateix per a totes les primitives:",
      chkOk: "Correcta! F′(x) = f(x) en tots els punts comprovats.", chkK: "Gairebé! F′(x) = k · f(x) amb k =", chkK2: "Has d'ajustar la constant: divideix F per", chkNo: "No és correcta: F′(x) ≠ f(x). Per exemple, en x =",
      chkNaN: "No he pogut comparar les funcions: revisa-les (o el domini).", left: "Esquerra", rightP: "Dreta", mid: "Punt mitjà",
      sum: "Suma de Riemann", exact: "Valor de la integral", err: "Diferència", width: "Amplària de cada rectangle",
      aPos: "Àrea per damunt de l'eix", aNeg: "Àrea per davall de l'eix", integ: "Integral", area: "Àrea", warn0: "Compte: f canvia de signe en [a, b], així que la integral no és l'àrea.",
      cuts: "Punts de tall", noCut: "no n'hi ha", inside: "Talls dins de l'interval", noneIn: "cap", pieces: "Integrals de cada tros", total: "Àrea total",
      noReg: "La corba no tanca cap recinte amb l'eix OX (necessita almenys dos talls). Escriu les rectes x = a i x = b.",
      noReg2: "Les corbes no tanquen cap recinte (necessiten almenys dos punts de tall). Escriu les rectes x = a i x = b.", same2: "Les dues funcions són iguals: no hi ha cap recinte.",
      both: "Escriu les dues rectes o cap.", indef: "Integral indefinida", def: "Integral definida (Barrow)", ax: "Àrea entre f i l'eix OX", btw: "Àrea entre f i g",
      pFam: ["2x", "3x² − 3", "x − 1", "4x³ − 4x"], pPoly: ["3x² − 4x + 5", "2x³ − x² + 4", "(x − 1)(x + 3)", "F(1) = 4", "f(2) = 5"],
      pChk: ["(2x+1)³ · A", "(2x+1)³ · B", "x(x²+1)⁴", "3x²/(x³+5)", "e³ˣ", "x·e^(x²)"], pRiem: ["x² en [0, 2]", "x/2 + 1 en [0, 4]", "4 − x² en [−2, 2]", "eˣ en [0, 1]"],
      pSign: ["x² − 1", "x³ − 4x", "x", "4 − x²"], pBar: ["2x + 1", "3x² − 4x + 1", "x² − 1", "3x² + 2x"],
      pA1: ["−x² + 4", "x² − 2x", "x³ − 4x", "x² + 1, [−1, 2]", "x² − 1, [0, 2]", "x² − 4x + 3, [0, 4]"],
      pA2: ["x² i x + 2", "x² − 4x i −x² + 2x", "x³ i x", "x² + 2 i x, [0, 2]", "x² i 2x, [1, 3]"],
      pLab: ["Integral indefinida", "Barrow i àrea", "Recinte amb OX", "Dues corbes", "Dues corbes, [0, 2]"] },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba", pc: "si", rest: "en el resto",
      bad: "No entiendo la expresión: revísala.", notPoly: "Escribe un polinomio (por ejemplo, 3x^2-2x+1).", aBad: "Escribe números para a y b, con a < b.",
      condBad: "Para la condición, escribe dos números: F(x₀) = y₀.", term: "Integramos término a término", prim: "Primitiva", cond: "Imponemos la condición", sol: "Solución",
      fam: "Familia de primitivas", slope: "Pendiente de la tangente en", same: "es la misma para todas las primitivas:",
      chkOk: "¡Correcta! F′(x) = f(x) en todos los puntos comprobados.", chkK: "¡Casi! F′(x) = k · f(x) con k =", chkK2: "Tienes que ajustar la constante: divide F entre", chkNo: "No es correcta: F′(x) ≠ f(x). Por ejemplo, en x =",
      chkNaN: "No he podido comparar las funciones: revísalas (o el dominio).", left: "Izquierda", rightP: "Derecha", mid: "Punto medio",
      sum: "Suma de Riemann", exact: "Valor de la integral", err: "Diferencia", width: "Anchura de cada rectángulo",
      aPos: "Área por encima del eje", aNeg: "Área por debajo del eje", integ: "Integral", area: "Área", warn0: "Cuidado: f cambia de signo en [a, b], así que la integral no es el área.",
      cuts: "Puntos de corte", noCut: "no hay", inside: "Cortes dentro del intervalo", noneIn: "ninguno", pieces: "Integrales de cada trozo", total: "Área total",
      noReg: "La curva no encierra ningún recinto con el eje OX (necesita al menos dos cortes). Escribe las rectas x = a y x = b.",
      noReg2: "Las curvas no encierran ningún recinto (necesitan al menos dos puntos de corte). Escribe las rectas x = a y x = b.", same2: "Las dos funciones son iguales: no hay ningún recinto.",
      both: "Escribe las dos rectas o ninguna.", indef: "Integral indefinida", def: "Integral definida (Barrow)", ax: "Área entre f y el eje OX", btw: "Área entre f y g",
      pFam: ["2x", "3x² − 3", "x − 1", "4x³ − 4x"], pPoly: ["3x² − 4x + 5", "2x³ − x² + 4", "(x − 1)(x + 3)", "F(1) = 4", "f(2) = 5"],
      pChk: ["(2x+1)³ · A", "(2x+1)³ · B", "x(x²+1)⁴", "3x²/(x³+5)", "e³ˣ", "x·e^(x²)"], pRiem: ["x² en [0, 2]", "x/2 + 1 en [0, 4]", "4 − x² en [−2, 2]", "eˣ en [0, 1]"],
      pSign: ["x² − 1", "x³ − 4x", "x", "4 − x²"], pBar: ["2x + 1", "3x² − 4x + 1", "x² − 1", "3x² + 2x"],
      pA1: ["−x² + 4", "x² − 2x", "x³ − 4x", "x² + 1, [−1, 2]", "x² − 1, [0, 2]", "x² − 4x + 3, [0, 4]"],
      pA2: ["x² y x + 2", "x² − 4x y −x² + 2x", "x³ y x", "x² + 2 y x, [0, 2]", "x² y 2x, [1, 3]"],
      pLab: ["Integral indefinida", "Barrow y área", "Recinto con OX", "Dos curvas", "Dos curvas, [0, 2]"] },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top", pc: "if", rest: "otherwise",
      bad: "I can't read that expression: check it.", notPoly: "Type a polynomial (for example, 3x^2-2x+1).", aBad: "Type numbers for a and b, with a < b.",
      condBad: "For the condition, type two numbers: F(x₀) = y₀.", term: "Integrate term by term", prim: "Antiderivative", cond: "Apply the condition", sol: "Answer",
      fam: "Family of antiderivatives", slope: "Slope of the tangent at", same: "is the same for every antiderivative:",
      chkOk: "Correct! F′(x) = f(x) at every point checked.", chkK: "Almost! F′(x) = k · f(x) with k =", chkK2: "Adjust the constant: divide F by", chkNo: "Not correct: F′(x) ≠ f(x). For example, at x =",
      chkNaN: "I couldn't compare the functions: check them (or the domain).", left: "Left", rightP: "Right", mid: "Midpoint",
      sum: "Riemann sum", exact: "Value of the integral", err: "Difference", width: "Width of each rectangle",
      aPos: "Area above the axis", aNeg: "Area below the axis", integ: "Integral", area: "Area", warn0: "Careful: f changes sign on [a, b], so the integral is not the area.",
      cuts: "Intersection points", noCut: "none", inside: "Roots inside the interval", noneIn: "none", pieces: "Integral over each piece", total: "Total area",
      noReg: "The curve does not enclose any region with the x-axis (it needs at least two roots). Type the lines x = a and x = b.",
      noReg2: "The curves do not enclose any region (they need at least two intersection points). Type the lines x = a and x = b.", same2: "Both functions are equal: there is no region.",
      both: "Type both lines or neither.", indef: "Indefinite integral", def: "Definite integral (Barrow)", ax: "Area between f and the x-axis", btw: "Area between f and g",
      pFam: ["2x", "3x² − 3", "x − 1", "4x³ − 4x"], pPoly: ["3x² − 4x + 5", "2x³ − x² + 4", "(x − 1)(x + 3)", "F(1) = 4", "f(2) = 5"],
      pChk: ["(2x+1)³ · A", "(2x+1)³ · B", "x(x²+1)⁴", "3x²/(x³+5)", "e³ˣ", "x·e^(x²)"], pRiem: ["x² on [0, 2]", "x/2 + 1 on [0, 4]", "4 − x² on [−2, 2]", "eˣ on [0, 1]"],
      pSign: ["x² − 1", "x³ − 4x", "x", "4 − x²"], pBar: ["2x + 1", "3x² − 4x + 1", "x² − 1", "3x² + 2x"],
      pA1: ["−x² + 4", "x² − 2x", "x³ − 4x", "x² + 1, [−1, 2]", "x² − 1, [0, 2]", "x² − 4x + 3, [0, 4]"],
      pA2: ["x² and x + 2", "x² − 4x and −x² + 2x", "x³ and x", "x² + 2 and x, [0, 2]", "x² and 2x, [1, 3]"],
      pLab: ["Indefinite integral", "Barrow and area", "Region with x-axis", "Two curves", "Two curves, [0, 2]"] }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }

  /*@@CORE@@*/
  /* ---------- nombres, arrels i integrals numèriques ---------- */
  function F(s) { return compile(parse(s)); }
  function sgn(v) { return v > 0 ? 1 : v < 0 ? -1 : 0; }
  function snap(x) { if (Math.abs(x) < 1e-9) return 0; var q = fracOf(x, 12); return q ? q.n / q.d : x; }
  // valor exacte si és senzill; si no, arrodonit
  function nn(v) { var s = niceTex(v); return s.indexOf("\\approx") === 0 ? numTex(+v.toFixed(4)) : s; }
  function roots(g, x0, x1, N) {
    N = N || 4000;
    var h = (x1 - x0) / N, xs = [], gs = [], out = [], i, it, m;
    for (i = 0; i <= N; i++) { xs.push(x0 + i * h); gs.push(g(xs[i])); }
    function push(r) {
      if (!(r >= x0 - 1e-12 && r <= x1 + 1e-12) || !isFinite(g(r))) return;
      r = snap(r);
      for (var k = 0; k < out.length; k++) if (Math.abs(out[k] - r) < 1e-6 * (1 + Math.abs(r))) return;
      out.push(r);
    }
    for (i = 0; i < N; i++) {
      var a = gs[i], b = gs[i + 1];
      if (!isFinite(a) || !isFinite(b)) continue;
      if (a === 0) { push(xs[i]); continue; }
      if (a * b < 0) {
        var p = xs[i], q = xs[i + 1], gp = a;
        for (it = 0; it < 80; it++) { m = (p + q) / 2; var gm = g(m); if (!isFinite(gm)) break; if (sgn(gm) === sgn(gp)) { p = m; gp = gm; } else q = m; }
        var r = (p + q) / 2;
        if (Math.abs(g(r)) < 1e-6 * (1 + Math.abs(a) + Math.abs(b))) push(r);
      } else if (i > 0 && isFinite(gs[i - 1]) && a * gs[i - 1] > 0 && Math.abs(a) <= Math.abs(gs[i - 1]) && Math.abs(a) <= Math.abs(b)) {
        // arrel doble (sense canvi de signe): mínim local de |g|
        var lo = xs[i - 1], hi = xs[i + 1];
        for (it = 0; it < 100; it++) { var m1 = lo + (hi - lo) / 3, m2 = hi - (hi - lo) / 3; if (Math.abs(g(m1)) < Math.abs(g(m2))) hi = m2; else lo = m1; }
        var rr = (lo + hi) / 2;
        if (Math.abs(g(rr)) < 1e-9) push(rr);
      }
    }
    return out.sort(function (p, q) { return p - q; });
  }
  // regla de Simpson
  function simpson(f, a, b, N) {
    N = N || 600; if (N % 2) N++;
    var h = (b - a) / N, s = f(a) + f(b);
    for (var i = 1; i < N; i++) s += (i % 2 ? 4 : 2) * f(a + i * h);
    return s * h / 3;
  }

  /* ---------- polinomis: primitiva i valors exactes ---------- */
  function polyOrNull(src) { try { return pTrim(polyOf(parse(src))); } catch (e) { return null; } }
  function pInt(p) { var r = [new Fr(0)]; p.forEach(function (c, k) { r.push(c.div(new Fr(k + 1))); }); return pTrim(r); }
  function pNum(p, x) { var r = 0; for (var i = p.length - 1; i >= 0; i--) r = r * x + p[i].val(); return r; }
  function pFn(p) { return function (x) { return pNum(p, x); }; }
  function frAbs(q) { return new Fr(Math.abs(q.n), q.d); }
  // tex d'un polinomi amb les fraccions «a dalt»: x^3/3 en lloc de 1/3 x^3
  function pTexI(p) {
    var s = "", first = true;
    for (var k = p.length - 1; k >= 0; k--) {
      var c = p[k]; if (c.zero()) continue;
      var neg = c.n < 0, n = Math.abs(c.n), xs = k === 0 ? "" : k === 1 ? "x" : "x^{" + k + "}", t;
      if (k === 0) t = c.d === 1 ? String(n) : "\\frac{" + n + "}{" + c.d + "}";
      else if (c.d === 1) t = (n === 1 ? "" : n) + xs;
      else t = "\\frac{" + (n === 1 ? "" : n) + xs + "}{" + c.d + "}";
      s += (neg ? "-" : first ? "" : "+") + t; first = false;
    }
    return s || "0";
  }
  // tex d'un nombre (Fr o decimal) entre parèntesis si és negatiu
  function par(t, neg) { return neg ? "\\left(" + t + "\\right)" : t; }
  // un punt: {q: Fr exacte o null, v: valor numèric}
  function P(q, v) { return q ? { q: q, v: q.val() } : { q: null, v: v }; }
  function ptT(o) { return o.q ? o.q.tex() : "\\approx" + numTex(+o.v.toFixed(3)); }
  function valT(o) { return o.q ? o.q.tex() : "\\approx" + numTex(+o.v.toFixed(4)); }
  // arrels d'un polinomi en [lo, hi]: exactes si són racionals senzilles
  function pRoots(p, lo, hi) {
    if (pDeg(p) < 1) return [];
    return roots(pFn(p), lo, hi, 6000).map(function (r) {
      var q = fracOf(r, 60);
      return q && pEval(p, q).zero() ? P(q) : P(null, r);
    });
  }
  // valor de H en un punt (exacte si es pot)
  function hAt(H, o) { return o.q ? P(pEval(H, o.q)) : P(null, pNum(H, o.v)); }
  function hDiff(B, A) { return B.q && A.q ? P(B.q.sub(A.q)) : P(null, B.v - A.v); }
  function parseLim(s) { s = String(s).trim(); if (!s) return null; var q = parseFr(s); return q ? q : undefined; }

  /* ---------- figures estàtiques ---------- */
  var FIGS = {
    fam: function () {
      var cs = [-2, 0, 2], cols = ["var(--r3)", "var(--accent)", "var(--plus)"], curves = [], pts = [];
      cs.forEach(function (c, i) { curves.push({ f: F("x^2+" + c), col: cols[i] }); curves.push({ f: lineF(2, 1, 1 + c), a: 0.3, b: 1.7, col: "var(--accent-2)" }); pts.push({ x: 1, y: 1 + c, col: cols[i] }); });
      return { v: [-2.5, 2.5, -3, 6.5], curves: curves, pts: pts, guides: [{ x: 1 }],
        labels: [{ x: -2.2, y: 5.6, t: "x² + 2", anchor: "start" }, { x: -2.2, y: 3.9, t: "x²", anchor: "start" }, { x: -2.2, y: 1.7, t: "x² − 2", anchor: "start" }, { x: 1.15, y: -2.6, t: t3("mateix pendent", "misma pendiente", "same slope"), anchor: "start" }] };
    },
    riem: function () {
      var f = F("x^2/2+1"), n = 6, h = 4 / n, rects = [];
      for (var i = 0; i < n; i++) rects.push({ a: i * h, b: (i + 1) * h, y: f((i + 0.5) * h) });
      return { v: [-0.6, 4.6, -0.8, 10], curves: [{ f: f }], rects: rects, guides: [{ x: 0 }, { x: 4 }],
        labels: [{ x: 0, y: -0.5, t: "a" }, { x: 4, y: -0.5, t: "b" }, { x: 1.2, y: 6.5, t: "y = f(x)" }] };
    },
    sign: function () {
      var f = F("(x^3-4x)/2");
      return { v: [-2.6, 2.8, -2.2, 2.2], curves: [{ f: f }], fill: [{ f: f, a: -2, b: 0, col: "var(--ok)" }, { f: f, a: 0, b: 2.4, col: "var(--bad)" }],
        labels: [{ x: -1.15, y: 0.6, t: "A₊" }, { x: 1.15, y: -0.75, t: "A₋" }, { x: 0.05, y: 1.75, t: "∫ = A₊ − A₋", anchor: "start" }] };
    },
    cPos: function () { var f = F("x^2/4+1"); return { v: [-0.5, 4.5, -0.6, 6], curves: [{ f: f }], fill: [{ f: f, a: 1, b: 4, col: "var(--ok)" }], guides: [{ x: 1 }, { x: 4 }], labels: [{ x: 1, y: -0.4, t: "a" }, { x: 4, y: -0.4, t: "b" }] }; },
    cNeg: function () { var f = F("-x^2/4-1"); return { v: [-0.5, 4.5, -6, 0.6], curves: [{ f: f }], fill: [{ f: f, a: 1, b: 4, col: "var(--bad)" }], guides: [{ x: 1 }, { x: 4 }], labels: [{ x: 1, y: 0.25, t: "a" }, { x: 4, y: 0.25, t: "b" }] }; },
    cMix: function () { var f = F("x^2-1"); return { v: [-0.5, 2.5, -1.6, 3.4], curves: [{ f: f }], fill: [{ f: f, a: 0, b: 1, col: "var(--bad)" }, { f: f, a: 1, b: 2, col: "var(--ok)" }], guides: [{ x: 2 }], labels: [{ x: -0.15, y: -0.3, t: "a" }, { x: 2, y: -0.3, t: "b" }, { x: 1, y: -0.3, t: "c" }] }; },
    cEnc: function () { var f = F("-x^2+4"); return { v: [-3, 3, -1.5, 5], curves: [{ f: f }], fill: [{ f: f, a: -2, b: 2, col: "var(--ok)" }], pts: [{ x: -2, y: 0 }, { x: 2, y: 0 }] }; },
    two: function () {
      var f = F("x+2"), g = F("x^2");
      return { v: [-2, 3, -1, 5.5], curves: [{ f: f }, { f: g, col: "var(--r3)" }], fill: [{ f: f, g: g, a: -1, b: 2, col: "var(--accent-2)" }], pts: [{ x: -1, y: 1 }, { x: 2, y: 4 }],
        labels: [{ x: 2.4, y: 5.1, t: "f", anchor: "start" }, { x: 1.6, y: 1.6, t: "g", anchor: "start" }, { x: 0.5, y: 1.4, t: "A = ∫(f − g)" }] };
    },
    twoAB: function () {
      var f = F("x^2"), g = F("2x");
      return { v: [-0.5, 3.5, -0.8, 9.5], curves: [{ f: f }, { f: g, col: "var(--r3)" }], fill: [{ f: g, g: f, a: 1, b: 2, col: "var(--accent-2)" }, { f: f, g: g, a: 2, b: 3, col: "var(--accent-2)" }], guides: [{ x: 1 }, { x: 3 }],
        pts: [{ x: 2, y: 4 }], labels: [{ x: 3.1, y: 8.6, t: "y = x²", anchor: "end" }, { x: 3.3, y: 5.4, t: "y = 2x", anchor: "end" }, { x: 1, y: -0.5, t: "x = 1" }, { x: 3, y: -0.5, t: "x = 3" }] };
    }
  };
  function wFigs() {
    document.querySelectorAll("[data-g]").forEach(function (el) {
      var mk = FIGS[el.getAttribute("data-g")]; if (!mk) return;
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "lp-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Gràfica");
      el.appendChild(svg);
      onLang(function () { plot(svg, mk()); });
    });
  }
  function lineF(m, a, fa) { return function (x) { return fa + m * (x - a); }; }
  function presetBtns(box, n, key, onPick) {
    var bs = [];
    for (var i = 0; i < n; i++) (function (i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { onPick(i); }); box.appendChild(b); bs.push(b);
    })(i);
    onLang(function () { bs.forEach(function (b, i) { b.textContent = u(key)[i]; }); });
  }

  /* ---------- widget: família de primitives ---------- */
  function wFam() {
    var w = document.getElementById("w-fam"); if (!w) return;
    var PRE = ["2x", "3x^2-3", "x-1", "4x^3-4x"];
    var fi = $(w, "f"), rc = $(w, "c"), rx = $(w, "x"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    rc.min = -4; rc.max = 4; rc.step = 0.5; rc.value = 0; rx.min = -2; rx.max = 2; rx.step = 0.1; rx.value = 1;
    presetBtns($(w, "presets"), PRE.length, "pFam", function (i) { fi.value = PRE[i]; rc.value = 0; draw(); });
    [fi, rc, rx].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var p = polyOrNull(fi.value), c = +rc.value, x = +rx.value;
      $(w, "cv").textContent = numTxt(c); $(w, "xv").textContent = numTxt(x);
      if (!p) { fi.classList.add("bad"); info.textContent = u("notPoly"); return; }
      fi.classList.remove("bad");
      var Pp = pInt(p), Fx = pFn(Pp), m = pNum(p, x), curves = [], pts = [], k;
      var yy = autoY([function (t) { return Fx(t) - 4; }, function (t) { return Fx(t) + 4; }], -2.5, 2.5, 0.05);
      var v = [-2.5, 2.5, Math.max(yy[0], -12), Math.min(yy[1], 14)], hw = 0.45;
      for (k = -4; k <= 4; k += 2) if (Math.abs(k - c) > 1e-9) curves.push({ f: (function (k) { return function (t) { return Fx(t) + k; }; })(k), col: "var(--border)" });
      curves.push({ f: function (t) { return Fx(t) + c; }, col: "var(--accent)" });
      for (k = -4; k <= 4; k += 2) { curves.push({ f: lineF(m, x, Fx(x) + k), a: x - hw, b: x + hw, col: "var(--accent-2)" }); }
      if ([-4, -2, 0, 2, 4].indexOf(c) < 0) curves.push({ f: lineF(m, x, Fx(x) + c), a: x - hw, b: x + hw, col: "var(--accent-2)" });
      pts.push({ x: x, y: Fx(x) + c });
      var h = "<p>" + tex("f(x)=" + pTex(p)) + "</p>";
      h += "<p>" + u("fam") + ": " + tex("\\displaystyle\\int f(x)\\,dx=" + pTexI(Pp) + "+C") + "</p>";
      h += "<p>" + tex("C=" + numTex(c) + ":\\quad F(x)=" + pTexI(c === 0 ? Pp : pAdd(Pp, [decFr(String(c))], 1))) + "</p>";
      h += "<p>" + u("slope") + " " + tex("x=" + numTex(+x.toFixed(2))) + " " + u("same") + " " + tex("f(" + numTex(+x.toFixed(2)) + ")=" + numTex(+m.toFixed(4))) + "</p>";
      info.innerHTML = h;
      plot(svg, { v: v, curves: curves, pts: pts, guides: [{ x: x }] });
    }
    onLang(draw);
  }

  /* ---------- widget: integrador de polinomis ---------- */
  function wPoly() {
    var w = document.getElementById("w-poly"); if (!w) return;
    var PRE = [["3x^2-4x+5", "", ""], ["2x^3-x^2+4", "", ""], ["(x-1)(x+3)", "", ""], ["3x^2-2x+1", "1", "4"], ["6x-4", "2", "5"]];
    var fi = $(w, "f"), xi = $(w, "x0"), yi = $(w, "y0"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pPoly", function (i) { fi.value = PRE[i][0]; xi.value = PRE[i][1]; yi.value = PRE[i][2]; draw(); });
    [fi, xi, yi].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var p = polyOrNull(fi.value);
      if (!p) { fi.classList.add("bad"); info.textContent = u("notPoly"); return; }
      fi.classList.remove("bad");
      var Pp = pInt(p), h = "<p>" + tex("f(x)=" + pTex(p)) + "</p><p><strong>" + u("term") + ":</strong></p><ul class=\"int-steps\">";
      for (var k = p.length - 1; k >= 0; k--) {
        var c = p[k]; if (c.zero()) continue;
        var mono = []; for (var j = 0; j < k; j++) mono.push(new Fr(0)); mono.push(c);  // c·x^k
        var step = k === 0 ? "\\int " + par(c.tex(), c.n < 0) + "\\,dx=" + pTexI(pInt(mono)) :
          "\\int " + pTex(mono) + "\\,dx=" + (c.n === 1 && c.d === 1 ? "" : par(c.tex(), c.n < 0) + "\\cdot") + "\\frac{x^{" + (k + 1) + "}}{" + (k + 1) + "}=" + pTexI(pInt(mono));
        h += "<li>" + tex(step) + "</li>";
      }
      h += "</ul><p>" + tex("\\displaystyle\\int\\left(" + pTex(p) + "\\right)dx=" + pTexI(Pp) + "+C") + "</p>";
      var x0 = parseLim(xi.value), y0 = parseLim(yi.value), Fin = Pp;
      var cond = x0 !== null || y0 !== null;
      xi.classList.toggle("bad", cond && !x0); yi.classList.toggle("bad", cond && !y0);
      if (cond && (!x0 || !y0)) h += '<p class="msg-bad">' + u("condBad") + "</p>";
      else if (cond) {
        var Fx0 = pEval(Pp, x0), C = y0.sub(Fx0);
        Fin = pAdd(Pp, [C], 1);
        h += "<p><strong>" + u("cond") + ":</strong> " + tex("F(" + x0.tex() + ")=" + y0.tex()) + "</p>";
        h += "<p>" + tex(Fx0.tex() + "+C=" + y0.tex() + "\\ \\Rightarrow\\ C=" + C.tex()) + "</p>";
        h += '<p class="msg-ok">' + u("sol") + ": " + tex("F(x)=" + pTexI(Fin)) + "</p>";
      }
      info.innerHTML = h;
      var f = pFn(p), Fn = pFn(Fin), xa = cond && x0 ? x0.val() : 0;
      var v0 = Math.min(-3, xa - 3), v1 = Math.max(3, xa + 3), yy = autoY([f, Fn], v0, v1);
      plot(svg, { v: [v0, v1, yy[0], yy[1]], curves: [{ f: f, col: "var(--muted)" }, { f: Fn, col: "var(--accent)" }], pts: cond && x0 && y0 ? [{ x: x0.val(), y: y0.val() }] : [] });
    }
    onLang(draw);
  }

  /* ---------- widget: comprova la primitiva ---------- */
  function wChk() {
    var w = document.getElementById("w-chk"); if (!w) return;
    var PRE = [["(2x+1)^3", "(2x+1)^4/8"], ["(2x+1)^3", "(2x+1)^4/4"], ["x(x^2+1)^4", "(x^2+1)^5/10"], ["3x^2/(x^3+5)", "ln(x^3+5)"], ["e^(3x)", "e^(3x)"], ["x*e^(x^2)", "e^(x^2)/2"]];
    var fi = $(w, "f"), Fi = $(w, "F"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pChk", function (i) { fi.value = PRE[i][0]; Fi.value = PRE[i][1]; draw(); });
    [fi, Fi].forEach(function (el) { el.addEventListener("input", draw); });
    function dF(G, x) { var h = 1e-5 * Math.max(1, Math.abs(x)); return (G(x + h) - G(x - h)) / (2 * h); }
    function draw() {
      var fn, Fn, nf, nF;
      try { nf = parse(fi.value); fn = compile(nf); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
      try { nF = parse(Fi.value); Fn = compile(nF); Fi.classList.remove("bad"); } catch (e) { Fi.classList.add("bad"); info.textContent = u("bad"); return; }
      var xs = [], i;
      for (i = 0; i <= 60; i++) { var x = -2.95 + 5.9 * i / 60; if (isFinite(fn(x)) && isFinite(Fn(x)) && isFinite(dF(Fn, x)) && Math.abs(fn(x)) < 1e7) xs.push(x); }
      var h = "<p>" + tex("f(x)=" + texA(strip(nf))) + "</p><p>" + tex("F(x)=" + texA(strip(nF))) + "</p>";
      if (xs.length < 8) { info.innerHTML = h + "<p>" + u("chkNaN") + "</p>"; plot(svg, { v: [-3, 3, -5, 5], curves: [{ f: fn }] }); return; }
      var bad = null, ks = [];
      xs.forEach(function (x) {
        var a = dF(Fn, x), b = fn(x);
        if (bad === null && Math.abs(a - b) > 1e-4 * (1 + Math.abs(b))) bad = x;
        if (Math.abs(b) > 1e-3) ks.push(a / b);
      });
      if (bad === null) h += '<p><span class="chk ok">✓ ' + u("chkOk") + "</span></p>";
      else {
        var k0 = ks.length ? ks[0] : NaN, cst = ks.length > 4 && ks.every(function (k) { return Math.abs(k - k0) < 1e-4 * (1 + Math.abs(k0)); });
        if (cst && Math.abs(k0) > 1e-6) h += '<p><span class="chk no">' + u("chkK") + " " + numTxt(snap(k0)) + "</span></p><p>" + u("chkK2") + " " + tex(nn(k0)) + ".</p>";
        else h += '<p><span class="chk no">✗ ' + u("chkNo") + " " + numTxt(+bad.toFixed(2)) + "</span></p><p>" + tex("F'(" + numTex(+bad.toFixed(2)) + ")\\approx" + numTex(+dF(Fn, bad).toFixed(4)) + ",\\quad f(" + numTex(+bad.toFixed(2)) + ")=" + numTex(+fn(bad).toFixed(4))) + "</p>";
      }
      info.innerHTML = h;
      var yy = autoY([fn], -3, 3);
      plot(svg, { v: [-3, 3, yy[0], yy[1]], curves: [{ f: fn, col: "var(--accent)" }, { f: function (x) { return dF(Fn, x); }, col: "var(--accent-2)" }] });
    }
    onLang(draw);
  }

  /* ---------- widget: sumes de Riemann ---------- */
  function wRiem() {
    var w = document.getElementById("w-riem"); if (!w) return;
    var PRE = [["x^2", "0", "2"], ["x/2+1", "0", "4"], ["4-x^2", "-2", "2"], ["e^x", "0", "1"]];
    var fi = $(w, "f"), ai = $(w, "a"), bi = $(w, "b"), rn = $(w, "n"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info"), mode = 0, mb = [];
    var box = $(w, "mode");
    ["left", "mid", "rightP"].forEach(function (k, i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { mode = i; draw(); }); box.appendChild(b); mb.push([b, k]);
    });
    presetBtns($(w, "presets"), PRE.length, "pRiem", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; bi.value = PRE[i][2]; draw(); });
    [fi, ai, bi, rn].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      mb.forEach(function (q, i) { q[0].textContent = u(q[1]); q[0].classList.toggle("on", i === mode); });
      var n = +rn.value, f, nf; $(w, "nv").textContent = n;
      try { nf = parse(fi.value); f = compile(nf); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
      var A = parseFr(ai.value), B = parseFr(bi.value), ok = A && B && A.val() < B.val();
      ai.classList.toggle("bad", !ok); bi.classList.toggle("bad", !ok);
      if (!ok) { info.textContent = u("aBad"); return; }
      var a = A.val(), b = B.val(), dx = (b - a) / n, S = 0, rects = [];
      for (var i = 0; i < n; i++) {
        var xi = a + (i + [0, 0.5, 1][mode]) * dx, y = f(xi);
        S += y * dx; rects.push({ a: a + i * dx, b: a + (i + 1) * dx, y: y, col: y >= 0 ? "var(--accent-2)" : "var(--bad)" });
      }
      var p = polyOrNull(fi.value), I, It;
      if (p) { var H = pInt(p), q = pEval(H, B).sub(pEval(H, A)); I = q.val(); It = q.tex() + (q.d === 1 ? "" : "\\approx" + numTex(+I.toFixed(5))); }
      else { I = simpson(f, a, b, 2000); It = nn(I); if (It.indexOf("\\approx") < 0 && !/^-?\d+$/.test(It)) It += "\\approx" + numTex(+I.toFixed(5)); }
      var h = "<p>" + tex("f(x)=" + texA(strip(nf))) + ", " + tex("[" + A.tex() + "," + B.tex() + "]") + "</p>";
      h += "<p>" + u("width") + ": " + tex("\\Delta x=\\frac{" + nn(b - a) + "}{" + n + "}=" + numTex(+dx.toFixed(4))) + "</p>";
      h += '<p class="sum-big">' + u("sum") + ": " + tex("S_{" + n + "}=" + numTex(+S.toFixed(5))) + "</p>";
      h += "<p>" + u("exact") + ": " + tex("\\displaystyle\\int_{" + A.tex() + "}^{" + B.tex() + "}f(x)\\,dx=" + It) + "</p>";
      h += "<p>" + u("err") + ": " + tex("|S_{" + n + "}-I|=" + numTex(+Math.abs(S - I).toFixed(5))) + "</p>";
      info.innerHTML = h;
      var pad = (b - a) * 0.12, yy = autoY([f], a - pad, b + pad);
      plot(svg, { v: [a - pad, b + pad, yy[0], yy[1]], curves: [{ f: f }], rects: rects, guides: [{ x: a }, { x: b }] });
    }
    onLang(draw);
  }

  /* ---------- trossos amb signe (numèricament) ---------- */
  function signPieces(f, a, b) {
    var rs = roots(f, a, b, 3000).filter(function (r) { return r > a + 1e-9 && r < b - 1e-9; }), cuts = [a].concat(rs).concat([b]), out = [];
    for (var i = 0; i + 1 < cuts.length; i++) out.push({ a: cuts[i], b: cuts[i + 1], v: simpson(f, cuts[i], cuts[i + 1], 400) });
    return out;
  }

  /* ---------- widget: integral i àrea ---------- */
  function wSign() {
    var w = document.getElementById("w-sign"); if (!w) return;
    var PRE = [["x^2-1", -1.5, 2], ["x^3-4x", -2, 2], ["x", -2, 2], ["4-x^2", -3, 1]];
    var fi = $(w, "f"), ra = $(w, "a"), rb = $(w, "b"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pSign", function (i) { fi.value = PRE[i][0]; ra.value = PRE[i][1]; rb.value = PRE[i][2]; draw(); });
    [fi, ra, rb].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var a = +ra.value, b = +rb.value, f, nf;
      $(w, "av").textContent = numTxt(a); $(w, "bv").textContent = numTxt(b);
      try { nf = parse(fi.value); f = compile(nf); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
      var h = "<p>" + tex("f(x)=" + texA(strip(nf))) + "</p>", fill = [];
      if (!(b > a)) { info.innerHTML = h + "<p>" + u("aBad") + "</p>"; plot(svg, { v: [-4, 4, -5, 5], curves: [{ f: f }], guides: [{ x: a }, { x: b }] }); return; }
      var pcs = signPieces(f, a, b), Ap = 0, An = 0;
      pcs.forEach(function (q) { if (q.v >= 0) Ap += q.v; else An -= q.v; fill.push({ f: f, a: q.a, b: q.b, col: q.v >= 0 ? "var(--ok)" : "var(--bad)" }); });
      h += "<p>" + u("aPos") + ": " + tex("A_{+}=" + nn(Ap)) + "<br>" + u("aNeg") + ": " + tex("A_{-}=" + nn(An)) + "</p>";
      h += '<p class="sum-big">' + u("integ") + ": " + tex("\\displaystyle\\int_{" + numTex(a) + "}^{" + numTex(b) + "}f(x)\\,dx=A_{+}-A_{-}=" + nn(Ap - An)) + "</p>";
      h += '<p class="sum-big">' + u("area") + ": " + tex("A=A_{+}+A_{-}=" + nn(Ap + An)) + "</p>";
      if (Ap > 1e-6 && An > 1e-6) h += '<p class="msg-bad">' + u("warn0") + "</p>";
      info.innerHTML = h;
      var yy = autoY([f], -4, 4);
      plot(svg, { v: [-4, 4, yy[0], yy[1]], curves: [{ f: f }], fill: fill, guides: [{ x: a }, { x: b }] });
    }
    onLang(draw);
  }

  /* ---------- widget: regla de Barrow ---------- */
  function wBarrow() {
    var w = document.getElementById("w-barrow"); if (!w) return;
    var PRE = [["2x+1", "1", "3"], ["3x^2-4x+1", "0", "2"], ["x^2-1", "-1", "2"], ["3x^2+2x", "0", "2"]];
    var fi = $(w, "f"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pBar", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; bi.value = PRE[i][2]; draw(); });
    [fi, ai, bi].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var p = polyOrNull(fi.value);
      if (!p) { fi.classList.add("bad"); info.textContent = u("notPoly"); return; }
      fi.classList.remove("bad");
      var A = parseFr(ai.value), B = parseFr(bi.value), ok = A && B && A.val() !== B.val();
      ai.classList.toggle("bad", !ok); bi.classList.toggle("bad", !ok);
      if (!ok) { info.textContent = u("aBad"); return; }
      var H = pInt(p), FA = pEval(H, A), FB = pEval(H, B), I = FB.sub(FA), at = A.tex(), bt = B.tex();
      var h = "<p>" + tex("\\displaystyle\\int_{" + at + "}^{" + bt + "}\\left(" + pTex(p) + "\\right)dx") + "</p><ol class=\"int-steps\">";
      h += "<li>" + u("prim") + ": " + tex("F(x)=" + pTexI(H)) + "</li>";
      h += "<li>" + tex("F(" + bt + ")=" + FB.tex()) + ", \\(\\ \\)" + tex("F(" + at + ")=" + FA.tex()) + "</li>";
      h += "<li>" + tex("\\Big[F(x)\\Big]_{" + at + "}^{" + bt + "}=F(" + bt + ")-F(" + at + ")=" + par(FB.tex(), false) + "-" + par(FA.tex(), FA.n < 0) + "=" + I.tex()) + (I.d === 1 ? "" : " " + tex("\\approx" + numTex(+I.val().toFixed(4)))) + "</li></ol>";
      var a = Math.min(A.val(), B.val()), b = Math.max(A.val(), B.val()), f = pFn(p), pcs = signPieces(f, a, b), fill = [];
      pcs.forEach(function (q) { fill.push({ f: f, a: q.a, b: q.b, col: q.v >= 0 ? "var(--ok)" : "var(--bad)" }); });
      if (pcs.length > 1) h += '<p class="msg-bad">' + u("warn0") + "</p>";
      info.innerHTML = h.replace(/\\\((.*?)\\\)/g, function (_, x) { return tex(x); });
      var pad = (b - a) * 0.25 + 0.3, yy = autoY([f], a - pad, b + pad);
      plot(svg, { v: [a - pad, b + pad, yy[0], yy[1]], curves: [{ f: f }], fill: fill, guides: [{ x: a }, { x: b }] });
    }
    onLang(draw);
  }

  /* ---------- àrees: entre f i OX, entre f i g, i calculadora ---------- */
  // h = f − g. Retorna {pts, H, pieces, total} o un missatge d'error
  function areaCalc(h, A, B) {
    var pts;
    if (A) {
      var rs = pRoots(h, A.val(), B.val()).filter(function (o) { return o.v > A.val() + 1e-9 && o.v < B.val() - 1e-9; });
      pts = [P(A)].concat(rs).concat([P(B)]);
      return finish(pts, rs);
    }
    var all = pRoots(h, -60, 60);
    if (all.length < 2) return { err: true, rs: all };
    return finish(all, all);
    function finish(pts, rs) {
      var H = pInt(h), Hv = pts.map(function (o) { return hAt(H, o); }), pieces = [], exact = true, tq = new Fr(0), tv = 0;
      for (var i = 0; i + 1 < pts.length; i++) {
        var d = hDiff(Hv[i + 1], Hv[i]);
        // una arrel doble no separa trossos de signe diferent, però no fa cap mal
        pieces.push({ a: pts[i], b: pts[i + 1], Ha: Hv[i], Hb: Hv[i + 1], d: d });
        if (d.q) tq = tq.add(frAbs(d.q)); else exact = false;
        tv += Math.abs(d.v);
      }
      return { pts: pts, rs: rs, H: H, pieces: pieces, total: exact ? P(tq) : P(null, tv), all: exact };
    }
  }
  function areaHtml(R, hTex, two, A) {
    var Gn = two ? "G" : "F", s = '<ol class="int-steps">';
    s += "<li>" + u("cuts") + ": " + tex((two ? "f(x)=g(x)\\iff " : "") + hTex + "=0") + " ⇒ " + (R.rs.length || !A ? tex("x=" + R.rs.map(ptT).join(",\\ x=")) : u("noCut")) + "</li>";
    if (A) s += "<li>" + u("inside") + " " + tex("(" + ptT(R.pts[0]) + "," + ptT(R.pts[R.pts.length - 1]) + ")") + ": " + (R.rs.length ? tex(R.rs.map(ptT).join(",\\ ")) : u("noneIn")) + "</li>";
    s += "<li>" + u("prim") + ": " + tex(Gn + "(x)=\\displaystyle\\int\\left(" + hTex + "\\right)dx=" + pTexI(R.H)) + "</li>";
    s += "<li>" + u("pieces") + ":<br>" + R.pieces.map(function (q) {
      return tex("\\displaystyle\\int_{" + ptT(q.a) + "}^{" + ptT(q.b) + "}=" + Gn + "(" + ptT(q.b) + ")-" + Gn + "(" + ptT(q.a) + ")=" + par(valT(q.Hb), false) + "-" + par(valT(q.Ha), q.Ha.v < 0 || !q.Ha.q) + "=" + valT(q.d));
    }).join("<br>") + "</li>";
    var abs = R.pieces.map(function (q) { return "\\left|" + valT(q.d) + "\\right|"; }).join("+");
    s += '<li class="sum-big">' + u("total") + ": " + tex("A=" + abs + "=" + valT(R.total) + "\\ \\text{u}^2") + (R.total.q && R.total.q.d > 1 ? " " + tex("\\approx" + numTex(+R.total.v.toFixed(3))) : "") + "</li></ol>";
    return s;
  }
  function areaPlot(svg, fP, gP, R, A, B, two) {
    var f = pFn(fP), g = gP ? pFn(gP) : null, xs = R && !R.err ? R.pts.map(function (o) { return o.v; }) : [A ? A.val() : -3, B ? B.val() : 3];
    var lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs), pad = Math.max((hi - lo) * 0.18, 0.6);
    var fs = g ? [f, g] : [f], yy = autoY(fs, lo - pad, hi + pad, 0.12), fill = [];
    if (R && !R.err) R.pieces.forEach(function (q) { fill.push({ f: f, g: g, a: q.a.v, b: q.b.v, col: two ? "var(--accent-2)" : q.d.v >= 0 ? "var(--ok)" : "var(--bad)" }); });
    var curves = [{ f: f, col: "var(--accent)" }]; if (g) curves.push({ f: g, col: "var(--r3)" });
    var pts = R && !R.err ? R.rs.map(function (o) { return { x: o.v, y: f(o.v), col: "var(--text)" }; }) : [];
    plot(svg, { v: [lo - pad, hi + pad, yy[0], yy[1]], curves: curves, fill: fill, pts: pts, guides: A ? [{ x: A.val() }, { x: B.val() }] : [] });
  }
  function readLims(ai, bi) {
    var A = parseLim(ai.value), B = parseLim(bi.value);
    if (A === null && B === null) { ai.classList.remove("bad"); bi.classList.remove("bad"); return { ok: true, A: null, B: null }; }
    var ok = A && B && A.val() < B.val();
    ai.classList.toggle("bad", !ok); bi.classList.toggle("bad", !ok);
    return { ok: !!ok, A: A, B: B, msg: (A === null) !== (B === null) ? u("both") : u("aBad") };
  }
  function wArea(id, two) {
    var w = document.getElementById(id); if (!w) return;
    var PRE = two ? [["x^2", "x+2", "", ""], ["x^2-4x", "-x^2+2x", "", ""], ["x^3", "x", "", ""], ["x^2+2", "x", "0", "2"], ["x^2", "2x", "1", "3"]]
      : [["-x^2+4", "", ""], ["x^2-2x", "", ""], ["x^3-4x", "", ""], ["x^2+1", "-1", "2"], ["x^2-1", "0", "2"], ["x^2-4x+3", "0", "4"]];
    var fi = $(w, "f"), gi = $(w, "g"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, two ? "pA2" : "pA1", function (i) {
      var q = PRE[i]; fi.value = q[0]; if (two) { gi.value = q[1]; ai.value = q[2]; bi.value = q[3]; } else { ai.value = q[1]; bi.value = q[2]; } draw();
    });
    [fi, gi, ai, bi].forEach(function (el) { if (el) el.addEventListener("input", draw); });
    function draw() {
      var fP = polyOrNull(fi.value), gP = two ? polyOrNull(gi.value) : [new Fr(0)];
      fi.classList.toggle("bad", !fP); if (two) gi.classList.toggle("bad", !gP);
      if (!fP || !gP) { info.textContent = u("notPoly"); return; }
      var L = readLims(ai, bi);
      if (!L.ok) { info.textContent = L.msg; return; }
      var hP = pAdd(fP, gP, -1), hTex = two ? "\\left(" + pTex(fP) + "\\right)-\\left(" + pTex(gP) + "\\right)" : pTex(fP);
      var head = "<p>" + tex("f(x)=" + pTex(fP)) + (two ? ",\\ " + tex("g(x)=" + pTex(gP)) : "") + (L.A ? ",\\ " + tex("x=" + L.A.tex()) + ", " + tex("x=" + L.B.tex()) : "") + "</p>";
      if (two && pDeg(hP) === 0 && hP[0].zero()) { info.innerHTML = head + "<p>" + u("same2") + "</p>"; areaPlot(svg, fP, gP, null, L.A, L.B, two); return; }
      if (two) head += "<p>" + tex("f(x)-g(x)=" + pTex(hP)) + "</p>";
      var R = areaCalc(hP, L.A, L.B);
      if (R.err) { info.innerHTML = head + "<p>" + u(two ? "noReg2" : "noReg") + "</p>"; areaPlot(svg, fP, two ? gP : null, null, null, null, two); return; }
      info.innerHTML = head + areaHtml(R, two ? pTex(hP) : pTex(fP), two, L.A);
      areaPlot(svg, fP, two ? gP : null, R, L.A, L.B, two);
    }
    onLang(draw);
  }

  /* ---------- calculadora d'integrals i àrees ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var PRE = [["3x^2-2x+1", "", "", ""], ["x^2-4x+3", "", "0", "4"], ["x^3-4x", "", "", ""], ["x^2", "x+2", "", ""], ["x^2", "x", "0", "2"]];
    var fi = $(w, "f"), gi = $(w, "g"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg.lp-svg"), out = $(w, "out");
    presetBtns($(w, "presets"), PRE.length, "pLab", function (i) { var q = PRE[i]; fi.value = q[0]; gi.value = q[1]; ai.value = q[2]; bi.value = q[3]; draw(); });
    [fi, gi, ai, bi].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var fP = polyOrNull(fi.value), two = gi.value.trim() !== "", gP = two ? polyOrNull(gi.value) : [new Fr(0)];
      fi.classList.toggle("bad", !fP); gi.classList.toggle("bad", !gP);
      if (!fP || !gP) { out.textContent = u("notPoly"); return; }
      var L = readLims(ai, bi);
      if (!L.ok) { out.textContent = L.msg; return; }
      var hP = pAdd(fP, gP, -1), H = pInt(fP);
      var h = "<h4>" + u("indef") + "</h4><p>" + tex("\\displaystyle\\int\\left(" + pTex(fP) + "\\right)dx=" + pTexI(H) + "+C") + "</p>";
      if (L.A) {
        var FA = pEval(H, L.A), FB = pEval(H, L.B), I = FB.sub(FA);
        h += "<h4>" + u("def") + "</h4><p>" + tex("\\displaystyle\\int_{" + L.A.tex() + "}^{" + L.B.tex() + "}f(x)\\,dx=F(" + L.B.tex() + ")-F(" + L.A.tex() + ")=" + FB.tex() + "-" + par(FA.tex(), FA.n < 0) + "=" + I.tex()) + "</p>";
      }
      h += "<h4>" + u(two ? "btw" : "ax") + "</h4>";
      if (two && hP.length === 1 && hP[0].zero()) { out.innerHTML = h + "<p>" + u("same2") + "</p>"; areaPlot(svg, fP, gP, null, L.A, L.B, true); return; }
      var R = areaCalc(hP, L.A, L.B);
      if (R.err) { out.innerHTML = h + "<p>" + u(two ? "noReg2" : "noReg") + "</p>"; areaPlot(svg, fP, two ? gP : null, null, null, null, two); return; }
      out.innerHTML = h + areaHtml(R, pTex(hP), two, L.A);
      areaPlot(svg, fP, two ? gP : null, R, L.A, L.B, two);
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("$\\int 3x^2\\,dx$ és…", "$\\int 3x^2\\,dx$ es…", "$\\int 3x^2\\,dx$ is…"),
      o: [q3("$6x+C$"), q3("$x^3+C$"), q3("$3x^3+C$")], a: 1, e: q3("$3\\cdot\\frac{x^3}{3}=x^3$. Comprovació: $(x^3)'=3x^2$.", "$3\\cdot\\frac{x^3}{3}=x^3$. Comprobación: $(x^3)'=3x^2$.", "$3\\cdot\\frac{x^3}{3}=x^3$. Check: $(x^3)'=3x^2$.") },
    { q: q3("$\\int(x+1)\\,dx$ és…", "$\\int(x+1)\\,dx$ es…", "$\\int(x+1)\\,dx$ is…"),
      o: [q3("$\\frac{x^2}{2}+x+C$"), q3("$x^2+x+C$"), q3("$\\frac{(x+1)^2}{2}$")], a: 0,
      e: q3("Terme a terme: $\\frac{x^2}{2}+x+C$. (La tercera opció també és una primitiva, però li falta la $+C$.)", "Término a término: $\\frac{x^2}{2}+x+C$. (La tercera opción también es una primitiva, pero le falta la $+C$.)", "Term by term: $\\frac{x^2}{2}+x+C$. (The third option is also an antiderivative, but it lacks the $+C$.)") },
    { q: q3("La primitiva de $f(x)=2x$ que passa per $(0,3)$ és…", "La primitiva de $f(x)=2x$ que pasa por $(0,3)$ es…", "The antiderivative of $f(x)=2x$ through $(0,3)$ is…"),
      o: [q3("$x^2+3$"), q3("$2x+3$"), q3("$x^2-3$")], a: 0, e: q3("$F(x)=x^2+C$ i $F(0)=C=3$.", "$F(x)=x^2+C$ y $F(0)=C=3$.", "$F(x)=x^2+C$ and $F(0)=C=3$.") },
    { q: q3("$\\int x\\,(x^2+1)^3\\,dx$ és…", "$\\int x\\,(x^2+1)^3\\,dx$ es…", "$\\int x\\,(x^2+1)^3\\,dx$ is…"),
      o: [q3("$\\frac{(x^2+1)^4}{4}+C$"), q3("$\\frac{(x^2+1)^4}{8}+C$"), q3("$\\frac{x^2}{2}\\cdot\\frac{(x^2+1)^4}{4}+C$")], a: 1,
      e: q3("$\\frac12\\int 2x(x^2+1)^3\\,dx=\\frac12\\cdot\\frac{(x^2+1)^4}{4}$.") },
    { q: q3("$\\displaystyle\\int_0^2 x\\,dx$ val…", "$\\displaystyle\\int_0^2 x\\,dx$ vale…", "$\\displaystyle\\int_0^2 x\\,dx$ equals…"),
      o: [q3("$1$"), q3("$2$"), q3("$4$")], a: 1, e: q3("És un triangle de base 2 i altura 2: $\\frac{2\\cdot2}{2}=2$. Amb Barrow: $\\left[\\frac{x^2}{2}\\right]_0^2=2$.", "Es un triángulo de base 2 y altura 2: $\\frac{2\\cdot2}{2}=2$. Con Barrow: $\\left[\\frac{x^2}{2}\\right]_0^2=2$.", "It is a triangle with base 2 and height 2: $\\frac{2\\cdot2}{2}=2$. With Barrow: $\\left[\\frac{x^2}{2}\\right]_0^2=2$.") },
    { q: q3("Si $f(x)\\lt0$ en tot $[a,b]$, aleshores $\\int_a^b f(x)\\,dx$ és…", "Si $f(x)\\lt0$ en todo $[a,b]$, entonces $\\int_a^b f(x)\\,dx$ es…", "If $f(x)\\lt0$ on all of $[a,b]$, then $\\int_a^b f(x)\\,dx$ is…"),
      o: [q3("positiva", "positiva", "positive"), q3("negativa", "negativa", "negative"), q3("zero", "cero", "zero")], a: 1,
      e: q3("És l'àrea canviada de signe.", "Es el área cambiada de signo.", "It is the area with a minus sign.") },
    { q: q3("$\\displaystyle\\int_1^3 2x\\,dx$ val…", "$\\displaystyle\\int_1^3 2x\\,dx$ vale…", "$\\displaystyle\\int_1^3 2x\\,dx$ equals…"),
      o: [q3("$8$"), q3("$9$"), q3("$4$")], a: 0, e: q3("$\\left[x^2\\right]_1^3=9-1=8$.") },
    { q: q3("Si $\\int_0^2 f(x)\\,dx=5$, quant val $\\int_2^0 f(x)\\,dx$?", "Si $\\int_0^2 f(x)\\,dx=5$, ¿cuánto vale $\\int_2^0 f(x)\\,dx$?", "If $\\int_0^2 f(x)\\,dx=5$, what is $\\int_2^0 f(x)\\,dx$?"),
      o: [q3("$5$"), q3("$-5$"), q3("$0$")], a: 1, e: q3("Canviar l'ordre dels límits canvia el signe.", "Cambiar el orden de los límites cambia el signo.", "Swapping the limits changes the sign.") },
    { q: q3("L'àrea del recinte limitat per $y=x^2-1$ i l'eix OX és…", "El área del recinto limitado por $y=x^2-1$ y el eje OX es…", "The area of the region bounded by $y=x^2-1$ and the x-axis is…"),
      o: [q3("$-\\frac43$ u²"), q3("$\\frac43$ u²"), q3("$\\frac23$ u²")], a: 1,
      e: q3("Talls en $\\pm1$; $\\int_{-1}^{1}(x^2-1)\\,dx=-\\frac43$; l'àrea és el valor absolut.", "Cortes en $\\pm1$; $\\int_{-1}^{1}(x^2-1)\\,dx=-\\frac43$; el área es el valor absoluto.", "Roots at $\\pm1$; $\\int_{-1}^{1}(x^2-1)\\,dx=-\\frac43$; the area is the absolute value.") },
    { q: q3("Per calcular l'àrea del recinte tancat per dues corbes $f$ i $g$, el primer pas és…", "Para calcular el área del recinto encerrado por dos curvas $f$ y $g$, el primer paso es…", "To find the area enclosed by two curves $f$ and $g$, the first step is…"),
      o: [q3("derivar $f-g$", "derivar $f-g$", "differentiate $f-g$"), q3("resoldre $f(x)=g(x)$ per trobar els punts de tall", "resolver $f(x)=g(x)$ para hallar los puntos de corte", "solve $f(x)=g(x)$ to find the intersection points"), q3("integrar $f$ entre $0$ i $1$", "integrar $f$ entre $0$ y $1$", "integrate $f$ from $0$ to $1$")], a: 1,
      e: q3("Els punts de tall són els límits d'integració (o divideixen l'interval en trossos).", "Los puntos de corte son los límites de integración (o dividen el intervalo en trozos).", "The intersection points are the limits of integration (or split the interval into pieces).") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Integrals · FentMates", es: "Integrales · FentMates", en: "Integrals · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }

  function init() {
    document.title = TITLES[lang];
    var Dl = [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, { delimiters: Dl, ignoredClasses: ["widget", "lab"], throwOnError: false });
      document.querySelectorAll(".widget .wt, .widget label, .widget .legend, .widget > p, #w-lab label, #w-lab .legend").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFigs, wFam, wPoly, wChk, wRiem, wSign, wBarrow, function wArea1() { wArea("w-area1", false); }, function wArea2() { wArea("w-area2", true); }, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM8 = { parse: parse, polyOrNull: polyOrNull, pInt: pInt, areaCalc: areaCalc, parseFr: parseFr };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
