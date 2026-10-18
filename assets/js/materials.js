/* ==========================================================
   MATERIALS — ací és on afiges el contingut de cada curs.

   Cada material té:
     type:  "notes" (apunts) | "exercises" (exercicis) | "video" (vídeo)
            | "resource" (recurs/enllaç) | "exam" (examen)
     title: text o bé { va: "...", es: "...", en: "..." }
     desc:  (opcional) igual que title
     date:  (opcional) "AAAA-MM-DD" -> durant uns dies es marca com a "Nou"
     url:   ruta al fitxer (p. ex. "materials/3eso/t1-apunts.pdf")
            o enllaç (YouTube, GeoGebra, Drive...). Si està buit -> "Pròximament".

   Als títols pots posar fórmules en LaTeX entre $...$ (doblant les barres: \\frac).
   Els enllaços de Google Drive funcionen directament (compartits com "Qualsevol amb l'enllaç").
   Els vídeos de YouTube s'obrin dins de la pàgina automàticament.
   Una unitat pot portar num: "★" (o un altre símbol) per a seccions especials
   que no compten com a unitat numerada (p. ex. el Resum teòric).
   Per afegir un curs nou: copia un bloc de LEVELS, canvia la clau
   i crea una pàgina .html com 3eso.html amb data-level="clau-nova".
   ========================================================== */

/* Dades de contacte (apareixen a l'inici i al peu de pàgina) */
window.SITE = {
  email: "xavicliment@gmail.com",
  x: "xavier_climent",
  linkedin: "https://www.linkedin.com/in/xavier-climent-balaguer-5679a4155",
  newDays: 14          // dies que un material es marca com a "Nou"
};

window.LEVELS = {
  "3eso": {
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
          { type: "exercises", title: { va: "Fitxa d'exercicis 1", es: "Ficha de ejercicios 1", en: "Worksheet 1" }, url: "" },
          { type: "video", title: { va: "Fraccions: operacions combinades", es: "Fracciones: operaciones combinadas", en: "Fractions: combined operations" }, url: "" }
        ]
      },
      {
        title: { va: "Nombres reals", es: "Números reales", en: "Real numbers" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/3eso/t2-nombres-reals.html", date: "2026-10-18" }
        ]
      },
      {
        title: { va: "Polinomis", es: "Polinomios", en: "Polynomials" },
        items: [
          { type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "" },
          { type: "resource", date: "2026-10-15", title: { va: "GeoGebra: identitats notables $(a+b)^2$", es: "GeoGebra: identidades notables $(a+b)^2$", en: "GeoGebra: special products $(a+b)^2$" }, url: "https://www.geogebra.org" }
        ]
      },
      {
        title: { va: "Equacions i sistemes", es: "Ecuaciones y sistemas", en: "Equations and systems" },
        items: [
          { type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "" },
          { type: "exercises", title: { va: "Problemes amb equacions", es: "Problemas con ecuaciones", en: "Equation word problems" }, url: "" }
        ]
      }
    ]
  },

  "2batx-ccss": {
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
          { type: "exercises", title: { va: "Exercicis tipus PAU", es: "Ejercicios tipo PAU", en: "Exam-style exercises" }, url: "" }
        ]
      },
      {
        title: { va: "Sistemes d'equacions lineals", es: "Sistemas de ecuaciones lineales", en: "Systems of linear equations" },
        items: [
          { type: "notes", title: { va: "Apunts interactius de la unitat", es: "Apuntes interactivos de la unidad", en: "Interactive unit notes" }, url: "materials/2batx-ccss/t2-sistemes-equacions.html", date: "2026-10-18" }
        ]
      },
      {
        title: { va: "Programació lineal", es: "Programación lineal", en: "Linear programming" },
        items: [
          { type: "notes", title: { va: "Apunts de la unitat", es: "Apuntes de la unidad", en: "Unit notes" }, url: "" },
          { type: "video", title: { va: "Resolució gràfica pas a pas", es: "Resolución gráfica paso a paso", en: "Graphical method step by step" }, url: "" }
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
