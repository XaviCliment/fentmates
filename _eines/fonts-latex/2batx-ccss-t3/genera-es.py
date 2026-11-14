# Versió en castellà de genera.py. Genera t3-fitxa-exercicis.tex i t3-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 3: Programació lineal)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les
# estrelles no es mostren. Els exercicis marcats amb \pau{...} són de la PAU de la Comunitat Valenciana.
# Les gràfiques (TikZ) es calculen amb aritmètica exacta (fractions) i, al final, CHK comprova tots els vèrtexs i
# tots els òptims que apareixen a les solucions.
# Ús: python3 genera.py && pdflatex t3-fitxa-exercicis.tex (dues vegades) && pdflatex t3-fitxa-solucions.tex
import os, re, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def dm(s): return r'\[' + s + r'\]'
def sist(*rows):
    return r'\left\{\begin{aligned}' + r'\\'.join(rows) + r'\end{aligned}\right.'

# ---------- nombres i punts ----------
def fr(x): return x if isinstance(x, F) else F(str(x))
def tn(x):
    x = fr(x)
    if x.denominator == 1: return str(x.numerator)
    d = x.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    if d == 1 and x.denominator <= 100:
        return ('%g' % float(x)).replace('.', '{,}')
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)
def pt(p):
    a, b = tn(p[0]), tn(p[1])
    return '(%s;\\ %s)' % (a, b) if ('{,}' in a + b or 'frac' in a + b) else '(%s,\\,%s)' % (a, b)

# ---------- geometria exacta ----------
BIG = F(10 ** 6)
def clip(P, a, b, c, s):
    out, n = [], len(P)
    if n == 0: return out
    val = lambda p: s * (a * p[0] + b * p[1] - c)
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
def C(a, b, op, c): return (fr(a), fr(b), op, fr(c))
def region(cons, box):
    x0, x1, y0, y1 = [fr(v) for v in box]
    P = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for a, b, op, c in cons:
        if op in ('<=', '<', '='): P = clip(P, a, b, c, 1)
        if op in ('>=', '>', '='): P = clip(P, a, b, c, -1)
    return P
def verts(cons):
    P = region(cons, (-BIG, BIG, -BIG, BIG))
    return [p for p in P if abs(p[0]) < BIG and abs(p[1]) < BIG], all(abs(p[0]) < BIG and abs(p[1]) < BIG for p in P), P
def optim(cons, p, q, goal):
    V, bounded, P = verts(cons)
    sg = 1 if goal == 'max' else -1
    vals = [fr(p) * v[0] + fr(q) * v[1] for v in V]
    best = max(vals, key=lambda v: sg * v)
    if any(sg * (fr(p) * h[0] + fr(q) * h[1] - best) > 0 for h in P if not (abs(h[0]) < BIG and abs(h[1]) < BIG)):
        return None, []
    return best, sorted(v for v, f in zip(V, vals) if f == best)

# ---------- gràfiques TikZ ----------
COL = ['accent', 'blue!70!black', 'violet', 'orange!85!black', 'teal', 'magenta!80!black']
def nice(r):
    e = 10 ** math.floor(math.log10(r / 5)); m = r / 5 / e
    return e * (1 if m < 1.5 else 2 if m < 3.5 else 5 if m < 7.5 else 10)
