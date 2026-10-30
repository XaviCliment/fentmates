# Genera t4-fitxa-exercicis.tex i t4-fitxa-solucions.tex (3r ESO, Unitat 4: Àlgebra. Polinomis)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les solucions algebraiques es calculen amb sympy (pt, dv, ruf) i les escrites a mà es comproven amb chk.
import os, re
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- àlgebra ----------
x, y, a, b = sp.symbols('x y a b')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s.replace('\\cdot', '*').replace(':', '/'), transformations=TR, local_dict={'x': x, 'y': y, 'a': a, 'b': b}) if isinstance(s, str) else s
def chk(l, r): assert sp.expand(S(l) - S(r)) == 0, (l, r, sp.expand(S(l)))
def ntex(c):
    c = sp.Rational(c)
    return str(c.p) if c.q == 1 else ('-' if c < 0 else '') + r'\tfrac{%d}{%d}' % (abs(c.p), c.q)
def pt(e):
    """polinomi en TeX, de grau més alt a més baix"""
    e = sp.expand(S(e))
    if e == 0: return '0'
    gens = sorted(e.free_symbols, key=str)
    if not gens: return ntex(e)
    out = ''
    for mon, c in sp.Poly(e, *gens).terms(order='grlex'):
        lit = ''.join(str(g) if k == 1 else '%s^{%d}' % (g, k) for g, k in zip(gens, mon) if k)
        q = abs(sp.Rational(c))
        out += ('-' if c < 0 else ('+' if out else '')) + (ntex(q) if q != 1 or not lit else '') + lit
    return out
def tx(s):
    """expressió escrita com a l'entrada -> TeX"""
    s = re.sub(r'\^(\d+)', r'^{\1}', s)
    s = re.sub(r'\b(\d+)/(\d+)', r'\\tfrac{\1}{\2}', s)
    return s.replace('*', r'\cdot ')
def ex(s, p=None):
    """'(x+3)^2' -> enunciat i solució (desenvolupat)"""
    return '$%s$' % tx(s), r'$%s=\res{%s}$' % (tx(s), pt(p or s))
def ops(lst, n):
    q, s = zip(*[ex(*e) if isinstance(e, tuple) else ex(e) for e in lst])
    return tasks(n, q), tasks(min(n, 2), s)
def dv(D, d):
    C, R = sp.div(S(D), S(d), x)
    return C, R
def dvsol(D, d):
    C, R = dv(D, d)
    return r'$C(x)=\res{%s},\ \ R%s=\res{%s}$' % (pt(C), '(x)' if sp.degree(R, x) > 0 else '', pt(R))
def coeffs(D):
    return [int(c) if sp.Rational(c).q == 1 else sp.Rational(c) for c in sp.Poly(S(D), x).all_coeffs()]
def ruf(D, r):
    """taula de Ruffini de D(x):(x-r) en LaTeX + quocient i residu"""
    cs = [Fr(int(c)) for c in coeffs(D)]; r = Fr(r)
    bot = [cs[0]]; mid = ['']
    for c in cs[1:]:
        m = bot[-1] * r; mid.append(m); bot.append(c + m)
    f = lambda v: '' if v == '' else str(v)
    n = len(cs)
    tab = (r'\begin{array}{r|%s|r}' % ('r' * (n - 1)) + ' & ' + ' & '.join(f(c) for c in cs) + r'\\ '
           + f(r) + ' & ' + ' & '.join(f(m) for m in mid) + r'\\ \hline & ' + ' & '.join(f(c) for c in bot) + r'\end{array}')
    C, R = dv(D, 'x-(%s)' % r)
    assert R == bot[-1] and coeffs(C) == [int(c) for c in bot[:-1]], (D, r)
    return tab, C, R
def rufsol(D, r):
    tab, C, R = ruf(D, r)
    return r'$%s\quad C(x)=\res{%s},\ \ R=\res{%s}$' % (tab, pt(C), pt(R))
