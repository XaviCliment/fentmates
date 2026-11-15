# Versió en castellà de genera.py. Genera t9-fitxa-exercicis-es.tex i t9-fitxa-solucions-es.tex
# (1r ESO, Unitat 9: Gràfics de funcions — coordenades cartesianes, aplicacions, taules i gràfics,
# interpretació de gràfics, funcions de proporcionalitat directa i funcions lineals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les comprovacions CHK (amb fraccions exactes) verifiquen cada resultat escrit.
import os, re, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def center(t): return r'\par\smallskip\begin{center}' + t + r'\end{center}'
def side(*figs):
    return r'\par\smallskip\begin{center}' + r'\hspace{0.8cm}'.join(figs) + r'\end{center}'

# ---------- comprovacions ----------
NCHK = [0]
def CHK(cond, *info):
    NCHK[0] += 1
    assert cond, info
def fr(v): return v if isinstance(v, Fr) else Fr(str(v).replace('{,}', '.').replace(',', '.'))
def lin(m, n=0):
    m, n = fr(m), fr(n)
    return lambda x: m * fr(x) + n
def at(P, x):
    for (a, ya), (b, yb) in zip(P, P[1:]):
        if a <= x <= b: return fr(ya) + (fr(yb) - fr(ya)) * (fr(x) - fr(a)) / (fr(b) - fr(a))
    raise ValueError(x)
def quad(x, y):
    if x == 0 and y == 0: return 'O'
    if y == 0: return 'X'
    if x == 0: return 'Y'
    return 'I' if x > 0 and y > 0 else 'II' if x < 0 < y else 'III' if x < 0 and y < 0 else 'IV'
QT = {'I': 'cuadrante I', 'II': 'cuadrante II', 'III': 'cuadrante III', 'IV': 'cuadrante IV', 'X': 'eje $X$', 'Y': 'eje $Y$'}

# ---------- nombres i taules ----------
def tn(v):
    v = fr(v)
    if v.denominator == 1: return str(v.numerator)
    t = ('%.6f' % float(v)).rstrip('0').rstrip('.')
    CHK(fr(t) == v, v)
    return t.replace('.', '{,}')
def pt(x, y):
    a, b = tn(x), tn(y)
    return '(%s;\\ %s)' % (a, b) if '{,}' in a + b else '(%s,\\ %s)' % (a, b)
def lab(t):
    """etiqueta d'una taula (dins de $...$): text normal o fórmula entre $"""
    return t[1:-1] if t.startswith('$') and t.endswith('$') else t if t in ('x', 'y') else r'\text{%s}' % t
def tv(xs, ys, xl='x', yl='y'):
    xl, yl = lab(xl), lab(yl)
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('c' * len(xs), xl, '&'.join(tn(a) if not isinstance(a, str) else a for a in xs), yl, '&'.join(tn(a) if not isinstance(a, str) else a for a in ys)))
def tvb(xs, xl='x', yl='y'):
    xl, yl = lab(xl), lab(yl)
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('C{0.75cm}' * len(xs), xl, '&'.join(tn(a) for a in xs), yl, '&'.join([r'\phantom{00}'] * len(xs))))
def eq(m, n=0, v='x'):
    m, n = fr(m), fr(n)
    if m == 0: return 'y=' + tn(n)
    s = v if m == 1 else '-' + v if m == -1 else tn(m) + v
    if n: s += ('+' if n > 0 else '-') + tn(abs(n))
    return 'y=' + s

# ---------- pla cartesià (TikZ) ----------
COL = {'p0': 'accent', 'p1': 'teal', 'p2': 'navy'}
def tp(win, pts=(), polys=(), fns=(), curves=(), proj=(), labs=(), u=0.42, uy=None, xs=1, ys=1, gx=None, gy=None, xl='x', yl='y'):
    """win = (x0, x1, y0, y1); pts: (x, y, etiqueta, color[, posició]); polys: (vèrtexs, color); fns: (m, n, color[, a, b]);
    curves: (punts, color); proj: (x, y) línies de projecció; labs: (x, y, text, posició)"""
    x0, x1, y0, y1 = [float(v) for v in win]
    uy = uy or u; gx = gx or xs; gy = gy or ys
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center),line cap=round,line join=round]' % (u, uy)]
    k = math.ceil(x0 / gx - 1e-9)
    while k * gx <= x1 + 1e-9: o.append(r'\draw[muted!30,line width=0.3pt] (%g,%g)--(%g,%g);' % (k * gx, y0, k * gx, y1)); k += 1
    k = math.ceil(y0 / gy - 1e-9)
    while k * gy <= y1 + 1e-9: o.append(r'\draw[muted!30,line width=0.3pt] (%g,%g)--(%g,%g);' % (x0, k * gy, x1, k * gy)); k += 1
    ax = min(max(0, y0), y1); ay = min(max(0, x0), x1)
    o.append(r'\draw[-latex,muted,line width=0.6pt] (%g,%g)--(%g,%g) node[right,font=\scriptsize,text=navy]{%s};' % (x0, ax, x1 + 0.3 * gx, ax, xl))
    o.append(r'\draw[-latex,muted,line width=0.6pt] (%g,%g)--(%g,%g) node[above,font=\scriptsize,text=navy]{%s};' % (ay, y0, ay, y1 + 0.3 * gy, yl))
    k = math.ceil(x0 / xs - 1e-9)
    while k * xs < x1 - 1e-9:
        v = k * xs
        if abs(v) > 1e-9 and v > x0 + 1e-9: o.append(r'\node[font=\tiny,text=muted,below,inner sep=1.5pt] at (%g,%g) {$%s$};' % (v, ax, tn(Fr(v).limit_denominator(100))))
        k += 1
    k = math.ceil(y0 / ys - 1e-9)
    while k * ys < y1 - 1e-9:
        v = k * ys
        if abs(v) > 1e-9 and v > y0 + 1e-9: o.append(r'\node[font=\tiny,text=muted,left,inner sep=1.5pt] at (%g,%g) {$%s$};' % (ay, v, tn(Fr(v).limit_denominator(100))))
        k += 1
    o.append(r'\node[font=\tiny,text=muted,below left,inner sep=1.5pt] at (%g,%g) {$0$};' % (ay, ax))
    for V, c in polys:
        o.append(r'\draw[%s,thick,fill=%s!15] %s--cycle;' % (c, c, '--'.join('(%g,%g)' % (float(p[0]), float(p[1])) for p in V)))
    for f in fns:
        m, n, c = float(fr(f[0])), float(fr(f[1])), f[2]
        lo = float(f[3]) if len(f) > 3 and f[3] is not None else x0
        hi = float(f[4]) if len(f) > 4 and f[4] is not None else x1
        if m != 0:
            xa, xb = (y0 - n) / m, (y1 - n) / m
            lo, hi = max(lo, min(xa, xb)), min(hi, max(xa, xb))
        if lo < hi: o.append(r'\draw[%s,line width=1.1pt] (%.3f,%.3f)--(%.3f,%.3f);' % (c, lo, m * lo + n, hi, m * hi + n))
    for P, c in curves:
        o.append(r'\draw[%s,line width=1.1pt] %s;' % (c, '--'.join('(%g,%g)' % (float(p[0]), float(p[1])) for p in P)))
    for px, py in proj:
        o.append(r'\draw[accent,dashed,thin] (%g,%g)--(%g,%g)--(%g,%g);' % (float(px), ax, float(px), float(py), ay, float(py)))
    for p in pts:
        px, py, lab, c = (tuple(p) + (None, 'p2'))[:4]
        pos = p[4] if len(p) > 4 else 'above right'
        o.append(r'\fill[%s] (%g,%g) circle (2.2pt)%s;' % (COL.get(c, c), float(px), float(py), (r' node[%s,font=\scriptsize,inner sep=1.5pt]{%s}' % (pos, lab)) if lab else ''))
    for px, py, t, pos in labs:
        o.append(r'\node[font=\scriptsize,%s] at (%g,%g) {%s};' % (pos, float(px), float(py), t))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]
