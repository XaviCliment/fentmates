# Versió en castellà de genera.py. Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 7: Aplicacions de la
# derivada) a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les
# estrelles no es mostren. Les seccions segueixen els apunts interactius (materials/2batx-mii/t7-aplicacions-derivada.html).
# Els exercicis marcats amb \pau{...} són de la PAU de València i d'altres comunitats, traduïts al valencià i presos del
# recull «Ejercicios de análisis en pruebas de acceso a la universidad de toda España» (curs 2026/27) de Juan Antonio
# Martínez García (www.ebaumatematicas.com). Les gràfiques de les solucions es calculen ací mateix i es dibuixen amb TikZ com
# a poligonals (graf), com a la unitat 7 de CCSS. Abans d'escriure els fitxers, sympy comprova tots els límits, tangents,
# extrems, punts d'inflexió, paràmetres i òptims de les solucions.
# Ús: python3 genera.py && pdflatex t7-fitxa-exercicis.tex (dues vegades) && pdflatex t7-fitxa-solucions.tex (dues vegades)
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

# =====================================================================
# 1. Rectes tangent i normal
g_ = x**2 - 2 * x - 4; eq(g_.subs(x, -3), 11); eq(sp.diff(g_, x).subs(x, -3), -8)
tang(ln(2 * x + 1), R(1, 2), 1, ln(2) - R(1, 2)); tang(exp(-2 * x), 0, -2, 1)
tang(x**2 + x, 1, 3, -1)
f_ = exp(x) / (x**3 - x); tang(f_, 2, -5 * E**2 / 36, 4 * E**2 / 9)
f_ = 1 / (1 + x**2); d1 = sp.diff(f_, x); ok(sp.solve(d1, x) == [0])
ok(sorted(sp.solve(sp.diff(d1, x), x)) == [-1 / sq(3), 1 / sq(3)]); eq(d1.subs(x, -1 / sq(3)), 9 / (8 * sq(3))); eq(f_.subs(x, -1 / sq(3)), R(3, 4))
f_ = 1 / (3 + x**2); d1 = sp.diff(f_, x); ok(sorted(sp.solve(sp.diff(d1, x), x)) == [-1, 1]); eq(d1.subs(x, -1), R(1, 8))
f_ = x**3 - 3 * x; ok(sp.solve(f_.subs(x, a_) + sp.diff(f_, x).subs(x, a_) * (0 - a_) - 2, a_) == [-1])
ok(sp.solve(sp.discriminant(x**2 - 4 * x + 10 - (2 * x + a_), x), a_) == [1])
f_ = x**2 / 4 + 4 * x + 4; ok(sorted(sp.solve(f_.subs(x, a_) - a_ * sp.diff(f_, x).subs(x, a_), a_)) == [-4, 4]); tang(f_, -4, 2, 0); tang(f_, 4, 6, 0)
tang(x**2, 2, 4, -4)
sec("Rectas tangente y normal",
 (1, r"Calcula:" + tasks(1, [r"\pau{Castilla-La Mancha, junio 2017} La recta normal a la gráfica de $g(x)=x^2-2x-4$ en el punto de abscisa $x=-3$.",
                              r"\pau{Aragón, ordinaria 2020} La recta tangente a $f(x)=\ln(2x+1)$ en $x=\frac12$.",
                              r"\pau{Cataluña, extraordinaria 2024} La recta tangente a $y=e^{-2x}$ en $x=0$ y el punto donde corta el eje de abscisas.",
                              r"\pau{Aragón, extraordinaria 2021} La recta tangente a $f(x)=\dfrac{e^x}{x^3-x}$ en $x=2$."])
     + recorda(r"Tangente: $y-f(a)=f'(a)(x-a)$. Normal: $y-f(a)=-\dfrac{1}{f'(a)}(x-a)$."),
     tasks(1, [r"$g(-3)=11$, $g'(-3)=-8\Rightarrow m_n=\frac18$: $y-11=\frac18(x+3)\Rightarrow\res{x-8y+91=0}$",
               r"$f\left(\frac12\right)=\ln2$, $f'(x)=\frac{2}{2x+1}=1$: $\res{y=x-\frac12+\ln2}$",
               r"$y'(0)=-2$: $\res{y=-2x+1}$, que corta el eje en $\res{\left(\frac12,0\right)}$",
               r"$f(2)=\frac{e^2}{6}$, $f'(x)=\frac{e^x(x^3-3x^2-x+1)}{(x^3-x)^2}\Rightarrow f'(2)=-\frac{5e^2}{36}$: $\res{y=-\frac{5e^2}{36}x+\frac{4e^2}{9}}$"])),
 (2, r"\pau{Cataluña, septiembre 2019} Considera la función $f(x)=\dfrac{1}{1+x^2}$." + tasks(1, [r"Calcula la ecuación de la recta tangente a la gráfica en los puntos en los que es horizontal.", r"Calcula las coordenadas del punto de la gráfica en el que la pendiente de la recta tangente es máxima."])
     + recorda(r"La pendiente de la tangente es $m(x)=f'(x)$: para hacerla máxima, derivamos $f'$ e igualamos a cero (es decir, $f''(x)=0$)."),
     tasks(1, [r"$f'(x)=\frac{-2x}{(1+x^2)^2}=0\Leftrightarrow x=0$: $\res{y=1}$",
               r"$f''(x)=\frac{6x^2-2}{(1+x^2)^3}=0\Leftrightarrow x=\pm\frac{1}{\sqrt3}$; $f'$ es máxima en $x=-\frac{1}{\sqrt3}$ $\left(f'=\frac{9}{8\sqrt3}>0\right)$: $\res{\left(-\frac{1}{\sqrt3},\frac34\right)}$"])),
 (2, r"\pau{Asturias, junio 2019} Dada la curva $y=\dfrac{1}{3+x^2}$, escribe la función $m(x)$ que da la pendiente de la recta tangente en cada punto y halla en qué $x$ la pendiente es máxima.",
     r"$m(x)=\dfrac{-2x}{(3+x^2)^2}$, \ $m'(x)=\dfrac{6x^2-6}{(3+x^2)^3}=0\Leftrightarrow x=\pm1$; \ $m'$ pasa de $+$ a $-$ en $x=-1$: \ pendiente máxima en $\res{x=-1}$ \ $\left(m(-1)=\frac18\right)$."),
 (2, r"\pau{La Rioja, ordinaria 2022} Dada la curva $f(x)=\frac14x^2+4x+4$, halla los puntos en los que la recta tangente pasa por el origen y escribe sus ecuaciones."
     + recorda(r"Si el punto no es de la curva, escribe la tangente en un punto genérico $(a,f(a))$ e impón que pase por el punto dado."),
     r"$0-f(a)=f'(a)(0-a)\Rightarrow-\frac{a^2}{4}-4a-4=-\frac{a^2}{2}-4a\Rightarrow a^2=16$: \ $\res{A(-4,-8)}$, tangente $\res{y=2x}$; \ $\res{B(4,24)}$, tangente $\res{y=6x}$."),
 (2, r"¿Cuántas rectas tangentes a $f(x)=x^3-3x$ pasan por el punto $(0,2)$? Escríbelas.",
     r"$2-(a^3-3a)=(3a^2-3)(0-a)\Rightarrow 2=-2a^3\Rightarrow a=-1$: solo \rest{una}, la tangente en $(-1,2)$, que es \res{y=2} (horizontal)."),
 (2, r"Halla $a$ para que la recta $y=2x+a$ sea tangente a la parábola $f(x)=x^2-4x+10$. ¿En qué punto?"
     + recorda(r"Una recta es tangente a una parábola si, al cortarlas, la ecuación de segundo grado tiene una raíz doble (discriminante cero)."),
     r"$x^2-4x+10=2x+a\Leftrightarrow x^2-6x+10-a=0$; \ $\Delta=36-4(10-a)=0\Rightarrow\res{a=1}$, en $\res{(3,7)}$ (también: $f'(x)=2x-4=2\Rightarrow x=3$)."),
 (2, r"\pau{Galicia, extraordinaria 2022} Halla los vértices del triángulo rectángulo que tiene la hipotenusa sobre la recta tangente a $f(x)=x^2$ en $x=2$ y un cateto de longitud 2 sobre el eje $X$ (a la derecha del punto donde la tangente corta el eje).",
     r"Tangente: $y=4x-4$, corta el eje en $(1,0)$. Vértices: $\res{A(1,0),\ B(3,0),\ C(3,8)}$."),
)

# =====================================================================
# 2. Regla de L'Hôpital
L((x - 1) / (exp(x - 1) - 1), 1, 1); L((exp(x - 2) - 1) / (2 * x - 4), 2, R(1, 2)); L(x * cos(x) / sin(x), 0, 1)
L(ln(cos(x) + sin(x)) / x, 0, 1); L((sin(2 * x**2) + x) / (ln(x + 1) + x), 0, R(1, 2)); L(x * sin(x) / (2 - 2 * cos(x)), 0, 1)
L(x**3 / exp(2 * x), sp.oo, 0); L(ln(x)**2 / x, sp.oo, 0); L(ln(sin(x)) / ln(x), 0, 1, '+'); L((exp(x) - 1) / (x**2 + 3), sp.oo, sp.oo)
L((x**2 - sin(x**2)) / (1 - cos(x)), 0, 0)
ok(sp.solve(sp.series(ln(x + 1) - a_ * sin(x) + 3 * x * cos(2 * x), x, 0, 2).removeO().coeff(x, 1), a_) == [4]); L((ln(x + 1) - 4 * sin(x) + 3 * x * cos(2 * x)) / x**2, 0, -R(1, 2))
L((1 - cos(2 * x)) / x**2, 0, 2)
ok(sp.solve([a_ + b_, a_ - 3], [a_, b_]) == {a_: 3, b_: -3}); L((3 * exp(x) - 3) / x, 0, 3)
Nn = 2 * x**3 + a_ * x**2 + b_ * x + 3; ok(sp.solve([Nn.subs(x, 1), sp.diff(Nn, x).subs(x, 1)], [a_, b_]) == {a_: -1, b_: -4})
L((2 * x**3 - x**2 - 4 * x + 3) / (-x**3 + 4 * x**2 - 5 * x + 2), 1, 5)
L((x**2 + 1) / (x + 1), 1, 1)
sec("Regla de L'Hôpital",
 (1, r"Calcula los límites siguientes:" + tasks(2, [r"\pau{Castilla-La Mancha, extraordinaria 2021} $\displaystyle\lim_{x\to1}\frac{x-1}{e^{x-1}-1}$", r"\pau{Castilla-La Mancha, ordinaria 2021} $\displaystyle\lim_{x\to2}\frac{e^{x-2}-1}{2x-4}$",
                                                 r"\pau{Galicia, ordinaria 2022} $\displaystyle\lim_{x\to0}\frac{x\cos x}{\sin x}$", r"\pau{Murcia, septiembre 2018} $\displaystyle\lim_{x\to0}\frac{\ln(\cos x+\sin x)}{x}$",
                                                 r"\pau{Cantabria, septiembre 2018} $\displaystyle\lim_{x\to0}\frac{\sin(2x^2)+x}{\ln(x+1)+x}$", r"\pau{Castilla y León, ordinaria 2022} $\displaystyle\lim_{x\to0}\frac{x\sin x}{2-2\cos x}$"])
     + recorda(r"Si $\lim\frac fg$ es $\left[\frac00\right]$ o $\left[\frac\infty\infty\right]$, entonces $\lim\frac{f}{g}=\lim\frac{f'}{g'}$. Derivamos el numerador y el denominador \textbf{por separado}."),
     tasks(2, [r"$\overset{\text{L'H}}{=}\lim\frac{1}{e^{x-1}}=\res{1}$", r"$\overset{\text{L'H}}{=}\lim\frac{e^{x-2}}{2}=\res{\frac12}$", r"$\overset{\text{L'H}}{=}\lim\frac{\cos x-x\sin x}{\cos x}=\res{1}$",
               r"$\overset{\text{L'H}}{=}\lim\frac{\cos x-\sin x}{\cos x+\sin x}=\res{1}$", r"$\overset{\text{L'H}}{=}\lim\frac{4x\cos(2x^2)+1}{\frac{1}{x+1}+1}=\res{\frac12}$", r"$\overset{\text{L'H}}{=}\lim\frac{\sin x+x\cos x}{2\sin x}\overset{\text{L'H}}{=}\lim\frac{2\cos x-x\sin x}{2\cos x}=\res{1}$"])),
 (2, r"Calcula estos límites del tipo $\left[\frac\infty\infty\right]$:" + tasks(2, [r"$\displaystyle\lim_{x\to+\infty}\frac{x^3}{e^{2x}}$", r"$\displaystyle\lim_{x\to+\infty}\frac{(\ln x)^2}{x}$", r"$\displaystyle\lim_{x\to0^+}\frac{\ln(\sin x)}{\ln x}$", r"\pau{Castilla-La Mancha, ordinaria 2024} $\displaystyle\lim_{x\to+\infty}\frac{e^x-1}{x^2+3}$"]),
     tasks(2, [r"$\frac{3x^2}{2e^{2x}}\to\frac{6x}{4e^{2x}}\to\frac{6}{8e^{2x}}\to\res{0}$", r"$\frac{2\ln x\cdot\frac1x}{1}=\frac{2\ln x}{x}\to\frac{2/x}{1}\to\res{0}$", r"$\frac{\cos x/\sin x}{1/x}=\frac{x\cos x}{\sin x}\to\res{1}$", r"$\frac{e^x}{2x}\to\frac{e^x}{2}\to\res{+\infty}$"])),
 (2, r"\pau{Aragón, ordinaria 2025} Calcula $\displaystyle\lim_{x\to0}\frac{x^2-\sin(x^2)}{1-\cos x}$.",
     r"$\left[\frac00\right]\overset{\text{L'H}}{=}\lim\frac{2x-2x\cos(x^2)}{\sin x}=\lim\frac{2x\left(1-\cos x^2\right)}{\sin x}$; como $\frac{x}{\sin x}\to1$ y $1-\cos x^2\to0$, el límite es $\res{0}$."),
 (2, r"Límites con parámetros:" + tasks(1, [r"\pau{Aragón, extraordinaria 2023} Calcula $a$ para que $\displaystyle L=\lim_{x\to0}\frac{\ln(x+1)-a\sin x+3x\cos(2x)}{x^2}$ sea finito, y calcula $L$.",
                                          r"\pau{Castilla y León, extraordinaria 2021} Calcula $m>0$ para que $\displaystyle\lim_{x\to0}\frac{1-\cos(mx)}{x^2}=2$.",
                                          r"\pau{Galicia, ordinaria 2023} Si $f(x)=ae^x+b$, halla $a$ y $b$ para que $f(0)=0$ y $\displaystyle\lim_{x\to0}\frac{f(x)}{x}=3$."])
     + recorda(r"Si el denominador tiende a 0 y el límite tiene que ser finito, el numerador también tiene que tender a 0: esto da una ecuación."),
     tasks(1, [r"$\overset{\text{L'H}}{=}\lim\frac{\frac{1}{x+1}-a\cos x+3\cos2x-6x\sin2x}{2x}=\frac{4-a}{0}$:\newline hace falta $\res{a=4}$; entonces $\overset{\text{L'H}}{=}\lim\frac{-\frac{1}{(x+1)^2}+4\sin x-12\sin2x-12x\cos2x}{2}=\res{-\frac12}$",
               r"$\overset{\text{L'H}}{=}\lim\frac{m\sin mx}{2x}\overset{\text{L'H}}{=}\frac{m^2}{2}=2\Rightarrow\res{m=2}$",
               r"$a+b=0$; \ $\lim\frac{ae^x+b}{x}\overset{\text{L'H}}{=}a=3$: \ $\res{a=3,\ b=-3}$"])),
 (3, r"\pau{Aragón, extraordinaria 2022} Calcula $a,b\in\mathbb R$ para que exista $\displaystyle\lim_{x\to1}\frac{2x^3+ax^2+bx+3}{-x^3+4x^2-5x+2}=L$ (finito) y calcula el límite.",
     r"El denominador es $-(x-1)^2(x-2)$ (raíz doble en 1). El numerador también tiene que tener la raíz doble $x=1$: $N(1)=5+a+b=0$, $N'(1)=6+2a+b=0\Rightarrow\res{a=-1,\ b=-4}$. Entonces $N=(x-1)^2(2x+3)$ y $L=\frac{2+3}{-(1-2)}=\res{5}$."),
 (2, r"¿Dónde está el error? \ $\displaystyle\lim_{x\to1}\frac{x^2+1}{x+1}\overset{\text{L'H}}{=}\lim_{x\to1}\frac{2x}{1}=2$. \ ¿Y en este otro? \ $\displaystyle\lim_{x\to+\infty}\frac{x+\sin x}{x}\overset{\text{L'H}}{=}\lim_{x\to+\infty}(1+\cos x)$, que no existe, ``por tanto el límite no existe''.",
     r"En el primero no hay indeterminación: $\frac{2}{2}=\res{1}$. En el segundo, L'Hôpital no concluye nada si $\lim\frac{f'}{g'}$ no existe: $\frac{x+\sin x}{x}=1+\frac{\sin x}{x}\to\res{1}$."),
)

