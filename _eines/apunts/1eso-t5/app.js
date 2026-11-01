(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u5-done", NSEC = 10;


  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", notIrr: "És equivalent, però no és irreductible: simplifica-la!", sym: "Escriu <, > o =.",
      writeD: "Escriu un nombre (amb coma decimal, per exemple 3,25).", writeF: "Escriu una fracció, per exemple 7/20.",
      plBad: "Escriu un nombre decimal amb com a molt 6 xifres enteres i 3 decimals.", reads: "Es llig:", rdBoth: "{a} i {b}", decomp: "Descomposició:", asFrac: "Com a fracció decimal:",
      plZeros: "Els zeros finals no canvien el valor: {a} = {b}.",
      zBad: "Escriu un decimal menor que 1000 amb com a molt 3 decimals.", zLine: "Entre {a} i {b} dividim en 10 parts: anem de {n} en {n}.",
      rBad: "Escriu un nombre decimal (com a molt 6 decimals).", rNone: "{x} ja té com a molt les {n}: no cal aproximar.",
      rKeep: "Ens quedem fins a les {n}. La primera xifra que eliminem és {d}:", rUp: "com que és 5 o més, sumem 1 a l'última xifra.", rDown: "com que és menor que 5, l'última xifra es queda igual.",
      trunc: "Truncament", round: "Arrodoniment",
      cBad: "Escriu dos nombres decimals (com a molt 4 decimals).", cNeg: "Per a restar, el primer nombre ha de ser el més gran.", cBig: "Els nombres són massa llargs per a fer-ho en columna.",
      cMul: "Multipliquem com si no hi haguera comes: {a}.", cMulK: "Decimals dels factors: {a} + {b} = {k}. Separem {k} xifres decimals al resultat.",
      cPad: "Alineem les comes i completem amb zeros (en gris) perquè tinguen els mateixos decimals.", cAlign: "Alineem les comes: unitats davall d'unitats, dècimes davall de dècimes…",
      zBad2: "Escriu un nombre decimal (com a molt 6 decimals).", pRight: "la coma es mou {p} llocs a la dreta", pLeft: "la coma es mou {p} llocs a l'esquerra", pZeros: "Hem afegit {n} zero(s) perquè no hi havia prou xifres.",
      dZero: "No es pot dividir entre 0.", dBad: "Escriu dividend i divisor (com a molt 4 decimals).", dMove: "El divisor té decimals: multipliquem dividend i divisor per {p}. El quocient no canvia.",
      dComma: "Comencem els decimals: posem la coma al quocient.", dAddZ: "Afegim un 0:", rem: "residu", dExact: "La divisió és exacta.", dRem: "Residu: {r}.", check: "Comprovació:",
      dLess1: "Hem dividit entre un nombre menor que 1: el quocient és més gran que el dividend.",
      fdBadD: "Escriu un decimal exacte (com a molt 6 decimals).", fdNat: "És un nombre natural: no té part decimal.", fdD1: "Té {k} xifra(es) decimal(s): al denominador posem un 1 seguit de {z} zero(s).",
      fdSimp: "Simplifiquem dividint entre el MCD, que és {g}.", fdIrr: "Ja és irreductible.", fdBadF: "Escriu un numerador natural (fins a 99 999) i un denominador entre 1 i 999.",
      fdStart: "Comencem: {a}, residu {r}. Ara posem la coma i anem afegint zeros:", fdRep: "aquest residu ja ha eixit: es repeteix tot!",
      fdExact: "Arribem a residu 0: és un <b>decimal exacte</b>.", fdWhole: "La divisió és exacta: la fracció és un <b>nombre natural</b>.", fdLong: "El període és molt llarg: només en mostrem una part.",
      fdPure: "És un <b>decimal periòdic pur</b>.", fdMixed: "És un <b>decimal periòdic mixt</b>.", fdPer: "Període: {p}.", fdAnte: "Anteperíode: {a}.",
      fdWhy1: "La fracció irreductible és {f} i el seu denominador ({d}) només té els factors 2 i 5: per això el decimal és exacte.",
      fdWhy2: "La fracció irreductible és {f} i el seu denominador ({d}) té factors diferents de 2 i 5: per això el decimal és periòdic.",
      prBad: "Escriu nombres diferents de 0 (pots posar x en una casella).", prOneX: "Només pots posar una x.", prYes: "Els productes són iguals: <b>formen proporció</b>.", prNo: "Els productes són diferents: <b>no formen proporció</b>.",
      prCross: "El producte dels extrems és igual al producte dels mitjans:",
      r3Bad: "Escriu tres quantitats diferents de 0 (com a molt 3 decimals).", r3D: "Directa: si una magnitud es multiplica per un nombre, l'altra també (més → més).",
      r3I: "Inversa: si una magnitud es multiplica per un nombre, l'altra es divideix (més → menys). El producte es manté.", r3Unit: "Reducció a la unitat:", r3Rule: "Regla de tres:", r3Prod: "els productes de cada fila són iguals.",
      kBad: "Escriu quatre parelles de nombres diferents de 0.", kDir: "Tots els quocients y : x són iguals: és una relació de <b>proporcionalitat directa</b> amb constant {k}. Els punts estan en una recta que passa per l'origen.",
      kInv: "Tots els productes x · y són iguals: és una relació de <b>proporcionalitat inversa</b> amb constant {k}.", kNone: "Ni els quocients ni els productes són tots iguals: <b>no és proporcional</b>.",
      pcBad: "Escriu les dues dades que coneixes (percentatge fins a 1000).", pcTot: "El {p} del total són {a}. Dividim la part entre el percentatge en forma decimal:", total: "Total", part: "Part",
      pcOver: "Un percentatge major que 100 % vol dir més que el total.",
      vBad: "Escriu una quantitat i un percentatge (una disminució ha de ser menor que el 100 %).", vUp: "Augment del {p}: paguem el {r}. Índex de variació: {i}.", vDown: "Disminució del {p}: paguem el {r}. Índex de variació: {i}.",
      vM1: "Mètode 1:", vM2: "Mètode 2 (amb l'índex):", vRound: "Arrodonit a cèntims: {v}.", vInv: "Coneixem la quantitat final: dividim entre l'índex de variació.", vIni: "Inicial", vFin: "Final",
      dCmp: "Escriu <, > o =:", dRound: "Arrodoneix {x} a les {n}.", dCalc: "Calcula:", dToF: "Escriu {x} com a fracció irreductible.", dToD: "Escriu {f} en forma decimal.", dX: "Calcula x:",
      dPct: "Calcula el {p} % de {n}.", dPctW: "Quin percentatge representa {a} de {n}? (escriu només el nombre)", dPctT: "El {p} % d'una quantitat és {a}. Quina és la quantitat?",
      dVarU: "Un preu de {q} € puja un {p} %. Quin és el preu final?", dVarD: "Un preu de {q} € baixa un {p} %. Quin és el preu final?",
      dVarIu: "Després de pujar un {p} %, un preu és de {f} €. Quin era el preu inicial?", dVarId: "Després d'una rebaixa del {p} %, un preu és de {f} €. Quin era el preu inicial?" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", notIrr: "Es equivalente, pero no es irreducible: ¡simplifícala!", sym: "Escribe <, > o =.",
      writeD: "Escribe un número (con coma decimal, por ejemplo 3,25).", writeF: "Escribe una fracción, por ejemplo 7/20.",
      plBad: "Escribe un número decimal con como mucho 6 cifras enteras y 3 decimales.", reads: "Se lee:", rdBoth: "{a} y {b}", decomp: "Descomposición:", asFrac: "Como fracción decimal:",
      plZeros: "Los ceros finales no cambian el valor: {a} = {b}.",
      zBad: "Escribe un decimal menor que 1000 con como mucho 3 decimales.", zLine: "Entre {a} y {b} dividimos en 10 partes: vamos de {n} en {n}.",
      rBad: "Escribe un número decimal (como mucho 6 decimales).", rNone: "{x} ya tiene como mucho las {n}: no hace falta aproximar.",
      rKeep: "Nos quedamos hasta las {n}. La primera cifra que eliminamos es {d}:", rUp: "como es 5 o más, sumamos 1 a la última cifra.", rDown: "como es menor que 5, la última cifra se queda igual.",
      trunc: "Truncamiento", round: "Redondeo",
      cBad: "Escribe dos números decimales (como mucho 4 decimales).", cNeg: "Para restar, el primer número tiene que ser el mayor.", cBig: "Los números son demasiado largos para hacerlo en columna.",
      cMul: "Multiplicamos como si no hubiera comas: {a}.", cMulK: "Decimales de los factores: {a} + {b} = {k}. Separamos {k} cifras decimales en el resultado.",
      cPad: "Alineamos las comas y completamos con ceros (en gris) para que tengan los mismos decimales.", cAlign: "Alineamos las comas: unidades debajo de unidades, décimas debajo de décimas…",
      zBad2: "Escribe un número decimal (como mucho 6 decimales).", pRight: "la coma se mueve {p} lugares a la derecha", pLeft: "la coma se mueve {p} lugares a la izquierda", pZeros: "Hemos añadido {n} cero(s) porque no había suficientes cifras.",
      dZero: "No se puede dividir entre 0.", dBad: "Escribe dividendo y divisor (como mucho 4 decimales).", dMove: "El divisor tiene decimales: multiplicamos dividendo y divisor por {p}. El cociente no cambia.",
      dComma: "Empezamos los decimales: ponemos la coma en el cociente.", dAddZ: "Añadimos un 0:", rem: "resto", dExact: "La división es exacta.", dRem: "Resto: {r}.", check: "Comprobación:",
      dLess1: "Hemos dividido entre un número menor que 1: el cociente es mayor que el dividendo.",
      fdBadD: "Escribe un decimal exacto (como mucho 6 decimales).", fdNat: "Es un número natural: no tiene parte decimal.", fdD1: "Tiene {k} cifra(s) decimal(es): en el denominador ponemos un 1 seguido de {z} cero(s).",
      fdSimp: "Simplificamos dividiendo entre el MCD, que es {g}.", fdIrr: "Ya es irreducible.", fdBadF: "Escribe un numerador natural (hasta 99 999) y un denominador entre 1 y 999.",
      fdStart: "Empezamos: {a}, resto {r}. Ahora ponemos la coma y vamos añadiendo ceros:", fdRep: "este resto ya ha salido: ¡se repite todo!",
      fdExact: "Llegamos a resto 0: es un <b>decimal exacto</b>.", fdWhole: "La división es exacta: la fracción es un <b>número natural</b>.", fdLong: "El periodo es muy largo: solo mostramos una parte.",
      fdPure: "Es un <b>decimal periódico puro</b>.", fdMixed: "Es un <b>decimal periódico mixto</b>.", fdPer: "Periodo: {p}.", fdAnte: "Anteperiodo: {a}.",
      fdWhy1: "La fracción irreducible es {f} y su denominador ({d}) solo tiene los factores 2 y 5: por eso el decimal es exacto.",
      fdWhy2: "La fracción irreducible es {f} y su denominador ({d}) tiene factores distintos de 2 y 5: por eso el decimal es periódico.",
      prBad: "Escribe números distintos de 0 (puedes poner x en una casilla).", prOneX: "Solo puedes poner una x.", prYes: "Los productos son iguales: <b>forman proporción</b>.", prNo: "Los productos son distintos: <b>no forman proporción</b>.",
      prCross: "El producto de los extremos es igual al producto de los medios:",
      r3Bad: "Escribe tres cantidades distintas de 0 (como mucho 3 decimales).", r3D: "Directa: si una magnitud se multiplica por un número, la otra también (más → más).",
      r3I: "Inversa: si una magnitud se multiplica por un número, la otra se divide (más → menos). El producto se mantiene.", r3Unit: "Reducción a la unidad:", r3Rule: "Regla de tres:", r3Prod: "los productos de cada fila son iguales.",
      kBad: "Escribe cuatro parejas de números distintos de 0.", kDir: "Todos los cocientes y : x son iguales: es una relación de <b>proporcionalidad directa</b> con constante {k}. Los puntos están en una recta que pasa por el origen.",
      kInv: "Todos los productos x · y son iguales: es una relación de <b>proporcionalidad inversa</b> con constante {k}.", kNone: "Ni los cocientes ni los productos son todos iguales: <b>no es proporcional</b>.",
      pcBad: "Escribe los dos datos que conoces (porcentaje hasta 1000).", pcTot: "El {p} del total son {a}. Dividimos la parte entre el porcentaje en forma decimal:", total: "Total", part: "Parte",
      pcOver: "Un porcentaje mayor que 100 % quiere decir más que el total.",
      vBad: "Escribe una cantidad y un porcentaje (una disminución tiene que ser menor que el 100 %).", vUp: "Aumento del {p}: pagamos el {r}. Índice de variación: {i}.", vDown: "Disminución del {p}: pagamos el {r}. Índice de variación: {i}.",
      vM1: "Método 1:", vM2: "Método 2 (con el índice):", vRound: "Redondeado a céntimos: {v}.", vInv: "Conocemos la cantidad final: dividimos entre el índice de variación.", vIni: "Inicial", vFin: "Final",
      dCmp: "Escribe <, > o =:", dRound: "Redondea {x} a las {n}.", dCalc: "Calcula:", dToF: "Escribe {x} como fracción irreducible.", dToD: "Escribe {f} en forma decimal.", dX: "Calcula x:",
      dPct: "Calcula el {p} % de {n}.", dPctW: "¿Qué porcentaje representa {a} de {n}? (escribe solo el número)", dPctT: "El {p} % de una cantidad es {a}. ¿Cuál es la cantidad?",
      dVarU: "Un precio de {q} € sube un {p} %. ¿Cuál es el precio final?", dVarD: "Un precio de {q} € baja un {p} %. ¿Cuál es el precio final?",
      dVarIu: "Después de subir un {p} %, un precio es de {f} €. ¿Cuál era el precio inicial?", dVarId: "Después de una rebaja del {p} %, un precio es de {f} €. ¿Cuál era el precio inicial?" },
    en: { next: "Next step", all: "Show all", reset: "Hide steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Toggle light and dark mode", notIrr: "It's equivalent, but not in its simplest form: simplify it!", sym: "Type <, > or =.",
      writeD: "Type a number (you can use a decimal comma or point, e.g. 3,25).", writeF: "Type a fraction, e.g. 7/20.",
      plBad: "Type a decimal with at most 6 whole-number digits and 3 decimals.", reads: "We read it:", rdBoth: "{a} and {b}", decomp: "Expanded form:", asFrac: "As a decimal fraction:",
      plZeros: "Trailing zeros don't change the value: {a} = {b}.",
      zBad: "Type a decimal less than 1000 with at most 3 decimals.", zLine: "Between {a} and {b} we split into 10 parts: we count in {n}.",
      rBad: "Type a decimal number (at most 6 decimals).", rNone: "{x} already has no more than {n}: nothing to approximate.",
      rKeep: "We keep up to the {n}. The first digit we remove is {d}:", rUp: "since it's 5 or more, add 1 to the last digit.", rDown: "since it's less than 5, the last digit stays the same.",
      trunc: "Truncated", round: "Rounded",
      cBad: "Type two decimals (at most 4 decimals).", cNeg: "To subtract, the first number must be the larger one.", cBig: "The numbers are too long to do in columns.",
      cMul: "Multiply as if there were no commas: {a}.", cMulK: "Decimals in the factors: {a} + {b} = {k}. Mark off {k} decimal places in the answer.",
      cPad: "Line up the commas and fill in zeros (in grey) so both have the same number of decimals.", cAlign: "Line up the commas: units under units, tenths under tenths…",
      zBad2: "Type a decimal number (at most 6 decimals).", pRight: "the comma moves {p} places to the right", pLeft: "the comma moves {p} places to the left", pZeros: "We added {n} zero(s) because there weren't enough digits.",
      dZero: "You can't divide by 0.", dBad: "Type a dividend and a divisor (at most 4 decimals).", dMove: "The divisor has decimals: multiply dividend and divisor by {p}. The quotient doesn't change.",
      dComma: "Starting the decimals: put the comma in the quotient.", dAddZ: "Add a 0:", rem: "remainder", dExact: "The division is exact.", dRem: "Remainder: {r}.", check: "Check:",
      dLess1: "We divided by a number less than 1: the quotient is bigger than the dividend.",
      fdBadD: "Type a terminating decimal (at most 6 decimals).", fdNat: "It's a whole number: it has no decimal part.", fdD1: "It has {k} decimal place(s): the denominator is a 1 followed by {z} zero(s).",
      fdSimp: "Simplify by dividing by the gcd, which is {g}.", fdIrr: "It's already in its simplest form.", fdBadF: "Type a whole-number numerator (up to 99,999) and a denominator from 1 to 999.",
      fdStart: "Start: {a}, remainder {r}. Now put the comma and keep adding zeros:", fdRep: "we've had this remainder before: everything repeats!",
      fdExact: "We reach remainder 0: it's a <b>terminating decimal</b>.", fdWhole: "The division is exact: the fraction is a <b>whole number</b>.", fdLong: "The period is very long: we only show part of it.",
      fdPure: "It's a <b>purely recurring decimal</b>.", fdMixed: "It's a <b>mixed recurring decimal</b>.", fdPer: "Period: {p}.", fdAnte: "Non-repeating part: {a}.",
      fdWhy1: "In simplest form it's {f}, and its denominator ({d}) only has the factors 2 and 5: that's why the decimal terminates.",
      fdWhy2: "In simplest form it's {f}, and its denominator ({d}) has factors other than 2 and 5: that's why the decimal recurs.",
      prBad: "Type numbers other than 0 (you can put x in one box).", prOneX: "You can only put one x.", prYes: "The products are equal: <b>it's a proportion</b>.", prNo: "The products are different: <b>it's not a proportion</b>.",
      prCross: "The product of the extremes equals the product of the means:",
      r3Bad: "Type three amounts other than 0 (at most 3 decimals).", r3D: "Direct: when one quantity is multiplied by a number, so is the other (more → more).",
      r3I: "Inverse: when one quantity is multiplied by a number, the other is divided by it (more → less). The product stays the same.", r3Unit: "Unit method:", r3Rule: "Rule of three:", r3Prod: "the products of each row are equal.",
      kBad: "Type four pairs of numbers other than 0.", kDir: "All the quotients y : x are equal: it's a <b>direct proportion</b> with constant {k}. The points lie on a line through the origin.",
      kInv: "All the products x · y are equal: it's an <b>inverse proportion</b> with constant {k}.", kNone: "Neither the quotients nor the products are all equal: it's <b>not proportional</b>.",
      pcBad: "Type the two values you know (percentage up to 1000).", pcTot: "{p} of the whole is {a}. Divide the part by the percentage as a decimal:", total: "Whole", part: "Part",
      pcOver: "A percentage over 100% means more than the whole.",
      vBad: "Type an amount and a percentage (a decrease must be less than 100%).", vUp: "{p} increase: we pay {r}. Multiplier: {i}.", vDown: "{p} decrease: we pay {r}. Multiplier: {i}.",
      vM1: "Method 1:", vM2: "Method 2 (with the multiplier):", vRound: "Rounded to the cent: {v}.", vInv: "We know the final amount: divide by the multiplier.", vIni: "Starting", vFin: "Final",
      dCmp: "Type <, > or =:", dRound: "Round {x} to the {n}.", dCalc: "Work out:", dToF: "Write {x} as a fraction in simplest form.", dToD: "Write {f} as a decimal.", dX: "Find x:",
      dPct: "Work out {p}% of {n}.", dPctW: "What percentage of {n} is {a}? (type just the number)", dPctT: "{p}% of an amount is {a}. What is the amount?",
      dVarU: "A price of {q} € goes up {p}%. What is the final price?", dVarD: "A price of {q} € goes down {p}%. What is the final price?",
      dVarIu: "After a {p}% rise, a price is {f} €. What was the starting price?", dVarId: "After {p}% off, a price is {f} €. What was the starting price?" }
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

  /* ---------- nombres decimals exactes: valor = i / 10^k ---------- */
  function p10(k) { return Math.pow(10, k); }
  function D(i, k, keep) { k = k || 0; if (!keep) while (k > 0 && i % 10 === 0) { i /= 10; k--; } return { i: i, k: k }; }
  function norm(x) { return D(x.i, x.k); }
  /* llegeix «3,25», «3.25», «0,035», «1.234,5»; keep = conserva els zeros finals */
  function pdec(s, keep) {
    s = String(s).trim().replace(/[\s  %€]/g, "");
    if (/^\d{1,3}(\.\d{3})+,\d+$/.test(s)) s = s.replace(/\./g, "");
    s = s.replace(",", ".");
    if (!/^(\d+(\.\d*)?|\.\d+)$/.test(s)) return null;
    var p = s.split("."), f = p[1] || "", ip = p[0] || "0";
    if (f.length > 8 || (ip.replace(/^0+/, "") + f).length > 15) return null;
    return D(parseInt(ip + f, 10), f.length, keep);
  }
  function dal(a, b) { var k = Math.max(a.k, b.k); return [a.i * p10(k - a.k), b.i * p10(k - b.k), k]; }
  function dadd(a, b) { var t = dal(a, b); return D(t[0] + t[1], t[2]); }
  function dsub(a, b) { var t = dal(a, b); return D(t[0] - t[1], t[2]); }
  function dmul(a, b) { return D(a.i * b.i, a.k + b.k); }
  function dcmp(a, b) { var t = dal(a, b); return t[0] - t[1]; }
  function dnum(x) { return x.i / p10(x.k); }
  function N(n) { return D(n, 0); }
  function digs(x, minK) {
    var k = Math.max(x.k, minK || 0), s = String(Math.abs(x.i) * p10(k - x.k));
    while (s.length <= k) s = "0" + s;
    return [s.slice(0, s.length - k), s.slice(s.length - k)];
  }
  function dstr(x, minK) { var p = digs(x, minK), ip = p[0]; if (ip.length > 4) ip = ip.replace(/\B(?=(\d{3})+(?!\d))/g, " "); return (x.i < 0 ? "−" : "") + ip + (p[1] ? "," + p[1] : ""); }
  function dt(x, minK) { var p = digs(x, minK), ip = p[0]; if (ip.length > 4) ip = ip.replace(/\B(?=(\d{3})+(?!\d))/g, "\\,"); return (x.i < 0 ? "-" : "") + ip + (p[1] ? "{,}" + p[1] : ""); }
  function truncD(x, k) { return x.k <= k ? x : D(Math.floor(x.i / p10(x.k - k)), k, true); }
  /* n/d arrodonit a k decimals */
  function rnd(n, d, k) { var m = p10(k), q = Math.floor(n * m / d), r = n * m - q * d; if (2 * r >= d) q++; return D(q, k, true); }
  function rndD(x, k) { return x.k <= k ? x : rnd(x.i, p10(x.k), k); }
  /* a : b com a fracció d'enters */
  function dq(a, b) { return [a.i * p10(b.k), b.i * p10(a.k)]; }
  /* divisió llarga n : d (enters) amb detecció del període */
  function ldiv(n, d, maxK) {
    var q = Math.floor(n / d), r = n - q * d, f = "", seen = {}, per = -1, rows = [];
    seen[r] = 0;
    while (r && f.length < maxK) {
      var r10 = r * 10, g = Math.floor(r10 / d);
      f += g; rows.push({ n: r10, g: g, r: r10 - g * d }); r = r10 - g * d;
      if (r && r in seen) { per = seen[r]; break; }
      seen[r] = f.length;
    }
    return { q: q, f: f, r: r, per: per, exact: r === 0, rows: rows };
  }
  /* n/d en TeX: exacte si té com a molt maxK decimals; si no, ≈ arrodonit */
  function qtex(n, d, k) {
    var L = ldiv(n, d, 6);
    if (L.exact) return { t: dt(D(parseInt(L.q + L.f, 10), L.f.length)), exact: true, v: D(parseInt(L.q + L.f, 10), L.f.length) };
    var v = rnd(n, d, k == null ? 2 : k);
    return { t: dt(v), exact: false, v: v };
  }
  function eq(q) { return (q.exact ? "=" : "\\approx ") + q.t; }
  function inVals(w) { var o = {}; w.querySelectorAll("[data-k]").forEach(function (x) { if (x.tagName === "INPUT") o[x.dataset.k] = x; }); return o; }
  function gsegs(w, cb) {
    var st = {};
    w.querySelectorAll(".seg").forEach(function (sg) {
      var g = sg.dataset.g, bs = sg.querySelectorAll("button");
      bs.forEach(function (b) {
        if (b.getAttribute("aria-pressed") === "true") st[g] = b.dataset.k;
        b.addEventListener("click", function () { bs.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); st[g] = b.dataset.k; cb(); });
      });
    });
    function set(g, k) { var sg = w.querySelector('.seg[data-g="' + g + '"]'); if (!sg) return; sg.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.k === k)); }); st[g] = k; }
    return { st: st, set: set };
  }
  function quickB(w, cb) { w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { cb(b.dataset.b.split(";")); }); }); }
  function ul(items) { return "<ul>" + items.map(function (s) { return "<li>" + s + "</li>"; }).join("") + "</ul>"; }

  /* ---------- noms de les posicions ---------- */
  var PN = {
    va: { i: ["unitats", "desenes", "centenes", "unitats de miler", "desenes de miler", "centenes de miler"], ia: ["U", "D", "C", "UM", "DM", "CM"],
          f: ["dècimes", "centèsimes", "mil·lèsimes"], f1: ["dècima", "centèsima", "mil·lèsima"], fa: ["d", "c", "m"], u1: "unitat" },
    es: { i: ["unidades", "decenas", "centenas", "unidades de millar", "decenas de millar", "centenas de millar"], ia: ["U", "D", "C", "UM", "DM", "CM"],
          f: ["décimas", "centésimas", "milésimas"], f1: ["décima", "centésima", "milésima"], fa: ["d", "c", "m"], u1: "unidad" },
    en: { i: ["units", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"], ia: ["U", "T", "H", "Th", "TTh", "HTh"],
          f: ["tenths", "hundredths", "thousandths"], f1: ["tenth", "hundredth", "thousandth"], fa: ["t", "h", "th"], u1: "unit" }
  };
  function pn() { return PN[lang] || PN.va; }
  function ordName(k) { return k === 0 ? pn().i[0] : pn().f[k - 1]; }

  /* ---------- 5.1 taula de valor posicional ---------- */
  function wPlace() {
    var w = document.getElementById("w-place"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var x = pdec(I.x.value, true);
      if (!x || x.k > 3 || digs(x)[0].replace(/^0+(?=\d)/, "").length > 6) { vis.innerHTML = ""; info.innerHTML = warn("plBad"); return; }
      var p = digs(x), ip = p[0].replace(/^0+(?=\d)/, ""), fp = p[1], P = pn(), h = "", r = "";
      for (var j = ip.length - 1; j >= 0; j--) { h += "<th>" + P.ia[j] + "<br><small>" + P.i[j] + "</small></th>"; r += '<td class="pi">' + ip[ip.length - 1 - j] + "</td>"; }
      if (fp) { h += '<th class="pc"></th>'; r += '<td class="pc">,</td>'; }
      for (var k = 0; k < fp.length; k++) { h += "<th>" + P.fa[k] + "<br><small>" + P.f[k] + "</small></th>"; r += '<td class="pf">' + fp[k] + "</td>"; }
      vis.innerHTML = '<div class="tbl-wrap"><table class="data pv"><thead><tr>' + h + "</tr></thead><tbody><tr>" + r + "</tr></tbody></table></div>";
      var iv = parseInt(ip, 10), fv = fp ? parseInt(fp, 10) : 0, read;
      var un = function (v) { return v === 1 ? P.u1 : P.i[0]; }, fn = function (v) { return v === 1 ? P.f1[fp.length - 1] : P.f[fp.length - 1]; };
      if (!fp || !fv) read = fh(iv) + " " + un(iv);
      else if (!iv) read = fh(fv) + " " + fn(fv);
      else read = fill(u("rdBoth"), { a: fh(iv) + " " + un(iv), b: fh(fv) + " " + fn(fv) });
      var parts = [];
      for (var a = 0; a < ip.length; a++) if (ip[a] !== "0") parts.push(dt(D(+ip[a] * p10(ip.length - 1 - a), 0)));
      for (var b = 0; b < fp.length; b++) if (fp[b] !== "0") parts.push(dt(D(+fp[b], b + 1, true)));
      var out = "<p><b>" + u("reads") + "</b> " + read + "</p>";
      if (parts.length > 1) out += "<p><b>" + u("decomp") + "</b> " + tex(dt(x) + "=" + parts.join("+")) + "</p>";
      if (fp) out += "<p><b>" + u("asFrac") + "</b> " + tex(dt(x) + "=" + frac(ft(x.i), ft(p10(x.k)))) + "</p>";
      var nx = norm(x);
      if (nx.k < x.k) out += hint(fill(u("plZeros"), { a: tex(dt(x)), b: tex(dt(nx)) }));
      info.innerHTML = out;
    }
    I.x.addEventListener("input", render);
    quickB(w, function (p) { I.x.value = p[0]; render(); });
    onLang(render);
  }

  /* ---------- 5.2 lupa de la recta ---------- */
  function zoomSVG(x) {
    var lev = Math.max(1, x.k), W = 540, X0 = 30, X1 = 510, H = 74, g = "", px = [];
    for (var L = 1; L <= lev; L++) {
      var lo = truncD(x, L - 1), y = 22 + (L - 1) * H, step = D(1, L);
      var X = function (v) { return X0 + (dnum(dsub(v, lo)) / dnum(dmul(step, N(10)))) * (X1 - X0); };
      g += '<line class="nl-ax" x1="' + (X0 - 14) + '" y1="' + y + '" x2="' + (X1 + 14) + '" y2="' + y + '"/>';
      for (var j = 0; j <= 10; j++) {
        var v = dadd(lo, dmul(step, N(j))), xx = X(v).toFixed(1), big = j === 0 || j === 10;
        g += '<line class="' + (big ? "nl-tb" : "nl-tk") + '" x1="' + xx + '" y1="' + (y - (big ? 9 : 6)) + '" x2="' + xx + '" y2="' + (y + (big ? 9 : 6)) + '"/>';
        g += '<text class="' + (big ? "fr-t" : "fr-tm") + '" x="' + xx + '" y="' + (y + 24) + '" text-anchor="middle" style="font-size:' + (big ? 12 : 10.5) + 'px">' + dstr(v, big ? L - 1 : L) + "</text>";
      }
      var xp = X(x);
      g += '<circle class="nl-dot" cx="' + xp.toFixed(1) + '" cy="' + y + '" r="6" style="fill:var(--accent)"/>';
      px.push({ y: y, a: X(truncD(x, L)), b: X(dadd(truncD(x, L), step)) });
    }
    for (var m = 0; m < px.length - 1; m++)
      g += '<line class="zl" x1="' + px[m].a.toFixed(1) + '" y1="' + (px[m].y + 9) + '" x2="' + X0 + '" y2="' + (px[m + 1].y - 9) + '"/><line class="zl" x1="' + px[m].b.toFixed(1) + '" y1="' + (px[m].y + 9) + '" x2="' + X1 + '" y2="' + (px[m + 1].y - 9) + '"/>';
    return '<svg viewBox="0 0 ' + W + " " + (lev * H + 4) + '">' + g + "</svg>";
  }
  function wZoom() {
    var w = document.getElementById("w-zoom"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var x = pdec(I.x.value);
      if (!x || x.k > 3 || dnum(x) >= 1000) { vis.innerHTML = ""; info.innerHTML = warn("zBad"); return; }
      vis.className = "fvis zoomv"; vis.innerHTML = zoomSVG(x);
      var lines = [], lev = Math.max(1, x.k);
      for (var L = 1; L <= lev; L++) {
        var lo = truncD(x, L - 1), hi = dadd(lo, D(1, L - 1));
        lines.push(fill(u("zLine"), { a: tex(dt(lo, L - 1)), b: tex(dt(hi, L - 1)), n: ordName(L) }));
      }
      info.innerHTML = ul(lines);
    }
    I.x.addEventListener("input", render);
    quickB(w, function (p) { I.x.value = p[0]; render(); });
    onLang(render);
  }

  /* ---------- 5.2 truncar i arrodonir ---------- */
  function wRound() {
    var w = document.getElementById("w-round"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info");
    var S = gsegs(w, render);
    function render() {
      var x = pdec(I.x.value), k = +S.st.k;
      if (!x || x.k > 6) { vis.innerHTML = ""; info.innerHTML = warn("rBad"); return; }
      if (x.k <= k) { vis.innerHTML = ""; info.innerHTML = "<p>" + fill(u("rNone"), { x: tex(dt(x)), n: ordName(k) }) + "</p>"; return; }
      var p = digs(x), s = p[0] + "," + p[1], cut = p[0].length + (k ? 1 + k : 0), ni = k ? cut : cut + 1, nxt = +p[1][k];
      var sh = '<div class="digits">';
      for (var c = 0; c < s.length; c++) {
        var ch = s[c], cls = ch === "," ? "cm" : c < cut ? "" : c === ni ? "z" : "fd";
        sh += '<span class="' + cls + '">' + ch + "</span>";
      }
      sh += "</div>";
      vis.innerHTML = sh;
      var t = truncD(x, k), r = rndD(x, k);
      info.innerHTML = "<p>" + fill(u("rKeep"), { n: ordName(k), d: "<b>" + nxt + "</b>" }) + " " + (nxt >= 5 ? u("rUp") : u("rDown")) + "</p>"
        + tex("\\text{" + u("trunc") + "}:\\ " + dt(t, k) + "\\qquad\\text{" + u("round") + "}:\\ " + dt(x) + "\\approx\\boxed{" + dt(r, k) + "}", true);
    }
    I.x.addEventListener("input", render);
    quickB(w, function (p) { I.x.value = p[0]; render(); });
    onLang(render);
  }

  /* ---------- 5.3 operacions en columna ---------- */
  function colAdd(a, b, op, r) {
    var k = Math.max(a.k, b.k, r.k), A = digs(a, k), B = digs(b, k), R = digs(r, k), wI = Math.max(A[0].length, B[0].length, R[0].length);
    function row(pre, d, ok, cls) {
      var h = "<tr" + (cls ? ' class="' + cls + '"' : "") + "><td>" + pre + "</td>";
      for (var j = 0; j < wI - d[0].length; j++) h += "<td></td>";
      for (j = 0; j < d[0].length; j++) h += "<td>" + d[0][j] + "</td>";
      if (k) { h += '<td class="cm">,</td>'; for (j = 0; j < k; j++) h += "<td" + (j >= ok ? ' class="z"' : "") + ">" + d[1][j] + "</td>"; }
      return h + "</tr>";
    }
    return '<div class="colop"><table>' + row("", A, a.k) + row(op === "+" ? "+" : "−", B, b.k) + row("", R, k, "res") + "</table></div>";
  }
  function colMul(a, b, r) {
    var da = digs(a), db = digs(b), sa = da[0] + da[1], sb = db[0] + db[1], sbi = String(b.i), prod = String(a.i * b.i), partials = [], W;
    for (var j = sbi.length - 1; j >= 0; j--) partials.push(String(a.i * +sbi[j]));
    W = Math.max(sa.length, sb.length, prod.length, partials.reduce(function (m, p, i) { return Math.max(m, p.length + i); }, 0)) + 1;
    function row(s, pre, kk, cls, shift) {
      var cells = s.split(""), h = "<tr" + (cls ? ' class="' + cls + '"' : "") + ">", sh = shift || 0;
      for (var j = 0; j < W - cells.length - sh; j++) h += "<td>" + (j === 0 ? pre : "") + "</td>";
      cells.forEach(function (c, i) { h += "<td>" + c + (kk && i === cells.length - kk - 1 ? '<span class="hl">,</span>' : "") + "</td>"; });
      for (j = 0; j < sh; j++) h += "<td></td>";
      return h + "</tr>";
    }
    var h = '<div class="colop"><table>' + row(sa, "", a.k) + row(sb, "×", b.k);
    if (sbi.length > 1) {
      partials.forEach(function (p, i) { h += row(p, i === partials.length - 1 ? "+" : "", 0, i === 0 ? "res" : "", i); });
    }
    var kk = a.k + b.k, pr = prod; while (pr.length <= kk) pr = "0" + pr;
    h += row(pr, "", kk, "res") + "</table></div>";
    return h;
  }
  function wCol() {
    var w = document.getElementById("w-col"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), S = gsegs(w, render);
    function render() {
      var a = pdec(I.a.value, true), b = pdec(I.b.value, true), op = S.st.op;
      if (!a || !b || a.k > 4 || b.k > 4 || dnum(a) > 1e6 || dnum(b) > 1e6) { vis.innerHTML = ""; info.innerHTML = warn("cBad"); return; }
      if (op === "-" && dcmp(a, b) < 0) { vis.innerHTML = ""; info.innerHTML = warn("cNeg"); return; }
      if (op === "*") {
        if (String(a.i).length + String(b.i).length > 12 || String(b.i).length > 4) { vis.innerHTML = ""; info.innerHTML = warn("cBig"); return; }
        var r = dmul(a, b), kk = a.k + b.k;
        vis.innerHTML = '<div class="colw">' + colMul(a, b, r) + "</div>";
        info.innerHTML = "<p>" + fill(u("cMul"), { a: tex(ft(a.i) + "\\cdot " + ft(b.i) + "=" + ft(a.i * b.i)) }) + "</p><p>" + fill(u("cMulK"), { a: a.k, b: b.k, k: kk }) + "</p>"
          + tex(dt(a) + "\\cdot " + dt(b) + "=" + (r.k < kk ? dt(D(a.i * b.i, kk, true)) + "=" : "") + "\\boxed{" + dt(r) + "}", true);
        return;
      }
      var res = op === "+" ? dadd(a, b) : dsub(a, b);
      vis.innerHTML = '<div class="colw">' + colAdd(a, b, op, res) + "</div>";
      info.innerHTML = "<p>" + u(a.k !== b.k ? "cPad" : "cAlign") + "</p>" + tex(dt(a) + (op === "+" ? "+" : "-") + dt(b) + "=\\boxed{" + dt(res) + "}", true);
    }
    ["a", "b"].forEach(function (k) { I[k].addEventListener("input", render); });
    quickB(w, function (p) { I.a.value = p[0]; I.b.value = p[1]; S.set("op", p[2]); render(); });
    onLang(render);
  }

  /* ---------- 5.3 multiplicar i dividir per la unitat seguida de zeros ---------- */
  function digRow(ip, fp, zl, zr) {
    var s = ip + fp, h = '<div class="digits">';
    for (var c = 0; c < s.length; c++) {
      if (c === ip.length && fp) h += '<span class="cm">,</span>';
      h += '<span' + (c < zl || c >= s.length - zr ? ' class="z"' : "") + ">" + s[c] + "</span>";
    }
    return h + "</div>";
  }
  function wP10() {
    var w = document.getElementById("w-p10"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), S = gsegs(w, render);
    function render() {
      var x = pdec(I.x.value, true), op = S.st.op, p = +S.st.p;
      if (!x || x.k > 6 || dnum(x) > 1e7) { vis.innerHTML = ""; info.innerHTML = warn("zBad2"); return; }
      var r, zl = 0, zr = 0, a = digs(x), orig = (a[0] + a[1]).length;
      if (op === "*") { if (x.k >= p) r = D(x.i, x.k - p, true); else { r = D(x.i * p10(p - x.k), 0, true); zr = p - x.k; } }
      else { r = D(x.i, x.k + p, true); var b0 = digs(r); zl = Math.max(0, (b0[0] + b0[1]).length - orig); }
      var b = digs(r);
      vis.innerHTML = digRow(a[0], a[1], 0, 0) + '<div class="dlab">' + (op === "*" ? "× " : ": ") + p10(p) + " ⟶ " + u(op === "*" ? "pRight" : "pLeft").replace("{p}", p) + "</div>" + digRow(b[0], b[1], zl, zr);
      var nr = norm(r);
      info.innerHTML = tex(dt(x) + (op === "*" ? "\\cdot " : ":") + ft(p10(p)) + "=\\boxed{" + dt(nr) + "}", true)
        + (zl + zr ? hint(fill(u("pZeros"), { n: zl + zr })) : "");
    }
    I.x.addEventListener("input", render);
    quickB(w, function (q) { I.x.value = q[0]; S.set("op", q[1]); S.set("p", q[2]); render(); });
    onLang(render);
  }

  /* ---------- 5.4 divisió pas a pas ---------- */
  function divRows(Nn, K, d, k) {
    var s = String(Nn); while (s.length <= K) s = "0" + s;
    var ip = s.slice(0, s.length - K), fp = (s.slice(s.length - K) + "0".repeat(Math.max(0, k - K))).slice(0, Math.max(k, 0));
    var all = ip + fp, cur = 0, rows = [], started = false;
    for (var j = 0; j < all.length; j++) {
      cur = cur * 10 + +all[j];
      if (!started && cur < d && j < ip.length - 1) continue;
      started = true;
      var g = Math.floor(cur / d);
      rows.push({ n: cur, g: g, r: cur - g * d, dec: j >= ip.length, first: j === ip.length, zero: j >= ip.length + K });
      cur = cur - g * d;
      if (!cur && j >= ip.length + K - 1) break;
    }
    return rows;
  }
  function wDiv() {
    var w = document.getElementById("w-div"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), S = gsegs(w, render);
    function render() {
      var a = pdec(I.a.value), b = pdec(I.b.value), k = +S.st.k;
      if (!a || !b || !b.i || a.k > 4 || b.k > 4 || dnum(a) > 1e6 || dnum(b) > 1e5) { vis.innerHTML = ""; info.innerHTML = warn(b && !b.i ? "dZero" : "dBad"); return; }
      var out = "", m = b.k, A = dmul(a, D(p10(m), 0)), d = b.i;
      if (m) out += "<p>" + fill(u("dMove"), { p: ft(p10(m)) }) + "</p>" + tex(dt(a) + ":" + dt(b) + "\\ \\xrightarrow{\\ \\cdot " + ft(p10(m)) + "\\ }\\ " + dt(A) + ":" + ft(d), true);
      var Nn = A.i, K = A.k, num = k >= K ? Nn * p10(k - K) : Nn, den = k >= K ? d : d * p10(K - k);
      if (num > 1e15) { vis.innerHTML = ""; info.innerHTML = warn("dBad"); return; }
      var q = D(Math.floor(num / den), k, true), rem = dsub(A, dmul(N(d), q));
      var rows = divRows(Nn, K, d, k), li = [];
      rows.slice(0, 16).forEach(function (r) {
        var s = (r.first ? '<span class="hl">' + u("dComma") + "</span> " : "") + (r.zero ? '<span class="hl">' + u("dAddZ") + "</span> " : "");
        li.push(s + tex(ft(r.n) + ":" + ft(d) + "=" + r.g) + " &nbsp;<span style=\"color:var(--muted)\">" + u("rem") + " " + r.r + "</span>");
      });
      if (rows.length > 16) li.push("…");
      vis.innerHTML = '<ol class="dsteps">' + li.map(function (s) { return "<li>" + s + "</li>"; }).join("") + "</ol>";
      var ex = !rem.i;
      out += tex(dt(A) + ":" + ft(d) + (ex ? "=" : "\\approx ") + "\\boxed{" + dt(ex ? norm(q) : q, ex ? 0 : k) + "}", true);
      out += "<p>" + (ex ? u("dExact") : fill(u("dRem"), { r: tex(dt(rem)) })) + " " + u("check") + " " + tex(ft(d) + "\\cdot " + dt(ex ? norm(q) : q, ex ? 0 : k) + (ex ? "" : "+" + dt(rem)) + "=" + dt(A)) + "</p>";
      if (dcmp(b, N(1)) < 0 && dcmp(q, a) > 0) out += hint(u("dLess1"));
      info.innerHTML = out;
    }
    ["a", "b"].forEach(function (x) { I[x].addEventListener("input", render); });
    quickB(w, function (p) { I.a.value = p[0]; I.b.value = p[1]; render(); });
    onLang(render);
  }

  /* ---------- 5.5 fraccions i decimals ---------- */
  function perTex(L) {
    if (L.exact) return dt(D(parseInt(L.q + L.f, 10), L.f.length));
    var ante = L.f.slice(0, L.per), per = L.f.slice(L.per);
    return ft(L.q) + "{,}" + ante + "\\overline{" + per + "}";
  }
  function wFd() {
    var w = document.getElementById("w-fd"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), S = gsegs(w, render);
    function render() {
      var m = S.st.m;
      w.querySelectorAll("[data-p]").forEach(function (e) { e.hidden = e.dataset.p !== m; });
      if (m === "d") {
        var x = pdec(I.x.value);
        if (!x || x.k > 6 || dnum(x) > 1e6) { vis.innerHTML = ""; info.innerHTML = warn("fdBadD"); return; }
        if (!x.k) { vis.innerHTML = ""; info.innerHTML = "<p>" + u("fdNat") + "</p>"; return; }
        var den = p10(x.k), g = gcd(x.i, den), f = rat(x.i, den);
        vis.innerHTML = "";
        info.innerHTML = "<p>" + fill(u("fdD1"), { k: x.k, z: x.k }) + "</p>" + tex(dt(x) + "=" + frac(ft(x.i), ft(den)) + (g > 1 ? "=" + frac(ft(x.i) + ":" + g, ft(den) + ":" + g) + "=\\boxed{" + fr(f) + "}" : ""), true)
          + (g > 1 ? "<p>" + fill(u("fdSimp"), { g: g }) + "</p>" : "<p>" + u("fdIrr") + "</p>");
        return;
      }
      var n = pnat(I.n.value), d = pnat(I.d.value);
      if (!(n >= 0) || !(d >= 1) || n > 99999 || d > 999) { vis.innerHTML = ""; info.innerHTML = warn("fdBadF"); return; }
      var L = ldiv(n, d, 40), li = [];
      L.rows.slice(0, 14).forEach(function (r, i) {
        var rep = !L.exact && L.per >= 0 && i === L.rows.length - 1;
        li.push(tex(ft(r.n) + ":" + ft(d) + "=" + r.g) + " &nbsp;<span style=\"color:var(--muted)\">" + u("rem") + " <b" + (rep ? ' class="hl"' : "") + ">" + r.r + "</b></span>" + (rep ? ' <span class="hl">← ' + u("fdRep") + "</span>" : ""));
      });
      if (L.rows.length > 14) li.push("…");
      vis.innerHTML = (L.rows.length ? "<p>" + fill(u("fdStart"), { a: tex(ft(n) + ":" + ft(d) + "=" + ft(L.q)), r: n - L.q * d }) + "</p>" : "") + '<ol class="dsteps">' + li.map(function (s) { return "<li>" + s + "</li>"; }).join("") + "</ol>";
      var kind, f = rat(n, d), dd = f.d; while (dd % 2 === 0) dd /= 2; while (dd % 5 === 0) dd /= 5;
      if (L.exact) kind = u(L.f ? "fdExact" : "fdWhole");
      else if (L.per < 0) kind = u("fdLong");
      else kind = u(L.per === 0 ? "fdPure" : "fdMixed");
      var expand = L.exact ? "" : "=" + ft(L.q) + "{,}" + (L.f + L.f.slice(L.per)).slice(0, Math.max(8, L.f.length + 2)) + "\\ldots";
      info.innerHTML = tex(frac(ft(n), ft(d)) + expand + "=\\boxed{" + (L.per < 0 && !L.exact ? dt(rnd(n, d, 6)) + "\\ldots" : perTex(L)) + "}", true) + "<p>" + kind
        + (!L.exact && L.per >= 0 ? " " + fill(u("fdPer"), { p: tex(L.f.slice(L.per)) }) + (L.per ? " " + fill(u("fdAnte"), { a: tex(L.f.slice(0, L.per)) }) : "") : "") + "</p>"
        + hint(fill(u(dd === 1 ? "fdWhy1" : "fdWhy2"), { f: tex(fr(f)), d: f.d }));
    }
    ["n", "d", "x"].forEach(function (x) { I[x].addEventListener("input", render); });
    quickB(w, function (p) { S.set("m", p[0]); if (p[0] === "f") { I.n.value = p[1]; I.d.value = p[2]; } else I.x.value = p[1]; render(); });
    onLang(render);
  }

  /* ---------- 5.6 terme desconegut d'una proporció ---------- */
  function wProp() {
    var w = document.getElementById("w-prop"); if (!w) return;
    var I = inVals(w), info = w.querySelector(".info"), ks = ["a", "b", "c", "d"];
    function render() {
      var v = {}, xs = [];
      for (var j = 0; j < 4; j++) {
        var s = I[ks[j]].value.trim();
        if (/^[xX]$/.test(s)) { xs.push(ks[j]); continue; }
        v[ks[j]] = pdec(s);
        if (!v[ks[j]] || !v[ks[j]].i || v[ks[j]].k > 4 || dnum(v[ks[j]]) > 1e6) { info.innerHTML = warn("prBad"); return; }
      }
      if (xs.length > 1) { info.innerHTML = warn("prOneX"); return; }
      var T = function (k) { return xs[0] === k ? "x" : dt(v[k]); };
      var lhs = frac(T("a"), T("b")) + "=" + frac(T("c"), T("d"));
      if (!xs.length) {
        var p1 = dmul(v.a, v.d), p2 = dmul(v.b, v.c), ok = !dcmp(p1, p2);
        info.innerHTML = tex(lhs, true) + "<p>" + tex(dt(v.a) + "\\cdot " + dt(v.d) + "=" + dt(p1)) + " &nbsp; " + tex(dt(v.b) + "\\cdot " + dt(v.c) + "=" + dt(p2)) + "</p><p>" + u(ok ? "prYes" : "prNo") + "</p>";
        return;
      }
      var x = xs[0], pair = (x === "a" || x === "d") ? ["b", "c"] : ["a", "d"], other = { a: "d", d: "a", b: "c", c: "b" }[x];
      var num = dmul(v[pair[0]], v[pair[1]]), Q = dq(num, v[other]), q = qtex(Q[0], Q[1], 2);
      info.innerHTML = tex(lhs, true) + "<p>" + u("prCross") + "</p>"
        + tex((x === "a" || x === "d" ? "x\\cdot " + dt(v[other]) : dt(v[other]) + "\\cdot x") + "=" + dt(v[pair[0]]) + "\\cdot " + dt(v[pair[1]]) + "=" + dt(num)
          + "\\ \\Rightarrow\\ x=" + frac(dt(num), dt(v[other])) + eq(q).replace(q.t, "\\boxed{" + q.t + "}"), true);
    }
    ks.forEach(function (k) { I[k].addEventListener("input", render); });
    quickB(w, function (p) { ks.forEach(function (k, j) { I[k].value = p[j]; }); render(); });
    onLang(render);
  }

  /* ---------- 5.7-5.8 regla de tres ---------- */
  function esc(s) { return String(s).replace(/[\\{}$&#%_^~]/g, "").slice(0, 18); }
  function wR3() {
    var w = document.getElementById("w-r3"); if (!w) return;
    var I = inVals(w), info = w.querySelector(".info"), vis = w.querySelector(".fvis"), u0 = w.querySelector(".u0"), S = gsegs(w, render);
    function render() {
      var a = pdec(I.a.value, true), b = pdec(I.b.value, true), c = pdec(I.c.value, true), t = S.st.t, ma = esc(I.ma.value), mb = esc(I.mb.value);
      u0.textContent = I.ma.value.slice(0, 18);
      if (!a || !b || !c || !a.i || !c.i || a.k > 3 || b.k > 3 || c.k > 3 || dnum(a) > 1e6 || dnum(b) > 1e6 || dnum(c) > 1e6) { vis.innerHTML = ""; info.innerHTML = warn("r3Bad"); return; }
      var A = "\\text{" + ma + "}", B = "\\text{" + mb + "}", eur = /€/.test(mb);
      var money = function (q) { if (eur && q.v.k === 1) q.t = dt(q.v, 2); return q; };
      vis.innerHTML = tex("\\begin{array}{rcl}" + dt(a) + "\\ " + A + "&\\longrightarrow&" + dt(b) + "\\ " + B + "\\\\" + dt(c) + "\\ " + A + "&\\longrightarrow&x\\end{array}", true);
      var out = "<p>" + u(t === "d" ? "r3D" : "r3I") + "</p>", num, den, unit, Q;
      if (t === "d") {
        Q = dq(b, a); unit = money(qtex(Q[0], Q[1], 4));
        out += "<p><b>" + u("r3Unit") + "</b> " + tex("1\\ " + A + "\\ \\to\\ " + dt(b) + ":" + dt(a) + eq(unit) + "\\ " + B) + "</p>";
        num = dmul(b, c); Q = dq(num, a);
        var x = money(qtex(Q[0], Q[1], 2));
        out += "<p><b>" + u("r3Rule") + "</b></p>" + tex(frac(dt(a), dt(c)) + "=" + frac(dt(b), "x") + "\\ \\Rightarrow\\ x=" + frac(dt(b) + "\\cdot " + dt(c), dt(a)) + "=" + frac(dt(num), dt(a)) + eq(x).replace(x.t, "\\boxed{" + x.t + "}") + "\\ " + B, true);
      } else {
        num = dmul(a, b); Q = dq(num, c); var y = money(qtex(Q[0], Q[1], 2));
        out += "<p><b>" + u("r3Unit") + "</b> " + tex("1\\ " + A + "\\ \\to\\ " + dt(b) + "\\cdot " + dt(a) + "=" + dt(num) + "\\ " + B) + "</p>";
        out += "<p><b>" + u("r3Rule") + "</b> " + u("r3Prod") + "</p>" + tex(dt(a) + "\\cdot " + dt(b) + "=" + dt(c) + "\\cdot x\\ \\Rightarrow\\ x=" + frac(dt(a) + "\\cdot " + dt(b), dt(c)) + "=" + frac(dt(num), dt(c)) + eq(y).replace(y.t, "\\boxed{" + y.t + "}") + "\\ " + B, true);
      }
      info.innerHTML = out;
    }
    ["a", "b", "c", "ma", "mb"].forEach(function (k) { I[k].addEventListener("input", render); });
    quickB(w, function (p) { S.set("t", p[0]); I.a.value = p[1]; I.ma.value = p[2]; I.b.value = p[3]; I.mb.value = p[4]; I.c.value = p[5]; render(); });
    onLang(render);
  }

  /* ---------- 5.8 directa, inversa o cap ---------- */
  function rdec(r) { var q = qtex(r.n, r.d, 3); return eq(q).replace(/^=/, ""); }
  function wKind() {
    var w = document.getElementById("w-kind"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var xs = [], ys = [];
      for (var j = 0; j < 4; j++) {
        var x = pdec(I["x" + j].value), y = pdec(I["y" + j].value);
        if (!x || !y || !x.i || !y.i || x.k > 3 || y.k > 3 || dnum(x) > 1e5 || dnum(y) > 1e5) { vis.innerHTML = ""; info.innerHTML = warn("kBad"); return; }
        xs.push(x); ys.push(y);
      }
      var R = function (v) { return rat(v.i, p10(v.k)); };
      var qs = xs.map(function (x, j) { return rdiv(R(ys[j]), R(x)); }), ps = xs.map(function (x, j) { return rmul(R(ys[j]), R(x)); });
      var allQ = qs.every(function (q) { return !rcmp(q, qs[0]); }), allP = ps.every(function (p) { return !rcmp(p, ps[0]); });
      var row = function (lab, arr, ok) { return "<tr><td>" + lab + "</td>" + arr.map(function (v) { return '<td class="' + (ok ? "ok" : "") + '">' + tex(rdec(v)) + "</td>"; }).join("") + "</tr>"; };
      var tab = '<div class="tbl-wrap"><table class="data ptab kres"><tbody>' + row(tex("y:x"), qs, allQ) + row(tex("x\\cdot y"), ps, allP) + "</tbody></table></div>";
      var xm = Math.max.apply(null, xs.map(dnum)), ym = Math.max.apply(null, ys.map(dnum)), W = 300, H = 190, X0 = 34, Y0 = H - 24, X1 = W - 12, Y1 = 12;
      var g = '<line class="nl-ax" x1="' + X0 + '" y1="' + Y0 + '" x2="' + X1 + '" y2="' + Y0 + '"/><line class="nl-ax" x1="' + X0 + '" y1="' + Y0 + '" x2="' + X0 + '" y2="' + Y1 + '"/>';
      if (allQ) g += '<line class="nl-seg" style="stroke-width:2.5" x1="' + X0 + '" y1="' + Y0 + '" x2="' + X1 + '" y2="' + (Y0 - rval(qs[0]) * xm * 1.1 / (ym * 1.1) * (Y0 - Y1)).toFixed(1) + '"/>';
      xs.forEach(function (x, j) { g += '<circle class="nl-dot" cx="' + (X0 + dnum(x) / (xm * 1.1) * (X1 - X0)).toFixed(1) + '" cy="' + (Y0 - dnum(ys[j]) / (ym * 1.1) * (Y0 - Y1)).toFixed(1) + '" r="5" style="fill:var(--accent)"/>'; });
      vis.innerHTML = tab + '<div class="figs"><svg viewBox="0 0 ' + W + " " + H + '" style="width:' + W + 'px">' + g + "</svg></div>";
      info.innerHTML = "<p>" + (allQ ? fill(u("kDir"), { k: tex(rdec(qs[0])) }) : allP ? fill(u("kInv"), { k: tex(rdec(ps[0])) }) : u("kNone")) + "</p>";
    }
    for (var j = 0; j < 4; j++) { I["x" + j].addEventListener("input", render); I["y" + j].addEventListener("input", render); }
    quickB(w, function (p) { for (var j = 0; j < 4; j++) { I["x" + j].value = p[j]; I["y" + j].value = p[4 + j]; } render(); });
    onLang(render);
  }

  /* ---------- 5.9 percentatges ---------- */
  function shiftD(x, s) { return D(x.i, x.k + s); }
  function bars(rows) {
    var mx = Math.max.apply(null, rows.map(function (r) { return r.v; })) || 1;
    return '<div class="vbars">' + rows.map(function (r) { return '<div class="vbar"><span>' + r.l + '</span><div class="tr"><div class="fl ' + (r.c || "") + '" style="width:' + Math.max(8, r.v / mx * 100).toFixed(1) + '%">' + r.t + "</div></div></div>"; }).join("") + "</div>";
  }
  function wPct() {
    var w = document.getElementById("w-pct"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), S = gsegs(w, render), last = {};
    function render() {
      var m = S.st.m, unk = { a: "a", p: "p", n: "n" }[m];
      ["p", "n", "a"].forEach(function (k) { var ro = k === unk; if (ro && I[k].value !== "?") last[k] = I[k].value; if (!ro && I[k].value === "?") I[k].value = last[k] || ""; I[k].readOnly = ro; I[k].classList.toggle("ro", ro); if (ro) I[k].value = "?"; });
      var p = pdec(I.p.value), n = pdec(I.n.value), a = pdec(I.a.value), out = "";
      var bad = function () { vis.innerHTML = ""; info.innerHTML = warn("pcBad"); };
      if (m === "a") {
        if (!p || !n || p.k > 3 || n.k > 3 || dnum(n) > 1e9 || dnum(p) > 1000) return bad();
        var pd = shiftD(p, 2), A = dmul(n, pd);
        out = tex(dt(p) + "\\,\\%=" + frac(dt(p), 100) + "=" + dt(pd), true) + tex(dt(p) + "\\,\\%\\ \\text{" + u("of") + "}\\ " + dt(n) + "=" + dt(n) + "\\cdot " + dt(pd) + "=\\boxed{" + dt(A) + "}", true);
        a = A;
      } else if (m === "p") {
        if (!a || !n || !n.i || a.k > 3 || n.k > 3 || dnum(n) > 1e9 || dnum(a) > 1e9) return bad();
        var Q = dq(dmul(a, N(100)), n), q = qtex(Q[0], Q[1], 2), Q1 = dq(a, n), q1 = qtex(Q1[0], Q1[1], 4);
        out = tex(frac(dt(a), dt(n)) + eq(q1) + "\\ \\Rightarrow\\ " + q1.t + "\\cdot 100" + eq(q).replace(q.t, "\\boxed{" + q.t + "\\,\\%}"), true);
        p = q.v;
      } else {
        if (!a || !p || !p.i || a.k > 3 || p.k > 3 || dnum(a) > 1e9 || dnum(p) > 1000) return bad();
        var pd2 = shiftD(p, 2), Q2 = dq(a, pd2), q2 = qtex(Q2[0], Q2[1], 2);
        out = "<p>" + fill(u("pcTot"), { p: tex(dt(p) + "\\,\\%"), a: tex(dt(a)) }) + "</p>" + tex("\\text{" + u("total") + "}=" + dt(a) + ":" + dt(pd2) + eq(q2).replace(q2.t, "\\boxed{" + q2.t + "}"), true)
          + "<p>" + u("check") + " " + tex(q2.t + "\\cdot " + dt(pd2) + (q2.exact ? "=" : "\\approx ") + dt(a)) + "</p>";
        n = q2.v;
      }
      var pv = dnum(p), cells = Math.round(Math.min(pv, 100));
      vis.innerHTML = '<div class="pgrid">' + Array.apply(null, Array(100)).map(function (_, i) { return i < cells ? '<i class="on"></i>' : "<i></i>"; }).join("") + "</div>"
        + bars([{ l: u("total"), v: dnum(n), t: dstr(rndD(n, 2)), c: "b2" }, { l: u("part") + " (" + dstr(rndD(p, 2)) + " %)", v: dnum(a), t: dstr(rndD(a, 2)) }]);
      info.innerHTML = out + (pv > 100 ? hint(u("pcOver")) : "");
    }
    ["p", "n", "a"].forEach(function (k) { I[k].addEventListener("input", render); });
    quickB(w, function (q) {
      S.set("m", q[0]);
      ["p", "n", "a"].forEach(function (k, j) { I[k].readOnly = false; if (q[j + 1] !== undefined && q[j + 1] !== "") I[k].value = q[j + 1]; else I[k].value = "?"; });
      render();
    });
    onLang(render);
  }

  /* ---------- 5.10 augments i disminucions ---------- */
  function wVar() {
    var w = document.getElementById("w-var"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), S = gsegs(w, render);
    function render() {
      var q = pdec(I.q.value), p = pdec(I.p.value), up = S.st.t === "+", fin = S.st.w === "f";
      if (!q || !p || q.k > 3 || p.k > 2 || dnum(q) > 1e9 || (!up && dcmp(p, N(100)) >= 0) || dnum(p) > 1000) { vis.innerHTML = ""; info.innerHTML = warn("vBad"); return; }
      var pd = shiftD(p, 2), idx = up ? dadd(N(1), pd) : dsub(N(1), pd), pr = up ? dadd(N(100), p) : dsub(N(100), p), out;
      out = "<p>" + fill(u(up ? "vUp" : "vDown"), { p: tex(dt(p) + "\\,\\%"), r: tex(dt(pr) + "\\,\\%"), i: tex(dt(idx)) }) + "</p>";
      var ini, fn;
      if (fin) {
        ini = q; fn = dmul(q, idx);
        var ch = dmul(q, pd), f2 = rndD(fn, 2);
        out += "<p><b>" + u("vM1") + "</b> " + tex(dt(q) + "\\cdot " + dt(pd) + "=" + dt(ch) + "\\qquad " + dt(q) + (up ? "+" : "-") + dt(ch) + "=" + dt(fn)) + "</p>"
          + "<p><b>" + u("vM2") + "</b></p>" + tex(dt(q) + "\\cdot " + dt(idx) + "=\\boxed{" + dt(fn) + "}", true)
          + (fn.k > 2 ? "<p>" + fill(u("vRound"), { v: tex(dt(f2, 2)) }) + "</p>" : "");
      } else {
        fn = q; var Q = dq(q, idx), x = qtex(Q[0], Q[1], 2); ini = x.v;
        out += "<p>" + u("vInv") + "</p>" + tex("\\text{" + u("vIni") + "}=" + dt(q) + ":" + dt(idx) + eq(x).replace(x.t, "\\boxed{" + x.t + "}"), true)
          + "<p>" + u("check") + " " + tex(x.t + "\\cdot " + dt(idx) + (x.exact ? "=" : "\\approx ") + dt(q)) + "</p>";
      }
      vis.innerHTML = bars([{ l: u("vIni"), v: dnum(ini), t: dstr(rndD(ini, 2)), c: "b2" }, { l: u("vFin"), v: dnum(fn), t: dstr(rndD(fn, 2)) }]);
      info.innerHTML = out;
    }
    ["q", "p"].forEach(function (k) { I[k].addEventListener("input", render); });
    quickB(w, function (p) { S.set("t", p[0]); S.set("w", p[1]); I.q.value = p[2]; I.p.value = p[3]; render(); });
    onLang(render);
  }

  /* ---------- entrenadors ---------- */
  function rdD(maxI, k) { return D(rint(0, maxI) * p10(k) + rint(1, p10(k) - 1), k, true); }
  var R3T = {
    d: [{ va: "Si {a} kg de pomes costen {b} €, quant costen {c} kg?", es: "Si {a} kg de manzanas cuestan {b} €, ¿cuánto cuestan {c} kg?", en: "If {a} kg of apples cost {b} €, how much do {c} kg cost?", u: "€" },
        { va: "{a} entrades de cine costen {b} €. Quant costen {c} entrades?", es: "{a} entradas de cine cuestan {b} €. ¿Cuánto cuestan {c} entradas?", en: "{a} cinema tickets cost {b} €. How much do {c} tickets cost?", u: "€" },
        { va: "Un cotxe gasta {b} L en {a} hores. Quants litres gasta en {c} hores (a la mateixa velocitat)?", es: "Un coche gasta {b} L en {a} horas. ¿Cuántos litros gasta en {c} horas (a la misma velocidad)?", en: "A car uses {b} L in {a} hours. How many litres in {c} hours (same speed)?", u: "L" }],
    i: [{ va: "{a} pintors pinten una nau en {b} dies. Quants dies tardarien {c} pintors?", es: "{a} pintores pintan una nave en {b} días. ¿Cuántos días tardarían {c} pintores?", en: "{a} painters paint a warehouse in {b} days. How many days would {c} painters take?", u: "" },
        { va: "{a} aixetes omplin un dipòsit en {b} hores. Quantes hores tardarien {c} aixetes iguals?", es: "{a} grifos llenan un depósito en {b} horas. ¿Cuántas horas tardarían {c} grifos iguales?", en: "{a} taps fill a tank in {b} hours. How many hours would {c} identical taps take?", u: "h" },
        { va: "Repartim uns caramels entre {a} xiquets i en toquen {b} a cadascun. Quants en tocarien si foren {c} xiquets?", es: "Repartimos unos caramelos entre {a} niños y tocan a {b} cada uno. ¿Cuántos tocarían si fueran {c} niños?", en: "We share some sweets among {a} children and each gets {b}. How many would each get if there were {c} children?", u: "" }]
  };
  var GEN = {
    cmp: function () {
      var a, b, c;
      do {
        var ip = rint(0, 9), t = pick([0, 0, 1, 1, 2, 3, 3]);
        a = D(ip * 100 + rint(1, 99), 2, true);
        if (t === 0) b = D(ip * 10 + rint(1, 9), 1);
        else if (t === 1) b = D(ip * 1000 + rint(1, 999), 3);
        else if (t === 2) b = D(a.i * 10, 3, true);
        else b = D((ip + pick([-1, 1, 0])) * 100 + rint(1, 99), 2);
        a = norm(a); b = norm(b); c = dcmp(a, b);
      } while (b.i < 0);
      var ans = c < 0 ? "<" : c > 0 ? ">" : "=", k = Math.max(a.k, b.k);
      return { t: "sym", ans: ans, q: function () { return u("dCmp") + " $" + dt(a) + "\\ \\square\\ " + dt(b) + "$"; },
        s: function () { return tex(dt(a, k) + "\\ \\boxed{" + ans + "}\\ " + dt(b, k), true); } };
    },
    round: function () {
      var k = rint(0, 2), x = D(rint(0, 99) * 10000 + rint(1, 9999), 4, true), r = rndD(x, k);
      return { t: "dec", ans: r, q: function () { return fill(u("dRound"), { x: "$" + dt(x) + "$", n: ordName(k) }); },
        s: function () { var nx = digs(x)[1][k]; return tex(dt(x) + "\\approx\\boxed{" + dt(r, k) + "}", true) + hint(fill(u("rKeep"), { n: ordName(k), d: "<b>" + nx + "</b>" }) + " " + (+nx >= 5 ? u("rUp") : u("rDown"))); } };
    },
    p10: function () {
      var x = D(rint(1, 9999), rint(0, 3)), op = Math.random() < .5 ? "*" : ":", p = rint(1, 3), r = op === "*" ? dmul(x, N(p10(p))) : D(x.i, x.k + p);
      return { t: "dec", ans: r, q: function () { return u("dCalc") + " $" + dt(x) + (op === "*" ? "\\cdot " : ":") + ft(p10(p)) + "$"; },
        s: function () { return tex(dt(x) + (op === "*" ? "\\cdot " : ":") + ft(p10(p)) + "=\\boxed{" + dt(r) + "}", true) + hint(u(op === "*" ? "pRight" : "pLeft").replace("{p}", p)); } };
    },
    ops: function () {
      var op = pick(["+", "-", "*"]), a, b, r;
      if (op === "*") { a = D(rint(2, 99), rint(1, 2)); b = Math.random() < .4 ? N(rint(2, 9)) : D(rint(2, 19), rint(1, 2)); r = dmul(a, b); }
      else { a = rdD(30, rint(1, 3)); b = rdD(20, rint(1, 3)); if (op === "-" && dcmp(a, b) < 0) { var t = a; a = b; b = t; } a = norm(a); b = norm(b); r = op === "+" ? dadd(a, b) : dsub(a, b); }
      a = norm(a); b = norm(b);
      return { t: "dec", ans: r, q: function () { return u("dCalc") + " $" + dt(a) + (op === "*" ? "\\cdot " : op) + dt(b) + "$"; },
        s: function () { return op === "*" ? tex(ft(a.i) + "\\cdot " + ft(b.i) + "=" + ft(a.i * b.i) + ",\\ " + a.k + "+" + b.k + "=" + (a.k + b.k) + "\\ \\text{dec.}\\ \\Rightarrow\\ \\boxed{" + dt(r) + "}", true) : colAdd(a, b, op, r); } };
    },
    div: function () {
      var b, q, a;
      do { b = D(rint(2, 60), pick([0, 1, 1, 2])); q = D(rint(2, 250), pick([0, 1, 2])); a = dmul(b, q); } while (a.k > 3 || dcmp(b, N(1)) === 0);
      return { t: "dec", ans: q, q: function () { return u("dCalc") + " $" + dt(a) + ":" + dt(b) + "$"; },
        s: function () { var m = b.k, A = dmul(a, N(p10(m))); return tex((m ? dt(a) + ":" + dt(b) + "=" + dt(A) + ":" + ft(b.i) + "=" : "") + "\\boxed{" + dt(q) + "}", true) + hint(u("check") + " " + tex(dt(b) + "\\cdot " + dt(q) + "=" + dt(a))); } };
    },
    fd: function () {
      if (Math.random() < .5) {
        var x = D(rint(1, 999), rint(1, 3)), f = rat(x.i, p10(x.k));
        if (f.d === p10(x.k) && Math.random() < .7) return GEN.fd();
        return { t: "frac", irr: true, ans: f, q: function () { return fill(u("dToF"), { x: "$" + dt(x) + "$" }); },
          s: function () { return tex(dt(x) + "=" + frac(ft(x.i), ft(p10(x.k))) + "=\\boxed{" + fr(f) + "}", true); } };
      }
      var d = pick([2, 4, 5, 8, 10, 20, 25, 40, 50]), n = rint(1, 3 * d), g = rat(n, d), L = ldiv(n, d, 6), v = D(parseInt(L.q + L.f, 10), L.f.length);
      if (g.d === 1) return GEN.fd();
      return { t: "dec", ans: v, q: function () { return fill(u("dToD"), { f: "$" + frac(n, d) + "$" }); },
        s: function () { return tex(frac(n, d) + "=" + n + ":" + d + "=\\boxed{" + dt(v) + "}", true); } };
    },
    prop: function () {
      var a = rint(1, 9), b = rint(2, 9), m = pick([N(2), N(3), N(4), N(5), D(15, 1), D(25, 1), N(6)]), c = dmul(N(a), m), d = dmul(N(b), m);
      if (a === b) return GEN.prop();
      var v = [N(a), N(b), c, d], pos = rint(0, 3), ans = v[pos];
      var T = function (j) { return j === pos ? "x" : dt(v[j]); };
      return { t: "dec", ans: ans, q: function () { return u("dX") + " $" + frac(T(0), T(1)) + "=" + frac(T(2), T(3)) + "$"; },
        s: function () { return tex(frac(dt(v[0]), dt(v[1])) + "=" + frac(dt(v[2]), dt(v[3])) + "\\qquad x=\\boxed{" + dt(ans) + "}", true) + hint(tex(dt(v[0]) + "\\cdot " + dt(v[3]) + "=" + dt(v[1]) + "\\cdot " + dt(v[2]) + "=" + dt(dmul(v[0], v[3])))); } };
    },
    r3: function () {
      var t = Math.random() < .5 ? "d" : "i", T = pick(R3T[t]), a, b, c, ans;
      if (t === "d") { a = rint(2, 9); var un = D(rint(30, 990), 2); b = dmul(N(a), un); do { c = rint(2, 15); } while (c === a); ans = dmul(N(c), un); }
      else {
        var P; do { a = rint(2, 12); b = N(rint(2, 20)); P = a * b.i; c = pick([2, 3, 4, 5, 6, 8, 10, 12, 15, 20].filter(function (x) { return x !== a && P % x === 0; })); } while (!c);
        ans = N(P / c);
      }
      return { t: "dec", ans: ans, q: function () { return fill(T[lang] || T.va, { a: a, b: "$" + dt(b, T.u === "€" && b.k ? 2 : 0) + "$", c: c }); },
        s: function () { return tex(t === "d" ? "x=" + frac(dt(b) + "\\cdot " + c, a) + "=\\boxed{" + dt(ans) + "}" : "x=" + frac(a + "\\cdot " + dt(b), c) + "=\\boxed{" + dt(ans) + "}", true) + hint(u(t === "d" ? "r3D" : "r3I")); } };
    },
    pct: function () {
      var k = rint(0, 2);
      if (k === 0) {
        var p = pick([N(5), N(10), N(12), N(15), N(20), N(25), N(30), N(40), N(60), N(75), N(80), D(25, 1), D(75, 1)]), n = N(rint(2, 60) * 10), a = dmul(n, shiftD(p, 2));
        return { t: "dec", ans: a, q: function () { return fill(u("dPct"), { p: dt(p), n: dt(n) }); }, s: function () { return tex(dt(n) + "\\cdot " + dt(shiftD(p, 2)) + "=\\boxed{" + dt(a) + "}", true); } };
      }
      if (k === 1) {
        var n1 = pick([20, 25, 40, 50, 80, 200, 250, 400, 500]), st = n1 / gcd(100, n1), a1 = st * rint(1, Math.floor((n1 - 1) / st)), pc = a1 * 100 / n1;
        return { t: "dec", ans: N(pc), q: function () { return fill(u("dPctW"), { a: ft(a1), n: ft(n1) }); }, s: function () { return tex(frac(a1, n1) + "=" + dt(D(pc, 2)) + "=\\boxed{" + pc + "\\,\\%}", true); } };
      }
      var p2 = pick([5, 10, 20, 25, 40, 50, 75, 30]), n2 = rint(2, 40) * 20, a2 = dmul(N(n2), D(p2, 2));
      return { t: "dec", ans: N(n2), q: function () { return fill(u("dPctT"), { p: p2, a: dt(a2) }); }, s: function () { return tex(dt(a2) + ":" + dt(D(p2, 2)) + "=\\boxed{" + ft(n2) + "}", true); } };
    },
    var: function () {
      var up = Math.random() < .45, p = pick(up ? [4, 10, 15, 20, 21, 25, 30, 50] : [5, 10, 12, 15, 20, 25, 30, 40, 50]), q = N(rint(2, 60) * pick([5, 10, 4])), idx = up ? dadd(N(1), D(p, 2)) : dsub(N(1), D(p, 2)), f = dmul(q, idx);
      if (Math.random() < .3) return { t: "dec", ans: q, q: function () { return fill(u(up ? "dVarIu" : "dVarId"), { p: p, f: dt(f, f.k ? 2 : 0) }); }, s: function () { return tex(dt(f) + ":" + dt(idx) + "=\\boxed{" + dt(q) + "}", true); } };
      return { t: "dec", ans: f, q: function () { return fill(u(up ? "dVarU" : "dVarD"), { p: p, q: dt(q) }); }, s: function () { return tex(dt(q) + "\\cdot " + dt(idx) + "=\\boxed{" + dt(f) + "}", true); } };
    }
  };
  function wDrill(w) {
    var kind = w.dataset.kind, q = GEN[kind](), done = false, res = 0, ok = 0, tot = 0;
    var dqEl = w.querySelector(".dq"), inp = w.querySelector(".tin"), info = w.querySelector(".info"), sc = w.querySelector(".dscore");
    function paint() {
      dqEl.innerHTML = rtex(q.q()); sc.textContent = tot ? "✓ " + ok + " / " + tot : "";
      if (done) info.innerHTML = (res === 1 ? '<span class="ok">✓ ' + u("right") + "</span>" : '<span class="ko">✗ ' + u(res === 2 ? "notIrr" : "wrong") + "</span>") + '<div class="dsol">' + q.s() + "</div>";
    }
    function check() {
      if (done) return;
      var raw = inp.value.trim(), good;
      if (q.t === "sym") {
        if (!/^[<>=]$/.test(raw)) { info.innerHTML = warn("sym"); return; }
        good = raw === q.ans ? 1 : 0;
      } else if (q.t === "frac") {
        var f = pfrac(raw);
        if (!f || !f.d) { info.innerHTML = warn("writeF"); return; }
        good = rcmp(f, q.ans) === 0 ? 1 : 0;
        if (good && q.irr) { var g = rat(f.n, f.d); if (g.n !== f.n || g.d !== f.d) good = 2; }
      } else {
        var x = pdec(raw);
        if (!x) { info.innerHTML = warn("writeD"); return; }
        good = dcmp(x, q.ans) === 0 ? 1 : 0;
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
    { q: { va: "En $45{,}307$, quant val la xifra 3?", es: "En $45{,}307$, ¿cuánto vale la cifra 3?", en: "In $45{,}307$, what is the digit 3 worth?" },
      o: [{ va: "$3$" }, { va: "$0{,}3$" }, { va: "$0{,}03$" }, { va: "$0{,}003$" }], a: 1,
      e: { va: "És la primera xifra després de la coma: 3 dècimes $=0{,}3$.", es: "Es la primera cifra después de la coma: 3 décimas $=0{,}3$.", en: "It's the first digit after the comma: 3 tenths $=0{,}3$." } },
    { q: { va: "Com s'escriu «cinc unitats i set mil·lèsimes»?", es: "¿Cómo se escribe «cinco unidades y siete milésimas»?", en: "How do you write “five units and seven thousandths”?" },
      o: [{ va: "$5{,}7$" }, { va: "$5{,}07$" }, { va: "$5{,}007$" }, { va: "$5{,}700$" }], a: 2,
      e: { va: "Les mil·lèsimes ocupen el tercer lloc després de la coma: $5{,}007$.", es: "Las milésimas ocupan el tercer lugar después de la coma: $5{,}007$.", en: "Thousandths are the third place after the comma: $5{,}007$." } },
    { q: { va: "Quin nombre és més gran?", es: "¿Qué número es mayor?", en: "Which number is largest?" },
      o: [{ va: "$3{,}48$" }, { va: "$3{,}5$" }, { va: "$3{,}099$" }, { va: "$3{,}409$" }], a: 1,
      e: { va: "Comparem les dècimes: $3{,}5$ en té 5 i els altres, 4 o menys. ($3{,}50>3{,}48$.)", es: "Comparamos las décimas: $3{,}5$ tiene 5 y los demás, 4 o menos. ($3{,}50>3{,}48$.)", en: "Compare the tenths: $3{,}5$ has 5 and the others 4 or fewer. ($3{,}50>3{,}48$.)" } },
    { q: { va: "Arrodonit a les centèsimes, $7{,}2961$ és…", es: "Redondeado a las centésimas, $7{,}2961$ es…", en: "Rounded to hundredths, $7{,}2961$ is…" },
      o: [{ va: "$7{,}29$" }, { va: "$7{,}30$" }, { va: "$7{,}3$" }, { va: "$7{,}296$" }], a: 1,
      e: { va: "La xifra que eliminem és un 6: sumem 1 a les centèsimes, $29+1=30$. S'escriu $7{,}30$ per a indicar que és a les centèsimes.", es: "La cifra que eliminamos es un 6: sumamos 1 a las centésimas, $29+1=30$. Se escribe $7{,}30$ para indicar que es a las centésimas.", en: "The removed digit is 6: add 1 to the hundredths, $29+1=30$. We write $7{,}30$ to show it's to hundredths." } },
    { q: { va: "$2{,}5+0{,}75=$", es: "$2{,}5+0{,}75=$", en: "$2{,}5+0{,}75=$" },
      o: [{ va: "$2{,}80$" }, { va: "$3{,}25$" }, { va: "$0{,}100$" }, { va: "$3{,}2$" }], a: 1,
      e: { va: "Alineem les comes: $2{,}50+0{,}75=3{,}25$.", es: "Alineamos las comas: $2{,}50+0{,}75=3{,}25$.", en: "Line up the commas: $2{,}50+0{,}75=3{,}25$." } },
    { q: { va: "$0{,}4\\cdot0{,}3=$", es: "$0{,}4\\cdot0{,}3=$", en: "$0{,}4\\cdot0{,}3=$" },
      o: [{ va: "$1{,}2$" }, { va: "$0{,}12$" }, { va: "$0{,}012$" }, { va: "$12$" }], a: 1,
      e: { va: "$4\\cdot3=12$ i els factors sumen $1+1=2$ decimals: $0{,}12$.", es: "$4\\cdot3=12$ y los factores suman $1+1=2$ decimales: $0{,}12$.", en: "$4\\cdot3=12$ and the factors have $1+1=2$ decimals: $0{,}12$." } },
    { q: { va: "$3{,}6:100=$", es: "$3{,}6:100=$", en: "$3{,}6:100=$" },
      o: [{ va: "$360$" }, { va: "$0{,}36$" }, { va: "$0{,}036$" }, { va: "$0{,}0036$" }], a: 2,
      e: { va: "Dividir entre 100 és moure la coma 2 llocs a l'esquerra: $0{,}036$.", es: "Dividir entre 100 es mover la coma 2 lugares a la izquierda: $0{,}036$.", en: "Dividing by 100 moves the comma 2 places left: $0{,}036$." } },
    { q: { va: "$4{,}2:0{,}6=$", es: "$4{,}2:0{,}6=$", en: "$4{,}2:0{,}6=$" },
      o: [{ va: "$0{,}7$" }, { va: "$7$" }, { va: "$70$" }, { va: "$2{,}52$" }], a: 1,
      e: { va: "Multipliquem tots dos per 10: $42:6=7$.", es: "Multiplicamos ambos por 10: $42:6=7$.", en: "Multiply both by 10: $42:6=7$." } },
    { q: { va: "Quin decimal correspon a $\\frac{3}{4}$?", es: "¿Qué decimal corresponde a $\\frac{3}{4}$?", en: "Which decimal is $\\frac{3}{4}$?" },
      o: [{ va: "$0{,}34$" }, { va: "$0{,}75$" }, { va: "$1{,}33$" }, { va: "$0{,}43$" }], a: 1,
      e: { va: "$3:4=0{,}75$.", es: "$3:4=0{,}75$.", en: "$3:4=0{,}75$." } },
    { q: { va: "$\\frac{5}{6}=0{,}8333\\ldots$ és un decimal…", es: "$\\frac{5}{6}=0{,}8333\\ldots$ es un decimal…", en: "$\\frac{5}{6}=0{,}8333\\ldots$ is a…" },
      o: [{ va: "exacte", es: "exacto", en: "terminating decimal" }, { va: "periòdic pur", es: "periódico puro", en: "purely recurring decimal" }, { va: "periòdic mixt", es: "periódico mixto", en: "mixed recurring decimal" }], a: 2,
      e: { va: "El 8 no es repeteix (anteperíode) i el 3 sí (període): $0{,}8\\overline{3}$, periòdic mixt.", es: "El 8 no se repite (anteperiodo) y el 3 sí (periodo): $0{,}8\\overline{3}$, periódico mixto.", en: "The 8 doesn't repeat but the 3 does: $0{,}8\\overline{3}$, mixed recurring." } },
    { q: { va: "$0{,}45$ com a fracció irreductible és…", es: "$0{,}45$ como fracción irreducible es…", en: "$0{,}45$ as a fraction in simplest form is…" },
      o: [{ va: "$\\frac{45}{10}$" }, { va: "$\\frac{9}{20}$" }, { va: "$\\frac{45}{100}$" }, { va: "$\\frac{4}{5}$" }], a: 1,
      e: { va: "$0{,}45=\\frac{45}{100}$, i simplificant entre 5: $\\frac{9}{20}$.", es: "$0{,}45=\\frac{45}{100}$, y simplificando entre 5: $\\frac{9}{20}$.", en: "$0{,}45=\\frac{45}{100}$; dividing by 5 gives $\\frac{9}{20}$." } },
    { q: { va: "Si $\\frac{4}{10}=\\frac{x}{25}$, quant val $x$?", es: "Si $\\frac{4}{10}=\\frac{x}{25}$, ¿cuánto vale $x$?", en: "If $\\frac{4}{10}=\\frac{x}{25}$, what is $x$?" },
      o: [{ va: "$19$" }, { va: "$10$" }, { va: "$62{,}5$" }, { va: "$8$" }], a: 1,
      e: { va: "$10\\cdot x=4\\cdot25=100$, així que $x=10$.", es: "$10\\cdot x=4\\cdot25=100$, así que $x=10$.", en: "$10\\cdot x=4\\cdot25=100$, so $x=10$." } },
    { q: { va: "Quina parella de magnituds és <b>inversament</b> proporcional?", es: "¿Qué pareja de magnitudes es <b>inversamente</b> proporcional?", en: "Which pair of quantities is <b>inversely</b> proportional?" },
      o: [{ va: "Kg de pa i preu", es: "Kg de pan y precio", en: "Kg of bread and price" }, { va: "Velocitat i temps d'un mateix trajecte", es: "Velocidad y tiempo de un mismo trayecto", en: "Speed and time for the same journey" },
        { va: "Edat i altura", es: "Edad y altura", en: "Age and height" }, { va: "Costat i perímetre d'un quadrat", es: "Lado y perímetro de un cuadrado", en: "Side and perimeter of a square" }], a: 1,
      e: { va: "Amb el doble de velocitat tardem la meitat: el producte (la distància) es manté.", es: "Con el doble de velocidad tardamos la mitad: el producto (la distancia) se mantiene.", en: "Twice the speed takes half the time: the product (the distance) stays the same." } },
    { q: { va: "5 bolígrafs costen 4 €. Quant costen 8 bolígrafs?", es: "5 bolígrafos cuestan 4 €. ¿Cuánto cuestan 8 bolígrafos?", en: "5 pens cost 4 €. How much do 8 pens cost?" },
      o: [{ va: "$7$ €" }, { va: "$6{,}40$ €" }, { va: "$2{,}50$ €" }, { va: "$10$ €" }], a: 1,
      e: { va: "Un bolígraf: $4:5=0{,}80$ €. Huit: $0{,}80\\cdot8=6{,}40$ €.", es: "Un bolígrafo: $4:5=0{,}80$ €. Ocho: $0{,}80\\cdot8=6{,}40$ €.", en: "One pen: $4:5=0{,}80$ €. Eight: $0{,}80\\cdot8=6{,}40$ €." } },
    { q: { va: "3 obrers fan una paret en 8 hores. Quant tardarien 6 obrers?", es: "3 obreros hacen una pared en 8 horas. ¿Cuánto tardarían 6 obreros?", en: "3 builders put up a wall in 8 hours. How long would 6 builders take?" },
      o: [{ va: "16 h" }, { va: "4 h" }, { va: "11 h" }, { va: "2 h" }], a: 1,
      e: { va: "És inversa: el doble d'obrers, la meitat de temps. $\\frac{3\\cdot8}{6}=4$ h.", es: "Es inversa: el doble de obreros, la mitad de tiempo. $\\frac{3\\cdot8}{6}=4$ h.", en: "It's inverse: twice the builders, half the time. $\\frac{3\\cdot8}{6}=4$ h." } },
    { q: { va: "El $30\\,\\%$ de 70 és…", es: "El $30\\,\\%$ de 70 es…", en: "$30\\%$ of 70 is…" },
      o: [{ va: "$2{,}1$" }, { va: "$21$" }, { va: "$40$" }, { va: "$210$" }], a: 1,
      e: { va: "$70\\cdot0{,}3=21$.", es: "$70\\cdot0{,}3=21$.", en: "$70\\cdot0{,}3=21$." } },
    { q: { va: "Una samarreta de 20 € té un 15 % de descompte. Quant paguem?", es: "Una camiseta de 20 € tiene un 15 % de descuento. ¿Cuánto pagamos?", en: "A 20 € T-shirt has 15% off. How much do we pay?" },
      o: [{ va: "$3$ €" }, { va: "$5$ €" }, { va: "$17$ €" }, { va: "$23$ €" }], a: 2,
      e: { va: "Paguem el 85 %: $20\\cdot0{,}85=17$ €.", es: "Pagamos el 85 %: $20\\cdot0{,}85=17$ €.", en: "We pay 85%: $20\\cdot0{,}85=17$ €." } },
    { q: { va: "Després d'afegir-hi l'IVA del 21 %, un producte costa $60{,}50$ €. Quant costava sense IVA?", es: "Después de añadirle el IVA del 21 %, un producto cuesta $60{,}50$ €. ¿Cuánto costaba sin IVA?", en: "After adding 21% VAT, an item costs $60{,}50$ €. What did it cost before VAT?" },
      o: [{ va: "$47{,}80$ €" }, { va: "$50$ €" }, { va: "$39{,}50$ €" }, { va: "$73{,}21$ €" }], a: 1,
      e: { va: "Dividim entre l'índex: $60{,}50:1{,}21=50$ €. (Restar el 21 % de 60,50 no dona el preu inicial!)", es: "Dividimos entre el índice: $60{,}50:1{,}21=50$ €. (¡Restar el 21 % de 60,50 no da el precio inicial!)", en: "Divide by the multiplier: $60{,}50:1{,}21=50$ €. (Taking 21% off 60.50 does not give the starting price!)" } }
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

  var TITLES = { va: "Proporcionalitat i percentatges. Nombres decimals · FentMates", es: "Proporcionalidad y porcentajes. Números decimales · FentMates", en: "Proportionality and percentages. Decimal numbers · FentMates" };
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
    wPlace(); wZoom(); wRound(); wCol(); wP10(); wDiv(); wFd(); wProp(); wR3(); wKind(); wPct(); wVar();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
    window.FM15 = { pdec: pdec, dt: dt, dmul: dmul, ldiv: ldiv, rndD: rndD, GEN: GEN };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
