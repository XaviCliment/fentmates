# Versió en castellà de genera.py. Genera t6-fitxa-exercicis.tex i t6-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 6: Càlcul de derivades.
# Derivabilitat d'una funció) a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a
# Batxillerat les estrelles no es mostren. Les seccions segueixen els apunts interactius (materials/2batx-mii/t6-derivades.html).
# Els exercicis marcats amb \pau{...} són de la PAU d'altres comunitats (de Matemàtiques II i de Matemàtiques aplicades a les
# CCSS II), traduïts al valencià i presos dels reculls d'ebaumatematicas.com ja usats a les fitxes de CCSS U5 i MII U5 i dels
# exàmens de 2026 resolts per Juan Antonio Martínez García. Alguns s'han ampliat amb l'estudi de la derivabilitat (ho indica
# «ampliat»). Abans d'escriure els fitxers, sympy comprova totes les derivades, les tangents, els paràmetres i les derivades
# laterals de les solucions.
# Ús: python3 genera.py && pdflatex t6-fitxa-exercicis.tex (dues vegades) && pdflatex t6-fitxa-solucions.tex (dues vegades)
import os, re
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def pw(*rows, name='f(x)'):
    return name + r'=\begin{cases}' + r'\\[3pt]'.join(r'%s&\text{si }%s' % r for r in rows) + r'\end{cases}'
def m(s): return '$' + s + '$'
def dm(s): return r'\[' + s + r'\]'
def fx(s, n='f'): return m(n + '(x)=' + s)

# ---------- comprovacions amb sympy ----------
x, y, h = sp.symbols('x y h', real=True)
E, ln, sq, sin, cos, tan, atan, asin, acos, pi = sp.E, sp.log, sp.sqrt, sp.sin, sp.cos, sp.tan, sp.atan, sp.asin, sp.acos, sp.pi
R = sp.Rational
NCHK = [0]
def num(e, at): return complex(sp.N(e.subs(x, at), 30))
def D(f, df, pts=(R(7, 10), R(13, 10), R(23, 10))):
    """df es la derivada de f (comprobado en unos cuantos puntos del dominio)."""
    g = sp.diff(f, x)
    for p in pts:
        a, b = num(g, p), num(df, p)
        assert abs(a - b) < 1e-9 * (1 + abs(a)), (f, df, p, a, b)
    NCHK[0] += 1
def Dn(f, n, dfn, pts=(R(7, 10), R(13, 10))):
    D_ = sp.diff(f, x, n)
    for p in pts: assert abs(num(D_ - dfn, p)) < 1e-9, (f, n, dfn)
    NCHK[0] += 1
def eq(a, b):
    assert abs(complex(sp.N(sp.sympify(a) - sp.sympify(b), 30))) < 1e-12, (a, b)
    NCHK[0] += 1
def lim(e, a, d):
    return sp.limit(e, x, a, d)
def lat(f, a, d):
    """derivada lateral por definición"""
    return sp.limit((f.subs(x, a + h) - f.subs(x, a)) / h, h, 0, d)
def chk_pw(fl, fr, a, cont, dl=None, dr=None, fa=None):
    """trozos fl (izquierda) y fr (derecha) en a: continuidad y derivadas laterales (por el límite de f')."""
    L, Rr = lim(fl, a, '-'), lim(fr, a, '+')
    v = fa if fa is not None else Rr
    c = sp.simplify(L - Rr) == 0 and sp.simplify(L - v) == 0
    assert c == cont, (fl, fr, a, L, Rr)
    if dl is not None: eq(lim(sp.diff(fl, x), a, '-'), dl) if dl not in (sp.oo, -sp.oo) else assert_(lim(sp.diff(fl, x), a, '-') == dl)
    if dr is not None: eq(lim(sp.diff(fr, x), a, '+'), dr) if dr not in (sp.oo, -sp.oo) else assert_(lim(sp.diff(fr, x), a, '+') == dr)
    NCHK[0] += 1
def assert_(c):
    assert c; NCHK[0] += 1
def tang(f, a, mm, n0):
    """tangente en a: y = mm x + n0"""
    eq(sp.diff(f, x).subs(x, a), mm); eq(f.subs(x, a) - mm * a, n0)
def impl(F, P, val):
    """y' = -F_x/F_y en el punto P de la curva F = 0"""
    s = {x: P[0], y: P[1]}
    eq(F.subs(s), 0); eq((-sp.diff(F, x) / sp.diff(F, y)).subs(s), val)

S = []  # [(títol, [(estrelles, enunciat, solució)])]
def sec(t, *exs): S.append((t, list(exs)))

# =====================================================================
# 1. Taxa de variació i derivada per definició
eq(((2**3 - 2) - 0) / 3, 2); eq((ln(E) - 0) / (E - 1), 1 / (E - 1)); eq((sin(pi / 2) - 0) / (pi / 2), 2 / pi)
s_ = -5 * x**2 + 20 * x
eq((s_.subs(x, 2) - s_.subs(x, 0)) / 2, 10); eq(sp.limit((s_.subs(x, 1 + h) - s_.subs(x, 1)) / h, h, 0), 10)
for f, a, v in [(1 / x**2, 2, -R(1, 4)), (x / (x + 1), 1, R(1, 4)), (sp.exp(3 * x), 0, 3), (sin(x), pi / 2, 0), (-x**2 + 4 * x + 3, 1, 2)]:
    eq(sp.limit((f.subs(x, a + h) - f.subs(x, a)) / h, h, 0), v)
for f, df in [(x**3, 3 * x**2), (1 / sq(x), -1 / (2 * x * sq(x))), (cos(x), -sin(x)), (ln(2 * x), 1 / x)]:
    assert_(sp.simplify(sp.limit((f.subs(x, x + h) - f) / h, h, 0) - df) == 0)
sec("Tasa de variación y derivada por definición",
 (1, r"Calcula la tasa de variación media de las funciones siguientes en el intervalo indicado:" + tasks(3, [r"$f(x)=x^3-x$ en $[0,2]$", r"$g(x)=\ln x$ en $[1,e]$", r"$h(x)=\sin x$ en $\left[0,\frac\pi2\right]$"])
     + recorda(r"$\text{TVM}[a,b]=\dfrac{f(b)-f(a)}{b-a}$: es la pendiente de la recta secante. La derivada es el límite de la TVM cuando el intervalo se hace tan pequeño como queramos."),
     tasks(3, [r"$\frac{6-0}{2}=\res{3}$", r"$\frac{1-0}{e-1}=\res{\frac{1}{e-1}}$", r"$\frac{1-0}{\pi/2}=\res{\frac2\pi}$"])),
 (2, r"Lanzamos una pelota hacia arriba y su altura, en metros, a los $t$ segundos es $s(t)=-5t^2+20t$. Calcula la velocidad media en los dos primeros segundos y, aplicando la definición de derivada, la velocidad instantánea en $t=1$.",
     r"$v_m=\frac{s(2)-s(0)}{2}=\frac{20}{2}=\res{10\text{ m/s}}$. \ $\dfrac{s(1+h)-s(1)}{h}=\dfrac{-5(1+h)^2+20(1+h)-15}{h}=\dfrac{10h-5h^2}{h}=10-5h\to\res{10\text{ m/s}}$."),
 (2, r"Calcula, aplicando la definición de derivada:" + tasks(2, [r"$f'(2)$ si $f(x)=\dfrac{1}{x^2}$", r"$f'(1)$ si $f(x)=\dfrac{x}{x+1}$", r"$f'(0)$ si $f(x)=e^{3x}$", r"$f'\!\left(\frac\pi2\right)$ si $f(x)=\sin x$"])
     + recorda(r"$f'(a)=\displaystyle\lim_{h\to0}\frac{f(a+h)-f(a)}{h}$. Con exponenciales y funciones trigonométricas, usa los infinitésimos equivalentes: $e^{u}-1\sim u$, \ $1-\cos u\sim\frac{u^2}{2}$, \ $\sin u\sim u$."),
     tasks(1, [r"$\dfrac{\frac{1}{(2+h)^2}-\frac14}{h}=\dfrac{4-(2+h)^2}{4h(2+h)^2}=\dfrac{-4-h}{4(2+h)^2}\to\res{-\frac14}$",
               r"$\dfrac{\frac{1+h}{2+h}-\frac12}{h}=\dfrac{h}{2h(2+h)}\to\res{\frac14}$",
               r"$\dfrac{e^{3h}-1}{h}\sim\dfrac{3h}{h}=\res{3}$",
               r"$\dfrac{\sin\left(\frac\pi2+h\right)-1}{h}=\dfrac{\cos h-1}{h}\sim\dfrac{-h^2/2}{h}\to\res{0}$"])),
 (3, r"Calcula la función derivada aplicando la definición:" + tasks(2, [fx(r'x^3'), fx(r'\dfrac{1}{\sqrt x}'), fx(r'\cos x'), fx(r'\ln(2x)')]),
     tasks(1, [r"$\dfrac{(x+h)^3-x^3}{h}=3x^2+3xh+h^2\to\res{3x^2}$",
               r"$\dfrac{\frac{1}{\sqrt{x+h}}-\frac1{\sqrt x}}{h}=\dfrac{\sqrt x-\sqrt{x+h}}{h\sqrt x\sqrt{x+h}}=\dfrac{-1}{\sqrt x\sqrt{x+h}\left(\sqrt x+\sqrt{x+h}\right)}\to\res{-\dfrac{1}{2x\sqrt x}}$",
               r"$\dfrac{\cos x(\cos h-1)-\sin x\sin h}{h}\to\cos x\cdot0-\sin x\cdot1=\res{-\sin x}$",
               r"$\dfrac{\ln(2x+2h)-\ln(2x)}{h}=\dfrac{\ln\left(1+\frac hx\right)}{h}\sim\dfrac{h/x}{h}=\res{\dfrac1x}$"])),
 (2, r"\pau{Navarra, extraordinaria 2023} Considera la función $g(x)=-x^2+4x+3$. Calcula la derivada de $g(x)$ en el punto $x=1$ aplicando la definición de derivada.",
     r"$g(1+h)=6+2h-h^2$, \ $g(1)=6$: \ $g'(1)=\displaystyle\lim_{h\to0}\frac{2h-h^2}{h}=\res{2}$"),
)

