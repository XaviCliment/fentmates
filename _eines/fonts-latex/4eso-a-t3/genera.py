# Genera t3-fitxa-exercicis.tex i t3-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 3: Polinomis)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució), en valencià i castellà amb T(va, es).
# Les eines comunes (tasks, recorda, ck, eq, build) són a ../comu/eso4b.py, com a les fitxes de 4t ESO B;
# build(..., curs='4eso-a') posa la capçalera de Matemàtiques A. Totes les solucions les calcula sympy:
# pt() escriu un polinomi ordenat, fac() la factorització, rft() la taula de Ruffini, dv() la divisió entera,
# i fe() comprova les solucions que s'escriuen a mà.
# Ús: python3 genera.py (valencià) i python3 genera-es.py (castellà); després pdflatex dues vegades cada .tex.
import os, sys
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

LANG = 'es' if (len(sys.argv) > 1 and sys.argv[1] == 'es') else 'va'
def T(va, es): return es if LANG == 'es' else va

x, y, k, m, a = sp.symbols('x y k m a')
LOC = {'x': x, 'y': y, 'k': k, 'm': m, 'a': a}
def E(s): return sp.sympify(s, locals=LOC) if isinstance(s, str) else s
def fe(p, q): assert sp.expand(E(p) - E(q)) == 0, (p, q)
def tl(v):
    v = sp.Rational(v)
    if v.q == 1: return str(v.p)
    return ('-' if v < 0 else '') + r'\frac{%d}{%d}' % (abs(v.p), v.q)
def pt(e):
    """polinomi en x, ordenat de major a menor grau"""
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
def fac(e):
    """factorització amb coeficients enters: constant, x^k i factors ordenats per l'arrel"""
    e = E(e); c, L = sp.factor_list(e)
    def key(fm):
        if fm[0] == x: return (-1, 0)
        f = sp.Poly(fm[0], x); d = f.degree()
        if d == 1: return (0, -f.all_coeffs()[1] / f.all_coeffs()[0])
        return (d, 0)
    L = sorted(L, key=key)
    parts = []
    for f, mm in L:
        s = pt(f); p = s if s == 'x' else '(' + s + ')'
        parts.append(p + ('^{%d}' % mm if mm > 1 else ''))
    ct = '' if c == 1 else '-' if c == -1 else tl(c)
    out = ct + ''.join(parts)
    assert sp.expand(c * sp.Mul(*[f ** mm for f, mm in L]) - e) == 0
    return out
def rft(P, av):
    """taula de Ruffini de P(x):(x-a); torna (tex, quocient, residu)"""
    P = E(P); av = sp.Rational(av)
    cs = [sp.Rational(c) for c in sp.Poly(P, x).all_coeffs()]
    r2, r3 = [], [cs[0]]
    for c in cs[1:]:
        p = r3[-1] * av; r2.append(p); r3.append(c + p)
    n = len(cs)
    tex = r'\begin{array}{r|%s|r} & %s\\ %s & & %s\\ \hline & %s\end{array}' % ('r' * (n - 1), ' & '.join(map(tl, cs)), tl(av), ' & '.join(map(tl, r2)), ' & '.join(map(tl, r3)))
    q = sum(r3[i] * x ** (n - 2 - i) for i in range(n - 1)); r = r3[-1]
    qq, rr = sp.div(P, x - av, x)
    assert sp.expand(qq - q) == 0 and rr == r
    return tex, q, r
def dv(D, d):
    q, r = sp.div(E(D), E(d), x)
    assert sp.expand(q * E(d) + r - E(D)) == 0
    return q, r
def val(P, v): return E(P).subs(x, sp.Rational(v))
def sub(P, v):
    """P(v) amb la substitució escrita: 2\\cdot(-1)^3-..."""
    P = sp.expand(E(P)); v = sp.Rational(v); V = tl(v)
    V = '(' + V + ')' if (v < 0 or v.q != 1) else V
    cs = sp.Poly(P, x).all_coeffs(); n = len(cs) - 1; out = ''
    for i, cc in enumerate(cs):
        cc = sp.Rational(cc); kk = n - i
        if cc == 0: continue
        s = '-' if cc < 0 else ('+' if out else ''); aa = abs(cc)
        pw = '' if kk == 0 else V if kk == 1 else V + '^{%d}' % kk
        out += s + (tl(aa) if kk == 0 else ('' if aa == 1 else tl(aa) + r'\cdot ') + pw)
    return out
def Tk(items, n=2, **kw): return tasks(n, items, **kw)
def cr(q, r): return r'$c(x)=' + Rm(pt(q)) + r',\ \ r=' + Rm(pt(r)) + '$'

S = []

# =====================================================================
# 1. Monomis
mons = [(r"-3x^4", "-3", "x^4", "4"), (r"x^2y", "1", "x^2y", "3"), (r"\frac25x", r"\frac25", "x", "1"), (r"-a^3b^2", "-1", "a^3b^2", "5"), (r"8", "8", "", "0"), (r"-x", "-1", "x", "1")]
def tmon(sol):
    h = r'\begin{center}\renewcommand{\arraystretch}{1.5}\begin{tabular}{|C{2.4cm}|C{2.6cm}|C{2.6cm}|C{1.6cm}|}\hline\rowcolor{soft}\textbf{' + T('Monomi', 'Monomio') + r'} & \textbf{' + T('Coeficient', 'Coeficiente') + r'} & \textbf{Part literal} & \textbf{' + T('Grau', 'Grado') + r'}\\\hline'
    if LANG == 'es': h = h.replace('Part literal', 'Parte literal')
    for r in mons:
        cells = [('$\\res{%s}$' % v if v else '\\rest{' + T('no en té', 'no tiene') + '}') if sol else '' for v in r[1:]]
        h += '$%s$ & %s\\\\\\hline' % (r[0], ' & '.join(cells))
    return h + r'\end{tabular}\end{center}'
red = ['5*x+3*x-x', '4*x**2-7*x**2+x**2', '2*x**3+5*x-x**3+3*x', '3*x**2-2*x+5-x**2+4*x-8', 'Rational(1,2)*x+Rational(3,4)*x', '6*x*y-2*x*y+x*y']
redT = [r"$5x+3x-x$", r"$4x^2-7x^2+x^2$", r"$2x^3+5x-x^3+3x$", r"$3x^2-2x+5-x^2+4x-8$", r"$\frac12x+\frac34x$", r"$6xy-2xy+xy$"]
redS = [r"7x", r"-2x^2", r"x^3+8x", r"2x^2+2x-3", r"\frac54x", r"5xy"]
for e, s in zip(red, ['7*x', '-2*x**2', 'x**3+8*x', '2*x**2+2*x-3', 'Rational(5,4)*x', '5*x*y']): fe(e, s)
prd = [('3*x**2*4*x**3', r"3x^2\cdot4x^3", r"12x^5"), ('(-2*x)*5*x**4', r"(-2x)\cdot5x^4", r"-10x^5"), ('(-x**3)*(-6*x**2)', r"(-x^3)\cdot(-6x^2)", r"6x^5"),
       ('Rational(2,3)*x*Rational(9,4)*x**2', r"\frac23x\cdot\frac94x^2", r"\frac32x^3"), ('4*x**2*y*3*x*y**3', r"4x^2y\cdot3xy^3", r"12x^3y^4"), ('2*x*(-3*x)*x**2', r"2x\cdot(-3x)\cdot x^2", r"-6x^4")]
