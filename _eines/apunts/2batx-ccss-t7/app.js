(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-u7-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt", pc: "si", rest: "en la resta",
      bad: "No entenc l'expressió: revisa-la.", noDiff: "Aquesta expressió no la sé derivar amb les regles de la unitat.",
      test: "Valor de prova", noDom: "fora del domini", mx: "màx", mn: "mín", incOn: "Creixent en", decOn: "Decreixent en",
      noCrit: "No hi ha cap punt on f′(x) = 0.", maxR: "Màxim relatiu", minR: "Mínim relatiu", noExt: "no és extrem", inc: "creixent", dec: "decreixent",
      cont: "contínua", ev: "evitable", sf: "salt finit", si: "salt infinit", as: "asimptòtica",
      dom: "Domini", den: "Denominador", denZ: "s'anul·la en", denNo: "no s'anul·la mai", lnArg: "Argument del logaritme", lnPos: "ha de ser positiu",
      sqArg: "Dins de l'arrel", sqPos: "no pot ser negatiu", empty: "La funció no existeix per a cap x de la finestra.", noCond: "No hi ha denominadors ni logaritmes: cap restricció.",
      cutX: "Talls amb l'eix OX", cutY: "Tall amb l'eix OY", noCutX: "no talla l'eix OX", noCutY: "no talla l'eix OY (x = 0 no és del domini)",
      sym: "Simetria", even: "parella: simètrica respecte de l'eix OY", odd: "senar: simètrica respecte de l'origen", noSym: "ni parella ni senar", symNoDom: "el domini no és simètric",
      av: "Asímptotes verticals", noAV: "no en té", ah: "Asímptota horitzontal", ao: "Asímptota obliqua", noAsy: "ni horitzontal ni obliqua", branch: "branca parabòlica",
      toL: "quan x → −∞", toR: "quan x → +∞", notTo: "el domini no hi arriba", poly: "És una funció polinòmica: no té asímptotes.",
      quo: "Quocient", rem: "Residu", divide: "Dividim", mult: "multipliquem", subt: "restem",
      dLt: "grau P < grau Q ⇒ asímptota horitzontal y = 0", dEq: "grau P = grau Q ⇒ asímptota horitzontal (quocient dels coeficients principals)",
      dP1: "grau P = grau Q + 1 ⇒ asímptota obliqua: el quocient C(x)", dBig: "grau P > grau Q + 1 ⇒ ni horitzontal ni obliqua (branca parabòlica)",
      above: "la funció queda per damunt de l'asímptota", below: "la funció queda per davall de l'asímptota", notPoly: "Escriu dos polinomis (el denominador no pot ser constant 0).",
      mono: "Monotonia", ext: "Extrems relatius", none: "cap", value: "Valor",
      sNames: ["Domini", "Punts de tall", "Simetria", "Asímptotes", "Monotonia i extrems", "Gràfica"],
      many: "Hi ha molts punts crítics: mostrem l'estudi en la finestra", piece: "Tros", atCut: "En", contAll: "És contínua en tot el domini.",
      latL: "límit per l'esquerra", latR: "límit per la dreta", val: "valor", noExtPw: "No té extrems relatius.",
      pDom: ["Polinòmica", "(x + 1)/(x² − 4)", "1/(x² + 1)", "e^(1/x)", "ln(x − 3)", "ln(x² − 4)", "x / ln x"],
      pCut: ["x³ − 4x", "x² − 2x − 3", "(x² − 1)/(x + 2)", "eˣ − 2", "ln(x + 1)", "x²·eˣ"],
      pSym: ["x⁴ − 3x²", "x³ − 3x", "x/(x² + 1)", "x²/(x² − 1)", "e^(−x²)", "eˣ", "x² + x"],
      pAsy: ["(2x + 1)/(x − 3)", "x/(x² − 1)", "3x²/(x² + 1)", "2 − e⁻ˣ", "ln(x + 2)", "(x² + 1)/x"],
      pObl: ["(x² + 3)/(x − 1)", "x²/(x + 1)", "(2x² − x + 1)/x", "x³/(x² − 1)", "(x³ + 1)/x", "(3x² + 1)/(x² − 4)"],
      pMx: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "x·eˣ", "ln x / x"],
      pEl: ["a·eˣ⁻ʰ + k", "a·(1/2)ˣ⁻ʰ + k", "a·ln(x − h) + k"],
      pPw: ["Exemple resolt", "Amb un salt", "Exponencial i logaritme", "Racional i recta"],
      pLab: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "(2x − 1)/(x + 1)", "x·eˣ", "eˣ/x", "ln x / x"] },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba", pc: "si", rest: "en el resto",
      bad: "No entiendo la expresión: revísala.", noDiff: "Esta expresión no la sé derivar con las reglas de la unidad.",
      test: "Valor de prueba", noDom: "fuera del dominio", mx: "máx", mn: "mín", incOn: "Creciente en", decOn: "Decreciente en",
      noCrit: "No hay ningún punto donde f′(x) = 0.", maxR: "Máximo relativo", minR: "Mínimo relativo", noExt: "no es extremo", inc: "creciente", dec: "decreciente",
      cont: "continua", ev: "evitable", sf: "salto finito", si: "salto infinito", as: "asintótica",
      dom: "Dominio", den: "Denominador", denZ: "se anula en", denNo: "no se anula nunca", lnArg: "Argumento del logaritmo", lnPos: "tiene que ser positivo",
      sqArg: "Dentro de la raíz", sqPos: "no puede ser negativo", empty: "La función no existe para ninguna x de la ventana.", noCond: "No hay denominadores ni logaritmos: ninguna restricción.",
      cutX: "Cortes con el eje OX", cutY: "Corte con el eje OY", noCutX: "no corta el eje OX", noCutY: "no corta el eje OY (x = 0 no es del dominio)",
      sym: "Simetría", even: "par: simétrica respecto del eje OY", odd: "impar: simétrica respecto del origen", noSym: "ni par ni impar", symNoDom: "el dominio no es simétrico",
      av: "Asíntotas verticales", noAV: "no tiene", ah: "Asíntota horizontal", ao: "Asíntota oblicua", noAsy: "ni horizontal ni oblicua", branch: "rama parabólica",
      toL: "cuando x → −∞", toR: "cuando x → +∞", notTo: "el dominio no llega", poly: "Es una función polinómica: no tiene asíntotas.",
      quo: "Cociente", rem: "Resto", divide: "Dividimos", mult: "multiplicamos", subt: "restamos",
      dLt: "grado P < grado Q ⇒ asíntota horizontal y = 0", dEq: "grado P = grado Q ⇒ asíntota horizontal (cociente de los coeficientes principales)",
      dP1: "grado P = grado Q + 1 ⇒ asíntota oblicua: el cociente C(x)", dBig: "grado P > grado Q + 1 ⇒ ni horizontal ni oblicua (rama parabólica)",
      above: "la función queda por encima de la asíntota", below: "la función queda por debajo de la asíntota", notPoly: "Escribe dos polinomios (el denominador no puede ser constante 0).",
      mono: "Monotonía", ext: "Extremos relativos", none: "ninguno", value: "Valor",
      sNames: ["Dominio", "Puntos de corte", "Simetría", "Asíntotas", "Monotonía y extremos", "Gráfica"],
      many: "Hay muchos puntos críticos: mostramos el estudio en la ventana", piece: "Trozo", atCut: "En", contAll: "Es continua en todo el dominio.",
      latL: "límite por la izquierda", latR: "límite por la derecha", val: "valor", noExtPw: "No tiene extremos relativos.",
      pDom: ["Polinómica", "(x + 1)/(x² − 4)", "1/(x² + 1)", "e^(1/x)", "ln(x − 3)", "ln(x² − 4)", "x / ln x"],
      pCut: ["x³ − 4x", "x² − 2x − 3", "(x² − 1)/(x + 2)", "eˣ − 2", "ln(x + 1)", "x²·eˣ"],
      pSym: ["x⁴ − 3x²", "x³ − 3x", "x/(x² + 1)", "x²/(x² − 1)", "e^(−x²)", "eˣ", "x² + x"],
      pAsy: ["(2x + 1)/(x − 3)", "x/(x² − 1)", "3x²/(x² + 1)", "2 − e⁻ˣ", "ln(x + 2)", "(x² + 1)/x"],
      pObl: ["(x² + 3)/(x − 1)", "x²/(x + 1)", "(2x² − x + 1)/x", "x³/(x² − 1)", "(x³ + 1)/x", "(3x² + 1)/(x² − 4)"],
      pMx: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "x·eˣ", "ln x / x"],
      pEl: ["a·eˣ⁻ʰ + k", "a·(1/2)ˣ⁻ʰ + k", "a·ln(x − h) + k"],
      pPw: ["Ejemplo resuelto", "Con un salto", "Exponencial y logaritmo", "Racional y recta"],
      pLab: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "(2x − 1)/(x + 1)", "x·eˣ", "eˣ/x", "ln x / x"] },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top", pc: "if", rest: "otherwise",
      bad: "I can't read that expression: check it.", noDiff: "I can't differentiate this with the rules of the unit.",
      test: "Test value", noDom: "outside the domain", mx: "max", mn: "min", incOn: "Increasing on", decOn: "Decreasing on",
      noCrit: "There is no point where f′(x) = 0.", maxR: "Relative maximum", minR: "Relative minimum", noExt: "not an extremum", inc: "increasing", dec: "decreasing",
      cont: "continuous", ev: "removable", sf: "finite jump", si: "infinite jump", as: "asymptotic",
      dom: "Domain", den: "Denominator", denZ: "is zero at", denNo: "is never zero", lnArg: "Argument of the logarithm", lnPos: "must be positive",
      sqArg: "Inside the root", sqPos: "cannot be negative", empty: "The function does not exist for any x in the window.", noCond: "No denominators or logarithms: no restrictions.",
      cutX: "x-intercepts", cutY: "y-intercept", noCutX: "it does not cross the x-axis", noCutY: "it does not cross the y-axis (x = 0 is not in the domain)",
      sym: "Symmetry", even: "even: symmetric about the y-axis", odd: "odd: symmetric about the origin", noSym: "neither even nor odd", symNoDom: "the domain is not symmetric",
      av: "Vertical asymptotes", noAV: "none", ah: "Horizontal asymptote", ao: "Oblique asymptote", noAsy: "neither horizontal nor oblique", branch: "parabolic branch",
      toL: "as x → −∞", toR: "as x → +∞", notTo: "the domain does not reach it", poly: "It is a polynomial: it has no asymptotes.",
      quo: "Quotient", rem: "Remainder", divide: "Divide", mult: "multiply", subt: "subtract",
      dLt: "deg P < deg Q ⇒ horizontal asymptote y = 0", dEq: "deg P = deg Q ⇒ horizontal asymptote (ratio of the leading coefficients)",
      dP1: "deg P = deg Q + 1 ⇒ oblique asymptote: the quotient C(x)", dBig: "deg P > deg Q + 1 ⇒ neither horizontal nor oblique (parabolic branch)",
      above: "the function lies above the asymptote", below: "the function lies below the asymptote", notPoly: "Type two polynomials (the denominator cannot be the constant 0).",
      mono: "Monotonicity", ext: "Relative extrema", none: "none", value: "Value",
      sNames: ["Domain", "Intercepts", "Symmetry", "Asymptotes", "Monotonicity and extrema", "Graph"],
      many: "There are many critical points: the study is shown for the window", piece: "Piece", atCut: "At", contAll: "It is continuous on its whole domain.",
      latL: "left-hand limit", latR: "right-hand limit", val: "value", noExtPw: "It has no relative extrema.",
      pDom: ["Polynomial", "(x + 1)/(x² − 4)", "1/(x² + 1)", "e^(1/x)", "ln(x − 3)", "ln(x² − 4)", "x / ln x"],
      pCut: ["x³ − 4x", "x² − 2x − 3", "(x² − 1)/(x + 2)", "eˣ − 2", "ln(x + 1)", "x²·eˣ"],
      pSym: ["x⁴ − 3x²", "x³ − 3x", "x/(x² + 1)", "x²/(x² − 1)", "e^(−x²)", "eˣ", "x² + x"],
      pAsy: ["(2x + 1)/(x − 3)", "x/(x² − 1)", "3x²/(x² + 1)", "2 − e⁻ˣ", "ln(x + 2)", "(x² + 1)/x"],
      pObl: ["(x² + 3)/(x − 1)", "x²/(x + 1)", "(2x² − x + 1)/x", "x³/(x² − 1)", "(x³ + 1)/x", "(3x² + 1)/(x² − 4)"],
      pMx: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "x·eˣ", "ln x / x"],
      pEl: ["a·eˣ⁻ʰ + k", "a·(1/2)ˣ⁻ʰ + k", "a·ln(x − h) + k"],
      pPw: ["Worked example", "With a jump", "Exponential and log", "Rational and line"],
      pLab: ["x³ − 6x² + 9x", "x⁴ − 2x²", "x²/(x² − 4)", "(x² + 3)/(x − 1)", "(2x − 1)/(x + 1)", "x·eˣ", "eˣ/x", "ln x / x"] }
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
  /*@@DERIV@@*/
  /*@@STUDY@@*/
  /* ---------- domini (numèricament, amb l'ajuda de l'expressió) ---------- */
  var XL = 40; // finestra d'estudi: [−40, 40]
  // denominadors, arguments de logaritmes i d'arrels de l'expressió
  function condsOf(n, out) {
    out = out || { den: [], ln: [], sq: [] };
    if (!n || typeof n !== "object") return out;
    if (n.t === "/") out.den.push(n.b);
    if (n.t === "f" && (n.n === "ln" || n.n === "log")) out.ln.push(n.a);
    if (n.t === "f" && n.n === "sqrt") out.sq.push(n.a);
    if (n.a) condsOf(n.a, out);
    if (n.b) condsOf(n.b, out);
    return out;
  }
  // dom: {iv:[{a,b,aInf,bInf,ai,bi}], ex:[punts exclosos dins dels intervals]}
  function domainOf(f, dens) {
    var N = 8000, h = 2 * XL / N, X = [], OK = [], i, runs = [], cur = null, holes = [];
    for (i = 0; i <= N; i++) { X.push(-XL + i * h); OK.push(isFinite(f(X[i]))); }
    // un sol punt fora (un forat) no talla el tram: és un punt exclòs
    for (i = 1; i < N; i++) if (!OK[i] && OK[i - 1] && OK[i + 1]) { OK[i] = true; holes.push(snap(X[i])); }
    for (i = 0; i <= N; i++) { if (OK[i]) { if (!cur) { cur = { i0: i }; runs.push(cur); } cur.i1 = i; } else cur = null; }
    function edge(xIn, xOut) {
      for (var it = 0; it < 80; it++) { var m = (xIn + xOut) / 2; if (isFinite(f(m))) xIn = m; else xOut = m; }
      return snap((xIn + xOut) / 2);
    }
    function far(s) { return [1e2, 1e3, 1e6].some(function (v) { return !isNaN(f(s * v)); }); }
    var iv = [];
    runs.forEach(function (r) {
      if (r.i1 - r.i0 < 2) return;
      var o = { aInf: false, bInf: false };
      if (r.i0 > 0) o.a = edge(X[r.i0], X[r.i0 - 1]); else if (far(-1)) o.aInf = true; else o.a = edge(X[0], -1e2);
      if (r.i1 < N) o.b = edge(X[r.i1], X[r.i1 + 1]); else if (far(1)) o.bInf = true; else o.b = edge(X[N], 1e2);
      o.ai = !o.aInf && isFinite(f(o.a)); o.bi = !o.bInf && isFinite(f(o.b));
      iv.push(o);
    });
    var ex = [];
    function inside(p) { return iv.some(function (o) { return (o.aInf || p > o.a + 1e-9) && (o.bInf || p < o.b - 1e-9); }); }
    function addEx(p) { if (!inside(p)) return; for (var k = 0; k < ex.length; k++) if (Math.abs(ex[k] - p) < 1e-6 * (1 + Math.abs(p))) return; ex.push(p); }
    (dens || []).forEach(function (g) { roots(g, -XL, XL).forEach(addEx); });
    holes.forEach(addEx);
    ex.sort(function (p, q) { return p - q; });
    return { iv: iv, ex: ex };
  }
  function inDom(Dm, x) {
    if (Dm.ex.some(function (p) { return Math.abs(p - x) < 1e-9; })) return false;
    return Dm.iv.some(function (o) { return (o.aInf || x > o.a || (o.ai && x === o.a)) && (o.bInf || x < o.b || (o.bi && x === o.b)); });
  }
  // trams del domini (separats pels punts exclosos)
  function domParts(Dm) {
    var out = [];
    Dm.iv.forEach(function (o) {
      var pts = Dm.ex.filter(function (p) { return (o.aInf || p > o.a) && (o.bInf || p < o.b); });
      var bs = [o.aInf ? -Infinity : o.a].concat(pts).concat([o.bInf ? Infinity : o.b]);
      for (var k = 0; k + 1 < bs.length; k++) out.push({ a: bs[k], b: bs[k + 1], ai: k === 0 && o.ai, bi: k + 2 === bs.length && o.bi });
    });
    return out;
  }
  function domTex(Dm) {
    if (!Dm.iv.length) return "\\varnothing";
    if (Dm.iv.length === 1 && Dm.iv[0].aInf && Dm.iv[0].bInf) return Dm.ex.length ? "\\mathbb R-\\{" + Dm.ex.map(nn).join(",\\,") + "\\}" : "\\mathbb R";
    return domParts(Dm).map(function (p) {
      return (p.ai ? "[" : "(") + (isFinite(p.a) ? nn(p.a) : "-\\infty") + "," + (isFinite(p.b) ? nn(p.b) : "+\\infty") + (p.bi ? "]" : ")");
    }).join("\\cup ");
  }
  // zones que no són del domini (per a ombrejar-les)
  function domBands(Dm) {
    var out = [], P = Dm.iv;
    if (!P.length) return [{ a: -1e9, b: 1e9 }];
    if (!P[0].aInf) out.push({ a: -1e9, b: P[0].a });
    for (var k = 0; k + 1 < P.length; k++) out.push({ a: P[k].b, b: P[k + 1].a });
    if (!P[P.length - 1].bInf) out.push({ a: P[P.length - 1].b, b: 1e9 });
    return out;
  }
  // explicació: on s'anul·len els denominadors i on són positius els arguments dels logaritmes
  function signSet(g, test) {
    return domTex(domainOf(function (x) { var v = g(x); return test(v) ? 1 : NaN; }, []));
  }
  function domWhy(n) {
    var C = condsOf(n), h = [];
    C.den.forEach(function (d) {
      var g = compile(d), r = roots(g, -XL, XL);
      if (strip(d).t === "n" || strip(d).t === "c") return;
      h.push("<li>" + u("den") + " " + tex(T(d)) + ": " + (r.length ? u("denZ") + " " + tex("x=" + r.map(nn).join(",\\ x=")) : u("denNo")) + "</li>");
    });
    C.ln.forEach(function (a) {
      var g = compile(a);
      h.push("<li>" + u("lnArg") + " " + u("lnPos") + ": " + tex(T(a) + "\\gt0\\ \\Leftrightarrow\\ x\\in " + signSet(g, function (v) { return v > 1e-12; })) + "</li>");
    });
    C.sq.forEach(function (a) {
      var g = compile(a);
      h.push("<li>" + u("sqArg") + " " + u("sqPos") + ": " + tex(T(a) + "\\geq0\\ \\Leftrightarrow\\ x\\in " + signSet(g, function (v) { return v > -1e-12; })) + "</li>");
    });
    return h.length ? "<ul>" + h.join("") + "</ul>" : "<p>" + u("noCond") + "</p>";
  }

  /* ---------- punts de tall, simetria i asímptotes ---------- */
  function cutsOf(f, Dm) {
    var y0 = inDom(Dm, 0) ? f(0) : NaN;
    var xs = roots(f, -XL, XL).filter(function (x) { return inDom(Dm, x) && Math.abs(f(x)) < 1e-7; });
    return { oy: isFinite(y0) ? (Math.abs(y0) < 1e-12 ? 0 : y0) : null, ox: xs };
  }
  function cutsHtml(C) {
    return "<p><strong>" + u("cutX") + ":</strong> " + (C.ox.length ? tex("f(x)=0\\ \\Rightarrow\\ " + C.ox.map(function (x) { return "(" + nn(x) + ",0)"; }).join(",\\ ")) : u("noCutX")) +
      "<br><strong>" + u("cutY") + ":</strong> " + (C.oy !== null ? tex("x=0\\ \\Rightarrow\\ f(0)=" + nn(C.oy) + "\\ \\Rightarrow\\ (0," + nn(C.oy) + ")") : u("noCutY")) + "</p>";
  }
  function cutPts(C) {
    var p = C.ox.map(function (x) { return { x: x, y: 0, col: "var(--accent-2)" }; });
    if (C.oy !== null) p.push({ x: 0, y: C.oy, col: "var(--accent-2)" });
    return p;
  }
  var SYM_X = [0.37, 0.81, 1.23, 1.9, 2.71, 3.3, 4.6, 6.1, 7.7, 11.3];
  function symOf(f) {
    var ev = true, od = true, any = false;
    for (var i = 0; i < SYM_X.length; i++) {
      var x = SYM_X[i], a = f(x), b = f(-x);
      if (isFinite(a) !== isFinite(b)) return "dom";
      if (!isFinite(a)) continue;
      any = true;
      var tol = 1e-9 * (1 + Math.abs(a));
      if (Math.abs(a - b) > tol) ev = false;
      if (Math.abs(a + b) > tol) od = false;
    }
    if (!any) return "none";
    return ev ? "even" : od ? "odd" : "none";
  }
  function symTxt(s) { return s === "even" ? u("even") : s === "odd" ? u("odd") : s === "dom" ? u("noSym") + " (" + u("symNoDom") + ")" : u("noSym"); }
  // fracció exacta P/Q, si ho és
  function ratOf(n) {
    try { return { P: pTrim(polyOf(n)), Q: [new Fr(1)] }; } catch (e) {}
    n = strip(n);
    if (n.t !== "/") return null;
    try { var P = pTrim(polyOf(n.a)), Q = pTrim(polyOf(n.b)); if (pDeg(Q) === 0 && Q[0].zero()) return null; return { P: P, Q: Q }; } catch (e) { return null; }
  }
  // divisió de polinomis (coeficients de grau 0..n), amb els passos
  function pDiv(P, Q) {
    var r = pTrim(P), dq = pDeg(Q), lq = Q[dq], q = [new Fr(0)], steps = [];
    function isZ(p) { return pDeg(p) === 0 && p[0].zero(); }
    while (!isZ(r) && pDeg(r) >= dq) {
      var k = pDeg(r) - dq, c = r[pDeg(r)].div(lq), mono = [];
      for (var j = 0; j < k; j++) mono.push(new Fr(0));
      mono.push(c);
      while (q.length <= k) q.push(new Fr(0));
      q[k] = c;
      var sub = pMul(mono, Q), nr = pAdd(r, sub, -1);
      if (pDeg(nr) >= pDeg(r) && !isZ(nr)) nr = pTrim(nr.slice(0, pDeg(r))); // el terme principal s'anul·la sempre
      steps.push({ r: r, m: mono, s: sub, n: nr });
      r = nr;
    }
    return { q: pTrim(q), r: r, steps: steps };
  }
  function pFn(p) { return function (x) { var v = 0; for (var i = p.length - 1; i >= 0; i--) v = v * x + p[i].val(); return v; }; }
  // asímptotes: verticals (límits laterals) i, en cada costat, horitzontal / obliqua / cap
  function asyOf(f, Dm, n, rat0) {
    var cand = [];
    function add(c) { if (!cand.some(function (p) { return Math.abs(p - c) < 1e-7; })) cand.push(c); }
    Dm.iv.forEach(function (o) { if (!o.aInf) add(o.a); if (!o.bInf) add(o.b); });
    Dm.ex.forEach(add);
    cand.sort(function (p, q) { return p - q; });
    var av = [];
    cand.forEach(function (c) {
      var L = isFinite(f(c - 1e-6)) ? limSide(f, c, -1) : null, R = isFinite(f(c + 1e-6)) ? limSide(f, c, 1) : null;
      if ((L && L.k === "inf") || (R && R.k === "inf")) av.push({ x: c, L: L, R: R });
    });
    var rat = rat0 || (n ? ratOf(n) : null), side = {};
    [-1, 1].forEach(function (s) {
      var P = Dm.iv[s < 0 ? 0 : Dm.iv.length - 1];
      if (!P || !(s < 0 ? P.aInf : P.bInf)) { side[s] = { k: "no" }; return; }
      if (rat) {
        var dP = pDeg(rat.P), dQ = pDeg(rat.Q);
        if (dQ === 0) { side[s] = { k: "p" }; return; }
        if (dP < dQ) { side[s] = { k: "h", y: 0 }; return; }
        if (dP === dQ) { side[s] = { k: "h", y: rat.P[dP].div(rat.Q[dQ]).val() }; return; }
        if (dP === dQ + 1) { var Dv = pDiv(rat.P, rat.Q); side[s] = { k: "o", m: Dv.q[1].val(), n: Dv.q[0].val() }; return; }
        side[s] = { k: "p" }; return;
      }
      var L = limSide(f, s * Infinity, s);
      if (L.k === "num") { side[s] = { k: "h", y: snap(Math.abs(L.v) < 1e-5 ? 0 : L.v) }; return; }
      if (L.k !== "inf") { side[s] = { k: "none" }; return; }
      var M = limSide(function (x) { return f(x) / x; }, s * Infinity, s);
      if (M.k === "num" && Math.abs(M.v) > 1e-6) {
        var m = snap(M.v), Nn = limSide(function (x) { return f(x) - m * x; }, s * Infinity, s);
        if (Nn.k === "num") { side[s] = { k: "o", m: m, n: snap(Math.abs(Nn.v) < 1e-5 ? 0 : Nn.v) }; return; }
      }
      side[s] = { k: "p" };
    });
    return { av: av, side: side, rat: rat };
  }
  function lineTx(m, b) { return lineT(m, 0, b); }
  function sideTx(o) {
    if (o.k === "h") return u("ah") + " " + tex("y=" + nn(o.y));
    if (o.k === "o") return u("ao") + " " + tex(lineTx(o.m, o.n));
    if (o.k === "no") return u("notTo");
    return u("noAsy") + (o.k === "p" ? " (" + u("branch") + ")" : "");
  }
  function avHtml(A) {
    if (!A.av.length) return u("noAV");
    return A.av.map(function (q) {
      var l = [];
      if (q.L) l.push(tex("\\lim_{x\\to " + nn(q.x) + "^-}f(x)=" + limTex(q.L)));
      if (q.R) l.push(tex("\\lim_{x\\to " + nn(q.x) + "^+}f(x)=" + limTex(q.R)));
      return tex("x=" + nn(q.x)) + " &nbsp;(" + l.join(",&ensp;") + ")";
    }).join("<br>");
  }
  function asyHtml(A, poly) {
    if (poly) return "<p>" + u("poly") + "</p>";
    var sL = A.side[-1], sR = A.side[1], same = sL.k === sR.k && (sL.k === "h" ? Math.abs(sL.y - sR.y) < 1e-9 : sL.k === "o" ? Math.abs(sL.m - sR.m) + Math.abs(sL.n - sR.n) < 1e-9 : true);
    var h = "<p><strong>" + u("av") + ":</strong> " + avHtml(A) + "</p><p>";
    h += same ? sideTx(sL) + " (" + u("toL") + " " + t3("i", "y", "and") + " " + u("toR").replace(/^(quan|cuando|as) /, "") + ")" : u("toL").replace(/^./, function (c) { return c.toUpperCase(); }) + ": " + sideTx(sL) + "<br>" + u("toR").replace(/^./, function (c) { return c.toUpperCase(); }) + ": " + sideTx(sR);
    return h + "</p>";
  }
  function asyPlot(A) {
    var ha = [], oa = [];
    [-1, 1].forEach(function (s) {
      var o = A.side[s];
      if (o.k === "h" && ha.indexOf(o.y) < 0) ha.push(o.y);
      if (o.k === "o" && !oa.some(function (q) { return q.m === o.m && q.n === o.n; })) oa.push({ m: o.m, n: o.n });
    });
    return { va: A.av.map(function (q) { return q.x; }), ha: ha, oa: oa };
  }
  // finestra que mostra els elements importants
  function viewOf(f, xs, ys, def) {
    xs = xs.filter(isFinite); ys = ys.filter(isFinite);
    var x0 = xs.length ? Math.min.apply(null, xs) - 3 : def[0], x1 = xs.length ? Math.max.apply(null, xs) + 3 : def[1];
    if (x1 - x0 < 8) { var c = (x0 + x1) / 2; x0 = c - 4; x1 = c + 4; }
    var yy = autoY([f], x0, x1);
    if (ys.length) {
      // els punts destacats han de cabre bé, però sense que les asímptotes verticals aplanen la corba
      var lo = Math.min.apply(null, ys), hi = Math.max.apply(null, ys), sp = Math.max(hi - lo, 2);
      yy = [Math.min(Math.max(yy[0], lo - 2.5 * sp), lo - 0.8 * sp), Math.max(Math.min(yy[1], hi + 2.5 * sp), hi + 0.8 * sp)];
    }
    return [x0, x1, yy[0], yy[1]];
  }

  /* ---------- estudi complet ---------- */
  function fullStudy(n) {
    var f = compile(n), C = condsOf(n), Dm = domainOf(f, C.den.map(compile));
    var R = { n: n, f: f, Dm: Dm, poly: false };
    try { polyOf(n); R.poly = true; } catch (e) {}
    R.cuts = cutsOf(f, Dm); R.sym = symOf(f); R.A = asyOf(f, Dm, n);
    try { R.S = studyF(n, -XL, XL); R.inf = true; if (R.S.ev.length > 14) { R.S = studyF(n, -8, 8); R.inf = false; } } catch (e) { if (!(e instanceof NoDiff)) throw e; R.S = null; }
    var xs = R.cuts.ox.concat(R.A.av.map(function (q) { return q.x; })), ys = [];
    if (R.cuts.oy !== null) { xs.push(0); ys.push(R.cuts.oy); }
    Dm.iv.forEach(function (o) { if (!o.aInf && Math.abs(o.a) < XL) xs.push(o.a); if (!o.bInf && Math.abs(o.b) < XL) xs.push(o.b); });
    if (R.S) R.S.ev.forEach(function (e) { if (e.k === "z" && e.t1 !== "none") { xs.push(e.x); ys.push(e.y); } });
    [-1, 1].forEach(function (s) { if (R.A.side[s].k === "h") ys.push(R.A.side[s].y); });
    R.view = viewOf(f, xs, ys, [-6, 6]);
    return R;
  }

  /* ---------- figures estàtiques ---------- */
  var PWF = {
    ex: { p: ["x+3", "x^2+1", "2/x"], c: [-1, 1] },
    jump: { p: ["x^2", "4-x"], c: [1] },
    el: { p: ["e^x", "ln(x+1)+1"], c: [0] },
    rat: { p: ["1/(x+2)", "x/2+1/2"], c: [0] }
  };
  var FIGS = {
    par: function () {
      var f = F("x^4/8-x^2+2.5"), a = 1.7, ya = f(a);
      return { v: [-3, 3, -0.5, 4], curves: [{ f: f }, { f: function () { return ya; }, a: -a, b: a, col: "var(--accent-2)" }], pts: [{ x: -a, y: ya }, { x: a, y: ya }], guides: [{ x: 0 }],
        labels: [{ x: -a, y: ya + 0.45, t: "(−a, f(a))" }, { x: a, y: ya + 0.45, t: "(a, f(a))" }] };
    },
    sen: function () {
      var f = F("x^3/3-x"), a = 2.1, ya = f(a);
      return { v: [-3, 3, -2.5, 2.5], curves: [{ f: f }, { f: lineF(ya / a, 0, 0), a: -a, b: a, col: "var(--accent-2)" }], pts: [{ x: -a, y: -ya }, { x: a, y: ya }, { x: 0, y: 0, col: "var(--accent-2)" }],
        labels: [{ x: a - 0.1, y: ya + 0.35, t: "(a, f(a))", anchor: "end" }, { x: -a + 0.1, y: -ya - 0.55, t: "(−a, −f(a))", anchor: "start" }] };
    },
    asV: function () {
      return { v: [-3, 7, -4, 6], curves: [{ f: F("1/(x-2)+1") }], va: [2], ha: [1],
        labels: [{ x: 2.15, y: 5.3, t: "x = 2", anchor: "start" }, { x: -2.8, y: 1.35, t: "y = 1", anchor: "start" }] };
    },
    asO: function () {
      return { v: [-7, 9, -12, 16], curves: [{ f: F("(x^2+3)/(x-1)") }], va: [1], oa: [{ m: 1, n: 1 }],
        labels: [{ x: 1.3, y: 14.5, t: "x = 1", anchor: "start" }, { x: 8.6, y: 7.5, t: "y = x + 1", anchor: "end" }] };
    },
    expo: function () {
      return { v: [-4, 4, -1, 5], curves: [{ f: F("e^x") }, { f: F("(1/2)^x"), col: "var(--r3)" }], ha: [0], pts: [{ x: 0, y: 1, col: "var(--text)" }],
        labels: [{ x: 1.75, y: 4.5, t: "y = eˣ", anchor: "end" }, { x: -2.4, y: 4.5, t: "y = (1/2)ˣ", anchor: "start" }] };
    },
    loga: function () {
      return { v: [-1, 7, -3.5, 3.5], curves: [{ f: F("ln(x)") }, { f: F("-ln(x)/ln(2)"), col: "var(--r3)" }], va: [0], pts: [{ x: 1, y: 0, col: "var(--text)" }],
        labels: [{ x: 6.8, y: 2.3, t: "y = ln x", anchor: "end" }, { x: 6.8, y: -2.3, t: "y = log₁/₂ x", anchor: "end" }] };
    },
    ex1: function () {
      return { v: [-1, 4.5, -2, 6], curves: [{ f: F("x^3-6x^2+9x") }], pts: [{ x: 0, y: 0, col: "var(--accent-2)" }, { x: 3, y: 0, col: "var(--accent-2)" }],
        mark: [{ x: 1, y: 4, col: "var(--ok)" }, { x: 3, y: 0, col: "var(--bad)" }], labels: [{ x: 1, y: 4.7, t: "(1, 4)" }, { x: 3.2, y: -0.8, t: "(3, 0)" }] };
    },
    ex2: function () {
      var r = Math.SQRT2;
      return { v: [-2.2, 2.2, -1.6, 3], curves: [{ f: F("x^4-2x^2") }], pts: [{ x: -r, y: 0, col: "var(--accent-2)" }, { x: r, y: 0, col: "var(--accent-2)" }],
        mark: [{ x: 0, y: 0, col: "var(--ok)" }, { x: -1, y: -1, col: "var(--bad)" }, { x: 1, y: -1, col: "var(--bad)" }],
        labels: [{ x: -1, y: -1.45, t: "(−1, −1)" }, { x: 1, y: -1.45, t: "(1, −1)" }, { x: 0, y: 0.35, t: "(0, 0)" }] };
    },
    ex3: function () {
      return { v: [-6, 6, -5, 6], curves: [{ f: F("x^2/(x^2-4)") }], va: [-2, 2], ha: [1], mark: [{ x: 0, y: 0, col: "var(--ok)" }],
        labels: [{ x: -5.8, y: 1.45, t: "y = 1", anchor: "start" }, { x: -2.15, y: 5.3, t: "x = −2", anchor: "end" }, { x: 2.15, y: 5.3, t: "x = 2", anchor: "start" }] };
    },
    ex4: function () {
      return { v: [-7, 9, -12, 16], curves: [{ f: F("(x^2+3)/(x-1)") }], va: [1], oa: [{ m: 1, n: 1 }], pts: [{ x: 0, y: -3, col: "var(--accent-2)" }],
        mark: [{ x: -1, y: -2, col: "var(--ok)" }, { x: 3, y: 6, col: "var(--bad)" }], labels: [{ x: -1.3, y: -0.6, t: "(−1, −2)", anchor: "end" }, { x: 3.4, y: 4.4, t: "(3, 6)", anchor: "start" }, { x: 8.6, y: 7.5, t: "y = x + 1", anchor: "end" }] };
    },
    ex5: function () {
      return { v: [-6, 1.5, -1, 3], curves: [{ f: F("x*e^x") }], ha: [0], pts: [{ x: 0, y: 0, col: "var(--accent-2)" }], mark: [{ x: -1, y: -1 / Math.E, col: "var(--bad)" }],
        labels: [{ x: -1, y: -0.75, t: "(−1, −1/e)" }] };
    },
    ex6: function () {
      return { v: [-0.5, 12, -2, 1], curves: [{ f: F("ln(x)/x") }], va: [0], ha: [0], pts: [{ x: 1, y: 0, col: "var(--accent-2)" }], mark: [{ x: Math.E, y: 1 / Math.E, col: "var(--ok)" }],
        labels: [{ x: Math.E, y: 0.62, t: "(e, 1/e)" }] };
    },
    ex7: function () {
      var P = pwMake(PWF.ex), v = [-5, 6, -1, 4], d = pwDraw(P, v);
      return { v: v, curves: d.curves, pts: d.pts, ha: [0], mark: [{ x: -1, y: 2, col: "var(--ok)" }, { x: 0, y: 1, col: "var(--bad)" }, { x: 1, y: 2, col: "var(--ok)" }],
        labels: [{ x: -1, y: 2.5, t: "(−1, 2)" }, { x: 0, y: 0.45, t: "(0, 1)" }, { x: 1.2, y: 2.5, t: "(1, 2)", anchor: "start" }] };
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

  /* ---------- ginys amb una funció escrita ---------- */
  // esquelet comú: botons d'exemples, camp f(x) i redibuix en canviar
  function fnWidget(id, PRE, key, draw) {
    var w = document.getElementById(id); if (!w) return;
    var fi = $(w, "f"), st = 0;
    presetBtns($(w, "presets"), PRE.length, key, function (i) { st = i; fi.value = PRE[i]; go(); });
    fi.addEventListener("input", function () { st = -1; go(); });
    function go() {
      var n;
      try { n = parse(fi.value); compile(n)(1); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); w.querySelector(".info").textContent = u("bad"); return; }
      draw(w, n, st);
    }
    onLang(go);
  }
  function wDom() {
    fnWidget("w-dom", ["x^3-2x", "(x+1)/(x^2-4)", "1/(x^2+1)", "e^(1/x)", "ln(x-3)", "ln(x^2-4)", "x/ln(x)"], "pDom", function (w, n) {
      var f = compile(n), Dm = domainOf(f, condsOf(n).den.map(compile)), v = viewOf(f, Dm.ex.concat(Dm.iv.map(function (o) { return o.aInf ? NaN : o.a; })).concat(Dm.iv.map(function (o) { return o.bInf ? NaN : o.b; })), [], [-6, 6]);
      w.querySelector(".info").innerHTML = "<p>" + tex("f(x)=" + T(n)) + "</p>" + domWhy(n) + "<p><strong>" + u("dom") + ":</strong> " + (Dm.iv.length ? tex("\\mathrm{Dom}\\,f=" + domTex(Dm)) : u("empty")) + "</p>";
      plot(w.querySelector("svg.lp-svg"), { v: v, band: domBands(Dm), curves: [{ f: f }], va: Dm.ex.filter(function (p) { return !isFinite(f(p - 1e-6)) || Math.abs(f(p - 1e-6)) > 1e4; }), pts: Dm.iv.reduce(function (a, o) {
        if (!o.aInf && isFinite(f(o.a))) a.push({ x: o.a, y: f(o.a) }); if (!o.bInf && isFinite(f(o.b))) a.push({ x: o.b, y: f(o.b) }); return a; }, []) });
    });
  }
  function wCut() {
    fnWidget("w-cut", ["x^3-4x", "x^2-2x-3", "(x^2-1)/(x+2)", "e^x-2", "ln(x+1)", "x^2*e^x"], "pCut", function (w, n) {
      var f = compile(n), Dm = domainOf(f, condsOf(n).den.map(compile)), C = cutsOf(f, Dm);
      var xs = C.ox.slice(), ys = [0]; if (C.oy !== null) { xs.push(0); ys.push(C.oy); }
      w.querySelector(".info").innerHTML = "<p>" + tex("f(x)=" + T(n)) + "</p>" + cutsHtml(C);
      plot(w.querySelector("svg.lp-svg"), { v: viewOf(f, xs, ys, [-5, 5]), band: domBands(Dm), curves: [{ f: f }], pts: cutPts(C),
        labels: cutPts(C).map(function (p) { return { x: p.x, y: p.y, t: "(" + numTxt(+p.x.toFixed(3)) + ", " + numTxt(+p.y.toFixed(3)) + ")", anchor: "start" }; }) });
    });
  }
  function wSym() {
    fnWidget("w-sym", ["x^4-3x^2", "x^3-3x", "x/(x^2+1)", "x^2/(x^2-1)", "e^(-x^2)", "e^x", "x^2+x"], "pSym", function (w, n) {
      var f = compile(n), s = symOf(f), rows = "";
      [1, 2, 3].forEach(function (x) {
        var a = f(x), b = f(-x);
        rows += "<tr><td>" + tex(String(x)) + "</td><td>" + tex(isFinite(a) ? nn(a) : "\\nexists") + "</td><td>" + tex(isFinite(b) ? nn(b) : "\\nexists") + "</td><td>" + tex(isFinite(a) ? nn(-a) : "\\nexists") + "</td></tr>";
      });
      var cls = s === "even" ? "ok" : s === "odd" ? "ev" : "as";
      w.querySelector(".info").innerHTML = "<p>" + tex("f(x)=" + T(n)) + "</p>" +
        '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("x") + "</th><th>" + tex("f(x)") + "</th><th>" + tex("f(-x)") + "</th><th>" + tex("-f(x)") + "</th></tr></thead><tbody>" + rows + "</tbody></table></div>" +
        "<p>" + (s === "even" ? tex("f(-x)=f(x)") : s === "odd" ? tex("f(-x)=-f(x)") : "") + ' <span class="badge ' + cls + '">' + symTxt(s) + "</span></p>";
      var v = viewOf(f, [-3, 3], [], [-5, 5]);
      plot(w.querySelector("svg.lp-svg"), { v: v, curves: [{ f: function (x) { return s === "odd" ? -f(-x) : f(-x); }, col: "var(--r3)" }, { f: f }], guides: s === "even" ? [{ x: 0 }] : [],
        pts: s === "odd" ? [{ x: 0, y: 0, col: "var(--accent-2)" }] : [] });
    });
  }
  function wAsy() {
    fnWidget("w-asy", ["(2x+1)/(x-3)", "x/(x^2-1)", "3x^2/(x^2+1)", "2-e^(-x)", "ln(x+2)", "(x^2+1)/x"], "pAsy", function (w, n) {
      var f = compile(n), Dm = domainOf(f, condsOf(n).den.map(compile)), A = asyOf(f, Dm, n), poly = !!(A.rat && pDeg(A.rat.Q) === 0), P = asyPlot(A);
      var ys = P.ha.slice();
      w.querySelector(".info").innerHTML = "<p>" + tex("f(x)=" + T(n)) + "</p>" + asyHtml(A, poly);
      plot(w.querySelector("svg.lp-svg"), Object.assign({ v: viewOf(f, P.va, ys, [-6, 6]), curves: [{ f: f }] }, P));
    });
  }
  function wMx() {
    fnWidget("w-mx", ["x^3-6x^2+9x", "x^4-2x^2", "x^2/(x^2-4)", "(x^2+3)/(x-1)", "x*e^x", "ln(x)/x"], "pMx", function (w, n) {
      var info = w.querySelector(".info"), tb = $(w, "tbl"), R;
      try { R = fullStudy(n); } catch (e) { info.textContent = u("bad"); tb.innerHTML = ""; return; }
      if (!R.S) { info.textContent = u("noDiff"); tb.innerHTML = ""; return; }
      info.innerHTML = "<p>" + tex("f(x)=" + T(n)) + "<br>" + tex("f'(x)=" + texD(R.S.dn)) + "</p>" + monoHtml(R.S, R.inf) + extHtml(R.S);
      tb.innerHTML = signTable(R.S, R.inf);
      plot(w.querySelector("svg.lp-svg"), Object.assign({ v: R.view, curves: monoCurves(R.S), mark: extMarks(R.S) }, asyPlot(R.A)));
    });
  }

  /* ---------- asímptota obliqua pel mètode del quocient ---------- */
  function wObl() {
    var w = document.getElementById("w-obl"); if (!w) return;
    var PRE = [["x^2+3", "x-1"], ["x^2", "x+1"], ["2x^2-x+1", "x"], ["x^3", "x^2-1"], ["x^3+1", "x"], ["3x^2+1", "x^2-4"]];
    var pi = $(w, "p"), qi = $(w, "q"), info = w.querySelector(".info"), dv = $(w, "div"), svg = w.querySelector("svg.lp-svg");
    presetBtns($(w, "presets"), PRE.length, "pObl", function (i) { pi.value = PRE[i][0]; qi.value = PRE[i][1]; draw(); });
    [pi, qi].forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var P, Q;
      try { P = pTrim(polyOf(parse(pi.value))); Q = pTrim(polyOf(parse(qi.value))); if (pDeg(Q) === 0 && Q[0].zero()) throw 0; pi.classList.remove("bad"); qi.classList.remove("bad"); }
      catch (e) { pi.classList.add("bad"); qi.classList.add("bad"); info.textContent = u("notPoly"); dv.innerHTML = ""; return; }
      var Dv = pDiv(P, Q), dP = pDeg(P), dQ = pDeg(Q), Pf = pFn(P), Qf = pFn(Q), f = function (x) { return Pf(x) / Qf(x); };
      var Dm = domainOf(f, [Qf]), A = asyOf(f, Dm, null, { P: P, Q: Q });
      var h = "<p>" + tex("f(x)=\\dfrac{" + pTex(P) + "}{" + pTex(Q) + "}") + "</p>";
      // passos de la divisió
      var s = "";
      Dv.steps.forEach(function (st, i) {
        var lead = [], k = pDeg(st.r); for (var j = 0; j < k; j++) lead.push(new Fr(0)); lead.push(st.r[k]);
        s += "<li>" + u("divide") + " " + tex("\\dfrac{" + pTex(lead) + "}{" + monoTex(Q[dQ], dQ, true) + "}=" + pTex(st.m)) + "; " + u("mult") + " " + tex(pTex(st.m) + "\\cdot\\left(" + pTex(Q) + "\\right)=" + pTex(st.s)) +
          "; " + u("subt") + ": " + tex("\\left(" + pTex(st.r) + "\\right)-\\left(" + pTex(st.s) + "\\right)=" + pTex(st.n)) + "</li>";
      });
      dv.innerHTML = (s ? "<ol>" + s + "</ol>" : "") + "<p>" + u("quo") + " " + tex("C(x)=" + pTex(Dv.q)) + ", &nbsp;" + u("rem") + " " + tex("R(x)=" + pTex(Dv.r)) + "<br>" +
        tex("f(x)=" + pTex(Dv.q) + (pDeg(Dv.r) === 0 && Dv.r[0].zero() ? "" : "+\\dfrac{" + pTex(Dv.r) + "}{" + pTex(Q) + "}")) + "</p>";
      var cas = dP < dQ ? "dLt" : dP === dQ ? "dEq" : dP === dQ + 1 ? "dP1" : "dBig";
      h += '<p class="verdict">' + u(cas).replace("C(x)", "") + (cas === "dEq" ? ": " + tex("y=\\dfrac{" + P[dP].tex() + "}{" + Q[dQ].tex() + "}=" + P[dP].div(Q[dQ]).tex()) : cas === "dP1" ? " " + tex("y=" + pTex(Dv.q)) : "") + "</p>";
      h += "<p><strong>" + u("av") + ":</strong> " + avHtml(A) + "</p>";
      var o = A.side[1];
      if (o.k === "o" || o.k === "h") {
        var g = o.k === "o" ? function (x) { return o.m * x + o.n; } : function () { return o.y; }, rows = "";
        [-1000, -100, -10, 10, 100, 1000].forEach(function (x) { var d = f(x) - g(x); rows += "<tr><td>" + tex(String(x)) + "</td><td>" + tex(numTex(+d.toPrecision(4))) + "</td></tr>"; });
        var yl = o.k === "o" ? lineTx(o.m, o.n).slice(2) : nn(o.y);
        h += '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("x") + "</th><th>" + tex("f(x)-\\left(" + yl + "\\right)") + "</th></tr></thead><tbody>" + rows + "</tbody></table></div>";
        var dl = f(-1000) - g(-1000), dr = f(1000) - g(1000);
        if (Math.abs(dl) > 1e-12 || Math.abs(dr) > 1e-12) h += "<p>" + u("toL").replace(/^./, function (c) { return c.toUpperCase(); }) + ": " + (dl > 0 ? u("above") : u("below")) + ".<br>" + u("toR").replace(/^./, function (c) { return c.toUpperCase(); }) + ": " + (dr > 0 ? u("above") : u("below")) + ".</p>";
      }
      info.innerHTML = h;
      var Pp = asyPlot(A);
      plot(svg, Object.assign({ v: viewOf(f, Pp.va, Pp.ha, [-6, 6]), curves: [{ f: f }] }, Pp));
    }
    onLang(draw);
  }

  /* ---------- famílies exponencials i logarítmiques ---------- */
  function wEl() {
    var w = document.getElementById("w-el"); if (!w) return;
    var ty = 0, ra = $(w, "a"), rh = $(w, "h"), rk = $(w, "k"), svg = w.querySelector("svg.lp-svg"), info = w.querySelector(".info");
    [ra, rh, rk].forEach(function (r) { r.min = -3; r.max = 3; r.step = 0.5; r.addEventListener("input", draw); });
    ra.value = 1; rh.value = 0; rk.value = 0;
    presetBtns($(w, "presets"), 3, "pEl", function (i) { ty = i; ra.value = 1; rh.value = 0; rk.value = i === 2 ? 0 : -1; draw(); });
    function sh(h) { return h === 0 ? "x" : h > 0 ? "x-" + nn(h) : "x+" + nn(-h); }
    function co(a) { return a === 1 ? "" : a === -1 ? "-" : nn(a) + "\\,"; }
    function kk(k) { return k === 0 ? "" : (k > 0 ? "+" : "-") + nn(Math.abs(k)); }
    function draw() {
      var a = +ra.value, h = +rh.value, k = +rk.value;
      if (a === 0) { a = 0.5; ra.value = 0.5; }
      $(w, "av").textContent = numTxt(a); $(w, "hv").textContent = numTxt(h); $(w, "kv").textContent = numTxt(k);
      var b = ty === 0 ? Math.E : 0.5, lb = Math.log(b), f, ft, H = "", cfg = { v: [-6, 6, -5, 5] }, pts = [];
      if (ty < 2) {
        f = function (x) { return a * Math.pow(b, x - h) + k; };
        ft = "f(x)=" + co(a) + (ty === 0 ? "e^{" + sh(h) + "}" : "\\left(\\tfrac12\\right)^{" + sh(h) + "}") + kk(k);
        var r = -k / a;
        H += "<p><strong>" + u("dom") + ":</strong> " + tex("\\mathbb R") + "</p>";
        H += "<p><strong>" + u("ah") + ":</strong> " + tex("y=" + nn(k)) + " " + (lb > 0 ? u("toL") : u("toR")) + "<br><strong>" + u("av") + ":</strong> " + u("noAV") + "</p>";
        H += "<p><strong>" + u("cutY") + ":</strong> " + tex("(0," + nn(f(0)) + ")") + "<br><strong>" + u("cutX") + ":</strong> " +
          (r > 0 ? tex((ty === 0 ? "e^{" + sh(h) + "}" : "\\left(\\tfrac12\\right)^{" + sh(h) + "}") + "=" + nn(r) + "\\ \\Rightarrow\\ x=" + nn(h + Math.log(r) / lb)) : u("noCutX")) + "</p>";
        H += "<p><strong>" + u("mono") + ":</strong> " + (a * lb > 0 ? u("inc") : u("dec")) + " " + t3("en", "en", "on") + " " + tex("\\mathbb R") + "</p>";
        cfg.ha = [k]; pts.push({ x: 0, y: f(0) }); if (r > 0) pts.push({ x: h + Math.log(r) / lb, y: 0 });
      } else {
        f = function (x) { return x > h ? a * Math.log(x - h) + k : NaN; };
        ft = "f(x)=" + co(a) + "\\ln(" + sh(h) + ")" + kk(k);
        var x0 = h + Math.exp(-k / a);
        H += "<p><strong>" + u("dom") + ":</strong> " + tex(sh(h) + "\\gt0\\ \\Rightarrow\\ (" + nn(h) + ",+\\infty)") + "</p>";
        H += "<p><strong>" + u("av") + ":</strong> " + tex("x=" + nn(h)) + " &nbsp;(" + tex("\\lim_{x\\to " + nn(h) + "^+}f(x)=" + (a > 0 ? "-\\infty" : "+\\infty")) + ")<br><strong>" + u("ah") + ":</strong> " + u("noAV") + "</p>";
        H += "<p><strong>" + u("cutX") + ":</strong> " + tex("\\ln(" + sh(h) + ")=" + nn(-k / a) + "\\ \\Rightarrow\\ x=" + nn(x0)) + "<br><strong>" + u("cutY") + ":</strong> " + (h < 0 ? tex("(0," + nn(f(0)) + ")") : u("noCutY")) + "</p>";
        H += "<p><strong>" + u("mono") + ":</strong> " + (a > 0 ? u("inc") : u("dec")) + " " + t3("en", "en", "on") + " " + tex("(" + nn(h) + ",+\\infty)") + "</p>";
        cfg.va = [h]; cfg.band = [{ a: -10, b: h }]; pts.push({ x: x0, y: 0 }); if (h < 0) pts.push({ x: 0, y: f(0) });
      }
      info.innerHTML = "<p>" + tex(ft) + "</p>" + H;
      cfg.curves = [{ f: f }]; cfg.pts = pts.map(function (p) { p.col = "var(--accent-2)"; return p; });
      plot(svg, cfg);
    }
    onLang(draw);
  }

  /* ---------- funcions a trossos ---------- */
  function pwStudy(def) {
    var P = pwMake(def), segs = [], av = [], ha = {};
    for (var i = 0; i < P.n; i++) {
      var B = P.bounds(i), lo = Math.max(B[0], -XL), hi = Math.min(B[1], XL); if (!(hi > lo)) continue;
      var n = parse(def.p[i]), fi = compile(n), S = null;
      try { S = crit(fi, compile(D(n)), lo, hi); } catch (e) { S = null; }
      if (S) S.seg.forEach(function (g) { segs.push({ a: g.a, b: g.b, s: g.s }); });
      condsOf(n).den.forEach(function (d) {
        roots(compile(d), lo, hi).forEach(function (r) { if (r > B[0] && r < B[1] && limSide(fi, r, 1).k === "inf") av.push(r); });
      });
      if (i === 0 && !isFinite(B[0])) { var L = limSide(fi, -Infinity, -1); if (L.k === "num") ha[-1] = snap(Math.abs(L.v) < 1e-5 ? 0 : L.v); }
      if (i === P.n - 1 && !isFinite(B[1])) { var R = limSide(fi, Infinity, 1); if (R.k === "num") ha[1] = snap(Math.abs(R.v) < 1e-5 ? 0 : R.v); }
    }
    // ajuntem els trams amb el mateix signe i busquem els extrems (també en els punts de tall, si hi és contínua)
    var runs = [];
    segs.forEach(function (g) {
      var r = runs[runs.length - 1];
      if (r && r.s === g.s && Math.abs(r.b - g.a) < 1e-9 && g.s !== 0 && isFinite(P.f(g.a)) && Math.abs(P.f(g.a) - P.f(g.a - 1e-7)) < 1e-4 && Math.abs(P.f(g.a) - P.f(g.a + 1e-7)) < 1e-4) r.b = g.b;
      else runs.push({ a: g.a, b: g.b, s: g.s });
    });
    var ext = [];
    for (var j = 0; j + 1 < runs.length; j++) {
      var x = runs[j].b, y = P.f(x);
      if (!isFinite(y) || Math.abs(x - runs[j + 1].a) > 1e-9) continue;
      if (Math.abs(P.f(x - 1e-7) - y) > 1e-4 || Math.abs(P.f(x + 1e-7) - y) > 1e-4) continue;
      if (runs[j].s > 0 && runs[j + 1].s < 0) ext.push({ x: snap(x), y: y, t: "max" });
      if (runs[j].s < 0 && runs[j + 1].s > 0) ext.push({ x: snap(x), y: y, t: "min" });
    }
    return { P: P, runs: runs, ext: ext, av: av, ha: ha };
  }
  function wPw() {
    var w = document.getElementById("w-pw"); if (!w) return;
    var PRE = [PWF.ex, PWF.jump, PWF.el, PWF.rat];
    var ins = ["p1", "c1", "p2", "c2", "p3"].map(function (r) { return $(w, r); }), info = w.querySelector(".info"), svg = w.querySelector("svg.lp-svg");
    presetBtns($(w, "presets"), PRE.length, "pPw", function (i) {
      var d = PRE[i]; ins[0].value = d.p[0]; ins[1].value = numTxt(d.c[0]).replace("−", "-"); ins[2].value = d.p[1];
      ins[3].value = d.c[1] !== undefined ? numTxt(d.c[1]).replace("−", "-") : ""; ins[4].value = d.p[2] || ""; draw();
    });
    ins.forEach(function (el) { el.addEventListener("input", draw); });
    function draw() {
      var def = { p: [ins[0].value, ins[2].value], c: [] }, okAll = true;
      ins.forEach(function (el) { el.classList.remove("bad"); });
      var c1 = parseFr(ins[1].value);
      if (!c1) { ins[1].classList.add("bad"); okAll = false; } else def.c.push(c1.val());
      if (ins[4].value.trim() !== "" || ins[3].value.trim() !== "") {
        var c2 = parseFr(ins[3].value);
        if (!c2 || (c1 && c2.val() <= c1.val())) { ins[3].classList.add("bad"); okAll = false; } else { def.c.push(c2.val()); def.p.push(ins[4].value); }
      }
      [0, 2, 4].forEach(function (k, i) { if (i < def.p.length) { try { parse(ins[k].value); } catch (e) { ins[k].classList.add("bad"); okAll = false; } } });
      if (!okAll) { info.textContent = u("bad"); return; }
      var Z;
      try { Z = pwStudy(def); } catch (e) { info.textContent = u("bad"); return; }
      var P = Z.P, h = "<p>" + tex(pwTex(def)) + "</p>", allC = true;
      P.c.forEach(function (c, k) {
        var L = sideAt(P.piece(k), c, -1), R = sideAt(P.piece(k + 1), c, 1), fc = P.f(c), cl = classify(L, R, fc);
        if (cl !== "ok") allC = false;
        h += "<p>" + u("atCut") + " " + tex("x=" + nn(c)) + ": " + tex("\\lim_{x\\to " + nn(c) + "^-}f(x)=" + limTex(L) + ",\\ \\lim_{x\\to " + nn(c) + "^+}f(x)=" + limTex(R) + ",\\ f(" + nn(c) + ")=" + nn(fc)) + " " + badge(cl) + "</p>";
      });
      if (allC && !Z.av.length) h += '<p class="msg-ok">' + u("contAll") + "</p>";
      if (Z.av.length) h += "<p><strong>" + u("av") + ":</strong> " + tex(Z.av.map(function (x) { return "x=" + nn(x); }).join(",\\ ")) + "</p>";
      if (Z.ha[-1] !== undefined) h += "<p><strong>" + u("ah") + ":</strong> " + tex("y=" + nn(Z.ha[-1])) + " " + u("toL") + "</p>";
      if (Z.ha[1] !== undefined) h += "<p><strong>" + u("ah") + ":</strong> " + tex("y=" + nn(Z.ha[1])) + " " + u("toR") + "</p>";
      var last = Z.runs.length - 1;
      function iv(r, j) { return intTex(r.a, r.b, j === 0 && r.a <= -XL + 1e-9, j === last && r.b >= XL - 1e-9); }
      var up = [], dn = [];
      Z.runs.forEach(function (r, j) { if (r.s > 0) up.push(iv(r, j)); if (r.s < 0) dn.push(iv(r, j)); });
      h += "<p><strong>" + u("incOn") + "</strong> " + (up.length ? tex(up.join("\\cup ")) : "—") + "<br><strong>" + u("decOn") + "</strong> " + (dn.length ? tex(dn.join("\\cup ")) : "—") + "</p>";
      h += "<p>" + (Z.ext.length ? Z.ext.map(function (e) { return '<span class="badge ' + (e.t === "max" ? "ok" : "as") + '">' + u(e.t === "max" ? "maxR" : "minR") + "</span> " + tex(ptTex(e.x, e.y)); }).join("<br>") : u("noExtPw")) + "</p>";
      info.innerHTML = h;
      var xs = P.c.concat(Z.av).concat(Z.ext.map(function (e) { return e.x; })), x0 = Math.min.apply(null, xs) - 4, x1 = Math.max.apply(null, xs) + 4;
      var yy = autoY([P.f], x0, x1);
      var v = [x0, x1, yy[0], yy[1]], d = pwDraw(P, v);
      var ha = []; if (Z.ha[-1] !== undefined) ha.push(Z.ha[-1]); if (Z.ha[1] !== undefined && ha.indexOf(Z.ha[1]) < 0) ha.push(Z.ha[1]);
      plot(svg, { v: v, curves: d.curves, pts: d.pts, va: Z.av, ha: ha, mark: Z.ext.map(function (e) { return { x: e.x, y: e.y, col: e.t === "max" ? "var(--ok)" : "var(--bad)" }; }) });
    }
    onLang(function () { if (!ins[0].value) { ins[0].value = PRE[0].p[0]; ins[1].value = "-1"; ins[2].value = PRE[0].p[1]; ins[3].value = "1"; ins[4].value = PRE[0].p[2]; } draw(); });
  }

  /* ---------- estudi complet pas a pas ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var PRE = ["x^3-6x^2+9x", "x^4-2x^2", "x^2/(x^2-4)", "(x^2+3)/(x-1)", "(2x-1)/(x+1)", "x*e^x", "e^x/x", "ln(x)/x"];
    var fi = $(w, "f"), out = $(w, "out"), tb = $(w, "tbl"), svg = w.querySelector("svg.lp-svg"), bn = $(w, "nx"), ba = $(w, "al"), cnt = $(w, "cnt"), R = null, shown = 1;
    presetBtns($(w, "presets"), PRE.length, "pLab", function (i) { fi.value = PRE[i]; setup(); });
    fi.addEventListener("input", setup);
    bn.addEventListener("click", function () { if (shown < 6) { shown++; draw(); } });
    ba.addEventListener("click", function () { shown = shown >= 6 ? 1 : 6; draw(); });
    function setup() {
      shown = 1;
      try { R = fullStudy(parse(fi.value)); fi.classList.remove("bad"); }
      catch (e) { R = null; fi.classList.add("bad"); out.textContent = u("bad"); tb.innerHTML = ""; return; }
      draw();
    }
    function row(i, html) { return '<div class="rs' + (i === shown - 1 ? " now" : "") + '"><h4>' + (i + 1) + ". " + u("sNames")[i] + "</h4>" + html + "</div>"; }
    function draw() {
      if (!R) return;
      var names = u("sNames"), rows = [], S = R.S;
      rows.push(row(0, (R.Dm.iv.length ? tex("\\mathrm{Dom}\\,f=" + domTex(R.Dm)) : u("empty")) + '<div class="why">' + domWhy(R.n) + "</div>"));
      if (shown > 1) rows.push(row(1, cutsHtml(R.cuts)));
      if (shown > 2) rows.push(row(2, symTxt(R.sym) + (R.sym === "even" ? " — " + tex("f(-x)=f(x)") : R.sym === "odd" ? " — " + tex("f(-x)=-f(x)") : "")));
      if (shown > 3) rows.push(row(3, asyHtml(R.A, R.poly)));
      if (shown > 4) rows.push(row(4, S ? "<p>" + tex("f'(x)=" + texD(S.dn)) + "</p>" + monoHtml(S, R.inf) + extHtml(S) : u("noDiff")));
      if (shown > 5) rows.push(row(5, "✓"));
      out.innerHTML = "<p>" + tex("f(x)=" + T(R.n)) + "</p>" + rows.join("");
      tb.innerHTML = shown > 4 && S ? signTable(S, R.inf) : "";
      bn.textContent = u("next") + " →"; bn.disabled = shown >= 6;
      ba.textContent = shown >= 6 ? u("reset") : u("all");
      cnt.textContent = u("step") + " " + shown + " " + u("of") + " 6 · " + names[shown - 1];
      var cfg = { v: R.view, band: domBands(R.Dm), curves: [], pts: [] };
      if (shown > 1) cfg.pts = cutPts(R.cuts);
      if (shown > 3) Object.assign(cfg, asyPlot(R.A));
      if (shown > 4 && S) cfg.mark = extMarks(S);
      if (shown > 5) cfg.curves = S ? monoCurves(S) : [{ f: R.f }];
      plot(svg, cfg);
    }
    onLang(setup);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("El domini de $f(x)=\\dfrac{x+1}{x^2-9}$ és…", "El dominio de $f(x)=\\dfrac{x+1}{x^2-9}$ es…", "The domain of $f(x)=\\dfrac{x+1}{x^2-9}$ is…"),
      o: [q3("$\\mathbb R$"), q3("$\\mathbb R-\\{-3,3\\}$"), q3("$\\mathbb R-\\{-1\\}$")], a: 1, e: q3("El denominador s'anul·la en $x^2=9\\Rightarrow x=\\pm3$.", "El denominador se anula en $x^2=9\\Rightarrow x=\\pm3$.", "The denominator is zero when $x^2=9\\Rightarrow x=\\pm3$.") },
    { q: q3("El domini de $f(x)=\\ln(x-2)$ és…", "El dominio de $f(x)=\\ln(x-2)$ es…", "The domain of $f(x)=\\ln(x-2)$ is…"),
      o: [q3("$[2,+\\infty)$"), q3("$(2,+\\infty)$"), q3("$\\mathbb R-\\{2\\}$")], a: 1, e: q3("L'argument del logaritme ha de ser positiu: $x-2\\gt0$.", "El argumento del logaritmo tiene que ser positivo: $x-2\\gt0$.", "The argument of the logarithm must be positive: $x-2\\gt0$.") },
    { q: q3("Els punts de tall de $f(x)=x^2-4x$ amb l'eix OX són…", "Los puntos de corte de $f(x)=x^2-4x$ con el eje OX son…", "The x-intercepts of $f(x)=x^2-4x$ are…"),
      o: [q3("$(0,0)$ i $(4,0)$", "$(0,0)$ y $(4,0)$", "$(0,0)$ and $(4,0)$"), q3("$(0,0)$ i $(-4,0)$", "$(0,0)$ y $(-4,0)$", "$(0,0)$ and $(-4,0)$"), q3("$(0,-4)$")], a: 0, e: q3("$x^2-4x=x(x-4)=0\\Rightarrow x=0,\\ x=4$.") },
    { q: q3("Si $f(-x)=-f(x)$ per a tot $x$ del domini, la funció és…", "Si $f(-x)=-f(x)$ para todo $x$ del dominio, la función es…", "If $f(-x)=-f(x)$ for every $x$ in the domain, the function is…"),
      o: [q3("parella: simètrica respecte de l'eix OY", "par: simétrica respecto del eje OY", "even: symmetric about the y-axis"), q3("senar: simètrica respecte de l'origen", "impar: simétrica respecto del origen", "odd: symmetric about the origin"), q3("periòdica", "periódica", "periodic")], a: 1,
      e: q3("Per exemple, $f(x)=x^3-3x$.", "Por ejemplo, $f(x)=x^3-3x$.", "For example, $f(x)=x^3-3x$.") },
    { q: q3("$f(x)=x^4-3x^2+1$ és…", "$f(x)=x^4-3x^2+1$ es…", "$f(x)=x^4-3x^2+1$ is…"),
      o: [q3("parella", "par", "even"), q3("senar", "impar", "odd"), q3("ni parella ni senar", "ni par ni impar", "neither")], a: 0, e: q3("Només hi ha potències parelles de $x$: $f(-x)=f(x)$.", "Solo hay potencias pares de $x$: $f(-x)=f(x)$.", "Only even powers of $x$ appear: $f(-x)=f(x)$.") },
    { q: q3("Les asímptotes de $f(x)=\\dfrac{2x+1}{x-3}$ són…", "Las asíntotas de $f(x)=\\dfrac{2x+1}{x-3}$ son…", "The asymptotes of $f(x)=\\dfrac{2x+1}{x-3}$ are…"),
      o: [q3("$x=3$ i $y=2$", "$x=3$ y $y=2$", "$x=3$ and $y=2$"), q3("$x=-3$ i $y=2$", "$x=-3$ y $y=2$", "$x=-3$ and $y=2$"), q3("$x=3$ i $y=0$", "$x=3$ y $y=0$", "$x=3$ and $y=0$")], a: 0,
      e: q3("El denominador s'anul·la en $x=3$; els graus són iguals: $y=\\frac21=2$.", "El denominador se anula en $x=3$; los grados son iguales: $y=\\frac21=2$.", "The denominator is zero at $x=3$; equal degrees: $y=\\frac21=2$.") },
    { q: q3("Una funció racional $\\frac{P(x)}{Q(x)}$ té asímptota obliqua quan…", "Una función racional $\\frac{P(x)}{Q(x)}$ tiene asíntota oblicua cuando…", "A rational function $\\frac{P(x)}{Q(x)}$ has an oblique asymptote when…"),
      o: [q3("grau $P$ = grau $Q$", "grado $P$ = grado $Q$", "deg $P$ = deg $Q$"), q3("grau $P$ = grau $Q$ + 1", "grado $P$ = grado $Q$ + 1", "deg $P$ = deg $Q$ + 1"), q3("grau $P$ < grau $Q$", "grado $P$ < grado $Q$", "deg $P$ < deg $Q$")], a: 1,
      e: q3("Aleshores el quocient de la divisió és de grau 1: $y=mx+n$.", "Entonces el cociente de la división es de grado 1: $y=mx+n$.", "Then the quotient of the division has degree 1: $y=mx+n$.") },
    { q: q3("L'asímptota obliqua de $f(x)=\\dfrac{x^2+3}{x-1}$ és…", "La asíntota oblicua de $f(x)=\\dfrac{x^2+3}{x-1}$ es…", "The oblique asymptote of $f(x)=\\dfrac{x^2+3}{x-1}$ is…"),
      o: [q3("$y=x$"), q3("$y=x+1$"), q3("$y=x-1$")], a: 1, e: q3("$x^2+3=(x-1)(x+1)+4$: el quocient és $x+1$.", "$x^2+3=(x-1)(x+1)+4$: el cociente es $x+1$.", "$x^2+3=(x-1)(x+1)+4$: the quotient is $x+1$.") },
    { q: q3("La funció $f(x)=e^x+2$ té…", "La función $f(x)=e^x+2$ tiene…", "The function $f(x)=e^x+2$ has…"),
      o: [q3("asímptota horitzontal $y=2$ quan $x\\to-\\infty$", "asíntota horizontal $y=2$ cuando $x\\to-\\infty$", "horizontal asymptote $y=2$ as $x\\to-\\infty$"), q3("asímptota vertical $x=2$", "asíntota vertical $x=2$", "vertical asymptote $x=2$"), q3("asímptota horitzontal $y=2$ quan $x\\to+\\infty$", "asíntota horizontal $y=2$ cuando $x\\to+\\infty$", "horizontal asymptote $y=2$ as $x\\to+\\infty$")], a: 0,
      e: q3("$\\lim_{x\\to-\\infty}e^x=0$, així que $f(x)\\to2$.", "$\\lim_{x\\to-\\infty}e^x=0$, así que $f(x)\\to2$.", "$\\lim_{x\\to-\\infty}e^x=0$, so $f(x)\\to2$.") },
    { q: q3("La funció $f(x)=\\ln x$ té una asímptota…", "La función $f(x)=\\ln x$ tiene una asíntota…", "The function $f(x)=\\ln x$ has an asymptote…"),
      o: [q3("vertical $x=0$", "vertical $x=0$", "vertical, $x=0$"), q3("horitzontal $y=0$", "horizontal $y=0$", "horizontal, $y=0$"), q3("vertical $x=1$", "vertical $x=1$", "vertical, $x=1$")], a: 0,
      e: q3("$\\lim_{x\\to0^+}\\ln x=-\\infty$.") },
    { q: q3("Una funció polinòmica…", "Una función polinómica…", "A polynomial function…"),
      o: [q3("sempre té asímptota horitzontal", "siempre tiene asíntota horizontal", "always has a horizontal asymptote"), q3("no té asímptotes", "no tiene asíntotas", "has no asymptotes"), q3("té asímptotes verticals on s'anul·la", "tiene asíntotas verticales donde se anula", "has vertical asymptotes at its zeros")], a: 1,
      e: q3("Té domini $\\mathbb R$ i als extrems tendeix a $\\pm\\infty$ (si no és constant ni de grau 1).", "Tiene dominio $\\mathbb R$ y en los extremos tiende a $\\pm\\infty$ (si no es constante ni de grado 1).", "Its domain is $\\mathbb R$ and it tends to $\\pm\\infty$ at both ends (unless it is constant or of degree 1).") },
    { q: q3("En una funció a trossos, els punts que cal estudiar sempre a banda són…", "En una función a trozos, los puntos que hay que estudiar siempre aparte son…", "In a piecewise function, the points that must always be studied separately are…"),
      o: [q3("els punts on canvia la definició", "los puntos donde cambia la definición", "the points where the definition changes"), q3("els talls amb OY", "los cortes con OY", "the y-intercepts"), q3("els enters", "los enteros", "the integers")], a: 0,
      e: q3("Allà pot haver-hi salts o punts angulosos, i també màxims o mínims.", "Allí puede haber saltos o puntos angulosos, y también máximos o mínimos.", "There may be jumps or corners there, and also maxima or minima.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Representació gràfica de funcions · FentMates", es: "Representación gráfica de funciones · FentMates", en: "Graphing functions · FentMates" };
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
      document.querySelectorAll(".widget .wt, .widget label, .widget .ttl, .widget .legend, #w-lab label, #w-lab .legend").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFigs, wDom, wCut, wSym, wAsy, wObl, wMx, wEl, wPw, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM7 = { parse: parse, fullStudy: fullStudy, domainOf: domainOf, asyOf: asyOf, pDiv: pDiv, pwStudy: pwStudy };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
