# Versió en castellà de genera.py: escriu els -es.tex. Original: genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (1r Batxillerat MI, Unitat 8: Límits i continuïtat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# La fitxa segueix els apartats dels apunts (8.1-8.10) i inclou els exercicis proposats als apunts del departament
# (límits de les famílies de funcions, quocients, ∞−∞, 1^∞, límits en un punt, tipus de discontinuïtat, el paràmetre m i
# les branques infinites), a més d'exercicis nous.
# Comprovacions: C() estima numèricament cada límit de les solucions (també els laterals), NX() comprova que una funció no està
# definida cap a un infinit, EQ() comprova identitats (divisions, factoritzacions) en uns quants valors i PAR() que els
# límits laterals coincideixen amb el valor del paràmetre trobat.
# Ús: python3 genera.py && pdflatex t8-fitxa-exercicis.tex (dues vegades) && pdflatex t8-fitxa-solucions.tex (dues vegades)
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def L(a, e): return r'\displaystyle\lim_{x\to %s}%s' % (a, e)
def pw(*rows, name='f(x)'):
    return name + r'=\begin{cases}' + r'\\[3pt]'.join(r'%s&\text{si }%s' % r for r in rows) + r'\end{cases}'
def m(s): return '$' + s + '$'
def dm(s): return r'\[' + s + r'\]'
PI, MI = r'+\infty', r'-\infty'

# ---------- comprovacions numèriques ----------
I, E, sq, ex, ln = math.inf, math.e, math.sqrt, math.exp, math.log
NCHK = [0]
def lim(f, a, side=1):
    """Estimació del límit: a pot ser ±inf; es queda amb el valor més estable."""
    if math.isinf(a): xs = [math.copysign(10 ** k, a) for k in (3, 4, 5, 6)]
    else: xs = [a + side * 10 ** -k for k in (4, 5, 6, 7)]
    v = []
    for t in xs:
        try: v.append(f(t))
        except (OverflowError, ZeroDivisionError, ValueError): pass
    assert len(v) >= 2, (a, side, v)
    if len(v) >= 3 and abs(v[-1] - v[-2]) <= abs(v[-2] - v[-3]): return v[-1]  # convergeix: l'últim és el millor
    return v[-1] if abs(v[-1]) > 1e7 or abs(v[-1] - v[-2]) < 1e-3 * (1 + abs(v[-1])) else v[-2]
def C(f, a, want, side=None, tol=2e-3):
    """comprova lim f quan x→a (si side és None i a és finit, els dos laterals)"""
    if math.isinf(a) and math.isinf(want):  # creixement lent (arrels, logaritmes): cada vegada més gran i més enllà de 20
        try: vs = [math.copysign(1, want) * f(math.copysign(10.0 ** k, a)) for k in (6, 9, 12)]
        except OverflowError: vs = [math.copysign(1, want) * f(math.copysign(10.0 ** k, a)) for k in (2, 2.3, 2.6)]
        assert vs[0] < vs[1] < vs[2] and vs[2] > 20, (a, want, vs)
        NCHK[0] += 1
        return
    for s in ((1, -1) if side is None and not math.isinf(a) else (side or 1,)):
        r = lim(f, a, s)
        good = (r > 1e5 if want > 0 else r < -1e5) if math.isinf(want) else abs(r - want) <= tol * (1 + abs(want))
        assert good, (a, s, want, r)
        NCHK[0] += 1
def NX(f, a):
    """f no està definida per a valors de x prop de a (±inf)"""
    for t in (math.copysign(10 ** k, a) for k in (2, 3, 4)):
        try: f(t); raise AssertionError(('definida', a, t))
        except (ValueError, ZeroDivisionError): pass
    NCHK[0] += 1
def EQ(f, g):
    for t in (-3.7, -1.3, 0.6, 2.9, 5.3):
        try: a, b = f(t), g(t)
        except ZeroDivisionError: continue
        assert abs(a - b) < 1e-9 * (1 + abs(a)), (t, a, b)
    NCHK[0] += 1
def PAR(*pairs):
    for l, r in pairs: assert abs(l - r) < 1e-12, (l, r)
    NCHK[0] += 1

# ---------- gràfiques (TikZ) ----------
def tzg(x0, x1, y0, y1, body, sc=0.42):
    g = r'\draw[muted!30,very thin] (%s,%s) grid (%s,%s);' % (x0, y0, x1, y1)
    g += r'\draw[-latex,thick] (%s,0)--(%s,0);\draw[-latex,thick] (0,%s)--(0,%s);' % (x0, x1 + 0.4, y0, y1 + 0.4)
    return r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]\begin{scope}%s\clip (%s,%s) rectangle (%s,%s);%s\end{scope}\end{tikzpicture}' % (sc, g, x0, y0, x1, y1, body)
CV = r'\draw[accent,line width=1.5pt,smooth,samples=90,domain=%s] plot (\x,{%s});'
def dot(x, y, o=False): return (r'\filldraw[fill=white,draw=accent,line width=1.1pt] (%s,%s) circle (0.17);' if o else r'\fill[accent] (%s,%s) circle (0.17);') % (x, y)
def tk(x, y, t, pos='below'): return r'\node[%s,font=\scriptsize] at (%s,%s) {$%s$};' % (pos, x, y, t)
def hl(y, x0, x1): return r'\draw[teal,dashed,thick] (%s,%s)--(%s,%s);' % (x0, y, x1, y)
def vl(x, y0, y1): return r'\draw[teal,dashed,thick] (%s,%s)--(%s,%s);' % (x, y0, x, y1)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Límits a l'infinit
GA = tzg(-5, 5, -4, 4, CV % ('-3.6:3.6', '\\x*\\x*\\x/8-\\x'), sc=0.3)
GB = tzg(-5, 5, -4, 4, CV % ('-5:2.5', '2^\\x-2') + hl(-2, -5, 5), sc=0.3)
GC = tzg(-5, 5, -4, 4, CV % ('-5:5', '2*\\x*\\x/(\\x*\\x+1)') + hl(2, -5, 5), sc=0.3)
GD = tzg(-5, 5, -4, 4, CV % ('-5:5', '1.5*sin(2*\\x r)'), sc=0.3)
C(lambda t: t**3 / 8 - t, I, I); C(lambda t: t**3 / 8 - t, -I, -I); C(lambda t: 2**t - 2, 900, I); C(lambda t: 2**t - 2, -I, -2)
C(lambda t: 2 * t * t / (t * t + 1), I, 2); C(lambda t: 2 * t * t / (t * t + 1), -I, 2)

FAM = [  # (f en LaTeX, lim −∞, lim +∞) — exercici dels apunts del departament
 (r'-2x^3+7x^2', PI, MI), (r'3x^4-7x', PI, PI), (r'10^x', '0', PI), (r'\sqrt{5x-8}', r'\nexists', PI),
 (r'\sqrt{-2x^2+1}', r'\nexists', r'\nexists'), (r'-5^x', '0', MI), (r'\sqrt{3-x}', PI, r'\nexists'),
 (r'\dfrac{x^2+3}{-x^3}', '0', '0'), (r'\dfrac{-x^3}{x^2+3}', PI, MI), (r'\dfrac{5x^3-10}{3x^3+10x^2}', r'\frac53', r'\frac53')]
C(lambda t: -2 * t**3 + 7 * t * t, -I, I); C(lambda t: -2 * t**3 + 7 * t * t, I, -I); C(lambda t: 3 * t**4 - 7 * t, -I, I); C(lambda t: 3 * t**4 - 7 * t, I, I)
C(lambda t: 10**t, -I, 0); C(lambda t: 10**t, 300, I); NX(lambda t: sq(5 * t - 8), -I); C(lambda t: sq(5 * t - 8), I, I)
NX(lambda t: sq(-2 * t * t + 1), -I); NX(lambda t: sq(-2 * t * t + 1), I); C(lambda t: -5**t, -I, 0); C(lambda t: -5**t, 300, -I)
C(lambda t: sq(3 - t), -I, I); NX(lambda t: sq(3 - t), I); C(lambda t: (t * t + 3) / -t**3, -I, 0); C(lambda t: (t * t + 3) / -t**3, I, 0)
C(lambda t: -t**3 / (t * t + 3), -I, I); C(lambda t: -t**3 / (t * t + 3), I, -I); C(lambda t: (5 * t**3 - 10) / (3 * t**3 + 10 * t * t), -I, 5 / 3); C(lambda t: (5 * t**3 - 10) / (3 * t**3 + 10 * t * t), I, 5 / 3)

