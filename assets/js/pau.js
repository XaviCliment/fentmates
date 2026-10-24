/* ==========================================================
   RACÓ PAU — data de l'examen i exàmens d'anys anteriors.

   date:      dia i hora d'inici de les proves PAU
              (format "AAAA-MM-DDTHH:MM:00+02:00", hora d'estiu)
   confirmed: posa true quan la data siga oficial
   exams:     exàmens de Matemàtiques CCSS; examsMII: de Matemàtiques II.
              Per a cada any i convocatòria ("ord" o "ext"),
              enllaç a l'examen i als criteris de qualificació (PDF a materials/pau/).
              Si l'enllaç està buit, apareix "Pròximament".
   ========================================================== */

window.PAU = {
  date: "2027-06-01T09:00:00+02:00",
  confirmed: true,

  exams: [
    { year: 2026, conv: "ord", exam: "materials/pau/pau-2026-ord-examen.pdf", criteria: "materials/pau/pau-2026-ord-criteris.pdf" },
    { year: 2026, conv: "ext", exam: "materials/pau/pau-2026-ext-examen.pdf", criteria: "materials/pau/pau-2026-ext-criteris.pdf" },
    { year: 2025, conv: "ord", exam: "materials/pau/pau-2025-ord-examen.pdf", criteria: "materials/pau/pau-2025-ord-criteris.pdf" },
    { year: 2025, conv: "ext", exam: "materials/pau/pau-2025-ext-examen.pdf", criteria: "materials/pau/pau-2025-ext-criteris.pdf" },
    { year: 2024, conv: "ord", exam: "materials/pau/pau-2024-ord-examen.pdf", criteria: "materials/pau/pau-2024-ord-criteris.pdf" },
    { year: 2024, conv: "ext", exam: "materials/pau/pau-2024-ext-examen.pdf", criteria: "materials/pau/pau-2024-ext-criteris.pdf" },
    { year: 2023, conv: "ord", exam: "materials/pau/pau-2023-ord-examen.pdf", criteria: "materials/pau/pau-2023-ord-criteris.pdf" },
    { year: 2023, conv: "ext", exam: "materials/pau/pau-2023-ext-examen.pdf", criteria: "materials/pau/pau-2023-ext-criteris.pdf" }
  ],

  examsMII: [
    { year: 2026, conv: "ord", exam: "materials/pau/mii-2026-ord-examen.pdf", criteria: "materials/pau/mii-2026-ord-criteris.pdf" },
    { year: 2026, conv: "ext", exam: "materials/pau/mii-2026-ext-examen.pdf", criteria: "materials/pau/mii-2026-ext-criteris.pdf" },
    { year: 2025, conv: "ord", exam: "materials/pau/mii-2025-ord-examen.pdf", criteria: "materials/pau/mii-2025-ord-criteris.pdf" },
    { year: 2025, conv: "ext", exam: "materials/pau/mii-2025-ext-examen.pdf", criteria: "materials/pau/mii-2025-ext-criteris.pdf" },
    { year: 2024, conv: "ord", exam: "materials/pau/mii-2024-ord-examen.pdf", criteria: "materials/pau/mii-2024-ord-criteris.pdf" },
    { year: 2024, conv: "ext", exam: "materials/pau/mii-2024-ext-examen.pdf", criteria: "materials/pau/mii-2024-ext-criteris.pdf" },
    { year: 2023, conv: "ord", exam: "materials/pau/mii-2023-ord-examen.pdf", criteria: "materials/pau/mii-2023-ord-criteris.pdf" },
    { year: 2023, conv: "ext", exam: "materials/pau/mii-2023-ext-examen.pdf", criteria: "materials/pau/mii-2023-ext-criteris.pdf" }
  ]
};
