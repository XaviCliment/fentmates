# Versió en castellà de genera.py: escriu els -es.tex. Original: genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (1r Batxillerat MI, Unitat 7: Funcions elementals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# La fitxa segueix els apartats dels apunts (7.1-7.9): les funcions elementals i, al final, problemes de màxims i mínims
# amb funcions quadràtiques (vèrtex i extrems de l'interval; sense límits ni derivades).
# Comprovacions: sympy calcula talls i vèrtexs; els màxims i mínims en un interval es comproven també amb una malla fina.
# Les gràfiques es dibuixen amb la classe Plot de _eines/apunts/1batx-mi-t6/fig.py (la mateixa dels apunts).
# Ús: python3 genera.py && pdflatex t7-fitxa-exercicis.tex (dues vegades) && pdflatex t7-fitxa-solucions.tex (dues vegades)
import os, re, sys, math
from sympy import symbols, sympify, solve, simplify, expand, Rational, sqrt as Ssqrt, S, log as Slog, Abs, Poly, nsimplify
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "apunts", "1batx-mi-t6"))
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
# 1. Funcions lineals i afins
ckeq(sympify('1+Rational(1,2)*(x+2)'), sympify('x/2+2')); ckeq(sympify('-1-3*(x-2)'), sympify('-3*x+5'))
l7 = [Plot(-3, 4, -4, 3, W=190).fn(lambda t: 2 * t - 3).dot(0, -3, 'b').dot(2, 1, 'b'),
      Plot(-2, 7, -1, 4, W=190).fn(lambda t: -t / 3 + 2).dot(0, 2, 'b').dot(3, 1, 'b'),
      Plot(-4, 4, -3, 2, W=190).fn(lambda t: -2)]
cknum(1.2 * 12 + 3.5, 17.9); cknum((23 - 3.5) / 1.2, 16.25)
S_.append(("Funciones lineales y afines", [
 (1, r"Halla la ecuación de la recta que pasa por $A(-2,1)$ y $B(4,4)$. ¿Es creciente o decreciente?",
     r'$m=\frac{4-1}{4+2}=\frac12$; \ $y=1+\frac12(x+2)\Rightarrow\res{y=\frac12x+2}$. \ $\res{\text{Creciente}}$ ($m\gt0$).'),
 (1, r"Halla la ecuación de la recta de pendiente $-3$ que pasa por $(2,-1)$ y sus puntos de corte con los ejes.",
     r'$y=-1-3(x-2)\Rightarrow\res{y=-3x+5}$. \ $OY$: $\res{(0,5)}$; \ $OX$: $\res{\left(\frac53,\,0\right)}$'),
 (1, r"Escribe la ecuación de cada una de estas rectas:" + tasks(3, [Gi(p, 3.4) for p in l7]),
     tasks(3, [R('y=2x-3'), R(r'y=-\frac13x+2'), R('y=-2')])),
 (2, r"Un taxi cobra $3{,}50$~€ de bajada de bandera y $1{,}20$~€ por kilómetro. Escribe la función que da el precio en función de los kilómetros. ¿Cuánto cuesta un viaje de 12 km? ¿Cuántos kilómetros has recorrido si has pagado 23~€?",
     r'$\res{f(x)=1{,}2x+3{,}5}$. \ $f(12)=\res{17{,}90\text{ €}}$. \ $1{,}2x+3{,}5=23\Rightarrow\res{x=16{,}25\text{ km}}$'),
 (1, r"Halla la ecuación de la recta paralela a $y=3x-1$ que pasa por el punto $(1,5)$.",
     r'Las rectas paralelas tienen la misma pendiente, $m=3$: $y=5+3(x-1)\Rightarrow\res{y=3x+2}$'),
 (2, r"Un depósito tiene 200 L de agua y se vacía a razón de 8 L por minuto. Escribe la función $V(t)$ que da los litros que quedan al cabo de $t$ minutos. ¿Cuándo se vacía? ¿Cuál es el dominio de la función en este contexto?",
     r'$\res{V(t)=200-8t}$. \ $V(t)=0\Rightarrow\res{t=25\text{ min}}$. \ $D=\res{\cc{0}{25}}$ (decreciente; recorrido $[0,200]$).'),
]))
ck(5 + 3 * (0 - 1) == 2 and 200 - 8 * 25 == 0)

