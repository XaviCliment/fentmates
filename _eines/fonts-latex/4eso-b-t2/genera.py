# Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (4t ESO Matemàtiques B, Unitat 2: Polinomis i fraccions algebraiques)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Les operacions, divisions, valors numèrics i residus es calculen ací amb sympy (pt() els escriu en LaTeX); les factoritzacions,
# m.c.d., m.c.m. i fraccions escrites a mà es comproven amb fe() (igualtat exacta amb sympy).
# Ús: python3 genera.py && pdflatex t2-fitxa-exercicis.tex (dues vegades) && pdflatex t2-fitxa-solucions.tex (dues vegades)
import os, sys
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

x = sp.symbols('x')
def E(s): return sp.sympify(s, locals={'x': x})
def pt(e):
    """polinomi en x, ordenat de major a menor grau, amb fraccions \\frac{}{}"""
    e = sp.expand(E(e) if isinstance(e, str) else e)
    if e == 0: return '0'
    cs = sp.Poly(e, x).all_coeffs(); n = len(cs) - 1; out = ''
    for i, c in enumerate(cs):
        c = sp.Rational(c); k = n - i
        if c == 0: continue
        s = '-' if c < 0 else ('+' if out else '')
        a = abs(c)
        at = (str(a.p) if a.q == 1 else r'\frac{%d}{%d}' % (a.p, a.q))
        if k > 0 and a == 1: at = ''
        out += s + at + ('' if k == 0 else 'x' if k == 1 else 'x^{%d}' % k)
    return out
def fe(a, b):
    """comprova que dues expressions són iguals (exactament)"""
    A, B = (E(a) if isinstance(a, str) else a), (E(b) if isinstance(b, str) else b)
    assert sp.simplify(A - B) == 0, (a, b)
def dv(D, d):
    q, r = sp.div(E(D), E(d), x)
    return q, r

S = []

# =====================================================================
# 1. Polinomis
S.append(("Polinomis", [
 (1, r"Ordena cada polinomi i indica'n el grau, el coeficient principal i el terme independent. És complet?" + tasks(2, [r"$3x^2-5+2x^4-x$", r"$7-x^3$", r"$x^5-2x^2+x^3-8x+1$", r"$-4x+6x^2-\frac12$"]),
     tasks(1, [r"$" + Rm(pt('3*x**2-5+2*x**4-x')) + r"$: grau 4, coeficient principal 2, terme independent $-5$. No és complet (falta $x^3$).",
               r"$" + Rm(pt('7-x**3')) + r"$: grau 3, coeficient principal $-1$, terme independent 7. No és complet.",
               r"$" + Rm(pt('x**5-2*x**2+x**3-8*x+1')) + r"$: grau 5, coeficient principal 1, terme independent 1. No és complet (falta $x^4$).",
               r"$" + Rm(pt('-4*x+6*x**2-Rational(1,2)')) + r"$: grau 2, coeficient principal 6, terme independent $-\frac12$. És complet."])),
 (1, r"Indica el coeficient, la part literal i el grau de cada monomi:" + tasks(4, [r"$-3x^4$", r"$\frac25xy^2$", r"$8$", r"$-a^3b^2$"]),
     tasks(2, [r"$-3$, \ $x^4$, \ " + R("4"), r"$\frac25$, \ $xy^2$, \ " + R("3"), r"$8$, \ cap, \ " + R("0"), r"$-1$, \ $a^3b^2$, \ " + R("5")])),
 (1, r"Redueix els termes semblants:" + tasks(3, [r"$3x^2-5x+7-x^2+2x-4$", r"$x^3-2x+4x^3+x^2-x$", r"$2x(x-3)-x^2$"]),
     tasks(3, [R(pt('3*x**2-5*x+7-x**2+2*x-4')), R(pt('x**3-2*x+4*x**3+x**2-x')), R(pt('2*x*(x-3)-x**2'))])),
]))

