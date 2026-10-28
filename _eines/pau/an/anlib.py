# Eines per a les solucions PAU d'anàlisi (unitats 4-8): polinomis i funcions racionals amb fraccions exactes,
# estudi complet d'una funció, funcions a trossos, integrals i àrees, i gràfiques en SVG.
# Les solucions són HTML amb fórmules KaTeX, com les de ../pr (SOL, st, L, ck).
import math, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pr'))
from comu import st, L, ck, CHK, p10  # noqa: E402,F401


def mathsafe(h):
    """dins de les fórmules, < i > es convertixen en \\lt i \\gt perquè l'HTML no els prenga per etiquetes"""
    import re
    return re.sub(r'\$\$.*?\$\$|\$[^$]*\$', lambda m: m.group(0).replace('<', r'\lt ').replace('>', r'\gt '), h, flags=re.S)


def SOL(items, res):
    """llista de passos numerats i resultat final (les gràfiques soltes no porten número)"""
    h = '<ol class="steps">'
    for i in items:
        h += ('<li style="list-style:none">%s</li>' if i.startswith('<svg') else '<li>%s</li>') % i
    return mathsafe(h + '</ol><p class="res"><strong>Solució:</strong> ' + res + '</p>')

INF = float('inf')


# ---------- nombres ----------
def nm(x, k=6):
    """nombre en TeX: enter, decimal exacte curt o fracció"""
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    if p10(x.denominator) and x.denominator <= 10 ** k:
        s = ('%.*f' % (k, float(x))).rstrip('0').rstrip('.')
        return s.replace('.', '{,}')
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)


def nmv(x):
    """valor d'una funció o arrel: decimal només si té com a molt tres xifres decimals, si no fracció"""
    x = F(x)
    if x.denominator != 1 and 1000 % x.denominator == 0 and x.denominator in (2, 4, 5, 10, 20, 25, 50, 100):
        return nm(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)


def nmf(x):
    """fracció (o enter)"""
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)


def ap(x, k=2):
    """valor aproximat amb coma decimal"""
    s = ('%.*f' % (k, float(x)))
    if '.' in s: s = s.rstrip('0').rstrip('.')
    if s == '-0': s = '0'
    return s.replace('.', '{,}')


def nv(x, k=2):
    """valor exacte i, si cal, aproximat"""
    x = F(x)
    if x.denominator == 1 or (p10(x.denominator) and x.denominator <= 10 ** 4): return nm(x)
    return nm(x) + r'\approx ' + ap(x, k)


def pt(x, y): return r'(%s,\,%s)' % (x if isinstance(x, str) else nmv(x), y if isinstance(y, str) else nmv(y))


# ---------- polinomis ----------
class P:
    """polinomi amb coeficients Fraction; c[i] és el coeficient de x^i"""
    def __init__(self, *hi, v='x'):
        if len(hi) == 1 and isinstance(hi[0], list): c = [F(t) for t in hi[0]]
        else: c = [F(t) if not isinstance(t, float) else F(str(t)) for t in reversed(hi)]
        while len(c) > 1 and c[-1] == 0: c.pop()
        self.c = c or [F(0)]; self.v = v

    @staticmethod
    def of(c, v='x'): return P(list(c), v=v)
    @property
    def deg(self): return len(self.c) - 1 if any(self.c) else -1
    @property
    def lead(self): return self.c[-1]
    def iszero(self): return not any(self.c)

    def __add__(s, o):
        o = o if isinstance(o, P) else P(o)
        n = max(len(s.c), len(o.c))
        return P.of([(s.c[i] if i < len(s.c) else 0) + (o.c[i] if i < len(o.c) else 0) for i in range(n)], s.v)
    __radd__ = __add__
    def __neg__(s): return P.of([-t for t in s.c], s.v)
    def __sub__(s, o): return s + (-(o if isinstance(o, P) else P(o)))
    def __rsub__(s, o): return (-s) + o
    def __mul__(s, o):
        if not isinstance(o, P): o = P(o)
        r = [F(0)] * (len(s.c) + len(o.c) - 1)
        for i, a in enumerate(s.c):
            for j, b in enumerate(o.c): r[i + j] += a * b
        return P.of(r, s.v)
    __rmul__ = __mul__
    def __pow__(s, n):
        r = P(1, v=s.v)
        for _ in range(n): r = r * s
        return r
    def __eq__(s, o): return isinstance(o, P) and s.c == o.c
    def __call__(s, x):
        if isinstance(x, float):
            r = 0.0
            for t in reversed(s.c): r = r * x + float(t)
            return r
        x = F(x); r = F(0)
        for t in reversed(s.c): r = r * x + t
        return r
    def d(s): return P.of([i * s.c[i] for i in range(1, len(s.c))] or [0], s.v)
    def prim(s): return P.of([0] + [s.c[i] / (i + 1) for i in range(len(s.c))], s.v)
    def divmod(s, o):
        a = list(s.c); q = [F(0)] * max(1, len(a) - len(o.c) + 1)
        while len(a) >= len(o.c) and any(a):
            k = a[-1] / o.c[-1]; sh = len(a) - len(o.c); q[sh] = k
            for i, t in enumerate(o.c): a[i + sh] -= k * t
            a.pop()
            while len(a) > 1 and a[-1] == 0: a.pop()
        return P.of(q, s.v), P.of(a or [0], s.v)
    def monic(s): return P.of([t / s.lead for t in s.c], s.v)
    def scale(s, k): return P.of([t * k for t in s.c], s.v)

    def tex(s, v=None, frac_ok=True, dec=True):
        """dec=False: els coeficients no enters s'escriuen com a fracció (x^3/3) encara que siguen decimals exactes"""
        v = v or s.v; out = []
        for i in range(len(s.c) - 1, -1, -1):
            a = s.c[i]
            if a == 0: continue
            sg = '-' if a < 0 else '+'; a = abs(a)
            mon = '' if i == 0 else (v if i == 1 else ('%s^%d' if i < 10 else '%s^{%d}') % (v, i))
            co = nm(a)
            fr_ = a.denominator != 1 and (not dec or not p10(a.denominator))
            if i > 0 and a == 1: co = ''
            elif i > 0 and fr_ and frac_ok:
                co = ''; mon = r'\frac{%s%s}{%d}' % ('' if a.numerator == 1 else a.numerator, mon, a.denominator)
            elif fr_: co = r'\frac{%d}{%d}' % (a.numerator, a.denominator)
            out.append((sg, co + mon))
        if not out: return '0'
        s0 = ('-' if out[0][0] == '-' else '') + out[0][1]
        return s0 + ''.join(sg + t for sg, t in out[1:])

    def __repr__(s): return s.tex()


