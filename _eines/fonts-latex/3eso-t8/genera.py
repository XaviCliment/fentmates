# Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (3r ESO, Unitat 8: Funció lineal i quadràtica)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Cada resultat es comprova amb sympy: imatges (im), pendents (slope), rectes per dos punts (line),
# punts de tall (cut), vèrtexs (vert) i arrels (roots).
import os, re, sys, math
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- comprovacions ----------
x = sp.Symbol('x')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def E(s): return sp.nsimplify(parse_expr(s.replace(',', '.'), transformations=TR, local_dict={'x': x}), rational=True)
def Q(v): return sp.nsimplify(v, rational=True)
R = sp.Rational
def same(a, b): assert sp.simplify(E(a) - E(b)) == 0, (a, b)
def im(s, a, want):
    v = E(s).subs(x, Q(a)); assert sp.simplify(v - Q(want)) == 0, (s, a, v, want)
def slope(P, Qq, want):
    m = (Q(Qq[1]) - Q(P[1])) / (Q(Qq[0]) - Q(P[0])); assert m == Q(want), (P, Qq, m, want)
def line(P, Qq, want):
    for A in (P, Qq): im(want, A[0], A[1])
    assert sp.degree(E(want), x) <= 1, want
def cut(f, g, want):
    s = sp.solve(sp.Eq(E(f), E(g)), x); assert len(s) == 1 and s[0] == Q(want[0]) and E(f).subs(x, s[0]) == Q(want[1]), (f, g, s, want)
def vert(f, want):
    a, b, c = sp.Poly(E(f), x).all_coeffs(); xv = -b / (2 * a)
    assert (xv, E(f).subs(x, xv)) == (Q(want[0]), Q(want[1])), (f, xv, E(f).subs(x, xv), want)
def roots(f, want):
    r = sorted([t for t in sp.solve(E(f), x) if t.is_real], key=float)
    assert r == sorted([Q(w) for w in want], key=float), (f, r, want)
def mn(f, m, n):
    p = sp.Poly(E(f), x); assert p.degree() <= 1 and p.coeff_monomial(x) == Q(m) and p.coeff_monomial(1) == Q(n), (f, m, n)
def nt(v):
    v = sp.nsimplify(v)
    if v.is_Integer: return str(v)
    d = float(v); s = '%g' % d
    if sp.nsimplify(s) == v: return s.replace('.', '{,}')
    return ('-' if v < 0 else '') + r'\tfrac{%d}{%d}' % (abs(v.p), v.q)
def tvf(s, xs, yl='y', xl='x'):
    """taula de valors (calculada amb sympy)"""
    ys = [nt(E(s).subs(x, Q(a))) for a in xs]
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('c' * len(xs), xl, '&'.join(nt(a) for a in xs), yl, '&'.join(ys)))
def tvbuida(xs, yl='y', xl='x'):
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('C{0.7cm}' * len(xs), xl, '&'.join(nt(a) for a in xs), yl, '&'.join([r'\phantom{00}'] * len(xs))))

# ---------- gràfiques (TikZ) ----------
def num(v):
    s = ('%g' % v); return s.replace('.', ',')
def axes(win, tx=1, ty=1, gx=1, gy=1, xl='x', yl='y', lab=True):
    x0, x1, y0, y1 = win
    o = [r'\draw[muted!22,very thin,xstep=%s,ystep=%s] (%s,%s) grid (%s,%s);' % (gx, gy, x0, y0, x1, y1)]
    ax = min(max(0, y0), y1); ay = min(max(0, x0), x1)
    o.append(r'\draw[-latex,muted] (%s,%s)--(%s,%s) node[right,font=\scriptsize]{$%s$};' % (x0, ax, x1 + 0.35 * gx, ax, xl))
    o.append(r'\draw[-latex,muted] (%s,%s)--(%s,%s) node[above,font=\scriptsize]{$%s$};' % (ay, y0, ay, y1 + 0.35 * gy, yl))
    if lab:
        k = math.ceil(x0 / tx) * tx
        while k < x1:
            if k: o.append(r'\node[font=\tiny,muted,below] at (%s,%s) {%s};' % (k, ax, num(k)))
            k += tx
        k = math.ceil(y0 / ty) * ty
        while k < y1:
            if k: o.append(r'\node[font=\tiny,muted,left] at (%s,%s) {%s};' % (ay, k, num(k)))
            k += ty
    return o
COLS = ['accent', 'teal', 'navy']
def tg(win, fns=(), dots=(), vlines=(), guides=(), ux=0.32, uy=None, tx=1, ty=1, gx=1, gy=1, xl='x', yl='y', labs=()):
    """gràfica de rectes i paràboles: fns = [(fórmula, a, b)] (a, b opcionals); dots = [(x, y)]"""
    x0, x1, y0, y1 = win
    uy = uy or ux
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center)]' % (ux, uy)] + axes(win, tx, ty, gx, gy, xl, yl)
    o.append(r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1))
    for g in guides: o.append(r'\draw[muted,dashed] (%s,%s)--(%s,%s);' % (g, y0, g, y1))
    for i, f in enumerate(fns):
        s, a, b = (tuple(f) + (None, None))[:3]
        a = x0 if a is None else a; b = x1 if b is None else b
        fl = sp.lambdify(x, E(s)); seg = []
        for k in range(201):
            t = a + (b - a) * k / 200; v = float(fl(t))
            if y0 - 3 * (y1 - y0) <= v <= y1 + 3 * (y1 - y0): seg.append((t, v))
        o.append(r'\draw[%s,line width=1.1pt] plot[smooth] coordinates {%s};' % (COLS[i % 3], ' '.join('(%.3f,%.3f)' % P for P in seg)))
    for v in vlines: o.append(r'\draw[%s,line width=1.1pt] (%s,%s)--(%s,%s);' % (COLS[len(fns) % 3], v, y0, v, y1))
    o.append(r'\end{scope}')
    for P in dots: o.append(r'\fill[navy] (%s,%s) circle (2.3pt);' % (float(P[0]), float(P[1])))
    for (px, py, t, pos) in labs: o.append(r'\node[font=\scriptsize,%s] at (%s,%s) {%s};' % (pos, px, py, t))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]
W6 = (-4, 4, -4, 4)