W5 = (-5, 5, -5, 5)

# =====================================================================
# 1. El pla cartesià. Coordenades d'un punt
# =====================================================================
P11 = [('A', 2, 3), ('B', -4, 1), ('C', -3, -2), ('D', 3, -4), ('E', 0, 2), ('F', 4, 0), ('G', -1, 4), ('H', -2, 0)]
F11 = tp(W5, pts=[(x, y, '$%s$' % n, 'p2') for n, x, y in P11])
P12 = [('P', 3, 1), ('Q', -2, 4), ('R', -4, -3), ('S', 1, -2), ('T', 0, -4), ('U', 5, 0)]
F12 = tp((-5, 6, -5, 5), pts=[(x, y, '$%s$' % n, 'p2') for n, x, y in P12])
Q13 = [(6, -2), (-3, -8), (-1, 7), (0, -5), (9, 0), (4, 4), (-6, 0), (-2, -2)]
F15 = tp(W5, pts=[(-2, 4, '$(-2,\\,4)$', 'p0'), (4, -2, '$(4,\\,-2)$', 'p1', 'below left')], u=0.38)
CHK(quad(-2, 4) == 'II' and quad(4, -2) == 'IV')
F18 = tp(W5, pts=[(k, k, None, 'p0') for k in range(-4, 5)] + [(k, 2, None, 'p1') for k in range(-4, 5)], fns=[(1, 0, 'accent!60'), (0, 2, 'teal!60')], u=0.38,
         labs=[(4.3, 4.6, '$y=x$', 'right'), (4.3, 2, '$y=2$', 'right')])
SQ = [(-3, -2), (1, -2), (1, 2), (-3, 2)]
F19 = tp(W5, polys=[(SQ, 'accent')], pts=[(-3, -2, '$A$', 'p2', 'below left'), (1, -2, '$B$', 'p2', 'below right'), (1, 2, '$C$', 'p2', 'above right'), (-3, 2, '$D$', 'p2', 'above left'), (-1, 0, '$M$', 'p1', 'above')], u=0.38)
CHK(SQ[1][0] - SQ[0][0] == SQ[2][1] - SQ[1][1] == 4 and ((-3 + 1) / 2, (-2 + 2) / 2) == (-1, 0))
S_.append(("El plano cartesiano. Coordenadas de un punto", [
 (1, r"Escribe las coordenadas de los puntos del dibujo:" + center(F11)
     + recorda(r"Las coordenadas de un punto se escriben $P(x,\ y)$: primero la \textbf{abscisa} $x$ (horizontal: derecha $+$, izquierda $-$) y después la \textbf{ordenada} $y$ (vertical: arriba $+$, abajo $-$)."),
     tasks(4, ['$%s%s$' % (n, ('\\res{' + pt(x, y) + '}')) for n, x, y in P11])),
 (1, r"Dibuja en unos ejes de coordenadas los puntos $P(3,\ 1)$, $Q(-2,\ 4)$, $R(-4,\ -3)$, $S(1,\ -2)$, $T(0,\ -4)$ y $U(5,\ 0)$.",
     center(F12)),
 (1, r"Sin dibujarlos, di en qué cuadrante o sobre qué eje está cada punto:" + tasks(4, ['$' + pt(x, y) + '$' for x, y in Q13])
     + recorda(r"Signos: cuadrante I $(+,\,+)$, II $(-,\,+)$, III $(-,\,-)$, IV $(+,\,-)$. Si $y=0$, el punto es del eje $X$; si $x=0$, del eje $Y$."),
     tasks(4, [r'\rest{%s}' % QT[quad(x, y)] for x, y in Q13])),
 (1, r"Escribe las coordenadas del punto:" + tasks(1, [r"que está 3 unidades a la derecha del eje $Y$ y 5 por encima del eje $X$;", r"que está 2 unidades a la izquierda del eje $Y$ y 4 por debajo del eje $X$;",
                                                   r"que está sobre el eje $X$, 6 unidades a la izquierda del origen;", r"que está sobre el eje $Y$, 1 unidad por encima del origen."]),
     tasks(4, [r'$\res{(3,\ 5)}$', r'$\res{(-2,\ -4)}$', r'$\res{(-6,\ 0)}$', r'$\res{(0,\ 1)}$'])),
 (2, r"Dibuja los puntos $(-2,\ 4)$ y $(4,\ -2)$. ¿Son el mismo punto? ¿En qué cuadrante está cada uno?",
     r"\rest{No}: el orden de las coordenadas importa. $(-2,\ 4)$ está en el \rest{cuadrante II} y $(4,\ -2)$, en el \rest{cuadrante IV}." + center(F15)),
 (2, r"Responde:" + tasks(1, [r"¿Qué punto del cuadrante II está a 4 unidades de cada eje?", r"¿Qué puntos del eje $X$ están a 3 unidades del origen?", r"¿Qué punto del cuadrante III tiene la abscisa $-5$ y la ordenada la mitad de la abscisa?"]),
     tasks(1, [r"En el II, $x<0$ e $y>0$: \ $\res{(-4,\ 4)}$", r"$\res{(3,\ 0)}$ y $\res{(-3,\ 0)}$", r"$y=-5:2=-2{,}5$: \ $\res{(-5;\ -2{,}5)}$"])),
 (2, r"El punto $(a,\ b)$ está en el cuadrante IV. ¿En qué cuadrante están los puntos $(-a,\ b)$, \ $(a,\ -b)$ \ y \ $(b,\ a)$?",
     r"En el IV, $a>0$ y $b<0$. \ $(-a,\ b)$: $(-,\ -)$, \rest{cuadrante III}. \ $(a,\ -b)$: $(+,\ +)$, \rest{cuadrante I}. \ $(b,\ a)$: $(-,\ +)$, \rest{cuadrante II}."),
 (3, r"Dibuja todos los puntos de coordenadas enteras entre $-4$ y $4$ que tienen la ordenada igual a la abscisa. Haz lo mismo con los que tienen la ordenada igual a 2. ¿Qué observas?",
     r"Los primeros están alineados en una recta inclinada que pasa por el origen (\rest{$y=x$}); los segundos, en una recta \rest{horizontal} (\rest{$y=2$})." + center(F18)),
 (3, r"Dibuja los puntos $A(-3,\ -2)$, $B(1,\ -2)$ y $C(1,\ 2)$. Halla el punto $D$ para que $ABCD$ sea un cuadrado y calcula las coordenadas del centro del cuadrado.",
     r"El lado mide 4: \ $D=\res{(-3,\ 2)}$. El centro está en la mitad de la diagonal: \ $M=\res{(-1,\ 0)}$." + center(F19)),
]))