def fig(cons, view, w=5.0, hmax=4.6, labels=True, test=None, level=None, opt=(), seg=None, draw_axes_cons=False, shade=True):
    x0, x1, y0, y1 = view
    sx = w / (x1 - x0); sy = min(sx, hmax / (y1 - y0))
    st = nice(x1 - x0); sty = nice(y1 - y0)
    s = r'\begin{tikzpicture}[x=%.4fcm,y=%.4fcm,baseline=(current bounding box.center)]' % (sx, sy)
    s += r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1)
    s += r'\foreach \i in {%s,%s,...,%s} \draw[muted!25,very thin] (\i,%s)--(\i,%s);' % (math.ceil(x0 / st) * st, math.ceil(x0 / st) * st + st, x1, y0, y1)
    s += r'\foreach \i in {%s,%s,...,%s} \draw[muted!25,very thin] (%s,\i)--(%s,\i);' % (math.ceil(y0 / sty) * sty, math.ceil(y0 / sty) * sty + sty, y1, x0, x1)
    if shade:
        R = region(cons, view)
        if len(R) >= 3: s += r'\fill[teal!22] ' + '--'.join('(%.4f,%.4f)' % (float(a), float(b)) for a, b in R) + '--cycle;'
        elif len(R) == 2: s += r'\draw[teal!45,line width=4pt] (%.4f,%.4f)--(%.4f,%.4f);' % (float(R[0][0]), float(R[0][1]), float(R[1][0]), float(R[1][1]))
    s += r'\end{scope}'
    s += r'\draw[-latex,thick] (%s,0)--(%s,0) node[below left=-1pt,font=\scriptsize]{$x$};' % (x0, x1 + 0.25 * st) if y0 <= 0 <= y1 else ''
    s += r'\draw[-latex,thick] (0,%s)--(0,%s) node[below left=-1pt,font=\scriptsize]{$y$};' % (y0, y1 + 0.25 * sty) if x0 <= 0 <= x1 else ''
    t = math.ceil(x0 / st) * st
    while t <= x1 + 1e-9:
        if abs(t) > 1e-9 and y0 <= 0 <= y1: s += r'\node[below,font=\tiny,text=muted] at (%s,0) {$%s$};' % (t, ('%g' % t).replace('.', '{,}'))
        t += st
    t = math.ceil(y0 / sty) * sty
    while t <= y1 + 1e-9:
        if abs(t) > 1e-9 and x0 <= 0 <= x1: s += r'\node[left,font=\tiny,text=muted] at (0,%s) {$%s$};' % (t, ('%g' % t).replace('.', '{,}'))
        t += sty
    s += r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1)
    k = 0
    for a, b, op, c in cons:
        if not draw_axes_cons and c == 0 and op == '>=' and (a, b) in ((1, 0), (0, 1)): continue
        a_, b_, c_ = float(a), float(b), float(c)
        if abs(b_) > abs(a_): P = [(x0 - 1, (c_ - a_ * (x0 - 1)) / b_), (x1 + 1, (c_ - a_ * (x1 + 1)) / b_)]
        else: P = [((c_ - b_ * (y0 - 1)) / a_, y0 - 1), ((c_ - b_ * (y1 + 1)) / a_, y1 + 1)]
        dash = ',dashed' if op in ('<', '>') else ''
        s += r'\draw[%s,line width=1.1pt%s] (%.4f,%.4f)--(%.4f,%.4f);' % (COL[k % len(COL)], dash, P[0][0], P[0][1], P[1][0], P[1][1])
        k += 1
    if level is not None:
        p, q, v = [float(z) for z in level]
        if abs(q) > abs(p): P = [(x0 - 1, (v - p * (x0 - 1)) / q), (x1 + 1, (v - p * (x1 + 1)) / q)]
        else: P = [((v - q * (y0 - 1)) / p, y0 - 1), ((v - q * (y1 + 1)) / p, y1 + 1)]
        s += r'\draw[navy,thick,densely dashed] (%.4f,%.4f)--(%.4f,%.4f);' % (P[0][0], P[0][1], P[1][0], P[1][1])
    if seg:
        s += r'\draw[accent,line width=3pt] (%.4f,%.4f)--(%.4f,%.4f);' % (float(seg[0][0]), float(seg[0][1]), float(seg[1][0]), float(seg[1][1]))
    s += r'\end{scope}'
    if labels:
        V, _, _ = verts(cons)
        if V:
            cx = sum(float(v[0]) for v in V) / len(V); cy = sum(float(v[1]) for v in V) / len(V)
            for v in V:
                vx, vy = float(v[0]), float(v[1])
                if not (x0 <= vx <= x1 and y0 <= vy <= y1): continue
                big = v in opt
                s += (r'\fill[accent] (%.4f,%.4f) circle (2.3pt);' if big else r'\filldraw[fill=white,draw=navy] (%.4f,%.4f) circle (1.5pt);') % (vx, vy)
                dx, dy = (vx - cx) * sx, (vy - cy) * sy
                ang = math.degrees(math.atan2(dy, dx)) if abs(dx) + abs(dy) > 1e-6 else 45
                s += r'\node[font=\tiny,inner sep=1.5pt,fill=white,fill opacity=.75,text opacity=1] at ($(%.4f,%.4f)+(%.1f:0.36cm)$) {$%s$};' % (vx, vy, ang, pt(v).replace('\\ ', ''))
    if test is not None:
        p, ok = test
        s += r'\fill[%s] (%s,%s) circle (2.2pt);' % ('teal' if ok else 'red!70!black', p[0], p[1])
    s += r'\end{tikzpicture}'
    return s

# ---------- dades de les gràfiques i comprovacions ----------
CHK = []   # (restriccions, vèrtexs esperats)  i  (restriccions, p, q, objectiu, valor esperat, punts esperats)
def reg(cons, expect):
    CHK.append(('v', cons, expect)); return cons
def opt(cons, p, q, goal, val, pts):
    CHK.append(('o', cons, p, q, goal, val, pts)); return pts
NN = [C(1, 0, '>=', 0), C(0, 1, '>=', 0)]

# regions que es fan servir en diversos exercicis
R6a = reg([C(1, 1, '<=', 5), C(1, -1, '>=', -1)] + NN, [(0, 0), (5, 0), (2, 3), (0, 1)])
R6b = reg([C(2, 1, '>=', 4), C(1, 2, '>=', 5)] + NN, [(0, 4), (1, 2), (5, 0)])
R7 = reg([C(1, 0, '>=', 1), C(1, 0, '<=', 4), C(0, 1, '>=', 0), C(0, 1, '<=', 3), C(1, 1, '<=', 6)], [(1, 0), (4, 0), (4, 2), (3, 3), (1, 3)])
R8a = reg([C(1, 1, '>=', 2), C(1, 1, '<=', 1)] + NN, [])
R8b = reg([C(-1, 1, '>=', 0), C(-1, 1, '<=', 2), C(1, 0, '>=', 0), C(1, 0, '<=', 3)], [(0, 0), (3, 3), (3, 5), (0, 2)])
R9 = reg([C(-2, 1, '<=', 0), C(1, 1, '<=', 6), C(0, 1, '>=', 0)], [(0, 0), (6, 0), (2, 4)])
R10 = reg([C(1, 2, '<=', 8), C(3, 1, '<=', 9)] + NN, [(0, 0), (3, 0), (2, 3), (0, 4)])
R11 = reg([C(1, 0, '>=', 1), C(0, 1, '>=', 2), C(1, 1, '>=', 5)], [(1, 4), (3, 2)])
RFUS = reg([C(3, 1, '<=', 60), C(1, 1, '<=', 30)] + NN, [(0, 0), (20, 0), (15, 15), (0, 30)])
RDIE = reg([C(2, 1, '>=', 8), C(1, 3, '>=', 9)] + NN, [(0, 8), (3, 2), (9, 0)])
RINV = reg([C(1, 1, '<=', 30), C(1, 0, '>=', 10), C(-1, 1, '<=', 0), C(0, 1, '>=', 0)], [(10, 0), (30, 0), (15, 15), (10, 10)])
RTRA = reg([C(1, 0, '>=', 0), C(1, 0, '<=', 20), C(0, 1, '>=', 0), C(0, 1, '<=', 25), C(1, 1, '<=', 30), C(1, 1, '>=', 20)], [(0, 20), (0, 25), (5, 25), (20, 10), (20, 0)])
RP81 = reg([C(2, 1, '>=', 8), C(1, 1, '>=', 6), C(1, 2, '>=', 10)] + NN, [(0, 8), (2, 4), (10, 0)])
RP80 = reg([C(1, 1, '<=', 5), C(2, 1, '<=', 8)] + NN, [(0, 0), (4, 0), (3, 2), (0, 5)])
RP79 = reg([C(1, 1, '<=', 10000), C(0, 1, '>=', 2000), C(1, 0, '<=', 6000), C(1, -1, '>=', 0)], [(2000, 2000), (6000, 2000), (6000, 4000), (5000, 5000)])
RP76 = reg([C(2, 1, '>=', 4), C(3, 10, '>=', 23), C(1, 12, '>=', 12)] + NN, [(0, 4), (1, 2), (6, F(1, 2)), (12, 0)])
RP17 = reg([C(4, -1, '>=', 0), C(5, 8, '<=', 74), C(3, -10, '<=', 0)], [(0, 0), (2, 8), (10, 3)])
RBUI = reg([C(1, 1, '<=', 10), C(2, 3, '>=', 40)] + NN, [])