# =====================================================================
# 3. Altres indeterminacions
L(x**2 * ln(x), 0, 0, '+'); L(sq(x**2 + 1) - x, sp.oo, 0); L(1 / sin(x) - 1 / x, 0, 0); L(sq(3 * x**2 - 2) - (sq(3) * x + 5), sp.oo, -5)
L((x**2 - 1) / (x + 2) - (x**2 + 1) / (x - 2), sp.oo, -4)
L(((x + 1) / x)**((x**2 + 1) / x), sp.oo, E); L(((2 * x + 1) / (2 * x - 3))**x, sp.oo, E**2)
L(((x**2 + 1) / x - (x**3 - x**2 - x + 2) / x**2)**((3 + x**2) / x), sp.oo, E**2); L(cos(x)**(1 / x**2), 0, exp(-R(1, 2)))
L(sin(x)**tan(x), pi / 2, 1, '-'); L((1 / x)**sin(x), 0, 1, '+'); L(sin(x)**x, 0, 1, '+'); L((x**2 + 1)**(1 / ln(x)), sp.oo, E**2)
L(((x + 1) / (2 * x + 1))**(1 / x), 0, exp(-1), '-')
L((1 + 3 * x)**(1 / sin(x)), 0, E**3)
L((1 + x - sin(x))**(1 / x**3), 0, exp(R(1, 6)), '+'); L(tan(x / 2)**(1 / cos(x)), pi / 2, exp(-1), '-')
sec("Otras indeterminaciones",
 (1, r"Calcula (tipo $0\cdot\infty$ y $\infty-\infty$):" + tasks(2, [r"$\displaystyle\lim_{x\to0^+}x^2\ln x$", r"\pau{Murcia, ordinaria 2021} $\displaystyle\lim_{x\to+\infty}\left(\sqrt{x^2+1}-x\right)$",
                                                                      r"$\displaystyle\lim_{x\to0}\left(\frac{1}{\sin x}-\frac1x\right)$", r"\pau{Aragón, ordinaria 2022} $\displaystyle\lim_{x\to+\infty}\left[\sqrt{3x^2-2}-\left(\sqrt3x+5\right)\right]$",
                                                                      r"\pau{La Rioja, ordinaria 2023} $\displaystyle\lim_{x\to\infty}\left(\frac{x^2-1}{x+2}-\frac{x^2+1}{x-2}\right)$"])
     + recorda(r"$0\cdot\infty$: escribe $f\cdot g=\frac{f}{1/g}$. \ $\infty-\infty$: haz denominador común o multiplica por el conjugado."),
     tasks(2, [r"$\frac{\ln x}{1/x^2}\overset{\text{L'H}}{=}\frac{1/x}{-2/x^3}=-\frac{x^2}{2}\to\res{0}$", r"$\frac{1}{\sqrt{x^2+1}+x}\to\res{0}$", r"$\frac{x-\sin x}{x\sin x}\overset{\text{L'H}}{=}\frac{1-\cos x}{\sin x+x\cos x}\overset{\text{L'H}}{=}\frac{\sin x}{2\cos x-x\sin x}\to\res{0}$",
               r"$\frac{3x^2-2-(\sqrt3x+5)^2}{\sqrt{3x^2-2}+\sqrt3x+5}=\frac{-10\sqrt3x-27}{\sqrt{3x^2-2}+\sqrt3x+5}\to\frac{-10\sqrt3}{2\sqrt3}=\res{-5}$", r"$\frac{-4x^2-2x}{x^2-4}\to\res{-4}$"])),
 (2, r"Calcula estos límites del tipo $1^\infty$:" + tasks(2, [r"\pau{Castilla-La Mancha, ordinaria 2022} $\displaystyle\lim_{x\to+\infty}\left(\frac{x+1}{x}\right)^{\frac{x^2+1}{x}}$", r"\pau{Castilla-La Mancha, ordinaria 2026} $\displaystyle\lim_{x\to\infty}\left(\frac{2x+1}{2x-3}\right)^{x}$",
                                                              r"\pau{Aragón, septiembre 2018} $\displaystyle\lim_{x\to+\infty}\left(\frac{x^2+1}{x}-\frac{x^3-x^2-x+2}{x^2}\right)^{\frac{3+x^2}{x}}$", r"$\displaystyle\lim_{x\to0}\left(\cos x\right)^{1/x^2}$"])
     + recorda(r"$1^\infty$: $\displaystyle\lim f^g=e^{\lim g\,(f-1)}$, o bien tomando logaritmos: $\ln L=\lim g\ln f$."),
     tasks(2, [r"$\frac{x^2+1}{x}\cdot\frac1x\to1\Rightarrow\res{e}$", r"$x\cdot\frac{4}{2x-3}\to2\Rightarrow\res{e^2}$", r"$f-1=\frac{2x-2}{x^2}$, $\ \frac{3+x^2}{x}\cdot\frac{2x-2}{x^2}\to2\Rightarrow\res{e^2}$", r"$\frac{\cos x-1}{x^2}\to-\frac12\Rightarrow\res{e^{-1/2}=\frac{1}{\sqrt e}}$"])),
 (2, r"Calcula (tipo $1^\infty$, $\infty^0$ y $0^0$):" + tasks(2, [r"$\displaystyle\lim_{x\to\frac\pi2^-}\left(\sin x\right)^{\tan x}$", r"$\displaystyle\lim_{x\to0^+}\left(\frac1x\right)^{\sin x}$", r"$\displaystyle\lim_{x\to0^+}\left(\sin x\right)^{x}$", r"$\displaystyle\lim_{x\to+\infty}\left(x^2+1\right)^{\frac{1}{\ln x}}$"])
     + recorda(r"Tomamos logaritmos: $\ln L=\lim g\cdot\ln f$ (que es $0\cdot\infty$) y al final $L=e^{\ln L}$."),
     tasks(2, [r"$\ln L=\lim\frac{\ln\sin x}{\cot x}\overset{\text{L'H}}{=}\lim\frac{\cot x}{-1/\sin^2x}=\lim(-\sin x\cos x)=0\Rightarrow\res{1}$", r"$\ln L=\lim\frac{-\ln x}{1/\sin x}\overset{\text{L'H}}{=}\lim\frac{\sin^2x}{x\cos x}=0\Rightarrow\res{1}$",
               r"$\ln L=\lim x\ln\sin x=\lim\frac{\ln\sin x}{1/x}\overset{\text{L'H}}{=}\lim\frac{-x^2\cos x}{\sin x}=0\Rightarrow\res{1}$", r"$\ln L=\lim\frac{\ln(x^2+1)}{\ln x}\overset{\text{L'H}}{=}\lim\frac{2x^2}{x^2+1}=2\Rightarrow\res{e^2}$"])),
 (2, r"\pau{Aragón, ordinaria 2020} Calcula $\displaystyle\lim_{x\to0^+}\left(1+x-\sin x\right)^{1/x^3}$ \ y \ \pau{Madrid, ordinaria 2024} $\displaystyle\lim_{x\to\frac\pi2}\left(\tan\frac x2\right)^{\frac{1}{\cos x}}$.",
     r"$\ln L=\lim\frac{\ln(1+x-\sin x)}{x^3}\overset{\text{L'H}}{=}\lim\frac{1-\cos x}{3x^2(1+x-\sin x)}=\frac16\Rightarrow\res{\sqrt[6]{e}}$. \quad $\lim\frac{\tan\frac x2-1}{\cos x}\overset{\text{L'H}}{=}\frac{\frac12\cdot2}{-1}=-1\Rightarrow\res{\frac1e}$."),
 (3, r"\pau{Castilla-La Mancha, septiembre 2017} Calcula $k$ para que sea continua en $x=0$ la función " + '$' + pw((r'\left(\dfrac{x+1}{2x+1}\right)^{1/x}', 'x<0'), (r'6x+k', r'x\geq0')) + '$.',
     r"$\displaystyle\lim_{x\to0^-}\left(\frac{x+1}{2x+1}\right)^{1/x}=e^{\lim\frac1x\cdot\frac{-x}{2x+1}}=e^{-1}$, \ $f(0)=k$: \ $\res{k=\frac1e}$."),
 (2, r"Halla $a$ para que $\displaystyle\lim_{x\to0}\left(1+ax\right)^{\frac{1}{\sin x}}=e^3$.",
     r"$\ln L=\lim\frac{\ln(1+ax)}{\sin x}\overset{\text{L'H}}{=}\lim\frac{a/(1+ax)}{\cos x}=a$: \ $e^a=e^3\Rightarrow\res{a=3}$."),
)

