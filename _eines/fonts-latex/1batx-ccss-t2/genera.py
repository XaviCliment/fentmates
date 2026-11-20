# Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (1r Batxillerat CCSS, Unitat 2: Àlgebra)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Bilingüe: T(valencià, castellà); genera-es.py l'executa amb FM_LANG=es i escriu els -es.tex.
# Parteix de la fitxa de la unitat 2 de 1r Batx MI (_eines/fonts-latex/1batx-mi-t2), sense inequacions (que a CCSS són a la
# unitat 3), amb les seccions dels apunts de CCSS i exercicis nous de polinomis, d'equacions de primer grau (parèntesis i
# denominadors) i de segon grau, i problemes de context (percentatges, IVA, interés compost).
# Les solucions de polinomis, fraccions i equacions polinòmiques i racionals es calculen ací amb sympy; les de radicals,
# logaritmes, exponencials i problemes s'escriuen a mà i CHK les comprova (numèricament o amb sympy).
# Ús: python3 genera.py && python3 genera-es.py, i pdflatex (dues vegades) dels quatre .tex
import os, re, math
import sympy as sp
from sympy import Rational as Q, sqrt
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va
x, y, a, b, k, m = sp.symbols('x y a b k m')
xr = sp.Symbol('x', real=True)

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def Ri(t): return R(t).strip('$')
def L(e):
    s = sp.latex(e, order='lex')
    return s.replace(r'\left(', '(').replace(r'\right)', ')').replace(r'\log{(', r'\log(').replace(r'\ln{(', r'\ln(')
def dec(v, n=3):
    s = ('%.' + str(n) + 'f') % float(v)
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    return s.replace('.', ',')
NOSOL = T(r'\text{no té solució}', r'\text{no tiene solución}')
NOVAL = T('no val', 'no vale')

CHK = []
def ck(cond, msg=''):
    CHK.append((bool(cond), msg)); return cond

# ---------- Ruffini ----------
def ruf(coefs_, a_):
    coefs_ = [sp.nsimplify(c) for c in coefs_]; a_ = sp.nsimplify(a_)
    res = [coefs_[0]]; prod = [None]
    for c in coefs_[1:]:
        mm = res[-1] * a_; prod.append(mm); res.append(c + mm)
    n = len(coefs_)
    cols = 'r|' + 'r' * (n - 1) + '|r'
    rows = [' & ' + ' & '.join(L(c) for c in coefs_), L(a_) + ' & ' + ' & '.join('' if p is None else L(p) for p in prod),
            r'\hline & ' + ' & '.join(L(r_) for r_ in res)]
    return r'{\def\arraystretch{1.5}\begin{array}{%s}%s\end{array}}' % (cols, r'\\'.join(rows)), res
def coefs(P): return sp.Poly(P, x).all_coeffs()
def solve_r(e): return sp.solveset(e, xr, domain=sp.S.Reals)
def solT(Sset):
    vals = sorted(list(Sset), key=float)
    return r',\ '.join('x=' + L(v) for v in vals) if vals else NOSOL
def rootsT(P):
    rr = sp.roots(sp.Poly(P, x), filter='R')
    items = sorted(rr.items(), key=lambda t: float(t[0]))
    return r',\ '.join('x=%s%s' % (L(r_), r'\ (\text{%s})' % {2: 'doble', 3: 'triple'}[mm] if mm > 1 else '') for r_, mm in items)

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Polinomis. Operacions
P0, Q0 = 2 * x ** 3 - x + 3, x ** 2 - 2 * x + 1
E0 = [P0 + Q0, P0 - 2 * Q0, P0 * Q0, Q0 ** 2]
E1 = [2 * (x - 2) ** 2 - 3 * (3 * x + 2) - 2 * (3 * x - 2) * (3 * x + 2), (3 * x + 2) ** 2 + 2 * (2 * x - 3) ** 2 - (x - 5) * (2 * x - 5),
      (2 * x ** 2 - 2 * x - 13) * (3 * x ** 2 - 2 * x) - 3 * x, (x ** 2 + 4) * (x ** 2 - 4) * (x - 2) + 2 * x * (x ** 3 - 10) * x,
      (Q(2, 3) * x - Q(3, 5)) * (Q(3, 2) * x ** 2 + Q(2, 5)) + Q(6, 25)]
r4a = sp.solve(sp.Poly(sp.expand((3 * x ** 2 - 5 * x + a) * (2 * x ** 2 + b * x) - (6 * x ** 4 - 19 * x ** 3 + 19 * x ** 2 - 6 * x)), x).coeffs(), [a, b], dict=True)
r4b = sp.solve(sp.Poly(sp.expand(2 * (x + 3) ** 2 - 3 * (x + a) - (2 * x ** 2 + b * x + 3)), x).coeffs(), [a, b], dict=True)
ck(r4a == [{a: 2, b: -3}] and r4b == [{a: 5, b: 9}], '4')
D5 = [(3 * x ** 3 + 2 * x ** 2 + x - 5, 3 * x ** 2 + 2), (3 * x ** 4 - 2 * x ** 2 - x + 4, x ** 2 + x + 2), (x ** 3 - 3 * x ** 2 - x + 6, 2 * x ** 3 - 2 * x + 3), (6 * x ** 4 - x ** 2 + 3 * x, 2 * x ** 2 + 1)]
def divsol(D, d):
    q, r = sp.div(D, d, x)
    ck(sp.expand(d * q + r - D) == 0)
    return r'$c(x)=' + Ri(L(q)) + r',\ \ r(x)=' + Ri(L(r)) + '$'
S.append((T("Polinomis. Operacions", "Polinomios. Operaciones"), [
 (1, T(r"Donats els polinomis $P(x)=2x^3-x+3$ i $Q(x)=x^2-2x+1$, calcula:", r"Dados los polinomios $P(x)=2x^3-x+3$ y $Q(x)=x^2-2x+1$, calcula:")
     + tasks(4, [r"$P(x)+Q(x)$", r"$P(x)-2Q(x)$", r"$P(x)\cdot Q(x)$", r"$\big(Q(x)\big)^2$"]),
     tasks(2, [R(L(sp.expand(e))) for e in E0])),
 (1, T(r"Simplifica les expressions polinòmiques següents:", r"Simplifica las expresiones polinómicas siguientes:") + tasks(1, [r"$2(x-2)^2-3(3x+2)-2(3x-2)(3x+2)$", r"$(3x+2)^2+2(2x-3)^2-(x-5)(2x-5)$", r"$(2x^2-2x-13)(3x^2-2x)-3x$",
      r"$(x^2+4)(x^2-4)(x-2)+2x(x^3-10)x$", r"$\left(\frac23x-\frac35\right)\left(\frac32x^2+\frac25\right)+\frac{6}{25}$"])
     + recorda(T(r"$(a\pm b)^2=a^2\pm2ab+b^2$, \ $(a+b)(a-b)=a^2-b^2$. Desenvolupa cada producte i redueix els termes semblants.",
                 r"$(a\pm b)^2=a^2\pm2ab+b^2$, \ $(a+b)(a-b)=a^2-b^2$. Desarrolla cada producto y reduce los términos semejantes.")),
     tasks(1, [R(L(sp.expand(e))) for e in E1])),
 (2, T(r"Calcula $(4x^2-3x+2)^2$. (Pots usar que $(a+b+c)^2=a^2+b^2+c^2+2ab+2ac+2bc$.)", r"Calcula $(4x^2-3x+2)^2$. (Puedes usar que $(a+b+c)^2=a^2+b^2+c^2+2ab+2ac+2bc$.)"),
     R(L(sp.expand((4 * x ** 2 - 3 * x + 2) ** 2)))),
 (2, T(r"Calcula els valors de $a$ i $b$ perquè es verifiquen les igualtats següents:", r"Calcula los valores de $a$ y $b$ para que se verifiquen las igualdades siguientes:")
     + tasks(1, [r"$(3x^2-5x+a)(2x^2+bx)=6x^4-19x^3+19x^2-6x$", r"$2(x+3)^2-3(x+a)=2x^2+bx+3$"]),
     tasks(1, [r"$6x^4+(3b-10)x^3+(2a-5b)x^2+abx$: \ $3b-10=-19$, $ab=-6\Rightarrow " + Ri("a=2,\\ b=-3") + "$",
               r"$2x^2+9x+18-3a$: \ $" + Ri("b=9") + r",\ \ 18-3a=3\Rightarrow " + Ri("a=5") + "$"])),
 (1, T(r"Efectua les divisions següents i indica'n el quocient i el residu:", r"Efectúa las divisiones siguientes e indica el cociente y el resto:")
     + tasks(1, [r"$(3x^3+2x^2+x-5):(3x^2+2)$", r"$(3x^4-2x^2-x+4):(x^2+x+2)$", r"$(x^3-3x^2-x+6):(2x^3-2x+3)$", r"$(6x^4-x^2+3x):(2x^2+1)$"])
     + recorda(T(r"Comprova-ho amb la prova de la divisió: $D(x)=d(x)\cdot c(x)+r(x)$, amb el grau de $r(x)$ menor que el de $d(x)$.",
                 r"Compruébalo con la prueba de la división: $D(x)=d(x)\cdot c(x)+r(x)$, con el grado de $r(x)$ menor que el de $d(x)$.")),
     tasks(1, [divsol(*d) for d in D5])),
]))

# =====================================================================
# 2. Regla de Ruffini. Teorema del residu
D6 = [(3 * x ** 3 + 2 * x ** 2 + x - 5, 1, -2), (3 * x ** 4 - 2 * x ** 2 - x + 4, 1, -2), (x ** 3 - 3 * x ** 2 - x + 6, 2, Q(-3, 2)), (4 * x ** 4 - 3 * x ** 2 + 5, -1, 5), (2 * x ** 5 - 12 * x ** 3 - 6 * x ** 2 - 117, 1, 3)]
def rufsol(D, lead, a_):
    Tb, res = ruf(coefs(D), a_)
    q, r = sp.div(D, lead * (x - a_), x)
    ck(r == res[-1] and sp.expand(sp.Poly(res[:-1], x).as_expr() / lead - q) == 0, 'ruf %s' % D)
    extra = '' if lead == 1 else (T(r'\ \ \text{(quocient de Ruffini dividit entre }%s)', r'\ \ \text{(cociente de Ruffini dividido entre }%s)') % L(lead))
    return r'$' + Tb + r'$\\[2pt]$c(x)=' + Ri(L(q)) + r',\ \ r=' + Ri(L(r)) + extra + '$'
P7 = [(2 * x ** 3 + 5 * x ** 2 - 2 * x + a, -3, a, 3), (2 * x ** 4 + 3 * x ** 3 - 2 * x ** 2 - a * x + 3, Q(-3, 2), a, 1),
      (-6 * x ** 4 + 11 * x ** 3 + a * x ** 2 + 5 * x + 4, Q(4, 3), a, -10), (4 * x ** 4 + 6 * x ** 3 - 13 * x ** 2 + x + b, 5, b, -2930)]
def s7(P, r_, var, val):
    ck(sp.solve(P.subs(x, r_), var) == [val], '7 %s' % P)
    return r'$P(%s)=%s=0\Rightarrow ' % (L(r_), L(sp.expand(P.subs(x, r_)))) + Ri('%s=%s' % (L(var), L(val))) + '$'
M8 = 2 * x ** 3 - 5 * x ** 2 + 4 * x - 4
ck(M8.subs(x, 2) == 0 and sp.div(M8, x - 2, x) == (2 * x ** 2 - x + 2, 0))
P9 = x ** 4 + 3 * x ** 3 - 2 * x ** 2 + 6 * x - 8
ck([P9.subs(x, v) for v in (1, 2, -1, -4, -3)] == [0, 36, -18, 0, -44])
def k13(P, r_, val):
    ck(sp.solve(P.subs(x, r_), k) == [val], '13 %s' % P)
    return r'$P(%s)=%s=0\Rightarrow ' % (L(r_), L(sp.expand(P.subs(x, r_)))) + Ri('k=' + L(val)) + '$'
