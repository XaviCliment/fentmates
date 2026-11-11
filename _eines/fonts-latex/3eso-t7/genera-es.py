# Versió en castellà de genera.py. Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (3r ESO, Unitat 7: Funcions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les gràfiques poligonals les estudia pl.py (el mateix mòdul que els apunts interactius), que comprova
# cada resultat per mostreig; les solucions d'aquests exercicis s'escriuen a partir d'aquest estudi.
# Les imatges, antiimatges i punts de tall es comproven amb sympy (im, roots).
import os, re, sys, math
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '3eso-t7'))
import pl
from pl import F, INF

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- comprovacions ----------
x = sp.Symbol('x')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def E(s): return sp.nsimplify(parse_expr(s.replace(',', '.'), transformations=TR, local_dict={'x': x}), rational=True)
def im(s, a, want):
    v = E(s).subs(x, sp.nsimplify(a)); assert sp.simplify(v - sp.nsimplify(want)) == 0, (s, a, v, want)
def roots(s, want):
    r = sorted(sp.solve(E(s), x), key=lambda t: float(t)) if sp.solve(E(s), x) and all(t.is_real for t in sp.solve(E(s), x)) else [t for t in sp.solve(E(s), x) if t.is_real]
    assert [sp.nsimplify(t) for t in r] == [sp.nsimplify(w) for w in want], (s, r, want)
def nt(v):
    v = sp.nsimplify(v)
    if v.is_Integer: return str(v)
    d = float(v); s = '%g' % d
    if sp.nsimplify(s) == v: return s.replace('.', '{,}')
    return ('-' if v < 0 else '') + r'\tfrac{%d}{%d}' % (abs(v.p), v.q)
def tvf(s, xs, yl='y', xl='x'):
    """taula de valors (calculada amb sympy)"""
    ys = [nt(E(s).subs(x, sp.nsimplify(a))) for a in xs]
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('c' * len(xs), xl, '&'.join(nt(a) for a in xs), yl, '&'.join(ys)))
def tvbuida(xs, yl='y', xl='x'):
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('C{0.7cm}' * len(xs), xl, '&'.join(nt(a) for a in xs), yl, '&'.join([r'\phantom{00}'] * len(xs))))

# ---------- estudi de les gràfiques (pl.py) ----------
def S(iv): return pl.settex(iv)
def PT(P): return pl.pttex(P)
def st(f): return pl.check(f)
def pts(L): return ',\\ '.join(PT(P) for P in L) if L else r'\text{no tiene}'
def absol(A): return (r'%s\ \text{(en }%s)' % (pl.num(A[0]), ',\\,'.join('x=' + pl.num(t) for t in A[1]))) if A else r'\text{no tiene}'
def domrec(f): s = st(f); return r'$\mathrm{Dom}=\res{%s}$; \ $\mathrm{Rec}=\res{%s}$' % (S(s['dom']), S(s['rec']))
def monot(f):
    s = st(f)
    parts = [r'%s: $\res{%s}$' % (nm, S(s['mono'][k])) for k, nm in (('+', 'crece'), ('-', 'decrece'), ('0', 'constante')) if s['mono'][k]]
    return r'; \ '.join(parts)
def extr(f, absolut=False):
    s = st(f); out = r'máx.\ rel.: $\res{%s}$; \ mín.\ rel.: $\res{%s}$' % (pts(s['max']), pts(s['min']))
    if absolut: out += r'\newline máx.\ abs.: $\res{%s}$; \ mín.\ abs.: $\res{%s}$' % (absol(s['amax']), absol(s['amin']))
    return out
TIPUS = {'salt': 'salto', 'forat': 'falta un punto o está desplazado', 'aillat': 'punto aislado'}
def cont(f):
    s = st(f)
    if not s['disc']: return r'\rest{continua}'
    return r'\rest{discontinua} en ' + ', '.join(r'$x=%s$ (%s)' % (pl.num(a), TIPUS[t]) for a, t in s['disc'])

# ---------- gràfiques (TikZ) ----------
def axes(win, tx=1, ty=1, gx=1, gy=1, xl='x', yl='y', lab=True):
    x0, x1, y0, y1 = win
    o = [r'\draw[muted!22,very thin,xstep=%s,ystep=%s] (%s,%s) grid (%s,%s);' % (gx, gy, x0, y0, x1, y1)]
    ax = min(max(0, y0), y1); ay = min(max(0, x0), x1)
    o.append(r'\draw[-latex,muted] (%s,%s)--(%s,%s) node[right,font=\scriptsize]{$%s$};' % (x0, ax, x1 + 0.35 * gx, ax, xl))
    o.append(r'\draw[-latex,muted] (%s,%s)--(%s,%s) node[above,font=\scriptsize]{$%s$};' % (ay, y0, ay, y1 + 0.35 * gy, yl))
    if lab:
        k = math.ceil(x0 / tx) * tx
        while k < x1:
            if k: o.append(r'\node[font=\tiny,muted,below] at (%s,%s) {%s};' % (k, ax, pl.num(k, ',')))
            k += tx
        k = math.ceil(y0 / ty) * ty
        while k < y1:
            if k: o.append(r'\node[font=\tiny,muted,left] at (%s,%s) {%s};' % (ay, k, pl.num(k, ',')))
            k += ty
    return o
