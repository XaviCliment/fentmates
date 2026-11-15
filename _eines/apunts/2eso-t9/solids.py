# Cossos geomètrics en perspectiva (Unitat 11): projecció, arestes ocultes i desenvolupaments.
# Torna llistes d'elements 2D per a G() de comu.py (apunts) i per a tz() de la fitxa (TikZ):
# ('poly', pts, cls) · ('seg', A, B, cls) · ('pl', pts, cls) polilínia oberta · ('circ', C, r, cls) · ('sect', C, r, a0, a1, cls)
# ('txt', P, text, opts) · ('dot', P). Classes: 'fr' cara visible, 'top' cara de dalt, 'ed' aresta, 'hid' aresta oculta,
# 'ax' altura o apotema (discontínua de color), 'bs' base destacada. app.js en té una còpia en JavaScript.
import math
from itertools import combinations

TH, PH = -28, 22  # gir al voltant de l'eix vertical i elevació de la vista (graus)

def proj(p, th=TH, ph=PH):
    t, f = math.radians(th), math.radians(ph)
    x, y, z = p
    u = x * math.cos(t) - y * math.sin(t); d = x * math.sin(t) + y * math.cos(t)
    return (u, z * math.cos(f) + d * math.sin(f))
def towards(th=TH, ph=PH):
    t, f = math.radians(th), math.radians(ph)
    return (-math.cos(f) * math.sin(t), -math.cos(f) * math.cos(t), math.sin(f))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def cen(P): return tuple(sum(p[i] for p in P) / len(P) for i in range(3))

def hull_faces(V, eps=1e-7):
    """cares d'un poliedre convex donat pels vèrtexs (ordenades al voltant del centre de cada cara)"""
    faces, seen = [], set()
    for i, j, k in combinations(range(len(V)), 3):
        n = cross(sub(V[j], V[i]), sub(V[k], V[i]))
        if dot(n, n) < 1e-12: continue
        s = [dot(n, sub(p, V[i])) for p in V]
        if max(s) > eps and min(s) < -eps: continue
        f = tuple(sorted(q for q, v in enumerate(s) if abs(v) <= eps))
        if f in seen: continue
        seen.add(f)
        c = cen([V[q] for q in f]); nn = math.sqrt(dot(n, n)); n = tuple(x / nn for x in n)
        a = sub(V[f[0]], c); b = cross(n, a)
        faces.append(sorted(f, key=lambda q: math.atan2(dot(sub(V[q], c), b), dot(sub(V[q], c), a))))
    return faces

def polyhedron(V, F=None, th=TH, ph=PH, fill='fr', bases=()):
    """dibuix d'un poliedre convex amb les arestes ocultes discontínues. bases: índexs de cares que es pinten diferent"""
    F = F or hull_faces(V)
    c = cen(V); w = towards(th, ph)
    front = []
    for f in F:
        P = [V[q] for q in f]; n = cross(sub(P[1], P[0]), sub(P[2], P[0]))
        if dot(n, sub(cen(P), c)) < 0: n = tuple(-x for x in n)
        front.append(dot(n, w) > 1e-9)
    E = {}
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]): E.setdefault(tuple(sorted((a, b))), []).append(front[fi])
    P2 = [proj(p, th, ph) for p in V]
    it = []
    for fi, f in enumerate(F):
        if front[fi]: it.append(('poly', [P2[q] for q in f], 'bs' if fi in bases else fill))
    for (a, b), fl in E.items():
        if not any(fl): it.append(('seg', P2[a], P2[b], 'hid'))
    for (a, b), fl in E.items():
        if any(fl): it.append(('seg', P2[a], P2[b], 'ed'))
    return it, P2

# ---------- poliedres concrets ----------
def ngon(n, R, z=0, rot=None):
    rot = -90 - 180 / n if rot is None else rot
    return [(R * math.cos(math.radians(rot + 360 * k / n)), R * math.sin(math.radians(rot + 360 * k / n)), z) for k in range(n)]