P13 = [(x ** 3 + x ** 2 - 2 * x + k, 2, -8), (x ** 3 - 2 * x ** 2 + k * x + 4, -2, -6), ((k - 3) * x ** 3 - 15 * x + k, -4, 4), (x ** 3 - (k - 3) * x ** 2 + (k - 5) * x - 3, 3, 6)]
P14 = x ** 3 - (3 * k + 2) * x ** 2 - 3
ck(sp.solve(P14.subs(x, -3), k) == [Q(-16, 9)] and sp.solve(P14.subs(x, -3) - 15, k) == [Q(-7, 3)])
ck(sp.solve((2 * x ** 4 + 9 * x ** 3 + 2 * x ** 2 - 6 * x + 3 * m).subs(x, -2) - 12, m) == [Q(32, 3)])
ck((x ** 100 - 2 * x ** 51 + 1).subs(x, -1) == 4)
SI, NO = T(r"\rest{sí}", r"\rest{sí}"), r"\rest{no}"
S.append((T("Regla de Ruffini. Teorema del residu", "Regla de Ruffini. Teorema del resto"), [
 (1, T(r"Efectua les divisions següents aplicant la regla de Ruffini:", r"Efectúa las divisiones siguientes aplicando la regla de Ruffini:")
     + tasks(2, [r"$(3x^3+2x^2+x-5):(x+2)$", r"$(3x^4-2x^2-x+4):(x+2)$", r"$(x^3-3x^2-x+6):(2x+3)$", r"$(4x^4-3x^2+5):(-x+5)$", r"$(2x^5-12x^3-6x^2-117):(x-3)$"])
     + recorda(T(r"Si el divisor és $ax+b$, fes Ruffini amb $-\frac ba$ i divideix el quocient entre $a$; el residu no canvia.",
                 r"Si el divisor es $ax+b$, haz Ruffini con $-\frac ba$ y divide el cociente entre $a$; el resto no cambia.")),
     tasks(1, [rufsol(*d) for d in D6])),
 (1, T(r"Calcula el valor numèric del polinomi $P(x)=x^2-2x-3$ per a $x=-1$ i $x=3$. Podries trobar un altre valor de $x$ per al qual el valor del polinomi siga zero? Raona la resposta.",
       r"Calcula el valor numérico del polinomio $P(x)=x^2-2x-3$ para $x=-1$ y $x=3$. ¿Podrías encontrar otro valor de $x$ para el que el valor del polinomio sea cero? Razona la respuesta."),
     r"$P(-1)=1+2-3=" + Ri("0") + r"$, \ $P(3)=9-6-3=" + Ri("0") + r"$. \rest{No}" + T(r": un polinomi de grau 2 té com a màxim dues arrels, i ja les hem trobades: $P(x)=(x+1)(x-3)$.",
                                                                                     r": un polinomio de grado 2 tiene como máximo dos raíces, y ya las hemos encontrado: $P(x)=(x+1)(x-3)$.")),
 (1, T(r"Comprova si els nombres següents són arrels del polinomi $P(x)=x^4+3x^3-2x^2+6x-8$:", r"Comprueba si los números siguientes son raíces del polinomio $P(x)=x^4+3x^3-2x^2+6x-8$:")
     + tasks(5, ["$x=1$", "$x=2$", "$x=-1$", "$x=-4$", "$x=-3$"]),
     tasks(5, [r"$P(1)=0$: " + SI, r"$P(2)=36$: " + NO, r"$P(-1)=-18$: " + NO, r"$P(-4)=0$: " + SI, r"$P(-3)=-44$: " + NO])),
 (1, T(r"Comprova si $M(x)=2x^3-5x^2+4x-4$ és divisible per $x-2$ i, si ho és, troba un polinomi $N(x)$ que permeta escriure $M(x)=(x-2)\cdot N(x)$.",
       r"Comprueba si $M(x)=2x^3-5x^2+4x-4$ es divisible por $x-2$ y, si lo es, encuentra un polinomio $N(x)$ que permita escribir $M(x)=(x-2)\cdot N(x)$."),
     r"$M(2)=16-20+8-4=0$: " + T(r"\rest{sí que és divisible}.\par Per Ruffini: $", r"\rest{sí es divisible}.\par Por Ruffini: $") + ruf(coefs(M8), 2)[0] + r"\Rightarrow " + Ri("N(x)=2x^2-x+2") + "$"),
 (1, T(r"Calcula, sense fer la divisió, el residu de les divisions següents:", r"Calcula, sin hacer la división, el resto de las divisiones siguientes:")
     + tasks(2, [r"$(x^3-2x+5):(x+2)$", r"$(x^{100}-2x^{51}+1):(x+1)$", r"$(2x^4-3x^2+x-1):(x-1)$", r"$(x^5-32):(x-2)$"])
     + recorda(T(r"Teorema del residu: el residu de dividir $P(x)$ entre $x-a$ és $P(a)$.", r"Teorema del resto: el resto de dividir $P(x)$ entre $x-a$ es $P(a)$.")),
     tasks(2, [r"$P(-2)=-8+4+5=" + Ri("1") + "$", r"$P(-1)=1+2+1=" + Ri("4") + "$", r"$P(1)=2-3+1-1=" + Ri("-1") + "$", r"$P(2)=32-32=" + Ri("0") + T(r"$ (exacta)", r"$ (exacta)")])),
 (2, T(r"Calcula el valor de $k$ perquè el polinomi:", r"Calcula el valor de $k$ para que el polinomio:")
     + tasks(1, [T(r"$P(x)=x^3+x^2-2x+k$ siga divisible per $x-2$", r"$P(x)=x^3+x^2-2x+k$ sea divisible por $x-2$"), T(r"$P(x)=x^3-2x^2+kx+4$ siga divisible per $x+2$", r"$P(x)=x^3-2x^2+kx+4$ sea divisible por $x+2$"),
                 T(r"$P(x)=(k-3)x^3-15x+k$ siga divisible per $x+4$", r"$P(x)=(k-3)x^3-15x+k$ sea divisible por $x+4$"), T(r"$P(x)=x^3-(k-3)x^2+(k-5)x-3$ siga divisible per $x-3$", r"$P(x)=x^3-(k-3)x^2+(k-5)x-3$ sea divisible por $x-3$")]),
     tasks(1, [k13(*p) for p in P13])),
 (2, T(r"Utilitza Ruffini (o el teorema del residu) per a calcular el valor de $a$ i $b$ que fa que les divisions següents siguen exactes:",
       r"Utiliza Ruffini (o el teorema del resto) para calcular el valor de $a$ y $b$ que hace que las divisiones siguientes sean exactas:")
     + tasks(1, [r"$(2x^3+5x^2-2x+a):(x+3)$", r"$(2x^4+3x^3-2x^2-ax+3):(2x+3)$", r"$(-6x^4+11x^3+ax^2+5x+4):(-3x+4)$", r"$(4x^4+6x^3-13x^2+x+b):(-x+5)$"]),
     tasks(1, [s7(*p) for p in P7]) + T(r"($P(r)$ ha de ser 0, on $r$ és l'arrel del divisor; és el mateix que obtindre residu 0 a Ruffini.)",
                                        r"($P(r)$ tiene que ser 0, donde $r$ es la raíz del divisor; es lo mismo que obtener resto 0 en Ruffini.)")),
 (2, T(r"Calcula el valor de $k$ perquè la divisió de $x^3-(3k+2)x^2-3$ entre $(x+3)$:", r"Calcula el valor de $k$ para que la división de $x^3-(3k+2)x^2-3$ entre $(x+3)$:")
     + tasks(2, [T("Siga exacta.", "Sea exacta."), T("Tinga residu 15.", "Tenga resto 15.")]),
     r"$P(-3)=-27-9(3k+2)-3=-48-27k$." + tasks(2, [r"$-48-27k=0\Rightarrow " + Ri(r"k=-\frac{16}{9}") + "$", r"$-48-27k=15\Rightarrow " + Ri(r"k=-\frac73") + "$"])),
 (2, T(r"Troba el valor de $m$ perquè el polinomi $2x^4+9x^3+2x^2-6x+3m$ tinga residu 12 en dividir-lo per $x+2$, sense fer la divisió.",
       r"Halla el valor de $m$ para que el polinomio $2x^4+9x^3+2x^2-6x+3m$ tenga resto 12 al dividirlo por $x+2$, sin hacer la división."),
     T("Teorema del residu: ", "Teorema del resto: ") + r"$P(-2)=32-72+8+12+3m=-20+3m=12\Rightarrow " + Ri(r"m=\frac{32}{3}") + "$"),
]))
ck(sp.Poly(x ** 3 - 2 * x + 5).eval(-2) == 1 and sp.Poly(2 * x ** 4 - 3 * x ** 2 + x - 1).eval(1) == -1 and sp.Poly(x ** 5 - 32).eval(2) == 0)

# =====================================================================
# 3. Factorització de polinomis
P11 = [(x - 3) * (x + 5) * (x - 2), x * (x - 2) ** 3 * (2 * x + 1), (2 * x - 1) * (3 * x + 2) * (x + 1) ** 3, x ** 3 - 3 * x ** 2 - 6 * x + 8, x ** 3 + 8 * x ** 2 + 17 * x + 10, 2 * x ** 5 - 11 * x ** 4 + 21 * x ** 3 - 16 * x ** 2 + 4 * x]
P12 = [x ** 3 - 2 * x ** 2 - 5 * x + 6, x ** 3 + x ** 2 - 5 * x + 3, 2 * x ** 4 - x ** 3 - 5 * x ** 2 + x + 3, 4 * x ** 3 - 4 * x ** 2 - 11 * x + 6, x ** 4 - 4 * x ** 2,
       6 * x ** 5 + 11 * x ** 4 + 3 * x ** 3 - 3 * x ** 2 - x, x ** 6 - 4 * x ** 4 - x ** 2 + 4, 3 * x ** 2 - 12 * x + 12]
