# Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 8: Representació gràfica
# de funcions) a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les
# estrelles no es mostren. Les seccions segueixen els apunts interactius (materials/2batx-mii/t8-representacio-funcions.html)
# i l'estructura de la unitat 7 de CCSS, amb més dificultat i amb funcions radicals, trigonomètriques i a trossos.
# Els exercicis marcats amb \pau{...} són de la PAU de València i d'altres comunitats, traduïts al valencià i presos del
# recull «Ejercicios de análisis en pruebas de acceso a la universidad de toda España» (curs 2026/27) de Juan Antonio
# Martínez García (www.ebaumatematicas.com). Les gràfiques de les solucions es calculen ací mateix i es dibuixen amb TikZ com
# a poligonals (graf), com a la unitat 7 de MII (d'on s'ha copiat el codi de les comprovacions i de les gràfiques). Abans
# d'escriure els fitxers, sympy comprova tots els dominis, límits, asímptotes, extrems, punts d'inflexió, períodes i
# paràmetres de les solucions.
# Ús: python3 genera.py && pdflatex t8-fitxa-exercicis.tex (dues vegades) && pdflatex t8-fitxa-solucions.tex (dues vegades)
import os, re, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    if any('pau{' in i or len(i) > 110 for i in items): n = 1  # les etiquetes PAU no caben en dues columnes
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def pw(*rows, name='f(x)'):
    return name + r'=\begin{cases}' + r'\\[3pt]'.join(r'%s&\text{si }%s' % r for r in rows) + r'\end{cases}'
def fx(s, n='f'): return '$' + n + '(x)=' + s + '$'

# ---------- comprovacions amb sympy ----------
x, y, h, t = sp.symbols('x y h t', real=True)
a_, b_, c_, d_, k_, m_ = sp.symbols('a b c d k m', real=True)
E, ln, sq, sin, cos, tan, atan, pi, exp = sp.E, sp.log, sp.sqrt, sp.sin, sp.cos, sp.tan, sp.atan, sp.pi, sp.exp
R = sp.Rational
NCHK = [0]
def N(e): return complex(sp.N(e, 30))
def eq(a, b, tol=1e-9):
    va, vb = N(sp.sympify(a)), N(sp.sympify(b))
    assert abs(va - vb) < tol * (1 + abs(va)), (a, b, va, vb)
    NCHK[0] += 1
def ok(c):
    assert c; NCHK[0] += 1
def L(e, a, val, d='+-'):
    r = sp.limit(e, x, a, d) if d != '+-' else sp.limit(e, x, a)
    if val in (sp.oo, -sp.oo): ok(r == val)
    else: eq(r, val)
def tang(f, a, mm, n0):
    eq(sp.diff(f, x).subs(x, a), mm); eq(f.subs(x, a) - mm * a, n0)
def crit(f, xs, lo=-50, hi=50):
    """els zeros reals de f' (en [lo, hi] i dins del domini) són xs"""
    d = sp.diff(f, x)
    sols = sorted(set(round(float(s), 9) for s in sp.solveset(sp.simplify(d), x, sp.Interval(lo, hi)) if s.is_real and abs(N(f.subs(x, s))) < 1e12))
    ok(len(sols) == len(xs) and all(abs(p - float(q)) < 1e-7 for p, q in zip(sols, sorted(float(v) for v in xs))))
def ext(f, x0, kind, val=None):
    """extrem relatiu en x0 (comprovat pel canvi de signe de f')"""
    d = sp.diff(f, x); e = 1e-4
    l, r = N(d.subs(x, x0 - e)).real, N(d.subs(x, x0 + e)).real
    ok((l > 0 > r) if kind == 'max' else (l < 0 < r))
    if val is not None: eq(f.subs(x, x0), val)
def infl(f, x0, val=None):
    d2 = sp.diff(f, x, 2); e = 1e-4
    ok(N(d2.subs(x, x0 - e)).real * N(d2.subs(x, x0 + e)).real < 0)
    if val is not None: eq(f.subs(x, x0), val)
def sgn_on(g, a, b, s):
    """g té signe s en uns quants punts de (a, b)"""
    for k in range(1, 8):
        p = a + (b - a) * k / 8
        ok(N(g.subs(x, p)).real * s > 0)

# ---------- gràfiques (com a la unitat 7 de CCSS) ----------
def nice(r):
    for s in (0.5, 1, 2, 5, 10, 20, 50, 100):
        if r / s <= 8: return s
    return 200
def fnum(v): return ('%g' % v).replace('.', '{,}')
def graf(curves, box, va=(), ha=(), oa=(), pts=(), mx=(), mn=(), ip=(), opn=(), w=6.0, h=4.4, xt=None):
    """curves: llista de funcions o de (f, a, b); box: (x0, x1, y0, y1). xt: marques de l'eix x [(valor, text)]."""
    x0, x1, y0, y1 = box
    sx, sy = w / (x1 - x0), h / (y1 - y0)
    stx, sty = nice(x1 - x0), nice(y1 - y0)
    o = [r'\begin{tikzpicture}[x=%.4fcm,y=%.4fcm,baseline=(current bounding box.center)]' % (sx, sy)]
    o.append(r'\draw[muted!25,very thin,xstep=%g,ystep=%g] (%g,%g) grid (%g,%g);' % (stx, sty, x0, y0, x1, y1))
    if y0 <= 0 <= y1: o.append(r'\draw[-latex,muted] (%g,0)--(%g,0);' % (x0, x1 + 0.35 / sx))
    if x0 <= 0 <= x1: o.append(r'\draw[-latex,muted] (0,%g)--(0,%g);' % (y0, y1 + 0.35 / sy))
    ay = 0 if y0 <= 0 <= y1 else y0
    ax = 0 if x0 <= 0 <= x1 else x0
    if xt is None:
        k = math.ceil(x0 / stx)
        while k * stx <= x1 + 1e-9:
            tt = k * stx
            if abs(tt) > 1e-9 and tt < x1 - 1e-9: o.append(r'\node[below,font=\tiny,text=muted,inner sep=1.5pt] at (%g,%g) {$%s$};' % (tt, ay, fnum(tt)))
            k += 1
    else:
        for v, s in xt: o.append(r'\node[below,font=\tiny,text=muted,inner sep=1.5pt] at (%g,%g) {$%s$};' % (v, ay, s))
    k = math.ceil(y0 / sty)
    while k * sty <= y1 + 1e-9:
        tt = k * sty
        if abs(tt) > 1e-9 and tt < y1 - 1e-9: o.append(r'\node[left,font=\tiny,text=muted,inner sep=1.5pt] at (%g,%g) {$%s$};' % (ax, tt, fnum(tt)))
        k += 1
    o.append(r'\begin{scope}\clip (%g,%g) rectangle (%g,%g);' % (x0, y0, x1, y1))
    for a in va: o.append(r'\draw[teal,dashed,thick] (%g,%g)--(%g,%g);' % (a, y0, a, y1))
    for b in ha: o.append(r'\draw[teal,dashed,thick] (%g,%g)--(%g,%g);' % (x0, b, x1, b))
    for m, n in oa: o.append(r'\draw[teal,dashed,thick] (%g,%g)--(%g,%g);' % (x0, m * x0 + n, x1, m * x1 + n))
    lim, span = 3 * (y1 - y0), y1 - y0
    for c in curves:
        f, a, b = (c, x0, x1) if callable(c) else c
        a, b = max(a, x0), min(b, x1)
        cuts = sorted([a, b] + [v for v in va if a < v < b])
        for p, q in zip(cuts, cuts[1:]):
            NN, seg, prev = 360, [], None
            for i in range(NN + 1):
                xx = p + (q - p) * i / NN
                if i == 0: xx += (q - p) * 1e-6
                if i == NN: xx -= (q - p) * 1e-6
                try: yy = f(xx)
                except (ValueError, ZeroDivisionError, OverflowError): yy = None
                if isinstance(yy, complex): yy = None
                if yy is None or not math.isfinite(yy) or yy < y0 - lim or yy > y1 + lim or (prev is not None and abs(yy - prev) > 1.5 * span):
                    if len(seg) > 1: o.append(r'\draw[accent,line width=1.4pt,line join=round] ' + '--'.join(seg) + ';')
                    seg, prev = [], None
                    if yy is None or not math.isfinite(yy) or yy < y0 - lim or yy > y1 + lim: continue
                seg.append('(%.3f,%.3f)' % (xx, yy)); prev = yy
            if len(seg) > 1: o.append(r'\draw[accent,line width=1.4pt,line join=round] ' + '--'.join(seg) + ';')
    o.append(r'\end{scope}')
    for X_, Y_ in pts: o.append(r'\fill[navy] (%g,%g) circle (2pt);' % (X_, Y_))
    for X_, Y_ in opn: o.append(r'\filldraw[fill=white,draw=accent,line width=1pt] (%g,%g) circle (2.2pt);' % (X_, Y_))
    for X_, Y_ in mx: o.append(r'\fill[green!50!black] (%g,%g) circle (2.6pt);' % (X_, Y_))
    for X_, Y_ in mn: o.append(r'\fill[red!70!black] (%g,%g) circle (2.6pt);' % (X_, Y_))
    for X_, Y_ in ip: o.append(r'\fill[violet] (%g,%g) circle (2.4pt);' % (X_, Y_))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'
me, ms, mln, mc, mt = math.exp, math.sin, math.log, math.cos, math.tan
r2, r3, PI = math.sqrt(2), math.sqrt(3), math.pi
def mlog(v): return mln(v) if v > 0 else float('nan')
def msq(v): return math.sqrt(v) if v >= 0 else float('nan')

