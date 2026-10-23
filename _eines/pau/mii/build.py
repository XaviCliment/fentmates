#!/usr/bin/env python3
"""Genera els materials d'àlgebra de 2n Batx MII (unitats 1 i 2).

- Pàgines d'exercicis PAU a partir de alg.txt (enunciats) i sol.txt (solucions, generat per sol_mii.py).
- Apunts interactius: còpia dels de 2n Batx CCSS, canviant només el curs i l'enllaç de tornada.

Ús (des de l'arrel del repositori):
    python3 _eines/pau/mii/sol_mii.py && python3 _eines/pau/mii/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.dirname(HERE))
from build_pau import parse, parse_sol, attach_sol, write_pages  # noqa: E402

OUT = os.path.join(ROOT, "materials", "2batx-mii")
MII = {"SUBJECT": "Matemàtiques II", "COLOR": "#4e81bd", "COURSE_URL": "2batx-mii.html",
       "COURSE": "2n Batxillerat MII", "RANGE": "1997–2026", "FIRST": "1997"}

alg = parse(os.path.join(HERE, "alg.txt"))
# alguns exercicis del recull no estan en ordre cronològic
alg.sort(key=lambda e: (e["y"], e["m"]))
sol = parse_sol(os.path.join(HERE, "sol.txt"))
attach_sol(alg, sol)
if sol:
    print("AVÍS: solucions sense exercici:", sorted(sol))
write_pages(OUT, [
    ("pau-u1-matrius.html", "1", "Matrius i determinants", [e for e in alg if e["k"] == "M"]),
    ("pau-u2-sistemes.html", "2", "Sistemes d'equacions lineals", [e for e in alg if e["k"] == "S"]),
], MII)

# Apunts i guies de calculadora: els mateixos que CCSS
REPL = [
    ("2batx-ccss.html", "2batx-mii.html"),
    ("2n Batxillerat CCSS II", "2n Batxillerat MII"),
    ("2º Bachillerato CCSS II", "2º Bachillerato MII"),
    ("2nd Baccalaureate, Social Sciences II", "2nd Baccalaureate, Maths II"),
    ("2nd Baccalaureate (Social Sciences)", "2nd Baccalaureate Maths II"),
    ("2n de Batxillerat CCSS", "2n de Batxillerat MII"),
    ("2n Batxillerat CCSS", "2n Batxillerat MII"),
    ("2º Bachillerato CCSS", "2º Bachillerato MII"),
]
for fn in ("t1-matrius-determinants.html", "t2-sistemes-equacions.html",
           "casio-u1-matrius.html", "casio-u2-sistemes.html"):
    s = open(os.path.join(ROOT, "materials", "2batx-ccss", fn), encoding="utf-8").read()
    for a, b in REPL:
        s = s.replace(a, b)
    assert "CCSS" not in s and "Social Sciences" not in s, fn
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(s)
    print(fn, "copiat")