X = P(1, 0)


def pgcd(a, b):
    while not b.iszero():
        _, r = a.divmod(b); a, b = b, r
    return a.monic() if not a.iszero() else a


# ---------- arrels ----------
class Rt:
    def __init__(s, val, tex, ex=None): s.val, s.tex, s.ex = val, tex, ex
    def __repr__(s): return s.tex


def isqrt_split(n):
    """sqrt(n) = k*sqrt(m) amb m lliure de quadrats"""
    k, m, d = 1, n, 2
    while d * d <= m:
        while m % (d * d) == 0: m //= d * d; k *= d
        d += 1
    return k, m


def qroots(a, b, c):
    """arrels reals de ax^2+bx+c (Fraction), exactes o amb arrel quadrada"""
    D = b * b - 4 * a * c
    if D < 0: return []
    if D == 0: return [Rt(float(-b / (2 * a)), nmf(-b / (2 * a)), -b / (2 * a))]
    num, den = D.numerator, D.denominator
    sq = math.isqrt(num * den)
    if sq * sq == num * den:
        r = sorted([(-b - F(sq, den)) / (2 * a), (-b + F(sq, den)) / (2 * a)])
        return [Rt(float(t), nmf(t), t) for t in r]
    k, m = isqrt_split(num * den)
    A = -b / (2 * a); B = abs(F(k, den) / (2 * a))
    Ld = A.denominator * B.denominator // math.gcd(A.denominator, B.denominator)
    Ai, Bi = int(A * Ld), int(B * Ld)
    out = []
    for sg in (-1, 1):
        val = float(A) + sg * float(B) * math.sqrt(m)
        bs = ('' if Bi == 1 else str(Bi)) + r'\sqrt{%d}' % m
        if Ai == 0: t = ('-' if sg < 0 else '') + bs
        else: t = '%d%s%s' % (Ai, '-' if sg < 0 else '+', bs)
        if Ld != 1:
            if Ai == 0: t = ('-' if sg < 0 else '') + r'\frac{%s}{%d}' % (bs, Ld)
            else: t = r'\frac{%s}{%d}' % (t, Ld)
        out.append(Rt(val, t))
    return sorted(out, key=lambda r: r.val)


def factor(p):
    """p = k * prod (x-r)^m * resta; torna (k, [(Fraction r, m)], resta mònica sense arrels racionals)"""
    k = p.lead; q = p.monic(); rts = []
    while q.deg >= 1:
        L = 1
        for t in q.c: L = L * t.denominator // math.gcd(L, t.denominator)
        ci = [int(t * L) for t in q.c]
        if ci[0] == 0:
            r = F(0)
        else:
            r = None
            a0, an = abs(ci[0]), abs(ci[-1])
            cands = sorted({F(sg * u, w) for u in divs(a0) for w in divs(an) for sg in (1, -1)}, key=lambda t: (abs(t), t))
            for t in cands:
                if q(t) == 0: r = t; break
        if r is None: break
        q, _ = q.divmod(P(1, -r)); rts.append(r)
    out = []
    for r in rts:
        if out and out[-1][0] == r: out[-1][1] += 1
        else: out.append([r, 1])
    out.sort(key=lambda t: t[0])
    return k, [tuple(t) for t in out], q


def divs(n):
    n = abs(n)
    return [d for d in range(1, n + 1) if n % d == 0] if n else [1]


def roots(p):
    """arrels reals diferents de p, ordenades (Rt)"""
    if p.deg <= 0: return []
    k, rs, rest = factor(p)
    out = [Rt(float(r), nmf(r), r) for r, m in rs]
    if rest.deg == 2: out += qroots(rest.c[2], rest.c[1], rest.c[0])
    elif rest.deg > 2:
        out += [Rt(v, ap(v, 3)) for v in nroots(rest)]
    elif rest.deg == 1: pass
    return sorted(out, key=lambda r: r.val)


