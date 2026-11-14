# Versió en castellà de genera.py: escriu els -es.tex. Original: genera t3-fitxa-exercicis.tex i t3-fitxa-solucions.tex (1r Batxillerat MI, Unitat 3: Sistemes d'equacions i inequacions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Els exercicis 1-28 són de la fitxa del departament; la secció 6 n'afegeix 4 de nous.
# Les solucions dels sistemes lineals i de les inequacions es calculen ací amb sympy; les altres s'escriuen a mà i CHK les comprova
# (numèricament o amb sympy). Les solucions d'inequacions porten la recta dibuixada i les de dues incògnites, la regió (TikZ, aritmètica exacta).
# Ús: python3 genera.py && pdflatex t3-fitxa-exercicis.tex (dues vegades) && pdflatex t3-fitxa-solucions.tex (dues vegades)
import os, re, math
from fractions import Fraction as F
import sympy as sp
from sympy import Rational as Q, sqrt, oo
HERE = os.path.dirname(os.path.abspath(__file__))
x, y, z, w, a, b, k, m = sp.symbols('x y z w a b k m')
xr = sp.Symbol('x', real=True)

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def L(e):
    s = sp.latex(e, order='lex')
    return s.replace(r'\left(', '(').replace(r'\right)', ')').replace(r'\log{(', r'\log(').replace(r'\ln{(', r'\ln(')
def dec(v, n=3):
    s = ('%.' + str(n) + 'f') % float(v)
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    return s.replace('.', ',')
def sist(*rows): return r'\left\{\begin{array}{l}' + r'\\'.join(rows) + r'\end{array}\right.'

CHK = []
def ck(cond, msg=''):
    CHK.append((bool(cond), msg)); return cond
def eqn(expr, vals, tol=1e-9):
    """comprova numèricament que expr(x) = 0 per a cada valor"""
    for v in vals:
        val = complex(sp.N(expr.subs(x, v), 30))
        ck(abs(val) < tol, 'eq %s at %s -> %s' % (expr, v, val))

# ---------- conjunts de la recta ----------
def ivs(Sset):
    if Sset == sp.S.EmptySet: return []
    parts = Sset.args if isinstance(Sset, sp.Union) else [Sset]
    out = []
    for I in parts:
        if isinstance(I, sp.Interval): out.append((I.start, not I.left_open, I.end, not I.right_open))
        elif isinstance(I, sp.FiniteSet): out += [(v, True, v, True) for v in I]
        else: raise ValueError(I)
    return sorted(out, key=lambda t: -1e18 if t[0] == -oo else float(t[0]))
def ivt(I):
    a_, ac, b_, bc = I
    if a_ == b_: return r'\{%s\}' % L(a_)
    ta = r'-\infty' if a_ == -oo else L(a_)
    tb = r'+\infty' if b_ == oo else L(b_)
    return ('[' if ac else '(') + ta + ', ' + tb + (']' if bc else ')')
def st(Sset):
    I = ivs(Sset)
    if not I: return r'\varnothing'
    if len(I) == 1 and I[0][0] == -oo and I[0][2] == oo: return r'\mathbb R'
    return r'\cup'.join(ivt(i) for i in I)
def recta(Sset):
    S = ivs(Sset)
    pts = [float(v) for I in S for v in (I[0], I[2]) if v not in (oo, -oo)] or [0]
    lo, hi = math.floor(min(pts)) - 1, math.ceil(max(pts)) + 1
    if hi - lo < 6: c = (hi + lo) / 2; lo, hi = math.floor(c - 3), math.ceil(c + 3)
    step = 2 if hi - lo > 14 else 1
    sc = min(0.42, 7.2 / (hi - lo + 1.4))
    o = [r'\begin{tikzpicture}[x=%.3fcm,baseline=-3pt]' % sc, r'\draw[-latex,muted] (%g,0)--(%g,0);' % (lo - 0.6, hi + 0.7)]
    v = math.ceil(lo / step) * step
    while v <= hi:
        o.append(r'\draw[muted] (%d,0.1)--(%d,-0.1) node[below=-1pt,font=\scriptsize,text=muted]{$%d$};' % (v, v, v)); v += step
    for a_, ac, b_, bc in S:
        xa = lo - 0.45 if a_ == -oo else float(a_); xb = hi + 0.45 if b_ == oo else float(b_)
        if a_ != b_: o.append(r'\draw[accent,line width=2.6pt] (%g,0)--(%g,0);' % (xa, xb))
        if a_ == -oo: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xa - 0.3, xa + 0.1, xa + 0.1))
        if b_ == oo: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xb + 0.3, xb - 0.1, xb - 0.1))
        for xv, c, lab in ((a_, ac, True), (b_, bc, a_ != b_)):
            if xv in (oo, -oo) or not lab: continue
            o.append((r'\fill[accent] (%g,0) circle (2.3pt);' if c else r'\filldraw[fill=white,draw=accent,line width=1.1pt] (%g,0) circle (2.3pt);') % float(xv))
            if not xv.is_integer: o.append(r'\node[above=1pt,font=\scriptsize,text=accent] at (%g,0) {$%s$};' % (float(xv), L(xv)))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def RI(Sset): return R('x\\in ' + st(Sset)) + r'\\[2pt]' + recta(Sset)
def ineq(e): return sp.solve_univariate_inequality(e, xr, relational=False)

