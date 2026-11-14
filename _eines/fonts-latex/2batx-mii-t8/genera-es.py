# Versió en castellà de genera.py. Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 8: Representació gràfica
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
    """los ceros reales de f' (en [lo, hi] y dentro del dominio) son xs"""
    d = sp.diff(f, x)
    sols = sorted(set(round(float(s), 9) for s in sp.solveset(sp.simplify(d), x, sp.Interval(lo, hi)) if s.is_real and abs(N(f.subs(x, s))) < 1e12))
    ok(len(sols) == len(xs) and all(abs(p - float(q)) < 1e-7 for p, q in zip(sols, sorted(float(v) for v in xs))))
def ext(f, x0, kind, val=None):
    """extremo relativo en x0 (comprobado por el cambio de signo de f')"""
    d = sp.diff(f, x); e = 1e-4
    l, r = N(d.subs(x, x0 - e)).real, N(d.subs(x, x0 + e)).real
    ok((l > 0 > r) if kind == 'max' else (l < 0 < r))
    if val is not None: eq(f.subs(x, x0), val)
def infl(f, x0, val=None):
    d2 = sp.diff(f, x, 2); e = 1e-4
    ok(N(d2.subs(x, x0 - e)).real * N(d2.subs(x, x0 + e)).real < 0)
    if val is not None: eq(f.subs(x, x0), val)