def cell(v, mark=False): return r'\textbf{%s}' % v if mark else v
def taula(V, fname, fexpr, vals, best=()):
    rows = ''.join(r'$%s$ & $%s$%s\\' % (pt(v), tn(f), r' \ $\leftarrow$' if v in best else '') for v, f in zip(V, vals))
    return r'\begin{center}\small\begin{tabular}{cc}\hline Vértice & $%s=%s$\\\hline %s\hline\end{tabular}\end{center}' % (fname, fexpr, rows)
def avalua(cons, p, q, V, fname, fexpr, best):
    return taula(V, fname, fexpr, [fr(p) * v[0] + fr(q) * v[1] for v in V], best)

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Inecuaciones lineales con dos incógnitas", [
 (1, r"Averigua cuáles de los puntos siguientes son solución de la inecuación $3x-2y\leq4$:" + tasks(4, [r'$(0,\,0)$', r'$(2,\,1)$', r'$(-1,\,3)$', r'$(4,\,-2)$'])
     + recorda(r"Un punto $(x_0,y_0)$ es solución si, al sustituirlo, la desigualdad es cierta."),
     tasks(2, [r"$0\leq4$: \rest{sí}", r"$6-2=4\leq4$: \rest{sí} (es de la recta frontera)", r"$-3-6=-9\leq4$: \rest{sí}", r"$12+4=16\not\leq4$: \rest{no}"])),
 (1, r"Resuelve gráficamente las inecuaciones siguientes:" + tasks(4, [r'$x+y\leq4$', r'$2x-y>2$', r'$y\geq3x$', r'$x-3y<6$'])
     + recorda(r"1) Dibuja la recta frontera: continua si es $\leq,\geq$ y discontinua si es $<,>$. \ 2) Elige un punto de prueba que no sea de la recta (normalmente $(0,\,0)$). \ 3) Si lo cumple, la solución es el semiplano que lo contiene; si no, el otro."),
     tasks(2, [r"Recta por $(4,\,0)$ y $(0,\,4)$; \ $(0,\,0)$: $0\leq4$ \checkmark. Semiplano del origen, recta continua.\par" + fig([C(1, 1, '<=', 4)], (-2, 6, -2, 6), w=3.8, labels=False, test=((0, 0), True)),
               r"Recta por $(1,\,0)$ y $(0,\,-2)$; \ $(0,\,0)$: $0>2$ \texttimes. Semiplano que no contiene el origen, recta discontinua.\par" + fig([C(2, -1, '>', 2)], (-2, 5, -4, 4), w=3.8, labels=False, test=((0, 0), False)),
               r"Recta $y=3x$, que pasa por el origen; con $(1,\,0)$: $0\geq3$ \texttimes. Semiplano por encima de la recta.\par" + fig([C(-3, 1, '>=', 0)], (-3, 3, -3, 5), w=3.8, labels=False, test=((1, 0), False)),
               r"Recta por $(6,\,0)$ y $(0,\,-2)$; \ $(0,\,0)$: $0<6$ \checkmark. Semiplano del origen, recta discontinua.\par" + fig([C(1, -3, '<', 6)], (-2, 8, -4, 3), w=3.8, labels=False, test=((0, 0), True))])),
 (1, r"Resuelve gráficamente las inecuaciones siguientes, en las que solo aparece una de las incógnitas:" + tasks(4, [r'$x\geq-2$', r'$y<3$', r'$2x\leq5$', r'$-y\geq1$'])
     + recorda(r"La recta $x=k$ es \textbf{vertical} e $y=k$ es \textbf{horizontal}. \ $x\geq k$: a la derecha; \ $x\leq k$: a la izquierda; \ $y\geq k$: por encima; \ $y\leq k$: por debajo. No hace falta punto de prueba."),
     tasks(2, [r"Semiplano a la \rest{derecha} de la recta vertical $x=-2$ (continua).\par" + fig([C(1, 0, '>=', -2)], (-4, 3, -3, 3), w=3.4, labels=False, draw_axes_cons=True),
               r"Semiplano \rest{por debajo} de la recta horizontal $y=3$ (discontinua).\par" + fig([C(0, 1, '<', 3)], (-3, 3, -2, 5), w=3.4, labels=False, draw_axes_cons=True),
               r"$x\leq2{,}5$: semiplano a la \rest{izquierda} de $x=2{,}5$ (continua).\par" + fig([C(1, 0, '<=', F(5, 2))], (-2, 4, -3, 3), w=3.4, labels=False, draw_axes_cons=True),
               r"Multiplicamos por $-1$ y \textbf{cambia el sentido}: $y\leq-1$. Semiplano \rest{por debajo} de $y=-1$.\par" + fig([C(0, 1, '<=', -1)], (-3, 3, -4, 2), w=3.4, labels=False, draw_axes_cons=True)])),
 (2, r"Escribe la inecuación que tiene como solución cada semiplano sombreado:" + tasks(2, [fig([C(1, 2, '<=', 4)], (-2, 6, -2, 4), w=4.2, labels=False), fig([C(2, -1, '<', 1)], (-2, 4, -3, 5), w=4.2, labels=False)])
     + recorda(r"Halla la ecuación de la recta a partir de dos puntos y decide el signo con un punto de la zona sombreada."),
     tasks(2, [r"Recta por $(0,\,2)$ y $(4,\,0)$: $x+2y=4$. El origen es de la zona sombreada y la recta es continua: \ $\res{x+2y\leq4}$",
               r"Recta por $(0,\,-1)$ y $(2,\,3)$: $y=2x-1$. El origen es de la zona sombreada ($0>-1$) y la recta es discontinua: \ $\res{y>2x-1}$, es decir, $2x-y<1$"])),
 (2, r"Expresa cada frase con una inecuación y represéntala gráficamente ($x$ e $y$ son dos números reales):" + tasks(1, [r"El doble de un número más el triple de otro no supera 12.", r"La diferencia entre el primer número y el segundo es, como mínimo, 2."]),
     tasks(2, [r"$\res{2x+3y\leq12}$. Recta por $(6,\,0)$ y $(0,\,4)$; semiplano del origen.\par" + fig([C(2, 3, '<=', 12)], (-2, 8, -2, 6), w=3.8, labels=False, test=((0, 0), True)),
               r"$\res{x-y\geq2}$. Recta por $(2,\,0)$ y $(0,\,-2)$; $(0,\,0)$ no la cumple: semiplano de abajo.\par" + fig([C(1, -1, '>=', 2)], (-2, 6, -4, 4), w=3.8, labels=False, test=((0, 0), False))])),
]))