def nroots(p):
    """arrels reals numèriques (bisecció) d'un polinomi sense arrels racionals"""
    B = 1 + max(abs(float(t / p.lead)) for t in p.c[:-1])
    xs = [-B + 2 * B * i / 4000 for i in range(4001)]; out = []
    for a, b in zip(xs, xs[1:]):
        fa, fb = p(a), p(b)
        if fa == 0: out.append(a)
        elif fa * fb < 0:
            for _ in range(80):
                m = (a + b) / 2
                if p(a) * p(m) <= 0: b = m
                else: a = m
            out.append((a + b) / 2)
    return out


def lin(r, v='x'):
    """factor lineal enter amb arrel r: x-2, 2x+1..."""
    r = F(r); q = r.denominator; p_ = r.numerator
    a = '' if q == 1 else str(q)
    if p_ == 0: return v if q == 1 else a + v
    return '%s%s%s%d' % (a, v, '-' if p_ > 0 else '+', abs(p_))


def ftex(p, v='x'):
    """polinomi factoritzat en TeX"""
    if p.deg <= 0: return nm(p.c[0])
    k, rs, rest = factor(p)
    parts = []; kk = k
    for r, m in rs:
        kk /= F(r).denominator ** m
        f = lin(r, v)
        if len(rs) == 1 and rest.deg == 0 and m == 1 and kk == 1: parts.append(f)
        else: parts.append(('(%s)' % f if not (f == v) else f) + ('^{%d}' % m if m > 1 else ''))
    if rest.deg > 0:
        g = pgcd(rest, rest.d()); sq = rest.divmod(g)[0].monic() if g.deg > 0 else rest
        m = rest.deg // sq.deg
        if sq ** m != rest: sq, m = rest, 1
        L = 1
        for t in sq.c: L = L * t.denominator // math.gcd(L, t.denominator)
        kk /= F(L) ** m
        if parts or kk != 1 or m > 1: parts.append('(%s)' % sq.scale(L).tex(v) + ('^{%d}' % m if m > 1 else ''))
        else: parts.append(sq.scale(L).tex(v))
    pre = '' if kk == 1 else ('-' if kk == -1 else nm(kk))
    s = pre + ''.join(parts)
    if s.startswith('-(') is False and s.startswith('-') and pre not in ('-',): pass
    return s


# ---------- funcions racionals ----------
class R:
    """f = num/den (polinomis)"""
    def __init__(s, num, den=None):
        s.n = num if isinstance(num, P) else P(num)
        s.q = den if den is not None else P(1)
        if not isinstance(s.q, P): s.q = P(s.q)
    @property
    def poly(s): return s.q.deg == 0
    def __call__(s, x):
        if isinstance(x, float):
            d = s.q(x)
            return s.n(x) / d if d != 0 else float('nan')
        return s.n(x) / s.q(x)
    def tex(s, v='x', dfrac=False):
        if s.poly: return (s.n.scale(1 / s.q.c[0])).tex(v)
        return r'\%s{%s}{%s}' % ('dfrac' if dfrac else 'frac', s.n.tex(v), s.q.tex(v))
    def d(s):
        if s.poly: return R(s.n.d().scale(1 / s.q.c[0]))
        N = s.n.d() * s.q - s.n * s.q.d(); D = s.q * s.q
        g = pgcd(N, D) if not N.iszero() else P(1)
        if g.deg > 0: N = N.divmod(g)[0]; D = D.divmod(g)[0]
        Lc = 1
        for t in N.c + D.c: Lc = Lc * t.denominator // math.gcd(Lc, t.denominator)
        N, D = N.scale(Lc), D.scale(Lc)
        G = 0
        for t in N.c + D.c: G = math.gcd(G, int(t))
        if D.lead < 0: G = -G
        return R(N.scale(F(1, G)), D.scale(F(1, G)))
    def fv(s, x):
        """valor exacte si x és racional, si no aproximat"""
        if isinstance(x, Rt): x = x.ex if x.ex is not None else x.val
        if isinstance(x, float): return s(x)
        return s(F(x))


def sgn(x): return '+' if x > 0 else ('-' if x < 0 else '0')


def ivl(a, b, ca=False, cb=False):
    """interval en TeX (a, b: Rt, nombre, text o ±inf)"""
    def t(x):
        if x == -INF: return r'-\infty'
        if x == INF: return r'+\infty'
        return x.tex if isinstance(x, Rt) else (x if isinstance(x, str) else nm(x))
    return '%s%s,\\,%s%s' % ('[' if ca else '(', t(a), t(b), ']' if cb else ')')


def vval(x): return x.val if isinstance(x, Rt) else (x if isinstance(x, float) else float(x))


def union(ivs): return r'\cup'.join(ivs) if ivs else r'\varnothing'


# ---------- taula de signes ----------
def taula_signes(cuts, fsign, labels=None, row2=None, excl=()):
    """cuts: punts de tall (Rt) ordenats; fsign(x float) -> signe de f'. Torna (html, [(a,b,signe)])"""
    pts = [-INF] + list(cuts) + [INF]; ivs = []
    for a, b in zip(pts, pts[1:]):
        va, vb = vval(a), vval(b)
        if va == -INF: m = vb - 1
        elif vb == INF: m = va + 1
        else: m = (va + vb) / 2
        ivs.append((a, b, fsign(m)))
    return taula_html(ivs, labels), ivs