def tg(f, win=None, ux=0.32, uy=None, tx=2, ty=2, gx=1, gy=1, xl='x', yl='y', curves=(), fns=(), dots=(), col='accent'):
    """gràfica d'una funció poligonal (punts plens / buits, fletxes) i corbes opcionals"""
    if win is None and f is not None:
        xs = [P[0] for p in f['p'] for P in p['v']] + [P[0] for P in f['pts']]
        ys = [P[1] for p in f['p'] for P in p['v']] + [P[1] for P in f['pts']]
        a, b = min(min(xs), 0) - 1, max(max(xs), 0) + 1
        c, d = min(min(ys), 0) - 1, max(max(ys), 0) + 1
        if any(p['l'] == 'a' for p in f['p']): a -= 1
        if any(p['r'] == 'a' for p in f['p']): b += 1
        win = (int(a), int(b), int(c), int(d))
    x0, x1, y0, y1 = win
    uy = uy or ux
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center)]' % (ux, uy)] + axes(win, tx, ty, gx, gy, xl, yl)
    o.append(r'\begin{scope}\clip (%s,%s) rectangle (%s,%s);' % (x0, y0, x1, y1))
    for c in curves:
        sharp = c[0] == 'poly'
        c = c[1] if sharp else c
        o.append(r'\draw[teal,line width=1.1pt] %s;' % (('--'.join('(%.3f,%.3f)' % P for P in c)) if sharp else 'plot[smooth] coordinates {%s}' % ' '.join('(%.3f,%.3f)' % P for P in c)))
    for s, a, b in fns:
        fl = sp.lambdify(x, E(s)); seg = []
        for i in range(161):
            t = a + (b - a) * i / 160
            try: v = float(fl(t))
            except ZeroDivisionError: v = float('nan')
            if v == v and y0 - 3 <= v <= y1 + 3: seg.append((t, v))
        o.append(r'\draw[%s,line width=1.1pt] plot[smooth] coordinates {%s};' % (col, ' '.join('(%.3f,%.3f)' % P for P in seg)))
    def ray(P, Q, back):
        m = float(pl.slope(P, Q)); dx = -1 if back else 1
        t = ((x0 if back else x1) - float(P[0])) * dx
        if abs(m) > 1e-12: t = min(t, ((y1 if m * dx > 0 else y0) - float(P[1])) / (m * dx))
        t = max(t - 0.2, 0.2)
        return r'\draw[%s,line width=1.1pt,-latex] (%s,%s)--(%.3f,%.3f);' % (col, float(P[0]), float(P[1]), float(P[0]) + dx * t, float(P[1]) + m * dx * t)
    if f:
        for p in f['p']:
            v = p['v']
            if len(v) > 1: o.append(r'\draw[%s,line width=1.1pt] %s;' % (col, '--'.join('(%s,%s)' % (float(P[0]), float(P[1])) for P in v)))
            if p['l'] == 'a': o.append(ray(v[0], v[1], True))
            if p['r'] == 'a': o.append(ray(v[-1], v[-2], False))
    o.append(r'\end{scope}')
    def dot(P, full):
        return (r'\fill[%s] (%s,%s) circle (2.2pt);' % (col, float(P[0]), float(P[1])) if full
                else r'\filldraw[fill=white,draw=%s,line width=0.9pt] (%s,%s) circle (2.2pt);' % (col, float(P[0]), float(P[1])))
    if f:
        for p in f['p']:
            v = p['v']
            if p['l'] != 'a': o.append(dot(v[0], p['l'] == 'c'))
            if p['r'] != 'a' and len(v) > 1: o.append(dot(v[-1], p['r'] == 'c'))
        for P in f['pts']: o.append(dot(P, True))
    for P in dots: o.append(r'\fill[navy] (%s,%s) circle (2.4pt);' % P)
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Concepte de funció
# =====================================================================
fA1 = F(('c', [(-4, 2), (-2, -2), (1, 3), (4, 1)], 'c'))
circ = [(3 * math.cos(t * math.pi / 30), 3 * math.sin(t * math.pi / 30)) for t in range(61)]
side = [(t / 10 * t / 10 / 2 - 3, t / 10) for t in range(-40, 41)]
zig = [(-4, -3), (0, 3), (-2, 0), (4, 2)]
W5 = (-5, 5, -4, 4)
S_.append(("Concepto de función", [
 (1, r"Indica si cada relación es una función:" + tasks(2, [r"A cada número natural, su cuadrado.", r"A cada persona, sus hermanos.", r"A cada cantidad de litros de gasolina, el precio que pagamos.", r"A cada $x>0$, sus raíces cuadradas.", r"A cada alumno, la nota del último examen.", r"A cada nota, los alumnos que la han sacado."])
     + recorda(r"Una relación es una función si a \textbf{cada} valor de la variable independiente ($x$) le corresponde \textbf{un único} valor de la variable dependiente ($y$)."),
     tasks(2, [r"\rest{sí}", r"\rest{no}: puede tener varios (o ninguno)", r"\rest{sí}", r"\rest{no}: el 9 tiene el 3 y el $-3$", r"\rest{sí}", r"\rest{no}: puede haber varios"])),
 (1, r"En cada relación, ¿cuál es la variable independiente y cuál la dependiente?" + tasks(1, [r"La duración de una llamada y lo que cuesta.", r"El número de obreros y el tiempo que tardan en acabar una obra.", r"El lado de un triángulo equilátero y su perímetro."]),
     tasks(1, [r"Independiente: \rest{la duración}; dependiente: \rest{el coste}.", r"Independiente: \rest{el número de obreros}; dependiente: \rest{el tiempo}.", r"Independiente: \rest{el lado}; dependiente: \rest{el perímetro} ($P=3x$)."])),
 (1, r"¿Cuáles de estas gráficas corresponden a una función?\par\smallskip" + tasks(4, [tg(fA1, W5, ux=0.27), tg(None, W5, ux=0.27, curves=[circ]), tg(None, W5, ux=0.27, curves=[side]), tg(None, W5, ux=0.27, curves=[('poly', zig)])]),
     r"Hacemos la prueba de la recta vertical:" + tasks(4, [r"\rest{sí}", r"\rest{no}", r"\rest{no}", r"\rest{no}"]) + r"En b), c) y d) hay rectas verticales que cortan la gráfica en dos o más puntos."),
 (2, r"¿Las siguientes tablas definen una función de $x$?" + tasks(2, [r"$\begin{array}{|c|c|c|c|c|}\hline x&1&2&2&3\\\hline y&4&5&6&7\\\hline\end{array}$", r"$\begin{array}{|c|c|c|c|c|}\hline x&1&2&3&4\\\hline y&5&5&5&6\\\hline\end{array}$"]),
     tasks(2, [r"\rest{no}: el 2 tiene dos imágenes (5 y 6)", r"\rest{sí}: cada $x$ tiene una sola $y$ (que se repita la $y$ no importa)"])),
 (2, r"Explica por qué la recta $y=3$ es la gráfica de una función y la recta $x=3$ no lo es.",
     r"En $y=3$, a cada $x$ le corresponde una sola imagen, el 3: \rest{es función} (constante). En $x=3$, al valor $x=3$ le corresponden infinitos valores de $y$: \rest{no es función} (la misma recta vertical la corta en infinitos puntos)."),
 (3, r"Dibuja una gráfica que pase por los puntos $(-2,\,1)$, $(0,\,3)$ y $(3,\,1)$ y que sea una función, y otra que pase por los mismos puntos y que \textbf{no} lo sea.",
     r"Respuesta abierta. Por ejemplo, la poligonal que une los tres puntos de izquierda a derecha \rest{es función}; una curva cerrada (como una circunferencia) que pase por los tres puntos \rest{no lo es}."),
 (3, r"A cada número $x$ le hacemos corresponder el número $y$ que cumple $y^2=x$. ¿Es una función? ¿Y si la condición es $y^3=x$?",
     r"$y^2=x$: para $x=4$, $y=2$ o $y=-2$: \rest{no es función}. $y^3=x$: cada número tiene una única raíz cúbica (por ejemplo, $y^3=8\Rightarrow y=2$; $y^3=-8\Rightarrow y=-2$): \rest{sí es función}."),
]))