for (e, _, _), s in zip(prd, ['12*x**5', '-10*x**5', '6*x**5', 'Rational(3,2)*x**3', '12*x**3*y**4', '-6*x**4']): fe(e, s)
quo = [('12*x**5/(3*x**2)', r"12x^5:3x^2", r"4x^3"), ('-20*x**6/(4*x)', r"-20x^6:4x", r"-5x^5"), ('9*x**4/(-3*x**4)', r"9x^4:(-3x^4)", r"-3"),
       ('(2*x**3)**2', r"(2x^3)^2", r"4x^6"), ('(-3*x**2)**3', r"(-3x^2)^3", r"-27x^6"), ('(Rational(1,2)*x)**4', r"\left(\frac12x\right)^4", r"\frac1{16}x^4")]
for (e, _, _), s in zip(quo, ['4*x**3', '-5*x**5', '-3', '4*x**6', '-27*x**6', 'Rational(1,16)*x**4']): fe(sp.simplify(E(e)), s)
vm = [(E('-2*x**3'), r"-2x^3", ['-1', '2', '1/2']), (E('Rational(3,4)*x**2'), r"\frac34x^2", ['-2', '0', '4'])]
S.append((T("Monomis", "Monomios"), [
 (1, T("Completa la taula:", "Completa la tabla:") + tmon(False), tmon(True)),
 (1, T(r"Agrupa els monomis semblants: \ $3x^2$, \ $-5x$, \ $x^3$, \ $7x^2$, \ $2x$, \ $-x^3$, \ $\frac12x^2$.", r"Agrupa los monomios semejantes: \ $3x^2$, \ $-5x$, \ $x^3$, \ $7x^2$, \ $2x$, \ $-x^3$, \ $\frac12x^2$."),
     R(r"\left\{3x^2,\ 7x^2,\ \tfrac12x^2\right\}") + r", \ " + R(r"\left\{-5x,\ 2x\right\}") + r", \ " + R(r"\left\{x^3,\ -x^3\right\}") + T(" (la mateixa part literal).", " (la misma parte literal).")),
 (1, T("Redueix:", "Reduce:") + Tk(redT, 3) + recorda(T("Només se sumen o resten els monomis semblants: se sumen els coeficients i es deixa la mateixa part literal.", "Solo se suman o restan los monomios semejantes: se suman los coeficientes y se deja la misma parte literal.")),
     Tk([R(s) for s in redS], 3)),
 (1, T("Calcula:", "Calcula:") + Tk(['$' + q + '$' for _, q, _ in prd], 3) + recorda(T(r"En el producte, es multipliquen els coeficients i se sumen els exponents de cada lletra: $x^2\cdot x^3=x^5$.", r"En el producto, se multiplican los coeficientes y se suman los exponentes de cada letra: $x^2\cdot x^3=x^5$.")),
     Tk([R(s) for _, _, s in prd], 3)),
 (2, T("Calcula:", "Calcula:") + Tk(['$' + q + '$' for _, q, _ in quo], 3),
     Tk([R(s) for _, _, s in quo], 3)),
 (2, T("Calcula el valor numèric de cada monomi per als valors indicats:", "Calcula el valor numérico de cada monomio para los valores indicados:")
     + Tk([r"$%s$ \ %s \ $x=%s$" % (t, T("per a", "para"), ',\\ '.join(tl(sp.Rational(v)) for v in vs)) for _, t, vs in vm], 1),
     Tk([r"$" + r";\ \ ".join(r"%s=%s" % (sub(p, v), Rm(tl(val(p, v)))) for v in vs) + "$" for p, t, vs in vm], 1)),
]))

# =====================================================================
# 2. Polinomis i valor numèric
tb = [(r"P(x)=3x^2-5x^4+x-7", "-5x^4+3x^2+x-7", "4", "-7", "-5", T("No", "No")), (r"Q(x)=6-2x+x^3", "x^3-2x+6", "3", "6", "1", T("No", "No")),
      (r"R(x)=4x-x^2+1", "-x^2+4x+1", "2", "1", "-1", T("Sí", "Sí")), (r"S(x)=2x^5+x^2-3x", "2x^5+x^2-3x", "5", "0", "2", T("No", "No")), (r"U(x)=\frac12x^3-x^2+3x-2", r"\frac12x^3-x^2+3x-2", "3", "-2", r"\frac12", T("Sí", "Sí"))]
def tpol(sol):
    h = r'\begin{center}\renewcommand{\arraystretch}{1.5}\small\begin{tabular}{|l|C{3.7cm}|C{1.1cm}|C{1.5cm}|C{1.6cm}|C{1.95cm}|}\hline\rowcolor{soft}\textbf{' + T('Polinomi', 'Polinomio') + r'} & \textbf{' + T('Ordenat', 'Ordenado') + r'} & \textbf{' + T('Grau', 'Grado') + r'} & \textbf{' + T('Terme indep.', 'Térm. indep.') + r'} & \textbf{' + T('Coef. princ.', 'Coef. princ.') + r'} & \textbf{' + T('Complet?', '¿Completo?') + r'}\\\hline'
    for r in tb: h += '$%s$ & %s\\\\\\hline' % (r[0], ' & '.join(('$\\res{%s}$' % v if i < 4 else '\\rest{%s}' % v) if sol else '' for i, v in enumerate(r[1:])))
    return h + r'\end{tabular}\end{center}'
