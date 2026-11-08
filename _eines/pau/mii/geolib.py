# Eines per a les solucions PAU de geometria de 2n Batx MII (unitats 3 i 4).
# Tot es calcula amb fraccions exactes; les distàncies i els angles es guarden al quadrat
# (o com a cosinus al quadrat) i es mostren simplificats: a√b/c.
import math
import re
from fractions import Fraction as F

CHK = [0]


def ck(c, msg="comprovació"):
    assert c, msg
    CHK[0] += 1


# ---------- nombres ----------
def nm(x):
    """fracció o enter en TeX"""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)


def tn(x):
    """fracció petita (\\tfrac) per a coordenades"""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ('-' if x < 0 else '') + r'\tfrac{%d}{%d}' % (abs(x.numerator), x.denominator)


def ap(x, k=2):
    s = '%.*f' % (k, float(x))
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    if s == '-0':
        s = '0'
    return s.replace('.', '{,}')


def sqf(n):
    """n = s^2 r amb r lliure de quadrats"""
    n = int(n)
    s, r, p = 1, 1, 2
    while p * p <= n:
        while n % (p * p) == 0:
            n //= p * p
            s *= p
        if n % p == 0:
            n //= p
            r *= p
        p += 1
    return s, r * n


def surd(x2):
    """√x2 = c·√r (c fracció, r enter lliure de quadrats)"""
    x2 = F(x2)
    assert x2 >= 0
    if x2 == 0:
        return F(0), 1
    p, q = x2.numerator, x2.denominator
    s, r = sqf(p * q)
    return F(s, q), r


def rq(x2, sign=1):
    """√x2 simplificada en TeX"""
    c, r = surd(x2)
    if c == 0:
        return '0'
    a, b = c.numerator, c.denominator
    sg = '-' if sign < 0 else ''
    if r == 1:
        return sg + nm(c)
    core = (r'\sqrt{%d}' % r) if a == 1 else (r'%d\sqrt{%d}' % (a, r))
    if b == 1:
        return sg + core
    return sg + r'\frac{%s}{%d}' % (core, b)


def sqv(n):
    """\\sqrt{n} tal qual (n enter o fracció)"""
    n = F(n)
    if n.denominator == 1:
        return r'\sqrt{%d}' % n.numerator
    return r'\sqrt{%s}' % nm(n)


def isq(x2):
    c, r = surd(x2)
    return r == 1


def dist_tex(num, den2):
    """|num|/√den2 simplificat (den2 = |n|²)"""
    return rq(F(num) ** 2 / F(den2))


# ---------- vectors ----------
def V(*a):
    return tuple(F(x) for x in a)


def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def sc(k, u): return tuple(F(k) * a for a in u)
def dot(u, v): return sum(a * b for a, b in zip(u, v))
def n2(u): return dot(u, u)
def mid(A, B): return tuple((a + b) / 2 for a, b in zip(A, B))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def det3(u, v, w): return dot(u, cross(v, w))


def par(u, v): return all(x == 0 for x in cross(u, v))
def zero(u): return all(x == 0 for x in u)


