# Figures de la Unitat 8 de 4t ESO A (Semblança. Aplicacions); les de ../2eso-t8/fig8.py (fetes a partir de ../3eso-t10/fig10.py)
# més inacc_tales(), inacc_cross() i alt_fig(): llistes d'elements per a G() de comu.py.
import math

def fnum(v):
    """nombre amb coma decimal (com a molt 2 decimals) per a les etiquetes"""
    r = round(float(v), 2)
    s = ('%d' % r) if r == int(r) else ('%.2f' % r).rstrip('0')
    return s.replace('.', ',')

def tales(d1, d2, ar=60, as_=78, p=2.2, labs=None, hot=None, lens=True):
    """tres paral·leles horitzontals (y = 0, d1, d1+d2) tallades per dues secants r i s.
    labs: etiquetes dels segments {'AB':…, 'BC':…, 'A1B1':…, 'B1C1':…}; hot: segment destacat"""
    Y = [0, d1, d1 + d2]
    tr, ts = 1 / math.tan(math.radians(ar)), 1 / math.tan(math.radians(as_))
    R = [(y * tr, y) for y in Y]; Sg = [(p + y * ts, y) for y in Y]
    x0 = min(R[0][0], R[2][0]) - 1.2; x1 = max(Sg[0][0], Sg[2][0]) + 1.2
    it = [('seg', (x0, y), (x1, y), 'par') for y in Y]
    e = 0.7
    it += [('seg', (-e * tr, -e), ((Y[2] + e) * tr, Y[2] + e), 'tv'), ('seg', (p - e * ts, -e), (p + (Y[2] + e) * ts, Y[2] + e), 'tv')]
    if hot:
        seg = {'AB': (R[0], R[1]), 'BC': (R[1], R[2]), 'A1B1': (Sg[0], Sg[1]), 'B1C1': (Sg[1], Sg[2]), 'AC': (R[0], R[2]), 'A1C1': (Sg[0], Sg[2])}
        for h in hot.split(','): it.append(('seg',) + seg[h] + ('hl',))
    for P in R + Sg: it.append(('dot', P))
    for P, n in zip(R, 'ABC'): it.append(('txt', P, n, {'dx': -9, 'dy': -5, 'a': 'end'}))
    for P, n in zip(Sg, 'ABC'): it.append(('txt', P, n + '′', {'dx': 9, 'dy': -5, 'a': 'start'}))
    it += [('txt', (x0, Y[2]), 'r', {'dx': 4, 'dy': -6, 'a': 'start', 'cls': 'par'})]
    it += [('txt', ((Y[2] + e) * tr, Y[2] + e), 'a', {'dx': -8, 'cls': 'tv'}), ('txt', (p + (Y[2] + e) * ts, Y[2] + e), 'b', {'dx': 8, 'cls': 'tv'})]
    if labs:
        def L(k, A, B, side):
            if k in labs: it.append(('txt', ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2), labs[k], {'dx': side * 10, 'a': 'end' if side < 0 else 'start', 'cls': 'hot' if hot and k in hot.split(',') else ''}))
        L('AB', R[0], R[1], -1); L('BC', R[1], R[2], -1); L('A1B1', Sg[0], Sg[1], 1); L('B1C1', Sg[1], Sg[2], 1)
    return it

