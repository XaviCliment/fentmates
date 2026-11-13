# Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (1r Batxillerat MI, Unitat 8: Límits i continuïtat)
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

S_.append(("Límits a l'infinit", [
 (1, r"Observa les gràfiques i escriu, per a cadascuna, el límit quan $x\to+\infty$ i quan $x\to-\infty$. Les rectes discontínues són asímptotes." + tasks(4, ['\\par' + g for g in (GA, GB, GC, GD)])
     + recorda(r"Per a $x\to+\infty$ mira el \textbf{final dret} de la gràfica i per a $x\to-\infty$, el \textbf{final esquerre}. Si la gràfica oscil·la sense acostar-se a cap valor, el límit no existeix."),
     tasks(2, [r'$\displaystyle\lim_{x\to+\infty}=\res{+\infty}$, \ $\displaystyle\lim_{x\to-\infty}=\res{-\infty}$', r'$\displaystyle\lim_{x\to+\infty}=\res{+\infty}$, \ $\displaystyle\lim_{x\to-\infty}=\res{-2}$',
               r'$\displaystyle\lim_{x\to\pm\infty}=\res{2}$ \ (asímptota $y=2$)', r'Oscil·la: \ $\res{\nexists}$ cap dels dos límits'])),
 (2, r"Calcula, per a cada funció, $\displaystyle\lim_{x\to-\infty}f(x)$ i $\displaystyle\lim_{x\to+\infty}f(x)$. Fixa't bé en el domini de les arrels." + tasks(2, ['$f(x)=%s$' % f for f, _, _ in FAM])
     + recorda(r"Potències, exponencials de base major que 1, arrels i logaritmes tendeixen a $+\infty$ quan $x\to+\infty$. Un polinomi es comporta com el seu terme de major grau. Si la funció no està definida cap a un infinit, el límit no existeix."),
     tasks(2, ['$%s$: \\ $\\res{%s}$ \\ i \\ $\\res{%s}$' % (f, a, b) for f, a, b in FAM])
     + r"\par\small (A la e), el domini és $\left[-\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right]$; a la f), $-5^x=-(5^x)$.)"),
 (1, r"Calcula els límits següents comparant els graus del numerador i del denominador:" + tasks(3, [m(L(PI, r'\dfrac{x^2-5x+3}{3x-5}')), m(L(PI, r'\dfrac{x^2+3}{x^3}')), m(L(PI, r'\dfrac{3x^2-5x+1}{2x^2-6}')),
     m(L(MI, r'\dfrac{4x^3-x}{2-x^2}')), m(L(MI, r'\dfrac{1-6x}{3x+2}')), m(L(MI, r'\dfrac{2x^2-1}{5-x}'))])
     + recorda(r"$\displaystyle\lim_{x\to\pm\infty}\frac{P(x)}{Q(x)}=\lim_{x\to\pm\infty}\frac{a_nx^n}{b_mx^m}$: \ si $n>m$, $\pm\infty$ (cal mirar el signe); \ si $n=m$, $\frac{a_n}{b_m}$; \ si $n<m$, $0$."),
     tasks(3, [r'$\lim\frac{x^2}{3x}=\lim\frac x3=\res{+\infty}$', r'$\lim\frac{x^2}{x^3}=\res{0}$', r'Mateix grau: $\res{\frac32}$', r'$\lim\frac{4x^3}{-x^2}=\lim(-4x)=\res{+\infty}$', r'$\frac{-6}{3}=\res{-2}$', r'$\lim\frac{2x^2}{-x}=\lim(-2x)=\res{+\infty}$'])),
 (2, r"Calcula els límits següents amb exponencials i arrels:" + tasks(3, [m(L(PI, r'\left(\tfrac13\right)^x')), m(L(MI, r'\left(3^x+1\right)')), m(L(MI, r'0{,}4^x')),
     m(L(PI, r'\dfrac{\sqrt{4x^2+1}}{x+3}')), m(L(MI, r'\dfrac{\sqrt{x^2+1}}{2x}')), m(L(PI, r'\left(e^{-x}+2\right)'))]),
     tasks(3, [r'$\left(\tfrac13\right)^{+\infty}=\res{0}$', r'$3^{-\infty}+1=\res{1}$', r'$0{,}4^{-\infty}=\res{+\infty}$', r'$\lim\frac{2x}{x}=\res{2}$', r'$\sqrt{x^2}=|x|=-x$: \ $\lim\frac{-x}{2x}=\res{-\frac12}$', r'$e^{-\infty}+2=\res{2}$'])),
]))