C(lambda t: (t * t - 5 * t + 3) / (3 * t - 5), I, I); C(lambda t: (t * t + 3) / t**3, I, 0); C(lambda t: (3 * t * t - 5 * t + 1) / (2 * t * t - 6), I, 1.5)
C(lambda t: (4 * t**3 - t) / (2 - t * t), -I, I); C(lambda t: (1 - 6 * t) / (3 * t + 2), -I, -2); C(lambda t: (2 * t * t - 1) / (5 - t), -I, I)
C(lambda t: (1 / 3)**t, I, 0); C(lambda t: 3**t + 1, -I, 1); C(lambda t: 0.4**t, -700, I); C(lambda t: sq(4 * t * t + 1) / (t + 3), I, 2)
C(lambda t: sq(t * t + 1) / (2 * t), -I, -0.5); C(lambda t: ex(-t) + 2, I, 2)

S_.append(("Límites en el infinito", [
 (1, r"Observa las gráficas y escribe, para cada una, el límite cuando $x\to+\infty$ y cuando $x\to-\infty$. Las rectas discontinuas son asíntotas." + tasks(4, ['\\par' + g for g in (GA, GB, GC, GD)])
     + recorda(r"Para $x\to+\infty$ mira el \textbf{final derecho} de la gráfica y para $x\to-\infty$, el \textbf{final izquierdo}. Si la gráfica oscila sin acercarse a ningún valor, el límite no existe."),
     tasks(2, [r'$\displaystyle\lim_{x\to+\infty}=\res{+\infty}$, \ $\displaystyle\lim_{x\to-\infty}=\res{-\infty}$', r'$\displaystyle\lim_{x\to+\infty}=\res{+\infty}$, \ $\displaystyle\lim_{x\to-\infty}=\res{-2}$',
               r'$\displaystyle\lim_{x\to\pm\infty}=\res{2}$ \ (asíntota $y=2$)', r'Oscila: \ $\res{\nexists}$ ninguno de los dos límites'])),
 (2, r"Calcula, para cada función, $\displaystyle\lim_{x\to-\infty}f(x)$ y $\displaystyle\lim_{x\to+\infty}f(x)$. Fíjate bien en el dominio de las raíces." + tasks(2, ['$f(x)=%s$' % f for f, _, _ in FAM])
     + recorda(r"Potencias, exponenciales de base mayor que 1, raíces y logaritmos tienden a $+\infty$ cuando $x\to+\infty$. Un polinomio se comporta como su término de mayor grado. Si la función no está definida hacia un infinito, el límite no existe."),
     tasks(2, ['$%s$: \\ $\\res{%s}$ \\ y \\ $\\res{%s}$' % (f, a, b) for f, a, b in FAM])
     + r"\par\small (En la e), el dominio es $\left[-\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right]$; en la f), $-5^x=-(5^x)$.)"),
 (1, r"Calcula los límites siguientes comparando los grados del numerador y del denominador:" + tasks(3, [m(L(PI, r'\dfrac{x^2-5x+3}{3x-5}')), m(L(PI, r'\dfrac{x^2+3}{x^3}')), m(L(PI, r'\dfrac{3x^2-5x+1}{2x^2-6}')),
     m(L(MI, r'\dfrac{4x^3-x}{2-x^2}')), m(L(MI, r'\dfrac{1-6x}{3x+2}')), m(L(MI, r'\dfrac{2x^2-1}{5-x}'))])
     + recorda(r"$\displaystyle\lim_{x\to\pm\infty}\frac{P(x)}{Q(x)}=\lim_{x\to\pm\infty}\frac{a_nx^n}{b_mx^m}$: \ si $n>m$, $\pm\infty$ (hay que mirar el signo); \ si $n=m$, $\frac{a_n}{b_m}$; \ si $n<m$, $0$."),
     tasks(3, [r'$\lim\frac{x^2}{3x}=\lim\frac x3=\res{+\infty}$', r'$\lim\frac{x^2}{x^3}=\res{0}$', r'Mismo grado: $\res{\frac32}$', r'$\lim\frac{4x^3}{-x^2}=\lim(-4x)=\res{+\infty}$', r'$\frac{-6}{3}=\res{-2}$', r'$\lim\frac{2x^2}{-x}=\lim(-2x)=\res{+\infty}$'])),
 (2, r"Calcula los límites siguientes con exponenciales y raíces:" + tasks(3, [m(L(PI, r'\left(\tfrac13\right)^x')), m(L(MI, r'\left(3^x+1\right)')), m(L(MI, r'0{,}4^x')),
     m(L(PI, r'\dfrac{\sqrt{4x^2+1}}{x+3}')), m(L(MI, r'\dfrac{\sqrt{x^2+1}}{2x}')), m(L(PI, r'\left(e^{-x}+2\right)'))]),
     tasks(3, [r'$\left(\tfrac13\right)^{+\infty}=\res{0}$', r'$3^{-\infty}+1=\res{1}$', r'$0{,}4^{-\infty}=\res{+\infty}$', r'$\lim\frac{2x}{x}=\res{2}$', r'$\sqrt{x^2}=|x|=-x$: \ $\lim\frac{-x}{2x}=\res{-\frac12}$', r'$e^{-\infty}+2=\res{2}$'])),
]))

# =====================================================================
# 2. Comparació d'infinits
C(lambda t: t**4 / 2**t, 900, 0); C(lambda t: 3**t / t**20, 600, I); C(lambda t: ln(t) / t, I, 0); C(lambda t: t**3 - ex(t), 600, -I)
C(lambda t: (2**t + t * t) / 2**(t + 1), 900, 0.5); C(lambda t: sq(t) - ln(t), I, I); C(lambda t: t - 2**t, 900, -I)
C(lambda t: t * t - sq(t**5 + 3), I, -I); C(lambda t: 3**t - sq(t**3 - 2), 600, I); C(lambda t: (5**t + t) / 4**t, 400, I)
S_.append(("Comparación de infinitos", [
 (1, r"Ordena estos infinitos de menor a mayor orden cuando $x\to+\infty$: \quad $x^2,\ \ 3^x,\ \ \ln x,\ \ x^5,\ \ \sqrt x,\ \ 1{,}1^x$."
     + recorda(r"Cuando $x\to+\infty$: \ logaritmos $\ll$ potencias $\ll$ exponenciales (de base mayor que 1). Entre potencias gana el exponente mayor y entre exponenciales, la base mayor."),
     r"$\res{\ln x\ll\sqrt x\ll x^2\ll x^5\ll1{,}1^x\ll3^x}$"),
 (2, r"Calcula los límites siguientes comparando infinitos:" + tasks(3, [m(L(PI, r'\dfrac{x^4}{2^x}')), m(L(PI, r'\dfrac{3^x}{x^{20}}')), m(L(PI, r'\dfrac{\ln x}{x}')), m(L(PI, r'\left(x^3-e^x\right)')),
     m(L(PI, r'\dfrac{2^x+x^2}{2^{x+1}}')), m(L(PI, r'\left(\sqrt x-\ln x\right)')), m(L(PI, r'\left(x-2^x\right)')), m(L(PI, r'\dfrac{5^x+x}{4^x}'))]),
     tasks(3, [r'$\res{0}$', r'$\res{+\infty}$', r'$\res{0}$', r'$\res{-\infty}$', r'$\lim\frac{2^x}{2\cdot2^x}=\res{\frac12}$', r'$\res{+\infty}$', r'$\res{-\infty}$', r'$\lim\left(\frac54\right)^x=\res{+\infty}$'])),
 (2, r"Indeterminación $\infty-\infty$ por comparación de infinitos:" + tasks(2, [m(L(PI, r'\left(x^2-\sqrt{x^5+3}\right)')), m(L(PI, r'\left(3^x-\sqrt{x^3-2}\right)'))]),
     tasks(2, [r'$\sqrt{x^5}=x^{5/2}$ y $\frac52>2$: \ $\res{-\infty}$', r'$3^x$ tiene mayor orden: \ $\res{+\infty}$'])),
]))