def val(e, **v): return S(e).subs({sp.Symbol(k): sp.Rational(w) for k, w in v.items()})

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S_.append(("Llenguatge algebraic", [
 (1, r"Escriu en llenguatge algebraic:" + tasks(2, [r"El doble d'un nombre més 5.", r"El triple d'un nombre menys el seu quadrat.", r"La meitat del següent d'un nombre.", r"El quadrat de la suma de dos nombres.",
      r"La suma de dos nombres consecutius.", r"La tercera part d'un nombre més el seu doble.", r"El $15\,\%$ d'un nombre.", r"La diferència dels quadrats de dos nombres."])
     + recorda(r"Fixa't en l'ordre: «el quadrat de la suma» és $(x+y)^2$, però «la suma dels quadrats» és $x^2+y^2$."),
     tasks(4, [r'$\res{2x+5}$', r'$\res{3x-x^2}$', r'$\res{\tfrac{x+1}{2}}$', r'$\res{(x+y)^2}$', r'$\res{x+(x+1)}$', r'$\res{\tfrac{x}{3}+2x}$', r'$\res{0{,}15x}$', r'$\res{x^2-y^2}$'])),
 (1, r"Escriu amb paraules el que expressa cada expressió algebraica:" + tasks(4, ['$2x-1$', '$x^2+3$', r'$\dfrac{x+y}{2}$', '$3(x-4)$']),
     tasks(2, [r"El doble d'un nombre menys 1.", r"El quadrat d'un nombre més 3.", r"La mitjana (semisuma) de dos nombres.", r"El triple de la diferència entre un nombre i 4."])),
 (1, r"Calcula el valor numèric de cada expressió per als valors indicats:" + tasks(2, [r'$3x-5$, \ per a $x=4$', r'$x^2-2x$, \ per a $x=-3$', r'$-x^2+5$, \ per a $x=-2$', r'$2x^2y-xy$, \ per a $x=1,\ y=-2$']),
     tasks(2, [r'$3\cdot4-5=\res{7}$', r'$(-3)^2-2\cdot(-3)=9+6=\res{15}$', r'$-(-2)^2+5=-4+5=\res{1}$', r'$2\cdot1^2\cdot(-2)-1\cdot(-2)=-4+2=\res{-2}$'])),
 (2, r"Escriu una expressió algebraica per al perímetre i l'àrea de cada figura:" + tasks(2, [r"Un rectangle de base $3x$ i altura $x+2$.", r"Un quadrat de costat $x-1$."]),
     tasks(1, [r"$P=2\cdot3x+2(x+2)=\res{8x+4}$; \ $A=\res{3x(x+2)}$", r"$P=\res{4(x-1)}=4x-4$; \ $A=\res{(x-1)^2}$"])),
 (2, r"En Pere té $x$ anys; la seua germana en té el doble menys 3 i son pare, 25 més que en Pere." + tasks(1, ["Escriu l'edat de cadascú i la suma de les tres edats.", "Escriu la suma de les tres edats d'ací a 4 anys.", "Quant sumen les tres edats si en Pere té 12 anys?"]),
     tasks(1, [r"Pere $x$, germana $2x-3$, pare $x+25$; \ suma: $x+(2x-3)+(x+25)=\res{4x+22}$", r"$(x+4)+(2x+1)+(x+29)=\res{4x+34}$", r"$4\cdot12+22=\res{70}$ anys"])),
 (2, r"Un aparcament cobra 1,80 € per entrar i 0,05 € per cada minut. Escriu l'expressió del preu d'una estada de $x$ minuts i calcula quant costen 2 hores.",
     r"Preu $=0{,}05x+1{,}80$. \ 2 h $=120$ min: \ $0{,}05\cdot120+1{,}80=\res{7{,}80\text{ €}}$."),
 (3, r"Fes servir el llenguatge algebraic per a demostrar que:" + tasks(1, [r"Si a un nombre li sumem el seu doble, el resultat sempre és múltiple de 3.", r"La suma de dos nombres parells sempre és parell.", r"La suma de dos nombres senars consecutius sempre és múltiple de 4."]),
     tasks(1, [r"$x+2x=\res{3x}$, \ que és múltiple de 3.", r"$2x+2y=\res{2(x+y)}$, \ que és el doble d'un enter: parell.", r"$(2x+1)+(2x+3)=4x+4=\res{4(x+1)}$, \ múltiple de 4."])),
]))
chk('x+(2x-3)+(x+25)', '4x+22'); chk('(x+4)+(2x+1)+(x+29)', '4x+34'); chk('(2x+1)+(2x+3)', '4(x+1)')
assert val('2x^2y-xy', x=1, y=-2) == -2 and val('x^2-2x', x=-3) == 15