S = []  # [(títol, [(estrelles, enunciat, solució)])]
def sec(tt, *exs): S.append((tt, list(exs)))

from sympy.calculus.util import continuous_domain
I_, U_ = sp.Interval, sp.Union
def dom(f, D, univ=sp.S.Reals):
    ok(sp.simplify(continuous_domain(f, x, univ).symmetric_difference(D)) == sp.S.EmptySet)
def lim_(f, a, d='+-'): return sp.limit(f, x, a, d) if d != '+-' else sp.limit(f, x, a)
def asy_h(f, val, side=sp.oo): L(f, side, val)
def obl(f, m, n, side=sp.oo):
    eq(sp.limit(f / x, x, side), m); eq(sp.limit(f - m * x, x, side), n)
def parity(f, kind):
    P = [(N(f.subs(x, p)), N(f.subs(x, -p))) for p in (0.31, 0.57, 0.83, 1.7, 2.9) if abs(N(f.subs(x, p))) < 1e12 and abs(N(f.subs(x, p)).imag) < 1e-12]
    ev, od = all(abs(u - v) < 1e-9 for u, v in P), all(abs(u + v) < 1e-9 for u, v in P)
    ok(len(P) >= 2 and (ev if kind == 'even' else od if kind == 'odd' else not ev and not od))
def period(f, T):
    for p in (0.31, 1.27, 2.9): eq(f.subs(x, p + T), f.subs(x, p))
    for k in range(2, 7):
        Tk = sp.Rational(1, k) * T
        ok(abs(N(f.subs(x, 0.7 + Tk) - f.subs(x, 0.7))) > 1e-6 or abs(N(f.subs(x, 1.9 + Tk) - f.subs(x, 1.9))) > 1e-6)
PIX = [(PI / 2, r'\frac\pi2'), (PI, r'\pi'), (3 * PI / 2, r'\frac{3\pi}2'), (2 * PI, r'2\pi')]
REP = recorda(r"Domini, simetria, talls, asímptotes (i posició), monotonia i extrems, curvatura i inflexió; després situem tota la informació i dibuixem.")
def rep(fn): return r"Fes l'estudi complet i representa " + fn + "."

# =====================================================================
# 1. Domini
dom((x + 3) / (x**2 - 5 * x + 6), U_(I_.open(-sp.oo, 2), I_.open(2, 3), I_.open(3, sp.oo)))
dom(sq(9 - x**2), I_(-3, 3)); dom(sq((x - 1) / (x + 2)), U_(I_.open(-sp.oo, -2), I_(1, sp.oo)))
dom(ln(4 - x**2), I_.open(-2, 2)); dom(1 / sq(x**2 - 2 * x - 3), U_(I_.open(-sp.oo, -1), I_.open(3, sp.oo)))
dom(sp.exp(x) / (sp.exp(2 * x) - 1), U_(I_.open(-sp.oo, 0), I_.open(0, sp.oo))); dom(ln(ln(x)), I_.open(1, sp.oo))
dom(sq((x**2 - 4) / (x**2 - 9)), U_(I_.open(-sp.oo, -3), I_(-2, 2), I_.open(3, sp.oo)))
dom(sp.log(x**2 - x, 2) - sq(3 - x), U_(I_.open(-sp.oo, 0), I_.Lopen(1, 3)))
dom(ln(x + 2) / (3 * x + 4), U_(I_.open(-2, -R(4, 3)), I_.open(-R(4, 3), sp.oo)))
dom((2 * x - 1) / sq(x**2 - x - 2), U_(I_.open(-sp.oo, -1), I_.open(2, sp.oo)))
ok(sp.solveset(sin(x) >= 0, x, I_(0, 2 * pi)) == I_(0, pi)); ok(U_(sp.solveset(cos(x) > 0, x, I_(0, 2 * pi)), sp.FiniteSet(2 * pi)) == U_(I_.Ropen(0, pi / 2), I_.Lopen(3 * pi / 2, 2 * pi)))
dom(sp.asin(x / 2), I_(-2, 2))
sec("Domini d'una funció",
 (1, r"Calcula el domini de les funcions següents:" + tasks(2, [r"$f(x)=\dfrac{x+3}{x^2-5x+6}$", r"$f(x)=\sqrt{9-x^2}$", r"$f(x)=\sqrt{\dfrac{x-1}{x+2}}$", r"$f(x)=\ln\left(4-x^2\right)$",
                                                               r"$f(x)=\dfrac{1}{\sqrt{x^2-2x-3}}$", r"$f(x)=\sqrt[3]{\dfrac{x}{x^2-1}}$", r"$f(x)=\dfrac{e^x}{e^{2x}-1}$", r"$f(x)=\ln(\ln x)$"])
     + recorda(r"Denominadors $\neq0$; radicands d'índex parell $\geq0$ (i $>0$ si l'arrel és al denominador); arguments dels logaritmes $>0$. El domini és la intersecció de totes les condicions."),
     tasks(2, [r"$\res{\mathbb R-\{2,3\}}$", r"$\res{[-3,3]}$", r"$\res{(-\infty,-2)\cup[1,+\infty)}$", r"$\res{(-2,2)}$", r"$(x+1)(x-3)>0$: $\res{(-\infty,-1)\cup(3,+\infty)}$",
               r"$\res{\mathbb R-\{-1,1\}}$ (índex senar)", r"$e^{2x}\neq1$: $\res{\mathbb R-\{0\}}$", r"$\ln x>0$: $\res{(1,+\infty)}$"])),
 (2, r"Domini de:" + tasks(2, [r"$f(x)=\tan3x$", r"$f(x)=\dfrac{1}{1-\cos x}$", r"$f(x)=\arcsin\dfrac x2$", r"$f(x)=\sqrt{\sin x}$, en $[0,2\pi]$", r"$f(x)=\ln(\cos x)$, en $[0,2\pi]$"]),
     tasks(2, [r"$3x\neq\frac\pi2+k\pi$: $\res{\mathbb R-\left\{\frac\pi6+\frac{k\pi}3\right\}}$", r"$\cos x\neq1$: $\res{\mathbb R-\{2k\pi\}}$", r"$-1\leq\frac x2\leq1$: $\res{[-2,2]}$", r"$\sin x\geq0$: $\res{[0,\pi]}$", r"$\cos x>0$: $\res{\left[0,\frac\pi2\right)\cup\left(\frac{3\pi}2,2\pi\right]}$"])),
 (2, r"Domini de:" + tasks(1, [r"\pau{Aragó, ordinària 2023} $f(x)=\dfrac{2x-1}{\sqrt{x^2-x-2}}$", r"\pau{Canàries, ordinària 2024} $f(x)=\dfrac{\ln(x+2)}{3x+4}$"]),
     tasks(1, [r"$(x+1)(x-2)>0$: $\res{(-\infty,-1)\cup(2,+\infty)}$", r"$x>-2$ i $x\neq-\frac43$: $\res{\left(-2,-\frac43\right)\cup\left(-\frac43,+\infty\right)}$"])),
 (3, r"Domini de:" + tasks(1, [r"$f(x)=\sqrt{\dfrac{x^2-4}{x^2-9}}$", r"$f(x)=\log_2\left(x^2-x\right)-\sqrt{3-x}$"]),
     tasks(1, [r"Signes de $\frac{(x+2)(x-2)}{(x+3)(x-3)}$ amb els punts $\pm2$ (inclosos) i $\pm3$ (exclosos): $\res{(-\infty,-3)\cup[-2,2]\cup(3,+\infty)}$",
               r"$x(x-1)>0$ i $x\leq3$: $\res{(-\infty,0)\cup(1,3]}$"])),
)

