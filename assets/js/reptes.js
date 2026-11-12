/* ==========================================================
   REPTES DE LA SETMANA i CURIOSITATS

   Les fórmules s'escriuen en LaTeX entre $...$ (en línia)
   o $$...$$ (centrades). Recorda doblar les barres: \\frac, \\sqrt...

   Reptes: el més recent (per data, sense passar d'avui) surt a
   la pàgina d'inici. Pots programar-ne de futurs: no es veuran
   fins que arribe la data.

   Amb hideSolution: true el repte es mostra sense la solució.
   Quan passe la setmana, esborra eixa línia per a publicar-la.
   ========================================================== */

window.CHALLENGES = [
  {
    date: "2026-11-02",
    level: { va: "3r ESO", es: "3º ESO", en: "3rd ESO" },
    title: { va: "El secret del full A4", es: "El secreto del folio A4", en: "The secret of A4 paper" },
    statement: {
      va: "Si doblegues un full DIN A4 per la meitat, obtens un A5 que té exactament la mateixa forma: els costats dels dos fulls són proporcionals. a) Quina és la raó entre el costat llarg i el curt d'un full DIN? b) Un full A0 té una àrea d'1 m², i en doblegar-lo per la meitat successivament s'obtenen l'A1, l'A2, l'A3 i l'A4. Quant mesuren els costats d'un A4? Expressa'ls primer amb radicals o potències i després en mil·límetres.",
      es: "Si doblas un folio DIN A4 por la mitad, obtienes un A5 que tiene exactamente la misma forma: los lados de las dos hojas son proporcionales. a) ¿Cuál es la razón entre el lado largo y el corto de una hoja DIN? b) Una hoja A0 tiene un área de 1 m², y al doblarla por la mitad sucesivamente se obtienen el A1, el A2, el A3 y el A4. ¿Cuánto miden los lados de un A4? Exprésalos primero con radicales o potencias y después en milímetros.",
      en: "If you fold an A4 sheet in half, you get an A5 sheet with exactly the same shape: the sides of the two sheets are proportional. a) What is the ratio between the long side and the short side of an A-series sheet? b) An A0 sheet has an area of 1 m², and folding it in half again and again gives A1, A2, A3 and A4. How long are the sides of an A4 sheet? Write them first with radicals or powers and then in millimetres."
    },
    solution: {
      va: "a) Si els costats són $a$ (llarg) i $b$ (curt), en doblegar-lo queden $b$ i $\\frac{a}{2}$. Perquè tinguen la mateixa forma: $\\frac{a}{b} = \\frac{b}{a/2}$, és a dir, $a^2 = 2b^2$ i $\\frac{a}{b} = \\mathbf{\\sqrt{2}}$. b) En l'A0, $a = \\sqrt{2}\\,b$ i $a \\cdot b = 1$, així que $\\sqrt{2}\\,b^2 = 1$: $b = \\frac{1}{\\sqrt[4]{2}} = 2^{-1/4} \\approx 0{,}8409$ m i $a = \\sqrt[4]{2} = 2^{1/4} \\approx 1{,}1892$ m. Cada dos doblecs els costats es fan la meitat, i de l'A0 a l'A4 n'hi ha quatre: els costats es divideixen entre 4. L'A4 fa $\\frac{2^{-1/4}}{4} = 2^{-9/4}$ m $\\approx \\mathbf{210}$ mm per $\\frac{2^{1/4}}{4} = 2^{-7/4}$ m $\\approx \\mathbf{297}$ mm. Mesura un full i ho comprovaràs!",
      es: "a) Si los lados son $a$ (largo) y $b$ (corto), al doblarlo quedan $b$ y $\\frac{a}{2}$. Para que tengan la misma forma: $\\frac{a}{b} = \\frac{b}{a/2}$, es decir, $a^2 = 2b^2$ y $\\frac{a}{b} = \\mathbf{\\sqrt{2}}$. b) En el A0, $a = \\sqrt{2}\\,b$ y $a \\cdot b = 1$, así que $\\sqrt{2}\\,b^2 = 1$: $b = \\frac{1}{\\sqrt[4]{2}} = 2^{-1/4} \\approx 0{,}8409$ m y $a = \\sqrt[4]{2} = 2^{1/4} \\approx 1{,}1892$ m. Cada dos dobleces los lados se reducen a la mitad, y del A0 al A4 hay cuatro: los lados se dividen entre 4. El A4 mide $\\frac{2^{-1/4}}{4} = 2^{-9/4}$ m $\\approx \\mathbf{210}$ mm por $\\frac{2^{1/4}}{4} = 2^{-7/4}$ m $\\approx \\mathbf{297}$ mm. ¡Mide un folio y lo comprobarás!",
      en: "a) If the sides are $a$ (long) and $b$ (short), after folding they are $b$ and $\\frac{a}{2}$. For the same shape: $\\frac{a}{b} = \\frac{b}{a/2}$, so $a^2 = 2b^2$ and $\\frac{a}{b} = \\mathbf{\\sqrt{2}}$. b) For A0, $a = \\sqrt{2}\\,b$ and $a \\cdot b = 1$, so $\\sqrt{2}\\,b^2 = 1$: $b = \\frac{1}{\\sqrt[4]{2}} = 2^{-1/4} \\approx 0.8409$ m and $a = \\sqrt[4]{2} = 2^{1/4} \\approx 1.1892$ m. Every two folds halve the sides, and there are four folds from A0 to A4: the sides are divided by 4. A4 measures $\\frac{2^{-1/4}}{4} = 2^{-9/4}$ m $\\approx \\mathbf{210}$ mm by $\\frac{2^{1/4}}{4} = 2^{-7/4}$ m $\\approx \\mathbf{297}$ mm. Measure a sheet and check!"
    }
  },
  {
    date: "2026-10-26",
    level: { va: "3r ESO", es: "3º ESO", en: "3rd ESO" },
    title: { va: "Un cor incansable", es: "Un corazón incansable", en: "A tireless heart" },
    statement: {
      va: "El cor d'una persona batega, de mitjana, unes 70 vegades per minut. Quantes vegades haurà bategat el teu cor quan complisques 80 anys? Fes el càlcul en notació científica i dona el resultat amb dues xifres decimals.",
      es: "El corazón de una persona late, de media, unas 70 veces por minuto. ¿Cuántas veces habrá latido tu corazón cuando cumplas 80 años? Haz el cálculo en notación científica y da el resultado con dos cifras decimales.",
      en: "A person's heart beats, on average, about 70 times a minute. How many times will your heart have beaten by the time you turn 80? Do the calculation in scientific notation and give the result to two decimal places."
    },
    solution: {
      va: "Multipliquem batecs per minut, minuts per hora, hores per dia, dies per any i anys: $70 \\cdot 60 \\cdot 24 \\cdot 365 \\cdot 80 = (7 \\cdot 10) \\cdot (6 \\cdot 10) \\cdot (2{,}4 \\cdot 10) \\cdot (3{,}65 \\cdot 10^2) \\cdot (8 \\cdot 10)$. Agrupem els nombres i les potències de 10: $(7 \\cdot 6 \\cdot 2{,}4 \\cdot 3{,}65 \\cdot 8) \\cdot 10^{1+1+1+2+1} = 2943{,}36 \\cdot 10^6 \\approx \\mathbf{2{,}94 \\cdot 10^9}$ batecs. Quasi tres mil milions!",
      es: "Multiplicamos latidos por minuto, minutos por hora, horas por día, días por año y años: $70 \\cdot 60 \\cdot 24 \\cdot 365 \\cdot 80 = (7 \\cdot 10) \\cdot (6 \\cdot 10) \\cdot (2{,}4 \\cdot 10) \\cdot (3{,}65 \\cdot 10^2) \\cdot (8 \\cdot 10)$. Agrupamos los números y las potencias de 10: $(7 \\cdot 6 \\cdot 2{,}4 \\cdot 3{,}65 \\cdot 8) \\cdot 10^{1+1+1+2+1} = 2943{,}36 \\cdot 10^6 \\approx \\mathbf{2{,}94 \\cdot 10^9}$ latidos. ¡Casi tres mil millones!",
      en: "Multiply beats per minute, minutes per hour, hours per day, days per year and years: $70 \\cdot 60 \\cdot 24 \\cdot 365 \\cdot 80 = (7 \\cdot 10) \\cdot (6 \\cdot 10) \\cdot (2.4 \\cdot 10) \\cdot (3.65 \\cdot 10^2) \\cdot (8 \\cdot 10)$. Group the numbers and the powers of 10: $(7 \\cdot 6 \\cdot 2.4 \\cdot 3.65 \\cdot 8) \\cdot 10^{1+1+1+2+1} = 2943.36 \\cdot 10^6 \\approx \\mathbf{2.94 \\cdot 10^9}$ beats. Almost three billion!"
    }
  },
  {
    date: "2026-10-19",
    level: { va: "3r ESO", es: "3º ESO", en: "3rd ESO" },
    title: { va: "Duel de potències", es: "Duelo de potencias", en: "Battle of powers" },
    statement: {
      va: "Quin nombre és més gran, $2^{300}$ o $3^{200}$? Tots dos tenen prop de cent xifres, així que la calculadora no t'ajudarà: cal trobar una manera de comparar-los.",
      es: "¿Qué número es mayor, $2^{300}$ o $3^{200}$? Ambos tienen cerca de cien cifras, así que la calculadora no te ayudará: hay que encontrar una forma de compararlos.",
      en: "Which number is bigger, $2^{300}$ or $3^{200}$? Both have nearly a hundred digits, so a calculator won't help: you need to find a way to compare them."
    },
    solution: {
      va: "Escrivim les dues potències amb el mateix exponent usant $(a^m)^n = a^{m \\cdot n}$: $2^{300} = (2^3)^{100} = 8^{100}$ i $3^{200} = (3^2)^{100} = 9^{100}$. Amb el mateix exponent, guanya la base més gran: com que $9 > 8$, el més gran és $\\mathbf{3^{200}}$.",
      es: "Escribimos las dos potencias con el mismo exponente usando $(a^m)^n = a^{m \\cdot n}$: $2^{300} = (2^3)^{100} = 8^{100}$ y $3^{200} = (3^2)^{100} = 9^{100}$. Con el mismo exponente, gana la base mayor: como $9 > 8$, el mayor es $\\mathbf{3^{200}}$.",
      en: "Write both powers with the same exponent using $(a^m)^n = a^{m \\cdot n}$: $2^{300} = (2^3)^{100} = 8^{100}$ and $3^{200} = (3^2)^{100} = 9^{100}$. With equal exponents, the bigger base wins: since $9 > 8$, the bigger number is $\\mathbf{3^{200}}$."
    }
  },
  {
    date: "2026-10-12",
    level: { va: "Per a tothom", es: "Para todos", en: "For everyone" },
    title: { va: "Zeros amagats", es: "Ceros escondidos", en: "Hidden zeros" },
    statement: {
      va: "Amb quants zeros acaba el nombre $100! = 100 \\cdot 99 \\cdot 98 \\cdots 2 \\cdot 1$?",
      es: "¿En cuántos ceros termina el número $100! = 100 \\cdot 99 \\cdot 98 \\cdots 2 \\cdot 1$?",
      en: "How many zeros does $100! = 100 \\cdot 99 \\cdot 98 \\cdots 2 \\cdot 1$ end with?"
    },
    solution: {
      va: "Cada zero final ve d'un factor $10 = 2 \\cdot 5$. Hi ha molts més 2 que 5, així que comptem els 5: hi ha $\\lfloor 100/5 \\rfloor = 20$ múltiples de 5 i $\\lfloor 100/25 \\rfloor = 4$ múltiples de 25, que n'aporten un altre. En total, $20 + 4 = \\mathbf{24}$ zeros.",
      es: "Cada cero final viene de un factor $10 = 2 \\cdot 5$. Hay muchos más 2 que 5, así que contamos los 5: hay $\\lfloor 100/5 \\rfloor = 20$ múltiplos de 5 y $\\lfloor 100/25 \\rfloor = 4$ múltiplos de 25, que aportan otro. En total, $20 + 4 = \\mathbf{24}$ ceros.",
      en: "Each trailing zero comes from a factor $10 = 2 \\cdot 5$. There are far more 2s than 5s, so we count the 5s: $\\lfloor 100/5 \\rfloor = 20$ multiples of 5 and $\\lfloor 100/25 \\rfloor = 4$ multiples of 25, which add one more each. In total, $20 + 4 = \\mathbf{24}$ zeros."
    }
  },
  {
    date: "2026-10-05",
    level: { va: "3r ESO", es: "3º ESO", en: "3rd ESO" },
    title: { va: "La suma dels senars", es: "La suma de los impares", en: "Sum of odd numbers" },
    statement: {
      va: "Calcula $1 + 3 + 5 + 7 + \\dots + 99$. Hi ha alguna manera ràpida de fer-ho?",
      es: "Calcula $1 + 3 + 5 + 7 + \\dots + 99$. ¿Hay alguna forma rápida de hacerlo?",
      en: "Work out $1 + 3 + 5 + 7 + \\dots + 99$. Is there a quick way to do it?"
    },
    solution: {
      va: "Observa: $1 = 1^2$, $1+3 = 2^2$, $1+3+5 = 3^2$… La suma dels $n$ primers senars és $n^2$. Fins a 99 hi ha 50 senars, per tant la suma és $50^2 = \\mathbf{2500}$.",
      es: "Observa: $1 = 1^2$, $1+3 = 2^2$, $1+3+5 = 3^2$… La suma de los $n$ primeros impares es $n^2$. Hasta 99 hay 50 impares, por tanto la suma es $50^2 = \\mathbf{2500}$.",
      en: "Notice: $1 = 1^2$, $1+3 = 2^2$, $1+3+5 = 3^2$… The sum of the first $n$ odd numbers is $n^2$. There are 50 odd numbers up to 99, so the sum is $50^2 = \\mathbf{2500}$."
    }
  }
];