# =====================================================================
# 2. Operacions amb polinomis
P, Q, Rr = E('2*x**3-x**2+4'), E('x**2+3*x-1'), E('x-2')
ops = [P + Q, P - Q, Q * Rr, P * Rr, P - Q * Rr]
divs = [('x**3-2*x**2+3*x-1', 'x**2+1'), ('6*x**4-x**2+3*x', '2*x**2+1'), ('2*x**4+x**3-5*x+2', 'x**2-x+1'), ('x**4-1', 'x**2+1')]
dres = [dv(a, b) for a, b in divs]
rufs = [('x**3-4*x**2+x+6', 'x-2'), ('2*x**4-3*x**2+x-5', 'x+1'), ('x**5-32', 'x-2'), ('3*x**3+2*x**2-x', 'x+2')]
rres = [dv(a, b) for a, b in rufs]
fe('(x+2)*(2*x-3)', '2*x**2+x-6')
S.append(("Operacions amb polinomis", [
 (1, r"Donats $P(x)=2x^3-x^2+4$, $Q(x)=x^2+3x-1$ i $R(x)=x-2$, calcula:" + tasks(3, [r"$P+Q$", r"$P-Q$", r"$Q\cdot R$", r"$P\cdot R$", r"$P-Q\cdot R$"]),
     tasks(2, [R(pt(e)) for e in ops])),
 (1, r"Desenvolupa les identitats notables:" + tasks(3, [r"$(x+5)^2$", r"$(2x-3)^2$", r"$(3x+1)(3x-1)$", r"$(x^2-2)^2$", r"$\left(\frac x2+4\right)^2$", r"$(5-x)(5+x)$"]),
     tasks(3, [R(pt(e)) for e in ['(x+5)**2', '(2*x-3)**2', '(3*x+1)*(3*x-1)', '(x**2-2)**2', '(x/2+4)**2', '(5-x)*(5+x)']])),
 (2, r"Escriu com el quadrat d'un binomi o com un producte (identitats notables a l'inrevés):" + tasks(4, [r"$x^2+6x+9$", r"$4x^2-20x+25$", r"$x^2-49$", r"$9x^2-1$"]),
     tasks(4, [R("(x+3)^2"), R("(2x-5)^2"), R("(x+7)(x-7)"), R("(3x+1)(3x-1)")])),
 (2, r"Opera i simplifica:" + tasks(1, [r"$(x+2)^2-(x-2)^2$", r"$3(x-1)^2-(2x+3)(2x-3)$", r"$(2x-1)^2-2(x+1)(x-1)$"]),
     tasks(3, [R(pt(e)) for e in ['(x+2)**2-(x-2)**2', '3*(x-1)**2-(2*x+3)*(2*x-3)', '(2*x-1)**2-2*(x+1)*(x-1)']])),
 (2, r"Fes les divisions i indica'n el quocient i el residu:" + tasks(2, [r"$(x^3-2x^2+3x-1):(x^2+1)$", r"$(6x^4-x^2+3x):(2x^2+1)$", r"$(2x^4+x^3-5x+2):(x^2-x+1)$", r"$(x^4-1):(x^2+1)$"])
     + recorda(r"Deixa buit el lloc dels termes que falten al dividend. Comprova-ho: $D(x)=d(x)\cdot c(x)+r(x)$."),
     tasks(1, [r"$c(x)=" + Rm(pt(q)) + r",\quad r(x)=" + Rm(pt(r)) + "$" for q, r in dres])),
 (1, r"Fes les divisions aplicant la regla de Ruffini:" + tasks(2, [r"$(x^3-4x^2+x+6):(x-2)$", r"$(2x^4-3x^2+x-5):(x+1)$", r"$(x^5-32):(x-2)$", r"$(3x^3+2x^2-x):(x+2)$"]),
     tasks(1, [r"$c(x)=" + Rm(pt(q)) + r",\quad r=" + Rm(pt(r)) + "$" for q, r in rres])),
 (2, r"Calcula $a$ i $b$ perquè $(x+a)(2x-3)=2x^2+bx-6$.",
     r"$(x+a)(2x-3)=2x^2+(2a-3)x-3a$. Igualant coeficients: $-3a=-6\Rightarrow" + Rm("a=2") + r"$ \ i \ $b=2a-3\Rightarrow" + Rm("b=1") + "$."),
]))
for (a, b), (q, r) in zip(divs + rufs, dres + rres): fe(E(b) * q + r, a); assert sp.degree(r, x) < sp.degree(E(b), x)
fe('(x+3)**2', 'x**2+6*x+9'); fe('(2*x-5)**2', '4*x**2-20*x+25'); fe('(x+7)*(x-7)', 'x**2-49'); fe('(3*x+1)*(3*x-1)', '9*x**2-1')