# =====================================================================
# 2. Rectes tangent i normal
tang(x**3 - 3 * x + 1, 2, 9, -15); tang(ln(x**2 - 3), 2, 4, -8)
eq(-R(1, 9) * (0 - 2) + 3, R(29, 9)); eq(-R(1, 4) * (0 - 2), R(1, 2))
tang(1 / (x + 1), 1, -R(1, 4), R(3, 4)); tang(sq(5 + x**2), -2, -R(2, 3), R(5, 3)); tang(x / (x**2 - 4), 1, -R(5, 9), R(2, 9))
for a, n0 in [(2, 11), (-2, 5)]: tang(3 / x + 8, a, -R(3, 4), n0)
tang(5 * x**3 * sp.exp(2 * x) + 1 / (x**2 + 1), 0, 0, 1)
tang(x**3 - 6 * x**2 + 9 * x, 2, -3, 8); assert_(sp.solve(sp.diff(x**3 - 6 * x**2 + 9 * x, x), x) == [1, 3])
a_, b_ = sp.symbols('a b')
assert_(sp.solve([(a_ * x + b_ / x).subs(x, 2) - 4, sp.diff(a_ * x + b_ / x, x).subs(x, 2)], [a_, b_]) == {a_: 1, b_: 4})
assert_(sp.solve([((a_ * x + b_) / (x**2 + 1)).subs(x, 0) - 1, sp.diff((a_ * x + b_) / (x**2 + 1), x).subs(x, 0) - 1], [a_, b_]) == {a_: 1, b_: 1})
hh = x**3 + a_ * x**2 + 3 * x + b_
assert_(sp.solve([hh.subs(x, 1) - 2, sp.diff(hh, x).subs(x, 1)], [a_, b_]) == {a_: -3, b_: 1})
assert_(sorted(sp.solve(2 * a_ - a_**2 + 3, a_)) == [-1, 3]); tang(x**2, 3, 6, -9); tang(x**2, -1, -2, -1)
# (afegits del recull de PAU de tota Espanya, curs 2026/27)
tang(1 / x, 3, -R(1, 9), R(2, 3))
tang((2 * x**2 + 2 * x - 2) / (3 * x**2 + 3), 1, R(2, 3), -R(1, 3)); eq(R(1, 3) + R(3, 2), R(11, 6))
c3 = sp.symbols('c3'); _f = a_ + b_ * cos(x) + c3 * sin(x)
assert_(sp.solve([_f.subs(x, pi / 2) - 1, sp.diff(_f, x).subs(x, pi / 2), _f.subs(x, 0) + 1], [a_, b_, c3]) == {a_: -1, b_: 0, c3: 2})
tang(-x * sp.exp(-x), -1, -2 * E, -E); eq(lim(sp.diff(-x * sp.exp(-x), x), 0, '-'), -1); eq(lim(sp.diff(x * sp.exp(-x), x), 0, '+'), 1)
tang(sq(-x) + E**3, -4, -R(1, 4), 1 + E**3)
sec("Rectas tangente y normal",
 (1, r"Escribe las ecuaciones de las rectas tangente y normal a la gráfica de cada función en el punto indicado:" + tasks(2, [r"$f(x)=x^3-3x+1$ en $x=2$", r"$g(x)=\ln(x^2-3)$ en $x=2$"])
     + recorda(r"Tangente: $y-f(a)=f'(a)(x-a)$. \ Normal (perpendicular a la tangente): $y-f(a)=-\dfrac{1}{f'(a)}(x-a)$; si $f'(a)=0$, la normal es la recta vertical $x=a$."),
     tasks(1, [r"$f(2)=3$, $f'(x)=3x^2-3$, $f'(2)=9$: \ tangente $\res{y=9x-15}$; \ normal $y-3=-\frac19(x-2)\Rightarrow\res{y=-\frac19x+\frac{29}{9}}$",
               r"$g(2)=\ln1=0$, $g'(x)=\frac{2x}{x^2-3}$, $g'(2)=4$: \ tangente $\res{y=4x-8}$; \ normal $\res{y=-\frac14x+\frac12}$"])),
 (2, r"Halla la ecuación de la recta tangente a la gráfica de cada función en el punto indicado:" + tasks(1, [r"\pau{Murcia, julio 2020} $f(x)=\dfrac{1}{x+1}$ en $x=1$.", r"\pau{Navarra, ordinaria 2023} $f(x)=\sqrt{5+x^2}$ en $x=-2$.", r"\pau{Navarra, ordinaria 2022} $f(x)=\dfrac{x}{x^2-4}$ en $x=1$."]),
     tasks(1, [r"$f(1)=\frac12$, $f'(x)=\frac{-1}{(x+1)^2}$, $f'(1)=-\frac14$: \ $\res{y=-\frac14x+\frac34}$",
               r"$f(-2)=3$, $f'(x)=\frac{x}{\sqrt{5+x^2}}$, $f'(-2)=-\frac23$: \ $\res{y=-\frac23x+\frac53}$",
               r"$f(1)=-\frac13$, $f'(x)=\frac{-(x^2+4)}{(x^2-4)^2}$, $f'(1)=-\frac59$: \ $\res{y=-\frac59x+\frac29}$"])),
 (2, r"\pau{Islas Baleares, extraordinaria 2021} Considera la función $f(x)=\dfrac3x+8$." + tasks(1, [r"Halla los puntos de la gráfica en los que la recta tangente es paralela a la recta $3x+4y+5=0$.", "Calcula las ecuaciones de las rectas tangentes en esos puntos."]),
     tasks(1, [r"Pendiente $-\frac34$: \ $-\frac{3}{x^2}=-\frac34\Rightarrow x=\pm2$: \ $\res{\left(2,\frac{19}{2}\right)}$ y $\res{\left(-2,\frac{13}{2}\right)}$",
               r"$\res{y=-\frac34x+11}$ \ y \ $\res{y=-\frac34x+5}$"])),
 (2, r"\pau{Murcia, septiembre 2018} Dada la función $f(x)=5x^3e^{2x}+\dfrac{1}{x^2+1}$, calcula $f'(0)$ y halla la ecuación de la recta tangente a la gráfica en el punto $(0,1)$.",
     r"$f'(x)=15x^2e^{2x}+10x^3e^{2x}-\dfrac{2x}{(x^2+1)^2}\Rightarrow\res{f'(0)=0}$: \ la tangente es horizontal, $\res{y=1}$."),
 (2, r"Dada $f(x)=x^3-6x^2+9x$, halla los puntos donde la tangente es horizontal y la ecuación de la recta tangente paralela a $y=-3x$.",
     r"$f'(x)=3x^2-12x+9=0\Rightarrow x=1,\ x=3$: \ $\res{(1,4)}$ y $\res{(3,0)}$. \ $3x^2-12x+9=-3\Rightarrow(x-2)^2=0$: en $(2,2)$, \ $\res{y=-3x+8}$."),
 (3, r"Halla las rectas tangentes a la parábola $y=x^2$ que pasan por el punto exterior $P(1,-3)$." + recorda(r"$P$ no es de la curva: escribe la tangente en un punto genérico $(a,a^2)$ e impón que pase por $P$."),
     r"Tangente en $(a,a^2)$: $y=2ax-a^2$. Pasa por $P$: $-3=2a-a^2\Rightarrow a=3$ o $a=-1$: \ $\res{y=6x-9}$ \ y \ $\res{y=-2x-1}$."),
 (2, r"Halla los parámetros en cada caso:" + tasks(1, [r"\pau{Madrid, extraordinaria 2022} $a$ y $b$ para que $f(x)=ax+\dfrac bx$ verifique $f(2)=4$ y $f'(2)=0$.",
                                                    r"\pau{Murcia, septiembre 2017} $a$ y $b$ para que $f(x)=\dfrac{ax+b}{x^2+1}$ cumpla $f(0)=1$ y $f'(0)=1$.",
                                                    r"\pau{Andalucía, ordinaria 2024} $a$ y $b$ para que sea horizontal la recta tangente a la gráfica de $h(x)=x^3+ax^2+3x+b$ en el punto $P(1,2)$."]),
     tasks(1, [r"$2a+\frac b2=4$, \ $a-\frac b4=0$: \ $\res{a=1,\ b=4}$", r"$f(0)=b=1$; \ $f'(x)=\frac{a(x^2+1)-(ax+b)2x}{(x^2+1)^2}$, $f'(0)=a=1$: \ $\res{a=1,\ b=1}$",
               r"$h'(1)=6+2a=0\Rightarrow a=-3$; \ $h(1)=1+a+3+b=2\Rightarrow\res{a=-3,\ b=1}$"])),
 (2, r"\pau{La Rioja, ordinaria 2024} Escribe la recta tangente a $y=\dfrac1x$ en el punto $\left(3,\frac13\right)$ y comprueba que el segmento de esta recta comprendido entre los ejes queda dividido en dos partes iguales por el punto de tangencia.",
     r"$y'=-\frac{1}{x^2}$, $y'(3)=-\frac19$: \ $\res{y=-\frac19x+\frac23}$. Corta los ejes en $(6,0)$ y $\left(0,\frac23\right)$, y el punto medio del segmento es $\left(\frac{6+0}{2},\frac{0+2/3}{2}\right)=\left(3,\frac13\right)$."),
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2021} Calcula las rectas tangente y normal a la gráfica de $f(x)=\dfrac{2x^2+2x-2}{3x^2+3}$ en el punto de abscisa $x=1$.",
     r"$f(1)=\frac13$, $f'(x)=\frac{-6x^2+24x+6}{(3x^2+3)^2}\Rightarrow f'(1)=\frac23$: \ tangente $\res{y=\frac23x-\frac13}$; \ normal $\res{y=-\frac32x+\frac{11}{6}}$."),
 (2, r"\pau{Andalucía, extraordinaria 2024} Halla $a$, $b$ y $c$ sabiendo que la gráfica de $f(x)=a+b\cos x+c\sin x$ tiene por recta tangente $y=1$ en el punto de abscisa $x=\frac\pi2$, y que la recta $y=x-1$ corta la gráfica en el punto de abscisa $x=0$.",
     r"$f\left(\frac\pi2\right)=a+c=1$, \ $f'\left(\frac\pi2\right)=-b=0$, \ $f(0)=a+b=-1$: \ $\res{a=-1,\ b=0,\ c=2}$."),
 (3, r"\pau{La Rioja, extraordinaria 2024} Escribe, si existen, las rectas tangentes a la curva $f(x)=|x|\,e^{-x}$ en los puntos de abscisa $x=0$ y $x=-1$." + recorda(r"Escribe primero la función a trozos: $|x|=-x$ si $x<0$."),
     r"En $x=0$: $f'(0^-)=-1\neq1=f'(0^+)$, punto anguloso: \rest{no hay tangente}. En $x=-1$: $f(x)=-xe^{-x}$, $f(-1)=e$, $f'(-1)=-2e$: \ $\res{y=-2ex-e}$."),
 (2, r"\pau{Aragón, ordinaria 2022} Para la función " + '$' + pw((r'\sqrt{-x}+e^3', r'x\leq0'), (r'(1-x)^{a/x}', 'x>0')) + '$' + r" (que es continua para $a=-3$), calcula la recta tangente en $x=-4$.",
     r"$f(-4)=2+e^3$, $f'(x)=\frac{-1}{2\sqrt{-x}}\Rightarrow f'(-4)=-\frac14$: \ $\res{y=-\frac14x+1+e^3}$."),
)

