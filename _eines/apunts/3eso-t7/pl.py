# Funcions definides per trossos lineals (poligonals) i el seu estudi: domini, recorregut,
# creixement, extrems i continuïtat. El fan servir build.py (apunts) i fonts-latex/3eso-t7/genera.py (fitxa);
# app.js en té una còpia en JavaScript (FN7.study) que dona els mateixos resultats.
#
# Una funció és {'p': [tros, ...], 'pts': [(x, y), ...]}; cada tros és {'v': [(x, y), ...], 'l': e, 'r': e}
# amb e = 'c' (extrem tancat, punt ple), 'o' (obert, punt buit) o 'a' (fletxa: la recta continua).
from fractions import Fraction as Fr
INF = float('inf')

def F(*pieces, pts=()):
    """F(('c', [(0,1),(2,3)], 'o'), ...) -> funció"""
    return {'p': [{'l': l, 'v': [(Fr(a), Fr(b)) for a, b in v], 'r': r} for l, v, r in pieces], 'pts': [(Fr(a), Fr(b)) for a, b in pts]}

def slope(P, Q): return (Q[1] - P[1]) / (Q[0] - P[0])
def sgn(v): return (v > 0) - (v < 0)

# ---------- normalització: uneix els trossos que es toquen sense salt ----------
def norm(f):
    ps = [dict(l=p['l'], v=list(p['v']), r=p['r']) for p in f['p']]
    pts = list(f['pts'])
    ps.sort(key=lambda p: p['v'][0][0])
    for p in ps:
        assert all(p['v'][i][0] < p['v'][i + 1][0] for i in range(len(p['v']) - 1)), p
        assert len(p['v']) >= 2 or (p['l'] == p['r'] == 'c')
    changed = True
    while changed:
        changed = False
        for i in range(len(ps) - 1):
            A, B = ps[i], ps[i + 1]
            if A['r'] != 'a' and B['l'] != 'a' and A['v'][-1] == B['v'][0]:
                P = A['v'][-1]
                filled = A['r'] == 'c' or B['l'] == 'c' or P in pts
                if filled:
                    if P in pts: pts.remove(P)
                    ps[i] = dict(l=A['l'], v=A['v'] + B['v'][1:], r=B['r']); del ps[i + 1]
                    changed = True; break
    # punts aïllats que tapen un extrem obert
    for p in ps:
        if p['l'] == 'o' and p['v'][0] in pts: pts.remove(p['v'][0]); p['l'] = 'c'
        if p['r'] == 'o' and p['v'][-1] in pts: pts.remove(p['v'][-1]); p['r'] = 'c'
    # vèrtexs alineats (mateix pendent) no són vèrtexs de veritat
    for p in ps:
        v = p['v']; i = 1
        while i < len(v) - 1:
            if slope(v[i - 1], v[i]) == slope(v[i], v[i + 1]): del v[i]
            else: i += 1
    return {'p': ps, 'pts': pts}

# ---------- intervals: (a, b, tancat_a, tancat_b) ----------
def union(iv):
    iv = sorted(iv, key=lambda t: (t[0], not t[2]))
    out = []
    for a, b, ca, cb in iv:
        if out:
            A, B, CA, CB = out[-1]
            if a < B or (a == B and (CB or ca)):
                if b > B: out[-1] = (A, b, CA, cb)
                elif b == B: out[-1] = (A, B, CA, CB or cb)
                continue
        out.append((a, b, ca, cb))
    return out

def value(f, xv):
    xv = Fr(xv)
    for p in f['p']:
        v = p['v']
        for i in range(len(v) - 1):
            P, Q = v[i], v[i + 1]
            inP = i > 0 or p['l'] in 'ca'; inQ = i < len(v) - 2 or p['r'] in 'ca'
            if P[0] < xv < Q[0] or (xv == P[0] and inP) or (xv == Q[0] and inQ):
                return P[1] + slope(P, Q) * (xv - P[0])
        if len(v) == 1 and xv == v[0][0]: return v[0][1]
        if p['l'] == 'a' and xv < v[0][0]: return v[0][1] + slope(v[0], v[1]) * (xv - v[0][0])
        if p['r'] == 'a' and xv > v[-1][0]: return v[-1][1] + slope(v[-2], v[-1]) * (xv - v[-1][0])
    for P in f['pts']:
        if P[0] == xv: return P[1]
    return None