# =====================================================================
# 3. Valor numèric i teorema del residu
P11 = E('x**3-3*x**2+2*x-1')
v11 = [P11.subs(x, a) for a in [0, 1, -1, 2, sp.Rational(1, 2)]]
res12 = [E(p).subs(x, a) for p, a in [('x**4-3*x**2+2', 1), ('x**5+2*x-3', -1), ('2*x**3-x+5', 2), ('x**10-1', -1)]]
ck([int(v) if v.q == 1 else v for v in res12], [0, -6, 19, 0])
K = sp.Symbol('k'); a_, b_ = sp.symbols('a b')
ks = [sp.solve((x**3 + K * x**2 - 5 * x + 6).subs(x, 3), K)[0], sp.solve((2 * x**3 - K * x + 4).subs(x, -2) - 8, K)[0], sp.solve((x**4 + K * x**2 - 4).subs(x, -2), K)[0]]
ck(ks, [-2, 10, -3])
ab = sp.solve([(x**3 + a_ * x**2 + b_ * x - 6).subs(x, 2), (x**3 + a_ * x**2 + b_ * x - 6).subs(x, -3)], [a_, b_])
ck((ab[a_], ab[b_]), (2, -5))
S.append(("Valor numèric i teorema del residu", [
 (1, r"Donat $P(x)=x^3-3x^2+2x-1$, calcula:" + tasks(5, [r"$P(0)$", r"$P(1)$", r"$P(-1)$", r"$P(2)$", r"$P\left(\frac12\right)$"]),
     tasks(5, [R(tn(F(int(v.p), int(v.q)))) for v in v11])),
 (2, r"Calcula, sense fer la divisió, el residu de:" + tasks(2, [r"$(x^4-3x^2+2):(x-1)$", r"$(x^5+2x-3):(x+1)$", r"$(2x^3-x+5):(x-2)$", r"$(x^{10}-1):(x+1)$"])
     + recorda(r"Teorema del residu: el residu de $P(x):(x-a)$ és $P(a)$."),
     tasks(2, [r"$P(1)=1-3+2=" + Rm("0") + "$", r"$P(-1)=-1-2-3=" + Rm("-6") + "$", r"$P(2)=16-2+5=" + Rm("19") + "$", r"$P(-1)=1-1=" + Rm("0") + "$"])),
 (2, r"Comprova que el residu de $(x^3-5x+3):(x-2)$ fet per Ruffini coincideix amb $P(2)$.",
     r"Ruffini amb 2: coeficients $1,\ 0,\ -5,\ 3$ $\to$ $1,\ 2,\ -1,\ 1$; el residu és " + R("1") + r". I $P(2)=8-10+3=1$. Coincideixen."),
 (2, r"Calcula el valor de $k$ en cada cas:" + tasks(1, [r"$x^3+kx^2-5x+6$ és divisible per $x-3$.", r"El residu de $(2x^3-kx+4):(x+2)$ és 8.", r"$x^4+kx^2-4$ és divisible per $x+2$."]),
     tasks(1, [r"$P(3)=27+9k-15+6=0\Rightarrow" + Rm("k=-2") + "$", r"$P(-2)=-16+2k+4=8\Rightarrow" + Rm("k=10") + "$", r"$P(-2)=16+4k-4=0\Rightarrow" + Rm("k=-3") + "$"])),
 (3, r"Troba $a$ i $b$ perquè $x^3+ax^2+bx-6$ siga divisible per $x-2$ i per $x+3$.",
     r"$P(2)=0$ i $P(-3)=0$: $\begin{cases}4a+2b=-2\\ 9a-3b=33\end{cases}\Rightarrow" + Rm("a=2,\ b=-5") + "$."),
]))
fe(E('x**3-5*x+3').subs(x, 2), 1)