# =====================================================================
# 4. Monotonia i extrems relatius
f_ = (x**2 + 1) / x; crit(f_, [-1, 1]); ext(f_, -1, 'max', -2); ext(f_, 1, 'min', 2)
f_ = 1 / (x**2 - x); crit(f_, [R(1, 2)]); ext(f_, R(1, 2), 'max', -4)
f_ = x * ln(x); crit(f_, [1 / E], 0.001, 50); ext(f_, 1 / E, 'min', -1 / E)
f_ = ln(x) / x; crit(f_, [E], 0.001, 50); ext(f_, E, 'max', 1 / E)
f_ = (exp(x) + exp(-x)) / 2; crit(f_, [0]); ext(f_, 0, 'min', 1)
f_ = -x**2 / 2 + 2 * ln(x + 1); crit(f_, [1], -0.999, 50); ext(f_, 1, 'max')
f_ = (x - 1) / (x * (x + 2)); crit(f_, [1 - sq(3), 1 + sq(3)]); ext(f_, 1 - sq(3), 'min'); ext(f_, 1 + sq(3), 'max')
f_ = (4 * x + 4) / x**2; crit(f_, [-2]); ext(f_, -2, 'min', -1)
f_ = x / (x**2 - 3 * x - 4); ok(sp.simplify(sp.diff(f_, x) - (-(x**2 + 4)) / (x**2 - 3 * x - 4)**2) == 0)
f_ = (x**2 - 3 * x + 3) / (x - 1); crit(f_, [0, 2]); ext(f_, 0, 'max', -3); ext(f_, 2, 'min', 1)
f_ = sin(x) + cos(x); ext(f_, pi / 4, 'max', sq(2)); ext(f_, 5 * pi / 4, 'min', -sq(2))
f_ = x - 2 * sin(x); ext(f_, pi / 3, 'min', pi / 3 - sq(3)); ext(f_, 5 * pi / 3, 'max', 5 * pi / 3 + sq(3))
ok(sp.limit(ln(x + 1) / (a_ * x), x, 0, '+') == 1 / a_); f_ = x**3 + b_ * x + 2; ok(sp.solve(sp.diff(f_, x).subs(x, -1), b_) == [-3]); ext(x**3 - 3 * x + 2, -1, 'max')
f_ = (2 * x**2 + 2 * x - 2) / (3 * x**2 + 3); crit(f_, [2 - sq(5), 2 + sq(5)]); ext(f_, 2 - sq(5), 'min', -sq(5) / 3); ext(f_, 2 + sq(5), 'max', sq(5) / 3)
f_ = (x**2 - 1)**R(2, 3); eq(sp.diff(f_, x).subs(x, R(1, 2)), R(4, 3) * R(1, 2) * (R(1, 4) - 1)**R(-1, 3))
f_ = x**5 - 5 * x**4; ok([sp.diff(f_, x, k).subs(x, 0) for k in range(1, 5)] == [0, 0, 0, -120]); eq(sp.diff(f_, x, 2).subs(x, 4), 320); eq(f_.subs(x, 4), -256)
f_ = a_ * x - sin(x) / x + 2; ok(sp.solve(sp.diff(f_, x).subs(x, -pi / 2), a_) == [4 / pi**2]); ok(N(sp.diff(f_.subs(a_, 4 / pi**2), x, 2).subs(x, -pi / 2)).real > 0)
sec("Monotonía y extremos relativos",
 (1, r"Estudia la monotonía y calcula los extremos relativos de las funciones siguientes:" + tasks(2, [r"\pau{Comunidad Valenciana, junio 2017} " + fx(r'\dfrac{x^2+1}{x}'), r"\pau{Comunidad Valenciana, junio 2018} " + fx(r'\dfrac{1}{x^2-x}'),
                                                                                              r"\pau{Murcia, ordinaria 2022} " + fx(r'x\ln x'), r"\pau{Castilla y León, extraordinaria 2020} " + fx(r'\dfrac{\ln x}{x}'),
                                                                                              r"\pau{Andalucía, septiembre 2017} " + fx(r'\dfrac{e^x+e^{-x}}{2}'), r"\pau{Aragón, extraordinaria 2020} " + fx(r'-\dfrac{x^2}{2}+2\ln(x+1)')])
     + recorda(r"Dominio $\to$ $f'$ $\to$ ceros de $f'$ y puntos fuera del dominio $\to$ tabla de signos de $f'$. Los extremos se dan como puntos $(a,f(a))$."),
     tasks(1, [r"$f'=1-\frac1{x^2}$: crece en $(-\infty,-1)\cup(1,+\infty)$, decrece en $(-1,0)\cup(0,1)$; \res{\text{máx. }(-1,-2)}, \res{\text{mín. }(1,2)}",
               r"$f'=\frac{-(2x-1)}{(x^2-x)^2}$: crece en $(-\infty,0)\cup\left(0,\frac12\right)$, decrece en $\left(\frac12,1\right)\cup(1,+\infty)$; \res{\text{máx. }\left(\frac12,-4\right)}",
               r"$f'=\ln x+1$: decrece en $\left(0,\frac1e\right)$, crece en $\left(\frac1e,+\infty\right)$; \res{\text{mín. }\left(\frac1e,-\frac1e\right)}",
               r"$f'=\frac{1-\ln x}{x^2}$: crece en $(0,e)$, decrece en $(e,+\infty)$; \res{\text{máx. }\left(e,\frac1e\right)}",
               r"$f'=\frac{e^x-e^{-x}}{2}$: decrece en $(-\infty,0)$, crece en $(0,+\infty)$; \res{\text{mín. }(0,1)}",
               r"Dominio $(-1,+\infty)$, $f'=-x+\frac{2}{x+1}=\frac{-(x+2)(x-1)}{x+1}$: crece en $(-1,1)$, decrece en $(1,+\infty)$; \res{\text{máx. }\left(1,-\frac12+2\ln2\right)}"])),
 (2, r"Estudia la monotonía y los extremos relativos de:" + tasks(1, [r"\pau{Comunidad Valenciana, ordinaria 2021} " + fx(r'\dfrac{x-1}{x(x+2)}'), r"\pau{Extremadura, extraordinaria 2024} " + fx(r'\dfrac{4x+4}{x^2}'),
                                                                   r"\pau{País Vasco, extraordinaria 2025} " + fx(r'\dfrac{x}{x^2-3x-4}'), r"\pau{Aragón, septiembre 2018} " + fx(r'\dfrac{x^2-3x+3}{x-1}')]),
     tasks(1, [r"$f'=\frac{-x^2+2x+2}{x^2(x+2)^2}$: decrece en $(-\infty,-2)\cup\left(-2,1-\sqrt3\right)\cup\left(1+\sqrt3,+\infty\right)$, crece en $\left(1-\sqrt3,0\right)\cup\left(0,1+\sqrt3\right)$; \res{\text{mín. en }x=1-\sqrt3}, \res{\text{máx. en }x=1+\sqrt3}",
               r"$f'=\frac{-4(x+2)}{x^3}$: decrece en $(-\infty,-2)\cup(0,+\infty)$, crece en $(-2,0)$; \res{\text{mín. }(-2,-1)}",
               r"$f'=\frac{-(x^2+4)}{(x^2-3x-4)^2}<0$: \rest{decreciente en todo el dominio} $\mathbb R-\{-1,4\}$, sin extremos",
               r"$f'=1-\frac{1}{(x-1)^2}$: crece en $(-\infty,0)\cup(2,+\infty)$, decrece en $(0,1)\cup(1,2)$; \res{\text{máx. }(0,-3)}, \res{\text{mín. }(2,1)}"])),
 (2, r"Monotonía y extremos de funciones trigonométricas en $[0,2\pi]$:" + tasks(2, [fx(r'\sin x+\cos x'), fx(r'x-2\sin x', 'g')]),
     tasks(1, [r"$f'=\cos x-\sin x=0\Rightarrow x=\frac\pi4,\frac{5\pi}4$: \res{\text{máx. }\left(\frac\pi4,\sqrt2\right)}, \res{\text{mín. }\left(\frac{5\pi}4,-\sqrt2\right)}; crece en $\left(0,\frac\pi4\right)\cup\left(\frac{5\pi}4,2\pi\right)$",
               r"$g'=1-2\cos x=0\Rightarrow x=\frac\pi3,\frac{5\pi}3$; $g''=2\sin x$: \res{\text{mín. }\left(\frac\pi3,\frac\pi3-\sqrt3\right)}, \res{\text{máx. }\left(\frac{5\pi}3,\frac{5\pi}3+\sqrt3\right)}"])),
 (2, r"\pau{Aragón, ordinaria 2021} Dada " + '$' + pw((r'x^3+bx+2', r'x\leq0'), (r'\dfrac{\ln(x+1)}{ax}', 'x>0')) + '$' + r", halla $a$ para que sea continua en $\mathbb R$ y, además, $b$ para que tenga un extremo relativo en $x=-1$. ¿De qué tipo es?",
     r"$\lim_{x\to0^+}\frac{\ln(x+1)}{ax}=\frac1a=f(0)=2\Rightarrow\res{a=\frac12}$ (para todo $b$). \ $f'(-1)=3+b=0\Rightarrow\res{b=-3}$; \ $f''(-1)=-6<0$: \rest{máximo relativo}."),
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2021} Halla y clasifica los extremos relativos de $f(x)=\dfrac{2x^2+2x-2}{3x^2+3}$.",
     r"$f'(x)=\frac{-6(x^2-4x-1)}{(3x^2+3)^2}=0\Leftrightarrow x=2\pm\sqrt5$: \ \res{\text{mín. }\left(2-\sqrt5,-\frac{\sqrt5}{3}\right)}, \ \res{\text{máx. }\left(2+\sqrt5,\frac{\sqrt5}{3}\right)}."),
 (3, r"Estudia la monotonía y los extremos de $f(x)=\sqrt[3]{(x^2-1)^2}$. ¿Qué puntos críticos no son de derivada nula?",
     r"$f'(x)=\frac{4x}{3\sqrt[3]{x^2-1}}$: se anula en $x=0$ y no existe en $x=\pm1$. Decrece en $(-\infty,-1)\cup(0,1)$ y crece en $(-1,0)\cup(1,+\infty)$: \res{\text{mín. }(\pm1,0)} (puntos de retroceso, no derivables) y \res{\text{máx. }(0,1)}."),
 (2, r"Clasifica los puntos críticos de $f(x)=x^5-5x^4$ con el criterio de las derivadas sucesivas.",
     r"$f'=5x^3(x-4)$: $x=0$ y $x=4$. \ $f''(4)=320>0$: \res{\text{mín. }(4,-256)}. \ En $x=0$: $f'=f''=f'''=0$ y $f^{(4)}(0)=-120<0$ (orden par): \res{\text{máx. }(0,0)}."),
 (2, r"\pau{Aragón, ordinaria 2023} Sea $f(x)=ax-\dfrac{\sin x}{x}+2$ si $x\neq0$ y $f(0)=2$. Halla $a$ para que $f$ tenga un extremo relativo en $x=-\frac\pi2$ y di de qué tipo es.",
     r"$f'(x)=a-\frac{x\cos x-\sin x}{x^2}$, \ $f'\left(-\frac\pi2\right)=a-\frac{4}{\pi^2}=0\Rightarrow\res{a=\frac{4}{\pi^2}}$; \ $f''\left(-\frac\pi2\right)>0$: \rest{mínimo relativo}."),
)

