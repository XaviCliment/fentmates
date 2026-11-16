# Genera t3-fitxa-exercicis.tex i t3-fitxa-solucions.tex (1r Batxillerat CCSS, Unitat 3: Inequacions i sistemes d'inequacions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Bilingüe: T(valencià, castellà); genera-es.py l'executa amb FM_LANG=es i escriu els -es.tex.
# Les eines (recta real, semiplans i regions en TikZ amb aritmètica exacta) són les de la fitxa de la unitat 3 de 1r Batx MI.
# sympy resol cada inequació i sistema (ineq, sysI) i ck() les compara amb la solució esperada escrita a mà; les regions es
# comproven amb regck (vèrtexs exactes) i els problemes de programació lineal amb pl() (vèrtexs, valors de F i òptim).
# Ús: python3 genera.py && python3 genera-es.py, i pdflatex (dues vegades) dels quatre .tex
import os, re, math
from fractions import Fraction as F
import sympy as sp
from sympy import Rational as Q, oo
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va
xr = sp.Symbol('x', real=True)
x = xr

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def L(e):
    s = sp.latex(e, order='lex')
    return s.replace(r'\left(', '(').replace(r'\right)', ')')
def sist(*rows): return r'\left\{\begin{array}{l}' + r'\\'.join(rows) + r'\end{array}\right.'
NOSOL = T(r'\text{no té solució}', r'\text{no tiene solución}')

CHK = []
def ck(cond, msg=''):
    CHK.append((bool(cond), msg)); return cond

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
    step = 5 if hi - lo > 30 else 2 if hi - lo > 14 else 1
    if step > 1: lo, hi = step * math.floor(lo / step), step * math.ceil(hi / step)
    sc = min(0.42, 7.2 / (hi - lo + 1.4))
    o = [r'\begin{tikzpicture}[x=%.3fcm,baseline=-3pt]' % sc, r'\draw[-latex,muted] (%g,0)--(%g,0);' % (lo - 0.6 * step, hi + 0.7 * step)]
    v = lo
    while v <= hi:
        o.append(r'\draw[muted] (%d,0.1)--(%d,-0.1) node[below=-1pt,font=\scriptsize,text=muted]{$%d$};' % (v, v, v)); v += step
    for a_, ac, b_, bc in S:
        xa = lo - 0.45 * step if a_ == -oo else float(a_); xb = hi + 0.45 * step if b_ == oo else float(b_)
        if a_ != b_: o.append(r'\draw[accent,line width=2.6pt] (%g,0)--(%g,0);' % (xa, xb))
        if a_ == -oo: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xa - 0.3 * step, xa + 0.1 * step, xa + 0.1 * step))
        if b_ == oo: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xb + 0.3 * step, xb - 0.1 * step, xb - 0.1 * step))
        for xv, c, lab in ((a_, ac, True), (b_, bc, a_ != b_)):
            if xv in (oo, -oo) or not lab: continue
            o.append((r'\fill[accent] (%g,0) circle (2.3pt);' if c else r'\filldraw[fill=white,draw=accent,line width=1.1pt] (%g,0) circle (2.3pt);') % float(xv))
            if not xv.is_integer or step > 1: o.append(r'\node[above=1pt,font=\scriptsize,text=accent] at (%g,0) {$%s$};' % (float(xv), L(xv)))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def RI(Sset): return (R('x\\in ' + st(Sset)) + r'\\[2pt]' + recta(Sset)) if Sset != sp.S.EmptySet else R(NOSOL)
def ineq(e): return sp.solve_univariate_inequality(e, xr, relational=False)
def sysI(*es):
    s_ = sp.S.Reals
    for e in es: s_ = s_.intersect(ineq(e))
    return s_
def Io(a_, b_): return sp.Interval.open(a_, b_)
def Ic(a_, b_): return sp.Interval(a_, b_)
def Ilo(a_, b_): return sp.Interval.Lopen(a_, b_)
def Iro(a_, b_): return sp.Interval.Ropen(a_, b_)
def iq(e, expect):
    """resol la inequació (o el sistema, si e és una llista) i comprova que la solució és l'esperada"""
    S_ = sysI(*e) if isinstance(e, (list, tuple)) else ineq(e)
    ck(S_ == expect, 'inequacio %s -> %s (esperat %s)' % (e, S_, expect))
    return S_

# ---------- semiplans i regions (com a la unitat 3 de 1r Batx MI) ----------
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
def fig(cons, view, wd=4.6, hmax=4.4, labels=True, pts=(), level=None):
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
    lines = [(A, B, op, c, COL[j % len(COL)]) for j, (A, B, op, c) in enumerate(cons)]
    if level: lines.append((fr(level[0]), fr(level[1]), '<', fr(level[2]), 'green!50!black'))
    for A, B, op, c, col in lines:
        a_, b_, c_ = float(A), float(B), float(c)
        if abs(b_) > abs(a_): P = [(x0 - 1, (c_ - a_ * (x0 - 1)) / b_), (x1 + 1, (c_ - a_ * (x1 + 1)) / b_)]
        else: P = [((c_ - b_ * (y0 - 1)) / a_, y0 - 1), ((c_ - b_ * (y1 + 1)) / a_, y1 + 1)]
        s += r'\draw[%s,line width=1.1pt%s] (%.4f,%.4f)--(%.4f,%.4f);' % (col, ',dashed' if op in ('<', '>') else '', P[0][0], P[0][1], P[1][0], P[1][1])
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
NN = [C(1, 0, '>=', 0), C(0, 1, '>=', 0)]