def taula_html(ivs, labels=None, row1=r"f'(x)", row2='f(x)'):
    h = '<div class="tbl"><table><tr><th>$x$</th>' + ''.join('<td>$%s$</td>' % ivl(a, b) for a, b, _ in ivs) + '</tr>'
    h += '<tr><th>$%s$</th>' % row1 + ''.join('<td>$%s$</td>' % s for _, _, s in ivs) + '</tr>'
    h += '<tr><th>$%s$</th>' % row2 + ''.join('<td>%s</td>' % ('↗' if s == '+' else '↘') for _, _, s in ivs) + '</tr></table></div>'
    return h


# ---------- estudi complet d'una funció racional ----------
def estudi(f, lab=None, name='f', graf=True, xr=None, yr=None, asim=True, extra_pts=(), only=None, v='x', obliq=True, dline=None, dt=None):
    """passos de l'estudi de f (R). lab: etiquetes dels apartats {'dom','tall','asi','mon','ext','gra'}"""
    lab = lab or {}
    def L_(k, t): return st(((lab[k] + ' ') if lab.get(k) else '') + t)
    S = []; res = {}
    num, den = f.n, f.q
    poles = [] if f.poly else roots(den)
    fx = '%s(%s)' % (name, v)
    # domini
    if 'dom' in lab or only is None:
        if f.poly:
            S.append(L_('dom', 'Domini.') + r' És una funció polinòmica: $\mathrm{Dom}\,%s=\mathbb{R}$.' % name)
            res['dom'] = r'\mathbb{R}'
        elif not poles:
            S.append(L_('dom', 'Domini.') + r' El denominador $%s$ no s’anul·la mai, per tant $\mathrm{Dom}\,%s=\mathbb{R}$.' % (den.tex(v), name))
            res['dom'] = r'\mathbb{R}'
        else:
            dz = r'\{' + ',\\ '.join(r.tex for r in poles) + r'\}'
            S.append(L_('dom', 'Domini.') + r' Anul·lem el denominador: $%s=0\iff %s$. Per tant $\mathrm{Dom}\,%s=\mathbb{R}-%s$.'
                     % (dt or den.tex(v), ',\\ '.join('%s=%s' % (v, r.tex) for r in poles), name, dz))
            res['dom'] = r'\mathbb{R}-' + dz
    # talls
    if 'tall' in lab or 'dom' in lab or only is None:
        t = []
        if not any(abs(r.val) < 1e-12 for r in poles):
            y0 = f(F(0)); res['y0'] = y0; t.append(r'Eix $OY$ ($%s=0$): $%s(0)=%s$ → $%s$.' % (v, name, nmv(y0), pt(0, y0)))
        zs = [r for r in roots(num) if not any(abs(r.val - p_.val) < 1e-12 for p_ in poles)]
        if zs:
            t.append(r'Eix $OX$ ($y=0$): $%s=0\iff %s$ → %s.' % (num.tex(v), ',\\ '.join('%s=%s' % (v, r.tex) for r in zs),
                     ', '.join('$%s$' % pt(r.tex, 0) for r in zs)))
        else:
            t.append(r'Eix $OX$: $%s=0$ no té solució real, no talla l’eix $OX$.' % num.tex(v))
        S.append(L_('tall', 'Punts de tall.') + ' ' + ' '.join(t))
        res['zeros'] = zs
    # asímptotes
    if asim and ('asi' in lab or only is None):
        t = []
        if f.poly:
            t.append('És un polinomi: no té asímptotes.')
        else:
            for r in poles:
                if abs(num(r.val)) < 1e-12: continue
                e = 1e-7
                sl, sr = f(r.val - e), f(r.val + e)
                inf = lambda s: r'+\infty' if s > 0 else r'-\infty'
                rb = r.tex if '\\' not in r.tex else r'\left(%s\right)' % r.tex
                t.append(r'$%s=%s$: $\displaystyle\lim_{%s\to %s^-}%s=%s$ i $\displaystyle\lim_{%s\to %s^+}%s=%s$.' %
                         (v, r.tex, v, rb, fx, inf(sl), v, rb, fx, inf(sr)))
            av = [r for r in poles if abs(num(r.val)) > 1e-12]
            if av: t.insert(0, 'Asímptotes verticals: ' + ', '.join('$%s=%s$' % (v, r.tex) for r in av) + ' (anul·len el denominador però no el numerador):')
            res['av'] = av
            dn, dd = num.deg, den.deg
            if dn < dd:
                t.append(r'Asímptota horitzontal: $\displaystyle\lim_{%s\to\pm\infty}%s=0$ (grau del numerador menor que el del denominador) → $y=0$.' % (v, fx)); res['ah'] = F(0)
            elif dn == dd:
                k = num.lead / den.lead
                t.append(r'Asímptota horitzontal: $\displaystyle\lim_{%s\to\pm\infty}%s=\frac{%s}{%s}=%s$ (graus iguals: quocient dels coeficients principals) → $y=%s$.' % (v, fx, nm(num.lead), nm(den.lead), nm(k), nm(k))); res['ah'] = k
            else:
                lp = (num.lead / den.lead > 0)
                t.append(r'No té asímptota horitzontal: $\displaystyle\lim_{%s\to\pm\infty}%s=\pm\infty$ (grau del numerador major).' % (v, fx))
                if dn == dd + 1 and obliq:
                    q, _ = num.divmod(den)
                    t.append(r'Té una asímptota obliqua $y=mx+n$ (el grau del numerador supera en 1 el del denominador): dividint, $y=%s$.' % q.tex(v)); res['ao'] = q
                res['ah'] = None
        S.append(L_('asi', 'Asímptotes.') + ' ' + ' '.join(t))
    # monotonia i extrems
    df = f.d(); res['df'] = df
    if 'mon' in lab or 'ext' in lab or only is None:
        if f.poly:
            S.append(L_('mon', 'Derivada.') + " $%s'(%s)=%s$." % (name, v, df.n.tex(v)))
        elif dline:
            S.append(L_('mon', 'Derivada') + ':' + dline)
        else:
            qt = r"\frac{(%s)(%s)-(%s)(%s)}{(%s)^2}" % (num.d().tex(v), den.tex(v), num.tex(v), den.d().tex(v), den.tex(v))
            N = num.d() * den - num * den.d()
            line = r"$$%s'(%s)=%s=\frac{%s}{(%s)^2}" % (name, v, qt, N.tex(v), den.tex(v))
            if df.q.deg < 2 * den.deg:
                line += r"=\frac{%s}{%s}" % (df.n.tex(v), ftex(df.q, v))
            S.append(L_('mon', 'Derivada') + ' (regla del quocient):' + line + '$$')
        crit = [r for r in roots(df.n) if not any(abs(r.val - p_.val) < 1e-12 for p_ in poles)]
        if df.n.deg <= 0:
            cz = r"$%s'(%s)$ no s’anul·la mai." % (name, v)
        else:
            cz = r"$%s'(%s)=0\iff %s=0\iff %s$." % (name, v, df.n.tex(v), ',\\ '.join('%s=%s' % (v, r.tex) for r in crit) if crit else r'\text{cap solució real}')
        cuts = sorted(crit + poles, key=lambda r: r.val)
        def fs(x): return sgn(df(x))
        h, ivs = taula_signes(cuts, fs)
        res['ivs'] = ivs
        cre = [ivl(a, b) for a, b, s in ivs if s == '+']; dec = [ivl(a, b) for a, b, s in ivs if s == '-']
        extra = ' i els punts que no són del domini' if poles else ''
        S.append(st('Signe de la derivada.') + ' ' + cz + ' Estudiem el signe de $%s\'$ en els intervals que determinen els punts crítics%s:' % (name, extra) + h +
                 r'Creixent en $%s$; decreixent en $%s$.' % (union(cre), union(dec)))
        res['cre'], res['dec'] = cre, dec
        ex = []
        for i, c in enumerate(cuts):
            if c not in crit: continue
            s1, s2 = ivs[i][2], ivs[i + 1][2]
            y = f.fv(c)
            if isinstance(y, float): where = r'$%s=%s$, amb $%s(%s)\approx %s$' % (v, c.tex, name, c.tex, ap(y))
            else: where = r'$%s$' % pt(c.tex, nmv(y))
            if s1 == '+' and s2 == '-': ex.append(('max', c, y, r'màxim relatiu en ' + where))
            elif s1 == '-' and s2 == '+': ex.append(('min', c, y, r'mínim relatiu en ' + where))
            else: ex.append(('inf', c, y, r'en $%s=%s$ la derivada s’anul·la però no canvia de signe: no hi ha extrem' % (v, c.tex)))
        res['ext'] = ex
        if ex:
            t_ = '; '.join(e[3] for e in ex); S.append(L_('ext', 'Màxims i mínims.') + ' ' + t_[0].upper() + t_[1:] + '.')
        else:
            S.append(L_('ext', 'Màxims i mínims.') + ' No té màxims ni mínims relatius.')
    if graf:
        pts = [(vval(z), 0.0) for z in res.get('zeros', [])]
        if not any(abs(r.val) < 1e-12 for r in poles): pts.append((0.0, float(f(F(0)))))
        pts += [(vval(e[1]), float(e[2])) for e in res.get('ext', [])]
        pts += list(extra_pts)
        g = plot([f], xr=xr, yr=yr, va=[r.val for r in res.get('av', [])], ha=[float(res['ah'])] if res.get('ah') is not None else [],
                 ob=[res['ao']] if res.get('ao') is not None else [], pts=pts, interest=[r.val for r in cuts] if 'ivs' in res else [])
        S.append(L_('gra', 'Gràfica.') + ' Amb la informació anterior:' + g)
    return S, res


