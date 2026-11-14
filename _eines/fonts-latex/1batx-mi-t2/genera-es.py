# Versió en castellà de genera.py: escriu els -es.tex. Original: genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (1r Batxillerat MI, Unitat 2: Àlgebra. Equacions i inequacions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Els exercicis 1-62 són de la fitxa del departament (l'1-55, amb la mateixa numeració); la secció 12 n'afegeix 9 de nous.
# Els sistemes són a la unitat 3 (carpeta 1batx-mi-t3).
# Les solucions de polinomis, fraccions, equacions polinòmiques i racionals i inequacions es calculen ací
# amb sympy; les de radicals, logaritmes, exponencials i problemes s'escriuen a mà i CHK les comprova (numèricament o amb
# sympy). Les solucions d'inequacions porten la recta dibuixada (TikZ, aritmètica exacta).
# Ús: python3 genera.py && pdflatex t2-fitxa-exercicis.tex (dues vegades) && pdflatex t2-fitxa-solucions.tex (dues vegades)
import os, re, math
from fractions import Fraction as F
import sympy as sp
from sympy import Rational as Q, sqrt, oo
HERE = os.path.dirname(os.path.abspath(__file__))
x, y, z, w, a, b, k, m = sp.symbols('x y z w a b k m')
xr = sp.Symbol('x', real=True)

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def L(e):
    s = sp.latex(e, order='lex')
    return s.replace(r'\left(', '(').replace(r'\right)', ')').replace(r'\log{(', r'\log(').replace(r'\ln{(', r'\ln(')
def dec(v, n=3):
    s = ('%.' + str(n) + 'f') % float(v)
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    return s.replace('.', ',')
def sist(*rows): return r'\left\{\begin{array}{l}' + r'\\'.join(rows) + r'\end{array}\right.'

CHK = []
def ck(cond, msg=''):
    CHK.append((bool(cond), msg)); return cond
def eqn(expr, vals, tol=1e-9):
    """comprova numèricament que expr(x) = 0 per a cada valor"""
    for v in vals:
        val = complex(sp.N(expr.subs(x, v), 30))
        ck(abs(val) < tol, 'eq %s at %s -> %s' % (expr, v, val))

# ---------- conjunts de la recta ----------
def ivs(Sset):
    if Sset == sp.S.EmptySet: return []
    parts = Sset.args if isinstance(Sset, sp.Union) else [Sset]
    out = []
    for I in parts:
        if isinstance(I, sp.Interval): out.append((I.start, not I.left_open, I.end, not I.right_open))
        elif isinstance(I, sp.FiniteSet): out += [(v, True, v, True) for v in I]
        else: raise ValueError(I)
    return sorted(out, key=lambda t: -1e18 if t[0] == -oo else float(t[0]))
def ivt(I):
    a_, ac, b_, bc = I
    if a_ == b_: return r'\{%s\}' % L(a_)
    ta = r'-\infty' if a_ == -oo else L(a_)
    tb = r'+\infty' if b_ == oo else L(b_)
    return ('[' if ac else '(') + ta + ', ' + tb + (']' if bc else ')')
def st(Sset):
    I = ivs(Sset)
    if not I: return r'\varnothing'
    if len(I) == 1 and I[0][0] == -oo and I[0][2] == oo: return r'\mathbb R'
    return r'\cup'.join(ivt(i) for i in I)
def recta(Sset):
    S = ivs(Sset)
    pts = [float(v) for I in S for v in (I[0], I[2]) if v not in (oo, -oo)] or [0]
    lo, hi = math.floor(min(pts)) - 1, math.ceil(max(pts)) + 1
    if hi - lo < 6: c = (hi + lo) / 2; lo, hi = math.floor(c - 3), math.ceil(c + 3)
    step = 2 if hi - lo > 14 else 1
    sc = min(0.42, 7.2 / (hi - lo + 1.4))
    o = [r'\begin{tikzpicture}[x=%.3fcm,baseline=-3pt]' % sc, r'\draw[-latex,muted] (%g,0)--(%g,0);' % (lo - 0.6, hi + 0.7)]
    v = math.ceil(lo / step) * step
    while v <= hi:
        o.append(r'\draw[muted] (%d,0.1)--(%d,-0.1) node[below=-1pt,font=\scriptsize,text=muted]{$%d$};' % (v, v, v)); v += step
    for a_, ac, b_, bc in S:
        xa = lo - 0.45 if a_ == -oo else float(a_); xb = hi + 0.45 if b_ == oo else float(b_)
        if a_ != b_: o.append(r'\draw[accent,line width=2.6pt] (%g,0)--(%g,0);' % (xa, xb))
        if a_ == -oo: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xa - 0.3, xa + 0.1, xa + 0.1))
        if b_ == oo: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xb + 0.3, xb - 0.1, xb - 0.1))
        for xv, c, lab in ((a_, ac, True), (b_, bc, a_ != b_)):
            if xv in (oo, -oo) or not lab: continue
            o.append((r'\fill[accent] (%g,0) circle (2.3pt);' if c else r'\filldraw[fill=white,draw=accent,line width=1.1pt] (%g,0) circle (2.3pt);') % float(xv))
            if not xv.is_integer: o.append(r'\node[above=1pt,font=\scriptsize,text=accent] at (%g,0) {$%s$};' % (float(xv), L(xv)))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def RI(Sset): return R('x\\in ' + st(Sset)) + r'\\[2pt]' + recta(Sset)
def ineq(e): return sp.solve_univariate_inequality(e, xr, relational=False)

# ---------- Ruffini ----------
def ruf(coefs, a_):
    coefs = [sp.nsimplify(c) for c in coefs]; a_ = sp.nsimplify(a_)
    res = [coefs[0]]; prod = [None]
    for c in coefs[1:]:
        mm = res[-1] * a_; prod.append(mm); res.append(c + mm)
    n = len(coefs)
    cols = 'r|' + 'r' * (n - 1) + '|r'
    rows = [' & ' + ' & '.join(L(c) for c in coefs), L(a_) + ' & ' + ' & '.join('' if p is None else L(p) for p in prod),
            r'\hline & ' + ' & '.join(L(r_) for r_ in res)]
    return r'{\def\arraystretch{1.5}\begin{array}{%s}%s\end{array}}' % (cols, r'\\'.join(rows)), res
def coefs(P): return sp.Poly(P, x).all_coeffs()

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Polinomis. Operacions
E1 = [2 * (x - 2) ** 2 - 3 * (3 * x + 2) - 2 * (3 * x - 2) * (3 * x + 2), (3 * x + 2) ** 2 + 2 * (2 * x - 3) ** 2 - (x - 5) * (2 * x - 5),
      (2 * x ** 2 - 2 * x - 13) * (3 * x ** 2 - 2 * x) - 3 * x, (x ** 2 + 4) * (x ** 2 - 4) * (x - 2) + 2 * x * (x ** 3 - 10) * x,
      (Q(2, 3) * x - Q(3, 5)) * (Q(3, 2) * x ** 2 + Q(2, 5)) + Q(6, 25)]
r4a = sp.solve(sp.Poly(sp.expand((3 * x ** 2 - 5 * x + a) * (2 * x ** 2 + b * x) - (6 * x ** 4 - 19 * x ** 3 + 19 * x ** 2 - 6 * x)), x).coeffs(), [a, b], dict=True)
r4b = sp.solve(sp.Poly(sp.expand(2 * (x + 3) ** 2 - 3 * (x + a) - (2 * x ** 2 + b * x + 3)), x).coeffs(), [a, b], dict=True)
ck(r4a == [{a: 2, b: -3}] and r4b == [{a: 5, b: 9}], '4')
D5 = [(3 * x ** 3 + 2 * x ** 2 + x - 5, 3 * x ** 2 + 2), (3 * x ** 4 - 2 * x ** 2 - x + 4, x ** 2 + x + 2), (x ** 3 - 3 * x ** 2 - x + 6, 2 * x ** 3 - 2 * x + 3)]
def divsol(D, d):
    q, r = sp.div(D, d, x)
    ck(sp.expand(d * q + r - D) == 0)
    return r'$c(x)=' + R(L(q)).strip('$') + r',\ \ r(x)=' + R(L(r)).strip('$') + '$'
D6 = [(3 * x ** 3 + 2 * x ** 2 + x - 5, 1, -2), (3 * x ** 4 - 2 * x ** 2 - x + 4, 1, -2), (x ** 3 - 3 * x ** 2 - x + 6, 2, Q(-3, 2)), (4 * x ** 4 - 3 * x ** 2 + 5, -1, 5), (2 * x ** 5 - 12 * x ** 3 - 6 * x ** 2 - 117, 1, 3)]
def rufsol(D, lead, a_):
    T, res = ruf(coefs(D), a_)
    q, r = sp.div(D, lead * (x - a_), x)
    ck(r == res[-1] and sp.expand(sp.Poly(res[:-1], x).as_expr() / lead - q) == 0, 'ruf %s' % D)
    extra = '' if lead == 1 else (r'\ \ \text{(cociente de Ruffini dividido entre }%s)' % L(lead))
    return r'$' + T + r'$\\[2pt]$c(x)=' + R(L(q)).strip('$') + r',\ \ r=' + R(L(r)).strip('$') + extra + '$'
P7 = [(2 * x ** 3 + 5 * x ** 2 - 2 * x + a, -3, a, 3), (2 * x ** 4 + 3 * x ** 3 - 2 * x ** 2 - a * x + 3, Q(-3, 2), a, 1),
      (-6 * x ** 4 + 11 * x ** 3 + a * x ** 2 + 5 * x + 4, Q(4, 3), a, -10), (4 * x ** 4 + 6 * x ** 3 - 13 * x ** 2 + x + b, 5, b, -2930)]
def s7(P, r_, var, val):
    ck(sp.solve(P.subs(x, r_), var) == [val], '7 %s' % P)
    return r'$P(%s)=%s=0\Rightarrow ' % (L(r_), L(sp.expand(P.subs(x, r_)))) + R('%s=%s' % (L(var), L(val))).strip('$') + '$'