def tpos(AB, AC, ang, t, labs=None, hot=None):
    """triangle ABC amb A al vèrtex de dalt (angle ang) i B′C′ ∥ BC a la fracció t des d'A"""
    a = math.radians(ang)
    A = (0, 0)
    B =(-AB * math.sin(math.radians(28)), -AB * math.cos(math.radians(28)))
    C = (AC * math.sin(a - math.radians(28)), -AC * math.cos(a - math.radians(28)))
    B1 = (B[0] * t, B[1] * t); C1 = (C[0] * t, C[1] * t)
    it = [('poly', [A, B, C], 'gf'), ('poly', [A, B1, C1], 'tr'), ('seg', B1, C1, 'hl'), ('seg', B, C, 'hl2')]
    for P in (A, B, C, B1, C1): it.append(('dot', P))
    it += [('txt', A, 'A', {'dy': -8}), ('txt', B, 'B', {'dx': -8, 'a': 'end', 'dy': 8}), ('txt', C, 'C', {'dx': 8, 'a': 'start', 'dy': 8}),
           ('txt', B1, 'B′', {'dx': -8, 'a': 'end'}), ('txt', C1, 'C′', {'dx': 8, 'a': 'start'})]
    if labs:
        pos = {'AB1': (A, B1, -1), 'B1B': (B1, B, -1), 'AC1': (A, C1, 1), 'C1C': (C1, C, 1), 'B1C1': (B1, C1, 0), 'BC': (B, C, 0), 'AB': (A, B, -1), 'AC': (A, C, 1)}
        for k, v in labs.items():
            P, Q, sd = pos[k]
            M = ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
            o = {'dx': sd * 10, 'a': 'end' if sd < 0 else 'start' if sd > 0 else 'middle', 'dy': 16 if k == 'BC' else (-5 if k == 'B1C1' else 4)}
            if hot == k: o['cls'] = 'hot'
            it.append(('txt', M, v, o))
    return it

def shadow(h1, s1, h2, s2, l1='', l2='', ls1='', ls2='', hot=None, gap=None):
    """pal (h1, ombra s1) i edifici o arbre (h2, ombra s2) amb els rajos de sol paral·lels"""
    g = gap if gap is not None else max(s1, 1) + 1.2
    x2 = s1 + g
    it = [('seg', (-0.6, 0), (x2 + s2 + 0.8, 0), 'axis'),
          ('poly', [(0, 0), (0, h1), (s1, 0)], 'tr'), ('ra', (0, 0), (1, 0), (0, 1)),
          ('poly', [(x2, 0), (x2, h2), (x2 + s2, 0)], 'gf'), ('ra', (x2, 0), (x2 + 1, 0), (x2, 1)),
          ('seg', (0, 0), (0, h1), 'wall'), ('seg', (x2, 0), (x2, h2), 'wall'),
          ('seg', (0, h1), (s1, 0), 'ray'), ('seg', (x2, h2), (x2 + s2, 0), 'ray')]
    it += [('txt', (0, h1 / 2), l1, {'dx': -8, 'a': 'end', 'cls': 'hot' if hot == 'h1' else ''}), ('txt', (s1 / 2, 0), ls1, {'dy': 15, 'cls': 'hot' if hot == 's1' else ''}),
           ('txt', (x2, h2 / 2), l2, {'dx': -8, 'a': 'end', 'cls': 'hot' if hot == 'h2' else ''}), ('txt', (x2 + s2 / 2, 0), ls2, {'dy': 15, 'cls': 'hot' if hot == 's2' else ''})]
    return it

def divseg(L, parts, ang=32, labs=True):
    """divisió del segment AB (longitud L) en parts proporcionals a «parts» amb el teorema de Tales"""
    tot = sum(parts); a = math.radians(ang); u = L * 0.95 / tot
    A = (0, 0); B = (L, 0)
    Pk = []; acc = 0
    for k in parts: acc += k; Pk.append((acc * u * math.cos(a), acc * u * math.sin(a)))
    it = [('seg', A, B, 'hl'), ('seg', A, (Pk[-1][0] * 1.08, Pk[-1][1] * 1.08), 'tv'), ('seg', Pk[-1], B, 'par')]
    acc = 0
    for i, k in enumerate(parts[:-1]):
        acc += k; X = (L * acc / tot, 0)
        it += [('seg', Pk[i], X, 'par'), ('dot', X)]
    # marques de la unitat a la semirecta auxiliar
    for j in range(1, tot + 1): it.append(('dot', (j * u * math.cos(a), j * u * math.sin(a)), 'sm'))
    it += [('dot', A), ('dot', B), ('txt', A, 'A', {'dx': -8, 'a': 'end'}), ('txt', B, 'B', {'dx': 8, 'a': 'start'})]
    if labs:
        acc = 0
        for k in parts:
            x0 = L * acc / tot; acc += k; x1 = L * acc / tot
            it.append(('txt', ((x0 + x1) / 2, 0), fnum(L * k / tot), {'dy': 16}))
    return it

