# Genera t5-fitxa-exercicis.tex i t5-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 5: Límits i continuïtat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les estrelles no es mostren.
# Les seccions segueixen els apunts interactius (materials/2batx-mii/t5-limits-continuitat.html). Al final de cada secció hi ha
# exercicis de la PAU de Matemàtiques II de 16 comunitats autònomes (2017-2026), traduïts al valencià i presos del recull
# «Ejercicios de análisis en pruebas de acceso a la universidad de toda España» (ebaumatematicas.com, curs 2026/27); se n'han
# llevat els apartats de derivades, integrals i els límits que necessiten la regla de L'Hôpital (no s'expliquen en aquesta unitat).
# Tots els límits i paràmetres de les solucions es comproven numèricament (mpmath, 150 xifres) abans d'escriure els fitxers.
# Ús: python3 genera.py && pdflatex t5-fitxa-exercicis.tex (dues vegades) && pdflatex t5-fitxa-solucions.tex (dues vegades)
import os, re
import mpmath as M
M.mp.dps = 150
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
sq, ln, ex, sin, cos, tan, pi, E = M.sqrt, M.log, M.exp, M.sin, M.cos, M.tan, M.pi, M.e
INF = M.inf
rc = lambda x: M.sign(x) * M.cbrt(abs(x))
NCHK = [0]
def lim(f, a, side=1, slow=False):
    if a == INF or a == -INF:
        xs = [M.mpf(10) ** k * (1 if a > 0 else -1) for k in ((10 ** 6, 10 ** 7, 10 ** 8) if slow else (24, 32, 40))]
    else:
        xs = [M.mpf(a) + side * M.mpf(10) ** -k for k in (12, 16, 20)]
    return [f(x) for x in xs]
def chk(f, a, exp, side=None, slow=False):
    """exp: nombre, INF o -INF; side None = pels dos costats (o a l'infinit)."""
    sides = [1] if (a in (INF, -INF) or side == 1) else [-1] if side == -1 else [-1, 1]
    for s in sides:
        v = lim(f, a, s, slow)
        if exp == INF: ok = v[-1] > 40 and v[-1] > v[1] > v[0]          # infinits lents (logaritmes) inclosos
        elif exp == -INF: ok = v[-1] < -40 and v[-1] < v[1] < v[0]
        else: ok = abs(v[-1] - exp) < M.mpf(10) ** -6 * (1 + abs(exp))
        assert ok, (a, s, exp, [M.nstr(x, 8) for x in v])
        NCHK[0] += 1
def eq(a, b, tol=1e-12):
    assert abs(M.mpf(a) - M.mpf(b)) <= tol * (1 + abs(M.mpf(b))), (M.nstr(a, 15), M.nstr(b, 15))
    NCHK[0] += 1
def ck(c, *msg):
    assert c, msg
    NCHK[0] += 1

S = []  # [(títol, [(estrelles, enunciat, solució)])]
def sec(t, *exs): S.append((t, list(exs)))

# =====================================================================
# 1. Límits a l'infinit
for f, a, v in [(lambda x: 2*x**5 - x**2, -INF, -INF), (lambda x: (4*x**3 - x)/(2*x**3 + 7), INF, 2), (lambda x: (1 - 3*x**2)/(x + 2), -INF, INF),
                (lambda x: (x**2 + 1)/(x**3 - 2), INF, 0), (lambda x: (2**(x + 1) + 5)/(2**x - 3), INF, 2), (lambda x: (3*ex(2*x) - ex(x))/(ex(2*x) + 4), -INF, 0),
                (lambda x: sq(9*x**2 + 1)/(2*x - 5), INF, M.mpf(3)/2), (lambda x: sq(9*x**2 + 1)/(2*x - 5), -INF, -M.mpf(3)/2), (lambda x: (3*x + sq(x**2 + 5))/(2*x + 1), -INF, 1),
                (lambda x: rc(8*x**3 - 1)/x, -INF, 2), (lambda x: sq(x**3 + x)/(x + 4), INF, INF), (lambda x: sq(x**2 - 5*x + 3)/(3*x - 2), -INF, -M.mpf(1)/3),
                (lambda x: x**3/ex(x), INF, 0), (lambda x: ln(x)/x**2, INF, 0), (lambda x: (2**x + x**4)/(3*2**x), INF, M.mpf(1)/3), (lambda x: x**10 - M.mpf(1.5)**x, INF, -INF),
                (lambda x: (3**x + 2**x)/(3**x - x**2), INF, 1), (lambda x: ln(x)**3/sq(x), INF, 0), (lambda x: ln(2*x + 1) - ln(x + 3), INF, ln(2)), (lambda x: ln(x**2 + 1) - ln(x), INF, INF),
                (lambda x: x**2/(ex(x) + ex(-x)), INF, 0)]:
    chk(f, a, v)
sec("Límits a l'infinit",
 (2, r"Calcula els límits següents:" + tasks(3, [m(L(MI, r'(2x^5-x^2)')), m(L(PI, r'\dfrac{4x^3-x}{2x^3+7}')), m(L(MI, r'\dfrac{1-3x^2}{x+2}')), m(L(PI, r'\dfrac{x^2+1}{x^3-2}')), m(L(PI, r'\dfrac{2^{x+1}+5}{2^{x}-3}')), m(L(MI, r'\dfrac{3e^{2x}-e^{x}}{e^{2x}+4}'))])
     + recorda(r"Quan $x\to\pm\infty$, en un quocient de polinomis manen els termes de major grau. Amb exponencials, dividim per l'exponencial que creix més de pressa (i recorda que $e^{x}\to0$ quan $x\to-\infty$)."),
     tasks(3, [r'$\lim 2x^5=\res{-\infty}$', r'$\frac42=\res{2}$', r'$\lim(-3x)=\res{+\infty}$', r'$\res{0}$', r'$\lim\frac{2+5\cdot2^{-x}}{1-3\cdot2^{-x}}=\res{2}$', r'$\frac{0-0}{0+4}=\res{0}$'])),
 (2, r"Calcula els límits següents amb arrels. Compte amb el signe quan $x\to-\infty$:" + tasks(3, [m(L(PI, r'\dfrac{\sqrt{9x^2+1}}{2x-5}')), m(L(MI, r'\dfrac{\sqrt{9x^2+1}}{2x-5}')), m(L(MI, r'\dfrac{3x+\sqrt{x^2+5}}{2x+1}')), m(L(MI, r'\dfrac{\sqrt[3]{8x^3-1}}{x}')), m(L(PI, r'\dfrac{\sqrt{x^3+x}}{x+4}')), m(L(MI, r'\dfrac{\sqrt{x^2-5x+3}}{3x-2}'))])
     + recorda(r"$\sqrt{x^2}=|x|$: quan $x\to-\infty$, $\sqrt{a x^2+\dots}\approx-\sqrt a\,x$. Si dubtes, fes el canvi $x=-t$ amb $t\to+\infty$."),
     tasks(3, [r'$\frac{3x}{2x}\to\res{\frac32}$', r'$\frac{-3x}{2x}\to\res{-\frac32}$', r'$\frac{3x-x}{2x}\to\res{1}$', r'$\frac{2x}{x}\to\res{2}$', r'$\frac{x^{3/2}}{x}=\sqrt x\to\res{+\infty}$', r'$\frac{-x}{3x}\to\res{-\frac13}$'])),
 (2, r"Ordena de menor a major ordre d'infinit (quan $x\to+\infty$) \ $x^3,\ 2^x,\ \ln x,\ \sqrt x,\ e^x,\ x^{10},\ (\ln x)^3$, \ i calcula:" + tasks(3, [m(L(PI, r'\dfrac{x^3}{e^x}')), m(L(PI, r'\dfrac{\ln x}{x^2}')), m(L(PI, r'\dfrac{2^x+x^4}{3\cdot2^x}')), m(L(PI, r'\left(x^{10}-1{,}5^x\right)')), m(L(PI, r'\dfrac{3^x+2^x}{3^x-x^2}')), m(L(PI, r'\dfrac{(\ln x)^3}{\sqrt x}'))]),
     r"$\res{\ln x\ll(\ln x)^3\ll\sqrt x\ll x^3\ll x^{10}\ll2^x\ll e^x}$ (qualsevol potència de $\ln x$ és menor que qualsevol potència de $x$)." + tasks(3, [r'$\res{0}$', r'$\res{0}$', r'$\frac{2^x}{3\cdot 2^x}\to\res{\frac13}$', r'$\res{-\infty}$', r'$\frac{3^x}{3^x}\to\res{1}$', r'$\res{0}$'])),
 (2, r"Calcula, fent servir les propietats dels logaritmes:" + tasks(2, [m(L(PI, r'\big(\ln(2x+1)-\ln(x+3)\big)')), m(L(PI, r'\big(\ln(x^2+1)-\ln x\big)'))]),
     tasks(2, [r'$\lim\ln\frac{2x+1}{x+3}=\res{\ln2}$', r'$\lim\ln\frac{x^2+1}{x}=\ln(+\infty)=\res{+\infty}$'])),
 (2, r"\pau{Andalusia, ordinària 2023} Considera la funció $f(x)=\dfrac{1}{e^x+e^{-x}}$. Calcula $\displaystyle\lim_{x\to+\infty}x^2f(x)$.",
     r"$\displaystyle\lim_{x\to+\infty}\frac{x^2}{e^x+e^{-x}}=\res{0}$: l'exponencial és un infinit d'ordre superior a $x^2$."),
)

# =====================================================================
# 2. Indeterminacions a l'infinit
for f, a, v in [(lambda x: x**2/(x + 1) - x, INF, -1), (lambda x: x**3/(x**2 + 1) - x**2/(x + 1), INF, 1), (lambda x: sq(x**2 + 8*x) - x, INF, 4), (lambda x: sq(x**2 + 3*x) - sq(x**2 - x), INF, 2),
                (lambda x: sq(x**2 + 2*x) + x, -INF, -1), (lambda x: rc(x**3 + 3*x**2) - x, INF, 1), (lambda x: sq(x**2 + 1) - 3*x, INF, -INF),
                (lambda x: x*(sq(x**2 + 4) - x), INF, 2), (lambda x: (2*x + 1)*(sq(x + 1) - sq(x)), INF, INF), (lambda x: x*ln(1 + 2/x), INF, 2), (lambda x: x**3*ex(-x), INF, 0),
                (lambda x: ((x + 2)/(x - 1))**(2*x), INF, ex(6)), (lambda x: ((2*x - 1)/(2*x + 3))**(x + 1), INF, ex(-2)), (lambda x: ((x**2 + 3)/(x**2 - 1))**(x**2), INF, ex(4)),
                (lambda x: ((3*x + 1)/(x + 2))**x, INF, INF), (lambda x: ((x - 4)/x)**(3*x), -INF, ex(-12)), (lambda x: ((x**2 - x + 1)/(x**2 + 2))**((x**2 + 1)/(x - 3)), INF, ex(-1)),
                (lambda x: x**(1/x), INF, 1),
                (lambda x: sq(x**2 + 5) - (x + 2), INF, -2), (lambda x: sq(3*x**2 - 2) - (sq(3)*x + 5), INF, -5), (lambda x: ((5*x + 1)/(5*x))**(x**2), INF, INF),
                (lambda x: (x**2/(x**2 + x - 1))**(2*x - 1), INF, ex(-2)), (lambda x: sq(x)/(sq(3*x**3 + 2*x**2) - sq(3*x**3)), INF, sq(3)), (lambda x: (1 + x)**(1/x), INF, 1),
                (lambda t: (15 + t**2)/(t + 1)**2, INF, 1), (lambda x: sq(x + 9) - sq(x - 9), INF, 0), (lambda x: ln(x)/sq(x), INF, 0)]:
    chk(f, a, v)