def domain(f):
    iv = []
    for p in f['p']:
        v = p['v']
        a = -INF if p['l'] == 'a' else v[0][0]; b = INF if p['r'] == 'a' else v[-1][0]
        iv.append((a, b, p['l'] == 'c', p['r'] == 'c'))
    iv += [(P[0], P[0], True, True) for P in f['pts']]
    return union(iv)

def rng(f):
    iv = []
    for p in f['p']:
        v = p['v']
        if len(v) == 1: iv.append((v[0][1], v[0][1], True, True)); continue
        for i in range(len(v) - 1):
            P, Q = v[i], v[i + 1]
            inP = i > 0 or p['l'] in 'ca'; inQ = i < len(v) - 2 or p['r'] in 'ca'
            if P[1] == Q[1]: iv.append((P[1], P[1], True, True))
            elif P[1] < Q[1]: iv.append((P[1], Q[1], inP, inQ))
            else: iv.append((Q[1], P[1], inQ, inP))
        if p['l'] == 'a':
            s = sgn(slope(v[0], v[1])); y0 = v[0][1]
            iv.append((-INF, y0, False, True) if s > 0 else (y0, INF, True, False) if s < 0 else (y0, y0, True, True))
        if p['r'] == 'a':
            s = sgn(slope(v[-2], v[-1])); y0 = v[-1][1]
            iv.append((y0, INF, True, False) if s > 0 else (-INF, y0, False, True) if s < 0 else (y0, y0, True, True))
    iv += [(P[1], P[1], True, True) for P in f['pts']]
    return union(iv)

def mono(f):
    """{'+': [intervals oberts], '-': [...], '0': [...]}"""
    out = {'+': [], '-': [], '0': []}
    for p in f['p']:
        v = p['v']
        if len(v) < 2: continue
        segs = []
        if p['l'] == 'a': segs.append((-INF, v[0][0], sgn(slope(v[0], v[1]))))
        segs += [(v[i][0], v[i + 1][0], sgn(slope(v[i], v[i + 1]))) for i in range(len(v) - 1)]
        if p['r'] == 'a': segs.append((v[-1][0], INF, sgn(slope(v[-2], v[-1]))))
        run = list(segs[0])
        for a, b, s in segs[1:] + [(None, None, None)]:
            if s == run[2]: run[1] = b; continue
            out['+' if run[2] > 0 else '-' if run[2] < 0 else '0'].append((run[0], run[1], False, False))
            run = [a, b, s]
    return out

def extrema(f):
    """màxims i mínims relatius (punts on canvia el creixement, amb la funció contínua)"""
    mx, mn = [], []
    for p in f['p']:
        v = p['v']
        for i in range(len(v)):
            if (i == 0 and p['l'] != 'a') or (i == len(v) - 1 and p['r'] != 'a'): continue
            sl = sgn(slope(v[i - 1], v[i])) if i > 0 else sgn(slope(v[0], v[1]))
            sr = sgn(slope(v[i], v[i + 1])) if i < len(v) - 1 else sgn(slope(v[-2], v[-1]))
            if sl > 0 and sr < 0: mx.append(v[i])
            if sl < 0 and sr > 0: mn.append(v[i])
    return mx, mn

def absolute(f):
    """(màxim absolut, mínim absolut): (valor, [x on s'assoleix]) o None"""
    R = rng(f)
    def where(yv):
        xs = set()
        for p in f['p']:
            for i, P in enumerate(p['v']):
                inc = (0 < i < len(p['v']) - 1) or (i == 0 and p['l'] in 'ca') or (i == len(p['v']) - 1 and p['r'] in 'ca')
                if inc and P[1] == yv: xs.add(P[0])
        for P in f['pts']:
            if P[1] == yv: xs.add(P[0])
        return sorted(xs)
    hi, lo = R[-1], R[0]
    M = (hi[1], where(hi[1])) if hi[1] != INF and hi[3] else None
    m = (lo[0], where(lo[0])) if lo[0] != -INF and lo[2] else None
    return M, m

