# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (1r Batxillerat MI, Unitat 7: Estudi de funcions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# La fitxa segueix els apartats dels apunts (7.1-7.16) i acaba amb problemes i estudis complets.
# Comprovacions: sympy calcula els talls, els vèrtexs, les composicions i les inverses; els dominis es comproven numèricament
# (la funció ha d'existir exactament en els punts del domini donat, en una malla fina i al voltant de cada extrem).
# Les gràfiques es dibuixen amb la classe Plot de _eines/apunts/1batx-mi-t7/fig.py (la mateixa dels apunts).
# Ús: python3 genera.py && pdflatex t7-fitxa-exercicis.tex (dues vegades) && pdflatex t7-fitxa-solucions.tex (dues vegades)
import os, re, sys, math
from sympy import symbols, sympify, solve, simplify, expand, Rational, sqrt as Ssqrt, S, log as Slog, Abs, Poly, nsimplify
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "apunts", "1batx-mi-t7"))
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
S_.append(("Concepte de funció", [
 (1, r"Quines d'aquestes gràfiques corresponen a una funció? Justifica-ho amb la prova de la recta vertical." + tasks(4, [Gi(p) for p in p1]),
     tasks(2, [R('\\text{Sí}'), R('\\text{No}') + ' (circumferència)', R('\\text{Sí}'), R('\\text{No}')]) + r'Les gràfiques b) i d) tenen valors de $x$ amb dues imatges: hi ha rectes verticals que les tallen dues vegades.'),
 (1, r"Indica si aquestes relacions són funcions:" + tasks(1, [
     "A cada nombre real li fem correspondre el seu quadrat.",
     "A cada nombre positiu li fem correspondre les seues arrels quadrades.",
     "A cada persona li fem correspondre el número del seu DNI.",
     "A cada alumne de la classe li fem correspondre els seus germans."]),
     tasks(1, [R('\\text{Sí}'), R('\\text{No}') + r': el 4 té dues arrels, $2$ i $-2$.', R('\\text{Sí}'), R('\\text{No}') + ': un alumne pot tindre dos o més germans.'])),
 (1, r"Donada $f(x)=x^2-3x+1$, calcula $f(-2)$, $f(0)$, $f\left(\frac12\right)$ i $f(a+1)$. Per a quins valors de $x$ val $f(x)=1$?",
     r'$f(-2)=\res{11}$, $f(0)=\res{1}$, $f\left(\frac12\right)=\res{-\frac14}$, $f(a+1)=\res{a^2-a-1}$. \ $x^2-3x=0\Rightarrow\res{x=0,\ x=3}$'),
]))

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
S_.append(("Domini i recorregut", [
 (1, r"Escriu el domini i el recorregut de les funcions representades:" + tasks(4, [Gi(p) for p in d1]),
     tasks(2, [r'$D=\res{\cc{-1}{3}}$, $R=\res{\cc{-2}{2}}$', r'$D=\res{\R-\{-1\}}$, $R=\res{\R-\{2\}}$', r'$D=\res{\co{-2}{+\infty}}$, $R=\res{\co{-1}{+\infty}}$', r'$D=\res{\cc{-4}{2}}$, $R=\res{\co{-1}{2}\cup\{3\}}$'])),
 (1, r"Calcula el domini d'aquestes funcions:" + tasks(3, ['$f(x)=%s$' % e[0] for e in e5])
     + recorda(r"denominador $\neq0$; radicand d'índex parell $\geq0$; argument del logaritme $\gt0$; l'exponent i el radicand d'índex senar han d'existir."),
     tasks(3, [R(e[4]) for e in e5])),
 (1, r"Pertanyen $x=2$ i $x=3$ al domini de $f(x)=\sqrt{x^2-5}$? Justifica-ho substituint, i després calcula el domini complet.",
     r'$f(2)=\sqrt{-1}$ no existeix: $\res{2\notin D(f)}$. $f(3)=\sqrt4=2$: $\res{3\in D(f)}$. $D(f)=\res{\oc{-\infty}{-\sqrt5}\cup\co{\sqrt5}{+\infty}}$'),
]))
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
    return s + (r'$OX$: ' + ', '.join(r'$\res{(%d,\,0)}$' % v for v in rr) if rr else r'$OX$: no en té')
s3 = [tall(rr, y) for (_, _, rr), y in zip(c3, ['4', '0', '-2', '1', '-8', r'\log_23\approx1{,}58', '5', '4'])]
S_.append(("Punts de tall amb els eixos", [
 (1, r"Troba els punts de tall amb els eixos de coordenades:" + tasks(4, ['$f(x)=%s$' % c[0] for c in c3])
     + recorda(r"tall amb $OY$: fem $x=0$; talls amb $OX$: resolem $f(x)=0$."), tasks(2, s3)),
]))

