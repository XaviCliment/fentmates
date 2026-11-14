# Versió en castellà de genera.py. Genera t2-fitxa-exercicis-es.tex i t2-fitxa-solucions-es.tex (4t ESO Matemàtiques B, Unitat 2: Polinomis i fraccions algebraiques)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Recull els exercicis de les fitxes del departament («Fitxa 2 (1a Av.): Polinomis 1» i «Polinomis 2», «Potències de binomis»,
# «Exercici 71 pàg. 68», «Simplificació», «Multiplicacions i divisions» i «Sumes i restes de fraccions algebraiques», i la
# «Fitxa: Fraccions algebraiques»), ordenats per temes com els apunts, i hi afig alguns exercicis propis (arrels, m.c.d. i
# m.c.m., problemes). Totes les solucions les calcula sympy: pt() i ML() escriuen polinomis, FT() fraccions simplificades i
# factoritzades, i fe() comprova les que s'escriuen a mà.
# Ús: python3 genera-es.py && pdflatex t2-fitxa-exercicis-es.tex (dues vegades) && pdflatex t2-fitxa-solucions-es.tex (dues vegades)
import os, sys
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

x, y, z, a, b, c, w, t, k, m = sp.symbols('x y z a b c w t k m')
LOC = {s.name: s for s in (x, y, z, a, b, c, w, t, k, m)}
def E(s): return sp.sympify(s, locals=LOC) if isinstance(s, str) else s
def pt(e):
    """polinomi en x, ordenat de major a menor grau, amb fraccions \\frac{}{}"""
    e = sp.expand(E(e))
    if e == 0: return '0'
    cs = sp.Poly(e, x).all_coeffs(); n = len(cs) - 1; out = ''
    for i, cc in enumerate(cs):
        cc = sp.Rational(cc); kk = n - i
        if cc == 0: continue
        s = '-' if cc < 0 else ('+' if out else '')
        aa = abs(cc); at = str(aa.p) if aa.q == 1 else r'\frac{%d}{%d}' % (aa.p, aa.q)
        if kk > 0 and aa == 1: at = ''
        out += s + at + ('' if kk == 0 else 'x' if kk == 1 else 'x^{%d}' % kk)
    return out
def ML(e): return sp.latex(sp.expand(E(e)), order='lex').replace(r'\cdot', '')
def FT(e):
    """fracció algebraica simplificada i factoritzada"""
    return sp.latex(sp.factor(sp.cancel(sp.together(E(e)))))
def FX(e): return sp.latex(sp.factor(E(e)))
def fe(a_, b_): assert sp.simplify(E(a_) - E(b_)) == 0, (a_, b_)
def dv(D, d): return sp.div(E(D), E(d), x)
def T(items, n=2): return tasks(n, items)

S = []

# =====================================================================
# 1. Polinomis i valor numèric (Polinomis 1, exercicis 1-5)
tb = [(r"P(x)=5x^4-3x^3+2x+10", "4", "10", "4", "Incompleto", "5"), (r"Q(x)=-5x^5-\frac32x^4-x^3+9x^2-6", "5", "-6", "5", "Incompleto", "-5"),
      (r"R(x)=4x^2+x+1", "2", "1", "3", "Completo", "4"), (r"S(x)=5x^2+2x^5+9x", "5", "0", "3", "Incompleto", "2"), (r"T(x)=3x-2", "1", "-2", "2", "Completo", "3"), (r"U(x)=x^3-4x^2+x+1", "3", "1", "4", "Completo", "1")]
def taula(sol):
    h = r'\begin{center}\renewcommand{\arraystretch}{1.45}\small\begin{tabular}{|l|C{1cm}|C{1.9cm}|C{1.5cm}|C{2cm}|C{1.7cm}|}\hline\rowcolor{soft}\textbf{Polinomio} & \textbf{Grado} & \textbf{Térm. indep.} & \textbf{N.\textsuperscript{o} términos} & \textbf{¿Completo?} & \textbf{Coef. princ.}\\\hline'
    for r in tb: h += '$%s$ & %s\\\\\\hline' % (r[0], ' & '.join(('$\\res{%s}$' % v if v[0] in '-0123456789' else '\\rest{%s}' % v) if sol else '' for v in r[1:]))
    return h + r'\end{tabular}\end{center}'
