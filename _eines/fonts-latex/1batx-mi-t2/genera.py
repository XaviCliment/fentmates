# Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (1r Batxillerat MI, Unitat 2: Àlgebra. Equacions i inequacions)
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
    extra = '' if lead == 1 else (r'\ \ \text{(quocient de Ruffini dividit entre }%s)' % L(lead))
    return r'$' + T + r'$\\[2pt]$c(x)=' + R(L(q)).strip('$') + r',\ \ r=' + R(L(r)).strip('$') + extra + '$'
P7 = [(2 * x ** 3 + 5 * x ** 2 - 2 * x + a, -3, a, 3), (2 * x ** 4 + 3 * x ** 3 - 2 * x ** 2 - a * x + 3, Q(-3, 2), a, 1),
      (-6 * x ** 4 + 11 * x ** 3 + a * x ** 2 + 5 * x + 4, Q(4, 3), a, -10), (4 * x ** 4 + 6 * x ** 3 - 13 * x ** 2 + x + b, 5, b, -2930)]
def s7(P, r_, var, val):
    ck(sp.solve(P.subs(x, r_), var) == [val], '7 %s' % P)
    return r'$P(%s)=%s=0\Rightarrow ' % (L(r_), L(sp.expand(P.subs(x, r_)))) + R('%s=%s' % (L(var), L(val))).strip('$') + '$'