def disc(f):
    """discontinuïtats dins del domini: [(x, 'salt' | 'forat' | 'aillat')]"""
    out = []
    ps = f['p']
    xs = sorted({p['v'][0][0] for p in ps if p['l'] != 'a'} | {p['v'][-1][0] for p in ps if p['r'] != 'a'} | {P[0] for P in f['pts']})
    for xv in xs:
        left = [p['v'][-1][1] for p in ps if p['r'] != 'a' and p['v'][-1][0] == xv and len(p['v']) > 1]
        right = [p['v'][0][1] for p in ps if p['l'] != 'a' and p['v'][0][0] == xv and len(p['v']) > 1]
        inside = [p for p in ps if (p['l'] == 'a' or p['v'][0][0] < xv) and (p['r'] == 'a' or p['v'][-1][0] > xv)]
        val = value(f, xv)
        if inside:
            if val is not None and any(P[0] == xv for P in f['pts']): out.append((xv, 'forat'))
            continue
        if left and right:
            out.append((xv, 'salt' if left[0] != right[0] else 'forat'))
        elif (left or right) and val is not None and not any(
                (p['v'][-1][0] == xv and p['r'] == 'c') or (p['v'][0][0] == xv and p['l'] == 'c') for p in ps):
            out.append((xv, 'forat'))
        elif not left and not right and val is not None:
            out.append((xv, 'aillat'))
    return out

def study(f):
    g = norm(f)
    mx, mn = extrema(g)
    M, m = absolute(g)
    return dict(dom=domain(g), rec=rng(g), mono=mono(g), max=mx, min=mn, amax=M, amin=m, disc=disc(g))

# ---------- escriptura en TeX ----------
def num(v, comma='{,}'):
    if v == INF: return r'+\infty'
    if v == -INF: return r'-\infty'
    v = Fr(v)
    if v.denominator == 1: return str(v.numerator)
    d = float(v)
    s = ('%g' % d)
    assert Fr(s) == v, v
    return s.replace('.', comma)

def ivtex(I, comma='{,}', sep=r',\,'):
    a, b, ca, cb = I
    if a == b: return r'\{%s\}' % num(a, comma)
    return ('[' if ca else '(') + num(a, comma) + sep + num(b, comma) + (']' if cb else ')')

def settex(iv, comma='{,}', sep=r',\,'):
    if not iv: return r'\varnothing'
    if len(iv) == 1 and iv[0][0] == -INF and iv[0][1] == INF: return r'\mathbb{R}'
    # ℝ − {a}
    if len(iv) == 2 and iv[0][0] == -INF and iv[1][1] == INF and iv[0][1] == iv[1][0] and not iv[0][3] and not iv[1][2]:
        return r'\mathbb{R}-\{%s\}' % num(iv[0][1], comma)
    # punts solts seguits: {1, 2, 3}
    parts, pend = [], []
    for I in iv + [None]:
        if I and I[0] == I[1]: pend.append(num(I[0], comma)); continue
        if pend: parts.append(r'\{%s\}' % sep.join(pend)); pend = []
        if I: parts.append(ivtex(I, comma, sep))
    return r'\cup '.join(parts)

def pttex(P, comma='{,}'): return '(%s,\\,%s)' % (num(P[0], comma), num(P[1], comma))

# ---------- comprovació numèrica (mostreig) ----------
def check(f, lo=-30, hi=30, n=6000):
    """compara study() amb un mostreig de la funció"""
    import math
    s = study(f)
    xs = [lo + (hi - lo) * Fr(i, n) for i in range(n + 1)]
    xs += [P[0] for P in f['pts']] + [P[0] for p in f['p'] for P in p['v']]
    def inset(xv, iv): return any((a < xv < b) or (xv == a and ca) or (xv == b and cb) or (a == b == xv) for a, b, ca, cb in iv)
    for xv in xs:
        val = value(f, xv)
        assert (val is not None) == inset(xv, s['dom']), ('dom', xv, val, s['dom'])
        if val is not None: assert inset(val, s['rec']), ('rec', xv, val, s['rec'])
    for key, sg in (('+', 1), ('-', -1), ('0', 0)):
        for a, b, _, _ in s['mono'][key]:
            a2 = max(a, lo); b2 = min(b, hi)
            pts = [a2 + (b2 - a2) * Fr(i + 1, 41) for i in range(40)]
            vals = [value(f, t) for t in pts]
            assert all(v is not None for v in vals), (key, a, b)
            assert all(sgn(vals[i + 1] - vals[i]) == sg for i in range(len(vals) - 1)), (key, a, b)
    for P in s['max'] + s['min']:
        assert value(f, P[0]) == P[1]
        for d in (Fr(1, 100), Fr(1, 1000)):
            l, r = value(f, P[0] - d), value(f, P[0] + d)
            if P in s['max']: assert l < P[1] and r < P[1], P
            else: assert l > P[1] and r > P[1], P
    for t in ('amax', 'amin'):
        if s[t]:
            yv, at = s[t]
            for xv in xs:
                val = value(f, xv)
                if val is not None: assert (val <= yv) if t == 'amax' else (val >= yv), (t, xv)
            for xv in at: assert value(f, xv) == yv
    return s
