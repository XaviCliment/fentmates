# Versió en castellà de genera.py. Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 8: Integrals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Com a la unitat 7, les gràfiques de les solucions es calculen ací mateix amb Python i es dibuixen amb TikZ com a
# poligonals (graf); ara, a més, ombregen les àrees. Les integrals i les àrees es comproven de manera exacta amb
# fraccions (CHK, al final): els polinomis s'escriuen com a Q(coeficients de grau més alt a més baix).
# Ús: python3 genera.py && pdflatex t8-fitxa-exercicis.tex (dues vegades) && pdflatex t8-fitxa-solucions.tex
import os, re, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def I(f, a=None, b=None): return r'$\displaystyle\int' + ('_{%s}^{%s}' % (a, b) if a is not None else '') + ' ' + f + r'\,dx$'

# ---------- polinomis exactes ----------
class Q:
    """Polinomi amb coeficients fraccionaris: Q(1, -4, 3) és x^2 - 4x + 3."""
    def __init__(self, *c): self.c = [Fr(x) for x in reversed(c)]  # c[k]: coeficient de x^k
    def __call__(self, x):
        if isinstance(x, Fr): return sum((ck * x**k for k, ck in enumerate(self.c)), Fr(0))
        return sum(float(ck) * x**k for k, ck in enumerate(self.c))
    def __sub__(self, o):
        n = max(len(self.c), len(o.c)); r = Q(); r.c = [(self.c[k] if k < len(self.c) else 0) - (o.c[k] if k < len(o.c) else 0) for k in range(n)]; return r
    def prim(self): r = Q(); r.c = [Fr(0)] + [ck / (k + 1) for k, ck in enumerate(self.c)]; return r
    def deriv(self): r = Q(); r.c = [ck * k for k, ck in enumerate(self.c)][1:] or [Fr(0)]; return r
    def roots(self):
        """arrels racionals (n/d amb |n/d| <= 20, d <= 12): als exercicis totes les arrels ho són"""
        out = set()
        for d in range(1, 13):
            for n in range(-20 * d, 20 * d + 1):
                if self(Fr(n, d)) == 0: out.add(Fr(n, d))
        return sorted(out)
def integ(p, a, b): P = p.prim(); return P(Fr(b)) - P(Fr(a))
def area(f, g=None, a=None, b=None):
    """àrea exacta entre f i g (o l'eix OX); sense a, b: recinte tancat entre els talls"""
    h = f - g if g else f
    rs = h.roots()
    if a is None: pts = rs
    else: pts = [Fr(a)] + [r for r in rs if Fr(a) < r < Fr(b)] + [Fr(b)]
    return sum(abs(integ(h, p, q)) for p, q in zip(pts, pts[1:]))

# ---------- gràfiques ----------
def nice(r):
    for s in (0.5, 1, 2, 5, 10, 20, 50, 100):
        if r / s <= 8: return s
    return 200
def fnum(v): return ('%g' % v).replace('.', '{,}')
FILL = {'+': 'green!55!black', '-': 'red!70!black', '=': 'teal'}
def graf(curves, box, fills=(), va=(), pts=(), labs=(), w=4.6, h=3.4):
    """curves: llista de funcions o de (f, a, b, color); fills: (f, g o None, a, b, clau de FILL); box: (x0, x1, y0, y1)."""
    x0, x1, y0, y1 = box
    sx, sy = w / (x1 - x0), h / (y1 - y0)
    stx, sty = nice(x1 - x0), nice(y1 - y0)
    o = [r'\begin{tikzpicture}[x=%.4fcm,y=%.4fcm,baseline=(current bounding box.center)]' % (sx, sy)]
    o.append(r'\draw[muted!25,very thin,xstep=%g,ystep=%g] (%g,%g) grid (%g,%g);' % (stx, sty, x0, y0, x1, y1))
    if y0 <= 0 <= y1: o.append(r'\draw[-latex,muted] (%g,0)--(%g,0);' % (x0, x1 + 0.3 / sx))
    if x0 <= 0 <= x1: o.append(r'\draw[-latex,muted] (0,%g)--(0,%g);' % (y0, y1 + 0.3 / sy))
    ay = 0 if y0 <= 0 <= y1 else y0
    ax = 0 if x0 <= 0 <= x1 else x0
    k = math.ceil(x0 / stx)
    while k * stx <= x1 + 1e-9:
        t = k * stx
        if abs(t) > 1e-9 and t < x1 - 1e-9: o.append(r'\node[below,font=\tiny,text=muted,inner sep=1.5pt] at (%g,%g) {$%s$};' % (t, ay, fnum(t)))
        k += 1
    k = math.ceil(y0 / sty)
    while k * sty <= y1 + 1e-9:
        t = k * sty
        if abs(t) > 1e-9 and t < y1 - 1e-9: o.append(r'\node[left,font=\tiny,text=muted,inner sep=1.5pt] at (%g,%g) {$%s$};' % (ax, t, fnum(t)))
        k += 1
    o.append(r'\begin{scope}\clip (%g,%g) rectangle (%g,%g);' % (x0, y0, x1, y1))
    for f, g, a, b, key in fills:
        N = 120
        top = ['(%.3f,%.3f)' % (a + (b - a) * i / N, f(a + (b - a) * i / N)) for i in range(N + 1)]
        bot = ['(%.3f,%.3f)' % (a + (b - a) * i / N, g(a + (b - a) * i / N) if g else 0) for i in range(N, -1, -1)]
        o.append(r'\fill[%s,opacity=.28] ' % FILL[key] + '--'.join(top + bot) + '--cycle;')
    for a in va: o.append(r'\draw[navy,dashed] (%g,%g)--(%g,%g);' % (a, y0, a, y1))
    for c in curves:
        f, a, b, col = (c, x0, x1, 'accent') if callable(c) else c
        a, b = max(a, x0), min(b, x1)
        N, seg = 240, []
        for i in range(N + 1):
            x = a + (b - a) * i / N
            y = f(x)
            if y < y0 - 2 * (y1 - y0) or y > y1 + 2 * (y1 - y0):
                if len(seg) > 1: o.append(r'\draw[%s,line width=1.3pt,line join=round] ' % col + '--'.join(seg) + ';')
                seg = []; continue
            seg.append('(%.3f,%.3f)' % (x, y))
        if len(seg) > 1: o.append(r'\draw[%s,line width=1.3pt,line join=round] ' % col + '--'.join(seg) + ';')
    o.append(r'\end{scope}')
    for x, y in pts: o.append(r'\fill[navy] (%g,%g) circle (1.8pt);' % (x, y))
    for x, y, t, pos in labs: o.append(r'\node[%s,font=\scriptsize,fill=white,fill opacity=.8,text opacity=1,inner sep=1pt] at (%g,%g) {$%s$};' % (pos, x, y, t))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'
