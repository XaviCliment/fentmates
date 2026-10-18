/* ==========================================================
   RACÓ PAU — data de l'examen i exàmens d'anys anteriors.

   date:      dia i hora d'inici de les proves PAU
              (format "AAAA-MM-DDTHH:MM:00+02:00", hora d'estiu)
   confirmed: posa true quan la data siga oficial
   exams:     per a cada any i convocatòria ("ord" o "ext"),
              enllaç a l'examen i a les solucions (Drive, PDF...).
              Si l'enllaç està buit, apareix "Pròximament".
   ========================================================== */

window.PAU = {
  date: "2027-06-01T09:00:00+02:00",
  confirmed: true,

  exams: [
    { year: 2026, conv: "ord", exam: "", solutions: "" },
    { year: 2026, conv: "ext", exam: "", solutions: "" },
    { year: 2025, conv: "ord", exam: "", solutions: "" },
    { year: 2025, conv: "ext", exam: "", solutions: "" },
    { year: 2024, conv: "ord", exam: "", solutions: "" },
    { year: 2024, conv: "ext", exam: "", solutions: "" },
    { year: 2023, conv: "ord", exam: "", solutions: "" },
    { year: 2023, conv: "ext", exam: "", solutions: "" }
  ]
};
