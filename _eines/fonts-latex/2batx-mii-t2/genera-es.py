# Versió en castellà de genera.py. Genera t2-fitxa-exercicis-es.tex i t2-fitxa-solucions-es.tex (2n Batxillerat Matemàtiques II, Unitat 2: Sistemes d'equacions lineals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les estrelles no es
# mostren. El nivell és més alt que el de la fitxa de CCSS (_eines/fonts-latex/2batx-ccss-t2): sistemes de 4 incògnites,
# discussions amb un i dos paràmetres, sistemes no quadrats, Cramer amb paràmetres i qüestions teòriques. Al final de cada
# secció hi ha exercicis de la PAU de Matemàtiques II de 16 comunitats autònomes (2024-2026), traduïts al valencià.
# Els sistemes es dibuixen a partir de les seues matrius (sy, amp), els passos de Gauss els calcula gauss() amb aritmètica
# exacta i, al final, CHK comprova totes les solucions, classificacions, rangs i determinants (els que depenen d'un
# paràmetre, en una graella de valors).
# Ús: python3 genera.py && pdflatex t2-fitxa-exercicis.tex (dues vegades) && pdflatex t2-fitxa-solucions.tex (dues vegades)
import os, re, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def m(s): return '$' + s + '$'
def dm(s): return r'\[' + s + r'\]'