# =====================================================================
# 5. Curvatura i punts d'inflexió
f_ = x**3 - 6 * x**2 + 9 * x; infl(f_, 2, 2); ext(f_, 1, 'max', 4); ext(f_, 3, 'min', 0)
f_ = exp(-x**2); infl(f_, 1 / sq(2), exp(-R(1, 2))); infl(f_, -1 / sq(2))
f_ = x / (x**2 + 1); ok(sp.simplify(sp.diff(f_, x, 2) - 2 * x * (x**2 - 3) / (x**2 + 1)**3) == 0); infl(f_, sq(3), sq(3) / 4); infl(f_, 0, 0)
f_ = ln(x**2 + 1); infl(f_, 1, ln(2)); infl(f_, -1)
f_ = x**3 - 3 * x**2 + 2 * x + 1; infl(f_, 1, 1); tang(f_, 1, -1, 2)
f_ = exp(x) * sin(x); ext(f_, 3 * pi / 4, 'max'); ext(f_, 7 * pi / 4, 'min'); infl(f_, pi / 2, exp(pi / 2)); infl(f_, 3 * pi / 2)
f_ = x**3 / (1 + x)**2; infl(f_, 0, 0); ext(f_, -3, 'max', -R(27, 4))
f_ = a_ * x**3 + b_ * x**2 + c_ * x + d_; ok(sp.solve(sp.diff(f_, x, 2), x) == [-b_ / (3 * a_)])
f_ = x * exp(x); ext(f_, -1, 'min', -1 / E); infl(f_, -2, -2 / E**2)
sec("Curvatura y puntos de inflexión",
 (1, r"Estudia la curvatura y halla los puntos de inflexión de:" + tasks(2, [r"\pau{Asturias, ordinaria 2020} " + fx(r'x^3-6x^2+9x'), r"\pau{Extremadura, ordinaria 2021} " + fx(r'e^{-x^2}'), r"\pau{Comunidad Valenciana, extraordinaria 2025} " + fx(r'\dfrac{x}{x^2+1}'), fx(r'\ln\left(x^2+1\right)')])
     + recorda(r"$f''>0$: convexa $\cup$; $\ f''<0$: cóncava $\cap$. Hay punto de inflexión donde $f''$ cambia de signo (y $f$ es continua)."),
     tasks(1, [r"$f''=6x-12$: cóncava en $(-\infty,2)$, convexa en $(2,+\infty)$, \res{\text{P.I. }(2,2)}",
               r"$f''=(4x^2-2)e^{-x^2}$: convexa en $\left(-\infty,-\frac{\sqrt2}2\right)\cup\left(\frac{\sqrt2}2,+\infty\right)$, cóncava entre ellos; \res{\text{P.I. }\left(\pm\frac{\sqrt2}{2},\frac{1}{\sqrt e}\right)}",
               r"$f''=\frac{2x(x^2-3)}{(x^2+1)^3}$: cóncava en $(-\infty,-\sqrt3)\cup(0,\sqrt3)$, convexa en $(-\sqrt3,0)\cup(\sqrt3,+\infty)$; \res{\text{P.I. }(0,0),\ \left(\pm\sqrt3,\pm\frac{\sqrt3}{4}\right)}",
               r"$f''=\frac{2(1-x^2)}{(x^2+1)^2}$: convexa en $(-1,1)$, cóncava fuera; \res{\text{P.I. }(\pm1,\ln2)}"])),
 (2, r"\pau{Castilla y León, ordinaria 2022} Dada $f(x)=xe^x$, determina su dominio, las asíntotas, la monotonía, los extremos, la curvatura y los puntos de inflexión.",
     r"Dominio $\mathbb R$; AH $y=0$ cuando $x\to-\infty$. $f'=(x+1)e^x$: \res{\text{mín. }\left(-1,-\frac1e\right)}. $f''=(x+2)e^x$: cóncava en $(-\infty,-2)$, convexa en $(-2,+\infty)$, \res{\text{P.I. }\left(-2,-\frac{2}{e^2}\right)}."),
 (2, r"Halla la recta tangente a la gráfica de $f(x)=x^3-3x^2+2x+1$ en su punto de inflexión. ¿La curva queda por encima o por debajo de la tangente?",
     r"$f''=6x-6=0\Rightarrow x=1$, $f(1)=1$, $f'(1)=-1$: \res{y=-x+2}. Como es un punto de inflexión, la tangente \rest{atraviesa} la curva (por debajo a la izquierda, por encima a la derecha)."),
 (2, r"Estudia la monotonía y la curvatura de $f(x)=e^x\sin x$ en $[0,2\pi]$.",
     r"$f'=e^x(\sin x+\cos x)$: \res{\text{máx. en }x=\frac{3\pi}4}, \res{\text{mín. en }x=\frac{7\pi}4}. $f''=2e^x\cos x$: convexa en $\left(0,\frac\pi2\right)\cup\left(\frac{3\pi}2,2\pi\right)$, cóncava en $\left(\frac\pi2,\frac{3\pi}2\right)$; \res{\text{P.I. en }x=\frac\pi2,\ \frac{3\pi}2}."),
 (2, r"\pau{La Rioja, extraordinaria 2022} Halla los intervalos de crecimiento y decrecimiento, los extremos y los puntos de inflexión de $f(x)=\dfrac{x^3}{(1+x)^2}$.",
     r"$f'=\frac{x^2(x+3)}{(x+1)^3}$: crece en $(-\infty,-3)\cup(-1,+\infty)$, decrece en $(-3,-1)$, \res{\text{máx. }\left(-3,-\frac{27}{4}\right)}. $f''=\frac{6x}{(x+1)^4}$: \res{\text{P.I. }(0,0)} (con tangente horizontal)."),
 (3, r"Demuestra que toda función polinómica de tercer grado $f(x)=ax^3+bx^2+cx+d$ ($a\neq0$) tiene exactamente un punto de inflexión. ¿Para qué valor de $x$?",
     r"$f''(x)=6ax+2b$ es de primer grado: se anula en un solo punto, $\res{x=-\frac{b}{3a}}$, y en él cambia de signo. (Es, además, el centro de simetría de la gráfica.)"),
)

# =====================================================================
# 6. Funcions amb paràmetres
f_ = a_ * x**3 + b_ * x**2 + c_ * x + d_
ok(sp.solve([sp.diff(f_, x).subs(x, -1), sp.diff(f_, x).subs(x, 1), f_.subs(x, -1) - 4, f_.subs(x, 1)], [a_, b_, c_, d_]) == {a_: 1, b_: 0, c_: -3, d_: 2})
f_ = x**3 + a_ * x**2 + b_ * x + c_; ok(sp.solve([f_.subs(x, 1), sp.diff(f_, x).subs(x, 0), sp.diff(f_, x).subs(x, -1) + 3], [a_, b_, c_]) == {a_: 3, b_: 0, c_: -4})
ok(sp.solve([sp.diff(f_, x, 2).subs(x, 1), sp.diff(f_, x).subs(x, -1), f_.subs(x, -1)], [a_, b_, c_]) == {a_: -3, b_: -9, c_: -5})
f_ = (a_ * x + b_) * exp(-x); ok(sp.solve([sp.diff(f_, x).subs(x, 2), f_.subs(x, 2) - exp(-2)], [a_, b_]) == {a_: 1, b_: -1}); ext((x - 1) * exp(-x), 2, 'max')
f_ = x**4 + a_ * x**3 + b_ * x**2; ok(sp.solve([sp.diff(f_, x).subs(x, 1), sp.diff(f_, x, 2).subs(x, 1)], [a_, b_]) == {a_: -R(8, 3), b_: 2}); infl(x**4 - R(8, 3) * x**3 + 2 * x**2, 1)
f_ = a_ * x**3 + b_ * x**2 - 3 * x + c_; ok(sp.solve([f_.subs(x, 0) - 1, sp.diff(f_, x).subs(x, 1), sp.diff(f_, x).subs(x, -1)], [a_, b_, c_]) == {a_: 1, b_: 0, c_: 1})
f_ = x**3 + a_ * x**2 + b_ * x + c_; ok(sp.solve([sp.diff(f_, x, 2).subs(x, 1), sp.diff(f_, x).subs(x, 2), f_.subs(x, 1) - 2], [a_, b_, c_]) == {a_: -3, b_: 0, c_: 4})
f_ = (exp(a_ * x) + b_) * x - E; ok(sp.solve([sp.diff(f_, x).subs(x, 0), sp.diff(f_, x, 2).subs(x, 2)], [a_, b_], dict=True) in ([{a_: -1, b_: -1}, {a_: 0, b_: -1}], [{a_: 0, b_: -1}, {a_: -1, b_: -1}]))  # a ≠ 0
f_ = a_ * sq(3 * x + 3) + b_ * sq(x - 1); ok(sp.solve([f_.subs(x, 2) - 8, sp.diff(f_, x, 2).subs(x, 2)], [a_, b_]) == {a_: 3, b_: -1})
sec("Funciones con parámetros",
 (1, r"\pau{Madrid, extraordinaria 2024}" + tasks(1, [r"Propón una función polinómica de grado 2 cuya gráfica sea tangente a la recta $y=x$ en $(0,0)$.", r"Propón una función polinómica de grado 2 que tenga un máximo relativo en $(1,1)$.", r"Justifica si una función polinómica de grado 2 puede tener dos extremos relativos."]),
     tasks(1, [r"Por ejemplo $\res{f(x)=x^2+x}$ ($f(0)=0$, $f'(0)=1$).", r"Por ejemplo $\res{f(x)=-x^2+2x}$ ($f'(1)=0$, $f(1)=1$, $f''<0$).", r"\rest{No}: $f'(x)=2ax+b$ es de primer grado y se anula en un solo punto."])),
 (2, r"Halla el polinomio de tercer grado que tiene un máximo relativo en $(-1,4)$ y un mínimo relativo en $(1,0)$."
     + recorda(r"Cuatro condiciones: $f'(-1)=0$, $f'(1)=0$, $f(-1)=4$, $f(1)=0$."),
     r"$f=ax^3+bx^2+cx+d$: $3a\mp2b+c=0\Rightarrow b=0,\ c=-3a$; \ $2a+d=4$, $-2a+d=0$: \ $\res{f(x)=x^3-3x+2}$ ($f''(-1)=-6<0$ \checkmark)."),
 (2, r"Resuelve:" + tasks(1, [r"\pau{Andalucía, extraordinaria 2026} $f(x)=x^3+ax^2+bx+c$ cumple $f(1)=0$, $x=0$ es un punto crítico y la tangente en $x=-1$ es paralela a $y+3x=0$. Halla $a$, $b$ y $c$.",
                           r"\pau{Castilla y León, extraordinaria 2020} Determina $f(x)=x^3+ax^2+bx+c$ si tiene un punto de inflexión en $x=1$ y la tangente en $(-1,0)$ es el eje de abscisas.",
                           r"\pau{Castilla-La Mancha, ordinaria 2024} Halla $a$, $b$, $c$ para que $f(x)=x^3+ax^2+bx+c$ tenga un extremo relativo en $x=2$ y un punto de inflexión en $P(1,2)$."]),
     tasks(1, [r"$f'(0)=b=0$, $f'(-1)=3-2a=-3$, $f(1)=1+a+c=0$: $\res{a=3,\ b=0,\ c=-4}$", r"$f''(1)=6+2a=0$, $f'(-1)=3-2a+b=0$, $f(-1)=0$: $\res{f(x)=x^3-3x^2-9x-5}$",
               r"$f''(1)=0\Rightarrow a=-3$; $f'(2)=0\Rightarrow b=0$; $f(1)=2\Rightarrow c=4$: $\res{a=-3,\ b=0,\ c=4}$"])),
 (2, r"Halla $a$ y $b$ para que $f(x)=(ax+b)\,e^{-x}$ tenga un extremo relativo en el punto $\left(2,\frac{1}{e^2}\right)$. ¿Es máximo o mínimo?",
     r"$f'(x)=e^{-x}(a-ax-b)$: $f'(2)=0\Rightarrow b=-a$; $f(2)=(2a+b)e^{-2}=ae^{-2}=e^{-2}\Rightarrow\res{a=1,\ b=-1}$. $f'(x)=e^{-x}(2-x)$ pasa de $+$ a $-$: \rest{máximo}."),
 (3, r"Halla $a$ y $b$ para que $f(x)=x^4+ax^3+bx^2$ tenga en $x=1$ un punto de inflexión con tangente horizontal.",
     r"$f'(1)=4+3a+2b=0$, $f''(1)=12+6a+2b=0\Rightarrow\res{a=-\frac83,\ b=2}$. Comprobación: $f''=4(3x-1)(x-1)$ cambia de signo en 1 \checkmark."),
 (2, r"\pau{Galicia, extraordinaria 2021} Halla $a,b,c$ para que $f(x)=ax^3+bx^2-3x+c$ cumpla $f(0)=1$ y tenga extremos relativos en $x=\pm1$. ¿De qué tipo son?",
     r"$\res{a=1,\ b=0,\ c=1}$; $f''(x)=6x$: \rest{máximo en $x=-1$ y mínimo en $x=1$}."),
 (2, r"\pau{Aragón, extraordinaria 2023} Sea $f(x)=\left(e^{ax}+b\right)x-e$, $a\neq0$. Calcula $a$ y $b$ sabiendo que tiene un extremo relativo en $x=0$ y un punto de inflexión en $x=2$.",
     r"$f'(x)=e^{ax}(1+ax)+b$, $f'(0)=1+b=0$; \ $f''(x)=ae^{ax}(2+ax)$, $f''(2)=0\Rightarrow 2+2a=0$: \ $\res{a=-1,\ b=-1}$."),
 (3, r"\pau{Canarias, junio 2018} Determina $a$ y $b$ para que $f(x)=a\sqrt{3x+3}+b\sqrt{x-1}$ tenga un punto de inflexión en $(2,8)$.",
     r"$f(2)=3a+b=8$; $f''(2)=-\frac{a}{12}-\frac b4=0\Rightarrow a=-3b$: \ $\res{a=3,\ b=-1}$."),
)