def minis(gs):
    """gràfiques petites amb la lletra de l'apartat, tres per fila"""
    cells = [r'\begin{tabular}{@{}c@{}}\small\bfseries\color{navy}%s)\\%s\end{tabular}' % (chr(97 + i), g) for i, g in enumerate(gs)]
    rows = [' & '.join(cells[i:i + 3]) for i in range(0, len(cells), 3)]
    return '\n\n\\begin{center}\\begin{tabular}{@{}ccc@{}}' + r'\\[4pt]'.join(rows) + '\\end{tabular}\\end{center}\n'
def gA(f, g=None, a=None, b=None, box=None, w=4.6, h=3.4):
    """gràfica d'un recinte: ombreja cada tros (verd si f > g, roig si f < g; turquesa entre dues corbes)"""
    hq = f - g if g else f
    rs = [float(r) for r in hq.roots()]
    xs = rs if a is None else [a] + [r for r in rs if a < r < b] + [b]
    fills = []
    for p, q in zip(xs, xs[1:]):
        key = '=' if g else ('+' if hq((p + q) / 2) > 0 else '-')
        fills.append((f, g, p, q, key))
    curves = [(f, -1e9, 1e9, 'accent')] + ([(g, -1e9, 1e9, 'navy')] if g else [])
    if box is None:
        lo, hi = min(xs), max(xs); pad = max(0.6, (hi - lo) * 0.2)
        x0, x1 = lo - pad, hi + pad
        ys = [fn(x0 + (x1 - x0) * i / 100) for i in range(101) for fn in ([f, g] if g else [f])] + [0]
        yl, yh = min(ys), max(ys); m = (yh - yl) * 0.08 + 0.2
        box = (x0, x1, yl - m, yh + m)
    return graf(curves, box, fills=fills, va=[] if a is None else [a, b], w=w, h=h)

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Primitivas e integral indefinida", [
 (1, r"Comprueba, derivando, si $F$ es una primitiva de $f$ en cada caso:" + tasks(2, [r"$F(x)=x^3-5x+2$, \ $f(x)=3x^2-5$", r"$F(x)=(x^2-1)^2$, \ $f(x)=4x^3-4x$",
      r"$F(x)=\dfrac{x^2}{2}+\dfrac1x$, \ $f(x)=x+\dfrac{1}{x^2}$", r"$F(x)=\dfrac{(2x+3)^3}{6}$, \ $f(x)=(2x+3)^2$"])
     + recorda(r"$F$ es una primitiva de $f$ si $F'(x)=f(x)$."),
     tasks(2, [r"$F'(x)=3x^2-5$: \rest{sí}.", r"$F'(x)=2(x^2-1)\cdot2x=4x^3-4x$: \rest{sí}.",
               r"$F'(x)=x-\frac{1}{x^2}\neq f(x)$: \rest{no}.", r"$F'(x)=\frac{3(2x+3)^2\cdot2}{6}=(2x+3)^2$: \rest{sí}."])),
 (1, r"Escribe tres primitivas diferentes de $f(x)=3x^2-4$. ¿Qué relación hay entre sus gráficas?",
     r"Por ejemplo, $\res{x^3-4x}$, $\res{x^3-4x+1}$ y $\res{x^3-4x-2}$ (en general, $x^3-4x+C$). Las gráficas son \rest{traslaciones verticales} unas de otras."),
 (2, r"Di si las afirmaciones siguientes son verdaderas o falsas. Justifícalo." + tasks(1, [r"Si $F$ y $G$ son dos primitivas de la misma función $f$, entonces $F-G$ es constante.",
      r"$\displaystyle\int f(x)\cdot g(x)\,dx=\int f(x)\,dx\cdot\int g(x)\,dx$.", r"$\displaystyle\int 5f(x)\,dx=5\int f(x)\,dx$."]),
     tasks(1, [r"\rest{Verdadera}: $(F-G)'=f-f=0$, y una función con derivada 0 es constante.",
               r"\rest{Falsa}. Por ejemplo, con $f(x)=g(x)=x$: $\int x^2\,dx=\frac{x^3}{3}+C$, pero $\int x\,dx\cdot\int x\,dx=\frac{x^4}{4}+\dots$",
               r"\rest{Verdadera}: las constantes que multiplican pueden salir fuera de la integral."])),
]))