M8 = 2 * x ** 3 - 5 * x ** 2 + 4 * x - 4
ck(M8.subs(x, 2) == 0 and sp.div(M8, x - 2, x) == (2 * x ** 2 - x + 2, 0))
S.append(("Polinomis. Operacions", [
 (1, r"Simplifica les següents expressions polinòmiques." + tasks(1, [r"$2(x-2)^2-3(3x+2)-2(3x-2)(3x+2)$", r"$(3x+2)^2+2(2x-3)^2-(x-5)(2x-5)$", r"$(2x^2-2x-13)(3x^2-2x)-3x$",
      r"$(x^2+4)(x^2-4)(x-2)+2x(x^3-10)x$", r"$\left(\frac23x-\frac35\right)\left(\frac32x^2+\frac25\right)+\frac{6}{25}$"])
     + recorda(r"$(a\pm b)^2=a^2\pm2ab+b^2$, \ $(a+b)(a-b)=a^2-b^2$. Desenvolupa cada producte i redueix els termes semblants."),
     tasks(1, [R(L(sp.expand(e))) for e in E1])),
 (2, r"Demostra la igualtat algebraica: \[(x+y+z)^2=x^2+y^2+z^2+2xy+2xz+2yz\]",
     r"$(x+y+z)^2=\big((x+y)+z\big)^2=(x+y)^2+2(x+y)z+z^2=x^2+2xy+y^2+2xz+2yz+z^2$. \rest{Queda demostrada.}"),
 (1, r"Calcula $(4x^2-3x+2)^2$.", R(L(sp.expand((4 * x ** 2 - 3 * x + 2) ** 2))) + r" \ (amb la identitat de l'exercici anterior)."),
 (2, r"Calcula els valors de $a$ i $b$ perquè es verifiquen les següents igualtats." + tasks(1, [r"$(3x^2-5x+a)(2x^2+bx)=6x^4-19x^3+19x^2-6x$", r"$2(x+3)^2-3(x+a)=2x^2+bx+3$"]),
     tasks(1, [r"$6x^4+(3b-10)x^3+(2a-5b)x^2+abx$: \ $3b-10=-19$, $ab=-6\Rightarrow " + R("a=2,\\ b=-3").strip('$') + "$",
               r"$2x^2+9x+18-3a$: \ $" + R("b=9").strip('$') + r",\ \ 18-3a=3\Rightarrow " + R("a=5").strip('$') + "$"])),
 (1, r"Efectua les següents divisions:" + tasks(1, [r"$(3x^3+2x^2+x-5):(3x^2+2)$", r"$(3x^4-2x^2-x+4):(x^2+x+2)$", r"$(x^3-3x^2-x+6):(2x^3-2x+3)$"]),
     tasks(1, [divsol(*d) for d in D5])),
 (1, r"Efectua les següents divisions aplicant la regla de Ruffini:" + tasks(2, [r"$(3x^3+2x^2+x-5):(x+2)$", r"$(3x^4-2x^2-x+4):(x+2)$", r"$(x^3-3x^2-x+6):(2x+3)$", r"$(4x^4-3x^2+5):(-x+5)$", r"$(2x^5-12x^3-6x^2-117):(x-3)$"])
     + recorda(r"Si el divisor és $ax+b$, fes Ruffini amb $-\frac ba$ i divideix el quocient entre $a$; el residu no canvia."),
     tasks(1, [rufsol(*d) for d in D6])),
 (2, r"Utilitza Ruffini per a calcular el valor de $a$ i $b$ que fa que les següents divisions siguen exactes:" + tasks(1, [r"$(2x^3+5x^2-2x+a):(x+3)$", r"$(2x^4+3x^3-2x^2-ax+3):(2x+3)$", r"$(-6x^4+11x^3+ax^2+5x+4):(-3x+4)$", r"$(4x^4+6x^3-13x^2+x+b):(-x+5)$"]),
     tasks(1, [s7(*p) for p in P7]) + r"(Amb el teorema del residu, $P(r)$ ha de ser 0, on $r$ és l'arrel del divisor; és el mateix que obtenir residu 0 a Ruffini.)"),
 (1, r"Comprova si $M(x)=2x^3-5x^2+4x-4$ és divisible per $x-2$ i, si ho és, troba un polinomi $N(x)$ que permeta escriure $M(x)=(x-2)\cdot N(x)$.",
     r"$M(2)=16-20+8-4=0$: \rest{sí que és divisible}.\par Per Ruffini: $" + ruf(coefs(M8), 2)[0] + r"\Rightarrow " + R("N(x)=2x^2-x+2").strip('$') + "$"),
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
S.append(("Factorització d'un polinomi. Teorema del residu", [
 (1, r"Comprova si són arrels del polinomi $P(x)=x^4+3x^3-2x^2+6x-8$ els nombres següents:" + tasks(5, ["$x=1$", "$x=2$", "$x=-1$", "$x=-4$", "$x=-3$"]),
     tasks(5, [r"$P(1)=0$: \rest{sí}", r"$P(2)=36$: \rest{no}", r"$P(-1)=-18$: \rest{no}", r"$P(-4)=0$: \rest{sí}", r"$P(-3)=-44$: \rest{no}"])),
 (1, r"Calcula el valor numèric del polinomi $P(x)=x^2-2x-3$ per a $x=-1$ i $x=3$. Podries trobar un altre valor de $x$ per al qual el valor del polinomi siga zero? Raona la resposta.",
     r"$P(-1)=1+2-3=" + R("0").strip('$') + r"$, \ $P(3)=9-6-3=" + R("0").strip('$') + r"$. \rest{No}: un polinomi de grau 2 té com a màxim dues arrels, i ja les hem trobades: $P(x)=(x+1)(x-3)$."),
 (1, r"Determina les arrels dels polinomis següents:" + tasks(2, [r"$(x-3)(x+5)(x-2)$", r"$x(x-2)^3(2x+1)$", r"$(2x-1)(3x+2)(x+1)^3$", r"$x^3-3x^2-6x+8$", r"$x^3+8x^2+17x+10$", r"$2x^5-11x^4+21x^3-16x^2+4x$"]),
     tasks(1, [R(rootsT(P11[i])) + ('' if i in (0, 1, 2) else r" \ $\big(" + L(sp.factor(P11[i])) + r"\big)$") for i in range(6)])),
 (2, r"Determina, si existeixen, les arrels enteres de cadascun dels següents polinomis i factoritza'ls." + tasks(2, [r"$P(x)=x^3-2x^2-5x+6$", r"$P(x)=x^3+x^2-5x+3$", r"$P(x)=2x^4-x^3-5x^2+x+3$", r"$P(x)=4x^3-4x^2-11x+6$", r"$P(x)=x^4-4x^2$",
      r"$P(x)=6x^5+11x^4+3x^3-3x^2-x$", r"$P(x)=x^6-4x^4-x^2+4$", r"$P(x)=\frac{x^4}{4}+\frac34x^2+\frac{9}{16}$ \ (comprova que no té arrels reals)"])
     + recorda(r"Les arrels enteres són divisors del terme independent. Prova-les amb Ruffini fins que quede un polinomi de grau 2."),
     tasks(1, [R(L(sp.factor(P))) + r" \ \small(arrels: $" + rootsT(P) + "$)" for P in P12] +
           [r"$t=x^2$: $\frac{t^2}{4}+\frac34t+\frac9{16}=0\Rightarrow\Delta=\frac9{16}-\frac9{16}=0$, $t=-\frac32\lt0$: \rest{no té arrels reals}. $P(x)=" + R(r"\frac{1}{16}(2x^2+3)^2").strip('$') + "$"])),
 (1, r"Calcula el valor de $k$ perquè el polinomi:" + tasks(1, [r"$P(x)=x^3+x^2-2x+k$ siga divisible per $x-2$", r"$P(x)=x^3-2x^2+kx+4$ siga divisible per $x+2$",
      r"$P(x)=(k-3)x^3-15x+k$ siga divisible per $x+4$", r"$P(x)=x^3-(k-3)x^2+(k-5)x-3$ siga divisible per $x-3$"]),
     tasks(1, [k13(*p) for p in P13])),
 (2, r"Calcula el valor de $k$ perquè la divisió de $x^3-(3k+2)x^2-3$ entre $(x+3)$:" + tasks(2, ["Siga exacta.", "Tinga residu 15."]),
     r"$P(-3)=-27-9(3k+2)-3=-48-27k$." + tasks(2, [r"$-48-27k=0\Rightarrow " + R(r"k=-\frac{16}{9}").strip('$') + "$", r"$-48-27k=15\Rightarrow " + R(r"k=-\frac73").strip('$') + "$"])),
 (2, r"D'un polinomi de segon grau, $P(x)$, sabem que $P(1)=-6$, $P(0)=-3$ i una de les seues arrels és 3. Determina'l.",
     r"$P(x)=ax^2+bx+c$: \ $c=-3$, \ $a+b-3=-6$, \ $9a+3b-3=0\Rightarrow a=2,\ b=-5$: \ " + R("P(x)=2x^2-5x-3")),
 (1, r"Troba el valor de $m$ perquè el polinomi $mx^3-6x^2-4x+8$ tinga 2 com a arrel.", r"$P(2)=8m-24-8+8=8m-24=0\Rightarrow " + R("m=3").strip('$') + "$"),
 (2, r"Determina $a$ i $b$ de manera que el polinomi $x^3+ax^2+bx-6$ siga divisible per $x-2$ i per $x+3$.",
     r"$P(2)=0$: $4a+2b=-2$; \ $P(-3)=0$: $9a-3b=33$. \ " + R(r"a=2,\ b=-5") + r" \ (i aleshores $P(x)=(x-2)(x+3)(x+1)$)."),
 (1, r"Troba el valor de $m$ perquè el polinomi $2x^4+9x^3+2x^2-6x+3m$ tinga residu 12 en dividir-lo per $x+2$, sense fer la divisió.",
     r"Teorema del residu: $P(-2)=32-72+8+12+3m=-20+3m=12\Rightarrow " + R(r"m=\frac{32}{3}").strip('$') + "$"),
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
S.append(("Fraccions algebraiques", [
 (2, r"Simplifica les següents fraccions algebraiques." + tasks(2, [r"$\dfrac{2x^2-8}{x^3+x^2-2x}$", r"$\dfrac{x^3-x}{x^3+3x^2+2x}$", r"$\dfrac{x^4-2x^3-3x^2}{x^4-9x^2}$", r"$\dfrac{x^3-3x^2+3x-1}{x^3-2x^2+x}$",
      r"$\dfrac{2x^4-5x^3+x^2+5x-3}{2x^3-x^2-7x+6}$", r"$\dfrac{2x^4+x^3-11x^2+11x-3}{2x^3+3x^2-8x+3}$", r"$\dfrac{x^3-2x^2-9x+18}{x^3-7x^2+16x-12}$", r"$\dfrac{x^4-5x^3+9x^2-7x+2}{x^4-6x^3+13x^2-12x+4}$"])
     + recorda(r"Factoritza el numerador i el denominador i simplifica només els \emph{factors} comuns."),
     tasks(1, [simp(*f_) for f_ in F19])),
 (2, r"Efectua les següents sumes i restes reduint prèviament a comú denominador:" + tasks(2, [r"$\dfrac{1}{x+1}+\dfrac{3}{x^2-1}$", r"$\dfrac{1}{x^2+x}+\dfrac{3}{x+1}$", r"$\dfrac{1}{2x}-\dfrac{3}{4x^2-4x}$",
      r"$\dfrac{1}{x^2+x}+\dfrac{3}{x^2-x}$", r"$\dfrac{2x}{x-2}+\dfrac{3x-1}{x+2}-\dfrac{1}{x^2-4}$", r"$\dfrac{1}{(x-1)^2}+\dfrac{2}{x-1}+\dfrac{1}{x^2-1}$"]),
     tasks(2, [res(e_) for e_ in E20])),
 (2, r"Opera i simplifica les fraccions algebraiques:" + tasks(2, [r"$\dfrac{3x+3}{12x-12}:\dfrac{(x+1)^2}{x^2-1}$", r"$\dfrac{x^2+2x-3}{(x-2)^3}\cdot\dfrac{(x-2)^2}{x^2-1}$", r"$\dfrac{6x+4}{x-2}\cdot\dfrac{4x+1}{2x+4}$",
      r"$\dfrac{-6x^2}{x^2+2x+1}\cdot\dfrac{x+1}{3x^3}\cdot\dfrac{x+1}{3x}$", r"$\left(\dfrac3x-\dfrac{2x}{x+1}\right)\cdot\dfrac{x^2+x}{x-1}$", r"$\dfrac{(x-1)^2}{2}\cdot\dfrac{1}{x^2-1}-\dfrac{3x}{(x+1)^2}$",
      r"$\left(\dfrac{2x-1}{x+1}-\dfrac{3x}{x-1}\right)\cdot\dfrac{x^3-x}{-x^2-6x+1}$"]),
     tasks(2, [res(e_) for e_ in E21])),
 (3, r"Calcula i simplifica el resultat de les operacions següents:" + tasks(2, [r"$\dfrac{x+1}{x}+\dfrac{2x+1}{x+2}-\dfrac{x}{x^2+1}$", r"$\dfrac{1+\frac{2x+1}{x-1}}{\frac{1}{x-1}+\frac{x}{x+1}}$", r"$\dfrac{ba-a^2}{a^3b-ab^3}:\dfrac{b}{a^2+2ab+b^2}$",
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
    return r',\ '.join('x=' + L(v) for v in vals) if vals else r'\text{no té solució}'
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
S.append(("Equacions polinòmiques", [
 (2, r"Resol les següents equacions polinòmiques:" + tasks(2, [r"$\dfrac{2x-3}{4}+\dfrac x2-\dfrac{3x-1}{5}=2x-1$", r"$2(3x-2)+x(x-1)=-4$", r"$(x+1)^3-(x-1)^3=7$", r"$\dfrac{x^2+1}{2}-\dfrac{2x-3}{4}+\dfrac{x^2}{6}=\dfrac{59}{12}$",
      r"$6x^4+13x^3-8x^2-17x+6=0$", r"$2x^4-x^3-3x-18=0$", r"$6x^4+5x^3=2x^2+x$", r"$x^3-7x+6=0$", r"$x^3-3x^2-9x+27=0$", r"$x^4-x^3-5x^2-x-6=0$", r"$x^4-1=0$", r"$x^4+x^3-9x^2-9x=0$"])
     + recorda(r"Passa-ho tot a un membre i factoritza (factor comú, Ruffini…): un producte val zero si algun factor val zero."),
     tasks(1, [ex23(e_) for e_ in E23])),
 (2, r"Resol les següents equacions biquadrades (o que es resolen amb un canvi de variable):" + tasks(2, [r"$x^4-17x^2+16=0$", r"$x^6-9x^3+8=0$", r"$x^4-8x^2-9=0$", r"$4x^6+8x^3-12=0$", r"$2(x+1)^4-8x^3-8(x+3)+8=0$", r"$\dfrac{9}{x^2}=10-x^2$"]),
     tasks(1, [r"$t=x^2$: $t^2-17t+16=0\Rightarrow t=16,\ t=1$: \ " + R(r"x=\pm4,\ x=\pm1"), r"$t=x^3$: $t^2-9t+8=0\Rightarrow t=8,\ t=1$: \ " + R(r"x=2,\ x=1"), r"$t^2-8t-9=0\Rightarrow t=9$ ($t=-1$ no dona solucions): \ " + R(r"x=\pm3"), r"$t=x^3$: $t^2+2t-3=0\Rightarrow t=1,\ t=-3$: \ " + R(r"x=1,\ x=-\sqrt[3]{3}"), r"Desenvolupant: $2x^4+12x^2-14=0\Rightarrow t^2+6t-7=0\Rightarrow t=1$ ($t=-7$ no dona solucions): \ " + R(r"x=\pm1"), r"Multipliquem per $x^2$: $x^4-10x^2+9=0\Rightarrow t=9,\ t=1$: \ " + R(r"x=\pm3,\ x=\pm1")])),
 (1, r"Resol les següents equacions factoritzades:" + tasks(2, [r"$(x^2-3)(x^2-4)=0$", r"$(3x+2)(x^2-4x)(x^2-9)=0$", r"$(x^2-4x+4)(x^2+6x+9)=0$", r"$(x-2)^2(x+1)^3(2x-7)=0$"]),
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
S.append(("Equacions racionals", [
 (2, r"Resol les equacions racionals següents:" + tasks(2, [r"$\dfrac1x+\dfrac1{x^2}+\dfrac1{x^3}=\dfrac78$", r"$\dfrac{2x}{3}+\dfrac{2x+3}{x-1}=\dfrac{11}{3x-3}$", r"$\dfrac{2x}{x-2}+\dfrac{3x}{x+2}=\dfrac{6x^2}{x^2-4}$", r"$\dfrac{3}{x^2-6x+8}+\dfrac{x-5}{x^2-5x+4}=\dfrac{1}{x-4}$", r"$\dfrac{x}{\sqrt2}+\dfrac{\sqrt2}{x}=\sqrt2\,x$", r"$\dfrac{x}{x-2}+\dfrac{2x}{2-x}=-x$", r"$\dfrac{1+\frac{x+1}{x-1}}{2-\frac{x-1}{x+1}}=2$", r"$\dfrac{1}{1-\frac{1}{x+1}}=\dfrac{x+1}{x}$"])
     + recorda(r"Multiplica pel m.c.m. dels denominadors i, al final, descarta les solucions que anul·len algun denominador."),
     tasks(1, [r"$8x^2+8x+8=7x^3\Rightarrow(x-2)(7x^2+6x+4)=0$ ($\Delta\lt0$): \ " + R("x=2"), r"Multipliquem per $3(x-1)$: $2x^2+4x+9=11\Rightarrow x^2+2x-1=0$: \ " + R(r"x=-1\pm\sqrt2"), r"$2x(x+2)+3x(x-2)=6x^2\Rightarrow x^2+2x=0\Rightarrow x=0,\ x=-2$; \ $x=-2$ anul·la un denominador: \ " + R("x=0"), r"m.c.m. $=(x-1)(x-2)(x-4)$: $3(x-1)+(x-5)(x-2)=(x-1)(x-2)\Rightarrow x^2-4x+7=x^2-3x+2$: \ " + R("x=5"), r"Multipliquem per $\sqrt2\,x$: $x^2+2=2x^2\Rightarrow$ " + R(r"x=\pm\sqrt2"), r"$-\dfrac{x}{x-2}=-x\Rightarrow x=x(x-2)\Rightarrow x^2-3x=0$: \ " + R(r"x=0,\ x=3"), r"Simplificant: $\dfrac{2x(x+1)}{(x-1)(x+3)}=2\Rightarrow x^2+x=x^2+2x-3$: \ " + R("x=3"), r"El primer membre és $\dfrac{x+1}{x}$: és una \rest{identitat}, es compleix per a tot $x\neq0,\ x\neq-1$."])),
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
S.append(("Equacions amb radicals", [
 (2, r"Resol les següents equacions amb radicals:" + tasks(2, [r"$-\sqrt{2x-3}+1=x$", r"$x+\sqrt{2x^2+2x-3}=-1$", r"$\sqrt{\dfrac{7x+1}{4}}=\dfrac{5x-7}{6}$", r"$\dfrac{\sqrt{2x-1}}{4}=\dfrac{3}{\sqrt{2x-1}}$", r"$\sqrt{2-5x}+x\sqrt3=0$", r"$\sqrt{2+\sqrt{x-4}}=\sqrt{12-x}$", r"$\sqrt x+\sqrt{x-4}=2$", r"$\sqrt{x+5}+\sqrt{2x+8}=7$", r"$\sqrt{x+4}+\sqrt{x-1}=5$", r"$\sqrt{x-7}+\sqrt{2x}=\sqrt{x+1}$", r"$\sqrt{1-4x}-2\sqrt{3+x}=\sqrt{3+x}$"])
     + recorda(r"Aïlla un radical, eleva al quadrat i repeteix si cal. Comprova \emph{sempre} les solucions en l'equació inicial."),
     tasks(1, [r"$2x-3=(1-x)^2\Rightarrow(x-2)^2=0$; \ $x=2$: $-1+1=0\neq2$: \ " + R(r"\text{no té solució}"), r"$2x^2+2x-3=(x+1)^2\Rightarrow x^2=4$; \ $x=2$ no val ($-1-2\lt0$): \ " + R("x=-2"), r"$9(7x+1)=(5x-7)^2\Rightarrow25x^2-133x+40=0\Rightarrow x=5,\ x=\frac{8}{25}$; \ $x=\frac8{25}$ no val: \ " + R("x=5"), r"$2x-1=12$: \ " + R(r"x=\frac{13}{2}"), r"$2-5x=3x^2\Rightarrow3x^2+5x-2=0\Rightarrow x=-2,\ x=\frac13$; \ $x=\frac13$ no val: \ " + R("x=-2"), r"$2+\sqrt{x-4}=12-x\Rightarrow x-4=(10-x)^2\Rightarrow x^2-21x+104=0\Rightarrow x=8,\ x=13$; \ $x=13$ no val: \ " + R("x=8"), r"$x=4-4\sqrt{x-4}+x-4\Rightarrow\sqrt{x-4}=0$: \ " + R("x=4"), r"$x-46=-14\sqrt{x+5}\Rightarrow x^2-288x+1136=0\Rightarrow x=4,\ x=284$; \ $x=284$ no val: \ " + R("x=4"), r"$10\sqrt{x-1}=20\Rightarrow\sqrt{x-1}=2$: \ " + R("x=5"), r"$2\sqrt{2x^2-14x}=8-2x\Rightarrow x^2-6x-16=0\Rightarrow x=8,\ x=-2$; cap no val: \ " + R(r"\text{no té solució}"), r"$\sqrt{1-4x}=3\sqrt{3+x}\Rightarrow1-4x=27+9x$: \ " + R("x=-2")])),
 (2, r"Resol les següents equacions amb radicals no quadrats:" + tasks(2, [r"$\sqrt[3]{x^2-1}+1=x$", r"$\dfrac{\sqrt{3x+7}}{\sqrt[3]{x+1}}=\sqrt[3]{x^2+2x+1}$", r"$\sqrt[3]{4x-1}=x-4$", r"$\sqrt[3]{4-2x}=\sqrt[6]{8x^2-16x}$", r"$\sqrt{2x+2}-\sqrt[4]{6x+10}=0$"])
     + recorda(r"Eleva els dos membres a l'índex de l'arrel (o al m.c.m. dels índexs)."),
     tasks(1, [r"$x^2-1=(x-1)^3\Rightarrow x(x-1)(x-3)=0$; totes valen ($\sqrt[3]{-1}=-1$): \ " + R(r"x=0,\ x=1,\ x=3"), r"$\sqrt{3x+7}=x+1\Rightarrow x^2-x-6=0\Rightarrow x=3,\ x=-2$; \ $x=-2$ no val: \ " + R("x=3"), r"$4x-1=(x-4)^3\Rightarrow(x-7)(x^2-5x+9)=0$: \ " + R("x=7"), r"$(4-2x)^2=8x^2-16x\Rightarrow4x^2=16$; totes dues valen: \ " + R(r"x=2,\ x=-2"), r"$(2x+2)^2=6x+10\Rightarrow2x^2+x-3=0\Rightarrow x=1,\ x=-\frac32$; \ $x=-\frac32$ no val: \ " + R("x=1")])),
 (2, r"Calcula el valor d'un nombre tal que, si se li suma una unitat i després s'extrau l'arrel quadrada, s'obté el doble que en restar-li 11 unitats i extraure l'arrel quadrada.",
     r"$\sqrt{x+1}=2\sqrt{x-11}\Rightarrow x+1=4x-44$: \ " + R("x=15") + r" \ (comprovació: $\sqrt{16}=4=2\sqrt4$)."),
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
S.append(("Equacions logarítmiques", [
 (2, r"Resol les següents equacions logarítmiques:" + tasks(2, [r"$\log2+\log(x+3)=\log(x+5)$", r"$\log(15-2x)=2\log x$", r"$\log(2x+3)-\log(x-1)=2\log2+2\log3$", r"$\frac12\log(x^2-3x+2)=\log x$", r"$\log\left(\dfrac{2x-2}{x}\right)=2\log(x-1)-\log x$", r"$2\log x=\log\dfrac x2-1$", r"$\log(4-5x)+\log(2x)=\log(2x-x^2)+\log3$", r"$\log_2(5x^2+15x+10)-\log_2(x+2)=2$", r"$\dfrac{\log(4-x)}{\log(x+2)}=2$", r"$\log_{x+3}9=\log_53$", r"$\log_332+\log_{\frac13}(6-x)=\log_{\sqrt3}x$"])
     + recorda(r"Agrupa els logaritmes amb les propietats fins a arribar a $\log A=\log B$ (i aleshores $A=B$). Comprova que tots els arguments són positius."),
     tasks(1, [r"$2(x+3)=x+5$: \ " + R("x=-1"), r"$15-2x=x^2\Rightarrow x=3,\ x=-5$; \ $x=-5$ no val: \ " + R("x=3"), r"$\dfrac{2x+3}{x-1}=36\Rightarrow34x=39$: \ " + R(r"x=\frac{39}{34}"), r"$x^2-3x+2=x^2\Rightarrow$ " + R(r"x=\frac23") + r" (val: $x\gt0$ i $x^2-3x+2=\frac49\gt0$)", r"$\dfrac{2x-2}{x}=\dfrac{(x-1)^2}{x}\Rightarrow(x-1)(x-3)=0$; \ $x=1$ no val: \ " + R("x=3"), r"$\log x^2=\log\dfrac{x}{20}\Rightarrow x^2=\dfrac x{20}$; \ $x=0$ no val: \ " + R(r"x=\frac1{20}"), r"$2x(4-5x)=3(2x-x^2)\Rightarrow7x^2-2x=0$; \ $x=0$ no val: \ " + R(r"x=\frac27"), r"$\dfrac{5(x+1)(x+2)}{x+2}=4\Rightarrow5x+5=4$: \ " + R(r"x=-\frac15"), r"$4-x=(x+2)^2\Rightarrow x^2+5x=0$; \ $x=-5$ no val: \ " + R("x=0"), r"Canvi de base: $\dfrac{2\log3}{\log(x+3)}=\dfrac{\log3}{\log5}\Rightarrow\log(x+3)=2\log5\Rightarrow x+3=25$: \ " + R("x=22"), r"En base 3: $\log_332-\log_3(6-x)=2\log_3x\Rightarrow x^2(6-x)=32\Rightarrow(x+2)(x-4)^2=0$: \ " + R("x=4")])),
 (1, r"Troba el nombre que compleix que, en afegir al seu logaritme decimal el logaritme decimal de 2, el resultat és 1.", r"$\log x+\log2=1\Rightarrow\log(2x)=\log10$: \ " + R("x=5")),
 (1, r"Calcula el valor d'un nombre sabent que el doble del seu logaritme decimal és igual a la suma dels logaritmes decimals de 4 i de 9.", r"$2\log x=\log4+\log9\Rightarrow x^2=36$ ($x\gt0$): \ " + R("x=6")),
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
S.append(("Equacions exponencials", [
 (2, r"Resol les següents equacions exponencials:" + tasks(2, [r"$4^{x^2+1}=2^{5x+5}$", r"$4^{(x-2)^2}=262144$", r"$3^{x+4}=5$", r"$\dfrac{1}{2^x}=16^{\frac{x(x-1)}{2}}$", r"$13^{x^2+2x}-\dfrac1{13}=0$", r"$2^{2x^2-4x-2}=16$", r"$2\cdot6^{4x-3}=24$", r"$3\cdot2^x=2\cdot3^x$", r"$\sqrt[x]{27}=3^{x+2}$", r"$2^{x+4}-8^x=0$", r"$7^{x^2-5x+6}=1$", r"$49^{\frac{x-5}{3}}=\dfrac{1}{\sqrt{7^{x-1}}}$"])
     + recorda(r"Si pots, escriu els dos membres amb la mateixa base i iguala els exponents; si no, pren logaritmes."),
     tasks(1, [r"$2^{2x^2+2}=2^{5x+5}\Rightarrow2x^2-5x-3=0$: \ " + R(r"x=3,\ x=-\frac12"), r"$262144=4^9\Rightarrow(x-2)^2=9$: \ " + R(r"x=5,\ x=-1"), r"$x+4=\dfrac{\log5}{\log3}$: \ " + R(r"x=\frac{\log5}{\log3}-4\approx" + dec(math.log(5) / math.log(3) - 4)), r"$2^{-x}=2^{2x(x-1)}\Rightarrow2x^2-x=0$: \ " + R(r"x=0,\ x=\frac12"), r"$13^{x^2+2x}=13^{-1}\Rightarrow(x+1)^2=0$: \ " + R("x=-1"), r"$2x^2-4x-2=4\Rightarrow x^2-2x-3=0$: \ " + R(r"x=3,\ x=-1"), r"$6^{4x-3}=12\Rightarrow4x-3=\dfrac{\log12}{\log6}$: \ " + R(r"x=\frac{3+\log_612}{4}\approx" + dec(1 + math.log(2) / (4 * math.log(6)))), r"$\left(\dfrac32\right)^x=\dfrac32$: \ " + R("x=1"), r"$3^{3/x}=3^{x+2}\Rightarrow x^2+2x-3=0$: \ " + R(r"x=1,\ x=-3"), r"$2^{x+4}=2^{3x}\Rightarrow x+4=3x$: \ " + R("x=2"), r"$x^2-5x+6=0$: \ " + R(r"x=2,\ x=3"), r"$7^{\frac{2(x-5)}{3}}=7^{-\frac{x-1}{2}}\Rightarrow4(x-5)=-3(x-1)$: \ " + R(r"x=\frac{23}{7}")])),
 (2, r"Resol les següents equacions exponencials:" + tasks(2, [r"$2^{x+1}+2^x+2^{x-1}=28$", r"$5^{x+3}-5^{x-1}-3120=0$", r"$4^x+4^{x-1}+4^{x-2}=336$", r"$3^{x+2}+3^{x+1}+3^x+3^{x-1}=120$", r"$2^{x-1}+2^{x-2}+2^{x-3}+2^{x-4}=960$", r"$6^x-9\cdot6^{-x}+8=0$"])
     + recorda(r"Descompon les potències ($a^{x+1}=a\cdot a^x$, $a^{x-1}=\frac{a^x}{a}$) i trau factor comú $a^x$."),
     tasks(1, [r"$2^x\left(2+1+\frac12\right)=28\Rightarrow2^x=8$: \ " + R("x=3"), r"$5^x\left(125-\frac15\right)=3120\Rightarrow5^x=25$: \ " + R("x=2"), r"$4^x\cdot\frac{21}{16}=336\Rightarrow4^x=256$: \ " + R("x=4"), r"$3^x\left(9+3+1+\frac13\right)=120\Rightarrow3^x=9$: \ " + R("x=2"), r"$2^x\cdot\frac{15}{16}=960\Rightarrow2^x=1024$: \ " + R("x=10"), r"$t=6^x$: $t^2+8t-9=0\Rightarrow t=1$ ($t=-9$ no val): \ " + R("x=0")])),
 (3, r"Resol les següents equacions exponencials:" + tasks(2, [r"$3^{2x}-3^{x-1}=3^{x+1}-1$", r"$2\cdot10^{2x+4}+3\cdot10^{x+2}-5=0$", r"$9^x+5\cdot3^x-24=0$", r"$9^x+3^{2x-1}+3^{x-1}=111$", r"$3^{x+2}+9^{x-1}=90$", r"$2^{2x-4}-5\cdot2^{x-3}+1=0$", r"$9^{x+2}+3^{x+3}-810=0$", r"$4^{x+1}+2^{x+3}=320$"])
     + recorda(r"Si hi ha $a^{2x}$ i $a^x$, fes el canvi $t=a^x$; les solucions $t\le0$ no valen."),
     tasks(1, [r"$t=3^x$: $3t^2-10t+3=0\Rightarrow t=3,\ t=\frac13$: \ " + R(r"x=1,\ x=-1"), r"$t=10^{x+2}$: $2t^2+3t-5=0\Rightarrow t=1$ ($t=-\frac52$ no val) $\Rightarrow x+2=0$: \ " + R("x=-2"), r"$t=3^x$: $t^2+5t-24=0\Rightarrow t=3$ ($t=-8$ no val): \ " + R("x=1"), r"$t=3^x$: $t^2+\frac{t^2}{3}+\frac t3=111\Rightarrow4t^2+t-333=0\Rightarrow t=9$: \ " + R("x=2"), r"$t=3^x$: $9t+\frac{t^2}{9}=90\Rightarrow t^2+81t-810=0\Rightarrow t=9$ ($t=-90$ no val): \ " + R("x=2"), r"$t=2^x$: $\frac{t^2}{16}-\frac{5t}{8}+1=0\Rightarrow t^2-10t+16=0\Rightarrow t=8,\ t=2$: \ " + R(r"x=3,\ x=1"), r"$t=3^x$: $81t^2+27t-810=0\Rightarrow3t^2+t-30=0\Rightarrow t=3$ ($t=-\frac{10}{3}$ no val): \ " + R("x=1"), r"$t=2^x$: $4t^2+8t-320=0\Rightarrow t^2+2t-80=0\Rightarrow t=8$ ($t=-10$ no val): \ " + R("x=3")])),
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
S.append(("Problemes d'equacions", [
 (2, r"Un comerciant té un tonell de vi de la classe A de preu 5\,€/L. Afig 50 litres de vi de la classe B de 2\,€/L i 50 litres d'aigua i la mescla resulta a 4\,€/L. Quants litres de la classe A tenia el tonell?",
     r"$5x+2\cdot50+0\cdot50=4(x+100)\Rightarrow$ " + R(r"x=300\ \text{L}")),
 (1, r"Tenim 30 litres de vi a 5\,€/L i volem afegir-hi vi de 10\,€/L per a obtindre una mescla que isca a 7\,€/L. Quants litres hem d'afegir?", r"$30\cdot5+10x=7(30+x)\Rightarrow3x=60$: \ " + R(r"20\ \text{L}")),
 (2, r"En una botiga es ven te blanc a 18\,€/kg i te verd a 14\,€/kg. També s'hi ven una mescla de tots dos a 16,4\,€/kg. Quina és la composició de la mescla?",
     r"En 1 kg, $x$ kg de te blanc: $18x+14(1-x)=16,4\Rightarrow x=0,6$: \ " + R(r"60\,\%\ \text{blanc i }40\,\%\ \text{verd}")),
 (1, r"En un col·legi hi ha tres cursos. El 60\,\% dels alumnes estudia primer, el 30\,\% estudia segon i la resta, que són 15 alumnes, estudia tercer. Quants alumnes hi ha al col·legi?",
     r"El 10\,\% són 15: \ " + R(r"150\ \text{alumnes}")),
 (2, r"El 80\,\% de les entrades d'un partit es reservaren per als socis del club; de les restants, el 25\,\% s'enviaren als socis del club contrari i les altres, 18\,000, es posaren a la venda. Quantes entrades hi havia?",
     r"A la venda queda el $75\,\%$ del $20\,\%$, és a dir, el $15\,\%$: $0,15x=18\,000\Rightarrow$ " + R(r"120\,000\ \text{entrades}")),
 (1, r"Una fàbrica exporta el 30\,\% de la producció a Àsia, el 40\,\% a Europa, el 15\,\% a Amèrica i la resta, que suposa una facturació de 3 milions d'euros, a Àfrica. Quina és la facturació total?",
     r"Àfrica és el 15\,\%: $0,15x=3\Rightarrow$ " + R(r"20\ \text{milions d'euros}")),
 (2, r"Un examen consta de 20 preguntes. Cada encert suma 5 punts i cada error resta 2 punts. Una alumna va traure 58 punts. Quantes preguntes va encertar i quantes va errar, si no se'n pot deixar cap sense contestar?",
     r"$5x-2(20-x)=58\Rightarrow7x=98$: \ " + R(r"14\ \text{encerts i }6\ \text{errades}")),
 (3, r"Un botiguer inverteix 125\,€ en la compra d'una partida de pomes. En rebutja 20 quilos per defectuoses i ven la resta per 147\,€, guanyant 0,40\,€ per quilo sobre el preu de compra. Quants quilos en va comprar?",
     r"$(x-20)\left(\dfrac{125}{x}+0,4\right)=147\Rightarrow x^2-75x-6250=0\Rightarrow x=125$ ($x=-50$ no té sentit): \ " + R(r"125\ \text{kg}")),
 (1, r"Calcula la base i l'altura d'un triangle rectangle si són nombres enters consecutius i la hipotenusa mesura 5 cm.", r"$x^2+(x+1)^2=25\Rightarrow x^2+x-12=0\Rightarrow x=3$: \ " + R(r"3\ \text{cm i }4\ \text{cm}")),
 (2, r"Calcula la longitud dels tres costats d'un triangle rectangle si són nombres parells consecutius.", r"$x^2+(x+2)^2=(x+4)^2\Rightarrow x^2-4x-12=0\Rightarrow x=6$: \ " + R(r"6,\ 8\ \text{i }10\ \text{cm}")),
 (2, r"Calcula les dimensions d'una finca rectangular si el perímetre mesura 140 m i la diagonal 50 m.", r"$x+y=70,\ x^2+y^2=2500\Rightarrow x^2-70x+1200=0$: \ " + R(r"40\ \text{m}\times30\ \text{m}")),
 (1, r"Una bassa tarda 5 hores a omplir-se amb la presa d'aigua habitual i 20 hores amb una mànega. Quant de temps cal si usem tots dos mètodes alhora?", r"$\frac15+\frac1{20}=\frac14$: \ " + R(r"T=4\ \text{h}")),
 (1, r"Un home tarda 2 hores a agranar una casa i un altre en tarda 3. Quant tardarien treballant junts?", r"$\frac12+\frac13=\frac56\Rightarrow T=\frac65$ h: \ " + R(r"1\ \text{h}\ 12\ \text{min}")),
 (2, r"Dues persones treballant juntes tarden 10 hores a fer un treball, però una treballa el doble de ràpid que l'altra. Quant tardaria cadascuna per separat?",
     r"$\dfrac1t+\dfrac1{2t}=\dfrac1{10}\Rightarrow t=15$: \ " + R(r"15\ \text{h i }30\ \text{h}")),
 (2, r"Una piscina es pot omplir amb 5 fonts que, per separat, tarden 10, 20, 30, 40 i 50 hores respectivament. Quant tardaran les cinc juntes?",
     r"$\frac1{10}+\frac1{20}+\frac1{30}+\frac1{40}+\frac1{50}=\frac{137}{600}\Rightarrow T=\frac{600}{137}\approx" + R(r"4,38\ \text{h}\approx4\ \text{h}\ 23\ \text{min}").strip('$') + "$"),
 (3, r"Un grup de persones contracta un autobús per 600\,€ a pagar a parts iguals; al final 10 persones no poden anar al viatge i cada persona que hi va ha de pagar 5\,€ més. Quantes persones anaven inicialment?",
     r"$\dfrac{600}{x-10}=\dfrac{600}{x}+5\Rightarrow x^2-10x-1200=0\Rightarrow x=40$: \ " + R(r"40\ \text{persones}")),
 (2, r"El nombre de malalts de grip en una ciutat al llarg del passat gener ve donat per $y(t)=100+200\cdot e^{0,2t}$, on $t$ són els dies transcorreguts des de l'1 de gener." + tasks(1, ["Quants malalts hi havia l'1 de gener?", "Quin dia el nombre de malalts era de 900?"]),
     tasks(1, [R(r"y(0)=300\ \text{malalts}"), r"$200e^{0,2t}=800\Rightarrow t=5\ln4\approx6,93$: \ " + R(r"\text{el 7 de gener (cap al final del dia)}")])),
 (2, r"La quantitat que queda d'una substància radioactiva després de $t$ dies és $q(t)=M\cdot e^{-0,1t}$." + tasks(1, ["Després de quant de temps la massa s'haurà reduït a la meitat?", "Si la massa inicial és de 27 mg, quanta substància quedarà després de 10 dies?"]),
     tasks(1, [r"$e^{-0,1t}=\frac12\Rightarrow t=10\ln2\approx" + R(r"6,93\ \text{dies}").strip('$') + "$", r"$27e^{-1}\approx" + R(r"9,93\ \text{mg}").strip('$') + "$"])),
 (2, r"Si inicialment hi ha $n$ bacteris en un cultiu i el nombre es duplica cada hora, després de $t$ hores n'hi ha $N=n\cdot2^t$. Si inicialment n'hi ha 4500, quant de temps tardarà el cultiu a arribar a 50\,000 bacteris?",
     r"$2^t=\dfrac{100}{9}\Rightarrow t=\dfrac{\log(100/9)}{\log2}\approx" + R(r"3,47\ \text{h}\approx3\ \text{h}\ 28\ \text{min}").strip('$') + "$"),
 (3, r"La biomassa $C$ (en kg) per unitat de superfície d'una regió segueix la funció $C(x)=\dfrac{4}{1+K\cdot a^{x/10}}$, amb $x\ge0$ el temps en anys." + tasks(1, [r"Calcula $K$ i $a$ perquè als 10 anys hi haja 1 kg de biomassa i als 20 anys, 1,6 kg.", "Quants anys han de passar perquè la biomassa siga de 3 kg?"]),
     tasks(1, [r"$1+Ka=4$, \ $1+Ka^2=2,5\Rightarrow Ka=3,\ Ka^2=1,5$: \ " + R(r"a=\frac12,\ K=6"), r"$1+6\cdot0,5^{x/10}=\frac43\Rightarrow0,5^{x/10}=\frac1{18}\Rightarrow x=10\log_218\approx" + R(r"41,7\ \text{anys}").strip('$') + "$"])),
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
S.append(("Inequacions amb una incògnita", [
 (1, r"Comprova si els nombres reals indicats pertanyen a la solució de les inequacions corresponents:" + tasks(1, [r"$x=-2$ de la inequació $x^3+x^2+x\le6$", r"$x=\dfrac1e$ de la inequació $x+\ln x\ge0$", r"$x=-0,5$ de la inequació $2^x+x-2\lt3^x$"]),
     tasks(1, [r"$-8+4-2=-6\le6$: \rest{sí}", r"$\frac1e-1\approx-0,63\not\ge0$: \rest{no}", r"$2^{-0,5}-2,5\approx-1,79\lt3^{-0,5}\approx0,58$: \rest{sí}"])),
 (1, r"Resol les següents inequacions:" + tasks(2, [r"$\dfrac{x-3}{2}-\dfrac{x-2}{8}\le\dfrac x2$", r"$2x-3-\dfrac x2\gt x+\dfrac{3x+1}{6}$", r"$x+2(x+1)+3(x+2)\lt\dfrac{x+38}{2}$", r"$\dfrac{x^2-1}{2}-\dfrac{3x-2}{3}\le\dfrac{(x+1)^2}{6}$"]),
     tasks(1, [r"$4x-12-x+2\le4x\Rightarrow-x\le10$: \ " + RI(ineq(I62[0])), r"$9x-18\gt9x+1\Rightarrow-18\gt1$, fals: \ " + R(r"\text{no té solució}"), r"$6x+8\lt\frac{x+38}{2}\Rightarrow11x\lt22$: \ " + RI(ineq(I62[2])), r"$2x^2-8x\le0\Rightarrow2x(x-4)\le0$: \ " + RI(ineq(I62[3]))])),
 (2, r"Resol les següents inequacions:" + tasks(2, [r"$-2x^3+3x\gt0$", r"$3x^2+x-24\ge0$", r"$x^3-4x\gt0$", r"$x^3+x^2-x-1\le0$", r"$3x(2x-1)+x^2\ge5x-1$", r"$-x^3-2x^2+x+2\le0$", r"$x^4-1\gt0$", r"$(x-1)(x+4)\lt-6$"])
     + recorda(r"Passa-ho tot a un membre, factoritza i fes la taula de signes. Els extrems s'inclouen si la desigualtat és $\le$ o $\ge$."),
     tasks(1, [RIf(e_) for e_ in I63])),
 (2, r"Resol les inequacions racionals següents:" + tasks(2, [r"$\dfrac{5x-2}{2x+1}\ge0$", r"$\dfrac{x^2-x-2}{x^2+x-2}\ge0$", r"$\dfrac{4x-5}{4x^2-x-5}\lt0$", r"$\dfrac{x^3}{x-9}\ge0$", r"$\dfrac{x^2+4x-5}{x^3-x}\ge0$", r"$\dfrac{2x+3}{x^3+1}\ge0$"])
     + recorda(r"Les arrels del denominador no s'inclouen mai en la solució."),
     tasks(1, [RIf(e_) for e_ in I64])),
]))
ck(ineq(I62[1]) == sp.S.EmptySet)

# =====================================================================
# 11. Problemes d'inequacions
ck(ineq(10 + Q(5, 100) * xr < Q(12, 100) * xr) == sp.Interval.open(Q(1000, 7), oo) and Q(1000, 7) > 142 and Q(1000, 7) < 143)
S87 = ineq(Q(3, 10) * 4 + Q(7, 10) * xr >= 5).intersect(sp.Interval(0, 10)); ck(S87 == sp.Interval(Q(38, 7), 10))
S90 = ineq(20 * xr - 5 * xr ** 2 > 15); ck(S90 == sp.Interval.open(1, 3))
S.append(("Problemes d'inequacions", [
 (1, r"Una companyia telefònica ofereix dues tarifes: la A té una quota fixa de 10\,€ al mes més 0,05\,€ per minut, i la B no té quota fixa però cobra 0,12\,€ per minut. A partir de quants minuts mensuals és més econòmica la tarifa A?",
     r"$10+0,05x\lt0,12x\Rightarrow x\gt\frac{1000}{7}\approx142,9$: \ " + R(r"\text{a partir de 143 minuts}")),
 (1, r"La nota final d'una assignatura es calcula amb el 30\,\% de la nota del primer examen i el 70\,\% de la del segon. Si una alumna ha tret un 4 en el primer, quina nota ha de traure en el segon per a aprovar (nota final $\ge5$)? Les notes van de 0 a 10.",
     r"$1,2+0,7x\ge5\Rightarrow x\ge\frac{38}{7}\approx5,43$: \ " + RI(S87)),
 (2, r"Es llança una pilota cap amunt i la seua altura, en metres, és $h(t)=20t-5t^2$, amb $t$ en segons $(0\le t\le4)$. Durant quant de temps està la pilota per damunt dels 15 metres?",
     r"$20t-5t^2\gt15\Rightarrow t^2-4t+3\lt0\Rightarrow t\in(1,3)$: \ " + R(r"2\ \text{segons}")),
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
S.append(("Ampliació i problemes", [
 (1, r"Calcula, sense fer la divisió, el residu de $(x^{100}-2x^{51}+1):(x+1)$.", r"$P(-1)=1+2+1=$ " + R("4")),
 (2, r"Troba el polinomi de grau 3 que té les arrels $1$, $-2$ i $3$ i que compleix $P(0)=12$.", r"$P(x)=a(x-1)(x+2)(x-3)$; \ $P(0)=6a=12\Rightarrow a=2$: \ " + R(L(P92))),
 (2, r"Simplifica:" + tasks(2, [r"$\dfrac{x^3-27}{x^2-9}$", r"$\dfrac{1-\frac1x}{1-\frac1{x^2}}$"]),
     tasks(2, [r"$\dfrac{(x-3)(x^2+3x+9)}{(x-3)(x+3)}=" + R(r"\frac{x^2+3x+9}{x+3}").strip('$') + "$", r"$\dfrac{\frac{x-1}{x}}{\frac{(x-1)(x+1)}{x^2}}=" + R(r"\frac{x}{x+1}").strip('$') + "$"])),
 (2, r"Resol $\dfrac{x}{x+1}+\dfrac{x+1}{x}=\dfrac52$.", r"$2x^2+2(x+1)^2=5x(x+1)\Rightarrow x^2+x-2=0$: \ " + R(r"x=1,\ x=-2") + r" (cap anul·la els denominadors)."),
 (2, r"Resol $\sqrt{x+3}-\sqrt{x-2}=1$.", r"$x+3=1+2\sqrt{x-2}+x-2\Rightarrow\sqrt{x-2}=2$: \ " + R("x=6") + r" \ ($3-2=1$ \checkmark)."),
 (2, r"Resol $2^{2x+1}-5\cdot2^x+2=0$.", r"$t=2^x$: $2t^2-5t+2=0\Rightarrow t=2,\ t=\frac12$: \ " + R(r"x=1,\ x=-1")),
 (2, r"Resol $\log_2(x+1)+\log_2(x-1)=3$.", r"$x^2-1=8\Rightarrow x=\pm3$; \ $x=-3$ no val: \ " + R("x=3")),
 (2, r"Resol $\dfrac{x^2-4}{x^2+1}\le0$. Per què no cal estudiar el signe del denominador?", r"$x^2+1\gt0$ sempre, així que només cal $x^2-4\le0$: \ " + RI(S100)),
 (2, r"Ingressem 5000\,€ en un compte al 4\,\% d'interés compost anual. Quants anys complets han de passar perquè hi haja almenys 8000\,€?",
     r"$5000\cdot1,04^t\ge8000\Rightarrow t\ge\dfrac{\log1,6}{\log1,04}\approx11,98$: \ " + R(r"12\ \text{anys}")),
]))

bad = [mm for c_, mm in CHK if not c_]
assert not bad, bad[:5]
assert [len(s_[1]) for s_ in S] == [8, 10, 4, 3, 1, 3, 3, 3, 20, 4, 3, 9], [len(s_[1]) for s_ in S]

# =====================================================================

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={polinomis, Ruffini, teorema del residu, factorització, fraccions algebraiques, equacions, inequacions}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques I}')
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

TIT = "Àlgebra. Equacions i inequacions"
def spc(t):
    # «, » separa elements; amb icomma la coma és un símbol normal i un «-» darrere seu seria una resta: el posem entre claus
    return re.sub(r'\$[^$]*\$', lambda mm: re.sub(r',((?:\\,|\\ |\\;|\s)+)-', r',\1{-}', mm.group(0).replace(', ', r',\, ')), t)
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 2: %s. 1r de Batxillerat MI}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 2: %s · 1r Batxillerat MI" % (t, TIT))
    assert 'Unitat 2' in p and 'unitat 2' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques I}{1r Batx}{''' + ('Solucions de la fitxa · Unitat 2' if sol else "Fitxa d'exercicis · Unitat 2") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Els resultats es donen de manera exacta (fraccions i arrels) i, quan cal, amb el valor aproximat. Pots comprovar les divisions, la factorització i les inequacions amb les eines interactives dels apunts de la unitat."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos. Dona els resultats de manera exacta i, si cal, també aproximats. En les equacions amb denominadors, radicals o logaritmes, comprova sempre les solucions. Els exercicis 1--62 són de la fitxa del departament; la secció 12 en té de nous per a ampliar i aplicar el que has aprés.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, spc(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't2-fitxa-solucions.tex' if sol else 't2-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S), 'exercicis;', len(CHK), 'comprovacions')
