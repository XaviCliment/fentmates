/* ==========================================================
   REPTES DE LA SETMANA i CURIOSITATS

   Les fórmules s'escriuen en LaTeX entre $...$ (en línia)
   o $$...$$ (centrades). Recorda doblar les barres: \\frac, \\sqrt...

   Reptes: el més recent (per data, sense passar d'avui) surt a
   la pàgina d'inici. Pots programar-ne de futurs: no es veuran
   fins que arribe la data.
   ========================================================== */

window.CHALLENGES = [
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
