# Genera t3-fitxa-exercicis.tex i t3-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 3: Programació lineal)
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
    return r'\begin{center}\small\begin{tabular}{cc}\hline Vèrtex & $%s=%s$\\\hline %s\hline\end{tabular}\end{center}' % (fname, fexpr, rows)
def avalua(cons, p, q, V, fname, fexpr, best):
    return taula(V, fname, fexpr, [fr(p) * v[0] + fr(q) * v[1] for v in V], best)

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Inequacions lineals amb dues incògnites", [
 (1, r"Esbrina quins dels punts següents són solució de la inequació $3x-2y\leq4$:" + tasks(4, [r'$(0,\,0)$', r'$(2,\,1)$', r'$(-1,\,3)$', r'$(4,\,-2)$'])
     + recorda(r"Un punt $(x_0,y_0)$ és solució si, en substituir-lo, la desigualtat és certa."),
     tasks(2, [r"$0\leq4$: \rest{sí}", r"$6-2=4\leq4$: \rest{sí} (és de la recta frontera)", r"$-3-6=-9\leq4$: \rest{sí}", r"$12+4=16\not\leq4$: \rest{no}"])),
 (1, r"Resol gràficament les inequacions següents:" + tasks(4, [r'$x+y\leq4$', r'$2x-y>2$', r'$y\geq3x$', r'$x-3y<6$'])
     + recorda(r"1) Dibuixa la recta frontera: contínua si és $\leq,\geq$ i discontínua si és $<,>$. \ 2) Tria un punt de prova que no siga de la recta (normalment $(0,\,0)$). \ 3) Si el compleix, la solució és el semipla que el conté; si no, l'altre."),
     tasks(2, [r"Recta per $(4,\,0)$ i $(0,\,4)$; \ $(0,\,0)$: $0\leq4$ \checkmark. Semipla de l'origen, recta contínua.\par" + fig([C(1, 1, '<=', 4)], (-2, 6, -2, 6), w=3.8, labels=False, test=((0, 0), True)),
               r"Recta per $(1,\,0)$ i $(0,\,-2)$; \ $(0,\,0)$: $0>2$ \texttimes. Semipla que no conté l'origen, recta discontínua.\par" + fig([C(2, -1, '>', 2)], (-2, 5, -4, 4), w=3.8, labels=False, test=((0, 0), False)),
               r"Recta $y=3x$, que passa per l'origen; amb $(1,\,0)$: $0\geq3$ \texttimes. Semipla de damunt de la recta.\par" + fig([C(-3, 1, '>=', 0)], (-3, 3, -3, 5), w=3.8, labels=False, test=((1, 0), False)),
               r"Recta per $(6,\,0)$ i $(0,\,-2)$; \ $(0,\,0)$: $0<6$ \checkmark. Semipla de l'origen, recta discontínua.\par" + fig([C(1, -3, '<', 6)], (-2, 8, -4, 3), w=3.8, labels=False, test=((0, 0), True))])),
 (1, r"Resol gràficament les inequacions següents, en les quals només apareix una de les incògnites:" + tasks(4, [r'$x\geq-2$', r'$y<3$', r'$2x\leq5$', r'$-y\geq1$'])
     + recorda(r"La recta $x=k$ és \textbf{vertical} i $y=k$ és \textbf{horitzontal}. \ $x\geq k$: a la dreta; \ $x\leq k$: a l'esquerra; \ $y\geq k$: per damunt; \ $y\leq k$: per davall. No cal punt de prova."),
     tasks(2, [r"Semipla a la \rest{dreta} de la recta vertical $x=-2$ (contínua).\par" + fig([C(1, 0, '>=', -2)], (-4, 3, -3, 3), w=3.4, labels=False, draw_axes_cons=True),
               r"Semipla \rest{per davall} de la recta horitzontal $y=3$ (discontínua).\par" + fig([C(0, 1, '<', 3)], (-3, 3, -2, 5), w=3.4, labels=False, draw_axes_cons=True),
               r"$x\leq2{,}5$: semipla a l'\rest{esquerra} de $x=2{,}5$ (contínua).\par" + fig([C(1, 0, '<=', F(5, 2))], (-2, 4, -3, 3), w=3.4, labels=False, draw_axes_cons=True),
               r"Multipliquem per $-1$ i \textbf{canvia el sentit}: $y\leq-1$. Semipla \rest{per davall} de $y=-1$.\par" + fig([C(0, 1, '<=', -1)], (-3, 3, -4, 2), w=3.4, labels=False, draw_axes_cons=True)])),
 (2, r"Escriu la inequació que té com a solució cada semipla ombrejat:" + tasks(2, [fig([C(1, 2, '<=', 4)], (-2, 6, -2, 4), w=4.2, labels=False), fig([C(2, -1, '<', 1)], (-2, 4, -3, 5), w=4.2, labels=False)])
     + recorda(r"Troba l'equació de la recta a partir de dos punts i decideix el signe amb un punt de l'ombrejat."),
     tasks(2, [r"Recta per $(0,\,2)$ i $(4,\,0)$: $x+2y=4$. L'origen és de l'ombrejat i la recta és contínua: \ $\res{x+2y\leq4}$",
               r"Recta per $(0,\,-1)$ i $(2,\,3)$: $y=2x-1$. L'origen és de l'ombrejat ($0>-1$) i la recta és discontínua: \ $\res{y>2x-1}$, és a dir, $2x-y<1$"])),
 (2, r"Expressa cada frase amb una inequació i representa-la gràficament ($x$ i $y$ són dos nombres reals):" + tasks(1, [r"El doble d'un nombre més el triple d'un altre no supera 12.", r"La diferència entre el primer nombre i el segon és, com a mínim, 2."]),
     tasks(2, [r"$\res{2x+3y\leq12}$. Recta per $(6,\,0)$ i $(0,\,4)$; semipla de l'origen.\par" + fig([C(2, 3, '<=', 12)], (-2, 8, -2, 6), w=3.8, labels=False, test=((0, 0), True)),
               r"$\res{x-y\geq2}$. Recta per $(2,\,0)$ i $(0,\,-2)$; $(0,\,0)$ no la compleix: semipla de davall.\par" + fig([C(1, -1, '>=', 2)], (-2, 6, -4, 4), w=3.8, labels=False, test=((0, 0), False))])),
]))