P2 = E('-3*x**4-2*x**3-x**2-1'); ck([int(P2.subs(x, 2)), int(P2.subs(x, -2))], [-69, -37])
P3 = ['6*x**3-x**2-3', '-3*x**4+2*x**3+7*x**2-x+5', '8', 'x**3-1']
v3 = [[int(E(p).subs(x, v)) for v in (3, -1, 0)] for p in P3]
k4 = sp.solve(E('x**4-2*x**2+5*x+k').subs(x, 2) - 6, k)[0]; a5 = sp.solve(E('-x**4-4*x**3+a*x+10').subs(x, -3) - 10, a)[0]
ck([int(k4), int(a5)], [-12, 9])
S.append(("Polinomios y valor numérico", [
 (1, r"Completa la tabla siguiente:" + taula(False), taula(True)),
 (1, r"Dado el polinomio $P(x)=-3x^4-2x^3-x^2-1$, calcula su valor numérico para $x=2$ y $x=-2$.",
     r"$P(2)=-48-16-4-1=" + Rm("-69") + r"$; \quad $P(-2)=-48+16-4-1=" + Rm("-37") + "$."),
 (1, r"Calcula el valor numérico de los polinomios siguientes para $x=3$, $x=-1$ y $x=0$:" + T([r"$P(x)=6x^3-x^2-3$", r"$Q(x)=-3x^4+2x^3+7x^2-x+5$", r"$R(x)=8$", r"$S(x)=x^3-1$"]),
     T([r"$%s,\ \ %s,\ \ %s$" % tuple(Rm(str(v)) for v in vs) for vs in v3])),
 (2, r"¿Qué valor debe tener $k$ para que el valor numérico del polinomio $P(x)=x^4-2x^2+5x+k$ para $x=2$ sea 6?",
     r"$P(2)=16-8+10+k=18+k=6\Rightarrow" + Rm("k=-12") + "$."),
 (2, r"¿Cuánto vale $a$ en el polinomio $P(x)=-x^4-4x^3+ax+10$, si sabemos que el valor numérico para $x=-3$ es 10?",
     r"$P(-3)=-81+108-3a+10=37-3a=10\Rightarrow" + Rm("a=9") + "$."),
]))

# =====================================================================
# 2. Operacions i identitats notables (Polinomis 1, exercicis 6, 9 i 10)
Pp, Qq, Rr = E('x**3+4*x**2-3*x+1'), E('2*x**3-x+3'), E('4*x**2-x')
o6 = [(Pp - 3 * Qq) * Rr, (Pp - Rr) * Qq]
i9 = ['(x+3)**2', '(5*x**2+7)**2', '(2*x-3)**2', '(2*x-5)*(2*x+5)', '(sqrt(2)*x-sqrt(50))**2', '(Rational(2,3)*x-Rational(3,2))**2']
c10 = ['3*x*(2*x-1)-(x-3)*(x+3)+(x-2)**2', '(2*x-1)**2+(x-1)*(3-x)-3*(x+5)**2', 'Rational(4,3)*(x-3)**2-Rational(1,3)*(3*x-1)*(3*x+1)-Rational(1,3)*(4*x**3+35)']
S.append(("Operaciones e identidades notables", [
 (2, r"Sean $P(x)=x^3+4x^2-3x+1$, $Q(x)=2x^3-x+3$ y $R(x)=4x^2-x$. Calcula:" + T([r"$[P(x)-3\cdot Q(x)]\cdot R(x)$", r"$[P(x)-R(x)]\cdot Q(x)$"]),
     T([r"$(" + pt(Pp - 3 * Qq) + r")(4x^2-x)=" + Rm(pt(o6[0])) + "$", r"$(" + pt(Pp - Rr) + r")(2x^3-x+3)=" + Rm(pt(o6[1])) + "$"], 1)),
 (1, r"Efectúa las operaciones siguientes aplicando las identidades notables:" + T([r"$(x+3)^2$", r"$(5x^2+7)^2$", r"$(2x-3)^2$", r"$(2x-5)\cdot(2x+5)$", r"$\left(\sqrt2x-\sqrt{50}\right)^2$", r"$\left(\frac23x-\frac32\right)^2$"], 3)
     + recorda(r"$(a\pm b)^2=a^2\pm2ab+b^2$ \quad y \quad $(a+b)(a-b)=a^2-b^2$."),
     T([R(pt(e)) for e in i9], 3)),
 (2, r"Calcula:" + T([r"$3x(2x-1)-(x-3)(x+3)+(x-2)^2$", r"$(2x-1)^2+(x-1)(3-x)-3(x+5)^2$", r"$\frac43(x-3)^2-\frac13(3x-1)(3x+1)-\frac13(4x^3+35)$"], 1),
     T([R(pt(e)) for e in c10], 1)),
]))