# ---------- semiplans i regions (com a la unitat 3 de 2n Batx CCSS) ----------
BIG = F(10 ** 6)
def fr(v): return v if isinstance(v, F) else F(str(v))
def clip(P, A, B, C, s):
    out, n = [], len(P)
    if n == 0: return out
    val = lambda p: s * (A * p[0] + B * p[1] - C)
    if n == 1: return P[:] if val(P[0]) <= 0 else []
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]; vp, vq = val(p), val(q)
        if vp <= 0: out.append(p)
        if (vp < 0 < vq) or (vq < 0 < vp):
            t = vp / (vp - vq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    r = []
    for p in out:
        if not r or r[-1] != p: r.append(p)
    while len(r) > 1 and r[0] == r[-1]: r.pop()
    return r
def C(A, B, op, c): return (fr(A), fr(B), op, fr(c))
def region(cons, box):
    x0, x1, y0, y1 = [fr(v) for v in box]
    P = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for A, B, op, c in cons:
        if op in ('<=', '<', '='): P = clip(P, A, B, c, 1)
        if op in ('>=', '>', '='): P = clip(P, A, B, c, -1)
    return P
def verts(cons):
    P = region(cons, (-BIG, BIG, -BIG, BIG))
    V = [p for p in P if abs(p[0]) < BIG and abs(p[1]) < BIG]
    return V, len(V) == len(P)
def tn(v):
    v = fr(v)
    if v.denominator == 1: return str(v.numerator)
    return ('-' if v < 0 else '') + r'\frac{%d}{%d}' % (abs(v.numerator), v.denominator)
def pt(p): return '(%s,\\,%s)' % (tn(p[0]), tn(p[1]))
COL = ['accent', 'blue!70!black', 'violet', 'orange!85!black', 'teal']
def nice(r):
    e = 10 ** math.floor(math.log10(r / 5)); mm = r / 5 / e
    return e * (1 if mm < 1.5 else 2 if mm < 3.5 else 5 if mm < 7.5 else 10)
def fig(cons, view, wd=4.6, hmax=4.4, labels=True, pts=()):
    x0, x1, y0, y1 = view
    sx = wd / (x1 - x0); sy = min(sx, hmax / (y1 - y0))
    stx = nice(x1 - x0); sty = nice(y1 - y0)
    s = r'\begin{tikzpicture}[x=%.4fcm,y=%.4fcm,baseline=(current bounding box.center)]' % (sx, sy)
    s += r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1)
    s += r'\foreach \i in {%s,%s,...,%s} \draw[muted!25,very thin] (\i,%s)--(\i,%s);' % (math.ceil(x0 / stx) * stx, math.ceil(x0 / stx) * stx + stx, x1, y0, y1)
    s += r'\foreach \i in {%s,%s,...,%s} \draw[muted!25,very thin] (%s,\i)--(%s,\i);' % (math.ceil(y0 / sty) * sty, math.ceil(y0 / sty) * sty + sty, y1, x0, x1)
    Rg = region(cons, view)
    if len(Rg) >= 3: s += r'\fill[teal!22] ' + '--'.join('(%.4f,%.4f)' % (float(p[0]), float(p[1])) for p in Rg) + '--cycle;'
    s += r'\end{scope}'
    if y0 <= 0 <= y1: s += r'\draw[-latex,thick] (%s,0)--(%s,0) node[below left=-1pt,font=\scriptsize]{$x$};' % (x0, x1 + 0.25 * stx)
    if x0 <= 0 <= x1: s += r'\draw[-latex,thick] (0,%s)--(0,%s) node[below left=-1pt,font=\scriptsize]{$y$};' % (y0, y1 + 0.25 * sty)
    t = math.ceil(x0 / stx) * stx
    while t <= x1 + 1e-9:
        if abs(t) > 1e-9 and y0 <= 0 <= y1: s += r'\node[below,font=\tiny,text=muted] at (%s,0) {$%s$};' % (t, ('%g' % t))
        t += stx
    t = math.ceil(y0 / sty) * sty
    while t <= y1 + 1e-9:
        if abs(t) > 1e-9 and x0 <= 0 <= x1: s += r'\node[left,font=\tiny,text=muted] at (0,%s) {$%s$};' % (t, ('%g' % t))
        t += sty
    s += r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1)
    for j, (A, B, op, c) in enumerate(cons):
        a_, b_, c_ = float(A), float(B), float(c)
        if abs(b_) > abs(a_): P = [(x0 - 1, (c_ - a_ * (x0 - 1)) / b_), (x1 + 1, (c_ - a_ * (x1 + 1)) / b_)]
        else: P = [((c_ - b_ * (y0 - 1)) / a_, y0 - 1), ((c_ - b_ * (y1 + 1)) / a_, y1 + 1)]
        s += r'\draw[%s,line width=1.1pt%s] (%.4f,%.4f)--(%.4f,%.4f);' % (COL[j % len(COL)], ',dashed' if op in ('<', '>') else '', P[0][0], P[0][1], P[1][0], P[1][1])
    s += r'\end{scope}'
    if labels:
        V, _ = verts(cons)
        if V:
            cx = sum(float(v[0]) for v in V) / len(V); cy = sum(float(v[1]) for v in V) / len(V)
            for v in V:
                vx, vy = float(v[0]), float(v[1])
                if not (x0 <= vx <= x1 and y0 <= vy <= y1): continue
                s += r'\filldraw[fill=white,draw=navy] (%.4f,%.4f) circle (1.5pt);' % (vx, vy)
                dx, dy = (vx - cx) * sx, (vy - cy) * sy
                ang = math.degrees(math.atan2(dy, dx)) if abs(dx) + abs(dy) > 1e-6 else 45
                s += r'\node[font=\tiny,inner sep=1.5pt,fill=white,fill opacity=.75,text opacity=1] at ($(%.4f,%.4f)+(%.1f:0.36cm)$) {$%s$};' % (vx, vy, ang, pt(v))
    for p, okp in pts:
        s += r'\fill[%s] (%s,%s) circle (2.2pt);' % ('teal' if okp else 'red!70!black', p[0], p[1])
    s += r'\end{tikzpicture}'
    return s
def regck(cons, expect, bounded=None):
    V, bd = verts(cons)
    ck(sorted(V) == sorted((fr(p[0]), fr(p[1])) for p in expect), 'vertexs %s' % V)
    if bounded is not None: ck(bd == bounded, 'fitada %s' % cons)
    return cons

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# ---------- comprovacions numèriques ----------
def okf(f, vs, bad=()):
    for v in vs: ck(abs(f(float(v))) < 1e-9, 'rad ok %s' % v)
    for v in bad:
        try: r = f(float(v)); ck(abs(r) > 1e-6, 'rad bad %s' % v)
        except ValueError: pass
sq = math.sqrt

# =====================================================================
# 1. Sistemes d'equacions lineals. Mètode de Gauss
ck(sp.solve([y - (x + 1) / 2 - 3, y - 2 * x - 10], [x, y]) == {x: Q(-13, 3), y: Q(4, 3)})
ck(sp.solve([2 * (2 * x + y) - 3 * (3 * x - 2 * y) + 34, x / 2 - y / 3 - 2], [x, y]) == {x: 2, y: -3})
lam = sp.Symbol(r'\lambda')
def gsol(eqs, vars_=(x, y, z)):
    S_ = sp.linsolve(eqs, list(vars_))
    if S_ == sp.S.EmptySet: return r'\rest{SI}: incompatible (aparece una ecuación $0=k\neq0$)'
    sol = list(S_)[0]
    free = [v for v in vars_ if any(s.has(v) for s in sol)]
    if not free: return r'\rest{SCD}: \ ' + R(r'(%s)=(%s)' % (','.join(L(v) for v in vars_), r',\ '.join(L(s) for s in sol)))
    sol = [s.subs(free[0], lam) for s in sol]
    return r'\rest{SCI}: \ ' + R(r'(%s)=(%s),\ \lambda\in\mathbb R' % (','.join(L(v) for v in vars_), r',\ '.join(L(sp.expand(s)) for s in sol)))