S.append(("Sistemas de inecuaciones. Región factible y vértices", [
 (1, r"Resuelve gráficamente los sistemas siguientes y calcula los vértices de la región solución. Indica si es acotada o no:" + tasks(2, [r'$' + sist(r'x+y&\leq5', r'x-y&\geq-1', r'x\geq0,\ y&\geq0') + r'$', r'$' + sist(r'2x+y&\geq4', r'x+2y&\geq5', r'x\geq0,\ y&\geq0') + r'$'])
     + recorda(r"La solución es la zona común a todos los semiplanos. Los vértices son los puntos de corte de dos rectas frontera que cumplen \textbf{todas} las inecuaciones."),
     tasks(2, [r"\rest{Acotada}. Vértices: $\res{(0,\,0),\ (5,\,0),\ (2,\,3),\ (0,\,1)}$; \ $(2,\,3)$ es el corte de $x+y=5$ y $x-y=-1$.\par" + fig(R6a, (-1, 6.5, -1, 5.5), w=4.4),
               r"\rest{No acotada}. Vértices: $\res{(0,\,4),\ (1,\,2),\ (5,\,0)}$; \ $(1,\,2)$ es el corte de $2x+y=4$ y $x+2y=5$.\par" + fig(R6b, (-1, 7, -1, 6), w=4.4)])),
 (1, r"Representa la región definida por las inecuaciones siguientes y calcula sus vértices:" + dm(r'1\leq x\leq4,\qquad 0\leq y\leq3,\qquad x+y\leq6')
     + recorda(r"Una doble desigualdad $a\leq x\leq b$ son dos inecuaciones: $x\geq a$ y $x\leq b$ (una franja vertical)."),
     r"Es la franja $1\leq x\leq4$, $0\leq y\leq3$, recortada por la recta $x+y=6$. Vértices: $\res{(1,\,0),\ (4,\,0),\ (4,\,2),\ (3,\,3),\ (1,\,3)}$. El punto $(4,\,3)$ no es vértice porque $4+3>6$." + '\n\n\\begin{center}' + fig(R7, (-0.5, 6.5, -1, 4.5), w=5) + '\\end{center}'),
 (2, r"Resuelve gráficamente los sistemas siguientes:" + tasks(2, [r'$' + sist(r'x+y&\geq2', r'x+y&\leq1', r'x\geq0,\ y&\geq0') + r'$', r'$' + sist(r'y&\geq x', r'y&\leq x+2', r'0\leq x&\leq3') + r'$']),
     tasks(2, [r"Las rectas $x+y=2$ y $x+y=1$ son paralelas y ningún punto puede cumplir las dos inecuaciones: la región es \rest{vacía}, el sistema \rest{no tiene solución}.",
               r"Franja entre dos rectas paralelas, cortada por $x=0$ y $x=3$: un paralelogramo de vértices $\res{(0,\,0),\ (3,\,3),\ (3,\,5),\ (0,\,2)}$.\par" + fig(R8b, (-1, 4.5, -1, 6), w=3.6)])),
 (2, r"Escribe el sistema de inecuaciones que tiene como solución la región sombreada:" + '\n\n\\begin{center}' + fig(R9, (-1, 7, -1, 5.5), w=5) + '\\end{center}',
     r"La recta que pasa por $(0,\,0)$ y $(2,\,4)$ es $y=2x$; la que pasa por $(2,\,4)$ y $(6,\,0)$ es $x+y=6$. Con puntos del interior, como $(3,\,1)$, decidimos el sentido: \ $\res{y\leq2x,\quad x+y\leq6,\quad y\geq0}$."),
 (2, r"Considera el sistema $\ x+2y\leq8,\ \ 3x+y\leq9,\ \ x\geq0,\ \ y\geq0$." + tasks(1, [r"Averigua si los puntos $(1,\,2)$, $(2,\,3)$ y $(3,\,1)$ pertenecen a la región factible.", r"Representa la región y calcula sus vértices."]),
     tasks(1, [r"$(1,\,2)$: $5\leq8$ y $5\leq9$: \rest{sí}. \ $(2,\,3)$: $8\leq8$ y $9\leq9$: \rest{sí} (es un vértice). \ $(3,\,1)$: $5\leq8$, pero $10>9$: \rest{no}.",
               r"Vértices: $\res{(0,\,0),\ (3,\,0),\ (2,\,3),\ (0,\,4)}$.\par" + fig(R10, (-1, 5.5, -1, 5.5), w=4)])),
 (2, r"Representa la región definida por $\ x\geq1,\ \ y\geq2,\ \ x+y\geq5\ $. ¿Es acotada? Calcula sus vértices.",
     r"Es \rest{no acotada} (se extiende hacia arriba y hacia la derecha). Vértices: $\res{(1,\,4)}$ y $\res{(3,\,2)}$. El punto $(1,\,2)$, corte de $x=1$ e $y=2$, no es vértice porque $1+2<5$." + '\n\n\\begin{center}' + fig(R11, (-0.5, 6, -0.5, 7), w=4.2) + '\\end{center}'),
]))