# =====================================================================
# 2. Aplicacions de les coordenades
# =====================================================================
MAPA = [('E', 2, 3, 'escuela'), ('P', -3, 2, 'parque'), ('H', 4, -2, 'hospital'), ('M', -2, -3, 'mercado'), ('B', 0, -1, 'biblioteca'), ('C', -4, 0, 'campo de fútbol')]
F21 = tp(W5, pts=[(x, y, r'\textbf{%s}' % n, 'p0') for n, x, y, _ in MAPA], labs=[(0.25, 0.25, r'\faFlag', 'above right,text=muted')])
RV = [(1, 1), (6, 1), (6, 4), (1, 4)]
CHK(2 * 5 + 2 * 3 == 16 and 5 * 3 == 15)
F22 = tp((-1, 7, -1, 5), polys=[(RV, 'accent')], pts=[(1, 1, '$A$', 'p2', 'below left'), (6, 1, '$B$', 'p2', 'below right'), (6, 4, '$C$', 'p2', 'above right'), (1, 4, '$D$', 'p2', 'above left')], u=0.4)
D23 = [((-2, 3), (5, 3)), ((4, -1), (4, 6)), ((-6, -2), (-1, -2)), ((0, -4), (0, 3))]
R23 = [7, 7, 5, 7]
for (A, B), r in zip(D23, R23): CHK(abs(A[0] - B[0]) + abs(A[1] - B[1]) == r and (A[0] == B[0] or A[1] == B[1]))
ROB = [(0, 0), (4, 0), (4, 3), (-2, 3), (-2, -1), (1, -1)]
CHK(ROB[-1] == (4 - 6 + 3, 3 - 4))
F24 = tp(W5, curves=[(ROB, 'accent')], pts=[(0, 0, '$S$', 'p1', 'below right'), (1, -1, '$F$', 'p0', 'below')], u=0.36)
TR = [(-4, 1), (-1, 1), (-2, 4)]; TR2 = [(x + 5, y - 4) for x, y in TR]
CHK(TR2 == [(1, -3), (4, -3), (3, 0)])
F25 = tp(W5, polys=[(TR, 'accent'), (TR2, 'teal')], labs=[(-2.4, 2.1, '$T$', ''), (2.6, -1.9, "$T'$", '')], u=0.36)
P26 = [(3, 5), (-2, 4), (-1, -6), (5, -3)]
REC = [(-2, 1), (3, 1), (3, -2)]; D4 = (-2, -2)
CHK(5 * 3 == 15 and 2 * 5 + 2 * 3 == 16)
F27 = tp(W5, polys=[(REC + [D4], 'teal')], pts=[(-2, 1, '$A$', 'p2', 'above left'), (3, 1, '$B$', 'p2', 'above right'), (3, -2, '$C$', 'p2', 'below right'), (-2, -2, '$D$', 'p0', 'below left')], u=0.36)
TRI = [(-2, -1), (4, -1), (1, 3)]
CHK(Fr(6 * 4, 2) == 12)
F28 = tp((-3, 5, -2, 4), polys=[(TRI, 'accent')], proj=[], pts=[(-2, -1, '$A$', 'p2', 'below left'), (4, -1, '$B$', 'p2', 'below right'), (1, 3, '$C$', 'p2', 'above')], u=0.42)
CASA = [(0, 0), (4, 0), (4, 2), (2, 4), (0, 2)]
def shoelace(V): return abs(sum(V[i][0] * V[(i + 1) % len(V)][1] - V[(i + 1) % len(V)][0] * V[i][1] for i in range(len(V)))) / Fr(2)
CHK(shoelace(CASA) == 12 == 4 * 2 + Fr(4 * 2, 2) and shoelace(TRI) == 12 and shoelace(REC + [D4]) == 15)
F29 = tp((-1, 5, -1, 5), polys=[(CASA, 'accent')], curves=[([(0, 2), (4, 2)], 'muted')], u=0.42)
S_.append(("Aplicaciones de las coordenadas", [
 (1, r"En este plano de un pueblo, la bandera es la plaza (el origen) y cada cuadro es una manzana de casas. Escribe las coordenadas de la escuela ($E$), el parque ($P$), el hospital ($H$) y el mercado ($M$). ¿Qué hay en $(0,\ -1)$? ¿Y en $(-4,\ 0)$?" + center(F21),
     r"$E\res{(2,\ 3)}$, \ $P\res{(-3,\ 2)}$, \ $H\res{(4,\ -2)}$, \ $M\res{(-2,\ -3)}$. \ En $(0,\ -1)$ está la \rest{biblioteca} y en $(-4,\ 0)$, el \rest{campo de fútbol}."),
 (1, r"Dibuja el polígono de vértices $A(1,\ 1)$, $B(6,\ 1)$, $C(6,\ 4)$ y $D(1,\ 4)$. ¿Qué polígono es? Calcula su perímetro y su área (la unidad es el cm)."
     + recorda(r"Si dos puntos tienen la misma $y$, la distancia entre ellos es la diferencia de las $x$; si tienen la misma $x$, la diferencia de las $y$."),
     r"Es un \rest{rectángulo} de base $6-1=5$\,cm y altura $4-1=3$\,cm: \ $P=2\cdot5+2\cdot3=\res{16\text{ cm}}$, \ $A=5\cdot3=\res{15\text{ cm}^2}$." + center(F22)),
 (1, r"Calcula la distancia entre los puntos:" + tasks(2, [r"$(-2,\ 3)$ y $(5,\ 3)$", r"$(4,\ -1)$ y $(4,\ 6)$", r"$(-6,\ -2)$ y $(-1,\ -2)$", r"$(0,\ -4)$ y $(0,\ 3)$"]),
     tasks(2, [r"$5-(-2)=\res{7}$", r"$6-(-1)=\res{7}$", r"$-1-(-6)=\res{5}$", r"$3-(-4)=\res{7}$"])),
 (2, r"Un robot sale del origen y hace estos movimientos: 4 a la derecha, 3 arriba, 6 a la izquierda, 4 abajo y 3 a la derecha. ¿Dónde acaba? Dibuja su camino.",
     r"$(0,\ 0)\to(4,\ 0)\to(4,\ 3)\to(-2,\ 3)\to(-2,\ -1)\to\res{(1,\ -1)}$" + center(F24)),
 (2, r"Desplaza el triángulo de vértices $(-4,\ 1)$, $(-1,\ 1)$ y $(-2,\ 4)$ 5 unidades a la derecha y 4 hacia abajo. Escribe los vértices nuevos y dibuja los dos triángulos."
     + recorda(r"Desplazar $a$ a la derecha y $b$ arriba: $(x,\ y)\to(x+a,\ y+b)$ (si va a la izquierda o abajo, restamos)."),
     r"Sumamos 5 a la $x$ y restamos 4 a la $y$: \ $\res{(1,\ -3)}$, \ $\res{(4,\ -3)}$, \ $\res{(3,\ 0)}$." + center(F25)),
 (2, r"Completa la tabla con los simétricos de cada punto respecto a los ejes:" + center(r"\renewcommand{\arraystretch}{1.3}\begin{tabular}{|c|C{2.2cm}|C{2.2cm}|}\hline Punto & Simétrico respecto al eje $X$ & Simétrico respecto al eje $Y$\\\hline "
     + r'\\\hline '.join('$' + pt(x, y) + '$ & & ' for x, y in P26) + r'\\\hline\end{tabular}')
     + recorda(r"Respecto al eje $X$ cambia el signo de la $y$: $(x,\ -y)$. Respecto al eje $Y$ cambia el signo de la $x$: $(-x,\ y)$."),
     center(r'\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|c|c|}\hline Punto & Eje $X$ & Eje $Y$\\\hline ' + r'\\\hline '.join('$%s$ & $\\res{%s}$ & $\\res{%s}$' % (pt(x, y), pt(x, -y), pt(-x, y)) for x, y in P26) + r'\\\hline\end{tabular}')),
 (2, r"Tres vértices de un rectángulo son $A(-2,\ 1)$, $B(3,\ 1)$ y $C(3,\ -2)$. Halla el cuarto vértice $D$ y calcula su área y su perímetro.",
     r"$D=\res{(-2,\ -2)}$. Base $3-(-2)=5$, altura $1-(-2)=3$: \ $A=\res{15\text{ u}^2}$, \ $P=\res{16\text{ u}}$." + center(F27)),
 (3, r"Dibuja el triángulo de vértices $A(-2,\ -1)$, $B(4,\ -1)$ y $C(1,\ 3)$ y calcula su área.",
     r"La base $AB$ es horizontal y mide $4-(-2)=6$. La altura es la distancia vertical de $C$ a la base: $3-(-1)=4$. \ $A=\dfrac{6\cdot4}{2}=\res{12\text{ u}^2}$" + center(F28)),
 (3, r"Dibuja el pentágono de vértices $(0,\ 0)$, $(4,\ 0)$, $(4,\ 2)$, $(2,\ 4)$ y $(0,\ 2)$ y calcula su área.",
     r"Tiene forma de casita: un rectángulo $4\times2$ y, encima, un triángulo de base 4 y altura 2. \ $A=8+\dfrac{4\cdot2}{2}=8+4=\res{12\text{ u}^2}$" + center(F29)),
]))