def resum(res, name='f', v='x', asim=True):
    """resum final d'un estudi (a partir dels resultats calculats)"""
    o = []
    if 'dom' in res: o.append(r'$\mathrm{Dom}\,%s=%s$' % (name, res['dom']))
    if 'zeros' in res:
        ps = ([pt(0, res['y0'])] if 'y0' in res else []) + [pt(z.tex, 0) for z in res['zeros'] if not (z.ex == 0 and 'y0' in res)]
        if ps: o.append('talls: ' + ', '.join('$%s$' % p_ for p_ in ps))
    if asim and ('av' in res or 'ah' in res):
        a = []
        if res.get('av'): a.append('AV ' + ', '.join('$%s=%s$' % (v, r.tex) for r in res['av']))
        if res.get('ah') is not None: a.append('AH $y=%s$' % nmv(res['ah']))
        elif res.get('ao') is not None: a.append('sense AH (obliqua $y=%s$)' % res['ao'].tex(v))
        else: a.append('sense AH')
        o.append(', '.join(a))
    if 'cre' in res:
        o.append(r'creix en $%s$ i decreix en $%s$' % (union(res['cre']), union(res['dec'])) if res['cre'] and res['dec'] else
                 (r'creix en $%s$' % union(res['cre']) if res['cre'] else r'decreix en $%s$' % union(res['dec'])))
    if 'ext' in res:
        e = [x[3].replace('relatiu en ', '') for x in res['ext'] if x[0] != 'inf']
        o.append('; '.join(e) if e else 'sense extrems relatius')
    return '; '.join(o) + '.'