# =====================================================================
# 7. Teoremes de Rolle i del valor mitjà
f_ = x**3 - 4 * x; ok(sorted(sp.solve(sp.diff(f_, x), x)) == [-2 / sq(3), 2 / sq(3)])
eq((1 / x).subs(x, 4) - 1, -R(3, 4)); ok(sp.solve(-1 / x**2 + R(1, 4), x) == [-2, 2])
f_ = x**2 + 2 * x; ok(sp.solve(sp.diff(f_, x) - (f_.subs(x, 2) - f_.subs(x, 0)) / 2, x) == [1])
sol = sp.solve([4 - 2 * a_ - b_ - (a_ + 2 * c_), -b_ - a_, a_ - c_], [a_, b_, c_]); ok(sol == {a_: 1, b_: -1, c_: 1})
sol = sp.solve([1 + a_ + b_ - c_, 2 + a_ - c_, b_ - 4 * c_], [a_, b_, c_]); ok(sol == {a_: -R(7, 4), b_: 1, c_: R(1, 4)})
sol = sp.solve([2 + a_ - b_ - c_, 4 + a_ - b_, 2 * b_ + c_], [a_, b_, c_]); ok(sol == {a_: -3, b_: 1, c_: -2})
f_ = x * sin(x) - cos(x); eq(f_.subs(x, -1), f_.subs(x, 1)); ok(sp.simplify(sp.diff(f_, x) - (2 * sin(x) + x * cos(x))) == 0); ext(f_, 0, 'min', -1)
f_ = x**4 + pi * x**3 + pi**2 * x**2 + pi**3 * x + pi**4; eq(f_.subs(x, -pi), f_.subs(x, 0)); eq(sp.diff(f_, x).subs(x, -pi), -2 * pi**3)
f_ = x**3 * (x - 1)**2 + 1; eq(f_.subs(x, 0), f_.subs(x, 1))
f_ = sq(x + sin(pi * x / 2)); eq(f_.subs(x, 1), sq(2)); eq(f_.subs(x, 2), sq(2)); eq(f_.subs(x, 3), sq(2))
f_ = x**3 + x - 1; ok(f_.subs(x, 0) < 0 and f_.subs(x, 1) > 0)
ok(sp.simplify((1 / b_**2 - 1 / a_**2) / (b_ - a_) + (a_ + b_) / (a_**2 * b_**2)) == 0)
sec("Teoremas de Rolle y del valor medio",
 (1, r"Comprueba si se cumplen las hipótesis del teorema indicado y, si es así, halla los valores de $c$:" + tasks(1, [r"Rolle: $f(x)=x^3-4x$ en $[-2,2]$.", r"Valor medio: $f(x)=x^2+2x$ en $[0,2]$.", r"Valor medio: $f(x)=\dfrac1x$ en $[1,4]$.", r"Rolle: $f(x)=|x|-1$ en $[-1,1]$."])
     + recorda(r"Rolle: $f$ continua en $[a,b]$, derivable en $(a,b)$ y $f(a)=f(b)$ $\Rightarrow$ $\exists c\in(a,b)$ con $f'(c)=0$. Valor medio: $f'(c)=\frac{f(b)-f(a)}{b-a}$."),
     tasks(1, [r"Polinomio, $f(\pm2)=0$: $3c^2-4=0\Rightarrow\res{c=\pm\frac{2}{\sqrt3}}$", r"$\frac{8-0}{2}=4=2c+2\Rightarrow\res{c=1}$", r"Continua y derivable en $[1,4]$: $\frac{1/4-1}{3}=-\frac14=-\frac1{c^2}\Rightarrow\res{c=2}$",
               r"\rest{No se puede aplicar}: no es derivable en $x=0$ (y, efectivamente, $f'=\pm1\neq0$)."])),
 (2, r"Halla los parámetros para que se cumplan las hipótesis del teorema de Rolle:" + tasks(1, [r"\pau{Extremadura, extraordinaria 2024} " + '$' + pw((r'x^2+ax-b', 'x<0'), (r'a+cx', r'x\geq0')) + '$ en $[-2,2]$.',
                                                                                              r"\pau{Extremadura, ordinaria 2023} " + '$' + pw((r'x^2+ax+b', r'0\leq x<1'), (r'cx', r'1\leq x\leq4')) + '$ en $[0,4]$.',
                                                                                              r"\pau{Galicia, septiembre 2018} " + '$' + pw((r'2x^2+ax', r'x\leq1'), (r'bx+c', 'x>1')) + '$ en $[0,2]$; troba també el punt on es compleix la tesi.'])
     + recorda(r"Tres condiciones: continuidad en el punto de cambio, derivabilidad en el punto de cambio y $f(a)=f(b)$."),
     tasks(1, [r"$-b=a$, $a=c$, $4-2a-b=a+2c$: $\res{a=1,\ b=-1,\ c=1}$", r"$1+a+b=c$, $2+a=c$, $b=4c$: $\res{a=-\frac74,\ b=1,\ c=\frac14}$", r"$2+a=b+c$, $4+a=b$, $0=2b+c$: $\res{a=-3,\ b=1,\ c=-2}$; \ $4x-3=0\Rightarrow\res{x=\frac34}$"])),
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2021} Enuncia el teorema de Rolle y úsalo para razonar si $f(x)=x\sin x-\cos x$ tiene al menos un extremo relativo en $[-1,1]$.",
     r"$f$ es continua y derivable y $f(-1)=f(1)$ (es par): existe $c\in(-1,1)$ con $f'(c)=0$. De hecho, $f'(x)=2\sin x+x\cos x$ se anula en $c=0$ y en él pasa de $-$ a $+$: hay \rest{un mínimo relativo en $x=0$}."),
 (2, r"\pau{Madrid, ordinaria 2024} Prueba que $f(x)=x^4+\pi x^3+\pi^2x^2+\pi^3x+\pi^4$ tiene al menos un punto de derivada nula en $(-\pi,0)$ usando el teorema de Rolle. Pruébalo de nuevo con el teorema de Bolzano.",
     r"Rolle: $f$ es polinómica y $f(-\pi)=\pi^4=f(0)$. \ Bolzano aplicado a $f'$: $f'(-\pi)=-2\pi^3<0$, $f'(0)=\pi^3>0$ y $f'$ es continua: \rest{existe $c\in(-\pi,0)$ con $f'(c)=0$}."),
 (2, r"\pau{La Rioja, ordinaria 2026} Sea $f(x)=x^3(x-1)^2+1$. Demuestra que la ecuación $f'(x)=0$ tiene alguna solución en $(0,1)$.",
     r"$f$ es polinómica (continua y derivable) y $f(0)=f(1)=1$: por Rolle, \rest{existe $c\in(0,1)$ con $f'(c)=0$}."),
 (3, r"\pau{Navarra, extraordinaria 2021} Considera $f(x)=\sqrt{x+\sin\frac{\pi x}{2}}$. Demuestra que es continua en $[1,3]$ y que existen $\alpha\in(1,2)$ y $\beta\in(2,3)$ tales que $f'(\alpha)=f'(\beta)=0$.",
     r"En $[1,3]$, $x+\sin\frac{\pi x}{2}\geq x-1\geq0$ y en $x=1$ vale 2: el radicando es positivo y $f$ es continua y derivable. $f(1)=f(2)=f(3)=\sqrt2$: Rolle en $[1,2]$ y en $[2,3]$ da \rest{$\alpha$ y $\beta$}."),
 (3, r"Demuestra que la ecuación $x^3+x-1=0$ tiene exactamente una solución real y que está en el intervalo $(0,1)$.",
     r"Bolzano: $f(0)=-1<0$, $f(1)=1>0$ $\Rightarrow$ al menos una raíz en $(0,1)$. Si hubiera dos, por Rolle $f'(c)=3c^2+1=0$, imposible: \rest{hay exactamente una}."),
 (3, r"\pau{Extremadura, julio 2017} Enuncia el teorema del valor medio y, aplicándolo a $f(x)=\dfrac{1}{x^2}$, prueba que si $1<a<b$, entonces $a+b<2a^2b^2$.",
     r"En $[a,b]$: $\frac{1/b^2-1/a^2}{b-a}=-\frac{a+b}{a^2b^2}=f'(c)=-\frac{2}{c^3}$, con $1<a<c<b$. Por tanto $\frac{a+b}{a^2b^2}=\frac{2}{c^3}<2$, es decir, \rest{$a+b<2a^2b^2$}."),
)

# =====================================================================
# 8. Extrems absoluts
f_ = x**3 - 3 * x; ok([f_.subs(x, v) for v in (-2, -1, 1, 3)] == [-2, 2, -2, 18])
f_ = x * exp(-x); ext(f_, 1, 'max', 1 / E); eq(f_.subs(x, 3), 3 / E**3)
f_ = x - 2 * ln(x); crit(f_, [2], 0.01, 50); eq(f_.subs(x, 2), 2 - 2 * ln(2)); ok(N(f_.subs(x, E)).real < 1 and N(f_.subs(x, 2)).real < N(f_.subs(x, E)).real)
F_ = 10 * t**3 / 3 - t**4 / 4 + 6; ok(sp.simplify(sp.diff(F_, t) - t**2 * (10 - t)) == 0); eq(F_.subs(t, 10), R(2518, 3))
ok([R(5, 3) * 1, 14 - 12 + 3, 14 - 24 + 12, 14 - 32 + R(64, 3)] == [R(5, 3), 5, 2, R(10, 3)])
p_ = sin(t)**2 * cos(t); ok(sp.simplify(sp.diff(p_, t) - sin(t) * (2 * cos(t)**2 - sin(t)**2)) == 0); eq(p_.subs(t, atan(sq(2))), 2 / (3 * sq(3)))
f_ = (x + 1) / (x**2 + 1); ext(f_, -1 + sq(2), 'max', (1 + sq(2)) / 2); ext(f_, -1 - sq(2), 'min', (1 - sq(2)) / 2)
f_ = 2 * cos(x + pi / 2) + 10; eq(f_.subs(x, pi / 2), 8); eq(f_.subs(x, 4), 10 - 2 * sin(4))
f_ = 5 * (t + 1) * exp(-t); ok(sp.simplify(sp.diff(f_, t) + 5 * t * exp(-t)) == 0)
sec("Extremos absolutos",
 (1, r"Halla los extremos absolutos de cada función en el intervalo indicado:" + tasks(2, [r"$f(x)=x^3-3x$ en $[-2,3]$", r"$f(x)=x\,e^{-x}$ en $[0,3]$", r"$f(x)=x-2\ln x$ en $[1,e]$", r"$f(x)=\sin x+\cos x$ en $[0,2\pi]$"])
     + recorda(r"Candidatos: los extremos del intervalo, los puntos críticos interiores ($f'=0$) y los puntos no derivables. El valor más grande es el máximo absoluto y el más pequeño, el mínimo."),
     tasks(1, [r"$f(-2)=-2$, $f(-1)=2$, $f(1)=-2$, $f(3)=18$: \res{\text{máx. } 18 \text{ en } x=3}, \res{\text{mín. }-2\text{ en }x=-2\text{ y }x=1}",
               r"$f(0)=0$, $f(1)=\frac1e$, $f(3)=\frac3{e^3}$: \res{\text{máx. }\tfrac1e\text{ en }x=1}, \res{\text{mín. }0\text{ en }x=0}",
               r"$f'=1-\frac2x=0\Rightarrow x=2$: $f(1)=1$, $f(2)=2-2\ln2\approx0{,}61$, $f(e)=e-2\approx0{,}72$: \res{\text{máx. }1\text{ en }x=1}, \res{\text{mín. }2-2\ln2\text{ en }x=2}",
               r"\res{\text{máx. }\sqrt2\text{ en }x=\tfrac\pi4}, \res{\text{mín. }-\sqrt2\text{ en }x=\tfrac{5\pi}4}"])),
 (2, r"\pau{Comunidad Valenciana, extraordinaria 2026} El coeficiente de gravedad de un brote de gripe $t$ días después de empezar cumple $F'(t)=t^2(10-t)$. Calcula $F(t)$ si $F(0)=6$, y cuántos días después se alcanza el máximo y cuál es.",
     r"$F(t)=\frac{10t^3}{3}-\frac{t^4}{4}+6$. $F'>0$ en $(0,10)$ y $<0$ en $(10,+\infty)$: máximo \res{\text{a los 10 días}}, $F(10)=\res{\frac{2518}{3}\approx839{,}33}$."),
 (2, r"\pau{Comunidad Valenciana, ordinaria 2026} Calcula los valores máximos y mínimos, relativos y absolutos, de $f(x)=\dfrac{x+1}{x^2+1}$.",
     r"$f'=\frac{-x^2-2x+1}{(x^2+1)^2}$: \res{\text{mín. }\left(-1-\sqrt2,\tfrac{1-\sqrt2}{2}\right)}, \res{\text{máx. }\left(-1+\sqrt2,\tfrac{1+\sqrt2}{2}\right)}; como $f\to0$ en $\pm\infty$, también son \rest{absolutos}."),
 (2, r"\pau{Asturias, extraordinaria 2025} La cantidad de agua de un depósito es $f(t)=2\cos\left(t+\frac\pi2\right)+10$, $t\in[0,4]$ horas. Calcula sus máximos y mínimos, demuestra que no se vacía nunca y di durante cuánto tiempo aumenta.",
     r"$f=10-2\sin t$, $f'=-2\cos t=0\Rightarrow t=\frac\pi2$. $f(0)=10$, $f\left(\frac\pi2\right)=8$, $f(4)\approx11{,}51$: \res{\text{mín. }8\ \left(t=\tfrac\pi2\right)}, \res{\text{máx. }\approx11{,}51\ (t=4)}. No se vacía ($f\geq8$). Aumenta en $\left(\frac\pi2,4\right)$: \res{\approx2{,}43\text{ h}}."),
 (2, r"\pau{Madrid, extraordinaria 2023} El consumo de un vehículo (litros/100 km) a velocidad $v$ (decenas de km/h) es $c(v)=\frac{5v}{3}$ si $0\leq v<3$ y $c(v)=14-4v+\frac{v^2}{3}$ si $v\geq3$." + tasks(1, [r"Si tiene que circular a más de 3 decenas de km/h, ¿a qué velocidad el consumo es mínimo?", r"Si $1\leq v\leq8$, ¿cuáles son el consumo máximo y el mínimo?"]),
     tasks(1, [r"$c'(v)=-4+\frac{2v}3=0\Rightarrow v=6$: \res{60\text{ km/h}} (2 l/100 km).", r"$c(1)=\frac53$, $c(3)=5$, $c(6)=2$, $c(8)=\frac{10}3$: \res{\text{mín. }\tfrac53\ (v=1)}, \res{\text{máx. }5\ (v=3)}."])),
 (3, r"\pau{Navarra, ordinaria 2025} El precio del kWh entre $t=0$ y $t=1$ es $p(t)=0{,}15+\sin^2\left(\frac\pi2t\right)\cos\left(\frac\pi2t\right)$. Calcula los instantes en los que el precio es máximo y mínimo.",
     r"Con $s=\frac\pi2t$: $\frac{d}{ds}\left(\sin^2s\cos s\right)=\sin s\left(2\cos^2s-\sin^2s\right)=0\Rightarrow\tan s=\sqrt2$. \res{\text{Máximo en }t=\tfrac2\pi\arctan\sqrt2\approx0{,}61}, $p\approx0{,}535$; \res{\text{mínimo }0{,}15\text{ en }t=0\text{ y }t=1}."),
 (2, r"\pau{Castilla-La Mancha, ordinaria 2025} La concentración de virus activos es $f(t)=5(t+1)e^{-t}$, $t\geq0$. ¿En qué instante la derivada $f'(t)$ toma el valor más pequeño? ¿Cuál es el valor a largo plazo?",
     r"$f'(t)=-5te^{-t}$, \ $f''(t)=5(t-1)e^{-t}$: $f'$ es mínima en \res{t=1} ($f'(1)=-\frac5e$). \ $\lim_{t\to+\infty}f(t)=\res{0}$."),
)

