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
   Cursos amb cards: true -> les unitats es mostren com a targetes. Cada unitat porta
   ill (dibuix: vegeu assets/js/illustrations.js, p. ex. naturals, fraccions, matrius, pl…)
   i block (color: all, ari, alg, pl, geo, an, pr), com als blocs del resum teòric.
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
    cards: true,
    name: { va: "1r ESO", es: "1º ESO", en: "1st ESO (Year 7)" },
    desc: {
      va: "Nombres naturals i enters, fraccions, proporcionalitat i geometria plana.",
      es: "Números naturales y enteros, fracciones, proporcionalidad y geometría plana.",
      en: "Whole numbers and integers, fractions, proportionality and plane geometry."
    },
    units: [
      {
        ill: "naturals", block: "ari",
        title: { va: "Nombres naturals", es: "Números naturales", en: "Natural numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t1-nombres-naturals.html", date: "2026-10-21" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 71 exercicis graduats per nivells de dificultat", es: "PDF · 71 ejercicios graduados por niveles de dificultad", en: "PDF · 71 exercises graded by difficulty" }, url: "materials/1eso/t1-fitxa-exercicis.pdf", download: true, date: "2026-10-21" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 71 exercicis", es: "PDF · Soluciones de los 71 ejercicios", en: "PDF · Solutions to all 71 exercises" }, url: "materials/1eso/t1-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-21" }
        ]
      },
      {
        ill: "divisibilitat", block: "ari",
        title: { va: "Divisibilitat", es: "Divisibilidad", en: "Divisibility" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t2-divisibilitat.html", date: "2026-10-21" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 70 exercicis graduats per nivells de dificultat", es: "PDF · 70 ejercicios graduados por niveles de dificultad", en: "PDF · 70 exercises graded by difficulty" }, url: "materials/1eso/t2-fitxa-exercicis.pdf", download: true, date: "2026-10-21" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 70 exercicis", es: "PDF · Soluciones de los 70 ejercicios", en: "PDF · Solutions to all 70 exercises" }, url: "materials/1eso/t2-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-21" }
        ]
      },
      {
        ill: "enters", block: "ari",
        title: { va: "Nombres enters", es: "Números enteros", en: "Integers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t3-nombres-enters.html", date: "2026-10-22" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis graduats per nivells de dificultat", es: "PDF · 54 ejercicios graduados por niveles de dificultad", en: "PDF · 54 exercises graded by difficulty" }, url: "materials/1eso/t3-fitxa-exercicis.pdf", download: true, date: "2026-10-22" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: "materials/1eso/t3-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-22" }
        ]
      },
      {
        ill: "fraccions", block: "ari",
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
    cards: true,
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
    cards: true,
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
        ill: "racionals", block: "ari",
        title: { va: "Nombres racionals", es: "Números racionales", en: "Rational numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t1-nombres-racionals.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 63 exercicis graduats per nivells de dificultat", es: "PDF · 63 ejercicios graduados por niveles de dificultad", en: "PDF · 63 exercises graded by difficulty" }, url: "materials/3eso/t1-fitxa-exercicis.pdf", download: true, date: "2026-10-19" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 63 exercicis", es: "PDF · Soluciones de los 63 ejercicios", en: "PDF · Solutions to all 63 exercises" }, url: "materials/3eso/t1-fitxa-solucions.pdf", download: true, date: "2026-10-19" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/3eso/casio-u1-racionals.html" }
        ]
      },
      {
        ill: "reals", block: "ari",
        title: { va: "Nombres reals", es: "Números reales", en: "Real numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t2-nombres-reals.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 46 exercicis graduats per nivells de dificultat", es: "PDF · 46 ejercicios graduados por niveles de dificultad", en: "PDF · 46 exercises graded by difficulty" }, url: "materials/3eso/t2-fitxa-exercicis.pdf", download: true, date: "2026-10-18" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 46 exercicis", es: "PDF · Soluciones de los 46 ejercicios", en: "PDF · Solutions to all 46 exercises" }, url: "materials/3eso/t2-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-18" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/3eso/casio-u2-reals.html" },
          { type: "notes", title: { va: "Presentació-resum per a l'examen (interactiva)", es: "Presentación-resumen para el examen (interactiva)", en: "Exam summary slides (interactive)" }, desc: { va: "15 diapositives amb mapa conceptual, errors típics i autoavaluació", es: "15 diapositivas con mapa conceptual, errores típicos y autoevaluación", en: "15 slides with a concept map, common mistakes and a self-check" }, url: "materials/3eso/t2-resum-diapositives.html", date: "2026-10-19" },
          { type: "exam", title: { va: "Model d'examen", es: "Modelo de examen", en: "Mock exam" }, desc: { va: "PDF · 9 preguntes de tota la unitat (10 punts)", es: "PDF · 9 preguntas de toda la unidad (10 puntos)", en: "PDF · 9 questions covering the whole unit (10 points)" }, url: "materials/3eso/t2-model-examen.pdf", download: true, hidden: true, date: "2026-10-26" },
          { type: "exam", title: { va: "Solucions del model d'examen", es: "Soluciones del modelo de examen", en: "Mock exam solutions" }, desc: { va: "PDF · Solucions i criteris de correcció", es: "PDF · Soluciones y criterios de corrección", en: "PDF · Solutions and marking criteria" }, url: "materials/3eso/t2-model-examen-solucions.pdf", download: true, hidden: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Fitxa de repàs per a l'examen", es: "Ficha de repaso para el examen", en: "Exam review worksheet" }, desc: { va: "PDF · 13 exercicis, un de cada contingut de la unitat", es: "PDF · 13 ejercicios, uno de cada contenido de la unidad", en: "PDF · 13 exercises, one for each topic of the unit" }, url: "materials/3eso/t2-fitxa-repas.pdf", download: true, hidden: true, date: "2026-10-29" },
          { type: "exercises", title: { va: "Solucions de la fitxa de repàs", es: "Soluciones de la ficha de repaso", en: "Review worksheet solutions" }, desc: { va: "PDF · Solucions pas a pas per a autocorregir-te", es: "PDF · Soluciones paso a paso para autocorregirte", en: "PDF · Step-by-step solutions to self-check" }, url: "materials/3eso/t2-fitxa-repas-solucions.pdf", download: true, hidden: true, date: "2026-10-29" }
        ]
      },
      {
        ill: "proporcionalitat", block: "ari",
        title: { va: "Proporcionalitat i percentatges", es: "Proporcionalidad y porcentajes", en: "Proportionality and percentages" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t3-proporcionalitat-percentatges.html", date: "2026-10-20" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 79 exercicis graduats per nivells de dificultat", es: "PDF · 79 ejercicios graduados por niveles de dificultad", en: "PDF · 79 exercises graded by difficulty" }, url: "materials/3eso/t3-fitxa-exercicis.pdf", download: true, date: "2026-10-20" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 79 exercicis", es: "PDF · Soluciones de los 79 ejercicios", en: "PDF · Solutions to all 79 exercises" }, url: "materials/3eso/t3-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-20" }
        ]
      },
      {
        ill: "polinomis", block: "alg",
        title: { va: "Polinomis", es: "Polinomios", en: "Polynomials" },
        items: [
          { type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "" },
          { type: "resource", date: "2026-10-15", title: { va: "GeoGebra: identitats notables $(a+b)^2$", es: "GeoGebra: identidades notables $(a+b)^2$", en: "GeoGebra: special products $(a+b)^2$" }, url: "https://www.geogebra.org" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/3eso/casio-u4-polinomis.html" }
        ]
      },
      {
        ill: "equacions", block: "alg",
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
    cards: true,
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
    cards: true,
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
    cards: true,
    name: { va: "1r Batxillerat MI", es: "1º Bachillerato MI", en: "1st Baccalaureate Maths I" },
    desc: {
      va: "Nombres reals i complexos, trigonometria, vectors, geometria analítica i anàlisi.",
      es: "Números reales y complejos, trigonometría, vectores, geometría analítica y análisis.",
      en: "Real and complex numbers, trigonometry, vectors, coordinate geometry and calculus."
    },
    units: [
      {
        // num: la unitat 5 del departament (les unitats anteriors encara no estan penjades)
        num: "5",
        ill: "geometria", block: "geo",
        title: { va: "Geometria analítica en el pla", es: "Geometría analítica en el plano", en: "Coordinate geometry in the plane" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, desc: { va: "Vectors, producte escalar, equacions de la recta, posicions relatives, angles i distàncies", es: "Vectores, producto escalar, ecuaciones de la recta, posiciones relativas, ángulos y distancias", en: "Vectors, dot product, equations of a line, relative positions, angles and distances" }, url: "materials/1batx-mi/t5-geometria-pla.html", date: "2026-10-29" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 61 exercicis, dels vectors als problemes mètrics", es: "PDF · 61 ejercicios, de los vectores a los problemas métricos", en: "PDF · 61 exercises, from vectors to metric problems" }, url: "materials/1batx-mi/t5-fitxa-exercicis.pdf", download: true, date: "2026-10-29" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 61 exercicis", es: "PDF · Soluciones de los 61 ejercicios", en: "PDF · Solutions to all 61 exercises" }, url: "materials/1batx-mi/t5-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-29" }
        ]
      }
    ]
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
    pau: true,
    cards: true,
    name: { va: "2n Batxillerat MII", es: "2º Bachillerato MII", en: "2nd Baccalaureate Maths II" },
    desc: {
      va: "Matrius, geometria a l'espai, anàlisi i probabilitat. Preparació de la PAU.",
      es: "Matrices, geometría en el espacio, análisis y probabilidad. Preparación de la PAU.",
      en: "Matrices, 3D geometry, calculus and probability. University entrance exam prep."
    },
    units: [
      {
        num: "★",
        ill: "resum", block: "all",
        title: { va: "Resum Teòric", es: "Resumen Teórico", en: "Theory Summary" },
        items: [
          { type: "notes", title: { va: "Formulari-resum teòric de tot el curs (interactiu)", es: "Formulario-resumen teórico de todo el curso (interactivo)", en: "Whole-course theory summary and formula sheet (interactive)" }, desc: { va: "Àlgebra, geometria, anàlisi i probabilitat", es: "Álgebra, geometría, análisis y probabilidad", en: "Algebra, geometry, calculus and probability" }, url: "materials/2batx-mii/resum-teoric.html", date: "2026-10-23" }
        ]
      },
      {
        ill: "matrius", block: "alg",
        title: { va: "Matrius i determinants", es: "Matrices y determinantes", en: "Matrices and determinants" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t1-matrius-determinants.html", date: "2026-10-23" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "59 exercicis resolts de la PAU valenciana (1999–2026)", es: "59 ejercicios resueltos de la PAU valenciana (1999–2026)", en: "59 solved past Valencian PAU exercises (1999–2026)" }, url: "materials/2batx-mii/pau-u1-matrius.html", date: "2026-10-23" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 79 exercicis, 34 de la PAU de 16 comunitats autònomes", es: "PDF · 79 ejercicios, 34 de la PAU de 16 comunidades autónomas", en: "PDF · 79 exercises, 34 from the PAU of 16 Spanish regions" }, url: "materials/2batx-mii/t1-fitxa-exercicis.pdf", download: true, date: "2026-10-29" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 79 exercicis", es: "PDF · Soluciones de los 79 ejercicios", en: "PDF · Solutions to all 79 exercises" }, url: "materials/2batx-mii/t1-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-29" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-mii/casio-u1-matrius.html", date: "2026-10-23" }
        ]
      },
      {
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions lineals", es: "Sistemas de ecuaciones lineales", en: "Systems of linear equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t2-sistemes-equacions.html", date: "2026-10-23" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "64 exercicis resolts de la PAU valenciana (1997–2026)", es: "64 ejercicios resueltos de la PAU valenciana (1997–2026)", en: "64 solved past Valencian PAU exercises (1997–2026)" }, url: "materials/2batx-mii/pau-u2-sistemes.html", date: "2026-10-23" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-mii/casio-u2-sistemes.html", date: "2026-10-23" }
        ]
      }
    ]
  },

  "2batx-ccss": {
    stage: "batx",
    cards: true,
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
        ill: "resum", block: "all",
        title: { va: "Resum Teòric", es: "Resumen Teórico", en: "Theory Summary" },
        items: [
          { type: "notes", title: { va: "Formulari-resum teòric de tot el curs (interactiu)", es: "Formulario-resumen teórico de todo el curso (interactivo)", en: "Whole-course theory summary and formula sheet (interactive)" }, desc: { va: "Àlgebra, programació lineal, anàlisi i probabilitat", es: "Álgebra, programación lineal, análisis y probabilidad", en: "Algebra, linear programming, calculus and probability" }, url: "materials/2batx-ccss/resum-teoric.html", date: "2026-10-18" }
        ]
      },
      {
        ill: "matrius", block: "alg",
        title: { va: "Matrius i determinants", es: "Matrices y determinantes", en: "Matrices and determinants" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t1-matrius-determinants.html", date: "2026-10-18" },
          { type: "video", title: { va: "Rang d'una matriu per determinants", es: "Rango de una matriz por determinantes", en: "Rank of a matrix using determinants" }, url: "https://youtu.be/yaOUjHAnH3M", date: "2026-10-23" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "33 exercicis de la PAU valenciana (1994–2026)", es: "33 ejercicios de la PAU valenciana (1994–2026)", en: "33 past Valencian PAU exercises (1994–2026)" }, url: "materials/2batx-ccss/pau-u1-matrius.html" },
          { type: "exam", title: { va: "Model d'examen tipus PAU", es: "Modelo de examen tipo PAU", en: "PAU-style mock exam" }, desc: { va: "4 problemes amb solucions i criteris de correcció", es: "4 problemas con soluciones y criterios de corrección", en: "4 problems with solutions and marking criteria" }, url: "materials/2batx-ccss/examen-u1-matrius-model1.html", date: "2026-10-21" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 50 exercicis, de les operacions a les equacions matricials", es: "PDF · 50 ejercicios, de las operaciones a las ecuaciones matriciales", en: "PDF · 50 exercises, from operations to matrix equations" }, url: "materials/2batx-ccss/t1-fitxa-exercicis.pdf", download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 50 exercicis", es: "PDF · Soluciones de los 50 ejercicios", en: "PDF · Solutions to all 50 exercises" }, url: "materials/2batx-ccss/t1-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-27" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u1-matrius.html" }
        ]
      },
      {
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions lineals", es: "Sistemas de ecuaciones lineales", en: "Systems of linear equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t2-sistemes-equacions.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "68 exercicis de la PAU valenciana (1994–2026)", es: "68 ejercicios de la PAU valenciana (1994–2026)", en: "68 past Valencian PAU exercises (1994–2026)" }, url: "materials/2batx-ccss/pau-u2-sistemes.html" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 60 exercicis, 42 de la PAU d'altres comunitats", es: "PDF · 60 ejercicios, 42 de la PAU de otras comunidades", en: "PDF · 60 exercises, 42 from other regions' PAU exams" }, url: "materials/2batx-ccss/t2-fitxa-exercicis.pdf", download: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 60 exercicis", es: "PDF · Soluciones de los 60 ejercicios", en: "PDF · Solutions to all 60 exercises" }, url: "materials/2batx-ccss/t2-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-26" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u2-sistemes.html" }
        ]
      },
      {
        ill: "pl", block: "pl",
        title: { va: "Programació lineal", es: "Programación lineal", en: "Linear programming" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t3-programacio-lineal.html", date: "2026-10-19" },
          { type: "video", title: { va: "Resolució gràfica pas a pas", es: "Resolución gráfica paso a paso", en: "Graphical method step by step" }, url: "" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "83 exercicis resolts de la PAU valenciana (1994–2026)", es: "83 ejercicios resueltos de la PAU valenciana (1994–2026)", en: "83 solved past Valencian PAU exercises (1994–2026)" }, url: "materials/2batx-ccss/pau-u3-programacio-lineal.html" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 29 exercicis, 5 de la PAU valenciana", es: "PDF · 29 ejercicios, 5 de la PAU valenciana", en: "PDF · 29 exercises, 5 from the Valencian PAU" }, url: "materials/2batx-ccss/t3-fitxa-exercicis.pdf", download: true, date: "2026-10-25" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 29 exercicis", es: "PDF · Soluciones de los 29 ejercicios", en: "PDF · Solutions to all 29 exercises" }, url: "materials/2batx-ccss/t3-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-25" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u3-programacio-lineal.html" }
        ]
      },
      {
        ill: "limits", block: "an",
        title: { va: "Límits i continuïtat", es: "Límites y continuidad", en: "Limits and continuity" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t4-limits-continuitat.html", date: "2026-10-24" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 55 exercicis, 22 de la PAU d'altres comunitats", es: "PDF · 55 ejercicios, 22 de la PAU de otras comunidades", en: "PDF · 55 exercises, 22 from other regions' PAU exams" }, url: "materials/2batx-ccss/t4-fitxa-exercicis.pdf", download: true, date: "2026-10-24" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 55 exercicis", es: "PDF · Soluciones de los 55 ejercicios", en: "PDF · Solutions to all 55 exercises" }, url: "materials/2batx-ccss/t4-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-24" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "26 exercicis resolts de la PAU valenciana (2002–2026)", es: "26 ejercicios resueltos de la PAU valenciana (2002–2026)", en: "26 solved past Valencian PAU exercises (2002–2026)" }, url: "materials/2batx-ccss/pau-u4-limits-continuitat.html", date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u4-limits-continuitat.html", date: "2026-10-28" }
        ]
      },
      {
        ill: "derivades", block: "an",
        title: { va: "Càlcul de derivades. Derivabilitat d'una funció", es: "Cálculo de derivadas. Derivabilidad de una función", en: "Computing derivatives. Differentiability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t5-derivades.html", date: "2026-10-25" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 48 exercicis, 28 enunciats de la PAU d'altres comunitats", es: "PDF · 48 ejercicios, 28 enunciados de la PAU de otras comunidades", en: "PDF · 48 exercises, 28 items from other regions' PAU exams" }, url: "materials/2batx-ccss/t5-fitxa-exercicis.pdf", download: true, date: "2026-10-25" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 48 exercicis", es: "PDF · Soluciones de los 48 ejercicios", en: "PDF · Solutions to all 48 exercises" }, url: "materials/2batx-ccss/t5-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-25" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "5 exercicis resolts de la PAU valenciana (2001–2026)", es: "5 ejercicios resueltos de la PAU valenciana (2001–2026)", en: "5 solved past Valencian PAU exercises (2001–2026)" }, url: "materials/2batx-ccss/pau-u5-derivades.html", date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u5-derivades.html", date: "2026-10-28" }
        ]
      },
      {
        ill: "aplicacions", block: "an",
        title: { va: "Aplicacions de la derivada", es: "Aplicaciones de la derivada", en: "Applications of the derivative" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t6-aplicacions-derivada.html", date: "2026-10-26" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis, 42 de la PAU d'altres comunitats", es: "PDF · 54 ejercicios, 42 de la PAU de otras comunidades", en: "PDF · 54 exercises, 42 from other regions' PAU exams" }, url: "materials/2batx-ccss/t6-fitxa-exercicis.pdf", download: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: "materials/2batx-ccss/t6-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "54 exercicis resolts de la PAU valenciana (1997–2026)", es: "54 ejercicios resueltos de la PAU valenciana (1997–2026)", en: "54 solved past Valencian PAU exercises (1997–2026)" }, url: "materials/2batx-ccss/pau-u6-aplicacions-derivada.html", date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u6-aplicacions-derivada.html", date: "2026-10-28" }
        ]
      },
      {
        ill: "grafiques", block: "an",
        title: { va: "Representació gràfica de funcions", es: "Representación gráfica de funciones", en: "Graphing functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t7-representacio-funcions.html", date: "2026-10-26" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 38 exercicis amb gràfiques a les solucions", es: "PDF · 38 ejercicios con gráficas en las soluciones", en: "PDF · 38 exercises with graphs in the solutions" }, url: "materials/2batx-ccss/t7-fitxa-exercicis.pdf", download: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 38 exercicis", es: "PDF · Soluciones de los 38 ejercicios", en: "PDF · Solutions to all 38 exercises" }, url: "materials/2batx-ccss/t7-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "34 exercicis resolts de la PAU valenciana (2006–2026)", es: "34 ejercicios resueltos de la PAU valenciana (2006–2026)", en: "34 solved past Valencian PAU exercises (2006–2026)" }, url: "materials/2batx-ccss/pau-u7-representacio-funcions.html", date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u7-representacio-funcions.html", date: "2026-10-28" }
        ]
      },
      {
        ill: "integrals", block: "an",
        title: { va: "Integrals", es: "Integrales", en: "Integrals" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t8-integrals.html", date: "2026-10-27" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 36 exercicis amb gràfiques a les solucions", es: "PDF · 36 ejercicios con gráficas en las soluciones", en: "PDF · 36 exercises with graphs in the solutions" }, url: "materials/2batx-ccss/t8-fitxa-exercicis.pdf", download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 36 exercicis", es: "PDF · Soluciones de los 36 ejercicios", en: "PDF · Solutions to all 36 exercises" }, url: "materials/2batx-ccss/t8-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "26 exercicis resolts de la PAU valenciana (2001–2026)", es: "26 ejercicios resueltos de la PAU valenciana (2001–2026)", en: "26 solved past Valencian PAU exercises (2001–2026)" }, url: "materials/2batx-ccss/pau-u8-integrals.html", date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u8-integrals.html", date: "2026-10-28" }
        ]
      },
      {
        ill: "probabilitat", block: "pr",
        title: { va: "Probabilitat", es: "Probabilidad", en: "Probability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t9-probabilitat.html", date: "2026-10-27" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 76 exercicis, 50 de la PAU d'altres comunitats", es: "PDF · 76 ejercicios, 50 de la PAU de otras comunidades", en: "PDF · 76 exercises, 50 from other regions' PAU exams" }, url: "materials/2batx-ccss/t9-fitxa-exercicis.pdf", download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 76 exercicis", es: "PDF · Soluciones de los 76 ejercicios", en: "PDF · Solutions to all 76 exercises" }, url: "materials/2batx-ccss/t9-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "100 exercicis resolts de la PAU valenciana (2000–2026)", es: "100 ejercicios resueltos de la PAU valenciana (2000–2026)", en: "100 solved past Valencian PAU exercises (2000–2026)" }, url: "materials/2batx-ccss/pau-u9-probabilitat.html", date: "2026-10-27" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u9-probabilitat.html", date: "2026-10-28" }
        ]
      },
      {
        ill: "normal", block: "pr",
        title: { va: "Distribució binomial i normal", es: "Distribución binomial y normal", en: "Binomial and normal distributions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t10-binomial-normal.html", date: "2026-10-27" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 53 exercicis, 37 de la PAU d'altres comunitats", es: "PDF · 53 ejercicios, 37 de la PAU de otras comunidades", en: "PDF · 53 exercises, 37 from other regions' PAU exams" }, url: "materials/2batx-ccss/t10-fitxa-exercicis.pdf", download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 53 exercicis", es: "PDF · Soluciones de los 53 ejercicios", en: "PDF · Solutions to all 53 exercises" }, url: "materials/2batx-ccss/t10-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "5 exercicis resolts de la PAU valenciana (2000–2026)", es: "5 ejercicios resueltos de la PAU valenciana (2000–2026)", en: "5 solved past Valencian PAU exercises (2000–2026)" }, url: "materials/2batx-ccss/pau-u10-binomial-normal.html", date: "2026-10-27" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u10-binomial-normal.html", date: "2026-10-28" }
        ]
      }
    ]
  }
};
