/* 4t ESO A · Unitat 1. Part 1 (fraccions, potències, qüestionari, índex i idioma): app.js de 2eso-t2 adaptat. */
(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4esoa-u1-done", NSEC = 10;

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
  /* textos dels ginys de fraccions (de la unitat 4 de 1r ESO) */
  var UI4 = {
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
      kfBad: "Escriu entre 2 i 6 fraccions positives separades per comes (fins a 10 unitats).", kOrd: "De menor a major:", kCd: "Amb denominador comú {m}, només cal comparar els numeradors:",
      opBad: "Escriu nombres naturals (denominadors diferents de 0).", opMcm: "Denominadors diferents: reduïm a comú denominador amb el mcm({b}, {d}) = {m}.", opSame: "Mateix denominador: sumem o restem els numeradors.",
      opSimp: "Simplifiquem dividint entre {g}.", opMul: "Multipliquem numeradors entre si i denominadors entre si.", opDiv: "Dividir és multiplicar per la inversa (o fer productes creuats).",
      opDiv0: "No es pot dividir entre 0.", opArea: "El rectangle mesura 1 × 1: les columnes pintades són {f1} i les files, {f2}. La zona doble és {r} del total.", opBars: "Totes les barres dividides en {m} parts iguals:",
      hParse: "No entenc l'expressió. Escriu fraccions com 3/4, nombres, + − · : i parèntesis ( ) [ ].", hDiv0: "No es pot dividir entre 0.", hBig: "Els nombres es fan massa grans.",
      kinds: { mul: "Multiplicació", div: "Divisió", add: "Suma", sub: "Resta" }, inPar: "dins del parèntesi", result: "Resultat:", already: "Ja és una fracció irreductible: no hi ha res a calcular.",
      rsBad: "Escriu un total entre 1 i 1 000 000 i dues fraccions pròpies (denominadors fins a 12).", rFirst: "Primer gastem {f} del total:", rLeft: "Queda:", rSecond: "Després, {f} <b>del que queda</b>:", rEnd: "Al final queda:",
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
      kfBad: "Escribe entre 2 y 6 fracciones positivas separadas por comas (hasta 10 unidades).", kOrd: "De menor a mayor:", kCd: "Con denominador común {m}, solo hay que comparar los numeradores:",
      opBad: "Escribe números naturales (denominadores distintos de 0).", opMcm: "Denominadores distintos: reducimos a común denominador con el mcm({b}, {d}) = {m}.", opSame: "Mismo denominador: sumamos o restamos los numeradores.",
      opSimp: "Simplificamos dividiendo entre {g}.", opMul: "Multiplicamos numeradores entre sí y denominadores entre sí.", opDiv: "Dividir es multiplicar por la inversa (o hacer productos cruzados).",
      opDiv0: "No se puede dividir entre 0.", opArea: "El rectángulo mide 1 × 1: las columnas pintadas son {f1} y las filas, {f2}. La zona doble es {r} del total.", opBars: "Todas las barras divididas en {m} partes iguales:",
      hParse: "No entiendo la expresión. Escribe fracciones como 3/4, números, + − · : y paréntesis ( ) [ ].", hDiv0: "No se puede dividir entre 0.", hBig: "Los números se hacen demasiado grandes.",
      kinds: { mul: "Multiplicación", div: "División", add: "Suma", sub: "Resta" }, inPar: "dentro del paréntesis", result: "Resultado:", already: "Ya es una fracción irreducible: no hay nada que calcular.",
      rsBad: "Escribe un total entre 1 y 1 000 000 y dos fracciones propias (denominadores hasta 12).", rFirst: "Primero gastamos {f} del total:", rLeft: "Queda:", rSecond: "Después, {f} <b>de lo que queda</b>:", rEnd: "Al final queda:",
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
      kfBad: "Type 2 to 6 positive fractions separated by commas (up to 10 wholes).", kOrd: "From smallest to largest:", kCd: "With the common denominator {m}, we only need to compare numerators:",
      opBad: "Type whole numbers (denominators can't be 0).", opMcm: "Different denominators: use a common denominator, lcm({b}, {d}) = {m}.", opSame: "Same denominator: add or subtract the numerators.",
      opSimp: "Simplify by dividing by {g}.", opMul: "Multiply numerators together and denominators together.", opDiv: "Dividing means multiplying by the reciprocal (or cross-multiplying).",
      opDiv0: "You can't divide by 0.", opArea: "The square is 1 × 1: the shaded columns are {f1} and the rows {f2}. The double-shaded area is {r} of the whole.", opBars: "All bars split into {m} equal parts:",
      hParse: "I can't read that expression. Type fractions like 3/4, numbers, + − · : and brackets ( ) [ ].", hDiv0: "You can't divide by 0.", hBig: "The numbers get too big.",
      kinds: { mul: "Multiplication", div: "Division", add: "Addition", sub: "Subtraction" }, inPar: "inside the brackets", result: "Result:", already: "It's already a simplified fraction: nothing to work out.",
      rsBad: "Type a total from 1 to 1,000,000 and two proper fractions (denominators up to 12).", rFirst: "First we spend {f} of the total:", rLeft: "Left:", rSecond: "Then {f} <b>of what is left</b>:", rEnd: "Left at the end:",
      rFrac: "As fractions of the total: {f1} + {f2} + {f3} = 1.", rL1: "1st part", rL2: "2nd part", rL3: "left",
      dOf: "Work out $\\tfrac{{a}}{{b}}$ of {n}", dOfT: "If $\\tfrac{{a}}{{b}}$ of a number is {p}, what is the number?", dPct: "Work out {p}% of {n}", dPctF: "Write {p}% as a fraction in its simplest form.",
      dSimp: "Write $\\tfrac{{a}}{{b}}$ in its simplest form", dX: "Find x:", dCmp: "Type <, > or =:", dCalc: "Work out and simplify:",
      un: ["whole", "wholes"] }
  };
  /* textos propis de la unitat 2 de 2n ESO (tenen prioritat sobre els anteriors) */
  var UI2 = {
    va: { kinds: { mul: "Multiplicació", div: "Divisió", add: "Suma", sub: "Resta", pow: "Potència" },
      hParse: "No entenc l'expressió. Escriu fraccions com 3/4, nombres, + − · : ^ i parèntesis ( ) [ ]. Una fracció elevada va entre parèntesis: (2/3)^2.",
      hPow00: "0 elevat a 0 no té sentit.",
      gBad: "Escriu la part entera (fins a 4 xifres), l'anteperíode (pot quedar buit; fins a 3 xifres) i el període (d'1 a 3 xifres).",
      gPure: "<b>Periòdic pur.</b> Numerador: el nombre sense la coma fins al final del primer període ({a}) menys la part entera ({b}). Denominador: tants 9 com xifres té el període.",
      gMixed: "<b>Periòdic mixt.</b> Numerador: el nombre sense la coma fins al final del primer període ({a}) menys la part que no es repeteix ({b}). Denominador: tants 9 com xifres té el període i tants 0 com xifres té l'anteperíode.",
      gWhy: "D'on ix la regla? Multipliquem $x$ per potències de 10 per a tindre dos nombres amb els mateixos decimals i els restem:",
      gCheck: "Comprovació:", g9: "Curiós: amb període 9 el decimal és, en realitat, un nombre exacte.",
      pwBad: "Escriu una fracció (numerador entre −20 i 20, denominador entre 1 i 20) i exponents naturals fins a 8.",
      pwQ: "Per al quocient, el primer exponent ha de ser major o igual que el segon.",
      pwDef: "Elevar és multiplicar la fracció per ella mateixa: elevem el numerador i el denominador.",
      pw0: "Qualsevol fracció diferent de 0 elevada a 0 val 1.", pw1: "Elevada a 1, la fracció es queda igual.",
      pwEven: "Base negativa i exponent <b>parell</b>: el resultat és <b>positiu</b>.", pwOdd: "Base negativa i exponent <b>senar</b>: el resultat és <b>negatiu</b>.",
      pwM: "Producte de potències amb la mateixa base: es deixa la base i es <b>sumen</b> els exponents.",
      pwQq: "Quocient de potències amb la mateixa base: es deixa la base i es <b>resten</b> els exponents.",
      pwPP: "Potència d'una potència: es deixa la base i es <b>multipliquen</b> els exponents.", pwBig: "El resultat és massa gran per a mostrar-lo.",
      dGen: "Escriu {x} com a fracció irreductible.", dPow: "Calcula:",
      dPr1: "Un dipòsit de {t} litres està ple fins a $\\tfrac{{a}}{{b}}$. Quants litres té?",
      dPr2: "Els $\\tfrac{{a}}{{b}}$ dels alumnes d'un institut són {p}. Quants alumnes hi ha en total?",
      dPr3: "Tenim {t} €. Gastem $\\tfrac{{a}}{{b}}$ i després $\\tfrac{{c}}{{d}}$ del que queda. Quants euros ens queden?",
      dPr4: "En una classe, $\\tfrac{{a}}{{b}}$ dels alumnes van a peu i $\\tfrac{{c}}{{d}}$ en autobús. Quina fracció dels alumnes va d'una altra manera?" },
    es: { kinds: { mul: "Multiplicación", div: "División", add: "Suma", sub: "Resta", pow: "Potencia" },
      hParse: "No entiendo la expresión. Escribe fracciones como 3/4, números, + − · : ^ y paréntesis ( ) [ ]. Una fracción elevada va entre paréntesis: (2/3)^2.",
      hPow00: "0 elevado a 0 no tiene sentido.",
      gBad: "Escribe la parte entera (hasta 4 cifras), el anteperiodo (puede quedar vacío; hasta 3 cifras) y el periodo (de 1 a 3 cifras).",
      gPure: "<b>Periódico puro.</b> Numerador: el número sin la coma hasta el final del primer periodo ({a}) menos la parte entera ({b}). Denominador: tantos 9 como cifras tiene el periodo.",
      gMixed: "<b>Periódico mixto.</b> Numerador: el número sin la coma hasta el final del primer periodo ({a}) menos la parte que no se repite ({b}). Denominador: tantos 9 como cifras tiene el periodo y tantos 0 como cifras tiene el anteperiodo.",
      gWhy: "¿De dónde sale la regla? Multiplicamos $x$ por potencias de 10 para tener dos números con los mismos decimales y los restamos:",
      gCheck: "Comprobación:", g9: "Curioso: con periodo 9 el decimal es, en realidad, un número exacto.",
      pwBad: "Escribe una fracción (numerador entre −20 y 20, denominador entre 1 y 20) y exponentes naturales hasta 8.",
      pwQ: "Para el cociente, el primer exponente tiene que ser mayor o igual que el segundo.",
      pwDef: "Elevar es multiplicar la fracción por sí misma: elevamos el numerador y el denominador.",
      pw0: "Cualquier fracción distinta de 0 elevada a 0 vale 1.", pw1: "Elevada a 1, la fracción se queda igual.",
      pwEven: "Base negativa y exponente <b>par</b>: el resultado es <b>positivo</b>.", pwOdd: "Base negativa y exponente <b>impar</b>: el resultado es <b>negativo</b>.",
      pwM: "Producto de potencias con la misma base: se deja la base y se <b>suman</b> los exponentes.",
      pwQq: "Cociente de potencias con la misma base: se deja la base y se <b>restan</b> los exponentes.",
      pwPP: "Potencia de una potencia: se deja la base y se <b>multiplican</b> los exponentes.", pwBig: "El resultado es demasiado grande para mostrarlo.",
      dGen: "Escribe {x} como fracción irreducible.", dPow: "Calcula:",
      dPr1: "Un depósito de {t} litros está lleno hasta $\\tfrac{{a}}{{b}}$. ¿Cuántos litros tiene?",
      dPr2: "Los $\\tfrac{{a}}{{b}}$ de los alumnos de un instituto son {p}. ¿Cuántos alumnos hay en total?",
      dPr3: "Tenemos {t} €. Gastamos $\\tfrac{{a}}{{b}}$ y después $\\tfrac{{c}}{{d}}$ de lo que queda. ¿Cuántos euros nos quedan?",
      dPr4: "En una clase, $\\tfrac{{a}}{{b}}$ de los alumnos van a pie y $\\tfrac{{c}}{{d}}$ en autobús. ¿Qué fracción de los alumnos va de otra manera?" },
    en: { kinds: { mul: "Multiplication", div: "Division", add: "Addition", sub: "Subtraction", pow: "Power" },
      hParse: "I can't read that. Type fractions like 3/4, numbers, + − · : ^ and brackets ( ) [ ]. Put a fraction in brackets before a power: (2/3)^2.",
      hPow00: "0 to the power 0 has no meaning.",
      gBad: "Type the whole-number part (up to 4 digits), the non-repeating part (may be empty; up to 3 digits) and the period (1 to 3 digits).",
      gPure: "<b>Purely recurring.</b> Numerator: the number without the comma up to the end of the first period ({a}) minus the whole-number part ({b}). Denominator: one 9 for each digit of the period.",
      gMixed: "<b>Mixed recurring.</b> Numerator: the number without the comma up to the end of the first period ({a}) minus the part that doesn't repeat ({b}). Denominator: one 9 for each digit of the period followed by one 0 for each non-repeating decimal digit.",
      gWhy: "Where does the rule come from? Multiply $x$ by powers of 10 to get two numbers with the same decimals, then subtract:",
      gCheck: "Check:", g9: "Fun fact: with period 9 the decimal is really a terminating number.",
      pwBad: "Type a fraction (numerator from −20 to 20, denominator from 1 to 20) and whole-number exponents up to 8.",
      pwQ: "For the quotient, the first exponent must be greater than or equal to the second.",
      pwDef: "A power multiplies the fraction by itself: raise the numerator and the denominator.",
      pw0: "Any non-zero fraction to the power 0 is 1.", pw1: "To the power 1, the fraction stays the same.",
      pwEven: "Negative base and <b>even</b> exponent: the result is <b>positive</b>.", pwOdd: "Negative base and <b>odd</b> exponent: the result is <b>negative</b>.",
      pwM: "Product of powers with the same base: keep the base and <b>add</b> the exponents.",
      pwQq: "Quotient of powers with the same base: keep the base and <b>subtract</b> the exponents.",
      pwPP: "Power of a power: keep the base and <b>multiply</b> the exponents.", pwBig: "The result is too big to show.",
      dGen: "Write {x} as a fraction in simplest form.", dPow: "Work out:",
      dPr1: "A {t}-litre tank is $\\tfrac{{a}}{{b}}$ full. How many litres are in it?",
      dPr2: "$\\tfrac{{a}}{{b}}$ of the students at a school are {p}. How many students are there in total?",
      dPr3: "We have {t} €. We spend $\\tfrac{{a}}{{b}}$ and then $\\tfrac{{c}}{{d}}$ of what's left. How many euros are left?",
      dPr4: "In a class, $\\tfrac{{a}}{{b}}$ of the students walk and $\\tfrac{{c}}{{d}}$ take the bus. What fraction of the students get there another way?" }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { var o = (UI2[lang] || UI2.va); if (k in o) return o[k]; o = UI[lang] || UI.va; if (k in o) return o[k]; o = UI4[lang] || UI4.va; return o[k]; }
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
  function plist(s) {
    var parts = String(s).split(/[;,]|\s+(?=[\d-])/).map(function (x) { return x.trim(); }).filter(Boolean), out = [];
    for (var i = 0; i < parts.length; i++) { var f = pfrac(parts[i]); if (!f) return null; out.push(f); }
    return out;
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
  function quick2(w, cb) { w.querySelectorAll(".quick button[data-b]").forEach(function (b) { b.addEventListener("click", function () { cb(b.dataset.b.split(/[\/,;]/)); }); }); }

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

  /* ---------- giny: comparar i ordenar ---------- */
  var COLS = ["var(--r1)", "var(--r2)", "var(--r3)", "var(--r4)", "var(--plus)", "var(--minus)"];
  function wCmp() {
    var w = document.getElementById("w-cmp"); if (!w) return;
    var inp = w.querySelector(".tin"), out = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var fs = plist(inp.value);
      out.innerHTML = "";
      if (!fs || fs.length < 2 || fs.length > 6 || fs.some(function (f) { return f.n < 0 || f.d > 1000 || f.n / f.d > 10; })) { info.innerHTML = warn("kfBad"); return; }
      var m = fs.map(function (f) { return f.d; }).reduce(lcm);
      if (m > 1e6) { info.innerHTML = warn("kfBad"); return; }
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
      if ("+-·:()[]^".indexOf(c) >= 0) { t.push({ k: c }); i++; continue; }
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
    function base() {
      var p = peek();
      if (p === "n") { var tk = t[i++]; if (!tk.v.d) throw 0; return { t: "n", v: tk.v, raw: tk.raw }; }
      if (p === "(" || p === "[") { i++; var e = expr(), cl = p === "(" ? ")" : "]"; if (peek() !== cl) throw 0; i++; return e.t === "n" && e.v.n >= 0 ? { t: "n", v: e.v, raw: e.raw, par: true } : { t: "p", k: p, e: e }; }
      throw 0;
    }
    /* potència: la base és un nombre, una fracció entre parèntesis o un parèntesi; l'exponent, un natural fins a 12 */
    function prim() {
      var b = base();
      if (peek() !== "^") return b;
      if (b.t === "n" && b.raw && !b.par) throw 0;
      i++; var tk = t[i++];
      if (!tk || tk.k !== "n" || tk.raw || tk.v.n > 12) throw 0;
      if (peek() === "^") throw 0;
      return { t: "w", b: b, e: tk.v.n };
    }
    try { var r = expr(); return i === t.length ? r : null; } catch (e) { return null; }
  }
  function isN(x) { return x.t === "n" || (x.t === "p" && x.e.t === "n"); }
  function nv(x) { return x.t === "n" ? x.v : x.e.v; }
  function first(x, pr) {
    if (x.t === "w") return first(x.b, pr) || (pr(x) ? x : null);
    if (x.t === "b") return first(x.l, pr) || (pr(x) ? x : null) || first(x.r, pr);
    return pr(x) ? x : null;
  }
  function grp(x) { return x.t === "p" && x.e.t !== "n"; }
  /* ordre: parèntesis (de dins cap a fora) → · i : → + i − (sempre d'esquerra a dreta) */
  function target(x, inG) {
    var g = first(x, grp);
    if (g) return target(g.e, true);
    var y = first(x, function (z) { return z.t === "w" && isN(z.b); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "·" || z.op === ":") && isN(z.l) && isN(z.r); }) ||
      first(x, function (z) { return z.t === "b" && (z.op === "+" || z.op === "-") && isN(z.l) && isN(z.r); });
    return y ? { n: y, g: !!inG } : null;
  }
  function rpow(a, e) { var n = 1, d = 1; for (var j = 0; j < e; j++) { n *= a.n; d *= a.d; } return rat(n, d); }
  function applyOp(y) {
    if (y.t === "w") { var bb = nv(y.b); return !bb.n && !y.e ? { err: u("hPow00") } : { v: rpow(bb, y.e), k: "pow" }; }
    var a = nv(y.l), b = nv(y.r);
    if (y.op === "+") return { v: radd(a, b), k: "add" };
    if (y.op === "-") return { v: rsub(a, b), k: "sub" };
    if (y.op === "·") return { v: rmul(a, b), k: "mul" };
    return !b.n ? { err: u("hDiv0") } : { v: rdiv(a, b), k: "div" };
  }
  function repl(x, tg, nw) {
    if (x === tg) return nw;
    if (x.t === "w") return { t: "w", b: repl(x.b, tg, nw), e: x.e };
    if (x.t === "b") return { t: "b", op: x.op, l: repl(x.l, tg, nw), r: repl(x.r, tg, nw) };
    if (x.t === "p") { var e = repl(x.e, tg, nw); return e.t === "n" && e.v.n >= 0 ? e : { t: "p", k: x.k, e: e }; }
    return x;
  }
  function tx(x, tg, val, top) {
    var s;
    if (x.t === "n") { s = fx(x.v.n, x.v.d); if (x.v.n < 0 && !top) s = "\\Bigl(" + s + "\\Bigr)"; }
    else if (x.t === "p") s = x.k === "(" ? "\\Bigl(" + tx(x.e, tg, val, true) + "\\Bigr)" : "\\Bigl[" + tx(x.e, tg, val, true) + "\\Bigr]";
    else if (x.t === "w") {
      s = x.b.t === "n" ? fx(x.b.v.n, x.b.v.d) : tx(x.b, tg, val, true);
      if (x.b.t === "n" && (x.b.v.d !== 1 || x.b.v.n < 0)) s = "\\left(" + s + "\\right)";
      s = "{" + s + "}^{" + x.e + "}";
    }
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
      if ([t, a, b, c, d].some(isNaN) || t < 1 || t > 1000000 || !b || !d || b > 12 || d > 12 || a >= b || c >= d || !a || !c) { info.innerHTML = warn("rsBad"); return; }
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

  /* ---------- 2.6 fracció generatriu ---------- */
  /* ent, ante, per: textos de xifres. Retorna x en TeX, la regla i la fracció irreductible */
  function gener(ent, ante, per) {
    ent = String(+ent);
    var full = parseInt(ent + ante + per, 10), part = parseInt(ent + ante, 10), den = parseInt("9".repeat(per.length) + "0".repeat(ante.length), 10);
    var x = ft(+ent) + "{,}" + ante + "\\overline{" + per + "}";
    return { x: x, full: full, part: part, num: full - part, den: den, f: rat(full - part, den),
      rule: frac(ft(full) + "-" + ft(part), ft(den)) + "=" + frac(ft(full - part), ft(den)) };
  }
  function wGen() {
    var w = document.getElementById("w-gen"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info");
    function render() {
      var e = I.e.value.trim(), a = I.a.value.trim(), p = I.p.value.trim();
      if (!/^\d{1,4}$/.test(e) || !/^\d{0,3}$/.test(a) || !/^\d{1,3}$/.test(p)) { vis.innerHTML = ""; info.innerHTML = warn("gBad"); return; }
      var z = gener(e, a, p), E = String(+e), k = a.length, m = p.length, f = z.f;
      vis.innerHTML = '<div class="gdig"><span class="ge">' + E + '</span><span class="gc">,</span>' + (a ? '<span class="ga">' + a + "</span>" : "") + '<span class="gp">' + p + '</span><span class="gp2">' + p + p.slice(0, 2) + "…</span></div>";
      var h = "<p>" + fill(u(a ? "gMixed" : "gPure"), { a: tex(ft(z.full)), b: tex(ft(z.part)) }) + "</p>";
      h += tex("x=" + z.x + "=" + z.rule + "=\\boxed{" + fr(f) + "}", true);
      var big = p10(k + m), small = p10(k);
      var l1 = (k ? ft(small) + "x=" + ft(z.part) + "{,}" : "x=" + E + "{,}") + "\\overline{" + p + "}";
      var l2 = ft(big) + "x=" + ft(z.full) + "{,}\\overline{" + p + "}";
      h += "<p>" + rtex(u("gWhy")) + "</p>" + tex("\\begin{aligned}" + l2 + "\\\\ -\\ " + l1 + "\\\\ \\hline " + ft(big - small) + "x=" + ft(z.num) + "\\end{aligned}\\qquad x=" + frac(ft(z.num), ft(big - small)) + "=" + fr(f), true);
      var L = ldiv(Math.abs(f.n), f.d, 40);
      h += hint(u("gCheck") + " " + tex(fr(f) + "=" + ft(f.n) + ":" + ft(f.d) + "=" + perTex(L)) + (/^9+$/.test(p) ? " " + u("g9") : ""));
      info.innerHTML = h;
    }
    ["e", "a", "p"].forEach(function (k) { I[k].addEventListener("input", render); });
    quickB(w, function (q) { I.e.value = q[0]; I.a.value = q[1]; I.p.value = q[2]; render(); });
    onLang(render);
  }

  /* ---------- 2.9 potències de fraccions ---------- */
  function pwT(r, n) { var s = fx(r.n, r.d); if (r.d !== 1 || r.n < 0) s = "\\left(" + s + "\\right)"; return "{" + s + "}^{" + n + "}"; }
  function wPow() {
    var w = document.getElementById("w-pow"); if (!w) return;
    var I = inVals(w), vis = w.querySelector(".fvis"), info = w.querySelector(".info"), S = gsegs(w, render);
    function render() {
      var mo = S.st.m;
      w.querySelectorAll("[data-p]").forEach(function (e) { e.hidden = e.dataset.p.split(" ").indexOf(mo) < 0; });
      var a = parseInt(String(I.a.value).replace(/[−–]/g, "-"), 10), b = pnat(I.b.value), m = pnat(I.m.value), n = pnat(I.n.value);
      if (mo === "p") n = m;
      vis.innerHTML = "";
      if (!/^\s*[-−–]?\d{1,2}\s*$/.test(I.a.value) || isNaN(a) || Math.abs(a) > 20 || !(b >= 1) || b > 20 || !(m >= 0) || m > 8 || !(n >= 0) || n > 8) { info.innerHTML = warn("pwBad"); return; }
      var B = rat(a, b), h = "", ex;
      if (!B.n && !m) { info.innerHTML = warn("hPow00"); return; }
      if (mo === "q" && m < n) { info.innerHTML = warn("pwQ"); return; }
      ex = mo === "p" ? m : mo === "m" ? m + n : mo === "q" ? m - n : m * n;
      if (Math.pow(Math.max(Math.abs(B.n), B.d), ex) > 1e12) { info.innerHTML = warn("pwBig"); return; }
      var V = rpow(B, ex), F = fx(B.n, B.d);
      if (mo === "p") {
        h = "<p>" + u(m === 0 ? "pw0" : m === 1 ? "pw1" : "pwDef") + "</p>";
        var prod = m >= 2 && m <= 6 ? "=" + Array(m + 1).join("|").split("").map(function () { return B.d === 1 && B.n >= 0 ? F : "\\left(" + F + "\\right)"; }).join("\\cdot ") : "";
        var raw = m >= 1 ? "=" + (B.n < 0 ? (m % 2 ? "-" : "+") : "") + frac(ft(Math.abs(B.n)) + "^{" + m + "}", ft(B.d) + "^{" + m + "}") : "";
        h += tex(pwT(B, m) + prod + raw + "=\\boxed{" + fr(V) + "}", true);
        if (B.n < 0 && m > 0) h += hint(u(m % 2 ? "pwOdd" : "pwEven"));
        if (B.d > 1 && B.n > 0 && B.n < B.d && m >= 2) vis.innerHTML = '<div class="brow"><span class="bl">' + tex(fr(B)) + "</span>" + barSVG(B.n, B.d, 600, 22, "fr-on") + "</div>";
      } else {
        var lhs = mo === "m" ? pwT(B, m) + "\\cdot " + pwT(B, n) : mo === "q" ? pwT(B, m) + ":" + pwT(B, n) : "\\left[" + pwT(B, m) + "\\right]^{" + n + "}";
        var mid = mo === "m" ? m + "+" + n : mo === "q" ? m + "-" + n : m + "\\cdot " + n;
        h = "<p>" + u(mo === "m" ? "pwM" : mo === "q" ? "pwQq" : "pwPP") + "</p>" + tex(lhs + "=" + (B.d === 1 && B.n >= 0 ? F : "\\left(" + F + "\\right)") + "^{" + mid + "}=" + pwT(B, ex) + "=\\boxed{" + fr(V) + "}", true);
        if (ex === 0) h += hint(u("pw0"));
      }
      info.innerHTML = h;
    }
    ["a", "b", "m", "n"].forEach(function (k) { I[k].addEventListener("input", render); });
    quickB(w, function (q) { S.set("m", q[0]); I.a.value = q[1]; I.b.value = q[2]; I.m.value = q[3]; I.n.value = q[4] || I.n.value; render(); });
    onLang(render);
  }

  /* ---------- entrenadors ---------- */
  function rdD(maxI, k) { return D(rint(0, maxI) * p10(k) + rint(1, p10(k) - 1), k, true); }
  function coprimeNum(b) { var a; do { a = rint(1, b - 1); } while (gcd(a, b) !== 1); return a; }
  function randFr(maxD) { var b = rint(2, maxD); return { n: coprimeNum(b), d: b }; }
  var GEN = {
    cmpd: function () {
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
    mul: function () {
      var f = { n: rint(1, 12), d: rint(2, 12) }, g = { n: rint(1, 12), d: rint(2, 12) }, op = Math.random() < .5 ? "·" : ":", r = op === "·" ? rmul(f, g) : rdiv(f, g);
      return { t: "frac", irr: true, ans: r, q: function () { return u("dCalc") + " $" + frac(f.n, f.d) + (op === "·" ? "\\cdot " : ":") + frac(g.n, g.d) + "$"; },
        s: function () { return opSteps(f.n, f.d, g.n, g.d, op).s.join(""); } };
    },
    sum: function () {
      var f, g, op, r;
      do { f = randFr(10); g = randFr(10); op = Math.random() < .5 ? "+" : "-"; r = op === "+" ? radd(f, g) : rsub(f, g); } while ((f.d === g.d && Math.random() < .6) || !r.n || lcm(f.d, g.d) > 60);
      if (Math.random() < .25) f = { n: rint(1, 4), d: 1 }, r = op === "+" ? radd(f, g) : rsub(f, g);
      return { t: "frac", irr: true, ans: r, q: function () { return u("dCalc") + " $" + fr(f) + (op === "+" ? "+" : "-") + fr(g) + "$"; },
        s: function () { return opSteps(f.n, f.d, g.n, g.d, op).s.join(""); } };
    },
    comb: function () {
      var a = randFr(6), b = randFr(6), c = randFr(5), kind = rint(0, 6), e, r;
      var A = a.n + "/" + a.d, B = b.n + "/" + b.d, C = c.n + "/" + c.d;
      if (kind === 0) e = A + "+" + B + "·" + C;
      else if (kind === 1) e = "(" + A + "+" + B + ")·" + C;
      else if (kind === 2) e = A + ":" + B + "-" + C;
      else if (kind === 3) e = "(" + A + "-" + B + "):" + C;
      else if (kind === 4) e = A + "-" + "(" + C + ")^2";
      else if (kind === 5) e = "(" + A + "-1)^2·" + C;
      else e = "1-" + A + "·(" + B + "+" + C + ")";
      r = run(e);
      if (!r.ok || Math.abs(r.v.n) > 200 || r.v.d > 200) return GEN.comb();
      var t = tx(parseExpr(e), null, null, true);
      return { t: "frac", irr: true, ans: r.v, q: function () { return u("dCalc") + " $" + t + "$"; },
        s: function () { return rowsHTML(run(e)).join("") + tex("\\boxed{" + fr(r.v) + "}", true); } };
    },
    pow: function () {
      var k = rint(0, 2), a, b, e, txt;
      if (k === 0) {
        b = rint(2, 5); a = coprimeNum(b) * (Math.random() < .45 ? -1 : 1); var n = pick([0, 1, 2, 2, 3, 3, 4]);
        if (Math.pow(b, n) > 700) n = 2;
        e = "(" + a + "/" + b + ")^" + n;
      } else if (k === 1) {
        b = rint(2, 4); a = coprimeNum(b); var m = rint(2, 5), p = rint(1, 3), q = rint(1, m + p - 1);
        e = "(" + a + "/" + b + ")^" + m + "·(" + a + "/" + b + ")^" + p + ":(" + a + "/" + b + ")^" + q;
        if (Math.pow(Math.max(a, b), m + p - q) > 800) return GEN.pow();
      } else {
        b = rint(2, 4); a = coprimeNum(b); var c = rint(2, 6);
        e = pick(["(" + a + "/" + b + ")^2+" + 1 + "/" + c, "1-(" + a + "/" + b + ")^2", "(" + a + "/" + b + "+1)^2", "(" + a + "/" + b + "-1)^3"]);
      }
      var r = run(e); if (!r.ok || r.v.d > 1000 || Math.abs(r.v.n) > 1000) return GEN.pow();
      txt = tx(parseExpr(e), null, null, true);
      return { t: "frac", irr: true, ans: r.v, q: function () { return u("dPow") + " $" + txt + "$"; },
        s: function () {
          var h = rowsHTML(run(e)).join("");
          if (k === 1) h += hint(u("pwM") + " " + u("pwQq"));
          return h + tex("\\boxed{" + fr(r.v) + "}", true);
        } };
    },
    gen: function () {
      var ent = rint(0, 4), A = Math.random() < .5 ? "" : String(rint(0, 9)) + (Math.random() < .2 ? String(rint(0, 9)) : ""), P, z;
      do { P = String(rint(1, 9)) + (Math.random() < .35 ? String(rint(0, 9)) : ""); } while (/^9+$/.test(P) || (P.length === 2 && P[0] === P[1]) || (A && A.slice(-1) === P.slice(-1)));
      z = gener(String(ent), A, P);
      return { t: "frac", irr: true, ans: z.f, q: function () { return fill(u("dGen"), { x: "$" + z.x + "$" }); },
        s: function () { return tex("x=" + z.x + "=" + z.rule + "=\\boxed{" + fr(z.f) + "}", true); } };
    },
    prob: function () {
      var k = rint(0, 3), a, b, c, d, t, ans;
      if (k === 0) { b = pick([3, 4, 5, 6, 8, 10]); a = coprimeNum(b); t = b * rint(5, 60); ans = t / b * a;
        return { t: "nat", ans: ans, q: function () { return fill(u("dPr1"), { t: ft(t), a: a, b: b }); }, s: function () { return tex(frac(a, b) + "\\cdot " + ft(t) + "=" + frac(a + "\\cdot " + ft(t), b) + "=\\boxed{" + ft(ans) + "}\\text{ L}", true); } }; }
      if (k === 1) { b = pick([3, 4, 5, 6, 7, 8, 9]); a = coprimeNum(b); t = b * rint(10, 120); var p = t / b * a;
        return { t: "nat", ans: t, q: function () { return fill(u("dPr2"), { a: a, b: b, p: ft(p) }); }, s: function () { return tex(ft(p) + ":" + frac(a, b) + "=" + frac(ft(p) + "\\cdot " + b, a) + "=\\boxed{" + ft(t) + "}", true); } }; }
      if (k === 2) { b = pick([2, 3, 4, 5]); a = coprimeNum(b); d = pick([2, 3, 4, 5]); c = coprimeNum(d); t = b * d * rint(2, 25) * 5;
        var l1 = t / b * (b - a), g2 = l1 / d * c, l2 = l1 - g2;
        return { t: "nat", ans: l2, q: function () { return fill(u("dPr3"), { t: ft(t), a: a, b: b, c: c, d: d }); },
          s: function () { return tex(frac(a, b) + "\\cdot " + ft(t) + "=" + ft(t / b * a) + "\\ \\to\\ " + ft(t) + "-" + ft(t / b * a) + "=" + ft(l1) + "\\qquad " + frac(c, d) + "\\cdot " + ft(l1) + "=" + ft(g2) + "\\ \\to\\ " + ft(l1) + "-" + ft(g2) + "=\\boxed{" + ft(l2) + "}\\text{ €}", true); } }; }
      do { b = pick([3, 4, 5, 6, 8, 10]); a = coprimeNum(b); d = pick([3, 4, 5, 6, 8, 10]); c = coprimeNum(d); } while (b === d || a * d + c * b >= b * d);
      var s = radd({ n: a, d: b }, { n: c, d: d }), rr = rsub({ n: 1, d: 1 }, s);
      return { t: "frac", irr: true, ans: rr, q: function () { return fill(u("dPr4"), { a: a, b: b, c: c, d: d }); },
        s: function () { return tex(frac(a, b) + "+" + frac(c, d) + "=" + fr(s) + "\\qquad 1-" + fr(s) + "=\\boxed{" + fr(rr) + "}", true); } };
    }
  };
  function wDrill(w) {
    var kind = w.dataset.kind, q = mk(), done = false, res = 0, ok = 0, tot = 0;
    function mk() { var z = GEN[kind](); if (z.t === "nat") { z.t = "frac"; z.ans = { n: z.ans, d: 1 }; z.irr = false; } return z; }
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
    function fresh() { q = mk(); done = false; inp.value = ""; info.innerHTML = ""; paint(); }
    w.querySelector('[data-a="check"]').addEventListener("click", check);
    w.querySelector('[data-a="new"]').addEventListener("click", function () { fresh(); inp.focus(); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { if (done) fresh(); else check(); } });
    onLang(paint);
  }

  /* ---------- qüestionari ---------- */
  var QUIZ = [
/*QUIZ*/
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

  var TITLES = { va: "Nombres naturals, enters i fraccionaris · FentMates", es: "Números naturales, enteros y fraccionarios · FentMates", en: "Natural numbers, integers and fractions · FentMates" };
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
    wRound(); wCol(); wP10(); wDiv(); wFd(); wGen(); wEq(); wCmp(); wPow(); wRest();
    document.querySelectorAll(".w-ops").forEach(wOps); document.querySelectorAll(".w-hier:not(.wz)").forEach(wHier);
    document.querySelectorAll(".w-drill:not(.wz)").forEach(wDrill); wQuiz();
    window.FM4A1 = { pdec: pdec, dt: dt, ldiv: ldiv, run: run, parseExpr: parseExpr, gener: gener, GEN: GEN };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();

/* 4t ESO A · Unitat 1. Part 2 (naturals i enters): app.js de 2eso-t1 adaptat. Segueix l'idioma de la part 1. */
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

    natc: function () {
      for (;;) {
        var a = rint(2, 9), b = rint(2, 9), c = rint(2, 6), s = rint(3, 10), k = rint(0, 5), e;
        if (k === 0) e = a + "+" + b + "·" + c;
        else if (k === 1) e = "(" + a + "+" + b + ")·" + c + "-" + s;
        else if (k === 2) e = c + "^2+" + a + "·" + b + "-" + s;
        else if (k === 3) e = "√" + s * s + "+" + a + "·(" + (b + c) + "-" + c + ")";
        else if (k === 4) e = a * b * c + ":" + b + "+" + c + "^3";
        else e = "√(" + (s * s - a) + "+" + a + ")·" + b + "-" + c + "^2";
        var res = run(e);
        if (!res.ok || res.v < 0 || res.v > 500) continue;
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
    wCtx(); wLine(); wAbs(); wAdd(); wPar(); wSign(); wPowZ(); wRootZ();
    document.querySelectorAll(".w-hier.wz").forEach(wHier);
    document.querySelectorAll(".w-drill.wz").forEach(wDrill);
    /* l'idioma el canvia la part 1: ací només el seguim */
    new MutationObserver(function () {
      var l = root.getAttribute("data-lang");
      if (l && l !== lang && LANGS.indexOf(l) >= 0) { lang = l; refreshers.forEach(function (fn) { fn(); }); }
    }).observe(root, { attributes: true, attributeFilter: ["data-lang"] });
    window.FM4A1z = { run: run, parseExpr: parseExpr, GEN: GEN };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
