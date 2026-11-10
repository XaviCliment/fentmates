(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-mii-u9-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt",
      bad: "No entenc l'expressió: revisa-la.", aBad: "Escriu dos límits a < b.", pc: "si", noDiff: "No sé derivar aquesta expressió.",
      fam: "Totes les primitives", slope: "En", same: "totes tenen el mateix pendent:", numF: "(primitiva calculada numèricament, amb F(0) = 0)",
      chkOk: "F′(x) = f(x): és una primitiva!", chkNo: "F′ i f no coincideixen; per exemple, en x =", chkK: "Gairebé: F′ = k·f amb k =", chkK2: "Divideix la teua F per", chkNaN: "No hi ha prou punts on totes dues estiguen definides.", dF: "Derivem la teua F:",
      chg: "Canvi", subst: "Substituïm", integ: "Integrem", undo: "Desfem el canvi", check: "Comprovació: F′ = f", pick: "Tria quina part és u:",
      good: "Bona tria: ∫v du és més senzilla.", badc: "Mala tria: ∫v du és més complicada que la inicial.", cyc: "Torna a aparéixer la integral inicial: l'aïllem.",
      ratBad: "Escriu dos polinomis (numerador i denominador).", ratNo: "No sé factoritzar el denominador amb arrels racionals i, com a molt, un factor de segon grau irreductible.",
      div: "Grau del numerador ≥ grau del denominador: primer dividim.", fact: "Factoritzem el denominador:", dec: "Descomposició en fraccions simples:", sys: "Coeficients (identificant numeradors):", res: "Resultat",
      left: "Esquerra", mid: "Punt mitjà", rightP: "Dreta", width: "Amplada de cada rectangle", sum: "Suma", exact: "Integral", err: "Error",
      barrow: "Regla de Barrow", num: "Valor numèric (Simpson)", noF: "Escriu una primitiva F per a aplicar Barrow (o deixa-ho en blanc per a veure només el valor numèric).", signed: "La integral resta l'àrea de davall de l'eix:",
      posA: "part positiva", negA: "part negativa", ftcT: "Funció integral", ftcD: "La derivada de la funció integral és f:",
      cutsX: "Talls amb l'eix OX", cutsFG: "Punts de tall de les corbes", noCut: "No troba prou punts de tall: escriu els límits a i b.", pieces: "Trossos", area: "Àrea", total: "Àrea total",
      encl: "Recinte tancat entre", limits: "Entre les rectes", hTop: "per damunt",
      pFam: ["2x", "cos x", "eˣ", "1/(1 + x²)", "3x² − 3"],
      pChk1: ["x⁴ → x⁵/5", "1/x → ln|x|", "sin x → cos x ✗", "1/cos² x → tan x", "1/√(1 − x²) → arcsin x", "2ˣ → 2ˣ/ln 2"],
      pChk2: ["(2x+1)³ → (2x+1)⁴/8", "(2x+1)³ → (2x+1)⁴/4", "x/(x² + 1) → ln(x² + 1)", "sin x cos² x", "e^(sin x) cos x", "1/(4 + x²)", "tan x"],
      pSub: ["x √(x + 1)", "eˣ/(1 + e²ˣ)", "1/(x + √x)", "sin³x cos x", "ln x / x", "√(1 − x²)"],
      pParts: ["x eˣ", "x cos 2x", "ln x", "x ln x", "x² eˣ", "eˣ sin x", "arctan x"],
      pRat: ["1/(x² − 1)", "(2x+3)/(x² + x − 2)", "(x³ + 1)/(x² − 1)", "(x + 5)/((x − 1)²(x + 2))", "1/(x³ + x)", "(3x + 1)/(x² + 2x + 5)", "(x² + 2)/(x(x + 1)²)"],
      pRiem: ["x²", "sin x", "4 − x²", "eˣ", "1/x"], pBar: ["x² − 1", "sin x", "1/x", "x eˣ", "1/(1 + x²)", "cos² x"], pFtc: ["t", "sin t", "e^(−t²)", "t² − 1", "1/t"],
      pA1: ["x² − 4", "x³ − 4x", "sin x en [0, 2π]", "x eˣ en [−1, 1]", "ln x en [1/e, e]", "4x − x³"], pA2: ["x² i x + 2", "x² i √x", "x³ i x", "sin x i cos x", "eˣ i e", "6x − x² i x² − 2x", "4/x i 5 − x"],
      pLab: ["x² i 2x", "x³ − 3x", "sin x en [0, π]", "ln x i 0 en [1, e]", "x eˣ i x en [0, 2]", "1/(1+x²) i x²/2"] },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba",
      bad: "No entiendo la expresión: revísala.", aBad: "Escribe dos límites a < b.", pc: "si", noDiff: "No sé derivar esta expresión.",
      fam: "Todas las primitivas", slope: "En", same: "todas tienen la misma pendiente:", numF: "(primitiva calculada numéricamente, con F(0) = 0)",
      chkOk: "F′(x) = f(x): ¡es una primitiva!", chkNo: "F′ y f no coinciden; por ejemplo, en x =", chkK: "Casi: F′ = k·f con k =", chkK2: "Divide tu F entre", chkNaN: "No hay suficientes puntos donde ambas estén definidas.", dF: "Derivamos tu F:",
      chg: "Cambio", subst: "Sustituimos", integ: "Integramos", undo: "Deshacemos el cambio", check: "Comprobación: F′ = f", pick: "Elige qué parte es u:",
      good: "Buena elección: ∫v du es más sencilla.", badc: "Mala elección: ∫v du es más complicada que la inicial.", cyc: "Vuelve a aparecer la integral inicial: la despejamos.",
      ratBad: "Escribe dos polinomios (numerador y denominador).", ratNo: "No sé factorizar el denominador con raíces racionales y, como mucho, un factor de segundo grado irreducible.",
      div: "Grado del numerador ≥ grado del denominador: primero dividimos.", fact: "Factorizamos el denominador:", dec: "Descomposición en fracciones simples:", sys: "Coeficientes (identificando numeradores):", res: "Resultado",
      left: "Izquierda", mid: "Punto medio", rightP: "Derecha", width: "Anchura de cada rectángulo", sum: "Suma", exact: "Integral", err: "Error",
      barrow: "Regla de Barrow", num: "Valor numérico (Simpson)", noF: "Escribe una primitiva F para aplicar Barrow (o déjalo en blanco para ver solo el valor numérico).", signed: "La integral resta el área de debajo del eje:",
      posA: "parte positiva", negA: "parte negativa", ftcT: "Función integral", ftcD: "La derivada de la función integral es f:",
      cutsX: "Cortes con el eje OX", cutsFG: "Puntos de corte de las curvas", noCut: "No encuentra suficientes puntos de corte: escribe los límites a y b.", pieces: "Trozos", area: "Área", total: "Área total",
      encl: "Recinto cerrado entre", limits: "Entre las rectas", hTop: "por encima",
      pFam: ["2x", "cos x", "eˣ", "1/(1 + x²)", "3x² − 3"],
      pChk1: ["x⁴ → x⁵/5", "1/x → ln|x|", "sen x → cos x ✗", "1/cos² x → tg x", "1/√(1 − x²) → arcsen x", "2ˣ → 2ˣ/ln 2"],
      pChk2: ["(2x+1)³ → (2x+1)⁴/8", "(2x+1)³ → (2x+1)⁴/4", "x/(x² + 1) → ln(x² + 1)", "sen x cos² x", "e^(sen x) cos x", "1/(4 + x²)", "tg x"],
      pSub: ["x √(x + 1)", "eˣ/(1 + e²ˣ)", "1/(x + √x)", "sen³x cos x", "ln x / x", "√(1 − x²)"],
      pParts: ["x eˣ", "x cos 2x", "ln x", "x ln x", "x² eˣ", "eˣ sen x", "arctg x"],
      pRat: ["1/(x² − 1)", "(2x+3)/(x² + x − 2)", "(x³ + 1)/(x² − 1)", "(x + 5)/((x − 1)²(x + 2))", "1/(x³ + x)", "(3x + 1)/(x² + 2x + 5)", "(x² + 2)/(x(x + 1)²)"],
      pRiem: ["x²", "sen x", "4 − x²", "eˣ", "1/x"], pBar: ["x² − 1", "sen x", "1/x", "x eˣ", "1/(1 + x²)", "cos² x"], pFtc: ["t", "sen t", "e^(−t²)", "t² − 1", "1/t"],
      pA1: ["x² − 4", "x³ − 4x", "sen x en [0, 2π]", "x eˣ en [−1, 1]", "ln x en [1/e, e]", "4x − x³"], pA2: ["x² y x + 2", "x² y √x", "x³ y x", "sen x y cos x", "eˣ y e", "6x − x² y x² − 2x", "4/x y 5 − x"],
      pLab: ["x² y 2x", "x³ − 3x", "sen x en [0, π]", "ln x y 0 en [1, e]", "x eˣ y x en [0, 2]", "1/(1+x²) y x²/2"] },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top",
      bad: "I can't read that expression: check it.", aBad: "Type two limits a < b.", pc: "if", noDiff: "I can't differentiate this expression.",
      fam: "All the antiderivatives", slope: "At", same: "they all have the same slope:", numF: "(antiderivative computed numerically, with F(0) = 0)",
      chkOk: "F′(x) = f(x): it is an antiderivative!", chkNo: "F′ and f do not match; for example, at x =", chkK: "Almost: F′ = k·f with k =", chkK2: "Divide your F by", chkNaN: "Not enough points where both are defined.", dF: "Differentiate your F:",
      chg: "Substitution", subst: "Substitute", integ: "Integrate", undo: "Undo the substitution", check: "Check: F′ = f", pick: "Choose which part is u:",
      good: "Good choice: ∫v du is simpler.", badc: "Bad choice: ∫v du is harder than the original.", cyc: "The original integral appears again: solve for it.",
      ratBad: "Type two polynomials (numerator and denominator).", ratNo: "I can't factor the denominator with rational roots and at most one irreducible quadratic factor.",
      div: "Degree of numerator ≥ degree of denominator: divide first.", fact: "Factor the denominator:", dec: "Partial fraction decomposition:", sys: "Coefficients (matching numerators):", res: "Result",
      left: "Left", mid: "Midpoint", rightP: "Right", width: "Width of each rectangle", sum: "Sum", exact: "Integral", err: "Error",
      barrow: "Fundamental theorem (Barrow's rule)", num: "Numerical value (Simpson)", noF: "Type an antiderivative F to apply Barrow's rule (or leave it blank to see only the numerical value).", signed: "The integral subtracts the area below the axis:",
      posA: "positive part", negA: "negative part", ftcT: "Integral function", ftcD: "The derivative of the integral function is f:",
      cutsX: "Intercepts with the x-axis", cutsFG: "Intersection points of the curves", noCut: "Not enough intersection points: type the limits a and b.", pieces: "Pieces", area: "Area", total: "Total area",
      encl: "Region enclosed between", limits: "Between the lines", hTop: "on top",
      pFam: ["2x", "cos x", "eˣ", "1/(1 + x²)", "3x² − 3"],
      pChk1: ["x⁴ → x⁵/5", "1/x → ln|x|", "sin x → cos x ✗", "1/cos² x → tan x", "1/√(1 − x²) → arcsin x", "2ˣ → 2ˣ/ln 2"],
      pChk2: ["(2x+1)³ → (2x+1)⁴/8", "(2x+1)³ → (2x+1)⁴/4", "x/(x² + 1) → ln(x² + 1)", "sin x cos² x", "e^(sin x) cos x", "1/(4 + x²)", "tan x"],
      pSub: ["x √(x + 1)", "eˣ/(1 + e²ˣ)", "1/(x + √x)", "sin³x cos x", "ln x / x", "√(1 − x²)"],
      pParts: ["x eˣ", "x cos 2x", "ln x", "x ln x", "x² eˣ", "eˣ sin x", "arctan x"],
      pRat: ["1/(x² − 1)", "(2x+3)/(x² + x − 2)", "(x³ + 1)/(x² − 1)", "(x + 5)/((x − 1)²(x + 2))", "1/(x³ + x)", "(3x + 1)/(x² + 2x + 5)", "(x² + 2)/(x(x + 1)²)"],
      pRiem: ["x²", "sin x", "4 − x²", "eˣ", "1/x"], pBar: ["x² − 1", "sin x", "1/x", "x eˣ", "1/(1 + x²)", "cos² x"], pFtc: ["t", "sin t", "e^(−t²)", "t² − 1", "1/t"],
      pA1: ["x² − 4", "x³ − 4x", "sin x on [0, 2π]", "x eˣ on [−1, 1]", "ln x on [1/e, e]", "4x − x³"], pA2: ["x² and x + 2", "x² and √x", "x³ and x", "sin x and cos x", "eˣ and e", "6x − x² and x² − 2x", "4/x and 5 − x"],
      pLab: ["x² and 2x", "x³ − 3x", "sin x on [0, π]", "ln x and 0 on [1, e]", "x eˣ and x on [0, 2]", "1/(1+x²) and x²/2"] }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { var v = (UI[lang] || UI.va)[k]; return v === undefined ? UI.va[k] : v; }
  function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }
  function rt(s) { return String(s).replace(/\\\((.*?)\\\)/g, function (m, f) { return tex(f); }); }

  /*@@CORE@@*/
  /*@@DERIV@@*/
  /*@@STUDY@@*/

  /* ---------- integrals numèriques i valors exactes ---------- */
  // Simpson adaptatiu
  function simpson(f, a, b, N) {
    N = N || 2000; if (N % 2) N++;
    var h = (b - a) / N, s = f(a) + f(b);
    for (var i = 1; i < N; i++) s += (i % 2 ? 4 : 2) * f(a + i * h);
    return s * h / 3;
  }
  // Simpson adaptatiu (precís també amb arrels en els extrems)
  function asimp(f, a, b, eps) {
    function S(a, b, fa, fm, fb) { return (b - a) / 6 * (fa + 4 * fm + fb); }
    function rec(a, b, fa, fm, fb, whole, eps, depth) {
      var m = (a + b) / 2, lm = (a + m) / 2, rm = (m + b) / 2, flm = f(lm), frm = f(rm);
      var L = S(a, m, fa, flm, fm), R = S(m, b, fm, frm, fb);
      if (depth <= 0 || Math.abs(L + R - whole) <= 15 * eps) return L + R + (L + R - whole) / 15;
      return rec(a, m, fa, flm, fm, L, eps / 2, depth - 1) + rec(m, b, fm, frm, fb, R, eps / 2, depth - 1);
    }
    var fa = f(a), fb = f(b), fm = f((a + b) / 2);
    return rec(a, b, fa, fm, fb, S(a, b, fa, fm, fb), eps, 48);
  }
  // integral amb extrems on f pot no existir (1/x en 0, ln x en 0): retalla una mica
  function integ(f, a, b) {
    var fa = isFinite(f(a)) ? a : a + 1e-12 * (1 + Math.abs(a)), fb = isFinite(f(b)) ? b : b - 1e-12 * (1 + Math.abs(b));
    var n = 16, h = (fb - fa) / n, s = 0;
    for (var i = 0; i < n; i++) s += asimp(f, fa + i * h, fa + (i + 1) * h, 1e-12);
    return s;
  }
  // reconeix a + b·c amb c = ln 2, ln 3, π, e…, a i b racionals senzills
  var BASIS = [[Math.log(2), "\\ln2"], [Math.log(3), "\\ln3"], [Math.log(5), "\\ln5"], [Math.PI, "\\pi"], [Math.E, "e"], [1 / Math.E, "e", 1], [Math.E * Math.E, "e^2"], [1 / (Math.E * Math.E), "e^2", 1], [Math.sqrt(2), "\\sqrt2"], [Math.sqrt(3), "\\sqrt3"], [Math.PI * Math.PI, "\\pi^2"], [Math.log(7), "\\ln7"], [Math.exp(0.5), "\\sqrt e"], [Math.exp(-0.5), "\\sqrt e", 1]];
  function sqrtSimp(s) {
    return s.replace(/(\d*)\\sqrt\{(\d+)\}/g, function (m, k, n) {
      n = +n; k = k ? +k : 1; var o = 1;
      for (var q = Math.floor(Math.sqrt(n)); q > 1; q--) if (n % (q * q) === 0) { o = q; n = n / (q * q); break; }
      k *= o; return (k === 1 ? "" : k) + (n === 1 ? (k === 1 ? "1" : "") : "\\sqrt{" + n + "}");
    });
  }
  function exactTex(v) {
    if (!isFinite(v)) return numTex(v);
    var s = sqrtSimp(nn(v).replace(/e\^\{1\}/g, "e")); if (s.indexOf("\\approx") < 0 && !/\d\{?,\}?\d{3}/.test(s) && !/\.\d{3}/.test(s)) return s;
    for (var k = 0; k < BASIS.length; k++) {
      var c = BASIS[k][0], ct = BASIS[k][1], inv = BASIS[k][2];
      for (var d = 1; d <= 12; d++) for (var n = -60; n <= 60; n++) {
        if (!n || gcdI(n, d) !== 1) continue;
        var a = fracOf(v - n / d * c, 12);
        if (!a || Math.abs(a.val() + n / d * c - v) > 1e-8 * (1 + Math.abs(v))) continue;
        var an = Math.abs(n), bq;
        if (inv) bq = "\\frac{" + an + "}{" + (d === 1 ? "" : d) + ct + "}";
        else bq = d === 1 ? (an === 1 ? "" : an) + ct : "\\frac{" + (an === 1 ? "" : an) + ct + "}{" + d + "}";
        if (a.zero()) return (n < 0 ? "-" : "") + bq;
        // el terme irracional primer si és positiu i el racional negatiu (e^2-1); si no, el racional primer
        if (n > 0 && a.n < 0) return bq + "-" + new Fr(-a.n, a.d).tex();
        return a.tex() + (n < 0 ? "-" : "+") + bq;
      }
    }
    return "\\approx" + numTex(+v.toFixed(4));
  }
  function eqT(v) { var s = exactTex(v); return s.indexOf("\\approx") === 0 ? s : "=" + s; }
  function exactA(v) { var s = exactTex(v); return s.indexOf("\\approx") === 0 || /^-?\d+$/.test(s) ? s : s + "\\approx" + numTex(+v.toFixed(4)); }
  function readF(fi) { try { var n = strip0(parse(fi.value)); fi.classList.remove("bad"); return n; } catch (e) { fi.classList.add("bad"); return null; } }
  function readLim(el) { var s = String(el.value).trim(); if (!s) return null; var v = readNum(s); el.classList.toggle("bad", !isFinite(v)); return isFinite(v) ? v : undefined; }
  function dF(G, x) { var h = 1e-5 * Math.max(1, Math.abs(x)); return (G(x + h) - G(x - h)) / (2 * h); }
  function sameFn(G, f, x0, x1) {
    var xs = [], bad = null, ks = [];
    for (var i = 0; i <= 80; i++) { var x = x0 + (x1 - x0) * (i + 0.37) / 81; if (isFinite(f(x)) && isFinite(G(x)) && isFinite(dF(G, x)) && Math.abs(f(x)) < 1e7) xs.push(x); }
    xs.forEach(function (x) { var a = dF(G, x), b = f(x); if (bad === null && Math.abs(a - b) > 1e-4 * (1 + Math.abs(b))) bad = x; if (Math.abs(b) > 1e-3) ks.push(a / b); });
    var k0 = ks.length ? ks[0] : NaN, cst = ks.length > 4 && ks.every(function (k) { return Math.abs(k - k0) < 1e-4 * (1 + Math.abs(k0)); });
    return { n: xs.length, bad: bad, k: cst ? k0 : null };
  }
  function chkHtml(G, f, x0, x1) {
    var S = sameFn(G, f, x0, x1);
    if (S.n < 8) return "<p>" + u("chkNaN") + "</p>";
    if (S.bad === null) return '<p><span class="chk ok">✓ ' + u("chkOk") + "</span></p>";
    if (S.k !== null && Math.abs(S.k) > 1e-6) return '<p><span class="chk no">' + u("chkK") + " " + numTxt(snap(S.k)) + "</span> " + u("chkK2") + " " + tex(nn(S.k)) + ".</p>";
    return '<p><span class="chk no">✗ ' + u("chkNo") + " " + numTxt(+S.bad.toFixed(2)) + "</span></p>";
  }
  function trimLabel(n) { return texD(n); }

  /* ---------- 9.1 família de primitives ---------- */
  function wFam() {
    var w = document.getElementById("w-fam"); if (!w) return;
    var PRE = ["2x", "cos(x)", "e^x", "1/(1+x^2)", "3x^2-3"];
    var fi = $(w, "f"), rc = $(w, "c"), rx = $(w, "x"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pFam", function (i) { fi.value = PRE[i]; rc.value = 0; draw(); });
    [fi, rc, rx].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var n = readF(fi); if (!n) { info.textContent = u("bad"); return; }
      var f = compile(n), c = +rc.value, x = +rx.value;
      $(w, "cv").textContent = numTxt(c); $(w, "xv").textContent = numTxt(x);
      // primitiva numèrica amb F(0) = 0, tabulada en [−3, 3]
      var M = 600, X0 = -3, X1 = 3, hh = (X1 - X0) / M, T = [0], i;
      for (i = 1; i <= M; i++) T.push(T[i - 1] + simpson(f, X0 + (i - 1) * hh, X0 + i * hh, 8));
      var off = T[M / 2];
      function F0(t) { if (t < X0 || t > X1) return NaN; var k = Math.min(M - 1, Math.floor((t - X0) / hh)), r = (t - X0 - k * hh) / hh; return T[k] + (T[k + 1] - T[k]) * r - off; }
      var m = f(x), curves = [], k, hw = 0.4;
      var yy = autoY([function (t) { return F0(t) - 4; }, function (t) { return F0(t) + 4; }], -2.8, 2.8, 0.05);
      var v = [-2.8, 2.8, Math.max(yy[0], -12), Math.min(yy[1], 14)];
      for (k = -4; k <= 4; k += 2) if (Math.abs(k - c) > 1e-9) curves.push({ f: (function (k) { return function (t) { return F0(t) + k; }; })(k), col: "var(--border)" });
      curves.push({ f: function (t) { return F0(t) + c; }, col: "var(--accent)" });
      for (k = -4; k <= 4; k += 2) curves.push({ f: lineF(m, x, F0(x) + k), a: x - hw, b: x + hw, col: "var(--accent-2)" });
      curves.push({ f: lineF(m, x, F0(x) + c), a: x - hw, b: x + hw, col: "var(--accent-2)" });
      var h = "<p>" + tex("f(x)=" + texD(n)) + "</p><p>" + u("fam") + ": " + tex("F(x)+C") + " <span class=\"hint\">" + u("numF") + "</span></p>";
      h += "<p>" + tex("C=" + numTex(c)) + "</p><p>" + u("slope") + " " + tex("x=" + numTex(+x.toFixed(2))) + " " + u("same") + " " + tex("F'(" + numTex(+x.toFixed(2)) + ")=f(" + numTex(+x.toFixed(2)) + ")=" + numTex(+m.toFixed(4))) + "</p>";
      info.innerHTML = h;
      plot(svg, { v: v, curves: curves, pts: [{ x: x, y: F0(x) + c }], guides: [{ x: x }] });
    }
    onLang(draw);
  }

  /* ---------- 9.2 i 9.3 comprova la primitiva ---------- */
  function wChk(id, PRE, key) {
    var w = document.getElementById(id); if (!w) return;
    var fi = $(w, "f"), Fi = $(w, "F"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, key, function (i) { fi.value = PRE[i][0]; Fi.value = PRE[i][1]; draw(); });
    [fi, Fi].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var nf = readF(fi), nF = readF(Fi); if (!nf || !nF) { info.textContent = u("bad"); return; }
      var fn = compile(nf), Fn = compile(nF), h = "<p>" + tex("f(x)=" + texD(nf)) + "</p><p>" + tex("F(x)=" + texD(nF)) + "</p>";
      try { h += "<p>" + u("dF") + " " + tex("F'(x)=" + texD(D(nF))) + "</p>"; } catch (e) {}
      info.innerHTML = h + chkHtml(Fn, fn, -3.1, 3.1);
      var yy = autoY([fn], -3.2, 3.2);
      plot(svg, { v: [-3.2, 3.2, yy[0], yy[1]], curves: [{ f: fn, col: "var(--accent)" }, { f: function (x) { return dF(Fn, x); }, col: "var(--accent-2)" }] });
    }
    onLang(draw);
  }

  /* ---------- passos guiats (canvi de variable i per parts) ---------- */
  function stepList(steps) { return '<ol class="int-steps">' + steps.map(function (s) { return "<li>" + (s[0] ? "<strong>" + u(s[0]) + ":</strong> " : "") + tex(s[1], true) + "</li>"; }).join("") + "</ol>"; }
  var SUB = [
    { f: "x*sqrt(x+1)", F: "2(x+1)^(5/2)/5-2(x+1)^(3/2)/3", s: [["chg", "t=\\sqrt{x+1}\\ \\Rightarrow\\ x=t^2-1,\\quad dx=2t\\,dt"], ["subst", "\\int x\\sqrt{x+1}\\,dx=\\int(t^2-1)\\,t\\cdot2t\\,dt=\\int\\left(2t^4-2t^2\\right)dt"], ["integ", "=\\frac{2t^5}{5}-\\frac{2t^3}{3}+C"], ["undo", "=\\frac25(x+1)^{5/2}-\\frac23(x+1)^{3/2}+C"]] },
    { f: "e^x/(1+e^(2x))", F: "arctan(e^x)", s: [["chg", "t=e^x,\\quad dt=e^x\\,dx"], ["subst", "\\int\\frac{e^x}{1+e^{2x}}\\,dx=\\int\\frac{dt}{1+t^2}"], ["integ", "=\\arctan t+C"], ["undo", "=\\arctan e^x+C"]] },
    { f: "1/(x+sqrt(x))", F: "2ln(sqrt(x)+1)", s: [["chg", "t=\\sqrt x\\ \\Rightarrow\\ x=t^2,\\quad dx=2t\\,dt"], ["subst", "\\int\\frac{dx}{x+\\sqrt x}=\\int\\frac{2t\\,dt}{t^2+t}=\\int\\frac{2\\,dt}{t+1}"], ["integ", "=2\\ln|t+1|+C"], ["undo", "=2\\ln\\left(\\sqrt x+1\\right)+C"]] },
    { f: "sin(x)^3*cos(x)", F: "sin(x)^4/4", s: [["chg", "t=\\sin x,\\quad dt=\\cos x\\,dx"], ["subst", "\\int\\sin^3x\\cos x\\,dx=\\int t^3\\,dt"], ["integ", "=\\frac{t^4}{4}+C"], ["undo", "=\\frac{\\sin^4x}{4}+C"]] },
    { f: "ln(x)/x", F: "ln(x)^2/2", s: [["chg", "t=\\ln x,\\quad dt=\\frac{dx}{x}"], ["subst", "\\int\\frac{\\ln x}{x}\\,dx=\\int t\\,dt"], ["integ", "=\\frac{t^2}{2}+C"], ["undo", "=\\frac{\\ln^2x}{2}+C"]] },
    { f: "sqrt(1-x^2)", F: "arcsin(x)/2+x*sqrt(1-x^2)/2", s: [["chg", "x=\\sin t,\\quad dx=\\cos t\\,dt,\\quad\\sqrt{1-x^2}=\\cos t"], ["subst", "\\int\\sqrt{1-x^2}\\,dx=\\int\\cos^2t\\,dt=\\int\\frac{1+\\cos2t}{2}\\,dt"], ["integ", "=\\frac t2+\\frac{\\sin2t}{4}+C=\\frac t2+\\frac{\\sin t\\cos t}{2}+C"], ["undo", "=\\frac{\\arcsin x}{2}+\\frac{x\\sqrt{1-x^2}}{2}+C"]] }
  ];
  function wSub() {
    var w = document.getElementById("w-sub"); if (!w) return;
    var out = $(w, "out"), svg = w.querySelector("svg.lp-svg"), cur = 0, shown = 1, bn = $(w, "nx"), ba = $(w, "al"), cnt = $(w, "cnt");
    presetBtns($(w, "presets"), SUB.length, "pSub", function (i) { cur = i; shown = 1; draw(); });
    bn.addEventListener("click", function () { if (shown < SUB[cur].s.length + 1) { shown++; draw(); } });
    ba.addEventListener("click", function () { shown = shown > SUB[cur].s.length ? 1 : SUB[cur].s.length + 1; draw(); });
    function draw() {
      var P = SUB[cur], nf = strip0(parse(P.f)), nF = strip0(parse(P.F)), f = compile(nf), G = compile(nF), N = P.s.length + 1;
      var h = "<p>" + tex("\\displaystyle\\int " + texD(nf) + "\\,dx") + "</p>" + stepList(P.s.slice(0, shown));
      if (shown >= N) h += "<p><strong>" + u("check") + "</strong> " + chkHtml(G, f, -0.99, 3).replace(/^<p>|<\/p>$/g, "") + "</p>";
      out.innerHTML = h;
      bn.textContent = u("next") + " →"; bn.disabled = shown >= N; ba.textContent = shown >= N ? u("reset") : u("all");
      cnt.textContent = u("step") + " " + shown + " " + u("of") + " " + N;
      var v = [-1.5, 3.5]; v = v.concat(autoY([f, G], v[0], v[1]));
      plot(svg, { v: v, curves: [{ f: f, col: "var(--accent)" }, { f: G, col: "var(--accent-2)" }] });
    }
    onLang(draw);
  }
  var PARTS = [
    { f: "x*e^x", F: "(x-1)e^x", A: "x", B: "e^x\\,dx", good: 0,
      g: [["", "u=x,\\ dv=e^x\\,dx\\ \\Rightarrow\\ du=dx,\\ v=e^x"], ["", "\\int xe^x\\,dx=xe^x-\\int e^x\\,dx=(x-1)e^x+C"]], b: ["", "u=e^x,\\ dv=x\\,dx\\ \\Rightarrow\\ \\int xe^x\\,dx=\\frac{x^2}{2}e^x-\\int\\frac{x^2}{2}e^x\\,dx\\quad(\\text{grau 2!})"] },
    { f: "x*cos(2x)", F: "x*sin(2x)/2+cos(2x)/4", A: "x", B: "\\cos2x\\,dx", good: 0,
      g: [["", "u=x,\\ dv=\\cos2x\\,dx\\ \\Rightarrow\\ du=dx,\\ v=\\frac{\\sin2x}{2}"], ["", "\\int x\\cos2x\\,dx=\\frac{x\\sin2x}{2}-\\int\\frac{\\sin2x}{2}\\,dx=\\frac{x\\sin2x}{2}+\\frac{\\cos2x}{4}+C"]], b: ["", "u=\\cos2x,\\ dv=x\\,dx\\ \\Rightarrow\\ \\frac{x^2}{2}\\cos2x+\\int x^2\\sin2x\\,dx\\quad(\\text{pitjor})"] },
    { f: "ln(x)", F: "x*ln(x)-x", A: "\\ln x", B: "dx", good: 0,
      g: [["", "u=\\ln x,\\ dv=dx\\ \\Rightarrow\\ du=\\frac{dx}{x},\\ v=x"], ["", "\\int\\ln x\\,dx=x\\ln x-\\int x\\cdot\\frac1x\\,dx=x\\ln x-x+C"]], b: ["", "dv=\\ln x\\,dx\\ \\Rightarrow\\ v=\\int\\ln x\\,dx\\quad(\\text{és el que busquem!})"] },
    { f: "x*ln(x)", F: "x^2*ln(x)/2-x^2/4", A: "\\ln x", B: "x\\,dx", good: 0,
      g: [["", "u=\\ln x,\\ dv=x\\,dx\\ \\Rightarrow\\ du=\\frac{dx}{x},\\ v=\\frac{x^2}{2}"], ["", "\\int x\\ln x\\,dx=\\frac{x^2\\ln x}{2}-\\int\\frac x2\\,dx=\\frac{x^2\\ln x}{2}-\\frac{x^2}{4}+C"]], b: ["", "dv=\\ln x\\,dx\\ \\Rightarrow\\ v=x\\ln x-x\\ \\Rightarrow\\ \\int(x\\ln x-x)\\,dx\\quad(\\text{tornem a començar})"] },
    { f: "x^2*e^x", F: "(x^2-2x+2)e^x", A: "x^2", B: "e^x\\,dx", good: 0,
      g: [["", "u=x^2,\\ dv=e^x\\,dx:\\quad\\int x^2e^x\\,dx=x^2e^x-2\\int xe^x\\,dx"], ["", "\\text{⟦de nou per parts‖de nuevo por partes‖by parts again⟧}:\\ \\int xe^x\\,dx=(x-1)e^x"], ["", "\\int x^2e^x\\,dx=\\left(x^2-2x+2\\right)e^x+C"]], b: ["", "u=e^x,\\ dv=x^2dx\\ \\Rightarrow\\ \\frac{x^3}{3}e^x-\\int\\frac{x^3}{3}e^x\\,dx\\quad(\\text{grau 3!})"] },
    { f: "e^x*sin(x)", F: "e^x*(sin(x)-cos(x))/2", A: "e^x", B: "\\sin x\\,dx", good: 2,
      g: [["", "I=\\int e^x\\sin x\\,dx;\\quad u=e^x,\\ dv=\\sin x\\,dx:\\ I=-e^x\\cos x+\\int e^x\\cos x\\,dx"], ["", "u=e^x,\\ dv=\\cos x\\,dx:\\ \\int e^x\\cos x\\,dx=e^x\\sin x-I"], ["cyc", "I=-e^x\\cos x+e^x\\sin x-I\\ \\Rightarrow\\ I=\\frac{e^x(\\sin x-\\cos x)}{2}+C"]], b: null },
    { f: "arctan(x)", F: "x*arctan(x)-ln(1+x^2)/2", A: "\\arctan x", B: "dx", good: 0,
      g: [["", "u=\\arctan x,\\ dv=dx\\ \\Rightarrow\\ du=\\frac{dx}{1+x^2},\\ v=x"], ["", "\\int\\arctan x\\,dx=x\\arctan x-\\int\\frac{x}{1+x^2}\\,dx=x\\arctan x-\\frac12\\ln\\left(1+x^2\\right)+C"]], b: ["", "dv=\\arctan x\\,dx\\quad(\\text{no en sabem la primitiva})"] }
  ];
  function wParts() {
    var w = document.getElementById("w-parts"); if (!w) return;
    var out = $(w, "out"), box = $(w, "uv"), svg = w.querySelector("svg.lp-svg"), cur = 0, ch = -1;
    presetBtns($(w, "presets"), PARTS.length, "pParts", function (i) { cur = i; ch = -1; draw(); });
    function draw() {
      var P = PARTS[cur], nf = strip0(parse(P.f)), f = compile(nf), G = compile(strip0(parse(P.F)));
      box.innerHTML = "";
      var lab = document.createElement("span"); lab.className = "hint"; lab.textContent = u("pick") + " "; box.appendChild(lab);
      ["u=" + P.A + ",\\ dv=" + P.B, "u=" + (P.B === "dx" ? "1" : P.B.replace("\\,dx", "")) + ",\\ dv=" + P.A + "\\,dx"].forEach(function (s, i) {
        var b = document.createElement("button"); b.type = "button"; b.className = "btn" + (ch === i ? " primary" : "");
        b.innerHTML = tex(s); b.addEventListener("click", function () { ch = i; draw(); }); box.appendChild(b);
      });
      var h = "<p>" + tex("\\displaystyle\\int " + texD(nf) + "\\,dx") + " &nbsp; <span class=\"hint\">" + tex("\\int u\\,dv=uv-\\int v\\,du") + "</span></p>";
      if (ch >= 0) {
        var ok = P.good === 2 || ch === P.good;
        if (ok) h += '<p><span class="chk ok">✓ ' + u("good") + "</span></p>" + stepList(P.g.map(function (s) { return [s[0], loc(s[1])]; })) + "<p><strong>" + u("check") + "</strong></p>" + chkHtml(G, f, 0.05, 3);
        else h += '<p><span class="chk no">✗ ' + u("badc") + "</span></p>" + stepList([[P.b[0], loc(P.b[1])]]);
      }
      out.innerHTML = h;
      var v = [-0.5, 3.2]; v = v.concat(autoY([f, G], v[0], v[1]));
      plot(svg, { v: v, curves: [{ f: f, col: "var(--accent)" }].concat(ch >= 0 && (P.good === 2 || ch === P.good) ? [{ f: G, col: "var(--accent-2)" }] : []) });
    }
    onLang(draw);
  }
  // ⟦va‖es‖en⟧ dins de les cadenes TeX dels passos, i \text{…} en català traduït
  var TXT = { "grau 2!": ["grau 2!", "¡grado 2!", "degree 2!"], "grau 3!": ["grau 3!", "¡grado 3!", "degree 3!"], "pitjor": ["pitjor", "peor", "worse"], "és el que busquem!": ["és el que busquem!", "¡es lo que buscamos!", "that is what we want!"],
    "tornem a començar": ["tornem a començar", "volvemos a empezar", "back to square one"], "no en sabem la primitiva": ["no en sabem la primitiva", "no sabemos su primitiva", "we do not know its antiderivative"] };
  function loc(s) {
    var i = lang === "es" ? 1 : lang === "en" ? 2 : 0;
    s = s.replace(/⟦(.*?)⟧/g, function (m, q) { return q.split("‖")[i]; });
    return s.replace(/\\text\{([^}]*)\}/g, function (m, q) { return TXT[q] ? "\\text{" + TXT[q][i] + "}" : m; });
  }

  /* ---------- 9.6 funcions racionals: fraccions simples exactes ---------- */
  function pDivide(P, Q) {
    P = pTrim(P); Q = pTrim(Q);
    var dq = Q.length - 1, r = P.slice(), q = [];
    for (var i = 0; i <= Math.max(0, P.length - 1 - dq); i++) q.push(new Fr(0));
    while (pTrim(r).length - 1 >= dq && !(pTrim(r).length === 1 && pTrim(r)[0].zero())) {
      r = pTrim(r);
      var k = r.length - 1 - dq, c = r[r.length - 1].div(Q[dq]); q[k] = c;
      var sub = []; for (var j = 0; j < k; j++) sub.push(new Fr(0));
      r = pAdd(r, sub.concat(Q.map(function (a) { return a.mul(c); })), -1);
      if (dq === 0) { r = [new Fr(0)]; break; }
    }
    return { q: pTrim(q), r: pTrim(r) };
  }
  function divisors(n) { n = Math.abs(n); var d = []; for (var i = 1; i <= n; i++) if (n % i === 0) d.push(i); return d.length ? d : [1]; }
  // arrels racionals (amb multiplicitat) i el factor que queda
  function factorQ(Q) {
    Q = pTrim(Q);
    var L = 1; Q.forEach(function (c) { L = L * c.d / gcdI(L, c.d); });
    var Z = Q.map(function (c) { return c.n * L / c.d; }), rts = [], cur = Q.slice();
    while (pDeg(cur) >= 1) {
      Z = cur.map(function (c) { return c; }); var LL = 1; Z.forEach(function (c) { LL = LL * c.d / gcdI(LL, c.d); });
      var ints = cur.map(function (c) { return c.n * LL / c.d; }), a0 = ints[0], an = ints[ints.length - 1], found = null;
      if (a0 === 0) found = new Fr(0);
      else divisors(a0).some(function (p) { return divisors(an).some(function (q) { return [1, -1].some(function (s) { var r = new Fr(s * p, q); if (pEval(cur, r).zero()) { found = r; return true; } return false; }); }); });
      if (!found) break;
      var R = ruffini(cur, found); cur = pTrim(R.q); rts.push(found);
    }
    return { roots: rts, rest: cur };
  }
  function polyFromRoots(rs, lead) { var p = [lead || new Fr(1)]; rs.forEach(function (r) { p = pMul(p, [new Fr(-r.n, r.d), new Fr(1)]); }); return p; }
  function solveLin(A, b) {
    var n = A.length, M = A.map(function (r, i) { return r.slice().concat([b[i]]); });
    for (var c = 0; c < n; c++) {
      var p = -1; for (var r = c; r < n; r++) if (!M[r][c].zero()) { p = r; break; }
      if (p < 0) return null;
      var t = M[c]; M[c] = M[p]; M[p] = t;
      for (r = 0; r < n; r++) if (r !== c && !M[r][c].zero()) { var k = M[r][c].div(M[c][c]); for (var j = c; j <= n; j++) M[r][j] = M[r][j].sub(k.mul(M[c][j])); }
    }
    return M.map(function (r, i) { return r[n].div(r[i]); });
  }
  function linT(r) { return r.zero() ? "x" : "x" + (r.n < 0 ? "+" : "-") + new Fr(Math.abs(r.n), r.d).tex(); }
  function coefT(c, rest, first) { if (c.zero()) return ""; var neg = c.n < 0, a = new Fr(Math.abs(c.n), c.d); return (neg ? "-" : first ? "" : "+") + (a.n === 1 && a.d === 1 && rest ? "" : a.tex()) + rest; }
  function fracT(c, den, first) { if (c.zero()) return ""; var neg = c.n < 0, a = new Fr(Math.abs(c.n), c.d); return (neg ? "-" : first ? "" : "+") + (a.d === 1 ? "\\dfrac{" + a.n + "}{" + den + "}" : "\\dfrac{" + a.n + "}{" + a.d + "\\left(" + den + "\\right)}"); }
  function sqrtTex(v) { var q = fracOf(v, 12); if (q) { var sn = Math.round(Math.sqrt(q.n)), sd = Math.round(Math.sqrt(q.d)); if (sn * sn === q.n && sd * sd === q.d) return new Fr(sn, sd).tex(); } return nn(Math.sqrt(v)); }
  function partial(P, Q) {
    P = pTrim(P); Q = pTrim(Q);
    var out = { div: null }, D = pDivide(P, Q), R = D.r;
    if (pDeg(P) >= pDeg(Q)) out.div = D.q;
    var Fq = factorQ(Q);
    if (pDeg(Fq.rest) > 2 || (pDeg(Fq.rest) === 2 && (function () { var c = Fq.rest, d = c[1].mul(c[1]).sub(new Fr(4).mul(c[2]).mul(c[0])); return d.val() >= 0; })())) return null;
    var lead = Fq.rest[pDeg(Fq.rest)], quad = pDeg(Fq.rest) === 2 ? Fq.rest.map(function (c) { return c.div(lead); }) : null;
    // arrels amb multiplicitat
    var mult = []; Fq.roots.forEach(function (r) { var e = mult.filter(function (m) { return m.r.sub(r).zero(); })[0]; if (e) e.m++; else mult.push({ r: r, m: 1 }); });
    mult.sort(function (a, b) { return a.r.val() - b.r.val(); });
    var Qm = Q.map(function (c) { return c.div(lead); }), Rm = R.map(function (c) { return c.div(lead); }), n = pDeg(Qm), cols = [], terms = [];
    mult.forEach(function (e) { for (var k = 1; k <= e.m; k++) { var dv = [new Fr(1)]; for (var j = 0; j < k; j++) dv = pMul(dv, [new Fr(-e.r.n, e.r.d), new Fr(1)]); cols.push(pDivide(Qm, dv).q); terms.push({ r: e.r, k: k }); } });
    if (quad) { var qq = pDivide(Qm, quad).q; cols.push(pMul(qq, [new Fr(0), new Fr(1)])); terms.push({ q: "M" }); cols.push(qq); terms.push({ q: "N" }); }
    var A = [], b = [];
    for (var i = 0; i < n; i++) { A.push(cols.map(function (c) { return c[i] || new Fr(0); })); b.push(Rm[i] || new Fr(0)); }
    var sol = solveLin(A, b); if (!sol) return null;
    terms.forEach(function (t, i) { t.c = sol[i]; });
    out.terms = terms; out.mult = mult; out.quad = quad; out.lead = lead; out.R = R;
    return out;
  }
  function wRat() {
    var w = document.getElementById("w-rat"); if (!w) return;
    var PRE = [["1", "x^2-1"], ["2x+3", "x^2+x-2"], ["x^3+1", "x^2-1"], ["x+5", "(x-1)^2(x+2)"], ["1", "x^3+x"], ["3x+1", "x^2+2x+5"], ["x^2+2", "x(x+1)^2"]];
    var Pi = $(w, "p"), Qi = $(w, "q"), out = $(w, "out"), svg = w.querySelector("svg.lp-svg");
    presetBtns($(w, "presets"), PRE.length, "pRat", function (i) { Pi.value = PRE[i][0]; Qi.value = PRE[i][1]; draw(); });
    [Pi, Qi].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var P, Q;
      try { P = pTrim(polyOf(parse(Pi.value))); Q = pTrim(polyOf(parse(Qi.value))); Pi.classList.remove("bad"); Qi.classList.remove("bad"); } catch (e) { out.textContent = u("ratBad"); return; }
      if (pDeg(Q) < 1) { out.textContent = u("ratBad"); return; }
      var S = partial(P, Q), h = "<p>" + tex("\\displaystyle\\int\\frac{" + pTex(P) + "}{" + pTex(Q) + "}\\,dx") + "</p>";
      var f = function (x) { return pNumV(P, x) / pNumV(Q, x); };
      if (!S) { out.innerHTML = h + "<p>" + u("ratNo") + "</p>"; plot(svg, { v: [-5, 5, -5, 5], curves: [{ f: f }] }); return; }
      var parts = [], prim = [], first = true;
      if (S.div) { h += "<p>" + u("div") + " " + tex("\\dfrac{" + pTex(P) + "}{" + pTex(Q) + "}=" + pTex(S.div) + "+\\dfrac{" + pTex(S.R) + "}{" + pTex(Q) + "}") + "</p>"; parts.push(pTex(S.div)); prim.push(pTexI(pIntP(S.div))); first = false; }
      var ft = (S.lead.n === 1 && S.lead.d === 1 ? "" : S.lead.tex()) + S.mult.map(function (e) { return (e.r.zero() ? "x" : "\\left(" + linT(e.r) + "\\right)") + (e.m > 1 ? "^{" + e.m + "}" : ""); }).join("") + (S.quad ? "\\left(" + pTex(S.quad) + "\\right)" : "");
      if (S.mult.length) h += "<p>" + u("fact") + " " + tex(pTex(Q) + "=" + ft) + "</p>";
      var dec = [], M = null, N = null, li = S.lead.n === 1 && S.lead.d === 1 ? "" : S.lead.tex();
      S.terms.forEach(function (t) {
        if (t.q === "M") { M = t.c; return; } if (t.q === "N") { N = t.c; return; }
        var den = (t.r.zero() ? "x" : linT(t.r)), denP = t.k > 1 ? (t.r.zero() ? "x" : "\\left(" + den + "\\right)") + "^{" + t.k + "}" : den;
        if (t.c.zero()) return;
        dec.push(fracT(t.c, denP, !dec.length));
        if (t.k === 1) prim.push(coefT(t.c, "\\ln\\left|" + den + "\\right|", !prim.length));
        else { var c2 = t.c.div(new Fr(-(t.k - 1))); prim.push(fracT(c2, denP.replace("^{" + t.k + "}", t.k - 1 > 1 ? "^{" + (t.k - 1) + "}" : ""), !prim.length)); }
      });
      if (S.quad) {
        var p = S.quad[1], q = S.quad[0], num = pTex([N, M]);
        dec.push((dec.length ? "+" : "") + "\\dfrac{" + num + "}{" + pTex(S.quad) + "}");
        var a1 = M.div(new Fr(2)), b1 = N.sub(M.mul(p).div(new Fr(2))), disc = q.sub(p.mul(p).div(new Fr(4))).val(), sq = sqrtTex(disc), half = p.div(new Fr(2));
        if (!a1.zero()) prim.push(coefT(a1, "\\ln\\left(" + pTex(S.quad) + "\\right)", !prim.length));
        if (!b1.zero()) {
          var kk = b1.val() / Math.sqrt(disc), kt = exactTex(kk), arg = "\\dfrac{" + (half.zero() ? "x" : "x" + (half.n > 0 ? "+" : "-") + new Fr(Math.abs(half.n), half.d).tex()) + "}{" + sq + "}";
          if (sq === "1") arg = half.zero() ? "x" : "x" + (half.n > 0 ? "+" : "-") + new Fr(Math.abs(half.n), half.d).tex();
          prim.push((kk < 0 ? "-" : prim.length ? "+" : "") + (Math.abs(kk - 1) < 1e-12 || Math.abs(kk + 1) < 1e-12 ? "" : kt.replace(/^-/, "")) + "\\arctan" + (sq === "1" && half.zero() ? " x" : "\\left(" + arg + "\\right)"));
        }
      }
      var R1 = S.R.map(function (c) { return c.div(S.lead); });
      if (S.mult.length) h += "<p>" + u("dec") + " " + tex("\\dfrac{" + pTex(S.div ? S.R : P) + "}{" + pTex(Q) + "}=" + dec.join("")) + "</p>";
      var sysT = S.terms.map(function (t) { return (t.q ? t.q : t.k > 1 ? "A_{" + nn(t.r.val()) + "," + t.k + "}" : "A_{" + nn(t.r.val()) + "}") + "=" + t.c.tex(); });
      h += '<p class="hint">' + u("sys") + " " + tex(sysT.join(",\\ ")) + "</p>";
      h += "<p><strong>" + u("res") + ":</strong> " + tex("\\displaystyle\\int\\frac{" + pTex(P) + "}{" + pTex(Q) + "}\\,dx=" + prim.join("") + "+C", true) + "</p>";
      out.innerHTML = h;
      var xs = S.mult.map(function (e) { return e.r.val(); }), x0 = Math.min.apply(null, xs.concat([-2])) - 3, x1 = Math.max.apply(null, xs.concat([2])) + 3;
      plot(svg, { v: [x0, x1].concat(autoY([f], x0, x1)), curves: [{ f: f }], va: xs });
    }
    onLang(draw);
  }
  function pNumV(p, x) { var r = 0; for (var i = p.length - 1; i >= 0; i--) r = r * x + p[i].val(); return r; }
  function pIntP(p) { var r = [new Fr(0)]; p.forEach(function (c, k) { r.push(c.div(new Fr(k + 1))); }); return pTrim(r); }
  function pTexI(p) { return pTex(p); }

  /* ---------- 9.7 sumes de Riemann ---------- */
  function wRiem() {
    var w = document.getElementById("w-riem"); if (!w) return;
    var PRE = [["x^2", "0", "2"], ["sin(x)", "0", "pi"], ["4-x^2", "-2", "2"], ["e^x", "0", "1"], ["1/x", "1", "e"]];
    var fi = $(w, "f"), ai = $(w, "a"), bi = $(w, "b"), rn = $(w, "n"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info"), mode = 0, mb = [], box = $(w, "mode");
    ["left", "mid", "rightP"].forEach(function (k, i) { var b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.addEventListener("click", function () { mode = i; draw(); }); box.appendChild(b); mb.push([b, k]); });
    presetBtns($(w, "presets"), PRE.length, "pRiem", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; bi.value = PRE[i][2]; draw(); });
    [fi, ai, bi, rn].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      mb.forEach(function (q, i) { q[0].textContent = u(q[1]); q[0].classList.toggle("on", i === mode); });
      var n = +rn.value; $(w, "nv").textContent = n;
      var nf = readF(fi); if (!nf) { info.textContent = u("bad"); return; }
      var f = compile(nf), a = readLim(ai), b = readLim(bi);
      if (!(isFinite(a) && isFinite(b) && a < b)) { info.textContent = u("aBad"); return; }
      var dx = (b - a) / n, S = 0, rects = [];
      for (var i = 0; i < n; i++) { var xi = a + (i + [0, 0.5, 1][mode]) * dx, y = f(xi); S += y * dx; rects.push({ a: a + i * dx, b: a + (i + 1) * dx, y: y, col: y >= 0 ? "var(--accent-2)" : "var(--bad)" }); }
      var I = integ(f, a, b);
      var h = "<p>" + tex("f(x)=" + texD(nf)) + ", " + tex("[" + nn(a) + "," + nn(b) + "]") + "</p>";
      h += "<p>" + u("width") + ": " + tex("\\Delta x=" + numTex(+dx.toFixed(4))) + "</p>";
      h += '<p class="sum-big">' + u("sum") + ": " + tex("S_{" + n + "}=" + numTex(+S.toFixed(5))) + "</p>";
      h += "<p>" + u("exact") + ": " + tex("\\displaystyle\\int_{" + nn(a) + "}^{" + nn(b) + "}f(x)\\,dx=" + exactA(I)) + "</p>";
      h += "<p>" + u("err") + ": " + tex("|S_{" + n + "}-I|=" + numTex(+Math.abs(S - I).toFixed(5))) + "</p>";
      info.innerHTML = h;
      var pad = (b - a) * 0.12, yy = autoY([f], a - pad, b + pad);
      plot(svg, { v: [a - pad, b + pad, yy[0], yy[1]], curves: [{ f: f }], rects: rects, guides: [{ x: a }, { x: b }] });
    }
    onLang(draw);
  }

  /* ---------- 9.7 regla de Barrow ---------- */
  function signPieces(f, a, b) {
    var rs = roots(f, a, b, 3000).filter(function (r) { return r > a + 1e-9 && r < b - 1e-9; }), cuts = [a].concat(rs).concat([b]), out = [];
    for (var i = 0; i + 1 < cuts.length; i++) out.push({ a: cuts[i], b: cuts[i + 1], v: integ(f, cuts[i], cuts[i + 1]) });
    return out;
  }
  function wBarrow() {
    var w = document.getElementById("w-barrow"); if (!w) return;
    var PRE = [["x^2-1", "x^3/3-x", "0", "2"], ["sin(x)", "-cos(x)", "0", "2pi"], ["1/x", "ln(x)", "1", "e"], ["x*e^x", "(x-1)e^x", "0", "1"], ["1/(1+x^2)", "arctan(x)", "0", "1"], ["cos(x)^2", "x/2+sin(2x)/4", "0", "pi"]];
    var fi = $(w, "f"), Fi = $(w, "F"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pBar", function (i) { fi.value = PRE[i][0]; Fi.value = PRE[i][1]; ai.value = PRE[i][2]; bi.value = PRE[i][3]; draw(); });
    [fi, Fi, ai, bi].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var nf = readF(fi); if (!nf) { info.textContent = u("bad"); return; }
      var f = compile(nf), a = readLim(ai), b = readLim(bi);
      if (!(isFinite(a) && isFinite(b) && a < b)) { info.textContent = u("aBad"); return; }
      var I = integ(f, a, b), h = "<p>" + tex("\\displaystyle\\int_{" + nn(a) + "}^{" + nn(b) + "}" + texD(nf) + "\\,dx") + "</p>";
      if (String(Fi.value).trim()) {
        var nF = readF(Fi);
        if (nF) {
          var G = compile(nF), Ga = G(a), Gb = G(b);
          h += chkHtml(G, f, a, b);
          h += "<p><strong>" + u("barrow") + ":</strong> " + tex("\\Big[" + texD(nF) + "\\Big]_{" + nn(a) + "}^{" + nn(b) + "}=F(" + nn(b) + ")-F(" + nn(a) + ")=" + exactTex(Gb) + "-" + (Ga < 0 ? "\\left(" + exactTex(Ga) + "\\right)" : exactTex(Ga)) + "=" + exactA(Gb - Ga)) + "</p>";
        }
      } else h += '<p class="hint">' + u("noF") + "</p>";
      h += "<p>" + u("num") + ": " + tex(numTex(+I.toFixed(6))) + "</p>";
      var pcs = signPieces(f, a, b), Ap = 0, An = 0, fill = [];
      pcs.forEach(function (q) { if (q.v >= 0) Ap += q.v; else An -= q.v; fill.push({ f: f, a: q.a, b: q.b, col: q.v >= 0 ? "var(--ok)" : "var(--bad)" }); });
      if (An > 1e-9 && Ap > 1e-9) h += "<p>" + u("signed") + " " + tex(exactTex(Ap) + "-" + exactTex(An) + "=" + exactTex(Ap - An)) + "</p>";
      info.innerHTML = h;
      var pad = (b - a) * 0.15, yy = autoY([f], a - pad, b + pad);
      plot(svg, { v: [a - pad, b + pad, yy[0], yy[1]], curves: [{ f: f }], fill: fill, guides: [{ x: a }, { x: b }] });
    }
    onLang(draw);
  }

  /* ---------- 9.8 funció integral ---------- */
  function wFtc() {
    var w = document.getElementById("w-ftc"); if (!w) return;
    var PRE = [["t", "0"], ["sin(t)", "0"], ["e^(-t^2)", "0"], ["t^2-1", "0"], ["1/t", "1"]];
    var fi = $(w, "f"), ai = $(w, "a"), rx = $(w, "x"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pFtc", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; draw(); });
    [fi, ai, rx].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var nf = readF(fi); if (!nf) { info.textContent = u("bad"); return; }
      var f = compile(nf), a = readLim(ai); if (!isFinite(a)) { info.textContent = u("aBad"); return; }
      var lo = a - 3, hi = a + 4, t;
      for (t = a; t > a - 3; t -= 0.01) if (!isFinite(f(t))) { lo = t + 0.02; break; }
      for (t = a; t < a + 4; t += 0.01) if (!isFinite(f(t))) { hi = t - 0.02; break; }
      rx.min = lo; rx.max = hi; rx.step = (hi - lo) / 400;
      var x = Math.min(hi, Math.max(lo, +rx.value)); $(w, "xv").textContent = numTxt(+x.toFixed(2));
      function Fi(t) { return t >= a ? integ(f, a, t) : -integ(f, t, a); }
      var Fx = Fi(x), FT = [], M = 160; for (var i = 0; i <= M; i++) { var t = lo + (hi - lo) * i / M; FT.push([t, Fi(t)]); }
      function Fp(t) { var k = Math.min(M - 1, Math.max(0, Math.floor((t - lo) / (hi - lo) * M))), r = (t - FT[k][0]) / (FT[k + 1][0] - FT[k][0]); return FT[k][1] + (FT[k + 1][1] - FT[k][1]) * r; }
      var h = "<p>" + tex("F(x)=\\displaystyle\\int_{" + nn(a) + "}^{x}" + texD(nf).replace(/x/g, "t") + "\\,dt") + "</p>";
      h += "<p>" + tex("F(" + numTex(+x.toFixed(2)) + ")\\approx" + numTex(+Fx.toFixed(4))) + "</p><p>" + u("ftcD") + " " + tex("F'(x)=f(x)") + "; " + tex("F'(" + numTex(+x.toFixed(2)) + ")=f(" + numTex(+x.toFixed(2)) + ")\\approx" + numTex(+f(x).toFixed(4))) + "</p>";
      info.innerHTML = h;
      var yy = autoY([f, Fp], lo, hi);
      plot(svg, { v: [lo, hi, yy[0], yy[1]], curves: [{ f: f, col: "var(--accent)" }, { f: Fp, col: "var(--r3)" }], fill: [{ f: f, a: Math.min(a, x), b: Math.max(a, x), col: x >= a ? "var(--ok)" : "var(--bad)" }], pts: [{ x: x, y: Fx, col: "var(--r3)" }], guides: [{ x: x }, { x: a }] });
    }
    onLang(draw);
  }

  /* ---------- 9.9 i 9.10 àrees ---------- */
  function readPair(s) {
    // «f i g en [a, b]» → parts; acceptem «;» com a separador
    return s;
  }
  function areaCalc(h, A, B, x0, x1) {
    var cuts;
    if (A !== null && B !== null) { cuts = [A].concat(roots(h, A, B, 4000).filter(function (r) { return r > A + 1e-9 && r < B - 1e-9; })).concat([B]); }
    else { cuts = roots(h, x0, x1, 6000); if (cuts.length < 2) return { err: true, cuts: cuts }; }
    var pcs = [];
    for (var i = 0; i + 1 < cuts.length; i++) pcs.push({ a: cuts[i], b: cuts[i + 1], v: integ(h, cuts[i], cuts[i + 1]) });
    var tot = pcs.reduce(function (s, q) { return s + Math.abs(q.v); }, 0);
    return { cuts: cuts, pieces: pcs, total: tot, lim: A !== null };
  }
  function wArea(id, PRE, key, two, opt) {
    var w = document.getElementById(id); if (!w) return;
    var fi = $(w, "f"), gi = $(w, "g"), ai = $(w, "a"), bi = $(w, "b"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, key, function (i) { fi.value = PRE[i][0]; if (gi) gi.value = PRE[i][1] || ""; ai.value = PRE[i][2] || ""; bi.value = PRE[i][3] || ""; draw(); });
    [fi, gi, ai, bi].forEach(function (el) { if (el) el.addEventListener("input", draw); });
    function draw() {
      var nf = readF(fi); if (!nf) { info.textContent = u("bad"); return; }
      var f = compile(nf), ng = null, g = null;
      if (gi && String(gi.value).trim()) { ng = readF(gi); if (!ng) { info.textContent = u("bad"); return; } g = compile(ng); }
      var A = readLim(ai), B = readLim(bi);
      if (A === undefined || B === undefined || (A !== null) !== (B !== null) || (A !== null && !(A < B))) { info.textContent = u("aBad"); return; }
      var hfn = g ? function (x) { return f(x) - g(x); } : f;
      var R = areaCalc(hfn, A, B, -12, 12), ftx = texD(nf), gtx = ng ? texD(ng) : "0";
      var h = "<p>" + tex("f(x)=" + ftx) + (ng ? "&ensp;" + tex("g(x)=" + gtx) : "") + "</p>";
      if (R.err) { info.innerHTML = h + "<p>" + u("noCut") + "</p>"; plot(svg, { v: [-6, 6].concat(autoY(g ? [f, g] : [f], -6, 6)), curves: [{ f: f }].concat(g ? [{ f: g, col: "var(--r3)" }] : []) }); return; }
      h += "<p><strong>" + (R.lim ? u("limits") : g ? u("cutsFG") : u("cutsX")) + ":</strong> " + tex(R.cuts.map(function (c) { return "x=" + nn(c); }).join(",\\ ")) + "</p>";
      h += "<p><strong>" + u("pieces") + ":</strong></p><ul>" + R.pieces.map(function (q) {
        return "<li>" + tex("\\displaystyle\\int_{" + nn(q.a) + "}^{" + nn(q.b) + "}" + (g ? "\\left(f-g\\right)" : "f") + "\\,dx" + eqT(q.v)) + (q.v < 0 ? " → " + tex("|\\cdot|" + eqT(-q.v)) : "") + "</li>";
      }).join("") + "</ul>";
      h += '<p class="sum-big">' + u("total") + ": " + tex("A" + (exactA(R.total).indexOf("\\approx") === 0 ? "" : "=") + exactA(R.total) + "\\ \\text{u}^2") + "</p>";
      info.innerHTML = h;
      var lo = R.cuts[0], hi = R.cuts[R.cuts.length - 1], pad = Math.max(0.6, (hi - lo) * 0.18), fs = g ? [f, g] : [f], yy = autoY(fs, lo - pad, hi + pad, 0.12), fill = [];
      R.pieces.forEach(function (q) { fill.push({ f: f, g: g, a: q.a, b: q.b, col: two ? "var(--accent-2)" : q.v >= 0 ? "var(--ok)" : "var(--bad)" }); });
      var pts = R.cuts.map(function (c) { return { x: c, y: f(c), col: "var(--text)" }; });
      plot(svg, { v: [lo - pad, hi + pad, yy[0], yy[1]], curves: [{ f: f }].concat(g ? [{ f: g, col: "var(--r3)" }] : []), fill: fill, pts: pts, guides: R.lim ? [{ x: lo }, { x: hi }] : [] });
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("Si $F'(x)=f(x)$, quina d'aquestes també és una primitiva de $f$?", "Si $F'(x)=f(x)$, ¿cuál de estas también es una primitiva de $f$?", "If $F'(x)=f(x)$, which of these is also an antiderivative of $f$?"),
      o: [q3("$F(x)+7$"), q3("$7F(x)$"), q3("$F(x+7)$")], a: 0, e: q3("Les primitives es diferencien en una constant: $(F+7)'=F'=f$.", "Las primitivas se diferencian en una constante: $(F+7)'=F'=f$.", "Antiderivatives differ by a constant: $(F+7)'=F'=f$.") },
    { q: q3("$\\displaystyle\\int\\frac{dx}{\\cos^2x}=$", "$\\displaystyle\\int\\frac{dx}{\\cos^2x}=$", "$\\displaystyle\\int\\frac{dx}{\\cos^2x}=$"),
      o: [q3("$\\tan x+C$"), q3("$-\\frac{1}{\\cos x}+C$"), q3("$\\frac{\\sin x}{\\cos^3x}+C$")], a: 0, e: q3("$(\\tan x)'=\\frac{1}{\\cos^2x}=1+\\tan^2x$.") },
    { q: q3("$\\displaystyle\\int\\sin(3x)\\,dx=$", "$\\displaystyle\\int\\sin(3x)\\,dx=$", "$\\displaystyle\\int\\sin(3x)\\,dx=$"),
      o: [q3("$-3\\cos3x+C$"), q3("$-\\frac13\\cos3x+C$"), q3("$\\frac13\\cos3x+C$")], a: 1, e: q3("Falta el 3 de la derivada de dins: $\\frac13\\int3\\sin3x\\,dx=-\\frac13\\cos3x+C$.", "Falta el 3 de la derivada de dentro: $\\frac13\\int3\\sin3x\\,dx=-\\frac13\\cos3x+C$.", "The inner derivative 3 is missing: $\\frac13\\int3\\sin3x\\,dx=-\\frac13\\cos3x+C$.") },
    { q: q3("$\\displaystyle\\int\\frac{dx}{4+x^2}=$", "$\\displaystyle\\int\\frac{dx}{4+x^2}=$", "$\\displaystyle\\int\\frac{dx}{4+x^2}=$"),
      o: [q3("$\\ln(4+x^2)+C$"), q3("$\\frac12\\arctan\\frac x2+C$"), q3("$\\arctan\\frac x2+C$")], a: 1, e: q3("$\\frac{1}{4}\\int\\frac{dx}{1+(x/2)^2}=\\frac14\\cdot2\\arctan\\frac x2$.") },
    { q: q3("$\\displaystyle\\int\\tan x\\,dx=$", "$\\displaystyle\\int\\tan x\\,dx=$", "$\\displaystyle\\int\\tan x\\,dx=$"),
      o: [q3("$-\\ln|\\cos x|+C$"), q3("$\\frac{\\tan^2x}{2}+C$"), q3("$\\ln|\\sin x|+C$")], a: 0, e: q3("$\\tan x=\\frac{\\sin x}{\\cos x}=-\\frac{(\\cos x)'}{\\cos x}$: és del tipus $\\frac{u'}{u}$.", "$\\tan x=\\frac{\\sin x}{\\cos x}=-\\frac{(\\cos x)'}{\\cos x}$: es del tipo $\\frac{u'}{u}$.", "$\\tan x=\\frac{\\sin x}{\\cos x}=-\\frac{(\\cos x)'}{\\cos x}$: it is of the form $\\frac{u'}{u}$.") },
    { q: q3("Per a $\\int x^2\\ln x\\,dx$ per parts, convé prendre…", "Para $\\int x^2\\ln x\\,dx$ por partes, conviene tomar…", "For $\\int x^2\\ln x\\,dx$ by parts, it is best to take…"),
      o: [q3("$u=x^2$, $dv=\\ln x\\,dx$"), q3("$u=\\ln x$, $dv=x^2dx$"), q3("$u=x^2\\ln x$, $dv=dx$")], a: 1, e: q3("El logaritme es deriva ($\\frac1x$) i la potència s'integra fàcilment: $\\frac{x^3}{3}\\ln x-\\int\\frac{x^2}{3}\\,dx$.", "El logaritmo se deriva ($\\frac1x$) y la potencia se integra fácilmente: $\\frac{x^3}{3}\\ln x-\\int\\frac{x^2}{3}\\,dx$.", "Differentiate the logarithm ($\\frac1x$) and integrate the power: $\\frac{x^3}{3}\\ln x-\\int\\frac{x^2}{3}\\,dx$.") },
    { q: q3("$\\displaystyle\\int\\frac{dx}{x^2-1}=$", "$\\displaystyle\\int\\frac{dx}{x^2-1}=$", "$\\displaystyle\\int\\frac{dx}{x^2-1}=$"),
      o: [q3("$\\ln|x^2-1|+C$"), q3("$\\frac12\\ln\\left|\\frac{x-1}{x+1}\\right|+C$"), q3("$\\arctan x+C$")], a: 1, e: q3("$\\frac{1}{x^2-1}=\\frac{1/2}{x-1}-\\frac{1/2}{x+1}$.") },
    { q: q3("Si el denominador té una arrel doble $x=a$, la descomposició inclou…", "Si el denominador tiene una raíz doble $x=a$, la descomposición incluye…", "If the denominator has a double root $x=a$, the decomposition includes…"),
      o: [q3("$\\frac{A}{x-a}$ només", "$\\frac{A}{x-a}$ solo", "$\\frac{A}{x-a}$ only"), q3("$\\frac{A}{x-a}+\\frac{B}{(x-a)^2}$"), q3("$\\frac{Ax+B}{(x-a)^2}$ i res més", "$\\frac{Ax+B}{(x-a)^2}$ y nada más", "$\\frac{Ax+B}{(x-a)^2}$ and nothing else")], a: 1, e: q3("I $\\int\\frac{B}{(x-a)^2}dx=-\\frac{B}{x-a}$.", "Y $\\int\\frac{B}{(x-a)^2}dx=-\\frac{B}{x-a}$.", "And $\\int\\frac{B}{(x-a)^2}dx=-\\frac{B}{x-a}$.") },
    { q: q3("$\\displaystyle\\int_0^{2\\pi}\\sin x\\,dx$ val…", "$\\displaystyle\\int_0^{2\\pi}\\sin x\\,dx$ vale…", "$\\displaystyle\\int_0^{2\\pi}\\sin x\\,dx$ equals…"),
      o: [q3("$0$"), q3("$4$"), q3("$2$")], a: 0, e: q3("La part positiva i la negativa es compensen; l'<strong>àrea</strong> sí que és 4.", "La parte positiva y la negativa se compensan; el <strong>área</strong> sí es 4.", "The positive and negative parts cancel; the <strong>area</strong> is 4.") },
    { q: q3("Si $F(x)=\\displaystyle\\int_0^{x^2}e^{t^2}dt$, aleshores $F'(x)=$", "Si $F(x)=\\displaystyle\\int_0^{x^2}e^{t^2}dt$, entonces $F'(x)=$", "If $F(x)=\\displaystyle\\int_0^{x^2}e^{t^2}dt$, then $F'(x)=$"),
      o: [q3("$e^{x^4}$"), q3("$2x\\,e^{x^4}$"), q3("$e^{x^2}$")], a: 1, e: q3("Teorema fonamental i regla de la cadena: $F'(x)=f(x^2)\\cdot2x$.", "Teorema fundamental y regla de la cadena: $F'(x)=f(x^2)\\cdot2x$.", "Fundamental theorem and chain rule: $F'(x)=f(x^2)\\cdot2x$.") },
    { q: q3("L'àrea tancada entre $y=x^2$ i $y=x$ és…", "El área encerrada entre $y=x^2$ e $y=x$ es…", "The area enclosed between $y=x^2$ and $y=x$ is…"),
      o: [q3("$\\frac16$"), q3("$\\frac13$"), q3("$\\frac12$")], a: 0, e: q3("$\\int_0^1(x-x^2)\\,dx=\\frac12-\\frac13=\\frac16$.") },
    { q: q3("Per a calcular l'àrea entre $f$ i l'eix OX en $[a,b]$ quan $f$ canvia de signe…", "Para calcular el área entre $f$ y el eje OX en $[a,b]$ cuando $f$ cambia de signo…", "To compute the area between $f$ and the x-axis on $[a,b]$ when $f$ changes sign…"),
      o: [q3("calculem $\\int_a^bf$ directament", "calculamos $\\int_a^bf$ directamente", "compute $\\int_a^bf$ directly"), q3("separem en trossos pels zeros i sumem els valors absoluts", "separamos en trozos por los ceros y sumamos los valores absolutos", "split at the zeros and add the absolute values"), q3("calculem $\\left|\\int_a^bf\\right|$", "calculamos $\\left|\\int_a^bf\\right|$", "compute $\\left|\\int_a^bf\\right|$")], a: 1, e: q3("Si no, les parts de davall de l'eix restarien.", "Si no, las partes de debajo del eje restarían.", "Otherwise, the parts below the axis would subtract.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Integrals · FentMates", es: "Integrales · FentMates", en: "Integrals · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }
  function wStudies() {
    wChk("w-chk1", [["x^4", "x^5/5"], ["1/x", "ln(abs(x))"], ["sin(x)", "cos(x)"], ["1/cos(x)^2", "tan(x)"], ["1/sqrt(1-x^2)", "arcsin(x)"], ["2^x", "2^x/ln(2)"]], "pChk1");
    wChk("w-chk2", [["(2x+1)^3", "(2x+1)^4/8"], ["(2x+1)^3", "(2x+1)^4/4"], ["x/(x^2+1)", "ln(x^2+1)"], ["sin(x)*cos(x)^2", "-cos(x)^3/3"], ["e^(sin(x))*cos(x)", "e^(sin(x))"], ["1/(4+x^2)", "arctan(x/2)/2"], ["tan(x)", "-ln(abs(cos(x)))"]], "pChk2");
    wArea("w-area1", [["x^2-4"], ["x^3-4x"], ["sin(x)", "", "0", "2pi"], ["x*e^x", "", "-1", "1"], ["ln(x)", "", "1/e", "e"], ["4x-x^3"]], "pA1", false);
    wArea("w-area2", [["x^2", "x+2"], ["x^2", "sqrt(x)"], ["x^3", "x"], ["sin(x)", "cos(x)", "pi/4", "5pi/4"], ["e^x", "e", "0", "1"], ["6x-x^2", "x^2-2x"], ["4/x", "5-x"]], "pA2", true);
    wArea("w-lab", [["x^2", "2x"], ["x^3-3x"], ["sin(x)", "", "0", "pi"], ["ln(x)", "", "1", "e"], ["x*e^x", "x", "0", "2"], ["1/(1+x^2)", "x^2/2"]], "pLab", true);
  }

  function init() {
    document.title = TITLES[lang];
    var Dl = [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, { delimiters: Dl, ignoredClasses: ["widget", "lab"], throwOnError: false });
      document.querySelectorAll(".widget .wt, .widget label, .widget .ttl, .widget .legend, .lab label, .lab .legend").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFam, wSub, wParts, wRat, wRiem, wBarrow, wFtc, wStudies, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM9 = { parse: parse, compile: compile, partial: partial, exactTex: exactTex, integ: integ, nn: nn };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