S.append(("Optimización de una función objetivo sobre una región", [
 (1, r"Calcula el máximo y el mínimo de la función $f(x,y)=3x+2y$ en la región del apartado a) del ejercicio 6."
     + recorda(r"Si la región es acotada, el máximo y el mínimo se alcanzan en vértices: evalúa la función en todos."),
     avalua(R6a, 3, 2, [(0, 0), (5, 0), (2, 3), (0, 1)], 'f', '3x+2y', opt(R6a, 3, 2, 'max', 15, [(5, 0)]) + opt(R6a, 3, 2, 'min', 0, [(0, 0)]))
     + r"Máximo: $\res{15}$ en $(5,\,0)$. \ Mínimo: $\res{0}$ en $(0,\,0)$."),
 (1, r"La región factible de un problema es el polígono de vértices $A(0,\,0)$, $B(6,\,0)$, $C(5,\,3)$, $D(2,\,5)$ y $E(0,\,4)$. Halla el máximo y el mínimo de las funciones $f(x,y)=x+2y$ y $g(x,y)=2x-y$ en esta región.",
     r"\begin{center}\small\begin{tabular}{ccc}\hline Vértice & $f=x+2y$ & $g=2x-y$\\\hline $A(0,\,0)$&0&0\\ $B(6,\,0)$&6&12\\ $C(5,\,3)$&11&7\\ $D(2,\,5)$&12&$-1$\\ $E(0,\,4)$&8&$-4$\\\hline\end{tabular}\end{center}"
     r"$f$: máximo $\res{12}$ en $D$ y mínimo $\res{0}$ en $A$. \ $g$: máximo $\res{12}$ en $B$ y mínimo $\res{-4}$ en $E$."),
 (2, r"Calcula, si existen, el máximo y el mínimo de $f(x,y)=4x+3y$ en la región del apartado b) del ejercicio 6."
     + recorda(r"Si la región no es acotada, puede que no haya máximo (o mínimo). Compruébalo con las rectas de nivel $4x+3y=k$."),
     avalua(R6b, 4, 3, [(0, 4), (1, 2), (5, 0)], 'f', '4x+3y', opt(R6b, 4, 3, 'min', 10, [(1, 2)]))
     + r"Mínimo: $\res{10}$ en $(1,\,2)$. \ La región se extiende indefinidamente hacia arriba y hacia la derecha y $f$ crece en ella sin límite: \rest{no tiene máximo}." + '\n\n\\begin{center}' + fig(R6b, (-1, 7, -1, 6), w=4.2, level=(4, 3, 10), opt=[(1, 2)]) + '\\end{center}'),
 (2, r"Resuelve el problema anterior gráficamente con rectas de nivel: dibuja la recta $4x+3y=0$ y desplázala paralelamente. ¿Cuál es el primer vértice de la región que toca?",
     r"Las rectas de nivel $4x+3y=k$ son paralelas a $4x+3y=0$; al aumentar $k$ se desplazan hacia arriba y a la derecha. El primer punto de la región que tocan es $\res{(1,\,2)}$, con $k=10$ (el mínimo). No hay un último: no hay máximo."),
]))

