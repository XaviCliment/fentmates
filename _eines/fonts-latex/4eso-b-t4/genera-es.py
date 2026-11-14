# Versió en castellà de genera.py. Genera t4-fitxa-exercicis-es.tex i t4-fitxa-solucions-es.tex (4t ESO Matemàtiques B, Unitat 4: Sistemes d'equacions i inequacions)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py i les figures
# del pla (rectes, semiplans i regions) a ../comu/regions.py. Cada solució escrita a mà es comprova ací: sistemes lineals i no
# lineals amb sympy (ls, nls, kind), sistemes d'inequacions amb una incògnita (ineqs) i vèrtexs de les regions (vx).
# Ús: python3 genera-es.py && pdflatex t4-fitxa-exercicis-es.tex (dues vegades) && pdflatex t4-fitxa-solucions-es.tex (dues vegades)
import os, sys, re
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *
from regions import fig, verts, C

x, y = sp.symbols('x y', real=True)
LOC = {'x': x, 'y': y}
def E(s): return sp.sympify(s, locals=LOC)
def eqs(*s): return [sp.Eq(E(a.split('=')[0]), E(a.split('=')[1])) for a in s]
def ls(system, sol):
    """sistema lineal amb solució única"""
    got = sp.solve(eqs(*system), [x, y], dict=True)
    assert len(got) == 1 and got[0][x] == E(sol[0]) and got[0][y] == E(sol[1]), (system, got)
def kind(system, k):
    A, b = sp.linear_eq_to_matrix([e.lhs - e.rhs for e in eqs(*system)], [x, y])
    r, ra = A.rank(), A.row_join(b).rank()
    got = 'SCD' if r == ra == 2 else 'SCI' if r == ra else 'SI'
    assert got == k, (system, got)
def nls(system, sols):
    got = sp.solve(eqs(*system), [x, y], dict=True)
    got = {(sp.nsimplify(g[x]), sp.nsimplify(g[y])) for g in got if g[x].is_real and g[y].is_real}
    exp = {(E(a), E(b)) for a, b in sols}
    assert got == exp, (system, got, exp)
def toset(s):
    if s == 'R': return sp.S.Reals
    if s == '0': return sp.S.EmptySet
    out = sp.S.EmptySet
    for p in s.split('U'):
        m = re.match(r'^([\[\(])([^,]+),([^,]+)([\]\)])$', p.strip())
        a = -sp.oo if m.group(2) == '-inf' else sp.Rational(m.group(2)); b = sp.oo if m.group(3) == 'inf' else sp.Rational(m.group(3))
        out = out.union(sp.Interval(a, b, m.group(1) == '(', m.group(4) == ')'))
    return out
def ineqs(system, expected):
    xr = sp.symbols('x', real=True); S = sp.S.Reals
    for e in system: S = S.intersect(sp.solve_univariate_inequality(sp.sympify(e, locals={'x': xr}), xr, relational=False))
    assert S == toset(expected), (system, S, expected)
def vx(cons, expected, bounded=True):
    V, b = verts(cons)
    assert sorted(V) == sorted((F(a), F(c)) for a, c in expected) and b == bounded, (V, b)
def sis(*rows):
    """sistema; si hi ha fraccions, separa més les files"""
    sep = r'\\[9pt] ' if any('frac' in r for r in rows) else r'\\[2pt] '
    return r'\begin{cases}' + sep.join(rows) + r'\end{cases}'
_tasks = tasks
def tasks(n, items, start=None, gap=None):
    """apartats amb sistemes: més espai entre files (més encara si hi ha fraccions)"""
    if gap is None and any('cases' in i for i in items): gap = '16pt' if any('frac' in i for i in items) else '9pt'
    return _tasks(n, items, start, gap)
def XY(a, b): return R('x=%s,\\ y=%s' % (a, b))
PRE = r'\usetikzlibrary{calc}' + '\n'

S = []