for p, q in [('3*x**2-5*x**4+x-7', '-5*x**4+3*x**2+x-7'), ('6-2*x+x**3', 'x**3-2*x+6'), ('4*x-x**2+1', '-x**2+4*x+1')]: fe(p, q)
P23 = 'x**3-2*x**2+4*x-1'; v23 = ['0', '1', '-1', '2', '-2']
P24 = ['2*x**2-5*x+3', '-x**3+4*x', 'x**4-3*x**2+2']; v24 = ['3', '-1', '0']
k25 = sp.solve(val('2*x**3-k*x+5', 2) - 9, k)[0]; a26 = sp.solve(val('x**2+a*x-4', -1) + 6, a)[0]
ck([k25, a26], [6, 3])
C = 'Rational(2,100)*x**2+3*x+50'; ck([val(C, 10), val(C, 100)], [82, 550])
H = '-5*x**2+20*x+1'; hv = [val(H, t) for t in (0, 1, 2, 4)]; ck(hv, [1, 16, 21, 1])
S.append((T("Polinomis i valor numèric", "Polinomios y valor numérico"), [
 (1, T("Completa la taula:", "Completa la tabla:") + tpol(False), tpol(True)),
 (1, T(r"Escriu, en cada cas, un polinomi que complisca les condicions:", r"Escribe, en cada caso, un polinomio que cumpla las condiciones:")
     + Tk([T("de grau 3, complet i amb terme independent $-2$;", "de grado 3, completo y con término independiente $-2$;"), T("de grau 4 i amb només dos termes;", "de grado 4 y solo dos términos;"),
           T("de grau 2, amb coeficient principal $-3$;", "de grado 2, con coeficiente principal $-3$;"), T("de grau 5 i sense terme independent.", "de grado 5 y sin término independiente.")], 2),
     T("Per exemple:", "Por ejemplo:") + Tk([R(r"x^3+2x^2-x-2"), R(r"x^4-7"), R(r"-3x^2+x+5"), R(r"x^5-4x^2+x")], 2)),
 (1, T(r"Donat el polinomi $P(x)=x^3-2x^2+4x-1$, calcula $P(0)$, $P(1)$, $P(-1)$, $P(2)$ i $P(-2)$.", r"Dado el polinomio $P(x)=x^3-2x^2+4x-1$, calcula $P(0)$, $P(1)$, $P(-1)$, $P(2)$ y $P(-2)$.")
     + recorda(T(r"Substituïm la $x$ pel nombre, entre parèntesis si és negatiu: $(-2)^3=-8$, $(-2)^2=4$.", r"Sustituimos la $x$ por el número, entre paréntesis si es negativo: $(-2)^3=-8$, $(-2)^2=4$.")),
     Tk([r"$P(%s)=%s=%s$" % (tl(sp.Rational(v)), sub(P23, v), Rm(tl(val(P23, v)))) for v in v23], 1)),
 (1, T(r"Calcula el valor numèric dels polinomis següents per a $x=3$, $x=-1$ i $x=0$:", r"Calcula el valor numérico de los polinomios siguientes para $x=3$, $x=-1$ y $x=0$:")
     + Tk([r"$P(x)=%s$" % pt(p) for p in P24], 3),
     Tk([r"$%s$" % r",\ \ ".join(Rm(tl(val(p, v))) for v in v24) for p in P24], 3)),
 (2, T(r"Quin valor ha de tindre $k$ perquè el polinomi $P(x)=2x^3-kx+5$ valga 9 per a $x=2$?", r"¿Qué valor tiene que tener $k$ para que el polinomio $P(x)=2x^3-kx+5$ valga 9 para $x=2$?"),
     r"$P(2)=16-2k+5=21-2k=9\Rightarrow" + Rm("k=6") + "$."),
 (2, T(r"Troba $a$ en el polinomi $P(x)=x^2+ax-4$ si sabem que $P(-1)=-6$.", r"Halla $a$ en el polinomio $P(x)=x^2+ax-4$ si sabemos que $P(-1)=-6$."),
     r"$P(-1)=1-a-4=-3-a=-6\Rightarrow" + Rm("a=3") + "$."),
 (2, T(r"El cost, en euros, de fabricar $x$ samarretes és $C(x)=0,02x^2+3x+50$. Quant costa fabricar-ne 10? I 100?", r"El coste, en euros, de fabricar $x$ camisetas es $C(x)=0,02x^2+3x+50$. ¿Cuánto cuesta fabricar 10? ¿Y 100?"),
     r"$C(10)=2+30+50=" + Rm(r"82\ \text{€}") + r"$; \ $C(100)=200+300+50=" + Rm(r"550\ \text{€}") + "$."),
 (3, T(r"L'altura (en metres) d'una pilota llançada cap amunt és $h(t)=-5t^2+20t+1$, on $t$ és el temps en segons. Calcula $h(0)$, $h(1)$, $h(2)$ i $h(4)$. Què signifiquen $h(0)$ i $h(4)$?", r"La altura (en metros) de una pelota lanzada hacia arriba es $h(t)=-5t^2+20t+1$, donde $t$ es el tiempo en segundos. Calcula $h(0)$, $h(1)$, $h(2)$ y $h(4)$. ¿Qué significan $h(0)$ y $h(4)$?"),
     r"$h(0)=" + Rm("1") + r"$, \ $h(1)=-5+20+1=" + Rm("16") + r"$, \ $h(2)=-20+40+1=" + Rm("21") + r"$, \ $h(4)=-80+80+1=" + Rm("1") + r"$ m.\\[2pt]"
     + T(r"$h(0)=1$: la pilota es llança des d'1 m d'altura; $h(4)=1$: als 4 s torna a estar a 1 m (l'altura màxima, 21 m, és als 2 s).", r"$h(0)=1$: la pelota se lanza desde 1 m de altura; $h(4)=1$: a los 4 s vuelve a estar a 1 m (la altura máxima, 21 m, es a los 2 s).")),
]))

# =====================================================================
# 3. Suma i resta
Pp, Qq, Rr = E('3*x**3-2*x**2+x-5'), E('x**3+4*x**2-6'), E('-2*x**2+3*x+1')
s31 = [Pp + Qq, Pp - Qq, Qq - Rr, Pp + Qq + Rr]; s32 = [Pp - (Qq + Rr), 2 * Pp - 3 * Rr, Pp - 2 * Qq + Rr]
Q33 = E('3*x**3+x**2-5') - E('x**3-2*x+4'); per34 = E('(x+3)+(2*x-1)+(x**2+x)')
ck([sp.expand(per34), per34.subs(x, 4)], [E('x**2+4*x+2'), 34])
S.append((T("Suma i resta de polinomis", "Suma y resta de polinomios"), [
 (1, T(r"Donats $P(x)=3x^3-2x^2+x-5$, $Q(x)=x^3+4x^2-6$ i $R(x)=-2x^2+3x+1$, calcula:", r"Dados $P(x)=3x^3-2x^2+x-5$, $Q(x)=x^3+4x^2-6$ y $R(x)=-2x^2+3x+1$, calcula:")
     + Tk([r"$P(x)+Q(x)$", r"$P(x)-Q(x)$", r"$Q(x)-R(x)$", r"$P(x)+Q(x)+R(x)$"], 2)
     + recorda(T(r"Per a restar, canviem el signe de \emph{tots} els termes del polinomi que restem: $-(x^2-3x)=-x^2+3x$.", r"Para restar, cambiamos el signo de \emph{todos} los términos del polinomio que restamos: $-(x^2-3x)=-x^2+3x$.")),
     Tk([R(pt(e)) for e in s31], 2)),
 (2, T("Amb els mateixos polinomis, calcula:", "Con los mismos polinomios, calcula:") + Tk([r"$P(x)-[Q(x)+R(x)]$", r"$2P(x)-3R(x)$", r"$P(x)-2Q(x)+R(x)$"], 3),
     Tk([R(pt(e)) for e in s32], 1)),
 (2, T(r"Troba el polinomi $Q(x)$ tal que $\left(x^3-2x+4\right)+Q(x)=3x^3+x^2-5$.", r"Halla el polinomio $Q(x)$ tal que $\left(x^3-2x+4\right)+Q(x)=3x^3+x^2-5$."),
     r"$Q(x)=\left(3x^3+x^2-5\right)-\left(x^3-2x+4\right)=" + Rm(pt(Q33)) + "$."),
 (2, T(r"Els costats d'un triangle fan $x+3$, $2x-1$ i $x^2+x$ centímetres. Escriu el polinomi que dona el perímetre i calcula'l per a $x=4$.", r"Los lados de un triángulo miden $x+3$, $2x-1$ y $x^2+x$ centímetros. Escribe el polinomio que da el perímetro y calcúlalo para $x=4$."),
     r"$P(x)=" + Rm(pt(per34)) + r"$; \ $P(4)=16+16+2=" + Rm(r"34\ \text{cm}") + "$."),
]))