# =====================================================================
# 2. Funcions quadràtiques i cúbiques
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
qtxt = [r'Cóncava $\cup$; $V\res{(3,-4)}$; $OX$: $(1,0)$, $(5,0)$; $OY$: $(0,5)$',
        r'Convexa $\cap$; $V\res{(-1,4)}$; $OX$: $(-3,0)$, $(1,0)$; $OY$: $(0,3)$',
        r'Cóncava $\cup$; $V\res{(-1,1)}$; no corta $OX$; $OY$: $(0,3)$',
        r'Convexa $\cap$; $V\res{(0,2)}$; $OX$: $(-2,0)$, $(2,0)$']
ckeq(sympify('x**2-4*x+3').subs(x, 0), 3); ckeq(sympify('x**2-4*x+3').subs(x, 1), 0); ckeq(-Rational(-4) / 2, 2)
th = sympify('-5*x**2+20*x+1'); ck(th.subs(x, 2) == 21)
tg = [v for v in solve(th, x) if float(v) > 0][0]; ckeq(tg, 2 + Ssqrt(105) / 5); cknum(float(tg), 4.05, 1e-3)
ckroots('x**3-4*x**2+3*x', [0, 1, 3])
S_.append(("Funciones cuadráticas y cúbicas", [
 (1, r"Representa estas parábolas calculando su forma, su vértice y sus puntos de corte:" + tasks(4, ['$y=%s$' % q[0] for q in q8])
     + recorda(r"$V_x=\dfrac{-b}{2a}$, $V_y=f(V_x)$. Si $a\gt0$, cóncava $\cup$; si $a\lt0$, convexa $\cap$."),
     tasks(2, [t + G(p, 3.2) for t, p in zip(qtxt, qplot)])),
 (2, r"Halla la parábola $y=ax^2+bx+c$ que corta al eje $OY$ en $(0,3)$, tiene el vértice en $x=2$ y pasa por el punto $(1,0)$.",
     r'$c=3$; \ $\frac{-b}{2a}=2\Rightarrow b=-4a$; \ $a+b+3=0\Rightarrow a=1,\ b=-4$: \ $\res{y=x^2-4x+3}$'),
 (2, r"Se lanza una pelota hacia arriba y su altura (en metros) a los $t$ segundos es $h(t)=-5t^2+20t+1$. ¿Qué altura máxima alcanza y cuándo? ¿Cuándo cae al suelo?",
     r'Vértice: $t=\frac{-20}{-10}=2$ s, $h(2)=\res{21\text{ m}}$ \ (a los $\res{2\text{ s}}$). \ $h(t)=0\Rightarrow t=2+\frac{\sqrt{105}}{5}\approx\res{4{,}05\text{ s}}$'),
 (2, r"Halla los puntos de corte con los ejes de $f(x)=x^3-4x^2+3x$ y explica cómo acaba la gráfica por la izquierda y por la derecha. Haz un esbozo.",
     r'$x(x-1)(x-3)=0$: $OX$ en $\res{(0,0),\ (1,0),\ (3,0)}$; $OY$ en $(0,0)$. Como $a=1\gt0$, baja por la izquierda y sube por la derecha.' + G(Plot(-1.5, 4.5, -4, 4, W=220).fn(lambda t: t ** 3 - 4 * t * t + 3 * t).dot(0, 0, 'b').dot(1, 0, 'b').dot(3, 0, 'b'))),
]))

# =====================================================================
# 3. Funcions racionals
r9 = [(r'y=\dfrac{2}{x-3}+1', '2/(x-3)+1', None), (r'y=-\dfrac{3}{x+2}', '-3/(x+2)', None),
      (r'y=\dfrac{2x+1}{x-1}', '(2*x+1)/(x-1)', '3/(x-1)+2'), (r'y=\dfrac{x-4}{x-2}', '(x-4)/(x-2)', '-2/(x-2)+1')]
for _, e, tr in r9:
    if tr: ckeq(sympify(e), sympify(tr))
s9 = [r'AV $\res{x=3}$, AH $\res{y=1}$; $D=\R-\{3\}$, $R=\R-\{1\}$; decreciente en cada rama.',
      r'AV $\res{x=-2}$, AH $\res{y=0}$; $D=\R-\{-2\}$, $R=\R-\{0\}$; creciente en cada rama.',
      r'$y=\res{\dfrac{3}{x-1}+2}$: AV $x=1$, AH $y=2$; $D=\R-\{1\}$, $R=\R-\{2\}$; decreciente en cada rama.',
      r'$y=\res{-\dfrac{2}{x-2}+1}$: AV $x=2$, AH $y=1$; $D=\R-\{2\}$, $R=\R-\{1\}$; creciente en cada rama.']