# ---------- gràfiques ----------
_gid = [0]


def nice_step(span):
    for s in (0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000):
        if span / s <= 12: return s
    return 10 ** math.ceil(math.log10(span / 10))


def plot(fs, xr=None, yr=None, va=(), ha=(), ob=(), pts=(), shade=(), interest=(), W=420, H=None, labels=(), dom=None, xl='x', yl='y'):
    """fs: llista de funcions (crida float->float) o (funció, [a,b]) per a trossos; shade: [(f, g, a, b)]"""
    _gid[0] += 1; cid = 'cp%d' % _gid[0]
    items = [(f, None) if not isinstance(f, tuple) else f for f in fs]
    xs_int = [p[0] for p in pts] + list(va) + list(interest)
    if xr is None:
        if xs_int:
            a, b = min(xs_int), max(xs_int); m = max(2.0, (b - a) * 0.45)
            xr = (math.floor(a - m), math.ceil(b + m))
        else: xr = (-5, 5)
    x0, x1 = xr
    ys = []
    N = 900
    samples = []
    for f, d in items:
        seg = []
        for i in range(N + 1):
            x = x0 + (x1 - x0) * i / N
            if d is not None and not (d[0] - 1e-12 <= x <= d[1] + 1e-12): seg.append(None); continue
            if any(abs(x - p_) < 1e-9 for p_ in va): seg.append(None); continue
            try: y = f(x)
            except (ZeroDivisionError, ValueError, OverflowError): y = None
            if y is not None and (y != y or abs(y) == INF): y = None
            seg.append((x, y) if y is not None else None)
            if y is not None and not any(abs(x - p_) < (x1 - x0) * 0.06 for p_ in va): ys.append(y)
        samples.append((seg, d))
    if yr is None:
        cand = [p[1] for p in pts] + list(ha) + [0.0]
        if ys:
            srt = sorted(ys); lo, hi = srt[int(len(srt) * .02)], srt[int(len(srt) * .98) - 1]
            lo, hi = min(lo, min(cand)), max(hi, max(cand))
        else: lo, hi = min(cand) - 1, max(cand) + 1
        sp = max(hi - lo, 1e-9); lo -= sp * .12; hi += sp * .12
        if va: lo, hi = min(lo, -abs(hi - lo) * .3 if lo < 0 else lo), hi
        yr = (lo, hi)
    y0, y1 = yr
    H = H or int(max(220, min(380, W * 0.72)))
    pad = 26
    def X(x): return pad + (x - x0) / (x1 - x0) * (W - 2 * pad)
    def Y(y): return H - pad - (y - y0) / (y1 - y0) * (H - 2 * pad)
    o = ['<svg class="graf" viewBox="0 0 %d %d" style="width:100%%;max-width:%dpx;display:block;margin:10px auto;font:11px Inter,sans-serif" role="img" aria-label="Gràfica">' % (W, H, W)]
    o.append('<defs><clipPath id="%s"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath></defs>' % (cid, pad, pad - 6, W - 2 * pad, H - 2 * pad + 12))
    # quadrícula i eixos
    sx, sy = nice_step(x1 - x0), nice_step(y1 - y0)
    g = []
    k = math.ceil(x0 / sx)
    while k * sx <= x1 + 1e-9:
        xv = k * sx
        if abs(xv) > 1e-9:
            g.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-opacity=".08"/>' % (X(xv), pad - 6, X(xv), H - pad + 6))
            if y0 <= 0 <= y1:
                g.append('<text x="%.1f" y="%.1f" text-anchor="middle" fill="currentColor" opacity=".65">%s</text>' % (X(xv), min(Y(0) + 13, H - 4), fmt(xv)))
        k += 1
    k = math.ceil(y0 / sy)
    while k * sy <= y1 + 1e-9:
        yv = k * sy
        if abs(yv) > 1e-9:
            g.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-opacity=".08"/>' % (pad - 6, Y(yv), W - pad + 6, Y(yv)))
            if x0 <= 0 <= x1:
                g.append('<text x="%.1f" y="%.1f" text-anchor="end" fill="currentColor" opacity=".65">%s</text>' % (max(X(0) - 4, 22), Y(yv) + 4, fmt(yv)))
        k += 1
    o += g
    if y0 <= 0 <= y1: o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-opacity=".6"/>' % (pad - 8, Y(0), W - pad + 8, Y(0)))
    if x0 <= 0 <= x1: o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-opacity=".6"/>' % (X(0), pad - 10, X(0), H - pad + 8))
    if y0 <= 0 <= y1: o.append('<text x="%d" y="%.1f" fill="currentColor" opacity=".7" font-style="italic">%s</text>' % (W - pad + 2, Y(0) - 5, xl))
    if x0 <= 0 <= x1: o.append('<text x="%.1f" y="%d" fill="currentColor" opacity=".7" font-style="italic">%s</text>' % (X(0) + 5, pad - 2, yl))
    # ombrejat
    for f, gg, a, b in shade:
        n = 160; top = []; bot = []
        for i in range(n + 1):
            x = a + (b - a) * i / n
            top.append('%.1f,%.1f' % (X(x), Y(f(x)))); bot.append('%.1f,%.1f' % (X(x), Y(gg(x) if gg else 0)))
        o.append('<polygon clip-path="url(#%s)" points="%s" fill="var(--c)" fill-opacity=".28" stroke="none"/>' % (cid, ' '.join(top + bot[::-1])))
    # asímptotes
    for a in va:
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="currentColor" stroke-opacity=".55" stroke-dasharray="5 4"/>' % (X(a), pad - 6, X(a), H - pad + 6))
    for h in ha:
        if y0 <= h <= y1:
            o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-opacity=".55" stroke-dasharray="5 4"/>' % (pad - 6, Y(h), W - pad + 6, Y(h)))
    for q in ob:
        o.append('<line clip-path="url(#%s)" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-opacity=".55" stroke-dasharray="5 4"/>' % (cid, X(x0), Y(q(float(x0))), X(x1), Y(q(float(x1)))))
    # corbes
    lim = (y1 - y0) * 4
    for seg, d in samples:
        path = []; pen = False
        for p_ in seg:
            if p_ is None or p_[1] < y0 - lim or p_[1] > y1 + lim: pen = False; continue
            path.append(('L' if pen else 'M') + '%.1f %.1f' % (X(p_[0]), Y(p_[1]))); pen = True
        o.append('<path clip-path="url(#%s)" d="%s" fill="none" stroke="var(--c)" stroke-width="2.4" stroke-linejoin="round"/>' % (cid, ' '.join(path)))
    for p_ in pts:
        x, y = p_[0], p_[1]
        if x0 <= x <= x1 and y0 <= y <= y1:
            hollow = len(p_) > 2 and p_[2] == 'o'
            o.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s" stroke="var(--c)" stroke-width="1.6"/>' % (X(x), Y(y), 'var(--surface)' if hollow else 'var(--c)'))
    for x, y, t in labels:
        o.append('<text x="%.1f" y="%.1f" fill="currentColor" style="font-size:11px">%s</text>' % (X(x), Y(y), t))
    o.append('</svg>')
    return ''.join(o)


