# Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 8: Integrals)
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
S.append(("Primitives i integral indefinida", [
 (1, r"Comprova, derivant, si $F$ és una primitiva de $f$ en cada cas:" + tasks(2, [r"$F(x)=x^3-5x+2$, \ $f(x)=3x^2-5$", r"$F(x)=(x^2-1)^2$, \ $f(x)=4x^3-4x$",
      r"$F(x)=\dfrac{x^2}{2}+\dfrac1x$, \ $f(x)=x+\dfrac{1}{x^2}$", r"$F(x)=\dfrac{(2x+3)^3}{6}$, \ $f(x)=(2x+3)^2$"])
     + recorda(r"$F$ és una primitiva de $f$ si $F'(x)=f(x)$."),
     tasks(2, [r"$F'(x)=3x^2-5$: \rest{sí}.", r"$F'(x)=2(x^2-1)\cdot2x=4x^3-4x$: \rest{sí}.",
               r"$F'(x)=x-\frac{1}{x^2}\neq f(x)$: \rest{no}.", r"$F'(x)=\frac{3(2x+3)^2\cdot2}{6}=(2x+3)^2$: \rest{sí}."])),
 (1, r"Escriu tres primitives diferents de $f(x)=3x^2-4$. Quina relació hi ha entre les seues gràfiques?",
     r"Per exemple, $\res{x^3-4x}$, $\res{x^3-4x+1}$ i $\res{x^3-4x-2}$ (en general, $x^3-4x+C$). Les gràfiques són \rest{traslladades verticals} les unes de les altres."),
 (2, r"Digues si les afirmacions següents són vertaderes o falses. Justifica-ho." + tasks(1, [r"Si $F$ i $G$ són dues primitives de la mateixa funció $f$, aleshores $F-G$ és constant.",
      r"$\displaystyle\int f(x)\cdot g(x)\,dx=\int f(x)\,dx\cdot\int g(x)\,dx$.", r"$\displaystyle\int 5f(x)\,dx=5\int f(x)\,dx$."]),
     tasks(1, [r"\rest{Vertadera}: $(F-G)'=f-f=0$, i una funció amb derivada 0 és constant.",
               r"\rest{Falsa}. Per exemple, amb $f(x)=g(x)=x$: $\int x^2\,dx=\frac{x^3}{3}+C$, però $\int x\,dx\cdot\int x\,dx=\frac{x^4}{4}+\dots$",
               r"\rest{Vertadera}: les constants que multipliquen poden eixir fora de la integral."])),
]))

# =====================================================================
S.append(("Integrals immediates", [
 (1, r"Calcula les integrals de polinomis següents:" + tasks(3, [I(r'(4x^3-6x^2+2x-5)'), I(r'(x^2+3x-1)'), I(r'(5x^4-x)'), I(r'\left(2-\frac x3\right)'),
      I(r'\left(\frac{x^3}{2}-\frac{2x^2}{3}+1\right)'), I(r'(6x^5+4x^3)'), I(r'7'), I(r'(0{,}5x-1{,}2)'), I(r'(-3x^2+8x)')])
     + recorda(r"Integrem terme a terme: $\displaystyle\int a\,x^n\,dx=a\,\frac{x^{n+1}}{n+1}+C$ i $\displaystyle\int k\,dx=kx+C$. No oblides la constant $C$."),
     tasks(3, [r"$\res{x^4-2x^3+x^2-5x+C}$", r"$\res{\frac{x^3}{3}+\frac{3x^2}{2}-x+C}$", r"$\res{x^5-\frac{x^2}{2}+C}$", r"$\res{2x-\frac{x^2}{6}+C}$",
               r"$\res{\frac{x^4}{8}-\frac{2x^3}{9}+x+C}$", r"$\res{x^6+x^4+C}$", r"$\res{7x+C}$", r"$\res{0{,}25x^2-1{,}2x+C}$", r"$\res{-x^3+4x^2+C}$"])),
 (1, r"Desenvolupa primer i després integra:" + tasks(3, [I(r'x(x+4)'), I(r'(x-3)^2'), I(r'(x+1)(x-1)'), I(r'(2x-1)(x+2)'), I(r'x^2(3x-2)'), I(r'\frac{x^3-2x^2}{x}')])
     + recorda(r"No hi ha cap regla per a integrar un producte o un quocient: si són polinomis, primer els desenvolupem (o simplifiquem)."),
     tasks(2, [r"$\int(x^2+4x)\,dx=\res{\frac{x^3}{3}+2x^2+C}$", r"$\int(x^2-6x+9)\,dx=\res{\frac{x^3}{3}-3x^2+9x+C}$", r"$\int(x^2-1)\,dx=\res{\frac{x^3}{3}-x+C}$",
               r"$\int(2x^2+3x-2)\,dx=\res{\frac{2x^3}{3}+\frac{3x^2}{2}-2x+C}$", r"$\int(3x^3-2x^2)\,dx=\res{\frac{3x^4}{4}-\frac{2x^3}{3}+C}$", r"$\int(x^2-2x)\,dx=\res{\frac{x^3}{3}-x^2+C}$ \ ($x\neq0$)"])),
 (2, r"Calcula aquestes integrals immediates (escriu les arrels i les fraccions com a potències):" + tasks(2, [I(r'\frac{1}{x^3}'), I(r'\sqrt[3]{x}'), I(r'\left(\frac2x+3e^x\right)'), I(r'\left(x+\frac{1}{\sqrt x}\right)')])
     + recorda(r"$\displaystyle\int x^n\,dx=\frac{x^{n+1}}{n+1}+C$ també val per a $n$ negatiu o fraccionari (si $n\neq-1$). A més, $\displaystyle\int\frac1x\,dx=\ln|x|+C$ i $\displaystyle\int e^x\,dx=e^x+C$."),
     tasks(2, [r"$\int x^{-3}\,dx=\frac{x^{-2}}{-2}=\res{-\frac{1}{2x^2}+C}$", r"$\int x^{1/3}\,dx=\res{\frac34\sqrt[3]{x^4}+C}$", r"$\res{2\ln|x|+3e^x+C}$", r"$\frac{x^2}{2}+\frac{x^{1/2}}{1/2}=\res{\frac{x^2}{2}+2\sqrt x+C}$"])),
]))