# ---------- programació lineal ----------
def pl(cons, a_, b_, goal, expect_opt, expect_val, view, wd=4.4, unit=''):
    """vèrtexs, valor de F = a x + b y en cada un i òptim (comprovats); torna (text dels valors, text de l'òptim, figura)"""
    V, bd = verts(cons)
    a_, b_ = fr(a_), fr(b_)
    Fv = [(v, a_ * v[0] + b_ * v[1]) for v in V]
    best = (max if goal == 'max' else min)(f for _, f in Fv)
    opt = [v for v, f in Fv if f == best]
    ck(best == fr(expect_val), 'optim %s != %s' % (best, expect_val))
    ck(sorted(opt) == sorted((fr(p[0]), fr(p[1])) for p in expect_opt), 'punts optims %s' % opt)
    if not bd:  # regió no fitada: comprovem que l'òptim existeix (F no millora als vèrtexs artificials)
        P = region(cons, (-BIG, BIG, -BIG, BIG))
        far = [a_ * p[0] + b_ * p[1] for p in P if p not in V]
        ck(all((f <= best) if goal == 'max' else (f >= best) for f in far), 'optim no fitat')
    # ordre dels vèrtexs: el de la regió (antihorari)
    vals = r';\ '.join('F%s=%s' % (pt(v), tn(f)) for v, f in Fv)
    return vals, best, opt, fig(cons, view, wd=wd, level=(a_, b_, best))

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Inequacions de primer grau
A1 = [iq(3 * x - 7 > 5, Io(4, oo)), iq(2 * x + 5 <= 4 * x - 1, Iro(3, oo)), iq(5 - 2 * x >= 11, Ilo(-oo, -3)),
      iq(4 * (x - 1) < 2 * x + 6, Io(-oo, 5)), iq(3 * (2 - x) >= 2 * (x + 8), Ilo(-oo, -2)), iq(x - 2 * (x + 3) > 4 - 3 * x, Io(5, oo))]
A2 = [iq(x / 2 + 1 <= x / 3 + 2, Ilo(-oo, 6)), iq((x - 1) / 3 - (x + 2) / 4 > 1, Io(22, oo)), iq((2 * x + 1) / 5 >= (x - 3) / 2, Ilo(-oo, 17)),
      iq(x - (x + 1) / 2 < (x - 2) / 3, Io(-oo, -1))]
A3 = [iq(2 * (x + 3) > 2 * x + 1, sp.S.Reals), iq(3 * x - 1 <= 3 * (x - 2), sp.S.EmptySet)]
A4 = iq(30 + 25 * x < 30 * x, Io(6, oo))
A5 = iq([16 + 2 * x <= 30, x > 0], Ilo(0, 7))
A6 = iq(900 + Q(5, 100) * x >= 1400, Iro(10000, oo))
S.append((T("Inequacions de primer grau", "Inecuaciones de primer grado"), [
 (1, T(r"Resol les inequacions següents i representa'n la solució:", r"Resuelve las inecuaciones siguientes y representa su solución:") + tasks(3, [r"$3x-7\gt5$", r"$2x+5\le4x-1$", r"$5-2x\ge11$", r"$4(x-1)\lt2x+6$", r"$3(2-x)\ge2(x+8)$", r"$x-2(x+3)\gt4-3x$"])
     + recorda(T(r"Si multipliques o divideixes per un nombre negatiu, la desigualtat canvia de sentit.", r"Si multiplicas o divides por un número negativo, la desigualdad cambia de sentido.")),
     tasks(2, [r"$3x\gt12\Rightarrow x\gt4$: \ " + RI(A1[0]), r"$-2x\le-6\Rightarrow x\ge3$: \ " + RI(A1[1]), r"$-2x\ge6\Rightarrow x\le-3$: \ " + RI(A1[2]),
               r"$2x\lt10\Rightarrow x\lt5$: \ " + RI(A1[3]), r"$-5x\ge10\Rightarrow x\le-2$: \ " + RI(A1[4]), r"$-x-6\gt4-3x\Rightarrow x\gt5$: \ " + RI(A1[5])])),
 (2, T(r"Resol les inequacions amb denominadors:", r"Resuelve las inecuaciones con denominadores:") + tasks(2, [r"$\dfrac{x}{2}+1\le\dfrac{x}{3}+2$", r"$\dfrac{x-1}{3}-\dfrac{x+2}{4}\gt1$", r"$\dfrac{2x+1}{5}\ge\dfrac{x-3}{2}$", r"$x-\dfrac{x+1}{2}\lt\dfrac{x-2}{3}$"]),
     tasks(2, [r"$\cdot6$: $3x+6\le2x+12\Rightarrow x\le6$: \ " + RI(A2[0]), r"$\cdot12$: $x-10\gt12\Rightarrow x\gt22$: \ " + RI(A2[1]),
               r"$\cdot10$: $4x+2\ge5x-15\Rightarrow x\le17$: \ " + RI(A2[2]), r"$\cdot6$: $3x-3\lt2x-4\Rightarrow x\lt-1$: \ " + RI(A2[3])])),
 (2, T(r"Resol i interpreta el resultat:", r"Resuelve e interpreta el resultado:") + tasks(2, [r"$2(x+3)\gt2x+1$", r"$3x-1\le3(x-2)$"]),
     tasks(2, [T(r"$2x+6\gt2x+1\Rightarrow0\gt-5$, cert sempre: ", r"$2x+6\gt2x+1\Rightarrow0\gt-5$, cierto siempre: ") + R(r"x\in\mathbb R"),
               T(r"$3x-1\le3x-6\Rightarrow0\le-5$, fals sempre: ", r"$3x-1\le3x-6\Rightarrow0\le-5$, falso siempre: ") + R(NOSOL)])),
 (2, T(r"Un gimnàs A cobra 30 € de matrícula i 25 € al mes, i un gimnàs B no cobra matrícula però costa 30 € al mes. A partir de quants mesos és més barat el gimnàs A?",
       r"Un gimnasio A cobra 30 € de matrícula y 25 € al mes, y un gimnasio B no cobra matrícula pero cuesta 30 € al mes. ¿A partir de cuántos meses es más barato el gimnasio A?"),
     T(r"$x=$ mesos: $30+25x\lt30x\Rightarrow-5x\lt-30\Rightarrow x\gt6$. ", r"$x=$ meses: $30+25x\lt30x\Rightarrow-5x\lt-30\Rightarrow x\gt6$. ") + R(T(r"\text{A partir de 7 mesos}", r"\text{A partir de 7 meses}"))),
 (2, T(r"Un costat d'un rectangle mesura 8 cm. Quant pot mesurar l'altre costat perquè el perímetre no supere els 30 cm?",
       r"Un lado de un rectángulo mide 8 cm. ¿Cuánto puede medir el otro lado para que el perímetro no supere los 30 cm?"),
     T(r"$16+2x\le30\Rightarrow x\le7$, i a més $x\gt0$: ", r"$16+2x\le30\Rightarrow x\le7$, y además $x\gt0$: ") + R(r"x\in(0,\,7]") + T(r" (entre 0 i 7 cm, 7 inclòs).", r" (entre 0 y 7 cm, 7 incluido).")),
 (2, T(r"Un venedor cobra 900 € fixos al mes més un 5\,\% de les vendes. Quant ha de vendre per a cobrar com a mínim 1\,400 €?",
       r"Un vendedor cobra 900 € fijos al mes más un 5\,\% de las ventas. ¿Cuánto tiene que vender para cobrar como mínimo 1\,400 €?"),
     r"$900+0{,}05x\ge1400\Rightarrow0{,}05x\ge500\Rightarrow x\ge10\,000$. " + R(T(r"\text{Com a mínim }10\,000\text{ €}", r"\text{Como mínimo }10\,000\text{ €}"))),
]))