# =====================================================================
S.append(("Integrales inmediatas", [
 (1, r"Calcula las integrales de polinomios siguientes:" + tasks(3, [I(r'(4x^3-6x^2+2x-5)'), I(r'(x^2+3x-1)'), I(r'(5x^4-x)'), I(r'\left(2-\frac x3\right)'),
      I(r'\left(\frac{x^3}{2}-\frac{2x^2}{3}+1\right)'), I(r'(6x^5+4x^3)'), I(r'7'), I(r'(0{,}5x-1{,}2)'), I(r'(-3x^2+8x)')])
     + recorda(r"Integramos término a término: $\displaystyle\int a\,x^n\,dx=a\,\frac{x^{n+1}}{n+1}+C$ y $\displaystyle\int k\,dx=kx+C$. No olvides la constante $C$."),
     tasks(3, [r"$\res{x^4-2x^3+x^2-5x+C}$", r"$\res{\frac{x^3}{3}+\frac{3x^2}{2}-x+C}$", r"$\res{x^5-\frac{x^2}{2}+C}$", r"$\res{2x-\frac{x^2}{6}+C}$",
               r"$\res{\frac{x^4}{8}-\frac{2x^3}{9}+x+C}$", r"$\res{x^6+x^4+C}$", r"$\res{7x+C}$", r"$\res{0{,}25x^2-1{,}2x+C}$", r"$\res{-x^3+4x^2+C}$"])),
 (1, r"Desarrolla primero y después integra:" + tasks(3, [I(r'x(x+4)'), I(r'(x-3)^2'), I(r'(x+1)(x-1)'), I(r'(2x-1)(x+2)'), I(r'x^2(3x-2)'), I(r'\frac{x^3-2x^2}{x}')])
     + recorda(r"No hay ninguna regla para integrar un producto o un cociente: si son polinomios, primero los desarrollamos (o simplificamos)."),
     tasks(2, [r"$\int(x^2+4x)\,dx=\res{\frac{x^3}{3}+2x^2+C}$", r"$\int(x^2-6x+9)\,dx=\res{\frac{x^3}{3}-3x^2+9x+C}$", r"$\int(x^2-1)\,dx=\res{\frac{x^3}{3}-x+C}$",
               r"$\int(2x^2+3x-2)\,dx=\res{\frac{2x^3}{3}+\frac{3x^2}{2}-2x+C}$", r"$\int(3x^3-2x^2)\,dx=\res{\frac{3x^4}{4}-\frac{2x^3}{3}+C}$", r"$\int(x^2-2x)\,dx=\res{\frac{x^3}{3}-x^2+C}$ \ ($x\neq0$)"])),
 (2, r"Calcula estas integrales inmediatas (escribe las raíces y las fracciones como potencias):" + tasks(2, [I(r'\frac{1}{x^3}'), I(r'\sqrt[3]{x}'), I(r'\left(\frac2x+3e^x\right)'), I(r'\left(x+\frac{1}{\sqrt x}\right)')])
     + recorda(r"$\displaystyle\int x^n\,dx=\frac{x^{n+1}}{n+1}+C$ también vale para $n$ negativo o fraccionario (si $n\neq-1$). Además, $\displaystyle\int\frac1x\,dx=\ln|x|+C$ y $\displaystyle\int e^x\,dx=e^x+C$."),
     tasks(2, [r"$\int x^{-3}\,dx=\frac{x^{-2}}{-2}=\res{-\frac{1}{2x^2}+C}$", r"$\int x^{1/3}\,dx=\res{\frac34\sqrt[3]{x^4}+C}$", r"$\res{2\ln|x|+3e^x+C}$", r"$\frac{x^2}{2}+\frac{x^{1/2}}{1/2}=\res{\frac{x^2}{2}+2\sqrt x+C}$"])),
]))

# =====================================================================
S.append(("Integrales casi inmediatas", [
 (2, r"Calcula las integrales siguientes ajustando constantes:" + tasks(2, [I(r'(5x+2)^3'), I(r'3x^2(x^3-1)^4'), I(r'x(x^2+5)^2'), I(r'\frac{4x+2}{x^2+x+1}'),
      I(r'\frac{1}{2x-5}'), I(r'e^{-2x}'), I(r'(2x+1)\,e^{x^2+x}'), I(r'x^3e^{x^4}')])
     + recorda(r"$\displaystyle\int u'\,u^n\,dx=\frac{u^{n+1}}{n+1}+C$, \ $\displaystyle\int\frac{u'}{u}\,dx=\ln|u|+C$, \ $\displaystyle\int u'\,e^{u}\,dx=e^{u}+C$. Si falta un factor constante, multiplicamos y dividimos por él."),
     tasks(2, [r"$\frac15\int5(5x+2)^3\,dx=\res{\frac{(5x+2)^4}{20}+C}$", r"$\res{\frac{(x^3-1)^5}{5}+C}$", r"$\frac12\int2x(x^2+5)^2\,dx=\res{\frac{(x^2+5)^3}{6}+C}$",
               r"$2\int\frac{2x+1}{x^2+x+1}\,dx=\res{2\ln(x^2+x+1)+C}$", r"$\res{\frac12\ln|2x-5|+C}$", r"$\res{-\frac{e^{-2x}}{2}+C}$", r"$\res{e^{x^2+x}+C}$", r"$\res{\frac{e^{x^4}}{4}+C}$"])),
 (2, r"Calcula $\displaystyle\int(x+2)^2\,dx$ de dos maneras: como integral casi inmediata y desarrollando el cuadrado. ¿Sale el mismo resultado? Explícalo.",
     r"Casi inmediata: $\res{\frac{(x+2)^3}{3}+C}$. Desarrollando: $\int(x^2+4x+4)\,dx=\res{\frac{x^3}{3}+2x^2+4x+C}$. Como $\frac{(x+2)^3}{3}=\frac{x^3}{3}+2x^2+4x+\frac83$, "
     r"las dos primitivas \rest{solo se diferencian en una constante}: ambas son correctas."),
]))