M8 = 2 * x ** 3 - 5 * x ** 2 + 4 * x - 4
ck(M8.subs(x, 2) == 0 and sp.div(M8, x - 2, x) == (2 * x ** 2 - x + 2, 0))
S.append(("Polinomios. Operaciones", [
 (1, r"Simplifica las siguientes expresiones polinómicas." + tasks(1, [r"$2(x-2)^2-3(3x+2)-2(3x-2)(3x+2)$", r"$(3x+2)^2+2(2x-3)^2-(x-5)(2x-5)$", r"$(2x^2-2x-13)(3x^2-2x)-3x$",
      r"$(x^2+4)(x^2-4)(x-2)+2x(x^3-10)x$", r"$\left(\frac23x-\frac35\right)\left(\frac32x^2+\frac25\right)+\frac{6}{25}$"])
     + recorda(r"$(a\pm b)^2=a^2\pm2ab+b^2$, \ $(a+b)(a-b)=a^2-b^2$. Desarrolla cada producto y reduce los términos semejantes."),
     tasks(1, [R(L(sp.expand(e))) for e in E1])),
 (2, r"Demuestra la igualdad algebraica: \[(x+y+z)^2=x^2+y^2+z^2+2xy+2xz+2yz\]",
     r"$(x+y+z)^2=\big((x+y)+z\big)^2=(x+y)^2+2(x+y)z+z^2=x^2+2xy+y^2+2xz+2yz+z^2$. \rest{Queda demostrada.}"),
 (1, r"Calcula $(4x^2-3x+2)^2$.", R(L(sp.expand((4 * x ** 2 - 3 * x + 2) ** 2))) + r" \ (con la identidad del ejercicio anterior)."),
 (2, r"Calcula los valores de $a$ y $b$ para que se verifiquen las siguientes igualdades." + tasks(1, [r"$(3x^2-5x+a)(2x^2+bx)=6x^4-19x^3+19x^2-6x$", r"$2(x+3)^2-3(x+a)=2x^2+bx+3$"]),
     tasks(1, [r"$6x^4+(3b-10)x^3+(2a-5b)x^2+abx$: \ $3b-10=-19$, $ab=-6\Rightarrow " + R("a=2,\\ b=-3").strip('$') + "$",
               r"$2x^2+9x+18-3a$: \ $" + R("b=9").strip('$') + r",\ \ 18-3a=3\Rightarrow " + R("a=5").strip('$') + "$"])),
 (1, r"Efectúa las siguientes divisiones:" + tasks(1, [r"$(3x^3+2x^2+x-5):(3x^2+2)$", r"$(3x^4-2x^2-x+4):(x^2+x+2)$", r"$(x^3-3x^2-x+6):(2x^3-2x+3)$"]),
     tasks(1, [divsol(*d) for d in D5])),
 (1, r"Efectúa las siguientes divisiones aplicando la regla de Ruffini:" + tasks(2, [r"$(3x^3+2x^2+x-5):(x+2)$", r"$(3x^4-2x^2-x+4):(x+2)$", r"$(x^3-3x^2-x+6):(2x+3)$", r"$(4x^4-3x^2+5):(-x+5)$", r"$(2x^5-12x^3-6x^2-117):(x-3)$"])
     + recorda(r"Si el divisor es $ax+b$, haz Ruffini con $-\frac ba$ y divide el cociente entre $a$; el resto no cambia."),
     tasks(1, [rufsol(*d) for d in D6])),
 (2, r"Utiliza Ruffini para calcular el valor de $a$ y $b$ que hace que las siguientes divisiones sean exactas:" + tasks(1, [r"$(2x^3+5x^2-2x+a):(x+3)$", r"$(2x^4+3x^3-2x^2-ax+3):(2x+3)$", r"$(-6x^4+11x^3+ax^2+5x+4):(-3x+4)$", r"$(4x^4+6x^3-13x^2+x+b):(-x+5)$"]),
     tasks(1, [s7(*p) for p in P7]) + r"(Con el teorema del resto, $P(r)$ debe ser 0, donde $r$ es la raíz del divisor; es lo mismo que obtener resto 0 en Ruffini.)"),
 (1, r"Comprueba si $M(x)=2x^3-5x^2+4x-4$ es divisible por $x-2$ y, si lo es, halla un polinomio $N(x)$ que permita escribir $M(x)=(x-2)\cdot N(x)$.",
     r"$M(2)=16-20+8-4=0$: \rest{sí es divisible}.\par Por Ruffini: $" + ruf(coefs(M8), 2)[0] + r"\Rightarrow " + R("N(x)=2x^2-x+2").strip('$') + "$"),
]))

# =====================================================================
# 2. Factorització d'un polinomi. Teorema del residu
P9 = x ** 4 + 3 * x ** 3 - 2 * x ** 2 + 6 * x - 8
v9 = [P9.subs(x, v) for v in (1, 2, -1, -4, -3)]
ck(v9 == [0, 36, -18, 0, -44])
def rootsT(P):
    rr = sp.roots(sp.Poly(P, x), filter='R')
    items = sorted(rr.items(), key=lambda t: float(t[0]))
    return r',\ '.join('x=%s%s' % (L(r_), r'\ (\text{%s})' % {2: 'doble', 3: 'triple'}[mm] if mm > 1 else '') for r_, mm in items)
P11 = [(x - 3) * (x + 5) * (x - 2), x * (x - 2) ** 3 * (2 * x + 1), (2 * x - 1) * (3 * x + 2) * (x + 1) ** 3, x ** 3 - 3 * x ** 2 - 6 * x + 8, x ** 3 + 8 * x ** 2 + 17 * x + 10, 2 * x ** 5 - 11 * x ** 4 + 21 * x ** 3 - 16 * x ** 2 + 4 * x]
P12 = [x ** 3 - 2 * x ** 2 - 5 * x + 6, x ** 3 + x ** 2 - 5 * x + 3, 2 * x ** 4 - x ** 3 - 5 * x ** 2 + x + 3, 4 * x ** 3 - 4 * x ** 2 - 11 * x + 6, x ** 4 - 4 * x ** 2,
       6 * x ** 5 + 11 * x ** 4 + 3 * x ** 3 - 3 * x ** 2 - x, x ** 6 - 4 * x ** 4 - x ** 2 + 4]
P12h = x ** 4 / 4 + Q(3, 4) * x ** 2 + Q(9, 16)
ck(sp.expand(P12h - (2 * x ** 2 + 3) ** 2 / 16) == 0 and sp.roots(sp.Poly(P12h, x), filter='R') == {})
def k13(P, r_, val):
    ck(sp.solve(P.subs(x, r_), k) == [val], '13 %s' % P)
    return r'$P(%s)=%s=0\Rightarrow ' % (L(r_), L(sp.expand(P.subs(x, r_)))) + R('k=' + L(val)).strip('$') + '$'
P13 = [(x ** 3 + x ** 2 - 2 * x + k, 2, -8), (x ** 3 - 2 * x ** 2 + k * x + 4, -2, -6), ((k - 3) * x ** 3 - 15 * x + k, -4, 4), (x ** 3 - (k - 3) * x ** 2 + (k - 5) * x - 3, 3, 6)]
P14 = x ** 3 - (3 * k + 2) * x ** 2 - 3
ck(sp.solve(P14.subs(x, -3), k) == [Q(-16, 9)] and sp.solve(P14.subs(x, -3) - 15, k) == [Q(-7, 3)])
A_, B_, C_ = sp.symbols('A B C')
ck(sp.solve([(A_ * x ** 2 + B_ * x + C_).subs(x, 1) + 6, C_ + 3, (A_ * x ** 2 + B_ * x + C_).subs(x, 3)], [A_, B_, C_]) == {A_: 2, B_: -5, C_: -3})
ck(sp.solve((m * x ** 3 - 6 * x ** 2 - 4 * x + 8).subs(x, 2), m) == [3])
ck(sp.solve([(x ** 3 + a * x ** 2 + b * x - 6).subs(x, 2), (x ** 3 + a * x ** 2 + b * x - 6).subs(x, -3)], [a, b]) == {a: 2, b: -5})
ck(sp.solve((2 * x ** 4 + 9 * x ** 3 + 2 * x ** 2 - 6 * x + 3 * m).subs(x, -2) - 12, m) == [Q(32, 3)])
S.append(("Factorización de un polinomio. Teorema del resto", [
 (1, r"Comprueba si son raíces del polinomio $P(x)=x^4+3x^3-2x^2+6x-8$ los números siguientes:" + tasks(5, ["$x=1$", "$x=2$", "$x=-1$", "$x=-4$", "$x=-3$"]),
     tasks(5, [r"$P(1)=0$: \rest{sí}", r"$P(2)=36$: \rest{no}", r"$P(-1)=-18$: \rest{no}", r"$P(-4)=0$: \rest{sí}", r"$P(-3)=-44$: \rest{no}"])),
 (1, r"Calcula el valor numérico del polinomio $P(x)=x^2-2x-3$ para $x=-1$ y $x=3$. ¿Podrías encontrar otro valor de $x$ para el cual el valor del polinomio sea cero? Razona la respuesta.",
     r"$P(-1)=1+2-3=" + R("0").strip('$') + r"$, \ $P(3)=9-6-3=" + R("0").strip('$') + r"$. \rest{No}: un polinomio de grado 2 tiene como máximo dos raíces, y ya las hemos encontrado: $P(x)=(x+1)(x-3)$."),
 (1, r"Determina las raíces de los polinomios siguientes:" + tasks(2, [r"$(x-3)(x+5)(x-2)$", r"$x(x-2)^3(2x+1)$", r"$(2x-1)(3x+2)(x+1)^3$", r"$x^3-3x^2-6x+8$", r"$x^3+8x^2+17x+10$", r"$2x^5-11x^4+21x^3-16x^2+4x$"]),
     tasks(1, [R(rootsT(P11[i])) + ('' if i in (0, 1, 2) else r" \ $\big(" + L(sp.factor(P11[i])) + r"\big)$") for i in range(6)])),
 (2, r"Determina, si existen, las raíces enteras de cada uno de los siguientes polinomios y factorízalos." + tasks(2, [r"$P(x)=x^3-2x^2-5x+6$", r"$P(x)=x^3+x^2-5x+3$", r"$P(x)=2x^4-x^3-5x^2+x+3$", r"$P(x)=4x^3-4x^2-11x+6$", r"$P(x)=x^4-4x^2$",
      r"$P(x)=6x^5+11x^4+3x^3-3x^2-x$", r"$P(x)=x^6-4x^4-x^2+4$", r"$P(x)=\frac{x^4}{4}+\frac34x^2+\frac{9}{16}$ \ (comprueba que no tiene raíces reales)"])
     + recorda(r"Las raíces enteras son divisores del término independiente. Pruébalas con Ruffini hasta que quede un polinomio de grado 2."),
     tasks(1, [R(L(sp.factor(P))) + r" \ \small(raíces: $" + rootsT(P) + "$)" for P in P12] +
           [r"$t=x^2$: $\frac{t^2}{4}+\frac34t+\frac9{16}=0\Rightarrow\Delta=\frac9{16}-\frac9{16}=0$, $t=-\frac32\lt0$: \rest{no tiene raíces reales}. $P(x)=" + R(r"\frac{1}{16}(2x^2+3)^2").strip('$') + "$"])),
 (1, r"Calcula el valor de $k$ para que el polinomio:" + tasks(1, [r"$P(x)=x^3+x^2-2x+k$ sea divisible por $x-2$", r"$P(x)=x^3-2x^2+kx+4$ sea divisible por $x+2$",
      r"$P(x)=(k-3)x^3-15x+k$ sea divisible por $x+4$", r"$P(x)=x^3-(k-3)x^2+(k-5)x-3$ sea divisible por $x-3$"]),
     tasks(1, [k13(*p) for p in P13])),
 (2, r"Calcula el valor de $k$ para que la división de $x^3-(3k+2)x^2-3$ entre $(x+3)$:" + tasks(2, ["Sea exacta.", "Tenga resto 15."]),
     r"$P(-3)=-27-9(3k+2)-3=-48-27k$." + tasks(2, [r"$-48-27k=0\Rightarrow " + R(r"k=-\frac{16}{9}").strip('$') + "$", r"$-48-27k=15\Rightarrow " + R(r"k=-\frac73").strip('$') + "$"])),
 (2, r"De un polinomio de segundo grado, $P(x)$, sabemos que $P(1)=-6$, $P(0)=-3$ y una de sus raíces es 3. Determínalo.",
     r"$P(x)=ax^2+bx+c$: \ $c=-3$, \ $a+b-3=-6$, \ $9a+3b-3=0\Rightarrow a=2,\ b=-5$: \ " + R("P(x)=2x^2-5x-3")),
 (1, r"Halla el valor de $m$ para que el polinomio $mx^3-6x^2-4x+8$ tenga 2 como raíz.", r"$P(2)=8m-24-8+8=8m-24=0\Rightarrow " + R("m=3").strip('$') + "$"),
 (2, r"Determina $a$ y $b$ de manera que el polinomio $x^3+ax^2+bx-6$ sea divisible por $x-2$ y por $x+3$.",
     r"$P(2)=0$: $4a+2b=-2$; \ $P(-3)=0$: $9a-3b=33$. \ " + R(r"a=2,\ b=-5") + r" \ (y entonces $P(x)=(x-2)(x+3)(x+1)$)."),
 (1, r"Halla el valor de $m$ para que el polinomio $2x^4+9x^3+2x^2-6x+3m$ tenga resto 12 al dividirlo por $x+2$, sin hacer la división.",
     r"Teorema del resto: $P(-2)=32-72+8+12+3m=-20+3m=12\Rightarrow " + R(r"m=\frac{32}{3}").strip('$') + "$"),
]))
ck(sp.expand(x ** 3 + 2 * x ** 2 - 5 * x - 6 - (x - 2) * (x + 3) * (x + 1)) == 0)