# =====================================================================
# 3. Relacions entre magnituds: taules i gràfics
# =====================================================================
PA = [1, 2, 3, 4, 5, 6]; PAv = [lin('0.4')(k) for k in PA]
CHK(PAv == [fr(v) for v in ('0.4', '0.8', '1.2', '1.6', '2', '2.4')])
F31 = tp((0, 6.6, 0, 2.7), pts=[(k, v, None, 'p0') for k, v in zip(PA, PAv)], u=0.62, uy=1.3, ys=0.4, xl='panecillos', yl='€')
F33 = tp((-1, 5, 0, 12.5), fns=[(2, 3, 'accent', 0, 4)], pts=[(k, 2 * k + 3, None, 'p2') for k in range(5)], u=0.5, uy=0.3, ys=2, gy=1)
H34 = [0, 3, 6, 9, 12, 15, 18, 21, 24]; T34 = [8, 6, 7, 12, 16, 18, 15, 11, 9]
F34 = tp((0, 25, 0, 20), curves=[(list(zip(H34, T34)), 'accent')], pts=[(h, t, None, 'p2') for h, t in zip(H34, T34)], u=0.26, uy=0.22, xs=3, ys=2, xl='h', yl=r'$^\circ$C')
T35 = [([1, 2, 3, 4], [5, 10, 15, 20]), ([1, 1, 2, 3], [4, 6, 8, 9]), ([0, 2, 4, 6], [3, 3, 3, 3])]
def isfun(T): return all(T[1][i] == T[1][j] for i in range(len(T[0])) for j in range(len(T[0])) if T[0][i] == T[0][j])
CHK([isfun(T) for T in T35] == [True, False, True])
T36a = ([0, 1, 2, 3], [5, 7, 9, 11]); T36b = ([1, 2, 3, 4], [10, 20, 30, 40]); T36c = ([0, 1, 2, 3], [9, 8, 7, 6])
for (X, Y), (m, n) in zip([T36a, T36b, T36c], [(2, 5), (10, 0), (-1, 9)]): CHK([lin(m, n)(x) for x in X] == Y)
MOB = lin(3, 10); CHK([MOB(k) for k in (0, 1, 2, 5, 10)] == [10, 13, 16, 25, 40])
F38 = tp((0, 5.5, 0, 26), pts=[(l, 4 * l, None, 'p0') for l in range(1, 6)] + [(l, l * l, None, 'p1') for l in range(1, 6)], curves=[([(l / 10, 4 * l / 10) for l in range(0, 53)], 'accent'), ([(l / 10, (l / 10) ** 2) for l in range(0, 51)], 'teal')],
         u=0.7, uy=0.15, ys=5, gy=5, xl='$l$', yl='', labs=[(5.3, 21, '$P$', 'right,text=accent'), (5, 25, '$A$', 'left,text=teal')])
CHK([4 * l for l in range(1, 6)] == [4, 8, 12, 16, 20] and [l * l for l in range(1, 6)] == [1, 4, 9, 16, 25])
F39 = tp((0, 10.5, 0, 10.5), pts=[(b, 10 - b, None, 'p0') for b in range(1, 10)], u=0.36, xs=1, ys=1, xl='base', yl='altura')
CHK(all(2 * b + 2 * (10 - b) == 20 for b in range(1, 10)))
S_.append(("Relaciones entre magnitudes: tablas y gráficas", [
 (1, r"Un panecillo vale 0,40\,€. Completa la tabla, dibuja la gráfica y di si se tienen que unir los puntos." + center(tvb(PA, 'Panecillos', 'Precio (€)'))
     + recorda(r"Cada par $(x,\ y)$ de la tabla es un punto de la gráfica. Unimos los puntos solo si también tienen sentido los valores intermedios."),
     center(tv(PA, PAv, 'Panecillos', 'Precio (€)')) + r"\rest{No} se unen: no se puede comprar medio panecillo." + center(F31)),
 (1, r"Di cuál es la variable independiente y cuál la dependiente:" + tasks(1, [r"el tiempo que está abierto un grifo y los litros de agua que salen;", r"el número de fotocopias y el precio que pagamos;", r"la hora del día y la temperatura;", r"los km que hace un coche y la gasolina que le queda."]),
     tasks(1, [r"independiente: \rest{tiempo}; dependiente: \rest{litros}", r"independiente: \rest{fotocopias}; dependiente: \rest{precio}", r"independiente: \rest{hora}; dependiente: \rest{temperatura}", r"independiente: \rest{km}; dependiente: \rest{gasolina}"])),
 (1, r"Completa la tabla de la función $y=2x+3$, escribe los puntos y dibújalos." + center(tvb([0, 1, 2, 3, 4])),
     center(tv([0, 1, 2, 3, 4], [2 * k + 3 for k in range(5)])) + r"Puntos: $(0,\ 3)$, $(1,\ 5)$, $(2,\ 7)$, $(3,\ 9)$, $(4,\ 11)$. Están alineados:" + center(F33)),
 (1, r"La tabla da la temperatura de un día de primavera. Dibuja la gráfica (uniendo los puntos) y di a qué hora hizo más calor y a qué hora más frío." + center(tv(H34, T34, 'Hora', r'$^\circ\text{C}$')),
     center(F34) + r"Más calor: a las \rest{15 h} (18\,$^\circ$C). Más frío: a las \rest{3 h} (6\,$^\circ$C)."),
 (2, r"¿Cuáles de estas tablas corresponden a una función? Explica por qué." + center(r'\quad '.join(tv(*T) for T in T35)),
     r"La 1.\textsuperscript{a} y la 3.\textsuperscript{a} \rest{sí}; la 2.\textsuperscript{a} \rest{no}, porque para $x=1$ hay dos valores de $y$ (4 y 6). La 3.\textsuperscript{a} es una función constante."),
 (2, r"Halla la fórmula de cada tabla:" + center(r'\quad '.join(tv(*T) for T in (T36a, T36b, T36c))),
     tasks(3, [r"Empieza en 5 y suma 2: \ $\res{y=2x+5}$", r"$y$ es 10 veces $x$: \ $\res{y=10x}$", r"Empieza en 9 y resta 1: \ $\res{y=9-x}$"])),
 (2, r"Una tarifa de móvil cuesta 10\,€ al mes más 3\,€ por cada GB de datos. Escribe la fórmula del precio $y$ si gastamos $x$ GB y haz una tabla para 0, 1, 2, 5 y 10 GB.",
     r"$\res{y=3x+10}$ \qquad " + tv([0, 1, 2, 5, 10], [10, 13, 16, 25, 40], 'GB', '€')),
 (3, r"Haz una tabla del perímetro $P$ y otra del área $A$ de un cuadrado de lado $l=1,\ 2,\ 3,\ 4,\ 5$\,cm. Escribe sus fórmulas y dibuja las gráficas. ¿Cuál es una recta?",
     tv([1, 2, 3, 4, 5], [4, 8, 12, 16, 20], '$l$', '$P$') + r'\quad ' + tv([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], '$l$', '$A$') + r"\quad $\res{P=4l}$, \ $\res{A=l^2}$" + center(F38)
     + r"La del \rest{perímetro} es una recta (suma siempre 4); la del área es una curva (suma 3, 5, 7, 9…)."),
 (3, r"Queremos hacer rectángulos de 20\,cm de perímetro con lados de cm enteros. Haz una tabla con la base $x$ y la altura $y$, escribe su fórmula y dibuja la gráfica. ¿Es creciente o decreciente?",
     r"La base y la altura suman 10: \ $\res{y=10-x}$. \quad " + tv(list(range(1, 10)), [10 - b for b in range(1, 10)], 'base', 'alt.') + center(F39) + r"Es \rest{decreciente}: cuanta más base, menos altura. No se unen los puntos (lados enteros)."),
]))