# =====================================================================
S.append(("Primitivas que cumplen una condición", [
 (1, r"Halla la primitiva de $f(x)=6x^2-4x+1$ que cumple $F(1)=3$.",
     r"$F(x)=2x^3-2x^2+x+C$; \ $F(1)=1+C=3\Rightarrow C=2$. \ $\res{F(x)=2x^3-2x^2+x+2}$"),
 (1, r"Halla la primitiva de $f(x)=x^2-1$ cuya gráfica pasa por el punto $(3,\,4)$.",
     r"$F(x)=\frac{x^3}{3}-x+C$; \ $F(3)=9-3+C=4\Rightarrow C=-2$. \ $\res{F(x)=\frac{x^3}{3}-x-2}$"),
 (2, r"La pendiente de la recta tangente a la gráfica de una función $f$ en cada punto $x$ es $3x^2-2x$, y la gráfica pasa por el punto $(1,\,2)$. Halla $f$.",
     r"$f'(x)=3x^2-2x\Rightarrow f(x)=x^3-x^2+C$; \ $f(1)=C=2$. \ $\res{f(x)=x^3-x^2+2}$"),
 (2, r"De una función $f$ sabemos que $f''(x)=6x-2$, que $f'(1)=3$ y que $f(0)=1$. Halla $f$.",
     r"$f'(x)=3x^2-2x+C_1$, \ $f'(1)=1+C_1=3\Rightarrow C_1=2$. \ $f(x)=x^3-x^2+2x+C_2$, \ $f(0)=C_2=1$. \ $\res{f(x)=x^3-x^2+2x+1}$"),
 (2, r"El coste marginal de fabricar $x$ unidades de un producto es $C'(x)=0{,}6x+20$ euros por unidad, y los costes fijos son de 500 €." + tasks(1, [r"Halla la función de coste total $C(x)$.", r"¿Cuánto cuesta fabricar 50 unidades?"])
     + recorda(r"El coste total es una primitiva del coste marginal. Los costes fijos son el coste cuando no se fabrica nada: $C(0)$."),
     tasks(1, [r"$C(x)=0{,}3x^2+20x+K$, con $C(0)=K=500$: $\res{C(x)=0{,}3x^2+20x+500}$", r"$C(50)=750+1000+500=\res{2\,250}$ €."])),
 (2, r"La velocidad de crecimiento de una población, en miles de habitantes por año, es $P'(t)=0{,}3t^2+2t$, donde $t$ son los años transcurridos desde el año 2020. En 2020 la población era de 50 mil habitantes." + tasks(1, [r"Halla la función $P(t)$ que da la población.", r"¿Qué población habrá en 2025?"]),
     tasks(1, [r"$P(t)=0{,}1t^3+t^2+K$, con $P(0)=50$: $\res{P(t)=0{,}1t^3+t^2+50}$", r"$P(5)=12{,}5+25+50=\res{87{,}5}$ miles de habitantes."])),
]))

# =====================================================================
G_RIEM = graf([lambda x: x * x], (-0.3, 2.3, -0.4, 4.4), fills=[(lambda x, k=k: (0.5 * k) ** 2, None, 0.5 * (k - 1), 0.5 * k, '=') for k in range(1, 5)], w=4.4, h=3.4)
S.append(("La integral definida. Regla de Barrow", [
 (1, r"Calcula estas integrales definidas haciendo un dibujo y usando áreas de figuras conocidas:" + tasks(4, [I('4', 0, 5), I('(x+2)', -2, 2), I('(-2x)', 0, 3), I('x', -1, 3)])
     + recorda(r"Si $f\geq0$, $\int_a^b f$ es el área; las partes por debajo del eje cuentan con signo negativo."),
     tasks(2, [r"Rectángulo $5\times4$: $\res{20}$", r"Triángulo de base 4 y altura 4: $\res{8}$", r"Triángulo por debajo del eje, de área 9: $\res{-9}$", r"$\frac92-\frac12=\res{4}$"])),
 (1, r"Calcula aplicando la regla de Barrow:" + tasks(3, [I('(x^2+1)', 0, 3), I('(6x^2-2x)', 1, 2), I('(3x^2-2x+1)', -1, 2), I('(x^3+2x)', -2, 0), I('(x^4-x)', 0, 1),
      I(r'\left(2-\frac x2\right)', 1, 4), I('(x^5-x^3+4)', -1, 1), I('(x-1)(x+3)', 0, 2), I('(x+1)^2', 1, 2)])
     + recorda(r"$\displaystyle\int_a^b f(x)\,dx=\Big[F(x)\Big]_a^b=F(b)-F(a)$. Cuidado con los paréntesis cuando $F(a)$ es negativo."),
     tasks(2, [r"$\Big[\frac{x^3}{3}+x\Big]_0^3=\res{12}$", r"$\Big[2x^3-x^2\Big]_1^2=12-1=\res{11}$", r"$\Big[x^3-x^2+x\Big]_{-1}^{2}=6-(-3)=\res{9}$",
               r"$\Big[\frac{x^4}{4}+x^2\Big]_{-2}^{0}=0-8=\res{-8}$", r"$\Big[\frac{x^5}{5}-\frac{x^2}{2}\Big]_0^1=\res{-\frac{3}{10}}$", r"$\Big[2x-\frac{x^2}{4}\Big]_1^4=4-\frac74=\res{\frac94}$",
               r"$\Big[\frac{x^6}{6}-\frac{x^4}{4}+4x\Big]_{-1}^{1}=\res{8}$", r"$\Big[\frac{x^3}{3}+x^2-3x\Big]_0^2=\res{\frac23}$", r"$\Big[\frac{(x+1)^3}{3}\Big]_1^2=\frac{27-8}{3}=\res{\frac{19}{3}}$"])),
 (2, r"Calcula:" + tasks(4, [I(r'\frac2x', 1, 'e'), I(r'e^x', 0, r'\ln2'), I(r'\frac{1}{\sqrt x}', 1, 4), I(r'\frac{1}{x^2}', 1, 2)]),
     tasks(2, [r"$\Big[2\ln x\Big]_1^e=\res{2}$", r"$\Big[e^x\Big]_0^{\ln2}=2-1=\res{1}$", r"$\Big[2\sqrt x\Big]_1^4=4-2=\res{2}$", r"$\Big[-\frac1x\Big]_1^2=-\frac12+1=\res{\frac12}$"])),
 (1, r"Sabemos que $\displaystyle\int_0^3 f(x)\,dx=4$, $\displaystyle\int_3^5 f(x)\,dx=-1$ y $\displaystyle\int_0^5 g(x)\,dx=2$. Calcula:" + tasks(3, [I('f(x)', 0, 5), I(r'\big(2f(x)-g(x)\big)', 5, 0), I('f(x)', 3, 3)]),
     tasks(3, [r"$4+(-1)=\res{3}$", r"$-(2\cdot3-2)=\res{-4}$", r"$\res{0}$"])),
 (2, r"Calcula el valor de $a>0$ para que $\displaystyle\int_0^a(2x+1)\,dx=6$.",
     r"$\Big[x^2+x\Big]_0^a=a^2+a=6\Rightarrow a^2+a-6=0\Rightarrow a=2$ o $a=-3$. Como $a>0$: $\res{a=2}$."),
 (2, r"Calcula $k$ para que $\displaystyle\int_1^3(kx-1)\,dx=10$.",
     r"$\Big[\frac{kx^2}{2}-x\Big]_1^3=\left(\frac{9k}{2}-3\right)-\left(\frac k2-1\right)=4k-2=10\Rightarrow\res{k=3}$."),
 (3, r"Halla $a$ y $b$ para que la función $f(x)=ax^2+b$ cumpla $f(1)=2$ y $\displaystyle\int_0^1 f(x)\,dx=1$.",
     r"$f(1)=a+b=2$ y $\int_0^1(ax^2+b)\,dx=\frac a3+b=1$. Restando: $\frac{2a}{3}=1\Rightarrow\res{a=\frac32,\ b=\frac12}$."),
 (2, r"Aproxima $\displaystyle\int_0^2x^2\,dx$ con 4 rectángulos de la misma anchura, tomando como altura el valor de la función en el extremo derecho de cada trozo. Compáralo con el valor exacto.",
     r"$\Delta x=0{,}5$: $S_4=0{,}5\,(0{,}25+1+2{,}25+4)=\res{3{,}75}$. Valor exacto: $\Big[\frac{x^3}{3}\Big]_0^2=\res{\frac83}\approx2{,}667$. La aproximación es por exceso (la función es creciente)." + cen(G_RIEM)),
]))