# =====================================================================
# 4. Producte de polinomis
p41 = ['3*x*(x**2-2*x+5)', '-2*x**2*(x**3-4*x+1)', 'Rational(1,2)*x*(4*x**2-6*x+2)', '5*x**3*(-x**2+x-3)', '(x**2-3*x+1)*(-4*x)', '-x*(2*x**4-x**2+7)']
p41T = [r"$3x\left(x^2-2x+5\right)$", r"$-2x^2\left(x^3-4x+1\right)$", r"$\frac12x\left(4x^2-6x+2\right)$", r"$5x^3\left(-x^2+x-3\right)$", r"$\left(x^2-3x+1\right)\cdot(-4x)$", r"$-x\left(2x^4-x^2+7\right)$"]
p42 = ['(x+2)*(x-5)', '(2*x-1)*(3*x+4)', '(x**2+1)*(x-3)', '(x**2-2*x+3)*(x+1)', '(2*x**2-x+4)*(x-2)', '(x**2+x-1)*(x**2-x+2)']
p42T = [r"$(x+2)(x-5)$", r"$(2x-1)(3x+4)$", r"$\left(x^2+1\right)(x-3)$", r"$\left(x^2-2x+3\right)(x+1)$", r"$\left(2x^2-x+4\right)(x-2)$", r"$\left(x^2+x-1\right)\left(x^2-x+2\right)$"]
P4, Q4, R4 = E('x**2-3*x+2'), E('2*x+1'), E('x-4')
p43 = [P4 * Q4, P4 * R4 - Q4, (Q4 + R4) * P4]
p44 = ['2*x*(x-3)-x*(x+1)', '(x+2)*(x-1)-(x-3)*(x+4)', '3*(x**2-1)-(x+1)*(2*x-3)']
p44T = [r"$2x(x-3)-x(x+1)$", r"$(x+2)(x-1)-(x-3)(x+4)$", r"$3\left(x^2-1\right)-(x+1)(2x-3)$"]
A45 = E('(2*x+3)*(x-1)'); ck([A45.subs(x, 5)], [52])
V45 = E('x*(x+2)*(x+5)'); ck([V45.subs(x, 3)], [120])
S.append((T("Producte de polinomis", "Producto de polinomios"), [
 (1, T("Multiplica:", "Multiplica:") + Tk(p41T, 2) + recorda(T(r"Es multiplica el monomi per cada terme del polinomi. Compte amb els signes: $(-)\cdot(-)=+$.", r"Se multiplica el monomio por cada término del polinomio. Cuidado con los signos: $(-)\cdot(-)=+$.")),
     Tk([R(pt(e)) for e in p41], 2)),
 (1, T("Multiplica i redueix:", "Multiplica y reduce:") + Tk(p42T, 2) + recorda(T("Cada terme del primer polinomi es multiplica per cada terme del segon; després es redueixen els termes semblants.", "Cada término del primer polinomio se multiplica por cada término del segundo; después se reducen los términos semejantes.")),
     Tk([R(pt(e)) for e in p42], 2)),
 (2, T(r"Donats $P(x)=x^2-3x+2$, $Q(x)=2x+1$ i $R(x)=x-4$, calcula:", r"Dados $P(x)=x^2-3x+2$, $Q(x)=2x+1$ y $R(x)=x-4$, calcula:") + Tk([r"$P(x)\cdot Q(x)$", r"$P(x)\cdot R(x)-Q(x)$", r"$[Q(x)+R(x)]\cdot P(x)$"], 3),
     Tk([R(pt(e)) for e in p43], 1)),
 (2, T("Opera i redueix:", "Opera y reduce:") + Tk(p44T, 1),
     Tk([R(pt(e)) for e in p44], 3)),
 (3, T(r"Un rectangle fa $2x+3$ cm de base i $x-1$ cm d'altura. Escriu el polinomi que dona l'àrea i calcula-la per a $x=5$. I el volum d'una caixa d'arestes $x$, $x+2$ i $x+5$? Calcula'l per a $x=3$.",
       r"Un rectángulo mide $2x+3$ cm de base y $x-1$ cm de altura. Escribe el polinomio que da el área y calcúlala para $x=5$. ¿Y el volumen de una caja de aristas $x$, $x+2$ y $x+5$? Calcúlalo para $x=3$."),
     T("Àrea: ", "Área: ") + r"$A(x)=(2x+3)(x-1)=" + Rm(pt(A45)) + r"$; \ $A(5)=13\cdot4=" + Rm(r"52\ \text{cm}^2") + r"$.\\[2pt]"
     + T("Volum: ", "Volumen: ") + r"$V(x)=" + Rm(pt(V45)) + r"$; \ $V(3)=3\cdot5\cdot8=" + Rm(r"120\ \text{cm}^3") + "$."),
]))

# =====================================================================
# 5. Identitats notables
i51 = ['(x+3)**2', '(x-4)**2', '(x+5)*(x-5)', '(2*x+1)**2', '(3*x-2)**2', '(2*x+7)*(2*x-7)', '(x**2+3)**2', '(5-x)**2', '(Rational(1,2)*x+1)**2']
i51T = [r"$(x+3)^2$", r"$(x-4)^2$", r"$(x+5)(x-5)$", r"$(2x+1)^2$", r"$(3x-2)^2$", r"$(2x+7)(2x-7)$", r"$\left(x^2+3\right)^2$", r"$(5-x)^2$", r"$\left(\frac12x+1\right)^2$"]
i52 = ['(x+1)**2-(x-1)**2', '(x+3)**2-(x+3)*(x-3)', '(2*x-1)**2+(x+2)*(x-2)', '2*(x-3)**2-(x+1)**2']
i52T = [r"$(x+1)^2-(x-1)^2$", r"$(x+3)^2-(x+3)(x-3)$", r"$(2x-1)^2+(x+2)(x-2)$", r"$2(x-3)^2-(x+1)^2$"]
fe('(x+6)**2', 'x**2+12*x+36'); fe('(2*x-5)**2', '4*x**2-20*x+25'); fe('(3*x+4)*(3*x-4)', '9*x**2-16')
ck([101 ** 2, 99 ** 2, 51 * 49], [10201, 9801, 2499])
S.append((T("Identitats notables", "Identidades notables"), [
 (1, T("Desenvolupa aplicant les identitats notables:", "Desarrolla aplicando las identidades notables:") + Tk(i51T, 3)
     + recorda(r"$(a+b)^2=a^2+2ab+b^2$, \quad $(a-b)^2=a^2-2ab+b^2$, \quad $(a+b)(a-b)=a^2-b^2$."),
     Tk([R(pt(e)) for e in i51], 3)),
 (2, T("Opera i simplifica:", "Opera y simplifica:") + Tk(i52T, 2),
     Tk([R(pt(e)) for e in i52], 2)),
 (2, T("Completa els buits:", "Completa los huecos:") + Tk([r"$(x+\square)^2=x^2+\square+36$", r"$(\square-5)^2=4x^2-\square+25$", r"$(3x+\square)(3x-\square)=\square-16$"], 1),
     Tk([r"$(x+" + Rm("6") + r")^2=x^2+" + Rm("12x") + "+36$", r"$(" + Rm("2x") + r"-5)^2=4x^2-" + Rm("20x") + "+25$", r"$(3x+" + Rm("4") + r")(3x-" + Rm("4") + r")=" + Rm("9x^2") + "-16$"], 1)),
 (3, T(r"Calcula sense calculadora, fent servir les identitats notables: \ $101^2$, \ $99^2$ \ i \ $51\cdot49$.", r"Calcula sin calculadora, usando las identidades notables: \ $101^2$, \ $99^2$ \ y \ $51\cdot49$."),
     r"$(100+1)^2=10000+200+1=" + Rm("10201") + r"$; \ $(100-1)^2=10000-200+1=" + Rm("9801") + r"$; \ $(50+1)(50-1)=2500-1=" + Rm("2499") + "$."),
]))