P12h = x ** 4 / 4 + Q(3, 4) * x ** 2 + Q(9, 16)
ck(sp.expand(P12h - (2 * x ** 2 + 3) ** 2 / 16) == 0 and sp.roots(sp.Poly(P12h, x), filter='R') == {})
A_, B_, C_ = sp.symbols('A B C')
ck(sp.solve([(A_ * x ** 2 + B_ * x + C_).subs(x, 1) + 6, C_ + 3, (A_ * x ** 2 + B_ * x + C_).subs(x, 3)], [A_, B_, C_]) == {A_: 2, B_: -5, C_: -3})
ck(sp.solve((m * x ** 3 - 6 * x ** 2 - 4 * x + 8).subs(x, 2), m) == [3])
ck(sp.solve([(x ** 3 + a * x ** 2 + b * x - 6).subs(x, 2), (x ** 3 + a * x ** 2 + b * x - 6).subs(x, -3)], [a, b]) == {a: 2, b: -5})
ck(sp.expand(x ** 3 + 2 * x ** 2 - 5 * x - 6 - (x - 2) * (x + 3) * (x + 1)) == 0)
P92 = sp.expand(2 * (x - 1) * (x + 2) * (x - 3)); ck(P92.subs(x, 0) == 12 and P92 == 2 * x ** 3 - 4 * x ** 2 - 10 * x + 12)
ARR = T("arrels", "raíces")
S.append((T("Factorització de polinomis", "Factorización de polinomios"), [
 (1, T(r"Determina les arrels dels polinomis següents:", r"Determina las raíces de los polinomios siguientes:")
     + tasks(2, [r"$(x-3)(x+5)(x-2)$", r"$x(x-2)^3(2x+1)$", r"$(2x-1)(3x+2)(x+1)^3$", r"$x^3-3x^2-6x+8$", r"$x^3+8x^2+17x+10$", r"$2x^5-11x^4+21x^3-16x^2+4x$"]),
     tasks(1, [R(rootsT(P11[i])) + ('' if i in (0, 1, 2) else r" \ $\big(" + L(sp.factor(P11[i])) + r"\big)$") for i in range(6)])),
 (2, T(r"Determina, si existeixen, les arrels enteres de cadascun dels polinomis següents i factoritza'ls:", r"Determina, si existen, las raíces enteras de cada uno de los polinomios siguientes y factorízalos:")
     + tasks(2, [r"$P(x)=x^3-2x^2-5x+6$", r"$P(x)=x^3+x^2-5x+3$", r"$P(x)=2x^4-x^3-5x^2+x+3$", r"$P(x)=4x^3-4x^2-11x+6$", r"$P(x)=x^4-4x^2$",
                 r"$P(x)=6x^5+11x^4+3x^3-3x^2-x$", r"$P(x)=x^6-4x^4-x^2+4$", r"$P(x)=3x^2-12x+12$",
                 r"$P(x)=\frac{x^4}{4}+\frac34x^2+\frac{9}{16}$ \ " + T("(comprova que no té arrels reals)", "(comprueba que no tiene raíces reales)")])
     + recorda(T(r"Primer, trau factor comú i busca identitats notables. Les arrels enteres són divisors del terme independent: prova-les amb Ruffini fins que quede un polinomi de grau 2.",
                 r"Primero, saca factor común y busca identidades notables. Las raíces enteras son divisores del término independiente: pruébalas con Ruffini hasta que quede un polinomio de grado 2.")),
     tasks(1, [R(L(sp.factor(P))) + r" \ \small(" + ARR + ": $" + rootsT(P) + "$)" for P in P12] +
           [r"$t=x^2$: $\frac{t^2}{4}+\frac34t+\frac9{16}=0\Rightarrow\Delta=\frac9{16}-\frac9{16}=0$, $t=-\frac32\lt0$: " + T(r"\rest{no té arrels reals}", r"\rest{no tiene raíces reales}") + ". $P(x)=" + Ri(r"\frac{1}{16}(2x^2+3)^2") + "$"])),
 (2, T(r"D'un polinomi de segon grau, $P(x)$, sabem que $P(1)=-6$, $P(0)=-3$ i que una de les seues arrels és 3. Determina'l i factoritza'l.",
       r"De un polinomio de segundo grado, $P(x)$, sabemos que $P(1)=-6$, $P(0)=-3$ y que una de sus raíces es 3. Determínalo y factorízalo."),
     r"$P(x)=ax^2+bx+c$: \ $c=-3$, \ $a+b-3=-6$, \ $9a+3b-3=0\Rightarrow a=2,\ b=-5$: \ " + R(r"P(x)=2x^2-5x-3=(x-3)(2x+1)")),
 (1, T(r"Troba el valor de $m$ perquè el polinomi $mx^3-6x^2-4x+8$ tinga 2 com a arrel. Factoritza'l després.", r"Halla el valor de $m$ para que el polinomio $mx^3-6x^2-4x+8$ tenga 2 como raíz. Factorízalo después."),
     r"$P(2)=8m-24-8+8=8m-24=0\Rightarrow " + Ri("m=3") + r"$; \ $3x^3-6x^2-4x+8=" + Ri(L(sp.factor(3 * x ** 3 - 6 * x ** 2 - 4 * x + 8))) + "$"),
 (2, T(r"Determina $a$ i $b$ de manera que el polinomi $x^3+ax^2+bx-6$ siga divisible per $x-2$ i per $x+3$.", r"Determina $a$ y $b$ de manera que el polinomio $x^3+ax^2+bx-6$ sea divisible por $x-2$ y por $x+3$."),
     r"$P(2)=0$: $4a+2b=-2$; \ $P(-3)=0$: $9a-3b=33$. \ " + R(r"a=2,\ b=-5") + T(r" \ (i aleshores $P(x)=(x-2)(x+3)(x+1)$).", r" \ (y entonces $P(x)=(x-2)(x+3)(x+1)$).")),
 (2, T(r"Troba el polinomi de grau 3 que té les arrels $1$, $-2$ i $3$ i que compleix $P(0)=12$.", r"Halla el polinomio de grado 3 que tiene las raíces $1$, $-2$ y $3$ y que cumple $P(0)=12$."),
     r"$P(x)=a(x-1)(x+2)(x-3)$; \ $P(0)=6a=12\Rightarrow a=2$: \ " + R(L(P92))),
]))
ck(sp.factor(3 * x ** 3 - 6 * x ** 2 - 4 * x + 8) == (x - 2) * (3 * x ** 2 - 4))

# =====================================================================
# 4. Fraccions algebraiques
F19 = [(2 * x ** 2 - 8, x ** 3 + x ** 2 - 2 * x), (x ** 3 - x, x ** 3 + 3 * x ** 2 + 2 * x), (x ** 4 - 2 * x ** 3 - 3 * x ** 2, x ** 4 - 9 * x ** 2), (x ** 3 - 3 * x ** 2 + 3 * x - 1, x ** 3 - 2 * x ** 2 + x),
       (2 * x ** 4 - 5 * x ** 3 + x ** 2 + 5 * x - 3, 2 * x ** 3 - x ** 2 - 7 * x + 6), (x ** 3 - 27, x ** 2 - 9),
       (x ** 3 - 2 * x ** 2 - 9 * x + 18, x ** 3 - 7 * x ** 2 + 16 * x - 12), (x ** 4 - 5 * x ** 3 + 9 * x ** 2 - 7 * x + 2, x ** 4 - 6 * x ** 3 + 13 * x ** 2 - 12 * x + 4)]
def simp(n, d): return r'$\dfrac{%s}{%s}=%s$' % (L(sp.factor(n)), L(sp.factor(d)), Ri(L(sp.factor(sp.cancel(n / d)))))
E20 = [1 / (x + 1) + 3 / (x ** 2 - 1), 1 / (x ** 2 + x) + 3 / (x + 1), 1 / (2 * x) - 3 / (4 * x ** 2 - 4 * x), 1 / (x ** 2 + x) + 3 / (x ** 2 - x),
       2 * x / (x - 2) + (3 * x - 1) / (x + 2) - 1 / (x ** 2 - 4), 1 / (x - 1) ** 2 + 2 / (x - 1) + 1 / (x ** 2 - 1)]
E21 = [(3 * x + 3) / (12 * x - 12) / ((x + 1) ** 2 / (x ** 2 - 1)), (x ** 2 + 2 * x - 3) / (x - 2) ** 3 * (x - 2) ** 2 / (x ** 2 - 1), (6 * x + 4) / (x - 2) * (4 * x + 1) / (2 * x + 4),
       -6 * x ** 2 / (x ** 2 + 2 * x + 1) * (x + 1) / (3 * x ** 3) * (x + 1) / (3 * x), (2 * x ** 2 - 7 * x + 6) / (x ** 2 + 2 * x + 1) * (x ** 2 + 6 * x + 5) / (2 * x - 3),
       (x ** 2 - 4) / (x ** 2 + x) / ((x - 2) / (x + 1))]
E22 = [(3 / x - 2 * x / (x + 1)) * ((x ** 2 + x) / (x - 1)), (x - 1) ** 2 / 2 * 1 / (x ** 2 - 1) - 3 * x / (x + 1) ** 2,
       ((2 * x - 1) / (x + 1) - 3 * x / (x - 1)) * ((x ** 3 - x) / (-x ** 2 - 6 * x + 1)), (x / (x - 1) - 1 / x) / ((x ** 2 - x + 1) / (x ** 2 - x)),
       (1 + (2 * x + 1) / (x - 1)) / (1 / (x - 1) + x / (x + 1)), 6 / (2 + x) - 4 / (2 - x) + 16 / (x ** 2 - 4), (1 - 1 / x) / (1 - 1 / x ** 2), 1 + 1 / (1 + 1 / (1 + 1 / x))]
def res(e): return R(L(sp.factor(sp.cancel(sp.together(e)))))
ck(sp.cancel((x / (x - 1) - 1 / x) / ((x ** 2 - x + 1) / (x ** 2 - x))) == 1)
S.append((T("Fraccions algebraiques", "Fracciones algebraicas"), [
 (2, T(r"Simplifica les fraccions algebraiques següents:", r"Simplifica las fracciones algebraicas siguientes:")
     + tasks(2, [r"$\dfrac{2x^2-8}{x^3+x^2-2x}$", r"$\dfrac{x^3-x}{x^3+3x^2+2x}$", r"$\dfrac{x^4-2x^3-3x^2}{x^4-9x^2}$", r"$\dfrac{x^3-3x^2+3x-1}{x^3-2x^2+x}$",
                 r"$\dfrac{2x^4-5x^3+x^2+5x-3}{2x^3-x^2-7x+6}$", r"$\dfrac{x^3-27}{x^2-9}$", r"$\dfrac{x^3-2x^2-9x+18}{x^3-7x^2+16x-12}$", r"$\dfrac{x^4-5x^3+9x^2-7x+2}{x^4-6x^3+13x^2-12x+4}$"])
     + recorda(T(r"Factoritza el numerador i el denominador i simplifica només els \emph{factors} comuns: $\dfrac{x+3}{x}\neq3$.",
                 r"Factoriza el numerador y el denominador y simplifica solo los \emph{factores} comunes: $\dfrac{x+3}{x}\neq3$.")),
     tasks(1, [simp(*f_) for f_ in F19])),
 (2, T(r"Efectua les sumes i restes següents reduint prèviament a comú denominador:", r"Efectúa las sumas y restas siguientes reduciendo previamente a común denominador:")
     + tasks(2, [r"$\dfrac{1}{x+1}+\dfrac{3}{x^2-1}$", r"$\dfrac{1}{x^2+x}+\dfrac{3}{x+1}$", r"$\dfrac{1}{2x}-\dfrac{3}{4x^2-4x}$",
                 r"$\dfrac{1}{x^2+x}+\dfrac{3}{x^2-x}$", r"$\dfrac{2x}{x-2}+\dfrac{3x-1}{x+2}-\dfrac{1}{x^2-4}$", r"$\dfrac{1}{(x-1)^2}+\dfrac{2}{x-1}+\dfrac{1}{x^2-1}$"])
     + recorda(T(r"Factoritza els denominadors: el comú denominador és el m.c.m. (factors comuns i no comuns amb el major exponent).",
                 r"Factoriza los denominadores: el común denominador es el m.c.m. (factores comunes y no comunes con el mayor exponente).")),
     tasks(2, [res(e_) for e_ in E20])),
 (2, T(r"Efectua els productes i quocients següents i simplifica el resultat:", r"Efectúa los productos y cocientes siguientes y simplifica el resultado:")
     + tasks(2, [r"$\dfrac{3x+3}{12x-12}:\dfrac{(x+1)^2}{x^2-1}$", r"$\dfrac{x^2+2x-3}{(x-2)^3}\cdot\dfrac{(x-2)^2}{x^2-1}$", r"$\dfrac{6x+4}{x-2}\cdot\dfrac{4x+1}{2x+4}$",
                 r"$\dfrac{-6x^2}{x^2+2x+1}\cdot\dfrac{x+1}{3x^3}\cdot\dfrac{x+1}{3x}$", r"$\dfrac{2x^2-7x+6}{x^2+2x+1}\cdot\dfrac{x^2+6x+5}{2x-3}$", r"$\dfrac{x^2-4}{x^2+x}:\dfrac{x-2}{x+1}$"])
     + recorda(T(r"Factoritza abans de multiplicar: així podràs simplificar sense desenvolupar els productes.", r"Factoriza antes de multiplicar: así podrás simplificar sin desarrollar los productos.")),
     tasks(2, [res(e_) for e_ in E21])),
 (3, T(r"Calcula i simplifica el resultat de les operacions combinades següents:", r"Calcula y simplifica el resultado de las operaciones combinadas siguientes:")
     + tasks(2, [r"$\left(\dfrac3x-\dfrac{2x}{x+1}\right)\cdot\dfrac{x^2+x}{x-1}$", r"$\dfrac{(x-1)^2}{2}\cdot\dfrac{1}{x^2-1}-\dfrac{3x}{(x+1)^2}$",
                 r"$\left(\dfrac{2x-1}{x+1}-\dfrac{3x}{x-1}\right)\cdot\dfrac{x^3-x}{-x^2-6x+1}$", r"$\left(\dfrac{x}{x-1}-\dfrac1x\right):\dfrac{x^2-x+1}{x^2-x}$",
                 r"$\dfrac{1+\frac{2x+1}{x-1}}{\frac{1}{x-1}+\frac{x}{x+1}}$", r"$\dfrac{6}{2+x}-\dfrac{4}{2-x}+\dfrac{16}{x^2-4}$", r"$\dfrac{1-\frac1x}{1-\frac1{x^2}}$", r"$1+\cfrac{1}{1+\cfrac{1}{1+\frac1x}}$"])
     + recorda(T(r"Primer els parèntesis (i els numeradors i denominadors de les fraccions compostes), després productes i quocients i, al final, sumes i restes.",
                 r"Primero los paréntesis (y los numeradores y denominadores de las fracciones compuestas), después productos y cocientes y, al final, sumas y restas.")),
     tasks(2, [res(e_) for e_ in E22])),
]))