# =====================================================================
# 1. Sistemes lineals. Classificació i mètode gràfic
ls(['3*x+2*y=4', 'x-y=3'], ['2', '-1'])
G = [(['x+y=5', 'x-y=1'], ('3', '2'), [C(1, 1, '=', 5), C(1, -1, '=', 1)]), (['2*x-y=1', 'x+y=5'], ('2', '3'), [C(2, -1, '=', 1), C(1, 1, '=', 5)]),
     (['x-2*y=-4', 'x+y=2'], ('0', '2'), [C(1, -2, '=', -4), C(1, 1, '=', 2)])]
for s_, so, cs in G: ls(s_, so); vx(cs, [(int(so[0]), int(so[1]))])
kind(['2*x+3*y=5', '4*x+6*y=10'], 'SCI'); kind(['x-y=2', '3*x-3*y=1'], 'SI'); kind(['x+2*y=3', '2*x-y=1'], 'SCD')
kind(['6*x+2*y=4', '3*x+y=5'], 'SI')
S.append(("Sistemas lineales. Método gráfico", [
 (1, r"Comprueba si $(2,-1)$ y $(1,1)$ son solución del sistema $" + sis('3x+2y=4', 'x-y=3') + "$.",
     r"$(2,-1)$: $6-2=4$ y $2+1=3$: " + R(r"\text{sí}") + r". \quad $(1,1)$: $3+2=5\neq4$: " + R(r"\text{no}") + "."),
 (2, r"Resuelve gráficamente los sistemas:" + tasks(3, ['$' + sis('x+y=5', 'x-y=1') + '$', '$' + sis('2x-y=1', 'x+y=5') + '$', '$' + sis('x-2y=-4', 'x+y=2') + '$'])
     + recorda(r"Haz una tabla de valores con dos puntos de cada recta. La solución es el punto de corte."),
     tasks(3, [XY(*so) + r'\\[2pt]' + fig(cs, (-2, 6, -2, 6), wd=3.6, hmax=3.6) for _, so, cs in G])),
 (2, r"Clasifica los sistemas sin resolverlos:" + tasks(3, ['$' + sis('2x+3y=5', '4x+6y=10') + '$', '$' + sis('x-y=2', '3x-3y=1') + '$', '$' + sis('x+2y=3', '2x-y=1') + '$']),
     tasks(3, [r"$\frac24=\frac36=\frac5{10}$: " + R(r"\text{SCI}"), r"$\frac13=\frac{-1}{-3}\neq\frac21$: " + R(r"\text{SI}"), r"$\frac12\neq\frac2{-1}$: " + R(r"\text{SCD}")])),
 (3, r"Halla el valor de $k$ para que el sistema $" + sis('kx+2y=4', '3x+y=5') + "$ sea incompatible.",
     r"Las rectas deben ser paralelas: $\frac k3=\frac21\Rightarrow" + Rm("k=6") + r"$; y como $\frac45\neq2$, no son la misma recta."),
]))

# =====================================================================
# 2. Mètodes de substitució, igualació i reducció
for s_, so in [(['y=2*x-3', '3*x+y=7'], ('2', '1')), (['x+3*y=10', '2*x-y=6'], ('4', '2')), (['y=x+4', 'y=3*x'], ('2', '6')), (['x=2*y-1', 'x=8-y'], ('5', '3')),
               (['2*x+3*y=12', '2*x-y=4'], ('3', '2')), (['3*x+2*y=7', '5*x-3*y=18'], ('3', '-1')), (['4*x+3*y=1', '3*x-2*y=5'], ('1', '-1')), (['x+y=9', 'x-y=3'], ('6', '3')),
               (['(x+1)/2+y/3=2', '2*(x-y)=x-3'], ('3/2', '9/4')), (['x/3+y/2=4', 'x/2-y/4=2'], ('6', '4')), (['3*(x-1)+y=6', 'x-2*(y+1)=-6'], ('2', '3')),
               (['x/2+y=5', '3*(x-1)-2*y=3'], ('4', '3')), (['(x+1)/5=y-1', '2*(x-y)+y=6'], ('4', '2')), (['x/3-y=4', '2*(x+y)-3*x=-10'], ('6', '-2')),
               (['x=(y+7)/3', 'x=(11-y)/3'], ('3', '2')), (['y/2=(x-1)/3', 'y=6-x'], ('4', '2')), (['x=(y-6)/2', 'x+y=3'], ('-1', '4')),
               (['(x+y)/2+(x-y)/4=Rational(5,2)', '2*(x+1)-3*(y-1)=8'], ('3', '1')), (['(x-1)/3+(y+3)/2=Rational(4,3)', '3*(x+y)-2*(x-y)=-3'], ('2', '-1')), (['x/5-y/2=0', '(x+1)/3+(y-2)/4=2'], ('5', '2'))]:
    ls(s_, so)