# =====================================================================
# 2. Inequacions de segon grau
B1 = [iq(x ** 2 - 3 * x - 4 < 0, Io(-1, 4)), iq(x ** 2 - x - 6 >= 0, sp.Union(Ilo(-oo, -2), Iro(3, oo))), iq(x ** 2 - 16 > 0, sp.Union(Io(-oo, -4), Io(4, oo))),
      iq(x ** 2 + 3 * x <= 0, Ic(-3, 0)), iq(-x ** 2 + 4 * x - 3 > 0, Io(1, 3)), iq(2 * x ** 2 - 5 * x + 2 <= 0, Ic(Q(1, 2), 2))]
B2 = [iq(x ** 2 + x + 1 > 0, sp.S.Reals), iq(x ** 2 + 2 * x + 4 <= 0, sp.S.EmptySet), iq(x ** 2 - 4 * x + 4 > 0, sp.Union(Io(-oo, 2), Io(2, oo))), iq(x ** 2 - 6 * x + 9 <= 0, sp.FiniteSet(3))]
B3 = [iq(x * (x - 2) > 3, sp.Union(Io(-oo, -1), Io(3, oo))), iq((x + 1) ** 2 <= 2 * x + 5, Ic(-2, 2)), iq(x ** 2 / 2 - x >= 4, sp.Union(Ilo(-oo, -2), Iro(4, oo)))]
B4 = iq(-x ** 2 + 10 * x - 16 > 0, Io(2, 8))
B5 = iq(x ** 2 + x < 12, Io(-4, 3))
S.append((T("Inequacions de segon grau", "Inecuaciones de segundo grado"), [
 (1, T(r"Resol:", r"Resuelve:") + tasks(3, [r"$x^2-3x-4\lt0$", r"$x^2-x-6\ge0$", r"$x^2-16\gt0$", r"$x^2+3x\le0$", r"$-x^2+4x-3\gt0$", r"$2x^2-5x+2\le0$"])
     + recorda(T(r"Calcula les arrels, divideix la recta en intervals i estudia el signe en cada un (o pensa en la paràbola).", r"Calcula las raíces, divide la recta en intervalos y estudia el signo en cada uno (o piensa en la parábola).")),
     tasks(2, [T(r"Arrels $-1$ i $4$: ", r"Raíces $-1$ y $4$: ") + RI(B1[0]), T(r"Arrels $-2$ i $3$: ", r"Raíces $-2$ y $3$: ") + RI(B1[1]), T(r"Arrels $\pm4$: ", r"Raíces $\pm4$: ") + RI(B1[2]),
               r"$x(x+3)\le0$: \ " + RI(B1[3]), r"$x^2-4x+3\lt0$, " + T(r"arrels $1$ i $3$: ", r"raíces $1$ y $3$: ") + RI(B1[4]), T(r"Arrels $\frac12$ i $2$: ", r"Raíces $\frac12$ y $2$: ") + RI(B1[5])])),
 (2, T(r"Resol aquests casos especials:", r"Resuelve estos casos especiales:") + tasks(2, [r"$x^2+x+1\gt0$", r"$x^2+2x+4\le0$", r"$x^2-4x+4\gt0$", r"$x^2-6x+9\le0$"]),
     tasks(2, [T(r"$\Delta\lt0$, sempre positiu: ", r"$\Delta\lt0$, siempre positivo: ") + R(r"\mathbb R"), T(r"$\Delta\lt0$, sempre positiu: ", r"$\Delta\lt0$, siempre positivo: ") + R(NOSOL),
               r"$(x-2)^2\gt0$: \ " + R(r"\mathbb R-\{2\}"), r"$(x-3)^2\le0$: \ " + R(r"x=3"),])),
 (2, T(r"Passa-ho tot a un membre i resol:", r"Pásalo todo a un miembro y resuelve:") + tasks(3, [r"$x(x-2)\gt3$", r"$(x+1)^2\le2x+5$", r"$\dfrac{x^2}{2}-x\ge4$"]),
     tasks(1, [r"$x^2-2x-3\gt0$: \ " + RI(B3[0]), r"$x^2-4\le0$: \ " + RI(B3[1]), r"$x^2-2x-8\ge0$: \ " + RI(B3[2])])),
 (2, T(r"El benefici d'una empresa, en milers d'euros, quan ven $x$ centenars d'unitats és $B(x)=-x^2+10x-16$. Quantes unitats ha de vendre per a tindre beneficis ($B(x)\gt0$)?",
       r"El beneficio de una empresa, en miles de euros, cuando vende $x$ centenares de unidades es $B(x)=-x^2+10x-16$. ¿Cuántas unidades tiene que vender para tener beneficios ($B(x)\gt0$)?"),
     T(r"$x^2-10x+16\lt0$, arrels $2$ i $8$: $x\in(2,\,8)$. ", r"$x^2-10x+16\lt0$, raíces $2$ y $8$: $x\in(2,\,8)$. ") + R(T(r"\text{Entre 200 i 800 unitats}", r"\text{Entre 200 y 800 unidades}"))),
 (2, T(r"La suma d'un nombre i el seu quadrat és menor que 12. Quins valors pot prendre el nombre?", r"La suma de un número y su cuadrado es menor que 12. ¿Qué valores puede tomar el número?"),
     T(r"$x^2+x-12\lt0$, arrels $-4$ i $3$: ", r"$x^2+x-12\lt0$, raíces $-4$ y $3$: ") + RI(B5)),
]))
ck(sp.solve(x ** 2 + x + 1) == [] and sp.solve(x ** 2 + 2 * x + 4) == [])