hp = lambda f, h, v: Plot(-6, 6, -5, 6, W=170, lx=2, ly=2).fn(f).vl(h).hl(v)
cknum(600 / 20, 30); cknum(600 / 24, 25)
S_.append(("Funciones racionales", [
 (1, r"Para cada función, escríbela (si hace falta) como traslación de $y=\frac kx$, indica sus asíntotas, su dominio, su recorrido y su monotonía, y dibújala:" + tasks(4, ['$%s$' % r[0] for r in r9]),
     tasks(2, [s + G(p, 3) for s, p in zip(s9, [hp(lambda t: 2 / (t - 3) + 1 if t != 3 else None, 3, 1), hp(lambda t: -3 / (t + 2) if t != -2 else None, -2, 0),
                                              hp(lambda t: 3 / (t - 1) + 2 if t != 1 else None, 1, 2), hp(lambda t: -2 / (t - 2) + 1 if t != 2 else None, 2, 1)])])),
 (2, r"Un grupo alquila un autobús por 600~€ y se reparte el precio a partes iguales. Escribe la función $p(n)$ que da lo que paga cada persona si van $n$ personas. ¿Cuánto paga cada uno si van 20 personas? ¿Cuántas personas van si cada una paga 24~€? ¿Qué pasa con $p(n)$ cuando $n$ se hace muy grande?",
     r'$\res{p(n)=\frac{600}{n}}$ (proporcionalidad inversa). \ $p(20)=\res{30\text{ €}}$. \ $\frac{600}{n}=24\Rightarrow\res{n=25}$. \ Cuando $n$ crece, $p(n)$ se acerca a 0 (asíntota horizontal $y=0$).'),
 (2, r"Una hipérbola de la forma $y=\dfrac{k}{x-a}+b$ tiene las asíntotas $x=2$ e $y=1$ y pasa por el punto $(3,4)$. Halla su expresión y el punto de corte con el eje $OY$.",
     r'$a=2$, $b=1$; \ $4=\frac{k}{3-2}+1\Rightarrow k=3$: \ $\res{y=\dfrac{3}{x-2}+1}$. \ $OY$: $y=-\frac32+1$: $\res{\left(0,\,-\frac12\right)}$'),
]))
ck(3 / (3 - 2) + 1 == 4 and 3 / (0 - 2) + 1 == -0.5)

# =====================================================================
# 4. Funcions radicals
r10 = [(r'y=\sqrt{x-3}+1', (3, 1), r'\co{3}{+\infty}', r'\co{1}{+\infty}', 'creciente', lambda t: sq(t - 3) + 1 if t >= 3 else None),
       (r'y=-\sqrt{x+2}', (-2, 0), r'\co{-2}{+\infty}', r'\oc{-\infty}{0}', 'decreciente', lambda t: -sq(t + 2) if t >= -2 else None),
       (r'y=\sqrt{4-x}', (4, 0), r'\oc{-\infty}{4}', r'\co{0}{+\infty}', 'decreciente', lambda t: sq(4 - t) if t <= 4 else None),
       (r'y=-\sqrt{-x-1}+3', (-1, 3), r'\oc{-\infty}{-1}', r'\oc{-\infty}{3}', 'creciente', lambda t: -sq(-t - 1) + 3 if t <= -1 else None)]
for _, (a_, b_), _, _, _, f in r10: cknum(f(a_), b_)
rp = lambda f, s: Plot(-6, 7, -4, 5, W=170, lx=2, ly=2).fn(f).dot(*s, col='b')
S_.append(("Funciones radicales", [
 (1, r"Indica el punto donde empieza cada función, el dominio, el recorrido y la monotonía, y dibújalas:" + tasks(4, ['$%s$' % r[0] for r in r10]),
     tasks(2, [r'Empieza en $\res{(%d,%d)}$; $D=%s$, $R=%s$; %s.' % (r[1][0], r[1][1], r[2], r[3], r[4]) + G(rp(r[5], r[1]), 3) for r in r10])),
 (2, r"Escribe la expresión de la función radical representada, que es una traslación de $y=\sqrt x$." + G(Plot(-3, 8, -3, 2, W=220).fn(lambda t: sq(t + 1) - 2 if t >= -1 else None, -1, 8).dot(-1, -2, 'b').dot(3, 0, 'b'), 4),
     r'Empieza en $(-1,-2)$: $\res{y=\sqrt{x+1}-2}$ (comprobación: pasa por $(3,0)$).'),
 (2, r"Dada $f(x)=\sqrt{2x-4}+1$, indica dónde empieza, el dominio y el recorrido. ¿Para qué valor de $x$ vale $f(x)=3$?",
     r'$2x-4=0\Rightarrow x=2$: empieza en $\res{(2,1)}$; $D=\res{\co{2}{+\infty}}$, $R=\res{\co{1}{+\infty}}$. \ $\sqrt{2x-4}=2\Rightarrow 2x-4=4\Rightarrow\res{x=4}$'),
]))
cknum(math.sqrt(2 * 4 - 4) + 1, 3)
cknum(sq(3 + 1) - 2, 0)