# =====================================================================
# 4. Interpretació de gràfics
# =====================================================================
EXC = [(0, 0), (1, 6), (2, 6), (4, 14), (5, 14), (7, 0)]
CHK(at(EXC, 3) == 10 and at(EXC, 6) == 7 and 14 + 14 == 28)
F41 = tp((0, 7.5, 0, 16), curves=[(EXC, 'accent')], pts=[(x, y, None, 'p2') for x, y in EXC], u=0.75, uy=0.3, ys=2, xl='tiempo (h)', yl='distancia (km)')
TA = [(0, 6), (2, 4), (6, 4), (10, 12), (14, 18), (18, 14), (22, 8), (24, 7)]
F42 = tp((0, 25, 0, 20), curves=[(TA, 'accent')], u=0.26, uy=0.2, xs=2, ys=2, xl='h', yl=r'$^\circ$C')
PL = [(0, 2), (1, 5), (2, 9), (3, 12), (4, 14), (5, 15), (6, 15)]
F43 = tp((0, 6.6, 0, 16.5), curves=[(PL, 'teal')], pts=[(x, y, None, 'p2') for x, y in PL], u=0.6, uy=0.22, ys=2, xl='semanas', yl='cm')
CHK(PL[4][1] == 14 and PL[1][1] - PL[0][1] == 3 and PL[2][1] - PL[1][1] == 4 and PL[6][1] - PL[5][1] == 0)
BOT = [(0, 0), (5, 20), (6, 26), (16, 26), (17, 20), (22, 0)]
F44 = tp((0, 23, 0, 30), curves=[(BOT, 'accent')], u=0.33, uy=0.14, xs=2, ys=5, gy=5, xl='min', yl='cm')
CHK(Fr(20, 5) == 4)
GR = {'A': [(0, 0), (2, 4), (4, 4), (6, 0)], 'B': [(0, 0), (6, 8)], 'C': [(0, 0), (2, 4), (4, 4), (6, 8)], 'D': [(0, 8), (3, 2), (6, 2)]}
def mini(P, cap): return r'\begin{tabular}{c}' + tp((0, 6.5, 0, 9), curves=[(P, 'accent')], u=0.3, uy=0.22, xs=2, ys=2, xl='$t$', yl='$d$') + r'\\ \textbf{' + cap + r'}\end{tabular}'
F45 = center(r'\hspace{0.3cm}'.join(mini(GR[k], k) for k in 'ABCD'))
TREN = [(0, 0), (20, 30), (25, 30), (45, 60), (50, 60), (70, 90)]
CHK(Fr(30, 20) == Fr(3, 2) and 90 == TREN[-1][1])
F46 = tp((0, 75, 0, 100), curves=[(TREN, 'accent')], u=0.12, uy=0.05, xs=10, gx=5, ys=20, gy=10, xl='min', yl='km')
CA = [(0, 0), (5, 75)]; CP = [(1, 0), (5, 100)]
CHK(lin(15)(4) == 60 and lin(25, -25)(4) == 75 and lin(15)(Fr(5, 2)) == lin(25, -25)(Fr(5, 2)) == Fr(75, 2))
F47 = tp((0, 5.5, 0, 105), curves=[(CA, 'accent'), (CP, 'teal')], pts=[(2.5, 37.5, None, 'p2')], u=0.9, uy=0.04, ys=20, gy=10, xl='h', yl='km', labs=[(5, 75, 'Ana', 'right,text=accent'), (4.6, 100, 'Pablo', 'left,text=teal')])
MARC = [(0, 0), (20, 1), (50, 1), (60, 0)]
F48 = tp((0, 65, 0, 1.4), curves=[(MARC, 'accent')], u=0.13, uy=3, xs=10, ys=0.5, gy=0.25, gx=5, xl='min', yl='km')
S_.append(("Interpretación de gráficas", [
 (1, r"La gráfica muestra la excursión en bici de Nuria (distancia a casa a lo largo del tiempo)." + center(F41)
     + tasks(1, [r"¿A qué distancia de casa estaba a las 3 horas? ¿Y a las 6 horas?", r"¿Cuántas veces paró y cuánto tiempo cada vez?", r"¿Cuál es la distancia máxima a la que llegó? ¿A qué hora?", r"¿Cuánto tardó en volver? ¿Qué distancia recorrió en total?"])
     + recorda(r"Gráfica de distancia y tiempo: si sube, se aleja; si es horizontal, está parado; si baja, vuelve. Cuanto más inclinada, más deprisa."),
     tasks(1, [r"$\res{10\text{ km}}$ y $\res{7\text{ km}}$", r"\rest{dos} veces, de $\res{1\text{ hora}}$ cada una (de 1 a 2 h y de 4 a 5 h)", r"$\res{14\text{ km}}$, de las 4 a las 5 h", r"de 5 a 7 h: $\res{2\text{ horas}}$; en total, $14+14=\res{28\text{ km}}$"])),
 (1, r"La gráfica da la temperatura a lo largo de un día." + center(F42) + tasks(1, [r"¿Cuál fue la temperatura máxima? ¿Y la mínima?", r"¿En qué intervalos de tiempo sube la temperatura? ¿En cuáles baja? ¿Cuándo es constante?"]),
     tasks(1, [r"Máxima: $\res{18\ ^\circ\text{C}}$ (a las 14 h). Mínima: $\res{4\ ^\circ\text{C}}$ (de 2 a 6 h).", r"Sube de \rest{6 a 14 h}; baja de \rest{0 a 2 h} y de \rest{14 a 24 h}; es constante de \rest{2 a 6 h}."])),
 (1, r"La gráfica muestra la altura de una planta durante 6 semanas." + center(F43) + tasks(1, [r"¿Cuánto medía al empezar? ¿Y en la 4.\textsuperscript{a} semana?", r"¿En qué semana creció más?", r"¿Qué pasa entre la 5.\textsuperscript{a} y la 6.\textsuperscript{a} semana?"]),
     tasks(1, [r"$\res{2\text{ cm}}$ y $\res{14\text{ cm}}$", r"en la \rest{2.\textsuperscript{a} semana} (de 5 a 9 cm: 4 cm)", r"\rest{no crece}: la gráfica es horizontal"])),
 (2, r"La gráfica muestra la altura del agua de una bañera. Explica qué pasa en cada tramo." + center(F44),
     r"De 0 a 5 min \rest{se llena} (4\,cm por minuto). De 5 a 6 min el agua sube de golpe: alguien \rest{se mete}. De 6 a 16 min se \rest{baña} (constante). De 16 a 17 min \rest{sale} y el agua baja. De 17 a 22 min \rest{se vacía}."),
 (2, r"¿Qué gráfica (tiempo, distancia a casa) corresponde a cada historia? Hay una que sobra." + F45
     + tasks(1, [r"Sara va a casa de una amiga sin parar.", r"Óscar sale de casa, se para a comprar el pan y continúa hasta la escuela.", r"Lucía va al quiosco, se queda un rato y vuelve a casa."]),
     tasks(3, [r"\rest{B}", r"\rest{C}", r"\rest{A}"]) + r"Sobra la D (empieza lejos de casa y se acerca)."),
 (2, r"La gráfica muestra el viaje de un tren." + center(F46) + tasks(1, [r"¿Cuántas paradas hace y cuánto duran?", r"¿Cuántos km hace entre parada y parada? ¿Cuánto tarda?", r"¿Qué distancia total recorre y cuánto tiempo tarda?"]),
     tasks(1, [r"\rest{2 paradas} de $\res{5\text{ min}}$", r"\res{30\text{ km}} en \res{20\text{ min}}", r"\res{90\text{ km}} en \res{70\text{ min}}"])),
 (3, r"Ana y Pablo hacen la misma ruta en bici. Observa la gráfica y responde." + center(F47)
     + tasks(1, [r"¿Quién sale primero? ¿Cuánto rato antes?", r"¿Cuántos km hace cada uno en una hora? ¿Quién va más deprisa?", r"¿Dónde y cuándo alcanza Pablo a Ana?"]),
     tasks(1, [r"\rest{Ana}, \res{1\text{ hora}} antes.", r"Ana: $75:5=\res{15\text{ km}}$; Pablo: $100:4=\res{25\text{ km}}$. \rest{Pablo} va más deprisa.", r"Las líneas se cortan a las $\res{2{,}5\text{ h}}$, a $\res{37{,}5\text{ km}}$ de la salida."])),
 (3, r"Marcos sale de casa, camina 1\,km en 20 minutos hasta la biblioteca, se queda allí media hora y vuelve a casa en 10 minutos. Dibuja la gráfica (tiempo en minutos, distancia a casa en km). ¿En qué tramo va más deprisa?",
     center(F48) + r"Puntos: $(0,\ 0)$, $(20,\ 1)$, $(50,\ 1)$, $(60,\ 0)$. Va más deprisa a la \rest{vuelta}: el tramo es más inclinado."),
]))

