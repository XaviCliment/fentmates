# Versió en castellà de genera.py. Genera t1-fitxa-exercicis-es.tex i t1-fitxa-solucions-es.tex (2n Batxillerat Matemàtiques II, Unitat 1: Matrius i determinants)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les estrelles
# no es mostren. El nivell és més alt que el de la fitxa de CCSS (_eines/fonts-latex/2batx-ccss-t1): potències n-èsimes,
# relacions polinòmiques, determinants amb lletres i d'ordre 4, rangs amb paràmetres, inverses en funció d'un paràmetre,
# equacions matricials no trivials i qüestions teòriques. Els resultats numèrics es calculen amb aritmètica exacta i
# CHK comprova totes les fórmules amb paràmetres (en una graella de valors) i totes les afirmacions teòriques.
# Ús: python3 genera.py && pdflatex t1-fitxa-exercicis.tex (dues vegades) && pdflatex t1-fitxa-solucions.tex (dues vegades)
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
G = [F(x, 2) for x in range(-9, 10)]  # graella de valors per a comprovar fórmules amb paràmetres
Z2 = [[0, 0], [0, 0]]
def isz(M): return all(c == 0 for r in M for c in r)
def lin(a, A, b, B): return add(sc(a, A), sc(b, B))  # aA+bB

# =====================================================================
A1 = [[i * i - j * j for j in range(1, 4)] for i in range(1, 4)]
B1 = [[int(j == i + 1) for j in range(4)] for i in range(4)]
C1 = [[min(i, j) for j in range(1, 4)] for i in range(1, 4)]
ck(asym(A1)); ck(sym(C1))
M2 = [[1, 4, -2], [0, 3, 5], [6, -1, 2]]
S2, T2 = sc(F(1, 2), add(M2, tr(M2))), sc(F(1, 2), sub(M2, tr(M2)))
ck(sym(S2) and asym(T2) and eq(add(S2, T2), M2))
P3, Q3, R3 = [[2, -1], [2, -1]], [[3, -4], [2, -3]], [[2, -4], [1, -2]]
S3 = [[1, 1, 3], [5, 2, 6], [-2, -1, -3]]
ck(eq(pw(P3, 2), P3)); ck(eq(pw(Q3, 2), eye(2))); ck(isz(pw(R3, 2)))
ck(not isz(pw(S3, 2)) and isz(pw(S3, 3)))
ck(not isz(pw(B1, 3)) and isz(pw(B1, 4)))
ck(not eq(pw(P3, 2), eye(2)) and not isz(pw(P3, 2)))
IP = sub(eye(2), P3); ck(eq(pw(IP, 2), IP) and isz(mul(P3, IP))); ck(eq(pw(sub(sc(2, P3), eye(2)), 2), eye(2)))
S.append(("Matrices. Definiciones y tipos", [
 (1, r"\label{ex:tipus}Escribe las matrices siguientes y di de qué tipo es cada una:" + tasks(1, [r"$A=(a_{ij})$, cuadrada de orden 3, con $a_{ij}=i^2-j^2$.",
     r"$B=(b_{ij})$, cuadrada de orden 4, con $b_{ij}=1$ si $j=i+1$ \ y \ $b_{ij}=0$ en caso contrario.", r"$C=(c_{ij})$, cuadrada de orden 3, con $c_{ij}=\min(i,j)$."]),
     tasks(1, [r"$A=" + pm(A1) + r"$: \ como $a_{ji}=j^2-i^2=-a_{ij}$, es \rest{antisimétrica}.",
               r"$B=" + pm(B1) + r"$: \rest{triangular superior} (con la diagonal principal también nula).",
               r"$C=" + pm(C1) + r"$: \ como $\min(i,j)=\min(j,i)$, es \rest{simétrica}."])),
 (2, r"Sea $A$ una matriz cuadrada cualquiera." + tasks(1, [r"Demuestra que $A+A^t$ es simétrica y que $A-A^t$ es antisimétrica.",
     r"Deduce que toda matriz cuadrada es la suma de una matriz simétrica y de una antisimétrica, y escribe \ $M=" + pm(M2) + r"$ \ de esta manera.",
     r"Demuestra que la única matriz que es a la vez simétrica y antisimétrica es la matriz nula."])
     + recorda(r"$(A+B)^t=A^t+B^t$, \ $(kA)^t=kA^t$ \ y \ $(A^t)^t=A$. \ $A$ es simétrica si $A^t=A$ y antisimétrica si $A^t=-A$."),
     tasks(1, [r"$(A+A^t)^t=A^t+(A^t)^t=A^t+A=A+A^t$ \ y \ $(A-A^t)^t=A^t-A=-(A-A^t)$.",
               r"$A=\underbrace{\tfrac12(A+A^t)}_{\text{simétrica}}+\underbrace{\tfrac12(A-A^t)}_{\text{antisimétrica}}$. \ Para $M$: \ $\res{M=" + pm(S2) + '+' + pm(T2) + r"}$",
               r"Si $A^t=A$ y $A^t=-A$, entonces $A=-A$, es decir, $2A=O$ y \rest{$A=O$}."])),
 (2, r"\label{ex:idem}Una matriz cuadrada $A$ es \emph{idempotente} si $A^2=A$, \emph{involutiva} si $A^2=I$ y \emph{nilpotente} si alguna potencia es la matriz nula (el menor exponente $k$ con $A^k=O$ se llama \emph{índice}). Clasifica las matrices:"
     + tasks(2, [r"$P=" + pm(P3) + "$", r"$Q=" + pm(Q3) + "$", r"$R=" + pm(R3) + "$", r"$S=" + pm(S3) + "$"])
     + r"\par ¿Cuál es el índice de nilpotencia de la matriz $B$ del ejercicio \ref{ex:tipus}?",
     tasks(1, [r"$P^2=" + pm(pw(P3, 2)) + r"=P$: \rest{idempotente}.", r"$Q^2=" + pm(pw(Q3, 2)) + r"=I$: \rest{involutiva}.",
               r"$R^2=" + pm(pw(R3, 2)) + r"$: \rest{nilpotente de índice 2}.", r"$S^2=" + pm(pw(S3, 2)) + r"$, \ $S^3=O$: \rest{nilpotente de índice 3}."])
     + r"\par Para $B$: \ $B^2=" + pm(pw(B1, 2)) + r"$, \ $B^3=" + pm(pw(B1, 3)) + r"$, \ $B^4=O$: \ \rest{índice 4}."),
 (3, r"Sea $A$ una matriz idempotente." + tasks(1, [r"Demuestra que $I-A$ también es idempotente y que $A(I-A)=O$.", r"Demuestra que $B=2A-I$ es involutiva.",
     r"Compruébalo con la matriz $P$ del ejercicio anterior."]),
     tasks(1, [r"$(I-A)^2=I-A-A+A^2=I-2A+A=I-A$; \ \ $A(I-A)=A-A^2=A-A=O$.", r"$(2A-I)^2=4A^2-2A-2A+I=4A-4A+I=I$.",
               r"$I-P=" + pm(IP) + r"$, \ $(I-P)^2=" + pm(pw(IP, 2)) + r"=I-P$, \ $P(I-P)=O$; \ \ $2P-I=" + pm(sub(sc(2, P3), eye(2))) + r"$ \ y \ $(2P-I)^2=I$."])),
]))

# =====================================================================
A5, B5, C5 = [[1, -2, 0], [3, 1, -1]], [[2, 1], [0, -1], [4, 3]], [[1, 2], [-1, 0]]
AB5 = mul(A5, B5)
ck(eq(tr(AB5), mul(tr(B5), tr(A5))))
A6 = [[1, 2], [0, 1]]
for x in range(-3, 4):
    for y in range(-3, 4): ck(eq(mul(A6, [[x, y], [0, x]]), mul([[x, y], [0, x]], A6)))
ck(not eq(mul(A6, [[0, 0], [1, 0]]), mul([[0, 0], [1, 0]], A6)))
sol7 = [(a, b, c) for a in range(-3, 4) for b in range(-3, 4) for c in range(-3, 4) if eq(pw([[a, b], [0, c]], 2), eye(2))]
ck(sorted(sol7) == sorted([(1, 0, 1), (-1, 0, -1)] + [(1, b, -1) for b in range(-3, 4)] + [(-1, b, 1) for b in range(-3, 4)]), sol7)
for mm in G:
    ck(eq(pw([[1, mm], [mm, 1]], 2), sc(2, [[1, mm], [mm, 1]])) == (mm * mm == 1))
    ck(eq(pw([[1, mm], [0, -1]], 2), eye(2)))
T9 = [[1, 1, 1], [0, 1, 1], [0, 0, 1]]
for n in range(1, 25): ck(eq(pw(T9, n), [[1, n, F(n * (n + 1), 2)], [0, 1, n], [0, 0, 1]]))
for a in G:
    for n in range(1, 9): ck(eq(pw([[a, 1], [0, a]], n), [[a ** n, n * a ** (n - 1)], [0, a ** n]]))
J = [[0, -1], [1, 0]]
ck(eq(pw(J, 2), sc(-1, eye(2))) and eq(pw(J, 4), eye(2))); ck(eq(pw(J, 2026), sc(-1, eye(2))))
SJ = eye(2); SJ = [[0, 0], [0, 0]]
P = eye(2)
for k in range(1, 2027): P = mul(P, J); SJ = add(SJ, P)
ck(eq(SJ, sub(J, eye(2))))
A12 = [[3, -4], [1, -1]]; N12 = sub(A12, eye(2))
ck(isz(pw(N12, 2)))
for n in range(1, 60): ck(eq(pw(A12, n), add(eye(2), sc(n, N12))))
A13 = [[1, 2], [3, 4]]
ck(eq(pw(A13, 2), lin(5, A13, 2, eye(2)))); ck(eq(pw(A13, 3), lin(27, A13, 10, eye(2)))); ck(eq(pw(A13, 4), lin(145, A13, 54, eye(2))))
S.append(("Operaciones con matrices", [
 (1, r"Dadas \ $A=" + pm(A5) + r"$, \ $B=" + pm(B5) + r"$ \ y \ $C=" + pm(C5) + r"$:" + tasks(1, [r"Calcula $(AB)^t-2C$ y $A\cdot B\cdot C$.", r"Calcula $B\cdot A$. ¿Tiene sentido comparar $AB$ y $BA$?",
     r"Comprueba que $(AB)^t=B^tA^t$ y explica por qué, en general, $A^tB^t$ no es igual a $(AB)^t$ (en este caso, ni siquiera tienen el mismo orden)."]),
     tasks(1, [r"$AB=" + pm(AB5) + r"$, \ \ $(AB)^t-2C=" + pm(tr(AB5)) + '-' + pm(sc(2, C5)) + '=' + r"\res{" + pm(sub(tr(AB5), sc(2, C5))) + r"}$, \ \ $ABC=\res{" + pm(mul(AB5, C5)) + r"}$",
               r"$BA=" + pm(mul(B5, A5)) + r"$: es de orden $3\times3$, mientras que $AB$ es $2\times2$: \rest{no son comparables}.",
               r"$B^tA^t=" + pm(tr(B5)) + pm(tr(A5)) + '=' + pm(mul(tr(B5), tr(A5))) + r"=(AB)^t$. \ $A^t$ es $3\times2$ y $B^t$ es $2\times3$: \ $A^tB^t$ es $3\times3$, mientras que $(AB)^t$ es $2\times2$. En general, $(AB)^t=B^tA^t$ y el producto no es conmutativo."])),
 (2, r"Sean $A$ y $B$ matrices cuadradas del mismo orden." + tasks(1, [r"Demuestra que $(A+B)^2=A^2+2AB+B^2$ si y solo si $AB=BA$.", r"Demuestra que $(A+B)(A-B)=A^2-B^2$ si y solo si $AB=BA$.",
     r"Halla todas las matrices $X$ de orden 2 que conmutan con \ $A=" + pm(A6) + r"$, es decir, tales que $AX=XA$."]),
     tasks(1, [r"$(A+B)^2=A^2+AB+BA+B^2$, que es igual a $A^2+2AB+B^2$ \ $\iff$ \ $AB+BA=2AB$ \ $\iff$ \ $BA=AB$.",
               r"$(A+B)(A-B)=A^2-AB+BA-B^2$, que es igual a $A^2-B^2$ \ $\iff$ \ $-AB+BA=O$ \ $\iff$ \ $AB=BA$.",
               r"Con $X=\begin{pmatrix}x & y\\ z & t\end{pmatrix}$: \ $AX=\begin{pmatrix}x+2z & y+2t\\ z & t\end{pmatrix}$, \ $XA=\begin{pmatrix}x & 2x+y\\ z & 2z+t\end{pmatrix}$."
               r"\par Igualando: $2z=0$, \ $2t=2x$: \ $\res{X=\begin{pmatrix}x & y\\ 0 & x\end{pmatrix}}$, \ con $x,y\in\mathbb{R}$ cualesquiera."])),
 (2, r"Halla todas las matrices de la forma \ $X=\begin{pmatrix}a & b\\ 0 & c\end{pmatrix}$ \ que cumplen $X^2=I$.",
     r"$X^2=\begin{pmatrix}a^2 & b(a+c)\\ 0 & c^2\end{pmatrix}=\begin{pmatrix}1 & 0\\ 0 & 1\end{pmatrix}$ \ $\Rightarrow$ \ $a=\pm1$, \ $c=\pm1$, \ $b(a+c)=0$."
     r"\par Si $a=c$, entonces $a+c\neq0$ y $b=0$: \ $\res{X=I}$ \ y \ $\res{X=-I}$. \ Si $a=-c$, $b$ puede ser cualquiera: \ $\res{X=\begin{pmatrix}1 & b\\ 0 & -1\end{pmatrix}}$ \ y \ $\res{X=\begin{pmatrix}-1 & b\\ 0 & 1\end{pmatrix}}$, \ $b\in\mathbb{R}$. ¡Hay infinitas soluciones!"),
 (2, r"Halla los valores de $m$ para los que \ $A=\begin{pmatrix}1 & m\\ m & 1\end{pmatrix}$ \ cumple $A^2=2A$. Comprueba después que \ $B=\begin{pmatrix}1 & m\\ 0 & -1\end{pmatrix}$ \ cumple $B^2=I$ para cualquier $m$, y calcula $B^{2027}$.",
     r"$A^2=\begin{pmatrix}1+m^2 & 2m\\ 2m & 1+m^2\end{pmatrix}=\begin{pmatrix}2 & 2m\\ 2m & 2\end{pmatrix}\iff1+m^2=2$: \ $\res{m=1\ \text{o}\ m=-1}$."
     r"\par $B^2=\begin{pmatrix}1 & m-m\\ 0 & 1\end{pmatrix}=I$. \ Como $2027=2\cdot1013+1$: \ $B^{2027}=(B^2)^{1013}\cdot B=\res{B}$"),
 (2, r"Dada \ $A=" + pm(T9) + r"$, calcula $A^2$ y $A^3$. Conjetura la expresión de $A^n$, comprueba que si es cierta para $n$ también lo es para $n+1$, y calcula $A^{10}$."
     + recorda(r"$1+2+\dots+n=\dfrac{n(n+1)}{2}$."),
     r"$A^2=" + pm(pw(T9, 2)) + r"$, \ $A^3=" + pm(pw(T9, 3)) + r"$ \ $\Rightarrow$ \ $\res{A^n=\begin{pmatrix}1 & n & \frac{n(n+1)}{2}\\ 0 & 1 & n\\ 0 & 0 & 1\end{pmatrix}}$"
     r"\par $A^n\cdot A=\begin{pmatrix}1 & n+1 & \frac{n(n+1)}{2}+n+1\\ 0 & 1 & n+1\\ 0 & 0 & 1\end{pmatrix}$ \ y \ $\frac{n(n+1)}{2}+n+1=\frac{(n+1)(n+2)}{2}$: es la misma fórmula con $n+1$. \ \ $A^{10}=" + pm(pw(T9, 10)) + r"$"),
 (2, r"Dada \ $A=\begin{pmatrix}a & 1\\ 0 & a\end{pmatrix}$, calcula $A^2$, $A^3$ y $A^4$, deduce la expresión de $A^n$ y calcula $A^{10}$ para $a=2$.",
     r"$A^2=\begin{pmatrix}a^2 & 2a\\ 0 & a^2\end{pmatrix}$, \ $A^3=\begin{pmatrix}a^3 & 3a^2\\ 0 & a^3\end{pmatrix}$, \ $A^4=\begin{pmatrix}a^4 & 4a^3\\ 0 & a^4\end{pmatrix}$ \ $\Rightarrow$ \ $\res{A^n=\begin{pmatrix}a^n & na^{n-1}\\ 0 & a^n\end{pmatrix}}$"
     r"\par (Al multiplicar por $A$: \ $na^{n-1}\cdot a+a^n=(n+1)a^n$.) \ Para $a=2$: \ $A^{10}=\begin{pmatrix}2^{10} & 10\cdot2^9\\ 0 & 2^{10}\end{pmatrix}=" + pm(pw([[2, 1], [0, 2]], 10)) + r"$"),
 (3, r"\label{ex:J}Sea \ $J=" + pm(J) + r"$." + tasks(1, [r"Calcula $J^2$, $J^3$ y $J^4$.", r"Calcula $J^{2026}$.", r"Calcula la suma \ $J+J^2+J^3+\dots+J^{2026}$."]),
     tasks(1, [r"$J^2=" + pm(pw(J, 2)) + r"=-I$, \ $J^3=-J=" + pm(pw(J, 3)) + r"$, \ $J^4=(J^2)^2=I$.",
               r"Las potencias se repiten cada 4 y $2026=4\cdot506+2$: \ $J^{2026}=J^2=\res{-I}$",
               r"$J+J^2+J^3+J^4=J-I-J+I=O$: cada bloque de cuatro potencias consecutivas suma $O$. Hay 506 bloques hasta $J^{2024}$, y quedan $J^{2025}+J^{2026}=J+J^2$:"
               r" \ $\res{J-I=" + pm(SJ) + r"}$"])),
 (3, r"Sea \ $A=" + pm(A12) + r"$ \ y sea $N=A-I$." + tasks(1, [r"Comprueba que $N^2=O$.", r"Demuestra que $A^n=I+nN$ para todo $n\geq1$ (multiplica $I+nN$ por $A=I+N$).", r"Calcula $A^{50}$."]),
     tasks(1, [r"$N=" + pm(N12) + r"$, \ $N^2=" + pm(pw(N12, 2)) + r"$",
               r"Para $n=1$ es cierta. Si $A^n=I+nN$: \ $A^{n+1}=(I+nN)(I+N)=I+N+nN+nN^2=I+(n+1)N$.",
               r"$A^{50}=I+50N=\res{" + pm(pw(A12, 50)) + r"}$"])),
 (3, r"\label{ex:pq}Sea \ $A=" + pm(A13) + r"$." + tasks(1, [r"Halla los números $p$ y $q$ tales que $A^2=pA+qI$.", r"Expresa $A^3$ y $A^4$ en la forma $\alpha A+\beta I$, sin calcularlas directamente."]),
     tasks(1, [r"$A^2=" + pm(pw(A13, 2)) + r"=p" + pm(A13) + r"+q" + pm(eye(2)) + r"$: \ de $2p=10$ y $3p=15$, $p=5$; de $p+q=7$, $q=2$: \ $\res{A^2=5A+2I}$",
               r"$A^3=A\cdot A^2=5A^2+2A=5(5A+2I)+2A=\res{27A+10I}$; \ \ $A^4=27A^2+10A=27(5A+2I)+10A=\res{145A+54I}$"])),
 (3, r"La \emph{traza} de una matriz cuadrada, $\operatorname{tr}(A)$, es la suma de los elementos de la diagonal principal." + tasks(1, [r"Comprueba que $\operatorname{tr}(AB)=\operatorname{tr}(BA)$ para dos matrices cualesquiera de orden 2.",
     r"Deduce que no existe ningún par de matrices de orden 2 tales que $AB-BA=I$."]),
     tasks(1, [r"Con $A=\begin{pmatrix}a & b\\ c & d\end{pmatrix}$ y $B=\begin{pmatrix}x & y\\ z & t\end{pmatrix}$: \ $\operatorname{tr}(AB)=(ax+bz)+(cy+dt)$ \ y \ $\operatorname{tr}(BA)=(xa+yc)+(zb+td)$: \rest{son iguales}.",
               r"$\operatorname{tr}(AB-BA)=\operatorname{tr}(AB)-\operatorname{tr}(BA)=0$, pero $\operatorname{tr}(I)=2$: \rest{es imposible}."])),
]))

