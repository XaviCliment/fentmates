# Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 2: Sistemes d'equacions lineals)
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
S.append(("Sistemes d'equacions lineals. Mètode de Gauss", [
 (1, r"Resol pel mètode de Gauss el sistema de quatre equacions i quatre incògnites:" + pr(R1, 'xyzt')
     + recorda(r"Fes zeros davall de la diagonal amb operacions entre files de la matriu ampliada i després resol de baix cap amunt. Tria com a fila pivot la que tinga un 1 en la columna que vols anul·lar."),
     G(R1, (1, -1, 2, 0), 'SCD') + r"Resolent de baix cap amunt: \ $\res{x=1;\ y=-1;\ z=2;\ t=0}$"),
 (2, r"Discuteix i resol, quan siga possible, pel mètode de Gauss:" + tasks(1, [m(sy(R2a, 'xyzt')), m(sy(R2b)), m(sy(R2c))]),
     tasks(1, [G(R2a, cls='SCI') + r"Rang 2 amb 4 incògnites: \rest{SCI amb dos paràmetres}. Amb $z=\lambda$, $t=\mu$: \ $y=-1+3\lambda-3\mu$, \ $x=1-y+z-t$:\par $\res{x=2-2\lambda+2\mu;\ y=-1+3\lambda-3\mu;\ z=\lambda;\ t=\mu}$",
               G(R2b, cls='SCD') + r"La 4a fila s'anul·la: queden tres equacions independents. \rest{SCD}: \ $\res{x=1;\ y=2;\ z=3}$",
               r"Els mateixos passos donen la darrera fila $(0\ 0\ 0\,|\,1)$: \ \rest{SI}. (Les tres primeres equacions obliguen $x=1$, $y=2$, $z=3$, i aleshores $3x+2y=7\neq8$.)"])),
 (3, r"Discuteix pel mètode de Gauss el sistema següent segons els valors de $k$ i $m$, i resol-lo quan siga compatible indeterminat:" + dm(sy(R3(Sym('k'), Sym('m')))),
     dm(r"\left(\begin{array}{rrr|r}1 & 2 & -1 & 1\\ 2 & 1 & 1 & 4\\ 4 & 5 & k & m\end{array}\right)\xrightarrow[F_3'=F_3-4F_1]{F_2'=F_2-2F_1}\left(\begin{array}{rrr|r}1 & 2 & -1 & 1\\ 0 & -3 & 3 & 2\\ 0 & -3 & k+4 & m-4\end{array}\right)\xrightarrow{F_3''=F_3'-F_2'}\left(\begin{array}{rrr|r}1 & 2 & -1 & 1\\ 0 & -3 & 3 & 2\\ 0 & 0 & k+1 & m-6\end{array}\right)")
     + tasks(1, [r"Si $k\neq-1$: \ \rest{SCD} (per a qualsevol $m$).", r"Si $k=-1$ i $m=6$: la 3a fila és nul·la: \ \rest{SCI}.", r"Si $k=-1$ i $m\neq6$: la 3a fila diu $0=m-6\neq0$: \ \rest{SI}."])
     + r"Per a $k=-1$, $m=6$, amb $z=\lambda$: \ $-3y+3\lambda=2\Rightarrow y=\lambda-\tfrac23$; \ $x=1-2y+z$:\par $\res{x=\tfrac73-\lambda;\ y=-\tfrac23+\lambda;\ z=\lambda}$"),
 (2, r"Escriu un sistema de tres equacions amb tres incògnites, sense cap coeficient nul en la tercera equació, que tinga com a solució general \ $x=1+\lambda$, \ $y=2-\lambda$, \ $z=\lambda$.",
     r"Hi ha infinites respostes. Busquem relacions que complisquen totes les solucions: $x+y=3$ i $y+z=2$. La tercera equació ha de ser combinació lineal de les dues (si no, el sistema seria SCD); per exemple, la suma: $x+2y+z=5$:" + dm(r"\boxed{" + sy(R4) + "}")),
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
S.append(("Expressió matricial. Mètode matricial", [
 (2, r"Siga \ $A=" + pm(A6) + r"$. Resol pel mètode matricial els sistemes $AX=B_1$ i $AX=B_2$, amb \ $B_1=" + pm([[b] for b in B6a]) + r"$ \ i \ $B_2=" + pm([[b] for b in B6b]) + r"$, calculant una sola vegada la matriu inversa."
     + recorda(r"Si $|A|\neq0$: \ $A\cdot X=B\Rightarrow X=A^{-1}\cdot B$. Quan diversos sistemes tenen la mateixa matriu de coeficients, n'hi ha prou de calcular $A^{-1}$ una vegada."),
     r"$|A|=5$, \ $\mathrm{Adj}(A)=" + pm(adjm(A6)) + r"$, \ $A^{-1}=\frac15" + pm(tr(adjm(A6))) + r"$."
     + dm(r"X_1=\frac15" + pm(tr(adjm(A6))) + pm([[b] for b in B6a]) + r"=\boxed{\begin{pmatrix}1\\ 0\\ 1\end{pmatrix}},\qquad X_2=\frac15" + pm(tr(adjm(A6))) + pm([[b] for b in B6b]) + r"=\boxed{\begin{pmatrix}2\\ -1\\ 1\end{pmatrix}}")),
 (2, r"Troba la matriu columna $X=\begin{pmatrix}x\\ y\\ z\end{pmatrix}$ tal que $AX=X+B$, essent \ $A=" + pm(A7) + r"$ \ i \ $B=" + pm([[b] for b in B7]) + r"$.",
     r"$AX-X=B\Rightarrow(A-I)X=B$, \ amb $A-I=" + pm(N7) + r"$, \ $|A-I|=4$, \ $(A-I)^{-1}=\frac14" + pm(tr(adjm(N7))) + r"$:"
     + dm(r"X=\frac14" + pm(tr(adjm(N7))) + pm([[b] for b in B7]) + r"=\boxed{\begin{pmatrix}1\\ -1\\ 1\end{pmatrix}}")),
 (3, r"Considera el sistema \ $" + sy(R8(Sym('k'))) + r"$" + tasks(1, [r"Per a quins valors de $k$ es pot resoldre pel mètode matricial?", r"Resol-lo pel mètode matricial en funció de $k$.", r"Què passa quan $k=2$?"]),
     tasks(1, [r"$|A|=" + vm(coef(R8(Sym('k')))) + r"=k-1-1=k-2$: \ si \ $\res{k\neq2}$",
               r"$\mathrm{Adj}(A)=\begin{pmatrix}k-1 & -1 & 1\\ -1 & 1 & -1\\ 1 & -1 & k-1\end{pmatrix}$ (és simètrica), \ $A^{-1}=\dfrac{1}{k-2}\begin{pmatrix}k-1 & -1 & 1\\ -1 & 1 & -1\\ 1 & -1 & k-1\end{pmatrix}$:"
               + dm(r"X=\frac{1}{k-2}\begin{pmatrix}k-1+0+1\\ -1+0-1\\ 1+0+k-1\end{pmatrix}=\frac{1}{k-2}\begin{pmatrix}k\\ -2\\ k\end{pmatrix}\ \Rightarrow\ \boxed{x=z=\tfrac{k}{k-2};\ \ y=\tfrac{2}{2-k}}"),
               r"$|A|=0$: la suma de la 1a i la 3a equacions dona $x+2y+z=2$, que contradiu la 2a ($x+2y+z=0$): \ \rest{SI}."])),
 (3, r"Siga $AX=B$ un sistema de $n$ equacions i $n$ incògnites." + tasks(1, [r"Demostra que, si $|A|\neq0$, el sistema té una única solució per a qualsevol $B$, i que el sistema homogeni $AX=O$ només té la solució trivial.",
     r"Demostra que, si $X_1$ i $X_2$ són solucions de $AX=B$, aleshores $X_1-X_2$ és solució de $AX=O$, i que $X_1+t\,(X_2-X_1)$ és solució de $AX=B$ per a tot $t\in\mathbb{R}$.", r"Dedueix que un sistema lineal no pot tenir exactament dues solucions."]),
     tasks(1, [r"Si $AX=B$, multiplicant per $A^{-1}$ per l'esquerra, $X=A^{-1}B$: la solució existeix i és única. Amb $B=O$, $X=A^{-1}O=O$.",
               r"$A(X_1-X_2)=AX_1-AX_2=B-B=O$; \ \ $A\big(X_1+t(X_2-X_1)\big)=B+t\,(B-B)=B$.",
               r"Si en té dues de diferents, $X_1+t(X_2-X_1)$ dona una solució diferent per a cada $t$: en té \rest{infinites}."])),
]))

# =====================================================================
R10 = lambda a: [[a, 1, 1, 1], [1, a, 1, 1], [1, 1, a, 1]]
detpoly(R10, lambda a: (a - 1) ** 2 * (a + 2))
for a in HV:
    if a not in (1, -2): ck('sol', R10(a), (1 / (a + 2),) * 3)
R12 = [[1, 1, 1, 2], [1, -1, 2, 1], [2, 0, 3, 3]]
ck('cls', R12, 'SCI'); ck('sol', R12, lambda l: ((3 - 3 * l) / 2, (1 + l) / 2, l))
S.append(("Regla de Cramer", [
 (2, r"Resol per la regla de Cramer, en funció de $a$, el sistema \ $" + sy(R10(Sym('a'))) + r"$ \ en els casos en què siga un sistema de Cramer."
     + recorda(r"Un sistema és de Cramer si té tantes equacions com incògnites i $|A|\neq0$. Aleshores $x=\dfrac{|A_x|}{|A|}$, \ldots, on $A_x$ s'obté substituint la columna de $x$ per la de termes independents."),
     r"$|A|=a^3-3a+2=(a-1)^2(a+2)$: és de Cramer si $a\neq1$ i $a\neq-2$. \ Sumant totes les columnes a la primera i traient factor comú:"
     + dm(r"|A_x|=\begin{vmatrix}1 & 1 & 1\\ 1 & a & 1\\ 1 & 1 & a\end{vmatrix}=(a-1)^2,\qquad x=\frac{(a-1)^2}{(a-1)^2(a+2)}=\frac{1}{a+2}")
     + r"i, de la mateixa manera (o per la simetria del sistema), $|A_y|=|A_z|=(a-1)^2$: \ $\res{x=y=z=\tfrac{1}{a+2}}$"),
 (3, r"Calcula, aplicant la regla de Cramer, només el valor de $t$ en el sistema de l'exercici \ref{ex:g4}.",
     r"$|A|=" + q(det(coef(R1))) + r"$ \ i \ $|A_t|=" + vm([r[:3] + [r[4]] for r in R1]) + '=' + q(det([r[:3] + [r[4]] for r in R1])) + r"$: \ $t=\dfrac{0}{" + q(det(coef(R1))) + r"}=\res{0}$, \ com havíem obtingut per Gauss."),
 (2, r"El sistema \ $" + sy(R12) + r"$ \ és compatible indeterminat. Resol-lo aplicant la regla de Cramer (passa $z$ al segon membre).",
     r"La 3a equació és la suma de les dues primeres, i $\begin{vmatrix}1 & 1\\ 1 & -1\end{vmatrix}=-2\neq0$: \ $\left\{\begin{aligned}x+y&=2-z\\ x-y&=1-2z\end{aligned}\right.$"
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
S.append(("Sistemes homogenis", [
 (2, r"Discuteix el sistema homogeni \ $" + sy(H14(Sym('a'))) + r"$ \ segons els valors de $a$ i resol-lo quan tinga solucions diferents de la trivial."
     + recorda(r"Un sistema homogeni sempre és compatible. Si $\operatorname{rg}(A)=r<n$, és SCI i la solució depèn de $n-r$ paràmetres."),
     r"$|A|=-a^3+3a-2=-(a-1)^2(a+2)$." + tasks(1, [r"Si $a\neq1$ i $a\neq-2$: \ \rest{SCD}, només la solució trivial \ $x=y=z=0$.",
     r"Si $a=1$: les tres equacions són $x+y+z=0$, rang 1: \ \rest{SCI amb dos paràmetres}:\par $\res{x=-\lambda-\mu;\ y=\lambda;\ z=\mu}$",
     r"Si $a=-2$: rang 2 ($\begin{vmatrix}1 & 1\\ 1 & -2\end{vmatrix}\neq0$). De les dues primeres, $x+y=2z$ i $x-2y=-z$: $y=z$, $x=z$: \ $\res{x=y=z=\lambda}$"])),
 (2, r"Resol el sistema homogeni \ $" + sy(H15, 'xyzt') + r"$ \ i digues quants paràmetres té la solució.",
     r"La 3a equació és la suma de les dues primeres i les dues primeres no són proporcionals: $\operatorname{rg}(A)=2$, amb 4 incògnites: \rest{dos paràmetres}. De la 3a, $x=-\tfrac32z$; amb $z=\lambda$, $t=\mu$, de la 1a, $y=-x-z-t$:"
     + dm(r"\boxed{x=-\tfrac32\lambda;\ \ y=\tfrac12\lambda-\mu;\ \ z=\lambda;\ \ t=\mu}")),
 (2, r"Escriu un sistema homogeni de dues equacions amb tres incògnites les solucions del qual siguen $(\lambda,\ 2\lambda,\ -\lambda)$, $\lambda\in\mathbb{R}$. Per a quin valor de $k$ l'equació $kx+y+3z=0$ també la compleixen totes aquestes solucions?",
     r"Per exemple, $y=2x$ i $z=-x$: \ $\res{" + sy(H16) + r"}$ \ (el rang és 2, de manera que la solució depèn d'un paràmetre). \ $k\lambda+2\lambda-3\lambda=0\Rightarrow\res{k=1}$"),
 (3, r"Raona les afirmacions següents:" + tasks(1, [r"Un sistema homogeni amb més incògnites que equacions sempre té solucions diferents de la trivial.", r"Si un sistema homogeni quadrat té alguna solució no trivial, aleshores $|A|=0$.",
     r"Si $X_1$ i $X_2$ són solucions d'un sistema homogeni, $aX_1+bX_2$ també ho és, per a qualssevol $a,b\in\mathbb{R}$."]),
     tasks(1, [r"\rest{Vertadera}: $\operatorname{rg}(A)\leq$ nombre d'equacions $<n$, i un sistema homogeni sempre és compatible: és SCI.", r"\rest{Vertadera}: si $|A|\neq0$, seria SCD i només tindria la solució trivial.",
               r"\rest{Vertadera}: $A(aX_1+bX_2)=aAX_1+bAX_2=aO+bO=O$."])),
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
 (2, r"\label{ex:r4}Classifica, sense resoldre'ls, els sistemes de quatre equacions i tres incògnites següents, i resol el que siga compatible:" + tasks(2, [m(sy(R18a)), m(sy(R18b))])
     + recorda(r"Amb 4 equacions i 3 incògnites, $\operatorname{rg}(A)\leq3$. Si $|A^*|\neq0$, aleshores $\operatorname{rg}(A^*)=4\neq\operatorname{rg}(A)$ i el sistema és incompatible."),
     r"El menor de les tres primeres files de $A$ val $" + q(det([r[:3] for r in R18a[:3]])) + r"\neq0$, i $\operatorname{rg}(A)=3$."
     + tasks(1, [r"$|A^*|=0$: \ $\operatorname{rg}(A^*)=3=n$: \ \rest{SCD}. Resolent les tres primeres equacions: \ $\res{x=y=z=1}$ \ (que també compleix la 4a).",
                 r"$|A^*|=" + q(det(R18b)) + r"\neq0$: \ $\operatorname{rg}(A^*)=4\neq3$: \ \rest{SI}."])),
 (2, r"Estudia el sistema \ $" + sy(R19, 'xyzt') + r"$ \ amb el teorema de Rouché-Frobenius i resol-lo.",
     r"Les dues primeres columnes són proporcionals, i també la 3a i la 4a (amb signe canviat): $\operatorname{rg}(A)\leq2$, i $\begin{vmatrix}1 & -1\\ 2 & 1\end{vmatrix}=3\neq0$ dona $\operatorname{rg}(A)=2$. La 3a equació és $E_2-E_1$, de manera que $\operatorname{rg}(A^*)=2<4$: \rest{SCI amb dos paràmetres}."
     r"\par Sumant les dues primeres: $3x+6y=6$; amb $y=\lambda$, $t=\mu$: \ $\res{x=2-2\lambda;\ y=\lambda;\ z=-1+\mu;\ t=\mu}$"),
 (2, r"Troba la relació que han de complir $a$, $b$ i $c$ perquè el sistema \ $" + sy(R21(Sym('a'), Sym('b'), Sym('c'))) + r"$ \ siga compatible. Pot ser compatible determinat?",
     r"$|A|=" + vm(coef(R21(0, 0, 0))) + r"=0$ i $\begin{vmatrix}1 & 1\\ 1 & -1\end{vmatrix}\neq0$: $\operatorname{rg}(A)=2$ sempre, de manera que \rest{mai no és SCD}. Com que $F_3=2F_1+F_2$ en la matriu $A$, el sistema és compatible si i només si els termes independents compleixen la mateixa relació:"
     + dm(r"\boxed{c=2a+b}") + r"(i aleshores és SCI; si no, $\operatorname{rg}(A^*)=3$ i és SI)."),
 (2, r"Digues si són vertaderes o falses les afirmacions següents i justifica-ho:" + tasks(1, [r"Un sistema de 4 equacions i 3 incògnites amb $\operatorname{rg}(A)=3$ sempre és compatible determinat.",
     r"Un sistema de 3 equacions i 4 incògnites no pot ser compatible determinat.", r"Si en un sistema de 4 equacions i 3 incògnites $|A^*|\neq0$, el sistema és incompatible.",
     r"Si un sistema de 3 equacions i 3 incògnites té $|A|=0$, és incompatible."]),
     tasks(1, [r"\rest{Falsa}: pot ser $\operatorname{rg}(A^*)=4$ (és el cas del segon sistema de l'exercici \ref{ex:r4}).", r"\rest{Vertadera}: $\operatorname{rg}(A)\leq3<4=n$.",
               r"\rest{Vertadera}: $\operatorname{rg}(A^*)=4$ i $\operatorname{rg}(A)\leq3$.", r"\rest{Falsa}: pot ser SCI (si $\operatorname{rg}(A)=\operatorname{rg}(A^*)<3$)."])),
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
S.append(("Discussió de sistemes amb paràmetres", [
 (2, r"Discuteix el sistema següent segons els valors de $a$ i resol-lo en tots els casos en què siga compatible:" + dm(sy(R22(Sym('a'))))
     + recorda(r"Calcula $|A|$ i troba'n les arrels (valors crítics). Per a la resta de valors el sistema és SCD; cada valor crític s'estudia a banda amb Rouché-Frobenius."),
     r"$|A|=(a-1)^2(a+2)$." + tasks(1, [r"Si $a\neq1$ i $a\neq-2$: \rest{SCD}. Per Cramer (o restant les equacions dues a dues):\par $\res{x=-\tfrac{a+1}{a+2};\ \ y=\tfrac{1}{a+2};\ \ z=\tfrac{(a+1)^2}{a+2}}$",
     r"Si $a=1$: les tres equacions són $x+y+z=1$: \ \rest{SCI amb dos paràmetres}:\par $\res{x=1-\lambda-\mu;\ y=\lambda;\ z=\mu}$",
     r"Si $a=-2$: sumant les tres equacions, $0=1-2+4=3$: \ \rest{SI} (\,$\operatorname{rg}(A)=2$, $\operatorname{rg}(A^*)=3$)."])),
 (2, r"Discuteix el sistema següent segons els valors de $a$ i $b$, i resol-lo quan siga compatible indeterminat:" + dm(sy(R23(Sym('a'), Sym('b')))),
     r"$|A|=" + vm(coef(R23(Sym('a'), 0))) + r"=3-a$." + tasks(1, [r"Si $a\neq3$: \ \rest{SCD}.", r"Si $a=3$ i $b=3$: la 3a equació és la suma de les dues primeres: \rest{SCI}.", r"Si $a=3$ i $b\neq3$: els coeficients de la 3a són la suma dels de les altres, però el terme independent no: \rest{SI}."])
     + r"Per a $a=b=3$, restant les dues primeres: $y+2z=1$; amb $z=\lambda$: \ $\res{x=\lambda;\ y=1-2\lambda;\ z=\lambda}$"),
 (2, r"Discuteix, segons els valors de $a$, el sistema de tres equacions i dues incògnites \ $" + sy(R24(Sym('a')), 'xy') + r"$, \ i resol-lo quan siga compatible.",
     r"$\operatorname{rg}(A)=2$ sempre ($\begin{vmatrix}1 & 2\\ 2 & -1\end{vmatrix}=-5\neq0$). \ $|A^*|=" + vm(R24(Sym('a'))) + r"=5a-5$." + tasks(1, [r"Si $a\neq1$: $\operatorname{rg}(A^*)=3$: \ \rest{SI}.", r"Si $a=1$: $\operatorname{rg}(A^*)=2=n$: \ \rest{SCD}: \ $\res{x=1;\ y=1}$"])),
 (3, r"Discuteix, segons els valors de $k$ i de $a$, el sistema \ $" + sy(R25(Sym('k'), Sym('a')), 'xyzt') + r"$",
     r"Sumant les dues primeres equacions: $2x+2z=1+a$. Les dues primeres files de $A$ no són proporcionals, així que $\operatorname{rg}(A)\geq2$."
     + tasks(1, [r"Si $k\neq2$: el menor de les columnes 1a, 2a i 3a, $" + vm([[1, 1, 1], [1, -1, 1], [2, 0, Sym('k')]]) + r"=-k+2\neq0$: \ $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3<4$: \ \rest{SCI amb un paràmetre}.",
                 r"Si $k=2$ i $a=2$: la 3a equació, $2x+2z=3$, coincideix amb la suma de les dues primeres: rang 2: \ \rest{SCI amb dos paràmetres}.",
                 r"Si $k=2$ i $a\neq2$: $2x+2z=3$ i $2x+2z=1+a$ es contradiuen: \ \rest{SI}."])),
 (2, r"Discuteix el sistema \ $" + sy(R26(Sym('m'))) + r"$ \ segons els valors de $m$ i resol-lo per a $m=0$ i per a $m=2$.",
     r"$|A|=" + vm(coef(R26(Sym('m')))) + r"=m-1$." + tasks(1, [r"Si $m\neq1$: \ \rest{SCD}.", r"Si $m=1$: la 1a equació és $x+y+z=2$ i la 3a, $x+y+z=1$: \ \rest{SI}.",
     r"$m=0$: \ $x+y+z=1$, \ $y-z=0$, \ $x+z=1$ \ $\Rightarrow$ \ $\res{x=1;\ y=0;\ z=0}$",
     r"$m=2$: \ $x+y+z=3$, \ $2x+y+z=2$, \ $x+2y+z=1$ \ $\Rightarrow$ \ $\res{x=%s;\ y=%s;\ z=%s}$" % tuple(q(v, 'tfrac') for v in S26)])),
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
S.append(("Problemes de plantejament", [
 (2, r"Un nombre de tres xifres compleix que la suma de les xifres és 12, que la xifra de les desenes és igual a la suma de les altres dues i que, si s'inverteix l'ordre de les xifres, el nombre augmenta en 396. Quin és el nombre?"
     + recorda(r"Si les xifres són $x$ (centenes), $y$ (desenes) i $z$ (unitats), el nombre val $100x+10y+z$."),
     r"$(100z+10y+x)-(100x+10y+z)=396\Leftrightarrow-99x+99z=396$:" + pr(N28) + r"De la 1a i la 3a: $2y=12$, $y=6$; aleshores $x+z=6$ i $z-x=4$: \ el nombre és \rest{165}."),
 (2, r"Troba el polinomi de tercer grau $p(x)=ax^3+bx^2+cx+d$ la gràfica del qual passa pels punts $(-1,-4)$, $(0,1)$, $(1,2)$ i $(2,11)$.",
     r"Substituint cada punt: \ " + pr(P29, 'abcd') + r" \ $d=1$; sumant la 1a i la 3a: $2b+2d=-2$, $b=-2$; aleshores $a+c=3$ i $8a+2c=18$: $a=2$, $c=1$." + dm(r"\boxed{p(x)=2x^3-2x^2+x+1}")),
 (2, r"Tenim 10 monedes d'1 €, de 2 € i de 5 € que sumen 25 €." + tasks(1, [r"Planteja el sistema i comprova que és compatible indeterminat. Escriu-ne la solució general.", r"Quines són les solucions possibles en el context del problema?",
     r"Quantes monedes hi ha de cada tipus si hi ha més monedes d'1 € que de 2 €?"]),
     tasks(1, [r"$x$, $y$, $z$: monedes d'1, 2 i 5 €. \ " + pr(M30) + r" \ Rang 2 i 3 incògnites: \rest{SCI}. Restant: $y+4z=15$; amb $z=\lambda$: \ $\res{x=-5+3\lambda;\ y=15-4\lambda;\ z=\lambda}$",
               r"Han de ser naturals: $x\geq0\Rightarrow\lambda\geq\tfrac53$ i $y\geq0\Rightarrow\lambda\leq\tfrac{15}{4}$, de manera que $\lambda=2$ o $\lambda=3$: \ \rest{1, 7 i 2} \ o \ \rest{4, 3 i 3} monedes.",
               r"\rest{4 monedes d'1 €, 3 de 2 € i 3 de 5 €}."])),
 (3, r"Un teatre ven 100 entrades de tres tipus: generals a 10 €, infantils a 5 € i sèniors a $k$ euros. Ha recaptat 600 € i ha venut tantes entrades infantils com sèniors." + tasks(1, [r"Planteja el sistema i discuteix-lo segons els valors de $k$.",
     r"Si l'entrada sènior costa 5 €, quantes entrades de cada tipus s'han venut?", r"Pot ser que l'entrada sènior coste 10 €? Raona-ho."]),
     tasks(1, [r"$x$ generals, $y$ infantils, $z$ sèniors: \ " + pr(T31(Sym('k'))) + r" \ $|A|=" + vm(coef(T31(Sym('k')))) + r"=k-15$. Si $k\neq15$: \rest{SCD}; si $k=15$: amb $y=z$, $x+2y=100$ i $10x+20y=600$ es contradiuen: \rest{SI}.",
               r"\rest{20 generals, 40 infantils i 40 sèniors}.", r"Amb $k=10$ el sistema és SCD, però la solució és $x=-60$, $y=z=80$: \rest{no té sentit} (no hi pot haver un nombre negatiu d'entrades)."])),
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
pau("Sistemes d'equacions lineals. Mètode de Gauss",
 (2, r"\pau{Andalusia, extraordinària 2025} Se sap que la suma de tres nombres naturals és 22 i que la suma de quatre vegades el primer més el triple del segon més el doble del tercer és 61. Pot ser 15 un dels tres nombres? En cas afirmatiu, calcula els altres. Hi ha altres opcions?",
     r"" + pr(A25) + r" \ Restant a la 2a el doble de la 1a: $2x+y=17$. Amb $x=\lambda$: \ $y=17-2\lambda$, \ $z=5+\lambda$ (\rest{SCI})."
     r"\par Perquè siguen naturals, $\lambda\geq1$ i $17-2\lambda\geq1$: $\lambda=1,\dots,8$. El 15 només pot ser $y$ (amb $\lambda=1$): \ \rest{1, 15 i 6}. Les altres opcions són $(2,13,7)$, $(3,11,8)$, $(4,9,9)$, $(5,7,10)$, $(6,5,11)$, $(7,3,12)$ i $(8,1,13)$."))

# --- 2. Expressió matricial
RIO = lambda a: [[1, -1, a, a], [a, 1, -1, a], [a + 1, 0, 1, a + 2]]
detpoly(RIO, lambda a: -(a - 2) * (a + 1))
for a in HV: ck('sol', RIO(a), (1, 1, 1))
pau("Expressió matricial. Mètode matricial",
 (2, r"\pau{La Rioja, extraordinària 2024} Donat el sistema d'equacions lineals dependent del paràmetre real $a$" + dm(sy(RIO(Sym('a')))) + r"troba la matriu $A^{-1}b$ sense calcular la matriu inversa de $A$, essent $A$ la matriu de coeficients i $b$ la de termes independents.",
     r"$A^{-1}b$ és la solució $X$ del sistema $AX=b$ (quan $A$ és invertible: $|A|=-a^2+a+2=-(a-2)(a+1)\neq0$, és a dir, $a\neq2$ i $a\neq-1$). Observant el sistema, $x=y=z=1$ compleix les tres equacions: $1-1+a=a$, $a+1-1=a$, $a+1+1=a+2$. Com que la solució és única:"
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
 (3, r"\pau{Illes Balears, extraordinària 2025} Donat el sistema \ $" + sy(BAL(Sym('k'))) + r"$, \ on $k$ és un nombre real qualsevol:" + tasks(1, [r"Discuteix, segons el paràmetre $k$, el nombre de solucions que té el sistema.", r"Resol el sistema quan siga possible."]),
     tasks(1, [r"$|A|=" + vm(coef(BAL(Sym('k')))) + r"=-k^2+k+3$, que s'anul·la per a $k=\frac{1\pm\sqrt{13}}{2}$. Si $k\neq\frac{1\pm\sqrt{13}}{2}$: \rest{SCD}. Si $k=\frac{1\pm\sqrt{13}}{2}$: $\begin{vmatrix}k & 1\\ 0 & k\end{vmatrix}=k^2\neq0$, així que $\operatorname{rg}(A)=2$, i el menor de $A^*$ \ $" + vm([[Sym('k'), 1, 1], [0, Sym('k'), 0], [3, -1, 0]]) + r"=-3k\neq0$ dona $\operatorname{rg}(A^*)=3$: \rest{SI}.",
               r"Per Cramer, amb $|A_x|=1-k$, $|A_y|=3$, $|A_z|=-3k$:" + dm(r"\boxed{x=\frac{1-k}{-k^2+k+3};\quad y=\frac{3}{-k^2+k+3};\quad z=\frac{-3k}{-k^2+k+3}}")])),
 (2, r"\pau{Catalunya, extraordinària 2026} Considera el sistema d'equacions \ $" + sy(CAT(Sym('k'))) + r"$, \ on $k$ és un paràmetre real." + tasks(1, [r"Discuteix el sistema en funció del paràmetre $k$.", r"Resol el sistema per a tots els valors de $k$ i comprova que, per a $k\neq1$, la solució no depèn de $k$."]),
     tasks(1, [r"$|A|=3k-3$. Si $k\neq1$: \rest{SCD}. Si $k=1$: $\begin{vmatrix}-1 & 2\\ 1 & 1\end{vmatrix}\neq0$, $\operatorname{rg}(A)=2$, i $3E_1=5E_3-E_2$, també en els termes independents: \rest{SCI}.",
               r"Si $k\neq1$, per Cramer: $|A_y|=" + vm(mn(CAT(0), [0, -1, 2])) + r"=0\Rightarrow y=0$, i aleshores $-x+2z=1$, $x+z=2$: \ $\res{x=1;\ y=0;\ z=1}$, que no depèn de $k$. Si $k=1$: restant la 1a i la 3a, $x=1$, i $y+z=1$: \ $\res{x=1;\ y=1-\lambda;\ z=\lambda}$"])))

# --- 4. Homogenis
RIH = lambda m: [[3, 1, -1, 0], [3, 2, -m, 0], [1, -1, -1, 0]]
detpoly(RIH, lambda m: 2 - 4 * m, HV); par(RIH, {F(1, 2): 'SCI'}, HV); ck('sol', RIH(F(1, 2)), lambda l: (l, -l, 2 * l))
pau("Sistemes homogenis",
 (2, r"\pau{La Rioja, ordinària 2025} Donat el sistema d'equacions homogeni \ $" + sy(RIH(Sym('m'))) + r"$, \ indica per a quins valors de $m$ el sistema té només la solució trivial. Resol el sistema per a un valor de $m$ que el faça compatible indeterminat.",
     r"$|A|=2-4m$. Si $m\neq\tfrac12$: \rest{només la solució trivial}. Per a $\res{m=\tfrac12}$, $\operatorname{rg}(A)=2$ (\,$\begin{vmatrix}3 & 1\\ 1 & -1\end{vmatrix}\neq0$): de la 1a i la 3a, $4x=2z$ i $y=z-3x$:"
     + dm(r"\boxed{x=\lambda;\ \ y=-\lambda;\ \ z=2\lambda,\quad\lambda\in\mathbb{R}}")))

# --- 5. Rouché-Frobenius
BL6 = [[2, 1, 1, 6500], [4, 5, 7, 22500], [1, 2, 3, 8000]]
ck('cls', BL6, 'SCI'); ck('det', coef(BL6), 0); ck('rank', coef(BL6), 2)
pau("Teorema de Rouché-Frobenius",
 (2, r"\pau{Illes Balears, extraordinària 2026} Volem determinar el cost per hora de tres serveis d'una empresa de lloguer de material audiovisual: il·luminació professional ($x$ €/hora), equip de so ($y$ €/hora) i càmeres d'enregistrament ($z$ €/hora). S'han registrat les despeses totals de tres esdeveniments:"
     + dm(r"\begin{aligned}&\text{Esdeveniment 1: } & 2x+y+z&=6500\\ &\text{Esdeveniment 2: } & 4x+5y+7z&=22500\\ &\text{Esdeveniment 3: } & x+2y+3z&=8000\end{aligned}")
     + r"Justifica si, amb aquesta informació, es poden determinar de manera única els costos dels tres serveis.",
     r"$|A|=" + vm(coef(BL6)) + r"=0$ i $\begin{vmatrix}2 & 1\\ 4 & 5\end{vmatrix}=6\neq0$: $\operatorname{rg}(A)=2$. La 2a equació és la suma de la 1a i el doble de la 3a, també en els termes independents ($6500+16000=22500$): $\operatorname{rg}(A^*)=2<3$."
     r" \ \rest{SCI}: \rest{no} es poden determinar de manera única."))

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
pau("Discussió de sistemes amb paràmetres",
 (2, r"\pau{Andalusia, ordinària 2026} Considera el sistema \ $\left\{\begin{aligned}3x-y&=a^2\\ (1-a)y+2z&=0\\ 4y+(3-a)z&=a-5\end{aligned}\right.$" + tasks(1, [r"Discuteix-lo segons els valors de $a$.", r"Per a $a=0$, resol el sistema, si és possible."]),
     tasks(1, [r"$|A|=3\big[(1-a)(3-a)-8\big]=3(a^2-4a-5)=3(a-5)(a+1)$. \ Si $a\neq5$ i $a\neq-1$: \rest{SCD}. \ Si $a=-1$: les dues últimes equacions són $2y+2z=0$ i $4y+4z=-6$: \rest{SI}. \ Si $a=5$: són $-4y+2z=0$ i $4y-2z=0$ (proporcionals): \rest{SCI}.",
               r"$3x-y=0$, \ $y+2z=0$, \ $4y+3z=-5$ \ $\Rightarrow$ \ $\res{x=-\tfrac23;\ y=-2;\ z=1}$"])),
 (2, r"\pau{Aragó, extraordinària 2025} Donat el sistema d'equacions lineals \ $\left\{\begin{aligned}x+2y-z&=-1\\ 8x+my-6z&=-8\\ -x-2y+m^2z&=m\end{aligned}\right.$, \ amb $m\in\mathbb{R}$:" + tasks(1, [r"Estudia, en funció de $m$, el nombre de solucions del sistema.", r"Resol, si és possible, el sistema per a $m=1$."]),
     tasks(1, [r"$|A|=m^3-16m^2-m+16=(m-16)(m^2-1)$. \ Si $m\neq16$ i $m\neq\pm1$: \rest{una solució}. \ Si $m=1$: la 3a equació és la 1a canviada de signe: \rest{infinites solucions}. \ Si $m=-1$: la 1a i la 3a diuen $x+2y-z=-1$ i $x+2y-z=1$: \rest{cap solució}. \ Si $m=16$: $\operatorname{rg}(A)=2$ i el menor $" + vm(m16) + '=' + q(det(m16)) + r"\neq0$ de $A^*$ dona $\operatorname{rg}(A^*)=3$: \rest{cap solució}.",
               r"$x+2y-z=-1$, \ $8x+y-6z=-8$. Restant a la 2a el sextuple de la 1a: $2x-11y=-2$. Amb $y=2\lambda$: $x=-1+11\lambda$, $z=x+2y+1=15\lambda$: \ $\res{x=-1+11\lambda;\ y=2\lambda;\ z=15\lambda}$"])),
 (2, r"\pau{Canàries, ordinària 2024} Donat el sistema d'equacions lineals amb un paràmetre $k\in\mathbb{R}$:" + dm(sy(CAN(Sym('k')))) + tasks(1, [r"Discuteix la resolució del sistema segons els valors de $k$.", r"Resol el sistema quan $k=4$."]),
     tasks(1, [r"$|A|=-k^2+2k+3=-(k-3)(k+1)$. \ Si $k\neq3$ i $k\neq-1$: \rest{SCD}. \ Si $k=3$: la 1a i la 3a equacions tenen els mateixos coeficients ($3x+y-3z$) i termes independents diferents: \rest{SI}. \ Si $k=-1$: el mateix passa amb la 2a i la 3a ($-x+y+z$): \rest{SI}.",
               r"Restant la 1a i la 3a: $z=4$; aleshores $4x+y=17$ i $-x+y=-8$: \ $\res{x=5;\ y=-3;\ z=4}$"])),
 (2, r"\pau{Cantàbria, ordinària 2026} Considera el sistema \ $" + sy(CTO(Sym('a'))) + r"$, \ dependent del paràmetre $a\in\mathbb{R}$." + tasks(1, [r"Discuteix el sistema en funció dels valors de $a$.", r"Per a $a=2$, si el sistema és compatible, troba'n la solució general.", r"Per a $a=1$, si el sistema és compatible, troba'n la solució general."]),
     tasks(1, [r"$|A|=1-a^2$. \ Si $a\neq\pm1$: \rest{SCD}. \ Si $a=-1$: les dues últimes són $y-z=1$ i $-y+z=3$: \rest{SI}. \ Si $a=1$: les dues últimes són $y+z=1$: \rest{SCI}.",
               r"$y+2z=1$, \ $2y+z=0$ \ $\Rightarrow$ \ $y=-\tfrac13$, $z=\tfrac23$: \ $\res{x=-\tfrac13;\ y=-\tfrac13;\ z=\tfrac23}$", r"$y+z=1$ i $x=-(y+z)=-1$: \ $\res{x=-1;\ y=1-\lambda;\ z=\lambda}$"])),
 (3, r"\pau{Cantàbria, extraordinària 2026} Considera el sistema \ $\left\{\begin{aligned}a^3x+y+az&=1\\ ax+a^2y&=a\end{aligned}\right.$, \ dependent del paràmetre $a\in\mathbb{R}$." + tasks(1, [r"Discuteix el sistema en funció dels valors de $a$.", r"Per a $a=0$, si el sistema és compatible, troba'n la solució general.", r"Per a $a=2$, si el sistema és compatible, troba'n la solució general."]),
     tasks(1, [r"Si $a\neq0$: el menor $\begin{vmatrix}1 & a\\ a^2 & 0\end{vmatrix}=-a^3\neq0$, i $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2<3$: \rest{SCI}. Si $a=0$: queda $y=1$ i $0=0$: rang 1, \rest{SCI amb dos paràmetres}. És a dir, \rest{SCI per a tot $a$}.",
               r"$\res{x=\lambda;\ y=1;\ z=\mu}$, \ $\lambda,\mu\in\mathbb{R}$.", r"$8x+y+2z=1$, \ $2x+4y=2$. Amb $y=\lambda$: $x=1-2\lambda$, \ $z=\frac{1-8x-y}{2}$: \ $\res{x=1-2\lambda;\ y=\lambda;\ z=-\tfrac72+\tfrac{15}{2}\lambda}$"])),
 (2, r"\pau{Castella-la Manxa, extraordinària 2025} Donat el sistema \ $" + sy(CLM(Sym('a'))) + r"$:" + tasks(1, [r"Discuteix la resolució del sistema segons els valors de $a\in\mathbb{R}$ i indica el nombre de solucions en cada cas.", r"Per a $a=0$, resol el sistema de forma raonada."]),
     tasks(1, [r"$|A|=2a-6$. \ Si $a\neq3$: \rest{SCD} (una solució). \ Si $a=3$: la 2a equació, $4x+2y=3$, és la suma de la 1a i la 3a: \rest{SCI} (infinites solucions).", r"Sumant la 1a i la 3a: $x+2y=3$; amb $4x+2y=0$: $x=-1$, $y=2$, $z=-1$: \ $\res{x=-1;\ y=2;\ z=-1}$"])),
 (3, r"\pau{Castella i Lleó, extraordinària 2026} Siguen \ $A=" + pm(CYA) + r"$ \ i $I$ la matriu identitat d'ordre 3. Discuteix el sistema \ $(A-\alpha I)\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}0\\ 0\\ 1\end{pmatrix}$ \ en funció del paràmetre $\alpha\in\mathbb{R}$.",
     r"$A-\alpha I=\begin{pmatrix}2-\alpha & 2 & 0\\ 0 & 2-\alpha & 0\\ 2 & 0 & 4-\alpha\end{pmatrix}$, \ $|A-\alpha I|=(2-\alpha)^2(4-\alpha)$."
     + tasks(1, [r"Si $\alpha\neq2$ i $\alpha\neq4$: \ \rest{SCD}.", r"Si $\alpha=2$: queda $2y=0$, $0=0$, $2x+2z=1$: rang 2: \ \rest{SCI} \ ($x=\lambda$, $y=0$, $z=\tfrac12-\lambda$).",
                 r"Si $\alpha=4$: la 3a columna de $A$ és nul·la i $\operatorname{rg}(A)=2$, però $" + vm(mn(CYE(F(4)), [0, 1, -1])) + r"=4\neq0$: $\operatorname{rg}(A^*)=3$: \ \rest{SI}."])),
 (2, r"\pau{Castella i Lleó, ordinària 2026} Considera el sistema \ $\left\{\begin{aligned}(m-10)x-2y-z&=-1\\ 7x+(m+2)y+2z&=m+1\\ 5x+2y+z&=1\end{aligned}\right.$, \ amb $m\in\mathbb{R}$." + tasks(1, [r"Discuteix el sistema segons els valors del paràmetre $m$.", r"Resol, raonadament, el sistema per a $m=3$."]),
     tasks(1, [r"$|A|=m^2-7m+10=(m-2)(m-5)$. \ Si $m\neq2$ i $m\neq5$: \rest{SCD}. \ Si $m=5$: la 1a equació és la 3a canviada de signe: \rest{SCI}. \ Si $m=2$: $\begin{vmatrix}-8 & -2\\ 7 & 4\end{vmatrix}\neq0$, $\operatorname{rg}(A)=2$, i $" + vm(m2c) + '=' + q(det(m2c)) + r"\neq0$: $\operatorname{rg}(A^*)=3$, \rest{SI}.",
               r"Sumant la 1a i la 3a: $-2x=0$, $x=0$; aleshores $5y+2z=4$ i $2y+z=1$: \ $\res{x=0;\ y=2;\ z=-3}$"])),
 (2, r"\pau{Catalunya, ordinària 2026} Considera el sistema \ $" + sy(CTO26(Sym('m'))) + r"$, \ que depèn del paràmetre real $m$." + tasks(1, [r"Discuteix el sistema per als diferents valors de $m$.", r"Resol-lo, si és possible, per al cas $m=1$.",
     r"Per a $m=1$, és possible afegir una quarta equació de manera que el sistema resultant siga compatible determinat i tinga com a solució $(x,y,z)=\left(3,\tfrac12,\tfrac12\right)$? Raona la resposta."]),
     tasks(1, [r"$|A|=m^2-4m+3=(m-1)(m-3)$. \ Si $m\neq1$ i $m\neq3$: \rest{SCD}. \ Si $m=1$: la 1a i la 3a equacions coincideixen: \rest{SCI}. \ Si $m=3$: la 1a i la 2a tenen els mateixos coeficients i termes independents 4 i 5: \rest{SI}.",
               r"$x+y+z=4$, $x+3y+z=5$: $y=\tfrac12$: \ $\res{x=\tfrac72-\lambda;\ y=\tfrac12;\ z=\lambda}$", r"Sí: $\left(3,\tfrac12,\tfrac12\right)$ és la solució amb $\lambda=\tfrac12$. N'hi ha prou d'afegir una equació que fixe $\lambda$, per exemple \ $\res{z=\tfrac12}$: aleshores $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3$ i és SCD."])),
 (2, r"\pau{Extremadura, extraordinària 2026} Donat el sistema \ $" + sy(EXE(Sym('k'))) + r"$:" + tasks(1, [r"Discuteix el sistema segons els valors del paràmetre $k$.", r"Resol el sistema per al valor $k=3$."]),
     tasks(1, [r"$|A|=k^2-k-6=(k-3)(k+2)$. \ Si $k\neq3$ i $k\neq-2$: \rest{SCD}. \ Si $k=-2$: $\operatorname{rg}(A)=2$ i $" + vm(mEX) + '=' + q(det(mEX)) + r"\neq0$: \rest{SI}. \ Si $k=3$: la 1a equació és la suma de la 2a i la 3a: \rest{SCI}.",
               r"$2x+3y-2z=6$, \ $x-y+z=3$. Sumant a la 1a el doble de la 2a: $4x+y=12$. Amb $x=3-\lambda$: $y=4\lambda$, \ $z=3-x+y=5\lambda$: \ $\res{x=3-\lambda;\ y=4\lambda;\ z=5\lambda}$"])),
 (2, r"\pau{Extremadura, extraordinària 2025} Es considera el sistema \ $" + sy(EXO(Sym('m'))) + r"$, \ amb $m\in\mathbb{R}$." + tasks(1, [r"Discuteix el sistema en funció del paràmetre $m$.", r"Resol-lo per al cas $m=1$."]),
     tasks(1, [r"$|A|=m^2-m-2=(m-2)(m+1)$. \ Si $m\neq2$ i $m\neq-1$: \rest{SCD}. \ Si $m=2$: la 1a equació és el doble de la 2a més tres vegades la 3a ($0=6-6$): \rest{SCI}. \ Si $m=-1$: $-E_2+6E_3$ té els mateixos coeficients que la 1a equació, $-x+7y+5z$, però terme independent $-15\neq0$: \rest{SI}.",
               r"Restant la 3a a la 2a: $x=5$; aleshores $7y+5z=-5$ i $y+z=-2$: \ $\res{x=5;\ y=\tfrac52;\ z=-\tfrac92}$"])),
 (2, r"\pau{Galícia, extraordinària 2026} Discuteix, segons els valors del paràmetre $m$, el sistema \ $\left\{\begin{aligned}2x+(2m-2)y+(m+6)z&=9\\ x+(m-2)y+3z&=2\\ 2y+(2m+2)z&=m-5\end{aligned}\right.$",
     r"$|A|=-2m-4=-2(m+2)$. \ Si $m\neq-2$: \rest{SCD}. \ Si $m=-2$: restant a la 1a el doble de la 2a s'obté $2y-2z=5$, mentre que la 3a és $2y-2z=-7$: \rest{SI}."),
 (2, r"\pau{Galícia, extraordinària 2025} Discuteix, segons els valors del paràmetre $m$, el sistema \ $\left\{\begin{aligned}x+my+z&=m\\ x+(3-m)z&=2m\\ my+2z&=3m\end{aligned}\right.$",
     r"$|A|=m^2-4m=m(m-4)$. \ Si $m\neq0$ i $m\neq4$: \rest{SCD}. \ Si $m=0$: queda $x+z=0$, $x+3z=0$, $2z=0$: $x=z=0$ i $y$ qualsevol: \rest{SCI}. \ Si $m=4$: restant les dues primeres, $4y+2z=-4$, mentre que la 3a és $4y+2z=12$: \rest{SI}."),
 (2, r"\pau{Madrid, extraordinària 2025} Siga el sistema d'equacions lineals dependent del paràmetre real $k$:" + dm(pm([[Sym('k'), 1, 1], ['k+1', 1, '-k'], [1, 'k+1', 0]]) + r"\begin{pmatrix}x\\ y\\ z\end{pmatrix}-\begin{pmatrix}0\\ k\\ 2k\end{pmatrix}=\begin{pmatrix}0\\ 0\\ 0\end{pmatrix}") + tasks(1, [r"Discuteix el sistema en funció dels valors de $k$.", r"Resol el sistema per a $k=0$."]),
     tasks(1, [r"El sistema és $AX=\begin{pmatrix}0\\ k\\ 2k\end{pmatrix}$, amb $|A|=k^3+2k^2+k=k(k+1)^2$. \ Si $k\neq0$ i $k\neq-1$: \rest{SCD}. \ Si $k=0$: és homogeni amb $\operatorname{rg}(A)=2$: \rest{SCI}. \ Si $k=-1$: la 1a més la 3a dona $y+z=-2$, mentre que la 2a és $y+z=-1$: \rest{SI}.",
               r"$y+z=0$, \ $x+y=0$: \ $\res{x=-\lambda;\ y=\lambda;\ z=-\lambda}$"])),
 (3, r"\pau{Navarra, extraordinària 2026} Estudia el sistema següent, que depèn del paràmetre real $a$, i resol-lo en els casos en què siga compatible indeterminat. Esmenta el resultat teòric emprat i justifica'n l'ús." + dm(r"\left\{\begin{aligned}(a^2-4)x+(a+2)y+2z&=4\\ (4-a^2)x+z&=2\\ (a^2-4)x+(a+2)y+az&=-4\end{aligned}\right."),
     r"Fem servir el \textbf{teorema de Rouché-Frobenius}, que relaciona el tipus de sistema amb els rangs de $A$ i de $A^*$. \ $|A|=(a^2-4)^2=(a-2)^2(a+2)^2$."
     + tasks(1, [r"Si $a\neq\pm2$: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3$: \ \rest{SCD}.", r"Si $a=2$: la 1a i la 3a equacions són $4y+2z=4$ i $4y+2z=-4$: \rest{SI}.",
                 r"Si $a=-2$: les equacions queden $2z=4$, $z=2$, $-2z=-4$: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=1<3$: \rest{SCI}: \ $\res{x=\lambda;\ y=\mu;\ z=2}$"])),
 (3, r"\pau{Navarra, extraordinària 2025} Estudia el sistema següent, que depèn del paràmetre real $m$, i resol-lo en els casos en què siga compatible. Esmenta el resultat teòric emprat i justifica'n l'ús." + dm(r"\left\{\begin{aligned}(m^2-m)x+(m+2)y-z&=1-m^2\\ (m^2-m)x+(2m+1)y&=2\\ (m-m^2)x-(2m+1)y+(m+2)z&=2m+2\end{aligned}\right."),
     r"Teorema de Rouché-Frobenius. Sumant la 2a i la 3a: $(m+2)z=2m+4$. \ $|A|=m(m-1)^2(m+2)$."
     + tasks(1, [r"Si $m\neq0,1,-2$: \rest{SCD}: $z=2$; restant la 1a a la 2a, $(m-1)y+z=1+m^2$, d'on $y=m+1$, i de la 2a s'aïlla $x$: \ $\res{x=\tfrac{1-3m-2m^2}{m(m-1)};\ y=m+1;\ z=2}$",
                 r"Si $m=0$: la columna de $x$ és nul·la, $\operatorname{rg}(A)=2$, i $" + vm(mn(NV5(F(0)), [1, 2, -1])) + r"=-2\neq0$: \rest{SI}.",
                 r"Si $m=1$: $3y-z=0$, $3y=2$, $-3y+3z=4$: \rest{SCI}: \ $\res{x=\lambda;\ y=\tfrac23;\ z=2}$",
                 r"Si $m=-2$: la 3a equació és la 2a canviada de signe: \rest{SCI}: de $6x-z=-3$ i $6x-3y=2$: \ $\res{x=\lambda;\ y=-\tfrac23+2\lambda;\ z=3+6\lambda}$"])),
 (2, r"\pau{País Basc, extraordinària 2025} Siga el sistema d'equacions lineals \ $\left\{\begin{aligned}x+3z&=3+\alpha y\\ z+\alpha x+y-2&=0\\ x+2z-y&=1\end{aligned}\right.$" + tasks(1, [r"Discuteix l'existència de solució segons els valors del paràmetre $\alpha$.", r"Si és possible, resol-lo en el cas $\alpha=0$."]),
     tasks(1, [r"Ordenant: $\left\{\begin{aligned}x-\alpha y+3z&=3\\ \alpha x+y+z&=2\\ x-y+2z&=1\end{aligned}\right.$. \ $|A|=2\alpha^2-4\alpha=2\alpha(\alpha-2)$. \ Si $\alpha\neq0$ i $\alpha\neq2$: \rest{SCD}. \ Si $\alpha=0$: la 1a equació és la suma de les altres dues: \rest{SCI}. \ Si $\alpha=2$: \rest{SI} ($\operatorname{rg}(A)=2$, $\operatorname{rg}(A^*)=3$).",
               r"$y+z=2$, \ $x-y+2z=1$: amb $z=\lambda$: \ $\res{x=3-3\lambda;\ y=2-\lambda;\ z=\lambda}$"])))
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
pau("Problemes de plantejament",
 (2, r"\pau{Aragó, extraordinària 2024} En un laboratori farmacèutic es fabriquen tres medicaments, M$_1$, M$_2$ i M$_3$, a partir de tres principis actius, A$_1$, A$_2$ i A$_3$. Un gram de M$_1$ necessita 10 mg de A$_1$, 10 mg de A$_2$ i 20 mg de A$_3$; un gram de M$_2$, 10, 20 i 30 mg, i un gram de M$_3$, 20, 30 i 50 mg, respectivament. Es disposa de 70 g de A$_1$, 90 g de A$_2$ i 160 g de A$_3$, i es vol gastar-ho tot. És possible? En cas afirmatiu, quines quantitats de cada medicament es poden fabricar?",
     r"$x$, $y$, $z$: grams de M$_1$, M$_2$ i M$_3$. Passant a mg i dividint entre 10:" + pr(AR24) + r"La 3a equació és la suma de les altres dues: \rest{SCI}. Restant les dues primeres, $y+z=2000$; amb $z=\lambda$: \ $\res{x=5000-\lambda;\ y=2000-\lambda;\ z=\lambda}$, \ amb \rest{$0\leq\lambda\leq2000$} perquè les quantitats no siguen negatives. És possible, i de moltes maneres."),
 (2, r"\pau{Astúries, extraordinària 2026} Una empresa de logística transporta mercaderia amb camions xicotets, mitjans i grans, i en fa servir 10 en total. Cada camió xicotet transporta 1 tona; cada mitjà, 2 tones, i cada gran, 3 tones. La càrrega total és de $(m+9)$ tones, amb $m\in\mathbb{R}$. El transport té un cost de 2 unitats per camió xicotet, 3 per camió mitjà i $7-m$ per camió gran, i el cost total és de 22 unitats."
     + tasks(1, [r"Planteja el sistema d'equacions lineals que modelitza la situació.", r"Determina un valor de $m$ per al qual el sistema té infinites solucions i resol-lo.", r"Resol el sistema per a $m=1$. Té sentit aquesta solució?"]),
     tasks(1, [pr(AS6(Sym('m'))), r"$|A|=3-m$: cal \ $\res{m=3}$. Aleshores la 3a equació és la suma de les altres dues: \rest{SCI}:\par $\res{x=8+\lambda;\ y=2-2\lambda;\ z=\lambda}$",
               r"$\res{x=11;\ y=-2;\ z=1}$: \rest{no té sentit}, perquè no hi pot haver un nombre negatiu de camions."])),
 (3, r"\pau{Astúries, ordinària 2026} Un client d'una cafeteria compra 1 café, 2 tes i 2 sucs i paga 11 euros. L'endemà compra 1 café, 3 tes i 3 sucs i paga 16 euros. El tercer dia compra 3 cafés, 3 tes i tots els sucs que puga pagar amb 21 euros exactes (no li han de tornar canvi)."
     + tasks(1, [r"Troba un sistema d'equacions lineals que modelitze el problema de calcular el preu de cada producte en funció del nombre $p$ de sucs que li donen el tercer dia, i discuteix-lo en funció de $p$.",
                 r"El cambrer del tercer dia li diu: «Per eixos diners et donaré dos sucs», i el client respon: «És impossible, el preu està mal calculat». Qui té raó? Justifica la resposta.", r"El cambrer li respon que en realitat té 4 sucs per a donar-li i el client queda satisfet. A quin preu li ha cobrat cada beguda?"]),
     tasks(1, [r"$c$, $t$, $s$: preus del café, el te i el suc: \ " + pr(AS7(Sym('p')), 'cts') + r" \ $|A|=p-3$. Si $p\neq3$: \rest{SCD}; si $p=3$: \rest{SI} (restant les dues primeres, $t+s=5$, i aleshores la 3a donaria $3c=6$ però la 1a, $c=1$).",
               r"Amb $p=2$: \ $c=1$, $t=8$, $s=-3$: un preu negatiu: \rest{té raó el client}.", r"Amb $p=4$: \ \rest{café 1 €, te 2 € i suc 3 €}."])),
 (2, r"\pau{Canàries, extraordinària 2025} Una empresa de pinsos per a peixos utilitza tres matèries primeres: subproductes vegetals (20\,\% de proteïna, 10\,\% de greix i 10\,\% de carbohidrats), farines (40\,\%, 20\,\% i 30\,\%) i subproductes carnis (60\,\%, 10\,\% i 30\,\%). Vol preparar 1000 kg de pinso que continguen un 36\,\% de proteïna, un 12\,\% de greix i un 20\,\% de carbohidrats. Quina quantitat de cada matèria primera ha d'utilitzar?",
     r"$x$, $y$, $z$: kg de cada matèria primera. Hi ha quatre equacions (massa total, proteïna, greix i carbohidrats):" + pr(CN5) + r"$|A^*|=0$ i el menor de les tres primeres files de $A$ és no nul: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3$, \rest{SCD}. Resolent: \ \rest{500 kg de vegetals, 200 kg de farines i 300 kg de carnis}."),
 (2, r"\pau{Castella-la Manxa, extraordinària 2024} Una gelateria ven gelats d'una, dues i tres boles a 1, 2 i 3 euros, respectivament. Divendres va vendre 157 gelats i en va obtenir 278 euros. També sabem que el nombre de gelats d'una bola venuts és $k$ vegades el nombre de gelats de tres boles, amb $k>0$."
     + tasks(1, [r"Planteja un sistema d'equacions lineals que permeta determinar el nombre de gelats venuts de cada tipus.", r"Estudia per a quins valors de $k$ el sistema té solució única. És possible que, en algun d'aquests casos, s'haja venut el mateix nombre de gelats d'una bola que de tres boles?"]),
     tasks(1, [pr(CL4(Sym('k'))), r"$|A|=1-k$: solució única si \ $\res{k\neq1}$ \ ($k>0$). Vendre'n el mateix nombre vol dir $k=1$, i aleshores el sistema és incompatible ($x=z$ dona $2x+y=157$ i $4x+2y=278$, contradictòries): \rest{no és possible}."])),
 (2, r"\pau{Madrid, ordinària 2025} En el bàsquet hi ha cistelles d'un punt, de dos i de tres. Calcula el nombre de llançaments d'un, de dos i de tres punts que va fer un equip en un partit, sabent que: l'equip va anotar 80 punts amb un encert del 80\,\% en els tirs d'un punt, del 50\,\% en els de dos i del 40\,\% en els de tres; la tercera part del nombre de llançaments de dos va ser igual a la cinquena part de la resta de llançaments, i el doble del nombre de llançaments de tres és cinc unitats menor que la resta de llançaments.",
     r"$x$, $y$, $z$: llançaments d'1, 2 i 3 punts: \ $0{,}8x+0{,}5\cdot2y+0{,}4\cdot3z=80$, \ $\frac y3=\frac{x+z}{5}$, \ $2z=x+y-5$:" + pr(MD5) + r"$\Rightarrow$ \ \rest{25 llançaments d'1 punt, 30 de 2 punts i 25 de 3 punts}."),
 (2, r"\pau{Múrcia, extraordinària 2026} Una empresa prepara capses de fruita de tres tipus. Les capses A porten 1 poma, 1 pera i 1 taronja; les B, 2 pomes, 1 pera i 1 taronja, i les C, 1 poma, 2 peres i 1 taronja. Un dia van preparar $x$ capses A, $y$ capses B i $z$ capses C, i van fer servir 400 pomes, 500 peres i $k$ taronges."
     + tasks(1, [r"Planteja un sistema d'equacions per a esbrinar quantes capses de cada tipus van preparar.", r"Discuteix i resol el sistema, donant la solució en funció del paràmetre $k$."]),
     tasks(1, [pr(MR6(Sym('k'))), r"$|A|=" + q(det(coef(MR6(0)))) + r"\neq0$: \rest{SCD per a tot $k$}. Restant la 3a a les altres: $y=400-k$, $z=500-k$, i $x=k-y-z$: \ $\res{x=3k-900;\ y=400-k;\ z=500-k}$. \ Perquè tinga sentit, $k$ ha de ser un nombre natural entre 300 i 400."])),
 (2, r"\pau{Múrcia, ordinària 2026} En Darío i la Cayetana inverteixen $x$ milers d'euros en publicitat, $y$ en materials i $z$ en logística, 12 mil euros en total. En Darío proposa que la inversió en publicitat més el doble de la inversió en materials siga igual a la inversió en logística més $k$, on $k>0$ és un paràmetre d'ajust econòmic. La Cayetana vol que el doble de la inversió en publicitat menys la de materials més la de logística siga 4 mil euros."
     + tasks(1, [r"Planteja un sistema de 3 equacions amb 3 incògnites que reculla les dades del problema.", r"Discuteix el sistema i, si té solució única, troba-la en funció de $k$."]),
     tasks(1, [pr(MR7(Sym('k'))), r"$|A|=-7\neq0$ per a tot $k$: \rest{SCD}. Per Cramer: \ $\res{x=\tfrac{2k}{7};\ y=4+\tfrac{k}{7};\ z=8-\tfrac{3k}{7}}$"])),
 (2, r"\pau{País Basc, extraordinària 2026} Una central lletera recull llet de tres productors. El productor A porta la llet en recipients de 10 litres i cobra 5 € per recipient; el B, en recipients de 15 litres i cobra 9 € per recipient, i el C, en recipients de 12 litres i cobra 4 € per recipient. L'última setmana s'han recollit 612 litres en 48 recipients i s'han de pagar 304 €."
     + tasks(1, [r"Planteja el sistema d'equacions que modelitza la situació.", r"Quant s'ha de pagar a cada productor per la llet que ha portat l'última setmana?"]),
     tasks(1, [r"$a$, $b$, $c$: recipients de cada productor: \ " + pr(PV6, 'abc'), r"Solució: $a=12$, $b=20$, $c=16$: \ \rest{60 € a A, 180 € a B i 64 € a C}."])))

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
KW = "pdfkeywords={sistemes d'equacions lineals, mètode de Gauss, mètode matricial, regla de Cramer, teorema de Rouché-Frobenius, sistemes homogenis, discussió de sistemes, paràmetres, problemes, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre = pre.replace(r'\usepackage{amsmath,amssymb}', r'\usepackage{amsmath,amssymb}' + '\n' + r'\allowdisplaybreaks')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Sistemes d'equacions lineals"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 2: %s. 2n de Batxillerat MII}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 2: %s · 2n Batxillerat MII" % (t, TIT))
    assert 'Unitat 2' in p and 'unitat 2' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques II}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 2' if sol else "Fitxa d'exercicis · Unitat 2") + r'''}{''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Els passos de Gauss poden ser diferents dels teus i ser igualment correctes; el que ha de coincidir és la classificació i la solució (en un SCI, la solució general es pot escriure de maneres diferents segons la incògnita que prengues com a paràmetre). Pots comprovar-ho amb el resolutor de sistemes dels apunts interactius."
             if sol else r"Resol els exercicis al quadern justificant cada pas: indica sempre el mètode que fas servir i, en els problemes, què representa cada incògnita. En les discussions amb paràmetres, estudia \textbf{tots} els casos. Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes (2024--2026), traduïts al valencià.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb el resolutor de sistemes dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't2-fitxa-solucions.tex' if sol else 't2-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'exercicis,', npau, 'de la PAU d\'altres comunitats')