S.append(("Sistemes d'inequacions. Regió factible i vèrtexs", [
 (1, r"Resol gràficament els sistemes següents i calcula els vèrtexs de la regió solució. Indica si és acotada o no:" + tasks(2, [r'$' + sist(r'x+y&\leq5', r'x-y&\geq-1', r'x\geq0,\ y&\geq0') + r'$', r'$' + sist(r'2x+y&\geq4', r'x+2y&\geq5', r'x\geq0,\ y&\geq0') + r'$'])
     + recorda(r"La solució és la zona comuna a tots els semiplans. Els vèrtexs són els punts de tall de dues rectes frontera que compleixen \textbf{totes} les inequacions."),
     tasks(2, [r"\rest{Acotada}. Vèrtexs: $\res{(0,\,0),\ (5,\,0),\ (2,\,3),\ (0,\,1)}$; \ $(2,\,3)$ és el tall de $x+y=5$ i $x-y=-1$.\par" + fig(R6a, (-1, 6.5, -1, 5.5), w=4.4),
               r"\rest{No acotada}. Vèrtexs: $\res{(0,\,4),\ (1,\,2),\ (5,\,0)}$; \ $(1,\,2)$ és el tall de $2x+y=4$ i $x+2y=5$.\par" + fig(R6b, (-1, 7, -1, 6), w=4.4)])),
 (1, r"Representa la regió definida per les inequacions següents i calcula'n els vèrtexs:" + dm(r'1\leq x\leq4,\qquad 0\leq y\leq3,\qquad x+y\leq6')
     + recorda(r"Una doble desigualtat $a\leq x\leq b$ són dues inequacions: $x\geq a$ i $x\leq b$ (una franja vertical)."),
     r"És la franja $1\leq x\leq4$, $0\leq y\leq3$, retallada per la recta $x+y=6$. Vèrtexs: $\res{(1,\,0),\ (4,\,0),\ (4,\,2),\ (3,\,3),\ (1,\,3)}$. El punt $(4,\,3)$ no és vèrtex perquè $4+3>6$." + '\n\n\\begin{center}' + fig(R7, (-0.5, 6.5, -1, 4.5), w=5) + '\\end{center}'),
 (2, r"Resol gràficament els sistemes següents:" + tasks(2, [r'$' + sist(r'x+y&\geq2', r'x+y&\leq1', r'x\geq0,\ y&\geq0') + r'$', r'$' + sist(r'y&\geq x', r'y&\leq x+2', r'0\leq x&\leq3') + r'$']),
     tasks(2, [r"Les rectes $x+y=2$ i $x+y=1$ són paral·leles i cap punt pot complir les dues inequacions: la regió és \rest{buida}, el sistema \rest{no té solució}.",
               r"Franja entre dues rectes paral·leles, tallada per $x=0$ i $x=3$: un paral·lelogram de vèrtexs $\res{(0,\,0),\ (3,\,3),\ (3,\,5),\ (0,\,2)}$.\par" + fig(R8b, (-1, 4.5, -1, 6), w=3.6)])),
 (2, r"Escriu el sistema d'inequacions que té com a solució la regió ombrejada:" + '\n\n\\begin{center}' + fig(R9, (-1, 7, -1, 5.5), w=5) + '\\end{center}',
     r"La recta que passa per $(0,\,0)$ i $(2,\,4)$ és $y=2x$; la que passa per $(2,\,4)$ i $(6,\,0)$ és $x+y=6$. Amb punts de l'interior, com $(3,\,1)$, decidim el sentit: \ $\res{y\leq2x,\quad x+y\leq6,\quad y\geq0}$."),
 (2, r"Considera el sistema $\ x+2y\leq8,\ \ 3x+y\leq9,\ \ x\geq0,\ \ y\geq0$." + tasks(1, [r"Esbrina si els punts $(1,\,2)$, $(2,\,3)$ i $(3,\,1)$ pertanyen a la regió factible.", r"Representa la regió i calcula'n els vèrtexs."]),
     tasks(1, [r"$(1,\,2)$: $5\leq8$ i $5\leq9$: \rest{sí}. \ $(2,\,3)$: $8\leq8$ i $9\leq9$: \rest{sí} (és un vèrtex). \ $(3,\,1)$: $5\leq8$, però $10>9$: \rest{no}.",
               r"Vèrtexs: $\res{(0,\,0),\ (3,\,0),\ (2,\,3),\ (0,\,4)}$.\par" + fig(R10, (-1, 5.5, -1, 5.5), w=4)])),
 (2, r"Representa la regió definida per $\ x\geq1,\ \ y\geq2,\ \ x+y\geq5\ $. És acotada? Calcula'n els vèrtexs.",
     r"És \rest{no acotada} (s'estén cap amunt i cap a la dreta). Vèrtexs: $\res{(1,\,4)}$ i $\res{(3,\,2)}$. El punt $(1,\,2)$, tall de $x=1$ i $y=2$, no és vèrtex perquè $1+2<5$." + '\n\n\\begin{center}' + fig(R11, (-0.5, 6, -0.5, 7), w=4.2) + '\\end{center}'),
]))