# =====================================================================
# 3. Indeterminacions a l'infinit
C(lambda t: (sq(t * t + 1) + 2 * t) / (3 * t - 1), I, 1); C(lambda t: (sq(4 * t**4 + t) - t) / (t * t + 5), I, 2); C(lambda t: (3 * t + sq(t)) / (t - sq(t)), I, 3, tol=5e-3)
C(lambda t: sq(4 * t**3 + t - 2) / (8 * t * t - 7), I, 0)
C(lambda t: (2 * t * t - 5 * t) / (t + 3) - 2 * t, I, -11); EQ(lambda t: (2 * t * t - 5 * t) / (t + 3) - 2 * t, lambda t: -11 * t / (t + 3))
C(lambda t: t * t / (t - 2) - t * t / (t + 2), I, 4); EQ(lambda t: t * t / (t - 2) - t * t / (t + 2), lambda t: 4 * t * t / (t * t - 4))
C(lambda t: t**3 / (t * t - 1) - t, I, 0); C(lambda t: (t * t + 1) / t + (5 * t - t * t) / (3 * t - 1), I, I)
EQ(lambda t: (t * t + 1) / t + (5 * t - t * t) / (3 * t - 1), lambda t: (2 * t**3 + 4 * t * t + 3 * t - 1) / (3 * t * t - t))
C(lambda t: t - sq(t * t - 1), I, 0); EQ(lambda t: sq(t + 2) - sq(t - 2) if t > 2 else 0, lambda t: 4 / (sq(t + 2) + sq(t - 2)) if t > 2 else 0); assert abs(4 / (sq(1e12 + 2) + sq(1e12 - 2))) < 1e-5; NCHK[0] += 1; C(lambda t: sq(t * t + 6 * t) - t, I, 3)
C(lambda t: sq(t * t - 2) - sq(t * t + t), I, -0.5); C(lambda t: 2 * t - sq(4 * t * t - 3 * t), I, 0.75)
C(lambda t: (t / (t + 2))**(2 * t + 1), I, E**-4); C(lambda t: ((2 * t - 2) / (2 * t + 1))**(3 * t * t), I, 0); C(lambda t: (1 + 3 / t)**(2 * t), I, E**6)
C(lambda t: ((t + 1) / (t - 2))**t, I, E**3); C(lambda t: ((t * t + 1) / (t * t - 3))**(t * t), 1e3, E**4); C(lambda t: ((3 * t + 1) / (t + 2))**t, 600, I)
C(lambda t: (12 * t + 3000) / t, I, 12); C(lambda t: 8 * t / (t * t + 4), I, 0); C(lambda t: (500 * t + 300) / (t + 1), I, 500)
S_.append(("Indeterminaciones en el infinito", [
 (2, r"Indeterminación $\frac{\infty}{\infty}$ con raíces:" + tasks(2, [m(L(PI, r'\dfrac{\sqrt{x^2+1}+2x}{3x-1}')), m(L(PI, r'\dfrac{\sqrt{4x^4+x}-x}{x^2+5}')), m(L(PI, r'\dfrac{3x+\sqrt x}{x-\sqrt x}')), m(L(PI, r'\dfrac{\sqrt{4x^3+x-2}}{8x^2-7}'))])
     + recorda(r"Nos quedamos con el término de mayor grado de cada parte: \ $\sqrt{x^2+1}\approx x$ (si $x>0$), \ $\sqrt{4x^3}=2x^{3/2}$."),
     tasks(2, [r'$\lim\frac{x+2x}{3x}=\res{1}$', r'$\lim\frac{2x^2}{x^2}=\res{2}$', r'$\lim\frac{3x}{x}=\res{3}$', r'$\lim\frac{2x^{3/2}}{8x^2}=\lim\frac{1}{4\sqrt x}=\res{0}$'])),
 (2, r"Indeterminación $\infty-\infty$ con fracciones:" + tasks(2, [m(L(PI, r'\left(\dfrac{2x^2-5x}{x+3}-2x\right)')), m(L(PI, r'\left(\dfrac{x^2}{x-2}-\dfrac{x^2}{x+2}\right)')), m(L(PI, r'\left(\dfrac{x^3}{x^2-1}-x\right)')), m(L(PI, r'\left(\dfrac{x^2+1}{x}+\dfrac{5x-x^2}{3x-1}\right)'))])
     + recorda(r"Si la indeterminación $\infty-\infty$ viene de una suma o resta de fracciones, \textbf{hacemos la operación} con denominador común y calculamos el límite de la fracción que resulta."),
     tasks(1, [r'$\dfrac{2x^2-5x-2x(x+3)}{x+3}=\dfrac{-11x}{x+3}\to\res{-11}$', r'$\dfrac{x^2(x+2)-x^2(x-2)}{x^2-4}=\dfrac{4x^2}{x^2-4}\to\res{4}$', r'$\dfrac{x^3-x(x^2-1)}{x^2-1}=\dfrac{x}{x^2-1}\to\res{0}$',
               r'$\dfrac{(x^2+1)(3x-1)+x(5x-x^2)}{x(3x-1)}=\dfrac{2x^3+4x^2+3x-1}{3x^2-x}\to\lim\dfrac{2x}{3}=\res{+\infty}$'])),
 (2, r"Indeterminación $\infty-\infty$ con raíces:" + tasks(3, [m(L(PI, r'\left(x-\sqrt{x^2-1}\right)')), m(L(PI, r'\left(\sqrt{x+2}-\sqrt{x-2}\right)')), m(L(PI, r'\left(\sqrt{x^2+6x}-x\right)')), m(L(PI, r'\left(\sqrt{x^2-2}-\sqrt{x^2+x}\right)')), m(L(PI, r'\left(2x-\sqrt{4x^2-3x}\right)'))])
     + recorda(r"Multiplicamos y dividimos por el \textbf{conjugado}: $(A-B)(A+B)=A^2-B^2$ hace desaparecer las raíces del numerador."),
     tasks(1, [r'$\dfrac{x^2-(x^2-1)}{x+\sqrt{x^2-1}}=\dfrac{1}{x+\sqrt{x^2-1}}\to\res{0}$', r'$\dfrac{(x+2)-(x-2)}{\sqrt{x+2}+\sqrt{x-2}}=\dfrac{4}{\sqrt{x+2}+\sqrt{x-2}}\to\res{0}$', r'$\dfrac{6x}{\sqrt{x^2+6x}+x}\to\dfrac{6x}{2x}=\res{3}$',
               r'$\dfrac{-2-x}{\sqrt{x^2-2}+\sqrt{x^2+x}}\to\dfrac{-x}{2x}=\res{-\frac12}$', r'$\dfrac{4x^2-(4x^2-3x)}{2x+\sqrt{4x^2-3x}}=\dfrac{3x}{2x+\sqrt{4x^2-3x}}\to\dfrac{3x}{4x}=\res{\frac34}$'])),
 (2, r"Indeterminación $1^{\infty}$:" + tasks(3, [m(L(PI, r'\left(\dfrac{x}{x+2}\right)^{2x+1}')), m(L(PI, r'\left(\dfrac{2x-2}{2x+1}\right)^{3x^2}')), m(L(PI, r'\left(1+\dfrac3x\right)^{2x}')),
     m(L(PI, r'\left(\dfrac{x+1}{x-2}\right)^{x}')), m(L(PI, r'\left(\dfrac{x^2+1}{x^2-3}\right)^{x^2}')), m(L(PI, r'\left(\dfrac{3x+1}{x+2}\right)^{x}'))])
     + recorda(r"Si $\lim f(x)=1$ y $\lim g(x)=\pm\infty$: \ $\lim f(x)^{g(x)}=e^{\lim\,(f(x)-1)\cdot g(x)}$. Si la base no tiende a 1, no hay indeterminación."),
     tasks(2, [r'$\frac{x}{x+2}-1=\frac{-2}{x+2}$; \ $\lim\frac{-2(2x+1)}{x+2}=-4$: \ $\res{e^{-4}=\frac{1}{e^4}}$', r'$\frac{-3}{2x+1}\cdot3x^2=\frac{-9x^2}{2x+1}\to-\infty$: \ $e^{-\infty}=\res{0}$', r'$e^{\lim\frac3x\cdot2x}=\res{e^6}$',
               r'$\frac{3}{x-2}\cdot x\to3$: \ $\res{e^3}$', r'$\frac{4}{x^2-3}\cdot x^2\to4$: \ $\res{e^4}$', r'La base tiende a $3$: \ $3^{+\infty}=\res{+\infty}$ (no es $1^\infty$)'])),
 (2, r"Problemas. Calcula el límite que responde a cada pregunta:" + tasks(1, [r"El coste medio (en euros) de fabricar $x$ unidades de un producto es $C(x)=\dfrac{12x+3\,000}{x}$. ¿A qué valor se acerca el coste por unidad si se fabrican muchísimas?",
     r"La concentración de un medicamento en sangre $t$ horas después de tomarlo es $c(t)=\dfrac{8t}{t^2+4}$ (mg/l). ¿Qué pasa con la concentración a muy largo plazo?",
     r"Una población de conejos evoluciona según $P(t)=\dfrac{500t+300}{t+1}$, con $t$ en meses. ¿Cuál es la población inicial? ¿Tiene algún límite el número de conejos?"]),
     tasks(1, [r"$\displaystyle\lim_{x\to+\infty}\frac{12x+3\,000}{x}=12$: el coste por unidad se acerca a \rest{12 €}.", r"$\displaystyle\lim_{t\to+\infty}\frac{8t}{t^2+4}=0$: \rest{el medicamento desaparece de la sangre}.",
               r"$P(0)=\res{300}$ conejos. \ $\displaystyle\lim_{t\to+\infty}P(t)=500$: la población se acerca a \rest{500 conejos} sin superarlos ($P(t)=500-\frac{200}{t+1}$)."])),
]))
EQ(lambda t: (500 * t + 300) / (t + 1), lambda t: 500 - 200 / (t + 1))