# =====================================================================
# 3. Regles de derivació i derivades successives
D(x**3 * sq(x) - 2 / sp.cbrt(x), R(7, 2) * x**R(5, 2) + R(2, 3) * x**R(-4, 3))
D(x * sp.exp(x) * sin(x), sp.exp(x) * (sin(x) + x * sin(x) + x * cos(x)))
D((x**2 - 1) / (x**2 + 1), 4 * x / (x**2 + 1)**2); D(x**3 / (x - 1), x**2 * (2 * x - 3) / (x - 1)**2)
D((1 - cos(x)) / sin(x), 1 / (1 + cos(x))); D(sp.exp(x) * (x**2 - 2 * x + 2), x**2 * sp.exp(x)); D(x * ln(x), ln(x) + 1)
D(x * atan(x) - ln(x**2 + 1) / 2, atan(x)); D(sin(x) / (1 + cos(x)), 1 / (1 + cos(x)))
Dn(x**4 - 2 * x**3 + x, 3, 24 * x - 12)
for n in range(1, 6):
    Dn(sp.exp(-2 * x), n, (-2)**n * sp.exp(-2 * x)); Dn(x * sp.exp(x), n, (x + n) * sp.exp(x))
    Dn(1 / (x + 1), n, (-1)**n * sp.factorial(n) / (x + 1)**(n + 1)); Dn(ln(x), n, (-1)**(n + 1) * sp.factorial(n - 1) / x**n)
Dn(cos(x), 2027 % 4, sin(x))
yy = sp.exp(-x) * sin(x); assert_(sp.simplify(sp.diff(yy, x, 2) + 2 * sp.diff(yy, x) + 2 * yy) == 0)
c_ = sp.symbols('c'); assert_(sp.solve([2 * a_ - 4, 2 * a_ + b_ - 3, a_ + b_ + c_ - 2], [a_, b_, c_]) == {a_: 2, b_: -1, c_: 1})
sec("Reglas de derivación y derivadas sucesivas",
 (1, r"Deriva y simplifica:" + tasks(2, [fx(r'x^3\sqrt{x}-\dfrac{2}{\sqrt[3]{x}}'), fx(r'x\,e^x\sin x'), fx(r'\dfrac{x^2-1}{x^2+1}'), fx(r'\dfrac{x^3}{x-1}'), fx(r'\dfrac{1-\cos x}{\sin x}'), fx(r'e^x\left(x^2-2x+2\right)')])
     + recorda(r"Escribe raíces e inversas como potencias. Producto de tres: $(fgh)'=f'gh+fg'h+fgh'$. Cociente: $\left(\frac fg\right)'=\frac{f'g-fg'}{g^2}$."),
     tasks(2, [r'$\left(x^{7/2}-2x^{-1/3}\right)^{\prime}=\res{\frac72x^2\sqrt x+\frac{2}{3x\sqrt[3]{x}}}$', r'$\res{e^x(\sin x+x\sin x+x\cos x)}$', r'$\res{\dfrac{4x}{(x^2+1)^2}}$', r'$\res{\dfrac{x^2(2x-3)}{(x-1)^2}}$',
               r'$\dfrac{\sin^2x-(1-\cos x)\cos x}{\sin^2x}=\dfrac{1-\cos x}{1-\cos^2x}=\res{\dfrac{1}{1+\cos x}}$', r'$e^x(x^2-2x+2+2x-2)=\res{x^2e^x}$'])),
 (1, r"\pau{Cantabria, ordinaria 2024} Considera la función $f(x)=x\ln x$ con $x>0$. Calcula la derivada de $f(x)$.",
     r"$f'(x)=1\cdot\ln x+x\cdot\frac1x=\res{\ln x+1}$"),
 (2, r"Comprueba que $F(x)=x\arctan x-\frac12\ln(x^2+1)$ tiene por derivada $\arctan x$.",
     r"$F'(x)=\arctan x+\dfrac{x}{1+x^2}-\dfrac12\cdot\dfrac{2x}{x^2+1}=\res{\arctan x}$ \ (ya lo veremos: $F$ es una \emph{primitiva} de $\arctan x$)."),
 (2, r"Derivadas sucesivas:" + tasks(1, [r"Calcula $f'''(x)$ si $f(x)=x^4-2x^3+x$.", r"Halla la derivada $n$-ésima de $e^{-2x}$, de $x\,e^x$, de $\dfrac{1}{x+1}$ y de $\ln x$.", r"¿Cuál es la derivada 2027.ª de $\cos x$?"])
     + recorda(r"Calcula tres o cuatro, busca el patrón y escríbelo en función de $n$. Las derivadas de $\sin x$ y $\cos x$ se repiten cada cuatro."),
     tasks(1, [r"$f'=4x^3-6x^2+1$, $f''=12x^2-12x$, $\res{f'''=24x-12}$",
               r"$\res{(-2)^ne^{-2x}}$; \ $\res{(x+n)e^x}$; \ $\res{\dfrac{(-1)^n\,n!}{(x+1)^{n+1}}}$; \ $\res{\dfrac{(-1)^{n+1}(n-1)!}{x^n}}$",
               r"$2027=4\cdot506+3$: la misma que la tercera, $\res{\sin x}$"])),
 (2, r"Halla $a$, $b$ y $c$ para que $f(x)=ax^2+bx+c$ cumpla $f(1)=2$, $f'(1)=3$ y $f''(1)=4$.",
     r"$f''=2a=4$, \ $f'(1)=2a+b=3$, \ $f(1)=a+b+c=2$: \ $\res{a=2,\ b=-1,\ c=1}$"),
 (3, r"Comprueba que la función $y=e^{-x}\sin x$ verifica la ecuación $y''+2y'+2y=0$.",
     r"$y'=e^{-x}(\cos x-\sin x)$, \ $y''=-2e^{-x}\cos x$. \ $y''+2y'+2y=e^{-x}\left(-2\cos x+2\cos x-2\sin x+2\sin x\right)=\res{0}$"),
)

# =====================================================================
# 4. Regla de la cadena
for f, df in [((3 * x**2 - 1)**4, 24 * x * (3 * x**2 - 1)**3), (sq(x**2 - 2 * x), (x - 1) / sq(x**2 - 2 * x)), ((x**2 + 1)**-3, -6 * x / (x**2 + 1)**4),
              (sp.cbrt(2 * x + 5), 2 / (3 * sp.cbrt((2 * x + 5)**2))), (sp.exp(3 * x - 1), 3 * sp.exp(3 * x - 1)), (2**(x**2), 2 * x * 2**(x**2) * ln(2)),
              (sin(3 * x)**2, 3 * sin(6 * x)), (cos(x**2), -2 * x * sin(x**2)), (tan(x)**3, 3 * tan(x)**2 * (1 + tan(x)**2)), (atan(2 * x), 2 / (1 + 4 * x**2)),
              (asin(sq(x)), 1 / (2 * sq(x) * sq(1 - x))), (acos(sp.exp(-x)), sp.exp(-x) / sq(1 - sp.exp(-2 * x))),
              (ln(x**2 - 3 * x), (2 * x - 3) / (x**2 - 3 * x)), (ln(sq((1 + x) / (1 - x))), 1 / (1 - x**2)), (ln(x**3 + 1) / ln(2), 3 * x**2 / ((x**3 + 1) * ln(2))),
              (ln(cos(x)), -tan(x)), (ln(x + sq(x**2 + 1)), 1 / sq(x**2 + 1)), (ln(tan(x / 2)), 1 / sin(x)),
              (x * sp.exp(-x**2), (1 - 2 * x**2) * sp.exp(-x**2)), ((x - 1)**2 * (x + 2)**3, (x - 1) * (x + 2)**2 * (5 * x + 1)), (sq(x + sq(x)), (2 * sq(x) + 1) / (4 * sq(x) * sq(x + sq(x)))),
              (sp.exp(sin(x)) * cos(x), sp.exp(sin(x)) * (cos(x)**2 - sin(x))), (sin(ln(x)) + cos(ln(x)), (cos(ln(x)) - sin(ln(x))) / x),
              ((x**2 - 2) * ln(x), 2 * x * ln(x) + (x**2 - 2) / x), (sp.exp(4 * x**3 + 2), 12 * x**2 * sp.exp(4 * x**3 + 2)),
              (x**2 * ln(x**2), 2 * x * ln(x**2) + 2 * x), (sp.exp(-3 * x + x**2), (2 * x - 3) * sp.exp(-3 * x + x**2)),
              (x**3 * sp.exp(2 * x**2), sp.exp(2 * x**2) * (3 * x**2 + 4 * x**4)), ((2 * x - 1) * sp.exp(x**2 - x), (4 * x**2 - 4 * x + 3) * sp.exp(x**2 - x)),
              ((x**2 + 2)**3 * sp.exp(-2 * x), -2 * (x**2 - 3 * x + 2) * (x**2 + 2)**2 * sp.exp(-2 * x))]:
    pts = (R(3, 10), R(1, 2), R(7, 10)) if f.has(asin) or f.has(acos) or f.has(sp.log(sq((1 + x) / (1 - x)))) else (R(7, 10), R(13, 10), R(23, 10))
    if f.has(ln(x**2 - 3 * x)): pts = (R(7, 2), 4, 5)
    if f.has(sq(x**2 - 2 * x)): pts = (R(5, 2), 3, 4)
    D(f, df, pts)