# =====================================================================
# 4. Arrels d'un polinomi
for p, rts in [('x**3-6*x**2+11*x-6', [1, 2, 3]), ('x**3+2*x**2-x-2', [1, -1, -2]), ('x**4-10*x**2+9', [1, -1, 3, -3]), ('x**3-3*x**2-4*x+12', [2, -2, 3])]:
    assert sorted(sp.roots(E(p), x).keys()) == sorted(rts), p
assert [E('x**3-7*x+6').subs(x, a) for a in [1, 2, -1, -3]] == [0, 0, 12, 0]
assert [r for r in sp.roots(E('x**3+x**2-12'), x) if r.is_real] == [2]
fe('(x-1)*(x+2)*(x-3)', 'x**3-2*x**2-5*x+6')
S.append(("Arrels d'un polinomi", [
 (1, r"Comprova si els nombres $1$, $2$, $-1$ i $-3$ són arrels de $P(x)=x^3-7x+6$.",
     tasks(4, [r"$P(1)=0$: " + R(r"\text{sí}"), r"$P(2)=0$: " + R(r"\text{sí}"), r"$P(-1)=12$: " + R(r"\text{no}"), r"$P(-3)=0$: " + R(r"\text{sí}")])),
 (2, r"Troba les arrels enteres dels polinomis següents:" + tasks(2, [r"$x^3-6x^2+11x-6$", r"$x^3+2x^2-x-2$", r"$x^4-10x^2+9$", r"$x^3-3x^2-4x+12$"])
     + recorda(r"Les arrels enteres d'un polinomi amb coeficients enters són divisors del terme independent."),
     tasks(2, [R(r"x=1,\ x=2,\ x=3"), R(r"x=1,\ x=-1,\ x=-2"), R(r"x=\pm1,\ x=\pm3"), R(r"x=2,\ x=-2,\ x=3")])),
 (2, r"Escriu els candidats a arrel entera de $x^3+x^2-12$ i troba quins ho són.",
     r"Divisors de 12: $\pm1,\ \pm2,\ \pm3,\ \pm4,\ \pm6,\ \pm12$. Només $P(2)=8+4-12=0$: l'única arrel és " + R("x=2") + r" (el quocient $x^2+3x+6$ no té arrels reals)."),
 (2, r"Escriu un polinomi de grau 3 que tinga per arrels $1$, $-2$ i $3$. I un de grau 2 amb una arrel doble en $x=4$.",
     r"$(x-1)(x+2)(x-3)=" + Rm(pt('(x-1)*(x+2)*(x-3)')) + r"$; \ $(x-4)^2=" + Rm(pt('(x-4)**2')) + r"$ (o qualsevol múltiple)."),
]))

# =====================================================================
# 5. Factorització
F20 = [('3*x**2-12*x', '3*x*(x-4)'), ('x**3-9*x', 'x*(x+3)*(x-3)'), ('2*x**3+8*x**2+8*x', '2*x*(x+2)**2'), ('x**4-x**2', 'x**2*(x+1)*(x-1)'), ('5*x**2-5', '5*(x+1)*(x-1)')]
F21 = [('x**2-5*x+6', '(x-2)*(x-3)'), ('x**2+x-12', '(x+4)*(x-3)'), ('2*x**2-x-1', '(2*x+1)*(x-1)'), ('3*x**2+6*x-9', '3*(x+3)*(x-1)')]
F22 = [('x**3-2*x**2-5*x+6', '(x-1)*(x+2)*(x-3)'), ('x**3+x**2-5*x+3', '(x-1)**2*(x+3)'), ('x**4-x**3-7*x**2+x+6', '(x-1)*(x+1)*(x+2)*(x-3)'),
       ('x**3-3*x-2', '(x+1)**2*(x-2)'), ('x**4-5*x**2+4', '(x-1)*(x+1)*(x-2)*(x+2)'), ('x**3-x**2-x+1', '(x-1)**2*(x+1)')]