# =====================================================================
# 5. Equacions polinòmiques
def lin1(lhs, rhs, M=1):
    """equació de primer grau: forma reduïda Ax=B i solució (o cap / identitat)"""
    e = sp.expand((lhs - rhs) * M)
    A, B = e.coeff(x, 1), -e.coeff(x, 0)
    ck(sp.degree(e, x) <= 1, 'lin %s' % e)
    pre = (r"m.c.m.$\,=%d$: \ " % M) if M > 1 else ''
    if A != 0:
        sol = B / A
        ck(sp.simplify((lhs - rhs).subs(x, sol)) == 0)
        return pre + r"$%s=%s$: \ " % (L(A * x), L(B)) + R('x=' + L(sol))
    if B != 0: return pre + r"$0\cdot x=%s$: \ " % L(B) + R(NOSOL)
    return pre + r"$0\cdot x=0$: " + T(r"\rest{identitat} (infinites solucions)", r"\rest{identidad} (infinitas soluciones)")
L1 = [(3 * (2 * x - 1) - 2 * (x + 4), 5 - (x - 2)), (2 * (x + 3) - 3 * (x - 1), 4 * (2 - x) + 1), (5 * x - 2 * (3 - x), 3 * (x + 2) - 4),
      (4 * (x - 1) - (2 * x + 3), 2 * (x - 3) + 1), (3 * (x + 2) - (x - 4), 2 * (x + 5)), (x - (2 * x - (3 - x)), 5)]
L2 = [((2 * x - 3) / 4 + x / 2 - (3 * x - 1) / 5, 2 * x - 1, 20), ((x + 3) / 4 - (2 * x - 1) / 6, x / 3 - 1, 12), ((x - 1) / 2 - (x + 2) / 3, 1, 6),
      (x / 2 - (x - 1) / 3, (x + 1) / 6 + 1, 6), (2 * (x + 1) / 3 - (x - 3) / 4, 1 + x / 12, 12), ((3 * x - 1) / 2 - 2 * (x + 1) / 5, x - (x - 2) / 10, 10)]
def quad(lhs, rhs=0, pre=''):
    e = sp.expand(lhs - rhs)
    p = sp.Poly(e, x)
    st_ = solve_r(e.subs(x, xr))
    rr = sp.roots(p, filter='R')
    txt = r"$%s=0$: \ " % L(e if p.LC() > 0 else -e) if pre is None else pre
    if not rr: return txt + T(r"$\Delta\lt0$: ", r"$\Delta\lt0$: ") + R(T(r"\text{no té solució real}", r"\text{no tiene solución real}"))
    if len(rr) == 1 and list(rr.values())[0] == 2: return txt + R('x=' + L(list(rr)[0]) + r'\ (\text{doble})')
    return txt + R(solT(st_))
Q3 = [(x ** 2 - 5 * x + 6, 0), (2 * x ** 2 + 3 * x - 2, 0), (3 * x ** 2 - 12, 0), (x ** 2 + 4 * x + 5, 0), (4 * x ** 2 - 4 * x + 1, 0), (5 * x ** 2 - 10 * x, 0),
      (2 * (3 * x - 2) + x * (x - 1), -4), ((x ** 2 + 1) / 2 - (2 * x - 3) / 4 + x ** 2 / 6, Q(59, 12)), ((x + 1) ** 3 - (x - 1) ** 3, 7), ((2 * x - 1) ** 2 - 3 * (x + 1), x * (x - 2))]
Q3pre = ['', '', '', '', '', '', None, T(r"Per 12: \ ", r"Por 12: \ ") + r"$6x^2+6-6x+9+2x^2=59\Rightarrow8x^2-6x-44=0\Rightarrow4x^2-3x-22=0$: \ ", r"$6x^2+2=7\Rightarrow x^2=\frac56$: \ ", None]
ck(sp.expand(12 * (Q3[7][0] - Q3[7][1])) == 8 * x ** 2 - 6 * x - 44)
E23 = [6 * x ** 4 + 13 * x ** 3 - 8 * x ** 2 - 17 * x + 6, 2 * x ** 4 - x ** 3 - 3 * x - 18, sp.Eq(6 * x ** 4 + 5 * x ** 3, 2 * x ** 2 + x), x ** 3 - 7 * x + 6, x ** 3 - 3 * x ** 2 - 9 * x + 27,
       x ** 4 - x ** 3 - 5 * x ** 2 - x - 6, x ** 4 - 1, x ** 4 + x ** 3 - 9 * x ** 2 - 9 * x]
def ex23(e):
    ex = (e.lhs - e.rhs) if isinstance(e, sp.Equality) else e
    return r'$' + L(sp.factor(ex)) + r'=0$: \ ' + R(solT(solve_r(ex.subs(x, xr))))
E24 = [x ** 4 - 17 * x ** 2 + 16, x ** 6 - 9 * x ** 3 + 8, x ** 4 - 8 * x ** 2 - 9, x ** 4 - 10 * x ** 2 + 9, 2 * (x + 1) ** 4 - 8 * x ** 3 - 8 * (x + 3) + 8, 4 * x ** 4 - 17 * x ** 2 + 4]
ck(sp.expand(E24[4]) == 2 * x ** 4 + 12 * x ** 2 - 14)
for e, sol in zip(E24, [{-4, -1, 1, 4}, {1, 2}, {-3, 3}, {-3, -1, 1, 3}, {-1, 1}, {-2, Q(-1, 2), Q(1, 2), 2}]):
    ck(set(solve_r(e.subs(x, xr))) == sol, '24 %s' % e)
E25 = [(x ** 2 - 3) * (x ** 2 - 4), (3 * x + 2) * (x ** 2 - 4 * x) * (x ** 2 - 9), (x ** 2 - 4 * x + 4) * (x ** 2 + 6 * x + 9), (x - 2) ** 2 * (x + 1) ** 3 * (2 * x - 7)]
S.append((T("Equacions polinòmiques", "Ecuaciones polinómicas"), [
 (1, T(r"Resol les equacions de primer grau següents:", r"Resuelve las ecuaciones de primer grado siguientes:")
     + tasks(2, [r"$3(2x-1)-2(x+4)=5-(x-2)$", r"$2(x+3)-3(x-1)=4(2-x)+1$", r"$5x-2(3-x)=3(x+2)-4$", r"$4(x-1)-(2x+3)=2(x-3)+1$", r"$3(x+2)-(x-4)=2(x+5)$", r"$x-\big[2x-(3-x)\big]=5$"])
     + recorda(T(r"Un signe $-$ davant d'un parèntesi canvia el signe de tots els termes de dins: \mbox{$-(x-2)=-x+2$}.", r"Un signo $-$ delante de un paréntesis cambia el signo de todos los términos de dentro: \mbox{$-(x-2)=-x+2$}.")),
     tasks(2, [lin1(*e) for e in L1])),
 (2, T(r"Resol les equacions de primer grau amb denominadors següents:", r"Resuelve las ecuaciones de primer grado con denominadores siguientes:")
     + tasks(2, [r"$\dfrac{2x-3}{4}+\dfrac x2-\dfrac{3x-1}{5}=2x-1$", r"$\dfrac{x+3}{4}-\dfrac{2x-1}{6}=\dfrac x3-1$", r"$\dfrac{x-1}{2}-\dfrac{x+2}{3}=1$",
                 r"$\dfrac x2-\dfrac{x-1}{3}=\dfrac{x+1}{6}+1$", r"$\dfrac{2(x+1)}{3}-\dfrac{x-3}{4}=1+\dfrac{x}{12}$", r"$\dfrac{3x-1}{2}-\dfrac{2(x+1)}{5}=x-\dfrac{x-2}{10}$"])
     + recorda(T(r"Multiplica tots els termes pel m.c.m. dels denominadors. Si davant d'una fracció hi ha un $-$, posa el numerador entre parèntesis.",
                 r"Multiplica todos los términos por el m.c.m. de los denominadores. Si delante de una fracción hay un $-$, pon el numerador entre paréntesis.")),
     tasks(1, [lin1(*e) for e in L2])),
 (1, T(r"Resol les equacions de segon grau següents:", r"Resuelve las ecuaciones de segundo grado siguientes:")
     + tasks(2, [r"$x^2-5x+6=0$", r"$2x^2+3x-2=0$", r"$3x^2-12=0$", r"$x^2+4x+5=0$", r"$4x^2-4x+1=0$", r"$5x^2-10x=0$",
                 r"$2(3x-2)+x(x-1)=-4$", r"$\dfrac{x^2+1}{2}-\dfrac{2x-3}{4}+\dfrac{x^2}{6}=\dfrac{59}{12}$", r"$(x+1)^3-(x-1)^3=7$", r"$(2x-1)^2-3(x+1)=x(x-2)$"])
     + recorda(T(r"$ax^2+bx+c=0\Rightarrow x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$. Les incompletes es resolen més ràpid: traent factor comú ($c=0$) o aïllant $x^2$ ($b=0$).",
                 r"$ax^2+bx+c=0\Rightarrow x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$. Las incompletas se resuelven más rápido: sacando factor común ($c=0$) o despejando $x^2$ ($b=0$).")),
     tasks(2, [quad(l_, r_, p_) for (l_, r_), p_ in zip(Q3, Q3pre)])),
 (2, T(r"Resol les equacions biquadrades següents (o que es resolen amb un canvi de variable):", r"Resuelve las ecuaciones bicuadradas siguientes (o que se resuelven con un cambio de variable):")
     + tasks(2, [r"$x^4-17x^2+16=0$", r"$x^6-9x^3+8=0$", r"$x^4-8x^2-9=0$", r"$\dfrac{9}{x^2}=10-x^2$", r"$2(x+1)^4-8x^3-8(x+3)+8=0$", r"$4x^4-17x^2+4=0$"]),
     tasks(1, [r"$t=x^2$: $t^2-17t+16=0\Rightarrow t=16,\ t=1$: \ " + R(r"x=\pm4,\ x=\pm1"), r"$t=x^3$: $t^2-9t+8=0\Rightarrow t=8,\ t=1$: \ " + R(r"x=2,\ x=1"),
               r"$t^2-8t-9=0\Rightarrow t=9$ ($t=-1$ " + T("no dona solucions", "no da soluciones") + r"): \ " + R(r"x=\pm3"),
               T(r"Multipliquem per $x^2$: ", r"Multiplicamos por $x^2$: ") + r"$x^4-10x^2+9=0\Rightarrow t=9,\ t=1$: \ " + R(r"x=\pm3,\ x=\pm1"),
               T("Desenvolupant: ", "Desarrollando: ") + r"$2x^4+12x^2-14=0\Rightarrow t^2+6t-7=0\Rightarrow t=1$ ($t=-7$ " + T("no dona solucions", "no da soluciones") + r"): \ " + R(r"x=\pm1"),
               r"$4t^2-17t+4=0\Rightarrow t=4,\ t=\frac14$: \ " + R(r"x=\pm2,\ x=\pm\frac12")])),
 (2, T(r"Resol les equacions polinòmiques de grau superior a 2 següents:", r"Resuelve las ecuaciones polinómicas de grado superior a 2 siguientes:")
     + tasks(2, [r"$6x^4+13x^3-8x^2-17x+6=0$", r"$2x^4-x^3-3x-18=0$", r"$6x^4+5x^3=2x^2+x$", r"$x^3-7x+6=0$", r"$x^3-3x^2-9x+27=0$", r"$x^4-x^3-5x^2-x-6=0$", r"$x^4-1=0$", r"$x^4+x^3-9x^2-9x=0$"])
     + recorda(T(r"Passa-ho tot a un membre i factoritza (factor comú, Ruffini…): un producte val zero si algun factor val zero.",
                 r"Pásalo todo a un miembro y factoriza (factor común, Ruffini…): un producto vale cero si algún factor vale cero.")),
     tasks(1, [ex23(e_) for e_ in E23])),
 (1, T(r"Resol les equacions factoritzades següents:", r"Resuelve las ecuaciones factorizadas siguientes:")
     + tasks(2, [r"$(x^2-3)(x^2-4)=0$", r"$(3x+2)(x^2-4x)(x^2-9)=0$", r"$(x^2-4x+4)(x^2+6x+9)=0$", r"$(x-2)^2(x+1)^3(2x-7)=0$"]),
     tasks(2, [R(solT(solve_r(e_.subs(x, xr)))) for e_ in E25])),
]))

