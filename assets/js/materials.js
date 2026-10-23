/* ==========================================================
   MATERIALS — ací és on afiges el contingut de cada curs.

   Cada material té:
     type:  "notes" (apunts) | "exercises" (exercicis) | "video" (vídeo)
            | "resource" (recurs/enllaç) | "exam" (examen) | "calc" (guia de calculadora)
     title: text o bé { va: "...", es: "...", en: "..." }
     desc:  (opcional) igual que title
     date:  (opcional) "AAAA-MM-DD", data en què es va penjar
     hidden: (opcional) true -> el material NO es mostra al web (p. ex. solucions)
     url:   ruta al fitxer (p. ex. "materials/3eso/t1-apunts.pdf")
            o enllaç (YouTube, GeoGebra, Drive...). Si està buit -> "Pròximament".

   Als títols pots posar fórmules en LaTeX entre $...$ (doblant les barres: \\frac).
   Els enllaços de Google Drive funcionen directament (compartits com "Qualsevol amb l'enllaç").
   Els vídeos de YouTube s'obrin dins de la pàgina automàticament.
   Una unitat pot portar num: "★" (o un altre símbol) per a seccions especials
   que no compten com a unitat numerada (p. ex. el Resum teòric).
   Un curs amb units: [] apareix com a "Pròximament".
   Per afegir un curs nou: copia un bloc de LEVELS, canvia la clau
   i crea una pàgina .html com 3eso.html amb data-level="clau-nova".
   ========================================================== */

/* Dades de contacte (apareixen a l'inici i al peu de pàgina) */
window.SITE = {
  email: "xavicliment@gmail.com",
  x: "xavier_climent",
  linkedin: "https://www.linkedin.com/in/xavier-climent-balaguer-5679a4155"
};