# =====================================================================
# 4. Límits en un punt
GG = tzg(-6, 6, -5, 5, CV % ('-6:-2.18', '1+1/(\\x+2)') + CV % ('-2:1', '\\x+1') + CV % ('1:5.9', '(\\x-3)*(\\x-3)/2+1')
         + hl(1, -6, -2) + vl(-2, -5, 5) + dot(-2, -1, True) + dot(1, 2) + dot(1, 3, True) + dot(3, 1, True) + dot(3, -1)
         + tk(1, 0, '1') + tk(3, 0, '3') + tk(-2, 0, '-2', 'above left') + tk(0, 1, '1', 'left'), sc=0.4)
g = lambda t: 1 + 1 / (t + 2) if t < -2 else (t + 1 if t <= 1 else (t - 3)**2 / 2 + 1)
C(g, -I, 1); C(g, I, I); C(g, -2, -I, -1); C(g, -2, -1, 1); C(g, 1, 2, -1); C(g, 1, 3, 1); C(g, 3, 1)
C(lambda t: 1 / (t - 1), 1, -I, -1)
C(lambda t: t**3 - 2 * t + 1, 2, 5); C(lambda t: (t * t + 3) / (t - 1), -1, -2); C(lambda t: 2 * t / (t - 3), 3, -I, -1); C(lambda t: 2 * t / (t - 3), 3, I, 1)
C(lambda t: (t - 1) / t**2, 0, -I); C(lambda t: (t + 2) / (1 - t), 1, I, -1); C(lambda t: (t + 2) / (1 - t), 1, -I, 1); C(lambda t: (1 - t) / (t - 2)**2, 2, -I)
assert ln(1e-12) < ln(1e-9) < ln(1e-6) < -10; NCHK[0] += 1  # ln(0+) = -inf (creixement lent)
f1 = lambda t: 2 * t + 5 if t < 3 else -t + 2
C(f1, 1, 7); C(f1, 5, -3); C(f1, 3, 11, -1); C(f1, 3, -1, 1)
f2 = lambda t: t * t + 1 if t < -1 else (1 - t if t < 2 else t - 3)
C(f2, -1, 2); C(f2, 2, -1)
S_.append(("Límites en un punto", [
 (1, r"\label{ex:graf}Observa la gráfica de la función $g$ y calcula, si existen, los límites que se indican. Calcula también $g(-2)$, $g(1)$ y $g(3)$.\par\smallskip{\centering " + GG + r"\par}\smallskip"
     + tasks(4, [m(L(MI, 'g(x)')), m(L(PI, 'g(x)')), m(L('-2^-', 'g(x)')), m(L('-2^+', 'g(x)')), m(L('1^-', 'g(x)')), m(L('1^+', 'g(x)')), m(L('1', 'g(x)')), m(L('3', 'g(x)'))])
     + recorda(r"Un punto vacío quiere decir que ese punto no es de la gráfica. El límite en un punto existe si los dos límites laterales coinciden, y no depende del valor de la función en el punto."),
     tasks(4, [r'$\res{1}$', r'$\res{+\infty}$', r'$\res{-\infty}$', r'$\res{-1}$', r'$\res{2}$', r'$\res{3}$', r'$\res{\nexists}$', r'$\res{1}$']) + r"\par $\res{\nexists g(-2)}$, \ $g(1)=\res{2}$, \ $g(3)=\res{-1}$. \ También $\nexists\displaystyle\lim_{x\to-2}g(x)$ (laterales diferentes)."),
 (1, r"Comprueba, dando a $x$ valores cada vez más próximos al punto, que $\displaystyle\lim_{x\to1^-}\frac{1}{x-1}=-\infty$ y que $\displaystyle\lim_{x\to-1^-}\left(x^2+5\right)=6$.",
     r"$x=0{,}9;\ 0{,}99;\ 0{,}999$: \ $\frac{1}{x-1}=-10;\ -100;\ -1\,000\to\res{-\infty}$. \ \ $x=-1{,}1;\ -1{,}01;\ -1{,}001$: \ $x^2+5=6{,}21;\ 6{,}0201;\ 6{,}002001\to\res{6}$."),
 (1, r"Calcula los límites siguientes. Cuando al sustituir salga $\frac k0$, estudia los límites laterales:" + tasks(3, [m(L('2', r'(x^3-2x+1)')), m(L('-1', r'\dfrac{x^2+3}{x-1}')), m(L('3', r'\dfrac{2x}{x-3}')),
     m(L('0', r'\dfrac{x-1}{x^2}')), m(L('1', r'\dfrac{x+2}{1-x}')), m(L('2', r'\dfrac{1-x}{(x-2)^2}')), m(L('3^+', r'\ln(x-3)'))])
     + recorda(r"Si al sustituir sale $\frac{k}{0}$ con $k\neq0$, el límite es infinito: para saber su signo, sustituimos un valor un poco más pequeño y otro un poco más grande que el punto."),
     tasks(3, [r'$8-4+1=\res{5}$', r'$\frac{4}{-2}=\res{-2}$', r'$\frac60$: \ $-\infty$ por la izquierda y $+\infty$ por la derecha: \ $\res{\nexists}$', r'$\frac{-1}{0^+}$: \ $\res{-\infty}$ por los dos lados',
               r'$\frac30$: \ $+\infty$ por la izquierda y $-\infty$ por la derecha: \ $\res{\nexists}$', r'$\frac{-1}{0^+}$: \ $\res{-\infty}$', r'$\ln(0^+)=\res{-\infty}$'])),
 (2, r"Calcula los límites de las funciones a trozos siguientes en los puntos indicados:" + tasks(2, [dm(pw((r'2x+5', 'x<3'), (r'-x+2', r'x\geq3'))) + r'Calcula $\displaystyle\lim_{x\to1}f(x)$, $\displaystyle\lim_{x\to5}f(x)$ y $\displaystyle\lim_{x\to3}f(x)$.',
     dm(pw((r'x^2+1', 'x<-1'), (r'1-x', r'-1\leq x<2'), (r'x-3', r'x\geq2'), name='g(x)')) + r'Calcula $\displaystyle\lim_{x\to-1}g(x)$ y $\displaystyle\lim_{x\to2}g(x)$.']),
     tasks(1, [r'$\lim_{x\to1}(2x+5)=\res{7}$ (el trozo de $x<3$); \ $\lim_{x\to5}(-x+2)=\res{-3}$; \ en $x=3$: $\lim_{x\to3^-}(2x+5)=11$ y $\lim_{x\to3^+}(-x+2)=-1$: \ $\res{\nexists}$.',
               r'$x=-1$: $\lim_{x\to-1^-}(x^2+1)=2$ y $\lim_{x\to-1^+}(1-x)=2$: \ $\res{2}$. \ \ $x=2$: $\lim_{x\to2^-}(1-x)=-1$ y $\lim_{x\to2^+}(x-3)=-1$: \ $\res{-1}$.'])),
]))

