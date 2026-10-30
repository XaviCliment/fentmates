# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (3r ESO, Unitat 7: Funcions)
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
def pts(L): return ',\\ '.join(PT(P) for P in L) if L else r'\text{no en té}'
def absol(A): return (r'%s\ \text{(en }%s)' % (pl.num(A[0]), ',\\,'.join('x=' + pl.num(t) for t in A[1]))) if A else r'\text{no en té}'
def domrec(f): s = st(f); return r'$\mathrm{Dom}=\res{%s}$; \ $\mathrm{Rec}=\res{%s}$' % (S(s['dom']), S(s['rec']))
def monot(f):
    s = st(f)
    parts = [r'%s: $\res{%s}$' % (nm, S(s['mono'][k])) for k, nm in (('+', 'creix'), ('-', 'decreix'), ('0', 'constant')) if s['mono'][k]]
    return r'; \ '.join(parts)
def extr(f, absolut=False):
    s = st(f); out = r'màx.\ rel.: $\res{%s}$; \ mín.\ rel.: $\res{%s}$' % (pts(s['max']), pts(s['min']))
    if absolut: out += r'\newline màx.\ abs.: $\res{%s}$; \ mín.\ abs.: $\res{%s}$' % (absol(s['amax']), absol(s['amin']))
    return out