window.CURIOSITIES = [
  {
    title: { va: "La paradoxa de l'aniversari", es: "La paradoja del cumpleaños", en: "The birthday paradox" },
    text: {
      va: "En una classe de només 23 persones, la probabilitat que dues facen anys el mateix dia ja supera el 50 %. Amb 30 persones, arriba al 70 %!",
      es: "En una clase de solo 23 personas, la probabilidad de que dos cumplan años el mismo día ya supera el 50 %. ¡Con 30 personas, llega al 70 %!",
      en: "In a class of just 23 people, the chance that two share a birthday is already over 50%. With 30 people, it reaches 70%!"
    }
  },
  {
    title: { va: "El secret que va enfonsar Hípasos", es: "El secreto que hundió a Hípaso", en: "The secret that sank Hippasus" },
    text: {
      va: "Els pitagòrics creien que tot es podia expressar amb fraccions. Segons la llegenda, quan Hípasos de Metapont va demostrar que la diagonal d'un quadrat de costat 1, $\\sqrt{2}$, no és cap fracció, el van llançar al mar per haver revelat el secret. Havia descobert els nombres irracionals!",
      es: "Los pitagóricos creían que todo se podía expresar con fracciones. Según la leyenda, cuando Hípaso de Metaponto demostró que la diagonal de un cuadrado de lado 1, $\\sqrt{2}$, no es ninguna fracción, lo arrojaron al mar por haber revelado el secreto. ¡Había descubierto los números irracionales!",
      en: "The Pythagoreans believed everything could be expressed with fractions. Legend has it that when Hippasus of Metapontum proved that the diagonal of a square of side 1, $\\sqrt{2}$, is not a fraction, he was thrown into the sea for revealing the secret. He had discovered irrational numbers!"
    }
  },
  {
    title: { va: "És $0{,}999\\ldots = 1$?", es: "¿Es $0{,}999\\ldots = 1$?", en: "Is $0.999\\ldots = 1$?" },
    text: {
      va: "Sí! Si $x = 0{,}999\\ldots$, aleshores $10x = 9{,}999\\ldots$. Restant: $9x = 9$, és a dir, $x = 1$.",
      es: "¡Sí! Si $x = 0{,}999\\ldots$, entonces $10x = 9{,}999\\ldots$. Restando: $9x = 9$, es decir, $x = 1$.",
      en: "Yes! If $x = 0.999\\ldots$, then $10x = 9.999\\ldots$. Subtracting: $9x = 9$, so $x = 1$."
    }
  },
  {
    title: { va: "El nombre $e$ i els diners", es: "El número $e$ y el dinero", en: "The number $e$ and money" },
    text: {
      va: "Si un banc et donara un 100 % d'interés anual repartit en infinits trams, 1 € es convertiria en $\\displaystyle\\lim_{n\\to\\infty}\\left(1+\\tfrac{1}{n}\\right)^n = e \\approx 2{,}718$ €.",
      es: "Si un banco te diera un 100 % de interés anual repartido en infinitos tramos, 1 € se convertiría en $\\displaystyle\\lim_{n\\to\\infty}\\left(1+\\tfrac{1}{n}\\right)^n = e \\approx 2{,}718$ €.",
      en: "If a bank paid 100% annual interest compounded infinitely often, €1 would become $\\displaystyle\\lim_{n\\to\\infty}\\left(1+\\tfrac{1}{n}\\right)^n = e \\approx 2.718$ €."
    }
  }
];