# =====================================================================
# 5. Funció de proporcionalitat directa: y = m·x
# =====================================================================
F51 = ['y=4x', 'y=x+4', r'y=-\tfrac{x}{2}', 'y=4', 'y=0{,}6x', 'y=-3x']
R51 = [r'\rest{sí}, $m=\res{4}$', r'\rest{no}', r'\rest{sí}, $m=\res{-\tfrac12}$', r'\rest{no}', r'\rest{sí}, $m=\res{0{,}6}$', r'\rest{sí}, $m=\res{-3}$']
X5 = [-2, -1, 0, 1, 2]
F52 = tp((-3, 3, -7, 7), fns=[(3, 0, 'accent')], pts=[(k, 3 * k, None, 'p2') for k in X5], u=0.42, uy=0.3, ys=2)
F53 = tp(W5, fns=[(-2, 0, 'accent'), (Fr(1, 2), 0, 'teal')], pts=[(-2, 4, None, 'p0'), (2, -4, None, 'p0'), (-4, -2, None, 'p1'), (4, 2, None, 'p1')], u=0.38, labs=[(-2.6, 4.6, '$y=-2x$', 'left,text=accent'), (4.4, 2.8, r'$y=\frac x2$', 'text=teal')])
CHK(fr(-6) / 3 == -2 and lin(-2)(-4) == 8 and lin(-2)(5) == -10)
T55 = ([2, 4, 6, 8], [3, 6, 9, 12])
CHK(len({Fr(y, x) for x, y in zip(*T55)}) == 1 and Fr(3, 2) * 10 == 15)
F55 = tp((-1, 9, -1, 13), fns=[(Fr(3, 2), 0, 'accent', 0, 8.6)], pts=[(x, y, None, 'p2') for x, y in zip(*T55)], u=0.38, uy=0.3, ys=2)
L56 = [('a', 5), ('b', Fr(-1, 2)), ('c', Fr(1, 3)), ('d', -2)]
F57 = tp((0, 55, 0, 60), fns=[(Fr(11, 10), 0, 'accent', 0, 54)], pts=[(20, 22, None, 'p2'), (50, 55, None, 'p0')], proj=[(20, 22), (50, 55)], u=0.13, uy=0.11, xs=10, gx=5, ys=10, gy=5, xl='€', yl='\\$')
CHK(fr('1.1') * 20 == 22 and 55 / fr('1.1') == 50 and fr('1.1') * 35 == fr('38.5'))
F58 = tp((0, 4.3, 0, 400), fns=[(90, 0, 'accent', 0, 4.2)], pts=[(fr('2.5'), 225, None, 'p0')], proj=[(2.5, 225)], u=1, uy=0.012, xs=1, gx=0.5, ys=50, gy=50, xl='$t$ (h)', yl='$d$ (km)')
CHK(lin(90)(3) == 270 and Fr(225, 90) == fr('2.5'))
S_.append(("Función de proporcionalidad directa: $y=m\\cdot x$", [
 (1, r"¿Cuáles de estas funciones son de proporcionalidad directa? Escribe su pendiente $m$." + tasks(6, ['$' + f + '$' for f in F51])
     + recorda(r"Una función de proporcionalidad directa es de la forma $y=m\cdot x$. Su gráfica es una recta que pasa por el origen. La pendiente $m$ es lo que aumenta $y$ cuando $x$ aumenta 1."),
     tasks(3, R51)),
 (1, r"Completa la tabla de $y=3x$ y dibuja su gráfica." + center(tvb(X5)),
     center(tv(X5, [3 * k for k in X5]) + r'\qquad ' + F52)),
 (1, r"Dibuja en los mismos ejes $y=-2x$ e $y=\dfrac{x}{2}$. ¿Cuál es creciente? ¿Cuál está más inclinada?",
     center(F53) + r"$y=\frac x2$ es \rest{creciente} ($m>0$). $y=-2x$ es decreciente y \rest{más inclinada} ($2>0{,}5$)."),
 (2, r"Una recta pasa por el origen y por el punto $(3,\ -6)$. Escribe su fórmula y comprueba si los puntos $(-4,\ 8)$ y $(5,\ -12)$ son de la recta.",
     r"$m=\dfrac{-6}{3}=-2$: \ $\res{y=-2x}$. \ $-2\cdot(-4)=8$: $(-4,\ 8)$ \rest{sí}. \ $-2\cdot5=-10\neq-12$: $(5,\ -12)$ \rest{no}."),
 (2, r"Comprueba que esta tabla es de proporcionalidad directa, escribe su fórmula y dibuja la gráfica. ¿Cuánto vale $y$ si $x=10$?" + center(tv(*T55)),
     r"$\frac32=\frac64=\frac96=\frac{12}{8}=1{,}5$: \ $\res{y=1{,}5x}$. \ Para $x=10$: $y=\res{15}$." + center(F55)),
 (2, r"Ordena estas rectas de más inclinada a menos y di cuáles son decrecientes: \ $a$: $y=5x$, \ $b$: $y=-\frac12x$, \ $c$: $y=\frac13x$, \ $d$: $y=-2x$.",
     r"Miramos $m$ sin signo: $5>2>\frac12>\frac13$. \ Orden: \rest{$a$, $d$, $b$, $c$}. Decrecientes ($m<0$): \rest{$b$ y $d$}."),
 (3, r"Un día, 1\,€ vale 1,10 dólares. Escribe la fórmula que pasa de euros ($x$) a dólares ($y$) y dibuja su gráfica. ¿Cuántos dólares son 20\,€? ¿Y 35\,€? ¿Cuántos euros son 55\,\$?",
     r"$\res{y=1{,}1x}$. \ $1{,}1\cdot20=\res{22\ \$}$; \ $1{,}1\cdot35=\res{38{,}5\ \$}$; \ $55:1{,}1=\res{50\text{ €}}$." + center(F57)),
 (3, r"Un coche va a 90\,km/h siempre a la misma velocidad. Escribe la fórmula de la distancia $d$ que recorre en $t$ horas, dibuja su gráfica y calcula qué distancia hace en 3 horas y cuánto tarda en hacer 225\,km.",
     r"$\res{d=90t}$. \ $90\cdot3=\res{270\text{ km}}$. \ $225:90=\res{2{,}5\text{ h}}$ (2 horas y media)." + center(F58)),
]))

