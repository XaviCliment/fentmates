# Versió en castellà de genera.py. Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 9: Integrals) a partir
# d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les estrelles no es mostren.
# Les seccions segueixen els apunts interactius (materials/2batx-mii/t9-integrals.html) i l'estructura de la unitat 8 de
# CCSS, amb més dificultat i amb les integrals trigonomètriques, el canvi de variable, la integració per parts, les funcions
# racionals i el teorema fonamental del càlcul.
# Els exercicis marcats amb \pau{...} són de la PAU de València i d'altres comunitats, traduïts al valencià i presos del
# recull «Ejercicios de análisis en pruebas de acceso a la universidad de toda España» (curs 2026/27) de Juan Antonio
# Martínez García (www.ebaumatematicas.com). Abans d'escriure els fitxers, sympy comprova totes les primitives (derivant-les),
# les integrals definides, els paràmetres i les àrees de les solucions. Les gràfiques dels recintes es dibuixen amb TikZ
# (graf, copiat de la unitat 7 de MII, i grafA, que hi afegeix les regions ombrejades).
# Ús: python3 genera.py && pdflatex t9-fitxa-exercicis.tex (dues vegades) && pdflatex t9-fitxa-solucions.tex (dues vegades)
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


# ---------- comprovacions d'integrals ----------
def prim(f, F, pts=(0.37, 0.81, 1.43, 2.2)):
    """F' = f (numéricamente en unos cuantos puntos donde ambas existen)"""
    d = sp.diff(F, x); k = 0
    for p in pts:
        a, b = N(d.subs(x, p)), N(f.subs(x, p))
        if abs(b) > 1e12 or b != b: continue
        assert abs(a - b) < 1e-9 * (1 + abs(b)), (f, F, p, a, b); k += 1
    ok(k >= 2)
def defi(f, a, b, val):
    eq(sp.Integral(f, (x, a, b)).evalf(30), val)
def area(f, g, cuts, val):
    """área entre f y g (g = 0 para el eje) sumando |∫| en los trozos dados"""
    h = f - g; s = 0
    for p, q in zip(cuts, cuts[1:]):
        s += abs(N(sp.Integral(h, (x, p, q)).evalf(30)))
        m = (N(p).real + N(q).real) / 2
        for r in cuts[1:-1]: ok(abs(N(h.subs(x, r))) < 1e-9)
    eq(s, val)
def shade(f, g, a, b, col='teal!25'):
    pts = []
    for i in range(121):
        xx = a + (b - a) * i / 120; pts.append('(%.3f,%.3f)' % (xx, f(xx)))
    for i in range(120, -1, -1):
        xx = a + (b - a) * i / 120; pts.append('(%.3f,%.3f)' % (xx, g(xx)))
    return r'\fill[%s] ' % col + '--'.join(pts) + '--cycle;'
def grafA(curves, box, fills=(), **kw):
    """como graf, pero con recintos sombreados (lista de (f, g, a, b))"""
    return _ins(graf(curves, box, **kw), '\n'.join(shade(*q) for q in fills))
def _ins(s, sh):
    i = s.index(r'\begin{scope}\clip'); j = s.index('\n', i)
    return s[:j + 1] + sh + '\n' + s[j + 1:]
Z = lambda v: 0

# =====================================================================
# 1. Primitiva i integral indefinida
prim(x * sp.exp(x), x * sp.exp(x) - sp.exp(x)); prim(1 / sin(x), ln(tan(x / 2))); prim(2 / (1 + x**2)**2, atan(x) + x / (1 + x**2)); prim(x / sq(x**2 + 1), sq(x**2 + 1))
f_ = x**4 - 3 * x**2 + 4 * x - 3; ok(sp.expand(sp.diff(f_, x, 2) - (12 * x**2 - 6)) == 0); eq(sp.diff(f_, x).subs(x, 1), 2); eq(f_.subs(x, 1), -1)
ok(sp.simplify(sp.diff(x / 2 - sin(x) * cos(x) / 2, x) - sin(x)**2) == 0)
G_ = x**3 / 3 + a_ * x**2 + b_ * x + 5; ok(sp.expand(sp.diff(G_, x) - (x**2 + 2 * a_ * x + b_)) == 0)
sec("Primitiva e integral indefinida",
 (1, r"Comprueba, derivando, que $F$ es una primitiva de $f$:" + tasks(2, [r"$f(x)=xe^x$, \ $F(x)=xe^x-e^x$", r"$f(x)=\dfrac{1}{\sin x}$, \ $F(x)=\ln\left(\tan\dfrac x2\right)$",
                                                                       r"$f(x)=\dfrac{2}{\left(1+x^2\right)^2}$, \ $F(x)=\arctan x+\dfrac{x}{1+x^2}$", r"$f(x)=\dfrac{x}{\sqrt{x^2+1}}$, \ $F(x)=\sqrt{x^2+1}$"])
     + recorda(r"$\displaystyle\int f(x)\,dx=F(x)+C\iff F'(x)=f(x)$. Una primitiva siempre se puede comprobar derivándola."),
     tasks(1, [r"$F'=e^x+xe^x-e^x=\res{xe^x}$", r"$F'=\dfrac{\frac{1}{2\cos^2(x/2)}}{\tan(x/2)}=\dfrac{1}{2\sin\frac x2\cos\frac x2}=\res{\dfrac{1}{\sin x}}$",
               r"$F'=\dfrac{1}{1+x^2}+\dfrac{1-x^2}{(1+x^2)^2}=\res{\dfrac{2}{(1+x^2)^2}}$", r"$F'=\dfrac{2x}{2\sqrt{x^2+1}}=\res{\dfrac{x}{\sqrt{x^2+1}}}$"])),
 (2, r"\pau{Asturias, extraordinaria 2025} $G(x)=\frac13x^3+ax^2+bx+5$ es una primitiva de una función $g$, donde $a$ y $b$ son constantes." + tasks(1, [r"Determina $g(x)$ en función de $a$ y $b$.", r"Escribe todas las primitivas de $g$."]),
     tasks(1, [r"$g(x)=G'(x)=\res{x^2+2ax+b}$", r"$\res{\frac13x^3+ax^2+bx+C}$, $C\in\mathbb R$"])),
 (2, r"Halla la función $f$ que cumple $f''(x)=12x^2-6$ y cuya recta tangente en $x=1$ es $y=2x-3$.",
     r"$f'(x)=4x^3-6x+C_1$, $f'(1)=2\Rightarrow C_1=4$; $f(x)=x^4-3x^2+4x+C_2$, $f(1)=-1\Rightarrow C_2=-3$: \res{f(x)=x^4-3x^2+4x-3}."),
 (3, r"\pau{Aragón, ordinaria 2024} Calcula $a$, $b$ y $c$ para que $f(x)=ax+b\sin x\cos x+c$ sea una primitiva de $g(x)=\sin^2x$.",
     r"$f'(x)=a+b\left(\cos^2x-\sin^2x\right)=a+b\cos2x$ y $\sin^2x=\frac12-\frac12\cos2x$: \res{a=\frac12,\ b=-\frac12}, y \rest{$c$ cualquiera}."),
)