S57 = [[x + 2 * y - 3 * z - 7, 2 * x + y - z - 6, 3 * x - y - z - 6], [x + y - z - 5, 3 * x - 2 * y - 2 * z - 5, 2 * x - 3 * y - z - 3], [2 * x + y + z - 5, 2 * x - y + 3 * z - 3, 3 * x + 2 * y + z - 8],
       [x + y - 2 * z, 2 * x - 3 * y + 3 * z - 4, 5 * x - 5 * y + 4 * z - 8], [5 * x + 2 * y - 2 * z, 3 * x - y + 3 * z, 8 * x + y + z + 1], [x + 3 * y - 2 * z, x - y + 3 * z, 2 * x + 2 * y + z],
       [2 * y - z + 1, 5 * x - y - 3 * z - 2, x - y + 2 * z - 3], [x + 2 * y - 2 * z - 2, 3 * x - 3 * y + z + 14, 5 * x - y - 2 * z + 15], [x + y + z - 1, 2 * x - 3 * z - 5, 2 * y + 5 * z - 2]]
S57j = [x + 3 * y - 2 * z + 2 * w - 12, 2 * x - 2 * y - z + w - 5, 3 * x + y - 2 * z - 4 * w - 16, 3 * x - 3 * z - 3 * w - 15]
ck(sp.linsolve(S57j, [x, y, z, w]) == sp.FiniteSet((4, 2, -1, 0)))
T57 = [sist(r"x+2y-3z=7", r"2x+y-z=6", r"3x-y-z=6"), sist(r"x+y-z=5", r"3x-2y-2z=5", r"2x-3y-z=3"), sist(r"2x+y+z=5", r"2x-y+3z=3", r"3x+2y+z=8"), sist(r"x+y-2z=0", r"2x-3y+3z=4", r"5x-5y+4z=8"),
       sist(r"5x+2y-2z=0", r"3x-y+3z=0", r"8x+y+z=-1"), sist(r"x+3y-2z=0", r"x-y+3z=0", r"2x+2y+z=0"), sist(r"2y-z=-1", r"5x-y-3z=2", r"x-y+2z=3"), sist(r"x+2y-2z=2", r"3x-3y+z=-14", r"5x-y-2z=-15"),
       sist(r"x+y+z=1", r"2x-3z=5", r"2y+5z=2")]
S.append(("Sistemas de ecuaciones lineales. Método de Gauss", [
 (1, r"Resuelve los siguientes sistemas de ecuaciones lineales:" + tasks(2, [r"$" + sist(r"y=\dfrac{x+1}{2}+3", r"y=2x+10") + "$", r"$" + sist(r"2(2x+y)-3(3x-2y)=-34", r"\dfrac x2-\dfrac y3=2") + "$"]),
     tasks(2, [r"$2x+10=\frac{x+1}{2}+3$: \ " + R(r"x=-\frac{13}{3},\ y=\frac43"), r"$-5x+8y=-34,\ 3x-2y=12$: \ " + R(r"x=2,\ y=-3")])),
 (2, r"Resuelve los siguientes sistemas de ecuaciones lineales por el método de Gauss y clasifícalos:" + tasks(2, ["$" + t + "$" for t in T57] + ["$" + sist(r"x+3y-2z+2w=12", r"2x-2y-z+w=5", r"3x+y-2z-4w=16", r"3x-3z-3w=15") + "$"])
     + recorda(r"Haz ceros debajo de la diagonal. La última fila $(0\ \ 0\ \ m\,|\,n)$ decide: $m\neq0$ SCD; $m=n=0$ SCI; $m=0,\ n\neq0$ SI."),
     tasks(1, [gsol(s_) for s_ in S57] + [r'\rest{SCD}: \ ' + R(r"(x,y,z,w)=(4,\ 2,\ -1,\ 0)")])),
]))

# =====================================================================
# 2. Sistemes d'equacions no lineals
def nlsol(eqs, expect):
    r_ = sp.solve(eqs, [x, y], dict=True)
    got = sorted([(d[x], d[y]) for d in r_ if d[x].is_real and d[y].is_real], key=lambda p: (float(p[0]), float(p[1])))
    ck(got == sorted(expect, key=lambda p: (float(p[0]), float(p[1]))), 'nl %s %s' % (eqs, got))
    return R(r',\ '.join('(%s,\\,%s)' % (L(p[0]), L(p[1])) for p in got)) if got else R(r'\text{no tiene solución real}')
NL = [([2 * x + 3 * y + 4, x ** 2 - 2 * x * y - 5], [(1, -2), (Q(-15, 7), Q(2, 21))], r"$x=\frac{-4-3y}{2}$ y sustituimos"),
      ([1 / x + 2 / y - 4, 10 * x * y - 9], [(Q(3, 10), 3), (Q(3, 2), Q(3, 5))], r"$\frac{y+2x}{xy}=4\Rightarrow y+2x=\frac{18}{5}$"),
      ([x ** 2 + 2 * y ** 2 - 6, 3 * x ** 2 - y ** 2 - 11], [(2, 1), (2, -1), (-2, 1), (-2, -1)], r"Reducción: $7x^2=28$"),
      ([2 * x + y - 8, 2 * x + 3 * y ** 2 - 22], [(5, -2), (Q(17, 6), Q(7, 3))], r"Restando: $3y^2-y-14=0$"),
      ([2 * x + 5 * y + 8, x * y - 3 * y - 4], [(1, -2), (-2, Q(-4, 5))], r"$x=\frac{-8-5y}{2}$ y sustituimos"),
      ([x + y, x * y - 1], [], r"$-x^2=1$"),
      ([2 * x - y - 3, x ** 2 - y ** 2 - 3], [(2, 1)], r"$y=2x-3\Rightarrow x^2-4x+4=0$"),
      ([x + y - 11, 1 / x + 6 / (y + 1) - 1], [(3, 8), (4, 7)], r"$y+1=12-x\Rightarrow x^2-7x+12=0$"),
      ([x * y + 3, x ** 2 + 2 * y ** 2 - 19], [(1, -3), (-1, 3), (3 * sqrt(2), -sqrt(2) / 2), (-3 * sqrt(2), sqrt(2) / 2)], r"$y=-\frac3x\Rightarrow x^4-19x^2+18=0$"),
      ([2 * x ** 2 + 3 * y ** 2 - 32, -3 * x ** 2 + 4 * y ** 2 + 48], [(4, 0), (-4, 0)], r"Reducción: $17y^2=0$"),
      ([sqrt(x) + sqrt(y) - 15, x - y - 105], [(121, 16)], r"$(\sqrt x-\sqrt y)(\sqrt x+\sqrt y)=105\Rightarrow\sqrt x-\sqrt y=7$"),
      ([x ** 2 - 2 * x * y - 16 + y ** 2, x ** 2 - y ** 2 - 72], [(11, 7), (-11, -7)], r"$(x-y)^2=16\Rightarrow x-y=\pm4$")]