# =====================================================================
# 6. Funció lineal: y = m·x + n
# =====================================================================
M61 = [('3x-4', 3, -4), ('-x+5', -1, 5), (r'\tfrac{x}{2}+1', Fr(1, 2), 1), ('-2x', -2, 0), ('7', 0, 7), ('6-4x', -4, 6)]
F62 = tp(W5, fns=[(2, -1, 'accent')], pts=[(k, 2 * k - 1, None, 'p2') for k in (-1, 0, 1, 2, 3)], u=0.38)
CHK([lin(2, -1)(k) for k in (-1, 0, 1, 2, 3)] == [-3, -1, 1, 3, 5])
P63 = [(2, 1), (-1, 7), (3, -2), (0, 3)]
CHK([lin(-2, 3)(x) == y for x, y in P63] == [False, False, False, True])
CHK([lin(-2, 3)(x) for x, _ in P63] == [-1, 5, -3, 3])
F64 = tp(W5, fns=[(1, 2, 'accent'), (-1, 4, 'teal')], pts=[(1, 3, '$(1,\\,3)$', 'p2')], u=0.38, labs=[(-4.4, -2.4, '$y=x+2$', 'above left,text=accent'), (-0.8, 4.9, '$y=-x+4$', 'left,text=teal')])
CHK(lin(1, 2)(1) == lin(-1, 4)(1) == 3)
L65 = [('a', 2, -1), ('b', -1, 3), ('c', Fr(1, 2), 1), ('d', 0, -3)]
F65 = tp(W5, fns=[(m, n, c) for (_, m, n), c in zip(L65, ['accent', 'teal', 'navy', 'violet'])],
         labs=[(2.8, 4.6, '$a$', 'right,text=accent'), (-1.8, 4.6, '$b$', 'left,text=teal'), (4.4, 3.2, '$c$', 'above,text=navy'), (-4.5, -3, '$d$', 'above,text=violet')], u=0.4)
for _, m, n in L65: CHK(lin(m, n)(0) == n and lin(m, n)(2) - lin(m, n)(0) == 2 * fr(m))
L66 = ['y=3x+1', 'y=-x', 'y=3x-4', 'y=5', 'y=-x+2', 'y=2']
T67 = ([0, 1, 2, 3], [4, 1, -2, -5])
CHK([lin(-3, 4)(x) for x in T67[0]] == T67[1])
CHK(lin(2, 3)(0) == 3 and lin(2, 3)(2) == 7 and lin(2, -3)(1) == -1 and lin(2, -3)(3) == 3)
CHK(lin(-3, 5)(2) == -1 and lin(2, 5)(3) == 11)
S_.append(("Función lineal: $y=m\\cdot x+n$", [
 (1, r"Escribe la pendiente $m$ y la ordenada en el origen $n$ de cada función:" + tasks(6, ['$y=' + s + '$' for s, _, _ in M61])
     + recorda(r"En $y=mx+n$, $m$ es la \textbf{pendiente} (lo que cambia $y$ cuando $x$ aumenta 1) y $n$ es la \textbf{ordenada en el origen}: la recta corta el eje $Y$ en $(0,\ n)$."),
     tasks(3, [r'$m=\res{%s}$, $n=\res{%s}$' % (tn(m), tn(n)) for _, m, n in M61])),
 (1, r"Completa la tabla de $y=2x-1$ y dibuja su gráfica. ¿Dónde corta el eje $Y$?" + center(tvb([-1, 0, 1, 2, 3])),
     center(tv([-1, 0, 1, 2, 3], [-3, -1, 1, 3, 5]) + r'\qquad ' + F62) + r"Corta el eje $Y$ en $\res{(0,\ -1)}$."),
 (1, r"¿Cuáles de estos puntos son de la recta $y=-2x+3$? \ $(2,\ 1)$, \ $(-1,\ 7)$, \ $(3,\ -2)$, \ $(0,\ 3)$.",
     r"Sustituimos la $x$: \ $x=2$: $-1\neq1$ \rest{no}; \ $x=-1$: $5\neq7$ \rest{no}; \ $x=3$: $-3\neq-2$ \rest{no}; \ $x=0$: $3$ \rest{sí}."),
 (2, r"Dibuja en los mismos ejes $y=x+2$ e $y=-x+4$. ¿En qué punto se cortan? Compruébalo con las fórmulas.",
     center(F64) + r"Se cortan en $\res{(1,\ 3)}$: \ $1+2=3$ \ y \ $-1+4=3$."),
 (2, r"Escribe la fórmula de cada una de las rectas del dibujo." + center(F65),
     tasks(4, [r"$\res{%s}$" % eq(m, n) for _, m, n in L65])),
 (2, r"Observa estas funciones: \ " + ', \ '.join('$' + s + '$' for s in L66) + r". ¿Cuáles son paralelas? ¿Cuáles pasan por el origen? ¿Cuáles son constantes?",
     r"Paralelas (misma $m$): \rest{$y=3x+1$ e $y=3x-4$}; \rest{$y=-x$ e $y=-x+2$}; \rest{$y=5$ e $y=2$}. Por el origen: \rest{$y=-x$}. Constantes: \rest{$y=5$ e $y=2$}."),
 (2, r"Halla la fórmula de la función lineal de esta tabla:" + center(tv(*T67)),
     r"Para $x=0$, $y=4$: $n=4$. Cada vez que $x$ aumenta 1, $y$ disminuye 3: $m=-3$. \ $\res{y=-3x+4}$"),
 (3, r"Halla la fórmula de la recta que pasa por:" + tasks(2, [r"$(0,\ 3)$ y $(2,\ 7)$", r"$(1,\ -1)$ y $(3,\ 3)$"]),
     tasks(1, [r"$n=3$; de $x=0$ a $x=2$, $y$ sube 4: $m=4:2=2$. \ $\res{y=2x+3}$",
               r"De $x=1$ a $x=3$, $y$ sube 4: $m=2$. Volviendo un paso atrás desde $(1,\ -1)$: $n=-1-2=-3$. \ $\res{y=2x-3}$"])),
 (3, r"Responde:" + tasks(1, [r"¿Qué valor tiene que tener $k$ para que el punto $(2,\ k)$ sea de la recta $y=-3x+5$?", r"¿Qué valor tiene que tener $a$ para que el punto $(a,\ 11)$ sea de la recta $y=2x+5$?"]),
     tasks(1, [r"$k=-3\cdot2+5=\res{-1}$", r"$2a+5=11\Rightarrow2a=6\Rightarrow a=\res{3}$"])),
]))

# =====================================================================
# 7. Problemes amb funcions lineals
# =====================================================================
TX = lin('1.5', '3.5'); CHK(TX(8) == fr('15.5') and (fr(26) - fr('3.5')) / fr('1.5') == 15)
F71 = tp((0, 16.5, 0, 28), fns=[(fr('1.5'), fr('3.5'), 'accent', 0, 16.5)], pts=[(0, 3.5, None, 'p2'), (8, 15.5, None, 'p2'), (15, 26, None, 'p0')], proj=[(8, 15.5), (15, 26)], u=0.36, uy=0.2, xs=2, gx=1, ys=4, gy=2, xl='km', yl='€')
ESP = lin(-3, 24); CHK(ESP(5) == 9 and Fr(24, 3) == 8)
F72 = tp((0, 8.8, 0, 26), fns=[(-3, 24, 'accent', 0, 8)], u=0.5, uy=0.16, xs=1, ys=4, gy=2, xl='h', yl='cm')
MB = lin('0.08', 6); CHK(MB(50) == 10 and (fr(9) - 6) / fr('0.08') == fr('37.5'))
DP = lin(25, 100); CHK(DP(6) == 250 and (fr(600) - 100) / 25 == 20)
LP = [(1, 55), (2, 90), (3, 125)]; LF = lin(35, 20)
for h, p in LP: CHK(LF(h) == p)
CHK(LF(6) == 230 and (fr(300) - 20) / 35 == 8)
FA = lin('1.8', 32); CHK(FA(0) == 32 and FA(100) == 212 and FA(25) == 77 and (fr(50) - 32) / fr('1.8') == 10)
PK = lin(2, 3); CHK(PK(5) == 13 and (fr(19) - 3) / 2 == 8)
LA, LB = lin('0.25', 30), lin('0.15', 50); CHK(LA(150) == fr('67.5') and LB(150) == fr('72.5') and LA(200) == LB(200) == 80)
F79 = tp((0, 330, 0, 140), fns=[(fr('0.25'), 30, 'accent', 0, 330), (fr('0.15'), 50, 'teal', 0, 330)], pts=[(200, 80, None, 'p2')], proj=[(200, 80)], u=0.03, uy=0.045, xs=50, gx=25, ys=20, gy=10, xl='km', yl='€',
         labs=[(320, 110, 'A', 'right,text=accent'), (320, 98, 'B', 'right,text=teal')])
