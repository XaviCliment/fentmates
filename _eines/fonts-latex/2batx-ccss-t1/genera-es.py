# Versió en castellà de genera.py. Genera t1-fitxa-exercicis.tex i t1-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 1: Matrius i determinants)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les estrelles
# no es mostren. Totes les matrius es dibuixen a partir de les seues dades i els resultats (productes, potències,
# determinants, adjunts, inverses, rangs, passos de Gauss i equacions matricials) es calculen amb aritmètica exacta;
# al final, CHK comprova totes les afirmacions que no surten directament d'un càlcul.
# Ús: python3 genera.py && pdflatex t1-fitxa-exercicis.tex (dues vegades) && pdflatex t1-fitxa-solucions.tex
import os, re, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def m(s): return '$' + s + '$'
def dm(s): return r'\[' + s + r'\]'

# ---------- nombres i matrius ----------
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
def pm(M, d='pmatrix', f=None):
    f = f or (lambda c: q(c, 'tfrac'))
    return r'\begin{%s}' % d + r'\\'.join(' & '.join(f(c) for c in r) for r in M) + r'\end{%s}' % d
def vm(M): return pm(M, 'vmatrix')
def pd(M): return pm(M, f=lambda c: c if isinstance(c, str) else dec(c))

# ---------- àlgebra exacta ----------
def mat(M): return [[fr(c) for c in r] for r in M]
def add(A, B): return [[fr(a) + fr(b) for a, b in zip(r, s)] for r, s in zip(A, B)]
def sc(k, A): return [[fr(k) * fr(a) for a in r] for r in A]
def sub(A, B): return add(A, sc(-1, B))
def mul(A, B):
    assert len(A[0]) == len(B)
    return [[sum(fr(A[i][k]) * fr(B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def eye(n): return [[F(int(i == j)) for j in range(n)] for i in range(n)]
def pw(A, n):
    R = eye(len(A))
    for _ in range(n): R = mul(R, A)
    return R
def tr(M): return [list(r) for r in zip(*M)]
def eq(A, B): return mat(A) == mat(B)
def det(M):
    M = mat(M)
    if len(M) == 1: return M[0][0]
    return sum((-1) ** j * M[0][j] * det([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(len(M)))
def menor(M, i, j): return [r[:j] + r[j + 1:] for k, r in enumerate(M) if k != i]
def cof(M, i, j): return (-1) ** (i + j) * det(menor(M, i, j))
def adjm(M): return [[cof(M, i, j) for j in range(len(M))] for i in range(len(M))]
def inv(M): d = det(M); return [[c / d for c in r] for r in tr(adjm(M))]
def rank(M):
    M = mat(M); r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                k = M[i][c] / M[r][c]; M[i] = [a - k * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def sym(M): return eq(M, tr(M))
def asym(M): return eq(M, sc(-1, tr(M)))

# determinant d'ordre 3 per Sarrus, amb els sis productes
def sarrus(M):
    M = mat(M)
    pos = [M[0][0] * M[1][1] * M[2][2], M[0][1] * M[1][2] * M[2][0], M[0][2] * M[1][0] * M[2][1]]
    neg = [M[0][2] * M[1][1] * M[2][0], M[0][0] * M[1][2] * M[2][1], M[0][1] * M[1][0] * M[2][2]]
    def g(v): return '(' + '+'.join(q(x) for x in v).replace('+-', '-') + ')'
    return vm(M) + '=' + g(pos) + '-' + g(neg) + '=' + q(sum(pos) - sum(neg))

# passos de la inversa per adjunts
def invpas(A, nm='A'):
    d = det(A); assert d != 0
    s = r"$|%s|=%s\neq0$, por tanto $%s$ tiene inversa:" % (nm, q(d), nm)
    # si |A| no és ±1, deixem el factor 1/|A| fora de la matriu (més llegible)
    s += dm(r'\mathrm{Adj}(%s)=' % nm + pm(adjm(A)) + r',\qquad %s^{-1}=\frac{1}{%s}\big(\mathrm{Adj}(%s)\big)^t=' % (nm, q(d), nm)
            + (pm(inv(A)) if abs(d) == 1 else r'\frac{1}{%s}' % q(d) + pm(tr(adjm(A)))))
    return s

# ---------- mètode de Gauss per al rang (aritmètica exacta) ----------
def fila(i, p): return 'F_%d%s' % (i + 1, "'" * p)
def gauss(R, start=r'A='):
    M = mat(R); P = [0] * len(M)
    out = [start + pm(M)]; r = 0
    for c in range(len(M[0])):
        if r >= len(M): break
        cand = [i for i in range(r, len(M)) if M[i][c] != 0]
        if not cand: continue
        best = next((i for i in cand if abs(M[i][c]) == 1), cand[0])
        if best != r:
            M[r], M[best] = M[best], M[r]; P[r], P[best] = P[best], P[r]
            out.append(r'\xrightarrow{F_%d\leftrightarrow F_%d}' % (r + 1, best + 1) + pm(M))
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
            out.append(arr + pm(M))
        r += 1
    lead = [next((j for j, v in enumerate(x) if v != 0), 99) for x in M]
    assert all(lead[i] < lead[i + 1] or lead[i + 1] == 99 for i in range(len(lead) - 1)), M
    assert rank(M) == rank(R)
    lines = [out[0] + (out[1] if len(out) > 1 else '')] + out[2:]
    return ''.join(dm(l) for l in lines)

CHK = []
def ck(cond, *info): CHK.append((bool(cond), info))

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
A1 = [[2 * i - j for j in range(1, 5)] for i in range(1, 4)]
B1 = [[i + j if i <= j else 0 for j in range(1, 4)] for i in range(1, 4)]
C2 = [[(-1) ** (i + j) * i for j in range(1, 4)] for i in range(1, 3)]
M2 = {'a': [[1, -2, 5]], 'b': [[3], [0], [-1]], 'c': [[2, 0, 0], [0, -1, 0], [0, 0, 4]], 'd': [[3, 0], [0, 3]],
      'e': [[1, 4, -2], [0, 3, 5], [0, 0, -1]], 'f': [[2, -1, 3], [-1, 0, 5], [3, 5, 4]], 'g': [[0, 2, -3], [-2, 0, 1], [3, -1, 0]], 'h': [[0, 0], [0, 0]]}
ck(sym(M2['f']) and not sym(M2['g'])); ck(asym(M2['g']) and not asym(M2['f'])); ck(sym(M2['c']) and sym(M2['d']))
ck(all(M2['e'][i][j] == 0 for i in range(3) for j in range(i)))
x3, y3, z3, t3 = 3, 2, 3, 1
ck(eq([[x3 + y3, 2], [3, x3 - y3]], [[5, z3 - 1], [2 * t3 + 1, 1]]))
A4 = lambda a, b, c: [[1, a + 1, 3], [2, 0, b], [c - 1, 5, 4]]
B4 = lambda x, y, z: [[0, x, -2], [3, y, z], [2, -1, 0]]
ck(sym(A4(1, 5, 4))); ck(asym(B4(-3, 0, 1)))
V5 = [[12, 8], [5, 10], [9, 4]]
S.append(("Matrices. Definiciones y tipos", [
 (1, r"Escribe las matrices siguientes:" + tasks(1, [r"$A=(a_{ij})$, de orden $3\times4$, con $a_{ij}=2i-j$. ¿Cuál es el elemento $a_{23}$? ¿Y el elemento $a_{32}$?",
     r"$B=(b_{ij})$, cuadrada de orden 3, con $b_{ij}=i+j$ si $i\leq j$ \ y \ $b_{ij}=0$ si $i>j$. ¿De qué tipo es?",
     r"$C=(c_{ij})$, de orden $2\times3$, con $c_{ij}=(-1)^{i+j}\cdot i$."])
     + recorda(r"$a_{ij}$ es el elemento que ocupa la fila $i$ y la columna $j$. Una matriz de orden $n\times m$ tiene $n$ filas y $m$ columnas."),
     tasks(1, [r"$A=" + pm(A1) + r"$, \ \ $\res{a_{23}=%d}$, \ $\res{a_{32}=%d}$" % (A1[1][2], A1[2][1]),
               r"$B=" + pm(B1) + r"$: \ es \rest{triangular superior} (todos los elementos por debajo de la diagonal principal son 0).",
               r"$C=" + pm(C2) + r"$"])),
 (1, r"Indica de qué tipo es cada una de las matrices siguientes (fila, columna, cuadrada, nula, diagonal, escalar, triangular, simétrica, antisimétrica):"
     + tasks(4, [m(pm(M2[k])) for k in 'abcdefgh']),
     tasks(2, [r"Matriz \rest{fila} ($1\times3$).", r"Matriz \rest{columna} ($3\times1$).", r"\rest{Diagonal} (y también simétrica y triangular).",
               r"\rest{Escalar}: diagonal con todos los elementos iguales ($3I_2$).", r"\rest{Triangular superior}.", r"\rest{Simétrica}: $A^t=A$.",
               r"\rest{Antisimétrica}: $A^t=-A$ (diagonal de ceros).", r"\rest{Nula} de orden 2."])),
 (1, r"Calcula $x$, $y$, $z$ y $t$ para que se cumpla la igualdad \ $\begin{pmatrix}x+y & 2\\ 3 & x-y\end{pmatrix}=\begin{pmatrix}5 & z-1\\ 2t+1 & 1\end{pmatrix}$.",
     r"Dos matrices son iguales si lo son elemento a elemento: \ $x+y=5$, \ $x-y=1$, \ $z-1=2$, \ $2t+1=3$\par $\Rightarrow$ \ $\res{x=3;\ y=2;\ z=3;\ t=1}$"),
 (2, r"Halla los valores de las letras para que:" + tasks(1, [r"$A=\begin{pmatrix}1 & a+1 & 3\\ 2 & 0 & b\\ c-1 & 5 & 4\end{pmatrix}$ \ sea simétrica.",
     r"$B=\begin{pmatrix}0 & x & -2\\ 3 & y & z\\ 2 & -1 & 0\end{pmatrix}$ \ sea antisimétrica."]),
     tasks(1, [r"Debe ser $a_{ij}=a_{ji}$: \ $a+1=2$, \ $b=5$, \ $c-1=3$: \ $\res{a=1;\ b=5;\ c=4}$",
               r"Debe ser $b_{ij}=-b_{ji}$ (y diagonal nula): \ $x=-3$, \ $y=0$, \ $z=1$: \ $\res{x=-3;\ y=0;\ z=1}$"])),
 (1, r"Una cadena tiene tres tiendas de bicicletas, B1, B2 y B3. En enero, B1 vendió 12 bicicletas urbanas y 8 de montaña; B2, 5 urbanas y 10 de montaña, y B3, 9 urbanas y 4 de montaña."
     + tasks(1, [r"Escribe la matriz $V$ de ventas (una fila por tienda y una columna por tipo). ¿Cuál es su orden?", r"¿Qué significa el elemento $v_{32}$?", r"Escribe $V^t$. ¿Qué información da cada fila de $V^t$?"]),
     tasks(1, [r"$V=" + pm(V5) + r"$, de orden \rest{$3\times2$}.", r"$v_{32}=4$: \rest{bicicletas de montaña vendidas por B3}.",
               r"$V^t=" + pm(tr(V5)) + r"$: la 1.\textsuperscript{a} fila son las ventas de urbanas de cada tienda y la 2.\textsuperscript{a}, las de montaña."])),
]))

# =====================================================================
A6, B6, C6 = [[2, -1, 0], [1, 3, -2]], [[1, 0, 4], [-2, 1, 3]], [[0, 2], [-1, 1]]
A8, B8 = [[1, 2], [3, -1]], [[0, 1], [2, -2]]
AB8, BA8 = mul(A8, B8), mul(B8, A8)
S8a, S8b = pw(add(A8, B8), 2), add(add(pw(A8, 2), sc(2, AB8)), pw(B8, 2))
ck(not eq(AB8, BA8)); ck(not eq(S8a, S8b)); ck(eq(S8a, add(add(add(pw(A8, 2), AB8), BA8), pw(B8, 2))))
A9, B9 = [[1, 0, 2], [-1, 1, 0], [0, 3, 1]], [[2, 1, 0], [0, -1, 1], [1, 0, 3]]
f10, c10 = [[1, 2, -1]], [[3], [0], [2]]
A11 = [[1, 1], [0, 1]]
for n in range(1, 30): ck(eq(pw(A11, n), [[1, n], [0, 1]]))
B12 = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
ck(eq(pw(B12, 3), eye(3))); ck(eq(pw(B12, 100), B12))
C13 = [[0, 1, 2], [0, 0, 3], [0, 0, 0]]
ck(eq(pw(C13, 3), [[0] * 3] * 3)); ck(not eq(pw(C13, 2), [[0] * 3] * 3))
I13 = add(eye(3), C13); ck(eq(pw(I13, 2), add(add(eye(3), sc(2, C13)), pw(C13, 2))))
for a in range(-2, 3):
    for b in range(-2, 3): ck(eq(mul(A11, [[a, b], [0, a]]), mul([[a, b], [0, a]], A11)))
ck(not eq(mul(A11, [[1, 0], [1, 1]]), mul([[1, 0], [1, 1]], A11)))
sol15 = [(a, b) for a in range(-9, 10) for b in range(-9, 10) if eq(pw([[a, 1], [0, b]], 2), [[4, 3], [0, 1]])]
ck(sol15 == [(2, 1)], sol15)
A16 = [[2, -1], [3, -2]]
ck(eq(pw(A16, 2), eye(2))); ck(eq(pw(A16, 51), A16))
A17 = [[2, -2, -4], [-1, 3, 4], [1, -2, -3]]
ck(eq(pw(A17, 2), A17)); ck(eq(pw(A17, 7), A17))
S.append(("Operaciones con matrices", [
 (1, r"Dadas las matrices \ $A=" + pm(A6) + r"$, \ $B=" + pm(B6) + r"$ \ y \ $C=" + pm(C6) + r"$, \ calcula:"
     + tasks(3, [r'$A+B$', r'$2A-3B$', r'$A^t-B^t$', r'$C\cdot A$', r'$A\cdot B^t$', r'$C^2-I$'])
     + recorda(r"Para sumar, las matrices deben tener el mismo orden. El producto $A\cdot B$ solo existe si el número de \textbf{columnas} de $A$ es igual al número de \textbf{filas} de $B$: \ $(n\times m)\cdot(m\times p)=n\times p$."),
     tasks(2, [r"$A+B=" + pm(add(A6, B6)) + r"$", r"$2A-3B=" + pm(sub(sc(2, A6), sc(3, B6))) + r"$",
               r"$A^t-B^t=(A-B)^t=" + pm(tr(sub(A6, B6))) + r"$", r"$C\cdot A=" + pm(mul(C6, A6)) + r"$",
               r"$A\cdot B^t=" + pm(mul(A6, tr(B6))) + r"$", r"$C^2-I=" + pm(pw(C6, 2)) + '-' + pm(eye(2)) + '=' + pm(sub(pw(C6, 2), eye(2))) + r"$"])),
 (1, r"Las matrices $A$, $B$, $C$ y $D$ tienen órdenes $2\times3$, $3\times3$, $3\times2$ y $2\times2$, respectivamente. Indica cuáles de estos productos se pueden hacer y, si se pueden hacer, qué orden tiene el resultado:"
     + tasks(4, [r'$A\cdot B$', r'$B\cdot A$', r'$A\cdot C$', r'$C\cdot A$', r'$B\cdot C$', r'$C\cdot D$', r'$D\cdot A$', r'$A^2$']),
     tasks(4, [r'$\res{2\times3}$', r'\rest{No}', r'$\res{2\times2}$', r'$\res{3\times3}$', r'$\res{3\times2}$', r'$\res{3\times2}$', r'$\res{2\times3}$', r'\rest{No} ($A$ no es cuadrada)'])),
 (1, r"Sean \ $A=" + pm(A8) + r"$ \ y \ $B=" + pm(B8) + r"$." + tasks(1, [r"Calcula $A\cdot B$ y $B\cdot A$. ¿Es conmutativo el producto de matrices?",
     r"Calcula $(A+B)^2$ y $A^2+2AB+B^2$. ¿Por qué no coinciden?"]),
     tasks(1, [r"$A\cdot B=" + pm(AB8) + r"$, \ \ $B\cdot A=" + pm(BA8) + r"$: \ $AB\neq BA$, el producto de matrices \rest{no es conmutativo}.",
               r"$(A+B)^2=" + pm(S8a) + r"$, \ \ $A^2+2AB+B^2=" + pm(S8b) + r"$.\par Son diferentes porque $(A+B)^2=A^2+AB+BA+B^2$, y $AB+BA\neq2AB$ cuando $AB\neq BA$."])),
 (1, r"Calcula $A\cdot B$ y $B\cdot A$ para \ $A=" + pm(A9) + r"$ \ y \ $B=" + pm(B9) + r"$.",
     r"$A\cdot B=" + pm(mul(A9, B9)) + r"$, \qquad $B\cdot A=" + pm(mul(B9, A9)) + r"$"),
 (1, r"Sean la matriz fila $F=" + pm(f10) + r"$ y la matriz columna $C=" + pm(c10) + r"$. Calcula $F\cdot C$ y $C\cdot F$.",
     r"$F\cdot C=" + pm(mul(f10, c10)) + r"$ \ (orden $1\times1$, un número), \qquad $C\cdot F=" + pm(mul(c10, f10)) + r"$ \ (orden $3\times3$)."),
 (2, r"Dada \ $A=" + pm(A11) + r"$, calcula $A^2$, $A^3$ y $A^4$. Deduce la expresión de $A^n$ y calcula $A^{20}$."
     + recorda(r"Para calcular potencias altas, calcula unas cuantas, busca la regularidad y generalízala."),
     r"$A^2=" + pm(pw(A11, 2)) + r"$, \ $A^3=" + pm(pw(A11, 3)) + r"$, \ $A^4=" + pm(pw(A11, 4)) + r"$ \ $\Rightarrow$ \ $\res{A^n=\begin{pmatrix}1 & n\\ 0 & 1\end{pmatrix}}$, \ \ $A^{20}=" + pm(pw(A11, 20)) + r"$"),
 (2, r"Dada \ $B=" + pm(B12) + r"$, calcula $B^2$ y $B^3$. ¿Cuánto vale $B^{100}$?",
     r"$B^2=" + pm(pw(B12, 2)) + r"$, \ $B^3=I$. Las potencias se repiten cada 3: como $100=3\cdot33+1$, \ $B^{100}=(B^3)^{33}\cdot B=\res{B}$"),
 (2, r"Sea \ $C=" + pm(C13) + r"$. Calcula $C^2$ y $C^3$. ¿Cuánto vale $C^n$ para $n\geq3$? Calcula también $(I+C)^2$.",
     r"$C^2=" + pm(pw(C13, 2)) + r"$, \ $C^3=O$ \ $\Rightarrow$ \ $\res{C^n=O\ \text{para}\ n\geq3}$.\par Como $I$ conmuta con $C$: \ $(I+C)^2=I+2C+C^2=" + pm(pw(I13, 2)) + r"$"),
 (3, r"Halla todas las matrices $X$ de orden 2 que conmutan con \ $A=" + pm(A11) + r"$, es decir, que cumplen $A\cdot X=X\cdot A$.",
     r"Con $X=\begin{pmatrix}a & b\\ c & d\end{pmatrix}$: \ $AX=\begin{pmatrix}a+c & b+d\\ c & d\end{pmatrix}$, \ $XA=\begin{pmatrix}a & a+b\\ c & c+d\end{pmatrix}$."
     + r"\par Igualando: $a+c=a\Rightarrow c=0$; \ $b+d=a+b\Rightarrow d=a$. \ \ $\res{X=\begin{pmatrix}a & b\\ 0 & a\end{pmatrix},\ a,b\in\mathbb{R}}$"),
 (2, r"Calcula $a$ y $b$ para que la matriz \ $A=\begin{pmatrix}a & 1\\ 0 & b\end{pmatrix}$ \ cumpla \ $A^2=\begin{pmatrix}4 & 3\\ 0 & 1\end{pmatrix}$.",
     r"$A^2=\begin{pmatrix}a^2 & a+b\\ 0 & b^2\end{pmatrix}$: \ $a^2=4$, \ $b^2=1$, \ $a+b=3$. Las únicas combinaciones de $a=\pm2$, $b=\pm1$ con suma 3 son \ $\res{a=2;\ b=1}$"),
 (2, r"Comprueba que la matriz \ $A=" + pm(A16) + r"$ \ cumple $A^2=I$ y calcula $A^{51}$ y $A^{100}$.",
     r"$A^2=" + pm(pw(A16, 2)) + r"=I$. \ $A^{51}=(A^2)^{25}\cdot A=\res{A}$; \ \ $A^{100}=(A^2)^{50}=\res{I}$"),
 (2, r"Una matriz cuadrada es \emph{idempotente} si $A^2=A$. Comprueba que \ $A=" + pm(A17) + r"$ \ es idempotente y calcula $A^n$.",
     r"$A^2=" + pm(pw(A17, 2)) + r"=A$. Entonces $A^3=A^2\cdot A=A\cdot A=A$, y así sucesivamente: \ $\res{A^n=A}$ para todo $n\geq1$."),
]))

# =====================================================================
D18 = [[[3, -2], [5, 4]], [[-1, 7], [2, -3]], [[0, 5], [-6, 9]]]
D19 = [[[1, 2, 3], [0, -1, 4], [2, 1, 0]], [[2, -1, 1], [3, 0, 2], [1, 4, -1]], [[1, 1, 1], [2, 3, 4], [4, 9, 16]]]
A20 = [[2, -1, 3], [0, 4, 0], [1, 5, -2]]
ck(det(A20) == 4 * cof(A20, 1, 1))
M21 = [[2, 0, 1, 0], [1, 3, 0, 0], [0, 1, 2, 1], [1, 0, 1, 0]]
ck(det(M21) == -det(menor(M21, 2, 3)))
for x in (2, -3): ck(det([[x, 3], [2, x + 1]]) == 0)
for x in (2, -2): ck(det([[x, 2, 1], [1, x, 0], [0, 1, 1]]) == 3)
for x in range(-5, 6): ck(det([[x, 2, 1], [1, x, 0], [0, 1, 1]]) == x * x - 1)
for k in range(-6, 7):
    ck(det([[k + 1, 3], [1, k - 1]]) == k * k - 4)
    ck(det([[1, 2, k], [2, k, 1], [1, 1, 1]]) == -k * k + 3 * k - 3)
S.append(("Determinantes", [
 (1, r"Calcula los determinantes de orden 2 siguientes:" + tasks(4, [m(vm(M)) for M in D18] + [r'$\begin{vmatrix}x & x+1\\ x-1 & x\end{vmatrix}$'])
     + recorda(r"$\begin{vmatrix}a & b\\ c & d\end{vmatrix}=ad-bc$. \ Solo tienen determinante las matrices cuadradas."),
     tasks(4, [m(q(det(M))) for M in D18] + [r'$x^2-(x^2-1)=\res{1}$'])),
 (1, r"Calcula, con la regla de Sarrus:" + tasks(3, [m(vm(M)) for M in D19])
     + recorda(r"Sarrus: sumamos los productos de la diagonal principal y de las dos ``paralelas'' y restamos los de la diagonal secundaria y sus ``paralelas''."),
     tasks(1, [m(sarrus(M)) for M in D19])),
 (2, r"Dada la matriz \ $A=" + pm(A20) + r"$:" + tasks(1, [r"Calcula los adjuntos $A_{12}$, $A_{22}$ y $A_{31}$.", r"Calcula $|A|$ desarrollando por la fila que te resulte más cómoda."])
     + recorda(r"El adjunto del elemento $a_{ij}$ es $A_{ij}=(-1)^{i+j}\cdot\alpha_{ij}$, donde $\alpha_{ij}$ es el menor que se obtiene al suprimir la fila $i$ y la columna $j$."),
     tasks(1, [r"$A_{12}=-" + vm(menor(A20, 0, 1)) + '=' + q(cof(A20, 0, 1)) + r"$, \ \ $A_{22}=+" + vm(menor(A20, 1, 1)) + '=' + q(cof(A20, 1, 1)) + r"$, \ \ $A_{31}=+" + vm(menor(A20, 2, 0)) + '=' + q(cof(A20, 2, 0)) + r"$",
               r"Por la 2.\textsuperscript{a} fila (solo hay un elemento no nulo): \ $|A|=4\cdot A_{22}=4\cdot(%s)=\res{%s}$" % (q(cof(A20, 1, 1)), q(det(A20)))])),
 (3, r"Calcula el determinante de orden 4 \ $" + vm(M21) + r"$ \ desarrollando por la columna que tenga más ceros.",
     r"La 4.\textsuperscript{a} columna solo tiene un elemento no nulo, $a_{34}=1$, con signo $(-1)^{3+4}=-1$:" + dm(r'|M|=-1\cdot' + sarrus(menor(M21, 2, 3)) + r'\ \Rightarrow\ \boxed{|M|=%s}' % q(det(M21)))),
 (2, r"Resuelve las ecuaciones siguientes:" + tasks(2, [r'$\begin{vmatrix}x & 3\\ 2 & x+1\end{vmatrix}=0$', r'$\begin{vmatrix}x & 2 & 1\\ 1 & x & 0\\ 0 & 1 & 1\end{vmatrix}=3$']),
     tasks(1, [r"$x(x+1)-6=x^2+x-6=0$: \ $\res{x=2;\ x=-3}$", r"Por Sarrus: $x^2+0+1-(0+0+2)=x^2-1=3$: \ $\res{x=2;\ x=-2}$"])),
 (2, r"Estudia para qué valores de $m$ se anulan los determinantes siguientes:" + tasks(2, [r'$\begin{vmatrix}m+1 & 3\\ 1 & m-1\end{vmatrix}$', r'$\begin{vmatrix}1 & 2 & m\\ 2 & m & 1\\ 1 & 1 & 1\end{vmatrix}$']),
     tasks(1, [r"$(m+1)(m-1)-3=m^2-4=0$: \ $\res{m=2;\ m=-2}$",
               r"$m+2+2m-(m^2+1+4)=-m^2+3m-3$. El discriminante es $9-12<0$: \rest{no se anula nunca}, para ningún valor de $m$."])),
]))

# =====================================================================
A24 = [[1, 2, 0], [0, 1, 1], [2, 0, 1]]
ck(det(A24) == 5)
a, b, c = A24
D24 = [([b, a, c], -5), ([a, [2 * x for x in b], c], 10), (tr(A24), 5), ([a, [x + 3 * y for x, y in zip(b, a)], c], 5),
       (sc(-1, A24), -5), (sc(2, A24), 40), ([a, b, [2 * z - x for x, z in zip(a, c)]], 10)]
for M, v in D24: ck(det(M) == v, M, v)
A25, B25 = [[2, 0, 0], [0, 1, 0], [0, 0, 1]], [[-3, 0, 0], [0, 1, 0], [0, 0, 1]]
ck(det(A25) == 2 and det(B25) == -3)
V25 = [det(mul(A25, B25)), det(sc(3, A25)), det(inv(A25)), det(mul(tr(A25), B25)), det(mul(pw(A25, 2), inv(B25))), det(sc(-2, B25))]
ck(V25 == [-6, 54, F(1, 2), -6, F(-4, 3), 24], V25)
ck(det([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 0); ck(det([[2, -1, 4], [6, -3, 12], [1, 5, 0]]) == 0)
for a in range(-2, 3):
    for b in range(-2, 3):
        for c in range(-2, 3): ck(det([[1, a, b + c], [1, b, a + c], [1, c, a + b]]) == 0)
M27 = [[1, 1, 1, 1], [1, 2, 2, 2], [1, 2, 3, 3], [1, 2, 3, 4]]
ck(det(M27) == 1)
for x in range(-5, 6): ck(det([[x, 1, 1], [1, x, 1], [1, 1, x]]) == (x + 2) * (x - 1) ** 2)
for M in ([[0, 2, -3], [-2, 0, 1], [3, -1, 0]], [[0, 5, 1], [-5, 0, -4], [-1, 4, 0]]): ck(det(M) == 0)
S.append(("Propiedades de los determinantes", [
 (2, r"Sabiendo que \ $\begin{vmatrix}a & b & c\\ d & e & f\\ g & h & i\end{vmatrix}=5$, \ calcula, sin desarrollarlos:"
     + tasks(2, [r'$\begin{vmatrix}d & e & f\\ a & b & c\\ g & h & i\end{vmatrix}$', r'$\begin{vmatrix}a & b & c\\ 2d & 2e & 2f\\ g & h & i\end{vmatrix}$',
                 r'$\begin{vmatrix}a & d & g\\ b & e & h\\ c & f & i\end{vmatrix}$', r'$\begin{vmatrix}a & b & c\\ d+3a & e+3b & f+3c\\ g & h & i\end{vmatrix}$',
                 r'$\begin{vmatrix}-a & -b & -c\\ -d & -e & -f\\ -g & -h & -i\end{vmatrix}$', r'$\begin{vmatrix}2a & 2b & 2c\\ 2d & 2e & 2f\\ 2g & 2h & 2i\end{vmatrix}$',
                 r'$\begin{vmatrix}a & b & c\\ d & e & f\\ 2g-a & 2h-b & 2i-c\end{vmatrix}$'])
     + recorda(r"Cambiar dos filas de sitio cambia el signo; multiplicar una fila por $k$ multiplica el determinante por $k$; sumar a una fila una combinación lineal de las otras no lo cambia; $|A^t|=|A|$; \ $|k\cdot A_n|=k^n|A|$."),
     tasks(2, [r"Cambiamos $F_1$ y $F_2$: \ $\res{-5}$", r"$F_2$ multiplicada por 2: \ $\res{10}$", r"Es el de la traspuesta: \ $\res{5}$",
               r"A $F_2$ le sumamos $3F_1$: \ $\res{5}$", r"$|-A|=(-1)^3\cdot5=\res{-5}$", r"$|2A|=2^3\cdot5=\res{40}$",
               r"$2F_3-F_1$: el factor 2 multiplica y restar $F_1$ no cambia nada: \ $\res{10}$"])),
 (2, r"Sean $A$ y $B$ dos matrices cuadradas de orden 3 con $|A|=2$ y $|B|=-3$. Calcula:" + tasks(3, [r'$|A\cdot B|$', r'$|3A|$', r'$|A^{-1}|$', r'$|A^t\cdot B|$', r'$|A^2\cdot B^{-1}|$', r'$|-2B|$'])
     + recorda(r"$|A\cdot B|=|A|\cdot|B|$, \ \ $|A^{-1}|=\dfrac{1}{|A|}$, \ \ $|A^t|=|A|$, \ \ $|k\cdot A_n|=k^n|A|$."),
     tasks(3, [r'$2\cdot(-3)=\res{-6}$', r'$3^3\cdot2=\res{54}$', r'$\res{\tfrac12}$', r'$2\cdot(-3)=\res{-6}$', r'$\dfrac{2^2}{-3}=\res{-\tfrac43}$', r'$(-2)^3\cdot(-3)=\res{24}$'])),
 (2, r"Justifica, sin desarrollarlos, que los determinantes siguientes valen cero:"
     + tasks(3, [r'$\begin{vmatrix}1 & 2 & 3\\ 4 & 5 & 6\\ 7 & 8 & 9\end{vmatrix}$', r'$\begin{vmatrix}2 & -1 & 4\\ 6 & -3 & 12\\ 1 & 5 & 0\end{vmatrix}$', r'$\begin{vmatrix}1 & a & b+c\\ 1 & b & a+c\\ 1 & c & a+b\end{vmatrix}$']),
     tasks(1, [r"$F_3-F_2=F_2-F_1=(3\ 3\ 3)$, es decir, $F_3=2F_2-F_1$: las filas son \rest{linealmente dependientes}.", r"$F_2=3F_1$: \rest{dos filas proporcionales}.",
               r"Sumando $C_2$ a $C_3$, la tercera columna queda $(a+b+c)$ en todas las filas: es proporcional a $C_1$, y el determinante \rest{vale 0}."])),
 (3, r"Calcula aplicando las propiedades (haz ceros antes de desarrollar):" + tasks(2, [m(vm(M27)), r'$\begin{vmatrix}x & 1 & 1\\ 1 & x & 1\\ 1 & 1 & x\end{vmatrix}$ \ (factoriza el resultado)']),
     tasks(1, [r"Restando a cada fila la anterior ($F_4-F_3$, $F_3-F_2$, $F_2-F_1$) queda triangular: \ $\begin{vmatrix}1 & 1 & 1 & 1\\ 0 & 1 & 1 & 1\\ 0 & 0 & 1 & 1\\ 0 & 0 & 0 & 1\end{vmatrix}=\res{1}$",
               r"Sumando todas las columnas a la primera y sacando factor común $x+2$:\ \ $(x+2)\begin{vmatrix}1 & 1 & 1\\ 1 & x & 1\\ 1 & 1 & x\end{vmatrix}=(x+2)\begin{vmatrix}1 & 1 & 1\\ 0 & x-1 & 0\\ 0 & 0 & x-1\end{vmatrix}=\res{(x+2)(x-1)^2}$"])),
 (3, r"Razona las afirmaciones siguientes:" + tasks(1, [r"Si $A$ es una matriz antisimétrica de orden 3, entonces $|A|=0$.", r"Si $A$ es cuadrada y $A\cdot A^t=I$, entonces $|A|=1$ o $|A|=-1$.",
     r"Si $A$ es idempotente ($A^2=A$), entonces $|A|$ solo puede valer 0 o 1."]),
     tasks(1, [r"$A^t=-A\Rightarrow|A|=|A^t|=|-A|=(-1)^3|A|=-|A|\Rightarrow2|A|=0\Rightarrow\res{|A|=0}$",
               r"$|A\cdot A^t|=|A|\cdot|A^t|=|A|^2=|I|=1\Rightarrow\res{|A|=\pm1}$",
               r"$|A|^2=|A^2|=|A|\Rightarrow|A|\big(|A|-1\big)=0\Rightarrow\res{|A|=0\ \text{o}\ |A|=1}$"])),
]))

# =====================================================================
R29 = [[[2, 4, 6], [1, 2, 3], [3, 6, 9]], [[1, -1, 2, 0], [2, 1, 0, 3], [3, 0, 2, 3]], [[1, 2, 1], [0, 1, 3], [2, 1, 0], [1, 0, 2]]]
rk29 = [rank(M) for M in R29]; ck(rk29 == [1, 2, 3], rk29)
R30 = [[1, 2, 0, 1], [2, 1, 3, -1], [3, 3, 3, 0]]
m2 = [[1, 2], [2, 1]]
m3a, m3b = [r[:3] for r in R30], [r[:2] + [r[3]] for r in R30]
ck(det(m2) == -3 and det(m3a) == 0 and det(m3b) == 0 and rank(R30) == 2)
K31 = lambda k: [[1, 1, k], [1, k, 1], [k, 1, 1]]
for k in range(-6, 7):
    ck(det(K31(k)) == -(k - 1) ** 2 * (k + 2))
    ck(rank(K31(k)) == (1 if k == 1 else 2 if k == -2 else 3))
B32 = lambda a: [[1, 2, -1, 3], [2, 1, a, 1], [1, -1, 3, -2]]
for a in range(-6, 7): ck(rank(B32(a)) == (2 if a == 2 else 3))
S.append(("Rango de una matriz", [
 (1, r"Calcula por el método de Gauss el rango de las matrices siguientes:" + tasks(3, [m(pm(M)) for M in R29])
     + recorda(r"El rango es el número de filas (o columnas) linealmente independientes. Por Gauss: escalonamos la matriz y contamos las filas que no son nulas."),
     tasks(1, [r"Todas las filas son proporcionales a $(1\ 2\ 3)$: \ $\res{\operatorname{rg}(A)=1}$",
               gauss(R29[1]) + r"Quedan dos filas no nulas: \ $\res{\operatorname{rg}(B)=2}$ \ (de hecho, $F_3=F_1+F_2$).",
               gauss(R29[2], 'C=') + r"Quedan tres filas no nulas: \ $\res{\operatorname{rg}(C)=3}$"])),
 (2, r"Calcula el rango de \ $A=" + pm(R30) + r"$ \ utilizando menores (determinantes)."
     + recorda(r"El rango es el orden del mayor menor no nulo. Si un menor de orden $k$ es no nulo, basta con \emph{orlarlo} (añadirle una fila y una columna) para buscar uno de orden $k+1$."),
     r"$" + vm(m2) + r"=-3\neq0\Rightarrow\operatorname{rg}(A)\geq2$. Orlamos este menor con la 3.\textsuperscript{a} fila y con las columnas 3.\textsuperscript{a} y 4.\textsuperscript{a}:"
     + dm(vm(m3a) + '=' + q(det(m3a)) + r',\qquad ' + vm(m3b) + '=' + q(det(m3b)))
     + r"Ambos son nulos: \ $\res{\operatorname{rg}(A)=2}$"),
 (3, r"Estudia el rango de la matriz \ $A=\begin{pmatrix}1 & 1 & k\\ 1 & k & 1\\ k & 1 & 1\end{pmatrix}$ \ según los valores de $k$.",
     r"$|A|=k+k+k-k^3-1-1=-k^3+3k-2=-(k-1)^2(k+2)$, que se anula si $k=1$ o $k=-2$." + tasks(1, [r"Si $k\neq1$ y $k\neq-2$: \ $|A|\neq0$, \ $\res{\operatorname{rg}(A)=3}$",
     r"Si $k=1$: todas las filas son $(1\ 1\ 1)$: \ $\res{\operatorname{rg}(A)=1}$", r"Si $k=-2$: $|A|=0$ y $\begin{vmatrix}1 & 1\\ 1 & -2\end{vmatrix}=-3\neq0$: \ $\res{\operatorname{rg}(A)=2}$"])),
 (3, r"Estudia el rango de la matriz \ $B=\begin{pmatrix}1 & 2 & -1 & 3\\ 2 & 1 & a & 1\\ 1 & -1 & 3 & -2\end{pmatrix}$ \ según los valores de $a$.",
     dm(r"B\xrightarrow[F_3'=F_3-F_1]{F_2'=F_2-2F_1}\begin{pmatrix}1 & 2 & -1 & 3\\ 0 & -3 & a+2 & -5\\ 0 & -3 & 4 & -5\end{pmatrix}\xrightarrow{F_3''=F_3'-F_2'}\begin{pmatrix}1 & 2 & -1 & 3\\ 0 & -3 & a+2 & -5\\ 0 & 0 & 2-a & 0\end{pmatrix}")
     + r"Si $\res{a=2}$, la 3.\textsuperscript{a} fila es nula: \ $\operatorname{rg}(B)=2$. \ Si $\res{a\neq2}$: \ $\operatorname{rg}(B)=3$."),
]))

# =====================================================================
A34, B34 = [[2, 1], [5, 3]], [[1, 2], [2, 4]]
ck(eq(inv(A34), [[3, -1], [-5, 2]])); ck(det(B34) == 0)
M35 = [[[4, 3], [2, 2]], [[-1, 2], [3, -5]], [[6, 4], [3, 2]]]
ck(det(M35[2]) == 0)
A36, B36 = [[1, 2, 1], [0, 1, 0], [2, 0, 3]], [[2, 1, 0], [0, 1, 3], [1, 0, 1]]
ck(det(A36) == 1 and det(B36) == 5)
for M in (A34, M35[0], M35[1], A36, B36): ck(eq(mul(M, inv(M)), eye(len(M))) and eq(mul(inv(M), M), eye(len(M))))
K37 = lambda k: [[1, 0, -1], [0, k, 3], [4, 1, -k]]
for k in range(-6, 7): ck(det(K37(k)) == -(k - 1) * (k - 3))
A38 = [[2, 1], [0, 1]]
ck(eq(add(sub(pw(A38, 2), sc(3, A38)), sc(2, eye(2))), [[0, 0], [0, 0]])); ck(eq(inv(A38), sc(F(1, 2), sub(sc(3, eye(2)), A38))))
A39, B39 = [[1, 2], [1, 3]], [[2, 1], [1, 1]]
ck(eq(inv(mul(A39, B39)), mul(inv(B39), inv(A39)))); ck(not eq(inv(mul(A39, B39)), mul(inv(A39), inv(B39))))
S.append(("Matriz inversa", [
 (1, r"Calcula, a partir de la definición ($A\cdot A^{-1}=I$, planteando un sistema), la inversa de las matrices siguientes, si existe:" + tasks(2, [r'$A=' + pm(A34) + '$', r'$B=' + pm(B34) + '$'])
     + recorda(r"Una matriz cuadrada tiene inversa si y solo si su determinante es distinto de cero (matriz \emph{regular})."),
     tasks(1, [r"$\begin{pmatrix}2 & 1\\ 5 & 3\end{pmatrix}\begin{pmatrix}x & y\\ z & t\end{pmatrix}=\begin{pmatrix}1 & 0\\ 0 & 1\end{pmatrix}$: \ $\left\{\begin{aligned}2x+z&=1\\ 5x+3z&=0\end{aligned}\right.$ \ y \ $\left\{\begin{aligned}2y+t&=0\\ 5y+3t&=1\end{aligned}\right.$ \ $\Rightarrow$ \ $\res{A^{-1}=" + pm(inv(A34)) + r"}$",
               r"$\left\{\begin{aligned}x+2z&=1\\ 2x+4z&=0\end{aligned}\right.$ es incompatible (la 2.\textsuperscript{a} ecuación sería $2=0$): \ \rest{$B$ no tiene inversa} \ ($|B|=0$)."])),
 (1, r"Calcula la inversa de las matrices siguientes por el método de los adjuntos, si existe, y comprueba el resultado:" + tasks(3, [m(pm(M)) for M in M35])
     + recorda(r"$A^{-1}=\dfrac{1}{|A|}\big(\mathrm{Adj}(A)\big)^t$. \ Para orden 2: \ $\begin{pmatrix}a & b\\ c & d\end{pmatrix}^{-1}=\dfrac{1}{ad-bc}\begin{pmatrix}d & -b\\ -c & a\end{pmatrix}$."),
     tasks(1, [r"$|A|=%s$: \ $A^{-1}=\frac{1}{%s}" % (q(det(M)), q(det(M))) + pm(tr(adjm(M))) + '=' + r'\res{' + pm(inv(M)) + '}$' for M in M35[:2]]
               + [r"$|C|=12-12=0$: \ \rest{no tiene inversa}."])),
 (2, r"Calcula la inversa de las matrices siguientes:" + tasks(2, [r'$A=' + pm(A36) + '$', r'$B=' + pm(B36) + '$']),
     tasks(1, [invpas(A36), invpas(B36, 'B')])),
 (2, r"Dada la matriz \ $M=\begin{pmatrix}1 & 0 & -1\\ 0 & k & 3\\ 4 & 1 & -k\end{pmatrix}$:" + tasks(1, [r"¿Para qué valores de $k$ tiene inversa?", r"Calcula $M^{-1}$ para $k=2$."]),
     tasks(1, [r"$|M|=-k^2-0+0-(-4k)-3-0=-k^2+4k-3=-(k-1)(k-3)$: \ tiene inversa si \ $\res{k\neq1\ \text{y}\ k\neq3}$", invpas(K37(2), 'M')])),
 (3, r"Sea \ $A=" + pm(A38) + r"$." + tasks(1, [r"Comprueba que $A^2-3A+2I=O$.", r"Utiliza esta igualdad para calcular $A^{-1}$ sin determinantes."]),
     tasks(1, [r"$A^2=" + pm(pw(A38, 2)) + r"$, \ $A^2-3A+2I=" + pm(pw(A38, 2)) + '-' + pm(sc(3, A38)) + '+' + pm(sc(2, eye(2))) + r"=O$",
               r"$A^2-3A=-2I\Rightarrow A(A-3I)=-2I\Rightarrow A\cdot\dfrac{3I-A}{2}=I$: \ $\res{A^{-1}=\dfrac12(3I-A)=" + pm(inv(A38)) + r"}$"])),
 (2, r"Dadas \ $A=" + pm(A39) + r"$ \ y \ $B=" + pm(B39) + r"$, calcula $(A\cdot B)^{-1}$ y comprueba que coincide con $B^{-1}\cdot A^{-1}$, pero no con $A^{-1}\cdot B^{-1}$.",
     r"$A\cdot B=" + pm(mul(A39, B39)) + r"$, \ $(A\cdot B)^{-1}=\res{" + pm(inv(mul(A39, B39))) + r"}$.\par $A^{-1}=" + pm(inv(A39)) + r"$, \ $B^{-1}=" + pm(inv(B39)) + r"$: \ $B^{-1}A^{-1}=" + pm(mul(inv(B39), inv(A39)))
     + r"$ \ (coincide), \ \ $A^{-1}B^{-1}=" + pm(mul(inv(A39), inv(B39))) + r"$ \ (no coincide)."),
]))

# =====================================================================
A41, B41 = A34, [[1, 0], [2, -1]]
X41a, X41b = mul(inv(A41), B41), mul(B41, inv(A41))
ck(eq(mul(A41, X41a), B41) and eq(mul(X41b, A41), B41))
A42, B42, C42 = A39, [[1, 0], [2, 1]], [[3, 4], [5, 9]]
X42 = mul(inv(A42), sub(C42, B42)); ck(eq(add(mul(A42, X42), B42), C42))
A43, B43 = [[4, 1], [3, 3]], [[1, 2], [0, -1]]
N43 = sub(A43, sc(2, eye(2))); X43 = mul(B43, inv(N43)); ck(eq(sub(mul(X43, A43), sc(2, X43)), B43))
A44, B44, C44 = A11, B39, [[3, 2], [1, 1]]
X44 = mul(mul(inv(A44), C44), inv(B44)); ck(eq(mul(mul(A44, X44), B44), C44))
A45, B45 = A36, [[1, 0], [2, 1], [3, -1]]
X45 = mul(inv(A45), B45); ck(eq(mul(A45, X45), B45))
X46, Y46 = [[1, 0], [-1, 2]], [[1, 1], [2, -2]]
P46, Q46 = add(sc(2, X46), Y46), sub(X46, Y46)
ck(eq(sc(F(1, 3), add(P46, Q46)), X46))
X47, Y47 = [[2, -1], [0, 1]], [[1, 1], [3, 0]]
P47, Q47 = sub(sc(3, X47), sc(2, Y47)), add(X47, Y47)
ck(eq(sc(F(1, 5), add(P47, sc(2, Q47))), X47))
A48 = [[1, -1], [2, -1]]
X48 = mul(inv(A48), add(tr(A48), eye(2))); ck(eq(mul(A48, X48), add(tr(A48), eye(2))))
S.append(("Ecuaciones y sistemas matriciales", [
 (2, r"Dadas \ $A=" + pm(A41) + r"$ \ y \ $B=" + pm(B41) + r"$, resuelve las ecuaciones matriciales:" + tasks(2, [r'$A\cdot X=B$', r'$X\cdot A=B$'])
     + recorda(r"Despejamos $X$ igual que en una ecuación numérica, pero \textbf{no podemos dividir}: multiplicamos por la inversa por el mismo lado donde está la matriz. \ $AX=B\Rightarrow X=A^{-1}B$; \ \ $XA=B\Rightarrow X=BA^{-1}$."),
     r"$|A|=1$, \ $A^{-1}=" + pm(inv(A41)) + r"$." + tasks(1, [r"$X=A^{-1}\cdot B=" + pm(inv(A41)) + pm(B41) + r"=\res{" + pm(X41a) + r"}$",
                                                           r"$X=B\cdot A^{-1}=" + pm(B41) + pm(inv(A41)) + r"=\res{" + pm(X41b) + r"}$"])),
 (2, r"Resuelve la ecuación $A\cdot X+B=C$, siendo \ $A=" + pm(A42) + r"$, \ $B=" + pm(B42) + r"$ \ y \ $C=" + pm(C42) + r"$.",
     r"$AX=C-B\Rightarrow X=A^{-1}(C-B)$, \ con $A^{-1}=" + pm(inv(A42)) + r"$:" + dm(r'X=' + pm(inv(A42)) + pm(sub(C42, B42)) + r'=\boxed{' + pm(X42) + '}')),
 (3, r"Resuelve la ecuación $X\cdot A-2X=B$, siendo \ $A=" + pm(A43) + r"$ \ y \ $B=" + pm(B43) + r"$.",
     r"Sacamos factor común $X$ por la \textbf{izquierda}: \ $X(A-2I)=B\Rightarrow X=B(A-2I)^{-1}$." + dm(r'A-2I=' + pm(N43) + r',\quad |A-2I|=' + q(det(N43)) + r',\quad (A-2I)^{-1}=' + pm(inv(N43)))
     + dm(r'X=' + pm(B43) + pm(inv(N43)) + r'=\boxed{' + pm(X43) + '}')),
 (3, r"Resuelve la ecuación $A\cdot X\cdot B=C$, siendo \ $A=" + pm(A44) + r"$, \ $B=" + pm(B44) + r"$ \ y \ $C=" + pm(C44) + r"$.",
     r"$X=A^{-1}\cdot C\cdot B^{-1}$ \ (primero por $A^{-1}$ por la izquierda y después por $B^{-1}$ por la derecha):" + dm(r'X=' + pm(inv(A44)) + pm(C44) + pm(inv(B44)) + '=' + pm(mul(inv(A44), C44)) + pm(inv(B44)) + r'=\boxed{' + pm(X44) + '}')),
 (2, r"Halla la matriz $X$ que cumple $A\cdot X=B$, siendo \ $A=" + pm(A45) + r"$ \ y \ $B=" + pm(B45) + r"$. \ (La inversa de $A$ la tienes en el ejercicio \ref{ex:inv3}.)",
     r"$X=A^{-1}\cdot B=" + pm(inv(A45)) + pm(B45) + r"=\res{" + pm(X45) + r"}$"),
 (2, r"Resuelve el sistema matricial \ $\left\{\begin{aligned}2X+Y&=" + pm(P46) + r"\\ X-Y&=" + pm(Q46) + r"\end{aligned}\right.$"
     + recorda(r"Los sistemas matriciales se resuelven por reducción o sustitución, como los numéricos."),
     r"Sumando las dos ecuaciones: \ $3X=" + pm(add(P46, Q46)) + r"\Rightarrow\res{X=" + pm(X46) + r"}$; \ \ $Y=X-" + pm(Q46) + r"=\res{" + pm(Y46) + r"}$"),
 (2, r"Resuelve el sistema matricial \ $\left\{\begin{aligned}3X-2Y&=" + pm(P47) + r"\\ X+Y&=" + pm(Q47) + r"\end{aligned}\right.$",
     r"Multiplicando la 2.\textsuperscript{a} por 2 y sumando: \ $5X=" + pm(add(P47, sc(2, Q47))) + r"\Rightarrow\res{X=" + pm(X47) + r"}$; \ \ $Y=" + pm(Q47) + r"-X=\res{" + pm(Y47) + r"}$"),
 (3, r"Dada \ $A=" + pm(A48) + r"$, halla la matriz $X$ tal que \ $A\cdot X=A^t+I$.",
     r"$|A|=1$, \ $A^{-1}=" + pm(inv(A48)) + r"$, \ $A^t+I=" + pm(add(tr(A48), eye(2))) + r"$:" + dm(r'X=A^{-1}(A^t+I)=' + pm(inv(A48)) + pm(add(tr(A48), eye(2))) + r'=\boxed{' + pm(X48) + '}')),
]))

# =====================================================================
P49, C49 = [[40, 25, 10], [30, 35, 20]], [[2, 15], [3, 20], [5, 30]]
PC49 = mul(P49, C49); ck(eq(PC49, [[205, 1400], [265, 1750]]))
V50, W50, p50 = [[10, 15, 4], [8, 20, 6], [12, 10, 5]], [[12, 10, 6], [9, 18, 4], [10, 14, 7]], [[30], [20], [50]]
I50 = mul(add(V50, W50), p50)
A51 = [[0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 0]]  # V, M, B, P (fila: origen; columna: destinació)
A51_2 = pw(A51, 2); ck(A51_2[3][2] == 1 and A51_2[0][0] == 2)
T52, x52 = [[F(9, 10), F(2, 10)], [F(1, 10), F(8, 10)]], [[5000], [3000]]
x52a = mul(T52, x52); x52b = mul(T52, x52a); ck(eq(x52a, [[5100], [2900]]) and eq(x52b, [[5170], [2830]]))
ck(eq(mul(T52, [[5333 + F(1, 3)], [2666 + F(2, 3)]]), [[5333 + F(1, 3)], [2666 + F(2, 3)]]))
S.append(("Problemas de aplicación", [
 (2, r"Una empresa fabrica tres modelos de muebles (A, B y C) en dos fábricas. La matriz $P$ da las unidades fabricadas cada semana (filas: fábricas F1 y F2; columnas: modelos A, B y C) y la matriz $C$, las horas de trabajo y el coste de material (en euros) de cada unidad (filas: modelos A, B y C):"
     + dm(r'P=' + pm(P49) + r'\qquad C=' + pm(C49))
     + tasks(1, [r"Calcula $P\cdot C$ y explica qué significa cada elemento.", r"¿Tiene sentido calcular $C\cdot P$?"])
     + recorda(r"Para multiplicar, las columnas de la primera matriz y las filas de la segunda deben referirse a la \textbf{misma} cosa (aquí, los modelos)."),
     tasks(1, [r"$P\cdot C=" + pm(PC49) + r"$: \ la 1.\textsuperscript{a} columna son las \rest{horas semanales} de cada fábrica (205 y 265) y la 2.\textsuperscript{a}, el \rest{coste semanal de material} (1400 € y 1750 €).",
               r"$C\cdot P$ se puede calcular ($3\times2$ por $2\times3$), pero \rest{no tiene sentido}: multiplicaría datos de fábricas por datos de horas y euros."])),
 (2, r"Tres tiendas (B1, B2 y B3) venden pantalones, camisas y chaquetas. Las matrices $V$ y $W$ recogen las unidades vendidas en enero y en febrero (filas: tiendas; columnas: pantalones, camisas, chaquetas), y $p$ es la matriz columna de los precios: 30 €, 20 € y 50 €."
     + dm(r'V=' + pm(V50) + r'\qquad W=' + pm(W50) + r'\qquad p=' + pm(p50))
     + tasks(1, [r"Calcula $V+W$. ¿Qué representa?", r"Calcula $(V+W)\cdot p$ e interprétalo.", r"Si en marzo todos los precios suben un 10\,\%, ¿qué matriz da los nuevos precios?"]),
     tasks(1, [r"$V+W=" + pm(add(V50, W50)) + r"$: \rest{unidades vendidas} por cada tienda en los dos meses.",
               r"$(V+W)\cdot p=" + pm(I50) + r"$: \rest{ingresos} de B1, B2 y B3 en enero y febrero (en euros).",
               r"$1{,}1\cdot p=" + pd(sc(F(11, 10), p50)) + r"$ (en euros)."])),
 (3, r"Una compañía aérea une Valencia (V), Madrid (M), Barcelona (B) y Palma (P) con estos vuelos directos: de V a M, B y P; de M a V y B; de B a M y P, y de P a V."
     + tasks(1, [r"Escribe la matriz $A$ en la que $a_{ij}=1$ si hay vuelo directo de la ciudad $i$ a la ciudad $j$, y $a_{ij}=0$ si no lo hay (orden: V, M, B, P).",
                 r"Calcula $A^2$. ¿Qué indican sus elementos?", r"¿De cuántas maneras se puede ir de Palma a Barcelona haciendo exactamente una escala? ¿Y salir de Valencia y volver haciendo una escala?"]),
     tasks(1, [r"$A=" + pm(A51) + r"$", r"$A^2=" + pm(A51_2) + r"$: el elemento $(i,j)$ es el número de trayectos de $i$ a $j$ con \rest{exactamente una escala}.",
               r"$(A^2)_{43}=%d$: \rest{una} (P$\to$V$\to$B). \ $(A^2)_{11}=%d$: \rest{dos} (V$\to$M$\to$V y V$\to$P$\to$V)." % (A51_2[3][2], A51_2[0][0])])),
 (3, r"Una comarca tiene dos zonas, la costa (C) y el interior (I). Cada año, el 10\,\% de los habitantes de la costa se traslada al interior, y el 20\,\% de los del interior se traslada a la costa; el resto se queda donde está. Ahora hay 5000 habitantes en la costa y 3000 en el interior."
     + tasks(1, [r"Escribe la matriz $T$ tal que $\begin{pmatrix}C_{n+1}\\ I_{n+1}\end{pmatrix}=T\cdot\begin{pmatrix}C_n\\ I_n\end{pmatrix}$.", r"¿Cuántos habitantes habrá en cada zona dentro de un año? ¿Y dentro de dos años?",
                 r"Comprueba que, si hubiera $\tfrac{16000}{3}$ habitantes en la costa y $\tfrac{8000}{3}$ en el interior, la distribución no cambiaría."]),
     tasks(1, [r"$T=" + pd(T52) + r"$", r"$T\cdot" + pm(x52) + '=' + pm(x52a) + r"$; \ \ $T\cdot" + pm(x52a) + '=' + pm(x52b) + r"$: \rest{5100 y 2900} dentro de un año y \rest{5170 y 2830} dentro de dos.",
               r"$0{,}9\cdot\tfrac{16000}{3}+0{,}2\cdot\tfrac{8000}{3}=\tfrac{14400+1600}{3}=\tfrac{16000}{3}$ \ y \ $0{,}1\cdot\tfrac{16000}{3}+0{,}8\cdot\tfrac{8000}{3}=\tfrac{1600+6400}{3}=\tfrac{8000}{3}$: \ \rest{se mantiene}."])),
]))

# =====================================================================
# etiqueta per a referenciar l'exercici de les inverses d'ordre 3
for sec in S:
    for i, (st, qq, s) in enumerate(sec[1]):
        if qq.startswith(r"Calcula la inversa de las matrices siguientes:"):
            sec[1][i] = (st, r'\label{ex:inv3}' + qq, s)
assert any(r'\label{ex:inv3}' in qq for sec in S for st, qq, s in sec[1])
bad = [info for ok, info in CHK if not ok]
assert not bad, bad
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
'''

TIT = "Matrices y determinantes"
KW = "matrices, operaciones con matrices, potencias de matrices, determinantes, regla de Sarrus, adjuntos, propiedades de los determinantes, rango, matriz inversa, ecuaciones matriciales, sistemas matriciales"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 1: %s' % (t, TIT), capcalera='%s · Unidad 1: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 1' if sol else 'Ficha de ejercicios · Unidad 1') + '}{' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los pasos intermedios (las operaciones de Gauss, la fila o columna por la que desarrollas un determinante\ldots) pueden ser diferentes de los tuyos y ser igualmente correctos; lo que debe coincidir es el resultado. Puedes comprobar determinantes, rangos e inversas con el laboratorio de matrices de los apuntes interactivos."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Antes de multiplicar dos matrices, comprueba que los órdenes lo permiten, y recuerda que el producto de matrices \textbf{no} es conmutativo: en las ecuaciones matriciales, fíjate bien por qué lado multiplicas por la inversa.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, qq, s in exs:
            n += 1
            lab = re.search(r'\\label\{[^}]*\}', qq)
            out.append('\\ex{%d} %s\n\n' % (st, ((lab.group(0) if lab else '') + s) if sol else qq))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con el laboratorio de matrices de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't1-fitxa-solucions-es.tex' if sol else 't1-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