# =====================================================================
# 2. Integrals immediates
for f_, F_ in [(4 * x**3 - 6 * x + 2, x**4 - 3 * x**2 + 2 * x), ((x**2 + 1) / sq(x), R(2, 5) * x**R(5, 2) + 2 * sq(x)), (sp.exp(x) - 3**x, sp.exp(x) - 3**x / ln(3)), (2 / x - 5 / (1 + x**2), 2 * ln(x) - 5 * atan(x)),
               (3 * cos(x) - 2 * sin(x), 3 * sin(x) + 2 * cos(x)), (1 + tan(x)**2, tan(x)), (4 / sq(1 - x**2), 4 * sp.asin(x)), (1 / x**3, -1 / (2 * x**2)),
               (cos(x)**2, x / 2 + sin(2 * x) / 4), (tan(x)**2, tan(x) - x), ((sin(x) + cos(x))**2, x - cos(2 * x) / 2), ((x + 1)**2 / x, x**2 / 2 + 2 * x + ln(x)), ((2 * x - 1) / sp.cbrt(x), R(6, 5) * x**R(5, 3) - R(3, 2) * x**R(2, 3))]:
    prim(f_, F_, (0.31, 0.55, 0.77))
sec("Integrales inmediatas",
 (1, r"Calcula:" + tasks(2, [r"$\displaystyle\int\left(4x^3-6x+2\right)dx$", r"$\displaystyle\int\frac{x^2+1}{\sqrt x}\,dx$", r"$\displaystyle\int\left(e^x-3^x\right)dx$", r"$\displaystyle\int\left(\frac2x-\frac{5}{1+x^2}\right)dx$",
                             r"$\displaystyle\int(3\cos x-2\sin x)\,dx$", r"$\displaystyle\int\left(1+\tan^2x\right)dx$", r"$\displaystyle\int\frac{4}{\sqrt{1-x^2}}\,dx$", r"$\displaystyle\int\frac{dx}{x^3}$"])
     + recorda(r"$\int x^n\,dx=\frac{x^{n+1}}{n+1}$ ($n\neq-1$), $\int\frac{dx}x=\ln|x|$, $\int a^x\,dx=\frac{a^x}{\ln a}$, $\int\frac{dx}{\cos^2x}=\tan x$, $\int\frac{dx}{1+x^2}=\arctan x$, $\int\frac{dx}{\sqrt{1-x^2}}=\arcsin x$."),
     tasks(2, [r"$\res{x^4-3x^2+2x+C}$", r"$\int\left(x^{3/2}+x^{-1/2}\right)dx=\res{\frac25\sqrt{x^5}+2\sqrt x+C}$", r"$\res{e^x-\frac{3^x}{\ln3}+C}$", r"$\res{2\ln|x|-5\arctan x+C}$",
               r"$\res{3\sin x+2\cos x+C}$", r"$\res{\tan x+C}$", r"$\res{4\arcsin x+C}$", r"$\res{-\frac{1}{2x^2}+C}$"])),
 (2, r"Transforma el integrando (operaciones o identidades trigonométricas) y calcula:" + tasks(2, [r"$\displaystyle\int\cos^2x\,dx$", r"$\displaystyle\int\tan^2x\,dx$", r"$\displaystyle\int(\sin x+\cos x)^2dx$", r"$\displaystyle\int\frac{(x+1)^2}{x}\,dx$", r"$\displaystyle\int\frac{2x-1}{\sqrt[3]{x}}\,dx$"])
     + recorda(r"$\cos^2x=\frac{1+\cos2x}{2}$, $\sin^2x=\frac{1-\cos2x}{2}$, $1+\tan^2x=\frac{1}{\cos^2x}$, $2\sin x\cos x=\sin2x$."),
     tasks(2, [r"$\res{\frac x2+\frac{\sin2x}{4}+C}$", r"$\int\left(\frac{1}{\cos^2x}-1\right)dx=\res{\tan x-x+C}$", r"$\int(1+\sin2x)\,dx=\res{x-\frac{\cos2x}{2}+C}$",
               r"$\int\left(x+2+\frac1x\right)dx=\res{\frac{x^2}2+2x+\ln|x|+C}$", r"$\int\left(2x^{2/3}-x^{-1/3}\right)dx=\res{\frac65\sqrt[3]{x^5}-\frac32\sqrt[3]{x^2}+C}$"])),
)

# =====================================================================
# 3. Integrals quasi immediates
for f_, F_ in [((3 * x - 2)**5, (3 * x - 2)**6 / 18), (x**2 / (x**3 + 1), ln(x**3 + 1) / 3), (sp.exp(-x / 2), -2 * sp.exp(-x / 2)), (cos(3 * x + 1), sin(3 * x + 1) / 3),
               (1 / cos(2 * x)**2, tan(2 * x) / 2), (x * sp.exp(x**2), sp.exp(x**2) / 2), (sin(x) / cos(x)**3, 1 / (2 * cos(x)**2)), (1 / (9 + x**2), atan(x / 3) / 3),
               (x / sq(1 - x**4), sp.asin(x**2) / 2), (cos(x) / sin(x), ln(sin(x))), (ln(x)**2 / x, ln(x)**3 / 3), (x * sin(x**2), -cos(x**2) / 2), (sin(x) / (1 + cos(x)**2), -atan(cos(x))),
               (sp.exp(2) * sp.exp(tan(x)) / (4 * cos(x)**2), sp.exp(2) * sp.exp(tan(x)) / 4), (x * cos(4 * x**2 - 1), sin(4 * x**2 - 1) / 8), (1 / (x**2 + 6 * x + 13), atan((x + 3) / 2) / 2),
               ((2 * x + 3) / (x**2 + 1), ln(x**2 + 1) + 3 * atan(x)), (1 / (sp.exp(x) + sp.exp(-x)), atan(sp.exp(x)))]:
    prim(f_, F_, (0.31, 0.55, 0.77))
