#!/usr/bin/env python3
"""Pàgines d'exercicis PAU de geometria de 2n Batx MII (unitats 3 i 4).

geo.txt: enunciats del recull de l'IES Vermellar (R = unitat 3, rectes i plans; D = unitat 4, problemes mètrics).
sol_geo.txt: solucions, generat per sol_geo.py.
Ús (des de l'arrel del repositori):
    python3 _eines/pau/mii/sol_geo.py && python3 _eines/pau/mii/build_geo.py
Només tematitza les dues pàgines que genera (no crida el aplica.py complet).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "_eines", "tema"))
from build_pau import parse, parse_sol, attach_sol, write_pages  # noqa: E402
from aplica import aplica_fitxer  # noqa: E402

OUT = os.path.join(ROOT, "materials", "2batx-mii")
MII = {"SUBJECT": "Matemàtiques II", "COLOR": "#f79645", "COURSE_URL": "2batx-mii.html",
       "COURSE": "2n Batxillerat MII", "RANGE": "1999–2026", "FIRST": "1999"}

geo = parse(os.path.join(HERE, "geo.txt"))
sol = parse_sol(os.path.join(HERE, "sol_geo.txt"))
attach_sol(geo, sol)
if sol:
    print("AVÍS: solucions sense exercici:", sorted(sol))
PAGES = [
    ("pau-u3-rectes-plans.html", "3", "Vectors, rectes i plans", [e for e in geo if e["k"] == "R"]),
    ("pau-u4-problemes-metrics.html", "4", "Problemes mètrics", [e for e in geo if e["k"] == "D"]),
]
write_pages(OUT, PAGES, MII)
for fn, *_ in PAGES:
    p = os.path.join(OUT, fn)
    s = open(p, encoding="utf-8").read().replace('"1999–1999"', '"1999"')
    open(p, "w", encoding="utf-8").write(s)
    aplica_fitxer(p)