TN = [sist(r"2x+3y=-4", r"x^2-2xy=5"), sist(r"\frac1x+\frac2y=4", r"10xy=9"), sist(r"x^2+2y^2=6", r"3x^2-y^2=11"), sist(r"2x+y=8", r"2x+3y^2=22"), sist(r"2x+5y=-8", r"xy-3y=4"), sist(r"x+y=0", r"xy=1"),
      sist(r"2x-y=3", r"x^2-y^2=3"), sist(r"x+y=11", r"\frac1x+\frac6{y+1}=1"), sist(r"xy=-3", r"x^2+2y^2=19"), sist(r"2x^2+3y^2=32", r"-3x^2+4y^2=-48"), sist(r"\sqrt x+\sqrt y=15", r"x-y=105"), sist(r"x^2-2xy=16-y^2", r"x^2-y^2=72")]
X1, Y1 = sp.symbols('X Y', positive=True)
ck(sp.solve([X1 + Y1 - 9, 4 * X1 + 5 * Y1 - 41], [X1, Y1]) == {X1: 4, Y1: 5} and sp.solve([X1 + Y1 - 5, 2 * X1 - Y1 - 7], [X1, Y1]) == {X1: 4, Y1: 1})
ck(sp.solve([X1 - Y1 - 1016, X1 - 128 * Y1], [X1, Y1]) == {X1: 1024, Y1: 8} and sp.solve([X1 + Y1 - 16, X1 / 3 - 49 * Y1 + 340], [X1, Y1]) == {X1: 9, Y1: 7})
ck(set(sp.solve(3 * x ** 2 - 20 * x + 32, x)) == {4, Q(8, 3)})
okf(lambda t: 1 / 2 ** t + 3 / 2 ** (5 - t) - 5 / 8, [2, math.log2(8 / 3)])
p_, q_ = sp.symbols('p q')
ck(sp.solve([2 * p_ - 3 * q_ - 7, p_ + q_ - 1], [p_, q_]) == {p_: 2, q_: -1} and sp.solve([p_ + 3 * q_ - 5, p_ - q_ - 3], [p_, q_]) == {p_: Q(7, 2), q_: Q(1, 2)})
ck(sp.solve([x - y - 21, x * y - 100], [x, y]) == [(-4, -25), (25, 4)] and sp.solve([x * y - 2187, x - 2 * y - 27], [x, y]) == [(-54, Q(-81, 2)), (81, 27)])
ck(sp.solve([3 * x + 2 * y - 64, x - 10 * y], [x, y]) == {x: 20, y: 2})
S.append(("Sistemas de ecuaciones no lineales", [
 (2, r"Resuelve los siguientes sistemas de ecuaciones no lineales:" + tasks(3, ["$" + t + "$" for t in TN]),
     tasks(1, [e[2] + r": \ " + nlsol(e[0], e[1]) for e in NL])),
 (2, r"Resuelve los siguientes sistemas de ecuaciones exponenciales:" + tasks(2, ["$" + sist(r"2^x+5^y=9", r"2^{x+2}+5^{y+1}=41") + "$", "$" + sist(r"2^x+3^y=5", r"2^{x+1}-3^y=7") + "$", "$" + sist(r"2^x-2^y=1016", r"2^{x-y}=128") + "$", "$" + sist(r"3^x+7^y=16", r"3^{x-1}-7^{y+2}=-340") + "$", "$" + sist(r"\dfrac{1}{2^x}+\dfrac{3}{2^y}=\dfrac{x+y}{8}", r"x+y=5") + "$"])
     + recorda(r"Cambio de variable: $u=2^x$, $v=5^y$\ldots\ y resuelve el sistema lineal en $u$ y $v$."),
     tasks(1, [r"$u+v=9,\ 4u+5v=41\Rightarrow u=4,\ v=5$: \ " + R(r"x=2,\ y=1"), r"$u+v=5,\ 2u-v=7\Rightarrow u=4,\ v=1$: \ " + R(r"x=2,\ y=0"), r"$2^x=128\cdot2^y\Rightarrow127\cdot2^y=1016\Rightarrow2^y=8$: \ " + R(r"x=10,\ y=3"), r"$u+v=16,\ \frac u3-49v=-340\Rightarrow u=9,\ v=7$: \ " + R(r"x=2,\ y=1"), r"$y=5-x$ y $t=2^x$: $\frac1t+\frac{3t}{32}=\frac58\Rightarrow3t^2-20t+32=0\Rightarrow t=4,\ t=\frac83$:\par " + R(r"(2,\,3)") + r" \ y \ " + R(r"\left(\log_2\tfrac83,\ 5-\log_2\tfrac83\right)\approx(1,415;\ 3,585)")])),
 (2, r"Halla las soluciones de los siguientes sistemas de ecuaciones logarítmicas:" + tasks(2, ["$" + sist(r"2\log x-3\log y=7", r"\log x+\log y=1") + "$", "$" + sist(r"x-y=21", r"\log x+\log y=2") + "$", "$" + sist(r"\log x+3\log y=5", r"\log x-\log y=3") + "$", "$" + sist(r"\log_3x=7-\log_3y", r"x-2y=27") + "$", "$" + sist(r"3x+2y=64", r"\log x-\log y=1") + "$", "$" + sist(r"\log x^2-2\log y=6", r"2\log x+\log y^2=2") + "$"])
     + recorda(r"Con $u=\log x$, $v=\log y$ se obtiene un sistema lineal; o bien agrupa los logaritmos. Comprueba que $x\gt0$ e $y\gt0$."),
     tasks(1, [r"$2u-3v=7,\ u+v=1\Rightarrow u=2,\ v=-1$: \ " + R(r"x=100,\ y=\frac1{10}"), r"$xy=100,\ x=21+y\Rightarrow y^2+21y-100=0\Rightarrow y=4$ ($y=-25$ no vale): \ " + R(r"x=25,\ y=4"), r"$u+3v=5,\ u-v=3\Rightarrow u=\frac72,\ v=\frac12$: \ " + R(r"x=10^{7/2}=1000\sqrt{10},\ y=\sqrt{10}"), r"$xy=3^7=2187$ y $x=27+2y\Rightarrow2y^2+27y-2187=0\Rightarrow y=27$: \ " + R(r"x=81,\ y=27"), r"$x=10y\Rightarrow32y=64$: \ " + R(r"x=20,\ y=2"), r"$2u-2v=6,\ 2u+2v=2\Rightarrow u=2,\ v=-1$: \ " + R(r"x=100,\ y=\frac1{10}")])),
]))

# =====================================================================
# 3. Sistemes d'inequacions amb una incògnita
def sysI(*es):
    s_ = sp.S.Reals
    for e in es: s_ = s_.intersect(ineq(e))
    return s_