# =====================================================================
# 1. Funció de proporcionalitat directa
# =====================================================================
for a in (1, 2, 3, 4): im('2.5x', a, R(5, 2) * a)
im('-2x/3', 3, -2); im('-2x/3', -6, 4); im('-2x/3', 9, -6)
im('7x/4', 4, 7); im('7x/4', -8, -14); im('0.12x', 250, 30); im('0.12x', 1, R(12, 100))
im('1.25x', 8, 10); im('1.25x', 22, R(55, 2))
S_.append(("Funció de proporcionalitat directa", [
 (1, r"Indica quines de les funcions següents són de proporcionalitat directa i, per a aquestes, la constant de proporcionalitat:" + tasks(3, [r"$y=5x$", r"$y=x+5$", r"$y=-\tfrac{x}{3}$", r"$y=x^2$", r"$y=0{,}8x$", r"$y=\dfrac{3}{x}$"])
     + recorda(r"Una funció de proporcionalitat directa té la forma $y=mx$: la seua gràfica és una recta que passa per l'origen i $m=\frac{y}{x}$ és la constant de proporcionalitat (o pendent)."),
     tasks(3, [r"\rest{sí}, $m=\res{5}$", r"\rest{no}", r"\rest{sí}, $m=\res{-\tfrac13}$", r"\rest{no}", r"\rest{sí}, $m=\res{0{,}8}$", r"\rest{no}"])),
 (1, r"Completa la taula de la funció $y=2{,}5x$ i representa-la." + r'\par\smallskip' + tvbuida([0, 1, 2, 3, 4]),
     tvf('2.5x', [0, 1, 2, 3, 4]) + r'\quad ' + tg((-1, 5, -1, 11), fns=[('2.5x',)], dots=[(0, 0), (2, 5), (4, 10)], ux=0.35, uy=0.2, ty=2, gy=1)),
 (1, r"Representa en els mateixos eixos les funcions $y=3x$, \ $y=\tfrac13x$ \ i \ $y=-2x$. Quina és la més inclinada? Quines són creixents?",
     tg((-4, 4, -5, 5), fns=[('3x',), ('x/3',), ('-2x',)], ux=0.35) + r'\quad La més inclinada és $\res{y=3x}$ ($|m|$ més gran). Creixents: $\res{y=3x}$ i $\res{y=\tfrac13x}$ ($m>0$); $y=-2x$ és decreixent.'),
 (2, r"Una funció de proporcionalitat directa passa pel punt $(3,\,-2)$. Escriu-ne l'expressió i comprova si els punts $(-6,\,4)$ i $(9,\,6)$ són de la gràfica.",
     r"$m=\frac{-2}{3}$: \ $\res{y=-\tfrac23x}$. \ $x=-6$: $y=4$ \rest{sí}; \ $x=9$: $y=-6\neq6$ \rest{no}."),
 (2, r"La taula següent, correspon a una funció de proporcionalitat directa? Si és així, escriu-la i calcula la $y$ per a $x=-8$." + r'\par\smallskip' + tvf('7x/4', [4, 8, 12, 20]),
     r"$\frac74=\frac{14}{8}=\frac{21}{12}=\frac{35}{20}=1{,}75$: \rest{sí}, $\res{y=1{,}75x}$. \ $y(-8)=\res{-14}$."),
 (2, r"En una ciutat, la tarifa de l'aigua és de 0,12 € per cada 100 litres (sense quota fixa). Escriu el preu en funció dels hectolitres consumits. Quant costen 250 hL? I 1 L?",
     r"$\res{y=0{,}12x}$ ($x$ en hL). \ $y(250)=\res{30\text{ €}}$. \ 1 L $=0{,}01$ hL: $\res{0{,}0012\text{ €}}$."),
 (3, r"En un mapa, 8 cm corresponen a 10 km. Escriu la distància real en funció de la distància en el mapa. Quina distància real hi ha entre dos pobles separats 22 cm en el mapa? Quants cm hi haurà en el mapa entre dues ciutats a 35 km?",
     r"$m=\frac{10}{8}=1{,}25$: \ $\res{y=1{,}25x}$ ($x$ en cm, $y$ en km). \ $y(22)=\res{27{,}5\text{ km}}$. \ $1{,}25x=35\Rightarrow\res{x=28\text{ cm}}$."),
]))
im('1.25x', 28, 35)

