#!/usr/bin/env python3
"""Genera assets/img/banner-adhesius.svg (banner de l'inici: adhesius de colors sobre blau).
Ús (des de l'arrel del web): python3 _eines/banner-adhesius/genera.py
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "img", "banner-adhesius.svg")
BG = "#3d6aa0"

ICON = {
    "pi": '<text x="0" y="14" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="44" stroke="none" fill="#fff">π</text>',
    "sum": '<text x="0" y="14" text-anchor="middle" font-family="Georgia,serif" font-size="44" stroke="none" fill="#fff">∑</text>',
    "bulb": '<path d="M-14 6 A20 20 0 1 1 14 6 Q8 12 8 20 H-8 Q-8 12 -14 6 Z"/><path d="M-7 26 H7 M-5 32 H5"/><path d="M0 -36 v-6 M-26 -26 l-5 -5 M26 -26 l5 -5 M-34 -6 h-6 M34 -6 h6"/>',
    "compass": '<circle cx="0" cy="-30" r="5"/><path d="M-3 -26 L-20 30 M3 -26 L20 30 M-14 10 L14 10"/><path d="M-20 30 l-2 6 M20 30 l0 6"/>',
    "dice": '<rect x="-22" y="-22" width="44" height="44" rx="9"/><path d="M-10 -10h0M10 10h0M0 0h0M10 -10h0M-10 10h0" stroke-width="6"/>',
    "calc": '<rect x="-22" y="-32" width="44" height="64" rx="7"/><rect x="-14" y="-24" width="28" height="12" rx="2"/><path d="M-10 -2h0M0 -2h0M10 -2h0M-10 8h0M0 8h0M10 8h0M-10 18h0M0 18h0M10 18h0" stroke-width="5"/>',
    "graph": '<path d="M-36 24 H36 M-28 32 V-32"/><path d="M-34 18 C-14 18 -10 -24 6 -24 S24 10 36 -6"/>',
    "star": '<path d="M0 -20 L6 -6 L21 -6 L9 3 L13 18 L0 9 L-13 18 L-9 3 L-21 -6 L-6 -6 Z"/>',
}
# color, icona, x, y, quadrat?, gir
STICKERS = [
    ("#ff7a50", "pi", 1100, 170, True, -8), ("#ffc94d", "bulb", 1280, 120, True, 6),
    ("#2bb3a3", "compass", 1450, 210, True, -6), ("#8064a1", "dice", 1200, 360, True, 10),
    ("#e0457b", "calc", 1390, 420, True, -4), ("#7fa040", "graph", 1040, 430, True, 4),
    ("#e0475b", "star", 1530, 500, True, 12), ("#ffc94d", "sum", 1555, 335, True, -10),
]


def shape(fill, square):
    if square:
        return f'<rect x="-62" y="-62" width="124" height="124" rx="30" fill="{fill}"/>'
    return f'<circle r="66" fill="{fill}"/>'


parts = []
for i, (c, ic, x, y, sq, rot) in enumerate(STICKERS):
    parts.append(
        f'<g transform="translate({x} {y}) rotate({rot})"><g class="f" style="animation-delay:{i * .5:.1f}s">'
        f'<g transform="translate(0 6)" opacity=".22">{shape("#000", sq)}</g>{shape(c, sq)}'
        f'<g fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">{ICON[ic]}</g></g></g>')
dots = "".join(f'<circle cx="{40 + (i * 97) % 1560}" cy="{30 + (i * 53) % 560}" r="3"/>' for i in range(60))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 600" preserveAspectRatio="xMaxYMid slice">
<style>
@keyframes bob {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
.f {{ animation: bob 6s ease-in-out infinite; }}
@media (prefers-reduced-motion: reduce) {{ .f {{ animation: none; }} }}
</style>
<rect width="1600" height="600" fill="{BG}"/>
<g fill="#fff" fill-opacity=".12">{dots}</g>
{"".join(parts)}
</svg>
'''
open(OUT, "w", encoding="utf-8").write(svg)
print(OUT)