# =====================================================================
# 2. Expressió d'una funció
# =====================================================================
for a, v in [(0, -5), (2, 1), (-3, -14), (Fr(1, 2), Fr(-7, 2))]: im('3x-5', a, v)
for a, v in [(0, 3), (1, 0), (-2, 15), (5, 8)]: im('x^2-4x+3', a, v)
for a, v in [(4, 3), (-2, -1), (1, 1)]: im('(2x+1)/3', a, v)
for a, v in [(4, 3), (-1, 2), (11, 4)]: im('sqrt(x+5)', a, v)
im('5x-3', 3, 12); im('5x-3', -1, -8); im('5x-3', Fr(3, 5), 0)
im('x^2-1', 3, 8); im('x^2-1', -3, 8); im('x^2-1', 0, -1); assert sp.solve(E('x^2-1+5'), x) and all(not t.is_real for t in sp.solve(E('x^2+4'), x))
for a in range(5): im('4x+3', a, 4 * a + 3)
for a in range(1, 5): im('x^2', a, a * a)
im('2+0,15x', 40, 8); im('2+0,15x', 60, 11)
im('4x+3', 2, 11); im('4x+3', -1, -1)
S_.append(("Expresión de una función", [
 (1, r"Dada la función $f(x)=3x-5$, calcula:" + tasks(4, [r"$f(0)$", r"$f(2)$", r"$f(-3)$", r"$f\!\left(\tfrac12\right)$"])
     + recorda(r"Para calcular la imagen $f(a)$, sustituimos la $x$ por $a$ en la fórmula. Los números negativos, entre paréntesis."),
     tasks(4, [r"$\res{-5}$", r"$6-5=\res{1}$", r"$-9-5=\res{-14}$", r"$\tfrac32-5=\res{-\tfrac72}$"])),
 (1, r"Si $g(x)=x^2-4x+3$, calcula $g(0)$, $g(1)$, $g(-2)$ y $g(5)$.",
     r"$g(0)=\res{3}$; \ $g(1)=1-4+3=\res{0}$; \ $g(-2)=4+8+3=\res{15}$; \ $g(5)=25-20+3=\res{8}$"),
 (1, r"Completa las tablas de valores:" + tasks(2, [r"$y=2x-1$\\[3pt]" + tvbuida([-2, -1, 0, 1, 2]), r"$y=-x^2+3$\\[3pt]" + tvbuida([-2, -1, 0, 1, 2])]),
     tasks(2, [tvf('2x-1', [-2, -1, 0, 1, 2]), tvf('-x^2+3', [-2, -1, 0, 1, 2])])),
 (2, r"Calcula las imágenes que se indican:" + tasks(2, [r"$h(x)=\dfrac{2x+1}{3}$: \ $h(4)$, $h(-2)$, $h(1)$", r"$k(x)=\sqrt{x+5}$: \ $k(4)$, $k(-1)$, $k(11)$"]),
     tasks(2, [r"$\tfrac93=\res{3}$; \ $\tfrac{-3}{3}=\res{-1}$; \ $\tfrac33=\res{1}$", r"$\sqrt9=\res{3}$; \ $\sqrt4=\res{2}$; \ $\sqrt{16}=\res{4}$"])),
 (2, r"Dada $f(x)=5x-3$, halla la antiimagen de:" + tasks(3, [r"$12$", r"$-8$", r"$0$"])
     + recorda(r"Para hallar la antiimagen de $k$, resolvemos la ecuación $f(x)=k$."),
     tasks(3, [r"$5x-3=12\Rightarrow\res{x=3}$", r"$5x-3=-8\Rightarrow\res{x=-1}$", r"$5x=3\Rightarrow\res{x=\tfrac35}$"])),
 (2, r"Dada $f(x)=x^2-1$, ¿qué valores de $x$ tienen por imagen:" + tasks(3, [r"$8$", r"$-1$", r"$-5$"]),
     tasks(3, [r"$x^2=9\Rightarrow\res{x=\pm3}$", r"$x^2=0\Rightarrow\res{x=0}$", r"$x^2=-4$: \rest{ninguno}"])),
 (2, r"Escribe la fórmula de cada función:" + tasks(1, [r"El perímetro de un rectángulo de base $x$ y altura 4 cm.", r"El precio de $x$ entradas de concierto a 8,50 € cada una.", r"El área de un círculo de radio $x$.", r"El tiempo que se tarda en hacer 300 km a una velocidad de $x$ km/h."]),
     tasks(1, [r"$\res{P(x)=2x+8}$", r"$\res{f(x)=8{,}5x}$", r"$\res{A(x)=\pi x^2}$", r"$\res{t(x)=\tfrac{300}{x}}$"])),
 (2, r"Halla la fórmula de las funciones que dan estas tablas:" + tasks(2, [tvf('4x+3', [0, 1, 2, 3, 4]), tvf('x^2', [1, 2, 3, 4])]),
     tasks(1, [r"Aumenta 4 cada vez y vale 3 en $x=0$: $\res{y=4x+3}$", r"Cada $y$ es el cuadrado de la $x$: $\res{y=x^2}$"])),
 (3, r"Una tienda de fotografía cobra 2 € por el envío más 0,15 € por cada foto revelada. Escribe la fórmula del precio en función del número de fotos, calcula el precio de 40 fotos y cuántas fotos podemos revelar con 11 €.",
     r"$f(x)=2+0{,}15x$. \ $f(40)=2+6=\res{8\text{ €}}$. \ $2+0{,}15x=11\Rightarrow 0{,}15x=9\Rightarrow\res{x=60}$ fotos."),
 (3, r"La función $f(x)=ax+3$ cumple que $f(2)=11$. Halla $a$ y calcula $f(-1)$.",
     r"$2a+3=11\Rightarrow\res{a=4}$. \ $f(x)=4x+3$, \ $f(-1)=-4+3=\res{-1}$"),
]))

