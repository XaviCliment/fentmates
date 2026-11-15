# Versió en castellà de genera.py: escriu els -es.tex. Original: genera t6-fitxa-exercicis.tex i t6-fitxa-solucions.tex (1r Batxillerat MI, Unitat 6: Estudi de funcions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# La fitxa segueix els apartats dels apunts (6.1-6.9). Els exercicis de funcions elementals són a la fitxa de la unitat 7
# (_eines/fonts-latex/1batx-mi-t7) i els estudis complets aniran en una unitat posterior.
# Comprovacions: sympy calcula els talls, els vèrtexs, les composicions i les inverses; els dominis es comproven numèricament
# (la funció ha d'existir exactament en els punts del domini donat, en una malla fina i al voltant de cada extrem).
# Les gràfiques es dibuixen amb la classe Plot de _eines/apunts/1batx-mi-t6/fig.py (la mateixa dels apunts).
# Ús: python3 genera.py && pdflatex t6-fitxa-exercicis.tex (dues vegades) && pdflatex t6-fitxa-solucions.tex (dues vegades)
import os, re, sys, math
from sympy import symbols, sympify, solve, simplify, expand, Rational, sqrt as Ssqrt, S, log as Slog, Abs, Poly, nsimplify
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "apunts", "1batx-mi-t6"))
from fig import Plot, piece, sq, lg, PI

x = symbols("x", real=True)
xp = symbols("x", positive=True)
_sympify = sympify
def sympify(s, locals=None):  # les expressions escrites com a text fan servir la x real
    return _sympify(s, locals=locals or {'x': x})

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def G(p, w=3.7): return '\\begin{center}' + p.tikz(w) + '\\end{center}'
def Gi(p, w=3.05): return p.tikz(w)

CHK = []
def ck(cond, msg=''):
    assert cond, msg
    CHK.append(True)

def defined(f, t):
    try:
        v = f(t)
    except OverflowError:  # existeix, però és massa gran per a un float
        return True
    except (ValueError, ZeroDivisionError):
        return False
    return v is not None and isinstance(v, (int, float)) and math.isfinite(v)
def ckdom(f, inD, edges=(), msg=''):
    """f està definida exactament on inD(t) és cert (malla fina i extrems ± 1e-6)"""
    pts = [i / 97 for i in range(-1500, 1501)] + [e + d for e in edges for d in (-1e-6, 0, 1e-6)]
    for t in pts:
        assert defined(f, t) == bool(inD(t)), (msg, t, defined(f, t), inD(t))
    CHK.append(True)
def cr(t): return math.copysign(abs(t) ** (1 / 3), t)
def nz(d):  # divisió que falla si el denominador és 0
    if abs(d) < 1e-12: raise ZeroDivisionError
    return d
def ckroots(expr, sols, dom=S.Reals, msg=''):
    got = sorted(solve(sympify(expr), x), key=lambda v: float(v))
    want = sorted([sympify(s) for s in sols], key=lambda v: float(v))
    assert len(got) == len(want) and all(simplify(a - b) == 0 for a, b in zip(got, want)), (msg, got, want)
    CHK.append(True)
def ckeq(a, b, sym=x, msg=''):
    d = simplify(sympify(a) - sympify(b)) if isinstance(a, str) or isinstance(b, str) else simplify(a - b)
    assert d == 0, (msg, a, b, d)
    CHK.append(True)
def cknum(a, b, tol=1e-9, msg=''):
    assert abs(a - b) <= tol * max(1, abs(b)), (msg, a, b)
    CHK.append(True)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Concepte de funció
p1 = [Plot(-4, 4, -3, 4, W=200).fn(lambda t: t * t - 2),
      Plot(-4, 4, -4, 4, W=200).param(lambda t: 3 * math.cos(t), lambda t: 3 * math.sin(t), 0, 2 * PI),
      Plot(-4, 4, -1, 4, W=200).fn(abs),
      Plot(-3, 5, -3, 3, W=200).param(lambda t: t * t - 2, lambda t: t, -2.7, 2.7)]