# =====================================================================
# 2. Talls amb els eixos i signe
g_ = x**3 - x**2 - 6 * x; ok(sorted(sp.solve(g_, x)) == [-2, 0, 3]); sgn_on(g_, -3, -2, -1); sgn_on(g_, -2, 0, 1); sgn_on(g_, 0, 3, -1)
g_ = (x**2 - 4 * x + 3) / (x + 1); sgn_on(g_, -5, -1, -1); sgn_on(g_, -1, 1, 1); sgn_on(g_, 1, 3, -1); eq(g_.subs(x, 0), 3)
g_ = (x**2 - 1) * sp.exp(x); sgn_on(g_, -1, 1, -1); eq(g_.subs(x, 0), -1)
g_ = ln(x**2 - 8); ok(sorted(sp.solve(g_, x)) == [-3, 3]); sgn_on(g_, 2 * sq(2), 3, -1)
g_ = x**3 + x - 3; ok(N(g_.subs(x, 1)).real < 0 < N(g_.subs(x, 2)).real); ok(sp.solveset(sp.diff(g_, x) <= 0, x, sp.S.Reals) == sp.S.EmptySet)
eq(g_.subs(x, R(3, 2)), R(15, 8))
g_ = (x - 2)**2 * (x + 1) / x**3; sgn_on(g_, -3, -1, 1); sgn_on(g_, -1, 0, -1); sgn_on(g_, 0, 2, 1); sgn_on(g_, 2, 5, 1)
g_ = x - 2 * sin(x); ok(N(g_.subs(x, 1.5)).real < 0 < N(g_.subs(x, 2.5)).real)
sec("Talls amb els eixos i signe de la funció",
 (1, r"Troba els punts de tall amb els eixos i estudia el signe de:" + tasks(2, [r"$f(x)=x^3-x^2-6x$", r"$f(x)=\dfrac{x^2-4x+3}{x+1}$", r"$f(x)=\left(x^2-1\right)e^x$", r"$f(x)=\ln\left(x^2-8\right)$"])
     + recorda(r"Els zeros de $f$ i els punts on no és contínua separen intervals de signe constant: n'hi ha prou amb un valor de prova en cada un."),
     tasks(1, [r"$x(x+2)(x-3)$: $(0,0)$, $(-2,0)$, $(3,0)$; \res{f<0\text{ en }(-\infty,-2)\cup(0,3)}, \res{f>0\text{ en }(-2,0)\cup(3,+\infty)}",
               r"$(0,3)$, $(1,0)$, $(3,0)$; \res{f<0\text{ en }(-\infty,-1)\cup(1,3)}, \res{f>0\text{ en }(-1,1)\cup(3,+\infty)}",
               r"$(0,-1)$, $(\pm1,0)$; \res{f<0\text{ en }(-1,1)}, positiva fora ($e^x>0$)",
               r"Domini $|x|>2\sqrt2$, no talla OY; $x^2-8=1\Rightarrow(\pm3,0)$; \res{f<0\text{ en }\left(-3,-2\sqrt2\right)\cup\left(2\sqrt2,3\right)}, positiva si $|x|>3$"])),
 (2, r"\pau{Extremadura, juny 2018} Demostra que $f(x)=x^3+x-3$ talla l'eix d'abscisses en un únic punt, que és positiu, i troba un interval de longitud $\frac12$ que el continga.",
     r"$f(1)=-1<0$, $f(2)=7>0$: per Bolzano hi ha un zero en $(1,2)$. $f'(x)=3x^2+1>0$: és estrictament creixent i el zero és \rest{únic}. Com que $f\left(\frac32\right)=\frac{15}8>0$, és en $\res{\left(1,\tfrac32\right)}$."),
 (2, r"Estudia el signe de $f(x)=\dfrac{(x-2)^2(x+1)}{x^3}$. On talla o toca l'eix OX?",
     r"Punts $-1$, $0$ i $2$ (doble). \res{f>0\text{ en }(-\infty,-1)\cup(0,2)\cup(2,+\infty)}, \res{f<0\text{ en }(-1,0)}. Talla OX en $(-1,0)$ i el \rest{toca} en $(2,0)$ sense canviar de signe."),
 (3, r"Quantes solucions té l'equació $x=2\sin x$? Localitza la positiva entre dos decimals consecutius.",
     r"$f(x)=x-2\sin x$ és senar i $f(0)=0$. Si $|x|>2$, $|x|>2\geq|2\sin x|$: no hi ha zeros. En $(0,2]$: $f'=1-2\cos x$: decreix en $\left(0,\frac\pi3\right)$ (i hi és negativa) i després creix, així que té un únic zero positiu; $f(1{,}8)\approx-0{,}15<0<f(1{,}9)\approx0{,}01$. Hi ha \res{3\text{ solucions}}: $0$ i $\pm x_0$, amb $\res{x_0\in(1{,}8;\,1{,}9)}$."),
)
eq((x - 2 * sin(x)).subs(x, 1.8), 1.8 - 2 * math.sin(1.8)); ok(1.8 - 2 * math.sin(1.8) < 0 < 1.9 - 2 * math.sin(1.9))

# =====================================================================
# 3. Simetries i periodicitat
parity(x**4 - 3 * x**2 + 1, 'even'); parity(x / (x**2 - 4), 'odd'); parity(sp.exp(-x**2) * cos(x), 'even'); parity(x**3 + 1, 'none')
parity(ln((1 + x) / (1 - x)), 'odd'); parity(sin(x) * cos(x) / x, 'even')
period(sin(3 * x), 2 * pi / 3); period(cos(x / 2), 4 * pi); period(sin(x) + sin(2 * x), 2 * pi); period(sin(2 * x)**2, pi / 2); period(tan(pi * x / 4), 4); period(sp.Abs(cos(x)), pi)
f_ = (x**2 + 1) / (x - 1); h_ = sp.symbols('h'); ok(sp.simplify(f_.subs(x, 1 + h_) - 2 + (f_.subs(x, 1 - h_) - 2)) == 0)
f_ = ln(x + sq(x**2 + 1)); eq(f_.subs(x, -1.3) + f_.subs(x, 1.3), 0); eq(f_.subs(x, -0.4) + f_.subs(x, 0.4), 0)
f_ = 1 / (x**2 - 6 * x + 10); ok(sp.simplify(f_.subs(x, 3 + h_) - f_.subs(x, 3 - h_)) == 0)
sec("Simetries i periodicitat",
 (1, r"Estudia la simetria de les funcions següents:" + tasks(2, [r"$f(x)=x^4-3x^2+1$", r"$f(x)=\dfrac{x}{x^2-4}$", r"$f(x)=e^{-x^2}\cos x$", r"$f(x)=x^3+1$", r"$f(x)=\ln\dfrac{1+x}{1-x}$", r"$f(x)=\dfrac{\sin x\cos x}{x}$"])
     + recorda(r"Parella: $f(-x)=f(x)$ (simetria respecte de OY). Senar: $f(-x)=-f(x)$ (respecte de l'origen). El domini ha de ser simètric."),
     tasks(2, [r"\rest{parella}", r"\rest{senar}", r"\rest{parella}", r"\rest{cap} ($f(-x)=1-x^3$)", r"\rest{senar}: $\ln\frac{1-x}{1+x}=-\ln\frac{1+x}{1-x}$", r"\rest{parella} (quocient de dues senars)"])),
 (1, r"Calcula el període de:" + tasks(3, [r"$\sin3x$", r"$\cos\dfrac x2$", r"$\sin x+\sin2x$", r"$\sin^2(2x)$", r"$\tan\dfrac{\pi x}{4}$", r"$|\cos x|$"]),
     tasks(3, [r"$\res{\frac{2\pi}3}$", r"$\res{4\pi}$", r"$\res{2\pi}$", r"$\res{\frac\pi2}$", r"$\res{4}$", r"$\res{\pi}$"])),
 (2, r"Comprova que la gràfica de $f(x)=\dfrac{x^2+1}{x-1}$ és simètrica respecte del punt en què es tallen les seues asímptotes, i que la de $g(x)=\dfrac{1}{x^2-6x+10}$ és simètrica respecte d'una recta vertical.",
     r"$f(x)=x+1+\frac{2}{x-1}$: AV $x=1$ i AO $y=x+1$, que es tallen en $(1,2)$; $f(1+h)-2=h+\frac2h$ és senar: simètrica respecte de \res{(1,2)}. \ $g(x)=\frac{1}{(x-3)^2+1}$: $g(3+h)=g(3-h)$, simètrica respecte de \res{x=3}."),
 (3, r"Demostra que $f(x)=\ln\left(x+\sqrt{x^2+1}\right)$ és senar.",
     r"$f(-x)=\ln\left(\sqrt{x^2+1}-x\right)=\ln\dfrac{\left(\sqrt{x^2+1}-x\right)\left(\sqrt{x^2+1}+x\right)}{\sqrt{x^2+1}+x}=\ln\dfrac{1}{\sqrt{x^2+1}+x}=-f(x)$: \rest{és senar}."),
)