# =====================================================================
# 5. Exponencials i logarítmiques
ex11 = [(r'y=2^{x-1}+3', 'y=3', '(1,4)', r'\oo{3}{+\infty}', 'creciente', lambda t: 2 ** (t - 1) + 3, (1, 4)),
        (r'y=\left(\frac13\right)^x-2', 'y=-2', '(0,-1)', r'\oo{-2}{+\infty}', 'decreciente', lambda t: (1 / 3) ** t - 2, (0, -1)),
        (r'y=-3^{x+1}', 'y=0', '(-1,-1)', r'\oo{-\infty}{0}', 'decreciente', lambda t: -3 ** (t + 1), (-1, -1)),
        (r'y=1-2^x', 'y=1', '(0,0)', r'\oo{-\infty}{1}', 'decreciente', lambda t: 1 - 2 ** t, (0, 0))]
for e in ex11: cknum(e[5](e[6][0]), e[6][1])
lg11 = [(r'y=\log_2(x+3)', 'x=-3', '(-2,0)', r'\oo{-3}{+\infty}', 'creciente', lambda t: lg(2, t + 3), (-2, 0)),
        (r'y=\log_3x-1', 'x=0', '(1,-1)', r'\oo{0}{+\infty}', 'creciente', lambda t: lg(3, t) - 1, (1, -1)),
        (r'y=\log_{\frac12}(x-1)+2', 'x=1', '(2,2)', r'\oo{1}{+\infty}', 'decreciente', lambda t: lg(.5, t - 1) + 2, (2, 2)),
        (r'y=\log(x-2)+1', 'x=2', '(3,1)', r'\oo{2}{+\infty}', 'creciente', lambda t: lg(10, t - 2) + 1, (3, 1))]
for e in lg11: cknum(e[5](e[6][0]), e[6][1])
P30 = 5000 * 1.03 ** 10; T30 = math.log(2) / math.log(1.03); M31 = 200 * .8 ** 3; T31 = math.log(.25) / math.log(.8)
cknum(round(P30), 6720); cknum(round(T30, 2), 23.45); cknum(M31, 102.4); cknum(round(T31, 2), 6.21)
ep = lambda f, s, h: Plot(-5, 5, -5, 6, W=170, lx=2, ly=2).fn(f).dot(*s, col='b').hl(h)
lp = lambda f, s, v: Plot(-4, 8, -4, 5, W=170, lx=2, ly=2).fn(f).dot(*s, col='b').vl(v)
S_.append(("Funciones exponenciales y logarítmicas", [
 (1, r"Indica la asíntota horizontal, el punto de referencia (la imagen del $(0,1)$ de $y=a^x$), el recorrido y la monotonía, y dibújalas:" + tasks(4, ['$%s$' % e[0] for e in ex11]),
     tasks(2, [r'AH $\res{%s}$; punto $%s$; $R=%s$; %s.' % (e[1], e[2], e[3], e[4]) + G(ep(e[5], e[6], float(e[1][2:])), 3) for e in ex11])),
 (1, r"Indica la asíntota vertical, el punto de referencia (la imagen del $(1,0)$ de $y=\log_ax$), el dominio y la monotonía, y dibújalas:" + tasks(4, ['$%s$' % e[0] for e in lg11]),
     tasks(2, [r'AV $\res{%s}$; punto $%s$; $D=%s$; %s.' % (e[1], e[2], e[3], e[4]) + G(lp(e[5], e[6], float(e[1][2:])), 3) for e in lg11])),
 (2, r"La población de un pueblo, que ahora tiene 5\,000 habitantes, crece un 3\,\% cada año: $P(t)=5\,000\cdot1{,}03^t$. ¿Cuántos habitantes tendrá dentro de 10 años? ¿Cuánto tiempo tardará en duplicarse?",
     r'$P(10)=5\,000\cdot1{,}03^{10}\approx\res{6\,720}$ habitantes. \ $1{,}03^t=2\Rightarrow t=\frac{\log2}{\log1{,}03}\approx\res{23{,}45\text{ años}}$'),
 (2, r"Un paciente toma 200 mg de un medicamento y cada hora se elimina el 20\,\%. Escribe la función que da la cantidad que queda al cabo de $t$ horas. ¿Cuánto queda al cabo de 3 horas? ¿Cuándo quedarán menos de 50 mg?",
     r'$\res{m(t)=200\cdot0{,}8^t}$. \ $m(3)=\res{102{,}4\text{ mg}}$. \ $0{,}8^t\lt0{,}25\Rightarrow t\gt\frac{\log0{,}25}{\log0{,}8}\approx\res{6{,}21\text{ h}}$'),
 (2, r"Las gráficas son traslaciones de $y=2^x$ y de $y=\log_2x$. Escribe sus expresiones." + tasks(2, [Gi(Plot(-5, 4, -4, 5, W=190, lx=2, ly=2).fn(lambda t: 2 ** (t + 1) - 3).hl(-3).dot(-1, -2, 'b').dot(1, 1, 'b'), 3.3),
                                                                                                    Gi(Plot(-1, 8, -3, 4, W=190, lx=2, ly=2).fn(lambda t: lg(2, t - 1) + 1, 1.005, 8).vl(1).dot(2, 1, 'b').dot(3, 2, 'b'), 3.3)]),
     tasks(2, [r'AH $y=-3$, punto de referencia $(-1,-2)$: $\res{y=2^{x+1}-3}$', r'AV $x=1$, punto de referencia $(2,1)$: $\res{y=\log_2(x-1)+1}$'])),
]))
ck(2 ** (1 + 1) - 3 == 1 and lg(2, 3 - 1) + 1 == 2)