# =====================================================================
# 3. Les funcions i els seus gràfics
# =====================================================================
for a in range(-1, 4): im('2x-3', a, 2 * a - 3)
roots('2x-3', [Fr(3, 2)]); roots('x^2-4', [-2, 2]); roots('3x+6', [-2]); roots('x^2-5x+6', [2, 3]); roots('x^3-4x', [-2, 0, 2])
assert all(not t.is_real for t in sp.solve(E('x^2+1'), x))
bici = F(('c', [(0, 0), (2, 30), (3, 30), (4, 40), (6, 0)], 'c'))
assert pl.value(bici, 5) == 20 and pl.value(bici, 1) == 15 and pl.value(bici, Fr(21, 4)) == 15
temp = F(('c', [(0, 4), (6, 0), (14, 16), (20, 10), (24, 6)], 'c'))
assert pl.value(temp, 10) == 8 and pl.value(temp, 11) == 10 and pl.value(temp, 20) == 10
for a in [1, 2, 3, 4, 6]: im('12/x', a, Fr(12, a)); im('12/x', -a, Fr(-12, a))
# gràfiques per a associar amb situacions
gI = tg(None, (-1, 6, -1, 6), ux=0.3, tx=10, ty=10, fns=[('5-(x-2.5)^2*0.8', 0, 5)], xl='t', yl='y')
gII = tg(F(('c', [(0, 0), (2, 5), (4, 5), (5, 0)], 'c')), (-1, 6, -1, 6), ux=0.3, tx=10, ty=10, xl='t', yl='y')
gIII = tg(None, (-1, 6, -1, 6), ux=0.3, tx=10, ty=10, fns=[('x', 0, 5.5)], xl='x', yl='y')
gIV = tg(None, (-1, 6, -1, 6), ux=0.3, tx=10, ty=10, fns=[('1+4*exp(-0.6*x)', 0, 5.5)], xl='t', yl='y')
S_.append(("Las funciones y sus gráficas", [
 (1, r"Haz una tabla de valores de $f(x)=2x-3$ para $x=-1,\,0,\,1,\,2,\,3$, representa la función y halla los puntos de corte con los ejes."
     + recorda(r"Corte con el eje $Y$: hacemos $x=0$. Corte con el eje $X$: resolvemos $f(x)=0$."),
     tvf('2x-3', [-1, 0, 1, 2, 3]) + r'\qquad ' + tg(None, (-3, 5, -6, 5), ux=0.28, fns=[('2x-3', -3, 5)], dots=[(0, -3), (1.5, 0)])
     + r'\newline Cortes: $\res{(0,\,-3)}$ y $\res{\left(\tfrac32,\,0\right)}$'),
 (1, r"Haz una tabla de valores de $g(x)=x^2-4$ para $x$ entre $-3$ y $3$ y represéntala. ¿Dónde corta a los ejes?",
     tvf('x^2-4', [-3, -2, -1, 0, 1, 2, 3]) + r'\qquad ' + tg(None, (-4, 4, -5, 6), ux=0.28, fns=[('x^2-4', -3.2, 3.2)], dots=[(0, -4), (-2, 0), (2, 0)])
     + r'\newline Cortes: $\res{(0,\,-4)}$, $\res{(-2,\,0)}$ y $\res{(2,\,0)}$'),
 (2, r"Halla los puntos de corte con los ejes:" + tasks(2, [r"$f(x)=3x+6$", r"$g(x)=x^2-5x+6$", r"$h(x)=x^2+1$", r"$k(x)=x^3-4x$"]),
     tasks(2, [r"$\res{(0,\,6)}$, $\res{(-2,\,0)}$", r"$\res{(0,\,6)}$, $\res{(2,\,0)}$, $\res{(3,\,0)}$", r"$\res{(0,\,1)}$; con el eje $X$, \rest{ninguno} ($x^2=-1$)", r"$x(x^2-4)=0$: $\res{(0,\,0)}$, $\res{(2,\,0)}$, $\res{(-2,\,0)}$"])),
 (2, r"La gráfica muestra la distancia a casa de un ciclista durante una salida.\par\smallskip\begin{center}" + tg(bici, (0, 7, 0, 45), ux=0.9, uy=0.07, tx=1, ty=10, gx=1, gy=5, xl='t\\ (\\mathrm{h})', yl='d\\ (\\mathrm{km})') + r"\end{center}"
     + tasks(1, [r"¿Cuántos kilómetros recorre en total?", r"¿Cuánto tiempo está parado?", r"¿A qué velocidad va en las dos primeras horas? ¿Y en la vuelta?", r"¿A qué distancia de casa está a las 5 h?", r"¿En qué momentos está a 15 km de casa?"]),
     tasks(1, [r"$40+40=\res{80\text{ km}}$", r"De 2 a 3 h: \rest{1 hora}", r"$30:2=\res{15\text{ km/h}}$; vuelta: $40:2=\res{20\text{ km/h}}$", r"$\res{20\text{ km}}$", r"A la ida, a \rest{1 h}; a la vuelta, a \rest{5 h 15 min} ($t=5{,}25$)"])),
 (2, r"La gráfica muestra la temperatura de un día de invierno en una ciudad.\par\smallskip\begin{center}" + tg(temp, (0, 25, -2, 18), ux=0.3, uy=0.17, tx=2, ty=2, gx=1, gy=1, xl='h', yl='T\\ (^\\circ\\mathrm{C})') + r"\end{center}"
     + tasks(2, [r"¿Qué temperatura había a las 10 h?", r"¿A qué hora hizo más calor? ¿Y más frío?", r"¿Cuándo había 10 °C?", r"¿Cuánto subió la temperatura de 6 h a 14 h?"]),
     tasks(2, [r"$\res{8\ ^\circ\mathrm{C}}$", r"Más calor: \rest{14 h} (16 °C); más frío: \rest{6 h} (0 °C)", r"A las \rest{11 h} y a las \rest{20 h}", r"$16-0=\res{16\ ^\circ\mathrm{C}}$"])),
 (2, r"Asocia cada situación con su gráfica:" + tasks(1, [r"El precio de la fruta según los kilos que compramos.", r"La altura de una pelota que lanzamos hacia arriba.", r"La temperatura de un café caliente que se enfría.", r"El agua de una bañera que llenamos, dejamos llena un rato y después vaciamos."])
     + r'\par\smallskip\begin{center}' + r'\hfill'.join(r'\textbf{%s}\ %s' % (n_, g_) for n_, g_ in zip(['I', 'II', 'III', 'IV'], [gI, gII, gIII, gIV])) + r'\end{center}',
     tasks(4, [r"a) $\to$ \rest{III}", r"b) $\to$ \rest{I}", r"c) $\to$ \rest{IV}", r"d) $\to$ \rest{II}"])),
 (3, r"Haz una tabla de valores de $f(x)=\dfrac{12}{x}$ para $x=\pm1,\,\pm2,\,\pm3,\,\pm4,\,\pm6$ y represéntala. ¿Por qué no podemos unir el punto de $x=-1$ con el de $x=1$?",
     tvf('12/x', [-6, -4, -3, -2, -1, 1, 2, 3, 4, 6]) + r'\newline ' + tg(None, (-7, 7, -13, 13), ux=0.26, uy=0.13, tx=2, ty=4, fns=[('12/x', -7, -0.95), ('12/x', 0.95, 7)])
     + r'\newline El 0 \rest{no tiene imagen} (no se puede dividir entre 0): la gráfica tiene dos ramas separadas.'),
 (3, r"Inventa una historia que corresponda a esta gráfica de la distancia a casa de una persona.\par\smallskip\begin{center}" + tg(F(('c', [(0, 0), (1, 2), (3, 2), (3.5, 0), (4, 0), (5, 3)], 'c')), (0, 6, 0, 4), ux=0.8, uy=0.5, tx=1, ty=1, xl='t\\ (\\mathrm{h})', yl='d\\ (\\mathrm{km})') + r"\end{center}",
     r"Respuesta abierta. Por ejemplo: sale de casa y camina 2 km en 1 h hasta casa de una amiga, donde está 2 h; vuelve a casa en media hora (a 4 km/h), se queda media hora y después sale de nuevo y se aleja 3 km en 1 h."),
]))

