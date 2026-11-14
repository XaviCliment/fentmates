# Versió en castellà de genera.py. Genera t3-fitxa-exercicis-es.tex i t3-fitxa-solucions-es.tex (4t ESO Matemàtiques B, Unitat 3: Equacions i inequacions)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Cada solució escrita a mà es comprova amb sympy: sol() resol l'equació en els reals i la compara amb les solucions esperades,
# i ineq() resol la inequació i la compara amb l'interval esperat (que després es dibuixa amb RI).
# Ús: python3 genera-es.py && pdflatex t3-fitxa-exercicis-es.tex (dues vegades) && pdflatex t3-fitxa-solucions-es.tex (dues vegades)
import os, sys, math, re
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

x = sp.symbols('x', real=True)
L = {'x': x, 'ln': sp.log, 'log10': lambda a: sp.log(a, 10), 'log2': lambda a: sp.log(a, 2), 'E': sp.E}
def E(s): return sp.sympify(s, locals=L)
def sol(eq, expected):
    """eq: 'lhs = rhs'; expected: llista de solucions (cadenes de sympy) o [] si no en té"""
    l, r = eq.split('=')
    got = sp.solveset(sp.Eq(E(l), E(r)), x, domain=sp.S.Reals)
    exp = sp.FiniteSet(*[E(v) for v in expected])
    if not isinstance(got, sp.FiniteSet) and got != sp.S.EmptySet:
        # sympy no la resol: cada solució esperada la compleix i un escombratge numèric no en troba cap altra
        f = E(l) - E(r)
        for v in exp: assert sp.simplify(f.subs(x, v)) == 0, (eq, v)
        fl = sp.lambdify(x, f, 'math'); roots = []; prev = None
        for i in range(-40000, 40001):
            t = i / 2000
            try: y = fl(t)
            except (ValueError, ZeroDivisionError, OverflowError): prev = None; continue
            if isinstance(y, complex): prev = None; continue
            if prev is not None and (y == 0 or prev[1] * y < 0): roots.append(t)
            prev = (t, y)
        assert len(roots) == len(exp), (eq, roots, exp)
        return
    assert got == exp or sp.simplify(sp.Add(*[sp.Abs(a - b) for a, b in zip(sorted(got, key=float), sorted(exp, key=float))])) == 0 and len(got) == len(exp), (eq, got, exp)
def red(eq):
    """forma polinòmica reduïda (enters, coeficient principal positiu) d'una equació amb denominadors"""
    l, r = eq.split('=')
    num = sp.numer(sp.together(sp.expand(E(l) - E(r))))
    P = sp.Poly(sp.expand(num), x); cs = P.all_coeffs(); g = sp.gcd_list(cs)
    if cs[0] < 0: g = -g
    return sp.latex(sp.expand(num / g)) + '=0'
def sols(eq):
    l, r = eq.split('=')
    S_ = sorted(sp.solveset(sp.Eq(E(l), E(r)), x, domain=sp.S.Reals), key=float)
    return R(r',\ '.join('x=' + sp.latex(v) for v in S_)) if S_ else r"no tiene solución"

def toset(s):
    if s == 'R': return sp.S.Reals
    if s == '0': return sp.S.EmptySet
    out = sp.S.EmptySet
    for p in s.split('U'):
        m = re.match(r'^([\[\(])([^,]+),([^,]+)([\]\)])$', p.strip())
        a = -sp.oo if m.group(2) == '-inf' else sp.Rational(m.group(2)); b = sp.oo if m.group(3) == 'inf' else sp.Rational(m.group(3))
        out = out.union(sp.Interval(a, b, m.group(1) == '(', m.group(4) == ')'))
    return out
def ineq(expr, expected):
    got = sp.solve_univariate_inequality(E(expr), x, relational=False)
    assert got == toset(expected), (expr, got, expected)
def RS(s, lo=None, hi=None):
    """solució d'una inequació: conjunt i recta"""
    if s == 'R': return R(r'\mathbb R') + r'\\[2pt]' + recta(P('(-inf,inf)'), -3, 3)
    if s == '0': return R(r'\varnothing')
    return RI(s, lo, hi)
def X(*v): return R(r',\ '.join('x=' + t for t in v))

S = []

# =====================================================================
# 1. Equacions de segon grau
for e, s_ in [('x**2-16=0', ['4', '-4']), ('3*x**2+12*x=0', ['0', '-4']), ('2*x**2-50=0', ['5', '-5']), ('x**2+9=0', []), ('5*x**2=3*x', ['0', '3/5']), ('4*x**2-1=0', ['1/2', '-1/2']),
              ('x**2-5*x+6=0', ['2', '3']), ('x**2+2*x-15=0', ['3', '-5']), ('2*x**2-7*x+3=0', ['3', '1/2']), ('x**2-6*x+9=0', ['3']), ('x**2+x+3=0', []), ('6*x**2-x-1=0', ['1/2', '-1/3']),
              ('(x+2)**2=3*x+10', ['2', '-3']), ('x*(x-3)=2*(x+7)', ['7', '-2']), ('(2*x-1)*(x+3)-x**2=3', ['1', '-6']), ('x**2/3-x/2=Rational(3,2)', ['3', '-3/2']), ('x**2+2*x-15=0', ['3', '-5'])]:
    sol(e, s_)