# =====================================================================
S.append(("Integrals quasi immediates", [
 (2, r"Calcula les integrals següents ajustant constants:" + tasks(2, [I(r'(5x+2)^3'), I(r'3x^2(x^3-1)^4'), I(r'x(x^2+5)^2'), I(r'\frac{4x+2}{x^2+x+1}'),
      I(r'\frac{1}{2x-5}'), I(r'e^{-2x}'), I(r'(2x+1)\,e^{x^2+x}'), I(r'x^3e^{x^4}')])
     + recorda(r"$\displaystyle\int u'\,u^n\,dx=\frac{u^{n+1}}{n+1}+C$, \ $\displaystyle\int\frac{u'}{u}\,dx=\ln|u|+C$, \ $\displaystyle\int u'\,e^{u}\,dx=e^{u}+C$. Si falta un factor constant, multipliquem i dividim per ell."),
     tasks(2, [r"$\frac15\int5(5x+2)^3\,dx=\res{\frac{(5x+2)^4}{20}+C}$", r"$\res{\frac{(x^3-1)^5}{5}+C}$", r"$\frac12\int2x(x^2+5)^2\,dx=\res{\frac{(x^2+5)^3}{6}+C}$",
               r"$2\int\frac{2x+1}{x^2+x+1}\,dx=\res{2\ln(x^2+x+1)+C}$", r"$\res{\frac12\ln|2x-5|+C}$", r"$\res{-\frac{e^{-2x}}{2}+C}$", r"$\res{e^{x^2+x}+C}$", r"$\res{\frac{e^{x^4}}{4}+C}$"])),
 (2, r"Calcula $\displaystyle\int(x+2)^2\,dx$ de dues maneres: com a integral quasi immediata i desenvolupant el quadrat. Ixen el mateix resultat? Explica-ho.",
     r"Quasi immediata: $\res{\frac{(x+2)^3}{3}+C}$. Desenvolupant: $\int(x^2+4x+4)\,dx=\res{\frac{x^3}{3}+2x^2+4x+C}$. Com que $\frac{(x+2)^3}{3}=\frac{x^3}{3}+2x^2+4x+\frac83$, "
     r"les dues primitives \rest{només es diferencien en una constant}: totes dues són correctes."),
]))