ff = lambda t: t * t - 3 * t + 1
cknum(ff(-2), 11); cknum(ff(0), 1); cknum(ff(.5), -.25)
a = symbols('a'); ckeq(expand(((a + 1) ** 2 - 3 * (a + 1) + 1)), a ** 2 - a - 1)
ckroots('x**2-3*x+1-1', [0, 3])
S_.append(("Concepto de función", [
 (1, r"¿Cuáles de estas gráficas corresponden a una función? Justifícalo con la prueba de la recta vertical." + tasks(4, [Gi(p) for p in p1]),
     tasks(2, [R('\\text{Sí}'), R('\\text{No}') + ' (circunferencia)', R('\\text{Sí}'), R('\\text{No}')]) + r'Las gráficas b) y d) tienen valores de $x$ con dos imágenes: hay rectas verticales que las cortan dos veces.'),
 (1, r"Indica si estas relaciones son funciones:" + tasks(1, [
     "A cada número real le hacemos corresponder su cuadrado.",
     "A cada número positivo le hacemos corresponder sus raíces cuadradas.",
     "A cada persona le hacemos corresponder el número de su DNI.",
     "A cada alumno de la clase le hacemos corresponder sus hermanos."]),
     tasks(1, [R('\\text{Sí}'), R('\\text{No}') + r': el 4 tiene dos raíces, $2$ y $-2$.', R('\\text{Sí}'), R('\\text{No}') + ': un alumno puede tener dos o más hermanos.'])),
 (1, r"Dada $f(x)=x^2-3x+1$, calcula $f(-2)$, $f(0)$, $f\left(\frac12\right)$ y $f(a+1)$. ¿Para qué valores de $x$ vale $f(x)=1$?",
     r'$f(-2)=\res{11}$, $f(0)=\res{1}$, $f\left(\frac12\right)=\res{-\frac14}$, $f(a+1)=\res{a^2-a-1}$. \ $x^2-3x=0\Rightarrow\res{x=0,\ x=3}$'),
 (2, r"Con 40 m de tela metálica queremos cerrar un corral rectangular. Si un lado mide $x$ metros, escribe la función $A(x)$ que da el área del corral. ¿Qué valores puede tomar $x$ (dominio en este contexto)? Calcula $A(5)$ y $A(10)$.",
     r'El otro lado mide $20-x$: $\res{A(x)=x(20-x)=20x-x^2}$. Debe ser $0\lt x\lt20$: $D=\res{\oo{0}{20}}$. $A(5)=\res{75\text{ m}^2}$, $A(10)=\res{100\text{ m}^2}$.'),
]))
Acorral = lambda t: t * (20 - t)
ck(Acorral(5) == 75 and Acorral(10) == 100)

# =====================================================================
# 2. Domini i recorregut
d1 = [piece(Plot(-2, 4, -3, 3, W=200), [(lambda t: (t - 1) ** 2 - 2, -1, 3, True, True)]),
      Plot(-5, 3, -3, 6, W=200, lx=2, ly=2).fn(lambda t: 2 + 1 / (t + 1) if t != -1 else None).vl(-1).hl(2),
      Plot(-3, 6, -2, 3, W=200).fn(lambda t: sq(t + 2) - 1 if t >= -2 else None, -2, 6).dot(-2, -1),
      Plot(-5, 3, -2, 4, W=200).fn(lambda t: t + 3, -4, -1).dot(-4, -1).dot(-1, 2, open=True).seg(-1, 3, 2, 3).dot(-1, 3).dot(2, 3)]