eq((15 + 0)/(0 + 1)**2, 15); chk(lambda x: (3*x)**(2/ln(x)), INF, ex(2), slow=True)
sec("Indeterminacions a l'infinit",
 (2, r"Indeterminació $\infty-\infty$:" + tasks(3, [m(L(PI, r'\left(\dfrac{x^2}{x+1}-x\right)')), m(L(PI, r'\left(\dfrac{x^3}{x^2+1}-\dfrac{x^2}{x+1}\right)')), m(L(PI, r'\left(\sqrt{x^2+8x}-x\right)')), m(L(PI, r'\left(\sqrt{x^2+3x}-\sqrt{x^2-x}\right)')), m(L(MI, r'\left(\sqrt{x^2+2x}+x\right)')), m(L(PI, r'\left(\sqrt{x^2+1}-3x\right)'))])
     + recorda(r"Amb fraccions, fem la resta. Amb arrels, multipliquem i dividim pel \textbf{conjugat}. Abans, comprova si els termes principals es cancel·len: si no ho fan, no hi ha indeterminació real."),
     tasks(2, [r'$\dfrac{-x}{x+1}\to\res{-1}$', r'$\dfrac{x^3-x^2}{x^3+x^2+x+1}\to\res{1}$', r'$\dfrac{8x}{\sqrt{x^2+8x}+x}\to\dfrac{8x}{2x}=\res{4}$', r'$\dfrac{4x}{\sqrt{x^2+3x}+\sqrt{x^2-x}}\to\res{2}$', r'$x=-t$: \ $\dfrac{-2t}{\sqrt{t^2-2t}+t}\to\res{-1}$', r'$x-3x=-2x\to\res{-\infty}$'])),
 (3, r"Calcula $\displaystyle\lim_{x\to+\infty}\left(\sqrt[3]{x^3+3x^2}-x\right)$. \ \textit{Indicació}: $A^3-B^3=(A-B)(A^2+AB+B^2)$.",
     r"Amb $A=\sqrt[3]{x^3+3x^2}$, $B=x$: \ $\dfrac{A^3-B^3}{A^2+AB+B^2}=\dfrac{3x^2}{A^2+Ax+x^2}\to\dfrac{3x^2}{3x^2}=\res{1}$"),
 (2, r"Indeterminació $0\cdot\infty$:" + tasks(2, [m(L(PI, r'x\left(\sqrt{x^2+4}-x\right)')), m(L(PI, r'(2x+1)\left(\sqrt{x+1}-\sqrt x\right)')), m(L(PI, r'x\ln\left(1+\dfrac2x\right)')), m(L(PI, r'x^3e^{-x}'))])
     + recorda(r"Transformem el producte en un quocient ($f\cdot g=\frac{f}{1/g}$) o operem. Un exponent es pot posar dins del logaritme: $x\ln A=\ln A^{x}$."),
     tasks(2, [r'$\dfrac{4x}{\sqrt{x^2+4}+x}\to\res{2}$', r'$\dfrac{2x+1}{\sqrt{x+1}+\sqrt x}\approx\sqrt x\to\res{+\infty}$', r'$\ln\left(1+\frac2x\right)^x\to\ln e^2=\res{2}$', r'$\dfrac{x^3}{e^x}\to\res{0}$'])),
 (2, r"Indeterminació $1^{\infty}$:" + tasks(3, [m(L(PI, r'\left(\dfrac{x+2}{x-1}\right)^{2x}')), m(L(PI, r'\left(\dfrac{2x-1}{2x+3}\right)^{x+1}')), m(L(PI, r'\left(\dfrac{x^2+3}{x^2-1}\right)^{x^2}')), m(L(PI, r'\left(\dfrac{3x+1}{x+2}\right)^{x}')), m(L(MI, r'\left(\dfrac{x-4}{x}\right)^{3x}')), m(L(PI, r'\left(\dfrac{x^2-x+1}{x^2+2}\right)^{\frac{x^2+1}{x-3}}'))])
     + recorda(r"Si $f\to1$ i $g\to\pm\infty$: \ $\lim f^{\,g}=e^{\lim\,(f-1)\,g}$. Si la base no tendeix a 1, no hi ha indeterminació."),
     tasks(2, [r'$e^{\lim\frac{3}{x-1}\cdot2x}=\res{e^6}$', r'$e^{\lim\frac{-4(x+1)}{2x+3}}=\res{e^{-2}}$', r'$e^{\lim\frac{4x^2}{x^2-1}}=\res{e^4}$', r'$3^{+\infty}=\res{+\infty}$ (no és $1^\infty$)', r'$e^{\lim\frac{-4}{x}\cdot3x}=\res{e^{-12}}$', r'$e^{\lim\frac{(-x-1)(x^2+1)}{(x^2+2)(x-3)}}=\res{e^{-1}}$'])),
 (3, r"Indeterminacions $\infty^0$. Calcula prenent logaritmes:" + tasks(2, [m(L(PI, r'x^{1/x}')), m(L(PI, r'(3x)^{\frac{2}{\ln x}}'))]),
     tasks(2, [r'$\ln L=\lim\frac{\ln x}{x}=0\Rightarrow L=\res{1}$', r'$\ln L=\lim\frac{2\ln3+2\ln x}{\ln x}=2\Rightarrow L=\res{e^2}$'])),
 (2, r"\pau{Aragó, ordinària 2024} Calcula justificadament $\displaystyle\lim_{x\to+\infty}\left[\sqrt{x^2+5}-(x+2)\right]$.",
     r"$\dfrac{x^2+5-(x+2)^2}{\sqrt{x^2+5}+x+2}=\dfrac{-4x+1}{\sqrt{x^2+5}+x+2}\to\dfrac{-4x}{2x}=\res{-2}$"),
 (2, r"\pau{Aragó, ordinària 2022} Calcula $\displaystyle\lim_{x\to+\infty}\left[\sqrt{3x^2-2}-\left(\sqrt3\,x+5\right)\right]$.",
     r"$\dfrac{3x^2-2-(\sqrt3x+5)^2}{\sqrt{3x^2-2}+\sqrt3x+5}=\dfrac{-10\sqrt3\,x-27}{\sqrt{3x^2-2}+\sqrt3x+5}\to\dfrac{-10\sqrt3\,x}{2\sqrt3\,x}=\res{-5}$"),
 (2, r"\pau{Navarra, extraordinària 2021} Calcula $\displaystyle\lim_{x\to+\infty}\dfrac{\sqrt x}{\sqrt{3x^3+2x^2}-\sqrt{3x^3}}$.",
     r"Pel conjugat: $\dfrac{\sqrt x\left(\sqrt{3x^3+2x^2}+\sqrt{3x^3}\right)}{2x^2}\approx\dfrac{\sqrt x\cdot2\sqrt3\,x^{3/2}}{2x^2}\to\res{\sqrt3}$"),
 (2, r"\pau{Múrcia, ordinària 2024} Calcula:" + tasks(2, [m(L(PI, r'\left(\sqrt{x+9}-\sqrt{x-9}\right)')), m(L(PI, r'\dfrac{\ln x}{\sqrt x}'))]),
     tasks(2, [r'$\dfrac{18}{\sqrt{x+9}+\sqrt{x-9}}\to\res{0}$', r'$\res{0}$ (comparació d\'infinits)'.replace("d\\'", "d’")])),
 (2, r"\pau{Castella-la Manxa, ordinària 2023} Calcula $\displaystyle\lim_{x\to+\infty}\left(\dfrac{5x+1}{5x}\right)^{x^2}$.",
     r"$1^\infty$: \ $e^{\lim\frac{1}{5x}\cdot x^2}=e^{+\infty}=\res{+\infty}$"),
 (2, r"\pau{Navarra, extraordinària 2022} Calcula $\displaystyle\lim_{x\to+\infty}\left(\dfrac{x^2}{x^2+x-1}\right)^{2x-1}$.",
     r"$\dfrac{x^2}{x^2+x-1}-1=\dfrac{1-x}{x^2+x-1}$; \ $\lim\dfrac{(1-x)(2x-1)}{x^2+x-1}=-2$: \ $\res{e^{-2}}$"),
 (2, r"\pau{La Rioja, extraordinària 2023} Calcula $\displaystyle\lim_{x\to+\infty}(1+x)^{1/x}$.",
     r"$\infty^0$: \ $\ln L=\lim\dfrac{\ln(1+x)}{x}=0$ (comparació d'infinits) $\Rightarrow L=\res{1}$"),
 (2, r"\pau{Illes Balears, extraordinària 2021} El nombre d'individus, en milions, d'una població és $P(t)=\dfrac{15+t^2}{(t+1)^2}$, on $t\geq0$ són els anys transcorreguts des de l'1 de gener del 2000." + tasks(1, [r"Quina població hi havia l'1 de gener del 2000?", r"Calcula la mida de la població a llarg termini."]),
     tasks(1, [r"$P(0)=\res{15}$ milions", r"$\displaystyle\lim_{t\to+\infty}P(t)=\res{1}$ milió d'individus"])),
)

# =====================================================================
# 3. Límits en un nombre
f3 = lambda x: (x + 1)/(x - 2)**2
chk(f3, 2, INF); chk(lambda x: (x - 3)/(x**3 - 5*x**2 + 3*x + 9), 3, -INF, -1); chk(lambda x: (x - 3)/(x**3 - 5*x**2 + 3*x + 9), 3, INF, 1)
for f, a, v in [(lambda x: (x**3 - 8)/(x - 2), 2, 12), (lambda x: (x**4 - 1)/(x**2 - x), 1, 4), (lambda x: (x**4 - 4*x**3 + 16*x - 16)/(x**3 - 6*x**2 + 12*x - 8), 2, 4),
                (lambda x: (sq(x + 5) - 3)/(x - 4), 4, M.mpf(1)/6), (lambda x: (sq(x + 1) - sq(2*x - 2))/(x**2 - 9), 3, -M.mpf(1)/24), (lambda x: (sq(1 + x) - 1)/(sq(4 + x) - 2), 0, 2),
                (lambda x: 1/(x - 1) - 2/(x**2 - 1), 1, M.mpf(1)/2), (lambda x: x/(x - 2) - 8/(x**2 - 4), 2, M.mpf(3)/2),
                (lambda x: (1 + 3*x)**(2/x), 0, ex(6)), (lambda x: ((x + 2)/(2*x))**(1/(x - 2)), 2, ex(-M.mpf(1)/4)), (lambda x: x**(3/(x - 1)), 1, ex(3)), (lambda x: (2*x - 1)**(1/(x - 1)), 1, ex(2)),
                (lambda x: (x**3 + 2*x**2 + x + 2)/(x**2 + 2*x), -2, -M.mpf(5)/2), (lambda x: (x**3 - 3*x**2 + 3*x - 9)/(3*x - 9), 3, 4),
                (lambda x: (sq(x**3 + x - 1) - sq(x**3 + 1))/(x - 2), 2, M.mpf(1)/6), (lambda x: (sq(9 + x) - sq(9 - x))/(3*x), 0, M.mpf(1)/9)]:
    chk(f, a, v)
eq((2 + 3)*(4 + 1), 25)  # x^4-4x^3+16x-16 = (x-2)^3(x+2)
for x in (-1.5, 0.3, 2.7, 5):
    eq(x**4 - 4*x**3 + 16*x - 16, (x - 2)**3*(x + 2)); eq(x**3 - 5*x**2 + 3*x + 9, (x - 3)**2*(x + 1)); eq(x**3 + 2*x**2 + x + 2, (x + 2)*(x**2 + 1))