# =====================================================================
# 2. Funció lineal
# =====================================================================
for f, m_, n_ in [('3x-4', 3, -4), ('-x+2', -1, 2), ('7', 0, 7), ('x/2', R(1, 2), 0), ('(5-2x)/3', R(-2, 3), R(5, 3)), ('2(x-1)+3', 2, 1)]: mn(f, m_, n_)
roots('2x-6', [3]); roots('-x/2+2', [4]); roots('4x+3', [R(-3, 4)]); roots('-3x-9', [-3])
im('-2x+3', 2, -1); im('-2x+3', -1, 5); im('-2x+3', 0, 3); im('-2x+3', 3, -3)
im('2x-3', 3, 3); im('2x-3', 0, -3); im('2x-3', 1, -1)
S_.append(("Funció lineal", [
 (1, r"Indica el pendent i l'ordenada en l'origen de cada funció, i digues si és creixent, decreixent o constant:" + tasks(3, [r"$y=3x-4$", r"$y=-x+2$", r"$y=7$", r"$y=\tfrac{x}{2}$", r"$y=\dfrac{5-2x}{3}$", r"$y=2(x-1)+3$"])
     + recorda(r"En $y=mx+n$, $m$ és el \textbf{pendent} (si $m>0$ creix, si $m<0$ decreix, si $m=0$ és constant) i $n$ és l'\textbf{ordenada en l'origen}: la recta talla l'eix $Y$ en $(0,\,n)$."),
     tasks(3, [r"$m=\res{3}$, $n=\res{-4}$; creixent", r"$m=\res{-1}$, $n=\res{2}$; decreixent", r"$m=\res{0}$, $n=\res{7}$; constant", r"$m=\res{\tfrac12}$, $n=\res{0}$; creixent", r"$m=\res{-\tfrac23}$, $n=\res{\tfrac53}$; decreixent", r"$y=2x+1$: $m=\res{2}$, $n=\res{1}$; creixent"])),
 (1, r"Fes una taula de valors i representa $y=-2x+3$.",
     tvf('-2x+3', [-1, 0, 1, 2, 3]) + r'\quad ' + tg((-2, 4, -4, 6), fns=[('-2x+3',)], dots=[(0, 3), (1, 1), (2, -1)], ux=0.32, ty=2)),
 (1, r"Escriu l'equació de la recta que té:" + tasks(2, [r"pendent $4$ i ordenada en l'origen $-1$", r"pendent $-\tfrac12$ i passa per $(0,\,5)$", r"pendent $0$ i passa per $(3,\,-2)$", r"passa per l'origen i per $(2,\,6)$"]),
     tasks(2, [r"$\res{y=4x-1}$", r"$\res{y=-\tfrac12x+5}$", r"$\res{y=-2}$", r"$\res{y=3x}$"])),
 (1, r"Troba els punts de tall amb els eixos de cada recta:" + tasks(2, [r"$y=2x-6$", r"$y=-\tfrac12x+2$", r"$y=4x+3$", r"$y=-3x-9$"]),
     tasks(2, [r"$\res{(0,\,-6)}$, $\res{(3,\,0)}$", r"$\res{(0,\,2)}$, $\res{(4,\,0)}$", r"$\res{(0,\,3)}$, $\res{(-\tfrac34,\,0)}$", r"$\res{(0,\,-9)}$, $\res{(-3,\,0)}$"])),
 (2, r"Associa cada recta amb la seua equació: \quad $y=x+1$, \ \ $y=-2x+2$, \ \ $y=\tfrac12x-2$, \ \ $y=-1$." + r'\par\smallskip'
     + tasks(4, [tg(W6, fns=[('-2x+2',)], ux=0.26), tg(W6, fns=[('-1',)], ux=0.26), tg(W6, fns=[('x+1',)], ux=0.26), tg(W6, fns=[('x/2-2',)], ux=0.26)]),
     tasks(4, [r"$\res{y=-2x+2}$", r"$\res{y=-1}$", r"$\res{y=x+1}$", r"$\res{y=\tfrac12x-2}$"])),
 (2, r"Representa sense fer cap taula, a partir del pendent i l'ordenada en l'origen:" + tasks(2, [r"$y=\tfrac23x-1$", r"$y=-\tfrac34x+2$"]),
     tasks(2, [r"Punt $(0,\,-1)$; avancem 3 i pugem 2: $(3,\,1)$.\\" + tg((-2, 5, -3, 3), fns=[('2x/3-1',)], dots=[(0, -1), (3, 1)], ux=0.3), r"Punt $(0,\,2)$; avancem 4 i baixem 3: $(4,\,-1)$.\\" + tg((-2, 5, -3, 3), fns=[('-3x/4+2',)], dots=[(0, 2), (4, -1)], ux=0.3)])),
 (2, r"Quines d'aquestes rectes passen pel punt $(2,\,-1)$?" + tasks(4, [r"$y=2x-5$", r"$y=-x+1$", r"$y=-\tfrac12x+1$", r"$x=2$"]),
     tasks(4, [r"$4-5=-1$: \rest{sí}", r"$-2+1=-1$: \rest{sí}", r"$-1+1=0\neq-1$: \rest{no}", r"\rest{sí} (però no és funció)"])),
 (3, r"Troba $k$ perquè la recta $y=kx-3$ passe pel punt $(4,\,5)$. On talla l'eix $X$?",
     r"$5=4k-3\Rightarrow\res{k=2}$. \ $2x-3=0\Rightarrow x=\tfrac32$: \ $\res{(\tfrac32,\,0)}$."),
 (3, r"Escriu en la forma $y=mx+n$ i digues el pendent i l'ordenada en l'origen:" + tasks(3, [r"$3x+y=7$", r"$2x-4y+8=0$", r"$\dfrac{x}{2}+\dfrac{y}{3}=1$"]),
     tasks(3, [r"$\res{y=-3x+7}$", r"$\res{y=\tfrac12x+2}$", r"$\res{y=-\tfrac32x+3}$"]) + r"Pendents $-3$, $\tfrac12$, $-\tfrac32$; ordenades $7$, $2$, $3$."),
]))
im('2x-5', 2, -1); im('-x+1', 2, -1); im('-x/2+1', 2, 0); im('2x-3', 4, 5); roots('2x-3', [R(3, 2)])
same('7-3x', '-3x+7'); same('(2x+8)/4', 'x/2+2'); same('3(1-x/2)', '-3x/2+3')
im('2x/3-1', 3, 1); im('-3x/4+2', 4, -1)