# =====================================================================
MON = [('-8x^3', '-8', 'x^3', 3), ('a^2b', '1', 'a^2b', 3), (r'\tfrac{2}{3}xy^4', r'\tfrac{2}{3}', 'xy^4', 5), ('-y', '-1', 'y', 1), ('12', '12', r'\text{---}', 0), ('5x^2y^3z', '5', 'x^2y^3z', 6)]
S_.append(("Monomis", [
 (1, r"Copia i completa la taula:\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|C{2.6cm}|C{2.6cm}|C{2.6cm}|C{1.6cm}|}\hline\rowcolor{soft}\textbf{Monomi} & \textbf{Coeficient} & \textbf{Part literal} & \textbf{Grau}\\\hline "
     + ''.join(r'$%s$ & & & \\\hline ' % m for m, _, _, _ in MON) + r'\end{tabular}\par}'
     + recorda(r"El \textbf{grau} d'un monomi és la suma dels exponents de la part literal. Si no s'escriu el coeficient, val 1."),
     r"{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|C{2.6cm}|C{2.6cm}|C{2.6cm}|C{1.6cm}|}\hline\rowcolor{soft}\textbf{Monomi} & \textbf{Coeficient} & \textbf{Part literal} & \textbf{Grau}\\\hline "
     + ''.join(r'$%s$ & $\res{%s}$ & $\res{%s}$ & $\res{%d}$\\\hline ' % m for m in MON) + r'\end{tabular}\par}'),
 (1, r"Quines d'aquestes expressions són monomis? Justifica la resposta." + tasks(4, ['$-3x^4$', r'$\dfrac{5}{x}$', r'$\dfrac{x^2}{4}$', '$2x+y$', r'$\sqrt{x}$', '$7$', r'$x^{-2}y$', r'$-\tfrac12ab^2$']),
     tasks(2, [r"\res{Sí}", r"No: la $x$ divideix", r"\res{Sí}: coeficient $\tfrac14$", r"No: té dos termes", r"No: exponent no natural", r"\res{Sí}: grau 0", r"No: exponent negatiu", r"\res{Sí}"])),
 (1, r"Agrupa els monomis semblants:\quad $4x^2,\ \ -xy,\ \ 3x,\ \ -\tfrac12x^2,\ \ 5yx,\ \ x,\ \ 2x^2y,\ \ -x^2y,\ \ 9$.",
     r"$\res{\{4x^2,\ -\tfrac12x^2\}}\quad \res{\{-xy,\ 5yx\}}\quad \res{\{3x,\ x\}}\quad \res{\{2x^2y,\ -x^2y\}}\quad \res{\{9\}}$"),
 (2, r"Indica el grau de cada monomi respecte de cada variable i el grau total. Escriu, per a cadascun, un monomi semblant." + tasks(3, ['$-6x^2y^5$', '$ab^3c$', r'$\tfrac{3}{5}x^4y$']),
     tasks(1, [r"$x$: 2, $y$: 5; grau \res{7}. \ P. ex.\ $x^2y^5$", r"$a$: 1, $b$: 3, $c$: 1; grau \res{5}. \ P. ex.\ $-2ab^3c$", r"$x$: 4, $y$: 1; grau \res{5}. \ P. ex.\ $10x^4y$"])),
 (2, r"Calcula el valor numèric:" + tasks(3, [r'$-4x^3$ \ per a $x=-2$', r'$3xy^2$ \ per a $x=2,\ y=-1$', r'$\tfrac12x^2y$ \ per a $x=4,\ y=3$']),
     tasks(3, [r'$-4\cdot(-8)=\res{32}$', r'$3\cdot2\cdot1=\res{6}$', r'$\tfrac12\cdot16\cdot3=\res{24}$'])),
 (3, r"Resol:" + tasks(1, [r"Troba $k$ perquè el monomi $-2x^{k}y^3$ siga de grau 8.", r"Troba $m$ i $n$ perquè $5x^{m+1}y^2$ i $-3x^4y^{n-1}$ siguen semblants.", r"Escriu un monomi de grau 6 amb tres variables, coeficient $-\tfrac23$ i grau 3 respecte de $x$."]),
     tasks(1, [r"$k+3=8\Rightarrow\res{k=5}$", r"$m+1=4$ i $n-1=2$: \ $\res{m=3,\ n=3}$", r"P. ex.\ $\res{-\tfrac23x^3yz^2}$"])),
]))
assert val('-4x^3', x=-2) == 32 and val('3x*y^2', x=2, y=-1) == 6 and val('x^2*y/2', x=4, y=3) == 24

# =====================================================================
SUMS = [('3x+5x', None), ('7x^2-2x^2', None), ('-4ab+ab', 'a*b*(-4+1)'), ('2x^3-x^3+5x^3', None), ('xy-3xy-2xy', None), ('6a^2b-6a^2b', None)]
RED = ['3x^2-5x+x^2+2x', '4xy-2x+3xy+7x', '2a^2-a+5-a^2+3a-8', 'x^3-2x+3x^3+x^2-4x']
PRO = ['2x^3*5x^2', '(-3a^2)*(4a^3)', '(6xy^2)*(-2x^3y)', '(1/2x^4)*(8x)', '(-x^2y)*(-xy^3)*2x', '(-5ab)*(3a^2b^2)']
S_.append(("Operacions amb monomis", [
 (1, r"Calcula:" + ops([e[0] for e in SUMS], 3)[0] + recorda(r"Només es poden sumar i restar monomis \textbf{semblants}: sumem els coeficients i \textbf{no canviem} la part literal."),
     ops([e[0] for e in SUMS], 3)[1]),
 (1, r"Redueix els termes semblants:" + ops(RED, 2)[0], ops(RED, 2)[1]),
 (1, r"Multiplica:" + ops(PRO, 3)[0] + recorda(r"Per a multiplicar, multipliquem els coeficients i \textbf{sumem els exponents} de cada lletra: $x^m\cdot x^n=x^{m+n}$."), ops(PRO, 2)[1]),
 (2, r"Divideix. Indica si el resultat és un monomi." + tasks(3, ['$12x^5:(3x^2)$', '$(-20a^4b^3):(5a^2b)$', '$9x^3y^2:(-3x^3y)$', '$(-14x^6):(-7x^6)$', r'$6x^2y:(4x)$', '$4x^2:(8x^3)$']),
     tasks(3, [r'$\res{4x^3}$', r'$\res{-4a^2b^2}$', r'$\res{-3y}$', r'$\res{2}$', r'$\res{\tfrac32xy}$', r'$\tfrac12x^{-1}$: \res{no és monomi}'])),
 (2, r"Calcula les potències:" + ops(['(2x^3)^2', '(-3xy^2)^3', '(-x^2y)^4', ('(1/2 x)^2', '(x/2)^2')], 4)[0], ops(['(2x^3)^2', '(-3xy^2)^3', '(-x^2y)^4', ('(1/2 x)^2', '(x/2)^2')], 4)[1]),
 (2, r"Opera i simplifica (recorda la jerarquia):" + tasks(2, [r'$3x\cdot2x^2-4x^3$', r'$10x^5:(2x^2)+x\cdot x^2$', r'$(2x)^3-5x\cdot x^2$', r'$6a^2b:(3a)-ab\cdot4$']),
     tasks(2, [r'$6x^3-4x^3=\res{2x^3}$', r'$5x^3+x^3=\res{6x^3}$', r'$8x^3-5x^3=\res{3x^3}$', r'$2ab-4ab=\res{-2ab}$'])),
 (3, r"Troba el monomi que falta en cada cas:" + tasks(1, [r'$(\quad?\quad)\cdot3x^2=12x^5$', r'$20x^4y^2:(\quad?\quad)=-5x^2y$', r'$4x^3+(\quad?\quad)=-x^3$', r'$(\quad?\quad)^2=9x^6y^2$ \ (dues solucions)']),
     tasks(2, [r'$\res{4x^3}$', r'$\res{-4x^2y}$', r'$\res{-5x^3}$', r'$\res{3x^3y}$ \ o \ $\res{-3x^3y}$'])),
]))
chk('20x^4y^2/(-5x^2y)', '-4x^2y'); chk('(3x^3y)^2', '9x^6y^2'); chk('3x*2x^2-4x^3', '2x^3'); chk('10x^5/(2x^2)+x*x^2', '6x^3'); chk('(2x)^3-5x*x^2', '3x^3'); chk('6a^2b/(3a)-a*b*4', '-2a*b')
for q_, r_ in [('12x^5/(3x^2)', '4x^3'), ('(-20a^4b^3)/(5a^2b)', '-4a^2b^2'), ('9x^3y^2/(-3x^3y)', '-3y'), ('6x^2y/(4x)', '3x*y/2')]: chk(q_, r_)