# =====================================================================
# 2. Comparació d'infinits
C(lambda t: t**4 / 2**t, 900, 0); C(lambda t: 3**t / t**20, 600, I); C(lambda t: ln(t) / t, I, 0); C(lambda t: t**3 - ex(t), 600, -I)
C(lambda t: (2**t + t * t) / 2**(t + 1), 900, 0.5); C(lambda t: sq(t) - ln(t), I, I); C(lambda t: t - 2**t, 900, -I)
C(lambda t: t * t - sq(t**5 + 3), I, -I); C(lambda t: 3**t - sq(t**3 - 2), 600, I); C(lambda t: (5**t + t) / 4**t, 400, I)
S_.append(("Comparació d'infinits", [
 (1, r"Ordena aquests infinits de menor a major ordre quan $x\to+\infty$: \quad $x^2,\ \ 3^x,\ \ \ln x,\ \ x^5,\ \ \sqrt x,\ \ 1{,}1^x$."
     + recorda(r"Quan $x\to+\infty$: \ logaritmes $\ll$ potències $\ll$ exponencials (de base major que 1). Entre potències guanya l'exponent major i entre exponencials, la base major."),
     r"$\res{\ln x\ll\sqrt x\ll x^2\ll x^5\ll1{,}1^x\ll3^x}$"),
 (2, r"Calcula els límits següents comparant infinits:" + tasks(3, [m(L(PI, r'\dfrac{x^4}{2^x}')), m(L(PI, r'\dfrac{3^x}{x^{20}}')), m(L(PI, r'\dfrac{\ln x}{x}')), m(L(PI, r'\left(x^3-e^x\right)')),
     m(L(PI, r'\dfrac{2^x+x^2}{2^{x+1}}')), m(L(PI, r'\left(\sqrt x-\ln x\right)')), m(L(PI, r'\left(x-2^x\right)')), m(L(PI, r'\dfrac{5^x+x}{4^x}'))]),
     tasks(3, [r'$\res{0}$', r'$\res{+\infty}$', r'$\res{0}$', r'$\res{-\infty}$', r'$\lim\frac{2^x}{2\cdot2^x}=\res{\frac12}$', r'$\res{+\infty}$', r'$\res{-\infty}$', r'$\lim\left(\frac54\right)^x=\res{+\infty}$'])),
 (2, r"Indeterminació $\infty-\infty$ per comparació d'infinits:" + tasks(2, [m(L(PI, r'\left(x^2-\sqrt{x^5+3}\right)')), m(L(PI, r'\left(3^x-\sqrt{x^3-2}\right)'))]),
     tasks(2, [r'$\sqrt{x^5}=x^{5/2}$ i $\frac52>2$: \ $\res{-\infty}$', r'$3^x$ té major ordre: \ $\res{+\infty}$'])),
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
S_.append(("Indeterminacions a l'infinit", [
 (2, r"Indeterminació $\frac{\infty}{\infty}$ amb arrels:" + tasks(2, [m(L(PI, r'\dfrac{\sqrt{x^2+1}+2x}{3x-1}')), m(L(PI, r'\dfrac{\sqrt{4x^4+x}-x}{x^2+5}')), m(L(PI, r'\dfrac{3x+\sqrt x}{x-\sqrt x}')), m(L(PI, r'\dfrac{\sqrt{4x^3+x-2}}{8x^2-7}'))])
     + recorda(r"Ens quedem amb el terme de major grau de cada part: \ $\sqrt{x^2+1}\approx x$ (si $x>0$), \ $\sqrt{4x^3}=2x^{3/2}$."),
     tasks(2, [r'$\lim\frac{x+2x}{3x}=\res{1}$', r'$\lim\frac{2x^2}{x^2}=\res{2}$', r'$\lim\frac{3x}{x}=\res{3}$', r'$\lim\frac{2x^{3/2}}{8x^2}=\lim\frac{1}{4\sqrt x}=\res{0}$'])),
 (2, r"Indeterminació $\infty-\infty$ amb fraccions:" + tasks(2, [m(L(PI, r'\left(\dfrac{2x^2-5x}{x+3}-2x\right)')), m(L(PI, r'\left(\dfrac{x^2}{x-2}-\dfrac{x^2}{x+2}\right)')), m(L(PI, r'\left(\dfrac{x^3}{x^2-1}-x\right)')), m(L(PI, r'\left(\dfrac{x^2+1}{x}+\dfrac{5x-x^2}{3x-1}\right)'))])
     + recorda(r"Si la indeterminació $\infty-\infty$ ve d'una suma o resta de fraccions, \textbf{fem l'operació} amb denominador comú i calculem el límit de la fracció que en resulta."),
     tasks(1, [r'$\dfrac{2x^2-5x-2x(x+3)}{x+3}=\dfrac{-11x}{x+3}\to\res{-11}$', r'$\dfrac{x^2(x+2)-x^2(x-2)}{x^2-4}=\dfrac{4x^2}{x^2-4}\to\res{4}$', r'$\dfrac{x^3-x(x^2-1)}{x^2-1}=\dfrac{x}{x^2-1}\to\res{0}$',
               r'$\dfrac{(x^2+1)(3x-1)+x(5x-x^2)}{x(3x-1)}=\dfrac{2x^3+4x^2+3x-1}{3x^2-x}\to\lim\dfrac{2x}{3}=\res{+\infty}$'])),
 (2, r"Indeterminació $\infty-\infty$ amb arrels:" + tasks(3, [m(L(PI, r'\left(x-\sqrt{x^2-1}\right)')), m(L(PI, r'\left(\sqrt{x+2}-\sqrt{x-2}\right)')), m(L(PI, r'\left(\sqrt{x^2+6x}-x\right)')), m(L(PI, r'\left(\sqrt{x^2-2}-\sqrt{x^2+x}\right)')), m(L(PI, r'\left(2x-\sqrt{4x^2-3x}\right)'))])
     + recorda(r"Multipliquem i dividim pel \textbf{conjugat}: $(A-B)(A+B)=A^2-B^2$ fa desaparéixer les arrels del numerador."),
     tasks(1, [r'$\dfrac{x^2-(x^2-1)}{x+\sqrt{x^2-1}}=\dfrac{1}{x+\sqrt{x^2-1}}\to\res{0}$', r'$\dfrac{(x+2)-(x-2)}{\sqrt{x+2}+\sqrt{x-2}}=\dfrac{4}{\sqrt{x+2}+\sqrt{x-2}}\to\res{0}$', r'$\dfrac{6x}{\sqrt{x^2+6x}+x}\to\dfrac{6x}{2x}=\res{3}$',
               r'$\dfrac{-2-x}{\sqrt{x^2-2}+\sqrt{x^2+x}}\to\dfrac{-x}{2x}=\res{-\frac12}$', r'$\dfrac{4x^2-(4x^2-3x)}{2x+\sqrt{4x^2-3x}}=\dfrac{3x}{2x+\sqrt{4x^2-3x}}\to\dfrac{3x}{4x}=\res{\frac34}$'])),
 (2, r"Indeterminació $1^{\infty}$:" + tasks(3, [m(L(PI, r'\left(\dfrac{x}{x+2}\right)^{2x+1}')), m(L(PI, r'\left(\dfrac{2x-2}{2x+1}\right)^{3x^2}')), m(L(PI, r'\left(1+\dfrac3x\right)^{2x}')),
     m(L(PI, r'\left(\dfrac{x+1}{x-2}\right)^{x}')), m(L(PI, r'\left(\dfrac{x^2+1}{x^2-3}\right)^{x^2}')), m(L(PI, r'\left(\dfrac{3x+1}{x+2}\right)^{x}'))])
     + recorda(r"Si $\lim f(x)=1$ i $\lim g(x)=\pm\infty$: \ $\lim f(x)^{g(x)}=e^{\lim\,(f(x)-1)\cdot g(x)}$. Si la base no tendeix a 1, no hi ha indeterminació."),
     tasks(2, [r'$\frac{x}{x+2}-1=\frac{-2}{x+2}$; \ $\lim\frac{-2(2x+1)}{x+2}=-4$: \ $\res{e^{-4}=\frac{1}{e^4}}$', r'$\frac{-3}{2x+1}\cdot3x^2=\frac{-9x^2}{2x+1}\to-\infty$: \ $e^{-\infty}=\res{0}$', r'$e^{\lim\frac3x\cdot2x}=\res{e^6}$',
               r'$\frac{3}{x-2}\cdot x\to3$: \ $\res{e^3}$', r'$\frac{4}{x^2-3}\cdot x^2\to4$: \ $\res{e^4}$', r'La base tendeix a $3$: \ $3^{+\infty}=\res{+\infty}$ (no és $1^\infty$)'])),
 (2, r"Problemes. Calcula el límit que respon cada pregunta:" + tasks(1, [r"El cost mitjà (en euros) de fabricar $x$ unitats d'un producte és $C(x)=\dfrac{12x+3\,000}{x}$. A quin valor s'acosta el cost per unitat si se'n fabriquen moltíssimes?",
     r"La concentració d'un medicament en sang $t$ hores després de prendre'l és $c(t)=\dfrac{8t}{t^2+4}$ (mg/l). Què passa amb la concentració a molt llarg termini?",
     r"Una població de conills evoluciona segons $P(t)=\dfrac{500t+300}{t+1}$, amb $t$ en mesos. Quina és la població inicial? Té algun límit el nombre de conills?"]),
     tasks(1, [r"$\displaystyle\lim_{x\to+\infty}\frac{12x+3\,000}{x}=12$: el cost per unitat s'acosta a \rest{12 €}.", r"$\displaystyle\lim_{t\to+\infty}\frac{8t}{t^2+4}=0$: \rest{el medicament desapareix de la sang}.",
               r"$P(0)=\res{300}$ conills. \ $\displaystyle\lim_{t\to+\infty}P(t)=500$: la població s'acosta a \rest{500 conills} sense superar-los ($P(t)=500-\frac{200}{t+1}$)."])),
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
S_.append(("Límits en un punt", [
 (1, r"\label{ex:graf}Observa la gràfica de la funció $g$ i calcula, si existeixen, els límits que s'indiquen. Calcula també $g(-2)$, $g(1)$ i $g(3)$.\par\smallskip{\centering " + GG + r"\par}\smallskip"
     + tasks(4, [m(L(MI, 'g(x)')), m(L(PI, 'g(x)')), m(L('-2^-', 'g(x)')), m(L('-2^+', 'g(x)')), m(L('1^-', 'g(x)')), m(L('1^+', 'g(x)')), m(L('1', 'g(x)')), m(L('3', 'g(x)'))])
     + recorda(r"Un punt buit vol dir que aquell punt no és de la gràfica. El límit en un punt existeix si els dos límits laterals coincideixen, i no depén del valor de la funció en el punt."),
     tasks(4, [r'$\res{1}$', r'$\res{+\infty}$', r'$\res{-\infty}$', r'$\res{-1}$', r'$\res{2}$', r'$\res{3}$', r'$\res{\nexists}$', r'$\res{1}$']) + r"\par $\res{\nexists g(-2)}$, \ $g(1)=\res{2}$, \ $g(3)=\res{-1}$. \ També $\nexists\displaystyle\lim_{x\to-2}g(x)$ (laterals diferents)."),
 (1, r"Comprova, donant a $x$ valors cada vegada més pròxims al punt, que $\displaystyle\lim_{x\to1^-}\frac{1}{x-1}=-\infty$ i que $\displaystyle\lim_{x\to-1^-}\left(x^2+5\right)=6$.",
     r"$x=0{,}9;\ 0{,}99;\ 0{,}999$: \ $\frac{1}{x-1}=-10;\ -100;\ -1\,000\to\res{-\infty}$. \ \ $x=-1{,}1;\ -1{,}01;\ -1{,}001$: \ $x^2+5=6{,}21;\ 6{,}0201;\ 6{,}002001\to\res{6}$."),
 (1, r"Calcula els límits següents. Quan en substituir isca $\frac k0$, estudia els límits laterals:" + tasks(3, [m(L('2', r'(x^3-2x+1)')), m(L('-1', r'\dfrac{x^2+3}{x-1}')), m(L('3', r'\dfrac{2x}{x-3}')),
     m(L('0', r'\dfrac{x-1}{x^2}')), m(L('1', r'\dfrac{x+2}{1-x}')), m(L('2', r'\dfrac{1-x}{(x-2)^2}')), m(L('3^+', r'\ln(x-3)'))])
     + recorda(r"Si en substituir ix $\frac{k}{0}$ amb $k\neq0$, el límit és infinit: per saber-ne el signe, substituïm un valor una mica més xicotet i un altre una mica més gran que el punt."),
     tasks(3, [r'$8-4+1=\res{5}$', r'$\frac{4}{-2}=\res{-2}$', r'$\frac60$: \ $-\infty$ per l’esquerra i $+\infty$ per la dreta: \ $\res{\nexists}$', r'$\frac{-1}{0^+}$: \ $\res{-\infty}$ pels dos costats',
               r'$\frac30$: \ $+\infty$ per l’esquerra i $-\infty$ per la dreta: \ $\res{\nexists}$', r'$\frac{-1}{0^+}$: \ $\res{-\infty}$', r'$\ln(0^+)=\res{-\infty}$'])),
 (2, r"Calcula els límits de les funcions a trossos següents en els punts indicats:" + tasks(2, [dm(pw((r'2x+5', 'x<3'), (r'-x+2', r'x\geq3'))) + r'Calcula $\displaystyle\lim_{x\to1}f(x)$, $\displaystyle\lim_{x\to5}f(x)$ i $\displaystyle\lim_{x\to3}f(x)$.',
     dm(pw((r'x^2+1', 'x<-1'), (r'1-x', r'-1\leq x<2'), (r'x-3', r'x\geq2'), name='g(x)')) + r'Calcula $\displaystyle\lim_{x\to-1}g(x)$ i $\displaystyle\lim_{x\to2}g(x)$.']),
     tasks(1, [r'$\lim_{x\to1}(2x+5)=\res{7}$ (el tros de $x<3$); \ $\lim_{x\to5}(-x+2)=\res{-3}$; \ en $x=3$: $\lim_{x\to3^-}(2x+5)=11$ i $\lim_{x\to3^+}(-x+2)=-1$: \ $\res{\nexists}$.',
               r'$x=-1$: $\lim_{x\to-1^-}(x^2+1)=2$ i $\lim_{x\to-1^+}(1-x)=2$: \ $\res{2}$. \ \ $x=2$: $\lim_{x\to2^-}(1-x)=-1$ i $\lim_{x\to2^+}(x-3)=-1$: \ $\res{-1}$.'])),
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
S_.append(("Indeterminacions en un punt", [
 (2, r"Resol les indeterminacions $\frac00$ factoritzant:" + tasks(3, [m(L('1', r'\dfrac{x-1}{x^2-3x+2}')), m(L('3', r'\dfrac{x^3-9x}{x^3-3x^2}')), m(L('2', r'\dfrac{x^2-4}{x^2+x-6}')),
     m(L('1', r'\dfrac{x^3-1}{x^2-1}')), m(L('-2', r'\dfrac{x^2+2x}{x^2+4x+4}')), m(L('1', r'\dfrac{x^3-3x+2}{x^3-x^2-x+1}'))])
     + recorda(r"Si $P(a)=Q(a)=0$, tots dos polinomis són divisibles per $(x-a)$: factoritzem (factor comú, identitats notables, equació de 2n grau o Ruffini), simplifiquem i tornem a substituir."),
     tasks(2, [r'$\frac{x-1}{(x-1)(x-2)}=\frac{1}{x-2}\to\res{-1}$', r'$\frac{x(x-3)(x+3)}{x^2(x-3)}=\frac{x+3}{x}\to\res{2}$', r'$\frac{(x-2)(x+2)}{(x-2)(x+3)}\to\res{\frac45}$',
               r'$\frac{(x-1)(x^2+x+1)}{(x-1)(x+1)}\to\res{\frac32}$', r'$\frac{x(x+2)}{(x+2)^2}=\frac{x}{x+2}\to\frac{-2}{0}$: \ $+\infty$ per l’esquerra, $-\infty$ per la dreta, $\res{\nexists}$', r'$\frac{(x-1)^2(x+2)}{(x-1)^2(x+1)}=\frac{x+2}{x+1}\to\res{\frac32}$'])),
 (2, r"Indeterminacions $\frac00$ amb arrels:" + tasks(2, [m(L('9', r'\dfrac{\sqrt x-3}{x-9}')), m(L('4', r'\dfrac{\sqrt{x+5}-3}{x-4}')), m(L('1', r'\dfrac{x-1}{\sqrt{x+3}-2}')), m(L('3', r'\dfrac{2-\sqrt{x+1}}{x-3}'))])
     + recorda(r"Multipliquem i dividim pel conjugat de l'expressió que té l'arrel i simplifiquem el factor que s'anul·la."),
     tasks(2, [r'$\frac{x-9}{(x-9)(\sqrt x+3)}=\frac{1}{\sqrt x+3}\to\res{\frac16}$', r'$\frac{x-4}{(x-4)(\sqrt{x+5}+3)}\to\res{\frac16}$', r'$\frac{(x-1)(\sqrt{x+3}+2)}{x-1}=\sqrt{x+3}+2\to\res{4}$', r'$\frac{4-(x+1)}{(x-3)(2+\sqrt{x+1})}=\frac{-1}{2+\sqrt{x+1}}\to\res{-\frac14}$'])),
 (2, r"Indeterminació $1^\infty$ en un punt:" + tasks(2, [m(L('0', r'(1+3x)^{\frac2x}')), m(L('2', r'(x-1)^{\frac{1}{x-2}}')), m(L('1', r'\left(\dfrac{x+3}{4}\right)^{\frac{2}{x-1}}')), m(L('1', r'(2-x)^{\frac{x}{x-1}}'))])
     + recorda(r"La fórmula és la mateixa que a l'infinit: \ $\displaystyle\lim_{x\to a}f(x)^{g(x)}=e^{\lim\limits_{x\to a}(f(x)-1)\cdot g(x)}$."),
     tasks(2, [r'$3x\cdot\frac2x=6$: \ $\res{e^6}$', r'$(x-2)\cdot\frac{1}{x-2}=1$: \ $\res{e}$', r'$\frac{x-1}{4}\cdot\frac{2}{x-1}=\frac12$: \ $\res{e^{1/2}=\sqrt e}$', r'$(1-x)\cdot\frac{x}{x-1}=-x\to-1$: \ $\res{e^{-1}=\frac1e}$'])),
 (2, r"Calcula $\displaystyle\lim_{x\to1}\left(\frac{1}{x-1}-\frac{2}{x^2-1}\right)$. Quina indeterminació hi apareix?",
     r"En substituir: $\frac10-\frac20$, és a dir, $\infty-\infty$. \ Restem: $\frac{x+1-2}{x^2-1}=\frac{x-1}{(x-1)(x+1)}=\frac{1}{x+1}\to\res{\frac12}$."),
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
S_.append(("Continuïtat i tipus de discontinuïtat", [
 (1, r"Classifica les discontinuïtats d'aquestes gràfiques en el punt $x=c$:" + tasks(4, ['\\par' + g for g in TI])
     + recorda(r"$f$ és contínua en $x=c$ si $\exists f(c)$, $\exists\displaystyle\lim_{x\to c}f(x)$ i tots dos coincideixen. Si el límit existeix però falla alguna altra condició, la discontinuïtat és \textbf{evitable}; si els laterals són nombres diferents, de \textbf{salt finit}; si un lateral és infinit i l'altre un nombre, de \textbf{salt infinit}; si tots dos són infinits, \textbf{asimptòtica}."),
     tasks(4, [r'\rest{Asimptòtica}', r'\rest{Salt finit}', r'\rest{Evitable} ($f(c)\neq\lim$)', r'\rest{Evitable} ($\nexists f(c)$)'])),
 (1, r"Torna a la gràfica de $g$ de l'exercici \ref{ex:graf}. En quins punts no és contínua? Classifica cada discontinuïtat.",
     r"$x=-2$: un lateral és $-\infty$ i l'altre $-1$: \rest{salt infinit}. \ $x=1$: laterals $2$ i $3$: \rest{salt finit}. \ $x=3$: $\lim_{x\to3}g(x)=1\neq g(3)=-1$: \rest{evitable}. \ És contínua en la resta de punts."),
 (1, r"Estudia la continuïtat de cada funció en el punt indicat i, si és discontínua, digues de quin tipus és:" + tasks(2, [r'$f(x)=\dfrac{x^2-x}{x}$ \ en $x=0$', r'$g(x)=\dfrac{x+1}{x-2}$ \ en $x=2$',
     r'$h(x)=\begin{cases}x^2+1&\text{si }x<0\\x+1&\text{si }x\geq0\end{cases}$ \ en $x=0$', r'$k(x)=\begin{cases}x+2&\text{si }x\leq1\\\dfrac{1}{x-1}&\text{si }x>1\end{cases}$ \ en $x=1$',
     r'$p(x)=\begin{cases}\dfrac{x^2-4}{x-2}&\text{si }x\neq2\\[2pt]3&\text{si }x=2\end{cases}$ \ en $x=2$']),
     tasks(1, [r'$\nexists f(0)$; \ $\lim_{x\to0}\frac{x(x-1)}{x}=-1$: \ \rest{evitable}', r'$\nexists g(2)$; \ $\frac30$: $-\infty$ per l’esquerra i $+\infty$ per la dreta: \ \rest{asimptòtica}', r'$h(0)=1$, \ $\lim_{x\to0^-}=1$, \ $\lim_{x\to0^+}=1$: \ \rest{contínua}',
               r'$k(1)=3$, \ $\lim_{x\to1^-}(x+2)=3$, \ $\lim_{x\to1^+}\frac{1}{x-1}=+\infty$: \ \rest{salt infinit}', r'$p(2)=3$, \ $\lim_{x\to2}(x+2)=4\neq3$: \ \rest{evitable}'])),
 (2, r"Estudia la continuïtat de les funcions següents:" + tasks(2, [r'$f(x)=\dfrac{x^2-1}{x^2+x-2}$', r'$g(x)=\dfrac{x+3}{x^2+4}$', r'$h(x)=\dfrac{x}{x^2-4x}$', r'$k(x)=\sqrt{x-4}$'])
     + recorda(r"Les funcions racionals són contínues en tot $\mathbb R$ excepte on s'anul·la el denominador. En aquests punts, si el límit és un nombre la discontinuïtat és evitable i si és $\frac k0$, asimptòtica."),
     tasks(1, [r'$x^2+x-2=0\Rightarrow x=1,\ x=-2$. \ $x=1$: $\frac{(x-1)(x+1)}{(x-1)(x+2)}\to\frac23$: \rest{evitable}; \ $x=-2$: $\frac{3}{0}$: \rest{asimptòtica}. Contínua en $\mathbb R-\{-2,1\}$.', r'$x^2+4\neq0$: \ \rest{contínua en tot $\mathbb R$}.',
               r'$x(x-4)=0\Rightarrow x=0,\ x=4$. \ $x=0$: $\frac{1}{x-4}\to-\frac14$: \rest{evitable}; \ $x=4$: $\frac{4}{0}$: \rest{asimptòtica}.', r'Contínua on està definida: \ \rest{$[4,+\infty)$}.'])),
 (2, r"Indica si cadascuna de les funcions següents és contínua i on presenta discontinuïtats:" + tasks(2, [r'$f(x)=\dfrac{x^2+2x}{x+5}$', r'$g(x)=\dfrac{x^2+2x}{x}$', dm(pw(('1', 'x<3'), ('4', r'x\geq3'), name='h(x)')), dm(pw(('1', r'x\leq0'), (r'1-x^2', '0<x<2'), ('-3', r'x\geq2'), name='k(x)'))]),
     tasks(1, [r'No està definida en $x=-5$, on $\frac{15}{0}$: \ \rest{asimptòtica en $x=-5$}; contínua en $\mathbb R-\{-5\}$.', r'$g(x)=x+2$ si $x\neq0$ i no està definida en $0$: \ \rest{evitable en $x=0$}.',
               r'$\lim_{x\to3^-}h=1\neq\lim_{x\to3^+}h=4$: \ \rest{salt finit en $x=3$}; contínua en $\mathbb R-\{3\}$.', r'$x=0$: $1=1=k(0)$; \ $x=2$: $\lim_{x\to2^-}(1-x^2)=-3=k(2)$: \ \rest{contínua en tot $\mathbb R$}.'])),
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
S_.append(("Funcions a trossos. Paràmetres", [
 (2, r"Estudia la continuïtat de les funcions següents:" + tasks(1, [dm(pw((r'x-3', 'x<2'), (r'x^2-5', r'x\geq2'))), dm(pw((r'2x+1', 'x<0'), (r'x^2+1', r'0\leq x<2'), (r'\dfrac{3}{x-1}', r'x\geq2'), name='g(x)')),
     dm(pw((r'x^2', r'x\leq-1'), (r'\dfrac1x', r'-1<x<1'), (r'\sqrt x', r'x\geq1'), name='h(x)'))])
     + recorda(r"Primer, la continuïtat de cada tros en el seu interval (compte amb els denominadors i les arrels!). Després, en cada punt on es trenca la funció, comparem $f(a)$ i els dos límits laterals."),
     tasks(1, [r'Trossos polinòmics: contínues. \ $x=2$: $f(2)=-1$, $\lim_{x\to2^-}(x-3)=-1$, $\lim_{x\to2^+}(x^2-5)=-1$: \ \rest{contínua en $\mathbb R$}.',
               r'El denominador $x-1$ s’anul·la en $1$, fora de $x\geq2$. \ $x=0$: $1=1=g(0)$, contínua. \ $x=2$: $\lim_{x\to2^-}=5$, $\lim_{x\to2^+}=3=g(2)$: \ \rest{salt finit en $x=2$}.',
               r'$\frac1x$ no està definida en $x=0$, que és del seu interval: $-\infty$ i $+\infty$, \rest{asimptòtica en $x=0$}. \ $x=-1$: $h(-1)=1$, laterals $1$ i $-1$: \rest{salt finit}. \ $x=1$: $h(1)=1$, laterals $1$ i $1$: contínua.'])),
 (2, r"Escriu $f(x)=\dfrac{|x^2-4|}{x-2}$ com una funció a trossos i estudia'n la continuïtat en $x=2$.",
     r"$x^2-4<0$ si $-2<x<2$. \ Per a $x>2$: $f(x)=\frac{(x-2)(x+2)}{x-2}=x+2\to4$; \ per a $-2<x<2$: $f(x)=-(x+2)\to-4$. \ $\nexists f(2)$ i els laterals són $-4$ i $4$: \ \rest{salt finit en $x=2$}."),
 (2, r"Calcula $m$ perquè aquesta funció siga contínua en tot $\mathbb R$:" + dm(pw((r'x^2-3', r'x\leq2'), (r'-x^2+m', 'x>2')))
     + recorda(r"Si la funció depén d'un paràmetre, \textbf{igualem els límits laterals} en el punt on es trenca i resolem l'equació."),
     r"$\lim_{x\to2^-}(x^2-3)=1=f(2)$; \ $\lim_{x\to2^+}(-x^2+m)=-4+m$. \ $-4+m=1\Rightarrow\res{m=5}$."),
 (2, r"Troba el valor del paràmetre perquè cada funció siga contínua en tot $\mathbb R$:" + tasks(1, [dm(pw((r'ax+3', 'x<1'), (r'x^2-a', r'x\geq1'))), dm(pw((r'\dfrac{x^2-9}{x-3}', r'x\neq3'), ('k', 'x=3'), name='g(x)')),
     dm(pw((r'2^x+a', r'x\leq0'), (r'\dfrac{x+4}{x+2}', 'x>0'), name='h(x)'))]),
     tasks(1, [r'$a+3=1-a\Rightarrow\res{a=-1}$', r'$\lim_{x\to3}(x+3)=6\Rightarrow\res{k=6}$', r'$1+a=\frac42=2\Rightarrow\res{a=1}$ \ (el denominador $x+2$ s’anul·la en $-2$, fora de $x>0$)'])),
 (3, r"Troba $a$ i $b$ perquè la funció següent siga contínua en tot $\mathbb R$:" + dm(pw((r'x+a', 'x<0'), (r'bx+1', r'0\leq x\leq2'), (r'x^2-a', 'x>2'))),
     r"$x=0$: $a=1$. \ $x=2$: $2b+1=4-a=3\Rightarrow b=1$. \ $\res{a=1,\ b=1}$"),
 (2, r"Un taxi cobra $P(x)=3+1{,}5x$ euros per un viatge de $x\leq10$ km i $P(x)=ax+8$ si $x>10$ km. Quant ha de valer $a$ perquè el preu no faça cap salt en els 10 km? Quant costa, llavors, un viatge de 25 km?",
     r"$\lim_{x\to10^-}P(x)=3+15=18$ i $\lim_{x\to10^+}P(x)=10a+8$: \ $10a+8=18\Rightarrow\res{a=1}$ €/km. \ $P(25)=25+8=\res{33\text{ €}}$."),
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
S_.append(("Branques infinites i asímptotes", [
 (2, r"Troba les branques infinites de les funcions següents. Si hi ha asímptotes, estudia la posició de la corba respecte d'elles:" + tasks(3, [r'$f(x)=\dfrac{x^2-1}{x^2+4}$', r'$g(x)=\dfrac{x}{(x-1)^2}$', r'$h(x)=\dfrac{2x^2}{x-3}$'])
     + recorda(r"AV: on el límit és infinit ($\frac k0$). \ AH: $\displaystyle\lim_{x\to\pm\infty}f(x)=b$. \ AO en una racional quan el grau de dalt és una unitat més gran: l'asímptota és el quocient de la divisió. La posició es veu amb el signe de $f(x)$ menys l'asímptota."),
     tasks(1, [r'Cap AV ($x^2+4\neq0$). \ AH $\res{y=1}$: \ $f(x)-1=\frac{-5}{x^2+4}<0$, la corba queda \rest{per davall}. No té AO.',
               r'AV $\res{x=1}$: $\frac{1}{0^+}$, $+\infty$ pels dos costats. \ AH $\res{y=0}$: per damunt si $x\to+\infty$ ($g>0$) i per davall si $x\to-\infty$. No té AO.',
               r'AV $\res{x=3}$: $-\infty$ per l’esquerra i $+\infty$ per la dreta. \ No té AH. \ $2x^2=(x-3)(2x+6)+18$: \ AO $\res{y=2x+6}$; \ $\frac{18}{x-3}$: per damunt si $x\to+\infty$ i per davall si $x\to-\infty$.'])),
 (2, r"Calcula totes les asímptotes de les funcions següents i estudia els límits laterals en cada asímptota vertical:" + tasks(2, [r'$f(x)=\dfrac{3x+1}{x-2}$', r'$f(x)=\dfrac{x^2}{x^2-4}$', r'$f(x)=\dfrac{x+1}{x^2-1}$', r'$f(x)=\dfrac{x^2+x+1}{x-1}$', r'$f(x)=\dfrac{x^3+1}{x^2}$', r'$f(x)=\dfrac{3\cdot2^x}{2^x+1}$']),
     tasks(1, [r'AV $\res{x=2}$ ($-\infty$ per l’esquerra, $+\infty$ per la dreta); AH $\res{y=3}$ ($f(x)-3=\frac{7}{x-2}$: per damunt a la dreta i per davall a l’esquerra).',
               r'AV $\res{x=-2}$ ($+\infty$ per l’esquerra, $-\infty$ per la dreta) i $\res{x=2}$ ($-\infty$ per l’esquerra, $+\infty$ per la dreta); AH $\res{y=1}$.',
               r'En $x=-1$: $\frac00$, $\frac{1}{x-1}\to-\frac12$: no hi ha AV (forat). \ AV $\res{x=1}$ ($-\infty$ per l’esquerra, $+\infty$ per la dreta); AH $\res{y=0}$.',
               r'AV $\res{x=1}$ ($-\infty$ per l’esquerra, $+\infty$ per la dreta). \ $x^2+x+1=(x-1)(x+2)+3$: AO $\res{y=x+2}$.',
               r'AV $\res{x=0}$ ($\frac{1}{0^+}$: $+\infty$ pels dos costats). \ $f(x)=x+\frac{1}{x^2}$: AO $\res{y=x}$, i la corba queda sempre per damunt.',
               r'No és racional: \ $\lim_{x\to+\infty}\frac{3\cdot2^x}{2^x}=3$ i $\lim_{x\to-\infty}\frac{3\cdot0}{0+1}=0$: \ AH $\res{y=3}$ per la dreta i $\res{y=0}$ per l’esquerra. No té AV.'])),
 (3, r"Calcula les asímptotes obliqües de $f(x)=\sqrt{x^2+4x}$ amb els límits $m=\displaystyle\lim\frac{f(x)}{x}$ i $n=\displaystyle\lim\,[f(x)-mx]$. Fes-ho quan $x\to+\infty$ i quan $x\to-\infty$.",
     r"$x\to+\infty$: $m=\lim\frac{\sqrt{x^2+4x}}{x}=1$, \ $n=\lim(\sqrt{x^2+4x}-x)=\lim\frac{4x}{\sqrt{x^2+4x}+x}=2$: \ $\res{y=x+2}$. \ \ $x\to-\infty$: $\sqrt{x^2}=-x$, $m=-1$, \ $n=\lim(\sqrt{x^2+4x}+x)=\lim\frac{4x}{\sqrt{x^2+4x}-x}=\frac{4x}{-2x}=-2$: \ $\res{y=-x-2}$."),
 (2, r"Quines d'aquestes funcions tenen branques parabòliques quan $x\to+\infty$? Justifica-ho calculant $\lim f(x)$ i $m=\lim\frac{f(x)}{x}$." + tasks(4, [r'$f(x)=x^3-3x$', r'$g(x)=\ln x$', r'$h(x)=\dfrac{x^3}{x-1}$', r'$k(x)=\dfrac{x^2+1}{x}$']),
     tasks(1, [r'$\lim f=+\infty$, $m=\lim(x^2-3)=+\infty$: \ \rest{branca parabòlica}', r'$\lim g=+\infty$, $m=\lim\frac{\ln x}{x}=0$: \ \rest{branca parabòlica}', r'$\lim h=+\infty$, $m=\lim\frac{x^2}{x-1}=+\infty$: \ \rest{branca parabòlica}', r'$k(x)=x+\frac1x$: \ \rest{asímptota obliqua $y=x$}, no és branca parabòlica'])),
 (3, r"Troba $a$, $b$ i $c$ perquè la funció $f(x)=\dfrac{ax+b}{x+c}$ tinga una asímptota vertical en $x=-2$, una asímptota horitzontal en $y=3$ i passe pel punt $(0,1)$.",
     r"AV $x=-2$: el denominador s'anul·la en $-2$: $c=2$. \ AH: $\displaystyle\lim_{x\to\pm\infty}\frac{ax+b}{x+2}=a=3$. \ Punt: $f(0)=\frac b2=1\Rightarrow b=2$. \ $\res{a=3,\ b=2,\ c=2}$"),
]))
C(lambda t: (3 * t + 2) / (t + 2), I, 3); C(lambda t: (3 * t + 2) / (t + 2), -2, I, -1)
C(lambda t: (t * t + 1) / t - t, I, 0)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={límits, límits a l'infinit, comparació d'infinits, indeterminacions, límits laterals, continuïtat, tipus de discontinuïtat, funcions a trossos, paràmetres, asímptotes, branques parabòliques}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
pre += r'''\providecommand{\gt}{>}\providecommand{\lt}{<}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def fix(t):
    """Fora dels dibuixos: l'espai després de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = "Límits i continuïtat"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 8: %s. 1r de Batxillerat MI}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 8: %s · 1r Batxillerat MI" % (t, TIT))
    assert 'continuïtat · 1r' in p and 'unitat 8: Límits' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques I}{1r Batx}{''' + ('Solucions de la fitxa · Unitat 8' if sol else "Fitxa d'exercicis · Unitat 8") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb la calculadora de límits dels apunts interactius de la unitat."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos: abans de transformar una expressió, substitueix i comprova si hi ha de veritat una indeterminació. Les seccions segueixen l'ordre dels apunts. Pots comprovar els resultats amb la calculadora de límits dels apunts interactius.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb la calculadora de límits dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't8-fitxa-solucions.tex' if sol else 't8-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis;', NCHK[0], 'comprovacions')