def simpair(pts, k, labs1=None, labs2=None, gap=1.5, names=('F', 'F′')):
    """figura i la seua ampliació/reducció de raó k, l'una al costat de l'altra"""
    xs = [p[0] for p in pts]; w = max(xs) - min(xs); x0 = min(xs)
    Q = [((p[0] - x0) * k + x0 + w + gap, p[1] * k) for p in pts]
    it = [('poly', pts, 'gf'), ('poly', Q, 'tr')]
    for lb, P_ in ((labs1, pts), (labs2, Q)):
        if lb:
            n = len(P_)
            cx = sum(p[0] for p in P_) / n; cy = sum(p[1] for p in P_) / n
            for i, t in enumerate(lb):
                if not t: continue
                A, B = P_[i], P_[(i + 1) % n]
                M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2); dx, dy = M[0] - cx, M[1] - cy; d = math.hypot(dx, dy) or 1
                it.append(('txt', (M[0] + dx / d * 0.45, M[1] + dy / d * 0.45), t, {}))
    return it

def tri_sides(a, b, c, X=0, cls='tr', labs=None, angs=None):
    """triangle de costats a (BC), b (CA), c (AB) amb la base BC horitzontal i B a l'origen desplaçat X"""
    B = (X, 0); C = (X + a, 0); xA = (a * a + c * c - b * b) / (2 * a); A = (X + xA, math.sqrt(max(c * c - xA * xA, 0)))
    it = [('poly', [A, B, C], cls)]
    if labs:
        for (P, Q, sd), t in zip(((B, C, 0), (C, A, 1), (A, B, -1)), labs):
            M = ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
            it.append(('txt', M, t, {'dy': 15} if sd == 0 else {'dx': 9 * sd, 'a': 'start' if sd > 0 else 'end'}))
    if angs:
        for V, t, a0, a1 in ((A, angs[0], math.degrees(math.atan2(B[1] - A[1], B[0] - A[0])), math.degrees(math.atan2(C[1] - A[1], C[0] - A[0]))),
                             (B, angs[1], 0, math.degrees(math.atan2(A[1], A[0] - X))), (C, angs[2], math.degrees(math.atan2(A[1], A[0] - C[0])), 180)):
            if not t: continue
            if a1 < a0: a0, a1 = a1, a0
            r = 0.16 * a
            it.append(('arc', V, r, a0, a1, 'ang'))
            m = math.radians((a0 + a1) / 2)
            it.append(('txt', (V[0] + 2.3 * r * math.cos(m), V[1] + 2.3 * r * math.sin(m)), t, {'cls': 'ang'}))
    return it, (A, B, C)

def inacc_tales(labs=('x', 'd', 'a', 'b'), hot='x'):
    """distància d'un punt B a un punt inaccessible A (l'altra riba) amb triangles en posició de Tales:
    B′ darrere de B en la recta AB (BB′ = d), C sobre la perpendicular en B (BC = a) i C′ sobre la perpendicular en B′
    (B′C′ = b), amb A, C i C′ alineats. Dibuix no a escala: les etiquetes porten les mesures."""
    X, d, a = 6.0, 2.6, 2.4
    b = a * (X + d) / X
    A, B, B1, C, C1 = (0, X), (0, 0), (0, -d), (a, 0), (b, -d)
    it = [('poly', [(-1.4, 0.3), (b + 1.2, 0.3), (b + 1.2, X - 0.3), (-1.4, X - 0.3)], 'water'),
          ('seg', (-1.4, 0), (b + 1.2, 0), 'axis'), ('seg', (-1.4, X), (b + 1.2, X), 'axis'),
          ('poly', [A, B1, C1], 'gf'), ('poly', [A, B, C], 'tr'), ('seg', A, C1, 'ray'),
          ('seg', A, B, 'hl'), ('ra', B, A, C), ('ra', B1, A, C1)]
    for P in (A, B, B1, C, C1): it.append(('dot', P))
    it += [('txt', A, 'A', {'dx': -8, 'a': 'end', 'dy': -4}), ('txt', B, 'B', {'dx': -8, 'a': 'end', 'dy': 12}), ('txt', B1, 'B′', {'dx': -8, 'a': 'end'}),
           ('txt', C, 'C', {'dx': 8, 'a': 'start', 'dy': 12}), ('txt', C1, 'C′', {'dx': 8, 'a': 'start'})]
    it += [('txt', (0, X / 2), labs[0], {'dx': -8, 'a': 'end', 'cls': 'hot' if hot == 'x' else ''}),
           ('txt', (0, -d / 2), labs[1], {'dx': -8, 'a': 'end', 'cls': 'hot' if hot == 'd' else ''}),
           ('txt', (a / 2, 0), labs[2], {'dy': -6, 'cls': 'hot' if hot == 'a' else ''}),
           ('txt', (b / 2, -d), labs[3], {'dy': 15, 'cls': 'hot' if hot == 'b' else ''})]
    return it