ok(sp.solve(sp.integrate(x * sin(x**2), (x, 0, a_)) - 1, a_) is not None); defi(x * sin(x**2), 0, sq(pi), 1)
defi(sin(x) / (1 + cos(x)**2), 0, pi / 2, pi / 4); eq(-atan(cos(pi)) + 1 - pi / 4, 1)
sec("Integrales casi inmediatas",
 (1, r"Calcula:" + tasks(2, [r"$\displaystyle\int(3x-2)^5dx$", r"$\displaystyle\int\frac{x^2}{x^3+1}\,dx$", r"$\displaystyle\int e^{-x/2}\,dx$", r"$\displaystyle\int\cos(3x+1)\,dx$", r"$\displaystyle\int\frac{dx}{\cos^2(2x)}$",
                             r"$\displaystyle\int xe^{x^2}dx$", r"$\displaystyle\int\frac{\sin x}{\cos^3x}\,dx$", r"$\displaystyle\int\frac{dx}{9+x^2}$", r"$\displaystyle\int\frac{x}{\sqrt{1-x^4}}\,dx$", r"$\displaystyle\int\frac{\cos x}{\sin x}\,dx$"])
     + recorda(r"Si aparecen $u$ y $u'$ (o $u'$ multiplicada por una constante): $\int u'u^n=\frac{u^{n+1}}{n+1}$, $\int\frac{u'}u=\ln|u|$, $\int u'e^u=e^u$, $\int u'\cos u=\sin u$, $\int\frac{u'}{1+u^2}=\arctan u$…"),
     tasks(2, [r"$\res{\frac{(3x-2)^6}{18}+C}$", r"$\res{\frac13\ln\left|x^3+1\right|+C}$", r"$\res{-2e^{-x/2}+C}$", r"$\res{\frac13\sin(3x+1)+C}$", r"$\res{\frac12\tan2x+C}$",
               r"$\res{\frac12e^{x^2}+C}$", r"$\int\sin x\cos^{-3}x=\res{\frac{1}{2\cos^2x}+C}$", r"$\res{\frac13\arctan\frac x3+C}$", r"$u=x^2$: $\res{\frac12\arcsin x^2+C}$", r"$\res{\ln|\sin x|+C}$"])),
 (2, r"Calcula las integrales siguientes:" + tasks(1, [r"\pau{Castilla y León, junio 2018} $\displaystyle\int\frac{(\ln x)^2}{x}\,dx$", r"\pau{Navarra, extraordinaria 2026} $\displaystyle\int\frac{e^2\,e^{\tan x}}{4\cos^2x}\,dx$",
                                                     r"\pau{Asturias, ordinaria 2025} $\displaystyle\int x\cos\left(4x^2-1\right)dx$"]),
     tasks(1, [r"$\res{\frac{(\ln x)^3}{3}+C}$", r"$u=\tan x$: $\res{\frac{e^2e^{\tan x}}{4}+C}$", r"$\frac18\int8x\cos\left(4x^2-1\right)dx=\res{\frac18\sin\left(4x^2-1\right)+C}$"])),
 (2, r"\pau{Murcia, extraordinaria 2021}" + tasks(1, [r"Calcula $\displaystyle\int x\sin\left(x^2\right)dx$.", r"Halla el menor valor de $a>0$ para el que $\displaystyle\int_0^ax\sin\left(x^2\right)dx=1$."]),
     tasks(1, [r"$\res{-\frac12\cos\left(x^2\right)+C}$", r"$\frac{1-\cos a^2}{2}=1\Rightarrow\cos a^2=-1\Rightarrow a^2=\pi$: \res{a=\sqrt\pi}"])),
 (2, r"\pau{Murcia, extraordinaria 2023} Sea $f(x)=\dfrac{\sin x}{1+\cos^2x}$." + tasks(1, [r"Calcula la integral indefinida de $f$.", r"Calcula $\displaystyle\int_0^{\pi/2}f(x)\,dx$.", r"Determina la primitiva de $f$ que pasa por el punto $(\pi,1)$."]),
     tasks(1, [r"$u=\cos x$: $\res{-\arctan(\cos x)+C}$", r"$\big[-\arctan(\cos x)\big]_0^{\pi/2}=0+\arctan1=\res{\frac\pi4}$", r"$-\arctan(-1)+C=\frac\pi4+C=1$: \res{F(x)=-\arctan(\cos x)+1-\frac\pi4}"])),
 (3, r"Calcula:" + tasks(1, [r"$\displaystyle\int\frac{dx}{x^2+6x+13}$", r"$\displaystyle\int\frac{2x+3}{x^2+1}\,dx$", r"$\displaystyle\int\frac{dx}{e^x+e^{-x}}$ (multiplica arriba y abajo por $e^x$)"]),
     tasks(1, [r"$(x+3)^2+4$: $\res{\frac12\arctan\frac{x+3}{2}+C}$", r"$\int\frac{2x}{x^2+1}+\int\frac{3}{x^2+1}=\res{\ln\left(x^2+1\right)+3\arctan x+C}$", r"$\int\frac{e^x}{e^{2x}+1}\,dx=\res{\arctan e^x+C}$"])),
)

# =====================================================================
# 4. Canvi de variable
for f_, F_ in [(x / sq(x + 2), R(2, 3) * (x + 2)**R(3, 2) - 4 * sq(x + 2)), (x * sq(1 - x**2), -(1 - x**2)**R(3, 2) / 3), (sp.exp(x) / (1 + 2 * sp.exp(x) + sp.exp(2 * x)), -1 / (1 + sp.exp(x))),
               (x * sp.exp(2 * x**2), sp.exp(2 * x**2) / 4), (1 / (x * ln(x)), ln(ln(x))), (sq(1 - x**2), sp.asin(x) / 2 + x * sq(1 - x**2) / 2), (1 / (sq(x) + sp.root(x, 4)), 2 * sq(x) - 4 * sp.root(x, 4) + 4 * ln(1 + sp.root(x, 4))),
               (sp.exp(x) / (sp.exp(2 * x) + sp.exp(x) - 2), ln((sp.exp(x) - 1) / (sp.exp(x) + 2)) / 3)]:
    prim(f_, F_, (1.31, 1.55, 1.77, 2.6))
prim(sq(1 - x**2), sp.asin(x) / 2 + x * sq(1 - x**2) / 2, (0.2, 0.5, 0.8)); prim(x * sq(1 - x**2), -(1 - x**2)**R(3, 2) / 3, (0.2, 0.5, 0.8)); defi(x * sq(1 - x**2), 0, 1, R(1, 3)); defi(sq(1 - x**2), 0, 1, pi / 4); eq((sp.exp(2 * x**2) / 4).subs(x, 0) - R(5, 4), -1); defi(1 / (sq(1 + x) - 1), 3, 8, 2 + 2 * ln(2))
sec("Integración por cambio de variable",
 (1, r"Calcula con el cambio indicado:" + tasks(1, [r"$\displaystyle\int\frac{x}{\sqrt{x+2}}\,dx$ \quad ($t=\sqrt{x+2}$)", r"$\displaystyle\int\frac{dx}{x\ln x}$ \quad ($t=\ln x$)", r"$\displaystyle\int\frac{dx}{\sqrt x+\sqrt[4]x}$ \quad ($x=t^4$)"])
     + recorda(r"Cambio $t=g(x)$, $dt=g'(x)\,dx$; todo tiene que quedar en $t$. Al final deshacemos el cambio (o, en una integral definida, cambiamos los límites)."),
     tasks(1, [r"$x=t^2-2$, $dx=2t\,dt$: $\int2\left(t^2-2\right)dt=\res{\frac23(x+2)^{3/2}-4\sqrt{x+2}+C}$", r"$\int\frac{dt}{t}=\res{\ln|\ln x|+C}$",
               r"$dx=4t^3dt$: $\int\frac{4t^3}{t^2+t}\,dt=4\int\left(t-1+\frac{1}{t+1}\right)dt=\res{2\sqrt x-4\sqrt[4]x+4\ln\left(1+\sqrt[4]x\right)+C}$"])),
 (2, r"\pau{Asturias, ordinaria 2022} Sea $f(x)=x\sqrt{1-x^2}$." + tasks(1, [r"Calcula una primitiva de $f$ que pase por el punto $(-1,0)$ (cambio $t=1-x^2$).", r"Calcula $\displaystyle\int_0^1f(x)\,dx$."]),
     tasks(1, [r"$dt=-2x\,dx$: $-\frac12\int\sqrt t\,dt=-\frac13t^{3/2}$; $\ F(-1)=C=0$: \res{F(x)=-\frac13\left(1-x^2\right)^{3/2}}", r"$F(1)-F(0)=0+\frac13=\res{\frac13}$"])),
 (2, r"\pau{Andalucía, extraordinaria 2022} Calcula $\displaystyle\int_3^8\frac{dx}{\sqrt{1+x}-1}$ (cambio $t=\sqrt{1+x}-1$).",
     r"$x=(t+1)^2-1$, $dx=2(t+1)\,dt$; límites $1$ y $2$: $\int_1^2\frac{2(t+1)}{t}\,dt=2\big[t+\ln t\big]_1^2=\res{2+2\ln2}$."),
 (2, r"Calcula las integrales siguientes con el cambio $t=e^x$:" + tasks(1, [r"\pau{Navarra, julio 2018} $\displaystyle\int\frac{e^x}{1+2e^x+e^{2x}}\,dx$", r"\pau{Castilla-La Mancha, junio 2018} $\displaystyle\int\frac{e^x}{e^{2x}+e^x-2}\,dx$"]),
     tasks(1, [r"$\int\frac{dt}{(1+t)^2}=\res{-\frac{1}{1+e^x}+C}$", r"$\int\frac{dt}{(t-1)(t+2)}=\frac13\int\left(\frac{1}{t-1}-\frac{1}{t+2}\right)dt=\res{\frac13\ln\left|\frac{e^x-1}{e^x+2}\right|+C}$"])),
 (2, r"\pau{Asturias, extraordinaria 2023} Calcula la primitiva de $f(x)=xe^{2x^2}$ que pasa por el punto $(0,-1)$ (puedes hacer el cambio $t=2x^2$).",
     r"$dt=4x\,dx$: $\frac14\int e^t\,dt=\frac14e^{2x^2}$; $\frac14+C=-1$: \res{F(x)=\frac14e^{2x^2}-\frac54}."),
 (3, r"Calcula $\displaystyle\int\sqrt{1-x^2}\,dx$ con el cambio $x=\sin t$ y deduce el área de un cuarto de círculo de radio 1.",
     r"$\int\cos^2t\,dt=\frac t2+\frac{\sin2t}{4}$: \res{\frac{\arcsin x}{2}+\frac{x\sqrt{1-x^2}}{2}+C}. \ $\int_0^1\sqrt{1-x^2}\,dx=\frac{\pi/2}{2}=\res{\frac\pi4}$, el área del cuarto de círculo."),
)