sec("Límits en un nombre i indeterminacions",
 (2, r"Calcula els límits laterals i digues si existeix el límit:" + tasks(2, [m(L('2', r'\dfrac{x+1}{(x-2)^2}')), m(L('3', r'\dfrac{x-3}{x^3-5x^2+3x+9}'))]),
     tasks(1, [r"$\frac{3}{0^+}$ pels dos costats: \ $\res{+\infty}$", r"$x^3-5x^2+3x+9=(x-3)^2(x+1)$: \ $\dfrac{1}{(x-3)(x+1)}$; \ $\lim_{x\to3^-}=\res{-\infty}$, \ $\lim_{x\to3^+}=\res{+\infty}$: \ $\res{\nexists}$ el límit"])),
 (2, r"Indeterminació $\frac00$ amb polinomis:" + tasks(3, [m(L('2', r'\dfrac{x^3-8}{x-2}')), m(L('1', r'\dfrac{x^4-1}{x^2-x}')), m(L('2', r'\dfrac{x^4-4x^3+16x-16}{x^3-6x^2+12x-8}'))])
     + recorda(r"Si $P(a)=Q(a)=0$, tots dos són divisibles per $(x-a)$: factoritzem (Ruffini), simplifiquem i tornem a substituir."),
     tasks(1, [r'$x^2+2x+4\to\res{12}$', r'$\dfrac{(x-1)(x+1)(x^2+1)}{x(x-1)}\to\res{4}$', r'$\dfrac{(x-2)^3(x+2)}{(x-2)^3}=x+2\to\res{4}$'])),
 (2, r"Indeterminació $\frac00$ amb arrels:" + tasks(3, [m(L('4', r'\dfrac{\sqrt{x+5}-3}{x-4}')), m(L('3', r'\dfrac{\sqrt{x+1}-\sqrt{2x-2}}{x^2-9}')), m(L('0', r'\dfrac{\sqrt{1+x}-1}{\sqrt{4+x}-2}'))]),
     tasks(1, [r'$\dfrac{x-4}{(x-4)(\sqrt{x+5}+3)}\to\res{\frac16}$', r'$\dfrac{-(x-3)}{(x-3)(x+3)\left(\sqrt{x+1}+\sqrt{2x-2}\right)}\to\dfrac{-1}{6\cdot4}=\res{-\frac{1}{24}}$', r'$\dfrac{x\left(\sqrt{4+x}+2\right)}{x\left(\sqrt{1+x}+1\right)}\to\res{2}$'])),
 (2, r"Indeterminacions $\infty-\infty$ i $1^\infty$ en un nombre:" + tasks(3, [m(L('1', r'\left(\dfrac{1}{x-1}-\dfrac{2}{x^2-1}\right)')), m(L('2', r'\left(\dfrac{x}{x-2}-\dfrac{8}{x^2-4}\right)')), m(L('0', r'(1+3x)^{2/x}')), m(L('2', r'\left(\dfrac{x+2}{2x}\right)^{\frac{1}{x-2}}')), m(L('1', r'x^{\frac{3}{x-1}}')), m(L('1', r'(2x-1)^{\frac{1}{x-1}}'))]),
     tasks(2, [r'$\dfrac{x-1}{(x-1)(x+1)}\to\res{\frac12}$', r'$\dfrac{(x-2)(x+4)}{(x-2)(x+2)}\to\res{\frac32}$', r'$e^{\lim3x\cdot\frac2x}=\res{e^6}$', r'$e^{\lim\frac{-1}{2x}}=\res{e^{-1/4}}$', r'$e^{\lim\frac{3(x-1)}{x-1}}=\res{e^3}$', r'$e^{\lim\frac{2(x-1)}{x-1}}=\res{e^2}$'])),
 (2, r"\pau{Castella-la Manxa, extraordinària 2024} Calcula $\displaystyle\lim_{x\to-2}\dfrac{x^3+2x^2+x+2}{x^2+2x}$.",
     r"$\dfrac{(x+2)(x^2+1)}{x(x+2)}=\dfrac{x^2+1}{x}\to\res{-\dfrac52}$"),
 (2, r"\pau{Castella-la Manxa, extraordinària 2023} Calcula $\displaystyle\lim_{x\to3}\dfrac{x^3-3x^2+3x-9}{3x-9}$.",
     r"$\dfrac{(x-3)(x^2+3)}{3(x-3)}\to\dfrac{12}{3}=\res{4}$"),
 (2, r"\pau{Castella i Lleó, ordinària 2023} Calcula $\displaystyle\lim_{x\to2}\dfrac{\sqrt{x^3+x-1}-\sqrt{x^3+1}}{x-2}$.",
     r"Pel conjugat: $\dfrac{x-2}{(x-2)\left(\sqrt{x^3+x-1}+\sqrt{x^3+1}\right)}\to\dfrac{1}{3+3}=\res{\dfrac16}$"),
 (2, r"\pau{Múrcia, ordinària 2023} Calcula $\displaystyle\lim_{x\to0}\dfrac{\sqrt{9+x}-\sqrt{9-x}}{3x}$.",
     r"$\dfrac{2x}{3x\left(\sqrt{9+x}+\sqrt{9-x}\right)}\to\dfrac{2}{3\cdot6}=\res{\dfrac19}$"),
)

# =====================================================================
# 4. Límits trigonomètrics i infinitèsims
for f, a, v in [(lambda x: sin(4*x)/(3*x), 0, M.mpf(4)/3), (lambda x: x*tan(2*x)/(1 - cos(x)), 0, 4), (lambda x: ln(1 + x**2)/sin(3*x)**2, 0, M.mpf(1)/9), (lambda x: (ex(x) - ex(-x))/sin(x), 0, 2),
                (lambda x: sin(3*x)/tan(5*x), 0, M.mpf(3)/5), (lambda x: (1 - cos(2*x))/(x*sin(x)), 0, 2), (lambda x: (ex(2*x) - 1)/ln(1 + 3*x), 0, M.mpf(2)/3),
                (lambda x: cos(x)/(2*x - pi), pi/2, -M.mpf(1)/2), (lambda x: sin(x)/(x - pi), pi, -1), (lambda x: ln(x)/(x**2 - 1), 1, M.mpf(1)/2), (lambda x: (sin(x) - tan(x))/(x**2*sin(x)), 0, -M.mpf(1)/2),
                (lambda x: cos(x)**(1/x**2), 0, ex(-M.mpf(1)/2)), (lambda x: x*sin(1/x), INF, 1), (lambda x: (3*x + cos(x))/x, -INF, 3), (lambda x: x**2*cos(1/x), 0, 0),
                (lambda x: (cos(2*x) - 1)/(x*sin(x)), 0, -2), (lambda x: ln(1 + x)/(ex(x) - 1), 0, 1), (lambda x: ln(x)/x, 1, 0), (lambda x: (x - 1)/ln(x), 1, 1), (lambda x: tan(x)/sin(x), 0, 1),
                (lambda x: cos(2*x)**(3/x**2), 0, ex(-6)), (lambda x: sin(pi*x/2)**(1/(1 - x)**2), 1, ex(-pi**2/8)), (lambda x: x*(ex(1/x) - 1), INF, 1)]:
    chk(f, a, v)
chk(lambda x: sq(x)*ln(x), 0, 0, 1)
sec("Límits trigonomètrics i infinitèsims equivalents",
 (2, r"Calcula, fent servir infinitèsims equivalents:" + tasks(3, [m(L('0', r'\dfrac{\sin 4x}{3x}')), m(L('0', r'\dfrac{x\tan 2x}{1-\cos x}')), m(L('0', r'\dfrac{\ln(1+x^2)}{\sin^2 3x}')), m(L('0', r'\dfrac{\sin 3x}{\tan 5x}')), m(L('0', r'\dfrac{1-\cos 2x}{x\sin x}')), m(L('0', r'\dfrac{e^{2x}-1}{\ln(1+3x)}'))])
     + recorda(r"Si $u\to0$: \ $\sin u\sim u$, \ $\tan u\sim u$, \ $1-\cos u\sim\frac{u^2}{2}$, \ $e^u-1\sim u$, \ $\ln(1+u)\sim u$. Només es poden substituir en \textbf{productes i quocients}, mai en sumes o restes."),
     tasks(3, [r'$\frac{4x}{3x}=\res{\frac43}$', r'$\frac{x\cdot2x}{x^2/2}=\res{4}$', r'$\frac{x^2}{9x^2}=\res{\frac19}$', r'$\frac{3x}{5x}=\res{\frac35}$', r'$\frac{(2x)^2/2}{x^2}=\res{2}$', r'$\frac{2x}{3x}=\res{\frac23}$'])),
 (2, r"Calcula (si el punt no és 0, fes primer un canvi de variable):" + tasks(3, [m(L('0', r'\dfrac{e^{x}-e^{-x}}{\sin x}')), m(L(r'\frac\pi2', r'\dfrac{\cos x}{2x-\pi}')), m(L(r'\pi', r'\dfrac{\sin x}{x-\pi}')), m(L('1', r'\dfrac{\ln x}{x^2-1}')), m(L('0', r'\dfrac{\sin x-\tan x}{x^2\sin x}')), m(L('0', r'(\cos x)^{1/x^2}'))]),
     tasks(2, [r'$\frac{e^{-x}(e^{2x}-1)}{\sin x}\sim\frac{2x}{x}\to\res{2}$', r'$t=x-\frac\pi2$: $\frac{-\sin t}{2t}\to\res{-\frac12}$', r'$t=x-\pi$: $\frac{-\sin t}{t}\to\res{-1}$', r'$t=x-1$: $\frac{t}{t(t+2)}\to\res{\frac12}$', r'$\tan x(\cos x-1)\sim-\frac{x^3}{2}$: \ $\res{-\frac12}$', r'$e^{\lim\frac{-x^2/2}{x^2}}=\res{e^{-1/2}}$'])),
 (2, r"Calcula, fent servir que el producte d'una funció fitada per una que tendeix a 0 tendeix a 0:" + tasks(3, [m(L(MI, r'\dfrac{3x+\cos x}{x}')), m(L('0', r'x^2\cos\dfrac1x')), m(L(PI, r'x\sin\dfrac1x'))]),
     tasks(3, [r'$3+\frac{\cos x}{x}\to\res{3}$', r'$\res{0}$', r'$t=\frac1x$: $\frac{\sin t}{t}\to\res{1}$'])),
 (2, r"\pau{Múrcia, ordinària 2023} Calcula $\displaystyle\lim_{x\to0}\dfrac{\cos(2x)-1}{x\sin x}$.",
     r"$\dfrac{-\frac{(2x)^2}{2}}{x\cdot x}=\res{-2}$"),
 (2, r"\pau{Castella i Lleó, extraordinària 2022} Calcula $\displaystyle\lim_{x\to0}\dfrac{\ln(1+x)}{e^x-1}$.",
     r"$\dfrac{x}{x}\to\res{1}$"),
 (2, r"\pau{Galícia, ordinària 2026} Calcula els límits següents:" + tasks(2, [m(L('1', r'\dfrac{\ln x}{x}')), m(L('1', r'\dfrac{x-1}{\ln x}')), m(L('0', r'\dfrac{\tan x}{\sin x}')), m(L('0^+', r'\sqrt x\,\ln x'))]),
     tasks(2, [r'$\frac{0}{1}=\res{0}$ (no és indeterminació)', r'$\ln x=\ln(1+(x-1))\sim x-1$: \ $\res{1}$', r'$\frac{1}{\cos x}\to\res{1}$', r'$t=\frac1x\to+\infty$: $-\frac{\ln t}{\sqrt t}\to\res{0}$'])),
 (2, r"\pau{La Rioja, extraordinària 2023} Calcula $\displaystyle\lim_{x\to0}(\cos2x)^{3/x^2}$.",
     r"$1^\infty$: \ $e^{\lim(\cos2x-1)\frac{3}{x^2}}=e^{\lim\frac{-2x^2\cdot3}{x^2}}=\res{e^{-6}}$"),
 (3, r"\pau{Aragó, extraordinària 2021} Calcula $\displaystyle\lim_{x\to1}\left(\sin\dfrac{\pi x}{2}\right)^{\frac{1}{(1-x)^2}}$.",
     r"$1^\infty$. Amb $t=x-1$: $\sin\left(\frac\pi2+\frac{\pi t}{2}\right)=\cos\frac{\pi t}{2}$ i $\cos\frac{\pi t}2-1\sim-\frac{\pi^2t^2}{8}$: \ $e^{\lim\frac{-\pi^2t^2/8}{t^2}}=\res{e^{-\pi^2/8}}$"),
 (2, r"\pau{Navarra, extraordinària 2021} Calcula $\displaystyle\lim_{x\to\infty}x\sin\dfrac1x$.",
     r"$t=\frac1x\to0$: \ $\dfrac{\sin t}{t}\to\res{1}$"),
 (2, r"\pau{Múrcia, extraordinària 2025} Calcula $\displaystyle\lim_{x\to+\infty}x\left(e^{1/x}-1\right)$.",
     r"$0\cdot\infty$; amb $t=\frac1x\to0^+$: \ $\dfrac{e^t-1}{t}\to\res{1}$"),
)

