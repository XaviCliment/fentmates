# Versió en castellà de genera.py. Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (3r ESO, Unitat 8: Funció lineal i quadràtica)
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
S_.append(("Función de proporcionalidad directa", [
 (1, r"Indica cuáles de las siguientes funciones son de proporcionalidad directa y, para estas, la constante de proporcionalidad:" + tasks(3, [r"$y=5x$", r"$y=x+5$", r"$y=-\tfrac{x}{3}$", r"$y=x^2$", r"$y=0{,}8x$", r"$y=\dfrac{3}{x}$"])
     + recorda(r"Una función de proporcionalidad directa tiene la forma $y=mx$: su gráfica es una recta que pasa por el origen y $m=\frac{y}{x}$ es la constante de proporcionalidad (o pendiente)."),
     tasks(3, [r"\rest{sí}, $m=\res{5}$", r"\rest{no}", r"\rest{sí}, $m=\res{-\tfrac13}$", r"\rest{no}", r"\rest{sí}, $m=\res{0{,}8}$", r"\rest{no}"])),
 (1, r"Completa la tabla de la función $y=2{,}5x$ y represéntala." + r'\par\smallskip' + tvbuida([0, 1, 2, 3, 4]),
     tvf('2.5x', [0, 1, 2, 3, 4]) + r'\quad ' + tg((-1, 5, -1, 11), fns=[('2.5x',)], dots=[(0, 0), (2, 5), (4, 10)], ux=0.35, uy=0.2, ty=2, gy=1)),
 (1, r"Representa en los mismos ejes las funciones $y=3x$, \ $y=\tfrac13x$ \ y \ $y=-2x$. ¿Cuál es la más inclinada? ¿Cuáles son crecientes?",
     tg((-4, 4, -5, 5), fns=[('3x',), ('x/3',), ('-2x',)], ux=0.35) + r'\quad La más inclinada es $\res{y=3x}$ ($|m|$ mayor). Crecientes: $\res{y=3x}$ y $\res{y=\tfrac13x}$ ($m>0$); $y=-2x$ es decreciente.'),
 (2, r"Una función de proporcionalidad directa pasa por el punto $(3,\,-2)$. Escribe su expresión y comprueba si los puntos $(-6,\,4)$ y $(9,\,6)$ son de la gráfica.",
     r"$m=\frac{-2}{3}$: \ $\res{y=-\tfrac23x}$. \ $x=-6$: $y=4$ \rest{sí}; \ $x=9$: $y=-6\neq6$ \rest{no}."),
 (2, r"¿La siguiente tabla corresponde a una función de proporcionalidad directa? Si es así, escríbela y calcula la $y$ para $x=-8$." + r'\par\smallskip' + tvf('7x/4', [4, 8, 12, 20]),
     r"$\frac74=\frac{14}{8}=\frac{21}{12}=\frac{35}{20}=1{,}75$: \rest{sí}, $\res{y=1{,}75x}$. \ $y(-8)=\res{-14}$."),
 (2, r"En una ciudad, la tarifa del agua es de 0,12 € por cada 100 litros (sin cuota fija). Escribe el precio en función de los hectolitros consumidos. ¿Cuánto cuestan 250 hL? ¿Y 1 L?",
     r"$\res{y=0{,}12x}$ ($x$ en hL). \ $y(250)=\res{30\text{ €}}$. \ 1 L $=0{,}01$ hL: $\res{0{,}0012\text{ €}}$."),
 (3, r"En un mapa, 8 cm corresponden a 10 km. Escribe la distancia real en función de la distancia en el mapa. ¿Qué distancia real hay entre dos pueblos separados 22 cm en el mapa? ¿Cuántos cm habrá en el mapa entre dos ciudades a 35 km?",
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
S_.append(("Función lineal", [
 (1, r"Indica la pendiente y la ordenada en el origen de cada función, y di si es creciente, decreciente o constante:" + tasks(3, [r"$y=3x-4$", r"$y=-x+2$", r"$y=7$", r"$y=\tfrac{x}{2}$", r"$y=\dfrac{5-2x}{3}$", r"$y=2(x-1)+3$"])
     + recorda(r"En $y=mx+n$, $m$ es la \textbf{pendiente} (si $m>0$ crece, si $m<0$ decrece, si $m=0$ es constante) y $n$ es la \textbf{ordenada en el origen}: la recta corta el eje $Y$ en $(0,\,n)$."),
     tasks(3, [r"$m=\res{3}$, $n=\res{-4}$; creciente", r"$m=\res{-1}$, $n=\res{2}$; decreciente", r"$m=\res{0}$, $n=\res{7}$; constante", r"$m=\res{\tfrac12}$, $n=\res{0}$; creciente", r"$m=\res{-\tfrac23}$, $n=\res{\tfrac53}$; decreciente", r"$y=2x+1$: $m=\res{2}$, $n=\res{1}$; creciente"])),
 (1, r"Haz una tabla de valores y representa $y=-2x+3$.",
     tvf('-2x+3', [-1, 0, 1, 2, 3]) + r'\quad ' + tg((-2, 4, -4, 6), fns=[('-2x+3',)], dots=[(0, 3), (1, 1), (2, -1)], ux=0.32, ty=2)),
 (1, r"Escribe la ecuación de la recta que tiene:" + tasks(2, [r"pendiente $4$ y ordenada en el origen $-1$", r"pendiente $-\tfrac12$ y pasa por $(0,\,5)$", r"pendiente $0$ y pasa por $(3,\,-2)$", r"pasa por el origen y por $(2,\,6)$"]),
     tasks(2, [r"$\res{y=4x-1}$", r"$\res{y=-\tfrac12x+5}$", r"$\res{y=-2}$", r"$\res{y=3x}$"])),
 (1, r"Halla los puntos de corte con los ejes de cada recta:" + tasks(2, [r"$y=2x-6$", r"$y=-\tfrac12x+2$", r"$y=4x+3$", r"$y=-3x-9$"]),
     tasks(2, [r"$\res{(0,\,-6)}$, $\res{(3,\,0)}$", r"$\res{(0,\,2)}$, $\res{(4,\,0)}$", r"$\res{(0,\,3)}$, $\res{(-\tfrac34,\,0)}$", r"$\res{(0,\,-9)}$, $\res{(-3,\,0)}$"])),
 (2, r"Asocia cada recta con su ecuación: \quad $y=x+1$, \ \ $y=-2x+2$, \ \ $y=\tfrac12x-2$, \ \ $y=-1$." + r'\par\smallskip'
     + tasks(4, [tg(W6, fns=[('-2x+2',)], ux=0.26), tg(W6, fns=[('-1',)], ux=0.26), tg(W6, fns=[('x+1',)], ux=0.26), tg(W6, fns=[('x/2-2',)], ux=0.26)]),
     tasks(4, [r"$\res{y=-2x+2}$", r"$\res{y=-1}$", r"$\res{y=x+1}$", r"$\res{y=\tfrac12x-2}$"])),
 (2, r"Representa sin hacer ninguna tabla, a partir de la pendiente y la ordenada en el origen:" + tasks(2, [r"$y=\tfrac23x-1$", r"$y=-\tfrac34x+2$"]),
     tasks(2, [r"Punto $(0,\,-1)$; avanzamos 3 y subimos 2: $(3,\,1)$.\\" + tg((-2, 5, -3, 3), fns=[('2x/3-1',)], dots=[(0, -1), (3, 1)], ux=0.3), r"Punto $(0,\,2)$; avanzamos 4 y bajamos 3: $(4,\,-1)$.\\" + tg((-2, 5, -3, 3), fns=[('-3x/4+2',)], dots=[(0, 2), (4, -1)], ux=0.3)])),
 (2, r"¿Cuáles de estas rectas pasan por el punto $(2,\,-1)$?" + tasks(4, [r"$y=2x-5$", r"$y=-x+1$", r"$y=-\tfrac12x+1$", r"$x=2$"]),
     tasks(4, [r"$4-5=-1$: \rest{sí}", r"$-2+1=-1$: \rest{sí}", r"$-1+1=0\neq-1$: \rest{no}", r"\rest{sí} (pero no es función)"])),
 (3, r"Halla $k$ para que la recta $y=kx-3$ pase por el punto $(4,\,5)$. ¿Dónde corta el eje $X$?",
     r"$5=4k-3\Rightarrow\res{k=2}$. \ $2x-3=0\Rightarrow x=\tfrac32$: \ $\res{(\tfrac32,\,0)}$."),
 (3, r"Escribe en la forma $y=mx+n$ y di la pendiente y la ordenada en el origen:" + tasks(3, [r"$3x+y=7$", r"$2x-4y+8=0$", r"$\dfrac{x}{2}+\dfrac{y}{3}=1$"]),
     tasks(3, [r"$\res{y=-3x+7}$", r"$\res{y=\tfrac12x+2}$", r"$\res{y=-\tfrac32x+3}$"]) + r"Pendientes $-3$, $\tfrac12$, $-\tfrac32$; ordenadas $7$, $2$, $3$."),
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
S_.append(("Ecuación de una recta", [
 (1, r"Calcula la pendiente de la recta que pasa por los puntos:" + tasks(2, [r"$(1,\,2)$ y $(4,\,11)$", r"$(-2,\,5)$ y $(2,\,-3)$", r"$(0,\,-1)$ y $(6,\,3)$", r"$(-3,\,4)$ y $(5,\,4)$"])
     + recorda(r"La pendiente de la recta que pasa por $(x_1,\,y_1)$ y $(x_2,\,y_2)$ es $m=\dfrac{y_2-y_1}{x_2-x_1}$."),
     tasks(2, [r"$\frac{11-2}{4-1}=\res{3}$", r"$\frac{-3-5}{2+2}=\res{-2}$", r"$\frac{3+1}{6-0}=\res{\tfrac23}$", r"$\frac{0}{8}=\res{0}$ (horizontal)"])),
 (1, r"Escribe la ecuación de la recta que pasa por el punto y tiene la pendiente indicada:" + tasks(3, [r"$(4,\,-1)$, \ $m=-\tfrac12$", r"$(-2,\,-1)$, \ $m=3$", r"$(0,\,8)$, \ $m=-4$"])
     + recorda(r"Ecuación punto-pendiente: $y-y_0=m\,(x-x_0)$. Después despejamos la $y$."),
     tasks(3, [r"$y+1=-\tfrac12(x-4)$\\$\res{y=-\tfrac12x+1}$", r"$y+1=3(x+2)$\\$\res{y=3x+5}$", r"$\res{y=-4x+8}$"])),
 (2, r"Halla la ecuación de la recta que pasa por los dos puntos:" + tasks(2, [r"$(1,\,3)$ y $(3,\,7)$", r"$(-1,\,4)$ y $(2,\,-2)$", r"$(-4,\,0)$ y $(2,\,3)$", r"$(-3,\,5)$ y $(3,\,1)$"]),
     tasks(2, [r"$m=2$: $\res{y=2x+1}$", r"$m=-2$: $\res{y=-2x+2}$", r"$m=\tfrac12$: $\res{y=\tfrac12x+2}$", r"$m=-\tfrac23$: $\res{y=-\tfrac23x+3}$"])),
 (2, r"Escribe la ecuación de cada recta a partir de la gráfica." + r'\par\smallskip' + tasks(3, [tg((-3, 4, -3, 4), fns=[('3x/2-1',)], dots=[(0, -1), (2, 2)], ux=0.3), tg((-3, 4, -3, 4), fns=[('-x/3+2',)], dots=[(0, 2), (3, 1)], ux=0.3), tg((-3, 4, -3, 4), fns=[('-2x-1',)], dots=[(0, -1), (-1, 1)], ux=0.3)]),
     tasks(3, [r"$(0,\,-1)$ y $(2,\,2)$: $\res{y=\tfrac32x-1}$", r"$(0,\,2)$ y $(3,\,1)$: $\res{y=-\tfrac13x+2}$", r"$(0,\,-1)$ y $(-1,\,1)$: $\res{y=-2x-1}$"])),
 (2, r"Escribe la ecuación de la recta:" + tasks(1, [r"paralela a $y=4x-3$ que pasa por $(1,\,5)$;", r"paralela a $2x+y=5$ que pasa por el origen;", r"horizontal que pasa por $(-2,\,6)$, y la vertical que pasa por el mismo punto."]),
     tasks(1, [r"$m=4$: $y-5=4(x-1)\Rightarrow\res{y=4x+1}$", r"$y=-2x+5$ tiene $m=-2$: $\res{y=-2x}$", r"$\res{y=6}$ \ y \ $\res{x=-2}$"])),
 (2, r"Comprueba si los puntos $A(-2,\,-7)$, $B(1,\,2)$ y $C(3,\,8)$ están alineados.",
     r"$m_{AB}=\frac{2+7}{1+2}=3$, \ $m_{BC}=\frac{8-2}{3-1}=3$. Misma pendiente: \rest{sí} están alineados (sobre $y=3x-1$)."),
 (3, r"Los puntos $(2,\,5)$ y $(6,\,k)$ son de una recta de pendiente $-\tfrac12$. Halla $k$ y la ecuación de la recta.",
     r"$\frac{k-5}{6-2}=-\frac12\Rightarrow k-5=-2\Rightarrow\res{k=3}$. \ $y-5=-\tfrac12(x-2)\Rightarrow\res{y=-\tfrac12x+6}$."),
 (3, r"Un triángulo tiene los vértices $A(0,\,0)$, $B(6,\,0)$ y $C(2,\,4)$. Halla las ecuaciones de las rectas que contienen los tres lados.",
     r"$AB$: $\res{y=0}$ (el eje $X$). \ $AC$: $m=2$, $\res{y=2x}$. \ $BC$: $m=\frac{4-0}{2-6}=-1$, $\res{y=-x+6}$."),
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
S_.append(("Aplicaciones de la función lineal", [
 (1, r"Un aparcamiento cobra 4 € por entrar y 0,75 € por cada hora. Escribe el precio en función de las horas, calcula el precio de 12 h y de 20 h, y di cuántas horas has estado si has pagado 22 €.",
     r"$\res{P(x)=0{,}75x+4}$. \ $P(12)=\res{13\text{ €}}$, \ $P(20)=\res{19\text{ €}}$. \ $0{,}75x+4=22\Rightarrow\res{x=24\text{ h}}$."
     ),
 (1, r"Un depósito de gasóleo tiene 1\,800 L y se gastan 150 L cada día. Escribe los litros que quedan en función de los días. ¿Cuántos quedan al cabo de 5 días? ¿Cuándo se vaciará? ¿Cuál es el dominio con sentido?",
     r"$\res{V(t)=1800-150t}$. \ $V(5)=\res{1050\text{ L}}$. \ $V(t)=0\Rightarrow\res{t=12\text{ días}}$. \ Dominio: $\res{[0,\,12]}$."),
 (1, r"Un electricista cobra 15 € por el desplazamiento y 8 € por hora de trabajo. Haz una tabla, escribe la fórmula y represéntala. ¿Cuánto cobra por 6 h? ¿Cuántas horas ha trabajado si cobra 95 €?",
     tvf('15+8x', [0, 1, 2, 4, 6], yl='P') + r'\ \ $\res{P=8x+15}$. \ $P(6)=\res{63\text{ €}}$; \ $8x+15=95\Rightarrow\res{x=10\text{ h}}$.\newline ' + tg((0, 11, 0, 100), fns=[('15+8x', 0, 10)], ux=0.35, uy=0.03, tx=2, ty=20, gx=1, gy=10, xl='h', yl='€')),
 (2, r"El agua se congela a 0 °C (32 °F) y hierve a 100 °C (212 °F). La relación entre las dos escalas es lineal.\par a) Halla la fórmula que pasa de °C a °F. \ b) ¿Cuántos °F son 37 °C? \ c) ¿Cuántos °C son 50 °F? ¿Y $-4$ °F?",
     r"a) $m=\frac{212-32}{100}=1{,}8$: \ $\res{F=1{,}8C+32}$. \ b) $\res{98{,}6\text{ °F}}$. \ c) $1{,}8C+32=50\Rightarrow\res{C=10\text{ °C}}$; \ $1{,}8C+32=-4\Rightarrow\res{C=-20\text{ °C}}$."),
 (2, r"Un ciclista está a 6 km de casa y se aleja a una velocidad constante de 20 km/h. Escribe la distancia a casa en función del tiempo (en horas), represéntala y di cuándo estará a 56 km.",
     r"$\res{d(t)=6+20t}$. \ $6+20t=56\Rightarrow\res{t=2{,}5\text{ h}}$.\newline " + tg((0, 4, 0, 90), fns=[('6+20x', 0, 3.5)], dots=[(2.5, 56)], ux=0.9, uy=0.025, tx=1, ty=20, gx=0.5, gy=10, xl='t', yl='d')),
 (2, r"El precio de un pedido en una librería en línea es lineal respecto al número de ejemplares, por el envío fijo. 10 libros cuestan 23 € y 25 libros, 32 €. Halla la fórmula. ¿Cuánto cuesta el envío? ¿Cuánto cuestan 40 libros?",
     r"$m=\frac{32-23}{25-10}=0{,}6$: \ $\res{P=0{,}6x+17}$. \ Envío: $P(0)=\res{17\text{ €}}$. \ $P(40)=\res{41\text{ €}}$."),
 (3, r"Una empresa de alquiler de furgonetas cobra 60 € al día más 0,12 € por km. Escribe el precio de un día en función de los km, calcula el precio de 400 km y halla cuántos km se pueden hacer con 90 €. Representa la función.",
     r"$\res{P=0{,}12x+60}$. \ $P(400)=\res{108\text{ €}}$. \ $0{,}12x+60=90\Rightarrow\res{x=250\text{ km}}$.\newline " + tg((0, 550, 0, 130), fns=[('60+0.12x', 0, 500)], ux=0.012, uy=0.025, tx=100, ty=20, gx=50, gy=10, xl='km', yl='€')),
 (3, r"Una vela mide 18 cm. Después de estar encendida 6 horas, mide 15. Si se consume de manera lineal, escribe la altura en función del tiempo y di cuántas horas dura en total.",
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
S_.append(("Estudio conjunto de dos funciones lineales", [
 (1, r"Indica la posición relativa de cada pareja de rectas (secantes, paralelas o coincidentes):" + tasks(2, [r"$y=2x+3$ \ y \ $y=-2x+3$", r"$y=-x+4$ \ y \ $y=-x-1$", r"$y=3x-2$ \ y \ $2y=6x-4$", r"$y=\tfrac12x$ \ y \ $y=2x$"])
     + recorda(r"Pendientes diferentes: \textbf{secantes} (un punto común). Misma pendiente y $n$ diferente: \textbf{paralelas}. Misma pendiente y misma $n$: \textbf{coincidentes}."),
     tasks(2, [r"\rest{secantes} (se cortan en $(0,\,3)$)", r"\rest{paralelas}", r"$y=3x-2$: \rest{coincidentes}", r"\rest{secantes} (en el origen)"])),
 (1, r"Halla el punto de corte de las rectas:" + tasks(2, [r"$y=2x+1$ \ y \ $y=-x+7$", r"$y=3x-2$ \ y \ $y=x+4$", r"$y=-2x+5$ \ y \ $y=\tfrac12x$", r"$y=\tfrac13x+1$ \ y \ $y=-x+5$"])
     + recorda(r"En el punto de corte las dos $y$ son iguales: igualamos las expresiones, resolvemos la ecuación y sustituimos."),
     tasks(2, [r"$3x=6$: \ $\res{(2,\,5)}$", r"$2x=6$: \ $\res{(3,\,7)}$", r"$\tfrac52x=5$: \ $\res{(2,\,1)}$", r"$\tfrac43x=4$: \ $\res{(3,\,2)}$"])),
 (2, r"Representa en los mismos ejes $y=2x-3$ y $y=x$ y halla gráficamente el punto de corte. Compruébalo analíticamente.",
     tg((-2, 5, -4, 5), fns=[('2x-3',), ('x',)], dots=[(3, 3)], ux=0.32) + r"\quad Se cortan en $\res{(3,\,3)}$: \ $2x-3=x\Rightarrow x=3$, $y=3$."),
 (2, r"Resuelve gráficamente el sistema $\left\{\begin{array}{l} x+y=3\\ x-y=1\end{array}\right.$ \ (despeja la $y$ de cada ecuación y representa las dos rectas).",
     r"$y=-x+3$ y $y=x-1$: \ " + tg((-1, 4, -2, 4), fns=[('-x+3',), ('x-1',)], dots=[(2, 1)], ux=0.35) + r" \ Solución: $\res{x=2,\ y=1}$."),
 (2, r"Escribe una recta paralela y una secante a $y=-3x+1$ que pasen por el punto $(0,\,4)$. ¿Dónde corta la secante que has elegido a la recta $y=-3x+1$?",
     r"Paralela: $\res{y=-3x+4}$. Secante: cualquiera con $m\neq-3$, por ejemplo $\res{y=x+4}$, que corta a $y=-3x+1$ en $x+4=-3x+1\Rightarrow x=-\tfrac34$: $\res{(-\tfrac34,\,\tfrac{13}{4})}$."),
 (3, r"Dos empresas de alquiler de coches: A cobra 25 € al día más 0,40 € por km; B cobra 10 € al día más 0,60 € por km. Escribe las dos funciones, represéntalas y di cuál conviene según los km que hacemos en un día.",
     r"$A(x)=0{,}4x+25$, \ $B(x)=0{,}6x+10$. \ $0{,}4x+25=0{,}6x+10\Rightarrow\res{x=75\text{ km}}$ (55 €).\newline \rest{Menos de 75 km: B}; \ \rest{más de 75 km: A}." + r'\newline ' + tg((0, 130, 0, 90), fns=[('25+0.4x', 0, 120), ('10+0.6x', 0, 120)], dots=[(75, 55)], ux=0.04, uy=0.035, tx=25, ty=20, gx=25, gy=10, xl='km', yl='€')),
 (3, r"Un club de pádel cobra 300 € de cuota anual y 20 € por partido; otro no tiene cuota pero cobra 30 € por partido. ¿A partir de cuántos partidos al año conviene el primer club?",
     r"$300+20x=30x\Rightarrow x=30$ (900 €). \ \rest{A partir de 31 partidos} conviene el primero (con 30, cuestan igual)."),
 (3, r"Pablo sale de casa caminando a 5 km/h. Cuatro horas más tarde sale su hermana en bici por el mismo camino a 20 km/h. Escribe la distancia a casa de cada uno en función del tiempo desde que sale Pablo y halla cuándo y dónde lo alcanza.",
     r"$d_P(t)=5t$, \ $d_G(t)=20(t-4)$ para $t\ge4$. \ $5t=20t-80\Rightarrow t=\tfrac{16}{3}\approx5{,}33$ h. Lo alcanza \rest{5 h 20 min} después de salir Pablo, a $\res{\tfrac{80}{3}\approx26{,}7\text{ km}}$."),
]))
cut('x+4', '-3x+1', (R(-3, 4), R(13, 4))); cut('5x', '20(x-4)', (R(16, 3), R(80, 3)))
cut('-x+3', 'x-1', (2, 1))

# =====================================================================
# 6. Funcions quadràtiques: la paràbola y = ax²
# =====================================================================
roots('x^2-9', [-3, 3]); roots('-2x^2+8', [-2, 2]); roots('x^2+1', []); roots('3x^2', [0])
im('-3x^2/4', 2, -3); im('-3x^2/4', -4, -12)
S_.append(("Funciones cuadráticas: la parábola $y=ax^2$", [
 (1, r"Completa la tabla de valores de $y=x^2$ y de $y=-\tfrac12x^2$ y represéntalas en los mismos ejes." + r'\par\smallskip' + tasks(2, [r"$y=x^2$\\[3pt]" + tvbuida([-3, -2, -1, 0, 1, 2, 3]), r"$y=-\tfrac12x^2$\\[3pt]" + tvbuida([-3, -2, -1, 0, 1, 2, 3])])
     + recorda(r"La gráfica de $y=ax^2$ es una \textbf{parábola} con el vértice en $(0,\,0)$ y simétrica respecto al eje $Y$. Si $a>0$ se abre hacia arriba; si $a<0$, hacia abajo. Cuanto mayor es $|a|$, más cerrada es."),
     tasks(2, [tvf('x^2', [-3, -2, -1, 0, 1, 2, 3]), tvf('-x^2/2', [-3, -2, -1, 0, 1, 2, 3])]) + tg((-4, 4, -5, 9), fns=[('x^2',), ('-x^2/2',)], ux=0.3, uy=0.22, ty=2)),
 (1, r"Sin representarlas, di hacia dónde se abre cada parábola, si es más abierta o más cerrada que $y=x^2$ y si el vértice es un máximo o un mínimo:" + tasks(4, [r"$y=4x^2$", r"$y=-x^2$", r"$y=\tfrac15x^2$", r"$y=-3x^2$"]),
     tasks(2, [r"hacia arriba, \rest{más cerrada}, mínimo", r"hacia abajo, \rest{igual}, máximo", r"hacia arriba, \rest{más abierta}, mínimo", r"hacia abajo, \rest{más cerrada}, máximo"])),
 (1, r"Asocia cada parábola con su ecuación: \quad $y=2x^2$, \ \ $y=-x^2+3$, \ \ $y=\tfrac12x^2$, \ \ $y=x^2-2$." + r'\par\smallskip'
     + tasks(4, [tg((-3, 3, -3, 4), fns=[('x^2/2',)], ux=0.28), tg((-3, 3, -3, 4), fns=[('x^2-2',)], ux=0.28), tg((-3, 3, -3, 4), fns=[('2x^2',)], ux=0.28), tg((-3, 3, -3, 4), fns=[('-x^2+3',)], ux=0.28)]),
     tasks(4, [r"$\res{y=\tfrac12x^2}$", r"$\res{y=x^2-2}$", r"$\res{y=2x^2}$", r"$\res{y=-x^2+3}$"])),
 (2, r"Indica el vértice de cada parábola y sus puntos de corte con los ejes:" + tasks(2, [r"$y=x^2-9$", r"$y=-2x^2+8$", r"$y=x^2+1$", r"$y=3x^2$"]),
     tasks(2, [r"$V\res{(0,\,-9)}$; cortes $\res{(\pm3,\,0)}$", r"$V\res{(0,\,8)}$; cortes $\res{(\pm2,\,0)}$", r"$V\res{(0,\,1)}$; \rest{no corta} el eje $X$", r"$V\res{(0,\,0)}$; solo corta en el origen"])),
 (2, r"Halla el valor de $a$ para que la parábola $y=ax^2$ pase por el punto $(2,\,-3)$. ¿Qué otra imagen conocemos sin calcular? Calcula también la imagen de $x=-4$.",
     r"$4a=-3\Rightarrow\res{a=-\tfrac34}$. Por simetría, $(-2,\,-3)$ también es de la parábola. \ $y(-4)=-\tfrac34\cdot16=\res{-12}$."),
 (3, r"Escribe la ecuación de una parábola de la forma $y=ax^2+c$ que tenga el vértice en $(0,\,4)$ y corte el eje $X$ en $x=2$. Represéntala.",
     r"$c=4$ y $4a+4=0\Rightarrow a=-1$: \ $\res{y=-x^2+4}$. \ " + tg((-3, 3, -2, 5), fns=[('-x^2+4',)], dots=[(0, 4), (-2, 0), (2, 0)], ux=0.32)),
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
S_.append(("Representación de $y=ax^2+bx+c$", [
 (1, r"Calcula el vértice y el eje de simetría de cada parábola y di si el vértice es un máximo o un mínimo:" + tasks(2, [r"$y=x^2-4x+1$", r"$y=-x^2+6x-8$", r"$y=2x^2+8x+3$", r"$y=-3x^2+6x$", r"$y=x^2+3x$"])
     + recorda(r"Vértice: $x_v=\dfrac{-b}{2a}$ y $y_v=f(x_v)$. El eje de simetría es la recta $x=x_v$. Si $a>0$ el vértice es un mínimo; si $a<0$, un máximo."),
     tasks(2, [r"$V\res{(2,\,-3)}$, eje $x=2$, mínimo", r"$V\res{(3,\,1)}$, eje $x=3$, máximo", r"$V\res{(-2,\,-5)}$, eje $x=-2$, mínimo", r"$V\res{(1,\,3)}$, eje $x=1$, máximo", r"$V\res{(-\tfrac32,\,-\tfrac94)}$, eje $x=-\tfrac32$, mínimo"])),
 (1, r"Halla los puntos de corte con los ejes:" + tasks(2, [r"$y=x^2-6x+5$", r"$y=-x^2+2x+3$", r"$y=x^2-4x+4$", r"$y=x^2+2x+5$", r"$y=2x^2-x-3$"]),
     tasks(2, [r"$(0,\,5)$; \ $\res{(1,\,0)}$, $\res{(5,\,0)}$", r"$(0,\,3)$; \ $\res{(-1,\,0)}$, $\res{(3,\,0)}$", r"$(0,\,4)$; \ $\res{(2,\,0)}$ (el vértice)", r"$(0,\,5)$; \ $\Delta=-16<0$: \rest{ninguno}", r"$(0,\,-3)$; \ $\res{(-1,\,0)}$, $\res{(\tfrac32,\,0)}$"])),
 (2, r"Estudia (forma, vértice, eje, cortes con los ejes) y representa $y=x^2-2x-8$.",
     r"$a>0$: hacia arriba. \ $V\res{(1,\,-9)}$, eje $x=1$. \ Cortes: $\res{(0,\,-8)}$, $\res{(-2,\,0)}$, $\res{(4,\,0)}$.\newline " + tvf('x^2-2x-8', [-2, -1, 0, 1, 2, 3, 4]) + r'\quad ' + tg((-3, 5, -10, 2), fns=[('x^2-2x-8',)], guides=[1], dots=[(1, -9), (-2, 0), (4, 0), (0, -8)], ux=0.3, uy=0.2, ty=2)),
 (2, r"Estudia y representa $y=-x^2-2x+3$.",
     r"$a<0$: hacia abajo. \ $V\res{(-1,\,4)}$ (máximo), eje $x=-1$. \ Cortes: $\res{(0,\,3)}$, $\res{(-3,\,0)}$, $\res{(1,\,0)}$.\newline " + tvf('-x^2-2x+3', [-4, -3, -2, -1, 0, 1, 2]) + r'\quad ' + tg((-5, 3, -6, 5), fns=[('-x^2-2x+3',)], guides=[-1], dots=[(-1, 4), (-3, 0), (1, 0), (0, 3)], ux=0.3, uy=0.25)),
 (2, r"Representa $y=x^2+4x+5$ con una tabla de valores alrededor del vértice. ¿Por qué no corta el eje $X$?",
     r"$V\res{(-2,\,1)}$, eje $x=-2$. " + tvf('x^2+4x+5', [-4, -3, -2, -1, 0]) + r" \ $\Delta=16-20<0$: el vértice es un mínimo por encima del eje, \rest{no lo corta}.\newline " + tg((-5, 1, -1, 6), fns=[('x^2+4x+5',)], guides=[-2], dots=[(-2, 1), (0, 5), (-4, 5)], ux=0.32)),
 (2, r"Asocia cada parábola con su ecuación: \quad $y=x^2-4x+3$, \ \ $y=-x^2+4x-4$, \ \ $y=x^2+2x$." + r'\par\smallskip'
     + tasks(3, [tg((-3, 5, -4, 4), fns=[('-x^2+4x-4',)], ux=0.26), tg((-3, 5, -4, 4), fns=[('x^2+2x',)], ux=0.26), tg((-3, 5, -4, 4), fns=[('x^2-4x+3',)], ux=0.26)]),
     tasks(1, [r"$\res{y=-x^2+4x-4}$ (hacia abajo, $V(2,\,0)$)", r"$\res{y=x^2+2x}$ (pasa por el origen)", r"$\res{y=x^2-4x+3}$ ($V(2,\,-1)$)"])),
 (3, r"Indica los intervalos de crecimiento y decrecimiento y el máximo o mínimo de $y=-2x^2+8x-5$.",
     r"$x_v=\frac{-8}{-4}=2$, $y_v=-8+16-5=3$; $a<0$: \rest{crece} en $\res{(-\infty,\,2)}$, \rest{decrece} en $\res{(2,\,+\infty)}$; \ máximo $\res{(2,\,3)}$."),
 (3, r"Halla $b$ para que el vértice de la parábola $y=x^2+bx+5$ esté en $x=3$. ¿Cuál es entonces el vértice? ¿Corta el eje $X$?",
     r"$\frac{-b}{2}=3\Rightarrow\res{b=-6}$. \ $y=x^2-6x+5$, \ $V\res{(3,\,-4)}$. \ \rest{Sí}: en $(1,\,0)$ y $(5,\,0)$."),
 (3, r"Escribe la ecuación de la parábola $y=x^2+bx+c$ que pasa por los puntos $(0,\,3)$ y $(1,\,0)$. Halla su vértice.",
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
S_.append(("Problemas con parábolas", [
 (1, r"Lanzamos un cohete de juguete hacia arriba y su altura (en m) al cabo de $t$ segundos es $h(t)=40t-5t^2$.\par a) ¿Qué altura máxima alcanza y en qué momento? \ b) ¿Cuándo vuelve al suelo? \ c) Representa la función en su dominio con sentido.",
     r"a) $t_v=\frac{-40}{-10}=4$ s, \ $h(4)=\res{80\text{ m}}$ \ a los $\res{4\text{ s}}$. \ b) $5t(8-t)=0\Rightarrow\res{t=8\text{ s}}$. \ c) Dominio $[0,\,8]$:\newline " + tg((0, 9, 0, 90), fns=[('40x-5x^2', 0, 8)], guides=[4], dots=[(4, 80)], ux=0.45, uy=0.035, tx=1, ty=20, gx=1, gy=10, xl='t', yl='h')
     + recorda(r"En un problema, el valor máximo o mínimo de una función cuadrática está en el \textbf{vértice}: $x_v$ dice cuándo (o con qué valor) y $y_v$, cuánto vale.")),
 (1, r"Dos números suman 30. Escribe su producto en función de uno de ellos y halla cuáles son si el producto es máximo.",
     r"$P(x)=x(30-x)=-x^2+30x$. \ $x_v=15$: \ los números son $\res{15\text{ y }15}$ (producto máximo $\res{225}$)."),
 (2, r"Con 60 m de valla queremos hacer un corral rectangular aprovechando una pared (solo hace falta valla en tres lados). Si $x$ es la longitud de los lados perpendiculares a la pared, escribe el área en función de $x$ y halla las dimensiones del área máxima.",
     r"Lado paralelo: $60-2x$. \ $A(x)=x(60-2x)=-2x^2+60x$. \ $x_v=15$: \ $\res{15\text{ m}\times30\text{ m}}$, área $\res{450\text{ m}^2}$."),
 (2, r"Desde lo alto de un edificio de 25 m lanzamos una pelota hacia arriba y su altura es $h(t)=25+20t-5t^2$. ¿Qué altura máxima alcanza? ¿Cuándo llega al suelo?",
     r"$t_v=2$ s, \ $h(2)=\res{45\text{ m}}$. \ $25+20t-5t^2=0\Rightarrow t^2-4t-5=0\Rightarrow t=5$ o $t=-1$ (no tiene sentido): \ $\res{t=5\text{ s}}$."),
 (2, r"Un rectángulo tiene 32 cm de perímetro. Escribe su área en función de la base $x$, haz una tabla para $x=2,\,4,\,6,\,8,\,10,\,12,\,14$ y di qué base da el área máxima.",
     r"Base + altura $=16$: $A(x)=x(16-x)$. \ " + tvf('x(16-x)', [2, 4, 6, 8, 10, 12, 14], yl='A') + r" \ Máximo para $\res{x=8}$: un cuadrado de 8 cm ($\res{64\text{ cm}^2}$)."),
 (3, r"Una agencia de viajes vende 400 billetes a 10 € cada uno. Por cada euro que sube el precio, vende 20 menos. Escribe los ingresos en función de la subida $x$ y halla qué precio da los ingresos máximos.",
     r"$I(x)=(10+x)(400-20x)=-20x^2+200x+4000$. \ $x_v=5$: precio $\res{15\text{ €}}$, vende 300 billetes e ingresa $\res{4500\text{ €}}$."),
 (3, r"El beneficio diario (en €) de una tienda en función del número $x$ de trabajadores es $B(x)=-x^2+12x-20$. ¿Cuántos trabajadores dan el beneficio máximo? ¿Con cuántos trabajadores no hay pérdidas?",
     r"$x_v=6$: \ $\res{6\text{ trabajadores}}$ (16 €). \ $B(x)=0\Rightarrow x=2$ y $x=10$; \ $B\ge0$ entre los dos: \rest{de 2 a 10 trabajadores}."),
]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = 'pdfkeywords={proporcionalitat directa, funció lineal, pendent, ordenada en l\'origen, equació de la recta, punt de tall, paràbola, vèrtex, funció quadràtica}'
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

pre = pre_

def build(sol_):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, ASSIGNATURA
    t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 8: Función lineal y cuadrática' % t, capcalera='%s · Unidad 8: Función lineal y cuadrática' % t,
                 pdfkeywords='proporcionalidad directa, función lineal, pendiente, ordenada en el origen, ecuación de la recta, punto de corte, parábola, vértice, función cuadrática')
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

''' + ASSIGNATURA + '{' + ('Soluciones de la ficha · Unidad 8' if sol_ else 'Ficha de ejercicios · Unidad 8') + '}{Función lineal y cuadrática}\n')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás herramientas que calculan rectas por dos puntos, puntos de corte y el estudio completo de una parábola."
             if sol_ else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Para dibujar gráficas, utiliza papel cuadriculado y elige una escala adecuada para cada eje.") + r'''
\end{tcolorbox}
''')
    num, k = {}, 0
    for i, (_, exs) in enumerate(S_, 1):
        for j in range(1, len(exs) + 1):
            k += 1; num['@S%dE%d@' % (i, j)] = str(k)
    ref = lambda t: re.sub(r'@S\d+E\d+@', lambda m: num[m.group(0)], t)
    n = 0
    refs = globals().get('REFS', {})
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st, q, s) in enumerate(exs):
            n += 1
            lab = ''.join(r'\label{%s}' % kk for kk, (tt, jj) in refs.items() if tt == title and jj == j)
            out.append('\\ex{%d}%s %s\n\n' % (st, lab, ref(s if sol_ else q)))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't8-fitxa-solucions-es.tex' if sol_ else 't8-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