# =====================================================================
# 3. Binomi de Newton (Polinomis 1, exercici 8, i fitxa «Potències de binomis»)
n8 = ['(x+2)**3', '(x-1)**4', '(2*x+3)**3', '(2*x+1)**5', '(2*x-3)**3', '(-2+x)**6']
nb = ['(x**2+x)**3', '(2*x**4-y)**5', '(4*x**3+2)**4', '(x**6-3*y**2)**5', '(3*y**2+5*x)**3', '(-2*x**3+2*x)**4', '(-2*x**3-3*x)**6', '(x-2*y)**4']
nbT = [r"$(x^2+x)^3$", r"$(2x^4-y)^5$", r"$(4x^3+2)^4$", r"$(x^6-3y^2)^5$", r"$(3y^2+5x)^3$", r"$(-2x^3+2x)^4$", r"$(-2x^3-3x)^6$", r"$(x-2y)^4$"]
S.append(("Binomio de Newton", [
 (2, r"Calcula las potencias siguientes utilizando la fórmula del binomio de Newton:" + T([r"$(x+2)^3$", r"$(x-1)^4$", r"$(2x+3)^3$", r"$(2x+1)^5$", r"$(2x-3)^3$", r"$(-2+x)^6$"], 3)
     + recorda(r"$(a+b)^n=\binom n0a^n+\binom n1a^{n-1}b+\cdots+\binom nnb^n$; los coeficientes son una fila del triángulo de Tartaglia. Si hay una resta, los signos se alternan."),
     T([R(pt(e)) for e in n8], 1)),
 (3, r"Calcula las potencias siguientes:" + T(nbT, 4),
     T([R(ML(e)) for e in nb], 1) + r"(En f) y g) conviene sacar primero el signo: $(-2x^3-3x)^6=(2x^3+3x)^6$.)"),
]))

# =====================================================================
# 4. Divisió de polinomis i regla de Ruffini (Polinomis 1, exercici 11; Polinomis 2, exercicis 1 i 2)
d11 = [('3*x**4+2*x**3-7*x**2+5*x+12', 'x**2-2*x+1'), ('x**5-3*x**4+x**2+3*x-5', 'x**2+x+1'), ('4*x**5+3*x**3+7*x**2+6*x+8', 'x**2+1'),
       ('x**5-2*x**4+3*x**3-5*x**2+10*x-15', 'x**2-2*x+3'), ('18*x**6-3*x**4+2*x**3+x', 'x**2-2')]
r1 = [('x**3-6*x**2+11*x-5', 'x-3'), ('x**4+7*x**3+13*x**2-x-17', 'x+4'), ('x**7-9*x**6+19*x**5+12*x**4-3*x**3+19*x**2-37*x-37', 'x-5')]
r2 = [('2*x**3-5*x**2+3', 'x-2'), ('x**4-3*x**3+1', 'x+2'), ('x**4+1', 'x+1')]
def QR(L): return [r"$c(x)=" + Rm(pt(q)) + r",\quad r(x)=" + Rm(pt(r)) + "$" for q, r in (dv(D, d) for D, d in L)]
S.append(("División de polinomios y regla de Ruffini", [
 (2, r"Efectúa las divisiones de polinomios siguientes:" + T([r"$(3x^4+2x^3-7x^2+5x+12):(x^2-2x+1)$", r"$(x^5-3x^4+x^2+3x-5):(x^2+x+1)$", r"$(4x^5+3x^3+7x^2+6x+8):(x^2+1)$",
      r"$(x^5-2x^4+3x^3-5x^2+10x-15):(x^2-2x+3)$", r"$(18x^6-3x^4+2x^3+x):(x^2-2)$"], 1)
     + recorda(r"Deja vacío el lugar de los términos que faltan en el dividendo. Comprobación: $D(x)=d(x)\cdot c(x)+r(x)$."),
     T(QR(d11), 1)),
 (1, r"Haz las divisiones con la regla de Ruffini e indica el cociente y el resto:" + T([r"$(x^3-6x^2+11x-5):(x-3)$", r"$(x^4+7x^3+13x^2-x-17):(x+4)$", r"$(x^7-9x^6+19x^5+12x^4-3x^3+19x^2-37x-37):(x-5)$"], 1),
     T(QR(r1), 1)),
 (1, r"Determina el resto de las divisiones siguientes con la regla de Ruffini:" + T([r"$(2x^3-5x^2+3):(x-2)$", r"$(x^4-3x^3+1):(x+2)$", r"$(x^4+1):(x+1)$"], 3),
     T([R(pt(dv(D, d)[1])) for D, d in r2], 3)),
]))
for D, d in d11 + r1 + r2: q, r = dv(D, d); fe(E(d) * q + r, D)