# =====================================================================
# 6. Equacions amb radicals (comprovacions numèriques amb arrels reals)
def cbrt(v): return math.copysign(abs(v) ** (1 / 3), v)
def okf(f, vs, bad=()):
    for v in vs: ck(abs(f(float(v))) < 1e-9, 'ok %s' % v)
    for v in bad:
        try: r = f(float(v)); ck(abs(r) > 1e-6, 'bad %s' % v)
        except ValueError: pass
sq = math.sqrt
okf(lambda t: -sq(2 * t - 3) + 1 - t, [], [2])
okf(lambda t: t + sq(2 * t * t + 2 * t - 3) + 1, [-2], [2])
okf(lambda t: sq((7 * t + 1) / 4) - (5 * t - 7) / 6, [5], [8 / 25])
okf(lambda t: sq(2 * t - 1) / 4 - 3 / sq(2 * t - 1), [6.5])
okf(lambda t: sq(2 - 5 * t) + t * sq(3), [-2], [1 / 3])
okf(lambda t: sq(2 + sq(t - 4)) - sq(12 - t), [8], [13])
okf(lambda t: sq(t) + sq(t - 4) - 2, [4])
okf(lambda t: sq(t + 5) + sq(2 * t + 8) - 7, [4], [284])
okf(lambda t: sq(t + 4) + sq(t - 1) - 5, [5])
okf(lambda t: sq(1 - 4 * t) - 2 * sq(3 + t) - sq(3 + t), [-2])
okf(lambda t: sq(t + 3) - sq(t - 2) - 1, [6])
okf(lambda t: cbrt(t * t - 1) + 1 - t, [0, 1, 3])
okf(lambda t: cbrt(4 * t - 1) - (t - 4), [7])
okf(lambda t: sq(2 * t + 2) - (6 * t + 10) ** 0.25, [1])
okf(lambda t: sq(t + 1) - 2 * sq(t - 11), [15])
okf(lambda t: t - sq(t) - 6, [9], [4])
ck(sp.factor(x ** 3 - 12 * x ** 2 + 44 * x - 63) == (x - 7) * (x ** 2 - 5 * x + 9))
S.append((T("Equacions amb radicals", "Ecuaciones con radicales"), [
 (2, T(r"Resol les equacions amb radicals següents:", r"Resuelve las ecuaciones con radicales siguientes:")
     + tasks(2, [r"$x-\sqrt x=6$", r"$-\sqrt{2x-3}+1=x$", r"$x+\sqrt{2x^2+2x-3}=-1$", r"$\sqrt{\dfrac{7x+1}{4}}=\dfrac{5x-7}{6}$", r"$\dfrac{\sqrt{2x-1}}{4}=\dfrac{3}{\sqrt{2x-1}}$", r"$\sqrt{2-5x}+x\sqrt3=0$",
                 r"$\sqrt{2+\sqrt{x-4}}=\sqrt{12-x}$", r"$\sqrt x+\sqrt{x-4}=2$", r"$\sqrt{x+5}+\sqrt{2x+8}=7$", r"$\sqrt{x+4}+\sqrt{x-1}=5$", r"$\sqrt{x+3}-\sqrt{x-2}=1$", r"$\sqrt{1-4x}-2\sqrt{3+x}=\sqrt{3+x}$"])
     + recorda(T(r"Aïlla un radical, eleva al quadrat i repeteix-ho si cal. Comprova \emph{sempre} les solucions en l'equació inicial: en elevar al quadrat poden aparéixer solucions falses.",
                 r"Aísla un radical, eleva al cuadrado y repítelo si hace falta. Comprueba \emph{siempre} las soluciones en la ecuación inicial: al elevar al cuadrado pueden aparecer soluciones falsas.")),
     tasks(1, [r"$x-6=\sqrt x\Rightarrow x^2-13x+36=0\Rightarrow x=9,\ x=4$; \ $x=4$ " + NOVAL + r" ($4-2\neq6$): \ " + R("x=9"),
               r"$2x-3=(1-x)^2\Rightarrow(x-2)^2=0$; \ $x=2$: $-1+1=0\neq2$: \ " + R(NOSOL),
               r"$2x^2+2x-3=(x+1)^2\Rightarrow x^2=4$; \ $x=2$ " + NOVAL + r" ($-1-2\lt0$): \ " + R("x=-2"),
               r"$9(7x+1)=(5x-7)^2\Rightarrow25x^2-133x+40=0\Rightarrow x=5,\ x=\frac{8}{25}$; \ $x=\frac8{25}$ " + NOVAL + r": \ " + R("x=5"),
               r"$2x-1=12$: \ " + R(r"x=\frac{13}{2}"),
               r"$2-5x=3x^2\Rightarrow3x^2+5x-2=0\Rightarrow x=-2,\ x=\frac13$; \ $x=\frac13$ " + NOVAL + r": \ " + R("x=-2"),
               r"$2+\sqrt{x-4}=12-x\Rightarrow x-4=(10-x)^2\Rightarrow x^2-21x+104=0\Rightarrow x=8,\ x=13$; \ $x=13$ " + NOVAL + r": \ " + R("x=8"),
               r"$x=4-4\sqrt{x-4}+x-4\Rightarrow\sqrt{x-4}=0$: \ " + R("x=4"),
               r"$x-46=-14\sqrt{x+5}\Rightarrow x^2-288x+1136=0\Rightarrow x=4,\ x=284$; \ $x=284$ " + NOVAL + r": \ " + R("x=4"),
               r"$10\sqrt{x-1}=20\Rightarrow\sqrt{x-1}=2$: \ " + R("x=5"),
               r"$x+3=1+2\sqrt{x-2}+x-2\Rightarrow\sqrt{x-2}=2$: \ " + R("x=6") + r" \ ($3-2=1$ \checkmark)",
               r"$\sqrt{1-4x}=3\sqrt{3+x}\Rightarrow1-4x=27+9x$: \ " + R("x=-2")])),
 (3, T(r"Resol les equacions amb radicals no quadrats següents:", r"Resuelve las ecuaciones con radicales no cuadrados siguientes:")
     + tasks(3, [r"$\sqrt[3]{x^2-1}+1=x$", r"$\sqrt[3]{4x-1}=x-4$", r"$\sqrt{2x+2}-\sqrt[4]{6x+10}=0$"])
     + recorda(T(r"Eleva els dos membres a l'índex de l'arrel (o al m.c.m. dels índexs).", r"Eleva los dos miembros al índice de la raíz (o al m.c.m. de los índices).")),
     tasks(1, [r"$x^2-1=(x-1)^3\Rightarrow x(x-1)(x-3)=0$; " + T("totes valen", "todas valen") + r" ($\sqrt[3]{-1}=-1$): \ " + R(r"x=0,\ x=1,\ x=3"),
               r"$4x-1=(x-4)^3\Rightarrow(x-7)(x^2-5x+9)=0$: \ " + R("x=7"),
               r"$(2x+2)^2=6x+10\Rightarrow2x^2+x-3=0\Rightarrow x=1,\ x=-\frac32$; \ $x=-\frac32$ " + NOVAL + r": \ " + R("x=1")])),
 (2, T(r"Calcula un nombre tal que, si se li suma una unitat i després se n'extrau l'arrel quadrada, s'obté el doble que si se li resten 11 unitats i se n'extrau l'arrel quadrada.",
       r"Calcula un número tal que, si se le suma una unidad y después se extrae la raíz cuadrada, se obtiene el doble que si se le restan 11 unidades y se extrae la raíz cuadrada."),
     r"$\sqrt{x+1}=2\sqrt{x-11}\Rightarrow x+1=4x-44$: \ " + R("x=15") + T(r" \ (comprovació: $\sqrt{16}=4=2\sqrt4$).", r" \ (comprobación: $\sqrt{16}=4=2\sqrt4$).")),
]))

# =====================================================================
# 7. Equacions racionals
E26 = [sp.Eq(1 / x + 1 / x ** 2 + 1 / x ** 3, Q(7, 8)), sp.Eq(2 * x / 3 + (2 * x + 3) / (x - 1), 11 / (3 * x - 3)), sp.Eq(2 * x / (x - 2) + 3 * x / (x + 2), 6 * x ** 2 / (x ** 2 - 4)),
       sp.Eq(3 / (x ** 2 - 6 * x + 8) + (x - 5) / (x ** 2 - 5 * x + 4), 1 / (x - 4)), sp.Eq(x / sqrt(2) + sqrt(2) / x, sqrt(2) * x), sp.Eq(x / (x - 2) + 2 * x / (2 - x), -x),
       sp.Eq((1 + (x + 1) / (x - 1)) / (2 - (x - 1) / (x + 1)), 2), sp.Eq(x / (x + 1) + (x + 1) / x, Q(5, 2))]
X26 = [[2], [-1 + sqrt(2), -1 - sqrt(2)], [0], [5], [sqrt(2), -sqrt(2)], [0, 3], [3], [1, -2]]
for e, sols in zip(E26, X26):
    ck(set(solve_r((e.lhs - e.rhs).subs(x, xr))) == set(sols), '26 %s' % e)