# =====================================================================
# 9. Problemes d'optimització
P_ = 320 / x + R(5, 2) * x**2; crit(P_, [4], 0.1, 50); eq(P_.subs(x, 4), 120)
A_ = 2 * x * (12 - x**2); crit(A_, [2], 0.01, sq(12)); eq(A_.subs(x, 2), 32)
S_ = sq(3) / 4 * x**2 + ((240 - 3 * x) / 4)**2; crit(S_, [720 / (9 + 4 * sq(3))], 0, 80); eq(3 * 720 / (9 + 4 * sq(3)), 2160 / (9 + 4 * sq(3)))
A_ = (80 - x) * (40 + R(5, 4) * x); crit(A_, [24], 0, 32); eq(A_.subs(x, 24), 3920)
A_ = x * sq(400 - x**2) / 4; crit(A_, [sq(200)], 0.01, 19.99); eq(A_.subs(x, sq(200)), 50)
D_ = x**4 - 3 * x**2 + 4; crit(D_, [-sq(R(3, 2)), 0, sq(R(3, 2))], -2, 2); eq(D_.subs(x, 2), 8)
A_ = 624 + 6 * x + 2400 / x; crit(A_, [20], 0.1, 100)
A2 = x**2 * (900 - 60 * x); crit(A2, [0, 10], 0, 15); eq(10 * sq(900 - 600) / 2, 50 * sq(3))
A_ = 4 * x - x**2 / 2 - pi * x**2 / 8; crit(A_, [16 / (4 + pi)], 0, 10); eq((8 - (16 / (4 + pi)) * (1 + pi / 2)) / 2, 8 / (4 + pi))
C_ = 140 * x**2 + 70 * 4 * x * 64 / x**2; crit(C_, [4], 0.1, 50)
H_ = x**2 + 4 / x**2; crit(H_, [-sq(2), sq(2)], -50, 50)
G_ = 6 * x + 2400 / x + 60; crit(G_, [20], 0.1, 100); eq(G_.subs(x, 20), 300)
A_ = 40 * x - x**2 / 2 - pi * x**2 / 8; crit(A_, [160 / (4 + pi)], 0, 60); eq(40 - (160 / (4 + pi)) * (2 + pi) / 4, 80 / (4 + pi))
A_ = x * (4 - x**2) / 2; crit(A_, [-2 / sq(3), 2 / sq(3)], -2, 2); eq((4 - R(4, 3)), R(8, 3)); eq(sq(R(4, 3) + R(64, 9)), sq(76) / 3)
T_ = sq(4 + x**2) / 3 + (3 - x) / 5; crit(T_, [R(3, 2)], 0, 3)
F_ = 5 - x + 2 * sq(x**2 + 36); crit(F_, [sq(12)], 0, 5); eq(F_.subs(x, sq(12)), 5 + 6 * sq(3))
V_ = x * (20 - 2 * x) * (30 - 2 * x); crit(V_, [(25 - 5 * sq(7)) / 3, (25 + 5 * sq(7)) / 3], 0, 50); ok(N((25 - 5 * sq(7)) / 3).real < 10)
S_ = pi * x**2 + 2 * pi * x * 216 / x**2; crit(S_, [6], 0.1, 50)
A_ = x * exp(-2 * x); ext(A_, R(1, 2), 'max', 1 / (2 * E))
S_ = x**2 / 16 + x**2 / 4 + (140 - 3 * x)**2 / 16; crit(S_, [30], 0, 46)
V_ = x - 2 * x**3 / 3; crit(V_, [-1 / sq(2), 1 / sq(2)], -5, 5); eq((3 - 1) / (3 / sq(2)), 2 * sq(2) / 3)
sec("Problemas de optimización",
 (2, r"\pau{Comunidad Valenciana, ordinaria 2025} Una empresa quiere hacer cajas de 80 cm$^3$ con base y tapa cuadradas. El material de las paredes laterales cuesta 1 céntimo por cm$^2$ y el de la base y la tapa es un 25\,\% más caro." + tasks(1, [r"Escribe el precio del material $P(x)$ en función del lado $x$ de la base.", r"Halla las dimensiones de la caja más barata.", r"¿Cuál es el precio en este caso?"])
     + recorda(r"Volumen: $x^2h=80$. Área lateral: $4xh$; base y tapa: $2x^2$."),
     tasks(1, [r"$h=\frac{80}{x^2}$: \ $\res{P(x)=\frac{320}{x}+2{,}5x^2}$ céntimos", r"$P'(x)=-\frac{320}{x^2}+5x=0\Rightarrow x^3=64$: \res{4\times4\times5\text{ cm}}", r"$P(4)=80+40=\res{120\text{ céntimos}=1{,}20\text{ €}}$"])),
 (2, r"\pau{Comunidad Valenciana, ordinaria 2023} El corte vertical de la entrada a una plaza amurallada tiene forma de parábola $y=-x^2+12$ ($x$, $y$ en metros; $y=0$ es el suelo). Queremos poner una puerta rectangular con las dos esquinas de arriba sobre la parábola y las de abajo en el suelo. Calcula las dimensiones de la puerta de superficie máxima y el área de la parte de la entrada que queda tapada con piedra.",
     r"$A(x)=2x(12-x^2)$, $0<x<\sqrt{12}$; $A'=24-6x^2=0\Rightarrow x=2$: puerta de \res{4\text{ m}\times8\text{ m}} ($32$ m$^2$). Área de la entrada: $\int_{-\sqrt{12}}^{\sqrt{12}}(12-x^2)\,dx=16\sqrt{12}$; piedra: \res{16\sqrt{12}-32\approx23{,}4\text{ m}^2}."),
 (2, r"\pau{Comunidad Valenciana, ordinaria 2022} Se quiere construir un cuadrado y un triángulo equilátero cortando en dos partes un cable de acero de 240 m." + tasks(1, [r"Calcula la suma de las áreas en función del lado $x$ del triángulo.", r"Calcula la longitud de cable que hace falta para el triángulo para que la suma de las áreas sea mínima."]),
     tasks(1, [r"$\res{S(x)=\frac{\sqrt3}{4}x^2+\left(\frac{240-3x}{4}\right)^2}$, $0\leq x\leq80$", r"$S'=\frac{\sqrt3}{2}x-\frac38(240-3x)=0\Rightarrow x=\frac{720}{9+4\sqrt3}$; cable: $3x=\res{\frac{2160}{9+4\sqrt3}\approx135{,}6\text{ m}}$"])),
 (2, r"\pau{Comunidad Valenciana, ordinaria 2021} Un espejo cuadrado de 80 cm de lado se ha roto por una esquina; el trozo caído es un triángulo rectángulo de catetos 32 cm (horizontal) y 40 cm (vertical). Recortamos una pieza rectangular $R$ con un vértice $(x,y)$ sobre la línea de rotura y el vértice opuesto en la esquina contraria del espejo. Halla el área de $R$ en función de $x$ ($0\leq x\leq32$), las dimensiones de $R$ de área máxima y esta área.",
     r"$y=40-\frac54x$; $A(x)=(80-x)(80-y)=\res{-\frac54x^2+60x+3200}$; $A'=0\Rightarrow x=24$: \res{56\text{ cm}\times70\text{ cm}}, $A=\res{3920\text{ cm}^2}$."),
 (2, r"\pau{Comunidad Valenciana, ordinaria 2020} En un triángulo isósceles los dos lados iguales miden 10 cm. Expresa el área en función de la longitud $x$ del tercer lado, estudia su monotonía en $[0,20]$ y halla el valor de $x$ que hace máxima el área.",
     r"$A(x)=\frac{x\sqrt{400-x^2}}{4}$; crece en $\left(0,\sqrt{200}\right)$ y decrece en $\left(\sqrt{200},20\right)$: máximo para $\res{x=10\sqrt2}$, $A=\res{50\text{ cm}^2}$ (el triángulo es rectángulo)."),
 (2, r"\pau{Comunidad Valenciana, julio 2019} Un proyectil unido al punto $(0,2)$ por una cuerda elástica recorre la curva $y=4-x^2$ entre $(-2,0)$ y $(2,0)$. Halla la distancia entre un punto de la curva y $(0,2)$ en función de $x$, y los puntos de la curva más alejados y más próximos a $(0,2)$.",
     r"$d(x)=\sqrt{x^4-3x^2+4}$. Derivamos el radicando: $4x^3-6x=0\Rightarrow x=0,\ \pm\sqrt{\frac32}$. Más próximos: \res{\left(\pm\sqrt{\tfrac32},\tfrac52\right)}; más alejados (comparando con los extremos): \res{(\pm2,0)}, con $d=\sqrt8$."),
 (2, r"\pau{Comunidad Valenciana, julio 2018} Dentro de una cartulina rectangular se quiere hacer un dibujo rectangular $R$ de 600 cm$^2$, con márgenes de 3 cm arriba y abajo y de 2 cm a los lados. Calcula el área de la cartulina en función de la base $x$ de $R$ y las dimensiones de la cartulina de área mínima.",
     r"$A(x)=(x+4)\left(\frac{600}{x}+6\right)=\res{624+6x+\frac{2400}{x}}$; $A'=6-\frac{2400}{x^2}=0\Rightarrow x=20$: cartulina de \res{24\text{ cm}\times36\text{ cm}}."),
 (3, r"\pau{Comunidad Valenciana, julio 2017} Se considera el triángulo de vértices $O(0,0)$, $A(x,y)$ y $B(0,y)$, con $x,y>0$, tal que $\overline{OA}+\overline{AB}=30$ m. Halla el área en función de $x$, el valor de $x$ para el que es máxima y esta área.",
     r"$\sqrt{x^2+y^2}=30-x\Rightarrow y=\sqrt{900-60x}$; $\res{A(x)=\frac{x\sqrt{900-60x}}{2}}$, $0< x<15$. Maximizamos $A^2$: $(900x^2-60x^3)'=0\Rightarrow\res{x=10}$; $A=5\sqrt{300}=\res{50\sqrt3\approx86{,}6\text{ m}^2}$."),
 (2, r"\pau{Andalucía, ordinaria 2026} Una ventana tiene forma de rectángulo coronado por un semicírculo. Si el perímetro de la ventana mide 8 m, halla las dimensiones que permiten la máxima entrada de luz.",
     r"Base $x$, altura $y$: $x+2y+\frac{\pi x}{2}=8$, $A=xy+\frac{\pi x^2}{8}=4x-\frac{x^2}{2}-\frac{\pi x^2}{8}$; $A'=0\Rightarrow\res{x=\frac{16}{4+\pi}\approx2{,}24\text{ m}}$, $\res{y=\frac{8}{4+\pi}\approx1{,}12\text{ m}}$."),
 (2, r"\pau{Aragón, extraordinaria 2021} Se quiere construir un depósito abierto (sin tapa) en forma de prisma de base cuadrada y 64 m$^3$ de capacidad. Los laterales cuestan 70 €/m$^2$ y la base, 140 €/m$^2$. Halla las dimensiones del depósito más económico.",
     r"$h=\frac{64}{x^2}$; $C(x)=140x^2+70\cdot4xh=140x^2+\frac{17\,920}{x}$; $C'=280x-\frac{17\,920}{x^2}=0\Rightarrow x^3=64$: un \res{\text{cubo de 4 m de arista}}."),
 (2, r"\pau{Aragón, septiembre 2018} De todos los triángulos rectángulos que tienen un área de 1 cm$^2$, halla el que tiene la hipotenusa más corta y da las longitudes de los tres lados.",
     r"Catetos $x$ y $\frac2x$: $h^2=x^2+\frac{4}{x^2}$; $(h^2)'=2x-\frac{8}{x^3}=0\Rightarrow x=\sqrt2$: catetos \res{\sqrt2\text{ y }\sqrt2\text{ cm}}, hipotenusa \res{2\text{ cm}}."),
 (2, r"\pau{Canarias, ordinaria 2023} Se quiere construir una Casa de la Juventud de 240 m$^2$ rodeada de una zona ajardinada que deja 3 m arriba, 3 m abajo, 3 m a la izquierda y 7 m a la derecha. ¿Qué dimensiones tiene que tener la casa para que la zona ajardinada sea mínima? ¿Cuál es esta área?",
     r"Casa $x\times\frac{240}{x}$: jardín $=(x+10)\left(\frac{240}{x}+6\right)-240=6x+\frac{2400}{x}+60$; mínimo para $x=20$: casa de \res{20\text{ m}\times12\text{ m}}, jardín de \res{300\text{ m}^2}."),
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2023} Un aparcamiento tiene forma de rectángulo de lados $h$ y $r$ con un semicírculo de radio $\frac h2$ adosado al lado $h$. Si la valla mide 80 m de perímetro, ¿cuánto tienen que valer $h$ y $r$ para que el área sea máxima?",
     r"$h+2r+\frac{\pi h}{2}=80$, $A=hr+\frac{\pi h^2}{8}=40h-\frac{h^2}2-\frac{\pi h^2}{8}$; $A'=0\Rightarrow\res{h=\frac{160}{4+\pi}\approx22{,}4\text{ m}}$, $\res{r=\frac{80}{4+\pi}\approx11{,}2\text{ m}}$."),
 (2, r"\pau{Galicia, julio 2019} De todos los triángulos rectángulos del primer cuadrante que tienen un vértice en el origen, otro sobre la parábola $y=4-x^2$, un cateto sobre el eje $X$ y el otro paralelo al eje $Y$, halla los catetos y la hipotenusa del de área máxima.",
     r"$A(x)=\frac{x(4-x^2)}{2}$, $0< x<2$; $A'=\frac{4-3x^2}{2}=0\Rightarrow x=\frac{2}{\sqrt3}$: catetos \res{\tfrac{2}{\sqrt3}\text{ y }\tfrac83}, hipotenusa \res{\tfrac{\sqrt{76}}{3}}."),
 (2, r"\pau{La Rioja, extraordinaria 2024} Un nadador está a 2 km de la playa, enfrente del puesto de la Cruz Roja. Quiere ir a las duchas, en la playa y a 3 km de la Cruz Roja. Nada a 3 km/h y camina por la arena a 5 km/h. ¿Dónde tiene que llegar nadando para tardar lo mínimo?",
     r"Si llega a $x$ km de la Cruz Roja: $T(x)=\frac{\sqrt{4+x^2}}{3}+\frac{3-x}{5}$; $T'=0\Rightarrow5x=3\sqrt{4+x^2}\Rightarrow x=\frac32$: \res{\text{a 1,5 km de la Cruz Roja}} (a medio camino)."),
 (3, r"\pau{Murcia, junio 2019} En un triángulo isósceles de base 12 cm (lado desigual) y altura 5 cm, buscamos un punto $A$ de la altura, a distancia $x$ de la base, tal que la suma de las distancias de $A$ a los tres vértices sea mínima. Comprueba que esta suma es $f(x)=5-x+2\sqrt{x^2+36}$, halla $x$ y el valor mínimo.",
     r"$f'(x)=-1+\frac{2x}{\sqrt{x^2+36}}=0\Rightarrow3x^2=36\Rightarrow\res{x=\sqrt{12}=2\sqrt3}$; $f\left(\sqrt{12}\right)=\res{5+6\sqrt3\approx15{,}39\text{ cm}}$."),
 (2, r"\pau{Navarra, ordinaria 2026} De una hoja de 20 cm $\times$ 30 cm se recorta un cuadrado en cada esquina para hacer una caja sin tapa doblando las solapas. Calcula el lado del cuadrado para que el volumen sea máximo.",
     r"$V(x)=x(20-2x)(30-2x)$, $0< x<10$; $V'=12x^2-200x+600=0\Rightarrow\res{x=\frac{25-5\sqrt7}{3}\approx3{,}92\text{ cm}}$ (la otra raíz no es del dominio)."),
 (2, r"\pau{País Vasco, extraordinaria 2024} Una empresa fabrica tazas cilíndricas (sin tapa) de $216\pi$ cm$^3$ y quiere que sean tan económicas como sea posible. ¿Qué dimensiones tienen que tener?",
     r"$r^2h=216$, $S=\pi r^2+2\pi rh=\pi r^2+\frac{432\pi}{r}$; $S'=0\Rightarrow r^3=216$: \res{r=6\text{ cm},\ h=6\text{ cm}}."),
 (2, r"\pau{Cataluña, extraordinaria 2024} Para cada punto $(x,y)$ de la curva $y=e^{-2x}$ con $x>0$, considera el rectángulo de vértices $(0,0)$, $(x,0)$, $(0,y)$ y $(x,y)$. Comprueba que el de área máxima es el de $x=\frac12$ y calcula su área.",
     r"$A(x)=xe^{-2x}$, $A'=(1-2x)e^{-2x}=0\Rightarrow x=\frac12$ ($A'$ pasa de $+$ a $-$): \res{A=\tfrac{1}{2e}\text{ u}^2}."),
 (3, r"\pau{Canarias, junio 2018} Un hilo de 140 m se divide en tres trozos, uno de los cuales mide el doble que otro. Con cada trozo se hace un cuadrado. ¿Qué longitud tiene que tener cada trozo para que la suma de las áreas sea mínima?",
     r"Trozos $x$, $2x$ y $140-3x$: $S=\frac{x^2}{16}+\frac{4x^2}{16}+\frac{(140-3x)^2}{16}$; $S'=\frac{10x-6(140-3x)}{16}=0\Rightarrow x=30$: \res{30,\ 60\text{ y }50\text{ m}}."),
 (2, r"\pau{Asturias, extraordinaria 2025} Se quiere construir una caja sin tapa con dos caras paralelas cuadradas de lado $x$ y tres caras rectangulares de lados $x$ y $y$. Si se quieren gastar 3 m$^2$ de material, ¿qué valores de $x$ y $y$ hacen máxima la capacidad?",
     r"$2x^2+3xy=3\Rightarrow y=\frac{3-2x^2}{3x}$; $V=x^2y=x-\frac{2x^3}{3}$, $V'=1-2x^2=0$: \res{x=\tfrac{\sqrt2}{2}\approx0{,}71\text{ m}}, \res{y=\tfrac{2\sqrt2}{3}\approx0{,}94\text{ m}}."),
)