# =====================================================================
# 3. Inequacions de grau superior
C1 = [iq(x ** 3 - 4 * x >= 0, sp.Union(Ic(-2, 0), Iro(2, oo))), iq((x - 1) * (x + 2) * (x - 3) < 0, sp.Union(Io(-oo, -2), Io(1, 3))),
      iq(x ** 3 - x ** 2 - 2 * x > 0, sp.Union(Io(-1, 0), Io(2, oo))), iq(x ** 3 - 6 * x ** 2 + 11 * x - 6 >= 0, sp.Union(Ic(1, 2), Iro(3, oo)))]
C2 = [iq(x ** 3 + x ** 2 - x - 1 <= 0, Ilo(-oo, 1)), iq(x ** 2 * (x - 3) <= 0, Ilo(-oo, 3)), iq((x + 2) ** 2 * (x - 1) > 0, Io(1, oo))]
C3 = iq(x ** 4 - 5 * x ** 2 + 4 > 0, sp.Union(Io(-oo, -2), Io(-1, 1), Io(2, oo)))
ck(sp.factor(x ** 3 - 6 * x ** 2 + 11 * x - 6) == (x - 1) * (x - 2) * (x - 3))
ck(sp.expand((x - 1) * (x + 1) ** 2 - (x ** 3 + x ** 2 - x - 1)) == 0)
S.append((T("Inequacions de grau superior", "Inecuaciones de grado superior"), [
 (2, T(r"Factoritza i resol amb una taula de signes:", r"Factoriza y resuelve con una tabla de signos:") + tasks(2, [r"$x^3-4x\ge0$", r"$(x-1)(x+2)(x-3)\lt0$", r"$x^3-x^2-2x\gt0$", r"$x^3-6x^2+11x-6\ge0$"]),
     tasks(1, [r"$x(x+2)(x-2)\ge0$: \ " + RI(C1[0]), T(r"Arrels $-2,\ 1,\ 3$: ", r"Raíces $-2,\ 1,\ 3$: ") + RI(C1[1]), r"$x(x+1)(x-2)\gt0$: \ " + RI(C1[2]),
               T(r"Ruffini: $(x-1)(x-2)(x-3)\ge0$: \ ", r"Ruffini: $(x-1)(x-2)(x-3)\ge0$: \ ") + RI(C1[3])])),
 (3, T(r"Compte amb les arrels dobles: un factor al quadrat no canvia de signe. Resol:", r"Cuidado con las raíces dobles: un factor al cuadrado no cambia de signo. Resuelve:") + tasks(3, [r"$x^3+x^2-x-1\le0$", r"$x^2(x-3)\le0$", r"$(x+2)^2(x-1)\gt0$"]),
     tasks(1, [r"$(x-1)(x+1)^2\le0$: \ " + RI(C2[0]), T(r"$x^2\ge0$ sempre, i val 0 en $x=0$: ", r"$x^2\ge0$ siempre, y vale 0 en $x=0$: ") + RI(C2[1]),
               T(r"$(x+2)^2\gt0$ si $x\ne-2$, i cal $x-1\gt0$: ", r"$(x+2)^2\gt0$ si $x\ne-2$, y hace falta $x-1\gt0$: ") + RI(C2[2])])),
 (3, T(r"Resol la inequació biquadrada $x^4-5x^2+4\gt0$.", r"Resuelve la inecuación bicuadrada $x^4-5x^2+4\gt0$."),
     T(r"$x^2=t$: $t^2-5t+4=0\Rightarrow t=1,\ t=4$; arrels $\pm1,\ \pm2$: $(x+2)(x+1)(x-1)(x-2)\gt0$: \ ", r"$x^2=t$: $t^2-5t+4=0\Rightarrow t=1,\ t=4$; raíces $\pm1,\ \pm2$: $(x+2)(x+1)(x-1)(x-2)\gt0$: \ ") + RI(C3)),
]))

# =====================================================================
# 4. Sistemes d'inequacions amb una incògnita
D1 = [iq([x + 3 > 0, 2 * x - 1 <= 5], Ilo(-3, 3)), iq([3 * x - 2 < x + 4, 5 - x <= 2 * x + 2], Iro(1, 3)), iq([2 * x + 1 > x + 4, 3 * x - 5 < x + 1], sp.S.EmptySet),
      iq([(x + 1) / 2 >= x - 1, 4 * x + 3 > x], Ilo(-1, 3)), iq([x ** 2 - 4 < 0, 2 * x + 1 >= 0], Iro(-Q(1, 2), 2)), iq([x ** 2 - 5 * x + 4 <= 0, x ** 2 - 9 > 0], Ilo(3, 4))]
D2 = iq([3 * x - 5 > 10, 2 * x + 1 < 21], Io(5, 10))
D3 = iq([80 * x >= 400, 80 * x <= 600], Ic(5, Q(15, 2)))
S.append((T("Sistemes d'inequacions amb una incògnita", "Sistemas de inecuaciones con una incógnita"), [
 (2, T(r"Resol els sistemes d'inequacions:", r"Resuelve los sistemas de inecuaciones:") + tasks(3, ["$" + sist(r"x+3\gt0", r"2x-1\le5") + "$", "$" + sist(r"3x-2\lt x+4", r"5-x\le2x+2") + "$", "$" + sist(r"2x+1\gt x+4", r"3x-5\lt x+1") + "$",
      "$" + sist(r"\dfrac{x+1}{2}\ge x-1", r"4x+3\gt x") + "$", "$" + sist(r"x^2-4\lt0", r"2x+1\ge0") + "$", "$" + sist(r"x^2-5x+4\le0", r"x^2-9\gt0") + "$"])
     + recorda(T(r"La solució del sistema és la intersecció de les solucions: dibuixa-les en rectes una sobre l'altra.", r"La solución del sistema es la intersección de las soluciones: dibújalas en rectas una sobre la otra.")),
     tasks(1, [T(r"$x\gt-3$ i $x\le3$: \ ", r"$x\gt-3$ y $x\le3$: \ ") + RI(D1[0]), T(r"$x\lt3$ i $x\ge1$: \ ", r"$x\lt3$ y $x\ge1$: \ ") + RI(D1[1]), T(r"$x\gt3$ i $x\lt3$: \ ", r"$x\gt3$ y $x\lt3$: \ ") + RI(D1[2]),
               T(r"$x\le3$ i $x\gt-1$: \ ", r"$x\le3$ y $x\gt-1$: \ ") + RI(D1[3]), T(r"$(-2,\,2)$ i $x\ge-\frac12$: \ ", r"$(-2,\,2)$ y $x\ge-\frac12$: \ ") + RI(D1[4]),
               T(r"$[1,\,4]$ i $(-\infty,-3)\cup(3,+\infty)$: \ ", r"$[1,\,4]$ y $(-\infty,-3)\cup(3,+\infty)$: \ ") + RI(D1[5])])),
 (2, T(r"Troba els nombres naturals tals que el seu triple menys 5 és major que 10 i el seu doble més 1 és menor que 21.", r"Halla los números naturales tales que su triple menos 5 es mayor que 10 y su doble más 1 es menor que 21."),
     "$" + sist(r"3x-5\gt10", r"2x+1\lt21") + r"\Rightarrow" + sist(r"x\gt5", r"x\lt10") + "$: $x\\in(5,\\,10)$. " + R(r"6,\ 7,\ 8,\ 9")),
 (2, T(r"Una família vol recórrer entre 400 i 600 km en un dia a una velocitat mitjana de 80 km/h. Quantes hores ha de conduir?", r"Una familia quiere recorrer entre 400 y 600 km en un día a una velocidad media de 80 km/h. ¿Cuántas horas tiene que conducir?"),
     "$" + sist(r"80t\ge400", r"80t\le600") + r"\Rightarrow5\le t\le7{,}5$. " + R(T(r"\text{Entre 5 i 7,5 hores}", r"\text{Entre 5 y 7,5 horas}"))),
]))