assert [b * b - 4 * a * c for a, b, c in [(3, -2, 5), (4, -12, 9), (1, 1, -1)]] == [-56, 0, 5]
Q2 = [('x*(x+3)/2-(x-1)*(x+1)/3=4', '\\dfrac{x(x+3)}{2}-\\dfrac{(x-1)(x+1)}{3}=4'), ('(x+3)*(x-3)/4-(x-1)**2/2=-2', '\\dfrac{(x+3)(x-3)}{4}-\\dfrac{(x-1)^2}{2}=-2'), ('(2*x+1)*(x-3)/5-(x-1)/2=(x**2-13)/10', '\\dfrac{(2x+1)(x-3)}{5}-\\dfrac{x-1}{2}=\\dfrac{x^2-13}{10}'), ('(x+1)**2/2-(x-1)**2/3=(x+11)/6+x', '\\dfrac{(x+1)^2}{2}-\\dfrac{(x-1)^2}{3}=\\dfrac{x+11}{6}+x'), ('x*(x-1)/3-(x+1)*(x-2)/4=1', '\\dfrac{x(x-1)}{3}-\\dfrac{(x+1)(x-2)}{4}=1'), ('(x-1)*(x+2)/4-(x+1)/2=(x-7)/4', '\\dfrac{(x-1)(x+2)}{4}-\\dfrac{x+1}{2}=\\dfrac{x-7}{4}'), ('(x+2)**2/4-(x-1)/2=(x**2+11)/8', '\\dfrac{(x+2)^2}{4}-\\dfrac{x-1}{2}=\\dfrac{x^2+11}{8}'), ('2*(x-1)**2-3*(x+1)*(x-2)=x*(x-5)-4', '2(x-1)^2-3(x+1)(x-2)=x(x-5)-4')]
S.append(("Ecuaciones de segundo grado", [
 (1, r"Resuelve las ecuaciones incompletas:" + tasks(3, [r"$x^2-16=0$", r"$3x^2+12x=0$", r"$2x^2-50=0$", r"$x^2+9=0$", r"$5x^2=3x$", r"$4x^2-1=0$"]),
     tasks(3, [X(r"\pm4"), X("0", "-4"), X(r"\pm5"), r"No tiene solución.", X("0", r"\frac35"), X(r"\pm\frac12")])),
 (1, r"Resuelve las ecuaciones:" + tasks(3, [r"$x^2-5x+6=0$", r"$x^2+2x-15=0$", r"$2x^2-7x+3=0$", r"$x^2-6x+9=0$", r"$x^2+x+3=0$", r"$6x^2-x-1=0$"])
     + recorda(r"$ax^2+bx+c=0\Rightarrow x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$."),
     tasks(3, [X("2", "3"), X("3", "-5"), X("3", r"\frac12"), X("3") + r" (doble)", r"No tiene solución ($\Delta<0$).", X(r"\frac12", r"-\frac13")])),
 (2, r"Opera hasta obtener la forma $ax^2+bx+c=0$ y resuelve:" + tasks(2, [r"$(x+2)^2=3x+10$", r"$x(x-3)=2(x+7)$", r"$(2x-1)(x+3)-x^2=3$", r"$\dfrac{x^2}{3}-\dfrac x2=\dfrac32$"], gap='10pt'),
     tasks(2, [r"$x^2+x-6=0$: " + X("2", "-3"), r"$x^2-5x-14=0$: " + X("7", "-2"), r"$x^2+5x-6=0$: " + X("1", "-6"), r"$2x^2-3x-9=0$: " + X("3", r"-\frac32")])),
 (3, r"Elimina los paréntesis y los denominadores, pasa a la forma $ax^2+bx+c=0$ y resuelve:" + tasks(2, ["$" + t + "$" for _, t in Q2], gap='14pt')
     + recorda(r"Primero desarrolla los productos y las identidades notables; después multiplica todos los términos por el m.c.m. de los denominadores. ¡Cuidado con el signo menos delante de una fracción!"),
     tasks(1, ["$" + red(e) + "$: " + sols(e) for e, _ in Q2])),
 (2, r"Sin resolverlas, indica cuántas soluciones tiene cada ecuación:" + tasks(3, [r"$3x^2-2x+5=0$", r"$4x^2-12x+9=0$", r"$x^2+x-1=0$"]) + r"Halla después $k$ para que $x^2-6x+k=0$ tenga una solución doble.",
     tasks(3, [r"$\Delta=-56$: " + R(r"\text{ninguna}"), r"$\Delta=0$: " + R(r"\text{una (doble)}"), r"$\Delta=5$: " + R(r"\text{dos}")]) + r"$\Delta=36-4k=0\Rightarrow" + Rm("k=9") + "$."),
 (3, r"Escribe una ecuación de segundo grado que tenga por soluciones $x=3$ y $x=-5$.",
     r"$(x-3)(x+5)=0\Rightarrow" + Rm("x^2+2x-15=0") + "$ (o cualquier múltiplo)."),
]))

