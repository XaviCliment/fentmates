(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-mii-u6-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt",
      cont: "contínua", ev: "evitable", sf: "salt finit", si: "salt infinit", as: "asimptòtica", pc: "si", rest: "en la resta", interval: "Interval",
      der: "derivable", nder: "no derivable", ang: "punt anguló", vt: "tangent vertical", cusp: "punt de retrocés", ncont: "no contínua",
      bad: "No entenc l'expressió: revisa-la.", aBad: "Escriu un nombre per al punt.", noDiff: "Aquesta expressió no la sé derivar amb les regles de la unitat (el valor absolut cal escriure'l a trossos).",
      tvm: "Taxa de variació mitjana", slope: "pendent de la recta secant", tang: "recta tangent", sec: "recta secant", exact: "Valor exacte (amb les regles de derivació)",
      est: "Estimació numèrica", left: "per l'esquerra", right2: "per la dreta", noLim: "Els dos quocients no s'acosten al mateix valor: no existeix la derivada.",
      quot: "quocient incremental", trap: "Compte! El producte de les derivades no és la derivada del producte:",
      sum: "Derivada d'una suma o resta: derivem terme a terme.", kf: "Constant per una funció: la constant es queda multiplicant.", fk: "Funció dividida per una constant: derivem el numerador.",
      prod: "Derivada d'un producte:", quo: "Derivada d'un quocient:", powx: "Derivada d'una potència de x:", neg: "Canvi de signe:", cst: "És una constant: la derivada és 0.",
      chain: "Funció composta: regla de la cadena.", outer: "funció de fora", inner: "funció de dins", elem: "Derivada d'una funció elemental (taula):", res: "Resultat",
      pointA: "En el punt", tline: "Recta tangent", isCD: "Contínua i derivable!", isC: "Contínua, però no derivable en", notC: "Encara no és contínua", almost: "Pràcticament contínua i derivable (diferències < 0,01): l'exacte és",
      wantC: "Contínua!", dl: "derivada per l'esquerra", dr: "derivada per la dreta", junction: "Punts on canvia l'expressió", pieceDer: "Derivem tros per tros (sense l'igual en els punts de canvi):",
      chkPieces: "Comprova també que cada tros siga derivable en el seu interval obert.", derAll: "La funció és derivable en tot el seu domini.", derExc: "La funció és derivable excepte en", andW: "i",
      zoomTip: "Fes zoom: si és derivable, la corba s'acaba confonent amb una recta.", fpoint: "Si \\(f\\) no és contínua en \\(a\\), no és derivable.",
      pTvm: ["Altura s(t)", "Població 2^x", "x³/3 − x"], pSec: ["x²", "√x", "x³ − 3x", "eˣ", "1/x", "sin x"], pQuot: ["x³ − 2x", "1/x²", "√(2x+1)", "sin x", "|x − 1|"],
      pRules: ["x² i x³", "x i eˣ", "Quocient", "ln x i x²"], pChain: ["(x²+1)⁵", "√(3x−1)", "e^(x²−x)", "ln(cos x)", "sin² 3x", "arctan √x", "e^(sin x)", "cos³ x", "tan x²", "arcsin 2x"],
      pZoom: ["x² en 1", "|x − 1| en 1", "∛x en 0", "∛x² en 0", "x|x| en 0", "Salt", "Unió suau"], pPwd: ["Exemple resum", "|x² − 4x|", "PAU Madrid 2022", "Trossos trigonomètrics", "PAU Astúries 2025", "PAU Navarra 2024"],
      pPar: ["PAU Andalusia 2022", "Amb logaritme", "PAU Andalusia 2020", "Amb sinus", "PAU Aragó 2022"], pLab: ["Polinomi", "Producte", "Quocient", "xˣ", "Arrel", "Logaritme", "Arctangent"],
      pLogd: ["xˣ", "x^(sin x)", "(sin x)^x", "(x²+1)^x", "x^(1/x)", "(ln x)^x"], pImpl: ["Circumferència", "El·lipse", "Full de Descartes", "x²+xy+y²=7", "y² = x³ − x + 1", "eʸ + xy = e", "x²y + y³ = 10"],
      logd: "Derivació logarítmica: hi ha x a la base i a l'exponent.", takeLn: "Prenem logaritmes neperians:", derBoth: "Derivem els dos membres (a l'esquerra, regla de la cadena):", isolate: "Aïllem y' i substituïm y:", uPos: "Cal que la base siga positiva: u(a) > 0.", impl: "Derivem els dos membres respecte de x, tenint en compte que y = y(x) (regla de la cadena) i aïllem y'. És el mateix que fer", notOn: "El punt no és de la corba: F(x₀, y₀) ≠ 0.", vtan: "Tangent vertical", normal: "Recta normal", eqBad: "Escriu una equació amb un signe =, per exemple x^2+y^2=25.", onC: "El punt és de la corba." },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba",
      cont: "continua", ev: "evitable", sf: "salto finito", si: "salto infinito", as: "asintótica", pc: "si", rest: "en el resto", interval: "Intervalo",
      der: "derivable", nder: "no derivable", ang: "punto anguloso", vt: "tangente vertical", cusp: "punto de retroceso", ncont: "no continua",
      bad: "No entiendo la expresión: revísala.", aBad: "Escribe un número para el punto.", noDiff: "Esta expresión no la sé derivar con las reglas de la unidad (el valor absoluto hay que escribirlo a trozos).",
      tvm: "Tasa de variación media", slope: "pendiente de la recta secante", tang: "recta tangente", sec: "recta secante", exact: "Valor exacto (con las reglas de derivación)",
      est: "Estimación numérica", left: "por la izquierda", right2: "por la derecha", noLim: "Los dos cocientes no se acercan al mismo valor: no existe la derivada.",
      quot: "cociente incremental", trap: "¡Cuidado! El producto de las derivadas no es la derivada del producto:",
      sum: "Derivada de una suma o resta: derivamos término a término.", kf: "Constante por una función: la constante se queda multiplicando.", fk: "Función dividida por una constante: derivamos el numerador.",
      prod: "Derivada de un producto:", quo: "Derivada de un cociente:", powx: "Derivada de una potencia de x:", neg: "Cambio de signo:", cst: "Es una constante: la derivada es 0.",
      chain: "Función compuesta: regla de la cadena.", outer: "función de fuera", inner: "función de dentro", elem: "Derivada de una función elemental (tabla):", res: "Resultado",
      pointA: "En el punto", tline: "Recta tangente", isCD: "¡Continua y derivable!", isC: "Continua, pero no derivable en", notC: "Todavía no es continua", almost: "Prácticamente continua y derivable (diferencias < 0,01): el exacto es",
      wantC: "¡Continua!", dl: "derivada por la izquierda", dr: "derivada por la derecha", junction: "Puntos donde cambia la expresión", pieceDer: "Derivamos trozo a trozo (sin el igual en los puntos de cambio):",
      chkPieces: "Comprueba también que cada trozo sea derivable en su intervalo abierto.", derAll: "La función es derivable en todo su dominio.", derExc: "La función es derivable excepto en", andW: "y",
      zoomTip: "Haz zoom: si es derivable, la curva acaba confundiéndose con una recta.", fpoint: "Si \\(f\\) no es continua en \\(a\\), no es derivable.",
      pTvm: ["Altura s(t)", "Población 2^x", "x³/3 − x"], pSec: ["x²", "√x", "x³ − 3x", "eˣ", "1/x", "sen x"], pQuot: ["x³ − 2x", "1/x²", "√(2x+1)", "sen x", "|x − 1|"],
      pRules: ["x² y x³", "x y eˣ", "Cociente", "ln x y x²"], pChain: ["(x²+1)⁵", "√(3x−1)", "e^(x²−x)", "ln(cos x)", "sen² 3x", "arctg √x", "e^(sen x)", "cos³ x", "tg x²", "arcsen 2x"],
      pZoom: ["x² en 1", "|x − 1| en 1", "∛x en 0", "∛x² en 0", "x|x| en 0", "Salto", "Unión suave"], pPwd: ["Ejemplo resumen", "|x² − 4x|", "PAU Madrid 2022", "Trozos trigonométricos", "PAU Asturias 2025", "PAU Navarra 2024"],
      pPar: ["PAU Andalucía 2022", "Con logaritmo", "PAU Andalucía 2020", "Con seno", "PAU Aragón 2022"], pLab: ["Polinomio", "Producto", "Cociente", "xˣ", "Raíz", "Logaritmo", "Arcotangente"],
      pLogd: ["xˣ", "x^(sen x)", "(sen x)^x", "(x²+1)^x", "x^(1/x)", "(ln x)^x"], pImpl: ["Circunferencia", "Elipse", "Folium de Descartes", "x²+xy+y²=7", "y² = x³ − x + 1", "eʸ + xy = e", "x²y + y³ = 10"],
      logd: "Derivación logarítmica: hay x en la base y en el exponente.", takeLn: "Tomamos logaritmos neperianos:", derBoth: "Derivamos los dos miembros (a la izquierda, regla de la cadena):", isolate: "Despejamos y' y sustituimos y:", uPos: "La base tiene que ser positiva: u(a) > 0.", impl: "Derivamos los dos miembros respecto de x, teniendo en cuenta que y = y(x) (regla de la cadena) y despejamos y'. Es lo mismo que hacer", notOn: "El punto no es de la curva: F(x₀, y₀) ≠ 0.", vtan: "Tangente vertical", normal: "Recta normal", eqBad: "Escribe una ecuación con un signo =, por ejemplo x^2+y^2=25.", onC: "El punto es de la curva." },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top",
      cont: "continuous", ev: "removable", sf: "finite jump", si: "infinite jump", as: "asymptotic", pc: "if", rest: "otherwise", interval: "Interval",
      der: "differentiable", nder: "not differentiable", ang: "corner point", vt: "vertical tangent", cusp: "cusp", ncont: "not continuous",
      bad: "I can't read that expression: check it.", aBad: "Type a number for the point.", noDiff: "I can't differentiate this with the rules of the unit (write absolute values piecewise).",
      tvm: "Average rate of change", slope: "slope of the secant line", tang: "tangent line", sec: "secant line", exact: "Exact value (with the differentiation rules)",
      est: "Numerical estimate", left: "from the left", right2: "from the right", noLim: "The two quotients do not approach the same value: the derivative does not exist.",
      quot: "difference quotient", trap: "Careful! The product of the derivatives is not the derivative of the product:",
      sum: "Derivative of a sum or difference: differentiate term by term.", kf: "Constant times a function: the constant stays as a factor.", fk: "Function divided by a constant: differentiate the numerator.",
      prod: "Product rule:", quo: "Quotient rule:", powx: "Power rule:", neg: "Change of sign:", cst: "It is a constant: the derivative is 0.",
      chain: "Composite function: chain rule.", outer: "outer function", inner: "inner function", elem: "Derivative of an elementary function (table):", res: "Result",
      pointA: "At the point", tline: "Tangent line", isCD: "Continuous and differentiable!", isC: "Continuous, but not differentiable at", notC: "Not continuous yet", almost: "Practically continuous and differentiable (differences < 0.01): the exact value is",
      wantC: "Continuous!", dl: "left-hand derivative", dr: "right-hand derivative", junction: "Points where the formula changes", pieceDer: "Differentiate piece by piece (no equals sign at the break points):",
      chkPieces: "Also check that each piece is differentiable on its open interval.", derAll: "The function is differentiable on its whole domain.", derExc: "The function is differentiable except at", andW: "and",
      zoomTip: "Zoom in: if it is differentiable, the curve ends up looking like a straight line.", fpoint: "If \\(f\\) is not continuous at \\(a\\), it is not differentiable.",
      pTvm: ["Height s(t)", "Population 2^x", "x³/3 − x"], pSec: ["x²", "√x", "x³ − 3x", "eˣ", "1/x", "sin x"], pQuot: ["x³ − 2x", "1/x²", "√(2x+1)", "sin x", "|x − 1|"],
      pRules: ["x² and x³", "x and eˣ", "Quotient", "ln x and x²"], pChain: ["(x²+1)⁵", "√(3x−1)", "e^(x²−x)", "ln(cos x)", "sin² 3x", "arctan √x", "e^(sin x)", "cos³ x", "tan x²", "arcsin 2x"],
      pZoom: ["x² at 1", "|x − 1| at 1", "∛x at 0", "∛x² at 0", "x|x| at 0", "Jump", "Smooth join"], pPwd: ["Summary example", "|x² − 4x|", "PAU Madrid 2022", "Trigonometric pieces", "PAU Asturias 2025", "PAU Navarre 2024"],
      pPar: ["PAU Andalusia 2022", "With a logarithm", "PAU Andalusia 2020", "With sine", "PAU Aragon 2022"], pLab: ["Polynomial", "Product", "Quotient", "xˣ", "Root", "Logarithm", "Arctangent"],
      pLogd: ["xˣ", "x^(sin x)", "(sin x)^x", "(x²+1)^x", "x^(1/x)", "(ln x)^x"], pImpl: ["Circle", "Ellipse", "Folium of Descartes", "x²+xy+y²=7", "y² = x³ − x + 1", "eʸ + xy = e", "x²y + y³ = 10"],
      logd: "Logarithmic differentiation: x appears in both the base and the exponent.", takeLn: "Take natural logarithms:", derBoth: "Differentiate both sides (on the left, chain rule):", isolate: "Solve for y' and substitute y:", uPos: "The base must be positive: u(a) > 0.", impl: "Differentiate both sides with respect to x, remembering that y = y(x) (chain rule), and solve for y'. It is the same as computing", notOn: "The point is not on the curve: F(x₀, y₀) ≠ 0.", vtan: "Vertical tangent", normal: "Normal line", eqBad: "Type an equation with an = sign, for example x^2+y^2=25.", onC: "The point lies on the curve." }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }

  /*@@CORE@@*/
  /* ---------- derivació simbòlica ---------- */
  function strip0(n) { while (n.t === "()") n = n.a; return n; }
  function num(v) { return v < 0 ? { t: "neg", a: num(-v) } : { t: "n", v: v, s: String(v) }; }
  var ZERO = num(0), ONE = num(1);
  function frNode(f) {
    if (f.n < 0) return { t: "neg", a: frNode(new Fr(-f.n, f.d)) };
    if (f.d > 1 && /^10*$/.test(String(f.d))) return num(+(f.n / f.d).toFixed(String(f.d).length - 1)); // decimals de l'enunciat
    return f.d === 1 ? num(f.n) : { t: "/", a: num(f.n), b: num(f.d) };
  }
  // valor racional d'una expressió constant (o null)
  function cst(n) {
    n = strip0(n);
    switch (n.t) {
      case "n": return decFr(n.s);
      case "neg": { var a = cst(n.a); return a && new Fr(-a.n, a.d); }
      case "+": case "-": case "*": case "/": {
        var p = cst(n.a), q = cst(n.b); if (!p || !q) return null;
        if (n.t === "+") return p.add(q); if (n.t === "-") return p.sub(q); if (n.t === "*") return p.mul(q);
        return q.zero() ? null : p.div(q);
      }
      case "^": {
        var b = cst(n.a), e = cst(n.b); if (!b || !e || e.d !== 1 || Math.abs(e.n) > 12) return null;
        if (b.zero() && e.n <= 0) return null;
        var r = new Fr(1); for (var i = 0; i < Math.abs(e.n); i++) r = r.mul(b);
        return e.n < 0 ? new Fr(1).div(r) : r;
      }
    }
    return null;
  }
  function isN(n, v) { var c = cst(n); return !!c && c.n === v && c.d === 1; }
  function indep(n) {
    if (!n || typeof n !== "object") return true;
    if (n.t === "v") return n.n !== "x" && n.n !== "t";
    return indep(n.a) && indep(n.b);
  }
  function B(t, a, b) { return { t: t, a: a, b: b }; }
  function Fn(name, a) { return { t: "f", n: name, a: a }; }
  function simp(n) {
    n = strip0(n);
    if (n.t === "n" || n.t === "v" || n.t === "c") return n;
    if (n.t === "f") return Fn(n.n, simp(n.a));
    var a = n.a ? simp(n.a) : null, b = n.b ? simp(n.b) : null;
    var m = { t: n.t, a: a, b: b };
    if (n.t !== "neg" && a && b && cst(a) && cst(b) && (n.t !== "^" || cst(m))) { var c = cst(m); if (c) return frNode(c); }
    switch (n.t) {
      case "neg":
        if (a.t === "neg") return a.a;
        if (isN(a, 0)) return ZERO;
        return { t: "neg", a: a };
      case "+":
        if (isN(a, 0)) return b; if (isN(b, 0)) return a;
        if (b.t === "neg") return simp(B("-", a, b.a));
        if (a.t === "neg") return simp(B("-", b, a.a));
        return m;
      case "-":
        if (isN(b, 0)) return a; if (isN(a, 0)) return simp({ t: "neg", a: b });
        if (b.t === "neg") return simp(B("+", a, b.a));
        return m;
      case "*": case "/":
        if (isN(a, 0)) return ZERO;
        if (n.t === "*" && isN(b, 0)) return ZERO;
        return prodNorm(m);
      case "^":
        if (isN(b, 0)) return ONE; if (isN(b, 1)) return a; if (isN(a, 1)) return ONE;
        var e = cst(b);
        if (e && e.n === 1 && e.d === 2) return Fn("sqrt", a);
        if (e && e.n < 0) return simp(B("/", ONE, B("^", a, frNode(new Fr(-e.n, e.d)))));
        if (a.t === "^" && cst(a.b) && e) return simp(B("^", a.a, frNode(cst(a.b).mul(e))));
        if (a.t === "f" && a.n === "sqrt" && e) return simp(B("^", a.a, frNode(e.mul(new Fr(1, 2)))));
        return m;
    }
    return m;
  }
  // productes i quocients: ajuntem constants i potències de la mateixa base i simplifiquem factors comuns
  function mkPow(b, k) {
    if (k.n === k.d) return b;
    if (k.n === 1 && k.d === 2) return Fn("sqrt", b);
    return B("^", b, frNode(k));
  }
  function rank(b) { b = strip0(b); return b.t === "v" ? 0 : (b.t === "+" || b.t === "-") ? 1 : b.t === "f" ? 3 : 2; }
  function prodNorm(n) {
    var c = new Fr(1), fs = [];
    (function col(m, e) {
      m = strip0(m);
      if (m.t === "*") { col(m.a, e); col(m.b, e); return; }
      if (m.t === "/") { col(m.a, e); col(m.b, -e); return; }
      if (m.t === "neg") { c = new Fr(-c.n, c.d); col(m.a, e); return; }
      var k = cst(m);
      if (k) { c = e > 0 ? c.mul(k) : c.div(k); return; }
      var base = m, ex = new Fr(e);
      if (m.t === "^" && cst(m.b)) { base = strip0(m.a); ex = cst(m.b).mul(new Fr(e)); }
      var key = texD(base), hit = null;
      fs.forEach(function (f) { if (f.key === key) hit = f; });
      if (hit) hit.k = hit.k.add(ex); else fs.push({ key: key, b: base, k: ex });
    })(n, 1);
    if (c.zero()) return ZERO;
    fs = fs.filter(function (f) { return !f.k.zero(); });
    fs.sort(function (p, q) { return rank(p.b) - rank(q.b); });
    function build(list, k0) {
      var out = k0 === 1 ? null : num(k0);
      list.forEach(function (f) { out = out ? B("*", out, f) : f; });
      return out || ONE;
    }
    var up = fs.filter(function (f) { return f.k.n > 0; }).map(function (f) { return mkPow(f.b, f.k); });
    var dn = fs.filter(function (f) { return f.k.n < 0; }).map(function (f) { return mkPow(f.b, new Fr(-f.k.n, f.k.d)); });
    var r = build(up, Math.abs(c.n));
    if (dn.length || c.d !== 1) r = B("/", r, build(dn, c.d));
    return c.n < 0 ? { t: "neg", a: r } : r;
  }
  // si una expressió és un polinomi de grau petit, l'escrivim desenvolupat i ordenat
  function polyNode(p) {
    var out = null;
    for (var k = p.length - 1; k >= 0; k--) {
      var c = p[k]; if (c.zero()) continue;
      var ab = new Fr(Math.abs(c.n), c.d), xk = k === 0 ? null : k === 1 ? { t: "v", n: "x" } : B("^", { t: "v", n: "x" }, num(k));
      var t = !xk ? frNode(ab) : (ab.n === 1 && ab.d === 1 ? xk : (ab.d === 1 ? B("*", num(ab.n), xk) : B("/", B("*", num(ab.n), xk), num(ab.d))));
      out = !out ? (c.n < 0 ? { t: "neg", a: t } : t) : B(c.n < 0 ? "-" : "+", out, t);
    }
    return out || ZERO;
  }
  function polyTry(n) {
    try { var p = pTrim(polyOf(n)); if (p.length <= 7 && p.filter(function (c) { return !c.zero(); }).length <= 6) return polyNode(p); } catch (e) {}
    return null;
  }
  function tidy(n) {
    // només desenvolupem sumes (un producte com 6x(x²+2)² es queda factoritzat)
    n = strip0(n);
    var sum = function (m) { m = strip0(m); return m.t === "+" || m.t === "-"; };
    if (sum(n)) { var p = polyTry(n); if (p) return p; }
    if (n.t === "neg") return { t: "neg", a: tidy(n.a) };
    if (n.t === "/" && sum(n.a)) { var q = polyTry(n.a); if (q) return simp(B("/", q, n.b)); }
    return n;
  }
  function NoDiff() { this.name = "NoDiff"; }
  function d(n) {
    n = strip0(n);
    if (indep(n)) return ZERO;
    switch (n.t) {
      case "v": return ONE;
      case "neg": return { t: "neg", a: d(n.a) };
      case "+": case "-": return B(n.t, d(n.a), d(n.b));
      case "*":
        if (indep(n.a)) return B("*", n.a, d(n.b));
        if (indep(n.b)) return B("*", n.b, d(n.a));
        return B("+", B("*", d(n.a), n.b), B("*", n.a, d(n.b)));
      case "/":
        if (indep(n.b)) return B("/", d(n.a), n.b);
        return B("/", B("-", B("*", d(n.a), n.b), B("*", n.a, d(n.b))), B("^", n.b, num(2)));
      case "^": {
        var b = strip0(n.a), e = strip0(n.b);
        if (indep(e)) return B("*", B("*", e, B("^", b, B("-", e, ONE))), d(b));
        if (indep(b)) return b.t === "c" && b.n === "e" ? B("*", B("^", b, e), d(e)) : B("*", B("*", B("^", b, e), Fn("ln", b)), d(e));
        // derivació logarítmica: (u^v)' = u^v·(v'·ln u + v·u'/u)
        return B("*", B("^", b, e), B("+", B("*", d(e), Fn("ln", b)), B("/", B("*", e, d(b)), b)));
      }
      case "f": {
        var g = n.a, dg = d(g);
        switch (n.n) {
          case "sqrt": return B("/", dg, B("*", num(2), Fn("sqrt", g)));
          case "exp": return B("*", Fn("exp", g), dg);
          case "ln": return B("/", dg, g);
          case "log": return B("/", dg, B("*", g, Fn("ln", num(10))));
          case "sin": return B("*", Fn("cos", g), dg);
          case "cos": return { t: "neg", a: B("*", Fn("sin", g), dg) };
          case "tan": return B("/", dg, B("^", Fn("cos", g), num(2)));
          case "arcsin": return B("/", dg, Fn("sqrt", B("-", ONE, B("^", g, num(2)))));
          case "arccos": return { t: "neg", a: B("/", dg, Fn("sqrt", B("-", ONE, B("^", g, num(2))))) };
          case "arctan": return B("/", dg, B("+", ONE, B("^", g, num(2))));
        }
        throw new NoDiff();
      }
    }
    throw new NoDiff();
  }
  function D(n) { return tidy(simp(d(n))); }

  // TeX més polit que el de la unitat 4: sin x, cos² x, exponents amb \frac
  var FNAME = { sin: "\\sin", cos: "\\cos", tan: "\\tan", arcsin: "\\arcsin", arccos: "\\arccos", arctan: "\\arctan", ln: "\\ln", log: "\\log" };
  function simpleArg(n) { n = strip0(n); return n.t === "v" || n.t === "n" || n.t === "c" || (n.t === "*" && strip0(n.a).t === "n" && strip0(n.b).t === "v"); }
  function texD(n, inExp) {
    n = strip0(n);
    function wrapSum(m) { m = strip0(m); var s = texD(m, inExp); return (m.t === "+" || m.t === "-" || m.t === "neg") ? "\\left(" + s + "\\right)" : s; }
    switch (n.t) {
      case "n": return decTex(n.s);
      case "c": return n.n === "e" ? "e" : "\\pi";
      case "v": return n.n;
      case "neg": return "-" + wrapSum(n.a);
      case "+": return texD(n.a, inExp) + "+" + texD(n.b, inExp);
      case "-": return texD(n.a, inExp) + "-" + wrapSum(n.b);
      case "*": {
        var l = strip0(n.a), r = strip0(n.b), tl = texD(l, inExp), tr = texD(r, inExp);
        if (l.t === "+" || l.t === "-") tl = "\\left(" + tl + "\\right)";
        if (r.t === "+" || r.t === "-" || r.t === "neg") tr = "\\left(" + tr + "\\right)";
        var dot = (/^[0-9]/.test(tr) || r.t === "n" || r.t === "/" || (r.t === "^" && strip0(r.a).t === "n")) ? "\\cdot " : l.t === "n" ? "" : "\\,";
        return tl + dot + tr;
      }
      case "/": return (inExp ? "\\frac{" : "\\dfrac{") + texD(n.a, inExp) + "}{" + texD(n.b, inExp) + "}";
      case "^": {
        var base = strip0(n.a), ex = texD(n.b, true), q = cst(n.b);
        if (q && q.d > 1 && q.n > 0 && !(base.t === "c")) return "\\sqrt" + (q.d === 2 ? "" : "[" + q.d + "]") + "{" + (q.n === 1 ? texD(base) : texD(B("^", base, num(q.n)))) + "}";
        if (base.t === "f" && FNAME[base.n] && base.n !== "ln" && base.n !== "log") return FNAME[base.n] + "^{" + ex + "}" + (simpleArg(base.a) ? " " + texD(base.a) : "\\left(" + texD(base.a) + "\\right)");
        var tb = texD(base, inExp);
        if (base.t !== "n" && base.t !== "v" && base.t !== "c") tb = "\\left(" + tb + "\\right)";
        return tb + "^{" + ex + "}";
      }
      case "f": {
        var arg = texD(n.a, inExp);
        if (n.n === "sqrt") return "\\sqrt{" + arg + "}";
        if (n.n === "abs") return "\\left|" + arg + "\\right|";
        if (n.n === "exp") return "e^{" + texD(n.a, true) + "}";
        return FNAME[n.n] + (simpleArg(n.a) ? " " + arg : "\\left(" + arg + "\\right)");
      }
    }
    return "?";
  }
  function T(src) { return texD(typeof src === "string" ? parse(src) : src); }
  function dOf(src) { return D(parse(src)); }

  // explicació pas a pas de la primera regla que cal aplicar
  var OUTER = {
    sqrt: "\\left[\\sqrt{g}\\right]'=\\dfrac{g'}{2\\sqrt{g}}", exp: "\\left[e^{g}\\right]'=e^{g}\\cdot g'", ln: "\\left[\\ln g\\right]'=\\dfrac{g'}{g}",
    log: "\\left[\\log g\\right]'=\\dfrac{g'}{g\\cdot\\ln 10}", sin: "\\left[\\sin g\\right]'=\\cos g\\cdot g'", cos: "\\left[\\cos g\\right]'=-\\sin g\\cdot g'",
    tan: "\\left[\\tan g\\right]'=\\dfrac{g'}{\\cos^2 g}", arcsin: "\\left[\\arcsin g\\right]'=\\dfrac{g'}{\\sqrt{1-g^2}}", arccos: "\\left[\\arccos g\\right]'=\\dfrac{-g'}{\\sqrt{1-g^2}}",
    arctan: "\\left[\\arctan g\\right]'=\\dfrac{g'}{1+g^2}"
  };
  var ELEM = {
    sqrt: "\\left(\\sqrt{x}\\right)'=\\dfrac{1}{2\\sqrt{x}}", exp: "\\left(e^{x}\\right)'=e^{x}", ln: "\\left(\\ln x\\right)'=\\dfrac1x", log: "\\left(\\log x\\right)'=\\dfrac{1}{x\\ln 10}",
    sin: "(\\sin x)'=\\cos x", cos: "(\\cos x)'=-\\sin x", tan: "(\\tan x)'=1+\\tan^2x=\\dfrac{1}{\\cos^2x}", arcsin: "(\\arcsin x)'=\\dfrac{1}{\\sqrt{1-x^2}}",
    arccos: "(\\arccos x)'=\\dfrac{-1}{\\sqrt{1-x^2}}", arctan: "(\\arctan x)'=\\dfrac{1}{1+x^2}"
  };
  function li(s) { return "<li>" + s + "</li>"; }
  function explain(src) {
    var n = strip0(parse(src)), res = D(n), fx = "f(x)=" + T(n), out = [];
    var gx = function (g) { g = strip0(g); return "g(x)=" + T(g) + ",\\quad g'(x)=" + T(D(g)); };
    if (indep(n)) out.push(u("cst"));
    else switch (n.t) {
      case "+": case "-": {
        var terms = [], st = [[n, 1]];
        while (st.length) { var p = st.pop(), q = strip0(p[0]); if (q.t === "+" || q.t === "-") { st.push([q.b, q.t === "-" ? -1 : 1]); st.push([q.a, 1]); } else terms.push(q); }
        out.push(u("sum") + "<ul>" + terms.map(function (t) { return li(tex("\\left(" + T(t) + "\\right)'=" + T(D(t)))); }).join("") + "</ul>");
        break;
      }
      case "neg": out.push(u("neg") + " " + tex("\\left(-g\\right)'=-g'") + ", " + tex(gx(n.a))); break;
      case "*":
        if (indep(n.a) || indep(n.b)) {
          var k = indep(n.a) ? n.a : n.b, g = indep(n.a) ? n.b : n.a;
          out.push(u("kf") + " " + tex("(k\\cdot g)'=k\\cdot g'") + "<br>" + tex("k=" + T(k) + ",\\quad " + gx(g)));
        } else {
          out.push(u("prod") + " " + tex("(u\\cdot v)'=u'\\cdot v+u\\cdot v'") + "<br>" + tex("u=" + T(n.a) + ",\\quad u'=" + T(D(n.a))) + "<br>" + tex("v=" + T(n.b) + ",\\quad v'=" + T(D(n.b))) +
            "<br>" + tex("f'(x)=" + texD(B("+", B("*", D(n.a), n.b), B("*", n.a, D(n.b))))));
        }
        break;
      case "/":
        if (indep(n.b)) { out.push(u("fk") + " " + tex("\\left(\\dfrac{g}{k}\\right)'=\\dfrac{g'}{k}") + "<br>" + tex("k=" + T(n.b) + ",\\quad " + gx(n.a))); break; }
        out.push(u("quo") + " " + tex("\\left(\\dfrac uv\\right)'=\\dfrac{u'\\cdot v-u\\cdot v'}{v^2}") + "<br>" + tex("u=" + T(n.a) + ",\\quad u'=" + T(D(n.a))) + "<br>" + tex("v=" + T(n.b) + ",\\quad v'=" + T(D(n.b))) +
          "<br>" + tex("f'(x)=\\dfrac{" + texD(B("-", B("*", D(n.a), n.b), B("*", n.a, D(n.b)))) + "}{" + texD(B("^", n.b, num(2))) + "}"));
        break;
      case "^": {
        var b = strip0(n.a), e = strip0(n.b);
        if (indep(e) && b.t === "v") out.push(u("powx") + " " + tex("(x^n)'=n\\,x^{n-1}") + ",\\ " + tex("n=" + texD(e, true)));
        else if (indep(e)) out.push(u("chain") + " " + tex("\\left[g^n\\right]'=n\\,g^{n-1}\\cdot g'") + "<br>" + tex("n=" + texD(e, true) + ",\\quad " + gx(b)));
        else if (b.t === "c" && b.n === "e") out.push((strip0(e).t === "v" ? u("elem") + " " + tex("(e^x)'=e^x") : u("chain") + " " + tex("\\left[e^{g}\\right]'=e^{g}\\cdot g'") + "<br>" + tex(gx(e))));
        else if (indep(b)) out.push((strip0(e).t === "v" ? u("elem") + " " + tex("(a^x)'=a^x\\cdot\\ln a") : u("chain") + " " + tex("\\left[a^{g}\\right]'=a^{g}\\cdot g'\\cdot\\ln a") + "<br>" + tex("a=" + T(b) + ",\\quad " + gx(e))));
        else out.push(u("logd") + "<br>" + tex("y=u^{v}\\ \\Rightarrow\\ \\ln y=v\\cdot\\ln u\\ \\Rightarrow\\ \\dfrac{y'}{y}=v'\\ln u+v\\,\\dfrac{u'}{u}") + "<br>" + tex("u=" + T(b) + ",\\quad u'=" + T(D(b))) + "<br>" + tex("v=" + T(e) + ",\\quad v'=" + T(D(e))));
        break;
      }
      case "f":
        if (n.n === "abs") throw new NoDiff();
        if (strip0(n.a).t === "v") out.push(u("elem") + " " + tex(ELEM[n.n]));
        else out.push(u("chain") + " " + tex(OUTER[n.n]) + "<br>" + u("inner") + ": " + tex(gx(n.a)));
        break;
    }
    return { html: "<p>" + tex(fx) + "</p>" + out.map(function (s) { return "<p>" + s + "</p>"; }).join("") + "<p><strong>" + u("res") + ":</strong> " + tex("f'(x)=" + texD(res)) + "</p>", d: res };
  }

  // valor numèric amb format
  // e^{1} -> e i e^{-1} -> 1/e (i niceTex no reconeix els negatius amb e)
  function nt(v) {
    if (isFinite(v) && v < 0 && niceTex(-v).indexOf("e^") === 0) return "-" + nt(-v);
    var t = niceTex(v); return t === "e^{1}" ? "e" : t === "e^{-1}" ? "\\frac1e" : t;
  }
  function badgeD(k) {
    var C = { der: "ok", nder: "as", ang: "sf", vt: "si", cusp: "si", ncont: "as" };
    return '<span class="badge ' + C[k] + '">' + u(k) + "</span>";
  }
  function lineTex(m, a, fa) { var b0 = fa - m * a; return "y=" + (Math.abs(m) < 1e-12 ? nt(fa) : (m === 1 ? "" : m === -1 ? "-" : nt(m)) + "x" + (Math.abs(b0) < 1e-12 ? "" : (b0 > 0 ? "+" : "") + nt(b0))); }
  function presetBtns(box, n, key, onPick) {
    var bs = [];
    for (var i = 0; i < n; i++) (function (i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { onPick(i); }); box.appendChild(b); bs.push(b);
    })(i);
    onLang(function () { bs.forEach(function (b, i) { b.textContent = u(key)[i]; }); });
    return bs;
  }
  function lineF(m, a, fa) { return function (x) { return fa + m * (x - a); }; }
  // límit lateral d'una expressió contínua en a: el seu valor (sideAt falla amb arrels com ∛x, que s'acosten molt a poc a poc)
  function contSide(g, a, side) {
    var y = g(a);
    if (isFinite(y) && Math.abs(g(a + side * 1e-12) - y) < 1e-3 * (1 + Math.abs(y))) return { k: "num", v: y };
    return sideAt(g, a, side);
  }
  // amb decimals a l'enunciat, escrivim els resultats amb decimals
  function limFmt(r, dec) { return dec && r.k === "num" ? numTex(+r.v.toFixed(6)) : limTex(r); }
  // derivades laterals a partir del quocient incremental
  function sideDer(f, a, side) { var fa = f(a); return limSide(function (x) { return (f(x) - fa) / (x - a); }, a, side); }
  // classificació de la derivabilitat en a
  function derClass(L, R, fa, dL, dR) {
    if (classify(L, R, fa) !== "ok") return "ncont";
    if (dL.k === "num" && dR.k === "num") return sameLim(dL, dR) ? "der" : "ang";
    if (dL.k === "inf" && dR.k === "inf" && dL.s === dR.s) return "vt";
    if (dL.k === "inf" && dR.k === "inf") return "cusp";
    return dL.k === "inf" || dR.k === "inf" ? (dL.k === "inf" && dR.k === "inf" ? "nder" : "nder") : "nder";
  }

  /* ---------- figures estàtiques ---------- */
  function F(s) { return compile(parse(s)); }
  var FIGS = {
    tvm: function () {
      var f = F("-x^2+10x"), m = (f(3) - f(1)) / 2;
      return { v: [-0.5, 7, -2, 28], curves: [{ f: f }, { f: lineF(m, 1, f(1)), col: "var(--accent-2)" }], pts: [{ x: 1, y: f(1) }, { x: 3, y: f(3) }], guides: [{ x: 1, y: f(1) }, { x: 3, y: f(3) }],
        labels: [{ x: 1, y: -1.4, t: "a" }, { x: 3, y: -1.4, t: "b" }, { x: 4.3, y: 26, t: "f(b) − f(a)", anchor: "start" }] };
    },
    tan: function () {
      var f = F("x^2/2+1");
      return { v: [-1, 4, -0.5, 7], curves: [{ f: f }, { f: lineF(1, 1, 1.5), col: "var(--accent-2)" }, { f: lineF(2.5, 1, 1.5), col: "var(--r3)" }, { f: lineF(1.6, 1, 1.5), col: "var(--r3)" }],
        pts: [{ x: 1, y: 1.5 }, { x: 4, y: 9 }, { x: 2.2, y: f(2.2), col: "var(--r3)" }], labels: [{ x: 0.9, y: 2.2, t: "P", anchor: "end" }, { x: 3.4, y: 3.6, t: "tangent", anchor: "start" }] };
    },
    abs: function () { return { v: [-3, 3, -1, 3], curves: [{ f: F("abs(x)") }, { f: lineF(-1, 0, 0), col: "var(--accent-2)", b: 0 }, { f: lineF(1, 0, 0), col: "var(--r3)", a: 0 }], pts: [{ x: 0, y: 0 }] }; },
    cbrt: function () { return { v: [-3, 3, -2, 2], curves: [{ f: F("x^(1/3)") }], guides: [{ x: 0 }], pts: [{ x: 0, y: 0 }] }; },
    cusp: function () { return { v: [-3, 3, -0.5, 2.5], curves: [{ f: F("x^(2/3)") }], guides: [{ x: 0 }], pts: [{ x: 0, y: 0 }] }; },
    norm: function () {
      return { v: [-1.5, 3.5, -1, 3], curves: [{ f: F("x^2/2") }, { f: lineF(1, 1, 0.5), col: "var(--accent-2)" }, { f: lineF(-1, 1, 0.5), col: "var(--r3)" }], pts: [{ x: 1, y: 0.5 }],
        labels: [{ x: 1.1, y: 0.1, t: "P", anchor: "start" }, { x: 2.9, y: 2.2, t: "t", anchor: "start" }, { x: -0.6, y: 2.4, t: "n", anchor: "end" }] };
    },
    jump: function () { return { v: [-1, 4, -1, 5], curves: [{ f: F("x+1"), b: 1 }, { f: F("x+2"), a: 1 }], pts: [{ x: 1, y: 2 }, { x: 1, y: 3, o: true }] }; },
    res: function () {
      var P = pwMake({ p: ["x+1", "x^2-1"], c: [2], inc: ["R"] }), v = [-1, 3.6, -1, 10], dr = pwDraw(P, v);
      return { v: v, curves: dr.curves.concat([{ f: lineF(1, 2, 3), col: "var(--accent-2)", a: 1, b: 2 }, { f: lineF(4, 2, 3), col: "var(--r3)", a: 2, b: 3 }]), pts: [{ x: 2, y: 3 }] };
    }
  };
  function wFigs() {
    document.querySelectorAll("[data-g]").forEach(function (el) {
      var mk = FIGS[el.getAttribute("data-g")]; if (!mk) return;
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "lp-svg"); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Gràfica");
      el.appendChild(svg);
      var cfg = mk();
      onLang(function () { plot(svg, cfg); });
    });
  }

  /* ---------- widget: taxa de variació mitjana ---------- */
  function wTvm() {
    var w = document.getElementById("w-tvm"); if (!w) return;
    var PRE = [{ e: "-5x^2+20x", v: [-0.5, 4.5, -3, 24], a: 0, b: 1 }, { e: "2^x", v: [-1, 5, -1, 24], a: 1, b: 3 }, { e: "x^3/3-x", v: [-3, 3, -4, 4], a: -1, b: 2 }];
    var st = 0, svg = w.querySelector("svg"), ra = $(w, "a"), rb = $(w, "b"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pTvm", function (i) { st = i; setup(); });
    [ra, rb].forEach(function (r) { r.addEventListener("input", draw); });
    function setup() { var P = PRE[st]; [ra, rb].forEach(function (r) { r.min = P.v[0]; r.max = P.v[1]; r.step = 0.1; }); ra.value = P.a; rb.value = P.b; draw(); }
    function draw() {
      var P = PRE[st], f = F(P.e), a = +ra.value, b = +rb.value;
      $(w, "av").textContent = numTxt(a); $(w, "bv").textContent = numTxt(b);
      var fa = f(a), fb = f(b), curves = [{ f: f }], h;
      h = "<p>" + tex("f(x)=" + T(P.e)) + "</p>";
      if (Math.abs(b - a) < 1e-9) h += "<p>" + tex("a=b") + "</p>";
      else {
        var m = (fb - fa) / (b - a);
        h += "<p>" + tex("\\text{TVM}[" + numTex(Math.min(a, b)) + "," + numTex(Math.max(a, b)) + "]=\\dfrac{f(" + numTex(b) + ")-f(" + numTex(a) + ")}{" + numTex(b) + "-" + (a < 0 ? "(" + numTex(a) + ")" : numTex(a)) + "}=\\dfrac{" + numTex(+fb.toFixed(4)) + "-" + (fa < 0 ? "(" + numTex(+fa.toFixed(4)) + ")" : numTex(+fa.toFixed(4))) + "}{" + numTex(+(b - a).toFixed(4)) + "}=" + numTex(+m.toFixed(4))) + "</p>";
        h += "<p>" + u("tvm") + " = " + u("slope") + ".</p>";
        curves.push({ f: lineF(m, a, fa), col: "var(--accent-2)" });
      }
      info.innerHTML = h;
      plot(svg, { v: P.v, curves: curves, pts: [{ x: a, y: fa }, { x: b, y: fb, col: COLS[1] }], guides: [{ x: a, y: fa }, { x: b, y: fb }] });
    }
    onLang(setup);
  }

  /* ---------- widget: de la secant a la tangent ---------- */
  function wSec() {
    var w = document.getElementById("w-sec"); if (!w) return;
    var PRE = [{ e: "x^2", a: 1, v: [-1.5, 3.4, -1, 8] }, { e: "sqrt(x)", a: 4, v: [-0.5, 8.5, -0.5, 3.5] }, { e: "x^3-3x", a: 1.5, v: [-2.5, 3.6, -4, 8] }, { e: "e^x", a: 0, v: [-2.5, 2.5, -1, 7] }, { e: "1/x", a: 1, v: [0, 3.5, -0.5, 4], hm: -0.8 }, { e: "sin(x)", a: 0, v: [-3.5, 3.5, -1.6, 1.6] }];
    var st = 0, svg = w.querySelector("svg"), rh = $(w, "h"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pSec", function (i) { st = i; setup(); });
    rh.addEventListener("input", draw);
    function setup() { var P = PRE[st]; rh.min = P.hm || -2; rh.max = 2; rh.step = 0.01; rh.value = 1.5; draw(); }
    function draw() {
      var P = PRE[st], f = F(P.e), a = P.a, h = +rh.value, fa = f(a), m0 = compile(dOf(P.e))(a);
      if (Math.abs(h) < 0.005) h = 0;
      $(w, "hv").textContent = numTxt(h);
      var rows = "";
      [1, 0.1, 0.01, 0.001, -0.001, -0.01, -0.1].forEach(function (k) { if (a + k <= 0 && P.e.indexOf("sqrt") >= 0) return; rows += "<tr><td>" + tex(numTex(k)) + "</td><td>" + tex(numTex(+((f(a + k) - fa) / k).toFixed(6))) + "</td></tr>"; });
      tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("h") + "</th><th>" + tex("\\dfrac{f(" + numTex(a) + "+h)-f(" + numTex(a) + ")}{h}") + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
      var curves = [{ f: f }, { f: lineF(m0, a, fa), col: "var(--accent-2)" }], pts = [{ x: a, y: fa }], H = "<p>" + tex("f(x)=" + T(P.e)) + "</p>";
      if (h !== 0) {
        var ms = (f(a + h) - fa) / h;
        curves.push({ f: lineF(ms, a, fa), col: "var(--r3)" }); pts.push({ x: a + h, y: f(a + h), col: "var(--r3)" });
        H += "<p>" + u("slope") + ": " + tex("\\dfrac{f(" + numTex(a) + "+h)-f(" + numTex(a) + ")}{h}=" + numTex(+ms.toFixed(5))) + "</p>";
      }
      H += "<p><strong>" + tex("f'(" + numTex(a) + ")=\\lim_{h\\to0}\\dfrac{f(" + numTex(a) + "+h)-f(" + numTex(a) + ")}{h}=" + nt(m0)) + "</strong></p>";
      H += "<p>" + u("tline") + ": " + tex(lineTex(m0, a, fa)) + "</p>";
      info.innerHTML = H;
      plot(svg, { v: P.v, curves: curves, pts: pts, guides: [{ x: a }] });
    }
    onLang(setup);
  }

  /* ---------- widget: derivada per definició (quocient incremental) ---------- */
  function wQuot() {
    var w = document.getElementById("w-quot"); if (!w) return;
    var PRE = [["x^3-2x", "1"], ["1/x^2", "1"], ["sqrt(2x+1)", "4"], ["sin(x)", "0"], ["abs(x-1)", "1"]];
    var fi = $(w, "f"), ai = $(w, "a"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pQuot", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; draw(); });
    [fi, ai].forEach(function (i) { i.addEventListener("input", draw); });
    function draw() {
      var f, a = parseFr(ai.value);
      try { f = fnOf(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
      if (!a) { ai.classList.add("bad"); info.textContent = u("aBad"); return; } ai.classList.remove("bad"); a = a.val();
      var fa = f(a), q = function (x) { return (f(x) - fa) / (x - a); }, rows = "";
      for (var k = 1; k <= 6; k++) { var h = Math.pow(10, -k); rows += "<tr><td>" + tex(numTex(h)) + "</td><td>" + tex(numTex(+q(a - h).toPrecision(7))) + "</td><td>" + tex(numTex(+q(a + h).toPrecision(7))) + "</td></tr>"; }
      tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("h") + "</th><th>" + tex("\\dfrac{f(a-h)-f(a)}{-h}") + "</th><th>" + tex("\\dfrac{f(a+h)-f(a)}{h}") + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
      var L = limSide(q, a, -1), R = limSide(q, a, 1), at = numTex(a);
      var H = "<p>" + tex("f(x)=" + T(fi.value) + ",\\quad a=" + at) + "</p><p>" + u("est") + ": " + tex("\\lim_{h\\to0^-}=" + limTex(L) + ",\\quad\\lim_{h\\to0^+}=" + limTex(R)) + "</p>";
      H += "<p><strong>" + (sameLim(L, R) && L.k === "num" ? tex("f'(" + at + ")=" + limTex(L)) : u("noLim")) + "</strong></p>";
      try { var dd = dOf(fi.value), v = compile(dd)(a); H += '<p style="color:var(--muted)">' + u("exact") + ": " + tex("f'(x)=" + texD(dd) + "\\ \\Rightarrow\\ f'(" + at + ")=" + (isFinite(v) ? nt(v) : "\\nexists")) + "</p>"; } catch (e) {}
      info.innerHTML = H;
    }
    onLang(draw);
  }

  /* ---------- widget: propietats (suma, producte, quocient) ---------- */
  function wRules() {
    var w = document.getElementById("w-rules"); if (!w) return;
    var PRE = [["x^2", "x^3", "1"], ["x", "e^x", "0"], ["x^2+1", "x-1", "2"], ["ln(x)", "x^2", "1"]];
    var iu = $(w, "u"), iv = $(w, "v"), ix = $(w, "x0"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pRules", function (i) { iu.value = PRE[i][0]; iv.value = PRE[i][1]; ix.value = PRE[i][2]; draw(); });
    [iu, iv, ix].forEach(function (i) { i.addEventListener("input", draw); });
    function draw() {
      var U, V, x0 = parseFr(ix.value);
      try { U = strip0(parse(iu.value)); iu.classList.remove("bad"); } catch (e) { iu.classList.add("bad"); info.textContent = u("bad"); return; }
      try { V = strip0(parse(iv.value)); iv.classList.remove("bad"); } catch (e) { iv.classList.add("bad"); info.textContent = u("bad"); return; }
      if (!x0) { ix.classList.add("bad"); info.textContent = u("aBad"); return; } ix.classList.remove("bad"); x0 = x0.val();
      var dU, dV; try { dU = D(U); dV = D(V); } catch (e) { info.textContent = u("noDiff"); return; }
      var ev = function (n) { return compile(n)(x0); }, xt = numTex(x0);
      var sumD = simp(B("+", dU, dV)), prD = simp(B("+", B("*", dU, V), B("*", U, dV))), quD = simp(B("/", B("-", B("*", dU, V), B("*", U, dV)), B("^", V, num(2))));
      var rows = [
        ["u'", texD(dU), ev(dU)], ["v'", texD(dV), ev(dV)],
        ["(u+v)'=u'+v'", texD(sumD), ev(sumD)],
        ["(u\\cdot v)'=u'v+uv'", texD(B("+", B("*", dU, V), B("*", U, dV))) + "=" + texD(prD), ev(prD)],
        ["\\left(\\dfrac uv\\right)'=\\dfrac{u'v-uv'}{v^2}", texD(quD), ev(quD)]
      ];
      var h = '<div class="tbl-wrap"><table class="data sm"><thead><tr><th></th><th></th><th>' + tex("x=" + xt) + "</th></tr></thead><tbody>";
      rows.forEach(function (r) { h += "<tr><td>" + tex(r[0]) + "</td><td>" + tex(r[1]) + "</td><td>" + tex(isFinite(r[2]) ? nt(r[2]) : "\\nexists") + "</td></tr>"; });
      h += "</tbody></table></div>";
      var a1 = ev(prD), a2 = ev(dU) * ev(dV);
      h += "<p>" + u("trap") + " " + tex("(u\\cdot v)'(" + xt + ")=" + nt(a1) + (Math.abs(a1 - a2) < 1e-9 ? "=" : "\\neq") + nt(a2) + "=u'(" + xt + ")\\cdot v'(" + xt + ")") + "</p>";
      info.innerHTML = h;
    }
    onLang(draw);
  }

  /* ---------- widget: f i f' ---------- */
  function wFd() {
    var w = document.getElementById("w-fd"); if (!w) return;
    var L = [
      { e: "x^2", v: [-3, 3, -1, 6], r: [-2.5, 2.5] }, { e: "x^3", v: [-2, 2, -5, 5], r: [-1.6, 1.6] }, { e: "sqrt(x)", v: [-0.5, 6, -0.5, 3], r: [0.1, 5.5] },
      { e: "1/x", v: [-4, 4, -4, 4], r: [0.3, 3.5] }, { e: "e^x", v: [-3, 2.5, -0.5, 8], r: [-2.5, 2] }, { e: "2^x", v: [-3, 3, -0.5, 7], r: [-2.5, 2.5] },
      { e: "ln(x)", v: [-0.5, 6, -3, 2.5], r: [0.2, 5.5] }, { e: "sin(x)", v: [-6.5, 6.5, -1.6, 1.6], r: [-6, 6] }, { e: "cos(x)", v: [-6.5, 6.5, -1.6, 1.6], r: [-6, 6] },
      { e: "tan(x)", v: [-1.5, 1.5, -5, 5], r: [-1.2, 1.2] }, { e: "arctan(x)", v: [-5, 5, -2, 2], r: [-4.5, 4.5] }
    ];
    var sel = $(w, "fn"), ra = $(w, "a"), sf = $(w, "pf"), sd = $(w, "pd"), info = w.querySelector(".info");
    L.forEach(function (o, i) { sel.add(new Option("f(x) = " + o.e.replace("sqrt(x)", "√x").replace("^x", "ˣ").replace("x^2", "x²").replace("x^3", "x³"), i)); });
    sel.addEventListener("change", setup); ra.addEventListener("input", draw);
    function setup() { var P = L[+sel.value]; ra.min = P.r[0]; ra.max = P.r[1]; ra.step = 0.01; ra.value = (P.r[0] + P.r[1]) / 2 + (P.r[1] - P.r[0]) / 5; draw(); }
    function draw() {
      var P = L[+sel.value], f = F(P.e), dn = dOf(P.e), df = compile(dn), a = +ra.value, fa = f(a), m = df(a);
      $(w, "av").textContent = numTxt(+a.toFixed(2));
      var yd = autoY([df], P.v[0], P.v[1]);
      if (P.e === "tan(x)") yd = [-0.5, 12];
      info.innerHTML = "<p>" + tex("f(x)=" + T(P.e) + "\\qquad f'(x)=" + texD(dn)) + "</p><p>" + tex("f'(" + numTex(+a.toFixed(2)) + ")=" + numTex(+m.toFixed(4))) + " = " + u("tang") + " (" + u("slope").split(" ")[0] + ")</p>";
      plot(sf, { v: P.v, curves: [{ f: f }, { f: lineF(m, a, fa), col: "var(--accent-2)" }], pts: [{ x: a, y: fa }], guides: [{ x: a }] });
      plot(sd, { v: [P.v[0], P.v[1], yd[0], yd[1]], curves: [{ f: df, col: "var(--accent-2)" }], pts: [{ x: a, y: m, col: "var(--accent-2)" }], guides: [{ x: a, y: m }] });
    }
    onLang(setup);
  }

  /* ---------- widget: regla de la cadena pas a pas ---------- */
  function wChain() {
    var w = document.getElementById("w-chain"); if (!w) return;
    var PRE = ["(x^2+1)^5", "sqrt(3x-1)", "e^(x^2-x)", "ln(cos(x))", "sin(3x)^2", "arctan(sqrt(x))", "e^(sin(x))", "cos(x)^3", "tan(x^2)", "arcsin(2x)"];
    var fi = $(w, "f"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pChain", function (i) { fi.value = PRE[i]; draw(); });
    fi.addEventListener("input", draw);
    function draw() {
      try { parse(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
      try { info.innerHTML = explain(fi.value).html; } catch (e) { info.textContent = u("noDiff"); }
    }
    onLang(draw);
  }

  /* ---------- widget: zoom i derivades laterals ---------- */
  function wZoom() {
    var w = document.getElementById("w-zoom"); if (!w) return;
    var PRE = [
      { d: { p: ["x^2"] }, a: 1, v: [-1, 3, -1, 5] }, { d: { p: ["abs(x-1)"] }, a: 1, v: [-1, 3, -0.5, 2] }, { d: { p: ["x^(1/3)"] }, a: 0, v: [-2, 2, -1.6, 1.6] },
      { d: { p: ["x^(2/3)"] }, a: 0, v: [-2, 2, -0.6, 2] }, { d: { p: ["x*abs(x)"] }, a: 0, v: [-2, 2, -2, 2] },
      { d: { p: ["2^(x+1)", "x^2-2x"], c: [0], inc: ["R"] }, a: 0, v: [-2, 2.5, -1.5, 3.5] },
      { d: { p: ["x^2-8x+60", "-x^2+32x-140"], c: [10], inc: ["L"] }, a: 10, v: [4, 16, 40, 120] }
    ];
    var st = 0, svg = w.querySelector("svg"), rz = $(w, "z"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pZoom", function (i) { st = i; rz.value = 0; draw(); });
    rz.addEventListener("input", draw);
    function draw() {
      var P = PRE[st], M = pwMake(P.d), f = M.f, a = P.a, fa = f(a), z = Math.pow(10, +rz.value);
      $(w, "zv").textContent = "×" + numTxt(+z.toPrecision(3));
      var L = contSide(M.piece(0), a, -1), R = contSide(M.piece(M.c.length ? 1 : 0), a, 1);
      var dL = sideDer(f, a, -1), dR = sideDer(f, a, 1), k = derClass(L, R, fa, dL, dR);
      var ft = M.n > 1 ? pwTex(P.d) : "f(x)=" + T(P.d.p[0]);
      var h = "<p>" + tex(ft) + "</p>";
      h += "<p>" + tex("\\lim_{x\\to" + numTex(a) + "^-}f(x)=" + limTex(L) + ",\\quad \\lim_{x\\to" + numTex(a) + "^+}f(x)=" + limTex(R) + ",\\quad f(" + numTex(a) + ")=" + nt(fa)) + "</p>";
      if (k !== "ncont") h += "<p>" + tex("f'(" + numTex(a) + "^-)=" + limTex(dL) + ",\\quad f'(" + numTex(a) + "^+)=" + limTex(dR)) + "</p>";
      h += "<p>" + badgeD(k) + (k === "der" ? " " + tex("f'(" + numTex(a) + ")=" + limTex(dL)) : k === "ncont" ? " " + u("fpoint").replace(/\\\(|\\\)/g, "") : "") + "</p>";
      info.innerHTML = h;
      var cx = a, cy = isFinite(fa) ? fa : (P.v[2] + P.v[3]) / 2, hx = (P.v[1] - P.v[0]) / 2 / z, hy = (P.v[3] - P.v[2]) / 2 / z;
      var v = z > 1.01 ? [cx - hx, cx + hx, cy - hy, cy + hy] : P.v, dr = pwDraw(M, v), curves = dr.curves.slice();
      if (k !== "ncont") {
        if (dL.k === "num") curves.push({ f: lineF(dL.v, a, fa), col: "var(--accent-2)", b: a });
        if (dR.k === "num") curves.push({ f: lineF(dR.v, a, fa), col: "var(--r3)", a: a });
      }
      plot(svg, { v: v, curves: curves, pts: dr.pts.concat(isFinite(fa) ? [{ x: a, y: fa }] : []), guides: k === "vt" ? [{ x: a }] : [] });
    }
    onLang(draw);
  }

  /* ---------- estudi de la derivabilitat d'una funció a trossos ---------- */
  function dPieces(def) { return def.p.map(function (e) { try { return compile(dOf(e)); } catch (x) { return null; } }); }
  function studyD(def, env) {
    var P = pwMake(def, env), DP = dPieces(def), out = [];
    P.c.forEach(function (c, k) {
      var inside = (c > P.dom[0] || (c === P.dom[0] && P.din[0])) && (c < P.dom[1] || (c === P.dom[1] && P.din[1]));
      if (!inside) return;
      var L = contSide(P.piece(k), c, -1), R = contSide(P.piece(k + 1), c, 1), fa = P.f(c), cl = classify(L, R, fa), dL = { k: "none" }, dR = { k: "none" };
      if (cl === "ok") {
        dL = DP[k] ? contSide(function (x) { return DP[k](x, env); }, c, -1) : sideDer(P.f, c, -1);
        dR = DP[k + 1] ? contSide(function (x) { return DP[k + 1](x, env); }, c, 1) : sideDer(P.f, c, 1);
      }
      out.push({ x: c, L: L, R: R, fa: fa, cl: cl, dL: dL, dR: dR, k: derClass(L, R, fa, dL, dR) });
    });
    return { P: P, cuts: out };
  }
  function dpwTex(def) {
    var c = def.c || [], dom = def.dom || [-Infinity, Infinity];
    var rows = def.p.map(function (e, i) {
      var lo = i === 0 ? dom[0] : c[i - 1], hi = i === c.length ? dom[1] : c[i], dt;
      try { dt = texD(dOf(e)); } catch (x) { dt = "?"; }
      return dt + "&\\text{" + u("pc") + " }" + condTex(lo, false, hi, false);
    });
    return "f'(x)=\\begin{cases}" + rows.join("\\\\[3pt]") + "\\end{cases}";
  }
  function tangentBits(S, view) {
    // segments de la mateixa llargària en pantalla, siga quin siga el pendent
    var curves = [], len = (view[1] - view[0]) * 0.12, r = (view[1] - view[0]) / (view[3] - view[2]) * 0.7;
    function dx(m) { return len / Math.sqrt(1 + m * m * r * r); }
    S.cuts.forEach(function (q) {
      if (q.cl !== "ok") return;
      if (q.dL.k === "num") curves.push({ f: lineF(q.dL.v, q.x, q.fa), col: "var(--accent-2)", a: q.x - dx(q.dL.v), b: q.x });
      if (q.dR.k === "num") curves.push({ f: lineF(q.dR.v, q.x, q.fa), col: "var(--r3)", a: q.x, b: q.x + dx(q.dR.v) });
    });
    return curves;
  }
  var PWD = {
    res: { d: { p: ["x+1", "x^2-1"], c: [2], inc: ["R"] }, v: [-1, 4, -1, 12] },
    abs: { d: { p: ["x^2-4x", "-x^2+4x", "x^2-4x"], c: [0, 4], inc: ["R", "L"] }, v: [-1.5, 5.5, -1.5, 6] },
    mad22: { d: { p: ["x", "x*ln(x)"], c: [0], inc: ["L"] }, v: [-1.5, 2.5, -1.5, 2.5] },
    trig: { d: { p: ["sin(x)", "x^2+x"], c: [0], inc: ["R"] }, v: [-3.5, 1.5, -1.5, 3.5] },
    ast25: { d: { p: ["x/2", "3-(x-5)^2"], c: [4], inc: ["R"], dom: [0, Infinity] }, v: [-0.5, 8, -2, 4] },
    nav24: { d: { p: ["-x^2-4x", "4-x", "x^2-6x+8"], c: [-1, 1], inc: ["R", "R"] }, v: [-5, 6, -3, 9] }
  };
  function wPwd() {
    var w = document.getElementById("w-pwd"); if (!w) return;
    var KEYS = ["res", "abs", "mad22", "trig", "ast25", "nav24"];
    var box = $(w, "pcs"), svg = w.querySelector("svg"), info = w.querySelector(".info"), def = null, cur = null, view = null, rows = [];
    presetBtns($(w, "presets"), KEYS.length, "pPwd", function (i) { cur = null; load(PWD[KEYS[i]].d, PWD[KEYS[i]].v); });
    function inp(v, cls) { var i = document.createElement("input"); i.type = "text"; i.className = "tin " + cls; i.value = v; i.autocomplete = "off"; i.spellcheck = false; i.addEventListener("input", read); return i; }
    function sel(v) { var s = document.createElement("select"); s.add(new Option("<", "R")); s.add(new Option("≤", "L")); s.value = v; s.addEventListener("change", read); return s; }
    function load(d, v) {
      def = { p: d.p.slice(), c: (d.c || []).slice(), dom: (d.dom || [-Infinity, Infinity]).slice(), din: (d.din || [true, true]).slice() };
      def.inc = (d.inc || def.c.map(function () { return "R"; })).slice();
      view = v; box.innerHTML = ""; rows = [];
      def.p.forEach(function (e, i) {
        var r = document.createElement("div"); r.className = "pc";
        var dot = document.createElement("span"); dot.className = "dot"; dot.style.background = COLS[0];
        var ie = inp(e, "w"); r.appendChild(dot); r.appendChild(ie);
        var o = { e: ie };
        if (i < def.c.length) { r.appendChild(document.createTextNode(u("pc") + " x ")); o.s = sel(def.inc[i]); o.c = inp(numTxt(def.c[i]), "s"); r.appendChild(o.s); r.appendChild(o.c); }
        else r.appendChild(document.createTextNode(u("rest")));
        box.appendChild(r); rows.push(o);
      });
      read();
    }
    function read() {
      var bad = false;
      var d = { p: [], c: [], inc: [], dom: def.dom, din: def.din };
      rows.forEach(function (o) {
        try { parse(o.e.value); o.e.classList.remove("bad"); } catch (e) { o.e.classList.add("bad"); bad = true; }
        d.p.push(o.e.value);
        if (o.c) { var v = parseFr(o.c.value); o.c.classList.toggle("bad", !v); if (!v) bad = true; d.c.push(v ? v.val() : 0); d.inc.push(o.s.value); }
      });
      for (var k = 1; k < d.c.length; k++) if (!(d.c[k] > d.c[k - 1])) bad = true;
      if (bad) { info.textContent = u("bad"); return; }
      cur = d; draw(d);
    }
    function draw(d) {
      var S = studyD(d), dec = /\d\.\d/.test(d.p.join(" ")), h = "<p>" + tex(pwTex(d)) + "</p><p>" + u("pieceDer") + "</p><p>" + tex(dpwTex(d)) + "</p>";
      h += '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("a") + "</th><th>" + tex("f(a)") + "</th><th>" + tex("\\lim\\limits_{x\\to a^-}") + "</th><th>" + tex("\\lim\\limits_{x\\to a^+}") + "</th><th>" + tex("f'(a^-)") + "</th><th>" + tex("f'(a^+)") + "</th><th></th></tr></thead><tbody>";
      S.cuts.forEach(function (q) {
        var cont = q.cl === "ok";
        h += "<tr><td>" + tex(numTex(q.x)) + "</td><td>" + tex(limFmt({ k: isFinite(q.fa) ? "num" : "none", v: q.fa }, dec)) + "</td><td>" + tex(limFmt(q.L, dec)) + "</td><td>" + tex(limFmt(q.R, dec)) + "</td><td>" + (cont ? tex(limFmt(q.dL, dec)) : "—") + "</td><td>" + (cont ? tex(limFmt(q.dR, dec)) : "—") + "</td><td>" + badgeD(q.k) + "</td></tr>";
      });
      h += "</tbody></table></div>";
      var bad = S.cuts.filter(function (q) { return q.k !== "der"; }).map(function (q) { return numTex(q.x); });
      h += "<p><strong>" + (bad.length ? u("derExc") + " " + tex("x=" + bad.join(",\\ x=")) + "." : u("derAll")) + "</strong> <span style=\"color:var(--muted)\">" + u("chkPieces") + "</span></p>";
      info.innerHTML = h;
      var dr = pwDraw(S.P, view);
      plot(svg, { v: view, curves: dr.curves.concat(tangentBits(S, view)), pts: dr.pts });
    }
    onLang(function () { load(cur || PWD.res.d, view || PWD.res.v); });
  }

  /* ---------- widget: paràmetres (contínua i derivable) ---------- */
  function wPard() {
    var w = document.getElementById("w-pard"); if (!w) return;
    var PRE = [
      { d: { p: ["6x-3", "a x^2+b x+2"], c: [1], inc: ["L"] }, tex: "f(x)=\\begin{cases}6x-3&\\SI x\\leq1\\\\ax^2+bx+2&\\SI x\\gt1\\end{cases}", a: [0, 8, 0.1, 2], b: [-8, 4, 0.1, 0], sol: "a=5,\\ b=-4", v: [-1, 3, -6, 14] },
      { d: { p: ["a x^2+b x", "ln(x)"], c: [1], inc: ["L"] }, tex: "f(x)=\\begin{cases}ax^2+bx&\\SI x\\leq1\\\\\\ln x&\\SI x\\gt1\\end{cases}", a: [-2, 3, 0.05, 0.5], b: [-3, 2, 0.05, 0], sol: "a=1,\\ b=-1", v: [-1, 4, -1.5, 2.5] },
      { d: { p: ["2+a/(x-1)", "a+b e^x"], c: [0], inc: ["R"] }, tex: "f(x)=\\begin{cases}2+\\dfrac{a}{x-1}&\\SI x\\lt0\\\\a+b\\,e^x&\\SI x\\geq0\\end{cases}", a: [-1, 4, 0.05, 1], b: [-4, 2, 0.05, 0], sol: "a=2,\\ b=-2", v: [-4, 2.5, -4, 5] },
      { d: { p: ["x^2+a x+b", "sin(2x)"], c: [0], inc: ["L"] }, tex: "f(x)=\\begin{cases}x^2+ax+b&\\SI x\\leq0\\\\\\sin 2x&\\SI x\\gt0\\end{cases}", a: [-3, 5, 0.05, 0], b: [-2, 2, 0.05, 1], sol: "a=2,\\ b=0", v: [-3, 2.5, -2, 3] },
      { d: { p: ["x^2+2sqrt(3)", "sqrt(a x+b)", "7/2-x/6"], c: [0, 3], inc: ["L", "L"] }, tex: "f(x)=\\begin{cases}x^2+2\\sqrt3&\\SI x\\leq0\\\\\\sqrt{ax+b}&\\SI 0\\lt x\\leq3\\\\\\dfrac72-\\dfrac x6&\\SI x\\gt3\\end{cases}", a: [-3, 3, 0.05, 0], b: [0, 20, 0.1, 8], sol: "a=-1,\\ b=12", v: [-3, 7, 0, 7], onlyC: true }
    ];
    var st = 0, svg = w.querySelector("svg"), fn = $(w, "fn"), out = $(w, "out"), ra = $(w, "a"), rb = $(w, "b"), av = $(w, "av"), bv = $(w, "bv");
    presetBtns($(w, "presets"), PRE.length, "pPar", function (i) { st = i; setup(); });
    [ra, rb].forEach(function (r) { r.addEventListener("input", draw); });
    function setup() {
      var P = PRE[st];
      ra.min = P.a[0]; ra.max = P.a[1]; ra.step = P.a[2]; ra.value = P.a[3];
      $(w, "sb").style.display = P.b ? "" : "none";
      if (P.b) { rb.min = P.b[0]; rb.max = P.b[1]; rb.step = P.b[2]; rb.value = P.b[3]; }
      draw();
    }
    function draw() {
      var P = PRE[st], env = { a: +ra.value, b: P.b ? +rb.value : 0 };
      av.textContent = numTxt(env.a); bv.textContent = numTxt(env.b);
      fn.innerHTML = tex(P.tex.replace(/\\SI /g, "\\text{" + u("pc") + " }"));
      var S = studyD(P.d, env), cont = S.cuts.every(function (q) { return q.cl === "ok"; }), der = S.cuts.every(function (q) { return q.k === "der"; });
      var near = S.cuts.every(function (q) {
        return q.L.k === "num" && q.R.k === "num" && Math.abs(q.L.v - q.R.v) < 0.01 && (P.onlyC || (q.dL.k === "num" && q.dR.k === "num" && Math.abs(q.dL.v - q.dR.v) < 0.01));
      });
      if (!S.cuts.every(function (q) { return q.cl === "ok"; })) near = near && S.cuts.every(function (q) { return q.L.k === "num" && q.R.k === "num" && Math.abs(q.L.v - q.R.v) < 0.01; });
      var h = S.cuts.map(function (q) {
        var xs = numTex(q.x), s = tex("x=" + xs + ":\\ \\lim_{x\\to" + xs + "^-}f=" + limTex(q.L) + ",\\ \\lim_{x\\to" + xs + "^+}f=" + limTex(q.R));
        if (q.cl === "ok") s += "<br>" + tex("\\phantom{x=" + xs + ":}\\ f'(" + xs + "^-)=" + limTex(q.dL) + ",\\ f'(" + xs + "^+)=" + limTex(q.dR));
        return "<div>" + s + " " + badgeD(q.k) + "</div>";
      }).join("");
      var ok = P.onlyC ? cont : cont && der, msg;
      if (ok) msg = "✓ " + (P.onlyC ? u("wantC") : u("isCD")) + " " + tex(P.sol);
      else if (near) msg = "≈ " + u("almost") + " " + tex(P.sol);
      else if (cont && !P.onlyC) msg = u("isC") + " " + tex("x=" + S.cuts.filter(function (q) { return q.k !== "der"; }).map(function (q) { return numTex(q.x); }).join(",\\ "));
      else msg = u("notC");
      h += '<p class="' + (ok || near ? "msg-ok" : "msg-bad") + '">' + msg + "</p>";
      out.innerHTML = h;
      var dr = pwDraw(S.P, P.v);
      plot(svg, { v: P.v, curves: dr.curves.concat(tangentBits(S, P.v)), pts: dr.pts });
    }
    onLang(setup);
  }

  /* ---------- widget: derivació logarítmica (y = u^v) ---------- */
  function wLogd() {
    var w = document.getElementById("w-logd"); if (!w) return;
    var PRE = [["x", "x", "1"], ["x", "sin(x)", "1"], ["sin(x)", "x", "1"], ["x^2+1", "x", "1"], ["x", "1/x", "2"], ["ln(x)", "x", "3"]];
    var iu = $(w, "u"), iv = $(w, "v"), ia = $(w, "a"), svg = w.querySelector("svg"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pLogd", function (i) { iu.value = PRE[i][0]; iv.value = PRE[i][1]; ia.value = PRE[i][2]; draw(); });
    [iu, iv, ia].forEach(function (i) { i.addEventListener("input", draw); });
    function wrap(n) { n = strip0(n); var s = texD(n); return n.t === "v" || n.t === "n" || n.t === "c" || n.t === "f" ? s : "\\left(" + s + "\\right)"; }
    function draw() {
      var U, V, a = parseFr(ia.value);
      try { U = strip0(parse(iu.value)); iu.classList.remove("bad"); } catch (e) { iu.classList.add("bad"); info.textContent = u("bad"); return; }
      try { V = strip0(parse(iv.value)); iv.classList.remove("bad"); } catch (e) { iv.classList.add("bad"); info.textContent = u("bad"); return; }
      var dU, dV; try { dU = D(U); dV = D(V); } catch (e) { info.textContent = u("noDiff"); return; }
      var ut = wrap(U), vt = texD(V), h = "";
      h += "<p>" + tex("y=" + ut + "^{" + vt + "}") + "</p>";
      h += "<p>1. " + u("takeLn") + " " + tex("\\ln y=" + (strip0(V).t === "+" || strip0(V).t === "-" ? "\\left(" + vt + "\\right)" : vt) + "\\cdot\\ln " + ut) + "</p>";
      var rhs = simp(B("+", B("*", dV, Fn("ln", U)), B("/", B("*", V, dU), U)));
      h += "<p>2. " + u("derBoth") + " " + tex("\\dfrac{y'}{y}=v'\\ln u+v\\,\\dfrac{u'}{u}=" + texD(rhs)) + "</p>";
      h += "<p>3. " + u("isolate") + " " + tex("y'=" + ut + "^{" + vt + "}\\left(" + texD(rhs) + "\\right)") + "</p>";
      var f = compile(B("^", U, V)), df = compile(B("*", B("^", U, V), rhs)), x0 = 0.05, x1 = 4;
      var hasA = !!a;
      if (hasA) {
        a = a.val(); var ua = compile(U)(a), fa = f(a), m = df(a), at = numTex(a);
        ia.classList.remove("bad");
        if (!(ua > 0)) h += '<p class="msg-bad">' + u("uPos") + "</p>";
        else h += "<p><strong>" + tex("f(" + at + ")=" + nt(fa) + ",\\quad f'(" + at + ")=" + nt(m)) + "</strong></p><p>" + u("tline") + ": " + tex(lineTex(m, a, fa)) + "</p>";
        x0 = Math.min(0.02, a - 1); x1 = Math.max(4, a + 1.5);
      } else ia.classList.add("bad");
      info.innerHTML = h;
      var gs = function (x) { return compile(U)(x) > 0 ? f(x) : NaN; }, curves = [{ f: gs }];
      var yy = autoY([gs], x0, x1, 0.1);
      if (hasA && isFinite(f(a)) && isFinite(df(a)) && compile(U)(a) > 0) curves.push({ f: lineF(df(a), a, f(a)), col: "var(--accent-2)" });
      plot(svg, { v: [x0, x1, yy[0], yy[1]], curves: curves, pts: hasA && isFinite(f(a)) ? [{ x: a, y: f(a) }] : [] });
    }
    onLang(draw);
  }

  /* ---------- widget: derivació implícita ---------- */
  function ren(n, m) {
    if (!n || typeof n !== "object") return n;
    var o = {}; for (var k in n) o[k] = n[k];
    if (n.t === "v" && m[n.n]) o.n = m[n.n];
    if (n.a) o.a = ren(n.a, m); if (n.b) o.b = ren(n.b, m);
    return o;
  }
  function dX(n) { return tidy(simp(d(n))); }                                    // y es tracta com una constant
  function dY(n) { return ren(tidy(simp(d(ren(n, { x: "q", y: "x" })))), { x: "y", q: "x" }); }
  // corba F(x, y) = 0 amb «marching squares»
  function contour(Fn2, v, nx, ny) {
    var segs = [], hx = (v[1] - v[0]) / nx, hy = (v[3] - v[2]) / ny, G = [], i, j;
    for (i = 0; i <= nx; i++) { G.push([]); for (j = 0; j <= ny; j++) G[i].push(Fn2(v[0] + i * hx, v[2] + j * hy)); }
    function ip(x1, y1, f1, x2, y2, f2) { var t = f1 / (f1 - f2); return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)]; }
    for (i = 0; i < nx; i++) for (j = 0; j < ny; j++) {
      var x = v[0] + i * hx, y = v[2] + j * hy, a = G[i][j], b = G[i + 1][j], c = G[i + 1][j + 1], e = G[i][j + 1];
      if (![a, b, c, e].every(isFinite)) continue;
      var P = [];
      if ((a > 0) !== (b > 0)) P.push(ip(x, y, a, x + hx, y, b));
      if ((b > 0) !== (c > 0)) P.push(ip(x + hx, y, b, x + hx, y + hy, c));
      if ((c > 0) !== (e > 0)) P.push(ip(x + hx, y + hy, c, x, y + hy, e));
      if ((e > 0) !== (a > 0)) P.push(ip(x, y + hy, e, x, y, a));
      var big = Math.max(Math.abs(a), Math.abs(b), Math.abs(c), Math.abs(e));
      if (big > 1e6) continue;
      if (P.length === 2) segs.push([P[0][0], P[0][1], P[1][0], P[1][1]]);
      else if (P.length === 4) { segs.push([P[0][0], P[0][1], P[1][0], P[1][1]]); segs.push([P[2][0], P[2][1], P[3][0], P[3][1]]); }
    }
    return segs;
  }
  function wImpl() {
    var w = document.getElementById("w-impl"); if (!w) return;
    var PRE = [
      ["x^2+y^2=25", "3", "4", [-7, 7, -6, 6]], ["4x^2+9y^2=36", "1.8", "1.6", [-4.5, 4.5, -3.2, 3.2]], ["x^3+y^3=6xy", "3", "3", [-5, 6, -5, 6]],
      ["x^2+xy+y^2=7", "1", "2", [-4.5, 4.5, -4, 4]], ["y^2=x^3-x+1", "1", "1", [-2.5, 3, -4, 4]], ["e^y+xy=e", "0", "1", [-3, 4, -1.5, 3.5]], ["x^2y+y^3=10", "1", "2", [-6, 6, -1, 4]]
    ];
    var ie = $(w, "eq"), ix = $(w, "x0"), iy = $(w, "y0"), svg = w.querySelector("svg"), info = w.querySelector(".info"), view = PRE[0][3];
    presetBtns($(w, "presets"), PRE.length, "pImpl", function (i) { ie.value = PRE[i][0]; ix.value = PRE[i][1]; iy.value = PRE[i][2]; view = PRE[i][3]; draw(); });
    [ie, ix, iy].forEach(function (i) { i.addEventListener("input", draw); });
    function draw() {
      var sides = ie.value.split("="), Fn0;
      if (sides.length !== 2) { ie.classList.add("bad"); info.textContent = u("eqBad"); return; }
      try { var Lh = strip0(parse(sides[0])), Rh = strip0(parse(sides[1])); Fn0 = simp(B("-", Lh, Rh)); ie.classList.remove("bad"); } catch (e) { ie.classList.add("bad"); info.textContent = u("bad"); return; }
      var Fx, Fy; try { Fx = dX(Fn0); Fy = dY(Fn0); } catch (e) { info.textContent = u("noDiff"); return; }
      var F = compile(Fn0), cFx = compile(Fx), cFy = compile(Fy), yp = simp(B("/", { t: "neg", a: Fx }, Fy));
      var h = "<p>" + tex(texD(Lh) + "=" + texD(Rh)) + "</p>";
      h += "<p>" + u("impl") + " " + tex("y'=-\\dfrac{F_x}{F_y}") + " " + tex("\\left(F=" + texD(Fn0) + "\\right)") + ":</p>";
      h += "<p>" + tex("F_x=" + texD(Fx) + ",\\qquad F_y=" + texD(Fy)) + "</p>";
      h += "<p><strong>" + tex("y'=" + texD(yp)) + "</strong></p>";
      var x0 = parseFr(ix.value), y0 = parseFr(iy.value), pts = [], curves = [];
      ix.classList.toggle("bad", !x0); iy.classList.toggle("bad", !y0);
      if (x0 && y0) {
        x0 = x0.val(); y0 = y0.val();
        var env = { y: y0 }, Fv = F(x0, env), gx = cFx(x0, env), gy = cFy(x0, env), P = "(" + numTex(x0) + "," + numTex(y0) + ")";
        if (!(Math.abs(Fv) < 1e-6 * (1 + Math.abs(x0) + Math.abs(y0)))) h += '<p class="msg-bad">' + u("notOn") + " " + tex("F" + P + "=" + nt(Fv)) + "</p>";
        else {
          h += '<p class="msg-ok">' + u("onC") + "</p>";
          if (Math.abs(gy) < 1e-12) { h += "<p>" + u("vtan") + ": " + tex("x=" + numTex(x0)) + "; " + u("normal") + ": " + tex("y=" + numTex(y0)) + "</p>"; curves.push({ f: function () { return y0; }, col: "var(--r3)" }); }
          else {
            var m = -gx / gy;
            h += "<p>" + tex("y'" + P + "=" + nt(m)) + "</p><p>" + u("tline") + ": " + tex(lineTex(m, x0, y0)) + "</p>";
            curves.push({ f: lineF(m, x0, y0), col: "var(--accent-2)" });
            if (Math.abs(m) > 1e-12) { h += "<p>" + u("normal") + ": " + tex(lineTex(-1 / m, x0, y0)) + "</p>"; curves.push({ f: lineF(-1 / m, x0, y0), col: "var(--r3)" }); }
            else h += "<p>" + u("normal") + ": " + tex("x=" + numTex(x0)) + "</p>";
          }
          pts.push({ x: x0, y: y0 });
        }
      }
      info.innerHTML = h;
      var segs = contour(function (x, y) { return F(x, { y: y }); }, view, 150, 110);
      plot(svg, { v: view, segs: [{ l: segs, col: "var(--accent)" }], curves: curves, pts: pts });
    }
    onLang(draw);
  }

  /* ---------- calculadora de derivades ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var PRE = [["x^3-6x^2+9x+1", "1"], ["x^2*e^(-x)", "1"], ["(x^2+1)/(x-2)", "3"], ["x^x", "1"], ["sqrt(1-x^2)", "0.6"], ["ln(sqrt((1+x)/(1-x)))", "0"], ["arctan((1+x)/(1-x))", "0"]];
    var fi = $(w, "f"), ai = $(w, "a"), svg = w.querySelector("svg"), info = w.querySelector(".info"), sb = $(w, "steps");
    presetBtns($(w, "presets"), PRE.length, "pLab", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; draw(); });
    [fi, ai].forEach(function (i) { i.addEventListener("input", draw); });
    function draw() {
      var f, ex, a = parseFr(ai.value);
      try { f = fnOf(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); sb.innerHTML = ""; info.textContent = u("bad"); return; }
      try { ex = explain(fi.value); } catch (e) { sb.innerHTML = ""; info.textContent = u("noDiff"); plot(svg, { v: [-5, 5, -5, 5], curves: [{ f: f }] }); return; }
      sb.innerHTML = ex.html;
      if (!a) { ai.classList.add("bad"); info.textContent = u("aBad"); return; } ai.classList.remove("bad"); a = a.val();
      var df = compile(ex.d), fa = f(a), m = df(a), at = numTex(a), h;
      if (!isFinite(fa)) h = "<p>" + tex("f(" + at + ")\\ \\nexists") + "</p>";
      else if (!isFinite(m)) h = "<p>" + tex("f(" + at + ")=" + nt(fa) + ",\\quad f'(" + at + ")\\ \\nexists") + "</p>";
      else h = "<p>" + tex("f(" + at + ")=" + nt(fa) + ",\\quad f'(" + at + ")=" + nt(m)) + "</p><p>" + u("tline") + ": " + tex("y-f(a)=f'(a)(x-a)\\ \\Rightarrow\\ " + lineTex(m, a, fa)) + "</p>";
      info.innerHTML = h;
      var x0 = a - 4, x1 = a + 4, yy = autoY([f], x0, x1), curves = [{ f: f }, { f: df, col: "var(--r3)" }];
      if (isFinite(fa) && yy[1] - yy[0] > 40) yy = [Math.max(yy[0], fa - 20), Math.min(yy[1], fa + 20)];
      if (isFinite(m) && isFinite(fa)) curves.push({ f: lineF(m, a, fa), col: "var(--accent-2)" });
      plot(svg, { v: [x0, x1, yy[0], yy[1]], curves: curves, pts: isFinite(fa) ? [{ x: a, y: fa }] : [], guides: [{ x: a }] });
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("La recta normal a $y=x^2$ en el punt $(1,1)$ és…", "La recta normal a $y=x^2$ en el punto $(1,1)$ es…", "The normal line to $y=x^2$ at the point $(1,1)$ is…"),
      o: [q3("$y=2x-1$"), q3("$y=-\\frac12x+\\frac32$"), q3("$y=-2x+3$")], a: 1, e: q3("$f'(1)=2$: la normal té pendent $-\\frac{1}{2}$: $y-1=-\\frac12(x-1)$.", "$f'(1)=2$: la normal tiene pendiente $-\\frac{1}{2}$: $y-1=-\\frac12(x-1)$.", "$f'(1)=2$: the normal has slope $-\\frac{1}{2}$: $y-1=-\\frac12(x-1)$.") },
    { q: q3("Per definició, $\\displaystyle\\lim_{h\\to0}\\frac{\\sin h}{h}$ val $1$. Això prova que…", "Por definición, $\\displaystyle\\lim_{h\\to0}\\frac{\\sin h}{h}$ vale $1$. Esto prueba que…", "By definition, $\\displaystyle\\lim_{h\\to0}\\frac{\\sin h}{h}=1$. This proves that…"),
      o: [q3("$(\\sin x)'(0)=1$"), q3("$(\\cos x)'(0)=1$"), q3("$(\\sin x)'(0)=0$")], a: 0, e: q3("És el quocient incremental de $\\sin x$ en $0$: $\\frac{\\sin(0+h)-\\sin0}{h}$.", "Es el cociente incremental de $\\sin x$ en $0$: $\\frac{\\sin(0+h)-\\sin0}{h}$.", "It is the difference quotient of $\\sin x$ at $0$: $\\frac{\\sin(0+h)-\\sin0}{h}$.") },
    { q: q3("La derivada $n$-èsima de $f(x)=e^{2x}$ és…", "La derivada $n$-ésima de $f(x)=e^{2x}$ es…", "The $n$-th derivative of $f(x)=e^{2x}$ is…"),
      o: [q3("$2n\\,e^{2x}$"), q3("$2^n e^{2x}$"), q3("$e^{2x}$")], a: 1, e: q3("Cada derivació multiplica per 2: $f'=2e^{2x}$, $f''=4e^{2x}$, …", "Cada derivación multiplica por 2: $f'=2e^{2x}$, $f''=4e^{2x}$, …", "Each differentiation multiplies by 2: $f'=2e^{2x}$, $f''=4e^{2x}$, …") },
    { q: q3("La derivada de $f(x)=\\ln\\sqrt{\\dfrac{1+x}{1-x}}$ és…", "La derivada de $f(x)=\\ln\\sqrt{\\dfrac{1+x}{1-x}}$ es…", "The derivative of $f(x)=\\ln\\sqrt{\\dfrac{1+x}{1-x}}$ is…"),
      o: [q3("$\\dfrac{1}{1-x^2}$"), q3("$\\dfrac{2}{1-x^2}$"), q3("$\\dfrac{x}{1-x^2}$")], a: 0, e: q3("$f=\\frac12\\ln(1+x)-\\frac12\\ln(1-x)\\Rightarrow f'=\\frac{1}{2(1+x)}+\\frac{1}{2(1-x)}=\\frac{1}{1-x^2}$.") },
    { q: q3("La derivada de $f(x)=\\sin^2(3x)$ és…", "La derivada de $f(x)=\\sin^2(3x)$ es…", "The derivative of $f(x)=\\sin^2(3x)$ is…"),
      o: [q3("$2\\sin3x\\cos3x$"), q3("$6\\sin3x\\cos3x$"), q3("$6\\cos^2 3x$")], a: 1, e: q3("Tres funcions encadenades: $2\\sin3x\\cdot\\cos3x\\cdot3$ ($=3\\sin6x$).", "Tres funciones encadenadas: $2\\sin3x\\cdot\\cos3x\\cdot3$ ($=3\\sin6x$).", "Three nested functions: $2\\sin3x\\cdot\\cos3x\\cdot3$ ($=3\\sin6x$).") },
    { q: q3("La derivada de $f(x)=\\arctan(\\sqrt x)$ és…", "La derivada de $f(x)=\\arctan(\\sqrt x)$ es…", "The derivative of $f(x)=\\arctan(\\sqrt x)$ is…"),
      o: [q3("$\\dfrac{1}{1+x}$"), q3("$\\dfrac{1}{2\\sqrt x\\,(1+x)}$"), q3("$\\dfrac{1}{2\\sqrt x\\,(1+x^2)}$")], a: 1, e: q3("$\\frac{g'}{1+g^2}$ amb $g=\\sqrt x$: $\\frac{1/(2\\sqrt x)}{1+x}$.", "$\\frac{g'}{1+g^2}$ con $g=\\sqrt x$: $\\frac{1/(2\\sqrt x)}{1+x}$.", "$\\frac{g'}{1+g^2}$ with $g=\\sqrt x$: $\\frac{1/(2\\sqrt x)}{1+x}$.") },
    { q: q3("La derivada de $f(x)=x^x$ ($x\\gt0$) és…", "La derivada de $f(x)=x^x$ ($x\\gt0$) es…", "The derivative of $f(x)=x^x$ ($x\\gt0$) is…"),
      o: [q3("$x\\cdot x^{x-1}=x^x$"), q3("$x^x\\ln x$"), q3("$x^x(\\ln x+1)$")], a: 2, e: q3("Derivació logarítmica: $\\ln y=x\\ln x\\Rightarrow\\frac{y'}{y}=\\ln x+1$. Ni la regla de la potència ni la de l'exponencial serveixen soles.", "Derivación logarítmica: $\\ln y=x\\ln x\\Rightarrow\\frac{y'}{y}=\\ln x+1$. Ni la regla de la potencia ni la de la exponencial sirven solas.", "Logarithmic differentiation: $\\ln y=x\\ln x\\Rightarrow\\frac{y'}{y}=\\ln x+1$. Neither the power rule nor the exponential rule works on its own.") },
    { q: q3("Si $x^2+y^2=25$, en el punt $(3,4)$ el pendent de la tangent és…", "Si $x^2+y^2=25$, en el punto $(3,4)$ la pendiente de la tangente es…", "If $x^2+y^2=25$, the slope of the tangent at $(3,4)$ is…"),
      o: [q3("$-\\frac34$"), q3("$\\frac43$"), q3("$-\\frac43$")], a: 0, e: q3("$2x+2yy'=0\\Rightarrow y'=-\\frac xy=-\\frac34$.") },
    { q: q3("Derivant implícitament $xy+y^3=2$, la derivada de $xy$ és…", "Derivando implícitamente $xy+y^3=2$, la derivada de $xy$ es…", "Differentiating $xy+y^3=2$ implicitly, the derivative of $xy$ is…"),
      o: [q3("$y'$"), q3("$y+xy'$"), q3("$1\\cdot y'$")], a: 1, e: q3("És un producte: $(x)'\\,y+x\\,(y)'=y+xy'$.", "Es un producto: $(x)'\\,y+x\\,(y)'=y+xy'$.", "It is a product: $(x)'\\,y+x\\,(y)'=y+xy'$.") },
    { q: q3("$f(x)=\\sqrt[3]{x^2}$ en $x=0$ és…", "$f(x)=\\sqrt[3]{x^2}$ en $x=0$ es…", "$f(x)=\\sqrt[3]{x^2}$ at $x=0$ is…"),
      o: [q3("derivable, amb $f'(0)=0$", "derivable, con $f'(0)=0$", "differentiable, with $f'(0)=0$"), q3("contínua però no derivable (punt de retrocés)", "continua pero no derivable (punto de retroceso)", "continuous but not differentiable (cusp)"), q3("no contínua", "no continua", "not continuous")], a: 1,
      e: q3("$\\frac{h^{2/3}}{h}=h^{-1/3}\\to\\mp\\infty$ per cada costat: tangent vertical amb punxa.", "$\\frac{h^{2/3}}{h}=h^{-1/3}\\to\\mp\\infty$ por cada lado: tangente vertical con pico.", "$\\frac{h^{2/3}}{h}=h^{-1/3}\\to\\mp\\infty$ on each side: vertical tangent with a cusp.") },
    { q: q3("$f(x)=x\\,|x|$ en $x=0$ és…", "$f(x)=x\\,|x|$ en $x=0$ es…", "$f(x)=x\\,|x|$ at $x=0$ is…"),
      o: [q3("derivable, amb $f'(0)=0$", "derivable, con $f'(0)=0$", "differentiable, with $f'(0)=0$"), q3("contínua però no derivable", "continua pero no derivable", "continuous but not differentiable"), q3("no contínua", "no continua", "not continuous")], a: 0,
      e: q3("$\\frac{h|h|}{h}=|h|\\to0$ pels dos costats.", "$\\frac{h|h|}{h}=|h|\\to0$ por los dos lados.", "$\\frac{h|h|}{h}=|h|\\to0$ from both sides.") },
    { q: q3("Perquè $f(x)=\\begin{cases}ax^2+bx&x\\leq1\\\\\\ln x&x\\gt1\\end{cases}$ siga derivable en $\\mathbb R$ cal que…", "Para que $f(x)=\\begin{cases}ax^2+bx&x\\leq1\\\\\\ln x&x\\gt1\\end{cases}$ sea derivable en $\\mathbb R$ hace falta que…", "For $f(x)=\\begin{cases}ax^2+bx&x\\leq1\\\\\\ln x&x\\gt1\\end{cases}$ to be differentiable on $\\mathbb R$ we need…"),
      o: [q3("$a=1,\\ b=-1$"), q3("$a=0,\\ b=1$"), q3("$a=-1,\\ b=1$")], a: 0, e: q3("Continuïtat: $a+b=0$. Derivabilitat: $2a+b=1$.", "Continuidad: $a+b=0$. Derivabilidad: $2a+b=1$.", "Continuity: $a+b=0$. Differentiability: $2a+b=1$.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Càlcul de derivades · FentMates", es: "Cálculo de derivadas · FentMates", en: "Computing derivatives · FentMates" };
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
    var all = [wChrome, wSteps, wNav, wFigs, wTvm, wSec, wQuot, wRules, wFd, wChain, wLogd, wImpl, wZoom, wPwd, wPard, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM6 = { parse: parse, D: D, texD: texD, compile: compile, explain: explain, dX: dX, dY: dY };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
