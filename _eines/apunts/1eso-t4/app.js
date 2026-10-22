(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u4-done", NSEC = 11;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", write: "Escriu la resposta (un nombre o una fracció com 3/4).",
      notIrr: "És equivalent, però no és irreductible: simplifica-la!", sym: "Escriu <, > o =.",
      pBad: "Escriu un numerador entre 0 i 60 i un denominador entre 1 i 24 (com a molt 5 unitats).", reads: "Es llegeix:", asDiv: "Com a divisió:",
      proper: "És una fracció <b>pròpia</b> (numerador < denominador): és <b>menor que la unitat</b>.", unit: "Numerador = denominador: la fracció és <b>igual a la unitat</b>.",
      improper: "És una fracció <b>impròpia</b> (numerador > denominador): és <b>major que la unitat</b>.", zero: "Si el numerador és 0, la fracció val 0.",
      wholes: "Conté {k} {uu} i {r}.", wholesE: "Són exactament {k} unitats senceres.", howP: "Dividim cada unitat en <b>{b}</b> parts iguals i n'agafem <b>{a}</b>.",
      oBad: "Escriu una fracció (denominador fins a 20) i una quantitat entre 1 i 100 000.", oStep1: "Dividim entre el denominador: cada part val", oStep2: "Multipliquem pel numerador:",
      oAlt: "També podem multiplicar primer i dividir després:", tStep1: "Les {a} parts pintades valen {p}: cada part val", tStep2: "El total són {b} parts:", tCheck: "Comprovació:",
      pcBad: "Escriu un percentatge entre 0 i 100 i una quantitat entre 0 i 1 000 000.", pcFrac: "{p} de cada 100 quadrets:", pcCalc: "Percentatge de la quantitat:", pcTip: "Truc: el 10 % és dividir entre 10; el 50 %, la meitat; el 25 %, la quarta part.",
      eBad: "Escriu una fracció (numerador i denominador fins a 200) i un factor entre 1 i 10.", eAmp: "Amplificació (multipliquem dalt i baix pel mateix nombre):", eSimp: "Simplificació: dividim entre el MCD({a}, {b}) = {g}:",
      eIrr: "Ja és <b>irreductible</b>: MCD({a}, {b}) = 1.", eSame: "Totes les barres tenen la mateixa part pintada: són fraccions <b>equivalents</b>.", eOrig: "Original", eAmpL: "× {k}", eIrrL: "Irreductible",
      cBad: "Escriu nombres naturals (pots posar x en una casella).", cYes: "Els productes creuats són iguals: les fraccions <b>són equivalents</b>.", cNo: "Els productes creuats són diferents: les fraccions <b>no són equivalents</b>.",
      cIrr: "Irreductibles:", cX: "Igualem els productes creuats i aïllem la x:", cXno: "La x no és un nombre natural: {v}.", cOneX: "Només pots posar una x.",
      dBad: "Escriu entre 2 i 6 fraccions separades per comes, per exemple: 5/6, 3/4, 7/10.", dMcm: "Nou denominador: el mcm dels denominadors.", dFr: "Fracció", dOp: "mcm : denominador", dNew: "Equivalent",
      kBad: "Escriu entre 2 i 6 fraccions positives separades per comes (fins a 10 unitats).", kOrd: "De menor a major:", kCd: "Amb denominador comú {m}, només cal comparar els numeradors:",
      opBad: "Escriu nombres naturals (denominadors diferents de 0).", opMcm: "Denominadors diferents: reduïm a comú denominador amb el mcm({b}, {d}) = {m}.", opSame: "Mateix denominador: sumem o restem els numeradors.",
      opSimp: "Simplifiquem dividint entre {g}.", opMul: "Multipliquem numeradors entre si i denominadors entre si.", opDiv: "Dividir és multiplicar per la inversa (o fer productes creuats).",
      opDiv0: "No es pot dividir entre 0.", opArea: "El rectangle mesura 1 × 1: les columnes pintades són {f1} i les files, {f2}. La zona doble és {r} del total.", opBars: "Totes les barres dividides en {m} parts iguals:",
      hParse: "No entenc l'expressió. Escriu fraccions com 3/4, nombres, + − · : i parèntesis ( ) [ ].", hDiv0: "No es pot dividir entre 0.", hBig: "Els nombres es fan massa grans.",
      kinds: { mul: "Multiplicació", div: "Divisió", add: "Suma", sub: "Resta" }, inPar: "dins del parèntesi", result: "Resultat:", already: "Ja és una fracció irreductible: no hi ha res a calcular.",
      rBad: "Escriu un total entre 1 i 1 000 000 i dues fraccions pròpies (denominadors fins a 12).", rFirst: "Primer gastem {f} del total:", rLeft: "Queda:", rSecond: "Després, {f} <b>del que queda</b>:", rEnd: "Al final queda:",
      rFrac: "En fraccions del total: {f1} + {f2} + {f3} = 1.", rL1: "1a part", rL2: "2a part", rL3: "queda",
      dOf: "Calcula: $\\tfrac{{a}}{{b}}$ de {n}", dOfT: "Si $\\tfrac{{a}}{{b}}$ d'un nombre són {p}, quin és el nombre?", dPct: "Calcula el {p} % de {n}", dPctF: "Escriu el {p} % com a fracció irreductible.",
      dSimp: "Escriu la fracció irreductible de $\\tfrac{{a}}{{b}}$", dX: "Calcula x:", dCmp: "Escriu <, > o =:", dCalc: "Calcula i simplifica:",
      un: ["unitat sencera", "unitats senceres"] },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", write: "Escribe la respuesta (un número o una fracción como 3/4).",
      notIrr: "Es equivalente, pero no es irreducible: ¡simplifícala!", sym: "Escribe <, > o =.",
      pBad: "Escribe un numerador entre 0 y 60 y un denominador entre 1 y 24 (como mucho 5 unidades).", reads: "Se lee:", asDiv: "Como división:",
      proper: "Es una fracción <b>propia</b> (numerador < denominador): es <b>menor que la unidad</b>.", unit: "Numerador = denominador: la fracción es <b>igual a la unidad</b>.",
      improper: "Es una fracción <b>impropia</b> (numerador > denominador): es <b>mayor que la unidad</b>.", zero: "Si el numerador es 0, la fracción vale 0.",
      wholes: "Contiene {k} {uu} y {r}.", wholesE: "Son exactamente {k} unidades enteras.", howP: "Dividimos cada unidad en <b>{b}</b> partes iguales y tomamos <b>{a}</b>.",
      oBad: "Escribe una fracción (denominador hasta 20) y una cantidad entre 1 y 100 000.", oStep1: "Dividimos entre el denominador: cada parte vale", oStep2: "Multiplicamos por el numerador:",
      oAlt: "También podemos multiplicar primero y dividir después:", tStep1: "Las {a} partes pintadas valen {p}: cada parte vale", tStep2: "El total son {b} partes:", tCheck: "Comprobación:",
      pcBad: "Escribe un porcentaje entre 0 y 100 y una cantidad entre 0 y 1 000 000.", pcFrac: "{p} de cada 100 cuadraditos:", pcCalc: "Porcentaje de la cantidad:", pcTip: "Truco: el 10 % es dividir entre 10; el 50 %, la mitad; el 25 %, la cuarta parte.",
      eBad: "Escribe una fracción (numerador y denominador hasta 200) y un factor entre 1 y 10.", eAmp: "Amplificación (multiplicamos arriba y abajo por el mismo número):", eSimp: "Simplificación: dividimos entre el MCD({a}, {b}) = {g}:",
      eIrr: "Ya es <b>irreducible</b>: MCD({a}, {b}) = 1.", eSame: "Todas las barras tienen la misma parte pintada: son fracciones <b>equivalentes</b>.", eOrig: "Original", eAmpL: "× {k}", eIrrL: "Irreducible",
      cBad: "Escribe números naturales (puedes poner x en una casilla).", cYes: "Los productos cruzados son iguales: las fracciones <b>son equivalentes</b>.", cNo: "Los productos cruzados son distintos: las fracciones <b>no son equivalentes</b>.",
      cIrr: "Irreducibles:", cX: "Igualamos los productos cruzados y despejamos la x:", cXno: "La x no es un número natural: {v}.", cOneX: "Solo puedes poner una x.",
      dBad: "Escribe entre 2 y 6 fracciones separadas por comas, por ejemplo: 5/6, 3/4, 7/10.", dMcm: "Nuevo denominador: el mcm de los denominadores.", dFr: "Fracción", dOp: "mcm : denominador", dNew: "Equivalente",
      kBad: "Escribe entre 2 y 6 fracciones positivas separadas por comas (hasta 10 unidades).", kOrd: "De menor a mayor:", kCd: "Con denominador común {m}, solo hay que comparar los numeradores:",
      opBad: "Escribe números naturales (denominadores distintos de 0).", opMcm: "Denominadores distintos: reducimos a común denominador con el mcm({b}, {d}) = {m}.", opSame: "Mismo denominador: sumamos o restamos los numeradores.",
      opSimp: "Simplificamos dividiendo entre {g}.", opMul: "Multiplicamos numeradores entre sí y denominadores entre sí.", opDiv: "Dividir es multiplicar por la inversa (o hacer productos cruzados).",
      opDiv0: "No se puede dividir entre 0.", opArea: "El rectángulo mide 1 × 1: las columnas pintadas son {f1} y las filas, {f2}. La zona doble es {r} del total.", opBars: "Todas las barras divididas en {m} partes iguales:",
      hParse: "No entiendo la expresión. Escribe fracciones como 3/4, números, + − · : y paréntesis ( ) [ ].", hDiv0: "No se puede dividir entre 0.", hBig: "Los números se hacen demasiado grandes.",
      kinds: { mul: "Multiplicación", div: "División", add: "Suma", sub: "Resta" }, inPar: "dentro del paréntesis", result: "Resultado:", already: "Ya es una fracción irreducible: no hay nada que calcular.",
      rBad: "Escribe un total entre 1 y 1 000 000 y dos fracciones propias (denominadores hasta 12).", rFirst: "Primero gastamos {f} del total:", rLeft: "Queda:", rSecond: "Después, {f} <b>de lo que queda</b>:", rEnd: "Al final queda:",
      rFrac: "En fracciones del total: {f1} + {f2} + {f3} = 1.", rL1: "1.ª parte", rL2: "2.ª parte", rL3: "queda",
      dOf: "Calcula: $\\tfrac{{a}}{{b}}$ de {n}", dOfT: "Si $\\tfrac{{a}}{{b}}$ de un número son {p}, ¿cuál es el número?", dPct: "Calcula el {p} % de {n}", dPctF: "Escribe el {p} % como fracción irreducible.",
      dSimp: "Escribe la fracción irreducible de $\\tfrac{{a}}{{b}}$", dX: "Calcula x:", dCmp: "Escribe <, > o =:", dCalc: "Calcula y simplifica:",
      un: ["unidad entera", "unidades enteras"] },
    en: { next: "Next step", all: "Show all", reset: "Hide steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Toggle light and dark mode", write: "Type your answer (a number or a fraction like 3/4).",
      notIrr: "It's equivalent, but not in its simplest form: simplify it!", sym: "Type <, > or =.",
      pBad: "Type a numerator from 0 to 60 and a denominator from 1 to 24 (at most 5 wholes).", reads: "We read it:", asDiv: "As a division:",
      proper: "It's a <b>proper</b> fraction (numerator < denominator): it's <b>less than one whole</b>.", unit: "Numerator = denominator: the fraction is <b>equal to one whole</b>.",
      improper: "It's an <b>improper</b> fraction (numerator > denominator): it's <b>more than one whole</b>.", zero: "If the numerator is 0, the fraction is 0.",
      wholes: "It contains {k} {uu} and {r}.", wholesE: "That's exactly {k} wholes.", howP: "Split each whole into <b>{b}</b> equal parts and take <b>{a}</b>.",
      oBad: "Type a fraction (denominator up to 20) and an amount from 1 to 100,000.", oStep1: "Divide by the denominator: each part is", oStep2: "Multiply by the numerator:",
      oAlt: "We can also multiply first and divide afterwards:", tStep1: "The {a} shaded parts are worth {p}: each part is", tStep2: "The whole is {b} parts:", tCheck: "Check:",
      pcBad: "Type a percentage from 0 to 100 and an amount from 0 to 1,000,000.", pcFrac: "{p} out of every 100 squares:", pcCalc: "Percentage of the amount:", pcTip: "Tip: 10% means dividing by 10; 50% is half; 25% is a quarter.",
      eBad: "Type a fraction (numerator and denominator up to 200) and a factor from 1 to 10.", eAmp: "Scaling up (multiply top and bottom by the same number):", eSimp: "Simplifying: divide by gcd({a}, {b}) = {g}:",
      eIrr: "It's already in its <b>simplest form</b>: gcd({a}, {b}) = 1.", eSame: "All the bars have the same shaded part: the fractions are <b>equivalent</b>.", eOrig: "Original", eAmpL: "× {k}", eIrrL: "Simplest",
      cBad: "Type whole numbers (you can put x in one box).", cYes: "The cross products are equal: the fractions <b>are equivalent</b>.", cNo: "The cross products are different: the fractions <b>are not equivalent</b>.",
      cIrr: "Simplest forms:", cX: "Set the cross products equal and solve for x:", cXno: "x is not a whole number: {v}.", cOneX: "You can only put one x.",
      dBad: "Type 2 to 6 fractions separated by commas, for example: 5/6, 3/4, 7/10.", dMcm: "New denominator: the lcm of the denominators.", dFr: "Fraction", dOp: "lcm : denominator", dNew: "Equivalent",
      kBad: "Type 2 to 6 positive fractions separated by commas (up to 10 wholes).", kOrd: "From smallest to largest:", kCd: "With the common denominator {m}, we only need to compare numerators:",
      opBad: "Type whole numbers (denominators can't be 0).", opMcm: "Different denominators: use a common denominator, lcm({b}, {d}) = {m}.", opSame: "Same denominator: add or subtract the numerators.",
      opSimp: "Simplify by dividing by {g}.", opMul: "Multiply numerators together and denominators together.", opDiv: "Dividing means multiplying by the reciprocal (or cross-multiplying).",
      opDiv0: "You can't divide by 0.", opArea: "The square is 1 × 1: the shaded columns are {f1} and the rows {f2}. The double-shaded area is {r} of the whole.", opBars: "All bars split into {m} equal parts:",
      hParse: "I can't read that expression. Type fractions like 3/4, numbers, + − · : and brackets ( ) [ ].", hDiv0: "You can't divide by 0.", hBig: "The numbers get too big.",
      kinds: { mul: "Multiplication", div: "Division", add: "Addition", sub: "Subtraction" }, inPar: "inside the brackets", result: "Result:", already: "It's already a simplified fraction: nothing to work out.",
      rBad: "Type a total from 1 to 1,000,000 and two proper fractions (denominators up to 12).", rFirst: "First we spend {f} of the total:", rLeft: "Left:", rSecond: "Then {f} <b>of what is left</b>:", rEnd: "Left at the end:",
      rFrac: "As fractions of the total: {f1} + {f2} + {f3} = 1.", rL1: "1st part", rL2: "2nd part", rL3: "left",
      dOf: "Work out $\\tfrac{{a}}{{b}}$ of {n}", dOfT: "If $\\tfrac{{a}}{{b}}$ of a number is {p}, what is the number?", dPct: "Work out {p}% of {n}", dPctF: "Write {p}% as a fraction in its simplest form.",
      dSimp: "Write $\\tfrac{{a}}{{b}}$ in its simplest form", dX: "Find x:", dCmp: "Type <, > or =:", dCalc: "Work out and simplify:",
      un: ["whole", "wholes"] }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
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

  /* ---------- nombres i format ---------- */
  function pnat(s) {
    s = String(s).trim().replace(/[\s  ]/g, "");
    if (/^\d{1,3}([.]\d{3})+$/.test(s)) s = s.replace(/[.]/g, "");
    if (!/^\d+$/.test(s)) return NaN;
    return parseInt(s, 10);
  }
  function fcore(x, th) {
    if (!isFinite(x)) return "—";
    var neg = x < 0, s = String(Math.round(Math.abs(x)));
    if (s.length > 4) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, th);
    return (neg ? "-" : "") + s;
  }
  function fh(x) { return fcore(x, " "); }
  function ft(x) { return fcore(x, "\\,"); }
  /* decimal amb coma: com a molt 3 decimals, sense zeros sobrants */
  function dec(x, k) {
    var s = (Math.round(x * 1000) / 1000).toFixed(k == null ? 3 : k).replace(/\.?0+$/, "");
    var p = s.split("."); return ft(+p[0]) + (p[1] ? "{,}" + p[1] : "");
  }
  function warn(k) { return '<span class="warn">' + u(k) + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function hint(s) { return '<div class="hint">' + s + "</div>"; }

  /* ---------- aritmètica de fraccions ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function lcm(a, b) { return a / gcd(a, b) * b; }
  function rat(n, d) { if (d < 0) { n = -n; d = -d; } var g = gcd(n, d) || 1; return { n: n / g, d: d / g }; }
  function radd(a, b) { return rat(a.n * b.d + b.n * a.d, a.d * b.d); }
  function rsub(a, b) { return rat(a.n * b.d - b.n * a.d, a.d * b.d); }
  function rmul(a, b) { return rat(a.n * b.n, a.d * b.d); }
  function rdiv(a, b) { return rat(a.n * b.d, a.d * b.n); }
  function rcmp(a, b) { return a.n * b.d - b.n * a.d; }
  function rval(a) { return a.n / a.d; }
  /* fracció en TeX (sense simplificar); els enters es mostren com a enters */
  function fx(n, d) { return d === 1 ? ft(n) : (n < 0 ? "-" : "") + "\\frac{" + ft(Math.abs(n)) + "}{" + ft(d) + "}"; }
  function fr(r) { return fx(r.n, r.d); }
  function frd(r) { return r.d === 1 ? ft(r.n) : (r.n < 0 ? "-" : "") + "\\dfrac{" + ft(Math.abs(r.n)) + "}{" + ft(r.d) + "}"; }
  function frac(n, d) { return "\\frac{" + n + "}{" + d + "}"; }
  /* llegeix «3/4», «-2/5», «7» o «x» */
  function pfrac(s) {
    s = String(s).trim().replace(/[−–]/g, "-").replace(/\s/g, "");
    var m = /^(-?)(\d{1,6})(?:\/(\d{1,6}))?$/.exec(s);
    if (!m) return null;
    var n = +m[2] * (m[1] ? -1 : 1), d = m[3] ? +m[3] : 1;
    return d ? { n: n, d: d } : null;
  }
  function plist(s) {
    var parts = String(s).split(/[;,]|\s+(?=[\d-])/).map(function (x) { return x.trim(); }).filter(Boolean), out = [];
    for (var i = 0; i < parts.length; i++) { var f = pfrac(parts[i]); if (!f) return null; out.push(f); }
    return out;
  }

  /* ---------- fraccions en lletres ---------- */
  var NUMW = {
    va: ["zero", "un", "dos", "tres", "quatre", "cinc", "sis", "set", "huit", "nou", "deu", "onze", "dotze", "tretze", "catorze", "quinze", "setze", "disset", "divuit", "dinou", "vint"],
    es: ["cero", "un", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte"],
    en: ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
  };
  var DENW = {
    va: { 2: ["mig", "mitjos"], 3: ["terç", "terços"], 4: ["quart", "quarts"], 5: ["cinqué", "cinquens"], 6: ["sisé", "sisens"], 7: ["seté", "setens"], 8: ["huité", "huitens"], 9: ["nové", "novens"], 10: ["desé", "desens"],
      11: ["onzé", "onzens"], 12: ["dotzé", "dotzens"], 13: ["tretzé", "tretzens"], 14: ["catorzé", "catorzens"], 15: ["quinzé", "quinzens"], 16: ["setzé", "setzens"], 17: ["disseté", "dissetens"], 18: ["divuité", "divuitens"],
      19: ["dinové", "dinovens"], 20: ["vinté", "vintens"], 100: ["centé", "centens"] },
    es: { 2: ["medio", "medios"], 3: ["tercio", "tercios"], 4: ["cuarto", "cuartos"], 5: ["quinto", "quintos"], 6: ["sexto", "sextos"], 7: ["séptimo", "séptimos"], 8: ["octavo", "octavos"], 9: ["noveno", "novenos"], 10: ["décimo", "décimos"],
      11: ["onceavo", "onceavos"], 12: ["doceavo", "doceavos"], 13: ["treceavo", "treceavos"], 14: ["catorceavo", "catorceavos"], 15: ["quinceavo", "quinceavos"], 16: ["dieciseisavo", "dieciseisavos"], 17: ["diecisieteavo", "diecisieteavos"],
      18: ["dieciochoavo", "dieciochoavos"], 19: ["diecinueveavo", "diecinueveavos"], 20: ["veinteavo", "veinteavos"], 100: ["centésimo", "centésimos"] },
    en: { 2: ["half", "halves"], 3: ["third", "thirds"], 4: ["quarter", "quarters"], 5: ["fifth", "fifths"], 6: ["sixth", "sixths"], 7: ["seventh", "sevenths"], 8: ["eighth", "eighths"], 9: ["ninth", "ninths"], 10: ["tenth", "tenths"],
      11: ["eleventh", "elevenths"], 12: ["twelfth", "twelfths"], 13: ["thirteenth", "thirteenths"], 14: ["fourteenth", "fourteenths"], 15: ["fifteenth", "fifteenths"], 16: ["sixteenth", "sixteenths"], 17: ["seventeenth", "seventeenths"],
      18: ["eighteenth", "eighteenths"], 19: ["nineteenth", "nineteenths"], 20: ["twentieth", "twentieths"], 100: ["hundredth", "hundredths"] }
  };
  function readFrac(a, b) {
    var dn = DENW[lang][b];
    if (!dn || a > 20) return "";
    return NUMW[lang][a] + " " + dn[a === 1 ? 0 : 1];
  }

  /* ---------- dibuixos SVG ---------- */
  function gridDims(b) { var r = 1; for (var i = 1; i * i <= b; i++) if (b % i === 0) r = i; return [r, b / r]; }
  function rectUnit(x0, b, on, S) {
    var d = gridDims(b), rr = d[0], cc = d[1], cw = S * 1.4 / cc, ch = S / rr, g = "";
    for (var k = 0; k < b; k++) {
      var r = Math.floor(k / cc), c = k % cc;
      g += '<rect class="' + (k < on ? "fr-on" : "fr-off") + '" x="' + (x0 + c * cw) + '" y="' + (r * ch) + '" width="' + cw + '" height="' + ch + '"/>';
    }
    for (var c2 = 1; c2 < cc; c2++) g += '<line class="fr-ln" x1="' + (x0 + c2 * cw) + '" y1="0" x2="' + (x0 + c2 * cw) + '" y2="' + S + '"/>';
    for (var r2 = 1; r2 < rr; r2++) g += '<line class="fr-ln" x1="' + x0 + '" y1="' + (r2 * ch) + '" x2="' + (x0 + S * 1.4) + '" y2="' + (r2 * ch) + '"/>';
    return g + '<rect class="fr-ln" x="' + x0 + '" y="0" width="' + (S * 1.4) + '" height="' + S + '"/>';
  }
  function circUnit(cx, b, on, R) {
    var cy = R + 1, g = "";
    if (b === 1) return '<circle class="' + (on ? "fr-on" : "fr-off") + '" cx="' + cx + '" cy="' + cy + '" r="' + R + '"/><circle class="fr-ln" cx="' + cx + '" cy="' + cy + '" r="' + R + '"/>';
    for (var k = 0; k < b; k++) {
      var a0 = -Math.PI / 2 + k * 2 * Math.PI / b, a1 = a0 + 2 * Math.PI / b;
      g += '<path class="' + (k < on ? "fr-on" : "fr-off") + ' fr-ln" style="fill:' + (k < on ? "var(--accent)" : "var(--surface-2)") + '" d="M' + cx + " " + cy + " L" + (cx + R * Math.cos(a0)).toFixed(2) + " " + (cy + R * Math.sin(a0)).toFixed(2) +
        " A" + R + " " + R + " 0 0 1 " + (cx + R * Math.cos(a1)).toFixed(2) + " " + (cy + R * Math.sin(a1)).toFixed(2) + ' Z"/>';
    }
    return g;
  }
  /* barra horitzontal: den parts, num pintades */
  function barSVG(num, den, W, H, cls, labels) {
    var cw = W / den, g = "";
    for (var k = 0; k < den; k++) g += '<rect class="' + (k < num ? (cls || "fr-on") : "fr-off") + '" x="' + (k * cw) + '" y="1" width="' + cw + '" height="' + H + '"/>';
    for (var j = 1; j < den; j++) g += '<line class="fr-ln" style="stroke-width:' + (den > 30 ? 0.6 : 1.2) + '" x1="' + (j * cw) + '" y1="1" x2="' + (j * cw) + '" y2="' + (H + 1) + '"/>';
    if (labels) for (var q = 0; q < den; q++) g += '<text class="' + (q < num ? "fr-tw" : "fr-tm") + '" x="' + (q * cw + cw / 2) + '" y="' + (H / 2 + 5) + '" text-anchor="middle">' + labels[q] + "</text>";
    return '<svg viewBox="-1 0 ' + (W + 2) + " " + (H + 2) + '" preserveAspectRatio="none" style="max-height:' + (H + 2) + 'px">' + g + '<rect class="fr-ln" x="0" y="1" width="' + W + '" height="' + H + '"/></svg>';
  }
  /* recta numèrica de lo a hi (enters) amb subdivisions 1/den; pts = [{v: rat, l: tex, c: color}] */
  function nlineSVG(lo, hi, den, pts, seg) {
    var X0 = 30, X1 = 610, W = X1 - X0, x = function (v) { return X0 + (v - lo) / (hi - lo) * W; }, s = "", fine = (hi - lo) * den <= 60;
    s += '<line class="nl-ax" x1="' + (X0 - 14) + '" y1="40" x2="' + (X1 + 14) + '" y2="40"/>';
    if (fine) for (var k = lo * den; k <= hi * den; k++) if (k % den) s += '<line class="nl-tk" x1="' + x(k / den) + '" y1="34" x2="' + x(k / den) + '" y2="46"/>';
    for (var i = lo; i <= hi; i++) s += '<line class="nl-tb" x1="' + x(i) + '" y1="30" x2="' + x(i) + '" y2="50"/><text class="fr-t" x="' + x(i) + '" y="68" text-anchor="middle">' + i + "</text>";
    if (seg) s += '<line class="nl-seg" x1="' + x(seg[0]) + '" y1="40" x2="' + x(seg[1]) + '" y2="40"/>';
    var lab = "", rank = pts.map(function (p, j) { return j; }).sort(function (i, j) { return rval(pts[i].v) - rval(pts[j].v); });
    pts.forEach(function (p, j) {
      var xx = x(rval(p.v)), up = rank.indexOf(j) % 2 === 0;
      s += '<circle class="nl-dot" cx="' + xx + '" cy="40" r="6.5" style="fill:' + (p.c || "var(--accent)") + '"/>';
      lab += '<div style="position:absolute;left:' + (xx / 640 * 100) + "%;top:" + (up ? "-30px" : "auto") + ";bottom:" + (up ? "auto" : "-36px") + ';transform:translateX(-50%);color:' + (p.c || "var(--accent)") + '">' + tex(p.l) + "</div>";
    });
    return '<div class="nline" style="position:relative;max-width:640px;margin:40px auto 44px"><svg viewBox="0 0 640 80">' + s + "</svg>" + lab + "</div>";
  }

  /* ---------- giny: concepte de fracció ---------- */
  function wPart() {
    var w = document.getElementById("w-part"); if (!w) return;
    var A = w.querySelector('[data-k="a"]'), B = w.querySelector('[data-k="b"]'), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), shape = "rect";
    function render() {
      var a = pnat(A.value), b = pnat(B.value);
      vis.innerHTML = "";
      if (isNaN(a) || isNaN(b) || b < 1 || b > 24 || a > 60 || Math.ceil(a / b) > 5) { info.innerHTML = warn("pBad"); return; }
      var nu = Math.max(1, Math.ceil(a / b)), svg = "", S = 90;
      if (shape === "line") vis.innerHTML = nlineSVG(0, nu, b, [{ v: rat(a, b), l: frac(a, b) }], [0, a / b]);
      else {
        for (var k = 0; k < nu; k++) {
          var on = Math.max(0, Math.min(b, a - k * b));
          svg += shape === "rect" ? rectUnit(k * (S * 1.4 + 16) + 1, b, on, S) : circUnit(k * (S + 18) + S / 2 + 1, b, on, S / 2);
        }
        var Wd = shape === "rect" ? nu * (S * 1.4 + 16) - 14 : nu * (S + 18) - 14;
        vis.innerHTML = '<svg viewBox="-1 -1 ' + (Wd + 2) + " " + (S + 4) + '" style="width:' + (Wd + 2) + 'px">' + svg + "</svg>";
      }
      var h = tex(frac(a, b) + (a % b === 0 ? "=" + ft(a / b) : ""), true), rd = readFrac(a, b);
      if (rd) h += "<div>" + u("reads") + " <b>" + rd + "</b></div>";
      h += "<div>" + u("asDiv") + " " + tex(frac(a, b) + "=" + a + ":" + b + (a % b === 0 ? "=" + (a / b) : (Math.round(a / b * 1000) === a / b * 1000 ? "=" : "\\approx ") + dec(a / b))) + "</div>";
      if (a === 0) h += "<div>" + u("zero") + "</div>";
      else if (a < b) h += "<div>" + u("proper") + "</div>";
      else if (a === b) h += "<div>" + u("unit") + "</div>";
      else {
        var q = Math.floor(a / b), r = a % b;
        h += "<div>" + u("improper") + "</div>" + (r ? tex(frac(a, b) + "=" + q + "+" + frac(r, b), true) + "<div>" + fill(u("wholes"), { k: q, uu: u("un")[q > 1 ? 1 : 0], r: tex(frac(r, b)) }) + "</div>" : "<div>" + fill(u("wholesE"), { k: q }) + "</div>");
      }
      info.innerHTML = h + hint(fill(u("howP"), { a: a, b: b }));
    }
    [A, B].forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, function (k) { shape = k; render(); });
    quick2(w, function (p) { A.value = p[0]; B.value = p[1]; render(); });
    onLang(render);
  }
  function quick2(w, cb) { w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { cb(b.dataset.b.split(/[\/,;]/)); }); }); }

  /* ---------- giny: fracció d'un nombre (model de barres) ---------- */
  function wOf() {
    var w = document.getElementById("w-of"); if (!w) return;
    var A = w.querySelector('[data-k="a"]'), B = w.querySelector('[data-k="b"]'), N = w.querySelector('[data-k="n"]'), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), mode = "of";
    w.querySelectorAll("[data-p]").forEach(function (s) { s.hidden = s.dataset.p !== mode; });
    function render() {
      w.querySelectorAll("[data-p]").forEach(function (s) { s.hidden = s.dataset.p !== mode; });
      var a = pnat(A.value), b = pnat(B.value), n = pnat(N.value);
      vis.innerHTML = "";
      if (isNaN(a) || isNaN(b) || isNaN(n) || b < 1 || b > 20 || a < 1 || a > b || n < 1 || n > 100000) { info.innerHTML = warn("oBad"); return; }
      var h = "";
      if (mode === "of") {
        var p = rat(n, b), lab = [], res = rat(n * a, b);
        for (var k = 0; k < b; k++) lab.push(b <= 12 ? (p.d === 1 ? fh(p.n) : "") : "");
        vis.innerHTML = '<div class="brow"><span class="bl">' + tex(ft(n)) + "</span>" + barSVG(a, b, 600, 46, "fr-on", lab) + "</div>";
        h = tex(frac(a, b) + "\\text{ " + (lang === "en" ? "of" : "de") + " }" + ft(n), true) +
          "<div>1. " + u("oStep1") + " " + tex(ft(n) + ":" + b + "=" + fr(p)) + "</div>" +
          "<div>2. " + u("oStep2") + " " + tex(fr(p) + "\\cdot " + a + "=\\boxed{" + fr(res) + "}") + "</div>" +
          hint(u("oAlt") + " " + tex(frac(a + "\\cdot " + ft(n), b) + "=" + frac(ft(a * n), b) + "=" + fr(res)));
      } else {
        var one = rat(n, a), tot = rat(n * b, a), lab2 = [];
        for (var j = 0; j < b; j++) lab2.push(b <= 12 && one.d === 1 ? (j < a ? fh(one.n) : "?") : "");
        vis.innerHTML = '<div class="brow"><span class="bl">' + tex("?") + "</span>" + barSVG(a, b, 600, 46, "fr-on2", lab2) + "</div>";
        h = "<div>1. " + fill(u("tStep1"), { a: a, p: fh(n) }) + " " + tex(ft(n) + ":" + a + "=" + fr(one)) + "</div>" +
          "<div>2. " + fill(u("tStep2"), { b: b }) + " " + tex(fr(one) + "\\cdot " + b + "=\\boxed{" + fr(tot) + "}") + "</div>" +
          hint(u("tCheck") + " " + tex(frac(a, b) + "\\text{ " + (lang === "en" ? "of" : "de") + " }" + fr(tot) + "=" + ft(n)));
      }
      info.innerHTML = h;
    }
    [A, B, N].forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, function (k) { mode = k; render(); });
    quick2(w, function (p) { A.value = p[0]; B.value = p[1]; N.value = p[2]; render(); });
    onLang(render);
  }

  /* ---------- giny: percentatges ---------- */
  function wPct() {
    var w = document.getElementById("w-pct"); if (!w) return;
    var P = w.querySelector('[data-k="p"]'), N = w.querySelector('[data-k="n"]'), grid = w.querySelector(".pgrid"), info = w.querySelector(".info");
    function render() {
      var p = pnat(P.value), n = pnat(N.value);
      if (isNaN(p) || isNaN(n) || p > 100 || n > 1000000) { grid.innerHTML = ""; info.innerHTML = warn("pcBad"); return; }
      var g = ""; for (var k = 0; k < 100; k++) g += "<i" + (k < p ? ' class="on"' : "") + "></i>";
      grid.innerHTML = g;
      var f = rat(p, 100), v = p * n / 100;
      info.innerHTML = "<div>" + fill(u("pcFrac"), { p: p }) + " " + tex(p + "\\,\\%=" + frac(p, 100) + (f.d !== 100 ? "=" + fr(f) : "")) + "</div>" +
        "<div>" + u("pcCalc") + "</div>" + tex(p + "\\,\\%\\text{ " + (lang === "en" ? "of" : "de") + " }" + ft(n) + "=" + frac(p + "\\cdot " + ft(n), 100) + "=" + frac(ft(p * n), 100) + "=\\boxed{" + dec(v, 2) + "}", true) +
        hint(u("pcTip"));
    }
    [P, N].forEach(function (x) { x.addEventListener("input", render); });
    quick2(w, function (q) { P.value = q[0]; N.value = q[1]; render(); });
    onLang(render);
  }

  /* ---------- giny: fraccions equivalents ---------- */
  function wEq() {
    var w = document.getElementById("w-eq"); if (!w) return;
    var A = w.querySelector('[data-k="a"]'), B = w.querySelector('[data-k="b"]'), K = w.querySelector('[data-k="k"]'), vis = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var a = pnat(A.value), b = pnat(B.value), k = pnat(K.value);
      vis.innerHTML = "";
      if (isNaN(a) || isNaN(b) || isNaN(k) || b < 1 || a > 200 || b > 200 || k < 1 || k > 10) { info.innerHTML = warn("eBad"); return; }
      var g = gcd(a, b) || 1, ir = rat(a, b);
      if (a <= b && b * k <= 120) {
        var row = function (l, nn, dd, c) { return '<div class="brow"><span class="bl">' + tex(frac(nn, dd)) + "</span>" + barSVG(nn, dd, 600, 30, c) + "</div>"; };
        vis.innerHTML = row(0, a, b, "fr-on") + (k > 1 ? row(1, a * k, b * k, "fr-on2") : "") + (g > 1 ? row(2, ir.n, ir.d, "fr-on3") : "");
      }
      var amp = [frac(a, b)]; for (var j = 2; j <= 5; j++) amp.push(frac(ft(a * j), ft(b * j)));
      var h = "<div>" + u("eAmp") + "</div>" + tex(amp.join("=") + "=\\ldots", true);
      if (k > 1) h += tex(frac(a, b) + "=" + frac(a + "\\cdot " + k, b + "\\cdot " + k) + "=" + frac(a * k, b * k), true);
      h += g > 1 ? "<div>" + fill(u("eSimp"), { a: a, b: b, g: g }) + "</div>" + tex(frac(a, b) + "=" + frac(a + ":" + g, b + ":" + g) + "=\\boxed{" + fr(ir) + "}", true)
        : "<div>" + fill(u("eIrr"), { a: a, b: b }) + "</div>";
      if (a <= b && b * k <= 120 && (k > 1 || g > 1)) h += hint(u("eSame"));
      info.innerHTML = h;
    }
    [A, B, K].forEach(function (x) { x.addEventListener("input", render); });
    quick2(w, function (p) { A.value = p[0]; B.value = p[1]; if (p[2]) K.value = p[2]; render(); });
    onLang(render);
  }

  /* ---------- giny: comprovar equivalència (productes creuats) ---------- */
  function wCheck() {
    var w = document.getElementById("w-check"); if (!w) return;
    var I = ["a", "b", "c", "d"].map(function (k) { return w.querySelector('[data-k="' + k + '"]'); }), vis = w.querySelector(".fvis"), info = w.querySelector(".info");
    function box(v) {
      return '<div class="xbox"><span class="fr"><span>' + v[0] + "</span><span>" + v[1] + '</span></span><span class="xg"></span><span class="fr"><span>' + v[2] + "</span><span>" + v[3] + "</span></span>" +
        '<svg preserveAspectRatio="none" viewBox="0 0 100 100"><line class="x1" x1="34" y1="30" x2="66" y2="72"/><line class="x2" x1="34" y1="72" x2="66" y2="30"/></svg></div>';
    }
    function render() {
      var raw = I.map(function (x) { return x.value.trim().toLowerCase(); }), xs = raw.filter(function (s) { return s === "x"; }).length;
      var v = raw.map(function (s) { return s === "x" ? "x" : pnat(s); });
      vis.innerHTML = "";
      if (xs > 1) { info.innerHTML = warn("cOneX"); return; }
      if (v.some(function (t) { return t !== "x" && (isNaN(t) || t > 100000); }) || v[1] === 0 || v[3] === 0) { info.innerHTML = warn("cBad"); return; }
      vis.innerHTML = '<div class="xwrap">' + box(raw.map(function (s, i) { return v[i] === "x" ? "x" : fh(v[i]); })) + "</div>";
      var L = (v[0] === "x" ? "x" : ft(v[0])) + "\\cdot " + (v[3] === "x" ? "x" : ft(v[3])), R = (v[1] === "x" ? "x" : ft(v[1])) + "\\cdot " + (v[2] === "x" ? "x" : ft(v[2]));
      if (!xs) {
        var p = v[0] * v[3], q = v[1] * v[2], ok = p === q;
        info.innerHTML = '<div class="xprod">' + tex("\\htmlClass{a}{" + L + "=" + ft(p) + "}\\qquad \\htmlClass{b}{" + R + "=" + ft(q) + "}", true) + "</div>" +
          '<div class="' + (ok ? "verd-ok" : "verd-ko") + '">' + (ok ? "✓ " : "✗ ") + u(ok ? "cYes" : "cNo") + "</div>" +
          hint(u("cIrr") + " " + tex(frac(v[0], v[1]) + "=" + fr(rat(v[0], v[1])) + "\\qquad " + frac(v[2], v[3]) + "=" + fr(rat(v[2], v[3]))));
        return;
      }
      var xi = v.indexOf("x"), num, den, eq;
      if (xi === 0) { num = v[1] * v[2]; den = v[3]; eq = "x\\cdot " + ft(v[3]) + "=" + R + "\\ \\Rightarrow\\ x=" + frac(ft(v[1]) + "\\cdot " + ft(v[2]), ft(v[3])); }
      else if (xi === 3) { num = v[1] * v[2]; den = v[0]; eq = ft(v[0]) + "\\cdot x=" + R + "\\ \\Rightarrow\\ x=" + frac(ft(v[1]) + "\\cdot " + ft(v[2]), ft(v[0])); }
      else if (xi === 1) { num = v[0] * v[3]; den = v[2]; eq = L + "=x\\cdot " + ft(v[2]) + "\\ \\Rightarrow\\ x=" + frac(ft(v[0]) + "\\cdot " + ft(v[3]), ft(v[2])); }
      else { num = v[0] * v[3]; den = v[1]; eq = L + "=" + ft(v[1]) + "\\cdot x\\ \\Rightarrow\\ x=" + frac(ft(v[0]) + "\\cdot " + ft(v[3]), ft(v[1])); }
      if (!den) { info.innerHTML = warn("cBad"); return; }
      var xv = rat(num, den);
      info.innerHTML = "<div>" + u("cX") + "</div>" + tex(eq + "=" + frac(ft(num), ft(den)) + (xv.d === 1 ? "=\\boxed{" + ft(xv.n) + "}" : ""), true) +
        (xv.d === 1 ? "" : "<div>" + fill(u("cXno"), { v: tex(fr(xv) + "\\approx " + dec(rval(xv))) }) + "</div>");
    }
    I.forEach(function (x) { x.addEventListener("input", render); });
    quick2(w, function (p) { I.forEach(function (x, i) { x.value = p[i]; }); render(); });
    onLang(render);
  }

  /* ---------- giny: reducció a comú denominador ---------- */
  function cdTable(fs, m) {
    return '<div class="tbl-wrap"><table class="data cdtab"><thead><tr><th>' + u("dFr") + "</th>" + fs.map(function (f) { return "<td>" + tex(frac(ft(f.n), ft(f.d))) + "</td>"; }).join("") + "</tr></thead><tbody>" +
      "<tr><th>" + u("dOp") + "</th>" + fs.map(function (f) { return "<td>" + tex(ft(m) + ":" + ft(f.d) + "=" + ft(m / f.d)) + "</td>"; }).join("") + "</tr>" +
      "<tr><th>" + u("dNew") + "</th>" + fs.map(function (f) { return "<td>" + tex(frac(ft(f.n) + "\\cdot " + ft(m / f.d), ft(m)) + "=" + frac("\\boxed{" + ft(f.n * m / f.d) + "}", ft(m))) + "</td>"; }).join("") + "</tr></tbody></table></div>";
  }
  function wCd() {
    var w = document.getElementById("w-cd"); if (!w) return;
    var inp = w.querySelector(".tin"), out = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var fs = plist(inp.value);
      out.innerHTML = "";
      if (!fs || fs.length < 2 || fs.length > 6 || fs.some(function (f) { return f.n < 0 || f.d > 1000; })) { info.innerHTML = warn("dBad"); return; }
      var m = fs.map(function (f) { return f.d; }).reduce(lcm);
      if (m > 1e6) { info.innerHTML = warn("dBad"); return; }
      info.innerHTML = tex("\\text{" + (lang === "en" ? "lcm" : "mcm") + "}(" + fs.map(function (f) { return ft(f.d); }).join(",") + ")=" + ft(m), true) + hint(u("dMcm"));
      out.innerHTML = cdTable(fs, m) + tex(fs.map(function (f) { return frac(ft(f.n * m / f.d), ft(m)); }).join(",\\quad "), true);
    }
    inp.addEventListener("input", render);
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.b; render(); }); });
    onLang(render);
  }

  /* ---------- giny: comparar i ordenar ---------- */
  var COLS = ["var(--r1)", "var(--r2)", "var(--r3)", "var(--r4)", "var(--plus)", "var(--minus)"];
  function wCmp() {
    var w = document.getElementById("w-cmp"); if (!w) return;
    var inp = w.querySelector(".tin"), out = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var fs = plist(inp.value);
      out.innerHTML = "";
      if (!fs || fs.length < 2 || fs.length > 6 || fs.some(function (f) { return f.n < 0 || f.d > 1000 || f.n / f.d > 10; })) { info.innerHTML = warn("kBad"); return; }
      var m = fs.map(function (f) { return f.d; }).reduce(lcm);
      if (m > 1e6) { info.innerHTML = warn("kBad"); return; }
      var it = fs.map(function (f, i) { return { f: f, i: i, k: f.n * m / f.d }; });
      var hi = Math.max(1, Math.ceil(Math.max.apply(null, it.map(function (x) { return x.f.n / x.f.d; }))));
      out.innerHTML = nlineSVG(0, hi, m, it.map(function (x) { return { v: x.f, l: frac(x.f.n, x.f.d), c: COLS[x.i] }; }));
      var so = it.slice().sort(function (p, q) { return p.k - q.k; }), ord = "";
      so.forEach(function (x, j) { ord += (j ? '<span class="lt">' + (x.k === so[j - 1].k ? "=" : "&lt;") + "</span>" : "") + '<span style="color:' + COLS[x.i] + '">' + tex(frac(x.f.n, x.f.d)) + "</span>"; });
      info.innerHTML = "<div>" + fill(u("kCd"), { m: fh(m) }) + "</div>" + tex(it.map(function (x) { return frac(x.f.n, x.f.d) + "=" + frac("\\mathbf{" + ft(x.k) + "}", ft(m)); }).join(",\\quad "), true) +
        "<div><b>" + u("kOrd") + "</b></div>" + '<div class="ord">' + ord + "</div>";
    }
    inp.addEventListener("input", render);
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.b; render(); }); });
    onLang(render);
  }

  /* ---------- giny: operacions amb dues fraccions ---------- */
  function opSteps(a, b, c, d, op) {
    var s = [], r, F1 = frac(ft(a), ft(b)), F2 = frac(ft(c), ft(d)), sg = op === "+" ? "+" : "-";
    if (op === "+" || op === "-") {
      var m = lcm(b, d), na = a * m / b, nc = c * m / d, n = op === "+" ? na + nc : na - nc;
      if (b === d) { s.push("<div>" + u("opSame") + "</div>"); s.push(tex(F1 + sg + F2 + "=" + frac(ft(a) + sg + ft(c), ft(b)) + "=" + fx(n, m), true)); }
      else {
        s.push("<div>" + fill(u("opMcm"), { b: b, d: d, m: fh(m) }) + "</div>");
        s.push(tex(F1 + sg + F2 + "=" + frac(ft(a) + "\\cdot " + m / b, ft(m)) + sg + frac(ft(c) + "\\cdot " + m / d, ft(m)) + "=" + frac(ft(na), ft(m)) + sg + frac(ft(nc), ft(m)) + "=" + fx(n, m), true));
      }
      r = rat(n, m);
      if (r.d !== m) s.push("<div>" + fill(u("opSimp"), { g: gcd(n, m) }) + "</div>" + tex(fx(n, m) + "=\\boxed{" + fr(r) + "}", true));
      else s.push(tex("\\boxed{" + fr(r) + "}", true));
    } else if (op === "·") {
      r = rat(a * c, b * d);
      s.push("<div>" + u("opMul") + "</div>" + tex(F1 + "\\cdot " + F2 + "=" + frac(ft(a) + "\\cdot " + ft(c), ft(b) + "\\cdot " + ft(d)) + "=" + frac(ft(a * c), ft(b * d)), true));
      s.push(r.d !== b * d ? "<div>" + fill(u("opSimp"), { g: gcd(a * c, b * d) }) + "</div>" + tex(frac(ft(a * c), ft(b * d)) + "=\\boxed{" + fr(r) + "}", true) : tex("\\boxed{" + fr(r) + "}", true));
    } else {
      if (!c) return { err: u("opDiv0") };
      r = rat(a * d, b * c);
      s.push("<div>" + u("opDiv") + "</div>" + tex(F1 + ":" + F2 + "=" + F1 + "\\cdot " + frac(ft(d), ft(c)) + "=" + frac(ft(a) + "\\cdot " + ft(d), ft(b) + "\\cdot " + ft(c)) + "=" + frac(ft(a * d), ft(b * c)), true));
      s.push(r.d !== b * c ? "<div>" + fill(u("opSimp"), { g: gcd(a * d, b * c) }) + "</div>" + tex(frac(ft(a * d), ft(b * c)) + "=\\boxed{" + fr(r) + "}", true) : tex("\\boxed{" + fr(r) + "}", true));
    }
    return { s: s, r: r };
  }
  function areaSVG(a, b, c, d) {
    var S = 220, cw = S / b, ch = S / d, g = "";
    for (var i = 0; i < b; i++) for (var j = 0; j < d; j++) {
      var inA = i < a, inC = j < c;
      g += '<rect x="' + (i * cw) + '" y="' + (j * ch) + '" width="' + cw + '" height="' + ch + '" style="fill:' + (inA && inC ? "var(--r3)" : inA ? "var(--hl-a)" : inC ? "var(--hl-b)" : "var(--surface-2)") + ';stroke:var(--muted);stroke-width:.8"/>';
    }
    return '<svg viewBox="-2 -2 ' + (S + 4) + " " + (S + 4) + '" style="width:' + (S + 4) + 'px">' + g + '<rect class="fr-ln" x="0" y="0" width="' + S + '" height="' + S + '"/></svg>';
  }
  function wOps(w) {
    var I = ["a", "b", "c", "d"].map(function (k) { return w.querySelector('[data-k="' + k + '"]'); }), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), opEl = w.querySelector(".opv");
    var op = w.querySelector('.seg button[aria-pressed="true"]').dataset.k;
    function render() {
      opEl.textContent = op === "-" ? "−" : op;
      var v = I.map(function (x) { return pnat(x.value); });
      vis.innerHTML = "";
      if (v.some(function (t) { return isNaN(t) || t > 10000; }) || !v[1] || !v[3]) { info.innerHTML = warn("opBad"); return; }
      var res = opSteps(v[0], v[1], v[2], v[3], op);
      if (res.err) { info.innerHTML = warn("opDiv0"); return; }
      info.innerHTML = res.s.join("");
      var m = lcm(v[1], v[3]);
      if ((op === "+" || op === "-") && m <= 36 && v[0] <= v[1] && v[2] <= v[3] && res.r.n >= 0 && rval(res.r) <= 1) {
        var k1 = v[0] * m / v[1], k2 = v[2] * m / v[3];
        var rw = function (lab, n, cls) { return '<div class="brow"><span class="bl">' + tex(lab) + "</span>" + barSVG(n, m, 600, 26, cls) + "</div>"; };
        vis.innerHTML = hint(fill(u("opBars"), { m: m })) + rw(frac(v[0], v[1]), k1, "fr-on") + rw(frac(v[2], v[3]), k2, "fr-on2") + rw(fr(res.r), op === "+" ? k1 + k2 : k1 - k2, "fr-on3");
      } else if (op === "·" && v[0] <= v[1] && v[2] <= v[3] && v[1] <= 12 && v[3] <= 12) {
        vis.innerHTML = '<div class="figs"><figure>' + areaSVG(v[0], v[1], v[2], v[3]) + "</figure></div>" +
          hint(fill(u("opArea"), { f1: tex(frac(v[0], v[1])), f2: tex(frac(v[2], v[3])), r: tex(frac(v[0] * v[2], v[1] * v[3])) }));
      }
    }
    I.forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, function (k) { op = k; render(); });
    quick2(w, function (p) { I.forEach(function (x, i) { x.value = p[i]; }); render(); });
    onLang(render);
  }

  /* ---------- operacions combinades pas a pas (amb fraccions) ---------- */
  function tokenize(s) {
    s = s.replace(/[×xX*]/g, "·").replace(/÷/g, ":").replace(/[−–]/g, "-").replace(/\{/g, "[").replace(/\}/g, "]").replace(/[\s ]/g, "");
    var t = [], i = 0;
    while (i < s.length) {
      var c = s.charAt(i);
      if (/\d/.test(c)) {
        var m = s.slice(i).match(/^(\d+)(?:\/(\d+))?/);
        t.push({ k: "n", v: m[2] ? { n: +m[1], d: +m[2] } : { n: +m[1], d: 1 }, raw: !!m[2] }); i += m[0].length; continue;
      }
      if ("+-·:()[]".indexOf(c) >= 0) { t.push({ k: c }); i++; continue; }
      return null;
    }
    return t;
  }
  function parseExpr(s) {
    var t = tokenize(s), i = 0;
    if (!t || !t.length) return null;
    function peek() { return t[i] && t[i].k; }
    function expr() {
      var a;
      if (peek() === "-") { i++; a = term(); a = neg(a); } else a = term();
      while (peek() === "+" || peek() === "-") { var op = t[i++].k; a = { t: "b", op: op, l: a, r: term() }; }
      return a;
    }
    function neg(a) { if (a.t === "n") return { t: "n", v: { n: -a.v.n, d: a.v.d }, raw: a.raw }; return { t: "b", op: "-", l: { t: "n", v: { n: 0, d: 1 } }, r: a }; }
    function term() {
      var a = prim();
      for (;;) {
        var p = peek();
        if (p === "·" || p === ":") { i++; a = { t: "b", op: p, l: a, r: prim() }; }
        else if (p === "(" || p === "[") a = { t: "b", op: "·", l: a, r: prim() };
        else return a;
      }
    }
    function prim() {
      var p = peek();
      if (p === "n") { var tk = t[i++]; if (!tk.v.d) throw 0; return { t: "n", v: tk.v, raw: tk.raw }; }
      if (p === "(" || p === "[") { i++; var e = expr(), cl = p === "(" ? ")" : "]"; if (peek() !== cl) throw 0; i++; return e.t === "n" && e.v.n >= 0 ? e : { t: "p", k: p, e: e }; }
      throw 0;
    }
    try { var r = expr(); return i === t.length ? r : null; } catch (e) { return null; }
  }
  function isN(x) { return x.t === "n" || (x.t === "p" && x.e.t === "n"); }
  function nv(x) { return x.t === "n" ? x.v : x.e.v; }
  function first(x, pr) {
    if (x.t === "b") return first(x.l, pr) || (pr(x) ? x : null) || first(x.r, pr);
    return pr(x) ? x : null;
  }
  function grp(x) { return x.t === "p" && x.e.t !== "n"; }
  /* ordre: parèntesis (de dins cap a fora) → · i : → + i − (sempre d'esquerra a dreta) */
  function target(x, inG) {
    var g = first(x, grp);
    if (g) return target(g.e, true);
    var y = first(x, function (z) { return z.t === "b" && (z.op === "·" || z.op === ":") && isN(z.l) && isN(z.r); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "+" || z.op === "-") && isN(z.l) && isN(z.r); });
    return y ? { n: y, g: !!inG } : null;
  }
  function applyOp(y) {
    var a = nv(y.l), b = nv(y.r);
    if (y.op === "+") return { v: radd(a, b), k: "add" };
    if (y.op === "-") return { v: rsub(a, b), k: "sub" };
    if (y.op === "·") return { v: rmul(a, b), k: "mul" };
    return !b.n ? { err: u("hDiv0") } : { v: rdiv(a, b), k: "div" };
  }
  function repl(x, tg, nw) {
    if (x === tg) return nw;
    if (x.t === "b") return { t: "b", op: x.op, l: repl(x.l, tg, nw), r: repl(x.r, tg, nw) };
    if (x.t === "p") { var e = repl(x.e, tg, nw); return e.t === "n" && e.v.n >= 0 ? e : { t: "p", k: x.k, e: e }; }
    return x;
  }
  function tx(x, tg, val, top) {
    var s;
    if (x.t === "n") { s = fx(x.v.n, x.v.d); if (x.v.n < 0 && !top) s = "\\Bigl(" + s + "\\Bigr)"; }
    else if (x.t === "p") s = x.k === "(" ? "\\Bigl(" + tx(x.e, tg, val, true) + "\\Bigr)" : "\\Bigl[" + tx(x.e, tg, val, true) + "\\Bigr]";
    else s = tx(x.l, tg, val, top) + { "+": "+", "-": "-", "·": "\\cdot ", ":": ":" }[x.op] + tx(x.r, tg, val, false);
    return x === tg ? "\\underbrace{\\htmlClass{hl}{" + s + "}}_{\\htmlClass{hlv}{\\textstyle " + fr(val) + "}}" : s;
  }
  function run(s) {
    var tree = parseExpr(s), rows = [];
    if (!tree) return { err: u("hParse"), rows: rows };
    var simp = function (x) {
      if (x.t === "n") { var r = rat(x.v.n, x.v.d); return r.n !== x.v.n || r.d !== x.v.d ? r : null; }
      return null;
    };
    if (tree.t === "n") { var r0 = simp(tree); return r0 ? { ok: true, v: r0, rows: [{ t: fx(tree.v.n, tree.v.d) + "=" + fr(r0), k: "simp" }] } : { ok: true, v: tree.v, rows: rows }; }
    for (var guard = 0; guard < 60; guard++) {
      var tg = target(tree);
      if (!tg) break;
      var r = applyOp(tg.n);
      if (!r.err && (Math.abs(r.v.n) > 1e9 || r.v.d > 1e9)) r = { err: u("hBig") };
      if (r.err) return { err: r.err, rows: rows, last: tx(tree, null, null, true) };
      rows.push({ t: tx(tree, tg.n, r.v, true), k: r.k, g: tg.g });
      tree = repl(tree, tg.n, { t: "n", v: r.v });
    }
    var fin = tree.t === "p" ? tree.e : tree;
    return { ok: true, v: fin.v, rows: rows, src: s };
  }
  function rowsHTML(res) {
    return res.rows.map(function (r, i) {
      var k = u("kinds")[r.k] || "";
      return '<div class="hrow">' + (k ? '<span class="hk">' + (i + 1) + " · " + k + (r.g ? " <small>(" + u("inPar") + ")</small>" : "") + "</span>" : "") + tex(r.t) + "</div>";
    });
  }
  function wHier(w) {
    var inp = w.querySelector(".tin"), box = w.querySelector(".hsteps"), info = w.querySelector(".info"), shown = 1;
    var bn = w.querySelector('[data-a="next"]'), ba = w.querySelector('[data-a="all"]'), cnt = w.querySelector(".step-count"), ctl = w.querySelector(".steps-ctl");
    function render() {
      var res = run(inp.value), rows = rowsHTML(res), n = rows.length;
      if (shown > n) shown = Math.max(1, n);
      var end = res.ok && (n === 0 || shown >= n);
      box.innerHTML = rows.map(function (h, i) { return i < shown ? h : ""; }).join("");
      ctl.hidden = n < 2;
      bn.textContent = u("next") + " →"; bn.disabled = shown >= n;
      ba.textContent = shown >= n ? u("reset") : u("all");
      cnt.textContent = u("step") + " " + Math.min(shown, n) + " " + u("of") + " " + n;
      if (!res.ok) info.innerHTML = (res.last ? tex(res.last) + "<br>" : "") + '<span class="warn">' + res.err + "</span>";
      else if (n === 0) info.innerHTML = '<span class="hint">' + u("already") + "</span>";
      else info.innerHTML = end ? "<b>" + u("result") + "</b> " + tex("\\boxed{" + frd(res.v) + "}") : "";
    }
    inp.addEventListener("input", function () { shown = 1; render(); });
    bn.addEventListener("click", function () { shown++; render(); });
    ba.addEventListener("click", function () { var n = run(inp.value).rows.length; shown = shown >= n ? 1 : n; render(); });
    w.querySelectorAll(".quick button[data-e]").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.e; shown = 1; render(); }); });
    w.querySelectorAll(".quick button[data-ins]").forEach(function (b) {
      b.addEventListener("click", function () {
        var a = inp.selectionStart == null ? inp.value.length : inp.selectionStart, z = inp.selectionEnd == null ? a : inp.selectionEnd;
        inp.value = inp.value.slice(0, a) + b.dataset.ins + inp.value.slice(z);
        inp.focus(); inp.setSelectionRange(a + b.dataset.ins.length, a + b.dataset.ins.length); shown = 1; render();
      });
    });
    onLang(render);
  }

  /* ---------- giny: fracció del que queda ---------- */
  function wRest() {
    var w = document.getElementById("w-rest"); if (!w) return;
    var T = w.querySelector('[data-k="t"]'), A = w.querySelector('[data-k="a"]'), B = w.querySelector('[data-k="b"]'), C = w.querySelector('[data-k="c"]'), D = w.querySelector('[data-k="d"]');
    var vis = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var t = pnat(T.value), a = pnat(A.value), b = pnat(B.value), c = pnat(C.value), d = pnat(D.value);
      vis.innerHTML = "";
      if ([t, a, b, c, d].some(isNaN) || t < 1 || t > 1000000 || !b || !d || b > 12 || d > 12 || a >= b || c >= d || !a || !c) { info.innerHTML = warn("rBad"); return; }
      var f1 = rat(a, b), left1 = rat(b - a, b), f2 = rmul(rat(c, d), left1), f3 = rsub(left1, f2);
      var v1 = rmul(f1, rat(t, 1)), l1 = rmul(left1, rat(t, 1)), v2 = rmul(f2, rat(t, 1)), v3 = rmul(f3, rat(t, 1));
      var n = b * d, W = 600, H = 46, cw = W / n, g = "", n1 = a * d, n2 = c * (b - a);
      for (var k = 0; k < n; k++) g += '<rect class="' + (k < n1 ? "fr-on" : k < n1 + n2 ? "fr-on2" : "fr-off") + '" x="' + (k * cw) + '" y="1" width="' + cw + '" height="' + H + '"/>';
      for (var j = 1; j <= a; j++) g += '<line class="fr-ln" style="stroke-width:2" x1="' + (j * d * cw) + '" y1="1" x2="' + (j * d * cw) + '" y2="' + (H + 1) + '"/>';
      for (var q = 1; q < d; q++) g += '<line class="fr-ln" x1="' + ((n1 + q * (b - a)) * cw) + '" y1="1" x2="' + ((n1 + q * (b - a)) * cw) + '" y2="' + (H + 1) + '"/>';
      var lab = function (x0, x1, txt) { return x1 - x0 > 40 ? '<text class="fr-t" x="' + ((x0 + x1) / 2) + '" y="' + (H + 20) + '" text-anchor="middle">' + txt + "</text>" : ""; };
      g += lab(0, n1 * cw, u("rL1")) + lab(n1 * cw, (n1 + n2) * cw, u("rL2")) + lab((n1 + n2) * cw, W, u("rL3"));
      vis.innerHTML = '<svg viewBox="-1 0 ' + (W + 2) + " " + (H + 28) + '">' + g + '<rect class="fr-ln" x="0" y="1" width="' + W + '" height="' + H + '"/></svg>';
      var of = "\\text{ " + (lang === "en" ? "of" : "de") + " }";
      info.innerHTML = "<div>1. " + fill(u("rFirst"), { f: tex(fr(f1)) }) + " " + tex(fr(f1) + of + ft(t) + "=" + fr(v1)) + " &nbsp; " + u("rLeft") + " " + tex(ft(t) + "-" + fr(v1) + "=" + fr(l1)) + "</div>" +
        "<div>2. " + fill(u("rSecond"), { f: tex(frac(c, d)) }) + " " + tex(frac(c, d) + of + fr(l1) + "=" + fr(v2)) + "</div>" +
        "<div>3. " + u("rEnd") + " " + tex(fr(l1) + "-" + fr(v2) + "=\\boxed{" + fr(v3) + "}") + "</div>" +
        hint(fill(u("rFrac"), { f1: tex(fr(f1)), f2: tex(frac(c, d) + "\\cdot " + fr(left1) + "=" + fr(f2)), f3: tex(fr(f3)) }));
    }
    [T, A, B, C, D].forEach(function (x) { x.addEventListener("input", render); });
    quick2(w, function (p) { [T, A, B, C, D].forEach(function (x, i) { x.value = p[i]; }); render(); });
    onLang(render);
  }

  /* ---------- entrenadors ---------- */
  function coprimeNum(b) { var a; do { a = rint(1, b - 1); } while (gcd(a, b) !== 1); return a; }
  function randFr(maxD) { var b = rint(2, maxD); return { n: coprimeNum(b), d: b }; }
  var GEN = {
    of: function () {
      var b = rint(2, 10), a = coprimeNum(b), k = rint(2, 15), n = b * k;
      if (Math.random() < .35) {
        var p = a * k;
        return { t: "nat", ans: n, q: function () { return fill(u("dOfT"), { a: a, b: b, p: p }); },
          s: function () { return tex(ft(p) + ":" + a + "=" + k + "\\qquad " + k + "\\cdot " + b + "=\\boxed{" + ft(n) + "}", true); } };
      }
      return { t: "nat", ans: a * k, q: function () { return fill(u("dOf"), { a: a, b: b, n: n }); },
        s: function () { return tex(ft(n) + ":" + b + "=" + k + "\\qquad " + k + "\\cdot " + a + "=\\boxed{" + ft(a * k) + "}", true); } };
    },
    pct: function () {
      if (Math.random() < .3) {
        var p0 = pick([5, 10, 20, 25, 30, 40, 50, 60, 75, 80, 15, 35, 45, 12, 8]), f = rat(p0, 100);
        return { t: "frac", irr: true, ans: f, q: function () { return fill(u("dPctF"), { p: p0 }); }, s: function () { return tex(p0 + "\\,\\%=" + frac(p0, 100) + "=\\boxed{" + fr(f) + "}", true); } };
      }
      var p = pick([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90]), n = rint(2, 40) * 20, v = p * n / 100;
      return { t: "nat", ans: v, q: function () { return fill(u("dPct"), { p: p, n: fh(n) }); }, s: function () { return tex(frac(p + "\\cdot " + ft(n), 100) + "=" + frac(ft(p * n), 100) + "=\\boxed{" + ft(v) + "}", true); } };
    },
    simp: function () {
      var f = randFr(12), k = rint(2, 12), a = f.n * k, b = f.d * k;
      return { t: "frac", irr: true, ans: f, q: function () { return fill(u("dSimp"), { a: a, b: b }); },
        s: function () { return tex("\\text{" + (lang === "en" ? "gcd" : "MCD") + "}(" + a + "," + b + ")=" + k + "\\qquad " + frac(a, b) + "=" + frac(a + ":" + k, b + ":" + k) + "=\\boxed{" + fr(f) + "}", true); } };
    },
    x: function () {
      var f = randFr(12), k = rint(2, 9), pos = rint(0, 3), v = [f.n, f.d, f.n * k, f.d * k], ans = v[pos], sh = v.slice();
      sh[pos] = "x";
      return { t: "nat", ans: ans, q: function () { return u("dX") + " $" + frac(sh[0], sh[1]) + "=" + frac(sh[2], sh[3]) + "$"; },
        s: function () { return tex(frac(v[0], v[1]) + "=" + frac(v[2], v[3]) + "\\qquad x=\\boxed{" + ans + "}", true) + hint(tex(v[0] + "\\cdot " + v[3] + "=" + v[1] + "\\cdot " + v[2] + "=" + (v[0] * v[3]))); } };
    },
    cmp: function () {
      var f, g;
      do { f = { n: rint(1, 15), d: rint(2, 12) }; g = Math.random() < .2 ? { n: f.n * 2, d: f.d * 2 } : { n: rint(1, 15), d: rint(2, 12) }; } while (f.n === g.n && f.d === g.d);
      var c = rcmp(f, g), ans = c < 0 ? "<" : c > 0 ? ">" : "=", m = lcm(f.d, g.d);
      return { t: "sym", ans: ans, q: function () { return u("dCmp") + " $" + frac(f.n, f.d) + "\\ \\square\\ " + frac(g.n, g.d) + "$"; },
        s: function () { return tex(frac(f.n * m / f.d, m) + "\\ \\boxed{" + (ans === "<" ? "<" : ans === ">" ? ">" : "=") + "}\\ " + frac(g.n * m / g.d, m), true); } };
    },
    sum: function () {
      var f, g, op, r;
      do { f = randFr(10); g = randFr(10); op = Math.random() < .5 ? "+" : "-"; if (op === "-" && rcmp(f, g) < 0) { var t0 = f; f = g; g = t0; } r = op === "+" ? radd(f, g) : rsub(f, g); } while (f.d === g.d && Math.random() < .6 || !r.n);
      return { t: "frac", irr: true, ans: r, q: function () { return u("dCalc") + " $" + fr(f) + (op === "+" ? "+" : "-") + fr(g) + "$"; },
        s: function () { return opSteps(f.n, f.d, g.n, g.d, op).s.join(""); } };
    },
    mul: function () {
      var f = { n: rint(1, 12), d: rint(2, 12) }, g = { n: rint(1, 12), d: rint(2, 12) }, op = Math.random() < .5 ? "·" : ":", r = op === "·" ? rmul(f, g) : rdiv(f, g);
      return { t: "frac", irr: true, ans: r, q: function () { return u("dCalc") + " $" + frac(f.n, f.d) + (op === "·" ? "\\cdot " : ":") + frac(g.n, g.d) + "$"; },
        s: function () { return opSteps(f.n, f.d, g.n, g.d, op).s.join(""); } };
    },
    comb: function () {
      var a = randFr(6), b = randFr(6), c = randFr(6), kind = rint(0, 3), e, r;
      var A = a.n + "/" + a.d, B = b.n + "/" + b.d, C = c.n + "/" + c.d;
      if (kind === 0) e = A + "+" + B + "·" + C;
      else if (kind === 1) e = "(" + A + "+" + B + ")·" + C;
      else if (kind === 2) e = A + ":" + B + "-" + C;
      else e = "(" + A + "-" + B + "):" + C;
      r = run(e);
      if (!r.ok || r.v.n < 0 || r.v.d > 200) return GEN.comb();
      var t = tx(parseExpr(e), null, null, true);
      return { t: "frac", irr: true, ans: r.v, q: function () { return u("dCalc") + " $" + t + "$"; },
        s: function () { return rowsHTML(run(e)).join("") + tex("\\boxed{" + fr(r.v) + "}", true); } };
    }
  };
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (done) info.innerHTML = (res === 1 ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u(res === 2 ? "notIrr" : "wrong") + "</span>") + '<div class="dsol">' + q.s() + "</div>";
    }
    function check() {
      if (done) return;
      var raw = inp.value.trim(), good;
      if (q.t === "sym") {
        if (!/^[<>=]$/.test(raw)) { info.innerHTML = warn("sym"); return; }
        good = raw === q.ans ? 1 : 0;
      } else {
        var f = pfrac(raw);
        if (!f) { info.innerHTML = warn("write"); return; }
        var ans = q.t === "nat" ? { n: q.ans, d: 1 } : q.ans;
        good = rcmp(f, ans) === 0 ? 1 : 0;
        if (good && q.irr) { var g = rat(f.n, f.d); if (g.n !== f.n || g.d !== f.d) good = 2; }
      }
      done = true; tot++; res = good; if (good === 1) ok++;
      paint();
    }
    function fresh() { q = GEN[kind](); done = false; inp.value = ""; info.innerHTML = ""; paint(); }
    w.querySelector('[data-a="check"]').addEventListener("click", check);
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); inp.focus(); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }

  /* ---------- qüestionari ---------- */
  var QUIZ = [
    { q: { va: "En la fracció $\\frac{3}{8}$, què indica el 8?", es: "En la fracción $\\frac{3}{8}$, ¿qué indica el 8?", en: "In the fraction $\\frac{3}{8}$, what does the 8 tell us?" },
      o: [{ va: "Les parts que agafem", es: "Las partes que tomamos", en: "The parts we take" }, { va: "Les parts iguals en què dividim la unitat", es: "Las partes iguales en que dividimos la unidad", en: "The equal parts the whole is split into" },
        { va: "Les parts que sobren", es: "Las partes que sobran", en: "The parts left over" }, { va: "Les unitats senceres", es: "Las unidades enteras", en: "The number of wholes" }], a: 1,
      e: { va: "El 8 és el <b>denominador</b>: dividim la unitat en 8 parts iguals. El 3 (numerador) diu quantes n'agafem.", es: "El 8 es el <b>denominador</b>: dividimos la unidad en 8 partes iguales. El 3 (numerador) dice cuántas tomamos.", en: "8 is the <b>denominator</b>: the whole is split into 8 equal parts. The 3 (numerator) says how many we take." } },
    { q: { va: "Quina d'aquestes fraccions és <b>impròpia</b>?", es: "¿Cuál de estas fracciones es <b>impropia</b>?", en: "Which of these fractions is <b>improper</b>?" },
      o: [{ va: "$\\frac{4}{9}$" }, { va: "$\\frac{7}{7}$" }, { va: "$\\frac{9}{4}$" }, { va: "$\\frac{1}{2}$" }], a: 2,
      e: { va: "$\\frac{9}{4}$ té el numerador més gran que el denominador: és major que 1 ($\\frac{9}{4}=2+\\frac{1}{4}$).", es: "$\\frac{9}{4}$ tiene el numerador mayor que el denominador: es mayor que 1 ($\\frac{9}{4}=2+\\frac{1}{4}$).", en: "$\\frac{9}{4}$ has a numerator bigger than its denominator: it's more than 1 ($\\frac{9}{4}=2+\\frac{1}{4}$)." } },
    { q: { va: "$\\frac{3}{5}$ de $40=$", es: "$\\frac{3}{5}$ de $40=$", en: "$\\frac{3}{5}$ of $40=$" },
      o: [{ va: "$8$" }, { va: "$24$" }, { va: "$15$" }, { va: "$120$" }], a: 1,
      e: { va: "$40:5=8$ i $8\\cdot3=24$.", es: "$40:5=8$ y $8\\cdot3=24$.", en: "$40:5=8$ and $8\\cdot3=24$." } },
    { q: { va: "El $25\\,\\%$ de $80$ és…", es: "El $25\\,\\%$ de $80$ es…", en: "$25\\%$ of $80$ is…" },
      o: [{ va: "$25$" }, { va: "$40$" }, { va: "$20$" }, { va: "$8$" }], a: 2,
      e: { va: "$25\\,\\%=\\frac{1}{4}$: la quarta part de 80 és 20.", es: "$25\\,\\%=\\frac{1}{4}$: la cuarta parte de 80 es 20.", en: "$25\\%=\\frac{1}{4}$: a quarter of 80 is 20." } },
    { q: { va: "Quin percentatge representa $\\frac{3}{5}$?", es: "¿Qué porcentaje representa $\\frac{3}{5}$?", en: "What percentage is $\\frac{3}{5}$?" },
      o: [{ va: "$35\\,\\%$" }, { va: "$60\\,\\%$" }, { va: "$30\\,\\%$" }, { va: "$53\\,\\%$" }], a: 1,
      e: { va: "$\\frac{3}{5}=\\frac{60}{100}=60\\,\\%$.", es: "$\\frac{3}{5}=\\frac{60}{100}=60\\,\\%$.", en: "$\\frac{3}{5}=\\frac{60}{100}=60\\%$." } },
    { q: { va: "Quina fracció <b>no</b> és equivalent a $\\frac{2}{3}$?", es: "¿Qué fracción <b>no</b> es equivalente a $\\frac{2}{3}$?", en: "Which fraction is <b>not</b> equivalent to $\\frac{2}{3}$?" },
      o: [{ va: "$\\frac{4}{6}$" }, { va: "$\\frac{10}{15}$" }, { va: "$\\frac{3}{4}$" }, { va: "$\\frac{20}{30}$" }], a: 2,
      e: { va: "Sumar 1 dalt i baix no dona una equivalent: cal <b>multiplicar</b> o <b>dividir</b> pel mateix nombre.", es: "Sumar 1 arriba y abajo no da una equivalente: hay que <b>multiplicar</b> o <b>dividir</b> por el mismo número.", en: "Adding 1 to top and bottom doesn't give an equivalent fraction: you must <b>multiply</b> or <b>divide</b> by the same number." } },
    { q: { va: "La fracció irreductible de $\\frac{36}{48}$ és…", es: "La fracción irreducible de $\\frac{36}{48}$ es…", en: "$\\frac{36}{48}$ in its simplest form is…" },
      o: [{ va: "$\\frac{18}{24}$" }, { va: "$\\frac{6}{8}$" }, { va: "$\\frac{3}{4}$" }, { va: "$\\frac{4}{3}$" }], a: 2,
      e: { va: "$\\text{MCD}(36,48)=12$: $\\frac{36:12}{48:12}=\\frac{3}{4}$. Les altres dues també són equivalents, però encara es poden simplificar.", es: "$\\text{MCD}(36,48)=12$: $\\frac{36:12}{48:12}=\\frac{3}{4}$. Las otras dos también son equivalentes, pero aún se pueden simplificar.", en: "$\\text{gcd}(36,48)=12$: $\\frac{36:12}{48:12}=\\frac{3}{4}$. The other two are equivalent too, but can still be simplified." } },
    { q: { va: "Són equivalents $\\frac{6}{15}$ i $\\frac{26}{34}$?", es: "¿Son equivalentes $\\frac{6}{15}$ y $\\frac{26}{34}$?", en: "Are $\\frac{6}{15}$ and $\\frac{26}{34}$ equivalent?" },
      o: [{ va: "Sí", es: "Sí", en: "Yes" }, { va: "No", es: "No", en: "No" }], a: 1,
      e: { va: "Productes creuats: $6\\cdot34=204$ i $15\\cdot26=390$. Són diferents.", es: "Productos cruzados: $6\\cdot34=204$ y $15\\cdot26=390$. Son distintos.", en: "Cross products: $6\\cdot34=204$ and $15\\cdot26=390$. They are different." } },
    { q: { va: "Si $\\frac{3}{14}=\\frac{x}{42}$, quant val $x$?", es: "Si $\\frac{3}{14}=\\frac{x}{42}$, ¿cuánto vale $x$?", en: "If $\\frac{3}{14}=\\frac{x}{42}$, what is $x$?" },
      o: [{ va: "$3$" }, { va: "$9$" }, { va: "$31$" }, { va: "$14$" }], a: 1,
      e: { va: "$42=14\\cdot3$, així que $x=3\\cdot3=9$.", es: "$42=14\\cdot3$, así que $x=3\\cdot3=9$.", en: "$42=14\\cdot3$, so $x=3\\cdot3=9$." } },
    { q: { va: "Reduïm $\\frac{1}{6}$ i $\\frac{3}{8}$ a comú denominador. Quin és el denominador més xicotet possible?", es: "Reducimos $\\frac{1}{6}$ y $\\frac{3}{8}$ a común denominador. ¿Cuál es el menor denominador posible?", en: "We give $\\frac{1}{6}$ and $\\frac{3}{8}$ a common denominator. What is the smallest one possible?" },
      o: [{ va: "$14$" }, { va: "$48$" }, { va: "$24$" }, { va: "$2$" }], a: 2,
      e: { va: "És el mcm: $\\text{mcm}(6,8)=24$. Amb 48 també es pot, però no és el més xicotet.", es: "Es el mcm: $\\text{mcm}(6,8)=24$. Con 48 también se puede, pero no es el menor.", en: "It's the lcm: $\\text{lcm}(6,8)=24$. 48 also works, but it isn't the smallest." } },
    { q: { va: "Quina és la fracció més gran?", es: "¿Cuál es la fracción mayor?", en: "Which fraction is the largest?" },
      o: [{ va: "$\\frac{3}{4}$" }, { va: "$\\frac{3}{5}$" }, { va: "$\\frac{3}{7}$" }, { va: "$\\frac{3}{10}$" }], a: 0,
      e: { va: "Amb el mateix numerador, és més gran la que té el denominador més xicotet: les parts són més grans.", es: "Con el mismo numerador, es mayor la que tiene el denominador más pequeño: las partes son más grandes.", en: "With the same numerator, the one with the smallest denominator is biggest: its parts are bigger." } },
    { q: { va: "$\\frac{1}{2}+\\frac{1}{3}=$", es: "$\\frac{1}{2}+\\frac{1}{3}=$", en: "$\\frac{1}{2}+\\frac{1}{3}=$" },
      o: [{ va: "$\\frac{2}{5}$" }, { va: "$\\frac{5}{6}$" }, { va: "$\\frac{2}{6}$" }, { va: "$\\frac{1}{5}$" }], a: 1,
      e: { va: "$\\frac{3}{6}+\\frac{2}{6}=\\frac{5}{6}$. <b>Mai</b> sumem numeradors i denominadors per separat!", es: "$\\frac{3}{6}+\\frac{2}{6}=\\frac{5}{6}$. ¡<b>Nunca</b> sumamos numeradores y denominadores por separado!", en: "$\\frac{3}{6}+\\frac{2}{6}=\\frac{5}{6}$. <b>Never</b> add numerators and denominators separately!" } },
    { q: { va: "$\\frac{6}{4}\\cdot\\frac{2}{5}=$", es: "$\\frac{6}{4}\\cdot\\frac{2}{5}=$", en: "$\\frac{6}{4}\\cdot\\frac{2}{5}=$" },
      o: [{ va: "$\\frac{3}{5}$" }, { va: "$\\frac{8}{9}$" }, { va: "$\\frac{30}{8}$" }, { va: "$\\frac{15}{4}$" }], a: 0,
      e: { va: "$\\frac{6\\cdot2}{4\\cdot5}=\\frac{12}{20}=\\frac{3}{5}$.", es: "$\\frac{6\\cdot2}{4\\cdot5}=\\frac{12}{20}=\\frac{3}{5}$.", en: "$\\frac{6\\cdot2}{4\\cdot5}=\\frac{12}{20}=\\frac{3}{5}$." } },
    { q: { va: "La inversa de $\\frac{4}{13}$ és…", es: "La inversa de $\\frac{4}{13}$ es…", en: "The reciprocal of $\\frac{4}{13}$ is…" },
      o: [{ va: "$-\\frac{4}{13}$" }, { va: "$\\frac{13}{4}$" }, { va: "$\\frac{8}{26}$" }, { va: "$1$" }], a: 1,
      e: { va: "Girem la fracció: $\\frac{4}{13}\\cdot\\frac{13}{4}=1$.", es: "Damos la vuelta a la fracción: $\\frac{4}{13}\\cdot\\frac{13}{4}=1$.", en: "Flip the fraction: $\\frac{4}{13}\\cdot\\frac{13}{4}=1$." } },
    { q: { va: "$\\frac{4}{3}:\\frac{5}{6}=$", es: "$\\frac{4}{3}:\\frac{5}{6}=$", en: "$\\frac{4}{3}:\\frac{5}{6}=$" },
      o: [{ va: "$\\frac{20}{18}$" }, { va: "$\\frac{8}{5}$" }, { va: "$\\frac{10}{9}$" }, { va: "$\\frac{5}{8}$" }], a: 1,
      e: { va: "Productes creuats: $\\frac{4\\cdot6}{3\\cdot5}=\\frac{24}{15}=\\frac{8}{5}$.", es: "Productos cruzados: $\\frac{4\\cdot6}{3\\cdot5}=\\frac{24}{15}=\\frac{8}{5}$.", en: "Cross-multiply: $\\frac{4\\cdot6}{3\\cdot5}=\\frac{24}{15}=\\frac{8}{5}$." } },
    { q: { va: "En $\\frac{1}{2}+\\frac{1}{2}\\cdot\\frac{2}{3}$, què fem primer?", es: "En $\\frac{1}{2}+\\frac{1}{2}\\cdot\\frac{2}{3}$, ¿qué hacemos primero?", en: "In $\\frac{1}{2}+\\frac{1}{2}\\cdot\\frac{2}{3}$, what do we do first?" },
      o: [{ va: "La suma", es: "La suma", en: "The addition" }, { va: "La multiplicació", es: "La multiplicación", en: "The multiplication" }, { va: "Igual, dona el mateix", es: "Da igual, sale lo mismo", en: "It doesn't matter" }], a: 1,
      e: { va: "Les multiplicacions i divisions van abans que les sumes i restes: $\\frac{1}{2}+\\frac{1}{3}=\\frac{5}{6}$.", es: "Las multiplicaciones y divisiones van antes que las sumas y restas: $\\frac{1}{2}+\\frac{1}{3}=\\frac{5}{6}$.", en: "Multiplication and division come before addition and subtraction: $\\frac{1}{2}+\\frac{1}{3}=\\frac{5}{6}$." } },
    { q: { va: "D'un bidó de 60 L gastem $\\frac{1}{2}$ i després $\\frac{1}{3}$ <b>del que queda</b>. Quants litres queden?", es: "De un bidón de 60 L gastamos $\\frac{1}{2}$ y después $\\frac{1}{3}$ <b>de lo que queda</b>. ¿Cuántos litros quedan?", en: "From a 60 L drum we use $\\frac{1}{2}$ and then $\\frac{1}{3}$ <b>of what is left</b>. How many litres are left?" },
      o: [{ va: "$10$ L" }, { va: "$20$ L" }, { va: "$30$ L" }, { va: "$40$ L" }], a: 1,
      e: { va: "Queden 30 L; $\\frac{1}{3}$ de 30 és 10; $30-10=20$ L.", es: "Quedan 30 L; $\\frac{1}{3}$ de 30 es 10; $30-10=20$ L.", en: "30 L are left; $\\frac{1}{3}$ of 30 is 10; $30-10=20$ L." } }
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

  var TITLES = { va: "Fraccions · FentMates", es: "Fracciones · FentMates", en: "Fractions · FentMates" };
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
    wPart(); wOf(); wPct(); wEq(); wCheck(); wCd(); wCmp();
    document.querySelectorAll(".w-ops").forEach(wOps); document.querySelectorAll(".w-hier").forEach(wHier); wRest();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
