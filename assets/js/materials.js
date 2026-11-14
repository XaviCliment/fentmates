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
            També pot ser { va: "...", es: "..." } per a enllaçar un fitxer diferent
            en cada idioma (si falta un idioma, s'usa el de va).

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
      va: "Nombres naturals i enters, fraccions, proporcionalitat, àlgebra i geometria plana.",
      es: "Números naturales y enteros, fracciones, proporcionalidad, álgebra y geometría plana.",
      en: "Whole numbers and integers, fractions, proportionality, algebra and plane geometry."
    },
    units: [
      {
        ill: "naturals", block: "ari",
        title: { va: "Nombres naturals", es: "Números naturales", en: "Natural numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t1-nombres-naturals.html", date: "2026-10-21" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 71 exercicis graduats per nivells de dificultat", es: "PDF · 71 ejercicios graduados por niveles de dificultad", en: "PDF · 71 exercises graded by difficulty" }, url: { va: "materials/1eso/t1-fitxa-exercicis.pdf", es: "materials/1eso/t1-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-21" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 71 exercicis", es: "PDF · Soluciones de los 71 ejercicios", en: "PDF · Solutions to all 71 exercises" }, url: { va: "materials/1eso/t1-fitxa-solucions.pdf", es: "materials/1eso/t1-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-21" }
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
      },
      {
        ill: "proporcionalitat", block: "ari",
        title: { va: "Proporcionalitat i percentatges. Nombres decimals", es: "Proporcionalidad y porcentajes. Números decimales", en: "Proportionality and percentages. Decimal numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t5-proporcionalitat-decimals.html", date: "2026-11-01" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 69 exercicis graduats per nivells de dificultat", es: "PDF · 69 ejercicios graduados por niveles de dificultad", en: "PDF · 69 exercises graded by difficulty" }, url: "materials/1eso/t5-fitxa-exercicis.pdf", download: true, date: "2026-11-01" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 69 exercicis", es: "PDF · Soluciones de los 69 ejercicios", en: "PDF · Solutions to all 69 exercises" }, url: "materials/1eso/t5-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-01" }
        ]
      },
      {
        ill: "equacions", block: "alg",
        title: { va: "Introducció a l'àlgebra. Equacions de 1r grau", es: "Introducción al álgebra. Ecuaciones de 1.er grado", en: "Introduction to algebra. First-degree equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t6-algebra-equacions.html", date: "2026-11-01" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 68 exercicis graduats per nivells de dificultat", es: "PDF · 68 ejercicios graduados por niveles de dificultad", en: "PDF · 68 exercises graded by difficulty" }, url: "materials/1eso/t6-fitxa-exercicis.pdf", download: true, date: "2026-11-01" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 68 exercicis", es: "PDF · Soluciones de los 68 ejercicios", en: "PDF · Solutions to all 68 exercises" }, url: "materials/1eso/t6-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-01" }
        ]
      },
      {
        ill: "angles", block: "geo",
        title: { va: "Geometria bàsica del pla", es: "Geometría básica del plano", en: "Basic plane geometry" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t7-geometria-pla.html", date: "2026-11-02" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 67 exercicis graduats per nivells de dificultat", es: "PDF · 67 ejercicios graduados por niveles de dificultad", en: "PDF · 67 exercises graded by difficulty" }, url: "materials/1eso/t7-fitxa-exercicis.pdf", download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 67 exercicis", es: "PDF · Soluciones de los 67 ejercicios", en: "PDF · Solutions to all 67 exercises" }, url: "materials/1eso/t7-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-02" }
        ]
      },
      {
        ill: "arees", block: "geo",
        title: { va: "Àrees i perímetres", es: "Áreas y perímetros", en: "Area and perimeter" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t8-arees-perimetres.html", date: "2026-11-02" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 87 exercicis graduats per nivells de dificultat", es: "PDF · 87 ejercicios graduados por niveles de dificultad", en: "PDF · 87 exercises graded by difficulty" }, url: "materials/1eso/t8-fitxa-exercicis.pdf", download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 87 exercicis", es: "PDF · Soluciones de los 87 ejercicios", en: "PDF · Solutions to all 87 exercises" }, url: "materials/1eso/t8-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-02" }
        ]
      },
      {
        ill: "lineal", block: "an",
        title: { va: "Gràfics de funcions", es: "Gráficas de funciones", en: "Graphs of functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t9-grafics-funcions.html", date: "2026-11-02" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 61 exercicis graduats per nivells de dificultat", es: "PDF · 61 ejercicios graduados por niveles de dificultad", en: "PDF · 61 exercises graded by difficulty" }, url: "materials/1eso/t9-fitxa-exercicis.pdf", download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 61 exercicis", es: "PDF · Soluciones de los 61 ejercicios", en: "PDF · Solutions to all 61 exercises" }, url: "materials/1eso/t9-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-02" }
        ]
      },
      {
        ill: "estadistica", block: "pr",
        title: { va: "Estadística", es: "Estadística", en: "Statistics" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t10-estadistica.html", date: "2026-11-02" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 65 exercicis graduats per nivells de dificultat", es: "PDF · 65 ejercicios graduados por niveles de dificultad", en: "PDF · 65 exercises graded by difficulty" }, url: "materials/1eso/t10-fitxa-exercicis.pdf", download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 65 exercicis", es: "PDF · Soluciones de los 65 ejercicios", en: "PDF · Solutions to all 65 exercises" }, url: "materials/1eso/t10-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-02" }
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
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 63 exercicis graduats per nivells de dificultat", es: "PDF · 63 ejercicios graduados por niveles de dificultad", en: "PDF · 63 exercises graded by difficulty" }, url: { va: "materials/3eso/t1-fitxa-exercicis.pdf", es: "materials/3eso/t1-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-19" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 63 exercicis", es: "PDF · Soluciones de los 63 ejercicios", en: "PDF · Solutions to all 63 exercises" }, url: { va: "materials/3eso/t1-fitxa-solucions.pdf", es: "materials/3eso/t1-fitxa-solucions-es.pdf" }, download: true, date: "2026-10-19" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/3eso/casio-u1-racionals.html", es: "materials/3eso/casio-u1-racionals-es.html" } }
        ]
      },
      {
        ill: "reals", block: "ari",
        title: { va: "Nombres reals", es: "Números reales", en: "Real numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t2-nombres-reals.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 46 exercicis graduats per nivells de dificultat", es: "PDF · 46 ejercicios graduados por niveles de dificultad", en: "PDF · 46 exercises graded by difficulty" }, url: { va: "materials/3eso/t2-fitxa-exercicis.pdf", es: "materials/3eso/t2-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-18" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 46 exercicis", es: "PDF · Soluciones de los 46 ejercicios", en: "PDF · Solutions to all 46 exercises" }, url: { va: "materials/3eso/t2-fitxa-solucions.pdf", es: "materials/3eso/t2-fitxa-solucions-es.pdf" }, download: true, date: "2026-10-18" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/3eso/casio-u2-reals.html", es: "materials/3eso/casio-u2-reals-es.html" } },
          { type: "notes", title: { va: "Presentació-resum per a l'examen (interactiva)", es: "Presentación-resumen para el examen (interactiva)", en: "Exam summary slides (interactive)" }, desc: { va: "15 diapositives amb mapa conceptual, errors típics i autoavaluació", es: "15 diapositivas con mapa conceptual, errores típicos y autoevaluación", en: "15 slides with a concept map, common mistakes and a self-check" }, url: "materials/3eso/t2-resum-diapositives.html", date: "2026-10-19" },
          { type: "exam", title: { va: "Model d'examen", es: "Modelo de examen", en: "Mock exam" }, desc: { va: "PDF · 9 preguntes de tota la unitat (10 punts)", es: "PDF · 9 preguntas de toda la unidad (10 puntos)", en: "PDF · 9 questions covering the whole unit (10 points)" }, url: "materials/3eso/t2-model-examen.pdf", download: true, hidden: true, date: "2026-10-26" },
          { type: "exam", title: { va: "Solucions del model d'examen", es: "Soluciones del modelo de examen", en: "Mock exam solutions" }, desc: { va: "PDF · Solucions i criteris de correcció", es: "PDF · Soluciones y criterios de corrección", en: "PDF · Solutions and marking criteria" }, url: "materials/3eso/t2-model-examen-solucions.pdf", download: true, hidden: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Fitxa de repàs per a l'examen", es: "Ficha de repaso para el examen", en: "Exam review worksheet" }, desc: { va: "PDF · 13 exercicis, un de cada contingut de la unitat", es: "PDF · 13 ejercicios, uno de cada contenido de la unidad", en: "PDF · 13 exercises, one for each topic of the unit" }, url: { va: "materials/3eso/t2-fitxa-repas.pdf", es: "materials/3eso/t2-fitxa-repas-es.pdf" }, download: true, date: "2026-10-29" },
          { type: "exercises", title: { va: "Solucions de la fitxa de repàs", es: "Soluciones de la ficha de repaso", en: "Review worksheet solutions" }, desc: { va: "PDF · Solucions pas a pas per a autocorregir-te", es: "PDF · Soluciones paso a paso para autocorregirte", en: "PDF · Step-by-step solutions to self-check" }, url: { va: "materials/3eso/t2-fitxa-repas-solucions.pdf", es: "materials/3eso/t2-fitxa-repas-solucions-es.pdf" }, download: true, date: "2026-10-29" }
        ]
      },
      {
        ill: "proporcionalitat", block: "ari",
        title: { va: "Proporcionalitat i percentatges", es: "Proporcionalidad y porcentajes", en: "Proportionality and percentages" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t3-proporcionalitat-percentatges.html", date: "2026-10-20" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 79 exercicis graduats per nivells de dificultat", es: "PDF · 79 ejercicios graduados por niveles de dificultad", en: "PDF · 79 exercises graded by difficulty" }, url: { va: "materials/3eso/t3-fitxa-exercicis.pdf", es: "materials/3eso/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-20" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 79 exercicis", es: "PDF · Soluciones de los 79 ejercicios", en: "PDF · Solutions to all 79 exercises" }, url: { va: "materials/3eso/t3-fitxa-solucions.pdf", es: "materials/3eso/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-20" }
        ]
      },
      {
        ill: "polinomis", block: "alg",
        title: { va: "Àlgebra", es: "Álgebra", en: "Algebra" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t4-polinomis.html", date: "2026-10-30" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 65 exercicis graduats per nivells de dificultat", es: "PDF · 65 ejercicios graduados por niveles de dificultad", en: "PDF · 65 exercises graded by difficulty" }, url: { va: "materials/3eso/t4-fitxa-exercicis.pdf", es: "materials/3eso/t4-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-30" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 65 exercicis", es: "PDF · Soluciones de los 65 ejercicios", en: "PDF · Solutions to all 65 exercises" }, url: { va: "materials/3eso/t4-fitxa-solucions.pdf", es: "materials/3eso/t4-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-30" },
          { type: "resource", date: "2026-10-15", title: { va: "GeoGebra: identitats notables $(a+b)^2$", es: "GeoGebra: identidades notables $(a+b)^2$", en: "GeoGebra: special products $(a+b)^2$" }, url: "https://www.geogebra.org" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/3eso/casio-u4-polinomis.html", es: "materials/3eso/casio-u4-polinomis-es.html" } }
        ]
      },
      {
        ill: "equacions", block: "alg",
        title: { va: "Equacions", es: "Ecuaciones", en: "Equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t5-equacions.html", date: "2026-10-30" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 62 exercicis graduats per nivells de dificultat", es: "PDF · 62 ejercicios graduados por niveles de dificultad", en: "PDF · 62 exercises graded by difficulty" }, url: { va: "materials/3eso/t5-fitxa-exercicis.pdf", es: "materials/3eso/t5-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-30" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 62 exercicis", es: "PDF · Soluciones de los 62 ejercicios", en: "PDF · Solutions to all 62 exercises" }, url: { va: "materials/3eso/t5-fitxa-solucions.pdf", es: "materials/3eso/t5-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-30" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/3eso/casio-u5-equacions.html", es: "materials/3eso/casio-u5-equacions-es.html" } }
        ]
      },
      {
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions", es: "Sistemas de ecuaciones", en: "Simultaneous equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t6-sistemes-equacions.html", date: "2026-10-30" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 63 exercicis graduats per nivells de dificultat", es: "PDF · 63 ejercicios graduados por niveles de dificultad", en: "PDF · 63 exercises graded by difficulty" }, url: { va: "materials/3eso/t6-fitxa-exercicis.pdf", es: "materials/3eso/t6-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-30" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 63 exercicis", es: "PDF · Soluciones de los 63 ejercicios", en: "PDF · Solutions to all 63 exercises" }, url: { va: "materials/3eso/t6-fitxa-solucions.pdf", es: "materials/3eso/t6-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-30" }
        ]
      },
      {
        ill: "grafiques", block: "an",
        title: { va: "Funcions", es: "Funciones", en: "Functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t7-funcions.html", date: "2026-10-30" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 60 exercicis graduats per nivells de dificultat", es: "PDF · 60 ejercicios graduados por niveles de dificultad", en: "PDF · 60 exercises graded by difficulty" }, url: { va: "materials/3eso/t7-fitxa-exercicis.pdf", es: "materials/3eso/t7-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-30" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 60 exercicis", es: "PDF · Soluciones de los 60 ejercicios", en: "PDF · Solutions to all 60 exercises" }, url: { va: "materials/3eso/t7-fitxa-solucions.pdf", es: "materials/3eso/t7-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-30" }
        ]
      },
      {
        ill: "lineal", block: "an",
        title: { va: "Funció lineal i quadràtica", es: "Función lineal y cuadrática", en: "Linear and quadratic functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t8-funcio-lineal-quadratica.html", date: "2026-10-30" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 62 exercicis graduats per nivells de dificultat", es: "PDF · 62 ejercicios graduados por niveles de dificultad", en: "PDF · 62 exercises graded by difficulty" }, url: { va: "materials/3eso/t8-fitxa-exercicis.pdf", es: "materials/3eso/t8-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-30" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 62 exercicis", es: "PDF · Soluciones de los 62 ejercicios", en: "PDF · Solutions to all 62 exercises" }, url: { va: "materials/3eso/t8-fitxa-solucions.pdf", es: "materials/3eso/t8-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-30" }
        ]
      },
      {
        ill: "pitagores", block: "geo",
        title: { va: "Perímetres i àrees. Teorema de Pitàgores", es: "Perímetros y áreas. Teorema de Pitágoras", en: "Perimeters and areas. Pythagoras' theorem" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t9-perimetres-arees-pitagores.html", date: "2026-10-31" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 71 exercicis graduats per nivells de dificultat", es: "PDF · 71 ejercicios graduados por niveles de dificultad", en: "PDF · 71 exercises graded by difficulty" }, url: { va: "materials/3eso/t9-fitxa-exercicis.pdf", es: "materials/3eso/t9-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-31" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 71 exercicis", es: "PDF · Soluciones de los 71 ejercicios", en: "PDF · Solutions to all 71 exercises" }, url: { va: "materials/3eso/t9-fitxa-solucions.pdf", es: "materials/3eso/t9-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-31" }
        ]
      },
      {
        ill: "tales", block: "geo",
        title: { va: "Proporcionalitat. Teorema de Tales", es: "Proporcionalidad. Teorema de Tales", en: "Proportionality. Thales' theorem" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t10-tales-semblanca.html", date: "2026-10-31" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 58 exercicis graduats per nivells de dificultat", es: "PDF · 58 ejercicios graduados por niveles de dificultad", en: "PDF · 58 exercises graded by difficulty" }, url: { va: "materials/3eso/t10-fitxa-exercicis.pdf", es: "materials/3eso/t10-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-31" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 58 exercicis", es: "PDF · Soluciones de los 58 ejercicios", en: "PDF · Solutions to all 58 exercises" }, url: { va: "materials/3eso/t10-fitxa-solucions.pdf", es: "materials/3eso/t10-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-31" }
        ]
      },
      {
        ill: "cossos", block: "geo",
        title: { va: "Cossos geomètrics", es: "Cuerpos geométricos", en: "Solids" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t11-cossos-geometrics.html", date: "2026-10-31" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 63 exercicis graduats per nivells de dificultat", es: "PDF · 63 ejercicios graduados por niveles de dificultad", en: "PDF · 63 exercises graded by difficulty" }, url: { va: "materials/3eso/t11-fitxa-exercicis.pdf", es: "materials/3eso/t11-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-31" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 63 exercicis", es: "PDF · Soluciones de los 63 ejercicios", en: "PDF · Solutions to all 63 exercises" }, url: { va: "materials/3eso/t11-fitxa-solucions.pdf", es: "materials/3eso/t11-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-31" }
        ]
      },
      {
        ill: "probabilitat", block: "pr",
        title: { va: "Probabilitat", es: "Probabilidad", en: "Probability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t12-probabilitat.html", date: "2026-11-01" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 52 exercicis graduats per nivells de dificultat", es: "PDF · 52 ejercicios graduados por niveles de dificultad", en: "PDF · 52 exercises graded by difficulty" }, url: { va: "materials/3eso/t12-fitxa-exercicis.pdf", es: "materials/3eso/t12-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-01" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 52 exercicis", es: "PDF · Soluciones de los 52 ejercicios", en: "PDF · Solutions to all 52 exercises" }, url: { va: "materials/3eso/t12-fitxa-solucions.pdf", es: "materials/3eso/t12-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-01" }
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
    units: [
      {
        num: "1",
        ill: "reals", block: "ari",
        title: { va: "Nombres reals", es: "Números reales", en: "Real numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t1-nombres-reals.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 36 exercicis: els 17 de la fitxa del departament i 19 d'ampliació", es: "PDF · 36 ejercicios: los 17 de la ficha del departamento y 19 de ampliación", en: "PDF · 36 exercises: the 17 from the department worksheet and 19 extension ones" }, url: "materials/4eso-b/t1-fitxa-exercicis.pdf", download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 36 exercicis", es: "PDF · Soluciones de los 36 ejercicios", en: "PDF · Solutions to all 36 exercises" }, url: "materials/4eso-b/t1-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "2",
        ill: "polinomis", block: "alg",
        title: { va: "Polinomis i fraccions algebraiques", es: "Polinomios y fracciones algebraicas", en: "Polynomials and algebraic fractions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t2-polinomis-fraccions.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 35 exercicis: els de les fitxes del departament, del binomi de Newton a les fraccions algebraiques", es: "PDF · 35 ejercicios: los de las fichas del departamento, del binomio de Newton a las fracciones algebraicas", en: "PDF · 35 exercises from the department worksheets, from the binomial theorem to algebraic fractions" }, url: "materials/4eso-b/t2-fitxa-exercicis.pdf", download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 35 exercicis", es: "PDF · Soluciones de los 35 ejercicios", en: "PDF · Solutions to all 35 exercises" }, url: "materials/4eso-b/t2-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "3",
        ill: "equacions", block: "alg",
        title: { va: "Equacions i inequacions", es: "Ecuaciones e inecuaciones", en: "Equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t3-equacions-inequacions.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 41 exercicis, de les equacions de segon grau a les inequacions", es: "PDF · 41 ejercicios, de las ecuaciones de segundo grado a las inecuaciones", en: "PDF · 41 exercises, from quadratic equations to inequalities" }, url: "materials/4eso-b/t3-fitxa-exercicis.pdf", download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 41 exercicis", es: "PDF · Soluciones de los 41 ejercicios", en: "PDF · Solutions to all 41 exercises" }, url: "materials/4eso-b/t3-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "4",
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions i inequacions", es: "Sistemas de ecuaciones e inecuaciones", en: "Systems of equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t4-sistemes-inequacions.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 31 exercicis, dels mètodes de resolució a les regions del pla", es: "PDF · 31 ejercicios, de los métodos de resolución a las regiones del plano", en: "PDF · 31 exercises, from solving methods to regions of the plane" }, url: "materials/4eso-b/t4-fitxa-exercicis.pdf", download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 31 exercicis", es: "PDF · Soluciones de los 31 ejercicios", en: "PDF · Solutions to all 31 exercises" }, url: "materials/4eso-b/t4-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "5",
        ill: "trigonometria", block: "geo",
        title: { va: "Trigonometria", es: "Trigonometría", en: "Trigonometry" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t5-trigonometria.html", date: "2026-11-14" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 64 exercicis, dels radians a la reducció al primer quadrant", es: "PDF · 64 ejercicios, de los radianes a la reducción al primer cuadrante", en: "PDF · 64 exercises, from radians to reduction to the first quadrant" }, url: "materials/4eso-b/t5-fitxa-exercicis.pdf", download: true, date: "2026-11-14" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 64 exercicis", es: "PDF · Soluciones de los 64 ejercicios", en: "PDF · Solutions to all 64 exercises" }, url: "materials/4eso-b/t5-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-14" }
        ]
      }
    ]
  },

  "1batx-mi": {
    color: "#9b1c1c",
    symbol: "sin",
    stage: "batx",
    cards: true,
    name: { va: "1r Batxillerat MI", es: "1º Bachillerato MI", en: "1st Baccalaureate Maths I" },
    desc: {
      va: "Nombres reals, àlgebra, geometria analítica, trigonometria, anàlisi i estadística.",
      es: "Números reales, álgebra, geometría analítica, trigonometría, análisis y estadística.",
      en: "Real numbers, algebra, coordinate geometry, trigonometry, calculus and statistics."
    },
    units: [
      {
        // num: el número de la unitat que es mostra a la targeta. Les dues parts de Trigonometria dels apunts del departament són una sola unitat, la 5
        num: "1",
        ill: "reals", block: "ari",
        title: { va: "Nombres reals", es: "Números reales", en: "Real numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t1-nombres-reals.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis, de la classificació dels nombres als logaritmes", es: "PDF · 54 ejercicios, de la clasificación de los números a los logaritmos", en: "PDF · 54 exercises, from classifying numbers to logarithms" }, url: "materials/1batx-mi/t1-fitxa-exercicis.pdf", download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: "materials/1batx-mi/t1-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-10" }
        ]
      },
      {
        num: "2",
        ill: "polinomis", block: "alg",
        title: { va: "Àlgebra. Equacions i inequacions", es: "Álgebra. Ecuaciones e inecuaciones", en: "Algebra. Equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t2-algebra.html", date: "2026-11-11" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 71 exercicis, dels polinomis a les inequacions i els problemes", es: "PDF · 71 ejercicios, de los polinomios a las inecuaciones y los problemas", en: "PDF · 71 exercises, from polynomials to inequalities and word problems" }, url: "materials/1batx-mi/t2-fitxa-exercicis.pdf", download: true, date: "2026-11-11" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 71 exercicis", es: "PDF · Soluciones de los 71 ejercicios", en: "PDF · Solutions to all 71 exercises" }, url: "materials/1batx-mi/t2-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-11" }
        ]
      },
      {
        num: "3",
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions i inequacions", es: "Sistemas de ecuaciones e inecuaciones", en: "Systems of equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t3-sistemes-inequacions.html", date: "2026-11-11" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 32 exercicis, del mètode de Gauss a les regions del pla i els problemes", es: "PDF · 32 ejercicios, del método de Gauss a las regiones del plano y los problemas", en: "PDF · 32 exercises, from Gaussian elimination to regions of the plane and word problems" }, url: "materials/1batx-mi/t3-fitxa-exercicis.pdf", download: true, date: "2026-11-11" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 32 exercicis", es: "PDF · Soluciones de los 32 ejercicios", en: "PDF · Solutions to all 32 exercises" }, url: "materials/1batx-mi/t3-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-11" }
        ]
      },
      {
        num: "4",
        ill: "geometria", block: "geo",
        title: { va: "Geometria analítica en el pla", es: "Geometría analítica en el plano", en: "Coordinate geometry in the plane" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t4-geometria-pla.html", date: "2026-10-29" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 61 exercicis, dels vectors als problemes mètrics", es: "PDF · 61 ejercicios, de los vectores a los problemas métricos", en: "PDF · 61 exercises, from vectors to metric problems" }, url: "materials/1batx-mi/t4-fitxa-exercicis.pdf", download: true, date: "2026-10-29" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 61 exercicis", es: "PDF · Soluciones de los 61 ejercicios", en: "PDF · Solutions to all 61 exercises" }, url: "materials/1batx-mi/t4-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-29" }
        ]
      },
      {
        num: "5",
        ill: "trigonometria", block: "geo",
        title: { va: "Trigonometria", es: "Trigonometría", en: "Trigonometry" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t5-trigonometria.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 73 exercicis, dels radians a les funcions trigonomètriques", es: "PDF · 73 ejercicios, de los radianes a las funciones trigonométricas", en: "PDF · 73 exercises, from radians to the trigonometric functions" }, url: "materials/1batx-mi/t5-fitxa-exercicis.pdf", download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 73 exercicis", es: "PDF · Soluciones de los 73 ejercicios", en: "PDF · Solutions to all 73 exercises" }, url: "materials/1batx-mi/t5-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-10" }
        ]
      },
      {
        num: "6",
        ill: "grafiques", block: "an",
        title: { va: "Estudi de funcions", es: "Estudio de funciones", en: "Studying functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t6-estudi-funcions.html", date: "2026-11-11" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 30 exercicis, del domini a la funció inversa", es: "PDF · 30 ejercicios, del dominio a la función inversa", en: "PDF · 30 exercises, from domains to inverse functions" }, url: "materials/1batx-mi/t6-fitxa-exercicis.pdf", download: true, date: "2026-11-11" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 30 exercicis", es: "PDF · Soluciones de los 30 ejercicios", en: "PDF · Solutions to all 30 exercises" }, url: "materials/1batx-mi/t6-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-11" }
        ]
      },
      {
        num: "7",
        ill: "grafiques", block: "an",
        title: { va: "Funcions elementals", es: "Funciones elementales", en: "Elementary functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t7-funcions-elementals.html", date: "2026-11-11" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 35 exercicis, de la recta als problemes de màxims i mínims", es: "PDF · 35 ejercicios, de la recta a los problemas de máximos y mínimos", en: "PDF · 35 exercises, from straight lines to maximum and minimum problems" }, url: "materials/1batx-mi/t7-fitxa-exercicis.pdf", download: true, date: "2026-11-11" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 35 exercicis", es: "PDF · Soluciones de los 35 ejercicios", en: "PDF · Solutions to all 35 exercises" }, url: "materials/1batx-mi/t7-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-11" }
        ]
      },
      {
        num: "8",
        ill: "limits", block: "an",
        title: { va: "Límits i continuïtat", es: "Límites y continuidad", en: "Limits and continuity" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t8-limits-continuitat.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 36 exercicis, dels límits a l'infinit a les branques infinites", es: "PDF · 36 ejercicios, de los límites en el infinito a las ramas infinitas", en: "PDF · 36 exercises, from limits at infinity to infinite branches" }, url: "materials/1batx-mi/t8-fitxa-exercicis.pdf", download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 36 exercicis", es: "PDF · Soluciones de los 36 ejercicios", en: "PDF · Solutions to all 36 exercises" }, url: "materials/1batx-mi/t8-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "9",
        ill: "derivades", block: "an",
        title: { va: "Derivades i aplicacions", es: "Derivadas y aplicaciones", en: "Derivatives and applications" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t9-derivades.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 31 exercicis, de la TVM a la representació gràfica i l'optimització", es: "PDF · 31 ejercicios, de la TVM a la representación gráfica y la optimización", en: "PDF · 31 exercises, from average rate of change to graphing and optimisation" }, url: "materials/1batx-mi/t9-fitxa-exercicis.pdf", download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 31 exercicis", es: "PDF · Soluciones de los 31 ejercicios", en: "PDF · Solutions to all 31 exercises" }, url: "materials/1batx-mi/t9-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "10",
        ill: "estadistica", block: "pr",
        title: { va: "Estadística", es: "Estadística", en: "Statistics" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t10-estadistica.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 34 exercicis, de les taules de freqüències a la recta de regressió", es: "PDF · 34 ejercicios, de las tablas de frecuencias a la recta de regresión", en: "PDF · 34 exercises, from frequency tables to the regression line" }, url: "materials/1batx-mi/t10-fitxa-exercicis.pdf", download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 34 exercicis", es: "PDF · Soluciones de los 34 ejercicios", en: "PDF · Solutions to all 34 exercises" }, url: "materials/1batx-mi/t10-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-13" }
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
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 62 exercicis, 32 de la PAU de 16 comunitats autònomes", es: "PDF · 62 ejercicios, 32 de la PAU de 16 comunidades autónomas", en: "PDF · 62 exercises, 32 from the PAU of 16 Spanish regions" }, url: "materials/2batx-mii/t2-fitxa-exercicis.pdf", download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 62 exercicis", es: "PDF · Soluciones de los 62 ejercicios", en: "PDF · Solutions to all 62 exercises" }, url: "materials/2batx-mii/t2-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-02" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-mii/casio-u2-sistemes.html", date: "2026-10-23" }
        ]
      },
      {
        ill: "geometria", block: "geo",
        title: { va: "Vectors i aplicacions. Rectes, plans i feixos de plans", es: "Vectores y aplicaciones. Rectas, planos y haces de planos", en: "Vectors and applications. Lines, planes and pencils of planes" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t3-vectors-rectes-plans.html", date: "2026-10-29" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "30 exercicis resolts de la PAU valenciana (1999–2026)", es: "30 ejercicios resueltos de la PAU valenciana (1999–2026)", en: "30 solved past Valencian PAU exercises (1999–2026)" }, url: "materials/2batx-mii/pau-u3-rectes-plans.html", date: "2026-11-08" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 92 exercicis, 40 de la PAU de 16 comunitats autònomes", es: "PDF · 92 ejercicios, 40 de la PAU de 16 comunidades autónomas", en: "PDF · 92 exercises, 40 from the PAU of 16 Spanish regions" }, url: "materials/2batx-mii/t3-fitxa-exercicis.pdf", download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 92 exercicis", es: "PDF · Soluciones de los 92 ejercicios", en: "PDF · Solutions to all 92 exercises" }, url: "materials/2batx-mii/t3-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-02" }
        ]
      },
      {
        ill: "geometria", block: "geo",
        title: { va: "Problemes mètrics", es: "Problemas métricos", en: "Metric problems" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t4-problemes-metrics.html", date: "2026-11-08" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "86 exercicis resolts de la PAU valenciana (1999–2026)", es: "86 ejercicios resueltos de la PAU valenciana (1999–2026)", en: "86 solved past Valencian PAU exercises (1999–2026)" }, url: "materials/2batx-mii/pau-u4-problemes-metrics.html", date: "2026-11-08" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 108 exercicis, 59 de la PAU de 16 comunitats autònomes", es: "PDF · 108 ejercicios, 59 de la PAU de 16 comunidades autónomas", en: "PDF · 108 exercises, 59 from the PAU of 16 Spanish regions" }, url: "materials/2batx-mii/t4-fitxa-exercicis.pdf", download: true, date: "2026-11-08" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 108 exercicis", es: "PDF · Soluciones de los 108 ejercicios", en: "PDF · Solutions to all 108 exercises" }, url: "materials/2batx-mii/t4-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-08" }
        ]
      },
      {
        ill: "limits", block: "an",
        title: { va: "Límits i continuïtat", es: "Límites y continuidad", en: "Limits and continuity" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t5-limits-continuitat.html", date: "2026-11-08" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "24 exercicis resolts de la PAU valenciana (2005–2026)", es: "24 ejercicios resueltos de la PAU valenciana (2005–2026)", en: "24 solved past Valencian PAU exercises (2005–2026)" }, url: "materials/2batx-mii/pau-u5-limits-continuitat.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 106 exercicis, 75 de la PAU de 16 comunitats autònomes", es: "PDF · 106 ejercicios, 75 de la PAU de 16 comunidades autónomas", en: "PDF · 106 exercises, 75 from the PAU of 16 Spanish regions" }, url: "materials/2batx-mii/t5-fitxa-exercicis.pdf", download: true, date: "2026-11-08" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 106 exercicis", es: "PDF · Soluciones de los 106 ejercicios", en: "PDF · Solutions to all 106 exercises" }, url: "materials/2batx-mii/t5-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-08" }
        ]
      },
      {
        ill: "derivades", block: "an",
        title: { va: "Càlcul de derivades. Derivabilitat d'una funció", es: "Cálculo de derivadas. Derivabilidad de una función", en: "Computing derivatives. Differentiability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t6-derivades.html", date: "2026-11-09" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "14 exercicis resolts de la PAU valenciana (2002–2018)", es: "14 ejercicios resueltos de la PAU valenciana (2002–2018)", en: "14 solved past Valencian PAU exercises (2002–2018)" }, url: "materials/2batx-mii/pau-u6-derivades.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 71 exercicis, 48 de la PAU de 14 comunitats autònomes", es: "PDF · 71 ejercicios, 48 de la PAU de 14 comunidades autónomas", en: "PDF · 71 exercises, 48 from the PAU of 14 Spanish regions" }, url: "materials/2batx-mii/t6-fitxa-exercicis.pdf", download: true, date: "2026-11-09" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 71 exercicis", es: "PDF · Soluciones de los 71 ejercicios", en: "PDF · Solutions to all 71 exercises" }, url: "materials/2batx-mii/t6-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-09" }
        ]
      },
      {
        ill: "aplicacions", block: "an",
        title: { va: "Aplicacions de la derivada", es: "Aplicaciones de la derivada", en: "Applications of the derivative" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t7-aplicacions-derivada.html", date: "2026-11-09" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "94 exercicis resolts de la PAU valenciana (2002–2026)", es: "94 ejercicios resueltos de la PAU valenciana (2002–2026)", en: "94 solved past Valencian PAU exercises (2002–2026)" }, url: "materials/2batx-mii/pau-u7-aplicacions-derivada.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 93 exercicis, 102 apartats de la PAU de 16 comunitats autònomes", es: "PDF · 93 ejercicios, 102 apartados de la PAU de 16 comunidades autónomas", en: "PDF · 93 exercises, 102 PAU items from 16 Spanish regions" }, url: "materials/2batx-mii/t7-fitxa-exercicis.pdf", download: true, date: "2026-11-09" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 93 exercicis, amb gràfiques", es: "PDF · Soluciones de los 93 ejercicios, con gráficas", en: "PDF · Solutions to all 93 exercises, with graphs" }, url: "materials/2batx-mii/t7-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-09" }
        ]
      },
      {
        ill: "grafiques", block: "an",
        title: { va: "Representació gràfica de funcions", es: "Representación gráfica de funciones", en: "Graphing functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t8-representacio-funcions.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "16 exercicis resolts de la PAU valenciana (2011–2026)", es: "16 ejercicios resueltos de la PAU valenciana (2011–2026)", en: "16 solved past Valencian PAU exercises (2011–2026)" }, url: "materials/2batx-mii/pau-u8-representacio-funcions.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 60 exercicis, 31 de la PAU de 13 comunitats autònomes", es: "PDF · 60 ejercicios, 31 de la PAU de 13 comunidades autónomas", en: "PDF · 60 exercises, 31 from the PAU of 13 Spanish regions" }, url: "materials/2batx-mii/t8-fitxa-exercicis.pdf", download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 60 exercicis, amb gràfiques", es: "PDF · Soluciones de los 60 ejercicios, con gráficas", en: "PDF · Solutions to all 60 exercises, with graphs" }, url: "materials/2batx-mii/t8-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-10" }
        ]
      },
      {
        ill: "integrals", block: "an",
        title: { va: "Integrals", es: "Integrales", en: "Integrals" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t9-integrals.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "57 exercicis resolts de la PAU valenciana (2002–2026)", es: "57 ejercicios resueltos de la PAU valenciana (2002–2026)", en: "57 solved past Valencian PAU exercises (2002–2026)" }, url: "materials/2batx-mii/pau-u9-integrals.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 56 exercicis, 48 apartats de la PAU de 14 comunitats autònomes", es: "PDF · 56 ejercicios, 48 apartados de la PAU de 14 comunidades autónomas", en: "PDF · 56 exercises, 48 PAU items from 14 Spanish regions" }, url: "materials/2batx-mii/t9-fitxa-exercicis.pdf", download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 56 exercicis, amb gràfiques", es: "PDF · Soluciones de los 56 ejercicios, con gráficas", en: "PDF · Solutions to all 56 exercises, with graphs" }, url: "materials/2batx-mii/t9-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-10" }
        ]
      },
      {
        ill: "probabilitat", block: "pr",
        title: { va: "Probabilitat", es: "Probabilidad", en: "Probability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t10-probabilitat.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "13 exercicis resolts de la PAU valenciana (2023–2026)", es: "13 ejercicios resueltos de la PAU valenciana (2023–2026)", en: "13 solved past Valencian PAU exercises (2023–2026)" }, url: "materials/2batx-mii/pau-u10-probabilitat.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 91 exercicis, 65 de la PAU de 16 comunitats autònomes", es: "PDF · 91 ejercicios, 65 de la PAU de 16 comunidades autónomas", en: "PDF · 91 exercises, 65 from the PAU of 16 Spanish regions" }, url: "materials/2batx-mii/t10-fitxa-exercicis.pdf", download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 91 exercicis, amb arbres i taules", es: "PDF · Soluciones de los 91 ejercicios, con árboles y tablas", en: "PDF · Solutions to all 91 exercises, with trees and tables" }, url: "materials/2batx-mii/t10-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-11-10" }
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
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "33 exercicis de la PAU valenciana (1994–2026)", es: "33 ejercicios de la PAU valenciana (1994–2026)", en: "33 past Valencian PAU exercises (1994–2026)" }, url: { va: "materials/2batx-ccss/pau-u1-matrius.html", es: "materials/2batx-ccss/pau-u1-matrius-es.html" } },
          { type: "exam", title: { va: "Model d'examen tipus PAU", es: "Modelo de examen tipo PAU", en: "PAU-style mock exam" }, desc: { va: "4 problemes amb solucions i criteris de correcció", es: "4 problemas con soluciones y criterios de corrección", en: "4 problems with solutions and marking criteria" }, url: "materials/2batx-ccss/examen-u1-matrius-model1.html", date: "2026-10-21" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 50 exercicis, de les operacions a les equacions matricials", es: "PDF · 50 ejercicios, de las operaciones a las ecuaciones matriciales", en: "PDF · 50 exercises, from operations to matrix equations" }, url: "materials/2batx-ccss/t1-fitxa-exercicis.pdf", download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 50 exercicis", es: "PDF · Soluciones de los 50 ejercicios", en: "PDF · Solutions to all 50 exercises" }, url: "materials/2batx-ccss/t1-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-27" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u1-matrius.html", es: "materials/2batx-ccss/casio-u1-matrius-es.html" } }
        ]
      },
      {
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions lineals", es: "Sistemas de ecuaciones lineales", en: "Systems of linear equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t2-sistemes-equacions.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "68 exercicis de la PAU valenciana (1994–2026)", es: "68 ejercicios de la PAU valenciana (1994–2026)", en: "68 past Valencian PAU exercises (1994–2026)" }, url: "materials/2batx-ccss/pau-u2-sistemes.html" },
          { type: "exam", title: { va: "Model d'examen tipus PAU", es: "Modelo de examen tipo PAU", en: "PAU-style mock exam" }, desc: { va: "4 problemes amb solucions i criteris de correcció", es: "4 problemas con soluciones y criterios de corrección", en: "4 problems with solutions and marking criteria" }, url: "materials/2batx-ccss/examen-u2-sistemes-model1.html", date: "2026-11-01" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 60 exercicis, 42 de la PAU d'altres comunitats", es: "PDF · 60 ejercicios, 42 de la PAU de otras comunidades", en: "PDF · 60 exercises, 42 from other regions' PAU exams" }, url: "materials/2batx-ccss/t2-fitxa-exercicis.pdf", download: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 60 exercicis", es: "PDF · Soluciones de los 60 ejercicios", en: "PDF · Solutions to all 60 exercises" }, url: "materials/2batx-ccss/t2-fitxa-solucions.pdf", download: true, date: "2026-10-26" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u2-sistemes.html", es: "materials/2batx-ccss/casio-u2-sistemes-es.html" } }
        ]
      },
      {
        // prova global de les unitats 1 i 2: estrella com el Resum teòric (no compta com a unitat) i blau més fosc (block: "algg")
        num: "★",
        ill: "global", block: "algg",
        title: { va: "Global d'Àlgebra", es: "Global de Álgebra", en: "Algebra block test" },
        items: [
          { type: "notes", title: { va: "Presentació-resum: mapa conceptual i errors típics", es: "Presentación-resumen: mapa conceptual y errores típicos", en: "Summary slides: concept map and common mistakes" }, desc: { va: "17 diapositives amb tot l'important de les unitats 1 i 2", es: "17 diapositivas con todo lo importante de las unidades 1 y 2", en: "17 slides with everything important from units 1 and 2" }, url: "materials/2batx-ccss/global-algebra-resum-diapositives.html", date: "2026-11-03" },
          { type: "exercises", title: { va: "Selecció d'exercicis PAU", es: "Selección de ejercicios PAU", en: "Selected PAU exercises" }, desc: { va: "19 exercicis resolts de la PAU 2026 d'11 comunitats, amb tot el bloc", es: "19 ejercicios resueltos de la PAU 2026 de 11 comunidades, con todo el bloque", en: "19 solved 2026 PAU exercises from 11 regions, covering the whole block" }, url: "materials/2batx-ccss/global-algebra-pau.html", date: "2026-11-03" },
          { type: "exam", title: { va: "Prova global tipus PAU", es: "Prueba global tipo PAU", en: "PAU-style block test" }, desc: { va: "4 problemes de les unitats 1 i 2 amb solucions i criteris de correcció", es: "4 problemas de las unidades 1 y 2 con soluciones y criterios de corrección", en: "4 problems on units 1 and 2 with solutions and marking criteria" }, url: "materials/2batx-ccss/global-algebra-prova-model1.html", date: "2026-11-03" }
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
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u3-programacio-lineal.html", es: "materials/2batx-ccss/casio-u3-programacio-lineal-es.html" } }
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
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u4-limits-continuitat.html", es: "materials/2batx-ccss/casio-u4-limits-continuitat-es.html" }, date: "2026-10-28" }
        ]
      },
      {
        ill: "derivades", block: "an",
        title: { va: "Càlcul de derivades. Derivabilitat d'una funció", es: "Cálculo de derivadas. Derivabilidad de una función", en: "Computing derivatives. Differentiability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t5-derivades.html", date: "2026-10-25" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 48 exercicis, 28 enunciats de la PAU d'altres comunitats", es: "PDF · 48 ejercicios, 28 enunciados de la PAU de otras comunidades", en: "PDF · 48 exercises, 28 items from other regions' PAU exams" }, url: "materials/2batx-ccss/t5-fitxa-exercicis.pdf", download: true, date: "2026-10-25" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 48 exercicis", es: "PDF · Soluciones de los 48 ejercicios", en: "PDF · Solutions to all 48 exercises" }, url: "materials/2batx-ccss/t5-fitxa-solucions.pdf", download: true, hidden: true, date: "2026-10-25" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "5 exercicis resolts de la PAU valenciana (2001–2026)", es: "5 ejercicios resueltos de la PAU valenciana (2001–2026)", en: "5 solved past Valencian PAU exercises (2001–2026)" }, url: { va: "materials/2batx-ccss/pau-u5-derivades.html", es: "materials/2batx-ccss/pau-u5-derivades-es.html" }, date: "2026-10-28" },
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
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "34 exercicis resolts de la PAU valenciana (2006–2026)", es: "34 ejercicios resueltos de la PAU valenciana (2006–2026)", en: "34 solved past Valencian PAU exercises (2006–2026)" }, url: { va: "materials/2batx-ccss/pau-u7-representacio-funcions.html", es: "materials/2batx-ccss/pau-u7-representacio-funcions-es.html" }, date: "2026-10-28" },
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
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "5 exercicis resolts de la PAU valenciana (2000–2026)", es: "5 ejercicios resueltos de la PAU valenciana (2000–2026)", en: "5 solved past Valencian PAU exercises (2000–2026)" }, url: { va: "materials/2batx-ccss/pau-u10-binomial-normal.html", es: "materials/2batx-ccss/pau-u10-binomial-normal-es.html" }, date: "2026-10-27" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: "materials/2batx-ccss/casio-u10-binomial-normal.html", date: "2026-10-28" }
        ]
      }
    ]
  }
};