# =====================================================================
# 5. Per parts
for f_, F_ in [(x * sin(x), -x * cos(x) + sin(x)), (x * sp.exp(-x), -(x + 1) * sp.exp(-x)), (x**3 * ln(x), x**4 * ln(x) / 4 - x**4 / 16), (ln(x + 1), (x + 1) * ln(x + 1) - x),
               ((3 - 2 * x) * sp.exp(-2 * x), (x - 1) * sp.exp(-2 * x)), ((2 * x + 5) * sp.exp(-2 * x), (-x - 3) * sp.exp(-2 * x) + 3), ((x**2 - 3 * x) * sp.exp(x), (x**2 - 5 * x + 5) * sp.exp(x) - 4),
               (x * ln(x**2), x**2 * ln(x) - x**2 / 2), (x**2 * sp.exp(-3 * x), -(x**2 / 3 + 2 * x / 9 + R(2, 27)) * sp.exp(-3 * x)), (ln(x**2 - 1), x * ln(x**2 - 1) - 2 * x - ln(x - 1) + ln(x + 1)),
               (sp.exp(2 * x) * cos(x), sp.exp(2 * x) * (2 * cos(x) + sin(x)) / 5), (x * ln(x)**2, x**2 * ln(x)**2 / 2 - x**2 * ln(x) / 2 + x**2 / 4), (x * atan(x), (x**2 + 1) * atan(x) / 2 - x / 2)]:
    prim(f_, F_, (1.31, 1.55, 1.77, 2.6))
eq(((-x - 3) * sp.exp(-2 * x) + 3).subs(x, 0), 0); eq(((x**2 - 5 * x + 5) * sp.exp(x) - 4).subs(x, 0), 1)
ok(sp.solve((ln(b_)**2 - 1) / 2 - R(3, 2), b_) is not None); defi(ln(x) / x, E, E**2, R(3, 2))
sec("Integración por partes",
 (1, r"Calcula por partes:" + tasks(2, [r"$\displaystyle\int x\sin x\,dx$", r"$\displaystyle\int xe^{-x}\,dx$", r"$\displaystyle\int x^3\ln x\,dx$", r"$\displaystyle\int\ln(x+1)\,dx$"])
     + recorda(r"$\int u\,dv=uv-\int v\,du$. Elige como $u$ la función que se simplifica al derivarla (logaritmos, arctan, polinomios) y como $dv$ la que sabemos integrar (exponenciales, seno, coseno)."),
     tasks(2, [r"$u=x$: $\res{-x\cos x+\sin x+C}$", r"$u=x$: $\res{-(x+1)e^{-x}+C}$", r"$u=\ln x$: $\res{\frac{x^4\ln x}{4}-\frac{x^4}{16}+C}$", r"$u=\ln(x+1)$, $v=x+1$: $\res{(x+1)\ln(x+1)-x+C}$"])),
 (2, r"Calcula:" + tasks(1, [r"\pau{Navarra, ordinaria 2022} $\displaystyle\int(3-2x)e^{-2x}dx$", r"\pau{Castilla y León, extraordinaria 2021} $\displaystyle\int x\ln\left(x^2\right)dx$", r"\pau{País Vasco, julio 2018} $\displaystyle\int x^2e^{-3x}dx$"]),
     tasks(1, [r"$u=3-2x$, $v=-\frac12e^{-2x}$: $\res{(x-1)e^{-2x}+C}$", r"$x\ln x^2=2x\ln x$: $\res{x^2\ln x-\frac{x^2}{2}+C}$", r"Dos veces por partes: $\res{-\left(\frac{x^2}{3}+\frac{2x}{9}+\frac{2}{27}\right)e^{-3x}+C}$"])),
 (2, r"Halla las primitivas que cumplen la condición dada:" + tasks(1, [r"\pau{Extremadura, ordinaria 2024} $f(x)=(2x+5)e^{-2x}$, \ con $F(0)=0$", r"\pau{Extremadura, extraordinaria 2026} $g(x)=\left(x^2-3x\right)e^x$, \ que pase por $P(0,1)$"]),
     tasks(1, [r"$\int(2x+5)e^{-2x}dx=-(x+3)e^{-2x}$: \res{F(x)=-(x+3)e^{-2x}+3}", r"Dos veces por partes: $\left(x^2-5x+5\right)e^x$; $5+C=1$: \res{G(x)=\left(x^2-5x+5\right)e^x-4}"])),
 (3, r"\pau{País Vasco, extraordinaria 2022} Calcula $\displaystyle\int\ln\left(x^2-1\right)dx$.",
     r"$u=\ln(x^2-1)$, $dv=dx$: $x\ln(x^2-1)-\int\frac{2x^2}{x^2-1}\,dx$, y $\frac{2x^2}{x^2-1}=2+\frac{1}{x-1}-\frac{1}{x+1}$: \res{x\ln\left(x^2-1\right)-2x-\ln|x-1|+\ln|x+1|+C}."),
 (3, r"\pau{Galicia, extraordinaria 2023} Calcula $\displaystyle\int\frac{\ln x}{x}\,dx$ por partes y halla algún valor de $B$ tal que $\displaystyle\int_e^B\frac{\ln x}{x}\,dx=\frac32$.",
     r"$u=\ln x$, $dv=\frac{dx}x$: $I=\ln^2x-I\Rightarrow I=\res{\frac{\ln^2x}{2}+C}$. $\frac{\ln^2B-1}{2}=\frac32\Rightarrow\ln B=\pm2$: por ejemplo \res{B=e^2}."),
 (3, r"Calcula $\displaystyle\int e^{2x}\cos x\,dx$ (integral cíclica).",
     r"Dos veces por partes con $u=e^{2x}$: $I=e^{2x}\sin x-2\left(-e^{2x}\cos x+2I\right)\Rightarrow5I=e^{2x}(\sin x+2\cos x)$: \res{I=\frac{e^{2x}(2\cos x+\sin x)}{5}+C}."),
 (2, r"Calcula:" + tasks(1, [r"\pau{Aragón, septiembre 2019} $\displaystyle\int x(\ln x)^2dx$", r"$\displaystyle\int x\arctan x\,dx$"]),
     tasks(1, [r"$u=\ln^2x$ y después $u=\ln x$: $\res{\frac{x^2\ln^2x}{2}-\frac{x^2\ln x}{2}+\frac{x^2}{4}+C}$", r"$u=\arctan x$, $v=\frac{x^2}2$: $\frac{x^2}{2}\arctan x-\frac12\int\frac{x^2}{1+x^2}dx=\res{\frac{x^2+1}{2}\arctan x-\frac x2+C}$"])),
)