# =====================================================================
PP = ['5x-3x^4+2-x^2', '7-x^3', '4x^2-3x+x^5', '-2+x']
def info(p):
    e = sp.Poly(S(p), x); cs = e.all_coeffs(); n = e.degree()
    nt = len([c for c in cs if c != 0])
    return r"$%s$; \ grau \res{%d}; \ %d termes; \ coef.\ princ.\ \res{%s}; \ t.\,i.\ \res{%s}" % (pt(p), n, nt, ntex(cs[0]), ntex(cs[-1]))
P4 = 'x^3-7x+6'
S_.append(("Polinomis", [
 (1, r"Per a cada polinomi: ordena'l, i indica'n el grau, el nombre de termes, el coeficient principal i el terme independent." + tasks(2, ['$P(x)=%s$' % tx(p) for p in PP])
     + recorda(r"El \textbf{grau} d'un polinomi és el grau del terme de grau més alt. El \textbf{terme independent} és el que no té lletra."),
     tasks(1, [info(p) for p in PP])),
 (1, r"Quins polinomis de l'exercici anterior són complets? Escriu els incomplets en forma completa (amb coeficients 0).",
     r"Cap no és complet, excepte $x-2$. \ $-3x^4+0x^3-x^2+5x+2$; \ $-x^3+0x^2+0x+7$; \ $x^5+0x^4+0x^3+4x^2-3x+0$."),
 (1, r"Siga $P(x)=2x^3-x^2+3x-4$. Calcula:" + tasks(4, ['$P(0)$', '$P(1)$', '$P(-2)$', r'$P\!\left(\tfrac12\right)$']),
     tasks(4, [r'$\res{%s}$' % ntex(val('2x^3-x^2+3x-4', x=v)) for v in ['0', '1', '-2', '1/2']])),
 (2, r"Indica el grau de cada polinomi:" + tasks(3, ['$3x^2y^3-xy+5$', '$a^4-2a^2b^3+b$', '$x^2y^2-x^3+7xy$']),
     tasks(3, [r'\res{5}', r'\res{5}', r'\res{4}'])),
 (2, r"Comprova quins dels nombres $1,\ -1,\ 2,\ -2,\ 3$ i $-3$ són arrels del polinomi $P(x)=%s$." % tx(P4),
     r"$P(1)=0$, \ $P(-1)=12$, \ $P(2)=0$, \ $P(-2)=12$, \ $P(3)=12$, \ $P(-3)=0$. \ Arrels: $\res{1,\ 2\ \text{i}\ -3}$."),
 (3, r"Resol:" + tasks(1, [r"Troba $m$ perquè $P(x)=2x^3-mx+4$ complisca $P(-2)=0$.", r"Troba $k$ perquè el polinomi $Q(x)=x^2+kx-6$ tinga per arrel $x=3$.", r"Escriu un polinomi de grau 4, incomplet, amb coeficient principal $-1$ i tal que $P(0)=5$."]),
     tasks(1, [r"$-16+2m+4=0\Rightarrow\res{m=6}$", r"$9+3k-6=0\Rightarrow\res{k=-1}$", r"P. ex.\ $\res{-x^4+2x^2+5}$"])),
]))
assert [val(P4, x=v) for v in [1, -1, 2, -2, 3, -3]] == [0, 12, 0, 12, 12, 0]
assert val('2x^3-6x+4', x=-2) == 0 and val('x^2-x-6', x=3) == 0