# =====================================================================
S.append(("Primitives que compleixen una condició", [
 (1, r"Troba la primitiva de $f(x)=6x^2-4x+1$ que compleix $F(1)=3$.",
     r"$F(x)=2x^3-2x^2+x+C$; \ $F(1)=1+C=3\Rightarrow C=2$. \ $\res{F(x)=2x^3-2x^2+x+2}$"),
 (1, r"Troba la primitiva de $f(x)=x^2-1$ la gràfica de la qual passa pel punt $(3,\,4)$.",
     r"$F(x)=\frac{x^3}{3}-x+C$; \ $F(3)=9-3+C=4\Rightarrow C=-2$. \ $\res{F(x)=\frac{x^3}{3}-x-2}$"),
 (2, r"El pendent de la recta tangent a la gràfica d'una funció $f$ en cada punt $x$ és $3x^2-2x$, i la gràfica passa pel punt $(1,\,2)$. Troba $f$.",
     r"$f'(x)=3x^2-2x\Rightarrow f(x)=x^3-x^2+C$; \ $f(1)=C=2$. \ $\res{f(x)=x^3-x^2+2}$"),
 (2, r"D'una funció $f$ sabem que $f''(x)=6x-2$, que $f'(1)=3$ i que $f(0)=1$. Troba $f$.",
     r"$f'(x)=3x^2-2x+C_1$, \ $f'(1)=1+C_1=3\Rightarrow C_1=2$. \ $f(x)=x^3-x^2+2x+C_2$, \ $f(0)=C_2=1$. \ $\res{f(x)=x^3-x^2+2x+1}$"),
 (2, r"El cost marginal de fabricar $x$ unitats d'un producte és $C'(x)=0{,}6x+20$ euros per unitat, i els costos fixos són de 500 €." + tasks(1, [r"Troba la funció de cost total $C(x)$.", r"Quant costa fabricar 50 unitats?"])
     + recorda(r"El cost total és una primitiva del cost marginal. Els costos fixos són el cost quan no es fabrica res: $C(0)$."),
     tasks(1, [r"$C(x)=0{,}3x^2+20x+K$, amb $C(0)=K=500$: $\res{C(x)=0{,}3x^2+20x+500}$", r"$C(50)=750+1000+500=\res{2\,250}$ €."])),
 (2, r"La velocitat de creixement d'una població, en milers d'habitants per any, és $P'(t)=0{,}3t^2+2t$, on $t$ són els anys transcorreguts des de l'any 2020. En el 2020 la població era de 50 mil habitants." + tasks(1, [r"Troba la funció $P(t)$ que dona la població.", r"Quina població hi haurà en el 2025?"]),
     tasks(1, [r"$P(t)=0{,}1t^3+t^2+K$, amb $P(0)=50$: $\res{P(t)=0{,}1t^3+t^2+50}$", r"$P(5)=12{,}5+25+50=\res{87{,}5}$ milers d'habitants."])),
]))