# =====================================================================
# 5. Indeterminacions en un punt
C(lambda t: (t - 1) / (t * t - 3 * t + 2), 1, -1); C(lambda t: (t**3 - 9 * t) / (t**3 - 3 * t * t), 3, 2); C(lambda t: (t * t - 4) / (t * t + t - 6), 2, 0.8)
C(lambda t: (t**3 - 1) / (t * t - 1), 1, 1.5); C(lambda t: (t * t + 2 * t) / (t * t + 4 * t + 4), -2, I, -1); C(lambda t: (t * t + 2 * t) / (t * t + 4 * t + 4), -2, -I, 1)
C(lambda t: (t**3 - 3 * t + 2) / (t**3 - t * t - t + 1), 1, 1.5)
EQ(lambda t: t**3 - 3 * t + 2, lambda t: (t - 1)**2 * (t + 2)); EQ(lambda t: t**3 - t * t - t + 1, lambda t: (t - 1)**2 * (t + 1))
C(lambda t: (sq(t) - 3) / (t - 9), 9, 1 / 6); C(lambda t: (sq(t + 5) - 3) / (t - 4), 4, 1 / 6); C(lambda t: (t - 1) / (sq(t + 3) - 2), 1, 4); C(lambda t: (2 - sq(t + 1)) / (t - 3), 3, -0.25)
C(lambda t: (1 + 3 * t)**(2 / t), 0, E**6); C(lambda t: (t - 1)**(1 / (t - 2)), 2, E); C(lambda t: ((t + 3) / 4)**(2 / (t - 1)), 1, E**0.5); C(lambda t: (2 - t)**(t / (t - 1)), 1, E**-1)
C(lambda t: 1 / (t - 1) - 2 / (t * t - 1), 1, 0.5)
S_.append(("Indeterminaciones en un punto", [
 (2, r"Resuelve las indeterminaciones $\frac00$ factorizando:" + tasks(3, [m(L('1', r'\dfrac{x-1}{x^2-3x+2}')), m(L('3', r'\dfrac{x^3-9x}{x^3-3x^2}')), m(L('2', r'\dfrac{x^2-4}{x^2+x-6}')),
     m(L('1', r'\dfrac{x^3-1}{x^2-1}')), m(L('-2', r'\dfrac{x^2+2x}{x^2+4x+4}')), m(L('1', r'\dfrac{x^3-3x+2}{x^3-x^2-x+1}'))])
     + recorda(r"Si $P(a)=Q(a)=0$, los dos polinomios son divisibles por $(x-a)$: factorizamos (factor común, identidades notables, ecuación de segundo grado o Ruffini), simplificamos y volvemos a sustituir."),
     tasks(2, [r'$\frac{x-1}{(x-1)(x-2)}=\frac{1}{x-2}\to\res{-1}$', r'$\frac{x(x-3)(x+3)}{x^2(x-3)}=\frac{x+3}{x}\to\res{2}$', r'$\frac{(x-2)(x+2)}{(x-2)(x+3)}\to\res{\frac45}$',
               r'$\frac{(x-1)(x^2+x+1)}{(x-1)(x+1)}\to\res{\frac32}$', r'$\frac{x(x+2)}{(x+2)^2}=\frac{x}{x+2}\to\frac{-2}{0}$: \ $+\infty$ por la izquierda, $-\infty$ por la derecha, $\res{\nexists}$', r'$\frac{(x-1)^2(x+2)}{(x-1)^2(x+1)}=\frac{x+2}{x+1}\to\res{\frac32}$'])),
 (2, r"Indeterminaciones $\frac00$ con raíces:" + tasks(2, [m(L('9', r'\dfrac{\sqrt x-3}{x-9}')), m(L('4', r'\dfrac{\sqrt{x+5}-3}{x-4}')), m(L('1', r'\dfrac{x-1}{\sqrt{x+3}-2}')), m(L('3', r'\dfrac{2-\sqrt{x+1}}{x-3}'))])
     + recorda(r"Multiplicamos y dividimos por el conjugado de la expresión que tiene la raíz y simplificamos el factor que se anula."),
     tasks(2, [r'$\frac{x-9}{(x-9)(\sqrt x+3)}=\frac{1}{\sqrt x+3}\to\res{\frac16}$', r'$\frac{x-4}{(x-4)(\sqrt{x+5}+3)}\to\res{\frac16}$', r'$\frac{(x-1)(\sqrt{x+3}+2)}{x-1}=\sqrt{x+3}+2\to\res{4}$', r'$\frac{4-(x+1)}{(x-3)(2+\sqrt{x+1})}=\frac{-1}{2+\sqrt{x+1}}\to\res{-\frac14}$'])),
 (2, r"Indeterminación $1^\infty$ en un punto:" + tasks(2, [m(L('0', r'(1+3x)^{\frac2x}')), m(L('2', r'(x-1)^{\frac{1}{x-2}}')), m(L('1', r'\left(\dfrac{x+3}{4}\right)^{\frac{2}{x-1}}')), m(L('1', r'(2-x)^{\frac{x}{x-1}}'))])
     + recorda(r"La fórmula es la misma que en el infinito: \ $\displaystyle\lim_{x\to a}f(x)^{g(x)}=e^{\lim\limits_{x\to a}(f(x)-1)\cdot g(x)}$."),
     tasks(2, [r'$3x\cdot\frac2x=6$: \ $\res{e^6}$', r'$(x-2)\cdot\frac{1}{x-2}=1$: \ $\res{e}$', r'$\frac{x-1}{4}\cdot\frac{2}{x-1}=\frac12$: \ $\res{e^{1/2}=\sqrt e}$', r'$(1-x)\cdot\frac{x}{x-1}=-x\to-1$: \ $\res{e^{-1}=\frac1e}$'])),
 (2, r"Calcula $\displaystyle\lim_{x\to1}\left(\frac{1}{x-1}-\frac{2}{x^2-1}\right)$. ¿Qué indeterminación aparece?",
     r"Al sustituir: $\frac10-\frac20$, es decir, $\infty-\infty$. \ Restamos: $\frac{x+1-2}{x^2-1}=\frac{x-1}{(x-1)(x+1)}=\frac{1}{x+1}\to\res{\frac12}$."),
]))