# =====================================================================
# 4. Asímptotes verticals i horitzontals
f_ = (2 * x**2 - 3) / (x**2 - 1); L(f_, 1, -sp.oo, '+'); L(f_, 1, sp.oo, '-'); asy_h(f_, 2); asy_h(f_, 2, -sp.oo)
f_ = (x + 2) / (x**2 - 4); L(f_, -2, -R(1, 4)); L(f_, 2, sp.oo, '+'); asy_h(f_, 0)
f_ = 3 * sp.exp(x) / (sp.exp(x) + 1); asy_h(f_, 3); asy_h(f_, 0, -sp.oo)
f_ = sq(x**2 + 1) / x; asy_h(f_, 1); asy_h(f_, -1, -sp.oo); L(f_, 0, sp.oo, '+'); L(f_, 0, -sp.oo, '-')
f_ = ln(x) / (x - 1); L(f_, 1, 1); L(f_, 0, sp.oo, '+'); asy_h(f_, 0)
f_ = (x**2 - 2 * x - 3) / (x**2 - 1); L(f_, -1, 2); L(f_, 1, sp.oo, '-'); asy_h(f_, 1); ok(sp.simplify(sp.diff(f_, x) - 2 / (x - 1)**2) == 0)
f_ = x**2 / (x**2 - 4); asy_h(f_, 1); crit(f_, [0]); ext(f_, 0, 'max', 0)
f_ = x * sp.exp(-a_ * x); ok(sp.solve(sp.diff(f_, x).subs(x, 1), a_) == [1]); ext(x * sp.exp(-x), 1, 'max')
f_ = (x + 4) / (x**2 - 7 * x - 8); crit(f_, [-10, 2]); ext(f_, -10, 'min'); ext(f_, 2, 'max'); asy_h(f_, 0)
f_ = x / (x**2 - 3 * x - 4); ok(sp.simplify(sp.diff(f_, x) + (x**2 + 4) / (x**2 - 3 * x - 4)**2) == 0); tang(f_, 0, -R(1, 4), 0)
sec("Asímptotes verticals i horitzontals",
 (1, r"Calcula les asímptotes verticals i horitzontals (amb els límits laterals):" + tasks(2, [r"$f(x)=\dfrac{2x^2-3}{x^2-1}$", r"$f(x)=\dfrac{x+2}{x^2-4}$", r"$f(x)=\dfrac{3e^x}{e^x+1}$", r"$f(x)=\dfrac{\sqrt{x^2+1}}{x}$", r"$f(x)=\dfrac{\ln x}{x-1}$"])
     + recorda(r"AV $x=a$ si algun límit lateral en $a$ és infinit. AH $y=k$ si $\displaystyle\lim_{x\to\pm\infty}f(x)=k$: estudia cada costat per separat. Compte: $\sqrt{x^2}=|x|$."),
     tasks(1, [r"\res{x=\pm1} ($\lim_{x\to1^\pm}f=\mp\infty$…), \res{y=2}",
               r"$f=\frac{1}{x-2}$ si $x\neq-2$: \res{x=2} (en $x=-2$ hi ha un forat, $\lim=-\frac14$), \res{y=0}",
               r"Sense AV; \res{y=3} en $+\infty$ i \res{y=0} en $-\infty$",
               r"\res{x=0} ($\pm\infty$ pels costats); \res{y=1} en $+\infty$ i \res{y=-1} en $-\infty$",
               r"Domini $(0,1)\cup(1,+\infty)$; $\lim_{x\to1}f=1$ (no és AV); \res{x=0} ($\to+\infty$); \res{y=0} en $+\infty$"])),
 (2, r"\pau{Andalusia, ordinària 2020} Estudia les asímptotes i la monotonia de $f(x)=\dfrac{x^2-2x-3}{x^2-1}$.",
     r"$f=\frac{(x-3)(x+1)}{(x-1)(x+1)}=\frac{x-3}{x-1}$ si $x\neq-1$: AV \res{x=1} (en $x=-1$, forat); AH \res{y=1}. $f'=\frac{2}{(x-1)^2}>0$: \rest{sempre creixent}."),
 (2, r"\pau{País Basc, juny 2018} Asímptotes, monotonia i extrems de $f(x)=\dfrac{x^2}{x^2-4}$.",
     r"AV \res{x=\pm2}, AH \res{y=1}. $f'=\frac{-8x}{(x^2-4)^2}$: creix en $(-\infty,-2)\cup(-2,0)$, decreix en $(0,2)\cup(2,+\infty)$; \res{\text{màxim }(0,0)}."),
 (2, r"\pau{Cantàbria, setembre 2019} Domini, asímptotes, monotonia i extrems de $f(x)=\dfrac{x+4}{x^2-7x-8}$.",
     r"Domini $\mathbb R-\{-1,8\}$; AV \res{x=-1,\ x=8}, AH \res{y=0}. $f'=\frac{-(x+10)(x-2)}{(x^2-7x-8)^2}$: decreix en $(-\infty,-10)\cup(2,8)\cup(8,+\infty)$, creix en $(-10,-1)\cup(-1,2)$; \res{\text{mín. en }x=-10}, \res{\text{màx. en }x=2}."),
 (2, r"\pau{País Basc, extraordinària 2025} Asímptotes i monotonia de $f(x)=\dfrac{x}{x^2-3x-4}$, i recta tangent en $x=0$.",
     r"AV \res{x=-1,\ x=4}, AH \res{y=0}. $f'=\frac{-(x^2+4)}{(x^2-3x-4)^2}<0$: decreixent en tot el domini. Tangent: \res{y=-\frac x4}."),
 (3, r"\pau{La Rioja, juny 2018} Sigui $f(x)=x\,e^{-ax}$. Estudia'n les asímptotes segons els valors de $a$ i troba $a$ perquè tinga un extrem relatiu en $x=1$. És màxim o mínim?",
     r"Sense AV ni AO. Si $a>0$: AH $y=0$ només quan $x\to+\infty$; si $a<0$: AH $y=0$ només quan $x\to-\infty$; si $a=0$ ($f=x$), cap. $f'=(1-ax)e^{-ax}$, $f'(1)=0\Rightarrow\res{a=1}$, i és un \rest{màxim} ($f'$ passa de $+$ a $-$)."),
)

# =====================================================================
# 5. Asímptotes obliqües i branques parabòliques
f_ = x**2 / (x - 1); obl(f_, 1, 1); obl(f_, 1, 1, -sp.oo); crit(f_, [0, 2]); ext(f_, 0, 'max', 0); ext(f_, 2, 'min', 4)
f_ = 1 / x + a_ * x + b_; s_ = sp.solve([sp.diff(f_, x).subs(x, R(1, 2)), f_.subs(x, R(1, 2)) - 6], [a_, b_]); ok(s_ == {a_: 4, b_: 2}); obl(f_.subs(s_), 4, 2)
f_ = (x**3 - 8) / (x**2 - 4); L(f_, 2, 3); L(f_, -2, -sp.oo, '-'); obl(f_, 1, 0); tang(f_, 1, R(5, 9), R(16, 9))
ok(sp.solve((4 * a_ - 2) / 7 - 2, a_) == [4])
f_ = (-x**2 - 2) / (-3 - x); obl(f_, 1, -3); L(f_, -3, sp.oo, '+')
f_ = sq(9 * x**2 + a_ * x + 1) - (3 * x - 1); ok(sp.solve(sp.limit(f_, x, sp.oo) - 2, a_) == [6])
f_ = 2 * x + 1 / x**2; obl(f_, 2, 0); obl(f_, 2, 0, -sp.oo); crit(f_, [1]); ext(f_, 1, 'min', 3)
eq(sp.limit(sq(x) / x, x, sp.oo), 0); eq(sp.limit((x + sq(x)) / x, x, sp.oo), 1); L(x + sq(x) - x, sp.oo, sp.oo); L(x * ln(x) / x, sp.oo, sp.oo)
f_ = sq(x**2 + x + 1) - x; asy_h(f_, R(1, 2)); obl(f_, -2, -R(1, 2), -sp.oo)
f_ = (2 * x**2 + b_ * x) / (x + 1); ok(sp.solve(sp.limit(f_ - 2 * x, x, sp.oo) + 1, b_) == [1])
sec("Asímptotes obliqües i branques parabòliques",
 (1, r"Calcula totes les asímptotes de:" + tasks(1, [r"\pau{Andalusia, juny 2017} $f(x)=\dfrac{x^2}{x-1}$ (troba'n també els extrems).", r"\pau{Astúries, extraordinària 2020} $f(x)=\dfrac{2x^3+1}{x^2}$ (i els extrems)."])
     + recorda(r"$m=\displaystyle\lim_{x\to\pm\infty}\frac{f(x)}{x}$ (finit i $\neq0$), $n=\displaystyle\lim_{x\to\pm\infty}\big(f(x)-mx\big)$. En les racionals, l'AO és el quocient de la divisió."),
     tasks(1, [r"$f=x+1+\frac{1}{x-1}$: AV \res{x=1}, AO \res{y=x+1}. $f'=\frac{x(x-2)}{(x-1)^2}$: \res{\text{màx. }(0,0)}, \res{\text{mín. }(2,4)}",
               r"$f=2x+\frac{1}{x^2}$: AV \res{x=0} ($\to+\infty$ pels dos costats), AO \res{y=2x}. $f'=2-\frac{2}{x^3}$: \res{\text{mín. }(1,3)}; creix en $(-\infty,0)\cup(1,+\infty)$"])),
 (2, r"\pau{Cantàbria, ordinària 2025} Sigui $f(x)=\dfrac{x^3-8}{x^2-4}$ si $x\neq2$ i $f(2)=e^k$." + tasks(1, [r"Troba $k$ perquè sigui contínua en $x=2$.", r"Calcula'n les asímptotes.", r"Escriu la recta tangent en $x=1$."]),
     tasks(1, [r"$f=\frac{x^2+2x+4}{x+2}\to3$: $e^k=3\Rightarrow\res{k=\ln3}$", r"AV \res{x=-2}; sense AH; $f=x+\frac{4}{x+2}$: AO \res{y=x}", r"$f(1)=\frac73$, $f'(1)=1-\frac49=\frac59$: \res{y=\frac59x+\frac{16}9}"])),
 (2, r"\pau{Canàries, ordinària 2021} Sigui $f(x)=\dfrac{ax^2-2}{b-x}$." + tasks(1, [r"Troba $a$ i $b$ perquè $f(-2)=2$ i $f$ siga contínua en $\mathbb R-\{5\}$.", r"Per a $a=-1$, $b=-3$, calcula les asímptotes."]),
     tasks(1, [r"$b=5$ i $\frac{4a-2}{7}=2\Rightarrow\res{a=4,\ b=5}$", r"$f=\frac{x^2+2}{x+3}=x-3+\frac{11}{x+3}$: AV \res{x=-3}, AO \res{y=x-3}"])),
 (2, r"\pau{Castella i Lleó, juliol 2018} Troba $a$ i $b$ perquè $f(x)=\dfrac1x+ax+b$ tinga un mínim relatiu en $\left(\frac12,6\right)$ i, amb aquests valors, troba'n les asímptotes.",
     r"$f'\left(\frac12\right)=-4+a=0\Rightarrow\res{a=4}$; $f\left(\frac12\right)=2+2+b=6\Rightarrow\res{b=2}$. AV \res{x=0}, AO \res{y=4x+2}."),
 (3, r"\pau{La Rioja, juliol 2018} Troba $a$ perquè $\displaystyle\lim_{x\to+\infty}\left(\sqrt{9x^2+ax+1}-(3x-1)\right)=2$. Quina és, aleshores, l'asímptota obliqua de $y=\sqrt{9x^2+ax+1}$ en $+\infty$?",
     r"$\lim\frac{ax+1}{\sqrt{9x^2+ax+1}+3x}+1=\frac a6+1=2\Rightarrow\res{a=6}$. L'asímptota és $y=3x-1+2$: \res{y=3x+1}."),
 (2, r"Estudia les branques infinites (asímptotes o branques parabòliques) de:" + tasks(2, [r"$f(x)=\sqrt x$", r"$f(x)=x+\sqrt x$", r"$f(x)=x\ln x$", r"$f(x)=\sqrt{x^2+x+1}-x$"]),
     tasks(1, [r"$\frac fx\to0$: branca parabòlica en la direcció de \rest{OX}", r"$m=1$, $n=\lim\sqrt x=+\infty$: branca en la direcció de \res{y=x}", r"$\frac fx=\ln x\to+\infty$: branca en la direcció de \rest{OY}",
               r"$+\infty$: $\frac{x+1}{\sqrt{x^2+x+1}+x}\to\frac12$, AH \res{y=\frac12}; $\ -\infty$: $m=-2$, $n=-\frac12$, AO \res{y=-2x-\frac12}"])),
 (2, r"Troba $b$ perquè $f(x)=\dfrac{2x^2+bx}{x+1}$ tinga l'asímptota obliqua $y=2x-1$.",
     r"$m=2$; $n=\lim\frac{(b-2)x}{x+1}=b-2=-1\Rightarrow\res{b=1}$."),
)