def inacc_cross(labs=('x', '', '', ''), hot='x'):
    """distància AB a través d'un riu amb dos triangles rectangles oposats pel vèrtex C: BC, CD i DE es mesuren a la riba"""
    A, B, C, D, E = (0, 9), (0, 0), (6, 0), (8, 0), (8, -3)
    it = [('poly', [(-1, 0.25), (9, 0.25), (9, 8.75), (-1, 8.75)], 'water'), ('poly', [A, B, C], 'gf'), ('poly', [C, D, E], 'tr'),
          ('seg', A, E, 'ray'), ('seg', (-1, 0), (9, 0), 'axis'), ('ra', B, (1, 0), (0, 1)), ('ra', D, (7, 0), (8, -1))]
    for P in (A, B, C, D, E): it.append(('dot', P))
    it += [('txt', A, 'A', {'dx': -8, 'a': 'end'}), ('txt', B, 'B', {'dx': -8, 'a': 'end'}), ('txt', C, 'C', {'dx': -6, 'dy': -8, 'a': 'end'}),
           ('txt', D, 'D', {'dx': 8, 'a': 'start', 'dy': -6}), ('txt', E, 'E', {'dx': 8, 'a': 'start'})]
    it += [('txt', (0, 4.5), labs[0], {'dx': -8, 'a': 'end', 'cls': 'hot' if hot == 'x' else ''}), ('txt', (3, 0), labs[1], {'dy': 15}),
           ('txt', (7, 0), labs[2], {'dy': -8}), ('txt', (8, -1.5), labs[3], {'dx': 8, 'a': 'start'})]
    return it

def alt_fig(m, n, labs=None, hot=None):
    """triangle rectangle ABC (angle recte en A) amb la hipotenusa BC horitzontal i l'altura AH: BH = m, HC = n.
    labs: {'a', 'b', 'c', 'h', 'm', 'n'} (b = AC, c = AB)"""
    a = m + n; h = math.sqrt(m * n)
    A, B, C, H = (m, h), (0, 0), (a, 0), (m, 0)
    it = [('poly', [A, B, H], 'gf'), ('poly', [A, H, C], 'tr'), ('seg', A, H, 'hl'), ('ra', H, A, C), ('ra', A, B, C)]
    for P in (A, B, C, H): it.append(('dot', P))
    it += [('txt', A, 'A', {'dy': -8}), ('txt', B, 'B', {'dx': -8, 'a': 'end'}), ('txt', C, 'C', {'dx': 8, 'a': 'start'}), ('txt', H, 'H', {'dy': 15})]
    if labs:
        def o(k, **kw):
            if hot and k in hot.split(','): kw['cls'] = 'hot'
            return kw
        pos = {'m': ((m / 2, 0), o('m', dy=15)), 'n': ((m + n / 2, 0), o('n', dy=15)), 'h': ((m, h / 2), o('h', dx=6, a='start')),
               'c': (off(B, A, 0.07 * a), o('c')), 'b': (off(A, C, 0.07 * a), o('b')), 'a': ((a / 2, 0), o('a', dy=30))}
        for k, t in labs.items():
            P, op = pos[k]; it.append(('txt', P, t, op))
    return it

def off(A, B, d):
    """punt mitjà d'AB desplaçat d cap a l'esquerra (mirant d'A a B)"""
    M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2); dx, dy = B[0] - A[0], B[1] - A[1]; nn = math.hypot(dx, dy)
    return (M[0] - dy / nn * d, M[1] + dx / nn * d)
