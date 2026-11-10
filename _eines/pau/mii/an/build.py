#!/usr/bin/env python3
"""Pàgines PAU d'anàlisi de 2n Batx MII (unitats 5-9) a partir del recull de l'IES Vermellar
(«Exercicis d'anàlisi de la selectivitat», Comunitat Valenciana 2002-2026, 128 exercicis).

- an.txt: enunciats en l'ordre del recull ("## U | Convocatòria", U = unitat més avançada que necessita l'exercici).
- XL: exercicis que també es mostren en unitats anteriors perquè algun apartat és d'aquestes unitats.
- sol_1.py, sol_2.py, sol_3.py: solucions pas a pas (número del recull -> HTML), comprovades amb sympy (mlib.py).
- figs.py: figures SVG dels enunciats (@@FIGn@@).
Ús (des de l'arrel del repositori):  python3 _eines/pau/mii/an/build.py
Només tematitza les cinc pàgines que genera (no crida el aplica.py complet).
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..')); sys.path.insert(0, os.path.join(ROOT, '_eines', 'tema'))
from build_pau import parse, write_pages  # noqa: E402
from aplica import aplica_fitxer  # noqa: E402
import mlib, figs  # noqa: E402

sols = {}
for mod in ('sol_1', 'sol_2', 'sol_3'):
    try: sols.update(__import__(mod).S)
    except ModuleNotFoundError: pass

OUT = os.path.join(ROOT, 'materials', '2batx-mii')
items = parse(os.path.join(HERE, 'an.txt'))
assert len(items) == 128, len(items)
for i, e in enumerate(items):
    e['num'] = i + 1
    e['h'] = re.sub(r'<p>@@FIG(\d+)@@</p>', lambda m_: figs.FIG[int(m_.group(1))], e['h'])
    if e['num'] in sols: e['s'] = sols[e['num']]

XL = {
    5: {31: 'b', 33: 'a', 37: 'a', 53: 'a', 61: 'a', 73: 'a', 79: 'a', 81: 'a', 86: 'b', 89: 'a', 95: 'a i b', 97: 'a',
        99: 'a', 101: 'a', 105: 'b', 109: 'a', 111: 'a i c', 118: 'a', 119: 'a', 120: 'a', 121: 'a', 123: 'a'},
    6: {31: 'a', 38: 'a', 54: 'a', 65: 'b', 91: 'a i b'},
    7: {13: 'a', 25: 'b', 29: 'a', 49: 'a', 50: 'c', 61: 'b', 63: 'b, c i d', 64: 'b i c', 65: 'a i b', 66: 'a i b',
        67: 'a i b', 72: 'b i c', 73: 'b', 75: 'b', 77: 'a', 79: 'b', 81: 'b', 83: 'c', 84: 'b', 86: 'a', 87: 'a',
        89: 'b', 93: 'a i c', 96: 'a, b i c', 101: 'b', 103: 'a', 105: 'c', 109: 'b', 110: 'a', 113: 'a', 118: 'b',
        119: 'a i b', 120: 'a', 121: 'a', 123: 'b i c', 125: 'a i b', 127: 'b'},
    8: {83: 'a, b i d', 87: 'b', 93: 'b', 99: 'b', 103: 'b', 105: 'a i b', 113: 'b', 116: 'a', 118: 'c', 120: 'b',
        121: 'b', 124: 'a', 125: 'c'},
}


def apartats(t):
    ps = [p for p in re.split(r', | i ', t)]
    s = ', '.join(p + ')' for p in ps[:-1]) + (' i ' if len(ps) > 1 else '') + ps[-1] + ')'
    return ('els apartats ' if len(ps) > 1 else 'l’apartat ') + s


NOMS = {'5': 'Límits i continuïtat', '6': 'Càlcul de derivades. Derivabilitat', '7': 'Aplicacions de la derivada',
        '8': 'Representació de funcions', '9': 'Integrals'}
FITX = {'5': 'pau-u5-limits-continuitat.html', '6': 'pau-u6-derivades.html', '7': 'pau-u7-aplicacions-derivada.html',
        '8': 'pau-u8-representacio-funcions.html', '9': 'pau-u9-integrals.html'}
units = []
for u in '56789':
    sel = []
    for e in items:
        if e['k'] == u: sel.append(e)
        elif e['num'] in XL.get(int(u), {}):
            assert int(e['k']) > int(u), (e['num'], u)
            note = ('<p class="xl" style="margin:0 0 10px;padding:6px 12px;border-radius:8px;font-size:.92rem;'
                    'background:color-mix(in srgb,var(--c) 12%%,transparent)"><strong>En aquesta unitat:</strong> %s. '
                    'La resta de l’exercici és de la unitat %s (%s).</p>' % (apartats(XL[int(u)][e['num']]), e['k'], NOMS[e['k']]))
            sel.append(dict(e, h=note + e['h']))
    units.append((FITX[u], u, NOMS[u], sel, '#7fa040'))
MII = {"SUBJECT": "Matemàtiques II", "COLOR": "#7fa040", "COURSE_URL": "2batx-mii.html",
       "COURSE": "2n Batxillerat MII", "RANGE": "2002–2026", "FIRST": "2002"}
write_pages(OUT, units, MII)
CSS = ('<style>.sol-body .steps > li, .sol-body .res, .ex p, .parts li { overflow-x: auto; overflow-y: hidden; position: relative; }'
       ' .ex .katex-display { overflow-x: auto; overflow-y: hidden; } .ex figure svg { max-width: 100%; height: auto; }</style>\n</head>')
for u in units:
    p = os.path.join(OUT, u[0]); s = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(s.replace('</head>', CSS, 1))
    aplica_fitxer(p)
missing = [e['num'] for e in items if 's' not in e]
print(len(mlib.CHK), 'comprovacions correctes;', len(sols), 'solucions', ('· FALTEN %d' % len(missing)) if missing else '')