# =====================================================================
G_RIEM = graf([lambda x: x * x], (-0.3, 2.3, -0.4, 4.4), fills=[(lambda x, k=k: (0.5 * k) ** 2, None, 0.5 * (k - 1), 0.5 * k, '=') for k in range(1, 5)], w=4.4, h=3.4)
S.append(("La integral definida. Regla de Barrow", [
 (1, r"Calcula aquestes integrals definides fent un dibuix i fent servir àrees de figures conegudes:" + tasks(4, [I('4', 0, 5), I('(x+2)', -2, 2), I('(-2x)', 0, 3), I('x', -1, 3)])
     + recorda(r"Si $f\geq0$, $\int_a^b f$ és l'àrea; les parts per davall de l'eix compten amb signe negatiu."),
     tasks(2, [r"Rectangle $5\times4$: $\res{20}$", r"Triangle de base 4 i altura 4: $\res{8}$", r"Triangle per davall de l'eix, d'àrea 9: $\res{-9}$", r"$\frac92-\frac12=\res{4}$"])),
 (1, r"Calcula aplicant la regla de Barrow:" + tasks(3, [I('(x^2+1)', 0, 3), I('(6x^2-2x)', 1, 2), I('(3x^2-2x+1)', -1, 2), I('(x^3+2x)', -2, 0), I('(x^4-x)', 0, 1),
      I(r'\left(2-\frac x2\right)', 1, 4), I('(x^5-x^3+4)', -1, 1), I('(x-1)(x+3)', 0, 2), I('(x+1)^2', 1, 2)])
     + recorda(r"$\displaystyle\int_a^b f(x)\,dx=\Big[F(x)\Big]_a^b=F(b)-F(a)$. Compte amb els parèntesis quan $F(a)$ és negatiu."),
     tasks(2, [r"$\Big[\frac{x^3}{3}+x\Big]_0^3=\res{12}$", r"$\Big[2x^3-x^2\Big]_1^2=12-1=\res{11}$", r"$\Big[x^3-x^2+x\Big]_{-1}^{2}=6-(-3)=\res{9}$",
               r"$\Big[\frac{x^4}{4}+x^2\Big]_{-2}^{0}=0-8=\res{-8}$", r"$\Big[\frac{x^5}{5}-\frac{x^2}{2}\Big]_0^1=\res{-\frac{3}{10}}$", r"$\Big[2x-\frac{x^2}{4}\Big]_1^4=4-\frac74=\res{\frac94}$",
               r"$\Big[\frac{x^6}{6}-\frac{x^4}{4}+4x\Big]_{-1}^{1}=\res{8}$", r"$\Big[\frac{x^3}{3}+x^2-3x\Big]_0^2=\res{\frac23}$", r"$\Big[\frac{(x+1)^3}{3}\Big]_1^2=\frac{27-8}{3}=\res{\frac{19}{3}}$"])),
 (2, r"Calcula:" + tasks(4, [I(r'\frac2x', 1, 'e'), I(r'e^x', 0, r'\ln2'), I(r'\frac{1}{\sqrt x}', 1, 4), I(r'\frac{1}{x^2}', 1, 2)]),
     tasks(2, [r"$\Big[2\ln x\Big]_1^e=\res{2}$", r"$\Big[e^x\Big]_0^{\ln2}=2-1=\res{1}$", r"$\Big[2\sqrt x\Big]_1^4=4-2=\res{2}$", r"$\Big[-\frac1x\Big]_1^2=-\frac12+1=\res{\frac12}$"])),
 (1, r"Sabem que $\displaystyle\int_0^3 f(x)\,dx=4$, $\displaystyle\int_3^5 f(x)\,dx=-1$ i $\displaystyle\int_0^5 g(x)\,dx=2$. Calcula:" + tasks(3, [I('f(x)', 0, 5), I(r'\big(2f(x)-g(x)\big)', 5, 0), I('f(x)', 3, 3)]),
     tasks(3, [r"$4+(-1)=\res{3}$", r"$-(2\cdot3-2)=\res{-4}$", r"$\res{0}$"])),
 (2, r"Calcula el valor de $a>0$ perquè $\displaystyle\int_0^a(2x+1)\,dx=6$.",
     r"$\Big[x^2+x\Big]_0^a=a^2+a=6\Rightarrow a^2+a-6=0\Rightarrow a=2$ o $a=-3$. Com que $a>0$: $\res{a=2}$."),
 (2, r"Calcula $k$ perquè $\displaystyle\int_1^3(kx-1)\,dx=10$.",
     r"$\Big[\frac{kx^2}{2}-x\Big]_1^3=\left(\frac{9k}{2}-3\right)-\left(\frac k2-1\right)=4k-2=10\Rightarrow\res{k=3}$."),
 (3, r"Troba $a$ i $b$ perquè la funció $f(x)=ax^2+b$ complisca $f(1)=2$ i $\displaystyle\int_0^1 f(x)\,dx=1$.",
     r"$f(1)=a+b=2$ i $\int_0^1(ax^2+b)\,dx=\frac a3+b=1$. Restant: $\frac{2a}{3}=1\Rightarrow\res{a=\frac32,\ b=\frac12}$."),
 (2, r"Aproxima $\displaystyle\int_0^2x^2\,dx$ amb 4 rectangles de la mateixa amplària, prenent com a altura el valor de la funció a l'extrem dret de cada tros. Compara-ho amb el valor exacte.",
     r"$\Delta x=0{,}5$: $S_4=0{,}5\,(0{,}25+1+2{,}25+4)=\res{3{,}75}$. Valor exacte: $\Big[\frac{x^3}{3}\Big]_0^2=\res{\frac83}\approx2{,}667$. L'aproximació és per excés (la funció és creixent)." + cen(G_RIEM)),
]))