# =====================================================================
# 2. Equacions biquadrades
for e, s_ in [('x**4-10*x**2+9=0', ['1', '-1', '3', '-3']), ('x**4-5*x**2-36=0', ['3', '-3']), ('x**4+3*x**2+2=0', []), ('4*x**4-17*x**2+4=0', ['2', '-2', '1/2', '-1/2']),
              ('x**4-8*x**2=0', ['0', '2*sqrt(2)', '-2*sqrt(2)']), ('(x**2-1)*(x**2+2)=10', ['sqrt(3)', '-sqrt(3)']), ('x**4-16=0', ['2', '-2'])]:
    sol(e, s_)
B2 = [('(x**2-2)*(x**2+2)=3*x**2', '(x^2-2)(x^2+2)=3x^2'), ('x**2*(x**2-5)/2=-2', '\\dfrac{x^2(x^2-5)}{2}=-2'), ('(x**2+1)**2-3*(x**2+1)=10', '(x^2+1)^2-3(x^2+1)=10'), ('x**4/4-5*x**2/2+4=0', '\\dfrac{x^4}{4}-\\dfrac{5x^2}{2}+4=0'), ('x**4/3-(x**2+2)/2=x**2-Rational(5,2)', '\\dfrac{x^4}{3}-\\dfrac{x^2+2}{2}=x^2-\\dfrac52'), ('(2*x**2-1)**2-(x**2+2)**2=3*x**4-21', '(2x^2-1)^2-(x^2+2)^2=3x^4-21')]
S.append(("Ecuaciones bicuadradas", [
 (1, r"Resuelve las ecuaciones bicuadradas:" + tasks(2, [r"$x^4-10x^2+9=0$", r"$x^4-5x^2-36=0$", r"$x^4+3x^2+2=0$", r"$4x^4-17x^2+4=0$"])
     + recorda(r"Haz el cambio $t=x^2$. Cada solución $t>0$ da $x=\pm\sqrt t$; las $t<0$ no dan soluciones."),
     tasks(2, [r"$t=9,\ t=1$: " + X(r"\pm3", r"\pm1"), r"$t=9,\ t=-4$: " + X(r"\pm3"), r"$t=-1,\ t=-2$: no tiene solución.", r"$t=4,\ t=\frac14$: " + X(r"\pm2", r"\pm\frac12")])),
 (2, r"Resuelve:" + tasks(3, [r"$x^4-8x^2=0$", r"$(x^2-1)(x^2+2)=10$", r"$x^4-16=0$"]),
     tasks(1, [r"$x^2(x^2-8)=0$: " + X("0", r"\pm2\sqrt2"), r"$x^4+x^2-12=0$: " + X(r"\pm\sqrt3"), X(r"\pm2")])),
 (3, r"Opera hasta obtener una ecuación bicuadrada y resuelve:" + tasks(2, ["$" + t + "$" for _, t in B2], gap='14pt'),
     tasks(1, ["$" + red(e) + "$: " + sols(e) for e, _ in B2]))
]))

# =====================================================================
# 3. Equacions polinòmiques de grau major que 2
for e, s_ in [('x**3-6*x**2+11*x-6=0', ['1', '2', '3']), ('x**3+2*x**2-x-2=0', ['1', '-1', '-2']), ('x**3-3*x+2=0', ['1', '-2']), ('2*x**3+x**2-8*x-4=0', ['2', '-1/2', '-2']),
              ('x**4-x**3-7*x**2+x+6=0', ['1', '-1', '-2', '3']), ('x**3=4*x', ['0', '2', '-2']), ('x**4+x**3=x**2+x', ['0', '-1', '1'])]:
    sol(e, s_)
S.append(("Ecuaciones de grado mayor que 2", [
 (2, r"Resuelve con la regla de Ruffini:" + tasks(2, [r"$x^3-6x^2+11x-6=0$", r"$x^3+2x^2-x-2=0$", r"$x^3-3x+2=0$", r"$2x^3+x^2-8x-4=0$"])
     + recorda(r"Prueba con los divisores del término independiente hasta llegar a una ecuación de segundo grado."),
     tasks(2, [X("1", "2", "3"), X("1", "-1", "-2"), r"$(x-1)^2(x+2)=0$: " + X("1", "-2"), X("2", r"-\frac12", "-2")])),
 (2, r"Pasa todos los términos a un miembro, factoriza y resuelve:" + tasks(3, [r"$x^4-x^3-7x^2+x+6=0$", r"$x^3=4x$", r"$x^4+x^3=x^2+x$"]),
     tasks(1, [r"$(x-1)(x+1)(x+2)(x-3)=0$: " + X(r"\pm1", "-2", "3"), r"$x(x+2)(x-2)=0$: " + X("0", r"\pm2"), r"$x(x+1)^2(x-1)=0$: " + X("0", "-1", "1")])),
]))