def circum(n, l): return l / (2 * math.sin(math.pi / n))
def prism(n, l, h): R = circum(n, l); return ngon(n, R, 0) + ngon(n, R, h)
def cuboid(a, b, c): return [(x, y, z) for z in (0, c) for y in (0, b) for x in (0, a)]
def pyramid(n, l, h): return ngon(n, circum(n, l), 0) + [(0, 0, h)]
def frustum(n, L, l, h): return ngon(n, circum(n, L), 0) + ngon(n, circum(n, l), h)
PHI = (1 + 5 ** 0.5) / 2
def platonic(name, s=1.0):
    if name == 'tetra': V = ngon(3, 2 * 2 ** 0.5 / 3 ** 0.5, -0.8) + [(0, 0, -0.8 + 2 * 2 ** 0.5 * (2 / 3) ** 0.5)]  # base horitzontal, aresta 2√2
    elif name == 'cub': V = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    elif name == 'octa': V = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    elif name == 'ico': V = [p for a in (-1, 1) for b in (-PHI, PHI) for p in ((0, a, b), (a, b, 0), (b, 0, a))]
    else:
        V = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
        V += [p for a in (-1 / PHI, 1 / PHI) for b in (-PHI, PHI) for p in ((0, a, b), (a, b, 0), (b, 0, a))]
    return [(x * s, y * s, z * s) for x, y, z in V]

# ---------- cossos de revolució (vista frontal, elevació ph) ----------
def _ell(r, b, cy, t0, t1, n=48):
    return [(r * math.cos(t0 + (t1 - t0) * k / n), cy + b * math.sin(t0 + (t1 - t0) * k / n)) for k in range(n + 1)]
def cylinder(r, h, ph=PH, y0=0, top=True):
    f = math.radians(ph); b = r * math.sin(f); H = h * math.cos(f)
    front = _ell(r, b, y0, math.pi, 2 * math.pi); back = _ell(r, b, y0, 0, math.pi)
    topf = _ell(r, b, y0 + H, math.pi, 2 * math.pi)
    side = [(-r, y0 + H)] + front + [(r, y0 + H)] + topf[::-1]
    it = [('poly', side, 'fr'), ('pl', back, 'hid'), ('pl', front, 'ed'), ('seg', (-r, y0), (-r, y0 + H), 'ed'), ('seg', (r, y0), (r, y0 + H), 'ed')]
    if top: it.append(('poly', _ell(r, b, y0 + H, 0, 2 * math.pi), 'top'))
    return it, {'B': (0, y0), 'T': (0, y0 + H), 'R': (r, y0), 'RT': (r, y0 + H), 'L': (-r, y0), 'LT': (-r, y0 + H), 'b': b}
def cone(r, h, ph=PH, y0=0, R2=None):
    """con (o tronc de con si R2 és el radi de dalt)"""
    f = math.radians(ph); b = r * math.sin(f); H = h * math.cos(f)
    Hap = H if R2 is None else H * r / (r - R2)      # altura (projectada) del vèrtex del con complet
    t0 = math.asin(min(b / Hap, 1)) if Hap > b else math.pi / 2
    vis = _ell(r, b, y0, math.pi - t0, 2 * math.pi + t0); hid = _ell(r, b, y0, t0, math.pi - t0)
    A = (0, y0 + H)
    if R2 is None:
        it = [('poly', [A] + vis, 'fr'), ('pl', hid, 'hid'), ('pl', vis, 'ed'), ('seg', A, vis[0], 'ed'), ('seg', A, vis[-1], 'ed')]
    else:
        k = R2 / r; b2 = b * k
        top = _ell(R2, b2, y0 + H, 0, 2 * math.pi); vt = _ell(R2, b2, y0 + H, math.pi - t0, 2 * math.pi + t0)
        it = [('poly', vis + vt[::-1], 'fr'), ('pl', hid, 'hid'), ('pl', vis, 'ed'), ('seg', vt[0], vis[0], 'ed'), ('seg', vt[-1], vis[-1], 'ed'), ('poly', top, 'top')]
    return it, {'B': (0, y0), 'A': A, 'R': (r, y0), 'L': (-r, y0), 'b': b}