# =====================================================================
# 6. Funcions racionals
for f_, F_ in [(1 / (x**2 - 4), ln((x - 2) / (x + 2)) / 4), ((x + 1) / (x**2 - 3 * x + 2), -2 * ln(x - 1) + 3 * ln(x - 2)), (3 * x / (x**2 + x - 2), 2 * ln(x + 2) + ln(x - 1)),
               ((-x**2 + 7 * x + 6) / (x**3 + x**2 - 2 * x), -3 * ln(x) + 4 * ln(x - 1) - 2 * ln(x + 2)), ((x**3 + 2 * x**2 + x - 10) / (x**2 + x - 2), x**2 / 2 + x - 2 * ln(x - 1) + 4 * ln(x + 2)),
               (1 / (x**2 - x - 2), ln((x - 2) / (x + 1)) / 3), ((2 * x - 1) / (x * (x + 1)**2), -ln(x) + ln(x + 1) - 3 / (x + 1)), ((x**4 + 2 * x - 6) / (x**2 + x - 2), x**3 / 3 - x**2 / 2 + 3 * x - ln(x - 1) - 2 * ln(x + 2)),
               ((x + 3) / (x**3 + 4 * x), R(3, 4) * ln(x) - R(3, 8) * ln(x**2 + 4) + atan(x / 2) / 2), ((-2 * x**2 + x + 1) / (2 * x**2 + 5 * x + 2), -x + 3 * ln(x + 2)),
               ((2 * x**2 + 1) / (x * (x - 1)), 2 * x - ln(x) + 3 * ln(x - 1)), ((x**3 + x**2 + 5 * x - 3) / (x**2 + 2 * x + 5), x**2 / 2 - x + ln(x**2 + 2 * x + 5))]:
    prim(f_, F_, (2.31, 2.55, 3.77, 4.6))
eq((2 * x - ln(x) + 3 * ln(x - 1)).subs(x, 2) + ln(2) - 4, 0); L((-2 * x**2 + x + 1) / (2 * x**2 + 5 * x + 2), -R(1, 2), 1)
sec("Integración de funciones racionales",
 (1, r"Calcula (raíces reales simples):" + tasks(2, [r"$\displaystyle\int\frac{dx}{x^2-4}$", r"$\displaystyle\int\frac{x+1}{x^2-3x+2}\,dx$", r"\pau{Extremadura, ordinaria 2021} $\displaystyle\int\frac{3x}{x^2+x-2}\,dx$", r"\pau{Navarra, julio 2017} $\displaystyle\int\frac{dx}{x^2-x-2}$"])
     + recorda(r"Si grado $P\geq$ grado $Q$, primero dividimos. Después factorizamos $Q$: $\frac{A}{x-a}$ para cada raíz simple, $\frac{A}{x-a}+\frac{B}{(x-a)^2}$ para una doble y $\frac{Mx+N}{x^2+px+q}$ para un factor sin raíces."),
     tasks(1, [r"$\frac14\left(\frac{1}{x-2}-\frac{1}{x+2}\right)$: $\res{\frac14\ln\left|\frac{x-2}{x+2}\right|+C}$", r"$\frac{-2}{x-1}+\frac{3}{x-2}$: $\res{-2\ln|x-1|+3\ln|x-2|+C}$",
               r"$\frac{2}{x+2}+\frac{1}{x-1}$: $\res{2\ln|x+2|+\ln|x-1|+C}$", r"$\frac13\left(\frac{1}{x-2}-\frac{1}{x+1}\right)$: $\res{\frac13\ln\left|\frac{x-2}{x+1}\right|+C}$"])),
 (2, r"\pau{Extremadura, extraordinaria 2024} Calcula $\displaystyle\int\frac{-x^2+7x+6}{x^3+x^2-2x}\,dx$.",
     r"$x^3+x^2-2x=x(x-1)(x+2)$: $\frac{-3}{x}+\frac{4}{x-1}-\frac{2}{x+2}$: \res{-3\ln|x|+4\ln|x-1|-2\ln|x+2|+C}."),
 (2, r"Calcula (grado del numerador mayor o igual):" + tasks(1, [r"\pau{Castilla-La Mancha, septiembre 2017} $\displaystyle\int\frac{x^3+2x^2+x-10}{x^2+x-2}\,dx$", r"\pau{Islas Baleares, extraordinaria 2023} $\displaystyle\int\frac{x^4+2x-6}{x^2+x-2}\,dx$"]),
     tasks(1, [r"$x+1+\frac{2x-8}{x^2+x-2}=x+1-\frac{2}{x-1}+\frac{4}{x+2}$: $\res{\frac{x^2}2+x-2\ln|x-1|+4\ln|x+2|+C}$", r"$x^2-x+3+\frac{-3x}{x^2+x-2}$: $\res{\frac{x^3}{3}-\frac{x^2}{2}+3x-\ln|x-1|-2\ln|x+2|+C}$"])),
 (2, r"\pau{País Vasco, junio 2018} Calcula $\displaystyle\int\frac{2x-1}{x(x+1)^2}\,dx$ (raíz doble).",
     r"$\frac{A}{x}+\frac{B}{x+1}+\frac{C}{(x+1)^2}$: $A=-1$, $C=3$, $B=1$: \res{-\ln|x|+\ln|x+1|-\frac{3}{x+1}+C}."),
 (3, r"Calcula $\displaystyle\int\frac{x+3}{x^3+4x}\,dx$ (factor de segundo grado sin raíces).",
     r"$\frac{x+3}{x(x^2+4)}=\frac{3/4}{x}+\frac{-\frac34x+1}{x^2+4}$: \res{\frac34\ln|x|-\frac38\ln\left(x^2+4\right)+\frac12\arctan\frac x2+C}."),
 (2, r"\pau{Comunidad Valenciana, extraordinaria 2023} Sea $f(x)=\dfrac{-2x^2+x+1}{2x^2+5x+2}$." + tasks(1, [r"Comprueba que $x=-\frac12$ es una discontinuidad evitable.", r"Calcula $\displaystyle\int f(x)\,dx$."]),
     tasks(1, [r"$f=\frac{-(2x+1)(x-1)}{(2x+1)(x+2)}$: $\lim_{x\to-1/2}f=\frac{-(x-1)}{x+2}\Big|_{-1/2}=\res{1}$ (finito)", r"$f=-1+\frac{3}{x+2}$: $\res{-x+3\ln|x+2|+C}$"])),
 (2, r"\pau{Comunidad Valenciana, ordinaria 2020} Sea $f(x)=\dfrac{2x^2+1}{x(x-1)}$. Calcula $\displaystyle\int f(x)\,dx$ y la primitiva de $f$ cuya gráfica pasa por el punto $(2,0)$.",
     r"$f=2-\frac1x+\frac{3}{x-1}$: $2x-\ln|x|+3\ln|x-1|+C$; $4-\ln2+C=0$: \res{F(x)=2x-\ln|x|+3\ln|x-1|+\ln2-4}."),
 (3, r"\pau{Comunidad Valenciana, julio 2019} Sea $h(x)=\dfrac{x^3+x^2+5x-3}{x^2+2x+5}$. Calcula la asíntota de la curva $y=h(x)$ y la primitiva $\int h(x)\,dx$.",
     r"$h(x)=x-1+\frac{2x+2}{x^2+2x+5}$: AO \res{y=x-1}. $\int h=\res{\frac{x^2}{2}-x+\ln\left(x^2+2x+5\right)+C}$ (el numerador de la fracción es la derivada del denominador)."),
)