F23 = [('x**4-2*x**3-3*x**2', 'x**2*(x-3)*(x+1)'), ('2*x**4+x**3-5*x**2+2*x', 'x*(x-1)*(2*x-1)*(x+2)'), ('x**5-x', 'x*(x-1)*(x+1)*(x**2+1)'), ('x**4+x**3-x-1', '(x-1)*(x+1)*(x**2+x+1)')]
for a, b in F20 + F21 + F22 + F23: fe(a, b)
assert not sp.roots(E('x**2-4*x+5'), x, filter='R') and not sp.roots(E('x**2+x+1'), x, filter='R') and not sp.roots(E('x**2+1'), x, filter='R')
fe('x**2*(x-3)**3*(x+1)', 'x**2*(x-3)**3*(x+1)')
S.append(("Factorització de polinomis", [
 (1, r"Factoritza traient factor comú i fent servir les identitats notables:" + tasks(3, [r"$3x^2-12x$", r"$x^3-9x$", r"$2x^3+8x^2+8x$", r"$x^4-x^2$", r"$5x^2-5$"]),
     tasks(3, [R("3x(x-4)"), R("x(x+3)(x-3)"), R("2x(x+2)^2"), R("x^2(x+1)(x-1)"), R("5(x+1)(x-1)")])),
 (2, r"Factoritza resolent l'equació de segon grau:" + tasks(3, [r"$x^2-5x+6$", r"$x^2+x-12$", r"$2x^2-x-1$", r"$x^2-4x+5$", r"$3x^2+6x-9$"])
     + recorda(r"Si $x_1$ i $x_2$ són les solucions de $ax^2+bx+c=0$, aleshores $ax^2+bx+c=a(x-x_1)(x-x_2)$."),
     tasks(2, [R("(x-2)(x-3)"), R("(x+4)(x-3)"), R(r"2\left(x+\tfrac12\right)(x-1)=(2x+1)(x-1)"), r"Irreductible ($\Delta=-4<0$).", R("3(x+3)(x-1)")])),
 (2, r"Factoritza amb la regla de Ruffini:" + tasks(2, [r"$x^3-2x^2-5x+6$", r"$x^3+x^2-5x+3$", r"$x^4-x^3-7x^2+x+6$", r"$x^3-3x-2$", r"$x^4-5x^2+4$", r"$x^3-x^2-x+1$"]),
     tasks(2, [R("(x-1)(x+2)(x-3)"), R("(x-1)^2(x+3)"), R("(x-1)(x+1)(x+2)(x-3)"), R("(x+1)^2(x-2)"), R("(x-1)(x+1)(x-2)(x+2)"), R("(x-1)^2(x+1)")])),
 (3, r"Factoritza completament:" + tasks(2, [r"$x^4-2x^3-3x^2$", r"$2x^4+x^3-5x^2+2x$", r"$x^5-x$", r"$x^4+x^3-x-1$"]),
     tasks(2, [R("x^2(x-3)(x+1)"), R("x(x-1)(2x-1)(x+2)"), R("x(x-1)(x+1)(x^2+1)"), R("(x-1)(x+1)(x^2+x+1)")])),
 (1, r"Indica les arrels de $P(x)=x^2(x-3)^3(x+1)$ i la multiplicitat de cadascuna. Quin és el grau de $P$?",
     r"$x=0$ (" + R(r"\text{doble}") + r"), $x=3$ (" + R(r"\text{triple}") + r"), $x=-1$ (" + R(r"\text{simple}") + r"). Grau $2+3+1=" + Rm("6") + "$."),
]))