for f, df in [(ln((x - 1) / (x + 1)), 2 / (x**2 - 1)), (ln((x**2 - 1) / (x**2 + 1)), 4 * x / ((x**2 - 1) * (x**2 + 1)))]: D(f, df, (R(5, 2), 3, 4))
D(ln(1 - x**3) / (1 - 2 * x**2)**2, (-3 * x**2 * (1 - 2 * x**2) + 8 * x * (1 - x**3) * ln(1 - x**3)) / ((1 - x**3) * (1 - 2 * x**2)**3), (R(3, 10), R(-4, 5), R(1, 2)))
f_ = x**3 * ln(2 * x + 5) + a_ * x + b_; assert_(sp.solve([f_.subs(x, 0) - 2, sp.diff(f_, x).subs(x, 0) - 1], [a_, b_]) == {a_: 1, b_: 2})
sec("Regla de la cadena",
 (1, r"Deriva estas potencias, raíces y exponenciales:" + tasks(3, [fx(r'(3x^2-1)^4'), fx(r'\sqrt{x^2-2x}'), fx(r'\dfrac{1}{(x^2+1)^3}'), fx(r'\sqrt[3]{2x+5}'), fx(r'e^{3x-1}'), fx(r'2^{x^2}')])
     + recorda(r"$\left[f(g(x))\right]'=f'(g(x))\cdot g'(x)$: derivamos la de fuera, dejando dentro $g(x)$, y multiplicamos por la derivada de la de dentro."),
     tasks(3, [r'$\res{24x(3x^2-1)^3}$', r'$\res{\dfrac{x-1}{\sqrt{x^2-2x}}}$', r'$\res{\dfrac{-6x}{(x^2+1)^4}}$', r'$\res{\dfrac{2}{3\sqrt[3]{(2x+5)^2}}}$', r'$\res{3e^{3x-1}}$', r'$\res{2x\cdot2^{x^2}\ln2}$'])),
 (2, r"Deriva estas funciones trigonométricas y trigonométricas inversas:" + tasks(3, [fx(r'\sin^2(3x)'), fx(r'\cos(x^2)'), fx(r'\tan^3x'), fx(r'\arctan(2x)'), fx(r'\arcsin\sqrt x'), fx(r'\arccos e^{-x}')]),
     tasks(2, [r'$2\sin3x\cos3x\cdot3=\res{3\sin6x}$', r'$\res{-2x\sin(x^2)}$', r'$\res{3\tan^2x\,(1+\tan^2x)}$', r'$\res{\dfrac{2}{1+4x^2}}$', r'$\dfrac{\frac{1}{2\sqrt x}}{\sqrt{1-x}}=\res{\dfrac{1}{2\sqrt x\sqrt{1-x}}}$', r'$\dfrac{-(-e^{-x})}{\sqrt{1-e^{-2x}}}=\res{\dfrac{e^{-x}}{\sqrt{1-e^{-2x}}}}$'])),
 (2, r"Deriva y simplifica (aprovecha las propiedades de los logaritmos antes de derivar):" + tasks(3, [fx(r'\ln(x^2-3x)'), fx(r'\ln\sqrt{\dfrac{1+x}{1-x}}'), fx(r'\log_2(x^3+1)'), fx(r'\ln(\cos x)'), fx(r'\ln\left(x+\sqrt{x^2+1}\right)'), fx(r'\ln\left(\tan\frac x2\right)')]),
     tasks(2, [r'$\res{\dfrac{2x-3}{x^2-3x}}$', r'$\frac12\left[\frac{1}{1+x}+\frac{1}{1-x}\right]=\res{\dfrac{1}{1-x^2}}$', r'$\res{\dfrac{3x^2}{(x^3+1)\ln2}}$', r'$\res{-\tan x}$',
               r'$\dfrac{1+\frac{x}{\sqrt{x^2+1}}}{x+\sqrt{x^2+1}}=\res{\dfrac{1}{\sqrt{x^2+1}}}$', r'$\dfrac{\frac12\left(1+\tan^2\frac x2\right)}{\tan\frac x2}=\dfrac{1}{2\sin\frac x2\cos\frac x2}=\res{\dfrac{1}{\sin x}}$'])),
 (2, r"Deriva y simplifica (hay más de una regla en cada función):" + tasks(2, [fx(r'x\,e^{-x^2}'), fx(r'(x-1)^2(x+2)^3'), fx(r'\sqrt{x+\sqrt x}'), fx(r'e^{\sin x}\cos x'), fx(r'\sin(\ln x)+\cos(\ln x)')]),
     tasks(2, [r'$\res{(1-2x^2)\,e^{-x^2}}$', r'$\res{(x-1)(x+2)^2(5x+1)}$', r'$\res{\dfrac{2\sqrt x+1}{4\sqrt x\,\sqrt{x+\sqrt x}}}$', r'$\res{e^{\sin x}\left(\cos^2x-\sin x\right)}$', r'$\res{\dfrac{\cos(\ln x)-\sin(\ln x)}{x}}$'])),
 (2, r"\pau{Murcia, septiembre 2020} Calcula las derivadas de las funciones siguientes:" + tasks(2, [fx(r'(x^2-2)\ln x'), fx(r'e^{4x^3+2}', 'g')]),
     tasks(2, [r'$\res{2x\ln x+\dfrac{x^2-2}{x}}$', r'$\res{12x^2e^{4x^3+2}}$'])),
 (2, r"\pau{Murcia, junio 2018} Halla las derivadas de las funciones siguientes:" + tasks(2, [fx(r'x^2\ln(x^2)', 'g'), fx(r'e^{-3x+x^2}', 'h')]),
     tasks(2, [r'$\res{2x\ln(x^2)+2x}$', r'$\res{(2x-3)\,e^{-3x+x^2}}$'])),
 (2, r"\pau{Andalucía, ordinaria 2021} Calcula la derivada de las funciones siguientes:" + tasks(2, [fx(r'\ln\left(\dfrac{x-1}{x+1}\right)'), fx(r'x^3\cdot e^{2x^2}', 'g')]),
     tasks(2, [r'$\frac{1}{x-1}-\frac{1}{x+1}=\res{\dfrac{2}{x^2-1}}$', r'$\res{e^{2x^2}\left(3x^2+4x^4\right)}$'])),
 (2, r"\pau{Andalucía, ordinaria (suplente) 2025} Calcula la derivada de las funciones siguientes:" + tasks(2, [fx(r'\ln\left(\dfrac{x^2-1}{x^2+1}\right)', 'g'), fx(r'(2x-1)\,e^{x^2-x}', 'h')]),
     tasks(2, [r'$\res{\dfrac{4x}{(x^2-1)(x^2+1)}}$', r'$\res{(4x^2-4x+3)\,e^{x^2-x}}$'])),
 (3, r"\pau{Andalucía, ordinaria 2024} Calcula la derivada de las funciones siguientes:" + tasks(2, [fx(r'(x^2+2)^3\cdot e^{-2x}'), fx(r'\dfrac{\ln(1-x^3)}{(1-2x^2)^2}', 'g')]),
     tasks(1, [r'$\res{-2(x^2-3x+2)(x^2+2)^2e^{-2x}}$', r'$\res{\dfrac{-3x^2(1-2x^2)+8x(1-x^3)\ln(1-x^3)}{(1-x^3)(1-2x^2)^3}}$'])),
 (2, r"\pau{Murcia, septiembre 2018} Halla $a$ y $b$ para que $f(x)=x^3\ln(2x+5)+ax+b$ cumpla $f(0)=2$ y $f'(0)=1$.",
     r"$f(0)=b=2$; \ $f'(x)=3x^2\ln(2x+5)+\dfrac{2x^3}{2x+5}+a$, \ $f'(0)=a=1$: \ $\res{a=1,\ b=2}$"),
)

# =====================================================================
# 5. Derivació logarítmica
for f, df in [(x**x, x**x * (ln(x) + 1)), (x**sin(x), x**sin(x) * (cos(x) * ln(x) + sin(x) / x)), (x**ln(x), 2 * ln(x) * x**(ln(x) - 1)), (x**(1 / x), x**(1 / x) * (1 - ln(x)) / x**2),
              ((x**2 + 1)**x, (x**2 + 1)**x * (ln(x**2 + 1) + 2 * x**2 / (x**2 + 1))), (ln(x)**x, ln(x)**x * (ln(ln(x)) + 1 / ln(x))),
              (cos(x)**sin(x), cos(x)**sin(x) * (cos(x) * ln(cos(x)) - sin(x)**2 / cos(x))), (x**(x**2), x**(x**2 + 1) * (2 * ln(x) + 1)),
              (x**3 * (x + 1)**5 / sq(x**2 + 4), x**3 * (x + 1)**5 / sq(x**2 + 4) * (3 / x + 5 / (x + 1) - x / (x**2 + 4))),
              ((x - 1)**2 * sp.cbrt(x + 2) / (x + 3)**4, (x - 1)**2 * sp.cbrt(x + 2) / (x + 3)**4 * (2 / (x - 1) + 1 / (3 * (x + 2)) - 4 / (x + 3)))]:
    D(f, df, (R(11, 10), R(13, 10), R(3, 2)))