# =====================================================================
# 7. Integral definida i regla de Barrow
defi(x**3 - 2 * x, 0, 1, -R(3, 4)); defi(1 / x + x, 1, E, (E**2 + 1) / 2); defi(cos(x), 0, pi / 2, 1); defi(1 / cos(x)**2, 0, pi / 4, 1); defi(x / (x**2 + 1), 0, 1, ln(2) / 2); defi(sp.exp(2 * x), -1, 1, (E**2 - E**-2) / 2)
defi(x * (ln(x) - 1), 1, 2, 2 * ln(2) - R(9, 4)); defi(x * cos(x), 0, pi / 2, pi / 2 - 1); defi((x + 1) * sp.exp(-x), 0, 1, 2 - 3 / E); defi((x + 10) * sp.exp(2 * x), 0, 5, (29 * E**10 - 19) / 4)
f_ = a_ * x * ln(x) - b_ * x; s_ = sp.solve([sp.diff(f_, x).subs(x, 1), sp.integrate(f_, (x, 1, 2)) - (8 * ln(2) - 9)], [a_, b_], dict=True); ok(s_ == [{a_: 4, b_: 4}])
defi(ln(x) / sq(x), 1, E**2, 4); prim(ln(x) / sq(x), 2 * sq(x) * (ln(x) - 2)); defi(x**2, 0, 3, 9)
sec("La integral definida y la regla de Barrow",
 (1, r"Calcula:" + tasks(2, [r"$\displaystyle\int_0^1\left(x^3-2x\right)dx$", r"$\displaystyle\int_1^e\left(\frac1x+x\right)dx$", r"$\displaystyle\int_0^{\pi/2}\cos x\,dx$", r"$\displaystyle\int_0^{\pi/4}\frac{dx}{\cos^2x}$", r"$\displaystyle\int_0^1\frac{x}{x^2+1}\,dx$", r"$\displaystyle\int_{-1}^1e^{2x}dx$"])
     + recorda(r"Regla de Barrow: $\int_a^bf(x)\,dx=F(b)-F(a)$, con $F$ una primitiva cualquiera de $f$ (continua en $[a,b]$)."),
     tasks(2, [r"$\frac14-1=\res{-\frac34}$", r"$1+\frac{e^2-1}{2}=\res{\frac{e^2+1}{2}}$", r"$\res{1}$", r"$\res{1}$", r"$\res{\frac{\ln2}{2}}$", r"$\res{\frac{e^2-e^{-2}}{2}}$"])),
 (2, r"Calcula:" + tasks(1, [r"\pau{Galicia, ordinaria 2020} $\displaystyle\int_1^2x(\ln x-1)\,dx$", r"\pau{Canarias, extraordinaria 2020} $\displaystyle\int_0^{\pi/2}x\cos x\,dx$", r"\pau{Castilla-La Mancha, julio 2019} $\displaystyle\int_0^1(x+1)e^{-x}dx$", r"\pau{Cantabria, junio 2019} $\displaystyle\int_0^5(x+10)e^{2x}dx$"]),
     tasks(1, [r"$\Big[\frac{x^2\ln x}{2}-\frac{3x^2}{4}\Big]_1^2=\res{2\ln2-\frac94\approx-0{,}86}$", r"$\big[x\sin x+\cos x\big]_0^{\pi/2}=\res{\frac\pi2-1}$", r"$\big[-(x+2)e^{-x}\big]_0^1=\res{2-\frac3e}$", r"$\Big[e^{2x}\left(\frac x2+\frac{19}4\right)\Big]_0^5=\res{\frac{29e^{10}-19}{4}}$"])),
 (3, r"\pau{Andalucía, septiembre 2018} Sea $f(x)=ax\ln x-bx$ ($x>0$). Determina $a$ y $b$ sabiendo que $f$ tiene un extremo relativo en $x=1$ y que $\displaystyle\int_1^2f(x)\,dx=8\ln2-9$.",
     r"$f'(x)=a\ln x+a-b$, $f'(1)=a-b=0$. $\int_1^2x\ln x\,dx=2\ln2-\frac34$ y $\int_1^2x\,dx=\frac32$: $a\left(2\ln2-\frac94\right)=8\ln2-9\Rightarrow$ \res{a=b=4}."),
 (2, r"\pau{Murcia, extraordinaria 2024} Sea $f(x)=\dfrac{\ln x}{\sqrt x}$. Calcula $\displaystyle\int f(x)\,dx$ y el valor de $a>0$ para el que $\displaystyle\int_1^af(x)\,dx=4$.",
     r"Por partes: $\res{2\sqrt x\,(\ln x-2)+C}$. $2\sqrt a(\ln a-2)+4=4\Rightarrow\ln a=2$: \res{a=e^2}."),
 (2, r"Halla el valor medio de $f(x)=x^2$ en $[0,3]$ y el punto $c$ que da el teorema del valor medio del cálculo integral.",
     r"$\frac13\int_0^3x^2dx=\frac93=\res{3}$; $c^2=3\Rightarrow\res{c=\sqrt3}\in[0,3]$."),
)
ok(s_[0][a_] == 4 and s_[0][b_] == 4)

