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
   Cursos amb byBlock: true -> les targetes de les unitats s'agrupen per bloc, amb un títol
   per bloc; les unitats de block: "all" (Resum teòric) van a dalt en una franja ampla.
   Cursos amb sections: true -> dins de cada unitat, els materials es reparteixen en
   columnes: Apunts (notes, video, resource), Exercicis (exercises), PAU (exercises amb
   «PAU» al títol i exam) i Calculadora (calc).
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
    byBlock: true,    // unitats agrupades per bloc (Àlgebra, Anàlisi…)
    sections: true,   // dins de cada unitat: columnes Apunts / Exercicis / PAU / Calculadora
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
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 70 exercicis graduats per nivells de dificultat", es: "PDF · 70 ejercicios graduados por niveles de dificultad", en: "PDF · 70 exercises graded by difficulty" }, url: { va: "materials/1eso/t2-fitxa-exercicis.pdf", es: "materials/1eso/t2-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-21" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 70 exercicis", es: "PDF · Soluciones de los 70 ejercicios", en: "PDF · Solutions to all 70 exercises" }, url: { va: "materials/1eso/t2-fitxa-solucions.pdf", es: "materials/1eso/t2-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-21" }
        ]
      },
      {
        ill: "enters", block: "ari",
        title: { va: "Nombres enters", es: "Números enteros", en: "Integers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t3-nombres-enters.html", date: "2026-10-22" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis graduats per nivells de dificultat", es: "PDF · 54 ejercicios graduados por niveles de dificultad", en: "PDF · 54 exercises graded by difficulty" }, url: { va: "materials/1eso/t3-fitxa-exercicis.pdf", es: "materials/1eso/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-22" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: { va: "materials/1eso/t3-fitxa-solucions.pdf", es: "materials/1eso/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-22" }
        ]
      },
      {
        ill: "fraccions", block: "ari",
        title: { va: "Fraccions", es: "Fracciones", en: "Fractions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t4-fraccions.html", date: "2026-10-22" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 70 exercicis graduats per nivells de dificultat", es: "PDF · 70 ejercicios graduados por niveles de dificultad", en: "PDF · 70 exercises graded by difficulty" }, url: { va: "materials/1eso/t4-fitxa-exercicis.pdf", es: "materials/1eso/t4-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-22" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 70 exercicis", es: "PDF · Soluciones de los 70 ejercicios", en: "PDF · Solutions to all 70 exercises" }, url: { va: "materials/1eso/t4-fitxa-solucions.pdf", es: "materials/1eso/t4-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-22" }
        ]
      },
      {
        ill: "proporcionalitat", block: "ari",
        title: { va: "Proporcionalitat i percentatges. Nombres decimals", es: "Proporcionalidad y porcentajes. Números decimales", en: "Proportionality and percentages. Decimal numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t5-proporcionalitat-decimals.html", date: "2026-11-01" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 69 exercicis graduats per nivells de dificultat", es: "PDF · 69 ejercicios graduados por niveles de dificultad", en: "PDF · 69 exercises graded by difficulty" }, url: { va: "materials/1eso/t5-fitxa-exercicis.pdf", es: "materials/1eso/t5-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-01" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 69 exercicis", es: "PDF · Soluciones de los 69 ejercicios", en: "PDF · Solutions to all 69 exercises" }, url: { va: "materials/1eso/t5-fitxa-solucions.pdf", es: "materials/1eso/t5-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-01" }
        ]
      },
      {
        ill: "equacions", block: "alg",
        title: { va: "Introducció a l'àlgebra. Equacions de 1r grau", es: "Introducción al álgebra. Ecuaciones de 1.er grado", en: "Introduction to algebra. First-degree equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t6-algebra-equacions.html", date: "2026-11-01" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 68 exercicis graduats per nivells de dificultat", es: "PDF · 68 ejercicios graduados por niveles de dificultad", en: "PDF · 68 exercises graded by difficulty" }, url: { va: "materials/1eso/t6-fitxa-exercicis.pdf", es: "materials/1eso/t6-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-01" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 68 exercicis", es: "PDF · Soluciones de los 68 ejercicios", en: "PDF · Solutions to all 68 exercises" }, url: { va: "materials/1eso/t6-fitxa-solucions.pdf", es: "materials/1eso/t6-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-01" }
        ]
      },
      {
        ill: "angles", block: "geo",
        title: { va: "Geometria bàsica del pla", es: "Geometría básica del plano", en: "Basic plane geometry" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t7-geometria-pla.html", date: "2026-11-02" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 67 exercicis graduats per nivells de dificultat", es: "PDF · 67 ejercicios graduados por niveles de dificultad", en: "PDF · 67 exercises graded by difficulty" }, url: { va: "materials/1eso/t7-fitxa-exercicis.pdf", es: "materials/1eso/t7-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 67 exercicis", es: "PDF · Soluciones de los 67 ejercicios", en: "PDF · Solutions to all 67 exercises" }, url: { va: "materials/1eso/t7-fitxa-solucions.pdf", es: "materials/1eso/t7-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-02" }
        ]
      },
      {
        ill: "arees", block: "geo",
        title: { va: "Àrees i perímetres", es: "Áreas y perímetros", en: "Area and perimeter" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t8-arees-perimetres.html", date: "2026-11-02" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 87 exercicis graduats per nivells de dificultat", es: "PDF · 87 ejercicios graduados por niveles de dificultad", en: "PDF · 87 exercises graded by difficulty" }, url: { va: "materials/1eso/t8-fitxa-exercicis.pdf", es: "materials/1eso/t8-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 87 exercicis", es: "PDF · Soluciones de los 87 ejercicios", en: "PDF · Solutions to all 87 exercises" }, url: { va: "materials/1eso/t8-fitxa-solucions.pdf", es: "materials/1eso/t8-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-02" }
        ]
      },
      {
        ill: "lineal", block: "an",
        title: { va: "Gràfics de funcions", es: "Gráficas de funciones", en: "Graphs of functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t9-grafics-funcions.html", date: "2026-11-02" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 61 exercicis graduats per nivells de dificultat", es: "PDF · 61 ejercicios graduados por niveles de dificultad", en: "PDF · 61 exercises graded by difficulty" }, url: { va: "materials/1eso/t9-fitxa-exercicis.pdf", es: "materials/1eso/t9-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 61 exercicis", es: "PDF · Soluciones de los 61 ejercicios", en: "PDF · Solutions to all 61 exercises" }, url: { va: "materials/1eso/t9-fitxa-solucions.pdf", es: "materials/1eso/t9-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-02" }
        ]
      },
      {
        ill: "estadistica", block: "pr",
        title: { va: "Estadística", es: "Estadística", en: "Statistics" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1eso/t10-estadistica.html", date: "2026-11-02" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 65 exercicis graduats per nivells de dificultat", es: "PDF · 65 ejercicios graduados por niveles de dificultad", en: "PDF · 65 exercises graded by difficulty" }, url: { va: "materials/1eso/t10-fitxa-exercicis.pdf", es: "materials/1eso/t10-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 65 exercicis", es: "PDF · Soluciones de los 65 ejercicios", en: "PDF · Solutions to all 65 exercises" }, url: { va: "materials/1eso/t10-fitxa-solucions.pdf", es: "materials/1eso/t10-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-02" }
        ]
      }
    ]
  },

  "2eso": {
    color: "#3b82f6",
    symbol: "%",
    stage: "eso",
    cards: true,
    byBlock: true,    // unitats agrupades per bloc (Àlgebra, Anàlisi…)
    sections: true,   // dins de cada unitat: columnes Apunts / Exercicis / PAU / Calculadora
    name: { va: "2n ESO", es: "2º ESO", en: "2nd ESO (Year 8)" },
    desc: {
      va: "Fraccions i decimals, percentatges, àlgebra inicial, equacions i geometria.",
      es: "Fracciones y decimales, porcentajes, álgebra inicial, ecuaciones y geometría.",
      en: "Fractions and decimals, percentages, early algebra, equations and geometry."
    },
    units: [
      {
        ill: "enters", block: "ari",
        title: { va: "Nombres naturals i enters", es: "Números naturales y enteros", en: "Natural numbers and integers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t1-naturals-enters.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 51 exercicis graduats per nivells de dificultat", es: "PDF · 51 ejercicios graduados por niveles de dificultad", en: "PDF · 50 exercises graded by difficulty" }, url: { va: "materials/2eso/t1-fitxa-exercicis.pdf", es: "materials/2eso/t1-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 51 exercicis", es: "PDF · Soluciones de los 51 ejercicios", en: "PDF · Solutions to all 51 exercises" }, url: { va: "materials/2eso/t1-fitxa-solucions.pdf", es: "materials/2eso/t1-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "fraccions", block: "ari",
        title: { va: "Decimals i fraccions", es: "Decimales y fracciones", en: "Decimals and fractions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t2-decimals-fraccions.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 66 exercicis graduats per nivells de dificultat", es: "PDF · 66 ejercicios graduados por niveles de dificultad", en: "PDF · 66 exercises graded by difficulty" }, url: { va: "materials/2eso/t2-fitxa-exercicis.pdf", es: "materials/2eso/t2-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 66 exercicis", es: "PDF · Soluciones de los 66 ejercicios", en: "PDF · Solutions to all 66 exercises" }, url: { va: "materials/2eso/t2-fitxa-solucions.pdf", es: "materials/2eso/t2-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "polinomis", block: "alg",
        title: { va: "Introducció a l'àlgebra. Polinomis", es: "Introducción al álgebra. Polinomios", en: "Introduction to algebra. Polynomials" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t3-algebra-polinomis.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 63 exercicis graduats per nivells de dificultat", es: "PDF · 63 ejercicios graduados por niveles de dificultad", en: "PDF · 63 exercises graded by difficulty" }, url: { va: "materials/2eso/t3-fitxa-exercicis.pdf", es: "materials/2eso/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 63 exercicis", es: "PDF · Soluciones de los 63 ejercicios", en: "PDF · Solutions to all 63 exercises" }, url: { va: "materials/2eso/t3-fitxa-solucions.pdf", es: "materials/2eso/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "equacions", block: "alg",
        title: { va: "Equacions de 1r i 2n grau", es: "Ecuaciones de 1.er y 2.º grado", en: "Linear and quadratic equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t4-equacions.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 70 exercicis graduats per nivells de dificultat", es: "PDF · 70 ejercicios graduados por niveles de dificultad", en: "PDF · 70 exercises graded by difficulty" }, url: { va: "materials/2eso/t4-fitxa-exercicis.pdf", es: "materials/2eso/t4-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 70 exercicis", es: "PDF · Soluciones de los 70 ejercicios", en: "PDF · Solutions to all 70 exercises" }, url: { va: "materials/2eso/t4-fitxa-solucions.pdf", es: "materials/2eso/t4-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions", es: "Sistemas de ecuaciones", en: "Simultaneous equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t5-sistemes-equacions.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 53 exercicis graduats per nivells de dificultat", es: "PDF · 53 ejercicios graduados por niveles de dificultad", en: "PDF · 53 exercises graded by difficulty" }, url: { va: "materials/2eso/t5-fitxa-exercicis.pdf", es: "materials/2eso/t5-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 53 exercicis", es: "PDF · Soluciones de los 53 ejercicios", en: "PDF · Solutions to all 53 exercises" }, url: { va: "materials/2eso/t5-fitxa-solucions.pdf", es: "materials/2eso/t5-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "proporcionalitat", block: "ari",
        title: { va: "Proporcionalitat i percentatges", es: "Proporcionalidad y porcentajes", en: "Proportionality and percentages" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t6-proporcionalitat-percentatges.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 57 exercicis graduats per nivells de dificultat", es: "PDF · 57 ejercicios graduados por niveles de dificultad", en: "PDF · 57 exercises graded by difficulty" }, url: { va: "materials/2eso/t6-fitxa-exercicis.pdf", es: "materials/2eso/t6-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 57 exercicis", es: "PDF · Soluciones de los 57 ejercicios", en: "PDF · Solutions to all 57 exercises" }, url: { va: "materials/2eso/t6-fitxa-solucions.pdf", es: "materials/2eso/t6-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "pitagores", block: "geo",
        title: { va: "Teorema de Pitàgores. Perímetres i àrees", es: "Teorema de Pitágoras. Perímetros y áreas", en: "Pythagoras' theorem. Perimeters and areas" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t7-pitagores-perimetres-arees.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 81 exercicis graduats per nivells de dificultat", es: "PDF · 81 ejercicios graduados por niveles de dificultad", en: "PDF · 81 exercises graded by difficulty" }, url: { va: "materials/2eso/t7-fitxa-exercicis.pdf", es: "materials/2eso/t7-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 81 exercicis", es: "PDF · Soluciones de los 81 ejercicios", en: "PDF · Solutions to all 81 exercises" }, url: { va: "materials/2eso/t7-fitxa-solucions.pdf", es: "materials/2eso/t7-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "tales", block: "geo",
        title: { va: "Semblança. Teorema de Tales", es: "Semejanza. Teorema de Tales", en: "Similarity. Thales' theorem" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t8-semblanca-tales.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 56 exercicis graduats per nivells de dificultat", es: "PDF · 56 ejercicios graduados por niveles de dificultad", en: "PDF · 56 exercises graded by difficulty" }, url: { va: "materials/2eso/t8-fitxa-exercicis.pdf", es: "materials/2eso/t8-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 56 exercicis", es: "PDF · Soluciones de los 56 ejercicios", en: "PDF · Solutions to all 56 exercises" }, url: { va: "materials/2eso/t8-fitxa-solucions.pdf", es: "materials/2eso/t8-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "cossos", block: "geo",
        title: { va: "Cossos geomètrics. Àrees i volums", es: "Cuerpos geométricos. Áreas y volúmenes", en: "Solids. Surface area and volume" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t9-cossos-geometrics.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 63 exercicis graduats per nivells de dificultat", es: "PDF · 63 ejercicios graduados por niveles de dificultad", en: "PDF · 63 exercises graded by difficulty" }, url: { va: "materials/2eso/t9-fitxa-exercicis.pdf", es: "materials/2eso/t9-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 63 exercicis", es: "PDF · Soluciones de los 63 ejercicios", en: "PDF · Solutions to all 63 exercises" }, url: { va: "materials/2eso/t9-fitxa-solucions.pdf", es: "materials/2eso/t9-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        ill: "grafiques", block: "an",
        title: { va: "Funcions", es: "Funciones", en: "Functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t10-funcions.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 59 exercicis graduats per nivells de dificultat", es: "PDF · 59 ejercicios graduados por niveles de dificultad", en: "PDF · 59 exercises graded by difficulty" }, url: { va: "materials/2eso/t10-fitxa-exercicis.pdf", es: "materials/2eso/t10-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 59 exercicis", es: "PDF · Soluciones de los 59 ejercicios", en: "PDF · Solutions to all 59 exercises" }, url: { va: "materials/2eso/t10-fitxa-solucions.pdf", es: "materials/2eso/t10-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      },
      {
        num: "11",
        ill: "probabilitat", block: "pr",
        title: { va: "Atzar i probabilitat", es: "Azar y probabilidad", en: "Chance and probability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2eso/t11-atzar-probabilitat.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis graduats per nivells de dificultat", es: "PDF · 54 ejercicios graduados por niveles de dificultad", en: "PDF · 54 exercises graded by difficulty" }, url: { va: "materials/2eso/t11-fitxa-exercicis.pdf", es: "materials/2eso/t11-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: { va: "materials/2eso/t11-fitxa-solucions.pdf", es: "materials/2eso/t11-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      }
    ]
  },

  "3eso": {
    stage: "eso",
    cards: true,
    sections: true,   // dins de cada unitat: columnes Apunts / Exercicis / PAU / Calculadora
    byBlock: true,    // unitats agrupades per bloc (Àlgebra, Anàlisi…)
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
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 46 exercicis", es: "PDF · Soluciones de los 46 ejercicios", en: "PDF · Solutions to all 46 exercises" }, url: { va: "materials/3eso/t2-fitxa-solucions.pdf", es: "materials/3eso/t2-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-18" },
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
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 86 exercicis graduats per nivells de dificultat", es: "PDF · 86 ejercicios graduados por niveles de dificultad", en: "PDF · 86 exercises graded by difficulty" }, url: { va: "materials/3eso/t3-fitxa-exercicis.pdf", es: "materials/3eso/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-20" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 86 exercicis", es: "PDF · Soluciones de los 86 ejercicios", en: "PDF · Solutions to all 86 exercises" }, url: { va: "materials/3eso/t3-fitxa-solucions.pdf", es: "materials/3eso/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-20" },
          { type: "exercises", title: { va: "Fitxa de repàs per a l'examen", es: "Ficha de repaso para el examen", en: "Exam review worksheet" }, desc: { va: "PDF · 11 exercicis de tota la unitat (sense interés compost, mescles ni moviments)", es: "PDF · 11 ejercicios de toda la unidad (sin interés compuesto, mezclas ni móviles)", en: "PDF · 11 exercises covering the unit (no compound interest, mixtures or motion)" }, url: { va: "materials/3eso/t3-fitxa-repas.pdf", es: "materials/3eso/t3-fitxa-repas-es.pdf" }, download: true, date: "2026-11-17" },
          { type: "exercises", title: { va: "Solucions de la fitxa de repàs", es: "Soluciones de la ficha de repaso", en: "Review worksheet solutions" }, desc: { va: "PDF · Solucions pas a pas per a autocorregir-te", es: "PDF · Soluciones paso a paso para autocorregirte", en: "PDF · Step-by-step solutions to self-check" }, url: { va: "materials/3eso/t3-fitxa-repas-solucions.pdf", es: "materials/3eso/t3-fitxa-repas-solucions-es.pdf" }, download: true, date: "2026-11-17" }
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
    byBlock: true,    // unitats agrupades per bloc (Àlgebra, Anàlisi…)
    sections: true,   // dins de cada unitat: columnes Apunts / Exercicis / PAU / Calculadora
    name: { va: "4t ESO Matemàtiques A", es: "4º ESO Matemáticas A", en: "4th ESO Maths A" },
    desc: {
      va: "Matemàtiques aplicades: nombres, àlgebra, funcions, estadística i probabilitat.",
      es: "Matemáticas aplicadas: números, álgebra, funciones, estadística y probabilidad.",
      en: "Applied maths: numbers, algebra, functions, statistics and probability."
    },
    units: [
      {
        num: "1",
        ill: "fraccions", block: "ari",
        title: { va: "Nombres naturals, enters i fraccionaris", es: "Números naturales, enteros y fraccionarios", en: "Natural numbers, integers and fractions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t1-naturals-enters-fraccions.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 62 exercicis graduats per nivells de dificultat", es: "PDF · 62 ejercicios graduados por niveles de dificultad", en: "PDF · 62 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t1-fitxa-exercicis.pdf", es: "materials/4eso-a/t1-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 62 exercicis", es: "PDF · Soluciones de los 62 ejercicios", en: "PDF · Solutions to all 62 exercises" }, url: { va: "materials/4eso-a/t1-fitxa-solucions.pdf", es: "materials/4eso-a/t1-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      },
      {
        num: "2",
        ill: "reals", block: "ari",
        title: { va: "Nombres reals", es: "Números reales", en: "Real numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t2-nombres-reals.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 57 exercicis graduats per nivells de dificultat", es: "PDF · 57 ejercicios graduados por niveles de dificultad", en: "PDF · 57 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t2-fitxa-exercicis.pdf", es: "materials/4eso-a/t2-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 57 exercicis", es: "PDF · Soluciones de los 57 ejercicios", en: "PDF · Solutions to all 57 exercises" }, url: { va: "materials/4eso-a/t2-fitxa-solucions.pdf", es: "materials/4eso-a/t2-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      },
      {
        num: "3",
        ill: "polinomis", block: "alg",
        title: { va: "Polinomis", es: "Polinomios", en: "Polynomials" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t3-polinomis.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 62 exercicis graduats per nivells de dificultat", es: "PDF · 62 ejercicios graduados por niveles de dificultad", en: "PDF · 62 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t3-fitxa-exercicis.pdf", es: "materials/4eso-a/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 62 exercicis", es: "PDF · Soluciones de los 62 ejercicios", en: "PDF · Solutions to all 62 exercises" }, url: { va: "materials/4eso-a/t3-fitxa-solucions.pdf", es: "materials/4eso-a/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      },
      {
        num: "4",
        ill: "equacions", block: "alg",
        title: { va: "Equacions", es: "Ecuaciones", en: "Equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t4-equacions.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 51 exercicis graduats per nivells de dificultat", es: "PDF · 51 ejercicios graduados por niveles de dificultad", en: "PDF · 51 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t4-fitxa-exercicis.pdf", es: "materials/4eso-a/t4-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 51 exercicis", es: "PDF · Soluciones de los 51 ejercicios", en: "PDF · Solutions to all 51 exercises" }, url: { va: "materials/4eso-a/t4-fitxa-solucions.pdf", es: "materials/4eso-a/t4-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      },
      {
        num: "5",
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions i inequacions", es: "Sistemas de ecuaciones e inecuaciones", en: "Systems of equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t5-sistemes-inequacions.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 45 exercicis graduats per nivells de dificultat", es: "PDF · 45 ejercicios graduados por niveles de dificultad", en: "PDF · 45 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t5-fitxa-exercicis.pdf", es: "materials/4eso-a/t5-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 45 exercicis", es: "PDF · Soluciones de los 45 ejercicios", en: "PDF · Solutions to all 45 exercises" }, url: { va: "materials/4eso-a/t5-fitxa-solucions.pdf", es: "materials/4eso-a/t5-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      },
      {
        num: "6",
        ill: "grafiques", block: "an",
        title: { va: "Funcions. Característiques", es: "Funciones. Características", en: "Functions and their features" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t6-funcions.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 50 exercicis graduats per nivells de dificultat", es: "PDF · 50 ejercicios graduados por niveles de dificultad", en: "PDF · 50 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t6-fitxa-exercicis.pdf", es: "materials/4eso-a/t6-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 50 exercicis", es: "PDF · Soluciones de los 50 ejercicios", en: "PDF · Solutions to all 50 exercises" }, url: { va: "materials/4eso-a/t6-fitxa-solucions.pdf", es: "materials/4eso-a/t6-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      },
      {
        num: "7",
        ill: "grafiques", block: "an",
        title: { va: "Funcions elementals", es: "Funciones elementales", en: "Elementary functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t7-funcions-elementals.html", date: "2026-11-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 55 exercicis graduats per nivells de dificultat", es: "PDF · 55 ejercicios graduados por niveles de dificultad", en: "PDF · 55 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t7-fitxa-exercicis.pdf", es: "materials/4eso-a/t7-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-18" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 55 exercicis", es: "PDF · Soluciones de los 55 ejercicios", en: "PDF · Solutions to all 55 exercises" }, url: { va: "materials/4eso-a/t7-fitxa-solucions.pdf", es: "materials/4eso-a/t7-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-18" }
        ]
      },
      {
        num: "8",
        ill: "tales", block: "geo",
        title: { va: "Semblança. Aplicacions", es: "Semejanza. Aplicaciones", en: "Similarity. Applications" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t8-semblanca-aplicacions.html", date: "2026-11-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 76 exercicis graduats per nivells de dificultat", es: "PDF · 76 ejercicios graduados por niveles de dificultad", en: "PDF · 76 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t8-fitxa-exercicis.pdf", es: "materials/4eso-a/t8-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-18" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 76 exercicis", es: "PDF · Soluciones de los 76 ejercicios", en: "PDF · Solutions to all 76 exercises" }, url: { va: "materials/4eso-a/t8-fitxa-solucions.pdf", es: "materials/4eso-a/t8-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-18" }
        ]
      },
      {
        num: "9",
        ill: "estadistica", block: "pr",
        title: { va: "Estadística Unidimensional", es: "Estadística Unidimensional", en: "One-Variable Statistics" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t9-estadistica.html", date: "2026-11-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis graduats per nivells de dificultat", es: "PDF · 54 ejercicios graduados por niveles de dificultad", en: "PDF · 54 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t9-fitxa-exercicis.pdf", es: "materials/4eso-a/t9-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-18" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: { va: "materials/4eso-a/t9-fitxa-solucions.pdf", es: "materials/4eso-a/t9-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-18" }
        ]
      },
      {
        num: "10",
        ill: "regressio", block: "pr",
        title: { va: "Estadística bidimensional", es: "Estadística bidimensional", en: "Bivariate Statistics" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t10-estadistica-bidimensional.html", date: "2026-11-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 41 exercicis graduats per nivells de dificultat", es: "PDF · 41 ejercicios graduados por niveles de dificultad", en: "PDF · 41 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t10-fitxa-exercicis.pdf", es: "materials/4eso-a/t10-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-18" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 41 exercicis", es: "PDF · Soluciones de los 41 ejercicios", en: "PDF · Solutions to all 41 exercises" }, url: { va: "materials/4eso-a/t10-fitxa-solucions.pdf", es: "materials/4eso-a/t10-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-18" }
        ]
      },
      {
        num: "11",
        ill: "probabilitat", block: "pr",
        title: { va: "Probabilitat", es: "Probabilidad", en: "Probability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-a/t11-probabilitat.html", date: "2026-11-18" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 56 exercicis graduats per nivells de dificultat", es: "PDF · 56 ejercicios graduados por niveles de dificultad", en: "PDF · 56 exercises graded by difficulty" }, url: { va: "materials/4eso-a/t11-fitxa-exercicis.pdf", es: "materials/4eso-a/t11-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-18" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 56 exercicis", es: "PDF · Soluciones de los 56 ejercicios", en: "PDF · Solutions to all 56 exercises" }, url: { va: "materials/4eso-a/t11-fitxa-solucions.pdf", es: "materials/4eso-a/t11-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-18" }
        ]
      }
    ]
  },

  "4eso-b": {
    color: "#6d28d9",
    symbol: "√",
    stage: "eso",
    cards: true,
    byBlock: true,    // unitats agrupades per bloc (Àlgebra, Anàlisi…)
    sections: true,   // dins de cada unitat: columnes Apunts / Exercicis / PAU / Calculadora
    name: { va: "4t ESO Matemàtiques B", es: "4º ESO Matemáticas B", en: "4th ESO Maths B" },
    desc: {
      va: "Radicals i logaritmes, àlgebra, trigonometria, geometria analítica, funcions, recompte i probabilitat.",
      es: "Radicales y logaritmos, álgebra, trigonometría, geometría analítica, funciones, recuento y probabilidad.",
      en: "Radicals and logarithms, algebra, trigonometry, coordinate geometry, functions, counting and probability."
    },
    units: [
      {
        num: "1",
        ill: "reals", block: "ari",
        title: { va: "Nombres reals", es: "Números reales", en: "Real numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t1-nombres-reals.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 36 exercicis graduats per nivells de dificultat", es: "PDF · 36 ejercicios graduados por niveles de dificultad", en: "PDF · 36 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t1-fitxa-exercicis.pdf", es: "materials/4eso-b/t1-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 36 exercicis", es: "PDF · Soluciones de los 36 ejercicios", en: "PDF · Solutions to all 36 exercises" }, url: { va: "materials/4eso-b/t1-fitxa-solucions.pdf", es: "materials/4eso-b/t1-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "2",
        ill: "polinomis", block: "alg",
        title: { va: "Polinomis i fraccions algebraiques", es: "Polinomios y fracciones algebraicas", en: "Polynomials and algebraic fractions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t2-polinomis-fraccions.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 35 exercicis graduats per nivells de dificultat", es: "PDF · 35 ejercicios graduados por niveles de dificultad", en: "PDF · 35 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t2-fitxa-exercicis.pdf", es: "materials/4eso-b/t2-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 35 exercicis", es: "PDF · Soluciones de los 35 ejercicios", en: "PDF · Solutions to all 35 exercises" }, url: { va: "materials/4eso-b/t2-fitxa-solucions.pdf", es: "materials/4eso-b/t2-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "3",
        ill: "equacions", block: "alg",
        title: { va: "Equacions i inequacions", es: "Ecuaciones e inecuaciones", en: "Equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t3-equacions-inequacions.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 41 exercicis graduats per nivells de dificultat", es: "PDF · 41 ejercicios graduados por niveles de dificultad", en: "PDF · 41 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t3-fitxa-exercicis.pdf", es: "materials/4eso-b/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 41 exercicis", es: "PDF · Soluciones de los 41 ejercicios", en: "PDF · Solutions to all 41 exercises" }, url: { va: "materials/4eso-b/t3-fitxa-solucions.pdf", es: "materials/4eso-b/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "4",
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions i inequacions", es: "Sistemas de ecuaciones e inecuaciones", en: "Systems of equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t4-sistemes-inequacions.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 31 exercicis graduats per nivells de dificultat", es: "PDF · 31 ejercicios graduados por niveles de dificultad", en: "PDF · 31 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t4-fitxa-exercicis.pdf", es: "materials/4eso-b/t4-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 31 exercicis", es: "PDF · Soluciones de los 31 ejercicios", en: "PDF · Solutions to all 31 exercises" }, url: { va: "materials/4eso-b/t4-fitxa-solucions.pdf", es: "materials/4eso-b/t4-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "5",
        ill: "trigonometria", block: "geo",
        title: { va: "Trigonometria", es: "Trigonometría", en: "Trigonometry" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t5-trigonometria.html", date: "2026-11-14" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 64 exercicis graduats per nivells de dificultat", es: "PDF · 64 ejercicios graduados por niveles de dificultad", en: "PDF · 64 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t5-fitxa-exercicis.pdf", es: "materials/4eso-b/t5-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-14" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 64 exercicis", es: "PDF · Soluciones de los 64 ejercicios", en: "PDF · Solutions to all 64 exercises" }, url: { va: "materials/4eso-b/t5-fitxa-solucions.pdf", es: "materials/4eso-b/t5-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-14" }
        ]
      },
      {
        num: "6",
        ill: "geometria", block: "geo",
        title: { va: "Vectors i rectes", es: "Vectores y rectas", en: "Vectors and lines" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t6-vectors-rectes.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 77 exercicis graduats per nivells de dificultat", es: "PDF · 77 ejercicios graduados por niveles de dificultad", en: "PDF · 77 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t6-fitxa-exercicis.pdf", es: "materials/4eso-b/t6-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 77 exercicis", es: "PDF · Soluciones de los 77 ejercicios", en: "PDF · Solutions to all 77 exercises" }, url: { va: "materials/4eso-b/t6-fitxa-solucions.pdf", es: "materials/4eso-b/t6-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        num: "7",
        ill: "grafiques", block: "an",
        title: { va: "Estudi de funcions", es: "Estudio de funciones", en: "Studying functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t7-estudi-funcions.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 40 exercicis graduats per nivells de dificultat", es: "PDF · 40 ejercicios graduados por niveles de dificultad", en: "PDF · 40 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t7-fitxa-exercicis.pdf", es: "materials/4eso-b/t7-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 40 exercicis", es: "PDF · Soluciones de los 40 ejercicios", en: "PDF · Solutions to all 40 exercises" }, url: { va: "materials/4eso-b/t7-fitxa-solucions.pdf", es: "materials/4eso-b/t7-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        num: "8",
        ill: "grafiques", block: "an",
        title: { va: "Funcions elementals", es: "Funciones elementales", en: "Elementary functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t8-funcions-elementals.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 45 exercicis graduats per nivells de dificultat", es: "PDF · 45 ejercicios graduados por niveles de dificultad", en: "PDF · 45 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t8-fitxa-exercicis.pdf", es: "materials/4eso-b/t8-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 45 exercicis", es: "PDF · Soluciones de los 45 ejercicios", en: "PDF · Solutions to all 45 exercises" }, url: { va: "materials/4eso-b/t8-fitxa-solucions.pdf", es: "materials/4eso-b/t8-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      },
      {
        num: "9",
        ill: "probabilitat", block: "pr",
        title: { va: "Tècniques de recompte. Probabilitat", es: "Técnicas de recuento. Probabilidad", en: "Counting techniques. Probability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/4eso-b/t9-recompte-probabilitat.html", date: "2026-11-15" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 79 exercicis graduats per nivells de dificultat", es: "PDF · 79 ejercicios graduados por niveles de dificultad", en: "PDF · 79 exercises graded by difficulty" }, url: { va: "materials/4eso-b/t9-fitxa-exercicis.pdf", es: "materials/4eso-b/t9-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-15" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 79 exercicis", es: "PDF · Soluciones de los 79 ejercicios", en: "PDF · Solutions to all 79 exercises" }, url: { va: "materials/4eso-b/t9-fitxa-solucions.pdf", es: "materials/4eso-b/t9-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-15" }
        ]
      }
    ]
  },

  "1batx-mi": {
    color: "#9b1c1c",
    symbol: "sin",
    stage: "batx",
    cards: true,
    byBlock: true,    // unitats agrupades per bloc (Àlgebra, Anàlisi…)
    sections: true,   // dins de cada unitat: columnes Apunts / Exercicis / PAU / Calculadora
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
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis graduats per nivells de dificultat", es: "PDF · 54 ejercicios graduados por niveles de dificultad", en: "PDF · 54 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t1-fitxa-exercicis.pdf", es: "materials/1batx-mi/t1-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: { va: "materials/1batx-mi/t1-fitxa-solucions.pdf", es: "materials/1batx-mi/t1-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-10" }
        ]
      },
      {
        num: "2",
        ill: "polinomis", block: "alg",
        title: { va: "Àlgebra. Equacions i inequacions", es: "Álgebra. Ecuaciones e inecuaciones", en: "Algebra. Equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t2-algebra.html", date: "2026-11-11" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 71 exercicis graduats per nivells de dificultat", es: "PDF · 71 ejercicios graduados por niveles de dificultad", en: "PDF · 71 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t2-fitxa-exercicis.pdf", es: "materials/1batx-mi/t2-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-11" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 71 exercicis", es: "PDF · Soluciones de los 71 ejercicios", en: "PDF · Solutions to all 71 exercises" }, url: { va: "materials/1batx-mi/t2-fitxa-solucions.pdf", es: "materials/1batx-mi/t2-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-11" }
        ]
      },
      {
        num: "3",
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions i inequacions", es: "Sistemas de ecuaciones e inecuaciones", en: "Systems of equations and inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t3-sistemes-inequacions.html", date: "2026-11-11" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 32 exercicis graduats per nivells de dificultat", es: "PDF · 32 ejercicios graduados por niveles de dificultad", en: "PDF · 32 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t3-fitxa-exercicis.pdf", es: "materials/1batx-mi/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-11" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 32 exercicis", es: "PDF · Soluciones de los 32 ejercicios", en: "PDF · Solutions to all 32 exercises" }, url: { va: "materials/1batx-mi/t3-fitxa-solucions.pdf", es: "materials/1batx-mi/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-11" }
        ]
      },
      {
        num: "4",
        ill: "geometria", block: "geo",
        title: { va: "Geometria analítica en el pla", es: "Geometría analítica en el plano", en: "Coordinate geometry in the plane" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t4-geometria-pla.html", date: "2026-10-29" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 61 exercicis graduats per nivells de dificultat", es: "PDF · 61 ejercicios graduados por niveles de dificultad", en: "PDF · 61 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t4-fitxa-exercicis.pdf", es: "materials/1batx-mi/t4-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-29" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 61 exercicis", es: "PDF · Soluciones de los 61 ejercicios", en: "PDF · Solutions to all 61 exercises" }, url: { va: "materials/1batx-mi/t4-fitxa-solucions.pdf", es: "materials/1batx-mi/t4-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-29" }
        ]
      },
      {
        num: "5",
        ill: "trigonometria", block: "geo",
        title: { va: "Trigonometria", es: "Trigonometría", en: "Trigonometry" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t5-trigonometria.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 73 exercicis graduats per nivells de dificultat", es: "PDF · 73 ejercicios graduados por niveles de dificultad", en: "PDF · 73 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t5-fitxa-exercicis.pdf", es: "materials/1batx-mi/t5-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 73 exercicis", es: "PDF · Soluciones de los 73 ejercicios", en: "PDF · Solutions to all 73 exercises" }, url: { va: "materials/1batx-mi/t5-fitxa-solucions.pdf", es: "materials/1batx-mi/t5-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-10" }
        ]
      },
      {
        num: "6",
        ill: "grafiques", block: "an",
        title: { va: "Estudi de funcions", es: "Estudio de funciones", en: "Studying functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t6-estudi-funcions.html", date: "2026-11-11" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 30 exercicis graduats per nivells de dificultat", es: "PDF · 30 ejercicios graduados por niveles de dificultad", en: "PDF · 30 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t6-fitxa-exercicis.pdf", es: "materials/1batx-mi/t6-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-11" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 30 exercicis", es: "PDF · Soluciones de los 30 ejercicios", en: "PDF · Solutions to all 30 exercises" }, url: { va: "materials/1batx-mi/t6-fitxa-solucions.pdf", es: "materials/1batx-mi/t6-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-11" }
        ]
      },
      {
        num: "7",
        ill: "grafiques", block: "an",
        title: { va: "Funcions elementals", es: "Funciones elementales", en: "Elementary functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t7-funcions-elementals.html", date: "2026-11-11" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 35 exercicis graduats per nivells de dificultat", es: "PDF · 35 ejercicios graduados por niveles de dificultad", en: "PDF · 35 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t7-fitxa-exercicis.pdf", es: "materials/1batx-mi/t7-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-11" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 35 exercicis", es: "PDF · Soluciones de los 35 ejercicios", en: "PDF · Solutions to all 35 exercises" }, url: { va: "materials/1batx-mi/t7-fitxa-solucions.pdf", es: "materials/1batx-mi/t7-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-11" }
        ]
      },
      {
        num: "8",
        ill: "limits", block: "an",
        title: { va: "Límits i continuïtat", es: "Límites y continuidad", en: "Limits and continuity" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t8-limits-continuitat.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 36 exercicis graduats per nivells de dificultat", es: "PDF · 36 ejercicios graduados por niveles de dificultad", en: "PDF · 36 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t8-fitxa-exercicis.pdf", es: "materials/1batx-mi/t8-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 36 exercicis", es: "PDF · Soluciones de los 36 ejercicios", en: "PDF · Solutions to all 36 exercises" }, url: { va: "materials/1batx-mi/t8-fitxa-solucions.pdf", es: "materials/1batx-mi/t8-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "9",
        ill: "derivades", block: "an",
        title: { va: "Derivades i aplicacions", es: "Derivadas y aplicaciones", en: "Derivatives and applications" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t9-derivades.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 31 exercicis graduats per nivells de dificultat", es: "PDF · 31 ejercicios graduados por niveles de dificultad", en: "PDF · 31 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t9-fitxa-exercicis.pdf", es: "materials/1batx-mi/t9-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 31 exercicis", es: "PDF · Soluciones de los 31 ejercicios", en: "PDF · Solutions to all 31 exercises" }, url: { va: "materials/1batx-mi/t9-fitxa-solucions.pdf", es: "materials/1batx-mi/t9-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-13" }
        ]
      },
      {
        num: "10",
        ill: "estadistica", block: "pr",
        title: { va: "Estadística", es: "Estadística", en: "Statistics" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-mi/t10-estadistica.html", date: "2026-11-13" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 34 exercicis graduats per nivells de dificultat", es: "PDF · 34 ejercicios graduados por niveles de dificultad", en: "PDF · 34 exercises graded by difficulty" }, url: { va: "materials/1batx-mi/t10-fitxa-exercicis.pdf", es: "materials/1batx-mi/t10-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-13" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 34 exercicis", es: "PDF · Soluciones de los 34 ejercicios", en: "PDF · Solutions to all 34 exercises" }, url: { va: "materials/1batx-mi/t10-fitxa-solucions.pdf", es: "materials/1batx-mi/t10-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-13" }
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
    cards: true,
    units: [
      {
        num: "3",
        ill: "pl", block: "alg",
        title: { va: "Inequacions i sistemes d'inequacions", es: "Inecuaciones y sistemas de inecuaciones", en: "Inequalities and systems of inequalities" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/1batx-ccss/t3-inequacions.html", date: "2026-11-16" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 31 exercicis graduats per nivells de dificultat", es: "PDF · 31 ejercicios graduados por niveles de dificultad", en: "PDF · 31 exercises graded by difficulty" }, url: { va: "materials/1batx-ccss/t3-fitxa-exercicis.pdf", es: "materials/1batx-ccss/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-16" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 31 exercicis", es: "PDF · Soluciones de los 31 ejercicios", en: "PDF · Solutions to all 31 exercises" }, url: { va: "materials/1batx-ccss/t3-fitxa-solucions.pdf", es: "materials/1batx-ccss/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-16" }
        ]
      }
    ]
  },

  "2batx-mii": {
    color: "#1e6b47",
    symbol: "∂",
    stage: "batx",
    pau: true,
    cards: true,
    byBlock: true,    // unitats agrupades per bloc (Àlgebra, Anàlisi…)
    sections: true,   // dins de cada unitat: columnes Apunts / Exercicis / PAU / Calculadora
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
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "59 exercicis resolts de la PAU valenciana (1999–2026)", es: "59 ejercicios resueltos de la PAU valenciana (1999–2026)", en: "59 solved past Valencian PAU exercises (1999–2026)" }, url: { va: "materials/2batx-mii/pau-u1-matrius.html", es: "materials/2batx-mii/pau-u1-matrius-es.html" }, date: "2026-10-23" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 88 exercicis graduats per nivells de dificultat", es: "PDF · 88 ejercicios graduados por niveles de dificultad", en: "PDF · 88 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t1-fitxa-exercicis.pdf", es: "materials/2batx-mii/t1-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-29" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 88 exercicis", es: "PDF · Soluciones de los 88 ejercicios", en: "PDF · Solutions to all 88 exercises" }, url: { va: "materials/2batx-mii/t1-fitxa-solucions.pdf", es: "materials/2batx-mii/t1-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-29" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-mii/casio-u1-matrius.html", es: "materials/2batx-mii/casio-u1-matrius-es.html" }, date: "2026-10-23" }
        ]
      },
      {
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions lineals", es: "Sistemas de ecuaciones lineales", en: "Systems of linear equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t2-sistemes-equacions.html", date: "2026-10-23" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "64 exercicis resolts de la PAU valenciana (1997–2026)", es: "64 ejercicios resueltos de la PAU valenciana (1997–2026)", en: "64 solved past Valencian PAU exercises (1997–2026)" }, url: { va: "materials/2batx-mii/pau-u2-sistemes.html", es: "materials/2batx-mii/pau-u2-sistemes-es.html" }, date: "2026-10-23" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 62 exercicis graduats per nivells de dificultat", es: "PDF · 62 ejercicios graduados por niveles de dificultad", en: "PDF · 62 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t2-fitxa-exercicis.pdf", es: "materials/2batx-mii/t2-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 62 exercicis", es: "PDF · Soluciones de los 62 ejercicios", en: "PDF · Solutions to all 62 exercises" }, url: { va: "materials/2batx-mii/t2-fitxa-solucions.pdf", es: "materials/2batx-mii/t2-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-02" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-mii/casio-u2-sistemes.html", es: "materials/2batx-mii/casio-u2-sistemes-es.html" }, date: "2026-10-23" }
        ]
      },
      {
        ill: "geometria", block: "geo",
        title: { va: "Vectors i aplicacions. Rectes, plans i feixos de plans", es: "Vectores y aplicaciones. Rectas, planos y haces de planos", en: "Vectors and applications. Lines, planes and pencils of planes" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t3-vectors-rectes-plans.html", date: "2026-10-29" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "30 exercicis resolts de la PAU valenciana (1999–2026)", es: "30 ejercicios resueltos de la PAU valenciana (1999–2026)", en: "30 solved past Valencian PAU exercises (1999–2026)" }, url: { va: "materials/2batx-mii/pau-u3-rectes-plans.html", es: "materials/2batx-mii/pau-u3-rectes-plans-es.html" }, date: "2026-11-08" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 92 exercicis graduats per nivells de dificultat", es: "PDF · 92 ejercicios graduados por niveles de dificultad", en: "PDF · 92 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t3-fitxa-exercicis.pdf", es: "materials/2batx-mii/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-02" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 92 exercicis", es: "PDF · Soluciones de los 92 ejercicios", en: "PDF · Solutions to all 92 exercises" }, url: { va: "materials/2batx-mii/t3-fitxa-solucions.pdf", es: "materials/2batx-mii/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-02" }
        ]
      },
      {
        ill: "geometria", block: "geo",
        title: { va: "Problemes mètrics", es: "Problemas métricos", en: "Metric problems" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t4-problemes-metrics.html", date: "2026-11-08" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "86 exercicis resolts de la PAU valenciana (1999–2026)", es: "86 ejercicios resueltos de la PAU valenciana (1999–2026)", en: "86 solved past Valencian PAU exercises (1999–2026)" }, url: { va: "materials/2batx-mii/pau-u4-problemes-metrics.html", es: "materials/2batx-mii/pau-u4-problemes-metrics-es.html" }, date: "2026-11-08" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 108 exercicis graduats per nivells de dificultat", es: "PDF · 108 ejercicios graduados por niveles de dificultad", en: "PDF · 108 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t4-fitxa-exercicis.pdf", es: "materials/2batx-mii/t4-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-08" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 108 exercicis", es: "PDF · Soluciones de los 108 ejercicios", en: "PDF · Solutions to all 108 exercises" }, url: { va: "materials/2batx-mii/t4-fitxa-solucions.pdf", es: "materials/2batx-mii/t4-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-08" }
        ]
      },
      {
        ill: "limits", block: "an",
        title: { va: "Límits i continuïtat", es: "Límites y continuidad", en: "Limits and continuity" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t5-limits-continuitat.html", date: "2026-11-08" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "24 exercicis resolts de la PAU valenciana (2005–2026)", es: "24 ejercicios resueltos de la PAU valenciana (2005–2026)", en: "24 solved past Valencian PAU exercises (2005–2026)" }, url: { va: "materials/2batx-mii/pau-u5-limits-continuitat.html", es: "materials/2batx-mii/pau-u5-limits-continuitat-es.html" }, date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 106 exercicis graduats per nivells de dificultat", es: "PDF · 106 ejercicios graduados por niveles de dificultad", en: "PDF · 106 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t5-fitxa-exercicis.pdf", es: "materials/2batx-mii/t5-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-08" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 106 exercicis", es: "PDF · Soluciones de los 106 ejercicios", en: "PDF · Solutions to all 106 exercises" }, url: { va: "materials/2batx-mii/t5-fitxa-solucions.pdf", es: "materials/2batx-mii/t5-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-08" }
        ]
      },
      {
        ill: "derivades", block: "an",
        title: { va: "Càlcul de derivades. Derivabilitat d'una funció", es: "Cálculo de derivadas. Derivabilidad de una función", en: "Computing derivatives. Differentiability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t6-derivades.html", date: "2026-11-09" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "14 exercicis resolts de la PAU valenciana (2002–2018)", es: "14 ejercicios resueltos de la PAU valenciana (2002–2018)", en: "14 solved past Valencian PAU exercises (2002–2018)" }, url: { va: "materials/2batx-mii/pau-u6-derivades.html", es: "materials/2batx-mii/pau-u6-derivades-es.html" }, date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 71 exercicis graduats per nivells de dificultat", es: "PDF · 71 ejercicios graduados por niveles de dificultad", en: "PDF · 71 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t6-fitxa-exercicis.pdf", es: "materials/2batx-mii/t6-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-09" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 71 exercicis", es: "PDF · Soluciones de los 71 ejercicios", en: "PDF · Solutions to all 71 exercises" }, url: { va: "materials/2batx-mii/t6-fitxa-solucions.pdf", es: "materials/2batx-mii/t6-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-09" }
        ]
      },
      {
        ill: "aplicacions", block: "an",
        title: { va: "Aplicacions de la derivada", es: "Aplicaciones de la derivada", en: "Applications of the derivative" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t7-aplicacions-derivada.html", date: "2026-11-09" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "94 exercicis resolts de la PAU valenciana (2002–2026)", es: "94 ejercicios resueltos de la PAU valenciana (2002–2026)", en: "94 solved past Valencian PAU exercises (2002–2026)" }, url: { va: "materials/2batx-mii/pau-u7-aplicacions-derivada.html", es: "materials/2batx-mii/pau-u7-aplicacions-derivada-es.html" }, date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 93 exercicis graduats per nivells de dificultat", es: "PDF · 93 ejercicios graduados por niveles de dificultad", en: "PDF · 93 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t7-fitxa-exercicis.pdf", es: "materials/2batx-mii/t7-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-09" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 93 exercicis, amb gràfiques", es: "PDF · Soluciones de los 93 ejercicios, con gráficas", en: "PDF · Solutions to all 93 exercises, with graphs" }, url: { va: "materials/2batx-mii/t7-fitxa-solucions.pdf", es: "materials/2batx-mii/t7-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-09" }
        ]
      },
      {
        ill: "grafiques", block: "an",
        title: { va: "Representació gràfica de funcions", es: "Representación gráfica de funciones", en: "Graphing functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t8-representacio-funcions.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "16 exercicis resolts de la PAU valenciana (2011–2026)", es: "16 ejercicios resueltos de la PAU valenciana (2011–2026)", en: "16 solved past Valencian PAU exercises (2011–2026)" }, url: { va: "materials/2batx-mii/pau-u8-representacio-funcions.html", es: "materials/2batx-mii/pau-u8-representacio-funcions-es.html" }, date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 60 exercicis graduats per nivells de dificultat", es: "PDF · 60 ejercicios graduados por niveles de dificultad", en: "PDF · 60 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t8-fitxa-exercicis.pdf", es: "materials/2batx-mii/t8-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 60 exercicis, amb gràfiques", es: "PDF · Soluciones de los 60 ejercicios, con gráficas", en: "PDF · Solutions to all 60 exercises, with graphs" }, url: { va: "materials/2batx-mii/t8-fitxa-solucions.pdf", es: "materials/2batx-mii/t8-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-10" }
        ]
      },
      {
        ill: "integrals", block: "an",
        title: { va: "Integrals", es: "Integrales", en: "Integrals" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t9-integrals.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "57 exercicis resolts de la PAU valenciana (2002–2026)", es: "57 ejercicios resueltos de la PAU valenciana (2002–2026)", en: "57 solved past Valencian PAU exercises (2002–2026)" }, url: { va: "materials/2batx-mii/pau-u9-integrals.html", es: "materials/2batx-mii/pau-u9-integrals-es.html" }, date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 56 exercicis graduats per nivells de dificultat", es: "PDF · 56 ejercicios graduados por niveles de dificultad", en: "PDF · 56 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t9-fitxa-exercicis.pdf", es: "materials/2batx-mii/t9-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 56 exercicis, amb gràfiques", es: "PDF · Soluciones de los 56 ejercicios, con gráficas", en: "PDF · Solutions to all 56 exercises, with graphs" }, url: { va: "materials/2batx-mii/t9-fitxa-solucions.pdf", es: "materials/2batx-mii/t9-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-10" }
        ]
      },
      {
        ill: "probabilitat", block: "pr",
        title: { va: "Probabilitat", es: "Probabilidad", en: "Probability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-mii/t10-probabilitat.html", date: "2026-11-10" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "13 exercicis resolts de la PAU valenciana (2023–2026)", es: "13 ejercicios resueltos de la PAU valenciana (2023–2026)", en: "13 solved past Valencian PAU exercises (2023–2026)" }, url: { va: "materials/2batx-mii/pau-u10-probabilitat.html", es: "materials/2batx-mii/pau-u10-probabilitat-es.html" }, date: "2026-11-10" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 91 exercicis graduats per nivells de dificultat", es: "PDF · 91 ejercicios graduados por niveles de dificultad", en: "PDF · 91 exercises graded by difficulty" }, url: { va: "materials/2batx-mii/t10-fitxa-exercicis.pdf", es: "materials/2batx-mii/t10-fitxa-exercicis-es.pdf" }, download: true, date: "2026-11-10" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 91 exercicis, amb arbres i taules", es: "PDF · Soluciones de los 91 ejercicios, con árboles y tablas", en: "PDF · Solutions to all 91 exercises, with trees and tables" }, url: { va: "materials/2batx-mii/t10-fitxa-solucions.pdf", es: "materials/2batx-mii/t10-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-11-10" }
        ]
      }
    ]
  },

  "2batx-ccss": {
    stage: "batx",
    cards: true,
    byBlock: true,    // unitats agrupades per bloc (Àlgebra, Anàlisi…)
    sections: true,   // dins de cada unitat: columnes Apunts / Exercicis / PAU / Calculadora
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
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 50 exercicis graduats per nivells de dificultat", es: "PDF · 50 ejercicios graduados por niveles de dificultad", en: "PDF · 50 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t1-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t1-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 50 exercicis", es: "PDF · Soluciones de los 50 ejercicios", en: "PDF · Solutions to all 50 exercises" }, url: { va: "materials/2batx-ccss/t1-fitxa-solucions.pdf", es: "materials/2batx-ccss/t1-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-27" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u1-matrius.html", es: "materials/2batx-ccss/casio-u1-matrius-es.html" } }
        ]
      },
      {
        ill: "sistemes", block: "alg",
        title: { va: "Sistemes d'equacions lineals", es: "Sistemas de ecuaciones lineales", en: "Systems of linear equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t2-sistemes-equacions.html", date: "2026-10-18" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "68 exercicis de la PAU valenciana (1994–2026)", es: "68 ejercicios de la PAU valenciana (1994–2026)", en: "68 past Valencian PAU exercises (1994–2026)" }, url: { va: "materials/2batx-ccss/pau-u2-sistemes.html", es: "materials/2batx-ccss/pau-u2-sistemes-es.html" } },
          { type: "exam", title: { va: "Model d'examen tipus PAU", es: "Modelo de examen tipo PAU", en: "PAU-style mock exam" }, desc: { va: "4 problemes amb solucions i criteris de correcció", es: "4 problemas con soluciones y criterios de corrección", en: "4 problems with solutions and marking criteria" }, url: "materials/2batx-ccss/examen-u2-sistemes-model1.html", date: "2026-11-01" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 60 exercicis graduats per nivells de dificultat", es: "PDF · 60 ejercicios graduados por niveles de dificultad", en: "PDF · 60 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t2-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t2-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 60 exercicis", es: "PDF · Soluciones de los 60 ejercicios", en: "PDF · Solutions to all 60 exercises" }, url: { va: "materials/2batx-ccss/t2-fitxa-solucions.pdf", es: "materials/2batx-ccss/t2-fitxa-solucions-es.pdf" }, download: true, date: "2026-10-26" },
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
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "83 exercicis resolts de la PAU valenciana (1994–2026)", es: "83 ejercicios resueltos de la PAU valenciana (1994–2026)", en: "83 solved past Valencian PAU exercises (1994–2026)" }, url: { va: "materials/2batx-ccss/pau-u3-programacio-lineal.html", es: "materials/2batx-ccss/pau-u3-programacio-lineal-es.html" } },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 29 exercicis graduats per nivells de dificultat", es: "PDF · 29 ejercicios graduados por niveles de dificultad", en: "PDF · 29 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t3-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t3-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-25" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 29 exercicis", es: "PDF · Soluciones de los 29 ejercicios", en: "PDF · Solutions to all 29 exercises" }, url: { va: "materials/2batx-ccss/t3-fitxa-solucions.pdf", es: "materials/2batx-ccss/t3-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-25" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u3-programacio-lineal.html", es: "materials/2batx-ccss/casio-u3-programacio-lineal-es.html" } }
        ]
      },
      {
        ill: "limits", block: "an",
        title: { va: "Límits i continuïtat", es: "Límites y continuidad", en: "Limits and continuity" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t4-limits-continuitat.html", date: "2026-10-24" },
          { type: "notes", ill: "theory", title: { va: "Apunts de teoria en PDF", es: "Apuntes de teoría en PDF", en: "Theory notes (PDF)" }, desc: { va: "PDF · 21 pàgines per a llegir o imprimir", es: "PDF · 21 páginas para leer o imprimir", en: "PDF · 21 pages to read or print" }, url: "materials/2batx-ccss/t4-apunts-teoria.pdf", download: true, date: "2026-11-19" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 55 exercicis graduats per nivells de dificultat", es: "PDF · 55 ejercicios graduados por niveles de dificultad", en: "PDF · 55 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t4-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t4-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-24" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 55 exercicis", es: "PDF · Soluciones de los 55 ejercicios", en: "PDF · Solutions to all 55 exercises" }, url: { va: "materials/2batx-ccss/t4-fitxa-solucions.pdf", es: "materials/2batx-ccss/t4-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-24" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "26 exercicis resolts de la PAU valenciana (2002–2026)", es: "26 ejercicios resueltos de la PAU valenciana (2002–2026)", en: "26 solved past Valencian PAU exercises (2002–2026)" }, url: { va: "materials/2batx-ccss/pau-u4-limits-continuitat.html", es: "materials/2batx-ccss/pau-u4-limits-continuitat-es.html" }, date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u4-limits-continuitat.html", es: "materials/2batx-ccss/casio-u4-limits-continuitat-es.html" }, date: "2026-10-28" }
        ]
      },
      {
        ill: "derivades", block: "an",
        title: { va: "Càlcul de derivades. Derivabilitat d'una funció", es: "Cálculo de derivadas. Derivabilidad de una función", en: "Computing derivatives. Differentiability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t5-derivades.html", date: "2026-10-25" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 48 exercicis graduats per nivells de dificultat", es: "PDF · 48 ejercicios graduados por niveles de dificultad", en: "PDF · 48 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t5-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t5-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-25" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 48 exercicis", es: "PDF · Soluciones de los 48 ejercicios", en: "PDF · Solutions to all 48 exercises" }, url: { va: "materials/2batx-ccss/t5-fitxa-solucions.pdf", es: "materials/2batx-ccss/t5-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-25" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "5 exercicis resolts de la PAU valenciana (2001–2026)", es: "5 ejercicios resueltos de la PAU valenciana (2001–2026)", en: "5 solved past Valencian PAU exercises (2001–2026)" }, url: { va: "materials/2batx-ccss/pau-u5-derivades.html", es: "materials/2batx-ccss/pau-u5-derivades-es.html" }, date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u5-derivades.html", es: "materials/2batx-ccss/casio-u5-derivades-es.html" }, date: "2026-10-28" }
        ]
      },
      {
        ill: "aplicacions", block: "an",
        title: { va: "Aplicacions de la derivada", es: "Aplicaciones de la derivada", en: "Applications of the derivative" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t6-aplicacions-derivada.html", date: "2026-10-26" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 54 exercicis graduats per nivells de dificultat", es: "PDF · 54 ejercicios graduados por niveles de dificultad", en: "PDF · 54 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t6-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t6-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 54 exercicis", es: "PDF · Soluciones de los 54 ejercicios", en: "PDF · Solutions to all 54 exercises" }, url: { va: "materials/2batx-ccss/t6-fitxa-solucions.pdf", es: "materials/2batx-ccss/t6-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "54 exercicis resolts de la PAU valenciana (1997–2026)", es: "54 ejercicios resueltos de la PAU valenciana (1997–2026)", en: "54 solved past Valencian PAU exercises (1997–2026)" }, url: { va: "materials/2batx-ccss/pau-u6-aplicacions-derivada.html", es: "materials/2batx-ccss/pau-u6-aplicacions-derivada-es.html" }, date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u6-aplicacions-derivada.html", es: "materials/2batx-ccss/casio-u6-aplicacions-derivada-es.html" }, date: "2026-10-28" }
        ]
      },
      {
        ill: "grafiques", block: "an",
        title: { va: "Representació gràfica de funcions", es: "Representación gráfica de funciones", en: "Graphing functions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t7-representacio-funcions.html", date: "2026-10-26" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 38 exercicis graduats per nivells de dificultat", es: "PDF · 38 ejercicios graduados por niveles de dificultad", en: "PDF · 38 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t7-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t7-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 38 exercicis", es: "PDF · Soluciones de los 38 ejercicios", en: "PDF · Solutions to all 38 exercises" }, url: { va: "materials/2batx-ccss/t7-fitxa-solucions.pdf", es: "materials/2batx-ccss/t7-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-26" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "34 exercicis resolts de la PAU valenciana (2006–2026)", es: "34 ejercicios resueltos de la PAU valenciana (2006–2026)", en: "34 solved past Valencian PAU exercises (2006–2026)" }, url: { va: "materials/2batx-ccss/pau-u7-representacio-funcions.html", es: "materials/2batx-ccss/pau-u7-representacio-funcions-es.html" }, date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u7-representacio-funcions.html", es: "materials/2batx-ccss/casio-u7-representacio-funcions-es.html" }, date: "2026-10-28" }
        ]
      },
      {
        ill: "integrals", block: "an",
        title: { va: "Integrals", es: "Integrales", en: "Integrals" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t8-integrals.html", date: "2026-10-27" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 36 exercicis graduats per nivells de dificultat", es: "PDF · 36 ejercicios graduados por niveles de dificultad", en: "PDF · 36 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t8-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t8-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 36 exercicis", es: "PDF · Soluciones de los 36 ejercicios", en: "PDF · Solutions to all 36 exercises" }, url: { va: "materials/2batx-ccss/t8-fitxa-solucions.pdf", es: "materials/2batx-ccss/t8-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "26 exercicis resolts de la PAU valenciana (2001–2026)", es: "26 ejercicios resueltos de la PAU valenciana (2001–2026)", en: "26 solved past Valencian PAU exercises (2001–2026)" }, url: { va: "materials/2batx-ccss/pau-u8-integrals.html", es: "materials/2batx-ccss/pau-u8-integrals-es.html" }, date: "2026-10-28" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u8-integrals.html", es: "materials/2batx-ccss/casio-u8-integrals-es.html" }, date: "2026-10-28" }
        ]
      },
      {
        ill: "probabilitat", block: "pr",
        title: { va: "Probabilitat", es: "Probabilidad", en: "Probability" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t9-probabilitat.html", date: "2026-10-27" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 76 exercicis graduats per nivells de dificultat", es: "PDF · 76 ejercicios graduados por niveles de dificultad", en: "PDF · 76 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t9-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t9-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 76 exercicis", es: "PDF · Soluciones de los 76 ejercicios", en: "PDF · Solutions to all 76 exercises" }, url: { va: "materials/2batx-ccss/t9-fitxa-solucions.pdf", es: "materials/2batx-ccss/t9-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "100 exercicis resolts de la PAU valenciana (2000–2026)", es: "100 ejercicios resueltos de la PAU valenciana (2000–2026)", en: "100 solved past Valencian PAU exercises (2000–2026)" }, url: { va: "materials/2batx-ccss/pau-u9-probabilitat.html", es: "materials/2batx-ccss/pau-u9-probabilitat-es.html" }, date: "2026-10-27" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u9-probabilitat.html", es: "materials/2batx-ccss/casio-u9-probabilitat-es.html" }, date: "2026-10-28" }
        ]
      },
      {
        ill: "normal", block: "pr",
        title: { va: "Distribució binomial i normal", es: "Distribución binomial y normal", en: "Binomial and normal distributions" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t10-binomial-normal.html", date: "2026-10-27" },
          { type: "exercises", title: { va: "Fitxa d'exercicis per practicar", es: "Ficha de ejercicios para practicar", en: "Practice worksheet" }, desc: { va: "PDF · 53 exercicis graduats per nivells de dificultat", es: "PDF · 53 ejercicios graduados por niveles de dificultad", en: "PDF · 53 exercises graded by difficulty" }, url: { va: "materials/2batx-ccss/t10-fitxa-exercicis.pdf", es: "materials/2batx-ccss/t10-fitxa-exercicis-es.pdf" }, download: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Solucions de la fitxa d'exercicis", es: "Soluciones de la ficha de ejercicios", en: "Worksheet solutions" }, desc: { va: "PDF · Solucions dels 53 exercicis", es: "PDF · Soluciones de los 53 ejercicios", en: "PDF · Solutions to all 53 exercises" }, url: { va: "materials/2batx-ccss/t10-fitxa-solucions.pdf", es: "materials/2batx-ccss/t10-fitxa-solucions-es.pdf" }, download: true, hidden: true, date: "2026-10-27" },
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, desc: { va: "5 exercicis resolts de la PAU valenciana (2000–2026)", es: "5 ejercicios resueltos de la PAU valenciana (2000–2026)", en: "5 solved past Valencian PAU exercises (2000–2026)" }, url: { va: "materials/2batx-ccss/pau-u10-binomial-normal.html", es: "materials/2batx-ccss/pau-u10-binomial-normal-es.html" }, date: "2026-10-27" },
          { type: "calc", title: { va: "Amb la calculadora: pas a pas", es: "Con la calculadora: paso a paso", en: "With the calculator: step by step" }, desc: { va: "Casio ClassWiz fx-991SP CW", es: "Casio ClassWiz fx-991SP CW", en: "Casio ClassWiz fx-991SP CW" }, url: { va: "materials/2batx-ccss/casio-u10-binomial-normal.html", es: "materials/2batx-ccss/casio-u10-binomial-normal-es.html" }, date: "2026-10-28" }
        ]
      }
    ]
  }
};