# =====================================================================
A24 = [(Q(1, 0, -9),), (Q(-1, 2, 3),), (Q(1, -5, 4),), (Q(1, 0, -9, 0),), (Q(1, -3, 2, 0),), (Q(1, 0, -1, 0, 0),)]
A25 = [(Q(1, 0, 1), 0, 3), (Q(-1, 0, 4), 0, 3), (Q(1, -4, 0), -1, 1), (Q(1, 0, -1, 0), 0, 2), (Q(1, -2, -3), 0, 4), (Q(2, -4), 0, 5)]
S.append(("Área entre una curva y el eje OX", [
 (2, r"Calcula el área del recinto limitado por la gráfica de cada función y el eje OX. Haz un esbozo." + tasks(3, [r"$f(x)=x^2-9$", r"$f(x)=-x^2+2x+3$", r"$f(x)=x^2-5x+4$", r"$f(x)=x^3-9x$", r"$f(x)=x^3-3x^2+2x$", r"$f(x)=x^4-x^2$"])
     + recorda(r"Primero buscamos los cortes con el eje OX ($f(x)=0$); son los límites de integración. Si hay más de dos, integramos cada trozo por separado y sumamos los valores absolutos."),
     tasks(1, [r"Cortes $\pm3$: $\int_{-3}^{3}(x^2-9)\,dx=\Big[\frac{x^3}{3}-9x\Big]_{-3}^{3}=-18-18=-36\Rightarrow\res{A=36\ \text{u}^2}$",
               r"Cortes $-1$ y $3$: $\Big[-\frac{x^3}{3}+x^2+3x\Big]_{-1}^{3}=9-\left(-\frac53\right)\Rightarrow\res{A=\frac{32}{3}\ \text{u}^2}$",
               r"Cortes $1$ y $4$: $\Big[\frac{x^3}{3}-\frac{5x^2}{2}+4x\Big]_{1}^{4}=-\frac83-\frac{11}{6}=-\frac92\Rightarrow\res{A=\frac92\ \text{u}^2}$",
               r"Cortes $-3,0,3$: $F(x)=\frac{x^4}{4}-\frac{9x^2}{2}$; $\int_{-3}^{0}f=\frac{81}{4}$, $\int_0^3f=-\frac{81}{4}\Rightarrow\res{A=\frac{81}{2}\ \text{u}^2}$",
               r"$x(x-1)(x-2)=0$; $F(x)=\frac{x^4}{4}-x^3+x^2$: $\int_0^1f=\frac14$, $\int_1^2f=-\frac14\Rightarrow\res{A=\frac12\ \text{u}^2}$",
               r"$x^2(x^2-1)=0$: cortes $-1$, $0$ (doble) y $1$; $f\leq0$ en $[-1,1]$: $\int_{-1}^{1}(x^4-x^2)\,dx=\frac25-\frac23=-\frac{4}{15}\Rightarrow\res{A=\frac{4}{15}\ \text{u}^2}$"])
     + minis([gA(*q, w=4.2, h=3) for q in A24])),
 (2, r"Calcula el área de la región limitada por la gráfica de $f$, el eje OX y las rectas indicadas:" + tasks(2, [r"$f(x)=x^2+1$, \ $x=0$, \ $x=3$", r"$f(x)=4-x^2$, \ $x=0$, \ $x=3$",
      r"$f(x)=x^2-4x$, \ $x=-1$, \ $x=1$", r"$f(x)=x^3-x$, \ $x=0$, \ $x=2$", r"$f(x)=x^2-2x-3$, \ $x=0$, \ $x=4$", r"$f(x)=2x-4$, \ $x=0$, \ $x=5$"])
     + recorda(r"Ahora los límites son $a$ y $b$, pero debemos mirar si $f$ corta el eje OX \textbf{dentro} del intervalo: esos cortes dividen la integral en trozos. Los cortes de fuera no cuentan."),
     tasks(1, [r"No corta el eje: $\Big[\frac{x^3}{3}+x\Big]_0^3=\res{12\ \text{u}^2}$",
               r"Corte en $x=2$: $\int_0^2f=\frac{16}{3}$, $\int_2^3f=3-\frac{16}{3}=-\frac73\Rightarrow\res{A=\frac{23}{3}\ \text{u}^2}$",
               r"Cortes $0$ y $4$; dentro solo el $0$: $\int_{-1}^{0}f=\frac73$, $\int_0^1f=-\frac53\Rightarrow\res{A=4\ \text{u}^2}$",
               r"Cortes $-1,0,1$; dentro solo el $1$: $\int_0^1f=-\frac14$, $\int_1^2f=\frac94\Rightarrow\res{A=\frac52\ \text{u}^2}$",
               r"Cortes $-1$ y $3$; dentro el $3$: $\int_0^3f=-9$, $\int_3^4f=\frac73\Rightarrow\res{A=\frac{34}{3}\ \text{u}^2}$",
               r"Corte en $x=2$: $\int_0^2f=-4$, $\int_2^5f=9\Rightarrow\res{A=13\ \text{u}^2}$ (dos triángulos)"])
     + minis([gA(q[0], None, q[1], q[2], w=4.2, h=3) for q in A25])),
 (1, r"Un alumno dice que el área limitada por $f(x)=x^3$, el eje OX y las rectas $x=-2$ y $x=2$ es 0, porque $\displaystyle\int_{-2}^{2}x^3\,dx=0$. ¿Tiene razón? Calcula el área correctamente.",
     r"\rest{No}: la integral vale 0 porque la parte de abajo ($x<0$) se compensa con la de arriba. $\int_{-2}^{0}x^3\,dx=-4$ y $\int_0^2x^3\,dx=4$, así que $\res{A=4+4=8\ \text{u}^2}$."
     + cen(gA(Q(1, 0, 0, 0), None, -2, 2))),
 (2, r"Considera la función $f(x)=x^2-4x+3$." + tasks(1, [r"Represéntala gráficamente.", r"Calcula el área del recinto limitado por la gráfica de $f$ y el eje OX.", r"Calcula el área del recinto limitado por la gráfica de $f$ y los dos ejes de coordenadas."]),
     tasks(1, [r"Parábola hacia arriba, vértice $(2,\,-1)$, cortes $(1,\,0)$, $(3,\,0)$ y $(0,\,3)$.", r"$\int_1^3(x^2-4x+3)\,dx=\Big[\frac{x^3}{3}-2x^2+3x\Big]_1^3=0-\frac43\Rightarrow\res{A=\frac43\ \text{u}^2}$",
               r"Entre $x=0$ y el primer corte, $x=1$: $\int_0^1f=\res{\frac43\ \text{u}^2}$"])
     + cen(gA(Q(1, -4, 3)), gA(Q(1, -4, 3), None, 0, 1, box=(-0.6, 4.4, -1.6, 3.6)))),
 (3, r"Calcula $a>0$ para que el área del recinto limitado por la parábola $f(x)=a^2-x^2$ y el eje OX sea 36.",
     r"Cortes $\pm a$: $\int_{-a}^{a}(a^2-x^2)\,dx=\Big[a^2x-\frac{x^3}{3}\Big]_{-a}^{a}=\frac{4a^3}{3}=36\Rightarrow a^3=27\Rightarrow\res{a=3}$."),
 (2, r"Calcula $k>0$ para que el área de la región limitada por $f(x)=x^2$, el eje OX y la recta $x=k$ sea 9.",
     r"$\int_0^k x^2\,dx=\frac{k^3}{3}=9\Rightarrow k^3=27\Rightarrow\res{k=3}$."),
]))