# =====================================================================
# 5. Teorema del residu (Polinomis 2, exercicis 3-8)
m3 = sp.solve(E('x**3-m*x**2+5*x-2').subs(x, -1), m)[0]; k4b = sp.solve(E('2*x**4+k*x**3-7*x+6').subs(x, 2) + 8, k)[0]
v5 = E('3*x**4-x**2+2*x-5').subs(x, 2); P7 = E('6*x**5-19*x**4+4*x**3-8*x**2+17*x-6').subs(x, 3); P8 = E('2*x**6+12*x**5+11*x**4-25*x**3-19*x**2-2*x-23').subs(x, -4)
ck([int(m3), int(k4b), int(v5), int(P7), int(P8)], [-8, -4, 43, 0, 1])
S.append(("Valor numérico y teorema del resto", [
 (2, r"Calcula $m$ para que el polinomio $P(x)=x^3-mx^2+5x-2$ sea divisible por $(x+1)$.",
     r"Debe ser $P(-1)=0$: $-1-m-5-2=0\Rightarrow" + Rm("m=-8") + "$."),
 (2, r"El resto de la división $(2x^4+kx^3-7x+6):(x-2)$ es igual a $-8$. ¿Cuánto vale $k$?",
     r"$P(2)=32+8k-14+6=24+8k=-8\Rightarrow" + Rm("k=-4") + "$."),
 (1, r"Calcula el valor numérico de $P(x)=3x^4-x^2+2x-5$ para $x=2$. Hazlo de dos formas diferentes.",
     r"Sustituyendo: $48-4+4-5=" + Rm("43") + r"$. Con Ruffini, el resto de $P(x):(x-2)$ también es 43 (teorema del resto)."),
 (2, r"Mediante el teorema del resto, comprueba si es verdad o no que:" + T([r"$(x-1)$ es divisor de $x^{55}+1$", r"$(x+1)$ es divisor de $x^{55}+1$"]),
     T([r"$P(1)=2\neq0$: " + R(r"\text{no}"), r"$P(-1)=-1+1=0$: " + R(r"\text{sí}")])),
 (2, r"Mediante el teorema del resto, comprueba si $x=3$ es solución de la ecuación $6x^5-19x^4+4x^3-8x^2+17x-6=0$.",
     r"El resto de dividir entre $x-3$ es $P(3)=0$: " + R(r"\text{sí lo es}") + "."),
 (2, r"Mediante el teorema del resto, comprueba si $x=-4$ es solución de la ecuación $2x^6+12x^5+11x^4-25x^3-19x^2-2x-23=0$.",
     r"El resto de dividir entre $x+4$ es $P(-4)=1\neq0$: " + R(r"\text{no lo es}") + "."),
]))

# =====================================================================
# 6. Arrels d'un polinomi (propis)
for p, rts in [('x**3-6*x**2+11*x-6', [1, 2, 3]), ('x**3+2*x**2-x-2', [1, -1, -2]), ('x**4-10*x**2+9', [1, -1, 3, -3]), ('x**3-3*x**2-4*x+12', [2, -2, 3])]:
    assert sorted(sp.roots(E(p), x).keys()) == sorted(rts), p
assert [r for r in sp.roots(E('x**3+x**2-12'), x) if r.is_real] == [2]
S.append(("Raíces de un polinomio", [
 (2, r"Halla las raíces enteras de los polinomios siguientes:" + T([r"$x^3-6x^2+11x-6$", r"$x^3+2x^2-x-2$", r"$x^4-10x^2+9$", r"$x^3-3x^2-4x+12$"])
     + recorda(r"Las raíces enteras de un polinomio con coeficientes enteros son divisores del término independiente."),
     T([R(r"x=1,\ x=2,\ x=3"), R(r"x=1,\ x=-1,\ x=-2"), R(r"x=\pm1,\ x=\pm3"), R(r"x=2,\ x=-2,\ x=3")])),
 (2, r"Escribe los candidatos a raíz entera de $x^3+x^2-12$ y halla cuáles lo son.",
     r"Divisors de 12: $\pm1,\ \pm2,\ \pm3,\ \pm4,\ \pm6,\ \pm12$. Solo $P(2)=0$: la única raíz es " + R("x=2") + r" (el cociente $x^2+3x+6$ no tiene raíces reales)."),
 (2, r"Escribe un polinomio de grado 3 que tenga por raíces $1$, $-2$ y $3$, y uno de grado 2 con una raíz doble en $x=4$.",
     r"$(x-1)(x+2)(x-3)=" + Rm(pt('(x-1)*(x+2)*(x-3)')) + r"$; \ $(x-4)^2=" + Rm(pt('(x-4)**2')) + r"$ (o cualquier múltiplo)."),
]))