e5 = [
 ('2x^3-5x+1', lambda t: 2 * t ** 3 - 5 * t + 1, lambda t: True, (), r'\R'),
 (r'\dfrac{3x}{x-5}', lambda t: 3 * t / nz(t - 5), lambda t: t != 5, (5,), r'\R-\{5\}'),
 (r'\dfrac{x+2}{x^2-9}', lambda t: (t + 2) / nz(t * t - 9), lambda t: abs(t) != 3, (-3, 3), r'\R-\{-3,\,3\}'),
 (r'\dfrac{x-1}{x^2+4}', lambda t: (t - 1) / (t * t + 4), lambda t: True, (), r'\R'),
 (r'\dfrac{2}{x^3-4x}', lambda t: 2 / nz(t ** 3 - 4 * t), lambda t: t not in (-2, 0, 2), (-2, 0, 2), r'\R-\{-2,\,0,\,2\}'),
 (r'\sqrt{2x-6}', lambda t: math.sqrt(2 * t - 6), lambda t: t >= 3, (3,), r'\co{3}{+\infty}'),
 (r'\sqrt{9-x^2}', lambda t: math.sqrt(9 - t * t), lambda t: -3 <= t <= 3, (-3, 3), r'\cc{-3}{3}'),
 (r'\sqrt{x^2-4x+3}', lambda t: math.sqrt(t * t - 4 * t + 3), lambda t: t <= 1 or t >= 3, (1, 3), r'\oc{-\infty}{1}\cup\co{3}{+\infty}'),
 (r'\sqrt[3]{x^2-1}', lambda t: cr(t * t - 1), lambda t: True, (), r'\R'),
 (r'\dfrac{1}{\sqrt{x-2}}', lambda t: 1 / nz(math.sqrt(t - 2)), lambda t: t > 2, (2,), r'\oo{2}{+\infty}'),
 (r'\log(3-x)', lambda t: math.log10(3 - t), lambda t: t < 3, (3,), r'\oo{-\infty}{3}'),
 (r'\ln(x^2-x-6)', lambda t: math.log(t * t - t - 6), lambda t: t < -2 or t > 3, (-2, 3), r'\oo{-\infty}{-2}\cup\oo{3}{+\infty}'),
 (r'2^{\frac{x+1}{x-3}}', lambda t: 2 ** ((t + 1) / nz(t - 3)), lambda t: t != 3, (3,), r'\R-\{3\}'),
 (r'\sqrt{\dfrac{x+3}{x-1}}', lambda t: math.sqrt((t + 3) / nz(t - 1)), lambda t: t <= -3 or t > 1, (-3, 1), r'\oc{-\infty}{-3}\cup\oo{1}{+\infty}'),
 (r'\dfrac{\log_2x}{x-4}', lambda t: math.log2(t) / nz(t - 4), lambda t: t > 0 and t != 4, (0, 4), r'\oo{0}{4}\cup\oo{4}{+\infty}'),
]
for tx, f, inD, ed, _ in e5: ckdom(f, inD, ed, tx)
S_.append(("Dominio y recorrido", [
 (1, r"Escribe el dominio y el recorrido de las funciones representadas:" + tasks(4, [Gi(p) for p in d1]),
     tasks(2, [r'$D=\res{\cc{-1}{3}}$, $R=\res{\cc{-2}{2}}$', r'$D=\res{\R-\{-1\}}$, $R=\res{\R-\{2\}}$', r'$D=\res{\co{-2}{+\infty}}$, $R=\res{\co{-1}{+\infty}}$', r'$D=\res{\cc{-4}{2}}$, $R=\res{\co{-1}{2}\cup\{3\}}$'])),
 (1, r"Calcula el dominio de estas funciones:" + tasks(3, ['$f(x)=%s$' % e[0] for e in e5])
     + recorda(r"denominador $\neq0$; radicando de índice par $\geq0$; argumento del logaritmo $\gt0$; el exponente y el radicando de índice impar deben existir."),
     tasks(3, [R(e[4]) for e in e5])),
 (1, r"¿Pertenecen $x=2$ y $x=3$ al dominio de $f(x)=\sqrt{x^2-5}$? Justifícalo sustituyendo y después calcula el dominio completo.",
     r'$f(2)=\sqrt{-1}$ no existe: $\res{2\notin D(f)}$. $f(3)=\sqrt4=2$: $\res{3\in D(f)}$. $D(f)=\res{\oc{-\infty}{-\sqrt5}\cup\co{\sqrt5}{+\infty}}$'),
 (2, r"Razonando qué valores puede tomar $y$, calcula el recorrido de:" + tasks(4, [r'$f(x)=x^2+2$', r'$g(x)=\sqrt{x-1}+3$', r'$h(x)=\dfrac2x$', r'$k(x)=5-x^2$']),
     tasks(2, [r'$x^2\geq0\Rightarrow R=\res{\co{2}{+\infty}}$', r'$\sqrt{x-1}\geq0\Rightarrow R=\res{\co{3}{+\infty}}$', r'$\frac2x$ no vale nunca 0: $R=\res{\R-\{0\}}$', r'$-x^2\le0\Rightarrow R=\res{\oc{-\infty}{5}}$'])),
]))
for t in [i / 7 for i in range(-200, 201)]:
    ck(t * t + 2 >= 2 and 5 - t * t <= 5 and (t == 0 or 2 / t != 0))
ckdom(lambda t: math.sqrt(t * t - 5), lambda t: abs(t) >= math.sqrt(5), (-math.sqrt(5), math.sqrt(5)))

# =====================================================================
# 3. Punts de tall
c3 = [('x^2-5x+4', 'x**2-5*x+4', [1, 4]), ('x^3-9x', 'x**3-9*x', [-3, 0, 3]), (r'\dfrac{x+4}{x-2}', '(x+4)/(x-2)', [-4]),
      (r'\sqrt{x+9}-2', 'sqrt(x+9)-2', [-5]), ('3^x-9', '3**x-9', [2]), (r'\log_2(x+3)', 'log(x+3,2)', [-2]),
      ('x^2+2x+5', 'x**2+2*x+5', []), ('x^4-5x^2+4', 'x**4-5*x**2+4', [-2, -1, 1, 2])]
oy = []
for _, e, rr in c3:
    ckroots(e, rr, msg=e)
    oy.append(sympify(e).subs(x, 0))