# =====================================================================
# 6. Trigonomètriques
for v in (PI / 2, 3 * PI / 2): cknum(math.cos(v), 0)
ck(abs(math.sin(PI) * math.cos(PI)) < 1e-12)
S_.append(("Funciones trigonométricas", [
 (1, r"Responde utilizando las gráficas de las funciones trigonométricas:" + tasks(1, [
     r"¿En qué puntos de $[0,2\pi]$ corta al eje $OX$ la función $y=\cos x$? ¿Dónde tiene los máximos y los mínimos en $[0,4\pi]$?",
     r"¿Cuál es el dominio de $y=\tan x$? ¿Y el período?",
     r"Indica el recorrido y el período de $y=3\sin x-1$ y de $y=2+\cos x$.",
     r"Estudia la simetría de $f(x)=\sin x\cdot\cos x$ y de $g(x)=x\sin x$."]),
     tasks(1, [r'$x=\res{\frac\pi2,\ \frac{3\pi}2}$. Máximos: $\res{(0,1),\ (2\pi,1),\ (4\pi,1)}$; mínimos: $\res{(\pi,-1),\ (3\pi,-1)}$.',
               r'$D=\res{\R-\left\{\frac\pi2+\pi k,\ k\in\mathbb Z\right\}}$; período $\res{\pi}$.',
               r'$y=3\sin x-1$: $R=\res{\cc{-4}{2}}$, $T=2\pi$. \ $y=2+\cos x$: $R=\res{\cc{1}{3}}$, $T=2\pi$.',
               r'$f(-x)=-\sin x\cos x=-f(x)$: $\res{\text{impar}}$. \ $g(-x)=(-x)(-\sin x)=g(x)$: $\res{\text{par}}$.'])),
 (2, r"Dibuja en $[0,2\pi]$ las funciones $y=\sin x+1$ e $y=2\cos x$ e indica su recorrido, sus máximos, sus mínimos y sus cortes con el eje $OX$.",
     r'$y=\sin x+1$: $R=\res{\cc{0}{2}}$; máximo $\res{\left(\frac\pi2,2\right)}$, mínimo $\res{\left(\frac{3\pi}2,0\right)}$, que es el único punto de corte con $OX$. \ $y=2\cos x$: $R=\res{\cc{-2}{2}}$; máximos $\res{(0,2),\ (2\pi,2)}$, mínimo $\res{(\pi,-2)}$; cortes $\res{\left(\frac\pi2,0\right),\ \left(\frac{3\pi}2,0\right)}$.'
     + G(Plot(-.3, 2 * PI + .3, -2.5, 2.5, sx=PI / 2, xlab=[(PI / 2, r'\frac\pi2'), (PI, r'\pi'), (3 * PI / 2, r'\frac{3\pi}2'), (2 * PI, r'2\pi')], W=300).fn(lambda t: math.sin(t) + 1).fn(lambda t: 2 * math.cos(t), col='b'), 5)),
]))
cknum(math.sin(3 * PI / 2) + 1, 0); cknum(2 * math.cos(PI), -2)