/* Reptes guardats per a més endavant (traure'ls del comentari i posar-los dins de CHALLENGES amb la data).

   Per a quan donem percentatges (3r ESO, unitat 3):

  {
    date: "AAAA-MM-DD",
    level: { va: "3r ESO", es: "3º ESO", en: "3rd ESO" },
    title: { va: "Síndries al sol", es: "Sandías al sol", en: "Watermelons in the sun" },
    hideSolution: true,
    statement: {
      va: "Un llaurador té 100 kg de síndries, i el 99 % del seu pes és aigua. Les deixa uns dies al sol i s'assequen una mica: ara l'aigua és el 98 % del pes. Quant pesen ara les síndries? Pensa-ho bé abans de respondre: el resultat sorprén quasi tothom.",
      es: "Un agricultor tiene 100 kg de sandías, y el 99 % de su peso es agua. Las deja unos días al sol y se secan un poco: ahora el agua es el 98 % del peso. ¿Cuánto pesan ahora las sandías? Piénsalo bien antes de responder: el resultado sorprende a casi todo el mundo.",
      en: "A farmer has 100 kg of watermelons, and 99% of their weight is water. He leaves them in the sun for a few days and they dry out a little: now water is 98% of the weight. How much do the watermelons weigh now? Think carefully before answering: the result surprises almost everyone."
    },
    solution: {
      va: "La part que no és aigua no canvia. Al principi és l'1 % de 100 kg, és a dir, $1$ kg. Després, l'aigua és el 98 %, així que eixe quilo és el 2 % del pes nou: $P = 1 : 0{,}02 = \\mathbf{50}$ kg. Han perdut la meitat del pes! Que l'aigua passe del 99 % al 98 % vol dir que la part seca passa de l'1 % al 2 %: la seua proporció es duplica, i per això el total es fa la meitat.",
      es: "La parte que no es agua no cambia. Al principio es el 1 % de 100 kg, es decir, $1$ kg. Después, el agua es el 98 %, así que ese kilo es el 2 % del peso nuevo: $P = 1 : 0{,}02 = \\mathbf{50}$ kg. ¡Han perdido la mitad del peso! Que el agua pase del 99 % al 98 % significa que la parte seca pasa del 1 % al 2 %: su proporción se duplica, y por eso el total se reduce a la mitad.",
      en: "The part that isn't water doesn't change. At first it is 1% of 100 kg, that is, $1$ kg. Afterwards water is 98%, so that kilo is 2% of the new weight: $P = 1 \\div 0.02 = \\mathbf{50}$ kg. They have lost half their weight! Water going from 99% to 98% means the dry part goes from 1% to 2%: its share doubles, so the total halves."
    }
  }

   Per a quan donem identitats notables (3r ESO, unitat 4):

  {
    date: "AAAA-MM-DD",
    level: { va: "3r ESO", es: "3º ESO", en: "3rd ESO" },
    title: { va: "Quadrats gegants", es: "Cuadrados gigantes", en: "Giant squares" },
    hideSolution: true,
    statement: {
      va: "Calcula $2026^2 - 2025^2$ sense calculadora i sense fer cap quadrat. Hi ha una identitat notable que ho resol en una línia.",
      es: "Calcula $2026^2 - 2025^2$ sin calculadora y sin hacer ningún cuadrado. Hay una identidad notable que lo resuelve en una línea.",
      en: "Work out $2026^2 - 2025^2$ without a calculator and without squaring anything. There is a special product that solves it in one line."
    },
    solution: {
      va: "Usem la suma per diferència: $a^2 - b^2 = (a+b)(a-b)$. Aleshores $2026^2 - 2025^2 = (2026 + 2025)(2026 - 2025) = 4051 \\cdot 1 = \\mathbf{4051}$. Fixa't: la diferència entre els quadrats de dos nombres consecutius sempre és la seua suma.",
      es: "Usamos la suma por diferencia: $a^2 - b^2 = (a+b)(a-b)$. Entonces $2026^2 - 2025^2 = (2026 + 2025)(2026 - 2025) = 4051 \\cdot 1 = \\mathbf{4051}$. Fíjate: la diferencia entre los cuadrados de dos números consecutivos siempre es su suma.",
      en: "Use the difference of two squares: $a^2 - b^2 = (a+b)(a-b)$. Then $2026^2 - 2025^2 = (2026 + 2025)(2026 - 2025) = 4051 \\cdot 1 = \\mathbf{4051}$. Notice: the difference between the squares of two consecutive numbers is always their sum."
    }
  }
*/