# =====================================================================
# 4. Equacions factoritzades
for e, s_ in [('(x-4)*(x+1)=0', ['4', '-1']), ('x*(2*x+3)*(x-5)=0', ['0', '-3/2', '5']), ('(x-1)**2*(x+7)=0', ['1', '-7']), ('3*(x+2)*(4*x-1)=0', ['-2', '1/4']),
              ('(x**2-16)*(x+3)=0', ['4', '-4', '-3']), ('(x**2-3*x+2)*(x**2+5)=0', ['1', '2']), ('x**3*(x**2-2*x-8)=0', ['0', '4', '-2']), ('(x-2)*(x+1)=4', ['3', '-2'])]:
    sol(e, s_)
S.append(("Ecuaciones factorizadas", [
 (1, r"Resuelve sin multiplicar los factores:" + tasks(2, [r"$(x-4)(x+1)=0$", r"$x(2x+3)(x-5)=0$", r"$(x-1)^2(x+7)=0$", r"$3(x+2)(4x-1)=0$"])
     + recorda(r"Un producto es cero si alguno de los factores es cero."),
     tasks(2, [X("4", "-1"), X("0", r"-\frac32", "5"), X("1", "-7"), X("-2", r"\frac14")])),
 (2, r"Resuelve:" + tasks(2, [r"$(x^2-16)(x+3)=0$", r"$(x^2-3x+2)(x^2+5)=0$", r"$x^3(x^2-2x-8)=0$", r"$(x-2)(x+1)=4$"]),
     tasks(2, [X(r"\pm4", "-3"), X("1", "2") + r" ($x^2+5=0$ no da ninguna)", X("0", "4", "-2"), r"No es «$=0$»: $x^2-x-6=0$, " + X("3", "-2")])),
]))

# =====================================================================
# 5. Equacions amb fraccions algebraiques
for e, s_ in [('5/x-1=4', ['1']), ('x/(x-1)=Rational(3,2)', ['3']), ('1/x+2/(x+1)=1', ['1+sqrt(2)', '1-sqrt(2)']), ('x+4/x=5', ['1', '4']),
              ('x/(x+2)-1/(x-2)=8/(x**2-4)', ['5']), ('3/(x-1)-2/(x+1)=6/(x**2-1)', []), ('1/(x-1)+1/(x+1)=Rational(4,3)', ['2', '-1/2']),
              ('x/(x-2)-2/(x+2)=8/(x**2-4)', []), ('(x+3)/(x-1)-(x-3)/(x+1)=4', ['1+sqrt(2)', '1-sqrt(2)']), ('2/x-3/(x**2+x)=1/(x+1)', ['1']), ('(x+1)/x-x/(x+1)=Rational(5,6)', ['2', '-3/5'])]:
    sol(e, s_)
S.append(("Ecuaciones con fracciones algebraicas", [
 (1, r"Resuelve:" + tasks(2, [r"$\dfrac5x-1=4$", r"$\dfrac{x}{x-1}=\dfrac32$", r"$\dfrac1x+\dfrac{2}{x+1}=1$", r"$x+\dfrac4x=5$"], gap='12pt'),
     tasks(2, [X("1"), X("3"), r"$x^2-2x-1=0$: " + X(r"1\pm\sqrt2"), r"$x^2-5x+4=0$: " + X("1", "4")])),
 (2, r"Resuelve y comprueba las soluciones:" + tasks(2, [r"$\dfrac{x}{x+2}-\dfrac{1}{x-2}=\dfrac{8}{x^2-4}$", r"$\dfrac{3}{x-1}-\dfrac{2}{x+1}=\dfrac{6}{x^2-1}$",
      r"$\dfrac{1}{x-1}+\dfrac{1}{x+1}=\dfrac43$", r"$\dfrac{x}{x-2}-\dfrac{2}{x+2}=\dfrac{8}{x^2-4}$", r"$\dfrac{x+3}{x-1}-\dfrac{x-3}{x+1}=4$", r"$\dfrac2x-\dfrac{3}{x^2+x}=\dfrac{1}{x+1}$"], gap='14pt')
     + recorda(r"Descarta las soluciones que anulan algún denominador."),
     tasks(1, [r"$x^2-3x-10=0\Rightarrow x=5,\ x=-2$; $x=-2$ anula un denominador: " + X("5"), r"$x+5=6\Rightarrow x=1$, que anula $x-1$: " + R(r"\text{no tiene solución}"),
               r"$2x^2-3x-2=0$: " + X("2", r"-\frac12"), r"$x^2+4=8\Rightarrow x=\pm2$, y las dos anulan un denominador: " + R(r"\text{no tiene solución}"),
               r"$x^2-2x-1=0$: " + X(r"1\pm\sqrt2"), r"$2(x+1)-3=x$: " + X("1")])),
 (3, r"Resuelve $\dfrac{x+1}{x}-\dfrac{x}{x+1}=\dfrac56$.",
     r"m.c.m. $=6x(x+1)$: $6(x+1)^2-6x^2=5x(x+1)\Rightarrow5x^2-7x-6=0\Rightarrow" + Rm(r"x=2,\ x=-\frac35") + "$ (las dos valen)."),
]))

