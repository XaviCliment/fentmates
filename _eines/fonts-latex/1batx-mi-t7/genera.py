# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (1r Batxillerat MI, Unitat 7: Funcions elementals)
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
S_.append(("Funcions lineals i afins", [
 (1, r"Troba l'equació de la recta que passa per $A(-2,1)$ i $B(4,4)$. És creixent o decreixent?",
     r'$m=\frac{4-1}{4+2}=\frac12$; \ $y=1+\frac12(x+2)\Rightarrow\res{y=\frac12x+2}$. \ $\res{\text{Creixent}}$ ($m\gt0$).'),
 (1, r"Troba l'equació de la recta de pendent $-3$ que passa per $(2,-1)$ i els seus punts de tall amb els eixos.",
     r'$y=-1-3(x-2)\Rightarrow\res{y=-3x+5}$. \ $OY$: $\res{(0,5)}$; \ $OX$: $\res{\left(\frac53,\,0\right)}$'),
 (1, r"Escriu l'equació de cadascuna d'aquestes rectes:" + tasks(3, [Gi(p, 3.4) for p in l7]),
     tasks(3, [R('y=2x-3'), R(r'y=-\frac13x+2'), R('y=-2')])),
 (2, r"Un taxi cobra $3{,}50$~€ de baixada de bandera i $1{,}20$~€ per quilòmetre. Escriu la funció que dona el preu en funció dels quilòmetres. Quant costa un viatge de 12 km? Quants quilòmetres has fet si has pagat 23~€?",
     r'$\res{f(x)=1{,}2x+3{,}5}$. \ $f(12)=\res{17{,}90\text{ €}}$. \ $1{,}2x+3{,}5=23\Rightarrow\res{x=16{,}25\text{ km}}$'),
 (1, r"Troba l'equació de la recta paral·lela a $y=3x-1$ que passa pel punt $(1,5)$.",
     r'Les rectes paral·leles tenen el mateix pendent, $m=3$: $y=5+3(x-1)\Rightarrow\res{y=3x+2}$'),
 (2, r"Un dipòsit té 200 L d'aigua i se'n buida a raó de 8 L per minut. Escriu la funció $V(t)$ que dona els litres que queden al cap de $t$ minuts. Quan es buida? Quin és el domini de la funció en aquest context?",
     r'$\res{V(t)=200-8t}$. \ $V(t)=0\Rightarrow\res{t=25\text{ min}}$. \ $D=\res{\cc{0}{25}}$ (decreixent; recorregut $[0,200]$).'),
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
# 3. Funcions racionals
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
 (2, r"Una hipèrbola de la forma $y=\dfrac{k}{x-a}+b$ té les asímptotes $x=2$ i $y=1$ i passa pel punt $(3,4)$. Troba'n l'expressió i el punt de tall amb l'eix $OY$.",
     r'$a=2$, $b=1$; \ $4=\frac{k}{3-2}+1\Rightarrow k=3$: \ $\res{y=\dfrac{3}{x-2}+1}$. \ $OY$: $y=-\frac32+1$: $\res{\left(0,\,-\frac12\right)}$'),
]))
ck(3 / (3 - 2) + 1 == 4 and 3 / (0 - 2) + 1 == -0.5)

# =====================================================================
# 4. Funcions radicals
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
 (2, r"Donada $f(x)=\sqrt{2x-4}+1$, indica on comença, el domini i el recorregut. Per a quin valor de $x$ val $f(x)=3$?",
     r'$2x-4=0\Rightarrow x=2$: comença en $\res{(2,1)}$; $D=\res{\co{2}{+\infty}}$, $R=\res{\co{1}{+\infty}}$. \ $\sqrt{2x-4}=2\Rightarrow 2x-4=4\Rightarrow\res{x=4}$'),
]))
cknum(math.sqrt(2 * 4 - 4) + 1, 3)
cknum(sq(3 + 1) - 2, 0)

# =====================================================================
# 5. Exponencials i logarítmiques
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
 (2, r"Les gràfiques són translacions de $y=2^x$ i de $y=\log_2x$. Escriu-ne les expressions." + tasks(2, [Gi(Plot(-5, 4, -4, 5, W=190, lx=2, ly=2).fn(lambda t: 2 ** (t + 1) - 3).hl(-3).dot(-1, -2, 'b').dot(1, 1, 'b'), 3.3),
                                                                                                    Gi(Plot(-1, 8, -3, 4, W=190, lx=2, ly=2).fn(lambda t: lg(2, t - 1) + 1, 1.005, 8).vl(1).dot(2, 1, 'b').dot(3, 2, 'b'), 3.3)]),
     tasks(2, [r'AH $y=-3$, punt de referència $(-1,-2)$: $\res{y=2^{x+1}-3}$', r'AV $x=1$, punt de referència $(2,1)$: $\res{y=\log_2(x-1)+1}$'])),
]))
ck(2 ** (1 + 1) - 3 == 1 and lg(2, 3 - 1) + 1 == 2)