# =====================================================================
# 4. Monotonia, màxims i mínims
P4 = [(-5, -2), (-3, 3), (-1, 1), (1, 4), (3, -3), (6, 2)]
g4 = Plot(-6, 7, -4, 5, W=300)
for (a_, b_), (c_, d_) in zip(P4, P4[1:]): g4.seg(a_, b_, c_, d_)
for q in P4: g4.dot(*q)
sol8 = lambda t: (t - 1) ** 2 / 2 - 2
cknum(sol8(-1), 0); cknum(sol8(3), 0); cknum(sol8(1), -2)
S_.append(("Monotonia. Màxims i mínims", [
 (1, r"Observa la gràfica i indica'n el domini, el recorregut, els intervals de creixement i de decreixement, i els màxims i mínims (relatius i absoluts)." + G(g4, 6),
     r'$D=\res{\cc{-5}{6}}$, $R=\res{\cc{-3}{4}}$. Creixent en $\res{\oo{-5}{-3}\cup\oo{-1}{1}\cup\oo{3}{6}}$; decreixent en $\res{\oo{-3}{-1}\cup\oo{1}{3}}$. Màxims: $\res{(-3,3)}$ relatiu i $\res{(1,4)}$ absolut. Mínims: $\res{(-1,1)}$ relatiu i $\res{(3,-3)}$ absolut.'),
 (2, r"Dibuixa la gràfica d'una funció amb domini $\R$, decreixent en $\oo{-\infty}{1}$, creixent en $\oo{1}{+\infty}$, amb mínim absolut en $(1,-2)$ i que talle l'eix $OX$ en $x=-1$ i en $x=3$. Pots trobar-ne una expressió?",
     r'Per exemple, la paràbola $\res{f(x)=\frac12(x-1)^2-2}$:' + G(Plot(-3, 5, -3, 4, W=220).fn(sol8).dot(1, -2, 'b').dot(-1, 0, 'b').dot(3, 0, 'b'))),
]))

# =====================================================================
# 5. Continuïtat
g5 = Plot(-6, 6, -2, 5, W=320)
g5.fn(lambda t: t / 2 + 3, -6, 0).dot(-3, 1.5, open=True).dot(-3, 3.5).dot(0, 3, open=True)
g5.fn(lambda t: 1 - t / 2, 0, 2).dot(0, 1).dot(2, 0, open=True).fn(lambda t: 1 / (t - 2), 2.02, 6).vl(2)
c5 = [(r'f(x)=\dfrac{x^2-4}{x-2}', 'evitable en $x=2$ (els dos costats arriben a 4, però $f(2)$ no existeix)'),
      (r'g(x)=\dfrac{1}{(x-1)^2}', r'asimptòtica en $x=1$ (pels dos costats tendeix a $+\infty$)'),
      (r'h(x)=\begin{cases}x+1, & \text{si } x\lt1\\ 3-x, & \text{si } x\geq1\end{cases}', 'contínua: els dos trossos arriben a 2 i $h(1)=2$'),
      (r'k(x)=\begin{cases}x^2, & \text{si } x\le0\\ x+2, & \text{si } x\gt0\end{cases}', 'salt finit en $x=0$ (de 0 a 2)')]