# ---------- nombres, sistemes i matrius ----------
def fr(x): return x if isinstance(x, F) else F(x)
def q(x, t='frac'):
    if isinstance(x, (str, Sym)): return str(x)
    x = fr(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\%s{%d}{%d}' % (t, abs(x.numerator), x.denominator)
def dec(x):
    if isinstance(x, (str, Sym)): return str(x)
    x = fr(x); d = x.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    return ('%g' % float(x)).replace('.', '{,}') if d == 1 else q(x, 'tfrac')
def lhs(cs, v):
    s = ''
    for c, x in zip(cs, v):
        if isinstance(c, Sym):
            t = c.w() + x
            s += t if not s or t.startswith('-') else '+' + t
            continue
        c = fr(c)
        if c == 0: continue
        a = abs(c); k = '' if a == 1 else dec(a)
        s += ('-' if c < 0 else '') + k + x if not s else ('-' if c < 0 else '+') + k + x
    return s or '0'
def sy(rows, v='xyz'):
    return r'\left\{\begin{aligned}' + r'\\'.join(lhs(r[:-1], v) + '&=' + dec(r[-1]) for r in rows) + r'\end{aligned}\right.'
def pm(M, d='pmatrix'): return r'\begin{%s}' % d + r'\\'.join(' & '.join(q(c, 'tfrac') for c in r) for r in M) + r'\end{%s}' % d
def vm(M): return pm(M, 'vmatrix')
def amp(R):
    n = len(R[0]) - 1
    return r'\left(\begin{array}{%s|r}' % ('r' * n) + r'\\'.join(' & '.join(q(c, 'tfrac') for c in r) for r in R) + r'\end{array}\right)'
def coef(R): return [r[:-1] for r in R]

# ---------- paràmetres simbòlics (només per a escriure els enunciats: Sym(Sym('k'))+4 -> k+4, 3*Sym(Sym('k')) -> 3k) ----------
class Sym:
    def __init__(self, e, atom=True): self.e, self.atom = e, atom
    def __str__(self): return self.e
    def w(self): return self.e if self.atom else '(' + self.e + ')'
    def __add__(self, o):
        if not isinstance(o, Sym) and o == 0: return self
        t = q(o); return Sym(self.e + ('' if t.startswith('-') else '+') + t, False)
    def __radd__(self, o):
        if o == 0: return self
        return Sym(q(o) + ('' if self.e.startswith('-') else '+') + self.e, False)
    def __sub__(self, o): return Sym(self.e + '-' + (o.w() if isinstance(o, Sym) else q(o)), False)
    def __rsub__(self, o): return Sym(q(o) + '-' + self.w(), False)
    def __neg__(self): return Sym('-' + self.w())
    def __mul__(self, o):
        if isinstance(o, Sym): return Sym(self.e + '^2') if o.e == self.e else Sym(self.w() + o.w())
        if o == 1: return self
        if o == -1: return -self
        return Sym(q(o) + self.w())
    __rmul__ = __mul__

# ---------- àlgebra exacta ----------
def det(M):
    M = [[fr(c) for c in r] for r in M]
    if len(M) == 1: return M[0][0]
    return sum((-1) ** j * M[0][j] * det([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(len(M)))
def rank(M):
    M = [[fr(c) for c in r] for r in M]; r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                k = M[i][c] / M[r][c]; M[i] = [a - k * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def classif(R):
    a, b, n = rank(coef(R)), rank(R), len(R[0]) - 1
    return 'SI' if a != b else 'SCD' if a == n else 'SCI'
def adjm(M):
    n = len(M)
    return [[(-1) ** (i + j) * det([r[:j] + r[j + 1:] for k, r in enumerate(M) if k != i]) for j in range(n)] for i in range(n)]
def tr(M): return [list(r) for r in zip(*M)]
def inv(M): d = det(M); return [[c / d for c in r] for r in tr(adjm(M))]
def subcol(R, j): return [r[:j] + [r[-1]] + r[j + 1:-1] for r in R]
def cramer(R): return det(coef(R)), [det(subcol(R, j)) for j in range(len(R[0]) - 1)]
def mult(A, X): return [sum(fr(a) * fr(x) for a, x in zip(r, X)) for r in A]
def satisfies(R, s): return all(sum(fr(c) * fr(x) for c, x in zip(r[:-1], s)) == fr(r[-1]) for r in R)

# ---------- passos del mètode de Gauss (amb aritmètica exacta) ----------
def fila(i, p): return 'F_%d%s' % (i + 1, "'" * p)
def gauss(R, start=r'A^*='):
    M = [[fr(c) for c in r] for r in R]; P = [0] * len(M)
    out = [start + amp(M)]; r = 0
    for c in range(len(M[0]) - 1):
        if r >= len(M): break
        cand = [i for i in range(r, len(M)) if M[i][c] != 0]
        if not cand: continue
        best = next((i for i in cand if abs(M[i][c]) == 1), cand[0])
        if best != r:
            M[r], M[best] = M[best], M[r]; P[r], P[best] = P[best], P[r]
            out.append(r'\xrightarrow{F_%d\leftrightarrow F_%d}' % (r + 1, best + 1) + amp(M))
        ops = []
        for i in range(r + 1, len(M)):
            e = M[i][c]
            if e == 0: continue
            p = M[r][c]; g = math.gcd(int(p), int(e)); a, b = p / g, e / g
            if a < 0: a, b = -a, -b
            M[i] = [a * x - b * y for x, y in zip(M[i], M[r])]
            old = fila(i, P[i]); P[i] += 1
            ka = '' if a == 1 else q(a)
            kb = '' if abs(b) == 1 else q(abs(b))
            ops.append('%s=%s%s%s%s' % (fila(i, P[i]), ka, old, '-' if b > 0 else '+', kb + fila(r, P[r])))
        if ops:
            arr = r'\xrightarrow{%s}' % ops[0] if len(ops) == 1 else r'\xrightarrow[%s]{%s}' % (r'\substack{' + r'\\'.join(ops[1:]) + '}' if len(ops) > 2 else ops[1], ops[0])
            out.append(arr + amp(M))
        r += 1
    lines = [out[0] + (out[1] if len(out) > 1 else '')] + out[2:]
    return ''.join(dm(l) for l in lines), M

CHK = []
def ck(kind, *a): CHK.append((kind,) + a)
def G(R, sol=None, cls=None, start=r'A^*='):
    t, M = gauss(R, start)
    GA.append((R, M))
    if cls: ck('cls', R, cls)
    if sol is not None: ck('sol', R, sol)
    return t
GA = []


S = []  # [(títol, [(estrelles, enunciat, solució)])]
def par(fun, crit, test, name=''):
    """fun(a) -> matriu ampliada; crit: {valor: classificació}; per a la resta de valors de test, SCD."""
    for v, c in crit.items(): ck('cls', fun(F(v)), c)
    for v in test:
        if F(v) not in [F(c) for c in crit]: ck('cls', fun(F(v)), 'SCD')
    return name
def detpoly(fun, p, vals=range(-6, 7)):
    for v in vals: ck('det', coef(fun(F(v))), p(F(v)))
HV = [F(v, 2) for v in range(-12, 13)]
def solve(R): return mult(inv(coef(R)), [r[-1] for r in R])
def pr(R, v='xyz'): return dm(sy(R, v))

# =====================================================================
R1 = [[1, 1, 1, 1, 2], [2, -1, 1, -1, 5], [1, 2, -1, 3, -3], [3, 1, -2, 1, -2]]
ck('cls', R1, 'SCD'); ck('sol', R1, (1, -1, 2, 0)); ck('det', coef(R1), -13)
R2a = [[1, 1, -1, 1, 1], [2, 1, 1, -1, 3], [3, 2, 0, 0, 4]]
ck('cls', R2a, 'SCI'); ck('rank', coef(R2a), 2); ck('sol', R2a, lambda l, u: (2 - 2 * l + 2 * u, -1 + 3 * l - 3 * u, l, u))
R2b = [[1, 1, 1, 6], [1, -1, 2, 5], [2, 1, -1, 1], [3, 2, 0, 7]]
R2c = [[1, 1, 1, 6], [1, -1, 2, 5], [2, 1, -1, 1], [3, 2, 0, 8]]
ck('cls', R2b, 'SCD'); ck('sol', R2b, (1, 2, 3)); ck('cls', R2c, 'SI')
R3 = lambda k, m: [[1, 2, -1, 1], [2, 1, 1, 4], [4, 5, k, m]]
for k in HV:
    for m_ in (F(6), F(0), F(5, 2)):
        ck('cls', R3(k, m_), 'SCD' if k != -1 else 'SCI' if m_ == 6 else 'SI')
ck('sol', R3(F(-1), F(6)), lambda l: (F(7, 3) - l, -F(2, 3) + l, l))
R4 = [[1, 1, 0, 3], [0, 1, 1, 2], [1, 2, 1, 5]]
ck('sol', R4, lambda l: (1 + l, 2 - l, l)); ck('cls', R4, 'SCI')
S.append(("Sistemas de ecuaciones lineales. Método de Gauss", [
 (1, r"Resuelve por el método de Gauss el sistema de cuatro ecuaciones y cuatro incógnitas:" + pr(R1, 'xyzt')
     + recorda(r"Haz ceros debajo de la diagonal con operaciones entre filas de la matriz ampliada y después resuelve de abajo arriba. Elige como fila pivote la que tenga un 1 en la columna que quieres anular."),
     G(R1, (1, -1, 2, 0), 'SCD') + r"Resolviendo de abajo arriba: \ $\res{x=1;\ y=-1;\ z=2;\ t=0}$"),
 (2, r"Discute y resuelve, cuando sea posible, por el método de Gauss:" + tasks(1, [m(sy(R2a, 'xyzt')), m(sy(R2b)), m(sy(R2c))]),
     tasks(1, [G(R2a, cls='SCI') + r"Rango 2 con 4 incógnitas: \rest{SCI con dos parámetros}. Con $z=\lambda$, $t=\mu$: \ $y=-1+3\lambda-3\mu$, \ $x=1-y+z-t$:\par $\res{x=2-2\lambda+2\mu;\ y=-1+3\lambda-3\mu;\ z=\lambda;\ t=\mu}$",
               G(R2b, cls='SCD') + r"La 4.ª fila se anula: quedan tres ecuaciones independientes. \rest{SCD}: \ $\res{x=1;\ y=2;\ z=3}$",
               r"Los mismos pasos dan la última fila $(0\ 0\ 0\,|\,1)$: \ \rest{SI}. (Las tres primeras ecuaciones obligan a $x=1$, $y=2$, $z=3$, y entonces $3x+2y=7\neq8$.)"])),
 (3, r"Discute por el método de Gauss el sistema siguiente según los valores de $k$ y $m$, y resuélvelo cuando sea compatible indeterminado:" + dm(sy(R3(Sym('k'), Sym('m')))),
     dm(r"\left(\begin{array}{rrr|r}1 & 2 & -1 & 1\\ 2 & 1 & 1 & 4\\ 4 & 5 & k & m\end{array}\right)\xrightarrow[F_3'=F_3-4F_1]{F_2'=F_2-2F_1}\left(\begin{array}{rrr|r}1 & 2 & -1 & 1\\ 0 & -3 & 3 & 2\\ 0 & -3 & k+4 & m-4\end{array}\right)\xrightarrow{F_3''=F_3'-F_2'}\left(\begin{array}{rrr|r}1 & 2 & -1 & 1\\ 0 & -3 & 3 & 2\\ 0 & 0 & k+1 & m-6\end{array}\right)")
     + tasks(1, [r"Si $k\neq-1$: \ \rest{SCD} (para cualquier $m$).", r"Si $k=-1$ y $m=6$: la 3.ª fila es nula: \ \rest{SCI}.", r"Si $k=-1$ y $m\neq6$: la 3.ª fila dice $0=m-6\neq0$: \ \rest{SI}."])
     + r"Para $k=-1$, $m=6$, con $z=\lambda$: \ $-3y+3\lambda=2\Rightarrow y=\lambda-\tfrac23$; \ $x=1-2y+z$:\par $\res{x=\tfrac73-\lambda;\ y=-\tfrac23+\lambda;\ z=\lambda}$"),
 (2, r"Escribe un sistema de tres ecuaciones con tres incógnitas, sin ningún coeficiente nulo en la tercera ecuación, que tenga como solución general \ $x=1+\lambda$, \ $y=2-\lambda$, \ $z=\lambda$.",
     r"Hay infinitas respuestas. Buscamos relaciones que cumplan todas las soluciones: $x+y=3$ e $y+z=2$. La tercera ecuación debe ser combinación lineal de las dos (si no, el sistema sería SCD); por ejemplo, la suma: $x+2y+z=5$:" + dm(r"\boxed{" + sy(R4) + "}")),
]))

# =====================================================================
A6 = [[1, 2, 1], [0, 1, 2], [1, 0, 2]]
ck('det', A6, 5); B6a, B6b = [2, 2, 3], [1, 1, 4]
ck('sol', [r + [b] for r, b in zip(A6, B6a)], (1, 0, 1)); ck('sol', [r + [b] for r, b in zip(A6, B6b)], (2, -1, 1))
A7 = [[3, 1, 0], [1, 3, 1], [0, 1, 3]]; N7 = [[2, 1, 0], [1, 2, 1], [0, 1, 2]]; B7 = [1, 0, 1]
ck('det', N7, 4); ck('sol', [r + [b] for r, b in zip(N7, B7)], (1, -1, 1))
R8 = lambda k: [[1, 1, 0, 1], [1, k, 1, 0], [0, 1, 1, 1]]
par(R8, {2: 'SI'}, HV); detpoly(R8, lambda k: k - 2, HV)
for k in HV:
    if k != 2: ck('sol', R8(k), (-k / (2 - k), 2 / (2 - k), -k / (2 - k)))
S.append(("Expresión matricial. Método matricial", [
 (2, r"Sea \ $A=" + pm(A6) + r"$. Resuelve por el método matricial los sistemas $AX=B_1$ y $AX=B_2$, con \ $B_1=" + pm([[b] for b in B6a]) + r"$ \ y \ $B_2=" + pm([[b] for b in B6b]) + r"$, calculando una sola vez la matriz inversa."
     + recorda(r"Si $|A|\neq0$: \ $A\cdot X=B\Rightarrow X=A^{-1}\cdot B$. Cuando varios sistemas tienen la misma matriz de coeficientes, basta con calcular $A^{-1}$ una vez."),
     r"$|A|=5$, \ $\mathrm{Adj}(A)=" + pm(adjm(A6)) + r"$, \ $A^{-1}=\frac15" + pm(tr(adjm(A6))) + r"$."
     + dm(r"X_1=\frac15" + pm(tr(adjm(A6))) + pm([[b] for b in B6a]) + r"=\boxed{\begin{pmatrix}1\\ 0\\ 1\end{pmatrix}},\qquad X_2=\frac15" + pm(tr(adjm(A6))) + pm([[b] for b in B6b]) + r"=\boxed{\begin{pmatrix}2\\ -1\\ 1\end{pmatrix}}")),
 (2, r"Halla la matriz columna $X=\begin{pmatrix}x\\ y\\ z\end{pmatrix}$ tal que $AX=X+B$, siendo \ $A=" + pm(A7) + r"$ \ y \ $B=" + pm([[b] for b in B7]) + r"$.",
     r"$AX-X=B\Rightarrow(A-I)X=B$, \ con $A-I=" + pm(N7) + r"$, \ $|A-I|=4$, \ $(A-I)^{-1}=\frac14" + pm(tr(adjm(N7))) + r"$:"
     + dm(r"X=\frac14" + pm(tr(adjm(N7))) + pm([[b] for b in B7]) + r"=\boxed{\begin{pmatrix}1\\ -1\\ 1\end{pmatrix}}")),
 (3, r"Considera el sistema \ $" + sy(R8(Sym('k'))) + r"$" + tasks(1, [r"¿Para qué valores de $k$ se puede resolver por el método matricial?", r"Resuélvelo por el método matricial en función de $k$.", r"¿Qué pasa cuando $k=2$?"]),
     tasks(1, [r"$|A|=" + vm(coef(R8(Sym('k')))) + r"=k-1-1=k-2$: \ si \ $\res{k\neq2}$",
               r"$\mathrm{Adj}(A)=\begin{pmatrix}k-1 & -1 & 1\\ -1 & 1 & -1\\ 1 & -1 & k-1\end{pmatrix}$ (es simétrica), \ $A^{-1}=\dfrac{1}{k-2}\begin{pmatrix}k-1 & -1 & 1\\ -1 & 1 & -1\\ 1 & -1 & k-1\end{pmatrix}$:"
               + dm(r"X=\frac{1}{k-2}\begin{pmatrix}k-1+0+1\\ -1+0-1\\ 1+0+k-1\end{pmatrix}=\frac{1}{k-2}\begin{pmatrix}k\\ -2\\ k\end{pmatrix}\ \Rightarrow\ \boxed{x=z=\tfrac{k}{k-2};\ \ y=\tfrac{2}{2-k}}"),
               r"$|A|=0$: la suma de la 1.ª y la 3.ª ecuaciones da $x+2y+z=2$, que contradice la 2.ª ($x+2y+z=0$): \ \rest{SI}."])),
 (3, r"Sea $AX=B$ un sistema de $n$ ecuaciones y $n$ incógnitas." + tasks(1, [r"Demuestra que, si $|A|\neq0$, el sistema tiene una única solución para cualquier $B$, y que el sistema homogéneo $AX=O$ solo tiene la solución trivial.",
     r"Demuestra que, si $X_1$ y $X_2$ son soluciones de $AX=B$, entonces $X_1-X_2$ es solución de $AX=O$, y que $X_1+t\,(X_2-X_1)$ es solución de $AX=B$ para todo $t\in\mathbb{R}$.", r"Deduce que un sistema lineal no puede tener exactamente dos soluciones."]),
     tasks(1, [r"Si $AX=B$, multiplicando por $A^{-1}$ por la izquierda, $X=A^{-1}B$: la solución existe y es única. Con $B=O$, $X=A^{-1}O=O$.",
               r"$A(X_1-X_2)=AX_1-AX_2=B-B=O$; \ \ $A\big(X_1+t(X_2-X_1)\big)=B+t\,(B-B)=B$.",
               r"Si tiene dos distintas, $X_1+t(X_2-X_1)$ da una solución distinta para cada $t$: tiene \rest{infinitas}."])),
]))

# =====================================================================
R10 = lambda a: [[a, 1, 1, 1], [1, a, 1, 1], [1, 1, a, 1]]
detpoly(R10, lambda a: (a - 1) ** 2 * (a + 2))
for a in HV:
    if a not in (1, -2): ck('sol', R10(a), (1 / (a + 2),) * 3)
R12 = [[1, 1, 1, 2], [1, -1, 2, 1], [2, 0, 3, 3]]
ck('cls', R12, 'SCI'); ck('sol', R12, lambda l: ((3 - 3 * l) / 2, (1 + l) / 2, l))
S.append(("Regla de Cramer", [
 (2, r"Resuelve por la regla de Cramer, en función de $a$, el sistema \ $" + sy(R10(Sym('a'))) + r"$ \ en los casos en que sea un sistema de Cramer."
     + recorda(r"Un sistema es de Cramer si tiene tantas ecuaciones como incógnitas y $|A|\neq0$. Entonces $x=\dfrac{|A_x|}{|A|}$, \ldots, donde $A_x$ se obtiene sustituyendo la columna de $x$ por la de términos independientes."),
     r"$|A|=a^3-3a+2=(a-1)^2(a+2)$: es de Cramer si $a\neq1$ y $a\neq-2$. \ Sumando todas las columnas a la primera y sacando factor común:"
     + dm(r"|A_x|=\begin{vmatrix}1 & 1 & 1\\ 1 & a & 1\\ 1 & 1 & a\end{vmatrix}=(a-1)^2,\qquad x=\frac{(a-1)^2}{(a-1)^2(a+2)}=\frac{1}{a+2}")
     + r"y, de la misma manera (o por la simetría del sistema), $|A_y|=|A_z|=(a-1)^2$: \ $\res{x=y=z=\tfrac{1}{a+2}}$"),
 (3, r"Calcula, aplicando la regla de Cramer, solo el valor de $t$ en el sistema del ejercicio \ref{ex:g4}.",
     r"$|A|=" + q(det(coef(R1))) + r"$ \ y \ $|A_t|=" + vm([r[:3] + [r[4]] for r in R1]) + '=' + q(det([r[:3] + [r[4]] for r in R1])) + r"$: \ $t=\dfrac{0}{" + q(det(coef(R1))) + r"}=\res{0}$, \ como habíamos obtenido por Gauss."),
 (2, r"El sistema \ $" + sy(R12) + r"$ \ es compatible indeterminado. Resuélvelo aplicando la regla de Cramer (pasa $z$ al segundo miembro).",
     r"La 3.ª ecuación es la suma de las dos primeras, y $\begin{vmatrix}1 & 1\\ 1 & -1\end{vmatrix}=-2\neq0$: \ $\left\{\begin{aligned}x+y&=2-z\\ x-y&=1-2z\end{aligned}\right.$"
     + dm(r"x=\frac{\begin{vmatrix}2-z & 1\\ 1-2z & -1\end{vmatrix}}{-2}=\frac{3-3z}{2},\qquad y=\frac{\begin{vmatrix}1 & 2-z\\ 1 & 1-2z\end{vmatrix}}{-2}=\frac{1+z}{2}")
     + dm(r"\boxed{x=\tfrac{3-3\lambda}{2};\ \ y=\tfrac{1+\lambda}{2};\ \ z=\lambda,\quad\lambda\in\mathbb{R}}")),
]))
S[0][1][0] = (S[0][1][0][0], r"\label{ex:g4}" + S[0][1][0][1], S[0][1][0][2])

# =====================================================================
H14 = lambda a: [[1, 1, a, 0], [1, a, 1, 0], [a, 1, 1, 0]]
detpoly(H14, lambda a: -(a - 1) ** 2 * (a + 2)); par(H14, {1: 'SCI', -2: 'SCI'}, HV)
ck('sol', H14(F(1)), lambda l, u: (-l - u, l, u)); ck('sol', H14(F(-2)), lambda l: (l, l, l))
H15 = [[1, 1, 1, 1, 0], [1, -1, 2, -1, 0], [2, 0, 3, 0, 0]]
ck('rank', coef(H15), 2); ck('sol', H15, lambda l, u: (-3 * l / 2, l / 2 - u, l, u))
H16 = [[2, -1, 0, 0], [1, 0, 1, 0]]
ck('sol', H16, lambda l: (l, 2 * l, -l)); ck('sol', [[1, 1, 3, 0]], (1, 2, -1))
S.append(("Sistemas homogéneos", [
 (2, r"Discute el sistema homogéneo \ $" + sy(H14(Sym('a'))) + r"$ \ según los valores de $a$ y resuélvelo cuando tenga soluciones distintas de la trivial."
     + recorda(r"Un sistema homogéneo siempre es compatible. Si $\operatorname{rg}(A)=r<n$, es SCI y la solución depende de $n-r$ parámetros."),
     r"$|A|=-a^3+3a-2=-(a-1)^2(a+2)$." + tasks(1, [r"Si $a\neq1$ y $a\neq-2$: \ \rest{SCD}, solo la solución trivial \ $x=y=z=0$.",
     r"Si $a=1$: las tres ecuaciones son $x+y+z=0$, rango 1: \ \rest{SCI con dos parámetros}:\par $\res{x=-\lambda-\mu;\ y=\lambda;\ z=\mu}$",
     r"Si $a=-2$: rango 2 ($\begin{vmatrix}1 & 1\\ 1 & -2\end{vmatrix}\neq0$). De las dos primeras, $x+y=2z$ y $x-2y=-z$: $y=z$, $x=z$: \ $\res{x=y=z=\lambda}$"])),
 (2, r"Resuelve el sistema homogéneo \ $" + sy(H15, 'xyzt') + r"$ \ y di cuántos parámetros tiene la solución.",
     r"La 3.ª ecuación es la suma de las dos primeras y las dos primeras no son proporcionales: $\operatorname{rg}(A)=2$, con 4 incógnitas: \rest{dos parámetros}. De la 3.ª, $x=-\tfrac32z$; con $z=\lambda$, $t=\mu$, de la 1.ª, $y=-x-z-t$:"
     + dm(r"\boxed{x=-\tfrac32\lambda;\ \ y=\tfrac12\lambda-\mu;\ \ z=\lambda;\ \ t=\mu}")),
 (2, r"Escribe un sistema homogéneo de dos ecuaciones con tres incógnitas cuyas soluciones sean $(\lambda,\ 2\lambda,\ -\lambda)$, $\lambda\in\mathbb{R}$. ¿Para qué valor de $k$ la ecuación $kx+y+3z=0$ también la cumplen todas estas soluciones?",
     r"Por ejemplo, $y=2x$ y $z=-x$: \ $\res{" + sy(H16) + r"}$ \ (el rango es 2, de modo que la solución depende de un parámetro). \ $k\lambda+2\lambda-3\lambda=0\Rightarrow\res{k=1}$"),
 (3, r"Razona las afirmaciones siguientes:" + tasks(1, [r"Un sistema homogéneo con más incógnitas que ecuaciones siempre tiene soluciones distintas de la trivial.", r"Si un sistema homogéneo cuadrado tiene alguna solución no trivial, entonces $|A|=0$.",
     r"Si $X_1$ y $X_2$ son soluciones de un sistema homogéneo, $aX_1+bX_2$ también lo es, para cualesquiera $a,b\in\mathbb{R}$."]),
     tasks(1, [r"\rest{Verdadera}: $\operatorname{rg}(A)\leq$ número de ecuaciones $<n$, y un sistema homogéneo siempre es compatible: es SCI.", r"\rest{Verdadera}: si $|A|\neq0$, sería SCD y solo tendría la solución trivial.",
               r"\rest{Verdadera}: $A(aX_1+bX_2)=aAX_1+bAX_2=aO+bO=O$."])),
]))

# =====================================================================
R18a = [[1, 1, 1, 3], [2, -1, 1, 2], [1, 2, -1, 2], [3, 1, 2, 6]]
R18b = [[1, 1, 1, 3], [2, -1, 1, 2], [1, 2, -1, 2], [3, 1, 2, 7]]
ck('det', R18a, 0); ck('det', R18b, 7); ck('cls', R18a, 'SCD'); ck('sol', R18a, (1, 1, 1)); ck('cls', R18b, 'SI'); ck('det', [r[:3] for r in R18a[:3]], 7)
R19 = [[1, 2, -1, 1, 3], [2, 4, 1, -1, 3], [1, 2, 2, -2, 0]]
ck('rank', coef(R19), 2); ck('cls', R19, 'SCI'); ck('sol', R19, lambda l, u: (2 - 2 * l, l, -1 + u, u))
R21 = lambda a, b, c: [[1, 1, 1, a], [1, -1, 2, b], [3, 1, 4, c]]
for a in range(-2, 3):
    for b in range(-2, 3):
        for c in range(-3, 4): ck('cls', R21(a, b, c), 'SCI' if c == 2 * a + b else 'SI')
S.append(("Teorema de Rouché-Frobenius", [
 (2, r"\label{ex:r4}Clasifica, sin resolverlos, los sistemas de cuatro ecuaciones y tres incógnitas siguientes, y resuelve el que sea compatible:" + tasks(2, [m(sy(R18a)), m(sy(R18b))])
     + recorda(r"Con 4 ecuaciones y 3 incógnitas, $\operatorname{rg}(A)\leq3$. Si $|A^*|\neq0$, entonces $\operatorname{rg}(A^*)=4\neq\operatorname{rg}(A)$ y el sistema es incompatible."),
     r"El menor de las tres primeras filas de $A$ vale $" + q(det([r[:3] for r in R18a[:3]])) + r"\neq0$, y $\operatorname{rg}(A)=3$."
     + tasks(1, [r"$|A^*|=0$: \ $\operatorname{rg}(A^*)=3=n$: \ \rest{SCD}. Resolviendo las tres primeras ecuaciones: \ $\res{x=y=z=1}$ \ (que también cumple la 4.ª).",
                 r"$|A^*|=" + q(det(R18b)) + r"\neq0$: \ $\operatorname{rg}(A^*)=4\neq3$: \ \rest{SI}."])),
 (2, r"Estudia el sistema \ $" + sy(R19, 'xyzt') + r"$ \ con el teorema de Rouché-Frobenius y resuélvelo.",
     r"Las dos primeras columnas son proporcionales, y también la 3.ª y la 4.ª (con signo cambiado): $\operatorname{rg}(A)\leq2$, y $\begin{vmatrix}1 & -1\\ 2 & 1\end{vmatrix}=3\neq0$ da $\operatorname{rg}(A)=2$. La 3.ª ecuación es $E_2-E_1$, de modo que $\operatorname{rg}(A^*)=2<4$: \rest{SCI con dos parámetros}."
     r"\par Sumando las dos primeras: $3x+6y=6$; con $y=\lambda$, $t=\mu$: \ $\res{x=2-2\lambda;\ y=\lambda;\ z=-1+\mu;\ t=\mu}$"),
 (2, r"Halla la relación que deben cumplir $a$, $b$ y $c$ para que el sistema \ $" + sy(R21(Sym('a'), Sym('b'), Sym('c'))) + r"$ \ sea compatible. ¿Puede ser compatible determinado?",
     r"$|A|=" + vm(coef(R21(0, 0, 0))) + r"=0$ y $\begin{vmatrix}1 & 1\\ 1 & -1\end{vmatrix}\neq0$: $\operatorname{rg}(A)=2$ siempre, de modo que \rest{nunca es SCD}. Como $F_3=2F_1+F_2$ en la matriz $A$, el sistema es compatible si y solo si los términos independientes cumplen la misma relación:"
     + dm(r"\boxed{c=2a+b}") + r"(y entonces es SCI; si no, $\operatorname{rg}(A^*)=3$ y es SI)."),
 (2, r"Di si son verdaderas o falsas las afirmaciones siguientes y justifícalo:" + tasks(1, [r"Un sistema de 4 ecuaciones y 3 incógnitas con $\operatorname{rg}(A)=3$ siempre es compatible determinado.",
     r"Un sistema de 3 ecuaciones y 4 incógnitas no puede ser compatible determinado.", r"Si en un sistema de 4 ecuaciones y 3 incógnitas $|A^*|\neq0$, el sistema es incompatible.",
     r"Si un sistema de 3 ecuaciones y 3 incógnitas tiene $|A|=0$, es incompatible."]),
     tasks(1, [r"\rest{Falsa}: puede ser $\operatorname{rg}(A^*)=4$ (es el caso del segundo sistema del ejercicio \ref{ex:r4}).", r"\rest{Verdadera}: $\operatorname{rg}(A)\leq3<4=n$.",
               r"\rest{Verdadera}: $\operatorname{rg}(A^*)=4$ y $\operatorname{rg}(A)\leq3$.", r"\rest{Falsa}: puede ser SCI (si $\operatorname{rg}(A)=\operatorname{rg}(A^*)<3$)."])),
]))

# =====================================================================
R22 = lambda a: [[a, 1, 1, 1], [1, a, 1, a], [1, 1, a, a * a]]
detpoly(R22, lambda a: (a - 1) ** 2 * (a + 2)); par(R22, {1: 'SCI', -2: 'SI'}, HV)
for a in HV:
    if a not in (1, -2): ck('sol', R22(a), (-(a + 1) / (a + 2), 1 / (a + 2), (a + 1) ** 2 / (a + 2)))
ck('sol', R22(F(1)), lambda l, u: (1 - l - u, l, u))
R23 = lambda a, b: [[1, 1, 1, 1], [1, 2, a, 2], [2, 3, 4, b]]
for a in HV:
    for b in (F(3), F(0), F(5, 2)): ck('cls', R23(a, b), 'SCD' if a != 3 else 'SCI' if b == 3 else 'SI')
    ck('det', coef(R23(a, 0)), 3 - a)
ck('sol', R23(F(3), F(3)), lambda l: (l, 1 - 2 * l, l))
R24 = lambda a: [[1, 2, 3], [2, -1, 1], [a, 1, 2]]
for a in HV: ck('det', R24(a), 5 * a - 5); ck('cls', R24(a), 'SCD' if a == 1 else 'SI')
ck('sol', R24(F(1)), (1, 1))
R25 = lambda k, a: [[1, 1, 1, 1, 1], [1, -1, 1, -1, a], [2, 0, k, 0, 3]]
for k in HV:
    for a in (F(2), F(0), F(-1, 2)):
        R = R25(k, a); ck('cls', R, 'SI' if (k == 2 and a != 2) else 'SCI')
        ck('rank', coef(R), 3 if k != 2 else 2)
R26 = lambda m: [[1, 1, 1, m + 1], [m, 1, m - 1, m], [1, m, 1, 1]]
detpoly(R26, lambda m: m - 1, HV); par(R26, {1: 'SI'}, HV)
ck('sol', R26(F(0)), (1, 0, 0)); S26 = solve(R26(F(2))); ck('sol', R26(F(2)), tuple(S26))
V27 = lambda a, b: [[1, 1, 1, 1], [1, 2, a, b], [1, 4, a * a, b * b]]
for a in HV:
    for b in HV[::2]:
        R = V27(a, b); ck('det', coef(R), (a - 1) * (a - 2))
        if a not in (1, 2): ck('cls', R, 'SCD'); ck('sol', R, ((2 - b) * (a - b) / (a - 1), (b - 1) * (a - b) / (a - 2), (b - 1) * (b - 2) / ((a - 1) * (a - 2))))
        else: ck('cls', R, 'SCI' if b in (1, 2) else 'SI')
    ck('det', [[1, 1, 1], [1, 2, a], [1, 4, a * a]], (a - 1) * (a - 2))
ck('sol', V27(F(1), F(1)), lambda l: (1 - l, 0, l)); ck('sol', V27(F(1), F(2)), lambda l: (-l, 1, l))
ck('sol', V27(F(2), F(1)), lambda l: (1, -l, l)); ck('sol', V27(F(2), F(2)), lambda l: (0, 1 - l, l))
B28 = lambda m: [[1, 2, -1, 1, 2], [2, 1, 1, -1, 1], [3, 3, m * m - 4, 0, m + 1]]
for m_ in HV:
    R = B28(m_)
    if m_ == 2: ck('cls', R, 'SCI'); ck('rank', coef(R), 2); ck('sol', R, lambda l, u: (u - l, 1 + l - u, l, u))
    elif m_ == -2: ck('cls', R, 'SI'); ck('rank', coef(R), 2)
    else: ck('cls', R, 'SCI'); ck('rank', coef(R), 3); ck('sol', R, (lambda c: lambda l: (l - c, 1 + c - l, c, l))(1 / (m_ + 2)))
ck('sol', B28(F(0)), lambda l: (-F(1, 2) + l, F(3, 2) - l, F(1, 2), l))
S.append(("Discusión de sistemas con parámetros", [
 (2, r"Discute el sistema siguiente según los valores de $a$ y resuélvelo en todos los casos en que sea compatible:" + dm(sy(R22(Sym('a'))))
     + recorda(r"Calcula $|A|$ y halla sus raíces (valores críticos). Para el resto de valores el sistema es SCD; cada valor crítico se estudia por separado con Rouché-Frobenius."),
     r"$|A|=(a-1)^2(a+2)$." + tasks(1, [r"Si $a\neq1$ y $a\neq-2$: \rest{SCD}. Por Cramer (o restando las ecuaciones dos a dos):\par $\res{x=-\tfrac{a+1}{a+2};\ \ y=\tfrac{1}{a+2};\ \ z=\tfrac{(a+1)^2}{a+2}}$",
     r"Si $a=1$: las tres ecuaciones son $x+y+z=1$: \ \rest{SCI con dos parámetros}:\par $\res{x=1-\lambda-\mu;\ y=\lambda;\ z=\mu}$",
     r"Si $a=-2$: sumando las tres ecuaciones, $0=1-2+4=3$: \ \rest{SI} (\,$\operatorname{rg}(A)=2$, $\operatorname{rg}(A^*)=3$)."])),
 (2, r"Discute el sistema siguiente según los valores de $a$ y $b$, y resuélvelo cuando sea compatible indeterminado:" + dm(sy(R23(Sym('a'), Sym('b')))),
     r"$|A|=" + vm(coef(R23(Sym('a'), 0))) + r"=3-a$." + tasks(1, [r"Si $a\neq3$: \ \rest{SCD}.", r"Si $a=3$ y $b=3$: la 3.ª ecuación es la suma de las dos primeras: \rest{SCI}.", r"Si $a=3$ y $b\neq3$: los coeficientes de la 3.ª son la suma de los de las otras, pero el término independiente no: \rest{SI}."])
     + r"Para $a=b=3$, restando las dos primeras: $y+2z=1$; con $z=\lambda$: \ $\res{x=\lambda;\ y=1-2\lambda;\ z=\lambda}$"),
 (2, r"Discute, según los valores de $a$, el sistema de tres ecuaciones y dos incógnitas \ $" + sy(R24(Sym('a')), 'xy') + r"$, \ y resuélvelo cuando sea compatible.",
     r"$\operatorname{rg}(A)=2$ siempre ($\begin{vmatrix}1 & 2\\ 2 & -1\end{vmatrix}=-5\neq0$). \ $|A^*|=" + vm(R24(Sym('a'))) + r"=5a-5$." + tasks(1, [r"Si $a\neq1$: $\operatorname{rg}(A^*)=3$: \ \rest{SI}.", r"Si $a=1$: $\operatorname{rg}(A^*)=2=n$: \ \rest{SCD}: \ $\res{x=1;\ y=1}$"])),
 (3, r"Discute, según los valores de $k$ y de $a$, el sistema \ $" + sy(R25(Sym('k'), Sym('a')), 'xyzt') + r"$",
     r"Sumando las dos primeras ecuaciones: $2x+2z=1+a$. Las dos primeras filas de $A$ no son proporcionales, así que $\operatorname{rg}(A)\geq2$."
     + tasks(1, [r"Si $k\neq2$: el menor de las columnas 1.ª, 2.ª y 3.ª, $" + vm([[1, 1, 1], [1, -1, 1], [2, 0, Sym('k')]]) + r"=-k+2\neq0$: \ $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3<4$: \ \rest{SCI con un parámetro}.",
                 r"Si $k=2$ y $a=2$: la 3.ª ecuación, $2x+2z=3$, coincide con la suma de las dos primeras: rango 2: \ \rest{SCI con dos parámetros}.",
                 r"Si $k=2$ y $a\neq2$: $2x+2z=3$ y $2x+2z=1+a$ se contradicen: \ \rest{SI}."])),
 (2, r"Discute el sistema \ $" + sy(R26(Sym('m'))) + r"$ \ según los valores de $m$ y resuélvelo para $m=0$ y para $m=2$.",
     r"$|A|=" + vm(coef(R26(Sym('m')))) + r"=m-1$." + tasks(1, [r"Si $m\neq1$: \ \rest{SCD}.", r"Si $m=1$: la 1.ª ecuación es $x+y+z=2$ y la 3.ª, $x+y+z=1$: \ \rest{SI}.",
     r"$m=0$: \ $x+y+z=1$, \ $y-z=0$, \ $x+z=1$ \ $\Rightarrow$ \ $\res{x=1;\ y=0;\ z=0}$",
     r"$m=2$: \ $x+y+z=3$, \ $2x+y+z=2$, \ $x+2y+z=1$ \ $\Rightarrow$ \ $\res{x=%s;\ y=%s;\ z=%s}$" % tuple(q(v, 'tfrac') for v in S26)])),
 (3, r"Discute el sistema siguiente según los valores de los parámetros $a$ y $b$, y resuélvelo en todos los casos en que sea compatible:" + dm(sy(V27(Sym('a'), Sym('b'))))
     + recorda(r"Cuando hay dos parámetros, primero se hallan los valores críticos del que aparece en la matriz $A$ (con $|A|=0$) y, para cada uno, se estudia qué valores del otro hacen $\operatorname{rg}(A^*)=\operatorname{rg}(A)$. Fíjate en la forma de los determinantes (ejercicio de Vandermonde de la unidad 1)."),
     r"$|A|=" + vm(coef(V27(Sym('a'), 0))) + r"$ es un determinante de Vandermonde (traspuesto) con los valores $1$, $2$ y $a$: \ $|A|=(2-1)(a-1)(a-2)=(a-1)(a-2)$."
     + tasks(1, [r"Si $a\neq1$ y $a\neq2$: \ \rest{SCD} para cualquier $b$. Por Cramer, los tres numeradores también son determinantes de Vandermonde:"
                 + dm(r"x=\frac{" + vm([[1, 1, 1], [Sym('b'), 2, Sym('a')], [Sym('b^2'), 4, Sym('a^2')]]) + r"}{(a-1)(a-2)}=\frac{(2-b)(a-b)(a-2)}{(a-1)(a-2)},\qquad y=\frac{" + vm([[1, 1, 1], [1, Sym('b'), Sym('a')], [1, Sym('b^2'), Sym('a^2')]]) + r"}{(a-1)(a-2)}=\frac{(b-1)(a-1)(a-b)}{(a-1)(a-2)}")
                 + dm(r"z=\frac{" + vm([[1, 1, 1], [1, 2, Sym('b')], [1, 4, Sym('b^2')]]) + r"}{(a-1)(a-2)}\ \Rightarrow\ \boxed{x=\frac{(2-b)(a-b)}{a-1};\ \ y=\frac{(b-1)(a-b)}{a-2};\ \ z=\frac{(b-1)(b-2)}{(a-1)(a-2)}}"),
                 r"Si $a=1$ o $a=2$: dos columnas de $A$ son iguales y $\operatorname{rg}(A)=2$ (\,$\begin{vmatrix}1 & 1\\ 1 & 2\end{vmatrix}\neq0$). El menor de $A^*$ formado por las columnas de $x$, de $y$ y de los términos independientes es \ $" + vm([[1, 1, 1], [1, 2, Sym('b')], [1, 4, Sym('b^2')]]) + r"=(b-1)(b-2)$:"
                 r"\par si $b\neq1$ y $b\neq2$, \ $\operatorname{rg}(A^*)=3$: \ \rest{SI}; \ si $b=1$ o $b=2$, \ $\operatorname{rg}(A^*)=2$: \ \rest{SCI}.",
                 r"Soluciones de los cuatro casos SCI (con $\lambda\in\mathbb{R}$):\par $a=1,\ b=1$: \ $\res{x=1-\lambda;\ y=0;\ z=\lambda}$ \qquad $a=1,\ b=2$: \ $\res{x=-\lambda;\ y=1;\ z=\lambda}$"
                 r"\par $a=2,\ b=1$: \ $\res{x=1;\ y=-\lambda;\ z=\lambda}$ \qquad $a=2,\ b=2$: \ $\res{x=0;\ y=1-\lambda;\ z=\lambda}$"])),
 (3, r"Discute el sistema de tres ecuaciones y cuatro incógnitas siguiente según los valores de $m$, y resuélvelo en todos los casos en que sea compatible:" + dm(sy(B28(Sym('m')), 'xyzt'))
     + recorda(r"Con 3 ecuaciones y 4 incógnitas, el sistema nunca puede ser SCD: si es compatible, la solución depende de $4-\operatorname{rg}(A)$ parámetros."),
     dm(r"A^*\xrightarrow[F_3'=F_3-3F_1]{F_2'=F_2-2F_1}\left(\begin{array}{rrrr|r}1 & 2 & -1 & 1 & 2\\ 0 & -3 & 3 & -3 & -3\\ 0 & -3 & m^2-1 & -3 & m-5\end{array}\right)\xrightarrow{F_3''=F_3'-F_2'}\left(\begin{array}{rrrr|r}1 & 2 & -1 & 1 & 2\\ 0 & -3 & 3 & -3 & -3\\ 0 & 0 & m^2-4 & 0 & m-2\end{array}\right)")
     + tasks(1, [r"Si $m\neq\pm2$: \ $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3<4$: \ \rest{SCI con un parámetro}. De la 3.ª fila, $z=\frac{m-2}{m^2-4}=\frac{1}{m+2}$; de la 2.ª, $y=1+z-t$; de la 1.ª, $x=2-2y+z-t=t-z$. Con $t=\lambda$:"
                 + dm(r"\boxed{x=\lambda-\tfrac{1}{m+2};\ \ y=1+\tfrac{1}{m+2}-\lambda;\ \ z=\tfrac{1}{m+2};\ \ t=\lambda}"),
                 r"Si $m=2$: la 3.ª fila es nula: \ $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2<4$: \ \rest{SCI con dos parámetros}. Con $z=\lambda$, $t=\mu$: \ $\res{x=\mu-\lambda;\ y=1+\lambda-\mu;\ z=\lambda;\ t=\mu}$",
                 r"Si $m=-2$: la 3.ª fila dice $0=-4$: \ $\operatorname{rg}(A)=2\neq\operatorname{rg}(A^*)=3$: \ \rest{SI}."])),
]))

# =====================================================================
N28 = [[1, 1, 1, 12], [-99, 0, 99, 396], [1, -1, 1, 0]]
ck('sol', N28, (1, 6, 5)); ck('cls', N28, 'SCD')
P29 = [[-1, 1, -1, 1, -4], [0, 0, 0, 1, 1], [1, 1, 1, 1, 2], [8, 4, 2, 1, 11]]
ck('sol', P29, (2, -2, 1, 1)); ck('cls', P29, 'SCD')
M30 = [[1, 1, 1, 10], [1, 2, 5, 25]]
ck('sol', M30, lambda l: (-5 + 3 * l, 15 - 4 * l, l))
nat30 = [(x, y, z) for x in range(0, 11) for y in range(0, 11) for z in range(0, 11) if x + y + z == 10 and x + 2 * y + 5 * z == 25]
ck('cls', M30, 'SCI'); assert nat30 == [(1, 7, 2), (4, 3, 3)], nat30
T31 = lambda k: [[1, 1, 1, 100], [10, 5, k, 600], [0, 1, -1, 0]]
par(T31, {15: 'SI'}, range(0, 20)); ck('sol', T31(F(5)), (20, 40, 40)); ck('sol', T31(F(10)), (-60, 80, 80))
for k in range(0, 15): ck('sol', T31(F(k)), (100 - F(800, 15 - k), F(400, 15 - k), F(400, 15 - k)))
S.append(("Problemas de planteamiento", [
 (2, r"Un número de tres cifras cumple que la suma de sus cifras es 12, que la cifra de las decenas es igual a la suma de las otras dos y que, si se invierte el orden de las cifras, el número aumenta en 396. ¿Cuál es el número?"
     + recorda(r"Si las cifras son $x$ (centenas), $y$ (decenas) y $z$ (unidades), el número vale $100x+10y+z$."),
     r"$(100z+10y+x)-(100x+10y+z)=396\Leftrightarrow-99x+99z=396$:" + pr(N28) + r"De la 1.ª y la 3.ª: $2y=12$, $y=6$; entonces $x+z=6$ y $z-x=4$: \ el número es \rest{165}."),
 (2, r"Halla el polinomio de tercer grado $p(x)=ax^3+bx^2+cx+d$ cuya gráfica pasa por los puntos $(-1,-4)$, $(0,1)$, $(1,2)$ y $(2,11)$.",
     r"Sustituyendo cada punto: \ " + pr(P29, 'abcd') + r" \ $d=1$; sumando la 1.ª y la 3.ª: $2b+2d=-2$, $b=-2$; entonces $a+c=3$ y $8a+2c=18$: $a=2$, $c=1$." + dm(r"\boxed{p(x)=2x^3-2x^2+x+1}")),
 (2, r"Tenemos 10 monedas de 1 €, de 2 € y de 5 € que suman 25 €." + tasks(1, [r"Plantea el sistema y comprueba que es compatible indeterminado. Escribe su solución general.", r"¿Cuáles son las soluciones posibles en el contexto del problema?",
     r"¿Cuántas monedas hay de cada tipo si hay más monedas de 1 € que de 2 €?"]),
     tasks(1, [r"$x$, $y$, $z$: monedas de 1, 2 y 5 €. \ " + pr(M30) + r" \ Rango 2 y 3 incógnitas: \rest{SCI}. Restando: $y+4z=15$; con $z=\lambda$: \ $\res{x=-5+3\lambda;\ y=15-4\lambda;\ z=\lambda}$",
               r"Deben ser naturales: $x\geq0\Rightarrow\lambda\geq\tfrac53$ e $y\geq0\Rightarrow\lambda\leq\tfrac{15}{4}$, de modo que $\lambda=2$ o $\lambda=3$: \ \rest{1, 7 y 2} \ o \ \rest{4, 3 y 3} monedas.",
               r"\rest{4 monedas de 1 €, 3 de 2 € y 3 de 5 €}."])),
 (3, r"Un teatro vende 100 entradas de tres tipos: generales a 10 €, infantiles a 5 € y sénior a $k$ euros. Ha recaudado 600 € y ha vendido tantas entradas infantiles como sénior." + tasks(1, [r"Plantea el sistema y discútelo según los valores de $k$.",
     r"Si la entrada sénior cuesta 5 €, ¿cuántas entradas de cada tipo se han vendido?", r"¿Puede ser que la entrada sénior cueste 10 €? Razónalo."]),
     tasks(1, [r"$x$ generales, $y$ infantiles, $z$ sénior: \ " + pr(T31(Sym('k'))) + r" \ $|A|=" + vm(coef(T31(Sym('k')))) + r"=k-15$. Si $k\neq15$: \rest{SCD}; si $k=15$: con $y=z$, $x+2y=100$ y $10x+20y=600$ se contradicen: \rest{SI}.",
               r"\rest{20 generales, 40 infantiles y 40 sénior}.", r"Con $k=10$ el sistema es SCD, pero la solución es $x=-60$, $y=z=80$: \rest{no tiene sentido} (no puede haber un número negativo de entradas)."])),
]))

# =====================================================================
# Exercicis de la PAU d'altres comunitats autònomes (presos del recull «Ejercicios de sistemas de ecuaciones en pruebas de
# acceso a la universidad de todas las comunidades autónomas de España», curs 2026/27, de J. A. Martínez García,
# ebaumatematicas.com). Es posen al final de cada secció; els apartats d'interpretació geomètrica (plans de l'espai,
# que encara no s'han estudiat) s'han suprimit. Notes: al recull, les solucions d'Extremadura 2026 (ord./extraord.)
# estan intercanviades, i la x de Navarra extraord. 2025 té una errata; ací se'n donen les correctes (comprovades).
SEC = {t: exs for t, exs in S}
def pau(sec, *exs): SEC[sec].extend(exs)
def mn(R, cols): return [[r[j] for j in cols] for r in R]  # menor amb les columnes indicades (la de termes indep. és -1)

# --- 1. Gauss
A25 = [[1, 1, 1, 22], [4, 3, 2, 61]]
ck('cls', A25, 'SCI'); ck('sol', A25, lambda l: (l, 17 - 2 * l, 5 + l))
nat = [(x, y, z) for x in range(1, 23) for y in range(1, 23) for z in range(1, 23) if x + y + z == 22 and 4 * x + 3 * y + 2 * z == 61]
assert nat == [(l, 17 - 2 * l, 5 + l) for l in range(1, 9)], nat
pau("Sistemas de ecuaciones lineales. Método de Gauss",
 (2, r"\pau{Andalucía, extraordinaria 2025} Se sabe que la suma de tres números naturales es 22 y que la suma de cuatro veces el primero más el triple del segundo más el doble del tercero es 61. ¿Puede ser 15 uno de los tres números? En caso afirmativo, calcula los otros. ¿Hay otras opciones?",
     r"" + pr(A25) + r" \ Restando a la 2.ª el doble de la 1.ª: $2x+y=17$. Con $x=\lambda$: \ $y=17-2\lambda$, \ $z=5+\lambda$ (\rest{SCI})."
     r"\par Para que sean naturales, $\lambda\geq1$ y $17-2\lambda\geq1$: $\lambda=1,\dots,8$. El 15 solo puede ser $y$ (con $\lambda=1$): \ \rest{1, 15 y 6}. Las otras opciones son $(2,13,7)$, $(3,11,8)$, $(4,9,9)$, $(5,7,10)$, $(6,5,11)$, $(7,3,12)$ y $(8,1,13)$."))

# --- 2. Expressió matricial
RIO = lambda a: [[1, -1, a, a], [a, 1, -1, a], [a + 1, 0, 1, a + 2]]
detpoly(RIO, lambda a: -(a - 2) * (a + 1))
for a in HV: ck('sol', RIO(a), (1, 1, 1))
pau("Expresión matricial. Método matricial",
 (2, r"\pau{La Rioja, extraordinaria 2024} Dado el sistema de ecuaciones lineales dependiente del parámetro real $a$" + dm(sy(RIO(Sym('a')))) + r"halla la matriz $A^{-1}b$ sin calcular la matriz inversa de $A$, siendo $A$ la matriz de coeficientes y $b$ la de términos independientes.",
     r"$A^{-1}b$ es la solución $X$ del sistema $AX=b$ (cuando $A$ es invertible: $|A|=-a^2+a+2=-(a-2)(a+1)\neq0$, es decir, $a\neq2$ y $a\neq-1$). Observando el sistema, $x=y=z=1$ cumple las tres ecuaciones: $1-1+a=a$, $a+1-1=a$, $a+1+1=a+2$. Como la solución es única:"
     + dm(r"A^{-1}b=\boxed{\begin{pmatrix}1\\ 1\\ 1\end{pmatrix}}")))

# --- 3. Cramer
BAL = lambda k: [[k, 1, 0, 1], [0, k, 1, 0], [3, -1, -1, 0]]
detpoly(BAL, lambda k: -k * k + k + 3, HV)
for k in HV: ck('sol', BAL(k), ((1 - k) / (-k * k + k + 3), F(3) / (-k * k + k + 3), -3 * k / (-k * k + k + 3))); ck('det', mn(BAL(k), [0, 1, -1]), -3 * k)
CAT = lambda k: [[2, k, 1, 3], [-1, 2, 2, 1], [1, 1, 1, 2]]
detpoly(CAT, lambda k: 3 * k - 3, HV); par(CAT, {1: 'SCI'}, HV)
for k in HV: ck('sol', CAT(k), (1, 0, 1))
ck('sol', CAT(F(1)), lambda l: (1, 1 - l, l)); ck('det', mn(CAT(0), [0, -1, 2]), 0)
pau("Regla de Cramer",
 (3, r"\pau{Islas Baleares, extraordinaria 2025} Dado el sistema \ $" + sy(BAL(Sym('k'))) + r"$, \ donde $k$ es un número real cualquiera:" + tasks(1, [r"Discute, según el parámetro $k$, el número de soluciones que tiene el sistema.", r"Resuelve el sistema cuando sea posible."]),
     tasks(1, [r"$|A|=" + vm(coef(BAL(Sym('k')))) + r"=-k^2+k+3$, que se anula para $k=\frac{1\pm\sqrt{13}}{2}$. Si $k\neq\frac{1\pm\sqrt{13}}{2}$: \rest{SCD}. Si $k=\frac{1\pm\sqrt{13}}{2}$: $\begin{vmatrix}k & 1\\ 0 & k\end{vmatrix}=k^2\neq0$, así que $\operatorname{rg}(A)=2$, y el menor de $A^*$ \ $" + vm([[Sym('k'), 1, 1], [0, Sym('k'), 0], [3, -1, 0]]) + r"=-3k\neq0$ da $\operatorname{rg}(A^*)=3$: \rest{SI}.",
               r"Por Cramer, con $|A_x|=1-k$, $|A_y|=3$, $|A_z|=-3k$:" + dm(r"\boxed{x=\frac{1-k}{-k^2+k+3};\quad y=\frac{3}{-k^2+k+3};\quad z=\frac{-3k}{-k^2+k+3}}")])),
 (2, r"\pau{Cataluña, extraordinaria 2026} Considera el sistema de ecuaciones \ $" + sy(CAT(Sym('k'))) + r"$, \ donde $k$ es un parámetro real." + tasks(1, [r"Discute el sistema en función del parámetro $k$.", r"Resuelve el sistema para todos los valores de $k$ y comprueba que, para $k\neq1$, la solución no depende de $k$."]),
     tasks(1, [r"$|A|=3k-3$. Si $k\neq1$: \rest{SCD}. Si $k=1$: $\begin{vmatrix}-1 & 2\\ 1 & 1\end{vmatrix}\neq0$, $\operatorname{rg}(A)=2$, y $3E_1=5E_3-E_2$, también en los términos independientes: \rest{SCI}.",
               r"Si $k\neq1$, por Cramer: $|A_y|=" + vm(mn(CAT(0), [0, -1, 2])) + r"=0\Rightarrow y=0$, y entonces $-x+2z=1$, $x+z=2$: \ $\res{x=1;\ y=0;\ z=1}$, que no depende de $k$. Si $k=1$: restando la 1.ª y la 3.ª, $x=1$, e $y+z=1$: \ $\res{x=1;\ y=1-\lambda;\ z=\lambda}$"])))
# --- 4. Homogenis
RIH = lambda m: [[3, 1, -1, 0], [3, 2, -m, 0], [1, -1, -1, 0]]
detpoly(RIH, lambda m: 2 - 4 * m, HV); par(RIH, {F(1, 2): 'SCI'}, HV); ck('sol', RIH(F(1, 2)), lambda l: (l, -l, 2 * l))
pau("Sistemas homogéneos",
 (2, r"\pau{La Rioja, ordinaria 2025} Dado el sistema de ecuaciones homogéneo \ $" + sy(RIH(Sym('m'))) + r"$, \ indica para qué valores de $m$ el sistema tiene solo la solución trivial. Resuelve el sistema para un valor de $m$ que lo haga compatible indeterminado.",
     r"$|A|=2-4m$. Si $m\neq\tfrac12$: \rest{solo la solución trivial}. Para $\res{m=\tfrac12}$, $\operatorname{rg}(A)=2$ (\,$\begin{vmatrix}3 & 1\\ 1 & -1\end{vmatrix}\neq0$): de la 1.ª y la 3.ª, $4x=2z$ e $y=z-3x$:"
     + dm(r"\boxed{x=\lambda;\ \ y=-\lambda;\ \ z=2\lambda,\quad\lambda\in\mathbb{R}}")))

# --- 5. Rouché-Frobenius
BL6 = [[2, 1, 1, 6500], [4, 5, 7, 22500], [1, 2, 3, 8000]]
ck('cls', BL6, 'SCI'); ck('det', coef(BL6), 0); ck('rank', coef(BL6), 2)
pau("Teorema de Rouché-Frobenius",
 (2, r"\pau{Islas Baleares, extraordinaria 2026} Queremos determinar el coste por hora de tres servicios de una empresa de alquiler de material audiovisual: iluminación profesional ($x$ €/hora), equipo de sonido ($y$ €/hora) y cámaras de grabación ($z$ €/hora). Se han registrado los gastos totales de tres eventos:"
     + dm(r"\begin{aligned}&\text{Evento 1: } & 2x+y+z&=6500\\ &\text{Evento 2: } & 4x+5y+7z&=22500\\ &\text{Evento 3: } & x+2y+3z&=8000\end{aligned}")
     + r"Justifica si, con esta información, se pueden determinar de manera única los costes de los tres servicios.",
     r"$|A|=" + vm(coef(BL6)) + r"=0$ y $\begin{vmatrix}2 & 1\\ 4 & 5\end{vmatrix}=6\neq0$: $\operatorname{rg}(A)=2$. La 2.ª ecuación es la suma de la 1.ª y el doble de la 3.ª, también en los términos independientes ($6500+16000=22500$): $\operatorname{rg}(A^*)=2<3$."
     r" \ \rest{SCI}: \rest{no} se pueden determinar de manera única."))

# --- 6. Discussió
AND = lambda a: [[3, -1, 0, a * a], [0, 1 - a, 2, 0], [0, 4, 3 - a, a - 5]]
detpoly(AND, lambda a: 3 * (a - 5) * (a + 1)); par(AND, {5: 'SCI', -1: 'SI'}, HV); ck('sol', AND(F(0)), (-F(2, 3), -2, 1))
ARA = lambda m: [[1, 2, -1, -1], [8, m, -6, -8], [-1, -2, m * m, m]]
detpoly(ARA, lambda m: (m - 16) * (m * m - 1)); par(ARA, {1: 'SCI', -1: 'SI', 16: 'SI'}, list(HV) + [16]); ck('sol', ARA(F(1)), lambda l: (-1 + 11 * l, 2 * l, 15 * l))
m16 = mn(ARA(F(16)), [0, 2, -1]); assert det(m16) != 0
CAN = lambda k: [[k, 1, -3, 5], [-1, 1, 1, -4], [k, 1, -k, 1]]
detpoly(CAN, lambda k: -(k - 3) * (k + 1)); par(CAN, {3: 'SI', -1: 'SI'}, HV); ck('sol', CAN(F(4)), (5, -3, 4))
CTO = lambda a: [[1, 1, 1, 0], [0, 1, a, 1], [0, a, 1, 2 - a]]
detpoly(CTO, lambda a: 1 - a * a); par(CTO, {1: 'SCI', -1: 'SI'}, HV); ck('sol', CTO(F(2)), (-F(1, 3), -F(1, 3), F(2, 3))); ck('sol', CTO(F(1)), lambda l: (-1, 1 - l, l))
CTE = lambda a: [[a ** 3, 1, a, 1], [a, a * a, 0, a]]
for a in HV: ck('cls', CTE(a), 'SCI'); ck('rank', coef(CTE(a)), 1 if a == 0 else 2)
ck('sol', CTE(F(0)), lambda l, u: (l, 1, u)); ck('sol', CTE(F(2)), lambda l: (1 - 2 * l, l, (-7 + 15 * l) / 2))
CLM = lambda a: [[1, 1, -1, 2], [4, 2, 0, a], [a, 1, 1, 1]]
detpoly(CLM, lambda a: 2 * a - 6); par(CLM, {3: 'SCI'}, HV); ck('sol', CLM(F(0)), (-1, 2, -1)); ck('sol', CLM(F(3)), lambda l: (l, (3 - 4 * l) / 2, (-1 - 2 * l) / 2))
CYA = [[2, 2, 0], [0, 2, 0], [2, 0, 4]]
CYE = lambda al: [[2 - al, 2, 0, 0], [0, 2 - al, 0, 0], [2, 0, 4 - al, 1]]
detpoly(CYE, lambda al: (2 - al) ** 2 * (4 - al)); par(CYE, {2: 'SCI', 4: 'SI'}, HV); ck('sol', CYE(F(2)), lambda l: (l, 0, F(1, 2) - l)); ck('det', mn(CYE(F(4)), [0, 1, -1]), 4)
CYO = lambda m: [[m - 10, -2, -1, -1], [7, m + 2, 2, m + 1], [5, 2, 1, 1]]
detpoly(CYO, lambda m: (m - 2) * (m - 5)); par(CYO, {2: 'SI', 5: 'SCI'}, HV); ck('sol', CYO(F(3)), (0, 2, -3))
m2c = mn(CYO(F(2)), [0, 1, -1]); assert det(m2c) != 0
CTO26 = lambda m: [[1, m, 1, 4], [1, 3, 1, 5], [m, 1, 1, 4]]
detpoly(CTO26, lambda m: (m - 1) * (m - 3)); par(CTO26, {1: 'SCI', 3: 'SI'}, HV); ck('sol', CTO26(F(1)), lambda l: (F(7, 2) - l, F(1, 2), l))
ck('cls', CTO26(F(1)) + [[0, 0, 1, F(1, 2)]], 'SCD'); ck('sol', CTO26(F(1)) + [[0, 0, 1, F(1, 2)]], (3, F(1, 2), F(1, 2)))
EXE = lambda k: [[k, 2, -1, 3 * k], [2, k, -2, 6], [1, -1, 1, k]]
detpoly(EXE, lambda k: (k - 3) * (k + 2)); par(EXE, {3: 'SCI', -2: 'SI'}, HV); ck('sol', EXE(F(3)), lambda l: (3 - l, 4 * l, 5 * l))
mEX = mn(EXE(F(-2)), [0, 2, -1]); assert det(mEX) != 0
EXO = lambda m: [[m, 7, 5, 0], [1, m, 1, 3], [0, 1, 1, -2]]
detpoly(EXO, lambda m: (m - 2) * (m + 1)); par(EXO, {2: 'SCI', -1: 'SI'}, HV); ck('sol', EXO(F(1)), (5, F(5, 2), -F(9, 2)))
GL6 = lambda m: [[2, 2 * m - 2, m + 6, 9], [1, m - 2, 3, 2], [0, 2, 2 * m + 2, m - 5]]
detpoly(GL6, lambda m: -2 * (m + 2)); par(GL6, {-2: 'SI'}, HV)
GL5 = lambda m: [[1, m, 1, m], [1, 0, 3 - m, 2 * m], [0, m, 2, 3 * m]]
detpoly(GL5, lambda m: m * (m - 4)); par(GL5, {0: 'SCI', 4: 'SI'}, HV)
MDE = lambda k: [[k, 1, 1, 0], [k + 1, 1, -k, k], [1, k + 1, 0, 2 * k]]
detpoly(MDE, lambda k: k * (k + 1) ** 2); par(MDE, {0: 'SCI', -1: 'SI'}, HV); ck('sol', MDE(F(0)), lambda l: (-l, l, -l))
NV6 = lambda a: [[a * a - 4, a + 2, 2, 4], [4 - a * a, 0, 1, 2], [a * a - 4, a + 2, a, -4]]
detpoly(NV6, lambda a: (a * a - 4) ** 2); par(NV6, {2: 'SI', -2: 'SCI'}, HV); ck('sol', NV6(F(-2)), lambda l, u: (l, u, 2))
NV5 = lambda m: [[m * m - m, m + 2, -1, 1 - m * m], [m * m - m, 2 * m + 1, 0, 2], [m - m * m, -(2 * m + 1), m + 2, 2 * m + 2]]
detpoly(NV5, lambda m: m * (m - 1) ** 2 * (m + 2)); par(NV5, {0: 'SI', 1: 'SCI', -2: 'SCI'}, HV)
for mm in HV:
    if mm not in (0, 1, -2): ck('sol', NV5(mm), ((1 - 3 * mm - 2 * mm * mm) / (mm * mm - mm), mm + 1, 2))
ck('sol', NV5(F(1)), lambda l: (l, F(2, 3), 2)); ck('sol', NV5(F(-2)), lambda l: (l, -F(2, 3) + 2 * l, 3 + 6 * l)); ck('det', mn(NV5(F(0)), [1, 2, -1]), -2)
PVE = lambda al: [[1, -al, 3, 3], [al, 1, 1, 2], [1, -1, 2, 1]]
detpoly(PVE, lambda al: 2 * al * (al - 2)); par(PVE, {0: 'SCI', 2: 'SI'}, HV); ck('sol', PVE(F(0)), lambda l: (3 - 3 * l, 2 - l, l))
pau("Discusión de sistemas con parámetros",
 (2, r"\pau{Andalucía, ordinaria 2026} Considera el sistema \ $\left\{\begin{aligned}3x-y&=a^2\\ (1-a)y+2z&=0\\ 4y+(3-a)z&=a-5\end{aligned}\right.$" + tasks(1, [r"Discútelo según los valores de $a$.", r"Para $a=0$, resuelve el sistema, si es posible."]),
     tasks(1, [r"$|A|=3\big[(1-a)(3-a)-8\big]=3(a^2-4a-5)=3(a-5)(a+1)$. \ Si $a\neq5$ y $a\neq-1$: \rest{SCD}. \ Si $a=-1$: las dos últimas ecuaciones son $2y+2z=0$ y $4y+4z=-6$: \rest{SI}. \ Si $a=5$: son $-4y+2z=0$ y $4y-2z=0$ (proporcionales): \rest{SCI}.",
               r"$3x-y=0$, \ $y+2z=0$, \ $4y+3z=-5$ \ $\Rightarrow$ \ $\res{x=-\tfrac23;\ y=-2;\ z=1}$"])),
 (2, r"\pau{Aragón, extraordinaria 2025} Dado el sistema de ecuaciones lineales \ $\left\{\begin{aligned}x+2y-z&=-1\\ 8x+my-6z&=-8\\ -x-2y+m^2z&=m\end{aligned}\right.$, \ con $m\in\mathbb{R}$:" + tasks(1, [r"Estudia, en función de $m$, el número de soluciones del sistema.", r"Resuelve, si es posible, el sistema para $m=1$."]),
     tasks(1, [r"$|A|=m^3-16m^2-m+16=(m-16)(m^2-1)$. \ Si $m\neq16$ y $m\neq\pm1$: \rest{una solución}. \ Si $m=1$: la 3.ª ecuación es la 1.ª cambiada de signo: \rest{infinitas soluciones}. \ Si $m=-1$: la 1.ª y la 3.ª dicen $x+2y-z=-1$ y $x+2y-z=1$: \rest{ninguna solución}. \ Si $m=16$: $\operatorname{rg}(A)=2$ y el menor $" + vm(m16) + '=' + q(det(m16)) + r"\neq0$ de $A^*$ da $\operatorname{rg}(A^*)=3$: \rest{ninguna solución}.",
               r"$x+2y-z=-1$, \ $8x+y-6z=-8$. Restando a la 2.ª el séxtuple de la 1.ª: $2x-11y=-2$. Con $y=2\lambda$: $x=-1+11\lambda$, $z=x+2y+1=15\lambda$: \ $\res{x=-1+11\lambda;\ y=2\lambda;\ z=15\lambda}$"])),
 (2, r"\pau{Canarias, ordinaria 2024} Dado el sistema de ecuaciones lineales con un parámetro $k\in\mathbb{R}$:" + dm(sy(CAN(Sym('k')))) + tasks(1, [r"Discute la resolución del sistema según los valores de $k$.", r"Resuelve el sistema cuando $k=4$."]),
     tasks(1, [r"$|A|=-k^2+2k+3=-(k-3)(k+1)$. \ Si $k\neq3$ y $k\neq-1$: \rest{SCD}. \ Si $k=3$: la 1.ª y la 3.ª ecuaciones tienen los mismos coeficientes ($3x+y-3z$) y términos independientes distintos: \rest{SI}. \ Si $k=-1$: lo mismo ocurre con la 2.ª y la 3.ª ($-x+y+z$): \rest{SI}.",
               r"Restando la 1.ª y la 3.ª: $z=4$; entonces $4x+y=17$ y $-x+y=-8$: \ $\res{x=5;\ y=-3;\ z=4}$"])),
 (2, r"\pau{Cantabria, ordinaria 2026} Considera el sistema \ $" + sy(CTO(Sym('a'))) + r"$, \ dependiente del parámetro $a\in\mathbb{R}$." + tasks(1, [r"Discute el sistema en función de los valores de $a$.", r"Para $a=2$, si el sistema es compatible, halla su solución general.", r"Para $a=1$, si el sistema es compatible, halla su solución general."]),
     tasks(1, [r"$|A|=1-a^2$. \ Si $a\neq\pm1$: \rest{SCD}. \ Si $a=-1$: las dos últimas son $y-z=1$ y $-y+z=3$: \rest{SI}. \ Si $a=1$: las dos últimas son $y+z=1$: \rest{SCI}.",
               r"$y+2z=1$, \ $2y+z=0$ \ $\Rightarrow$ \ $y=-\tfrac13$, $z=\tfrac23$: \ $\res{x=-\tfrac13;\ y=-\tfrac13;\ z=\tfrac23}$", r"$y+z=1$ y $x=-(y+z)=-1$: \ $\res{x=-1;\ y=1-\lambda;\ z=\lambda}$"])),
 (3, r"\pau{Cantabria, extraordinaria 2026} Considera el sistema \ $\left\{\begin{aligned}a^3x+y+az&=1\\ ax+a^2y&=a\end{aligned}\right.$, \ dependiente del parámetro $a\in\mathbb{R}$." + tasks(1, [r"Discute el sistema en función de los valores de $a$.", r"Para $a=0$, si el sistema es compatible, halla su solución general.", r"Para $a=2$, si el sistema es compatible, halla su solución general."]),
     tasks(1, [r"Si $a\neq0$: el menor $\begin{vmatrix}1 & a\\ a^2 & 0\end{vmatrix}=-a^3\neq0$, y $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2<3$: \rest{SCI}. Si $a=0$: queda $y=1$ y $0=0$: rango 1, \rest{SCI con dos parámetros}. Es decir, \rest{SCI para todo $a$}.",
               r"$\res{x=\lambda;\ y=1;\ z=\mu}$, \ $\lambda,\mu\in\mathbb{R}$.", r"$8x+y+2z=1$, \ $2x+4y=2$. Con $y=\lambda$: $x=1-2\lambda$, \ $z=\frac{1-8x-y}{2}$: \ $\res{x=1-2\lambda;\ y=\lambda;\ z=-\tfrac72+\tfrac{15}{2}\lambda}$"])),
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2025} Dado el sistema \ $" + sy(CLM(Sym('a'))) + r"$:" + tasks(1, [r"Discute la resolución del sistema según los valores de $a\in\mathbb{R}$ e indica el número de soluciones en cada caso.", r"Para $a=0$, resuelve el sistema de forma razonada."]),
     tasks(1, [r"$|A|=2a-6$. \ Si $a\neq3$: \rest{SCD} (una solución). \ Si $a=3$: la 2.ª ecuación, $4x+2y=3$, es la suma de la 1.ª y la 3.ª: \rest{SCI} (infinitas soluciones).", r"Sumando la 1.ª y la 3.ª: $x+2y=3$; con $4x+2y=0$: $x=-1$, $y=2$, $z=-1$: \ $\res{x=-1;\ y=2;\ z=-1}$"])),
 (3, r"\pau{Castilla y León, extraordinaria 2026} Sean \ $A=" + pm(CYA) + r"$ \ e $I$ la matriz identidad de orden 3. Discute el sistema \ $(A-\alpha I)\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}0\\ 0\\ 1\end{pmatrix}$ \ en función del parámetro $\alpha\in\mathbb{R}$.",
     r"$A-\alpha I=\begin{pmatrix}2-\alpha & 2 & 0\\ 0 & 2-\alpha & 0\\ 2 & 0 & 4-\alpha\end{pmatrix}$, \ $|A-\alpha I|=(2-\alpha)^2(4-\alpha)$."
     + tasks(1, [r"Si $\alpha\neq2$ y $\alpha\neq4$: \ \rest{SCD}.", r"Si $\alpha=2$: queda $2y=0$, $0=0$, $2x+2z=1$: rango 2: \ \rest{SCI} \ ($x=\lambda$, $y=0$, $z=\tfrac12-\lambda$).",
                 r"Si $\alpha=4$: la 3.ª columna de $A$ es nula y $\operatorname{rg}(A)=2$, pero $" + vm(mn(CYE(F(4)), [0, 1, -1])) + r"=4\neq0$: $\operatorname{rg}(A^*)=3$: \ \rest{SI}."])),
 (2, r"\pau{Castilla y León, ordinaria 2026} Considera el sistema \ $\left\{\begin{aligned}(m-10)x-2y-z&=-1\\ 7x+(m+2)y+2z&=m+1\\ 5x+2y+z&=1\end{aligned}\right.$, \ con $m\in\mathbb{R}$." + tasks(1, [r"Discute el sistema según los valores del parámetro $m$.", r"Resuelve, razonadamente, el sistema para $m=3$."]),
     tasks(1, [r"$|A|=m^2-7m+10=(m-2)(m-5)$. \ Si $m\neq2$ y $m\neq5$: \rest{SCD}. \ Si $m=5$: la 1.ª ecuación es la 3.ª cambiada de signo: \rest{SCI}. \ Si $m=2$: $\begin{vmatrix}-8 & -2\\ 7 & 4\end{vmatrix}\neq0$, $\operatorname{rg}(A)=2$, y $" + vm(m2c) + '=' + q(det(m2c)) + r"\neq0$: $\operatorname{rg}(A^*)=3$, \rest{SI}.",
               r"Sumando la 1.ª y la 3.ª: $-2x=0$, $x=0$; entonces $5y+2z=4$ y $2y+z=1$: \ $\res{x=0;\ y=2;\ z=-3}$"])),
 (2, r"\pau{Cataluña, ordinaria 2026} Considera el sistema \ $" + sy(CTO26(Sym('m'))) + r"$, \ que depende del parámetro real $m$." + tasks(1, [r"Discute el sistema para los distintos valores de $m$.", r"Resuélvelo, si es posible, para el caso $m=1$.",
     r"Para $m=1$, ¿es posible añadir una cuarta ecuación de manera que el sistema resultante sea compatible determinado y tenga como solución $(x,y,z)=\left(3,\tfrac12,\tfrac12\right)$? Razona la respuesta."]),
     tasks(1, [r"$|A|=m^2-4m+3=(m-1)(m-3)$. \ Si $m\neq1$ y $m\neq3$: \rest{SCD}. \ Si $m=1$: la 1.ª y la 3.ª ecuaciones coinciden: \rest{SCI}. \ Si $m=3$: la 1.ª y la 2.ª tienen los mismos coeficientes y términos independientes 4 y 5: \rest{SI}.",
               r"$x+y+z=4$, $x+3y+z=5$: $y=\tfrac12$: \ $\res{x=\tfrac72-\lambda;\ y=\tfrac12;\ z=\lambda}$", r"Sí: $\left(3,\tfrac12,\tfrac12\right)$ es la solución con $\lambda=\tfrac12$. Basta con añadir una ecuación que fije $\lambda$, por ejemplo \ $\res{z=\tfrac12}$: entonces $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3$ y es SCD."])),
 (2, r"\pau{Extremadura, extraordinaria 2026} Dado el sistema \ $" + sy(EXE(Sym('k'))) + r"$:" + tasks(1, [r"Discute el sistema según los valores del parámetro $k$.", r"Resuelve el sistema para el valor $k=3$."]),
     tasks(1, [r"$|A|=k^2-k-6=(k-3)(k+2)$. \ Si $k\neq3$ y $k\neq-2$: \rest{SCD}. \ Si $k=-2$: $\operatorname{rg}(A)=2$ y $" + vm(mEX) + '=' + q(det(mEX)) + r"\neq0$: \rest{SI}. \ Si $k=3$: la 1.ª ecuación es la suma de la 2.ª y la 3.ª: \rest{SCI}.",
               r"$2x+3y-2z=6$, \ $x-y+z=3$. Sumando a la 1.ª el doble de la 2.ª: $4x+y=12$. Con $x=3-\lambda$: $y=4\lambda$, \ $z=3-x+y=5\lambda$: \ $\res{x=3-\lambda;\ y=4\lambda;\ z=5\lambda}$"])),
 (2, r"\pau{Extremadura, extraordinaria 2025} Se considera el sistema \ $" + sy(EXO(Sym('m'))) + r"$, \ con $m\in\mathbb{R}$." + tasks(1, [r"Discute el sistema en función del parámetro $m$.", r"Resuélvelo para el caso $m=1$."]),
     tasks(1, [r"$|A|=m^2-m-2=(m-2)(m+1)$. \ Si $m\neq2$ y $m\neq-1$: \rest{SCD}. \ Si $m=2$: la 1.ª ecuación es el doble de la 2.ª más tres veces la 3.ª ($0=6-6$): \rest{SCI}. \ Si $m=-1$: $-E_2+6E_3$ tiene los mismos coeficientes que la 1.ª ecuación, $-x+7y+5z$, pero término independiente $-15\neq0$: \rest{SI}.",
               r"Restando la 3.ª a la 2.ª: $x=5$; entonces $7y+5z=-5$ e $y+z=-2$: \ $\res{x=5;\ y=\tfrac52;\ z=-\tfrac92}$"])),
 (2, r"\pau{Galicia, extraordinaria 2026} Discute, según los valores del parámetro $m$, el sistema\[\left\{\begin{aligned}2x+(2m-2)y+(m+6)z&=9\\ x+(m-2)y+3z&=2\\ 2y+(2m+2)z&=m-5\end{aligned}\right.\]",
     r"$|A|=-2m-4=-2(m+2)$. \ Si $m\neq-2$: \rest{SCD}. \ Si $m=-2$: restando a la 1.ª el doble de la 2.ª se obtiene $2y-2z=5$, mientras que la 3.ª es $2y-2z=-7$: \rest{SI}."),
 (2, r"\pau{Galicia, extraordinaria 2025} Discute, según los valores del parámetro $m$, el sistema\[\left\{\begin{aligned}x+my+z&=m\\ x+(3-m)z&=2m\\ my+2z&=3m\end{aligned}\right.\]",
     r"$|A|=m^2-4m=m(m-4)$. \ Si $m\neq0$ y $m\neq4$: \rest{SCD}. \ Si $m=0$: queda $x+z=0$, $x+3z=0$, $2z=0$: $x=z=0$ e $y$ cualquiera: \rest{SCI}. \ Si $m=4$: restando las dos primeras, $4y+2z=-4$, mientras que la 3.ª es $4y+2z=12$: \rest{SI}."),
 (2, r"\pau{Madrid, extraordinaria 2025} Sea el sistema de ecuaciones lineales dependiente del parámetro real $k$:" + dm(pm([[Sym('k'), 1, 1], ['k+1', 1, '-k'], [1, 'k+1', 0]]) + r"\begin{pmatrix}x\\ y\\ z\end{pmatrix}-\begin{pmatrix}0\\ k\\ 2k\end{pmatrix}=\begin{pmatrix}0\\ 0\\ 0\end{pmatrix}") + tasks(1, [r"Discute el sistema en función de los valores de $k$.", r"Resuelve el sistema para $k=0$."]),
     tasks(1, [r"El sistema es $AX=\begin{pmatrix}0\\ k\\ 2k\end{pmatrix}$, con $|A|=k^3+2k^2+k=k(k+1)^2$. \ Si $k\neq0$ y $k\neq-1$: \rest{SCD}. \ Si $k=0$: es homogéneo con $\operatorname{rg}(A)=2$: \rest{SCI}. \ Si $k=-1$: la 1.ª más la 3.ª da $y+z=-2$, mientras que la 2.ª es $y+z=-1$: \rest{SI}.",
               r"$y+z=0$, \ $x+y=0$: \ $\res{x=-\lambda;\ y=\lambda;\ z=-\lambda}$"])),
 (3, r"\pau{Navarra, extraordinaria 2026} Estudia el sistema siguiente, que depende del parámetro real $a$, y resuélvelo en los casos en que sea compatible indeterminado. Menciona el resultado teórico empleado y justifica su uso." + dm(r"\left\{\begin{aligned}(a^2-4)x+(a+2)y+2z&=4\\ (4-a^2)x+z&=2\\ (a^2-4)x+(a+2)y+az&=-4\end{aligned}\right."),
     r"Utilizamos el \textbf{teorema de Rouché-Frobenius}, que relaciona el tipo de sistema con los rangos de $A$ y de $A^*$. \ $|A|=(a^2-4)^2=(a-2)^2(a+2)^2$."
     + tasks(1, [r"Si $a\neq\pm2$: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3$: \ \rest{SCD}.", r"Si $a=2$: la 1.ª y la 3.ª ecuaciones son $4y+2z=4$ y $4y+2z=-4$: \rest{SI}.",
                 r"Si $a=-2$: las ecuaciones quedan $2z=4$, $z=2$, $-2z=-4$: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=1<3$: \rest{SCI}: \ $\res{x=\lambda;\ y=\mu;\ z=2}$"])),
 (3, r"\pau{Navarra, extraordinaria 2025} Estudia el sistema siguiente, que depende del parámetro real $m$, y resuélvelo en los casos en que sea compatible. Menciona el resultado teórico empleado y justifica su uso." + dm(r"\left\{\begin{aligned}(m^2-m)x+(m+2)y-z&=1-m^2\\ (m^2-m)x+(2m+1)y&=2\\ (m-m^2)x-(2m+1)y+(m+2)z&=2m+2\end{aligned}\right."),
     r"Teorema de Rouché-Frobenius. Sumando la 2.ª y la 3.ª: $(m+2)z=2m+4$. \ $|A|=m(m-1)^2(m+2)$."
     + tasks(1, [r"Si $m\neq0,1,-2$: \rest{SCD}: $z=2$; restando la 1.ª a la 2.ª, $(m-1)y+z=1+m^2$, de donde $y=m+1$, y de la 2.ª se despeja $x$: \ $\res{x=\tfrac{1-3m-2m^2}{m(m-1)};\ y=m+1;\ z=2}$",
                 r"Si $m=0$: la columna de $x$ es nula, $\operatorname{rg}(A)=2$, y $" + vm(mn(NV5(F(0)), [1, 2, -1])) + r"=-2\neq0$: \rest{SI}.",
                 r"Si $m=1$: $3y-z=0$, $3y=2$, $-3y+3z=4$: \rest{SCI}: \ $\res{x=\lambda;\ y=\tfrac23;\ z=2}$",
                 r"Si $m=-2$: la 3.ª ecuación es la 2.ª cambiada de signo: \rest{SCI}: de $6x-z=-3$ y $6x-3y=2$: \ $\res{x=\lambda;\ y=-\tfrac23+2\lambda;\ z=3+6\lambda}$"])),
 (2, r"\pau{País Vasco, extraordinaria 2025} Sea el sistema de ecuaciones lineales" + dm(r"\left\{\begin{aligned}x+3z&=3+\alpha y\\ z+\alpha x+y-2&=0\\ x+2z-y&=1\end{aligned}\right.") + tasks(1, [r"Discute la existencia de solución según los valores del parámetro $\alpha$.", r"Si es posible, resuélvelo en el caso $\alpha=0$."]),
     tasks(1, [r"Ordenando: $\left\{\begin{aligned}x-\alpha y+3z&=3\\ \alpha x+y+z&=2\\ x-y+2z&=1\end{aligned}\right.$. \ $|A|=2\alpha^2-4\alpha=2\alpha(\alpha-2)$. \ Si $\alpha\neq0$ y $\alpha\neq2$: \rest{SCD}. \ Si $\alpha=0$: la 1.ª ecuación es la suma de las otras dos: \rest{SCI}. \ Si $\alpha=2$: \rest{SI} ($\operatorname{rg}(A)=2$, $\operatorname{rg}(A^*)=3$).",
               r"$y+z=2$, \ $x-y+2z=1$: con $z=\lambda$: \ $\res{x=3-3\lambda;\ y=2-\lambda;\ z=\lambda}$"])))
ck('cls', PVE(F(2)), 'SI'); ck('rank', coef(PVE(F(2))), 2)

# --- 7. Problemes
AR24 = [[1, 1, 2, 7000], [1, 2, 3, 9000], [2, 3, 5, 16000]]
ck('cls', AR24, 'SCI'); ck('sol', AR24, lambda l: (5000 - l, 2000 - l, l))
AS6 = lambda m: [[1, 1, 1, 10], [1, 2, 3, m + 9], [2, 3, 7 - m, 22]]
detpoly(AS6, lambda m: 3 - m); par(AS6, {3: 'SCI'}, HV); ck('sol', AS6(F(3)), lambda l: (8 + l, 2 - 2 * l, l)); ck('sol', AS6(F(1)), (11, -2, 1))
AS7 = lambda p: [[1, 2, 2, 11], [1, 3, 3, 16], [3, 3, p, 21]]
detpoly(AS7, lambda p: p - 3); par(AS7, {3: 'SI'}, HV); ck('sol', AS7(F(2)), (1, 8, -3)); ck('sol', AS7(F(4)), (1, 2, 3))
CN5 = [[1, 1, 1, 1000], [F(2, 10), F(4, 10), F(6, 10), 360], [F(1, 10), F(2, 10), F(1, 10), 120], [F(1, 10), F(3, 10), F(3, 10), 200]]
ck('cls', CN5, 'SCD'); ck('det', coef(CN5)[:3], -F(4, 100)); ck('sol', CN5, (500, 200, 300)); ck('det', CN5, 0)
CL4 = lambda k: [[1, 1, 1, 157], [1, 2, 3, 278], [1, 0, -k, 0]]
detpoly(CL4, lambda k: 1 - k, HV); par(CL4, {1: 'SI'}, HV)
MD5 = [[F(8, 10), 1, F(12, 10), 80], [3, -5, 3, 0], [1, 1, -2, 5]]
ck('cls', MD5, 'SCD'); ck('sol', MD5, (25, 30, 25))
MR6 = lambda k: [[1, 2, 1, 400], [1, 1, 2, 500], [1, 1, 1, k]]
for k in range(250, 450, 7): ck('sol', MR6(F(k)), (3 * k - 900, 400 - k, 500 - k)); ck('cls', MR6(F(k)), 'SCD')
MR7 = lambda k: [[1, 1, 1, 12], [1, 2, -1, k], [2, -1, 1, 4]]
for k in HV: ck('det', coef(MR7(k)), -7); ck('sol', MR7(k), (2 * k / 7, 4 + k / 7, 8 - 3 * k / 7))
PV6 = [[10, 15, 12, 612], [1, 1, 1, 48], [5, 9, 4, 304]]
ck('cls', PV6, 'SCD'); ck('sol', PV6, (12, 20, 16))
pau("Problemas de planteamiento",
 (2, r"\pau{Aragón, extraordinaria 2024} En un laboratorio farmacéutico se fabrican tres medicamentos, M$_1$, M$_2$ y M$_3$, a partir de tres principios activos, A$_1$, A$_2$ y A$_3$. Un gramo de M$_1$ necesita 10 mg de A$_1$, 10 mg de A$_2$ y 20 mg de A$_3$; un gramo de M$_2$, 10, 20 y 30 mg, y un gramo de M$_3$, 20, 30 y 50 mg, respectivamente. Se dispone de 70 g de A$_1$, 90 g de A$_2$ y 160 g de A$_3$, y se quiere gastar todo. ¿Es posible? En caso afirmativo, ¿qué cantidades de cada medicamento se pueden fabricar?",
     r"$x$, $y$, $z$: gramos de M$_1$, M$_2$ y M$_3$. Pasando a mg y dividiendo entre 10:" + pr(AR24) + r"La 3.ª ecuación es la suma de las otras dos: \rest{SCI}. Restando las dos primeras, $y+z=2000$; con $z=\lambda$: \ $\res{x=5000-\lambda;\ y=2000-\lambda;\ z=\lambda}$, \ con \rest{$0\leq\lambda\leq2000$} para que las cantidades no sean negativas. Es posible, y de muchas maneras."),
 (2, r"\pau{Asturias, extraordinaria 2026} Una empresa de logística transporta mercancía con camiones pequeños, medianos y grandes, y utiliza 10 en total. Cada camión pequeño transporta 1 tonelada; cada mediano, 2 toneladas, y cada grande, 3 toneladas. La carga total es de $(m+9)$ toneladas, con $m\in\mathbb{R}$. El transporte tiene un coste de 2 unidades por camión pequeño, 3 por camión mediano y $7-m$ por camión grande, y el coste total es de 22 unidades."
     + tasks(1, [r"Plantea el sistema de ecuaciones lineales que modeliza la situación.", r"Determina un valor de $m$ para el que el sistema tiene infinitas soluciones y resuélvelo.", r"Resuelve el sistema para $m=1$. ¿Tiene sentido esta solución?"]),
     tasks(1, [pr(AS6(Sym('m'))), r"$|A|=3-m$: hace falta \ $\res{m=3}$. Entonces la 3.ª ecuación es la suma de las otras dos: \rest{SCI}:\par $\res{x=8+\lambda;\ y=2-2\lambda;\ z=\lambda}$",
               r"$\res{x=11;\ y=-2;\ z=1}$: \rest{no tiene sentido}: el número de camiones no puede ser negativo."])),
 (3, r"\pau{Asturias, ordinaria 2026} Un cliente de una cafetería compra 1 café, 2 tés y 2 zumos y paga 11 euros. Al día siguiente compra 1 café, 3 tés y 3 zumos y paga 16 euros. El tercer día compra 3 cafés, 3 tés y todos los zumos que pueda pagar con 21 euros exactos (no le tienen que devolver cambio)."
     + tasks(1, [r"Halla un sistema de ecuaciones lineales que modelice el problema de calcular el precio de cada producto en función del número $p$ de zumos que le dan el tercer día, y discútelo en función de $p$.",
                 r"El camarero del tercer día le dice: «Por ese dinero te daré dos zumos», y el cliente responde: «Es imposible, el precio está mal calculado». ¿Quién tiene razón? Justifica la respuesta.", r"El camarero le responde que en realidad tiene 4 zumos para darle y el cliente queda satisfecho. ¿A qué precio le ha cobrado cada bebida?"]),
     tasks(1, [r"$c$, $t$, $s$: precios del café, el té y el zumo: \ " + pr(AS7(Sym('p')), 'cts') + r" \ $|A|=p-3$. Si $p\neq3$: \rest{SCD}; si $p=3$: \rest{SI} (restando las dos primeras, $t+s=5$, y entonces la 3.ª daría $3c=6$ pero la 1.ª, $c=1$).",
               r"Con $p=2$: \ $c=1$, $t=8$, $s=-3$: un precio negativo: \rest{tiene razón el cliente}.", r"Con $p=4$: \ \rest{café 1 €, té 2 € y zumo 3 €}."])),
 (2, r"\pau{Canarias, extraordinaria 2025} Una empresa de piensos para peces utiliza tres materias primas: subproductos vegetales (20\,\% de proteína, 10\,\% de grasa y 10\,\% de carbohidratos), harinas (40\,\%, 20\,\% y 30\,\%) y subproductos cárnicos (60\,\%, 10\,\% y 30\,\%). Quiere preparar 1000 kg de pienso que contengan un 36\,\% de proteína, un 12\,\% de grasa y un 20\,\% de carbohidratos. ¿Qué cantidad de cada materia prima debe utilizar?",
     r"$x$, $y$, $z$: kg de cada materia prima. Hay cuatro ecuaciones (masa total, proteína, grasa y carbohidratos):" + pr(CN5) + r"$|A^*|=0$ y el menor de las tres primeras filas de $A$ es no nulo: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3$, \rest{SCD}. Resolviendo: \ \rest{500 kg de vegetales, 200 kg de harinas y 300 kg de cárnicos}."),
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2024} Una heladería vende helados de una, dos y tres bolas a 1, 2 y 3 euros, respectivamente. El viernes vendió 157 helados y obtuvo 278 euros. También sabemos que el número de helados de una bola vendidos es $k$ veces el número de helados de tres bolas, con $k>0$."
     + tasks(1, [r"Plantea un sistema de ecuaciones lineales que permita determinar el número de helados vendidos de cada tipo.", r"Estudia para qué valores de $k$ el sistema tiene solución única. ¿Es posible que, en alguno de estos casos, se haya vendido el mismo número de helados de una bola que de tres bolas?"]),
     tasks(1, [pr(CL4(Sym('k'))), r"$|A|=1-k$: solución única si \ $\res{k\neq1}$ \ ($k>0$). Vender el mismo número quiere decir $k=1$, y entonces el sistema es incompatible ($x=z$ da $2x+y=157$ y $4x+2y=278$, contradictorias): \rest{no es posible}."])),
 (2, r"\pau{Madrid, ordinaria 2025} En el baloncesto hay canastas de un punto, de dos y de tres. Calcula el número de lanzamientos de uno, de dos y de tres puntos que hizo un equipo en un partido, sabiendo que: el equipo anotó 80 puntos con un acierto del 80\,\% en los tiros de un punto, del 50\,\% en los de dos y del 40\,\% en los de tres; la tercera parte del número de lanzamientos de dos fue igual a la quinta parte del resto de lanzamientos, y el doble del número de lanzamientos de tres es cinco unidades menor que el resto de lanzamientos.",
     r"$x$, $y$, $z$: lanzamientos de 1, 2 y 3 puntos: \ $0{,}8x+0{,}5\cdot2y+0{,}4\cdot3z=80$, \ $\frac y3=\frac{x+z}{5}$, \ $2z=x+y-5$:" + pr(MD5) + r"$\Rightarrow$ \ \rest{25 lanzamientos de 1 punto, 30 de 2 puntos y 25 de 3 puntos}."),
 (2, r"\pau{Murcia, extraordinaria 2026} Una empresa prepara cajas de fruta de tres tipos. Las cajas A llevan 1 manzana, 1 pera y 1 naranja; las B, 2 manzanas, 1 pera y 1 naranja, y las C, 1 manzana, 2 peras y 1 naranja. Un día prepararon $x$ cajas A, $y$ cajas B y $z$ cajas C, y utilizaron 400 manzanas, 500 peras y $k$ naranjas."
     + tasks(1, [r"Plantea un sistema de ecuaciones para averiguar cuántas cajas de cada tipo prepararon.", r"Discute y resuelve el sistema, dando la solución en función del parámetro $k$."]),
     tasks(1, [pr(MR6(Sym('k'))), r"$|A|=" + q(det(coef(MR6(0)))) + r"\neq0$: \rest{SCD para todo $k$}. Restando la 3.ª a las otras: $y=400-k$, $z=500-k$, y $x=k-y-z$: \ $\res{x=3k-900;\ y=400-k;\ z=500-k}$. \ Para que tenga sentido, $k$ debe ser un número natural entre 300 y 400."])),
 (2, r"\pau{Murcia, ordinaria 2026} Darío y Cayetana invierten $x$ miles de euros en publicidad, $y$ en materiales y $z$ en logística, 12 mil euros en total. Darío propone que la inversión en publicidad más el doble de la inversión en materiales sea igual a la inversión en logística más $k$, donde $k>0$ es un parámetro de ajuste económico. Cayetana quiere que el doble de la inversión en publicidad menos la de materiales más la de logística sea 4 mil euros."
     + tasks(1, [r"Plantea un sistema de 3 ecuaciones con 3 incógnitas que recoja los datos del problema.", r"Discute el sistema y, si tiene solución única, hállala en función de $k$."]),
     tasks(1, [pr(MR7(Sym('k'))), r"$|A|=-7\neq0$ para todo $k$: \rest{SCD}. Por Cramer: \ $\res{x=\tfrac{2k}{7};\ y=4+\tfrac{k}{7};\ z=8-\tfrac{3k}{7}}$"])),
 (2, r"\pau{País Vasco, extraordinaria 2026} Una central lechera recoge leche de tres productores. El productor A lleva la leche en recipientes de 10 litros y cobra 5 € por recipiente; el B, en recipientes de 15 litros y cobra 9 € por recipiente, y el C, en recipientes de 12 litros y cobra 4 € por recipiente. La última semana se han recogido 612 litros en 48 recipientes y hay que pagar 304 €."
     + tasks(1, [r"Plantea el sistema de ecuaciones que modeliza la situación.", r"¿Cuánto hay que pagar a cada productor por la leche que ha llevado la última semana?"]),
     tasks(1, [r"$a$, $b$, $c$: recipientes de cada productor: \ " + pr(PV6, 'abc'), r"Solución: $a=12$, $b=20$, $c=16$: \ \rest{60 € a A, 180 € a B y 64 € a C}."])))