ck(sp.simplify(1 / (1 - 1 / (x + 1)) - (x + 1) / x) == 0)
ck(set(solve_r((xr - 2) / (xr + 2) - 1 / (xr - 2) - (2 * xr - 6) / (xr ** 2 - 4) - 1)) == {Q(12, 7)})
S.append((T("Equacions racionals", "Ecuaciones racionales"), [
 (2, T(r"Resol les equacions racionals següents:", r"Resuelve las ecuaciones racionales siguientes:")
     + tasks(2, [r"$\dfrac1x+\dfrac1{x^2}+\dfrac1{x^3}=\dfrac78$", r"$\dfrac{2x}{3}+\dfrac{2x+3}{x-1}=\dfrac{11}{3x-3}$", r"$\dfrac{2x}{x-2}+\dfrac{3x}{x+2}=\dfrac{6x^2}{x^2-4}$",
                 r"$\dfrac{3}{x^2-6x+8}+\dfrac{x-5}{x^2-5x+4}=\dfrac{1}{x-4}$", r"$\dfrac{x}{\sqrt2}+\dfrac{\sqrt2}{x}=\sqrt2\,x$", r"$\dfrac{x}{x-2}+\dfrac{2x}{2-x}=-x$",
                 r"$\dfrac{x}{x+1}+\dfrac{x+1}{x}=\dfrac52$", r"$\dfrac{1+\frac{x+1}{x-1}}{2-\frac{x-1}{x+1}}=2$", r"$\dfrac{1}{1-\frac{1}{x+1}}=\dfrac{x+1}{x}$"])
     + recorda(T(r"Multiplica pel m.c.m. dels denominadors i, al final, descarta les solucions que anul·len algun denominador.",
                 r"Multiplica por el m.c.m. de los denominadores y, al final, descarta las soluciones que anulan algún denominador.")),
     tasks(1, [r"$8x^2+8x+8=7x^3\Rightarrow(x-2)(7x^2+6x+4)=0$ ($\Delta\lt0$): \ " + R("x=2"),
               T(r"Multipliquem per $3(x-1)$: ", r"Multiplicamos por $3(x-1)$: ") + r"$2x^2+4x+9=11\Rightarrow x^2+2x-1=0$: \ " + R(r"x=-1\pm\sqrt2"),
               r"$2x(x+2)+3x(x-2)=6x^2\Rightarrow x^2+2x=0\Rightarrow x=0,\ x=-2$; \ $x=-2$ " + T("anul·la un denominador", "anula un denominador") + r": \ " + R("x=0"),
               r"m.c.m. $=(x-1)(x-2)(x-4)$: $3(x-1)+(x-5)(x-2)=(x-1)(x-2)\Rightarrow x^2-4x+7=x^2-3x+2$: \ " + R("x=5"),
               T(r"Multipliquem per $\sqrt2\,x$: ", r"Multiplicamos por $\sqrt2\,x$: ") + r"$x^2+2=2x^2\Rightarrow$ " + R(r"x=\pm\sqrt2"),
               r"$-\dfrac{x}{x-2}=-x\Rightarrow x=x(x-2)\Rightarrow x^2-3x=0$: \ " + R(r"x=0,\ x=3"),
               r"$2x^2+2(x+1)^2=5x(x+1)\Rightarrow x^2+x-2=0$: \ " + R(r"x=1,\ x=-2") + T(r" (cap anul·la els denominadors)", r" (ninguna anula los denominadores)"),
               T("Simplificant: ", "Simplificando: ") + r"$\dfrac{2x(x+1)}{(x-1)(x+3)}=2\Rightarrow x^2+x=x^2+2x-3$: \ " + R("x=3"),
               T(r"El primer membre és $\dfrac{x+1}{x}$: és una \rest{identitat}, es compleix per a tot $x\neq0,\ x\neq-1$.", r"El primer miembro es $\dfrac{x+1}{x}$: es una \rest{identidad}, se cumple para todo $x\neq0,\ x\neq-1$.")])),
 (2, T(r"Resol $\dfrac{x-2}{x+2}-\dfrac{1}{x-2}=\dfrac{2x-6}{x^2-4}+1$.", r"Resuelve $\dfrac{x-2}{x+2}-\dfrac{1}{x-2}=\dfrac{2x-6}{x^2-4}+1$."),
     r"m.c.m. $=(x+2)(x-2)$: \ $(x-2)^2-(x+2)=2x-6+(x^2-4)\Rightarrow x^2-5x+2=x^2+2x-10\Rightarrow7x=12$, " + T("i en comprovar-ho:", "y al comprobarlo:")
     + r" $x=\frac{12}{7}$ " + T("sí que és vàlida", "sí es válida") + r": \ " + R(r"x=\frac{12}{7}")),
 (3, T(r"Un grup de persones lloga un autobús per 600\,€ a pagar a parts iguals; al final, 10 persones no poden anar al viatge i cadascuna de les que hi van ha de pagar 5\,€ més. Quantes persones hi anaven inicialment?",
       r"Un grupo de personas alquila un autobús por 600\,€ a pagar a partes iguales; al final, 10 personas no pueden ir al viaje y cada una de las que van tiene que pagar 5\,€ más. ¿Cuántas personas iban inicialmente?"),
     r"$\dfrac{600}{x-10}=\dfrac{600}{x}+5\Rightarrow x^2-10x-1200=0\Rightarrow x=40$ ($x=-30$ " + T("no té sentit", "no tiene sentido") + r"): \ " + R(T(r"40\ \text{persones}", r"40\ \text{personas}"))),
]))
xs = Q(12, 7)
ck(sp.simplify((xs - 2) / (xs + 2) - 1 / (xs - 2) - (2 * xs - 6) / (xs ** 2 - 4) - 1) == 0)
ck(sp.expand((x - 2) ** 2 - (x + 2) - (2 * x - 6 + x ** 2 - 4)) == -7 * x + 12)
ck(set(sp.solve(x ** 2 - 10 * x - 1200, x)) == {40, -30})

# =====================================================================
# 8. Equacions exponencials
okf(lambda t: 4 ** (t * t + 1) - 2 ** (5 * t + 5), [-0.5, 3])
okf(lambda t: 4 ** ((t - 2) ** 2) - 262144, [-1, 5])
okf(lambda t: 3 ** (t + 4) - 5, [math.log(5) / math.log(3) - 4])
okf(lambda t: 2 ** (-t) - 16 ** (t * (t - 1) / 2), [0, 0.5])
okf(lambda t: 13 ** (t * t + 2 * t) - 1 / 13, [-1])
okf(lambda t: 2 ** (2 * t * t - 4 * t - 2) - 16, [-1, 3])
okf(lambda t: 2 * 6 ** (4 * t - 3) - 24, [1 + math.log(2) / (4 * math.log(6))])
okf(lambda t: 3 * 2 ** t - 2 * 3 ** t, [1])
okf(lambda t: 27 ** (1 / t) - 3 ** (t + 2), [1, -3])
okf(lambda t: 2 ** (t + 4) - 8 ** t, [2])
okf(lambda t: 7 ** (t * t - 5 * t + 6) - 1, [2, 3])
okf(lambda t: 49 ** ((t - 5) / 3) - 1 / sq(7 ** (t - 1)), [23 / 7])
okf(lambda t: 2 ** (t + 1) + 2 ** t + 2 ** (t - 1) - 28, [3])
okf(lambda t: 5 ** (t + 3) - 5 ** (t - 1) - 3120, [2])
okf(lambda t: 4 ** t + 4 ** (t - 1) + 4 ** (t - 2) - 336, [4])
okf(lambda t: 3 ** (t + 2) + 3 ** (t + 1) + 3 ** t + 3 ** (t - 1) - 120, [2])
okf(lambda t: 2 ** (t - 1) + 2 ** (t - 2) + 2 ** (t - 3) + 2 ** (t - 4) - 960, [10])
okf(lambda t: 6 ** t - 9 * 6 ** (-t) + 8, [0])
okf(lambda t: 3 ** (2 * t) - 3 ** (t - 1) - 3 ** (t + 1) + 1, [-1, 1])
okf(lambda t: 2 * 10 ** (2 * t + 4) + 3 * 10 ** (t + 2) - 5, [-2])
okf(lambda t: 9 ** t + 5 * 3 ** t - 24, [1])
okf(lambda t: 3 ** (t + 2) + 9 ** (t - 1) - 90, [2])
okf(lambda t: 2 ** (2 * t - 4) - 5 * 2 ** (t - 3) + 1, [1, 3])
okf(lambda t: 4 ** (t + 1) + 2 ** (t + 3) - 320, [3])
okf(lambda t: 2 ** (2 * t + 1) - 5 * 2 ** t + 2, [1, -1])
for P_, rts in [(3 * x ** 2 - 10 * x + 3, {3, Q(1, 3)}), (x ** 2 + 81 * x - 810, {9, -90}), (2 * x ** 2 + 3 * x - 5, {1, Q(-5, 2)}), (x ** 2 - 10 * x + 16, {8, 2}), (x ** 2 + 5 * x - 24, {3, -8}),
                (x ** 2 + 2 * x - 80, {8, -10}), (x ** 2 + 8 * x - 9, {1, -9}), (2 * x ** 2 - 5 * x + 2, {2, Q(1, 2)})]:
    ck(set(sp.solve(P_, x)) == rts, 'exp %s' % P_)
NOVT = T(r"no val", r"no vale")
ck(abs(math.log(1.6) / math.log(1.04) - 11.98) < 0.01 and abs(math.log(2) / math.log(1.03) - 23.45) < 0.01)
ck(abs(math.log(1.2) / math.log(1.025) - 7.38) < 0.01)
S.append((T("Equacions exponencials", "Ecuaciones exponenciales"), [
 (2, T(r"Resol les equacions exponencials següents:", r"Resuelve las ecuaciones exponenciales siguientes:")
     + tasks(2, [r"$4^{x^2+1}=2^{5x+5}$", r"$4^{(x-2)^2}=262144$", r"$3^{x+4}=5$", r"$\dfrac{1}{2^x}=16^{\frac{x(x-1)}{2}}$", r"$13^{x^2+2x}-\dfrac1{13}=0$", r"$2^{2x^2-4x-2}=16$",
                 r"$2\cdot6^{4x-3}=24$", r"$3\cdot2^x=2\cdot3^x$", r"$\sqrt[x]{27}=3^{x+2}$", r"$2^{x+4}-8^x=0$", r"$7^{x^2-5x+6}=1$", r"$49^{\frac{x-5}{3}}=\dfrac{1}{\sqrt{7^{x-1}}}$"])
     + recorda(T(r"Si pots, escriu els dos membres amb la mateixa base i iguala els exponents; si no, pren logaritmes.", r"Si puedes, escribe los dos miembros con la misma base e iguala los exponentes; si no, toma logaritmos.")),
     tasks(1, [r"$2^{2x^2+2}=2^{5x+5}\Rightarrow2x^2-5x-3=0$: \ " + R(r"x=3,\ x=-\frac12"), r"$262144=4^9\Rightarrow(x-2)^2=9$: \ " + R(r"x=5,\ x=-1"),
               r"$x+4=\dfrac{\log5}{\log3}$: \ " + R(r"x=\frac{\log5}{\log3}-4\approx" + dec(math.log(5) / math.log(3) - 4)), r"$2^{-x}=2^{2x(x-1)}\Rightarrow2x^2-x=0$: \ " + R(r"x=0,\ x=\frac12"),
               r"$13^{x^2+2x}=13^{-1}\Rightarrow(x+1)^2=0$: \ " + R("x=-1"), r"$2x^2-4x-2=4\Rightarrow x^2-2x-3=0$: \ " + R(r"x=3,\ x=-1"),
               r"$6^{4x-3}=12\Rightarrow4x-3=\dfrac{\log12}{\log6}$: \ " + R(r"x=\frac{3+\log_612}{4}\approx" + dec(1 + math.log(2) / (4 * math.log(6)))), r"$\left(\dfrac32\right)^x=\dfrac32$: \ " + R("x=1"),
               r"$3^{3/x}=3^{x+2}\Rightarrow x^2+2x-3=0$: \ " + R(r"x=1,\ x=-3"), r"$2^{x+4}=2^{3x}\Rightarrow x+4=3x$: \ " + R("x=2"), r"$x^2-5x+6=0$: \ " + R(r"x=2,\ x=3"),
               r"$7^{\frac{2(x-5)}{3}}=7^{-\frac{x-1}{2}}\Rightarrow4(x-5)=-3(x-1)$: \ " + R(r"x=\frac{23}{7}")])),
 (2, T(r"Resol les equacions exponencials següents:", r"Resuelve las ecuaciones exponenciales siguientes:")
     + tasks(2, [r"$2^{x+1}+2^x+2^{x-1}=28$", r"$5^{x+3}-5^{x-1}-3120=0$", r"$4^x+4^{x-1}+4^{x-2}=336$", r"$3^{x+2}+3^{x+1}+3^x+3^{x-1}=120$", r"$2^{x-1}+2^{x-2}+2^{x-3}+2^{x-4}=960$", r"$6^x-9\cdot6^{-x}+8=0$"])
     + recorda(T(r"Descompon les potències ($a^{x+1}=a\cdot a^x$, $a^{x-1}=\frac{a^x}{a}$) i trau factor comú $a^x$.", r"Descompón las potencias ($a^{x+1}=a\cdot a^x$, $a^{x-1}=\frac{a^x}{a}$) y saca factor común $a^x$.")),
     tasks(1, [r"$2^x\left(2+1+\frac12\right)=28\Rightarrow2^x=8$: \ " + R("x=3"), r"$5^x\left(125-\frac15\right)=3120\Rightarrow5^x=25$: \ " + R("x=2"), r"$4^x\cdot\frac{21}{16}=336\Rightarrow4^x=256$: \ " + R("x=4"),
               r"$3^x\left(9+3+1+\frac13\right)=120\Rightarrow3^x=9$: \ " + R("x=2"), r"$2^x\cdot\frac{15}{16}=960\Rightarrow2^x=1024$: \ " + R("x=10"), r"$t=6^x$: $t^2+8t-9=0\Rightarrow t=1$ ($t=-9$ " + NOVT + r"): \ " + R("x=0")])),
 (3, T(r"Resol les equacions exponencials següents fent un canvi de variable:", r"Resuelve las ecuaciones exponenciales siguientes haciendo un cambio de variable:")
     + tasks(2, [r"$9^x+5\cdot3^x-24=0$", r"$2^{2x+1}-5\cdot2^x+2=0$", r"$3^{2x}-3^{x-1}=3^{x+1}-1$", r"$2\cdot10^{2x+4}+3\cdot10^{x+2}-5=0$", r"$3^{x+2}+9^{x-1}=90$", r"$2^{2x-4}-5\cdot2^{x-3}+1=0$", r"$4^{x+1}+2^{x+3}=320$"])
     + recorda(T(r"Si hi ha $a^{2x}$ i $a^x$, fes el canvi $t=a^x$; les solucions $t\le0$ no valen.", r"Si hay $a^{2x}$ y $a^x$, haz el cambio $t=a^x$; las soluciones $t\le0$ no valen.")),
     tasks(1, [r"$t=3^x$: $t^2+5t-24=0\Rightarrow t=3$ ($t=-8$ " + NOVT + r"): \ " + R("x=1"),
               r"$t=2^x$: $2t^2-5t+2=0\Rightarrow t=2,\ t=\frac12$: \ " + R(r"x=1,\ x=-1"),
               r"$t=3^x$: $3t^2-10t+3=0\Rightarrow t=3,\ t=\frac13$: \ " + R(r"x=1,\ x=-1"),
               r"$t=10^{x+2}$: $2t^2+3t-5=0\Rightarrow t=1$ ($t=-\frac52$ " + NOVT + r") $\Rightarrow x+2=0$: \ " + R("x=-2"),
               r"$t=3^x$: $9t+\frac{t^2}{9}=90\Rightarrow t^2+81t-810=0\Rightarrow t=9$ ($t=-90$ " + NOVT + r"): \ " + R("x=2"),
               r"$t=2^x$: $\frac{t^2}{16}-\frac{5t}{8}+1=0\Rightarrow t^2-10t+16=0\Rightarrow t=8,\ t=2$: \ " + R(r"x=3,\ x=1"),
               r"$t=2^x$: $4t^2+8t-320=0\Rightarrow t^2+2t-80=0\Rightarrow t=8$ ($t=-10$ " + NOVT + r"): \ " + R("x=3")])),
 (2, T(r"Ingressem 5000\,€ en un compte al 4\,\% d'interés compost anual. Quants anys complets han de passar perquè hi haja almenys 8000\,€?",
       r"Ingresamos 5000\,€ en una cuenta al 4\,\% de interés compuesto anual. ¿Cuántos años completos tienen que pasar para que haya al menos 8000\,€?"),
     r"$5000\cdot1,04^t=8000\Rightarrow1,04^t=1,6\Rightarrow t=\dfrac{\log1,6}{\log1,04}\approx11,98$: \ " + R(T(r"12\ \text{anys}", r"12\ \text{años}"))),
 (2, T(r"Quant de temps tarda a duplicar-se un capital col·locat al 3\,\% d'interés compost anual? I si l'interés és del 2,5\,\%, quant tarda a augmentar un 20\,\%?",
       r"¿Cuánto tiempo tarda en duplicarse un capital colocado al 3\,\% de interés compuesto anual? ¿Y si el interés es del 2,5\,\%, cuánto tarda en aumentar un 20\,\%?"),
     tasks(1, [r"$C\cdot1,03^t=2C\Rightarrow t=\dfrac{\log2}{\log1,03}\approx23,45$: \ " + R(T(r"24\ \text{anys}", r"24\ \text{años}")),
               r"$1,025^t=1,2\Rightarrow t=\dfrac{\log1,2}{\log1,025}\approx7,38$: \ " + R(T(r"8\ \text{anys}", r"8\ \text{años}"))])),
]))