def fmt(v):
    if abs(v - round(v)) < 1e-9: return str(int(round(v)))
    return ('%g' % v).replace('.', ',')


# ---------- integrals i àrees ----------
def barrow(p, a, b, v='x', name=None, dx=None):
    """text de la regla de Barrow per a un polinomi p entre a i b; torna (tex, valor)"""
    Fp = p.prim(); val = Fp(b) - Fp(a)
    dx = dx or 'd' + v
    lhs = r'\int_{%s}^{%s}%s\,%s' % (nm(a), nm(b), ('(%s)' % p.tex(v)) if len(p.c) > 1 and sum(1 for t in p.c if t) > 1 else p.tex(v), dx)
    dc = any(t.denominator != 1 for t in p.c)
    t = r'%s=\Big[%s\Big]_{%s}^{%s}=\left(%s\right)-\left(%s\right)=%s' % (lhs, Fp.tex(v, dec=dc), nm(a), nm(b), nm(Fp(b)), nm(Fp(a)), nm(val))
    return t, val


def area_steps(p, a, b, v='x', q=None, nf='f', ng='g'):
    """àrea entre p (i q, o l'eix OX) en [a,b]; torna (llista de passos, valor)"""
    h = p - q if q is not None else p
    rz = sorted({r.ex for r in roots(h) if r.ex is not None and a < r.ex < b})
    irr = [r for r in roots(h) if r.ex is None and a < r.val < b]
    assert not irr, 'arrels irracionals dins de l’interval'
    cuts = [F(a)] + rz + [F(b)]
    S = []
    hname = ('%s(%s)-%s(%s)' % (nf, v, ng, v)) if q is not None else '%s(%s)' % (nf, v)
    if rz:
        S.append(r'Punts de tall dins de $[%s,\,%s]$: $%s=0\iff %s$.' % (nm(a), nm(b), hname, ',\\ '.join('%s=%s' % (v, nm(r)) for r in rz)))
    else:
        S.append(r'$%s$ no s’anul·la dins de $(%s,\,%s)$: no canvia de signe.' % (hname, nm(a), nm(b)))
    tot = F(0); terms = []; Fp = h.prim()
    for u, w in zip(cuts, cuts[1:]):
        val = Fp(w) - Fp(u); tot += abs(val); terms.append(abs(val))
        S.append(r'$$\int_{%s}^{%s}%s\,d%s=\Big[%s\Big]_{%s}^{%s}=%s$$' % (nm(u), nm(w), ptex(h, v), v, Fp.tex(v, dec=any(t.denominator != 1 for t in h.c)), nm(u), nm(w), nm(val)))
    if len(terms) > 1:
        S.append(r'L’àrea és la suma dels valors absoluts: $A=%s=%s$ u².' % ('+'.join(nm(t) for t in terms), nv(tot)))
    else:
        S.append(r'$A=%s$ u².' % nv(tot))
    return S, tot