# =====================================================================
# 5. Límits amb paràmetres
chk(lambda x: (8*x**2 - 3*x)/(2*x**2 + 5), INF, 4); chk(lambda x: (6*x**2 + 1)/(2*x**2 - x), INF, 3); chk(lambda x: sq(4*x**2 + x) - 2*x, INF, M.mpf(1)/4)
chk(lambda x: ((2*x + 3)/(2*x + 2))**(4*x), INF, ex(2)); chk(lambda x: (x**2 + 4*x + 3)/(x**2 + 3*x), -3, M.mpf(2)/3); chk(lambda x: (ex(3*x) - 1)/sin(2*x), 0, M.mpf(3)/2)
chk(lambda x: (x**2 + x - 2)/(x - 1), 1, 3); chk(lambda x: sq(x**2 + 3*x) - sq(x**2 - x), INF, 2); chk(lambda x: (1 - cos(4*x))/(x*sin(x)), 0, 8)
for a_, v in [(2, INF), (0, -INF), (1, M.mpf(1)/3)]: chk(lambda x: ((a_ - 1)*x**2 + x)/(3*x + 1), INF, v)
for a_, v in [(1, 0), (-1, INF), (0, ex(-1))]: chk(lambda x: ((x + 1)/(x + 2))**(a_*x**2 + x), INF, v)
chk(lambda x: 2*x/(ln(x)**2 + 2*x), INF, 1)
for k_, s, v in [(0, None, 0), (-1, None, 0), (1, -1, -INF), (1, 1, INF), (2, 1, INF)]: chk(lambda x: (x**4 + x**3 - x**2 - x)/(x**2 - 1)**(2*k_), 1, v, s)
for x in (-2.5, 0.5, 3): eq(x**4 + x**3 - x**2 - x, x*(x + 1)**2*(x - 1))
chk(lambda x: (4*x + 1)/(2*x - 2), 1, INF, 1); chk(lambda x: (4*x + 1)/(2*x - 2), INF, 2)
sec("Límits amb paràmetres",
 (2, r"Calcula el valor dels paràmetres perquè:" + tasks(1, [m(L(PI, r'\dfrac{ax^2-3x}{2x^2+5}') + '=4'), m(L(PI, r'\dfrac{ax^3+bx^2+1}{2x^2-x}') + '=3'), m(L(PI, r'\left(\dfrac{2x+3}{2x+a}\right)^{4x}') + '=e^2'), m(L('0', r'\dfrac{e^{mx}-1}{\sin 2x}') + r'=\dfrac32')])
     + recorda(r"Calculem el límit com si el paràmetre fóra un nombre i imposem la condició."),
     tasks(2, [r'$\frac a2=4\Rightarrow\res{a=8}$', r'Finit $\Rightarrow\res{a=0}$; \ $\frac b2=3\Rightarrow\res{b=6}$', r'$e^{\lim\frac{4x(3-a)}{2x+a}}=e^{2(3-a)}\Rightarrow\res{a=2}$', r'$\frac{mx}{2x}=\frac m2\Rightarrow\res{m=3}$'])),
 (2, r"Troba el valor de $a$ perquè el límit siga finit, i calcula'l en cada cas:" + tasks(2, [m(L(PI, r'\left(\sqrt{ax^2+x}-2x\right)')), m(L('-3', r'\dfrac{x^2+ax+3}{x^2+3x}'))]),
     tasks(1, [r"Si $a\neq4$, $(\sqrt a-2)x\to\pm\infty$. \ $\res{a=4}$: \ $\dfrac{x}{\sqrt{4x^2+x}+2x}\to\res{\frac14}$", r"El numerador s'ha d'anul·lar en $-3$: $9-3a+3=0\Rightarrow\res{a=4}$; \ $\dfrac{(x+3)(x+1)}{x(x+3)}\to\res{\frac23}$"])),
 (2, r"Troba $a$ i $b$ perquè $\displaystyle\lim_{x\to1}\dfrac{x^2+ax+b}{x-1}=3$.",
     r"Ha de ser $\frac00$: $1+a+b=0$; \ $x^2+ax-1-a=(x-1)(x+1+a)\Rightarrow2+a=3$: \ $\res{a=1,\ b=-2}$"),
 (2, r"Troba $a$ perquè:" + tasks(2, [m(L(PI, r'\left(\sqrt{x^2+ax}-\sqrt{x^2-x}\right)') + '=2'), m(L('0', r'\dfrac{1-\cos(ax)}{x\sin x}') + '=8')]),
     tasks(2, [r'$\dfrac{(a+1)x}{2x}=\dfrac{a+1}{2}=2\Rightarrow\res{a=3}$', r'$\dfrac{a^2x^2/2}{x^2}=\dfrac{a^2}{2}=8\Rightarrow\res{a=\pm4}$'])),
 (3, r"Discuteix, segons els valors del paràmetre $a$, els límits següents:" + tasks(1, [m(L(PI, r'\dfrac{(a-1)x^2+x}{3x+1}')), m(L(PI, r'\left(\dfrac{x+1}{x+2}\right)^{ax^2+x}'))]),
     tasks(1, [r"$a>1$: $\res{+\infty}$; \ $a<1$: $\res{-\infty}$; \ $a=1$: $\frac{x}{3x+1}\to\res{\frac13}$", r"$1^\infty$: $e^{\lim\frac{-(ax^2+x)}{x+2}}$. \ $a>0$: $e^{-\infty}=\res{0}$; \ $a<0$: $\res{+\infty}$; \ $a=0$: $\res{e^{-1}}$"])),
 (2, r"\pau{Andalusia, extraordinària 2022} Calcula $a$ sabent que $\displaystyle\lim_{x\to+\infty}\dfrac{ax}{(\ln x)^2+2x}=1$.",
     r"$(\ln x)^2$ és un infinit d'ordre inferior a $x$: \ $\lim\dfrac{ax}{2x}=\dfrac a2=1\Rightarrow\res{a=2}$"),
 (3, r"\pau{Aragó, extraordinària 2025} Calcula (si existeix), en funció del valor de $k\in\mathbb Z$, el límit \ $\displaystyle\lim_{x\to1}\dfrac{x^4+x^3-x^2-x}{\left(x^2-1\right)^{2k}}$.",
     r"$x^4+x^3-x^2-x=x(x-1)(x+1)^2$, \ i queda $x(x+1)^{2-2k}(x-1)^{1-2k}$. \ Si $k\leq0$, l'exponent $1-2k\geq1$: \ $\res{0}$. \ Si $k\geq1$, $(x-1)^{1-2k}$ té exponent negatiu i senar: $\lim_{x\to1^-}=-\infty$, $\lim_{x\to1^+}=+\infty$: \ el límit \rest{és infinit (no existeix)}"),
 (2, r"\pau{Castella-la Manxa, extraordinària 2022} Troba raonadament $a$ i $b$ perquè la funció $f(x)=\dfrac{ax+1}{2x+b}$ tinga una discontinuïtat de salt infinit en $x=1$ i tendisca a 2 quan $x\to+\infty$.",
     r"Denominador nul en 1: $\res{b=-2}$ (el numerador $a+1\neq0$). \ $\lim_{x\to+\infty}=\frac a2=2\Rightarrow\res{a=4}$"),
)