# =====================================================================
# 3. Equació d'una recta
# =====================================================================
slope((1, 2), (4, 11), 3); slope((-2, 5), (2, -3), -2); slope((0, -1), (6, 3), R(2, 3)); slope((-3, 4), (5, 4), 0)
im('-x/2+1', 4, -1); im('3x+5', -2, -1); im('-4x+8', 0, 8)
line((1, 3), (3, 7), '2x+1'); line((-1, 4), (2, -2), '-2x+2'); line((-4, 0), (2, 3), 'x/2+2'); line((-3, 5), (3, 1), '-2x/3+3')
S_.append(("Equació d'una recta", [
 (1, r"Calcula el pendent de la recta que passa pels punts:" + tasks(2, [r"$(1,\,2)$ i $(4,\,11)$", r"$(-2,\,5)$ i $(2,\,-3)$", r"$(0,\,-1)$ i $(6,\,3)$", r"$(-3,\,4)$ i $(5,\,4)$"])
     + recorda(r"El pendent de la recta que passa per $(x_1,\,y_1)$ i $(x_2,\,y_2)$ és $m=\dfrac{y_2-y_1}{x_2-x_1}$."),
     tasks(2, [r"$\frac{11-2}{4-1}=\res{3}$", r"$\frac{-3-5}{2+2}=\res{-2}$", r"$\frac{3+1}{6-0}=\res{\tfrac23}$", r"$\frac{0}{8}=\res{0}$ (horitzontal)"])),
 (1, r"Escriu l'equació de la recta que passa pel punt i té el pendent indicat:" + tasks(3, [r"$(4,\,-1)$, \ $m=-\tfrac12$", r"$(-2,\,-1)$, \ $m=3$", r"$(0,\,8)$, \ $m=-4$"])
     + recorda(r"Equació punt-pendent: $y-y_0=m\,(x-x_0)$. Després aïllem la $y$."),
     tasks(3, [r"$y+1=-\tfrac12(x-4)$\\$\res{y=-\tfrac12x+1}$", r"$y+1=3(x+2)$\\$\res{y=3x+5}$", r"$\res{y=-4x+8}$"])),
 (2, r"Troba l'equació de la recta que passa pels dos punts:" + tasks(2, [r"$(1,\,3)$ i $(3,\,7)$", r"$(-1,\,4)$ i $(2,\,-2)$", r"$(-4,\,0)$ i $(2,\,3)$", r"$(-3,\,5)$ i $(3,\,1)$"]),
     tasks(2, [r"$m=2$: $\res{y=2x+1}$", r"$m=-2$: $\res{y=-2x+2}$", r"$m=\tfrac12$: $\res{y=\tfrac12x+2}$", r"$m=-\tfrac23$: $\res{y=-\tfrac23x+3}$"])),
 (2, r"Escriu l'equació de cada recta a partir de la gràfica." + r'\par\smallskip' + tasks(3, [tg((-3, 4, -3, 4), fns=[('3x/2-1',)], dots=[(0, -1), (2, 2)], ux=0.3), tg((-3, 4, -3, 4), fns=[('-x/3+2',)], dots=[(0, 2), (3, 1)], ux=0.3), tg((-3, 4, -3, 4), fns=[('-2x-1',)], dots=[(0, -1), (-1, 1)], ux=0.3)]),
     tasks(3, [r"$(0,\,-1)$ i $(2,\,2)$: $\res{y=\tfrac32x-1}$", r"$(0,\,2)$ i $(3,\,1)$: $\res{y=-\tfrac13x+2}$", r"$(0,\,-1)$ i $(-1,\,1)$: $\res{y=-2x-1}$"])),
 (2, r"Escriu l'equació de la recta:" + tasks(1, [r"paral·lela a $y=4x-3$ que passa per $(1,\,5)$;", r"paral·lela a $2x+y=5$ que passa per l'origen;", r"horitzontal que passa per $(-2,\,6)$, i la vertical que passa pel mateix punt."]),
     tasks(1, [r"$m=4$: $y-5=4(x-1)\Rightarrow\res{y=4x+1}$", r"$y=-2x+5$ té $m=-2$: $\res{y=-2x}$", r"$\res{y=6}$ \ i \ $\res{x=-2}$"])),
 (2, r"Comprova si els punts $A(-2,\,-7)$, $B(1,\,2)$ i $C(3,\,8)$ estan alineats.",
     r"$m_{AB}=\frac{2+7}{1+2}=3$, \ $m_{BC}=\frac{8-2}{3-1}=3$. Mateix pendent: \rest{sí} que estan alineats (sobre $y=3x-1$)."),
 (3, r"Els punts $(2,\,5)$ i $(6,\,k)$ són d'una recta de pendent $-\tfrac12$. Troba $k$ i l'equació de la recta.",
     r"$\frac{k-5}{6-2}=-\frac12\Rightarrow k-5=-2\Rightarrow\res{k=3}$. \ $y-5=-\tfrac12(x-2)\Rightarrow\res{y=-\tfrac12x+6}$."),
 (3, r"Un triangle té els vèrtexs $A(0,\,0)$, $B(6,\,0)$ i $C(2,\,4)$. Troba les equacions de les rectes que contenen els tres costats.",
     r"$AB$: $\res{y=0}$ (l'eix $X$). \ $AC$: $m=2$, $\res{y=2x}$. \ $BC$: $m=\frac{4-0}{2-6}=-1$, $\res{y=-x+6}$."),
]))
line((0, -1), (2, 2), '3x/2-1'); line((0, 2), (3, 1), '-x/3+2'); line((0, -1), (-1, 1), '-2x-1'); im('4x+1', 1, 5); same('5-2x', '-2x+5')
slope((-2, -7), (1, 2), 3); slope((1, 2), (3, 8), 3); line((-2, -7), (3, 8), '3x-1'); im('-x/2+6', 2, 5); im('-x/2+6', 6, 3)
line((0, 0), (2, 4), '2x'); line((6, 0), (2, 4), '-x+6')

# =====================================================================
# 4. Aplicacions de la funció lineal
# =====================================================================
im('0.75x+4', 12, 13); im('0.75x+4', 20, 19); roots('0.75x+4-22', [24])
im('1800-150x', 5, 1050); roots('1800-150x', [12])
im('15+8x', 6, 63); roots('15+8x-95', [10])
line((0, 32), (100, 212), '1.8x+32'); im('1.8x+32', 37, R(986, 10)); roots('1.8x+32-50', [10]); roots('1.8x+32-(-4)', [-20])
line((10, 23), (25, 32), '0.6x+17'); im('0.6x+17', 0, 17); im('0.6x+17', 40, 41)
im('60+0.12x', 400, 108); roots('60+0.12x-90', [250])
line((0, 18), (6, 15), '-x/2+18'); roots('-x/2+18', [36])
S_.append(("Aplicacions de la funció lineal", [
 (1, r"Un aparcament cobra 4 € per entrar i 0,75 € per cada hora. Escriu el preu en funció de les hores, calcula el preu de 12 h i de 20 h, i digues quantes hores has estat si has pagat 22 €.",
     r"$\res{P(x)=0{,}75x+4}$. \ $P(12)=\res{13\text{ €}}$, \ $P(20)=\res{19\text{ €}}$. \ $0{,}75x+4=22\Rightarrow\res{x=24\text{ h}}$."
     ),
 (1, r"Un dipòsit de gasoil té 1\,800 L i se'n gasten 150 L cada dia. Escriu els litres que queden en funció dels dies. Quants en queden al cap de 5 dies? Quan es buidarà? Quin és el domini amb sentit?",
     r"$\res{V(t)=1800-150t}$. \ $V(5)=\res{1050\text{ L}}$. \ $V(t)=0\Rightarrow\res{t=12\text{ dies}}$. \ Domini: $\res{[0,\,12]}$."),
 (1, r"Un electricista cobra 15 € pel desplaçament i 8 € per hora de treball. Fes una taula, escriu la fórmula i representa-la. Quant cobra per 6 h? Quantes hores ha treballat si cobra 95 €?",
     tvf('15+8x', [0, 1, 2, 4, 6], yl='P') + r'\ \ $\res{P=8x+15}$. \ $P(6)=\res{63\text{ €}}$; \ $8x+15=95\Rightarrow\res{x=10\text{ h}}$.\newline ' + tg((0, 11, 0, 100), fns=[('15+8x', 0, 10)], ux=0.35, uy=0.03, tx=2, ty=20, gx=1, gy=10, xl='h', yl='€')),
 (2, r"L'aigua es congela a 0 °C (32 °F) i bull a 100 °C (212 °F). La relació entre les dues escales és lineal.\par a) Troba la fórmula que passa de °C a °F. \ b) Quants °F són 37 °C? \ c) Quants °C són 50 °F? I $-4$ °F?",
     r"a) $m=\frac{212-32}{100}=1{,}8$: \ $\res{F=1{,}8C+32}$. \ b) $\res{98{,}6\text{ °F}}$. \ c) $1{,}8C+32=50\Rightarrow\res{C=10\text{ °C}}$; \ $1{,}8C+32=-4\Rightarrow\res{C=-20\text{ °C}}$."),
 (2, r"Un ciclista està a 6 km de casa i s'allunya a una velocitat constant de 20 km/h. Escriu la distància a casa en funció del temps (en hores), representa-la i digues quan estarà a 56 km.",
     r"$\res{d(t)=6+20t}$. \ $6+20t=56\Rightarrow\res{t=2{,}5\text{ h}}$.\newline " + tg((0, 4, 0, 90), fns=[('6+20x', 0, 3.5)], dots=[(2.5, 56)], ux=0.9, uy=0.025, tx=1, ty=20, gx=0.5, gy=10, xl='t', yl='d')),
 (2, r"El preu d'un llibre en una llibreria en línia és lineal respecte del nombre d'exemplars per l'enviament fix. 10 llibres costen 23 € i 25 llibres, 32 €. Troba la fórmula. Quant costa l'enviament? Quant costen 40 llibres?",
     r"$m=\frac{32-23}{25-10}=0{,}6$: \ $\res{P=0{,}6x+17}$. \ Enviament: $P(0)=\res{17\text{ €}}$. \ $P(40)=\res{41\text{ €}}$."),
 (3, r"Una empresa de lloguer de furgonetes cobra 60 € al dia més 0,12 € per km. Escriu el preu d'un dia en funció dels km, calcula el preu de 400 km i troba quants km es poden fer amb 90 €. Representa la funció.",
     r"$\res{P=0{,}12x+60}$. \ $P(400)=\res{108\text{ €}}$. \ $0{,}12x+60=90\Rightarrow\res{x=250\text{ km}}$.\newline " + tg((0, 550, 0, 130), fns=[('60+0.12x', 0, 500)], ux=0.012, uy=0.025, tx=100, ty=20, gx=50, gy=10, xl='km', yl='€')),
 (3, r"Una espelma fa 18 cm. Després d'estar encesa 6 hores, en fa 15. Si es consumeix de manera lineal, escriu l'altura en funció del temps i digues quantes hores dura en total.",
     r"$m=\frac{15-18}{6}=-0{,}5$ cm/h: \ $\res{h(t)=18-0{,}5t}$. \ $h=0\Rightarrow\res{t=36\text{ h}}$."),
]))
im('6+20x', 2.5, 56)