# =====================================================================
# 6. Divisibilitat. M.c.d. i m.c.m.
assert [sp.rem(E(p), E(d), x) == 0 for p, d in [('x**3-1', 'x-1'), ('x**2+4', 'x+2'), ('x**4-1', 'x+1'), ('x**2-9', 'x-3')]] == [True, False, True, True]
MM = [(['x**2-4', 'x**2+4*x+4'], 'x+2', '(x+2)**2*(x-2)'), (['x**2-x', 'x**2-1'], 'x-1', 'x*(x+1)*(x-1)'), (['x**3-x', 'x**2-2*x+1'], 'x-1', 'x*(x+1)*(x-1)**2'),
      (['2*x+4', 'x**2+2*x', '3*x'], '1', '6*x*(x+2)'), (['x**3-2*x**2-x+2', 'x**2-3*x+2'], '(x-1)*(x-2)', '(x-1)*(x+1)*(x-2)')]
for ps, g, l in MM:
    G = E(ps[0]); L = E(ps[0])
    for p in ps[1:]: G = sp.gcd(G, E(p)); L = sp.lcm(L, E(p))
    fe(sp.factor(G) / sp.LC(sp.Poly(G, x)) * sp.LC(sp.Poly(E(g), x)), g)
    assert sp.simplify(L / E(l)).is_number, (L, l)
S.append(("Divisibilitat. M.c.d. i m.c.m.", [
 (1, r"Indica, sense fer la divisió, si el primer polinomi és divisor del segon:" + tasks(2, [r"$x-1$ i $x^3-1$", r"$x+2$ i $x^2+4$", r"$x+1$ i $x^4-1$", r"$x-3$ i $x^2-9$"]),
     tasks(2, [r"$1-1=0$: " + R(r"\text{sí}"), r"$4+4=8\neq0$: " + R(r"\text{no}"), r"$1-1=0$: " + R(r"\text{sí}"), r"$9-9=0$: " + R(r"\text{sí}")])),
 (2, r"Calcula el m.c.d. i el m.c.m. de:" + tasks(1, [r"$x^2-4$ i $x^2+4x+4$", r"$x^2-x$ i $x^2-1$", r"$x^3-x$ i $x^2-2x+1$", r"$2x+4$, \ $x^2+2x$ i $3x$"])
     + recorda(r"Factoritza primer. M.c.d.: factors comuns amb el menor exponent. M.c.m.: tots els factors amb el major exponent."),
     tasks(1, [r"$(x+2)(x-2)$, \ $(x+2)^2$: \ m.c.d. $=" + Rm("x+2") + r"$, \ m.c.m. $=" + Rm("(x+2)^2(x-2)") + "$",
               r"$x(x-1)$, \ $(x+1)(x-1)$: \ m.c.d. $=" + Rm("x-1") + r"$, \ m.c.m. $=" + Rm("x(x+1)(x-1)") + "$",
               r"$x(x+1)(x-1)$, \ $(x-1)^2$: \ m.c.d. $=" + Rm("x-1") + r"$, \ m.c.m. $=" + Rm("x(x+1)(x-1)^2") + "$",
               r"$2(x+2)$, \ $x(x+2)$, \ $3x$: \ m.c.d. $=" + Rm("1") + r"$, \ m.c.m. $=" + Rm("6x(x+2)") + "$"])),
 (3, r"Factoritza $P(x)=x^3-2x^2-x+2$ i $Q(x)=x^2-3x+2$, i calcula'n el m.c.d. i el m.c.m.",
     r"$P(x)=(x-1)(x+1)(x-2)$, \ $Q(x)=(x-1)(x-2)$. \ m.c.d. $=" + Rm("(x-1)(x-2)") + r"$, \ m.c.m. $=" + Rm("(x-1)(x+1)(x-2)") + "$."),
]))
fe('x**3-2*x**2-x+2', '(x-1)*(x+1)*(x-2)'); fe('x**2-3*x+2', '(x-1)*(x-2)')

