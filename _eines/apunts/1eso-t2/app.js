(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1eso-u2-done", NSEC = 10;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", write: "Escriu un nombre natural.",
      relYes: ["<b>{a}</b> és múltiple de <b>{b}</b>", "<b>{b}</b> és divisor de <b>{a}</b>", "<b>{a}</b> és divisible per <b>{b}</b>"],
      relNo: ["<b>{a}</b> no és múltiple de <b>{b}</b>", "<b>{b}</b> no és divisor de <b>{a}</b>", "<b>{a}</b> no és divisible per <b>{b}</b>"],
      relEx: "La divisió és <b>exacta</b> (residu 0):", relIn: "La divisió <b>no</b> és exacta (residu {r}):", relAlso: "Com que {a} = {b} · {q}, també {q} és divisor de {a}.",
      relNear: "Els múltiples de {b} més pròxims a {a} són {m1} i {m2}.", relZero: "El 0 és múltiple de tots els nombres: 0 = {b} · 0.", relB0: "No es pot dividir entre 0: el 0 no és divisor de cap nombre.",
      rows: "Fem files de {b}: n'hi ha {q} de completes", rowsL: " i en sobren {r}.", rowsN: " i no en sobra cap.", row: "fila", left: "sobren", dotsBig: "(El dibuix només es fa fins a 120 punts i files de 12 com a molt.)",
      mBad: "Escriu nombres entre 1 i 50 (el segon és opcional).", mOf: "Múltiples de {n}", mBoth: "Múltiples comuns", mCom: "Múltiples comuns de {n} i {m} fins a 100:",
      mFirst: "El més xicotet (sense el 0) és <b>{l}</b>: és el seu <b>mínim comú múltiple</b> (apartat 2.7).", mNone: "No n'hi ha cap fins a 100: el primer és {l}.", mJump: "Anem saltant de {n} en {n}: cada múltiple és l'anterior més {n}. La llista no s'acaba mai.",
      dvBad: "Escriu un nombre entre 1 i 100 000.", dvDiv: "Divisió", dvRes: "Resultat", dvPair: "Parella", dvStop: "Parem: el quocient ja és menor o igual que el divisor.",
      dvCount: "{n} té <b>{k}</b> divisors.", dvPrime: " Només en té dos: és un nombre <b>primer</b>.", dvOne: " L'1 només té un divisor: ell mateix.", dvSq: " Com que {r} · {r} = {n}, el {r} només el comptem una vegada.",
      dvExact: "(Només mostrem les divisions exactes.)", dvRect: "Rectangles que podem fer amb {n} quadrets:",
      even: "parella", odd: "senar", c2: "Acaba en {d}, que és {p}.", c5: "Acaba en {d}.", mulY: "→ {s} és múltiple de {k}.", mulN: "→ {s} no és múltiple de {k}.",
      c11: "Lloc senar: {o}. Lloc parell: {e}.", m11Y: "→ és 0 o múltiple d'11.", m11N: "→ no és 0 ni múltiple d'11.", yes: "Sí", no: "No",
      posO: "lloc senar", posE: "lloc parell", cAll: "{n} és divisible per: <b>{l}</b>.", cNone: "{n} no és divisible per cap d'aquests nombres.",
      sv0: "Prem «Següent pas» per a començar a garbellar.", sv1: "L'1 no és primer: el ratllem.", svP: "El <b>{p}</b> és primer: l'encerclem i ratllem tots els seus múltiples: {l}…", svA: " (Alguns ja estaven ratllats.)",
      svEnd: "Com que 11 · 11 = 121 ja és més gran que 100, tots els nombres que queden sense ratllar són primers: n'hi ha <b>25</b>.", svTap: "Toca un nombre per a veure'n els divisors.",
      svCell: "<b>{n}</b>: divisors {d} → {t}.", prime: "primer", comp: "compost", neither: "ni primer ni compost",
      prBad: "Escriu un nombre entre 2 i 100 000.", prDiv: "Divisió", prQ: "Quocient", prR: "Residu",
      prYes: "<b>{n}</b> és <b>primer</b>: cap divisió és exacta i, en dividir entre {p}, el quocient ({q}) ja és menor que el divisor.", prTwo: "<b>2</b> és primer: només té els divisors 1 i 2.",
      prNo: "<b>{n}</b> és <b>compost</b>: {n} = {p} · {q}.",
      fBad: "Escriu un nombre entre 2 i 1 000 000.", fPrime: "{n} és primer: la seua descomposició és ell mateix.", f2: "és parell", f3: "xifres: {s}", f5: "acaba en {d}", f11: "criteri de l'11",
      fRule: "Dividim sempre entre el primer més xicotet possible fins a arribar a 1. Els factors repetits s'escriuen com a potència.", fTree: "Partim cada nombre compost en dos factors; les fulles (en cercle) són els primers.",
      gBad: "Escriu nombres entre 1 i 100 000 (el tercer és opcional).", gRuleM: "<b>mcm</b>: factors comuns i no comuns, cadascun amb el <b>major</b> exponent.", gRuleD: "<b>MCD</b>: només els factors comuns, cadascun amb el <b>menor</b> exponent.",
      gNc: "no és comú", gLong: "La llista seria massa llarga ({k} múltiples): millor amb la descomposició.", gComM: "El primer múltiple comú és <b>{l}</b>.", gComD: "Divisors comuns: {l}. El més gran és <b>{g}</b>.",
      gCop: "Com que el MCD és 1, són <b>primers entre si</b>.", gRel: "Comprovació: MCD · mcm = {g} · {l} = {p} = {a} · {b}.", gNum: "Nombre", mcm: "mcm", mcd: "MCD",
      coBad: "Escriu períodes entre 1 i 500 (el tercer és opcional).", coTime: "Escriu l'hora així: 8:00.", un: { min: "min", d: "dies", s: "s" }, every: "cada",
      coRes: "Tornen a coincidir al cap de <b>{l} {u}</b>", coClock: ", és a dir, a les <b>{h}</b>", coAgain: "Després, cada {l} {u}: al cap de {l2}, de {l3}…",
      tBad: "Escriu mesures entre 1 i 2000 cm.", tChips: "Costats possibles (divisors comuns):", tRes: "Rajoles de <b>{d} × {d}</b> cm: {x} en el llarg i {y} en l'ample → <b>{n} rajoles</b>.",
      tMax: "És la rajola més gran possible: {d} = MCD({a}, {b}).", tSmall: "Es pot fer, però no és la més gran: el MCD és {g}.", tOne: "El MCD és 1: només ho podem fer amb rajoles d'1 cm!", tMany: "(Hi ha massa rajoles per a dibuixar-les totes.)",
      dMultN: "Quin és el primer múltiple de {n} més gran que {N}?", dMultC: "Quants múltiples de {n} hi ha entre 1 i {N}?", dMultS: "Hi ha {q} múltiples: de {n} fins a {n} · {q} = {m}.",
      dDivs: "Quants divisors té {n}?", dCrit: "Quina és la xifra més xicoteta que pots posar en el lloc de ■ perquè {x} siga divisible per {k}?",
      dFactN: "Quin nombre té aquesta descomposició?", dFactE: "Quin és l'exponent del {p} en la descomposició de {n}?", dCalc: "Calcula:" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", write: "Escribe un número natural.",
      relYes: ["<b>{a}</b> es múltiplo de <b>{b}</b>", "<b>{b}</b> es divisor de <b>{a}</b>", "<b>{a}</b> es divisible por <b>{b}</b>"],
      relNo: ["<b>{a}</b> no es múltiplo de <b>{b}</b>", "<b>{b}</b> no es divisor de <b>{a}</b>", "<b>{a}</b> no es divisible por <b>{b}</b>"],
      relEx: "La división es <b>exacta</b> (resto 0):", relIn: "La división <b>no</b> es exacta (resto {r}):", relAlso: "Como {a} = {b} · {q}, también {q} es divisor de {a}.",
      relNear: "Los múltiplos de {b} más próximos a {a} son {m1} y {m2}.", relZero: "El 0 es múltiplo de todos los números: 0 = {b} · 0.", relB0: "No se puede dividir entre 0: el 0 no es divisor de ningún número.",
      rows: "Hacemos filas de {b}: hay {q} completas", rowsL: " y sobran {r}.", rowsN: " y no sobra ninguno.", row: "fila", left: "sobran", dotsBig: "(El dibujo solo se hace hasta 120 puntos y filas de 12 como mucho.)",
      mBad: "Escribe números entre 1 y 50 (el segundo es opcional).", mOf: "Múltiplos de {n}", mBoth: "Múltiplos comunes", mCom: "Múltiplos comunes de {n} y {m} hasta 100:",
      mFirst: "El menor (sin el 0) es <b>{l}</b>: es su <b>mínimo común múltiplo</b> (apartado 2.7).", mNone: "No hay ninguno hasta 100: el primero es {l}.", mJump: "Vamos saltando de {n} en {n}: cada múltiplo es el anterior más {n}. La lista no se acaba nunca.",
      dvBad: "Escribe un número entre 1 y 100 000.", dvDiv: "División", dvRes: "Resultado", dvPair: "Pareja", dvStop: "Paramos: el cociente ya es menor o igual que el divisor.",
      dvCount: "{n} tiene <b>{k}</b> divisores.", dvPrime: " Solo tiene dos: es un número <b>primo</b>.", dvOne: " El 1 solo tiene un divisor: él mismo.", dvSq: " Como {r} · {r} = {n}, el {r} solo lo contamos una vez.",
      dvExact: "(Solo mostramos las divisiones exactas.)", dvRect: "Rectángulos que podemos hacer con {n} cuadraditos:",
      even: "par", odd: "impar", c2: "Acaba en {d}, que es {p}.", c5: "Acaba en {d}.", mulY: "→ {s} es múltiplo de {k}.", mulN: "→ {s} no es múltiplo de {k}.",
      c11: "Lugar impar: {o}. Lugar par: {e}.", m11Y: "→ es 0 o múltiplo de 11.", m11N: "→ no es 0 ni múltiplo de 11.", yes: "Sí", no: "No",
      posO: "lugar impar", posE: "lugar par", cAll: "{n} es divisible por: <b>{l}</b>.", cNone: "{n} no es divisible por ninguno de estos números.",
      sv0: "Pulsa «Siguiente paso» para empezar a cribar.", sv1: "El 1 no es primo: lo tachamos.", svP: "El <b>{p}</b> es primo: lo rodeamos y tachamos todos sus múltiplos: {l}…", svA: " (Algunos ya estaban tachados.)",
      svEnd: "Como 11 · 11 = 121 ya es mayor que 100, todos los números que quedan sin tachar son primos: hay <b>25</b>.", svTap: "Toca un número para ver sus divisores.",
      svCell: "<b>{n}</b>: divisores {d} → {t}.", prime: "primo", comp: "compuesto", neither: "ni primo ni compuesto",
      prBad: "Escribe un número entre 2 y 100 000.", prDiv: "División", prQ: "Cociente", prR: "Resto",
      prYes: "<b>{n}</b> es <b>primo</b>: ninguna división es exacta y, al dividir entre {p}, el cociente ({q}) ya es menor que el divisor.", prTwo: "<b>2</b> es primo: solo tiene los divisores 1 y 2.",
      prNo: "<b>{n}</b> es <b>compuesto</b>: {n} = {p} · {q}.",
      fBad: "Escribe un número entre 2 y 1 000 000.", fPrime: "{n} es primo: su descomposición es él mismo.", f2: "es par", f3: "cifras: {s}", f5: "acaba en {d}", f11: "criterio del 11",
      fRule: "Dividimos siempre entre el primo más pequeño posible hasta llegar a 1. Los factores repetidos se escriben como potencia.", fTree: "Partimos cada número compuesto en dos factores; las hojas (en círculo) son los primos.",
      gBad: "Escribe números entre 1 y 100 000 (el tercero es opcional).", gRuleM: "<b>mcm</b>: factores comunes y no comunes, cada uno con el <b>mayor</b> exponente.", gRuleD: "<b>MCD</b>: solo los factores comunes, cada uno con el <b>menor</b> exponente.",
      gNc: "no es común", gLong: "La lista sería demasiado larga ({k} múltiplos): mejor con la descomposición.", gComM: "El primer múltiplo común es <b>{l}</b>.", gComD: "Divisores comunes: {l}. El mayor es <b>{g}</b>.",
      gCop: "Como el MCD es 1, son <b>primos entre sí</b>.", gRel: "Comprobación: MCD · mcm = {g} · {l} = {p} = {a} · {b}.", gNum: "Número", mcm: "mcm", mcd: "MCD",
      coBad: "Escribe periodos entre 1 y 500 (el tercero es opcional).", coTime: "Escribe la hora así: 8:00.", un: { min: "min", d: "días", s: "s" }, every: "cada",
      coRes: "Vuelven a coincidir al cabo de <b>{l} {u}</b>", coClock: ", es decir, a las <b>{h}</b>", coAgain: "Después, cada {l} {u}: al cabo de {l2}, de {l3}…",
      tBad: "Escribe medidas entre 1 y 2000 cm.", tChips: "Lados posibles (divisores comunes):", tRes: "Baldosas de <b>{d} × {d}</b> cm: {x} a lo largo y {y} a lo ancho → <b>{n} baldosas</b>.",
      tMax: "Es la baldosa más grande posible: {d} = MCD({a}, {b}).", tSmall: "Se puede hacer, pero no es la mayor: el MCD es {g}.", tOne: "El MCD es 1: ¡solo lo podemos hacer con baldosas de 1 cm!", tMany: "(Hay demasiadas baldosas para dibujarlas todas.)",
      dMultN: "¿Cuál es el primer múltiplo de {n} mayor que {N}?", dMultC: "¿Cuántos múltiplos de {n} hay entre 1 y {N}?", dMultS: "Hay {q} múltiplos: de {n} hasta {n} · {q} = {m}.",
      dDivs: "¿Cuántos divisores tiene {n}?", dCrit: "¿Cuál es la cifra más pequeña que puedes poner en el lugar de ■ para que {x} sea divisible por {k}?",
      dFactN: "¿Qué número tiene esta descomposición?", dFactE: "¿Cuál es el exponente del {p} en la descomposición de {n}?", dCalc: "Calcula:" },
    en: { next: "Next step", all: "Show all", reset: "Hide steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Toggle light and dark mode", write: "Type a whole number.",
      relYes: ["<b>{a}</b> is a multiple of <b>{b}</b>", "<b>{b}</b> is a divisor of <b>{a}</b>", "<b>{a}</b> is divisible by <b>{b}</b>"],
      relNo: ["<b>{a}</b> is not a multiple of <b>{b}</b>", "<b>{b}</b> is not a divisor of <b>{a}</b>", "<b>{a}</b> is not divisible by <b>{b}</b>"],
      relEx: "The division is <b>exact</b> (remainder 0):", relIn: "The division is <b>not</b> exact (remainder {r}):", relAlso: "Since {a} = {b} · {q}, {q} is also a divisor of {a}.",
      relNear: "The multiples of {b} closest to {a} are {m1} and {m2}.", relZero: "0 is a multiple of every number: 0 = {b} · 0.", relB0: "You can't divide by 0: 0 is not a divisor of any number.",
      rows: "Make rows of {b}: there are {q} full rows", rowsL: " and {r} left over.", rowsN: " and none left over.", row: "row", left: "left", dotsBig: "(The picture is only drawn up to 120 dots and rows of at most 12.)",
      mBad: "Type numbers from 1 to 50 (the second one is optional).", mOf: "Multiples of {n}", mBoth: "Common multiples", mCom: "Common multiples of {n} and {m} up to 100:",
      mFirst: "The smallest (not counting 0) is <b>{l}</b>: their <b>least common multiple</b> (section 2.7).", mNone: "There are none up to 100: the first is {l}.", mJump: "We jump in steps of {n}: each multiple is the previous one plus {n}. The list never ends.",
      dvBad: "Type a number from 1 to 100,000.", dvDiv: "Division", dvRes: "Result", dvPair: "Pair", dvStop: "Stop: the quotient is now less than or equal to the divisor.",
      dvCount: "{n} has <b>{k}</b> divisors.", dvPrime: " Only two: it is a <b>prime</b> number.", dvOne: " 1 has only one divisor: itself.", dvSq: " Since {r} · {r} = {n}, we count {r} only once.",
      dvExact: "(Only the exact divisions are shown.)", dvRect: "Rectangles we can make with {n} squares:",
      even: "even", odd: "odd", c2: "It ends in {d}, which is {p}.", c5: "It ends in {d}.", mulY: "→ {s} is a multiple of {k}.", mulN: "→ {s} is not a multiple of {k}.",
      c11: "Odd places: {o}. Even places: {e}.", m11Y: "→ it's 0 or a multiple of 11.", m11N: "→ it's neither 0 nor a multiple of 11.", yes: "Yes", no: "No",
      posO: "odd place", posE: "even place", cAll: "{n} is divisible by: <b>{l}</b>.", cNone: "{n} is not divisible by any of these numbers.",
      sv0: "Press “Next step” to start sieving.", sv1: "1 is not prime: cross it out.", svP: "<b>{p}</b> is prime: circle it and cross out all its multiples: {l}…", svA: " (Some were already crossed out.)",
      svEnd: "Since 11 · 11 = 121 is already bigger than 100, every number left uncrossed is prime: there are <b>25</b>.", svTap: "Tap a number to see its divisors.",
      svCell: "<b>{n}</b>: divisors {d} → {t}.", prime: "prime", comp: "composite", neither: "neither prime nor composite",
      prBad: "Type a number from 2 to 100,000.", prDiv: "Division", prQ: "Quotient", prR: "Remainder",
      prYes: "<b>{n}</b> is <b>prime</b>: no division is exact and, dividing by {p}, the quotient ({q}) is already less than the divisor.", prTwo: "<b>2</b> is prime: its only divisors are 1 and 2.",
      prNo: "<b>{n}</b> is <b>composite</b>: {n} = {p} · {q}.",
      fBad: "Type a number from 2 to 1,000,000.", fPrime: "{n} is prime: its factorisation is just itself.", f2: "even", f3: "digits: {s}", f5: "ends in {d}", f11: "rule for 11",
      fRule: "Always divide by the smallest possible prime until you reach 1. Repeated factors are written as powers.", fTree: "Split each composite number into two factors; the leaves (circled) are the primes.",
      gBad: "Type numbers from 1 to 100,000 (the third one is optional).", gRuleM: "<b>lcm</b>: every factor, common or not, each with its <b>highest</b> exponent.", gRuleD: "<b>gcd</b>: only the common factors, each with its <b>lowest</b> exponent.",
      gNc: "not common", gLong: "The list would be too long ({k} multiples): better use factorisation.", gComM: "The first common multiple is <b>{l}</b>.", gComD: "Common divisors: {l}. The largest is <b>{g}</b>.",
      gCop: "Since the gcd is 1, they are <b>coprime</b>.", gRel: "Check: gcd · lcm = {g} · {l} = {p} = {a} · {b}.", gNum: "Number", mcm: "lcm", mcd: "gcd",
      coBad: "Type periods from 1 to 500 (the third one is optional).", coTime: "Type the time like this: 8:00.", un: { min: "min", d: "days", s: "s" }, every: "every",
      coRes: "They coincide again after <b>{l} {u}</b>", coClock: ", that is, at <b>{h}</b>", coAgain: "After that, every {l} {u}: after {l2}, {l3}…",
      tBad: "Type lengths from 1 to 2000 cm.", tChips: "Possible sides (common divisors):", tRes: "<b>{d} × {d}</b> cm tiles: {x} along the length and {y} along the width → <b>{n} tiles</b>.",
      tMax: "It's the biggest possible tile: {d} = gcd({a}, {b}).", tSmall: "It works, but it isn't the biggest: the gcd is {g}.", tOne: "The gcd is 1: we can only do it with 1 cm tiles!", tMany: "(Too many tiles to draw them all.)",
      dMultN: "What is the first multiple of {n} greater than {N}?", dMultC: "How many multiples of {n} are there from 1 to {N}?", dMultS: "There are {q} multiples: from {n} up to {n} · {q} = {m}.",
      dDivs: "How many divisors does {n} have?", dCrit: "What is the smallest digit you can put in place of ■ so that {x} is divisible by {k}?",
      dFactN: "Which number has this factorisation?", dFactE: "What is the exponent of {p} in the factorisation of {n}?", dCalc: "Work out:" }
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
    s = String(s).trim().replace(/[\s  ]/g, "");
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
  function fh(x) { return fcore(x, " "); }
  function ft(x) { return fcore(x, "\\,"); }
  function warn(k) { return '<span class="warn">' + u(k) + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function hint(s) { return '<div class="hint">' + s + "</div>"; }

  /* ---------- aritmètica ---------- */
  function isPrime(n) { if (n < 2) return false; for (var i = 2; i * i <= n; i++) if (n % i === 0) return false; return true; }
  function factor(n) {
    var f = [], p = 2;
    while (n > 1 && p * p <= n) { var e = 0; while (n % p === 0) { n /= p; e++; } if (e) f.push([p, e]); p++; }
    if (n > 1) f.push([n, 1]);
    return f;
  }
  function ftex(f) { return f.length ? f.map(function (x) { return x[0] + (x[1] > 1 ? "^{" + x[1] + "}" : ""); }).join("\\cdot ") : "1"; }
  function divisors(n) { var a = [], b = []; for (var i = 1; i * i <= n; i++) if (n % i === 0) { a.push(i); if (i * i !== n) b.unshift(n / i); } return a.concat(b); }
  function gcd(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }
  function lcm(a, b) { return a / gcd(a, b) * b; }
  function digitSum(s) { var t = 0; for (var i = 0; i < s.length; i++) t += +s.charAt(i); return t; }
  function altSums(s) { var o = 0, e = 0; for (var i = 0; i < s.length; i++) { var d = +s.charAt(s.length - 1 - i); if (i % 2) e += d; else o += d; } return [o, e]; }
  function list(a) { return a.map(fh).join(", "); }
  function readNums(w, keys, max) {
    var v = [];
    for (var i = 0; i < keys.length; i++) {
      var raw = w.querySelector('[data-k="' + keys[i] + '"]').value.trim();
      if (!raw && i >= 2) continue;
      var x = pnat(raw);
      if (isNaN(x) || x < 1 || x > max) return null;
      v.push(x);
    }
    return v;
  }
  function quickFill(w, keys, render) {
    w.querySelectorAll(".quick button").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = b.dataset.b.split(/[,:]/);
        keys.forEach(function (k, i) { var el = w.querySelector('[data-k="' + k + '"]'); if (el) el.value = p[i] || ""; });
        render();
      });
    });
  }

  /* ---------- giny: relació de divisibilitat ---------- */
  function wRel() {
    var w = document.getElementById("w-rel"); if (!w) return;
    var A = w.querySelector('[data-k="a"]'), B = w.querySelector('[data-k="b"]'), info = w.querySelector(".info"), dots = w.querySelector(".dots");
    function render() {
      var a = pnat(A.value), b = pnat(B.value);
      dots.innerHTML = "";
      if (isNaN(a) || isNaN(b) || a > 999999999 || b > 999999999) { info.innerHTML = warn("write"); return; }
      if (b === 0) { info.innerHTML = warn("relB0"); return; }
      var q = Math.floor(a / b), r = a % b, o = { a: fh(a), b: fh(b), q: fh(q), r: fh(r) }, h;
      if (!r) {
        h = "<div>" + fill(u("relEx"), o) + "</div>" + tex(ft(a) + "=" + ft(b) + "\\cdot " + ft(q), true) +
          '<ul class="rel ok">' + u("relYes").map(function (s) { return "<li>✓ " + fill(s, o) + "</li>"; }).join("") + "</ul>" +
          (a === 0 ? hint(fill(u("relZero"), o)) : q !== b ? hint(fill(u("relAlso"), o)) : "");
      } else {
        h = "<div>" + fill(u("relIn"), o) + "</div>" + tex(ft(a) + "=" + ft(b) + "\\cdot " + ft(q) + "+" + ft(r), true) +
          '<ul class="rel ko">' + u("relNo").map(function (s) { return "<li>✗ " + fill(s, o) + "</li>"; }).join("") + "</ul>" +
          hint(fill(u("relNear"), { a: fh(a), b: fh(b), m1: fh(b * q), m2: fh(b * (q + 1)) }));
      }
      info.innerHTML = h;
      if (a > 0 && a <= 120 && b <= 12) {
        var d = "";
        for (var g = 0; g < q; g++) { var row = ""; for (var i = 0; i < b; i++) row += "<i></i>"; d += '<div class="drow"><span class="dl">' + u("row") + " " + (g + 1) + "</span>" + row + "</div>"; }
        if (r) { var rr = ""; for (var j = 0; j < r; j++) rr += '<i class="x"></i>'; d += '<div class="drow"><span class="dl">' + u("left") + "</span>" + rr + "</div>"; }
        dots.innerHTML = d + hint(fill(u("rows"), o) + (r ? fill(u("rowsL"), o) : u("rowsN")));
      } else if (a > 0) dots.innerHTML = hint(u("dotsBig"));
    }
    [A, B].forEach(function (x) { x.addEventListener("input", render); });
    quickFill(w, ["a", "b"], render);
    onLang(render);
  }

  /* ---------- giny: múltiples (taula del 100) ---------- */
  function wMult() {
    var w = document.getElementById("w-mult"); if (!w) return;
    var N = w.querySelector('[data-k="n"]'), M = w.querySelector('[data-k="m"]'), grid = w.querySelector(".hgrid"), leg = w.querySelector(".legend"), info = w.querySelector(".info");
    function render() {
      var n = pnat(N.value), mr = M.value.trim(), m = mr ? pnat(mr) : 0;
      if (isNaN(n) || n < 1 || n > 50 || isNaN(m) || m > 50) { grid.innerHTML = leg.innerHTML = ""; info.innerHTML = warn("mBad"); return; }
      var h = "";
      for (var k = 1; k <= 100; k++) {
        var a = k % n === 0, b = m && k % m === 0;
        h += '<span class="' + (a && b ? "ab" : a ? "a" : b ? "b" : "") + '">' + k + "</span>";
      }
      grid.innerHTML = h;
      leg.innerHTML = '<span><i class="a"></i>' + fill(u("mOf"), { n: n }) + "</span>" + (m ? '<span><i class="b"></i>' + fill(u("mOf"), { n: m }) + '</span><span><i class="ab"></i>' + u("mBoth") + "</span>" : "");
      function ml(x) { var t = []; for (var i = 0; i <= 10; i++) t.push(ft(x * i)); return "\\text{M}(" + x + ")=\\{" + t.join(",\\ ") + ",\\ \\ldots\\}"; }
      var s = tex(ml(n), true) + (m ? tex(ml(m), true) : "") + hint(fill(u("mJump"), { n: n }));
      if (m) {
        var l = lcm(n, m), c = [];
        for (var x = l; x <= 100; x += l) c.push(x);
        s += "<div>" + fill(u("mCom"), { n: n, m: m }) + " <b>" + (c.length ? list(c) : "—") + "</b></div><div>" + (c.length ? fill(u("mFirst"), { l: fh(l) }) : fill(u("mNone"), { l: fh(l) })) + "</div>";
      }
      info.innerHTML = s;
    }
    [N, M].forEach(function (x) { x.addEventListener("input", render); });
    quickFill(w, ["n", "m"], render);
    onLang(render);
  }

  /* ---------- giny: divisors ---------- */
  function wDivs() {
    var w = document.getElementById("w-divs"); if (!w) return;
    var inp = w.querySelector(".tin"), tb = w.querySelector(".dvt"), rc = w.querySelector(".rects"), info = w.querySelector(".info");
    function render() {
      var n = pnat(inp.value);
      tb.innerHTML = rc.innerHTML = "";
      if (isNaN(n) || n < 1 || n > 100000) { info.innerHTML = warn("dvBad"); return; }
      var all = Math.sqrt(n) <= 30, h = "", i;
      for (i = 1; i * i <= n; i++) {
        var q = Math.floor(n / i), r = n % i;
        if (r && !all) continue;
        h += "<tr" + (r ? ' class="no"' : "") + "><td>" + tex(ft(n) + ":" + i) + "</td><td>" + (r ? tex(ft(q) + ",\\ r=" + r) : tex(ft(q))) + "</td><td>" + (r ? "✗" : tex(i + "\\cdot " + ft(q))) + "</td></tr>";
      }
      h += '<tr class="stop"><td>' + tex(ft(n) + ":" + i) + "</td><td>" + tex(ft(Math.floor(n / i)) + (n % i ? ",\\ r=" + ft(n % i) : "")) + '</td><td class="l">' + u("dvStop") + "</td></tr>";
      tb.innerHTML = '<table class="data dvtab"><thead><tr><th>' + u("dvDiv") + "</th><th>" + u("dvRes") + "</th><th>" + u("dvPair") + "</th></tr></thead><tbody>" + h + "</tbody></table>" + (all ? "" : hint(u("dvExact")));
      var d = divisors(n), r0 = Math.round(Math.sqrt(n));
      info.innerHTML = tex("\\text{Div}(" + ft(n) + ")=\\{" + d.map(ft).join(",\\ ") + "\\}", true) +
        "<div>" + fill(u("dvCount"), { n: fh(n), k: d.length }) + (n === 1 ? u("dvOne") : d.length === 2 ? u("dvPrime") : r0 * r0 === n ? fill(u("dvSq"), { r: r0, n: fh(n) }) : "") + "</div>";
      if (n <= 60 && n > 1) {
        var s = "";
        d.forEach(function (a) {
          var b = n / a; if (a > b) return;
          var c = Math.max(4, Math.min(12, Math.floor(260 / b))), g = "";
          for (var y = 0; y < a; y++) for (var x = 0; x < b; x++) g += '<rect x="' + (x * c + 1) + '" y="' + (y * c + 1) + '" width="' + (c - 1.5) + '" height="' + (c - 1.5) + '" rx="1.5"/>';
          s += '<figure><svg viewBox="0 0 ' + (b * c + 2) + " " + (a * c + 2) + '" style="width:' + (b * c + 2) + 'px">' + g + "</svg><figcaption>" + a + " × " + b + "</figcaption></figure>";
        });
        rc.innerHTML = hint(fill(u("dvRect"), { n: n })) + '<div class="rgal">' + s + "</div>";
      }
    }
    inp.addEventListener("input", render);
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.b; render(); }); });
    onLang(render);
  }

  /* ---------- giny: criteris de divisibilitat ---------- */
  function critInfo(n, k) {
    var s = String(n), last = +s.charAt(s.length - 1), ok = n % k === 0, t;
    if (k === 2) t = fill(u("c2"), { d: last, p: u(last % 2 ? "odd" : "even") });
    else if (k === 5) t = fill(u("c5"), { d: last });
    else if (k === 3 || k === 9) { var S = digitSum(s); t = tex(s.length > 1 ? s.split("").join("+") + "=" + S : String(S)) + " " + fill(u(S % k ? "mulN" : "mulY"), { s: S, k: k }); }
    else { var a = altSums(s), hi = Math.max(a[0], a[1]), lo = Math.min(a[0], a[1]); t = fill(u("c11"), { o: a[0], e: a[1] }) + " " + tex(hi + "-" + lo + "=" + (hi - lo)) + " " + u(ok ? "m11Y" : "m11N"); }
    return { ok: ok, t: t };
  }
  function wCrit() {
    var w = document.getElementById("w-crit"); if (!w) return;
    var inp = w.querySelector(".tin"), dg = w.querySelector(".cdig"), cc = w.querySelector(".ccards"), info = w.querySelector(".info");
    function render() {
      var n = pnat(inp.value);
      if (isNaN(n) || n < 1 || n > 999999999) { dg.innerHTML = cc.innerHTML = ""; info.innerHTML = warn("write"); return; }
      var s = String(n), h = "";
      for (var i = 0; i < s.length; i++) { var pos = s.length - i; h += '<span class="' + (pos % 2 ? "po" : "pe") + '">' + s.charAt(i) + "<small>" + pos + "</small></span>"; }
      dg.innerHTML = '<div class="cd">' + h + '</div><div class="clegend"><span class="po">' + u("posO") + '</span><span class="pe">' + u("posE") + "</span></div>";
      var yes = [];
      cc.innerHTML = [2, 3, 5, 9, 11].map(function (k) {
        var c = critInfo(n, k); if (c.ok) yes.push(k);
        return '<div class="card ' + (c.ok ? "ok" : "ko") + '"><h4>÷ ' + k + '</h4><div class="verd">' + (c.ok ? "✓ " + u("yes") : "✗ " + u("no")) + '</div><div class="why">' + c.t + "</div></div>";
      }).join("");
      info.innerHTML = yes.length ? fill(u("cAll"), { n: fh(n), l: yes.join(", ") }) : fill(u("cNone"), { n: fh(n) });
    }
    inp.addEventListener("input", render);
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.b; render(); }); });
    onLang(render);
  }

  /* ---------- giny: garbell d'Eratòstenes ---------- */
  function wSieve() {
    var w = document.getElementById("w-sieve"); if (!w) return;
    var grid = w.querySelector(".sieve"), info = w.querySelector(".info"), st = 0, sel = null, PS = [2, 3, 5, 7];
    var bn = w.querySelector('[data-a="next"]'), ba = w.querySelector('[data-a="all"]'), br = w.querySelector('[data-a="reset"]');
    function spf(k) { for (var i = 0; i < PS.length; i++) if (k % PS[i] === 0 && k !== PS[i]) return i; return -1; }
    function render() {
      var h = "";
      for (var k = 1; k <= 100; k++) {
        var c = "", f = spf(k);
        if (k === 1) { if (st >= 1) c = "x" + (st === 1 ? " new" : ""); }
        else if (f >= 0) { if (st >= f + 2) c = "x c" + PS[f] + (st === f + 2 ? " new" : ""); }
        else if (PS.indexOf(k) >= 0) { if (st >= PS.indexOf(k) + 2) c = "p c" + k; }
        else if (st >= 6) c = "p";
        h += '<button type="button" class="' + c + (sel === k ? " sel" : "") + '" data-n="' + k + '">' + k + "</button>";
      }
      grid.innerHTML = h;
      grid.querySelectorAll("button").forEach(function (b) { b.addEventListener("click", function () { sel = +b.dataset.n; render(); }); });
      var t;
      if (st === 0) t = u("sv0"); else if (st === 1) t = u("sv1"); else if (st === 6) t = u("svEnd");
      else { var p = PS[st - 2], l = []; for (var j = 2; j <= 5; j++) l.push(p * j); t = fill(u("svP"), { p: p, l: l.join(", ") }) + (p > 2 ? u("svA") : ""); }
      var c2 = "";
      if (sel) { var d = divisors(sel); c2 = fill(u("svCell"), { n: sel, d: d.join(", "), t: u(sel === 1 ? "neither" : d.length === 2 ? "prime" : "comp") }); }
      info.innerHTML = "<div>" + t + "</div>" + hint(c2 || u("svTap"));
      bn.textContent = u("next") + " →"; bn.disabled = st >= 6; ba.textContent = u("all");
    }
    bn.addEventListener("click", function () { if (st < 6) st++; render(); });
    ba.addEventListener("click", function () { st = 6; render(); });
    br.addEventListener("click", function () { st = 0; sel = null; render(); });
    onLang(render);
  }

  /* ---------- giny: és primer? ---------- */
  function wPrime() {
    var w = document.getElementById("w-prime"); if (!w) return;
    var inp = w.querySelector(".tin"), tb = w.querySelector(".pvt2"), info = w.querySelector(".info");
    function render() {
      var n = pnat(inp.value);
      tb.innerHTML = "";
      if (isNaN(n) || n < 2 || n > 100000) { info.innerHTML = warn("prBad"); return; }
      if (n === 2) { info.innerHTML = u("prTwo"); return; }
      var rows = "", res = "";
      for (var p = 2; ; p++) {
        if (!isPrime(p)) continue;
        var q = Math.floor(n / p), r = n % p;
        rows += "<tr" + (!r ? ' class="hit"' : p * p > n ? ' class="stop"' : "") + "><td>" + tex(ft(n) + ":" + p) + "</td><td>" + ft(q) + "</td><td>" + ft(r) + "</td><td>" + (!r ? "✓" : p * p > n ? tex(ft(q) + "\\lt " + p) : "✗") + "</td></tr>";
        if (!r) { res = fill(u("prNo"), { n: fh(n), p: p, q: fh(q) }); break; }
        if (p * p > n) { res = fill(u("prYes"), { n: fh(n), p: p, q: fh(q) }); break; }
      }
      tb.innerHTML = '<table class="data prtab"><thead><tr><th>' + u("prDiv") + "</th><th>" + u("prQ") + "</th><th>" + u("prR") + "</th><th></th></tr></thead><tbody>" + rows + "</tbody></table>";
      info.innerHTML = res;
    }
    inp.addEventListener("input", render);
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.b; render(); }); });
    onLang(render);
  }

  /* ---------- giny: factorització ---------- */
  function why(m, p) {
    var s = String(m);
    if (p === 2) return u("f2");
    if (p === 3) return fill(u("f3"), { s: s.length > 1 ? s.split("").join("+") + "=" + digitSum(s) : s });
    if (p === 5) return fill(u("f5"), { d: s.charAt(s.length - 1) });
    if (p === 11) return u("f11");
    return "";
  }
  function ftree(m) {
    if (m < 4 || isPrime(m)) return { v: m };
    var d = 1; for (var i = 2; i * i <= m; i++) if (m % i === 0) d = i;
    return { v: m, k: [ftree(d), ftree(m / d)] };
  }
  function treeSVG(t) {
    var leaf = 0, depth = 0, W = 50, H = 62, out = "";
    (function lay(n, dpt) {
      n.y = 24 + dpt * H; depth = Math.max(depth, dpt);
      if (!n.k) { n.x = 30 + leaf++ * W; return; }
      lay(n.k[0], dpt + 1); lay(n.k[1], dpt + 1); n.x = (n.k[0].x + n.k[1].x) / 2;
    })(t, 0);
    (function draw(n) {
      if (n.k) n.k.forEach(function (c) { out += '<line class="tr-l" x1="' + n.x + '" y1="' + (n.y + 13) + '" x2="' + c.x + '" y2="' + (c.y - 15) + '"/>'; draw(c); });
      out += n.k ? '<text class="tr-c" x="' + n.x + '" y="' + (n.y + 6) + '" text-anchor="middle">' + fh(n.v) + "</text>"
        : '<circle class="tr-p" cx="' + n.x + '" cy="' + n.y + '" r="16"/><text class="tr-pt" x="' + n.x + '" y="' + (n.y + 5) + '" text-anchor="middle">' + n.v + "</text>";
    })(t);
    var wd = leaf * W + 10;
    return '<svg viewBox="0 0 ' + wd + " " + (depth * H + 48) + '" style="width:' + wd + 'px">' + out + "</svg>";
  }
  function wFact() {
    var w = document.getElementById("w-fact"); if (!w) return;
    var inp = w.querySelector(".tin"), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), mode = "col";
    function render() {
      var n = pnat(inp.value);
      vis.innerHTML = "";
      if (isNaN(n) || n < 2 || n > 1000000) { info.innerHTML = warn("fBad"); return; }
      var f = factor(n);
      if (f.length === 1 && f[0][1] === 1) { info.innerHTML = fill(u("fPrime"), { n: fh(n) }); return; }
      if (mode === "col") {
        var m = n, h = "";
        f.forEach(function (x) { for (var e = 0; e < x[1]; e++) { h += "<tr><td>" + fh(m) + "</td><td>" + x[0] + '</td><td class="why">' + why(m, x[0]) + "</td></tr>"; m /= x[0]; } });
        h += "<tr><td>1</td><td></td><td></td></tr>";
        vis.innerHTML = '<table class="fcol">' + h + "</table>";
      } else vis.innerHTML = '<div class="tree">' + treeSVG(ftree(n)) + "</div>";
      var flat = []; f.forEach(function (x) { for (var e = 0; e < x[1]; e++) flat.push(x[0]); });
      info.innerHTML = (flat.length > f.length ? tex(ft(n) + "=" + flat.join("\\cdot "), true) : "") + tex("\\boxed{" + ft(n) + "=" + ftex(f) + "}", true) + hint(u(mode === "col" ? "fRule" : "fTree"));
    }
    inp.addEventListener("input", render);
    segBind(w, function (k) { mode = k; render(); });
    w.querySelectorAll(".quick button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.b; render(); }); });
    onLang(render);
  }

  /* ---------- giny: mcm i MCD ---------- */
  function chips(a, cls) { return '<span class="chl">' + a.map(function (x) { return '<span class="ch' + (cls(x) ? " " + cls(x) : "") + '">' + fh(x) + "</span>"; }).join("") + "</span>"; }
  function wGcd(w) {
    var M = w.dataset.mode === "mcm", out = w.querySelector(".gout"), info = w.querySelector(".info"), mode = "fac";
    function render() {
      var v = readNums(w, ["a", "b", "c"], 100000);
      if (!v) { out.innerHTML = ""; info.innerHTML = warn("gBad"); return; }
      var L = v.reduce(lcm), G = v.reduce(gcd), R = M ? L : G, name = u(M ? "mcm" : "mcd"), args = v.map(ft).join(",");
      var h = "";
      if (mode === "fac") {
        var fs = v.map(factor), ps = [];
        fs.forEach(function (f) { f.forEach(function (x) { if (ps.indexOf(x[0]) < 0) ps.push(x[0]); }); });
        ps.sort(function (a, b) { return a - b; });
        var ex = fs.map(function (f) { return ps.map(function (p) { for (var i = 0; i < f.length; i++) if (f[i][0] === p) return f[i][1]; return 0; }); });
        var ch = ps.map(function (_, j) { var col = ex.map(function (r) { return r[j]; }); return M ? Math.max.apply(null, col) : Math.min.apply(null, col); });
        h += '<div class="flines">' + v.map(function (x, i) { return tex(ft(x) + "=" + ftex(fs[i])); }).join("") + "</div>";
        if (ps.length) {
          var pe = function (p, e) { return e ? tex(e > 1 ? p + "^{" + e + "}" : String(p)) : "—"; };
          h += '<div class="tbl-wrap"><table class="data gtab"><thead><tr><th>' + u("gNum") + "</th>" + ps.map(function (p) { return "<th>" + p + "</th>"; }).join("") + "</tr></thead><tbody>" +
            v.map(function (x, i) { return "<tr><th>" + fh(x) + "</th>" + ps.map(function (p, j) { var e = ex[i][j]; return '<td class="' + (ch[j] && e === ch[j] ? "pick" : "") + (!M && !ch[j] ? " nc" : "") + '">' + pe(p, e) + "</td>"; }).join("") + "</tr>"; }).join("") +
            '<tr class="res"><th>' + name + "</th>" + ps.map(function (p, j) { return "<td>" + (ch[j] ? pe(p, ch[j]) : '<small>' + u("gNc") + "</small>") + "</td>"; }).join("") + "</tr></tbody></table></div>";
        }
        var rf = ps.map(function (p, j) { return [p, ch[j]]; }).filter(function (x) { return x[1]; });
        info.innerHTML = tex("\\text{" + name + "}(" + args + ")=" + (ftex(rf) !== String(R) ? ftex(rf) + "=" : "") + "\\boxed{" + ft(R) + "}", true);
      } else {
        if (M) {
          var too = v.some(function (x) { return L / x > 30; });
          h += v.map(function (x) {
            var a = [], k = too ? 12 : L / x; for (var i = 1; i <= k; i++) a.push(x * i);
            return '<div class="lrow"><span class="lh">' + tex("\\text{M}(" + ft(x) + ")") + "</span>" + chips(a, function (y) { return y === L ? "pick" : ""; }) + (too ? " …" : "") + "</div>";
          }).join("");
          info.innerHTML = (too ? warn("gLong") + " " : fill(u("gComM"), { l: fh(L) })) + tex("\\text{" + name + "}(" + args + ")=\\boxed{" + ft(R) + "}", true);
        } else {
          h += v.map(function (x) { return '<div class="lrow"><span class="lh">' + tex("\\text{Div}(" + ft(x) + ")") + "</span>" + chips(divisors(x), function (y) { return y === G ? "pick" : G % y === 0 ? "cm" : ""; }) + "</div>"; }).join("");
          info.innerHTML = fill(u("gComD"), { l: list(divisors(G)), g: fh(G) }) + tex("\\text{" + name + "}(" + args + ")=\\boxed{" + ft(R) + "}", true);
        }
      }
      out.innerHTML = h;
      info.innerHTML += hint(u(M ? "gRuleM" : "gRuleD")) + (!M && G === 1 ? "<div>" + u("gCop") + "</div>" : "") +
        (v.length === 2 ? hint(fill(u("gRel"), { g: fh(G), l: fh(L), p: fh(G * L), a: fh(v[0]), b: fh(v[1]) })) : "");
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, function (k) { mode = k; render(); });
    quickFill(w, ["a", "b", "c"], render);
    onLang(render);
  }

  /* ---------- giny: coincidències (problemes de mcm) ---------- */
  function wCoin() {
    var w = document.getElementById("w-coin"); if (!w) return;
    var ch = w.querySelector(".chart"), info = w.querySelector(".info"), T = w.querySelector('[data-k="t"]'), lab = w.querySelector(".tstart"), unit = "min";
    function clock(t0, m) { var t = (t0 + m) % 1440; return Math.floor(t / 60) + ":" + ("0" + t % 60).slice(-2); }
    function render() {
      lab.hidden = unit !== "min";
      var v = readNums(w, ["a", "b", "c"], 500);
      if (!v) { ch.innerHTML = ""; info.innerHTML = warn("coBad"); return; }
      var L = v.reduce(lcm), H = 2 * L, X0 = 70, X1 = 600, x = function (t) { return X0 + t / H * (X1 - X0); }, s = "", un = u("un")[unit];
      var tm = /^(\d{1,2})[:.h](\d{2})$/.exec(T.value.trim()), t0 = tm && +tm[1] < 24 && +tm[2] < 60 ? +tm[1] * 60 + +tm[2] : null;
      var cols = ["var(--r1)", "var(--r2)", "var(--r3)"], Y = function (i) { return 26 + i * 34; }, yb = Y(v.length - 1) + 22;
      [0, L, H].forEach(function (t) { s += '<line class="co-hit" x1="' + x(t) + '" y1="10" x2="' + x(t) + '" y2="' + yb + '"/>'; });
      v.forEach(function (p, i) {
        var y = Y(i), n = H / p;
        s += '<text class="sv-t" x="' + (X0 - 10) + '" y="' + (y + 4) + '" text-anchor="end">' + u("every") + " " + p + "</text>";
        s += '<line class="sv-ax" x1="' + X0 + '" y1="' + y + '" x2="' + X1 + '" y2="' + y + '"/>';
        for (var k = 0; k <= n; k++) {
          var hit = (k * p) % L === 0;
          s += n <= 80 || hit ? '<circle cx="' + x(k * p) + '" cy="' + y + '" r="' + (hit ? 6.5 : 4) + '" style="fill:' + cols[i] + '"' + (hit ? ' class="co-on"' : "") + "/>" : '<line x1="' + x(k * p) + '" y1="' + (y - 4) + '" x2="' + x(k * p) + '" y2="' + (y + 4) + '" style="stroke:' + cols[i] + '"/>';
        }
      });
      [0, L, H].forEach(function (t) {
        s += '<text class="sv-tb" x="' + x(t) + '" y="' + (yb + 16) + '" text-anchor="middle">' + fh(t) + (t ? " " + un : "") + "</text>";
        if (unit === "min" && t0 != null) s += '<text class="sv-t" x="' + x(t) + '" y="' + (yb + 32) + '" text-anchor="middle">' + clock(t0, t) + "</text>";
      });
      ch.innerHTML = '<svg viewBox="0 0 620 ' + (yb + 40) + '" role="img" aria-label="coincidències">' + s + "</svg>";
      var f = factor(L);
      info.innerHTML = tex(v.map(function (p) { return ft(p) + "=" + ftex(factor(p)); }).join("\\qquad "), true) +
        tex("\\text{" + u("mcm") + "}(" + v.join(",") + ")=" + ftex(f) + (ftex(f) !== String(L) ? "=" + ft(L) : ""), true) +
        "<div>" + fill(u("coRes"), { l: fh(L), u: un }) + (unit === "min" && t0 != null ? fill(u("coClock"), { h: clock(t0, L) }) : "") + ".</div>" +
        (unit === "min" && t0 == null ? warn("coTime") : "") + hint(fill(u("coAgain"), { l: fh(L), u: un, l2: fh(2 * L), l3: fh(3 * L) }));
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, function (k) { unit = k; render(); });
    quickFill(w, ["a", "b", "c"], render);
    onLang(render);
  }

  /* ---------- giny: rajoles (problemes de MCD) ---------- */
  function wTile() {
    var w = document.getElementById("w-tile"); if (!w) return;
    var tc = w.querySelector(".tchips"), ch = w.querySelector(".chart"), info = w.querySelector(".info"), d = null;
    function render() {
      var v = readNums(w, ["a", "b"], 2000);
      if (!v) { tc.innerHTML = ch.innerHTML = ""; info.innerHTML = warn("tBad"); return; }
      var a = v[0], b = v[1], G = gcd(a, b), cd = divisors(G);
      if (d == null || cd.indexOf(d) < 0) d = G;
      tc.innerHTML = '<span class="ql">' + u("tChips") + "</span>" + cd.map(function (x) { return '<button type="button" data-d="' + x + '" aria-pressed="' + (x === d) + '"' + (x === G ? ' class="max"' : "") + ">" + x + "</button>"; }).join("");
      tc.querySelectorAll("button").forEach(function (bt) { bt.addEventListener("click", function () { d = +bt.dataset.d; render(); }); });
      var sc = Math.min(560 / a, 300 / b), W = a * sc, Hh = b * sc, nx = a / d, ny = b / d, s = '<rect class="tl-bg" x="20" y="10" width="' + W + '" height="' + Hh + '"/>';
      if (nx + ny <= 240) {
        for (var i = 1; i < nx; i++) s += '<line class="tl-l" x1="' + (20 + i * d * sc) + '" y1="10" x2="' + (20 + i * d * sc) + '" y2="' + (10 + Hh) + '"/>';
        for (var j = 1; j < ny; j++) s += '<line class="tl-l" x1="20" y1="' + (10 + j * d * sc) + '" x2="' + (20 + W) + '" y2="' + (10 + j * d * sc) + '"/>';
        s += '<rect class="tl-one" x="20" y="10" width="' + d * sc + '" height="' + d * sc + '"/>';
      }
      s += '<rect class="tl-fr" x="20" y="10" width="' + W + '" height="' + Hh + '"/>';
      s += '<text class="sv-t" x="' + (20 + W / 2) + '" y="' + (Hh + 28) + '" text-anchor="middle">' + fh(a) + ' cm</text><text class="sv-t" x="' + (W + 28) + '" y="' + (10 + Hh / 2) + '">' + fh(b) + " cm</text>";
      ch.innerHTML = '<svg viewBox="0 0 ' + (W + 80) + " " + (Hh + 40) + '" role="img" aria-label="rajoles">' + s + "</svg>";
      info.innerHTML = tex(ft(a) + "=" + ftex(factor(a)) + "\\qquad " + ft(b) + "=" + ftex(factor(b)) + "\\qquad \\text{" + u("mcd") + "}=" + ft(G), true) +
        "<div>" + fill(u("tRes"), { d: fh(d), x: fh(nx), y: fh(ny), n: fh(nx * ny) }) + "</div>" +
        hint(G === 1 ? u("tOne") : d === G ? fill(u("tMax"), { d: fh(G), a: fh(a), b: fh(b) }) : fill(u("tSmall"), { g: fh(G) })) + (nx + ny > 240 ? hint(u("tMany")) : "");
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", function () { d = null; render(); }); });
    quickFill(w, ["a", "b"], function () { d = null; render(); });
    onLang(render);
  }

  /* ---------- entrenadors ---------- */
  var GEN = {
    mult: function () {
      var n = rint(3, 25), N = rint(50, 500), q = Math.floor(N / n), r = N % n;
      if (Math.random() < .5) {
        var ans = n * (q + 1);
        return { ans: ans, q: function () { return fill(u("dMultN"), { n: n, N: fh(N) }); },
          s: function () { return tex(ft(N) + "=" + n + "\\cdot " + q + "+" + r + "\\ \\Rightarrow\\ " + n + "\\cdot " + (q + 1) + "=\\boxed{" + ft(ans) + "}", true); } };
      }
      return { ans: q, q: function () { return fill(u("dMultC"), { n: n, N: fh(N) }); },
        s: function () { return tex(ft(N) + "=" + n + "\\cdot " + q + "+" + r, true) + "<div>" + fill(u("dMultS"), { q: q, n: n, m: fh(n * q) }) + "</div>"; } };
    },
    divs: function () {
      var n = pick([12, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 60, 64, 72, 80, 84, 90, 96, 100, 13, 17, 25, 49, 81]), d = divisors(n);
      return { ans: d.length, q: function () { return fill(u("dDivs"), { n: n }); }, s: function () { return tex("\\text{Div}(" + n + ")=\\{" + d.join(",\\ ") + "\\}\\ \\to\\ \\boxed{" + d.length + "}", true); } };
    },
    crit: function () {
      for (;;) {
        var k = pick([3, 3, 9, 9, 11, 11, 2, 5]), len = rint(3, 5), d = [], ans = -1, x;
        for (var i = 0; i < len; i++) d.push(i ? rint(0, 9) : rint(1, 9));
        var pos = k === 2 || k === 5 ? len - 1 : rint(1, len - 1);
        for (x = 0; x <= 9; x++) { d[pos] = x; if (+d.join("") % k === 0) { ans = x; break; } }
        if (ans < 0) continue;
        var full = +d.join(""), sh = d.slice(); sh[pos] = "\\square ";
        return { ans: ans, q: function () { return fill(u("dCrit"), { x: "$" + sh.join("") + "$", k: k }); },
          s: function () { return "<div>" + critInfo(full, k).t + "</div>" + tex("\\boxed{" + ft(full) + "}", true); } };
      }
    },
    fact: function () {
      if (Math.random() < .5) {
        var f, v;
        do { f = []; v = 1; [2, 3, 5, 7, 11].forEach(function (p) { var e = Math.random() < .6 ? rint(1, p < 5 ? 4 : 2) : 0; if (e) { f.push([p, e]); v *= Math.pow(p, e); } }); } while (f.length < 2 || v > 3000);
        return { ans: v, q: function () { return u("dFactN") + " $" + ftex(f) + "$"; }, s: function () { return tex(ftex(f) + "=" + f.map(function (x) { return Math.pow(x[0], x[1]); }).join("\\cdot ") + "=\\boxed{" + ft(v) + "}", true); } };
      }
      var n, ff;
      do { n = rint(24, 1000); ff = factor(n); } while (ff.length < 2 || !ff.some(function (x) { return x[1] > 1; }));
      var t = pick(ff.filter(function (x) { return x[1] > 1; }).concat(ff));
      return { ans: t[1], q: function () { return fill(u("dFactE"), { p: t[0], n: fh(n) }); }, s: function () { return tex(ft(n) + "=" + ftex(ff) + "\\ \\to\\ \\boxed{" + t[1] + "}", true); } };
    },
    mcm: function () {
      var a, b, l;
      do { a = rint(4, 60); b = rint(4, 60); l = lcm(a, b); } while (a === b || l > 720 || ((l === a || l === b || l === a * b) && Math.random() < .7));
      return { ans: l, q: function () { return u("dCalc") + " $\\text{" + u("mcm") + "}(" + a + "," + b + ")$"; },
        s: function () { return tex(a + "=" + ftex(factor(a)) + "\\qquad " + b + "=" + ftex(factor(b)), true) + tex("\\text{" + u("mcm") + "}=" + ftex(factor(l)) + "=\\boxed{" + ft(l) + "}", true); } };
    },
    mcd: function () {
      var a, b, g;
      do { a = rint(12, 180); b = rint(12, 180); g = gcd(a, b); } while (a === b || g < 4 || ((g === a || g === b) && Math.random() < .7));
      return { ans: g, q: function () { return u("dCalc") + " $\\text{" + u("mcd") + "}(" + a + "," + b + ")$"; },
        s: function () { return tex(a + "=" + ftex(factor(a)) + "\\qquad " + b + "=" + ftex(factor(b)), true) + tex("\\text{" + u("mcd") + "}=" + ftex(factor(g)) + "=\\boxed{" + g + "}", true); } };
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
    { q: { va: "Quina frase és certa?", es: "¿Qué frase es cierta?", en: "Which sentence is true?" },
      o: [{ va: "$6$ és múltiple de $24$", es: "$6$ es múltiplo de $24$", en: "$6$ is a multiple of $24$" }, { va: "$24$ és divisor de $6$", es: "$24$ es divisor de $6$", en: "$24$ is a divisor of $6$" },
        { va: "$6$ és divisor de $24$", es: "$6$ es divisor de $24$", en: "$6$ is a divisor of $24$" }, { va: "$24$ no és divisible per $6$", es: "$24$ no es divisible por $6$", en: "$24$ is not divisible by $6$" }], a: 2,
      e: { va: "$24:6=4$ exacta: $6$ és divisor de $24$ (i $24$ és múltiple de $6$).", es: "$24:6=4$ exacta: $6$ es divisor de $24$ (y $24$ es múltiplo de $6$).", en: "$24:6=4$ exactly: $6$ is a divisor of $24$ (and $24$ is a multiple of $6$)." } },
    { q: { va: "Quin d'aquests nombres <b>no</b> és múltiple de 7?", es: "¿Cuál de estos números <b>no</b> es múltiplo de 7?", en: "Which of these is <b>not</b> a multiple of 7?" },
      o: [{ va: "$0$" }, { va: "$49$" }, { va: "$70$" }, { va: "$75$" }], a: 3,
      e: { va: "$75=7\\cdot10+5$. El 0 sí que ho és: $0=7\\cdot0$.", es: "$75=7\\cdot10+5$. El 0 sí lo es: $0=7\\cdot0$.", en: "$75=7\\cdot10+5$. 0 is one: $0=7\\cdot0$." } },
    { q: { va: "Quants divisors té el 12?", es: "¿Cuántos divisores tiene el 12?", en: "How many divisors does 12 have?" },
      o: [{ va: "$4$" }, { va: "$5$" }, { va: "$6$" }, { va: "$12$" }], a: 2,
      e: { va: "$1,\\ 2,\\ 3,\\ 4,\\ 6,\\ 12$: en té 6.", es: "$1,\\ 2,\\ 3,\\ 4,\\ 6,\\ 12$: tiene 6.", en: "$1,\\ 2,\\ 3,\\ 4,\\ 6,\\ 12$: it has 6." } },
    { q: { va: "$4785$ és divisible per…", es: "$4785$ es divisible por…", en: "$4785$ is divisible by…" },
      o: [{ va: "2 i 5", es: "2 y 5", en: "2 and 5" }, { va: "3 i 5", es: "3 y 5", en: "3 and 5" }, { va: "5 i 9", es: "5 y 9", en: "5 and 9" }, { va: "2 i 3", es: "2 y 3", en: "2 and 3" }], a: 1,
      e: { va: "Acaba en 5 (per 5 sí, per 2 no) i les xifres sumen 24 (per 3 sí, per 9 no).", es: "Acaba en 5 (por 5 sí, por 2 no) y las cifras suman 24 (por 3 sí, por 9 no).", en: "It ends in 5 (yes for 5, no for 2) and its digits add up to 24 (yes for 3, no for 9)." } },
    { q: { va: "Quin d'aquests nombres és divisible per 11?", es: "¿Cuál de estos números es divisible por 11?", en: "Which of these is divisible by 11?" },
      o: [{ va: "$1234$" }, { va: "$5841$" }, { va: "$4321$" }, { va: "$2020$" }], a: 1,
      e: { va: "En $5841$: lloc senar $1+8=9$, lloc parell $4+5=9$; la diferència és 0.", es: "En $5841$: lugar impar $1+8=9$, lugar par $4+5=9$; la diferencia es 0.", en: "In $5841$: odd places $1+8=9$, even places $4+5=9$; the difference is 0." } },
    { q: { va: "El nombre 1 és…", es: "El número 1 es…", en: "The number 1 is…" },
      o: [{ va: "primer", es: "primo", en: "prime" }, { va: "compost", es: "compuesto", en: "composite" }, { va: "ni primer ni compost", es: "ni primo ni compuesto", en: "neither prime nor composite" }, { va: "primer i compost", es: "primo y compuesto", en: "both" }], a: 2,
      e: { va: "Només té un divisor (ell mateix); els primers en tenen exactament dos.", es: "Solo tiene un divisor (él mismo); los primos tienen exactamente dos.", en: "It has only one divisor (itself); primes have exactly two." } },
    { q: { va: "Quin d'aquests nombres és primer?", es: "¿Cuál de estos números es primo?", en: "Which of these is prime?" },
      o: [{ va: "$21$" }, { va: "$39$" }, { va: "$51$" }, { va: "$53$" }], a: 3,
      e: { va: "$21=3\\cdot7$, $39=3\\cdot13$ i $51=3\\cdot17$. El 53 només es pot dividir entre 1 i ell mateix.", es: "$21=3\\cdot7$, $39=3\\cdot13$ y $51=3\\cdot17$. El 53 solo se puede dividir entre 1 y sí mismo.", en: "$21=3\\cdot7$, $39=3\\cdot13$ and $51=3\\cdot17$. 53 can only be divided by 1 and itself." } },
    { q: { va: "La descomposició en factors primers de 60 és…", es: "La descomposición en factores primos de 60 es…", en: "The prime factorisation of 60 is…" },
      o: [{ va: "$2^2\\cdot3\\cdot5$" }, { va: "$2\\cdot3\\cdot10$" }, { va: "$4\\cdot15$" }, { va: "$2\\cdot3^2\\cdot5$" }], a: 0,
      e: { va: "Tots els factors han de ser primers: $60=2\\cdot2\\cdot3\\cdot5$. El 10, el 4 i el 15 no són primers.", es: "Todos los factores tienen que ser primos: $60=2\\cdot2\\cdot3\\cdot5$. El 10, el 4 y el 15 no son primos.", en: "Every factor must be prime: $60=2\\cdot2\\cdot3\\cdot5$. 10, 4 and 15 aren't prime." } },
    { q: { va: "$2^3\\cdot5=$", es: "$2^3\\cdot5=$", en: "$2^3\\cdot5=$" },
      o: [{ va: "$30$" }, { va: "$40$" }, { va: "$16$" }, { va: "$80$" }], a: 1,
      e: { va: "$2^3=8$ i $8\\cdot5=40$.", es: "$2^3=8$ y $8\\cdot5=40$.", en: "$2^3=8$ and $8\\cdot5=40$." } },
    { q: { va: "$\\text{mcm}(4,6)=$", es: "$\\text{mcm}(4,6)=$", en: "$\\text{lcm}(4,6)=$" },
      o: [{ va: "$2$" }, { va: "$12$" }, { va: "$24$" }, { va: "$6$" }], a: 1,
      e: { va: "$\\text{M}(4)=\\{4,8,12,\\ldots\\}$, $\\text{M}(6)=\\{6,12,\\ldots\\}$. El 24 també és comú, però no és el més xicotet.", es: "$\\text{M}(4)=\\{4,8,12,\\ldots\\}$, $\\text{M}(6)=\\{6,12,\\ldots\\}$. El 24 también es común, pero no es el menor.", en: "$\\text{M}(4)=\\{4,8,12,\\ldots\\}$, $\\text{M}(6)=\\{6,12,\\ldots\\}$. 24 is also common, but not the smallest." } },
    { q: { va: "$\\text{MCD}(12,18)=$", es: "$\\text{MCD}(12,18)=$", en: "$\\text{gcd}(12,18)=$" },
      o: [{ va: "$2$" }, { va: "$3$" }, { va: "$6$" }, { va: "$36$" }], a: 2,
      e: { va: "Divisors comuns: 1, 2, 3 i 6. El més gran és 6. (36 és el mcm!)", es: "Divisores comunes: 1, 2, 3 y 6. El mayor es 6. (¡36 es el mcm!)", en: "Common divisors: 1, 2, 3 and 6. The largest is 6. (36 is the lcm!)" } },
    { q: { va: "$\\text{mcm}(5,7)=$", es: "$\\text{mcm}(5,7)=$", en: "$\\text{lcm}(5,7)=$" },
      o: [{ va: "$1$" }, { va: "$12$" }, { va: "$35$" }, { va: "$70$" }], a: 2,
      e: { va: "No tenen factors comuns: el mcm és el producte, $5\\cdot7=35$.", es: "No tienen factores comunes: el mcm es el producto, $5\\cdot7=35$.", en: "They share no factors: the lcm is the product, $5\\cdot7=35$." } },
    { q: { va: "$\\text{MCD}(8,15)=1$. Diem que 8 i 15 són…", es: "$\\text{MCD}(8,15)=1$. Decimos que 8 y 15 son…", en: "$\\text{gcd}(8,15)=1$. We say 8 and 15 are…" },
      o: [{ va: "primers", es: "primos", en: "primes" }, { va: "primers entre si", es: "primos entre sí", en: "coprime" }, { va: "compostos entre si", es: "compuestos entre sí", en: "co-composite" }, { va: "múltiples", es: "múltiplos", en: "multiples" }], a: 1,
      e: { va: "Ni el 8 ni el 15 són primers, però no tenen cap divisor comú llevat de l'1: són primers entre si.", es: "Ni el 8 ni el 15 son primos, pero no tienen ningún divisor común salvo el 1: son primos entre sí.", en: "Neither 8 nor 15 is prime, but their only common divisor is 1: they are coprime." } },
    { q: { va: "Per a calcular el <b>mcm</b> a partir de la descomposició, agafem…", es: "Para calcular el <b>mcm</b> a partir de la descomposición, tomamos…", en: "To find the <b>lcm</b> from the factorisation, we take…" },
      o: [{ va: "els factors comuns i no comuns amb el major exponent", es: "los factores comunes y no comunes con el mayor exponente", en: "all the factors with the highest exponent" }, { va: "només els comuns amb el menor exponent", es: "solo los comunes con el menor exponente", en: "only the common ones with the lowest exponent" },
        { va: "els comuns i no comuns amb el menor exponent", es: "los comunes y no comunes con el menor exponente", en: "all the factors with the lowest exponent" }, { va: "només els comuns amb el major exponent", es: "solo los comunes con el mayor exponente", en: "only the common ones with the highest exponent" }], a: 0,
      e: { va: "La segona opció és la regla del MCD. No les confongues!", es: "La segunda opción es la regla del MCD. ¡No las confundas!", en: "The second option is the gcd rule. Don't mix them up!" } },
    { q: { va: "Dos semàfors es posen en verd cada 40 i cada 60 segons. Si ara ho han fet alhora, quan ho tornaran a fer?", es: "Dos semáforos se ponen en verde cada 40 y cada 60 segundos. Si ahora lo han hecho a la vez, ¿cuándo lo volverán a hacer?", en: "Two traffic lights turn green every 40 and every 60 seconds. If they just did it together, when will they do it again?" },
      o: [{ va: "al cap de 20 s", es: "al cabo de 20 s", en: "after 20 s" }, { va: "al cap de 100 s", es: "al cabo de 100 s", en: "after 100 s" }, { va: "al cap de 120 s", es: "al cabo de 120 s", en: "after 120 s" }, { va: "al cap de 2400 s", es: "al cabo de 2400 s", en: "after 2400 s" }], a: 2,
      e: { va: "Tornen a coincidir: és un problema de mcm. $\\text{mcm}(40,60)=120$.", es: "Vuelven a coincidir: es un problema de mcm. $\\text{mcm}(40,60)=120$.", en: "They coincide again: it's an lcm problem. $\\text{lcm}(40,60)=120$." } },
    { q: { va: "Volem tallar dues cordes de 12 m i 20 m en trossos iguals, el més llargs possible. Quant farà cada tros?", es: "Queremos cortar dos cuerdas de 12 m y 20 m en trozos iguales, lo más largos posible. ¿Cuánto medirá cada trozo?", en: "We want to cut two ropes of 12 m and 20 m into equal pieces, as long as possible. How long is each piece?" },
      o: [{ va: "$2$ m" }, { va: "$4$ m" }, { va: "$60$ m" }, { va: "$240$ m" }], a: 1,
      e: { va: "Tallar en parts iguals el més grans possible: és un problema de MCD. $\\text{MCD}(12,20)=4$.", es: "Cortar en partes iguales lo más grandes posible: es un problema de MCD. $\\text{MCD}(12,20)=4$.", en: "Cutting into equal pieces as big as possible: it's a gcd problem. $\\text{gcd}(12,20)=4$." } }
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

  var TITLES = { va: "Divisibilitat · FentMates", es: "Divisibilidad · FentMates", en: "Divisibility · FentMates" };
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
    wRel(); wMult(); wDivs(); wCrit(); wSieve(); wPrime(); wFact();
    document.querySelectorAll(".w-gcd").forEach(wGcd); wCoin(); wTile();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