# =====================================================================
P5, Q5, R5 = '3x^3-2x^2+x-5', '-x^3+4x^2-6', '2x^2-3x+1'
def sumsol(e): return r'$%s$' % pt(e)
S_.append(("Suma i resta de polinomis", [
 (1, r"Siguen els polinomis $P(x)=%s$, \ $Q(x)=%s$ \ i \ $R(x)=%s$. Calcula:" % (pt(P5), pt(Q5), pt(R5)) + tasks(4, ['$P+Q$', '$P-Q$', '$Q+R$', '$R-P$'])
     + recorda(r"Per a restar, sumem l'\textbf{oposat}: canviem el signe de \textbf{tots} els termes del polinomi que restem."),
     tasks(2, [r'$P+Q=\res{%s}$' % pt('(%s)+(%s)' % (P5, Q5)), r'$P-Q=\res{%s}$' % pt('(%s)-(%s)' % (P5, Q5)), r'$Q+R=\res{%s}$' % pt('(%s)+(%s)' % (Q5, R5)), r'$R-P=\res{%s}$' % pt('(%s)-(%s)' % (R5, P5))])),
 (1, r"Fes aquestes sumes i restes col·locant els termes semblants en columna:" + tasks(1, [r'$(4x^4-3x^2+2x)+(x^3+5x^2-2x+7)$', r'$(x^3-6x+1)-(2x^3+x^2-6x-4)$']),
     tasks(1, [r'$\res{%s}$' % pt('(4x^4-3x^2+2x)+(x^3+5x^2-2x+7)'), r'$\res{%s}$' % pt('(x^3-6x+1)-(2x^3+x^2-6x-4)')])),
 (2, r"Amb els polinomis de l'exercici @S5E1@, calcula:" + tasks(3, ['$P-Q+R$', '$P-(Q-R)$', '$P-(Q+R)$']),
     tasks(3, [r'$\res{%s}$' % pt('(%s)-(%s)+(%s)' % (P5, Q5, R5)), r'$\res{%s}$' % pt('(%s)-((%s)-(%s))' % (P5, Q5, R5)), r'$\res{%s}$' % pt('(%s)-((%s)+(%s))' % (P5, Q5, R5))])),
 (2, r"Amb els polinomis de l'exercici @S5E1@, calcula $2P+3Q$ i $P-2R$.",
     r'$2P+3Q=\res{%s}$; \quad $P-2R=\res{%s}$' % (pt('2(%s)+3(%s)' % (P5, Q5)), pt('(%s)-2(%s)' % (P5, R5)))),
 (2, r"Opera i redueix:" + tasks(1, [r'$(5x^2y-3xy+y^2)-(2x^2y+xy-4y^2)$', r'$(a^2-2ab+b^2)+(a^2+2ab+b^2)-(2a^2-b^2)$']),
     tasks(2, [r'$\res{%s}$' % pt('(5x^2y-3xy+y^2)-(2x^2y+xy-4y^2)'), r'$\res{%s}$' % pt('(a^2-2ab+b^2)+(a^2+2ab+b^2)-(2a^2-b^2)')])),
 (3, r"Troba el polinomi $X(x)$ en cada cas:" + tasks(1, [r'$P(x)+X(x)=Q(x)$, \ amb $P$ i $Q$ els de l\'exercici @S5E1@.', r'$(2x^3+x-1)-X(x)=x^3-4x^2+3$']),
     tasks(1, [r'$X=Q-P=\res{%s}$' % pt('(%s)-(%s)' % (Q5, P5)), r'$X=(2x^3+x-1)-(x^3-4x^2+3)=\res{%s}$' % pt('(2x^3+x-1)-(x^3-4x^2+3)')])),
]))

# =====================================================================
S_.append(("Producte de polinomis", [
 (1, r"Multiplica:" + ops(['3x(2x^2-5x+4)', '-2x^2(x^3-3x+1)', '4ab(a-2b)', '-x(x^2-x-1)'], 2)[0]
     + recorda(r"Multipliquem el monomi per \textbf{cada terme} del polinomi (propietat distributiva)."), ops(['3x(2x^2-5x+4)', '-2x^2(x^3-3x+1)', '4ab(a-2b)', '-x(x^2-x-1)'], 2)[1]),
 (1, r"Multiplica:" + ops(['(x+3)(x+5)', '(x-4)(x+2)', '(2x-1)(x-3)', '(3x+2)(2x-5)'], 2)[0], ops(['(x+3)(x+5)', '(x-4)(x+2)', '(2x-1)(x-3)', '(3x+2)(2x-5)'], 2)[1]),
 (2, r"Multiplica:" + ops(['(x^2-3x+2)(x+4)', '(2x^2+x-1)(x-3)', '(x^3-2x+1)(x^2+x)', '(x^2+x+1)(x^2-x+1)'], 1)[0], ops(['(x^2-3x+2)(x+4)', '(2x^2+x-1)(x-3)', '(x^3-2x+1)(x^2+x)', '(x^2+x+1)(x^2-x+1)'], 1)[1]),
 (2, r"Siguen $P(x)=x^2-2x+3$ i $Q(x)=2x-1$. Calcula $P\cdot Q$ i $Q\cdot Q$. Quin grau té cada producte?",
     r'$P\cdot Q=\res{%s}$ (grau 3); \quad $Q\cdot Q=\res{%s}$ (grau 2)' % (pt('(x^2-2x+3)(2x-1)'), pt('(2x-1)^2'))),
 (2, r"Opera i redueix:" + tasks(1, [r'$2x(x-3)-(x+1)(x-2)$', r'$(x+4)(x-1)-x(x+3)$', r'$3(x^2-1)-(2x+1)(x-2)$']),
     tasks(1, [r'$\res{%s}$' % pt('2x(x-3)-(x+1)(x-2)'), r'$\res{%s}$' % pt('(x+4)(x-1)-x(x+3)'), r'$\res{%s}$' % pt('3(x^2-1)-(2x+1)(x-2)')])),
 (3, r"Calcula $(x-1)(x+2)(x+3)$ i $(x+1)(x-1)(x^2+1)$.",
     r'$\res{%s}$; \quad $\res{%s}$' % (pt('(x-1)(x+2)(x+3)'), pt('(x+1)(x-1)(x^2+1)'))),
 (3, r"D'una planxa rectangular de $(2x+3)$ cm per $(x+4)$ cm en retallem un quadrat de costat $x$ cm. Escriu com a polinomi l'àrea que queda i calcula-la per a $x=5$.",
     r'$(2x+3)(x+4)-x^2=\res{%s}$; \ per a $x=5$: \ $\res{%s\text{ cm}^2}$' % (pt('(2x+3)(x+4)-x^2'), val('(2x+3)(x+4)-x^2', x=5))),
]))