S.append(("Optimització d'una funció objectiu sobre una regió", [
 (1, r"Calcula el màxim i el mínim de la funció $f(x,y)=3x+2y$ en la regió de l'apartat a) de l'exercici 6."
     + recorda(r"Si la regió és acotada, el màxim i el mínim s'assoleixen en vèrtexs: avalua la funció en tots."),
     avalua(R6a, 3, 2, [(0, 0), (5, 0), (2, 3), (0, 1)], 'f', '3x+2y', opt(R6a, 3, 2, 'max', 15, [(5, 0)]) + opt(R6a, 3, 2, 'min', 0, [(0, 0)]))
     + r"Màxim: $\res{15}$ en $(5,\,0)$. \ Mínim: $\res{0}$ en $(0,\,0)$."),
 (1, r"La regió factible d'un problema és el polígon de vèrtexs $A(0,\,0)$, $B(6,\,0)$, $C(5,\,3)$, $D(2,\,5)$ i $E(0,\,4)$. Troba el màxim i el mínim de les funcions $f(x,y)=x+2y$ i $g(x,y)=2x-y$ en aquesta regió.",
     r"\begin{center}\small\begin{tabular}{ccc}\hline Vèrtex & $f=x+2y$ & $g=2x-y$\\\hline $A(0,\,0)$&0&0\\ $B(6,\,0)$&6&12\\ $C(5,\,3)$&11&7\\ $D(2,\,5)$&12&$-1$\\ $E(0,\,4)$&8&$-4$\\\hline\end{tabular}\end{center}"
     r"$f$: màxim $\res{12}$ en $D$ i mínim $\res{0}$ en $A$. \ $g$: màxim $\res{12}$ en $B$ i mínim $\res{-4}$ en $E$."),
 (2, r"Calcula, si existeixen, el màxim i el mínim de $f(x,y)=4x+3y$ en la regió de l'apartat b) de l'exercici 6."
     + recorda(r"Si la regió no és acotada, pot ser que no hi haja màxim (o mínim). Comprova-ho amb les rectes de nivell $4x+3y=k$."),
     avalua(R6b, 4, 3, [(0, 4), (1, 2), (5, 0)], 'f', '4x+3y', opt(R6b, 4, 3, 'min', 10, [(1, 2)]))
     + r"Mínim: $\res{10}$ en $(1,\,2)$. \ La regió s'estén indefinidament cap amunt i cap a la dreta i $f$ hi creix sense límit: \rest{no té màxim}." + '\n\n\\begin{center}' + fig(R6b, (-1, 7, -1, 6), w=4.2, level=(4, 3, 10), opt=[(1, 2)]) + '\\end{center}'),
 (2, r"Resol el problema anterior gràficament amb rectes de nivell: dibuixa la recta $4x+3y=0$ i desplaça-la paral·lelament. Quin és el primer vèrtex de la regió que toca?",
     r"Les rectes de nivell $4x+3y=k$ són paral·leles a $4x+3y=0$; en augmentar $k$ es desplacen cap amunt i a la dreta. El primer punt de la regió que toquen és $\res{(1,\,2)}$, amb $k=10$ (el mínim). No n'hi ha un últim: no hi ha màxim."),
]))