# =====================================================================
# 6. Continuïtat
chk(lambda x: sin(3*x)/x, 0, 3); chk(lambda x: 1/(1 + ex(1/x)), 0, 1, -1); chk(lambda x: 1/(1 + ex(1/x)), 0, 0, 1); chk(lambda x: x*cos(1/x), 0, 0)
chk(lambda x: (ex(x) - 1)/x, 0, 1, 1); eq((ex(2) - 1)/2, M.mpf('3.19452804946532511361521373028750390')); eq(ln(4)/ln(2), 2)
chk(lambda x: 3/(x + 2), -2, -INF, -1); chk(lambda x: 3/(x + 2), -2, INF, 1); eq(3/(-1 + 2), 3); eq(2 - 1, sq(4) - 1)
chk(lambda x: sin(2*x)/x, 0, 2, -1); eq(pi + 2, cos(pi) + pi + 3)
chk(lambda x: x/(1 + ex(1/x)), 0, 0); chk(lambda x: (x**2 - 4)/abs(x - 2), 2, -4, -1); chk(lambda x: (x**2 - 4)/abs(x - 2), 2, 4, 1)
chk(lambda x: ex(1/(x - 1)), 1, 0, -1); chk(lambda x: ex(1/(x - 1)), 1, INF, 1)
eq(3**2 + 2*3 + 1, 16); eq(2*3/(3 - 4), -6); chk(lambda x: 2*x/(x - 4), 4, -INF, -1); chk(lambda x: 2*x/(x - 4), 4, INF, 1)
eq(2**0, 1); eq(1 - 2, -1); eq(ln(1), 0); eq(4/M.mpf(2), 3 - (4 - 5)**2)
eq(M.mpf(1)/3, 2*1/M.mpf(3 + 3)); chk(lambda x: 2*x**2/(3 - 3*x), 1, INF, -1); chk(lambda x: 2*x**2/(3 - 3*x), 1, -INF, 1); chk(lambda x: (x**2/(2 + x**2))**(2*x**2 - 1), -INF, ex(-4))
chk(lambda x: (x - 1)*sq(x)/(x**2 - 1), 1, M.mpf(1)/2); chk(lambda x: (1 - cos(x))/x, 0, 0); chk(lambda x: ln(1 + x)/(1 + x), 0, 0, 1); chk(lambda x: x*ex(4*x), 0, 0, -1)
chk(lambda x: (cos(pi*x)**2 - 1)/(1 - x), 1, 0, -1); eq(ln(1*ex(2)) - 2, 0); chk(lambda x: x*ln(x), 0, 0, 1)
sec("Continuïtat de funcions",
 (2, r"Estudia la continuïtat en $x=0$ de les funcions següents i classifica la discontinuïtat, si n'hi ha:" + tasks(1, ['$' + pw((r'\dfrac{\sin 3x}{x}', r'x\neq0'), ('3', 'x=0')) + '$', r'$g(x)=\dfrac{1}{1+e^{1/x}}$', r'$h(x)=x\cos\dfrac1x$. Quin valor caldria donar a $h(0)$ perquè fóra contínua?'])
     + recorda(r"$f$ és contínua en $a$ si $\exists f(a)$, $\exists\lim_{x\to a}f(x)$ i són iguals. Discontinuïtats: evitable (el límit existeix), de salt finit (laterals finits i diferents), de salt infinit (un lateral infinit) i asimptòtica (tots dos infinits)."),
     tasks(1, [r"$\lim\frac{3x}{x}=3=f(0)$: \ \rest{contínua}", r"$\lim_{x\to0^-}=1$, $\lim_{x\to0^+}=0$: \ \rest{salt finit}", r"$\cos\frac1x$ fitada: $\lim=0$, $\nexists h(0)$: \ \rest{evitable}; \ $\res{h(0)=0}$"])),
 (2, r"Estudia la continuïtat de les funcions següents:" + tasks(1, ['$' + pw((r'\cos x', r'x\leq0'), (r'\dfrac{e^x-1}{x}', r'0<x<2'), (r'\log_2(x+2)', r'x\geq2')) + '$', '$' + pw((r'\dfrac{3}{x+2}', r'x<-1'), (r'2-|x|', r'-1\leq x\leq1'), (r'\sqrt{x+3}-1', r'x>1'), name='g(x)') + '$', '$' + pw((r'\dfrac{\sin 2x}{x}', r'x<0'), (r'x+2', r'0\leq x<\pi'), (r'\cos x+\pi+3', r'x\geq\pi'), name='h(x)') + '$'])
     + recorda(r"Primer, cada tros en el seu interval obert (denominadors, logaritmes, arrels, $\tan$\ldots\ només compten si el punt és dins del tros). Després, els punts on canvia l'expressió."),
     tasks(1, [r"$x=0$: $f(0)=1=\lim_{x\to0^+}\frac{e^x-1}{x}$, contínua. \ $x=2$: $\lim^-=\frac{e^2-1}{2}\approx3{,}19\neq f(2)=2$: \rest{salt finit}. \ Contínua en $\res{\mathbb R-\{2\}}$",
               r"$x=-2$ (és de $x<-1$): \rest{asimptòtica}. \ $x=-1$: $\lim^-=3$, $g(-1)=1$: \rest{salt finit}. \ $x=1$: $1=1$, contínua. \ Contínua en $\res{\mathbb R-\{-2,-1\}}$",
               r"$x=0$: $\lim^-=2=h(0)$; \ $x=\pi$: $\lim^-=\pi+2=h(\pi)$. \ $\res{\text{Contínua en }\mathbb R}$"])),
 (2, r"Estudia la continuïtat de:" + tasks(3, [r'$f(x)=\dfrac{x}{1+e^{1/x}}$', r'$g(x)=\dfrac{x^2-4}{|x-2|}$', r'$h(x)=e^{\frac{1}{x-1}}$']),
     tasks(1, [r"$x=0$: $\lim^-=\frac{0}{1}=0$, $\lim^+=\frac{0}{+\infty}=0$, $\nexists f(0)$: \ \rest{evitable}", r"$x=2$: $\lim^-=-(x+2)\to-4$, $\lim^+=x+2\to4$: \ \rest{salt finit}", r"$x=1$: $\lim^-=e^{-\infty}=0$, $\lim^+=e^{+\infty}=+\infty$: \ \rest{salt infinit}"])),
 (2, r"\pau{Castella-la Manxa, extraordinària 2024} Estudia la continuïtat de la funció i, si en té, classifica'n les discontinuïtats:" + dm(pw((r'x^2+2x+1', r'x<3'), (r'\dfrac{2x}{x-4}', r'x\geq3'))),
     r"$x=3$: $\lim^-=16$, $f(3)=\lim^+=-6$: \rest{salt finit}. \ $x=4$ (és de $x\geq3$): $\frac{8}{0^\mp}=\mp\infty$: \rest{asimptòtica}. \ Contínua en $\res{\mathbb R-\{3,4\}}$"),
 (2, r"\pau{Castella-la Manxa, extraordinària 2020} Estudia la continuïtat de $f$ en $x=1$ i en $x=2$ i classifica-hi el tipus de discontinuïtat, si n'hi ha:" + dm(pw((r'2^{x-1}', r'x\leq1'), (r'x-2', r'1<x<2'), (r'\ln(x-1)', r'x\geq2'))),
     r"$x=1$: $f(1)=1$, $\lim^+=-1$: \rest{salt finit}. \ $x=2$: $\lim^-=0=\ln1=f(2)$: \rest{contínua}"),
 (2, r"\pau{Astúries, ordinària 2025} Estudia si la funció és contínua en el seu domini:" + dm(pw((r'\dfrac x2', r'0\leq x<4'), (r'3-(x-5)^2', r'4\leq x'))),
     r"Dos trossos polinòmics. $x=4$: $\lim^-=2$, $f(4)=3-1=2$: \ \rest{contínua en tot el domini} $[0,+\infty)$"),
 (2, r"\pau{Madrid, ordinària 2023} Donada la funció" + dm(pw((r'\dfrac{x^2}{2+x^2}', r'x\leq-1'), (r'\dfrac{2x^2}{3-3x}', r'x>-1'))) + tasks(1, [r"Estudia la continuïtat de $f$ en $\mathbb R$.", r"Calcula $\displaystyle\lim_{x\to-\infty}f(x)^{2x^2-1}$."]),
     tasks(1, [r"$x=-1$: $\frac13=\frac13$, contínua. $x=1$ (és de $x>-1$): $\frac{2}{0^\pm}$, \rest{asimptòtica}. Contínua en $\res{\mathbb R-\{1\}}$", r"$1^\infty$: $\frac{x^2}{2+x^2}-1=\frac{-2}{2+x^2}$; $\lim\frac{-2(2x^2-1)}{2+x^2}=-4$: \ $\res{e^{-4}}$"])),
 (2, r"\pau{Illes Balears, extraordinària 2024} Indica el domini de $g(x)=\dfrac{(x-1)\sqrt x}{x^2-1}$. És contínua en el seu domini? Si no ho és, quin tipus de discontinuïtat presenta?",
     r"Domini $\res{[0,1)\cup(1,+\infty)}$, on és contínua. En $x=1$: $\lim\frac{\sqrt x}{x+1}=\frac12$, $\nexists g(1)$: \ \rest{discontinuïtat evitable}"),
 (2, r"\pau{Castella i Lleó, extraordinària 2021} Estudia la continuïtat de la funció" + dm(pw((r'\dfrac{1-\cos x}{x}', r'x\neq0'), ('0', 'x=0'))),
     r"$\lim_{x\to0}\dfrac{x^2/2}{x}=0=f(0)$: \ $\res{\text{contínua en }\mathbb R}$"),
 (2, r"\pau{Galícia, extraordinària 2025} Estudia la continuïtat en $x=0$ de la funció" + dm(pw((r'x\,e^{4x}', r'x<0'), (r'\dfrac{\ln(1+x)}{1+x}', r'x\geq0'))),
     r"$\lim^-=0$, $f(0)=\frac{\ln1}{1}=0=\lim^+$: \ \rest{contínua en $x=0$}"),
 (3, r"\pau{Navarra, ordinària 2023} Estudia la continuïtat en $\mathbb R$ de la funció" + dm(pw((r'\dfrac{\cos^2(\pi x)-1}{1-x}', r'x<1'), (r'\ln\left(x\,e^{x+1}\right)-2x', r'x\geq1'))),
     r"Trossos continus (en $x<1$, $1-x\neq0$; en $x\geq1$, $xe^{x+1}>0$). $f(1)=\ln e^2-2=0$. \ $\lim_{x\to1^-}\dfrac{-\sin^2(\pi x)}{1-x}$; amb $t=x-1$: $\dfrac{-\sin^2(\pi t)}{-t}\sim\dfrac{\pi^2t^2}{t}\to0$. \ $\res{\text{Contínua en }\mathbb R}$"),
 (2, r"\pau{Madrid, extraordinària 2022} Estudia la continuïtat en $x=0$ de $f(x)=\begin{cases}x&\text{si }x\leq0\\x\ln x&\text{si }x>0\end{cases}$.",
     r"$f(0)=0$; \ $\lim_{x\to0^+}x\ln x\overset{t=1/x}{=}\lim_{t\to+\infty}\frac{-\ln t}{t}=0$: \ \rest{contínua}"),
)