# =====================================================================
# 7. Factorització (Polinomis 1, exercici 7; Polinomis 2, exercici 9; exercici 71 pàg. 68)
f7 = [('5*x*y**2+10*y', r'5y(xy+2)'), ('12*x**3-4*x**2', r'4x^2(3x-1)'), ('6*b**2-24', r'6(b^2-4)=6(b+2)(b-2)'), ('4*a*b**2*c**4-28*a**2*b**3*c**5+42*a**5*b**6*c**3', r'2ab^2c^3(2c-14abc^2+21a^4b^4)'),
      ('24*z**2-12*z+12', r'12(2z^2-z+1)'), ('5*w**4*t**6+25*w**6*t**4', r'5w^4t^4(t^2+5w^2)')]
fe(f7[0][0], '5*y*(x*y+2)'); fe(f7[1][0], '4*x**2*(3*x-1)'); fe(f7[2][0], '6*(b+2)*(b-2)'); fe(f7[3][0], '2*a*b**2*c**3*(2*c-14*a*b*c**2+21*a**4*b**4)'); fe(f7[4][0], '12*(2*z**2-z+1)'); fe(f7[5][0], '5*w**4*t**4*(t**2+5*w**2)')
f9 = ['x**4-x**3-7*x**2+x+6', 'x**5+x**4-5*x**3-x**2+8*x-4', 'x**4+4*x**3-2*x**2-12*x+9', '2*x**5-6*x**4-19*x**3+24*x**2+32*x', 'x**3+3*x**2+5*x+6', '2*x**4-7*x**3+x**2+7*x-3']
f71 = ['x**3+2*x**2+2*x+1', 'x**3+4*x**2+6*x+4', 'x**3+x-2', 'x**3-x-6', 'x**4-29*x**2+100', 'x**4-24*x**2-25', 'x**4-3*x**3+4*x**2+3*x-5', 'x**4+2*x**3+x**2-8*x-20']
S.append(("Factorización", [
 (1, r"Saca factor común:" + T([r"$5xy^2+10y$", r"$12x^3-4x^2$", r"$6b^2-24$", r"$4ab^2c^4-28a^2b^3c^5+42a^5b^6c^3$", r"$24z^2-12z+12$", r"$5w^4t^6+25w^6t^4$"]),
     T([R(s_) for _, s_ in f7])),
 (2, r"Factoriza los polinomios siguientes:" + T([r"$x^4-x^3-7x^2+x+6$", r"$x^5+x^4-5x^3-x^2+8x-4$", r"$x^4+4x^3-2x^2-12x+9$", r"$2x^5-6x^4-19x^3+24x^2+32x$", r"$x^3+3x^2+5x+6$", r"$2x^4-7x^3+x^2+7x-3$"])
     + recorda(r"Saca factor común, busca raíces entre los divisores del término independiente con Ruffini y, cuando llegues a grado 2, resuelve la ecuación."),
     T([R(FX(e)) for e in f9])),
 (2, r"Halla la factorización de los polinomios siguientes. Si algún factor de grado 2 no tiene raíces reales, es irreducible:" + T([r"$x^3+2x^2+2x+1$", r"$x^3+4x^2+6x+4$", r"$x^3+x-2$", r"$x^3-x-6$", r"$x^4-29x^2+100$", r"$x^4-24x^2-25$", r"$x^4-3x^3+4x^2+3x-5$", r"$x^4+2x^3+x^2-8x-20$"]),
     T([R(FX(e)) for e in f71])),
]))

