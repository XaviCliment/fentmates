# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 7: Aplicacions de la
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
sec("Rectes tangent i normal",
 (1, r"Calcula:" + tasks(1, [r"\pau{Castella-la Manxa, juny 2017} La recta normal a la gràfica de $g(x)=x^2-2x-4$ en el punt d'abscissa $x=-3$.",
                              r"\pau{Aragó, ordinària 2020} La recta tangent a $f(x)=\ln(2x+1)$ en $x=\frac12$.",
                              r"\pau{Catalunya, extraordinària 2024} La recta tangent a $y=e^{-2x}$ en $x=0$ i el punt on talla l'eix d'abscisses.",
                              r"\pau{Aragó, extraordinària 2021} La recta tangent a $f(x)=\dfrac{e^x}{x^3-x}$ en $x=2$."])
     + recorda(r"Tangent: $y-f(a)=f'(a)(x-a)$. Normal: $y-f(a)=-\dfrac{1}{f'(a)}(x-a)$."),
     tasks(1, [r"$g(-3)=11$, $g'(-3)=-8\Rightarrow m_n=\frac18$: $y-11=\frac18(x+3)\Rightarrow\res{x-8y+91=0}$",
               r"$f\left(\frac12\right)=\ln2$, $f'(x)=\frac{2}{2x+1}=1$: $\res{y=x-\frac12+\ln2}$",
               r"$y'(0)=-2$: $\res{y=-2x+1}$, que talla l'eix en $\res{\left(\frac12,0\right)}$",
               r"$f(2)=\frac{e^2}{6}$, $f'(x)=\frac{e^x(x^3-3x^2-x+1)}{(x^3-x)^2}\Rightarrow f'(2)=-\frac{5e^2}{36}$: $\res{y=-\frac{5e^2}{36}x+\frac{4e^2}{9}}$"])),
 (2, r"\pau{Catalunya, setembre 2019} Considera la funció $f(x)=\dfrac{1}{1+x^2}$." + tasks(1, [r"Calcula l'equació de la recta tangent a la gràfica en els punts en què és horitzontal.", r"Calcula les coordenades del punt de la gràfica en què el pendent de la recta tangent és màxim."])
     + recorda(r"El pendent de la tangent és $m(x)=f'(x)$: per a fer-lo màxim, derivem $f'$ i igualem a zero (és a dir, $f''(x)=0$)."),
     tasks(1, [r"$f'(x)=\frac{-2x}{(1+x^2)^2}=0\Leftrightarrow x=0$: $\res{y=1}$",
               r"$f''(x)=\frac{6x^2-2}{(1+x^2)^3}=0\Leftrightarrow x=\pm\frac{1}{\sqrt3}$; $f'$ és màxim en $x=-\frac{1}{\sqrt3}$ $\left(f'=\frac{9}{8\sqrt3}>0\right)$: $\res{\left(-\frac{1}{\sqrt3},\frac34\right)}$"])),
 (2, r"\pau{Astúries, juny 2019} Donada la corba $y=\dfrac{1}{3+x^2}$, escriu la funció $m(x)$ que dona el pendent de la recta tangent en cada punt i troba en quin $x$ el pendent és màxim.",
     r"$m(x)=\dfrac{-2x}{(3+x^2)^2}$, \ $m'(x)=\dfrac{6x^2-6}{(3+x^2)^3}=0\Leftrightarrow x=\pm1$; \ $m'$ passa de $+$ a $-$ en $x=-1$: \ pendent màxim en $\res{x=-1}$ \ $\left(m(-1)=\frac18\right)$."),
 (2, r"\pau{La Rioja, ordinària 2022} Donada la corba $f(x)=\frac14x^2+4x+4$, troba els punts en què la recta tangent passa per l'origen i escriu-ne les equacions."
     + recorda(r"Si el punt no és de la corba, escriu la tangent en un punt genèric $(a,f(a))$ i imposa que passe pel punt donat."),
     r"$0-f(a)=f'(a)(0-a)\Rightarrow-\frac{a^2}{4}-4a-4=-\frac{a^2}{2}-4a\Rightarrow a^2=16$: \ $\res{A(-4,-8)}$, tangent $\res{y=2x}$; \ $\res{B(4,24)}$, tangent $\res{y=6x}$."),
 (2, r"Quantes rectes tangents a $f(x)=x^3-3x$ passen pel punt $(0,2)$? Escriu-les.",
     r"$2-(a^3-3a)=(3a^2-3)(0-a)\Rightarrow 2=-2a^3\Rightarrow a=-1$: només \rest{una}, la tangent en $(-1,2)$, que és \res{y=2} (horitzontal)."),
 (2, r"Troba $a$ perquè la recta $y=2x+a$ siga tangent a la paràbola $f(x)=x^2-4x+10$. En quin punt?"
     + recorda(r"Una recta és tangent a una paràbola si, en tallar-les, l'equació de segon grau té una arrel doble (discriminant zero)."),
     r"$x^2-4x+10=2x+a\Leftrightarrow x^2-6x+10-a=0$; \ $\Delta=36-4(10-a)=0\Rightarrow\res{a=1}$, en $\res{(3,7)}$ (també: $f'(x)=2x-4=2\Rightarrow x=3$)."),
 (2, r"\pau{Galícia, extraordinària 2022} Troba els vèrtexs del triangle rectangle que té la hipotenusa sobre la recta tangent a $f(x)=x^2$ en $x=2$ i un catet de longitud 2 sobre l'eix $X$ (a la dreta del punt on la tangent talla l'eix).",
     r"Tangent: $y=4x-4$, talla l'eix en $(1,0)$. Vèrtexs: $\res{A(1,0),\ B(3,0),\ C(3,8)}$."),
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
 (1, r"Calcula els límits següents:" + tasks(2, [r"\pau{Castella-la Manxa, extraordinària 2021} $\displaystyle\lim_{x\to1}\frac{x-1}{e^{x-1}-1}$", r"\pau{Castella-la Manxa, ordinària 2021} $\displaystyle\lim_{x\to2}\frac{e^{x-2}-1}{2x-4}$",
                                                 r"\pau{Galícia, ordinària 2022} $\displaystyle\lim_{x\to0}\frac{x\cos x}{\sin x}$", r"\pau{Múrcia, setembre 2018} $\displaystyle\lim_{x\to0}\frac{\ln(\cos x+\sin x)}{x}$",
                                                 r"\pau{Cantàbria, setembre 2018} $\displaystyle\lim_{x\to0}\frac{\sin(2x^2)+x}{\ln(x+1)+x}$", r"\pau{Castella i Lleó, ordinària 2022} $\displaystyle\lim_{x\to0}\frac{x\sin x}{2-2\cos x}$"])
     + recorda(r"Si $\lim\frac fg$ és $\left[\frac00\right]$ o $\left[\frac\infty\infty\right]$, aleshores $\lim\frac{f}{g}=\lim\frac{f'}{g'}$. Derivem el numerador i el denominador \textbf{per separat}."),
     tasks(2, [r"$\overset{\text{L'H}}{=}\lim\frac{1}{e^{x-1}}=\res{1}$", r"$\overset{\text{L'H}}{=}\lim\frac{e^{x-2}}{2}=\res{\frac12}$", r"$\overset{\text{L'H}}{=}\lim\frac{\cos x-x\sin x}{\cos x}=\res{1}$",
               r"$\overset{\text{L'H}}{=}\lim\frac{\cos x-\sin x}{\cos x+\sin x}=\res{1}$", r"$\overset{\text{L'H}}{=}\lim\frac{4x\cos(2x^2)+1}{\frac{1}{x+1}+1}=\res{\frac12}$", r"$\overset{\text{L'H}}{=}\lim\frac{\sin x+x\cos x}{2\sin x}\overset{\text{L'H}}{=}\lim\frac{2\cos x-x\sin x}{2\cos x}=\res{1}$"])),
 (2, r"Calcula aquests límits del tipus $\left[\frac\infty\infty\right]$:" + tasks(2, [r"$\displaystyle\lim_{x\to+\infty}\frac{x^3}{e^{2x}}$", r"$\displaystyle\lim_{x\to+\infty}\frac{(\ln x)^2}{x}$", r"$\displaystyle\lim_{x\to0^+}\frac{\ln(\sin x)}{\ln x}$", r"\pau{Castella-la Manxa, ordinària 2024} $\displaystyle\lim_{x\to+\infty}\frac{e^x-1}{x^2+3}$"]),
     tasks(2, [r"$\frac{3x^2}{2e^{2x}}\to\frac{6x}{4e^{2x}}\to\frac{6}{8e^{2x}}\to\res{0}$", r"$\frac{2\ln x\cdot\frac1x}{1}=\frac{2\ln x}{x}\to\frac{2/x}{1}\to\res{0}$", r"$\frac{\cos x/\sin x}{1/x}=\frac{x\cos x}{\sin x}\to\res{1}$", r"$\frac{e^x}{2x}\to\frac{e^x}{2}\to\res{+\infty}$"])),
 (2, r"\pau{Aragó, ordinària 2025} Calcula $\displaystyle\lim_{x\to0}\frac{x^2-\sin(x^2)}{1-\cos x}$.",
     r"$\left[\frac00\right]\overset{\text{L'H}}{=}\lim\frac{2x-2x\cos(x^2)}{\sin x}=\lim\frac{2x\left(1-\cos x^2\right)}{\sin x}$; com que $\frac{x}{\sin x}\to1$ i $1-\cos x^2\to0$, el límit és $\res{0}$."),
 (2, r"Límits amb paràmetres:" + tasks(1, [r"\pau{Aragó, extraordinària 2023} Calcula $a$ perquè $\displaystyle L=\lim_{x\to0}\frac{\ln(x+1)-a\sin x+3x\cos(2x)}{x^2}$ siga finit, i calcula $L$.",
                                          r"\pau{Castella i Lleó, extraordinària 2021} Calcula $m>0$ perquè $\displaystyle\lim_{x\to0}\frac{1-\cos(mx)}{x^2}=2$.",
                                          r"\pau{Galícia, ordinària 2023} Si $f(x)=ae^x+b$, troba $a$ i $b$ perquè $f(0)=0$ i $\displaystyle\lim_{x\to0}\frac{f(x)}{x}=3$."])
     + recorda(r"Si el denominador tendeix a 0 i el límit ha de ser finit, el numerador també ha de tendir a 0: això dona una equació."),
     tasks(1, [r"$\overset{\text{L'H}}{=}\lim\frac{\frac{1}{x+1}-a\cos x+3\cos2x-6x\sin2x}{2x}=\frac{4-a}{0}$: cal $\res{a=4}$; aleshores $\overset{\text{L'H}}{=}\lim\frac{-\frac{1}{(x+1)^2}+4\sin x-12\sin2x-12x\cos2x}{2}=\res{-\frac12}$",
               r"$\overset{\text{L'H}}{=}\lim\frac{m\sin mx}{2x}\overset{\text{L'H}}{=}\frac{m^2}{2}=2\Rightarrow\res{m=2}$",
               r"$a+b=0$; \ $\lim\frac{ae^x+b}{x}\overset{\text{L'H}}{=}a=3$: \ $\res{a=3,\ b=-3}$"])),
 (3, r"\pau{Aragó, extraordinària 2022} Calcula $a,b\in\mathbb R$ perquè existisca $\displaystyle\lim_{x\to1}\frac{2x^3+ax^2+bx+3}{-x^3+4x^2-5x+2}=L$ (finit) i calcula el límit.",
     r"El denominador és $-(x-1)^2(x-2)$ (arrel doble en 1). El numerador també ha de tindre l'arrel doble $x=1$: $N(1)=5+a+b=0$, $N'(1)=6+2a+b=0\Rightarrow\res{a=-1,\ b=-4}$. Aleshores $N=(x-1)^2(2x+3)$ i $L=\frac{2+3}{-(1-2)}=\res{5}$."),
 (2, r"On és l'error? \ $\displaystyle\lim_{x\to1}\frac{x^2+1}{x+1}\overset{\text{L'H}}{=}\lim_{x\to1}\frac{2x}{1}=2$. \ I en aquest altre: \ $\displaystyle\lim_{x\to+\infty}\frac{x+\sin x}{x}\overset{\text{L'H}}{=}\lim_{x\to+\infty}(1+\cos x)$, que no existeix, ``per tant el límit no existeix''.",
     r"En el primer no hi ha indeterminació: $\frac{2}{2}=\res{1}$. En el segon, L'Hôpital no conclou res si $\lim\frac{f'}{g'}$ no existeix: $\frac{x+\sin x}{x}=1+\frac{\sin x}{x}\to\res{1}$."),
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
sec("Altres indeterminacions",
 (1, r"Calcula (tipus $0\cdot\infty$ i $\infty-\infty$):" + tasks(2, [r"$\displaystyle\lim_{x\to0^+}x^2\ln x$", r"\pau{Múrcia, ordinària 2021} $\displaystyle\lim_{x\to+\infty}\left(\sqrt{x^2+1}-x\right)$",
                                                                      r"$\displaystyle\lim_{x\to0}\left(\frac{1}{\sin x}-\frac1x\right)$", r"\pau{Aragó, ordinària 2022} $\displaystyle\lim_{x\to+\infty}\left[\sqrt{3x^2-2}-\left(\sqrt3x+5\right)\right]$",
                                                                      r"\pau{La Rioja, ordinària 2023} $\displaystyle\lim_{x\to\infty}\left(\frac{x^2-1}{x+2}-\frac{x^2+1}{x-2}\right)$"])
     + recorda(r"$0\cdot\infty$: escriu $f\cdot g=\frac{f}{1/g}$. \ $\infty-\infty$: fes denominador comú o multiplica pel conjugat."),
     tasks(2, [r"$\frac{\ln x}{1/x^2}\overset{\text{L'H}}{=}\frac{1/x}{-2/x^3}=-\frac{x^2}{2}\to\res{0}$", r"$\frac{1}{\sqrt{x^2+1}+x}\to\res{0}$", r"$\frac{x-\sin x}{x\sin x}\overset{\text{L'H}}{=}\frac{1-\cos x}{\sin x+x\cos x}\overset{\text{L'H}}{=}\frac{\sin x}{2\cos x-x\sin x}\to\res{0}$",
               r"$\frac{3x^2-2-(\sqrt3x+5)^2}{\sqrt{3x^2-2}+\sqrt3x+5}=\frac{-10\sqrt3x-27}{\sqrt{3x^2-2}+\sqrt3x+5}\to\frac{-10\sqrt3}{2\sqrt3}=\res{-5}$", r"$\frac{-4x^2-2x}{x^2-4}\to\res{-4}$"])),
 (2, r"Calcula aquests límits del tipus $1^\infty$:" + tasks(2, [r"\pau{Castella-la Manxa, ordinària 2022} $\displaystyle\lim_{x\to+\infty}\left(\frac{x+1}{x}\right)^{\frac{x^2+1}{x}}$", r"\pau{Castella-la Manxa, ordinària 2026} $\displaystyle\lim_{x\to\infty}\left(\frac{2x+1}{2x-3}\right)^{x}$",
                                                              r"\pau{Aragó, setembre 2018} $\displaystyle\lim_{x\to+\infty}\left(\frac{x^2+1}{x}-\frac{x^3-x^2-x+2}{x^2}\right)^{\frac{3+x^2}{x}}$", r"$\displaystyle\lim_{x\to0}\left(\cos x\right)^{1/x^2}$"])
     + recorda(r"$1^\infty$: $\displaystyle\lim f^g=e^{\lim g\,(f-1)}$, o bé prenent logaritmes: $\ln L=\lim g\ln f$."),
     tasks(2, [r"$\frac{x^2+1}{x}\cdot\frac1x\to1\Rightarrow\res{e}$", r"$x\cdot\frac{4}{2x-3}\to2\Rightarrow\res{e^2}$", r"$f-1=\frac{2x-2}{x^2}$, $\ \frac{3+x^2}{x}\cdot\frac{2x-2}{x^2}\to2\Rightarrow\res{e^2}$", r"$\frac{\cos x-1}{x^2}\to-\frac12\Rightarrow\res{e^{-1/2}=\frac{1}{\sqrt e}}$"])),
 (2, r"Calcula (tipus $1^\infty$, $\infty^0$ i $0^0$):" + tasks(2, [r"$\displaystyle\lim_{x\to\frac\pi2^-}\left(\sin x\right)^{\tan x}$", r"$\displaystyle\lim_{x\to0^+}\left(\frac1x\right)^{\sin x}$", r"$\displaystyle\lim_{x\to0^+}\left(\sin x\right)^{x}$", r"$\displaystyle\lim_{x\to+\infty}\left(x^2+1\right)^{\frac{1}{\ln x}}$"])
     + recorda(r"Prenem logaritmes: $\ln L=\lim g\cdot\ln f$ (que és $0\cdot\infty$) i al final $L=e^{\ln L}$."),
     tasks(2, [r"$\ln L=\lim\frac{\ln\sin x}{\cot x}\overset{\text{L'H}}{=}\lim\frac{\cot x}{-1/\sin^2x}=\lim(-\sin x\cos x)=0\Rightarrow\res{1}$", r"$\ln L=\lim\frac{-\ln x}{1/\sin x}\overset{\text{L'H}}{=}\lim\frac{\sin^2x}{x\cos x}=0\Rightarrow\res{1}$",
               r"$\ln L=\lim x\ln\sin x=\lim\frac{\ln\sin x}{1/x}\overset{\text{L'H}}{=}\lim\frac{-x^2\cos x}{\sin x}=0\Rightarrow\res{1}$", r"$\ln L=\lim\frac{\ln(x^2+1)}{\ln x}\overset{\text{L'H}}{=}\lim\frac{2x^2}{x^2+1}=2\Rightarrow\res{e^2}$"])),
 (2, r"\pau{Aragó, ordinària 2020} Calcula $\displaystyle\lim_{x\to0^+}\left(1+x-\sin x\right)^{1/x^3}$ \ i \ \pau{Madrid, ordinària 2024} $\displaystyle\lim_{x\to\frac\pi2}\left(\tan\frac x2\right)^{\frac{1}{\cos x}}$.",
     r"$\ln L=\lim\frac{\ln(1+x-\sin x)}{x^3}\overset{\text{L'H}}{=}\lim\frac{1-\cos x}{3x^2(1+x-\sin x)}=\frac16\Rightarrow\res{\sqrt[6]{e}}$. \quad $\lim\frac{\tan\frac x2-1}{\cos x}\overset{\text{L'H}}{=}\frac{\frac12\cdot2}{-1}=-1\Rightarrow\res{\frac1e}$."),
 (3, r"\pau{Castella-la Manxa, setembre 2017} Calcula $k$ perquè sigui contínua en $x=0$ la funció " + '$' + pw((r'\left(\dfrac{x+1}{2x+1}\right)^{1/x}', 'x<0'), (r'6x+k', r'x\geq0')) + '$.',
     r"$\displaystyle\lim_{x\to0^-}\left(\frac{x+1}{2x+1}\right)^{1/x}=e^{\lim\frac1x\cdot\frac{-x}{2x+1}}=e^{-1}$, \ $f(0)=k$: \ $\res{k=\frac1e}$."),
 (2, r"Troba $a$ perquè $\displaystyle\lim_{x\to0}\left(1+ax\right)^{\frac{1}{\sin x}}=e^3$.",
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
sec("Monotonia i extrems relatius",
 (1, r"Estudia la monotonia i calcula els extrems relatius de les funcions següents:" + tasks(2, [r"\pau{València, juny 2017} " + fx(r'\dfrac{x^2+1}{x}'), r"\pau{València, juny 2018} " + fx(r'\dfrac{1}{x^2-x}'),
                                                                                              r"\pau{Múrcia, ordinària 2022} " + fx(r'x\ln x'), r"\pau{Castella i Lleó, extraordinària 2020} " + fx(r'\dfrac{\ln x}{x}'),
                                                                                              r"\pau{Andalusia, setembre 2017} " + fx(r'\dfrac{e^x+e^{-x}}{2}'), r"\pau{Aragó, extraordinària 2020} " + fx(r'-\dfrac{x^2}{2}+2\ln(x+1)')])
     + recorda(r"Domini $\to$ $f'$ $\to$ zeros de $f'$ i punts fora del domini $\to$ taula de signes de $f'$. Els extrems es donen com a punts $(a,f(a))$."),
     tasks(1, [r"$f'=1-\frac1{x^2}$: creix en $(-\infty,-1)\cup(1,+\infty)$, decreix en $(-1,0)\cup(0,1)$; \res{\text{màx. }(-1,-2)}, \res{\text{mín. }(1,2)}",
               r"$f'=\frac{-(2x-1)}{(x^2-x)^2}$: creix en $(-\infty,0)\cup\left(0,\frac12\right)$, decreix en $\left(\frac12,1\right)\cup(1,+\infty)$; \res{\text{màx. }\left(\frac12,-4\right)}",
               r"$f'=\ln x+1$: decreix en $\left(0,\frac1e\right)$, creix en $\left(\frac1e,+\infty\right)$; \res{\text{mín. }\left(\frac1e,-\frac1e\right)}",
               r"$f'=\frac{1-\ln x}{x^2}$: creix en $(0,e)$, decreix en $(e,+\infty)$; \res{\text{màx. }\left(e,\frac1e\right)}",
               r"$f'=\frac{e^x-e^{-x}}{2}$: decreix en $(-\infty,0)$, creix en $(0,+\infty)$; \res{\text{mín. }(0,1)}",
               r"Domini $(-1,+\infty)$, $f'=-x+\frac{2}{x+1}=\frac{-(x+2)(x-1)}{x+1}$: creix en $(-1,1)$, decreix en $(1,+\infty)$; \res{\text{màx. }\left(1,-\frac12+2\ln2\right)}"])),
 (2, r"Estudia la monotonia i els extrems relatius de:" + tasks(1, [r"\pau{València, ordinària 2021} " + fx(r'\dfrac{x-1}{x(x+2)}'), r"\pau{Extremadura, extraordinària 2024} " + fx(r'\dfrac{4x+4}{x^2}'),
                                                                   r"\pau{País Basc, extraordinària 2025} " + fx(r'\dfrac{x}{x^2-3x-4}'), r"\pau{Aragó, setembre 2018} " + fx(r'\dfrac{x^2-3x+3}{x-1}')]),
     tasks(1, [r"$f'=\frac{-x^2+2x+2}{x^2(x+2)^2}$: decreix en $(-\infty,-2)\cup\left(-2,1-\sqrt3\right)\cup\left(1+\sqrt3,+\infty\right)$, creix en $\left(1-\sqrt3,0\right)\cup\left(0,1+\sqrt3\right)$; \res{\text{mín. en }x=1-\sqrt3}, \res{\text{màx. en }x=1+\sqrt3}",
               r"$f'=\frac{-4(x+2)}{x^3}$: decreix en $(-\infty,-2)\cup(0,+\infty)$, creix en $(-2,0)$; \res{\text{mín. }(-2,-1)}",
               r"$f'=\frac{-(x^2+4)}{(x^2-3x-4)^2}<0$: \rest{decreixent en tot el domini} $\mathbb R-\{-1,4\}$, sense extrems",
               r"$f'=1-\frac{1}{(x-1)^2}$: creix en $(-\infty,0)\cup(2,+\infty)$, decreix en $(0,1)\cup(1,2)$; \res{\text{màx. }(0,-3)}, \res{\text{mín. }(2,1)}"])),
 (2, r"Monotonia i extrems de funcions trigonomètriques en $[0,2\pi]$:" + tasks(2, [fx(r'\sin x+\cos x'), fx(r'x-2\sin x', 'g')]),
     tasks(1, [r"$f'=\cos x-\sin x=0\Rightarrow x=\frac\pi4,\frac{5\pi}4$: \res{\text{màx. }\left(\frac\pi4,\sqrt2\right)}, \res{\text{mín. }\left(\frac{5\pi}4,-\sqrt2\right)}; creix en $\left(0,\frac\pi4\right)\cup\left(\frac{5\pi}4,2\pi\right)$",
               r"$g'=1-2\cos x=0\Rightarrow x=\frac\pi3,\frac{5\pi}3$; $g''=2\sin x$: \res{\text{mín. }\left(\frac\pi3,\frac\pi3-\sqrt3\right)}, \res{\text{màx. }\left(\frac{5\pi}3,\frac{5\pi}3+\sqrt3\right)}"])),
 (2, r"\pau{Aragó, ordinària 2021} Donada " + '$' + pw((r'x^3+bx+2', r'x\leq0'), (r'\dfrac{\ln(x+1)}{ax}', 'x>0')) + '$' + r", troba $a$ perquè siga contínua en $\mathbb R$ i, a més, $b$ perquè tinga un extrem relatiu en $x=-1$. De quin tipus és?",
     r"$\lim_{x\to0^+}\frac{\ln(x+1)}{ax}=\frac1a=f(0)=2\Rightarrow\res{a=\frac12}$ (per a tot $b$). \ $f'(-1)=3+b=0\Rightarrow\res{b=-3}$; \ $f''(-1)=-6<0$: \rest{màxim relatiu}."),
 (2, r"\pau{Castella-la Manxa, extraordinària 2021} Troba i classifica els extrems relatius de $f(x)=\dfrac{2x^2+2x-2}{3x^2+3}$.",
     r"$f'(x)=\frac{-6(x^2-4x-1)}{(3x^2+3)^2}=0\Leftrightarrow x=2\pm\sqrt5$: \ \res{\text{mín. }\left(2-\sqrt5,-\frac{\sqrt5}{3}\right)}, \ \res{\text{màx. }\left(2+\sqrt5,\frac{\sqrt5}{3}\right)}."),
 (3, r"Estudia la monotonia i els extrems de $f(x)=\sqrt[3]{(x^2-1)^2}$. Quins punts crítics no són de derivada nul·la?",
     r"$f'(x)=\frac{4x}{3\sqrt[3]{x^2-1}}$: s'anul·la en $x=0$ i no existeix en $x=\pm1$. Decreix en $(-\infty,-1)\cup(0,1)$ i creix en $(-1,0)\cup(1,+\infty)$: \res{\text{mín. }(\pm1,0)} (punts de retrocés, no derivables) i \res{\text{màx. }(0,1)}."),
 (2, r"Classifica els punts crítics de $f(x)=x^5-5x^4$ amb el criteri de les derivades successives.",
     r"$f'=5x^3(x-4)$: $x=0$ i $x=4$. \ $f''(4)=320>0$: \res{\text{mín. }(4,-256)}. \ En $x=0$: $f'=f''=f'''=0$ i $f^{(4)}(0)=-120<0$ (ordre parell): \res{\text{màx. }(0,0)}."),
 (2, r"\pau{Aragó, ordinària 2023} Sigui $f(x)=ax-\dfrac{\sin x}{x}+2$ si $x\neq0$ i $f(0)=2$. Troba $a$ perquè $f$ tinga un extrem relatiu en $x=-\frac\pi2$ i digues de quin tipus és.",
     r"$f'(x)=a-\frac{x\cos x-\sin x}{x^2}$, \ $f'\left(-\frac\pi2\right)=a-\frac{4}{\pi^2}=0\Rightarrow\res{a=\frac{4}{\pi^2}}$; \ $f''\left(-\frac\pi2\right)>0$: \rest{mínim relatiu}."),
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
sec("Curvatura i punts d'inflexió",
 (1, r"Estudia la curvatura i troba els punts d'inflexió de:" + tasks(2, [r"\pau{Astúries, ordinària 2020} " + fx(r'x^3-6x^2+9x'), r"\pau{Extremadura, ordinària 2021} " + fx(r'e^{-x^2}'), r"\pau{València, extraordinària 2025} " + fx(r'\dfrac{x}{x^2+1}'), fx(r'\ln\left(x^2+1\right)')])
     + recorda(r"$f''>0$: convexa $\cup$; $\ f''<0$: còncava $\cap$. Hi ha punt d'inflexió on $f''$ canvia de signe (i $f$ és contínua)."),
     tasks(1, [r"$f''=6x-12$: còncava en $(-\infty,2)$, convexa en $(2,+\infty)$, \res{\text{P.I. }(2,2)}",
               r"$f''=(4x^2-2)e^{-x^2}$: convexa en $\left(-\infty,-\frac{\sqrt2}2\right)\cup\left(\frac{\sqrt2}2,+\infty\right)$, còncava entre; \res{\text{P.I. }\left(\pm\frac{\sqrt2}{2},\frac{1}{\sqrt e}\right)}",
               r"$f''=\frac{2x(x^2-3)}{(x^2+1)^3}$: còncava en $(-\infty,-\sqrt3)\cup(0,\sqrt3)$, convexa en $(-\sqrt3,0)\cup(\sqrt3,+\infty)$; \res{\text{P.I. }(0,0),\ \left(\pm\sqrt3,\pm\frac{\sqrt3}{4}\right)}",
               r"$f''=\frac{2(1-x^2)}{(x^2+1)^2}$: convexa en $(-1,1)$, còncava fora; \res{\text{P.I. }(\pm1,\ln2)}"])),
 (2, r"\pau{Castella i Lleó, ordinària 2022} Dada $f(x)=xe^x$, determina'n el domini, les asímptotes, la monotonia, els extrems, la curvatura i els punts d'inflexió.",
     r"Domini $\mathbb R$; AH $y=0$ quan $x\to-\infty$. $f'=(x+1)e^x$: \res{\text{mín. }\left(-1,-\frac1e\right)}. $f''=(x+2)e^x$: còncava en $(-\infty,-2)$, convexa en $(-2,+\infty)$, \res{\text{P.I. }\left(-2,-\frac{2}{e^2}\right)}."),
 (2, r"Troba la recta tangent a la gràfica de $f(x)=x^3-3x^2+2x+1$ en el seu punt d'inflexió. La corba queda per damunt o per davall de la tangent?",
     r"$f''=6x-6=0\Rightarrow x=1$, $f(1)=1$, $f'(1)=-1$: \res{y=-x+2}. Com que és un punt d'inflexió, la tangent \rest{travessa} la corba (per davall a l'esquerra, per damunt a la dreta)."),
 (2, r"Estudia la monotonia i la curvatura de $f(x)=e^x\sin x$ en $[0,2\pi]$.",
     r"$f'=e^x(\sin x+\cos x)$: \res{\text{màx. en }x=\frac{3\pi}4}, \res{\text{mín. en }x=\frac{7\pi}4}. $f''=2e^x\cos x$: convexa en $\left(0,\frac\pi2\right)\cup\left(\frac{3\pi}2,2\pi\right)$, còncava en $\left(\frac\pi2,\frac{3\pi}2\right)$; \res{\text{P.I. en }x=\frac\pi2,\ \frac{3\pi}2}."),
 (2, r"\pau{La Rioja, extraordinària 2022} Troba els intervals de creixement i decreixement, els extrems i els punts d'inflexió de $f(x)=\dfrac{x^3}{(1+x)^2}$.",
     r"$f'=\frac{x^2(x+3)}{(x+1)^3}$: creix en $(-\infty,-3)\cup(-1,+\infty)$, decreix en $(-3,-1)$, \res{\text{màx. }\left(-3,-\frac{27}{4}\right)}. $f''=\frac{6x}{(x+1)^4}$: \res{\text{P.I. }(0,0)} (amb tangent horitzontal)."),
 (3, r"Demostra que tota funció polinòmica de tercer grau $f(x)=ax^3+bx^2+cx+d$ ($a\neq0$) té exactament un punt d'inflexió. Per a quin valor de $x$?",
     r"$f''(x)=6ax+2b$ és de primer grau: s'anul·la en un sol punt, $\res{x=-\frac{b}{3a}}$, i hi canvia de signe. (És, a més, el centre de simetria de la gràfica.)"),
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
sec("Funcions amb paràmetres",
 (1, r"\pau{Madrid, extraordinària 2024}" + tasks(1, [r"Proposa una funció polinòmica de grau 2 la gràfica de la qual siga tangent a la recta $y=x$ en $(0,0)$.", r"Proposa una funció polinòmica de grau 2 que tinga un màxim relatiu en $(1,1)$.", r"Justifica si una funció polinòmica de grau 2 pot tindre dos extrems relatius."]),
     tasks(1, [r"Per exemple $\res{f(x)=x^2+x}$ ($f(0)=0$, $f'(0)=1$).", r"Per exemple $\res{f(x)=-x^2+2x}$ ($f'(1)=0$, $f(1)=1$, $f''<0$).", r"\rest{No}: $f'(x)=2ax+b$ és de primer grau i s'anul·la en un sol punt."])),
 (2, r"Troba el polinomi de tercer grau que té un màxim relatiu en $(-1,4)$ i un mínim relatiu en $(1,0)$."
     + recorda(r"Quatre condicions: $f'(-1)=0$, $f'(1)=0$, $f(-1)=4$, $f(1)=0$."),
     r"$f=ax^3+bx^2+cx+d$: $3a\mp2b+c=0\Rightarrow b=0,\ c=-3a$; \ $2a+d=4$, $-2a+d=0$: \ $\res{f(x)=x^3-3x+2}$ ($f''(-1)=-6<0$ \checkmark)."),
 (2, r"Resol:" + tasks(1, [r"\pau{Andalusia, extraordinària 2026} $f(x)=x^3+ax^2+bx+c$ compleix $f(1)=0$, $x=0$ és un punt crític i la tangent en $x=-1$ és paral·lela a $y+3x=0$. Troba $a$, $b$ i $c$.",
                           r"\pau{Castella i Lleó, extraordinària 2020} Determina $f(x)=x^3+ax^2+bx+c$ si té un punt d'inflexió en $x=1$ i la tangent en $(-1,0)$ és l'eix d'abscisses.",
                           r"\pau{Castella-la Manxa, ordinària 2024} Troba $a$, $b$, $c$ perquè $f(x)=x^3+ax^2+bx+c$ tinga un extrem relatiu en $x=2$ i un punt d'inflexió en $P(1,2)$."]),
     tasks(1, [r"$f'(0)=b=0$, $f'(-1)=3-2a=-3$, $f(1)=1+a+c=0$: $\res{a=3,\ b=0,\ c=-4}$", r"$f''(1)=6+2a=0$, $f'(-1)=3-2a+b=0$, $f(-1)=0$: $\res{f(x)=x^3-3x^2-9x-5}$",
               r"$f''(1)=0\Rightarrow a=-3$; $f'(2)=0\Rightarrow b=0$; $f(1)=2\Rightarrow c=4$: $\res{a=-3,\ b=0,\ c=4}$"])),
 (2, r"Troba $a$ i $b$ perquè $f(x)=(ax+b)\,e^{-x}$ tinga un extrem relatiu en el punt $\left(2,\frac{1}{e^2}\right)$. És màxim o mínim?",
     r"$f'(x)=e^{-x}(a-ax-b)$: $f'(2)=0\Rightarrow b=-a$; $f(2)=(2a+b)e^{-2}=ae^{-2}=e^{-2}\Rightarrow\res{a=1,\ b=-1}$. $f'(x)=e^{-x}(2-x)$ passa de $+$ a $-$: \rest{màxim}."),
 (3, r"Troba $a$ i $b$ perquè $f(x)=x^4+ax^3+bx^2$ tinga en $x=1$ un punt d'inflexió amb tangent horitzontal.",
     r"$f'(1)=4+3a+2b=0$, $f''(1)=12+6a+2b=0\Rightarrow\res{a=-\frac83,\ b=2}$. Comprovació: $f''=4(3x-1)(x-1)$ canvia de signe en 1 \checkmark."),
 (2, r"\pau{Galícia, extraordinària 2021} Troba $a,b,c$ perquè $f(x)=ax^3+bx^2-3x+c$ complisca $f(0)=1$ i tinga extrems relatius en $x=\pm1$. De quin tipus són?",
     r"$\res{a=1,\ b=0,\ c=1}$; $f''(x)=6x$: \rest{màxim en $x=-1$ i mínim en $x=1$}."),
 (2, r"\pau{Aragó, extraordinària 2023} Sigui $f(x)=\left(e^{ax}+b\right)x-e$, $a\neq0$. Calcula $a$ i $b$ sabent que té un extrem relatiu en $x=0$ i un punt d'inflexió en $x=2$.",
     r"$f'(x)=e^{ax}(1+ax)+b$, $f'(0)=1+b=0$; \ $f''(x)=ae^{ax}(2+ax)$, $f''(2)=0\Rightarrow 2+2a=0$: \ $\res{a=-1,\ b=-1}$."),
 (3, r"\pau{Canàries, juny 2018} Determina $a$ i $b$ perquè $f(x)=a\sqrt{3x+3}+b\sqrt{x-1}$ tinga un punt d'inflexió en $(2,8)$.",
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
sec("Teoremes de Rolle i del valor mitjà",
 (1, r"Comprova si es compleixen les hipòtesis del teorema indicat i, si és així, troba els valors de $c$:" + tasks(1, [r"Rolle: $f(x)=x^3-4x$ en $[-2,2]$.", r"Valor mitjà: $f(x)=x^2+2x$ en $[0,2]$.", r"Valor mitjà: $f(x)=\dfrac1x$ en $[1,4]$.", r"Rolle: $f(x)=|x|-1$ en $[-1,1]$."])
     + recorda(r"Rolle: $f$ contínua en $[a,b]$, derivable en $(a,b)$ i $f(a)=f(b)$ $\Rightarrow$ $\exists c\in(a,b)$ amb $f'(c)=0$. Valor mitjà: $f'(c)=\frac{f(b)-f(a)}{b-a}$."),
     tasks(1, [r"Polinomi, $f(\pm2)=0$: $3c^2-4=0\Rightarrow\res{c=\pm\frac{2}{\sqrt3}}$", r"$\frac{8-0}{2}=4=2c+2\Rightarrow\res{c=1}$", r"Contínua i derivable en $[1,4]$: $\frac{1/4-1}{3}=-\frac14=-\frac1{c^2}\Rightarrow\res{c=2}$",
               r"\rest{No es pot aplicar}: no és derivable en $x=0$ (i, efectivament, $f'=\pm1\neq0$)."])),
 (2, r"Troba els paràmetres perquè es complisquen les hipòtesis del teorema de Rolle:" + tasks(1, [r"\pau{Extremadura, extraordinària 2024} " + '$' + pw((r'x^2+ax-b', 'x<0'), (r'a+cx', r'x\geq0')) + '$ en $[-2,2]$.',
                                                                                              r"\pau{Extremadura, ordinària 2023} " + '$' + pw((r'x^2+ax+b', r'0\leq x<1'), (r'cx', r'1\leq x\leq4')) + '$ en $[0,4]$.',
                                                                                              r"\pau{Galícia, setembre 2018} " + '$' + pw((r'2x^2+ax', r'x\leq1'), (r'bx+c', 'x>1')) + '$ en $[0,2]$; troba també el punt on es compleix la tesi.'])
     + recorda(r"Tres condicions: continuïtat en el punt de canvi, derivabilitat en el punt de canvi i $f(a)=f(b)$."),
     tasks(1, [r"$-b=a$, $a=c$, $4-2a-b=a+2c$: $\res{a=1,\ b=-1,\ c=1}$", r"$1+a+b=c$, $2+a=c$, $b=4c$: $\res{a=-\frac74,\ b=1,\ c=\frac14}$", r"$2+a=b+c$, $4+a=b$, $0=2b+c$: $\res{a=-3,\ b=1,\ c=-2}$; \ $4x-3=0\Rightarrow\res{x=\frac34}$"])),
 (2, r"\pau{Castella-la Manxa, extraordinària 2021} Enuncia el teorema de Rolle i usa'l per a raonar si $f(x)=x\sin x-\cos x$ té almenys un extrem relatiu en $[-1,1]$.",
     r"$f$ és contínua i derivable i $f(-1)=f(1)$ (és parella): existeix $c\in(-1,1)$ amb $f'(c)=0$. De fet, $f'(x)=2\sin x+x\cos x$ s'anul·la en $c=0$ i hi passa de $-$ a $+$: hi ha \rest{un mínim relatiu en $x=0$}."),
 (2, r"\pau{Madrid, ordinària 2024} Prova que $f(x)=x^4+\pi x^3+\pi^2x^2+\pi^3x+\pi^4$ té almenys un punt de derivada nul·la en $(-\pi,0)$ usant el teorema de Rolle. Prova-ho de nou amb el teorema de Bolzano.",
     r"Rolle: $f$ és polinòmica i $f(-\pi)=\pi^4=f(0)$. \ Bolzano aplicat a $f'$: $f'(-\pi)=-2\pi^3<0$, $f'(0)=\pi^3>0$ i $f'$ és contínua: \rest{existeix $c\in(-\pi,0)$ amb $f'(c)=0$}."),
 (2, r"\pau{La Rioja, ordinària 2026} Sigui $f(x)=x^3(x-1)^2+1$. Demostra que l'equació $f'(x)=0$ té alguna solució en $(0,1)$.",
     r"$f$ és polinòmica (contínua i derivable) i $f(0)=f(1)=1$: per Rolle, \rest{existeix $c\in(0,1)$ amb $f'(c)=0$}."),
 (3, r"\pau{Navarra, extraordinària 2021} Considera $f(x)=\sqrt{x+\sin\frac{\pi x}{2}}$. Demostra que és contínua en $[1,3]$ i que existeixen $\alpha\in(1,2)$ i $\beta\in(2,3)$ tals que $f'(\alpha)=f'(\beta)=0$.",
     r"En $[1,3]$, $x+\sin\frac{\pi x}{2}\geq x-1\geq0$ i en $x=1$ val 2: el radicand és positiu i $f$ és contínua i derivable. $f(1)=f(2)=f(3)=\sqrt2$: Rolle en $[1,2]$ i en $[2,3]$ dona \rest{$\alpha$ i $\beta$}."),
 (3, r"Demostra que l'equació $x^3+x-1=0$ té exactament una solució real i que és a l'interval $(0,1)$.",
     r"Bolzano: $f(0)=-1<0$, $f(1)=1>0$ $\Rightarrow$ almenys una arrel en $(0,1)$. Si n'hi haguera dues, per Rolle $f'(c)=3c^2+1=0$, impossible: \rest{n'hi ha exactament una}."),
 (3, r"\pau{Extremadura, juliol 2017} Enuncia el teorema del valor mitjà i, aplicant-lo a $f(x)=\dfrac{1}{x^2}$, prova que si $1<a<b$, aleshores $a+b<2a^2b^2$.",
     r"En $[a,b]$: $\frac{1/b^2-1/a^2}{b-a}=-\frac{a+b}{a^2b^2}=f'(c)=-\frac{2}{c^3}$, amb $1<a<c<b$. Per tant $\frac{a+b}{a^2b^2}=\frac{2}{c^3}<2$, és a dir, \rest{$a+b<2a^2b^2$}."),
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
sec("Extrems absoluts",
 (1, r"Troba els extrems absoluts de cada funció en l'interval indicat:" + tasks(2, [r"$f(x)=x^3-3x$ en $[-2,3]$", r"$f(x)=x\,e^{-x}$ en $[0,3]$", r"$f(x)=x-2\ln x$ en $[1,e]$", r"$f(x)=\sin x+\cos x$ en $[0,2\pi]$"])
     + recorda(r"Candidats: els extrems de l'interval, els punts crítics de dins ($f'=0$) i els punts no derivables. El valor més gran és el màxim absolut i el més xicotet, el mínim."),
     tasks(1, [r"$f(-2)=-2$, $f(-1)=2$, $f(1)=-2$, $f(3)=18$: \res{\text{màx. } 18 \text{ en } x=3}, \res{\text{mín. }-2\text{ en }x=-2\text{ i }x=1}",
               r"$f(0)=0$, $f(1)=\frac1e$, $f(3)=\frac3{e^3}$: \res{\text{màx. }\tfrac1e\text{ en }x=1}, \res{\text{mín. }0\text{ en }x=0}",
               r"$f'=1-\frac2x=0\Rightarrow x=2$: $f(1)=1$, $f(2)=2-2\ln2\approx0{,}61$, $f(e)=e-2\approx0{,}72$: \res{\text{màx. }1\text{ en }x=1}, \res{\text{mín. }2-2\ln2\text{ en }x=2}",
               r"\res{\text{màx. }\sqrt2\text{ en }x=\tfrac\pi4}, \res{\text{mín. }-\sqrt2\text{ en }x=\tfrac{5\pi}4}"])),
 (2, r"\pau{València, extraordinària 2026} El coeficient de gravetat d'un brot de grip $t$ dies després de començar compleix $F'(t)=t^2(10-t)$. Calcula $F(t)$ si $F(0)=6$, i quants dies després s'arriba al màxim i quin és.",
     r"$F(t)=\frac{10t^3}{3}-\frac{t^4}{4}+6$. $F'>0$ en $(0,10)$ i $<0$ en $(10,+\infty)$: màxim \res{\text{als 10 dies}}, $F(10)=\res{\frac{2518}{3}\approx839{,}33}$."),
 (2, r"\pau{València, ordinària 2026} Calcula els valors màxims i mínims, relatius i absoluts, de $f(x)=\dfrac{x+1}{x^2+1}$.",
     r"$f'=\frac{-x^2-2x+1}{(x^2+1)^2}$: \res{\text{mín. }\left(-1-\sqrt2,\tfrac{1-\sqrt2}{2}\right)}, \res{\text{màx. }\left(-1+\sqrt2,\tfrac{1+\sqrt2}{2}\right)}; com que $f\to0$ en $\pm\infty$, també són \rest{absoluts}."),
 (2, r"\pau{Astúries, extraordinària 2025} La quantitat d'aigua d'un dipòsit és $f(t)=2\cos\left(t+\frac\pi2\right)+10$, $t\in[0,4]$ hores. Calcula'n els màxims i mínims, demostra que no es buida mai i digues durant quant de temps augmenta.",
     r"$f=10-2\sin t$, $f'=-2\cos t=0\Rightarrow t=\frac\pi2$. $f(0)=10$, $f\left(\frac\pi2\right)=8$, $f(4)\approx11{,}51$: \res{\text{mín. }8\ \left(t=\tfrac\pi2\right)}, \res{\text{màx. }\approx11{,}51\ (t=4)}. No es buida ($f\geq8$). Augmenta en $\left(\frac\pi2,4\right)$: \res{\approx2{,}43\text{ h}}."),
 (2, r"\pau{Madrid, extraordinària 2023} El consum d'un vehicle (litres/100 km) a velocitat $v$ (desenes de km/h) és $c(v)=\frac{5v}{3}$ si $0\leq v<3$ i $c(v)=14-4v+\frac{v^2}{3}$ si $v\geq3$." + tasks(1, [r"Si ha de circular a més de 3 desenes de km/h, a quina velocitat el consum és mínim?", r"Si $1\leq v\leq8$, quins són el consum màxim i el mínim?"]),
     tasks(1, [r"$c'(v)=-4+\frac{2v}3=0\Rightarrow v=6$: \res{60\text{ km/h}} (2 l/100 km).", r"$c(1)=\frac53$, $c(3)=5$, $c(6)=2$, $c(8)=\frac{10}3$: \res{\text{mín. }\tfrac53\ (v=1)}, \res{\text{màx. }5\ (v=3)}."])),
 (3, r"\pau{Navarra, ordinària 2025} El preu del kWh entre $t=0$ i $t=1$ és $p(t)=0{,}15+\sin^2\left(\frac\pi2t\right)\cos\left(\frac\pi2t\right)$. Calcula els instants en què el preu és màxim i mínim.",
     r"Amb $s=\frac\pi2t$: $\frac{d}{ds}\left(\sin^2s\cos s\right)=\sin s\left(2\cos^2s-\sin^2s\right)=0\Rightarrow\tan s=\sqrt2$. \res{\text{Màxim en }t=\tfrac2\pi\arctan\sqrt2\approx0{,}61}, $p\approx0{,}535$; \res{\text{mínim }0{,}15\text{ en }t=0\text{ i }t=1}."),
 (2, r"\pau{Castella-la Manxa, ordinària 2025} La concentració de virus actius és $f(t)=5(t+1)e^{-t}$, $t\geq0$. En quin instant la derivada $f'(t)$ pren el valor més xicotet? Quin és el valor a llarg termini?",
     r"$f'(t)=-5te^{-t}$, \ $f''(t)=5(t-1)e^{-t}$: $f'$ és mínima en \res{t=1} ($f'(1)=-\frac5e$). \ $\lim_{t\to+\infty}f(t)=\res{0}$."),
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
sec("Problemes d'optimització",
 (2, r"\pau{València, ordinària 2025} Una empresa vol fer caixes de 80 cm$^3$ amb base i tapa quadrades. El material de les parets laterals costa 1 cèntim per cm$^2$ i el de la base i la tapa és un 25\,\% més car." + tasks(1, [r"Escriu el preu del material $P(x)$ en funció del costat $x$ de la base.", r"Troba les dimensions de la caixa més barata.", r"Quin és el preu en aquest cas?"])
     + recorda(r"Volum: $x^2h=80$. Àrea lateral: $4xh$; base i tapa: $2x^2$."),
     tasks(1, [r"$h=\frac{80}{x^2}$: \ $\res{P(x)=\frac{320}{x}+2{,}5x^2}$ cèntims", r"$P'(x)=-\frac{320}{x^2}+5x=0\Rightarrow x^3=64$: \res{4\times4\times5\text{ cm}}", r"$P(4)=80+40=\res{120\text{ cèntims}=1{,}20\text{ €}}$"])),
 (2, r"\pau{València, ordinària 2023} El tall vertical de l'entrada a una plaça emmurallada té forma de paràbola $y=-x^2+12$ ($x$, $y$ en metres; $y=0$ és el terra). Volem posar-hi una porta rectangular amb els dos cantons de dalt sobre la paràbola i els de baix a terra. Calcula les dimensions de la porta de superfície màxima i l'àrea de la part de l'entrada que queda tapada amb pedra.",
     r"$A(x)=2x(12-x^2)$, $0<x<\sqrt{12}$; $A'=24-6x^2=0\Rightarrow x=2$: porta de \res{4\text{ m}\times8\text{ m}} ($32$ m$^2$). Àrea de l'entrada: $\int_{-\sqrt{12}}^{\sqrt{12}}(12-x^2)\,dx=16\sqrt{12}$; pedra: \res{16\sqrt{12}-32\approx23{,}4\text{ m}^2}."),
 (2, r"\pau{València, ordinària 2022} Es vol construir un quadrat i un triangle equilàter tallant en dues parts un cable d'acer de 240 m." + tasks(1, [r"Calcula la suma de les àrees en funció del costat $x$ del triangle.", r"Calcula la longitud de cable que cal per al triangle perquè la suma de les àrees siga mínima."]),
     tasks(1, [r"$\res{S(x)=\frac{\sqrt3}{4}x^2+\left(\frac{240-3x}{4}\right)^2}$, $0\leq x\leq80$", r"$S'=\frac{\sqrt3}{2}x-\frac38(240-3x)=0\Rightarrow x=\frac{720}{9+4\sqrt3}$; cable: $3x=\res{\frac{2160}{9+4\sqrt3}\approx135{,}6\text{ m}}$"])),
 (2, r"\pau{València, ordinària 2021} Un espill quadrat de 80 cm de costat s'ha trencat per un cantó; el tros caigut és un triangle rectangle de catets 32 cm (horitzontal) i 40 cm (vertical). Retallem una peça rectangular $R$ amb un vèrtex $(x,y)$ sobre la línia de trencament i el vèrtex oposat en el cantó contrari de l'espill. Troba l'àrea de $R$ en funció de $x$ ($0\leq x\leq32$), les dimensions de $R$ d'àrea màxima i aquesta àrea.",
     r"$y=40-\frac54x$; $A(x)=(80-x)(80-y)=\res{-\frac54x^2+60x+3200}$; $A'=0\Rightarrow x=24$: \res{56\text{ cm}\times70\text{ cm}}, $A=\res{3920\text{ cm}^2}$."),
 (2, r"\pau{València, ordinària 2020} En un triangle isòsceles els dos costats iguals mesuren 10 cm. Expressa l'àrea en funció de la longitud $x$ del tercer costat, estudia'n la monotonia en $[0,20]$ i troba el valor de $x$ que fa màxima l'àrea.",
     r"$A(x)=\frac{x\sqrt{400-x^2}}{4}$; creix en $\left(0,\sqrt{200}\right)$ i decreix en $\left(\sqrt{200},20\right)$: màxim per a $\res{x=10\sqrt2}$, $A=\res{50\text{ cm}^2}$ (el triangle és rectangle)."),
 (2, r"\pau{València, juliol 2019} Un projectil unit al punt $(0,2)$ per una corda elàstica recorre la corba $y=4-x^2$ entre $(-2,0)$ i $(2,0)$. Troba la distància entre un punt de la corba i $(0,2)$ en funció de $x$, i els punts de la corba més allunyats i més pròxims a $(0,2)$.",
     r"$d(x)=\sqrt{x^4-3x^2+4}$. Derivem el radicand: $4x^3-6x=0\Rightarrow x=0,\ \pm\sqrt{\frac32}$. Més pròxims: \res{\left(\pm\sqrt{\tfrac32},\tfrac52\right)}; més allunyats (comparant amb els extrems): \res{(\pm2,0)}, amb $d=\sqrt8$."),
 (2, r"\pau{València, juliol 2018} Dins d'una cartolina rectangular es vol fer un dibuix rectangular $R$ de 600 cm$^2$, amb marges de 3 cm dalt i baix i de 2 cm als costats. Calcula l'àrea de la cartolina en funció de la base $x$ de $R$ i les dimensions de la cartolina d'àrea mínima.",
     r"$A(x)=(x+4)\left(\frac{600}{x}+6\right)=\res{624+6x+\frac{2400}{x}}$; $A'=6-\frac{2400}{x^2}=0\Rightarrow x=20$: cartolina de \res{24\text{ cm}\times36\text{ cm}}."),
 (3, r"\pau{València, juliol 2017} Es considera el triangle de vèrtexs $O(0,0)$, $A(x,y)$ i $B(0,y)$, amb $x,y>0$, tal que $\overline{OA}+\overline{AB}=30$ m. Troba l'àrea en funció de $x$, el valor de $x$ per al qual és màxima i aquesta àrea.",
     r"$\sqrt{x^2+y^2}=30-x\Rightarrow y=\sqrt{900-60x}$; $\res{A(x)=\frac{x\sqrt{900-60x}}{2}}$, $0< x<15$. Maximitzem $A^2$: $(900x^2-60x^3)'=0\Rightarrow\res{x=10}$; $A=5\sqrt{300}=\res{50\sqrt3\approx86{,}6\text{ m}^2}$."),
 (2, r"\pau{Andalusia, ordinària 2026} Una finestra té forma de rectangle coronat per un semicercle. Si el perímetre de la finestra mesura 8 m, troba les dimensions que permeten la màxima entrada de llum.",
     r"Base $x$, altura $y$: $x+2y+\frac{\pi x}{2}=8$, $A=xy+\frac{\pi x^2}{8}=4x-\frac{x^2}{2}-\frac{\pi x^2}{8}$; $A'=0\Rightarrow\res{x=\frac{16}{4+\pi}\approx2{,}24\text{ m}}$, $\res{y=\frac{8}{4+\pi}\approx1{,}12\text{ m}}$."),
 (2, r"\pau{Aragó, extraordinària 2021} Es vol construir un dipòsit obert (sense tapa) en forma de prisma de base quadrada i 64 m$^3$ de capacitat. Els laterals costen 70 €/m$^2$ i la base, 140 €/m$^2$. Troba les dimensions del dipòsit més econòmic.",
     r"$h=\frac{64}{x^2}$; $C(x)=140x^2+70\cdot4xh=140x^2+\frac{17\,920}{x}$; $C'=280x-\frac{17\,920}{x^2}=0\Rightarrow x^3=64$: un \res{\text{cub de 4 m d'aresta}}."),
 (2, r"\pau{Aragó, setembre 2018} De tots els triangles rectangles que tenen una àrea d'1 cm$^2$, troba el que té la hipotenusa més curta i dona les longituds dels tres costats.",
     r"Catets $x$ i $\frac2x$: $h^2=x^2+\frac{4}{x^2}$; $(h^2)'=2x-\frac{8}{x^3}=0\Rightarrow x=\sqrt2$: catets \res{\sqrt2\text{ i }\sqrt2\text{ cm}}, hipotenusa \res{2\text{ cm}}."),
 (2, r"\pau{Canàries, ordinària 2023} Es vol construir una Casa de la Joventut de 240 m$^2$ envoltada d'una zona enjardinada que deixa 3 m dalt, 3 m baix, 3 m a l'esquerra i 7 m a la dreta. Quines dimensions ha de tindre la casa perquè la zona enjardinada siga mínima? Quina és aquesta àrea?",
     r"Casa $x\times\frac{240}{x}$: jardí $=(x+10)\left(\frac{240}{x}+6\right)-240=6x+\frac{2400}{x}+60$; mínim per a $x=20$: casa de \res{20\text{ m}\times12\text{ m}}, jardí de \res{300\text{ m}^2}."),
 (2, r"\pau{Castella-la Manxa, extraordinària 2023} Un aparcament té forma de rectangle de costats $h$ i $r$ amb un semicercle de radi $\frac h2$ adossat al costat $h$. Si la tanca fa 80 m de perímetre, quant han de valdre $h$ i $r$ perquè l'àrea siga màxima?",
     r"$h+2r+\frac{\pi h}{2}=80$, $A=hr+\frac{\pi h^2}{8}=40h-\frac{h^2}2-\frac{\pi h^2}{8}$; $A'=0\Rightarrow\res{h=\frac{160}{4+\pi}\approx22{,}4\text{ m}}$, $\res{r=\frac{80}{4+\pi}\approx11{,}2\text{ m}}$."),
 (2, r"\pau{Galícia, juliol 2019} De tots els triangles rectangles del primer quadrant que tenen un vèrtex en l'origen, un altre sobre la paràbola $y=4-x^2$, un catet sobre l'eix $X$ i l'altre paral·lel a l'eix $Y$, troba els catets i la hipotenusa del d'àrea màxima.",
     r"$A(x)=\frac{x(4-x^2)}{2}$, $0< x<2$; $A'=\frac{4-3x^2}{2}=0\Rightarrow x=\frac{2}{\sqrt3}$: catets \res{\tfrac{2}{\sqrt3}\text{ i }\tfrac83}, hipotenusa \res{\tfrac{\sqrt{76}}{3}}."),
 (2, r"\pau{La Rioja, extraordinària 2024} Un nedador està a 2 km de la platja, enfront del lloc de la Creu Roja. Vol anar a les dutxes, a la platja i a 3 km de la Creu Roja. Neda a 3 km/h i camina per l'arena a 5 km/h. On ha d'arribar nadant per a tardar el mínim?",
     r"Si arriba a $x$ km de la Creu Roja: $T(x)=\frac{\sqrt{4+x^2}}{3}+\frac{3-x}{5}$; $T'=0\Rightarrow5x=3\sqrt{4+x^2}\Rightarrow x=\frac32$: \res{\text{a 1,5 km de la Creu Roja}} (a mig camí)."),
 (3, r"\pau{Múrcia, juny 2019} En un triangle isòsceles de base 12 cm (costat desigual) i altura 5 cm, busquem un punt $A$ de l'altura, a distància $x$ de la base, tal que la suma de les distàncies d'$A$ als tres vèrtexs siga mínima. Comprova que aquesta suma és $f(x)=5-x+2\sqrt{x^2+36}$, troba $x$ i el valor mínim.",
     r"$f'(x)=-1+\frac{2x}{\sqrt{x^2+36}}=0\Rightarrow3x^2=36\Rightarrow\res{x=\sqrt{12}=2\sqrt3}$; $f\left(\sqrt{12}\right)=\res{5+6\sqrt3\approx15{,}39\text{ cm}}$."),
 (2, r"\pau{Navarra, ordinària 2026} D'un full de 20 cm $\times$ 30 cm es retalla un quadrat en cada cantó per a fer una caixa sense tapa doblegant les solapes. Calcula el costat del quadrat perquè el volum siga màxim.",
     r"$V(x)=x(20-2x)(30-2x)$, $0< x<10$; $V'=12x^2-200x+600=0\Rightarrow\res{x=\frac{25-5\sqrt7}{3}\approx3{,}92\text{ cm}}$ (l'altra arrel no és del domini)."),
 (2, r"\pau{País Basc, extraordinària 2024} Una empresa fabrica tasses cilíndriques (sense tapa) de $216\pi$ cm$^3$ i vol que siguen tan econòmiques com siga possible. Quines dimensions han de tindre?",
     r"$r^2h=216$, $S=\pi r^2+2\pi rh=\pi r^2+\frac{432\pi}{r}$; $S'=0\Rightarrow r^3=216$: \res{r=6\text{ cm},\ h=6\text{ cm}}."),
 (2, r"\pau{Catalunya, extraordinària 2024} Per a cada punt $(x,y)$ de la corba $y=e^{-2x}$ amb $x>0$, considera el rectangle de vèrtexs $(0,0)$, $(x,0)$, $(0,y)$ i $(x,y)$. Comprova que el d'àrea màxima és el de $x=\frac12$ i calcula'n l'àrea.",
     r"$A(x)=xe^{-2x}$, $A'=(1-2x)e^{-2x}=0\Rightarrow x=\frac12$ ($A'$ passa de $+$ a $-$): \res{A=\tfrac{1}{2e}\text{ u}^2}."),
 (3, r"\pau{Canàries, juny 2018} Un fil de 140 m es divideix en tres trossos, un dels quals fa el doble que un altre. Amb cada tros es fa un quadrat. Quina longitud ha de tindre cada tros perquè la suma de les àrees siga mínima?",
     r"Trossos $x$, $2x$ i $140-3x$: $S=\frac{x^2}{16}+\frac{4x^2}{16}+\frac{(140-3x)^2}{16}$; $S'=\frac{10x-6(140-3x)}{16}=0\Rightarrow x=30$: \res{30,\ 60\text{ i }50\text{ m}}."),
 (2, r"\pau{Astúries, extraordinària 2025} Es vol construir una caixa sense tapa amb dues cares paral·leles quadrades de costat $x$ i tres cares rectangulars de costats $x$ i $y$. Si es volen gastar 3 m$^2$ de material, quins valors de $x$ i $y$ fan màxima la capacitat?",
     r"$2x^2+3xy=3\Rightarrow y=\frac{3-2x^2}{3x}$; $V=x^2y=x-\frac{2x^3}{3}$, $V'=1-2x^2=0$: \res{x=\tfrac{\sqrt2}{2}\approx0{,}71\text{ m}}, \res{y=\tfrac{2\sqrt2}{3}\approx0{,}94\text{ m}}."),
)

# =====================================================================
# 10–12. Representació de funcions
REP = recorda(r"Domini, simetria, talls, asímptotes, monotonia i extrems, curvatura i inflexió; després situem tota la informació i dibuixem.")
def rep(fn): return r"Fes l'estudi complet i representa " + fn + "."
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
sec("Representació de funcions polinòmiques i racionals",
 (1, rep(r"\pau{Andalusia, ordinària 2021} " + fx(r'4x^3-x^4')) + REP,
     r"Domini $\mathbb R$. Talls $(0,0)$ i $(4,0)$. $f'=4x^2(3-x)$: creix en $(-\infty,3)$, decreix en $(3,+\infty)$; \res{\text{màx. }(3,27)}. $f''=12x(2-x)$: \res{\text{P.I. }(0,0)\text{ i }(2,16)}; còncava fora de $(0,2)$."
     + cen(graf([lambda v: 4 * v**3 - v**4], (-1.5, 4.5, -10, 32), pts=[(0, 0), (4, 0)], mx=[(3, 27)], ip=[(0, 0), (2, 16)]))),
 (2, rep(r"\pau{València, extraordinària 2025} " + fx(r'\dfrac{x}{x^2+1}')),
     r"Domini $\mathbb R$, senar, tall $(0,0)$. AH $\res{y=0}$. $f'=\frac{1-x^2}{(x^2+1)^2}$: \res{\text{mín. }\left(-1,-\tfrac12\right)}, \res{\text{màx. }\left(1,\tfrac12\right)} (també absoluts). P.I. en $x=0$, $x=\pm\sqrt3$."
     + cen(graf([lambda v: v / (v * v + 1)], (-6, 6, -0.8, 0.8), ha=[0], pts=[(0, 0)], mx=[(1, 0.5)], mn=[(-1, -0.5)], ip=[(-r3, -r3 / 4), (r3, r3 / 4)]))),
 (2, rep(r"\pau{València, ordinària 2022} " + fx(r'\dfrac{x^2+3}{x^2-4}')),
     r"Domini $\mathbb R-\{\pm2\}$, parella, tall $\left(0,-\frac34\right)$. AV $\res{x=\pm2}$, AH $\res{y=1}$. $f'=\frac{-14x}{(x^2-4)^2}$: creix en $(-\infty,-2)\cup(-2,0)$, decreix en $(0,2)\cup(2,+\infty)$; \res{\text{màx. }\left(0,-\tfrac34\right)}. Sense inflexió."
     + cen(graf([lambda v: (v * v + 3) / (v * v - 4)], (-6, 6, -6, 7), va=[-2, 2], ha=[1], mx=[(0, -0.75)]))),
 (2, rep(r"\pau{València, juny 2017} " + fx(r'\dfrac{x^2+1}{x}')),
     r"Domini $\mathbb R-\{0\}$, senar, sense talls. AV $\res{x=0}$, AO $\res{y=x}$. \res{\text{màx. }(-1,-2)}, \res{\text{mín. }(1,2)}. $f''=\frac{2}{x^3}$: còncava en $(-\infty,0)$, convexa en $(0,+\infty)$."
     + cen(graf([lambda v: (v * v + 1) / v], (-5, 5, -7, 7), va=[0], oa=[(1, 0)], mx=[(-1, -2)], mn=[(1, 2)]))),
 (3, rep(r"\pau{Astúries, extraordinària 2022} " + fx(r'\dfrac{2x^2}{1-x}')),
     r"Domini $\mathbb R-\{1\}$, tall $(0,0)$. AV $\res{x=1}$, AO $\res{y=-2x-2}$. $f'=\frac{2x(2-x)}{(1-x)^2}$: \res{\text{mín. }(0,0)}, \res{\text{màx. }(2,-8)}. Sense inflexió."
     + cen(graf([lambda v: 2 * v * v / (1 - v)], (-5, 6, -20, 12), va=[1], oa=[(-2, -2)], mn=[(0, 0)], mx=[(2, -8)]))),
)
sec("Representació de funcions radicals, exponencials i logarítmiques",
 (2, rep(r"\pau{València, extraordinària 2021} " + fx(r'x\,e^{1-x^2}')) + REP,
     r"Domini $\mathbb R$, senar, tall $(0,0)$, AH $\res{y=0}$. $f'=e^{1-x^2}(1-2x^2)$: \res{\text{mín. }\left(-\tfrac{\sqrt2}{2},-\sqrt{\tfrac e2}\right)}, \res{\text{màx. }\left(\tfrac{\sqrt2}{2},\sqrt{\tfrac e2}\right)}. P.I. en $x=0$ i $x=\pm\sqrt{\frac32}$."
     + cen(graf([lambda v: v * me(1 - v * v)], (-3, 3, -1.5, 1.5), ha=[0], pts=[(0, 0)], mx=[(r2 / 2, math.sqrt(math.e / 2))], mn=[(-r2 / 2, -math.sqrt(math.e / 2))]))),
 (2, rep(r"\pau{València, ordinària 2023} " + fx(r'\dfrac1x+\ln(x+1)')),
     r"Domini $(-1,0)\cup(0,+\infty)$. AV $\res{x=-1}$ i $\res{x=0}$. $f'=\frac{x^2-x-1}{x^2(x+1)}$: \res{\text{màx. en }x=\tfrac{1-\sqrt5}{2}}, \res{\text{mín. en }x=\tfrac{1+\sqrt5}{2}}."
     + cen(graf([(lambda v: 1 / v + mln(v + 1), -0.999, 8)], (-1.3, 6, -6, 6), va=[-1, 0], mx=[((1 - math.sqrt(5)) / 2, 1 / ((1 - math.sqrt(5)) / 2) + mln((1 - math.sqrt(5)) / 2 + 1))], mn=[((1 + math.sqrt(5)) / 2, 1 / ((1 + math.sqrt(5)) / 2) + mln((1 + math.sqrt(5)) / 2 + 1))]))),
 (2, rep(r"\pau{Madrid, extraordinària 2026} " + fx(r'\dfrac{x}{\ln x}')),
     r"Domini $(0,1)\cup(1,+\infty)$. AV $\res{x=1}$; $\lim_{x\to0^+}f=0$. $f'=\frac{\ln x-1}{\ln^2x}$: decreix en $(0,1)\cup(1,e)$, creix en $(e,+\infty)$; \res{\text{mín. }(e,e)}. $f''=\frac{2-\ln x}{x\ln^3x}$: \res{\text{P.I. }\left(e^2,\tfrac{e^2}{2}\right)}."
     + cen(graf([(lambda v: v / mln(v), 0.001, 12)], (-0.5, 12, -8, 10), va=[1], mn=[(math.e, math.e)], ip=[(math.e**2, math.e**2 / 2)]))),
 (2, rep(r"\pau{País Basc, juliol 2018} " + fx(r'x^2e^{-x}')),
     r"Domini $\mathbb R$, tall $(0,0)$, $f\geq0$. AH $\res{y=0}$ quan $x\to+\infty$. $f'=x(2-x)e^{-x}$: \res{\text{mín. }(0,0)}, \res{\text{màx. }\left(2,\tfrac{4}{e^2}\right)}. P.I. en $x=2\pm\sqrt2$."
     + cen(graf([lambda v: v * v * me(-v)], (-1.5, 9, -0.2, 1.2), ha=[0], mn=[(0, 0)], mx=[(2, 4 / math.e**2)], ip=[(2 - r2, (2 - r2)**2 * me(r2 - 2)), (2 + r2, (2 + r2)**2 * me(-2 - r2))]))),
 (3, rep(r"\pau{Múrcia, setembre 2018} " + fx(r'x\sqrt{18-x^2}') + " (en tot el seu domini)"),
     r"Domini $\left[-3\sqrt2,3\sqrt2\right]$, senar, talls $(0,0)$ i $\left(\pm3\sqrt2,0\right)$ (amb tangent vertical). $f'=\frac{18-2x^2}{\sqrt{18-x^2}}$: \res{\text{mín. }(-3,-9)}, \res{\text{màx. }(3,9)}."
     + cen(graf([(lambda v: v * msq(18 - v * v), -3 * r2, 3 * r2)], (-5, 5, -10, 10), pts=[(0, 0), (-3 * r2, 0), (3 * r2, 0)], mn=[(-3, -9)], mx=[(3, 9)]))),
)
sec("Representació de funcions trigonomètriques i a trossos",
 (2, rep(fx(r'2\sin x+\sin2x')) + REP,
     r"Període $2\pi$, senar. Talls $x=k\pi$. \res{\text{màx. }\left(\tfrac\pi3,\tfrac{3\sqrt3}{2}\right)}, \res{\text{mín. }\left(\tfrac{5\pi}3,-\tfrac{3\sqrt3}{2}\right)} ($+2k\pi$); en $x=\pi$, $f'=0$ sense extrem. P.I. en $x=k\pi$ i on $\cos x=-\frac14$."
     + cen(graf([lambda v: 2 * ms(v) + ms(2 * v)], (-1, 7.3, -3, 3), mx=[(PI / 3, 3 * r3 / 2)], mn=[(5 * PI / 3, -3 * r3 / 2)], ip=[(PI, 0)], pts=[(0, 0), (2 * PI, 0)], xt=[(PI / 2, r'\frac\pi2'), (PI, r'\pi'), (3 * PI / 2, r'\frac{3\pi}2'), (2 * PI, r'2\pi')]))),
 (2, r"\pau{València, ordinària 2026 · Madrid, ordinària 2025} Un decorador pinta en una paret de 12 m de llarg i 3 m d'alt la corba $f(x)=\cos\frac{\pi x}{9}+2$. Dibuixa-la en $[0,12]$ amb els talls amb els eixos, els extrems absoluts i la monotonia. Està la corba dins de la paret?",
     r"Talla OY en $(0,3)$; no talla OX. $f'=-\frac\pi9\sin\frac{\pi x}{9}$: decreix en $[0,9]$, creix en $[9,12]$; \res{\text{màx. abs. }(0,3)}, \res{\text{mín. abs. }(9,1)}, $f(12)=\frac32$. Com que $1\leq f\leq3$, \rest{sí}."
     + cen(graf([(lambda v: mc(PI * v / 9) + 2, 0, 12)], (-0.5, 12.5, 0, 3.5), pts=[(12, 1.5)], mx=[(0, 3)], mn=[(9, 1)]))),
 (2, r"\pau{Galícia, ordinària 2023} Estudia si $f(x)=x+\sin x$ té extrems o punts d'inflexió en $(0,2\pi)$ i esbossa'n la gràfica.",
     r"$f'=1+\cos x\geq0$: creixent, \rest{sense extrems}. $f''=-\sin x$: còncava en $(0,\pi)$, convexa en $(\pi,2\pi)$; \res{\text{P.I. }(\pi,\pi)} (amb tangent horitzontal)."
     + cen(graf([(lambda v: v + ms(v), 0, 2 * PI)], (-0.3, 6.6, -0.3, 6.6), ip=[(PI, PI)], xt=[(PI, r'\pi'), (2 * PI, r'2\pi')]))),
 (2, rep(fx(r'\sin^2x')),
     r"Període $\pi$, parella, $0\leq f\leq1$. \res{\text{mín. }(k\pi,0)}, \res{\text{màx. }\left(\tfrac\pi2+k\pi,1\right)}. $f''=2\cos2x$: P.I. en $x=\frac\pi4+\frac{k\pi}2$."
     + cen(graf([lambda v: ms(v)**2], (-3.5, 6.6, -0.3, 1.4), mn=[(0, 0), (PI, 0), (2 * PI, 0), (-PI, 0)], mx=[(PI / 2, 1), (3 * PI / 2, 1), (-PI / 2, 1)], xt=[(-PI, r'-\pi'), (PI, r'\pi'), (2 * PI, r'2\pi')]))),
 (2, r"\pau{Andalusia, ordinària 2022} Sigui " + '$' + pw((r'2x+4', 'x<0'), (r'(x-2)^2', r'x\geq0')) + '$' + r". Calcula els punts de tall amb l'eix d'abscisses, estudia'n la continuïtat, la derivabilitat i els extrems, i esbossa la gràfica.",
     r"Talls $(-2,0)$ i $(2,0)$. Contínua ($4=4$) però no derivable en 0 ($f'(0^-)=2\neq-4=f'(0^+)$). Creix en $(-\infty,0)\cup(2,+\infty)$ i decreix en $(0,2)$: \res{\text{màx. }(0,4)} (punt anguló) i \res{\text{mín. }(2,0)}."
     + cen(graf([(lambda v: 2 * v + 4, -4, 0), (lambda v: (v - 2)**2, 0, 5)], (-3.5, 5, -2, 6), pts=[(-2, 0)], mx=[(0, 4)], mn=[(2, 0)]))),
 (3, rep(fx(r'\left|x^2-4x\right|')),
     r"$f=x^2-4x$ si $x\leq0$ o $x\geq4$, i $-x^2+4x$ si $0< x<4$. \res{\text{mín. }(0,0),\ (4,0)} (punts angulosos), \res{\text{màx. }(2,4)}; convexa fora de $[0,4]$ i còncava dins."
     + cen(graf([lambda v: abs(v * v - 4 * v)], (-2, 6, -1, 8), mn=[(0, 0), (4, 0)], mx=[(2, 4)]))),
)

# =====================================================================
print(NCHK[0], 'comprovacions correctes')
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Aplicacions de la derivada"
def build(sol):
    tt = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 7: %s. 2n de Batxillerat MII}" % (tt, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 7: %s · 2n Batxillerat MII" % (tt, TIT))
    assert 'MII}' in p and '2n Batxillerat MII' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques II}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 7' if sol else "Fitxa d'exercicis · Unitat 7") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Les gràfiques de les solucions marquen en verd els màxims, en roig els mínims i en violeta els punts d'inflexió; les línies discontínues són asímptotes. Pots comprovar els estudis complets amb la calculadora dels apunts interactius."
             if sol else r"Resol els exercicis al quadern justificant cada pas. Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat de València i d'altres comunitats autònomes, traduïts al valencià. Pots comprovar els resultats amb les eines dels apunts interactius (L'Hôpital pas a pas, estudi complet d'una funció, optimització\dots).") + r'''
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
    name = 't7-fitxa-solucions.tex' if sol else 't7-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'exercicis,', npau, 'de la PAU de', len(regs), 'comunitats:', ', '.join(regs))