# =====================================================================
A30 = [(Q(1, 0, 0), Q(2, 0)), (Q(1, 0, -2), Q(1, 0)), (Q(-1, 6, 0), Q(1, -2, 0)), (Q(1, 0, 0, 0), Q(1, 0, 0)), (Q(1, 0, -2, 0), Q(2, 0)), (Q(-1, 0, 4), Q(1, 0, -4))]
A31 = [(Q(1, 0, 1), Q(-1, 0, -1), -1, 2), (Q(1, 0, 0), Q(1, 0), -1, 1), (Q(1, 0, -4), Q(-1, 2), 0, 3), (Q(1, 0, 0, 0), Q(1, 0), 0, 2)]
S.append(("Área entre dos curvas", [
 (2, r"Calcula el área del recinto cerrado por las gráficas de las funciones:" + tasks(2, [r"$f(x)=x^2$ \ y \ $g(x)=2x$", r"$f(x)=x^2-2$ \ y \ $g(x)=x$", r"$f(x)=-x^2+6x$ \ y \ $g(x)=x^2-2x$",
      r"$f(x)=x^3$ \ y \ $g(x)=x^2$", r"$f(x)=x^3-2x$ \ y \ $g(x)=2x$", r"$f(x)=4-x^2$ \ y \ $g(x)=x^2-4$"])
     + recorda(r"Resolvemos $f(x)=g(x)$ para hallar los puntos de corte, que son los límites. Integramos $f-g$ en cada trozo y sumamos los valores absolutos (o integramos «la de arriba menos la de abajo»)."),
     tasks(1, [r"Cortes $0$ y $2$: $\int_0^2(2x-x^2)\,dx=4-\frac83\Rightarrow\res{A=\frac43\ \text{u}^2}$",
               r"$x^2-x-2=0\Rightarrow-1,\ 2$: $\int_{-1}^{2}(x+2-x^2)\,dx\Rightarrow\res{A=\frac92\ \text{u}^2}$",
               r"$2x^2-8x=0\Rightarrow0,\ 4$: $\int_0^4(-2x^2+8x)\,dx=-\frac{128}{3}+64\Rightarrow\res{A=\frac{64}{3}\ \text{u}^2}$",
               r"$x^2(x-1)=0\Rightarrow0,\ 1$: $\int_0^1(x^2-x^3)\,dx=\frac13-\frac14\Rightarrow\res{A=\frac{1}{12}\ \text{u}^2}$",
               r"$x^3-4x=0\Rightarrow-2,0,2$: $\int_{-2}^{0}(x^3-4x)\,dx=4$, $\int_0^2(x^3-4x)\,dx=-4\Rightarrow\res{A=8\ \text{u}^2}$",
               r"$2x^2-8=0\Rightarrow\pm2$: $\int_{-2}^{2}(8-2x^2)\,dx=32-\frac{32}{3}\Rightarrow\res{A=\frac{64}{3}\ \text{u}^2}$"])
     + minis([gA(f, g, w=4.2, h=3) for f, g in A30])),
 (2, r"Calcula el área de la región limitada por las gráficas de $f$ y $g$ y las rectas indicadas:" + tasks(2, [r"$f(x)=x^2+1$, \ $g(x)=-x^2-1$, \ $x=-1$, \ $x=2$", r"$f(x)=x^2$, \ $g(x)=x$, \ $x=-1$, \ $x=1$",
      r"$f(x)=x^2-4$, \ $g(x)=-x+2$, \ $x=0$, \ $x=3$", r"$f(x)=x^3$, \ $g(x)=x$, \ $x=0$, \ $x=2$"]),
     tasks(1, [r"No se cortan ($2x^2+2>0$): $\int_{-1}^{2}(2x^2+2)\,dx=\Big[\frac{2x^3}{3}+2x\Big]_{-1}^{2}=\frac{28}{3}+\frac83\Rightarrow\res{A=12\ \text{u}^2}$",
               r"Cortes $0$ y $1$; dentro de $(-1,\,1)$ solo el $0$: $\int_{-1}^{0}(x^2-x)\,dx=\frac56$, $\int_0^1(x^2-x)\,dx=-\frac16\Rightarrow\res{A=1\ \text{u}^2}$",
               r"$x^2+x-6=0\Rightarrow-3,\ 2$; dentro el $2$: $\int_0^2(x^2+x-6)\,dx=-\frac{22}{3}$, $\int_2^3(\dots)\,dx=\frac{17}{6}\Rightarrow\res{A=\frac{61}{6}\ \text{u}^2}$",
               r"Cortes $-1,0,1$; dentro el $1$: $\int_0^1(x^3-x)\,dx=-\frac14$, $\int_1^2(x^3-x)\,dx=\frac94\Rightarrow\res{A=\frac52\ \text{u}^2}$"])
     + minis([gA(f, g, a, b, w=4.2, h=3) for f, g, a, b in A31])),
 (3, r"Calcula el área de la región limitada por la parábola $y=x^2$, la recta tangente a la parábola en $x=1$ y el eje OY.",
     r"Tangente: $y-1=2(x-1)\Rightarrow y=2x-1$. La parábola queda por encima: $x^2-(2x-1)=(x-1)^2\geq0$. Entre $x=0$ (eje OY) y $x=1$: $\int_0^1(x-1)^2\,dx=\Big[\frac{(x-1)^3}{3}\Big]_0^1=\res{\frac13\ \text{u}^2}$."
     + cen(gA(Q(1, 0, 0), Q(2, -1), 0, 1, box=(-0.8, 2.2, -1.6, 3.4)))),
 (2, r"Considera las funciones $f(x)=-x^2+5x$ y $g(x)=x$." + tasks(1, [r"Represéntalas en los mismos ejes.", r"Calcula el área del recinto cerrado por las dos gráficas."]),
     tasks(1, [r"Parábola hacia abajo con vértice $\left(\frac52,\frac{25}{4}\right)$ y cortes $(0,\,0)$ y $(5,\,0)$; recta bisectriz.",
               r"$-x^2+5x=x\Rightarrow x=0,\ 4$: $\int_0^4(-x^2+4x)\,dx=-\frac{64}{3}+32\Rightarrow\res{A=\frac{32}{3}\ \text{u}^2}$"])
     + cen(gA(Q(-1, 5, 0), Q(1, 0)))),
 (3, r"Calcula $m>0$ para que el área del recinto limitado por la parábola $y=x^2$ y la recta $y=mx$ sea 36.",
     r"Cortes $x=0$ y $x=m$: $\int_0^m(mx-x^2)\,dx=\frac{m^3}{2}-\frac{m^3}{3}=\frac{m^3}{6}=36\Rightarrow m^3=216\Rightarrow\res{m=6}$."),
]))