# =====================================================================
# 8. Teorema fonamental del càlcul
F_ = sp.Integral((sp.Symbol('t')**2 - 4) * sp.exp(sp.Symbol('t')), (sp.Symbol('t'), 0, x)); ext(sp.integrate((x**2 - 4) * sp.exp(x), x), -2, 'max'); ext(sp.integrate((x**2 - 4) * sp.exp(x), x), 2, 'min')
L((sp.integrate(sp.exp(x**2), (x, 0, x)) - x) / x**3, 0, R(1, 3))
tt = sp.Symbol('t', positive=True); G_ = x**3 * ln(x**3) - x**3 + 1; eq(sp.diff(G_, x).subs(x, 1.7), (9 * x**2 * ln(x)).subs(x, 1.7)); eq(G_.subs(x, R(13, 10)), sp.Integral(ln(tt), (tt, 1, R(13, 10)**3)).evalf(30))
eq(sp.diff(sp.integrate(sp.exp(-tt), (tt, 0, x**2)), x).subs(x, 1.3), (2 * x * sp.exp(-x**2)).subs(x, 1.3))
ok(sp.expand(sp.diff(x**2 * sp.exp(x), x) - (2 * x + x**2) * sp.exp(x)) == 0)
sec("Teorema fundamental del cálculo",
 (2, r"Calcula la derivada de:" + tasks(2, [r"$F(x)=\displaystyle\int_0^x\frac{dt}{1+t^4}$", r"$G(x)=\displaystyle\int_1^{x^3}\ln t\,dt$ \ ($x>0$)", r"$H(x)=\displaystyle\int_0^{x^2}e^{-t}\,dt$", r"$K(x)=\displaystyle\int_{x}^{1}\cos\left(t^2\right)dt$"])
     + recorda(r"$\dfrac{d}{dx}\displaystyle\int_a^{x}f(t)\,dt=f(x)$ y, con la regla de la cadena, $\dfrac{d}{dx}\displaystyle\int_a^{g(x)}f(t)\,dt=f\big(g(x)\big)\,g'(x)$."),
     tasks(2, [r"$\res{\frac{1}{1+x^4}}$", r"$\ln\left(x^3\right)\cdot3x^2=\res{9x^2\ln x}$", r"$\res{2xe^{-x^2}}$", r"$\res{-\cos\left(x^2\right)}$"])),
 (2, r"Halla los extremos relativos de $F(x)=\displaystyle\int_0^x\left(t^2-4\right)e^{t}\,dt$.",
     r"$F'(x)=\left(x^2-4\right)e^x=0\Leftrightarrow x=\pm2$; $F'$ pasa de $+$ a $-$ en $-2$ y de $-$ a $+$ en $2$: \res{\text{máx. en }x=-2}, \res{\text{mín. en }x=2}."),
 (2, r"\pau{Aragón, extraordinaria 2026} No toda función tiene una primitiva expresable con funciones elementales; por ejemplo $f(x)=\sin\left(x^2\right)$. Sea $F$ la primitiva de $f$ con $F(0)=0$." + tasks(1, [r"¿Cuál es la derivada de $F$?", r"Calcula $\displaystyle\lim_{x\to0}\frac{F(x)}{x^3}$ con la regla de L'Hôpital."]),
     tasks(1, [r"$\res{F'(x)=\sin\left(x^2\right)}$", r"$\overset{\text{L'H}}{=}\lim\frac{\sin x^2}{3x^2}=\res{\frac13}$"])),
 (3, r"Calcula $\displaystyle\lim_{x\to0}\frac{\int_0^xe^{t^2}dt-x}{x^3}$.",
     r"$\left[\frac00\right]\overset{\text{L'H}}{=}\lim\frac{e^{x^2}-1}{3x^2}\overset{\text{L'H}}{=}\lim\frac{2xe^{x^2}}{6x}=\res{\frac13}$."),
 (3, r"Halla una función continua $f$ tal que $\displaystyle\int_0^xf(t)\,dt=x^2e^x$ para todo $x$.",
     r"Derivando los dos miembros: \res{f(x)=\left(2x+x^2\right)e^x}."),
)
L(sp.sin(x**2) / (3 * x**2), 0, R(1, 3))

# =====================================================================
# 9. Àrea entre una corba i l'eix OX
area(-x**2 + 4 * x, 0, [1, 3], R(22, 3)); area((x - 1) * (x + 2), 0, [-3, -2, 1, 2], R(49, 6))
area(sin(pi - 2 * x), 0, [-pi / 4, 0, pi / 4], 1); prim(sin(pi - 2 * x), cos(pi - 2 * x) / 2); eq((cos(pi - 2 * x) / 2).subs(x, pi / 2) + R(1, 2), 1)
area(4 * sin(x - pi), 0, [0, pi], 8); area(x * ln(x), 0, [1, E], (E**2 + 1) / 4); area(x**2 - 6 * x, 0, [0, 6], 36); area(x**3 - x, 0, [-1, 0, 1], R(1, 2))
sec("Área entre una curva y el eje OX",
 (1, r"\pau{Cantabria, extraordinaria 2021} Sea $f(x)=-x^2+4x$. Calcula una primitiva y el área del recinto limitado por $f$, las rectas $x=1$, $x=3$ y el eje OX."
     + recorda(r"Busca los cortes con OX dentro del intervalo, integra en cada trozo y suma los valores absolutos. ¡Haz un esbozo!"),
     r"$F(x)=-\frac{x^3}{3}+2x^2$. En $[1,3]$, $f>0$: $A=F(3)-F(1)=9-\frac53=\res{\frac{22}{3}\text{ u}^2}$."
     + cen(grafA([lambda v: -v * v + 4 * v], (-0.5, 4.5, -1, 4.6), fills=[(lambda v: -v * v + 4 * v, Z, 1, 3)], pts=[(0, 0), (4, 0)]))),
 (2, r"\pau{Castilla-La Mancha, septiembre 2017} Calcula el área de la región determinada por $f(x)=(x-1)(x+2)$, las rectas $x=-3$, $x=2$ y el eje de abscisas. Esbózala.",
     r"Cortes $-2$ y $1$. $\int_{-3}^{-2}f=\frac{11}{6}$, $\left|\int_{-2}^1f\right|=\frac92$, $\int_1^2f=\frac{11}6$: \res{A=\frac{49}{6}\text{ u}^2}."
     + cen(grafA([lambda v: (v - 1) * (v + 2)], (-3.5, 2.5, -3, 4.5), fills=[(lambda v: (v - 1) * (v + 2), Z, -3, -2, 'green!25'), (lambda v: (v - 1) * (v + 2), Z, -2, 1, 'red!20'), (lambda v: (v - 1) * (v + 2), Z, 1, 2, 'green!25')], pts=[(-2, 0), (1, 0)]))),
 (2, r"\pau{Asturias, extraordinaria 2024} Sea $f(x)=\sin(\pi-2x)$." + tasks(1, [r"Calcula una primitiva que pase por el punto $\left(\frac\pi2,1\right)$.", r"Calcula el área limitada por $f$, el eje $X$ y las rectas $x=-\frac\pi4$ y $x=\frac\pi4$."]),
     tasks(1, [r"$\int\sin(\pi-2x)\,dx=\frac{\cos(\pi-2x)}{2}$; $\frac12+C=1$: \res{F(x)=\frac{\cos(\pi-2x)}{2}+\frac12}", r"$f=\sin2x$ cambia de signo en 0: $\frac12+\frac12=\res{1\text{ u}^2}$"])),
 (2, r"\pau{Asturias, ordinaria 2025} Calcula el área acotada entre $f(x)=4\sin(x-\pi)$ y las rectas $y=0$, $x=0$ y $x=\pi$.",
     r"$4\sin(x-\pi)=-4\sin x\leq0$ en $[0,\pi]$: $A=\int_0^\pi4\sin x\,dx=\res{8\text{ u}^2}$."),
 (2, r"Calcula el área entre $f(x)=x\ln x$, el eje OX y la recta $x=e$.",
     r"Corta OX en $x=1$ y $f\geq0$ en $[1,e]$: $\Big[\frac{x^2\ln x}{2}-\frac{x^2}{4}\Big]_1^e=\res{\frac{e^2+1}{4}\text{ u}^2}$."
     + cen(grafA([(lambda v: v * mlog(v), 0.001, 3.3)], (-0.3, 3.2, -0.6, 3.5), fills=[(lambda v: v * mlog(v), Z, 1, math.e)], pts=[(1, 0)], va=[]))),
 (3, r"Halla $b>0$ para que el área del recinto limitado por $y=x^2-bx$ y el eje OX valga 36.",
     r"Cortes $0$ y $b$: $A=\left|\int_0^b\left(x^2-bx\right)dx\right|=\frac{b^3}{6}=36\Rightarrow\res{b=6}$."),
 (2, r"Calcula el área del recinto limitado por $f(x)=x^3-x$ y el eje OX. ¿Por qué $\int_{-1}^1f(x)\,dx=0$?",
     r"Cortes $-1$, $0$, $1$; cada trozo vale $\frac14$ en valor absoluto: \res{A=\frac12\text{ u}^2}. La integral es 0 porque $f$ es impar y los trozos se compensan."),
)