# =====================================================================
# 3. Fraccions algebraiques
F19 = [(2 * x ** 2 - 8, x ** 3 + x ** 2 - 2 * x), (x ** 3 - x, x ** 3 + 3 * x ** 2 + 2 * x), (x ** 4 - 2 * x ** 3 - 3 * x ** 2, x ** 4 - 9 * x ** 2), (x ** 3 - 3 * x ** 2 + 3 * x - 1, x ** 3 - 2 * x ** 2 + x),
       (2 * x ** 4 - 5 * x ** 3 + x ** 2 + 5 * x - 3, 2 * x ** 3 - x ** 2 - 7 * x + 6), (2 * x ** 4 + x ** 3 - 11 * x ** 2 + 11 * x - 3, 2 * x ** 3 + 3 * x ** 2 - 8 * x + 3),
       (x ** 3 - 2 * x ** 2 - 9 * x + 18, x ** 3 - 7 * x ** 2 + 16 * x - 12), (x ** 4 - 5 * x ** 3 + 9 * x ** 2 - 7 * x + 2, x ** 4 - 6 * x ** 3 + 13 * x ** 2 - 12 * x + 4)]
def simp(n, d): return r'$\dfrac{%s}{%s}=%s$' % (L(sp.factor(n)), L(sp.factor(d)), R(L(sp.factor(sp.cancel(n / d)))).strip('$'))
E20 = [1 / (x + 1) + 3 / (x ** 2 - 1), 1 / (x ** 2 + x) + 3 / (x + 1), 1 / (2 * x) - 3 / (4 * x ** 2 - 4 * x), 1 / (x ** 2 + x) + 3 / (x ** 2 - x),
       2 * x / (x - 2) + (3 * x - 1) / (x + 2) - 1 / (x ** 2 - 4), 1 / (x - 1) ** 2 + 2 / (x - 1) + 1 / (x ** 2 - 1)]
E21 = [(3 * x + 3) / (12 * x - 12) / ((x + 1) ** 2 / (x ** 2 - 1)), (x ** 2 + 2 * x - 3) / (x - 2) ** 3 * (x - 2) ** 2 / (x ** 2 - 1), (6 * x + 4) / (x - 2) * (4 * x + 1) / (2 * x + 4),
       -6 * x ** 2 / (x ** 2 + 2 * x + 1) * (x + 1) / (3 * x ** 3) * (x + 1) / (3 * x), (3 / x - 2 * x / (x + 1)) * ((x ** 2 + x) / (x - 1)), (x - 1) ** 2 / 2 * 1 / (x ** 2 - 1) - 3 * x / (x + 1) ** 2,
       ((2 * x - 1) / (x + 1) - 3 * x / (x - 1)) * ((x ** 3 - x) / (-x ** 2 - 6 * x + 1))]
E22 = [(x + 1) / x + (2 * x + 1) / (x + 2) - x / (x ** 2 + 1), (1 + (2 * x + 1) / (x - 1)) / (1 / (x - 1) + x / (x + 1)), (b * a - a ** 2) / (a ** 3 * b - a * b ** 3) / (b / (a ** 2 + 2 * a * b + b ** 2)),
       a ** 2 / (a * b) + a * b ** 2 / b ** 4 - a, 6 / (2 + x) - 4 / (2 - x) + 16 / (x ** 2 - 4), (2 * x ** 2 - 7 * x + 6) / (x ** 2 + 2 * x + 1) * (x ** 2 + 6 * x + 5) / (2 * x - 3),
       (x ** 2 - y ** 2) / (1 / x + 1 / y), (a + x) / (x ** 2 - a ** 2) * (x - a) / (x + a), 1 + 1 / (1 + 1 / (1 + 1 / x)), 1 + ((2 * x + 1) / (x - 1)) / (1 / (x - 1) + x / (x + 1))]
def res(e): return R(L(sp.factor(sp.cancel(sp.together(e)))))
S.append(("Fracciones algebraicas", [
 (2, r"Simplifica las siguientes fracciones algebraicas." + tasks(2, [r"$\dfrac{2x^2-8}{x^3+x^2-2x}$", r"$\dfrac{x^3-x}{x^3+3x^2+2x}$", r"$\dfrac{x^4-2x^3-3x^2}{x^4-9x^2}$", r"$\dfrac{x^3-3x^2+3x-1}{x^3-2x^2+x}$",
      r"$\dfrac{2x^4-5x^3+x^2+5x-3}{2x^3-x^2-7x+6}$", r"$\dfrac{2x^4+x^3-11x^2+11x-3}{2x^3+3x^2-8x+3}$", r"$\dfrac{x^3-2x^2-9x+18}{x^3-7x^2+16x-12}$", r"$\dfrac{x^4-5x^3+9x^2-7x+2}{x^4-6x^3+13x^2-12x+4}$"])
     + recorda(r"Factoriza el numerador y el denominador y simplifica solo los \emph{factores} comunes."),
     tasks(1, [simp(*f_) for f_ in F19])),
 (2, r"Efectúa las siguientes sumas y restas reduciendo previamente a común denominador:" + tasks(2, [r"$\dfrac{1}{x+1}+\dfrac{3}{x^2-1}$", r"$\dfrac{1}{x^2+x}+\dfrac{3}{x+1}$", r"$\dfrac{1}{2x}-\dfrac{3}{4x^2-4x}$",
      r"$\dfrac{1}{x^2+x}+\dfrac{3}{x^2-x}$", r"$\dfrac{2x}{x-2}+\dfrac{3x-1}{x+2}-\dfrac{1}{x^2-4}$", r"$\dfrac{1}{(x-1)^2}+\dfrac{2}{x-1}+\dfrac{1}{x^2-1}$"]),
     tasks(2, [res(e_) for e_ in E20])),
 (2, r"Opera y simplifica las fracciones algebraicas:" + tasks(2, [r"$\dfrac{3x+3}{12x-12}:\dfrac{(x+1)^2}{x^2-1}$", r"$\dfrac{x^2+2x-3}{(x-2)^3}\cdot\dfrac{(x-2)^2}{x^2-1}$", r"$\dfrac{6x+4}{x-2}\cdot\dfrac{4x+1}{2x+4}$",
      r"$\dfrac{-6x^2}{x^2+2x+1}\cdot\dfrac{x+1}{3x^3}\cdot\dfrac{x+1}{3x}$", r"$\left(\dfrac3x-\dfrac{2x}{x+1}\right)\cdot\dfrac{x^2+x}{x-1}$", r"$\dfrac{(x-1)^2}{2}\cdot\dfrac{1}{x^2-1}-\dfrac{3x}{(x+1)^2}$",
      r"$\left(\dfrac{2x-1}{x+1}-\dfrac{3x}{x-1}\right)\cdot\dfrac{x^3-x}{-x^2-6x+1}$"]),
     tasks(2, [res(e_) for e_ in E21])),
 (3, r"Calcula y simplifica el resultado de las operaciones siguientes:" + tasks(2, [r"$\dfrac{x+1}{x}+\dfrac{2x+1}{x+2}-\dfrac{x}{x^2+1}$", r"$\dfrac{1+\frac{2x+1}{x-1}}{\frac{1}{x-1}+\frac{x}{x+1}}$", r"$\dfrac{ba-a^2}{a^3b-ab^3}:\dfrac{b}{a^2+2ab+b^2}$",
      r"$\dfrac{a^2}{ab}+\dfrac{ab^2}{b^4}-a$", r"$\dfrac{6}{2+x}-\dfrac{4}{2-x}+\dfrac{16}{x^2-4}$", r"$\dfrac{2x^2-7x+6}{x^2+2x+1}\cdot\dfrac{x^2+6x+5}{2x-3}$",
      r"$(x^2-y^2):\left(\dfrac1x+\dfrac1y\right)$", r"$\dfrac{a+x}{x^2-a^2}\cdot\dfrac{x-a}{x+a}$", r"$1+\cfrac{1}{1+\cfrac{1}{1+\frac1x}}$", r"$1+\dfrac{\frac{2x+1}{x-1}}{\frac{1}{x-1}+\frac{x}{x+1}}$"]),
     tasks(2, [res(e_) for e_ in E22])),
]))