# =====================================================================
# 10–12. Representació de funcions
REP = recorda(r"Dominio, simetría, cortes, asíntotas, monotonía y extremos, curvatura e inflexión; después situamos toda la información y dibujamos.")
def rep(fn): return r"Haz el estudio completo y representa " + fn + "."
f_ = x / (x**2 + 1); ext(f_, 1, 'max', R(1, 2)); ext(f_, -1, 'min', -R(1, 2))
f_ = (x**2 + 3) / (x**2 - 4); ext(f_, 0, 'max', -R(3, 4)); L(f_, sp.oo, 1)
f_ = (x**2 + 1) / x; L(f_ - x, sp.oo, 0)
f_ = x**3 - 6 * x**2 + 9 * x; ext(f_, 1, 'max', 4); ext(f_, 3, 'min', 0)
f_ = 4 * x**3 - x**4; ext(f_, 3, 'max', 27); infl(f_, 0, 0); infl(f_, 2, 16)
f_ = 2 * x**2 / (1 - x); ext(f_, 0, 'min', 0); ext(f_, 2, 'max', -8); L(f_ - (-2 * x - 2), sp.oo, 0)
f_ = x * exp(1 - x**2); ext(f_, sq(2) / 2, 'max', sq(E / 2)); infl(f_, 0, 0); infl(f_, sq(R(3, 2)))
f_ = 1 / x + ln(x + 1); ext(f_, (1 - sq(5)) / 2, 'max'); ext(f_, (1 + sq(5)) / 2, 'min')
f_ = x / ln(x); ext(f_, E, 'min', E); infl(f_, E**2, E**2 / 2)
f_ = x**2 * exp(-x); ext(f_, 0, 'min', 0); ext(f_, 2, 'max', 4 / E**2); infl(f_, 2 - sq(2)); infl(f_, 2 + sq(2))
f_ = x * sq(18 - x**2); ext(f_, 3, 'max', 9); ext(f_, -3, 'min', -9)
f_ = 2 * sin(x) + sin(2 * x); ext(f_, pi / 3, 'max', 3 * sq(3) / 2); ext(f_, 5 * pi / 3, 'min', -3 * sq(3) / 2); infl(f_, pi); infl(f_, sp.acos(-R(1, 4)))
f_ = cos(pi * x / 9) + 2; ext(f_, 9, 'min', 1); eq(f_.subs(x, 12), R(3, 2))
f_ = sin(x)**2; ext(f_, pi / 2, 'max', 1); infl(f_, pi / 4, R(1, 2))
f_ = x + sin(x); infl(f_, pi, pi)
sec("Representación de funciones polinómicas y racionales",
 (1, rep(r"\pau{Andalucía, ordinaria 2021} " + fx(r'4x^3-x^4')) + REP,
     r"Dominio $\mathbb R$. Cortes $(0,0)$ y $(4,0)$. $f'=4x^2(3-x)$: crece en $(-\infty,3)$, decrece en $(3,+\infty)$; \res{\text{máx. }(3,27)}. $f''=12x(2-x)$: \res{\text{P.I. }(0,0)\text{ y }(2,16)}; cóncava fuera de $(0,2)$."
     + cen(graf([lambda v: 4 * v**3 - v**4], (-1.5, 4.5, -10, 32), pts=[(0, 0), (4, 0)], mx=[(3, 27)], ip=[(0, 0), (2, 16)]))),
 (2, rep(r"\pau{Comunidad Valenciana, extraordinaria 2025} " + fx(r'\dfrac{x}{x^2+1}')),
     r"Dominio $\mathbb R$, impar, corte $(0,0)$. AH $\res{y=0}$. $f'=\frac{1-x^2}{(x^2+1)^2}$: \res{\text{mín. }\left(-1,-\tfrac12\right)}, \res{\text{máx. }\left(1,\tfrac12\right)} (también absolutos). P.I. en $x=0$, $x=\pm\sqrt3$."
     + cen(graf([lambda v: v / (v * v + 1)], (-6, 6, -0.8, 0.8), ha=[0], pts=[(0, 0)], mx=[(1, 0.5)], mn=[(-1, -0.5)], ip=[(-r3, -r3 / 4), (r3, r3 / 4)]))),
 (2, rep(r"\pau{Comunidad Valenciana, ordinaria 2022} " + fx(r'\dfrac{x^2+3}{x^2-4}')),
     r"Dominio $\mathbb R-\{\pm2\}$, par, corte $\left(0,-\frac34\right)$. AV $\res{x=\pm2}$, AH $\res{y=1}$. $f'=\frac{-14x}{(x^2-4)^2}$: crece en $(-\infty,-2)\cup(-2,0)$, decrece en $(0,2)\cup(2,+\infty)$; \res{\text{máx. }\left(0,-\tfrac34\right)}. Sin inflexión."
     + cen(graf([lambda v: (v * v + 3) / (v * v - 4)], (-6, 6, -6, 7), va=[-2, 2], ha=[1], mx=[(0, -0.75)]))),
 (2, rep(r"\pau{Comunidad Valenciana, junio 2017} " + fx(r'\dfrac{x^2+1}{x}')),
     r"Dominio $\mathbb R-\{0\}$, impar, sin cortes. AV $\res{x=0}$, AO $\res{y=x}$. \res{\text{máx. }(-1,-2)}, \res{\text{mín. }(1,2)}. $f''=\frac{2}{x^3}$: cóncava en $(-\infty,0)$, convexa en $(0,+\infty)$."
     + cen(graf([lambda v: (v * v + 1) / v], (-5, 5, -7, 7), va=[0], oa=[(1, 0)], mx=[(-1, -2)], mn=[(1, 2)]))),
 (3, rep(r"\pau{Asturias, extraordinaria 2022} " + fx(r'\dfrac{2x^2}{1-x}')),
     r"Dominio $\mathbb R-\{1\}$, corte $(0,0)$. AV $\res{x=1}$, AO $\res{y=-2x-2}$. $f'=\frac{2x(2-x)}{(1-x)^2}$: \res{\text{mín. }(0,0)}, \res{\text{máx. }(2,-8)}. Sin inflexión."
     + cen(graf([lambda v: 2 * v * v / (1 - v)], (-5, 6, -20, 12), va=[1], oa=[(-2, -2)], mn=[(0, 0)], mx=[(2, -8)]))),
)
sec("Representación de funciones radicales, exponenciales y logarítmicas",
 (2, rep(r"\pau{Comunidad Valenciana, extraordinaria 2021} " + fx(r'x\,e^{1-x^2}')) + REP,
     r"Dominio $\mathbb R$, impar, corte $(0,0)$, AH $\res{y=0}$. $f'=e^{1-x^2}(1-2x^2)$: \res{\text{mín. }\left(-\tfrac{\sqrt2}{2},-\sqrt{\tfrac e2}\right)}, \res{\text{máx. }\left(\tfrac{\sqrt2}{2},\sqrt{\tfrac e2}\right)}. P.I. en $x=0$ y $x=\pm\sqrt{\frac32}$."
     + cen(graf([lambda v: v * me(1 - v * v)], (-3, 3, -1.5, 1.5), ha=[0], pts=[(0, 0)], mx=[(r2 / 2, math.sqrt(math.e / 2))], mn=[(-r2 / 2, -math.sqrt(math.e / 2))]))),
 (2, rep(r"\pau{Comunidad Valenciana, ordinaria 2023} " + fx(r'\dfrac1x+\ln(x+1)')),
     r"Dominio $(-1,0)\cup(0,+\infty)$. AV $\res{x=-1}$ y $\res{x=0}$. $f'=\frac{x^2-x-1}{x^2(x+1)}$: \res{\text{máx. en }x=\tfrac{1-\sqrt5}{2}}, \res{\text{mín. en }x=\tfrac{1+\sqrt5}{2}}."
     + cen(graf([(lambda v: 1 / v + mln(v + 1), -0.999, 8)], (-1.3, 6, -6, 6), va=[-1, 0], mx=[((1 - math.sqrt(5)) / 2, 1 / ((1 - math.sqrt(5)) / 2) + mln((1 - math.sqrt(5)) / 2 + 1))], mn=[((1 + math.sqrt(5)) / 2, 1 / ((1 + math.sqrt(5)) / 2) + mln((1 + math.sqrt(5)) / 2 + 1))]))),
 (2, rep(r"\pau{Madrid, extraordinaria 2026} " + fx(r'\dfrac{x}{\ln x}')),
     r"Dominio $(0,1)\cup(1,+\infty)$. AV $\res{x=1}$; $\lim_{x\to0^+}f=0$. $f'=\frac{\ln x-1}{\ln^2x}$: decrece en $(0,1)\cup(1,e)$, crece en $(e,+\infty)$; \res{\text{mín. }(e,e)}. $f''=\frac{2-\ln x}{x\ln^3x}$: \res{\text{P.I. }\left(e^2,\tfrac{e^2}{2}\right)}."
     + cen(graf([(lambda v: v / mln(v), 0.001, 12)], (-0.5, 12, -8, 10), va=[1], mn=[(math.e, math.e)], ip=[(math.e**2, math.e**2 / 2)]))),
 (2, rep(r"\pau{País Vasco, julio 2018} " + fx(r'x^2e^{-x}')),
     r"Dominio $\mathbb R$, corte $(0,0)$, $f\geq0$. AH $\res{y=0}$ cuando $x\to+\infty$. $f'=x(2-x)e^{-x}$: \res{\text{mín. }(0,0)}, \res{\text{máx. }\left(2,\tfrac{4}{e^2}\right)}. P.I. en $x=2\pm\sqrt2$."
     + cen(graf([lambda v: v * v * me(-v)], (-1.5, 9, -0.2, 1.2), ha=[0], mn=[(0, 0)], mx=[(2, 4 / math.e**2)], ip=[(2 - r2, (2 - r2)**2 * me(r2 - 2)), (2 + r2, (2 + r2)**2 * me(-2 - r2))]))),
 (3, rep(r"\pau{Murcia, septiembre 2018} " + fx(r'x\sqrt{18-x^2}') + " (en todo su dominio)"),
     r"Dominio $\left[-3\sqrt2,3\sqrt2\right]$, impar, cortes $(0,0)$ y $\left(\pm3\sqrt2,0\right)$ (con tangente vertical). $f'=\frac{18-2x^2}{\sqrt{18-x^2}}$: \res{\text{mín. }(-3,-9)}, \res{\text{máx. }(3,9)}."
     + cen(graf([(lambda v: v * msq(18 - v * v), -3 * r2, 3 * r2)], (-5, 5, -10, 10), pts=[(0, 0), (-3 * r2, 0), (3 * r2, 0)], mn=[(-3, -9)], mx=[(3, 9)]))),
)
sec("Representación de funciones trigonométricas y a trozos",
 (2, rep(fx(r'2\sin x+\sin2x')) + REP,
     r"Período $2\pi$, impar. Cortes $x=k\pi$. \res{\text{máx. }\left(\tfrac\pi3,\tfrac{3\sqrt3}{2}\right)}, \res{\text{mín. }\left(\tfrac{5\pi}3,-\tfrac{3\sqrt3}{2}\right)} ($+2k\pi$); en $x=\pi$, $f'=0$ sin extremo. P.I. en $x=k\pi$ y donde $\cos x=-\frac14$."
     + cen(graf([lambda v: 2 * ms(v) + ms(2 * v)], (-1, 7.3, -3, 3), mx=[(PI / 3, 3 * r3 / 2)], mn=[(5 * PI / 3, -3 * r3 / 2)], ip=[(PI, 0)], pts=[(0, 0), (2 * PI, 0)], xt=[(PI / 2, r'\frac\pi2'), (PI, r'\pi'), (3 * PI / 2, r'\frac{3\pi}2'), (2 * PI, r'2\pi')]))),
 (2, r"\pau{Comunidad Valenciana, ordinaria 2026 · Madrid, ordinaria 2025} Un decorador pinta en una pared de 12 m de largo y 3 m de alto la curva $f(x)=\cos\frac{\pi x}{9}+2$. Dibújala en $[0,12]$ con los cortes con los ejes, los extremos absolutos y la monotonía. ¿Está la curva dentro de la pared?",
     r"Corta OY en $(0,3)$; no corta OX. $f'=-\frac\pi9\sin\frac{\pi x}{9}$: decrece en $[0,9]$, crece en $[9,12]$; \res{\text{máx. abs. }(0,3)}, \res{\text{mín. abs. }(9,1)}, $f(12)=\frac32$. Como $1\leq f\leq3$, \rest{sí}."
     + cen(graf([(lambda v: mc(PI * v / 9) + 2, 0, 12)], (-0.5, 12.5, 0, 3.5), pts=[(12, 1.5)], mx=[(0, 3)], mn=[(9, 1)]))),
 (2, r"\pau{Galicia, ordinaria 2023} Estudia si $f(x)=x+\sin x$ tiene extremos o puntos de inflexión en $(0,2\pi)$ y esboza su gráfica.",
     r"$f'=1+\cos x\geq0$: creciente, \rest{sin extremos}. $f''=-\sin x$: cóncava en $(0,\pi)$, convexa en $(\pi,2\pi)$; \res{\text{P.I. }(\pi,\pi)} (con tangente horizontal)."
     + cen(graf([(lambda v: v + ms(v), 0, 2 * PI)], (-0.3, 6.6, -0.3, 6.6), ip=[(PI, PI)], xt=[(PI, r'\pi'), (2 * PI, r'2\pi')]))),
 (2, rep(fx(r'\sin^2x')),
     r"Período $\pi$, par, $0\leq f\leq1$. \res{\text{mín. }(k\pi,0)}, \res{\text{máx. }\left(\tfrac\pi2+k\pi,1\right)}. $f''=2\cos2x$: P.I. en $x=\frac\pi4+\frac{k\pi}2$."
     + cen(graf([lambda v: ms(v)**2], (-3.5, 6.6, -0.3, 1.4), mn=[(0, 0), (PI, 0), (2 * PI, 0), (-PI, 0)], mx=[(PI / 2, 1), (3 * PI / 2, 1), (-PI / 2, 1)], xt=[(-PI, r'-\pi'), (PI, r'\pi'), (2 * PI, r'2\pi')]))),
 (2, r"\pau{Andalucía, ordinaria 2022} Sea " + '$' + pw((r'2x+4', 'x<0'), (r'(x-2)^2', r'x\geq0')) + '$' + r". Calcula los puntos de corte con el eje de abscisas, estudia su continuidad, su derivabilidad y sus extremos, y esboza la gráfica.",
     r"Cortes $(-2,0)$ y $(2,0)$. Continua ($4=4$) pero no derivable en 0 ($f'(0^-)=2\neq-4=f'(0^+)$). Crece en $(-\infty,0)\cup(2,+\infty)$ y decrece en $(0,2)$: \res{\text{máx. }(0,4)} (punto anguloso) y \res{\text{mín. }(2,0)}."
     + cen(graf([(lambda v: 2 * v + 4, -4, 0), (lambda v: (v - 2)**2, 0, 5)], (-3.5, 5, -2, 6), pts=[(-2, 0)], mx=[(0, 4)], mn=[(2, 0)]))),
 (3, rep(fx(r'\left|x^2-4x\right|')),
     r"$f=x^2-4x$ si $x\leq0$ o $x\geq4$, y $-x^2+4x$ si $0< x<4$. \res{\text{mín. }(0,0),\ (4,0)} (puntos angulosos), \res{\text{máx. }(2,4)}; convexa fuera de $[0,4]$ y cóncava dentro."
     + cen(graf([lambda v: abs(v * v - 4 * v)], (-2, 6, -1, 8), mn=[(0, 0), (4, 0)], mx=[(2, 4)]))),
)