# =====================================================================
A24 = [(Q(1, 0, -9),), (Q(-1, 2, 3),), (Q(1, -5, 4),), (Q(1, 0, -9, 0),), (Q(1, -3, 2, 0),), (Q(1, 0, -1, 0, 0),)]
A25 = [(Q(1, 0, 1), 0, 3), (Q(-1, 0, 4), 0, 3), (Q(1, -4, 0), -1, 1), (Q(1, 0, -1, 0), 0, 2), (Q(1, -2, -3), 0, 4), (Q(2, -4), 0, 5)]
S.append(("Àrea entre una corba i l'eix OX", [
 (2, r"Calcula l'àrea del recinte limitat per la gràfica de cada funció i l'eix OX. Fes-ne un esbós." + tasks(3, [r"$f(x)=x^2-9$", r"$f(x)=-x^2+2x+3$", r"$f(x)=x^2-5x+4$", r"$f(x)=x^3-9x$", r"$f(x)=x^3-3x^2+2x$", r"$f(x)=x^4-x^2$"])
     + recorda(r"Primer busquem els talls amb l'eix OX ($f(x)=0$); són els límits d'integració. Si n'hi ha més de dos, integrem cada tros per separat i sumem els valors absoluts."),
     tasks(1, [r"Talls $\pm3$: $\int_{-3}^{3}(x^2-9)\,dx=\Big[\frac{x^3}{3}-9x\Big]_{-3}^{3}=-18-18=-36\Rightarrow\res{A=36\ \text{u}^2}$",
               r"Talls $-1$ i $3$: $\Big[-\frac{x^3}{3}+x^2+3x\Big]_{-1}^{3}=9-\left(-\frac53\right)\Rightarrow\res{A=\frac{32}{3}\ \text{u}^2}$",
               r"Talls $1$ i $4$: $\Big[\frac{x^3}{3}-\frac{5x^2}{2}+4x\Big]_{1}^{4}=-\frac83-\frac{11}{6}=-\frac92\Rightarrow\res{A=\frac92\ \text{u}^2}$",
               r"Talls $-3,0,3$: $F(x)=\frac{x^4}{4}-\frac{9x^2}{2}$; $\int_{-3}^{0}f=\frac{81}{4}$, $\int_0^3f=-\frac{81}{4}\Rightarrow\res{A=\frac{81}{2}\ \text{u}^2}$",
               r"$x(x-1)(x-2)=0$; $F(x)=\frac{x^4}{4}-x^3+x^2$: $\int_0^1f=\frac14$, $\int_1^2f=-\frac14\Rightarrow\res{A=\frac12\ \text{u}^2}$",
               r"$x^2(x^2-1)=0$: talls $-1$, $0$ (doble) i $1$; $f\leq0$ en $[-1,1]$: $\int_{-1}^{1}(x^4-x^2)\,dx=\frac25-\frac23=-\frac{4}{15}\Rightarrow\res{A=\frac{4}{15}\ \text{u}^2}$"])
     + minis([gA(*q, w=4.2, h=3) for q in A24])),
 (2, r"Calcula l'àrea de la regió limitada per la gràfica de $f$, l'eix OX i les rectes indicades:" + tasks(2, [r"$f(x)=x^2+1$, \ $x=0$, \ $x=3$", r"$f(x)=4-x^2$, \ $x=0$, \ $x=3$",
      r"$f(x)=x^2-4x$, \ $x=-1$, \ $x=1$", r"$f(x)=x^3-x$, \ $x=0$, \ $x=2$", r"$f(x)=x^2-2x-3$, \ $x=0$, \ $x=4$", r"$f(x)=2x-4$, \ $x=0$, \ $x=5$"])
     + recorda(r"Ara els límits són $a$ i $b$, però hem de mirar si $f$ talla l'eix OX \textbf{dins} de l'interval: aquests talls divideixen la integral en trossos. Els talls de fora no compten."),
     tasks(1, [r"No talla l'eix: $\Big[\frac{x^3}{3}+x\Big]_0^3=\res{12\ \text{u}^2}$",
               r"Tall en $x=2$: $\int_0^2f=\frac{16}{3}$, $\int_2^3f=3-\frac{16}{3}=-\frac73\Rightarrow\res{A=\frac{23}{3}\ \text{u}^2}$",
               r"Talls $0$ i $4$; dins només el $0$: $\int_{-1}^{0}f=\frac73$, $\int_0^1f=-\frac53\Rightarrow\res{A=4\ \text{u}^2}$",
               r"Talls $-1,0,1$; dins només l'$1$: $\int_0^1f=-\frac14$, $\int_1^2f=\frac94\Rightarrow\res{A=\frac52\ \text{u}^2}$",
               r"Talls $-1$ i $3$; dins el $3$: $\int_0^3f=-9$, $\int_3^4f=\frac73\Rightarrow\res{A=\frac{34}{3}\ \text{u}^2}$",
               r"Tall en $x=2$: $\int_0^2f=-4$, $\int_2^5f=9\Rightarrow\res{A=13\ \text{u}^2}$ (dos triangles)"])
     + minis([gA(q[0], None, q[1], q[2], w=4.2, h=3) for q in A25])),
 (1, r"Un alumne diu que l'àrea limitada per $f(x)=x^3$, l'eix OX i les rectes $x=-2$ i $x=2$ és 0, perquè $\displaystyle\int_{-2}^{2}x^3\,dx=0$. Té raó? Calcula l'àrea correctament.",
     r"\rest{No}: la integral val 0 perquè la part de baix ($x<0$) es compensa amb la de dalt. $\int_{-2}^{0}x^3\,dx=-4$ i $\int_0^2x^3\,dx=4$, així que $\res{A=4+4=8\ \text{u}^2}$."
     + cen(gA(Q(1, 0, 0, 0), None, -2, 2))),
 (2, r"Considera la funció $f(x)=x^2-4x+3$." + tasks(1, [r"Representa-la gràficament.", r"Calcula l'àrea del recinte limitat per la gràfica de $f$ i l'eix OX.", r"Calcula l'àrea del recinte limitat per la gràfica de $f$ i els dos eixos de coordenades."]),
     tasks(1, [r"Paràbola cap amunt, vèrtex $(2,\,-1)$, talls $(1,\,0)$, $(3,\,0)$ i $(0,\,3)$.", r"$\int_1^3(x^2-4x+3)\,dx=\Big[\frac{x^3}{3}-2x^2+3x\Big]_1^3=0-\frac43\Rightarrow\res{A=\frac43\ \text{u}^2}$",
               r"Entre $x=0$ i el primer tall, $x=1$: $\int_0^1f=\res{\frac43\ \text{u}^2}$"])
     + cen(gA(Q(1, -4, 3)), gA(Q(1, -4, 3), None, 0, 1, box=(-0.6, 4.4, -1.6, 3.6)))),
 (3, r"Calcula $a>0$ perquè l'àrea del recinte limitat per la paràbola $f(x)=a^2-x^2$ i l'eix OX siga 36.",
     r"Talls $\pm a$: $\int_{-a}^{a}(a^2-x^2)\,dx=\Big[a^2x-\frac{x^3}{3}\Big]_{-a}^{a}=\frac{4a^3}{3}=36\Rightarrow a^3=27\Rightarrow\res{a=3}$."),
 (2, r"Calcula $k>0$ perquè l'àrea de la regió limitada per $f(x)=x^2$, l'eix OX i la recta $x=k$ siga 9.",
     r"$\int_0^k x^2\,dx=\frac{k^3}{3}=9\Rightarrow k^3=27\Rightarrow\res{k=3}$."),
]))

