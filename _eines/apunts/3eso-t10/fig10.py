# Figures de la Unitat 10 (Tales i semblança) per als apunts: llistes d'elements per a G() de comu.py.
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