S65 = [sysI(2 * xr - 3 <= 0, 3 * xr + 1 > 0), sysI(xr + 2 <= 2, 2 * xr - (xr - 1) / 3 <= xr - Q(1, 3), xr ** 2 + 2 * xr - 8 > 0), sysI(2 * xr + 1 < xr + 2, 3 * xr - 1 <= 4 * xr),
       sysI(3 * xr - 4 > xr, xr >= 2 * xr - 1), sysI(xr ** 2 + 2 * xr - 3 >= 0, 2 * (xr - 3) > -6), sysI((xr - 1) / (xr + 2) > 0, xr ** 2 >= 1)]
S.append(("Sistemas de inecuaciones con una incógnita", [
 (2, r"Resuelve los sistemas de inecuaciones siguientes:" + tasks(3, ["$" + sist(r"2x-3\le0", r"3x+1\gt0") + "$", "$" + sist(r"x+2\le2", r"2x-\frac{x-1}{3}\le x-\frac13", r"x^2+2x-8\gt0") + "$", "$" + sist(r"2x+1\lt x+2", r"3x-1\le4x") + "$",
      "$" + sist(r"3x-4\gt x", r"x\ge2x-1") + "$", "$" + sist(r"x^2+2x-3\ge0", r"2(x-3)\gt-6") + "$", "$" + sist(r"\dfrac{x-1}{x+2}\gt0", r"x^2\ge1") + "$"]),
     tasks(1, [r"$x\le\frac32$ y $x\gt-\frac13$: \ " + RI(S65[0]), r"$x\le0$, $x\le-1$ y $x\in(-\infty,\,{-}4)\cup(2,+\infty)$: \ " + RI(S65[1]), r"$x\lt1$ y $x\ge-1$: \ " + RI(S65[2]),
               r"$x\gt2$ y $x\le1$: \ " + R(r"\text{no tiene solución}"), r"$(-\infty,\,{-}3]\cup[1,+\infty)$ y $x\gt0$: \ " + RI(S65[4]), r"$(-\infty,\,{-}2)\cup(1,+\infty)$ y $(-\infty,-1]\cup[1,+\infty)$: \ " + RI(S65[5])])),
]))
ck(S65[3] == sp.S.EmptySet)

# =====================================================================
# 4. Inequacions i sistemes amb dues incògnites
NN = [C(1, 0, '>=', 0), C(0, 1, '>=', 0)]
H66 = [([C(3, 4, '<=', 12)], (-2, 6, -2, 5), r"Recta continua por $(4,0)$ y $(0,3)$; $O$: $0\le12$ \checkmark: semiplano de $O$."),
       ([C(-3, 4, '>=', 4)], (-4, 4, -2, 4), r"Recta continua por $(0,1)$ y $(-\frac43,0)$; $O$: $0\ge4$ falso: semiplano que \rest{no} contiene $O$."),
       ([C(2, 1, '<', 2)], (-2, 4, -3, 4), r"Recta discontinua por $(1,0)$ y $(0,2)$; $O$: $0\lt2$ \checkmark: semiplano de $O$."),
       ([C(1, -1, '>', -2)], (-4, 3, -2, 5), r"$x-y\gt-2$: recta discontinua por $(-2,0)$ y $(0,2)$; $O$: $0\gt-2$ \checkmark: semiplano de $O$.")]
R67 = [(regck([C(0, 1, '>=', 0), C(0, 1, '<', 2), C(1, 1, '<=', 3), C(1, -1, '>=', 2), C(1, 0, '>=', 0)], [(2, 0), (3, 0), (F(5, 2), F(1, 2))], True), (-1, 4, -1, 3), r"Triángulo de vértices $(2,0)$, $(3,0)$ y $\left(\frac52,\frac12\right)$ (la condición $y\lt2$ no influye)."),
       (regck([C(2, 1, '<', 4), C(-1, 1, '>=', 0)], [(F(4, 3), F(4, 3))], False), (-3, 4, -3, 5), r"Región \rest{no acotada} con un solo vértice, $\left(\frac43,\frac43\right)$ (el borde de $y\lt-2x+4$ no se incluye)."),
       (regck([C(0, 1, '<=', 2), C(1, 0, '>', -4), C(1, -1, '<', -3)], [(-4, -1), (-4, 2), (-1, 2)], True), (-5, 1, -2, 4), r"Triángulo de vértices $(-4,\,{-}1)$, $(-4,2)$ y $(-1,2)$; solo el lado $y=2$ es de la región."),
       (regck([C(1, 1, '<=', 6), C(-1, 2, '<=', 0), C(1, 0, '>=', 0)], [(0, 0), (4, 2)], False), (-1, 7, -3, 4), r"Región \rest{no acotada} (hacia abajo) con vértices $(0,0)$ y $(4,2)$."),
       (regck([C(2, 1, '<', 2), C(1, -1, '>', -2), C(1, 0, '>', 0), C(0, 1, '>', 0)], [(0, 0), (1, 0), (0, 2)], True), (-1, 3, -1, 3), r"Triángulo de vértices $(0,0)$, $(1,0)$ y $(0,2)$, sin los bordes ($x\gt y-2$ no influye)."),
       (regck([C(0, 1, '>=', 3), C(0, 1, '<=', 5), C(1, 0, '<=', 6), C(1, 0, '>=', 4)], [(4, 3), (6, 3), (6, 5), (4, 5)], True), (-1, 7, -1, 6), r"Rectángulo de vértices $(4,3)$, $(6,3)$, $(6,5)$ y $(4,5)$.")]
for c_, v_, _ in H66: pass
S.append(("Inecuaciones y sistemas con dos incógnitas", [
 (1, r"Resuelve las siguientes inecuaciones con dos incógnitas:" + tasks(2, [r"$3x+4y\le12$", r"$-3x+4y\ge4$", r"$2x+y\lt2$", r"$x\gt y-2$"])
     + recorda(r"Dibuja la recta (continua si es $\le,\ge$; discontinua si es $\lt,\gt$) y prueba un punto que no esté en ella, como $O(0,0)$."),
     tasks(2, [H66[i][2] + r"\par" + fig(H66[i][0], H66[i][1], wd=3.6, labels=False) for i in range(4)])),
 (2, r"Resuelve los sistemas de inecuaciones con dos incógnitas:" + tasks(3, ["$" + sist(r"0\le y\lt2", r"x+y\le3", r"x-y\ge2", r"x\ge0,\ y\ge0") + "$", "$" + sist(r"y\lt-2x+4", r"y\ge x") + "$", "$" + sist(r"y\le2", r"x\gt-4", r"x-y\lt-3") + "$",
      "$" + sist(r"x+y\le6", r"2y\le x", r"x\ge0") + "$", "$" + sist(r"2x+y\lt2", r"x\gt y-2", r"x\gt0,\ y\gt0") + "$", "$" + sist(r"3\le y\le5", r"x-6\le0", r"x-4\ge0") + "$"]),
     tasks(2, [r[2] + r"\par" + fig(r[0], r[1], wd=3.6) for r in R67])),
]))