# =====================================================================
# 7. Fraccions algebraiques
SI = [('(x**2-9)/(x**2+3*x)', '(x-3)/x'), ('(x**2-4*x+4)/(x**2-4)', '(x-2)/(x+2)'), ('(2*x**2-2)/(4*x+4)', '(x-1)/2'), ('(x**3-x)/(x**2+x)', 'x-1'), ('(x**2-5*x+6)/(x**2-x-6)', '(x-2)/(x+2)')]
SU = [('2/x+3/x**2', '(2*x+3)/x**2'), ('1/(x+1)+1/(x-1)', '2*x/(x**2-1)'), ('x/(x-2)-2/(x+2)', '(x**2+4)/(x**2-4)'), ('3/(x**2-1)-1/(x+1)', '(4-x)/(x**2-1)'), ('1/(x**2+x)+2/x', '(2*x+3)/(x*(x+1))')]
PQ = [('(x**2-4)/(3*x)*(6*x**2)/(x+2)', '2*x*(x-2)'), ('(x+1)/(x**2-1)*(x-1)/x', '1/x'), ('((x**2-x)/(x+3))/(x/(x**2-9))', '(x-1)*(x-3)'), ('(2*x/(x**2-1))/(4*x**2/(x+1))', '1/(2*x*(x-1))')]
CO = [('(1+1/x)*(x/(x**2-1))', '1/(x-1)'), ('(x/(x-1)-1)/(1/(x**2-1))', 'x+1'), ('(1/x-1/(x+1))*(x**2+x)', '1'), ('(x+2)/(x-2)-(x-2)/(x+2)', '8*x/(x**2-4)')]
for a, b in SI + SU + PQ + CO: fe(a, b)
fe('(x+1)*(x**2-1)', '(x-1)*(x**2+2*x+1)'); assert sp.simplify(E('2*(x**2+1)') - E('x*(2*x+2)')) != 0
S.append(("Fraccions algebraiques", [
 (1, r"Indica per a quins valors de $x$ no tenen sentit les fraccions següents:" + tasks(4, [r"$\dfrac{3}{x-2}$", r"$\dfrac{x+1}{x^2-9}$", r"$\dfrac{x}{x^2+1}$", r"$\dfrac{5}{x^2-4x}$"]),
     tasks(4, [R("x=2"), R(r"x=\pm3"), r"Sempre en tenen.", R(r"x=0,\ x=4")])),
 (2, r"Simplifica les fraccions algebraiques:" + tasks(3, [r"$\dfrac{x^2-9}{x^2+3x}$", r"$\dfrac{x^2-4x+4}{x^2-4}$", r"$\dfrac{2x^2-2}{4x+4}$", r"$\dfrac{x^3-x}{x^2+x}$", r"$\dfrac{x^2-5x+6}{x^2-x-6}$"])
     + recorda(r"Només es poden simplificar factors: factoritza el numerador i el denominador."),
     tasks(3, [R(r"\dfrac{x-3}{x}"), R(r"\dfrac{x-2}{x+2}"), R(r"\dfrac{x-1}{2}"), R("x-1"), R(r"\dfrac{x-2}{x+2}")])),
 (2, r"Comprova si són equivalents:" + tasks(1, [r"$\dfrac{x+1}{x-1}$ \ i \ $\dfrac{x^2+2x+1}{x^2-1}$", r"$\dfrac{2}{x}$ \ i \ $\dfrac{2x+2}{x^2+1}$"]),
     tasks(1, [R(r"\text{Sí}") + r": $(x+1)(x^2-1)=(x-1)(x^2+2x+1)$ (o bé, simplificant la segona: $\frac{(x+1)^2}{(x+1)(x-1)}=\frac{x+1}{x-1}$).", R(r"\text{No}") + r": $2(x^2+1)\neq x(2x+2)$."])),
 (2, r"Calcula i simplifica:" + tasks(2, [r"$\dfrac2x+\dfrac3{x^2}$", r"$\dfrac{1}{x+1}+\dfrac{1}{x-1}$", r"$\dfrac{x}{x-2}-\dfrac{2}{x+2}$", r"$\dfrac{3}{x^2-1}-\dfrac{1}{x+1}$", r"$\dfrac{1}{x^2+x}+\dfrac{2}{x}$"]),
     tasks(2, [R(r"\dfrac{2x+3}{x^2}"), R(r"\dfrac{2x}{x^2-1}"), R(r"\dfrac{x^2+4}{x^2-4}"), R(r"\dfrac{4-x}{x^2-1}"), R(r"\dfrac{2x+3}{x(x+1)}")])),
 (2, r"Calcula i simplifica:" + tasks(2, [r"$\dfrac{x^2-4}{3x}\cdot\dfrac{6x^2}{x+2}$", r"$\dfrac{x+1}{x^2-1}\cdot\dfrac{x-1}{x}$", r"$\dfrac{x^2-x}{x+3}:\dfrac{x}{x^2-9}$", r"$\dfrac{2x}{x^2-1}:\dfrac{4x^2}{x+1}$"]),
     tasks(2, [R("2x(x-2)"), R(r"\dfrac1x"), R("(x-1)(x-3)"), R(r"\dfrac{1}{2x(x-1)}")])),
 (3, r"Fes les operacions combinades i simplifica:" + tasks(2, [r"$\left(1+\dfrac1x\right)\cdot\dfrac{x}{x^2-1}$", r"$\left(\dfrac{x}{x-1}-1\right):\dfrac{1}{x^2-1}$", r"$\left(\dfrac1x-\dfrac{1}{x+1}\right)\cdot(x^2+x)$", r"$\dfrac{x+2}{x-2}-\dfrac{x-2}{x+2}$"]),
     tasks(2, [R(r"\dfrac{1}{x-1}"), R("x+1"), R("1"), R(r"\dfrac{8x}{x^2-4}")])),
]))