# =====================================================================
# 7. A trossos i valor absolut
fp = lambda t: 2 * t + 4 if t < -1 else (t * t - 1 if t < 2 else 3)
ck([fp(-3), fp(0), fp(2), fp(5)] == [-2, -1, 3, 3])
g13 = Plot(-5, 5, -4, 5, W=230).fn(lambda t: 2 * t + 4, -5, -1).dot(-1, 2, open=True).fn(lambda t: t * t - 1, -1, 2).dot(-1, 0).seg(2, 3, 5, 3).dot(2, 3)
gq = Plot(-4, 5, -1, 5, W=230).fn(lambda t: -t, -4, 0).fn(lambda t: t * t, 0, 2).dot(2, 4).seg(2, 1, 5, 1).dot(2, 1, open=True)
ab = [('|x-3|', r'\begin{cases}-x+3, & \text{si } x\lt3\\ x-3, & \text{si } x\geq3\end{cases}', None),
      ('|x^2-4x|', r'\begin{cases}x^2-4x, & \text{si } x\lt0\\ -x^2+4x, & \text{si } 0\le x\le4\\ x^2-4x, & \text{si } x\gt4\end{cases}', lambda t: abs(t * t - 4 * t)),
      ('|x^2-x-2|', r'\begin{cases}x^2-x-2, & \text{si } x\lt-1\\ -x^2+x+2, & \text{si } -1\le x\le2\\ x^2-x-2, & \text{si } x\gt2\end{cases}', lambda t: abs(t * t - t - 2)),
      ('|2x+1|', r'\begin{cases}-2x-1, & \text{si } x\lt-\frac12\\ 2x+1, & \text{si } x\geq-\frac12\end{cases}', None)]
ckroots('x**2-4*x', [0, 4]); ckroots('x**2-x-2', [-1, 2])
S_.append(("Funciones a trozos y valor absoluto", [
 (1, r"Representa $f(x)=\begin{cases}2x+4, & \text{si } x\lt-1\\ x^2-1, & \text{si } -1\le x\lt2\\ 3, & \text{si } x\geq2\end{cases}$, calcula $f(-3)$, $f(0)$, $f(2)$ y $f(5)$, y estudia su continuidad y su recorrido.",
     r'$f(-3)=\res{-2}$, $f(0)=\res{-1}$, $f(2)=\res{3}$, $f(5)=\res{3}$. En $x=-1$: $\res{\text{salto finito}}$ (de 2 a 0); en $x=2$: $\res{\text{continua}}$ (los dos lados llegan a 3). $R=\res{\oc{-\infty}{3}}$.' + G(g13, 4.2)),
 (2, r"Escribe la expresión de la función a trozos representada:" + G(gq, 4.2),
     r'$\res{f(x)=\begin{cases}-x, & \text{si } x\lt0\\ x^2, & \text{si } 0\le x\le2\\ 1, & \text{si } x\gt2\end{cases}}$'),
 (1, r"Escribe a trozos y representa:" + tasks(4, ['$y=%s$' % a_[0] for a_ in ab]) + recorda(r"halla dónde se anula la expresión de dentro, estudia su signo y cámbiale el signo donde es negativa."),
     tasks(2, ['$y=%s$' % a_[1] + (G(Plot(-2, 6, -1, 6, W=170).fn(a_[2]).fn(lambda t: t * t - 4 * t, col='v', dash=True), 2.8) if i == 1 else G(Plot(-3, 4, -1, 6, W=170).fn(a_[2]).fn(lambda t: t * t - t - 2, col='v', dash=True), 2.8) if i == 2 else '') for i, a_ in enumerate(ab)])),
 (2, r"Un aparcamiento cobra 2~€ por la primera hora (o fracción) y $1{,}50$~€ por cada hora de más. Escribe la función a trozos que da el precio según las horas $x$ (con $x\gt0$, contando las horas de manera continua), calcula el precio de 3 horas y cuántas horas has estado si pagas 8~€. ¿Es continua en $x=1$?",
     r'$\res{f(x)=\begin{cases}2, & \text{si } 0\lt x\le1\\ 2+1{,}5(x-1), & \text{si } x\gt1\end{cases}}$. \ $f(3)=\res{5\text{ €}}$. \ $2+1{,}5(x-1)=8\Rightarrow\res{x=5\text{ h}}$. \ $\res{\text{Sí}}$: los dos trozos valen 2.'),
 (2, r"Resuelve gráficamente la ecuación $|x-1|=3$: dibuja $y=|x-1|$ y la recta $y=3$, y halla dónde se cortan.",
     r'$x-1=3$ o $x-1=-3$: $\res{x=4,\ x=-2}$.' + G(Plot(-4, 6, -1, 5, W=210).fn(lambda t: abs(t - 1)).fn(lambda t: 3, col='b').dot(-2, 3, 'g').dot(4, 3, 'g'), 3.6)),
]))
ck(2 + 1.5 * (3 - 1) == 5 and 2 + 1.5 * (5 - 1) == 8 and abs(4 - 1) == 3 and abs(-2 - 1) == 3)