# =====================================================================
# 6. Divisió de polinomis
d61 = [('6*x**3-9*x**2+3*x', '3*x'), ('10*x**5-15*x**3+5*x**2', '5*x**2'), ('8*x**4-4*x**3+2*x**2', '-2*x**2')]
d61T = [r"$\left(6x^3-9x^2+3x\right):3x$", r"$\left(10x^5-15x^3+5x^2\right):5x^2$", r"$\left(8x^4-4x^3+2x^2\right):\left(-2x^2\right)$"]
d62 = [('2*x**3+3*x**2-x+4', 'x**2+1'), ('x**4-2*x**3+3*x-1', 'x**2-x'), ('6*x**3-x**2+x+5', '2*x-1'), ('x**4-1', 'x**2+1'), ('3*x**4+2*x**2-x', 'x**2-2*x+1')]
d62T = [r"$\left(2x^3+3x^2-x+4\right):\left(x^2+1\right)$", r"$\left(x^4-2x^3+3x-1\right):\left(x^2-x\right)$", r"$\left(6x^3-x^2+x+5\right):(2x-1)$", r"$\left(x^4-1\right):\left(x^2+1\right)$", r"$\left(3x^4+2x^2-x\right):\left(x^2-2x+1\right)$"]
q62 = [dv(D, d) for D, d in d62]
D64 = E('(x**2-2)*(x+3)+2*x-1'); h65, r65 = dv('2*x**2+7*x+3', 'x+3'); ck([r65], [0])
q1, r1 = q62[0]
S.append((T("Divisió de polinomis", "División de polinomios"), [
 (1, T("Divideix:", "Divide:") + Tk(d61T, 1),
     Tk([R(pt(dv(D, d)[0])) for D, d in d61], 3)),
 (2, T("Fes les divisions següents i indica el quocient i el residu:", "Haz las divisiones siguientes e indica el cociente y el resto:") + Tk(d62T, 1)
     + recorda(T(r"Ordena el dividend i deixa buit el lloc dels termes que falten. Para quan el residu tinga grau menor que el divisor.", r"Ordena el dividendo y deja hueco para los términos que faltan. Para cuando el resto tenga grado menor que el divisor.")),
     Tk([r"$c(x)=" + Rm(pt(q)) + r",\ \ r(x)=" + Rm(pt(r)) + "$" for q, r in q62], 1)),
 (2, T(r"Comprova el resultat de la divisió a) de l'exercici anterior amb la prova de la divisió, $D(x)=d(x)\cdot c(x)+r(x)$.", r"Comprueba el resultado de la división a) del ejercicio anterior con la prueba de la división, $D(x)=d(x)\cdot c(x)+r(x)$."),
     r"$\left(x^2+1\right)(" + pt(q1) + ")+(" + pt(r1) + ")=" + pt(sp.expand(E('x**2+1') * q1)) + "+(" + pt(r1) + ")=" + Rm(pt(E(d62[0][0]))) + r"$\ \ \checkmark"),
 (3, T(r"En una divisió, el divisor és $x^2-2$, el quocient és $x+3$ i el residu és $2x-1$. Quin és el dividend?", r"En una división, el divisor es $x^2-2$, el cociente es $x+3$ y el resto es $2x-1$. ¿Cuál es el dividendo?"),
     r"$D(x)=\left(x^2-2\right)(x+3)+2x-1=x^3+3x^2-2x-6+2x-1=" + Rm(pt(D64)) + "$."),
 (3, T(r"L'àrea d'un rectangle és $2x^2+7x+3$ i la base fa $x+3$. Quant fa l'altura? Quin és el perímetre?", r"El área de un rectángulo es $2x^2+7x+3$ y la base mide $x+3$. ¿Cuánto mide la altura? ¿Cuál es el perímetro?"),
     T("Altura: ", "Altura: ") + r"$\left(2x^2+7x+3\right):(x+3)=" + Rm(pt(h65)) + r"$ \ " + T("(residu 0)", "(resto 0)") + r"; \ " + T("perímetre: ", "perímetro: ") + r"$2(x+3)+2(2x+1)=" + Rm(pt(2 * (x + 3) + 2 * h65)) + "$."),
]))

