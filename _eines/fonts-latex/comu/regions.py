# Semiplans, regions del pla i figures TikZ per a les fitxes de 4t ESO B (sistemes d'inequacions amb dues incògnites).
# Còpia literal de les funcions de _eines/fonts-latex/1batx-mi-t3/genera.py (fr, clip, C, region, verts, tn, pt, nice, fig),
# que no es pot importar perquè en importar-lo escriu els .tex de 1r Batx MI. Les figures necessiten \usetikzlibrary{calc}.
import math
from fractions import Fraction as F
# ---------- semiplans i regions (com a la unitat 3 de 2n Batx CCSS) ----------
BIG = F(10 ** 6)
def fr(v): return v if isinstance(v, F) else F(str(v))
def clip(P, A, B, C, s):
    out, n = [], len(P)
    if n == 0: return out
    val = lambda p: s * (A * p[0] + B * p[1] - C)
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
def C(A, B, op, c): return (fr(A), fr(B), op, fr(c))
def region(cons, box):
    x0, x1, y0, y1 = [fr(v) for v in box]
    P = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for A, B, op, c in cons:
        if op in ('<=', '<', '='): P = clip(P, A, B, c, 1)
        if op in ('>=', '>', '='): P = clip(P, A, B, c, -1)
    return P
def verts(cons):
    P = region(cons, (-BIG, BIG, -BIG, BIG))
    V = [p for p in P if abs(p[0]) < BIG and abs(p[1]) < BIG]
    return V, len(V) == len(P)
def tn(v):
    v = fr(v)
    if v.denominator == 1: return str(v.numerator)
    return ('-' if v < 0 else '') + r'\frac{%d}{%d}' % (abs(v.numerator), v.denominator)
def pt(p): return '(%s,\\,%s)' % (tn(p[0]), tn(p[1]))
COL = ['accent', 'blue!70!black', 'violet', 'orange!85!black', 'teal']
def nice(r):
    e = 10 ** math.floor(math.log10(r / 5)); mm = r / 5 / e
    return e * (1 if mm < 1.5 else 2 if mm < 3.5 else 5 if mm < 7.5 else 10)
def fig(cons, view, wd=4.6, hmax=4.4, labels=True, pts=()):
    x0, x1, y0, y1 = view
    sx = wd / (x1 - x0); sy = min(sx, hmax / (y1 - y0))
    stx = nice(x1 - x0); sty = nice(y1 - y0)
    s = r'\begin{tikzpicture}[x=%.4fcm,y=%.4fcm,baseline=(current bounding box.center)]' % (sx, sy)
    s += r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1)
    s += r'\foreach \i in {%s,%s,...,%s} \draw[muted!25,very thin] (\i,%s)--(\i,%s);' % (math.ceil(x0 / stx) * stx, math.ceil(x0 / stx) * stx + stx, x1, y0, y1)
    s += r'\foreach \i in {%s,%s,...,%s} \draw[muted!25,very thin] (%s,\i)--(%s,\i);' % (math.ceil(y0 / sty) * sty, math.ceil(y0 / sty) * sty + sty, y1, x0, x1)
    Rg = region(cons, view)
    if len(Rg) >= 3: s += r'\fill[teal!22] ' + '--'.join('(%.4f,%.4f)' % (float(p[0]), float(p[1])) for p in Rg) + '--cycle;'
    s += r'\end{scope}'
    if y0 <= 0 <= y1: s += r'\draw[-latex,thick] (%s,0)--(%s,0) node[below left=-1pt,font=\scriptsize]{$x$};' % (x0, x1 + 0.25 * stx)
    if x0 <= 0 <= x1: s += r'\draw[-latex,thick] (0,%s)--(0,%s) node[below left=-1pt,font=\scriptsize]{$y$};' % (y0, y1 + 0.25 * sty)
    t = math.ceil(x0 / stx) * stx
    while t <= x1 + 1e-9:
        if abs(t) > 1e-9 and y0 <= 0 <= y1: s += r'\node[below,font=\tiny,text=muted] at (%s,0) {$%s$};' % (t, ('%g' % t))
        t += stx
    t = math.ceil(y0 / sty) * sty
    while t <= y1 + 1e-9:
        if abs(t) > 1e-9 and x0 <= 0 <= x1: s += r'\node[left,font=\tiny,text=muted] at (0,%s) {$%s$};' % (t, ('%g' % t))
        t += sty
    s += r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1)
    for j, (A, B, op, c) in enumerate(cons):
        a_, b_, c_ = float(A), float(B), float(c)
        if abs(b_) > abs(a_): P = [(x0 - 1, (c_ - a_ * (x0 - 1)) / b_), (x1 + 1, (c_ - a_ * (x1 + 1)) / b_)]
        else: P = [((c_ - b_ * (y0 - 1)) / a_, y0 - 1), ((c_ - b_ * (y1 + 1)) / a_, y1 + 1)]
        s += r'\draw[%s,line width=1.1pt%s] (%.4f,%.4f)--(%.4f,%.4f);' % (COL[j % len(COL)], ',dashed' if op in ('<', '>') else '', P[0][0], P[0][1], P[1][0], P[1][1])
    s += r'\end{scope}'
    if labels:
        V, _ = verts(cons)
        if V:
            cx = sum(float(v[0]) for v in V) / len(V); cy = sum(float(v[1]) for v in V) / len(V)
            for v in V:
                vx, vy = float(v[0]), float(v[1])
                if not (x0 <= vx <= x1 and y0 <= vy <= y1): continue
                s += r'\filldraw[fill=white,draw=navy] (%.4f,%.4f) circle (1.5pt);' % (vx, vy)
                dx, dy = (vx - cx) * sx, (vy - cy) * sy
                ang = math.degrees(math.atan2(dy, dx)) if abs(dx) + abs(dy) > 1e-6 else 45
                s += r'\node[font=\tiny,inner sep=1.5pt,fill=white,fill opacity=.75,text opacity=1] at ($(%.4f,%.4f)+(%.1f:0.36cm)$) {$%s$};' % (vx, vy, ang, pt(v))
    for p, okp in pts:
        s += r'\fill[%s] (%s,%s) circle (2.2pt);' % ('teal' if okp else 'red!70!black', p[0], p[1])
    s += r'\end{tikzpicture}'
    return s
