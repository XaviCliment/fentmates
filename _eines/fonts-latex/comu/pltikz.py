# Eines comunes de programació lineal per als documents LaTeX (apunts imprimibles de la unitat 3 de 2n Batx CCSS):
# aritmètica exacta amb fractions, regions factibles (retall de polígons per semiplans), vèrtexs, òptims
# i gràfiques TikZ de les regions.
import math
from fractions import Fraction as F

def fr(x): return x if isinstance(x, F) else F(str(x))
def tn(x):
    """Nombre en TeX: enter, decimal curt amb coma o fracció."""
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

BIG = F(10 ** 6)
def C(a, b, op, c): return (fr(a), fr(b), op, fr(c))
def _clip(P, a, b, c, s):
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
def region(cons, box):
    x0, x1, y0, y1 = [fr(v) for v in box]
    P = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for a, b, op, c in cons:
        if op in ('<=', '<', '='): P = _clip(P, a, b, c, 1)
        if op in ('>=', '>', '='): P = _clip(P, a, b, c, -1)
    return P
def verts(cons):
    """(vèrtexs reals, acotada?, polígon dins la caixa gran)"""
    P = region(cons, (-BIG, BIG, -BIG, BIG))
    inb = lambda p: abs(p[0]) < BIG and abs(p[1]) < BIG
    return [p for p in P if inb(p)], all(inb(p) for p in P), P
def optim(cons, p, q, goal):
    """(valor òptim, punts on s'assoleix) o (None, []) si no n'hi ha"""
    V, bounded, P = verts(cons)
    if not V: return None, []
    sg = 1 if goal == 'max' else -1
    vals = [fr(p) * v[0] + fr(q) * v[1] for v in V]
    best = max(vals, key=lambda v: sg * v)
    if any(sg * (fr(p) * h[0] + fr(q) * h[1] - best) > 0 for h in P if not (abs(h[0]) < BIG and abs(h[1]) < BIG)):
        return None, []
    return best, sorted(v for v, f in zip(V, vals) if f == best)

COL = ['accent', 'blue!70!black', 'violet', 'orange!85!black', 'teal', 'magenta!80!black']
def nice(r):
    e = 10 ** math.floor(math.log10(r / 5)); m = r / 5 / e
    return e * (1 if m < 1.5 else 2 if m < 3.5 else 5 if m < 7.5 else 10)
def _line(a, b, c, view):
    x0, x1, y0, y1 = view
    a, b, c = float(a), float(b), float(c)
    if abs(b) > abs(a): return [(x0 - 1, (c - a * (x0 - 1)) / b), (x1 + 1, (c - a * (x1 + 1)) / b)]
    return [((c - b * (y0 - 1)) / a, y0 - 1), ((c - b * (y1 + 1)) / a, y1 + 1)]