# =====================================================================
# 6. Monotonia, extrems i curvatura
f_ = 9 / (x**2 + x - 2); crit(f_, [-R(1, 2)]); ext(f_, -R(1, 2), 'max', -4)
f_ = sp.exp(-x**2); ext(f_, 0, 'max', 1); infl(f_, 1 / sq(2)); infl(f_, -1 / sq(2))
f_ = x**3 + a_ * x**2 + b_ * x + c_; s_ = sp.solve([sp.diff(f_, x, 2).subs(x, 1), sp.diff(f_, x).subs(x, 1) + 3, f_.subs(x, 1) - 2], [a_, b_, c_]); ok(s_ == {a_: -3, b_: 0, c_: 4})
f_ = x**4 - 4 * x**3; crit(f_, [0, 3]); ext(f_, 3, 'min', -27); infl(f_, 0, 0); infl(f_, 2, -16)
f_ = x**2 * ln(x); crit(f_, [sp.exp(-R(1, 2))], 0.001, 50); ext(f_, sp.exp(-R(1, 2)), 'min', -1 / (2 * E)); infl(f_, sp.exp(-R(3, 2)))
f_ = (x - 1) / x**2; crit(f_, [2]); ext(f_, 2, 'max', R(1, 4)); infl(f_, 3, R(2, 9))
sec("Monotonia, extrems i curvatura",
 (1, r"\pau{Catalunya, extraordinària 2022} Sigui $f(x)=\dfrac{9}{x^2+x-2}$. Determina'n el domini, les asímptotes, els extrems relatius i els intervals de creixement i decreixement."
     + recorda(r"Taula de signes de $f'$ amb els zeros de $f'$ i els punts que no són del domini; $f''$ per a la curvatura."),
     r"Domini $\mathbb R-\{-2,1\}$; AV \res{x=-2,\ x=1}, AH \res{y=0}. $f'=\frac{-9(2x+1)}{(x^2+x-2)^2}$: creix en $(-\infty,-2)\cup\left(-2,-\frac12\right)$, decreix en $\left(-\frac12,1\right)\cup(1,+\infty)$; \res{\text{màx. }\left(-\tfrac12,-4\right)}."),
 (2, r"\pau{Extremadura, ordinària 2021} Asímptotes, monotonia, extrems relatius i punts d'inflexió de $f(x)=e^{-x^2}$.",
     r"AH \res{y=0}. $f'=-2xe^{-x^2}$: creix en $(-\infty,0)$, decreix en $(0,+\infty)$; \res{\text{màx. }(0,1)}. $f''=(4x^2-2)e^{-x^2}$: \res{\text{P.I. en }x=\pm\tfrac{1}{\sqrt2}}."),
 (2, r"Estudia la monotonia, els extrems i la curvatura de $f(x)=x^4-4x^3$." ,
     r"$f'=4x^2(x-3)$: decreix en $(-\infty,3)$, creix en $(3,+\infty)$; \res{\text{mín. }(3,-27)} (en $x=0$, $f'=0$ sense extrem). $f''=12x(x-2)$: \res{\text{P.I. }(0,0)\text{ i }(2,-16)}; convexa en $(-\infty,0)\cup(2,+\infty)$."),
 (2, r"Estudia la monotonia i la curvatura de $f(x)=x^2\ln x$ i de $g(x)=\dfrac{x-1}{x^2}$.",
     r"$f'=x(2\ln x+1)$: \res{\text{mín. }\left(e^{-1/2},-\tfrac{1}{2e}\right)}; $f''=2\ln x+3$: P.I. en \res{x=e^{-3/2}}. \ $g'=\frac{2-x}{x^3}$: decreix en $(-\infty,0)\cup(2,+\infty)$, creix en $(0,2)$, \res{\text{màx. }\left(2,\tfrac14\right)}; $g''=\frac{2(x-3)}{x^4}$: \res{\text{P.I. }\left(3,\tfrac29\right)}."),
 (3, r"Troba $a$, $b$ i $c$ perquè $f(x)=x^3+ax^2+bx+c$ tinga un punt d'inflexió en $(1,2)$ amb tangent de pendent $-3$.",
     r"$f''(1)=6+2a=0$, $f'(1)=3+2a+b=-3$, $f(1)=1+a+b+c=2$: \res{a=-3,\ b=0,\ c=4}."),
)

# =====================================================================
# 7. Representació de funcions polinòmiques i racionals
f_ = x**3 + 3 * x**2 - 2; crit(f_, [-2, 0]); ext(f_, -2, 'max', 2); ext(f_, 0, 'min', -2); infl(f_, -1, 0)
f_ = (x**2 - 4) / (1 - x); obl(f_, -1, -1); ok(all(N(sp.diff(f_, x).subs(x, p)).real < 0 for p in (-9, -2, 0, 0.9, 1.1, 2, 7))); ok(sp.simplify(sp.diff(f_, x) - (-x**2 + 2 * x - 4) / (1 - x)**2) == 0)
f_ = (x - 4) / (1 - x); asy_h(f_, -1); ok(sp.simplify(sp.diff(f_, x) + 3 / (1 - x)**2) == 0)
f_ = (x + 3) / (x + 2)**2; asy_h(f_, 0); infl(f_, -5, -R(2, 9)); tang(f_, -5, -R(1, 27), -R(11, 27)); crit(f_, [-4]); ext(f_, -4, 'min', -R(1, 4))
f_ = 2 * x / (x**2 + 1); ext(f_, 1, 'max', 1); ext(f_, -1, 'min', -1)
f_ = x**3 / (x - 1)**2; obl(f_, 1, 2); crit(f_, [0, 3]); ext(f_, 3, 'min', R(27, 4)); infl(f_, 0, 0)
sec("Representació de funcions polinòmiques i racionals",
 (1, rep(r"\pau{País Basc, juliol 2019} " + fx(r'x^3+3x^2-2')) + REP,
     r"Domini $\mathbb R$, sense asímptotes. $f'=3x(x+2)$: \res{\text{màx. }(-2,2)}, \res{\text{mín. }(0,-2)}. $f''=6x+6$: \res{\text{P.I. }(-1,0)}."
     + cen(graf([lambda v: v**3 + 3 * v**2 - 2], (-3.5, 1.8, -3, 3.5), mx=[(-2, 2)], mn=[(0, -2)], ip=[(-1, 0)]))),
 (2, rep(r"\pau{Astúries, extraordinària 2024} " + fx(r'\dfrac{x^2-4}{1-x}')),
     r"Domini $\mathbb R-\{1\}$, talls $(\pm2,0)$, $(0,-4)$. AV \res{x=1}, AO \res{y=-x-1}. $f'=\frac{-x^2+2x-4}{(1-x)^2}<0$: \rest{decreixent}, sense extrems ni punts d'inflexió."
     + cen(graf([(lambda v: (v * v - 4) / (1 - v))], (-6, 7, -10, 10), va=[1], oa=[(-1, -1)], pts=[(-2, 0), (2, 0), (0, -4)]))),
 (2, rep(r"\pau{La Rioja, extraordinària 2020} " + fx(r'\dfrac{x+3}{(x+2)^2}') + r" i calcula la recta tangent en el punt d'inflexió"),
     r"AV \res{x=-2}, AH \res{y=0}. $f'=\frac{-(x+4)}{(x+2)^3}$: \res{\text{mín. }\left(-4,-\tfrac14\right)}. $f''=\frac{2(x+5)}{(x+2)^4}$: \res{\text{P.I. }\left(-5,-\tfrac29\right)}, tangent \res{x+27y+11=0}."
     + cen(graf([lambda v: (v + 3) / (v + 2)**2], (-9, 3, -1, 4), va=[-2], ha=[0], mn=[(-4, -0.25)], ip=[(-5, -2 / 9)], pts=[(-3, 0), (0, 0.75)]))),
 (2, rep(r"\pau{València, extraordinària 2025} " + fx(r'\dfrac{2x}{x^2+1}') + r" i calcula'n els extrems absoluts"),
     r"Senar, AH \res{y=0}. $f'=\frac{2(1-x^2)}{(x^2+1)^2}$: \res{\text{mín. abs. }(-1,-1)}, \res{\text{màx. abs. }(1,1)}. $f''=\frac{4x(x^2-3)}{(x^2+1)^3}$: P.I. en $0$ i $\pm\sqrt3$."
     + cen(graf([lambda v: 2 * v / (v * v + 1)], (-6, 6, -1.5, 1.5), ha=[0], mx=[(1, 1)], mn=[(-1, -1)], ip=[(0, 0), (r3, r3 / 2), (-r3, -r3 / 2)]))),
 (3, rep(fx(r'\dfrac{x^3}{(x-1)^2}')),
     r"AV \res{x=1}; $f=x+2+\frac{3x-2}{(x-1)^2}$: AO \res{y=x+2}. $f'=\frac{x^2(x-3)}{(x-1)^3}$: creix en $(-\infty,1)\cup(3,+\infty)$, decreix en $(1,3)$, \res{\text{mín. }\left(3,\tfrac{27}{4}\right)}. $f''=\frac{6x}{(x-1)^4}$: \res{\text{P.I. }(0,0)}."
     + cen(graf([lambda v: v**3 / (v - 1)**2], (-6, 8, -8, 16), va=[1], oa=[(1, 2)], mn=[(3, 6.75)], ip=[(0, 0)]))),
)
ok(sp.simplify(sp.diff(x**3 / (x - 1)**2, x) - x**2 * (x - 3) / (x - 1)**3) == 0)