# =====================================================================
A30 = [(Q(1, 0, 0), Q(2, 0)), (Q(1, 0, -2), Q(1, 0)), (Q(-1, 6, 0), Q(1, -2, 0)), (Q(1, 0, 0, 0), Q(1, 0, 0)), (Q(1, 0, -2, 0), Q(2, 0)), (Q(-1, 0, 4), Q(1, 0, -4))]
A31 = [(Q(1, 0, 1), Q(-1, 0, -1), -1, 2), (Q(1, 0, 0), Q(1, 0), -1, 1), (Q(1, 0, -4), Q(-1, 2), 0, 3), (Q(1, 0, 0, 0), Q(1, 0), 0, 2)]
S.append(("Àrea entre dues corbes", [
 (2, r"Calcula l'àrea del recinte tancat per les gràfiques de les funcions:" + tasks(2, [r"$f(x)=x^2$ \ i \ $g(x)=2x$", r"$f(x)=x^2-2$ \ i \ $g(x)=x$", r"$f(x)=-x^2+6x$ \ i \ $g(x)=x^2-2x$",
      r"$f(x)=x^3$ \ i \ $g(x)=x^2$", r"$f(x)=x^3-2x$ \ i \ $g(x)=2x$", r"$f(x)=4-x^2$ \ i \ $g(x)=x^2-4$"])
     + recorda(r"Resolem $f(x)=g(x)$ per trobar els punts de tall, que són els límits. Integrem $f-g$ en cada tros i sumem els valors absoluts (o integrem «la de dalt menys la de baix»)."),
     tasks(1, [r"Talls $0$ i $2$: $\int_0^2(2x-x^2)\,dx=4-\frac83\Rightarrow\res{A=\frac43\ \text{u}^2}$",
               r"$x^2-x-2=0\Rightarrow-1,\ 2$: $\int_{-1}^{2}(x+2-x^2)\,dx\Rightarrow\res{A=\frac92\ \text{u}^2}$",
               r"$2x^2-8x=0\Rightarrow0,\ 4$: $\int_0^4(-2x^2+8x)\,dx=-\frac{128}{3}+64\Rightarrow\res{A=\frac{64}{3}\ \text{u}^2}$",
               r"$x^2(x-1)=0\Rightarrow0,\ 1$: $\int_0^1(x^2-x^3)\,dx=\frac13-\frac14\Rightarrow\res{A=\frac{1}{12}\ \text{u}^2}$",
               r"$x^3-4x=0\Rightarrow-2,0,2$: $\int_{-2}^{0}(x^3-4x)\,dx=4$, $\int_0^2(x^3-4x)\,dx=-4\Rightarrow\res{A=8\ \text{u}^2}$",
               r"$2x^2-8=0\Rightarrow\pm2$: $\int_{-2}^{2}(8-2x^2)\,dx=32-\frac{32}{3}\Rightarrow\res{A=\frac{64}{3}\ \text{u}^2}$"])
     + minis([gA(f, g, w=4.2, h=3) for f, g in A30])),
 (2, r"Calcula l'àrea de la regió limitada per les gràfiques de $f$ i $g$ i les rectes indicades:" + tasks(2, [r"$f(x)=x^2+1$, \ $g(x)=-x^2-1$, \ $x=-1$, \ $x=2$", r"$f(x)=x^2$, \ $g(x)=x$, \ $x=-1$, \ $x=1$",
      r"$f(x)=x^2-4$, \ $g(x)=-x+2$, \ $x=0$, \ $x=3$", r"$f(x)=x^3$, \ $g(x)=x$, \ $x=0$, \ $x=2$"]),
     tasks(1, [r"No es tallen ($2x^2+2>0$): $\int_{-1}^{2}(2x^2+2)\,dx=\Big[\frac{2x^3}{3}+2x\Big]_{-1}^{2}=\frac{28}{3}+\frac83\Rightarrow\res{A=12\ \text{u}^2}$",
               r"Talls $0$ i $1$; dins de $(-1,\,1)$ només el $0$: $\int_{-1}^{0}(x^2-x)\,dx=\frac56$, $\int_0^1(x^2-x)\,dx=-\frac16\Rightarrow\res{A=1\ \text{u}^2}$",
               r"$x^2+x-6=0\Rightarrow-3,\ 2$; dins el $2$: $\int_0^2(x^2+x-6)\,dx=-\frac{22}{3}$, $\int_2^3(\dots)\,dx=\frac{17}{6}\Rightarrow\res{A=\frac{61}{6}\ \text{u}^2}$",
               r"Talls $-1,0,1$; dins l'$1$: $\int_0^1(x^3-x)\,dx=-\frac14$, $\int_1^2(x^3-x)\,dx=\frac94\Rightarrow\res{A=\frac52\ \text{u}^2}$"])
     + minis([gA(f, g, a, b, w=4.2, h=3) for f, g, a, b in A31])),
 (3, r"Calcula l'àrea de la regió limitada per la paràbola $y=x^2$, la recta tangent a la paràbola en $x=1$ i l'eix OY.",
     r"Tangent: $y-1=2(x-1)\Rightarrow y=2x-1$. La paràbola queda per damunt: $x^2-(2x-1)=(x-1)^2\geq0$. Entre $x=0$ (eix OY) i $x=1$: $\int_0^1(x-1)^2\,dx=\Big[\frac{(x-1)^3}{3}\Big]_0^1=\res{\frac13\ \text{u}^2}$."
     + cen(gA(Q(1, 0, 0), Q(2, -1), 0, 1, box=(-0.8, 2.2, -1.6, 3.4)))),
 (2, r"Considera les funcions $f(x)=-x^2+5x$ i $g(x)=x$." + tasks(1, [r"Representa-les en els mateixos eixos.", r"Calcula l'àrea del recinte tancat per les dues gràfiques."]),
     tasks(1, [r"Paràbola cap avall amb vèrtex $\left(\frac52,\frac{25}{4}\right)$ i talls $(0,\,0)$ i $(5,\,0)$; recta bisectriu.",
               r"$-x^2+5x=x\Rightarrow x=0,\ 4$: $\int_0^4(-x^2+4x)\,dx=-\frac{64}{3}+32\Rightarrow\res{A=\frac{32}{3}\ \text{u}^2}$"])
     + cen(gA(Q(-1, 5, 0), Q(1, 0)))),
 (3, r"Calcula $m>0$ perquè l'àrea del recinte limitat per la paràbola $y=x^2$ i la recta $y=mx$ siga 36.",
     r"Talls $x=0$ i $x=m$: $\int_0^m(mx-x^2)\,dx=\frac{m^3}{2}-\frac{m^3}{3}=\frac{m^3}{6}=36\Rightarrow m^3=216\Rightarrow\res{m=6}$."),
]))

