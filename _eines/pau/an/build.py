#!/usr/bin/env python3
"""Genera les pàgines PAU d'anàlisi de 2n Batx CCSS (unitats 4-8) a partir del dossier
«Exercicis d'anàlisi de la selectivitat» (Comunitat Valenciana, 1997-2026).

- an.txt: enunciats en el mateix ordre que el dossier ("## U | Convocatòria", U = unitat on va l'exercici).
  Cada exercici va a la unitat més avançada que necessita (p. ex. continuïtat + integral -> unitat 8).
- XL: exercicis que també es mostren a les unitats 4 i 5 perquè algun apartat és d'aquestes unitats.
- sol_a.py, sol_b.py, sol_c.py: solucions pas a pas (número del dossier -> HTML), calculades amb fraccions
  exactes i comprovades (ck). Les gràfiques es dibuixen en SVG (anlib.plot).
Reutilitza parse() i write_pages() de ../build_pau.py.
Ús (des de l'arrel del web):  python3 _eines/pau/an/build.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '..', '..', 'tema'))
from build_pau import parse, write_pages, CCSS  # noqa: E402
from aplica import aplica_fitxer  # noqa: E402
import anlib, sol_a, sol_b, sol_c  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'materials', '2batx-ccss'))
items = parse(os.path.join(HERE, 'an.txt'))
assert len(items) == 118, len(items)
sols = {**sol_a.S, **sol_b.S, **sol_c.S}
for i, e in enumerate(items):
    e['num'] = i + 1
    e['h'] = e['h'].replace('<p>@@FIG62@@</p>', sol_b.FIG62)
    if e['num'] in sols: e['s'] = sols[e['num']]
    if e['conv'] == 'Sense data': e['y'] = 0

XL = {
    4: {30: 'a', 31: 'a i b', 34: 'a', 36: 'a', 39: 'b', 41: 'c', 44: 'a', 48: 'a', 50: 'a', 52: 'a', 57: 'c', 60: 'a',
        63: 'a', 66: 'a', 69: 'a', 70: 'a i c', 76: 'a i d', 78: 'a', 80: 'd', 86: 'a i c', 102: 'a', 105: 'a',
        115: 'a', 117: 'a'},
    5: {33: 'd i e', 107: 'a', 113: 'a'},
}


def apartats(t):
    return ('els apartats ' if ' i ' in t else 'l’apartat ') + ' i '.join(p + ')' for p in t.split(' i '))


NOMS = {'4': 'Límits i continuïtat', '5': 'Derivades', '6': 'Aplicacions de la derivada',
        '7': 'Representació gràfica de funcions', '8': 'Integrals'}
FITX = {'4': 'pau-u4-limits-continuitat.html', '5': 'pau-u5-derivades.html', '6': 'pau-u6-aplicacions-derivada.html',
        '7': 'pau-u7-representacio-funcions.html', '8': 'pau-u8-integrals.html'}
units = []
for u in '45678':
    sel = []
    for e in items:
        if e['k'] == u: sel.append(e)
        elif e['num'] in XL.get(int(u), {}):
            note = ('<p class="xl" style="margin:0 0 10px;padding:6px 12px;border-radius:8px;font-size:.92rem;'
                    'background:color-mix(in srgb,var(--c) 12%%,transparent)"><strong>En aquesta unitat:</strong> %s. '
                    'La resta de l’exercici és de la unitat %s (%s).</p>' % (apartats(XL[int(u)][e['num']]), e['k'], NOMS[e['k']]))
            sel.append(dict(e, h=note + e['h']))
    units.append((FITX[u], u, NOMS[u], sel, '#7fa040'))
opts = dict(CCSS, RANGE='1997–2026', FIRST='1997')
write_pages(OUT, units, opts)
# les fórmules llargues es desplacen dins del seu pas (position: relative perquè el MathML ocult de KaTeX,
# que va en posició absoluta, no faça més ampla la pàgina en el mòbil)
CSS = ('<style>.sol-body .steps > li, .sol-body .res, .ex p, .parts li { overflow-x: auto; overflow-y: hidden; position: relative; }'
       ' .ex .katex-display { overflow-x: auto; overflow-y: hidden; }</style>\n</head>')
for u in units:
    p = os.path.join(OUT, u[0]); s = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(s.replace('</head>', CSS, 1))
    aplica_fitxer(p)
print(len(anlib.CHK), 'comprovacions correctes')