# =====================================================================
# 4. Domini i recorregut
# =====================================================================
d1 = F(('c', [(-4, 3), (-1, -2), (2, 1), (4, 1)], 'c'))
d2 = F(('o', [(-3, -1), (1, 3)], 'c'), ('o', [(1, 0), (4, -2)], 'o'))
d3 = F(('a', [(-2, 2), (0, -1), (2, 2)], 'a'))
d4 = F(('c', [(-5, 1), (-2, 4)], 'c'), ('c', [(1, -2), (4, 0)], 'a'))
d5 = F(('c', [(-4, -3), (-1, 0)], 'o'), ('c', [(-1, 2), (3, 2)], 'o'), pts=[(5, -1)])
d6 = F(('a', [(-3, -1), (0, 2)], 'o'), ('o', [(0, -2), (3, 1)], 'a'))
assert S(st(d1)['dom']) == r'[-4,\,4]' and S(st(d1)['rec']) == r'[-2,\,3]'
assert S(st(d2)['dom']) == r'(-3,\,4)' and S(st(d2)['rec']) == r'(-2,\,3]'
assert S(st(d3)['dom']) == r'\mathbb{R}' and S(st(d3)['rec']) == r'[-1,\,+\infty)'
S_.append(("Dominio y recorrido", [
 (1, r"Escribe el dominio y el recorrido de estas funciones:" + tasks(3, [tg(d1, ux=0.27), tg(d2, ux=0.27), tg(d3, ux=0.27)])
     + recorda(r"Dominio: valores de $x$ que tienen imagen (proyección sobre el eje $X$). Recorrido: valores que toma la $y$ (proyección sobre el eje $Y$). Punto lleno: $[\ ]$; punto vacío: $(\ )$; flecha: $\pm\infty$."),
     tasks(1, [domrec(d1), domrec(d2), domrec(d3)])),
 (1, r"Calcula el dominio de:" + tasks(4, [r"$f(x)=3x^2-2x+1$", r"$g(x)=\dfrac{4}{x-1}$", r"$h(x)=\sqrt{x-2}$", r"$k(x)=\dfrac{x+3}{x+5}$"]),
     tasks(4, [r"$\res{\mathbb{R}}$", r"$\res{\mathbb{R}-\{1\}}$", r"$\res{[2,\,+\infty)}$", r"$\res{\mathbb{R}-\{-5\}}$"])),
 (2, r"Escribe el dominio y el recorrido de estas funciones:" + tasks(3, [tg(d4, ux=0.25), tg(d5, ux=0.27), tg(d6, ux=0.27)]),
     tasks(1, [domrec(d4), domrec(d5), domrec(d6)])),
 (2, r"Calcula el dominio de:" + tasks(4, [r"$f(x)=\dfrac{1}{x^2-4}$", r"$g(x)=\sqrt{6-2x}$", r"$h(x)=\dfrac{x}{x^2+1}$", r"$k(x)=\dfrac{5}{3x-9}$"]),
     tasks(4, [r"$x^2\neq4$: $\res{\mathbb{R}-\{-2,\,2\}}$", r"$6-2x\ge0$: $\res{(-\infty,\,3]}$", r"$x^2+1\neq0$ siempre: $\res{\mathbb{R}}$", r"$3x\neq9$: $\res{\mathbb{R}-\{3\}}$"])),
 (2, r"¿Qué dominio tienen estas funciones en su contexto?" + tasks(1, [r"El precio de $x$ bolígrafos a 0,80 € la unidad.", r"El área de un cuadrado de lado $x$: $A(x)=x^2$.", r"La altura de una pelota, $h(t)=20t-5t^2$, mientras está en el aire ($t$ en segundos)."]),
     tasks(1, [r"\rest{los números naturales} $0,\,1,\,2,\,3\ldots$", r"$x>0$: $\res{(0,\,+\infty)}$", r"$20t-5t^2=0\Rightarrow t=0$ o $t=4$: $\res{[0,\,4]}$"])),
 (3, r"Dibuja la gráfica de una función que tenga dominio $[-3,\,4]$ y recorrido $[-2,\,5]$.",
     r"Respuesta abierta. Por ejemplo, la poligonal que une $(-3,\,0)$, $(0,\,5)$, $(2,\,-2)$ y $(4,\,1)$ con los extremos llenos: \newline " + tg(F(('c', [(-3, 0), (0, 5), (2, -2), (4, 1)], 'c')), ux=0.25)),
 (3, r"Calcula el dominio de $f(x)=\dfrac{\sqrt{x+1}}{x-3}$.",
     r"Hace falta que $x+1\ge0$ ($x\ge-1$) y que $x\neq3$: $\res{\mathrm{Dom}\,f=[-1,\,3)\cup(3,\,+\infty)}$"),
]))
assert S(st(F(('c', [(-3, 0), (0, 5), (2, -2), (4, 1)], 'c')))['dom']) == r'[-3,\,4]' and S(st(F(('c', [(-3, 0), (0, 5), (2, -2), (4, 1)], 'c')))['rec']) == r'[-2,\,5]'
im('20x-5x^2', 4, 0)