# =====================================================================
M15 = [[1, 0, 2, 0], [3, -1, 1, 2], [0, 2, 1, -1], [2, 1, 0, 3]]
m15a, m15b = menor(M15, 0, 0), menor(M15, 0, 2)
ck(det(M15) == det(m15a) + 2 * det(m15b))
for x in G: ck(det([[x, 2, 3], [x, x, 3], [x, x, x]]) == x * (x - 2) * (x - 3))
D2 = lambda m: [[m, 1], [1, m]]
D3 = lambda m: [[m, 1, 0], [1, m, 1], [0, 1, m]]
D4 = lambda m: [[m, 1, 0, 0], [1, m, 1, 0], [0, 1, m, 1], [0, 0, 1, m]]
for x in G:
    ck(det(D3(x)) == x ** 3 - 2 * x); ck(det(D4(x)) == x * det(D3(x)) - det(D2(x))); ck(det(D4(x)) == x ** 4 - 3 * x * x + 1)
    ck(det(menor(D4(x), 0, 1)) == det(D2(x)))
for r in ((1 + 5 ** .5) / 2, -(1 + 5 ** .5) / 2, (5 ** .5 - 1) / 2, -(5 ** .5 - 1) / 2): ck(abs(r ** 4 - 3 * r * r + 1) < 1e-12)
S.append(("Determinantes", [
 (1, r"Calcula el determinante \ $|M|=" + vm(M15) + r"$ \ desarrollando por la primera fila.",
     r"La primera fila solo tiene dos elementos no nulos ($a_{11}=1$ y $a_{13}=2$, ambos con signo $+$):"
     + dm(r'|M|=1\cdot' + vm(m15a) + r'+2\cdot' + vm(m15b) + '=' + q(det(m15a)) + '+2\cdot(' + q(det(m15b)) + r')=\boxed{' + q(det(M15)) + '}')),
 (2, r"Resuelve la ecuación \ $\begin{vmatrix}x & 2 & 3\\ x & x & 3\\ x & x & x\end{vmatrix}=0$.",
     r"Por Sarrus: \ $x^3+6x+3x^2-(3x^2+3x^2+2x^2)=x^3-5x^2+6x=x(x-2)(x-3)=0$: \ $\res{x=0;\ x=2;\ x=3}$"),
 (3, r"Considera los determinantes \ $D_2=\begin{vmatrix}m & 1\\ 1 & m\end{vmatrix}$, \ $D_3=\begin{vmatrix}m & 1 & 0\\ 1 & m & 1\\ 0 & 1 & m\end{vmatrix}$ \ y \ $D_4=\begin{vmatrix}m & 1 & 0 & 0\\ 1 & m & 1 & 0\\ 0 & 1 & m & 1\\ 0 & 0 & 1 & m\end{vmatrix}$."
     + tasks(1, [r"Calcula $D_3$ y halla los valores de $m$ que lo anulan.", r"Desarrollando por la primera fila, comprueba que $D_4=m\cdot D_3-D_2$. Calcula $D_4$ y halla los valores de $m$ que lo anulan."]),
     tasks(1, [r"$D_3=m^3-m-m=m^3-2m=m(m^2-2)$: \ se anula para \ $\res{m=0;\ m=\pm\sqrt2}$",
               r"$D_4=m\cdot D_3-1\cdot\begin{vmatrix}1 & 1 & 0\\ 0 & m & 1\\ 0 & 1 & m\end{vmatrix}=m\cdot D_3-1\cdot(m^2-1)=m\cdot D_3-D_2$ \ (el menor se desarrolla por la 1.ª columna)."
               r"\par $D_4=m^4-2m^2-m^2+1=\res{m^4-3m^2+1}$. \ Ecuación bicuadrada: $m^2=\frac{3\pm\sqrt5}{2}$, \ y como $\frac{3+\sqrt5}{2}=\left(\frac{1+\sqrt5}{2}\right)^2$ \ y \ $\frac{3-\sqrt5}{2}=\left(\frac{\sqrt5-1}{2}\right)^2$:"
               r" \ $\res{m=\pm\tfrac{1+\sqrt5}{2};\ m=\pm\tfrac{\sqrt5-1}{2}}$"])),
]))

# =====================================================================
import random
random.seed(1)
def rnd3(d):
    while True:
        M = [[random.randint(-4, 4) for _ in range(3)] for _ in range(3)]
        if det(M) == d: return M
