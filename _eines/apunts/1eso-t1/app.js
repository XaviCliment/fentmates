(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u1-done", NSEC = 9;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", write: "Escriu un nombre natural.",
      natBad: "Escriu un nombre natural (només xifres) de fins a 9 xifres.",
      ord: ["unitats", "desenes", "centenes", "unitats de miler", "desenes de miler", "centenes de miler", "unitats de milió", "desenes de milió", "centenes de milió"],
      ab: ["U", "D", "C", "UM", "DM", "CM", "UMi", "DMi", "CMi"],
      read: "Es llig:", decomp: "Descomposició:", digitVal: "La xifra <b>{d}</b> està en el lloc de les <b>{o}</b>: val <b>{v}</b>.", tapDigit: "Toca una xifra de la taula per a veure quant val.",
      err: "Error", look: "La xifra següent (la de les {o}) és un <b>{d}</b>.", up: "Com que és 5 o més, sumem 1 a les {o2} i posem zeros darrere.", keep: "Com que és menor que 5, les {o2} es queden igual i posem zeros darrere.",
      truncDo: "Canviem per zeros totes les xifres que hi ha a la dreta de les {o2}.", nearer: "El nombre arrodonit és el més pròxim a {n}.",
      oTo: ["", "a les desenes", "a les centenes", "a les unitats de miler", "a les desenes de miler", "a les centenes de miler", "a les unitats de milió"],
      divZero: "No es pot dividir entre 0.", exact: "Exacta", inexact: "Entera", type: "Tipus", q: "Quocient", r: "Residu", proof: "Prova:",
      grp: "Repartim {D} en {d} grups iguals: cada grup en té <b>{q}</b> i en sobren <b>{r}</b>.", grpBig: "(El dibuix només es fa si el dividend és com a molt 120 i el divisor com a molt 12.)", rLess: "El residu sempre és menor que el divisor: {r} < {d}.", group: "grup", left: "sobren",
      hParse: "No entenc l'expressió. Usa xifres, + − · : ^ √ i parèntesis ( ) [ ].", hNeg: "{a} − {b}: amb nombres naturals no podem restar un nombre més gran d'un altre més xicotet.",
      hDiv: "{a} : {b} no és exacta. Ací volem que totes les divisions siguen exactes.", hDiv0: "No es pot dividir entre 0.", hSq: "√{a} no és exacta.", hBig: "El resultat és massa gran.",
      kinds: { pow: "Potència", sq: "Arrel", mul: "Multiplicació", div: "Divisió", add: "Suma", sub: "Resta" }, inPar: "dins del parèntesi", result: "Resultat:", already: "Ja és un nombre: no hi ha res a calcular.",
      ctx: {
        bus: { tot: "Persones", g: "Places per autobús", ans: "Calen <b>{x} autobusos</b>.", why: "Amb {q} autobusos es queden {r} persones a terra: necessitem un autobús més, encara que no vaja ple.", whyEx: "Tots els autobusos van plens." },
        box: { tot: "Ous", g: "Ous per caixa", ans: "Es poden omplir <b>{x} caixes</b>.", why: "Els {r} ous que sobren no omplen una caixa: no la comptem.", whyEx: "No sobra cap ou." },
        share: { tot: "Caramels", g: "Xiquets", ans: "Cada xiquet rep <b>{q} caramels</b> i en sobren <b>{r}</b>.", why: "El quocient és el que rep cadascú i el residu, el que sobra.", whyEx: "No en sobra cap: el repartiment és exacte." }
      },
      powRead: "Es llig: «{a} elevat a {n}»", powSq: "Es llig: «{a} al quadrat»", powCb: "Es llig: «{a} al cub»",
      powGrid: "{a}² = un quadrat de {a} × {a} = {v} caselles", powCube: "{a}³ = {a} capes de {a} × {a} = {v} cubets", powNo: "Amb exponents més grans ja no ho podem dibuixar: les potències creixen molt de pressa!",
      powCubeBig: "Per a dibuixar el cub, tria una base de 6 com a molt.", powOne: "{a}¹ = {a}: només hi ha un factor.", powZeroB: "0 multiplicat per ell mateix sempre dona 0.", powOneB: "1 multiplicat per ell mateix sempre dona 1.", layer: "capa",
      tenNo: "Aquest nombre no acaba en zero: no es pot abreujar amb una potència de 10.", tenZ: "Comptem els zeros del final: n'hi ha <b>{z}</b>, per tant, ×10<sup>{z}</sup>.", tenAlso: "També és correcte (però no tan abreujat):",
      tenPoly: "Cada xifra es multiplica per la potència de 10 del seu lloc. Els termes amb xifra 0 es poden ometre.",
      pBadQ: "Per a usar aquesta propietat amb nombres naturals, l'exponent del dividend (m) ha de ser major o igual que el del divisor (n).", pBadD: "Per a obtindre un nombre natural, {a} ha de ser múltiple de {b}.",
      pCheck: "Comprovació:", pBig: "(el nombre és massa gran per a calcular-lo ací)", pZero: "Tot nombre (diferent de 0) dividit entre ell mateix dona 1. Per això {a}⁰ = 1.", pZeroBad: "La base ha de ser diferent de 0.",
      sqEx: "Arrel exacta", sqInt: "Arrel entera", sqTiles: "Amb <b>{n}</b> rajoles fem un quadrat de <b>{b} × {b}</b> ({bb} rajoles)", sqLeft: " i en sobren <b>{r}</b> (el residu).", sqNone: " i no en sobra cap: {n} és un quadrat perfecte.", sqNeed: "Per al quadrat de {b1} × {b1} en faltarien {f}.", sqR: "residu",
      dRound: "Arrodoneix {n} {o}.", dTrunc: "Trunca {n} {o}.", dComb: "Calcula:", dPow: "Calcula:", dTenN: "Quin nombre és?", dTenE: "Completa l'exponent:", dProps: "Completa:", dSq: "Calcula l'arrel quadrada (exacta o entera) de",
      rMul: "Mateixa base: es deixa la base i se sumen els exponents.", rDiv: "Mateixa base: es deixa la base i es resten els exponents.", rPow: "Potència d'una potència: es multipliquen els exponents.", rSame: "Mateix exponent: es multipliquen les bases i es deixa l'exponent.", rZero: "Tota potència d'exponent 0 (amb base diferent de 0) val 1.",
      sqSol: "Com que {b}² = {bb} i {b1}² = {bb1}, l'arrel entera és {b} i el residu, {n} − {bb} = {r}." },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", write: "Escribe un número natural.",
      natBad: "Escribe un número natural (solo cifras) de hasta 9 cifras.",
      ord: ["unidades", "decenas", "centenas", "unidades de millar", "decenas de millar", "centenas de millar", "unidades de millón", "decenas de millón", "centenas de millón"],
      ab: ["U", "D", "C", "UM", "DM", "CM", "UMi", "DMi", "CMi"],
      read: "Se lee:", decomp: "Descomposición:", digitVal: "La cifra <b>{d}</b> está en el lugar de las <b>{o}</b>: vale <b>{v}</b>.", tapDigit: "Toca una cifra de la tabla para ver cuánto vale.",
      err: "Error", look: "La cifra siguiente (la de las {o}) es un <b>{d}</b>.", up: "Como es 5 o más, sumamos 1 a las {o2} y ponemos ceros detrás.", keep: "Como es menor que 5, las {o2} se quedan igual y ponemos ceros detrás.",
      truncDo: "Cambiamos por ceros todas las cifras que hay a la derecha de las {o2}.", nearer: "El número redondeado es el más próximo a {n}.",
      oTo: ["", "a las decenas", "a las centenas", "a las unidades de millar", "a las decenas de millar", "a las centenas de millar", "a las unidades de millón"],
      divZero: "No se puede dividir entre 0.", exact: "Exacta", inexact: "Entera", type: "Tipo", q: "Cociente", r: "Resto", proof: "Prueba:",
      grp: "Repartimos {D} en {d} grupos iguales: cada grupo tiene <b>{q}</b> y sobran <b>{r}</b>.", grpBig: "(El dibujo solo se hace si el dividendo es como mucho 120 y el divisor como mucho 12.)", rLess: "El resto siempre es menor que el divisor: {r} < {d}.", group: "grupo", left: "sobran",
      hParse: "No entiendo la expresión. Usa cifras, + − · : ^ √ y paréntesis ( ) [ ].", hNeg: "{a} − {b}: con números naturales no podemos restar un número mayor de otro más pequeño.",
      hDiv: "{a} : {b} no es exacta. Aquí queremos que todas las divisiones sean exactas.", hDiv0: "No se puede dividir entre 0.", hSq: "√{a} no es exacta.", hBig: "El resultado es demasiado grande.",
      kinds: { pow: "Potencia", sq: "Raíz", mul: "Multiplicación", div: "División", add: "Suma", sub: "Resta" }, inPar: "dentro del paréntesis", result: "Resultado:", already: "Ya es un número: no hay nada que calcular.",
      ctx: {
        bus: { tot: "Personas", g: "Plazas por autobús", ans: "Hacen falta <b>{x} autobuses</b>.", why: "Con {q} autobuses se quedan {r} personas en tierra: necesitamos un autobús más, aunque no vaya lleno.", whyEx: "Todos los autobuses van llenos." },
        box: { tot: "Huevos", g: "Huevos por caja", ans: "Se pueden llenar <b>{x} cajas</b>.", why: "Los {r} huevos que sobran no llenan una caja: no la contamos.", whyEx: "No sobra ningún huevo." },
        share: { tot: "Caramelos", g: "Niños", ans: "Cada niño recibe <b>{q} caramelos</b> y sobran <b>{r}</b>.", why: "El cociente es lo que recibe cada uno y el resto, lo que sobra.", whyEx: "No sobra ninguno: el reparto es exacto." }
      },
      powRead: "Se lee: «{a} elevado a {n}»", powSq: "Se lee: «{a} al cuadrado»", powCb: "Se lee: «{a} al cubo»",
      powGrid: "{a}² = un cuadrado de {a} × {a} = {v} casillas", powCube: "{a}³ = {a} capas de {a} × {a} = {v} cubitos", powNo: "Con exponentes más grandes ya no lo podemos dibujar: ¡las potencias crecen muy deprisa!",
      powCubeBig: "Para dibujar el cubo, elige una base de 6 como mucho.", powOne: "{a}¹ = {a}: solo hay un factor.", powZeroB: "0 multiplicado por sí mismo siempre da 0.", powOneB: "1 multiplicado por sí mismo siempre da 1.", layer: "capa",
      tenNo: "Este número no acaba en cero: no se puede abreviar con una potencia de 10.", tenZ: "Contamos los ceros del final: hay <b>{z}</b>, por tanto, ×10<sup>{z}</sup>.", tenAlso: "También es correcto (pero no tan abreviado):",
      tenPoly: "Cada cifra se multiplica por la potencia de 10 de su lugar. Los términos con cifra 0 se pueden omitir.",
      pBadQ: "Para usar esta propiedad con números naturales, el exponente del dividendo (m) debe ser mayor o igual que el del divisor (n).", pBadD: "Para obtener un número natural, {a} debe ser múltiplo de {b}.",
      pCheck: "Comprobación:", pBig: "(el número es demasiado grande para calcularlo aquí)", pZero: "Todo número (distinto de 0) dividido entre sí mismo da 1. Por eso {a}⁰ = 1.", pZeroBad: "La base debe ser distinta de 0.",
      sqEx: "Raíz exacta", sqInt: "Raíz entera", sqTiles: "Con <b>{n}</b> baldosas hacemos un cuadrado de <b>{b} × {b}</b> ({bb} baldosas)", sqLeft: " y sobran <b>{r}</b> (el resto).", sqNone: " y no sobra ninguna: {n} es un cuadrado perfecto.", sqNeed: "Para el cuadrado de {b1} × {b1} faltarían {f}.", sqR: "resto",
      dRound: "Redondea {n} {o}.", dTrunc: "Trunca {n} {o}.", dComb: "Calcula:", dPow: "Calcula:", dTenN: "¿Qué número es?", dTenE: "Completa el exponente:", dProps: "Completa:", dSq: "Calcula la raíz cuadrada (exacta o entera) de",
      rMul: "Misma base: se deja la base y se suman los exponentes.", rDiv: "Misma base: se deja la base y se restan los exponentes.", rPow: "Potencia de una potencia: se multiplican los exponentes.", rSame: "Mismo exponente: se multiplican las bases y se deja el exponente.", rZero: "Toda potencia de exponente 0 (con base distinta de 0) vale 1.",
      sqSol: "Como {b}² = {bb} y {b1}² = {bb1}, la raíz entera es {b} y el resto, {n} − {bb} = {r}." },
    en: { next: "Next step", all: "Show all", reset: "Hide steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Toggle light and dark mode", write: "Type a whole number.",
      natBad: "Type a whole number (digits only) with up to 9 digits.",
      ord: ["units", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions", "ten millions", "hundred millions"],
      ab: ["U", "T", "H", "Th", "TTh", "HTh", "M", "TM", "HM"],
      read: "In words:", decomp: "Expanded form:", digitVal: "The digit <b>{d}</b> is in the <b>{o}</b> place: it is worth <b>{v}</b>.", tapDigit: "Tap a digit in the table to see what it is worth.",
      err: "Error", look: "The next digit (the {o} digit) is <b>{d}</b>.", up: "It's 5 or more, so we add 1 to the {o2} and put zeros after it.", keep: "It's less than 5, so the {o2} stay the same and we put zeros after it.",
      truncDo: "Replace every digit to the right of the {o2} with a zero.", nearer: "The rounded number is the one closest to {n}.",
      oTo: ["", "to the tens", "to the hundreds", "to the thousands", "to the ten thousands", "to the hundred thousands", "to the millions"],
      divZero: "You can't divide by 0.", exact: "Exact", inexact: "With remainder", type: "Type", q: "Quotient", r: "Remainder", proof: "Check:",
      grp: "We share {D} into {d} equal groups: each group gets <b>{q}</b> and <b>{r}</b> are left over.", grpBig: "(The picture is only drawn when the dividend is at most 120 and the divisor at most 12.)", rLess: "The remainder is always less than the divisor: {r} < {d}.", group: "group", left: "left over",
      hParse: "I can't read that expression. Use digits, + − · : ^ √ and brackets ( ) [ ].", hNeg: "{a} − {b}: with natural numbers we can't take a bigger number away from a smaller one.",
      hDiv: "{a} : {b} is not exact. Here we want every division to be exact.", hDiv0: "You can't divide by 0.", hSq: "√{a} is not exact.", hBig: "The result is too big.",
      kinds: { pow: "Power", sq: "Root", mul: "Multiplication", div: "Division", add: "Addition", sub: "Subtraction" }, inPar: "inside the brackets", result: "Result:", already: "It's already a number: nothing to work out.",
      ctx: {
        bus: { tot: "People", g: "Seats per coach", ans: "We need <b>{x} coaches</b>.", why: "With {q} coaches, {r} people would be left behind: we need one more coach, even if it isn't full.", whyEx: "Every coach is full." },
        box: { tot: "Eggs", g: "Eggs per box", ans: "We can fill <b>{x} boxes</b>.", why: "The {r} eggs left over don't fill a box, so we don't count it.", whyEx: "No eggs are left over." },
        share: { tot: "Sweets", g: "Children", ans: "Each child gets <b>{q} sweets</b> and <b>{r}</b> are left over.", why: "The quotient is what each one gets and the remainder is what's left.", whyEx: "None are left: it shares out exactly." }
      },
      powRead: "In words: “{a} to the power of {n}”", powSq: "In words: “{a} squared”", powCb: "In words: “{a} cubed”",
      powGrid: "{a}² = a {a} × {a} square = {v} cells", powCube: "{a}³ = {a} layers of {a} × {a} = {v} little cubes", powNo: "With bigger exponents we can't draw it any more: powers grow really fast!",
      powCubeBig: "To draw the cube, pick a base of 6 or less.", powOne: "{a}¹ = {a}: there's just one factor.", powZeroB: "0 times itself is always 0.", powOneB: "1 times itself is always 1.", layer: "layer",
      tenNo: "This number doesn't end in zero: it can't be shortened with a power of 10.", tenZ: "Count the zeros at the end: there are <b>{z}</b>, so ×10<sup>{z}</sup>.", tenAlso: "Also correct (but not as short):",
      tenPoly: "Each digit is multiplied by the power of 10 of its place. Terms with a 0 digit can be left out.",
      pBadQ: "To use this property with natural numbers, the exponent on top (m) must be greater than or equal to the one below (n).", pBadD: "To get a natural number, {a} must be a multiple of {b}.",
      pCheck: "Check:", pBig: "(the number is too big to work out here)", pZero: "Any number (other than 0) divided by itself is 1. That's why {a}⁰ = 1.", pZeroBad: "The base must not be 0.",
      sqEx: "Exact root", sqInt: "Whole-number root", sqTiles: "With <b>{n}</b> tiles we make a <b>{b} × {b}</b> square ({bb} tiles)", sqLeft: " and <b>{r}</b> are left over (the remainder).", sqNone: " and none are left over: {n} is a perfect square.", sqNeed: "For a {b1} × {b1} square we'd need {f} more.", sqR: "remainder",
      dRound: "Round {n} {o}.", dTrunc: "Truncate {n} {o}.", dComb: "Work out:", dPow: "Work out:", dTenN: "Which number is it?", dTenE: "Fill in the exponent:", dProps: "Fill in:", dSq: "Find the square root (exact or whole-number) of",
      rMul: "Same base: keep the base and add the exponents.", rDiv: "Same base: keep the base and subtract the exponents.", rPow: "Power of a power: multiply the exponents.", rSame: "Same exponent: multiply the bases and keep the exponent.", rZero: "Any power with exponent 0 (and base other than 0) is 1.",
      sqSol: "Since {b}² = {bb} and {b1}² = {bb1}, the whole-number root is {b} and the remainder is {n} − {bb} = {r}." }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var MACROS = { "\\dc": "\\htmlClass{dc}{{,}}", "\\tri": "\\htmlClass{lva}{\\text{#1}}\\htmlClass{les}{\\text{#2}}\\htmlClass{len}{\\text{#3}}" };
  var KOPT = { throwOnError: false, strict: "ignore", macros: MACROS, trust: function (c) { return c.command === "\\htmlClass"; } };
  function tex(s, display) {
    try { return window.katex.renderToString(s, { throwOnError: false, strict: "ignore", displayMode: !!display, macros: MACROS, trust: KOPT.trust }); } catch (e) { return s; }
  }
  function rtex(s) { return s.replace(/\$([^$]+)\$/g, function (_, m) { return tex(m); }); }
  function segBind(w, cb) {
    var bs = w.querySelectorAll(".seg button");
    bs.forEach(function (b) { b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); cb(b.dataset.k); }); });
  }

  /* ---------- nombres i format ---------- */
  function pnat(s) {
    s = String(s).trim().replace(/[\s  ]/g, "");
    if (/^\d{1,3}([.,]\d{3})+$/.test(s)) s = s.replace(/[.,]/g, "");
    if (!/^\d+$/.test(s)) return NaN;
    return parseInt(s, 10);
  }
  function fcore(x, th) {
    if (!isFinite(x)) return "—";
    var s = String(Math.round(x));
    if (s.length > 4) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, th);
    return s;
  }
  function fh(x) { return fcore(x, " "); }
  function ft(x) { return fcore(x, "\\,"); }
  function warn(k) { return '<span class="warn">' + u(k) + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function expand(a, n) {
    if (n <= 6) { var f = []; for (var i = 0; i < n; i++) f.push(a); return f.join("\\cdot "); }
    return "\\underbrace{" + a + "\\cdot " + a + "\\cdots " + a + "}_{" + n + "}";
  }

  /* ---------- nombres en lletres ---------- */
  var VA_U = ["zero", "u", "dos", "tres", "quatre", "cinc", "sis", "set", "huit", "nou", "deu", "onze", "dotze", "tretze", "catorze", "quinze", "setze", "dèsset", "dihuit", "dènou"];
  var VA_T = ["", "", "vint", "trenta", "quaranta", "cinquanta", "seixanta", "setanta", "huitanta", "noranta"];
  function va99(n) { if (n < 20) return VA_U[n]; var t = Math.floor(n / 10), x = n % 10; return x ? VA_T[t] + (t === 2 ? "-i-" : "-") + VA_U[x] : VA_T[t]; }
  function va999(n) { var h = Math.floor(n / 100), r = n % 100, s = h ? (h === 1 ? "cent" : VA_U[h] + "-cents") : ""; return r ? (s ? s + " " : "") + va99(r) : s; }
  function vaUn(s) { return s.replace(/(^|[ -])u$/, "$1un"); }
  function va6(n) { var k = Math.floor(n / 1000), r = n % 1000, s = k ? (k === 1 ? "mil" : vaUn(va999(k)) + " mil") : ""; return r ? (s ? s + " " : "") + va999(r) : s; }
  function vaW(n) { if (!n) return "zero"; var m = Math.floor(n / 1e6), r = n % 1e6, s = m ? (m === 1 ? "un milió" : vaUn(va6(m)) + " milions") : ""; return r ? (s ? s + " " : "") + va6(r) : s; }
  var ES_U = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve",
    "veinte", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"];
  var ES_T = ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"];
  var ES_H = ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"];
  function es99(n) { if (n < 30) return ES_U[n]; var t = Math.floor(n / 10), x = n % 10; return ES_T[t] + (x ? " y " + ES_U[x] : ""); }
  function es999(n) { if (n === 100) return "cien"; var h = Math.floor(n / 100), r = n % 100; return (h ? ES_H[h] : "") + (h && r ? " " : "") + (r ? es99(r) : ""); }
  function esUn(s) { return s.replace(/veintiuno$/, "veintiún").replace(/(^| )uno$/, "$1un"); }
  function es6(n) { var k = Math.floor(n / 1000), r = n % 1000, s = k ? (k === 1 ? "mil" : esUn(es999(k)) + " mil") : ""; return r ? (s ? s + " " : "") + es999(r) : s; }
  function esW(n) { if (!n) return "cero"; var m = Math.floor(n / 1e6), r = n % 1e6, s = m ? (m === 1 ? "un millón" : esUn(es6(m)) + " millones") : ""; return r ? (s ? s + " " : "") + es6(r) : s; }
  var EN_U = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
  var EN_T = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
  function en99(n) { if (n < 20) return EN_U[n]; var t = Math.floor(n / 10), x = n % 10; return EN_T[t] + (x ? "-" + EN_U[x] : ""); }
  function en999(n) { var h = Math.floor(n / 100), r = n % 100; return (h ? EN_U[h] + " hundred" : "") + (h && r ? " and " : "") + (r ? en99(r) : ""); }
  function enW(n) {
    if (!n) return "zero";
    var p = [], m = Math.floor(n / 1e6), k = Math.floor(n / 1000) % 1000, r = n % 1000;
    if (m) p.push(en999(m) + " million"); if (k) p.push(en999(k) + " thousand");
    if (r) p.push((p.length && r < 100 ? "and " : "") + en999(r));
    return p.join(" ");
  }
  function words(n) { return { va: vaW, es: esW, en: enW }[lang](n); }

  /* ---------- giny: valor posicional ---------- */
  function wPlace() {
    var w = document.getElementById("w-place"); if (!w) return;
    var inp = w.querySelector(".tin"), out = w.querySelector(".pv"), info = w.querySelector(".info"), sel = null;
    function render() {
      var n = pnat(inp.value);
      if (isNaN(n) || n > 999999999) { out.innerHTML = ""; info.innerHTML = warn("natBad"); return; }
      var s = String(n), L = s.length, cols = Math.max(L, 4), h = "", d = "", v = "";
      if (sel != null && sel >= L) sel = null;
      for (var i = cols - 1; i >= 0; i--) {
        var g = "pg" + Math.floor(i / 3), dig = i < L ? s.charAt(L - 1 - i) : "";
        h += '<th class="' + g + '" title="' + u("ord")[i] + '">' + u("ab")[i] + "</th>";
        d += '<td class="dg ' + g + (sel === i ? " on" : "") + '">' + (dig ? '<button type="button" data-i="' + i + '">' + dig + "</button>" : "") + "</td>";
        v += '<td class="vv">' + (dig ? fh(+dig * Math.pow(10, i)) : "") + "</td>";
      }
      out.innerHTML = '<table class="data pvt"><thead><tr>' + h + "</tr></thead><tbody><tr>" + d + "</tr><tr>" + v + "</tr></tbody></table>";
      out.querySelectorAll("button[data-i]").forEach(function (b) { b.addEventListener("click", function () { sel = +b.dataset.i; render(); }); });
      var t1 = [], t2 = [];
      for (var j = L - 1; j >= 0; j--) {
        var dj = +s.charAt(L - 1 - j);
        t1.push(dj + "\\,\\text{" + u("ab")[j] + "}");
        if (dj) t2.push(ft(dj * Math.pow(10, j)));
      }
      var msg = sel != null ? fill(u("digitVal"), { d: s.charAt(L - 1 - sel), o: u("ord")[sel], v: fh(+s.charAt(L - 1 - sel) * Math.pow(10, sel)) }) : '<span class="hint">' + u("tapDigit") + "</span>";
      info.innerHTML = "<div><b>" + u("read") + "</b> <em>" + words(n) + "</em></div><div><b>" + u("decomp") + "</b></div>" +
        tex(ft(n) + "=" + t1.join("+") + (t2.length > 1 ? "=" + t2.join("+") : ""), true) + "<div>" + msg + "</div>";
    }
    inp.addEventListener("input", function () { sel = null; render(); });
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.b; sel = null; render(); }); });
    onLang(render);
  }

  /* ---------- giny: aproximació ---------- */
  function digitsHTML(n, k) {
    var s = String(n), L = s.length, h = "";
    for (var i = L - 1; i >= 0; i--) {
      var c = i === k ? "o" : i === k - 1 ? "nx" : i < k - 1 ? "z" : "";
      h += '<span class="' + c + '">' + s.charAt(L - 1 - i) + "</span>";
      if (i % 3 === 0 && i > 0 && L > 4) h += '<span class="sp"></span>';
    }
    return '<div class="digits">' + h + "</div>";
  }
  function approx(n, k) {
    var p = Math.pow(10, k), lo = Math.floor(n / p) * p, nd = Math.floor(n / (p / 10)) % 10;
    return { p: p, lo: lo, hi: lo + p, nd: nd, r: nd >= 5 ? lo + p : lo };
  }
  function wRound() {
    var w = document.getElementById("w-round"); if (!w) return;
    var k = 2, inp = w.querySelector(".tin"), dg = w.querySelector(".dgw"), ch = w.querySelector(".chart"), info = w.querySelector(".info");
    var O = { t: w.querySelector('[data-o="t"]'), r: w.querySelector('[data-o="r"]') };
    function render() {
      var n = pnat(inp.value);
      if (isNaN(n) || n > 999999999) { info.innerHTML = warn("natBad"); dg.innerHTML = ch.innerHTML = O.t.innerHTML = O.r.innerHTML = ""; return; }
      var a = approx(n, k);
      dg.innerHTML = digitsHTML(n, k);
      O.t.innerHTML = tex(ft(a.lo), true) + '<div class="hint">' + u("err") + ": " + fh(n) + " − " + fh(a.lo) + " = " + fh(n - a.lo) + "</div>";
      O.r.innerHTML = tex(ft(a.r), true) + '<div class="hint">' + u("err") + ": " + (a.r >= n ? fh(a.r) + " − " + fh(n) + " = " + fh(a.r - n) : fh(n) + " − " + fh(a.r) + " = " + fh(n - a.r)) + "</div>";
      var X0 = 40, X1 = 580, x = function (v) { return X0 + (v - a.lo) / a.p * (X1 - X0); }, svg = "", mid = a.lo + a.p / 2;
      for (var i = 0; i <= 10; i++) { var xi = X0 + i * (X1 - X0) / 10; svg += '<line class="sv-grid" x1="' + xi + '" y1="52" x2="' + xi + '" y2="' + (i % 5 ? 60 : 66) + '"/>'; }
      svg += '<line class="sv-ax" x1="' + X0 + '" y1="56" x2="' + X1 + '" y2="56"/>';
      svg += '<text class="sv-t" x="' + X0 + '" y="84" text-anchor="middle">' + fh(a.lo) + '</text><text class="sv-t" x="' + X1 + '" y="84" text-anchor="middle">' + fh(a.hi) + '</text><text class="sv-t" x="' + x(mid) + '" y="84" text-anchor="middle">' + fh(mid) + "</text>";
      svg += '<line class="sv-mid" x1="' + x(mid) + '" y1="20" x2="' + x(mid) + '" y2="66"/>';
      var xn = x(n), xr = x(a.r);
      svg += '<path class="sv-arr" d="M' + xn + " 40 Q" + (xn + xr) / 2 + " 14 " + xr + ' 46"/><circle class="sv-rd" cx="' + xr + '" cy="56" r="7"/>';
      svg += '<circle class="sv-pt" cx="' + xn + '" cy="56" r="6"/><text class="sv-tb" x="' + Math.max(60, Math.min(560, xn)) + '" y="14" text-anchor="middle">' + fh(n) + "</text>";
      ch.innerHTML = '<svg viewBox="0 0 620 92" role="img" aria-label="recta">' + svg + "</svg>";
      info.innerHTML = '<div class="hint">✂ ' + fill(u("truncDo"), { o2: u("ord")[k] }) + "</div><div>⚖ " + fill(u("look"), { o: u("ord")[k - 1], d: a.nd }) + " " + fill(u(a.nd >= 5 ? "up" : "keep"), { o2: u("ord")[k] }) + '</div><div class="hint">' + fill(u("nearer"), { n: fh(n) }) + "</div>";
    }
    inp.addEventListener("input", render);
    segBind(w, function (v) { k = +v; render(); });
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.b; render(); }); });
    onLang(render);
  }

  /* ---------- giny: divisió ---------- */
  function wDiv() {
    var w = document.getElementById("w-div"); if (!w) return;
    var I = { D: w.querySelector('[data-k="D"]'), d: w.querySelector('[data-k="d"]') }, info = w.querySelector(".info"), dots = w.querySelector(".dots");
    var O = { q: w.querySelector('[data-o="q"]'), r: w.querySelector('[data-o="r"]'), t: w.querySelector('[data-o="t"]') };
    function render() {
      var D = pnat(I.D.value), d = pnat(I.d.value);
      if (isNaN(D) || isNaN(d) || D > 999999999 || d > 999999999) { info.innerHTML = warn("write"); dots.innerHTML = O.q.innerHTML = O.r.innerHTML = O.t.innerHTML = ""; return; }
      if (d === 0) { info.innerHTML = warn("divZero"); dots.innerHTML = O.q.innerHTML = O.r.innerHTML = O.t.innerHTML = ""; return; }
      var q = Math.floor(D / d), r = D % d;
      O.q.innerHTML = tex(ft(q), true); O.r.innerHTML = tex(ft(r), true); O.t.innerHTML = "<strong>" + u(r ? "inexact" : "exact") + "</strong>";
      var h = "";
      if (D <= 120 && d <= 12) {
        for (var g = 0; g < d; g++) { var row = ""; for (var i = 0; i < q; i++) row += "<i></i>"; h += '<div class="drow"><span class="dl">' + u("group") + " " + (g + 1) + "</span>" + row + "</div>"; }
        if (r) { var rr = ""; for (var j = 0; j < r; j++) rr += '<i class="x"></i>'; h += '<div class="drow"><span class="dl">' + u("left") + "</span>" + rr + "</div>"; }
        dots.innerHTML = h;
      } else dots.innerHTML = '<div class="hint">' + u("grpBig") + "</div>";
      info.innerHTML = tex("\\underbrace{" + ft(D) + "}_{D}=\\underbrace{" + ft(d) + "}_{d}\\cdot\\underbrace{" + ft(q) + "}_{q}+\\underbrace{" + ft(r) + "}_{r}", true) +
        "<div>" + u("proof") + " " + tex(ft(d) + "\\cdot" + ft(q) + "+" + ft(r) + "=" + ft(d * q) + "+" + ft(r) + "=" + ft(D)) + "</div>" +
        '<div class="hint">' + (D <= 120 && d <= 12 ? fill(u("grp"), { D: fh(D), d: fh(d), q: fh(q), r: fh(r) }) + " " : "") + fill(u("rLess"), { r: fh(r), d: fh(d) }) + "</div>";
    }
    [I.D, I.d].forEach(function (x) { x.addEventListener("input", render); });
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { var p = b.dataset.b.split(":"); I.D.value = p[0]; I.d.value = p[1]; render(); }); });
    onLang(render);
  }

  /* ---------- operacions combinades pas a pas ---------- */
  function tokenize(s) {
    s = s.replace(/[×xX*]/g, "·").replace(/[\/÷]/g, ":").replace(/[−–]/g, "-").replace(/\{/g, "[").replace(/\}/g, "]").replace(/[\s ]/g, "");
    var t = [], i = 0;
    while (i < s.length) {
      var c = s.charAt(i);
      if (/\d/.test(c)) { var m = s.slice(i).match(/^\d+/)[0]; t.push({ k: "n", v: parseInt(m, 10) }); i += m.length; continue; }
      if ("+-·:^√()[]".indexOf(c) >= 0) { t.push({ k: c }); i++; continue; }
      return null;
    }
    return t;
  }
  function parseExpr(s) {
    var t = tokenize(s), i = 0;
    if (!t || !t.length) return null;
    function peek() { return t[i] && t[i].k; }
    function expr() { var a = term(); while (peek() === "+" || peek() === "-") { var op = t[i++].k; a = { t: "b", op: op, l: a, r: term() }; } return a; }
    function term() {
      var a = fac();
      for (;;) {
        var p = peek();
        if (p === "·" || p === ":") { i++; a = { t: "b", op: p, l: a, r: fac() }; }
        else if (p === "(" || p === "[" || p === "√") a = { t: "b", op: "·", l: a, r: fac() };
        else return a;
      }
    }
    function fac() { var a = un(); if (peek() === "^") { i++; a = { t: "b", op: "^", l: a, r: fac() }; } return a; }
    function un() { if (peek() === "√") { i++; var e = un(); if (e.t === "p") e = e.e; return { t: "s", e: e }; } return prim(); }
    function prim() {
      var p = peek();
      if (p === "n") return { t: "n", v: t[i++].v };
      if (p === "(" || p === "[") { i++; var e = expr(), cl = p === "(" ? ")" : "]"; if (peek() !== cl) throw 0; i++; return e.t === "n" ? e : { t: "p", k: p, e: e }; }
      throw 0;
    }
    try { var r = expr(); return i === t.length ? r : null; } catch (e) { return null; }
  }
  function isN(x) { return x.t === "n"; }
  function first(x, pr) {
    if (x.t === "b") return first(x.l, pr) || (pr(x) ? x : null) || first(x.r, pr);
    return pr(x) ? x : null;
  }
  function grp(x) { return (x.t === "p" || x.t === "s") && !isN(x.e); }
  /* ordre: parèntesis (de dins cap a fora) → potències i arrels → · i : → + i − (sempre d'esquerra a dreta) */
  function target(x, inG) {
    var g = first(x, grp);
    if (g) return target(g.e, true);
    var y = first(x, function (z) { return (z.t === "b" && z.op === "^" && isN(z.l) && isN(z.r)) || (z.t === "s" && isN(z.e)); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "·" || z.op === ":") && isN(z.l) && isN(z.r); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "+" || z.op === "-") && isN(z.l) && isN(z.r); });
    return y ? { n: y, g: !!inG } : null;
  }
  function applyOp(y) {
    if (y.t === "s") { var a0 = y.e.v, b0 = Math.round(Math.sqrt(a0)); return b0 * b0 === a0 ? { v: b0, k: "sq" } : { err: fill(u("hSq"), { a: fh(a0) }) }; }
    var a = y.l.v, b = y.r.v;
    if (y.op === "+") return { v: a + b, k: "add" };
    if (y.op === "-") return a < b ? { err: fill(u("hNeg"), { a: fh(a), b: fh(b) }) } : { v: a - b, k: "sub" };
    if (y.op === "·") return { v: a * b, k: "mul" };
    if (y.op === ":") return !b ? { err: u("hDiv0") } : a % b ? { err: fill(u("hDiv"), { a: fh(a), b: fh(b) }) } : { v: a / b, k: "div" };
    return { v: Math.pow(a, b), k: "pow" };
  }
  function repl(x, tg, nv) {
    if (x === tg) return nv;
    if (x.t === "b") return { t: "b", op: x.op, l: repl(x.l, tg, nv), r: repl(x.r, tg, nv) };
    if (x.t === "p") { var e = repl(x.e, tg, nv); return isN(e) ? e : { t: "p", k: x.k, e: e }; }
    if (x.t === "s") return { t: "s", e: repl(x.e, tg, nv) };
    return x;
  }
  function tx(x, tg, val) {
    var s;
    if (x.t === "n") s = ft(x.v);
    else if (x.t === "p") s = x.k === "(" ? "\\left(" + tx(x.e, tg, val) + "\\right)" : "\\left[" + tx(x.e, tg, val) + "\\right]";
    else if (x.t === "s") s = "\\sqrt{" + tx(x.e, tg, val) + "}";
    else if (x.op === "^") s = "{" + tx(x.l, tg, val) + "}^{" + tx(x.r, tg, val) + "}";
    else s = tx(x.l, tg, val) + { "+": "+", "-": "-", "·": "\\cdot ", ":": ":" }[x.op] + tx(x.r, tg, val);
    return x === tg ? "\\underbrace{\\htmlClass{hl}{" + s + "}}_{\\htmlClass{hlv}{" + ft(val) + "}}" : s;
  }
  function run(s) {
    var tree = parseExpr(s), rows = [];
    if (!tree) return { err: u("hParse"), rows: rows };
    for (var guard = 0; guard < 60; guard++) {
      var tg = target(tree);
      if (!tg) break;
      var r = applyOp(tg.n);
      if (!r.err && r.v > 1e12) r = { err: u("hBig") };
      if (r.err) return { err: r.err, rows: rows, last: tx(tree) };
      rows.push({ t: tx(tree, tg.n, r.v), k: r.k, g: tg.g });
      tree = repl(tree, tg.n, { t: "n", v: r.v });
    }
    return { ok: true, v: tree.v, rows: rows, src: s };
  }
  function rowsHTML(res) {
    return res.rows.map(function (r, i) {
      return '<div class="hrow"><span class="hk">' + (i + 1) + " · " + u("kinds")[r.k] + (r.g ? " <small>(" + u("inPar") + ")</small>" : "") + "</span>" + tex(r.t) + "</div>";
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
      else info.innerHTML = end ? "<b>" + u("result") + "</b> " + tex("\\boxed{" + ft(res.v) + "}") : "";
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

  /* ---------- giny: què fem amb el residu? ---------- */
  function wRest() {
    var w = document.getElementById("w-rest"); if (!w) return;
    var ctx = "bus", I = { N: w.querySelector('[data-k="N"]'), g: w.querySelector('[data-k="g"]') }, info = w.querySelector(".info"), vis = w.querySelector(".bxs");
    var DEF = { bus: ["197", "55"], box: ["1350", "12"], share: ["250", "23"] };
    function render() {
      var C = u("ctx")[ctx];
      w.querySelector('[data-f="N"]').textContent = C.tot; w.querySelector('[data-f="g"]').textContent = C.g;
      var N = pnat(I.N.value), g = pnat(I.g.value);
      if (isNaN(N) || isNaN(g) || !g) { info.innerHTML = warn(isNaN(N) || isNaN(g) ? "write" : "divZero"); vis.innerHTML = ""; return; }
      var q = Math.floor(N / g), r = N % g, x = ctx === "bus" ? q + (r ? 1 : 0) : q, h = "";
      if (ctx === "share") {
        if (g <= 30) for (var k = 0; k < g; k++) h += '<span class="kid">🙂<b>' + fh(q) + "</b></span>";
        if (r) h += '<span class="kid left">🍬<b>+' + fh(r) + "</b></span>";
      } else if (x <= 40) {
        for (var i = 0; i < q; i++) h += '<span class="bx"><i style="width:100%"></i></span>';
        if (r) h += '<span class="bx ' + (ctx === "bus" ? "part" : "no") + '"><i style="width:' + (r / g * 100) + '%"></i></span>';
      }
      vis.innerHTML = h;
      info.innerHTML = tex(ft(N) + "=" + ft(g) + "\\cdot" + ft(q) + "+" + ft(r), true) + "<div>" + fill(C.ans, { x: fh(x), q: fh(q), r: fh(r) }) + '</div><div class="hint">' + fill(r ? C.why : C.whyEx, { q: fh(q), r: fh(r) }) + "</div>";
    }
    [I.N, I.g].forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, function (k) { ctx = k; I.N.value = DEF[k][0]; I.g.value = DEF[k][1]; render(); });
    onLang(render);
  }

  /* ---------- giny: potències ---------- */
  function cellGrid(a, cls) {
    var s = Math.min(22, Math.floor(260 / Math.max(a, 1))), h = "";
    for (var y = 0; y < a; y++) for (var x = 0; x < a; x++) h += '<rect class="' + cls + '" x="' + (x * s + 1) + '" y="' + (y * s + 1) + '" width="' + (s - 2) + '" height="' + (s - 2) + '" rx="2"/>';
    return '<svg viewBox="0 0 ' + (a * s + 2) + " " + (a * s + 2) + '" style="width:' + (a * s + 2) + 'px">' + h + "</svg>";
  }
  function wPow() {
    var w = document.getElementById("w-pow"); if (!w) return;
    var A = w.querySelector('[data-k="a"]'), N = w.querySelector('[data-k="n"]'), info = w.querySelector(".info"), vis = w.querySelector(".pvis"), ch = w.querySelector(".pchain");
    function render() {
      var a = +A.value, n = +N.value, v = Math.pow(a, n);
      w.querySelector('[data-v="a"]').textContent = a; w.querySelector('[data-v="n"]').textContent = n;
      var rd = n === 2 ? u("powSq") : n === 3 ? u("powCb") : u("powRead"), h = "";
      info.innerHTML = tex("\\underbrace{" + a + "}_{\\text{base}}{}^{\\overbrace{" + n + "}^{\\text{exp.}}}" + (n > 1 ? "=" + expand(a, n) : "") + "=\\boxed{" + ft(v) + "}", true) +
        "<div>" + fill(rd, { a: a, n: n }) + "</div>" + (a === 0 ? '<div class="hint">' + u("powZeroB") + "</div>" : a === 1 ? '<div class="hint">' + u("powOneB") + "</div>" : "");
      if (a > 0 && n === 1) h = '<div class="hint">' + fill(u("powOne"), { a: a }) + "</div>";
      else if (a > 0 && n === 2) h = cellGrid(a, "t-sq") + '<div class="hint">' + fill(u("powGrid"), { a: a, v: fh(v) }) + "</div>";
      else if (a > 0 && n === 3 && a <= 6) {
        for (var k = 0; k < a; k++) h += '<div class="layer">' + cellGrid(a, "t-cb").replace(/width:(\d+)px/, function (_, p) { return "width:" + Math.round(p * .55) + "px"; }) + '<span class="hint">' + u("layer") + " " + (k + 1) + "</span></div>";
        h = '<div class="layers">' + h + '</div><div class="hint">' + fill(u("powCube"), { a: a, v: fh(v) }) + "</div>";
      } else if (a > 0 && n === 3) h = '<div class="hint">' + u("powCubeBig") + "</div>";
      else if (a > 1) h = '<div class="hint">' + u("powNo") + "</div>";
      vis.innerHTML = h;
      var c = "";
      if (a > 1) for (var e = 1; e <= Math.max(n, 4); e++) c += '<span class="pc' + (e === n ? " on" : "") + '">' + tex(a + "^{" + e + "}=" + ft(Math.pow(a, e))) + "</span>";
      ch.innerHTML = c;
    }
    [A, N].forEach(function (x) { x.addEventListener("input", render); });
    onLang(render);
  }

  /* ---------- giny: potències de 10 ---------- */
  function polyTex(n, skip) {
    var s = String(n), L = s.length, t = [];
    for (var i = L - 1; i >= 0; i--) {
      var d = +s.charAt(L - 1 - i);
      if (skip && !d && L > 1) continue;
      t.push(i >= 2 ? d + "\\cdot10^{" + i + "}" : i === 1 ? d + "\\cdot10" : String(d));
    }
    return t.join("+");
  }
  function wTen() {
    var w = document.getElementById("w-ten"); if (!w) return;
    var mode = "abbr", inp = w.querySelector(".tin"), info = w.querySelector(".info");
    function render() {
      var n = pnat(inp.value);
      if (isNaN(n) || n > 999999999) { info.innerHTML = warn("natBad"); return; }
      if (mode === "abbr") {
        var z = 0, m = n; while (m && m % 10 === 0) { m /= 10; z++; }
        if (!z) { info.innerHTML = '<span class="warn">' + u("tenNo") + "</span>"; return; }
        var also = [];
        for (var k = z - 1; k >= Math.max(1, z - 2); k--) also.push(ft(n / Math.pow(10, k)) + "\\cdot10^{" + k + "}");
        info.innerHTML = tex(ft(n) + "=" + ft(m) + "\\cdot" + ft(Math.pow(10, z)) + "=\\boxed{" + ft(m) + "\\cdot10^{" + z + "}}", true) + "<div>" + fill(u("tenZ"), { z: z }) + "</div>" +
          (also.length ? '<div class="hint">' + u("tenAlso") + " " + tex(also.join("\\quad")) + "</div>" : "");
      } else {
        var full = polyTex(n, false), short = polyTex(n, true);
        info.innerHTML = tex(ft(n) + "=" + full + (short !== full ? "=" + short : ""), true) + '<div class="hint">' + u("tenPoly") + "</div>";
      }
    }
    inp.addEventListener("input", render);
    segBind(w, function (k) { mode = k; inp.value = k === "abbr" ? "45000000" : "30705"; render(); });
    w.querySelectorAll(".quick button").forEach(function (b) {
      b.addEventListener("click", function () {
        mode = b.dataset.m; w.querySelectorAll(".seg button").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.k === mode)); });
        inp.value = b.dataset.b; render();
      });
    });
    onLang(render);
  }

  /* ---------- giny: propietats de les potències ---------- */
  function wProps() {
    var w = document.getElementById("w-props"); if (!w) return;
    var mode = "mul", info = w.querySelector(".info"), I = {};
    ["a", "b", "m", "n"].forEach(function (k) { I[k] = w.querySelector('[data-k="' + k + '"]'); });
    var NEED = { mul: "amn", div: "amn", pow: "amn", same: "abn", quo: "abn", zero: "an" };
    function P(a, e) { return a + "^{" + e + "}"; }
    function num(v) { return v > 1e15 ? "\\text{" + u("pBig") + "}" : ft(v); }
    function render() {
      w.querySelectorAll("[data-f]").forEach(function (l) { l.hidden = NEED[mode].indexOf(l.dataset.f) < 0; });
      var a = Math.max(0, Math.min(12, +I.a.value || 0)), b = Math.max(1, Math.min(12, +I.b.value || 1)), m = Math.max(1, Math.min(6, +I.m.value || 1)), n = Math.max(1, Math.min(6, +I.n.value || 1)), s, c = "", h = "";
      if (mode === "mul") {
        s = P(a, m) + "\\cdot " + P(a, n) + "=\\underbrace{(" + expand(a, m) + ")}_{" + m + "}\\cdot\\underbrace{(" + expand(a, n) + ")}_{" + n + "}=" + P(a, m + "+" + n) + "=\\boxed{" + P(a, m + n) + "}";
        c = ft(Math.pow(a, m)) + "\\cdot" + ft(Math.pow(a, n)) + "=" + num(Math.pow(a, m + n));
      } else if (mode === "div") {
        if (m < n) { info.innerHTML = '<span class="warn">' + u("pBadQ") + "</span>"; return; }
        var top = [], bot = [];
        for (var i = 0; i < m; i++) top.push(i < n ? "\\cancel{" + a + "}" : a);
        for (var j = 0; j < n; j++) bot.push("\\cancel{" + a + "}");
        s = P(a, m) + ":" + P(a, n) + "=\\dfrac{" + top.join("\\cdot ") + "}{" + bot.join("\\cdot ") + "}=" + P(a, m + "-" + n) + "=\\boxed{" + P(a, m - n) + "}";
        c = a ? ft(Math.pow(a, m)) + ":" + ft(Math.pow(a, n)) + "=" + num(Math.pow(a, m - n)) : "";
        if (m === n && a) h = '<div class="hint">' + fill(u("pZero"), { a: a }) + "</div>";
      } else if (mode === "pow") {
        var f = [], ex = [];
        for (var k = 0; k < n; k++) { f.push(P(a, m)); ex.push(m); }
        s = "\\left(" + P(a, m) + "\\right)^{" + n + "}=\\underbrace{" + f.join("\\cdot ") + "}_{" + n + "}=" + P(a, ex.join("+")) + "=" + P(a, m + "\\cdot " + n) + "=\\boxed{" + P(a, m * n) + "}";
        c = ft(Math.pow(a, m)) + "^{" + n + "}=" + num(Math.pow(a, m * n));
      } else if (mode === "same") {
        var ab = [];
        for (var q = 0; q < n; q++) ab.push("(" + a + "\\cdot " + b + ")");
        s = P(a, n) + "\\cdot " + P(b, n) + "=(" + expand(a, n) + ")\\cdot(" + expand(b, n) + ")=" + ab.join("\\cdot ") + "=(" + a + "\\cdot " + b + ")^{" + n + "}=\\boxed{" + P(a * b, n) + "}";
        c = ft(Math.pow(a, n)) + "\\cdot" + ft(Math.pow(b, n)) + "=" + num(Math.pow(a * b, n));
      } else if (mode === "quo") {
        if (a % b) { info.innerHTML = '<span class="warn">' + fill(u("pBadD"), { a: a, b: b }) + "</span>"; return; }
        var fr = [];
        for (var z = 0; z < n; z++) fr.push("\\frac{" + a + "}{" + b + "}");
        s = P(a, n) + ":" + P(b, n) + "=\\dfrac{" + expand(a, n) + "}{" + expand(b, n) + "}=" + fr.join("\\cdot ") + "=(" + a + ":" + b + ")^{" + n + "}=\\boxed{" + P(a / b, n) + "}";
        c = ft(Math.pow(a, n)) + ":" + ft(Math.pow(b, n)) + "=" + num(Math.pow(a / b, n));
      } else {
        if (!a) { info.innerHTML = '<span class="warn">' + u("pZeroBad") + "</span>"; return; }
        s = P(a, n) + ":" + P(a, n) + "=" + P(a, n + "-" + n) + "=" + P(a, 0) + "\\qquad " + P(a, n) + ":" + P(a, n) + "=" + ft(Math.pow(a, n)) + ":" + ft(Math.pow(a, n)) + "=1\\qquad\\Rightarrow\\qquad\\boxed{" + P(a, 0) + "=1}";
        h = '<div class="hint">' + fill(u("pZero"), { a: a }) + "</div>";
      }
      info.innerHTML = tex(s, true) + (c ? "<div>" + u("pCheck") + " " + tex(c) + "</div>" : "") + h;
    }
    ["a", "b", "m", "n"].forEach(function (k) { I[k].addEventListener("input", render); });
    segBind(w, function (k) { mode = k; if (k === "quo") { I.a.value = 6; I.b.value = 3; } render(); });
    onLang(render);
  }

  /* ---------- giny: arrels quadrades ---------- */
  function wSqrt() {
    var w = document.getElementById("w-sqrt"); if (!w) return;
    var R = w.querySelector('input[type="range"]'), T = w.querySelector(".tin"), vis = w.querySelector(".tiles"), info = w.querySelector(".info");
    function render(src) {
      var n = src === "t" ? pnat(T.value) : +R.value;
      if (isNaN(n) || n < 1 || n > 400) { info.innerHTML = warn("write"); vis.innerHTML = ""; return; }
      if (src === "t") R.value = Math.min(n, +R.max); else T.value = n;
      var b = Math.floor(Math.sqrt(n)), r = n - b * b, s = Math.max(8, Math.min(24, Math.floor(300 / (b + 1)))), h = "", W = (b + 1) * s + 4;
      if (r) h += '<rect class="t-gh" x="2" y="2" width="' + ((b + 1) * s) + '" height="' + ((b + 1) * s) + '" rx="4"/>';
      for (var y = 0; y < b; y++) for (var x = 0; x < b; x++) h += '<rect class="t-sq" x="' + (x * s + 3) + '" y="' + (y * s + 3) + '" width="' + (s - 2) + '" height="' + (s - 2) + '" rx="2"/>';
      for (var k = 0; k < r; k++) { var cx = k < b ? b : k - b, cy = k < b ? k : b; h += '<rect class="t-ex" x="' + (cx * s + 3) + '" y="' + (cy * s + 3) + '" width="' + (s - 2) + '" height="' + (s - 2) + '" rx="2"/>'; }
      vis.innerHTML = '<svg viewBox="0 0 ' + W + " " + W + '" style="width:' + W + 'px">' + h + "</svg>";
      var b1 = b + 1;
      info.innerHTML = (r ? tex(b + "^2=" + ft(b * b) + "\\lt " + ft(n) + "\\lt " + ft(b1 * b1) + "=" + b1 + "^2", true) + "<div><b>" + u("sqInt") + ":</b> " + b + " &nbsp;·&nbsp; <b>" + u("sqR") + ":</b> " + r + " &nbsp;&nbsp; " + tex(ft(n) + "=" + b + "^2+" + r) + "</div>"
        : tex(b + "^2=" + ft(n) + "\\ \\Rightarrow\\ \\sqrt{" + ft(n) + "}=" + b, true) + "<div><b>" + u("sqEx") + "</b></div>") +
        '<div class="hint">' + fill(u("sqTiles"), { n: fh(n), b: b, bb: fh(b * b) }) + (r ? fill(u("sqLeft"), { r: r }) + " " + fill(u("sqNeed"), { b1: b1, f: b1 * b1 - n }) : fill(u("sqNone"), { n: fh(n) })) + "</div>";
    }
    R.addEventListener("input", function () { render("r"); });
    T.addEventListener("input", function () { render("t"); });
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { T.value = b.dataset.b; render("t"); }); });
    onLang(function () { render("t"); });
  }

  /* ---------- entrenadors ---------- */
  var COMB = [
    function () { return rint(2, 30) + "+" + rint(2, 9) + "·" + rint(2, 9); },
    function () { return rint(3, 9) + "·" + rint(3, 9) + "-" + rint(1, 9); },
    function () { return "(" + rint(2, 15) + "+" + rint(2, 15) + ")·" + rint(2, 6); },
    function () { var c = rint(2, 9); return rint(10, 40) + "-" + c * rint(2, 4) + ":" + c; },
    function () { return rint(2, 9) + "·" + rint(2, 9) + "+" + rint(2, 9) + "·" + rint(2, 9); },
    function () { return rint(30, 60) + "-" + rint(2, 4) + "·(" + rint(2, 6) + "+" + rint(1, 4) + ")"; },
    function () { var c = rint(2, 6); return c * rint(2, 9) + ":" + c + "+" + rint(2, 9) + "·" + rint(2, 5); },
    function () { return "(" + rint(10, 20) + "-" + rint(2, 9) + ")·(" + rint(1, 5) + "+" + rint(1, 5) + ")"; },
    function () { var c = rint(2, 5); return "(" + rint(2, 9) + "+" + rint(2, 9) + ")·" + c + "-" + rint(2, 9); }
  ];
  var GEN = {
    round: function () {
      var len = rint(4, 7), n = rint(Math.pow(10, len - 1), Math.pow(10, len) - 1), k = rint(1, Math.min(len - 1, 5)), tr = Math.random() < .3, a = approx(n, k);
      return { ans: tr ? a.lo : a.r,
        q: function () { return fill(u(tr ? "dTrunc" : "dRound"), { n: fh(n), o: u("oTo")[k] }); },
        s: function () { return digitsHTML(n, k) + (tr ? "<div>" + fill(u("truncDo"), { o2: u("ord")[k] }) + "</div>" : "<div>" + fill(u("look"), { o: u("ord")[k - 1], d: a.nd }) + " " + fill(u(a.nd >= 5 ? "up" : "keep"), { o2: u("ord")[k] }) + "</div>") + tex("\\boxed{" + ft(tr ? a.lo : a.r) + "}", true); } };
    },
    comb: function () {
      for (var t = 0; t < 100; t++) {
        var e = pick(COMB)(), r = run(e);
        if (r.ok && r.v <= 999) return { ans: r.v, q: function () { return u("dComb") + " $" + tx(parseExpr(e)) + "$"; }, s: function () { return rowsHTML(r).join("") + tex("\\boxed{" + ft(r.v) + "}", true); } };
      }
    },
    pow: function () {
      var a, n;
      do { a = rint(2, 10); n = rint(2, 4); } while (Math.pow(a, n) > 10000);
      var z = Math.random();
      if (z < .15) { a = 10; n = rint(2, 6); } else if (z < .25) { a = pick([0, 1]); n = rint(3, 9); }
      var v = Math.pow(a, n);
      return { ans: v, q: function () { return u("dPow") + " $" + a + "^{" + n + "}$"; }, s: function () { return tex(a + "^{" + n + "}=" + expand(a, n) + "=" + ft(v), true); } };
    },
    ten: function () {
      if (Math.random() < .5) {
        var e = rint(3, 7), m = pick([2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 25, 34, 45, 72, 306]), N = m * Math.pow(10, e);
        return { ans: e, q: function () { return u("dTenE") + " $" + ft(N) + "=" + m + "\\cdot10^{\\square}$"; },
          s: function () { return tex(ft(N) + "=" + m + "\\cdot" + ft(Math.pow(10, e)) + "=" + m + "\\cdot10^{" + e + "}", true) + "<div>" + fill(u("tenZ"), { z: e }) + "</div>"; } };
      }
      var len = rint(4, 7), M = 0;
      for (var i = len - 1; i >= 0; i--) M = M * 10 + (i === len - 1 ? rint(1, 9) : Math.random() < .4 ? 0 : rint(1, 9));
      return { ans: M, q: function () { return u("dTenN") + " $" + polyTex(M, true) + "$"; }, s: function () { return tex(polyTex(M, true) + "=" + ft(M), true); } };
    },
    props: function () {
      var a = rint(2, 9), m = rint(2, 8), n = rint(2, 6), t = rint(0, 5), Q, A, S;
      if (t === 0) { Q = a + "^{" + m + "}\\cdot" + a + "^{" + n + "}=" + a + "^{\\square}"; A = m + n; S = [u("rMul"), a + "^{" + m + "+" + n + "}=" + a + "^{" + A + "}"]; }
      else if (t === 1) { m = n + rint(1, 6); Q = a + "^{" + m + "}:" + a + "^{" + n + "}=" + a + "^{\\square}"; A = m - n; S = [u("rDiv"), a + "^{" + m + "-" + n + "}=" + a + "^{" + A + "}"]; }
      else if (t === 2) { m = rint(2, 5); n = rint(2, 4); Q = "\\left(" + a + "^{" + m + "}\\right)^{" + n + "}=" + a + "^{\\square}"; A = m * n; S = [u("rPow"), a + "^{" + m + "\\cdot " + n + "}=" + a + "^{" + A + "}"]; }
      else if (t === 3) { a = rint(2, 6); var b = rint(2, 5); Q = a + "^{" + n + "}\\cdot" + b + "^{" + n + "}=\\square^{" + n + "}"; A = a * b; S = [u("rSame"), "(" + a + "\\cdot " + b + ")^{" + n + "}=" + A + "^{" + n + "}"]; }
      else if (t === 4) { a = rint(2, 99); Q = a + "^{0}=\\square"; A = 1; S = [u("rZero"), a + "^{0}=1"]; }
      else { var p = rint(2, m + n - 1); Q = a + "^{" + m + "}\\cdot" + a + "^{" + n + "}:" + a + "^{" + p + "}=" + a + "^{\\square}"; A = m + n - p; S = [u("rMul") + " " + u("rDiv"), a + "^{" + m + "+" + n + "-" + p + "}=" + a + "^{" + A + "}"]; }
      return { ans: A, q: function () { return u("dProps") + " $" + Q + "$"; }, s: function () { return "<div>" + S[0] + "</div>" + tex(S[1], true); } };
    },
    sqrt: function () {
      var b = rint(2, 20), N = Math.random() < .5 ? b * b : b * b + rint(1, 2 * b);
      return { ans: b, q: function () { return u("dSq") + " $" + ft(N) + "$: $\\sqrt{" + ft(N) + "}$"; },
        s: function () {
          var r = N - b * b;
          return r ? tex(b + "^2=" + ft(b * b) + "\\lt " + ft(N) + "\\lt " + ft((b + 1) * (b + 1)) + "=" + (b + 1) + "^2", true) + "<div>" + fill(u("sqSol"), { b: b, bb: fh(b * b), b1: b + 1, bb1: fh((b + 1) * (b + 1)), n: fh(N), r: r }) + "</div>"
            : tex(b + "^2=" + ft(N) + "\\ \\Rightarrow\\ \\sqrt{" + ft(N) + "}=" + b, true) + "<div><b>" + u("sqEx") + "</b></div>";
        } };
    }
  };
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, good = false, ok = 0, tot = 0;
    var dq = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore");
    function paint() {
      dq.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (done) info.innerHTML = (good ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u("wrong") + "</span>") + '<div class="dsol">' + q.s() + "</div>";
    }
    function check() {
      if (done) return;
      var v = pnat(inp.value);
      if (isNaN(v)) { info.innerHTML = warn("write"); return; }
      done = true; tot++; good = v === q.ans; if (good) ok++;
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
    { q: { va: "Quin d'aquests nombres <b>no</b> és natural?", es: "¿Cuál de estos números <b>no</b> es natural?", en: "Which of these is <b>not</b> a natural number?" },
      o: [{ va: "$0$" }, { va: "$25$" }, { va: "$7\\,000\\,000$" }, { va: "$3\\dc5$" }], a: 3,
      e: { va: "Els naturals són 0, 1, 2, 3… i no tenen part decimal: $3\\dc5$ no ho és.", es: "Los naturales son 0, 1, 2, 3… y no tienen parte decimal: $3\\dc5$ no lo es.", en: "Natural numbers are 0, 1, 2, 3… with no decimal part: $3\\dc5$ isn't one." } },
    { q: { va: "En el nombre $52\\,806$, la xifra 2 val…", es: "En el número $52\\,806$, la cifra 2 vale…", en: "In the number $52\\,806$, the digit 2 is worth…" },
      o: [{ va: "$2$" }, { va: "$20$" }, { va: "$200$" }, { va: "$2000$" }], a: 3,
      e: { va: "Està en el lloc de les unitats de miler: val $2000$.", es: "Está en el lugar de las unidades de millar: vale $2000$.", en: "It's in the thousands place: it's worth $2000$." } },
    { q: { va: "Si arrodonim $6482$ a les centenes obtenim…", es: "Si redondeamos $6482$ a las centenas obtenemos…", en: "Rounding $6482$ to the hundreds gives…" },
      o: [{ va: "$6400$" }, { va: "$6500$" }, { va: "$6480$" }, { va: "$7000$" }], a: 1,
      e: { va: "La xifra de les desenes és 8 (≥ 5): sumem 1 a les centenes → $6500$.", es: "La cifra de las decenas es 8 (≥ 5): sumamos 1 a las centenas → $6500$.", en: "The tens digit is 8 (≥ 5): add 1 to the hundreds → $6500$." } },
    { q: { va: "I si el <b>truncam</b> a les centenes?", es: "¿Y si lo <b>truncamos</b> a las centenas?", en: "And if we <b>truncate</b> it to the hundreds?" },
      o: [{ va: "$6400$" }, { va: "$6500$" }, { va: "$6000$" }, { va: "$6480$" }], a: 0,
      e: { va: "Truncar és posar zeros després de les centenes: $6400$.", es: "Truncar es poner ceros después de las centenas: $6400$.", en: "Truncating means putting zeros after the hundreds: $6400$." } },
    { q: { va: "$3+4\\cdot5=$", es: "$3+4\\cdot5=$", en: "$3+4\\cdot5=$" },
      o: [{ va: "$35$" }, { va: "$23$" }, { va: "$27$" }, { va: "$60$" }], a: 1,
      e: { va: "Primer la multiplicació: $3+20=23$. (35 és l'error de sumar primer.)", es: "Primero la multiplicación: $3+20=23$. (35 es el error de sumar primero.)", en: "Multiplication first: $3+20=23$. (35 is the mistake of adding first.)" } },
    { q: { va: "En la divisió $47:6$, el quocient i el residu són…", es: "En la división $47:6$, el cociente y el resto son…", en: "In the division $47:6$, the quotient and remainder are…" },
      o: [{ va: "$q=7,\\ r=5$" }, { va: "$q=8,\\ r=1$" }, { va: "$q=6,\\ r=11$" }, { va: "$q=7,\\ r=6$" }], a: 0,
      e: { va: "$6\\cdot7+5=47$ i $5\\lt6$. (Amb $q=8$ ens passem: $6\\cdot8=48$.)", es: "$6\\cdot7+5=47$ y $5\\lt6$. (Con $q=8$ nos pasamos: $6\\cdot8=48$.)", en: "$6\\cdot7+5=47$ and $5\\lt6$. ($q=8$ is too much: $6\\cdot8=48$.)" } },
    { q: { va: "$20-(8-3)\\cdot2=$", es: "$20-(8-3)\\cdot2=$", en: "$20-(8-3)\\cdot2=$" },
      o: [{ va: "$10$" }, { va: "$26$" }, { va: "$30$" }, { va: "$2$" }], a: 0,
      e: { va: "Parèntesi: $20-5\\cdot2$; multiplicació: $20-10=10$.", es: "Paréntesis: $20-5\\cdot2$; multiplicación: $20-10=10$.", en: "Brackets: $20-5\\cdot2$; multiplication: $20-10=10$." } },
    { q: { va: "$2^5$ val…", es: "$2^5$ vale…", en: "$2^5$ equals…" },
      o: [{ va: "$10$" }, { va: "$25$" }, { va: "$32$" }, { va: "$7$" }], a: 2,
      e: { va: "$2\\cdot2\\cdot2\\cdot2\\cdot2=32$. (10 seria $2\\cdot5$: un error molt típic.)", es: "$2\\cdot2\\cdot2\\cdot2\\cdot2=32$. (10 sería $2\\cdot5$: un error muy típico.)", en: "$2\\cdot2\\cdot2\\cdot2\\cdot2=32$. (10 would be $2\\cdot5$: a very common mistake.)" } },
    { q: { va: "Quina és certa?", es: "¿Cuál es cierta?", en: "Which one is true?" },
      o: [{ va: "$2^3=3^2$" }, { va: "$2^3\\lt3^2$" }, { va: "$2^3\\gt3^2$" }, { va: "$2^3=6$" }], a: 1,
      e: { va: "$2^3=8$ i $3^2=9$, així que $8\\lt9$.", es: "$2^3=8$ y $3^2=9$, así que $8\\lt9$.", en: "$2^3=8$ and $3^2=9$, so $8\\lt9$." } },
    { q: { va: "$4\\,500\\,000$ escrit de forma abreujada és…", es: "$4\\,500\\,000$ escrito de forma abreviada es…", en: "$4\\,500\\,000$ written in short form is…" },
      o: [{ va: "$45\\cdot10^6$" }, { va: "$45\\cdot10^5$" }, { va: "$4\\cdot10^5$" }, { va: "$45^5$" }], a: 1,
      e: { va: "Acaba en 5 zeros: $45\\cdot10^5$.", es: "Acaba en 5 ceros: $45\\cdot10^5$.", en: "It ends in 5 zeros: $45\\cdot10^5$." } },
    { q: { va: "$3\\cdot10^4+5\\cdot10^2+7=$", es: "$3\\cdot10^4+5\\cdot10^2+7=$", en: "$3\\cdot10^4+5\\cdot10^2+7=$" },
      o: [{ va: "$3057$" }, { va: "$30\\,507$" }, { va: "$300\\,507$" }, { va: "$35\\,007$" }], a: 1,
      e: { va: "$30\\,000+500+7=30\\,507$ (no hi ha milers ni desenes: hi van zeros).", es: "$30\\,000+500+7=30\\,507$ (no hay millares ni decenas: van ceros).", en: "$30\\,000+500+7=30\\,507$ (no thousands or tens: those are zeros)." } },
    { q: { va: "$5^4\\cdot5^3=$", es: "$5^4\\cdot5^3=$", en: "$5^4\\cdot5^3=$" },
      o: [{ va: "$5^{12}$" }, { va: "$25^7$" }, { va: "$5^7$" }, { va: "$5^1$" }], a: 2,
      e: { va: "Mateixa base: se sumen els exponents, $4+3=7$.", es: "Misma base: se suman los exponentes, $4+3=7$.", en: "Same base: add the exponents, $4+3=7$." } },
    { q: { va: "$\\left(2^3\\right)^2=$", es: "$\\left(2^3\\right)^2=$", en: "$\\left(2^3\\right)^2=$" },
      o: [{ va: "$2^5$" }, { va: "$2^6$" }, { va: "$2^9$" }, { va: "$6^2$" }], a: 1,
      e: { va: "Potència d'una potència: es multipliquen els exponents, $3\\cdot2=6$.", es: "Potencia de una potencia: se multiplican los exponentes, $3\\cdot2=6$.", en: "Power of a power: multiply the exponents, $3\\cdot2=6$." } },
    { q: { va: "$7^0=$", es: "$7^0=$", en: "$7^0=$" },
      o: [{ va: "$0$" }, { va: "$1$" }, { va: "$7$" }, { va: "$70$" }], a: 1,
      e: { va: "Tota potència d'exponent 0 (amb base diferent de 0) val 1.", es: "Toda potencia de exponente 0 (con base distinta de 0) vale 1.", en: "Any power with exponent 0 (base other than 0) is 1." } },
    { q: { va: "L'arrel quadrada entera de 50 i el seu residu són…", es: "La raíz cuadrada entera de 50 y su resto son…", en: "The whole-number square root of 50 and its remainder are…" },
      o: [{ va: "$7$ i $1$", es: "$7$ y $1$", en: "$7$ and $1$" }, { va: "$7$ i $7$", es: "$7$ y $7$", en: "$7$ and $7$" }, { va: "$25$ i $0$", es: "$25$ y $0$", en: "$25$ and $0$" }, { va: "$8$ i $14$", es: "$8$ y $14$", en: "$8$ and $14$" }], a: 0,
      e: { va: "$7^2=49\\le50\\lt64=8^2$: arrel entera 7 i residu $50-49=1$.", es: "$7^2=49\\le50\\lt64=8^2$: raíz entera 7 y resto $50-49=1$.", en: "$7^2=49\\le50\\lt64=8^2$: root 7 and remainder $50-49=1$." } },
    { q: { va: "$\\sqrt{9+16}=$", es: "$\\sqrt{9+16}=$", en: "$\\sqrt{9+16}=$" },
      o: [{ va: "$7$" }, { va: "$5$" }, { va: "$25$" }, { va: "$12\\dc5$" }], a: 1,
      e: { va: "Primer el de dins: $\\sqrt{25}=5$. (7 seria $\\sqrt9+\\sqrt{16}$, i això <b>no</b> és el mateix!)", es: "Primero lo de dentro: $\\sqrt{25}=5$. (7 sería $\\sqrt9+\\sqrt{16}$, ¡y eso <b>no</b> es lo mismo!)", en: "Inside first: $\\sqrt{25}=5$. (7 would be $\\sqrt9+\\sqrt{16}$, which is <b>not</b> the same!)" } }
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

  var TITLES = { va: "Nombres naturals · FentMates", es: "Números naturales · FentMates", en: "Natural numbers · FentMates" };
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
    wPlace(); wRound(); wDiv(); document.querySelectorAll(".w-hier").forEach(wHier); wRest();
    wPow(); wTen(); wProps(); wSqrt(); document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