S.append(("Problemas de programación lineal", [
 (1, r"Una carpintería fabrica mesas y sillas. Cada mesa necesita 3 horas de montaje y 1 hora de acabado, y cada silla, 1 hora de montaje y 1 hora de acabado. Cada semana se dispone de 60 horas de montaje y 30 horas de acabado. El beneficio es de 40 € por mesa y de 20 € por silla. ¿Cuántas mesas y cuántas sillas hay que fabricar para obtener el máximo beneficio?"
     + recorda(r"Pasos: variables (tabla de datos) $\to$ función objetivo $\to$ restricciones $\to$ región factible $\to$ vértices $\to$ evaluación $\to$ respuesta."),
     r"$x$ = mesas, $y$ = sillas. \ $\max\ B(x,y)=40x+20y$ \ con \ $3x+y\leq60$, \ $x+y\leq30$, \ $x,y\geq0$." + '\n\n\\begin{center}' + fig(RFUS, (-3, 35, -3, 35), w=4.4, level=(40, 20, 900), opt=[(15, 15)]) + '\\end{center}'
     + avalua(RFUS, 40, 20, [(0, 0), (20, 0), (15, 15), (0, 30)], 'B', '40x+20y', opt(RFUS, 40, 20, 'max', 900, [(15, 15)]))
     + r"Hay que fabricar \rest{15 mesas y 15 sillas}; beneficio máximo $\res{900\text{ €}}$."),
 (2, r"Un ganadero quiere mezclar dos piensos, P y Q. Cada kg de P aporta 2 unidades de vitamina A y 1 de vitamina B, y cada kg de Q, 1 unidad de A y 3 de B. Cada día el ganado necesita al menos 8 unidades de A y 9 de B. Si el kg de P cuesta 3 € y el de Q, 2 €, ¿cuántos kg de cada pienso debe comprar para que el coste sea mínimo?",
     r"$x$ = kg de P, $y$ = kg de Q. \ $\min\ C(x,y)=3x+2y$ \ con \ $2x+y\geq8$, \ $x+3y\geq9$, \ $x,y\geq0$. La región \textbf{no es acotada}." + '\n\n\\begin{center}' + fig(RDIE, (-1, 11, -1, 10), w=4.4, level=(3, 2, 13), opt=[(3, 2)]) + '\\end{center}'
     + avalua(RDIE, 3, 2, [(0, 8), (3, 2), (9, 0)], 'C', '3x+2y', opt(RDIE, 3, 2, 'min', 13, [(3, 2)]))
     + r"Como los coeficientes son positivos, alejarse del origen solo encarece el coste: el mínimo existe. Hay que comprar \rest{3 kg de P y 2 kg de Q}; coste mínimo $\res{13\text{ €}}$."),
 (2, r"Una persona dispone de 30\,000 € para invertir en dos fondos, A y B, con rentabilidades anuales del 4\,\% y del 6\,\%. Quiere poner al menos 10\,000 € en A y no quiere invertir en B (más arriesgado) más de lo que invierte en A. ¿Cómo debe repartir el dinero para obtener el máximo rendimiento?",
     r"$x$, $y$ = miles de euros en A y en B. Cada millar rinde 40 € en A y 60 € en B: \ $\max\ R(x,y)=40x+60y$ \ con \ $x+y\leq30$, \ $x\geq10$, \ $y\leq x$, \ $y\geq0$." + '\n\n\\begin{center}' + fig(RINV, (-2, 34, -2, 20), w=4.6, level=(40, 60, 1500), opt=[(15, 15)]) + '\\end{center}'
     + avalua(RINV, 40, 60, [(10, 0), (30, 0), (15, 15), (10, 10)], 'R', '40x+60y', opt(RINV, 40, 60, 'max', 1500, [(15, 15)]))
     + r"Debe invertir \rest{15\,000 € en A y 15\,000 € en B}; rendimiento máximo $\res{1500\text{ €}}$."),
 (3, r"Una empresa tiene dos almacenes: M1, con 30 toneladas de producto, y M2, con 25 toneladas. Debe servir 20 toneladas a la tienda T1 y 25 a la tienda T2. El coste de transporte por tonelada (en euros) es:" + '\n\n'
     r"\begin{center}\small\begin{tabular}{c|cc}& T1 & T2\\\hline M1 & 5 & 3\\ M2 & 2 & 4\end{tabular}\end{center}"
     r"¿Cómo se debe organizar el transporte para que el coste sea mínimo? ¿Cuál es ese coste?",
     r"$x$ = toneladas de M1 a T1, $y$ = toneladas de M1 a T2; entonces M2 envía $20-x$ a T1 y $25-y$ a T2. \ Restricciones: $0\leq x\leq20$, $0\leq y\leq25$, \ $x+y\leq30$ (M1), \ $(20-x)+(25-y)\leq25\Leftrightarrow x+y\geq20$ (M2). \ Coste: $5x+3y+2(20-x)+4(25-y)=3x-y+140$." + '\n\n\\begin{center}' + fig(RTRA, (-2, 23, -2, 28), w=4.2, level=(3, -1, -25), opt=[(0, 25)]) + '\\end{center}'
     + avalua(RTRA, 3, -1, [(0, 20), (0, 25), (5, 25), (20, 10), (20, 0)], '3x-y', '', opt(RTRA, 3, -1, 'min', -25, [(0, 25)])).replace('$3x-y=$', '$3x-y$')
     + r"Mínimo de $3x-y$: $-25$ en $(0,\,25)$. M1 envía \rest{0 t a T1 y 25 t a T2} y M2 envía \rest{20 t a T1 y 0 t a T2}. Coste mínimo: $-25+140=\res{115\text{ €}}$."),
 (2, r"\pau{C. Valenciana, julio 2025} Una agencia de viajes organiza excursiones a la montaña y a la playa. La agencia obtiene 700 euros de beneficio por cada excursión a la montaña y 500 euros por cada excursión a la playa. Dispone de un total de 10 autobuses y 8 guías turísticos. Cada excursión a la montaña requiere 2 autobuses y 2 guías, mientras que cada excursión a la playa requiere 2 autobuses y 1 guía." + tasks(1, [r"¿Cuántas excursiones a la montaña y cuántas a la playa debe organizar para obtener el máximo beneficio posible?", r"¿Cuál es ese beneficio máximo?"]),
     r"$x$ = excursiones a la montaña, $y$ = a la playa. \ $\max\ B=700x+500y$ \ con \ $2x+2y\leq10$, \ $2x+y\leq8$, \ $x,y\geq0$." + '\n\n\\begin{center}' + fig(RP80, (-0.5, 6, -0.5, 6), w=3.8, level=(700, 500, 3100), opt=[(3, 2)]) + '\\end{center}'
     + avalua(RP80, 700, 500, [(0, 0), (4, 0), (3, 2), (0, 5)], 'B', '700x+500y', opt(RP80, 700, 500, 'max', 3100, [(3, 2)]))
     + tasks(2, [r"\rest{3 a la montaña y 2 a la playa}", r"$\res{3100\text{ €}}$"])),
 (2, r"\pau{C. Valenciana, junio 2025} Un creador de contenido desea invertir en publicidad hasta 10\,000 euros. Ha considerado dos empresas, A y B. La empresa A garantiza un incremento anual en número de seguidores del 10\,\% de lo que se invierte en ella, y la B, del 7\,\%. El creador quiere invertir al menos 2000 euros en la empresa B y un máximo de 6000 euros en la A, invirtiendo siempre en la A al menos lo que invierte en la B." + tasks(1, [r"¿Cuánto dinero debe asignar a cada empresa para que el incremento de seguidores sea máximo?", r"¿Cuál es ese incremento máximo?"]),
     r"$x$, $y$ = euros en A y en B. \ $\max\ S=0{,}1x+0{,}07y$ \ con \ $x+y\leq10\,000$, \ $y\geq2000$, \ $x\leq6000$, \ $x\geq y$." + '\n\n'
     + avalua(RP79, F(1, 10), F(7, 100), [(2000, 2000), (6000, 2000), (6000, 4000), (5000, 5000)], 'S', '0{,}1x+0{,}07y', opt(RP79, F(1, 10), F(7, 100), 'max', 880, [(6000, 4000)]))
     + tasks(2, [r"\rest{6000 € en A y 4000 € en B}", r"$\res{880}$ seguidores"])),
 (2, r"\pau{C. Valenciana, junio 2023} El veterinario me ha recomendado que mi perro tome diariamente un mínimo de 8 unidades de hidratos de carbono, 46 de proteínas y 12 de grasas. Una lata de la marca A contiene 4 unidades de hidratos, 6 de proteínas y 1 de grasas; una lata de la marca B, 2 unidades de hidratos, 20 de proteínas y 12 de grasas. La lata A cuesta 10 euros y la B, 16 euros." + tasks(1, [r"¿Cómo tendré que combinar las dos marcas para obtener la dieta deseada al precio mínimo?", r"¿Cuál es el precio mínimo que tendré que pagar?"]),
     r"$\min\ C=10x+16y$ \ con \ $4x+2y\geq8$, \ $6x+20y\geq46$, \ $x+12y\geq12$, \ $x,y\geq0$ (región no acotada)." + '\n\n\\begin{center}' + fig(RP76, (-1, 13, -0.5, 5), w=4.6, level=(10, 16, 42), opt=[(1, 2)]) + '\\end{center}'
     + avalua(RP76, 10, 16, [(0, 4), (1, 2), (6, F(1, 2)), (12, 0)], 'C', '10x+16y', opt(RP76, 10, 16, 'min', 42, [(1, 2)]))
     + tasks(2, [r"\rest{1 lata de A y 2 de B}", r"$\res{42\text{ €}}$"])),
 (2, r"\pau{C. Valenciana, junio 2026} Una granja quiere crear una mezcla fertilizante con dos compuestos, NutriMax y BioGrow. Se deben aplicar como mínimo 8 unidades de nitrógeno, 6 de fósforo y 10 de potasio. Un litro de NutriMax contiene 2 unidades de nitrógeno, 1 de fósforo y 1 de potasio, y un litro de BioGrow, 1 de nitrógeno, 1 de fósforo y 2 de potasio. El litro de NutriMax cuesta 5 euros y el de BioGrow, 4 euros." + tasks(1, [r"¿Cuántos litros de cada producto se deben utilizar para que el coste de la mezcla sea mínimo?", r"¿Cuál es ese coste mínimo?"]),
     r"$\min\ C=5x+4y$ \ con \ $2x+y\geq8$, \ $x+y\geq6$, \ $x+2y\geq10$, \ $x,y\geq0$. Las tres rectas pasan por $(2,\,4)$." + '\n\n'
     + avalua(RP81, 5, 4, [(0, 8), (2, 4), (10, 0)], 'C', '5x+4y', opt(RP81, 5, 4, 'min', 26, [(2, 4)]))
     + tasks(2, [r"\rest{2 litros de NutriMax y 4 de BioGrow}", r"$\res{26\text{ €}}$"])),
]))