# =====================================================================
ID1 = ['(x+3)^2', '(x-5)^2', '(x+4)(x-4)', '(a+1)^2', '(x-1)^2', '(y+7)(y-7)']
ID2 = ['(2x+5)^2', '(3x-1)^2', '(2x+3y)(2x-3y)', '(x^2-2)^2', ('(1/2x+2)^2', '(x/2+2)^2'), '(-x-3)^2']
FAC = [('x^2+6x+9', '(x+3)^2'), ('x^2-10x+25', '(x-5)^2'), ('x^2-81', '(x+9)(x-9)'), ('4x^2+4x+1', '(2x+1)^2'), ('9x^2-16', '(3x+4)(3x-4)'), ('25x^2-30x+9', '(5x-3)^2')]
S_.append(("Identitats notables", [
 (1, r"Desenvolupa:" + ops(ID1, 3)[0] + recorda(r"$(a+b)^2=a^2+2ab+b^2$, \quad $(a-b)^2=a^2-2ab+b^2$, \quad $(a+b)(a-b)=a^2-b^2$."), ops(ID1, 2)[1]),
 (2, r"Desenvolupa:" + ops(ID2, 3)[0], ops(ID2, 2)[1]),
 (2, r"Expressa com a quadrat d'un binomi o com a suma per diferència:" + tasks(3, ['$%s$' % f for f, _ in FAC]),
     tasks(3, [r'$\res{%s}$' % g for _, g in FAC])),
 (2, r"Completa:" + tasks(1, [r'$(x+\ \square\ )^2=x^2+\ \square\ +49$', r'$(\ \square\ -3)^2=4x^2-\ \square\ +9$', r'$(x+\ \square\ )(x-\ \square\ )=x^2-64$', r'$(3x+\ \square\ )^2=\ \square\ +12x+\ \square$']),
     tasks(1, [r'$(x+\res{7})^2=x^2+\res{14x}+49$', r'$(\res{2x}-3)^2=4x^2-\res{12x}+9$', r'$(x+\res{8})(x-\res{8})=x^2-64$', r'$(3x+\res{2})^2=\res{9x^2}+12x+\res{4}$'])),
 (2, r"Opera i simplifica:" + tasks(1, [r'$(x+2)^2-(x-2)^2$', r'$(x+3)(x-3)-(x-3)^2$', r'$2(x+1)^2-(x+1)(x-1)$']),
     tasks(1, [r'$\res{%s}$' % pt('(x+2)^2-(x-2)^2'), r'$\res{%s}$' % pt('(x+3)(x-3)-(x-3)^2'), r'$\res{%s}$' % pt('2(x+1)^2-(x+1)(x-1)')])),
 (3, r"Calcula mentalment amb les identitats notables:" + tasks(4, ['$101^2$', '$99^2$', r'$51\cdot49$', r'$1002^2$']),
     tasks(2, [r'$(100+1)^2=10\,000+200+1=\res{10\,201}$', r'$(100-1)^2=10\,000-200+1=\res{9801}$', r'$(50+1)(50-1)=2500-1=\res{2499}$', r'$(1000+2)^2=\res{1\,004\,004}$'])),
 (3, r"Demostra que la diferència entre els quadrats de dos nombres consecutius sempre és un nombre senar.",
     r"$(x+1)^2-x^2=x^2+2x+1-x^2=\res{2x+1}$, \ que és senar."),
]))
for f_, g_ in FAC: chk(f_, g_)
chk('(x+7)^2', 'x^2+14x+49'); chk('(2x-3)^2', '4x^2-12x+9'); chk('(3x+2)^2', '9x^2+12x+4'); chk('(x+8)(x-8)', 'x^2-64')
assert 101**2 == 10201 and 99**2 == 9801 and 51 * 49 == 2499 and 1002**2 == 1004004

