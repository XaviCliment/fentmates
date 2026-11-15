(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-2eso-u6-done", NSEC = 8;


  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      repBad: "Escriu una quantitat positiva i entre 2 i 6 nombres positius separats per punt i coma.", repSum: "Comprovació: la suma de les parts és",
      repInv: "Inversament a {v} → directament als inversos. Amb el m.c.m. ({m}) queden enters:", share: "rep",
      compoD: "directa: multipliquem per", compoI: "inversa: multipliquem per", compoBad: "Omple totes les caselles amb nombres positius.",
      compoTip: "Fes clic en D / I per a canviar el tipus de relació amb la incògnita.", rel: "Relació",
      dCoI: "{a} obrers, treballant {b} hores al dia, fan una obra en {c} dies. Quants dies tardaran {d} obrers treballant {e} hores al dia?",
      dCoD: "{a} vaques mengen {b} kg de pinso en {c} dies. Quants kg de pinso menjaran {d} vaques en {e} dies?",
      dCoIh: "Més obrers → menys dies (I); més hores al dia → menys dies (I).", dCoDh: "Més vaques → més pinso (D); més dies → més pinso (D).",
      dRepD: "Reparteix {n} en parts directament proporcionals a {v}. Quant correspon a la part proporcional a {x}?",
      dRepI: "Reparteix {n} en parts inversament proporcionals a {v}. Quant correspon a la part inversament proporcional a {x}?",
      dRepIh: "Repartim directament als inversos; amb el m.c.m. ({m}), als nombres {w}.",
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
      repBad: "Escribe una cantidad positiva y entre 2 y 6 números positivos separados por punto y coma.", repSum: "Comprobación: la suma de las partes es",
      repInv: "Inversamente a {v} → directamente a los inversos. Con el m.c.m. ({m}) quedan enteros:", share: "recibe",
      compoD: "directa: multiplicamos por", compoI: "inversa: multiplicamos por", compoBad: "Rellena todas las casillas con números positivos.",
      compoTip: "Haz clic en D / I para cambiar el tipo de relación con la incógnita.", rel: "Relación",
      dCoI: "{a} obreros, trabajando {b} horas al día, hacen una obra en {c} días. ¿Cuántos días tardarán {d} obreros trabajando {e} horas al día?",
      dCoD: "{a} vacas comen {b} kg de pienso en {c} días. ¿Cuántos kg de pienso comerán {d} vacas en {e} días?",
      dCoIh: "Más obreros → menos días (I); más horas al día → menos días (I).", dCoDh: "Más vacas → más pienso (D); más días → más pienso (D).",
      dRepD: "Reparte {n} en partes directamente proporcionales a {v}. ¿Cuánto corresponde a la parte proporcional a {x}?",
      dRepI: "Reparte {n} en partes inversamente proporcionales a {v}. ¿Cuánto corresponde a la parte inversamente proporcional a {x}?",
      dRepIh: "Repartimos directamente a los inversos; con el m.c.m. ({m}), a los números {w}.",
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
      repBad: "Type a positive amount and 2 to 6 positive numbers separated by semicolons.", repSum: "Check: the shares add up to",
      repInv: "Inversely to {v} → directly to the reciprocals. Using the LCM ({m}) they become whole numbers:", share: "gets",
      compoD: "direct: multiply by", compoI: "inverse: multiply by", compoBad: "Fill every box with a positive number.",
      compoTip: "Click D / I to change the type of relation with the unknown.", rel: "Relation",
      dCoI: "{a} builders, working {b} hours a day, finish a job in {c} days. How many days will {d} builders working {e} hours a day take?",
      dCoD: "{a} cows eat {b} kg of feed in {c} days. How many kg of feed will {d} cows eat in {e} days?",
      dCoIh: "More builders → fewer days (I); more hours a day → fewer days (I).", dCoDh: "More cows → more feed (D); more days → more feed (D).",
      dRepD: "Share {n} in direct proportion to {v}. How much is the share for {x}?",
      dRepI: "Share {n} in inverse proportion to {v}. How much is the share for {x}?",
      dRepIh: "We share directly in proportion to the reciprocals; using the LCM ({m}), to the numbers {w}.",
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

  /* ---------- 6.1 terme desconegut d'una proporció ---------- */
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

  /* ---------- 6.2-6.3 regla de tres ---------- */
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

  /* ---------- 6.3 directa, inversa o cap ---------- */
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

  /* ---------- 6.6-6.7 percentatges ---------- */
  function shiftD(x, s) { return D(x.i, x.k + s); }
  function bars(rows) {
    var mx = Math.max.apply(null, rows.map(function (r) { return r.v; })) || 1;
    return '<div class="vbars">' + rows.map(function (r) { return '<div class="vbar"><span>' + r.l + '</span><div class="tr"><div class="fl ' + (r.c || "") + '" style="width:' + Math.max(8, r.v / mx * 100).toFixed(1) + '%">' + r.t + "</div></div></div>"; }).join("") + "</div>";
  }
  function wPct(w) {
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

  /* ---------- 6.8 augments i disminucions ---------- */
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

  /* ---------- 6.4-6.5 proporcionalitat composta i repartiments (ginys de 3r ESO, amb els seus formats) ---------- */
  function M3() {
  function pn(s) {
    s = String(s).trim().replace(/\s/g, "").replace("−", "-").replace(",", ".");
    if (!/^-?(\d+\.?\d*|\.\d+)$/.test(s)) return NaN;
    return parseFloat(s);
  }
  function rnd(x, d) { var f = Math.pow(10, d); return Math.round(x * f) / f; }
  function fcore(x, d, dec, th, keep) {
    if (!isFinite(x)) return "—";
    if (d == null) d = 2;
    var neg = x < 0, s = Math.abs(rnd(x, d)).toFixed(d);
    if (keep && /\.\d*[1-9]/.test(s)) { /* manté 2 decimals per als diners */ }
    else if (s.indexOf(".") >= 0) s = s.replace(/0+$/, "").replace(/\.$/, "");
    var p = s.split(".");
    if (p[0].length > 4) p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, th);
    return (neg && +s !== 0 ? "-" : "") + p[0] + (p[1] ? dec + p[1] : "");
  }
  function fh(x, d, keep) { return fcore(x, d, lang === "en" ? "." : ",", " ", keep).replace("-", "−"); }
  function ft(x, d, keep) { return fcore(x, d, lang === "en" ? "." : "{,}", "\\,", keep); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function wRep() {
    var w = document.getElementById("w-rep"); if (!w) return;
    var mode = "d", iN = w.querySelector('[data-k="n"]'), iV = w.querySelector('[data-k="v"]'), stack = w.querySelector(".stack"), info = w.querySelector(".info");
    function render() {
      var N = pn(iN.value), vs = iV.value.split(/[;\s]+/).filter(function (s) { return s !== ""; }).map(pn);
      if (!(N > 0) || vs.length < 2 || vs.length > 6 || vs.some(function (v) { return !(v > 0); })) { info.innerHTML = warn("repBad"); stack.innerHTML = ""; return; }
      var ints = vs.every(function (v) { return v === Math.round(v) && v <= 1e4; }), wts, h = "";
      if (mode === "d") wts = vs.slice();
      else if (ints) {
        var m = vs.reduce(function (a, b) { return lcm(a, b); }, 1);
        wts = vs.map(function (v) { return m / v; });
        h += '<div class="hint">' + fill(u("repInv"), { v: vs.map(function (v) { return fh(v); }).join(", "), m: fh(m) }) + "</div>" + tex(vs.map(function (v) { return "\\frac{1}{" + ft(v) + "}=\\frac{" + ft(m / v) + "}{" + ft(m) + "}"; }).join(",\\quad "), true);
      } else wts = vs.map(function (v) { return 1 / v; });
      var S = wts.reduce(function (a, b) { return a + b; }, 0), k = N / S, sh = wts.map(function (x) { return k * x; });
      var wt = function (x) { return mode === "i" && !ints ? "\\frac{1}{" + ft(1 / x, 4) + "}" : ft(x, 4); };
      h += tex("k=\\frac{" + ft(N, 2) + "}{" + wts.map(wt).join("+") + "}=\\frac{" + ft(N, 2) + "}{" + ft(S, 4) + "}" + (Math.abs(rnd(k, 4) - k) > 1e-9 ? "\\approx " : "=") + ft(k, 4), true);
      h += "<ul>" + sh.map(function (s, i) { return "<li><strong>" + String.fromCharCode(65 + i) + "</strong> (" + fh(vs[i], 4) + ") " + u("share") + " " + tex(wt(wts[i]) + "\\cdot" + ft(k, 4) + (Math.abs(rnd(s, 2) - s) > 1e-9 ? "\\approx" : "=") + ft(s, 2, true)) + "</li>"; }).join("") + "</ul>";
      h += '<div class="hint">' + u("repSum") + " " + fh(sh.reduce(function (a, b) { return a + b; }, 0), 2, true) + " ✓</div>";
      stack.innerHTML = sh.map(function (s, i) { return '<div class="k' + (i + 1) + '" style="flex-grow:' + s + '" title="' + fh(s, 2, true) + '">' + String.fromCharCode(65 + i) + ": " + fh(s, 2, true) + "</div>"; }).join("");
      info.innerHTML = h;
    }
    iN.addEventListener("input", render); iV.addEventListener("input", render);
    segBind(w, function (k) { mode = k; render(); });
    w.querySelectorAll(".quick button[data-b]").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = b.dataset.b.split(";"); mode = p[0];
        w.querySelectorAll(".seg button").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.k === mode)); });
        iN.value = p[1]; iV.value = p.slice(2).map(function (t) { return t.trim(); }).join("; "); render();
      });
    });
    onLang(render);
  }


  var PRE = [
    { n: { va: ["Aixetes", "Hores", "Litres"], es: ["Grifos", "Horas", "Litros"], en: ["Taps", "Hours", "Litres"] }, rel: ["D", "D"], a: [5, 6], x: 9000, b: [3, 8] },
    { n: { va: ["Obrers", "Hores/dia", "Dies"], es: ["Obreros", "Horas/día", "Días"], en: ["Builders", "Hours/day", "Days"] }, rel: ["I", "I"], a: [8, 6], x: 15, b: [10, 9] },
    { n: { va: ["Gallines", "Dies", "Pinso (kg)"], es: ["Gallinas", "Días", "Pienso (kg)"], en: ["Hens", "Days", "Feed (kg)"] }, rel: ["D", "D"], a: [12, 10], x: 18, b: [20, 15] },
    { n: { va: ["Màquines", "Hores/dia", "Peces", "Dies"], es: ["Máquinas", "Horas/día", "Piezas", "Días"], en: ["Machines", "Hours/day", "Parts", "Days"] }, rel: ["I", "I", "D"], a: [9, 8, 4320], x: 5, b: [12, 6, 6480] }
  ];
  function wCompo() {
    var w = document.getElementById("w-compo"); if (!w) return;
    var tbl = w.querySelector("table.compo"), info = w.querySelector(".info"), cur = null;
    function load(i) { var p = PRE[i]; cur = { pi: i, rel: p.rel.slice(), a: p.a.map(String), x: String(p.x), b: p.b.map(String) }; build(); }
    function build() {
      var p = PRE[cur.pi], nm = p.n[lang], k = cur.rel.length, h = "<thead><tr>";
      for (var i = 0; i <= k; i++) h += "<th>" + esc(nm[i]) + "</th>";
      h += "</tr></thead><tbody><tr>";
      for (i = 0; i < k; i++) h += '<td><input class="tin" type="text" inputmode="decimal" data-r="a" data-i="' + i + '" value="' + esc(cur.a[i].replace(".", lang === "en" ? "." : ",")) + '"></td>';
      h += '<td><input class="tin" type="text" inputmode="decimal" data-r="x" value="' + esc(cur.x.replace(".", lang === "en" ? "." : ",")) + '"></td></tr><tr>';
      for (i = 0; i < k; i++) h += '<td><input class="tin" type="text" inputmode="decimal" data-r="b" data-i="' + i + '" value="' + esc(cur.b[i].replace(".", lang === "en" ? "." : ",")) + '"></td>';
      h += '<td class="x">x</td></tr><tr class="grp">';
      for (i = 0; i < k; i++) h += '<td><button type="button" class="rel ' + cur.rel[i] + '" data-i="' + i + '" title="' + esc(u("compoTip")) + '">' + cur.rel[i] + "</button></td>";
      h += "<td>" + esc(u("rel")) + "</td></tr></tbody>";
      tbl.innerHTML = h;
      tbl.querySelectorAll("input").forEach(function (inp) {
        inp.addEventListener("input", function () { if (inp.dataset.r === "x") cur.x = inp.value; else cur[inp.dataset.r][+inp.dataset.i] = inp.value; calc(); });
      });
      tbl.querySelectorAll(".rel").forEach(function (b) {
        b.addEventListener("click", function () { var i = +b.dataset.i; cur.rel[i] = cur.rel[i] === "D" ? "I" : "D"; b.className = "rel " + cur.rel[i]; b.textContent = cur.rel[i]; calc(); });
      });
      calc();
    }
    function calc() {
      var nm = PRE[cur.pi].n[lang], a = cur.a.map(pn), b = cur.b.map(pn), x1 = pn(cur.x);
      if (!(x1 > 0) || a.concat(b).some(function (v) { return !(v > 0); })) { info.innerHTML = warn("compoBad"); return; }
      var x = x1, fr = [], li = "", num = x1, den = 1;
      cur.rel.forEach(function (r, i) {
        var t = r === "D" ? "\\frac{" + ft(b[i], 4) + "}{" + ft(a[i], 4) + "}" : "\\frac{" + ft(a[i], 4) + "}{" + ft(b[i], 4) + "}";
        x *= r === "D" ? b[i] / a[i] : a[i] / b[i];
        num *= r === "D" ? b[i] : a[i]; den *= r === "D" ? a[i] : b[i];
        fr.push(t);
        li += "<li><strong>" + esc(nm[i]) + "</strong>: " + fh(a[i], 4) + " → " + fh(b[i], 4) + " · " + u(r === "D" ? "compoD" : "compoI") + " " + tex(t) + "</li>";
      });
      var s = "x=" + ft(x1, 4) + "\\cdot" + fr.join("\\cdot") + "=\\frac{" + ft(num, 4) + "}{" + ft(den, 4) + "}" + (Math.abs(rnd(x, 4) - x) > 1e-9 ? "\\approx" : "=") + "\\boxed{" + ft(x, 4) + "}";
      info.innerHTML = "<ul>" + li + "</ul>" + tex(s, true) + '<div class="hint">' + u("compoTip") + "</div>";
    }
    w.querySelectorAll("[data-pre]").forEach(function (b) { b.addEventListener("click", function () { load(+b.dataset.pre); }); });
    load(0);
    refreshers.push(build);
  }
  wRep(); wCompo();
  }

  /* ---------- entrenadors ---------- */
  function rdD(maxI, k) { return D(rint(0, maxI) * p10(k) + rint(1, p10(k) - 1), k, true); }
  var R3T = {
    d: [{ va: "Si {a} kg de pomes costen {b} €, quant costen {c} kg?", es: "Si {a} kg de manzanas cuestan {b} €, ¿cuánto cuestan {c} kg?", en: "If {a} kg of apples cost {b} €, how much do {c} kg cost?", u: "€" },
        { va: "{a} entrades de cine costen {b} €. Quant costen {c} entrades?", es: "{a} entradas de cine cuestan {b} €. ¿Cuánto cuestan {c} entradas?", en: "{a} cinema tickets cost {b} €. How much do {c} tickets cost?", u: "€" },
        { va: "Un cotxe gasta {b} L en {a} hores. Quants litres gasta en {c} hores (a la mateixa velocitat)?", es: "Un coche gasta {b} L en {a} horas. ¿Cuántos litros gasta en {c} horas (a la misma velocidad)?", en: "A car uses {b} L in {a} hours. How many litres in {c} hours (same speed)?", u: "L" },
        { va: "{a} m de tela costen {b} €. Quant costen {c} m de la mateixa tela?", es: "{a} m de tela cuestan {b} €. ¿Cuánto cuestan {c} m de la misma tela?", en: "{a} m of cloth cost {b} €. How much do {c} m of the same cloth cost?", u: "€" }],
    i: [{ va: "{a} pintors pinten una nau en {b} dies. Quants dies tardarien {c} pintors?", es: "{a} pintores pintan una nave en {b} días. ¿Cuántos días tardarían {c} pintores?", en: "{a} painters paint a warehouse in {b} days. How many days would {c} painters take?", u: "" },
        { va: "{a} aixetes omplin un dipòsit en {b} hores. Quantes hores tardarien {c} aixetes iguals?", es: "{a} grifos llenan un depósito en {b} horas. ¿Cuántas horas tardarían {c} grifos iguales?", en: "{a} taps fill a tank in {b} hours. How many hours would {c} identical taps take?", u: "h" },
        { va: "Repartim uns caramels entre {a} xiquets i en toquen {b} a cadascun. Quants en tocarien si foren {c} xiquets?", es: "Repartimos unos caramelos entre {a} niños y tocan a {b} cada uno. ¿Cuántos tocarían si fueran {c} niños?", en: "We share some sweets among {a} children and each gets {b}. How many would each get if there were {c} children?", u: "" },
        { va: "{a} amics paguen {b} € cadascun per un regal. Quant pagaria cadascun si foren {c} amics?", es: "{a} amigos pagan {b} € cada uno por un regalo. ¿Cuánto pagaría cada uno si fueran {c} amigos?", en: "{a} friends pay {b} € each for a present. How much would each pay if there were {c} friends?", u: "€" }]
  };
  var GEN = {
    prop: function () {
      var a = rint(1, 9), b = rint(2, 9), m = pick([N(2), N(3), N(4), N(5), D(15, 1), D(25, 1), N(6)]), c = dmul(N(a), m), d = dmul(N(b), m);
      if (a === b) return GEN.prop();
      var v = [N(a), N(b), c, d], pos = rint(0, 3), ans = v[pos];
      var T = function (j) { return j === pos ? "x" : dt(v[j]); };
      return { t: "dec", ans: ans, q: function () { return u("dX") + " $" + frac(T(0), T(1)) + "=" + frac(T(2), T(3)) + "$"; },
        s: function () { return tex(frac(dt(v[0]), dt(v[1])) + "=" + frac(dt(v[2]), dt(v[3])) + "\\qquad x=\\boxed{" + dt(ans) + "}", true) + hint(tex(dt(v[0]) + "\\cdot " + dt(v[3]) + "=" + dt(v[1]) + "\\cdot " + dt(v[2]) + "=" + dt(dmul(v[0], v[3])))); } };
    },
    r3d: function () { return GEN.r3("d"); },
    r3: function (tt) {
      var t = tt || (Math.random() < .5 ? "d" : "i"), T = pick(R3T[t]), a, b, c, ans;
      if (t === "d") { a = rint(2, 9); var un = D(rint(30, 990), 2); b = dmul(N(a), un); do { c = rint(2, 15); } while (c === a); ans = dmul(N(c), un); }
      else {
        var P; do { a = rint(2, 12); b = N(rint(2, 20)); P = a * b.i; c = pick([2, 3, 4, 5, 6, 8, 10, 12, 15, 20].filter(function (x) { return x !== a && P % x === 0; })); } while (!c);
        ans = N(P / c);
      }
      return { t: "dec", ans: ans, q: function () { return fill(T[lang] || T.va, { a: a, b: "$" + dt(b, T.u === "€" && b.k ? 2 : 0) + "$", c: c }); },
        s: function () { return tex(t === "d" ? "x=" + frac(dt(b) + "\\cdot " + c, a) + "=\\boxed{" + dt(ans) + "}" : "x=" + frac(a + "\\cdot " + dt(b), c) + "=\\boxed{" + dt(ans) + "}", true) + hint(u(t === "d" ? "r3D" : "r3I")); } };
    },
    pof: function () {
      var p = pick([N(5), N(10), N(12), N(15), N(20), N(25), N(30), N(40), N(60), N(75), N(80), N(4), N(21), D(25, 1), D(125, 1)]), n = N(rint(2, 60) * 10), a = dmul(n, shiftD(p, 2));
      return { t: "dec", ans: a, q: function () { return fill(u("dPct"), { p: dt(p), n: dt(n) }); }, s: function () { return tex(dt(n) + "\\cdot " + dt(shiftD(p, 2)) + "=\\boxed{" + dt(a) + "}", true); } };
    },
    pwh: function () {
      var n1 = pick([20, 25, 40, 50, 80, 120, 160, 200, 250, 400, 500, 800]), st = n1 / gcd(100, n1), a1 = st * rint(1, Math.floor((n1 - 1) / st)), pc = a1 * 100 / n1;
      return { t: "dec", ans: N(pc), q: function () { return fill(u("dPctW"), { a: ft(a1), n: ft(n1) }); }, s: function () { return tex(frac(a1, n1) + "=" + dt(D(pc, 2)) + "=\\boxed{" + pc + "\\,\\%}", true); } };
    },
    ptot: function () {
      var p2 = pick([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80]), n2 = rint(2, 40) * 20, a2 = dmul(N(n2), D(p2, 2));
      return { t: "dec", ans: N(n2), q: function () { return fill(u("dPctT"), { p: p2, a: dt(a2) }); }, s: function () { return tex(dt(a2) + ":" + dt(D(p2, 2)) + "=\\boxed{" + ft(n2) + "}", true) + hint(u("check") + " " + tex(ft(n2) + "\\cdot " + dt(D(p2, 2)) + "=" + dt(a2))); } };
    },
    compo: function () {
      var a, b, c, d, e, P, ans;
      if (Math.random() < .5) {
        do { a = rint(3, 12); b = pick([4, 5, 6, 8, 10]); c = rint(4, 20); d = rint(3, 12); e = pick([4, 5, 6, 8, 10]); P = a * b * c; } while ((a === d && b === e) || P % (d * e) !== 0 || P / (d * e) > 60);
        ans = P / (d * e);
        return { t: "dec", ans: N(ans), q: function () { return fill(u("dCoI"), { a: a, b: b, c: c, d: d, e: e }); },
          s: function () { return tex("x=" + c + "\\cdot" + frac(a, d) + "\\cdot" + frac(b, e) + "=" + frac(ft(P), ft(d * e)) + "=\\boxed{" + ft(ans) + "}", true) + hint(u("dCoIh")); } };
      }
      var kk = rint(2, 9);
      do { a = rint(2, 12); c = rint(2, 10); d = rint(2, 15); e = rint(2, 15); } while (a === d && c === e);
      b = a * c * kk; ans = kk * d * e;
      return { t: "dec", ans: N(ans), q: function () { return fill(u("dCoD"), { a: a, b: ft(b), c: c, d: d, e: e }); },
        s: function () { return tex("x=" + ft(b) + "\\cdot" + frac(d, a) + "\\cdot" + frac(e, c) + "=\\boxed{" + ft(ans) + "}", true) + hint(u("dCoDh")); } };
    },
    rep: function () {
      var inv = Math.random() < .4, vs, w, m = 1;
      if (inv) { vs = pick([[2, 3], [3, 4], [2, 5], [2, 3, 6], [2, 3, 4], [3, 4, 6], [2, 4, 8], [3, 6, 9], [4, 6, 12], [2, 5, 10]]); m = vs.reduce(function (x, y) { return lcm(x, y); }, 1); w = vs.map(function (v) { return m / v; }); }
      else { vs = []; while (vs.length < 3) { var v = rint(2, 12); if (vs.indexOf(v) < 0) vs.push(v); } vs.sort(function (x, y) { return x - y; }); w = vs; }
      var S = w.reduce(function (x, y) { return x + y; }, 0), k = rint(2, 40) * pick([1, 5, 10]), Nn = S * k, j = rint(0, vs.length - 1), ans = w[j] * k;
      return { t: "dec", ans: N(ans), q: function () { return fill(u(inv ? "dRepI" : "dRepD"), { n: ft(Nn), v: vs.join(", "), x: vs[j] }); },
        s: function () { return (inv ? hint(fill(u("dRepIh"), { m: m, w: w.join(", ") })) : "") + tex("k=" + frac(ft(Nn), w.join("+")) + "=" + frac(ft(Nn), S) + "=" + ft(k) + "\\qquad " + w[j] + "\\cdot " + ft(k) + "=\\boxed{" + ft(ans) + "}", true); } };
    },
    var: function () {
      var up = Math.random() < .45, p = pick(up ? [4, 10, 15, 20, 21, 25, 30, 50] : [5, 10, 12, 15, 20, 25, 30, 40, 50]), q = N(rint(2, 60) * pick([5, 10, 4])), idx = up ? dadd(N(1), D(p, 2)) : dsub(N(1), D(p, 2)), f = dmul(q, idx);
      if (Math.random() < .3) return { t: "dec", ans: q, q: function () { return fill(u(up ? "dVarIu" : "dVarId"), { p: p, f: "$" + dt(f, f.k ? 2 : 0) + "$" }); }, s: function () { return tex(dt(f) + ":" + dt(idx) + "=\\boxed{" + dt(q) + "}", true); } };
      return { t: "dec", ans: f, q: function () { return fill(u(up ? "dVarU" : "dVarD"), { p: p, q: "$" + dt(q) + "$" }); }, s: function () { return tex(dt(q) + "\\cdot " + dt(idx) + "=\\boxed{" + dt(f) + "}", true); } };
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
    { q: { va: "En una classe hi ha 12 xics i 18 xiques. La raó entre xics i xiques és…", es: "En una clase hay 12 chicos y 18 chicas. La razón entre chicos y chicas es…", en: "A class has 12 boys and 18 girls. The ratio of boys to girls is…" },
      o: [{ va: "$\\frac{3}{2}$" }, { va: "$\\frac{2}{3}$" }, { va: "$\\frac{2}{5}$" }, { va: "$\\frac{12}{30}$" }], a: 1,
      e: { va: "$\\frac{12}{18}=\\frac{2}{3}$: per cada 2 xics hi ha 3 xiques.", es: "$\\frac{12}{18}=\\frac{2}{3}$: por cada 2 chicos hay 3 chicas.", en: "$\\frac{12}{18}=\\frac{2}{3}$: for every 2 boys there are 3 girls." } },
    { q: { va: "Si $\\frac{6}{x}=\\frac{9}{12}$, quant val $x$?", es: "Si $\\frac{6}{x}=\\frac{9}{12}$, ¿cuánto vale $x$?", en: "If $\\frac{6}{x}=\\frac{9}{12}$, what is $x$?" },
      o: [{ va: "$4{,}5$" }, { va: "$8$" }, { va: "$18$" }, { va: "$9$" }], a: 1,
      e: { va: "$9\\cdot x=6\\cdot12=72$, així que $x=72:9=8$.", es: "$9\\cdot x=6\\cdot12=72$, así que $x=72:9=8$.", en: "$9\\cdot x=6\\cdot12=72$, so $x=72:9=8$." } },
    { q: { va: "Quina parella de raons <b>no</b> forma proporció?", es: "¿Qué pareja de razones <b>no</b> forma proporción?", en: "Which pair of ratios does <b>not</b> form a proportion?" },
      o: [{ va: "$\\frac{4}{6}$ i $\\frac{10}{15}$", es: "$\\frac{4}{6}$ y $\\frac{10}{15}$", en: "$\\frac{4}{6}$ and $\\frac{10}{15}$" }, { va: "$\\frac{3}{5}$ i $\\frac{12}{20}$", es: "$\\frac{3}{5}$ y $\\frac{12}{20}$", en: "$\\frac{3}{5}$ and $\\frac{12}{20}$" }, { va: "$\\frac{8}{12}$ i $\\frac{6}{10}$", es: "$\\frac{8}{12}$ y $\\frac{6}{10}$", en: "$\\frac{8}{12}$ and $\\frac{6}{10}$" }, { va: "$\\frac{2}{7}$ i $\\frac{6}{21}$", es: "$\\frac{2}{7}$ y $\\frac{6}{21}$", en: "$\\frac{2}{7}$ and $\\frac{6}{21}$" }], a: 2,
      e: { va: "$8\\cdot10=80$ però $12\\cdot6=72$: els productes creuats no coincideixen.", es: "$8\\cdot10=80$ pero $12\\cdot6=72$: los productos cruzados no coinciden.", en: "$8\\cdot10=80$ but $12\\cdot6=72$: the cross products don't match." } },
    { q: { va: "Quina parella de magnituds és <b>directament</b> proporcional?", es: "¿Qué pareja de magnitudes es <b>directamente</b> proporcional?", en: "Which pair of quantities is <b>directly</b> proportional?" },
      o: [{ va: "Edat i altura d'una persona", es: "Edad y altura de una persona", en: "A person's age and height" }, { va: "Velocitat i temps d'un trajecte", es: "Velocidad y tiempo de un trayecto", en: "Speed and time for a journey" }, { va: "Litres de gasolina i preu", es: "Litros de gasolina y precio", en: "Litres of petrol and price" }, { va: "Obrers i dies que tarden", es: "Obreros y días que tardan", en: "Builders and days they take" }], a: 2,
      e: { va: "El doble de litres costa el doble: el quocient (el preu per litre) és constant.", es: "El doble de litros cuesta el doble: el cociente (el precio por litro) es constante.", en: "Twice the litres cost twice as much: the quotient (price per litre) is constant." } },
    { q: { va: "En una taula de proporcionalitat directa, a 4 li correspon 10. Què li correspon a 6?", es: "En una tabla de proporcionalidad directa, a 4 le corresponde 10. ¿Qué le corresponde a 6?", en: "In a direct proportion table, 4 corresponds to 10. What corresponds to 6?" },
      o: [{ va: "$12$" }, { va: "$15$" }, { va: "$\\frac{20}{3}$" }, { va: "$24$" }], a: 1,
      e: { va: "Constant $k=10:4=2{,}5$; $6\\cdot2{,}5=15$.", es: "Constante $k=10:4=2{,}5$; $6\\cdot2{,}5=15$.", en: "Constant $k=10:4=2{,}5$; $6\\cdot2{,}5=15$." } },
    { q: { va: "8 bolígrafs costen 6 €. Quant costen 12 bolígrafs?", es: "8 bolígrafos cuestan 6 €. ¿Cuánto cuestan 12 bolígrafos?", en: "8 pens cost 6 €. How much do 12 pens cost?" },
      o: [{ va: "$4$ €" }, { va: "$9$ €" }, { va: "$10$ €" }, { va: "$16$ €" }], a: 1,
      e: { va: "Un bolígraf: $6:8=0{,}75$ €. Dotze: $0{,}75\\cdot12=9$ €.", es: "Un bolígrafo: $6:8=0{,}75$ €. Doce: $0{,}75\\cdot12=9$ €.", en: "One pen: $6:8=0{,}75$ €. Twelve: $0{,}75\\cdot12=9$ €." } },
    { q: { va: "En una relació de proporcionalitat <b>inversa</b>, què es manté constant?", es: "En una relación de proporcionalidad <b>inversa</b>, ¿qué se mantiene constante?", en: "In an <b>inverse</b> proportion, what stays constant?" },
      o: [{ va: "La suma", es: "La suma", en: "The sum" }, { va: "El quocient", es: "El cociente", en: "The quotient" }, { va: "El producte", es: "El producto", en: "The product" }, { va: "La diferència", es: "La diferencia", en: "The difference" }], a: 2,
      e: { va: "Si una es multiplica per un nombre i l'altra es divideix pel mateix, el producte no canvia.", es: "Si una se multiplica por un número y la otra se divide por el mismo, el producto no cambia.", en: "If one is multiplied by a number and the other divided by it, the product doesn't change." } },
    { q: { va: "6 obrers fan una paret en 10 dies. Quant tardarien 4 obrers?", es: "6 obreros hacen una pared en 10 días. ¿Cuánto tardarían 4 obreros?", en: "6 builders build a wall in 10 days. How long would 4 builders take?" },
      o: [{ va: "$6{,}7$ dies", es: "$6{,}7$ días", en: "$6{,}7$ days" }, { va: "$8$ dies", es: "$8$ días", en: "$8$ days" }, { va: "$15$ dies", es: "$15$ días", en: "$15$ days" }, { va: "$24$ dies", es: "$24$ días", en: "$24$ days" }], a: 2,
      e: { va: "Inversa: $6\\cdot10=4\\cdot x\\Rightarrow x=15$ dies. Amb menys obrers, més dies.", es: "Inversa: $6\\cdot10=4\\cdot x\\Rightarrow x=15$ días. Con menos obreros, más días.", en: "Inverse: $6\\cdot10=4\\cdot x\\Rightarrow x=15$ days. Fewer builders, more days." } },
    { q: { va: "12 gallines mengen 18 kg de pinso en 10 dies. Quant menjaran 20 gallines en 15 dies?", es: "12 gallinas comen 18 kg de pienso en 10 días. ¿Cuánto comerán 20 gallinas en 15 días?", en: "12 hens eat 18 kg of feed in 10 days. How much will 20 hens eat in 15 days?" },
      o: [{ va: "$30$ kg" }, { va: "$45$ kg" }, { va: "$27$ kg" }, { va: "$7{,}2$ kg" }], a: 1,
      e: { va: "Directa i directa: $18\\cdot\\frac{20}{12}\\cdot\\frac{15}{10}=45$ kg.", es: "Directa y directa: $18\\cdot\\frac{20}{12}\\cdot\\frac{15}{10}=45$ kg.", en: "Direct and direct: $18\\cdot\\frac{20}{12}\\cdot\\frac{15}{10}=45$ kg." } },
    { q: { va: "8 obrers treballant 6 h/dia tarden 15 dies. Quants dies tardaran 10 obrers a 9 h/dia?", es: "8 obreros trabajando 6 h/día tardan 15 días. ¿Cuántos días tardarán 10 obreros a 9 h/día?", en: "8 builders working 6 h/day take 15 days. How many days will 10 builders at 9 h/day take?" },
      o: [{ va: "$8$" }, { va: "$28{,}1$" }, { va: "$12$" }, { va: "$10$" }], a: 0,
      e: { va: "Les dues són inverses: $15\\cdot\\frac{8}{10}\\cdot\\frac{6}{9}=8$ dies.", es: "Las dos son inversas: $15\\cdot\\frac{8}{10}\\cdot\\frac{6}{9}=8$ días.", en: "Both are inverse: $15\\cdot\\frac{8}{10}\\cdot\\frac{6}{9}=8$ days." } },
    { q: { va: "Repartim 900 € de manera directament proporcional a 2, 3 i 4. Quant rep la part més gran?", es: "Repartimos 900 € de forma directamente proporcional a 2, 3 y 4. ¿Cuánto recibe la parte mayor?", en: "We share 900 € in direct proportion to 2, 3 and 4. How much is the largest share?" },
      o: [{ va: "$300$ €" }, { va: "$400$ €" }, { va: "$450$ €" }, { va: "$225$ €" }], a: 1,
      e: { va: "$k=\\frac{900}{9}=100$; $4\\cdot100=400$ €.", es: "$k=\\frac{900}{9}=100$; $4\\cdot100=400$ €.", en: "$k=\\frac{900}{9}=100$; $4\\cdot100=400$ €." } },
    { q: { va: "Repartim 300 de manera inversament proporcional a 2 i 3. Quant correspon al 2?", es: "Repartimos 300 de forma inversamente proporcional a 2 y 3. ¿Cuánto corresponde al 2?", en: "We share 300 in inverse proportion to 2 and 3. How much goes to the 2?" },
      o: [{ va: "$120$" }, { va: "$180$" }, { va: "$150$" }, { va: "$100$" }], a: 1,
      e: { va: "$\\frac{1}{2},\\frac{1}{3}\\to\\frac{3}{6},\\frac{2}{6}$: repartim a 3 i 2. $k=60$ i al 2 li toca $3\\cdot60=180$ (rep més qui té el nombre menor).", es: "$\\frac{1}{2},\\frac{1}{3}\\to\\frac{3}{6},\\frac{2}{6}$: repartimos a 3 y 2. $k=60$ y al 2 le toca $3\\cdot60=180$ (recibe más quien tiene el número menor).", en: "$\\frac{1}{2},\\frac{1}{3}\\to\\frac{3}{6},\\frac{2}{6}$: share in proportion to 3 and 2. $k=60$ and the 2 gets $3\\cdot60=180$ (the smaller number gets more)." } },
    { q: { va: "$\\frac{3}{8}$ en forma de percentatge és…", es: "$\\frac{3}{8}$ en forma de porcentaje es…", en: "$\\frac{3}{8}$ as a percentage is…" },
      o: [{ va: "$38\\,\\%$" }, { va: "$3{,}8\\,\\%$" }, { va: "$37{,}5\\,\\%$" }, { va: "$0{,}375\\,\\%$" }], a: 2,
      e: { va: "$3:8=0{,}375$ i $0{,}375\\cdot100=37{,}5\\,\\%$.", es: "$3:8=0{,}375$ y $0{,}375\\cdot100=37{,}5\\,\\%$.", en: "$3:8=0{,}375$ and $0{,}375\\cdot100=37{,}5\\%$." } },
    { q: { va: "El $15\\,\\%$ de 340 és…", es: "El $15\\,\\%$ de 340 es…", en: "$15\\%$ of 340 is…" },
      o: [{ va: "$34$" }, { va: "$51$" }, { va: "$5{,}1$" }, { va: "$22{,}7$" }], a: 1,
      e: { va: "El 10 % és 34 i el 5 %, 17: $34+17=51$. (O bé $340\\cdot0{,}15=51$.)", es: "El 10 % es 34 y el 5 %, 17: $34+17=51$. (O bien $340\\cdot0{,}15=51$.)", en: "10% is 34 and 5% is 17: $34+17=51$. (Or $340\\cdot0{,}15=51$.)" } },
    { q: { va: "Quin percentatge representa 18 respecte de 72?", es: "¿Qué porcentaje representa 18 respecto de 72?", en: "What percentage of 72 is 18?" },
      o: [{ va: "$18\\,\\%$" }, { va: "$25\\,\\%$" }, { va: "$40\\,\\%$" }, { va: "$4\\,\\%$" }], a: 1,
      e: { va: "$\\frac{18}{72}=0{,}25=25\\,\\%$.", es: "$\\frac{18}{72}=0{,}25=25\\,\\%$.", en: "$\\frac{18}{72}=0{,}25=25\\%$." } },
    { q: { va: "El 24 % d'un nombre és 18. El nombre és…", es: "El 24 % de un número es 18. El número es…", en: "24% of a number is 18. The number is…" },
      o: [{ va: "$4{,}32$" }, { va: "$75$" }, { va: "$42$" }, { va: "$133{,}3$" }], a: 1,
      e: { va: "$18:0{,}24=75$. Comprovació: $75\\cdot0{,}24=18$.", es: "$18:0{,}24=75$. Comprobación: $75\\cdot0{,}24=18$.", en: "$18:0{,}24=75$. Check: $75\\cdot0{,}24=18$." } },
    { q: { va: "Quin índex de variació correspon a una rebaixa del 8 %?", es: "¿Qué índice de variación corresponde a una rebaja del 8 %?", en: "Which multiplier corresponds to an 8% reduction?" },
      o: [{ va: "$0{,}08$" }, { va: "$1{,}08$" }, { va: "$0{,}92$" }, { va: "$0{,}8$" }], a: 2,
      e: { va: "$1-0{,}08=0{,}92$: paguem el 92 %.", es: "$1-0{,}08=0{,}92$: pagamos el 92 %.", en: "$1-0{,}08=0{,}92$: we pay 92%." } },
    { q: { va: "Després d'un descompte del 25 % paguem 48 €. El preu inicial era…", es: "Tras un descuento del 25 % pagamos 48 €. El precio inicial era…", en: "After 25% off we pay 48 €. The original price was…" },
      o: [{ va: "$60$ €" }, { va: "$64$ €" }, { va: "$36$ €" }, { va: "$73$ €" }], a: 1,
      e: { va: "$48:0{,}75=64$ €. (60 € és l'error de sumar el 25 % de 48.)", es: "$48:0{,}75=64$ €. (60 € es el error de sumar el 25 % de 48.)", en: "$48:0{,}75=64$ €. (60 € is the mistake of adding 25% of 48.)" } },
    { q: { va: "Un preu puja un 20 % i després baixa un 20 %. Al final…", es: "Un precio sube un 20 % y después baja un 20 %. Al final…", en: "A price rises 20% and then falls 20%. In the end…" },
      o: [{ va: "queda igual", es: "queda igual", en: "it's unchanged" }, { va: "ha baixat un 4 %", es: "ha bajado un 4 %", en: "it's 4% lower" }, { va: "ha pujat un 4 %", es: "ha subido un 4 %", en: "it's 4% higher" }, { va: "ha baixat un 20 %", es: "ha bajado un 20 %", en: "it's 20% lower" }], a: 1,
      e: { va: "$1{,}2\\cdot0{,}8=0{,}96=1-0{,}04$: ha baixat un 4 %.", es: "$1{,}2\\cdot0{,}8=0{,}96=1-0{,}04$: ha bajado un 4 %.", en: "$1{,}2\\cdot0{,}8=0{,}96=1-0{,}04$: it has fallen 4%." } }
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

  var TITLES = { va: "Proporcionalitat i percentatges · FentMates", es: "Proporcionalidad y porcentajes · FentMates", en: "Proportionality and percentages · FentMates" };
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
    wProp(); wR3(); wKind(); document.querySelectorAll(".w-pctc").forEach(wPct); wVar(); M3();
    document.querySelectorAll(".w-drill").forEach(wDrill); wQuiz();
    window.FM26 = { pdec: pdec, dt: dt, dmul: dmul, rndD: rndD, GEN: GEN };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