def fig(cons, view, w=5.0, hmax=4.6, labels=True, names=None, test=None, levels=(), opt=(), seg=None,
        draw_axes_cons=False, shade=True, extra=''):
    """Gràfica TikZ d'una regió. labels: mostra les coordenades dels vèrtexs; names: {vèrtex: 'A'} posa també la lletra;
    levels: [(p, q, k, etiqueta)] rectes de nivell discontínues; opt: vèrtexs òptims (punt gran); seg: segment òptim."""
    x0, x1, y0, y1 = view
    sx = w / (x1 - x0); sy = min(sx, hmax / (y1 - y0))
    st, sty = nice(x1 - x0), nice(y1 - y0)
    s = r'\begin{tikzpicture}[x=%.4fcm,y=%.4fcm,baseline=(current bounding box.center)]' % (sx, sy)
    s += r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1)
    gx = math.ceil(x0 / st) * st; gy = math.ceil(y0 / sty) * sty
    s += r'\foreach \i in {%s,%s,...,%s} \draw[muted!25,very thin] (\i,%s)--(\i,%s);' % (gx, gx + st, x1, y0, y1)
    s += r'\foreach \i in {%s,%s,...,%s} \draw[muted!25,very thin] (%s,\i)--(%s,\i);' % (gy, gy + sty, y1, x0, x1)
    if shade:
        R = region(cons, view)
        if len(R) >= 3: s += r'\fill[teal!22] ' + '--'.join('(%.4f,%.4f)' % (float(a), float(b)) for a, b in R) + '--cycle;'
        elif len(R) == 2: s += r'\draw[teal!45,line width=4pt] (%.4f,%.4f)--(%.4f,%.4f);' % (float(R[0][0]), float(R[0][1]), float(R[1][0]), float(R[1][1]))
    s += r'\end{scope}'
    if y0 <= 0 <= y1: s += r'\draw[-latex,thick] (%s,0)--(%s,0) node[below left=-1pt,font=\scriptsize]{$x$};' % (x0, x1 + 0.25 * st)
    if x0 <= 0 <= x1: s += r'\draw[-latex,thick] (0,%s)--(0,%s) node[below left=-1pt,font=\scriptsize]{$y$};' % (y0, y1 + 0.25 * sty)
    t = gx
    while t <= x1 + 1e-9:
        if abs(t) > 1e-9 and y0 <= 0 <= y1: s += r'\node[below,font=\tiny,text=muted] at (%s,0) {$%s$};' % (t, ('%g' % t).replace('.', '{,}'))
        t += st
    t = gy
    while t <= y1 + 1e-9:
        if abs(t) > 1e-9 and x0 <= 0 <= x1: s += r'\node[left,font=\tiny,text=muted] at (0,%s) {$%s$};' % (t, ('%g' % t).replace('.', '{,}'))
        t += sty
    s += r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1)
    k = 0
    for a, b, op, c in cons:
        if not draw_axes_cons and c == 0 and op == '>=' and (a, b) in ((1, 0), (0, 1)): continue
        P = _line(a, b, c, view)
        s += r'\draw[%s,line width=1.1pt%s] (%.4f,%.4f)--(%.4f,%.4f);' % (COL[k % len(COL)], ',dashed' if op in ('<', '>') else '', P[0][0], P[0][1], P[1][0], P[1][1])
        k += 1
    for p, q, v, lab in levels:
        P = _line(p, q, v, view)
        s += r'\draw[navy,thick,densely dashed] (%.4f,%.4f)--(%.4f,%.4f);' % (P[0][0], P[0][1], P[1][0], P[1][1])
    if seg:
        s += r'\draw[accent,line width=3pt] (%.4f,%.4f)--(%.4f,%.4f);' % (float(seg[0][0]), float(seg[0][1]), float(seg[1][0]), float(seg[1][1]))
    s += r'\end{scope}'
    for p, q, v, lab in levels:
        if not lab: continue
        P = _line(p, q, v, view)
        # etiqueta a l'extrem de la recta que queda dins de la finestra, a la dreta
        pts = [(x, (float(v) - float(p) * x) / float(q)) for x in [x1 - 0.06 * (x1 - x0)]] if float(q) else []
        if pts and y0 <= pts[0][1] <= y1:
            s += r'\node[font=\tiny,text=navy,fill=white,fill opacity=.8,text opacity=1,inner sep=1pt,anchor=south] at (%.4f,%.4f) {$%s$};' % (pts[0][0], pts[0][1], lab)
    if labels:
        V, _, _ = verts(cons)
        if V:
            cx = sum(float(v[0]) for v in V) / len(V); cy = sum(float(v[1]) for v in V) / len(V)
            for v in V:
                vx, vy = float(v[0]), float(v[1])
                if not (x0 <= vx <= x1 and y0 <= vy <= y1): continue
                big = v in [(fr(a), fr(b)) for a, b in opt]
                s += (r'\fill[accent] (%.4f,%.4f) circle (2.3pt);' if big else r'\filldraw[fill=white,draw=navy] (%.4f,%.4f) circle (1.5pt);') % (vx, vy)
                dx, dy = (vx - cx) * sx, (vy - cy) * sy
                ang = math.degrees(math.atan2(dy, dx)) if abs(dx) + abs(dy) > 1e-6 else 45
                nm = (names or {}).get((int(v[0]) if v[0].denominator == 1 else v[0], int(v[1]) if v[1].denominator == 1 else v[1]), '')
                s += (r'\node[font=\tiny,inner sep=1.5pt,fill=white,fill opacity=.75,text opacity=1] at ($(%.4f,%.4f)+(%.1f:0.36cm)$) {$%s%s$};'
                      % (vx, vy, ang, nm, pt(v).replace('\\ ', '')))
    if test is not None:
        p, ok = test
        s += r'\fill[%s] (%s,%s) circle (2.2pt);' % ('teal' if ok else 'red!70!black', p[0], p[1])
    s += extra + r'\end{tikzpicture}'
    return s