# =====================================================================
# 5. Inequacions amb dues incògnites
E1 = [([C(1, 1, '<=', 4)], (-2, 6, -2, 6), T(r"Recta contínua per $(4,0)$ i $(0,4)$; $O$: $0\le4$ \checkmark: semiplà de $O$.", r"Recta continua por $(4,0)$ y $(0,4)$; $O$: $0\le4$ \checkmark: semiplano de $O$.")),
      ([C(2, -1, '>', 2)], (-2, 4, -4, 3), T(r"Recta discontínua per $(1,0)$ i $(0,-2)$; $O$: $0\gt2$ fals: semiplà que \rest{no} conté $O$.", r"Recta discontinua por $(1,0)$ y $(0,-2)$; $O$: $0\gt2$ falso: semiplano que \rest{no} contiene $O$.")),
      ([C(-3, 1, '<', 0)], (-3, 3, -4, 4), T(r"Recta discontínua per $(0,0)$ i $(1,3)$; amb $(1,0)$: $0\lt3$ \checkmark: semiplà de $(1,0)$.", r"Recta discontinua por $(0,0)$ y $(1,3)$; con $(1,0)$: $0\lt3$ \checkmark: semiplano de $(1,0)$.")),
      ([C(1, 0, '>=', -2)], (-4, 3, -3, 3), T(r"Recta vertical contínua $x=-2$; $O$: $0\ge-2$ \checkmark: semiplà de la dreta.", r"Recta vertical continua $x=-2$; $O$: $0\ge-2$ \checkmark: semiplano de la derecha."))]
E3 = regck([C(2, 4, '<=', 20)] + NN, [(0, 0), (10, 0), (0, 5)], True)
ck(2 * 4 + 4 * 3 <= 20)
S.append((T("Inequacions amb dues incògnites", "Inecuaciones con dos incógnitas"), [
 (1, T(r"Representa la solució de les inequacions:", r"Representa la solución de las inecuaciones:") + tasks(4, [r"$x+y\le4$", r"$2x-y\gt2$", r"$y\lt3x$", r"$x\ge-2$"])
     + recorda(T(r"Dibuixa la recta (contínua si és $\le,\ge$; discontínua si és $\lt,\gt$) i prova un punt que no hi estiga, com $O(0,0)$.", r"Dibuja la recta (continua si es $\le,\ge$; discontinua si es $\lt,\gt$) y prueba un punto que no esté en ella, como $O(0,0)$.")),
     tasks(2, [E1[i][2] + r"\par" + fig(E1[i][0], E1[i][1], wd=3.6, labels=False) for i in range(4)])),
 (1, T(r"Comprova si els punts $A(1,2)$, $B(3,1)$ i $C(-1,4)$ són solució de la inequació $2x+y\le5$.", r"Comprueba si los puntos $A(1,2)$, $B(3,1)$ y $C(-1,4)$ son solución de la inecuación $2x+y\le5$."),
     T(r"$A$: $2+2=4\le5$ \checkmark. \ $B$: $6+1=7\le5$ fals. \ $C$: $-2+4=2\le5$ \checkmark. \ ", r"$A$: $2+2=4\le5$ \checkmark. \ $B$: $6+1=7\le5$ falso. \ $C$: $-2+4=2\le5$ \checkmark. \ ") + R(T(r"A\text{ i }C\text{ sí; }B\text{ no}", r"A\text{ y }C\text{ sí; }B\text{ no}"))),
 (2, T(r"Amb 20 € com a màxim volem comprar bolígrafs de 2 € i quaderns de 4 €. Escriu les inequacions que han de complir el nombre de bolígrafs, $x$, i de quaderns, $y$, i representa-les. Podem comprar 4 bolígrafs i 3 quaderns?",
       r"Con 20 € como máximo queremos comprar bolígrafos de 2 € y cuadernos de 4 €. Escribe las inecuaciones que tienen que cumplir el número de bolígrafos, $x$, y de cuadernos, $y$, y represéntalas. ¿Podemos comprar 4 bolígrafos y 3 cuadernos?"),
     r"$2x+4y\le20,\ x\ge0,\ y\ge0$. \ " + T(r"$(4,3)$: $8+12=20\le20$: ", r"$(4,3)$: $8+12=20\le20$: ") + R(T(r"\text{sí (gastem just 20 €)}", r"\text{sí (gastamos justo 20 €)}")) + r"\par" + fig(E3, (-1, 11, -1, 6), wd=4.2, pts=[((4, 3), True)])),
]))