# =====================================================================
# 9. Equacions logarítmiques
lg = math.log10
okf(lambda t: lg(2) + lg(t + 3) - lg(t + 5), [-1])
okf(lambda t: lg(15 - 2 * t) - 2 * lg(t), [3])
okf(lambda t: lg(2 * t + 3) - lg(t - 1) - 2 * lg(2) - 2 * lg(3), [39 / 34])
okf(lambda t: 0.5 * lg(t * t - 3 * t + 2) - lg(t), [2 / 3])
okf(lambda t: lg((2 * t - 2) / t) - 2 * lg(t - 1) + lg(t), [3])
okf(lambda t: 2 * lg(t) - lg(t / 2) + 1, [1 / 20])
okf(lambda t: lg(4 - 5 * t) + lg(2 * t) - lg(2 * t - t * t) - lg(3), [2 / 7])
okf(lambda t: math.log2(5 * t * t + 15 * t + 10) - math.log2(t + 2) - 2, [-0.2])
okf(lambda t: lg(4 - t) / lg(t + 2) - 2, [0])
okf(lambda t: math.log2(t + 1) + math.log2(t - 1) - 3, [3])
okf(lambda t: lg(t) + lg(2) - 1, [5]); okf(lambda t: 2 * lg(t) - lg(4) - lg(9), [6])
ck(set(sp.solve(x ** 2 - 3 * x - 18, x)) == {6, -3})
S.append((T("Equacions logarítmiques", "Ecuaciones logarítmicas"), [
 (2, T(r"Resol les equacions logarítmiques següents:", r"Resuelve las ecuaciones logarítmicas siguientes:")
     + tasks(2, [r"$\log2+\log(x+3)=\log(x+5)$", r"$\log(15-2x)=2\log x$", r"$\log(2x+3)-\log(x-1)=2\log2+2\log3$", r"$\frac12\log(x^2-3x+2)=\log x$", r"$\log\left(\dfrac{2x-2}{x}\right)=2\log(x-1)-\log x$",
                 r"$2\log x=\log\dfrac x2-1$", r"$\log(4-5x)+\log(2x)=\log(2x-x^2)+\log3$", r"$\log_2(x+1)+\log_2(x-1)=3$", r"$\log_2(5x^2+15x+10)-\log_2(x+2)=2$", r"$\dfrac{\log(4-x)}{\log(x+2)}=2$"])
     + recorda(T(r"Agrupa els logaritmes amb les propietats fins a arribar a $\log A=\log B$ (i aleshores $A=B$). Comprova que tots els arguments són positius.",
                 r"Agrupa los logaritmos con las propiedades hasta llegar a $\log A=\log B$ (y entonces $A=B$). Comprueba que todos los argumentos son positivos.")),
     tasks(1, [r"$2(x+3)=x+5$: \ " + R("x=-1"), r"$15-2x=x^2\Rightarrow x=3,\ x=-5$; \ $x=-5$ " + NOVAL + r": \ " + R("x=3"), r"$\dfrac{2x+3}{x-1}=36\Rightarrow34x=39$: \ " + R(r"x=\frac{39}{34}"),
               r"$x^2-3x+2=x^2\Rightarrow$ " + R(r"x=\frac23") + T(r" (val: $x\gt0$ i $x^2-3x+2=\frac49\gt0$)", r" (vale: $x\gt0$ y $x^2-3x+2=\frac49\gt0$)"),
               r"$\dfrac{2x-2}{x}=\dfrac{(x-1)^2}{x}\Rightarrow(x-1)(x-3)=0$; \ $x=1$ " + NOVAL + r": \ " + R("x=3"),
               r"$\log x^2=\log\dfrac{x}{20}\Rightarrow x^2=\dfrac x{20}$; \ $x=0$ " + NOVAL + r": \ " + R(r"x=\frac1{20}"),
               r"$2x(4-5x)=3(2x-x^2)\Rightarrow7x^2-2x=0$; \ $x=0$ " + NOVAL + r": \ " + R(r"x=\frac27"),
               r"$x^2-1=8\Rightarrow x=\pm3$; \ $x=-3$ " + NOVAL + r": \ " + R("x=3"),
               r"$\dfrac{5(x+1)(x+2)}{x+2}=4\Rightarrow5x+5=4$: \ " + R(r"x=-\frac15"),
               r"$4-x=(x+2)^2\Rightarrow x^2+5x=0$; \ $x=-5$ " + NOVAL + r": \ " + R("x=0")])),
 (1, T(r"Troba el nombre que compleix que, en afegir al seu logaritme decimal el logaritme decimal de 2, el resultat és 1.", r"Halla el número que cumple que, al añadir a su logaritmo decimal el logaritmo decimal de 2, el resultado es 1."),
     r"$\log x+\log2=1\Rightarrow\log(2x)=\log10$: \ " + R("x=5")),
 (1, T(r"Calcula el valor d'un nombre sabent que el doble del seu logaritme decimal és igual a la suma dels logaritmes decimals de 4 i de 9.", r"Calcula el valor de un número sabiendo que el doble de su logaritmo decimal es igual a la suma de los logaritmos decimales de 4 y de 9."),
     r"$2\log x=\log4+\log9\Rightarrow x^2=36$ ($x\gt0$): \ " + R("x=6")),
 (2, T(r"Resol $2\log x-\log(x+6)=\log3$.", r"Resuelve $2\log x-\log(x+6)=\log3$."),
     r"$\dfrac{x^2}{x+6}=3\Rightarrow x^2-3x-18=0\Rightarrow x=6,\ x=-3$; \ $x=-3$ " + NOVAL + r": \ " + R("x=6")),
]))
okf(lambda t: 2 * lg(t) - lg(t + 6) - lg(3), [6], [-3])

# =====================================================================
# 10. Problemes
def one(eq, val, var=x):
    sols = sp.solve(eq, var); ck(val in sols, 'prob %s -> %s' % (eq, sols)); return val