# =====================================================================
# 7. Regla de Ruffini
r71 = [('x**3-4*x**2+x+6', 2), ('x**3+2*x**2-x+3', -1), ('2*x**3-3*x**2+4', 1), ('x**4-3*x**2+2*x-5', -2), ('x**4-16', 2), ('3*x**3-5*x+1', -3)]
def dT(a_): return 'x-%d' % a_ if a_ > 0 else 'x+%d' % -a_
r71T = [r"$\left(%s\right):(%s)$" % (pt(P), dT(a_)) for P, a_ in r71]
R71 = [rft(P, a_) for P, a_ in r71]
r72 = [('x**5-1', 1), ('x**3+27', -3)]; R72 = [rft(P, a_) for P, a_ in r72]
R73 = [rft('x**3-2*x**2-5*x+6', 3), rft('x**3-2*x**2-5*x+6', -1)]
k74 = sp.solve(val('x**3+k*x**2-4*x+12', 2), k)[0]; ck([k74], [-3])
S.append((T("Regla de Ruffini", "Regla de Ruffini"), [
 (1, T("Divideix aplicant la regla de Ruffini i indica el quocient i el residu:", "Divide aplicando la regla de Ruffini e indica el cociente y el resto:") + Tk(r71T, 2)
     + recorda(T(r"Escriu tots els coeficients, amb un 0 per a cada terme que falte. Si el divisor és $x+2$, a l'esquerra va el $-2$.", r"Escribe todos los coeficientes, con un 0 por cada término que falte. Si el divisor es $x+2$, a la izquierda va el $-2$.")),
     Tk([r"$%s$\\[2pt]" % t + cr(q, r) for t, q, r in R71], 2, gap='8pt')),
 (2, T("Divideix per Ruffini:", "Divide por Ruffini:") + Tk([r"$\left(x^5-1\right):(x-1)$", r"$\left(x^3+27\right):(x+3)$"], 2),
     Tk([r"$%s$\\[2pt]" % t + cr(q, r) for t, q, r in R72], 2)),
 (2, T(r"Fes servir la regla de Ruffini per a saber si $x^3-2x^2-5x+6$ és divisible entre $x-3$ i entre $x+1$.", r"Usa la regla de Ruffini para saber si $x^3-2x^2-5x+6$ es divisible entre $x-3$ y entre $x+1$."),
     Tk([r"$%s$\\[2pt]" % R73[0][0] + T("Residu 0: ", "Resto 0: ") + R(T(r"\text{sí que és divisible}", r"\text{sí es divisible}")), r"$%s$\\[2pt]" % R73[1][0] + T("Residu 8: ", "Resto 8: ") + R(T(r"\text{no és divisible}", r"\text{no es divisible}"))], 2)),
 (3, T(r"Troba el valor de $k$ perquè la divisió $\left(x^3+kx^2-4x+12\right):(x-2)$ siga exacta.", r"Halla el valor de $k$ para que la división $\left(x^3+kx^2-4x+12\right):(x-2)$ sea exacta."),
     T(r"Amb Ruffini, el residu és $8+4k-8+12=4k+12$. Ha de ser 0: ", r"Con Ruffini, el resto es $8+4k-8+12=4k+12$. Tiene que ser 0: ") + r"$4k+12=0\Rightarrow" + Rm("k=-3") + "$."),
]))
assert R73[1][2] == 8 and R73[0][2] == 0

# =====================================================================
# 8. El valor numèric amb Ruffini (teorema del residu)
t81 = [('x**3-5*x+2', 2), ('x**4+2*x**3-x', -1), ('2*x**5-3*x**2+1', 1), ('x**3+x**2+x+1', -2)]
P82 = 'x**4-2*x**3-5*x**2+x+3'; R82 = [rft(P82, 3), rft(P82, -2)]
ck([R82[0][2], R82[1][2]], [val(P82, 3), val(P82, -2)])
m83 = sp.solve(val('x**3-m*x+4', -2) - 10, m)[0]; a84 = sp.solve(val('2*x**3+a*x**2-x+3', 1) - 5, a)[0]; ck([m83, a84], [7, 1])
S.append((T("Valor numèric amb Ruffini. Teorema del residu", "Valor numérico con Ruffini. Teorema del resto"), [
 (1, T("Calcula, sense fer la divisió, el residu de:", "Calcula, sin hacer la división, el resto de:") + Tk([r"$\left(%s\right):(%s)$" % (pt(P), dT(a_)) for P, a_ in t81], 2)
     + recorda(T(r"El residu de la divisió $P(x):(x-a)$ és el valor numèric $P(a)$.", r"El resto de la división $P(x):(x-a)$ es el valor numérico $P(a)$.")),
     Tk([r"$r=P(%s)=%s=%s$" % (tl(a_), sub(P, a_), Rm(tl(val(P, a_)))) for P, a_ in t81], 1)),
 (2, T(r"Donat $P(x)=x^4-2x^3-5x^2+x+3$, calcula $P(3)$ i $P(-2)$ amb la regla de Ruffini. Comprova-ho substituint.", r"Dado $P(x)=x^4-2x^3-5x^2+x+3$, calcula $P(3)$ y $P(-2)$ con la regla de Ruffini. Compruébalo sustituyendo."),
     Tk([r"$%s$\\[2pt]$P(3)=%s$\\[1pt]{\small $%s=%s$}" % (R82[0][0], Rm(tl(R82[0][2])), sub(P82, 3), tl(val(P82, 3))),
         r"$%s$\\[2pt]$P(-2)=%s$\\[1pt]{\small $%s=%s$}" % (R82[1][0], Rm(tl(R82[1][2])), sub(P82, -2), tl(val(P82, -2)))], 2)),
 (2, T(r"Troba $m$ perquè el residu de la divisió $\left(x^3-mx+4\right):(x+2)$ siga 10.", r"Halla $m$ para que el resto de la división $\left(x^3-mx+4\right):(x+2)$ sea 10."),
     r"$P(-2)=-8+2m+4=2m-4=10\Rightarrow" + Rm("m=7") + "$."),
 (3, T(r"Quin valor ha de tindre $a$ perquè el polinomi $2x^3+ax^2-x+3$ done residu 5 en dividir-lo entre $x-1$?", r"¿Qué valor tiene que tener $a$ para que el polinomio $2x^3+ax^2-x+3$ dé resto 5 al dividirlo entre $x-1$?"),
     r"$P(1)=2+a-1+3=4+a=5\Rightarrow" + Rm("a=1") + "$."),
]))

# =====================================================================
# 9. Arrels d'un polinomi
P91 = 'x**3-2*x**2-x+2'; ck([val(P91, v) for v in (1, -1, 2)], [0, 0, 0])
P92 = 'x**3+x**2-6*x'; v92 = [0, 2, -2, -3]; z92 = [val(P92, v) for v in v92]; ck(z92, [0, 0, 8, 0])
a93 = ['x**3-6*x**2+11*x-6', 'x**3+2*x**2-x-2', 'x**3-3*x+2', 'x**4-5*x**2+4']
def roots(P):
    rs = {r_: mm for r_, mm in sp.roots(sp.Poly(E(P), x)).items() if r_.is_real}; out = []
    for r_ in sorted(rs, key=lambda t: float(t)):
        out.append('x=' + tl(r_) + (T(' (doble)', ' (doble)') if rs[r_] == 2 else T(' (triple)', ' (triple)') if rs[r_] == 3 else ''))
    return out