# =====================================================================
# 6. Sistemes d'inequacions amb dues incògnites
F1 = [(regck([C(1, 1, '<=', 4)] + NN, [(0, 0), (4, 0), (0, 4)], True), (-1, 5, -1, 5)),
      (regck([C(1, 2, '<=', 8), C(1, 0, '<=', 4)] + NN, [(0, 0), (4, 0), (4, 2), (0, 4)], True), (-1, 6, -1, 5)),
      (regck([C(-1, 1, '<=', 0), C(1, 0, '<=', 3), C(0, 1, '>=', 0)], [(0, 0), (3, 0), (3, 3)], True), (-1, 4, -1, 4)),
      (regck([C(1, 1, '>=', 2), C(1, 0, '<=', 4), C(0, 1, '<=', 3)], [(-1, 3), (4, 3), (4, -2)], True), (-2, 5, -3, 4)),
      (regck([C(2, 1, '<=', 6), C(1, 1, '>=', 2)] + NN, [(2, 0), (3, 0), (0, 6), (0, 2)], True), (-1, 4, -1, 7)),
      (regck([C(1, 1, '>=', 3), C(0, 1, '>=', 1), C(1, 0, '>=', 0)], [(0, 3), (2, 1)], False), (-1, 6, -1, 6))]
FT = [T(r"Triangle de vèrtexs $(0,0)$, $(4,0)$ i $(0,4)$.", r"Triángulo de vértices $(0,0)$, $(4,0)$ y $(0,4)$."),
      T(r"Quadrilàter: $(0,0)$, $(4,0)$, $(4,2)$, $(0,4)$.", r"Cuadrilátero: $(0,0)$, $(4,0)$, $(4,2)$, $(0,4)$."),
      T(r"Triangle de vèrtexs $(0,0)$, $(3,0)$ i $(3,3)$.", r"Triángulo de vértices $(0,0)$, $(3,0)$ y $(3,3)$."),
      T(r"Triangle de vèrtexs $(-1,3)$, $(4,3)$ i $(4,-2)$.", r"Triángulo de vértices $(-1,3)$, $(4,3)$ y $(4,-2)$."),
      T(r"Quadrilàter: $(2,0)$, $(3,0)$, $(0,6)$, $(0,2)$.", r"Cuadrilátero: $(2,0)$, $(3,0)$, $(0,6)$, $(0,2)$."),
      T(r"Regió \rest{no fitada} amb vèrtexs $(0,3)$ i $(2,1)$.", r"Región \rest{no acotada} con vértices $(0,3)$ y $(2,1)$.")]
F2 = regck([C(1, 2, '<=', 2), C(1, 2, '>=', 6)], [], None)
ck(len(region(F2, (-BIG, BIG, -BIG, BIG))) == 0)
F3 = regck([C(1, 0, '>=', 1), C(1, 0, '<=', 4), C(0, 1, '>=', 1), C(0, 1, '<=', 3)], [(1, 1), (4, 1), (4, 3), (1, 3)], True)
S.append((T("Sistemes d'inequacions amb dues incògnites", "Sistemas de inecuaciones con dos incógnitas"), [
 (2, T(r"Resol els sistemes, troba els vèrtexs de la regió solució i digues si és fitada:", r"Resuelve los sistemas, halla los vértices de la región solución y di si es acotada:") + tasks(3, [
      "$" + sist(r"x+y\le4", r"x\ge0,\ y\ge0") + "$", "$" + sist(r"x+2y\le8", r"x\le4", r"x\ge0,\ y\ge0") + "$", "$" + sist(r"y\le x", r"x\le3", r"y\ge0") + "$",
      "$" + sist(r"x+y\ge2", r"x\le4", r"y\le3") + "$", "$" + sist(r"2x+y\le6", r"x+y\ge2", r"x\ge0,\ y\ge0") + "$", "$" + sist(r"x+y\ge3", r"y\ge1", r"x\ge0") + "$"])
     + recorda(T(r"Cada vèrtex és el tall de dues rectes frontera: resol el sistema format per les seues equacions.", r"Cada vértice es el corte de dos rectas frontera: resuelve el sistema formado por sus ecuaciones.")),
     tasks(2, [FT[i] + r"\par" + fig(F1[i][0], F1[i][1], wd=3.6) for i in range(6)])),
 (2, T(r"Té solució el sistema $\left\{\begin{array}{l}x+2y\le2\\ x+2y\ge6\end{array}\right.$? Raona-ho.", r"¿Tiene solución el sistema $\left\{\begin{array}{l}x+2y\le2\\ x+2y\ge6\end{array}\right.$? Razónalo."),
     T(r"Les rectes $x+2y=2$ i $x+2y=6$ són paral·leles i $x+2y$ no pot ser alhora $\le2$ i $\ge6$: ", r"Las rectas $x+2y=2$ y $x+2y=6$ son paralelas y $x+2y$ no puede ser a la vez $\le2$ y $\ge6$: ") + R(NOSOL)),
 (3, T(r"Escriu un sistema d'inequacions la solució del qual siga el rectangle de vèrtexs $(1,1)$, $(4,1)$, $(4,3)$ i $(1,3)$, amb les vores incloses.", r"Escribe un sistema de inecuaciones cuya solución sea el rectángulo de vértices $(1,1)$, $(4,1)$, $(4,3)$ y $(1,3)$, con los bordes incluidos."),
     R(r"1\le x\le4,\ \ 1\le y\le3") + r"\par" + fig(F3, (-1, 5, -1, 4), wd=3.6)),
]))

# =====================================================================
# 7. Programació lineal
G1 = [C(1, 1, '<=', 5), C(1, 0, '<=', 3)] + NN
g1 = pl(G1, 3, 2, 'max', [(3, 2)], 13, (-1, 6, -1, 6))
G2 = [C(1, 1, '>=', 4), C(1, 0, '<=', 5), C(0, 1, '<=', 5)] + NN
g2 = pl(G2, 2, 3, 'min', [(4, 0)], 8, (-1, 6, -1, 6))
G3 = [C(1, 2, '<=', 8), C(1, 0, '<=', 4)] + NN
g3 = pl(G3, 1, 2, 'max', [(4, 2), (0, 4)], 8, (-1, 6, -1, 5))
G4 = [C(1, 1, '<=', 20), C(1, 0, '<=', 12)] + NN
g4 = pl(G4, 6, 4, 'max', [(12, 8)], 104, (-2, 22, -2, 22))
G5 = [C(2, 1, '<=', 40), C(1, 1, '<=', 30)] + NN
g5 = pl(G5, 50, 30, 'max', [(10, 20)], 1100, (-3, 33, -3, 42))
G6 = [C(1, 2, '>=', 10), C(3, 1, '>=', 15)] + NN
g6 = pl(G6, 2, 3, 'min', [(4, 3)], 17, (-1, 12, -1, 17))
G7 = [C(1, 1, '<=', 10), C(0, 1, '<=', 6), C(1, 0, '>=', 2)] + NN
g7 = pl(G7, 40, 60, 'max', [(4, 6)], 520, (-1, 11, -1, 8))
G8 = [C(40, 50, '>=', 400), C(1, 0, '<=', 8), C(0, 1, '<=', 10), C(1, 1, '<=', 9)] + NN
g8 = pl(G8, 600, 800, 'min', [(5, 4)], 6200, (-1, 10, -1, 10))
regck(G8, [(0, 8), (0, 9), (5, 4)], True)
def plsol(cons_t, f_t, g, frase):
    vals, best, opt, fg = g
    return (cons_t + r'; \ ' + f_t + r'.\par ' + T(r'Vèrtexs i valors: $', r'Vértices y valores: $') + vals + r'$.\par ' + frase + r'\par' + fg)