# =====================================================================
# 5. Estudi conjunt de dues funcions lineals
# =====================================================================
cut('2x+1', '-x+7', (2, 5)); cut('3x-2', 'x+4', (3, 7)); cut('-2x+5', 'x/2', (2, 1)); cut('x/3+1', '-x+5', (3, 2))
cut('2x-3', 'x', (3, 3)); cut('-x+3', 'x-1', (2, 1))
same('(6x-4)/2', '3x-2')
cut('25+0.4x', '10+0.6x', (75, 55)); cut('300+20x', '30x', (30, 900)); cut('5x', '60+2x', (20, 100))
S_.append(("Estudi conjunt de dues funcions lineals", [
 (1, r"Indica la posició relativa de cada parella de rectes (secants, paral·leles o coincidents):" + tasks(2, [r"$y=2x+3$ \ i \ $y=-2x+3$", r"$y=-x+4$ \ i \ $y=-x-1$", r"$y=3x-2$ \ i \ $2y=6x-4$", r"$y=\tfrac12x$ \ i \ $y=2x$"])
     + recorda(r"Pendents diferents: \textbf{secants} (un punt comú). Mateix pendent i $n$ diferent: \textbf{paral·leles}. Mateix pendent i mateixa $n$: \textbf{coincidents}."),
     tasks(2, [r"\rest{secants} (es tallen en $(0,\,3)$)", r"\rest{paral·leles}", r"$y=3x-2$: \rest{coincidents}", r"\rest{secants} (en l'origen)"])),
 (1, r"Troba el punt de tall de les rectes:" + tasks(2, [r"$y=2x+1$ \ i \ $y=-x+7$", r"$y=3x-2$ \ i \ $y=x+4$", r"$y=-2x+5$ \ i \ $y=\tfrac12x$", r"$y=\tfrac13x+1$ \ i \ $y=-x+5$"])
     + recorda(r"En el punt de tall les dues $y$ són iguals: igualem les expressions, resolem l'equació i substituïm."),
     tasks(2, [r"$3x=6$: \ $\res{(2,\,5)}$", r"$2x=6$: \ $\res{(3,\,7)}$", r"$\tfrac52x=5$: \ $\res{(2,\,1)}$", r"$\tfrac43x=4$: \ $\res{(3,\,2)}$"])),
 (2, r"Representa en els mateixos eixos $y=2x-3$ i $y=x$ i troba gràficament el punt de tall. Comprova-ho analíticament.",
     tg((-2, 5, -4, 5), fns=[('2x-3',), ('x',)], dots=[(3, 3)], ux=0.32) + r"\quad Es tallen en $\res{(3,\,3)}$: \ $2x-3=x\Rightarrow x=3$, $y=3$."),
 (2, r"Resol gràficament el sistema $\left\{\begin{array}{l} x+y=3\\ x-y=1\end{array}\right.$ \ (aïlla la $y$ de cada equació i representa les dues rectes).",
     r"$y=-x+3$ i $y=x-1$: \ " + tg((-1, 4, -2, 4), fns=[('-x+3',), ('x-1',)], dots=[(2, 1)], ux=0.35) + r" \ Solució: $\res{x=2,\ y=1}$."),
 (2, r"Escriu una recta paral·lela i una secant a $y=-3x+1$ que passen pel punt $(0,\,4)$. On talla la secant que has triat la recta $y=-3x+1$?",
     r"Paral·lela: $\res{y=-3x+4}$. Secant: qualsevol amb $m\neq-3$, per exemple $\res{y=x+4}$, que talla $y=-3x+1$ en $x+4=-3x+1\Rightarrow x=-\tfrac34$: $\res{(-\tfrac34,\,\tfrac{13}{4})}$."),
 (3, r"Dues empreses de lloguer de cotxes: A cobra 25 € al dia més 0,40 € per km; B cobra 10 € al dia més 0,60 € per km. Escriu les dues funcions, representa-les i digues quina convé segons els km que fem en un dia.",
     r"$A(x)=0{,}4x+25$, \ $B(x)=0{,}6x+10$. \ $0{,}4x+25=0{,}6x+10\Rightarrow\res{x=75\text{ km}}$ (55 €).\newline \rest{Menys de 75 km: B}; \ \rest{més de 75 km: A}." + r'\newline ' + tg((0, 130, 0, 90), fns=[('25+0.4x', 0, 120), ('10+0.6x', 0, 120)], dots=[(75, 55)], ux=0.04, uy=0.035, tx=25, ty=20, gx=25, gy=10, xl='km', yl='€')),
 (3, r"Un club de pàdel cobra 300 € de quota anual i 20 € per partida; un altre no té quota però cobra 30 € per partida. A partir de quantes partides a l'any convé el primer club?",
     r"$300+20x=30x\Rightarrow x=30$ (900 €). \ \rest{A partir de 31 partides} convé el primer (amb 30, costen igual)."),
 (3, r"En Pau ix de casa caminant a 5 km/h. Quatre hores més tard ix la seua germana en bici pel mateix camí a 20 km/h. Escriu la distància a casa de cadascun en funció del temps des que ix en Pau i troba quan i on l'atrapa.",
     r"$d_P(t)=5t$, \ $d_G(t)=20(t-4)$ per a $t\ge4$. \ $5t=20t-80\Rightarrow t=\tfrac{16}{3}\approx5{,}33$ h. L'atrapa \rest{5 h 20 min} després d'eixir en Pau, a $\res{\tfrac{80}{3}\approx26{,}7\text{ km}}$."),
]))
cut('x+4', '-3x+1', (R(-3, 4), R(13, 4))); cut('5x', '20(x-4)', (R(16, 3), R(80, 3)))
cut('-x+3', 'x-1', (2, 1))