def sphere(r, ph=PH, y0=0, half=False):
    """esfera (o semiesfera, amb el cercle màxim a baix) amb el centre en (0, y0)"""
    f = math.radians(ph); b = r * math.sin(f)
    front = _ell(r, b, y0, math.pi, 2 * math.pi); back = _ell(r, b, y0, 0, math.pi)
    if half:
        dome = [(r * math.cos(t), y0 + r * math.sin(t)) for t in [math.pi * k / 48 for k in range(49)]]
        return [('poly', dome + front[1:-1], 'fr'), ('pl', dome, 'ed'), ('pl', front, 'ed'), ('pl', back, 'hid')], {'C': (0, y0), 'R': (r, y0)}
    return [('circ', (0, y0), r, 'fr'), ('pl', back, 'hid'), ('pl', front, 'ed')], {'C': (0, y0), 'R': (r, y0)}
def capsule(r, h, ph=PH):
    """cilindre vertical de radi r i altura h amb una semiesfera a cada extrem"""
    f = math.radians(ph); b = r * math.sin(f); H = h * math.cos(f)
    top = [(r * math.cos(t), H + r * math.sin(t)) for t in [math.pi * k / 48 for k in range(49)]]
    bot = [(-r * math.cos(t), -r * math.sin(t)) for t in [math.pi * k / 48 for k in range(49)]]
    out = top + bot
    return [('poly', out, 'fr'), ('pl', _ell(r, b, 0, math.pi, 2 * math.pi), 'ed'), ('pl', _ell(r, b, H, math.pi, 2 * math.pi), 'ed'), ('pl', out + out[:1], 'ed')], {'B': (0, 0), 'T': (0, H)}
def shift(it, dx, dy):
    def S(p): return (p[0] + dx, p[1] + dy)
    out = []
    for e in it:
        k = e[0]
        if k in ('poly', 'pl'): out.append((k, [S(p) for p in e[1]]) + tuple(e[2:]))
        elif k == 'seg': out.append((k, S(e[1]), S(e[2])) + tuple(e[3:]))
        elif k in ('circ', 'sect', 'txt', 'dot'): out.append((k, S(e[1])) + tuple(e[2:]))
        else: out.append(e)
    return out

# ---------- desenvolupaments ----------
def net_prism(n, l, h):
    it = []
    for k in range(n): it.append(('poly', [(k * l, 0), ((k + 1) * l, 0), ((k + 1) * l, h), (k * l, h)], 'nf'))
    a = l / (2 * math.tan(math.pi / n))
    for y0, s in ((0, -1), (h, 1)):
        C = (l / 2, y0 + s * a); R = circum(n, l)
        rot = 90 + 180 / n if s < 0 else -90 - 180 / n
        it.append(('poly', [(C[0] + R * math.cos(math.radians(rot + 360 * k / n)), C[1] + R * math.sin(math.radians(rot + 360 * k / n))) for k in range(n)], 'bs'))
    return it
def net_pyramid(n, l, ap):
    """base al centre i els triangles plegats cap enfora"""
    R = circum(n, l); a = l / (2 * math.tan(math.pi / n)); rot = -90 - 180 / n
    B = [(R * math.cos(math.radians(rot + 360 * k / n)), R * math.sin(math.radians(rot + 360 * k / n))) for k in range(n)]
    it = [('poly', B, 'bs')]
    for k in range(n):
        P, Q = B[k], B[(k + 1) % n]; M = ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2); d = math.hypot(*M)
        it.append(('poly', [P, Q, (M[0] / d * (a + ap), M[1] / d * (a + ap))], 'nf'))
    return it
def net_cylinder(r, h):
    L = 2 * math.pi * r
    return [('poly', [(0, 0), (L, 0), (L, h), (0, h)], 'nf'), ('circ', (L / 2, -r), r, 'bs'), ('circ', (L / 2, h + r), r, 'bs')]
def net_cone(r, g):
    ang = 360 * r / g
    return [('sect', (0, 0), g, 270 - ang / 2, 270 + ang / 2, 'nf'), ('circ', (0, -g - r), r, 'bs')]