# =====================================================================
# 6. Trigonomètriques
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
 (2, r"Dibuixa en $[0,2\pi]$ les funcions $y=\sin x+1$ i $y=2\cos x$ i indica'n el recorregut, els màxims, els mínims i els talls amb l'eix $OX$.",
     r'$y=\sin x+1$: $R=\res{\cc{0}{2}}$; màxim $\res{\left(\frac\pi2,2\right)}$, mínim $\res{\left(\frac{3\pi}2,0\right)}$, que és l\'únic punt de tall amb $OX$. \ $y=2\cos x$: $R=\res{\cc{-2}{2}}$; màxims $\res{(0,2),\ (2\pi,2)}$, mínim $\res{(\pi,-2)}$; talls $\res{\left(\frac\pi2,0\right),\ \left(\frac{3\pi}2,0\right)}$.'
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
S_.append(("Funcions a trossos i valor absolut", [
 (1, r"Representa $f(x)=\begin{cases}2x+4, & \text{si } x\lt-1\\ x^2-1, & \text{si } -1\le x\lt2\\ 3, & \text{si } x\geq2\end{cases}$, calcula $f(-3)$, $f(0)$, $f(2)$ i $f(5)$, i estudia'n la continuïtat i el recorregut.",
     r'$f(-3)=\res{-2}$, $f(0)=\res{-1}$, $f(2)=\res{3}$, $f(5)=\res{3}$. En $x=-1$: $\res{\text{salt finit}}$ (de 2 a 0); en $x=2$: $\res{\text{contínua}}$ (els dos costats arriben a 3). $R=\res{\oc{-\infty}{3}}$.' + G(g13, 4.2)),
 (2, r"Escriu l'expressió de la funció a trossos representada:" + G(gq, 4.2),
     r'$\res{f(x)=\begin{cases}-x, & \text{si } x\lt0\\ x^2, & \text{si } 0\le x\le2\\ 1, & \text{si } x\gt2\end{cases}}$'),
 (1, r"Escriu a trossos i representa:" + tasks(4, ['$y=%s$' % a_[0] for a_ in ab]) + recorda(r"troba on s'anul·la l'expressió de dins, estudia'n el signe i canvia-li el signe on és negativa."),
     tasks(2, ['$y=%s$' % a_[1] + (G(Plot(-2, 6, -1, 6, W=170).fn(a_[2]).fn(lambda t: t * t - 4 * t, col='v', dash=True), 2.8) if i == 1 else G(Plot(-3, 4, -1, 6, W=170).fn(a_[2]).fn(lambda t: t * t - t - 2, col='v', dash=True), 2.8) if i == 2 else '') for i, a_ in enumerate(ab)])),
 (2, r"Un aparcament cobra 2~€ per la primera hora (o fracció) i $1{,}50$~€ per cada hora de més. Escriu la funció a trossos que dona el preu segons les hores $x$ (amb $x\gt0$, comptant les hores de manera contínua), calcula el preu de 3 hores i quantes hores has estat si pagues 8~€. És contínua en $x=1$?",
     r'$\res{f(x)=\begin{cases}2, & \text{si } 0\lt x\le1\\ 2+1{,}5(x-1), & \text{si } x\gt1\end{cases}}$. \ $f(3)=\res{5\text{ €}}$. \ $2+1{,}5(x-1)=8\Rightarrow\res{x=5\text{ h}}$. \ $\res{\text{Sí}}$: els dos trossos valen 2.'),
 (2, r"Resol gràficament l'equació $|x-1|=3$: dibuixa $y=|x-1|$ i la recta $y=3$, i troba on es tallen.",
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
S_.append(("Problemes amb funcions quadràtiques", [
 (1, r"Troba el màxim i el mínim de $f(x)=x^2-4x+1$ en l'interval $[-1,3]$ i en l'interval $[3,5]$."
     + recorda(r"en un interval tancat, el màxim i el mínim d'una paràbola són al vèrtex (si està dins de l'interval) o en els extrems de l'interval. Calcula'ls tots i compara."),
     r'Vèrtex: $x=2$, $f(2)=-3$. En $[-1,3]$ (el vèrtex hi és): $f(-1)=6$, $f(3)=-2$: màxim $\res{(-1,6)}$, mínim $\res{(2,-3)}$. En $[3,5]$ (el vèrtex no hi és; la funció hi és creixent): mínim $\res{(3,-2)}$, màxim $\res{(5,6)}$.'
     + G(Plot(-2, 6, -4, 7, W=220).fn(F6).dot(2, -3, 'v').dot(-1, 6, 'b').dot(3, -2, 'b').dot(5, 6, 'b'), 3.6)),
 (2, r"Dos nombres sumen 20. Quins són si el seu producte és el més gran possible? I si la suma dels seus quadrats és la més petita possible?",
     r'Si un és $x$, l\'altre és $20-x$. Producte: $P(x)=x(20-x)=-x^2+20x$, vèrtex en $x=10$: $\res{10\text{ i }10}$, producte $100$. Quadrats: $S(x)=x^2+(20-x)^2=2x^2-40x+400$, vèrtex en $x=10$: també $\res{10\text{ i }10}$, suma mínima $200$.'),
 (2, r"Una botiga ven un producte a $p$ euros i, a aquest preu, en ven $200-4p$ unitats al mes ($0\le p\le50$). Escriu la funció d'ingressos $I(p)$. A quin preu són màxims els ingressos i quant valen? Si per motius de competència el preu ha d'estar entre 30 i 45~€, quin preu convé posar?",
     r'$\res{I(p)=p(200-4p)=200p-4p^2}$. Vèrtex: $p=\frac{-200}{-8}=25$: $\res{p=25\text{ €}}$, $I(25)=\res{2\,500\text{ €}}$. En $[30,45]$ el vèrtex no hi és i $I$ hi és decreixent: el millor és $\res{p=30\text{ €}}$, amb $I(30)=2\,400$~€.'
     + G(Plot(-3, 53, -300, 2900, sx=5, sy=500, lx=10, ly=500, W=280).fn(I1, 0, 50).dot(25, 2500, 'v').dot(30, 2400, 'b').gd(30, 0, 30, 2400).gd(45, 0, 45, I1(45)), 4.6)),
 (2, r"Una empresa fabrica $x$ unitats d'un article ($0\le x\le50$). Els ingressos són $I(x)=60x$ i els costos $C(x)=x^2+20x+300$ (en euros). Escriu la funció de beneficis $B(x)=I(x)-C(x)$. Quantes unitats ha de fabricar per a obtindre el benefici màxim? Entre quantes unitats hi ha guanys? Si només pot fabricar-ne 15 com a màxim, quin és el benefici més gran?",
     r'$\res{B(x)=-x^2+40x-300}$. Vèrtex: $\res{x=20}$ unitats, $B(20)=\res{100\text{ €}}$. $B(x)=0\Rightarrow x=10,\ x=30$: hi ha guanys si $\res{10\lt x\lt30}$. En $[0,15]$, $B$ és creixent: màxim en $x=15$, $B(15)=\res{75\text{ €}}$.'),
 (2, r"El cost per unitat (en euros) de fabricar $x$ centenars de peces és $c(x)=0{,}5x^2-20x+250$, amb $0\le x\le40$. Quina producció fa mínim el cost per unitat? Quin és aquest cost? I si la màquina només pot fer com a molt 1\,500 peces?",
     r'Vèrtex: $x=\frac{20}{1}=20$: $\res{2\,000\text{ peces}}$, $c(20)=\res{50\text{ €}}$. Amb $x\le15$, $c$ és decreixent en $[0,15]$: mínim en $x=15$, $c(15)=\res{62{,}50\text{ €}}$.'),
 (2, r"Amb 60 m de tanca volem fer un corral rectangular arrimat a una paret (el costat de la paret no es tanca). Si els dos costats perpendiculars a la paret mesuren $x$, escriu l'àrea $A(x)$ i troba les dimensions del corral d'àrea màxima.",
     r'El costat paral·lel mesura $60-2x$: $\res{A(x)=x(60-2x)=60x-2x^2}$, $0\lt x\lt30$. Vèrtex: $x=15$: $\res{15\text{ m}\times30\text{ m}}$, àrea màxima $\res{450\text{ m}^2}$.'),
 (3, r"Un hotel té 40 habitacions. Si cobra 80~€ per nit, les ompli totes; per cada 5~€ que puja el preu, queda una habitació buida. Si el puja $n$ vegades 5~€, escriu els ingressos $I(n)$. Quin preu fa màxims els ingressos? Quantes habitacions s'ocupen?",
     r'Preu $80+5n$, habitacions $40-n$: $\res{I(n)=(80+5n)(40-n)=-5n^2+120n+3\,200}$. Vèrtex: $n=12$: preu $\res{140\text{ €}}$, $\res{28}$ habitacions, ingressos $\res{3\,920\text{ €}}$.'),
]))

assert all(CHK)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={funció lineal, funció afí, paràbola, funció cúbica, hipèrbola, funció radical, exponencial, logaritme, funcions trigonomètriques, funcions a trossos, valor absolut, problemes d'optimització, ingressos i costos}"
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

TIT = "Funcions elementals"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 7: %s. 1r de Batxillerat MI}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 7: %s · 1r Batxillerat MI" % (t, TIT))
    assert 'elementals · 1r' in p and 'unitat 7: Funcions' in p
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
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Els intervals s'escriuen com als apunts: $\left]a,b\right[$ obert i $[a,b]$ tancat. Pots comprovar les gràfiques, les translacions i els màxims i mínims amb els ginys dels apunts interactius de la unitat."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos i fes un dibuix sempre que t'ajude. Escriu els intervals com als apunts ($\left]a,b\right[$ obert, $[a,b]$ tancat). Les seccions segueixen l'ordre dels apunts i la darrera té problemes de màxims i mínims amb funcions quadràtiques.") + r'''
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