def prim(u):
    """vector proporcional amb components enteres primeres entre si (primer no nul positiu)"""
    from math import gcd
    l = 1
    for x in u:
        l = l * x.denominator // gcd(l, x.denominator)
    w = [int(x * l) for x in u]
    g = 0
    for x in w:
        g = gcd(g, abs(x))
    g = g or 1
    w = [x // g for x in w]
    for x in w:
        if x != 0:
            if x < 0:
                w = [-y for y in w]
            break
    return tuple(F(x) for x in w)


def pv(u):
    return '(' + ','.join(nm(x) for x in u) + ')'


def pvt(u):
    return '(' + ',\\,'.join(tn(x) for x in u) + ')'


def crossx(u, v, nu=None, nv=None):
    """producte vectorial amb el determinant"""
    w = cross(u, v)
    return (r'\begin{vmatrix}\vec i&\vec j&\vec k\\ %s\\ %s\end{vmatrix}=%s'
            % ('&'.join(nm(x) for x in u), '&'.join(nm(x) for x in v), pv(w))), w


def detx(u, v, w):
    """determinant 3x3 (producte mixt)"""
    return r'\begin{vmatrix}%s\\ %s\\ %s\end{vmatrix}=%s' % (
        '&'.join(nm(x) for x in u), '&'.join(nm(x) for x in v), '&'.join(nm(x) for x in w), nm(det3(u, v, w)))


def modx(u):
    """|u|=√(a²+b²+c²)=..."""
    s = '+'.join(('(%s)^2' % nm(x)) if x < 0 or x.denominator != 1 else '%s^2' % nm(x) for x in u)
    return r'\sqrt{%s}=%s' % (s, rq(n2(u)))


# ---------- expressions lineals ----------
def lin(cs, vs=('x', 'y', 'z'), const=None):
    """a x + b y + c z (+ k) en TeX"""
    out = ''
    for c, v in zip(cs, vs):
        c = F(c)
        if c == 0:
            continue
        if c == 1:
            t = v
        elif c == -1:
            t = '-' + v
        else:
            t = nm(c) + v
        if out and not t.startswith('-'):
            out += '+'
        out += t
    if const is not None and F(const) != 0:
        k = nm(const)
        out += k if (k.startswith('-') or not out) else '+' + k
    return out or '0'


def aff(a, b, p=r'\lambda'):
    """a + b·p"""
    a, b = F(a), F(b)
    if b == 0:
        return nm(a)
    t = p if b == 1 else ('-' + p if b == -1 else nm(b) + p)
    if a == 0:
        return t
    return nm(a) + ('' if t.startswith('-') else '+') + t


# ---------- plans ----------
class Pl:
    """pla n·X + d = 0"""

    def __init__(self, n, d):
        n = tuple(F(x) for x in n)
        d = F(d)
        assert not zero(n)
        # coeficients enters, primers entre si, primer coeficient no nul positiu
        from math import gcd
        l = 1
        for x in n + (d,):
            l = l * x.denominator // gcd(l, x.denominator)
        w = [int(x * l) for x in n + (d,)]
        g = 0
        for x in w:
            g = gcd(g, abs(x))
        w = [x // g for x in w]
        if [x for x in w[:3] if x != 0][0] < 0:
            w = [-x for x in w]
        self.n = tuple(F(x) for x in w[:3])
        self.d = F(w[3])

    def ev(self, X): return dot(self.n, X) + self.d
    def has(self, X): return self.ev(X) == 0

    def tex(self):
        return lin(self.n, const=self.d) + '=0'

    def __eq__(self, o): return self.n == o.n and self.d == o.d


def pl_pn(P, n):
    """pla per P amb normal n"""
    return Pl(n, -dot(n, P))


def pl_puv(P, u, v):
    w = cross(u, v)
    assert not zero(w)
    return pl_pn(P, w)


def pl3(A, B, C):
    return pl_puv(A, sub(B, A), sub(C, A))


def pl_det(P, u, v):
    """explicació: det(X-P, u, v)=0"""
    return (r'\begin{vmatrix}x%s&y%s&z%s\\ %s\\ %s\end{vmatrix}=0'
            % (neg(P[0]), neg(P[1]), neg(P[2]), '&'.join(nm(x) for x in u), '&'.join(nm(x) for x in v)))


def neg(a):
    """-a com a sufix: x-3, x+2, x"""
    a = F(a)
    if a == 0:
        return ''
    return ('-' + nm(a)) if a > 0 else ('+' + nm(-a))


# ---------- rectes ----------
def par_tex(P, d, p=r'\lambda'):
    """equacions paramètriques en línia"""
    return r'x=%s,\ \ y=%s,\ \ z=%s' % (aff(P[0], d[0], p), aff(P[1], d[1], p), aff(P[2], d[2], p))


def par_cases(P, d, p=r'\lambda'):
    return r'\begin{cases}x=%s\\ y=%s\\ z=%s\end{cases}' % (aff(P[0], d[0], p), aff(P[1], d[1], p), aff(P[2], d[2], p))


def vec_tex(P, d, p=r'\lambda'):
    return r'(x,y,z)=%s+%s%s' % (pv(P), p, pv(d))


def cont_tex(P, d):
    """equació contínua (si algun component és 0 s'escriu igual, com fa la PAU)"""
    parts = []
    for v, a, b in zip('xyz', P, d):
        num = v + neg(a)
        if b == 1:
            parts.append(num)
        else:
            parts.append(r'\dfrac{%s}{%s}' % (num, nm(b)))
    return '='.join(parts)


def pt_on(P, d, t): return add(P, sc(t, d))


def solve2(a, b, c, d, e, f):
    """a x + b y = e ; c x + d y = f"""
    D = a * d - b * c
    if D == 0:
        return None
    return ((e * d - b * f) / D, (a * f - e * c) / D)


def line_pl(p1, p2, prefer=(2, 1, 0)):
    """recta intersecció de dos plans: (punt, director primitiu, coordenada anul·lada)"""
    d = cross(p1.n, p2.n)
    assert not zero(d), 'plans paral·lels'
    best = None
    for k in prefer:
        i, j = [t for t in range(3) if t != k]
        for val in (0, 1, -1, 2, -2, 3):
            s = solve2(p1.n[i], p1.n[j], p2.n[i], p2.n[j], -p1.d - p1.n[k] * val, -p2.d - p2.n[k] * val)
            if s is None:
                break
            P = [F(0)] * 3
            P[i], P[j], P[k] = s[0], s[1], F(val)
            P = tuple(P)
            ck(p1.has(P) and p2.has(P))
            if all(x.denominator == 1 for x in P):
                return P, prim(d), (k, val)
            if best is None:
                best = (P, prim(d), (k, val))
    assert best
    return best


def line_pl_tex(p1, p2, P, d, k, pn='R'):
    """explicació breu de com s'obté la recta intersecció"""
    var = 'xyz'[k[0]]
    return (r'Un director és $\vec n_1\times\vec n_2=%s\times%s=%s$, i per tant podem prendre $\vec d=%s$. '
            r'Per a un punt, fem $%s=%s$ i resolem el sistema: $%s%s$.'
            % (pv(p1.n), pv(p2.n), pv(cross(p1.n, p2.n)), pv(d), var, nm(k[1]), pn, pv(P)))


def meet_lp(P, d, pl):
    """paràmetre i punt de tall de recta i pla (None si paral·lels)"""
    den = dot(pl.n, d)
    if den == 0:
        return None
    t = -pl.ev(P) / den
    X = pt_on(P, d, t)
    ck(pl.has(X))
    return t, X


def meet_ll(P, d, Q, e):
    """P + t d = Q + s e"""
    w = sub(Q, P)
    if det3(w, d, e) != 0 or par(d, e):
        return None
    # resolem amb dues coordenades on el menor no s'anul·la
    for i, j in ((0, 1), (0, 2), (1, 2)):
        s = solve2(d[i], -e[i], d[j], -e[j], w[i], w[j])
        if s:
            t, u = s
            X = pt_on(P, d, t)
            ck(X == pt_on(Q, e, u))
            return t, u, X
    raise AssertionError


def pos_ll(P, d, Q, e):
    if par(d, e):
        return 'coincidents' if par(sub(Q, P), d) else 'paral·leles'
    return 'es tallen' if det3(sub(Q, P), d, e) == 0 else "s'encreuen"


# ---------- distàncies (al quadrat) ----------
def d2_pp(A, B): return n2(sub(A, B))
def d2_ppl(Q, pl): return pl.ev(Q) ** 2 / n2(pl.n)
def d2_pl(Q, P, d): return n2(cross(sub(Q, P), d)) / n2(d)
def d2_ll(P, d, Q, e): return det3(sub(Q, P), d, e) ** 2 / n2(cross(d, e))


def proj_pl(Q, pl):
    t = -pl.ev(Q) / n2(pl.n)
    X = pt_on(Q, pl.n, t)
    ck(pl.has(X))
    return t, X


def proj_line(Q, P, d):
    t = dot(sub(Q, P), d) / n2(d)
    X = pt_on(P, d, t)
    ck(dot(sub(Q, X), d) == 0)
    return t, X


def sym(Q, M): return sub(sc(2, M), Q)


# ---------- angles ----------
def deg(c):
    """angle (en graus) de cosinus c (float)"""
    return math.degrees(math.acos(max(-1.0, min(1.0, float(c)))))


def cos_tex(num, a2, b2):
    """|num|/(√a2·√b2) simplificat"""
    v2 = F(num) ** 2 / (F(a2) * F(b2))
    return rq(v2), v2


def ang(u, v, absval=True):
    """(tex del càlcul del cosinus, valor exacte al quadrat, graus)"""
    num = dot(u, v)
    if absval:
        num = abs(num)
    v2 = num ** 2 / (n2(u) * n2(v))
    g = deg(math.copysign(math.sqrt(float(v2)), float(num)))
    return v2, g


EXACT = '@@EX@@'


def gr(g, k=2):
    """graus; si l'angle és exacte (0, 30, 45, 60, 90...) es marca perquè s'escriga «=» en lloc de «≈»"""
    if abs(g - round(g)) < 1e-9 and round(g) % 15 == 0:
        return EXACT + '%d^\\circ' % round(g)
    return ap(g, k) + r'^\circ'


# ---------- HTML ----------
def mathsafe(h):
    return re.sub(r'\$\$.*?\$\$|\$[^$]*\$', lambda m: m.group(0).replace('<', r'\lt ').replace('>', r'\gt '), h, flags=re.S)


def steps(*items):
    return '<ol class="steps">' + ''.join('<li>%s</li>' % i for i in items if i) + '</ol>'


def res(t): return '<p class="res"><strong>Solució:</strong> %s</p>' % t


def ap_(t): return '<strong>%s</strong> ' % t


# ---------- passos explicats ----------
def pr_(a):
    a = F(a)
    return '(%s)' % nm(a) if a < 0 or a.denominator != 1 else nm(a)


def subst(pl, Q):
    """A·x0+B·y0+C·z0+D amb nombres"""
    out = ''
    for c, x in zip(pl.n, Q):
        if c == 0:
            continue
        t = (nm(c) if c not in (1, -1) else ('' if c == 1 else '-')) + (r'\cdot ' + pr_(x) if c not in (1, -1) else pr_(x))
        if out and not t.startswith('-'):
            out += '+'
        out += t
    if pl.d != 0:
        out += ('+' if pl.d > 0 else '') + nm(pl.d)
    return out


def sqn(u):
    """√(a²+b²+c²) amb nombres"""
    return r'\sqrt{%s}' % '+'.join(pr_(x) + '^2' for x in u if x != 0)


def dpl_x(Q, pl, Qn='P', pn=r'\pi'):
    """d(Q,π) explicada; torna (tex, d²)"""
    num = pl.ev(Q)
    d2 = num ** 2 / n2(pl.n)
    t = r'd(%s,%s)=\dfrac{|%s|}{%s}=\dfrac{%s}{%s}' % (Qn, pn, subst(pl, Q), sqn(pl.n), nm(abs(num)), sqv(n2(pl.n)))
    r = rq(d2)
    if r != r'\dfrac{%s}{%s}' % (nm(abs(num)), sqv(n2(pl.n))):
        t += '=' + r
    if not isq(d2):
        t += r'\approx ' + ap(math.sqrt(float(d2)))
    return t + r'\ \text{u}', d2


def dpr_x(Q, P, d, Qn='Q', Pn='P', rn='r'):
    """d(Q,r) amb el producte vectorial; torna (tex, d²)"""
    w = sub(Q, P)
    cx, c = crossx(w, d)
    d2 = n2(c) / n2(d)
    t = (r'$\overrightarrow{%s%s}=%s$, $\ \overrightarrow{%s%s}\times\vec d=%s$. '
         r'$$d(%s,%s)=\frac{|\overrightarrow{%s%s}\times\vec d|}{|\vec d|}=\frac{%s}{%s}=%s%s\ \text{u}$$'
         % (Pn, Qn, pv(w), Pn, Qn, cx, Qn, rn, Pn, Qn, sqv(n2(c)), sqv(n2(d)), rq(d2),
            '' if isq(d2) else r'\approx ' + ap(math.sqrt(float(d2)))))
    return t, d2


def dll_x(P, d, Q, e, Pn='P', Qn='Q', rn='r', sn='s'):
    """d(r,s) per a rectes que s'encreuen (producte mixt); torna (tex, d²)"""
    w = sub(Q, P)
    cx, c = crossx(d, e)
    m = det3(w, d, e)
    d2 = m ** 2 / n2(c)
    t = (r'$\overrightarrow{%s%s}=%s$, $\ [\overrightarrow{%s%s},\vec d_%s,\vec d_%s]=%s$, $\ \vec d_%s\times\vec d_%s=%s$. '
         r'$$d(%s,%s)=\frac{|[\overrightarrow{%s%s},\vec d_%s,\vec d_%s]|}{|\vec d_%s\times\vec d_%s|}=\frac{%s}{%s}=%s%s\ \text{u}$$'
         % (Pn, Qn, pv(w), Pn, Qn, rn, sn, detx(w, d, e), rn, sn, cx, rn, sn, Pn, Qn, rn, sn, rn, sn,
            nm(abs(m)), sqv(n2(c)), rq(d2), '' if isq(d2) else r'\approx ' + ap(math.sqrt(float(d2)))))
    return t, d2


def ang_x(u, v, kind='rr', un=r'\vec u', vn=r'\vec v'):
    """angle entre rectes ('rr'), plans ('pp'), recta-pla ('rp': sin) o vectors ('vv': amb signe)"""
    num = dot(u, v)
    a = num if kind == 'vv' else abs(num)
    c2 = num ** 2 / (n2(u) * n2(v))
    fn = r'\sin' if kind == 'rp' else r'\cos'
    g = math.degrees(math.asin(math.sqrt(float(c2)))) if kind == 'rp' else deg(math.copysign(math.sqrt(float(c2)), float(a)) if a != 0 else 0)
    bars = ('', '') if kind == 'vv' else ('|', '|')
    t = (r'%s\alpha=\frac{%s%s\cdot %s%s}{|%s|\,|%s|}=\frac{%s}{%s\cdot%s}'
         % (fn, bars[0], un, vn, bars[1], un, vn, nm(a), sqv(n2(u)), sqv(n2(v))))
    r = rq(c2, -1 if a < 0 else 1)
    t += '=' + r
    return t, c2, g


def feet(P, d, Q, e):
    """peus de la perpendicular comuna: X=P+λd, Y=Q+μe"""
    w = sub(Q, P)
    s = solve2(dot(d, d), -dot(e, d), dot(d, e), -dot(e, e), dot(w, d), dot(w, e))
    lam, mu = s
    X, Y = pt_on(P, d, lam), pt_on(Q, e, mu)
    ck(dot(sub(Y, X), d) == 0 and dot(sub(Y, X), e) == 0)
    return lam, mu, X, Y


def pencil_x(p1, p2, P, n1=r'\pi_1', n2_=r'\pi_2'):
    """pla del feix de p1, p2 que passa per P"""
    a, b = p1.ev(P), p2.ev(P)
    if b == 0:
        raise AssertionError('P és de p2')
    mu = -a / b
    pl = Pl(add(p1.n, sc(mu, p2.n)), p1.d + mu * p2.d)
    ck(pl.has(P))
    t = (r'Feix de plans per $r$: $(%s)+\mu(%s)=0$. Imposem que passe per $P$: $%s+\mu\cdot(%s)=0\Rightarrow\mu=%s$. '
         r'Substituint i simplificant: $\ %s$.'
         % (lin(p1.n, const=p1.d), lin(p2.n, const=p2.d), nm(a), nm(b), nm(mu), pl.tex()))
    return t, pl


def gp(P, d, p=r'\lambda'):
    """punt genèric de la recta: (a+bλ, ...)"""
    return '(' + ',\\,'.join(aff(P[i], d[i], p) for i in range(3)) + ')'