tang(x**x, 1, 1, 0); tang(x**x, 2, 4 + 4 * ln(2), -4 - 8 * ln(2)); assert_(sp.solve(ln(x) + 1, x) == [sp.exp(-1)])
sec("Derivación logarítmica",
 (2, r"Deriva aplicando la derivación logarítmica:" + tasks(2, [m(r'y=x^x'), m(r'y=x^{\sin x}'), m(r'y=x^{\ln x}'), m(r'y=x^{1/x}'), m(r'y=(x^2+1)^x'), m(r'y=(\ln x)^x\ \ (x>1)'), m(r'y=(\cos x)^{\sin x}\ \ \left(0<x<\frac\pi2\right)'), m(r'y=x^{x^2}')])
     + recorda(r"Tomamos logaritmos: $\ln y=v\ln u$. Derivamos los dos miembros: $\dfrac{y'}{y}=v'\ln u+v\dfrac{u'}{u}$. Despejamos $y'$ y sustituimos $y$."),
     tasks(1, [r'$\ln y=x\ln x\Rightarrow\res{y^{\prime}=x^x(\ln x+1)}$', r'$\res{y^{\prime}=x^{\sin x}\left(\cos x\ln x+\dfrac{\sin x}{x}\right)}$',
               r'$\ln y=(\ln x)^2\Rightarrow\res{y^{\prime}=\dfrac{2\ln x}{x}\,x^{\ln x}}$', r'$\ln y=\dfrac{\ln x}{x}\Rightarrow\res{y^{\prime}=x^{1/x}\,\dfrac{1-\ln x}{x^2}}$',
               r'$\res{y^{\prime}=(x^2+1)^x\left(\ln(x^2+1)+\dfrac{2x^2}{x^2+1}\right)}$', r'$\res{y^{\prime}=(\ln x)^x\left(\ln(\ln x)+\dfrac{1}{\ln x}\right)}$',
               r'$\res{y^{\prime}=(\cos x)^{\sin x}\left(\cos x\ln(\cos x)-\dfrac{\sin^2x}{\cos x}\right)}$', r'$\ln y=x^2\ln x\Rightarrow\res{y^{\prime}=x^{x^2+1}(2\ln x+1)}$'])),
 (2, r"Deriva con la derivación logarítmica (es más rápido que con las reglas del producto y del cociente):" + tasks(2, [m(r'y=\dfrac{x^3(x+1)^5}{\sqrt{x^2+4}}\ \ (x>0)'), m(r'y=\dfrac{(x-1)^2\sqrt[3]{x+2}}{(x+3)^4}\ \ (x>1)')]),
     tasks(1, [r'$\res{y^{\prime}=\dfrac{x^3(x+1)^5}{\sqrt{x^2+4}}\left(\dfrac3x+\dfrac{5}{x+1}-\dfrac{x}{x^2+4}\right)}$', r'$\res{y^{\prime}=\dfrac{(x-1)^2\sqrt[3]{x+2}}{(x+3)^4}\left(\dfrac{2}{x-1}+\dfrac{1}{3(x+2)}-\dfrac{4}{x+3}\right)}$'])),
 (2, r"Considera la función $f(x)=x^x$, con $x>0$." + tasks(1, [r"Halla las rectas tangentes a la gráfica en $x=1$ y en $x=2$.", r"¿En qué punto la tangente es horizontal?", r"Explica por qué es incorrecto derivarla como si fuera una potencia, $(x^x)'=x\cdot x^{x-1}$, o como si fuera una exponencial, $(x^x)'=x^x\ln x$."]),
     tasks(1, [r"$f'(x)=x^x(\ln x+1)$: \ $f(1)=1$, $f'(1)=1$: $\res{y=x}$; \ $f(2)=4$, $f'(2)=4(1+\ln2)$: $\res{y=4(1+\ln2)(x-2)+4}$",
               r"$\ln x+1=0\Rightarrow x=\frac1e$: \ $\res{\left(\frac1e,\ e^{-1/e}\right)}$",
               r"La regla de la potencia exige exponente constante, y la de la exponencial, base constante. Aquí varían ambas: de hecho, $(x^x)'$ es la \rest{suma} de las dos expresiones incorrectas, $x\cdot x^{x-1}+x^x\ln x$."])),
)

# =====================================================================
# 6. Derivació implícita
for F, val, P in [(x**2 + y**2 - 4 * x, (2 - x) / y, (1, sq(3))), (x**3 + y**3 - 3 * x * y, (y - x**2) / (y**2 - x), (R(3, 2), R(3, 2))),
                  (x**2 * y + x * y**2 - 6, -(2 * x * y + y**2) / (x**2 + 2 * x * y), (1, 2)), (sp.exp(x * y) - x - y, (1 - y * sp.exp(x * y)) / (x * sp.exp(x * y) - 1), (0, 1)),
                  (sq(x) + sq(y) - 3, -sq(y) / sq(x), (1, 4)), (x - y - ln(y), y / (y + 1), (1, 1))]:
    impl(F, P, val.subs({x: P[0], y: P[1]}))
impl(x**2 + x * y + y**2 - 7, (2, 1), -R(5, 4)); impl(x**3 + y**3 - 9 * x * y, (2, 4), R(4, 5)); impl(9 * x**2 + 16 * y**2 - 144, (R(16, 5), R(9, 5)), -1); impl(y**2 - x**3, (1, 1), R(3, 2))
eq(-R(5, 4) * (0 - 2) + 1, R(7, 2)); eq(R(4, 5) * (0 - 2) + 1, -R(3, 5)); eq(R(4, 5) * (0 - 2) + 4, R(12, 5))
Fh = x**2 + x * y + y**2 - 3
assert_(sorted(sp.solve([Fh, 2 * x + y], [x, y])) == [(-1, 2), (1, -2)]); assert_(sorted(sp.solve([Fh, x + 2 * y], [x, y])) == [(-2, 1), (2, -1)])
Fxy = y * ln(x) - x * ln(y); eq(Fxy.subs({x: 2, y: 4}), 0)
eq((-sp.diff(Fxy, x) / sp.diff(Fxy, y)).subs({x: 2, y: 4}), 4 * (ln(2) - 1) / (2 * ln(2) - 1))
sec("Derivación implícita",
 (2, r"Calcula $y'$ en cada caso:" + tasks(2, [m(r'x^2+y^2=4x'), m(r'x^3+y^3=3xy'), m(r'x^2y+xy^2=6'), m(r'e^{xy}=x+y'), m(r'\sqrt x+\sqrt y=3'), m(r'x=y+\ln y')])
     + recorda(r"Derivamos los dos miembros respecto a $x$ pensando que $y=y(x)$: $(y^2)'=2y\,y'$, \ $(xy)'=y+x\,y'$, \ $(e^{y})'=e^{y}\,y'$. Después despejamos $y'$."),
     tasks(2, [r'$2x+2yy^{\prime}=4\Rightarrow\res{y^{\prime}=\dfrac{2-x}{y}}$', r'$\res{y^{\prime}=\dfrac{y-x^2}{y^2-x}}$', r'$\res{y^{\prime}=-\dfrac{2xy+y^2}{x^2+2xy}}$', r'$e^{xy}(y+xy^{\prime})=1+y^{\prime}\Rightarrow\res{y^{\prime}=\dfrac{1-ye^{xy}}{xe^{xy}-1}}$',
               r'$\res{y^{\prime}=-\dfrac{\sqrt y}{\sqrt x}}$', r'$1=y^{\prime}+\dfrac{y^{\prime}}{y}\Rightarrow\res{y^{\prime}=\dfrac{y}{y+1}}$'])),
 (2, r"Halla la recta tangente (y, en el primer caso, también la normal) a cada curva en el punto indicado. Comprueba primero que el punto es de la curva." + tasks(1, [r"$x^2+xy+y^2=7$ en $(2,1)$", r"$x^3+y^3=9xy$ en $(2,4)$", r"$\dfrac{x^2}{16}+\dfrac{y^2}{9}=1$ en $\left(\frac{16}{5},\frac95\right)$", r"$y^2=x^3$ en $(1,1)$"]),
     tasks(1, [r"$y^{\prime}=-\frac{2x+y}{x+2y}=-\frac54$: \ tangente $\res{y=-\frac54x+\frac72}$; \ normal $\res{y=\frac45x-\frac35}$",
               r"$y^{\prime}=\frac{3y-x^2}{y^2-3x}=\frac{8}{10}$: \ $\res{y=\frac45x+\frac{12}{5}}$",
               r"$9x^2+16y^2=144$: $y^{\prime}=-\frac{9x}{16y}=-1$: \ $\res{y=-x+5}$",
               r"$2yy^{\prime}=3x^2$: $y^{\prime}=\frac32$: \ $\res{y=\frac32x-\frac12}$"])),
 (3, r"¿En qué puntos de la curva $x^2+xy+y^2=3$ la recta tangente es horizontal? ¿Y vertical?",
     r"$y'=-\dfrac{2x+y}{x+2y}$. Horizontal si $2x+y=0$: $3x^2=3$, \ $\res{(1,-2)}$ y $\res{(-1,2)}$. Vertical si $x+2y=0$ (denominador nulo): $3y^2=3$, \ $\res{(-2,1)}$ y $\res{(2,-1)}$."),
 (3, r"Calcula la derivada segunda $y''$ y exprésala en función de $x$ y $y$ (o solo de $y$):" + tasks(3, [m(r'x^2+y^2=r^2'), m(r'x^2-y^2=1'), m(r'y^3+y=x')]),
     tasks(1, [r"$y^{\prime}=-\frac xy$, \ $y^{\prime\prime}=-\frac{y-xy^{\prime}}{y^2}=\res{-\dfrac{r^2}{y^3}}$", r"$y^{\prime}=\frac xy$, \ $\res{y^{\prime\prime}=\dfrac{y^2-x^2}{y^3}=-\dfrac{1}{y^3}}$",
               r"$y^{\prime}=\frac{1}{3y^2+1}$, \ $\res{y^{\prime\prime}=\dfrac{-6y\,y^{\prime}}{(3y^2+1)^2}=\dfrac{-6y}{(3y^2+1)^3}}$"])),
 (2, r"Deduce, derivando implícitamente, las derivadas de $y=\ln x$ (a partir de $e^y=x$), de $y=\arcsin x$ (a partir de $\sin y=x$) y de $y=\arctan x$ (a partir de $\tan y=x$).",
     tasks(1, [r"$e^yy^{\prime}=1\Rightarrow\res{y^{\prime}=\frac{1}{e^y}=\frac1x}$", r"$\cos y\,y^{\prime}=1\Rightarrow\res{y^{\prime}=\frac{1}{\sqrt{1-\sin^2y}}=\frac{1}{\sqrt{1-x^2}}}$",
               r"$(1+\tan^2y)\,y^{\prime}=1\Rightarrow\res{y^{\prime}=\frac{1}{1+x^2}}$"])),
 (3, r"Las dos técnicas a la vez. El punto $(2,4)$ es de la curva $x^y=y^x$, ya que $2^4=4^2$. Halla la pendiente de la tangente en este punto." + recorda(r"Toma primero logaritmos ($y\ln x=x\ln y$) y después deriva implícitamente."),
     r"$y^{\prime}\ln x+\dfrac yx=\ln y+\dfrac{x\,y^{\prime}}{y}$. En $(2,4)$: $y^{\prime}\left(\ln2-\frac12\right)=2\ln2-2$: \ $\res{y^{\prime}=\dfrac{4(\ln2-1)}{2\ln2-1}\approx-3{,}18}$"),
)