# =====================================================================
# 6. Equacions amb radicals
for e, s_ in [('sqrt(x+5)=3', ['4']), ('sqrt(2*x-1)=5', ['13']), ('sqrt(x**2+9)=5', ['4', '-4']), ('sqrt(x+3)=-2', []),
              ('sqrt(x+2)=x', ['2']), ('x+sqrt(x-1)=7', ['5']), ('sqrt(3*x+4)-x=0', ['4']), ('2*sqrt(x)=x-3', ['9']), ('sqrt(2*x+3)=x', ['3']), ('x-sqrt(x+10)=2', ['6']), ('sqrt(5*x+4)-2=x', ['0', '1']), ('3+sqrt(x-1)=x', ['5']),
              ('sqrt(x+7)-sqrt(x)=1', ['9']), ('sqrt(2*x+1)+sqrt(x-3)=4', ['4'])]:
    sol(e, s_)
S.append(("Ecuaciones con radicales", [
 (1, r"Resuelve:" + tasks(4, [r"$\sqrt{x+5}=3$", r"$\sqrt{2x-1}=5$", r"$\sqrt{x^2+9}=5$", r"$\sqrt{x+3}=-2$"]),
     tasks(4, [X("4"), X("13"), X(r"\pm4"), r"No tiene: una raíz no es negativa."])),
 (2, r"Resuelve y comprueba las soluciones:" + tasks(2, [r"$\sqrt{x+2}=x$", r"$x+\sqrt{x-1}=7$", r"$\sqrt{3x+4}-x=0$", r"$2\sqrt x=x-3$",
      r"$\sqrt{2x+3}=x$", r"$x-\sqrt{x+10}=2$", r"$\sqrt{5x+4}-2=x$", r"$3+\sqrt{x-1}=x$"])
     + recorda(r"Aísla el radical, eleva al cuadrado y comprueba todas las soluciones en la ecuación inicial."),
     tasks(1, [r"$x^2-x-2=0\Rightarrow x=2,\ x=-1$; $x=-1$ no vale ($\sqrt1\neq-1$): " + X("2"), r"$x^2-15x+50=0\Rightarrow x=5,\ x=10$; $x=10$ no vale ($10+3\neq7$): " + X("5"),
               r"$x^2-3x-4=0\Rightarrow x=4,\ x=-1$; $x=-1$ no vale ($1+1\neq0$): " + X("4"), r"$x^2-10x+9=0\Rightarrow x=1,\ x=9$; $x=1$ no vale ($2\neq-2$): " + X("9"),
               r"$x^2-2x-3=0\Rightarrow x=3,\ x=-1$; $x=-1$ no vale: " + X("3"), r"$x^2-5x-6=0\Rightarrow x=6,\ x=-1$; $x=-1$ no vale ($-1-3\neq2$): " + X("6"),
               r"$x^2-x=0\Rightarrow x=0,\ x=1$; las dos valen: " + X("0", "1"), r"$x^2-7x+10=0\Rightarrow x=5,\ x=2$; $x=2$ no vale ($3+1\neq2$): " + X("5")])),
 (3, r"Resuelve (hay dos radicales):" + tasks(2, [r"$\sqrt{x+7}-\sqrt x=1$", r"$\sqrt{2x+1}+\sqrt{x-3}=4$"]),
     tasks(1, [r"$x+7=1+2\sqrt x+x\Rightarrow\sqrt x=3$: " + X("9"), r"$x-12=-8\sqrt{x-3}\Rightarrow x^2-88x+336=0\Rightarrow x=4,\ x=84$; $x=84$ no vale ($13+9\neq4$): " + X("4")])),
]))

# =====================================================================
# 7. Equacions exponencials
for e, s_ in [('2**x=32', ['5']), ('3**(x-2)=27', ['5']), ('5**(2*x)=Rational(1,25)', ['-1']), ('4**x=8', ['3/2']), ('2**(x**2-1)=8', ['2', '-2']), ('10**(x+1)=Rational(1,1000)', ['-4']),
              ('2**(x+1)+2**x=24', ['3']), ('3**(x+2)-3**x=72', ['2']), ('5**x+5**(x-1)=30', ['2']), ('4**x-5*2**x+4=0', ['0', '2']), ('9**x-10*3**x+9=0', ['0', '2']), ('4**x-2**x-12=0', ['2'])]:
    sol(e, s_)