# =====================================================================
# 6. Continuïtat i tipus de discontinuïtat
def mini(body): return tzg(-3, 3, -3, 3, body + tk(1, 0, 'c'), sc=0.32)
TI = [mini(CV % ('-3:0.66', '1/(\\x-1)') + CV % ('1.34:3', '1/(\\x-1)') + vl(1, -3, 3)),
      mini(CV % ('-3:1', '\\x+1') + CV % ('1:3', '\\x-2') + dot(1, 2) + dot(1, -1, True)),
      mini(CV % ('-2.4:2.4', '\\x*\\x/2-1') + dot(1, -0.5, True) + dot(1, 1.5)),
      mini(CV % ('-3:3', '\\x/2+1') + dot(1, 1.5, True))]
C(lambda t: (t * t - t) / t, 0, -1); C(lambda t: (t + 1) / (t - 2), 2, -I, -1); C(lambda t: (t + 1) / (t - 2), 2, I, 1)
h1 = lambda t: t * t + 1 if t < 0 else t + 1
C(h1, 0, 1); k1 = lambda t: t + 2 if t <= 1 else 1 / (t - 1)
C(k1, 1, 3, -1); C(k1, 1, I, 1); C(lambda t: (t * t - 4) / (t - 2), 2, 4)
C(lambda t: (t * t - 1) / (t * t + t - 2), 1, 2 / 3); C(lambda t: (t * t - 1) / (t * t + t - 2), -2, I, -1); C(lambda t: (t * t - 1) / (t * t + t - 2), -2, -I, 1)
C(lambda t: t / (t * t - 4 * t), 0, -0.25); C(lambda t: t / (t * t - 4 * t), 4, I, 1); C(lambda t: t / (t * t - 4 * t), 4, -I, -1)
C(lambda t: (t * t + 2 * t) / (t + 5), -5, -I, -1); C(lambda t: (t * t + 2 * t) / (t + 5), -5, I, 1); C(lambda t: (t * t + 2 * t) / t, 0, 2)
d1 = lambda t: 1 if t <= 0 else (1 - t * t if t < 2 else -3)
C(d1, 0, 1); C(d1, 2, -3)
S_.append(("Continuidad y tipos de discontinuidad", [
 (1, r"Clasifica las discontinuidades de estas gráficas en el punto $x=c$:" + tasks(4, ['\\par' + g for g in TI])
     + recorda(r"$f$ es continua en $x=c$ si $\exists f(c)$, $\exists\displaystyle\lim_{x\to c}f(x)$ y ambos coinciden. Si el límite existe pero falla alguna otra condición, la discontinuidad es \textbf{evitable}; si los laterales son números diferentes, de \textbf{salto finito}; si un lateral es infinito y el otro un número, de \textbf{salto infinito}; si los dos son infinitos, \textbf{asintótica}."),
     tasks(4, [r'\rest{Asintótica}', r'\rest{Salto finito}', r'\rest{Evitable} ($f(c)\neq\lim$)', r'\rest{Evitable} ($\nexists f(c)$)'])),
 (1, r"Vuelve a la gráfica de $g$ del ejercicio \ref{ex:graf}. ¿En qué puntos no es continua? Clasifica cada discontinuidad.",
     r"$x=-2$: un lateral es $-\infty$ y el otro $-1$: \rest{salto infinito}. \ $x=1$: laterales $2$ y $3$: \rest{salto finito}. \ $x=3$: $\lim_{x\to3}g(x)=1\neq g(3)=-1$: \rest{evitable}. \ Es continua en el resto de puntos."),
 (1, r"Estudia la continuidad de cada función en el punto indicado y, si es discontinua, di de qué tipo es:" + tasks(2, [r'$f(x)=\dfrac{x^2-x}{x}$ \ en $x=0$', r'$g(x)=\dfrac{x+1}{x-2}$ \ en $x=2$',
     r'$h(x)=\begin{cases}x^2+1&\text{si }x<0\\x+1&\text{si }x\geq0\end{cases}$ \ en $x=0$', r'$k(x)=\begin{cases}x+2&\text{si }x\leq1\\\dfrac{1}{x-1}&\text{si }x>1\end{cases}$ \ en $x=1$',
     r'$p(x)=\begin{cases}\dfrac{x^2-4}{x-2}&\text{si }x\neq2\\[2pt]3&\text{si }x=2\end{cases}$ \ en $x=2$']),
     tasks(1, [r'$\nexists f(0)$; \ $\lim_{x\to0}\frac{x(x-1)}{x}=-1$: \ \rest{evitable}', r'$\nexists g(2)$; \ $\frac30$: $-\infty$ por la izquierda y $+\infty$ por la derecha: \ \rest{asintótica}', r'$h(0)=1$, \ $\lim_{x\to0^-}=1$, \ $\lim_{x\to0^+}=1$: \ \rest{continua}',
               r'$k(1)=3$, \ $\lim_{x\to1^-}(x+2)=3$, \ $\lim_{x\to1^+}\frac{1}{x-1}=+\infty$: \ \rest{salto infinito}', r'$p(2)=3$, \ $\lim_{x\to2}(x+2)=4\neq3$: \ \rest{evitable}'])),
 (2, r"Estudia la continuidad de las funciones siguientes:" + tasks(2, [r'$f(x)=\dfrac{x^2-1}{x^2+x-2}$', r'$g(x)=\dfrac{x+3}{x^2+4}$', r'$h(x)=\dfrac{x}{x^2-4x}$', r'$k(x)=\sqrt{x-4}$'])
     + recorda(r"Las funciones racionales son continuas en todo $\mathbb R$ excepto donde se anula el denominador. En esos puntos, si el límite es un número la discontinuidad es evitable y si es $\frac k0$, asintótica."),
     tasks(1, [r'$x^2+x-2=0\Rightarrow x=1,\ x=-2$. \ $x=1$: $\frac{(x-1)(x+1)}{(x-1)(x+2)}\to\frac23$: \rest{evitable}; \ $x=-2$: $\frac{3}{0}$: \rest{asintótica}. Continua en $\mathbb R-\{-2,1\}$.', r'$x^2+4\neq0$: \ \rest{continua en todo $\mathbb R$}.',
               r'$x(x-4)=0\Rightarrow x=0,\ x=4$. \ $x=0$: $\frac{1}{x-4}\to-\frac14$: \rest{evitable}; \ $x=4$: $\frac{4}{0}$: \rest{asintótica}.', r'Continua donde está definida: \ \rest{$[4,+\infty)$}.'])),
 (2, r"Indica si cada una de las funciones siguientes es continua y dónde presenta discontinuidades:" + tasks(2, [r'$f(x)=\dfrac{x^2+2x}{x+5}$', r'$g(x)=\dfrac{x^2+2x}{x}$', dm(pw(('1', 'x<3'), ('4', r'x\geq3'), name='h(x)')), dm(pw(('1', r'x\leq0'), (r'1-x^2', '0<x<2'), ('-3', r'x\geq2'), name='k(x)'))]),
     tasks(1, [r'No está definida en $x=-5$, donde $\frac{15}{0}$: \ \rest{asintótica en $x=-5$}; continua en $\mathbb R-\{-5\}$.', r'$g(x)=x+2$ si $x\neq0$ y no está definida en $0$: \ \rest{evitable en $x=0$}.',
               r'$\lim_{x\to3^-}h=1\neq\lim_{x\to3^+}h=4$: \ \rest{salto finito en $x=3$}; continua en $\mathbb R-\{3\}$.', r'$x=0$: $1=1=k(0)$; \ $x=2$: $\lim_{x\to2^-}(1-x^2)=-3=k(2)$: \ \rest{continua en todo $\mathbb R$}.'])),
]))