ck(oy == [4, 0, -2, 1, -8, Slog(3) / Slog(2), 5, 4])
def tall(rr, y0):
    s = r'$OY$: $\res{(0,\,%s)}$; ' % y0
    return s + (r'$OX$: ' + ', '.join(r'$\res{(%d,\,0)}$' % v for v in rr) if rr else r'$OX$: no tiene')
s3 = [tall(rr, y) for (_, _, rr), y in zip(c3, ['4', '0', '-2', '1', '-8', r'\log_23\approx1{,}58', '5', '4'])]
S_.append(("Puntos de corte con los ejes", [
 (1, r"Halla los puntos de corte con los ejes de coordenadas:" + tasks(4, ['$f(x)=%s$' % c[0] for c in c3])
     + recorda(r"corte con $OY$: hacemos $x=0$; cortes con $OX$: resolvemos $f(x)=0$."), tasks(2, s3)),
 (2, r"Halla el valor de $a$ para que la función $f(x)=x^2+ax-6$ corte al eje $OX$ en $x=2$. ¿Dónde lo corta la otra vez? ¿Y dónde corta al eje $OY$?",
     r'$f(2)=4+2a-6=0\Rightarrow\res{a=1}$. $x^2+x-6=0\Rightarrow$ el otro corte es $\res{(-3,\,0)}$. $OY$: $\res{(0,\,-6)}$.'),
]))
ckroots('x**2+x-6', [-3, 2])

# =====================================================================
# 4. Monotonia, màxims i mínims
P4 = [(-5, -2), (-3, 3), (-1, 1), (1, 4), (3, -3), (6, 2)]
g4 = Plot(-6, 7, -4, 5, W=300)
for (a_, b_), (c_, d_) in zip(P4, P4[1:]): g4.seg(a_, b_, c_, d_)
for q in P4: g4.dot(*q)
sol8 = lambda t: (t - 1) ** 2 / 2 - 2
cknum(sol8(-1), 0); cknum(sol8(3), 0); cknum(sol8(1), -2)
S_.append(("Monotonía. Máximos y mínimos", [
 (1, r"Observa la gráfica e indica su dominio, su recorrido, los intervalos de crecimiento y de decrecimiento, y los máximos y mínimos (relativos y absolutos)." + G(g4, 6),
     r'$D=\res{\cc{-5}{6}}$, $R=\res{\cc{-3}{4}}$. Creciente en $\res{\oo{-5}{-3}\cup\oo{-1}{1}\cup\oo{3}{6}}$; decreciente en $\res{\oo{-3}{-1}\cup\oo{1}{3}}$. Máximos: $\res{(-3,3)}$ relativo y $\res{(1,4)}$ absoluto. Mínimos: $\res{(-1,1)}$ relativo y $\res{(3,-3)}$ absoluto.'),
 (2, r"Dibuja la gráfica de una función con dominio $\R$, decreciente en $\oo{-\infty}{1}$, creciente en $\oo{1}{+\infty}$, con mínimo absoluto en $(1,-2)$ y que corte al eje $OX$ en $x=-1$ y en $x=3$. ¿Puedes encontrar una expresión?",
     r'Por ejemplo, la parábola $\res{f(x)=\frac12(x-1)^2-2}$:' + G(Plot(-3, 5, -3, 4, W=220).fn(sol8).dot(1, -2, 'b').dot(-1, 0, 'b').dot(3, 0, 'b'))),
 (1, r"La gráfica es la de $f(x)=x^3-3x$. Indica sus intervalos de crecimiento y de decrecimiento y sus extremos relativos. ¿Tiene máximo o mínimo absoluto?" + G(Plot(-3, 3, -4, 4, W=230).fn(lambda t: t ** 3 - 3 * t).dot(-1, 2).dot(1, -2), 4),
     r'Creciente en $\res{\oo{-\infty}{-1}\cup\oo{1}{+\infty}}$; decreciente en $\res{\oo{-1}{1}}$. Máximo relativo $\res{(-1,2)}$ y mínimo relativo $\res{(1,-2)}$. No tiene extremos absolutos: por la derecha sube hasta $+\infty$ y por la izquierda baja hasta $-\infty$.'),
]))
fc = lambda t: t ** 3 - 3 * t
ck(fc(-1) == 2 and fc(1) == -2); ckroots('3*x**2-3', [-1, 1])