a94 = ['x**2-7*x+12', '2*x**2-x-1', 'x**2+2*x+5', 'x**2-6*x+9']
ck([sp.Poly(E(a94[2]), x).discriminant() < 0], [True])
P96 = E('(x-2)*(x+1)*(x-3)'); k96 = sp.solve(val('x**3+k*x-6', 2), k)[0]; ck([k96], [-1])
S.append((T("Arrels d'un polinomi", "Raíces de un polinomio"), [
 (1, T(r"Comprova si $x=1$, $x=-1$ i $x=2$ són arrels del polinomi $P(x)=x^3-2x^2-x+2$.", r"Comprueba si $x=1$, $x=-1$ y $x=2$ son raíces del polinomio $P(x)=x^3-2x^2-x+2$."),
     r"$P(1)=1-2-1+2=0$, \ $P(-1)=-1-2+1+2=0$, \ $P(2)=8-8-2+2=0$: \ " + R(T(r"\text{les tres són arrels}", r"\text{las tres son raíces}")) + "."),
 (1, T(r"Quins d'aquests nombres són arrels de $x^3+x^2-6x$? \ $0$, \ $2$, \ $-2$, \ $-3$.", r"¿Cuáles de estos números son raíces de $x^3+x^2-6x$? \ $0$, \ $2$, \ $-2$, \ $-3$."),
     r"$P(0)=0$, \ $P(2)=8+4-12=0$, \ $P(-2)=-8+4+12=8$, \ $P(-3)=-27+9+18=0$: \ " + R(T(r"\text{són arrels } 0,\ 2\text{ i }-3", r"\text{son raíces } 0,\ 2\text{ y }-3")) + "."),
 (2, T("Troba les arrels enteres dels polinomis:", "Halla las raíces enteras de los polinomios:") + Tk(['$' + pt(p) + '$' for p in a93], 2)
     + recorda(T("Les arrels enteres són divisors del terme independent: prova'ls amb Ruffini (o calculant el valor numèric).", "Las raíces enteras son divisores del término independiente: pruébalos con Ruffini (o calculando el valor numérico).")),
     Tk([R(r',\ '.join(roots(p)).replace(' (doble)', r'\ (\text{doble})')) for p in a93], 2)),
 (2, T("Troba les arrels dels polinomis de segon grau resolent l'equació:", "Halla las raíces de los polinomios de segundo grado resolviendo la ecuación:") + Tk(['$' + pt(p) + '$' for p in a94], 2),
     Tk([R(r',\ '.join(roots(p)).replace(' (doble)', r'\ (\text{doble})')) if roots(p) else R(T(r"\text{no en té } (\Delta=4-20<0)", r"\text{no tiene } (\Delta=4-20<0)")) for p in a94], 2)),
 (2, T(r"Sense fer cap càlcul, explica per què $x=5$ no pot ser una arrel de $x^3+x^2-3x+6$.", r"Sin hacer ningún cálculo, explica por qué $x=5$ no puede ser una raíz de $x^3+x^2-3x+6$."),
     T(r"Les arrels enteres han de ser divisors del terme independent, 6, i ", r"Las raíces enteras tienen que ser divisores del término independiente, 6, y ") + r"\\[2pt]" + R(T(r"5\text{ no és divisor de }6", r"5\text{ no es divisor de }6")) + "."),
 (3, T(r"Escriu un polinomi de grau 3, amb coeficient principal 1, que tinga per arrels $2$, $-1$ i $3$. Troba també $k$ perquè $x=2$ siga arrel de $x^3+kx-6$.", r"Escribe un polinomio de grado 3, con coeficiente principal 1, que tenga por raíces $2$, $-1$ y $3$. Halla también $k$ para que $x=2$ sea raíz de $x^3+kx-6$."),
     r"$(x-2)(x+1)(x-3)=" + Rm(pt(P96)) + r"$; \ $8+2k-6=0\Rightarrow" + Rm("k=-1") + "$."),
]))

# =====================================================================
# 10. Factor comú i identitats notables
f101 = ['4*x**2-8*x', '3*x**3+6*x**2-9*x', '5*x**4-10*x**3', '12*x**5-18*x**3+6*x**2', 'x**3+x**2+x', '2*x**4-14*x**2']
f101S = [r"4x(x-2)", r"3x\left(x^2+2x-3\right)", r"5x^3(x-2)", r"6x^2\left(2x^3-3x+1\right)", r"x\left(x^2+x+1\right)", r"2x^2\left(x^2-7\right)"]
for e, s in zip(f101, ['4*x*(x-2)', '3*x*(x**2+2*x-3)', '5*x**3*(x-2)', '6*x**2*(2*x**3-3*x+1)', 'x*(x**2+x+1)', '2*x**2*(x**2-7)']): fe(e, s)
f102 = ['x**2-36', 'x**2+8*x+16', 'x**2-12*x+36', '9*x**2-4', '4*x**2+20*x+25', '25*x**2-10*x+1', 'x**4-9', 'x**2-Rational(1,4)', '16-x**2']
f102S = [r"(x+6)(x-6)", r"(x+4)^2", r"(x-6)^2", r"(3x+2)(3x-2)", r"(2x+5)^2", r"(5x-1)^2", r"\left(x^2+3\right)\left(x^2-3\right)", r"\left(x+\frac12\right)\left(x-\frac12\right)", r"(4+x)(4-x)"]
for e, s in zip(f102, ['(x+6)*(x-6)', '(x+4)**2', '(x-6)**2', '(3*x+2)*(3*x-2)', '(2*x+5)**2', '(5*x-1)**2', '(x**2+3)*(x**2-3)', '(x+Rational(1,2))*(x-Rational(1,2))', '(4+x)*(4-x)']): fe(e, s)
f103 = ['2*x**3-18*x', '3*x**3+12*x**2+12*x', 'x**4-x**2', '5*x**3-10*x**2+5*x', 'x**5-16*x', '2*x**4-50*x**2']
f103S = [r"2x\left(x^2-9\right)=2x(x+3)(x-3)", r"3x\left(x^2+4x+4\right)=3x(x+2)^2", r"x^2\left(x^2-1\right)=x^2(x+1)(x-1)", r"5x\left(x^2-2x+1\right)=5x(x-1)^2", r"x\left(x^4-16\right)=x\left(x^2+4\right)(x+2)(x-2)", r"2x^2\left(x^2-25\right)=2x^2(x+5)(x-5)"]
for e, s in zip(f103, ['2*x*(x+3)*(x-3)', '3*x*(x+2)**2', 'x**2*(x+1)*(x-1)', '5*x*(x-1)**2', 'x*(x**2+4)*(x+2)*(x-2)', '2*x**2*(x+5)*(x-5)']): fe(e, s)
ck([83 ** 2 - 17 ** 2, 100 * 66], [6600, 6600])
S.append((T("Factor comú i identitats notables", "Factor común e identidades notables"), [
 (1, T("Trau factor comú:", "Saca factor común:") + Tk(['$' + pt(e) + '$' for e in f101], 3)
     + recorda(T(r"Es trau el m.c.d. dels coeficients i la menor potència de $x$: $6x^3-9x^2=3x^2(2x-3)$.", r"Se saca el m.c.d. de los coeficientes y la menor potencia de $x$: $6x^3-9x^2=3x^2(2x-3)$.")),
     Tk([R(s) for s in f101S], 3)),
 (1, T("Factoritza fent servir les identitats notables:", "Factoriza usando las identidades notables:") + Tk(['$' + pt(e) + '$' if e != '16-x**2' else '$16-x^2$' for e in f102], 3)
     + recorda(r"$a^2+2ab+b^2=(a+b)^2$, \quad $a^2-2ab+b^2=(a-b)^2$, \quad $a^2-b^2=(a+b)(a-b)$."),
     Tk([R(s) for s in f102S], 3)),
 (2, T("Factoritza: primer trau factor comú i després aplica una identitat notable.", "Factoriza: primero saca factor común y después aplica una identidad notable.") + Tk(['$' + pt(e) + '$' for e in f103], 3),
     Tk(['$' + s.split('=')[0] + '=' + Rm(s.split('=')[1]) + '$' for s in f103S], 2)),
 (3, T(r"Calcula sense calculadora, factoritzant: \ $83^2-17^2$.", r"Calcula sin calculadora, factorizando: \ $83^2-17^2$."),
     r"$83^2-17^2=(83+17)(83-17)=100\cdot66=" + Rm("6600") + "$."),
]))