S.append(("Problemes de programació lineal", [
 (1, r"Una fusteria fabrica taules i cadires. Cada taula necessita 3 hores de muntatge i 1 hora d'acabat, i cada cadira, 1 hora de muntatge i 1 hora d'acabat. Cada setmana es disposa de 60 hores de muntatge i 30 hores d'acabat. El benefici és de 40 € per taula i de 20 € per cadira. Quantes taules i quantes cadires cal fabricar per obtenir el màxim benefici?"
     + recorda(r"Passos: variables (taula de dades) $\to$ funció objectiu $\to$ restriccions $\to$ regió factible $\to$ vèrtexs $\to$ avaluació $\to$ resposta."),
     r"$x$ = taules, $y$ = cadires. \ $\max\ B(x,y)=40x+20y$ \ amb \ $3x+y\leq60$, \ $x+y\leq30$, \ $x,y\geq0$." + '\n\n\\begin{center}' + fig(RFUS, (-3, 35, -3, 35), w=4.4, level=(40, 20, 900), opt=[(15, 15)]) + '\\end{center}'
     + avalua(RFUS, 40, 20, [(0, 0), (20, 0), (15, 15), (0, 30)], 'B', '40x+20y', opt(RFUS, 40, 20, 'max', 900, [(15, 15)]))
     + r"Cal fabricar \rest{15 taules i 15 cadires}; benefici màxim $\res{900\text{ €}}$."),
 (2, r"Un ramader vol barrejar dos pinsos, P i Q. Cada kg de P aporta 2 unitats de vitamina A i 1 de vitamina B, i cada kg de Q, 1 unitat de A i 3 de B. Cada dia el bestiar necessita almenys 8 unitats de A i 9 de B. Si el kg de P costa 3 € i el de Q, 2 €, quants kg de cada pinso ha de comprar perquè el cost siga mínim?",
     r"$x$ = kg de P, $y$ = kg de Q. \ $\min\ C(x,y)=3x+2y$ \ amb \ $2x+y\geq8$, \ $x+3y\geq9$, \ $x,y\geq0$. La regió \textbf{no és acotada}." + '\n\n\\begin{center}' + fig(RDIE, (-1, 11, -1, 10), w=4.4, level=(3, 2, 13), opt=[(3, 2)]) + '\\end{center}'
     + avalua(RDIE, 3, 2, [(0, 8), (3, 2), (9, 0)], 'C', '3x+2y', opt(RDIE, 3, 2, 'min', 13, [(3, 2)]))
     + r"Com que els coeficients són positius, allunyar-se de l'origen només encareix el cost: el mínim existeix. Cal comprar \rest{3 kg de P i 2 kg de Q}; cost mínim $\res{13\text{ €}}$."),
 (2, r"Una persona disposa de 30\,000 € per invertir en dos fons, A i B, amb rendibilitats anuals del 4\,\% i del 6\,\%. Vol posar almenys 10\,000 € en A i no vol invertir en B (més arriscat) més del que inverteix en A. Com ha de repartir els diners per obtenir el màxim rendiment?",
     r"$x$, $y$ = milers d'euros en A i en B. Cada miler rendeix 40 € en A i 60 € en B: \ $\max\ R(x,y)=40x+60y$ \ amb \ $x+y\leq30$, \ $x\geq10$, \ $y\leq x$, \ $y\geq0$." + '\n\n\\begin{center}' + fig(RINV, (-2, 34, -2, 20), w=4.6, level=(40, 60, 1500), opt=[(15, 15)]) + '\\end{center}'
     + avalua(RINV, 40, 60, [(10, 0), (30, 0), (15, 15), (10, 10)], 'R', '40x+60y', opt(RINV, 40, 60, 'max', 1500, [(15, 15)]))
     + r"Ha d'invertir \rest{15\,000 € en A i 15\,000 € en B}; rendiment màxim $\res{1500\text{ €}}$."),
 (3, r"Una empresa té dos magatzems: M1, amb 30 tones de producte, i M2, amb 25 tones. Ha de servir 20 tones a la botiga T1 i 25 a la botiga T2. El cost de transport per tona (en euros) és:" + '\n\n'
     r"\begin{center}\small\begin{tabular}{c|cc}& T1 & T2\\\hline M1 & 5 & 3\\ M2 & 2 & 4\end{tabular}\end{center}"
     r"Com s'ha d'organitzar el transport perquè el cost siga mínim? Quin és aquest cost?",
     r"$x$ = tones de M1 a T1, $y$ = tones de M1 a T2; aleshores M2 envia $20-x$ a T1 i $25-y$ a T2. \ Restriccions: $0\leq x\leq20$, $0\leq y\leq25$, \ $x+y\leq30$ (M1), \ $(20-x)+(25-y)\leq25\Leftrightarrow x+y\geq20$ (M2). \ Cost: $5x+3y+2(20-x)+4(25-y)=3x-y+140$." + '\n\n\\begin{center}' + fig(RTRA, (-2, 23, -2, 28), w=4.2, level=(3, -1, -25), opt=[(0, 25)]) + '\\end{center}'
     + avalua(RTRA, 3, -1, [(0, 20), (0, 25), (5, 25), (20, 10), (20, 0)], '3x-y', '', opt(RTRA, 3, -1, 'min', -25, [(0, 25)])).replace('$3x-y=$', '$3x-y$')
     + r"Mínim de $3x-y$: $-25$ en $(0,\,25)$. M1 envia \rest{0 t a T1 i 25 t a T2} i M2 envia \rest{20 t a T1 i 0 t a T2}. Cost mínim: $-25+140=\res{115\text{ €}}$."),
 (2, r"\pau{C. Valenciana, juliol 2025} Una agència de viatges organitza excursions a la muntanya i a la platja. L'agència obté 700 euros de benefici per cada excursió a la muntanya i 500 euros per cada excursió a la platja. Disposa d'un total de 10 autobusos i 8 guies turístics. Cada excursió a la muntanya requereix 2 autobusos i 2 guies, mentre que cada excursió a la platja requereix 2 autobusos i 1 guia." + tasks(1, [r"Quantes excursions a la muntanya i quantes a la platja ha d'organitzar per obtenir el màxim benefici possible?", r"Quin és aquest benefici màxim?"]),
     r"$x$ = excursions a la muntanya, $y$ = a la platja. \ $\max\ B=700x+500y$ \ amb \ $2x+2y\leq10$, \ $2x+y\leq8$, \ $x,y\geq0$." + '\n\n\\begin{center}' + fig(RP80, (-0.5, 6, -0.5, 6), w=3.8, level=(700, 500, 3100), opt=[(3, 2)]) + '\\end{center}'
     + avalua(RP80, 700, 500, [(0, 0), (4, 0), (3, 2), (0, 5)], 'B', '700x+500y', opt(RP80, 700, 500, 'max', 3100, [(3, 2)]))
     + tasks(2, [r"\rest{3 a la muntanya i 2 a la platja}", r"$\res{3100\text{ €}}$"])),
 (2, r"\pau{C. Valenciana, juny 2025} Un creador de contingut desitja invertir en publicitat fins a 10\,000 euros. Ha considerat dues empreses, A i B. L'empresa A garanteix un increment anual en nombre de seguidors del 10\,\% del que s'hi inverteix, i la B, del 7\,\%. El creador vol invertir almenys 2000 euros en l'empresa B i un màxim de 6000 euros en la A, invertint sempre en la A almenys el que inverteix en la B." + tasks(1, [r"Quants diners ha d'assignar a cada empresa perquè l'increment de seguidors siga màxim?", r"Quin és aquest increment màxim?"]),
     r"$x$, $y$ = euros en A i en B. \ $\max\ S=0{,}1x+0{,}07y$ \ amb \ $x+y\leq10\,000$, \ $y\geq2000$, \ $x\leq6000$, \ $x\geq y$." + '\n\n'
     + avalua(RP79, F(1, 10), F(7, 100), [(2000, 2000), (6000, 2000), (6000, 4000), (5000, 5000)], 'S', '0{,}1x+0{,}07y', opt(RP79, F(1, 10), F(7, 100), 'max', 880, [(6000, 4000)]))
     + tasks(2, [r"\rest{6000 € en A i 4000 € en B}", r"$\res{880}$ seguidors"])),
 (2, r"\pau{C. Valenciana, juny 2023} El veterinari m'ha recomanat que el meu gos prenga diàriament un mínim de 8 unitats d'hidrats de carboni, 46 de proteïnes i 12 de greixos. Una llanda de la marca A conté 4 unitats d'hidrats, 6 de proteïnes i 1 de greixos; una llanda de la marca B, 2 unitats d'hidrats, 20 de proteïnes i 12 de greixos. La llanda A costa 10 euros i la B, 16 euros." + tasks(1, [r"Com hauré de combinar les dues marques per obtenir la dieta desitjada pel preu mínim?", r"Quin és el mínim preu que hauré de pagar?"]),
     r"$\min\ C=10x+16y$ \ amb \ $4x+2y\geq8$, \ $6x+20y\geq46$, \ $x+12y\geq12$, \ $x,y\geq0$ (regió no acotada)." + '\n\n\\begin{center}' + fig(RP76, (-1, 13, -0.5, 5), w=4.6, level=(10, 16, 42), opt=[(1, 2)]) + '\\end{center}'
     + avalua(RP76, 10, 16, [(0, 4), (1, 2), (6, F(1, 2)), (12, 0)], 'C', '10x+16y', opt(RP76, 10, 16, 'min', 42, [(1, 2)]))
     + tasks(2, [r"\rest{1 llanda de A i 2 de B}", r"$\res{42\text{ €}}$"])),
 (2, r"\pau{C. Valenciana, juny 2026} Una granja vol crear una mescla fertilitzant amb dos compostos, NutriMax i BioGrow. S'han d'aplicar com a mínim 8 unitats de nitrogen, 6 de fòsfor i 10 de potassi. Un litre de NutriMax conté 2 unitats de nitrogen, 1 de fòsfor i 1 de potassi, i un litre de BioGrow, 1 de nitrogen, 1 de fòsfor i 2 de potassi. El litre de NutriMax costa 5 euros i el de BioGrow, 4 euros." + tasks(1, [r"Quants litres de cada producte s'han d'utilitzar perquè el cost de la mescla siga mínim?", r"Quin és aquest cost mínim?"]),
     r"$\min\ C=5x+4y$ \ amb \ $2x+y\geq8$, \ $x+y\geq6$, \ $x+2y\geq10$, \ $x,y\geq0$. Les tres rectes passen per $(2,\,4)$." + '\n\n'
     + avalua(RP81, 5, 4, [(0, 8), (2, 4), (10, 0)], 'C', '5x+4y', opt(RP81, 5, 4, 'min', 26, [(2, 4)]))
     + tasks(2, [r"\rest{2 litres de NutriMax i 4 de BioGrow}", r"$\res{26\text{ €}}$"])),
]))