c19 = [math.log(10, 2), math.log(50, 3), 1 + math.log(30, 7), math.log(2) / math.log(1.05)]
ck([round(v, 3) for v in c19], [3.322, 3.561, 2.748, 14.207])
S.append(("Ecuaciones exponenciales", [
 (1, r"Escribe los dos miembros como potencias de la misma base y resuelve:" + tasks(3, [r"$2^x=32$", r"$3^{x-2}=27$", r"$5^{2x}=\frac{1}{25}$", r"$4^x=8$", r"$2^{x^2-1}=8$", r"$10^{x+1}=0,001$"]),
     tasks(3, [X("5"), X("5"), X("-1"), X(r"\frac32"), X(r"\pm2"), X("-4")])),
 (1, r"Resuelve tomando logaritmos (da el resultado con tres decimales):" + tasks(4, [r"$2^x=10$", r"$3^x=50$", r"$7^{x-1}=30$", r"$1,05^x=2$"])
     + recorda(r"$a^x=b\Rightarrow x=\dfrac{\log b}{\log a}$."),
     tasks(2, [R(r"x=\frac{\log10}{\log2}\approx" + dec(c19[0])), R(r"x=\frac{\log50}{\log3}\approx" + dec(c19[1])), R(r"x=1+\frac{\log30}{\log7}\approx" + dec(c19[2])), R(r"x=\frac{\log2}{\log1,05}\approx" + dec(c19[3]))])),
 (2, r"Resuelve sacando factor común:" + tasks(3, [r"$2^{x+1}+2^x=24$", r"$3^{x+2}-3^x=72$", r"$5^x+5^{x-1}=30$"]),
     tasks(3, [r"$3\cdot2^x=24$: " + X("3"), r"$8\cdot3^x=72$: " + X("2"), r"$\frac65\cdot5^x=30$: " + X("2")])),
 (3, r"Resuelve con un cambio de variable:" + tasks(3, [r"$4^x-5\cdot2^x+4=0$", r"$9^x-10\cdot3^x+9=0$", r"$4^x-2^x-12=0$"]),
     tasks(1, [r"$t=2^x$: $t=1,\ t=4$; " + X("0", "2"), r"$t=3^x$: $t=1,\ t=9$; " + X("0", "2"), r"$t=4$ ($t=-3$ no vale): " + X("2")])),
]))

# =====================================================================
# 8. Equacions logarítmiques
for e, s_ in [('log10(x)=3', ['1000']), ('log2(x+1)=4', ['15']), ('ln(x)=0', ['1']), ('log(3*x-1,5)=2', ['26/3']),
              ('log10(x)+log10(4)=log10(20)', ['5']), ('log10(x+3)-log10(x-1)=log10(3)', ['3']), ('2*log10(x)=log10(5*x-6)', ['2', '3']), ('log10(x)+log10(x+9)=1', ['1']), ('log10(x+1)+log10(x-2)=1', ['4']), ('2*log10(x)-log10(x-2)=log10(9)', ['3', '6']),
              ('log10(2*x+4)-log10(x)=log10(3)', ['4']), ('log(x+2,3)+log(x-4,3)=3', ['7']),
              ('log10(x+6)=1+log10(x-3)', ['4']), ('log2(x)+log2(x-2)=3', ['4'])]:
    sol(e, s_)
S.append(("Ecuaciones logarítmicas", [
 (1, r"Resuelve aplicando la definición de logaritmo:" + tasks(4, [r"$\log x=3$", r"$\log_2(x+1)=4$", r"$\ln x=0$", r"$\log_5(3x-1)=2$"]),
     tasks(4, [X("1000"), X("15"), X("1"), X(r"\frac{26}{3}")])),
 (2, r"Resuelve y comprueba las soluciones:" + tasks(2, [r"$\log x+\log4=\log20$", r"$\log(x+3)-\log(x-1)=\log3$", r"$2\log x=\log(5x-6)$", r"$\log x+\log(x+9)=1$",
      r"$\log(x+1)+\log(x-2)=1$", r"$2\log x-\log(x-2)=\log9$", r"$\log(2x+4)-\log x=\log3$", r"$\log_3(x+2)+\log_3(x-4)=3$"])
     + recorda(r"Agrupa en un solo logaritmo en cada miembro. Los argumentos de los logaritmos deben ser positivos."),
     tasks(2, [X("5"), X("3"), r"$x^2-5x+6=0$: " + X("2", "3"), r"$x^2+9x-10=0$; $x=-10$ no vale: " + X("1"),
               r"$x^2-x-2=10\Rightarrow x=4,\ x=-3$; $x=-3$ no vale: " + X("4"), r"$x^2=9(x-2)\Rightarrow x^2-9x+18=0$; las dos valen: " + X("3", "6"),
               r"$2x+4=3x$: " + X("4"), r"$(x+2)(x-4)=27\Rightarrow x^2-2x-35=0$; $x=-5$ no vale: " + X("7")])),
 (3, r"Resuelve:" + tasks(2, [r"$\log(x+6)=1+\log(x-3)$", r"$\log_2x+\log_2(x-2)=3$"]),
     tasks(2, [r"$x+6=10(x-3)$: " + X("4"), r"$x^2-2x-8=0$; $x=-2$ no vale: " + X("4")])),
]))