# =====================================================================
# 8. Problemes amb funcions quadràtiques: màxims i mínims sense derivades (vèrtex i extrems de l'interval)
def maxmin(f, a, b, vx):
    """màxim i mínim de f en [a,b]: es comparen el vèrtex (si és dins) i els extrems; es comprova amb una malla fina"""
    cand = [a, b] + ([vx] if a <= vx <= b else [])
    vals = [f(c) for c in cand]
    mesh = [f(a + (b - a) * i / 4000) for i in range(4001)]
    ck(abs(max(vals) - max(mesh)) < 1e-6 and abs(min(vals) - min(mesh)) < 1e-6)
    return max(vals), min(vals)
I1 = lambda p: p * (200 - 4 * p)
ck(maxmin(I1, 0, 50, 25) == (2500, 0)); ck(maxmin(I1, 30, 45, 25)[0] == 2400)
B2 = lambda t: 60 * t - (t * t + 20 * t + 300)
ck(maxmin(B2, 0, 50, 20)[0] == 100); ckroots('-x**2+40*x-300', [10, 30]); ck(maxmin(B2, 0, 15, 20)[0] == 75)
C3 = lambda t: .5 * t * t - 20 * t + 250
ck(maxmin(C3, 0, 40, 20)[1] == 50); ck(maxmin(C3, 0, 15, 20)[1] == 62.5)
A4 = lambda t: t * (60 - 2 * t)
ck(maxmin(A4, 0, 30, 15)[0] == 450)
H5 = lambda n: (80 + 5 * n) * (40 - n)
ck(maxmin(H5, 0, 40, 12)[0] == 3920 and 80 + 5 * 12 == 140 and 40 - 12 == 28)
F6 = lambda t: t * t - 4 * t + 1
ck(maxmin(F6, -1, 3, 2) == (6, -3)); ck(maxmin(F6, 3, 5, 2) == (6, -2))
P7 = lambda t: t * (20 - t); Q7 = lambda t: t * t + (20 - t) ** 2
ck(maxmin(P7, 0, 20, 10)[0] == 100 and maxmin(Q7, 0, 20, 10)[1] == 200)
S_.append(("Problemas con funciones cuadráticas", [
 (1, r"Halla el máximo y el mínimo de $f(x)=x^2-4x+1$ en el intervalo $[-1,3]$ y en el intervalo $[3,5]$."
     + recorda(r"en un intervalo cerrado, el máximo y el mínimo de una parábola están en el vértice (si está dentro del intervalo) o en los extremos del intervalo. Calcúlalos todos y compara."),
     r'Vértice: $x=2$, $f(2)=-3$. En $[-1,3]$ (el vértice está dentro): $f(-1)=6$, $f(3)=-2$: máximo $\res{(-1,6)}$, mínimo $\res{(2,-3)}$. En $[3,5]$ (el vértice no está; la función es creciente): mínimo $\res{(3,-2)}$, máximo $\res{(5,6)}$.'
     + G(Plot(-2, 6, -4, 7, W=220).fn(F6).dot(2, -3, 'v').dot(-1, 6, 'b').dot(3, -2, 'b').dot(5, 6, 'b'), 3.6)),
 (2, r"Dos números suman 20. ¿Cuáles son si su producto es el mayor posible? ¿Y si la suma de sus cuadrados es la menor posible?",
     r'Si uno es $x$, el otro es $20-x$. Producto: $P(x)=x(20-x)=-x^2+20x$, vértice en $x=10$: $\res{10\text{ y }10}$, producto $100$. Cuadrados: $S(x)=x^2+(20-x)^2=2x^2-40x+400$, vértice en $x=10$: también $\res{10\text{ y }10}$, suma mínima $200$.'),
 (2, r"Una tienda vende un producto a $p$ euros y, a ese precio, vende $200-4p$ unidades al mes ($0\le p\le50$). Escribe la función de ingresos $I(p)$. ¿A qué precio son máximos los ingresos y cuánto valen? Si por motivos de competencia el precio debe estar entre 30 y 45~€, ¿qué precio conviene poner?",
     r'$\res{I(p)=p(200-4p)=200p-4p^2}$. Vértice: $p=\frac{-200}{-8}=25$: $\res{p=25\text{ €}}$, $I(25)=\res{2\,500\text{ €}}$. En $[30,45]$ el vértice no está e $I$ es decreciente: lo mejor es $\res{p=30\text{ €}}$, con $I(30)=2\,400$~€.'
     + G(Plot(-3, 53, -300, 2900, sx=5, sy=500, lx=10, ly=500, W=280).fn(I1, 0, 50).dot(25, 2500, 'v').dot(30, 2400, 'b').gd(30, 0, 30, 2400).gd(45, 0, 45, I1(45)), 4.6)),
 (2, r"Una empresa fabrica $x$ unidades de un artículo ($0\le x\le50$). Los ingresos son $I(x)=60x$ y los costes $C(x)=x^2+20x+300$ (en euros). Escribe la función de beneficios $B(x)=I(x)-C(x)$. ¿Cuántas unidades debe fabricar para obtener el beneficio máximo? ¿Entre cuántas unidades hay ganancias? Si solo puede fabricar 15 como máximo, ¿cuál es el mayor beneficio?",
     r'$\res{B(x)=-x^2+40x-300}$. Vértice: $\res{x=20}$ unidades, $B(20)=\res{100\text{ €}}$. $B(x)=0\Rightarrow x=10,\ x=30$: hay ganancias si $\res{10\lt x\lt30}$. En $[0,15]$, $B$ es creciente: máximo en $x=15$, $B(15)=\res{75\text{ €}}$.'),
 (2, r"El coste por unidad (en euros) de fabricar $x$ centenares de piezas es $c(x)=0{,}5x^2-20x+250$, con $0\le x\le40$. ¿Qué producción hace mínimo el coste por unidad? ¿Cuál es ese coste? ¿Y si la máquina solo puede hacer como mucho 1\,500 piezas?",
     r'Vértice: $x=\frac{20}{1}=20$: $\res{2\,000\text{ piezas}}$, $c(20)=\res{50\text{ €}}$. Con $x\le15$, $c$ es decreciente en $[0,15]$: mínimo en $x=15$, $c(15)=\res{62{,}50\text{ €}}$.'),
 (2, r"Con 60 m de valla queremos hacer un corral rectangular pegado a una pared (el lado de la pared no se valla). Si los dos lados perpendiculares a la pared miden $x$, escribe el área $A(x)$ y halla las dimensiones del corral de área máxima.",
     r'El lado paralelo mide $60-2x$: $\res{A(x)=x(60-2x)=60x-2x^2}$, $0\lt x\lt30$. Vértice: $x=15$: $\res{15\text{ m}\times30\text{ m}}$, área máxima $\res{450\text{ m}^2}$.'),
 (3, r"Un hotel tiene 40 habitaciones. Si cobra 80~€ por noche, las llena todas; por cada 5~€ que sube el precio, queda una habitación vacía. Si lo sube $n$ veces 5~€, escribe los ingresos $I(n)$. ¿Qué precio hace máximos los ingresos? ¿Cuántas habitaciones se ocupan?",
     r'Precio $80+5n$, habitaciones $40-n$: $\res{I(n)=(80+5n)(40-n)=-5n^2+120n+3\,200}$. Vértice: $n=12$: precio $\res{140\text{ €}}$, $\res{28}$ habitaciones, ingresos $\res{3\,920\text{ €}}$.'),
]))

