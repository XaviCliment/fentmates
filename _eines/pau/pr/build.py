#!/usr/bin/env python3
"""Genera les pàgines PAU de probabilitat (unitat 9) i de distribucions binomial i normal (unitat 10)
de 2n Batx CCSS a partir del dossier de selectivitat de la Comunitat Valenciana.

- pr.txt: enunciats ("## R | Convocatòria" probabilitat, "## B | Convocatòria" binomial i normal), transcrits del
  dossier «Exercicis de probabilitat de la selectivitat» (2000-2026) en el mateix ordre (keys.json: número del dossier
  -> [tipus, convocatòria, ordre dins de la convocatòria]).
- sol_u9a.py, sol_u9b.py, sol_u10.py: solucions pas a pas, calculades amb fraccions exactes i comprovades (ck).
Reutilitza parse() i write_pages() de ../build_pau.py, però no toca les pàgines de les unitats 1-3.
Ús (des de l'arrel del web):  python3 _eines/pau/pr/build.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '..', '..', 'tema'))
from build_pau import parse, write_pages, CCSS  # noqa: E402
from aplica import aplica_fitxer  # noqa: E402
import comu, sol_u9a, sol_u9b  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'materials', '2batx-ccss'))
items = parse(os.path.join(HERE, 'pr.txt'))
keys = {int(k): tuple(v) for k, v in json.load(open(os.path.join(HERE, 'keys.json'), encoding='utf-8')).items()}
sols = {**sol_u9a.S, **sol_u9b.S}
try:
    import sol_u10; sols.update(sol_u10.S)
except ImportError:
    pass
# enllaça cada solució amb el seu exercici (tipus, convocatòria i ordre dins de la convocatòria)
seen = {}
for e in items:
    k = (e['k'], e['conv']); seen[k] = seen.get(k, 0) + 1
    e['num'] = [n for n, v in keys.items() if v == (e['k'], e['conv'], seen[k])][0]
    if e['num'] in sols: e['s'] = sols[e['num']]
assert len(items) == 105
units = [('pau-u9-probabilitat.html', '9', 'Probabilitat', [e for e in items if e['k'] == 'R'], '#8064a1')]
if 'sol_u10' in sys.modules:
    units.append(('pau-u10-binomial-normal.html', '10', 'Distribució binomial i normal', [e for e in items if e['k'] == 'B'], '#8064a1'))
opts = dict(CCSS, RANGE='2000–2026', FIRST='2000')
write_pages(OUT, units, opts)
for u in units:
    p = os.path.join(OUT, u[0]); s = open(p, encoding='utf-8').read()
    # el dossier comença l'any 2000: llevem el filtre «2000–1999»
    s = s.replace(', ["2000", "2000–1999", 0, 1999]]', ']')
    open(p, 'w', encoding='utf-8').write(s)
    aplica_fitxer(p)
print(len(comu.CHK), 'comprovacions correctes')