# =====================================================================
# 5. Continuïtat
g5 = Plot(-6, 6, -2, 5, W=320)
g5.fn(lambda t: t / 2 + 3, -6, 0).dot(-3, 1.5, open=True).dot(-3, 3.5).dot(0, 3, open=True)
g5.fn(lambda t: 1 - t / 2, 0, 2).dot(0, 1).dot(2, 0, open=True).fn(lambda t: 1 / (t - 2), 2.02, 6).vl(2)
# exercici 15: una altra gràfica amb tres discontinuïtats de tipus diferents
g15 = Plot(-6, 7, -2, 7, W=320)
g15.fn(lambda t: t + 5, -6, -3).dot(-6, -1).dot(-3, 2, open=True).dot(-3, 4)
g15.fn(lambda t: 2 - (t + 3) / 2, -3, 1).dot(1, 0)
g15.fn(lambda t: 2 / (t - 1), 1.05, 3).dot(3, 1, open=True).vl(1)
g15.fn(lambda t: t - 1, 3, 7).dot(3, 2)
ck(-3 + 5 == 2 - 0 / 2 and 2 - (1 + 3) / 2 == 0 and 2 / (3 - 1) == 1 and 3 - 1 == 2)
# exercici 16: quatre gràfiques, totes estudiades en x = 2
def c16():
    return Plot(-1, 5, -2, 5, W=170)
g16 = [c16().fn(lambda t: 3 + (t - 2) / 2 - (t - 2) ** 2 / 4).dot(2, 3, open=True),
       c16().fn(lambda t: (t - 2) / 2 + 1, -1, 2).dot(2, 1).fn(lambda t: 3 + (t - 2) ** 2 / 3, 2, 5).dot(2, 3, open=True),
       c16().fn(lambda t: abs(t - 2) + 1).dot(2, 1),
       c16().fn(lambda t: 1 / (t - 2) + 1 if abs(t - 2) > 1e-9 else None).vl(2)]
s16 = [r'Discontinuidad $\res{\text{evitable}}$: los dos lados llegan a 3, pero $f(2)$ no existe. Sería continua si $\res{f(2)=3}$.',
       r'Discontinuidad de $\res{\text{salto finito}}$: por la izquierda llega a 1 (y $f(2)=1$) y por la derecha a 3; el salto es de 2 unidades.',
       r'$\res{\text{Continua}}$: los dos lados llegan a 1 y $f(2)=1$. Tiene un pico, pero se dibuja sin levantar el lápiz.',
       r'Discontinuidad $\res{\text{asintótica}}$: por la izquierda tiende a $-\infty$ y por la derecha a $+\infty$ (asíntota vertical $x=2$).']
S_.append(("Continuidad", [
 (1, r"Indica en qué puntos es discontinua esta función y clasifica cada discontinuidad." + G(g5, 6.2),
     r'$x=-3$: $\res{\text{evitable}}$ (el punto está fuera de su sitio). $x=0$: $\res{\text{salto finito}}$ (de 3 a 1). $x=2$: $\res{\text{salto infinito}}$ (por la izquierda llega a 0 y por la derecha tiende a $+\infty$).'),
 (1, r"Indica en qué puntos es discontinua esta función y clasifica cada discontinuidad. ¿En qué intervalos es continua?" + G(g15, 6.2),
     r'$x=-3$: $\res{\text{evitable}}$ (los dos lados llegan a 2, pero $f(-3)=4$: el punto está fuera de su sitio). $x=1$: $\res{\text{salto infinito}}$ (por la izquierda llega a 0 y por la derecha tiende a $+\infty$). $x=3$: $\res{\text{salto finito}}$ (por la izquierda llega a 1 y $f(3)=2$). Es continua en $\res{\co{-6}{-3}\cup\oo{-3}{1}\cup\oo{1}{3}\cup\cc{3}{7}}$, es decir, en cada trozo entre estos puntos.'),
 (2, r"Estudia la continuidad de cada función en $x=2$. Si es discontinua, clasifica la discontinuidad y, si es evitable, indica qué valor debería tener $f(2)$ para que fuera continua." + tasks(4, [Gi(p, 3.05) for p in g16]),
     tasks(1, s16)),
]))

# =====================================================================
# 6. Simetries i periodicitat
p6 = [('x^4-2x^2+3', 'x**4-2*x**2+3', 'parella'), ('x^3+5x', 'x**3+5*x', 'senar'), ('x^3+1', 'x**3+1', 'cap'), (r'\dfrac{2x}{x^2+1}', '2*x/(x**2+1)', 'senar'),
      (r'\dfrac{x^2-1}{x^4+2}', '(x**2-1)/(x**4+2)', 'parella'), ('|x|-x^2', 'Abs(x)-x**2', 'parella'), (r'x\,|x|', 'x*Abs(x)', 'senar'), (r'\sqrt{x^2+1}', 'sqrt(x**2+1)', 'parella')]