# =====================================================================
# 8. Problemes
fe('(x**2+5*x+6)/(x+3)', 'x+2'); fe('2*(x+3)+2*(x+2)', '4*x+10'); fe('(x**3+6*x**2+8*x)/(x*(x+2))', 'x+4'); fe('x**3-x+5-(3*x**2-2*x+1)', 'x**3-3*x**2+x+4')
S.append(("Problemes", [
 (2, r"Un rectangle té una base de $x+3$ cm i una àrea de $x^2+5x+6$ cm$^2$. Expressa'n l'altura i el perímetre.",
     r"Altura: $(x^2+5x+6):(x+3)=" + Rm(r"x+2\ \text{cm}") + r"$. Perímetre: $2(x+3)+2(x+2)=" + Rm(r"4x+10\ \text{cm}") + "$."),
 (2, r"El volum d'una caixa és $x^3+6x^2+8x$ cm$^3$ i la base és un rectangle de costats $x$ i $x+2$. Quina és l'altura?",
     r"$\dfrac{x^3+6x^2+8x}{x(x+2)}=\dfrac{x(x+2)(x+4)}{x(x+2)}=" + Rm(r"x+4\ \text{cm}") + "$."),
 (1, r"Quin polinomi cal sumar a $3x^2-2x+1$ per a obtindre $x^3-x+5$?",
     r"$(x^3-x+5)-(3x^2-2x+1)=" + Rm(pt('x**3-3*x**2+x+4')) + "$."),
]))

build(HERE, 2, "Polinomis i fraccions algebraiques", S,
      "polinomis, operacions, Ruffini, valor numèric, teorema del residu, arrels, factorització, m.c.d., m.c.m., fraccions algebraiques",
      r"Resol-los al quadern mostrant tots els passos. Ordena sempre els polinomis i, en les divisions, deixa el lloc dels termes que falten. Simplifica tots els resultats.",
      r"Intenta resoldre cada exercici abans de mirar-ne la solució. Pots comprovar les divisions, Ruffini, les arrels, les factoritzacions i les fraccions amb les eines interactives dels apunts de la unitat.")