S.append((T("Programació lineal", "Programación lineal"), [
 (1, T(r"Calcula el màxim de $F(x,y)=3x+2y$ en la regió definida per $x+y\le5$, $x\le3$, $x\ge0$, $y\ge0$.", r"Calcula el máximo de $F(x,y)=3x+2y$ en la región definida por $x+y\le5$, $x\le3$, $x\ge0$, $y\ge0$."),
     plsol(T(r"Regió fitada", r"Región acotada"), r"$F=3x+2y$", g1, T(r"Màxim: ", r"Máximo: ") + R(r"F(3,2)=13"))),
 (2, T(r"Calcula el mínim de $F(x,y)=2x+3y$ amb les restriccions $x+y\ge4$, $x\le5$, $y\le5$, $x\ge0$, $y\ge0$.", r"Calcula el mínimo de $F(x,y)=2x+3y$ con las restricciones $x+y\ge4$, $x\le5$, $y\le5$, $x\ge0$, $y\ge0$."),
     plsol(T(r"Regió fitada", r"Región acotada"), r"$F=2x+3y$", g2, T(r"Mínim: ", r"Mínimo: ") + R(r"F(4,0)=8"))),
 (3, T(r"Maximitza $F(x,y)=x+2y$ amb $x+2y\le8$, $x\le4$, $x\ge0$, $y\ge0$. Què hi observes?", r"Maximiza $F(x,y)=x+2y$ con $x+2y\le8$, $x\le4$, $x\ge0$, $y\ge0$. ¿Qué observas?"),
     plsol(T(r"Regió fitada", r"Región acotada"), r"$F=x+2y$", g3, T(r"El màxim, $F=8$, s'assoleix en $(4,2)$ i en $(0,4)$, perquè la funció objectiu és paral·lela a la restricció $x+2y\le8$: ", r"El máximo, $F=8$, se alcanza en $(4,2)$ y en $(0,4)$, porque la función objetivo es paralela a la restricción $x+2y\le8$: ")
           + R(T(r"\text{infinites solucions (tot el segment)}", r"\text{infinitas soluciones (todo el segmento)}")))),
 (2, T(r"Una pastisseria fa pastissos de xocolata i de nata. Cada dia en pot fer com a màxim 20, i com a màxim 12 de xocolata. Cada pastís de xocolata dona 6 € de benefici i cada pastís de nata, 4 €. Quants n'ha de fer de cada tipus per a obtindre el benefici màxim?",
       r"Una pastelería hace pasteles de chocolate y de nata. Cada día puede hacer como máximo 20, y como máximo 12 de chocolate. Cada pastel de chocolate da 6 € de beneficio y cada pastel de nata, 4 €. ¿Cuántos tiene que hacer de cada tipo para obtener el beneficio máximo?"),
     plsol(T(r"$x=$ xocolata, $y=$ nata: $x+y\le20,\ x\le12,\ x\ge0,\ y\ge0$", r"$x=$ chocolate, $y=$ nata: $x+y\le20,\ x\le12,\ x\ge0,\ y\ge0$"), r"$F=6x+4y$ (" + T("màxim", "máximo") + ")", g4,
           R(T(r"\text{12 de xocolata i 8 de nata: 104 €}", r"\text{12 de chocolate y 8 de nata: 104 €}")))),
 (2, T(r"Un taller fa taules i cadires. Cada taula necessita 2 hores de fusteria i 1 de pintura, i cada cadira, 1 hora de fusteria i 1 de pintura. Cada setmana hi ha 40 hores de fusteria i 30 de pintura. El benefici és de 50 € per taula i de 30 € per cadira. Quantes taules i cadires ha de fer per a guanyar el màxim?",
       r"Un taller hace mesas y sillas. Cada mesa necesita 2 horas de carpintería y 1 de pintura, y cada silla, 1 hora de carpintería y 1 de pintura. Cada semana hay 40 horas de carpintería y 30 de pintura. El beneficio es de 50 € por mesa y de 30 € por silla. ¿Cuántas mesas y sillas tiene que hacer para ganar el máximo?"),
     plsol(T(r"$x=$ taules, $y=$ cadires: $2x+y\le40,\ x+y\le30,\ x\ge0,\ y\ge0$", r"$x=$ mesas, $y=$ sillas: $2x+y\le40,\ x+y\le30,\ x\ge0,\ y\ge0$"), r"$F=50x+30y$ (" + T("màxim", "máximo") + ")", g5,
           T(r"El vèrtex $(10,20)$ és el tall de $2x+y=40$ i $x+y=30$. ", r"El vértice $(10,20)$ es el corte de $2x+y=40$ y $x+y=30$. ") + R(T(r"\text{10 taules i 20 cadires: 1\,100 €}", r"\text{10 mesas y 20 sillas: 1\,100 €}")))),
 (2, T(r"Un dietista combina dos aliments, A i B. Cada ració de A té 1 unitat de ferro i 3 de calci, i cada ració de B, 2 de ferro i 1 de calci. Cal prendre com a mínim 10 unitats de ferro i 15 de calci. Si una ració de A costa 2 € i una de B, 3 €, quantes racions de cada aliment fan la dieta més barata?",
       r"Un dietista combina dos alimentos, A y B. Cada ración de A tiene 1 unidad de hierro y 3 de calcio, y cada ración de B, 2 de hierro y 1 de calcio. Hay que tomar como mínimo 10 unidades de hierro y 15 de calcio. Si una ración de A cuesta 2 € y una de B, 3 €, ¿cuántas raciones de cada alimento hacen la dieta más barata?"),
     plsol(r"$x+2y\ge10,\ 3x+y\ge15,\ x\ge0,\ y\ge0$ (" + T("regió no fitada", "región no acotada") + ")", r"$C=2x+3y$ (" + T("mínim", "mínimo") + ")", g6,
           T(r"Com que $C$ creix cap on s'estén la regió, el mínim existeix: ", r"Como $C$ crece hacia donde se extiende la región, el mínimo existe: ") + R(T(r"\text{4 racions de A i 3 de B: 17 €}", r"\text{4 raciones de A y 3 de B: 17 €}")))),
 (3, T(r"Una persona vol invertir com a màxim 10\,000 € en dos fons. El fons A dona un 4\,\% anual i el B, un 6\,\%. En el fons B vol posar com a màxim 6\,000 € i en el A, com a mínim 2\,000 €. Com ha de repartir els diners per a obtindre el màxim benefici? (Treballa en milers d'euros.)",
       r"Una persona quiere invertir como máximo 10\,000 € en dos fondos. El fondo A da un 4\,\% anual y el B, un 6\,\%. En el fondo B quiere poner como máximo 6\,000 € y en el A, como mínimo 2\,000 €. ¿Cómo tiene que repartir el dinero para obtener el máximo beneficio? (Trabaja en miles de euros.)"),
     plsol(T(r"$x,\,y=$ milers d'euros en A i en B: $x+y\le10,\ y\le6,\ x\ge2,\ y\ge0$", r"$x,\,y=$ miles de euros en A y en B: $x+y\le10,\ y\le6,\ x\ge2,\ y\ge0$"), T(r"benefici en €: $F=40x+60y$", r"beneficio en €: $F=40x+60y$"), g7,
           R(T(r"\text{4\,000 € en A i 6\,000 € en B: 520 €}", r"\text{4\,000 € en A y 6\,000 € en B: 520 €}")))),
 (3, T(r"Un institut organitza una excursió per a 400 alumnes. L'empresa de transport té 8 autobusos de 40 places i 10 de 50 places, però només 9 conductors. Llogar un autobús menut costa 600 € i un de gran, 800 €. Quants autobusos de cada tipus cal llogar perquè l'excursió siga el més barata possible?",
       r"Un instituto organiza una excursión para 400 alumnos. La empresa de transporte tiene 8 autobuses de 40 plazas y 10 de 50 plazas, pero solo 9 conductores. Alquilar un autobús pequeño cuesta 600 € y uno grande, 800 €. ¿Cuántos autobuses de cada tipo hay que alquilar para que la excursión sea lo más barata posible?"),
     plsol(T(r"$x=$ menuts, $y=$ grans: $40x+50y\ge400,\ x+y\le9,\ x\le8,\ y\le10,\ x\ge0,\ y\ge0$", r"$x=$ pequeños, $y=$ grandes: $40x+50y\ge400,\ x+y\le9,\ x\le8,\ y\le10,\ x\ge0,\ y\ge0$"), r"$C=600x+800y$ (" + T("mínim", "mínimo") + ")", g8,
           T(r"Les restriccions $x\le8$ i $y\le10$ no hi influeixen. ", r"Las restricciones $x\le8$ e $y\le10$ no influyen. ") + R(T(r"\text{5 menuts i 4 grans: 6\,200 €}", r"\text{5 pequeños y 4 grandes: 6\,200 €}")))),
]))

