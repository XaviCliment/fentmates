#!/usr/bin/env python3
"""Pàgina PAU de probabilitat de 2n Batx MII (unitat 10) a partir del recull de l'IES Vermellar
(«Exercicis d'estadística i probabilitat de la selectivitat», Comunitat Valenciana 2023-2026, 13 exercicis, pp. 61-64).

- pr.txt: enunciats en l'ordre del recull ("## P | Convocatòria").
- sol.py: solucions pas a pas (S[número del recull] -> HTML), amb fraccions exactes i la binomial, comprovades amb ck()
  (fa servir les eines de ../../pr/comu.py, les mateixes que les pàgines PAU de probabilitat de CCSS).
Ús (des de l'arrel del repositori):  python3 _eines/pau/mii/pr/build.py
Només tematitza la pàgina que genera (no crida el aplica.py complet).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..')); sys.path.insert(0, os.path.join(ROOT, '_eines', 'tema'))
from build_pau import parse, write_pages  # noqa: E402
from aplica import aplica_fitxer  # noqa: E402
import sol  # noqa: E402

OUT = os.path.join(ROOT, 'materials', '2batx-mii')
items = parse(os.path.join(HERE, 'pr.txt'))
assert len(items) == 13, len(items)
for i, e in enumerate(items):
    e['num'] = i + 1
    e['s'] = sol.S[e['num']]
FN = 'pau-u10-probabilitat.html'
MII = {"SUBJECT": "Matemàtiques II", "COLOR": "#8064a1", "COURSE_URL": "2batx-mii.html",
       "COURSE": "2n Batxillerat MII", "RANGE": "2023–2026", "FIRST": "2023"}
write_pages(OUT, [(FN, '10', 'Probabilitat', items, '#8064a1')], MII)
p = os.path.join(OUT, FN); s = open(p, encoding='utf-8').read()
# el recull només té exercicis de 2023 a 2026: deixem només el filtre «Tots»
a = s.index('var PERIODS = ['); b = s.index('];', a) + 2
s = s[:a] + 'var PERIODS = [["tots", "Tots", 0, 9999]];' + s[b:]
CSS = ('<style>.sol-body .steps > li, .sol-body .res, .ex p, .parts li { overflow-x: auto; overflow-y: hidden; position: relative; }'
       ' .ex .katex-display { overflow-x: auto; overflow-y: hidden; } .ex .tbl table th, .ex .tbl table td { padding: 4px 10px; }</style>\n</head>')
open(p, 'w', encoding='utf-8').write(s.replace('</head>', CSS, 1))
aplica_fitxer(p)
print(len(sol.comu.CHK), 'comprovacions correctes')