# =====================================================================
# 7. Funcions a trossos i paràmetres
fa = lambda t: t - 3 if t < 2 else t * t - 5
C(fa, 2, -1)
fb = lambda t: 2 * t + 1 if t < 0 else (t * t + 1 if t < 2 else 3 / (t - 1))
C(fb, 0, 1); C(fb, 2, 5, -1); C(fb, 2, 3, 1)
fc = lambda t: t * t if t <= -1 else (1 / t if t < 1 else sq(t))
C(fc, -1, 1, -1); C(fc, -1, -1, 1); C(fc, 0, -I, -1); C(fc, 0, I, 1); C(fc, 1, 1)
fd = lambda t: abs(t * t - 4) / (t - 2)
C(fd, 2, -4, -1); C(fd, 2, 4, 1)
PAR((4 - 3, -4 + 5), (-1 + 3, 1 + 1), (6, 3 + 3), (1, 0 + 1), (2 * 1 + 1, 4 - 1), (2**0 + 1, (0 + 4) / (0 + 2)), (3 + 1.5 * 10, 1 * 10 + 8))
S_.append(("Funciones a trozos. Parámetros", [
 (2, r"Estudia la continuidad de las funciones siguientes:" + tasks(1, [dm(pw((r'x-3', 'x<2'), (r'x^2-5', r'x\geq2'))), dm(pw((r'2x+1', 'x<0'), (r'x^2+1', r'0\leq x<2'), (r'\dfrac{3}{x-1}', r'x\geq2'), name='g(x)')),
     dm(pw((r'x^2', r'x\leq-1'), (r'\dfrac1x', r'-1<x<1'), (r'\sqrt x', r'x\geq1'), name='h(x)'))])
     + recorda(r"Primero, la continuidad de cada trozo en su intervalo (¡cuidado con los denominadores y las raíces!). Después, en cada punto donde se rompe la función, comparamos $f(a)$ y los dos límites laterales."),
     tasks(1, [r'Trozos polinómicos: continuas. \ $x=2$: $f(2)=-1$, $\lim_{x\to2^-}(x-3)=-1$, $\lim_{x\to2^+}(x^2-5)=-1$: \ \rest{continua} en $\mathbb R$.',
               r'El denominador $x-1$ se anula en $1$, fuera de $x\geq2$. \ $x=0$: $1=1=g(0)$, continua. \ $x=2$: $\lim_{x\to2^-}=5$, $\lim_{x\to2^+}=3=g(2)$: \ \rest{salto finito} en $x=2$.',
               r'$\frac1x$ no está definida en $x=0$, que es de su intervalo: $-\infty$ y $+\infty$, \rest{asintótica en $x=0$}. \ $x=-1$: $h(-1)=1$, laterales $1$ y $-1$: \rest{salto finito}. \ $x=1$: $h(1)=1$, laterales $1$ y $1$: continua.'])),
 (2, r"Escribe $f(x)=\dfrac{|x^2-4|}{x-2}$ como una función a trozos y estudia su continuidad en $x=2$.",
     r"$x^2-4<0$ si $-2<x<2$. \ Para $x>2$: $f(x)=\frac{(x-2)(x+2)}{x-2}=x+2\to4$; \ para $-2<x<2$: $f(x)=-(x+2)\to-4$. \ $\nexists f(2)$ y los laterales son $-4$ y $4$: \ \rest{salto finito} en $x=2$."),
 (2, r"Calcula $m$ para que esta función sea continua en todo $\mathbb R$:" + dm(pw((r'x^2-3', r'x\leq2'), (r'-x^2+m', 'x>2')))
     + recorda(r"Si la función depende de un parámetro, \textbf{igualamos los límites laterales} en el punto donde se rompe y resolvemos la ecuación."),
     r"$\lim_{x\to2^-}(x^2-3)=1=f(2)$; \ $\lim_{x\to2^+}(-x^2+m)=-4+m$. \ $-4+m=1\Rightarrow\res{m=5}$."),
 (2, r"Halla el valor del parámetro para que cada función sea continua en todo $\mathbb R$:" + tasks(1, [dm(pw((r'ax+3', 'x<1'), (r'x^2-a', r'x\geq1'))), dm(pw((r'\dfrac{x^2-9}{x-3}', r'x\neq3'), ('k', 'x=3'), name='g(x)')),
     dm(pw((r'2^x+a', r'x\leq0'), (r'\dfrac{x+4}{x+2}', 'x>0'), name='h(x)'))]),
     tasks(1, [r'$a+3=1-a\Rightarrow\res{a=-1}$', r'$\lim_{x\to3}(x+3)=6\Rightarrow\res{k=6}$', r'$1+a=\frac42=2\Rightarrow\res{a=1}$ \ (el denominador $x+2$ se anula en $-2$, fuera de $x>0$)'])),
 (3, r"Halla $a$ y $b$ para que la función siguiente sea continua en todo $\mathbb R$:" + dm(pw((r'x+a', 'x<0'), (r'bx+1', r'0\leq x\leq2'), (r'x^2-a', 'x>2'))),
     r"$x=0$: $a=1$. \ $x=2$: $2b+1=4-a=3\Rightarrow b=1$. \ $\res{a=1,\ b=1}$"),
 (2, r"Un taxi cobra $P(x)=3+1{,}5x$ euros por un viaje de $x\leq10$ km y $P(x)=ax+8$ si $x>10$ km. ¿Cuánto debe valer $a$ para que el precio no dé ningún salto en los 10 km? ¿Cuánto cuesta, entonces, un viaje de 25 km?",
     r"$\lim_{x\to10^-}P(x)=3+15=18$ y $\lim_{x\to10^+}P(x)=10a+8$: \ $10a+8=18\Rightarrow\res{a=1}$ €/km. \ $P(25)=25+8=\res{33\text{ €}}$."),
]))