for _, e, k in p6:
    f = sympify(e, locals={'x': x}); fm = f.subs(x, -x)
    ev, od = simplify(fm - f) == 0, simplify(fm + f) == 0
    ck((k == 'parella') == ev and (k == 'senar') == od, e)
half = [(0, 0), (1, 2), (3, -1), (4, 0)]
def halfplot(sym):
    p = Plot(-5, 5, -3, 3, W=210)
    for (a_, b_), (c_, d_) in zip(half, half[1:]):
        p.seg(a_, b_, c_, d_)
        if sym: p.seg(-a_, sym * b_, -c_, sym * d_, 'b')
    return p
S_.append(("Simetrías y periodicidad", [
 (1, r"Estudia si estas funciones son pares, impares o ninguna de las dos:" + tasks(4, ['$f(x)=%s$' % c[0] for c in p6]) + recorda(r"par: $f(-x)=f(x)$; impar: $f(-x)=-f(x)$."),
     tasks(4, [R('\\text{' + {'parella': 'Par', 'senar': 'Impar', 'cap': 'Ninguna'}[c[2]] + '}') for c in p6])),
 (2, r"La gráfica siguiente es la parte de una función $f$ correspondiente a $x\in[0,4]$. Complétala en $[-4,0]$ si $f$ es par y, en otra gráfica, si $f$ es impar." + G(halfplot(0), 4.2),
     tasks(2, ['Par (simetría respecto de $OY$):' + G(halfplot(1), 3.6), 'Impar (simetría respecto del origen):' + G(halfplot(-1), 3.6)])),
 (2, r"Una función $f$ es periódica de período 3, y $f(1)=2$ y $f(2)=-1$. Calcula $f(7)$, $f(-4)$ y $f(11)$.",
     r'$f(7)=f(1+2\cdot3)=\res{2}$; \ $f(-4)=f(-4+6)=f(2)=\res{-1}$; \ $f(11)=f(2+3\cdot3)=\res{-1}$'),
]))

# =====================================================================
# 7. Transformacions de funcions (translacions)
FP = [(-3, 0), (-1, 2), (1, 1), (2, 3)]
def fpol(t):
    for (a_, b_), (c_, d_) in zip(FP, FP[1:]):
        if a_ <= t <= c_: return b_ + (d_ - b_) * (t - a_) / (c_ - a_)
    return None
def trp(h, k, base=True):
    p = Plot(-6, 6, -4, 6, W=200, lx=2, ly=2)
    if base: p.fn(fpol, -3, 2, 'm', dash=True)
    if (h, k) != (0, 0) or not base:
        for (a_, b_), (c_, d_) in zip(FP, FP[1:]): p.seg(a_ + h, b_ + k, c_ + h, d_ + k)
        for a_, b_ in FP: p.dot(a_ + h, b_ + k)
    return p
T2 = [('f(x)-2', 0, -2), ('f(x+3)', -3, 0), ('f(x-1)+4', 1, 4)]
s72 = []
for tx, h, k in T2:  # D=[-2,4], R=[-1,3], màxim (1,3)
    s72.append(r'$%s$: $D=\res{\cc{%d}{%d}}$, $R=\res{\cc{%d}{%d}}$, máximo $\res{(%d,%d)}$' % (tx, -2 + h, 4 + h, -1 + k, 3 + k, 1 + h, 3 + k))