# =====================================================================
# 8. Funcions radicals
f_ = x / sq(x - 1); crit(f_, [2], 1.001, 50); ext(f_, 2, 'min', 2); L(f_, 1, sp.oo, '+'); eq(sp.limit(f_ / x, x, sp.oo), 0)
f_ = x - 3 * sp.cbrt(x); crit(f_, [1], 0.001, 50); ext(f_, 1, 'min', -2)
f_ = (x + 1) / sq(x**2 + 3); crit(f_, [3]); ext(f_, 3, 'max', 2 / sq(3)); asy_h(f_, 1); asy_h(f_, -1, -sp.oo)
f_ = sq(x**2 - 9); obl(f_, 1, 0); obl(f_, -1, 0, -sp.oo)
f_ = x * sq(4 - x**2); crit(f_, [-sq(2), sq(2)], -1.999, 1.999); ext(f_, sq(2), 'max', 2)
sec("Representació de funcions radicals",
 (1, r"Domini, talls i asímptotes de:" + tasks(2, [r"$f(x)=\sqrt{x^2-9}$", r"$f(x)=\dfrac{x+1}{\sqrt{x^2+3}}$"])
     + recorda(r"$\sqrt{x^2+bx+c}\approx|x|+\frac b2$ quan $x\to\pm\infty$: les asímptotes poden ser diferents en cada costat. Multiplica pel conjugat per a calcular $n$."),
     tasks(1, [r"Domini $(-\infty,-3]\cup[3,+\infty)$, talls $(\pm3,0)$; AO \res{y=x} en $+\infty$ i \res{y=-x} en $-\infty$",
               r"Domini $\mathbb R$, talls $(-1,0)$ i $\left(0,\frac{1}{\sqrt3}\right)$; AH \res{y=1} en $+\infty$ i \res{y=-1} en $-\infty$"])),
 (2, rep(fx(r'\dfrac{x}{\sqrt{x-1}}')),
     r"Domini $(1,+\infty)$; AV \res{x=1} ($\to+\infty$). $f'=\frac{x-2}{2(x-1)^{3/2}}$: \res{\text{mín. }(2,2)}. $f''=\frac{4-x}{4(x-1)^{5/2}}$: \res{\text{P.I. }\left(4,\tfrac{4}{\sqrt3}\right)}. Branca parabòlica en la direcció de OX."
     + cen(graf([(lambda v: v / msq(v - 1), 1.0001, 12)], (-0.5, 12, -0.5, 6), va=[1], mn=[(2, 2)], ip=[(4, 4 / r3)]))),
 (2, rep(fx(r'x-3\sqrt[3]{x}')),
     r"Senar, talls $(0,0)$ i $\left(\pm3\sqrt3,0\right)$. $f'=1-\frac{1}{\sqrt[3]{x^2}}$: \res{\text{màx. }(-1,2)}, \res{\text{mín. }(1,-2)}; en $x=0$ tangent vertical. $f''=\frac{2}{3\sqrt[3]{x^5}}$: \res{\text{P.I. }(0,0)} (amb tangent vertical)."
     + cen(graf([lambda v: v - 3 * math.copysign(abs(v)**(1 / 3), v)], (-7, 7, -4, 4), mx=[(-1, 2)], mn=[(1, -2)], ip=[(0, 0)], pts=[(-3 * r3, 0), (3 * r3, 0)]))),
 (2, rep(fx(r'\dfrac{x+1}{\sqrt{x^2+3}}')),
     r"AH \res{y=1} ($+\infty$) i \res{y=-1} ($-\infty$). $f'=\frac{3-x}{(x^2+3)^{3/2}}$: creix en $(-\infty,3)$, decreix en $(3,+\infty)$; \res{\text{màx. abs. }\left(3,\tfrac{2}{\sqrt3}\right)}."
     + cen(graf([lambda v: (v + 1) / math.sqrt(v * v + 3)], (-10, 12, -1.5, 1.5), ha=[1, -1], mx=[(3, 2 / r3)], pts=[(-1, 0), (0, 1 / r3)]))),
 (3, r"Sigui $f(x)=x\sqrt{4-x^2}$. Estudia'n el domini, la simetria, els extrems absoluts i els punts en què la tangent és vertical, i representa-la.",
     r"Domini $[-2,2]$, senar. $f'=\frac{2(2-x^2)}{\sqrt{4-x^2}}$: \res{\text{mín. abs. }\left(-\sqrt2,-2\right)}, \res{\text{màx. abs. }\left(\sqrt2,2\right)}; tangents verticals en \res{x=\pm2}; P.I. $(0,0)$."
     + cen(graf([(lambda v: v * msq(4 - v * v), -2, 2)], (-2.6, 2.6, -2.6, 2.6), mx=[(r2, 2)], mn=[(-r2, -2)], ip=[(0, 0)], pts=[(-2, 0), (2, 0)]))),
)
infl(x / sq(x - 1), 4, 4 / sq(3))

# =====================================================================
# 9. Exponencials i logarítmiques
f_ = x * sp.exp(-x); ext(f_, 1, 'max', 1 / E); infl(f_, 2, 2 / E**2); asy_h(f_, 0)
f_ = 2 * x * sp.exp(-2 * x**2); ext(f_, R(1, 2), 'max', 1 / sq(E)); ext(f_, -R(1, 2), 'min', -1 / sq(E))
f_ = sp.exp(x) / x; ext(f_, 1, 'min', E); asy_h(f_, 0, -sp.oo); L(f_, 0, sp.oo, '+')
f_ = ln(x**2 - 4); ok(sorted(sp.solve(f_, x)) == [-sq(5), sq(5)])
f_ = x * (ln(x) - 1); ext(f_, 1, 'min', -1); L(f_, 0, 0, '+')
f_ = ln(x) / x; ext(f_, E, 'max', 1 / E); infl(f_, E**R(3, 2), R(3, 2) * E**(-R(3, 2)))
sec("Representació de funcions exponencials i logarítmiques",
 (1, rep(r"\pau{Castella i Lleó, juny 2018} " + fx(r'x\,e^{-x}')) + REP,
     r"Tall $(0,0)$; AH \res{y=0} en $+\infty$. $f'=(1-x)e^{-x}$: \res{\text{màx. }\left(1,\tfrac1e\right)}. $f''=(x-2)e^{-x}$: \res{\text{P.I. }\left(2,\tfrac{2}{e^2}\right)}."
     + cen(graf([lambda v: v * me(-v)], (-1.5, 7, -2, 0.7), ha=[0], mx=[(1, 1 / math.e)], ip=[(2, 2 / math.e**2)]))),
 (2, rep(r"\pau{País Basc, extraordinària 2024} " + fx(r'2x\,e^{-2x^2}')),
     r"Senar, AH \res{y=0}. $f'=2(1-4x^2)e^{-2x^2}$: \res{\text{mín. }\left(-\tfrac12,-\tfrac{1}{\sqrt e}\right)}, \res{\text{màx. }\left(\tfrac12,\tfrac{1}{\sqrt e}\right)}. P.I. en $x=0$ i $x=\pm\frac{\sqrt3}{2}$."
     + cen(graf([lambda v: 2 * v * me(-2 * v * v)], (-2.5, 2.5, -0.9, 0.9), ha=[0], mx=[(0.5, 1 / math.sqrt(math.e))], mn=[(-0.5, -1 / math.sqrt(math.e))], ip=[(0, 0), (r3 / 2, r3 * me(-1.5)), (-r3 / 2, -r3 * me(-1.5))]))),
 (2, rep(r"\pau{Cantàbria, extraordinària 2022} " + fx(r'\dfrac{e^x}{x}')),
     r"AV \res{x=0}, AH \res{y=0} en $-\infty$. $f'=\frac{(x-1)e^x}{x^2}$: \res{\text{mín. }(1,e)}. $f''=\frac{e^x(x^2-2x+2)}{x^3}$: còncava en $(-\infty,0)$, convexa en $(0,+\infty)$."
     + cen(graf([lambda v: me(v) / v], (-5, 3.5, -4, 10), va=[0], ha=[0], mn=[(1, math.e)]))),
 (2, rep(r"\pau{Catalunya, ordinària 2021} " + fx(r'\dfrac{\ln x}{x}')),
     r"Domini $(0,+\infty)$; AV \res{x=0}, AH \res{y=0}; tall $(1,0)$. $f'=\frac{1-\ln x}{x^2}$: \res{\text{màx. }\left(e,\tfrac1e\right)}. $f''=\frac{2\ln x-3}{x^3}$: \res{\text{P.I. en }x=e^{3/2}}."
     + cen(graf([(lambda v: mln(v) / v, 0.05, 20)], (-0.5, 20, -2, 0.8), va=[0], ha=[0], mx=[(math.e, 1 / math.e)], ip=[(math.e**1.5, 1.5 * math.e**-1.5)], pts=[(1, 0)]))),
 (2, rep(fx(r'\ln\left(x^2-4\right)')),
     r"Domini $|x|>2$, parella; AV \res{x=\pm2}; talls $\left(\pm\sqrt5,0\right)$. $f'=\frac{2x}{x^2-4}$: decreix en $(-\infty,-2)$, creix en $(2,+\infty)$; sense extrems. $f''=\frac{-2(x^2+4)}{(x^2-4)^2}<0$: còncava."
     + cen(graf([(lambda v: mlog(v * v - 4), -9, -2.0001), (lambda v: mlog(v * v - 4), 2.0001, 9)], (-8, 8, -4, 5), va=[-2, 2], pts=[(-math.sqrt(5), 0), (math.sqrt(5), 0)]))),
 (2, r"\pau{Castella i Lleó, ordinària 2023} Domini, monotonia i extrems de $f(x)=x(\ln x-1)$. Com és la gràfica a prop de $x=0$?",
     r"Domini $(0,+\infty)$. $f'=\ln x$: decreix en $(0,1)$, creix en $(1,+\infty)$; \res{\text{mín. }(1,-1)}. Tall $(e,0)$. $\lim_{x\to0^+}f=0$: la gràfica \rest{surt de l'origen} (sense AV)."),
)