# =====================================================================
# 4. Equacions polinòmiques
def solve_r(e):
    return sp.solveset(e, xr, domain=sp.S.Reals)
def solT(Sset):
    vals = sorted(list(Sset), key=float)
    return r',\ '.join('x=' + L(v) for v in vals) if vals else r'\text{no tiene solución}'
E23 = [sp.Eq((2 * x - 3) / 4 + x / 2 - (3 * x - 1) / 5, 2 * x - 1), sp.Eq(2 * (3 * x - 2) + x * (x - 1), -4), sp.Eq((x + 1) ** 3 - (x - 1) ** 3, 7), sp.Eq((x ** 2 + 1) / 2 - (2 * x - 3) / 4 + x ** 2 / 6, Q(59, 12)),
       6 * x ** 4 + 13 * x ** 3 - 8 * x ** 2 - 17 * x + 6, 2 * x ** 4 - x ** 3 - 3 * x - 18, sp.Eq(6 * x ** 4 + 5 * x ** 3, 2 * x ** 2 + x), x ** 3 - 7 * x + 6, x ** 3 - 3 * x ** 2 - 9 * x + 27,
       x ** 4 - x ** 3 - 5 * x ** 2 - x - 6, x ** 4 - 1, x ** 4 + x ** 3 - 9 * x ** 2 - 9 * x]
def ex23(e):
    ex = (e.lhs - e.rhs) if isinstance(e, sp.Equality) else e
    f = sp.factor(ex); sol = solve_r(ex.subs(x, xr))
    pre = '' if f.is_polynomial(x) and sp.degree(sp.numer(sp.together(ex)), x) <= 2 else r'$' + L(f) + r'=0$: \ '
    return pre + R(solT(sol))
E24 = [x ** 4 - 17 * x ** 2 + 16, x ** 6 - 9 * x ** 3 + 8, x ** 4 - 8 * x ** 2 - 9, 4 * x ** 6 + 8 * x ** 3 - 12, 2 * (x + 1) ** 4 - 8 * x ** 3 - 8 * (x + 3) + 8, x ** 4 - 10 * x ** 2 + 9]
ck(sp.expand(E24[4]) == 2 * x ** 4 + 12 * x ** 2 - 14)
for e, sol in zip(E24, [{-4, -1, 1, 4}, {1, 2}, {-3, 3}, None, {-1, 1}, {-3, -1, 1, 3}]):
    if sol is not None: ck(set(solve_r(e.subs(x, xr))) == sol, '24 %s' % e)
eqn(E24[3], [1, -sp.cbrt(3)])
E25 = [(x ** 2 - 3) * (x ** 2 - 4), (3 * x + 2) * (x ** 2 - 4 * x) * (x ** 2 - 9), (x ** 2 - 4 * x + 4) * (x ** 2 + 6 * x + 9), (x - 2) ** 2 * (x + 1) ** 3 * (2 * x - 7)]
S.append(("Ecuaciones polinómicas", [
 (2, r"Resuelve las siguientes ecuaciones polinómicas:" + tasks(2, [r"$\dfrac{2x-3}{4}+\dfrac x2-\dfrac{3x-1}{5}=2x-1$", r"$2(3x-2)+x(x-1)=-4$", r"$(x+1)^3-(x-1)^3=7$", r"$\dfrac{x^2+1}{2}-\dfrac{2x-3}{4}+\dfrac{x^2}{6}=\dfrac{59}{12}$",
      r"$6x^4+13x^3-8x^2-17x+6=0$", r"$2x^4-x^3-3x-18=0$", r"$6x^4+5x^3=2x^2+x$", r"$x^3-7x+6=0$", r"$x^3-3x^2-9x+27=0$", r"$x^4-x^3-5x^2-x-6=0$", r"$x^4-1=0$", r"$x^4+x^3-9x^2-9x=0$"])
     + recorda(r"Pásalo todo a un miembro y factoriza (factor común, Ruffini…): un producto vale cero si algún factor vale cero."),
     tasks(1, [ex23(e_) for e_ in E23])),
 (2, r"Resuelve las siguientes ecuaciones bicuadradas (o que se resuelven con un cambio de variable):" + tasks(2, [r"$x^4-17x^2+16=0$", r"$x^6-9x^3+8=0$", r"$x^4-8x^2-9=0$", r"$4x^6+8x^3-12=0$", r"$2(x+1)^4-8x^3-8(x+3)+8=0$", r"$\dfrac{9}{x^2}=10-x^2$"]),
     tasks(1, [r"$t=x^2$: $t^2-17t+16=0\Rightarrow t=16,\ t=1$: \ " + R(r"x=\pm4,\ x=\pm1"), r"$t=x^3$: $t^2-9t+8=0\Rightarrow t=8,\ t=1$: \ " + R(r"x=2,\ x=1"), r"$t^2-8t-9=0\Rightarrow t=9$ ($t=-1$ no da soluciones): \ " + R(r"x=\pm3"), r"$t=x^3$: $t^2+2t-3=0\Rightarrow t=1,\ t=-3$: \ " + R(r"x=1,\ x=-\sqrt[3]{3}"), r"Desarrollando: $2x^4+12x^2-14=0\Rightarrow t^2+6t-7=0\Rightarrow t=1$ ($t=-7$ no da soluciones): \ " + R(r"x=\pm1"), r"Multiplicamos por $x^2$: $x^4-10x^2+9=0\Rightarrow t=9,\ t=1$: \ " + R(r"x=\pm3,\ x=\pm1")])),
 (1, r"Resuelve las siguientes ecuaciones factorizadas:" + tasks(2, [r"$(x^2-3)(x^2-4)=0$", r"$(3x+2)(x^2-4x)(x^2-9)=0$", r"$(x^2-4x+4)(x^2+6x+9)=0$", r"$(x-2)^2(x+1)^3(2x-7)=0$"]),
     tasks(2, [R(solT(solve_r(e_.subs(x, xr)))) for e_ in E25])),
]))

# =====================================================================
# 5. Equacions racionals
E26 = [sp.Eq(1 / x + 1 / x ** 2 + 1 / x ** 3, Q(7, 8)), sp.Eq(2 * x / 3 + (2 * x + 3) / (x - 1), 11 / (3 * x - 3)), sp.Eq(2 * x / (x - 2) + 3 * x / (x + 2), 6 * x ** 2 / (x ** 2 - 4)),
       sp.Eq(3 / (x ** 2 - 6 * x + 8) + (x - 5) / (x ** 2 - 5 * x + 4), 1 / (x - 4)), sp.Eq(x / sqrt(2) + sqrt(2) / x, sqrt(2) * x), sp.Eq(x / (x - 2) + 2 * x / (2 - x), -x),
       sp.Eq((1 + (x + 1) / (x - 1)) / (2 - (x - 1) / (x + 1)), 2)]
X26 = [[2], [-1 + sqrt(2), -1 - sqrt(2)], [0], [5], [sqrt(2), -sqrt(2)], [0, 3], [3]]
for e, sols in zip(E26, X26):
    ck(set(solve_r((e.lhs - e.rhs).subs(x, xr))) == set(sols), '26 %s' % e)
ck(sp.simplify(1 / (1 - 1 / (x + 1)) - (x + 1) / x) == 0)
S.append(("Ecuaciones racionales", [
 (2, r"Resuelve las ecuaciones racionales siguientes:" + tasks(2, [r"$\dfrac1x+\dfrac1{x^2}+\dfrac1{x^3}=\dfrac78$", r"$\dfrac{2x}{3}+\dfrac{2x+3}{x-1}=\dfrac{11}{3x-3}$", r"$\dfrac{2x}{x-2}+\dfrac{3x}{x+2}=\dfrac{6x^2}{x^2-4}$", r"$\dfrac{3}{x^2-6x+8}+\dfrac{x-5}{x^2-5x+4}=\dfrac{1}{x-4}$", r"$\dfrac{x}{\sqrt2}+\dfrac{\sqrt2}{x}=\sqrt2\,x$", r"$\dfrac{x}{x-2}+\dfrac{2x}{2-x}=-x$", r"$\dfrac{1+\frac{x+1}{x-1}}{2-\frac{x-1}{x+1}}=2$", r"$\dfrac{1}{1-\frac{1}{x+1}}=\dfrac{x+1}{x}$"])
     + recorda(r"Multiplica por el m.c.m. de los denominadores y, al final, descarta las soluciones que anulan algún denominador."),
     tasks(1, [r"$8x^2+8x+8=7x^3\Rightarrow(x-2)(7x^2+6x+4)=0$ ($\Delta\lt0$): \ " + R("x=2"), r"Multiplicamos por $3(x-1)$: $2x^2+4x+9=11\Rightarrow x^2+2x-1=0$: \ " + R(r"x=-1\pm\sqrt2"), r"$2x(x+2)+3x(x-2)=6x^2\Rightarrow x^2+2x=0\Rightarrow x=0,\ x=-2$; \ $x=-2$ anula un denominador: \ " + R("x=0"), r"m.c.m. $=(x-1)(x-2)(x-4)$: $3(x-1)+(x-5)(x-2)=(x-1)(x-2)\Rightarrow x^2-4x+7=x^2-3x+2$: \ " + R("x=5"), r"Multiplicamos por $\sqrt2\,x$: $x^2+2=2x^2\Rightarrow$ " + R(r"x=\pm\sqrt2"), r"$-\dfrac{x}{x-2}=-x\Rightarrow x=x(x-2)\Rightarrow x^2-3x=0$: \ " + R(r"x=0,\ x=3"), r"Simplificando: $\dfrac{2x(x+1)}{(x-1)(x+3)}=2\Rightarrow x^2+x=x^2+2x-3$: \ " + R("x=3"), r"El primer miembro es $\dfrac{x+1}{x}$: es una \rest{identidad}, se cumple para todo $x\neq0,\ x\neq-1$."])),
]))