Mr = rnd3(3); (a, b, c), (d_, e, f), (g, h, i_) = Mr
ck(det([[2 * a, 2 * b, 2 * c], [d_ - 3 * g, e - 3 * h, f - 3 * i_], [g, h, i_]]) == 6)
ck(det([[a + d_, b + e, c + f], [d_ + g, e + h, f + i_], [g + a, h + b, i_ + c]]) == 6)
ck(det([[3 * c, a, b + 2 * a], [3 * f, d_, e + 2 * d_], [3 * i_, g, h + 2 * g]]) == 9)
ck(det([[g, h, i_], [a, b, c], [d_, e, f]]) == 3)
ck(det([[a - b, b - c, c - a], [d_ - e, e - f, f - d_], [g - h, h - i_, i_ - g]]) == 0)
ck(det(sc(-2, tr(Mr))) == -24)
A20, B20, C20 = [[2, 0, 0], [0, 1, 0], [0, 0, 1]], [[F(-1, 2), 0, 0], [0, 1, 0], [0, 0, 1]], [[-2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
R20 = [det(mul(sc(2, inv(A20)), tr(B20))), det(inv(sc(3, A20))), det(mul(pw(A20, 2), pw(inv(B20), 3))), det(mul(mul(tr(A20), inv(sc(2, B20))), A20)), det(mul(mul(B20, A20), inv(B20))),
       det(sc(3, C20)), det(mul(tr(C20), pw(C20, 3))), det(mul(inv(sc(2, C20)), pw(C20, 2)))]
ck(R20 == [-2, F(1, 54), -32, -1, 2, -162, 16, F(-1, 8)], R20)
ck(136 == 17 * 8 and 255 == 17 * 15 and 323 == 17 * 19)
M21 = [[1, 3, 6], [2, 5, 5], [3, 2, 3]]; ck(det(M21) % 17 == 0)
for x in G:
    for y in G[::3]:
        ck(det([[x + y, x, x], [x, x + y, x], [x, x, x + y]]) == y * y * (3 * x + y))
        ck(det([[x, y, y, y], [y, x, y, y], [y, y, x, y], [y, y, y, x]]) == (x + 3 * y) * (x - y) ** 3)
        for z in G[::4]: ck(det([[1, 1, 1], [x, y, z], [x * x, y * y, z * z]]) == (y - x) * (z - x) * (z - y))
    ck(det([[1, 1, 1], [1, x, 2], [1, x * x, 4]]) == (x - 1) * (2 - x))
ck(det([[1, 1, 1], [2, 3, 5], [4, 9, 25]]) == 6)
for n in (3, 5):
    Aa = [[0 if i == j else (i - j) * (i + 2 * j + 1) for j in range(n)] for i in range(n)]
    Aa = [[Aa[i][j] if i < j else -Aa[j][i] if i > j else 0 for j in range(n)] for i in range(n)]
    ck(asym(Aa) and det(Aa) == 0)
S.append(("Propiedades de los determinantes", [
 (2, r"Sabiendo que \ $\begin{vmatrix}a & b & c\\ d & e & f\\ g & h & i\end{vmatrix}=3$, \ calcula, sin desarrollarlos:"
     + tasks(2, [r'$\begin{vmatrix}2a & 2b & 2c\\ d-3g & e-3h & f-3i\\ g & h & i\end{vmatrix}$', r'$\begin{vmatrix}a+d & b+e & c+f\\ d+g & e+h & f+i\\ g+a & h+b & i+c\end{vmatrix}$',
                 r'$\begin{vmatrix}3c & a & b+2a\\ 3f & d & e+2d\\ 3i & g & h+2g\end{vmatrix}$', r'$\begin{vmatrix}g & h & i\\ a & b & c\\ d & e & f\end{vmatrix}$',
                 r'$\begin{vmatrix}a-b & b-c & c-a\\ d-e & e-f & f-d\\ g-h & h-i & i-g\end{vmatrix}$', r'$|-2A^t|$, donde $A$ es la matriz del determinante dado'])
     + recorda(r"Un determinante es lineal respecto a cada fila (o columna): si una fila es una suma, el determinante se descompone en una suma de dos determinantes."),
     tasks(1, [r"Sacamos el factor 2 de $F_1$; restar $3F_3$ a $F_2$ no lo cambia: \ $2\cdot3=\res{6}$",
               r"Hacemos $F_1-F_2+F_3$ y obtenemos $(2a\ \ 2b\ \ 2c)$; sacamos el 2 y, después, $F_3-F_1$ y $F_2-F_3$ dejan $(g\ h\ i)$ y $(d\ e\ f)$: \ $2\cdot3=\res{6}$",
               r"$C_3-2C_2$ da $(b\ e\ h)$; sacamos el 3 de $C_1$ y queda el orden de columnas $(c,a,b)$, que son dos cambios respecto a $(a,b,c)$: \ $3\cdot3=\res{9}$",
               r"De $(F_1,F_2,F_3)$ a $(F_3,F_1,F_2)$ hay dos cambios de filas: \ $\res{3}$",
               r"$C_1+C_2+C_3$ es la columna nula: \ $\res{0}$", r"$|-2A^t|=(-2)^3|A|=\res{-24}$"])),
 (2, r"Sean $A$ y $B$ matrices cuadradas de orden 3 con $|A|=2$ y $|B|=-\tfrac12$, y $C$ una matriz cuadrada de orden 4 con $|C|=-2$. Calcula:"
     + tasks(4, [r'$|2A^{-1}B^t|$', r'$|(3A)^{-1}|$', r'$|A^2B^{-3}|$', r'$|A^t(2B)^{-1}A|$', r'$|BAB^{-1}|$', r'$|3C|$', r'$|C^tC^3|$', r'$|(2C)^{-1}C^2|$']),
     tasks(2, [r"$2^3\cdot\frac12\cdot\left(-\frac12\right)=\res{-2}$", r"$\dfrac{1}{3^3\cdot2}=\res{\tfrac1{54}}$", r"$\dfrac{2^2}{(-1/2)^3}=\res{-32}$",
               r"$2\cdot\dfrac{1}{2^3\cdot(-1/2)}\cdot2=\res{-1}$", r"$|B|\cdot|A|\cdot\dfrac{1}{|B|}=\res{2}$", r"$3^4\cdot(-2)=\res{-162}$", r"$|C|^4=(-2)^4=\res{16}$",
               r"$\dfrac{(-2)^2}{2^4\cdot(-2)}=\res{-\tfrac18}$"])),
 (2, r"Sabiendo que los números 136, 255 y 323 son múltiplos de 17, demuestra, sin calcularlo, que el determinante \ $" + vm(M21) + r"$ \ también es múltiplo de 17. Compruébalo después calculándolo.",
     r"Hacemos $C_3'=100C_1+10C_2+C_3$ (no cambia el determinante):" + dm(vm(M21) + '=' + vm([[1, 3, 136], [2, 5, 255], [3, 2, 323]]) + '=17\cdot' + vm([[1, 3, 8], [2, 5, 15], [3, 2, 19]]))
     + r"y el último determinante es un número entero. \ Efectivamente, vale $" + q(det(M21)) + r"=17\cdot(" + q(det(M21) / 17) + ")$."),
 (3, r"\label{ex:lletres}Calcula, haciendo ceros antes de desarrollar, y expresa el resultado factorizado:" + tasks(1, [r'$\begin{vmatrix}a+b & a & a\\ a & a+b & a\\ a & a & a+b\end{vmatrix}$', r'$\begin{vmatrix}a & b & b & b\\ b & a & b & b\\ b & b & a & b\\ b & b & b & a\end{vmatrix}$']),
     tasks(1, [r"Sumamos todas las columnas a la primera y sacamos el factor $3a+b$; después restamos $F_1$ a las otras filas:"
               + dm(r'(3a+b)\begin{vmatrix}1 & a & a\\ 1 & a+b & a\\ 1 & a & a+b\end{vmatrix}=(3a+b)\begin{vmatrix}1 & a & a\\ 0 & b & 0\\ 0 & 0 & b\end{vmatrix}=\boxed{b^2(3a+b)}'),
               r"De la misma manera, con el factor $a+3b$:" + dm(r'(a+3b)\begin{vmatrix}1 & b & b & b\\ 1 & a & b & b\\ 1 & b & a & b\\ 1 & b & b & a\end{vmatrix}=(a+3b)\begin{vmatrix}1 & b & b & b\\ 0 & a-b & 0 & 0\\ 0 & 0 & a-b & 0\\ 0 & 0 & 0 & a-b\end{vmatrix}=\boxed{(a+3b)(a-b)^3}')])),
 (3, r"\label{ex:vdm}Demuestra que \ $\begin{vmatrix}1 & 1 & 1\\ a & b & c\\ a^2 & b^2 & c^2\end{vmatrix}=(b-a)(c-a)(c-b)$ \ (\emph{determinante de Vandermonde}) y utilízalo para:"
     + tasks(1, [r"calcular \ $\begin{vmatrix}1 & 1 & 1\\ 2 & 3 & 5\\ 4 & 9 & 25\end{vmatrix}$;", r"resolver la ecuación \ $\begin{vmatrix}1 & 1 & 1\\ 1 & x & 2\\ 1 & x^2 & 4\end{vmatrix}=0$."]),
     r"Hacemos $C_2-C_1$ y $C_3-C_1$, desarrollamos por la 1.ª fila y sacamos los factores $b-a$ y $c-a$:"
     + dm(r'\begin{vmatrix}1 & 0 & 0\\ a & b-a & c-a\\ a^2 & b^2-a^2 & c^2-a^2\end{vmatrix}=(b-a)(c-a)\begin{vmatrix}1 & 1\\ b+a & c+a\end{vmatrix}=(b-a)(c-a)(c-b)')
     + tasks(1, [r"$a=2$, $b=3$, $c=5$: \ $(3-2)(5-2)(5-3)=\res{6}$", r"$a=1$, $b=x$, $c=2$: \ $(x-1)(2-1)(2-x)=0$: \ $\res{x=1;\ x=2}$"])),
 (3, r"Razona las cuestiones siguientes:" + tasks(1, [r"¿Existe alguna matriz real $A$ de orden 3 tal que $A^2=-I$? ¿Y de orden 2? (Piensa en la matriz $J$ del ejercicio \ref{ex:J}.)",
     r"$B$ es una matriz cuadrada de orden 3 tal que $4B^3=B$. ¿Qué valores puede tener $|B|$?", r"Si $A$ es antisimétrica y de orden \emph{impar}, entonces $|A|=0$.",
     r"Si $A$ es de orden 3 y $A\cdot A^t=4I$, ¿cuánto puede valer $|A|$?"]),
     tasks(1, [r"$|A|^2=|A^2|=|-I|=(-1)^3=-1$, que es imposible: \rest{no existe}. \ En orden 2, $|-I|=(-1)^2=1$ y no hay contradicción: $J^2=-I$.",
               r"$|4B^3|=4^3|B|^3=|B|\Rightarrow|B|\,(64|B|^2-1)=0$: \ $\res{|B|=0;\ |B|=\pm\tfrac18}$",
               r"$|A|=|A^t|=|-A|=(-1)^n|A|=-|A|$ (porque $n$ es impar) $\Rightarrow2|A|=0\Rightarrow\res{|A|=0}$",
               r"$|A|\cdot|A^t|=|A|^2=|4I|=4^3=64$: \ $\res{|A|=\pm8}$"])),
]))

# =====================================================================
R25 = [[1, 2, 0, -1, 3], [2, 3, 1, 0, 1], [0, 1, -1, -2, 5], [1, 1, 2, 1, 0]]
ck(rank(R25) == 3, rank(R25))
B26 = lambda m: [[m, 1, 1, 2], [1, m, 1, 1], [1, 1, m, 1]]
for x in G:
    ck(det([r[:3] for r in B26(x)]) == (x - 1) ** 2 * (x + 2))
    ck(rank(B26(x)) == (2 if x == 1 else 3))
m26 = [[r[0], r[1], r[3]] for r in B26(-2)]; ck(det(m26) != 0)
A27 = lambda a: [[a, 1, 1, 1], [1, a, 1, 1], [1, 1, a, 1], [1, 1, 1, a]]
for x in G: ck(rank(A27(x)) == (1 if x == 1 else 3 if x == -3 else 4))
m27 = [r[:3] for r in A27(-3)[:3]]; ck(det(m27) == -16)
R28 = lambda a, b: [[1, -1, 2, 1], [2, 1, a, 3], [1, 2, 1, b]]
for x in G:
    for y in G: ck(rank(R28(x, y)) == (2 if (x, y) == (3, 2) else 3))
S.append(("Rango de una matriz", [
 (1, r"Calcula por el método de Gauss el rango de \ $A=" + pm(R25) + r"$.",
     gauss(R25) + r"Quedan tres filas no nulas: \ $\res{\operatorname{rg}(A)=3}$ \ (de hecho, $F_3=2F_1-F_2$)."),
 (3, r"Estudia, utilizando menores, el rango de la matriz \ $B=\begin{pmatrix}m & 1 & 1 & 2\\ 1 & m & 1 & 1\\ 1 & 1 & m & 1\end{pmatrix}$ \ según los valores de $m$."
     + recorda(r"Que se anule un menor de orden 3 no quiere decir que el rango sea 2: hay que comprobar que se anulan \textbf{todos} los menores de orden 3 que contienen un menor de orden 2 no nulo."),
     r"Menor de las tres primeras columnas: \ $\begin{vmatrix}m & 1 & 1\\ 1 & m & 1\\ 1 & 1 & m\end{vmatrix}=m^3-3m+2=(m-1)^2(m+2)$."
     + tasks(1, [r"Si $m\neq1$ y $m\neq-2$: \ hay un menor de orden 3 no nulo: \ $\res{\operatorname{rg}(B)=3}$",
                 r"Si $m=1$: \ $B=\begin{pmatrix}1 & 1 & 1 & 2\\ 1 & 1 & 1 & 1\\ 1 & 1 & 1 & 1\end{pmatrix}$, dos filas iguales y $\begin{vmatrix}1 & 2\\ 1 & 1\end{vmatrix}=-1\neq0$: \ $\res{\operatorname{rg}(B)=2}$",
                 r"Si $m=-2$: \ el menor de las columnas 1.ª, 2.ª y 4.ª es \ $" + vm(m26) + '=' + q(det(m26)) + r"\neq0$: \ $\res{\operatorname{rg}(B)=3}$"])),
 (3, r"Estudia el rango de \ $A=\begin{pmatrix}a & 1 & 1 & 1\\ 1 & a & 1 & 1\\ 1 & 1 & a & 1\\ 1 & 1 & 1 & a\end{pmatrix}$ \ según los valores de $a$. (Aprovecha el ejercicio \ref{ex:lletres}.)",
     r"Con $b=1$ en el ejercicio \ref{ex:lletres}: \ $|A|=(a+3)(a-1)^3$." + tasks(1, [r"Si $a\neq1$ y $a\neq-3$: \ $\res{\operatorname{rg}(A)=4}$", r"Si $a=1$: todas las filas son $(1\ 1\ 1\ 1)$: \ $\res{\operatorname{rg}(A)=1}$",
     r"Si $a=-3$: \ $|A|=0$ y el menor \ $" + vm(m27) + r"=" + q(det(m27)) + r"\neq0$ \ (es el primer determinante del ejercicio \ref{ex:lletres} con $a=1$, $b=-4$): \ $\res{\operatorname{rg}(A)=3}$"])),
 (3, r"Estudia el rango de \ $M=" + pm(R28('a', 'b')) + r"$ \ según los valores de $a$ y $b$.",
     dm(r"M\xrightarrow[F_3'=F_3-F_1]{F_2'=F_2-2F_1}\begin{pmatrix}1 & -1 & 2 & 1\\ 0 & 3 & a-4 & 1\\ 0 & 3 & -1 & b-1\end{pmatrix}\xrightarrow{F_3''=F_3'-F_2'}\begin{pmatrix}1 & -1 & 2 & 1\\ 0 & 3 & a-4 & 1\\ 0 & 0 & 3-a & b-2\end{pmatrix}")
     + r"La 3.ª fila es nula solo si $3-a=0$ y $b-2=0$: \ si $\res{a=3\ \text{y}\ b=2}$, \ $\operatorname{rg}(M)=2$; \ en cualquier otro caso, \ $\res{\operatorname{rg}(M)=3}$"),
]))

# =====================================================================
A30 = [[2, 1, -1], [0, 1, 3], [1, 0, 2]]
ck(det(A30) == 8); ck(eq(mul(A30, inv(A30)), eye(3)))
for a in G[::2]:
    for b in G[::3]:
        for c in G[::3]: ck(eq(inv([[1, a, b], [0, 1, c], [0, 0, 1]]), [[1, -a, a * c - b], [0, 1, -c], [0, 0, 1]]))
for m_ in G:
    if m_ != 0: ck(eq(inv([[m_, 1, 0], [0, m_, 1], [0, 0, m_]]), [[1 / m_, -1 / m_ ** 2, 1 / m_ ** 3], [0, 1 / m_, -1 / m_ ** 2], [0, 0, 1 / m_]]))
K32 = lambda k: [[1, k, 0], [k, 1, k], [0, k, 1]]
for k in G: ck(det(K32(k)) == 1 - 2 * k * k)
N33 = [[0, 2, 1], [0, 0, 3], [0, 0, 0]]
ck(isz(pw(N33, 3))); ck(eq(inv(sub(eye(3), N33)), add(add(eye(3), N33), pw(N33, 2))))
A34 = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
ck(eq(pw(A34, 2), add(A34, sc(2, eye(3))))); ck(eq(inv(A34), sc(F(1, 2), sub(A34, eye(3))))); ck(eq(pw(A34, 3), lin(3, A34, 2, eye(3)))); ck(eq(pw(A34, 4), lin(5, A34, 6, eye(3))))
ck(eq(inv(A13), sc(F(1, 2), sub(A13, sc(5, eye(2))))))
Q35 = sc(F(1, 3), [[1, 2, 2], [2, 1, -2], [2, -2, 1]])
ck(eq(mul(Q35, tr(Q35)), eye(3)) and sym(Q35) and eq(pw(Q35, 2), eye(3)))
S.append(("Matriz inversa", [
 (2, r"Calcula la inversa de las matrices siguientes:" + tasks(2, [r'$A=' + pm(A30) + '$', r'$B=\begin{pmatrix}1 & a & b\\ 0 & 1 & c\\ 0 & 0 & 1\end{pmatrix}$ \ ($a$, $b$, $c$ reales)'])
     + recorda(r"$A^{-1}=\dfrac{1}{|A|}\big(\mathrm{Adj}(A)\big)^t$, y solo existe si $|A|\neq0$."),
     tasks(1, [invpas(A30) + r"(Comprueba que $A\cdot A^{-1}=I$.)",
               r"$|B|=1$ para todos los valores de $a$, $b$, $c$. \ $\mathrm{Adj}(B)=\begin{pmatrix}1 & 0 & 0\\ -a & 1 & 0\\ ac-b & -c & 1\end{pmatrix}$, \ \ $\res{B^{-1}=\begin{pmatrix}1 & -a & ac-b\\ 0 & 1 & -c\\ 0 & 0 & 1\end{pmatrix}}$"])),
 (2, r"Dada \ $A=\begin{pmatrix}m & 1 & 0\\ 0 & m & 1\\ 0 & 0 & m\end{pmatrix}$, halla para qué valores de $m$ tiene inversa y calcúlala en función de $m$.",
     r"$|A|=m^3$: tiene inversa si \ $\res{m\neq0}$. \ $\mathrm{Adj}(A)=\begin{pmatrix}m^2 & 0 & 0\\ -m & m^2 & 0\\ 1 & -m & m^2\end{pmatrix}$, \ y"
     + dm(r'A^{-1}=\frac{1}{m^3}\begin{pmatrix}m^2 & -m & 1\\ 0 & m^2 & -m\\ 0 & 0 & m^2\end{pmatrix}=\boxed{\begin{pmatrix}\frac1m & -\frac1{m^2} & \frac1{m^3}\\[2pt] 0 & \frac1m & -\frac1{m^2}\\[2pt] 0 & 0 & \frac1m\end{pmatrix}}')),
 (2, r"Dada \ $M=\begin{pmatrix}1 & k & 0\\ k & 1 & k\\ 0 & k & 1\end{pmatrix}$:" + tasks(1, [r"¿Para qué valores de $k$ tiene inversa?", r"Calcula $M^{-1}$ para $k=1$."]),
     tasks(1, [r"$|M|=1-k^2-k^2=1-2k^2$, que se anula si $k^2=\frac12$: \ tiene inversa si \ $\res{k\neq\pm\tfrac{\sqrt2}{2}}$", invpas(K32(1), 'M')])),
 (3, r"Sea $N$ una matriz cuadrada tal que $N^3=O$." + tasks(1, [r"Demuestra que $I-N$ tiene inversa y que $(I-N)^{-1}=I+N+N^2$.", r"Utilízalo para calcular la inversa de \ $" + pm(sub(eye(3), N33)) + r"$."]),
     tasks(1, [r"$(I-N)(I+N+N^2)=I+N+N^2-N-N^2-N^3=I-N^3=I$ (e igual en el otro orden).",
               r"Es $I-N$ con $N=" + pm(N33) + r"$, $N^2=" + pm(pw(N33, 2)) + r"$, $N^3=O$: \ $(I-N)^{-1}=I+N+N^2=\res{" + pm(inv(sub(eye(3), N33))) + r"}$"])),
 (3, r"Sea \ $A=" + pm(A34) + r"$." + tasks(1, [r"Comprueba que $A^2=A+2I$.", r"Deduce que $A$ es invertible y expresa $A^{-1}$ en función de $A$ y de $I$.", r"Expresa $A^3$ y $A^4$ en la forma $\alpha A+\beta I$.",
     r"Haz el mismo razonamiento para calcular la inversa de la matriz del ejercicio \ref{ex:pq}."]),
     tasks(1, [r"$A^2=" + pm(pw(A34, 2)) + r"=A+2I$", r"$A^2-A=2I\Rightarrow A\cdot\frac{A-I}{2}=I$: \ $\res{A^{-1}=\tfrac12(A-I)=" + pm(inv(A34)) + r"}$",
               r"$A^3=A^2+2A=\res{3A+2I}$; \ \ $A^4=3A^2+2A=\res{5A+6I}$",
               r"$A^2=5A+2I\Rightarrow A(A-5I)=2I$: \ $A^{-1}=\tfrac12(A-5I)=\res{" + pm(inv(A13)) + r"}$"])),
 (3, r"Demuestra las propiedades siguientes de matrices invertibles:" + tasks(1, [r"$(A^t)^{-1}=(A^{-1})^t$.", r"Si $A$ es simétrica e invertible, $A^{-1}$ también es simétrica.",
     r"Una matriz es \emph{ortogonal} si $A\cdot A^t=I$. Comprueba que \ $Q=\frac13" + pm([[1, 2, 2], [2, 1, -2], [2, -2, 1]]) + r"$ \ es ortogonal y escribe $Q^{-1}$ sin hacer ningún cálculo más."]),
     tasks(1, [r"$A^t\cdot(A^{-1})^t=(A^{-1}A)^t=I^t=I$: por tanto, $(A^{-1})^t$ es la inversa de $A^t$.", r"$(A^{-1})^t=(A^t)^{-1}=A^{-1}$.",
               r"$Q\cdot Q^t=\frac19" + pm(mul([[1, 2, 2], [2, 1, -2], [2, -2, 1]], tr([[1, 2, 2], [2, 1, -2], [2, -2, 1]]))) + r"=I$. \ Entonces $Q^{-1}=Q^t$, y como $Q$ es simétrica: \ $\res{Q^{-1}=Q}$"])),
]))

# =====================================================================
A36, B36 = [[3, 1, 0], [0, 3, 1], [1, 0, 2]], [[1, 0], [2, 1], [0, -1]]
N36 = sub(A36, sc(2, eye(3))); ck(det(N36) == 1)
X36 = sc(-1, mul(inv(N36), B36)); ck(eq(add(mul(A36, X36), B36), sc(2, X36)))
A37, B37 = [[0, 1, 0], [1, 1, 1], [0, 0, 0]], [[1, 2, 1], [0, 1, -1]]
N37 = add(A37, eye(3)); ck(det(N37) == 1)
X37 = mul(B37, inv(N37)); ck(eq(add(mul(X37, A37), X37), B37))
A38, B38 = [[1, 1], [1, 2]], [[2, 1], [1, 1]]
X38 = mul(mul(A38, inv(B38)), A38); ck(eq(mul(mul(A38, inv(X38)), A38), B38))
A39, B39, X39 = N36, [[2, 1], [1, 1]], [[1, 0], [-1, 2], [0, 1]]
C39 = mul(mul(A39, X39), B39); ck(eq(mul(mul(inv(A39), C39), inv(B39)), X39))
A40, B40, B40b = [[1, 0], [2, 1], [1, 1]], [[1, 2], [3, 5], [2, 3]], [[1, 2], [3, 5], [2, 4]]
ck(eq(mul(A40, [[1, 2], [1, 1]]), B40))
A41 = lambda m: [[1, 0, 1], [0, m, 0], [1, 0, m]]
for x in G: ck(det(A41(x)) == x * (x - 1))
B41 = mul(pw(A41(2), 2), [[1], [1], [-1]]); ck(eq(B41, [[-1], [4], [-2]]))
A42 = [[4, 1], [2, 3]]
for al in G: ck((det(sub(A42, sc(al, eye(2)))) == 0) == (al in (2, 5)))
ck(eq(mul(A42, [[1], [1]]), [[5], [5]])); ck(eq(mul(A42, [[1], [-2]]), [[2], [-4]]))
A43, X43, Y43 = [[1, 2], [0, 1]], [[1, 1], [0, 2]], [[2, 0], [-1, 1]]
C43, D43 = add(mul(A43, X43), Y43), sub(X43, Y43)
N43 = add(A43, eye(2)); ck(eq(mul(inv(N43), add(C43, D43)), X43))
S.append(("Ecuaciones y sistemas matriciales", [
 (2, r"\label{ex:axb}Resuelve la ecuación $AX+B=2X$, siendo \ $A=" + pm(A36) + r"$ \ y \ $B=" + pm(B36) + r"$."
     + recorda(r"Para sacar factor común $X$ hay que escribir $2X=2IX$; y hay que poner el factor por el lado correcto: \ $AX-2IX=(A-2I)X$."),
     r"$AX-2IX=-B\Rightarrow(A-2I)X=-B\Rightarrow X=-(A-2I)^{-1}B$." + dm(r'A-2I=' + pm(N36) + r',\quad|A-2I|=1,\quad(A-2I)^{-1}=' + pm(inv(N36)))
     + dm(r'X=-' + pm(inv(N36)) + pm(B36) + r'=\boxed{' + pm(X36) + '}')),
 (2, r"Resuelve la ecuación $XA+X=B$, siendo \ $A=" + pm(A37) + r"$ \ y \ $B=" + pm(B37) + r"$. ¿Qué orden debe tener $X$?",
     r"$X$ debe ser $2\times3$. \ $X(A+I)=B\Rightarrow X=B(A+I)^{-1}$, \ con $|A+I|=1$ y $(A+I)^{-1}=" + pm(inv(N37)) + r"$:" + dm(r'X=' + pm(B37) + pm(inv(N37)) + r'=\boxed{' + pm(X37) + '}')),
 (3, r"Resuelve la ecuación $A\,X^{-1}A=B$, siendo \ $A=" + pm(A38) + r"$ \ y \ $B=" + pm(B38) + r"$.",
     r"$X^{-1}=A^{-1}BA^{-1}$ \ e, invirtiendo, \ $X=(A^{-1}BA^{-1})^{-1}=AB^{-1}A$. \ Con $B^{-1}=" + pm(inv(B38)) + r"$:" + dm(r'X=' + pm(A38) + pm(inv(B38)) + pm(A38) + r'=\boxed{' + pm(X38) + '}')),
 (3, r"Resuelve la ecuación $AXB=C$, siendo \ $A=" + pm(A39) + r"$, \ $B=" + pm(B39) + r"$ \ y \ $C=" + pm(C39) + r"$. \ (La inversa de $A$ ya la has calculado en el ejercicio \ref{ex:axb}: es la matriz $A-2I$.)",
     r"$X=A^{-1}CB^{-1}$, con $B^{-1}=" + pm(inv(B39)) + r"$:" + dm(r'X=' + pm(inv(A39)) + pm(C39) + pm(inv(B39)) + '=' + pm(mul(inv(A39), C39)) + pm(inv(B39)) + r'=\boxed{' + pm(X39) + '}')),
 (3, r"Sea \ $A=" + pm(A40) + r"$." + tasks(1, [r"Resuelve la ecuación $AX=" + pm(B40) + r"$.", r"Resuelve la ecuación $AX=" + pm(B40b) + r"$."]) + r"(¡Atención: $A$ no es cuadrada!)",
     r"$X$ debe ser $2\times2$: \ $X=\begin{pmatrix}x & y\\ z & t\end{pmatrix}$, \ $AX=\begin{pmatrix}x & y\\ 2x+z & 2y+t\\ x+z & y+t\end{pmatrix}$."
     + tasks(1, [r"$x=1$, $y=2$, $2x+z=3\Rightarrow z=1$, $2y+t=5\Rightarrow t=1$; y la 3.ª fila también se cumple: $x+z=2$, $y+t=3$. \ $\res{X=" + pm([[1, 2], [1, 1]]) + r"}$",
                 r"Las dos primeras filas dan la misma $X$, pero entonces $y+t=3\neq4$: \ \rest{no tiene solución}."])),
 (3, r"Dadas \ $A=\begin{pmatrix}1 & 0 & 1\\ 0 & m & 0\\ 1 & 0 & m\end{pmatrix}$ \ y \ $B=" + pm(B41) + r"$:" + tasks(1, [r"¿Para qué valores de $m$ la ecuación $A^2X=B$ tiene una única solución?", r"Resuélvela para $m=2$."]),
     tasks(1, [r"$|A^2|=|A|^2$ y $|A|=m^2-m=m(m-1)$: hay solución única ($X=(A^2)^{-1}B$) si \ $\res{m\neq0\ \text{y}\ m\neq1}$",
               r"$A^2=" + pm(pw(A41(2), 2)) + r"$, \ $|A^2|=" + q(det(pw(A41(2), 2))) + r"$, \ $(A^2)^{-1}=\frac14" + pm(tr(adjm(pw(A41(2), 2)))) + r"$:"
               + dm(r'X=\frac14' + pm(tr(adjm(pw(A41(2), 2)))) + pm(B41) + r'=\boxed{' + pm(mul(inv(pw(A41(2), 2)), B41)) + '}')])),
 (3, r"Sea \ $A=" + pm(A42) + r"$ \ y sea $X=\begin{pmatrix}x\\ y\end{pmatrix}$." + tasks(1, [r"¿Para qué valores de $\alpha$ la ecuación $AX=\alpha X$ tiene soluciones distintas de $X=\begin{pmatrix}0\\ 0\end{pmatrix}$?",
     r"Halla todas las soluciones para cada uno de estos valores.", r"Sin calcular $A^{100}$, calcula $A^{100}\begin{pmatrix}1\\ 1\end{pmatrix}$."]),
     tasks(1, [r"$AX=\alpha X\iff(A-\alpha I)X=O$. Si $|A-\alpha I|\neq0$, multiplicando por $(A-\alpha I)^{-1}$ queda $X=O$. Por tanto, hace falta \ $|A-\alpha I|=(4-\alpha)(3-\alpha)-2=\alpha^2-7\alpha+10=0$: \ $\res{\alpha=2;\ \alpha=5}$",
               r"$\alpha=5$: \ $\begin{pmatrix}-1 & 1\\ 2 & -2\end{pmatrix}X=O\Rightarrow y=x$: \ $\res{X=\begin{pmatrix}t\\ t\end{pmatrix}}$. \ \ $\alpha=2$: \ $\begin{pmatrix}2 & 1\\ 2 & 1\end{pmatrix}X=O\Rightarrow y=-2x$: \ $\res{X=\begin{pmatrix}t\\ -2t\end{pmatrix}}$, \ $t\in\mathbb{R}$.",
               r"$A\begin{pmatrix}1\\ 1\end{pmatrix}=5\begin{pmatrix}1\\ 1\end{pmatrix}\Rightarrow A^2\begin{pmatrix}1\\ 1\end{pmatrix}=5A\begin{pmatrix}1\\ 1\end{pmatrix}=5^2\begin{pmatrix}1\\ 1\end{pmatrix}\Rightarrow\dots\Rightarrow A^{100}\begin{pmatrix}1\\ 1\end{pmatrix}=\res{\begin{pmatrix}5^{100}\\ 5^{100}\end{pmatrix}}$"])),
 (3, r"Resuelve el sistema matricial \ $\left\{\begin{aligned}AX+Y&=" + pm(C43) + r"\\ X-Y&=" + pm(D43) + r"\end{aligned}\right.$ \ siendo \ $A=" + pm(A43) + r"$.",
     r"Sumando las dos ecuaciones: \ $AX+X=(A+I)X=" + pm(add(C43, D43)) + r"$. \ $A+I=" + pm(N43) + r"$, \ $(A+I)^{-1}=" + pd(inv(N43)) + r"$:"
     + dm(r'X=' + pd(inv(N43)) + pm(add(C43, D43)) + r'=\boxed{' + pm(X43) + r'},\qquad Y=X-' + pm(D43) + r'=\boxed{' + pm(Y43) + '}')),
]))

# =====================================================================
M45 = [[0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 0]]
M45_2 = pw(M45, 2); P45 = add(M45, M45_2); pts45 = [sum(r) for r in P45]
ck(pts45 == [5, 4, 2, 3], pts45)
A46, x46 = [[F(2, 10), F(3, 10)], [F(4, 10), F(1, 10)]], [[100], [80]]
d46 = sub(x46, mul(A46, x46)); ck(eq(d46, [[56], [32]])); ck(eq(mul(inv(sub(eye(2), A46)), d46), x46))
H = [[2, 1], [3, 2]]; msg = [[13, 1], [20, 5], [19, 0]]
cod = [mul(H, [[a], [b]]) for a, b in msg]; ck([c[0][0] for c in cod] == [27, 45, 38] and [c[1][0] for c in cod] == [41, 70, 57])
ck(eq(inv(H), [[2, -1], [-3, 2]]))
ck(isz(mul(R3, R3)) and not isz(R3)); ck(det(sc(2, eye(2))) == 4)
S.append(("Problemas y cuestiones", [
 (2, r"En una liga de cuatro equipos (A, B, C y D), cada equipo juega una vez contra cada uno de los otros y no hay empates. A gana a B y a C; B gana a C y a D; C gana a D, y D gana a A."
     + tasks(1, [r"Escribe la matriz $M$ en la que $m_{ij}=1$ si el equipo $i$ ha ganado al equipo $j$, y $m_{ij}=0$ si no.", r"Calcula $M^2$. ¿Qué indica el elemento $(i,j)$ de $M^2$?",
                 r"Para ordenar los equipos, cada equipo obtiene un punto por cada victoria directa y un punto por cada victoria ``indirecta'' (ganar a un equipo que ha ganado a otro). Utiliza $M+M^2$ para hacer la clasificación."]),
     tasks(1, [r"$M=" + pm(M45) + r"$", r"$M^2=" + pm(M45_2) + r"$: el número de victorias indirectas de $i$ sobre $j$ (a través de un tercer equipo).",
               r"$M+M^2=" + pm(P45) + r"$; sumando cada fila: A: %d, B: %d, C: %d, D: %d.\par Clasificación: \rest{1.\textsuperscript{o} A, 2.\textsuperscript{o} B, 3.\textsuperscript{o} D, 4.\textsuperscript{o} C}." % tuple(pts45)])),
 (2, r"Una economía tiene dos sectores, agricultura (1) e industria (2). Para producir 1 € del sector 1 hacen falta 0,20 € del sector 1 y 0,40 € del sector 2; para producir 1 € del sector 2 hacen falta 0,30 € del sector 1 y 0,10 € del sector 2. Si $A=" + pd(A46) + r"$ y $x$ es el vector de producción, la producción que queda para el consumo es $d=x-Ax=(I-A)x$."
     + tasks(1, [r"Si la producción es de 100 y 80 millones de euros, ¿qué parte se destina al consumo?", r"¿Qué producción hace falta para que el consumo sea de 56 y 32 millones? Resuélvelo con $(I-A)^{-1}$."]),
     tasks(1, [r"$d=(I-A)x=" + pd(sub(eye(2), A46)) + pm(x46) + '=' + pm(d46) + r"$: \rest{56 y 32 millones}.",
               r"$|I-A|=0{,}6$, \ $(I-A)^{-1}=\frac{1}{0{,}6}" + pd(tr(adjm(sub(eye(2), A46)))) + r"$, \ $x=(I-A)^{-1}d=\frac{1}{0{,}6}" + pm(mul(tr(adjm(sub(eye(2), A46))), d46)) + '=' + pm(x46) + r"$: \rest{100 y 80 millones} (coherente con el apartado anterior)."])),
 (2, r"Para codificar un mensaje, se sustituye cada letra por su lugar en el alfabeto (A$=1$, B$=2$, \ldots, Z$=26$; espacio $=0$), se agrupan los números de dos en dos en matrices columna y se multiplica cada una por $H=" + pm(H) + r"$. Hemos recibido"
     + dm(pm([[27], [41]]) + r',\quad' + pm([[45], [70]]) + r',\quad' + pm([[38], [57]]))
     + r"Descifra el mensaje. (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z.)",
     r"$|H|=1$, \ $H^{-1}=" + pm(inv(H)) + r"$. \ $H^{-1}\begin{pmatrix}27\\ 41\end{pmatrix}=\begin{pmatrix}13\\ 1\end{pmatrix}$, \ $H^{-1}\begin{pmatrix}45\\ 70\end{pmatrix}=\begin{pmatrix}20\\ 5\end{pmatrix}$, \ $H^{-1}\begin{pmatrix}38\\ 57\end{pmatrix}=\begin{pmatrix}19\\ 0\end{pmatrix}$:"
     r" 13, 1, 20, 5, 19, 0 \ $\to$ \ \rest{MATES}"),
 (3, r"Di si son verdaderas o falsas las afirmaciones siguientes ($A$, $B$, $C$ son matrices cuadradas del mismo orden). Si son verdaderas, demuéstralo; si son falsas, da un contraejemplo."
     + tasks(1, [r"Si $AB=O$, entonces $A=O$ o $B=O$.", r"Si $A$ es invertible y $AB=AC$, entonces $B=C$.", r"$|A+B|=|A|+|B|$.", r"Si $A^2=A$ y $|A|\neq0$, entonces $A=I$.",
                 r"Si $AB=I$, entonces también $BA=I$."]),
     tasks(1, [r"\rest{Falsa}: la matriz $R=" + pm(R3) + r"$ del ejercicio \ref{ex:idem} cumple $R\cdot R=O$ y $R\neq O$.", r"\rest{Verdadera}: multiplicando por $A^{-1}$ por la izquierda, $A^{-1}AB=A^{-1}AC\Rightarrow B=C$.",
               r"\rest{Falsa}: con $A=B=I_2$, \ $|A+B|=|2I_2|=4$, pero $|A|+|B|=2$.", r"\rest{Verdadera}: $A$ tiene inversa; multiplicando $A^2=A$ por $A^{-1}$: $A=I$.",
               r"\rest{Verdadera}: $|A|\cdot|B|=|I|=1$, así que $|A|\neq0$ y existe $A^{-1}$. Entonces $B=A^{-1}AB=A^{-1}$, y $BA=A^{-1}A=I$."])),
]))


# =====================================================================
# Exercicis de la PAU d'altres comunitats autònomes (presos del recull «Ejercicios de matrices en pruebas de acceso a la
# universidad de todas las comunidades autónomas de España», curs 2026/27, de J. A. Martínez García, ebaumatematicas.com).
# Es posen al final de cada secció; els apartats que necessiten continguts posteriors s'han suprimit.
SEC = {t: exs for t, exs in S}
def pau(sec, *exs): SEC[sec].extend(exs)

# --- 1. Definicions i tipus
A_ct, B_ct = [[2, -3, -5], [-1, 4, 5], [1, -3, -4]], [[2, 2, 0], [-1, -1, 0], [1, 2, 1]]
ck(eq(mul(A_ct, B_ct), A_ct) and eq(mul(B_ct, A_ct), B_ct) and eq(pw(A_ct, 2), A_ct) and eq(pw(B_ct, 2), B_ct))
pau("Matrices. Definiciones y tipos",
 (2, r"\pau{Cataluña, ordinaria 2023} Considera las matrices \ $A=" + pm(A_ct) + r"$ \ y \ $B=" + pm(B_ct) + r"$."
     + tasks(1, [r"Calcula $A\cdot B$ y $B\cdot A$.", r"Sean $C$ y $D$ dos matrices cuadradas del mismo orden que cumplen $C\cdot D=C$ y $D\cdot C=D$. Demuestra que $C$ y $D$ son idempotentes."]),
     tasks(1, [r"$A\cdot B=" + pm(mul(A_ct, B_ct)) + r"=\res{A}$, \qquad $B\cdot A=" + pm(mul(B_ct, A_ct)) + r"=\res{B}$",
               r"$C^2=C\cdot C=(CD)\cdot C=C\cdot(DC)=C\cdot D=C$ \ y \ $D^2=(DC)\cdot D=D\cdot(CD)=D\cdot C=D$: \rest{son idempotentes}. (Por el apartado anterior, $A$ y $B$ son un ejemplo.)"])))

# --- 2. Operacions
A_md = [[1, 5], [-1, -3]]
AA_md = add(A_md, pw(A_md, 2))
for a in G:
    for b in G[::3]:
        for c in G[::3]:
            Bm = [[a, b], [b, c]]
            ck(eq(mul(Bm, A_md), mul(AA_md, Bm)) == (b == -a and c == -a))
Ak = A_md
for k in range(2, 12):
    Ak = add(pw(Ak, 2), Ak); ck(eq(Ak, A_md if k % 2 else AA_md))
pau("Operaciones con matrices",
 (3, r"\pau{Madrid, extraordinaria 2025} Dada la matriz \ $A=" + pm(A_md) + r"$:"
     + tasks(1, [r"Halla las matrices simétricas $B$ que verifican $BA=(A+A^2)B$.", r"Con $A_1=A$, se consideran las matrices $A_2=A_1^2+A_1$, $A_3=A_2^2+A_2$, $A_4=A_3^2+A_3$, y así sucesivamente. Halla $A_{2025}$."]),
     tasks(1, [r"$A+A^2=" + pm(AA_md) + r"$.\par Con $B=\begin{pmatrix}a & b\\ b & c\end{pmatrix}$: \ $BA=\begin{pmatrix}a-b & 5a-3b\\ b-c & 5b-3c\end{pmatrix}$, \ $(A+A^2)B=\begin{pmatrix}-3a-5b & -3b-5c\\ a+b & b+c\end{pmatrix}$."
               r"\par Igualando: $4a+4b=0$, $5a=-5c$, \ldots: \ $b=-a$, $c=-a$: \ $\res{B=\begin{pmatrix}a & -a\\ -a & -a\end{pmatrix}}$, \ $a\in\mathbb{R}$.",
               r"$A_2=A^2+A=" + pm(AA_md) + r"$, \ $A_3=A_2^2+A_2=" + pm(pw(AA_md, 2)) + '+' + pm(AA_md) + '=' + pm(add(pw(AA_md, 2), AA_md)) + r"=A$. Las matrices se repiten cada 2: las de índice impar son $A$, y como 2025 es impar:\par $\res{A_{2025}=A=" + pm(A_md) + r"}$"])))

# --- 3. Determinants
for t in G[::2]:
    for r in G[::2]:
        ck(det([[t, t, t], [t, 3 + t, -3 + t], [2, -1, 5]]) == 0); ck(det([[1 + r, r, 3 * r], [2, -1, 1], [r, r, 3 * r]]) == -4 * r)
pau("Determinantes",
 (2, r"\pau{Navarra, ordinaria 2026} Calcula los valores posibles de $r$ y $t$ para que $|A|+|B|=4$, sabiendo que"
     + dm(r"A=\begin{pmatrix}t & t & t\\ t & 3+t & -3+t\\ 2 & -1 & 5\end{pmatrix},\qquad B=\begin{pmatrix}1+r & r & 3r\\ 2 & -1 & 1\\ r & r & 3r\end{pmatrix}"),
     r"En $|A|$, hacemos $F_2-F_1$: \ $|A|=\begin{vmatrix}t & t & t\\ 0 & 3 & -3\\ 2 & -1 & 5\end{vmatrix}=t\,(15-3)-t\,(0+6)+t\,(0-6)=0$ para todo $t$."
     r"\par En $|B|$, hacemos $F_1-F_3$: \ $|B|=\begin{vmatrix}1 & 0 & 0\\ 2 & -1 & 1\\ r & r & 3r\end{vmatrix}=-3r-r=-4r$."
     r"\par $0-4r=4$: \ $\res{r=-1}$ \ y \ \rest{$t$ cualquiera}."))

# --- 4. Propietats dels determinants
for al in G[::2]:
    for be in G[::2]:
        A_ad = [[al, be, 1], [2, al, be], [3, 4, al]]
        ck(det([[-3, -4, -al], [al - 2, be - al, 1 - be], [8, 4 * al, 4 * be]]) == -4 * det(A_ad))
        if det(A_ad) != 0: ck(det(mul(mul(inv(A_ad), pw(tr(A_ad), 2)), A_ad)) == det(A_ad) ** 2)
M_cl = rnd3(-2); (a, b, c), (d_, e, f), (g, h, i_) = M_cl
ck(det([[g - 5 * a, 2 * d_, a], [2 * h - 10 * b, 4 * e, 2 * b], [i_ - 5 * c, 2 * f, c]]) == 8)
for t in G:
    A_nv = [[t + 1, t * t, 2], [t + 1, t * t + t - 2, 2 - t], [t + 1, t * t, 4]]; B_nv = [[t, 3 * t, t * t - 1], [0, t, 2 - t], [t, 4 * t, t * t]]
    ck(det(A_nv) == 2 * (t + 1) * (t - 2)); ck(det(B_nv) == t * t * (t - 1))
ck(det(sc(3, mul(pw(tr(A20), 2), inv(mul(A20, B20))))) == 27 * F(4) / (2 * F(-1, 2)))  # comprovació de la regla amb |A|=2, |B|=-1/2
for x in G: ck(det([[2, 1, 1], [0, -1, x], [-1, -1, 0]]) == x - 1)
r3 = 3 ** .5
O1, O2 = [[r3 / 2, .5], [-.5, r3 / 2]], [[r3 / 2, .5], [-.5, -r3 / 2]]
def mulf(A, B): return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def trf(A): return [list(r) for r in zip(*A)]
ck(all(abs(v - w) < 1e-12 for r, s in zip(mulf(O1, trf(O1)), [[1, 0], [0, 1]]) for v, w in zip(r, s)))
ck(abs(mulf(O2, trf(O2))[0][1] + r3 / 2) < 1e-12)
pau("Propiedades de los determinantes",
 (2, r"\pau{Andalucía, ordinaria 2026} Considera la matriz \ $A=\begin{pmatrix}\alpha & \beta & 1\\ 2 & \alpha & \beta\\ 3 & 4 & \alpha\end{pmatrix}$, \ que cumple $|A|=-2$."
     + tasks(1, [r"Calcula \ $\begin{vmatrix}-3 & -4 & -\alpha\\ \alpha-2 & \beta-\alpha & 1-\beta\\ 8 & 4\alpha & 4\beta\end{vmatrix}$.", r"Calcula \ $\left|A^{-1}\left(A^t\right)^2A\right|$."]),
     tasks(1, [r"Las filas son $-F_3$, \ $F_1-F_2$ \ y \ $4F_2$. Sacamos los factores $-1$ y $4$, sumamos la 3.ª fila a la 2.ª y hacemos dos cambios de filas:"
               + dm(r"-4\,\begin{vmatrix}F_3\\ F_1-F_2\\ F_2\end{vmatrix}=-4\,\begin{vmatrix}F_3\\ F_1\\ F_2\end{vmatrix}=-4\,|A|=-4\cdot(-2)=\boxed{8}"),
               r"$\dfrac{1}{|A|}\cdot|A|^2\cdot|A|=|A|^2=\res{4}$"])),
 (2, r"\pau{Castilla y León, extraordinaria 2026} Si \ $\begin{vmatrix}a & b & c\\ d & e & f\\ g & h & i\end{vmatrix}=-2$, \ calcula el valor de \ $\begin{vmatrix}g-5a & 2d & a\\ 2h-10b & 4e & 2b\\ i-5c & 2f & c\end{vmatrix}$.",
     r"Sacamos el factor 2 de la 2.ª fila y el factor 2 de la 2.ª columna, y hacemos $C_1+5C_3$:"
     + dm(r"4\begin{vmatrix}g & d & a\\ h & e & b\\ i & f & c\end{vmatrix}=4\begin{vmatrix}g & h & i\\ d & e & f\\ a & b & c\end{vmatrix}=-4\begin{vmatrix}a & b & c\\ d & e & f\\ g & h & i\end{vmatrix}=-4\cdot(-2)=\boxed{8}")
     + r"(hemos traspuesto y, después, hemos intercambiado $F_1$ y $F_3$)."),
 (2, r"\pau{Navarra, extraordinaria 2025} Sean $A$ y $B$ dos matrices cuadradas $3\times3$ tales que $|A|=\tfrac13$ y $|B|=3$. Calcula $|C|$ sabiendo que \ $C=3\cdot\left(A^t\right)^2\cdot(A\cdot B)^{-1}$.",
     r"$|C|=3^3\cdot|A|^2\cdot\dfrac{1}{|A|\cdot|B|}=27\cdot\dfrac19\cdot\dfrac{1}{\frac13\cdot3}=\res{3}$"),
 (3, r"\pau{Asturias, extraordinaria 2025} Una matriz $M$ verifica que $|M|=x$. (Los apartados son independientes.)"
     + tasks(1, [r"Supongamos que $M$ es $2\times2$ y que $M^2=(x-1)I$. Calcula todos los valores posibles de $x$.",
                 r"Supongamos que \ $M=\begin{pmatrix}2 & 1 & 1\\ 0 & -1 & x\\ -1 & -1 & 0\end{pmatrix}$. ¿Existe algún valor de $x$ para el que sea $|M|=x$?",
                 r"Supongamos que $M$ es $3\times3$, que $x\neq0$ y que $M=xM^2$. Calcula los valores posibles de $x$ y de $|M^{-1}|$."]),
     tasks(1, [r"$|M^2|=|M|^2=x^2$ \ y \ $|(x-1)I_2|=(x-1)^2$: \ $x^2=x^2-2x+1$: \ $\res{x=\tfrac12}$",
               r"$|M|=2(0+x)-1(0+x)+1(0-1)=x-1$, y $x-1=x$ no tiene solución: \rest{no existe ninguno}.",
               r"$|M|=x^3|M|^2\Rightarrow x=x^3\cdot x^2=x^5\Rightarrow x^4=1$: \ $\res{x=1,\ |M^{-1}|=1}$ \ o \ $\res{x=-1,\ |M^{-1}|=-1}$"])),
 (2, r"\pau{Murcia, extraordinaria 2024} Una matriz cuadrada $A$ de orden 2 es \emph{ortogonal} si $A\cdot A^t=I$."
     + tasks(1, [r"Estudia si son ortogonales las matrices \ $\begin{pmatrix}\sqrt3/2 & 1/2\\ -1/2 & \sqrt3/2\end{pmatrix}$ \ y \ $\begin{pmatrix}\sqrt3/2 & 1/2\\ -1/2 & -\sqrt3/2\end{pmatrix}$.",
                 r"Si $A$ es una matriz ortogonal cualquiera de orden 2, calcula razonadamente su determinante.", r"Justifica que, si $A$ y $B$ son ortogonales de orden 2, el producto $C=A\cdot B$ también lo es."]),
     tasks(1, [r"La 1.ª: $\begin{pmatrix}\frac34+\frac14 & -\frac{\sqrt3}4+\frac{\sqrt3}4\\ -\frac{\sqrt3}4+\frac{\sqrt3}4 & \frac14+\frac34\end{pmatrix}=I$: \rest{es ortogonal}. La 2.ª: el elemento $(1,2)$ del producto es $-\frac{\sqrt3}4-\frac{\sqrt3}4=-\frac{\sqrt3}{2}\neq0$: \rest{no lo es}.",
               r"$|A|\cdot|A^t|=|A|^2=|I|=1$: \ $\res{|A|=\pm1}$", r"$C\cdot C^t=AB\,B^tA^t=A\,(BB^t)\,A^t=A\,I\,A^t=AA^t=I$."])),
 (3, r"\pau{Navarra, extraordinaria 2026} Dadas las matrices siguientes, calcula $\left|A\cdot B^{-1}\right|$ en función del parámetro $t$. ¿Para qué valores de $t$ no existe $\left|A\cdot B^{-1}\right|$?"
     + dm(r"A=\begin{pmatrix}t+1 & t^2 & 2\\ t+1 & t^2+t-2 & 2-t\\ t+1 & t^2 & 4\end{pmatrix},\qquad B=\begin{pmatrix}t & 3t & t^2-1\\ 0 & t & 2-t\\ t & 4t & t^2\end{pmatrix}"),
     r"En $|A|$ sacamos $t+1$ de la 1.ª columna y hacemos $F_2-F_1$, $F_3-F_1$:"
     + dm(r"|A|=(t+1)\begin{vmatrix}1 & t^2 & 2\\ 0 & t-2 & -t\\ 0 & 0 & 2\end{vmatrix}=2(t+1)(t-2)")
     + r"En $|B|$ sacamos $t$ de la 1.ª columna y hacemos $F_3-F_1$:"
     + dm(r"|B|=t\begin{vmatrix}1 & 3t & t^2-1\\ 0 & t & 2-t\\ 0 & t & 1\end{vmatrix}=t\,\big(t-t(2-t)\big)=t^2(t-1)")
     + r"$\left|AB^{-1}\right|=\dfrac{|A|}{|B|}=\res{\dfrac{2(t+1)(t-2)}{t^2(t-1)}}$, \ que no existe si $B$ no tiene inversa: \ $\res{t=0\ \text{o}\ t=1}$"))

# --- 5. Rang
for a in G:
    Mc = [[a, a - 1, a * a - a], [a, 1, a], [a, 1, a - 1]]
    ck(det(Mc) == a * (a - 2)); ck(rank(Mc) == (2 if a in (0, 2) else 3))
for m_ in G:
    Mp = [[1, 3, 4, 1], [m_, 2 - m_, 2, 1], [m_, -2, m_ - 2, 1]]
    ck(rank(Mp) == (2 if m_ in (1, 4) else 3))
    ck(det([[1, 3, 1], [m_, 2 - m_, 1], [m_, -2, 1]]) == (m_ - 1) * (m_ - 4))
A_bl = [[1, 0, 0], [2, 0, 0], [-2, 1, 1]]
for k in G: ck(rank(sub(sc(3, A_bl), sc(k, eye(3)))) == (2 if k == 0 else 1 if k == 3 else 3)); ck(det(sub(sc(3, A_bl), sc(k, eye(3)))) == -k * (3 - k) ** 2)
for a in G:
    Ac, Bc = [[-1, 1], [1, 2], [1, a]], [[1, a, 0], [3, 0, 2]]
    ck(rank(mul(Ac, Bc)) == 2 and det(mul(Ac, Bc)) == 0); ck(det(mul(Bc, Ac)) == (2 * a - 1) * (a + 2)); ck(rank(mul(Bc, Ac)) == (1 if a in (F(1, 2), -2) else 2))
for a in G:
    A_as = [[-1, 2, -2], [0, 3, -4], [a, 2, -3]]
    ck(eq(pw(A_as, 2), eye(3)) == (a == 0)); ck(det(A_as) == 1 - 2 * a); ck(rank(A_as) == (2 if a == F(1, 2) else 3))
pau("Rango de una matriz",
 (2, r"\pau{Castilla-La Mancha, extraordinaria 2026} Estudia el rango de la matriz siguiente en función del parámetro real $a$: \ $A=\begin{pmatrix}a & a-1 & a^2-a\\ a & 1 & a\\ a & 1 & a-1\end{pmatrix}$.",
     r"Hacemos $F_2-F_3$: la 2.ª fila queda $(0\ 0\ 1)$, y desarrollando por esta fila: \ $|A|=-\begin{vmatrix}a & a-1\\ a & 1\end{vmatrix}=-(a-a^2+a)=a(a-2)$."
     + tasks(1, [r"Si $a\neq0$ y $a\neq2$: \ $\res{\operatorname{rg}(A)=3}$", r"Si $a=0$: \ $A=\begin{pmatrix}0 & -1 & 0\\ 0 & 1 & 0\\ 0 & 1 & -1\end{pmatrix}$ y $\begin{vmatrix}1 & 0\\ 1 & -1\end{vmatrix}\neq0$: \ $\res{\operatorname{rg}(A)=2}$",
                 r"Si $a=2$: \ $A=\begin{pmatrix}2 & 1 & 2\\ 2 & 1 & 2\\ 2 & 1 & 1\end{pmatrix}$ y $\begin{vmatrix}1 & 2\\ 1 & 1\end{vmatrix}\neq0$: \ $\res{\operatorname{rg}(A)=2}$"])),
 (3, r"\pau{País Vasco, extraordinaria 2024} Calcula el rango de la matriz $A$ según los valores del parámetro $m$: \ $A=\begin{pmatrix}1 & 3 & 4 & 1\\ m & 2-m & 2 & 1\\ m & -2 & m-2 & 1\end{pmatrix}$.",
     r"$\begin{vmatrix}1 & 3 & 1\\ m & 2-m & 1\\ m & -2 & 1\end{vmatrix}$ (columnas 1.ª, 2.ª y 4.ª) $=(m-1)(m-4)$." + tasks(1, [r"Si $m\neq1$ y $m\neq4$: \ $\res{\operatorname{rg}(A)=3}$",
     r"Si $m=1$: \ $A=" + pm([[1, 3, 4, 1], [1, 1, 2, 1], [1, -2, -1, 1]]) + r"$; los cuatro menores de orden 3 son nulos ($F_3=\tfrac52F_2-\tfrac32F_1$) y $\begin{vmatrix}1 & 3\\ 1 & 1\end{vmatrix}\neq0$: \ $\res{\operatorname{rg}(A)=2}$",
     r"Si $m=4$: \ $A=" + pm([[1, 3, 4, 1], [4, -2, 2, 1], [4, -2, 2, 1]]) + r"$, dos filas iguales y $\begin{vmatrix}1 & 3\\ 4 & -2\end{vmatrix}\neq0$: \ $\res{\operatorname{rg}(A)=2}$"])),
 (2, r"\pau{Islas Baleares, extraordinaria 2024} Sea $I_3$ la matriz identidad de orden 3 y \ $A=" + pm(A_bl) + r"$." + tasks(1, [r"Calcula la matriz $B=3A-kI_3$ en función del parámetro real $k$.", r"Discute el rango de $B$ según el parámetro $k$."]),
     tasks(1, [r"$\res{B=\begin{pmatrix}3-k & 0 & 0\\ 6 & -k & 0\\ -6 & 3 & 3-k\end{pmatrix}}$",
               r"Es triangular: $|B|=-k(3-k)^2$. \ Si $k\neq0$ y $k\neq3$: \ $\res{\operatorname{rg}(B)=3}$. \ Si $k=0$: $B=" + pm(sc(3, A_bl)) + r"$, \ $\res{\operatorname{rg}(B)=2}$. \ Si $k=3$: $B=" + pm(sub(sc(3, A_bl), sc(3, eye(3)))) + r"$, \ $\res{\operatorname{rg}(B)=1}$"])),
 (3, r"\pau{Cantabria, extraordinaria 2025} Considera las matrices \ $A=\begin{pmatrix}-1 & 1\\ 1 & 2\\ 1 & a\end{pmatrix}$ \ y \ $B=\begin{pmatrix}1 & a & 0\\ 3 & 0 & 2\end{pmatrix}$, con $a\in\mathbb{R}$."
     + tasks(1, [r"Estudia el rango de $AB$ en función de los valores de $a$.", r"Estudia el rango de $BA$ en función de los valores de $a$."]),
     tasks(1, [r"$AB=\begin{pmatrix}2 & -a & 2\\ 7 & a & 4\\ 1+3a & a & 2a\end{pmatrix}$. Por Sarrus, $|AB|=4a^2-4a(1+3a)+14a-2a(1+3a)-8a+14a^2=0$ para cualquier $a$, y el menor $\begin{vmatrix}2 & 2\\ 7 & 4\end{vmatrix}=-6\neq0$: \ $\res{\operatorname{rg}(AB)=2}$ para todo $a$.",
               r"$BA=\begin{pmatrix}a-1 & 1+2a\\ -1 & 3+2a\end{pmatrix}$, \ $|BA|=(a-1)(3+2a)+1+2a=2a^2+3a-2=(2a-1)(a+2)$. \ Si $a\neq\tfrac12$ y $a\neq-2$: \ $\res{\operatorname{rg}(BA)=2}$; \ si $a=\tfrac12$ o $a=-2$: \ $\res{\operatorname{rg}(BA)=1}$ (no es la matriz nula)."])),
 (3, r"\pau{Asturias, ordinaria 2026} Para cada $a\in\mathbb{R}$ se considera la matriz \ $A=\begin{pmatrix}-1 & 2 & -2\\ 0 & 3 & -4\\ a & 2 & -3\end{pmatrix}$."
     + tasks(1, [r"Calcula todos los valores de $a$ que hacen que $A^2=I$.", r"Si una matriz $B$ de tamaño $3\times3$ verifica $B^2=2I$, ¿qué valores puede tomar $\det(B)$?", r"Calcula el rango y el determinante de $A$ para cada valor de $a$."]),
     tasks(1, [r"$A^2=\begin{pmatrix}1-2a & 0 & 0\\ -4a & 1 & 0\\ -4a & 2a & 1-2a\end{pmatrix}$ (haz el producto), que es $I$ si y solo si \ $\res{a=0}$",
               r"$|B|^2=|2I|=2^3=8$: \ $\res{\det(B)=\pm2\sqrt2}$",
               r"$|A|=-1(-9+8)-2(0+4a)-2(0-3a)=1-2a$. \ Si $a\neq\tfrac12$: \ $\res{\operatorname{rg}(A)=3}$; \ si $a=\tfrac12$: \ $|A|=0$ y $\begin{vmatrix}-1 & 2\\ 0 & 3\end{vmatrix}\neq0$: \ $\res{\operatorname{rg}(A)=2}$"])))
for a in G: ck(eq(pw([[-1, 2, -2], [0, 3, -4], [a, 2, -3]], 2), [[1 - 2 * a, 0, 0], [-4 * a, 1, 0], [-4 * a, 2 * a, 1 - 2 * a]]))
for a in G: ck(eq(mul([[-1, 1], [1, 2], [1, a]], [[1, a, 0], [3, 0, 2]]), [[2, -a, 2], [7, a, 4], [1 + 3 * a, a, 2 * a]]))

# --- 6. Matriu inversa
K_cn = lambda k: [[3, -k, 0], [1, 2, k], [k, 0, k]]
for k in G: ck(det(K_cn(k)) == -k * (k - 3) * (k + 2))
r3, pi = 3 ** .5, math.pi
Mf = [[1, 2, 3, 4], [.5, .5, r3, 0], [1 / 3, 5, 0, -1], [pi, 0, 2, 2]]
Nf = [[0, 3, 4, 2], [.5, -.5, r3, 1], [1 / 3, 5, -1, 0], [pi, 0, 2, 1]]
MN = [[1, -1, -1, 2], [0, 1, 0, -1], [0, 0, 1, -1], [0, 0, 0, 1]]
ck(all(abs(Mf[i][j] - Nf[i][j] - MN[i][j]) < 1e-12 for i in range(4) for j in range(4)))
A_c3, B_c3 = [[2, 1], [3, 2]], [[2, -1], [-3, 2]]
ck(eq(pw(sub(A_c3, sc(2, eye(2))), 2), sc(3, eye(2)))); ck(eq(inv(A_c3), sub(sc(4, eye(2)), A_c3)) and eq(inv(A_c3), B_c3))
X_c3 = mul(inv(A_c3), B_c3); ck(eq(X_c3, [[7, -4], [-12, 7]]))
A_mu = [[0, 0, 1], [0, 0, 0], [0, 0, 0]]
ck(isz(pw(A_mu, 2))); ck(eq(pw(add(A_mu, eye(3)), 2), add(sc(2, A_mu), eye(3))) and eq(pw(add(A_mu, eye(3)), 3), add(sc(3, A_mu), eye(3))))
ck(eq(mul(sub(eye(3), A_mu), add(eye(3), A_mu)), eye(3)))
for al in G: ck(det([[1, al, 1], [0, 1, 1], [0, al, 1]]) == 1 - al)
A_pv = [[1, 0, 1], [0, 1, 1], [0, 0, 1]]
ck(eq(inv(A_pv), [[1, 0, -1], [0, 1, -1], [0, 0, 1]])); ck(eq(pw(A_pv, 2025), [[1, 0, 2025], [0, 1, 2025], [0, 0, 1]]))
A_gl, B_gl = [[1, 0, 1], [0, 2, 0]], [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
X_gl, Y_gl = mul(A_gl, tr(A_gl)), mul(tr(A_gl), A_gl); ck(det(Y_gl) == 0 and det(X_gl) == 8)
for a in range(-2, 3):
    for b in range(-2, 3):
        for c in range(-2, 3): ck(eq(mul(B_gl, [[a], [b], [c]]), [[a], [b], [c]]) == (a == 0 and c == 0))
X_lr = [[1, 1], [1, 2], [1, 1], [1, 3]]
H_lr = sub(eye(4), mul(mul(X_lr, inv(mul(tr(X_lr), X_lr))), tr(X_lr)))
ck(eq(pw(H_lr, 2), H_lr)); ck(eq(sc(11, H_lr), [[6, -2, -5, 1], [-2, 8, -2, -4], [-5, -2, 6, 1], [1, -4, 1, 2]]))
pau("Matriz inversa",
 (2, r"\pau{Canarias, extraordinaria 2026} Dada la matriz \ $A=\begin{pmatrix}3 & -k & 0\\ 1 & 2 & k\\ k & 0 & k\end{pmatrix}$, \ con $k\in\mathbb{R}$:" + tasks(1, [r"Averigua los valores de $k$ para los que $A$ tiene inversa.", r"Calcula la inversa de $A$ cuando $k=1$."]),
     tasks(1, [r"$|A|=6k+k^2-k^3=-k(k^2-k-6)=-k(k-3)(k+2)$: tiene inversa si \ $\res{k\neq0,\ k\neq3\ \text{y}\ k\neq-2}$", invpas(K_cn(1))])),
 (2, r"\pau{Aragón, extraordinaria 2026} Sean $A$, $M$ y $N$ tres matrices cuadradas de orden 4 que satisfacen la condición \ $M\cdot A=I+N\cdot A$."
     + tasks(1, [r"Justifica que $A$ es regular (es decir, invertible).", r"Si \ $M=" + pm([[1, 2, 3, 4], [r'1/2', r'1/2', r'\sqrt3', 0], [r'1/3', 5, 0, -1], [r'\pi', 0, 2, 2]]) + r"$ \ y \ $N=" + pm([[0, 3, 4, 2], [r'1/2', r'-1/2', r'\sqrt3', 1], [r'1/3', 5, -1, 0], [r'\pi', 0, 2, 1]]) + r"$, \ calcula $A^{-1}$."]),
     tasks(1, [r"$MA-NA=I\Rightarrow(M-N)\cdot A=I$: \ $A$ tiene inversa y \ $\res{A^{-1}=M-N}$", r"$A^{-1}=M-N=\res{" + pm(MN) + r"}$"])),
 (2, r"\pau{Cataluña, extraordinaria 2023} Sean \ $A=" + pm(A_c3) + r"$, \ $B=" + pm(B_c3) + r"$ \ y la matriz identidad $I$ de orden 2."
     + tasks(1, [r"Comprueba que $(A-2I)^2=3I$.", r"Utilizando esta igualdad, halla la inversa de $A$ en función de $A$ y de $I$, y comprueba que coincide con $B$.", r"Calcula la matriz $X$ que satisface $A\cdot X=B$."]),
     tasks(1, [r"$A-2I=" + pm(sub(A_c3, sc(2, eye(2)))) + r"$, \ $(A-2I)^2=" + pm(pw(sub(A_c3, sc(2, eye(2))), 2)) + r"=3I$",
               r"$A^2-4A+4I=3I\Rightarrow A^2-4A=-I\Rightarrow A(4I-A)=I$: \ $\res{A^{-1}=4I-A=" + pm(inv(A_c3)) + r"=B}$",
               r"$X=A^{-1}B=B\cdot B=\res{" + pm(X_c3) + r"}$"])),
 (3, r"\pau{Murcia, extraordinaria 2025} Sea $A$ una matriz cuadrada de orden 3 que cumple $A^2=O$, donde $O$ es la matriz nula de orden 3." + tasks(1, [r"Demuestra que $(A+I)^2=2A+I$ y que $(A+I)^3=3A+I$.",
     r"Demuestra que la matriz $I-A$ es la inversa de la matriz $I+A$.", r"Resuelve la ecuación matricial $X+AX=A$, expresando $X$ en función de $A$."]),
     tasks(1, [r"$(A+I)^2=A^2+2A+I=2A+I$; \ \ $(A+I)^3=(2A+I)(A+I)=2A^2+3A+I=3A+I$.", r"$(I+A)(I-A)=I-A+A-A^2=I$ (e igual en el otro orden).",
               r"$(I+A)X=A\Rightarrow X=(I+A)^{-1}A=(I-A)A=A-A^2$: \ $\res{X=A}$"])),
 (2, r"\pau{País Vasco, extraordinaria 2025} Sea $\alpha$ un número real y \ $A=\begin{pmatrix}1 & \alpha & 1\\ 0 & 1 & 1\\ 0 & \alpha & 1\end{pmatrix}$."
     + tasks(1, [r"Halla los valores de $\alpha$ para los que existe la matriz inversa de $A$.", r"En el caso $\alpha=0$, calcula, si es posible, $A^{-1}$ y $A^{2025}$."]),
     tasks(1, [r"$|A|=1\cdot(1-\alpha)$: existe si \ $\res{\alpha\neq1}$",
               invpas(A_pv) + r"$A^2=" + pm(pw(A_pv, 2)) + r"$, \ $A^3=" + pm(pw(A_pv, 3)) + r"$, \ldots \ $\Rightarrow$ \ $A^n=\begin{pmatrix}1 & 0 & n\\ 0 & 1 & n\\ 0 & 0 & 1\end{pmatrix}$, \ \ $\res{A^{2025}=" + pm(pw(A_pv, 2025)) + r"}$"])),
 (2, r"\pau{Galicia, extraordinaria 2026} Dadas las matrices \ $A=" + pm(A_gl) + r"$ \ y \ $B=" + pm(B_gl) + r"$:"
     + tasks(1, [r"Calcula las matrices $X=AA^t$ e $Y=A^tA$. ¿Son invertibles $X$ o $Y$? Razona la respuesta y calcula las inversas cuando sea posible.", r"Calcula las matrices de la forma $M=\begin{pmatrix}a\\ b\\ c\end{pmatrix}$ tales que $BM=M$."]),
     tasks(1, [r"$X=" + pm(X_gl) + r"$, \ $|X|=8\neq0$: \ $\res{X^{-1}=" + pm(inv(X_gl)) + r"}$.\par $Y=" + pm(Y_gl) + r"$ tiene dos filas iguales: \ \rest{$Y$ no es invertible}.",
               r"$BM=\begin{pmatrix}a+c\\ b\\ a+c\end{pmatrix}=\begin{pmatrix}a\\ b\\ c\end{pmatrix}\Rightarrow c=0,\ a=0$: \ $\res{M=\begin{pmatrix}0\\ b\\ 0\end{pmatrix}}$, \ $b\in\mathbb{R}$."])),
 (3, r"\pau{La Rioja, extraordinaria 2026} Dada la matriz \ $X=" + pm(X_lr) + r"$, \ calcula \ $A=I_4-X\left(X^tX\right)^{-1}X^t$ \ y comprueba que es idempotente, es decir, que $A^2=A$. Demuestra después que esto ocurre para cualquier matriz $X$ para la que $X^tX$ sea invertible.",
     r"$X^tX=" + pm(mul(tr(X_lr), X_lr)) + r"$, \ $|X^tX|=" + q(det(mul(tr(X_lr), X_lr))) + r"$, \ $\left(X^tX\right)^{-1}=\frac1{11}" + pm(tr(adjm(mul(tr(X_lr), X_lr)))) + r"$:"
     + dm(r"A=I_4-\frac1{11}" + pm(sc(11, mul(mul(X_lr, inv(mul(tr(X_lr), X_lr))), tr(X_lr)))) + r"=\boxed{\frac1{11}" + pm(sc(11, H_lr)) + "}")
     + r"En general, con $P=X\left(X^tX\right)^{-1}X^t$: \ $P^2=X\left(X^tX\right)^{-1}\left(X^tX\right)\left(X^tX\right)^{-1}X^t=P$, \ y entonces $(I-P)^2=I-2P+P^2=I-P$."))

# --- 7. Equacions i sistemes matricials
A_an, B_an = [[2, 2], [3, 4]], [[3, 1], [2, 2]]
ck(det(A_an) == 2 and det(B_an) == 4); Y_an = mul(inv(A_an), B_an); ck(eq(mul(mul(pw(A_an, 3), Y_an), inv(B_an)), pw(A_an, 2)))
A_cr = [[1, 2, 0], [0, 1, 0], [-1, 1, 1]]
X_cr, Y_cr = sc(F(1, 2), add(A_cr, inv(A_cr))), sc(F(1, 4), sub(A_cr, inv(A_cr)))
ck(eq(add(X_cr, sc(2, Y_cr)), A_cr) and eq(sub(X_cr, sc(2, Y_cr)), inv(A_cr)))
B_cm = [[3, -1, -1], [-1, 1, 0], [-1, 0, 1]]
sol_cm = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if eq(mul([[1, a, 1], [1, 2, 1], [1, 1, b]], B_cm), eye(3))]; ck(sol_cm == [(1, 2)], sol_cm)
P_cm, Q_cm = [[1, 0], [2, 3]], [[4, 1], [7, 9]]
Y_cm = sub(Q_cm, sc(2, P_cm)); X_cm = sub(P_cm, Y_cm); ck(eq(add(X_cm, Y_cm), P_cm) and eq(add(sc(2, X_cm), sc(3, Y_cm)), Q_cm))
A_ex, B_ex = [[0, 2, 3], [2, 3, 5], [1, 3, 1]], [[-1, 0, 1], [0, -1, 1], [2, 1, -3]]
N_ex = add(tr(A_ex), eye(3)); X_ex = mul(inv(N_ex), add(sc(2, B_ex), eye(3)))
ck(eq(inv(N_ex), [[-7, 1, 2], [5, -1, -1], [-2, 1, 0]])); ck(eq(sub(mul(tr(A_ex), X_ex), eye(3)), sub(sc(2, B_ex), X_ex))); ck(eq(X_ex, [[15, 3, -22], [-9, -1, 13], [2, -1, -2]]))
L_md = lambda l: [[1, l - 2, l], [0, 1, l - 1], [1, 0, 1]]
for l in G: ck(det(L_md(l)) == (l - 1) * (l - 3)); ck(rank(L_md(l)) == (2 if l in (1, 3) else 3))
A_m2 = L_md(2); X_m2 = sub(A_m2, inv(A_m2)); ck(eq(sub(pw(A_m2, 2), mul(A_m2, X_m2)), eye(3)))
A_me, B_me, C_me = [[1, 0, 1], [0, 1, 0], [0, 2, 1]], [[2, -1], [1, 0], [-1, -2]], [[1, 0, 0], [-1, 1, 0], [0, -1, 1]]
X_me = mul(inv(add(A_me, eye(3))), B_me); ck(eq(add(mul(A_me, X_me), X_me), B_me)); ck(det(add(A_me, eye(3))) == 8)
P_nv, Q_nv = [[-1, 1], [2, -1]], [[1, 0], [1, 2]]
A_nv2 = mul(inv(Q_nv), inv(P_nv)); ck(eq(mul(mul(Q_nv, A_nv2), P_nv), eye(2))); ck(eq(A_nv2, [[1, 1], [F(1, 2), 0]]))
ck(eq(mul(mul(mul(A_nv2, P_nv), Q_nv), A_nv2), mul(inv(Q_nv), inv(P_nv))))
B_bl, b_bl = [[0, 1, 2], [1, 1, 1], [0, 3, 1]], [[0], [1], [0]]
A_bl2 = inv(sub(eye(3), B_bl)); ck(eq(add(add(mul(A_bl2, B_bl), A_bl2), eye(3)), sc(2, A_bl2)))
x_bl = mul(sub(eye(3), B_bl), b_bl); ck(eq(x_bl, [[-1], [0], [-3]]) and eq(mul(A_bl2, x_bl), b_bl))
for a in G:
    A_ca = [[1, a, 0], [0, 1, 0], [0, 0, a]]
    ck(rank(A_ca) == (2 if a == 0 else 3)); ck(eq(pw(A_ca, 6), [[1, 6 * a, 0], [0, 1, 0], [0, 0, a ** 6]]))
A_c1, C_c1 = [[1, -1, 0], [0, 1, 0], [0, 0, -1]], [[2, 2, 2], [0, 0, -1], [0, -2, -2]]
X_c1 = mul(mul(inv(A_c1), C_c1), A_c1); ck(eq(X_c1, [[2, 0, -1], [0, 0, 1], [0, 2, -2]])); ck(eq(mul(mul(A_c1, X_c1), inv(A_c1)), C_c1))
A_cl, B_cl = [[2, 2, 0], [0, 2, 0], [2, 0, 4]], [[-3, 4, -6], [-2, 1, -2], [-11, 3, -8]]
X_cl = mul(inv(A_cl), sub(sc(F(1, 4), pw(A_cl, 2)), B_cl)); ck(eq(X_cl, [[1, -1, 2], [1, 0, 1], [3, 0, 2]])); ck(eq(sub(sc(F(1, 4), pw(A_cl, 2)), mul(A_cl, X_cl)), B_cl))
A_a4 = [[1, F(1, 8), F(1, 8)], [0, 1, 0], [0, 0, 1]]
for n in range(1, 30): ck(eq(pw(A_a4, n), [[1, F(n, 8), F(n, 8)], [0, 1, 0], [0, 0, 1]]))
X_a4 = sc(-1, pw(inv(A_a4), 3)); ck(eq(add(mul(mul(pw(A_a4, 2), X_a4), A_a4), eye(3)), [[0] * 3] * 3)); ck(eq(X_a4, [[-1, F(3, 8), F(3, 8)], [0, -1, 0], [0, 0, -1]]))
pau("Ecuaciones y sistemas matriciales",
 (2, r"\pau{Andalucía, extraordinaria 2026} Considera las matrices \ $A=" + pm(A_an) + r"$ \ y \ $B=" + pm(B_an) + r"$."
     + tasks(1, [r"Halla razonadamente el determinante de una matriz $X$ que verifica \ $A^3XB^t=5B^2A^{-1}$.", r"Determina, si existe, una matriz $Y$ que verifica \ $A^3YB^{-1}=A^2$."]),
     tasks(1, [r"$|A|=2$, $|B|=4$, y las matrices son de orden 2: \ $|A|^3\,|X|\,|B|=5^2\,|B|^2\,\dfrac{1}{|A|}\Rightarrow8\cdot|X|\cdot4=25\cdot16\cdot\tfrac12$: \ $\res{|X|=\tfrac{25}{4}}$",
               r"$Y=A^{-3}A^2B=A^{-1}B=\frac12" + pm(tr(adjm(A_an))) + pm(B_an) + r"=\res{" + pm(Y_an) + r"}$"])),
 (2, r"\pau{Canarias, ordinaria 2026} Dada la matriz \ $A=" + pm(A_cr) + r"$, \ halla dos matrices cuadradas de orden 3 tales que la primera más el doble de la segunda dé la matriz $A$, y la primera menos el doble de la segunda dé la inversa de $A$.",
     r"$\left\{\begin{aligned}X+2Y&=A\\ X-2Y&=A^{-1}\end{aligned}\right.\Rightarrow X=\tfrac12\left(A+A^{-1}\right),\ \ Y=\tfrac14\left(A-A^{-1}\right)$, \ con $|A|=1$ y $A^{-1}=" + pm(inv(A_cr)) + r"$:"
     + dm(r"X=\boxed{" + pm(X_cr) + r"},\qquad Y=\boxed{" + pm(Y_cr) + "}")),
 (2, r"\pau{Castilla-La Mancha, ordinaria 2026}" + tasks(1, [r"Determina los valores de $a$ y $b$ para que las matrices \ $A=\begin{pmatrix}1 & a & 1\\ 1 & 2 & 1\\ 1 & 1 & b\end{pmatrix}$ \ y \ $B=" + pm(B_cm) + r"$ \ cumplan $A\cdot B=I$.",
     r"Resuelve razonadamente el sistema \ $\left\{\begin{aligned}X+Y&=" + pm(P_cm) + r"\\ 2X+3Y&=" + pm(Q_cm) + r"\end{aligned}\right.$"]),
     tasks(1, [r"$AB=\begin{pmatrix}3-a & a-1 & 0\\ 0 & 1 & 0\\ 2-b & 0 & b-1\end{pmatrix}=I\iff3-a=1,\ a-1=0,\ 2-b=0,\ b-1=1$: \ $\res{a=1;\ b=2}$",
               r"Restando a la 2.ª ecuación el doble de la 1.ª: \ $\res{Y=" + pm(Y_cm) + r"}$, \ y \ $X=" + pm(P_cm) + r"-Y=\res{" + pm(X_cm) + r"}$"])),
 (2, r"\pau{Extremadura, extraordinaria 2025} Sean las matrices" + dm(r"A=" + pm(A_ex) + r",\qquad B=" + pm(B_ex))
     + tasks(1, [r"Obtén la inversa de la matriz $A^t+I$, donde $I$ es la matriz identidad de orden 3.", r"Resuelve la ecuación matricial \ $A^tX-I=2B-X$."]),
     tasks(1, [r"$A^t+I=" + pm(N_ex) + r"$, \ $|A^t+I|=" + q(det(N_ex)) + r"$: \ $\res{\left(A^t+I\right)^{-1}=" + pm(inv(N_ex)) + r"}$",
               r"$A^tX+X=2B+I\Rightarrow(A^t+I)X=2B+I\Rightarrow X=(A^t+I)^{-1}(2B+I)$:" + dm(r"X=" + pm(inv(N_ex)) + pm(add(sc(2, B_ex), eye(3))) + r"=\boxed{" + pm(X_ex) + "}")])),
 (2, r"\pau{Galicia, ordinaria 2026} Considera la igualdad matricial $A(X-I)B=C$, donde $X$ es cuadrada e $I$ es la matriz identidad."
     + tasks(1, [r"Despeja $X$ suponiendo que $A$ y $B$ son cuadradas e invertibles.", r"¿Qué dimensiones tienen $X$ y $B$ si $A$ y $C$ son matrices $1\times2$? Halla $X$, simétrica y con los elementos de la diagonal que suman 0, si $A=(1\ \ 1)$, $B=I$ y $C=(0\ \ 0)$."]),
     tasks(1, [r"$X-I=A^{-1}CB^{-1}$: \ $\res{X=A^{-1}CB^{-1}+I}$",
               r"$A(X-I)$ debe tener sentido, así que $X$ es $2\times2$; y $(1\times2)\cdot B=1\times2$ obliga a que $B$ sea $2\times2$. Con $X=\begin{pmatrix}p & q\\ q & -p\end{pmatrix}$: \ $(1\ \ 1)\begin{pmatrix}p-1 & q\\ q & -p-1\end{pmatrix}=(p-1+q\ \ \ q-p-1)=(0\ \ 0)$"
               r" \ $\Rightarrow$ \ $q=1$, $p=0$: \ $\res{X=\begin{pmatrix}0 & 1\\ 1 & 0\end{pmatrix}}$"])),
 (3, r"\pau{Madrid, ordinaria 2026} Dada la matriz real \ $A=\begin{pmatrix}1 & \lambda-2 & \lambda\\ 0 & 1 & \lambda-1\\ 1 & 0 & 1\end{pmatrix}$:" + tasks(1, [r"Discute el rango de $A$ en función del parámetro $\lambda$.", r"Para el caso $\lambda=2$, resuelve la ecuación matricial $A^2-AX=I$."]),
     tasks(1, [r"$|A|=1+(\lambda-2)(\lambda-1)-\lambda=\lambda^2-4\lambda+3=(\lambda-1)(\lambda-3)$. \ Si $\lambda\neq1$ y $\lambda\neq3$: \ $\res{\operatorname{rg}(A)=3}$; \ si $\lambda=1$ o $\lambda=3$: \ $|A|=0$ y $\begin{vmatrix}0 & 1\\ 1 & 0\end{vmatrix}\neq0$: \ $\res{\operatorname{rg}(A)=2}$",
               r"$AX=A^2-I\Rightarrow X=A^{-1}(A^2-I)=A-A^{-1}$. Con $A=" + pm(A_m2) + r"$, \ $A^{-1}=" + pm(inv(A_m2)) + r"$: \ $X=\res{" + pm(X_m2) + r"}$"])),
 (2, r"\pau{Madrid, extraordinaria 2026} Se consideran las matrices \ $A=" + pm(A_me) + r"$, \ $B=" + pm(B_me) + r"$ \ y \ $C=" + pm(C_me) + r"$."
     + tasks(1, [r"Resuelve la ecuación matricial $AX+X=B$.", r"Calcula el determinante de la matriz $(2C)^{100}$ aplicando las propiedades de los determinantes.", r"Justifica si las matrices $A$ y $AB$ son invertibles."]),
     tasks(1, [r"$(A+I)X=B$, \ $|A+I|=8$, \ $(A+I)^{-1}=\frac18" + pm(tr(adjm(add(A_me, eye(3))))) + r"$: \ $X=\res{" + pm(X_me) + r"}$",
               r"$|C|=1$ (triangular): \ $|(2C)^{100}|=\left(2^3\cdot1\right)^{100}=\res{2^{300}}$", r"$|A|=" + q(det(A_me)) + r"\neq0$: \rest{$A$ es invertible}. $AB$ es $3\times2$, \rest{no es cuadrada} y no puede tener inversa."])),
 (2, r"\pau{Navarra, extraordinaria 2024} Sean $A$, $P$ y $Q$ tres matrices cuadradas regulares tales que $Q\cdot A\cdot P=I$, donde $I$ es la matriz identidad de la misma dimensión."
     + tasks(1, [r"Demuestra que \ $A\cdot P\cdot Q\cdot A=Q^{-1}\cdot P^{-1}$.", r"Calcula la matriz $A$ en el caso \ $P=" + pm(P_nv) + r"$ \ y \ $Q=" + pm(Q_nv) + r"$."]),
     tasks(1, [r"De $QAP=I$: \ $A=Q^{-1}P^{-1}$. Entonces \ $APQA=Q^{-1}P^{-1}PQ\,Q^{-1}P^{-1}=Q^{-1}P^{-1}$.",
               r"$A=Q^{-1}P^{-1}=(PQ)^{-1}$, \ $PQ=" + pm(mul(P_nv, Q_nv)) + r"$: \ $\res{A=" + pm(A_nv2) + r"}$"])),
 (2, r"\pau{Islas Baleares, ordinaria 2026} Sean $A$ y $B$ dos matrices $3\times3$ tales que $A$ es invertible y \ $AB+A+I=2A$, \ con $I$ la matriz identidad de orden 3."
     + tasks(1, [r"Calcula la inversa de $A$ en función de $I$ y $B$.", r"Sean \ $B=" + pm(B_bl) + r"$ \ y \ $b=" + pm(b_bl) + r"$. Calcula $x$ tal que $Ax=b$, donde $A$ cumple la igualdad del enunciado."]),
     tasks(1, [r"$AB-A=-I\Rightarrow A(I-B)=I$: \ $\res{A^{-1}=I-B}$", r"$x=A^{-1}b=(I-B)\,b=" + pm(sub(eye(3), B_bl)) + pm(b_bl) + r"=\res{" + pm(x_bl) + r"}$ \ (no hace falta calcular $A$)."])),
 (3, r"\pau{Cantabria, ordinaria 2026} Considera la matriz \ $A=\begin{pmatrix}1 & a & 0\\ 0 & 1 & 0\\ 0 & 0 & a\end{pmatrix}$, \ que depende del parámetro $a\in\mathbb{R}$."
     + tasks(1, [r"Estudia el rango de $A$ en función del valor del parámetro $a$.", r"Calcula $A^{100}$ en función del parámetro $a$.", r"Para $a=-1$, calcula, si es posible, la matriz $X$ que cumple \ $AXA^{-1}=" + pm(C_c1) + r"$."]),
     tasks(1, [r"$|A|=a$. \ Si $a\neq0$: \ $\res{\operatorname{rg}(A)=3}$; \ si $a=0$: \ $\res{\operatorname{rg}(A)=2}$",
               r"$A^2=\begin{pmatrix}1 & 2a & 0\\ 0 & 1 & 0\\ 0 & 0 & a^2\end{pmatrix}$, \ $A^3=\begin{pmatrix}1 & 3a & 0\\ 0 & 1 & 0\\ 0 & 0 & a^3\end{pmatrix}$, \ldots \ $\Rightarrow$ \ $\res{A^{100}=\begin{pmatrix}1 & 100a & 0\\ 0 & 1 & 0\\ 0 & 0 & a^{100}\end{pmatrix}}$",
               r"$X=A^{-1}CA$, con $A=" + pm(A_c1) + r"$ \ y \ $A^{-1}=" + pm(inv(A_c1)) + r"$: \ $X=\res{" + pm(X_c1) + r"}$"])),
 (3, r"\pau{Castilla y León, extraordinaria 2026} Sean las matrices" + dm(r"A=" + pm(A_cl) + r",\qquad B=" + pm(B_cl)) + r"Resuelve la ecuación matricial \ $\tfrac14A^2-AX=B$.",
     r"$AX=\tfrac14A^2-B\Rightarrow X=A^{-1}\left(\tfrac14A^2-B\right)$. \ $|A|=" + q(det(A_cl)) + r"$, \ $A^{-1}=\frac1{16}" + pm(tr(adjm(A_cl))) + r"$, \ $\tfrac14A^2-B=" + pm(sub(sc(F(1, 4), pw(A_cl, 2)), B_cl)) + r"$:"
     + dm(r"X=\frac1{16}" + pm(tr(adjm(A_cl))) + pm(sub(sc(F(1, 4), pw(A_cl, 2)), B_cl)) + r"=\boxed{" + pm(X_cl) + "}")),
 (3, r"\pau{Andalucía, ordinaria 2024} Considera la matriz \ $A=\begin{pmatrix}1 & 1/8 & 1/8\\ 0 & 1 & 0\\ 0 & 0 & 1\end{pmatrix}$." + tasks(1, [r"Calcula $A^{2024}$.",
     r"Halla la matriz $X$, si es posible, que verifica $A^2XA+I=O$, donde $I$ y $O$ son la matriz identidad y la matriz nula de orden 3."]),
     tasks(1, [r"$A^2=\begin{pmatrix}1 & 2/8 & 2/8\\ 0 & 1 & 0\\ 0 & 0 & 1\end{pmatrix}$, \ldots, \ $A^n=\begin{pmatrix}1 & n/8 & n/8\\ 0 & 1 & 0\\ 0 & 0 & 1\end{pmatrix}$: \ $\res{A^{2024}=" + pm(pw(A_a4, 2024)) + r"}$",
               r"$|A|=1$. \ $A^2XA=-I\Rightarrow X=-A^{-2}A^{-1}=-\left(A^{-1}\right)^3$. Como $A^{-1}=" + pm(inv(A_a4)) + r"$ (cambiando $n$ por $-n$ en la fórmula de $A^n$), \ $\left(A^{-1}\right)^3=" + pm(pw(inv(A_a4), 3)) + r"$ \ y \ $X=\res{" + pm(X_a4) + r"}$"])))

# --- 8. Problemes
M_ar = [[1, 0, 0], [1, 1, 0], [1, 0, 1]]; p_ar = [[100], [124], [234]]
ck(eq(mul(pw(M_ar, 2), p_ar), [[100], [324], [434]]))
for k in range(1, 20): ck(eq(pw(M_ar, k), [[1, 0, 0], [k, 1, 0], [k, 0, 1]]))
pau("Problemas y cuestiones",
 (2, r"\pau{Aragón, ordinaria 2026} En un ecosistema interactúan tres especies, A, B y C. La población de cada especie en el mes $k$ es $a_k$, $b_k$ y $c_k$, respectivamente, y la evolución de las poblaciones de un mes al siguiente viene dada por"
     + dm(r"\begin{pmatrix}a_{k+1}\\ b_{k+1}\\ c_{k+1}\end{pmatrix}=M\begin{pmatrix}a_k\\ b_k\\ c_k\end{pmatrix},\qquad M=" + pm(M_ar))
     + tasks(1, [r"Si en el instante inicial ($k=0$) hay 100 ejemplares de la especie A, 124 de la B y 234 de la C, ¿cuántos ejemplares de cada especie habrá dos meses después?",
                 r"Razona (sin calcular $M^k$) que se cumple \ $\begin{pmatrix}a_k\\ b_k\\ c_k\end{pmatrix}=M^k\begin{pmatrix}a_0\\ b_0\\ c_0\end{pmatrix}$.", r"Calcula $M^k$ para $k\in\mathbb{N}$. ¿Qué pasará con el número de ejemplares de cada especie con el paso del tiempo?"]),
     tasks(1, [r"$M^2=" + pm(pw(M_ar, 2)) + r"$, \ $M^2" + pm(p_ar) + '=' + pm(mul(pw(M_ar, 2), p_ar)) + r"$: \ \rest{100 de A, 324 de B y 434 de C}.",
               r"Cada mes se multiplica por $M$: \ $X_1=MX_0$, \ $X_2=MX_1=M^2X_0$, \ldots, \ y si $X_k=M^kX_0$, entonces $X_{k+1}=MX_k=M^{k+1}X_0$.",
               r"$\res{M^k=\begin{pmatrix}1 & 0 & 0\\ k & 1 & 0\\ k & 0 & 1\end{pmatrix}}$: \ $a_k=a_0=100$ se mantiene, y $b_k=124+100k$, $c_k=234+100k$: las especies B y C \rest{aumentan 100 ejemplares cada mes}."])))

# =====================================================================
bad = [info for ok, info in CHK if not ok]
assert not bad, bad
print(len(CHK), 'comprovacions correctes')

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre = pre.replace(r'\usepackage{amsmath,amssymb}', r'\usepackage{amsmath,amssymb}' + '\n' + r'\allowdisplaybreaks')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
% etiqueta dels exercicis de la PAU
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
TIT = "Matrices y determinantes"
KW = "matrices, matrices idempotentes, involutivas, nilpotentes, potencias de matrices, determinantes, propiedades de los determinantes, Vandermonde, rango con parámetros, matriz inversa, ecuaciones matriciales, sistemas matriciales"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 1: %s' % (t, TIT), capcalera='%s · Unidad 1: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 1' if sol else 'Ficha de ejercicios · Unidad 1') + '}{' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los pasos intermedios (las operaciones de Gauss, la fila o columna por la que desarrollas un determinante, el menor que eliges para estudiar un rango\ldots) pueden ser distintos de los tuyos y ser igualmente correctos; lo que debe coincidir es el resultado. En los ejercicios con parámetros, revisa que has estudiado \textbf{todos} los casos."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos y justificando cada afirmación. Recuerda que el producto de matrices \textbf{no} es conmutativo: en las identidades con matrices y en las ecuaciones matriciales, fíjate bien por qué lado multiplicas. En los ejercicios con parámetros, estudia todos los casos. Los ejercicios marcados con \textcolor{teal}{\faUniversity\ PAU} son de las pruebas de acceso a la universidad de distintas comunidades autónomas (2023--2026).") + r'''
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