# =====================================================================
# 7. Funcions a trossos amb paràmetres
chk(lambda x: sin(3*x)/x, 0, 3, -1); chk(lambda x: (ex(4*x) - 1)/x, 0, 4, -1); eq(cos(0) + 3, 4)
chk(lambda x: (x**2 + 3*x - 10)/(x - 2), 2, 7, -1); eq(7 + ln(1), 7); chk(lambda x: tan(3*x)/sin(x), 0, 3, -1); eq(sq(9), 3)
eq(-2*sin(-pi/2), (-1)*sin(-pi/2) + 1); eq(-1*sin(pi/2) + 1, cos(pi/2)); eq(3*ex(0), 3); chk(lambda x: ln(1 + 3*x)/x, 0, 3, 1); eq(ln(4), ln(2)*sq(1 + 3))
chk(lambda x: (sq(x + 1) - 2)/(x - 3), 3, M.mpf(1)/4); chk(lambda x: (1 + 2*x)**(1/x), 0, ex(2), 1)
eq(1/M.mpf(-1), -M.mpf(3)/4 + -M.mpf(1)/4); eq(M.mpf(3)/4 - M.mpf(1)/4, M.mpf(1)/(1 + 1)); chk(lambda x: x**2/(x + 1) - (x - 1), INF, 0)
for a_ in (0, 2.5): eq(a_ - cos(0), 0**2 - (1 - a_)*sin(0 + pi/2))
chk(lambda x: (ex(2*x) - 1)/x, 0, 2); chk(lambda x: (1 - x)**(-3/x), 0, ex(3), 1)
for a_ in (2, 3): eq(5 - a_*1, 6/(a_*1))
for b_ in (1, -2): eq((0 + -4*b_)/(2*0 - 4), 10*0 + 0 + b_)
for b_ in (1, 3): chk(lambda x: (ex(2*b_*x) - 1)/(2*x), 0, b_)
eq((4*4 - 2)/(5 + 2), 2); chk(lambda x: (x**2 + 2)/(x + 3) - (x - 3), INF, 0)
eq(1 + 3 + 4, ln(1)/1 + 4*2); chk(lambda x: ln(x)/x, INF, 0)
chk(lambda x: (x**3 - 8)/(x**2 - 4), 2, 3); chk(lambda x: (x**3 - 8)/(x**2 - 4) - x, INF, 0); chk(lambda x: (x**3 - 8)/(x**2 - 4), -2, INF, 1)
eq(sin(pi/2), 2/(pi/2) + (pi - 4)/pi)
eq(-2 + 2, 0); eq(4 - 2*2, 0); eq(2*sin(0) + 0, 0); eq((-2)**2 + 3*(-2), -2)
chk(lambda x: ((x + 1)/(2*x + 1))**(1/x), 0, 1/E, -1)
chk(lambda x: (cos(x) - 1)/(-x**2/2), 0, 1)
eq(5*ex(0), (0 - 2)**2 + 1); eq((2 - 2)**2 + 1, 1)
eq(2*1 + -M.mpf(5)/2 + M.mpf(1)/2, ln(1)); eq(2 + M.mpf(5)/2 + M.mpf(1)/2, 5)
eq(1, 1); chk(lambda x: ln(x)/(x - 1), 1, 1)
sec("Funcions a trossos amb paràmetres",
 (2, r"Troba els paràmetres perquè les funcions siguen contínues en tot el seu domini:" + tasks(2, ['$' + pw((r'\dfrac{\sin(ax)}{x}', r'x<0'), (r'x^2+3', r'x\geq0')) + '$', '$' + pw((r'\dfrac{e^{ax}-1}{x}', r'x<0'), (r'\cos x+3', r'x\geq0'), name='g(x)') + '$', '$' + pw((r'\dfrac{x^2+ax-10}{x-2}', r'x<2'), (r'b+\ln(x-1)', r'x\geq2'), name='h(x)') + '$', '$' + pw((r'\dfrac{\tan3x}{\sin x}', r'-\frac\pi6<x<0'), ('a', 'x=0'), (r'\sqrt{x+b}', 'x>0'), name='k(x)') + '$'])
     + recorda(r"En cada punt de canvi igualem els límits laterals i el valor de la funció. Si un tros dona $\frac00$, resolem la indeterminació; si el límit ha de ser finit i el denominador s'anul·la, el numerador també s'ha d'anul·lar."),
     tasks(2, [r'$\lim\frac{ax}{x}=a=3$: \ $\res{a=3}$', r'$\lim\frac{ax}{x}=a=g(0)=4$: \ $\res{a=4}$', r'$4+2a-10=0\Rightarrow\res{a=3}$, límit $7$; \ $b+\ln1=7\Rightarrow\res{b=7}$', r'$\frac{3x}{x}\to3$: \ $\res{a=3}$; \ $\sqrt b=3\Rightarrow\res{b=9}$'])),
 (2, r"Troba els paràmetres perquè les funcions siguen contínues en $\mathbb R$:" + tasks(1, ['$' + pw((r'-2\sin x', r'x\leq-\frac\pi2'), (r'a\sin x+b', r'-\frac\pi2<x<\frac\pi2'), (r'\cos x', r'x\geq\frac\pi2')) + '$', '$' + pw((r'a\,e^{x}', r'x\leq0'), (r'\dfrac{\ln(1+3x)}{x}', r'0<x\leq1'), (r'b\sqrt{x+3}', r'x>1'), name='g(x)') + '$']),
     tasks(1, [r"$x=-\frac\pi2$: $2=-a+b$; \ $x=\frac\pi2$: $a+b=0$: \ $\res{a=-1,\ b=1}$", r"$x=0$: $a=\lim\frac{3x}{x}=3$; \ $x=1$: $\ln4=2b$: \ $\res{a=3,\ b=\ln2}$"])),
 (2, r"Troba $k$ i $a$ perquè les funcions siguen contínues:" + tasks(2, ['$' + pw((r'\dfrac{\sqrt{x+1}-2}{x-3}', r'x\neq3'), ('k', 'x=3')) + '$', '$' + pw((r'x+e^2', r'x\leq0'), (r'(1+ax)^{1/x}', r'x>0'), name='g(x)') + '$']),
     tasks(2, [r'Conjugat: $\frac14$: \ $\res{k=\frac14}$', r'$1^\infty$: $e^{a}=e^2$: \ $\res{a=2}$'])),
 (2, r"\pau{Andalusia, ordinària 2022} Considera la funció contínua" + dm(pw((r'\dfrac1x', r'x<-1'), (r'ax+b', r'-1\leq x<1'), (r'\dfrac{x^2}{x+1}', r'x\geq1'))) + tasks(1, [r"Calcula $a$ i $b$.", r"Estudia i troba les asímptotes de la gràfica de $f$."]),
     tasks(1, [r"$x=-1$: $-1=-a+b$; \ $x=1$: $a+b=\frac12$: \ $\res{a=\frac34,\ b=-\frac14}$", r"Cap AV ($\frac1x$ i $\frac{x^2}{x+1}$ no fallen dins dels seus trossos). \ AH $\res{y=0}$ quan $x\to-\infty$; \ AO $\res{y=x-1}$ quan $x\to+\infty$ ($x^2=(x+1)(x-1)+1$)"])),
 (2, r"\pau{Aragó, extraordinària 2024} Estudia la continuïtat en $\mathbb R$, segons els valors de $a$ i $b$, de" + dm(pw((r'a-\cos x', r'x\leq0'), (r'x^2-b\sin\left(x+\frac\pi2\right)', r'x>0'))),
     r"$f(0)=a-1$, \ $\lim_{x\to0^+}=-b\sin\frac\pi2=-b$. \ Contínua en $\mathbb R$ si $\res{b=1-a}$; si no, salt finit en $x=0$."),
 (2, r"\pau{Aragó, ordinària 2024} Estudia la continuïtat en $\mathbb R$, segons els valors de $a$, de" + dm(pw((r'\dfrac{e^{2x}-1}{x}', r'x\neq0'), ('a', 'x=0'))),
     r"$\lim_{x\to0}\frac{2x}{x}=2$: contínua en $\mathbb R$ si $\res{a=2}$; si $a\neq2$, discontinuïtat evitable en $x=0$."),
 (2, r"\pau{Aragó, ordinària 2022} Determina $a$ perquè $f$ siga contínua en $\mathbb R$:" + dm(pw((r'\sqrt{-x}+e^3', r'x\leq0'), (r'(1-x)^{a/x}', r'x>0'))),
     r"$f(0)=e^3$; \ $\lim_{x\to0^+}(1-x)^{a/x}=e^{\lim(-x)\frac ax}=e^{-a}$: \ $\res{a=-3}$"),
 (2, r"\pau{Aragó, extraordinària 2021} Calcula els valors de $a\neq0$ perquè $f$ siga contínua:" + dm(pw((r'5-ax^2', r'x\leq1'), (r'\dfrac{6}{ax}', r'x>1'))),
     r"$5-a=\frac6a\Rightarrow a^2-5a+6=0$: \ $\res{a=2\ \text{o}\ a=3}$"),
 (2, r"\pau{Illes Balears, ordinària 2022} Troba la condició que han de complir $a$ i $b$ perquè $f$ siga contínua:" + dm(pw((r'\dfrac{x^2+a}{2x-4}', r'x\leq0'), (r'10x^2+x+b', r'x>0'))),
     r"$f(0)=-\frac a4$, \ $\lim_{x\to0^+}=b$: \ $\res{a=-4b}$"),
 (2, r"\pau{Illes Balears, extraordinària 2021} Considera $f(x)=\begin{cases}\dfrac{e^{ax}-1}{2x}&\text{si }x\neq0\\b&\text{si }x=0\end{cases}$." + tasks(1, [r"Estudia la continuïtat de $f$ en els punts $x\neq0$.", r"Quina relació hi ha d'haver entre $a$ i $b$ perquè $f$ siga contínua en $x=0$?"]),
     tasks(1, [r"\rest{Contínua} (quocient de contínues amb $2x\neq0$)", r"$\lim\frac{ax}{2x}=\frac a2=b$: \ $\res{a=2b}$"])),
 (2, r"\pau{Canàries, ordinària 2021} Siga $f(x)=\dfrac{ax^2-2}{b-x}$." + tasks(1, [r"Calcula $a$ i $b$ perquè $f(-2)=2$ i $f$ siga contínua en $\mathbb R-\{5\}$.", r"Troba les asímptotes de $f$ si $a=-1$ i $b=-3$."]),
     tasks(1, [r"El denominador s'anul·la en $x=5$: $\res{b=5}$; \ $\frac{4a-2}{7}=2$: $\res{a=4}$", r"$f(x)=\frac{x^2+2}{x+3}$: AV $\res{x=-3}$; \ $x^2+2=(x+3)(x-3)+11$: AO $\res{y=x-3}$"])),
 (2, r"\pau{Cantàbria, extraordinària 2026} Considera" + dm(pw((r'x^2+3x+a^2', r'x<1'), (r'\dfrac{\ln x}{x}+4a', r'x\geq1'))) + tasks(1, [r"Calcula els valors de $a$ per als quals $f$ és contínua en tot el seu domini.", r"Calcula les asímptotes de $f$ en funció de $a$."]),
     tasks(1, [r"$4+a^2=4a\Rightarrow(a-2)^2=0$: \ $\res{a=2}$", r"Cap AV. Quan $x\to-\infty$, $f\to+\infty$ i $\frac fx\to-\infty$: res. Quan $x\to+\infty$, $\frac{\ln x}{x}\to0$: AH $\res{y=4a}$"])),
 (2, r"\pau{Cantàbria, ordinària 2025} Considera $f(x)=\begin{cases}\dfrac{x^3-8}{x^2-4}&\text{si }x\neq2\\e^{k}&\text{si }x=2\end{cases}$." + tasks(1, [r"Determina $k$ perquè $f$ siga contínua en $x=2$.", r"Troba les asímptotes de $f$ i especifica'n el tipus."]),
     tasks(1, [r"$\frac{(x-2)(x^2+2x+4)}{(x-2)(x+2)}\to\frac{12}{4}=3=e^k$: \ $\res{k=\ln3}$", r"AV $\res{x=-2}$; \ cap AH; \ $\frac{x^2+2x+4}{x+2}=x+\frac{4}{x+2}$: AO $\res{y=x}$"])),
 (2, r"\pau{Cantàbria, extraordinària 2020} Considera" + dm(pw((r'\sin x', r'x\leq\frac\pi2'), (r'\dfrac2x+a', r'x>\frac\pi2'))) + tasks(1, [r"Troba $a$ perquè $f$ siga contínua.", r"Calcula $\displaystyle\lim_{x\to+\infty}f(x)$ i $\displaystyle\lim_{x\to-\infty}f(x)$."]),
     tasks(1, [r"$1=\frac4\pi+a$: \ $\res{a=\dfrac{\pi-4}{\pi}}$", r"$\lim_{x\to+\infty}=\res{a}$; \ $\lim_{x\to-\infty}\sin x$: \ $\res{\nexists}$ (oscil·la)"])),
 (2, r"\pau{Cantàbria, extraordinària 2018} Siga" + dm(pw((r'x+2', r'x\leq-2'), (r'x^2+ax', r'-2<x<0'), (r'2\sin x+b', r'0\leq x'))) + tasks(1, [r"Determina $a$ i $b$ perquè $f$ siga contínua en $\mathbb R$.", r"Si $a=3$ i $b=0$, classifica la discontinuïtat en $x=-2$."]),
     tasks(1, [r"$x=-2$: $0=4-2a$; \ $x=0$: $0=b$: \ $\res{a=2,\ b=0}$", r"$f(-2)=0$, $\lim^+=4-6=-2$: \ \rest{salt finit}"])),
 (2, r"\pau{Castella-la Manxa, extraordinària 2017} Determina $k$ perquè $f$ siga contínua en $x=0$:" + dm(pw((r'\left(\dfrac{x+1}{2x+1}\right)^{1/x}', r'x<0'), (r'6x+k', r'x\geq0'))),
     r"$1^\infty$: $\frac{x+1}{2x+1}-1=\frac{-x}{2x+1}$, \ $e^{\lim\frac{-1}{2x+1}}=e^{-1}$: \ $\res{k=\dfrac1e}$"),
 (2, r"\pau{Castella i Lleó, extraordinària 2024} Quins valors han de prendre $a\in\mathbb R$ i $b\in\mathbb R-\{0\}$ perquè $f$ siga contínua en $\mathbb R$?" + dm(pw((r'\dfrac{\cos x-a}{bx^2}', r'x\neq0'), ('1', 'x=0'))),
     r"Límit finit $\Rightarrow\res{a=1}$; \ $\frac{-x^2/2}{bx^2}=-\frac{1}{2b}=1$: \ $\res{b=-\frac12}$"),
 (2, r"\pau{Catalunya, ordinària 2026} Determina els valors de $m$ que fan que $f$ siga contínua en tot el seu domini:" + dm(pw((r'5e^{2x}', r'x\leq0'), (r'(x+m)^2+1', r'0<x<2'), ('1', r'2\leq x'))),
     r"$x=0$: $5=m^2+1\Rightarrow m=\pm2$; \ $x=2$: $(2+m)^2+1=1\Rightarrow m=-2$: \ $\res{m=-2}$"),
 (2, r"\pau{Extremadura, extraordinària 2023} Troba $a$ i $b$ perquè $f$ siga contínua en $x=1$ i la seua gràfica passe pel punt $(-1,5)$:" + dm(pw((r'2x^2+ax+b', r'x\leq1'), (r'\ln x', r'x>1'))),
     r"$2+a+b=0$ i $2-a+b=5$: \ $\res{a=-\frac52,\ b=\frac12}$"),
 (2, r"\pau{Múrcia, extraordinària 2022} Considera $f(x)=\begin{cases}\dfrac{\ln x}{x-1}&\text{si }x>0,\ x\neq1\\a&\text{si }x=1\end{cases}$." + tasks(1, [r"Calcula el límit de $f(x)$ quan $x\to+\infty$.", r"Determina $a$ perquè $f$ siga contínua en $x=1$."]),
     tasks(1, [r"$\res{0}$ (comparació d'infinits)", r"$t=x-1$: $\frac{\ln(1+t)}{t}\to1$: \ $\res{a=1}$"])),
)