# =====================================================================
# 6. Funcions quadràtiques: la paràbola y = ax²
# =====================================================================
roots('x^2-9', [-3, 3]); roots('-2x^2+8', [-2, 2]); roots('x^2+1', []); roots('3x^2', [0])
im('-3x^2/4', 2, -3); im('-3x^2/4', -4, -12)
S_.append(("Funcions quadràtiques: la paràbola $y=ax^2$", [
 (1, r"Completa la taula de valors de $y=x^2$ i de $y=-\tfrac12x^2$ i representa-les en els mateixos eixos." + r'\par\smallskip' + tasks(2, [r"$y=x^2$\\[3pt]" + tvbuida([-3, -2, -1, 0, 1, 2, 3]), r"$y=-\tfrac12x^2$\\[3pt]" + tvbuida([-3, -2, -1, 0, 1, 2, 3])])
     + recorda(r"La gràfica de $y=ax^2$ és una \textbf{paràbola} amb el vèrtex en $(0,\,0)$ i simètrica respecte de l'eix $Y$. Si $a>0$ s'obri cap amunt; si $a<0$, cap avall. Com més gran és $|a|$, més tancada és."),
     tasks(2, [tvf('x^2', [-3, -2, -1, 0, 1, 2, 3]), tvf('-x^2/2', [-3, -2, -1, 0, 1, 2, 3])]) + tg((-4, 4, -5, 9), fns=[('x^2',), ('-x^2/2',)], ux=0.3, uy=0.22, ty=2)),
 (1, r"Sense representar-les, digues cap on s'obri cada paràbola, si és més oberta o més tancada que $y=x^2$ i si el vèrtex és un màxim o un mínim:" + tasks(4, [r"$y=4x^2$", r"$y=-x^2$", r"$y=\tfrac15x^2$", r"$y=-3x^2$"]),
     tasks(2, [r"cap amunt, \rest{més tancada}, mínim", r"cap avall, \rest{igual}, màxim", r"cap amunt, \rest{més oberta}, mínim", r"cap avall, \rest{més tancada}, màxim"])),
 (1, r"Associa cada paràbola amb la seua equació: \quad $y=2x^2$, \ \ $y=-x^2+3$, \ \ $y=\tfrac12x^2$, \ \ $y=x^2-2$." + r'\par\smallskip'
     + tasks(4, [tg((-3, 3, -3, 4), fns=[('x^2/2',)], ux=0.28), tg((-3, 3, -3, 4), fns=[('x^2-2',)], ux=0.28), tg((-3, 3, -3, 4), fns=[('2x^2',)], ux=0.28), tg((-3, 3, -3, 4), fns=[('-x^2+3',)], ux=0.28)]),
     tasks(4, [r"$\res{y=\tfrac12x^2}$", r"$\res{y=x^2-2}$", r"$\res{y=2x^2}$", r"$\res{y=-x^2+3}$"])),
 (2, r"Indica el vèrtex de cada paràbola i els seus punts de tall amb els eixos:" + tasks(2, [r"$y=x^2-9$", r"$y=-2x^2+8$", r"$y=x^2+1$", r"$y=3x^2$"]),
     tasks(2, [r"$V\res{(0,\,-9)}$; talls $\res{(\pm3,\,0)}$", r"$V\res{(0,\,8)}$; talls $\res{(\pm2,\,0)}$", r"$V\res{(0,\,1)}$; \rest{no talla} l'eix $X$", r"$V\res{(0,\,0)}$; només talla en l'origen"])),
 (2, r"Troba el valor de $a$ perquè la paràbola $y=ax^2$ passe pel punt $(2,\,-3)$. Quina altra imatge coneixem sense calcular? Calcula també la imatge de $x=-4$.",
     r"$4a=-3\Rightarrow\res{a=-\tfrac34}$. Per simetria, $(-2,\,-3)$ també és de la paràbola. \ $y(-4)=-\tfrac34\cdot16=\res{-12}$."),
 (3, r"Escriu l'equació d'una paràbola de la forma $y=ax^2+c$ que tinga el vèrtex en $(0,\,4)$ i talle l'eix $X$ en $x=2$. Representa-la.",
     r"$c=4$ i $4a+4=0\Rightarrow a=-1$: \ $\res{y=-x^2+4}$. \ " + tg((-3, 3, -2, 5), fns=[('-x^2+4',)], dots=[(0, 4), (-2, 0), (2, 0)], ux=0.32)),
]))
roots('-x^2+4', [-2, 2])