# =====================================================================
# 8. Branques infinites i asímptotes
C(lambda t: (t * t - 1) / (t * t + 4), I, 1); C(lambda t: (t * t - 1) / (t * t + 4), -I, 1)
C(lambda t: t / (t - 1)**2, 1, I); C(lambda t: t / (t - 1)**2, I, 0); C(lambda t: 2 * t * t / (t - 3), 3, -I, -1); C(lambda t: 2 * t * t / (t - 3), 3, I, 1)
EQ(lambda t: 2 * t * t, lambda t: (t - 3) * (2 * t + 6) + 18); C(lambda t: 2 * t * t / (t - 3) - (2 * t + 6), I, 0)
C(lambda t: (3 * t + 1) / (t - 2), 2, -I, -1); C(lambda t: (3 * t + 1) / (t - 2), 2, I, 1); C(lambda t: (3 * t + 1) / (t - 2), I, 3); EQ(lambda t: (3 * t + 1) / (t - 2) - 3, lambda t: 7 / (t - 2))
C(lambda t: t * t / (t * t - 4), -2, I, -1); C(lambda t: t * t / (t * t - 4), -2, -I, 1); C(lambda t: t * t / (t * t - 4), 2, -I, -1); C(lambda t: t * t / (t * t - 4), 2, I, 1); C(lambda t: t * t / (t * t - 4), I, 1)
C(lambda t: (t + 1) / (t * t - 1), -1, -0.5); C(lambda t: (t + 1) / (t * t - 1), 1, -I, -1); C(lambda t: (t + 1) / (t * t - 1), 1, I, 1); C(lambda t: (t + 1) / (t * t - 1), I, 0)
C(lambda t: (t * t + t + 1) / (t - 1), 1, -I, -1); C(lambda t: (t * t + t + 1) / (t - 1), 1, I, 1); EQ(lambda t: t * t + t + 1, lambda t: (t - 1) * (t + 2) + 3)
C(lambda t: (t**3 + 1) / t**2, 0, I); EQ(lambda t: (t**3 + 1) / t**2, lambda t: t + 1 / t**2)
C(lambda t: 3 * 2**t / (2**t + 1), 900, 3); C(lambda t: 3 * 2**t / (2**t + 1), -I, 0)
C(lambda t: sq(t * t + 4 * t) / t, I, 1); C(lambda t: sq(t * t + 4 * t) - t, I, 2); C(lambda t: sq(t * t + 4 * t) / t, -I, -1); C(lambda t: sq(t * t + 4 * t) + t, -I, -2)
C(lambda t: (t**3 - 3 * t) / t, I, I); C(lambda t: ln(t) / t, I, 0); C(lambda t: ln(t), I, I); C(lambda t: t**3 / (t - 1) / t, I, I); C(lambda t: t**3 / (t - 1), 1, I, 1)
PAR((-2 + 2, 0), (3 * 0 + 2, 2 * 1))  # c = 2 (AV x = -2), (3·0+2)/(0+2) = 1
S_.append(("Ramas infinitas y asíntotas", [
 (2, r"Halla las ramas infinitas de las funciones siguientes. Si hay asíntotas, estudia la posición de la curva respecto de ellas:" + tasks(3, [r'$f(x)=\dfrac{x^2-1}{x^2+4}$', r'$g(x)=\dfrac{x}{(x-1)^2}$', r'$h(x)=\dfrac{2x^2}{x-3}$'])
     + recorda(r"AV: donde el límite es infinito ($\frac k0$). \ AH: $\displaystyle\lim_{x\to\pm\infty}f(x)=b$. \ AO en una racional cuando el grado de arriba es una unidad mayor: la asíntota es el cociente de la división. La posición se ve con el signo de $f(x)$ menos la asíntota."),
     tasks(1, [r'Ninguna AV ($x^2+4\neq0$). \ AH $\res{y=1}$: \ $f(x)-1=\frac{-5}{x^2+4}<0$, la curva queda \rest{por debajo}. No tiene AO.',
               r'AV $\res{x=1}$: $\frac{1}{0^+}$, $+\infty$ por los dos lados. \ AH $\res{y=0}$: por encima si $x\to+\infty$ ($g>0$) y por debajo si $x\to-\infty$. No tiene AO.',
               r'AV $\res{x=3}$: $-\infty$ por la izquierda y $+\infty$ por la derecha. \ No tiene AH. \ $2x^2=(x-3)(2x+6)+18$: \ AO $\res{y=2x+6}$; \ $\frac{18}{x-3}$: por encima si $x\to+\infty$ y por debajo si $x\to-\infty$.'])),
 (2, r"Calcula todas las asíntotas de las funciones siguientes y estudia los límites laterales en cada asíntota vertical:" + tasks(2, [r'$f(x)=\dfrac{3x+1}{x-2}$', r'$f(x)=\dfrac{x^2}{x^2-4}$', r'$f(x)=\dfrac{x+1}{x^2-1}$', r'$f(x)=\dfrac{x^2+x+1}{x-1}$', r'$f(x)=\dfrac{x^3+1}{x^2}$', r'$f(x)=\dfrac{3\cdot2^x}{2^x+1}$']),
     tasks(1, [r'AV $\res{x=2}$ ($-\infty$ por la izquierda, $+\infty$ por la derecha); AH $\res{y=3}$ ($f(x)-3=\frac{7}{x-2}$: por encima a la derecha y por debajo a la izquierda).',
               r'AV $\res{x=-2}$ ($+\infty$ por la izquierda, $-\infty$ por la derecha) y $\res{x=2}$ ($-\infty$ por la izquierda, $+\infty$ por la derecha); AH $\res{y=1}$.',
               r'En $x=-1$: $\frac00$, $\frac{1}{x-1}\to-\frac12$: no hay AV (agujero). \ AV $\res{x=1}$ ($-\infty$ por la izquierda, $+\infty$ por la derecha); AH $\res{y=0}$.',
               r'AV $\res{x=1}$ ($-\infty$ por la izquierda, $+\infty$ por la derecha). \ $x^2+x+1=(x-1)(x+2)+3$: AO $\res{y=x+2}$.',
               r'AV $\res{x=0}$ ($\frac{1}{0^+}$: $+\infty$ por los dos lados). \ $f(x)=x+\frac{1}{x^2}$: AO $\res{y=x}$, y la curva queda siempre por encima.',
               r'No es racional: \ $\lim_{x\to+\infty}\frac{3\cdot2^x}{2^x}=3$ i $\lim_{x\to-\infty}\frac{3\cdot0}{0+1}=0$: \ AH $\res{y=3}$ por la derecha y $\res{y=0}$ por la izquierda. No tiene AV.'])),
 (3, r"Calcula las asíntotas oblicuas de $f(x)=\sqrt{x^2+4x}$ con los límites $m=\displaystyle\lim\frac{f(x)}{x}$ i $n=\displaystyle\lim\,[f(x)-mx]$. Hazlo cuando $x\to+\infty$ y cuando $x\to-\infty$.",
     r"$x\to+\infty$: $m=\lim\frac{\sqrt{x^2+4x}}{x}=1$, \ $n=\lim(\sqrt{x^2+4x}-x)=\lim\frac{4x}{\sqrt{x^2+4x}+x}=2$: \ $\res{y=x+2}$. \ \ $x\to-\infty$: $\sqrt{x^2}=-x$, $m=-1$, \ $n=\lim(\sqrt{x^2+4x}+x)=\lim\frac{4x}{\sqrt{x^2+4x}-x}=\frac{4x}{-2x}=-2$: \ $\res{y=-x-2}$."),
 (2, r"¿Cuáles de estas funciones tienen ramas parabólicas cuando $x\to+\infty$? Justifícalo calculando $\lim f(x)$ i $m=\lim\frac{f(x)}{x}$." + tasks(4, [r'$f(x)=x^3-3x$', r'$g(x)=\ln x$', r'$h(x)=\dfrac{x^3}{x-1}$', r'$k(x)=\dfrac{x^2+1}{x}$']),
     tasks(1, [r'$\lim f=+\infty$, $m=\lim(x^2-3)=+\infty$: \ \rest{rama parabólica}', r'$\lim g=+\infty$, $m=\lim\frac{\ln x}{x}=0$: \ \rest{rama parabólica}', r'$\lim h=+\infty$, $m=\lim\frac{x^2}{x-1}=+\infty$: \ \rest{rama parabólica}', r'$k(x)=x+\frac1x$: \ \rest{asíntota oblicua $y=x$}, no es rama parabólica'])),
 (3, r"Halla $a$, $b$ y $c$ para que la función $f(x)=\dfrac{ax+b}{x+c}$ tenga una asíntota vertical en $x=-2$, una asíntota horizontal en $y=3$ y pase por el punto $(0,1)$.",
     r"AV $x=-2$: el denominador se anula en $-2$: $c=2$. \ AH: $\displaystyle\lim_{x\to\pm\infty}\frac{ax+b}{x+2}=a=3$. \ Punto: $f(0)=\frac b2=1\Rightarrow b=2$. \ $\res{a=3,\ b=2,\ c=2}$"),
]))
C(lambda t: (3 * t + 2) / (t + 2), I, 3); C(lambda t: (3 * t + 2) / (t + 2), -2, I, -1)
C(lambda t: (t * t + 1) / t - t, I, 0)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "límites, límites en el infinito, comparación de infinitos, indeterminaciones, límites laterales, continuidad, tipos de discontinuidad, funciones a trozos, parámetros, asíntotas, ramas parabólicas"
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
pre += r'''\providecommand{\gt}{>}\providecommand{\lt}{<}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

def fix(t):
    """Fora dels dibuixos: l'espai després de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = "Límites y continuidad"
def build(sol):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 8: %s' % (t, TIT), capcalera='%s · Unidad 8: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-mi')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1batx-mi') + '{' + ('Soluciones de la ficha · Unidad 8' if sol else 'Ficha de ejercicios · Unidad 8') + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con la calculadora de límites de los apuntes interactivos de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos: antes de transformar una expresión, sustituye y comprueba si hay de verdad una indeterminación. Las secciones siguen el orden de los apuntes. Puedes comprobar los resultados con la calculadora de límites de los apuntes interactivos.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            if sol:
                lab = re.search(r'\\label\{[^}]*\}', q)
                s = (lab.group(0) if lab else '') + s
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con la calculadora de límites de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't8-fitxa-solucions-es.tex' if sol else 't8-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis;', NCHK[0], 'comprovacions')