# =====================================================================
# 6. Equacions amb radicals (comprovacions numèriques amb arrels reals)
def cbrt(v): return math.copysign(abs(v) ** (1 / 3), v)
def okf(f, vs, bad=()):
    for v in vs: ck(abs(f(float(v))) < 1e-9, 'rad ok %s' % v)
    for v in bad:
        try: r = f(float(v)); ck(abs(r) > 1e-6, 'rad bad %s' % v)
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
okf(lambda t: cbrt(t * t - 1) + 1 - t, [0, 1, 3])
okf(lambda t: sq(3 * t + 7) / cbrt(t + 1) - cbrt(t * t + 2 * t + 1), [3], [-2])
okf(lambda t: cbrt(4 * t - 1) - (t - 4), [7])
okf(lambda t: cbrt(4 - 2 * t) - (8 * t * t - 16 * t) ** (1 / 6), [2, -2])
okf(lambda t: sq(2 * t + 2) - (6 * t + 10) ** 0.25, [1])
okf(lambda t: sq(t + 1) - 2 * sq(t - 11), [15])
ck(sp.factor(x ** 3 - 12 * x ** 2 + 44 * x - 63) == (x - 7) * (x ** 2 - 5 * x + 9))
S.append(("Ecuaciones con radicales", [
 (2, r"Resuelve las siguientes ecuaciones con radicales:" + tasks(2, [r"$-\sqrt{2x-3}+1=x$", r"$x+\sqrt{2x^2+2x-3}=-1$", r"$\sqrt{\dfrac{7x+1}{4}}=\dfrac{5x-7}{6}$", r"$\dfrac{\sqrt{2x-1}}{4}=\dfrac{3}{\sqrt{2x-1}}$", r"$\sqrt{2-5x}+x\sqrt3=0$", r"$\sqrt{2+\sqrt{x-4}}=\sqrt{12-x}$", r"$\sqrt x+\sqrt{x-4}=2$", r"$\sqrt{x+5}+\sqrt{2x+8}=7$", r"$\sqrt{x+4}+\sqrt{x-1}=5$", r"$\sqrt{x-7}+\sqrt{2x}=\sqrt{x+1}$", r"$\sqrt{1-4x}-2\sqrt{3+x}=\sqrt{3+x}$"])
     + recorda(r"Aísla un radical, eleva al cuadrado y repite si hace falta. Comprueba \emph{siempre} las soluciones en la ecuación inicial."),
     tasks(1, [r"$2x-3=(1-x)^2\Rightarrow(x-2)^2=0$; \ $x=2$: $-1+1=0\neq2$: \ " + R(r"\text{no tiene solución}"), r"$2x^2+2x-3=(x+1)^2\Rightarrow x^2=4$; \ $x=2$ no vale ($-1-2\lt0$): \ " + R("x=-2"), r"$9(7x+1)=(5x-7)^2\Rightarrow25x^2-133x+40=0\Rightarrow x=5,\ x=\frac{8}{25}$; \ $x=\frac8{25}$ no vale: \ " + R("x=5"), r"$2x-1=12$: \ " + R(r"x=\frac{13}{2}"), r"$2-5x=3x^2\Rightarrow3x^2+5x-2=0\Rightarrow x=-2,\ x=\frac13$; \ $x=\frac13$ no vale: \ " + R("x=-2"), r"$2+\sqrt{x-4}=12-x\Rightarrow x-4=(10-x)^2\Rightarrow x^2-21x+104=0\Rightarrow x=8,\ x=13$; \ $x=13$ no vale: \ " + R("x=8"), r"$x=4-4\sqrt{x-4}+x-4\Rightarrow\sqrt{x-4}=0$: \ " + R("x=4"), r"$x-46=-14\sqrt{x+5}\Rightarrow x^2-288x+1136=0\Rightarrow x=4,\ x=284$; \ $x=284$ no vale: \ " + R("x=4"), r"$10\sqrt{x-1}=20\Rightarrow\sqrt{x-1}=2$: \ " + R("x=5"), r"$2\sqrt{2x^2-14x}=8-2x\Rightarrow x^2-6x-16=0\Rightarrow x=8,\ x=-2$; ninguna vale: \ " + R(r"\text{no tiene solución}"), r"$\sqrt{1-4x}=3\sqrt{3+x}\Rightarrow1-4x=27+9x$: \ " + R("x=-2")])),
 (2, r"Resuelve las siguientes ecuaciones con radicales no cuadráticos:" + tasks(2, [r"$\sqrt[3]{x^2-1}+1=x$", r"$\dfrac{\sqrt{3x+7}}{\sqrt[3]{x+1}}=\sqrt[3]{x^2+2x+1}$", r"$\sqrt[3]{4x-1}=x-4$", r"$\sqrt[3]{4-2x}=\sqrt[6]{8x^2-16x}$", r"$\sqrt{2x+2}-\sqrt[4]{6x+10}=0$"])
     + recorda(r"Eleva los dos miembros al índice de la raíz (o al m.c.m. de los índices)."),
     tasks(1, [r"$x^2-1=(x-1)^3\Rightarrow x(x-1)(x-3)=0$; todas valen ($\sqrt[3]{-1}=-1$): \ " + R(r"x=0,\ x=1,\ x=3"), r"$\sqrt{3x+7}=x+1\Rightarrow x^2-x-6=0\Rightarrow x=3,\ x=-2$; \ $x=-2$ no vale: \ " + R("x=3"), r"$4x-1=(x-4)^3\Rightarrow(x-7)(x^2-5x+9)=0$: \ " + R("x=7"), r"$(4-2x)^2=8x^2-16x\Rightarrow4x^2=16$; las dos valen: \ " + R(r"x=2,\ x=-2"), r"$(2x+2)^2=6x+10\Rightarrow2x^2+x-3=0\Rightarrow x=1,\ x=-\frac32$; \ $x=-\frac32$ no vale: \ " + R("x=1")])),
 (2, r"Calcula el valor de un número tal que, si se le suma una unidad y después se extrae la raíz cuadrada, se obtiene el doble que al restarle 11 unidades y extraer la raíz cuadrada.",
     r"$\sqrt{x+1}=2\sqrt{x-11}\Rightarrow x+1=4x-44$: \ " + R("x=15") + r" \ (comprobación: $\sqrt{16}=4=2\sqrt4$)."),
]))

# =====================================================================
# 7. Equacions logarítmiques
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
okf(lambda t: math.log(9) / math.log(t + 3) - math.log(3) / math.log(5), [22])
okf(lambda t: math.log(32, 3) + math.log(6 - t, 1 / 3) - math.log(t, math.sqrt(3)), [4])
okf(lambda t: lg(t) + lg(2) - 1, [5]); okf(lambda t: 2 * lg(t) - lg(4) - lg(9), [6])
S.append(("Ecuaciones logarítmicas", [
 (2, r"Resuelve las siguientes ecuaciones logarítmicas:" + tasks(2, [r"$\log2+\log(x+3)=\log(x+5)$", r"$\log(15-2x)=2\log x$", r"$\log(2x+3)-\log(x-1)=2\log2+2\log3$", r"$\frac12\log(x^2-3x+2)=\log x$", r"$\log\left(\dfrac{2x-2}{x}\right)=2\log(x-1)-\log x$", r"$2\log x=\log\dfrac x2-1$", r"$\log(4-5x)+\log(2x)=\log(2x-x^2)+\log3$", r"$\log_2(5x^2+15x+10)-\log_2(x+2)=2$", r"$\dfrac{\log(4-x)}{\log(x+2)}=2$", r"$\log_{x+3}9=\log_53$", r"$\log_332+\log_{\frac13}(6-x)=\log_{\sqrt3}x$"])
     + recorda(r"Agrupa los logaritmos con las propiedades hasta llegar a $\log A=\log B$ (y entonces $A=B$). Comprueba que todos los argumentos son positivos."),
     tasks(1, [r"$2(x+3)=x+5$: \ " + R("x=-1"), r"$15-2x=x^2\Rightarrow x=3,\ x=-5$; \ $x=-5$ no vale: \ " + R("x=3"), r"$\dfrac{2x+3}{x-1}=36\Rightarrow34x=39$: \ " + R(r"x=\frac{39}{34}"), r"$x^2-3x+2=x^2\Rightarrow$ " + R(r"x=\frac23") + r" (vale: $x\gt0$ y $x^2-3x+2=\frac49\gt0$)", r"$\dfrac{2x-2}{x}=\dfrac{(x-1)^2}{x}\Rightarrow(x-1)(x-3)=0$; \ $x=1$ no vale: \ " + R("x=3"), r"$\log x^2=\log\dfrac{x}{20}\Rightarrow x^2=\dfrac x{20}$; \ $x=0$ no vale: \ " + R(r"x=\frac1{20}"), r"$2x(4-5x)=3(2x-x^2)\Rightarrow7x^2-2x=0$; \ $x=0$ no vale: \ " + R(r"x=\frac27"), r"$\dfrac{5(x+1)(x+2)}{x+2}=4\Rightarrow5x+5=4$: \ " + R(r"x=-\frac15"), r"$4-x=(x+2)^2\Rightarrow x^2+5x=0$; \ $x=-5$ no vale: \ " + R("x=0"), r"Cambio de base: $\dfrac{2\log3}{\log(x+3)}=\dfrac{\log3}{\log5}\Rightarrow\log(x+3)=2\log5\Rightarrow x+3=25$: \ " + R("x=22"), r"En base 3: $\log_332-\log_3(6-x)=2\log_3x\Rightarrow x^2(6-x)=32\Rightarrow(x+2)(x-4)^2=0$: \ " + R("x=4")])),
 (1, r"Halla el número que cumple que, al añadir a su logaritmo decimal el logaritmo decimal de 2, el resultado es 1.", r"$\log x+\log2=1\Rightarrow\log(2x)=\log10$: \ " + R("x=5")),
 (1, r"Calcula el valor de un número sabiendo que el doble de su logaritmo decimal es igual a la suma de los logaritmos decimales de 4 y de 9.", r"$2\log x=\log4+\log9\Rightarrow x^2=36$ ($x\gt0$): \ " + R("x=6")),
]))
ck(sp.factor(x ** 3 - 6 * x ** 2 + 32) == (x - 4) ** 2 * (x + 2))