ck(s72[0].count('-4') == 0 and '(1,1)' in s72[0] and '(-2,3)' in s72[1] and '(2,7)' in s72[2])
q73 = [('x^2-6x+11', '(x-3)**2+2', '(x-3)^2+2', '(3,\\,2)'), ('x^2+4x', '(x+2)**2-4', '(x+2)^2-4', '(-2,\\,-4)'), ('x^2+2x+5', '(x+1)**2+4', '(x+1)^2+4', '(-1,\\,4)')]
for a_, b_ in [('x**2-6*x+11', '(x-3)**2+2'), ('x**2+4*x', '(x+2)**2-4'), ('x**2+2*x+5', '(x+1)**2+4')]: ckeq(sympify(a_), expand(sympify(b_)))
S_.append(("Transformaciones de funciones", [
 (1, r"A partir de la gráfica de $f$, dibuja las gráficas de $f(x)+2$, $f(x-3)$ y $f(x+1)-2$." + G(trp(0, 0), 3.6),
     tasks(3, [r'$f(x)+2$: 2 arriba' + G(trp(0, 2), 3.2), r'$f(x-3)$: 3 a la derecha' + G(trp(3, 0), 3.2), r'$f(x+1)-2$: 1 a la izquierda y 2 abajo' + G(trp(-1, -2), 3.2)])),
 (1, r"Una función $f$ tiene dominio $[-2,4]$, recorrido $[-1,3]$ y un máximo en $(1,3)$. Indica el dominio, el recorrido y el máximo de:" + tasks(3, ['$y=%s$' % t[0] for t in T2]),
     tasks(1, s72)),
 (1, r"Escribe cada parábola como una traslación de $y=x^2$ (completando el cuadrado), explica el desplazamiento y da su vértice:" + tasks(3, ['$y=%s$' % q[0] for q in q73]),
     tasks(1, [r'$y=\res{%s}$: vértice $\res{%s}$' % (q[2], q[3]) for q in q73]) + r'Por ejemplo, $(x-3)^2+2$ es $x^2$ desplazada 3 a la derecha y 2 arriba.'),
 (2, r"Escribe la expresión de la función que se obtiene al desplazar:" + tasks(1, [r"$y=|x|$ 3 unidades hacia la derecha y 1 hacia arriba;", r"$y=\sqrt x$ 5 unidades hacia la izquierda y 2 hacia abajo;", r"$y=\dfrac1x$ 4 unidades hacia la derecha y 1 hacia arriba. ¿Cuáles son las asíntotas de la nueva función?"]),
     tasks(1, [R(r'y=|x-3|+1'), R(r'y=\sqrt{x+5}-2'), R(r'y=\dfrac{1}{x-4}+1') + r'; asíntotas $\res{x=4}$ y $\res{y=1}$'])),
 (2, r"La gráfica es una traslación de $y=|x|$. Escribe su expresión." + G(Plot(-7, 3, -4, 4, W=220).fn(lambda t: abs(t + 2) - 3).dot(-2, -3, 'b'), 3.8),
     r'El vértice pasa de $(0,0)$ a $(-2,-3)$: $\res{y=|x+2|-3}$'),
]))
ck(abs(-2 + 2) - 3 == -3)

# =====================================================================
# 8. Composició i inversa
f14, g14, h14 = sympify('x**2+1'), sympify('2*x-3'), sympify('1/(x+1)')
ckeq(expand(f14.subs(x, g14)), sympify('4*x**2-12*x+10')); ckeq(expand(g14.subs(x, f14)), sympify('2*x**2-1'))
ckeq(h14.subs(x, g14), sympify('1/(2*x-2)')); ckeq(g14.subs(x, h14), sympify('(-3*x-1)/(x+1)')); ckeq(expand(f14.subs(x, f14)), sympify('x**4+2*x**2+2'))
ck(f14.subs(x, g14).subs(x, 2) == 2)
inv = [('5x-2', '5*x-2', '(x+2)/5', r'\dfrac{x+2}{5}'), (r'\dfrac{3x+1}{2}', '(3*x+1)/2', '(2*x-1)/3', r'\dfrac{2x-1}{3}'),
       ('x^3-4', 'x**3-4', None, r'\sqrt[3]{x+4}'), (r'\dfrac{x+2}{x-1}', '(x+2)/(x-1)', '(x+2)/(x-1)', r'\dfrac{x+2}{x-1}'),
       ('2^{x+1}', '2**(x+1)', 'log(x,2)-1', r'\log_2x-1'), (r'\log_3(x-2)', 'log(x-2,3)', '3**x+2', r'3^x+2'),
       (r'\sqrt{x-1}', 'sqrt(x-1)', 'x**2+1', r'x^2+1\ \ (x\geq0)')]
for _, fs, gs, _ in inv:
    if gs is None: continue
    F_ = sympify(fs, locals={'x': xp}); G_ = sympify(gs, locals={'x': xp})
    ck(simplify(F_.subs(xp, G_) - xp) == 0 and simplify(G_.subs(xp, F_) - xp) == 0, fs)