TIPUS = {'salt': 'salt', 'forat': 'falta un punt o està desplaçat', 'aillat': 'punt aïllat'}
def cont(f):
    s = st(f)
    if not s['disc']: return r'\rest{contínua}'
    return r'\rest{discontínua} en ' + ', '.join(r'$x=%s$ (%s)' % (pl.num(a), TIPUS[t]) for a, t in s['disc'])

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
S_.append(("Concepte de funció", [
 (1, r"Indica si cada relació és una funció:" + tasks(2, [r"A cada nombre natural, el seu quadrat.", r"A cada persona, els seus germans.", r"A cada quantitat de litres de gasolina, el preu que paguem.", r"A cada $x>0$, les seues arrels quadrades.", r"A cada alumne, la nota de l'últim examen.", r"A cada nota, els alumnes que l'han tret."])
     + recorda(r"Una relació és una funció si a \textbf{cada} valor de la variable independent ($x$) li correspon \textbf{un únic} valor de la variable dependent ($y$)."),
     tasks(2, [r"\rest{sí}", r"\rest{no}: pot tindre'n diversos (o cap)", r"\rest{sí}", r"\rest{no}: el 9 té el 3 i el $-3$", r"\rest{sí}", r"\rest{no}: n\'hi pot haver diversos"])),
 (1, r"En cada relació, quina és la variable independent i quina la dependent?" + tasks(1, [r"La durada d'una trucada i el que costa.", r"El nombre d'obrers i el temps que tarden a acabar una obra.", r"El costat d'un triangle equilàter i el seu perímetre."]),
     tasks(1, [r"Independent: \rest{la durada}; dependent: \rest{el cost}.", r"Independent: \rest{el nombre d'obrers}; dependent: \rest{el temps}.", r"Independent: \rest{el costat}; dependent: \rest{el perímetre} ($P=3x$)."])),
 (1, r"Quines d'aquestes gràfiques corresponen a una funció?\par\smallskip" + tasks(4, [tg(fA1, W5, ux=0.27), tg(None, W5, ux=0.27, curves=[circ]), tg(None, W5, ux=0.27, curves=[side]), tg(None, W5, ux=0.27, curves=[('poly', zig)])]),
     r"Fem la prova de la recta vertical: " + tasks(4, [r"\rest{sí}", r"\rest{no}", r"\rest{no}", r"\rest{no}"]) + r"En b), c) i d) hi ha rectes verticals que tallen la gràfica en dos o més punts."),
 (2, r"Les taules següents, defineixen una funció de $x$?" + tasks(2, [r"$\begin{array}{|c|c|c|c|c|}\hline x&1&2&2&3\\\hline y&4&5&6&7\\\hline\end{array}$", r"$\begin{array}{|c|c|c|c|c|}\hline x&1&2&3&4\\\hline y&5&5&5&6\\\hline\end{array}$"]),
     tasks(2, [r"\rest{no}: el 2 té dues imatges (5 i 6)", r"\rest{sí}: cada $x$ té una sola $y$ (que es repetisca la $y$ no importa)"])),
 (2, r"Explica per què la recta $y=3$ és la gràfica d'una funció i la recta $x=3$ no ho és.",
     r"En $y=3$, a cada $x$ li correspon una sola imatge, el 3: \rest{és funció} (constant). En $x=3$, al valor $x=3$ li corresponen infinits valors de $y$: \rest{no és funció} (la mateixa recta vertical la talla en infinits punts)."),
 (3, r"Dibuixa una gràfica que passe pels punts $(-2,\,1)$, $(0,\,3)$ i $(3,\,1)$ i que siga una funció, i una altra que passe pels mateixos punts i que \textbf{no} ho siga.",
     r"Resposta oberta. Per exemple, la poligonal que uneix els tres punts d'esquerra a dreta \rest{és funció}; una corba tancada (com una circumferència) que passe pels tres punts \rest{no ho és}."),
 (3, r"A cada nombre $x$ li fem correspondre el nombre $y$ que compleix $y^2=x$. És una funció? I si la condició és $y^3=x$?",
     r"$y^2=x$: per a $x=4$, $y=2$ o $y=-2$: \rest{no és funció}. $y^3=x$: cada nombre té una única arrel cúbica (per exemple, $y^3=8\Rightarrow y=2$; $y^3=-8\Rightarrow y=-2$): \rest{sí que és funció}."),
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
S_.append(("Expressió d'una funció", [
 (1, r"Donada la funció $f(x)=3x-5$, calcula:" + tasks(4, [r"$f(0)$", r"$f(2)$", r"$f(-3)$", r"$f\!\left(\tfrac12\right)$"])
     + recorda(r"Per a calcular la imatge $f(a)$, substituïm la $x$ per $a$ en la fórmula. Els nombres negatius, entre parèntesis."),
     tasks(4, [r"$\res{-5}$", r"$6-5=\res{1}$", r"$-9-5=\res{-14}$", r"$\tfrac32-5=\res{-\tfrac72}$"])),
 (1, r"Si $g(x)=x^2-4x+3$, calcula $g(0)$, $g(1)$, $g(-2)$ i $g(5)$.",
     r"$g(0)=\res{3}$; \ $g(1)=1-4+3=\res{0}$; \ $g(-2)=4+8+3=\res{15}$; \ $g(5)=25-20+3=\res{8}$"),
 (1, r"Completa les taules de valors:" + tasks(2, [r"$y=2x-1$\\[3pt]" + tvbuida([-2, -1, 0, 1, 2]), r"$y=-x^2+3$\\[3pt]" + tvbuida([-2, -1, 0, 1, 2])]),
     tasks(2, [tvf('2x-1', [-2, -1, 0, 1, 2]), tvf('-x^2+3', [-2, -1, 0, 1, 2])])),
 (2, r"Calcula les imatges que s'indiquen:" + tasks(2, [r"$h(x)=\dfrac{2x+1}{3}$: \ $h(4)$, $h(-2)$, $h(1)$", r"$k(x)=\sqrt{x+5}$: \ $k(4)$, $k(-1)$, $k(11)$"]),
     tasks(2, [r"$\tfrac93=\res{3}$; \ $\tfrac{-3}{3}=\res{-1}$; \ $\tfrac33=\res{1}$", r"$\sqrt9=\res{3}$; \ $\sqrt4=\res{2}$; \ $\sqrt{16}=\res{4}$"])),
 (2, r"Donada $f(x)=5x-3$, troba l'antiimatge de:" + tasks(3, [r"$12$", r"$-8$", r"$0$"])
     + recorda(r"Per a trobar l'antiimatge de $k$, resolem l'equació $f(x)=k$."),
     tasks(3, [r"$5x-3=12\Rightarrow\res{x=3}$", r"$5x-3=-8\Rightarrow\res{x=-1}$", r"$5x=3\Rightarrow\res{x=\tfrac35}$"])),
 (2, r"Donada $f(x)=x^2-1$, quins valors de $x$ tenen per imatge:" + tasks(3, [r"$8$", r"$-1$", r"$-5$"]),
     tasks(3, [r"$x^2=9\Rightarrow\res{x=\pm3}$", r"$x^2=0\Rightarrow\res{x=0}$", r"$x^2=-4$: \rest{cap}"])),
 (2, r"Escriu la fórmula de cada funció:" + tasks(1, [r"El perímetre d'un rectangle de base $x$ i altura 4 cm.", r"El preu de $x$ entrades de concert a 8,50 € cadascuna.", r"L'àrea d'un cercle de radi $x$.", r"El temps que es tarda a fer 300 km a una velocitat de $x$ km/h."]),
     tasks(1, [r"$\res{P(x)=2x+8}$", r"$\res{f(x)=8{,}5x}$", r"$\res{A(x)=\pi x^2}$", r"$\res{t(x)=\tfrac{300}{x}}$"])),
 (2, r"Troba la fórmula de les funcions que donen aquestes taules:" + tasks(2, [tvf('4x+3', [0, 1, 2, 3, 4]), tvf('x^2', [1, 2, 3, 4])]),
     tasks(1, [r"Augmenta 4 cada vegada i val 3 en $x=0$: $\res{y=4x+3}$", r"Cada $y$ és el quadrat de la $x$: $\res{y=x^2}$"])),
 (3, r"Una botiga de fotografia cobra 2 € per l'enviament més 0,15 € per cada foto revelada. Escriu la fórmula del preu en funció del nombre de fotos, calcula el preu de 40 fotos i quantes fotos podem revelar amb 11 €.",
     r"$f(x)=2+0{,}15x$. \ $f(40)=2+6=\res{8\text{ €}}$. \ $2+0{,}15x=11\Rightarrow 0{,}15x=9\Rightarrow\res{x=60}$ fotos."),
 (3, r"La funció $f(x)=ax+3$ compleix que $f(2)=11$. Troba $a$ i calcula $f(-1)$.",
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
S_.append(("Les funcions i els seus gràfics", [
 (1, r"Fes una taula de valors de $f(x)=2x-3$ per a $x=-1,\,0,\,1,\,2,\,3$, representa la funció i troba els punts de tall amb els eixos."
     + recorda(r"Tall amb l'eix $Y$: fem $x=0$. Tall amb l'eix $X$: resolem $f(x)=0$."),
     tvf('2x-3', [-1, 0, 1, 2, 3]) + r'\qquad ' + tg(None, (-3, 5, -6, 5), ux=0.28, fns=[('2x-3', -3, 5)], dots=[(0, -3), (1.5, 0)])
     + r'\newline Talls: $\res{(0,\,-3)}$ i $\res{\left(\tfrac32,\,0\right)}$'),
 (1, r"Fes una taula de valors de $g(x)=x^2-4$ per a $x$ entre $-3$ i $3$ i representa-la. On talla els eixos?",
     tvf('x^2-4', [-3, -2, -1, 0, 1, 2, 3]) + r'\qquad ' + tg(None, (-4, 4, -5, 6), ux=0.28, fns=[('x^2-4', -3.2, 3.2)], dots=[(0, -4), (-2, 0), (2, 0)])
     + r'\newline Talls: $\res{(0,\,-4)}$, $\res{(-2,\,0)}$ i $\res{(2,\,0)}$'),
 (2, r"Troba els punts de tall amb els eixos:" + tasks(2, [r"$f(x)=3x+6$", r"$g(x)=x^2-5x+6$", r"$h(x)=x^2+1$", r"$k(x)=x^3-4x$"]),
     tasks(2, [r"$\res{(0,\,6)}$, $\res{(-2,\,0)}$", r"$\res{(0,\,6)}$, $\res{(2,\,0)}$, $\res{(3,\,0)}$", r"$\res{(0,\,1)}$; amb l'eix $X$, \rest{cap} ($x^2=-1$)", r"$x(x^2-4)=0$: $\res{(0,\,0)}$, $\res{(2,\,0)}$, $\res{(-2,\,0)}$"])),
 (2, r"La gràfica mostra la distància a casa d'un ciclista durant una eixida.\par\smallskip\begin{center}" + tg(bici, (0, 7, 0, 45), ux=0.9, uy=0.07, tx=1, ty=10, gx=1, gy=5, xl='t\\ (\\mathrm{h})', yl='d\\ (\\mathrm{km})') + r"\end{center}"
     + tasks(1, [r"Quants quilòmetres recorre en total?", r"Quant de temps està parat?", r"A quina velocitat va en les dues primeres hores? I en la tornada?", r"A quina distància de casa està a les 5 h?", r"En quins moments està a 15 km de casa?"]),
     tasks(1, [r"$40+40=\res{80\text{ km}}$", r"De 2 a 3 h: \rest{1 hora}", r"$30:2=\res{15\text{ km/h}}$; tornada: $40:2=\res{20\text{ km/h}}$", r"$\res{20\text{ km}}$", r"A l'anada, a \rest{1 h}; a la tornada, a \rest{5 h 15 min} ($t=5{,}25$)"])),
 (2, r"La gràfica mostra la temperatura d'un dia d'hivern en una ciutat.\par\smallskip\begin{center}" + tg(temp, (0, 25, -2, 18), ux=0.3, uy=0.17, tx=2, ty=2, gx=1, gy=1, xl='h', yl='T\\ (^\\circ\\mathrm{C})') + r"\end{center}"
     + tasks(2, [r"Quina temperatura hi havia a les 10 h?", r"A quina hora va fer més calor? I més fred?", r"Quan hi havia 10 °C?", r"Quant va pujar la temperatura de 6 h a 14 h?"]),
     tasks(2, [r"$\res{8\ ^\circ\mathrm{C}}$", r"Més calor: \rest{14 h} (16 °C); més fred: \rest{6 h} (0 °C)", r"A les \rest{11 h} i a les \rest{20 h}", r"$16-0=\res{16\ ^\circ\mathrm{C}}$"])),
 (2, r"Associa cada situació amb la seua gràfica:" + tasks(1, [r"El preu de la fruita segons els quilos que en comprem.", r"L'altura d'una pilota que llancem cap amunt.", r"La temperatura d'un cafè calent que es refreda.", r"L'aigua d'una banyera que omplim, deixem plena una estona i després buidem."])
     + r'\par\smallskip\begin{center}' + r'\hfill'.join(r'\textbf{%s}\ %s' % (n_, g_) for n_, g_ in zip(['I', 'II', 'III', 'IV'], [gI, gII, gIII, gIV])) + r'\end{center}',
     tasks(4, [r"a) $\to$ \rest{III}", r"b) $\to$ \rest{I}", r"c) $\to$ \rest{IV}", r"d) $\to$ \rest{II}"])),
 (3, r"Fes una taula de valors de $f(x)=\dfrac{12}{x}$ per a $x=\pm1,\,\pm2,\,\pm3,\,\pm4,\,\pm6$ i representa-la. Per què no podem unir el punt de $x=-1$ amb el de $x=1$?",
     tvf('12/x', [-6, -4, -3, -2, -1, 1, 2, 3, 4, 6]) + r'\newline ' + tg(None, (-7, 7, -13, 13), ux=0.26, uy=0.13, tx=2, ty=4, fns=[('12/x', -7, -0.95), ('12/x', 0.95, 7)])
     + r'\newline El 0 \rest{no té imatge} (no es pot dividir entre 0): la gràfica té dues branques separades.'),
 (3, r"Inventa una història que corresponga a aquesta gràfica de la distància a casa d'una persona.\par\smallskip\begin{center}" + tg(F(('c', [(0, 0), (1, 2), (3, 2), (3.5, 0), (4, 0), (5, 3)], 'c')), (0, 6, 0, 4), ux=0.8, uy=0.5, tx=1, ty=1, xl='t\\ (\\mathrm{h})', yl='d\\ (\\mathrm{km})') + r"\end{center}",
     r"Resposta oberta. Per exemple: ix de casa i camina 2 km en 1 h fins a casa d'una amiga, on està 2 h; torna a casa en mitja hora (a 4 km/h), hi està mitja hora i després ix de nou i s'allunya 3 km en 1 h."),
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
S_.append(("Domini i recorregut", [
 (1, r"Escriu el domini i el recorregut d'aquestes funcions:" + tasks(3, [tg(d1, ux=0.27), tg(d2, ux=0.27), tg(d3, ux=0.27)])
     + recorda(r"Domini: valors de $x$ que tenen imatge (projecció sobre l'eix $X$). Recorregut: valors que pren la $y$ (projecció sobre l'eix $Y$). Punt ple: $[\ ]$; punt buit: $(\ )$; fletxa: $\pm\infty$."),
     tasks(1, [domrec(d1), domrec(d2), domrec(d3)])),
 (1, r"Calcula el domini de:" + tasks(4, [r"$f(x)=3x^2-2x+1$", r"$g(x)=\dfrac{4}{x-1}$", r"$h(x)=\sqrt{x-2}$", r"$k(x)=\dfrac{x+3}{x+5}$"]),
     tasks(4, [r"$\res{\mathbb{R}}$", r"$\res{\mathbb{R}-\{1\}}$", r"$\res{[2,\,+\infty)}$", r"$\res{\mathbb{R}-\{-5\}}$"])),
 (2, r"Escriu el domini i el recorregut d'aquestes funcions:" + tasks(3, [tg(d4, ux=0.25), tg(d5, ux=0.27), tg(d6, ux=0.27)]),
     tasks(1, [domrec(d4), domrec(d5), domrec(d6)])),
 (2, r"Calcula el domini de:" + tasks(4, [r"$f(x)=\dfrac{1}{x^2-4}$", r"$g(x)=\sqrt{6-2x}$", r"$h(x)=\dfrac{x}{x^2+1}$", r"$k(x)=\dfrac{5}{3x-9}$"]),
     tasks(4, [r"$x^2\neq4$: $\res{\mathbb{R}-\{-2,\,2\}}$", r"$6-2x\ge0$: $\res{(-\infty,\,3]}$", r"$x^2+1\neq0$ sempre: $\res{\mathbb{R}}$", r"$3x\neq9$: $\res{\mathbb{R}-\{3\}}$"])),
 (2, r"Quin domini tenen aquestes funcions en el seu context?" + tasks(1, [r"El preu de $x$ bolígrafs a 0,80 € la unitat.", r"L'àrea d'un quadrat de costat $x$: $A(x)=x^2$.", r"L'altura d'una pilota, $h(t)=20t-5t^2$, mentre està en l'aire ($t$ en segons)."]),
     tasks(1, [r"\rest{els nombres naturals} $0,\,1,\,2,\,3\ldots$", r"$x>0$: $\res{(0,\,+\infty)}$", r"$20t-5t^2=0\Rightarrow t=0$ o $t=4$: $\res{[0,\,4]}$"])),
 (3, r"Dibuixa la gràfica d'una funció que tinga domini $[-3,\,4]$ i recorregut $[-2,\,5]$.",
     r"Resposta oberta. Per exemple, la poligonal que uneix $(-3,\,0)$, $(0,\,5)$, $(2,\,-2)$ i $(4,\,1)$ amb els extrems plens: \newline " + tg(F(('c', [(-3, 0), (0, 5), (2, -2), (4, 1)], 'c')), ux=0.25)),
 (3, r"Calcula el domini de $f(x)=\dfrac{\sqrt{x+1}}{x-3}$.",
     r"Cal que $x+1\ge0$ ($x\ge-1$) i que $x\neq3$: $\res{\mathrm{Dom}\,f=[-1,\,3)\cup(3,\,+\infty)}$"),
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
S_.append(("Creixement i decreixement", [
 (1, r"Indica els intervals on aquestes funcions són creixents, decreixents o constants:" + tasks(3, [tg(m1, ux=0.27), tg(m2, ux=0.27), tg(m3, ux=0.27)])
     + recorda(r"Llegim la gràfica d'esquerra a dreta. Els intervals es donen amb valors de la $x$ i són oberts."),
     tasks(1, [monot(m1), monot(m2), monot(m3)])),
 (1, r"Sense dibuixar-les, digues si aquestes funcions són creixents, decreixents o constants:" + tasks(4, [r"$y=4x-1$", r"$y=-3x+2$", r"$y=5$", r"$y=\tfrac{x}{2}$"]),
     tasks(4, [r"\rest{creixent}", r"\rest{decreixent}", r"\rest{constant}", r"\rest{creixent}"]) + r"Comparant dues imatges: per exemple, $f(0)$ i $f(1)$."),
 (2, r"Estudia el creixement i el decreixement d'aquestes funcions:" + tasks(2, [tg(m4, ux=0.3), tg(m5, ux=0.3)]),
     tasks(1, [monot(m4), monot(m5)])),
 (2, r"Amb la gràfica de la temperatura de l'exercici \ref{ex:temp}, escriu els intervals de temps en què la temperatura puja i en què baixa.",
     monot(temp) + r'. La temperatura puja de 6 h a 14 h i baixa la resta del dia.'),
 (3, r"En Pau diu que la funció de l'apartat a) de l'exercici \ref{ex:mono1} «creix en $(-2,\,3)$». Quin error ha comés?",
     r"Ha donat valors de la $y$ (de $-2$ a $3$) en lloc dels de la $x$. La funció creix en $\res{(-5,\,-2)\cup(1,\,4)}$."),
 (3, r"Dibuixa la gràfica d'una funció de domini $\mathbb{R}$ que siga decreixent en $(-\infty,\,-1)$, constant en $(-1,\,2)$ i creixent en $(2,\,+\infty)$.",
     r"Resposta oberta. Per exemple: \newline " + tg(F(('a', [(-3, 3), (-1, -1), (2, -1), (4, 3)], 'a')), ux=0.27)),
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
S_.append(("Màxims i mínims", [
 (1, r"Troba els màxims i mínims relatius d'aquestes funcions:" + tasks(2, [tg(e1, ux=0.3), tg(e2, ux=0.3)])
     + recorda(r"Màxim relatiu: la funció passa de creixent a decreixent. Mínim relatiu: passa de decreixent a creixent. S'escriuen com a punts $(x,\,y)$."),
     tasks(1, [extr(e1), extr(e2)])),
 (2, r"Troba els màxims i mínims, relatius i absoluts, d'aquestes funcions:" + tasks(2, [tg(e3, ux=0.3), tg(e4, ux=0.3)]),
     tasks(1, [extr(e3, True), extr(e4, True) + r'. No té màxim absolut perquè els extrems són buits.'])),
 (2, r"Fes una taula de valors de $f(x)=x^2-6x+5$ per a $x=0,\,1,\ldots,\,6$ i representa-la. On té el mínim? Quins són els punts de tall amb els eixos?",
     tvf('x^2-6x+5', [0, 1, 2, 3, 4, 5, 6]) + r'\qquad ' + tg(None, (-1, 7, -5, 6), ux=0.28, fns=[('x^2-6x+5', -0.3, 6.3)], dots=[(3, -4)])
     + r'\newline Mínim: $\res{(3,\,-4)}$. Talls: $(0,\,5)$, $(1,\,0)$ i $(5,\,0)$.'),
 (2, r"L'altura en metres d'un coet d'aigua és $h(t)=40t-5t^2$, amb $t$ en segons. Fes una taula per a $t=0,\,2,\,4,\,6,\,8$. Quina altura màxima assoleix i quan? Quan torna a terra?",
     tvf('40x-5x^2', [0, 2, 4, 6, 8], xl='t', yl='h') + r'\newline Màxim: $\res{(4,\,80)}$: als 4 s arriba a 80 m. Torna a terra als \rest{8 s}.'),
 (3, r"Dibuixa una funció de domini $\mathbb{R}$ amb un màxim relatiu en $(-2,\,3)$ i un mínim relatiu en $(1,\,-1)$, que no tinga ni màxim ni mínim absoluts.",
     r"Resposta oberta. Per exemple: \newline " + tg(F(('a', [(-4, -1), (-2, 3), (1, -1), (3, 3)], 'a')), ux=0.27)),
 (3, r"Raona si són vertaderes o falses:" + tasks(1, [r"Un màxim absolut sempre és també un màxim relatiu.", r"Si una funció contínua té dos màxims relatius, entre ells hi ha d'haver almenys un mínim relatiu.", r"Si una funció és creixent en tot el domini, no té màxims ni mínims relatius."]),
     tasks(1, [r"\rest{Falsa}: pot estar en un extrem del domini, on no hi ha màxim relatiu. Per exemple, $y=x$ amb domini $[0,\,2]$ té el màxim absolut en $(2,\,2)$.", r"\rest{Vertadera}: per a anar d'un cim a l'altre sense alçar el llapis, la gràfica ha de baixar i tornar a pujar.", r"\rest{Vertadera}: mai no canvia de creixent a decreixent."])),
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
S_.append(("Continuïtat", [
 (1, r"Digues si aquestes funcions són contínues. Si no ho són, indica on són discontínues i per què:" + tasks(3, [tg(c1, ux=0.27), tg(c2, ux=0.27), tg(c3, ux=0.27)])
     + recorda(r"Una funció és contínua si es pot dibuixar sense alçar el llapis del paper."),
     tasks(1, [cont(c1), cont(c2), cont(c3)])),
 (1, r"Un aparcament cobra 1,50 € per cada hora o fracció, fins a un màxim de 4 hores. Representa la funció preu i calcula quant es paga per 2 h 30 min. És contínua?",
     tg(park, (0, 5, 0, 7), ux=0.8, uy=0.4, tx=1, ty=1, xl='t', yl='\\text{€}') + r'\newline 2 h 30 min és la 3a hora: $\res{4{,}50\text{ €}}$. \rest{Discontínua} en $t=1,\,2,\,3$ (salts): és una funció esglaonada.'),
 (2, r"Donada $f(x)=\begin{cases}x+3 & \text{si } x<0\\ 3-x^2 & \text{si } x\ge0\end{cases}$, calcula $f(-2)$, $f(0)$ i $f(2)$. És contínua en $x=0$?",
     r"$f(-2)=\res{1}$, $f(0)=\res{3}$, $f(2)=\res{-1}$. Per l'esquerra, $x+3$ s'acosta a $3$, i $f(0)=3$: \rest{és contínua} en $x=0$."),
 (2, r"Donada $g(x)=\begin{cases}2x & \text{si } x\le1\\ x+3 & \text{si } x>1\end{cases}$, calcula $g(1)$ i digues si és contínua en $x=1$. Dibuixa-la.",
     r"$g(1)=\res{2}$. Per la dreta, $x+3$ s'acosta a $4$: fa un \rest{salt} en $x=1$, \rest{no és contínua}. \newline " + tg(F(('a', [(-1, -2), (1, 2)], 'c'), ('o', [(1, 4), (3, 6)], 'a')), (-3, 5, -4, 8), ux=0.25)),
 (2, r"Una empresa de missatgeria cobra 3 € per paquets de fins a 1 kg, 5 € per paquets de més d'1 kg fins a 3 kg i 8 € per paquets de més de 3 kg fins a 5 kg. Dibuixa la gràfica, escriu el domini i el recorregut i indica on és discontínua.",
     tg(F(('o', [(0, 3), (1, 3)], 'c'), ('o', [(1, 5), (3, 5)], 'c'), ('o', [(3, 8), (5, 8)], 'c')), (0, 6, 0, 9), ux=0.6, uy=0.35, tx=1, ty=1, xl='\\mathrm{kg}', yl='\\text{€}')
     + r'\newline ' + domrec(F(('o', [(0, 3), (1, 3)], 'c'), ('o', [(1, 5), (3, 5)], 'c'), ('o', [(3, 8), (5, 8)], 'c'))) + r'. Discontínua en $x=1$ i $x=3$ (salts).'),
 (3, r"Troba el valor de $a$ perquè la funció $f(x)=\begin{cases}x^2+a & \text{si } x<2\\ 3x-1 & \text{si } x\ge2\end{cases}$ siga contínua.",
     r"Els dos trossos han de valdre el mateix en $x=2$: $4+a=6-1\Rightarrow\res{a=1}$"),
 (3, r"On són discontínues aquestes funcions? Per què?" + tasks(2, [r"$f(x)=\dfrac{1}{x-2}$", r"$g(x)=\dfrac{3}{x^2-9}$"]),
     tasks(1, [r"En $\res{x=2}$: no és del domini (branques infinites)", r"En $\res{x=-3}$ i $\res{x=3}$: anul·len el denominador"])),
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
 (1, r"Un taxi cobra 3,50 € per la baixada de bandera i 1,10 € per quilòmetre. Escriu la fórmula del preu, calcula quant costa un trajecte de 12 km i quants quilòmetres hem fet si hem pagat 25,50 €.",
     r"$f(x)=3{,}5+1{,}1x$. \ $f(12)=3{,}5+13{,}2=\res{16{,}70\text{ €}}$. \ $3{,}5+1{,}1x=25{,}5\Rightarrow 1{,}1x=22\Rightarrow\res{x=20\text{ km}}$"),
 (1, r"Una tarifa de mòbil A costa 10 € al mes més 0,05 € per minut, i una tarifa B costa 0,15 € per minut. Escriu les dues fórmules. Quina convé a qui parla 60 minuts al mes? I 150 minuts? Per a quants minuts costen el mateix?",
     r"$A(x)=10+0{,}05x$, \ $B(x)=0{,}15x$. \ 60 min: $A=13$ €, $B=9$ €: \rest{B}. \ 150 min: $A=17{,}50$ €, $B=22{,}50$ €: \rest{A}. \ Iguals: $10+0{,}05x=0{,}15x\Rightarrow\res{x=100\text{ min}}$"),
 (2, r"Fes l'estudi complet d'aquesta funció: domini, recorregut, punts de tall, creixement, màxims i mínims i continuïtat.\par\smallskip\begin{center}" + tg(full, ux=0.4) + r"\end{center}",
     domrec(full) + r'\newline Talls: amb l\'eix $Y$, $\res{(0,\,-2)}$; amb l\'eix $X$, $\res{(-5,\,0)}$, $\res{(-1{,}2,\,0)}$, $\res{(1{,}6,\,0)}$ i $\res{(3{,}5,\,0)}$.'
     + r'\newline ' + monot(full) + r'\newline ' + extr(full, True) + r' (s\'acosta a $-4$, però el punt $(0,\,-4)$ és buit)\newline ' + cont(full)),
 (2, r"Un dipòsit té 20 L d'aigua. S'omple durant 5 minuts fins als 120 L, es manté així 10 minuts i després es buida del tot en 10 minuts. Dibuixa la gràfica volum--temps i estudia-la. A quina velocitat s'omple i a quina es buida?",
     tg(tank, (0, 27, 0, 130), ux=0.25, uy=0.022, tx=5, ty=20, gx=5, gy=10, xl='t', yl='V') + r'\newline ' + domrec(tank) + r'\newline ' + monot(tank)
     + r'\newline S\'omple a $100:5=\res{20\text{ L/min}}$ i es buida a $120:10=\res{12\text{ L/min}}$. Màxim absolut 120 L; mínim absolut 0 L (minut 25).'),
 (2, r"Amb 24 m de tanca volem fer un corral rectangular. Escriu l'àrea en funció de la base $x$, fes una taula per a $x=1,\,3,\,6,\,9,\,11$ i digues quines dimensions donen l'àrea màxima.",
     r"Base + altura $=12$: $A(x)=x(12-x)$, amb domini $(0,\,12)$." + r'\newline ' + tvf('x(12-x)', [1, 3, 6, 9, 11], yl='A') + r'\newline Màxim en $(6,\,36)$: un \rest{quadrat de 6 m de costat} ($36\ \mathrm{m}^2$).'),
 (2, r"Llancem una pilota cap amunt i la seua altura en metres és $h(t)=30t-5t^2$ ($t$ en segons). Fes una taula per a $t=0,\,1,\,2,\,3,\,4,\,6$, representa-la i respon: quina altura màxima assoleix? Quan torna a terra? Quin domini té sentit?",
     tvf('30x-5x^2', [0, 1, 2, 3, 4, 6], xl='t', yl='h') + r'\newline Màxim $\res{(3,\,45)}$: 45 m als 3 s. Torna a terra als \rest{6 s}. Domini: $\res{[0,\,6]}$.'),
 (3, r"El gimnàs A cobra 30 € de quota mensual més 2 € per sessió; el gimnàs B no té quota però cobra 5 € per sessió. Escriu les dues funcions, representa-les en els mateixos eixos i digues a partir de quantes sessions al mes convé el gimnàs A.",
     r"$A(x)=30+2x$, \ $B(x)=5x$. Iguals si $30+2x=5x\Rightarrow x=10$. \ \rest{A partir d'11 sessions} convé A (amb 10, costen igual: 50 €)." + r'\newline ' + tg(None, (0, 16, 0, 80), ux=0.3, uy=0.05, tx=2, ty=10, gx=1, gy=10, fns=[('30+2x', 0, 15), ('5x', 0, 15)], dots=[(10, 50)])),
 (3, r"La tarifa de l'aigua d'un poble és 0,50 €/m\textsuperscript{3} fins a 10 m\textsuperscript{3} i 0,80 €/m\textsuperscript{3} per cada m\textsuperscript{3} que passa de 10. Escriu la funció a trossos, calcula el preu de 15 m\textsuperscript{3} i digues si és contínua.",
     r"$f(x)=\begin{cases}0{,}5x & \text{si } 0\le x\le10\\ 5+0{,}8(x-10) & \text{si } x>10\end{cases}$ \quad $f(15)=5+4=\res{9\text{ €}}$. \ En $x=10$ els dos trossos valen 5: \rest{és contínua}."),
 (3, r"L'Anna ix de casa caminant a 5 km/h. Una hora després, el seu germà ix pel mateix camí amb bicicleta a 15 km/h. Escriu la distància a casa de cadascun en funció del temps (des que ix l'Anna) i troba quan i on l'atrapa.",
     r"$d_A(t)=5t$, \ $d_G(t)=15(t-1)$ per a $t\ge1$. \ $5t=15t-15\Rightarrow t=1{,}5$. L'atrapa \rest{a l'hora i mitja} d'eixir l'Anna, a $\res{7{,}5\text{ km}}$ de casa."),
]
assert [pl.value(full, t) for t in (-5, Fr(-6, 5), Fr(8, 5), Fr(7, 2))] == [0, 0, 0, 0] and pl.value(full, 0) == -2
assert st(full)['min'] == [] and st(full)['amin'] is None and st(full)['max'] == [(-3, 3), (2, 1)]
S_.append(("Problemes amb funcions", [(st_, q + (recorda(r"Identifica les variables (què és la $x$ i què és la $y$, amb les unitats), escriu la fórmula o dibuixa la gràfica i interpreta cada resultat en el context del problema.") if i == 0 else ''), s) for i, (st_, q, s) in enumerate(PB)]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = 'pdfkeywords={funcions, imatge, antiimatge, taula de valors, gràfiques, domini, recorregut, creixement, màxims i mínims, continuïtat}'
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt').replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert r'\refstepcounter{exer}' in pre_
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
# referències creuades entre exercicis
REFS = {'ex:temp': ("Les funcions i els seus gràfics", 4), 'ex:mono1': ("Creixement i decreixement", 0)}

def build(sol_):
    t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
    p = pre_.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                     "pdftitle={%s de la unitat 7: Funcions. 3r d'ESO}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 7: Funcions · 3r d'ESO" % t)
    assert 'Unitat 7' in p and 'unitat 7' in p
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{3r ESO}{''' + ('Solucions de la fitxa · Unitat 7' if sol_ else "Fitxa d'exercicis · Unitat 7") + r'''}{Funcions}
''')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs eines que calculen imatges, fan taules de valors i estudien gràfiques."
             if sol_ else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Per a dibuixar gràfiques, fes servir paper quadriculat i tria una escala adequada per a cada eix.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            n += 1
            lab = ''.join(r'\label{%s}' % k for k, (tt, jj) in REFS.items() if tt == title and jj == j)
            out.append('\\ex{%d}%s %s\n\n' % (st_, lab, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't7-fitxa-solucions.tex' if sol_ else 't7-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