# =====================================================================
# 8. Equacions exponencials
ex = math.exp
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
okf(lambda t: 9 ** t + 3 ** (2 * t - 1) + 3 ** (t - 1) - 111, [2])
okf(lambda t: 3 ** (t + 2) + 9 ** (t - 1) - 90, [2])
okf(lambda t: 2 ** (2 * t - 4) - 5 * 2 ** (t - 3) + 1, [1, 3])
okf(lambda t: 9 ** (t + 2) + 3 ** (t + 3) - 810, [1])
okf(lambda t: 4 ** (t + 1) + 2 ** (t + 3) - 320, [3])
S.append(("Ecuaciones exponenciales", [
 (2, r"Resuelve las siguientes ecuaciones exponenciales:" + tasks(2, [r"$4^{x^2+1}=2^{5x+5}$", r"$4^{(x-2)^2}=262144$", r"$3^{x+4}=5$", r"$\dfrac{1}{2^x}=16^{\frac{x(x-1)}{2}}$", r"$13^{x^2+2x}-\dfrac1{13}=0$", r"$2^{2x^2-4x-2}=16$", r"$2\cdot6^{4x-3}=24$", r"$3\cdot2^x=2\cdot3^x$", r"$\sqrt[x]{27}=3^{x+2}$", r"$2^{x+4}-8^x=0$", r"$7^{x^2-5x+6}=1$", r"$49^{\frac{x-5}{3}}=\dfrac{1}{\sqrt{7^{x-1}}}$"])
     + recorda(r"Si puedes, escribe los dos miembros con la misma base e iguala los exponentes; si no, toma logaritmos."),
     tasks(1, [r"$2^{2x^2+2}=2^{5x+5}\Rightarrow2x^2-5x-3=0$: \ " + R(r"x=3,\ x=-\frac12"), r"$262144=4^9\Rightarrow(x-2)^2=9$: \ " + R(r"x=5,\ x=-1"), r"$x+4=\dfrac{\log5}{\log3}$: \ " + R(r"x=\frac{\log5}{\log3}-4\approx" + dec(math.log(5) / math.log(3) - 4)), r"$2^{-x}=2^{2x(x-1)}\Rightarrow2x^2-x=0$: \ " + R(r"x=0,\ x=\frac12"), r"$13^{x^2+2x}=13^{-1}\Rightarrow(x+1)^2=0$: \ " + R("x=-1"), r"$2x^2-4x-2=4\Rightarrow x^2-2x-3=0$: \ " + R(r"x=3,\ x=-1"), r"$6^{4x-3}=12\Rightarrow4x-3=\dfrac{\log12}{\log6}$: \ " + R(r"x=\frac{3+\log_612}{4}\approx" + dec(1 + math.log(2) / (4 * math.log(6)))), r"$\left(\dfrac32\right)^x=\dfrac32$: \ " + R("x=1"), r"$3^{3/x}=3^{x+2}\Rightarrow x^2+2x-3=0$: \ " + R(r"x=1,\ x=-3"), r"$2^{x+4}=2^{3x}\Rightarrow x+4=3x$: \ " + R("x=2"), r"$x^2-5x+6=0$: \ " + R(r"x=2,\ x=3"), r"$7^{\frac{2(x-5)}{3}}=7^{-\frac{x-1}{2}}\Rightarrow4(x-5)=-3(x-1)$: \ " + R(r"x=\frac{23}{7}")])),
 (2, r"Resuelve las siguientes ecuaciones exponenciales:" + tasks(2, [r"$2^{x+1}+2^x+2^{x-1}=28$", r"$5^{x+3}-5^{x-1}-3120=0$", r"$4^x+4^{x-1}+4^{x-2}=336$", r"$3^{x+2}+3^{x+1}+3^x+3^{x-1}=120$", r"$2^{x-1}+2^{x-2}+2^{x-3}+2^{x-4}=960$", r"$6^x-9\cdot6^{-x}+8=0$"])
     + recorda(r"Descompón las potencias ($a^{x+1}=a\cdot a^x$, $a^{x-1}=\frac{a^x}{a}$) y saca factor común $a^x$."),
     tasks(1, [r"$2^x\left(2+1+\frac12\right)=28\Rightarrow2^x=8$: \ " + R("x=3"), r"$5^x\left(125-\frac15\right)=3120\Rightarrow5^x=25$: \ " + R("x=2"), r"$4^x\cdot\frac{21}{16}=336\Rightarrow4^x=256$: \ " + R("x=4"), r"$3^x\left(9+3+1+\frac13\right)=120\Rightarrow3^x=9$: \ " + R("x=2"), r"$2^x\cdot\frac{15}{16}=960\Rightarrow2^x=1024$: \ " + R("x=10"), r"$t=6^x$: $t^2+8t-9=0\Rightarrow t=1$ ($t=-9$ no vale): \ " + R("x=0")])),
 (3, r"Resuelve las siguientes ecuaciones exponenciales:" + tasks(2, [r"$3^{2x}-3^{x-1}=3^{x+1}-1$", r"$2\cdot10^{2x+4}+3\cdot10^{x+2}-5=0$", r"$9^x+5\cdot3^x-24=0$", r"$9^x+3^{2x-1}+3^{x-1}=111$", r"$3^{x+2}+9^{x-1}=90$", r"$2^{2x-4}-5\cdot2^{x-3}+1=0$", r"$9^{x+2}+3^{x+3}-810=0$", r"$4^{x+1}+2^{x+3}=320$"])
     + recorda(r"Si hay $a^{2x}$ y $a^x$, haz el cambio $t=a^x$; las soluciones $t\le0$ no valen."),
     tasks(1, [r"$t=3^x$: $3t^2-10t+3=0\Rightarrow t=3,\ t=\frac13$: \ " + R(r"x=1,\ x=-1"), r"$t=10^{x+2}$: $2t^2+3t-5=0\Rightarrow t=1$ ($t=-\frac52$ no vale) $\Rightarrow x+2=0$: \ " + R("x=-2"), r"$t=3^x$: $t^2+5t-24=0\Rightarrow t=3$ ($t=-8$ no vale): \ " + R("x=1"), r"$t=3^x$: $t^2+\frac{t^2}{3}+\frac t3=111\Rightarrow4t^2+t-333=0\Rightarrow t=9$: \ " + R("x=2"), r"$t=3^x$: $9t+\frac{t^2}{9}=90\Rightarrow t^2+81t-810=0\Rightarrow t=9$ ($t=-90$ no vale): \ " + R("x=2"), r"$t=2^x$: $\frac{t^2}{16}-\frac{5t}{8}+1=0\Rightarrow t^2-10t+16=0\Rightarrow t=8,\ t=2$: \ " + R(r"x=3,\ x=1"), r"$t=3^x$: $81t^2+27t-810=0\Rightarrow3t^2+t-30=0\Rightarrow t=3$ ($t=-\frac{10}{3}$ no vale): \ " + R("x=1"), r"$t=2^x$: $4t^2+8t-320=0\Rightarrow t^2+2t-80=0\Rightarrow t=8$ ($t=-10$ no vale): \ " + R("x=3")])),
]))
for P_, rts in [(3 * x ** 2 - 10 * x + 3, {3, Q(1, 3)}), (x ** 2 + 81 * x - 810, {9, -90}), (2 * x ** 2 + 3 * x - 5, {1, Q(-5, 2)}), (x ** 2 - 10 * x + 16, {8, 2}), (x ** 2 + 5 * x - 24, {3, -8}),
                (3 * x ** 2 + x - 30, {3, Q(-10, 3)}), (4 * x ** 2 + x - 333, {9, Q(-37, 4)}), (x ** 2 + 2 * x - 80, {8, -10}), (x ** 2 + 8 * x - 9, {1, -9})]:
    ck(set(sp.solve(P_, x)) == rts, 'exp %s' % P_)

# =====================================================================
# 9. Problemes d'equacions
t_ = sp.symbols('t')
def one(eq, val, var=x):
    sols = sp.solve(eq, var); ck(val in sols, 'prob %s -> %s' % (eq, sols)); return val