# =====================================================================
print(NCHK[0], 'comprobaciones correctas')
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={L'Hôpital, indeterminacions, monotonia, extrems, curvatura, punts d'inflexió, Rolle, valor mitjà, optimització, representació de funcions, PAU}"
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

TIT = "Aplicaciones de la derivada"
def build(sol):
    tt = 'Soluciones de la ficha' if sol else "Ficha de ejercicios"
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    p = preambul(pre, pdftitle='%s de la unidad 7: %s' % (tt, TIT), capcalera='%s · Unidad 7: %s' % (tt, TIT),
                 pdfkeywords="L'Hôpital, indeterminaciones, monotonía, extremos, curvatura, puntos de inflexión, Rolle, valor medio, optimización, representación de funciones, PAU", curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 7' if sol else "Ficha de ejercicios · Unidad 7") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.2cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Las gráficas de las soluciones marcan en verde los máximos, en rojo los mínimos y en violeta los puntos de inflexión; las líneas discontinuas son asíntotas. Puedes comprobar los estudios completos con la calculadora de los apuntes interactivos."
             if sol else r"Resuelve los ejercicios en el cuaderno justificando cada paso. Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de la Comunidad Valenciana y de otras comunidades autónomas, traducidos al castellano. Puedes comprobar los resultados con las herramientas de los apuntes interactivos (L'Hôpital paso a paso, estudio completo de una función, optimización\dots).") + r'''
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
    name = 't7-fitxa-solucions-es.tex' if sol else 't7-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'ejercicios,', npau, 'de la PAU de', len(regs), 'comunidades:', ', '.join(regs))