bad = [mm for c_, mm in CHK if not c_]
assert not bad, bad[:5]
NEX = sum(len(s_[1]) for s_ in S)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("inequacions, primer grau, segon grau, sistemes d'inequacions, semiplans, regions del pla, programació lineal",
       "inecuaciones, primer grado, segundo grado, sistemas de inecuaciones, semiplanos, regiones del plano, programación lineal")
if not ES:
    pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: 'pdfkeywords={' + KW + '}', pre)
    pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les CCSS I}')
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{''' + T('Recorda', 'Recuerda') + r''':}\ #1\end{tcolorbox}}
'''

TIT = T("Inequacions i sistemes d'inequacions", "Inecuaciones y sistemas de inecuaciones")
def spc(t):
    # «, » separa elements; amb icomma la coma és un símbol normal i un «-» darrere seu seria una resta: el posem entre claus
    return re.sub(r'\$[^$]*\$', lambda mm: re.sub(r',((?:\\,|\\ |\\;|\s)+)-', r',\1{-}', mm.group(0).replace(', ', r',\, ')), t)
def build(sol):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 3: %s' % (t, TIT), capcalera='%s · Unidad 3: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-ccss')
        cap = assignatura('1batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 3' if sol else 'Ficha de ejercicios · Unidad 3') + '}'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                        "pdftitle={%s de la unitat 3: %s. 1r de Batxillerat CCSS}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 3: %s · 1r Batxillerat CCSS" % (t, TIT))
        assert 'Unitat 3' in p and 'unitat 3' in p
        cap = r'\capcalera{Matemàtiques CCSS}{1r Batx}{' + ('Solucions de la fitxa · Unitat 3' if sol else "Fitxa d'exercicis · Unitat 3") + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + cap + r'''{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. En els problemes de programació lineal es dona la regió factible amb els vèrtexs i, en verd, la recta de nivell que passa per l'òptim. Pots comprovar els resultats amb les eines interactives dels apunts de la unitat.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. En los problemas de programación lineal se da la región factible con los vértices y, en verde, la recta de nivel que pasa por el óptimo. Puedes comprobar los resultados con las herramientas interactivas de los apuntes de la unidad.")
             if sol else T(r"Resol els exercicis al quadern mostrant tots els passos. Escriu les solucions de les inequacions en forma d'interval i representa-les a la recta real; en les de dues incògnites, dibuixa la regió solució. En els problemes, defineix les incògnites i respon amb una frase.",
                           r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Escribe las soluciones de las inecuaciones en forma de intervalo y represéntalas en la recta real; en las de dos incógnitas, dibuja la región solución. En los problemas, define las incógnitas y responde con una frase."))
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + intro + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, spc(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = ('t3-fitxa-solucions' if sol else 't3-fitxa-exercicis') + ('-es' if ES else '') + '.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(NEX, T('exercicis;', 'ejercicios;'), len(CHK), T('comprovacions', 'comprobaciones'))