# =====================================================================
# 7. Representació de y = ax² + bx + c
# =====================================================================
vert('x^2-4x+1', (2, -3)); vert('-x^2+6x-8', (3, 1)); vert('2x^2+8x+3', (-2, -5)); vert('-3x^2+6x', (1, 3)); vert('x^2+3x', (R(-3, 2), R(-9, 4)))
roots('x^2-6x+5', [1, 5]); roots('-x^2+2x+3', [-1, 3]); roots('x^2-4x+4', [2]); roots('x^2+2x+5', []); roots('2x^2-x-3', [-1, R(3, 2)])
vert('x^2-2x-8', (1, -9)); roots('x^2-2x-8', [-2, 4]); vert('-x^2-2x+3', (-1, 4)); roots('-x^2-2x+3', [-3, 1])
vert('x^2+4x+5', (-2, 1)); roots('x^2+4x+5', []); vert('-x^2+4x-4', (2, 0)); roots('-x^2+4x-4', [2])
vert('x^2-4x+3', (2, -1)); vert('x^2-6x', (3, -9))
S_.append(("Representació de $y=ax^2+bx+c$", [
 (1, r"Calcula el vèrtex i l'eix de simetria de cada paràbola i digues si el vèrtex és un màxim o un mínim:" + tasks(2, [r"$y=x^2-4x+1$", r"$y=-x^2+6x-8$", r"$y=2x^2+8x+3$", r"$y=-3x^2+6x$", r"$y=x^2+3x$"])
     + recorda(r"Vèrtex: $x_v=\dfrac{-b}{2a}$ i $y_v=f(x_v)$. L'eix de simetria és la recta $x=x_v$. Si $a>0$ el vèrtex és un mínim; si $a<0$, un màxim."),
     tasks(2, [r"$V\res{(2,\,-3)}$, eix $x=2$, mínim", r"$V\res{(3,\,1)}$, eix $x=3$, màxim", r"$V\res{(-2,\,-5)}$, eix $x=-2$, mínim", r"$V\res{(1,\,3)}$, eix $x=1$, màxim", r"$V\res{(-\tfrac32,\,-\tfrac94)}$, eix $x=-\tfrac32$, mínim"])),
 (1, r"Troba els punts de tall amb els eixos:" + tasks(2, [r"$y=x^2-6x+5$", r"$y=-x^2+2x+3$", r"$y=x^2-4x+4$", r"$y=x^2+2x+5$", r"$y=2x^2-x-3$"]),
     tasks(2, [r"$(0,\,5)$; \ $\res{(1,\,0)}$, $\res{(5,\,0)}$", r"$(0,\,3)$; \ $\res{(-1,\,0)}$, $\res{(3,\,0)}$", r"$(0,\,4)$; \ $\res{(2,\,0)}$ (el vèrtex)", r"$(0,\,5)$; \ $\Delta=-16<0$: \rest{cap}", r"$(0,\,-3)$; \ $\res{(-1,\,0)}$, $\res{(\tfrac32,\,0)}$"])),
 (2, r"Estudia (forma, vèrtex, eix, talls amb els eixos) i representa $y=x^2-2x-8$.",
     r"$a>0$: cap amunt. \ $V\res{(1,\,-9)}$, eix $x=1$. \ Talls: $\res{(0,\,-8)}$, $\res{(-2,\,0)}$, $\res{(4,\,0)}$.\newline " + tvf('x^2-2x-8', [-2, -1, 0, 1, 2, 3, 4]) + r'\quad ' + tg((-3, 5, -10, 2), fns=[('x^2-2x-8',)], guides=[1], dots=[(1, -9), (-2, 0), (4, 0), (0, -8)], ux=0.3, uy=0.2, ty=2)),
 (2, r"Estudia i representa $y=-x^2-2x+3$.",
     r"$a<0$: cap avall. \ $V\res{(-1,\,4)}$ (màxim), eix $x=-1$. \ Talls: $\res{(0,\,3)}$, $\res{(-3,\,0)}$, $\res{(1,\,0)}$.\newline " + tvf('-x^2-2x+3', [-4, -3, -2, -1, 0, 1, 2]) + r'\quad ' + tg((-5, 3, -6, 5), fns=[('-x^2-2x+3',)], guides=[-1], dots=[(-1, 4), (-3, 0), (1, 0), (0, 3)], ux=0.3, uy=0.25)),
 (2, r"Representa $y=x^2+4x+5$ amb una taula de valors al voltant del vèrtex. Per què no talla l'eix $X$?",
     r"$V\res{(-2,\,1)}$, eix $x=-2$. " + tvf('x^2+4x+5', [-4, -3, -2, -1, 0]) + r" \ $\Delta=16-20<0$: el vèrtex és un mínim per damunt de l'eix, \rest{no el talla}.\newline " + tg((-5, 1, -1, 6), fns=[('x^2+4x+5',)], guides=[-2], dots=[(-2, 1), (0, 5), (-4, 5)], ux=0.32)),
 (2, r"Associa cada paràbola amb la seua equació: \quad $y=x^2-4x+3$, \ \ $y=-x^2+4x-4$, \ \ $y=x^2+2x$." + r'\par\smallskip'
     + tasks(3, [tg((-3, 5, -4, 4), fns=[('-x^2+4x-4',)], ux=0.26), tg((-3, 5, -4, 4), fns=[('x^2+2x',)], ux=0.26), tg((-3, 5, -4, 4), fns=[('x^2-4x+3',)], ux=0.26)]),
     tasks(1, [r"$\res{y=-x^2+4x-4}$ (cap avall, $V(2,\,0)$)", r"$\res{y=x^2+2x}$ (passa per l'origen)", r"$\res{y=x^2-4x+3}$ ($V(2,\,-1)$)"])),
 (3, r"Indica els intervals de creixement i decreixement i el màxim o mínim de $y=-2x^2+8x-5$.",
     r"$x_v=\frac{-8}{-4}=2$, $y_v=-8+16-5=3$; $a<0$: \rest{creix} en $\res{(-\infty,\,2)}$, \rest{decreix} en $\res{(2,\,+\infty)}$; \ màxim $\res{(2,\,3)}$."),
 (3, r"Troba $b$ perquè el vèrtex de la paràbola $y=x^2+bx+5$ estiga en $x=3$. Quin és aleshores el vèrtex? Talla l'eix $X$?",
     r"$\frac{-b}{2}=3\Rightarrow\res{b=-6}$. \ $y=x^2-6x+5$, \ $V\res{(3,\,-4)}$. \ \rest{Sí}: en $(1,\,0)$ i $(5,\,0)$."),
 (3, r"Escriu l'equació de la paràbola $y=x^2+bx+c$ que passa pels punts $(0,\,3)$ i $(1,\,0)$. Troba'n el vèrtex.",
     r"$(0,\,3)$: $c=3$. \ $(1,\,0)$: $1+b+3=0\Rightarrow b=-4$. \ $\res{y=x^2-4x+3}$, \ $V\res{(2,\,-1)}$."),
]))
vert('-2x^2+8x-5', (2, 3)); vert('x^2-6x+5', (3, -4)); im('x^2-4x+3', 0, 3); im('x^2-4x+3', 1, 0); roots('x^2+2x', [-2, 0]); vert('x^2+2x', (-1, -1)); vert('-x^2+4x-4', (2, 0))