# =====================================================================
# 5. Problemes de sistemes i inequacions
def lin(eqs, vars_, expect):
    got = sp.solve(eqs, vars_)
    ck(got == dict(zip(vars_, expect)), 'lin %s -> %s' % (eqs, got)); return expect
A, B, Cc, D = sp.symbols('A B C D')
lin([x + y - 250, 4 * x + 2 * y - 800], [x, y], [150, 100])
ck(sp.factor(x ** 3 - 5 * x + 4) == (x - 1) * (x ** 2 + x - 4))
lin([x + y + z - 21, 50 * x + 100 * y + 200 * z - 1800, x - 5 * z], [x, y, z], [10, 9, 2])
lin([x + y + z - 60, x - 3 * (y + z), 2 * y - 3 * z], [x, y, z], [45, 9, 6])
lin([x + y + z - 50, x + y - 4 * z, 2 * x + 3 * y + 4 * z - 140], [x, y, z], [20, 20, 10])
lin([10 * x + 15 * y + 30 * z - 775, y - z - 5, z - Q(1, 5) * (x + y + z)], [x, y, z], [25, 15, 10])
lin([x + y + z - 8, 10 * x + 20 * y + 50 * z - 290, x - 2 * y], [x, y, z], [2, 1, 5])
lin([x + y + z - 800, 10 * x + 20 * y + 50 * z - 21000, x - y - z], [x, y, z], [400, 100, 300])
lin([x + y + z - 1405, 6 * x + 4 * y + 3 * z - 7920, 4 * y + 3 * z - Q(6, 10) * x], [x, y, z], [1200, 105, 100])
lin([x + y + z - 200, y - x - z, 200 * x + 500 * y + 250 * z - 73500], [x, y, z], [30, 100, 70])
lin([x + y + z - 9, 100 * x + 120 * y + 150 * z - 1160, z - y - 1], [x, y, z], [2, 3, 4])
lin([Q(9, 10) * (x + y + z) - Q(396, 100), y - x / 2, z - y - Q(1, 5) * x], [x, y, z], [2, 1, Q(7, 5)])
lin([x + y + z - 7000, Q(5, 100) * x + Q(3, 100) * y + Q(1, 100) * z - 202, x + y - z - 2600], [x, y, z], [1800, 3000, 2200])
lin([x + y + z - 60, y - 2 * (x + z), z - x / 2 - 2], [x, y, z], [12, 40, 8])
lin([200 * x + 100 * y + 300 * z - 830, Q(5, 4) * (200 * x + 100 * y) + Q(7, 5) * 300 * z - 1087, x - z - Q(1, 2)], [x, y, z], [Q(8, 5), Q(9, 5), Q(11, 10)])
lin([y - x - z, 4 * x + 8 * y + 10 * z - 1116, 8 * y - 10 * z - 156], [x, y, z], [30, 72, 42])
ck(30 * Q(5, 2) + 72 * 4 + 42 * 5 == 573)
lin([x + y + z - Q(15, 2), z - y - 1, x - 5 * (z - x)], [x, y, z], [Q(5, 2), 2, 3])
lin([x + y + z - 42000, Q(5, 100) * x + Q(7, 100) * y + Q(9, 100) * z - 2600, Q(5, 100) * x - Q(7, 100) * y - Q(9, 100) * z + 200], [x, y, z], [24000, 11000, 7000])
S88 = sysI(6 * xr + 2 >= 20, 6 * xr + 2 <= 30); ck(S88 == sp.Interval(3, Q(14, 3)))
R89 = regck([C(2, 1, '<=', 40), C(1, 2, '<=', 50)] + NN, [(0, 0), (20, 0), (10, 20), (0, 25)], True)
ck(2 * 15 + 12 > 40 and 2 * 10 + 20 <= 40 and 10 + 2 * 20 <= 50)
S.append(("Problemas de sistemas e inecuaciones", [
 (1, r"En una granja hay 250 animales entre conejos y gallinas. Si el número total de patas es 800, ¿cuántos animales hay de cada tipo?", r"$x+y=250,\ 4x+2y=800$: \ " + R(r"150\ \text{conejos y }100\ \text{gallinas}")),
 (3, r"Hemos necesitado 10 dm$^2$ de cartón para construir una caja con tapa, de base cuadrada y 2 dm$^3$ de volumen. ¿Cuáles son las dimensiones de la caja si el lado de la base es un número entero de decímetros?",
     r"$x^2h=2,\ 2x^2+4xh=10\Rightarrow2x^2+\frac8x=10\Rightarrow x^3-5x+4=0\Rightarrow(x-1)(x^2+x-4)=0$. La única raíz entera es $x=1$: \ " + R(r"1\ \text{dm}\times1\ \text{dm}\times2\ \text{dm}")),
 (2, r"En una caja registradora hay billetes de 50\,€, 100\,€ y 200\,€: 21 billetes en total y 1\,800\,€. El número de billetes de 50\,€ es el quíntuple de los de 200\,€. ¿Cuántos hay de cada clase?",
     r"$x+y+z=21,\ 50x+100y+200z=1800,\ x=5z$: \ " + R(r"10\ \text{de }50\,€,\ 9\ \text{de }100\,€,\ 2\ \text{de }200\,€")),
 (2, r"Tres nietos quieren hacer un regalo de 60\,€ a su abuela: Luis, el mayor, aporta el triple de lo que aportan los otros dos juntos, y Carmen aporta 3\,€ por cada 2 que aporta Pedro. ¿Cuánto aporta cada uno?",
     r"$L+C+P=60,\ L=3(C+P),\ 2C=3P$: \ " + R(r"\text{Luis }45\,€,\ \text{Carmen }9\,€,\ \text{Pedro }6\,€")),
 (2, r"Calcula cuántas bicicletas, triciclos y coches tiene una juguetería si en total hay 50 vehículos, el número de bicicletas y triciclos cuadruplica el de coches y hay 140 ruedas.",
     r"$b+t+c=50,\ b+t=4c,\ 2b+3t+4c=140$: \ " + R(r"20\ \text{bicicletas},\ 20\ \text{triciclos},\ 10\ \text{coches}")),
 (2, r"Para un espectáculo hay entradas A, B y C, de 10, 15 y 30\,€. La recaudación fue de 775\,€, se vendieron 5 entradas más del tipo B que del C y el 20\,\% de las entradas eran del tipo C. ¿Cuántas se vendieron de cada tipo?",
     r"$10a+15b+30c=775,\ b=c+5,\ c=0,2(a+b+c)$: \ " + R(r"25\ \text{A},\ 15\ \text{B},\ 10\ \text{C}")),
 (2, r"Un cajero solo tiene billetes de 10, 20 y 50\,€. Sacamos 290\,€ y nos da exactamente 8 billetes; el número de billetes de 10\,€ es el doble de los de 20\,€. Plantea y resuelve el sistema.",
     r"$x+y+z=8,\ 10x+20y+50z=290,\ x=2y$: \ " + R(r"2\ \text{de }10\,€,\ 1\ \text{de }20\,€,\ 5\ \text{de }50\,€")),
 (2, r"Un cajero automático contiene 800 billetes de 10, 20 y 50\,€ con un importe de 21\,000\,€. El número de billetes de 10\,€ es igual que el de 20\,€ y 50\,€ juntos. ¿Cuántos billetes hay de cada tipo?",
     r"$x+y+z=800,\ 10x+20y+50z=21000,\ x=y+z$: \ " + R(r"400\ \text{de }10\,€,\ 100\ \text{de }20\,€,\ 300\ \text{de }50\,€")),
 (3, r"En un cine se han vendido 1405 entradas y se han recaudado 7920\,€. La entrada normal cuesta 6\,€, la del día del espectador 4\,€ y la de los jubilados 3\,€. La recaudación de las entradas de precio reducido es el 10\,\% de la de las entradas normales. ¿Cuántas entradas de cada tipo se han vendido?",
     r"$n+e+j=1405,\ 6n+4e+3j=7920,\ 4e+3j=0,1\cdot6n$:\par " + R(r"1200\ \text{normales},\ 105\ \text{del espectador},\ 100\ \text{de jubilados}")),
 (2, r"Un comerciante vende relojes A a 200\,€, B a 500\,€ y C a 250\,€. Un mes vende 200; los del tipo B son tantos como los de A y C juntos, y la recaudación es de 73\,500\,€. ¿Cuántos ha vendido de cada tipo?",
     r"$a+b+c=200,\ b=a+c,\ 200a+500b+250c=73500$: \ " + R(r"30\ \text{A},\ 100\ \text{B},\ 70\ \text{C}")),
 (2, r"Una persona compra memorias externas, lectores de libros electrónicos y tabletas gráficas a 100, 120 y 150\,€ la unidad. Paga 1160\,€ por 9 unidades y compra una tableta más que lectores. ¿Cuántas unidades de cada producto compra?",
     r"$m+l+t=9,\ 100m+120l+150t=1160,\ t=l+1$: \ " + R(r"2\ \text{memorias},\ 3\ \text{lectores},\ 4\ \text{tabletas}")),
 (2, r"Después de un descuento del 10\,\% en cada precio, se ha pagado 3,96\,€ por un rotulador, un cuaderno y una carpeta. El cuaderno vale la mitad que el rotulador y la carpeta, lo que vale el cuaderno más el 20\,\% del rotulador. Calcula el precio original de cada objeto.",
     r"$0,9(r+q+c)=3,96,\ q=\frac r2,\ c=q+0,2r$: \ " + R(r"\text{rotulador }2\,€,\ \text{cuaderno }1\,€,\ \text{carpeta }1,40\,€")),
 (3, r"Una persona invierte 7000\,€ en acciones de las empresas A y B y en un depósito al 1\,\%. Con las acciones obtiene un 5\,\% (A) y un 3\,\% (B), y el beneficio total es de 202\,€. El dinero en acciones supera en 2600\,€ al del depósito. ¿Cuánto destinó a cada inversión?",
     r"$a+b+d=7000,\ 0,05a+0,03b+0,01d=202,\ a+b=d+2600$: \ " + R(r"\text{A }1800\,€,\ \text{B }3000\,€,\ \text{depósito }2200\,€")),
 (2, r"Una agencia de viajes vende 60 billetes a Londres, París y Roma. Los de París son el doble de los otros dos destinos juntos y a Roma se emiten dos más que la mitad de los de Londres. ¿Cuántos billetes se han vendido para cada destino?",
     r"$l+p+r=60,\ p=2(l+r),\ r=\frac l2+2$: \ " + R(r"\text{Londres }12,\ \text{París }40,\ \text{Roma }8")),
 (3, r"Un comerciante compra 200 kg de melocotones, 100 de manzanas y 300 de peras. Los vende subiendo un 25\,\% el precio de los melocotones y las manzanas y un 40\,\% el de las peras, y obtiene 1087\,€, de los cuales 257 son de beneficio. Si el kilo de melocotones le costó 50 céntimos más que el de peras, ¿cuál fue el precio de compra de cada fruta?",
     r"$200b+100p+300q=830,\ 1,25(200b+100p)+1,4\cdot300q=1087,\ b=q+0,5$:\par " + R(r"\text{melocotones }1,60\,€/\text{kg},\ \text{manzanas }1,80\,€/\text{kg},\ \text{peras }1,10\,€/\text{kg}")),
 (3, r"Un restaurante ofrece desayunos a 4\,€, comidas a 8\,€ y cenas a 10\,€. El último sábado se sirvieron tantas comidas como desayunos y cenas juntos, la recaudación total fue de 1116\,€ y la de las comidas superó a la de las cenas en 156\,€." + tasks(1, ["¿Cuántos desayunos, comidas y cenas se sirvieron?", "¿Qué beneficio se obtuvo si las ganancias son de 2,5\,€ por desayuno, 4\,€ por comida y 5\,€ por cena?"]),
     tasks(1, [r"$l=d+s,\ 4d+8l+10s=1116,\ 8l-10s=156$: \ " + R(r"30\ \text{desayunos},\ 72\ \text{comidas},\ 42\ \text{cenas}"), r"$30\cdot2,5+72\cdot4+42\cdot5=$ " + R(r"573\,€")])),
 (2, r"Un estudiante sacó 7,5 puntos en un examen de tres preguntas. En la tercera sacó un punto más que en la segunda, y los puntos de la primera quintuplicaban la diferencia entre los de la tercera y la primera. ¿Qué puntuación sacó en cada pregunta?",
     r"$p_1+p_2+p_3=7,5,\ p_3=p_2+1,\ p_1=5(p_3-p_1)$: \ " + R(r"2,5;\ \ 2;\ \ 3\ \text{puntos}")),
 (3, r"Un inversor reparte 42\,000\,€ entre una cuenta de ahorro al 5\,\%, un depósito a plazo fijo al 7\,\% y unos bonos al 9\,\% anual. En un año obtiene 2600\,€ de intereses, y los de la cuenta de ahorro son 200\,€ menos que la suma de los de las otras dos inversiones. ¿Cuánto invirtió en cada producto?",
     r"$a+b+c=42000,\ 0,05a+0,07b+0,09c=2600,\ 0,05a=0,07b+0,09c-200$: \ " + R(r"24\,000\,€,\ 11\,000\,€,\ 7000\,€")),
 (2, r"El largo de un rectángulo es 1 cm más que el doble del ancho. Queremos que el perímetro sea como mínimo de 20 cm y como máximo de 30 cm. ¿Entre qué valores puede estar el ancho?",
     r"$20\le2(x+2x+1)\le30\Rightarrow20\le6x+2\le30$: \ " + RI(S88) + r" \ (en cm)"),
 (2, r"Un artesano fabrica collares y pulseras. Un collar necesita 2 horas de trabajo y 1 unidad de material, y una pulsera, 1 hora y 2 unidades de material. Cada semana dispone, como máximo, de 40 horas y 50 unidades de material." +
     tasks(1, ["Plantea el sistema de inecuaciones y representa la región de las posibles combinaciones de collares y pulseras.", "¿Puede fabricar 15 collares y 12 pulseras en una semana? ¿Y 10 collares y 20 pulseras?"]),
     tasks(1, [r"$2x+y\le40,\ x+2y\le50,\ x\ge0,\ y\ge0$. Vértices $(0,0)$, $(20,0)$, $(10,20)$ y $(0,25)$.\par" + fig(R89, (-2, 28, -2, 28), wd=4.2, pts=[((15, 12), False), ((10, 20), True)]),
               r"$(15,12)$: $2\cdot15+12=42\gt40$: \rest{no} (faltan horas). \ $(10,20)$: $40\le40$ y $50\le50$: \rest{sí}, y aprovecha todas las horas y todo el material."])),
]))