# =====================================================================
# 5. Creixement i decreixement
# =====================================================================
m1 = F(('c', [(-5, -2), (-2, 3), (1, -1), (4, 2)], 'c'))
m2 = F(('c', [(-4, 4), (-1, 1), (2, 1), (4, -3)], 'c'))
m3 = F(('a', [(-1, -3), (1, 1), (3, -1)], 'a'))
m4 = F(('a', [(-3, 2), (-1, -2), (1, -2), (3, 2)], 'c'))
m5 = F(('c', [(-4, -1), (-1, 2)], 'o'), ('c', [(-1, -2), (2, 1), (5, -1)], 'c'))
assert S(st(m1)['mono']['+']) == r'(-5,\,-2)\cup (1,\,4)'
S_.append(("Crecimiento y decrecimiento", [
 (1, r"Indica los intervalos donde estas funciones son crecientes, decrecientes o constantes:" + tasks(3, [tg(m1, ux=0.27), tg(m2, ux=0.27), tg(m3, ux=0.27)])
     + recorda(r"Leemos la gráfica de izquierda a derecha. Los intervalos se dan con valores de la $x$ y son abiertos."),
     tasks(1, [monot(m1), monot(m2), monot(m3)])),
 (1, r"Sin dibujarlas, di si estas funciones son crecientes, decrecientes o constantes:" + tasks(4, [r"$y=4x-1$", r"$y=-3x+2$", r"$y=5$", r"$y=\tfrac{x}{2}$"]),
     tasks(4, [r"\rest{creciente}", r"\rest{decreciente}", r"\rest{constante}", r"\rest{creciente}"]) + r"Comparando dos imágenes: por ejemplo, $f(0)$ y $f(1)$."),
 (2, r"Estudia el crecimiento y el decrecimiento de estas funciones:" + tasks(2, [tg(m4, ux=0.3), tg(m5, ux=0.3)]),
     tasks(1, [monot(m4), monot(m5)])),
 (2, r"Con la gráfica de la temperatura del ejercicio \ref{ex:temp}, escribe los intervalos de tiempo en los que la temperatura sube y en los que baja.",
     monot(temp) + r'. La temperatura sube de 6 h a 14 h y baja el resto del día.'),
 (3, r"Pablo dice que la función del apartado a) del ejercicio \ref{ex:mono1} «crece en $(-2,\,3)$». ¿Qué error ha cometido?",
     r"Ha dado valores de la $y$ (de $-2$ a $3$) en lugar de los de la $x$. La función crece en $\res{(-5,\,-2)\cup(1,\,4)}$."),
 (3, r"Dibuja la gráfica de una función de dominio $\mathbb{R}$ que sea decreciente en $(-\infty,\,-1)$, constante en $(-1,\,2)$ y creciente en $(2,\,+\infty)$.",
     r"Respuesta abierta. Por ejemplo: \newline " + tg(F(('a', [(-3, 3), (-1, -1), (2, -1), (4, 3)], 'a')), ux=0.27)),
]))
assert S(st(F(('a', [(-3, 3), (-1, -1), (2, -1), (4, 3)], 'a')))['mono']['-']) == r'(-\infty,\,-1)' and S(st(F(('a', [(-3, 3), (-1, -1), (2, -1), (4, 3)], 'a')))['mono']['0']) == r'(-1,\,2)'

# =====================================================================
# 6. Màxims i mínims
# =====================================================================
e1 = F(('c', [(-5, 1), (-3, 4), (0, -2), (3, 3), (5, 0)], 'c'))
e2 = F(('a', [(-3, -1), (-1, 3), (2, -3)], 'a'))
e3 = F(('c', [(-4, -2), (-1, 3), (1, 1), (3, 3), (5, -1)], 'o'))
e4 = F(('o', [(-3, 4), (0, -1), (3, 4)], 'o'))
for a, v in [(0, 5), (1, 0), (2, -3), (3, -4), (4, -3), (5, 0), (6, 5)]: im('x^2-6x+5', a, v)
for a, v in [(0, 0), (2, 60), (4, 80), (6, 60), (8, 0)]: im('40x-5x^2', a, v)
assert st(e1)['max'] == [(-3, 4), (3, 3)] and st(e2)['amax'] == (3, [-1]) and st(e2)['amin'] is None
S_.append(("Máximos y mínimos", [
 (1, r"Halla los máximos y mínimos relativos de estas funciones:" + tasks(2, [tg(e1, ux=0.3), tg(e2, ux=0.3)])
     + recorda(r"Máximo relativo: la función pasa de creciente a decreciente. Mínimo relativo: pasa de decreciente a creciente. Se escriben como puntos $(x,\,y)$."),
     tasks(1, [extr(e1), extr(e2)])),
 (2, r"Halla los máximos y mínimos, relativos y absolutos, de estas funciones:" + tasks(2, [tg(e3, ux=0.3), tg(e4, ux=0.3)]),
     tasks(1, [extr(e3, True), extr(e4, True) + r'. No tiene máximo absoluto porque los extremos son vacíos.'])),
 (2, r"Haz una tabla de valores de $f(x)=x^2-6x+5$ para $x=0,\,1,\ldots,\,6$ y represéntala. ¿Dónde tiene el mínimo? ¿Cuáles son los puntos de corte con los ejes?",
     tvf('x^2-6x+5', [0, 1, 2, 3, 4, 5, 6]) + r'\qquad ' + tg(None, (-1, 7, -5, 6), ux=0.28, fns=[('x^2-6x+5', -0.3, 6.3)], dots=[(3, -4)])
     + r'\newline Mínimo: $\res{(3,\,-4)}$. Cortes: $(0,\,5)$, $(1,\,0)$ y $(5,\,0)$.'),
 (2, r"La altura en metros de un cohete de agua es $h(t)=40t-5t^2$, con $t$ en segundos. Haz una tabla para $t=0,\,2,\,4,\,6,\,8$. ¿Qué altura máxima alcanza y cuándo? ¿Cuándo vuelve al suelo?",
     tvf('40x-5x^2', [0, 2, 4, 6, 8], xl='t', yl='h') + r'\newline Máximo: $\res{(4,\,80)}$: a los 4 s llega a 80 m. Vuelve al suelo a los \rest{8 s}.'),
 (3, r"Dibuja una función de dominio $\mathbb{R}$ con un máximo relativo en $(-2,\,3)$ y un mínimo relativo en $(1,\,-1)$, que no tenga ni máximo ni mínimo absolutos.",
     r"Respuesta abierta. Por ejemplo: \newline " + tg(F(('a', [(-4, -1), (-2, 3), (1, -1), (3, 3)], 'a')), ux=0.27)),
 (3, r"Razona si son verdaderas o falsas:" + tasks(1, [r"Un máximo absoluto siempre es también un máximo relativo.", r"Si una función continua tiene dos máximos relativos, entre ellos tiene que haber al menos un mínimo relativo.", r"Si una función es creciente en todo el dominio, no tiene máximos ni mínimos relativos."]),
     tasks(1, [r"\rest{Falsa}: puede estar en un extremo del dominio, donde no hay máximo relativo. Por ejemplo, $y=x$ con dominio $[0,\,2]$ tiene el máximo absoluto en $(2,\,2)$.", r"\rest{Verdadera}: para ir de una cima a la otra sin levantar el lápiz, la gráfica tiene que bajar y volver a subir.", r"\rest{Verdadera}: nunca cambia de creciente a decreciente."])),
]))
fE5 = F(('a', [(-4, -1), (-2, 3), (1, -1), (3, 3)], 'a')); sE5 = st(fE5)
assert sE5['max'] == [(-2, 3)] and sE5['min'] == [(1, -1)] and sE5['amax'] is None and sE5['amin'] is None
assert st(e4)['min'] == [(0, -1)] and st(e4)['amax'] is None