# =====================================================================
# 10. Àrea entre dues corbes
area(x**2 - 2 * x + 1, -x**2 + 5, [-1, 2], 9); area(6 * x - x**2, x**2 - 2 * x, [0, 4], R(64, 3)); area(sq(3 * x), x**2 / 3, [0, 3], 3); area(x**2 / 4, 2 * sq(x), [0, 4], R(16, 3))
area(-x**2, x**3, [-1, 0], R(1, 12)); area(2 * x * sp.exp(-x), x**2 * sp.exp(-x), [0, 2], 4 / E**2); area(3 * x - x**2, x - 3, [-1, 3], R(32, 3)); area(4 / x, x, [2, 4], 6 - 4 * ln(2))
area(x**2 - 4 * x + 1, -x + 1, [0, 3], R(9, 2))
sec("Área entre dos curvas",
 (1, r"\pau{País Vasco, ordinaria 2020} Dibuja la región cerrada por $f(x)=x^2-2x+1$ y $g(x)=-x^2+5$, y calcula su área."
     + recorda(r"Cortes: $f(x)=g(x)$. Área $=\int_a^b|f-g|\,dx$: en cada trozo, «la de arriba menos la de abajo»."),
     r"$2x^2-2x-4=0\Rightarrow x=-1,\ x=2$. $A=\int_{-1}^2\left(-2x^2+2x+4\right)dx=\res{9\text{ u}^2}$."
     + cen(grafA([lambda v: v * v - 2 * v + 1, lambda v: -v * v + 5], (-2, 3, -1.5, 6), fills=[(lambda v: -v * v + 5, lambda v: v * v - 2 * v + 1, -1, 2)], pts=[(-1, 4), (2, 1)]))),
 (2, r"\pau{Andalucía, junio 2018} Esboza el recinto limitado por $f(x)=6x-x^2$ y $g(x)=x^2-2x$, halla sus puntos de corte y calcula su área.",
     r"$2x^2-8x=0\Rightarrow(0,0),\ (4,8)$. $A=\int_0^4\left(8x-2x^2\right)dx=\res{\frac{64}{3}\text{ u}^2}$."
     + cen(grafA([lambda v: 6 * v - v * v, lambda v: v * v - 2 * v], (-1, 5.5, -2, 10), fills=[(lambda v: 6 * v - v * v, lambda v: v * v - 2 * v, 0, 4)], pts=[(0, 0), (4, 8)]))),
 (2, r"Calcula el área del recinto limitado por las dos curvas:" + tasks(1, [r"\pau{Castilla y León, ordinaria 2022} $y=\sqrt{3x}$ \ y \ $y=\frac13x^2$", r"\pau{Asturias, junio 2017} $f(x)=\frac{x^2}{4}$ \ y \ $g(x)=2\sqrt x$", r"\pau{Castilla y León, extraordinaria 2023} $f(x)=-x^2$ \ y \ $g(x)=x^3$, en $[-1,0]$"]),
     tasks(1, [r"Cortes $0$ y $3$: $\int_0^3\left(\sqrt{3x}-\frac{x^2}3\right)dx=6-3=\res{3\text{ u}^2}$", r"Cortes $0$ y $4$: $\int_0^4\left(2\sqrt x-\frac{x^2}{4}\right)dx=\frac{32}3-\frac{16}3=\res{\frac{16}{3}\text{ u}^2}$", r"$g\geq f$ en $[-1,0]$: $\int_{-1}^0\left(x^3+x^2\right)dx=\res{\frac{1}{12}\text{ u}^2}$"])),
 (2, r"\pau{Castilla-La Mancha, junio 2018} Calcula el área del recinto cerrado por $f(x)=2xe^{-x}$ y $g(x)=x^2e^{-x}$.",
     r"$xe^{-x}(2-x)=0\Rightarrow x=0,\ x=2$. Como $\left(x^2e^{-x}\right)'=(2x-x^2)e^{-x}$: $A=\big[x^2e^{-x}\big]_0^2=\res{\frac{4}{e^2}\text{ u}^2}$."
     + cen(grafA([lambda v: 2 * v * me(-v), lambda v: v * v * me(-v)], (-0.5, 4.5, -0.2, 0.9), fills=[(lambda v: 2 * v * me(-v), lambda v: v * v * me(-v), 0, 2)], pts=[(0, 0), (2, 4 / math.e**2)]))),
 (2, r"\pau{Canarias, extraordinaria 2022} Representa el recinto que encierran $y=3x-x^2$ y $y=x-3$ y calcula su área.",
     r"$x^2-2x-3=0\Rightarrow x=-1,\ x=3$. $A=\int_{-1}^3\left(-x^2+2x+3\right)dx=\res{\frac{32}{3}\text{ u}^2}$."),
 (2, r"\pau{Extremadura, ordinaria 2020} Representa la región delimitada por $f(x)=x^2-4x+1$ y $g(x)=-x+1$ y calcula su área.",
     r"Cortes $x=0$ y $x=3$: $A=\int_0^3\left(3x-x^2\right)dx=\res{\frac92\text{ u}^2}$."),
 (3, r"Calcula el área del recinto del primer cuadrante limitado por $y=\frac4x$, $y=x$ y la recta $x=4$.",
     r"$\frac4x=x\Rightarrow x=2$. Entre 2 y 4 la recta va por encima: $A=\int_2^4\left(x-\frac4x\right)dx=\res{6-4\ln2\approx3{,}23\text{ u}^2}$."
     + cen(grafA([(lambda v: 4 / v, 0.3, 5), lambda v: v], (-0.3, 4.6, -0.3, 5), fills=[(lambda v: v, lambda v: 4 / v, 2, 4)], pts=[(2, 2)]))),
)

# =====================================================================
print(NCHK[0], 'comprobaciones correctas')
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={integrals, primitives, integrals immediates, canvi de variable, integració per parts, funcions racionals, integral definida, regla de Barrow, teorema fonamental del càlcul, àrees, PAU}"
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

TIT = "Integrales"
def build(sol):
    tt = 'Soluciones de la ficha' if sol else "Ficha de ejercicios"
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    p = preambul(pre, pdftitle='%s de la unidad 9: %s' % (tt, TIT), capcalera='%s · Unidad 9: %s' % (tt, TIT),
                 pdfkeywords='integrales, primitivas, integrales inmediatas, cambio de variable, integración por partes, funciones racionales, integral definida, regla de Barrow, teorema fundamental del cálculo, áreas, PAU', curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 9' if sol else "Ficha de ejercicios · Unidad 9") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.2cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Siempre puedes comprobar una primitiva derivándola. En las gráficas, los recintos de las áreas están sombreados. Puedes comprobar las áreas con la calculadora de los apuntes interactivos."
             if sol else r"Resuelve los ejercicios en el cuaderno justificando cada paso. Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de la Comunidad Valenciana y de otras comunidades autónomas, traducidos al castellano. Puedes comprobar los resultados con las herramientas de los apuntes interactivos (comprobación de primitivas, por partes paso a paso, fracciones simples, calculadora de áreas\dots).") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus primitivas derivándolas y las áreas con las herramientas de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't9-fitxa-solucions-es.tex' if sol else 't9-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'ejercicios,', npau, 'de la PAU de', len(regs), 'comunidades:', ', '.join(regs))