# =====================================================================
# 10. Trigonomètriques
f_ = sin(x) * (1 + cos(x)); crit(f_, [pi / 3, pi, 5 * pi / 3], 0.001, 2 * math.pi - 0.001); ext(f_, pi / 3, 'max', 3 * sq(3) / 4); ext(f_, 5 * pi / 3, 'min', -3 * sq(3) / 4)
f_ = sin(x)**2 + cos(x); ext(f_, pi / 3, 'max', R(5, 4)); ext(f_, pi, 'min', -1); ext(f_, 0, 'min', 1); parity(f_, 'even')
f_ = tan(x) - 2 * x; ext(f_, pi / 4, 'min', 1 - pi / 2); ext(f_, -pi / 4, 'max', pi / 2 - 1); parity(f_, 'odd')
f_ = (1 - cos(x)) / x; L(f_, 0, 0); asy_h(f_, 0)
f_ = x + cos(x); infl(f_, pi / 2); infl(f_, 3 * pi / 2)
sec("Representació de funcions trigonomètriques",
 (2, rep(fx(r'\sin x\,(1+\cos x)')) + recorda(r"Si és periòdica, estudia-la en un període. Factoritza $f'$ amb les identitats ($\cos2x=2\cos^2x-1$…)."),
     r"Període $2\pi$, senar. $f'=\cos x+\cos2x=(2\cos x-1)(\cos x+1)$: zeros $\frac\pi3$, $\pi$, $\frac{5\pi}3$. \res{\text{màx. }\left(\tfrac\pi3,\tfrac{3\sqrt3}4\right)}, \res{\text{mín. }\left(\tfrac{5\pi}3,-\tfrac{3\sqrt3}4\right)} ($+2k\pi$); en $x=\pi$, $f'=0$ sense extrem."
     + cen(graf([lambda v: ms(v) * (1 + mc(v))], (-1, 7.3, -1.6, 1.6), mx=[(PI / 3, 3 * r3 / 4)], mn=[(5 * PI / 3, -3 * r3 / 4)], pts=[(0, 0), (PI, 0), (2 * PI, 0)], xt=PIX))),
 (2, rep(fx(r'\sin^2x+\cos x') + r" en $[0,2\pi]$"),
     r"Parella, període $2\pi$. $f'=\sin x\,(2\cos x-1)$: \res{\text{màx. }\left(\tfrac\pi3,\tfrac54\right)\text{ i }\left(\tfrac{5\pi}3,\tfrac54\right)}, \res{\text{mín. }(\pi,-1)}; en $x=0$ i $x=2\pi$, mínims relatius de valor 1."
     + cen(graf([(lambda v: ms(v)**2 + mc(v), 0, 2 * PI)], (-0.4, 6.8, -1.3, 1.6), mx=[(PI / 3, 1.25), (5 * PI / 3, 1.25)], mn=[(PI, -1), (0, 1), (2 * PI, 1)], xt=PIX))),
 (2, r"Estudia $f(x)=\tan x-2x$ en $\left(-\frac\pi2,\frac\pi2\right)$: asímptotes, extrems i curvatura.",
     r"Senar; AV \res{x=\pm\frac\pi2}. $f'=\frac{1}{\cos^2x}-2=0\Leftrightarrow\cos^2x=\frac12$: \res{\text{màx. }\left(-\tfrac\pi4,\tfrac\pi2-1\right)}, \res{\text{mín. }\left(\tfrac\pi4,1-\tfrac\pi2\right)}. $f''=\frac{2\sin x}{\cos^3x}$: \res{\text{P.I. }(0,0)}."
     + cen(graf([(lambda v: mt(v) - 2 * v, -PI / 2 + 0.01, PI / 2 - 0.01)], (-1.8, 1.8, -4, 4), va=[-PI / 2, PI / 2], mx=[(-PI / 4, PI / 2 - 1)], mn=[(PI / 4, 1 - PI / 2)], ip=[(0, 0)]))),
 (2, r"\pau{Cantàbria, extraordinària 2020} Sigui $f(x)=\dfrac{1-\cos x}{x}$. Calcula $\displaystyle\lim_{x\to0}f(x)$ i les asímptotes de $f$.",
     r"$\left[\frac00\right]\overset{\text{L'H}}{=}\lim\frac{\sin x}{1}=\res{0}$: no hi ha AV. Com que $0\leq1-\cos x\leq2$, $\left|f\right|\leq\frac2{|x|}\to0$: AH \res{y=0} (en tots dos costats); sense AO."),
 (2, r"Estudia la monotonia i la curvatura de $f(x)=x+\cos x$ en $[0,2\pi]$ i representa-la.",
     r"$f'=1-\sin x\geq0$: \rest{creixent} (amb tangent horitzontal en $\frac\pi2$). $f''=-\cos x$: \res{\text{P.I. en }\tfrac\pi2\text{ i }\tfrac{3\pi}2}; còncava en $\left(0,\frac\pi2\right)\cup\left(\frac{3\pi}2,2\pi\right)$."
     + cen(graf([(lambda v: v + mc(v), 0, 2 * PI)], (-0.4, 6.8, -0.5, 7.5), ip=[(PI / 2, PI / 2), (3 * PI / 2, 3 * PI / 2)], pts=[(0, 1), (2 * PI, 2 * PI + 1)], xt=PIX))),
)
crit(sin(x)**2 + cos(x), [pi / 3, pi, 5 * pi / 3], 0.001, 2 * math.pi - 0.001)