kind(['2*x-4*y=6', '-x+2*y=-3'], 'SCI'); kind(['x+y=3', '2*x+2*y=7'], 'SI')
S.append(("Métodos de sustitución, igualación y reducción", [
 (2, r"Resuelve por el método de sustitución:" + tasks(2, ['$' + sis('y=2x-3', '3x+y=7') + '$', '$' + sis('x+3y=10', '2x-y=6') + '$', '$' + sis(r'\dfrac x2+y=5', '3(x-1)-2y=3') + '$',
      '$' + sis(r'\dfrac{x+1}{5}=y-1', '2(x-y)+y=6') + '$', '$' + sis(r'\dfrac x3-y=4', '2(x+y)-3x=-10') + '$']),
     tasks(1, [r"$3x+2x-3=7$: " + XY('2', '1'), r"$x=10-3y\Rightarrow 20-6y-y=6$: " + XY('4', '2'), r"$x=10-2y\Rightarrow 3(9-2y)-2y=3\Rightarrow-8y=-24$: " + XY('4', '3'),
               r"$x=5y-6\Rightarrow 2(4y-6)+y=6\Rightarrow 9y=18$: " + XY('4', '2'), r"$y=\frac x3-4\Rightarrow -x+2\left(\frac x3-4\right)=-10\Rightarrow-\frac x3=-2$: " + XY('6', '-2')])),
 (2, r"Resuelve por el método de igualación:" + tasks(2, ['$' + sis('y=x+4', 'y=3x') + '$', '$' + sis('x=2y-1', 'x=8-y') + '$', '$' + sis(r'x=\dfrac{y+7}{3}', r'x=\dfrac{11-y}{3}') + '$',
      '$' + sis(r'\dfrac y2=\dfrac{x-1}{3}', 'y=6-x') + '$', '$' + sis(r'x=\dfrac{y-6}{2}', 'x+y=3') + '$']),
     tasks(1, [r"$x+4=3x$: " + XY('2', '6'), r"$2y-1=8-y$: " + XY('5', '3'), r"$y+7=11-y$: " + XY('3', '2'),
               r"$y=\frac{2(x-1)}{3}$ y $y=6-x$: $\frac{2(x-1)}{3}=6-x\Rightarrow5x=20$: " + XY('4', '2'), r"$x=3-y$: $\frac{y-6}{2}=3-y\Rightarrow3y=12$: " + XY('-1', '4')])),
 (2, r"Resuelve por el método de reducción:" + tasks(2, ['$' + sis('2x+3y=12', '2x-y=4') + '$', '$' + sis('3x+2y=7', '5x-3y=18') + '$', '$' + sis('4x+3y=1', '3x-2y=5') + '$',
      '$' + sis(r'\dfrac{x+y}{2}+\dfrac{x-y}{4}=\dfrac52', '2(x+1)-3(y-1)=8') + '$', '$' + sis(r'\dfrac{x-1}{3}+\dfrac{y+3}{2}=\dfrac43', '3(x+y)-2(x-y)=-3') + '$',
      '$' + sis(r'\dfrac x5-\dfrac y2=0', r'\dfrac{x+1}{3}+\dfrac{y-2}{4}=2') + '$'])
     + recorda(r"Multiplica las ecuaciones para que una incógnita tenga el mismo coeficiente (o el opuesto) y réstalas (o súmalas)."),
     tasks(1, [r"Restando: $4y=8$; " + XY('3', '2'), r"$3E_1+2E_2$: $19x=57$; " + XY('3', '-1'), r"$2E_1+3E_2$: $17x=17$; " + XY('1', '-1'),
               r"$" + sis('3x+y=10', '2x-3y=3') + r"$, \ $3E_1+E_2$: $11x=33$; " + XY('3', '1'), r"$" + sis('2x+3y=1', 'x+5y=-3') + r"$, \ $E_1-2E_2$: $-7y=7$; " + XY('2', '-1'),
               r"$" + sis('2x-5y=0', '4x+3y=26') + r"$, \ $E_2-2E_1$: $13y=26$; " + XY('5', '2')])),
 (2, r"Resuelve el sistema $" + sis('x+y=9', 'x-y=3') + r"$ por los tres métodos algebraicos y comprueba que obtienes la misma solución.",
     r"Sustitución: $x=9-y\Rightarrow9-2y=3$. Igualación: $9-y=3+y$. Reducción: sumando, $2x=12$. En los tres: " + XY('6', '3') + "."),
 (2, r"Simplifica las ecuaciones y resuelve:" + tasks(3, ['$' + sis(r'\dfrac{x+1}{2}+\dfrac y3=2', '2(x-y)=x-3') + '$', '$' + sis(r'\dfrac x3+\dfrac y2=4', r'\dfrac x2-\dfrac y4=2') + '$', '$' + sis('3(x-1)+y=6', 'x-2(y+1)=-6') + '$']),
     tasks(1, [r"$" + sis('3x+2y=9', 'x-2y=-3') + r"$: " + XY(r'\frac32', r'\frac94'), r"$" + sis('2x+3y=24', '2x-y=8') + r"$: " + XY('6', '4'), r"$" + sis('3x+y=9', 'x-2y=-4') + r"$: " + XY('2', '3')])),
 (2, r"Resuelve y clasifica:" + tasks(2, ['$' + sis('2x-4y=6', '-x+2y=-3') + '$', '$' + sis('x+y=3', '2x+2y=7') + '$']),
     tasks(1, [r"La 1.\textsuperscript{a} es $-2$ por la 2.\textsuperscript{a}: " + R(r"\text{SCI}") + r", con infinitas soluciones $x=3+2y$ (por ejemplo, $(3,0)$, $(5,1)$\ldots).", r"Restando el doble de la 1.\textsuperscript{a}: $0=1$, imposible: " + R(r"\text{SI}") + "."])),
]))

