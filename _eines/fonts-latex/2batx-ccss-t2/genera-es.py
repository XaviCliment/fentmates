# Versió en castellà de genera.py. Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 2: Sistemes d'equacions lineals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les estrelles
# no es mostren. Els exercicis marcats amb \pau{...} són de la PAU d'altres comunitats (exàmens de Matemàtiques
# Aplicades a les CCSS II 2022-2025 recollits a www.ebaumatematicas.com), traduïts al valencià.
# Els sistemes es dibuixen a partir de les seues matrius (sy, amp), els passos de Gauss els calcula gauss() amb
# aritmètica exacta i, al final, CHK comprova totes les solucions, classificacions, determinants i discussions.
# Ús: python3 genera.py && pdflatex t2-fitxa-exercicis.tex (dues vegades) && pdflatex t2-fitxa-solucions.tex
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
    if isinstance(x, str): return x
    x = fr(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\%s{%d}{%d}' % (t, abs(x.numerator), x.denominator)
def dec(x):
    x = fr(x); d = x.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    return ('%g' % float(x)).replace('.', '{,}') if d == 1 else q(x, 'tfrac')
def lhs(cs, v):
    s = ''
    for c, x in zip(cs, v):
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

# =====================================================================
R1 = [[2, -1, 1, 5], [1, 1, -1, -2], [3, 0, 2, 7]]
ck('sol', R1, (1, -1, 2)); ck('no', R1, (2, 1, 2)); ck('no', R1, (0, 1, 3))
R2a, R2b, R2c = [[1, 1, 3], [2, -1, 0]], [[1, -2, 1], [-2, 4, -2]], [[3, 1, 2], [6, 2, 5]]
ck('cls', R2a, 'SCD'); ck('sol', R2a, (1, 2)); ck('cls', R2b, 'SCI'); ck('cls', R2c, 'SI')
B3 = [[1, 1, 1, 3], [2, -1, 1, 2]]
R3a, R3b, R3c = B3 + [[3, 0, 2, 5]], B3 + [[1, 1, 1, 0]], B3 + [[0, 0, 1, 1]]
ck('cls', R3a, 'SCI'); ck('cls', R3b, 'SI'); ck('cls', R3c, 'SCD'); ck('sol', R3c, (1, 1, 1))
R4a = [[1, 1, 1, 6], [2, -1, 3, 9], [1, 2, -1, 2]]
R4b = [[2, 1, -1, 1], [1, -1, 2, 5], [3, 2, 1, 10]]
R5a = [[1, -1, 2, 1], [2, 1, -1, 3], [4, -1, 3, 5]]
R5b = [[1, -1, 2, 1], [2, 1, -1, 3], [4, -1, 3, 6]]
R5c = [[1, -2, 1, 3], [-2, 4, -2, -6], [3, -6, 3, 9]]
ck('sol', R5a, lambda l: (F(4, 3) - F(1, 3) * l, F(1, 3) + F(5, 3) * l, l)); ck('cls', R5a, 'SCI')
ck('sol', R5c, lambda l, u: (3 + 2 * l - u, l, u)); ck('cls', R5c, 'SCI'); ck('rank', R5c, 1)
RNAV = [[1, 1, 3, 1], [4, 3, 5, 5], [2, 1, -1, 3]]
ck('sol', RNAV, lambda l: (2 + 4 * l, -1 - 7 * l, l))
S.append(("Sistemas de ecuaciones lineales. Método de Gauss", [
 (1, r"Comprueba cuáles de las ternas siguientes son solución del sistema \ $" + sy(R1) + r"$" + tasks(3, [r'$(1,-1,2)$', r'$(2,1,2)$', r'$(0,1,3)$'])
     + recorda(r"Una terna $(x,y,z)$ es solución si, al sustituirla, se cumplen \textbf{todas} las ecuaciones a la vez."),
     tasks(3, [r"$5=5$, \ $-2=-2$, \ $7=7$: \rest{sí}", r"La 2.\textsuperscript{a}: $2+1-2=1\neq-2$: \rest{no}", r"La 1.\textsuperscript{a}: $0-1+3=2\neq5$: \rest{no}"])),
 (1, r"Clasifica los sistemas siguientes e interprétalos geométricamente (cada ecuación es una recta del plano):" + tasks(3, [m(sy(R2a, 'xy')), m(sy(R2b, 'xy')), m(sy(R2c, 'xy'))])
     + recorda(r"SCD: las rectas se cortan en un punto. \ SCI: son la misma recta. \ SI: son paralelas."),
     tasks(1, [r"Sumando: $3x=3$, $x=1$, $y=2$. \rest{SCD}: rectas secantes en $(1,2)$.", r"La 2.\textsuperscript{a} es la 1.\textsuperscript{a} por $-2$: \rest{SCI}, la misma recta: $x=1+2\lambda,\ y=\lambda$.",
               r"La 1.\textsuperscript{a} por 2 da $6x+2y=4\neq5$: \rest{SI}, rectas paralelas."])),
 (2, r"Añade una ecuación al sistema \ $" + sy(B3) + r"$ \ de manera que el sistema resultante sea:" + tasks(3, ['compatible indeterminado', 'incompatible', 'compatible determinado'])
     + recorda(r"Una ecuación que es combinación lineal de las otras no aporta información; una con los mismos coeficientes y otro término independiente las contradice."),
     r"Hay muchas respuestas posibles; por ejemplo:" + tasks(1, [r"La suma de las dos: \ $\res{3x+2z=5}$ \ (SCI).", r"Mismos coeficientes que la 1.\textsuperscript{a} y otro término independiente: \ $\res{x+y+z=0}$ \ (SI).",
               r"\ $\res{z=1}$: \ queda $x+y=2,\ 2x-y=1$, \ de donde $x=1,\ y=1,\ z=1$ (SCD)."])),
 (1, r"Resuelve por el método de Gauss:" + tasks(2, [m(sy(R4a)), m(sy(R4b))])
     + recorda(r"Haz ceros por debajo de la diagonal con operaciones entre filas de la matriz ampliada y después resuelve de abajo arriba."),
     tasks(1, [G(R4a, (1, 2, 3), 'SCD') + r"$-5z=-15\Rightarrow z=3$; \ $y-6=-4\Rightarrow y=2$; \ $x=6-2-3$: \ $\res{x=1;\ y=2;\ z=3}$",
               G(R4b, (1, 2, 3), 'SCD') + r"$10z=30\Rightarrow z=3$; \ $3y-15=-9\Rightarrow y=2$; \ $x=5+2-6$: \ $\res{x=1;\ y=2;\ z=3}$"])),
 (2, r"Discute y resuelve, cuando sea posible, por el método de Gauss:" + tasks(3, [m(sy(R5a)), m(sy(R5b)), m(sy(R5c))])
     + recorda(r"Una fila $(0\ 0\ 0\,|\,0)$ se puede suprimir; una fila $(0\ 0\ 0\,|\,d)$ con $d\neq0$ quiere decir que el sistema es incompatible. En un SCI hay tantos parámetros como incógnitas \emph{sobran}."),
     tasks(1, [G(R5a) + r"\rest{SCI}. Hacemos $z=\lambda$: $3y=1+5\lambda$, \ $x=1+y-2\lambda$: \ $\res{x=\tfrac{4-\lambda}{3};\ y=\tfrac{1+5\lambda}{3};\ z=\lambda}$",
               G(R5b, cls='SI') + r"La última fila dice $0=1$: \ \rest{SI}, no tiene solución.",
               r"La 2.\textsuperscript{a} y la 3.\textsuperscript{a} ecuaciones son la 1.\textsuperscript{a} multiplicada por $-2$ y por $3$: solo queda $x-2y+z=3$ (rango 1). \rest{SCI con dos parámetros}: \ $\res{x=3+2\lambda-\mu;\ y=\lambda;\ z=\mu}$"])),
 (2, r"\pau{Navarra, EvAU extraordinaria 2023} Clasifica el sistema siguiente en función del número de soluciones y resuélvelo utilizando el método de Gauss:" + dm(sy(RNAV)),
     G(RNAV, cls='SCI') + r"Queda una fila de ceros: \rest{SCI}. Con $z=\lambda$: \ $-y-7\lambda=1\Rightarrow y=-1-7\lambda$; \ $x=1-y-3\lambda=2+4\lambda$." + dm(r'\boxed{x=2+4\lambda;\ \ y=-1-7\lambda;\ \ z=\lambda,\quad\lambda\in\mathbb{R}}')),
]))

# =====================================================================
R7a = [[2, 0, -1, 1], [1, 1, 0, 0], [0, 1, 1, 2]]
ck('det', coef(R7a), 1); ck('sol', R7a, (3, -3, 5)); assert mult(inv(coef(R7a)), [1, 0, 2]) == [3, -3, 5]
M7b, B7b = [[1, 2, 0], [-1, 0, 3]], [4, 1]
R7b = [r + [b] for r, b in zip(M7b, B7b)]
ck('cls', R7b, 'SCI'); ck('sol', R7b, lambda l: (-1 + 3 * l, (5 - 3 * l) / 2, l))
A8a, B8a = [[3, 2], [1, 1]], [7, 3]
A8b, B8b = [[1, 0, 1], [1, 1, 0], [0, 1, 1]], [3, 3, 4]
INV8a, INV8b = [[1, -2], [-1, 3]], [[F(1, 2), F(1, 2), F(-1, 2)], [F(-1, 2), F(1, 2), F(1, 2)], [F(1, 2), F(-1, 2), F(1, 2)]]
ck('inv', A8a, INV8a); ck('inv', A8b, INV8b); ck('det', A8b, 2)
ck('sol', [r + [b] for r, b in zip(A8a, B8a)], (1, 2)); ck('sol', [r + [b] for r, b in zip(A8b, B8b)], (1, 2, 2))
RGAL = [[2, 1, 1, 2], [0, 2, -1, -1], [1, 1, 0, 1]]
INVG = inv(coef(RGAL))
ck('det', coef(RGAL), -1); ck('inv', coef(RGAL), INVG); ck('sol', RGAL, (2, -1, -1))
RPV = [[3, -2, -2, 3], [1, 0, -1, 1], [0, 2, -1, 0]]
ck('det', coef(RPV), 0); ck('cls', RPV, 'SCI'); ck('sol', RPV, lambda l: (1 + l, l / 2, l))
A11 = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
INV11 = [[F(1, 2), F(-1, 2), F(1, 2)], [F(1, 2), F(1, 2), F(-1, 2)], [F(-1, 2), F(1, 2), F(1, 2)]]
ck('inv', A11, INV11); ck('sol', [r + [b] for r, b in zip(A11, [1, 2, 3])], (1, 0, 2))
for k in range(-5, 6): ck('det', [[1, k, 0], [0, 1, 1], [k, 0, 1]], 1 + k * k)
S.append(("Expresión matricial. Método matricial", [
 (2, r"Escribe en forma matricial $A\cdot X=B$ y resuélvelo utilizando la inversa de la matriz $A$:" + dm(sy(R7a))
     + recorda(r"Si $|A|\neq0$: \ $A\cdot X=B\Rightarrow X=A^{-1}\cdot B$, \ con $A^{-1}=\dfrac{1}{|A|}\big(\mathrm{Adj}(A)\big)^t$. Multiplicamos por $A^{-1}$ por la \textbf{izquierda}. Cuidado con las incógnitas que no aparecen: su coeficiente es 0."),
     dm(pm(coef(R7a)) + r'\cdot\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}1\\ 0\\ 2\end{pmatrix}')
     + r"$|A|=" + vm(coef(R7a)) + r"=1\neq0$, por tanto $A$ tiene inversa:" + dm(r'\mathrm{Adj}(A)=' + pm(adjm(coef(R7a))) + r',\qquad A^{-1}=\frac{1}{1}\big(\mathrm{Adj}(A)\big)^t=' + pm(inv(coef(R7a))))
     + dm(r'X=A^{-1}\cdot B=' + pm(inv(coef(R7a))) + r'\begin{pmatrix}1\\ 0\\ 2\end{pmatrix}=\begin{pmatrix}3\\ -3\\ 5\end{pmatrix}\ \Rightarrow\ \boxed{x=3;\ y=-3;\ z=5}')),
 (1, r"Escribe el sistema de ecuaciones que corresponde a la ecuación matricial \ $" + pm(M7b) + r"\cdot\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}4\\ 1\end{pmatrix}$. \ ¿Cuántas ecuaciones y cuántas incógnitas tiene? ¿De qué tipo de sistema se puede tratar (SCD, SCI o SI)? Justifica la respuesta.",
     r"$\res{" + sy([r + [b] for r, b in zip(M7b, B7b)]) + r"}$ \ \ Tiene \rest{2 ecuaciones y 3 incógnitas} (el producto de una matriz $2\times3$ por una $3\times1$ es $2\times1$).\par No puede ser SCD: con 2 ecuaciones y 3 incógnitas, al escalonar siempre sobra al menos una incógnita. Las filas de $A$ no son proporcionales y, con $F_2'=F_2+F_1$, queda $2y+3z=5$: no aparece ninguna fila del tipo $0=d\neq0$. Por tanto, es \rest{SCI}, con un parámetro: \ $x=-1+3\lambda;\ y=\tfrac{5-3\lambda}{2};\ z=\lambda$."),
 (2, r"Resuelve por el método matricial (con la matriz inversa):" + tasks(2, [m(sy([r + [b] for r, b in zip(A8a, B8a)], 'xy')), m(sy([r + [b] for r, b in zip(A8b, B8b)]))]),
     tasks(1, [r"$|A|=1$, \ $A^{-1}=" + pm(INV8a) + r"$, \ $X=" + pm(INV8a) + r"\begin{pmatrix}7\\ 3\end{pmatrix}=\begin{pmatrix}1\\ 2\end{pmatrix}$: \ $\res{x=1;\ y=2}$",
               r"$|A|=2$, \ $A^{-1}=\frac12" + pm([[1, 1, -1], [-1, 1, 1], [1, -1, 1]]) + r"$, \ $X=\frac12" + pm([[1, 1, -1], [-1, 1, 1], [1, -1, 1]]) + r"\begin{pmatrix}3\\ 3\\ 4\end{pmatrix}=\frac12\begin{pmatrix}2\\ 4\\ 4\end{pmatrix}$: \ $\res{x=1;\ y=2;\ z=2}$"])),
 (2, r"\pau{Galicia, ABAU extraordinaria 2023} Expresa en forma matricial el sistema de ecuaciones siguiente y resuélvelo:" + dm(sy(RGAL)),
     dm(pm(coef(RGAL)) + r'\cdot\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}2\\ -1\\ 1\end{pmatrix}')
     + r"$|A|=-1\neq0$, por tanto $A$ tiene inversa:" + dm(r'\mathrm{Adj}(A)=' + pm(adjm(coef(RGAL))) + r',\qquad A^{-1}=\frac{1}{-1}\big(\mathrm{Adj}(A)\big)^t=' + pm(INVG))
     + dm(r'X=A^{-1}\cdot B=' + pm(INVG) + r'\begin{pmatrix}2\\ -1\\ 1\end{pmatrix}=\begin{pmatrix}2\\ -1\\ -1\end{pmatrix}\ \Rightarrow\ \boxed{x=2;\ y=-1;\ z=-1}')),
 (2, r"\pau{País Vasco, PAU extraordinaria 2025} Considera el sistema de ecuaciones lineales" + dm(sy(RPV)) + tasks(1, ["Exprésalo mediante una ecuación matricial.", "¿La matriz de los coeficientes tiene inversa? Razona la respuesta.", "Resuelve el sistema de ecuaciones lineales."]),
     tasks(1, [r"$" + pm(coef(RPV)) + r"\cdot\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}3\\ 1\\ 0\end{pmatrix}$",
               r"$|A|=3\cdot2+(-2)\cdot1+(-2)\cdot2=6-2-4=0$: \ \rest{no tiene inversa} y no podemos aplicar el método matricial.",
               G(RPV) + r"\rest{SCI}. Con $z=\lambda$: \ $2y=\lambda$, \ $x=1+z$: \ $\res{x=1+\lambda;\ y=\tfrac{\lambda}{2};\ z=\lambda,\ \ \lambda\in\mathbb{R}}$"])),
 (3, r"Considera el sistema \ $\left\{\begin{aligned}x+ky&=1\\ y+z&=2\\ kx+z&=3\end{aligned}\right.$" + tasks(1, [r"Comprueba que se puede resolver por el método matricial para cualquier valor de $k$.", r"Resuélvelo por el método matricial para $k=1$."]),
     tasks(1, [r"$|A|=" + vm([[1, 'k', 0], [0, 1, 1], ['k', 0, 1]]) + r"=1+k^2>0$ para todo $k$: \ $A$ \rest{siempre es invertible}.",
               r"$|A|=2$, \ $A^{-1}=\frac12" + pm([[1, -1, 1], [1, 1, -1], [-1, 1, 1]]) + r"$, \ $X=\frac12" + pm([[1, -1, 1], [1, 1, -1], [-1, 1, 1]]) + r"\begin{pmatrix}1\\ 2\\ 3\end{pmatrix}=\frac12\begin{pmatrix}2\\ 0\\ 4\end{pmatrix}$: \ $\res{x=1;\ y=0;\ z=2}$"])),
]))

# =====================================================================
R12a = [[2, -3, -4], [5, 1, 7]]
R12b = [[1, 1, 1, 2], [2, -1, 1, 5], [1, 2, -1, -3]]
ck('sol', R12a, (1, 2)); ck('det', coef(R12a), 17); ck('det', [[-4, -3], [7, 1]], 17); ck('det', [[2, -4], [5, 7]], 34)
ck('sol', R12b, (1, -1, 2)); ck('det', coef(R12b), 7)
assert cramer(R12b) == (7, [7, -7, 14])
RCYL = [[1, 2, 1, 1], [1, -2, 2, 4], [3, 1, -2, 5]]
ck('det', coef(RCYL), 25); ck('sol', RCYL, (F(52, 25), -F(17, 25), F(7, 25)))
DCYL, DSCYL = cramer(RCYL); assert DSCYL == [52, -17, 7]
R14 = [[1, 2, -1, 3], [2, -1, 3, 1]]
ck('sol', R14, lambda l: (1 - l, 1 + l, l)); ck('cls', R14, 'SCI')
R15 = [[1, -1, 2, 0], [3, 1, -1, 2], [2, 3, 1, 4]]
ck('det', coef(R15), 23); ck('sol', R15, (F(10, 23), F(22, 23), F(6, 23))); assert cramer(R15) == (23, [10, 22, 6])
S.append(("Regla de Cramer", [
 (1, r"Resuelve aplicando la regla de Cramer:" + tasks(2, [m(sy(R12a, 'xy')), m(sy(R12b))])
     + recorda(r"Si el sistema es cuadrado y $|A|\neq0$, cada incógnita es un cociente de determinantes: en el numerador, la columna de la incógnita se sustituye por la de los términos independientes."),
     tasks(1, [r"$|A|=" + vm(coef(R12a)) + r"=17$: \ $x=\dfrac{" + vm([[-4, -3], [7, 1]]) + r"}{17}=\dfrac{17}{17}$, \ $y=\dfrac{" + vm([[2, -4], [5, 7]]) + r"}{17}=\dfrac{34}{17}$: \ $\res{x=1;\ y=2}$",
               r"$|A|=7$, \ $|A_x|=7$, \ $|A_y|=-7$, \ $|A_z|=14$: \ $\res{x=1;\ y=-1;\ z=2}$"])),
 (2, r"\pau{Castilla y León, PAU ordinaria 2025} Dado el sistema \ $\left\{\begin{aligned}ax+2y+z&=1\\ x+by+2z&=4\\ 3x+y+bz&=5\end{aligned}\right.$, \ resuélvelo para $a=1$ y $b=-2$.",
     r"Queda $" + sy(RCYL) + r"$, con $|A|=" + vm(coef(RCYL)) + r"=25\neq0$: es de Cramer."
     + dm(r'x=\frac{' + vm(subcol(RCYL, 0)) + r'}{25}=\frac{52}{25},\quad y=\frac{' + vm(subcol(RCYL, 1)) + r'}{25}=\frac{-17}{25},\quad z=\frac{' + vm(subcol(RCYL, 2)) + r'}{25}=\frac{7}{25}')
     + dm(r'\boxed{x=\tfrac{52}{25};\ \ y=-\tfrac{17}{25};\ \ z=\tfrac{7}{25}}')),
 (2, r"Justifica que el sistema siguiente es de Cramer y calcula, \textbf{solo}, el valor de $z$. Comprueba después el resultado calculando también $x$ e $y$." + dm(sy(R15)),
     r"$|A|=" + vm(coef(R15)) + r"=23\neq0$. \ $z=\dfrac{" + vm(subcol(R15, 2)) + r"}{23}=\res{\dfrac{6}{23}}$; \ $x=\dfrac{10}{23}$, \ $y=\dfrac{22}{23}$ (y se comprueba en las tres ecuaciones)."),
 (3, r"Resuelve aplicando la regla de Cramer el sistema compatible indeterminado \ $" + sy(R14) + r"$ \ (pasa $z$ al segundo miembro).",
     r"$\begin{vmatrix}1&2\\ 2&-1\end{vmatrix}=-5\neq0$: \ $\left\{\begin{aligned}x+2y&=3+z\\ 2x-y&=1-3z\end{aligned}\right.$" + dm(r'x=\frac{\begin{vmatrix}3+z&2\\ 1-3z&-1\end{vmatrix}}{-5}=\frac{-5+5z}{-5}=1-z,\qquad y=\frac{\begin{vmatrix}1&3+z\\ 2&1-3z\end{vmatrix}}{-5}=\frac{-5-5z}{-5}=1+z')
     + dm(r'\boxed{x=1-\lambda;\ \ y=1+\lambda;\ \ z=\lambda,\quad\lambda\in\mathbb{R}}')),
]))

# =====================================================================
R20a = [[1, 2, -1, 0], [2, -1, 1, 0], [3, 1, 1, 0]]
R20b = [[1, -1, 1, 0], [2, 1, -1, 0], [1, 2, -2, 0]]
ck('det', coef(R20a), -5); ck('cls', R20a, 'SCD'); ck('det', coef(R20b), 0); ck('cls', R20b, 'SCI'); ck('sol', R20b, lambda l: (0, l, l))
R21 = [[1, 1, -2, 0], [3, -1, 0, 0], [-1, 3, -4, 0]]
ck('det', coef(R21), 0); ck('cls', R21, 'SCI'); ck('sol', R21, lambda l: (l, 3 * l, 2 * l)); ck('sol', R21, (2, 6, 4))
R22 = [[2, -1, 1, 0], [1, 3, -2, 0]]
ck('sol', R22, lambda l: (-l, 5 * l, 7 * l)); ck('cls', R22, 'SCI')
S.append(("Sistemas homogéneos", [
 (1, r"Clasifica y resuelve los sistemas homogéneos siguientes:" + tasks(2, [m(sy(R20a)), m(sy(R20b))])
     + recorda(r"Un sistema homogéneo siempre es compatible (tiene la solución trivial $x=y=z=0$). Tiene más soluciones si y solo si $\operatorname{rg}(A)<n$; si es cuadrado, cuando $|A|=0$."),
     tasks(1, [r"$|A|=" + vm(coef(R20a)) + r"=-5\neq0$: \ \rest{SCD}, solo la solución trivial \ $\res{x=y=z=0}$.",
               r"$|A|=0$ y $\begin{vmatrix}1&-1\\ 2&1\end{vmatrix}=3\neq0$: \ $\operatorname{rg}(A)=2<3$, \ \rest{SCI}. Sumando las dos primeras, $3x=0$; y de la 1.\textsuperscript{a}, $y=z$: \ $\res{x=0;\ y=\lambda;\ z=\lambda}$"])),
 (2, r"Considera el sistema homogéneo \ $" + sy(R21) + r"$" + tasks(1, ["Razona, sin resolverlo, si tiene soluciones distintas de la trivial.", "Resuélvelo por el método de Gauss.", r"Halla la solución que cumple $x+y+z=12$."]),
     tasks(1, [r"$|A|=" + vm(coef(R21)) + r"=0\Rightarrow\operatorname{rg}(A)<3$: \ \rest{SCI}, tiene infinitas soluciones además de la trivial.",
               G(R21) + r"Con $z=2\lambda$: \ $-4y+12\lambda=0\Rightarrow y=3\lambda$; \ $x=-y+2z=\lambda$: \ $\res{x=\lambda;\ y=3\lambda;\ z=2\lambda,\ \ \lambda\in\mathbb{R}}$",
               r"$\lambda+3\lambda+2\lambda=6\lambda=12\Rightarrow\lambda=2$: \ $\res{x=2;\ y=6;\ z=4}$"])),
 (1, r"¿Por qué el sistema \ $" + sy(R22) + r"$ \ tiene infinitas soluciones sin calcular ningún determinante? Resuélvelo.",
     r"Es homogéneo (compatible) y $\operatorname{rg}(A)\leq2<3$ incógnitas: \rest{SCI}. Pasando $z$ al segundo miembro: $2x-y=-z$, $x+3y=2z$ \ $\Rightarrow x=-\frac z7,\ y=\frac{5z}{7}$. Con $z=7\lambda$: \ $\res{x=-\lambda;\ y=5\lambda;\ z=7\lambda}$"),
]))

# =====================================================================
R16a = [[1, 2, 5], [3, -1, 1], [2, 1, 4]]
R16b = [[1, 2, 5], [3, -1, 1], [1, 1, 2]]
R16c = [[1, 1, -1, 2], [2, -1, 1, 1], [5, -1, 1, 4]]
ck('cls', R16a, 'SCD'); ck('sol', R16a, (1, 2)); ck('cls', R16b, 'SI'); ck('cls', R16c, 'SCI')
ck('det', R16a, 0); ck('det', R16b, 7); ck('det', coef(R16c), 0)
for M in ([[1, 1, 2], [2, -1, 1], [5, -1, 4]], [[1, -1, 2], [2, 1, 1], [5, 1, 4]]): ck('det', M, 0)
ck('sol', R16c, lambda l: (1, 1 + l, l))
RMU = [[3, 2, -1, 3], [1, -1, 2, 4], [2, 3, -1, 3]]
ck('det', coef(RMU), -10); ck('sol', RMU, (1, 1, 2))
R18 = [[1, 1, 1, 3], [1, -1, 1, 1], [2, 1, -1, 2], [3, 1, 1, 5]]
ck('det', R18, 0); ck('det', [r[:3] for r in R18[:3]], 6); ck('cls', R18, 'SCD'); ck('sol', R18, (1, 1, 1))
S.append(("Teorema de Rouché-Frobenius", [
 (1, r"Clasifica los sistemas siguientes aplicando el teorema de Rouché-Frobenius (no hace falta resolverlos):" + tasks(3, [m(sy(R16a, 'xy')), m(sy(R16b, 'xy')), m(sy(R16c))])
     + recorda(r"$\operatorname{rg}(A)\neq\operatorname{rg}(A^*)$: SI. \ $\operatorname{rg}(A)=\operatorname{rg}(A^*)=n$: SCD. \ $\operatorname{rg}(A)=\operatorname{rg}(A^*)<n$: SCI ($n$ = número de incógnitas)."),
     tasks(1, [r"$\begin{vmatrix}1&2\\ 3&-1\end{vmatrix}=-7\neq0\Rightarrow\operatorname{rg}(A)=2$; \ $|A^*|=" + vm(R16a) + r"=0\Rightarrow\operatorname{rg}(A^*)=2=n$: \ \rest{SCD} (la solución es $x=1,\ y=2$).",
               r"$\operatorname{rg}(A)=2$; \ $|A^*|=" + vm(R16b) + r"=7\neq0\Rightarrow\operatorname{rg}(A^*)=3$: \ \rest{SI}.",
               r"$|A|=0$ y $\begin{vmatrix}1&1\\ 2&-1\end{vmatrix}=-3\neq0\Rightarrow\operatorname{rg}(A)=2$. Los menores de orden 3 de $A^*$ con la columna de términos independientes también valen 0 $\Rightarrow\operatorname{rg}(A^*)=2<3$: \ \rest{SCI} (la 3.\textsuperscript{a} ecuación es la 1.\textsuperscript{a} más el doble de la 2.\textsuperscript{a})."])),
 (2, r"\pau{Murcia, PAU ordinaria 2025} Discute y resuelve, si es posible, el sistema lineal siguiente:" + dm(sy(RMU)),
     r"$|A|=" + vm(coef(RMU)) + r"=-10\neq0\Rightarrow\operatorname{rg}(A)=\operatorname{rg}(A^*)=3=n$: \ \rest{SCD}. Por Cramer o por Gauss: \ $\res{x=1;\ y=1;\ z=2}$"),
 (2, r"Clasifica el sistema siguiente y, si es compatible, resuélvelo:" + dm(sy(R18)),
     r"$" + vm([r[:3] for r in R18[:3]]) + r"=6\neq0\Rightarrow\operatorname{rg}(A)=3$; \ $|A^*|=0\Rightarrow\operatorname{rg}(A^*)=3=n$: \ \rest{SCD}. Suprimimos la 4.\textsuperscript{a} ecuación (no forma parte del menor) y resolvemos las tres primeras: \ $\res{x=1;\ y=1;\ z=1}$"),
 (2, r"Razona si son verdaderas o falsas las afirmaciones siguientes:" + tasks(1, [r"Un sistema de 3 ecuaciones y 2 incógnitas no puede ser compatible determinado.",
                r"Si un sistema de 3 ecuaciones y 3 incógnitas tiene $|A|\neq0$, siempre es compatible determinado.",
                r"Si $\operatorname{rg}(A)=2$ y $\operatorname{rg}(A^*)=3$, el sistema tiene dos soluciones.",
                r"Un sistema de 2 ecuaciones y 3 incógnitas puede ser compatible determinado."]),
     tasks(1, [r"\rest{Falsa}: si $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$ es SCD (como en el primer apartado del ejercicio \ref{ex:rf}).",
               r"\rest{Verdadera}: $\operatorname{rg}(A)=3$ y $\operatorname{rg}(A^*)$ no puede pasar de 3 (tiene 3 filas): $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3=n$.",
               r"\rest{Falsa}: los rangos son distintos y el sistema es incompatible (ninguna solución).",
               r"\rest{Falsa}: $\operatorname{rg}(A)\leq2<3$, así que, si es compatible, es indeterminado."])),
]))
S[-1][1][0] = (S[-1][1][0][0], r"\label{ex:rf}" + S[-1][1][0][1], S[-1][1][0][2])

# =====================================================================
def par(fun, crit, test, name):
    """fun(a) -> matriu ampliada; crit: {valor: classificació}; per a la resta de valors de test, SCD."""
    for v, c in crit.items(): ck('cls', fun(F(v)), c)
    for v in test:
        if v not in crit: ck('cls', fun(F(v)), 'SCD')
    return name
AST25 = lambda m: [[1, -1, -m], [10, 10 + m, 150]]
par(AST25, {-20: 'SI'}, range(-25, 5), 'ast25')
ck('cls', [[1, -1, 15], [10, -10, 150]], 'SCI'); ck('sol', [[1, -1, 15], [10, -10, 150]], (15, 0))
def AST24(m):
    A = [[2, 1], [-1, m]]; B = [[1, m], [-1, 1]]; C = [[0, 2 * m], [-2 * m, -1]]
    AB = [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    N = [[AB[i][j] - C[i][j] for j in range(2)] for i in range(2)]
    return [N[0] + [1], N[1] + [1]]
assert AST24(F(5)) == [[1, 1, 1], [4, 1, 1]]
par(AST24, {2: 'SCI'}, range(-4, 6), 'ast24'); ck('sol', AST24(F(-1)), (0, 1))
MAD22 = lambda a: [[1, a, 1, 2], [1, 0, -a, 0], [1, 1, 1, 2]]
par(MAD22, {1: 'SCI', -1: 'SI'}, range(-3, 4), 'mad22'); ck('sol', MAD22(F(0)), (0, 0, 2))
for a in range(-3, 4): ck('det', coef(MAD22(a)), 1 - a * a)
ck('sol', MAD22(F(1)), lambda l: (l, 2 - 2 * l, l)); ck('det', [[1, -1, 2], [1, 0, 0], [1, 1, 2]], 4)
MAD24E = lambda a: [[2, 1, 3, 2], [3, 1, 1, 0], [8, a, 5, 2]]
par(MAD24E, {3: 'SCI'}, range(-3, 6), 'mad24e'); ck('sol', MAD24E(F(3)), lambda l: (-2 + 2 * l, 6 - 7 * l, l))
for a in range(-3, 6): ck('det', coef(MAD24E(a)), 7 * a - 21)
ck('det', [[2, 1, 2], [3, 1, 0], [8, 3, 2]], 0); ck('det', [[2, 3, 2], [3, 1, 0], [8, 5, 2]], 0); ck('det', [[1, 3, 2], [1, 1, 0], [3, 5, 2]], 0)
MAD24O = lambda a: [[2, 1, 1, a], [1, a, 1, a + 1], [1, 1, a, 2]]
par(MAD24O, {0: 'SI', 1: 'SCI'}, range(-3, 4), 'mad24o'); ck('sol', MAD24O(F(1)), lambda l: (-1, 3 - l, l))
for a in range(-3, 4): ck('det', coef(MAD24O(a)), 2 * a * a - 2 * a)
ck('det', [[2, 1, 0], [1, 0, 1], [1, 1, 2]], -3)
MAD25 = lambda a: [[1, 1, 1, 2], [2, -1, 1, 3], [a + 1, 0, a, 5]]
par(MAD25, {2: 'SCI'}, range(-3, 5), 'mad25'); ck('sol', MAD25(F(2)), lambda l: ((5 - 2 * l) / 3, (1 - l) / 3, l))
for a in range(-3, 5): ck('det', coef(MAD25(a)), 2 - a)
MUR25 = lambda a: [[1, -1, 1, 1], [2, -1, 1, a], [3, 2, -a, 4]]
par(MUR25, {2: 'SI'}, range(-3, 5), 'mur25'); ck('sol', MUR25(F(1)), (0, 5, 6))
for a in range(-3, 5): ck('det', coef(MUR25(a)), 2 - a)
ck('det', [[1, -1, 1], [2, -1, 2], [3, 2, 4]], 1)
MUR23 = lambda a: [[a, 1, 1, 1], [2, 1, 1, 1], [1, a, 1, 2]]
par(MUR23, {1: 'SI', 2: 'SCI'}, range(-3, 5), 'mur23'); ck('sol', MUR23(F(0)), (0, -1, 2))
for a in range(-3, 5): ck('det', coef(MUR23(a)), -a * a + 3 * a - 2)
ck('sol', MUR23(F(2)), lambda l: (-l / 3, 1 - l / 3, l))
MAD23 = lambda a: [[a, 1, 2, 1], [1, a, 2, a], [1, 2, a, 1]]
par(MAD23, {1: 'SCI', 2: 'SI', -3: 'SI'}, range(-4, 5), 'mad23'); ck('sol', MAD23(F(0)), (-F(1, 3), F(2, 3), F(1, 6)))
for a in range(-4, 5): ck('det', coef(MAD23(a)), (a - 1) * (a - 2) * (a + 3))
ck('det', [[-3, 1, 1], [1, -3, -3], [1, 2, 1]], -8); ck('sol', MAD23(F(1)), lambda l: (1 - 3 * l, l, l))
CYL = lambda a, b: [[a, 2, 1, 1], [1, b, 2, 4], [3, 1, b, 5]]
for a in range(-5, 25):
    for b in range(-6, 7): ck('det', coef(CYL(a, b)), a * b * b - 2 * a - 5 * b + 13)
par(lambda a: CYL(a, -1), {18: 'SI'}, range(10, 25), 'cyl1'); par(lambda b: CYL(3, b), {}, range(-6, 7), 'cyl2')
ck('det', [[2, 1, 1], [-1, 2, 4], [1, -1, 5]], 36)
HOMK = lambda k: [[1, 1, -1, 0], [2, -1, k, 0], [1, 2, 1, 0]]
par(HOMK, {-8: 'SCI'}, range(-10, 4), 'homk'); ck('sol', HOMK(F(-8)), lambda l: (3 * l, -2 * l, l))
for k in range(-10, 4): ck('det', coef(HOMK(k)), -k - 8)
S.append(("Discusión de sistemas con parámetros", [
 (2, r"\pau{Asturias, PAU extraordinaria 2025} Dado el sistema de ecuaciones \ $\left\{\begin{aligned}x-y&=-m\\ 10x+(10+m)y&=150\end{aligned}\right.$, \ con incógnitas $x$ e $y$:" + tasks(1, [r"¿Para qué valores del parámetro $m$ tiene el sistema una única solución?",
         r"Si el sistema fuera \ $\left\{\begin{aligned}x-y&=-\lambda\\ 10x+(10+m)y&=150\end{aligned}\right.$, \ halla el valor de $m$ y un valor de $\lambda$ para los que el sistema tenga infinitas soluciones, y calcula una de ellas."])
     + recorda(r"Calcula $|A|$ y busca los valores que lo anulan (valores críticos); estudia cada valor crítico por separado con Rouché-Frobenius."),
     tasks(1, [r"$|A|=\begin{vmatrix}1&-1\\ 10&10+m\end{vmatrix}=20+m$. \ Tiene solución única (SCD) si y solo si \ $\res{m\neq-20}$. (Para $m=-20$: $x-y=20$ y $x-y=15$, SI.)",
               r"Debe ser $|A|=0$: $\res{m=-20}$; entonces la 2.\textsuperscript{a} ecuación es $x-y=15$ y, para que coincida con la 1.\textsuperscript{a}, $\res{\lambda=-15}$. Una solución: $\res{x=15,\ y=0}$ (en general, $x=15+t,\ y=t$)."])),
 (2, r"\pau{Asturias, EBAU extraordinaria 2024} Sean las matrices $A=" + pm([[2, 1], [-1, 'm']]) + r"$, $B=" + pm([[1, 'm'], [-1, 1]]) + r"$, $C=" + pm([[0, '2m'], ['-2m', -1]]) + r"$, $D=\begin{pmatrix}x\\ y\end{pmatrix}$ y $E=\begin{pmatrix}1\\ 1\end{pmatrix}$."
     + tasks(1, [r"Si $(A\cdot B-C)\cdot D=E$, plantea un sistema de dos ecuaciones y dos incógnitas ($x$ e $y$) en función del parámetro $m$.", r"¿Para qué valores de $m$ tiene solución el sistema? Si la tiene, ¿es siempre única? Resuelve el sistema para $m=-1$."]),
     tasks(1, [r"$A\cdot B=\begin{pmatrix}1&2m+1\\ -1-m&0\end{pmatrix}$, \ $A\cdot B-C=\begin{pmatrix}1&1\\ m-1&1\end{pmatrix}$: \ \ $\res{\left\{\begin{aligned}x+y&=1\\ (m-1)x+y&=1\end{aligned}\right.}$",
               r"$|A|=2-m$. \ Si $m\neq2$: \rest{SCD}, solución única. \ Si $m=2$: las dos ecuaciones son $x+y=1$, \rest{SCI}. \ Tiene solución \rest{para todo $m$}, pero solo es única si $m\neq2$. \ Para $m=-1$: $x+y=1$, $-2x+y=1$ \ $\Rightarrow\res{x=0;\ y=1}$."])),
 (2, r"\pau{Madrid, EvAU extraordinaria 2022} Considera el sistema de ecuaciones lineales dependiente del parámetro $a\in\mathbb{R}$:" + dm(r'\left\{\begin{aligned}x+ay+z&=2\\ x-az&=0\\ x+y+z&=2\end{aligned}\right.') + tasks(1, ["Discute la compatibilidad del sistema para los diferentes valores de $a$.", "Resuelve el sistema para $a=0$."]),
     tasks(1, [r"$|A|=\begin{vmatrix}1&a&1\\ 1&0&-a\\ 1&1&1\end{vmatrix}=1-a^2=0\Rightarrow a=\pm1$."
               + r"\par $\bullet$ $a\neq\pm1$: \rest{SCD}. \ $\bullet$ $a=1$: la 1.\textsuperscript{a} y la 3.\textsuperscript{a} ecuaciones son iguales, $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$: \rest{SCI}. \ $\bullet$ $a=-1$: $\operatorname{rg}(A)=2$ y $\begin{vmatrix}1&-1&2\\ 1&0&0\\ 1&1&2\end{vmatrix}=4\neq0\Rightarrow\operatorname{rg}(A^*)=3$: \rest{SI}.",
               r"$x+z=2$, $x=0$, $x+y+z=2$: \ $\res{x=0;\ y=0;\ z=2}$"])),
 (2, r"\pau{Madrid, EvAU extraordinaria 2024} Considera el sistema de ecuaciones lineales dependiente del parámetro $a\in\mathbb{R}$:" + dm(r'\left\{\begin{aligned}2x+y+3z&=2\\ 3x+y+z&=0\\ 8x+ay+5z&=2\end{aligned}\right.') + tasks(1, ["Discute el sistema para los diferentes valores de $a$.", "Resuelve el sistema de ecuaciones para $a=3$."]),
     tasks(1, [r"$|A|=7a-21=0\Rightarrow a=3$. \ $\bullet$ $a\neq3$: \rest{SCD}. \ $\bullet$ $a=3$: $\begin{vmatrix}2&1\\ 3&1\end{vmatrix}=-1\neq0$, $\operatorname{rg}(A)=2$, y los menores de orden 3 de $A^*$ valen 0 (la 3.\textsuperscript{a} ecuación es $E_1+2E_2$): $\operatorname{rg}(A^*)=2$, \rest{SCI}.",
               r"Restando $E_2-E_1$: $x-2z=-2$. Con $z=\lambda$: $x=-2+2\lambda$, \ $y=-3x-z=6-7\lambda$:\par $\res{x=-2+2\lambda;\ y=6-7\lambda;\ z=\lambda}$"])),
 (2, r"\pau{Madrid, EvAU ordinaria 2024} Considera el sistema de ecuaciones lineales dependiente del parámetro $a\in\mathbb{R}$:" + dm(r'\left\{\begin{aligned}2x+y+z&=a\\ x+ay+z&=a+1\\ x+y+az&=2\end{aligned}\right.') + tasks(1, ["Discute el sistema en función de los valores del parámetro $a$.", "Resuelve el sistema de ecuaciones para $a=1$."]),
     tasks(1, [r"$|A|=2a^2-2a=2a(a-1)=0\Rightarrow a=0,\ a=1$."
               + r"\par $\bullet$ $a\neq0,1$: \rest{SCD}. \ $\bullet$ $a=0$: $\operatorname{rg}(A)=2$ y $\begin{vmatrix}2&1&0\\ 1&0&1\\ 1&1&2\end{vmatrix}=-3\neq0$: \rest{SI}. \ $\bullet$ $a=1$: la 2.\textsuperscript{a} y la 3.\textsuperscript{a} ecuaciones coinciden ($x+y+z=2$), $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$: \rest{SCI}.",
               r"$2x+y+z=1$ y $x+y+z=2$. Restando: $x=-1$; con $z=\lambda$: \ $\res{x=-1;\ y=3-\lambda;\ z=\lambda}$"])),
 (2, r"\pau{Madrid, PAU extraordinaria 2025} Se considera el sistema de ecuaciones dependiente del parámetro real $a$:" + dm(r'\left\{\begin{aligned}x+y+z&=2\\ 2x-y+z&=3\\ (a+1)x+az&=5\end{aligned}\right.') + tasks(1, ["Discute el sistema en función de los valores del parámetro real $a$.", "Resuelve el sistema para $a=2$."]),
     tasks(1, [r"$|A|=2-a=0\Rightarrow a=2$. \ $\bullet$ $a\neq2$: \rest{SCD}. \ $\bullet$ $a=2$: la 3.\textsuperscript{a} ecuación, $3x+2z=5$, es la suma de las dos primeras: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$, \rest{SCI}.",
               r"Con $z=\lambda$: $x+y=2-\lambda$, $2x-y=3-\lambda$ $\Rightarrow$ \ $\res{x=\tfrac{5-2\lambda}{3};\ y=\tfrac{1-\lambda}{3};\ z=\lambda}$"])),
 (2, r"\pau{Murcia, PAU extraordinaria 2025} Considera el sistema de ecuaciones siguiente, donde $a$ es un número real desconocido:" + dm(r'\left\{\begin{aligned}x-y+z&=1\\ 2x-y+z&=a\\ 3x+2y-az&=4\end{aligned}\right.') + tasks(1, ["Discute el sistema de ecuaciones según los valores de $a$.", "Resuelve el sistema para $a=1$."]),
     tasks(1, [r"$|A|=2-a=0\Rightarrow a=2$. \ $\bullet$ $a\neq2$: \rest{SCD}. \ $\bullet$ $a=2$: $\operatorname{rg}(A)=2$ y $\begin{vmatrix}1&-1&1\\ 2&-1&2\\ 3&2&4\end{vmatrix}=1\neq0\Rightarrow\operatorname{rg}(A^*)=3$: \rest{SI}.",
               r"$E_2-E_1$: $x=0$. Entonces $-y+z=1$ y $2y-z=4$: \ $\res{x=0;\ y=5;\ z=6}$"])),
 (2, r"\pau{Murcia, EBAU ordinaria 2023} Discute el sistema lineal de ecuaciones en función de los valores del parámetro $a$ y resuélvelo para $a=0$:" + dm(r'\left\{\begin{aligned}ax+y+z&=1\\ 2x+y+z&=1\\ x+ay+z&=2\end{aligned}\right.'),
     r"$|A|=-a^2+3a-2=-(a-1)(a-2)=0\Rightarrow a=1,\ a=2$."
     + r"\par $\bullet$ $a\neq1,2$: \rest{SCD}. \ $\bullet$ $a=1$: la 1.\textsuperscript{a} y la 3.\textsuperscript{a} ecuaciones tienen los mismos coeficientes y términos independientes distintos: \rest{SI}. \ $\bullet$ $a=2$: la 1.\textsuperscript{a} y la 2.\textsuperscript{a} son iguales, $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$: \rest{SCI}."
     + r"\par Para $a=0$: $y+z=1$, $2x+y+z=1$, $x+z=2$ \ $\Rightarrow\res{x=0;\ y=-1;\ z=2}$"),
 (2, r"Halla el valor de $k$ para que el sistema homogéneo \ $\left\{\begin{aligned}x+y-z&=0\\ 2x-y+kz&=0\\ x+2y+z&=0\end{aligned}\right.$ \ tenga soluciones distintas de la trivial y resuélvelo para ese valor.",
     r"$|A|=\begin{vmatrix}1&1&-1\\ 2&-1&k\\ 1&2&1\end{vmatrix}=-k-8=0\Rightarrow\res{k=-8}$. Si $k\neq-8$: \rest{SCD}, solo la solución trivial. Para $k=-8$ es \rest{SCI}: de la 1.\textsuperscript{a}, $z=x+y$; en la 3.\textsuperscript{a}, $2x+3y=0$." + dm(r'\boxed{x=3\lambda;\ \ y=-2\lambda;\ \ z=\lambda,\quad\lambda\in\mathbb{R}}')),
 (3, r"\pau{Madrid, EvAU extraordinaria 2023} Considera el sistema de ecuaciones lineales dependiente del parámetro real $a$:" + dm(r'\left\{\begin{aligned}ax+y+2z&=1\\ x+ay+2z&=a\\ x+2y+az&=1\end{aligned}\right.') + tasks(1, ["Discute el sistema en función de los valores del parámetro $a$.", "Resuelve el sistema de ecuaciones para $a=0$."]),
     tasks(1, [r"$|A|=a^3-7a+6=(a-1)(a-2)(a+3)=0\Rightarrow a=1,\ a=2,\ a=-3$."
               + r"\par $\bullet$ $a\neq1,2,-3$: \rest{SCD}. \ $\bullet$ $a=1$: la 1.\textsuperscript{a} y la 2.\textsuperscript{a} ecuaciones son iguales, $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$: \rest{SCI}. \ $\bullet$ $a=2$: la 2.\textsuperscript{a} y la 3.\textsuperscript{a} tienen los mismos coeficientes y términos independientes distintos: \rest{SI}. \ $\bullet$ $a=-3$: $\operatorname{rg}(A)=2$ y $\begin{vmatrix}-3&1&1\\ 1&-3&-3\\ 1&2&1\end{vmatrix}=-8\neq0$: \rest{SI}.",
               r"$y+2z=1$, $x+2z=0$, $x+2y=1$ \ $\Rightarrow\res{x=-\tfrac13;\ y=\tfrac23;\ z=\tfrac16}$"])),
 (3, r"\pau{Castilla y León, PAU ordinaria 2025} Dado el sistema con los parámetros $a$ y $b$:" + dm(r'\left\{\begin{aligned}ax+2y+z&=1\\ x+by+2z&=4\\ 3x+y+bz&=5\end{aligned}\right.') + tasks(1, [r"Si $b=-1$, clasifica el sistema en función de los diferentes valores del parámetro $a$.", r"Si $a=3$, clasifica el sistema en función de los diferentes valores del parámetro $b$."]),
     r"En general, $|A|=ab^2-2a-5b+13$ (el ejercicio de la sección de Cramer resolvía el caso $a=1$, $b=-2$)."
     + tasks(1, [r"$|A|=18-a=0\Rightarrow a=18$. \ $a\neq18$: \rest{SCD}. \ $a=18$: $\begin{vmatrix}1&-1\\ 3&1\end{vmatrix}=4\neq0$, $\operatorname{rg}(A)=2$, y $\begin{vmatrix}2&1&1\\ -1&2&4\\ 1&-1&5\end{vmatrix}=36\neq0$: \rest{SI}.",
                 r"$|A|=3b^2-5b+7$, que no se anula nunca (discriminante $25-84<0$): \rest{SCD para todo $b$}."])),
]))

# =====================================================================
def prob(R, sol, n=None):
    ck('sol', R, sol); ck('cls', R, 'SCD' if n is None else n)
    return R
P = {}
P['can22'] = prob([[1, 1, 1, 45], [40, 20, 60, 1700], [1, -3, 0, 0]], (30, 10, 5))
P['can23'] = prob([[1, 1, 1, 875], [-8, 5, 0, 0], [9, 9, -26, 0]], (250, 400, 225))
P['can24e'] = prob([[300, 400, 800, 28000], [1, -2, 0, 0], [0, 1, -2, 0]], (40, 20, 10))
P['can24o'] = prob([[1, -2, 0, 0], [0, 2, -5, 0], [F(3, 10), F(3, 10), F(3, 10), 51]], (100, 50, 20))
P['cnt22'] = prob([[4, 2, 3, 20], [3, 2, 2, 15], [1, 1, 0, 4]], (3, 1, 2))
P['cnt23'] = prob([[1, 1, 1, 180], [100, 200, 400, 29200], [1, -2, -2, 0]], (120, 34, 26))
P['cnt24e'] = prob([[5, 6, 2, 500], [0, 2, -1, 0], [1, 1, 0, 70]], (40, 30, 60))
P['cnt24o'] = prob([[300, 200, 100, 13000], [100, 100, 20, 4200], [2, 2, -1, 0]], (10, 20, 60))
P['cyl23'] = prob([[F(9, 10), F(9, 10), F(9, 10), 117], [2, 0, -1, 0], [0, -1, 1, 20]], (30, 40, 60))
P['clm22a'] = prob([[1, 1, 1, 15], [1, 0, -3, -1], [0, -3, 4, 0]], (8, 4, 3))
P['clm22b'] = prob([[10, 6, 3, 851000], [1, -1, 0, 2000], [5, 0, -6, 13000]], (47000, 45000, 37000))
P['clm22c'] = prob([[12, 6, 6, 51], [1, -1, 0, 1], [0, 1, -1, -F(1, 2)]], (F(5, 2), F(3, 2), 2))
P['clm23'] = prob([[1, 1, 1, 50], [2, -1, 0, 1], [2, 0, -5, 0]], (15, 29, 6))
P['clm23o'] = prob([[1, 1, 1, 70000], [1, 1, -1, 0], [3, -4, 1, 0]], (15000, 20000, 35000))
P['clm24e'] = prob([[1, 1, 1, 72], [-1, 1, -1, 0], [1, -F(1, 3), -1, 0]], (24, 36, 12))
P['clm24o'] = prob([[1, 1, 1, 36], [3, 0, -1, 0], [0, 2, -1, 6]], (6, 12, 18))
P['clm24v'] = prob([[-3, 4, -1, 1], [1, -1, 0, 7], [1, 1, -19, 0]], (32, 25, 3))
P['clm25'] = prob([[1, 1, 1, 25], [140, 130, 160, 3610], [1, -4, 1, 0]], (12, 5, 8))
P['cat22'] = prob([[1, -1, -1, 0], [-1, 19, -1, 0], [1, 0, -1, 5]], (50, 5, 45))
P['cat23'] = prob([[5, 30, 10, 550], [1, 15, 20, 200]], lambda l: (50 + 10 * l, 10 - 2 * l, l), 'SCI')
P['mad24e'] = prob([[1, 1, 1, 70], [1, -1, -1, 0], [4, 2, 1, 180]], (35, 5, 30))
P['mad24o'] = prob([[1, 1, 1, 600], [10, 8, 5, 4900], [1, 0, -2, 0]], (200, 300, 100))
P['nav25'] = prob([[1, 1, 1, 65], [1, -1, 0, 5], [6, 12, 24, 720]], (30, 25, 10))
P['pv25e'] = prob([[1, 1, 1, 8], [10, 20, 50, 290], [1, -2, 0, 0]], (2, 1, 5))
P['pv25o'] = prob([[1, 1, 1, 20], [F(1, 4), F(1, 2), 1, 10], [1, F(9, 5), F(33, 10), F(178, 5)]], (8, 8, 4))
AST25O = lambda m: [[1, 3, 90], [2, m, 15 * m]]
par(AST25O, {6: 'SI'}, range(-3, 20), 'ast25o'); ck('sol', AST25O(F(15)), (75, 5)); ck('sol', AST25O(F(9)), (135, -15))
for mm in (-3, -1, 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15): ck('sol', AST25O(F(mm)), (F(45 * mm, mm - 6), F(15 * (mm - 12), mm - 6)))
AST23 = lambda m: [[1, -m, 0], [F(3, 20), F(3, 20), 3 * m]]
par(AST23, {-1: 'SI'}, range(-4, 6), 'ast23'); ck('sol', AST23(F(3)), (45, 15))
for mm in (0, 1, 2, 3, 4, 5): ck('sol', AST23(F(mm)), (F(20 * mm * mm, 1 + mm), F(20 * mm, 1 + mm)))
def pr(R, v): return dm(sy(R, v))
S.append(("Problemas de planteamiento", [
 (1, r"\pau{Canarias, EBAU ordinaria 2022} Una empresa dedicada a actividades y deportes acuáticos ha vendido en un día un total de 45 sesiones entre pádel surf, kayak y moto acuática. Los precios por sesión y persona de estas actividades son 40 €, 20 € y 60 €, respectivamente, y la empresa ha recaudado un total de 1\,700 € ese día. Además, por cada persona que elige kayak hay tres que eligen pádel surf." + tasks(1, ["Plantea el sistema de ecuaciones correspondiente.", "¿Cuántas personas van a cada actividad?"])
     + recorda(r"Define bien las incógnitas (qué representa cada letra), traduce cada frase en una ecuación y, al final, comprueba que la solución tiene sentido en el contexto (números naturales, precios positivos\dots)."),
     r"$x$, $y$, $z$: personas de pádel surf, kayak y moto. \ " + pr(P['can22'], 'xyz') + r" \ Con $x=3y$: $4y+z=45$ y $7y+3z=85$\par $\Rightarrow$ \ \rest{30 de pádel surf, 10 de kayak y 5 de moto acuática}."),
 (2, r"\pau{Canarias, EBAU ordinaria 2023} En un barrio viven 875 personas clasificadas en tres grupos: niños y jóvenes, adultos y jubilados. La cuarta parte de los adultos es igual al doble de la quinta parte de los niños y jóvenes, y por cada 9 jubilados hay 26 del resto." + tasks(1, ["Plantea el sistema de ecuaciones correspondiente.", "Explicando los pasos del método empleado, resuelve el sistema planteado.", "¿Cuántas personas hay en cada grupo?"]),
     r"$x$: niños y jóvenes, $y$: adultos, $z$: jubilados. \ $\frac y4=\frac{2x}{5}$, \ $\frac{z}{x+y}=\frac{9}{26}$: \ " + pr(P['can23'], 'xyz') + r" \ De la 3.\textsuperscript{a} y la 1.\textsuperscript{a}: $35z=9\cdot875$, $z=225$; $x+y=650$ e $y=\frac85x$\par $\Rightarrow$ \ \rest{250 niños y jóvenes, 400 adultos y 225 jubilados}."),
 (1, r"\pau{Canarias, EBAU extraordinaria 2024} En una tienda de electrónica se venden teléfonos móviles, tabletas y ordenadores portátiles. Un móvil cuesta 300 €, una tableta 400 € y un portátil 800 €. En una semana se han ingresado 28\,000 € en ventas de estos aparatos. Se han vendido el doble de móviles que de tabletas y, por cada dos tabletas, se ha vendido un portátil." + tasks(1, ["Plantea el sistema de ecuaciones correspondiente.", "¿Cuántos aparatos de cada tipo se han vendido?"]),
     pr(P['can24e'], 'xyz') + r" ($x$ móviles, $y$ tabletas, $z$ portátiles). \ Con $y=2z$, $x=4z$: $2800z=28\,000$\par $\Rightarrow$ \ \rest{40 móviles, 20 tabletas y 10 portátiles}."),
 (2, r"\pau{Canarias, EBAU ordinaria 2024} Una jugadora de ajedrez ha conseguido premios en 51 de los torneos en los que ha participado a lo largo de su vida. Los torneos han sido locales, nacionales e internacionales. El número de torneos locales en los que ha jugado ha sido el doble de los nacionales; además, por cada cinco torneos nacionales ha participado en dos internacionales. Los torneos en los que ha conseguido premio representan un 30\,\% de todos los torneos en los que ha participado." + tasks(1, ["Plantea el sistema de ecuaciones correspondiente.", "¿En cuántos torneos de cada clase ha participado esta jugadora?"]),
     r"$x$, $y$, $z$: torneos locales, nacionales e internacionales. \ " + pr(P['can24o'], 'xyz') + r" \ El total es $51/0{,}3=170$; con $x=2y$ y $z=\frac25y$: $\frac{17}{5}y=170$\par $\Rightarrow$ \ \rest{100 locales, 50 nacionales y 20 internacionales}."),
 (2, r"\pau{Cantabria, EBAU extraordinaria 2022} Un día de playa, Fabiola se acerca al chiringuito y compra 3 helados, 2 granizados y 2 horchatas, y paga un total de 20 €. Al comprobar el tique se da cuenta de que le han cobrado un helado y una horchata de más. Tras reclamar, el vendedor le devuelve 5 €. Además, para compensar el error, le ofrece llevarse en promoción un helado y un granizado por 2 €, lo que supone un descuento del 50\,\% respecto de los precios originales." + tasks(1, ["Plantea el sistema de ecuaciones que permite calcular el precio (sin descuento) de un helado, un granizado y una horchata.", "Resuélvelo."]),
     r"$x$, $y$, $z$: precio de un helado, de un granizado y de una horchata. Le han cobrado 4 helados, 2 granizados y 3 horchatas por 20 €; lo que tenía que pagar es 15 €; y el 50\,\% de $x+y$ es 2 €:\ " + pr(P['cnt22'], 'xyz')
     + r" \ Restando las dos primeras: $x+z=5$; con $y=4-x$, $z=5-x$ en la 2.\textsuperscript{a}: $x=3$\par $\Rightarrow$ \ \rest{helado 3 €, granizado 1 €, horchata 2 €}."),
 (1, r"\pau{Cantabria, EBAU ordinaria 2023} En un almacén de construcción venden sacos de cemento de 25 kg, 50 kg y 100 kg. Cierto día se vendió un total de 180 sacos por un importe de 29\,200 €. Se sabe que el precio del kg de cemento es de 4 € y que ese día se vendieron el doble de sacos de 25 kg que la suma de los sacos de 50 kg y de los de 100 kg." + tasks(1, ["Plantea un sistema de ecuaciones que permita calcular cuántos sacos de cada tamaño se vendieron ese día.", "Resuélvelo."]),
     r"Un saco de 25 kg vale 100 €, uno de 50 kg, 200 € y uno de 100 kg, 400 €: \ " + pr(P['cnt23'], 'xyz') + r" \ De la 1.\textsuperscript{a} y la 3.\textsuperscript{a}: $3(y+z)=180$, $y+z=60$, $x=120$; e $y+2z=86$\par $\Rightarrow$ \ \rest{120 sacos de 25 kg, 34 de 50 kg y 26 de 100 kg}."),
 (2, r"\pau{Cantabria, EBAU extraordinaria 2024} Una organización encargada de un evento deportivo tiene un presupuesto de 500 € para adquirir material promocional: banderas, camisetas y gorras. Los precios por unidad son de 5, 6 y 2 euros, respectivamente. La cantidad de camisetas debe ser la mitad de la de gorras, y la suma de banderas y camisetas debe ser 70." + tasks(1, ["Plantea el sistema de ecuaciones que permite calcular las unidades que se deben comprar de cada artículo si se quiere agotar el presupuesto.", "Analiza la compatibilidad del sistema.", "Resuélvelo."]),
     tasks(1, [r"$x$ banderas, $y$ camisetas, $z$ gorras: \ " + pr(P['cnt24e'], 'xyz'), r"$|A|=" + vm(coef(P['cnt24e'])) + r"=-5\neq0$: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3$, \rest{SCD}.", r"\rest{40 banderas, 30 camisetas y 60 gorras}."])),
 (2, r"\pau{Cantabria, EBAU ordinaria 2024} Una empresa de jardinería necesita adquirir 300 kg de tierra, 200 kg de piedras decorativas y 100 kg de semillas. Al comparar precios entre dos proveedores, A y B, obtiene estas ofertas: el proveedor A le ofrece un precio total de 13\,000 €; el proveedor B, que hace descuentos por renovación de inventario, reduce el precio de la tierra a un tercio del que ofrece A, el de las piedras a la mitad y el de las semillas a una quinta parte, y resulta un ahorro de 8\,800 € respecto del precio total de A. Además, para el proveedor A, el precio por kg de las semillas es el doble de la suma de los precios por kg de la tierra y de las piedras." + tasks(1, ["Plantea el sistema de ecuaciones que permite calcular el precio por kilogramo de la tierra, las piedras y las semillas en el proveedor A.", "Analiza la compatibilidad del sistema.", "Resuélvelo."]),
     tasks(1, [r"$x$, $y$, $z$: €/kg de tierra, piedras y semillas en A. El proveedor B cobra $13\,000-8\,800=4\,200$ €: \ " + pr(P['cnt24o'], 'xyz'),
               r"$|A|=" + vm(coef(P['cnt24o'])) + r"=" + q(det(coef(P['cnt24o']))) + r"\neq0$: \rest{SCD}.", r"Sustituyendo $z=2x+2y$: $5x+4y=130$ y $x+y=30$\par $\Rightarrow$ \ \rest{tierra 10 €/kg, piedras 20 €/kg, semillas 60 €/kg}."])),
 (1, r"\pau{Castilla y León, EBAU ordinaria 2023} Compramos tres entradas para tres actividades: una para el teatro, otra para un partido de baloncesto y otra para un concierto. Después de descontarnos el 10\,\% del precio total, hemos pagado 117 euros por todas las entradas. Sabemos que el precio de la entrada del concierto es el doble que el de la entrada del teatro y que la entrada del concierto es 20 euros más cara que la del partido de baloncesto. Determina el precio de la entrada de cada actividad.",
     r"$x$ teatro, $y$ baloncesto, $z$ concierto: \ " + pr(P['cyl23'], 'xyz') + r" \ $x+y+z=130$; con $x=\frac z2$, $y=z-20$: $\frac52z=150$\par $\Rightarrow$ \ \rest{teatro 30 €, baloncesto 40 €, concierto 60 €}."),
 (1, r"\pau{Castilla-La Mancha, EvAU extraordinaria 2022} El número total de premios Goya recibidos a lo largo de la carrera por tres mujeres (Isabel, Carmen y Enma) es de 15. Si aumentamos en un premio la cantidad que ha recibido Isabel, obtenemos el triple de los premios ganados por Enma, y los que ha recibido Enma equivalen a las tres cuartas partes de los que ha recibido Carmen." + tasks(1, ["Plantea el sistema de ecuaciones que nos permite averiguar cuántos premios Goya ha recibido cada una.", "Resuelve razonadamente el sistema planteado."]),
     r"$x$ Isabel, $y$ Carmen, $z$ Enma: $x+1=3z$, $z=\frac34y$: \ " + pr(P['clm22a'], 'xyz') + r"\par $\Rightarrow$ \ \rest{Isabel 8, Carmen 4 y Enma 3}."),
 (2, r"\pau{Castilla-La Mancha, EvAU extraordinaria 2022} Un concesionario de automóviles tiene en oferta tres modelos de coche: un deportivo, un familiar y un monovolumen. El mes pasado se vendieron 10 deportivos, 6 familiares y 3 monovolúmenes y se obtuvieron 851\,000 euros. El deportivo vale 2\,000 euros más que el familiar. Por 5 deportivos vendidos se obtienen 13\,000 euros más que si se venden 6 monovolúmenes." + tasks(1, ["Plantea el sistema de ecuaciones que nos permite averiguar el precio de cada uno de los tres modelos.", "Resuelve razonadamente el sistema planteado."]),
     pr(P['clm22b'], 'xyz') + r" \ Con $y=x-2000$ y $z=\frac{5x-13000}{6}$ en la 1.\textsuperscript{a}: $18{,}5x=869\,500$.\par $\Rightarrow$ \ \rest{deportivo 47\,000 €, familiar 45\,000 €, monovolumen 37\,000 €}."),
 (1, r"\pau{Castilla-La Mancha, EvAU ordinaria 2022} La caja de bombones que compro cuesta 51 euros y contiene 12 bombones de chocolate negro, 6 de chocolate con leche y 6 de chocolate blanco. Cada bombón de chocolate negro cuesta un euro más que los de chocolate con leche, y estos cuestan 50 céntimos menos que los de chocolate blanco." + tasks(1, ["Plantea el sistema de ecuaciones que nos permite averiguar cuánto cuesta cada tipo de bombón.", "Resuelve razonadamente el sistema planteado."]),
     pr(P['clm22c'], 'xyz') + r" \ Con $x=y+1$, $z=y+0{,}5$: $24y+15=51$\par $\Rightarrow$ \ \rest{negro 2{,}50 €, con leche 1{,}50 €, blanco 2 €}."),
 (2, r"\pau{Castilla-La Mancha, EvAU extraordinaria 2023} Una cooperativa manchega que distribuye tres tipos de vino, blanco, rosado y tinto, ha recibido un pedido de 50 botellas. Se sabe que el doble de botellas de vino blanco, por un lado, excede en una unidad a las de vino rosado y, por otro, coincide con el quíntuple del número de botellas de vino tinto." + tasks(1, ["Plantea un sistema de ecuaciones para averiguar cuántas botellas de vino blanco, rosado y tinto se pidieron.", "Resuelve razonadamente el sistema planteado."]),
     pr(P['clm23'], 'xyz') + r" \ Con $y=2x-1$, $z=\frac{2x}{5}$: $\frac{17}{5}x=51$\par $\Rightarrow$ \ \rest{15 de blanco, 29 de rosado y 6 de tinto}."),
 (2, r"\pau{Castilla-La Mancha, EvAU ordinaria 2023} La discografía de un grupo de rock legendario se reedita en tres discos (I, II y III) y las ventas totales alcanzan las 70\,000 unidades. Sabemos que del disco III se vendieron tantas unidades como de los otros dos juntos, y que la diferencia entre las unidades vendidas del III y las del II equivale al triple de la diferencia entre las vendidas del II y las del I." + tasks(1, ["Plantea el sistema de ecuaciones para calcular cuántas unidades de cada disco se vendieron.", "Resuelve razonadamente el sistema planteado."]),
     r"$z-y=3(y-x)$: \ " + pr(P['clm23o'], 'xyz') + r" \ Sumando las dos primeras, $z=35\,000$\par $\Rightarrow$ \ \rest{15\,000 del I, 20\,000 del II y 35\,000 del III}."),
 (2, r"\pau{Castilla-La Mancha, EvAU extraordinaria 2024} De los bebés inscritos en el mes de mayo en Castilla-La Mancha, 72 se llaman Alba, Pablo o David. Sabemos que el número de bebés llamados David coincide con la diferencia entre los que se llaman Pablo y las que se llaman Alba. Además, se han inscrito tantas niñas con el nombre de Alba como la suma de los inscritos como David y un tercio de los inscritos como Pablo." + tasks(1, ["Plantea el sistema de ecuaciones que permite averiguar cuántos bebés se han inscrito con cada nombre.", "Resuelve razonadamente el sistema planteado."]),
     r"$x$ Alba, $y$ Pablo, $z$ David: \ " + pr(P['clm24e'], 'xyz') + r" \ Sumando las dos primeras: $2y=72$, $y=36$\par $\Rightarrow$ \ \rest{24 Alba, 36 Pablo y 12 David}."),
 (2, r"\pau{Castilla-La Mancha, EvAU ordinaria 2024} En la fase nacional de la Olimpiada Matemática Española se reparten 36 medallas de oro, de plata y de bronce. El número de medallas de bronce triplica el de medallas de oro y, si dos de las medallas de plata pasaran a la categoría de bronce, entonces la cantidad de medallas de bronce duplicaría la de plata." + tasks(1, ["Plantea el sistema de ecuaciones para calcular cuántas medallas de cada tipo se reparten.", "Resuelve razonadamente el sistema planteado."]),
     r"$x$ oro, $y$ plata, $z$ bronce: $z+2=2(y-2)$: \ " + pr(P['clm24o'], 'xyz') + r"\par $\Rightarrow$ \ \rest{6 de oro, 12 de plata y 18 de bronce}."),
 (3, r"\pau{Castilla-La Mancha, EvAU ordinaria 2024} En una clase se celebran elecciones a delegada y se presentan dos candidatas, Inés y Nerea. Se sabe que cuatro veces el número de votos de Nerea menos tres veces el número de votos de Inés excede en un voto al número de votos nulos. Si dividimos el número de votos de Inés entre el de Nerea, obtenemos cociente 1 y resto 7 ($D=d\cdot c+r$). El 5\,\% del total de votos emitidos es nulo." + tasks(1, ["Plantea el sistema de ecuaciones para calcular el número de votos nulos y los que recibieron Inés y Nerea.", "Resuelve razonadamente el sistema planteado."]),
     r"$x$ Inés, $y$ Nerea, $z$ nulos: $4y-3x=z+1$, \ $x=y+7$, \ $z=0{,}05(x+y+z)\Leftrightarrow x+y-19z=0$: \ " + pr(P['clm24v'], 'xyz') + r"\par $\Rightarrow$ \ \rest{Inés 32 votos, Nerea 25 votos y 3 nulos}."),
 (1, r"\pau{Castilla-La Mancha, PAU extraordinaria 2025} En el Parador de Turismo de Almagro se alojaron ayer 25 huéspedes procedentes de Italia, Portugal y Japón. El gasto total en el Parador fue de 3\,610 €: 140 € por cada huésped italiano, 130 € por cada portugués y 160 € por cada japonés. El registro muestra que el número de portugueses es la cuarta parte de la suma de los huéspedes de los otros dos países." + tasks(1, ["Plantea el sistema de ecuaciones para calcular cuántos huéspedes hay de cada país.", "Calcula el número de huéspedes de cada uno de los países."]),
     pr(P['clm25'], 'xyz') + r" \ De la 1.\textsuperscript{a} y la 3.\textsuperscript{a}: $5y=25$, $y=5$; después $7x+8z=148$ y $x+z=20$\par $\Rightarrow$ \ \rest{12 italianos, 5 portugueses y 8 japoneses}."),
 (2, r"\pau{Cataluña, PAU extraordinaria 2022} Martín le cuenta a Marcelo que el otro día, cuando cogió el autocar para ir de Barcelona a Tarragona, el autocar se averió justo a mitad del trayecto. Desde ese punto fue a pie hasta la población más próxima, de manera que recorrió a pie una vigésima parte del trayecto total. Allí cogió un taxi hasta Tarragona, y dice que recorrió 5 km más en autocar que en taxi." + tasks(1, ["Plantea y resuelve un sistema de ecuaciones para calcular cuántos kilómetros recorrió en autocar, a pie y en taxi.", "Si el autocar iba a 100 km/h, Martín caminó a 5 km/h y el taxi iba a 90 km/h, ¿cuánto tiempo tardó en hacer todo el trayecto?"]),
     tasks(1, [r"$x$ autocar, $y$ a pie, $z$ taxi. El trayecto total es $x+y+z$: \ $x=\frac{x+y+z}{2}$, \ $y=\frac{x+y+z}{20}$, \ $x=z+5$:\ " + pr(P['cat22'], 'xyz') + r" \ De la 1.\textsuperscript{a} y la 2.\textsuperscript{a}, $x=10y$ y $z=9y$; en la 3.\textsuperscript{a}, $y=5$: \ \rest{50 km en autocar, 5 km a pie y 45 km en taxi}.",
               r"$\frac{50}{100}+\frac55+\frac{45}{90}=0{,}5+1+0{,}5=\res{2\text{ horas}}$."])),
 (3, r"\pau{Cataluña, PAU ordinaria 2023} Una empresa distribuye dos tipos de paquetes a las farmacias, A y B. El paquete A contiene 5 termómetros digitales de infrarrojos, 30 mascarillas y 10 test rápidos de antígenos. El paquete B contiene 1 termómetro, 15 mascarillas y 20 test. El paquete A cuesta 550 € y el B, 200 €. El precio de cada producto es el mismo en los dos tipos de paquete." + tasks(1, ["Con estos datos, ¿es posible hallar el precio de un termómetro, el de una mascarilla y el de un test de antígenos? Justifica la respuesta planteando y clasificando un sistema de ecuaciones. Resuelve el sistema dejando la solución en función del precio del test de antígenos.", "Si un test de antígenos cuesta 4 €, ¿cuál será el precio de una mascarilla? ¿Y el de un termómetro?"]),
     tasks(1, [r"$x$ termómetro, $y$ mascarilla, $z$ test: \ " + pr(P['cat23'], 'xyz') + r" \ Dos ecuaciones y tres incógnitas, $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2<3$: \rest{SCI}, \textbf{no} se pueden determinar los precios. Restando $5E_2-E_1$: $45y+90z=450$: \ $\res{y=10-2z;\ \ x=50+10z}$.",
               r"$z=4$: \ \rest{la mascarilla cuesta 2 € y el termómetro, 90 €}."])),
 (1, r"\pau{Madrid, EvAU extraordinaria 2024} En una tienda de música hay 70 instrumentos de tres tipos: guitarras, pianos y violines. Se sabe que la cantidad de pianos más la de violines es igual a la de guitarras. Si tuviéramos el mismo número de violines, pero el doble de pianos y cuatro veces el de guitarras, el total de instrumentos de la tienda sería de 180. Plantea un sistema de ecuaciones y determina el número de instrumentos de cada tipo.",
     r"$x$ guitarras, $y$ pianos, $z$ violines: \ " + pr(P['mad24e'], 'xyz') + r" \ De las dos primeras, $x=35$\par $\Rightarrow$ \ \rest{35 guitarras, 5 pianos y 30 violines}."),
 (1, r"\pau{Madrid, EvAU ordinaria 2024} Un equipo de baloncesto regional ha vendido tres tipos de entradas para el último partido: generales a 10 €, de estudiante a 8 € e infantiles a 5 €. El equipo ha vendido 600 entradas y ha ingresado 4\,900 €. Además, ha vendido el doble de entradas generales que de infantiles. Plantea el sistema de ecuaciones y resuélvelo para calcular el número de entradas vendidas de cada tipo.",
     pr(P['mad24o'], 'xyz') + r" \ Con $x=2z$: $3z+y=600$ y $25z+8y=4900$\par $\Rightarrow$ \ \rest{200 generales, 300 de estudiante y 100 infantiles}."),
 (2, r"\pau{Navarra, PAU ordinaria 2025} Una empresa envasa pastas en cajas de 250 g, 500 g y 1 kg. Cierto día se envasaron 65 cajas en total, 5 cajas más de tamaño pequeño (250 g) que de mediano (500 g). Sabiendo que el kilo de pastas cuesta 24 euros y que el importe total de las pastas envasadas ese día es de 720 euros, ¿cuántas cajas de cada tipo se han envasado?" + tasks(1, ["Plantea el sistema de ecuaciones lineales.", "Resuelve el sistema. Interpreta la solución en el contexto del problema."]),
     r"Las cajas valen 6 €, 12 € y 24 €: \ " + pr(P['nav25'], 'xyz') + r"\par $\Rightarrow$ \ \rest{30 cajas de 250 g, 25 de 500 g y 10 de 1 kg} (números naturales: la solución tiene sentido)."),
 (1, r"\pau{País Vasco, PAU extraordinaria 2025} El cajero automático de un banco solo dispone de billetes de 10, 20 y 50 euros. Hemos sacado 290 euros y el cajero nos ha dado exactamente 8 billetes. Además, el número de billetes de 10 euros es el doble que el de 20 euros." + tasks(1, ["Plantea el sistema de ecuaciones lineales asociado a este problema.", "Resuelve el sistema de ecuaciones lineales."]),
     pr(P['pv25e'], 'xyz') + r" \ Con $x=2y$: $3y+z=8$ y $40y+50z=290$\par $\Rightarrow$ \ \rest{2 billetes de 10 €, 1 de 20 € y 5 de 50 €}."),
 (2, r"\pau{País Vasco, PAU ordinaria 2025} Una tienda tiene latas de conserva de tomate de tres fabricantes: A, B y C. El fabricante A envasa el tomate en latas de 250 g, el B en latas de 500 g y el C en latas de 1 kg. Estas latas se venden a 1 €, 1{,}80 € y 3{,}30 €, respectivamente. Compramos 20 latas que pesan en total 10 kg y valen 35{,}60 €. Queremos saber cuántas latas hemos comprado de cada fabricante." + tasks(1, ["Plantea el sistema de ecuaciones que resuelve el problema.", "Resuelve el problema."]),
     pr(P['pv25o'], 'xyz') + r" \ Multiplicando por 4 la 2.\textsuperscript{a} y por 10 la 3.\textsuperscript{a}, y restando la 1.\textsuperscript{a}: $y+3z=20$ y $8y+23z=156$\par $\Rightarrow$ \ \rest{8 latas de A, 8 de B y 4 de C}."),
 (3, r"\pau{Asturias, PAU ordinaria 2025} En una atracción hay dos tipos de pases, el VIP y el normal, de precios $x$ e $y$ euros, respectivamente. Un grupo de personas pagó 90 € por un pase VIP y tres normales, mientras que otro grupo pagó $15m$ € por dos pases VIP y $m$ pases normales. Para determinar el precio de cada pase se utiliza el sistema" + dm(r'\left\{\begin{aligned}x+3y&=90\\ 2x+my&=15m\end{aligned}\right.') + tasks(1, ["Si $m=15$, ¿cuál fue el precio de cada tipo de pase?", "Da un valor de $m$ para el que el sistema tenga solución, pero esta solución no tenga sentido en el contexto del problema. Justifica la respuesta.", "¿Para qué valor de $m$ el sistema no tiene solución? Justifica la respuesta."]),
     tasks(1, [r"$x+3y=90$, $2x+15y=225$\par $\Rightarrow$ \ \rest{VIP 75 €, normal 5 €}.",
               r"Para $m\neq6$ es SCD con $x=\frac{45m}{m-6}$, $y=\frac{15(m-12)}{m-6}$. Si $6<m<12$, el precio $y$ es negativo: por ejemplo, $\res{m=9}$ da $x=135$, $y=-15$, que no tiene sentido.",
               r"$|A|=m-6=0\Rightarrow\res{m=6}$: $2x+6y=90$ contradice $x+3y=90$ (que multiplicada por 2 da 180): \rest{SI}."])),
 (3, r"\pau{Asturias, EBAU extraordinaria 2023} En una fiesta se bebieron $m$ copas de vino tinto por cada una de vino blanco. Cada copa (de vino tinto o blanco) contiene 0{,}15 litros y en total se bebieron $3m$ litros de vino." + tasks(1, ["Plantea un sistema de dos ecuaciones en función del parámetro $m$ en el que las incógnitas $x$ e $y$ sean el número de copas de vino tinto y de vino blanco, respectivamente.", "¿Para qué valores de $m$ tiene solución el sistema anterior? Si la tiene, ¿es siempre única? ¿Cuántas copas de cada tipo se bebieron si en total se consumieron 9 litros de vino?"]),
     tasks(1, [r"$\res{\left\{\begin{aligned}x-my&=0\\ 0{,}15x+0{,}15y&=3m\end{aligned}\right.}$",
               r"$|A|=0{,}15(1+m)$. Si $m\neq-1$: \rest{SCD} (solución única, $x=\frac{20m^2}{1+m}$, $y=\frac{20m}{1+m}$). Si $m=-1$: $x+y=0$ y $x+y=-20$: \rest{SI}. \ Con 9 litros, $3m=9$, $m=3$: $x+y=60$, $x=3y$\par $\Rightarrow$ \ \rest{45 copas de vino tinto y 15 de blanco}."])),
]))

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
print(len(CHK), 'comprobaciones correctas')

# =====================================================================
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
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

TIT = "Sistemas de ecuaciones lineales"
KW = "sistemas de ecuaciones lineales, método de Gauss, método matricial, regla de Cramer, teorema de Rouché-Frobenius, sistemas homogéneos, discusión de sistemas, parámetros, problemas, PAU"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 2: %s' % (t, TIT), capcalera='%s · Unidad 2: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 2' if sol else 'Ficha de ejercicios · Unidad 2') + '}{' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los pasos de Gauss pueden ser diferentes de los tuyos y ser igualmente correctos; lo que debe coincidir es la clasificación y la solución (en un SCI, la solución general se puede escribir de maneras diferentes según la incógnita que tomes como parámetro). Puedes comprobarlo con el resolutor de sistemas de los apuntes interactivos."
             if sol else r"Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas. Resuélvelos en el cuaderno justificando cada paso: indica siempre el método que utilizas y, en los problemas, qué representa cada incógnita.") + r'''
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
