# Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 2: Sistemes d'equacions lineals)
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
S.append(("Sistemes d'equacions lineals. Mètode de Gauss", [
 (1, r"Comprova quines de les ternes següents són solució del sistema \ $" + sy(R1) + r"$" + tasks(3, [r'$(1,-1,2)$', r'$(2,1,2)$', r'$(0,1,3)$'])
     + recorda(r"Una terna $(x,y,z)$ és solució si, en substituir-la, es compleixen \textbf{totes} les equacions alhora."),
     tasks(3, [r"$5=5$, \ $-2=-2$, \ $7=7$: \rest{sí}", r"La 2a: $2+1-2=1\neq-2$: \rest{no}", r"La 1a: $0-1+3=2\neq5$: \rest{no}"])),
 (1, r"Classifica els sistemes següents i interpreta'ls geomètricament (cada equació és una recta del pla):" + tasks(3, [m(sy(R2a, 'xy')), m(sy(R2b, 'xy')), m(sy(R2c, 'xy'))])
     + recorda(r"SCD: les rectes es tallen en un punt. \ SCI: són la mateixa recta. \ SI: són paral·leles."),
     tasks(1, [r"Sumant: $3x=3$, $x=1$, $y=2$. \rest{SCD}: rectes secants en $(1,2)$.", r"La 2a és la 1a per $-2$: \rest{SCI}, la mateixa recta: $x=1+2\lambda,\ y=\lambda$.",
               r"La 1a per 2 dona $6x+2y=4\neq5$: \rest{SI}, rectes paral·leles."])),
 (2, r"Afegeix una equació al sistema \ $" + sy(B3) + r"$ \ de manera que el sistema resultant siga:" + tasks(3, ['compatible indeterminat', 'incompatible', 'compatible determinat'])
     + recorda(r"Una equació que és combinació lineal de les altres no aporta informació; una amb els mateixos coeficients i un altre terme independent les contradiu."),
     r"Hi ha moltes respostes possibles; per exemple:" + tasks(1, [r"La suma de les dues: \ $\res{3x+2z=5}$ \ (SCI).", r"Mateixos coeficients que la 1a i un altre terme independent: \ $\res{x+y+z=0}$ \ (SI).",
               r"\ $\res{z=1}$: \ queda $x+y=2,\ 2x-y=1$, \ d'on $x=1,\ y=1,\ z=1$ (SCD)."])),
 (1, r"Resol pel mètode de Gauss:" + tasks(2, [m(sy(R4a)), m(sy(R4b))])
     + recorda(r"Fes zeros davall de la diagonal amb operacions entre files de la matriu ampliada i després resol de baix cap amunt."),
     tasks(1, [G(R4a, (1, 2, 3), 'SCD') + r"$-5z=-15\Rightarrow z=3$; \ $y-6=-4\Rightarrow y=2$; \ $x=6-2-3$: \ $\res{x=1;\ y=2;\ z=3}$",
               G(R4b, (1, 2, 3), 'SCD') + r"$10z=30\Rightarrow z=3$; \ $3y-15=-9\Rightarrow y=2$; \ $x=5+2-6$: \ $\res{x=1;\ y=2;\ z=3}$"])),
 (2, r"Discuteix i resol, quan siga possible, pel mètode de Gauss:" + tasks(3, [m(sy(R5a)), m(sy(R5b)), m(sy(R5c))])
     + recorda(r"Una fila $(0\ 0\ 0\,|\,0)$ es pot suprimir; una fila $(0\ 0\ 0\,|\,d)$ amb $d\neq0$ vol dir que el sistema és incompatible. En un SCI hi ha tants paràmetres com incògnites \emph{sobren}."),
     tasks(1, [G(R5a) + r"\rest{SCI}. Fem $z=\lambda$: $3y=1+5\lambda$, \ $x=1+y-2\lambda$: \ $\res{x=\tfrac{4-\lambda}{3};\ y=\tfrac{1+5\lambda}{3};\ z=\lambda}$",
               G(R5b, cls='SI') + r"L'última fila diu $0=1$: \ \rest{SI}, no té solució.",
               r"La 2a i la 3a equacions són la 1a multiplicada per $-2$ i per $3$: només queda $x-2y+z=3$ (rang 1). \rest{SCI amb dos paràmetres}: \ $\res{x=3+2\lambda-\mu;\ y=\lambda;\ z=\mu}$"])),
 (2, r"\pau{Navarra, EvAU extraordinària 2023} Classifica el sistema següent en funció del nombre de solucions i resol-lo utilitzant el mètode de Gauss:" + dm(sy(RNAV)),
     G(RNAV, cls='SCI') + r"Queda una fila de zeros: \rest{SCI}. Amb $z=\lambda$: \ $-y-7\lambda=1\Rightarrow y=-1-7\lambda$; \ $x=1-y-3\lambda=2+4\lambda$." + dm(r'\boxed{x=2+4\lambda;\ \ y=-1-7\lambda;\ \ z=\lambda,\quad\lambda\in\mathbb{R}}')),
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
S.append(("Expressió matricial. Mètode matricial", [
 (2, r"Escriu en forma matricial $A\cdot X=B$ i resol-lo utilitzant la inversa de la matriu $A$:" + dm(sy(R7a))
     + recorda(r"Si $|A|\neq0$: \ $A\cdot X=B\Rightarrow X=A^{-1}\cdot B$, \ amb $A^{-1}=\dfrac{1}{|A|}\big(\mathrm{Adj}(A)\big)^t$. Multipliquem per $A^{-1}$ per l'\textbf{esquerra}. Compte amb les incògnites que no apareixen: el seu coeficient és 0."),
     dm(pm(coef(R7a)) + r'\cdot\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}1\\ 0\\ 2\end{pmatrix}')
     + r"$|A|=" + vm(coef(R7a)) + r"=1\neq0$, per tant $A$ té inversa:" + dm(r'\mathrm{Adj}(A)=' + pm(adjm(coef(R7a))) + r',\qquad A^{-1}=\frac{1}{1}\big(\mathrm{Adj}(A)\big)^t=' + pm(inv(coef(R7a))))
     + dm(r'X=A^{-1}\cdot B=' + pm(inv(coef(R7a))) + r'\begin{pmatrix}1\\ 0\\ 2\end{pmatrix}=\begin{pmatrix}3\\ -3\\ 5\end{pmatrix}\ \Rightarrow\ \boxed{x=3;\ y=-3;\ z=5}')),
 (1, r"Escriu el sistema d'equacions que correspon a l'equació matricial \ $" + pm(M7b) + r"\cdot\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}4\\ 1\end{pmatrix}$. \ Quantes equacions i quantes incògnites té? De quin tipus de sistema es pot tractar (SCD, SCI o SI)? Justifica la resposta.",
     r"$\res{" + sy([r + [b] for r, b in zip(M7b, B7b)]) + r"}$ \ \ Té \rest{2 equacions i 3 incògnites} (el producte d'una matriu $2\times3$ per una $3\times1$ és $2\times1$).\par No pot ser SCD: amb 2 equacions i 3 incògnites, en esglaonar sempre sobra almenys una incògnita. Les files de $A$ no són proporcionals i, amb $F_2'=F_2+F_1$, queda $2y+3z=5$: no apareix cap fila del tipus $0=d\neq0$. Per tant, és \rest{SCI}, amb un paràmetre: \ $x=-1+3\lambda;\ y=\tfrac{5-3\lambda}{2};\ z=\lambda$."),
 (2, r"Resol pel mètode matricial (amb la matriu inversa):" + tasks(2, [m(sy([r + [b] for r, b in zip(A8a, B8a)], 'xy')), m(sy([r + [b] for r, b in zip(A8b, B8b)]))]),
     tasks(1, [r"$|A|=1$, \ $A^{-1}=" + pm(INV8a) + r"$, \ $X=" + pm(INV8a) + r"\begin{pmatrix}7\\ 3\end{pmatrix}=\begin{pmatrix}1\\ 2\end{pmatrix}$: \ $\res{x=1;\ y=2}$",
               r"$|A|=2$, \ $A^{-1}=\frac12" + pm([[1, 1, -1], [-1, 1, 1], [1, -1, 1]]) + r"$, \ $X=\frac12" + pm([[1, 1, -1], [-1, 1, 1], [1, -1, 1]]) + r"\begin{pmatrix}3\\ 3\\ 4\end{pmatrix}=\frac12\begin{pmatrix}2\\ 4\\ 4\end{pmatrix}$: \ $\res{x=1;\ y=2;\ z=2}$"])),
 (2, r"\pau{Galícia, ABAU extraordinària 2023} Expressa en forma matricial el sistema d'equacions següent i resol-lo:" + dm(sy(RGAL)),
     dm(pm(coef(RGAL)) + r'\cdot\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}2\\ -1\\ 1\end{pmatrix}')
     + r"$|A|=-1\neq0$, per tant $A$ té inversa:" + dm(r'\mathrm{Adj}(A)=' + pm(adjm(coef(RGAL))) + r',\qquad A^{-1}=\frac{1}{-1}\big(\mathrm{Adj}(A)\big)^t=' + pm(INVG))
     + dm(r'X=A^{-1}\cdot B=' + pm(INVG) + r'\begin{pmatrix}2\\ -1\\ 1\end{pmatrix}=\begin{pmatrix}2\\ -1\\ -1\end{pmatrix}\ \Rightarrow\ \boxed{x=2;\ y=-1;\ z=-1}')),
 (2, r"\pau{País Basc, PAU extraordinària 2025} Considera el sistema d'equacions lineals" + dm(sy(RPV)) + tasks(1, ["Expressa'l mitjançant una equació matricial.", "La matriu dels coeficients té inversa? Raona la resposta.", "Resol el sistema d'equacions lineals."]),
     tasks(1, [r"$" + pm(coef(RPV)) + r"\cdot\begin{pmatrix}x\\ y\\ z\end{pmatrix}=\begin{pmatrix}3\\ 1\\ 0\end{pmatrix}$",
               r"$|A|=3\cdot2+(-2)\cdot1+(-2)\cdot2=6-2-4=0$: \ \rest{no té inversa} i no podem aplicar el mètode matricial.",
               G(RPV) + r"\rest{SCI}. Amb $z=\lambda$: \ $2y=\lambda$, \ $x=1+z$: \ $\res{x=1+\lambda;\ y=\tfrac{\lambda}{2};\ z=\lambda,\ \ \lambda\in\mathbb{R}}$"])),
 (3, r"Considera el sistema \ $\left\{\begin{aligned}x+ky&=1\\ y+z&=2\\ kx+z&=3\end{aligned}\right.$" + tasks(1, [r"Comprova que es pot resoldre pel mètode matricial per a qualsevol valor de $k$.", r"Resol-lo pel mètode matricial per a $k=1$."]),
     tasks(1, [r"$|A|=" + vm([[1, 'k', 0], [0, 1, 1], ['k', 0, 1]]) + r"=1+k^2>0$ per a tot $k$: \ $A$ \rest{sempre és invertible}.",
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
 (1, r"Resol aplicant la regla de Cramer:" + tasks(2, [m(sy(R12a, 'xy')), m(sy(R12b))])
     + recorda(r"Si el sistema és quadrat i $|A|\neq0$, cada incògnita és un quocient de determinants: al numerador, la columna de la incògnita se substitueix per la dels termes independents."),
     tasks(1, [r"$|A|=" + vm(coef(R12a)) + r"=17$: \ $x=\dfrac{" + vm([[-4, -3], [7, 1]]) + r"}{17}=\dfrac{17}{17}$, \ $y=\dfrac{" + vm([[2, -4], [5, 7]]) + r"}{17}=\dfrac{34}{17}$: \ $\res{x=1;\ y=2}$",
               r"$|A|=7$, \ $|A_x|=7$, \ $|A_y|=-7$, \ $|A_z|=14$: \ $\res{x=1;\ y=-1;\ z=2}$"])),
 (2, r"\pau{Castella i Lleó, PAU ordinària 2025} Donat el sistema \ $\left\{\begin{aligned}ax+2y+z&=1\\ x+by+2z&=4\\ 3x+y+bz&=5\end{aligned}\right.$, \ resol-lo per a $a=1$ i $b=-2$.",
     r"Queda $" + sy(RCYL) + r"$, amb $|A|=" + vm(coef(RCYL)) + r"=25\neq0$: és de Cramer."
     + dm(r'x=\frac{' + vm(subcol(RCYL, 0)) + r'}{25}=\frac{52}{25},\quad y=\frac{' + vm(subcol(RCYL, 1)) + r'}{25}=\frac{-17}{25},\quad z=\frac{' + vm(subcol(RCYL, 2)) + r'}{25}=\frac{7}{25}')
     + dm(r'\boxed{x=\tfrac{52}{25};\ \ y=-\tfrac{17}{25};\ \ z=\tfrac{7}{25}}')),
 (2, r"Justifica que el sistema següent és de Cramer i calcula, \textbf{només}, el valor de $z$. Comprova després el resultat calculant també $x$ i $y$." + dm(sy(R15)),
     r"$|A|=" + vm(coef(R15)) + r"=23\neq0$. \ $z=\dfrac{" + vm(subcol(R15, 2)) + r"}{23}=\res{\dfrac{6}{23}}$; \ $x=\dfrac{10}{23}$, \ $y=\dfrac{22}{23}$ (i es comprova en les tres equacions)."),
 (3, r"Resol aplicant la regla de Cramer el sistema compatible indeterminat \ $" + sy(R14) + r"$ \ (passa $z$ al segon membre).",
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
S.append(("Sistemes homogenis", [
 (1, r"Classifica i resol els sistemes homogenis següents:" + tasks(2, [m(sy(R20a)), m(sy(R20b))])
     + recorda(r"Un sistema homogeni sempre és compatible (té la solució trivial $x=y=z=0$). Té més solucions si i només si $\operatorname{rg}(A)<n$; si és quadrat, quan $|A|=0$."),
     tasks(1, [r"$|A|=" + vm(coef(R20a)) + r"=-5\neq0$: \ \rest{SCD}, només la solució trivial \ $\res{x=y=z=0}$.",
               r"$|A|=0$ i $\begin{vmatrix}1&-1\\ 2&1\end{vmatrix}=3\neq0$: \ $\operatorname{rg}(A)=2<3$, \ \rest{SCI}. Sumant les dues primeres, $3x=0$; i de la 1a, $y=z$: \ $\res{x=0;\ y=\lambda;\ z=\lambda}$"])),
 (2, r"Considera el sistema homogeni \ $" + sy(R21) + r"$" + tasks(1, ["Raona, sense resoldre'l, si té solucions diferents de la trivial.", "Resol-lo pel mètode de Gauss.", r"Troba la solució que compleix $x+y+z=12$."]),
     tasks(1, [r"$|A|=" + vm(coef(R21)) + r"=0\Rightarrow\operatorname{rg}(A)<3$: \ \rest{SCI}, té infinites solucions a més de la trivial.",
               G(R21) + r"Amb $z=2\lambda$: \ $-4y+12\lambda=0\Rightarrow y=3\lambda$; \ $x=-y+2z=\lambda$: \ $\res{x=\lambda;\ y=3\lambda;\ z=2\lambda,\ \ \lambda\in\mathbb{R}}$",
               r"$\lambda+3\lambda+2\lambda=6\lambda=12\Rightarrow\lambda=2$: \ $\res{x=2;\ y=6;\ z=4}$"])),
 (1, r"Per què el sistema \ $" + sy(R22) + r"$ \ té infinites solucions sense calcular cap determinant? Resol-lo.",
     r"És homogeni (compatible) i $\operatorname{rg}(A)\leq2<3$ incògnites: \rest{SCI}. Passant $z$ al segon membre: $2x-y=-z$, $x+3y=2z$ \ $\Rightarrow x=-\frac z7,\ y=\frac{5z}{7}$. Amb $z=7\lambda$: \ $\res{x=-\lambda;\ y=5\lambda;\ z=7\lambda}$"),
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
 (1, r"Classifica els sistemes següents aplicant el teorema de Rouché-Frobenius (no cal resoldre'ls):" + tasks(3, [m(sy(R16a, 'xy')), m(sy(R16b, 'xy')), m(sy(R16c))])
     + recorda(r"$\operatorname{rg}(A)\neq\operatorname{rg}(A^*)$: SI. \ $\operatorname{rg}(A)=\operatorname{rg}(A^*)=n$: SCD. \ $\operatorname{rg}(A)=\operatorname{rg}(A^*)<n$: SCI ($n$ = nombre d'incògnites)."),
     tasks(1, [r"$\begin{vmatrix}1&2\\ 3&-1\end{vmatrix}=-7\neq0\Rightarrow\operatorname{rg}(A)=2$; \ $|A^*|=" + vm(R16a) + r"=0\Rightarrow\operatorname{rg}(A^*)=2=n$: \ \rest{SCD} (la solució és $x=1,\ y=2$).",
               r"$\operatorname{rg}(A)=2$; \ $|A^*|=" + vm(R16b) + r"=7\neq0\Rightarrow\operatorname{rg}(A^*)=3$: \ \rest{SI}.",
               r"$|A|=0$ i $\begin{vmatrix}1&1\\ 2&-1\end{vmatrix}=-3\neq0\Rightarrow\operatorname{rg}(A)=2$. Els menors d'ordre 3 de $A^*$ amb la columna de termes independents també valen 0 $\Rightarrow\operatorname{rg}(A^*)=2<3$: \ \rest{SCI} (la 3a equació és la 1a més el doble de la 2a)."])),
 (2, r"\pau{Múrcia, PAU ordinària 2025} Discuteix i resol, si és possible, el sistema lineal següent:" + dm(sy(RMU)),
     r"$|A|=" + vm(coef(RMU)) + r"=-10\neq0\Rightarrow\operatorname{rg}(A)=\operatorname{rg}(A^*)=3=n$: \ \rest{SCD}. Per Cramer o per Gauss: \ $\res{x=1;\ y=1;\ z=2}$"),
 (2, r"Classifica el sistema següent i, si és compatible, resol-lo:" + dm(sy(R18)),
     r"$" + vm([r[:3] for r in R18[:3]]) + r"=6\neq0\Rightarrow\operatorname{rg}(A)=3$; \ $|A^*|=0\Rightarrow\operatorname{rg}(A^*)=3=n$: \ \rest{SCD}. Suprimim la 4a equació (no forma part del menor) i resolem les tres primeres: \ $\res{x=1;\ y=1;\ z=1}$"),
 (2, r"Raona si són certes o falses les afirmacions següents:" + tasks(1, [r"Un sistema de 3 equacions i 2 incògnites no pot ser compatible determinat.",
                r"Si un sistema de 3 equacions i 3 incògnites té $|A|\neq0$, sempre és compatible determinat.",
                r"Si $\operatorname{rg}(A)=2$ i $\operatorname{rg}(A^*)=3$, el sistema té dues solucions.",
                r"Un sistema de 2 equacions i 3 incògnites pot ser compatible determinat."]),
     tasks(1, [r"\rest{Falsa}: si $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$ és SCD (com al primer apartat de l'exercici \ref{ex:rf}).",
               r"\rest{Certa}: $\operatorname{rg}(A)=3$ i $\operatorname{rg}(A^*)$ no pot passar de 3 (té 3 files): $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3=n$.",
               r"\rest{Falsa}: els rangs són diferents i el sistema és incompatible (cap solució).",
               r"\rest{Falsa}: $\operatorname{rg}(A)\leq2<3$, així que, si és compatible, és indeterminat."])),
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
S.append(("Discussió de sistemes amb paràmetres", [
 (2, r"\pau{Astúries, PAU extraordinària 2025} Donat el sistema d'equacions \ $\left\{\begin{aligned}x-y&=-m\\ 10x+(10+m)y&=150\end{aligned}\right.$, \ amb incògnites $x$ i $y$:" + tasks(1, [r"Per a quins valors del paràmetre $m$ té el sistema una única solució?",
         r"Si el sistema fóra \ $\left\{\begin{aligned}x-y&=-\lambda\\ 10x+(10+m)y&=150\end{aligned}\right.$, \ troba el valor de $m$ i un valor de $\lambda$ per als quals el sistema tinga infinites solucions, i calcula'n una."])
     + recorda(r"Calcula $|A|$ i busca els valors que l'anul·len (valors crítics); estudia cada valor crític a banda amb Rouché-Frobenius."),
     tasks(1, [r"$|A|=\begin{vmatrix}1&-1\\ 10&10+m\end{vmatrix}=20+m$. \ Té solució única (SCD) si i només si \ $\res{m\neq-20}$. (Per a $m=-20$: $x-y=20$ i $x-y=15$, SI.)",
               r"Cal $|A|=0$: $\res{m=-20}$; aleshores la 2a equació és $x-y=15$ i, perquè coincidisca amb la 1a, $\res{\lambda=-15}$. Una solució: $\res{x=15,\ y=0}$ (en general, $x=15+t,\ y=t$)."])),
 (2, r"\pau{Astúries, EBAU extraordinària 2024} Siguen les matrius $A=" + pm([[2, 1], [-1, 'm']]) + r"$, $B=" + pm([[1, 'm'], [-1, 1]]) + r"$, $C=" + pm([[0, '2m'], ['-2m', -1]]) + r"$, $D=\begin{pmatrix}x\\ y\end{pmatrix}$ i $E=\begin{pmatrix}1\\ 1\end{pmatrix}$."
     + tasks(1, [r"Si $(A\cdot B-C)\cdot D=E$, planteja un sistema de dues equacions i dues incògnites ($x$ i $y$) en funció del paràmetre $m$.", r"Per a quins valors de $m$ té solució el sistema? Si en té, és sempre única? Resol el sistema per a $m=-1$."]),
     tasks(1, [r"$A\cdot B=\begin{pmatrix}1&2m+1\\ -1-m&0\end{pmatrix}$, \ $A\cdot B-C=\begin{pmatrix}1&1\\ m-1&1\end{pmatrix}$: \ \ $\res{\left\{\begin{aligned}x+y&=1\\ (m-1)x+y&=1\end{aligned}\right.}$",
               r"$|A|=2-m$. \ Si $m\neq2$: \rest{SCD}, solució única. \ Si $m=2$: les dues equacions són $x+y=1$, \rest{SCI}. \ Té solució \rest{per a tot $m$}, però només és única si $m\neq2$. \ Per a $m=-1$: $x+y=1$, $-2x+y=1$ \ $\Rightarrow\res{x=0;\ y=1}$."])),
 (2, r"\pau{Madrid, EvAU extraordinària 2022} Considera el sistema d'equacions lineals dependent del paràmetre $a\in\mathbb{R}$:" + dm(r'\left\{\begin{aligned}x+ay+z&=2\\ x-az&=0\\ x+y+z&=2\end{aligned}\right.') + tasks(1, ["Discuteix la compatibilitat del sistema per als diferents valors de $a$.", "Resol el sistema per a $a=0$."]),
     tasks(1, [r"$|A|=\begin{vmatrix}1&a&1\\ 1&0&-a\\ 1&1&1\end{vmatrix}=1-a^2=0\Rightarrow a=\pm1$."
               + r"\par $\bullet$ $a\neq\pm1$: \rest{SCD}. \ $\bullet$ $a=1$: la 1a i la 3a equacions són iguals, $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$: \rest{SCI}. \ $\bullet$ $a=-1$: $\operatorname{rg}(A)=2$ i $\begin{vmatrix}1&-1&2\\ 1&0&0\\ 1&1&2\end{vmatrix}=4\neq0\Rightarrow\operatorname{rg}(A^*)=3$: \rest{SI}.",
               r"$x+z=2$, $x=0$, $x+y+z=2$: \ $\res{x=0;\ y=0;\ z=2}$"])),
 (2, r"\pau{Madrid, EvAU extraordinària 2024} Considera el sistema d'equacions lineals dependent del paràmetre $a\in\mathbb{R}$:" + dm(r'\left\{\begin{aligned}2x+y+3z&=2\\ 3x+y+z&=0\\ 8x+ay+5z&=2\end{aligned}\right.') + tasks(1, ["Discuteix el sistema per als diferents valors de $a$.", "Resol el sistema d'equacions per a $a=3$."]),
     tasks(1, [r"$|A|=7a-21=0\Rightarrow a=3$. \ $\bullet$ $a\neq3$: \rest{SCD}. \ $\bullet$ $a=3$: $\begin{vmatrix}2&1\\ 3&1\end{vmatrix}=-1\neq0$, $\operatorname{rg}(A)=2$, i els menors d'ordre 3 de $A^*$ valen 0 (la 3a equació és $E_1+2E_2$): $\operatorname{rg}(A^*)=2$, \rest{SCI}.",
               r"Restant $E_2-E_1$: $x-2z=-2$. Amb $z=\lambda$: $x=-2+2\lambda$, \ $y=-3x-z=6-7\lambda$:\par $\res{x=-2+2\lambda;\ y=6-7\lambda;\ z=\lambda}$"])),
 (2, r"\pau{Madrid, EvAU ordinària 2024} Considera el sistema d'equacions lineals dependent del paràmetre $a\in\mathbb{R}$:" + dm(r'\left\{\begin{aligned}2x+y+z&=a\\ x+ay+z&=a+1\\ x+y+az&=2\end{aligned}\right.') + tasks(1, ["Discuteix el sistema en funció dels valors del paràmetre $a$.", "Resol el sistema d'equacions per a $a=1$."]),
     tasks(1, [r"$|A|=2a^2-2a=2a(a-1)=0\Rightarrow a=0,\ a=1$."
               + r"\par $\bullet$ $a\neq0,1$: \rest{SCD}. \ $\bullet$ $a=0$: $\operatorname{rg}(A)=2$ i $\begin{vmatrix}2&1&0\\ 1&0&1\\ 1&1&2\end{vmatrix}=-3\neq0$: \rest{SI}. \ $\bullet$ $a=1$: la 2a i la 3a equacions coincideixen ($x+y+z=2$), $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$: \rest{SCI}.",
               r"$2x+y+z=1$ i $x+y+z=2$. Restant: $x=-1$; amb $z=\lambda$: \ $\res{x=-1;\ y=3-\lambda;\ z=\lambda}$"])),
 (2, r"\pau{Madrid, PAU extraordinària 2025} Es considera el sistema d'equacions dependent del paràmetre real $a$:" + dm(r'\left\{\begin{aligned}x+y+z&=2\\ 2x-y+z&=3\\ (a+1)x+az&=5\end{aligned}\right.') + tasks(1, ["Discuteix el sistema en funció dels valors del paràmetre real $a$.", "Resol el sistema per a $a=2$."]),
     tasks(1, [r"$|A|=2-a=0\Rightarrow a=2$. \ $\bullet$ $a\neq2$: \rest{SCD}. \ $\bullet$ $a=2$: la 3a equació, $3x+2z=5$, és la suma de les dues primeres: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$, \rest{SCI}.",
               r"Amb $z=\lambda$: $x+y=2-\lambda$, $2x-y=3-\lambda$ $\Rightarrow$ \ $\res{x=\tfrac{5-2\lambda}{3};\ y=\tfrac{1-\lambda}{3};\ z=\lambda}$"])),
 (2, r"\pau{Múrcia, PAU extraordinària 2025} Considera el sistema d'equacions següent, on $a$ és un nombre real desconegut:" + dm(r'\left\{\begin{aligned}x-y+z&=1\\ 2x-y+z&=a\\ 3x+2y-az&=4\end{aligned}\right.') + tasks(1, ["Discuteix el sistema d'equacions segons els valors de $a$.", "Resol el sistema per a $a=1$."]),
     tasks(1, [r"$|A|=2-a=0\Rightarrow a=2$. \ $\bullet$ $a\neq2$: \rest{SCD}. \ $\bullet$ $a=2$: $\operatorname{rg}(A)=2$ i $\begin{vmatrix}1&-1&1\\ 2&-1&2\\ 3&2&4\end{vmatrix}=1\neq0\Rightarrow\operatorname{rg}(A^*)=3$: \rest{SI}.",
               r"$E_2-E_1$: $x=0$. Aleshores $-y+z=1$ i $2y-z=4$: \ $\res{x=0;\ y=5;\ z=6}$"])),
 (2, r"\pau{Múrcia, EBAU ordinària 2023} Discuteix el sistema lineal d'equacions en funció dels valors del paràmetre $a$ i resol-lo per a $a=0$:" + dm(r'\left\{\begin{aligned}ax+y+z&=1\\ 2x+y+z&=1\\ x+ay+z&=2\end{aligned}\right.'),
     r"$|A|=-a^2+3a-2=-(a-1)(a-2)=0\Rightarrow a=1,\ a=2$."
     + r"\par $\bullet$ $a\neq1,2$: \rest{SCD}. \ $\bullet$ $a=1$: la 1a i la 3a equacions tenen els mateixos coeficients i termes independents diferents: \rest{SI}. \ $\bullet$ $a=2$: la 1a i la 2a són iguals, $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$: \rest{SCI}."
     + r"\par Per a $a=0$: $y+z=1$, $2x+y+z=1$, $x+z=2$ \ $\Rightarrow\res{x=0;\ y=-1;\ z=2}$"),
 (2, r"Troba el valor de $k$ perquè el sistema homogeni \ $\left\{\begin{aligned}x+y-z&=0\\ 2x-y+kz&=0\\ x+2y+z&=0\end{aligned}\right.$ \ tinga solucions diferents de la trivial i resol-lo per a aquest valor.",
     r"$|A|=\begin{vmatrix}1&1&-1\\ 2&-1&k\\ 1&2&1\end{vmatrix}=-k-8=0\Rightarrow\res{k=-8}$. Si $k\neq-8$: \rest{SCD}, només la solució trivial. Per a $k=-8$ és \rest{SCI}: de la 1a, $z=x+y$; a la 3a, $2x+3y=0$." + dm(r'\boxed{x=3\lambda;\ \ y=-2\lambda;\ \ z=\lambda,\quad\lambda\in\mathbb{R}}')),
 (3, r"\pau{Madrid, EvAU extraordinària 2023} Considera el sistema d'equacions lineals dependent del paràmetre real $a$:" + dm(r'\left\{\begin{aligned}ax+y+2z&=1\\ x+ay+2z&=a\\ x+2y+az&=1\end{aligned}\right.') + tasks(1, ["Discuteix el sistema en funció dels valors del paràmetre $a$.", "Resol el sistema d'equacions per a $a=0$."]),
     tasks(1, [r"$|A|=a^3-7a+6=(a-1)(a-2)(a+3)=0\Rightarrow a=1,\ a=2,\ a=-3$."
               + r"\par $\bullet$ $a\neq1,2,-3$: \rest{SCD}. \ $\bullet$ $a=1$: la 1a i la 2a equacions són iguals, $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2$: \rest{SCI}. \ $\bullet$ $a=2$: la 2a i la 3a tenen els mateixos coeficients i termes independents diferents: \rest{SI}. \ $\bullet$ $a=-3$: $\operatorname{rg}(A)=2$ i $\begin{vmatrix}-3&1&1\\ 1&-3&-3\\ 1&2&1\end{vmatrix}=-8\neq0$: \rest{SI}.",
               r"$y+2z=1$, $x+2z=0$, $x+2y=1$ \ $\Rightarrow\res{x=-\tfrac13;\ y=\tfrac23;\ z=\tfrac16}$"])),
 (3, r"\pau{Castella i Lleó, PAU ordinària 2025} Donat el sistema amb els paràmetres $a$ i $b$:" + dm(r'\left\{\begin{aligned}ax+2y+z&=1\\ x+by+2z&=4\\ 3x+y+bz&=5\end{aligned}\right.') + tasks(1, [r"Si $b=-1$, classifica el sistema en funció dels diferents valors del paràmetre $a$.", r"Si $a=3$, classifica el sistema en funció dels diferents valors del paràmetre $b$."]),
     r"En general, $|A|=ab^2-2a-5b+13$ (l'exercici de la secció de Cramer resolia el cas $a=1$, $b=-2$)."
     + tasks(1, [r"$|A|=18-a=0\Rightarrow a=18$. \ $a\neq18$: \rest{SCD}. \ $a=18$: $\begin{vmatrix}1&-1\\ 3&1\end{vmatrix}=4\neq0$, $\operatorname{rg}(A)=2$, i $\begin{vmatrix}2&1&1\\ -1&2&4\\ 1&-1&5\end{vmatrix}=36\neq0$: \rest{SI}.",
                 r"$|A|=3b^2-5b+7$, que no s'anul·la mai (discriminant $25-84<0$): \rest{SCD per a tot $b$}."])),
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
S.append(("Problemes de plantejament", [
 (1, r"\pau{Canàries, EBAU ordinària 2022} Una empresa dedicada a activitats i esports aquàtics ha venut en un dia un total de 45 sessions entre pàdel surf, caiac i moto aquàtica. Els preus per sessió i persona d'aquestes activitats són 40 €, 20 € i 60 €, respectivament, i l'empresa ha recaptat un total de 1\,700 € aquell dia. A més, per cada persona que tria caiac n'hi ha tres que trien pàdel surf." + tasks(1, ["Planteja el sistema d'equacions corresponent.", "Quantes persones van a cada activitat?"])
     + recorda(r"Defineix bé les incògnites (què representa cada lletra), tradueix cada frase en una equació i, al final, comprova que la solució té sentit en el context (nombres naturals, preus positius\dots)."),
     r"$x$, $y$, $z$: persones de pàdel surf, caiac i moto. \ " + pr(P['can22'], 'xyz') + r" \ Amb $x=3y$: $4y+z=45$ i $7y+3z=85$\par $\Rightarrow$ \ \rest{30 de pàdel surf, 10 de caiac i 5 de moto aquàtica}."),
 (2, r"\pau{Canàries, EBAU ordinària 2023} En un barri viuen 875 persones classificades en tres grups: xiquets i joves, adults i jubilats. La quarta part dels adults és igual al doble de la cinquena part dels xiquets i joves, i per cada 9 jubilats n'hi ha 26 de la resta." + tasks(1, ["Planteja el sistema d'equacions corresponent.", "Explicant els passos del mètode emprat, resol el sistema plantejat.", "Quantes persones hi ha en cada grup?"]),
     r"$x$: xiquets i joves, $y$: adults, $z$: jubilats. \ $\frac y4=\frac{2x}{5}$, \ $\frac{z}{x+y}=\frac{9}{26}$: \ " + pr(P['can23'], 'xyz') + r" \ De la 3a i la 1a: $35z=9\cdot875$, $z=225$; $x+y=650$ i $y=\frac85x$\par $\Rightarrow$ \ \rest{250 xiquets i joves, 400 adults i 225 jubilats}."),
 (1, r"\pau{Canàries, EBAU extraordinària 2024} En una botiga d'electrònica es venen telèfons mòbils, tauletes i ordinadors portàtils. Un mòbil costa 300 €, una tauleta 400 € i un portàtil 800 €. En una setmana s'han ingressat 28\,000 € en vendes d'aquests aparells. S'han venut el doble de mòbils que de tauletes i, per cada dues tauletes, s'ha venut un portàtil." + tasks(1, ["Planteja el sistema d'equacions corresponent.", "Quants aparells de cada tipus s'han venut?"]),
     pr(P['can24e'], 'xyz') + r" ($x$ mòbils, $y$ tauletes, $z$ portàtils). \ Amb $y=2z$, $x=4z$: $2800z=28\,000$\par $\Rightarrow$ \ \rest{40 mòbils, 20 tauletes i 10 portàtils}."),
 (2, r"\pau{Canàries, EBAU ordinària 2024} Una jugadora d'escacs ha aconseguit premis en 51 dels tornejos en què ha participat al llarg de la seua vida. Els tornejos han sigut locals, nacionals i internacionals. El nombre de tornejos locals en què ha jugat ha sigut el doble dels nacionals; a més, per cada cinc tornejos nacionals ha participat en dos d'internacionals. Els tornejos en què ha aconseguit premi representen un 30\,\% de tots els tornejos en què ha participat." + tasks(1, ["Planteja el sistema d'equacions corresponent.", "En quants tornejos de cada classe ha participat aquesta jugadora?"]),
     r"$x$, $y$, $z$: tornejos locals, nacionals i internacionals. \ " + pr(P['can24o'], 'xyz') + r" \ El total és $51/0{,}3=170$; amb $x=2y$ i $z=\frac25y$: $\frac{17}{5}y=170$\par $\Rightarrow$ \ \rest{100 locals, 50 nacionals i 20 internacionals}."),
 (2, r"\pau{Cantàbria, EBAU extraordinària 2022} Un dia de platja, la Fabiola s'acosta al xiringuito i compra 3 gelats, 2 granissats i 2 orxates, i paga un total de 20 €. En comprovar el tiquet s'adona que li han cobrat un gelat i una orxata de més. Després de reclamar, el venedor li torna 5 €. A més, per compensar l'error, li ofereix endur-se en promoció un gelat i un granissat per 2 €, la qual cosa suposa un descompte del 50\,\% respecte dels preus originals." + tasks(1, ["Planteja el sistema d'equacions que permet calcular el preu (sense descompte) d'un gelat, un granissat i una orxata.", "Resol-lo."]),
     r"$x$, $y$, $z$: preu d'un gelat, d'un granissat i d'una orxata. Li han cobrat 4 gelats, 2 granissats i 3 orxates per 20 €; el que havia de pagar és 15 €; i el 50\,\% de $x+y$ és 2 €:\ " + pr(P['cnt22'], 'xyz')
     + r" \ Restant les dues primeres: $x+z=5$; amb $y=4-x$, $z=5-x$ en la 2a: $x=3$\par $\Rightarrow$ \ \rest{gelat 3 €, granissat 1 €, orxata 2 €}."),
 (1, r"\pau{Cantàbria, EBAU ordinària 2023} En un magatzem de construcció venen sacs de ciment de 25 kg, 50 kg i 100 kg. Cert dia es va vendre un total de 180 sacs per un import de 29\,200 €. Se sap que el preu del kg de ciment és de 4 € i que aquell dia es van vendre el doble de sacs de 25 kg que la suma dels sacs de 50 kg i dels de 100 kg." + tasks(1, ["Planteja un sistema d'equacions que permeta calcular quants sacs de cada grandària es van vendre aquell dia.", "Resol-lo."]),
     r"Un sac de 25 kg val 100 €, un de 50 kg, 200 € i un de 100 kg, 400 €: \ " + pr(P['cnt23'], 'xyz') + r" \ De la 1a i la 3a: $3(y+z)=180$, $y+z=60$, $x=120$; i $y+2z=86$\par $\Rightarrow$ \ \rest{120 sacs de 25 kg, 34 de 50 kg i 26 de 100 kg}."),
 (2, r"\pau{Cantàbria, EBAU extraordinària 2024} Una organització encarregada d'un esdeveniment esportiu té un pressupost de 500 € per a adquirir material promocional: banderes, samarretes i gorres. Els preus per unitat són de 5, 6 i 2 euros, respectivament. La quantitat de samarretes ha de ser la meitat de la de gorres, i la suma de banderes i samarretes ha de ser 70." + tasks(1, ["Planteja el sistema d'equacions que permet calcular les unitats que s'han de comprar de cada article si es vol esgotar el pressupost.", "Analitza la compatibilitat del sistema.", "Resol-lo."]),
     tasks(1, [r"$x$ banderes, $y$ samarretes, $z$ gorres: \ " + pr(P['cnt24e'], 'xyz'), r"$|A|=" + vm(coef(P['cnt24e'])) + r"=-5\neq0$: $\operatorname{rg}(A)=\operatorname{rg}(A^*)=3$, \rest{SCD}.", r"\rest{40 banderes, 30 samarretes i 60 gorres}."])),
 (2, r"\pau{Cantàbria, EBAU ordinària 2024} Una empresa de jardineria necessita adquirir 300 kg de terra, 200 kg de pedres decoratives i 100 kg de llavors. En comparar preus entre dos proveïdors, A i B, obté aquestes ofertes: el proveïdor A li ofereix un preu total de 13\,000 €; el proveïdor B, que fa descomptes per renovació d'inventari, redueix el preu de la terra a un terç del que ofereix A, el de les pedres a la meitat i el de les llavors a una cinquena part, i resulta un estalvi de 8\,800 € respecte del preu total d'A. A més, per al proveïdor A, el preu per kg de les llavors és el doble de la suma dels preus per kg de la terra i de les pedres." + tasks(1, ["Planteja el sistema d'equacions que permet calcular el preu per kilogram de la terra, les pedres i les llavors en el proveïdor A.", "Analitza la compatibilitat del sistema.", "Resol-lo."]),
     tasks(1, [r"$x$, $y$, $z$: €/kg de terra, pedres i llavors en A. El proveïdor B cobra $13\,000-8\,800=4\,200$ €: \ " + pr(P['cnt24o'], 'xyz'),
               r"$|A|=" + vm(coef(P['cnt24o'])) + r"=" + q(det(coef(P['cnt24o']))) + r"\neq0$: \rest{SCD}.", r"Substituint $z=2x+2y$: $5x+4y=130$ i $x+y=30$\par $\Rightarrow$ \ \rest{terra 10 €/kg, pedres 20 €/kg, llavors 60 €/kg}."])),
 (1, r"\pau{Castella i Lleó, EBAU ordinària 2023} Comprem tres entrades per a tres activitats: una per al teatre, una altra per a un partit de bàsquet i una altra per a un concert. Després de descomptar-nos el 10\,\% del preu total, hem pagat 117 euros per totes les entrades. Sabem que el preu de l'entrada del concert és el doble que el de l'entrada del teatre i que l'entrada del concert és 20 euros més cara que la del partit de bàsquet. Determina el preu de l'entrada de cada activitat.",
     r"$x$ teatre, $y$ bàsquet, $z$ concert: \ " + pr(P['cyl23'], 'xyz') + r" \ $x+y+z=130$; amb $x=\frac z2$, $y=z-20$: $\frac52z=150$\par $\Rightarrow$ \ \rest{teatre 30 €, bàsquet 40 €, concert 60 €}."),
 (1, r"\pau{Castella-la Manxa, EvAU extraordinària 2022} El nombre total de premis Goya rebuts al llarg de la carrera per tres dones (Isabel, Carmen i Enma) és de 15. Si augmentem en un premi la quantitat que ha rebut Isabel, obtenim el triple dels premis guanyats per Enma, i els que ha rebut Enma equivalen a les tres quartes parts dels que ha rebut Carmen." + tasks(1, ["Planteja el sistema d'equacions que ens permet esbrinar quants premis Goya ha rebut cada una.", "Resol raonadament el sistema plantejat."]),
     r"$x$ Isabel, $y$ Carmen, $z$ Enma: $x+1=3z$, $z=\frac34y$: \ " + pr(P['clm22a'], 'xyz') + r"\par $\Rightarrow$ \ \rest{Isabel 8, Carmen 4 i Enma 3}."),
 (2, r"\pau{Castella-la Manxa, EvAU extraordinària 2022} Un concessionari d'automòbils té en oferta tres models de cotxe: un esportiu, un familiar i un monovolum. El mes passat es van vendre 10 esportius, 6 familiars i 3 monovolums i es van obtenir 851\,000 euros. L'esportiu val 2\,000 euros més que el familiar. Per 5 esportius venuts s'obtenen 13\,000 euros més que si es venen 6 monovolums." + tasks(1, ["Planteja el sistema d'equacions que ens permet esbrinar el preu de cadascun dels tres models.", "Resol raonadament el sistema plantejat."]),
     pr(P['clm22b'], 'xyz') + r" \ Amb $y=x-2000$ i $z=\frac{5x-13000}{6}$ en la 1a: $18{,}5x=869\,500$.\par $\Rightarrow$ \ \rest{esportiu 47\,000 €, familiar 45\,000 €, monovolum 37\,000 €}."),
 (1, r"\pau{Castella-la Manxa, EvAU ordinària 2022} La capsa de bombons que compre costa 51 euros i conté 12 bombons de xocolata negra, 6 de xocolata amb llet i 6 de xocolata blanca. Cada bombó de xocolata negra costa un euro més que els de xocolata amb llet, i aquests costen 50 cèntims menys que els de xocolata blanca." + tasks(1, ["Planteja el sistema d'equacions que ens permet esbrinar quant costa cada tipus de bombó.", "Resol raonadament el sistema plantejat."]),
     pr(P['clm22c'], 'xyz') + r" \ Amb $x=y+1$, $z=y+0{,}5$: $24y+15=51$\par $\Rightarrow$ \ \rest{negra 2{,}50 €, amb llet 1{,}50 €, blanca 2 €}."),
 (2, r"\pau{Castella-la Manxa, EvAU extraordinària 2023} Una cooperativa manxega que distribueix tres tipus de vi, blanc, rosat i negre, ha rebut una comanda de 50 botelles. Se sap que el doble de botelles de vi blanc, d'una banda, excedeix en una unitat les de vi rosat i, d'una altra, coincideix amb el quíntuple del nombre de botelles de vi negre." + tasks(1, ["Planteja un sistema d'equacions per esbrinar quantes botelles de vi blanc, rosat i negre es van demanar.", "Resol raonadament el sistema plantejat."]),
     pr(P['clm23'], 'xyz') + r" \ Amb $y=2x-1$, $z=\frac{2x}{5}$: $\frac{17}{5}x=51$\par $\Rightarrow$ \ \rest{15 de blanc, 29 de rosat i 6 de negre}."),
 (2, r"\pau{Castella-la Manxa, EvAU ordinària 2023} La discografia d'un grup de rock llegendari es reedita en tres discos (I, II i III) i les vendes totals arriben a 70\,000 unitats. Sabem que del disc III se'n van vendre tantes unitats com dels altres dos junts, i que la diferència entre les unitats venudes del III i les del II equival al triple de la diferència entre les venudes del II i les del I." + tasks(1, ["Planteja el sistema d'equacions per calcular quantes unitats de cada disc es van vendre.", "Resol raonadament el sistema plantejat."]),
     r"$z-y=3(y-x)$: \ " + pr(P['clm23o'], 'xyz') + r" \ Sumant les dues primeres, $z=35\,000$\par $\Rightarrow$ \ \rest{15\,000 del I, 20\,000 del II i 35\,000 del III}."),
 (2, r"\pau{Castella-la Manxa, EvAU extraordinària 2024} Dels nadons inscrits el mes de maig a Castella-la Manxa, 72 es diuen Alba, Pablo o David. Sabem que el nombre de nadons anomenats David coincideix amb la diferència entre els que es diuen Pablo i les que es diuen Alba. A més, s'hi han inscrit tantes xiquetes amb el nom d'Alba com la suma dels inscrits com a David i un terç dels inscrits com a Pablo." + tasks(1, ["Planteja el sistema d'equacions que permet esbrinar quants nadons s'han inscrit amb cada nom.", "Resol raonadament el sistema plantejat."]),
     r"$x$ Alba, $y$ Pablo, $z$ David: \ " + pr(P['clm24e'], 'xyz') + r" \ Sumant les dues primeres: $2y=72$, $y=36$\par $\Rightarrow$ \ \rest{24 Alba, 36 Pablo i 12 David}."),
 (2, r"\pau{Castella-la Manxa, EvAU ordinària 2024} A la fase nacional de l'Olimpíada Matemàtica Espanyola es reparteixen 36 medalles d'or, de plata i de bronze. El nombre de medalles de bronze triplica el de medalles d'or i, si dues de les medalles de plata passaren a la categoria de bronze, aleshores la quantitat de medalles de bronze duplicaria la de plata." + tasks(1, ["Planteja el sistema d'equacions per calcular quantes medalles de cada tipus es reparteixen.", "Resol raonadament el sistema plantejat."]),
     r"$x$ or, $y$ plata, $z$ bronze: $z+2=2(y-2)$: \ " + pr(P['clm24o'], 'xyz') + r"\par $\Rightarrow$ \ \rest{6 d'or, 12 de plata i 18 de bronze}."),
 (3, r"\pau{Castella-la Manxa, EvAU ordinària 2024} En una classe se celebren eleccions a delegada i s'hi presenten dues candidates, Inés i Nerea. Se sap que quatre vegades el nombre de vots de Nerea menys tres vegades el nombre de vots d'Inés excedeix en un vot el nombre de vots nuls. Si dividim el nombre de vots d'Inés entre el de Nerea, obtenim quocient 1 i residu 7 ($D=d\cdot c+r$). El 5\,\% del total de vots emesos és nul." + tasks(1, ["Planteja el sistema d'equacions per calcular el nombre de vots nuls i els que van rebre Inés i Nerea.", "Resol raonadament el sistema plantejat."]),
     r"$x$ Inés, $y$ Nerea, $z$ nuls: $4y-3x=z+1$, \ $x=y+7$, \ $z=0{,}05(x+y+z)\Leftrightarrow x+y-19z=0$: \ " + pr(P['clm24v'], 'xyz') + r"\par $\Rightarrow$ \ \rest{Inés 32 vots, Nerea 25 vots i 3 nuls}."),
 (1, r"\pau{Castella-la Manxa, PAU extraordinària 2025} Al Parador de Turisme d'Almagro es van allotjar ahir 25 hostes procedents d'Itàlia, Portugal i el Japó. La despesa total al Parador va ser de 3\,610 €: 140 € per cada hoste italià, 130 € per cada portugués i 160 € per cada japonés. El registre mostra que el nombre de portuguesos és la quarta part de la suma dels hostes dels altres dos països." + tasks(1, ["Planteja el sistema d'equacions per calcular quants hostes hi ha de cada país.", "Calcula el nombre d'hostes de cadascun dels països."]),
     pr(P['clm25'], 'xyz') + r" \ De la 1a i la 3a: $5y=25$, $y=5$; després $7x+8z=148$ i $x+z=20$\par $\Rightarrow$ \ \rest{12 italians, 5 portuguesos i 8 japonesos}."),
 (2, r"\pau{Catalunya, PAU extraordinària 2022} En Martí explica a en Marcel que l'altre dia, quan va agafar l'autocar per anar de Barcelona a Tarragona, l'autocar es va avariar just a la meitat del trajecte. Des d'aquell punt va anar a peu fins a la població més pròxima, de manera que va recórrer a peu una vintena part del trajecte total. Allí va agafar un taxi fins a Tarragona, i diu que va recórrer 5 km més en autocar que en taxi." + tasks(1, ["Planteja i resol un sistema d'equacions per calcular quants quilòmetres va recórrer en autocar, a peu i en taxi.", "Si l'autocar anava a 100 km/h, en Martí va caminar a 5 km/h i el taxi anava a 90 km/h, quant de temps va tardar a fer tot el trajecte?"]),
     tasks(1, [r"$x$ autocar, $y$ a peu, $z$ taxi. El trajecte total és $x+y+z$: \ $x=\frac{x+y+z}{2}$, \ $y=\frac{x+y+z}{20}$, \ $x=z+5$:\ " + pr(P['cat22'], 'xyz') + r" \ De la 1a i la 2a, $x=10y$ i $z=9y$; en la 3a, $y=5$: \ \rest{50 km en autocar, 5 km a peu i 45 km en taxi}.",
               r"$\frac{50}{100}+\frac55+\frac{45}{90}=0{,}5+1+0{,}5=\res{2\text{ hores}}$."])),
 (3, r"\pau{Catalunya, PAU ordinària 2023} Una empresa distribueix dos tipus de paquets a les farmàcies, A i B. El paquet A conté 5 termòmetres digitals d'infrarojos, 30 mascaretes i 10 tests ràpids d'antígens. El paquet B conté 1 termòmetre, 15 mascaretes i 20 tests. El paquet A costa 550 € i el B, 200 €. El preu de cada producte és el mateix en els dos tipus de paquet." + tasks(1, ["Amb aquestes dades, és possible trobar el preu d'un termòmetre, el d'una mascareta i el d'un test d'antígens? Justifica la resposta plantejant i classificant un sistema d'equacions. Resol el sistema deixant la solució en funció del preu del test d'antígens.", "Si un test d'antígens costa 4 €, quin serà el preu d'una mascareta? I el d'un termòmetre?"]),
     tasks(1, [r"$x$ termòmetre, $y$ mascareta, $z$ test: \ " + pr(P['cat23'], 'xyz') + r" \ Dues equacions i tres incògnites, $\operatorname{rg}(A)=\operatorname{rg}(A^*)=2<3$: \rest{SCI}, \textbf{no} es poden determinar els preus. Restant $5E_2-E_1$: $45y+90z=450$: \ $\res{y=10-2z;\ \ x=50+10z}$.",
               r"$z=4$: \ \rest{la mascareta costa 2 € i el termòmetre, 90 €}."])),
 (1, r"\pau{Madrid, EvAU extraordinària 2024} En una botiga de música hi ha 70 instruments de tres tipus: guitarres, pianos i violins. Se sap que la quantitat de pianos més la de violins és igual a la de guitarres. Si tinguérem el mateix nombre de violins, però el doble de pianos i quatre vegades el de guitarres, el total d'instruments de la botiga seria de 180. Planteja un sistema d'equacions i determina el nombre d'instruments de cada tipus.",
     r"$x$ guitarres, $y$ pianos, $z$ violins: \ " + pr(P['mad24e'], 'xyz') + r" \ De les dues primeres, $x=35$\par $\Rightarrow$ \ \rest{35 guitarres, 5 pianos i 30 violins}."),
 (1, r"\pau{Madrid, EvAU ordinària 2024} Un equip de bàsquet regional ha venut tres tipus d'entrades per al darrer partit: generals a 10 €, d'estudiant a 8 € i infantils a 5 €. L'equip ha venut 600 entrades i ha ingressat 4\,900 €. A més, ha venut el doble d'entrades generals que d'infantils. Planteja el sistema d'equacions i resol-lo per calcular el nombre d'entrades venudes de cada tipus.",
     pr(P['mad24o'], 'xyz') + r" \ Amb $x=2z$: $3z+y=600$ i $25z+8y=4900$\par $\Rightarrow$ \ \rest{200 generals, 300 d'estudiant i 100 infantils}."),
 (2, r"\pau{Navarra, PAU ordinària 2025} Una empresa envasa pastes en capses de 250 g, 500 g i 1 kg. Cert dia es van envasar 65 capses en total, 5 capses més de grandària petita (250 g) que de mitjana (500 g). Sabent que el kilo de pastes costa 24 euros i que l'import total de les pastes envasades aquell dia és de 720 euros, quantes capses de cada tipus s'hi han envasat?" + tasks(1, ["Planteja el sistema d'equacions lineals.", "Resol el sistema. Interpreta la solució en el context del problema."]),
     r"Les capses valen 6 €, 12 € i 24 €: \ " + pr(P['nav25'], 'xyz') + r"\par $\Rightarrow$ \ \rest{30 capses de 250 g, 25 de 500 g i 10 d'1 kg} (nombres naturals: la solució té sentit)."),
 (1, r"\pau{País Basc, PAU extraordinària 2025} El caixer automàtic d'un banc només disposa de bitllets de 10, 20 i 50 euros. Hem tret 290 euros i el caixer ens ha donat exactament 8 bitllets. A més, el nombre de bitllets de 10 euros és el doble que el de 20 euros." + tasks(1, ["Planteja el sistema d'equacions lineals associat a aquest problema.", "Resol el sistema d'equacions lineals."]),
     pr(P['pv25e'], 'xyz') + r" \ Amb $x=2y$: $3y+z=8$ i $40y+50z=290$\par $\Rightarrow$ \ \rest{2 bitllets de 10 €, 1 de 20 € i 5 de 50 €}."),
 (2, r"\pau{País Basc, PAU ordinària 2025} Una botiga té llandes de conserva de tomaca de tres fabricants: A, B i C. El fabricant A envasa la tomaca en llandes de 250 g, el B en llandes de 500 g i el C en llandes d'1 kg. Aquestes llandes es venen a 1 €, 1{,}80 € i 3{,}30 €, respectivament. Comprem 20 llandes que pesen en total 10 kg i valen 35{,}60 €. Volem saber quantes llandes hem comprat de cada fabricant." + tasks(1, ["Planteja el sistema d'equacions que resol el problema.", "Resol el problema."]),
     pr(P['pv25o'], 'xyz') + r" \ Multiplicant per 4 la 2a i per 10 la 3a, i restant la 1a: $y+3z=20$ i $8y+23z=156$\par $\Rightarrow$ \ \rest{8 llandes d'A, 8 de B i 4 de C}."),
 (3, r"\pau{Astúries, PAU ordinària 2025} En una atracció hi ha dos tipus de passis, el VIP i el normal, de preus $x$ i $y$ euros, respectivament. Un grup de persones va pagar 90 € per un passi VIP i tres de normals, mentre que un altre grup va pagar $15m$ € per dos passis VIP i $m$ passis normals. Per determinar el preu de cada passi s'utilitza el sistema" + dm(r'\left\{\begin{aligned}x+3y&=90\\ 2x+my&=15m\end{aligned}\right.') + tasks(1, ["Si $m=15$, quin va ser el preu de cada tipus de passi?", "Dona un valor de $m$ per al qual el sistema tinga solució, però aquesta solució no tinga sentit en el context del problema. Justifica la resposta.", "Per a quin valor de $m$ el sistema no té solució? Justifica la resposta."]),
     tasks(1, [r"$x+3y=90$, $2x+15y=225$\par $\Rightarrow$ \ \rest{VIP 75 €, normal 5 €}.",
               r"Per a $m\neq6$ és SCD amb $x=\frac{45m}{m-6}$, $y=\frac{15(m-12)}{m-6}$. Si $6<m<12$, el preu $y$ és negatiu: per exemple, $\res{m=9}$ dona $x=135$, $y=-15$, que no té sentit.",
               r"$|A|=m-6=0\Rightarrow\res{m=6}$: $2x+6y=90$ contradiu $x+3y=90$ (que multiplicada per 2 dona 180): \rest{SI}."])),
 (3, r"\pau{Astúries, EBAU extraordinària 2023} En una festa es van beure $m$ copes de vi negre per cada una de vi blanc. Cada copa (de vi negre o blanc) conté 0{,}15 litres i en total es van beure $3m$ litres de vi." + tasks(1, ["Planteja un sistema de dues equacions en funció del paràmetre $m$ en què les incògnites $x$ i $y$ siguen el nombre de copes de vi negre i de vi blanc, respectivament.", "Per a quins valors de $m$ té solució el sistema anterior? Si en té, és sempre única? Quantes copes de cada tipus es van beure si en total es van consumir 9 litres de vi?"]),
     tasks(1, [r"$\res{\left\{\begin{aligned}x-my&=0\\ 0{,}15x+0{,}15y&=3m\end{aligned}\right.}$",
               r"$|A|=0{,}15(1+m)$. Si $m\neq-1$: \rest{SCD} (solució única, $x=\frac{20m^2}{1+m}$, $y=\frac{20m}{1+m}$). Si $m=-1$: $x+y=0$ i $x+y=-20$: \rest{SI}. \ Amb 9 litres, $3m=9$, $m=3$: $x+y=60$, $x=3y$\par $\Rightarrow$ \ \rest{45 copes de vi negre i 15 de blanc}."])),
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
print(len(CHK), 'comprovacions correctes')

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={sistemes d'equacions lineals, mètode de Gauss, mètode matricial, regla de Cramer, teorema de Rouché-Frobenius, sistemes homogenis, discussió de sistemes, paràmetres, problemes, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
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
                    "pdftitle={%s de la unitat 2: %s. 2n de Batxillerat CCSS}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 2: %s · 2n Batxillerat CCSS" % (t, TIT))
    assert 'Unitat 2' in p and 'unitat 2' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 2' if sol else "Fitxa d'exercicis · Unitat 2") + r'''}{''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Els passos de Gauss poden ser diferents dels teus i ser igualment correctes; el que ha de coincidir és la classificació i la solució (en un SCI, la solució general es pot escriure de maneres diferents segons la incògnita que prengues com a paràmetre). Pots comprovar-ho amb el resolutor de sistemes dels apunts interactius."
             if sol else r"Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes (traduïts al valencià). Resol-los al quadern justificant cada pas: indica sempre el mètode que fas servir i, en els problemes, què representa cada incògnita.") + r'''
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
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'exercicis,', npau, 'de la PAU d\'altres comunitats')