one(5 * x + 2 * 50 - 4 * (x + 100), 300); one(30 * 5 + 10 * x - 7 * (30 + x), 20); one(18 * x + 14 * (1 - x) - Q(82, 5), Q(3, 5))
one(Q(1, 10) * x - 15, 150); one(Q(3, 4) * Q(1, 5) * x - 18000, 120000); one(Q(15, 100) * x - 3, 20); one(5 * x - 2 * (20 - x) - 58, 14)
one(x ** 2 - 75 * x - 6250, 125); one(x ** 2 + (x + 1) ** 2 - 25, 3); one(x ** 2 + (x + 2) ** 2 - (x + 4) ** 2, 6); one(x ** 2 + (70 - x) ** 2 - 2500, 40)
ck(Q(1, 5) + Q(1, 20) == Q(1, 4) and Q(1, 2) + Q(1, 3) == Q(5, 6) and Q(1, 10) + Q(1, 20) + Q(1, 30) + Q(1, 40) + Q(1, 50) == Q(137, 600))
one(1 / x + 1 / (2 * x) - Q(1, 10), 15); one(x ** 2 - 10 * x - 1200, 40)
ck(abs(5 * math.log(4) - 6.931) < 1e-3 and abs(27 * math.exp(-1) - 9.933) < 1e-3 and abs(math.log2(100 / 9) - 3.474) < 1e-3)
Kk, aa = sp.symbols('K a', positive=True)
ck(sp.solve([1 + Kk * aa - 4, 1 + Kk * aa ** 2 - Q(5, 2)], [Kk, aa], dict=True) == [{Kk: 6, aa: Q(1, 2)}])
ck(abs(10 * math.log2(18) - 41.70) < 0.01)
S.append(("Problemas de ecuaciones", [
 (2, r"Un comerciante tiene un tonel de vino de la clase A de precio 5\,€/L. Añade 50 litros de vino de la clase B de 2\,€/L y 50 litros de agua y la mezcla resulta a 4\,€/L. ¿Cuántos litros de la clase A tenía el tonel?",
     r"$5x+2\cdot50+0\cdot50=4(x+100)\Rightarrow$ " + R(r"x=300\ \text{L}")),
 (1, r"Tenemos 30 litros de vino a 5\,€/L y queremos añadirle vino de 10\,€/L para obtener una mezcla que salga a 7\,€/L. ¿Cuántos litros tenemos que añadir?", r"$30\cdot5+10x=7(30+x)\Rightarrow3x=60$: \ " + R(r"20\ \text{L}")),
 (2, r"En una tienda se vende té blanco a 18\,€/kg y té verde a 14\,€/kg. También se vende una mezcla de los dos a 16,4\,€/kg. ¿Cuál es la composición de la mezcla?",
     r"En 1 kg, $x$ kg de té blanco: $18x+14(1-x)=16,4\Rightarrow x=0,6$: \ " + R(r"60\,\%\ \text{blanco y }40\,\%\ \text{verde}")),
 (1, r"En un colegio hay tres cursos. El 60\,\% de los alumnos estudia primero, el 30\,\% estudia segundo y el resto, que son 15 alumnos, estudia tercero. ¿Cuántos alumnos hay en el colegio?",
     r"El 10\,\% son 15: \ " + R(r"150\ \text{alumnos}")),
 (2, r"El 80\,\% de las entradas de un partido se reservaron para los socios del club; de las restantes, el 25\,\% se enviaron a los socios del club contrario y las demás, 18\,000, se pusieron a la venta. ¿Cuántas entradas había?",
     r"A la venta queda el $75\,\%$ del $20\,\%$, es decir, el $15\,\%$: $0,15x=18\,000\Rightarrow$ " + R(r"120\,000\ \text{entradas}")),
 (1, r"Una fábrica exporta el 30\,\% de la producción a Asia, el 40\,\% a Europa, el 15\,\% a América y el resto, que supone una facturación de 3 millones de euros, a África. ¿Cuál es la facturación total?",
     r"África es el 15\,\%: $0,15x=3\Rightarrow$ " + R(r"20\ \text{millones de euros}")),
 (2, r"Un examen consta de 20 preguntas. Cada acierto suma 5 puntos y cada error resta 2 puntos. Una alumna sacó 58 puntos. ¿Cuántas preguntas acertó y cuántas falló, si no se puede dejar ninguna sin contestar?",
     r"$5x-2(20-x)=58\Rightarrow7x=98$: \ " + R(r"14\ \text{aciertos y }6\ \text{errores}")),
 (3, r"Un tendero invierte 125\,€ en la compra de una partida de manzanas. Desecha 20 kilos por defectuosas y vende el resto por 147\,€, ganando 0,40\,€ por kilo sobre el precio de compra. ¿Cuántos kilos compró?",
     r"$(x-20)\left(\dfrac{125}{x}+0,4\right)=147\Rightarrow x^2-75x-6250=0\Rightarrow x=125$ ($x=-50$ no tiene sentido): \ " + R(r"125\ \text{kg}")),
 (1, r"Calcula la base y la altura de un triángulo rectángulo si son números enteros consecutivos y la hipotenusa mide 5 cm.", r"$x^2+(x+1)^2=25\Rightarrow x^2+x-12=0\Rightarrow x=3$: \ " + R(r"3\ \text{cm y }4\ \text{cm}")),
 (2, r"Calcula la longitud de los tres lados de un triángulo rectángulo si son números pares consecutivos.", r"$x^2+(x+2)^2=(x+4)^2\Rightarrow x^2-4x-12=0\Rightarrow x=6$: \ " + R(r"6,\ 8\ \text{y }10\ \text{cm}")),
 (2, r"Calcula las dimensiones de una finca rectangular si el perímetro mide 140 m y la diagonal 50 m.", r"$x+y=70,\ x^2+y^2=2500\Rightarrow x^2-70x+1200=0$: \ " + R(r"40\ \text{m}\times30\ \text{m}")),
 (1, r"Una balsa tarda 5 horas en llenarse con la toma de agua habitual y 20 horas con una manguera. ¿Cuánto tiempo hace falta si usamos los dos métodos a la vez?", r"$\frac15+\frac1{20}=\frac14$: \ " + R(r"T=4\ \text{h}")),
 (1, r"Un hombre tarda 2 horas en barrer una casa y otro tarda 3. ¿Cuánto tardarían trabajando juntos?", r"$\frac12+\frac13=\frac56\Rightarrow T=\frac65$ h: \ " + R(r"1\ \text{h}\ 12\ \text{min}")),
 (2, r"Dos personas trabajando juntas tardan 10 horas en hacer un trabajo, pero una trabaja el doble de rápido que la otra. ¿Cuánto tardaría cada una por separado?",
     r"$\dfrac1t+\dfrac1{2t}=\dfrac1{10}\Rightarrow t=15$: \ " + R(r"15\ \text{h y }30\ \text{h}")),
 (2, r"Una piscina se puede llenar con 5 fuentes que, por separado, tardan 10, 20, 30, 40 y 50 horas respectivamente. ¿Cuánto tardarán las cinco juntas?",
     r"$\frac1{10}+\frac1{20}+\frac1{30}+\frac1{40}+\frac1{50}=\frac{137}{600}\Rightarrow T=\frac{600}{137}\approx" + R(r"4,38\ \text{h}\approx4\ \text{h}\ 23\ \text{min}").strip('$') + "$"),
 (3, r"Un grupo de personas contrata un autobús por 600\,€ a pagar a partes iguales; al final 10 personas no pueden ir al viaje y cada persona que va tiene que pagar 5\,€ más. ¿Cuántas personas iban inicialmente?",
     r"$\dfrac{600}{x-10}=\dfrac{600}{x}+5\Rightarrow x^2-10x-1200=0\Rightarrow x=40$: \ " + R(r"40\ \text{personas}")),
 (2, r"El número de enfermos de gripe en una ciudad a lo largo del pasado enero viene dado por $y(t)=100+200\cdot e^{0,2t}$, donde $t$ son los días transcurridos desde el 1 de enero." + tasks(1, ["¿Cuántos enfermos había el 1 de enero?", "¿Qué día el número de enfermos era de 900?"]),
     tasks(1, [R(r"y(0)=300\ \text{enfermos}"), r"$200e^{0,2t}=800\Rightarrow t=5\ln4\approx6,93$: \ " + R(r"\text{el 7 de enero (hacia el final del día)}")])),
 (2, r"La cantidad que queda de una sustancia radiactiva después de $t$ días es $q(t)=M\cdot e^{-0,1t}$." + tasks(1, ["¿Después de cuánto tiempo la masa se habrá reducido a la mitad?", "Si la masa inicial es de 27 mg, ¿cuánta sustancia quedará después de 10 días?"]),
     tasks(1, [r"$e^{-0,1t}=\frac12\Rightarrow t=10\ln2\approx" + R(r"6,93\ \text{días}").strip('$') + "$", r"$27e^{-1}\approx" + R(r"9,93\ \text{mg}").strip('$') + "$"])),
 (2, r"Si inicialmente hay $n$ bacterias en un cultivo y el número se duplica cada hora, después de $t$ horas hay $N=n\cdot2^t$. Si inicialmente hay 4500, ¿cuánto tiempo tardará el cultivo en llegar a 50\,000 bacterias?",
     r"$2^t=\dfrac{100}{9}\Rightarrow t=\dfrac{\log(100/9)}{\log2}\approx" + R(r"3,47\ \text{h}\approx3\ \text{h}\ 28\ \text{min}").strip('$') + "$"),
 (3, r"La biomasa $C$ (en kg) por unidad de superficie de una región sigue la función $C(x)=\dfrac{4}{1+K\cdot a^{x/10}}$, con $x\ge0$ el tiempo en años." + tasks(1, [r"Calcula $K$ y $a$ para que a los 10 años haya 1 kg de biomasa y a los 20 años, 1,6 kg.", "¿Cuántos años tienen que pasar para que la biomasa sea de 3 kg?"]),
     tasks(1, [r"$1+Ka=4$, \ $1+Ka^2=2,5\Rightarrow Ka=3,\ Ka^2=1,5$: \ " + R(r"a=\frac12,\ K=6"), r"$1+6\cdot0,5^{x/10}=\frac43\Rightarrow0,5^{x/10}=\frac1{18}\Rightarrow x=10\log_218\approx" + R(r"41,7\ \text{años}").strip('$') + "$"])),
]))

# =====================================================================
# 10. Inequacions amb una incògnita
I62 = [(xr - 3) / 2 - (xr - 2) / 8 <= xr / 2, 2 * xr - 3 - xr / 2 > xr + (3 * xr + 1) / 6, xr + 2 * (xr + 1) + 3 * (xr + 2) < (xr + 38) / 2, (xr ** 2 - 1) / 2 - (3 * xr - 2) / 3 <= (xr + 1) ** 2 / 6]
I63 = [-2 * xr ** 3 + 3 * xr > 0, 3 * xr ** 2 + xr - 24 >= 0, xr ** 3 - 4 * xr > 0, xr ** 3 + xr ** 2 - xr - 1 <= 0, 3 * xr * (2 * xr - 1) + xr ** 2 >= 5 * xr - 1, -xr ** 3 - 2 * xr ** 2 + xr + 2 <= 0, xr ** 4 - 1 > 0, (xr - 1) * (xr + 4) < -6]
I64 = [(5 * xr - 2) / (2 * xr + 1) >= 0, (xr ** 2 - xr - 2) / (xr ** 2 + xr - 2) >= 0, (4 * xr - 5) / (4 * xr ** 2 - xr - 5) < 0, xr ** 3 / (xr - 9) >= 0, (xr ** 2 + 4 * xr - 5) / (xr ** 3 - xr) >= 0, (2 * xr + 3) / (xr ** 3 + 1) >= 0]
ck(-8 + 4 - 2 <= 6 and not (1 / math.e + math.log(1 / math.e) >= 0) and 2 ** -0.5 - 0.5 - 2 < 3 ** -0.5)
def fac(e):
    d = e.lhs - e.rhs if not isinstance(e, sp.core.relational.Relational) or True else e
    n_, d_ = sp.fraction(sp.together(e.lhs - e.rhs))
    return L(sp.factor(n_)) if d_ == 1 else r'\dfrac{%s}{%s}' % (L(sp.factor(n_)), L(sp.factor(d_)))