# =====================================================================
# 8. Divisibilitat. M.c.d. i m.c.m. (propis)
MM = [(['x**2-4', 'x**2+4*x+4'], '(x+2)**2*(x-2)'), (['x**2-x', 'x**2-1'], 'x*(x+1)*(x-1)'), (['x**3-x', 'x**2-2*x+1'], 'x*(x+1)*(x-1)**2'), (['x**3-2*x**2-x+2', 'x**2-3*x+2'], '(x-1)*(x+1)*(x-2)')]
for ps, l in MM: assert sp.simplify(sp.lcm(E(ps[0]), E(ps[1])) / E(l)).is_number
S.append(("Divisibilidad. M.c.d. y m.c.m.", [
 (1, r"Indica, sin hacer la división, si el primer polinomio es divisor del segundo:" + T([r"$x-1$ y $x^3-1$", r"$x+2$ y $x^2+4$", r"$x+1$ y $x^4-1$", r"$x-3$ y $x^2-9$"]),
     T([r"$1-1=0$: " + R(r"\text{sí}"), r"$4+4=8\neq0$: " + R(r"\text{no}"), r"$1-1=0$: " + R(r"\text{sí}"), r"$9-9=0$: " + R(r"\text{sí}")])),
 (2, r"Calcula el m.c.d. y el m.c.m. de:" + T([r"$x^2-4$ y $x^2+4x+4$", r"$x^2-x$ y $x^2-1$", r"$x^3-x$ y $x^2-2x+1$", r"$x^3-2x^2-x+2$ y $x^2-3x+2$"], 1)
     + recorda(r"Factoriza primero. M.c.d.: factores comunes con el menor exponente. M.c.m.: todos los factores con el mayor exponente."),
     T([r"m.c.d. $=" + Rm("x+2") + r"$, \ m.c.m. $=" + Rm("(x+2)^2(x-2)") + "$", r"m.c.d. $=" + Rm("x-1") + r"$, \ m.c.m. $=" + Rm("x(x+1)(x-1)") + "$",
        r"m.c.d. $=" + Rm("x-1") + r"$, \ m.c.m. $=" + Rm("x(x+1)(x-1)^2") + "$", r"m.c.d. $=" + Rm("(x-1)(x-2)") + r"$, \ m.c.m. $=" + Rm("(x-1)(x+1)(x-2)") + "$"], 1)),
]))

# =====================================================================
# 9. Simplificació de fraccions algebraiques (fitxa «Simplificació» i Fraccions algebraiques 1a-d, f)
sm = [(r"\dfrac{x^3+5x^2+8x+4}{x^2-4}", '(x**3+5*x**2+8*x+4)/(x**2-4)'), (r"\dfrac{x^3-1}{x^2-1}", '(x**3-1)/(x**2-1)'), (r"\dfrac{x^3-5x^2-9x+45}{x^3+x^2-21x-45}", '(x**3-5*x**2-9*x+45)/(x**3+x**2-21*x-45)'),
      (r"\dfrac{x^2+9}{x^4-81}", '(x**2+9)/(x**4-81)'), (r"\dfrac{x^5+x^4}{x^4-x^2}", '(x**5+x**4)/(x**4-x**2)'), (r"\dfrac{x^3+x}{x^4-x}", '(x**3+x)/(x**4-x)'),
      (r"\dfrac{x^2-14x+49}{x^2-49}", '(x**2-14*x+49)/(x**2-49)'), (r"\dfrac{x^3+3x}{x^2+3}", '(x**3+3*x)/(x**2+3)')]
sm2 = [(r"\dfrac{2x^3-5x^2-3x}{x^2-9}", '(2*x**3-5*x**2-3*x)/(x**2-9)'), (r"\dfrac{x^3-8}{x^2+2x+4}", '(x**3-8)/(x**2+2*x+4)'), (r"\dfrac{6x^2-7x-20}{2x^2-18}", '(6*x**2-7*x-20)/(2*x**2-18)'),
       (r"\dfrac{x^4-16}{x^3+4x^2-4x-16}", '(x**4-16)/(x**3+4*x**2-4*x-16)'), (r"\dfrac{x^4-1}{x^4-2x^3+2x^2-2x+1}", '(x**4-1)/(x**4-2*x**3+2*x**2-2*x+1)')]
S.append(("Simplificación de fracciones algebraicas", [
 (2, r"Simplifica las fracciones algebraicas siguientes:" + T(['$' + d + '$' for d, _ in sm], 4)
     + recorda(r"Factoriza el numerador y el denominador (factor común, identidades notables, Ruffini) y elimina los factores comunes."),
     T([R(FT(e)) for _, e in sm], 3)),
 (2, r"Simplifica:" + T(['$' + d + '$' for d, _ in sm2], 3),
     T([R(FT(e)) for _, e in sm2], 3)),
]))