S.append(("Casos especiales: infinitas soluciones y problemas sin solución", [
 (2, r"En la carpintería del ejercicio 16 cambian los precios y ahora el beneficio es de 30 € por mesa y 10 € por silla. ¿Qué producción da el máximo beneficio? ¿Es única?"
     + recorda(r"Si el óptimo se alcanza en dos vértices, se alcanza en todos los puntos del segmento que los une: ocurre cuando la función objetivo es paralela a un lado de la región."),
     avalua(RFUS, 30, 10, [(0, 0), (20, 0), (15, 15), (0, 30)], 'B', '30x+10y', opt(RFUS, 30, 10, 'max', 600, [(15, 15), (20, 0)]))
     + r"El máximo, $\res{600\text{ €}}$, se alcanza en $(20,\,0)$ y en $(15,\,15)$: $30x+10y=10(3x+y)$ es paralela a $3x+y=60$. Hay \rest{infinitas soluciones}: el segmento $y=60-3x$, $15\leq x\leq20$. Como se fabrican unidades enteras: $(15,\,15)$, $(16,\,12)$, $(17,\,9)$, $(18,\,6)$, $(19,\,3)$ y $(20,\,0)$." + '\n\n\\begin{center}' + fig(RFUS, (-3, 35, -3, 35), w=4.2, level=(30, 10, 600), opt=[(15, 15), (20, 0)], seg=((15, 15), (20, 0))) + '\\end{center}'),
 (2, r"En la región del ejercicio 17 (la de los piensos), estudia si existen el máximo y el mínimo de las funciones:" + tasks(2, [r'$f(x,y)=x+y$', r'$g(x,y)=2x+y$']),
     tasks(1, [r"$f$: $f(0,\,8)=8$, $f(3,\,2)=5$, $f(9,\,0)=9$. Mínimo $\res{5}$ en $(3,\,2)$; \rest{no tiene máximo} (la región no es acotada y $f$ crece en ella indefinidamente).",
               r"$g$: $g(0,\,8)=8$, $g(3,\,2)=8$, $g(9,\,0)=18$. El mínimo, $\res{8}$, se alcanza en \rest{todo el segmento} de extremos $(0,\,8)$ y $(3,\,2)$ ($g$ es paralela a $2x+y=8$). \rest{No tiene máximo}."])
     + "%s%s" % (opt(RDIE, 1, 1, 'min', 5, [(3, 2)]) and '', opt(RDIE, 2, 1, 'min', 8, [(0, 8), (3, 2)]) and '')),
 (2, r"Una empresa debe producir $x$ unidades de un producto A e $y$ de un producto B. Por capacidad, no puede fabricar más de 10 unidades en total, pero un contrato la obliga a cumplir $2x+3y\geq40$. Maximiza el beneficio $B(x,y)=3x+2y$.",
     r"Con $x+y\leq10$ y $x,y\geq0$, el valor más grande de $2x+3y$ es $3\cdot10=30<40$. Las restricciones son incompatibles: la región factible es \rest{vacía} y el problema \rest{no tiene solución}." + '\n\n\\begin{center}' + fig(RBUI, (-1, 22, -1, 15), w=4) + '\\end{center}'),
 (3, r"En la región del ejercicio 6a), halla los valores de $k$ para que la función $f(x,y)=kx+y$ alcance el máximo en infinitos puntos.",
     r"Es necesario que $f$ sea paralela a un lado en el que esté el máximo. Lado $x+y=5$ (de $(5,\,0)$ a $(2,\,3)$): $\res{k=1}$; entonces $f=x+y$ vale 5 en todo el lado y es el máximo. Lado $x-y=-1$ (de $(0,\,1)$ a $(2,\,3)$): $\res{k=-1}$; $f=y-x$ vale 1 en todo el lado y es el máximo (en $(0,\,0)$ vale 0 y en $(5,\,0)$, $-5$). Para los otros lados (ejes), $f=y$ y $f=x$ no tienen en ellos el máximo."
     + "%s%s" % (opt(R6a, 1, 1, 'max', 5, [(2, 3), (5, 0)]) and '', opt(R6a, -1, 1, 'max', 1, [(0, 1), (2, 3)]) and '')),
 (2, r"\pau{C. Valenciana, junio 1998} Considera el triángulo de vértices $(0,\,0)$, $(2,\,8)$ y $(10,\,3)$. Determina razonadamente:" + tasks(1, [r"El punto del triángulo en el que la función $f(x,y)=-4x+y+9$ toma el máximo.", r"El punto del triángulo en el que la función $g(x,y)=4x+y+12$ toma el máximo."]),
     tasks(1, [r"$f(0,\,0)=9$, $f(2,\,8)=9$, $f(10,\,3)=-28$. El máximo, $\res{9}$, se alcanza en \rest{todos los puntos del segmento} de extremos $(0,\,0)$ y $(2,\,8)$.",
               r"$g(0,\,0)=12$, $g(2,\,8)=28$, $g(10,\,3)=55$: máximo $\res{55}$ en $\res{(10,\,3)}$."])
     + "%s%s" % (opt(RP17, -4, 1, 'max', 0, [(0, 0), (2, 8)]) and '', opt(RP17, 4, 1, 'max', 43, [(10, 3)]) and '')),
 (1, r"Razona si son verdaderas o falsas las afirmaciones siguientes:" + tasks(1, [r"Si la región factible es acotada y no vacía, la función objetivo siempre tiene máximo y mínimo.", r"Si la región factible no es acotada, la función objetivo no tiene nunca mínimo.", r"El óptimo de una función objetivo no constante puede estar en un punto del interior de la región.", r"Si dos vértices dan el mismo valor máximo, el problema tiene infinitas soluciones."]),
     tasks(1, [r"\rest{Verdadera}: es el teorema fundamental, y se alcanzan en vértices.", r"\rest{Falsa}: en los problemas de dieta la región no es acotada y hay mínimo (ejercicio 17).", r"\rest{Falsa}: siempre se puede mejorar moviéndose en la dirección en la que crece (o decrece) la función, hasta llegar a la frontera.", r"\rest{Verdadera}: también es óptimo todo el segmento que los une."])),
]))