# =====================================================================
# comprovacions
def inv_ok(A, Ai):
    n = len(A)
    return all(sum(fr(A[i][k]) * fr(Ai[k][j]) for k in range(n)) == (1 if i == j else 0) for i in range(n) for j in range(n))
for c in CHK:
    k = c[0]
    if k == 'cls': assert classif(c[1]) == c[2], (c[1], classif(c[1]), c[2])
    elif k == 'det': assert det(c[1]) == fr(c[2]), (c[1], det(c[1]), c[2])
    elif k == 'inv': assert inv_ok(c[1], c[2]), c[1]
    elif k == 'rank': assert rank(c[1]) == c[2], c[1]
    elif k == 'no': assert not satisfies(c[1], c[2]), c
    elif k == 'sol':
        R, s = c[1], c[2]
        if callable(s):
            na = s.__code__.co_argcount
            for t in [(F(v),) * na if na == 1 else (F(v), F(v * v - 3)) for v in range(-3, 4)]:
                assert satisfies(R, s(*t[:na])), (R, t)
            assert rank(coef(R)) == len(R[0]) - 1 - na, (R, 'paràmetres')
        else:
            assert satisfies(R, s), (R, s)
# Gauss: la matriu final ha de ser esglaonada i equivalent a la inicial (mateix rang de A i de A*)
for R, M in GA:
    assert rank(coef(M)) == rank(coef(R)) and rank(M) == rank(R)
    lead = [next((j for j, v in enumerate(r) if v != 0), 99) for r in M]
    assert all(lead[i] < lead[i + 1] or lead[i + 1] == 99 for i in range(len(lead) - 1)), M