# =====================================================================
# 11. A trossos, valor absolut i transformacions
f_ = sp.Abs(x**2 - 2 * x - 3); eq(f_.subs(x, 1), 4)
f_ = x**2 - 4 * sp.Abs(x) + 3; eq(f_.subs(x, 2), -1); eq(f_.subs(x, 0), 3); ok(sorted(sp.solve(x**2 - 4 * x + 3, x)) == [1, 3])
ok(sp.solve([9 * a_ + b_ - ln(1), 6 * a_ - 1], [a_, b_]) == {a_: R(1, 6), b_: -R(3, 2)})
L(x * ln(x), 0, 0, '+'); L(sp.diff(x * ln(x), x), 0, -sp.oo, '+'); ext(x * ln(x), 1 / E, 'min', -1 / E)
sec("Funcions a trossos, amb valor absolut i transformacions",
 (1, r"Escriu a trossos i representa:" + tasks(2, [r"$f(x)=\left|x^2-2x-3\right|$", r"$f(x)=x^2-4|x|+3$", r"$f(x)=e^{-|x|}$", r"$f(x)=|x|\,(x-2)$"])
     + recorda(r"$|g(x)|=g(x)$ si $g(x)\geq0$ i $-g(x)$ si $g(x)<0$. Els canvis de tros solen ser punts angulosos."),
     tasks(2, [r"Mínims angulosos $(-1,0)$, $(3,0)$; \res{\text{màx. }(1,4)}" + cen(graf([lambda v: abs(v * v - 2 * v - 3)], (-2.5, 4.5, -0.5, 6), mn=[(-1, 0), (3, 0)], mx=[(1, 4)], w=4.6, h=3.2)),
               r"Parella: \res{\text{mín. }(\pm2,-1)}, \res{\text{màx. anguló }(0,3)}" + cen(graf([lambda v: v * v - 4 * abs(v) + 3], (-4.5, 4.5, -1.5, 4), mn=[(-2, -1), (2, -1)], mx=[(0, 3)], pts=[(-3, 0), (-1, 0), (1, 0), (3, 0)], w=4.6, h=3.2)),
               r"Parella, AH $y=0$, \res{\text{màx. anguló }(0,1)}" + cen(graf([lambda v: me(-abs(v))], (-4, 4, -0.3, 1.3), ha=[0], mx=[(0, 1)], w=4.6, h=3.2)),
               r"$-x^2+2x$ si $x<0$, $x^2-2x$ si $x\geq0$: \res{\text{màx. anguló }(0,0)}, \res{\text{mín. }(1,-1)}" + cen(graf([lambda v: abs(v) * (v - 2)], (-2, 3.5, -3, 2), mx=[(0, 0)], mn=[(1, -1)], pts=[(2, 0)], w=4.6, h=3.2))])),
 (2, r"A partir de les gràfiques de les funcions elementals, dibuixa:" + tasks(2, [r"$y=\sqrt{x+4}-2$", r"$y=-\sqrt{-x}$", r"$y=2-e^{-x}$", r"$y=\left|\ln(x+1)\right|$"]),
     tasks(1, [r"$\sqrt x$ traslladada 4 a l'esquerra i 2 avall: comença en $(-4,-2)$ i passa per \res{(0,0)}", r"$\sqrt x$ amb simetries respecte de OY i de OX (respecte de l'origen): domini $(-\infty,0]$",
               r"$e^x$ $\to$ $e^{-x}$ (simetria OY) $\to$ $-e^{-x}$ (simetria OX) $\to$ $+2$: AH \res{y=2} en $+\infty$, tall \res{(0,1)}", r"$\ln(x+1)$ (AV $x=-1$) amb la part negativa reflectida: \res{\text{mín. anguló }(0,0)}"])),
 (2, r"\pau{Galícia, juny 2017} Calcula $a$ i $b$ perquè sigui derivable en $x=3$ la funció $f(x)=\begin{cases}ax^2+b&\text{si }x<3\\ \ln(x-2)&\text{si }x\geq3\end{cases}$ i representa-la.",
     r"Contínua: $9a+b=\ln1=0$; derivable: $6a=\frac{1}{3-2}=1$. \res{a=\frac16,\ b=-\frac32}. Paràbola de vèrtex $\left(0,-\frac32\right)$ fins a $(3,0)$ i després $\ln(x-2)$, sense angle."
     + cen(graf([(lambda v: v * v / 6 - 1.5, -5, 3), (lambda v: mlog(v - 2), 3, 9)], (-4.5, 9, -2, 3), mn=[(0, -1.5)], pts=[(3, 0), (-3, 0)]))),
 (3, r"\pau{Madrid, extraordinària 2022} Sigui $f(x)=\begin{cases}x&\text{si }x\leq0\\ x\ln x&\text{si }x>0\end{cases}$." + tasks(1, [r"Estudia la continuïtat i la derivabilitat en $x=0$.", r"Estudia'n la monotonia i els extrems relatius, i representa-la."]),
     tasks(1, [r"$\lim_{x\to0^+}x\ln x=0=f(0)$: \rest{contínua}. $f'(0^-)=1$ i $f'(0^+)=\lim(\ln x+1)=-\infty$: \rest{no derivable}.",
               r"Creix en $(-\infty,0)$, decreix en $\left(0,\frac1e\right)$, creix en $\left(\frac1e,+\infty\right)$: \res{\text{màx. }(0,0)} (no derivable), \res{\text{mín. }\left(\tfrac1e,-\tfrac1e\right)}."
               + cen(graf([(lambda v: v, -3, 0), (lambda v: v * mlog(v), 0.0001, 3)], (-2.5, 2.8, -1.5, 2), mx=[(0, 0)], mn=[(1 / math.e, -1 / math.e)], pts=[(1, 0)]))])),
)

# =====================================================================
# 12. Gràfiques de f, f' i f''
fp = (x - 1)**2 * (x + 2); ok(sp.expand(sp.diff(fp, x) - 3 * (x - 1) * (x + 1)) == 0)
g_ = a_ * x**3 + b_ * x**2 + 1; ok(sp.solve([sp.diff(g_, x, 2).subs(x, R(1, 2)), sp.diff(g_, x).subs(x, R(1, 2)) + R(3, 2)], [a_, b_]) == {a_: 2, b_: -3})
p_ = a_ * x**3 + b_ * x**2 + c_ * x + d_; ok(sp.solve([sp.diff(p_, x).subs(x, -1), sp.diff(p_, x).subs(x, 2), p_.subs(x, 0) - 1, p_.subs(x, 2) + 19], [a_, b_, c_, d_]) == {a_: 2, b_: -3, c_: -12, d_: 1})
sec("Informació a partir de les gràfiques de f, f' i f''",
 (2, r"Sabem que $f'(x)=(x-1)^2(x+2)$. Sense calcular $f$, estudia'n la monotonia, els extrems i la curvatura, i dibuixa'n una gràfica possible."
     + recorda(r"$f'>0\Rightarrow f$ creix; canvi de signe de $f'$ $\Rightarrow$ extrem; $f'$ creix ($f''>0$) $\Rightarrow f$ convexa; extrem de $f'$ $\Rightarrow$ inflexió de $f$."),
     r"$f'\geq0$ si $x>-2$: decreix en $(-\infty,-2)$, creix en $(-2,+\infty)$; \res{\text{mín. en }x=-2}; en $x=1$, \rest{inflexió amb tangent horitzontal}. $f''=3(x-1)(x+1)$: convexa en $(-\infty,-1)\cup(1,+\infty)$, còncava en $(-1,1)$; \res{\text{P.I. en }x=\pm1}."),
 (2, r"\pau{Catalunya, extraordinària 2021} Calcula $a$ i $b$ perquè $g(x)=ax^3+bx^2+1$ tinga un punt d'inflexió en $x=\frac12$ i la seua derivada en aquest punt siga $-\frac32$.",
     r"$g''\left(\frac12\right)=3a+2b=0$, $g'\left(\frac12\right)=\frac{3a}4+b=-\frac32$: \res{a=2,\ b=-3}."),
 (2, r"La gràfica de la derivada d'un polinomi $p$ de grau 3 és una paràbola que talla l'eix OX en $x=-1$ i $x=2$. Si $p(0)=1$ i $p(2)=-19$, troba $p$ i digues on té els extrems i el punt d'inflexió.",
     r"$p'=k(x+1)(x-2)=k(x^2-x-2)\Rightarrow p=k\left(\frac{x^3}3-\frac{x^2}2-2x\right)+1$; $p(2)=-\frac{10k}3+1=-19\Rightarrow k=6$: \res{p(x)=2x^3-3x^2-12x+1}. Màx. en \res{x=-1}, mín. en \res{x=2}, P.I. en \res{x=\frac12}."),
 (2, r"\pau{Galícia, extraordinària 2026} Dibuixa la gràfica d'una funció $f:\mathbb R-\{2\}\to\mathbb R$ tal que $f$, $f'$ i $f''$ tinguen el mateix signe en $(-1,2)$ i $\displaystyle\lim_{x\to2^+}f(x)=-\infty$. Explica el dibuix.",
     r"Per exemple, \res{f(x)=\frac{1}{2-x}}: en $(-1,2)$ és positiva, creixent ($f'>0$) i convexa ($f''>0$); té l'AV $x=2$ ($+\infty$ per l'esquerra, $-\infty$ per la dreta) i l'AH $y=0$."
     + cen(graf([lambda v: 1 / (2 - v)], (-3, 6, -5, 5), va=[2], ha=[0]))),
 (3, r"\pau{Galícia, ordinària 2022} Dibuixa la gràfica d'una funció contínua i no negativa en $[0,3]$ tal que $f(0)=f(3)=0$, $f''>0$ en $(0,1)$, $f''<0$ en $(2,3)$ i constant en $(1,2)$. Pot ser derivable en $x=1$?",
     r"Per exemple, \res{x^2} en $[0,1]$, \res{1} en $[1,2]$ i \res{1-(x-2)^2} en $[2,3]$. En $x=1$ \rest{no} pot ser derivable: si és convexa i puja des de $(0,0)$, el pendent és positiu i creixent i no pot valdre 0 en $x=1$."
     + cen(graf([(lambda v: v * v, 0, 1), (lambda v: 1, 1, 2), (lambda v: 1 - (v - 2)**2, 2, 3)], (-0.4, 3.4, -0.3, 1.4), pts=[(0, 0), (3, 0)]))),
)

# =====================================================================
print(NCHK[0], 'comprovacions correctes')
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={representació de funcions, domini, simetries, periodicitat, asímptotes, branques parabòliques, monotonia, curvatura, funcions radicals, trigonomètriques, a trossos, transformacions, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre = pre.replace(r'\usepackage{amsmath,amssymb}', r'\usepackage{amsmath,amssymb}' + '\n' + r'\allowdisplaybreaks')
pre += '\n\\setlength{\\emergencystretch}{3em}\n'
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Representació gràfica de funcions"
def build(sol):
    tt = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 8: %s. 2n de Batxillerat MII}" % (tt, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 8: %s · 2n Batxillerat MII" % (tt, TIT))
    assert 'MII}' in p and '2n Batxillerat MII' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques II}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 8' if sol else "Fitxa d'exercicis · Unitat 8") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Les gràfiques de les solucions marquen en verd els màxims, en roig els mínims i en violeta els punts d'inflexió; les línies discontínues són asímptotes. Pots comprovar els estudis complets amb la calculadora dels apunts interactius."
             if sol else r"Resol els exercicis al quadern justificant cada pas. Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat de València i d'altres comunitats autònomes, traduïts al valencià. Pots comprovar els resultats amb les eines dels apunts interactius (dominis, asímptotes, estudi complet d'una funció pas a pas, transformacions\dots).") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, qq, s in exs:
            n += 1
            if sol:
                head = re.sub(r'(\\pau\{[^}]*\}).*', r'\1', qq, flags=re.S) if qq.startswith('\\pau{') else ''
                out.append('\\ex{%d} %s%s\n\n' % (st, head, s))
            else:
                out.append('\\ex{%d} %s\n\n' % (st, qq))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus estudis amb les eines dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't8-fitxa-solucions.tex' if sol else 't8-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'exercicis,', npau, 'de la PAU de', len(regs), 'comunitats:', ', '.join(regs))