# =====================================================================
FC1 = [('5x^2-15x', '5x(x-3)'), ('8x^3+12x^2', '4x^2(2x+3)'), ('6x^4-9x^3+3x^2', '3x^2(2x^2-3x+1)'), ('7x-14', '7(x-2)'), ('x^5-x^3+x^2', 'x^2(x^3-x+1)'), ('10x^3-4x', '2x(5x^2-2)')]
FC2 = [('6x^2y-9xy^2', '3xy(2x-3y)'), ('4a^3b^2+2a^2b', '2a^2b(2ab+1)'), ('12x^2y^3-8xy^2+4xy', '4xy(3xy^2-2y+1)'), ('15a^2-10ab+5a', '5a(3a-2b+1)')]
FC3 = [('x(x-2)+5(x-2)', '(x-2)(x+5)'), ('3(x+1)-x(x+1)', '(x+1)(3-x)'), ('2x(x+4)-(x+4)', '(x+4)(2x-1)')]
FC4 = [('x^3-4x', 'x(x+2)(x-2)'), ('2x^2-8x+8', '2(x-2)^2'), ('3x^3+6x^2+3x', '3x(x+1)^2'), ('x^4-16x^2', 'x^2(x+4)(x-4)'), ('5x^2-45', '5(x+3)(x-3)'), ('x^3-x', 'x(x+1)(x-1)')]
def fcs(lst, n): return tasks(n, ['$%s$' % tx(f) for f, _ in lst]), tasks(min(n, 2), [r'$%s=\res{%s}$' % (tx(f), tx(g)) for f, g in lst])
S_.append(("Extracció de factor comú", [
 (1, r"Trau factor comú:" + fcs(FC1, 3)[0] + recorda(r"Factor comú: el MCD dels coeficients i les lletres que estan en \textbf{tots} els termes amb el \textbf{menor} exponent. Comprova-ho multiplicant!"), fcs(FC1, 3)[1]),
 (1, r"Trau factor comú:" + fcs(FC2, 2)[0], fcs(FC2, 2)[1]),
 (2, r"Trau factor comú un binomi:" + fcs(FC3, 3)[0], fcs(FC3, 3)[1]),
 (2, r"Factoritza al màxim: primer trau factor comú i després aplica una identitat notable." + fcs(FC4, 3)[0], fcs(FC4, 2)[1]),
 (3, r"Calcula de la manera més ràpida traient factor comú:" + tasks(3, [r'$13\cdot47+13\cdot53$', r'$98^2+2\cdot98$', r'$37\cdot25+37\cdot75$']),
     tasks(3, [r'$13\cdot100=\res{1300}$', r'$98\cdot100=\res{9800}$', r'$37\cdot100=\res{3700}$'])),
 (3, r"A un rectangle de costats $x$ i $x+3$ li llevem un rectangle de costats $3$ i $x+3$. Escriu l'àrea que queda, trau factor comú i comprova que és una diferència de quadrats.",
     r"$x(x+3)-3(x+3)=\res{(x+3)(x-3)}=x^2-9$."),
]))
for lst in (FC1, FC2, FC3, FC4): [chk(f, g) for f, g in lst]
chk('x(x+3)-3(x+3)', 'x^2-9')

# =====================================================================
DV1 = [('x^2+7x+10', 'x+2'), ('x^2-3x+5', 'x-1'), ('2x^2+x-3', 'x-1')]
DV2 = [('x^3-2x^2+3x-1', 'x-2'), ('3x^3+x-4', 'x+1')]
DV3 = [('x^4-2x^3+x-3', 'x^2+1'), ('2x^4+x^3-3x^2+x', 'x^2-x+2')]
def dq(lst, n): return tasks(n, ['$(%s):(%s)$' % (tx(D), tx(d)) for D, d in lst])
def ds(lst): return tasks(1, [dvsol(D, d) for D, d in lst])
S_.append(("Divisió de polinomis", [
 (1, r"Fes aquestes divisions i indica el quocient i el residu:" + dq(DV1, 3) + recorda(r"Seguim dividint fins que el grau del residu siga \textbf{menor} que el del divisor. Comprovació: $D=d\cdot C+R$."), ds(DV1)),
 (1, r"Divideix. Compte amb els termes que falten en el dividend:" + dq(DV2, 2), ds(DV2)),
 (2, r"Divideix:" + dq(DV3, 1), ds(DV3)),
 (2, r"Divideix $(6x^3-x^2+4x-5):(2x-1)$ i comprova el resultat amb la prova de la divisió.",
     dvsol('6x^3-x^2+4x-5', '2x-1') + r". \ Prova: $(2x-1)(%s)+(%s)=%s$." % (pt(dv('6x^3-x^2+4x-5', '2x-1')[0]), pt(dv('6x^3-x^2+4x-5', '2x-1')[1]), pt('6x^3-x^2+4x-5'))),
 (2, r"En una divisió de polinomis, el divisor és $x^2-3$, el quocient $2x+1$ i el residu $x-4$. Quin és el dividend?",
     r"$D=(x^2-3)(2x+1)+(x-4)=\res{%s}$" % pt('(x^2-3)(2x+1)+(x-4)')),
 (3, r"En dividir $D(x)=x^3+x^2-3x+5$ entre un polinomi $d(x)$ obtenim de quocient $x+2$ i de residu $-2x+3$. Troba $d(x)$.",
     r"$D-R=x^3+x^2-x+2=d\cdot(x+2)$, \ i dividint: \ $d(x)=\res{%s}$." % pt(dv('x^3+x^2-x+2', 'x+2')[0])),
]))
assert dv('x^3+x^2-x+2', 'x+2')[1] == 0 and sp.expand(S('(x^2-x+1)(x+2)+(-2x+3)') - S('x^3+x^2-3x+5')) == 0