# =====================================================================
S.append(("Problemes d'aplicació", [
 (2, r"La funció de demanda d'un producte és $p(x)=100-x^2$, on $p$ és el preu (en euros) i $x$ la quantitat demandada (en milers d'unitats). El preu de mercat és de 64 €." + tasks(1, [r"Quina quantitat es demana a aquest preu?",
      r"L'\textbf{excedent del consumidor} és l'àrea compresa entre la corba de demanda i la recta $p=64$, des de $x=0$ fins a la quantitat demandada. Calcula'l."]),
     tasks(1, [r"$100-x^2=64\Rightarrow x^2=36\Rightarrow\res{x=6}$ milers d'unitats.", r"$\int_0^6(100-x^2-64)\,dx=\Big[36x-\frac{x^3}{3}\Big]_0^6=216-72=\res{144}$ milers d'euros."])
     + cen(gA(Q(-1, 0, 100), Q(64), 0, 6, box=(-0.8, 10.5, -8, 112)))),
 (2, r"El benefici marginal d'una empresa (en milers d'euros) quan ven $x$ tones és $B'(x)=40-2x$. Si no ven res, té unes pèrdues de 100 mil euros." + tasks(1, [r"Troba la funció de benefici $B(x)$.", r"Quantes tones ha de vendre per obtindre el benefici màxim? Quin és aquest benefici?", r"Quant augmenta el benefici si passa de vendre 5 tones a vendre'n 10? (Calcula-ho amb una integral definida.)"]),
     tasks(1, [r"$B(x)=40x-x^2+K$, amb $B(0)=-100$: $\res{B(x)=-x^2+40x-100}$", r"$B'(x)=0\Rightarrow x=20$ ($B''=-2<0$): $\res{20}$ tones i $B(20)=\res{300}$ mil euros.",
               r"$\int_5^{10}(40-2x)\,dx=\Big[40x-x^2\Big]_5^{10}=300-175=\res{125}$ mil euros."])),
 (3, r"Un pou de petroli produeix, $t$ anys després d'obrir-lo, a un ritme de $r(t)=12-\frac{3}{4}t^2$ milers de barrils per any." + tasks(1, [r"Quan deixarà de produir?", r"Quants barrils produirà en total, des que s'obri fins que es tanque?"]),
     tasks(1, [r"$12-\frac34t^2=0\Rightarrow t^2=16\Rightarrow\res{t=4}$ anys.", r"$\int_0^4\left(12-\frac34t^2\right)dt=\Big[12t-\frac{t^3}{4}\Big]_0^4=48-16=\res{32}$ milers de barrils."])),
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
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={integrals, primitiva, integral indefinida, integrals immediates, integral definida, regla de Barrow, àrees, àrea entre dues corbes}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

TIT = "Integrals"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 8: %s. 2n de Batxillerat CCSS}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 8: %s · 2n Batxillerat CCSS" % (t, TIT))
    assert 'Unitat 8' in p and 'unitat 8' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 8' if sol else "Fitxa d'exercicis · Unitat 8") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. A les gràfiques, les zones verdes són trossos on la integral és positiva, les roges on és negativa i les turqueses, regions entre dues corbes. Pots comprovar qualsevol resultat amb la calculadora d'integrals i àrees dels apunts interactius de la unitat."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos. A la PAU de Ciències Socials les integrals són de polinomis: integra terme a terme, aplica la regla de Barrow amb compte amb els signes i, en els problemes d'àrees, busca sempre primer els punts de tall i fes un esbós del recinte. No oblides la constant $C$ en les integrals indefinides ni les unitats ($\text{u}^2$) en les àrees.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb la calculadora d\'integrals i àrees dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't8-fitxa-solucions.tex' if sol else 't8-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