ckeq(sympify('(x**2-4)/(x-2)').subs(x, 2.0000001) - 4 < 1e-5, True) if False else None
cknum((2.000001 ** 2 - 4) / (2.000001 - 2), 4, 1e-5)
S_.append(("Continuïtat", [
 (1, r"Indica en quins punts és discontínua aquesta funció i classifica cada discontinuïtat." + G(g5, 6.2),
     r'$x=-3$: $\res{\text{evitable}}$ (el punt està fora de lloc). $x=0$: $\res{\text{salt finit}}$ (de 3 a 1). $x=2$: $\res{\text{salt infinit}}$ (per l\'esquerra arriba a 0 i per la dreta tendeix a $+\infty$).'),
 (2, r"Estudia la continuïtat d'aquestes funcions i classifica les discontinuïtats:" + tasks(2, ['$%s$' % c[0] for c in c5]),
     tasks(1, [c[1] for c in c5])),
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
S_.append(("Simetries i periodicitat", [
 (1, r"Estudia si aquestes funcions són parelles, senars o cap de les dues:" + tasks(4, ['$f(x)=%s$' % c[0] for c in p6]) + recorda(r"parella: $f(-x)=f(x)$; senar: $f(-x)=-f(x)$."),
     tasks(4, [R('\\text{' + {'parella': 'Parella', 'senar': 'Senar', 'cap': 'Cap'}[c[2]] + '}') for c in p6])),
 (2, r"La gràfica següent és la part d'una funció $f$ corresponent a $x\in[0,4]$. Completa-la en $[-4,0]$ si $f$ és parella i, en una altra gràfica, si $f$ és senar." + G(halfplot(0), 4.2),
     tasks(2, ['Parella (simetria respecte de $OY$):' + G(halfplot(1), 3.6), 'Senar (simetria respecte de l\'origen):' + G(halfplot(-1), 3.6)])),
 (2, r"Una funció $f$ és periòdica de període 3, i $f(1)=2$ i $f(2)=-1$. Calcula $f(7)$, $f(-4)$ i $f(11)$.",
     r'$f(7)=f(1+2\cdot3)=\res{2}$; \ $f(-4)=f(-4+6)=f(2)=\res{-1}$; \ $f(11)=f(2+3\cdot3)=\res{-1}$'),
]))

# =====================================================================
# 7. Funcions lineals i afins
ckeq(sympify('1+Rational(1,2)*(x+2)'), sympify('x/2+2')); ckeq(sympify('-1-3*(x-2)'), sympify('-3*x+5'))
l7 = [Plot(-3, 4, -4, 3, W=190).fn(lambda t: 2 * t - 3).dot(0, -3, 'b').dot(2, 1, 'b'),
      Plot(-2, 7, -1, 4, W=190).fn(lambda t: -t / 3 + 2).dot(0, 2, 'b').dot(3, 1, 'b'),
      Plot(-4, 4, -3, 2, W=190).fn(lambda t: -2)]
cknum(1.2 * 12 + 3.5, 17.9); cknum((23 - 3.5) / 1.2, 16.25)
S_.append(("Funcions lineals i afins", [
 (1, r"Troba l'equació de la recta que passa per $A(-2,1)$ i $B(4,4)$. És creixent o decreixent?",
     r'$m=\frac{4-1}{4+2}=\frac12$; \ $y=1+\frac12(x+2)\Rightarrow\res{y=\frac12x+2}$. \ $\res{\text{Creixent}}$ ($m\gt0$).'),
 (1, r"Troba l'equació de la recta de pendent $-3$ que passa per $(2,-1)$ i els seus punts de tall amb els eixos.",
     r'$y=-1-3(x-2)\Rightarrow\res{y=-3x+5}$. \ $OY$: $\res{(0,5)}$; \ $OX$: $\res{\left(\frac53,\,0\right)}$'),
 (1, r"Escriu l'equació de cadascuna d'aquestes rectes:" + tasks(3, [Gi(p, 3.4) for p in l7]),
     tasks(3, [R('y=2x-3'), R(r'y=-\frac13x+2'), R('y=-2')])),
 (2, r"Un taxi cobra $3{,}50$~€ de baixada de bandera i $1{,}20$~€ per quilòmetre. Escriu la funció que dona el preu en funció dels quilòmetres. Quant costa un viatge de 12 km? Quants quilòmetres has fet si has pagat 23~€?",
     r'$\res{f(x)=1{,}2x+3{,}5}$. \ $f(12)=\res{17{,}90\text{ €}}$. \ $1{,}2x+3{,}5=23\Rightarrow\res{x=16{,}25\text{ km}}$'),
]))

# =====================================================================
# 8. Funcions quadràtiques i cúbiques
q8 = [('x^2-6x+5', 1, -6, 5), ('-x^2-2x+3', -1, -2, 3), ('2x^2+4x+3', 2, 4, 3), (r'-\frac12x^2+2', Rational(-1, 2), 0, 2)]
qs, qg = [], []
for tx, A, B, C in q8:
    f = A * x ** 2 + B * x + C; vx = Rational(-B, 1) / (2 * A); vy = f.subs(x, vx); rr = sorted(solve(f, x), key=float)
    qs.append((vx, vy, rr))
ck([(q[0], q[1]) for q in qs] == [(3, -4), (-1, 4), (-1, 1), (0, 2)]); ck([q[2] for q in qs] == [[1, 5], [-3, 1], [], [-2, 2]])
qplot = [Plot(-1, 7, -5, 6, W=180).fn(lambda t: t * t - 6 * t + 5).dot(3, -4, 'v').dot(1, 0, 'b').dot(5, 0, 'b').dot(0, 5, 'g'),
         Plot(-5, 3, -6, 5, W=180).fn(lambda t: -t * t - 2 * t + 3).dot(-1, 4, 'v').dot(-3, 0, 'b').dot(1, 0, 'b').dot(0, 3, 'g'),
         Plot(-4, 2, -1, 9, W=180).fn(lambda t: 2 * t * t + 4 * t + 3).dot(-1, 1, 'v').dot(0, 3, 'g'),
         Plot(-4, 4, -5, 3, W=180).fn(lambda t: -t * t / 2 + 2).dot(0, 2, 'v').dot(-2, 0, 'b').dot(2, 0, 'b')]
qtxt = [r'Còncava $\cup$; $V\res{(3,-4)}$; $OX$: $(1,0)$, $(5,0)$; $OY$: $(0,5)$',
        r'Convexa $\cap$; $V\res{(-1,4)}$; $OX$: $(-3,0)$, $(1,0)$; $OY$: $(0,3)$',
        r'Còncava $\cup$; $V\res{(-1,1)}$; no talla $OX$; $OY$: $(0,3)$',
        r'Convexa $\cap$; $V\res{(0,2)}$; $OX$: $(-2,0)$, $(2,0)$']
ckeq(sympify('x**2-4*x+3').subs(x, 0), 3); ckeq(sympify('x**2-4*x+3').subs(x, 1), 0); ckeq(-Rational(-4) / 2, 2)
th = sympify('-5*x**2+20*x+1'); ck(th.subs(x, 2) == 21)
tg = [v for v in solve(th, x) if float(v) > 0][0]; ckeq(tg, 2 + Ssqrt(105) / 5); cknum(float(tg), 4.05, 1e-3)
ckroots('x**3-4*x**2+3*x', [0, 1, 3])
S_.append(("Funcions quadràtiques i cúbiques", [
 (1, r"Representa aquestes paràboles calculant-ne la forma, el vèrtex i els punts de tall:" + tasks(4, ['$y=%s$' % q[0] for q in q8])
     + recorda(r"$V_x=\dfrac{-b}{2a}$, $V_y=f(V_x)$. Si $a\gt0$, còncava $\cup$; si $a\lt0$, convexa $\cap$."),
     tasks(2, [t + G(p, 3.2) for t, p in zip(qtxt, qplot)])),
 (2, r"Troba la paràbola $y=ax^2+bx+c$ que talla l'eix $OY$ en $(0,3)$, té el vèrtex en $x=2$ i passa pel punt $(1,0)$.",
     r'$c=3$; \ $\frac{-b}{2a}=2\Rightarrow b=-4a$; \ $a+b+3=0\Rightarrow a=1,\ b=-4$: \ $\res{y=x^2-4x+3}$'),
 (2, r"Es llança una pilota cap amunt i la seua altura (en metres) als $t$ segons és $h(t)=-5t^2+20t+1$. Quina altura màxima arriba a tindre i quan? Quan cau a terra?",
     r'Vèrtex: $t=\frac{-20}{-10}=2$ s, $h(2)=\res{21\text{ m}}$ \ (als $\res{2\text{ s}}$). \ $h(t)=0\Rightarrow t=2+\frac{\sqrt{105}}{5}\approx\res{4{,}05\text{ s}}$'),
 (2, r"Troba els punts de tall amb els eixos de $f(x)=x^3-4x^2+3x$ i explica com acaba la gràfica per l'esquerra i per la dreta. Fes-ne un esbós.",
     r'$x(x-1)(x-3)=0$: $OX$ en $\res{(0,0),\ (1,0),\ (3,0)}$; $OY$ en $(0,0)$. Com que $a=1\gt0$, baixa per l\'esquerra i puja per la dreta.' + G(Plot(-1.5, 4.5, -4, 4, W=220).fn(lambda t: t ** 3 - 4 * t * t + 3 * t).dot(0, 0, 'b').dot(1, 0, 'b').dot(3, 0, 'b'))),
]))

# =====================================================================
# 9. Funcions racionals
r9 = [(r'y=\dfrac{2}{x-3}+1', '2/(x-3)+1', None), (r'y=-\dfrac{3}{x+2}', '-3/(x+2)', None),
      (r'y=\dfrac{2x+1}{x-1}', '(2*x+1)/(x-1)', '3/(x-1)+2'), (r'y=\dfrac{x-4}{x-2}', '(x-4)/(x-2)', '-2/(x-2)+1')]
for _, e, tr in r9:
    if tr: ckeq(sympify(e), sympify(tr))
s9 = [r'AV $\res{x=3}$, AH $\res{y=1}$; $D=\R-\{3\}$, $R=\R-\{1\}$; decreixent a cada branca.',
      r'AV $\res{x=-2}$, AH $\res{y=0}$; $D=\R-\{-2\}$, $R=\R-\{0\}$; creixent a cada branca.',
      r'$y=\res{\dfrac{3}{x-1}+2}$: AV $x=1$, AH $y=2$; $D=\R-\{1\}$, $R=\R-\{2\}$; decreixent a cada branca.',
      r'$y=\res{-\dfrac{2}{x-2}+1}$: AV $x=2$, AH $y=1$; $D=\R-\{2\}$, $R=\R-\{1\}$; creixent a cada branca.']
hp = lambda f, h, v: Plot(-6, 6, -5, 6, W=170, lx=2, ly=2).fn(f).vl(h).hl(v)
cknum(600 / 20, 30); cknum(600 / 24, 25)
S_.append(("Funcions racionals", [
 (1, r"Per a cada funció, escriu-la (si cal) com a translació de $y=\frac kx$, indica'n les asímptotes, el domini, el recorregut i la monotonia, i dibuixa-la:" + tasks(4, ['$%s$' % r[0] for r in r9]),
     tasks(2, [s + G(p, 3) for s, p in zip(s9, [hp(lambda t: 2 / (t - 3) + 1 if t != 3 else None, 3, 1), hp(lambda t: -3 / (t + 2) if t != -2 else None, -2, 0),
                                              hp(lambda t: 3 / (t - 1) + 2 if t != 1 else None, 1, 2), hp(lambda t: -2 / (t - 2) + 1 if t != 2 else None, 2, 1)])])),
 (2, r"Un grup lloga un autobús per 600~€ i se'n reparteix el preu a parts iguals. Escriu la funció $p(n)$ que dona el que paga cada persona si hi van $n$ persones. Quant paga cadascú si hi van 20 persones? Quantes persones hi van si cadascuna paga 24~€? Què passa amb $p(n)$ quan $n$ es fa molt gran?",
     r'$\res{p(n)=\frac{600}{n}}$ (proporcionalitat inversa). \ $p(20)=\res{30\text{ €}}$. \ $\frac{600}{n}=24\Rightarrow\res{n=25}$. \ Quan $n$ creix, $p(n)$ s\'acosta a 0 (asímptota horitzontal $y=0$).'),
]))

# =====================================================================
# 10. Funcions radicals
r10 = [(r'y=\sqrt{x-3}+1', (3, 1), r'\co{3}{+\infty}', r'\co{1}{+\infty}', 'creixent', lambda t: sq(t - 3) + 1 if t >= 3 else None),
       (r'y=-\sqrt{x+2}', (-2, 0), r'\co{-2}{+\infty}', r'\oc{-\infty}{0}', 'decreixent', lambda t: -sq(t + 2) if t >= -2 else None),
       (r'y=\sqrt{4-x}', (4, 0), r'\oc{-\infty}{4}', r'\co{0}{+\infty}', 'decreixent', lambda t: sq(4 - t) if t <= 4 else None),
       (r'y=-\sqrt{-x-1}+3', (-1, 3), r'\oc{-\infty}{-1}', r'\oc{-\infty}{3}', 'creixent', lambda t: -sq(-t - 1) + 3 if t <= -1 else None)]
for _, (a_, b_), _, _, _, f in r10: cknum(f(a_), b_)
rp = lambda f, s: Plot(-6, 7, -4, 5, W=170, lx=2, ly=2).fn(f).dot(*s, col='b')
S_.append(("Funcions radicals", [
 (1, r"Indica el punt on comença cada funció, el domini, el recorregut i la monotonia, i dibuixa-les:" + tasks(4, ['$%s$' % r[0] for r in r10]),
     tasks(2, [r'Comença en $\res{(%d,%d)}$; $D=%s$, $R=%s$; %s.' % (r[1][0], r[1][1], r[2], r[3], r[4]) + G(rp(r[5], r[1]), 3) for r in r10])),
 (2, r"Escriu l'expressió de la funció radical representada, que és una translació de $y=\sqrt x$." + G(Plot(-3, 8, -3, 2, W=220).fn(lambda t: sq(t + 1) - 2 if t >= -1 else None, -1, 8).dot(-1, -2, 'b').dot(3, 0, 'b'), 4),
     r'Comença en $(-1,-2)$: $\res{y=\sqrt{x+1}-2}$ (comprovació: passa per $(3,0)$).'),
]))
cknum(sq(3 + 1) - 2, 0)

# =====================================================================
# 11. Exponencials i logarítmiques
ex11 = [(r'y=2^{x-1}+3', 'y=3', '(1,4)', r'\oo{3}{+\infty}', 'creixent', lambda t: 2 ** (t - 1) + 3, (1, 4)),
        (r'y=\left(\frac13\right)^x-2', 'y=-2', '(0,-1)', r'\oo{-2}{+\infty}', 'decreixent', lambda t: (1 / 3) ** t - 2, (0, -1)),
        (r'y=-3^{x+1}', 'y=0', '(-1,-1)', r'\oo{-\infty}{0}', 'decreixent', lambda t: -3 ** (t + 1), (-1, -1)),
        (r'y=1-2^x', 'y=1', '(0,0)', r'\oo{-\infty}{1}', 'decreixent', lambda t: 1 - 2 ** t, (0, 0))]
for e in ex11: cknum(e[5](e[6][0]), e[6][1])
lg11 = [(r'y=\log_2(x+3)', 'x=-3', '(-2,0)', r'\oo{-3}{+\infty}', 'creixent', lambda t: lg(2, t + 3), (-2, 0)),
        (r'y=\log_3x-1', 'x=0', '(1,-1)', r'\oo{0}{+\infty}', 'creixent', lambda t: lg(3, t) - 1, (1, -1)),
        (r'y=\log_{\frac12}(x-1)+2', 'x=1', '(2,2)', r'\oo{1}{+\infty}', 'decreixent', lambda t: lg(.5, t - 1) + 2, (2, 2)),
        (r'y=\log(x-2)+1', 'x=2', '(3,1)', r'\oo{2}{+\infty}', 'creixent', lambda t: lg(10, t - 2) + 1, (3, 1))]
for e in lg11: cknum(e[5](e[6][0]), e[6][1])
P30 = 5000 * 1.03 ** 10; T30 = math.log(2) / math.log(1.03); M31 = 200 * .8 ** 3; T31 = math.log(.25) / math.log(.8)
cknum(round(P30), 6720); cknum(round(T30, 2), 23.45); cknum(M31, 102.4); cknum(round(T31, 2), 6.21)
ep = lambda f, s, h: Plot(-5, 5, -5, 6, W=170, lx=2, ly=2).fn(f).dot(*s, col='b').hl(h)
lp = lambda f, s, v: Plot(-4, 8, -4, 5, W=170, lx=2, ly=2).fn(f).dot(*s, col='b').vl(v)
S_.append(("Funcions exponencials i logarítmiques", [
 (1, r"Indica l'asímptota horitzontal, el punt de referència (la imatge del $(0,1)$ de $y=a^x$), el recorregut i la monotonia, i dibuixa-les:" + tasks(4, ['$%s$' % e[0] for e in ex11]),
     tasks(2, [r'AH $\res{%s}$; punt $%s$; $R=%s$; %s.' % (e[1], e[2], e[3], e[4]) + G(ep(e[5], e[6], float(e[1][2:])), 3) for e in ex11])),
 (1, r"Indica l'asímptota vertical, el punt de referència (la imatge del $(1,0)$ de $y=\log_ax$), el domini i la monotonia, i dibuixa-les:" + tasks(4, ['$%s$' % e[0] for e in lg11]),
     tasks(2, [r'AV $\res{%s}$; punt $%s$; $D=%s$; %s.' % (e[1], e[2], e[3], e[4]) + G(lp(e[5], e[6], float(e[1][2:])), 3) for e in lg11])),
 (2, r"La població d'un poble, que ara té 5\,000 habitants, creix un 3\,\% cada any: $P(t)=5\,000\cdot1{,}03^t$. Quants habitants tindrà d'ací a 10 anys? Quant de temps tardarà a duplicar-se?",
     r'$P(10)=5\,000\cdot1{,}03^{10}\approx\res{6\,720}$ habitants. \ $1{,}03^t=2\Rightarrow t=\frac{\log2}{\log1{,}03}\approx\res{23{,}45\text{ anys}}$'),
 (2, r"Un pacient pren 200 mg d'un medicament i cada hora se n'elimina el 20\,\%. Escriu la funció que dona la quantitat que queda al cap de $t$ hores. Quant en queda al cap de 3 hores? Quan quedaran menys de 50 mg?",
     r'$\res{m(t)=200\cdot0{,}8^t}$. \ $m(3)=\res{102{,}4\text{ mg}}$. \ $0{,}8^t\lt0{,}25\Rightarrow t\gt\frac{\log0{,}25}{\log0{,}8}\approx\res{6{,}21\text{ h}}$'),
]))

# =====================================================================
# 12. Trigonomètriques
for v in (PI / 2, 3 * PI / 2): cknum(math.cos(v), 0)
ck(abs(math.sin(PI) * math.cos(PI)) < 1e-12)
S_.append(("Funcions trigonomètriques", [
 (1, r"Respon fent servir les gràfiques de les funcions trigonomètriques:" + tasks(1, [
     r"En quins punts de $[0,2\pi]$ talla l'eix $OX$ la funció $y=\cos x$? On té els màxims i els mínims en $[0,4\pi]$?",
     r"Quin és el domini de $y=\tan x$? I el període?",
     r"Indica el recorregut i el període de $y=3\sin x-1$ i de $y=2+\cos x$.",
     r"Estudia la simetria de $f(x)=\sin x\cdot\cos x$ i de $g(x)=x\sin x$."]),
     tasks(1, [r'$x=\res{\frac\pi2,\ \frac{3\pi}2}$. Màxims: $\res{(0,1),\ (2\pi,1),\ (4\pi,1)}$; mínims: $\res{(\pi,-1),\ (3\pi,-1)}$.',
               r'$D=\res{\R-\left\{\frac\pi2+\pi k,\ k\in\mathbb Z\right\}}$; període $\res{\pi}$.',
               r'$y=3\sin x-1$: $R=\res{\cc{-4}{2}}$, $T=2\pi$. \ $y=2+\cos x$: $R=\res{\cc{1}{3}}$, $T=2\pi$.',
               r'$f(-x)=-\sin x\cos x=-f(x)$: $\res{\text{senar}}$. \ $g(-x)=(-x)(-\sin x)=g(x)$: $\res{\text{parella}}$.'])),
]))

# =====================================================================
# 13. A trossos i valor absolut
fp = lambda t: 2 * t + 4 if t < -1 else (t * t - 1 if t < 2 else 3)
ck([fp(-3), fp(0), fp(2), fp(5)] == [-2, -1, 3, 3])
g13 = Plot(-5, 5, -4, 5, W=230).fn(lambda t: 2 * t + 4, -5, -1).dot(-1, 2, open=True).fn(lambda t: t * t - 1, -1, 2).dot(-1, 0).seg(2, 3, 5, 3).dot(2, 3)
gq = Plot(-4, 5, -1, 5, W=230).fn(lambda t: -t, -4, 0).fn(lambda t: t * t, 0, 2).dot(2, 4).seg(2, 1, 5, 1).dot(2, 1, open=True)
ab = [('|x-3|', r'\begin{cases}-x+3, & \text{si } x\lt3\\ x-3, & \text{si } x\geq3\end{cases}', None),
      ('|x^2-4x|', r'\begin{cases}x^2-4x, & \text{si } x\lt0\\ -x^2+4x, & \text{si } 0\le x\le4\\ x^2-4x, & \text{si } x\gt4\end{cases}', lambda t: abs(t * t - 4 * t)),
      ('|x^2-x-2|', r'\begin{cases}x^2-x-2, & \text{si } x\lt-1\\ -x^2+x+2, & \text{si } -1\le x\le2\\ x^2-x-2, & \text{si } x\gt2\end{cases}', lambda t: abs(t * t - t - 2)),
      ('|2x+1|', r'\begin{cases}-2x-1, & \text{si } x\lt-\frac12\\ 2x+1, & \text{si } x\geq-\frac12\end{cases}', None)]
ckroots('x**2-4*x', [0, 4]); ckroots('x**2-x-2', [-1, 2])
S_.append(("Funcions a trossos i valor absolut", [
 (1, r"Representa $f(x)=\begin{cases}2x+4, & \text{si } x\lt-1\\ x^2-1, & \text{si } -1\le x\lt2\\ 3, & \text{si } x\geq2\end{cases}$, calcula $f(-3)$, $f(0)$, $f(2)$ i $f(5)$, i estudia'n la continuïtat i el recorregut.",
     r'$f(-3)=\res{-2}$, $f(0)=\res{-1}$, $f(2)=\res{3}$, $f(5)=\res{3}$. En $x=-1$: $\res{\text{salt finit}}$ (de 2 a 0); en $x=2$: $\res{\text{contínua}}$ (els dos costats arriben a 3). $R=\res{\oc{-\infty}{3}}$.' + G(g13, 4.2)),
 (2, r"Escriu l'expressió de la funció a trossos representada:" + G(gq, 4.2),
     r'$\res{f(x)=\begin{cases}-x, & \text{si } x\lt0\\ x^2, & \text{si } 0\le x\le2\\ 1, & \text{si } x\gt2\end{cases}}$'),
 (1, r"Escriu a trossos i representa:" + tasks(4, ['$y=%s$' % a_[0] for a_ in ab]) + recorda(r"troba on s'anul·la l'expressió de dins, estudia'n el signe i canvia-li el signe on és negativa."),
     tasks(2, ['$y=%s$' % a_[1] + (G(Plot(-2, 6, -1, 6, W=170).fn(a_[2]).fn(lambda t: t * t - 4 * t, col='v', dash=True), 2.8) if i == 1 else G(Plot(-3, 4, -1, 6, W=170).fn(a_[2]).fn(lambda t: t * t - t - 2, col='v', dash=True), 2.8) if i == 2 else '') for i, a_ in enumerate(ab)])),
]))

# =====================================================================
# 14. Composició i inversa
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
S_.append(("Composició de funcions i funció inversa", [
 (1, r"Amb $f(x)=x^2+1$, $g(x)=2x-3$ i $h(x)=\dfrac{1}{x+1}$, calcula:" + tasks(3, [r'$(f\circ g)(x)$', r'$(g\circ f)(x)$', r'$(h\circ g)(x)$', r'$(g\circ h)(x)$', r'$(f\circ f)(x)$', r'$(f\circ g)(2)$']),
     tasks(3, [R('4x^2-12x+10'), R('2x^2-1'), R(r'\frac{1}{2x-2}'), R(r'\frac{-3x-1}{x+1}'), R('x^4+2x^2+2'), R('2')])),
 (2, r"Escriu cada funció com a composició de dues funcions més senzilles, $F=f\circ g$:" + tasks(4, [r'$F(x)=\sqrt{3x+1}$', r'$F(x)=(x-5)^4$', r'$F(x)=2^{x^2}$', r'$F(x)=\dfrac{1}{x^2+3}$']),
     tasks(2, [r'$g(x)=3x+1$, $f(x)=\sqrt x$', r'$g(x)=x-5$, $f(x)=x^4$', r'$g(x)=x^2$, $f(x)=2^x$', r'$g(x)=x^2+3$, $f(x)=\frac1x$'])),
 (1, r"Calcula la inversa de cada funció i comprova que $(f\circ f^{-1})(x)=x$:" + tasks(4, ['$f(x)=%s$' % i[0] for i in inv])
     + r'En g) considera només $x\geq1$.' + recorda(r"canvia $f(x)$ per $y$, intercanvia $x$ i $y$ i aïlla $y$."),
     tasks(2, [r'$f^{-1}(x)=\res{%s}$' % i[3] for i in inv]) + r'Fixa\'t que la funció d) és la seua pròpia inversa.'),
 (2, r"Dibuixa en uns mateixos eixos $f(x)=2^x$, la recta $y=x$ i la inversa de $f$. Quina funció és?",
     r'$f^{-1}(x)=\res{\log_2x}$, simètrica de $2^x$ respecte de $y=x$.' + G(Plot(-3, 6, -3, 6, W=210).seg(-3, -3, 6, 6, 'm', True).fn(lambda t: 2 ** t).fn(lambda t: lg(2, t), .01, 6, 'g'), 3.6)),
]))

# =====================================================================
# 15. Estudis complets i problemes
f15 = sympify('(x+1)/(x-2)'); ckeq(f15, sympify('3/(x-2)+1')); ck(f15.subs(x, 0) == Rational(-1, 2)); ckroots('x+1', [-1])
g15 = lambda t: t * t - 2 * abs(t)
ck([g15(-2), g15(0), g15(2), g15(1), g15(-1)] == [0, 0, 0, -1, -1])
tarifa = lambda t: 10 if t <= 5 else 10 + 2 * (t - 5)
ck([tarifa(3), tarifa(8), tarifa(5)] == [10, 16, 10])
S_.append(("Estudis complets i problemes", [
 (2, r"Fes l'estudi complet de $f(x)=\dfrac{x+1}{x-2}$: domini, talls amb els eixos, expressió com a translació de $y=\frac kx$, asímptotes, monotonia, recorregut, simetria i gràfica.",
     r'$D=\res{\R-\{2\}}$; $OY$: $\res{\left(0,-\frac12\right)}$; $OX$: $\res{(-1,0)}$. $f(x)=\res{\frac{3}{x-2}+1}$: AV $x=2$, AH $y=1$. Decreixent a cada branca; $R=\res{\R-\{1\}}$; sense simetria.'
     + G(Plot(-6, 8, -5, 7, W=220, lx=2, ly=2).fn(lambda t: (t + 1) / (t - 2) if t != 2 else None).vl(2).hl(1).dot(0, -.5, 'g').dot(-1, 0, 'b'), 4)),
 (2, r"Escriu a trossos $f(x)=x^2-2|x|$ i fes-ne l'estudi: domini, talls, simetria, monotonia, extrems i recorregut.",
     r'$f(x)=\res{\begin{cases}x^2+2x, & \text{si } x\lt0\\ x^2-2x, & \text{si } x\geq0\end{cases}}$. $D=\R$; talls $(-2,0)$, $(0,0)$, $(2,0)$; $\res{\text{parella}}$. Decreixent en $\oo{-\infty}{-1}\cup\oo{0}{1}$ i creixent en $\oo{-1}{0}\cup\oo{1}{+\infty}$; mínims absoluts $\res{(-1,-1),\ (1,-1)}$, màxim relatiu $\res{(0,0)}$; $R=\res{\co{-1}{+\infty}}$.'
     + G(Plot(-3.5, 3.5, -2, 4, W=220).fn(g15).dot(-1, -1, 'v').dot(1, -1, 'v').dot(0, 0, 'v').dot(-2, 0, 'b').dot(2, 0, 'b'), 4)),
 (2, r"Una companyia de telefonia cobra 10~€ al mes si es gasten com a molt 5 GB de dades, i 2~€ més per cada GB que passe de 5. Escriu la funció que dona el preu segons els GB gastats, $x\geq0$, representa-la i calcula el preu si es gasten 3 GB i 8 GB. És contínua?",
     r'$\res{f(x)=\begin{cases}10, & \text{si } 0\le x\le5\\ 2x, & \text{si } x\gt5\end{cases}}$ \ ($10+2(x-5)=2x$). \ $f(3)=\res{10\text{ €}}$, $f(8)=\res{16\text{ €}}$. És $\res{\text{contínua}}$: en $x=5$ els dos trossos valen 10.'
     + G(Plot(-1, 10, -2, 22, W=220, sy=2, ly=4).seg(0, 10, 5, 10).fn(lambda t: 2 * t, 5, 10).dot(0, 10), 4)),
]))
ck(all(2 * t == 10 + 2 * (t - 5) for t in range(6, 12)))

assert all(CHK)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={funcions, domini, recorregut, punts de tall, monotonia, màxims i mínims, continuïtat, simetria, periodicitat, funció lineal, paràbola, hipèrbola, funció radical, exponencial, logaritme, funcions a trossos, valor absolut, composició, funció inversa}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques I}')
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def fix(t):
    """Fora dels dibuixos: l'apòstrof escrit \\' dins de cadenes r'' (en LaTeX seria un accent) i l'espai després
    de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = "Estudi de funcions"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 7: %s. 1r de Batxillerat MI}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 7: %s · 1r Batxillerat MI" % (t, TIT))
    assert 'funcions · 1r' in p and 'unitat 7: Estudi' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques I}{1r Batx}{''' + ('Solucions de la fitxa · Unitat 7' if sol else "Fitxa d'exercicis · Unitat 7") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Els intervals s'escriuen com als apunts: $\left]a,b\right[$ obert i $[a,b]$ tancat. Pots comprovar dominis, talls, translacions, composicions i inverses amb els ginys dels apunts interactius de la unitat."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos i fes un dibuix sempre que t'ajude. Escriu els intervals com als apunts ($\left]a,b\right[$ obert, $[a,b]$ tancat). Les seccions segueixen l'ordre dels apunts i la darrera té estudis complets i problemes.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't7-fitxa-solucions.tex' if sol else 't7-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis;', len(CHK), 'comprovacions')
