#!/usr/bin/env python3
"""Genera sol_geo.txt: solucions pas a pas dels exercicis PAU de geometria de 2n Batx MII.

Els exercicis es numeren com en el recull de l'IES Vermellar (1-116, ordre de geo.txt).
Tots els càlculs es fan amb fraccions exactes (geolib.py) i es comproven amb ck().
Ús (des de l'arrel del repositori):
    python3 _eines/pau/mii/sol_geo.py && python3 _eines/pau/mii/build_geo.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from build_pau import parse  # noqa: E402
from geolib import *  # noqa: E402,F401,F403
import geolib  # noqa: E402

EX = parse(os.path.join(HERE, "geo.txt"))
KEY = {}
_seen = {}
for i, e in enumerate(EX, 1):
    k = (e["k"], e["conv"])
    _seen[k] = _seen.get(k, 0) + 1
    KEY[i] = (e["k"], e["conv"], _seen[k])

OUT = {}


def sol(num, html):
    assert num not in OUT, num
    h = html.strip().replace(r"\approx " + EXACT, "=").replace(r"\approx" + EXACT, "=").replace(EXACT, "")
    OUT[num] = mathsafe(h)


L = r"\lambda"
M_ = r"\mu"

for f in ("sol_g1.py", "sol_g2.py", "sol_g3.py"):
    p = os.path.join(HERE, f)
    if os.path.exists(p):
        exec(open(p, encoding="utf-8").read())

missing = [i for i in KEY if i not in OUT]
blocks = ["## %s | %s | %d\n%s" % (KEY[i] + (OUT[i],)) for i in sorted(OUT)]
open(os.path.join(HERE, "sol_geo.txt"), "w", encoding="utf-8").write(
    "Solucions dels exercicis PAU de geometria de 2n Batx MII. FITXER GENERAT per sol_geo.py: no l'editeu a mà.\n\n"
    + "\n\n".join(blocks) + "\n")
print(len(OUT), "solucions,", geolib.CHK[0], "comprovacions")
if missing:
    print("FALTEN:", missing)