window.LEVELS = {
  "1eso": {
    color: "#e6b84a",
    symbol: "½",
    stage: "eso",
    name: { va: "1r ESO", es: "1º ESO", en: "1st ESO (Year 7)" },
    desc: {
      va: "Nombres naturals i enters, fraccions, proporcionalitat i geometria plana.",
      es: "Números naturales y enteros, fracciones, proporcionalidad y geometría plana.",
      en: "Whole numbers and integers, fractions, proportionality and plane geometry."
    },
    units: [
      {
        title: { va: "Nombres naturals", es: "Números naturales", en: "Natural numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t1-nombres-naturals.html", date: "2026-10-21" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 71 exercicis graduats per nivells de dificultat", es: "PDF · 71 ejercicios graduados por niveles de dificultad", en: "PDF · 71 exercises graded by difficulty" }, url: "materials/1eso/t1-fitxa-exercicis.pdf", download: true, date: "2026-10-21" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 71 exercicis", es: "PDF · Soluciones de los 71 ejercicios", en: "PDF · Solutions to all 71 exercises" }, url: "materials/1eso/t1-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-21" }
        ]
      },
      {
        title: { va: "Divisibilitat", es: "Divisibilidad", en: "Divisibility" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t2-divisibilitat.html", date: "2026-10-21" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 70 exercicis graduats per nivells de dificultat", es: "PDF · 70 ejercicios graduados por niveles de dificultad", en: "PDF · 70 exercises graded by difficulty" }, url: "materials/1eso/t2-fitxa-exercicis.pdf", download: true, date: "2026-10-21" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 70 exercicis", es: "PDF · Soluciones de los 70 ejercicios", en: "PDF · Solutions to all 70 exercises" }, url: "materials/1eso/t2-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-21" }
        ]
      },
      {
        title: { va: "Nombres enters", es: "Números enteros", en: "Integers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t3-nombres-enters.html", date: "2026-10-22" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis graduats per nivells de dificultat", es: "PDF · 54 ejercicios graduados por niveles de dificultad", en: "PDF · 54 exercises graded by difficulty" }, url: "materials/1eso/t3-fitxa-exercicis.pdf", download: true, date: "2026-10-22" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: "materials/1eso/t3-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-22" }
        ]
      },
      {
        title: { va: "Fraccions", es: "Fracciones", en: "Fractions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t4-fraccions.html", date: "2026-10-22" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 70 exercicis graduats per nivells de dificultat", es: "PDF · 70 ejercicios graduados por niveles de dificultad", en: "PDF · 70 exercises graded by difficulty" }, url: "materials/1eso/t4-fitxa-exercicis.pdf", download: true, date: "2026-10-22" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 70 exercicis", es: "PDF · Soluciones de los 70 ejercicios", en: "PDF · Solutions to all 70 exercises" }, url: "materials/1eso/t4-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-22" }
        ]
      }
    ]
  },

  "2eso": {
    color: "#3b82f6",
    symbol: "%",
    stage: "eso",
    name: { va: "2n ESO", es: "2º ESO", en: "2nd ESO (Year 8)" },
    desc: {
      va: "Fraccions i decimals, percentatges, àlgebra inicial, equacions i geometria.",
      es: "Fracciones y decimales, porcentajes, álgebra inicial, ecuaciones y geometría.",
      en: "Fractions and decimals, percentages, early algebra, equations and geometry."
    },
    units: []
  },

  "3eso": {
    stage: "eso",
    color: "#ff7a50",
    symbol: "x²",
    name: { va: "3r ESO", es: "3º ESO", en: "3rd ESO (Year 9)" },
    desc: {
      va: "Nombres, àlgebra, geometria, funcions i estadística.",
      es: "Números, álgebra, geometría, funciones y estadística.",
      en: "Numbers, algebra, geometry, functions and statistics."
    },
    units: [
      {
        title: { va: "Nombres racionals", es: "Números racionales", en: "Rational numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t1-nombres-racionals.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 63 exercicis graduats per nivells de dificultat", es: "PDF · 63 ejercicios graduados por niveles de dificultad", en: "PDF · 63 exercises graded by difficulty" }, url: "materials/3eso/t1-fitxa-exercicis.pdf", download: true, date: "2026-10-19" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 63 exercicis", es: "PDF · Soluciones de los 63 ejercicios", en: "PDF · Solutions to all 63 exercises" }, url: "materials/3eso/t1-fitxa-solucions.pdf", download: true, date: "2026-10-19" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/3eso/casio-u1-racionals.html" }
        ]
      },
      {
        title: { va: "Nombres reals", es: "Números reales", en: "Real numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t2-nombres-reals.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 46 exercicis graduats per nivells de dificultat", es: "PDF · 46 ejercicios graduados por niveles de dificultad", en: "PDF · 46 exercises graded by difficulty" }, url: "materials/3eso/t2-fitxa-exercicis.pdf", download: true, date: "2026-10-18" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 46 exercicis", es: "PDF · Soluciones de los 46 ejercicios", en: "PDF · Solutions to all 46 exercises" }, url: "materials/3eso/t2-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-18" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/3eso/casio-u2-reals.html" },
          { type: "notes", title: { va: "Presentació-resum per a l'examen (interactiva)", es: "Presentación-resumen para el examen (interactiva)", en: "Exam summary slides (interactive)" }, desc: { va: "15 diapositives amb mapa conceptual, errors típics i autoavaluació", es: "15 diapositivas con mapa conceptual, errores típicos y autoevaluación", en: "15 slides with a concept map, common mistakes and a self-check" }, url: "materials/3eso/t2-resum-diapositives.html", date: "2026-10-19" }
        ]
      },
      {
        title: { va: "Proporcionalitat i percentatges", es: "Proporcionalidad y porcentajes", en: "Proportionality and percentages" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t3-proporcionalitat-percentatges.html", date: "2026-10-20" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 79 exercicis graduats per nivells de dificultat", es: "PDF · 79 ejercicios graduados por niveles de dificultad", en: "PDF · 79 exercises graded by difficulty" }, url: "materials/3eso/t3-fitxa-exercicis.pdf", download: true, date: "2026-10-20" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 79 exercicis", es: "PDF · Soluciones de los 79 ejercicios", en: "PDF · Solutions to all 79 exercises" }, url: "materials/3eso/t3-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-20" }
        ]
      },
      {
        title: { va: "Polinomis", es: "Polinomios", en: "Polynomials" },
        items: [
          { type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "" },
          { type: "resource", date: "2026-10-15", title: { va: "GeoGebra: identitats notables $(a+b)^2$", es: "GeoGebra: identidades notables $(a+b)^2$", en: "GeoGebra: special products $(a+b)^2$" }, url: "https://www.geogebra.org" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/3eso/casio-u4-polinomis.html" }
        ]
      },
      {
        title: { va: "Equacions i sistemes", es: "Ecuaciones y sistemas", en: "Equations and systems" },
        items: [
          { type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "" },
          { type: "exercises", title: { va: "Problemes amb equacions", es: "Problemas con ecuaciones", en: "Equation word problems" }, url: "" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/3eso/casio-u5-equacions.html" }
        ]
      }
    ]
  },

  "4eso-a": {
    color: "#a78bfa",
    symbol: "Δ",
    stage: "eso",
    name: { va: "4t ESO Matemàtiques A", es: "4º ESO Matemáticas A", en: "4th ESO Maths A" },
    desc: {
      va: "Matemàtiques aplicades: nombres, àlgebra, funcions, estadística i probabilitat.",
      es: "Matemáticas aplicadas: números, álgebra, funciones, estadística y probabilidad.",
      en: "Applied maths: numbers, algebra, functions, statistics and probability."
    },
    units: []
  },

  "4eso-b": {
    color: "#6d28d9",
    symbol: "√",
    stage: "eso",
    name: { va: "4t ESO Matemàtiques B", es: "4º ESO Matemáticas B", en: "4th ESO Maths B" },
    desc: {
      va: "Radicals i logaritmes, àlgebra, trigonometria, geometria analítica i funcions.",
      es: "Radicales y logaritmos, álgebra, trigonometría, geometría analítica y funciones.",
      en: "Radicals and logarithms, algebra, trigonometry, coordinate geometry and functions."
    },
    units: []
  },

  "1batx-mi": {
    color: "#9b1c1c",
    symbol: "sin",
    stage: "batx",
    name: { va: "1r Batxillerat MI", es: "1º Bachillerato MI", en: "1st Baccalaureate Maths I" },
    desc: {
      va: "Nombres reals i complexos, trigonometria, vectors, geometria analítica i anàlisi.",
      es: "Números reales y complejos, trigonometría, vectores, geometría analítica y análisis.",
      en: "Real and complex numbers, trigonometry, vectors, coordinate geometry and calculus."
    },
    units: []
  },

  "1batx-ccss": {
    color: "#ef6b6b",
    symbol: "σ",
    stage: "batx",
    name: { va: "1r Batxillerat CCSS", es: "1º Bachillerato CCSS", en: "1st Baccalaureate (Social Sciences)" },
    desc: {
      va: "Matemàtica financera, àlgebra, funcions, estadística i probabilitat.",
      es: "Matemática financiera, álgebra, funciones, estadística y probabilidad.",
      en: "Financial maths, algebra, functions, statistics and probability."
    },
    units: []
  },

  "2batx-mii": {
    color: "#1e6b47",
    symbol: "∂",
    stage: "batx",
    name: { va: "2n Batxillerat MII", es: "2º Bachillerato MII", en: "2nd Baccalaureate Maths II" },
    desc: {
      va: "Matrius, geometria a l'espai, anàlisi i probabilitat. Preparació de la PAU.",
      es: "Matrices, geometría en el espacio, análisis y probabilidad. Preparación de la PAU.",
      en: "Matrices, 3D geometry, calculus and probability. University entrance exam prep."
    },
    units: [
      {
        num: "★",
        title: { va: "Resum Teòric", es: "Resumen Teórico", en: "Theory Summary" },
        items: [
          { type: "notes", title: { va: "Formulari-resum teòric de tot el curs (interactiu)", es: "Formulario-resumen teórico de todo el curso (interactivo)", en: "Whole-course theory summary and formula sheet (interactive)" }, desc: { va: "Àlgebra, geometria, anàlisi i probabilitat", es: "Álgebra, geometría, análisis y probabilidad", en: "Algebra, geometry, calculus and probability" }, url: "materials/2batx-mii/resum-teoric.html", date: "2026-10-23" }
        ]
      },
      {
        title: { va: "Matrius i determinants", es: "Matrices y determinantes", en: "Matrices and determinants" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t1-matrius-determinants.html", date: "2026-10-23" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "59 exercicis resolts de la PAU valenciana (1999–2026)", es: "59 ejercicios resueltos de la PAU valenciana (1999–2026)", en: "59 solved past Valencian PAU exercises (1999–2026)" }, url: "materials/2batx-mii/pau-u1-matrius.html", date: "2026-10-23" }
        ]
      },
      {
        title: { va: "Sistemes d'equacions lineals", es: "Sistemas de ecuaciones lineales", en: "Systems of linear equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t2-sistemes-equacions.html", date: "2026-10-23" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "64 exercicis resolts de la PAU valenciana (1997–2026)", es: "64 ejercicios resueltos de la PAU valenciana (1997–2026)", en: "64 solved past Valencian PAU exercises (1997–2026)" }, url: "materials/2batx-mii/pau-u2-sistemes.html", date: "2026-10-23" }
        ]
      }
    ]
  },

  "2batx-ccss": {
    stage: "batx",
    color: "#2bb3a3",
    symbol: "∫",
    pau: true,
    name: { va: "2n Batxillerat CCSS", es: "2º Bachillerato CCSS", en: "2nd Baccalaureate (Social Sciences)" },
    desc: {
      va: "Matrius, programació lineal, anàlisi i probabilitat. Preparació de la PAU.",
      es: "Matrices, programación lineal, análisis y probabilidad. Preparación de la PAU.",
      en: "Matrices, linear programming, calculus and probability. University entrance exam prep."
    },
    units: [
      {
        num: "★",
        title: { va: "Resum Teòric", es: "Resumen Teórico", en: "Theory Summary" },
        items: [
          { type: "notes", title: { va: "Formulari-resum teòric de tot el curs (interactiu)", es: "Formulario-resumen teórico de todo el curso (interactivo)", en: "Whole-course theory summary and formula sheet (interactive)" }, desc: { va: "Àlgebra, programació lineal, anàlisi i probabilitat", es: "Álgebra, programación lineal, análisis y probabilidad", en: "Algebra, linear programming, calculus and probability" }, url: "materials/2batx-ccss/resum-teoric.html", date: "2026-10-18" }
        ]
      },
      {
        title: { va: "Matrius i determinants", es: "Matrices y determinantes", en: "Matrices and determinants" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t1-matrius-determinants.html", date: "2026-10-18" },
          { type: "video", title: { va: "Rang d'una matriu per determinants", es: "Rango de una matriz por determinantes", en: "Rank of a matrix using determinants" }, url: "https://youtu.be/yaOUjHAnH3M", date: "2026-10-23" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "33 exercicis de la PAU valenciana (1994–2026)", es: "33 ejercicios de la PAU valenciana (1994–2026)", en: "33 past Valencian PAU exercises (1994–2026)" }, url: "materials/2batx-ccss/pau-u1-matrius.html" },
          { type: "exam", title: { va: "Model d'examen tipus PAU", es: "Modelo de examen tipo PAU", en: "PAU-style mock exam" }, desc: { va: "4 problemes amb solucions i criteris de correcció", es: "4 problemas con soluciones y criterios de corrección", en: "4 problems with solutions and marking criteria" }, url: "materials/2batx-ccss/examen-u1-matrius-model1.html", date: "2026-10-21" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u1-matrius.html" }
        ]
      },
      {
        title: { va: "Sistemes d'equacions lineals", es: "Sistemas de ecuaciones lineales", en: "Systems of linear equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t2-sistemes-equacions.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "68 exercicis de la PAU valenciana (1994–2026)", es: "68 ejercicios de la PAU valenciana (1994–2026)", en: "68 past Valencian PAU exercises (1994–2026)" }, url: "materials/2batx-ccss/pau-u2-sistemes.html" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u2-sistemes.html" }
        ]
      },
      {
        title: { va: "Programació lineal", es: "Programación lineal", en: "Linear programming" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t3-programacio-lineal.html", date: "2026-10-19" },
          { type: "video", title: { va: "Resolució gràfica pas a pas", es: "Resolución gráfica paso a paso", en: "Graphical method step by step" }, url: "" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "83 exercicis resolts de la PAU valenciana (1994–2026)", es: "83 ejercicios resueltos de la PAU valenciana (1994–2026)", en: "83 solved past Valencian PAU exercises (1994–2026)" }, url: "materials/2batx-ccss/pau-u3-programacio-lineal.html" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u3-programacio-lineal.html" }
        ]
      },
      {
        title: { va: "Derivades i aplicacions", es: "Derivadas y aplicaciones", en: "Derivatives and applications" },
        items: [
          { type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "" }
        ]
      },
      {
        title: { va: "Probabilitat", es: "Probabilidad", en: "Probability" },
        items: [
          { type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "" },
          { type: "exam", title: { va: "Exàmens PAU anteriors", es: "Exámenes PAU anteriores", en: "Past entrance exams" }, url: "" }
        ]
      }
    ]
  }
};