# =====================================================================
# 7. Continuïtat i derivabilitat
for f, a, l, r_ in [(sp.Abs(x + 1), -1, -1, 1), (sp.Abs(x**2 - 9), 3, -6, 6), (x * sp.Abs(x - 1), 1, -1, 1), (sp.Abs(sin(x)), pi, -1, 1), (x**2 * sp.Abs(x), 0, 0, 0)]:
    eq(lat(f, a, '-'), l); eq(lat(f, a, '+'), r_)
assert_(lat(sp.cbrt(x**2), 0, '+') == sp.oo)
assert_(sp.limit(h * sin(1 / h), h, 0) == 0)
sec("Continuidad y derivabilidad",
 (2, r"Calcula las derivadas laterales en el punto indicado y di si la función es derivable en él:" + tasks(2, [r"$f(x)=|x+1|$ en $x=-1$", r"$f(x)=|x^2-9|$ en $x=3$", r"$f(x)=x\,|x-1|$ en $x=1$", r"$f(x)=\sqrt[3]{x^2}$ en $x=0$", r"$f(x)=|\sin x|$ en $x=\pi$", r"$f(x)=x^2|x|$ en $x=0$"])
     + recorda(r"$f'(a^\pm)=\displaystyle\lim_{h\to0^\pm}\frac{f(a+h)-f(a)}{h}$. Es derivable si ambas existen, son finitas y son iguales."),
     tasks(2, [r"$-1\neq1$: \rest{no} (anguloso)", r"$-6\neq6$: \rest{no}", r"$-1\neq1$: \rest{no}", r"$\frac{h^{2/3}}{h}\to\mp\infty$: \rest{no} (retroceso)", r"$-1\neq1$: \rest{no}", r"$\frac{h^2|h|}{h}\to0$: \rest{sí}, $f'(0)=0$"])),
 (1, r"Razona si son verdaderas o falsas. Si son falsas, pon un contraejemplo:" + tasks(1, [r"Si $f$ es continua en $x=a$, entonces es derivable en $x=a$.", r"Si $f$ no es continua en $x=a$, entonces no es derivable en $x=a$.", r"Si $f$ y $g$ no son derivables en $x=a$, $f+g$ tampoco lo es.", r"Si $f$ es derivable en $x=a$, $|f|$ también lo es."]),
     tasks(1, [r"\rest{Falso}: $|x|$ en $x=0$.", r"\rest{Verdadero}: es el contrarrecíproco de «derivable $\Rightarrow$ continua».", r"\rest{Falso}: $|x|+(-|x|)=0$.", r"\rest{Falso}: $f(x)=x$ es derivable en 0 y $|x|$ no."])),
 (2, r"\pau{Galicia, ordinaria 2026} Dibuja, cuando sea posible, la gráfica de una función continua pero no derivable en $x=0$.",
     r"\rest{Es posible}: por ejemplo $f(x)=|x|$ (punto anguloso en el origen) o $f(x)=\sqrt[3]{x}$ (tangente vertical)."),
 (3, r"Sea $f(x)=x^2\sin\dfrac1x$ si $x\neq0$ y $f(0)=0$. Demuestra, aplicando la definición, que $f$ es derivable en $x=0$. ¿Pasa lo mismo con $g(x)=x\sin\dfrac1x$, $g(0)=0$?" + recorda(r"Si una función tiende a 0 y la otra está acotada, el producto tiende a 0."),
     r"$\dfrac{f(h)-f(0)}{h}=h\sin\dfrac1h\to0$ (0 por acotada): \ $\res{f'(0)=0}$. \ En cambio, $\dfrac{g(h)}{h}=\sin\dfrac1h$ oscila entre $-1$ y $1$: \ $g$ \rest{no es derivable} en 0 (aunque es continua)."),
)

# =====================================================================
# 8. Derivabilitat de funcions a trossos
chk_pw(sp.exp(x), x + 1, 0, True, 1, 1); chk_pw(3 - x**2, 2 / x, 1, True, -2, -2)
chk_pw(-x**2 + 4 * x + 3, 2 * x - 5, 4, True, -4, 2)
chk_pw(10 + 5 * x / 2, x**2 + 1, -2, True, R(5, 2), -4, fa=5)
chk_pw(x**2 - 8 * x + 60, -x**2 + 32 * x - 140, 10, True, 12, 12, fa=80)
chk_pw(-x**2 - 4 * x, 4 - x, -1, False); chk_pw(4 - x, x**2 - 6 * x + 8, 1, True, -1, -4)
chk_pw(2**(x + 1), x**2 - 2 * x, 0, False)
chk_pw(x, x * ln(x), 0, True, 1, -sp.oo, fa=0)
chk_pw(x / 2, 3 - (x - 5)**2, 4, True, R(1, 2), 2)
a34, b34 = R(3, 4), -R(1, 4)
chk_pw(1 / x, a34 * x + b34, -1, True, -1, a34, fa=-1); chk_pw(a34 * x + b34, x**2 / (x + 1), 1, True, a34, a34)
chk_pw(sin(x), ln(1 + x), 0, True, 1, 1); chk_pw(cos(x), 1 + x**2, 0, True, 0, 0)
t = x
chk_pw(-t**2 + 2 * t - R(3, 10), R(1, 10) * t - R(12, 100), R(18, 10), True, -R(16, 10), R(1, 10))
chk_pw(R(1, 10) * t - R(12, 100), -R(1, 2) * t**2 + R(83, 10) * t - R(2862, 100), 5, True, R(1, 10), R(33, 10))
for f, cuts in [(sp.Abs(x - 1) + sp.Abs(x + 1), [-1, 1]), (x * sp.Abs(x - 2), [2]), (sp.exp(-sp.Abs(x)), [0]), (sp.Abs(x**2 - 5 * x + 4), [1, 4])]:
    for c in cuts: assert_(sp.simplify(lat(f, c, '-') - lat(f, c, '+')) != 0)
sec("Derivabilidad de funciones a trozos",
 (2, r"Estudia la continuidad y la derivabilidad de las funciones siguientes:" + tasks(2, ['$' + pw((r'e^x', 'x<0'), (r'x+1', r'x\geq0')) + '$', '$' + pw((r'3-x^2', 'x<1'), (r'\dfrac2x', r'x\geq1'), name='g(x)') + '$'])
     + recorda(r"Primero la continuidad. Después derivamos trozo a trozo (sin el igual en los puntos de cambio) y, en cada punto de cambio donde es continua, comparamos $f'(a^-)$ y $f'(a^+)$."),
     tasks(2, [r"$1=1$; $f'(0^-)=e^0=1=f'(0^+)$: \rest{derivable en $\mathbb R$}", r"$2=2$; $g'(1^-)=-2=-\frac{2}{1^2}=g'(1^+)$: \rest{derivable en $\mathbb R$}"])),
 (2, r"\pau{Andalucía, extraordinaria 2024} Estudia la continuidad y la derivabilidad de" + dm(pw((r'-x^2+4x+3', 'x<4'), (r'2x-5', r'x\geq4'))),
     r"$x=4$: $3=3$, continua. $f'(4^-)=-2\cdot4+4=-4\neq2=f'(4^+)$: \ continua en $\mathbb R$, \rest{derivable en $\mathbb R-\{4\}$}."),
 (2, r"\pau{Andalucía, ordinaria (suplente) 2025} Estudia la continuidad y la derivabilidad de $f$ en el punto de abscisa $x=-2$:" + dm(pw((r'10+\dfrac{5x}{2}', r'x\leq-2'), (r'x^2+1', r'-2<x<2'), (r'10-\dfrac{5x}{2}', r'x\geq2'))),
     r"$f(-2)=5=\displaystyle\lim_{x\to-2^+}(x^2+1)$: continua. $f'(-2^-)=\frac52\neq-4=f'(-2^+)$: \ \rest{no derivable en $x=-2$}."),
 (2, r"\pau{Andalucía, ordinaria 2024} La velocidad del viento, en km/h, prevista para cierto día en una zona de Sierra Nevada viene dada por" + dm(pw((r't^2-8t+60', r'0\leq t\leq10'), (r'-t^2+32t-140', r'10<t\leq24'), name='v(t)')) + r"donde $t$ es el tiempo en horas. Comprueba que la función $v$ es continua y derivable.",
     r"$t=10$: $80=80$. \ $v'(10^-)=2\cdot10-8=12$, \ $v'(10^+)=-20+32=12$: \ \rest{continua en $[0,24]$ y derivable en $(0,24)$}, con $v'(10)=12$."),
 (2, r"\pau{Navarra, ordinaria 2024} Estudia la continuidad (clasificando las discontinuidades) y la derivabilidad de" + dm(pw((r'-x^2-4x', r'x<-1'), (r'4-x', r'-1\leq x<1'), (r'x^2-6x+8', r'x\geq1'))),
     r"$x=-1$: $3\neq5$, \rest{salto finito} (no derivable). $x=1$: $3=3$, continua; $f'(1^-)=-1\neq-4=f'(1^+)$. \ \rest{Continua en $\mathbb R-\{-1\}$, derivable en $\mathbb R-\{-1,1\}$}."),
 (2, r"\pau{Andalucía, extraordinaria 2021} Estudia la continuidad y la derivabilidad de" + dm(pw((r'2^{x+1}', 'x<0'), (r'x^2-2x', r'x\geq0'))),
     r"$\displaystyle\lim_{x\to0^-}2^{x+1}=2\neq0=f(0)$: salto finito en $x=0$. \ \rest{Continua y derivable en $\mathbb R-\{0\}$}."),
 (3, r"\pau{Madrid, extraordinaria 2022 (ampliado)} Estudia la continuidad y la derivabilidad en $x=0$ de" + dm(pw((r'x', r'x\leq0'), (r'x\ln x', 'x>0'))),
     r"$\displaystyle\lim_{x\to0^+}x\ln x=0=f(0)$: \rest{continua}. $f'(0^-)=1$, \ $f'(0^+)=\displaystyle\lim_{x\to0^+}(\ln x+1)=-\infty$: \ \rest{no derivable en $x=0$}."),
 (2, r"\pau{Asturias, ordinaria 2025 (ampliado)} Estudia la continuidad y la derivabilidad de" + dm(pw((r'\dfrac x2', r'0\leq x<4'), (r'3-(x-5)^2', r'4\leq x'))),
     r"$x=4$: $2=2$, continua en $[0,+\infty)$. $f'(4^-)=\frac12\neq2=f'(4^+)$: \ \rest{derivable en $(0,4)\cup(4,+\infty)$}."),
 (3, r"\pau{Andalucía, ordinaria 2022 (ampliado)} Considera la función continua" + dm(pw((r'\dfrac1x', r'x<-1'), (r'ax+b', r'-1\leq x<1'), (r'\dfrac{x^2}{x+1}', r'x\geq1'))) + tasks(1, [r"Calcula $a$ y $b$.", r"Estudia la derivabilidad de $f$."]),
     tasks(1, [r"$-1=-a+b$ y $a+b=\frac12$: \ $\res{a=\frac34,\ b=-\frac14}$",
               r"$x=-1$: $f'(-1^-)=-\frac{1}{(-1)^2}=-1\neq\frac34$; \ $x=1$: $f'(1^-)=\frac34$ y $f'(1^+)=\frac{x^2+2x}{(x+1)^2}\big|_{x=1}=\frac34$. \ \rest{Derivable en $\mathbb R-\{-1\}$}."])),
 (2, r"Estudia la derivabilidad de" + tasks(2, ['$' + pw((r'\sin x', r'x\leq0'), (r'\ln(1+x)', 'x>0')) + '$', '$' + pw((r'\cos x', r'x\leq0'), (r'1+x^2', 'x>0'), name='g(x)') + '$']),
     tasks(2, [r"$0=0$; $f'(0^\pm)=1$: \rest{derivable en $(-1,+\infty)$}", r"$1=1$; $g'(0^-)=-\sin0=0=g'(0^+)$: \rest{derivable en $\mathbb R$}"])),
 (3, r"\pau{Andalucía, extraordinaria 2021} El número de diagnosticados por PCR en Andalucía, en miles de personas, se aproxima por" + dm(pw((r'-t^2+2t-0{,}3', r'0{,}2\leq t\leq1{,}8'), (r'0{,}1t-0{,}12', r'1{,}8<t\leq5'), (r'-0{,}5t^2+8{,}3t-28{,}62', r'5<t\leq10'), name='f(t)')) + r"donde $t$ es el tiempo en meses. Estudia la continuidad y la derivabilidad de $f$.",
     r"$t=1{,}8$: $0{,}06=0{,}06$; $f'(1{,}8^-)=-1{,}6\neq0{,}1$. \ $t=5$: $0{,}38=0{,}38$; $f'(5^-)=0{,}1\neq3{,}3$. \ \rest{Continua en $[0{,}2;\,10]$, derivable en $(0{,}2;\,10)-\{1{,}8;\ 5\}$}."),
 (3, r"Escribe a trozos y estudia la derivabilidad de:" + tasks(2, [fx(r'|x-1|+|x+1|'), fx(r'x\,|x-2|', 'g'), fx(r'e^{-|x|}', 'h'), fx(r'|x^2-5x+4|', 'k')]),
     tasks(1, [r"$f=-2x$ ($x<-1$), $2$ ($-1\leq x\leq1$), $2x$ ($x>1$): \rest{derivable en $\mathbb R-\{-1,1\}$}", r"$g'(2^-)=-2\neq2=g'(2^+)$: \rest{$\mathbb R-\{2\}$}",
               r"$h'(0^-)=1\neq-1=h'(0^+)$: \rest{$\mathbb R-\{0\}$}", r"$x^2-5x+4<0$ en $(1,4)$; $k'(1^\mp)=\mp3$, $k'(4^\mp)=\mp3$: \rest{$\mathbb R-\{1,4\}$}"])),
)