# =====================================================================
S.append(("Problemas de aplicación", [
 (2, r"La función de demanda de un producto es $p(x)=100-x^2$, donde $p$ es el precio (en euros) y $x$ la cantidad demandada (en miles de unidades). El precio de mercado es de 64 €." + tasks(1, [r"¿Qué cantidad se demanda a este precio?",
      r"El \textbf{excedente del consumidor} es el área comprendida entre la curva de demanda y la recta $p=64$, desde $x=0$ hasta la cantidad demandada. Calcúlalo."]),
     tasks(1, [r"$100-x^2=64\Rightarrow x^2=36\Rightarrow\res{x=6}$ miles de unidades.", r"$\int_0^6(100-x^2-64)\,dx=\Big[36x-\frac{x^3}{3}\Big]_0^6=216-72=\res{144}$ miles de euros."])
     + cen(gA(Q(-1, 0, 100), Q(64), 0, 6, box=(-0.8, 10.5, -8, 112)))),
 (2, r"El beneficio marginal de una empresa (en miles de euros) cuando vende $x$ toneladas es $B'(x)=40-2x$. Si no vende nada, tiene unas pérdidas de 100 mil euros." + tasks(1, [r"Halla la función de beneficio $B(x)$.", r"¿Cuántas toneladas debe vender para obtener el beneficio máximo? ¿Cuál es ese beneficio?", r"¿Cuánto aumenta el beneficio si pasa de vender 5 toneladas a vender 10? (Calcúlalo con una integral definida.)"]),
     tasks(1, [r"$B(x)=40x-x^2+K$, con $B(0)=-100$: $\res{B(x)=-x^2+40x-100}$", r"$B'(x)=0\Rightarrow x=20$ ($B''=-2<0$): $\res{20}$ toneladas y $B(20)=\res{300}$ mil euros.",
               r"$\int_5^{10}(40-2x)\,dx=\Big[40x-x^2\Big]_5^{10}=300-175=\res{125}$ mil euros."])),
 (3, r"Un pozo de petróleo produce, $t$ años después de abrirlo, a un ritmo de $r(t)=12-\frac{3}{4}t^2$ miles de barriles por año." + tasks(1, [r"¿Cuándo dejará de producir?", r"¿Cuántos barriles producirá en total, desde que se abre hasta que se cierra?"]),
     tasks(1, [r"$12-\frac34t^2=0\Rightarrow t^2=16\Rightarrow\res{t=4}$ años.", r"$\int_0^4\left(12-\frac34t^2\right)dt=\Big[12t-\frac{t^3}{4}\Big]_0^4=48-16=\res{32}$ miles de barriles."])),
]))