S.append(("Casos especials: infinites solucions i problemes sense solució", [
 (2, r"En la fusteria de l'exercici 16 canvien els preus i ara el benefici és de 30 € per taula i 10 € per cadira. Quina producció dona el màxim benefici? És única?"
     + recorda(r"Si l'òptim s'assoleix en dos vèrtexs, s'assoleix en tots els punts del segment que els uneix: passa quan la funció objectiu és paral·lela a un costat de la regió."),
     avalua(RFUS, 30, 10, [(0, 0), (20, 0), (15, 15), (0, 30)], 'B', '30x+10y', opt(RFUS, 30, 10, 'max', 600, [(15, 15), (20, 0)]))
     + r"El màxim, $\res{600\text{ €}}$, s'assoleix en $(20,\,0)$ i en $(15,\,15)$: $30x+10y=10(3x+y)$ és paral·lela a $3x+y=60$. Hi ha \rest{infinites solucions}: el segment $y=60-3x$, $15\leq x\leq20$. Com que es fabriquen unitats senceres: $(15,\,15)$, $(16,\,12)$, $(17,\,9)$, $(18,\,6)$, $(19,\,3)$ i $(20,\,0)$." + '\n\n\\begin{center}' + fig(RFUS, (-3, 35, -3, 35), w=4.2, level=(30, 10, 600), opt=[(15, 15), (20, 0)], seg=((15, 15), (20, 0))) + '\\end{center}'),
 (2, r"En la regió de l'exercici 17 (la dels pinsos), estudia si existeixen el màxim i el mínim de les funcions:" + tasks(2, [r'$f(x,y)=x+y$', r'$g(x,y)=2x+y$']),
     tasks(1, [r"$f$: $f(0,\,8)=8$, $f(3,\,2)=5$, $f(9,\,0)=9$. Mínim $\res{5}$ en $(3,\,2)$; \rest{no té màxim} (la regió no és acotada i $f$ hi creix indefinidament).",
               r"$g$: $g(0,\,8)=8$, $g(3,\,2)=8$, $g(9,\,0)=18$. El mínim, $\res{8}$, s'assoleix en \rest{tot el segment} d'extrems $(0,\,8)$ i $(3,\,2)$ ($g$ és paral·lela a $2x+y=8$). \rest{No té màxim}."])
     + "%s%s" % (opt(RDIE, 1, 1, 'min', 5, [(3, 2)]) and '', opt(RDIE, 2, 1, 'min', 8, [(0, 8), (3, 2)]) and '')),
 (2, r"Una empresa ha de produir $x$ unitats d'un producte A i $y$ d'un producte B. Per capacitat, no pot fabricar més de 10 unitats en total, però un contracte l'obliga a complir $2x+3y\geq40$. Maximitza el benefici $B(x,y)=3x+2y$.",
     r"Amb $x+y\leq10$ i $x,y\geq0$, el valor més gran de $2x+3y$ és $3\cdot10=30<40$. Les restriccions són incompatibles: la regió factible és \rest{buida} i el problema \rest{no té solució}." + '\n\n\\begin{center}' + fig(RBUI, (-1, 22, -1, 15), w=4) + '\\end{center}'),
 (3, r"En la regió de l'exercici 6a), troba els valors de $k$ perquè la funció $f(x,y)=kx+y$ assolisca el màxim en infinits punts.",
     r"Cal que $f$ siga paral·lela a un costat on hi haja el màxim. Costat $x+y=5$ (de $(5,\,0)$ a $(2,\,3)$): $\res{k=1}$; aleshores $f=x+y$ val 5 en tot el costat i és el màxim. Costat $x-y=-1$ (de $(0,\,1)$ a $(2,\,3)$): $\res{k=-1}$; $f=y-x$ val 1 en tot el costat i és el màxim (en $(0,\,0)$ val 0 i en $(5,\,0)$, $-5$). Per als altres costats (eixos), $f=y$ i $f=x$ no hi tenen el màxim."
     + "%s%s" % (opt(R6a, 1, 1, 'max', 5, [(2, 3), (5, 0)]) and '', opt(R6a, -1, 1, 'max', 1, [(0, 1), (2, 3)]) and '')),
 (2, r"\pau{C. Valenciana, juny 1998} Considera el triangle de vèrtexs $(0,\,0)$, $(2,\,8)$ i $(10,\,3)$. Determina raonadament:" + tasks(1, [r"El punt del triangle on la funció $f(x,y)=-4x+y+9$ pren el màxim.", r"El punt del triangle on la funció $g(x,y)=4x+y+12$ pren el màxim."]),
     tasks(1, [r"$f(0,\,0)=9$, $f(2,\,8)=9$, $f(10,\,3)=-28$. El màxim, $\res{9}$, s'assoleix en \rest{tots els punts del segment} d'extrems $(0,\,0)$ i $(2,\,8)$.",
               r"$g(0,\,0)=12$, $g(2,\,8)=28$, $g(10,\,3)=55$: màxim $\res{55}$ en $\res{(10,\,3)}$."])
     + "%s%s" % (opt(RP17, -4, 1, 'max', 0, [(0, 0), (2, 8)]) and '', opt(RP17, 4, 1, 'max', 43, [(10, 3)]) and '')),
 (1, r"Raona si són vertaderes o falses les afirmacions següents:" + tasks(1, [r"Si la regió factible és acotada i no buida, la funció objectiu sempre té màxim i mínim.", r"Si la regió factible no és acotada, la funció objectiu no té mai mínim.", r"L'òptim d'una funció objectiu no constant pot estar en un punt de l'interior de la regió.", r"Si dos vèrtexs donen el mateix valor màxim, el problema té infinites solucions."]),
     tasks(1, [r"\rest{Vertadera}: és el teorema fonamental, i s'assoleixen en vèrtexs.", r"\rest{Falsa}: en els problemes de dieta la regió no és acotada i hi ha mínim (exercici 17).", r"\rest{Falsa}: sempre es pot millorar movent-se en la direcció en què creix (o decreix) la funció, fins a arribar a la frontera.", r"\rest{Vertadera}: també és òptim tot el segment que els uneix."])),
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
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={programació lineal, inequacions, sistemes d'inequacions, regió factible, vèrtexs, funció objectiu, rectes de nivell, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre = pre.replace(r'\usepackage{tikz}', r'\usepackage{tikz}' + '\n' + r'\usetikzlibrary{calc}')
assert 'refstepcounter{exer}' in pre and 'usetikzlibrary{calc}' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Programació lineal"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 3: %s. 2n de Batxillerat CCSS}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 3: %s · 2n Batxillerat CCSS" % (t, TIT))
    assert '2n Batxillerat CCSS' in p and '2n de Batxillerat CCSS' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 3' if sol else "Fitxa d'exercicis · Unitat 3") + r'''}{Programació lineal}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Pots comprovar les regions factibles, els vèrtexs i els òptims amb el resolutor de programació lineal dels apunts interactius de la unitat."
             if sol else r"Fes les gràfiques amb regle i paper quadriculat, i indica sempre els vèrtexs de la regió. Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat de la Comunitat Valenciana; en trobaràs molts més, resolts, a la pàgina d'exercicis PAU de la unitat.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb el resolutor dels apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't3-fitxa-solucions.tex' if sol else 't3-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'exercicis,', npau, 'de la PAU de la Comunitat Valenciana;', len(CHK), 'comprovacions correctes')