# =====================================================================
# 3. Sistemes no lineals
nls(['x+y=5', 'x**2+y**2=13'], [('2', '3'), ('3', '2')]); nls(['x-y=2', 'x*y=15'], [('5', '3'), ('-3', '-5')]); nls(['y=x**2-4', 'y=2*x-1'], [('3', '5'), ('-1', '-3')])
nls(['x**2+y**2=25', 'x**2-y**2=7'], [('4', '3'), ('4', '-3'), ('-4', '3'), ('-4', '-3')]); nls(['2*x**2+y**2=6', 'x**2-y**2=3'], [('sqrt(3)', '0'), ('-sqrt(3)', '0')])
nls(['x+y=1', '1/x+1/y=-Rational(1,6)'], [('3', '-2'), ('-2', '3')]); nls(['x**2+y**2=10', 'x*y=3'], [('1', '3'), ('3', '1'), ('-1', '-3'), ('-3', '-1')])
nls(['x**2+y**2=4', 'y=x+3'], [])
nls(['x**2+y**2=10', 'x+y=4'], [('1', '3'), ('3', '1')]); nls(['y=x**2-2*x', 'y=x+4'], [('4', '8'), ('-1', '3')]); nls(['1/x+1/y=Rational(5,6)', 'x+y=5'], [('2', '3'), ('3', '2')])
nls(['x*y=12', 'x**2+y**2=25'], [('3', '4'), ('4', '3'), ('-3', '-4'), ('-4', '-3')]); nls(['sqrt(x)+y=5', 'x-y=1'], [('4', '3')]); nls(['sqrt(x+y)=3', 'x-y=1'], [('5', '4')]); nls(['sqrt(x+3)=y', 'x+y=9'], [('6', '3')])
S.append(("Sistemas no lineales", [
 (2, r"Resuelve por el método de sustitución:" + tasks(3, ['$' + sis('x+y=5', 'x^2+y^2=13') + '$', '$' + sis('x-y=2', 'xy=15') + '$', '$' + sis('y=x^2-4', 'y=2x-1') + '$']),
     tasks(1, [r"$x^2+(5-x)^2=13\Rightarrow x^2-5x+6=0$: " + R(r"(2,3),\ (3,2)"), r"$(y+2)y=15\Rightarrow y^2+2y-15=0$: " + R(r"(5,3),\ (-3,-5)"), r"$x^2-4=2x-1\Rightarrow x^2-2x-3=0$: " + R(r"(3,5),\ (-1,-3)")])),
 (2, r"Resuelve por el método de reducción:" + tasks(2, ['$' + sis('x^2+y^2=25', 'x^2-y^2=7') + '$', '$' + sis('2x^2+y^2=6', 'x^2-y^2=3') + '$']),
     tasks(1, [r"Sumando: $2x^2=32\Rightarrow x=\pm4$, $y=\pm3$: " + R(r"(4,3),\ (4,-3),\ (-4,3),\ (-4,-3)"), r"Sumando: $3x^2=9\Rightarrow x=\pm\sqrt3$, $y=0$: " + R(r"(\sqrt3,0),\ (-\sqrt3,0)")])),
 (3, r"Resuelve:" + tasks(2, ['$' + sis('x+y=1', r'\dfrac1x+\dfrac1y=-\dfrac16') + '$', '$' + sis('x^2+y^2=10', 'xy=3') + '$']),
     tasks(1, [r"$\frac{x+y}{xy}=-\frac16\Rightarrow xy=-6$; $x(1-x)=-6$: " + R(r"(3,-2),\ (-2,3)"), r"$y=\frac3x\Rightarrow x^4-10x^2+9=0\Rightarrow x=\pm1,\ \pm3$: " + R(r"(1,3),\ (3,1),\ (-1,-3),\ (-3,-1)")])),
 (2, r"Resuelve:" + tasks(2, ['$' + sis('x^2+y^2=10', 'x+y=4') + '$', '$' + sis('y=x^2-2x', 'y=x+4') + '$', '$' + sis(r'\dfrac1x+\dfrac1y=\dfrac56', 'x+y=5') + '$', '$' + sis('xy=12', 'x^2+y^2=25') + '$']),
     tasks(1, [r"$x^2+(4-x)^2=10\Rightarrow x^2-4x+3=0$: " + R(r"(1,3),\ (3,1)"), r"$x^2-2x=x+4\Rightarrow x^2-3x-4=0$: " + R(r"(4,8),\ (-1,3)"),
               r"$\frac{x+y}{xy}=\frac56\Rightarrow xy=6$; $x(5-x)=6$: " + R(r"(2,3),\ (3,2)"), r"$y=\frac{12}x\Rightarrow x^4-25x^2+144=0\Rightarrow x=\pm3,\ \pm4$: " + R(r"(3,4),\ (4,3),\ (-3,-4),\ (-4,-3)")])),
 (3, r"Resuelve los sistemas siguientes, en los que hay raíces. Comprueba las soluciones:" + tasks(3, ['$' + sis(r'\sqrt x+y=5', 'x-y=1') + '$', '$' + sis(r'\sqrt{x+y}=3', 'x-y=1') + '$', '$' + sis(r'\sqrt{x+3}=y', 'x+y=9') + '$'])
     + recorda(r"Aísla la raíz y eleva al cuadrado; después comprueba cada solución en el sistema inicial, porque al elevar al cuadrado pueden aparecer soluciones falsas."),
     tasks(1, [r"$y=x-1\Rightarrow\sqrt x=6-x\Rightarrow x^2-13x+36=0\Rightarrow x=4,\ x=9$; $x=9$ no vale ($\sqrt9\neq6-9$): " + R(r"(4,3)"),
               r"$x+y=9$ y $x-y=1$: " + R(r"(5,4)"), r"$y=9-x\Rightarrow x+3=(9-x)^2\Rightarrow x^2-19x+78=0\Rightarrow x=6,\ x=13$; $x=13$ no vale ($y=-4<0$): " + R(r"(6,3)")])),
 (2, r"Sin dibujar, averigua si la recta $y=x+3$ corta a la circunferencia $x^2+y^2=4$.",
     r"$x^2+(x+3)^2=4\Rightarrow2x^2+6x+5=0$, $\Delta=36-40<0$: " + R(r"\text{no la corta}") + r" (el sistema no tiene solución)."),
]))

