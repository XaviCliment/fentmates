(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2eso-u2-done", NSEC = 11;

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
    { q: { va: "Arrodonit a les centèsimes, $4{,}2961$ és…", es: "Redondeado a las centésimas, $4{,}2961$ es…", en: "Rounded to hundredths, $4{,}2961$ is…" },
      o: [{ va: "$4{,}29$" }, { va: "$4{,}30$" }, { va: "$4{,}3$" }, { va: "$4{,}296$" }], a: 1,
      e: { va: "La primera xifra que eliminem és un 6: sumem 1 a les centèsimes. S'escriu $4{,}30$ per a indicar que és a les centèsimes.", es: "La primera cifra que eliminamos es un 6: sumamos 1 a las centésimas. Se escribe $4{,}30$ para indicar que es a las centésimas.", en: "The first digit removed is 6: add 1 to the hundredths. We write $4{,}30$ to show it's to hundredths." } },
    { q: { va: "Quin d'aquests nombres és un decimal <b>periòdic mixt</b>?", es: "¿Cuál de estos números es un decimal <b>periódico mixto</b>?", en: "Which of these is a <b>mixed recurring</b> decimal?" },
      o: [{ va: "$2{,}333\\ldots$" }, { va: "$2{,}1333\\ldots$" }, { va: "$2{,}13$" }, { va: "$2{,}131331333\\ldots$" }], a: 1,
      e: { va: "En $2{,}1\\overline{3}$ el 1 no es repeteix (anteperíode) i el 3 sí (període). $2{,}\\overline{3}$ és pur, $2{,}13$ és exacte i l'últim no té període.", es: "En $2{,}1\\overline{3}$ el 1 no se repite (anteperiodo) y el 3 sí (periodo). $2{,}\\overline{3}$ es puro, $2{,}13$ es exacto y el último no tiene periodo.", en: "In $2{,}1\\overline{3}$ the 1 doesn't repeat and the 3 does. $2{,}\\overline{3}$ is pure, $2{,}13$ terminates and the last one has no period." } },
    { q: { va: "$\\pi=3{,}14159\\ldots$ és un nombre decimal…", es: "$\\pi=3{,}14159\\ldots$ es un número decimal…", en: "$\\pi=3{,}14159\\ldots$ is a decimal that is…" },
      o: [{ va: "exacte", es: "exacto", en: "terminating" }, { va: "periòdic pur", es: "periódico puro", en: "purely recurring" }, { va: "periòdic mixt", es: "periódico mixto", en: "mixed recurring" }, { va: "no exacte i no periòdic", es: "no exacto y no periódico", en: "neither terminating nor recurring" }], a: 3,
      e: { va: "Té infinites xifres decimals que no es repeteixen mai: no es pot escriure com a fracció.", es: "Tiene infinitas cifras decimales que no se repiten nunca: no se puede escribir como fracción.", en: "It has infinitely many decimals that never repeat: it can't be written as a fraction." } },
    { q: { va: "$2{,}5\\cdot0{,}04=$", es: "$2{,}5\\cdot0{,}04=$", en: "$2{,}5\\cdot0{,}04=$" },
      o: [{ va: "$1$" }, { va: "$0{,}1$" }, { va: "$0{,}01$" }, { va: "$10$" }], a: 1,
      e: { va: "$25\\cdot4=100$ i els factors tenen $1+2=3$ decimals: $0{,}100=0{,}1$.", es: "$25\\cdot4=100$ y los factores tienen $1+2=3$ decimales: $0{,}100=0{,}1$.", en: "$25\\cdot4=100$ and the factors have $1+2=3$ decimals: $0{,}100=0{,}1$." } },
    { q: { va: "$3{,}6:0{,}12=$", es: "$3{,}6:0{,}12=$", en: "$3{,}6:0{,}12=$" },
      o: [{ va: "$0{,}3$" }, { va: "$3$" }, { va: "$30$" }, { va: "$300$" }], a: 2,
      e: { va: "Multipliquem dividend i divisor per 100: $360:12=30$.", es: "Multiplicamos dividendo y divisor por 100: $360:12=30$.", en: "Multiply dividend and divisor by 100: $360:12=30$." } },
    { q: { va: "Quina fracció és equivalent a $\\frac{6}{15}$?", es: "¿Qué fracción es equivalente a $\\frac{6}{15}$?", en: "Which fraction is equivalent to $\\frac{6}{15}$?" },
      o: [{ va: "$\\frac{3}{5}$" }, { va: "$\\frac{2}{5}$" }, { va: "$\\frac{12}{20}$" }, { va: "$\\frac{1}{9}$" }], a: 1,
      e: { va: "Dividim numerador i denominador entre 3: $\\frac{6}{15}=\\frac{2}{5}$ (o bé $6\\cdot5=15\\cdot2$).", es: "Dividimos numerador y denominador entre 3: $\\frac{6}{15}=\\frac{2}{5}$ (o bien $6\\cdot5=15\\cdot2$).", en: "Divide top and bottom by 3: $\\frac{6}{15}=\\frac{2}{5}$ (or check $6\\cdot5=15\\cdot2$)." } },
    { q: { va: "Quina fracció és la més gran?", es: "¿Qué fracción es la mayor?", en: "Which fraction is largest?" },
      o: [{ va: "$\\frac{2}{3}$" }, { va: "$\\frac{3}{4}$" }, { va: "$\\frac{5}{8}$" }, { va: "$\\frac{7}{12}$" }], a: 1,
      e: { va: "Amb denominador 24: $\\frac{16}{24},\\ \\frac{18}{24},\\ \\frac{15}{24},\\ \\frac{14}{24}$. La més gran és $\\frac{3}{4}$.", es: "Con denominador 24: $\\frac{16}{24},\\ \\frac{18}{24},\\ \\frac{15}{24},\\ \\frac{14}{24}$. La mayor es $\\frac{3}{4}$.", en: "With denominator 24: $\\frac{16}{24},\\ \\frac{18}{24},\\ \\frac{15}{24},\\ \\frac{14}{24}$. The largest is $\\frac{3}{4}$." } },
    { q: { va: "Sense fer la divisió, $\\frac{7}{40}$ és un decimal…", es: "Sin hacer la división, $\\frac{7}{40}$ es un decimal…", en: "Without dividing, $\\frac{7}{40}$ is…" },
      o: [{ va: "exacte", es: "exacto", en: "terminating" }, { va: "periòdic pur", es: "periódico puro", en: "purely recurring" }, { va: "periòdic mixt", es: "periódico mixto", en: "mixed recurring" }], a: 0,
      e: { va: "És irreductible i $40=2^3\\cdot5$ només té els factors 2 i 5: és exacte ($0{,}175$).", es: "Es irreducible y $40=2^3\\cdot5$ solo tiene los factores 2 y 5: es exacto ($0{,}175$).", en: "It's in simplest form and $40=2^3\\cdot5$ only has the factors 2 and 5: it terminates ($0{,}175$)." } },
    { q: { va: "La fracció generatriu de $0{,}\\overline{45}$ és…", es: "La fracción generatriz de $0{,}\\overline{45}$ es…", en: "The fraction equal to $0{,}\\overline{45}$ is…" },
      o: [{ va: "$\\frac{45}{100}$" }, { va: "$\\frac{9}{20}$" }, { va: "$\\frac{5}{11}$" }, { va: "$\\frac{41}{90}$" }], a: 2,
      e: { va: "Periòdic pur amb període de 2 xifres: $\\frac{45}{99}=\\frac{5}{11}$.", es: "Periódico puro con periodo de 2 cifras: $\\frac{45}{99}=\\frac{5}{11}$.", en: "Purely recurring with a 2-digit period: $\\frac{45}{99}=\\frac{5}{11}$." } },
    { q: { va: "La fracció generatriu de $1{,}2\\overline{3}$ és…", es: "La fracción generatriz de $1{,}2\\overline{3}$ es…", en: "The fraction equal to $1{,}2\\overline{3}$ is…" },
      o: [{ va: "$\\frac{123}{99}$" }, { va: "$\\frac{111}{90}$" }, { va: "$\\frac{37}{30}$" }, { va: "$\\frac{122}{99}$" }], a: 2,
      e: { va: "$\\frac{123-12}{90}=\\frac{111}{90}$, que simplificada (entre 3) és $\\frac{37}{30}$.", es: "$\\frac{123-12}{90}=\\frac{111}{90}$, que simplificada (entre 3) es $\\frac{37}{30}$.", en: "$\\frac{123-12}{90}=\\frac{111}{90}$, which simplifies (divide by 3) to $\\frac{37}{30}$." } },
    { q: { va: "$\\frac{3}{4}-\\frac{5}{6}=$", es: "$\\frac{3}{4}-\\frac{5}{6}=$", en: "$\\frac{3}{4}-\\frac{5}{6}=$" },
      o: [{ va: "$-\\frac{2}{2}$" }, { va: "$-\\frac{1}{12}$" }, { va: "$\\frac{1}{12}$" }, { va: "$-\\frac{2}{10}$" }], a: 1,
      e: { va: "mcm$(4,6)=12$: $\\frac{9}{12}-\\frac{10}{12}=-\\frac{1}{12}$. Mai no restem numeradors i denominadors per separat!", es: "mcm$(4,6)=12$: $\\frac{9}{12}-\\frac{10}{12}=-\\frac{1}{12}$. ¡Nunca restamos numeradores y denominadores por separado!", en: "lcm$(4,6)=12$: $\\frac{9}{12}-\\frac{10}{12}=-\\frac{1}{12}$. Never subtract tops and bottoms separately!" } },
    { q: { va: "$\\frac{4}{9}\\cdot\\frac{3}{8}=$", es: "$\\frac{4}{9}\\cdot\\frac{3}{8}=$", en: "$\\frac{4}{9}\\cdot\\frac{3}{8}=$" },
      o: [{ va: "$\\frac{7}{17}$" }, { va: "$\\frac{1}{6}$" }, { va: "$\\frac{32}{27}$" }, { va: "$\\frac{12}{17}$" }], a: 1,
      e: { va: "$\\frac{4\\cdot3}{9\\cdot8}=\\frac{12}{72}=\\frac{1}{6}$.", es: "$\\frac{4\\cdot3}{9\\cdot8}=\\frac{12}{72}=\\frac{1}{6}$.", en: "$\\frac{4\\cdot3}{9\\cdot8}=\\frac{12}{72}=\\frac{1}{6}$." } },
    { q: { va: "$\\frac{2}{5}:\\frac{4}{15}=$", es: "$\\frac{2}{5}:\\frac{4}{15}=$", en: "$\\frac{2}{5}:\\frac{4}{15}=$" },
      o: [{ va: "$\\frac{8}{75}$" }, { va: "$\\frac{2}{3}$" }, { va: "$\\frac{3}{2}$" }, { va: "$\\frac{1}{2}$" }], a: 2,
      e: { va: "Multipliquem per la inversa: $\\frac{2}{5}\\cdot\\frac{15}{4}=\\frac{30}{20}=\\frac{3}{2}$.", es: "Multiplicamos por la inversa: $\\frac{2}{5}\\cdot\\frac{15}{4}=\\frac{30}{20}=\\frac{3}{2}$.", en: "Multiply by the reciprocal: $\\frac{2}{5}\\cdot\\frac{15}{4}=\\frac{30}{20}=\\frac{3}{2}$." } },
    { q: { va: "$\\left(-\\frac{2}{3}\\right)^3=$", es: "$\\left(-\\frac{2}{3}\\right)^3=$", en: "$\\left(-\\frac{2}{3}\\right)^3=$" },
      o: [{ va: "$\\frac{8}{27}$" }, { va: "$-\\frac{8}{27}$" }, { va: "$-\\frac{6}{9}$" }, { va: "$-\\frac{8}{9}$" }], a: 1,
      e: { va: "Elevem dalt i baix: $\\frac{2^3}{3^3}=\\frac{8}{27}$, i com que la base és negativa i l'exponent senar, el resultat és negatiu.", es: "Elevamos arriba y abajo: $\\frac{2^3}{3^3}=\\frac{8}{27}$, y como la base es negativa y el exponente impar, el resultado es negativo.", en: "Raise top and bottom: $\\frac{2^3}{3^3}=\\frac{8}{27}$; the base is negative and the exponent odd, so the result is negative." } },
    { q: { va: "$\\left(\\frac{3}{5}\\right)^4\\cdot\\left(\\frac{3}{5}\\right)^2:\\left(\\frac{3}{5}\\right)^5=$", es: "$\\left(\\frac{3}{5}\\right)^4\\cdot\\left(\\frac{3}{5}\\right)^2:\\left(\\frac{3}{5}\\right)^5=$", en: "$\\left(\\frac{3}{5}\\right)^4\\cdot\\left(\\frac{3}{5}\\right)^2:\\left(\\frac{3}{5}\\right)^5=$" },
      o: [{ va: "$\\left(\\frac{3}{5}\\right)^{3}$" }, { va: "$\\frac{3}{5}$" }, { va: "$\\left(\\frac{3}{5}\\right)^{11}$" }, { va: "$1$" }], a: 1,
      e: { va: "Mateixa base: $4+2-5=1$, així que queda $\\left(\\frac{3}{5}\\right)^1=\\frac{3}{5}$.", es: "Misma base: $4+2-5=1$, así que queda $\\left(\\frac{3}{5}\\right)^1=\\frac{3}{5}$.", en: "Same base: $4+2-5=1$, so we get $\\left(\\frac{3}{5}\\right)^1=\\frac{3}{5}$." } },
    { q: { va: "$\\frac{1}{2}+\\frac{1}{2}\\cdot\\frac{4}{3}=$", es: "$\\frac{1}{2}+\\frac{1}{2}\\cdot\\frac{4}{3}=$", en: "$\\frac{1}{2}+\\frac{1}{2}\\cdot\\frac{4}{3}=$" },
      o: [{ va: "$\\frac{4}{3}$" }, { va: "$\\frac{7}{6}$" }, { va: "$\\frac{5}{6}$" }, { va: "$\\frac{2}{3}$" }], a: 1,
      e: { va: "Primer el producte: $\\frac{1}{2}\\cdot\\frac{4}{3}=\\frac{2}{3}$. Després la suma: $\\frac{1}{2}+\\frac{2}{3}=\\frac{7}{6}$.", es: "Primero el producto: $\\frac{1}{2}\\cdot\\frac{4}{3}=\\frac{2}{3}$. Después la suma: $\\frac{1}{2}+\\frac{2}{3}=\\frac{7}{6}$.", en: "Product first: $\\frac{1}{2}\\cdot\\frac{4}{3}=\\frac{2}{3}$. Then the sum: $\\frac{1}{2}+\\frac{2}{3}=\\frac{7}{6}$." } },
    { q: { va: "Els $\\frac{3}{5}$ d'una quantitat són 36. Quina és la quantitat?", es: "Los $\\frac{3}{5}$ de una cantidad son 36. ¿Cuál es la cantidad?", en: "$\\frac{3}{5}$ of an amount is 36. What is the amount?" },
      o: [{ va: "$21{,}6$" }, { va: "$60$" }, { va: "$45$" }, { va: "$108$" }], a: 1,
      e: { va: "Cada cinquena part val $36:3=12$; el total són 5 parts: $12\\cdot5=60$.", es: "Cada quinta parte vale $36:3=12$; el total son 5 partes: $12\\cdot5=60$.", en: "Each fifth is $36:3=12$; the whole is 5 fifths: $12\\cdot5=60$." } },
    { q: { va: "Gastem $\\frac{1}{4}$ dels diners i després $\\frac{2}{3}$ del que queda. Quina fracció dels diners ens queda?", es: "Gastamos $\\frac{1}{4}$ del dinero y después $\\frac{2}{3}$ de lo que queda. ¿Qué fracción del dinero nos queda?", en: "We spend $\\frac{1}{4}$ of our money and then $\\frac{2}{3}$ of what's left. What fraction of the money is left?" },
      o: [{ va: "$\\frac{1}{12}$" }, { va: "$\\frac{1}{4}$" }, { va: "$\\frac{1}{2}$" }, { va: "$\\frac{5}{12}$" }], a: 1,
      e: { va: "Queden $\\frac{3}{4}$; en gastem $\\frac{2}{3}\\cdot\\frac{3}{4}=\\frac{1}{2}$. Queda $\\frac{3}{4}-\\frac{1}{2}=\\frac{1}{4}$ (o bé $\\frac{1}{3}$ de $\\frac{3}{4}$).", es: "Quedan $\\frac{3}{4}$; gastamos $\\frac{2}{3}\\cdot\\frac{3}{4}=\\frac{1}{2}$. Queda $\\frac{3}{4}-\\frac{1}{2}=\\frac{1}{4}$ (o bien $\\frac{1}{3}$ de $\\frac{3}{4}$).", en: "$\\frac{3}{4}$ is left; we spend $\\frac{2}{3}\\cdot\\frac{3}{4}=\\frac{1}{2}$. Left: $\\frac{3}{4}-\\frac{1}{2}=\\frac{1}{4}$ (that is, $\\frac{1}{3}$ of $\\frac{3}{4}$)." } }
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

  var TITLES = { va: "Decimals i fraccions · FentMates", es: "Decimales y fracciones · FentMates", en: "Decimals and fractions · FentMates" };
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
    document.querySelectorAll(".w-ops").forEach(wOps); document.querySelectorAll(".w-hier").forEach(wHier);
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
    window.FM22 = { pdec: pdec, dt: dt, ldiv: ldiv, run: run, parseExpr: parseExpr, gener: gener, GEN: GEN };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