GA_, GB_ = lin(20, 45), lin(35); CHK(GA_(3) == GB_(3) == 105 and GA_(2) > GB_(2) and GA_(6) < GB_(6))
F710 = tp((0, 6.5, 0, 240), fns=[(20, 45, 'accent', 0, 6.5), (35, 0, 'teal', 0, 6.5)], pts=[(3, 105, None, 'p2')], proj=[(3, 105)], u=0.9, uy=0.022, ys=40, gy=20, xl='meses', yl='€',
          labs=[(6.5, 175, 'A', 'right,text=accent'), (6.4, 227, 'B', 'right,text=teal')])
S_.append(("Problemas con funciones lineales", [
 (1, r"Un taxi cobra 3,50\,€ de bajada de bandera y 1,50\,€ por km. Escribe la fórmula del precio, dibuja su gráfica y calcula cuánto cuesta un viaje de 8\,km. ¿Cuántos km hemos hecho si pagamos 26\,€?"
     + recorda(r"En muchos problemas hay una \textbf{parte fija} $n$ y una cantidad $m$ que se suma (o se resta) por cada unidad: $y=mx+n$."),
     r"$\res{y=1{,}5x+3{,}5}$. \ $1{,}5\cdot8+3{,}5=\res{15{,}50\text{ €}}$. \ $1{,}5x+3{,}5=26\Rightarrow1{,}5x=22{,}5\Rightarrow x=\res{15\text{ km}}$." + center(F71)),
 (1, r"Una vela mide 24\,cm y se consume 3\,cm cada hora. Escribe la fórmula de la altura $y$ al cabo de $x$ horas y dibuja su gráfica. ¿Cuánto medirá al cabo de 5\,h? ¿Cuándo se acabará?",
     r"$\res{y=-3x+24}$. \ $-15+24=\res{9\text{ cm}}$. \ $-3x+24=0\Rightarrow x=\res{8\text{ h}}$." + center(F72)),
 (1, r"Una tarifa de teléfono cuesta 6\,€ al mes más 0,08\,€ por minuto. ¿Cuánto pagamos si hablamos 50 minutos? ¿Cuántos minutos hemos hablado si pagamos 9\,€?",
     r"$y=0{,}08x+6$. \ $0{,}08\cdot50+6=\res{10\text{ €}}$. \ $0{,}08x=3\Rightarrow x=\res{37{,}5\text{ min}}$."),
 (2, r"Un depósito tiene 100\,L de agua y un grifo echa 25\,L cada minuto. Escribe la fórmula. ¿Cuántos litros habrá al cabo de 6 minutos? Si caben 600\,L, ¿cuándo se llenará?",
     r"$\res{y=25x+100}$. \ $150+100=\res{250\text{ L}}$. \ $25x+100=600\Rightarrow25x=500\Rightarrow x=\res{20\text{ min}}$."),
 (2, r"Un fontanero cobra según esta tabla. Halla la fórmula y calcula cuánto cobrará por 6 horas. ¿Cuántas horas ha trabajado si cobra 300\,€?" + center(tv([h for h, _ in LP], [p for _, p in LP], 'Horas', 'Precio (€)')),
     r"Cada hora más suma 35\,€: $m=35$; para 0 horas, $55-35=20$\,€: $n=20$. \ $\res{y=35x+20}$. \ $35\cdot6+20=\res{230\text{ €}}$. \ $35x+20=300\Rightarrow x=\res{8\text{ h}}$."),
 (2, r"Para pasar de grados Celsius ($x$) a grados Fahrenheit ($y$) se usa la fórmula $y=1{,}8x+32$. ¿A cuántos $^\circ$F equivalen 0\,$^\circ$C, 25\,$^\circ$C y 100\,$^\circ$C? ¿A cuántos $^\circ$C equivalen 50\,$^\circ$F?",
     r"$\res{32\ ^\circ\text{F}}$, \ $1{,}8\cdot25+32=\res{77\ ^\circ\text{F}}$, \ $\res{212\ ^\circ\text{F}}$. \ $1{,}8x+32=50\Rightarrow1{,}8x=18\Rightarrow x=\res{10\ ^\circ\text{C}}$."),
 (2, r"Un aparcamiento cobra 3\,€ por entrar y 2\,€ por cada hora. Escribe la fórmula y haz una tabla para 1, 2, 3, 4 y 5 horas. ¿Cuántas horas hemos dejado allí el coche si pagamos 19\,€?",
     r"$\res{y=2x+3}$ \quad " + tv([1, 2, 3, 4, 5], [PK(k) for k in range(1, 6)], 'h', '€') + r" \quad $2x+3=19\Rightarrow x=\res{8\text{ h}}$."),
 (3, r"Para alquilar una furgoneta, la empresa A cobra 30\,€ más 0,25\,€ por km y la empresa B, 50\,€ más 0,15\,€ por km. ¿Cuál conviene si hacemos 150\,km? ¿Para cuántos km cuestan lo mismo? Haz la gráfica de las dos.",
     r"A: $y=0{,}25x+30$; \ B: $y=0{,}15x+50$. \ Para 150\,km: A $=67{,}50$\,€, B $=72{,}50$\,€: conviene la \rest{A}. Cada km, A cobra 0,10\,€ más, pero empieza 20\,€ por debajo: cuestan lo mismo cuando $0{,}10x=20$, \ $x=\res{200\text{ km}}$ (80\,€)." + center(F79)),
 (3, r"El gimnasio A cobra 45\,€ de matrícula y 20\,€ al mes; el gimnasio B no tiene matrícula y cobra 35\,€ al mes. Haz la gráfica de las dos tarifas. ¿Cuándo cuestan lo mismo? ¿Cuál conviene si quieres ir 6 meses?",
     r"A: $y=20x+45$; \ B: $y=35x$. \ Cuestan lo mismo a los $\res{3\text{ meses}}$ (105\,€). Para 6 meses: A $=165$\,€ y B $=210$\,€: conviene el \rest{A}." + center(F710)),
]))
CHK(GA_(6) == 165 and GB_(6) == 210)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\definecolor{violet}{HTML}{7C6CF0}\n'
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TIT = "Gráficas de funciones"

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 9: %s' % (t, TIT), capcalera='%s · Unidad 9' % t,
                 pdfkeywords='coordenadas cartesianas, ejes, cuadrantes, abscisa, ordenada, planos, desplazamientos, simetrías, tablas de valores, gráficas, funciones, crecimiento, máximos y mínimos, proporcionalidad directa, pendiente, función lineal, ordenada en el origen',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 9' if sol else 'Ficha de ejercicios · Unidad 9') + '}{' + TIT + '}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás un plano cartesiano para situar puntos y herramientas para pasar de la tabla a la gráfica y para explorar las rectas $y=mx+n$."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Para dibujar puntos, rectas y gráficas usa papel cuadriculado y escribe siempre el nombre y la unidad de cada eje.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't9-fitxa-solucions-es.tex' if sol else 't9-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios,', NCHK[0], 'comprobaciones')