# =====================================================================
# 8. Teorema de Bolzano
f8 = lambda x: x**3 + x - 1
eq(f8(0.5), -0.375); eq(f8(0.6), -0.184); eq(f8(0.7), 0.043); ck(abs(M.findroot(f8, 0.7) - M.mpf('0.6823278')) < 1e-6)
g8 = lambda x: x**5 + x**3 - 1; ck(g8(0.8) < 0 < g8(0.9))
ck(ex(-1) - 1 < 0); ck(cos(pi/2) - pi/2 < 0)
ck(0**3 - 0 == 0 and 2**3 - 2 == 6)
A = lambda x: -M.mpf('0.0001')*x**3 + M.mpf('0.05')*x**2 - 4*x + 200; eq(A(0), 200); eq(A(500), -1800)
eq(0**3 + 6*0 + 3*0 - 10, -10); eq(2**3 + 6*4 + 3*2 - 10, 28)
ck(cos(0) - 2 + 0 < 0 < cos(2*pi) - 2 + 2*pi); ck(0 + sin(0) - 2 < 0 < pi/2 + sin(pi/2) - 2)
ck(ex(0) + 0 - 2 < 0 < ex(1) + 1 - 2)
ck(0**6 + 0 - 1 < 0 < 1 + 1 - 1)
fc = lambda x: (2*x**3 - 5*x + 4)/(1 - x); eq(fc(-2), -M.mpf(2)/3); eq(fc(0), 4); eq(fc(2), -10); eq(fc(-1), M.mpf(7)/2)
ck(0 + 0 - 3 < 0 < 8 + 2 - 3)
eq(M.mpf(-1)/2, -1/M.mpf(2)); eq((M.mpf(1)/2 + 1)*sin(pi/2), M.mpf(3)/2)
fn = lambda x: sin(pi/4*ln(1/x)); eq(fn(1/E), sq(2)/2); eq(fn(E), -sq(2)/2); ck(fn(E) < E*sq(2)/(1 - E**2) < fn(1/E))
fl = lambda x: M.log(sin(pi*(x + 1)/4) + 2**((x - 5)/2), 2); eq(fl(6), -M.mpf(1)/2); eq(fl(7), 1)
ck(all(sin(pi*(x + 1)/4) + 2**((x - 5)/2) > 0 for x in [6 + k/M.mpf(20) for k in range(21)]))
sec("Teorema de Bolzano",
 (2, r"Demostra que l'equació $x^3+x-1=0$ té almenys una solució en l'interval $(0,1)$ i troba-la amb una xifra decimal exacta."
     + recorda(r"\textbf{Bolzano}: si $f$ és contínua en $[a,b]$ i $f(a)\cdot f(b)<0$, existeix almenys un $c\in(a,b)$ amb $f(c)=0$. Per afinar, parteix l'interval per la meitat i queda't amb la meitat on hi ha canvi de signe."),
     r"$f$ polinòmica, contínua; $f(0)=-1<0$, $f(1)=1>0$. \ $f(0{,}5)=-0{,}375$, $f(0{,}7)=0{,}043$, $f(0{,}6)=-0{,}184$: \ $c\in(0{,}6;\,0{,}7)$, \ $\res{c\approx0{,}6\ldots}$ ($c\approx0{,}682$)"),
 (2, r"Demostra que:" + tasks(1, [r"l'equació $x^5+x^3=1$ té alguna solució real, i troba un interval de longitud $0{,}1$ que la continga;", r"l'equació $e^{-x}=x$ té alguna solució en $(0,1)$;", r"les gràfiques de $y=\cos x$ i $y=x$ es tallen en algun punt de $\left(0,\frac\pi2\right)$;", r"la funció $f(x)=x^3-x$ pren el valor $5$ en algun punt de $[1,2]$."]),
     tasks(1, [r"$g=x^5+x^3-1$: $g(0)=-1$, $g(1)=1$; $g(0{,}8)=-0{,}16$, $g(0{,}9)=0{,}32$: \ $\res{(0{,}8;\ 0{,}9)}$", r"$h=e^{-x}-x$: $h(0)=1>0$, $h(1)=\frac1e-1<0$", r"$h=\cos x-x$: $h(0)=1>0$, $h\left(\frac\pi2\right)=-\frac\pi2<0$", r"$f(1)=0<5<6=f(2)$ i $f$ contínua: valors intermedis (o Bolzano a $x^3-x-5$)"])),
 (2, r"Raona si es pot aplicar el teorema de Bolzano i, si és el cas, què en podem deduir:" + tasks(1, [r"$f(x)=\dfrac1x$ en $[-1,1]$", r"$f(x)=\tan x$ en $\left[\frac\pi4,\frac{3\pi}4\right]$", r"$f(x)=x^3+ax-1$ en $[0,1]$, amb $a>0$", r"$f(x)=x^2-1$ en $[-2,2]$"]),
     tasks(1, [r"\rest{No}: no és contínua en $x=0$ (i de fet no s'anul·la mai)", r"\rest{No}: no és contínua en $\frac\pi2$ (i no té cap arrel en l'interval)", r"\rest{Sí}: $f(0)=-1<0$, $f(1)=a>0$: té una arrel en $(0,1)$", r"\rest{No}: $f(-2)=f(2)=3>0$. Bolzano no diu res, però en té dues ($\pm1$)"])),
 (2, r"\pau{Illes Balears, ordinària 2025} L'altitud (en metres) d'un terreny en un tram de 500 metres és $A(x)=-0{,}0001x^3+0{,}05x^2-4x+200$, amb $x\in[0,500]$ la distància recorreguda horitzontalment. Demostra que hi ha almenys un punt del tram on l'altitud és 0.",
     r"$A$ és polinòmica, contínua en $[0,500]$; $A(0)=200>0$, $A(500)=-1800<0$. Per Bolzano, \rest{existeix $c\in(0,500)$ amb $A(c)=0$}"),
 (2, r"\pau{Castella-la Manxa, ordinària 2023} Enuncia el teorema de Bolzano i utilitza'l per justificar que $f(x)=x^3+6x^2+3x-10$ té almenys una arrel en $[0,2]$.",
     r"$f$ contínua; $f(0)=-10<0$, $f(2)=28>0$: \ \rest{existeix $c\in(0,2)$ amb $f(c)=0$}"),
 (2, r"\pau{Castella-la Manxa, extraordinària 2017} Enuncia el teorema de Bolzano i comprova si l'equació $\cos x=2-x$ té alguna solució real en l'interval $[0,2\pi]$.",
     r"$g(x)=\cos x-2+x$, contínua; $g(0)=-1<0$, $g(2\pi)=2\pi-1>0$: \ \rest{sí que en té}"),
 (2, r"\pau{Castella i Lleó, extraordinària 2022} Esbrina si la funció $f(x)=x+\sin x-2$ s'anul·la en algun punt de l'interval $\left[0,\frac\pi2\right]$.",
     r"Contínua; $f(0)=-2<0$, $f\left(\frac\pi2\right)=\frac\pi2-1>0$: \ \rest{sí, per Bolzano}"),
 (2, r"\pau{Castella i Lleó, extraordinària 2024} Donada la funció $f(x)=e^x+x^3-2$, demostra que $f$ s'anul·la per a algun valor de $x$ i que aquest valor és únic.",
     r"$f$ contínua, $f(0)=-1<0$, $f(1)=e-1>0$: \rest{s'anul·la en $(0,1)$}. És \rest{únic} perquè $e^x$ i $x^3$ són estrictament creixents i, per tant, també ho és la seua suma: no pot tornar a valer 0."),
 (2, r"\pau{Castella i Lleó, ordinària 2017} Enuncia el teorema de Bolzano, interpreta'l geomètricament i troba un interval en què $P(x)=x^6+x^4-1$ tinga almenys una arrel.",
     r"Una corba contínua que passa d'un costat a l'altre de l'eix $OX$ el talla. \ $P(0)=-1$, $P(1)=1$: \ $\res{(0,1)}$"),
 (2, r"\pau{Extremadura, ordinària 2018} Enuncia el teorema de Bolzano i demostra, usant-lo, que la funció $f(x)=x^3+x-3$ té una arrel real positiva.",
     r"$f(0)=-3<0$, $f(2)=7>0$, contínua: \ \rest{hi ha una arrel en $(0,2)$}"),
 (2, r"\pau{Madrid, ordinària 2022} Comprova si $f(x)=\dfrac{x}{x^2+1}$ verifica les hipòtesis del teorema de Bolzano en l'interval $[-1,1]$.",
     r"\rest{Sí}: és contínua ($x^2+1\neq0$) i $f(-1)=-\frac12<0<\frac12=f(1)$"),
 (3, r"\pau{Catalunya, ordinària 2019} Considera la funció $f(x)=\dfrac{2x^3-5x+4}{1-x}$." + tasks(1, [r"Calcula el domini i estudia la continuïtat de $f$. Té asímptota vertical?", r"Observa que $f(-2)=-\frac23$, $f(0)=4$ i $f(2)=-10$. Raona si, a partir d'aquesta informació, podem deduir que l'interval $(-2,0)$ conté un zero de la funció. I l'interval $(0,2)$? Troba un interval determinat per dos enters consecutius que continga, com a mínim, un zero de la funció."]),
     tasks(1, [r"Domini $\mathbb R-\{1\}$, contínua en tot el domini; en $x=1$, $\frac10$: \ AV $\res{x=1}$", r"En $[-2,0]$ és contínua i canvia de signe: \rest{sí}. En $[0,2]$ no és contínua (falla en 1): \rest{no podem deduir-ho}. $f(-1)=\frac72>0$: \ $\res{(-2,-1)}$"])),
 (2, r"\pau{Galícia, ordinària 2026} Dibuixa, si és possible, la gràfica d'una funció contínua en $[a,b]$, amb $f(a)f(b)<0$, i que talle l'eix $X$ en més d'un punt de l'interval $(a,b)$.",
     r"\rest{És possible}: Bolzano assegura almenys un tall, no un de sol. Per exemple, $f(x)=x^3-x$ en $[-2,2]$ (talla en $-1$, $0$ i $1$)."),
 (2, r"\pau{Navarra, ordinària 2023} Es considera $f(x)=(x+1)\sin(\pi x)$. Comprova que existeix un valor $\alpha\in(0,1)$ tal que $f(\alpha)=\frac34$. Enuncia el resultat teòric utilitzat.",
     r"Teorema dels valors intermedis: $f$ contínua en $\left[0,\frac12\right]$, $f(0)=0<\frac34<\frac32=f\left(\frac12\right)$: \ \rest{existeix $\alpha\in\left(0,\frac12\right)$}"),
 (3, r"\pau{Navarra, extraordinària 2022} Siga $f(x)=\sin\left(\dfrac\pi4\ln\dfrac1x\right)$." + tasks(1, [r"Demostra que és contínua en $\left[\frac1e,e\right]$.", r"Demostra que existeix $\alpha\in\left(\frac1e,e\right)$ tal que $f(\alpha)=\dfrac{e\sqrt2}{1-e^2}$. Enuncia el resultat utilitzat."]),
     tasks(1, [r"Composició de contínues ($\ln$ està definit per a $x>0$)", r"$f\left(\frac1e\right)=\frac{\sqrt2}{2}\approx0{,}71$, $f(e)=-\frac{\sqrt2}{2}$ i $\frac{e\sqrt2}{1-e^2}\approx-0{,}60$ està entre tots dos: \ \rest{valors intermedis}"])),
 (3, r"\pau{Navarra, extraordinària 2021} Es considera $f(x)=\log_2\left[\sin\dfrac{\pi(x+1)}{4}+2^{\frac{x-5}{2}}\right]$." + tasks(1, [r"Demostra que és contínua en $[6,7]$.", r"Demostra que existeix $\alpha\in(6,7)$ tal que $f(\alpha)=0$."]),
     tasks(1, [r"En $[6,7]$, $\sin\frac{\pi(x+1)}{4}\geq-\frac{\sqrt2}{2}$ i $2^{\frac{x-5}{2}}\geq\sqrt2$: l'argument és positiu i $f$ és composició de contínues", r"$f(6)=\log_2\frac{\sqrt2}{2}=-\frac12<0$, $f(7)=\log_22=1>0$: \ \rest{Bolzano}"])),
)