print(len(CHK), 'comprovacions correctes')

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre = pre.replace(r'\usepackage{amsmath,amssymb}', r'\usepackage{amsmath,amssymb}' + '\n' + r'\allowdisplaybreaks')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
TIT = "Sistemas de ecuaciones lineales"
KW = "sistemas de ecuaciones lineales, método de Gauss, método matricial, regla de Cramer, teorema de Rouché-Frobenius, sistemas homogéneos, discusión de sistemas, parámetros, problemas, PAU"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 2: %s' % (t, TIT), capcalera='%s · Unidad 2: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 2' if sol else 'Ficha de ejercicios · Unidad 2') + '}{' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los pasos de Gauss pueden ser distintos de los tuyos y ser igualmente correctos; lo que debe coincidir es la clasificación y la solución (en un SCI, la solución general se puede escribir de maneras distintas según la incógnita que tomes como parámetro). Puedes comprobarlo con el resolutor de sistemas de los apuntes interactivos."
             if sol else r"Resuelve los ejercicios en el cuaderno justificando cada paso: indica siempre el método que utilizas y, en los problemas, qué representa cada incógnita. En las discusiones con parámetros, estudia \textbf{todos} los casos. Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas (2024--2026).") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con el resolutor de sistemas de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't2-fitxa-solucions-es.tex' if sol else 't2-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'ejercicios,', npau, 'de la PAU de otras comunidades')