# =====================================================================
# 9. Inequacions de primer grau
for e, s_ in [('2*x-5>3', '(4,inf)'), ('3-x<=5', '[-2,inf)'), ('4*x+1<2*x-7', '(-inf,-4)'), ('-3*x>=12', '(-inf,-4]'),
              ('3*(x-2)-2*(x+1)>=x-8', 'R'), ('(x+1)/2-(x-3)/4<2', '(-inf,3)'), ('2*x-(3-x)/2>x/3', '(9/13,inf)'), ('5*x-1>5*(x+1)', '0'), ('15+x/2>40', '(50,inf)')]:
    ineq(e, s_)
S.append(("Inecuaciones de primer grado", [
 (1, r"Resuelve y representa la solución:" + tasks(4, [r"$2x-5>3$", r"$3-x\le5$", r"$4x+1<2x-7$", r"$-3x\ge12$"])
     + recorda(r"Si multiplicas o divides por un número negativo, la desigualdad cambia de sentido."),
     tasks(2, [RS('(4,inf)'), RS('[-2,inf)'), RS('(-inf,-4)'), RS('(-inf,-4]')])),
 (2, r"Resuelve:" + tasks(2, [r"$3(x-2)-2(x+1)\ge x-8$", r"$\dfrac{x+1}{2}-\dfrac{x-3}{4}<2$", r"$2x-\dfrac{3-x}{2}>\dfrac x3$", r"$5x-1>5(x+1)$"], gap='12pt'),
     tasks(2, [r"$0\ge0$, siempre: " + RS('R'), RS('(-inf,3)'), RS('(9/13,inf)', -1, 3), r"$-1>5$, nunca: " + RS('0')])),
 (2, r"Con la tarifa A, un móvil cuesta 40 € al mes. Con la tarifa B cuesta 15 € al mes más 0,50 € por cada GB. ¿A partir de cuántos GB es más cara la tarifa B?",
     r"$15+0,5x>40\Rightarrow x>50$: con " + R(r"\text{más de 50 GB}") + r" es más cara la B."),
]))

# =====================================================================
# 10. Inequacions de segon grau o superior
for e, s_ in [('x**2-9<0', '(-3,3)'), ('x**2-3*x-10>=0', '(-inf,-2]U[5,inf)'), ('x**2+4*x>0', '(-inf,-4)U(0,inf)'), ('-x**2+2*x+3>0', '(-1,3)'), ('x**2-4*x+4<=0', '[2,2]'), ('x**2+x+1>0', 'R'),
              ('x**3-x>0', '(-1,0)U(1,inf)'), ('(x-1)*(x+2)*(x-4)<=0', '(-inf,-2]U[1,4]'), ('x**3-2*x**2-3*x>=0', '[-1,0]U[3,inf)'), ('x*(x+3)<40', '(-8,5)')]:
    ineq(e, s_)
S.append(("Inecuaciones de segundo grado o superior", [
 (2, r"Resuelve y representa la solución:" + tasks(3, [r"$x^2-9<0$", r"$x^2-3x-10\ge0$", r"$x^2+4x>0$", r"$-x^2+2x+3>0$", r"$x^2-4x+4\le0$", r"$x^2+x+1>0$"])
     + recorda(r"Calcula las raíces, divide la recta en intervalos y estudia el signo en cada uno."),
     tasks(2, [RS('(-3,3)'), RS('(-inf,-2]U[5,inf)'), RS('(-inf,-4)U(0,inf)'), RS('(-1,3)'), r"Solo $x=2$: " + RS('[2,2]'), r"$\Delta<0$ y $a>0$, siempre positivo: " + RS('R')])),
 (3, r"Resuelve:" + tasks(3, [r"$x^3-x>0$", r"$(x-1)(x+2)(x-4)\le0$", r"$x^3-2x^2-3x\ge0$"]),
     tasks(2, [RS('(-1,0)U(1,inf)'), RS('(-inf,-2]U[1,4]'), r"$x(x+1)(x-3)\ge0$: " + RS('[-1,0]U[3,inf)')])),
 (2, r"Los lados de un rectángulo miden $x$ y $x+3$ cm. ¿Para qué valores de $x$ el área es menor que 40 cm$^2$?",
     r"$x(x+3)<40\Rightarrow x^2+3x-40<0\Rightarrow x\in(-8, 5)$. Como $x>0$: " + R(r"x\in(0, 5)") + "."),
]))

