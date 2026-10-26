(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2batx-u4-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt",
      bad: "No entenc l'expressió: revisa-la.", badPoly: "Escriu polinomis (per exemple 3x^2-5x+1).", left: "Per l'esquerra", right2: "Per la dreta", limit: "Límit",
      noLim: "no existeix", undef: "la funció no està definida en aquest costat", osc: "no s'estabilitza", est: "Estimació numèrica",
      cont: "contínua", ev: "evitable", sf: "salt finit", si: "salt infinit", as: "asimptòtica", disc: "discontinuïtat",
      lead: "Ens quedem amb els termes de major grau", same: "Mateix grau: quocient dels coeficients principals.", topBig: "El grau de dalt és més gran: el límit és infinit.", botBig: "El grau de baix és més gran: el límit és 0.",
      zeroQ: "Q(x) no pot ser el polinomi zero.", subst: "Substituïm", direct: "No hi ha indeterminació: el límit és el valor de la fracció.", kz: "Ix k/0: el límit és infinit. Estudiem el signe a cada costat.",
      ind: "Indeterminació 0/0: tots dos són divisibles per", ruff: "Ruffini", simpl: "Simplifiquem", now: "Tornem a substituir", aBad: "Escriu un nombre (enter, decimal o fracció) per a a.",
      ofRow: "valor de", towards: "s'acosta a", grows: "creix sense fita", decr: "decreix sense fita", target: "Valor exacte", hl: "Fila marcada: el valor actual de n.",
      fFaster: "f és un infinit d'ordre superior: f/g → +∞", gFaster: "g és un infinit d'ordre superior: f/g → 0", sameOrd: "Mateix ordre: f/g s'acosta a un nombre", ident: "Són la mateixa funció!",
      point: "Punt", piece: "Tros", cut: "Punt de tall", interval: "Interval", junction: "Punts on es trenca", denZero: "El denominador s'anul·la en", outDom: "fora del seu interval",
      contAll: "La funció és contínua en tot l'interval.", contExc: "La funció és contínua en l'interval excepte en", andW: "i", rest: "en la resta", fa: "f(a)",
      pzero: "Punts on s'anul·la un denominador", noDen: "Cap denominador s'anul·la dins del seu tros.", isCont: "Contínua!", notYet: "Encara hi ha salt", almost: "Pràcticament contínua (salt < 0,01): l'exacte és",
      clsTitle: "Classificació", why: ["Els dos laterals coincideixen amb f(a).", "El límit existeix, però f(a) no existeix o és diferent.", "Els laterals són nombres diferents.", "Un lateral és infinit i l'altre és un nombre.", "Els dos laterals són infinits."],
      sideL: "esquerra", sideR: "dreta", at: "en", nanIn: "Hi ha algun valor que no és un nombre.", h: "h", infPts: "(punt d'acumulació)",
      pInf: ["Asímptota y = 2", "Exponencial", "Polinomi", "Oscil·la"], pDeg: ["Grau menor", "Mateix grau", "Grau major", "Senar a −∞"],
      pOne: ["Exemple 1", "Exemple 2", "(1 + 3/x)^x", "Base → 1 ràpid", "Exponent x²"], pSide: ["A trossos", "4x²/(x²−1)", "0/0", "3/(x−2)²"],
      pFact: ["Exemple 1", "Exemple 2", "Exemple 3", "Directe"], pPw: ["PAU 2006", "PAU 2007", "PAU 2009", "PAU 2014", "PAU 2006 (a=0)", "PAU 2015", "PAU 2010"],
      pPar: ["Exemple resum", "PAU 2007", "PAU 2017", "PAU 2006", "Dos paràmetres", "PAU 2026"], pLab: ["0/0", "∞−∞", "1^∞", "Infinits", "Salt", "Asímptota"],
      pc: "si", lt: "<", le: "≤", lo: "des de", hi: "fins a", addPc: "＋ Tros", rmPc: "Lleva" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba",
      bad: "No entiendo la expresión: revísala.", badPoly: "Escribe polinomios (por ejemplo 3x^2-5x+1).", left: "Por la izquierda", right2: "Por la derecha", limit: "Límite",
      noLim: "no existe", undef: "la función no está definida en este lado", osc: "no se estabiliza", est: "Estimación numérica",
      cont: "continua", ev: "evitable", sf: "salto finito", si: "salto infinito", as: "asintótica", disc: "discontinuidad",
      lead: "Nos quedamos con los términos de mayor grado", same: "Mismo grado: cociente de los coeficientes principales.", topBig: "El grado de arriba es mayor: el límite es infinito.", botBig: "El grado de abajo es mayor: el límite es 0.",
      zeroQ: "Q(x) no puede ser el polinomio cero.", subst: "Sustituimos", direct: "No hay indeterminación: el límite es el valor de la fracción.", kz: "Sale k/0: el límite es infinito. Estudiamos el signo a cada lado.",
      ind: "Indeterminación 0/0: los dos son divisibles por", ruff: "Ruffini", simpl: "Simplificamos", now: "Volvemos a sustituir", aBad: "Escribe un número (entero, decimal o fracción) para a.",
      ofRow: "valor de", towards: "se acerca a", grows: "crece sin cota", decr: "decrece sin cota", target: "Valor exacto", hl: "Fila marcada: el valor actual de n.",
      fFaster: "f es un infinito de orden superior: f/g → +∞", gFaster: "g es un infinito de orden superior: f/g → 0", sameOrd: "Mismo orden: f/g se acerca a un número", ident: "¡Son la misma función!",
      point: "Punto", piece: "Trozo", cut: "Punto de corte", interval: "Intervalo", junction: "Puntos donde se rompe", denZero: "El denominador se anula en", outDom: "fuera de su intervalo",
      contAll: "La función es continua en todo el intervalo.", contExc: "La función es continua en el intervalo excepto en", andW: "y", rest: "en el resto", fa: "f(a)",
      pzero: "Puntos donde se anula un denominador", noDen: "Ningún denominador se anula dentro de su trozo.", isCont: "¡Continua!", notYet: "Todavía hay salto", almost: "Prácticamente continua (salto < 0,01): el exacto es",
      clsTitle: "Clasificación", why: ["Los dos laterales coinciden con f(a).", "El límite existe, pero f(a) no existe o es distinto.", "Los laterales son números distintos.", "Un lateral es infinito y el otro es un número.", "Los dos laterales son infinitos."],
      sideL: "izquierda", sideR: "derecha", at: "en", nanIn: "Hay algún valor que no es un número.", h: "h", infPts: "",
      pInf: ["Asíntota y = 2", "Exponencial", "Polinomio", "Oscila"], pDeg: ["Grado menor", "Mismo grado", "Grado mayor", "Impar en −∞"],
      pOne: ["Ejemplo 1", "Ejemplo 2", "(1 + 3/x)^x", "Base → 1 rápido", "Exponente x²"], pSide: ["A trozos", "4x²/(x²−1)", "0/0", "3/(x−2)²"],
      pFact: ["Ejemplo 1", "Ejemplo 2", "Ejemplo 3", "Directo"], pPw: ["PAU 2006", "PAU 2007", "PAU 2009", "PAU 2014", "PAU 2006 (a=0)", "PAU 2015", "PAU 2010"],
      pPar: ["Ejemplo resumen", "PAU 2007", "PAU 2017", "PAU 2006", "Dos parámetros", "PAU 2026"], pLab: ["0/0", "∞−∞", "1^∞", "Infinitos", "Salto", "Asíntota"],
      pc: "si", lt: "<", le: "≤", lo: "desde", hi: "hasta", addPc: "＋ Trozo", rmPc: "Quitar" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top",
      bad: "I can't read that expression: check it.", badPoly: "Type polynomials (for example 3x^2-5x+1).", left: "From the left", right2: "From the right", limit: "Limit",
      noLim: "does not exist", undef: "the function is not defined on this side", osc: "does not settle", est: "Numerical estimate",
      cont: "continuous", ev: "removable", sf: "finite jump", si: "infinite jump", as: "asymptotic", disc: "discontinuity",
      lead: "Keep the highest-degree terms", same: "Same degree: ratio of the leading coefficients.", topBig: "The top degree is larger: the limit is infinite.", botBig: "The bottom degree is larger: the limit is 0.",
      zeroQ: "Q(x) cannot be the zero polynomial.", subst: "Substitute", direct: "No indeterminate form: the limit is the value of the fraction.", kz: "We get k/0: the limit is infinite. Study the sign on each side.",
      ind: "0/0 form: both are divisible by", ruff: "Ruffini", simpl: "Cancel", now: "Substitute again", aBad: "Type a number (integer, decimal or fraction) for a.",
      ofRow: "value of", towards: "approaches", grows: "grows without bound", decr: "decreases without bound", target: "Exact value", hl: "Highlighted row: the current value of n.",
      fFaster: "f is an infinity of higher order: f/g → +∞", gFaster: "g is an infinity of higher order: f/g → 0", sameOrd: "Same order: f/g tends to a number", ident: "They are the same function!",
      point: "Point", piece: "Piece", cut: "Break point", interval: "Interval", junction: "Break points", denZero: "The denominator vanishes at", outDom: "outside its interval",
      contAll: "The function is continuous on the whole interval.", contExc: "The function is continuous on the interval except at", andW: "and", rest: "otherwise", fa: "f(a)",
      pzero: "Points where a denominator vanishes", noDen: "No denominator vanishes inside its piece.", isCont: "Continuous!", notYet: "There is still a jump", almost: "Practically continuous (jump < 0.01): the exact value is",
      clsTitle: "Classification", why: ["Both one-sided limits equal f(a).", "The limit exists, but f(a) does not exist or is different.", "The one-sided limits are different numbers.", "One one-sided limit is infinite and the other is a number.", "Both one-sided limits are infinite."],
      sideL: "left", sideR: "right", at: "at", nanIn: "Some value is not a number.", h: "h", infPts: "",
      pInf: ["Asymptote y = 2", "Exponential", "Polynomial", "Oscillates"], pDeg: ["Lower degree", "Same degree", "Higher degree", "Odd at −∞"],
      pOne: ["Example 1", "Example 2", "(1 + 3/x)^x", "Base → 1 fast", "Exponent x²"], pSide: ["Piecewise", "4x²/(x²−1)", "0/0", "3/(x−2)²"],
      pFact: ["Example 1", "Example 2", "Example 3", "Direct"], pPw: ["PAU 2006", "PAU 2007", "PAU 2009", "PAU 2014", "PAU 2006 (a=0)", "PAU 2015", "PAU 2010"],
      pPar: ["Summary example", "PAU 2007", "PAU 2017", "PAU 2006", "Two parameters", "PAU 2026"], pLab: ["0/0", "∞−∞", "1^∞", "Infinities", "Jump", "Asymptote"],
      pc: "if", lt: "<", le: "≤", lo: "from", hi: "to", addPc: "＋ Piece", rmPc: "Remove" }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }

  /* ---------- fraccions exactes ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  function Fr(n, d) { if (d === undefined) d = 1; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d); this.n = n / g; this.d = d / g; }
  Fr.prototype.add = function (o) { return new Fr(this.n * o.d + o.n * this.d, this.d * o.d); };
  Fr.prototype.sub = function (o) { return new Fr(this.n * o.d - o.n * this.d, this.d * o.d); };
  Fr.prototype.mul = function (o) { return new Fr(this.n * o.n, this.d * o.d); };
  Fr.prototype.div = function (o) { return new Fr(this.n * o.d, this.d * o.n); };
  Fr.prototype.zero = function () { return this.n === 0; };
  Fr.prototype.val = function () { return this.n / this.d; };
  Fr.prototype.tex = function () { if (this.d === 1) return String(this.n); return (this.n < 0 ? "-" : "") + "\\frac{" + Math.abs(this.n) + "}{" + this.d + "}"; };
  Fr.prototype.txt = function () { return (this.d === 1 ? String(this.n) : this.n + "/" + this.d).replace(/-/g, "−"); };
  function decFr(s) { var p = s.split("."), k = p[1] ? p[1].length : 0, f = Math.pow(10, k); return new Fr(Math.round(parseFloat(s) * f), f); }
  function parseFr(s) {
    s = String(s).trim().replace(/,/g, ".").replace(/−/g, "-");
    var m = s.match(/^(-?\d*\.?\d+)(?:\/(-?\d*\.?\d+))?$/);
    if (!m) return null;
    var a = decFr(m[1]); if (!m[2]) return a;
    var b = decFr(m[2]); return b.zero() ? null : a.div(b);
  }

  /* ---------- nombres ---------- */
  function decTex(s) { return lang === "en" ? s : s.replace(".", "{,}"); }
  function numTex(v) {
    if (v !== v) return "\\nexists";
    if (v === Infinity) return "+\\infty";
    if (v === -Infinity) return "-\\infty";
    if (v === 0) return "0";
    var a = Math.abs(v);
    if (a >= 1e6 || a < 1e-4) {
      var e = Math.floor(Math.log10(a)), m = +(v / Math.pow(10, e)).toFixed(3);
      if (Math.abs(m) >= 10) { m = +(m / 10).toFixed(3); e++; }
      return decTex(String(m)) + "\\cdot10^{" + e + "}";
    }
    return decTex(String(+v.toPrecision(7)));
  }
  function numTxt(v) {
    if (v !== v) return "∄";
    if (v === Infinity) return "+∞";
    if (v === -Infinity) return "−∞";
    var s = String(+v.toPrecision(6));
    if (/e/.test(s)) s = v.toExponential(3);
    return (lang === "en" ? s : s.replace(".", ",")).replace(/^-/, "−");
  }
  // reconeix fraccions senzilles i potències de e
  function fracOf(v, maxD) {
    for (var d = 1; d <= maxD; d++) { var n = Math.round(v * d); if (Math.abs(n / d - v) < 1e-7 * Math.max(1, Math.abs(v))) return new Fr(n, d); }
    return null;
  }
  function niceTex(v) {
    if (v !== v || !isFinite(v)) return numTex(v);
    if (Math.abs(v) < 5e-7) return "0";
    var f = fracOf(v, 60);
    var sv = String(+v.toFixed(6));
    if (f && (f.d <= 12 || !/^-?\d+\.\d{1,3}$/.test(sv))) return f.tex();
    if (f) return decTex(sv);
    if (v > 0) { var r = fracOf(Math.log(v), 6); if (r && Math.abs(r.n) <= 40) return "e^{" + r.tex() + "}"; }
    var q = fracOf(v * v, 60);
    if (q && q.d === 1) return (v < 0 ? "-" : "") + "\\sqrt{" + q.n + "}";
    return "\\approx" + decTex(String(+v.toPrecision(6)));
  }

  /* ---------- lectura d'expressions ---------- */
  var NAMES = ["sqrt", "exp", "abs", "log", "sin", "cos", "ln", "pi", "x", "t", "a", "b", "e"];
  var FUNCS = { sqrt: 1, exp: 1, abs: 1, log: 1, sin: 1, cos: 1, ln: 1 };
  function tokenize(src) {
    var s = String(src).replace(/\s+/g, "").replace(/,/g, ".").replace(/[−–]/g, "-").replace(/[·×]/g, "*").replace(/\*\*/g, "^").replace(/√/g, "sqrt").replace(/²/g, "^2").replace(/³/g, "^3").replace(/π/g, "pi").toLowerCase();
    var out = [], i = 0, m;
    while (i < s.length) {
      var r = s.slice(i);
      if ((m = r.match(/^(\d+\.?\d*|\.\d+)/))) { out.push({ k: "n", v: m[1] }); i += m[1].length; continue; }
      if (/^[a-z]/.test(r)) {
        var hit = null;
        for (var j = 0; j < NAMES.length; j++) if (r.indexOf(NAMES[j]) === 0) { hit = NAMES[j]; break; }
        if (!hit) throw new Error("name");
        out.push({ k: FUNCS[hit] ? "f" : "v", v: hit }); i += hit.length; continue;
      }
      if ("+-*/^()".indexOf(r[0]) >= 0) { out.push({ k: r[0] }); i++; continue; }
      throw new Error("char");
    }
    return out;
  }
  function parse(src) {
    var T = tokenize(src), p = 0;
    if (!T.length) throw new Error("empty");
    function peek() { return T[p] || { k: "end" }; }
    function eat(k) { if (peek().k !== k) throw new Error("expected " + k); p++; }
    function expr() {
      var a = term();
      while (peek().k === "+" || peek().k === "-") { var o = T[p++].k; a = { t: o, a: a, b: term() }; }
      return a;
    }
    function term() {
      var a = unary();
      for (;;) {
        var k = peek().k;
        if (k === "*" || k === "/") { p++; a = { t: k, a: a, b: unary() }; }
        else if (k === "n" || k === "v" || k === "f" || k === "(") a = { t: "*", a: a, b: power(), imp: true };
        else return a;
      }
    }
    function unary() {
      if (peek().k === "-") { p++; return { t: "neg", a: unary() }; }
      if (peek().k === "+") { p++; return unary(); }
      return power();
    }
    function power() {
      var a = atom();
      if (peek().k === "^") { p++; return { t: "^", a: a, b: unary() }; }
      return a;
    }
    function atom() {
      var k = peek();
      if (k.k === "n") { p++; return { t: "n", v: parseFloat(k.v), s: k.v }; }
      if (k.k === "v") { p++; return k.v === "e" || k.v === "pi" ? { t: "c", n: k.v } : { t: "v", n: k.v }; }
      if (k.k === "f") { p++; var arg = peek().k === "(" ? atom() : power(); return { t: "f", n: k.v, a: arg }; }
      if (k.k === "(") { p++; var e = expr(); eat(")"); return { t: "()", a: e }; }
      throw new Error("atom");
    }
    var r = expr();
    if (p < T.length) throw new Error("trailing");
    return r;
  }
  function strip(n) { while (n.t === "()") n = n.a; return n; }
  var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: Math.log10, ln: Math.log, sin: Math.sin, cos: Math.cos };
  function compile(ast) {
    function ev(n, x, env) {
      switch (n.t) {
        case "n": return n.v;
        case "c": return n.n === "e" ? Math.E : Math.PI;
        case "v": return n.n === "x" || n.n === "t" ? x : (env && env[n.n] !== undefined ? env[n.n] : NaN);
        case "()": return ev(n.a, x, env);
        case "neg": return -ev(n.a, x, env);
        case "+": return ev(n.a, x, env) + ev(n.b, x, env);
        case "-": return ev(n.a, x, env) - ev(n.b, x, env);
        case "*": return ev(n.a, x, env) * ev(n.b, x, env);
        case "/": return ev(n.a, x, env) / ev(n.b, x, env);
        case "^": {
          var b = ev(n.a, x, env), e = ev(n.b, x, env);
          if (b < 0 && e !== Math.round(e)) { var q = fracOf(e, 9); if (q && q.d % 2 === 1) return (q.n % 2 ? -1 : 1) * Math.pow(-b, e); }
          return Math.pow(b, e);
        }
        case "f": return FN[n.n](ev(n.a, x, env));
      }
      return NaN;
    }
    return function (x, env) { var v = ev(ast, x, env); return v === v ? v : NaN; };
  }
  function fnOf(src) { var a = parse(src); return compile(a); }

  // TeX d'una expressió
  var PREC = { "+": 1, "-": 1, "*": 2, "/": 2, neg: 2, "^": 4 };
  function texA(n) {
    switch (n.t) {
      case "n": return decTex(n.s);
      case "c": return n.n === "e" ? "e" : "\\pi";
      case "v": return n.n;
      case "()": return texA(strip(n.a));
      case "neg": { var a = strip(n.a); var s = texA(a); return "-" + ((a.t === "+" || a.t === "-" || a.t === "neg") ? "\\left(" + s + "\\right)" : s); }
      case "+": return texA(n.a) + "+" + texA(n.b);
      case "-": { var b = strip(n.b); var sb = texA(b); return texA(n.a) + "-" + ((b.t === "+" || b.t === "-" || b.t === "neg") ? "\\left(" + sb + "\\right)" : sb); }
      case "*": {
        var l = strip(n.a), r = strip(n.b), tl = texA(l), tr = texA(r);
        if (l.t === "+" || l.t === "-") tl = "\\left(" + tl + "\\right)";
        if (r.t === "+" || r.t === "-" || r.t === "neg") tr = "\\left(" + tr + "\\right)";
        var dot = (r.t === "n" || (r.t === "^" && strip(r.a).t === "n") || (l.t === "n" && r.t === "n")) ? "\\cdot " : (/^[0-9{]/.test(tr) ? "\\cdot " : "\\,");
        if (l.t === "n" && (r.t === "v" || r.t === "f" || r.t === "c" || (r.t === "^" && strip(r.a).t !== "n") || r.t === "()" )) dot = "";
        if (n.imp && dot === "\\,") dot = "";
        return tl + dot + tr;
      }
      case "/": return "\\dfrac{" + texA(strip(n.a)) + "}{" + texA(strip(n.b)) + "}";
      case "^": {
        var base = strip(n.a), tb = texA(base);
        if (base.t !== "n" && base.t !== "v" && base.t !== "c") tb = "\\left(" + tb + "\\right)";
        return tb + "^{" + texA(strip(n.b)) + "}";
      }
      case "f": {
        var arg = texA(strip(n.a));
        if (n.n === "sqrt") return "\\sqrt{" + arg + "}";
        if (n.n === "abs") return "\\left|" + arg + "\\right|";
        if (n.n === "exp") return "e^{" + arg + "}";
        return "\\" + (n.n === "ln" ? "ln" : n.n) + "\\left(" + arg + "\\right)";
      }
    }
    return "?";
  }
  function texOf(src) { try { return texA(strip(parse(src))); } catch (e) { return "?"; } }

  /* ---------- polinomis amb coeficients fraccionaris ---------- */
  function pTrim(p) { p = p.slice(); while (p.length > 1 && p[p.length - 1].zero()) p.pop(); return p; }
  function pAdd(p, q, s) { var r = []; for (var i = 0; i < Math.max(p.length, q.length); i++) { var a = p[i] || new Fr(0), b = q[i] || new Fr(0); r.push(s < 0 ? a.sub(b) : a.add(b)); } return pTrim(r); }
  function pMul(p, q) { var r = []; for (var i = 0; i < p.length + q.length - 1; i++) r.push(new Fr(0)); p.forEach(function (a, i) { q.forEach(function (b, j) { r[i + j] = r[i + j].add(a.mul(b)); }); }); return pTrim(r); }
  function polyOf(n) {
    switch (n.t) {
      case "n": return [decFr(n.s)];
      case "v": if (n.n === "x") return [new Fr(0), new Fr(1)]; throw new Error("var");
      case "()": return polyOf(n.a);
      case "neg": return polyOf(n.a).map(function (c) { return new Fr(-c.n, c.d); });
      case "+": return pAdd(polyOf(n.a), polyOf(n.b), 1);
      case "-": return pAdd(polyOf(n.a), polyOf(n.b), -1);
      case "*": return pMul(polyOf(n.a), polyOf(n.b));
      case "/": { var d = pTrim(polyOf(n.b)); if (d.length > 1 || d[0].zero()) throw new Error("div"); return polyOf(n.a).map(function (c) { return c.div(d[0]); }); }
      case "^": {
        var e = strip(n.b); if (e.t !== "n" || !/^\d+$/.test(e.s) || +e.s > 20) throw new Error("pow");
        var b = polyOf(n.a), r = [new Fr(1)]; for (var i = 0; i < +e.s; i++) r = pMul(r, b); return r;
      }
    }
    throw new Error("poly");
  }
  function polyParse(src) { return pTrim(polyOf(parse(src))); }
  function pDeg(p) { return pTrim(p).length - 1; }
  function pEval(p, a) { var r = new Fr(0); for (var i = p.length - 1; i >= 0; i--) r = r.mul(a).add(p[i]); return r; }
  function monoTex(c, k, first) {
    if (c.zero()) return "";
    var neg = c.n < 0, ab = new Fr(Math.abs(c.n), c.d), cs = (k > 0 && ab.n === 1 && ab.d === 1) ? "" : ab.tex();
    var xs = k === 0 ? "" : k === 1 ? "x" : "x^{" + k + "}";
    return (neg ? "-" : first ? "" : "+") + cs + xs;
  }
  function pTex(p) {
    var s = "", first = true;
    for (var k = p.length - 1; k >= 0; k--) { var m = monoTex(p[k], k, first); if (m) { s += m; first = false; } }
    return s || "0";
  }
  function ruffini(p, a) { // p: coeficients de grau 0..n; divideix per (x − a)
    var c = p.slice().reverse(), row = [null], res = [c[0]];
    for (var i = 1; i < c.length; i++) { var m = res[i - 1].mul(a); row.push(m); res.push(c[i].add(m)); }
    var r = res.pop();
    return { q: res.slice().reverse(), r: r, top: c, mid: row, bot: res.concat([r]) };
  }
  function ruffHtml(R, a) {
    function td(x, cls) { return "<td" + (cls ? ' class="' + cls + '"' : "") + ">" + (x ? x.txt() : "") + "</td>"; }
    var t = "<tr><td></td>" + R.top.map(function (x) { return td(x); }).join("") + "</tr>";
    t += "<tr>" + td(a) + R.mid.map(function (x) { return td(x); }).join("") + "</tr>";
    t += "<tr><td></td>" + R.bot.map(function (x, i) { return td(x, i === R.bot.length - 1 ? "rz" : ""); }).join("") + "</tr>";
    return '<table class="rf">' + t + "</table>";
  }

  /* ---------- estimació numèrica de límits ---------- */
  // side: -1 (esquerra) o +1 (dreta); a pot ser ±Infinity
  function samples(f, a, side) {
    var out = [];
    for (var k = 1; k <= 8; k++) {
      var x = isFinite(a) ? a + side * Math.pow(10, -k) : (a > 0 ? 1 : -1) * Math.pow(10, k);
      out.push({ x: x, y: f(x) });
    }
    if (isFinite(a)) return out;
    // si les exponencials desborden aviat, anem doblant x fins on es pot calcular
    var ok = 0; while (ok < out.length && isFinite(out[ok].y)) ok++;
    if (ok >= 5) return out;
    var d = [];
    for (var x2 = 10; x2 < 1e9; x2 *= 2) {
      var y = f((a > 0 ? 1 : -1) * x2); d.push({ x: x2, y: y });
      if (!isFinite(y)) { if (y !== y) d.pop(); break; }
    }
    return d.length >= 5 ? d : out;
  }
  function analyse(S) {
    var v = S.map(function (s) { return s.y; });
    var tail = v.slice(4);
    if (tail.every(function (y) { return y !== y; })) return { k: "none" };
    var last = v[v.length - 1];
    if (last === Infinity || last === -Infinity) return { k: "inf", s: last > 0 ? 1 : -1 };
    var fin = v.filter(function (y) { return isFinite(y); });
    if (fin.length < 5) return { k: "none" };
    var w = fin.slice(-5), d = [];
    for (var i = 1; i < w.length; i++) d.push(w[i] - w[i - 1]);
    var sameSign = d.every(function (x) { return x > 0; }) || d.every(function (x) { return x < 0; });
    var notShrinking = Math.abs(d[3]) >= 0.5 * Math.abs(d[2]) && Math.abs(d[2]) >= 0.5 * Math.abs(d[1]);
    if (sameSign && notShrinking && Math.abs(d[3]) > 1e-9 * (1 + Math.abs(w[4]))) return { k: "inf", s: d[3] > 0 ? 1 : -1 };
    var best = null;
    for (var j = 2; j < fin.length; j++) {
      var dd = Math.abs(fin[j] - fin[j - 1]);
      if (best === null || dd < best.d) best = { d: dd, v: fin[j] };
    }
    if (best.d <= 1e-5 * Math.max(1, Math.abs(best.v))) return { k: "num", v: best.v };
    var shrink = Math.abs(d[3]) < 0.6 * Math.abs(d[2]) && Math.abs(d[2]) < 0.6 * Math.abs(d[1]);
    if (shrink) return { k: "num", v: w[4], approx: true };
    return { k: "osc" };
  }
  function limSide(f, a, side) { return analyse(samples(f, a, side)); }
  function limVal(r) { return r.k === "num" ? (Math.abs(r.v) < 5e-7 ? 0 : r.v) : r.k === "inf" ? r.s * Infinity : NaN; }
  function limTex(r) {
    if (r.k === "num") return niceTex(r.v);
    if (r.k === "inf") return r.s > 0 ? "+\\infty" : "-\\infty";
    return "\\nexists";
  }
  function sameLim(p, q) {
    if (p.k === "num" && q.k === "num") return Math.abs(p.v - q.v) <= 1e-5 * Math.max(1, Math.abs(p.v));
    return p.k === "inf" && q.k === "inf" && p.s === q.s;
  }
  // valor exacte quan es pot (polinomis, etc.), si no, estimació
  function sideAt(f, c, side) {
    var y = f(c);
    if (isFinite(y)) { var y2 = f(c + side * 1e-7); if (isFinite(y2) && Math.abs(y2 - y) < 1e-4 * (1 + Math.abs(y))) return { k: "num", v: y }; }
    return limSide(f, c, side);
  }
  // tipus de discontinuïtat a partir dels laterals i f(a)
  function classify(L, R, fa) {
    var fin = function (r) { return r.k === "num"; };
    if (fin(L) && fin(R) && sameLim(L, R)) return (fa === fa && isFinite(fa) && Math.abs(fa - L.v) <= 1e-5 * Math.max(1, Math.abs(fa))) ? "ok" : "ev";
    if (fin(L) && fin(R)) return "sf";
    var iL = L.k === "inf", iR = R.k === "inf";
    if (iL && iR) return "as";
    if ((iL && fin(R)) || (iR && fin(L))) return "si";
    if (fin(L) || fin(R)) return "si";
    return "as";
  }
  var BADGE = { ok: ["ok", "cont"], ev: ["ev", "ev"], sf: ["sf", "sf"], si: ["si", "si"], as: ["as", "as"] };
  function badge(c) { return '<span class="badge ' + BADGE[c][0] + '">' + u(BADGE[c][1]) + "</span>"; }

  /* ---------- dibuix de gràfiques ---------- */
  var W = 420, H = 300, ML = 30, MR = 10, MT = 10, MB = 22;
  var COLS = ["var(--accent)", "var(--accent-2)", "var(--r3)", "var(--plus)", "var(--r4)"];
  function niceStep(r) { var e = Math.pow(10, Math.floor(Math.log10(r / 6))), m = r / 6 / e; return e * (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10); }
  function numLab(x) { var s = String(+x.toFixed(6)); return (lang === "en" ? s : s.replace(".", ",")).replace("-", "−"); }
  var clipN = 0;
  /* cfg: {v:[x0,x1,y0,y1], curves:[{f,a,b,col}], va:[], ha:[], pts:[{x,y,o,col}], guides:[{x,y}], mark:[{x,y,col}], ticks:[{x,t}]} */
  function plot(svg, cfg) {
    var v = cfg.v, x0 = v[0], x1 = v[1], y0 = v[2], y1 = v[3];
    var sx = (W - ML - MR) / (x1 - x0), sy = (H - MT - MB) / (y1 - y0);
    function X(x) { return +(ML + (x - x0) * sx).toFixed(2); }
    function Y(y) { return +(H - MB - (y - y0) * sy).toFixed(2); }
    var g = "", id = "lc" + (++clipN);
    g += '<defs><clipPath id="' + id + '"><rect x="' + ML + '" y="' + MT + '" width="' + (W - ML - MR) + '" height="' + (H - MT - MB) + '"/></clipPath></defs>';
    var st = niceStep(x1 - x0), sty = niceStep(y1 - y0), t;
    for (t = Math.ceil(x0 / st) * st; t <= x1 + 1e-9; t += st) g += '<line class="g" x1="' + X(t) + '" y1="' + MT + '" x2="' + X(t) + '" y2="' + (H - MB) + '"/>';
    for (t = Math.ceil(y0 / sty) * sty; t <= y1 + 1e-9; t += sty) g += '<line class="g" x1="' + ML + '" y1="' + Y(t) + '" x2="' + (W - MR) + '" y2="' + Y(t) + '"/>';
    var ay = Math.min(Math.max(0, y0), y1), ax = Math.min(Math.max(0, x0), x1);
    g += '<line class="ax" x1="' + ML + '" y1="' + Y(ay) + '" x2="' + (W - MR) + '" y2="' + Y(ay) + '"/><line class="ax" x1="' + X(ax) + '" y1="' + MT + '" x2="' + X(ax) + '" y2="' + (H - MB) + '"/>';
    for (t = Math.ceil(x0 / st) * st; t <= x1 + 1e-9; t += st) if (Math.abs(t) > 1e-9) g += '<text x="' + X(t) + '" y="' + (H - 6) + '" text-anchor="middle">' + numLab(t) + "</text>";
    for (t = Math.ceil(y0 / sty) * sty; t <= y1 + 1e-9; t += sty) if (Math.abs(t) > 1e-9) g += '<text x="' + (ML - 4) + '" y="' + (Y(t) + 3.5) + '" text-anchor="end">' + numLab(t) + "</text>";
    var body = "";
    (cfg.ha || []).forEach(function (y) { body += '<line class="asy" x1="' + ML + '" y1="' + Y(y) + '" x2="' + (W - MR) + '" y2="' + Y(y) + '"/>'; });
    (cfg.va || []).forEach(function (x) { body += '<line class="asy" x1="' + X(x) + '" y1="' + MT + '" x2="' + X(x) + '" y2="' + (H - MB) + '"/>'; });
    (cfg.oa || []).forEach(function (q) { body += '<line class="asy" x1="' + X(x0) + '" y1="' + Y(q.m * x0 + q.n) + '" x2="' + X(x1) + '" y2="' + Y(q.m * x1 + q.n) + '"/>'; });
    (cfg.guides || []).forEach(function (q) {
      if (q.x !== undefined) body += '<line class="gd" x1="' + X(q.x) + '" y1="' + MT + '" x2="' + X(q.x) + '" y2="' + (H - MB) + '"/>';
      if (q.y !== undefined && isFinite(q.y)) body += '<line class="gd" x1="' + ML + '" y1="' + Y(q.y) + '" x2="' + (W - MR) + '" y2="' + Y(q.y) + '"/>';
    });
    var lim = (y1 - y0) * 4;
    (cfg.curves || []).forEach(function (c, ci) {
      var a = Math.max(c.a === undefined ? -Infinity : c.a, x0), b = Math.min(c.b === undefined ? Infinity : c.b, x1);
      if (!(b > a)) return;
      var N = 700, d = "", pen = false, prevY = null, eps = (b - a) * 1e-6;
      for (var i = 0; i <= N; i++) {
        var x = a + (b - a) * i / N;
        if (i === 0) x += eps; if (i === N) x -= eps;
        var y = c.f(x);
        if (!isFinite(y) || y < y0 - lim || y > y1 + lim) { pen = false; prevY = null; continue; }
        if (prevY !== null && Math.abs(y - prevY) > (y1 - y0) * 1.5) pen = false;
        d += (pen ? "L" : "M") + X(x) + "," + Y(y); pen = true; prevY = y;
      }
      body += '<path class="cv" d="' + d + '" style="stroke:' + (c.col || COLS[ci % COLS.length]) + '"/>';
    });
    (cfg.mark || []).forEach(function (q) {
      if (q.x < x0 || q.x > x1 || !isFinite(q.y) || q.y < y0 || q.y > y1) return;
      body += '<circle class="mk" cx="' + X(q.x) + '" cy="' + Y(q.y) + '" r="6" style="fill:' + (q.col || "var(--text)") + '"/>';
    });
    (cfg.pts || []).forEach(function (q) {
      if (!isFinite(q.y) || q.y < y0 - 1e-9 || q.y > y1 + 1e-9) return;
      var col = q.col || COLS[0];
      body += q.o ? '<circle class="open" cx="' + X(q.x) + '" cy="' + Y(q.y) + '" r="4.5" style="stroke:' + col + '"/>'
        : '<circle cx="' + X(q.x) + '" cy="' + Y(q.y) + '" r="4.5" style="fill:' + col + '"/>';
    });
    (cfg.labels || []).forEach(function (q) { body += '<text class="vl" x="' + X(q.x) + '" y="' + Y(q.y) + '" text-anchor="' + (q.anchor || "middle") + '">' + q.t + "</text>"; });
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.innerHTML = g + '<g clip-path="url(#' + id + ')">' + body + "</g>";
  }

  /* ---------- funcions a trossos ---------- */
  // def: {p:[expr...], c:[talls], inc:["L"|"R"], dom:[lo,hi], din:[bool,bool], at:{x:valor}}
  function pwMake(def, env) {
    var fs = def.p.map(function (e) { return compile(parse(e)); });
    var c = def.c || [], inc = def.inc || c.map(function () { return "R"; });
    var dom = def.dom || [-Infinity, Infinity], din = def.din || [true, true];
    function idx(x) {
      for (var k = 0; k < c.length; k++) { if (x < c[k]) return k; if (x === c[k]) return inc[k] === "L" ? k : k + 1; }
      return c.length;
    }
    function inDom(x) { return (x > dom[0] || (x === dom[0] && din[0])) && (x < dom[1] || (x === dom[1] && din[1])); }
    function f(x) {
      if (!inDom(x)) return NaN;
      if (def.at && def.at[x] !== undefined) return def.at[x];
      return fs[idx(x)](x, env);
    }
    function piece(i) { return function (x) { return fs[i](x, env); }; }
    function bounds(i) { return [i === 0 ? dom[0] : c[i - 1], i === c.length ? dom[1] : c[i]]; }
    return { f: f, fs: fs, piece: piece, bounds: bounds, c: c, inc: inc, dom: dom, din: din, n: fs.length, env: env };
  }
  // corbes i punts (plens/buits) per al dibuix
  function pwDraw(P, view, cols) {
    var curves = [], pts = [];
    for (var i = 0; i < P.n; i++) { var B = P.bounds(i); curves.push({ f: P.piece(i), a: B[0], b: B[1], col: (cols || [])[i] || COLS[0] }); }
    P.c.forEach(function (c, k) {
      var L = sideAt(P.piece(k), c, -1), R = sideAt(P.piece(k + 1), c, 1), fc = P.f(c);
      var col = COLS[0];
      if (L.k === "num" && R.k === "num" && sameLim(L, R) && Math.abs(fc - L.v) < 1e-6 * (1 + Math.abs(fc))) return;
      if (isFinite(fc)) pts.push({ x: c, y: fc, col: col });
      if (L.k === "num" && !(isFinite(fc) && Math.abs(fc - L.v) < 1e-9 * (1 + Math.abs(fc)))) pts.push({ x: c, y: L.v, o: true, col: col });
      if (R.k === "num" && !(isFinite(fc) && Math.abs(fc - R.v) < 1e-9 * (1 + Math.abs(fc)))) pts.push({ x: c, y: R.v, o: true, col: col });
    });
    [0, 1].forEach(function (s) {
      var x = P.dom[s]; if (!isFinite(x) || x < view[0] || x > view[1]) return;
      var y = P.piece(s ? P.n - 1 : 0)(x);
      if (isFinite(y)) pts.push({ x: x, y: y, o: !P.din[s] });
    });
    return { curves: curves, pts: pts };
  }
  function condTex(lo, loIn, hi, hiIn) {
    var L = isFinite(lo), R = isFinite(hi);
    if (L && R) return numTex(lo) + (loIn ? "\\leq " : "\\lt ") + "x" + (hiIn ? "\\leq " : "\\lt ") + numTex(hi);
    if (L) return "x" + (loIn ? "\\geq " : "\\gt ") + numTex(lo);
    if (R) return "x" + (hiIn ? "\\leq " : "\\lt ") + numTex(hi);
    return "x\\in\\mathbb R";
  }
  function pwTex(def, name) {
    var c = def.c || [], inc = def.inc || c.map(function () { return "R"; }), dom = def.dom || [-Infinity, Infinity], din = def.din || [true, true];
    var rows = def.p.map(function (e, i) {
      var lo = i === 0 ? dom[0] : c[i - 1], hi = i === c.length ? dom[1] : c[i];
      var loIn = i === 0 ? din[0] : inc[i - 1] === "R", hiIn = i === c.length ? din[1] : inc[i] === "L";
      return texOf(e) + "&\\text{" + u("pc") + " }" + condTex(lo, loIn, hi, hiIn);
    });
    return (name || "f(x)") + "=\\begin{cases}" + rows.join("\\\\[3pt]") + "\\end{cases}";
  }
  function autoY(fs, x0, x1, pad) {
    var ys = [];
    fs.forEach(function (f) { for (var i = 0; i <= 200; i++) { var y = f(x0 + (x1 - x0) * i / 200); if (isFinite(y)) ys.push(y); } });
    if (!ys.length) return [-5, 5];
    ys.sort(function (a, b) { return a - b; });
    var lo = ys[Math.floor(ys.length * 0.04)], hi = ys[Math.ceil(ys.length * 0.96) - 1];
    if (hi - lo < 1e-9) { lo -= 1; hi += 1; }
    var m = (hi - lo) * (pad || 0.15);
    return [Math.min(lo - m, -0.5), Math.max(hi + m, 0.5)];
  }

  /* ---------- figures estàtiques ---------- */
  function F(s) { return compile(parse(s)); }
  var FIGS = {
    inf1: function () { return { v: [-6, 6, -1, 3.2], curves: [{ f: F("2x^2/(x^2+1)") }], ha: [2] }; },
    inf2: function () { return { v: [-6, 4, -2, 6], curves: [{ f: F("2^x-1") }], ha: [-1] }; },
    inf3: function () { return { v: [-6, 6, -6, 6], curves: [{ f: F("x^3/10-x") }] }; },
    inf4: function () { return { v: [-10, 10, -2, 2], curves: [{ f: F("sin(x)") }] }; },
    inf5: function () { return { v: [-4, 10, -1, 4], curves: [{ f: F("sqrt(x-2)"), a: 2 }], pts: [{ x: 2, y: 0 }] }; },
    inf6: function () { return { v: [-5, 5, -1, 4], curves: [{ f: F("sqrt(9-x^2)"), a: -3, b: 3 }], pts: [{ x: -3, y: 0 }, { x: 3, y: 0 }] }; },
    pf: function () { return { v: [-6, 6, -2, 4], curves: [{ f: F("(3x^2-2)/(x^2+2)") }], ha: [3] }; },
    pg: function () { return { v: [-6, 3, -5, 3], curves: [{ f: F("2-e^x") }], ha: [2] }; },
    ph: function () { return { v: [-6, 6, -6, 6], curves: [{ f: F("-x^3/8+x") }] }; },
    grafG: function () {
      return { v: [-4, 6, -4, 6], va: [-1], curves: [{ f: F("-1/(x+1)"), a: -4, b: -1 }, { f: F("x"), a: -1, b: 2 }, { f: F("4-(x-2)^2/2"), a: 2, b: 6 }],
        pts: [{ x: -1, y: -1, o: true }, { x: 1, y: 1, o: true }, { x: 1, y: 3 }, { x: 2, y: 2, o: true }, { x: 2, y: 4 }] };
    },
    tev: function () { return { v: [-1, 3, -1, 4], guides: [{ x: 1 }], curves: [{ f: F("x/2+1") }], pts: [{ x: 1, y: 1.5, o: true }, { x: 1, y: 3 }], labels: [{ x: 1.12, y: -0.7, t: "a", anchor: "start" }] }; },
    tsf: function () { return { v: [-1, 3, -1, 4], guides: [{ x: 1 }], curves: [{ f: F("x+1"), b: 1 }, { f: F("x/2"), a: 1 }], pts: [{ x: 1, y: 2, o: true }, { x: 1, y: 0.5 }], labels: [{ x: 1.12, y: -0.7, t: "a", anchor: "start" }] }; },
    tsi: function () { return { v: [-1, 3, -2, 5], va: [1], curves: [{ f: F("1/(2(1-x))"), b: 1 }, { f: F("x-2"), a: 1 }], pts: [{ x: 1, y: -1 }], labels: [{ x: 1.12, y: -1.7, t: "a", anchor: "start" }] }; },
    tas: function () { return { v: [-1, 3, -5, 5], va: [1], curves: [{ f: F("1/(x-1)") }], labels: [{ x: 1.12, y: -4.6, t: "a", anchor: "start" }] }; },
    rat1: function () { return { v: [-3, 5, -6, 6], va: [2], ha: [1], curves: [{ f: F("(x^2-1)/(x^2-3x+2)") }], pts: [{ x: 1, y: -2, o: true }] }; },
    asV: function () { return { v: [-5, 5, -6, 6], va: [-2, 2], ha: [0], curves: [{ f: F("(x+1)/(x^2-4)") }] }; },
    asH: function () { return { v: [-8, 8, -1.5, 4.5], ha: [3], curves: [{ f: F("(3x^2-1)/(x^2+2)") }] }; },
    asO: function () { return { v: [-6, 8, -8, 12], va: [1], oa: [{ m: 1, n: 1 }], curves: [{ f: F("(x^2+3)/(x-1)") }] }; },
    pau30: function () { var def = PW.pau30, P = pwMake(def), v = [-3.5, 3.5, -1, 5], d = pwDraw(P, v); return { v: v, curves: d.curves, pts: d.pts }; }
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

  /* ---------- funcions a trossos dels exemples i de la PAU ---------- */
  var PW = {
    pau30: { p: ["3x+10", "x^2", "(x+3)/2"], c: [-2, 1], inc: ["R", "R"], dom: [-3, 3], din: [true, true] },
    pau34: { p: ["2", "x^2", "1"], c: [-3, 1], inc: ["L", "R"], dom: [-4, 2], din: [true, true] },
    pau44: { p: ["-x", "x-1", "x^2-2x-6"], c: [-1, 4], inc: ["R", "R"], dom: [-2, 6], din: [false, false] },
    pau63: { p: ["-x+15", "x^2-8x+26", "2x+2"], c: [3, 6], inc: ["L", "L"], dom: [0, 8], din: [true, true] },
    pau31: { p: ["3x", "2", "(2x-11)/(x-3)"], c: [-1, 1], inc: ["R", "R"] },
    pau70: { p: ["15.5-1.1x", "(5x+45)/(x+2)"], c: [5], inc: ["L"], dom: [0, Infinity], din: [true, false] },
    pau50: { p: ["2/x", "1", "-x^2+6x-8", "0"], c: [2, 3, 4], inc: ["L", "L", "L"], dom: [1, 5], din: [true, true] }
  };

  /* ---------- widget: límits a l'infinit ---------- */
  function presetBtns(box, n, key, onPick) {
    var bs = [];
    for (var i = 0; i < n; i++) (function (i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { onPick(i); }); box.appendChild(b); bs.push(b);
    })(i);
    onLang(function () { bs.forEach(function (b, i) { b.textContent = u(key)[i]; }); });
    return bs;
  }
  function wInf() {
    var w = document.getElementById("w-inf"); if (!w) return;
    var PRE = [
      { e: "2x^2/(x^2+1)", v: [-8, 8, -1, 3.2], ha: [2] },
      { e: "2^x-1", v: [-8, 5, -2, 8], ha: [-1] },
      { e: "x^3/10-x", v: [-8, 8, -8, 8] },
      { e: "sin(x)", v: [-12, 12, -2, 2] }
    ];
    var st = { i: 0, s: 1 }, svg = w.querySelector("svg"), rng = $(w, "n"), nv = $(w, "nv"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
    var dirB = [].slice.call($(w, "dir").querySelectorAll("button"));
    presetBtns($(w, "presets"), PRE.length, "pInf", function (i) { st.i = i; draw(); });
    dirB.forEach(function (b) { b.addEventListener("click", function () { st.s = +b.dataset.k; draw(); }); });
    rng.addEventListener("input", draw);
    function draw() {
      var P = PRE[st.i], f = F(P.e), t = +rng.value, n = Math.round(t), x = st.s * Math.pow(10, t), y = f(x);
      nv.textContent = numTxt(+x.toPrecision(3));
      dirB.forEach(function (b) { b.setAttribute("aria-pressed", String(+b.dataset.k === st.s)); });
      var rows = "";
      for (var k = 0; k <= 6; k++) { var xk = st.s * Math.pow(10, k); rows += "<tr><td" + (k === n ? ' class="hl"' : "") + ">" + tex(numTex(xk)) + "</td><td" + (k === n ? ' class="hl"' : "") + ">" + tex(numTex(f(xk))) + "</td></tr>"; }
      tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("x") + '</th><th>' + tex("f(x)=" + texOf(P.e)) + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
      var r = limSide(f, st.s * Infinity, 1);
      info.innerHTML = tex("\\lim_{x\\to" + (st.s > 0 ? "+" : "-") + "\\infty}" + texOf(P.e) + "=" + limTex(r)) + (r.k === "osc" ? " (" + u("osc") + ")" : "") +
        "<br>" + tex("f(" + numTex(+x.toPrecision(3)) + ")=" + numTex(y));
      // el punt es mou dins de la finestra; quan arriba a la vora, la finestra s'eixampla per seguir-lo
      var edge = st.s > 0 ? P.v[1] : -P.v[0], k2 = Math.max(1, Math.abs(x) * 1.15 / edge);
      plot(svg, { v: [P.v[0] * k2, P.v[1] * k2, P.v[2], P.v[3]], ha: P.ha, curves: [{ f: f }], mark: [{ x: x, y: y }], guides: [{ x: x, y: y }] });
    }
    onLang(draw);
  }

  /* ---------- widget: comparador de graus ---------- */
  function wDeg() {
    var w = document.getElementById("w-deg"); if (!w) return;
    var PRE = [["3x^2-5x+1", "x^3-x"], ["4x^3+x", "2x^3-7"], ["x^3+1", "2x-x^2"], ["-2x^3+x", "x^2+1"]];
    var ip = $(w, "p"), iq = $(w, "q"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pDeg", function (i) { ip.value = PRE[i][0]; iq.value = PRE[i][1]; draw(); });
    [ip, iq].forEach(function (i) { i.addEventListener("input", draw); });
    function draw() {
      var P, Q;
      try { P = polyParse(ip.value); ip.classList.remove("bad"); } catch (e) { ip.classList.add("bad"); info.textContent = u("badPoly"); return; }
      try { Q = polyParse(iq.value); iq.classList.remove("bad"); } catch (e) { iq.classList.add("bad"); info.textContent = u("badPoly"); return; }
      if (Q.length === 1 && Q[0].zero()) { info.textContent = u("zeroQ"); return; }
      var n = pDeg(P), m = pDeg(Q), an = P[n], bm = Q[m];
      var lt = monoTex(an, n, true) || "0", lb = monoTex(bm, m, true);
      var frac = "\\dfrac{" + pTex(P) + "}{" + pTex(Q) + "}", fl = "\\dfrac{" + lt + "}{" + lb + "}";
      var h = "<p>" + u("lead") + ": " + tex(frac + "\\ \\sim\\ " + fl) + "</p>";
      var res = [1, -1].map(function (s) {
        var sym = s > 0 ? "+\\infty" : "-\\infty", L = "\\lim_{x\\to" + sym + "}" + fl, out;
        if (P.length === 1 && P[0].zero()) out = "0";
        else if (n === m) out = an.div(bm).tex();
        else if (n < m) { var k = m - n; out = an.div(bm).tex() + "\\cdot\\dfrac{1}{" + (k === 1 ? "x" : "x^{" + k + "}") + "}"; out = "\\lim_{x\\to" + sym + "}" + out + "=0"; return tex(L + "=" + out); }
        else {
          var k2 = n - m, c = an.div(bm), sg = (c.n > 0 ? 1 : -1) * (s < 0 && k2 % 2 ? -1 : 1);
          var mono = (c.n === 1 && c.d === 1 ? "" : c.n === -1 && c.d === 1 ? "-" : c.tex()) + (k2 === 1 ? "x" : "x^{" + k2 + "}");
          return tex(L + "=\\lim_{x\\to" + sym + "}" + mono + "=" + (sg > 0 ? "+\\infty" : "-\\infty"));
        }
        return tex(L + "=" + out);
      });
      var why = n === m ? u("same") : n > m ? u("topBig") : u("botBig");
      info.innerHTML = h + "<p>" + res[0] + "</p><p>" + res[1] + "</p><p style=\"color:var(--muted)\">" + tex("n=" + n + ",\\ m=" + m) + " · " + why + "</p>";
    }
    onLang(draw);
  }

  /* ---------- widget: cursa d'infinits ---------- */
  function wRace() {
    var w = document.getElementById("w-race"); if (!w) return;
    var L = [
      { t: "\\ln x", f: Math.log, r: 0, p: 1 }, { t: "\\sqrt{x}", f: Math.sqrt, r: 1, p: 0.5 }, { t: "x", f: function (x) { return x; }, r: 1, p: 1 },
      { t: "x^2", f: function (x) { return x * x; }, r: 1, p: 2 }, { t: "x^3", f: function (x) { return x * x * x; }, r: 1, p: 3 }, { t: "x^{10}", f: function (x) { return Math.pow(x, 10); }, r: 1, p: 10 },
      { t: "1{,}1^x", f: function (x) { return Math.pow(1.1, x); }, r: 2, p: 1.1 }, { t: "2^x", f: function (x) { return Math.pow(2, x); }, r: 2, p: 2 },
      { t: "e^x", f: Math.exp, r: 2, p: Math.E }, { t: "3^x", f: function (x) { return Math.pow(3, x); }, r: 2, p: 3 }
    ];
    var sf = $(w, "f"), sg = $(w, "g"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
    L.forEach(function (o, i) { sf.add(new Option(o.t.replace("\\ln x", "ln x").replace("\\sqrt{x}", "√x").replace("{,}", lang === "en" ? "." : ",").replace("^{10}", "^10"), i)); sg.add(new Option(sf.options[i].text, i)); });
    sf.value = "5"; sg.value = "7";
    [sf, sg].forEach(function (s) { s.addEventListener("change", draw); });
    function draw() {
      var a = L[+sf.value], b = L[+sg.value], X = [10, 50, 100, 200, 500];
      var rows = X.map(function (x) { var fa = a.f(x), gb = b.f(x); return "<tr><td>" + x + "</td><td>" + tex(numTex(fa)) + "</td><td>" + tex(numTex(gb)) + "</td><td>" + tex(numTex(fa / gb)) + "</td></tr>"; }).join("");
      tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("x") + '</th><th>' + tex("f(x)=" + a.t) + "</th><th>" + tex("g(x)=" + b.t) + "</th><th>" + tex("f/g") + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
      var c = a === b ? 0 : a.r !== b.r ? a.r - b.r : a.p - b.p, msg;
      if (a === b) msg = u("ident");
      else msg = c > 0 ? u("fFaster") : c < 0 ? u("gFaster") : u("sameOrd");
      info.innerHTML = "<strong>" + msg + "</strong> " + (a === b ? "" : tex("\\lim_{x\\to+\\infty}\\dfrac{" + a.t + "}{" + b.t + "}=" + (c > 0 ? "+\\infty" : "0")));
    }
    onLang(draw);
  }

  /* ---------- widget: 1^∞ numèricament ---------- */
  function wOne() {
    var w = document.getElementById("w-one"); if (!w) return;
    var PRE = [
      { b: "(x-3)/(x-1)", e: "2x-1", s: -1, v: Math.exp(-4), t: "e^{-4}=\\dfrac{1}{e^4}" },
      { b: "(2x+1)/(2x-3)", e: "x", s: 1, v: Math.exp(2), t: "e^{2}" },
      { b: "1+3/x", e: "x", s: 1, v: Math.exp(3), t: "e^{3}" },
      { b: "(x^2+1)/x^2", e: "x", s: 1, v: 1, t: "e^{0}=1" },
      { b: "(3x-1)/(3x+2)", e: "x^2", s: 1, v: 0, t: "e^{-\\infty}=0" }
    ];
    var st = 0, rng = $(w, "n"), nv = $(w, "nv"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pOne", function (i) { st = i; draw(); });
    rng.addEventListener("input", draw);
    function draw() {
      var P = PRE[st], fb = F(P.b), fe = F(P.e), n = +rng.value; nv.textContent = n;
      var ft = "\\left(" + texOf(P.b) + "\\right)^{" + texOf(P.e) + "}", rows = "";
      for (var k = 1; k <= 7; k++) {
        var x = P.s * Math.pow(10, k), y = Math.pow(fb(x), fe(x)), c = k === n ? ' class="hl"' : "";
        rows += "<tr><td" + c + ">" + tex(numTex(x)) + "</td><td" + c + ">" + tex(numTex(y)) + "</td></tr>";
      }
      tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("x") + '</th><th>' + tex(ft) + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
      info.innerHTML = tex("\\lim_{x\\to" + (P.s > 0 ? "+" : "-") + "\\infty}" + ft + "=" + P.t) + " &nbsp;(" + u("target") + " ≈ " + numTxt(P.v) + ")";
    }
    onLang(draw);
  }

  /* ---------- widget: límits laterals ---------- */
  function wSide() {
    var w = document.getElementById("w-side"); if (!w) return;
    var PRE = [
      { d: { p: ["2x^2-6", "2x/(x-3)"], c: [1], inc: ["L"] }, a: 1, v: [-2, 2.8, -7, 4] },
      { d: { p: ["4x^2/(x^2-1)"] }, a: 1, v: [-0.5, 2.5, -30, 30], va: [1] },
      { d: { p: ["(x^2-x-2)/(x^2-4)"] }, a: 2, v: [0, 4, -0.5, 1.5], hole: true },
      { d: { p: ["3/(x-2)^2"] }, a: 2, v: [0, 4, -1, 40], va: [2] }
    ];
    var st = 0, svg = w.querySelector("svg"), rng = $(w, "n"), nv = $(w, "nv"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pSide", function (i) { st = i; draw(); });
    rng.addEventListener("input", draw);
    function draw() {
      var P = PRE[st], M = pwMake(P.d), f = M.f, a = P.a, t = +rng.value, n = Math.round(t), h = Math.pow(10, -t);
      nv.textContent = numTxt(+h.toPrecision(2));
      var rows = "";
      for (var k = 0; k <= 6; k++) {
        var hk = Math.pow(10, -k), c = k === n ? ' class="hl"' : "";
        rows += "<tr><td" + c + ">" + tex(numTex(hk)) + "</td><td" + c + ">" + tex(numTex(f(a - hk))) + "</td><td" + c + ">" + tex(numTex(f(a + hk))) + "</td></tr>";
      }
      tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("h") + '</th><th>' + tex("f(" + numTex(a) + "-h)") + "</th><th>" + tex("f(" + numTex(a) + "+h)") + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
      var L = limSide(f, a, -1), R = limSide(f, a, 1), ft = M.n > 1 ? pwTex(P.d) : "f(x)=" + texOf(P.d.p[0]);
      var concl = sameLim(L, R) ? tex("\\lim_{x\\to" + a + "}f(x)=" + limTex(L)) : tex("\\nexists\\lim_{x\\to" + a + "}f(x)");
      info.innerHTML = "<p>" + tex(ft) + "</p><p>" + tex("\\lim_{x\\to" + a + "^-}f(x)=" + limTex(L) + ",\\quad\\lim_{x\\to" + a + "^+}f(x)=" + limTex(R)) + "</p><p><strong>" + concl + "</strong></p>";
      // els punts a ± h s'acosten a a i, alhora, la finestra fa zoom al voltant de a
      var W0 = Math.min(a - P.v[0], P.v[1] - a), W = Math.min(W0, Math.max(3 * h, W0 * Math.sqrt(h))), v = P.v;
      if (W < W0) { var yy = autoY([f], a - W, a + W); v = [a - W, a + W, Math.max(yy[0], P.v[2] * 50), Math.min(yy[1], P.v[3] * 50)]; }
      var dr = pwDraw(M, v), pts = dr.pts;
      if (P.hole) pts.push({ x: a, y: L.v, o: true });
      plot(svg, { v: v, va: P.va, curves: dr.curves, pts: pts, guides: [{ x: a }], mark: [{ x: a - h, y: f(a - h), col: "var(--plus)" }, { x: a + h, y: f(a + h), col: "var(--minus)" }] });
    }
    onLang(draw);
  }

  /* ---------- widget: factoritzador (0/0) ---------- */
  function wFact() {
    var w = document.getElementById("w-fact"); if (!w) return;
    var PRE = [["x^2-x-2", "x^2-4", "2"], ["x^3-3x+2", "x^2-1", "1"], ["x^2+x", "x^2+2x+1", "-1"], ["x^2+1", "x+3", "1"]];
    var ip = $(w, "p"), iq = $(w, "q"), ia = $(w, "a"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pFact", function (i) { ip.value = PRE[i][0]; iq.value = PRE[i][1]; ia.value = PRE[i][2]; draw(); });
    [ip, iq, ia].forEach(function (i) { i.addEventListener("input", draw); });
    function draw() {
      var P, Q, a = parseFr(ia.value);
      try { P = polyParse(ip.value); ip.classList.remove("bad"); } catch (e) { ip.classList.add("bad"); info.textContent = u("badPoly"); return; }
      try { Q = polyParse(iq.value); iq.classList.remove("bad"); } catch (e) { iq.classList.add("bad"); info.textContent = u("badPoly"); return; }
      if (!a) { ia.classList.add("bad"); info.textContent = u("aBad"); return; } ia.classList.remove("bad");
      if (Q.length === 1 && Q[0].zero()) { info.textContent = u("zeroQ"); return; }
      var at = a.tex(), xa = a.n < 0 ? "x+" + new Fr(-a.n, a.d).tex() : "x-" + at;
      if (a.zero()) xa = "x";
      var limS = "\\lim_{x\\to" + at + "}", h = "", guard = 0;
      for (;;) {
        var pa = pEval(P, a), qa = pEval(Q, a), fr = "\\dfrac{" + pTex(P) + "}{" + pTex(Q) + "}";
        h += "<p>" + u(guard ? "now" : "subst") + ": " + tex(limS + fr + "=\\dfrac{" + pa.tex() + "}{" + qa.tex() + "}") + "</p>";
        if (!qa.zero()) { h += "<p>" + u("direct") + " " + tex(limS + "f(x)=" + pa.div(qa).tex()) + "</p>"; break; }
        if (!pa.zero()) {
          var m = 0, Q1 = Q; while (pEval(Q1, a).zero() && pDeg(Q1) > 0) { Q1 = ruffini(Q1, a).q; m++; }
          var sg = (pa.n > 0 ? 1 : -1) * (pEval(Q1, a).n > 0 ? 1 : -1);
          var l = sg * (m % 2 ? -1 : 1), r = sg;
          var inf = function (s) { return s > 0 ? "+\\infty" : "-\\infty"; };
          h += "<p>" + u("kz") + "</p><p>" + tex(limS.replace("}", "^-}") + "f(x)=" + inf(l) + ",\\quad " + limS.replace("}", "^+}") + "f(x)=" + inf(r)) + "</p>";
          h += "<p><strong>" + (l === r ? tex(limS + "f(x)=" + inf(r)) : tex("\\nexists" + limS + "f(x)")) + "</strong></p>";
          break;
        }
        var RP = ruffini(P, a), RQ = ruffini(Q, a);
        h += "<p>" + u("ind") + " " + tex("(" + xa + ")") + ". " + u("ruff") + ":</p><div class=\"two\"><div>" + tex("P") + ruffHtml(RP, a) + "</div><div>" + tex("Q") + ruffHtml(RQ, a) + "</div></div>";
        P = pTrim(RP.q.length ? RP.q : [new Fr(0)]); Q = pTrim(RQ.q.length ? RQ.q : [new Fr(0)]);
        h += "<p>" + u("simpl") + ": " + tex(fr + "=\\dfrac{\\cancel{(" + xa + ")}\\left(" + pTex(P) + "\\right)}{\\cancel{(" + xa + ")}\\left(" + pTex(Q) + "\\right)}") + "</p>";
        if (++guard > 8 || (Q.length === 1 && Q[0].zero())) break;
      }
      info.innerHTML = h;
    }
    onLang(draw);
  }

  /* ---------- widget: classificador de discontinuïtats ---------- */
  function wType() {
    var w = document.getElementById("w-type"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info");
    var R = ["l", "r", "f"].map(function (k) { return { s: $(w, k), i: $(w, k + "v") }; });
    R.forEach(function (o) { o.s.addEventListener("change", draw); o.i.addEventListener("input", draw); });
    function get(o) {
      if (o.s.value === "+") return { k: "inf", s: 1 };
      if (o.s.value === "-") return { k: "inf", s: -1 };
      if (o.s.value === "x") return { k: "none" };
      var v = parseFr(o.i.value); return v ? { k: "num", v: v.val() } : null;
    }
    function draw() {
      R.forEach(function (o) { o.i.style.visibility = o.s.value === "n" ? "visible" : "hidden"; });
      var L = get(R[0]), Rr = get(R[1]), fa = get(R[2]);
      if (!L || !Rr || !fa) { info.textContent = u("nanIn"); return; }
      var faV = fa.k === "num" ? fa.v : NaN, c = classify(L, Rr, faV);
      var whyI = { ok: 0, ev: 1, sf: 2, si: 3, as: 4 }[c];
      info.innerHTML = "<p><strong>" + u("clsTitle") + ":</strong> " + badge(c) + "</p><p>" + u("why")[whyI] + "</p>";
      var ys = [L, Rr].filter(function (r) { return r.k === "num"; }).map(function (r) { return r.v; });
      if (fa.k === "num") ys.push(fa.v);
      var lo = Math.min.apply(null, ys.concat([0])), hi = Math.max.apply(null, ys.concat([0]));
      var pad = Math.max(2, (hi - lo) * 0.4), v = [-3, 3, lo - pad, hi + pad];
      function br(r, side) {
        if (r.k === "num") return function (x) { return r.v + 0.35 * x * side * -1; };
        return function (x) { return r.s * (pad * 0.6) / Math.abs(x) + (r.s > 0 ? lo : hi); };
      }
      var pts = [];
      if (L.k === "num") pts.push({ x: 0, y: L.v, o: true });
      if (Rr.k === "num") pts.push({ x: 0, y: Rr.v, o: true });
      if (fa.k === "num") pts.push({ x: 0, y: fa.v });
      plot(svg, { v: v, curves: [{ f: br(L, -1), b: 0 }, { f: br(Rr, 1), a: 0 }], pts: pts, va: (L.k === "inf" || Rr.k === "inf") ? [0] : [], labels: [{ x: 0.15, y: v[2] + (v[3] - v[2]) * 0.04, t: "a", anchor: "start" }] });
    }
    onLang(draw);
  }

  /* ---------- estudi de la continuïtat d'una funció a trossos ---------- */
  function denoms(n, out) {
    if (!n || typeof n !== "object") return out;
    if (n.t === "/") out.push(compile(n.b));
    ["a", "b"].forEach(function (k) { if (n[k]) denoms(n[k], out); });
    return out;
  }
  function zerosIn(d, lo, hi, env) {
    var a = isFinite(lo) ? lo : -60, b = isFinite(hi) ? hi : 60, N = 6000, Z = [], prev = null;
    if (!(b > a)) return Z;
    for (var i = 0; i <= N; i++) {
      var x = (a * N + i * (b - a)) / N, y = d(x, env);
      if (y === 0) Z.push(x);
      else if (prev && prev.y !== 0 && isFinite(prev.y) && isFinite(y) && (prev.y < 0) !== (y < 0)) {
        var p = prev.x, q = x;
        for (var k = 0; k < 80; k++) { var m = (p + q) / 2, ym = d(m, env); if ((ym < 0) === (d(p, env) < 0)) p = m; else q = m; }
        var z = (p + q) / 2, zr = Math.round(z * 1000) / 1000; if (Math.abs(zr - z) < 1e-7) z = zr;
        if (Math.abs(d(z, env)) < 1e-6 || Math.abs(1 / d(z, env)) > 1e6) Z.push(z);
      }
      prev = { x: x, y: y };
    }
    return Z.filter(function (z, i) { return Z.indexOf(z) === i; });
  }
  function study(def, env) {
    var P = pwMake(def, env), out = { cuts: [], zeros: [], bad: [] };
    P.c.forEach(function (c, k) {
      var inside = (c > P.dom[0] || (c === P.dom[0] && P.din[0])) && (c < P.dom[1] || (c === P.dom[1] && P.din[1]));
      if (!inside) return;
      var L = sideAt(P.piece(k), c, -1), R = sideAt(P.piece(k + 1), c, 1), fa = P.f(c), cl = classify(L, R, fa);
      out.cuts.push({ x: c, L: L, R: R, fa: fa, cl: cl });
      if (cl !== "ok") out.bad.push(c);
    });
    def.p.forEach(function (e, i) {
      var B = P.bounds(i), g = P.piece(i);
      denoms(parse(e), []).forEach(function (d) {
        zerosIn(d, B[0], B[1], env).forEach(function (z) {
          var inPiece = z > B[0] && z < B[1];
          if (!inPiece || out.zeros.some(function (q) { return Math.abs(q.x - z) < 1e-9; })) return;
          var L = limSide(g, z, -1), R = limSide(g, z, 1), cl = classify(L, R, NaN);
          out.zeros.push({ x: z, i: i, L: L, R: R, cl: cl }); out.bad.push(z);
        });
      });
    });
    out.bad.sort(function (a, b) { return a - b; });
    out.P = P;
    return out;
  }
  function wPw() {
    var w = document.getElementById("w-pw"); if (!w) return;
    var KEYS = ["pau30", "pau34", "pau44", "pau63", "pau31", "pau70", "pau50"];
    var VIEWS = { pau30: [-3.5, 3.5, -1, 5], pau34: [-4.5, 2.5, -1, 10], pau44: [-2.5, 6.5, -3, 20], pau63: [-0.5, 8.5, 0, 20], pau31: [-4, 8, -8, 12], pau70: [-0.5, 20, 0, 18], pau50: [0.5, 5.5, -0.5, 2.5] };
    var box = $(w, "pcs"), svg = w.querySelector("svg"), info = w.querySelector(".info"), def = null, cur = null, view = null, rows = [];
    presetBtns($(w, "presets"), KEYS.length, "pPw", function (i) { cur = null; load(PW[KEYS[i]], VIEWS[KEYS[i]]); });
    function inp(v, cls) { var i = document.createElement("input"); i.type = "text"; i.className = "tin " + cls; i.value = v; i.autocomplete = "off"; i.spellcheck = false; i.addEventListener("input", read); return i; }
    function sel(v) { var s = document.createElement("select"); s.add(new Option("<", "R")); s.add(new Option("≤", "L")); s.value = v; s.addEventListener("change", read); return s; }
    function load(d, v) {
      def = { p: d.p.slice(), c: (d.c || []).slice(), dom: (d.dom || [-Infinity, Infinity]).slice(), din: (d.din || [true, true]).slice() };
      def.inc = (d.inc || def.c.map(function () { return "R"; })).slice();
      view = v; box.innerHTML = ""; rows = [];
      var top = document.createElement("div"); top.className = "pc";
      var lo = inp(isFinite(def.dom[0]) ? numTxt(def.dom[0]) : "", "s"), hi = inp(isFinite(def.dom[1]) ? numTxt(def.dom[1]) : "", "s");
      top.appendChild(document.createTextNode(u("interval") + ": ")); top.appendChild(lo); top.appendChild(document.createTextNode(" ≤ x ≤ ")); top.appendChild(hi);
      box.appendChild(top);
      def.p.forEach(function (e, i) {
        var r = document.createElement("div"); r.className = "pc";
        var dot = document.createElement("span"); dot.className = "dot"; dot.style.background = COLS[i % COLS.length];
        var ie = inp(e, "w"); r.appendChild(dot); r.appendChild(ie);
        var o = { e: ie };
        if (i < def.c.length) { r.appendChild(document.createTextNode(u("pc") + " x ")); o.s = sel(def.inc[i]); o.c = inp(numTxt(def.c[i]), "s"); r.appendChild(o.s); r.appendChild(o.c); }
        else r.appendChild(document.createTextNode(u("rest")));
        box.appendChild(r); rows.push(o);
      });
      rows.lo = lo; rows.hi = hi;
      read();
    }
    function read() {
      var bad = false;
      function num(i, blank) { var s = i.value.trim(); if (!s && blank !== undefined) { i.classList.remove("bad"); return blank; } var v = parseFr(s); i.classList.toggle("bad", !v); if (!v) bad = true; return v ? v.val() : 0; }
      var d = { p: [], c: [], inc: [], dom: [num(rows.lo, -Infinity), num(rows.hi, Infinity)], din: [true, true] };
      rows.forEach(function (o, i) {
        try { parse(o.e.value); o.e.classList.remove("bad"); } catch (e) { o.e.classList.add("bad"); bad = true; }
        d.p.push(o.e.value);
        if (o.c) { d.c.push(num(o.c)); d.inc.push(o.s.value); }
      });
      if (def.dom && def.din) d.din = def.din;
      for (var k = 1; k < d.c.length; k++) if (!(d.c[k] > d.c[k - 1])) bad = true;
      if (bad) { info.textContent = u("bad"); return; }
      cur = d; draw(d);
    }
    function draw(d) {
      var S = study(d), P = S.P;
      var h = "<p>" + tex(pwTex(d)) + "</p>";
      if (S.cuts.length) {
        h += '<div class="tbl-wrap"><table class="data sm"><thead><tr><th>' + tex("a") + "</th><th>" + tex("f(a)") + "</th><th>" + tex("\\lim\\limits_{x\\to a^-}") + "</th><th>" + tex("\\lim\\limits_{x\\to a^+}") + "</th><th></th></tr></thead><tbody>";
        S.cuts.forEach(function (q) { h += "<tr><td>" + tex(numTex(q.x)) + "</td><td>" + tex(niceTex(isFinite(q.fa) ? q.fa : NaN)) + "</td><td>" + tex(limTex(q.L)) + "</td><td>" + tex(limTex(q.R)) + "</td><td>" + badge(q.cl) + "</td></tr>"; });
        h += "</tbody></table></div>";
      }
      h += "<p>" + (S.zeros.length ? u("pzero") + ": " + S.zeros.map(function (q) { return tex("x=" + niceTex(q.x)) + " " + badge(q.cl); }).join(", ") : u("noDen")) + "</p>";
      h += "<p><strong>" + (S.bad.length ? u("contExc") + " " + tex("x=" + S.bad.map(function (x) { return niceTex(x); }).join(",\\ x=")) + "." : u("contAll")) + "</strong></p>";
      info.innerHTML = h;
      var dr = pwDraw(P, view, P.fs.map(function (_, i) { return COLS[i % COLS.length]; }));
      plot(svg, { v: view, curves: dr.curves, pts: dr.pts, va: S.zeros.filter(function (q) { return q.cl === "as" || q.cl === "si"; }).map(function (q) { return q.x; }) });
    }
    onLang(function () { load(cur || PW.pau30, view || VIEWS.pau30); });
  }

  /* ---------- widget: paràmetres ---------- */
  function wPar() {
    var w = document.getElementById("w-par"); if (!w) return;
    var PRE = [
      { d: { p: ["a x^2-6", "2x/(x+3)+x"], c: [1], inc: ["L"] }, tex: "f(x)=\\begin{cases}ax^2-6&\\SI x\\leq1\\\\\\dfrac{2x}{x+3}+x&\\SI x\\gt1\\end{cases}", a: [0, 12, 0.1, 5], sol: "a=\\frac{15}{2}", v: [-2, 4, -8, 8] },
      { d: { p: ["x+2", "x^2-6x+12", "-2x+a"], c: [2, 4], inc: ["R", "L"], dom: [0, 8], din: [true, true] }, tex: "f(x)=\\begin{cases}x+2&\\SI 0\\leq x\\lt2\\\\x^2-6x+12&\\SI 2\\leq x\\leq4\\\\-2x+a&\\SI 4\\lt x\\leq8\\end{cases}", a: [0, 20, 0.5, 8], sol: "a=12", v: [-0.5, 8.5, -10, 12] },
      { d: { p: ["x^3-3x-20", "2/(a-x)"], c: [3], inc: ["L"] }, tex: "f(x)=\\begin{cases}x^3-3x-20&\\SI x\\leq3\\\\\\dfrac{2}{a-x}&\\SI x\\gt3\\end{cases}", a: [-2, 6, 0.1, 0], sol: "a=2", v: [0, 6, -10, 6] },
      { d: { p: ["3x+a", "a x+2", "(2x-11)/(x-3)"], c: [-1, 1], inc: ["R", "R"] }, tex: "f(x)=\\begin{cases}3x+a&\\SI x\\lt-1\\\\ax+2&\\SI -1\\leq x\\lt1\\\\\\dfrac{2x-11}{x-3}&\\SI x\\geq1\\end{cases}", a: [-3, 6, 0.1, 0], sol: "a=\\frac52", v: [-4, 2.8, -8, 8] },
      { d: { p: ["x^2+a", "b x+1", "2x-a"], c: [1, 3], inc: ["R", "R"] }, tex: "f(x)=\\begin{cases}x^2+a&\\SI x\\lt1\\\\bx+1&\\SI 1\\leq x\\lt3\\\\2x-a&\\SI x\\geq3\\end{cases}", a: [-2, 4, 0.05, 0], b: [-2, 4, 0.05, 2], sol: "a=b=\\frac54", v: [-2, 6, -3, 10] },
      { d: { p: ["ln(x^2+a)", "(x+1)^2", "5x+b/(x+1)"], c: [1, 4], inc: ["R", "L"] }, tex: "f(x)=\\begin{cases}\\ln(x^2+a)&\\SI x\\lt1\\\\(x+1)^2&\\SI 1\\leq x\\leq4\\\\5x+\\dfrac{b}{x+1}&\\SI x\\gt4\\end{cases}", a: [1, 80, 0.1, 20], b: [0, 50, 1, 10], sol: "a=e^4-1\\approx53{,}6,\\ b=25", v: [-1, 6, 0, 40] }
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
      var fx = P.tex.replace(/\\SI /g, "\\text{" + u("pc") + " }");
      fn.innerHTML = tex(fx);
      var S = study(P.d, env), ok = S.cuts.every(function (q) { return q.cl === "ok"; });
      var near = S.cuts.every(function (q) { return q.L.k === "num" && q.R.k === "num" && Math.abs(q.L.v - q.R.v) < 0.01 && isFinite(q.fa) && Math.abs(q.fa - q.L.v) < 0.01; });
      var h = S.cuts.map(function (q) {
        return "<div>" + tex("x=" + numTex(q.x) + ":\\ \\lim_{x\\to" + numTex(q.x) + "^-}f=" + limTex(q.L) + ",\\ \\lim_{x\\to" + numTex(q.x) + "^+}f=" + limTex(q.R)) + " " + badge(q.cl) + "</div>";
      }).join("");
      h += '<p class="' + (ok ? "msg-ok" : near ? "msg-ok" : "msg-bad") + '">' + (ok ? "✓ " + u("isCont") + " " + tex(P.sol) : near ? "≈ " + u("almost") + " " + tex(P.sol) : u("notYet")) + "</p>";
      out.innerHTML = h;
      var dr = pwDraw(S.P, P.v, S.P.fs.map(function (_, i) { return COLS[i % COLS.length]; }));
      plot(svg, { v: P.v, curves: dr.curves, pts: dr.pts });
    }
    onLang(setup);
  }

  /* ---------- calculadora de límits ---------- */
  function wLab() {
    var w = document.getElementById("w-lab"); if (!w) return;
    var PRE = [["(x^2-x-2)/(x^2-4)", "2"], ["sqrt(x^2+4x)-x", "inf"], ["((2x+1)/(2x-3))^x", "inf"], ["x^2/e^x", "inf"], ["abs(x)/x", "0"], ["4x^2/(x^2-1)", "1"]];
    var fi = $(w, "f"), ai = $(w, "a"), svg = w.querySelector("svg"), tb = w.querySelector(".vtbl"), info = w.querySelector(".info");
    presetBtns($(w, "presets"), PRE.length, "pLab", function (i) { fi.value = PRE[i][0]; ai.value = PRE[i][1]; draw(); });
    [fi, ai].forEach(function (i) { i.addEventListener("input", draw); });
    function draw() {
      var f, a, s = ai.value.trim().toLowerCase().replace(/\s/g, "").replace("∞", "inf").replace("−", "-");
      try { f = fnOf(fi.value); fi.classList.remove("bad"); } catch (e) { fi.classList.add("bad"); info.textContent = u("bad"); return; }
      if (/^\+?inf/.test(s)) a = Infinity; else if (/^-inf/.test(s)) a = -Infinity;
      else { var q = parseFr(s); if (!q) { ai.classList.add("bad"); info.textContent = u("aBad"); return; } a = q.val(); }
      ai.classList.remove("bad");
      var ft = texOf(fi.value), at = isFinite(a) ? numTex(a) : a > 0 ? "+\\infty" : "-\\infty", rows = "", h;
      if (isFinite(a)) {
        for (var k = 1; k <= 6; k++) { var hk = Math.pow(10, -k); rows += "<tr><td>" + tex(numTex(a - hk)) + "</td><td>" + tex(numTex(f(a - hk))) + "</td><td>" + tex(numTex(a + hk)) + "</td><td>" + tex(numTex(f(a + hk))) + "</td></tr>"; }
        tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("x") + '</th><th>' + tex("f(x)") + '</th><th>' + tex("x") + '</th><th>' + tex("f(x)") + '</th></tr></thead><tbody>' + rows + "</tbody></table>";
        var L = limSide(f, a, -1), R = limSide(f, a, 1), fa = f(a);
        h = "<p>" + tex("f(x)=" + ft) + "</p><p>" + tex("\\lim_{x\\to" + at + "^-}f(x)=" + limTex(L) + ",\\quad\\lim_{x\\to" + at + "^+}f(x)=" + limTex(R)) + "</p>";
        h += "<p><strong>" + u("est") + ":</strong> " + (sameLim(L, R) ? tex("\\lim_{x\\to" + at + "}f(x)=" + limTex(L)) : tex("\\nexists\\lim_{x\\to" + at + "}f(x)")) + "</p>";
        h += "<p>" + tex("f(" + at + ")=" + niceTex(isFinite(fa) ? fa : NaN)) + " → " + badge(classify(L, R, fa)) + "</p>";
        var d = 3, ysv = autoY([f], a - d, a + d), vy = [ysv[0], ysv[1]];
        var pts = []; if (L.k === "num") pts.push({ x: a, y: L.v, o: !(isFinite(fa) && Math.abs(fa - L.v) < 1e-6) });
        if (R.k === "num" && !sameLim(L, R)) pts.push({ x: a, y: R.v, o: !(isFinite(fa) && Math.abs(fa - R.v) < 1e-6) });
        if (isFinite(fa)) pts.push({ x: a, y: fa });
        plot(svg, { v: [a - d, a + d, vy[0], vy[1]], curves: [{ f: f }], guides: [{ x: a }], pts: pts, va: (L.k === "inf" || R.k === "inf") ? [a] : [] });
      } else {
        for (var j = 1; j <= 7; j++) { var x = (a > 0 ? 1 : -1) * Math.pow(10, j); rows += "<tr><td>" + tex(numTex(x)) + "</td><td>" + tex(numTex(f(x))) + "</td></tr>"; }
        tb.innerHTML = '<table class="data sm"><thead><tr><th>' + tex("x") + '</th><th>' + tex("f(x)") + '</th></tr></thead><tbody>' + rows + "</tbody></table>";
        var r = limSide(f, a, 1);
        h = "<p>" + tex("f(x)=" + ft) + "</p><p><strong>" + u("est") + ":</strong> " + tex("\\lim_{x\\to" + at + "}f(x)=" + limTex(r)) + (r.k === "osc" ? " (" + u("osc") + ")" : "") + "</p>";
        var x0 = a > 0 ? -2 : -20, x1 = a > 0 ? 20 : 2, yy = autoY([f], x0, x1);
        plot(svg, { v: [x0, x1, yy[0], yy[1]], curves: [{ f: f }], ha: r.k === "num" ? [limVal(r)] : [] });
      }
      info.innerHTML = h;
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  var QUIZ = [
    { q: { va: "Si la gràfica de $f$ s'acosta a la recta $y=3$ quan $x$ es fa molt gran…", es: "Si la gráfica de $f$ se acerca a la recta $y=3$ cuando $x$ se hace muy grande…", en: "If the graph of $f$ approaches the line $y=3$ as $x$ grows…" },
      o: [{ va: "$\\lim_{x\\to+\\infty}f(x)=3$", es: "$\\lim_{x\\to+\\infty}f(x)=3$", en: "$\\lim_{x\\to+\\infty}f(x)=3$" }, { va: "$\\lim_{x\\to3}f(x)=+\\infty$", es: "$\\lim_{x\\to3}f(x)=+\\infty$", en: "$\\lim_{x\\to3}f(x)=+\\infty$" }, { va: "$f(3)=+\\infty$", es: "$f(3)=+\\infty$", en: "$f(3)=+\\infty$" }], a: 0,
      e: { va: "$y=3$ és una asímptota horitzontal per la dreta.", es: "$y=3$ es una asíntota horizontal por la derecha.", en: "$y=3$ is a horizontal asymptote on the right." } },
    { q: { va: "$\\lim_{x\\to-\\infty}(2x^3-x^2+5)$ val…", es: "$\\lim_{x\\to-\\infty}(2x^3-x^2+5)$ vale…", en: "$\\lim_{x\\to-\\infty}(2x^3-x^2+5)$ equals…" },
      o: [{ va: "$+\\infty$", es: "$+\\infty$", en: "$+\\infty$" }, { va: "$-\\infty$", es: "$-\\infty$", en: "$-\\infty$" }, { va: "$5$", es: "$5$", en: "$5$" }], a: 1,
      e: { va: "Mana el terme $2x^3$, i $(-\\infty)^3=-\\infty$.", es: "Manda el término $2x^3$, y $(-\\infty)^3=-\\infty$.", en: "The term $2x^3$ dominates, and $(-\\infty)^3=-\\infty$." } },
    { q: { va: "$\\lim_{x\\to+\\infty}\\dfrac{6x^2-1}{3x^2+x}$ val…", es: "$\\lim_{x\\to+\\infty}\\dfrac{6x^2-1}{3x^2+x}$ vale…", en: "$\\lim_{x\\to+\\infty}\\dfrac{6x^2-1}{3x^2+x}$ equals…" },
      o: [{ va: "$0$", es: "$0$", en: "$0$" }, { va: "$2$", es: "$2$", en: "$2$" }, { va: "$+\\infty$", es: "$+\\infty$", en: "$+\\infty$" }], a: 1,
      e: { va: "Mateix grau: $\\frac63=2$.", es: "Mismo grado: $\\frac63=2$.", en: "Same degree: $\\frac63=2$." } },
    { q: { va: "$\\lim_{x\\to+\\infty}\\dfrac{x^5}{e^x}$ val…", es: "$\\lim_{x\\to+\\infty}\\dfrac{x^5}{e^x}$ vale…", en: "$\\lim_{x\\to+\\infty}\\dfrac{x^5}{e^x}$ equals…" },
      o: [{ va: "$+\\infty$", es: "$+\\infty$", en: "$+\\infty$" }, { va: "$1$", es: "$1$", en: "$1$" }, { va: "$0$", es: "$0$", en: "$0$" }], a: 2,
      e: { va: "L'exponencial és un infinit d'ordre superior a qualsevol potència.", es: "La exponencial es un infinito de orden superior a cualquier potencia.", en: "The exponential is an infinity of higher order than any power." } },
    { q: { va: "Per resoldre $\\lim_{x\\to+\\infty}\\left(\\sqrt{x^2+5x}-x\\right)$…", es: "Para resolver $\\lim_{x\\to+\\infty}\\left(\\sqrt{x^2+5x}-x\\right)$…", en: "To compute $\\lim_{x\\to+\\infty}\\left(\\sqrt{x^2+5x}-x\\right)$…" },
      o: [{ va: "multipliquem i dividim pel conjugat", es: "multiplicamos y dividimos por el conjugado", en: "multiply and divide by the conjugate" }, { va: "factoritzem amb Ruffini", es: "factorizamos con Ruffini", en: "factorise with Ruffini" }, { va: "el resultat és $0$ perquè $\\infty-\\infty=0$", es: "el resultado es $0$ porque $\\infty-\\infty=0$", en: "the answer is $0$ because $\\infty-\\infty=0$" }], a: 0,
      e: { va: "Queda $\\frac{5x}{\\sqrt{x^2+5x}+x}\\to\\frac52$. Recorda: $\\infty-\\infty$ és una indeterminació.", es: "Queda $\\frac{5x}{\\sqrt{x^2+5x}+x}\\to\\frac52$. Recuerda: $\\infty-\\infty$ es una indeterminación.", en: "We get $\\frac{5x}{\\sqrt{x^2+5x}+x}\\to\\frac52$. Remember: $\\infty-\\infty$ is indeterminate." } },
    { q: { va: "$\\lim_{x\\to+\\infty}\\left(1+\\dfrac{2}{x}\\right)^{x}$ val…", es: "$\\lim_{x\\to+\\infty}\\left(1+\\dfrac{2}{x}\\right)^{x}$ vale…", en: "$\\lim_{x\\to+\\infty}\\left(1+\\dfrac{2}{x}\\right)^{x}$ equals…" },
      o: [{ va: "$1$", es: "$1$", en: "$1$" }, { va: "$e^2$", es: "$e^2$", en: "$e^2$" }, { va: "$+\\infty$", es: "$+\\infty$", en: "$+\\infty$" }], a: 1,
      e: { va: "$1^\\infty$: $e^{\\lim\\frac2x\\cdot x}=e^2$.", es: "$1^\\infty$: $e^{\\lim\\frac2x\\cdot x}=e^2$.", en: "$1^\\infty$: $e^{\\lim\\frac2x\\cdot x}=e^2$." } },
    { q: { va: "$\\lim_{x\\to3}\\dfrac{x^2-9}{x-3}$ val…", es: "$\\lim_{x\\to3}\\dfrac{x^2-9}{x-3}$ vale…", en: "$\\lim_{x\\to3}\\dfrac{x^2-9}{x-3}$ equals…" },
      o: [{ va: "$0$", es: "$0$", en: "$0$" }, { va: "no existeix", es: "no existe", en: "does not exist" }, { va: "$6$", es: "$6$", en: "$6$" }], a: 2,
      e: { va: "$\\frac{(x-3)(x+3)}{x-3}=x+3\\to6$.", es: "$\\frac{(x-3)(x+3)}{x-3}=x+3\\to6$.", en: "$\\frac{(x-3)(x+3)}{x-3}=x+3\\to6$." } },
    { q: { va: "Si $\\lim_{x\\to2^-}f(x)=1$ i $\\lim_{x\\to2^+}f(x)=4$, en $x=2$ hi ha…", es: "Si $\\lim_{x\\to2^-}f(x)=1$ y $\\lim_{x\\to2^+}f(x)=4$, en $x=2$ hay…", en: "If $\\lim_{x\\to2^-}f(x)=1$ and $\\lim_{x\\to2^+}f(x)=4$, at $x=2$ there is…" },
      o: [{ va: "una discontinuïtat evitable", es: "una discontinuidad evitable", en: "a removable discontinuity" }, { va: "una discontinuïtat de salt finit", es: "una discontinuidad de salto finito", en: "a finite jump discontinuity" }, { va: "una asímptota vertical", es: "una asíntota vertical", en: "a vertical asymptote" }], a: 1,
      e: { va: "Els laterals són nombres diferents: salt de 3 unitats.", es: "Los laterales son números distintos: salto de 3 unidades.", en: "The one-sided limits are different numbers: a jump of 3 units." } },
    { q: { va: "La funció $f(x)=\\dfrac{x-1}{x^2-1}$ en $x=1$ té una discontinuïtat…", es: "La función $f(x)=\\dfrac{x-1}{x^2-1}$ en $x=1$ tiene una discontinuidad…", en: "The function $f(x)=\\dfrac{x-1}{x^2-1}$ at $x=1$ has a discontinuity that is…" },
      o: [{ va: "evitable", es: "evitable", en: "removable" }, { va: "asimptòtica", es: "asintótica", en: "asymptotic" }, { va: "de salt finit", es: "de salto finito", en: "a finite jump" }], a: 0,
      e: { va: "$\\lim_{x\\to1}\\frac{1}{x+1}=\\frac12$ existeix, però $f(1)$ no.", es: "$\\lim_{x\\to1}\\frac{1}{x+1}=\\frac12$ existe, pero $f(1)$ no.", en: "$\\lim_{x\\to1}\\frac{1}{x+1}=\\frac12$ exists, but $f(1)$ does not." } },
    { q: { va: "Perquè $f(x)=\\begin{cases}x+a&x\\lt2\\\\x^2&x\\geq2\\end{cases}$ siga contínua, $a$ ha de valer…", es: "Para que $f(x)=\\begin{cases}x+a&x\\lt2\\\\x^2&x\\geq2\\end{cases}$ sea continua, $a$ debe valer…", en: "For $f(x)=\\begin{cases}x+a&x\\lt2\\\\x^2&x\\geq2\\end{cases}$ to be continuous, $a$ must be…" },
      o: [{ va: "$2$", es: "$2$", en: "$2$" }, { va: "$4$", es: "$4$", en: "$4$" }, { va: "$0$", es: "$0$", en: "$0$" }], a: 0,
      e: { va: "Igualem els laterals en $x=2$: $2+a=4\\Rightarrow a=2$.", es: "Igualamos los laterales en $x=2$: $2+a=4\\Rightarrow a=2$.", en: "Equate the one-sided limits at $x=2$: $2+a=4\\Rightarrow a=2$." } }
,
    { q: { va: "La funció $f(x)=\\dfrac{x+2}{x^2-9}$ té asímptotes verticals…", es: "La función $f(x)=\\dfrac{x+2}{x^2-9}$ tiene asíntotas verticales…", en: "The function $f(x)=\\dfrac{x+2}{x^2-9}$ has vertical asymptotes…" },
      o: [{ va: "$x=-3$ i $x=3$", es: "$x=-3$ y $x=3$", en: "$x=-3$ and $x=3$" }, { va: "$x=-2$", es: "$x=-2$", en: "$x=-2$" }, { va: "no en té", es: "no tiene", en: "none" }], a: 0,
      e: { va: "El denominador s'anul·la en $x=\\pm3$ i el numerador no: $\\frac{k}{0}$.", es: "El denominador se anula en $x=\\pm3$ y el numerador no: $\\frac{k}{0}$.", en: "The denominator vanishes at $x=\\pm3$ and the numerator does not: $\\frac{k}{0}$." } },
    { q: { va: "L'asímptota obliqua de $f(x)=\\dfrac{x^2+1}{x}$ és…", es: "La asíntota oblicua de $f(x)=\\dfrac{x^2+1}{x}$ es…", en: "The oblique asymptote of $f(x)=\\dfrac{x^2+1}{x}$ is…" },
      o: [{ va: "$y=x+1$", es: "$y=x+1$", en: "$y=x+1$" }, { va: "$y=1$", es: "$y=1$", en: "$y=1$" }, { va: "$y=x$", es: "$y=x$", en: "$y=x$" }], a: 2,
      e: { va: "$f(x)=x+\\frac1x$: el quocient és $x$.", es: "$f(x)=x+\\frac1x$: el cociente es $x$.", en: "$f(x)=x+\\frac1x$: the quotient is $x$." } }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Límits i continuïtat · FentMates", es: "Límites y continuidad · FentMates", en: "Limits and continuity · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }

  function init() {
    document.title = TITLES[lang];
    var D = [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, { delimiters: D, ignoredClasses: ["widget", "lab"], throwOnError: false });
      document.querySelectorAll(".widget .wt, .widget label, #w-lab label").forEach(function (el) { window.renderMathInElement(el, { delimiters: D, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wFigs, wInf, wDeg, wRace, wOne, wSide, wFact, wType, wPw, wPar, wLab, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