# ---------- comprovacions ----------
for c in CHK:
    if c[0] == 'v':
        V, _, _ = verts(c[1])
        assert sorted(V) == sorted((fr(a), fr(b)) for a, b in c[2]), (V, c[2])
    else:
        _, cons, p, q, goal, val, pts = c
        best, at = optim(cons, p, q, goal)
        assert best == fr(val) and at == sorted((fr(a), fr(b)) for a, b in pts), (p, q, goal, best, at)
# exercici del polígon (13) i transport: comprovacions directes
POL = [(0, 0), (6, 0), (5, 3), (2, 5), (0, 4)]
assert [x + 2 * y for x, y in POL] == [0, 6, 11, 12, 8] and [2 * x - y for x, y in POL] == [0, 12, 7, -1, -4]
assert 5 * 0 + 3 * 25 + 2 * 20 + 4 * 0 == 115 and 3 * 0 - 25 + 140 == 115
assert max(2 * x + 3 * y for x, y in [(0, 0), (10, 0), (0, 10)]) == 30 < 40

# =====================================================================
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre = pre.replace(r'\usepackage{tikz}', r'\usepackage{tikz}' + '\n' + r'\usetikzlibrary{calc}')
assert 'refstepcounter{exer}' in pre and 'usetikzlibrary{calc}' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Programación lineal"
KW = "programación lineal, inecuaciones, sistemas de inecuaciones, región factible, vértices, función objetivo, rectas de nivel, PAU"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 3: %s' % (t, TIT), capcalera='%s · Unidad 3: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 3' if sol else 'Ficha de ejercicios · Unidad 3') + '}{' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar las regiones factibles, los vértices y los óptimos con el resolutor de programación lineal de los apuntes interactivos de la unidad."
             if sol else r"Haz las gráficas con regla y papel cuadriculado, e indica siempre los vértices de la región. Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de la Comunidad Valenciana; encontrarás muchos más, resueltos, en la página de ejercicios PAU de la unidad.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            if sol:
                head = re.sub(r'(\\pau\{[^}]*\}).*', r'\1', q, flags=re.S) if q.startswith('\\pau{') else ''
                out.append('\\ex{%d} %s%s\n\n' % (st, head, s))
            else:
                out.append('\\ex{%d} %s\n\n' % (st, q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con el resolutor de los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't3-fitxa-solucions-es.tex' if sol else 't3-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'ejercicios,', npau, 'de la PAU de la Comunidad Valenciana;', len(CHK), 'comprobaciones correctas')