assert all(CHK)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "función lineal, función afín, parábola, función cúbica, hipérbola, función radical, exponencial, logaritmo, funciones trigonométricas, funciones a trozos, valor absoluto, problemas de optimización, ingresos y costes"
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

def fix(t):
    """Fora dels dibuixos: l'apòstrof escrit \\' dins de cadenes r'' (en LaTeX seria un accent) i l'espai després
    de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = "Funciones elementales"
def build(sol):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 7: %s' % (t, TIT), capcalera='%s · Unidad 7: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-mi')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1batx-mi') + '{' + ('Soluciones de la ficha · Unidad 7' if sol else 'Ficha de ejercicios · Unidad 7') + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.8cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los intervalos se escriben como en los apuntes: $\left]a,b\right[$ abierto y $[a,b]$ cerrado. Puedes comprobar las gráficas, las traslaciones y los máximos y mínimos con las herramientas de los apuntes interactivos de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos y haz un dibujo siempre que te ayude. Escribe los intervalos como en los apuntes ($\left]a,b\right[$ abierto, $[a,b]$ cerrado). Las secciones siguen el orden de los apuntes y la última tiene problemas de máximos y mínimos con funciones cuadráticas.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't7-fitxa-solucions-es.tex' if sol else 't7-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'ejercicios;', len(CHK), 'comprobaciones')