# =====================================================================
# 7. Continuïtat
# =====================================================================
c1 = F(('c', [(-4, -2), (-1, 1), (2, -1), (4, 2)], 'c'))
c2 = F(('c', [(-4, 2), (0, 2)], 'o'), ('c', [(0, -1), (4, 3)], 'c'))
c3 = F(('c', [(-4, -1), (1, 4)], 'o'), ('o', [(1, 4), (4, 1)], 'c'), pts=[(1, 1)])
park = F(('o', [(0, 1.5), (1, 1.5)], 'c'), ('o', [(1, 3), (2, 3)], 'c'), ('o', [(2, 4.5), (3, 4.5)], 'c'), ('o', [(3, 6), (4, 6)], 'c'))
assert pl.value(park, Fr(5, 2)) == Fr(9, 2) and [d[0] for d in st(park)['disc']] == [1, 2, 3]
im('x+3', -2, 1); im('3-x^2', 0, 3); im('3-x^2', 2, -1); im('2x', 1, 2); im('x+3', 1, 4)
S_.append(("Continuidad", [
 (1, r"Di si estas funciones son continuas. Si no lo son, indica dónde son discontinuas y por qué:" + tasks(3, [tg(c1, ux=0.27), tg(c2, ux=0.27), tg(c3, ux=0.27)])
     + recorda(r"Una función es continua si se puede dibujar sin levantar el lápiz del papel."),
     tasks(1, [cont(c1), cont(c2), cont(c3)])),
 (1, r"Un aparcamiento cobra 1,50 € por cada hora o fracción, hasta un máximo de 4 horas. Representa la función precio y calcula cuánto se paga por 2 h 30 min. ¿Es continua?",
     tg(park, (0, 5, 0, 7), ux=0.8, uy=0.4, tx=1, ty=1, xl='t', yl='\\text{€}') + r'\newline 2 h 30 min es la 3.ª hora: $\res{4{,}50\text{ €}}$. \rest{Discontinua} en $t=1,\,2,\,3$ (saltos): es una función escalonada.'),
 (2, r"Dada $f(x)=\begin{cases}x+3 & \text{si } x<0\\ 3-x^2 & \text{si } x\ge0\end{cases}$, calcula $f(-2)$, $f(0)$ y $f(2)$. ¿Es continua en $x=0$?",
     r"$f(-2)=\res{1}$, $f(0)=\res{3}$, $f(2)=\res{-1}$. Por la izquierda, $x+3$ se acerca a $3$, y $f(0)=3$: \rest{es continua} en $x=0$."),
 (2, r"Dada $g(x)=\begin{cases}2x & \text{si } x\le1\\ x+3 & \text{si } x>1\end{cases}$, calcula $g(1)$ y di si es continua en $x=1$. Dibújala.",
     r"$g(1)=\res{2}$. Por la derecha, $x+3$ se acerca a $4$: da un \rest{salto} en $x=1$, \rest{no es continua}. \newline " + tg(F(('a', [(-1, -2), (1, 2)], 'c'), ('o', [(1, 4), (3, 6)], 'a')), (-3, 5, -4, 8), ux=0.25)),
 (2, r"Una empresa de mensajería cobra 3 € por paquetes de hasta 1 kg, 5 € por paquetes de más de 1 kg hasta 3 kg y 8 € por paquetes de más de 3 kg hasta 5 kg. Dibuja la gráfica, escribe el dominio y el recorrido e indica dónde es discontinua.",
     tg(F(('o', [(0, 3), (1, 3)], 'c'), ('o', [(1, 5), (3, 5)], 'c'), ('o', [(3, 8), (5, 8)], 'c')), (0, 6, 0, 9), ux=0.6, uy=0.35, tx=1, ty=1, xl='\\mathrm{kg}', yl='\\text{€}')
     + r'\newline ' + domrec(F(('o', [(0, 3), (1, 3)], 'c'), ('o', [(1, 5), (3, 5)], 'c'), ('o', [(3, 8), (5, 8)], 'c'))) + r'. Discontinua en $x=1$ y $x=3$ (saltos).'),
 (3, r"Halla el valor de $a$ para que la función $f(x)=\begin{cases}x^2+a & \text{si } x<2\\ 3x-1 & \text{si } x\ge2\end{cases}$ sea continua.",
     r"Los dos trozos tienen que valer lo mismo en $x=2$: $4+a=6-1\Rightarrow\res{a=1}$"),
 (3, r"¿Dónde son discontinuas estas funciones? ¿Por qué?" + tasks(2, [r"$f(x)=\dfrac{1}{x-2}$", r"$g(x)=\dfrac{3}{x^2-9}$"]),
     tasks(1, [r"En $\res{x=2}$: no es del dominio (ramas infinitas)", r"En $\res{x=-3}$ y $\res{x=3}$: anulan el denominador"])),
]))
assert [d for d in st(F(('a', [(-1, -2), (1, 2)], 'c'), ('o', [(1, 4), (3, 6)], 'a')))['disc']] == [(1, 'salt')]
assert 2 ** 2 + 1 == 3 * 2 - 1