# =====================================================================
# 6. Ampliació (exercicis nous)
aP = sp.Symbol('a')
M98 = sp.Matrix([[1, 1, 1, 3], [1, -1, 1, 1], [2, 0, aP, 4]])
ck(sp.linsolve([x + y + z - 3, x - y + z - 1, 2 * x + 5 * z - 4], [x, y, z]) == sp.FiniteSet((2, 1, 0)))
ck(sp.linsolve([x + y + z - 3, x - y + z - 1, 2 * x + 2 * z - 4], [x, y, z]) == sp.FiniteSet((2 - z, 1, z)))
ck(sp.linsolve([x + y + z - 3, x - y + z - 1, 2 * x + 2 * z - 5], [x, y, z]) == sp.EmptySet)
lin([x - 2 - 3 * (y - 2), x + 10 - 2 * (y + 10)], [x, y], [38, 14])
lin([x * 0 + x + y - 5, x - y + 1], [x, y], [2, 3])
ck(set(sp.solve(x ** 2 - 5 * x + 6, x)) == {2, 3})
R103 = regck([C(1, 0, '>=', 0), C(0, 1, '>=', 0), C(1, 2, '<=', 4)], [(0, 0), (4, 0), (0, 2)], True)
S.append(("Ampliación y problemas", [
 (3, r"Clasifica el sistema según los valores de $a$ y resuélvelo cuando sea compatible: \ $" + sist(r"x+y+z=3", r"x-y+z=1", r"2x+az=4") + "$",
     r"$\left(\begin{array}{rrr|r}1&1&1&3\\1&-1&1&1\\2&0&a&4\end{array}\right)\to\left(\begin{array}{rrr|r}1&1&1&3\\0&-2&0&-2\\0&-2&a-2&-2\end{array}\right)\to\left(\begin{array}{rrr|r}1&1&1&3\\0&-2&0&-2\\0&0&a-2&0\end{array}\right)$\par"
     + r" Si $a\neq2$: \rest{SCD}, " + R(r"(2,\ 1,\ 0)") + r". \ Si $a=2$: \rest{SCI}, " + R(r"(2-\lambda,\ 1,\ \lambda)") + r". (Nunca es incompatible.)"),
 (2, r"Un rectángulo tiene 10 cm de perímetro y 6 cm$^2$ de área. ¿Cuáles son sus dimensiones?", r"$x+y=5,\ xy=6\Rightarrow x^2-5x+6=0$: \ " + R(r"2\ \text{cm}\times3\ \text{cm}")),
 (2, r"Hace 2 años la edad de un padre era el triple de la del hijo y dentro de 10 años será el doble. ¿Cuántos años tienen ahora?", r"$p-2=3(f-2),\ p+10=2(f+10)$: \ " + R(r"\text{padre }38,\ \text{hijo }14\ \text{años}")),
 (3, r"Escribe un sistema de inecuaciones cuya solución sea el triángulo de vértices $(0,0)$, $(4,0)$ y $(0,2)$, con los bordes incluidos.",
     R(r"x\ge0,\ \ y\ge0,\ \ x+2y\le4") + r" \ (la recta por $(4,0)$ y $(0,2)$ es $x+2y=4$, y $O$ la cumple).\par" + fig(R103, (-1, 5, -1, 3), wd=3.6)),
]))