# ---------- comprovacions exactes ----------
F_ = Fr
CHK = [
 # immediates (derivem la primitiva i comparem coeficients)
 (Q(1, -2, 1, -5, 0).deriv().c, Q(4, -6, 2, -5).c), (Q(F_(1, 3), F_(3, 2), -1, 0).deriv().c, Q(1, 3, -1).c), (Q(F_(1, 8), F_(-2, 9), 0, 1, 0).deriv().c, Q(F_(1, 2), F_(-2, 3), 0, 1).c),
 (Q(F_(2, 3), F_(3, 2), -2, 0).deriv().c, Q(2, 3, -2).c), (Q(F_(3, 4), F_(-2, 3), 0, 0, 0).deriv().c, Q(3, -2, 0, 0).c), (Q(F_(1, 3), -3, 9, 0).deriv().c, Q(1, -6, 9).c),
 # condicions
 (Q(2, -2, 1, 2)(1), 3), (Q(F_(1, 3), 0, -1, -2)(3), 4), (Q(1, -1, 0, 2)(1), 2), (Q(1, -1, 2, 1).deriv()(1), 3), (Q(1, -1, 2, 1).deriv().deriv().c, Q(6, -2).c), (Q(1, -1, 2, 1)(0), 1),
 (Q(F_(3, 10), 20, 500)(50), 2250), (Q(F_(1, 10), 1, 0, 50)(5), F_(175, 2)), (Q(F_(1, 10), 1, 0, 50).deriv().c, Q(F_(3, 10), 2, 0).c),
 # Barrow
 (integ(Q(1, 0, 1), 0, 3), 12), (integ(Q(6, -2, 0), 1, 2), 11), (integ(Q(3, -2, 1), -1, 2), 9), (integ(Q(1, 0, 2, 0), -2, 0), -8), (integ(Q(1, 0, 0, -1, 0), 0, 1), F_(-3, 10)),
 (integ(Q(F_(-1, 2), 2), 1, 4), F_(9, 4)), (integ(Q(1, 0, -1, 0, 0, 0), -1, 1) + 8, 8), (integ(Q(1, 2, -3), 0, 2), F_(2, 3)), (integ(Q(1, 2, 1), 1, 2), F_(19, 3)),
 (integ(Q(1, 2), -2, 2), 8), (integ(Q(-2, 0), 0, 3), -9), (integ(Q(1, 0), -1, 3), 4), (integ(Q(2, 1), 0, 2), 6), (integ(Q(3, -1), 1, 3), 10), (integ(Q(F_(3, 2), 0, F_(1, 2)), 0, 1), 1),
 (F_(1, 2) * (F_(1, 4) + 1 + F_(9, 4) + 4), F_(15, 4)), (integ(Q(1, 0, 0), 0, 2), F_(8, 3)),
 # àrees amb l'eix OX
 (area(*A24[0]), 36), (area(*A24[1]), F_(32, 3)), (area(*A24[2]), F_(9, 2)), (area(*A24[3]), F_(81, 2)), (area(*A24[4]), F_(1, 2)), (area(*A24[5]), F_(4, 15)),
 (area(A25[0][0], None, 0, 3), 12), (area(A25[1][0], None, 0, 3), F_(23, 3)), (area(A25[2][0], None, -1, 1), 4), (area(A25[3][0], None, 0, 2), F_(5, 2)),
 (area(A25[4][0], None, 0, 4), F_(34, 3)), (area(A25[5][0], None, 0, 5), 13), (area(Q(1, 0, 0, 0), None, -2, 2), 8), (area(Q(1, -4, 3)), F_(4, 3)), (area(Q(1, -4, 3), None, 0, 1), F_(4, 3)),
 (area(Q(-1, 0, 9)), 36), (area(Q(1, 0, 0), None, 0, 3), 9),
 # àrees entre dues corbes
 (area(*A30[0]), F_(4, 3)), (area(*A30[1]), F_(9, 2)), (area(*A30[2]), F_(64, 3)), (area(*A30[3]), F_(1, 12)), (area(*A30[4]), 8), (area(*A30[5]), F_(64, 3)),
 (area(*A31[0]), 12), (area(*A31[1]), 1), (area(*A31[2]), F_(61, 6)), (area(*A31[3]), F_(5, 2)), (area(Q(1, 0, 0), Q(2, -1), 0, 1), F_(1, 3)), (area(Q(-1, 5, 0), Q(1, 0)), F_(32, 3)),
 (area(Q(1, 0, 0), Q(6, 0)), 36),
 # problemes
 (area(Q(-1, 0, 100), Q(64), 0, 6), 144), (Q(-1, 40, -100)(20), 300), (integ(Q(-2, 40), 5, 10), 125), (integ(Q(F_(-3, 4), 0, 12), 0, 4), 32),
]
for l, r in CHK: assert l == (r if isinstance(r, list) else Fr(r)), (l, r)

# =====================================================================
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

TIT = "Integrales"
KW = "integrales, primitiva, integral indefinida, integrales inmediatas, integral definida, regla de Barrow, áreas, área entre dos curvas"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 8: %s' % (t, TIT), capcalera='%s · Unidad 8: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 8' if sol else 'Ficha de ejercicios · Unidad 8') + '}{\\raggedright ' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. En las gráficas, las zonas verdes son trozos donde la integral es positiva, las rojas donde es negativa y las turquesas, regiones entre dos curvas. Puedes comprobar cualquier resultado con la calculadora de integrales y áreas de los apuntes interactivos de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. En la PAU de Ciencias Sociales las integrales son de polinomios: integra término a término, aplica la regla de Barrow con cuidado con los signos y, en los problemas de áreas, busca siempre primero los puntos de corte y haz un esbozo del recinto. No olvides la constante $C$ en las integrales indefinidas ni las unidades ($\text{u}^2$) en las áreas.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con la calculadora de integrales y áreas de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't8-fitxa-solucions-es.tex' if sol else 't8-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