# =====================================================================
# 4. Problemes amb sistemes
for s_, so in [(['x+y=28', 'x-y=4'], ('16', '12')), (['3*x+2*y=33', '2*x+3*y=27'], ('9', '3')), (['x+y=11', '9*x-9*y=27'], ('7', '4')), (['x+y=20', '8*x+12*y=188'], ('13', '7'))]: ls(s_, so)
nls(['x+y=14', 'x**2+y**2=100'], [('8', '6'), ('6', '8')]); nls(['x**2+y**2=169', 'x*y=60'], [('12', '5'), ('5', '12'), ('-12', '-5'), ('-5', '-12')])
S.append(("Problemas con sistemas", [
 (1, r"En una clase hay 28 alumnos, y el número de chicas supera en 4 al de chicos. ¿Cuántas chicas y cuántos chicos hay?",
     r"$" + sis('x+y=28', 'x-y=4') + r"$: " + R(r"16\ \text{chicas y}\ 12\ \text{chicos}") + "."),
 (2, r"Tres entradas de adulto y dos de niño cuestan 33 €, y dos de adulto y tres de niño, 27 €. ¿Cuánto cuesta cada entrada?",
     r"$" + sis('3a+2c=33', '2a+3c=27') + r"$: " + R(r"\text{adulto}\ 9\ \text{€, niño}\ 3\ \text{€}") + "."),
 (2, r"Las cifras de un número de dos cifras suman 11. Si las intercambiamos, el número disminuye en 27. ¿Cuál es el número?",
     r"$x$ decenas, $y$ unidades: $" + sis('x+y=11', '(10x+y)-(10y+x)=27') + r"\Rightarrow x-y=3$: el número es " + R("74") + "."),
 (2, r"Queremos hacer 20 kg de una mezcla de café a 9,40 €/kg con café de 8 €/kg y café de 12 €/kg. ¿Cuántos kilos debemos poner de cada clase?",
     r"$" + sis('x+y=20', '8x+12y=20\cdot9{,}40=188') + r"$: " + R(r"13\ \text{kg de 8 € y}\ 7\ \text{kg de 12 €}") + "."),
 (2, r"El perímetro de un rectángulo es de 28 m y la diagonal mide 10 m. ¿Cuánto miden los lados?",
     r"$" + sis('x+y=14', 'x^2+y^2=100') + r"\Rightarrow x^2-14x+48=0$: " + R(r"8\ \text{m y}\ 6\ \text{m}") + "."),
 (3, r"La hipotenusa de un triángulo rectángulo mide 13 cm y el área, 30 cm$^2$. ¿Cuánto miden los catetos?",
     r"$" + sis('x^2+y^2=169', r'\frac{xy}{2}=30') + r"$; como $(x+y)^2=169+120=289$, $x+y=17$ y $xy=60$: " + R(r"12\ \text{cm y}\ 5\ \text{cm}") + "."),
]))