# =====================================================================
# 10. Multiplicació i divisió (fitxa «Multiplicacions i divisions» i Fraccions algebraiques 1e)
md = [(r"\dfrac{x-6}{x^2+3x+2}\cdot\dfrac{x^2+2x}{x^2-36}", '(x-6)/(x**2+3*x+2)*(x**2+2*x)/(x**2-36)'),
      (r"\dfrac{x^2-3x+2}{x^4-9x^2}\cdot\dfrac{x^2-3x}{x-1}", '(x**2-3*x+2)/(x**4-9*x**2)*(x**2-3*x)/(x-1)'),
      (r"\dfrac{2x^2+8x}{x^2-10x+25}\cdot\dfrac{x^2-25}{2x}", '(2*x**2+8*x)/(x**2-10*x+25)*(x**2-25)/(2*x)'),
      (r"\dfrac{\ \frac{1}{x-1}\ }{\frac{2x}{x+2}}\cdot\dfrac{\ \frac{x-1}{x+2}\ }{\frac1x}", '(1/(x-1))/(2*x/(x+2))*((x-1)/(x+2))/(1/x)'),
      (r"\dfrac{x^3-5x^2}{x^3+3x^2-4x-12}:\dfrac{x-5}{x^3+4x^2+4x}", '((x**3-5*x**2)/(x**3+3*x**2-4*x-12))/((x-5)/(x**3+4*x**2+4*x))'),
      (r"\dfrac{x^2-3x-4}{x^3+x^2-x-1}:\dfrac{x^3-2x^2-7x-4}{x^2-1}", '((x**2-3*x-4)/(x**3+x**2-x-1))/((x**3-2*x**2-7*x-4)/(x**2-1))'),
      (r"\dfrac{x^3}{8x-8}:\dfrac{x^2}{x^2-x}", '(x**3/(8*x-8))/(x**2/(x**2-x))'),
      (r"\dfrac{\ \frac{x}{x-3}\ }{\frac{x+3}{x}}:\dfrac{\ \frac{1}{x+1}\ }{\frac{x^2-9}{x^3+x^2}}", '((x/(x-3))/((x+3)/x))/((1/(x+1))/((x**2-9)/(x**3+x**2)))'),
      (r"\dfrac{x^2-6x+5}{x^2+5x+6}\cdot\dfrac{2x^2-8}{x^2-x}:\dfrac{2x-10}{x^2+3x}", '(x**2-6*x+5)/(x**2+5*x+6)*(2*x**2-8)/(x**2-x)/((2*x-10)/(x**2+3*x))')]
S.append(("Multiplicación y división de fracciones algebraicas", [
 (2, r"Haz las multiplicaciones y divisiones siguientes y simplifica el resultado:" + T(['$' + d + '$' for d, _ in md], 2)
     + recorda(r"Factoriza antes de multiplicar: así verás qué factores se simplifican."),
     T([R(FT(e)) for _, e in md], 3)),
]))

# =====================================================================
# 11. Suma i resta (fitxa «Sumes i restes» i Fraccions algebraiques 1j, k, m, n)
sr = [(r"\dfrac{5x+1}{x-2}+\dfrac{x^2+x-3}{x-2}", '(5*x+1)/(x-2)+(x**2+x-3)/(x-2)'), (r"\dfrac{x^2-1}{3x+2}-\dfrac{3x^2-5x-10}{3x+2}", '(x**2-1)/(3*x+2)-(3*x**2-5*x-10)/(3*x+2)'),
      (r"\dfrac{1}{x^2-1}-\dfrac{2}{x^2-2x-3}", '1/(x**2-1)-2/(x**2-2*x-3)'), (r"\dfrac{1}{x-5}+\dfrac{1}{x+5}", '1/(x-5)+1/(x+5)'),
      (r"\dfrac{x-3}{x}+\dfrac{6}{x^2+2x}-\dfrac{x+1}{x+2}", '(x-3)/x+6/(x**2+2*x)-(x+1)/(x+2)'), (r"\dfrac{x+1}{x^3-1}-\dfrac{x-2}{x^2-1}", '(x+1)/(x**3-1)-(x-2)/(x**2-1)'),
      (r"\dfrac{x+1}{x-1}+\dfrac{x-1}{x+1}", '(x+1)/(x-1)+(x-1)/(x+1)'), (r"\dfrac{2x}{x^2-16}+\dfrac{x+1}{3x+12}", '2*x/(x**2-16)+(x+1)/(3*x+12)'),
      (r"\dfrac2x+\dfrac{5x}{x-3}-\dfrac{x-4}{x^2-9}", '2/x+5*x/(x-3)-(x-4)/(x**2-9)'), (r"\dfrac{x-2}{x^3-x}+\dfrac{x}{x^2-1}", '(x-2)/(x**3-x)+x/(x**2-1)')]