# =====================================================================
# 8. Problemes amb paràboles
# =====================================================================
vert('40x-5x^2', (4, 80)); roots('40x-5x^2', [0, 8])
vert('x(30-x)', (15, 225)); vert('x(60-2x)', (15, 450))
vert('25+20x-5x^2', (2, 45)); roots('25+20x-5x^2', [-1, 5])
vert('(10+x)(400-20x)', (5, 4500)); same('(10+x)(400-20x)', '-20x^2+200x+4000')
vert('x(16-x)', (8, 64)); vert('-x^2+12x-20', (6, 16)); roots('-x^2+12x-20', [2, 10])
S_.append(("Problemes amb paràboles", [
 (1, r"Llancem un coet de joguet cap amunt i la seua altura (en m) al cap de $t$ segons és $h(t)=40t-5t^2$.\par a) Quina altura màxima assoleix i en quin moment? \ b) Quan torna a terra? \ c) Representa la funció en el seu domini amb sentit.",
     r"a) $t_v=\frac{-40}{-10}=4$ s, \ $h(4)=\res{80\text{ m}}$ \ als $\res{4\text{ s}}$. \ b) $5t(8-t)=0\Rightarrow\res{t=8\text{ s}}$. \ c) Domini $[0,\,8]$:\newline " + tg((0, 9, 0, 90), fns=[('40x-5x^2', 0, 8)], guides=[4], dots=[(4, 80)], ux=0.45, uy=0.035, tx=1, ty=20, gx=1, gy=10, xl='t', yl='h')
     + recorda(r"En un problema, el valor màxim o mínim d'una funció quadràtica està en el \textbf{vèrtex}: $x_v$ diu quan (o amb quin valor) i $y_v$, quant val.")),
 (1, r"Dos nombres sumen 30. Escriu el seu producte en funció d'un d'ells i troba quins són si el producte és màxim.",
     r"$P(x)=x(30-x)=-x^2+30x$. \ $x_v=15$: \ els nombres són $\res{15\text{ i }15}$ (producte màxim $\res{225}$)."),
 (2, r"Amb 60 m de tanca volem fer un corral rectangular aprofitant una paret (només cal tanca en tres costats). Si $x$ és la longitud dels costats perpendiculars a la paret, escriu l'àrea en funció de $x$ i troba les dimensions de l'àrea màxima.",
     r"Costat paral·lel: $60-2x$. \ $A(x)=x(60-2x)=-2x^2+60x$. \ $x_v=15$: \ $\res{15\text{ m}\times30\text{ m}}$, àrea $\res{450\text{ m}^2}$."),
 (2, r"Des de dalt d'un edifici de 25 m llancem una pilota cap amunt i la seua altura és $h(t)=25+20t-5t^2$. Quina altura màxima assoleix? Quan arriba a terra?",
     r"$t_v=2$ s, \ $h(2)=\res{45\text{ m}}$. \ $25+20t-5t^2=0\Rightarrow t^2-4t-5=0\Rightarrow t=5$ o $t=-1$ (no té sentit): \ $\res{t=5\text{ s}}$."),
 (2, r"Un rectangle té 32 cm de perímetre. Escriu la seua àrea en funció de la base $x$, fes una taula per a $x=2,\,4,\,6,\,8,\,10,\,12,\,14$ i digues quina base dona l'àrea màxima.",
     r"Base + altura $=16$: $A(x)=x(16-x)$. \ " + tvf('x(16-x)', [2, 4, 6, 8, 10, 12, 14], yl='A') + r" \ Màxim per a $\res{x=8}$: un quadrat de 8 cm ($\res{64\text{ cm}^2}$)."),
 (3, r"Una agència de viatges ven 400 bitllets a 10 € cadascun. Per cada euro que en puja el preu, en ven 20 menys. Escriu els ingressos en funció de la pujada $x$ i troba quin preu dona els ingressos màxims.",
     r"$I(x)=(10+x)(400-20x)=-20x^2+200x+4000$. \ $x_v=5$: preu $\res{15\text{ €}}$, ven 300 bitllets i ingressa $\res{4500\text{ €}}$."),
 (3, r"El benefici diari (en €) d'una botiga en funció del nombre $x$ de treballadors és $B(x)=-x^2+12x-20$. Quants treballadors donen el benefici màxim? Amb quants treballadors no hi ha pèrdues?",
     r"$x_v=6$: \ $\res{6\text{ treballadors}}$ (16 €). \ $B(x)=0\Rightarrow x=2$ i $x=10$; \ $B\ge0$ entre els dos: \rest{de 2 a 10 treballadors}."),
]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = 'pdfkeywords={proporcionalitat directa, funció lineal, pendent, ordenada en l\'origen, equació de la recta, punt de tall, paràbola, vèrtex, funció quadràtica}'
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def build(sol_):
    t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
    p = pre_.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                     "pdftitle={%s de la unitat 8: Funció lineal i quadràtica. 3r d'ESO}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 8: Funció lineal i quadràtica · 3r d'ESO" % t)
    assert 'Unitat 8' in p and 'unitat 8' in p
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{3r ESO}{''' + ('Solucions de la fitxa · Unitat 8' if sol_ else "Fitxa d'exercicis · Unitat 8") + r'''}{Funció lineal i quadràtica}
''')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs eines que calculen rectes per dos punts, punts de tall i l'estudi complet d'una paràbola."
             if sol_ else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Per a dibuixar gràfiques, fes servir paper quadriculat i tria una escala adequada per a cada eix.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st_, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st_, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't8-fitxa-solucions.tex' if sol_ else 't8-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
