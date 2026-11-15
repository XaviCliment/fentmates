(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2eso-u1-done", NSEC = 10;

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", writeN: "Escriu un nombre natural.",
      relYes: ["<b>{a}</b> és múltiple de <b>{b}</b>", "<b>{b}</b> és divisor de <b>{a}</b>", "<b>{a}</b> és divisible per <b>{b}</b>"],
      relNo: ["<b>{a}</b> no és múltiple de <b>{b}</b>", "<b>{b}</b> no és divisor de <b>{a}</b>", "<b>{a}</b> no és divisible per <b>{b}</b>"],
      relEx: "La divisió és <b>exacta</b> (residu 0):", relIn: "La divisió <b>no</b> és exacta (residu {r}):", relAlso: "Com que {a} = {b} · {q}, també {q} és divisor de {a}.",
      relNear: "Els múltiples de {b} més pròxims a {a} són {m1} i {m2}.", relZero: "El 0 és múltiple de tots els nombres: 0 = {b} · 0.", relB0: "No es pot dividir entre 0: el 0 no és divisor de cap nombre.",
      rows: "Fem files de {b}: n'hi ha {q} de completes", rowsL: " i en sobren {r}.", rowsN: " i no en sobra cap.", row: "fila", left: "sobren", dotsBig: "(El dibuix només es fa fins a 120 punts i files de 12 com a molt.)",
      mBad: "Escriu nombres entre 1 i 50 (el segon és opcional).", mOf: "Múltiples de {n}", mBoth: "Múltiples comuns", mCom: "Múltiples comuns de {n} i {m} fins a 100:",
      mFirst: "El més xicotet (sense el 0) és <b>{l}</b>: és el seu <b>mínim comú múltiple</b> (apartat 1.5).", mNone: "No n'hi ha cap fins a 100: el primer és {l}.", mJump: "Anem saltant de {n} en {n}: cada múltiple és l'anterior més {n}. La llista no s'acaba mai.",
      dvBad: "Escriu un nombre entre 1 i 100 000.", dvDiv: "Divisió", dvRes: "Resultat", dvPair: "Parella", dvStop: "Parem: el quocient ja és menor o igual que el divisor.",
      dvCount: "{n} té <b>{k}</b> divisors.", dvPrime: " Només en té dos: és un nombre <b>primer</b>.", dvOne: " L'1 només té un divisor: ell mateix.", dvSq: " Com que {r} · {r} = {n}, el {r} només el comptem una vegada.",
      dvExact: "(Només mostrem les divisions exactes.)", dvRect: "Rectangles que podem fer amb {n} quadrets:",
      even: "parella", odd: "senar", c2: "Acaba en {d}, que és {p}.", c5: "Acaba en {d}.", mulY: "→ {s} és múltiple de {k}.", mulN: "→ {s} no és múltiple de {k}.",
      c11: "Lloc senar: {o}. Lloc parell: {e}.", m11Y: "→ és 0 o múltiple d'11.", m11N: "→ no és 0 ni múltiple d'11.", yes: "Sí", no: "No",
      posO: "lloc senar", posE: "lloc parell", cAll: "{n} és divisible per: <b>{l}</b>.", cNone: "{n} no és divisible per cap d'aquests nombres.",
      sv0: "Prem «Següent pas» per a començar a garbellar.", sv1: "L'1 no és primer: el ratllem.", svP: "El <b>{p}</b> és primer: l'encerclem i ratllem tots els seus múltiples: {l}…", svA: " (Alguns ja estaven ratllats.)",
      svEnd: "Com que 11 · 11 = 121 ja és més gran que 100, tots els nombres que queden sense ratllar són primers: n'hi ha <b>25</b>.", svTap: "Toca un nombre per a veure'n els divisors.",
      svCell: "<b>{n}</b>: divisors {d} → {t}.", prime: "primer", comp: "compost", neither: "ni primer ni compost",
      pmBad: "Escriu un nombre entre 2 i 100 000.", prDiv: "Divisió", prQ: "Quocient", prR: "Residu",
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
      dFactN: "Quin nombre té aquesta descomposició?", dFactE: "Quin és l'exponent del {p} en la descomposició de {n}?", dCalc: "Calcula:",
      next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", write: "Escriu un nombre enter (per exemple, −7).",
      ctx: {
        temp: { p: "{n} °C sobre zero", n: "{n} °C baix zero", z: "0 °C: ni fa calor ni fred… de gel!", zero: "0 °C", up: "més calor", down: "més fred" },
        floor: { p: "planta {n}", n: "soterrani {n}", z: "planta baixa", zero: "planta baixa", up: "plantes", down: "soterranis" },
        alt: { p: "{n} m d'altitud (sobre el nivell de la mar)", n: "{n} m de profunditat (sota el nivell de la mar)", z: "al nivell de la mar", zero: "nivell de la mar", up: "altitud", down: "profunditat" },
        money: { p: "tinc {n} €", n: "dec {n} €", z: "ni tinc ni dec res", zero: "0 €", up: "diners", down: "deutes" },
        year: { p: "any {n} d. C.", n: "any {n} a. C.", z: "", zero: "naixement de Crist", up: "després de Crist", down: "abans de Crist" } },
      cxBad: "Escriu un enter entre −9999 i 9999.", cxRef: "El 0 és la <b>referència</b>: {z}. Els positius estan per damunt i els negatius, per davall.", cxYear0: "Compte: no hi ha cap «any 0»! De l'any 1 a. C. es passa directament a l'any 1 d. C.",
      cxSay: "Ho diem així:", cxNum: "Ho escrivim així:",
      lnBad: "Escriu entre 1 i 15 enters separats per comes (entre −1000 i 1000).", lnAsc: "De menor a major:", lnDesc: "De major a menor:", lnRight: "Com més a la dreta en la recta, més gran és el nombre.",
      lnCmp: "{a} està més a la {s} que {b}, per tant", lnL: "esquerra", lnR: "dreta", lnEq: "Són el mateix nombre.", lnRep: "(Els nombres repetits només es dibuixen una vegada.)",
      abBad: "Escriu un enter entre −1000 i 1000.", abDist: "{a} està a <b>{d}</b> unitats del 0: el seu valor absolut és {d}.", abOp: "L'oposat de {a} és <b>{o}</b>: està a la mateixa distància del 0, però a l'altre costat.",
      abZero: "El 0 és l'únic nombre que és igual al seu oposat i que té valor absolut 0.", abPair: "Entre {a} i {o} hi ha {t} unitats (el doble de {d}).",
      adBad: "Escriu enters entre −200 i 200.", adSub: "Restar és sumar l'oposat:", adSame: "Tenen el <b>mateix signe</b>: sumem {x} + {y} = {s} i posem el signe comú ({g}).",
      adDiff: "Tenen <b>signes diferents</b>: restem {x} − {y} = {s} i posem el signe del que té major valor absolut ({g}).", adZero: "Són oposats: la suma és 0.", adZ: "Sumar 0 no canvia res.",
      adMove: "Partim de {a} i ens movem {m} unitats cap a la {s}.", sgP: "+", sgN: "−",
      prBad: "Escriu termes com 3, −5, (+7), −(−4)… separats per + o −.", prRule: "Traiem els parèntesis amb la regla dels signes:", prGroup: "Agrupem positius i negatius:", prOnly: "No hi ha parèntesis: ja podem operar.",
      sgBad: "Escriu enters entre −1000 i 1000.", sgDiv0: "No es pot dividir entre 0.", sgInex: "{a} : {b} no és exacta: el resultat no és un nombre enter.", sgZero: "Si un dels factors és 0, el producte és 0 (no té signe).",
      sgSame: "Signes <b>iguals</b> → resultat <b>positiu</b>.", sgDiff: "Signes <b>diferents</b> → resultat <b>negatiu</b>.", sgAbs: "Primer operem els valors absoluts: {x} {o} {y} = {r}.",
      hParse: "No entenc l'expressió. Usa xifres, + − · : i parèntesis ( ) [ ].", hDiv: "{a} : {b} no és exacta: el resultat no seria enter.", hDiv0: "No es pot dividir entre 0.", hBig: "El resultat és massa gran.",
      kinds: { pow: "Potència", root: "Arrel", opp: "Signe davant del parèntesi", mul: "Multiplicació", div: "Divisió", add: "Suma", sub: "Resta" }, inPar: "dins del parèntesi", result: "Resultat:", already: "Ja és un nombre: no hi ha res a calcular.",
      elBad: "Escriu un enter de partida i una llista de canvis com +5, −3, +2 (com a molt 20).", elStart: "Partida", elEnd: "Final", elVar: "Variació total: {v}.", elMax: "El valor més alt ha sigut {M} i el més baix, {m}.",
      elSay: "Al final:", elUnit: { floor: "", temp: " °C", money: " €" },
      dMin: "Quin és el més <b>xicotet</b> d'aquests nombres?", dMax: "Quin és el més <b>gran</b> d'aquests nombres?", dOpp: "Dos nombres oposats estan a {d} unitats l'un de l'altre. Quin és el negatiu?", dCalc: "Calcula:", dMiss: "Quin nombre falta?",
      hExp: "En aquesta unitat els exponents són nombres naturals (0, 1, 2…).", h00: "0⁰ no està definit.", hRneg: "√({a}) no existeix: cap enter elevat al quadrat dona un nombre negatiu.", hRin: "√{a} no és exacta: {a} no és un quadrat perfecte (prova la calculadora d'arrels enteres).",
      pzBad: "Escriu una base entera entre −20 i 20 i un exponent natural entre 0 i 12.", pz00: "0⁰ no està definit.", pzPos: "Base <b>positiva</b> → el resultat sempre és <b>positiu</b>.",
      pzEven: "Base <b>negativa</b> i exponent <b>parell</b> ({n}): els {n} signes − s'emparellen (− · − = +) → resultat <b>positiu</b>.", pzOdd: "Base <b>negativa</b> i exponent <b>senar</b> ({n}): en fer parelles en sobra un signe − → resultat <b>negatiu</b>.",
      pzZero: "Base 0: el resultat és 0 (si l'exponent no és 0).", pzExp0: "Tota potència d'exponent 0 (amb base diferent de 0) val <b>1</b>.", pzOne: "Exponent 1: la potència és la mateixa base.", pzMinus: "Compte amb el parèntesi! Sense parèntesi, el signe − no s'eleva:", pzMany: "{n} factors",
      rzBad: "Escriu un enter entre −1 000 000 i 1 000 000.", rzNeg: "No existeix: el quadrat de qualsevol enter és positiu o zero, mai negatiu.", rzEx: "<b>{a}</b> és un <b>quadrat perfecte</b>: té dues arrels quadrades, <b>{s}</b> i <b>−{s}</b>.", rzZero: "L'única arrel quadrada de 0 és 0.",
      rzIn: "<b>{a}</b> no és un quadrat perfecte: està entre {lo} i {hi}. La seua <b>arrel entera</b> és <b>{s}</b> i el <b>residu</b>, <b>{r}</b>.", rzChk: "Comprovació: {s}² + {r} = {a}.",
      dRoot: "Calcula l'arrel quadrada positiva:", dPow: "Calcula:", _: "" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", writeN: "Escribe un número natural.",
      relYes: ["<b>{a}</b> es múltiplo de <b>{b}</b>", "<b>{b}</b> es divisor de <b>{a}</b>", "<b>{a}</b> es divisible por <b>{b}</b>"],
      relNo: ["<b>{a}</b> no es múltiplo de <b>{b}</b>", "<b>{b}</b> no es divisor de <b>{a}</b>", "<b>{a}</b> no es divisible por <b>{b}</b>"],
      relEx: "La división es <b>exacta</b> (resto 0):", relIn: "La división <b>no</b> es exacta (resto {r}):", relAlso: "Como {a} = {b} · {q}, también {q} es divisor de {a}.",
      relNear: "Los múltiplos de {b} más próximos a {a} son {m1} y {m2}.", relZero: "El 0 es múltiplo de todos los números: 0 = {b} · 0.", relB0: "No se puede dividir entre 0: el 0 no es divisor de ningún número.",
      rows: "Hacemos filas de {b}: hay {q} completas", rowsL: " y sobran {r}.", rowsN: " y no sobra ninguno.", row: "fila", left: "sobran", dotsBig: "(El dibujo solo se hace hasta 120 puntos y filas de 12 como mucho.)",
      mBad: "Escribe números entre 1 y 50 (el segundo es opcional).", mOf: "Múltiplos de {n}", mBoth: "Múltiplos comunes", mCom: "Múltiplos comunes de {n} y {m} hasta 100:",
      mFirst: "El menor (sin el 0) es <b>{l}</b>: es su <b>mínimo común múltiplo</b> (apartado 1.5).", mNone: "No hay ninguno hasta 100: el primero es {l}.", mJump: "Vamos saltando de {n} en {n}: cada múltiplo es el anterior más {n}. La lista no se acaba nunca.",
      dvBad: "Escribe un número entre 1 y 100 000.", dvDiv: "División", dvRes: "Resultado", dvPair: "Pareja", dvStop: "Paramos: el cociente ya es menor o igual que el divisor.",
      dvCount: "{n} tiene <b>{k}</b> divisores.", dvPrime: " Solo tiene dos: es un número <b>primo</b>.", dvOne: " El 1 solo tiene un divisor: él mismo.", dvSq: " Como {r} · {r} = {n}, el {r} solo lo contamos una vez.",
      dvExact: "(Solo mostramos las divisiones exactas.)", dvRect: "Rectángulos que podemos hacer con {n} cuadraditos:",
      even: "par", odd: "impar", c2: "Acaba en {d}, que es {p}.", c5: "Acaba en {d}.", mulY: "→ {s} es múltiplo de {k}.", mulN: "→ {s} no es múltiplo de {k}.",
      c11: "Lugar impar: {o}. Lugar par: {e}.", m11Y: "→ es 0 o múltiplo de 11.", m11N: "→ no es 0 ni múltiplo de 11.", yes: "Sí", no: "No",
      posO: "lugar impar", posE: "lugar par", cAll: "{n} es divisible por: <b>{l}</b>.", cNone: "{n} no es divisible por ninguno de estos números.",
      sv0: "Pulsa «Siguiente paso» para empezar a cribar.", sv1: "El 1 no es primo: lo tachamos.", svP: "El <b>{p}</b> es primo: lo rodeamos y tachamos todos sus múltiplos: {l}…", svA: " (Algunos ya estaban tachados.)",
      svEnd: "Como 11 · 11 = 121 ya es mayor que 100, todos los números que quedan sin tachar son primos: hay <b>25</b>.", svTap: "Toca un número para ver sus divisores.",
      svCell: "<b>{n}</b>: divisores {d} → {t}.", prime: "primo", comp: "compuesto", neither: "ni primo ni compuesto",
      pmBad: "Escribe un número entre 2 y 100 000.", prDiv: "División", prQ: "Cociente", prR: "Resto",
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
      dFactN: "¿Qué número tiene esta descomposición?", dFactE: "¿Cuál es el exponente del {p} en la descomposición de {n}?", dCalc: "Calcula:",
      next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", write: "Escribe un número entero (por ejemplo, −7).",
      ctx: {
        temp: { p: "{n} °C sobre cero", n: "{n} °C bajo cero", z: "0 °C: ¡ni calor ni frío… de hielo!", zero: "0 °C", up: "más calor", down: "más frío" },
        floor: { p: "planta {n}", n: "sótano {n}", z: "planta baja", zero: "planta baja", up: "plantas", down: "sótanos" },
        alt: { p: "{n} m de altitud (sobre el nivel del mar)", n: "{n} m de profundidad (bajo el nivel del mar)", z: "al nivel del mar", zero: "nivel del mar", up: "altitud", down: "profundidad" },
        money: { p: "tengo {n} €", n: "debo {n} €", z: "ni tengo ni debo nada", zero: "0 €", up: "dinero", down: "deudas" },
        year: { p: "año {n} d. C.", n: "año {n} a. C.", z: "", zero: "nacimiento de Cristo", up: "después de Cristo", down: "antes de Cristo" } },
      cxBad: "Escribe un entero entre −9999 y 9999.", cxRef: "El 0 es la <b>referencia</b>: {z}. Los positivos están por encima y los negativos, por debajo.", cxYear0: "¡Cuidado: no existe el «año 0»! Del año 1 a. C. se pasa directamente al año 1 d. C.",
      cxSay: "Lo decimos así:", cxNum: "Lo escribimos así:",
      lnBad: "Escribe entre 1 y 15 enteros separados por comas (entre −1000 y 1000).", lnAsc: "De menor a mayor:", lnDesc: "De mayor a menor:", lnRight: "Cuanto más a la derecha en la recta, mayor es el número.",
      lnCmp: "{a} está más a la {s} que {b}, por tanto", lnL: "izquierda", lnR: "derecha", lnEq: "Son el mismo número.", lnRep: "(Los números repetidos solo se dibujan una vez.)",
      abBad: "Escribe un entero entre −1000 y 1000.", abDist: "{a} está a <b>{d}</b> unidades del 0: su valor absoluto es {d}.", abOp: "El opuesto de {a} es <b>{o}</b>: está a la misma distancia del 0, pero al otro lado.",
      abZero: "El 0 es el único número que es igual a su opuesto y que tiene valor absoluto 0.", abPair: "Entre {a} y {o} hay {t} unidades (el doble de {d}).",
      adBad: "Escribe enteros entre −200 y 200.", adSub: "Restar es sumar el opuesto:", adSame: "Tienen el <b>mismo signo</b>: sumamos {x} + {y} = {s} y ponemos el signo común ({g}).",
      adDiff: "Tienen <b>signos distintos</b>: restamos {x} − {y} = {s} y ponemos el signo del que tiene mayor valor absoluto ({g}).", adZero: "Son opuestos: la suma es 0.", adZ: "Sumar 0 no cambia nada.",
      adMove: "Partimos de {a} y nos movemos {m} unidades hacia la {s}.", sgP: "+", sgN: "−",
      prBad: "Escribe términos como 3, −5, (+7), −(−4)… separados por + o −.", prRule: "Quitamos los paréntesis con la regla de los signos:", prGroup: "Agrupamos positivos y negativos:", prOnly: "No hay paréntesis: ya podemos operar.",
      sgBad: "Escribe enteros entre −1000 y 1000.", sgDiv0: "No se puede dividir entre 0.", sgInex: "{a} : {b} no es exacta: el resultado no es un número entero.", sgZero: "Si uno de los factores es 0, el producto es 0 (no tiene signo).",
      sgSame: "Signos <b>iguales</b> → resultado <b>positivo</b>.", sgDiff: "Signos <b>distintos</b> → resultado <b>negativo</b>.", sgAbs: "Primero operamos los valores absolutos: {x} {o} {y} = {r}.",
      hParse: "No entiendo la expresión. Usa cifras, + − · : y paréntesis ( ) [ ].", hDiv: "{a} : {b} no es exacta: el resultado no sería entero.", hDiv0: "No se puede dividir entre 0.", hBig: "El resultado es demasiado grande.",
      kinds: { pow: "Potencia", root: "Raíz", opp: "Signo delante del paréntesis", mul: "Multiplicación", div: "División", add: "Suma", sub: "Resta" }, inPar: "dentro del paréntesis", result: "Resultado:", already: "Ya es un número: no hay nada que calcular.",
      elBad: "Escribe un entero de partida y una lista de cambios como +5, −3, +2 (como mucho 20).", elStart: "Salida", elEnd: "Final", elVar: "Variación total: {v}.", elMax: "El valor más alto ha sido {M} y el más bajo, {m}.",
      elSay: "Al final:", elUnit: { floor: "", temp: " °C", money: " €" },
      dMin: "¿Cuál es el <b>menor</b> de estos números?", dMax: "¿Cuál es el <b>mayor</b> de estos números?", dOpp: "Dos números opuestos están a {d} unidades el uno del otro. ¿Cuál es el negativo?", dCalc: "Calcula:", dMiss: "¿Qué número falta?",
      hExp: "En esta unidad los exponentes son números naturales (0, 1, 2…).", h00: "0⁰ no está definido.", hRneg: "√({a}) no existe: ningún entero elevado al cuadrado da un número negativo.", hRin: "√{a} no es exacta: {a} no es un cuadrado perfecto (prueba la calculadora de raíces enteras).",
      pzBad: "Escribe una base entera entre −20 y 20 y un exponente natural entre 0 y 12.", pz00: "0⁰ no está definido.", pzPos: "Base <b>positiva</b> → el resultado siempre es <b>positivo</b>.",
      pzEven: "Base <b>negativa</b> y exponente <b>par</b> ({n}): los {n} signos − se emparejan (− · − = +) → resultado <b>positivo</b>.", pzOdd: "Base <b>negativa</b> y exponente <b>impar</b> ({n}): al hacer parejas sobra un signo − → resultado <b>negativo</b>.",
      pzZero: "Base 0: el resultado es 0 (si el exponente no es 0).", pzExp0: "Toda potencia de exponente 0 (con base distinta de 0) vale <b>1</b>.", pzOne: "Exponente 1: la potencia es la misma base.", pzMinus: "¡Cuidado con el paréntesis! Sin paréntesis, el signo − no se eleva:", pzMany: "{n} factores",
      rzBad: "Escribe un entero entre −1 000 000 y 1 000 000.", rzNeg: "No existe: el cuadrado de cualquier entero es positivo o cero, nunca negativo.", rzEx: "<b>{a}</b> es un <b>cuadrado perfecto</b>: tiene dos raíces cuadradas, <b>{s}</b> y <b>−{s}</b>.", rzZero: "La única raíz cuadrada de 0 es 0.",
      rzIn: "<b>{a}</b> no es un cuadrado perfecto: está entre {lo} y {hi}. Su <b>raíz entera</b> es <b>{s}</b> y el <b>resto</b>, <b>{r}</b>.", rzChk: "Comprobación: {s}² + {r} = {a}.",
      dRoot: "Calcula la raíz cuadrada positiva:", dPow: "Calcula:", _: "" },
    en: { next: "Next step", all: "Show all", reset: "Hide steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Toggle light and dark mode", writeN: "Type a whole number.",
      relYes: ["<b>{a}</b> is a multiple of <b>{b}</b>", "<b>{b}</b> is a divisor of <b>{a}</b>", "<b>{a}</b> is divisible by <b>{b}</b>"],
      relNo: ["<b>{a}</b> is not a multiple of <b>{b}</b>", "<b>{b}</b> is not a divisor of <b>{a}</b>", "<b>{a}</b> is not divisible by <b>{b}</b>"],
      relEx: "The division is <b>exact</b> (remainder 0):", relIn: "The division is <b>not</b> exact (remainder {r}):", relAlso: "Since {a} = {b} · {q}, {q} is also a divisor of {a}.",
      relNear: "The multiples of {b} closest to {a} are {m1} and {m2}.", relZero: "0 is a multiple of every number: 0 = {b} · 0.", relB0: "You can't divide by 0: 0 is not a divisor of any number.",
      rows: "Make rows of {b}: there are {q} full rows", rowsL: " and {r} left over.", rowsN: " and none left over.", row: "row", left: "left", dotsBig: "(The picture is only drawn up to 120 dots and rows of at most 12.)",
      mBad: "Type numbers from 1 to 50 (the second one is optional).", mOf: "Multiples of {n}", mBoth: "Common multiples", mCom: "Common multiples of {n} and {m} up to 100:",
      mFirst: "The smallest (not counting 0) is <b>{l}</b>: their <b>least common multiple</b> (section 1.5).", mNone: "There are none up to 100: the first is {l}.", mJump: "We jump in steps of {n}: each multiple is the previous one plus {n}. The list never ends.",
      dvBad: "Type a number from 1 to 100,000.", dvDiv: "Division", dvRes: "Result", dvPair: "Pair", dvStop: "Stop: the quotient is now less than or equal to the divisor.",
      dvCount: "{n} has <b>{k}</b> divisors.", dvPrime: " Only two: it is a <b>prime</b> number.", dvOne: " 1 has only one divisor: itself.", dvSq: " Since {r} · {r} = {n}, we count {r} only once.",
      dvExact: "(Only the exact divisions are shown.)", dvRect: "Rectangles we can make with {n} squares:",
      even: "even", odd: "odd", c2: "It ends in {d}, which is {p}.", c5: "It ends in {d}.", mulY: "→ {s} is a multiple of {k}.", mulN: "→ {s} is not a multiple of {k}.",
      c11: "Odd places: {o}. Even places: {e}.", m11Y: "→ it's 0 or a multiple of 11.", m11N: "→ it's neither 0 nor a multiple of 11.", yes: "Yes", no: "No",
      posO: "odd place", posE: "even place", cAll: "{n} is divisible by: <b>{l}</b>.", cNone: "{n} is not divisible by any of these numbers.",
      sv0: "Press “Next step” to start sieving.", sv1: "1 is not prime: cross it out.", svP: "<b>{p}</b> is prime: circle it and cross out all its multiples: {l}…", svA: " (Some were already crossed out.)",
      svEnd: "Since 11 · 11 = 121 is already bigger than 100, every number left uncrossed is prime: there are <b>25</b>.", svTap: "Tap a number to see its divisors.",
      svCell: "<b>{n}</b>: divisors {d} → {t}.", prime: "prime", comp: "composite", neither: "neither prime nor composite",
      pmBad: "Type a number from 2 to 100,000.", prDiv: "Division", prQ: "Quotient", prR: "Remainder",
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
      dFactN: "Which number has this factorisation?", dFactE: "What is the exponent of {p} in the factorisation of {n}?", dCalc: "Work out:",
      next: "Next step", all: "Show all", reset: "Hide steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Toggle light and dark mode", write: "Type an integer (for example, −7).",
      ctx: {
        temp: { p: "{n} °C above zero", n: "{n} °C below zero", z: "0 °C: freezing point!", zero: "0 °C", up: "warmer", down: "colder" },
        floor: { p: "floor {n}", n: "basement {n}", z: "ground floor", zero: "ground floor", up: "floors", down: "basements" },
        alt: { p: "{n} m above sea level", n: "{n} m below sea level", z: "at sea level", zero: "sea level", up: "height", down: "depth" },
        money: { p: "I have €{n}", n: "I owe €{n}", z: "I have nothing and owe nothing", zero: "€0", up: "money", down: "debts" },
        year: { p: "year {n} AD", n: "year {n} BC", z: "", zero: "birth of Christ", up: "AD", down: "BC" } },
      cxBad: "Type an integer from −9999 to 9999.", cxRef: "0 is the <b>reference point</b>: {z}. Positives are above it and negatives below it.", cxYear0: "Careful: there is no “year 0”! Year 1 BC is followed directly by year 1 AD.",
      cxSay: "We say:", cxNum: "We write:",
      lnBad: "Type from 1 to 15 integers separated by commas (between −1000 and 1000).", lnAsc: "From smallest to largest:", lnDesc: "From largest to smallest:", lnRight: "The further right on the number line, the bigger the number.",
      lnCmp: "{a} is further {s} than {b}, so", lnL: "left", lnR: "right", lnEq: "They are the same number.", lnRep: "(Repeated numbers are drawn only once.)",
      abBad: "Type an integer from −1000 to 1000.", abDist: "{a} is <b>{d}</b> units away from 0: its absolute value is {d}.", abOp: "The opposite of {a} is <b>{o}</b>: it's the same distance from 0, but on the other side.",
      abZero: "0 is the only number that equals its opposite and has absolute value 0.", abPair: "There are {t} units between {a} and {o} (twice {d}).",
      adBad: "Type integers from −200 to 200.", adSub: "Subtracting is adding the opposite:", adSame: "They have the <b>same sign</b>: add {x} + {y} = {s} and keep the common sign ({g}).",
      adDiff: "They have <b>different signs</b>: subtract {x} − {y} = {s} and take the sign of the one with the larger absolute value ({g}).", adZero: "They are opposites: the sum is 0.", adZ: "Adding 0 changes nothing.",
      adMove: "Start at {a} and move {m} units to the {s}.", sgP: "+", sgN: "−",
      prBad: "Type terms like 3, −5, (+7), −(−4)… joined by + or −.", prRule: "Remove the brackets using the sign rule:", prGroup: "Group positives and negatives:", prOnly: "There are no brackets: we can work it out directly.",
      sgBad: "Type integers from −1000 to 1000.", sgDiv0: "You can't divide by 0.", sgInex: "{a} : {b} is not exact: the result is not an integer.", sgZero: "If one factor is 0, the product is 0 (which has no sign).",
      sgSame: "<b>Same</b> signs → <b>positive</b> result.", sgDiff: "<b>Different</b> signs → <b>negative</b> result.", sgAbs: "First work with the absolute values: {x} {o} {y} = {r}.",
      hParse: "I can't read that expression. Use digits, + − · : and brackets ( ) [ ].", hDiv: "{a} : {b} is not exact: the result wouldn't be an integer.", hDiv0: "You can't divide by 0.", hBig: "The result is too big.",
      kinds: { pow: "Power", root: "Root", opp: "Sign before brackets", mul: "Multiplication", div: "Division", add: "Addition", sub: "Subtraction" }, inPar: "inside the brackets", result: "Result:", already: "It's already a number: nothing to work out.",
      elBad: "Type a starting integer and a list of changes like +5, −3, +2 (at most 20).", elStart: "Start", elEnd: "End", elVar: "Total change: {v}.", elMax: "The highest value was {M} and the lowest, {m}.",
      elSay: "At the end:", elUnit: { floor: "", temp: " °C", money: " €" },
      dMin: "Which is the <b>smallest</b> of these numbers?", dMax: "Which is the <b>largest</b> of these numbers?", dOpp: "Two opposite numbers are {d} units apart. Which is the negative one?", dCalc: "Work out:", dMiss: "Which number is missing?",
      hExp: "In this unit exponents are natural numbers (0, 1, 2…).", h00: "0⁰ is not defined.", hRneg: "√({a}) doesn't exist: no integer squared gives a negative number.", hRin: "√{a} isn't exact: {a} is not a perfect square (try the integer root calculator).",
      pzBad: "Enter an integer base between −20 and 20 and a natural exponent between 0 and 12.", pz00: "0⁰ is not defined.", pzPos: "<b>Positive</b> base → the result is always <b>positive</b>.",
      pzEven: "<b>Negative</b> base and <b>even</b> exponent ({n}): the {n} minus signs pair up (− · − = +) → <b>positive</b> result.", pzOdd: "<b>Negative</b> base and <b>odd</b> exponent ({n}): pairing them leaves one minus sign over → <b>negative</b> result.",
      pzZero: "Base 0: the result is 0 (if the exponent isn't 0).", pzExp0: "Any power with exponent 0 (and a non-zero base) equals <b>1</b>.", pzOne: "Exponent 1: the power is the base itself.", pzMinus: "Watch the brackets! Without them, the minus sign is not raised to the power:", pzMany: "{n} factors",
      rzBad: "Enter an integer between −1 000 000 and 1 000 000.", rzNeg: "It doesn't exist: the square of any integer is positive or zero, never negative.", rzEx: "<b>{a}</b> is a <b>perfect square</b>: it has two square roots, <b>{s}</b> and <b>−{s}</b>.", rzZero: "The only square root of 0 is 0.",
      rzIn: "<b>{a}</b> is not a perfect square: it lies between {lo} and {hi}. Its <b>integer root</b> is <b>{s}</b> and the <b>remainder</b> is <b>{r}</b>.", rzChk: "Check: {s}² + {r} = {a}.",
      dRoot: "Work out the positive square root:", dPow: "Work out:", _: "" }
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
  function segVal(w) { var b = w.querySelector('.seg button[aria-pressed="true"]'); return b ? b.dataset.k : null; }
  function segSet(w, k) { w.querySelectorAll(".seg button").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.k === k)); }); }

  /* ---------- nombres i format ---------- */
  function norm(s) { return String(s).replace(/[−–—]/g, "-").replace(/[×xX*]/g, "·").replace(/[\/÷]/g, ":").replace(/[\s  ]/g, ""); }
  function pint(s) {
    s = norm(s);
    if (!/^[+-]?\d{1,9}$/.test(s)) return NaN;
    return parseInt(s, 10);
  }
  function fcore(x, th) {
    if (!isFinite(x)) return "—";
    var s = String(Math.round(Math.abs(x)));
    if (s.length > 4) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, th);
    return s;
  }
  function fh(x) { return (x < 0 ? "−" : "") + fcore(x, " "); }          // HTML: −7
  function fs(x) { return (x > 0 ? "+" : "") + fh(x); }                    // HTML amb signe: +7, −7
  function ft(x) { return (x < 0 ? "-" : "") + fcore(x, "\\,"); }          // TeX: -7
  function fp(x) { return x < 0 ? "(" + ft(x) + ")" : ft(x); }             // TeX amb parèntesi si és negatiu
  function fps(x) { return "(" + (x > 0 ? "+" : "") + ft(x) + ")"; }       // TeX: (+7), (-7)
  function warn(k) { return '<span class="warn">' + u(k) + "</span>"; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function rnz(a, b) { var x; do { x = rint(a, b); } while (!x); return x; }
  function hint(s) { return '<div class="hint">' + s + "</div>"; }
  function sgnW(x) { return x > 0 ? "+" : "−"; }
  function readInt(w, k, max) { var el = w.querySelector('[data-k="' + k + '"]'), x = pint(el.value); return isNaN(x) || Math.abs(x) > max ? null : x; }
  function readList(s, maxN, maxV) {
    var p = norm(s).split(/[,;]+/).filter(function (x) { return x !== ""; });
    if (!p.length || p.length > maxN) return null;
    var v = p.map(pint);
    return v.every(function (x) { return !isNaN(x) && Math.abs(x) <= maxV; }) ? v : null;
  }
  function quickFill(w, keys, render) {
    w.querySelectorAll(".quick button[data-b]").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = b.dataset.b.split("|");
        keys.forEach(function (k, i) { var el = w.querySelector('[data-k="' + k + '"]'); if (el && p[i] != null) el.value = p[i]; });
        render();
      });
    });
  }

  /* ---------- recta numèrica en SVG ---------- */
  var STEPS = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000];
  function axis(lo, hi, Y, opt) {
    opt = opt || {};
    var st = 1;
    for (var i = 0; i < STEPS.length; i++) { st = STEPS[i]; if ((hi - lo) / st <= (opt.max || 20)) break; }
    lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st) * st;
    var X0 = 34, X1 = 586, x = function (v) { return X0 + (v - lo) / (hi - lo) * (X1 - X0); };
    var s = '<line class="sv-ax" x1="' + (X0 - 22) + '" y1="' + Y + '" x2="' + (X1 + 22) + '" y2="' + Y + '"/>' +
      '<path class="sv-ax" fill="none" d="M' + (X1 + 14) + " " + (Y - 6) + " L" + (X1 + 24) + " " + Y + " L" + (X1 + 14) + " " + (Y + 6) + '"/>' +
      '<path class="sv-ax" fill="none" d="M' + (X0 - 14) + " " + (Y - 6) + " L" + (X0 - 24) + " " + Y + " L" + (X0 - 14) + " " + (Y + 6) + '"/>';
    for (var v = lo; v <= hi; v += st) {
      s += '<line class="sv-ax" x1="' + x(v) + '" y1="' + (Y - 6) + '" x2="' + x(v) + '" y2="' + (Y + 6) + '"/>';
      if (!opt.noLab) s += '<text class="' + (v ? "sv-t" : "sv-tb") + '" x="' + x(v) + '" y="' + (Y + 24) + '" text-anchor="middle">' + fh(v) + "</text>";
    }
    return { x: x, s: s, lo: lo, hi: hi, st: st };
  }
  function head(x, y, dir, cls) { return '<path class="' + cls + '" d="M' + x + " " + y + " l" + (-9 * dir) + " -5 l0 10 z" + '"/>'; }
  function svgWrap(h, s, lab) { return '<svg viewBox="0 0 620 ' + h + '" role="img" aria-label="' + lab + '">' + s + "</svg>"; }

  /* ======== divisibilitat (de 1r ESO, unitat 2) ======== */
  function pnat(s) {
    s = String(s).trim().replace(/[\s  ]/g, "");
    if (/^\d{1,3}([.,]\d{3})+$/.test(s)) s = s.replace(/[.,]/g, "");
    if (!/^\d+$/.test(s)) return NaN;
    return parseInt(s, 10);
  }  function isPrime(n) { if (n < 2) return false; for (var i = 2; i * i <= n; i++) if (n % i === 0) return false; return true; }
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
  function quickFillN(w, keys, render) {
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
      if (isNaN(a) || isNaN(b) || a > 999999999 || b > 999999999) { info.innerHTML = warn("writeN"); return; }
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
    quickFillN(w, ["a", "b"], render);
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
    quickFillN(w, ["n", "m"], render);
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
      if (isNaN(n) || n < 1 || n > 999999999) { dg.innerHTML = cc.innerHTML = ""; info.innerHTML = warn("writeN"); return; }
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
      if (isNaN(n) || n < 2 || n > 100000) { info.innerHTML = warn("pmBad"); return; }
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
    quickFillN(w, ["a", "b", "c"], render);
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
    quickFillN(w, ["a", "b", "c"], render);
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
    quickFillN(w, ["a", "b"], function () { d = null; render(); });
    onLang(render);
  }

  /* ---------- entrenadors ---------- */

  /* ---------- giny: enters en context ---------- */
  function wCtx() {
    var w = document.getElementById("w-ctx"); if (!w) return;
    var V = w.querySelector('[data-k="v"]'), ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function render() {
      var c = segVal(w) || "temp", v = pint(V.value), C = u("ctx")[c];
      if (isNaN(v) || Math.abs(v) > 9999) { ch.innerHTML = ""; info.innerHTML = warn("cxBad"); return; }
      var R = 5; while (R < Math.abs(v) * 1.15) R = R < 10 ? 10 : R * (String(R).charAt(0) === "2" ? 2.5 : 2);
      var H = 280, T = 20, B = 260, y = function (t) { return T + (R - t) / (2 * R) * (B - T); }, s = "";
      s += '<rect class="cx-up" x="150" y="' + T + '" width="120" height="' + (y(0) - T) + '" rx="6"/><rect class="cx-dn" x="150" y="' + y(0) + '" width="120" height="' + (B - y(0)) + '" rx="6"/>';
      for (var k = -5; k <= 5; k++) { var t = R * k / 5; s += '<line class="sv-ax" x1="142" y1="' + y(t) + '" x2="150" y2="' + y(t) + '"/><text class="' + (k ? "sv-t" : "sv-tb") + '" x="136" y="' + (y(t) + 4) + '" text-anchor="end">' + fs(t).replace("+0", "0") + "</text>"; }
      s += '<line class="cx-zero" x1="144" y1="' + y(0) + '" x2="300" y2="' + y(0) + '"/><text class="sv-tb" x="306" y="' + (y(0) + 5) + '">' + C.zero + "</text>";
      s += '<text class="sv-t" x="306" y="' + (T + 14) + '">▲ ' + C.up + '</text><text class="sv-t" x="306" y="' + (B - 4) + '">▼ ' + C.down + "</text>";
      if (v) s += '<rect class="' + (v > 0 ? "cx-bp" : "cx-bn") + '" x="190" y="' + Math.min(y(0), y(v)) + '" width="40" height="' + Math.abs(y(v) - y(0)) + '"/>';
      s += '<line class="cx-mk" x1="176" y1="' + y(v) + '" x2="244" y2="' + y(v) + '"/><text class="cx-lab" x="252" y="' + (y(v) + (v > 0 ? -6 : 18)) + '">' + fs(v).replace("+0", "0") + "</text>";
      ch.innerHTML = '<svg viewBox="0 0 620 ' + H + '" role="img" aria-label="escala">' + s + "</svg>";
      var say = v > 0 ? fill(C.p, { n: fh(v) }) : v < 0 ? fill(C.n, { n: fh(-v) }) : C.z;
      var h = c === "year" && !v ? warn("cxYear0") : "<div>" + u("cxSay") + " <b>" + say + "</b></div><div>" + u("cxNum") + " " + tex((v > 0 ? "+" : "") + ft(v), true) + "</div>";
      info.innerHTML = h + hint(fill(u("cxRef"), { z: C.zero }));
    }
    V.addEventListener("input", render);
    segBind(w, render);
    w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { var p = b.dataset.b.split("|"); segSet(w, p[0]); V.value = p[1]; render(); }); });
    onLang(render);
  }

  /* ---------- giny: recta numèrica i ordre ---------- */
  function lineSVG(vals, hl) {
    var mn = Math.min.apply(null, vals.concat([0])), mx = Math.max.apply(null, vals.concat([0]));
    var A = axis(mn - 1, mx + 1, 52), s = A.s, last = [-99, -99], uniq = vals.filter(function (x, i) { return vals.indexOf(x) === i; }).sort(function (a, b) { return a - b; });
    uniq.forEach(function (v) {
      var X = A.x(v), row = X - last[0] < 30 ? (X - last[1] < 30 ? 0 : 1) : 0;
      if (row === 0) last[0] = X; else last[1] = X;
      var ly = row ? 92 : 22;
      s += '<line class="ln-st" x1="' + X + '" y1="' + (row ? 58 : 46) + '" x2="' + X + '" y2="' + (row ? 80 : 28) + '"/>';
      s += '<circle class="' + (hl && hl.indexOf(v) >= 0 ? "ln-hl" : v < 0 ? "ln-n" : v > 0 ? "ln-p" : "ln-z") + '" cx="' + X + '" cy="52" r="6.5"/><text class="ln-lab" x="' + X + '" y="' + (ly + 4) + '" text-anchor="middle">' + fh(v) + "</text>";
    });
    return svgWrap(104, s.replace(/<text class="sv-t[b]?" [^>]*>[^<]*<\/text>/g, function (m) { return m.replace(/y="(\d+)"/, 'y="$1" opacity=".55"'); }), "recta");
  }
  function wLine() {
    var w = document.getElementById("w-line"); if (!w) return;
    var I = w.querySelector('[data-k="v"]'), ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function render() {
      var v = readList(I.value, 15, 1000), up = segVal(w) !== "desc";
      if (!v) { ch.innerHTML = ""; info.innerHTML = warn("lnBad"); return; }
      ch.innerHTML = lineSVG(v);
      var o = v.slice().sort(function (a, b) { return up ? a - b : b - a; });
      var h = "<div><b>" + u(up ? "lnAsc" : "lnDesc") + "</b></div>" + tex(o.map(function (x, i) { return (i ? (x === o[i - 1] ? "=" : up ? "<" : ">") : "") + ft(x); }).join(""), true);
      if (v.length === 2) {
        var a = v[0], b = v[1];
        h += a === b ? hint(u("lnEq")) : "<div>" + fill(u("lnCmp"), { a: fh(a), b: fh(b), s: u(a > b ? "lnR" : "lnL") }) + " " + tex(ft(a) + (a > b ? ">" : "<") + ft(b)) + "</div>";
      }
      if (o.some(function (x, i) { return i && x === o[i - 1]; })) h += hint(u("lnRep"));
      info.innerHTML = h + hint(u("lnRight"));
    }
    I.addEventListener("input", render);
    segBind(w, render);
    quickFill(w, ["v"], render);
    onLang(render);
  }

  /* ---------- giny: valor absolut i oposat ---------- */
  function wAbs() {
    var w = document.getElementById("w-abs"); if (!w) return;
    var A = w.querySelector('[data-k="a"]'), ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function render() {
      var a = pint(A.value);
      if (isNaN(a) || Math.abs(a) > 1000) { ch.innerHTML = ""; info.innerHTML = warn("abBad"); return; }
      var d = Math.abs(a), R = Math.max(5, d + 1), X = axis(-R, R, 70), s = X.s, x0 = X.x(0);
      if (d) {
        [a, -a].forEach(function (v, i) {
          var xv = X.x(v), cls = i ? "ab-op" : "ab-a";
          s += '<path class="' + cls + '" fill="none" d="M' + x0 + " 64 Q " + (x0 + xv) / 2 + " 4 " + xv + ' 64"/>';
          s += '<text class="ab-t ' + cls + 't" x="' + (x0 + xv) / 2 + '" y="28" text-anchor="middle">' + fh(d) + "</text>";
          s += '<circle class="' + (i ? "ln-op" : "ln-hl") + '" cx="' + xv + '" cy="70" r="7"/>';
        });
      } else s += '<circle class="ln-hl" cx="' + x0 + '" cy="70" r="7"/>';
      ch.innerHTML = svgWrap(104, s, "valor absolut");
      var o = { a: fh(a), d: fh(d), o: fh(-a), t: fh(2 * d) };
      info.innerHTML = tex("|" + ft(a) + "|=" + ft(d) + "\\qquad \\text{op}" + "(" + ft(a) + ")=" + ft(-a), true) +
        "<div>" + fill(u("abDist"), o) + "</div>" + (d ? "<div>" + fill(u("abOp"), o) + "</div>" + hint(fill(u("abPair"), o)) : hint(u("abZero")));
    }
    A.addEventListener("input", render);
    quickFill(w, ["a"], render);
    onLang(render);
  }

  /* ---------- giny: suma i resta en la recta ---------- */
  function sumRule(x, y) {
    var r = x + y, o = { x: fh(Math.abs(x)), y: fh(Math.abs(y)), s: "", g: "" };
    if (!y || !x) return u("adZ");
    if (!r) return u("adZero");
    if ((x > 0) === (y > 0)) { o.s = fh(Math.abs(r)); o.g = sgnW(x); return fill(u("adSame"), o); }
    var big = Math.abs(x) >= Math.abs(y) ? x : y; o.x = fh(Math.max(Math.abs(x), Math.abs(y))); o.y = fh(Math.min(Math.abs(x), Math.abs(y))); o.s = fh(Math.abs(r)); o.g = sgnW(big);
    return fill(u("adDiff"), o);
  }
  function wAdd() {
    var w = document.getElementById("w-add"); if (!w) return;
    var ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function render() {
      var a = readInt(w, "a", 200), b = readInt(w, "b", 200), op = segVal(w) || "+";
      if (a == null || b == null) { ch.innerHTML = ""; info.innerHTML = warn("adBad"); return; }
      var c = op === "+" ? b : -b, r = a + c, X = axis(Math.min(0, a, r) - 1, Math.max(0, a, r) + 1, 70), s = X.s, xa = X.x(a), xr = X.x(r);
      if (c) {
        var dir = c > 0 ? 1 : -1;
        s += '<path class="ad-arr" fill="none" d="M' + xa + " 62 Q " + (xa + xr) / 2 + " 6 " + (xr - 4 * dir) + ' 58"/>' + head(xr, 60, dir, "ad-hd");
        s += '<text class="ad-t" x="' + (xa + xr) / 2 + '" y="24" text-anchor="middle">' + fs(c) + "</text>";
      }
      s += '<circle class="ln-z" cx="' + xa + '" cy="70" r="6.5"/><circle class="ln-hl" cx="' + xr + '" cy="70" r="7"/>';
      ch.innerHTML = svgWrap(104, s, "suma");
      var h = tex(ft(a) + op + fp(b) + "=" + (op === "-" ? ft(a) + "+" + fp(c) + "=" : "") + "\\boxed{" + ft(r) + "}", true);
      if (op === "-") h += hint(u("adSub") + " " + tex("-" + fp(b) + "=+" + fp(c)));
      h += "<div>" + sumRule(a, c) + "</div>";
      if (c) h += hint(fill(u("adMove"), { a: fh(a), m: fh(Math.abs(c)), s: u(c > 0 ? "lnR" : "lnL") }));
      info.innerHTML = h;
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, render);
    w.querySelectorAll(".quick button[data-b]").forEach(function (bt) { bt.addEventListener("click", function () { var p = bt.dataset.b.split("|"); w.querySelector('[data-k="a"]').value = p[0]; segSet(w, p[1]); w.querySelector('[data-k="b"]').value = p[2]; render(); }); });
    onLang(render);
  }

  /* ---------- parèntesis en sumes i restes ---------- */
  function parTerms(s) {
    s = norm(s);
    var t = [], m;
    while (s.length) {
      if ((m = s.match(/^([+-]?)\(([+-]?)(\d{1,6})\)/))) t.push({ o: m[1] || "+", i: m[2] || "+", n: +m[3], p: true, ou: !!m[1], iu: !!m[2] });
      else if ((m = s.match(/^([+-]?)(\d{1,6})/))) t.push({ o: m[1] || "+", i: "+", n: +m[2], p: false, ou: !!m[1] });
      else return null;
      if (t.length > 1 && !t[t.length - 1].ou) return null;
      s = s.slice(m[0].length);
    }
    if (!t.length || t.length > 12) return null;
    t.forEach(function (x) { x.s = x.o === x.i ? 1 : -1; x.v = x.s * x.n; });
    return t;
  }
  function termTex(x, first) {
    var o = first && x.o === "+" && !x.ou ? "" : x.o;
    return o + (x.p ? "(" + (x.iu ? x.i : "") + ft(x.n) + ")" : ft(x.n));
  }
  function flatTex(t) { return t.map(function (x, i) { return (x.v < 0 ? "-" : i ? "+" : "") + ft(x.n); }).join(""); }
  function parSteps(t) {
    var P = 0, N = 0, out = [];
    t.forEach(function (x) { if (x.v > 0) P += x.v; else N -= x.v; });
    var has = t.some(function (x) { return x.p; });
    out.push(t.map(function (x, i) { return termTex(x, !i); }).join("") + (has ? "=" + flatTex(t) : ""));
    if (t.length > 2 && P && N) out.push("=" + ft(P) + "-" + ft(N));
    out.push("=\\boxed{" + ft(P - N) + "}");
    return { tex: out.join(""), P: P, N: N, has: has };
  }
  function wPar() {
    var w = document.getElementById("w-par"); if (!w) return;
    var inp = w.querySelector(".tin"), out = w.querySelector(".pchips"), info = w.querySelector(".info");
    function render() {
      var t = parTerms(inp.value);
      if (!t) { out.innerHTML = ""; info.innerHTML = warn("prBad"); return; }
      var r = parSteps(t);
      out.innerHTML = r.has ? '<span class="ql">' + u("prRule") + "</span>" + t.filter(function (x) { return x.p; }).map(function (x) {
        return '<span class="pch ' + (x.s > 0 ? "p" : "n") + '">' + tex(x.o + "(" + x.i + ft(x.n) + ")\\ \\to\\ " + (x.s > 0 ? "+" : "-") + ft(x.n)) + '<small>' + x.o + " ( " + x.i + " → " + (x.s > 0 ? "+" : "−") + "</small></span>";
      }).join("") : '<span class="ql">' + u("prOnly") + "</span>";
      var g = r.P && r.N && t.length > 2 ? hint(u("prGroup") + " " + tex("(" + t.filter(function (x) { return x.v > 0; }).map(function (x) { return ft(x.n); }).join("+") + ")-(" + t.filter(function (x) { return x.v < 0; }).map(function (x) { return ft(x.n); }).join("+") + ")=" + ft(r.P) + "-" + ft(r.N))) : "";
      info.innerHTML = tex(r.tex, true) + g;
    }
    inp.addEventListener("input", render);
    w.querySelectorAll(".quick button[data-e]").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.dataset.e; render(); }); });
    onLang(render);
  }

  /* ---------- giny: regla dels signes ---------- */
  function wSign() {
    var w = document.getElementById("w-sign"); if (!w) return;
    var tb = w.querySelector(".sgtab"), info = w.querySelector(".info");
    function render() {
      var a = readInt(w, "a", 1000), b = readInt(w, "b", 1000), op = segVal(w) || "·";
      tb.querySelectorAll("td").forEach(function (td) { td.classList.remove("on"); });
      tb.querySelector(".sop").textContent = op;
      if (a == null || b == null) { info.innerHTML = warn("sgBad"); return; }
      var sym = op === "·" ? "\\cdot " : ":";
      if (op === ":" && !b) { info.innerHTML = warn("sgDiv0"); return; }
      if (op === ":" && a % b) { info.innerHTML = tex(fp(a) + ":" + fp(b), true) + '<span class="warn">' + fill(u("sgInex"), { a: fh(a), b: fh(b) }) + "</span>"; return; }
      var r = op === "·" ? a * b : a / b;
      if (a && b) tb.querySelector('td[data-c="' + (a > 0 ? "p" : "n") + (b > 0 ? "p" : "n") + '"]').classList.add("on");
      var h = tex(fps(a) + sym + fps(b) + "=" + (a && b ? (r > 0 ? "+" : "-") + "(" + ft(Math.abs(a)) + sym + ft(Math.abs(b)) + ")=" : "") + "\\boxed{" + ft(r) + "}", true);
      if (!a || !b) h += hint(op === "·" || !a ? u("sgZero") : "");
      else h += "<div>" + fill(u("sgAbs"), { x: fh(Math.abs(a)), y: fh(Math.abs(b)), o: op, r: fh(Math.abs(r)) }) + "</div><div>" + u((a > 0) === (b > 0) ? "sgSame" : "sgDiff") + "</div>";
      info.innerHTML = h;
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, render);
    w.querySelectorAll(".quick button[data-b]").forEach(function (bt) { bt.addEventListener("click", function () { var p = bt.dataset.b.split("|"); w.querySelector('[data-k="a"]').value = p[0]; segSet(w, p[1]); w.querySelector('[data-k="b"]').value = p[2]; render(); }); });
    onLang(render);
  }

  /* ---------- operacions combinades pas a pas (amb enters) ---------- */
  function tokenize(s) {
    s = norm(s).replace(/\{/g, "[").replace(/\}/g, "]");
    var t = [], i = 0;
    while (i < s.length) {
      var c = s.charAt(i);
      if (/\d/.test(c)) { var m = s.slice(i).match(/^\d+/)[0]; if (m.length > 9) return null; t.push({ k: "n", v: parseInt(m, 10) }); i += m.length; continue; }
      if ("+-·:()[]^√".indexOf(c) >= 0) { t.push({ k: c }); i++; continue; }
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
      var a = un();
      for (;;) {
        var p = peek();
        if (p === "·" || p === ":") { i++; a = { t: "b", op: p, l: a, r: un() }; }
        else if (p === "(" || p === "[" || p === "√") a = { t: "b", op: "·", l: a, r: pw() };
        else return a;
      }
    }
    /* un signe davant d'un nombre forma un enter; davant d'un parèntesi és «l'oposat de» */
    function un() {
      var p = peek();
      if (p === "+" || p === "-") {
        i++;
        if (peek() === "n" && !(t[i + 1] && t[i + 1].k === "^")) { var v = t[i++].v; return { t: "n", v: p === "-" ? -v : v }; }
        var e = un();
        return p === "-" ? { t: "u", e: e } : e;
      }
      return pw();
    }
    /* potència: base^exponent; −3^2 és l'oposat de 3^2, però (−3)^2 té base −3 */
    function pw() { var b = prim(); if (peek() === "^") { i++; return { t: "w", b: b, e: prim() }; } return b; }
    function prim() {
      var p = peek();
      if (p === "n") return { t: "n", v: t[i++].v };
      if (p === "√") { i++; return { t: "r", e: prim() }; }
      if (p === "(" || p === "[") { i++; var e = expr(), cl = p === "(" ? ")" : "]"; if (peek() !== cl) throw 0; i++; return e.t === "n" ? e : { t: "p", k: p, e: e }; }
      throw 0;
    }
    try { var r = expr(); return i === t.length ? r : null; } catch (e) { return null; }
  }
  function isN(x) { return x.t === "n"; }
  function first(x, pr) {
    if (x.t === "b") return first(x.l, pr) || (pr(x) ? x : null) || first(x.r, pr);
    if (x.t === "u") return first(x.e, pr) || (pr(x) ? x : null);
    if (x.t === "w") return first(x.b, pr) || first(x.e, pr) || (pr(x) ? x : null);
    if (x.t === "r") return first(x.e, pr) || (pr(x) ? x : null);
    return pr(x) ? x : null;
  }
  function grp(x) { return x.t === "p" && !isN(x.e); }
  /* ordre: parèntesis (de dins cap a fora) → signe davant del parèntesi → · i : → + i − (sempre d'esquerra a dreta) */
  function target(x, inG) {
    var g = first(x, grp);
    if (g) return target(g.e, true);
    var y = first(x, function (z) { return z.t === "u" && isN(z.e); }) ||
      first(x, function (z) { return (z.t === "w" && isN(z.b) && isN(z.e)) || (z.t === "r" && isN(z.e)); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "·" || z.op === ":") && isN(z.l) && isN(z.r); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "+" || z.op === "-") && isN(z.l) && isN(z.r); });
    return y ? { n: y, g: !!inG } : null;
  }
  function applyOp(y) {
    if (y.t === "u") return { v: -y.e.v, k: "opp" };
    if (y.t === "w") {
      var bb = y.b.v, nn = y.e.v;
      if (nn < 0) return { err: u("hExp") };
      if (!bb && !nn) return { err: u("h00") };
      return { v: Math.pow(bb, nn), k: "pow" };
    }
    if (y.t === "r") {
      var ra = y.e.v, rs = Math.round(Math.sqrt(Math.abs(ra)));
      if (ra < 0) return { err: fill(u("hRneg"), { a: fh(ra) }) };
      if (rs * rs !== ra) return { err: fill(u("hRin"), { a: fh(ra), s: rs * rs > ra ? rs - 1 : rs }) };
      return { v: rs, k: "root" };
    }
    var a = y.l.v, b = y.r.v;
    if (y.op === "+") return { v: a + b, k: "add" };
    if (y.op === "-") return { v: a - b, k: "sub" };
    if (y.op === "·") return { v: a * b, k: "mul" };
    return !b ? { err: u("hDiv0") } : a % b ? { err: fill(u("hDiv"), { a: fh(a), b: fh(b) }) } : { v: a / b, k: "div" };
  }
  function repl(x, tg, nv) {
    if (x === tg) return nv;
    if (x.t === "b") return { t: "b", op: x.op, l: repl(x.l, tg, nv), r: repl(x.r, tg, nv) };
    if (x.t === "p") { var e = repl(x.e, tg, nv); return isN(e) ? e : { t: "p", k: x.k, e: e }; }
    if (x.t === "u") { var ue = repl(x.e, tg, nv); return isN(ue) && (x.e.t === "w" || x.e.t === "r") ? { t: "n", v: -ue.v } : { t: "u", e: ue }; }
    if (x.t === "w") return { t: "w", b: repl(x.b, tg, nv), e: repl(x.e, tg, nv) };
    if (x.t === "r") return { t: "r", e: repl(x.e, tg, nv) };
    return x;
  }
  /* lead: el terme va al principi (de tota l'expressió o d'un parèntesi), i un negatiu no necessita parèntesi */
  function tx(x, tg, val, lead) {
    var s;
    if (x.t === "n") s = x.v < 0 && !lead ? "(" + ft(x.v) + ")" : ft(x.v);
    else if (x.t === "p") s = x.k === "(" ? "\\left(" + tx(x.e, tg, val, true) + "\\right)" : "\\left[" + tx(x.e, tg, val, true) + "\\right]";
    else if (x.t === "u") { s = "-" + (isN(x.e) ? "(" + ft(x.e.v) + ")" : tx(x.e, tg, val, false)); if (!lead && (x.e.t === "w" || x.e.t === "r")) s = "(" + s + ")"; }
    else if (x.t === "w") s = (isN(x.b) ? (x.b.v < 0 ? "(" + ft(x.b.v) + ")" : ft(x.b.v)) : "{" + tx(x.b, tg, val, true) + "}") + "^{" + tx(x.e, tg, val, true) + "}";
    else if (x.t === "r") s = "\\sqrt{" + tx(x.e, tg, val, true) + "}";
    else s = tx(x.l, tg, val, lead) + { "+": "+", "-": "-", "·": "\\cdot ", ":": ":" }[x.op] + tx(x.r, tg, val, false);
    if (x === tg) s = "\\underbrace{\\htmlClass{hl}{" + s + "}}_{\\htmlClass{hlv}{" + ft(val) + "}}";
    return s;
  }
  function run(s) {
    var tree = parseExpr(s), rows = [];
    if (!tree) return { err: u("hParse"), rows: rows };
    for (var guard = 0; guard < 80; guard++) {
      var tg = target(tree);
      if (!tg) break;
      var r = applyOp(tg.n);
      if (!r.err && Math.abs(r.v) > 1e12) r = { err: u("hBig") };
      if (r.err) return { err: r.err, rows: rows, last: tx(tree, null, 0, true) };
      rows.push({ t: tx(tree, tg.n, r.v, true), k: r.k, g: tg.g });
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

  /* ---------- giny: ascensor, temperatures i comptes ---------- */
  function wElev() {
    var w = document.getElementById("w-elev"); if (!w) return;
    var ch = w.querySelector(".chart"), info = w.querySelector(".info");
    function say(c, v) { var C = u("ctx")[c]; return v > 0 ? fill(C.p, { n: fh(v) }) : v < 0 ? fill(C.n, { n: fh(-v) }) : C.z; }
    function render() {
      var c = segVal(w) || "floor", s0 = readInt(w, "s", 9999), mv = readList(w.querySelector('[data-k="m"]').value, 20, 9999);
      if (s0 == null || !mv) { ch.innerHTML = ""; info.innerHTML = warn("elBad"); return; }
      var vals = [s0]; mv.forEach(function (d) { vals.push(vals[vals.length - 1] + d); });
      var n = vals.length, mn = Math.min.apply(null, vals.concat([0])), mx = Math.max.apply(null, vals.concat([0]));
      if (mx === mn) mx = mn + 1;
      var L = 56, Rr = 600, T = 18, B = 222, X = function (i) { return L + i * (Rr - L) / (n - 1 || 1); }, Y = function (v) { return T + (mx - v) / (mx - mn) * (B - T); };
      var st = 1; for (var q = 0; q < STEPS.length; q++) { st = STEPS[q]; if ((mx - mn) / st <= 8) break; }
      var s = "";
      for (var g = Math.ceil(mn / st) * st; g <= mx; g += st) s += '<line class="' + (g ? "sv-grid" : "el-zero") + '" x1="' + L + '" y1="' + Y(g) + '" x2="' + Rr + '" y2="' + Y(g) + '"/><text class="' + (g ? "sv-t" : "sv-tb") + '" x="' + (L - 8) + '" y="' + (Y(g) + 4) + '" text-anchor="end">' + fh(g) + "</text>";
      var d = "M" + X(0) + " " + Y(vals[0]);
      for (var i = 1; i < n; i++) d += " L" + X(i) + " " + Y(vals[i - 1]) + " L" + X(i) + " " + Y(vals[i]);
      s += '<path class="el-path" fill="none" d="' + d + '"/>';
      for (var j = 0; j < n; j++) {
        s += '<circle class="' + (j === n - 1 ? "ln-hl" : vals[j] < 0 ? "ln-n" : vals[j] > 0 ? "ln-p" : "ln-z") + '" cx="' + X(j) + '" cy="' + Y(vals[j]) + '" r="' + (j === n - 1 ? 7 : 5) + '"/>';
        if (j) s += '<text class="el-d ' + (mv[j - 1] > 0 ? "up" : "dn") + '" x="' + (X(j) - (X(j) - X(j - 1)) / 2) + '" y="' + (Y(vals[j - 1]) + (mv[j - 1] > 0 ? 16 : -7)) + '" text-anchor="middle">' + fs(mv[j - 1]) + "</text>";
      }
      s += '<text class="sv-t" x="' + X(0) + '" y="' + (B + 24) + '" text-anchor="middle">' + u("elStart") + '</text><text class="sv-t" x="' + X(n - 1) + '" y="' + (B + 24) + '" text-anchor="end">' + u("elEnd") + "</text>";
      ch.innerHTML = '<svg viewBox="0 0 620 252" role="img" aria-label="gràfic">' + s + "</svg>";
      var f = vals[n - 1], un = u("elUnit")[c];
      info.innerHTML = tex(ft(s0) + mv.map(function (x) { return (x >= 0 ? "+" : "") + ft(x); }).join("") + "=\\boxed{" + ft(f) + "}", true) +
        "<div>" + u("elSay") + " <b>" + say(c, f) + "</b></div>" +
        hint(fill(u("elVar"), { v: fs(f - s0) + un }) + " " + fill(u("elMax"), { M: fh(Math.max.apply(null, vals)) + un, m: fh(Math.min.apply(null, vals)) + un }));
    }
    w.querySelectorAll(".tin").forEach(function (x) { x.addEventListener("input", render); });
    segBind(w, render);
    w.querySelectorAll(".quick button[data-b]").forEach(function (bt) { bt.addEventListener("click", function () { var p = bt.dataset.b.split("|"); segSet(w, p[0]); w.querySelector('[data-k="s"]').value = p[1]; w.querySelector('[data-k="m"]').value = p[2]; render(); }); });
    onLang(render);
  }

  /* ---------- entrenadors ---------- */

  /* ---------- giny: potències d'enters ---------- */
  function wPowZ() {
    var w = document.getElementById("w-powz"); if (!w) return;
    var out = w.querySelector(".pz"), info = w.querySelector(".info");
    function render() {
      var b = readInt(w, "b", 20), n = readInt(w, "n", 12);
      if (b === null || n === null || n < 0) { out.innerHTML = ""; info.innerHTML = warn("pzBad"); return; }
      if (!b && !n) { out.innerHTML = ""; info.innerHTML = warn("pz00"); return; }
      var v = Math.pow(b, n), B = fp(b), prod;
      if (n === 0) prod = "1";
      else if (n <= 8) { var f = []; for (var k = 0; k < n; k++) f.push(B); prod = f.join("\\cdot "); }
      else prod = "\\underbrace{" + B + "\\cdot " + B + "\\cdots " + B + "}_{\\text{" + fill(u("pzMany"), { n: n }) + "}}";
      var h = tex(B + "^{" + n + "}" + (n > 1 ? "=" + prod : "") + "=" + ft(v), true);
      var t = n === 0 ? u("pzExp0") : !b ? u("pzZero") : n === 1 ? u("pzOne") : b > 0 ? u("pzPos") : fill(u(n % 2 ? "pzOdd" : "pzEven"), { n: n });
      if (b < 0 && n > 0) t += "<br>" + u("pzMinus") + " " + tex("-" + ft(-b) + "^{" + n + "}=-\\left(" + ft(-b) + "^{" + n + "}\\right)=" + ft(-Math.pow(-b, n)) + "\\quad\\text{vs.}\\quad " + B + "^{" + n + "}=" + ft(v));
      out.innerHTML = h; info.innerHTML = hint(t);
    }
    w.querySelectorAll("input").forEach(function (el) { el.addEventListener("input", render); });
    quickFill(w, ["b", "n"], render);
    onLang(render);
  }

  /* ---------- giny: arrel quadrada d'un enter (exacta o entera) ---------- */
  function wRootZ() {
    var w = document.getElementById("w-rootz"); if (!w) return;
    var out = w.querySelector(".rz"), info = w.querySelector(".info");
    function render() {
      var a = readInt(w, "a", 1000000);
      if (a === null) { out.innerHTML = ""; info.innerHTML = warn("rzBad"); return; }
      if (a < 0) { out.innerHTML = tex("\\sqrt{" + ft(a) + "}\\ \\text{?}\\qquad (+k)^2\\ge 0,\\ \\ (-k)^2\\ge 0", true); info.innerHTML = '<span class="warn">' + u("rzNeg") + "</span>"; return; }
      var s = Math.floor(Math.sqrt(a)); while (s * s > a) s--; while ((s + 1) * (s + 1) <= a) s++;
      var r = a - s * s;
      if (!a) { out.innerHTML = tex("\\sqrt{0}=0", true); info.innerHTML = hint(u("rzZero")); return; }
      if (!r) {
        out.innerHTML = tex("\\sqrt{" + ft(a) + "}=\\pm" + ft(s) + "\\qquad (+" + ft(s) + ")^2=" + ft(a) + "\\qquad (-" + ft(s) + ")^2=" + ft(a), true);
        info.innerHTML = hint(fill(u("rzEx"), { a: fh(a), s: fh(s) }));
        return;
      }
      out.innerHTML = tex(ft(s) + "^2=" + ft(s * s) + "\\ <\\ " + ft(a) + "\\ <\\ " + ft(s + 1) + "^2=" + ft((s + 1) * (s + 1)), true) +
        tex("\\sqrt{" + ft(a) + "}\\approx " + ft(s) + "\\qquad " + ft(a) + "=" + ft(s) + "^2+" + ft(r), true);
      info.innerHTML = hint(fill(u("rzIn"), { a: fh(a), lo: fh(s * s), hi: fh((s + 1) * (s + 1)), s: fh(s), r: fh(r) }) + "<br>" + fill(u("rzChk"), { s: fh(s), r: fh(r), a: fh(a) }));
    }
    w.querySelectorAll("input").forEach(function (el) { el.addEventListener("input", render); });
    quickFill(w, ["a"], render);
    onLang(render);
  }

  function stepsTex(e) { var r = run(e); return r.rows.map(function (x) { return tex(x.t, true); }).join("") + tex("\\boxed{" + ft(r.v) + "}", true); }
  var GEN = {
    pow: function () {
      var k = rint(0, 4), b, n, e, ans, sol;
      if (k <= 1) { b = rnz(-6, 6); n = Math.abs(b) > 3 ? rint(0, 3) : rint(0, 5); e = fp(b) + "^{" + n + "}"; ans = Math.pow(b, n); }
      else if (k === 2) { b = rint(2, 5); n = rint(2, 4); e = "-" + b + "^{" + n + "}"; ans = -Math.pow(b, n); }
      else if (k === 3) { var sr = rint(1, 15); e = "\\sqrt{" + sr * sr + "}"; ans = sr;
        return { ans: ans, q: function () { return u("dRoot") + " $" + e + "$"; }, s: function () { return tex(e + "=\\pm" + sr + "\\ \\to\\ \\boxed{" + sr + "}", true); } }; }
      else { var m = rint(2, 5), p = rint(1, 3); b = pick([-2, -3, -1, 2, -5]); e = fp(b) + "^{" + (m + p) + "}:" + fp(b) + "^{" + m + "}"; ans = Math.pow(b, p);
        sol = e + "=" + fp(b) + "^{" + p + "}=\\boxed{" + ft(ans) + "}";
        return { ans: ans, q: function () { return u("dPow") + " $" + e + "$"; }, s: function () { return tex(sol, true); } }; }
      return { ans: ans, q: function () { return u("dPow") + " $" + e + "$"; }, s: function () { return tex(e + "=\\boxed{" + ft(ans) + "}", true); } };
    },
    comb2: function () {
      for (;;) {
        var a = rnz(-5, 5), b = rnz(-4, 4), c = rnz(-9, 9), s = rint(2, 9), k = rint(0, 4), e;
        if (k === 0) e = "(" + a + ")^2-" + Math.abs(c) + "·(" + b + ")";
        else if (k === 1) e = "√" + s * s + "-(" + b + ")^3";
        else if (k === 2) e = "-" + Math.abs(a) + "^2+(" + b + ")·(" + c + ")";
        else if (k === 3) e = "[(" + a + ")^2-" + s + "]·(" + b + ")";
        else { var bs = s * s - c; if (bs < 0) continue; e = "√(" + bs + (c > 0 ? "+" : "-") + Math.abs(c) + ")·(" + b + ")-" + Math.abs(a) + "^2"; }
        var res = run(e);
        if (!res.ok || Math.abs(res.v) > 200) continue;
        return { ans: res.v, q: function () { return u("dCalc") + " $" + tx(parseExpr(e), null, 0, true) + "$"; }, s: function () { return stepsTex(e); } };
      }
    },

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
    },
    ord: function () {
      var v = [];
      while (v.length < rint(5, 7)) { var x = rint(-25, 25); if (v.indexOf(x) < 0) v.push(x); }
      var mx = Math.random() < .5, o = v.slice().sort(function (a, b) { return a - b; }), ans = mx ? o[o.length - 1] : o[0];
      return { ans: ans, q: function () { return u(mx ? "dMax" : "dMin") + " $" + v.map(ft).join(",\\ \\ ") + "$"; },
        s: function () { return lineSVG(v, [ans]) + tex(o.map(ft).join("<"), true); } };
    },
    abs: function () {
      var a = rnz(-30, 30), f = rint(0, 5), e, ans;
      if (f === 0) { e = "|" + ft(a) + "|"; ans = Math.abs(a); }
      else if (f === 1) { e = "\\text{op}(" + ft(a) + ")"; ans = -a; }
      else if (f === 2) { e = "\\text{op}(\\text{op}(" + ft(a) + "))"; ans = a; }
      else if (f === 3) { e = "|\\text{op}(" + ft(a) + ")|"; ans = Math.abs(a); }
      else if (f === 4) { e = "\\text{op}(|" + ft(a) + "|)"; ans = -Math.abs(a); }
      else { var d = 2 * rint(2, 40); return { ans: -d / 2, q: function () { return fill(u("dOpp"), { d: d }); }, s: function () { return tex(ft(d) + ":2=" + ft(d / 2) + "\\ \\to\\ " + ft(-d / 2) + "\\text{ i }" + ft(d / 2) + "\\ \\to\\ \\boxed{" + ft(-d / 2) + "}", true); } }; }
      return { ans: ans, q: function () { return u("dCalc") + " $" + e + "$"; }, s: function () { return tex(e + "=\\boxed{" + ft(ans) + "}", true); } };
    },
    add: function () {
      var a = rnz(-15, 15), b = rnz(-15, 15), k = rint(0, 2), t;
      if (k === 0) t = ft(a) + (b > 0 ? "+" : "-") + ft(Math.abs(b));
      else if (k === 1) t = fps(a) + pick(["+", "-"]) + fps(b);
      else { var c = rnz(-12, 12); t = ft(a) + (b > 0 ? "+" : "-") + ft(Math.abs(b)) + (c > 0 ? "+" : "-") + ft(Math.abs(c)); }
      var e = t.replace(/\\,/g, ""), r = run(e);
      return { ans: r.v, q: function () { return u("dCalc") + " $" + t + "$"; }, s: function () { var p = parTerms(e); return tex(p ? parSteps(p).tex : t + "=\\boxed{" + ft(r.v) + "}", true); } };
    },
    par: function () {
      var n = rint(3, 5), t = [];
      for (var i = 0; i < n; i++) {
        var o = i ? pick(["+", "-"]) : pick(["", "", "-"]), x = rint(1, 15);
        t.push(Math.random() < .7 ? o + "(" + pick(["+", "-"]) + x + ")" : o + x);
      }
      var e = t.join(""), p = parTerms(e);
      return { ans: parSteps(p).P - parSteps(p).N, q: function () { return u("dCalc") + " $" + p.map(function (x, i) { return termTex(x, !i); }).join("") + "$"; }, s: function () { return tex(parSteps(p).tex, true); } };
    },
    mul: function () {
      var k = rint(0, 3), a = rnz(-12, 12), b = rnz(-12, 12);
      if (k === 0) return { ans: a * b, q: function () { return u("dCalc") + " $" + fps(a) + "\\cdot " + fps(b) + "$"; }, s: function () { return tex(fps(a) + "\\cdot " + fps(b) + "=\\boxed{" + ft(a * b) + "}", true); } };
      if (k === 1) return { ans: a, q: function () { return u("dCalc") + " $" + fps(a * b) + ":" + fps(b) + "$"; }, s: function () { return tex(fps(a * b) + ":" + fps(b) + "=\\boxed{" + ft(a) + "}", true); } };
      if (k === 2) { var c = rnz(-6, 6); a = rnz(-6, 6); b = rnz(-6, 6); return { ans: a * b * c, q: function () { return u("dCalc") + " $" + fps(a) + "\\cdot " + fps(b) + "\\cdot " + fps(c) + "$"; }, s: function () { return tex(fps(a) + "\\cdot " + fps(b) + "\\cdot " + fps(c) + "=" + fp(a * b) + "\\cdot " + fps(c) + "=\\boxed{" + ft(a * b * c) + "}", true); } }; }
      return { ans: b, q: function () { return u("dMiss") + " $" + fps(a) + "\\cdot (\\ \\square\\ )=" + ft(a * b) + "$"; }, s: function () { return tex(ft(a * b) + ":" + fps(a) + "=\\boxed{" + ft(b) + "}", true); } };
    },
    comb: function () {
      function r() { return rnz(-9, 9); }
      for (;;) {
        var a = r(), b = r(), c = r(), d = r(), k = rint(0, 5), e;
        if (k === 0) e = fps(a) + "·" + fps(b) + "+" + fps(c) + "·" + fps(d);
        else if (k === 1) e = ft(a * 3) + "-" + fps(b) + "·" + fps(c);
        else if (k === 2) e = "(" + ft(a) + (b > 0 ? "+" : "-") + ft(Math.abs(b)) + ")·" + fps(c);
        else if (k === 3) e = fps(a * b) + ":" + fps(b) + "-" + fps(c) + "·" + fps(d);
        else if (k === 4) e = ft(a) + "-[" + ft(b) + "-(" + ft(c) + (d > 0 ? "+" : "-") + ft(Math.abs(d)) + ")]";
        else e = ft(a * 2) + "+" + fps(b) + "·[" + ft(c) + (d > 0 ? "+" : "-") + ft(Math.abs(d)) + "]";
        var res = run(e);
        if (!res.ok || Math.abs(res.v) > 150) continue;
        return { ans: res.v, q: function () { return u("dCalc") + " $" + tx(parseExpr(e), null, 0, true) + "$"; }, s: function () { return stepsTex(e); } };
      }
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
      var v = pint(inp.value);
      if (isNaN(v)) { info.innerHTML = warn("write"); return; }
      done = true; tot++; good = v === q.ans; if (good) ok++;
      paint();
    }
    function fresh() { q = GEN[kind](); done = false; inp.value = ""; info.innerHTML = ""; paint(); }
    w.querySelector('[data-a="check"]').addEventListener("click", check);
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); inp.focus(); });
    w.querySelector('[data-a="neg"]').addEventListener("click", function () { var v = inp.value.trim(); inp.value = /^[−-]/.test(v) ? v.slice(1) : "−" + v; inp.focus(); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }

  /* ---------- qüestionari ---------- */
  var QUIZ = [
    {"q": {"va": "Quina d'aquestes operacions amb nombres naturals <b>no</b> sempre dona un nombre natural?", "es": "¿Cuál de estas operaciones con números naturales <b>no</b> siempre da un número natural?", "en": "Which of these operations on natural numbers does <b>not</b> always give a natural number?"}, "o": [{"va": "La suma", "es": "La suma", "en": "Addition"}, {"va": "La multiplicació", "es": "La multiplicación", "en": "Multiplication"}, {"va": "La resta", "es": "La resta", "en": "Subtraction"}, {"va": "La potència", "es": "La potencia", "en": "Powers"}], "a": 2, "e": {"va": "$3-5$ no és un nombre natural: per això necessitem els enters.", "es": "$3-5$ no es un número natural: por eso necesitamos los enteros.", "en": "$3-5$ is not a natural number: that's why we need integers."}},
    {"q": {"va": "En una divisió entera el divisor és 9, el quocient 12 i el residu 5. Quin és el dividend?", "es": "En una división entera el divisor es 9, el cociente 12 y el resto 5. ¿Cuál es el dividendo?", "en": "In a division the divisor is 9, the quotient 12 and the remainder 5. What is the dividend?"}, "o": [{"va": "$103$"}, {"va": "$113$"}, {"va": "$108$"}, {"va": "$26$"}], "a": 1, "e": {"va": "$D=d\\cdot q+r=9\\cdot12+5=113$.", "es": "$D=d\\cdot q+r=9\\cdot12+5=113$.", "en": "$D=d\\cdot q+r=9\\cdot12+5=113$."}},
    {"q": {"va": "Quina afirmació és <b>certa</b>?", "es": "¿Qué afirmación es <b>cierta</b>?", "en": "Which statement is <b>true</b>?"}, "o": [{"va": "15 és divisor de 5", "es": "15 es divisor de 5", "en": "15 is a divisor of 5"}, {"va": "0 és múltiple de 7", "es": "0 es múltiplo de 7", "en": "0 is a multiple of 7"}, {"va": "1 és un nombre primer", "es": "1 es un número primo", "en": "1 is a prime number"}, {"va": "Un nombre té infinits divisors", "es": "Un número tiene infinitos divisores", "en": "A number has infinitely many divisors"}], "a": 1, "e": {"va": "$0=7\\cdot0$. En canvi, 5 és divisor de 15 (i no al revés), l'1 no és primer i els divisors d'un nombre són finits.", "es": "$0=7\\cdot0$. En cambio, 5 es divisor de 15 (y no al revés), el 1 no es primo y los divisores de un número son finitos.", "en": "$0=7\\cdot0$. On the other hand, 5 is a divisor of 15 (not the other way round), 1 is not prime and a number has finitely many divisors."}},
    {"q": {"va": "Quin d'aquests nombres és divisible per 3 <b>i</b> per 11?", "es": "¿Cuál de estos números es divisible por 3 <b>y</b> por 11?", "en": "Which of these numbers is divisible by 3 <b>and</b> by 11?"}, "o": [{"va": "$1452$"}, {"va": "$2002$"}, {"va": "$1234$"}, {"va": "$1210$"}], "a": 0, "e": {"va": "$1+4+5+2=12$ és múltiple de 3 i $(1+5)-(4+2)=0$. El 2002 i el 1210 són múltiples d'11, però no de 3.", "es": "$1+4+5+2=12$ es múltiplo de 3 y $(1+5)-(4+2)=0$. El 2002 y el 1210 son múltiplos de 11, pero no de 3.", "en": "$1+4+5+2=12$ is a multiple of 3 and $(1+5)-(4+2)=0$. 2002 and 1210 are multiples of 11, but not of 3."}},
    {"q": {"va": "La descomposició en factors primers de 360 és…", "es": "La descomposición en factores primos de 360 es…", "en": "The prime factorisation of 360 is…"}, "o": [{"va": "$2^3\\cdot3^2\\cdot5$"}, {"va": "$2^2\\cdot3^2\\cdot10$"}, {"va": "$2^3\\cdot45$"}, {"va": "$2\\cdot3\\cdot5\\cdot12$"}], "a": 0, "e": {"va": "Tots els factors han de ser primers: $360=2\\cdot2\\cdot2\\cdot3\\cdot3\\cdot5$.", "es": "Todos los factores tienen que ser primos: $360=2\\cdot2\\cdot2\\cdot3\\cdot3\\cdot5$.", "en": "All the factors must be prime: $360=2\\cdot2\\cdot2\\cdot3\\cdot3\\cdot5$."}},
    {"q": {"va": "Quant val $\\text{MCD}(48,36)$?", "es": "¿Cuánto vale $\\text{MCD}(48,36)$?", "en": "What is $\\gcd(48,36)$?"}, "o": [{"va": "$4$"}, {"va": "$6$"}, {"va": "$12$"}, {"va": "$144$"}], "a": 2, "e": {"va": "$48=2^4\\cdot3$, $36=2^2\\cdot3^2$. Factors comuns amb el menor exponent: $2^2\\cdot3=12$.", "es": "$48=2^4\\cdot3$, $36=2^2\\cdot3^2$. Factores comunes con el menor exponente: $2^2\\cdot3=12$.", "en": "$48=2^4\\cdot3$, $36=2^2\\cdot3^2$. Common factors with the lowest exponent: $2^2\\cdot3=12$."}},
    {"q": {"va": "Quant val $\\text{mcm}(12,18)$?", "es": "¿Cuánto vale $\\text{mcm}(12,18)$?", "en": "What is $\\text{lcm}(12,18)$?"}, "o": [{"va": "$6$"}, {"va": "$36$"}, {"va": "$72$"}, {"va": "$216$"}], "a": 1, "e": {"va": "$12=2^2\\cdot3$, $18=2\\cdot3^2$. Comuns i no comuns amb el major exponent: $2^2\\cdot3^2=36$.", "es": "$12=2^2\\cdot3$, $18=2\\cdot3^2$. Comunes y no comunes con el mayor exponente: $2^2\\cdot3^2=36$.", "en": "$12=2^2\\cdot3$, $18=2\\cdot3^2$. Common and non-common factors with the highest exponent: $2^2\\cdot3^2=36$."}},
    {"q": {"va": "Dos semàfors canvien de color cada 40 s i cada 60 s. Si ara canvien alhora, quan tornaran a coincidir?", "es": "Dos semáforos cambian de color cada 40 s y cada 60 s. Si ahora cambian a la vez, ¿cuándo volverán a coincidir?", "en": "Two traffic lights change every 40 s and every 60 s. If they change together now, when will they next coincide?"}, "o": [{"va": "Al cap de 20 s", "es": "A los 20 s", "en": "After 20 s"}, {"va": "Al cap de 120 s", "es": "A los 120 s", "en": "After 120 s"}, {"va": "Al cap de 100 s", "es": "A los 100 s", "en": "After 100 s"}, {"va": "Al cap de 2400 s", "es": "A los 2400 s", "en": "After 2400 s"}], "a": 1, "e": {"va": "«Tornar a coincidir» és un problema de mcm: $\\text{mcm}(40,60)=120$ s, és a dir, 2 minuts.", "es": "«Volver a coincidir» es un problema de mcm: $\\text{mcm}(40,60)=120$ s, es decir, 2 minutos.", "en": "“Coinciding again” is an LCM problem: $\\text{lcm}(40,60)=120$ s, that is, 2 minutes."}},
    {"q": {"va": "Quina desigualtat és <b>certa</b>?", "es": "¿Qué desigualdad es <b>cierta</b>?", "en": "Which inequality is <b>true</b>?"}, "o": [{"va": "$-3<-8$"}, {"va": "$-3>-8$"}, {"va": "$-10>2$"}, {"va": "$0<-1$"}], "a": 1, "e": {"va": "En la recta, $-3$ està més a la dreta que $-8$. Entre negatius, és més gran el de menor valor absolut.", "es": "En la recta, $-3$ está más a la derecha que $-8$. Entre negativos, es mayor el de menor valor absoluto.", "en": "On the number line, $-3$ is to the right of $-8$. Among negatives, the one with the smaller absolute value is larger."}},
    {"q": {"va": "$(-7)-(-3)=$", "es": "$(-7)-(-3)=$", "en": "$(-7)-(-3)=$"}, "o": [{"va": "$-10$"}, {"va": "$-4$"}, {"va": "$4$"}, {"va": "$10$"}], "a": 1, "e": {"va": "Restar és sumar l'oposat: $-7+3=-4$.", "es": "Restar es sumar el opuesto: $-7+3=-4$.", "en": "Subtracting is adding the opposite: $-7+3=-4$."}},
    {"q": {"va": "$(-4)\\cdot(+3):(-6)=$", "es": "$(-4)\\cdot(+3):(-6)=$", "en": "$(-4)\\cdot(+3):(-6)=$"}, "o": [{"va": "$-2$"}, {"va": "$2$"}, {"va": "$-8$"}, {"va": "$8$"}], "a": 1, "e": {"va": "D'esquerra a dreta: $(-12):(-6)=+2$ (signes iguals → positiu).", "es": "De izquierda a derecha: $(-12):(-6)=+2$ (signos iguales → positivo).", "en": "From left to right: $(-12):(-6)=+2$ (same signs → positive)."}},
    {"q": {"va": "$5-3\\cdot(-2)=$", "es": "$5-3\\cdot(-2)=$", "en": "$5-3\\cdot(-2)=$"}, "o": [{"va": "$4$"}, {"va": "$-4$"}, {"va": "$11$"}, {"va": "$-1$"}], "a": 2, "e": {"va": "Primer la multiplicació: $5-(-6)=5+6=11$.", "es": "Primero la multiplicación: $5-(-6)=5+6=11$.", "en": "Multiplication first: $5-(-6)=5+6=11$."}},
    {"q": {"va": "$-2^4=$", "es": "$-2^4=$", "en": "$-2^4=$"}, "o": [{"va": "$16$"}, {"va": "$-16$"}, {"va": "$-8$"}, {"va": "$8$"}], "a": 1, "e": {"va": "Sense parèntesi, la base és 2: $-2^4=-(2^4)=-16$. En canvi, $(-2)^4=16$.", "es": "Sin paréntesis, la base es 2: $-2^4=-(2^4)=-16$. En cambio, $(-2)^4=16$.", "en": "Without brackets the base is 2: $-2^4=-(2^4)=-16$. However, $(-2)^4=16$."}},
    {"q": {"va": "$(-2)^3\\cdot(-2)^2=$", "es": "$(-2)^3\\cdot(-2)^2=$", "en": "$(-2)^3\\cdot(-2)^2=$"}, "o": [{"va": "$(-2)^6$"}, {"va": "$32$"}, {"va": "$-32$"}, {"va": "$4^5$"}], "a": 2, "e": {"va": "Mateixa base: sumem exponents, $(-2)^5=-32$ (exponent senar → negatiu).", "es": "Misma base: sumamos exponentes, $(-2)^5=-32$ (exponente impar → negativo).", "en": "Same base: add the exponents, $(-2)^5=-32$ (odd exponent → negative)."}},
    {"q": {"va": "$\\sqrt{-9}=$", "es": "$\\sqrt{-9}=$", "en": "$\\sqrt{-9}=$"}, "o": [{"va": "$-3$"}, {"va": "$3$"}, {"va": "$\\pm3$"}, {"va": "No existeix", "es": "No existe", "en": "It doesn't exist"}], "a": 3, "e": {"va": "$3^2=9$ i $(-3)^2=9$: cap enter elevat al quadrat dona $-9$.", "es": "$3^2=9$ y $(-3)^2=9$: ningún entero elevado al cuadrado da $-9$.", "en": "$3^2=9$ and $(-3)^2=9$: no integer squared gives $-9$."}},
    {"q": {"va": "$\\left[(-3)^2-\\sqrt{16}\\right]\\cdot(-2)=$", "es": "$\\left[(-3)^2-\\sqrt{16}\\right]\\cdot(-2)=$", "en": "$\\left[(-3)^2-\\sqrt{16}\\right]\\cdot(-2)=$"}, "o": [{"va": "$-10$"}, {"va": "$10$"}, {"va": "$-26$"}, {"va": "$2$"}], "a": 0, "e": {"va": "Dins del claudàtor: $9-4=5$. Després, $5\\cdot(-2)=-10$.", "es": "Dentro del corchete: $9-4=5$. Después, $5\\cdot(-2)=-10$.", "en": "Inside the brackets: $9-4=5$. Then $5\\cdot(-2)=-10$."}}
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

  var TITLES = { va: "Nombres naturals i enters · FentMates", es: "Números naturales y enteros · FentMates", en: "Natural numbers and integers · FentMates" };
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
    wCtx(); wLine(); wAbs(); wAdd(); wPar(); wSign(); wElev(); wPowZ(); wRootZ();
    document.querySelectorAll(".w-hier").forEach(wHier);
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