bad = [mm for c_, mm in CHK if not c_]
assert not bad, bad[:5]
assert [len(s_[1]) for s_ in S] == [2, 3, 1, 2, 20, 4], [len(s_[1]) for s_ in S]

# =====================================================================

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "sistemas de ecuaciones, Gauss, sistemas no lineales, inecuaciones, sistemas de inecuaciones, regiones del plano"
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre = pre.replace(r'\usepackage{tikz}', '\\usepackage{tikz}\n\\usetikzlibrary{calc}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'\providecommand{\lt}{<}\providecommand{\gt}{>}' + '\n'
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

TIT = "Sistemas de ecuaciones e inecuaciones"
def spc(t):
    # «, » separa elements; amb icomma la coma és un símbol normal i un «-» darrere seu seria una resta: el posem entre claus
    return re.sub(r'\$[^$]*\$', lambda mm: re.sub(r',((?:\\,|\\ |\\;|\s)+)-', r',\1{-}', mm.group(0).replace(', ', r',\, ')), t)
def build(sol):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 3: %s' % (t, TIT), capcalera='%s · Unidad 3: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-mi')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1batx-mi') + '{' + ('Soluciones de la ficha · Unidad 3' if sol else 'Ficha de ejercicios · Unidad 3') + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.8cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los resultados se dan de manera exacta (fracciones y raíces) y, cuando hace falta, con el valor aproximado. Puedes comprobar Gauss, los sistemas no lineales y las regiones con las herramientas interactivas de los apuntes de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Da los resultados de manera exacta y, si hace falta, también aproximados. En los sistemas con denominadores, radicales o logaritmos, comprueba siempre las soluciones. Los ejercicios 1--28 son de la ficha del departamento; la sección 6 tiene otros nuevos para ampliar y aplicar lo que has aprendido.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, spc(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't3-fitxa-solucions-es.tex' if sol else 't3-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S), 'ejercicios;', len(CHK), 'comprobaciones')