# =====================================================================
# 11. Problemes
sol('x*(x+1)=156', ['12', '-13']); sol('600/x-600/(x+2)=25', ['6', '-8']); sol('1/x+1/(x+5)=Rational(1,6)', ['10', '-3']); sol('x+sqrt(x)=42', ['36']); sol('x+1/x=Rational(26,5)', ['5', '1/5'])
ineq('x**2<3*x', '(0,3)'); ineq('x**3>x', '(-1,0)U(1,inf)'); sol('x**2+(17-x)**2=169', ['5', '12'])
t33 = math.log(1.2) / math.log(1.03); ck([round(t33, 2), math.ceil(t33)], [6.17, 7]); sol('500*2**(x/3)=16000', ['15'])
S.append(("Problemas", [
 (2, r"El producto de dos números naturales consecutivos es 156. ¿Cuáles son?",
     r"$x(x+1)=156\Rightarrow x^2+x-156=0\Rightarrow x=12$ ($x=-13$ no es natural). Son " + R(r"12\ \text{y}\ 13") + "."),
 (2, r"Un rectángulo tiene 34 cm de perímetro y 13 cm de diagonal. ¿Cuánto miden los lados?",
     r"$x+y=17$ y $x^2+y^2=169$: $x^2+(17-x)^2=169\Rightarrow x^2-17x+60=0\Rightarrow$ " + R(r"12\ \text{cm}\ \text{y}\ 5\ \text{cm}") + "."),
 (2, r"¿Cuántos años deben pasar para que 5000 € a un 3\,\% de interés compuesto anual se conviertan en 6000 €?",
     r"$5000\cdot1,03^t=6000\Rightarrow t=\dfrac{\log1,2}{\log1,03}\approx" + dec(t33, 2) + r"$: hacen falta " + R(r"7\ \text{años}") + "."),
 (2, r"Un grupo de amigos alquila un apartamento por 600 €. Si hubieran sido dos amigos más, cada uno habría pagado 25 € menos. ¿Cuántos amigos son?",
     r"$\dfrac{600}{x}-\dfrac{600}{x+2}=25\Rightarrow x^2+2x-48=0\Rightarrow x=6$ ($x=-8$ no tiene sentido): son " + R(r"6\ \text{amigos}") + "."),
 (3, r"Un grifo tarda 5 horas más que otro en llenar un depósito. Si los abrimos juntos, lo llenan en 6 horas. ¿Cuánto tarda cada uno por separado?",
     r"$\dfrac1x+\dfrac{1}{x+5}=\dfrac16\Rightarrow x^2-7x-30=0\Rightarrow x=10$ ($x=-3$ no tiene sentido): " + R(r"10\ \text{h y}\ 15\ \text{h}") + "."),
 (2, r"Si a un número positivo le sumamos su raíz cuadrada, obtenemos 42. ¿Cuál es el número?",
     r"$x+\sqrt x=42\Rightarrow\sqrt x=42-x\Rightarrow x^2-85x+1764=0\Rightarrow x=36,\ x=49$; $x=49$ no vale ($49+7\neq42$): " + R("36") + "."),
 (2, r"La suma de un número y su inverso es $\frac{26}{5}$. ¿Cuál es el número?",
     r"$x+\dfrac1x=\dfrac{26}{5}\Rightarrow5x^2-26x+5=0$: " + R(r"x=5\ \text{o}\ x=\frac15") + "."),
 (3, r"¿Para qué números su cuadrado es menor que su triple? ¿Y para cuáles su cubo es mayor que el propio número?",
     r"$x^2<3x\Rightarrow x(x-3)<0$: " + RS('(0,3)') + r" \quad $x^3>x\Rightarrow x(x-1)(x+1)>0$: " + RS('(-1,0)U(1,inf)')),
 (3, r"Una población de bacterias sigue la fórmula $N=500\cdot2^{t/3}$, con $t$ en horas. ¿Cuándo habrá 16\,000 bacterias?",
     r"$2^{t/3}=32=2^5\Rightarrow\frac t3=5\Rightarrow" + Rm(r"t=15\ \text{horas}") + "$."),
]))

build(HERE, 3, "Ecuaciones e inecuaciones", S,
      "ecuaciones de segundo grado, bicuadradas, Ruffini, factorizadas, fracciones algebraicas, radicales, exponenciales, logarítmicas, inecuaciones",
      r"Resuélvelos en el cuaderno mostrando todos los pasos. Comprueba siempre las soluciones de las ecuaciones con fracciones, con radicales y logarítmicas, y da las soluciones de las inecuaciones como intervalo y representadas en la recta.",
      r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar las ecuaciones y las inecuaciones con las herramientas interactivas de los apuntes de la unidad.", lang='es')
