# Figures pròpies de la Unitat 7 de 4t ESO Matemàtiques A (Funcions elementals). Fan servir la classe Plot de
# _eines/apunts/4eso-b-t7/fig.py (SVG per als apunts i TikZ per a la fitxa); la resta de figures dels apunts són les de
# fig.figures() de 4t ESO B (unitats 7 i 8). Marcador als contingut-*.html: @@FIG:nom@@.
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "4eso-b-t7"))
from fig import Plot, sq


def qrep(a, b, c, x0, x1, y0, y1, W=260):
    """paràbola amb els punts que es calculen per a representar-la: vèrtex (lila), eix, tall OY i el seu simètric (verd),
    talls OX (blau) i dos punts més de la taula (taronja)"""
    f = lambda t: a * t * t + b * t + c
    vx = -b / (2 * a)
    p = Plot(x0, x1, y0, y1, W=W).gd(vx, y0, vx, y1).fn(f)
    d = b * b - 4 * a * c
    if d >= 0:
        for r in {(-b - math.sqrt(d)) / (2 * a), (-b + math.sqrt(d)) / (2 * a)}: p.dot(r, 0, "b")
    p.dot(0, c, "g")
    if abs(vx) > 1e-9: p.dot(2 * vx, c, "g")
    for t in (vx - 2, vx + 2):
        if abs(t) > 1e-9 and abs(t - 2 * vx) > 1e-9: p.dot(t, f(t), "o")
    return p.dot(vx, f(vx), "v")


def figures():
    F = {}
    # 7.4 representació de paràboles (exemples resolts)
    F["qrep1"] = qrep(1, -4, 3, -2, 6, -2, 6)
    F["qrep2"] = qrep(-1, 2, -2, -3, 5, -7, 1)
    # 7.5 y = √x a partir de la taula de valors
    p = Plot(-1, 10, -1, 4, W=260).fn(sq, 0, 10)
    for t in (0, 1, 4, 9): p.dot(t, math.sqrt(t), "b")
    F["sq0"] = p
    # 7.6 taula de la velocitat i el temps (v · t = 120)
    p = Plot(-8, 130, -.6, 7, sx=20, sy=1, lx=20, ly=1, W=280).fn(lambda v: 120 / v, 16, 130)
    for v in (20, 40, 60, 80, 120): p.dot(v, 120 / v, "b")
    F["vt"] = p
    # 7.8 creixement i decreixement exponencial
    p = Plot(-.5, 6.5, -60, 700, sx=1, sy=100, lx=1, ly=100, W=260).fn(lambda t: 100 * 1.4 ** t, 0, 6.5, "g").fn(lambda t: 600 * .7 ** t, 0, 6.5, "b")
    for t in range(7): p.dot(t, 100 * 1.4 ** t, "g").dot(t, 600 * .7 ** t, "b")
    F["egr"] = p
    # 7.9 problemes
    F["pil"] = (Plot(-.4, 4.6, -3, 24, sx=1, sy=5, lx=1, ly=5, W=260).fn(lambda t: -5 * t * t + 20 * t, 0, 4)
                .dot(2, 20, "v").gd(2, 0, 2, 20).gd(0, 20, 2, 20).dot(0, 0, "b").dot(4, 0, "b"))
    p = Plot(-.6, 13, -.6, 13, sx=1, sy=1, lx=2, ly=2, W=240).fn(lambda n: 24 / n, 1.8, 13, "m", dash=True)
    for n in (2, 3, 4, 6, 8, 12): p.dot(n, 24 / n, "b")
    F["aix"] = p
    p = Plot(-8, 90, -.4, 4.6, sx=10, sy=1, lx=20, ly=1, W=260).fn(lambda h: math.sqrt(h / 5), 0, 90)
    for h in (0, 5, 20, 45, 80): p.dot(h, math.sqrt(h / 5), "b")
    F["caig"] = p
    return F