# =====================================================================
# 11. Factorització de polinomis
f111 = ['x**2-5*x+6', 'x**2+x-12', '2*x**2-8*x+6', 'x**2-4*x-5']
f112 = ['x**3-2*x**2-5*x+6', 'x**3+4*x**2+x-6', 'x**3-7*x-6', 'x**3-3*x**2-4*x+12']
f113 = ['x**4-x**3-7*x**2+x+6', '2*x**3-4*x**2-2*x+4', 'x**4-2*x**3-3*x**2', 'x**3-x**2-8*x+12']
f114 = ['x**3-3*x**2+3*x-1', 'x**4-8*x**2+16']
def facR(p): return R(fac(p))
S.append((T("Factorització de polinomis", "Factorización de polinomios"), [
 (2, T("Factoritza aquests polinomis de segon grau (busca'n primer les arrels):", "Factoriza estos polinomios de segundo grado (busca primero sus raíces):") + Tk(['$' + pt(p) + '$' for p in f111], 2)
     + recorda(T(r"Si $x_1$ i $x_2$ són les arrels de $ax^2+bx+c$, aleshores $ax^2+bx+c=a(x-x_1)(x-x_2)$.", r"Si $x_1$ y $x_2$ son las raíces de $ax^2+bx+c$, entonces $ax^2+bx+c=a(x-x_1)(x-x_2)$.")),
     Tk([facR(p) for p in f111], 2)),
 (2, T("Factoritza amb la regla de Ruffini:", "Factoriza con la regla de Ruffini:") + Tk(['$' + pt(p) + '$' for p in f112], 2),
     Tk([facR(p) for p in f112], 2)),
 (3, T("Factoritza (si es pot, trau primer factor comú):", "Factoriza (si se puede, saca primero factor común):") + Tk(['$' + pt(p) + '$' for p in f113], 2),
     Tk([facR(p) for p in f113], 2)),
 (3, T("Factoritza i indica les arrels i quantes vegades es repeteix cadascuna:", "Factoriza e indica las raíces y cuántas veces se repite cada una:") + Tk(['$' + pt(p) + '$' for p in f114], 2),
     Tk([facR(f114[0]) + T(r": $x=1$ (triple)", r": $x=1$ (triple)"), facR(f114[1]) + T(r": $x=-2$ i $x=2$ (dobles)", r": $x=-2$ y $x=2$ (dobles)")], 1)),
]))
ck([fac(f114[0]), fac(f114[1])], ['(x-1)^{3}', '(x+2)^{2}(x-2)^{2}'])

# =====================================================================
# 12. Problemes
V122 = E('x*(20-2*x)*(30-2*x)'); ck([V122.subs(x, 5)], [1000])
b123, r123 = dv('x**2+5*x+6', 'x+2'); ck([r123], [0])
S.append((T("Problemes", "Problemas"), [
 (2, T(r"A un quadrat de costat $x+2$ li retallem un quadrat de costat $x$. Escriu el polinomi que dona l'àrea que queda i calcula-la per a $x=3$ cm.", r"A un cuadrado de lado $x+2$ le recortamos un cuadrado de lado $x$. Escribe el polinomio que da el área que queda y calcúlala para $x=3$ cm."),
     r"$(x+2)^2-x^2=x^2+4x+4-x^2=" + Rm("4x+4") + r"$; \ " + T("per a $x=3$: ", "para $x=3$: ") + R(r"16\ \text{cm}^2") + "."),
 (2, T(r"D'una làmina de cartó de $20\times30$ cm retallem un quadrat de costat $x$ en cada cantó i pleguem les vores per a fer una caixa sense tapa. Escriu el polinomi $V(x)$ del volum de la caixa i calcula'l per a $x=5$ cm.", r"De una lámina de cartón de $20\times30$ cm recortamos un cuadrado de lado $x$ en cada esquina y doblamos los bordes para hacer una caja sin tapa. Escribe el polinomio $V(x)$ del volumen de la caja y calcúlalo para $x=5$ cm."),
     r"$V(x)=x(20-2x)(30-2x)=" + Rm(pt(V122)) + r"$; \ $V(5)=5\cdot10\cdot20=" + Rm(r"1000\ \text{cm}^3") + "$."),
 (3, T(r"L'àrea d'un rectangle és $x^2+5x+6$ i un dels costats fa $x+2$. Quant fa l'altre costat? Escriu el perímetre i calcula'l per a $x=4$.", r"El área de un rectángulo es $x^2+5x+6$ y uno de los lados mide $x+2$. ¿Cuánto mide el otro lado? Escribe el perímetro y calcúlalo para $x=4$."),
     r"$\left(x^2+5x+6\right):(x+2)=" + Rm(pt(b123)) + r"$; \ $P(x)=2(x+2)+2(x+3)=" + Rm("4x+10") + r"$; \ $P(4)=" + Rm("26") + "$."),
 (3, T(r"Pensa un nombre, suma-li 3, eleva el resultat al quadrat i resta-li el quadrat del nombre pensat. Comprova amb polinomis que el resultat sempre és el séxtuple del nombre més 9.", r"Piensa un número, súmale 3, eleva el resultado al cuadrado y réstale el cuadrado del número pensado. Comprueba con polinomios que el resultado siempre es el séxtuplo del número más 9."),
     r"$(x+3)^2-x^2=x^2+6x+9-x^2=" + Rm("6x+9") + "$."),
]))
fe('(x+3)**2-x**2', '6*x+9'); fe('2*(x+2)+2*(x+3)', '4*x+10'); fe('(x+2)**2-x**2', '4*x+4')

# =====================================================================
TITOL = T("Polinomis", "Polinomios")
KW = T("polinomis, monomis, valor numèric, suma de polinomis, resta de polinomis, producte de polinomis, identitats notables, divisió de polinomis, regla de Ruffini, teorema del residu, arrels, factorització, factor comú",
       "polinomios, monomios, valor numérico, suma de polinomios, resta de polinomios, producto de polinomios, identidades notables, división de polinomios, regla de Ruffini, teorema del resto, raíces, factorización, factor común")
INTRO_EX = T(r"Resol-los al quadern mostrant tots els passos. Pots comprovar els resultats amb les eines interactives dels apunts.", r"Resuélvelos en el cuaderno mostrando todos los pasos. Puedes comprobar los resultados con las herramientas interactivas de los apuntes.")
INTRO_SOL = T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat.",
              r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad.")
build(HERE, 3, TITOL, S, KW, INTRO_EX, INTRO_SOL, lang=LANG, curs='4eso-a')
