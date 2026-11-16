# Figures pròpies de la Unitat 6 de 4t ESO Matemàtiques A (Funcions. Característiques). Fan servir la classe Plot de
# _eines/apunts/4eso-b-t7/fig.py (SVG per als apunts i TikZ per a la fitxa); la resta de figures dels apunts són les de
# fig.figures() de 4t ESO B (unitat 7). Marcador als contingut-*.html: @@FIG:nom@@.
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "4eso-b-t7"))
from fig import Plot, piece, sq


def poly(p, pts, col="a", dots=True):
    for (a, b), (c, d) in zip(pts, pts[1:]): p.seg(a, b, c, d, col)
    if dots:
        for q in pts: p.dot(*q, col=col)
    return p


# 6.7 excursió: distància a casa (km) en funció del temps (h)
EXC = [(0, 0), (2, 8), (3, 8), (4, 10), (6, 0)]
# 6.7 dipòsit: volum (L) en funció del temps (min)
DIP = [(0, 0), (10, 200), (15, 200), (25, 0)]
# 6.8 aparcament: 2 € la primera hora (o fracció) i 1,50 € cada hora més (o fracció), fins a 4 h
PARK = [(0, 1, 2), (1, 2, 3.5), (2, 3, 5), (3, 4, 6.5)]


def exc(W=320):
    return poly(Plot(-.4, 6.6, -1.2, 12, sx=1, sy=2, lx=1, ly=2, W=W), EXC)


def dip(W=320):
    return poly(Plot(-1.5, 27, -25, 240, sx=5, sy=40, lx=5, ly=40, W=W), DIP)


def park(W=300):
    p = Plot(-.4, 4.6, -.8, 7.5, sx=1, sy=1, lx=1, ly=1, W=W)
    for a, b, y in PARK:
        p.seg(a, y, b, y).dot(a, y, open=True).dot(b, y)
    return p


def taxi(W=280):
    p = Plot(-1, 11, -1.5, 17, sx=1, sy=2, lx=2, ly=2, W=W).fn(lambda t: 3 + 1.2 * t, 0, 11)
    for t in (0, 5, 10): p.dot(t, 3 + 1.2 * t, "b")
    return p


def corral(W=280):
    return (Plot(-2, 22, -12, 120, sx=2, sy=20, lx=4, ly=20, W=W).fn(lambda t: t * (20 - t), 0, 20)
            .dot(0, 0, open=True).dot(20, 0, open=True).dot(10, 100, "b").gd(10, 0, 10, 100).gd(0, 100, 10, 100))


def gym(W=300):
    """6.8 dues ofertes de gimnàs: A = 30 + 20x, B = 35x (es tallen en x = 2)"""
    p = Plot(-.5, 6.6, -15, 230, sx=1, sy=20, lx=1, ly=40, W=W)
    p.fn(lambda t: 30 + 20 * t, 0, 6.6, "b").fn(lambda t: 35 * t, 0, 6.6, "o").dot(2, 70, "v").text(5.6, 118, "A", "b").text(4.9, 205, "B", "o")
    return p


def figures():
    F = {}
    F["gym"] = gym()
    F["exc"] = exc()
    F["dip"] = dip()
    F["park"] = park()
    F["taxi"] = taxi()
    F["corral"] = corral()
    # 6.1 variables: taula de valors d'una funció donada per punts (no s'uneixen)
    p = Plot(-.5, 6.5, -1, 13, sx=1, sy=2, lx=1, ly=2, W=260)
    for n in range(1, 7): p.dot(n, 2 * n, "b")
    F["entrades"] = p
    # 6.2 domini i recorregut a partir de la gràfica (la d'una paràbola tallada)
    F["domg"] = piece(Plot(-3, 5, -2, 6, W=240), [(lambda t: 5 - (t - 1) ** 2, -1, 3, True, False)]).xbar(-1, 3).ybar(1, 5)
    return F