# =====================================================================
# 5. Sistemes d'inequacions amb una incògnita
for s_, e in [(['x-3<0', 'x+1>=0'], '[-1,3)'), (['2*x+1>5', '3*x-2<=10'], '(2,4]'), (['x+4<1', '2*x>-2'], '0'), (['5-x<=2', '4*x+1>=9'], '[3,inf)'),
              (['3*(x-1)>=x+1', '(x+2)/3<2'], '[2,4)'), (['2*x-5<x+1', 'x/2+1>0'], '(-2,6)'), (['x**2-9<=0', '2*x-1>0'], '(1/2,3]'), (['x**2-4*x>0', 'x+2>=0'], '[-2,0)U(4,inf)'),
              (['3+Rational(6,5)*x>=9', '3+Rational(6,5)*x<=15'], '[5,10]')]:
    ineqs(s_, e)
S.append(("Sistemas de inecuaciones con una incógnita", [
 (1, r"Resuelve los sistemas y representa la solución:" + tasks(2, ['$' + sis(r'x-3<0', r'x+1\ge0') + '$', '$' + sis(r'2x+1>5', r'3x-2\le10') + '$', '$' + sis(r'x+4<1', r'2x>-2') + '$', '$' + sis(r'5-x\le2', r'4x+1\ge9') + '$'])
     + recorda(r"Resuelve cada inecuación y haz la intersección de las soluciones: dibújalas una encima de la otra."),
     tasks(2, [RI('[-1,3)'), RI('(2,4]'), r"$x<-3$ y $x>-1$: " + R(r"\varnothing"), r"$x\ge3$ y $x\ge2$: " + RI('[3,inf)')])),
 (2, r"Resuelve:" + tasks(2, ['$' + sis(r'3(x-1)\ge x+1', r'\dfrac{x+2}{3}<2') + '$', '$' + sis(r'2x-5<x+1', r'\dfrac x2+1>0') + '$']),
     tasks(2, [r"$x\ge2$ y $x<4$: " + RI('[2,4)'), r"$x<6$ y $x>-2$: " + RI('(-2,6)')])),
 (3, r"Resuelve (alguna inecuación es de segundo grado):" + tasks(2, ['$' + sis(r'x^2-9\le0', r'2x-1>0') + '$', '$' + sis(r'x^2-4x>0', r'x+2\ge0') + '$']),
     tasks(1, [r"$[-3, 3]\cap\left(\frac12, +\infty\right)$: " + RI('(1/2,3]', -1, 4), r"$\big((-\infty, 0)\cup(4, +\infty)\big)\cap[-2, +\infty)$: " + RI('[-2,0)U(4,inf)')])),
 (2, r"Un taxi cobra 3 € por la bajada de bandera y 1,20 € por kilómetro. Si queremos gastar como mínimo 9 € y como máximo 15 €, ¿cuántos kilómetros podemos hacer?",
     r"$" + sis(r'3+1{,}2x\ge9', r'3+1{,}2x\le15') + r"\Rightarrow" + Rm(r"5\le x\le10") + r"$: entre 5 y 10 km."),
]))