# =====================================================================
# 9. Funcions a trossos amb paràmetres
def solve2(eqs, vs): return sp.solve(eqs, vs, dict=True)
assert_(solve2([3 - (a_ + b_ + 2), 6 - (2 * a_ + b_)], [a_, b_]) == [{a_: 5, b_: -4}])
assert_(solve2([2 - a_ - (a_ + b_), -a_ - b_], [a_, b_]) == [{a_: 2, b_: -2}])
assert_(sp.solve(8 + a_ + 1, a_) == [-9])
eq((-4 * x + a_).subs(x, -2).subs(a_, -9), (x**2 - 5).subs(x, -2)); eq((x**2 - 5).subs(x, 1), (-7 * x + 3).subs(x, 1))
assert_(solve2([2 * sq(3) - sq(b_), sq(3 * a_ + b_) - 3], [a_, b_]) == [{a_: -1, b_: 12}])
chk_pw(x**2 + 2 * sq(3), sq(12 - x), 0, True, 0, -1 / (4 * sq(3))); chk_pw(sq(12 - x), R(7, 2) - x / 6, 3, True, -R(1, 6), -R(1, 6))
tt = sp.Rational(5, 2)
assert_(solve2([(-x**2 + 2 * x + 10).subs(x, tt) - (x**2 + a_ * x + b_).subs(x, tt), sp.diff(-x**2 + 2 * x + 10, x).subs(x, tt) - sp.diff(x**2 + a_ * x + b_, x).subs(x, tt)], [a_, b_]) == [{a_: -8, b_: R(45, 2)}])
m_ = sp.symbols('m'); assert_(set(sp.solve(5 - (m_**2 + 1), m_)) & set(sp.solve((2 + m_)**2, m_)) == {-2})
chk_pw(5 * sp.exp(2 * x), (x - 2)**2 + 1, 0, True, 10, -4); chk_pw((x - 2)**2 + 1, sp.Integer(1) + 0 * x, 2, True, 0, 0)
assert_(solve2([2 + a_ + b_, 2 - a_ + b_ - 5], [a_, b_]) == [{a_: -R(5, 2), b_: R(1, 2)}]); chk_pw(2 * x**2 - R(5, 2) * x + R(1, 2), ln(x), 1, True, R(3, 2), 1)
assert_(sorted(sp.solve(5 - a_ - 6 / a_, a_)) == [2, 3])
assert_(solve2([a_ + b_, 2 * a_ + b_ - 1], [a_, b_]) == [{a_: 1, b_: -1}]); assert_(solve2([a_ + b_ - 1, 2 * a_ + 1], [a_, b_]) == [{a_: -R(1, 2), b_: R(3, 2)}])
assert_(solve2([1 + b_ - 3, a_ - 2], [a_, b_]) == [{a_: 2, b_: 2}]); chk_pw(sp.exp(2 * x) + 2, sin(2 * x) + 3, 0, True, 2, 2)
chk_pw(sp.Integer(0) + x, atan(x), 0, True, 1, 1)
# (afegits del recull de PAU de tota Espanya, curs 2026/27)
k2, m2, k_ = sp.symbols('k2 m2 k')
assert_(solve2([k2 + 2 - (1 - m2), 2 * k2 + 2 - 2], [k2, m2]) == [{k2: 0, m2: -1}])
assert_(lim(-x * sp.exp(x) / x, 0, '+') == -1); chk_pw(x**2 - x - 1, -sp.exp(x), 0, True, -1, -1)
assert_(solve2([a_ - 1 - b_, -1 - (-b_ - 1)], [a_, b_]) == [{a_: 1, b_: 0}]); chk_pw(1 - x, -ln(x), 1, True, -1, -1)
assert_(solve2([1 - b_, -a_ - b_], [a_, b_]) == [{a_: -1, b_: 1}]); chk_pw(x**2 + x + 1, sp.exp(x), 0, True, 1, 1)
assert_(solve2([a_ + b_ - 2, a_ - 1], [a_, b_]) == [{a_: 1, b_: 1}]); chk_pw((x**2 - 1) / (x - 1), x + 1, 1, True, 1, 1)
_g = 2 * sp.exp(x) / (1 + x**2); chk_pw(3 * x**2 - sin(-2 * x) + 2, _g, 0, True, 2, 2); tang(_g, 2, 2 * E**2 / 25, 6 * E**2 / 25)
assert_(sorted(sp.solve(3 - k_ - 2 / k_, k_)) == [1, 2]); assert_(sorted(sp.solve(-2 * k_ + 2 / k_, k_)) == [-1, 1]); chk_pw(3 - x**2, 2 / x, 1, True, -2, -2)
sec("Funciones a trozos con parámetros",
 (2, r"\pau{Andalucía, ordinaria 2022} Determina $a$ y $b$ para que $f$ sea continua y derivable en todo su dominio:" + dm(pw((r'6x-3', r'x\leq1'), (r'ax^2+bx+2', 'x>1')))
     + recorda(r"En cada punto de cambio: continuidad ($\lim^-=\lim^+=f(a)$) y derivabilidad ($f'(a^-)=f'(a^+)$). Con dos parámetros, un sistema de dos ecuaciones."),
     r"$3=a+b+2$ \ y \ $6=2a+b$: \ $\res{a=5,\ b=-4}$"),
 (2, r"\pau{Andalucía, extraordinaria 2020} Calcula $a$ y $b$ para que la función sea continua y derivable en su dominio:" + dm(pw((r'2+\dfrac{a}{x-1}', 'x<0'), (r'a+be^x', r'x\geq0'))),
     r"$2-a=a+b$; \ $f'(0^-)=-a$, $f'(0^+)=b$: \ $\res{a=2,\ b=-2}$"),
 (2, r"Calcula los valores de $a$ para que $f$ sea continua y derivable:" + tasks(1, [r"\pau{Islas Baleares, ordinaria 2022} \ $" + pw((r'x^2-3x+2', 'x<0'), (r'x^2+ax+2', r'x\geq0')) + "$", r"\pau{Islas Baleares, ordinaria 2021} \ $" + pw((r'x^2-3x+2', 'x<0'), (r'e^{ax}+1', r'x\geq0')) + "$"]),
     tasks(1, [r"Continua para todo $a$; $-3=a$: \ $\res{a=-3}$", r"Continua para todo $a$ ($2=e^0+1$); $-3=a\,e^0$: \ $\res{a=-3}$"])),
 (2, r"\pau{Islas Baleares, extraordinaria 2021} Considera" + dm(pw((r'-4x+a', r'x\leq-2'), (r'x^2-5', r'-2<x<1'), (r'-7x+3', r'x\geq1'))) + tasks(1, [r"Calcula los valores de $a$ para que $f$ sea continua.", r"¿Es $f$ derivable para $a=1$?"]),
     tasks(1, [r"$x=-2$: $8+a=-1\Rightarrow\res{a=-9}$ ($x=1$: $-4=-4$ siempre)", r"Para $a=1$ no es continua en $x=-2$ $\Rightarrow$ no derivable. En $x=1$: $f'(1^-)=2\neq-7$. \ \rest{No es derivable ni en $-2$ ni en $1$}."])),
 (3, r"\pau{Aragón, ordinaria 2022} Siendo $a$, $b$ parámetros reales, se considera" + dm(pw((r'x^2+2\sqrt3', r'x\leq0'), (r'\sqrt{ax+b}', r'0<x\leq3'), (r'\dfrac72-\dfrac x6', 'x>3'))) + tasks(1, [r"Determina el valor de los parámetros para que $f$ sea continua.", r"Para estos valores, analiza si $f$ es derivable en $x=0$ y en $x=3$."]),
     tasks(1, [r"$2\sqrt3=\sqrt b$ y $\sqrt{3a+b}=3$: \ $\res{a=-1,\ b=12}$", r"$f'(0^-)=0\neq-\frac{1}{4\sqrt3}=f'(0^+)$: \rest{no derivable en 0}; \ $f'(3^\pm)=-\frac16$: \rest{derivable en 3}"])),
 (2, r"\pau{Andalucía, ordinaria (suplente) 2025} El nivel de concentración de un alumno durante un examen de 5 horas viene dado por" + dm(pw((r'-t^2+2t+10', r'0\leq t\leq2{,}5'), (r't^2+at+b', r'2{,}5<t\leq5'), name='f(t)')) + r"donde $t$ es el tiempo en horas. ¿Con qué nivel empieza el examen? Determina $a$ y $b$ para que $f$ sea continua y derivable en $t=2{,}5$.",
     r"$\res{f(0)=10}$. \ $8{,}75=6{,}25+2{,}5a+b$ \ y \ $-3=5+a$: \ $\res{a=-8,\ b=22{,}5}$"),
 (3, r"\pau{Cataluña, ordinaria 2026 (ampliado)} Determina los valores de $m$ que hacen que $f$ sea continua en todo su dominio y, para estos valores, estudia su derivabilidad:" + dm(pw((r'5e^{2x}', r'x\leq0'), (r'(x+m)^2+1', r'0<x<2'), ('1', r'2\leq x'))),
     r"$x=0$: $m=\pm2$; \ $x=2$: $m=-2$: \ $\res{m=-2}$. \ $f'(0^-)=10\neq-4=f'(0^+)$; \ $f'(2^\pm)=0$: \ \rest{derivable en $\mathbb R-\{0\}$}."),
 (2, r"\pau{Extremadura, extraordinaria 2023 (ampliado)} Halla $a$ y $b$ para que $f$ sea continua en $x=1$ y su gráfica pase por $(-1,5)$. ¿Es derivable en $x=1$?" + dm(pw((r'2x^2+ax+b', r'x\leq1'), (r'\ln x', 'x>1'))),
     r"$2+a+b=0$, \ $2-a+b=5$: \ $\res{a=-\frac52,\ b=\frac12}$. \ $f'(1^-)=4+a=\frac32\neq1=f'(1^+)$: \ \rest{no derivable en $x=1$}."),
 (2, r"\pau{Aragón, extraordinaria 2021 (ampliado)} Calcula los valores de $a\neq0$ para que $f$ sea continua y estudia si, para alguno de estos valores, es derivable en $x=1$:" + dm(pw((r'5-ax^2', r'x\leq1'), (r'\dfrac{6}{ax}', 'x>1'))),
     r"$5-a=\frac6a\Rightarrow\res{a=2\ \text{o}\ a=3}$. \ $f'(1^-)=-2a$, $f'(1^+)=-\frac6a$: \ $-4\neq-3$, \ $-6\neq-2$: \ \rest{nunca es derivable en $x=1$}."),
 (2, r"Halla los parámetros para que cada función sea derivable en su dominio:" + tasks(2, ['$' + pw((r'ax^2+bx', r'x\leq1'), (r'\ln x', 'x>1')) + '$', '$' + pw((r'ax^2+b', 'x<1'), (r'\dfrac1x', r'x\geq1'), name='g(x)') + '$',
                                                                                     '$' + pw((r'e^{ax}+b', r'x\leq0'), (r'\sin2x+3', 'x>0'), name='h(x)') + '$', '$' + pw((r'a+bx', r'x\leq0'), (r'\arctan x', 'x>0'), name='k(x)') + '$']),
     tasks(2, [r"$a+b=0$, $2a+b=1$: $\res{a=1,\ b=-1}$", r"$a+b=1$, $2a=-1$: $\res{a=-\frac12,\ b=\frac32}$", r"$1+b=3$, $a=2$: $\res{a=2,\ b=2}$", r"$a=0$, $b=\frac{1}{1+0}$: $\res{a=0,\ b=1}$"])),
 (2, r"Halla los parámetros en cada caso:" + tasks(1, [r"\pau{Galicia, ordinaria 2025} ¿Qué condición tienen que cumplir $k$ y $m$ para que " + '$' + pw((r'kx^2+2x', r'x\leq1'), (r'x^2-m', 'x>1')) + '$' + r" sea continua en $x=1$? ¿Y para qué valores es derivable en $x=1$?",
                                                  r"\pau{Galicia, extraordinaria 2024} Si " + '$' + pw((r'x^2+bx-1', r'x\leq0'), (r'\dfrac{k-xe^x}{x}', 'x>0')) + '$' + r", ¿qué valor de $k$ la hace continua en $x=0$ para cualquier $b$? ¿Para qué $b$ y $k$ es derivable en $x=0$?",
                                                  r"\pau{Canarias, junio 2019} Halla $a$ y $b$ para que " + '$' + pw((r'a-x', r'x\leq1'), (r'\dfrac bx-\ln x', 'x>1')) + '$' + r" sea derivable en todo su dominio y escribe la función resultante."])
     + recorda(r"Si un trozo tiene la forma $\frac{\dots}{x}$ y tiene que ser continuo en 0, el numerador se tiene que anular en 0 (si no, el límite es infinito)."),
     tasks(1, [r"Continua si $k+2=1-m$, es decir, $\res{m=-k-1}$. Derivable si, además, $2k+2=2$: $\res{k=0,\ m=-1}$.",
               r"$f(0)=-1$; el límite por la derecha es finito solo si $k=0$, y entonces $\lim_{x\to0^+}(-e^x)=-1$: $\res{k=0}$. $f'(0^-)=b$, $f'(0^+)=-1$: $\res{b=-1,\ k=0}$.",
               r"$a-1=b$, $\ -1=-b-1$: $\res{a=1,\ b=0}$; \ $f(x)=1-x$ si $x\leq1$ y $-\ln x$ si $x>1$."])),
 (2, r"Halla los parámetros para que cada función sea continua y derivable en el punto de cambio:" + tasks(1, [r"\pau{Castilla-La Mancha, ordinaria 2021} " + '$' + pw((r'x^2-ax+1', 'x<0'), (r'be^x', r'x\geq0')) + '$',
                                                  r"\pau{Castilla-La Mancha, ordinaria 2026} " + '$' + pw((r'\dfrac{x^2-1}{x-1}', 'x<1'), (r'ax+b', r'x\geq1')) + '$',
                                                  r"\pau{Andalucía, junio 2018} $k\neq0$ para que sea derivable " + '$' + pw((r'3-kx^2', r'x\leq1'), (r'\dfrac{2}{kx}', 'x>1')) + '$']),
     tasks(1, [r"$b=1$, $\ -a=b$: $\res{a=-1,\ b=1}$", r"$\frac{x^2-1}{x-1}=x+1$: continuidad $a+b=2$, derivabilidad $a=1$: $\res{a=b=1}$",
               r"Continuidad: $3-k=\frac2k\Rightarrow k=1$ o $k=2$; derivabilidad: $-2k=-\frac2k\Rightarrow k=\pm1$: $\res{k=1}$"])),
 (3, r"\pau{Madrid, ordinaria 2026} Sea " + '$' + pw((r'3x^2-\sin(ax)+b', 'x<0'), (r'\dfrac{2e^x}{1+x^2}', r'x\geq0')) + '$.' + tasks(1, [r"Calcula $a$ y $b$ para que sea continua y derivable en $x=0$.", r"Halla la recta tangente a la gráfica en $x=2$."]),
     tasks(1, [r"Continuidad: $b=2$. $f'(0^-)=-a$, $f'(0^+)=\frac{2e^0(1+0)-2e^0\cdot0}{1}=2$: $\res{a=-2,\ b=2}$.", r"$f(2)=\frac{2e^2}{5}$, $f'(x)=\frac{2e^x(x-1)^2}{(1+x^2)^2}\Rightarrow f'(2)=\frac{2e^2}{25}$: $\res{y=\frac{2e^2}{25}x+\frac{6e^2}{25}}$."])),
)