def sgn_on(g, a, b, s):
    """g tiene signo s en unos cuantos puntos de (a, b)"""
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
    """curves: lista de funciones o de (f, a, b); box: (x0, x1, y0, y1). xt: marcas del eje x [(valor, texto)]."""
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
REP = recorda(r"Dominio, simetría, cortes, asíntotas (y posición), monotonía y extremos, curvatura e inflexión; después situamos toda la información y dibujamos.")
def rep(fn): return r"Haz el estudio completo y representa " + fn + "."

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
sec("Dominio de una función",
 (1, r"Calcula el dominio de las funciones siguientes:" + tasks(2, [r"$f(x)=\dfrac{x+3}{x^2-5x+6}$", r"$f(x)=\sqrt{9-x^2}$", r"$f(x)=\sqrt{\dfrac{x-1}{x+2}}$", r"$f(x)=\ln\left(4-x^2\right)$",
                                                               r"$f(x)=\dfrac{1}{\sqrt{x^2-2x-3}}$", r"$f(x)=\sqrt[3]{\dfrac{x}{x^2-1}}$", r"$f(x)=\dfrac{e^x}{e^{2x}-1}$", r"$f(x)=\ln(\ln x)$"])
     + recorda(r"Denominadores $\neq0$; radicandos de índice par $\geq0$ (y $>0$ si la raíz está en el denominador); argumentos de los logaritmos $>0$. El dominio es la intersección de todas las condiciones."),
     tasks(2, [r"$\res{\mathbb R-\{2,3\}}$", r"$\res{[-3,3]}$", r"$\res{(-\infty,-2)\cup[1,+\infty)}$", r"$\res{(-2,2)}$", r"$(x+1)(x-3)>0$: $\res{(-\infty,-1)\cup(3,+\infty)}$",
               r"$\res{\mathbb R-\{-1,1\}}$ (índice impar)", r"$e^{2x}\neq1$: $\res{\mathbb R-\{0\}}$", r"$\ln x>0$: $\res{(1,+\infty)}$"])),
 (2, r"Dominio de:" + tasks(2, [r"$f(x)=\tan3x$", r"$f(x)=\dfrac{1}{1-\cos x}$", r"$f(x)=\arcsin\dfrac x2$", r"$f(x)=\sqrt{\sin x}$, en $[0,2\pi]$", r"$f(x)=\ln(\cos x)$, en $[0,2\pi]$"]),
     tasks(2, [r"$3x\neq\frac\pi2+k\pi$: $\res{\mathbb R-\left\{\frac\pi6+\frac{k\pi}3\right\}}$", r"$\cos x\neq1$: $\res{\mathbb R-\{2k\pi\}}$", r"$-1\leq\frac x2\leq1$: $\res{[-2,2]}$", r"$\sin x\geq0$: $\res{[0,\pi]}$", r"$\cos x>0$: $\res{\left[0,\frac\pi2\right)\cup\left(\frac{3\pi}2,2\pi\right]}$"])),
 (2, r"Dominio de:" + tasks(1, [r"\pau{Aragón, ordinaria 2023} $f(x)=\dfrac{2x-1}{\sqrt{x^2-x-2}}$", r"\pau{Canarias, ordinaria 2024} $f(x)=\dfrac{\ln(x+2)}{3x+4}$"]),
     tasks(1, [r"$(x+1)(x-2)>0$: $\res{(-\infty,-1)\cup(2,+\infty)}$", r"$x>-2$ y $x\neq-\frac43$: $\res{\left(-2,-\frac43\right)\cup\left(-\frac43,+\infty\right)}$"])),
 (3, r"Dominio de:" + tasks(1, [r"$f(x)=\sqrt{\dfrac{x^2-4}{x^2-9}}$", r"$f(x)=\log_2\left(x^2-x\right)-\sqrt{3-x}$"]),
     tasks(1, [r"Signos de $\frac{(x+2)(x-2)}{(x+3)(x-3)}$ con los puntos $\pm2$ (incluidos) y $\pm3$ (excluidos): $\res{(-\infty,-3)\cup[-2,2]\cup(3,+\infty)}$",
               r"$x(x-1)>0$ y $x\leq3$: $\res{(-\infty,0)\cup(1,3]}$"])),
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
sec("Cortes con los ejes y signo de la función",
 (1, r"Halla los puntos de corte con los ejes y estudia el signo de:" + tasks(2, [r"$f(x)=x^3-x^2-6x$", r"$f(x)=\dfrac{x^2-4x+3}{x+1}$", r"$f(x)=\left(x^2-1\right)e^x$", r"$f(x)=\ln\left(x^2-8\right)$"])
     + recorda(r"Los ceros de $f$ y los puntos donde no es continua separan intervalos de signo constante: basta con un valor de prueba en cada uno."),
     tasks(1, [r"$x(x+2)(x-3)$: $(0,0)$, $(-2,0)$, $(3,0)$; \res{f<0\text{ en }(-\infty,-2)\cup(0,3)}, \res{f>0\text{ en }(-2,0)\cup(3,+\infty)}",
               r"$(0,3)$, $(1,0)$, $(3,0)$; \res{f<0\text{ en }(-\infty,-1)\cup(1,3)}, \res{f>0\text{ en }(-1,1)\cup(3,+\infty)}",
               r"$(0,-1)$, $(\pm1,0)$; \res{f<0\text{ en }(-1,1)}, positiva fuera ($e^x>0$)",
               r"Dominio $|x|>2\sqrt2$, no corta OY; $x^2-8=1\Rightarrow(\pm3,0)$; \res{f<0\text{ en }\left(-3,-2\sqrt2\right)\cup\left(2\sqrt2,3\right)}, positiva si $|x|>3$"])),
 (2, r"\pau{Extremadura, junio 2018} Demuestra que $f(x)=x^3+x-3$ corta el eje de abscisas en un único punto, que es positivo, y halla un intervalo de longitud $\frac12$ que lo contenga.",
     r"$f(1)=-1<0$, $f(2)=7>0$: por Bolzano hay un cero en $(1,2)$. $f'(x)=3x^2+1>0$: es estrictamente creciente y el cero es \rest{único}. Como $f\left(\frac32\right)=\frac{15}8>0$, está en $\res{\left(1,\tfrac32\right)}$."),
 (2, r"Estudia el signo de $f(x)=\dfrac{(x-2)^2(x+1)}{x^3}$. ¿Dónde corta o toca el eje OX?",
     r"Puntos $-1$, $0$ y $2$ (doble). \res{f>0\text{ en }(-\infty,-1)\cup(0,2)\cup(2,+\infty)}, \res{f<0\text{ en }(-1,0)}. Corta OX en $(-1,0)$ y lo \rest{toca} en $(2,0)$ sin cambiar de signo."),
 (3, r"¿Cuántas soluciones tiene la ecuación $x=2\sin x$? Localiza la positiva entre dos décimas consecutivas.",
     r"$f(x)=x-2\sin x$ es impar y $f(0)=0$. Si $|x|>2$, $|x|>2\geq|2\sin x|$: no hay ceros. En $(0,2]$: $f'=1-2\cos x$: decrece en $\left(0,\frac\pi3\right)$ (y allí es negativa) y después crece, así que tiene un único cero positivo; $f(1{,}8)\approx-0{,}15<0<f(1{,}9)\approx0{,}01$. Hay \res{3\text{ soluciones}}: $0$ y $\pm x_0$, con $\res{x_0\in(1{,}8;\,1{,}9)}$."),
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
sec("Simetrías y periodicidad",
 (1, r"Estudia la simetría de las funciones siguientes:" + tasks(2, [r"$f(x)=x^4-3x^2+1$", r"$f(x)=\dfrac{x}{x^2-4}$", r"$f(x)=e^{-x^2}\cos x$", r"$f(x)=x^3+1$", r"$f(x)=\ln\dfrac{1+x}{1-x}$", r"$f(x)=\dfrac{\sin x\cos x}{x}$"])
     + recorda(r"Par: $f(-x)=f(x)$ (simetría respecto a OY). Impar: $f(-x)=-f(x)$ (respecto al origen). El dominio tiene que ser simétrico."),
     tasks(2, [r"\rest{par}", r"\rest{impar}", r"\rest{par}", r"\rest{ninguna} ($f(-x)=1-x^3$)", r"\rest{impar}: $\ln\frac{1-x}{1+x}=-\ln\frac{1+x}{1-x}$", r"\rest{par} (cociente de dos impares)"])),
 (1, r"Calcula el período de:" + tasks(3, [r"$\sin3x$", r"$\cos\dfrac x2$", r"$\sin x+\sin2x$", r"$\sin^2(2x)$", r"$\tan\dfrac{\pi x}{4}$", r"$|\cos x|$"]),
     tasks(3, [r"$\res{\frac{2\pi}3}$", r"$\res{4\pi}$", r"$\res{2\pi}$", r"$\res{\frac\pi2}$", r"$\res{4}$", r"$\res{\pi}$"])),
 (2, r"Comprueba que la gráfica de $f(x)=\dfrac{x^2+1}{x-1}$ es simétrica respecto al punto en el que se cortan sus asíntotas, y que la de $g(x)=\dfrac{1}{x^2-6x+10}$ es simétrica respecto a una recta vertical.",
     r"$f(x)=x+1+\frac{2}{x-1}$: AV $x=1$ y AO $y=x+1$, que se cortan en $(1,2)$; $f(1+h)-2=h+\frac2h$ es impar: simétrica respecto a \res{(1,2)}. \ $g(x)=\frac{1}{(x-3)^2+1}$: $g(3+h)=g(3-h)$, simétrica respecto a \res{x=3}."),
 (3, r"Demuestra que $f(x)=\ln\left(x+\sqrt{x^2+1}\right)$ es impar.",
     r"$f(-x)=\ln\left(\sqrt{x^2+1}-x\right)=\ln\dfrac{\left(\sqrt{x^2+1}-x\right)\left(\sqrt{x^2+1}+x\right)}{\sqrt{x^2+1}+x}=\ln\dfrac{1}{\sqrt{x^2+1}+x}=-f(x)$: \rest{es impar}."),
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
sec("Asíntotas verticales y horizontales",
 (1, r"Calcula las asíntotas verticales y horizontales (con los límites laterales):" + tasks(2, [r"$f(x)=\dfrac{2x^2-3}{x^2-1}$", r"$f(x)=\dfrac{x+2}{x^2-4}$", r"$f(x)=\dfrac{3e^x}{e^x+1}$", r"$f(x)=\dfrac{\sqrt{x^2+1}}{x}$", r"$f(x)=\dfrac{\ln x}{x-1}$"])
     + recorda(r"AV $x=a$ si algún límite lateral en $a$ es infinito. AH $y=k$ si $\displaystyle\lim_{x\to\pm\infty}f(x)=k$: estudia cada lado por separado. Cuidado: $\sqrt{x^2}=|x|$."),
     tasks(1, [r"\res{x=\pm1} ($\lim_{x\to1^\pm}f=\mp\infty$…), \res{y=2}",
               r"$f=\frac{1}{x-2}$ si $x\neq-2$: \res{x=2} (en $x=-2$ hay un agujero, $\lim=-\frac14$), \res{y=0}",
               r"Sin AV; \res{y=3} en $+\infty$ y \res{y=0} en $-\infty$",
               r"\res{x=0} ($\pm\infty$ por los lados); \res{y=1} en $+\infty$ y \res{y=-1} en $-\infty$",
               r"Dominio $(0,1)\cup(1,+\infty)$; $\lim_{x\to1}f=1$ (no es AV); \res{x=0} ($\to+\infty$); \res{y=0} en $+\infty$"])),
 (2, r"\pau{Andalucía, ordinaria 2020} Estudia las asíntotas y la monotonía de $f(x)=\dfrac{x^2-2x-3}{x^2-1}$.",
     r"$f=\frac{(x-3)(x+1)}{(x-1)(x+1)}=\frac{x-3}{x-1}$ si $x\neq-1$: AV \res{x=1} (en $x=-1$, agujero); AH \res{y=1}. $f'=\frac{2}{(x-1)^2}>0$: \rest{siempre creciente}."),
 (2, r"\pau{País Vasco, junio 2018} Asíntotas, monotonía y extremos de $f(x)=\dfrac{x^2}{x^2-4}$.",
     r"AV \res{x=\pm2}, AH \res{y=1}. $f'=\frac{-8x}{(x^2-4)^2}$: crece en $(-\infty,-2)\cup(-2,0)$, decrece en $(0,2)\cup(2,+\infty)$; \res{\text{máximo }(0,0)}."),
 (2, r"\pau{Cantabria, septiembre 2019} Dominio, asíntotas, monotonía y extremos de $f(x)=\dfrac{x+4}{x^2-7x-8}$.",
     r"Dominio $\mathbb R-\{-1,8\}$; AV \res{x=-1,\ x=8}, AH \res{y=0}. $f'=\frac{-(x+10)(x-2)}{(x^2-7x-8)^2}$: decrece en $(-\infty,-10)\cup(2,8)\cup(8,+\infty)$, crece en $(-10,-1)\cup(-1,2)$; \res{\text{mín. en }x=-10}, \res{\text{máx. en }x=2}."),
 (2, r"\pau{País Vasco, extraordinaria 2025} Asíntotas y monotonía de $f(x)=\dfrac{x}{x^2-3x-4}$, y recta tangente en $x=0$.",
     r"AV \res{x=-1,\ x=4}, AH \res{y=0}. $f'=\frac{-(x^2+4)}{(x^2-3x-4)^2}<0$: decreciente en todo el dominio. Tangente: \res{y=-\frac x4}."),
 (3, r"\pau{La Rioja, junio 2018} Sea $f(x)=x\,e^{-ax}$. Estudia sus asíntotas según los valores de $a$ y halla $a$ para que tenga un extremo relativo en $x=1$. ¿Es máximo o mínimo?",
     r"Sin AV ni AO. Si $a>0$: AH $y=0$ solo cuando $x\to+\infty$; si $a<0$: AH $y=0$ solo cuando $x\to-\infty$; si $a=0$ ($f=x$), ninguna. $f'=(1-ax)e^{-ax}$, $f'(1)=0\Rightarrow\res{a=1}$, y es un \rest{máximo} ($f'$ pasa de $+$ a $-$)."),
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
sec("Asíntotas oblicuas y ramas parabólicas",
 (1, r"Calcula todas las asíntotas de:" + tasks(1, [r"\pau{Andalucía, junio 2017} $f(x)=\dfrac{x^2}{x-1}$ (halla también sus extremos).", r"\pau{Asturias, extraordinaria 2020} $f(x)=\dfrac{2x^3+1}{x^2}$ (y los extremos)."])
     + recorda(r"$m=\displaystyle\lim_{x\to\pm\infty}\frac{f(x)}{x}$ (finito y $\neq0$), $n=\displaystyle\lim_{x\to\pm\infty}\big(f(x)-mx\big)$. En las racionales, la AO es el cociente de la división."),
     tasks(1, [r"$f=x+1+\frac{1}{x-1}$: AV \res{x=1}, AO \res{y=x+1}. $f'=\frac{x(x-2)}{(x-1)^2}$: \res{\text{máx. }(0,0)}, \res{\text{mín. }(2,4)}",
               r"$f=2x+\frac{1}{x^2}$: AV \res{x=0} ($\to+\infty$ por los dos lados), AO \res{y=2x}. $f'=2-\frac{2}{x^3}$: \res{\text{mín. }(1,3)}; crece en $(-\infty,0)\cup(1,+\infty)$"])),
 (2, r"\pau{Cantabria, ordinaria 2025} Sea $f(x)=\dfrac{x^3-8}{x^2-4}$ si $x\neq2$ y $f(2)=e^k$." + tasks(1, [r"Halla $k$ para que sea continua en $x=2$.", r"Calcula sus asíntotas.", r"Escribe la recta tangente en $x=1$."]),
     tasks(1, [r"$f=\frac{x^2+2x+4}{x+2}\to3$: $e^k=3\Rightarrow\res{k=\ln3}$", r"AV \res{x=-2}; sin AH; $f=x+\frac{4}{x+2}$: AO \res{y=x}", r"$f(1)=\frac73$, $f'(1)=1-\frac49=\frac59$: \res{y=\frac59x+\frac{16}9}"])),
 (2, r"\pau{Canarias, ordinaria 2021} Sea $f(x)=\dfrac{ax^2-2}{b-x}$." + tasks(1, [r"Halla $a$ y $b$ para que $f(-2)=2$ y $f$ sea continua en $\mathbb R-\{5\}$.", r"Para $a=-1$, $b=-3$, calcula las asíntotas."]),
     tasks(1, [r"$b=5$ y $\frac{4a-2}{7}=2\Rightarrow\res{a=4,\ b=5}$", r"$f=\frac{x^2+2}{x+3}=x-3+\frac{11}{x+3}$: AV \res{x=-3}, AO \res{y=x-3}"])),
 (2, r"\pau{Castilla y León, julio 2018} Halla $a$ y $b$ para que $f(x)=\dfrac1x+ax+b$ tenga un mínimo relativo en $\left(\frac12,6\right)$ y, con estos valores, halla sus asíntotas.",
     r"$f'\left(\frac12\right)=-4+a=0\Rightarrow\res{a=4}$; $f\left(\frac12\right)=2+2+b=6\Rightarrow\res{b=2}$. AV \res{x=0}, AO \res{y=4x+2}."),
 (3, r"\pau{La Rioja, julio 2018} Halla $a$ para que $\displaystyle\lim_{x\to+\infty}\left(\sqrt{9x^2+ax+1}-(3x-1)\right)=2$. ¿Cuál es, entonces, la asíntota oblicua de $y=\sqrt{9x^2+ax+1}$ en $+\infty$?",
     r"$\lim\frac{ax+1}{\sqrt{9x^2+ax+1}+3x}+1=\frac a6+1=2\Rightarrow\res{a=6}$. La asíntota es $y=3x-1+2$: \res{y=3x+1}."),
 (2, r"Estudia las ramas infinitas (asíntotas o ramas parabólicas) de:" + tasks(2, [r"$f(x)=\sqrt x$", r"$f(x)=x+\sqrt x$", r"$f(x)=x\ln x$", r"$f(x)=\sqrt{x^2+x+1}-x$"]),
     tasks(1, [r"$\frac fx\to0$: rama parabólica en la dirección de \rest{OX}", r"$m=1$, $n=\lim\sqrt x=+\infty$: rama en la dirección de \res{y=x}", r"$\frac fx=\ln x\to+\infty$: rama en la dirección de \rest{OY}",
               r"$+\infty$: $\frac{x+1}{\sqrt{x^2+x+1}+x}\to\frac12$, AH \res{y=\frac12}; $\ -\infty$: $m=-2$, $n=-\frac12$, AO \res{y=-2x-\frac12}"])),
 (2, r"Halla $b$ para que $f(x)=\dfrac{2x^2+bx}{x+1}$ tenga la asíntota oblicua $y=2x-1$.",
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
sec("Monotonía, extremos y curvatura",
 (1, r"\pau{Cataluña, extraordinaria 2022} Sea $f(x)=\dfrac{9}{x^2+x-2}$. Determina su dominio, las asíntotas, los extremos relativos y los intervalos de crecimiento y decrecimiento."
     + recorda(r"Tabla de signos de $f'$ con los ceros de $f'$ y los puntos que no son del dominio; $f''$ para la curvatura."),
     r"Dominio $\mathbb R-\{-2,1\}$; AV \res{x=-2,\ x=1}, AH \res{y=0}. $f'=\frac{-9(2x+1)}{(x^2+x-2)^2}$: crece en $(-\infty,-2)\cup\left(-2,-\frac12\right)$, decrece en $\left(-\frac12,1\right)\cup(1,+\infty)$; \res{\text{máx. }\left(-\tfrac12,-4\right)}."),
 (2, r"\pau{Extremadura, ordinaria 2021} Asíntotas, monotonía, extremos relativos y puntos de inflexión de $f(x)=e^{-x^2}$.",
     r"AH \res{y=0}. $f'=-2xe^{-x^2}$: crece en $(-\infty,0)$, decrece en $(0,+\infty)$; \res{\text{máx. }(0,1)}. $f''=(4x^2-2)e^{-x^2}$: \res{\text{P.I. en }x=\pm\tfrac{1}{\sqrt2}}."),
 (2, r"Estudia la monotonía, los extremos y la curvatura de $f(x)=x^4-4x^3$." ,
     r"$f'=4x^2(x-3)$: decrece en $(-\infty,3)$, crece en $(3,+\infty)$; \res{\text{mín. }(3,-27)} (en $x=0$, $f'=0$ sin extremo). $f''=12x(x-2)$: \res{\text{P.I. }(0,0)\text{ y }(2,-16)}; convexa en $(-\infty,0)\cup(2,+\infty)$."),
 (2, r"Estudia la monotonía y la curvatura de $f(x)=x^2\ln x$ y de $g(x)=\dfrac{x-1}{x^2}$.",
     r"$f'=x(2\ln x+1)$: \res{\text{mín. }\left(e^{-1/2},-\tfrac{1}{2e}\right)}; $f''=2\ln x+3$: P.I. en \res{x=e^{-3/2}}. \ $g'=\frac{2-x}{x^3}$: decrece en $(-\infty,0)\cup(2,+\infty)$, crece en $(0,2)$, \res{\text{máx. }\left(2,\tfrac14\right)}; $g''=\frac{2(x-3)}{x^4}$: \res{\text{P.I. }\left(3,\tfrac29\right)}."),
 (3, r"Halla $a$, $b$ y $c$ para que $f(x)=x^3+ax^2+bx+c$ tenga un punto de inflexión en $(1,2)$ con tangente de pendiente $-3$.",
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
sec("Representación de funciones polinómicas y racionales",
 (1, rep(r"\pau{País Vasco, julio 2019} " + fx(r'x^3+3x^2-2')) + REP,
     r"Dominio $\mathbb R$, sin asíntotas. $f'=3x(x+2)$: \res{\text{máx. }(-2,2)}, \res{\text{mín. }(0,-2)}. $f''=6x+6$: \res{\text{P.I. }(-1,0)}."
     + cen(graf([lambda v: v**3 + 3 * v**2 - 2], (-3.5, 1.8, -3, 3.5), mx=[(-2, 2)], mn=[(0, -2)], ip=[(-1, 0)]))),
 (2, rep(r"\pau{Asturias, extraordinaria 2024} " + fx(r'\dfrac{x^2-4}{1-x}')),
     r"Dominio $\mathbb R-\{1\}$, cortes $(\pm2,0)$, $(0,-4)$. AV \res{x=1}, AO \res{y=-x-1}. $f'=\frac{-x^2+2x-4}{(1-x)^2}<0$: \rest{decreciente}, sin extremos ni puntos de inflexión."
     + cen(graf([(lambda v: (v * v - 4) / (1 - v))], (-6, 7, -10, 10), va=[1], oa=[(-1, -1)], pts=[(-2, 0), (2, 0), (0, -4)]))),
 (2, rep(r"\pau{La Rioja, extraordinaria 2020} " + fx(r'\dfrac{x+3}{(x+2)^2}') + r" y calcula la recta tangente en el punto de inflexión"),
     r"AV \res{x=-2}, AH \res{y=0}. $f'=\frac{-(x+4)}{(x+2)^3}$: \res{\text{mín. }\left(-4,-\tfrac14\right)}. $f''=\frac{2(x+5)}{(x+2)^4}$: \res{\text{P.I. }\left(-5,-\tfrac29\right)}, tangente \res{x+27y+11=0}."
     + cen(graf([lambda v: (v + 3) / (v + 2)**2], (-9, 3, -1, 4), va=[-2], ha=[0], mn=[(-4, -0.25)], ip=[(-5, -2 / 9)], pts=[(-3, 0), (0, 0.75)]))),
 (2, rep(r"\pau{Comunidad Valenciana, extraordinaria 2025} " + fx(r'\dfrac{2x}{x^2+1}') + r" y calcula sus extremos absolutos"),
     r"Impar, AH \res{y=0}. $f'=\frac{2(1-x^2)}{(x^2+1)^2}$: \res{\text{mín. abs. }(-1,-1)}, \res{\text{máx. abs. }(1,1)}. $f''=\frac{4x(x^2-3)}{(x^2+1)^3}$: P.I. en $0$ y $\pm\sqrt3$."
     + cen(graf([lambda v: 2 * v / (v * v + 1)], (-6, 6, -1.5, 1.5), ha=[0], mx=[(1, 1)], mn=[(-1, -1)], ip=[(0, 0), (r3, r3 / 2), (-r3, -r3 / 2)]))),
 (3, rep(fx(r'\dfrac{x^3}{(x-1)^2}')),
     r"AV \res{x=1}; $f=x+2+\frac{3x-2}{(x-1)^2}$: AO \res{y=x+2}. $f'=\frac{x^2(x-3)}{(x-1)^3}$: crece en $(-\infty,1)\cup(3,+\infty)$, decrece en $(1,3)$, \res{\text{mín. }\left(3,\tfrac{27}{4}\right)}. $f''=\frac{6x}{(x-1)^4}$: \res{\text{P.I. }(0,0)}."
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
sec("Representación de funciones radicales",
 (1, r"Dominio, cortes y asíntotas de:" + tasks(2, [r"$f(x)=\sqrt{x^2-9}$", r"$f(x)=\dfrac{x+1}{\sqrt{x^2+3}}$"])
     + recorda(r"$\sqrt{x^2+bx+c}\approx|x|+\frac b2$ cuando $x\to\pm\infty$: las asíntotas pueden ser distintas en cada lado. Multiplica por el conjugado para calcular $n$."),
     tasks(1, [r"Dominio $(-\infty,-3]\cup[3,+\infty)$, cortes $(\pm3,0)$; AO \res{y=x} en $+\infty$ y \res{y=-x} en $-\infty$",
               r"Dominio $\mathbb R$, cortes $(-1,0)$ y $\left(0,\frac{1}{\sqrt3}\right)$; AH \res{y=1} en $+\infty$ y \res{y=-1} en $-\infty$"])),
 (2, rep(fx(r'\dfrac{x}{\sqrt{x-1}}')),
     r"Dominio $(1,+\infty)$; AV \res{x=1} ($\to+\infty$). $f'=\frac{x-2}{2(x-1)^{3/2}}$: \res{\text{mín. }(2,2)}. $f''=\frac{4-x}{4(x-1)^{5/2}}$: \res{\text{P.I. }\left(4,\tfrac{4}{\sqrt3}\right)}. Rama parabólica en la dirección de OX."
     + cen(graf([(lambda v: v / msq(v - 1), 1.0001, 12)], (-0.5, 12, -0.5, 6), va=[1], mn=[(2, 2)], ip=[(4, 4 / r3)]))),
 (2, rep(fx(r'x-3\sqrt[3]{x}')),
     r"Impar, cortes $(0,0)$ y $\left(\pm3\sqrt3,0\right)$. $f'=1-\frac{1}{\sqrt[3]{x^2}}$: \res{\text{máx. }(-1,2)}, \res{\text{mín. }(1,-2)}; en $x=0$ tangente vertical. $f''=\frac{2}{3\sqrt[3]{x^5}}$: \res{\text{P.I. }(0,0)} (con tangente vertical)."
     + cen(graf([lambda v: v - 3 * math.copysign(abs(v)**(1 / 3), v)], (-7, 7, -4, 4), mx=[(-1, 2)], mn=[(1, -2)], ip=[(0, 0)], pts=[(-3 * r3, 0), (3 * r3, 0)]))),
 (2, rep(fx(r'\dfrac{x+1}{\sqrt{x^2+3}}')),
     r"AH \res{y=1} ($+\infty$) y \res{y=-1} ($-\infty$). $f'=\frac{3-x}{(x^2+3)^{3/2}}$: crece en $(-\infty,3)$, decrece en $(3,+\infty)$; \res{\text{máx. abs. }\left(3,\tfrac{2}{\sqrt3}\right)}."
     + cen(graf([lambda v: (v + 1) / math.sqrt(v * v + 3)], (-10, 12, -1.5, 1.5), ha=[1, -1], mx=[(3, 2 / r3)], pts=[(-1, 0), (0, 1 / r3)]))),
 (3, r"Sea $f(x)=x\sqrt{4-x^2}$. Estudia su dominio, la simetría, los extremos absolutos y los puntos en los que la tangente es vertical, y represéntala.",
     r"Dominio $[-2,2]$, impar. $f'=\frac{2(2-x^2)}{\sqrt{4-x^2}}$: \res{\text{mín. abs. }\left(-\sqrt2,-2\right)}, \res{\text{máx. abs. }\left(\sqrt2,2\right)}; tangentes verticales en \res{x=\pm2}; P.I. $(0,0)$."
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
sec("Representación de funciones exponenciales y logarítmicas",
 (1, rep(r"\pau{Castilla y León, junio 2018} " + fx(r'x\,e^{-x}')) + REP,
     r"Corte $(0,0)$; AH \res{y=0} en $+\infty$. $f'=(1-x)e^{-x}$: \res{\text{máx. }\left(1,\tfrac1e\right)}. $f''=(x-2)e^{-x}$: \res{\text{P.I. }\left(2,\tfrac{2}{e^2}\right)}."
     + cen(graf([lambda v: v * me(-v)], (-1.5, 7, -2, 0.7), ha=[0], mx=[(1, 1 / math.e)], ip=[(2, 2 / math.e**2)]))),
 (2, rep(r"\pau{País Vasco, extraordinaria 2024} " + fx(r'2x\,e^{-2x^2}')),
     r"Impar, AH \res{y=0}. $f'=2(1-4x^2)e^{-2x^2}$: \res{\text{mín. }\left(-\tfrac12,-\tfrac{1}{\sqrt e}\right)}, \res{\text{máx. }\left(\tfrac12,\tfrac{1}{\sqrt e}\right)}. P.I. en $x=0$ y $x=\pm\frac{\sqrt3}{2}$."
     + cen(graf([lambda v: 2 * v * me(-2 * v * v)], (-2.5, 2.5, -0.9, 0.9), ha=[0], mx=[(0.5, 1 / math.sqrt(math.e))], mn=[(-0.5, -1 / math.sqrt(math.e))], ip=[(0, 0), (r3 / 2, r3 * me(-1.5)), (-r3 / 2, -r3 * me(-1.5))]))),
 (2, rep(r"\pau{Cantabria, extraordinaria 2022} " + fx(r'\dfrac{e^x}{x}')),
     r"AV \res{x=0}, AH \res{y=0} en $-\infty$. $f'=\frac{(x-1)e^x}{x^2}$: \res{\text{mín. }(1,e)}. $f''=\frac{e^x(x^2-2x+2)}{x^3}$: cóncava en $(-\infty,0)$, convexa en $(0,+\infty)$."
     + cen(graf([lambda v: me(v) / v], (-5, 3.5, -4, 10), va=[0], ha=[0], mn=[(1, math.e)]))),
 (2, rep(r"\pau{Cataluña, ordinaria 2021} " + fx(r'\dfrac{\ln x}{x}')),
     r"Dominio $(0,+\infty)$; AV \res{x=0}, AH \res{y=0}; corte $(1,0)$. $f'=\frac{1-\ln x}{x^2}$: \res{\text{máx. }\left(e,\tfrac1e\right)}. $f''=\frac{2\ln x-3}{x^3}$: \res{\text{P.I. en }x=e^{3/2}}."
     + cen(graf([(lambda v: mln(v) / v, 0.05, 20)], (-0.5, 20, -2, 0.8), va=[0], ha=[0], mx=[(math.e, 1 / math.e)], ip=[(math.e**1.5, 1.5 * math.e**-1.5)], pts=[(1, 0)]))),
 (2, rep(fx(r'\ln\left(x^2-4\right)')),
     r"Dominio $|x|>2$, par; AV \res{x=\pm2}; cortes $\left(\pm\sqrt5,0\right)$. $f'=\frac{2x}{x^2-4}$: decrece en $(-\infty,-2)$, crece en $(2,+\infty)$; sin extremos. $f''=\frac{-2(x^2+4)}{(x^2-4)^2}<0$: cóncava."
     + cen(graf([(lambda v: mlog(v * v - 4), -9, -2.0001), (lambda v: mlog(v * v - 4), 2.0001, 9)], (-8, 8, -4, 5), va=[-2, 2], pts=[(-math.sqrt(5), 0), (math.sqrt(5), 0)]))),
 (2, r"\pau{Castilla y León, ordinaria 2023} Dominio, monotonía y extremos de $f(x)=x(\ln x-1)$. ¿Cómo es la gráfica cerca de $x=0$?",
     r"Dominio $(0,+\infty)$. $f'=\ln x$: decrece en $(0,1)$, crece en $(1,+\infty)$; \res{\text{mín. }(1,-1)}. Corte $(e,0)$. $\lim_{x\to0^+}f=0$: la gráfica \rest{sale del origen} (sin AV)."),
)

# =====================================================================
# 10. Trigonomètriques
f_ = sin(x) * (1 + cos(x)); crit(f_, [pi / 3, pi, 5 * pi / 3], 0.001, 2 * math.pi - 0.001); ext(f_, pi / 3, 'max', 3 * sq(3) / 4); ext(f_, 5 * pi / 3, 'min', -3 * sq(3) / 4)
f_ = sin(x)**2 + cos(x); ext(f_, pi / 3, 'max', R(5, 4)); ext(f_, pi, 'min', -1); ext(f_, 0, 'min', 1); parity(f_, 'even')
f_ = tan(x) - 2 * x; ext(f_, pi / 4, 'min', 1 - pi / 2); ext(f_, -pi / 4, 'max', pi / 2 - 1); parity(f_, 'odd')
f_ = (1 - cos(x)) / x; L(f_, 0, 0); asy_h(f_, 0)
f_ = x + cos(x); infl(f_, pi / 2); infl(f_, 3 * pi / 2)
sec("Representación de funciones trigonométricas",
 (2, rep(fx(r'\sin x\,(1+\cos x)')) + recorda(r"Si es periódica, estúdiala en un período. Factoriza $f'$ con las identidades ($\cos2x=2\cos^2x-1$…)."),
     r"Período $2\pi$, impar. $f'=\cos x+\cos2x=(2\cos x-1)(\cos x+1)$: ceros $\frac\pi3$, $\pi$, $\frac{5\pi}3$. \res{\text{máx. }\left(\tfrac\pi3,\tfrac{3\sqrt3}4\right)}, \res{\text{mín. }\left(\tfrac{5\pi}3,-\tfrac{3\sqrt3}4\right)} ($+2k\pi$); en $x=\pi$, $f'=0$ sin extremo."
     + cen(graf([lambda v: ms(v) * (1 + mc(v))], (-1, 7.3, -1.6, 1.6), mx=[(PI / 3, 3 * r3 / 4)], mn=[(5 * PI / 3, -3 * r3 / 4)], pts=[(0, 0), (PI, 0), (2 * PI, 0)], xt=PIX))),
 (2, rep(fx(r'\sin^2x+\cos x') + r" en $[0,2\pi]$"),
     r"Par, período $2\pi$. $f'=\sin x\,(2\cos x-1)$: \res{\text{máx. }\left(\tfrac\pi3,\tfrac54\right)\text{ y }\left(\tfrac{5\pi}3,\tfrac54\right)}, \res{\text{mín. }(\pi,-1)}; en $x=0$ y $x=2\pi$, mínimos relativos de valor 1."
     + cen(graf([(lambda v: ms(v)**2 + mc(v), 0, 2 * PI)], (-0.4, 6.8, -1.3, 1.6), mx=[(PI / 3, 1.25), (5 * PI / 3, 1.25)], mn=[(PI, -1), (0, 1), (2 * PI, 1)], xt=PIX))),
 (2, r"Estudia $f(x)=\tan x-2x$ en $\left(-\frac\pi2,\frac\pi2\right)$: asíntotas, extremos y curvatura.",
     r"Impar; AV \res{x=\pm\frac\pi2}. $f'=\frac{1}{\cos^2x}-2=0\Leftrightarrow\cos^2x=\frac12$: \res{\text{máx. }\left(-\tfrac\pi4,\tfrac\pi2-1\right)}, \res{\text{mín. }\left(\tfrac\pi4,1-\tfrac\pi2\right)}. $f''=\frac{2\sin x}{\cos^3x}$: \res{\text{P.I. }(0,0)}."
     + cen(graf([(lambda v: mt(v) - 2 * v, -PI / 2 + 0.01, PI / 2 - 0.01)], (-1.8, 1.8, -4, 4), va=[-PI / 2, PI / 2], mx=[(-PI / 4, PI / 2 - 1)], mn=[(PI / 4, 1 - PI / 2)], ip=[(0, 0)]))),
 (2, r"\pau{Cantabria, extraordinaria 2020} Sea $f(x)=\dfrac{1-\cos x}{x}$. Calcula $\displaystyle\lim_{x\to0}f(x)$ y las asíntotas de $f$.",
     r"$\left[\frac00\right]\overset{\text{L'H}}{=}\lim\frac{\sin x}{1}=\res{0}$: no hay AV. Como $0\leq1-\cos x\leq2$, $\left|f\right|\leq\frac2{|x|}\to0$: AH \res{y=0} (en ambos lados); sin AO."),
 (2, r"Estudia la monotonía y la curvatura de $f(x)=x+\cos x$ en $[0,2\pi]$ y represéntala.",
     r"$f'=1-\sin x\geq0$: \rest{creciente} (con tangente horizontal en $\frac\pi2$). $f''=-\cos x$: \res{\text{P.I. en }\tfrac\pi2\text{ y }\tfrac{3\pi}2}; cóncava en $\left(0,\frac\pi2\right)\cup\left(\frac{3\pi}2,2\pi\right)$."
     + cen(graf([(lambda v: v + mc(v), 0, 2 * PI)], (-0.4, 6.8, -0.5, 7.5), ip=[(PI / 2, PI / 2), (3 * PI / 2, 3 * PI / 2)], pts=[(0, 1), (2 * PI, 2 * PI + 1)], xt=PIX))),
)
crit(sin(x)**2 + cos(x), [pi / 3, pi, 5 * pi / 3], 0.001, 2 * math.pi - 0.001)

# =====================================================================
# 11. A trossos, valor absolut i transformacions
f_ = sp.Abs(x**2 - 2 * x - 3); eq(f_.subs(x, 1), 4)
f_ = x**2 - 4 * sp.Abs(x) + 3; eq(f_.subs(x, 2), -1); eq(f_.subs(x, 0), 3); ok(sorted(sp.solve(x**2 - 4 * x + 3, x)) == [1, 3])
ok(sp.solve([9 * a_ + b_ - ln(1), 6 * a_ - 1], [a_, b_]) == {a_: R(1, 6), b_: -R(3, 2)})
L(x * ln(x), 0, 0, '+'); L(sp.diff(x * ln(x), x), 0, -sp.oo, '+'); ext(x * ln(x), 1 / E, 'min', -1 / E)
sec("Funciones a trozos, con valor absoluto y transformaciones",
 (1, r"Escribe a trozos y representa:" + tasks(2, [r"$f(x)=\left|x^2-2x-3\right|$", r"$f(x)=x^2-4|x|+3$", r"$f(x)=e^{-|x|}$", r"$f(x)=|x|\,(x-2)$"])
     + recorda(r"$|g(x)|=g(x)$ si $g(x)\geq0$ y $-g(x)$ si $g(x)<0$. Los cambios de trozo suelen ser puntos angulosos."),
     tasks(2, [r"Mínimos angulosos $(-1,0)$, $(3,0)$; \res{\text{máx. }(1,4)}" + cen(graf([lambda v: abs(v * v - 2 * v - 3)], (-2.5, 4.5, -0.5, 6), mn=[(-1, 0), (3, 0)], mx=[(1, 4)], w=4.6, h=3.2)),
               r"Par: \res{\text{mín. }(\pm2,-1)}, \res{\text{máx. anguloso }(0,3)}" + cen(graf([lambda v: v * v - 4 * abs(v) + 3], (-4.5, 4.5, -1.5, 4), mn=[(-2, -1), (2, -1)], mx=[(0, 3)], pts=[(-3, 0), (-1, 0), (1, 0), (3, 0)], w=4.6, h=3.2)),
               r"Par, AH $y=0$, \res{\text{máx. anguloso }(0,1)}" + cen(graf([lambda v: me(-abs(v))], (-4, 4, -0.3, 1.3), ha=[0], mx=[(0, 1)], w=4.6, h=3.2)),
               r"$-x^2+2x$ si $x<0$, $x^2-2x$ si $x\geq0$: \res{\text{máx. anguloso }(0,0)}, \res{\text{mín. }(1,-1)}" + cen(graf([lambda v: abs(v) * (v - 2)], (-2, 3.5, -3, 2), mx=[(0, 0)], mn=[(1, -1)], pts=[(2, 0)], w=4.6, h=3.2))])),
 (2, r"A partir de las gráficas de las funciones elementales, dibuja:" + tasks(2, [r"$y=\sqrt{x+4}-2$", r"$y=-\sqrt{-x}$", r"$y=2-e^{-x}$", r"$y=\left|\ln(x+1)\right|$"]),
     tasks(1, [r"$\sqrt x$ trasladada 4 a la izquierda y 2 hacia abajo: empieza en $(-4,-2)$ y pasa por \res{(0,0)}", r"$\sqrt x$ con simetrías respecto a OY y a OX (respecto al origen): dominio $(-\infty,0]$",
               r"$e^x$ $\to$ $e^{-x}$ (simetría OY) $\to$ $-e^{-x}$ (simetría OX) $\to$ $+2$: AH \res{y=2} en $+\infty$, corte \res{(0,1)}", r"$\ln(x+1)$ (AV $x=-1$) con la parte negativa reflejada: \res{\text{mín. anguloso }(0,0)}"])),
 (2, r"\pau{Galicia, junio 2017} Calcula $a$ y $b$ para que sea derivable en $x=3$ la función $f(x)=\begin{cases}ax^2+b&\text{si }x<3\\ \ln(x-2)&\text{si }x\geq3\end{cases}$ y represéntala.",
     r"Continua: $9a+b=\ln1=0$; derivable: $6a=\frac{1}{3-2}=1$. \res{a=\frac16,\ b=-\frac32}. Parábola de vértice $\left(0,-\frac32\right)$ hasta $(3,0)$ y después $\ln(x-2)$, sin ángulo."
     + cen(graf([(lambda v: v * v / 6 - 1.5, -5, 3), (lambda v: mlog(v - 2), 3, 9)], (-4.5, 9, -2, 3), mn=[(0, -1.5)], pts=[(3, 0), (-3, 0)]))),
 (3, r"\pau{Madrid, extraordinaria 2022} Sea $f(x)=\begin{cases}x&\text{si }x\leq0\\ x\ln x&\text{si }x>0\end{cases}$." + tasks(1, [r"Estudia la continuidad y la derivabilidad en $x=0$.", r"Estudia su monotonía y sus extremos relativos, y represéntala."]),
     tasks(1, [r"$\lim_{x\to0^+}x\ln x=0=f(0)$: \rest{continua}. $f'(0^-)=1$ y $f'(0^+)=\lim(\ln x+1)=-\infty$: \rest{no derivable}.",
               r"Crece en $(-\infty,0)$, decrece en $\left(0,\frac1e\right)$, crece en $\left(\frac1e,+\infty\right)$: \res{\text{máx. }(0,0)} (no derivable), \res{\text{mín. }\left(\tfrac1e,-\tfrac1e\right)}."
               + cen(graf([(lambda v: v, -3, 0), (lambda v: v * mlog(v), 0.0001, 3)], (-2.5, 2.8, -1.5, 2), mx=[(0, 0)], mn=[(1 / math.e, -1 / math.e)], pts=[(1, 0)]))])),
)

# =====================================================================
# 12. Gràfiques de f, f' i f''
fp = (x - 1)**2 * (x + 2); ok(sp.expand(sp.diff(fp, x) - 3 * (x - 1) * (x + 1)) == 0)
g_ = a_ * x**3 + b_ * x**2 + 1; ok(sp.solve([sp.diff(g_, x, 2).subs(x, R(1, 2)), sp.diff(g_, x).subs(x, R(1, 2)) + R(3, 2)], [a_, b_]) == {a_: 2, b_: -3})
p_ = a_ * x**3 + b_ * x**2 + c_ * x + d_; ok(sp.solve([sp.diff(p_, x).subs(x, -1), sp.diff(p_, x).subs(x, 2), p_.subs(x, 0) - 1, p_.subs(x, 2) + 19], [a_, b_, c_, d_]) == {a_: 2, b_: -3, c_: -12, d_: 1})
sec("Información a partir de las gráficas de f, f' y f''",
 (2, r"Sabemos que $f'(x)=(x-1)^2(x+2)$. Sin calcular $f$, estudia su monotonía, los extremos y la curvatura, y dibuja una gráfica posible."
     + recorda(r"$f'>0\Rightarrow f$ crece; cambio de signo de $f'$ $\Rightarrow$ extremo; $f'$ crece ($f''>0$) $\Rightarrow f$ convexa; extremo de $f'$ $\Rightarrow$ inflexión de $f$."),
     r"$f'\geq0$ si $x>-2$: decrece en $(-\infty,-2)$, crece en $(-2,+\infty)$; \res{\text{mín. en }x=-2}; en $x=1$, \rest{inflexión con tangente horizontal}. $f''=3(x-1)(x+1)$: convexa en $(-\infty,-1)\cup(1,+\infty)$, cóncava en $(-1,1)$; \res{\text{P.I. en }x=\pm1}."),
 (2, r"\pau{Cataluña, extraordinaria 2021} Calcula $a$ y $b$ para que $g(x)=ax^3+bx^2+1$ tenga un punto de inflexión en $x=\frac12$ y su derivada en ese punto sea $-\frac32$.",
     r"$g''\left(\frac12\right)=3a+2b=0$, $g'\left(\frac12\right)=\frac{3a}4+b=-\frac32$: \res{a=2,\ b=-3}."),
 (2, r"La gráfica de la derivada de un polinomio $p$ de grado 3 es una parábola que corta el eje OX en $x=-1$ y $x=2$. Si $p(0)=1$ y $p(2)=-19$, halla $p$ y di dónde tiene los extremos y el punto de inflexión.",
     r"$p'=k(x+1)(x-2)=k(x^2-x-2)\Rightarrow p=k\left(\frac{x^3}3-\frac{x^2}2-2x\right)+1$; $p(2)=-\frac{10k}3+1=-19\Rightarrow k=6$: \res{p(x)=2x^3-3x^2-12x+1}. Máx. en \res{x=-1}, mín. en \res{x=2}, P.I. en \res{x=\frac12}."),
 (2, r"\pau{Galicia, extraordinaria 2026} Dibuja la gráfica de una función $f:\mathbb R-\{2\}\to\mathbb R$ tal que $f$, $f'$ y $f''$ tengan el mismo signo en $(-1,2)$ y $\displaystyle\lim_{x\to2^+}f(x)=-\infty$. Explica el dibujo.",
     r"Por ejemplo, \res{f(x)=\frac{1}{2-x}}: en $(-1,2)$ es positiva, creciente ($f'>0$) y convexa ($f''>0$); tiene la AV $x=2$ ($+\infty$ por la izquierda, $-\infty$ por la derecha) y la AH $y=0$."
     + cen(graf([lambda v: 1 / (2 - v)], (-3, 6, -5, 5), va=[2], ha=[0]))),
 (3, r"\pau{Galicia, ordinaria 2022} Dibuja la gráfica de una función continua y no negativa en $[0,3]$ tal que $f(0)=f(3)=0$, $f''>0$ en $(0,1)$, $f''<0$ en $(2,3)$ y constante en $(1,2)$. ¿Puede ser derivable en $x=1$?",
     r"Por ejemplo, \res{x^2} en $[0,1]$, \res{1} en $[1,2]$ y \res{1-(x-2)^2} en $[2,3]$. En $x=1$ \rest{no} puede ser derivable: si es convexa y sube desde $(0,0)$, la pendiente es positiva y creciente y no puede valer 0 en $x=1$."
     + cen(graf([(lambda v: v * v, 0, 1), (lambda v: 1, 1, 2), (lambda v: 1 - (v - 2)**2, 2, 3)], (-0.4, 3.4, -0.3, 1.4), pts=[(0, 0), (3, 0)]))),
)

# =====================================================================
print(NCHK[0], 'comprobaciones correctas')
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Representación gráfica de funciones"
def build(sol):
    tt = 'Soluciones de la ficha' if sol else "Ficha de ejercicios"
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    p = preambul(pre, pdftitle='%s de la unidad 8: %s' % (tt, TIT), capcalera='%s · Unidad 8: %s' % (tt, TIT),
                 pdfkeywords='representación de funciones, dominio, simetrías, periodicidad, asíntotas, ramas parabólicas, monotonía, curvatura, funciones radicales, trigonométricas, a trozos, transformaciones, PAU', curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 8' if sol else "Ficha de ejercicios · Unidad 8") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.2cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Las gráficas de las soluciones marcan en verde los máximos, en rojo los mínimos y en violeta los puntos de inflexión; las líneas discontinuas son asíntotas. Puedes comprobar los estudios completos con la calculadora de los apuntes interactivos."
             if sol else r"Resuelve los ejercicios en el cuaderno justificando cada paso. Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de la Comunidad Valenciana y de otras comunidades autónomas, traducidos al castellano. Puedes comprobar los resultados con las herramientas de los apuntes interactivos (dominios, asíntotas, estudio completo de una función paso a paso, transformaciones\dots).") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus estudios con las herramientas de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't8-fitxa-solucions-es.tex' if sol else 't8-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'ejercicios,', npau, 'de la PAU de', len(regs), 'comunidades:', ', '.join(regs))