# =====================================================================
RF1 = [('x^3-3x^2+2x-4', 2), ('x^2+6x+5', -1), ('2x^3-5x^2+x+3', 3)]
RF2 = [('x^4-3x^2+2x-1', -2), ('3x^3-4x+5', 1)]
RF3 = [('x^4-16', 2), ('x^5+1', -1)]
def rq(lst, n): return tasks(n, ['$(%s):(x%s)$' % (tx(D), '-%d' % r if r > 0 else '+%d' % -r) for D, r in lst])
def rs(lst): return tasks(1, [rufsol(D, r) for D, r in lst])
P10 = 'x^3-3x^2-4x+12'
S_.append(("Regla de Ruffini", [
 (1, r"Divideix aplicant la regla de Ruffini:" + rq(RF1, 2) + recorda(r"Escriu els coeficients del dividend \textbf{ordenat i complet}. Si el divisor és $x-a$, a l'esquerra posem $a$ (per a $x+2$ posem $-2$)."), rs(RF1)),
 (1, r"Divideix per Ruffini. Compte amb els termes que falten:" + rq(RF2, 2), rs(RF2)),
 (2, r"Divideix per Ruffini:" + rq(RF3, 2), rs(RF3)),
 (2, r"Calcula, sense fer la divisió, el residu de:" + tasks(3, [r'$(x^3-5x+7):(x+3)$', r'$(2x^4-x^2+1):(x-1)$', r'$(x^{5}-2x^3+x):(x+2)$']),
     tasks(3, [r'$P(-3)=\res{%s}$' % val('x^3-5x+7', x=-3), r'$P(1)=\res{%s}$' % val('2x^4-x^2+1', x=1), r'$P(-2)=\res{%s}$' % val('x^5-2x^3+x', x=-2)])),
 (2, r"Comprova, amb el teorema del residu, quins dels nombres $1,\ -1,\ 2,\ -2,\ 3,\ -3$ són arrels de $P(x)=%s$." % tx(P10),
     r"$P(2)=0$, \ $P(-2)=0$ \ i \ $P(3)=0$: \ arrels \res{2,\ -2\ \text{i}\ 3}. \ Les altres no ($P(1)=6$, $P(-1)=12$, $P(-3)=-30$)."),
 (3, r"Resol:" + tasks(1, [r"Troba $k$ perquè la divisió $(2x^3+kx^2-x+3):(x+1)$ siga exacta.", r"Troba $m$ perquè el residu de $(x^3-mx+4):(x-2)$ siga 4."]),
     tasks(1, [r"$P(-1)=-2+k+1+3=k+2=0\Rightarrow\res{k=-2}$", r"$P(2)=8-2m+4=4\Rightarrow\res{m=4}$"])),
 (3, r"Comprova que $x=1$ és una arrel de $P(x)=x^3-2x^2-x+2$. Divideix per Ruffini entre $x-1$ i, aplicant Ruffini una altra vegada al quocient, escriu $P(x)$ com a producte de tres factors de grau 1.",
     r"$%s$ \ $\Rightarrow$ \ $x^2-x-2$; \ i amb $x=-1$: \ $%s$\par\smallskip $P(x)=\res{(x-1)(x+1)(x-2)}$" % (ruf('x^3-2x^2-x+2', 1)[0], ruf('x^2-x-2', -1)[0])),
]))
assert [val(P10, x=v) for v in [1, -1, 2, -2, 3, -3]] == [6, 12, 0, 0, 0, -30]
assert val('2x^3-2x^2-x+3', x=-1) == 0 and val('x^3-4x+4', x=2) == 4
chk('(x-1)(x+1)(x-2)', 'x^3-2x^2-x+2'); assert ruf('x^3-2x^2-x+2', 1)[2] == 0 and ruf('x^2-x-2', -1)[2] == 0

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={llenguatge algebraic, monomis, polinomis, suma, resta, producte, identitats notables, factor comú, divisió de polinomis, regla de Ruffini}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 4: Àlgebra. Polinomis. 3r d'ESO}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 4: Àlgebra · 3r d'ESO" % t)
    assert 'Unitat 4' in p and 'unitat 4' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{3r ESO}{''' + ('Solucions de la fitxa · Unitat 4' if sol else "Fitxa d'exercicis · Unitat 4") + r'''}{Àlgebra. Polinomis}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs calculadores pas a pas de cada procediment."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i dona els polinomis ordenats de major a menor grau. Fes els càlculs sense calculadora.") + r'''
\end{tcolorbox}
''')
    num, k = {}, 0
    for i, (_, exs) in enumerate(S_, 1):
        for j in range(1, len(exs) + 1):
            k += 1; num['@S%dE%d@' % (i, j)] = str(k)
    ref = lambda t: re.sub(r'@S\d+E\d+@', lambda m: num[m.group(0)], t)
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, ref(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't4-fitxa-solucions.tex' if sol else 't4-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