# =====================================================================
print(NCHK[0], 'comprobaciones correctas')
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={derivada, recta tangent, recta normal, regla de la cadena, derivació logarítmica, derivació implícita, derivabilitat, funcions a trossos, paràmetres, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre = pre.replace(r'\usepackage{amsmath,amssymb}', r'\usepackage{amsmath,amssymb}' + '\n' + r'\allowdisplaybreaks')
pre += '\n\\setlength{\\emergencystretch}{3em}\n'
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Cálculo de derivadas. Derivabilidad de una función"
def build(sol):
    t = 'Soluciones de la ficha' if sol else "Ficha de ejercicios"
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    p = preambul(pre, pdftitle='%s de la unidad 6: %s' % (t, TIT), capcalera='%s · Unidad 6: %s' % (t, 'Cálculo de derivadas'),
                 pdfkeywords='derivada, recta tangente, recta normal, regla de la cadena, derivación logarítmica, derivación implícita, derivabilidad, funciones a trozos, parámetros, PAU', curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 6' if sol else "Ficha de ejercicios · Unidad 6") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.2cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, recuerda que una derivada se puede escribir de muchas maneras equivalentes: compruébala con la calculadora de derivadas de los apuntes interactivos de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno justificando cada paso. Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas (de Matemáticas II y de Matemáticas Aplicadas a las Ciencias Sociales II), traducidos al castellano; a los marcados como «ampliado» se les ha añadido el estudio de la derivabilidad. Puedes comprobar los resultados con las herramientas de los apuntes interactivos.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus derivadas con la calculadora de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't6-fitxa-solucions-es.tex' if sol else 't6-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
regs = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
print(n, 'ejercicios,', npau, 'de la PAU de', len(regs), 'comunidades:', ', '.join(regs))