# =====================================================================
# 6. Inequacions amb dues incògnites
H = [C(1, 1, '<=', 3), C(2, -1, '>', 4), C(-2, 1, '>=', 0), C(1, 0, '<', -1)]
pts26 = [((1, 1), 5 <= 6), ((3, -2), 0 <= 6), ((0, 5), 15 <= 6)]
assert [p[1] for p in pts26] == [True, True, False]
S.append(("Inecuaciones con dos incógnitas", [
 (1, r"Representa la solución de las inecuaciones:" + tasks(4, [r"$x+y\le3$", r"$2x-y>4$", r"$y\ge2x$", r"$x<-1$"])
     + recorda(r"Dibuja la recta frontera (continua si hay $\le$ o $\ge$, discontinua si hay $<$ o $>$) y prueba un punto que no esté en ella."),
     tasks(2, [t + r'\\[2pt]' + fig([h], (-4, 5, -4, 5), wd=3.4, hmax=3.4, labels=False) for t, h in zip([r"$(0,0)$: $0\le3$ sí, semiplano del origen.", r"$(0,0)$: $0>4$ no, el otro semiplano.", r"$(1,0)$: $0\ge2$ no, el otro semiplano.", r"$(0,0)$: $0<-1$ no, el otro semiplano."], H)])),
 (1, r"Indica cuáles de estos puntos son solución de $2x+3y\le6$: $A(1,1)$, $B(3,-2)$, $C(0,5)$.",
     r"$A$: $5\le6$ " + R(r"\text{sí}") + r"; \ $B$: $0\le6$ " + R(r"\text{sí}") + r"; \ $C$: $15\le6$ " + R(r"\text{no}") + "."),
]))