one(38 + x - 2 * (10 + x), 18); one(x * Q(121, 100) - Q(121, 2), 50); one(x * Q(80, 100) * Q(90, 100) - 36, 50)
one(5 * x + 2 * 50 - 4 * (x + 100), 300); one(30 * 5 + 10 * x - 7 * (30 + x), 20); one(18 * x + 14 * (1 - x) - Q(82, 5), Q(3, 5))
one(Q(1, 10) * x - 15, 150); one(Q(15, 100) * x - 3, 20); one(5 * x - 2 * (20 - x) - 58, 14)
one(x ** 2 - 75 * x - 6250, 125); one(x ** 2 + (x + 1) ** 2 - 25, 3); one(x ** 2 + (70 - x) ** 2 - 2500, 40)
ck(Q(1, 5) + Q(1, 20) == Q(1, 4) and Q(1, 2) + Q(1, 3) == Q(5, 6))
one(1 / x + 1 / (2 * x) - Q(1, 10), 15)
ck(abs(5 * math.log(4) - 6.931) < 1e-3 and abs(27 * math.exp(-1) - 9.933) < 1e-3 and abs(math.log2(100 / 9) - 3.474) < 1e-3)
one(x + (x + 1) + (x + 2) - 93, 30); one(x * (x + 10) - 1200, 30)
S.append((T("Problemes", "Problemas"), [
 (1, T(r"Una mare té 38 anys i el seu fill, 10. Quants anys han de passar perquè l'edat de la mare siga el doble que la del fill?",
       r"Una madre tiene 38 años y su hijo, 10. ¿Cuántos años tienen que pasar para que la edad de la madre sea el doble que la del hijo?"),
     r"$38+x=2(10+x)\Rightarrow$ " + R(T(r"x=18\ \text{anys}", r"x=18\ \text{años}"))),
 (1, T(r"La suma de tres nombres naturals consecutius és 93. Quins són?", r"La suma de tres números naturales consecutivos es 93. ¿Cuáles son?"),
     r"$x+(x+1)+(x+2)=93\Rightarrow3x=90$: \ " + R(r"30,\ 31,\ 32")),
 (1, T(r"Un article costa 60,50\,€ amb l'IVA del 21\,\% inclòs. Quin és el preu sense IVA?", r"Un artículo cuesta 60,50\,€ con el IVA del 21\,\% incluido. ¿Cuál es el precio sin IVA?"),
     r"$1,21x=60,50\Rightarrow$ " + R(r"x=50\ \text{€}")),
 (2, T(r"Després d'una rebaixa del 20\,\% i d'una altra del 10\,\% sobre el preu ja rebaixat, una jaqueta costa 36\,€. Quant costava abans de les rebaixes? Quin és el percentatge total de rebaixa?",
       r"Después de una rebaja del 20\,\% y de otra del 10\,\% sobre el precio ya rebajado, una chaqueta cuesta 36\,€. ¿Cuánto costaba antes de las rebajas? ¿Cuál es el porcentaje total de rebaja?"),
     r"$0,8\cdot0,9\,x=0,72x=36\Rightarrow$ " + R(r"x=50\ \text{€}") + r"; \ " + T("rebaixa total: ", "rebaja total: ") + R(r"28\,\%") + T(r" (no el 30\,\%).", r" (no el 30\,\%).")),
 (2, T(r"Un comerciant té un tonell de vi de classe A de 5\,€/L. Hi afig 50 litres de vi de classe B de 2\,€/L i 50 litres d'aigua, i la mescla resulta a 4\,€/L. Quants litres de vi de classe A tenia el tonell?",
       r"Un comerciante tiene un tonel de vino de clase A de 5\,€/L. Le añade 50 litros de vino de clase B de 2\,€/L y 50 litros de agua, y la mezcla resulta a 4\,€/L. ¿Cuántos litros de vino de clase A tenía el tonel?"),
     r"$5x+2\cdot50+0\cdot50=4(x+100)\Rightarrow$ " + R(r"x=300\ \text{L}")),
 (1, T(r"Tenim 30 litres de vi a 5\,€/L i volem afegir-hi vi de 10\,€/L per a obtindre una mescla que isca a 7\,€/L. Quants litres n'hem d'afegir?",
       r"Tenemos 30 litros de vino a 5\,€/L y queremos añadir vino de 10\,€/L para obtener una mezcla que salga a 7\,€/L. ¿Cuántos litros tenemos que añadir?"),
     r"$30\cdot5+10x=7(30+x)\Rightarrow3x=60$: \ " + R(r"20\ \text{L}")),
 (2, T(r"En una botiga es ven te blanc a 18\,€/kg i te verd a 14\,€/kg, i també una mescla dels dos a 16,40\,€/kg. Quina és la composició de la mescla?",
       r"En una tienda se vende té blanco a 18\,€/kg y té verde a 14\,€/kg, y también una mezcla de los dos a 16,40\,€/kg. ¿Cuál es la composición de la mezcla?"),
     T(r"En 1 kg, $x$ kg de te blanc: ", r"En 1 kg, $x$ kg de té blanco: ") + r"$18x+14(1-x)=16,4\Rightarrow x=0,6$: \ " + R(T(r"60\,\%\ \text{blanc i }40\,\%\ \text{verd}", r"60\,\%\ \text{blanco y }40\,\%\ \text{verde}"))),
 (1, T(r"En un institut hi ha tres cursos. El 60\,\% de l'alumnat estudia primer, el 30\,\% estudia segon i la resta, que són 15 alumnes, estudia tercer. Quants alumnes hi ha a l'institut?",
       r"En un instituto hay tres cursos. El 60\,\% del alumnado estudia primero, el 30\,\% estudia segundo y el resto, que son 15 alumnos, estudia tercero. ¿Cuántos alumnos hay en el instituto?"),
     T(r"El 10\,\% són 15: \ ", r"El 10\,\% son 15: \ ") + R(T(r"150\ \text{alumnes}", r"150\ \text{alumnos}"))),
 (1, T(r"Una fàbrica exporta el 30\,\% de la producció a Àsia, el 40\,\% a Europa, el 15\,\% a Amèrica i la resta, que suposa una facturació de 3 milions d'euros, a Àfrica. Quina és la facturació total?",
       r"Una fábrica exporta el 30\,\% de la producción a Asia, el 40\,\% a Europa, el 15\,\% a América y el resto, que supone una facturación de 3 millones de euros, a África. ¿Cuál es la facturación total?"),
     T(r"Àfrica és el 15\,\%: ", r"África es el 15\,\%: ") + r"$0,15x=3\Rightarrow$ " + R(T(r"20\ \text{milions d'euros}", r"20\ \text{millones de euros}"))),
 (2, T(r"Un examen té 20 preguntes. Cada encert suma 5 punts i cada errada en resta 2. Una alumna va traure 58 punts. Quantes preguntes va encertar i quantes en va errar, si no en podia deixar cap sense contestar?",
       r"Un examen tiene 20 preguntas. Cada acierto suma 5 puntos y cada fallo resta 2. Una alumna sacó 58 puntos. ¿Cuántas preguntas acertó y cuántas falló, si no podía dejar ninguna sin contestar?"),
     r"$5x-2(20-x)=58\Rightarrow7x=98$: \ " + R(T(r"14\ \text{encerts i }6\ \text{errades}", r"14\ \text{aciertos y }6\ \text{fallos}"))),
 (3, T(r"Un botiguer inverteix 125\,€ en la compra d'una partida de pomes. En rebutja 20 quilos per defectuoses i ven la resta per 147\,€, i guanya 0,40\,€ per quilo sobre el preu de compra. Quants quilos en va comprar?",
       r"Un tendero invierte 125\,€ en la compra de una partida de manzanas. Desecha 20 kilos por defectuosos y vende el resto por 147\,€, ganando 0,40\,€ por kilo sobre el precio de compra. ¿Cuántos kilos compró?"),
     r"$(x-20)\left(\dfrac{125}{x}+0,4\right)=147\Rightarrow x^2-75x-6250=0\Rightarrow x=125$ ($x=-50$ " + T("no té sentit", "no tiene sentido") + r"): \ " + R(r"125\ \text{kg}")),
 (2, T(r"Un solar rectangular fa 10 m més de llarg que d'ample i té una superfície de 1200 m$^2$. Quines en són les dimensions?",
       r"Un solar rectangular mide 10 m más de largo que de ancho y tiene una superficie de 1200 m$^2$. ¿Cuáles son sus dimensiones?"),
     r"$x(x+10)=1200\Rightarrow x^2+10x-1200=0\Rightarrow x=30$ ($x=-40$ " + T("no té sentit", "no tiene sentido") + r"): \ " + R(r"30\ \text{m}\times40\ \text{m}")),
 (2, T(r"Calcula les dimensions d'una finca rectangular si el perímetre fa 140 m i la diagonal, 50 m.", r"Calcula las dimensiones de una finca rectangular si el perímetro mide 140 m y la diagonal, 50 m."),
     r"$x^2+(70-x)^2=2500\Rightarrow x^2-70x+1200=0$: \ " + R(r"40\ \text{m}\times30\ \text{m}")),
 (1, T(r"Una bassa tarda 5 hores a omplir-se amb la presa d'aigua habitual i 20 hores amb una mànega. Quant de temps cal si fem servir tots dos mètodes alhora?",
       r"Una balsa tarda 5 horas en llenarse con la toma de agua habitual y 20 horas con una manguera. ¿Cuánto tiempo hace falta si usamos los dos métodos a la vez?"),
     r"$\frac15+\frac1{20}=\frac14$: \ " + R(r"T=4\ \text{h}")),
 (2, T(r"Dues persones treballant juntes tarden 10 hores a fer un treball, però una treballa el doble de ràpid que l'altra. Quant tardaria cadascuna per separat?",
       r"Dos personas trabajando juntas tardan 10 horas en hacer un trabajo, pero una trabaja el doble de rápido que la otra. ¿Cuánto tardaría cada una por separado?"),
     r"$\dfrac1t+\dfrac1{2t}=\dfrac1{10}\Rightarrow t=15$: \ " + R(T(r"15\ \text{h i }30\ \text{h}", r"15\ \text{h y }30\ \text{h}"))),
 (2, T(r"El nombre de malalts de grip en una ciutat al llarg del passat gener ve donat per $y(t)=100+200\cdot e^{0,2t}$, on $t$ són els dies transcorreguts des de l'1 de gener.",
       r"El número de enfermos de gripe en una ciudad a lo largo del pasado enero viene dado por $y(t)=100+200\cdot e^{0,2t}$, donde $t$ son los días transcurridos desde el 1 de enero.")
     + tasks(1, [T("Quants malalts hi havia l'1 de gener?", "¿Cuántos enfermos había el 1 de enero?"), T("Quin dia el nombre de malalts era de 900?", "¿Qué día el número de enfermos era de 900?")]),
     tasks(1, [R(T(r"y(0)=300\ \text{malalts}", r"y(0)=300\ \text{enfermos}")), r"$200e^{0,2t}=800\Rightarrow t=5\ln4\approx6,93$: \ " + R(T(r"\text{el 7 de gener (cap al final del dia)}", r"\text{el 7 de enero (hacia el final del día)}"))])),
 (2, T(r"Si inicialment hi ha $n$ bacteris en un cultiu i el nombre es duplica cada hora, després de $t$ hores n'hi ha $N=n\cdot2^t$. Si inicialment n'hi ha 4500, quant de temps tardarà el cultiu a arribar a 50\,000 bacteris?",
       r"Si inicialmente hay $n$ bacterias en un cultivo y el número se duplica cada hora, después de $t$ horas hay $N=n\cdot2^t$. Si inicialmente hay 4500, ¿cuánto tiempo tardará el cultivo en llegar a 50\,000 bacterias?"),
     r"$2^t=\dfrac{100}{9}\Rightarrow t=\dfrac{\log(100/9)}{\log2}\approx" + Ri(r"3,47\ \text{h}\approx3\ \text{h}\ 28\ \text{min}") + "$"),
]))

bad = [mm for c_, mm in CHK if not c_]
assert not bad, bad[:5]
assert [len(s_[1]) for s_ in S] == [5, 9, 6, 4, 6, 3, 3, 5, 4, 17], [len(s_[1]) for s_ in S]
NEX = sum(len(s_[1]) for s_ in S)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("polinomis, Ruffini, teorema del residu, factorització, fraccions algebraiques, equacions de primer i segon grau, biquadrades, radicals, racionals, exponencials, logarítmiques",
       "polinomios, Ruffini, teorema del resto, factorización, fracciones algebraicas, ecuaciones de primer y segundo grado, bicuadradas, radicales, racionales, exponenciales, logarítmicas")
if not ES:
    pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: 'pdfkeywords={' + KW + '}', pre)
    pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les CCSS I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'\providecommand{\lt}{<}\providecommand{\gt}{>}' + '\n'
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{''' + T('Recorda', 'Recuerda') + r''':}\ #1\end{tcolorbox}}
'''

TIT = T("Àlgebra", "Álgebra")
def spc(t):
    # «, » separa elements; amb icomma la coma és un símbol normal i un «-» darrere seu seria una resta: el posem entre claus
    return re.sub(r'\$[^$]*\$', lambda mm: re.sub(r',((?:\\,|\\ |\\;|\s)+)-', r',\1{-}', mm.group(0).replace(', ', r',\, ')), t)
def build(sol):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 2: %s' % (t, TIT), capcalera='%s · Unidad 2: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-ccss')
        cap_ = assignatura('1batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 2' if sol else 'Ficha de ejercicios · Unidad 2') + '}'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                        "pdftitle={%s de la unitat 2: %s. 1r de Batxillerat CCSS}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 2: %s · 1r Batxillerat CCSS" % (t, TIT))
        assert 'Unitat 2' in p and 'unitat 2' in p
        cap_ = r'\capcalera{Matemàtiques CCSS}{1r Batx}{' + ('Solucions de la fitxa · Unitat 2' if sol else "Fitxa d'exercicis · Unitat 2") + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + cap_ + r'''{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Els resultats es donen de manera exacta (fraccions i arrels) i, quan cal, amb el valor aproximat. Pots comprovar les divisions, la factorització, les fraccions i les equacions de primer i segon grau amb les eines interactives dels apunts de la unitat.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Los resultados se dan de manera exacta (fracciones y raíces) y, cuando hace falta, con el valor aproximado. Puedes comprobar las divisiones, la factorización, las fracciones y las ecuaciones de primer y segundo grado con las herramientas interactivas de los apuntes de la unidad.")
             if sol else T(r"Resol els exercicis al quadern mostrant tots els passos. Dona els resultats de manera exacta i, si cal, també aproximats. En les equacions amb radicals, denominadors amb $x$ o logaritmes, comprova sempre les solucions. En els problemes, indica què és la incògnita i respon amb una frase.",
                           r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Da los resultados de manera exacta y, si hace falta, también aproximados. En las ecuaciones con radicales, denominadores con $x$ o logaritmos, comprueba siempre las soluciones. En los problemas, indica qué es la incógnita y responde con una frase."))
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + intro + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, spc(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = ('t2-fitxa-solucions' if sol else 't2-fitxa-exercicis') + ('-es' if ES else '') + '.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(NEX, T('exercicis;', 'ejercicios;'), len(CHK), T('comprovacions', 'comprobaciones'))