# ---------- funcions a trossos ----------
def ptex(p, v='x'):
    """expressió entre parèntesis si cal (per a límits i integrals)"""
    t = p.tex(v) if isinstance(p, (P, R)) else p
    if isinstance(p, P) and sum(1 for c in p.c if c) == 1 and p.lead > 0: return t
    if isinstance(p, R) and not p.poly: return t
    return '(%s)' % t


def cont(c, fl, fr_, fc='r', name='f', v='x'):
    """continuïtat en x=c entre els trossos fl (esquerra) i fr_ (dreta). fc: 'l' si f(c) és del tros esquerre,
    'r' si és del dret, un valor, o None si f(c) no està definida. Torna (text, contínua?)"""
    c = F(c); a = fl(c); b = fr_(c)
    val = a if fc == 'l' else (b if fc == 'r' else fc)
    t = (r'$\displaystyle\lim_{%s\to %s^-}%s(%s)=\lim_{%s\to %s^-}%s=%s$; $\displaystyle\lim_{%s\to %s^+}%s(%s)=\lim_{%s\to %s^+}%s=%s$'
         % (v, nm(c), name, v, v, nm(c), ptex(fl, v), nm(a), v, nm(c), name, v, v, nm(c), ptex(fr_, v), nm(b)))
    if val is not None: t += r'; $%s(%s)=%s$' % (name, nm(c), nm(val))
    if a == b and val == a:
        return t + r'. Coincideixen: $%s$ és contínua en $%s=%s$.' % (name, v, nm(c)), True
    if a != b:
        return t + r'. Els límits laterals són diferents: en $%s=%s$ hi ha una discontinuïtat de salt (inevitable).' % (v, nm(c)), False
    return t + r'. El límit existeix però no coincideix amb el valor de la funció: discontinuïtat evitable en $%s=%s$.' % (v, nm(c)), False


def taula_vals(rows, name='f', v='x'):
    """rows: [(x, valor)] -> taula HTML de valors"""
    def t(x): return x if isinstance(x, str) else nm(x)
    return ('<div class="tbl"><table><tr><th>$%s$</th>' % v + ''.join('<td>$%s$</td>' % t(x) for x, _ in rows) +
            '</tr><tr><th>$%s(%s)$</th>' % (name, v) + ''.join('<td>$%s$</td>' % t(y) for _, y in rows) + '</tr></table></div>')


def extrems_abs(rows, name='f', v='x', unit=''):
    """text del màxim i del mínim absoluts a partir dels candidats [(x, valor)]"""
    vals = [y for _, y in rows]
    def t(x): return x if isinstance(x, str) else nm(x)
    M, m = max(vals), min(vals)
    xm = [t(x) for x, y in rows if y == M]; xn = [t(x) for x, y in rows if y == m]
    def j(xs): return ' i '.join('$%s=%s$' % (v, x) for x in xs)
    return (r'Màxim absolut: $%s=%s$%s, en %s. Mínim absolut: $%s=%s$%s, en %s.' % (name, nm(M), unit, j(xm), name, nm(m), unit, j(xn))), M, m


def taula_m(rows, row1=r"f'(x)", row2='f(x)'):
    """taula de monotonia amb etiquetes d'interval lliures: rows = [(interval TeX, signe)]"""
    return ('<div class="tbl"><table><tr><th>$x$</th>' + ''.join('<td>$%s$</td>' % a for a, _ in rows) + '</tr>' +
            '<tr><th>$%s$</th>' % row1 + ''.join('<td>$%s$</td>' % s for _, s in rows) + '</tr>' +
            '<tr><th>$%s$</th>' % row2 + ''.join('<td>%s</td>' % ('↗' if s == '+' else ('↘' if s == '-' else '→')) for _, s in rows) + '</tr></table></div>')


def eq2(a, b, c, v='x'):
    """resol ax^2+bx+c=0 amb la fórmula; torna (text, arrels Fraction o Rt)"""
    a, b, c = F(a), F(b), F(c); D = b * b - 4 * a * c
    rs = qroots(a, b, c)
    t = r'$%s=0\Rightarrow %s=\dfrac{%s\pm\sqrt{%s}}{%s}' % (P(a, b, c, v=v).tex(v), v, nm(-b), nm(D), nm(2 * a))
    if D < 0: return t + r'$: no té solucions reals', []
    return t + '=' + (r'\begin{cases}%s\\%s\end{cases}' % (rs[0].tex, rs[-1].tex) if len(rs) == 2 else rs[0].tex) + '$', rs