# =====================================================================
# 9. Asímptotes
chk(lambda x: (2*x - 1)/(x + 3), -3, INF, -1); chk(lambda x: (2*x - 1)/(x + 3), INF, 2)
chk(lambda x: (2*x**3 - x)/(x**2 - 1) - 2*x, INF, 0); chk(lambda x: ex(x)/(x - 1), -INF, 0); chk(lambda x: ex(x)/(x*(x - 1)), INF, INF)
chk(lambda x: sq(4*x**2 + x) - 2*x, INF, M.mpf(1)/4); chk(lambda x: sq(4*x**2 + x) + 2*x, -INF, -M.mpf(1)/4)
chk(lambda x: ln(x/(x - 2)), 0, -INF, -1); chk(lambda x: ln(x/(x - 2)), 2, INF, 1); chk(lambda x: ln(x/(x - 2)), INF, 0)
chk(lambda x: x + sin(x)/x - x, INF, 0); chk(lambda x: sin(x)/x + x, 0, 1)
for f, a, v in [(lambda x: (2*x**2 - 3*x + 2)/(x - 1) - 2*x, INF, -1), (lambda x: (x**2 - 2*x + 1)/(x + 4) - (x - 6), INF, 0), (lambda x: (x**2 + 3*x + 1)/(x + 9) - (x - 6), INF, 0),
                (lambda x: (ex(x) - 1)/(ex(2*x) - 4), -INF, M.mpf(1)/4), (lambda x: (ex(x) - 1)/(ex(2*x) - 4), INF, 0), (lambda x: (x**3 + 5*x**2)/(x**2 - 1) - (x + 5), INF, 0),
                (lambda x: x**2/(2 - x) - (-x - 2), INF, 0), (lambda x: ln(2*x)/x, 0, -INF), (lambda x: ln(2*x)/x, INF, 0), (lambda x: x/(x**2 - 3*x - 4), INF, 0), (lambda x: x/(x - 1)**2, 1, INF),
                (lambda x: (x**2 + 1)/(x - 2) - (x + 2), INF, 0), (lambda x: (1 - cos(x))/x, 0, 0), (lambda x: (1 - cos(x))/x, INF, 0), (lambda x: (2*x + 1)/x, -INF, 2)]:
    chk(f, a, v, 1 if a in (0, 1) and v in (-INF, INF) else None)
eq((2 + 4)*0, 0); chk(lambda x: (2*x + 1)/x, 0, -INF, -1)
sec("Asímptotes",
 (2, r"Calcula totes les asímptotes de les funcions següents i estudia els límits laterals en les verticals:" + tasks(2, [r'$f(x)=\dfrac{2x-1}{x+3}$', r'$f(x)=\dfrac{2x^3-x}{x^2-1}$', r'$f(x)=\dfrac{e^x}{x-1}$', r'$f(x)=\sqrt{4x^2+x}$', r'$f(x)=\ln\dfrac{x}{x-2}$', r'$f(x)=x+\dfrac{\sin x}{x}$'])
     + recorda(r"AV: on la funció tendeix a $\pm\infty$ (zeros de denominadors, extrems del domini d'un logaritme\ldots). AH: $\lim_{x\to\pm\infty}f(x)=k$. AO $y=mx+n$: $m=\lim\frac{f(x)}{x}$, $n=\lim(f(x)-mx)$; estudia cada costat per separat."),
     tasks(1, [r"AV $\res{x=-3}$ ($+\infty$ per l'esquerra, $-\infty$ per la dreta); AH $\res{y=2}$",
               r"AV $\res{x=\pm1}$ (en totes dues, $-\infty$ per l'esquerra i $+\infty$ per la dreta); $2x^3-x=(x^2-1)2x+x$: AO $\res{y=2x}$",
               r"AV $\res{x=1}$ ($-\infty$ per l'esquerra, $+\infty$ per la dreta); AH $\res{y=0}$ només quan $x\to-\infty$; quan $x\to+\infty$, $\frac fx\to+\infty$: cap AO",
               r"AO $\res{y=2x+\frac14}$ quan $x\to+\infty$ i $\res{y=-2x-\frac14}$ quan $x\to-\infty$; cap AV",
               r"Domini $x<0$ o $x>2$. AV $\res{x=0}$ ($\lim_{x\to0^-}=-\infty$) i $\res{x=2}$ ($\lim_{x\to2^+}=+\infty$); AH $\res{y=0}$",
               r"En $x=0$ el límit és 1: no hi ha AV (evitable). AO $\res{y=x}$ pels dos costats"])),
 (2, r"\pau{Andalusia, ordinària 2021} La gràfica de $f(x)=\dfrac{ax^2+bx+2}{x-1}$ ($x\neq1$) té una asímptota obliqua que passa pel punt $(1,1)$ i té pendent 2. Calcula $a$ i $b$.",
     r"$m=a=2$; \ $n=\lim(f(x)-2x)=\lim\frac{(b+2)x+2}{x-1}=b+2$. Passa per $(1,1)$: $2+b+2=1$: \ $\res{a=2,\ b=-3}$"),
 (2, r"\pau{Cantàbria, ordinària 2026} Calcula els valors de $a$ per als quals $f(x)=\dfrac{x^2+ax+1}{x+a^2}$ té com a asímptota obliqua la recta $y=x-6$.",
     r"El quocient de la divisió és $x+a-a^2$: \ $a-a^2=-6\Rightarrow\res{a=3\ \text{o}\ a=-2}$"),
 (2, r"\pau{Cantàbria, ordinària 2026} Calcula, si n'hi ha, les asímptotes de $f(x)=\dfrac{e^x-1}{e^{2x}-4}$.",
     r"AV $\res{x=\ln2}$ ($e^{2x}=4$ i el numerador val 1); AH $\res{y=\frac14}$ quan $x\to-\infty$ i $\res{y=0}$ quan $x\to+\infty$"),
 (2, r"\pau{Cantàbria, extraordinària 2018} Per a quin valor de $d$ té la funció $\dfrac{x^d+1}{x-2}$ una asímptota obliqua en $+\infty$? Calcula-la.",
     r"Cal grau del numerador = grau del denominador $+1$: $\res{d=2}$; \ $x^2+1=(x-2)(x+2)+5$: \ $\res{y=x+2}$"),
 (2, r"\pau{Cantàbria, extraordinària 2020} Considera $f(x)=\dfrac{1-\cos x}{x}$. Calcula $\displaystyle\lim_{x\to0}f(x)$ i les asímptotes de $f$.",
     r"$\lim\frac{x^2/2}{x}=\res{0}$: no hi ha AV. $|1-\cos x|\leq2$: $\lim_{x\to\pm\infty}f=0$: AH $\res{y=0}$"),
 (2, r"\pau{Canàries, extraordinària 2020} Troba les asímptotes de la funció $f(x)=\dfrac{x^3+5x^2}{x^2-1}$.",
     r"AV $\res{x=-1}$ i $\res{x=1}$; cap AH; $x^3+5x^2=(x^2-1)(x+5)+x+5$: AO $\res{y=x+5}$"),
 (2, r"\pau{Castella i Lleó, extraordinària 2022} Troba el domini i les asímptotes de $f(x)=\dfrac{x^2}{2-x}$.",
     r"Domini $\mathbb R-\{2\}$; AV $\res{x=2}$; cap AH; $x^2=(2-x)(-x-2)+4$: AO $\res{y=-x-2}$"),
 (2, r"\pau{Illes Balears, ordinària 2025} Determina el domini de $f(x)=\dfrac1x\ln(2x)$ i el comportament de la funció en els extrems del domini.",
     r"Domini $\res{(0,+\infty)}$. $\lim_{x\to0^+}=(+\infty)(-\infty)=-\infty$: AV $\res{x=0}$. $\lim_{x\to+\infty}=0$: AH $\res{y=0}$"),
 (2, r"\pau{La Rioja, extraordinària 2023} Troba el domini i les asímptotes de $f(x)=\dfrac{1+4x^4-x^2}{x}$.",
     r"Domini $\mathbb R-\{0\}$; AV $\res{x=0}$; cap AH ni AO (el grau del numerador supera en 3 el del denominador)"),
 (2, r"\pau{Madrid, extraordinària 2022} Siga $f(x)=\begin{cases}\dfrac{2x+1}{x}&\text{si }x<0\\x^2-4x+3&\text{si }x\geq0\end{cases}$. Estudia la continuïtat de $f$ i calcula, si n'hi ha, les asímptotes horitzontals i verticals.",
     r"$x=0$: $\lim^-=\frac{1}{0^-}=-\infty$, $f(0)=3$: \rest{salt infinit}; contínua en $\mathbb R-\{0\}$. AV $\res{x=0}$ (per l'esquerra); AH $\res{y=2}$ quan $x\to-\infty$"),
 (2, r"\pau{País Basc, extraordinària 2025} Troba les asímptotes de $f(x)=\dfrac{x}{x^2-3x-4}$.",
     r"$x^2-3x-4=(x-4)(x+1)$: AV $\res{x=-1}$ i $\res{x=4}$; AH $\res{y=0}$"),
 (2, r"\pau{País Basc, ordinària 2024} Troba les asímptotes de $f(x)=\dfrac{x}{x^2-2x+1}$.",
     r"$\frac{x}{(x-1)^2}$: AV $\res{x=1}$ ($+\infty$ pels dos costats); AH $\res{y=0}$; cap AO"),
 (2, r"\pau{Extremadura, ordinària 2018} Estudia el domini i les asímptotes de $f(x)=\dfrac{1}{x^2-1}$.",
     r"Domini $\mathbb R-\{-1,1\}$; AV $\res{x=-1}$ i $\res{x=1}$; AH $\res{y=0}$; cap AO"),
)

# =====================================================================
print(NCHK[0], 'comprovacions correctes')
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={límits, indeterminacions, infinitèsims equivalents, límits trigonomètrics, paràmetres, continuïtat, funcions a trossos, teorema de Bolzano, asímptotes, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre = pre.replace(r'\usepackage{amsmath,amssymb}', r'\usepackage{amsmath,amssymb}' + '\n' + r'\allowdisplaybreaks')
pre += '\n\\setlength{\\emergencystretch}{3em}\n'
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Límits i continuïtat"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 5: %s. 2n de Batxillerat MII}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 5: %s · 2n Batxillerat MII" % (t, TIT))
    assert 'MII}' in p and '2n Batxillerat MII' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques II}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 5' if sol else "Fitxa d'exercicis · Unitat 5") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb la calculadora de límits dels apunts interactius de la unitat. Cap d'aquests límits necessita derivades: n'hi ha prou amb operar, el conjugat, la comparació d'infinits, la fórmula de $1^\infty$ i els infinitèsims equivalents."
             if sol else r"Resol els exercicis al quadern justificant cada pas. Cap límit d'aquesta fitxa necessita derivades (la regla de L'Hôpital la veurem més endavant). Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes, traduïts al valencià (només els apartats que corresponen a aquesta unitat).") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, qq, s in exs:
            n += 1
            lab = re.search(r'\\label\{[^}]*\}', qq)
            if sol:
                head = re.sub(r'(\\pau\{[^}]*\}).*', r'\1', qq, flags=re.S) if qq.startswith('\\pau{') else ''
                out.append('\\ex{%d} %s%s\n\n' % (st, (lab.group(0) if lab else '') + head, s))
            else:
                out.append('\\ex{%d} %s\n\n' % (st, qq))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb la calculadora de límits dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't5-fitxa-solucions.tex' if sol else 't5-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'exercicis,', npau, 'de la PAU de', len(regs), 'comunitats:', ', '.join(regs))