OPS = {sp.StrictLessThan: r'\lt', sp.LessThan: r'\le', sp.StrictGreaterThan: r'\gt', sp.GreaterThan: r'\ge'}
def RIf(e): return r'$' + fac(e).replace('x', 'x') + OPS[type(e)] + r'0$: \ ' + RI(ineq(e))
S.append(("Inecuaciones con una incógnita", [
 (1, r"Comprueba si los números reales indicados pertenecen a la solución de las inecuaciones correspondientes:" + tasks(1, [r"$x=-2$ de la inecuación $x^3+x^2+x\le6$", r"$x=\dfrac1e$ de la inecuación $x+\ln x\ge0$", r"$x=-0,5$ de la inecuación $2^x+x-2\lt3^x$"]),
     tasks(1, [r"$-8+4-2=-6\le6$: \rest{sí}", r"$\frac1e-1\approx-0,63\not\ge0$: \rest{no}", r"$2^{-0,5}-2,5\approx-1,79\lt3^{-0,5}\approx0,58$: \rest{sí}"])),
 (1, r"Resuelve las siguientes inecuaciones:" + tasks(2, [r"$\dfrac{x-3}{2}-\dfrac{x-2}{8}\le\dfrac x2$", r"$2x-3-\dfrac x2\gt x+\dfrac{3x+1}{6}$", r"$x+2(x+1)+3(x+2)\lt\dfrac{x+38}{2}$", r"$\dfrac{x^2-1}{2}-\dfrac{3x-2}{3}\le\dfrac{(x+1)^2}{6}$"]),
     tasks(1, [r"$4x-12-x+2\le4x\Rightarrow-x\le10$: \ " + RI(ineq(I62[0])), r"$9x-18\gt9x+1\Rightarrow-18\gt1$, falso: \ " + R(r"\text{no tiene solución}"), r"$6x+8\lt\frac{x+38}{2}\Rightarrow11x\lt22$: \ " + RI(ineq(I62[2])), r"$2x^2-8x\le0\Rightarrow2x(x-4)\le0$: \ " + RI(ineq(I62[3]))])),
 (2, r"Resuelve las siguientes inecuaciones:" + tasks(2, [r"$-2x^3+3x\gt0$", r"$3x^2+x-24\ge0$", r"$x^3-4x\gt0$", r"$x^3+x^2-x-1\le0$", r"$3x(2x-1)+x^2\ge5x-1$", r"$-x^3-2x^2+x+2\le0$", r"$x^4-1\gt0$", r"$(x-1)(x+4)\lt-6$"])
     + recorda(r"Pásalo todo a un miembro, factoriza y haz la tabla de signos. Los extremos se incluyen si la desigualdad es $\le$ o $\ge$."),
     tasks(1, [RIf(e_) for e_ in I63])),
 (2, r"Resuelve las inecuaciones racionales siguientes:" + tasks(2, [r"$\dfrac{5x-2}{2x+1}\ge0$", r"$\dfrac{x^2-x-2}{x^2+x-2}\ge0$", r"$\dfrac{4x-5}{4x^2-x-5}\lt0$", r"$\dfrac{x^3}{x-9}\ge0$", r"$\dfrac{x^2+4x-5}{x^3-x}\ge0$", r"$\dfrac{2x+3}{x^3+1}\ge0$"])
     + recorda(r"Las raíces del denominador no se incluyen nunca en la solución."),
     tasks(1, [RIf(e_) for e_ in I64])),
]))
ck(ineq(I62[1]) == sp.S.EmptySet)

# =====================================================================
# 11. Problemes d'inequacions
ck(ineq(10 + Q(5, 100) * xr < Q(12, 100) * xr) == sp.Interval.open(Q(1000, 7), oo) and Q(1000, 7) > 142 and Q(1000, 7) < 143)
S87 = ineq(Q(3, 10) * 4 + Q(7, 10) * xr >= 5).intersect(sp.Interval(0, 10)); ck(S87 == sp.Interval(Q(38, 7), 10))
S90 = ineq(20 * xr - 5 * xr ** 2 > 15); ck(S90 == sp.Interval.open(1, 3))
S.append(("Problemas de inecuaciones", [
 (1, r"Una compañía telefónica ofrece dos tarifas: la A tiene una cuota fija de 10\,€ al mes más 0,05\,€ por minuto, y la B no tiene cuota fija pero cobra 0,12\,€ por minuto. ¿A partir de cuántos minutos mensuales es más económica la tarifa A?",
     r"$10+0,05x\lt0,12x\Rightarrow x\gt\frac{1000}{7}\approx142,9$: \ " + R(r"\text{a partir de 143 minutos}")),
 (1, r"La nota final de una asignatura se calcula con el 30\,\% de la nota del primer examen y el 70\,\% de la del segundo. Si una alumna ha sacado un 4 en el primero, ¿qué nota tiene que sacar en el segundo para aprobar (nota final $\ge5$)? Las notas van de 0 a 10.",
     r"$1,2+0,7x\ge5\Rightarrow x\ge\frac{38}{7}\approx5,43$: \ " + RI(S87)),
 (2, r"Se lanza una pelota hacia arriba y su altura, en metros, es $h(t)=20t-5t^2$, con $t$ en segundos $(0\le t\le4)$. ¿Durante cuánto tiempo está la pelota por encima de los 15 metros?",
     r"$20t-5t^2\gt15\Rightarrow t^2-4t+3\lt0\Rightarrow t\in(1,3)$: \ " + R(r"2\ \text{segundos}")),
]))

# =====================================================================
# 12. Ampliació (exercicis nous)
P91 = x ** 100 - 2 * x ** 51 + 1; ck(P91.subs(x, -1) == 4)
P92 = sp.expand(2 * (x - 1) * (x + 2) * (x - 3)); ck(P92.subs(x, 0) == 12 and P92 == 2 * x ** 3 - 4 * x ** 2 - 10 * x + 12)
ck(sp.cancel((x ** 3 - 27) / (x ** 2 - 9)) == (x ** 2 + 3 * x + 9) / (x + 3))
ck(sp.cancel((1 - 1 / x) / (1 - 1 / x ** 2)) == x / (x + 1))
ck(set(solve_r((xr / (xr + 1) + (xr + 1) / xr - Q(5, 2)))) == {1, -2})
okf(lambda t: sq(t + 3) - sq(t - 2) - 1, [6])
ck(set(sp.solve(2 * x ** 2 - 5 * x + 2, x)) == {2, Q(1, 2)})
okf(lambda t: math.log2(t + 1) + math.log2(t - 1) - 3, [3])
S100 = ineq((xr ** 2 - 4) / (xr ** 2 + 1) <= 0); ck(S100 == sp.Interval(-2, 2))
ck(abs(math.log(1.6) / math.log(1.04) - 11.98) < 0.01)
S.append(("Ampliación y problemas", [
 (1, r"Calcula, sin hacer la división, el resto de $(x^{100}-2x^{51}+1):(x+1)$.", r"$P(-1)=1+2+1=$ " + R("4")),
 (2, r"Halla el polinomio de grado 3 que tiene las raíces $1$, $-2$ y $3$ y que cumple $P(0)=12$.", r"$P(x)=a(x-1)(x+2)(x-3)$; \ $P(0)=6a=12\Rightarrow a=2$: \ " + R(L(P92))),
 (2, r"Simplifica:" + tasks(2, [r"$\dfrac{x^3-27}{x^2-9}$", r"$\dfrac{1-\frac1x}{1-\frac1{x^2}}$"]),
     tasks(2, [r"$\dfrac{(x-3)(x^2+3x+9)}{(x-3)(x+3)}=" + R(r"\frac{x^2+3x+9}{x+3}").strip('$') + "$", r"$\dfrac{\frac{x-1}{x}}{\frac{(x-1)(x+1)}{x^2}}=" + R(r"\frac{x}{x+1}").strip('$') + "$"])),
 (2, r"Resuelve $\dfrac{x}{x+1}+\dfrac{x+1}{x}=\dfrac52$.", r"$2x^2+2(x+1)^2=5x(x+1)\Rightarrow x^2+x-2=0$: \ " + R(r"x=1,\ x=-2") + r" (ninguna anula los denominadores)."),
 (2, r"Resuelve $\sqrt{x+3}-\sqrt{x-2}=1$.", r"$x+3=1+2\sqrt{x-2}+x-2\Rightarrow\sqrt{x-2}=2$: \ " + R("x=6") + r" \ ($3-2=1$ \checkmark)."),
 (2, r"Resuelve $2^{2x+1}-5\cdot2^x+2=0$.", r"$t=2^x$: $2t^2-5t+2=0\Rightarrow t=2,\ t=\frac12$: \ " + R(r"x=1,\ x=-1")),
 (2, r"Resuelve $\log_2(x+1)+\log_2(x-1)=3$.", r"$x^2-1=8\Rightarrow x=\pm3$; \ $x=-3$ no vale: \ " + R("x=3")),
 (2, r"Resuelve $\dfrac{x^2-4}{x^2+1}\le0$. ¿Por qué no hace falta estudiar el signo del denominador?", r"$x^2+1\gt0$ siempre, así que solo hace falta $x^2-4\le0$: \ " + RI(S100)),
 (2, r"Ingresamos 5000\,€ en una cuenta al 4\,\% de interés compuesto anual. ¿Cuántos años completos tienen que pasar para que haya al menos 8000\,€?",
     r"$5000\cdot1,04^t\ge8000\Rightarrow t\ge\dfrac{\log1,6}{\log1,04}\approx11,98$: \ " + R(r"12\ \text{años}")),
]))

bad = [mm for c_, mm in CHK if not c_]
assert not bad, bad[:5]
assert [len(s_[1]) for s_ in S] == [8, 10, 4, 3, 1, 3, 3, 3, 20, 4, 3, 9], [len(s_[1]) for s_ in S]

# =====================================================================

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "polinomios, Ruffini, teorema del resto, factorización, fracciones algebraicas, ecuaciones, inecuaciones"
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre = pre.replace(r'\usepackage{tikz}', '\\usepackage{tikz}\n\\usetikzlibrary{calc}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'\providecommand{\lt}{<}\providecommand{\gt}{>}' + '\n'
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

TIT = "Álgebra. Ecuaciones e inecuaciones"
def spc(t):
    # «, » separa elements; amb icomma la coma és un símbol normal i un «-» darrere seu seria una resta: el posem entre claus
    return re.sub(r'\$[^$]*\$', lambda mm: re.sub(r',((?:\\,|\\ |\\;|\s)+)-', r',\1{-}', mm.group(0).replace(', ', r',\, ')), t)
def build(sol):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 2: %s' % (t, TIT), capcalera='%s · Unidad 2: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-mi')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1batx-mi') + '{' + ('Soluciones de la ficha · Unidad 2' if sol else 'Ficha de ejercicios · Unidad 2') + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.8cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los resultados se dan de manera exacta (fracciones y raíces) y, cuando hace falta, con el valor aproximado. Puedes comprobar las divisiones, la factorización y las inecuaciones con las herramientas interactivas de los apuntes de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Da los resultados de manera exacta y, si hace falta, también aproximados. En las ecuaciones con denominadores, radicales o logaritmos, comprueba siempre las soluciones. Los ejercicios 1--62 son de la ficha del departamento; la sección 12 tiene otros nuevos para ampliar y aplicar lo que has aprendido.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, spc(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't2-fitxa-solucions-es.tex' if sol else 't2-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S), 'ejercicios;', len(CHK), 'comprobaciones')