for t in (-3.0, 0.5, 2.0, 7.0): cknum(cr(t ** 3 - 4 + 4), t)
S_.append(("Composición de funciones y función inversa", [
 (1, r"Con $f(x)=x^2+1$, $g(x)=2x-3$ y $h(x)=\dfrac{1}{x+1}$, calcula:" + tasks(3, [r'$(f\circ g)(x)$', r'$(g\circ f)(x)$', r'$(h\circ g)(x)$', r'$(g\circ h)(x)$', r'$(f\circ f)(x)$', r'$(f\circ g)(2)$']),
     tasks(3, [R('4x^2-12x+10'), R('2x^2-1'), R(r'\frac{1}{2x-2}'), R(r'\frac{-3x-1}{x+1}'), R('x^4+2x^2+2'), R('2')])),
 (2, r"Escribe cada función como composición de dos funciones más sencillas, $F=f\circ g$:" + tasks(4, [r'$F(x)=\sqrt{3x+1}$', r'$F(x)=(x-5)^4$', r'$F(x)=2^{x^2}$', r'$F(x)=\dfrac{1}{x^2+3}$']),
     tasks(2, [r'$g(x)=3x+1$, $f(x)=\sqrt x$', r'$g(x)=x-5$, $f(x)=x^4$', r'$g(x)=x^2$, $f(x)=2^x$', r'$g(x)=x^2+3$, $f(x)=\frac1x$'])),
 (1, r"Calcula la inversa de cada función y comprueba que $(f\circ f^{-1})(x)=x$:" + tasks(4, ['$f(x)=%s$' % i[0] for i in inv])
     + r'En g) considera solo $x\geq1$.' + recorda(r"cambia $f(x)$ por $y$, intercambia $x$ e $y$ y despeja $y$."),
     tasks(2, [r'$f^{-1}(x)=\res{%s}$' % i[3] for i in inv]) + r'Fíjate en que la función d) es su propia inversa.'),
 (2, r"Dibuja en unos mismos ejes $f(x)=2^x$, la recta $y=x$ y la inversa de $f$. ¿Qué función es?",
     r'$f^{-1}(x)=\res{\log_2x}$, simétrica de $2^x$ respecto de $y=x$.' + G(Plot(-3, 6, -3, 6, W=210).seg(-3, -3, 6, 6, 'm', True).fn(lambda t: 2 ** t).fn(lambda t: lg(2, t), .01, 6, 'g'), 3.6)),
 (2, r"Con $f(x)=\sqrt x$ y $g(x)=x-4$, calcula $(f\circ g)(x)$ y $(g\circ f)(x)$ y el dominio de cada una. Calcula $(f\circ g)(13)$ y $(g\circ f)(9)$.",
     r'$(f\circ g)(x)=\res{\sqrt{x-4}}$, $D=\res{\co{4}{+\infty}}$. \ $(g\circ f)(x)=\res{\sqrt x-4}$, $D=\res{\co{0}{+\infty}}$. \ $(f\circ g)(13)=\res{3}$, $(g\circ f)(9)=\res{-1}$.'),
 (2, r"De una función $f$ que tiene inversa sabemos que $f(1)=3$, $f(2)=5$ y $f(4)=-1$. Calcula $f^{-1}(5)$, $f^{-1}(-1)$ y $(f^{-1}\circ f)(2)$. ¿Qué puntos de la gráfica de $f^{-1}$ conoces?",
     r'$f^{-1}(5)=\res{2}$, $f^{-1}(-1)=\res{4}$, $(f^{-1}\circ f)(2)=\res{2}$. La gráfica de $f^{-1}$ pasa por $\res{(3,1),\ (5,2),\ (-1,4)}$ (se intercambian las coordenadas).'),
]))
ck(math.sqrt(13 - 4) == 3 and math.sqrt(9) - 4 == -1)
ckdom(lambda t: math.sqrt(t - 4), lambda t: t >= 4, (4,))

assert all(CHK)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "funciones, dominio, recorrido, puntos de corte, monotonía, máximos y mínimos, continuidad, simetría, periodicidad, traslaciones, composición, función inversa"
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'''\usetikzlibrary{calc}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\providecommand{\gt}{>}\providecommand{\lt}{<}
% intervals a la manera dels apunts: ]a,b[, [a,b], ...
\newcommand{\R}{\mathbb{R}}
\newcommand{\oo}[2]{\left]#1,\,#2\right[}
\newcommand{\oc}[2]{\left]#1,\,#2\right]}
\newcommand{\co}[2]{\left[#1,\,#2\right[}
\newcommand{\cc}[2]{\left[#1,\,#2\right]}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

def fix(t):
    """Fora dels dibuixos: l'apòstrof escrit \\' dins de cadenes r'' (en LaTeX seria un accent) i l'espai després
    de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = "Estudio de funciones"
def build(sol):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 6: %s' % (t, TIT), capcalera='%s · Unidad 6: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-mi')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1batx-mi') + '{' + ('Soluciones de la ficha · Unidad 6' if sol else 'Ficha de ejercicios · Unidad 6') + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los intervalos se escriben como en los apuntes: $\left]a,b\right[$ abierto y $[a,b]$ cerrado. Puedes comprobar dominios, cortes, traslaciones, composiciones e inversas con las herramientas de los apuntes interactivos de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos y haz un dibujo siempre que te ayude. Escribe los intervalos como en los apuntes ($\left]a,b\right[$ abierto, $[a,b]$ cerrado). Las secciones siguen el orden de los apuntes de la unidad.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't6-fitxa-solucions-es.tex' if sol else 't6-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'ejercicios;', len(CHK), 'comprobaciones')