sr2 = [(r"\dfrac{2}{x-2}-\dfrac{6}{x^2-x-2}+\dfrac{1}{x+1}", '2/(x-2)-6/(x**2-x-2)+1/(x+1)'), (r"\dfrac{2x^2-x}{x+3}+\dfrac{2x}{x-3}+\dfrac{12}{x^2-9}", '(2*x**2-x)/(x+3)+2*x/(x-3)+12/(x**2-9)'),
       (r"\dfrac{x}{x+1}-\dfrac{16}{6}+\dfrac{x+1}{x}", 'x/(x+1)-Rational(16,6)+(x+1)/x'), (r"\dfrac{x+1}{x^2}-\dfrac{x}{x+1}-\dfrac{1}{x^3+x^2}", '(x+1)/x**2-x/(x+1)-1/(x**3+x**2)')]
S.append(("Suma y resta de fracciones algebraicas", [
 (2, r"Efectúa las sumas y restas siguientes de fracciones algebraicas:" + T(['$' + d + '$' for d, _ in sr], 2)
     + recorda(r"Factoriza los denominadores, calcula su m.c.m. y reduce a común denominador. Simplifica el resultado si se puede."),
     T([R(FT(e)) for _, e in sr], 2)),
 (3, r"Opera y simplifica:" + T(['$' + d + '$' for d, _ in sr2], 2),
     T([R(FT(e)) for _, e in sr2], 2)),
]))

# =====================================================================
# 12. Operacions combinades (Fraccions algebraiques 1g, h, i, l, o)
oc = [(r"\dfrac{a+b}{a-b}-\dfrac{a-b}{a+b}+\dfrac{a^2}{a^2-b^2}", '(a+b)/(a-b)-(a-b)/(a+b)+a**2/(a**2-b**2)'), (r"\left(1+\dfrac1x\right):\left(1+\dfrac1{x+1}\right):\dfrac{x+1}{x+2}", '((1+1/x)/(1+1/(x+1)))/((x+1)/(x+2))'),
      (r"(a^2-b^2):\left(\dfrac1a+\dfrac1b\right)", '(a**2-b**2)/(1/a+1/b)'), (r"\left(x-\dfrac{x^2}{x-y}\right):\left(y-\dfrac{y^2}{x+y}\right)", '(x-x**2/(x-y))/(y-y**2/(x+y))'),
      (r"\dfrac{3x+5}{x^2-4}+\dfrac{2}{2-x}+\dfrac{-x^2+4x-1}{x-2}:(x+2)", '(3*x+5)/(x**2-4)+2/(2-x)+((-x**2+4*x-1)/(x-2))/(x+2)')]
S.append(("Operaciones combinadas", [
 (3, r"Opera y simplifica:" + T(['$' + d + '$' for d, _ in oc], 1)
     + recorda(r"Respeta la jerarquía: primero los paréntesis, después los productos y cocientes (de izquierda a derecha) y al final las sumas y restas."),
     T([R(FT(e)) for _, e in oc], 2)),
]))

# =====================================================================
# 13. Problemes (propis)
fe('(x**2+5*x+6)/(x+3)', 'x+2'); fe('(x**3+6*x**2+8*x)/(x*(x+2))', 'x+4')
S.append(("Problemas", [
 (2, r"Un rectángulo tiene una base de $x+3$ cm y un área de $x^2+5x+6$ cm$^2$. Expresa su altura y su perímetro.",
     r"Altura: $(x^2+5x+6):(x+3)=" + Rm(r"x+2\ \text{cm}") + r"$. Perímetro: $2(x+3)+2(x+2)=" + Rm(r"4x+10\ \text{cm}") + "$."),
 (2, r"El volumen de una caja es $x^3+6x^2+8x$ cm$^3$ y la base es un rectángulo de lados $x$ y $x+2$. ¿Cuál es la altura?",
     r"$\dfrac{x(x+2)(x+4)}{x(x+2)}=" + Rm(r"x+4\ \text{cm}") + "$."),
]))

build(HERE, 2, "Polinomios y fracciones algebraicas", S,
      "polinomios, valor numérico, identidades notables, binomio de Newton, Ruffini, teorema del resto, factorización, m.c.d., m.c.m., fracciones algebraicas",
      r"Resuélvelos en el cuaderno mostrando todos los pasos. Ordena siempre los polinomios y, en las divisiones, deja el lugar de los términos que faltan. Factoriza antes de operar con fracciones y simplifica todos los resultados. Recoge los ejercicios de las fichas del departamento de la unidad.",
      r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar las divisiones, Ruffini, las raíces, las factorizaciones y las fracciones con las herramientas interactivas de los apuntes de la unidad.", lang='es')