# =====================================================================
# 7. Sistemes d'inequacions amb dues incògnites
R27 = [([C(1, 1, '<=', 5), C(1, 0, '>=', 0), C(0, 1, '>=', 0)], [(0, 0), (5, 0), (0, 5)], True, (-1, 6, -1, 6)),
       ([C(-1, 1, '>=', 0), C(0, 1, '<=', 4), C(1, 0, '>=', 1)], [(1, 1), (1, 4), (4, 4)], True, (-1, 6, -1, 6)),
       ([C(1, 2, '<=', 8), C(1, -1, '>=', -1), C(0, 1, '>=', 0)], [(-1, 0), (8, 0), (2, 3)], True, (-2, 9, -1, 6))]
for cs, V, b, _ in R27: vx(cs, V, b)
R28 = [C(1, 1, '>=', 2), C(1, 0, '>=', 0), C(0, 1, '>=', 0)]; vx(R28, [(2, 0), (0, 2)], False)
R29 = [C(1, 1, '<=', 10), C(1, 0, '>=', 2), C(-1, 1, '<=', 0), C(0, 1, '>=', 0)]; vx(R29, [(2, 0), (10, 0), (5, 5), (2, 2)], True)
assert not (4 + 5 <= 10 and 5 <= 4)
def vt(V): return r',\ '.join('(%d,%d)' % v for v in V)
S.append(("Sistemas de inecuaciones con dos incógnitas", [
 (2, r"Representa la región solución de cada sistema y halla sus vértices:" + tasks(3, ['$' + sis(r'x+y\le5', r'x\ge0', r'y\ge0') + '$', '$' + sis(r'y\ge x', r'y\le4', r'x\ge1') + '$', '$' + sis(r'x+2y\le8', r'x-y\ge-1', r'y\ge0') + '$'])
     + recorda(r"La solución es la intersección de los semiplanos. Los vértices son los puntos de corte de las rectas frontera."),
     tasks(3, [R(vt(V)) + r'\\[2pt]' + fig(cs, view, wd=3.6, hmax=3.4) for cs, V, b, view in R27])),
 (3, r"Representa la región solución de $" + sis(r'x+y\ge2', r'x\ge0', r'y\ge0') + r"$. ¿Está acotada?",
     R(r"\text{No está acotada}") + r": tiene vértices en $(2,0)$ y $(0,2)$ y se extiende indefinidamente.\\[2pt]" + fig(R28, (-1, 6, -1, 6), wd=3.6, hmax=3.4)),
 (2, r"Un taller hace mesas ($x$) y sillas ($y$). Cada día puede hacer como máximo 10 piezas en total, al menos 2 mesas, y nunca más sillas que mesas. Escribe el sistema de inecuaciones, represéntalo y di si pueden hacer 4 mesas y 5 sillas.",
     r"$" + sis(r'x+y\le10', r'x\ge2', r'y\le x', r'y\ge0') + r"$, de vértices " + R(vt([(2, 0), (10, 0), (5, 5), (2, 2)])) + r". El punto $(4,5)$ \rest{no} es de la región: $5>4$, habría más sillas que mesas.\\[2pt]" + fig(R29, (-1, 11, -1, 7), wd=4.6, hmax=3.4)),
]))

build(HERE, 4, "Sistemas de ecuaciones e inecuaciones", S,
      "sistemas de ecuaciones, método gráfico, sustitución, igualación, reducción, sistemas no lineales, problemas, sistemas de inecuaciones, semiplanos",
      r"Resuélvelos en el cuaderno mostrando todos los pasos. Comprueba las soluciones de los sistemas en las dos ecuaciones y, en los problemas, responde con una frase.",
      r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar los sistemas, las inecuaciones y las regiones con las herramientas interactivas de los apuntes de la unidad.",
      extra_pre=PRE, lang='es')