# =====================================================================
# 8. Problemes amb funcions
# =====================================================================
im('3,5+1,1x', 12, Fr('16.7')); im('3,5+1,1x', 20, Fr('25.5'))
assert sp.solve(E('10+0,05x-0,15x'), x) == [100]
full = F(('c', [(-5, 0), (-3, 3), (0, -2)], 'c'), ('o', [(0, -4), (2, 1), (5, -1)], 'c'))
sF = st(full)
tank = F(('c', [(0, 20), (5, 120), (15, 120), (25, 0)], 'c')); sTk = st(tank)
assert S(sTk['mono']['+']) == r'(0,\,5)' and S(sTk['mono']['0']) == r'(5,\,15)' and S(sTk['mono']['-']) == r'(15,\,25)'
for a, v in [(1, 11), (3, 27), (6, 36), (9, 27), (11, 11)]: im('x(12-x)', a, v)
assert sp.solve(sp.diff(E('x(12-x)'), x), x) == [6]
for a, v in [(0, 0), (1, 25), (2, 40), (3, 45), (4, 40), (6, 0)]: im('30x-5x^2', a, v)
assert sp.solve(E('30+2x-5x'), x) == [10]
im('0,5x', 10, 5); im('5+0,8(x-10)', 15, 9)
assert sp.solve(E('5x-15(x-1)'), x) == [Fr(3, 2)]; im('5x', Fr(3, 2), Fr(15, 2))
PB = [
 (1, r"Un taxi cobra 3,50 € por la bajada de bandera y 1,10 € por kilómetro. Escribe la fórmula del precio, calcula cuánto cuesta un trayecto de 12 km y cuántos kilómetros hemos hecho si hemos pagado 25,50 €.",
     r"$f(x)=3{,}5+1{,}1x$. \ $f(12)=3{,}5+13{,}2=\res{16{,}70\text{ €}}$. \ $3{,}5+1{,}1x=25{,}5\Rightarrow 1{,}1x=22\Rightarrow\res{x=20\text{ km}}$"),
 (1, r"Una tarifa de móvil A cuesta 10 € al mes más 0,05 € por minuto, y una tarifa B cuesta 0,15 € por minuto. Escribe las dos fórmulas. ¿Cuál le conviene a quien habla 60 minutos al mes? ¿Y 150 minutos? ¿Para cuántos minutos cuestan lo mismo?",
     r"$A(x)=10+0{,}05x$, \ $B(x)=0{,}15x$. \ 60 min: $A=13$ €, $B=9$ €: \rest{B}. \ 150 min: $A=17{,}50$ €, $B=22{,}50$ €: \rest{A}. \ Iguals: $10+0{,}05x=0{,}15x\Rightarrow\res{x=100\text{ min}}$"),
 (2, r"Haz el estudio completo de esta función: dominio, recorrido, puntos de corte, crecimiento, máximos y mínimos y continuidad.\par\smallskip\begin{center}" + tg(full, ux=0.4) + r"\end{center}",
     domrec(full) + r'\newline Cortes: con el eje $Y$, $\res{(0,\,-2)}$; con el eje $X$, $\res{(-5,\,0)}$, $\res{(-1{,}2,\,0)}$, $\res{(1{,}6,\,0)}$ y $\res{(3{,}5,\,0)}$.'
     + r'\newline ' + monot(full) + r'\newline ' + extr(full, True) + r' (se acerca a $-4$, pero el punto $(0,\,-4)$ es vacío)\newline' + cont(full)),
 (2, r"Un depósito tiene 20 L de agua. Se llena durante 5 minutos hasta los 120 L, se mantiene así 10 minutos y después se vacía del todo en 10 minutos. Dibuja la gráfica volumen--tiempo y estúdiala. ¿A qué velocidad se llena y a cuál se vacía?",
     tg(tank, (0, 27, 0, 130), ux=0.25, uy=0.022, tx=5, ty=20, gx=5, gy=10, xl='t', yl='V') + r'\newline ' + domrec(tank) + r'\newline ' + monot(tank)
     + r'\newline Se llena a $100:5=\res{20\text{ L/min}}$ y se vacía a $120:10=\res{12\text{ L/min}}$. Máximo absoluto 120 L; mínimo absoluto 0 L (minuto 25).'),
 (2, r"Con 24 m de valla queremos hacer un corral rectangular. Escribe el área en función de la base $x$, haz una tabla para $x=1,\,3,\,6,\,9,\,11$ y di qué dimensiones dan el área máxima.",
     r"Base + altura $=12$: $A(x)=x(12-x)$, con dominio $(0,\,12)$." + r'\newline ' + tvf('x(12-x)', [1, 3, 6, 9, 11], yl='A') + r'\newline Máximo en $(6,\,36)$: un \rest{cuadrado de 6 m de lado} ($36\ \mathrm{m}^2$).'),
 (2, r"Lanzamos una pelota hacia arriba y su altura en metros es $h(t)=30t-5t^2$ ($t$ en segundos). Haz una tabla para $t=0,\,1,\,2,\,3,\,4,\,6$, represéntala y responde: ¿qué altura máxima alcanza? ¿Cuándo vuelve al suelo? ¿Qué dominio tiene sentido?",
     tvf('30x-5x^2', [0, 1, 2, 3, 4, 6], xl='t', yl='h') + r'\newline Máximo $\res{(3,\,45)}$: 45 m a los 3 s. Vuelve al suelo a los \rest{6 s}. Dominio: $\res{[0,\,6]}$.'),
 (3, r"El gimnasio A cobra 30 € de cuota mensual más 2 € por sesión; el gimnasio B no tiene cuota pero cobra 5 € por sesión. Escribe las dos funciones, represéntalas en los mismos ejes y di a partir de cuántas sesiones al mes conviene el gimnasio A.",
     r"$A(x)=30+2x$, \ $B(x)=5x$. Iguales si $30+2x=5x\Rightarrow x=10$. \ \rest{A partir de 11 sesiones} conviene A (con 10, cuestan igual: 50 €)." + r'\newline ' + tg(None, (0, 16, 0, 80), ux=0.3, uy=0.05, tx=2, ty=10, gx=1, gy=10, fns=[('30+2x', 0, 15), ('5x', 0, 15)], dots=[(10, 50)])),
 (3, r"La tarifa del agua de un pueblo es 0,50 €/m\textsuperscript{3} hasta 10 m\textsuperscript{3} y 0,80 €/m\textsuperscript{3} por cada m\textsuperscript{3} que pasa de 10. Escribe la función a trozos, calcula el precio de 15 m\textsuperscript{3} y di si es continua.",
     r"$f(x)=\begin{cases}0{,}5x & \text{si } 0\le x\le10\\ 5+0{,}8(x-10) & \text{si } x>10\end{cases}$ \quad $f(15)=5+4=\res{9\text{ €}}$. \ En $x=10$ los dos trozos valen 5: \rest{es continua}."),
 (3, r"Ana sale de casa caminando a 5 km/h. Una hora después, su hermano sale por el mismo camino en bicicleta a 15 km/h. Escribe la distancia a casa de cada uno en función del tiempo (desde que sale Ana) y halla cuándo y dónde la alcanza.",
     r"$d_A(t)=5t$, \ $d_G(t)=15(t-1)$ para $t\ge1$. \ $5t=15t-15\Rightarrow t=1{,}5$. La alcanza \rest{a la hora y media} de salir Ana, a $\res{7{,}5\text{ km}}$ de casa."),
]
assert [pl.value(full, t) for t in (-5, Fr(-6, 5), Fr(8, 5), Fr(7, 2))] == [0, 0, 0, 0] and pl.value(full, 0) == -2
assert st(full)['min'] == [] and st(full)['amin'] is None and st(full)['max'] == [(-3, 3), (2, 1)]
S_.append(("Problemas con funciones", [(st_, q + (recorda(r"Identifica las variables (qué es la $x$ y qué es la $y$, con las unidades), escribe la fórmula o dibuja la gráfica e interpreta cada resultado en el contexto del problema.") if i == 0 else ''), s) for i, (st_, q, s) in enumerate(PB)]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = 'pdfkeywords={funcions, imatge, antiimatge, taula de valors, gràfiques, domini, recorregut, creixement, màxims i mínims, continuïtat}'
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt').replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert r'\refstepcounter{exer}' in pre_
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
# referències creuades entre exercicis
REFS = {'ex:temp': ("Las funciones y sus gráficas", 4), 'ex:mono1': ("Crecimiento y decrecimiento", 0)}

pre = pre_

def build(sol_):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, ASSIGNATURA
    t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 7: Funciones' % t, capcalera='%s · Unidad 7: Funciones' % t,
                 pdfkeywords='funciones, imagen, antiimagen, tabla de valores, gráficas, dominio, recorrido, crecimiento, máximos y mínimos, continuidad')
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

''' + ASSIGNATURA + '{' + ('Soluciones de la ficha · Unidad 7' if sol_ else 'Ficha de ejercicios · Unidad 7') + '}{Funciones}\n')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás herramientas que calculan imágenes, hacen tablas de valores y estudian gráficas."
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
    name = 't7-fitxa-solucions-es.tex' if sol_ else 't7-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
