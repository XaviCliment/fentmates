"""Genera les solucions dels exercicis PAU de matrius (unitat 1) amb càlcul exacte."""
from fractions import Fraction as Fr
import sys

sys.path.insert(0, sys.argv[1])
from gauss_gen import gauss, ft  # noqa: E402

OUT = []


def M(*rows):
    return [[Fr(x) for x in r] for r in rows]


def mul(*Ms):
    R = Ms[0]
    for B in Ms[1:]:
        assert len(R[0]) == len(B), "dimensions"
        R = [[sum(R[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(R))]
    return R


def add(A, B): return [[a + b for a, b in zip(r, s)] for r, s in zip(A, B)]
def sub(A, B): return [[a - b for a, b in zip(r, s)] for r, s in zip(A, B)]
def sc(k, A): return [[Fr(k) * a for a in r] for r in A]
def T(A): return [list(c) for c in zip(*A)]
def I(n): return [[Fr(int(i == j)) for j in range(n)] for i in range(n)]


def minor(A, i, j): return [r[:j] + r[j + 1:] for k, r in enumerate(A) if k != i]


def det(A):
    if len(A) == 1:
        return A[0][0]
    return sum((-1) ** j * A[0][j] * det(minor(A, 0, j)) for j in range(len(A)))


def cof(A): return [[(-1) ** (i + j) * det(minor(A, i, j)) for j in range(len(A))] for i in range(len(A))]


def inv(A):
    d = det(A)
    assert d != 0
    return sc(1 / d, T(cof(A)))


def tx(A, env="pmatrix"):
    return r"\begin{%s}" % env + r"\\ ".join("&".join(ft(x) for x in r) for r in A) + r"\end{%s}" % env


def ints(A): return all(x.denominator == 1 for r in A for x in r)


def nice(A):
    """Matriu amb fraccions: si tots comparteixen denominador, el traiem fora."""
    if ints(A):
        return tx(A)
    from math import lcm
    d = 1
    for r in A:
        for x in r:
            d = lcm(d, x.denominator)
    return r"\frac{1}{%d}" % d + tx(sc(d, A))


def inv_html(A, name="A"):
    d = det(A)
    n = len(A)
    s = "$$|%s|=%s=%s\\neq0$$" % (name, tx(A, "vmatrix"), ft(d))
    if n == 2:
        a, b = A[0]
        c, e = A[1]
        adjT = [[e, -b], [-c, a]]
        s += "Per tant, $%s$ té inversa. Per a una matriu $2\\times2$, $\\ %s^{-1}=\\frac{1}{|%s|}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$:" % (name, name, name)
    else:
        adjT = T(cof(A))
        s += "Per tant, $%s$ té inversa. Calculem la matriu d'adjunts i la transposem:" % name
        s += "$$\\mathrm{Adj}(%s)=%s\\qquad \\mathrm{Adj}(%s)^t=%s$$" % (name, tx(cof(A)), name, tx(adjT))
    R = inv(A)
    s += "$$%s^{-1}=\\frac{1}{%s}%s" % (name, ft(d), tx(adjT))
    if ints(R) or d == 1:
        s += "=%s" % tx(R)
    else:
        s += "=%s" % nice(R)
    return s + "$$", R


def sol(conv, n, html):
    OUT.append("## M | %s | %d\n%s" % (conv, n, html.strip()))


def steps(*items):
    return '<ol class="steps">' + "".join("<li>%s</li>" % i for i in items) + "</ol>"


def res(t): return '<p class="res"><strong>Solució:</strong> %s</p>' % t


def chk(A, X, B, what):
    assert A == B, what


# ---------------- 1. Setembre 2002 ----------------
A = M([2, 1], [-5, 0]); B = M([3, -4], [-1, 1]); C = M([-2, -7], [13, 2])
R = sub(sc(2, B), C)
ih, Ai = inv_html(A)
X = mul(Ai, R)
assert mul(A, X) == R
sol("Setembre 2002", 1, steps(
    "<strong>Aïllem $X$.</strong> Com que $A$ multiplica per l'esquerra, multipliquem els dos membres per $A^{-1}$ per l'esquerra: $$AX=2B-C\\ \\Rightarrow\\ X=A^{-1}(2B-C)$$",
    "<strong>Calculem $2B-C$.</strong> $$2B-C=%s-%s=%s$$" % (tx(sc(2, B)), tx(C), tx(R)),
    "<strong>Calculem $A^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=A^{-1}(2B-C)=%s%s=%s$$" % (nice(Ai), tx(R), tx(X)),
    "<strong>Comprovació.</strong> $AX=%s%s=%s=2B-C$. ✓" % (tx(A), tx(X), tx(mul(A, X))),
) + res("$X=%s$" % tx(X)))

# ---------------- 2. Juny 2004 ----------------
A = M([-4, 0], [1, 1]); B = M([-1, 2], [2, 0]); C = M([2, 0], [-1, 2])
ihA, Ai = inv_html(A, "A"); ihB, Bi = inv_html(B, "B")
X = mul(Ai, sc(2, C), Bi)
assert mul(A, X, B) == sc(2, C)
sol("Juny 2004", 1, steps(
    "<strong>Aïllem $X$.</strong> Multipliquem per $A^{-1}$ per l'esquerra i per $B^{-1}$ per la dreta (l'ordre importa, el producte no és commutatiu): $$AXB=2C\\ \\Rightarrow\\ X=A^{-1}\\,(2C)\\,B^{-1}$$",
    "<strong>Calculem $A^{-1}$.</strong>" + ihA,
    "<strong>Calculem $B^{-1}$.</strong>" + ihB,
    "<strong>Calculem $X$.</strong> $$A^{-1}(2C)=%s%s=%s$$ $$X=%s%s=%s$$" % (nice(Ai), tx(sc(2, C)), nice(mul(Ai, sc(2, C))), nice(mul(Ai, sc(2, C))), nice(Bi), nice(X)),
    "<strong>Comprovació.</strong> $AXB=%s=2C$. ✓" % tx(mul(A, X, B)),
) + res("$X=%s$" % nice(X)))

# ---------------- 3. Setembre 2004 ----------------
A = M([3, 2, -1], [3, 0, 1], [2, 1, 3]); B = M([-2], [-1], [1])
D = sub(A, sc(3, I(3)))
ih, Di = inv_html(D, "(A-3I)")
X = mul(Di, B)
assert sub(mul(A, X), B) == sc(3, X)
sol("Setembre 2004", 1, steps(
    "<strong>Aïllem $X$.</strong> Passem $3X$ a l'esquerra i traiem $X$ factor comú per la dreta (escrivim $3X=3IX$): $$AX-3X=B\\ \\Rightarrow\\ (A-3I)X=B\\ \\Rightarrow\\ X=(A-3I)^{-1}B$$",
    "<strong>Calculem $A-3I$.</strong> $$A-3I=%s$$" % tx(D),
    "<strong>Calculem $(A-3I)^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=(A-3I)^{-1}B=%s%s=%s$$" % (nice(Di), tx(B), tx(X)),
    "<strong>Comprovació.</strong> $AX-B=%s=3X$. ✓" % tx(sub(mul(A, X), B)),
) + res("$X=%s$" % tx(X)))

# ---------------- 4. Setembre 2005 ----------------
A = M([1, 0], [1, 1]); B = M([1, 2], [-1, -3]); C = M([-1, -2], [-3, -8])
ihA, Ai = inv_html(A, "A"); ihB, Bi = inv_html(B, "B")
X = mul(Ai, C, Bi)
assert X[1][0] == 0 and mul(A, X, B) == C
sol("Setembre 2005", 1, steps(
    "<strong>Aïllem $X$.</strong> $$AXB=C\\ \\Rightarrow\\ X=A^{-1}\\,C\\,B^{-1}$$",
    "<strong>Calculem $A^{-1}$.</strong>" + ihA,
    "<strong>Calculem $B^{-1}$.</strong>" + ihB,
    "<strong>Calculem $X$.</strong> $$A^{-1}C=%s%s=%s$$ $$X=%s%s=%s$$" % (tx(Ai), tx(C), tx(mul(Ai, C)), tx(mul(Ai, C)), tx(Bi), tx(X)),
    "<strong>Comparem amb la forma donada.</strong> $X=\\begin{pmatrix}a&b\\\\0&c\\end{pmatrix}$ i efectivament l'element de la fila 2, columna 1 és 0, amb $a=%s$, $b=%s$, $c=%s$." % (ft(X[0][0]), ft(X[0][1]), ft(X[1][1])),
    "<strong>Comprovació.</strong> $AXB=%s=C$. ✓" % tx(mul(A, X, B)),
) + res("$X=%s$, és a dir, $a=%s,\\ b=%s,\\ c=%s$." % (tx(X), ft(X[0][0]), ft(X[0][1]), ft(X[1][1]))))

# ---------------- 5. Setembre 2006 ----------------
B = M([3, -1], [0, 2])
P = add(B, I(2)); ih, Pi = inv_html(P, "(B+I)")
Aa = mul(sc(2, T(B)), Pi)
assert add(mul(Aa, B), Aa) == sc(2, T(B))
sol("Setembre 2006", 1, steps(
    "<strong>Aïllem $A$.</strong> Traiem $A$ factor comú per l'esquerra ($A=AI$) i multipliquem per $(B+I)^{-1}$ per la dreta: $$A(B+I)=2B^t\\ \\Rightarrow\\ A=2B^t(B+I)^{-1}$$",
    "<strong>Calculem $B+I$ i $2B^t$.</strong> $$B+I=%s;\\qquad 2B^t=%s$$" % (tx(P), tx(sc(2, T(B)))),
    "<strong>Calculem $(B+I)^{-1}$.</strong>" + ih,
    "<strong>Calculem $A$.</strong> $$A=2B^t(B+I)^{-1}=%s%s=%s$$" % (tx(sc(2, T(B))), nice(Pi), nice(Aa)),
    "<strong>Comprovació.</strong> $AB+A=%s=2B^t$. ✓" % tx(add(mul(Aa, B), Aa)),
) + res("$A=%s$" % nice(Aa)))

# ---------------- 6. Juny 2007 ----------------
A = M([1, 2], [-1, 3])
ih, Ai = inv_html(A)
AAt = mul(A, T(A)); R = sub(AAt, sc(5, Ai))
sol("Juny 2007", 1, steps(
    "<strong>Calculem $A\\cdot A^t$.</strong> $$A\\cdot A^t=%s%s=%s$$" % (tx(A), tx(T(A)), tx(AAt)),
    "<strong>Calculem $A^{-1}$.</strong>" + ih,
    "<strong>Calculem el resultat.</strong> $$A\\cdot A^t-5A^{-1}=%s-%s=%s$$" % (tx(AAt), tx(sc(5, Ai)), tx(R)),
) + res("$A\\cdot A^t-5A^{-1}=%s$" % tx(R)))

# ---------------- 7. Juny 2008 ----------------
A = M([1, 1], [-1, 1]); B = M([2, 1], [-1, 1])
ih, Ai = inv_html(A)
X = sub(T(B), Ai)
assert add(mul(A, X), I(2)) == mul(A, T(B))
sol("Juny 2008", 1, steps(
    "<strong>Aïllem $X$.</strong> $$AX=AB^t-I\\ \\Rightarrow\\ X=A^{-1}(AB^t-I)=B^t-A^{-1}$$",
    "<strong>Calculem $A^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=B^t-A^{-1}=%s-%s=%s$$" % (tx(T(B)), nice(Ai), nice(X)),
    "<strong>Comprovació.</strong> $AX+I=%s=AB^t$. ✓" % tx(add(mul(A, X), I(2))),
) + res("$X=%s$" % nice(X)))

# ---------------- 8. Setembre 2008 ----------------
A = M([1, 3], [4, 2]); R = M([6, 8], [10, -20])
ih, Ai = inv_html(A)
A2 = mul(A, A); D = sub(R, sc(5, A)); A2i = mul(Ai, Ai)
X = mul(D, A2i)
assert add(mul(X, A2), sc(5, A)) == R
sol("Setembre 2008", 1, steps(
    "<strong>Apartat a) Inversa de $A$.</strong>" + ih,
    "<strong>Apartat b) Aïllem $X$.</strong> $A^2$ multiplica per la dreta, així que multipliquem per $(A^2)^{-1}=(A^{-1})^2$ per la dreta: $$XA^2=\\begin{pmatrix}6&8\\\\10&-20\\end{pmatrix}-5A\\ \\Rightarrow\\ X=\\left[\\begin{pmatrix}6&8\\\\10&-20\\end{pmatrix}-5A\\right](A^{-1})^2$$",
    "<strong>Calculem.</strong> $$\\begin{pmatrix}6&8\\\\10&-20\\end{pmatrix}-5A=%s;\\qquad (A^{-1})^2=%s$$ $$X=%s\\cdot%s=%s$$" % (tx(D), nice(A2i), tx(D), nice(A2i), nice(X)),
    "<strong>Comprovació.</strong> $A^2=%s$ i $XA^2+5A=%s$. ✓" % (tx(A2), tx(add(mul(X, A2), sc(5, A)))),
) + res("a) $A^{-1}=%s$. &nbsp; b) $X=%s$" % (nice(Ai), nice(X))))

# ---------------- 9. Juny 2010 ----------------
P = M([2, 2], [-1, -3]); v = M([3], [2]); Q = M([2, 0, -1], [4, -1, 3]); w = M([1], [5], [-3])
Qw = mul(Q, w); rhs = add(Qw, v); P2 = sc(2, P)
ih, P2i = inv_html(P2, "P")
X = mul(P2i, rhs)
assert sub(mul(P2, X), v) == Qw
sol("Juny 2010", 1, steps(
    "<strong>Simplifiquem.</strong> Calculem el producte del segon membre i anomenem $P=2\\begin{pmatrix}2&2\\\\-1&-3\\end{pmatrix}=%s$: $$\\begin{pmatrix}2&0&-1\\\\4&-1&3\\end{pmatrix}\\begin{pmatrix}1\\\\5\\\\-3\\end{pmatrix}=%s\\ \\Rightarrow\\ PX-\\begin{pmatrix}3\\\\2\\end{pmatrix}=%s$$" % (tx(P2), tx(Qw), tx(Qw)),
    "<strong>Aïllem $X$</strong> (serà una matriu $2\\times1$): $$PX=%s+%s=%s\\ \\Rightarrow\\ X=P^{-1}%s$$" % (tx(Qw), tx(v), tx(rhs), tx(rhs)),
    "<strong>Calculem $P^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=%s%s=%s$$" % (nice(P2i), tx(rhs), nice(X)),
    "<strong>Comprovació.</strong> $PX-\\begin{pmatrix}3\\\\2\\end{pmatrix}=%s$. ✓" % tx(sub(mul(P2, X), v)),
) + res("$X=%s$" % nice(X)))

# ---------------- 10. Juny 2011 ----------------
A = M([1, -2], [-1, 4]); B = M([1, 0], [-2, -1]); C = M([3, 1], [2, -1])
ihC, Ci = inv_html(C, "C"); ihA, Ai = inv_html(A, "A")
D = sub(C, T(B)); X = mul(Ai, D)
assert add(mul(A, X), T(B)) == C
sol("Juny 2011", 1, steps(
    "<strong>Apartat a) Inversa de $C$.</strong>" + ihC,
    "<strong>Apartat b) Aïllem $X$.</strong> $$AX=C-B^t\\ \\Rightarrow\\ X=A^{-1}(C-B^t)$$ $$C-B^t=%s-%s=%s$$" % (tx(C), tx(T(B)), tx(D)),
    "<strong>Calculem $A^{-1}$.</strong>" + ihA,
    "<strong>Calculem $X$.</strong> $$X=%s%s=%s$$" % (nice(Ai), tx(D), nice(X)),
    "<strong>Comprovació.</strong> $AX+B^t=%s=C$. ✓" % tx(add(mul(A, X), T(B))),
) + res("a) $C^{-1}=%s$. &nbsp; b) $X=%s$" % (nice(Ci), nice(X))))

# ---------------- 11. Setembre 2011 ----------------
A = M([3, 1], [2, 4]); B = M([-1, 2], [0, 1]); C = M([2, -1], [1, -2]); D = M([8, 8], [8, 3])
AB = mul(A, B); R1 = add(AB, sc(3, C))
ih, Ai = inv_html(A)
E = sub(D, I(2)); X = mul(Ai, E)
assert add(mul(A, X), I(2)) == D
sol("Setembre 2011", 1, steps(
    "<strong>Apartat a).</strong> $$AB=%s%s=%s;\\qquad AB+3C=%s+%s=%s$$" % (tx(A), tx(B), tx(AB), tx(AB), tx(sc(3, C)), tx(R1)),
    "<strong>Apartat b) Aïllem $X$.</strong> $$AX=D-I\\ \\Rightarrow\\ X=A^{-1}(D-I),\\qquad D-I=%s$$" % tx(E),
    "<strong>Calculem $A^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=%s%s=%s$$" % (nice(Ai), tx(E), nice(X)),
    "<strong>Comprovació.</strong> $AX+I=%s=D$. ✓" % tx(add(mul(A, X), I(2))),
) + res("a) $AB+3C=%s$. &nbsp; b) $X=%s$" % (tx(R1), nice(X))))

# ---------------- 12. Juny 2012 ----------------
A = M([1, 2], [-1, 3]); B = M([2, -6], [-1, -2])
# AX - XA amb X = [[x,0],[y,z]] -> sistema lineal en x,y,z
cols = []
for e in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
    Xe = M([e[0], 0], [e[1], e[2]])
    cols.append(sub(mul(A, Xe), mul(Xe, A)))
rows = [[cols[k][i][j] for k in range(3)] + [B[i][j]] for i in range(2) for j in range(2)]
gh, gs = gauss(rows, ["x", "y", "z"])
sol("Juny 2012", 1, steps(
    "<strong>Calculem $AX$ i $XA$</strong> amb $X=\\begin{pmatrix}x&0\\\\y&z\\end{pmatrix}$: $$AX=\\begin{pmatrix}1&2\\\\-1&3\\end{pmatrix}\\begin{pmatrix}x&0\\\\y&z\\end{pmatrix}=\\begin{pmatrix}x+2y&2z\\\\-x+3y&3z\\end{pmatrix};\\qquad XA=\\begin{pmatrix}x&0\\\\y&z\\end{pmatrix}\\begin{pmatrix}1&2\\\\-1&3\\end{pmatrix}=\\begin{pmatrix}x&2x\\\\y-z&2y+3z\\end{pmatrix}$$",
    "<strong>Igualem $AX-XA=B$ element a element.</strong> $$\\begin{pmatrix}2y&2z-2x\\\\-x+2y+z&-2y\\end{pmatrix}=\\begin{pmatrix}2&-6\\\\-1&-2\\end{pmatrix}\\ \\Rightarrow\\ \\left\\{\\begin{aligned}2y&=2\\\\-2x+2z&=-6\\\\-x+2y+z&=-1\\\\-2y&=-2\\end{aligned}\\right.$$",
    "<strong>Resolem pel mètode de Gauss.</strong>" + gh,
) + res("totes les matrius $X=\\begin{pmatrix}%s&0\\\\%s&%s\\end{pmatrix}$, amb $\\lambda\\in\\mathbb{R}$ (infinites solucions)." % tuple(gs)))
assert gs == ["3+\\lambda", "1", "\\lambda"], gs

# ---------------- 13. Juny 2013 ----------------
P = M([3, 1], [4, 3]); Q = M([0, 5], [-7, -3])
X1 = sc(Fr(1, 3), add(P, Q)); Y1 = sub(P, X1)
A = M([3, 2], [2, 2]); R = M([1, 0], [8, 6])
ih, Ai = inv_html(A)
X3 = mul(R, Ai)
assert mul(X3, A) == R and add(X1, Y1) == P and sub(sc(2, X1), Y1) == Q
sol("Juny 2013", 1, steps(
    "<strong>Apartat a).</strong> Sumem les dues equacions per eliminar $Y$: $$3X=%s+%s=%s\\ \\Rightarrow\\ X=%s$$ $$Y=%s-X=%s$$" % (tx(P), tx(Q), tx(add(P, Q)), nice(X1), tx(P), nice(Y1)),
    "<strong>Apartat b) Inversa de $A$.</strong>" + ih,
    "<strong>Apartat c).</strong> $A$ multiplica per la dreta, així que $X=\\begin{pmatrix}1&0\\\\8&6\\end{pmatrix}A^{-1}$: $$X=%s%s=%s$$" % (tx(R), nice(Ai), nice(X3)),
    "<strong>Comprovació.</strong> $XA=%s$. ✓" % tx(mul(X3, A)),
) + res("a) $X=%s,\\ Y=%s$. &nbsp; b) $A^{-1}=%s$. &nbsp; c) $X=%s$" % (nice(X1), nice(Y1), nice(Ai), nice(X3))))

# ---------------- 14. Juliol 2013 ----------------
A = M([1, 2], [0, 3]); B = M([2, -1], [1, 2]); C = M([0, 1], [-1, 2])
AB = mul(A, B); D = sub(AB, C)
ih, Di = inv_html(D, "(AB-C)")
X = mul(sc(2, C), Di)
assert sub(mul(X, A, B), mul(X, C)) == sc(2, C)
sol("Juliol 2013", 1, steps(
    "<strong>Aïllem $X$.</strong> Traiem $X$ factor comú per l'esquerra i multipliquem per la dreta per la inversa: $$X(AB-C)=2C\\ \\Rightarrow\\ X=2C\\,(AB-C)^{-1}$$",
    "<strong>Calculem $AB-C$.</strong> $$AB=%s%s=%s;\\qquad AB-C=%s$$" % (tx(A), tx(B), tx(AB), tx(D)),
    "<strong>Calculem $(AB-C)^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=%s%s=%s$$" % (tx(sc(2, C)), nice(Di), nice(X)),
    "<strong>Comprovació.</strong> $XAB-XC=%s=2C$. ✓" % tx(sub(mul(X, A, B), mul(X, C))),
) + res("$X=%s$" % nice(X)))

# ---------------- 15. Juliol 2014 ----------------
S = M([5, 3], [3, 0]); Dd = M([1, 1], [-1, 0])
A = sc(Fr(1, 2), add(S, Dd)); B = sc(Fr(1, 2), sub(S, Dd))
ih, Ai = inv_html(A)
X = mul(Ai, B, Ai)
assert mul(A, X, A) == B
sol("Juliol 2014", 1, steps(
    "<strong>Apartat a).</strong> Sumant i restant les dues igualtats: $$2A=%s\\Rightarrow A=%s;\\qquad 2B=%s\\Rightarrow B=%s$$" % (tx(add(S, Dd)), nice(A), tx(sub(S, Dd)), nice(B)),
    "<strong>Apartat b) Aïllem $X$.</strong> $$AXA=B\\ \\Rightarrow\\ X=A^{-1}\\,B\\,A^{-1}$$" + "<strong>Inversa de $A$:</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$A^{-1}B=%s%s=%s;\\qquad X=%s%s=%s$$" % (nice(Ai), nice(B), nice(mul(Ai, B)), nice(mul(Ai, B)), nice(Ai), nice(X)),
    "<strong>Comprovació.</strong> $AXA=%s=B$. ✓" % nice(mul(A, X, A)),
) + res("a) $A=%s,\\ B=%s$. &nbsp; b) $X=%s$" % (nice(A), nice(B), nice(X))))

# ---------------- 16. Juliol 2015 ----------------
A = M([1, 2], [-1, 4]); B = M([2, 2], [1, -1]); C = M([1, -1], [1, -3])
BC = mul(B, C); D = sub(A, BC)
ih, Di = inv_html(D, "(A-BC)")
X = mul(Di, sc(3, C))
assert sub(mul(A, X), mul(B, C, X)) == sc(3, C)
E = add(T(A), B); ihE, Ei = inv_html(E, "(A^t+B)")
sol("Juliol 2015", 1, steps(
    "<strong>Apartat a) Aïllem $X$.</strong> Traiem $X$ factor comú per la dreta: $$(A-BC)X=3C\\ \\Rightarrow\\ X=(A-BC)^{-1}\\,3C$$",
    "<strong>Calculem $A-BC$.</strong> $$BC=%s%s=%s;\\qquad A-BC=%s$$" % (tx(B), tx(C), tx(BC), tx(D)),
    "<strong>Calculem $(A-BC)^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=%s%s=%s$$" % (nice(Di), tx(sc(3, C)), nice(X)),
    "<strong>Apartat b).</strong> $$A^t+B=%s+%s=%s$$" % (tx(T(A)), tx(B), tx(E)) + ihE,
) + res("a) $X=%s$. &nbsp; b) $(A^t+B)^{-1}=%s$" % (nice(X), nice(Ei))))

# ---------------- 17. Juny 2016 ----------------
A = M([1, 2, 1], [1, 3, 1], [0, 1, 3]); B = M([0, -1, 2], [1, 0, -1], [2, 1, 0])
ih, Ai = inv_html(A)
X = mul(Ai, add(A, B))
assert mul(A, X) == add(A, B)
sol("Juny 2016", 1, steps(
    "<strong>Apartat a) Inversa de $A$.</strong>" + ih,
    "<strong>Apartat b) Aïllem $X$.</strong> $$AX=A+B\\ \\Rightarrow\\ X=A^{-1}(A+B)=I+A^{-1}B$$",
    "<strong>Calculem.</strong> $$A^{-1}B=%s%s=%s$$ $$X=I+A^{-1}B=%s$$" % (nice(Ai), tx(B), nice(mul(Ai, B)), nice(X)),
    "<strong>Comprovació.</strong> $AX=%s=A+B$. ✓" % tx(mul(A, X)),
) + res("a) $A^{-1}=%s$. &nbsp; b) $X=%s$" % (nice(Ai), nice(X))))

# ---------------- 18. Juliol 2016 ----------------
A = M([1, 2], [-1, -3]); B = M([1, 3], [0, 2])
AmI = sub(A, I(2)); R1 = mul(AmI, AmI); R2 = mul(A, T(B))
ih, Bi = inv_html(B, "B"); R3 = sub(A, Bi)
sol("Juliol 2016", 1, steps(
    "<strong>Apartat a).</strong> $$A-I=%s;\\qquad (A-I)^2=%s%s=%s$$" % (tx(AmI), tx(AmI), tx(AmI), tx(R1)),
    "<strong>Apartat b).</strong> $$A\\cdot B^t=%s%s=%s$$" % (tx(A), tx(T(B)), tx(R2)),
    "<strong>Apartat c).</strong> Primer la inversa de $B$:" + ih + "$$A-B^{-1}=%s-%s=%s$$" % (tx(A), nice(Bi), nice(R3)),
) + res("a) $%s$. &nbsp; b) $%s$. &nbsp; c) $%s$" % (tx(R1), tx(R2), nice(R3))))

# ---------------- 19. Juny 2017 ----------------
A = M([-1, -2, 4], [2, 3, 0], [1, 0, 2]); B = M([4, -2, 0], [1, 2, 1], [3, 1, 0])
P = add(T(A), B); Q = mul(A, B)
Y = sc(Fr(1, 3), sub(P, Q)); X = add(Q, Y)
assert add(X, sc(2, Y)) == P and sub(X, Y) == Q
sol("Juny 2017", 1, steps(
    "<strong>Resolem el sistema matricial.</strong> Restant la 2a equació a la 1a eliminem $X$: $$3Y=(A^t+B)-AB\\ \\Rightarrow\\ Y=\\tfrac13\\big[(A^t+B)-AB\\big];\\qquad X=AB+Y$$",
    "<strong>Calculem $A^t+B$ i $AB$.</strong> $$A^t+B=%s+%s=%s$$ $$AB=%s%s=%s$$" % (tx(T(A)), tx(B), tx(P), tx(A), tx(B), tx(Q)),
    "<strong>Calculem $Y$ i $X$.</strong> $$Y=\\tfrac13%s=%s$$ $$X=AB+Y=%s$$" % (tx(sub(P, Q)), nice(Y), nice(X)),
    "<strong>Comprovació.</strong> $X+2Y=%s=A^t+B$ i $X-Y=%s=AB$. ✓" % (tx(add(X, sc(2, Y))), tx(sub(X, Y))),
) + res("$X=%s,\\quad Y=%s$" % (nice(X), nice(Y))))

# ---------------- 20. Juny 2018 ----------------
A = M([2, -1, 5], [3, 1, -2], [5, 1, 3]); C = M([7, 4, 1], [1, -1, 4], [8, 4, 6])
ih, Ai = inv_html(A)
X = mul(Ai, C)
assert mul(A, X) == C
sol("Juny 2018", 1, steps(
    "<strong>Apartat a) Inversa de $A$.</strong>" + ih,
    "<strong>Apartat b).</strong> $$AX=C\\ \\Rightarrow\\ X=A^{-1}C=%s%s=%s$$" % (nice(Ai), tx(C), nice(X)),
    "<strong>Comprovació.</strong> $AX=%s=C$. ✓" % tx(mul(A, X)),
) + res("a) $A^{-1}=%s$. &nbsp; b) $X=%s$" % (nice(Ai), nice(X))))

# ---------------- 21. Juliol 2018 ----------------
A = M([1, -2, 1], [2, 0, -3], [0, 1, -1]); B = M([1, -2, 0], [-1, 2, 2], [2, -1, 3]); c = M([-2], [-1], [3])
ih, Ai = inv_html(A)
Btc = mul(T(B), c); x = mul(Ai, Btc)
assert mul(A, x) == Btc
sol("Juliol 2018", 1, steps(
    "<strong>Apartat a) Determinant i inversa de $A$.</strong>" + ih,
    "<strong>Apartat b).</strong> $$B^tc=%s%s=%s$$ $$Ax=B^tc\\ \\Rightarrow\\ x=A^{-1}B^tc=%s%s=%s$$" % (tx(T(B)), tx(c), tx(Btc), nice(Ai), tx(Btc), nice(x)),
    "<strong>Comprovació.</strong> $Ax=%s=B^tc$. ✓" % tx(mul(A, x)),
) + res("a) $|A|=%s$, $A^{-1}=%s$. &nbsp; b) $x=%s$" % (ft(det(A)), nice(Ai), nice(x))))

# ---------------- 22. Juny 2019 ----------------
A = M([3, 1], [1, 1]); B = M([0, 2], [-1, 2])
AB = mul(A, B); ih, ABi = inv_html(AB, "AB")
R2 = sub(mul(A, T(B)), mul(T(A), B))
ihB, Bti = inv_html(T(B), "(B^t)")
X = mul(Bti, sub(T(A), mul(T(A), B)))
assert add(mul(T(B), X), mul(T(A), B)) == T(A)
sol("Juny 2019", 1, steps(
    "<strong>Apartat a).</strong> $$AB=%s%s=%s$$" % (tx(A), tx(B), tx(AB)) + ih,
    "<strong>Apartat b).</strong> $$AB^t-A^tB=%s%s-%s%s=%s-%s=%s$$" % (tx(A), tx(T(B)), tx(T(A)), tx(B), tx(mul(A, T(B))), tx(mul(T(A), B)), tx(R2)),
    "<strong>Apartat c) Aïllem $X$.</strong> $$B^tX=A^t-A^tB\\ \\Rightarrow\\ X=(B^t)^{-1}(A^t-A^tB)$$ $$A^t-A^tB=%s-%s=%s$$" % (tx(T(A)), tx(mul(T(A), B)), tx(sub(T(A), mul(T(A), B)))) + ihB,
    "<strong>Calculem $X$.</strong> $$X=%s%s=%s$$" % (nice(Bti), tx(sub(T(A), mul(T(A), B))), nice(X)),
    "<strong>Comprovació.</strong> $B^tX+A^tB=%s=A^t$. ✓" % tx(add(mul(T(B), X), mul(T(A), B))),
) + res("a) $(AB)^{-1}=%s$. &nbsp; b) $%s$. &nbsp; c) $X=%s$" % (nice(ABi), tx(R2), nice(X))))

# ---------------- 23. Juliol 2019 ----------------
A = sc(Fr(1, 3), M([1, -2, 2], [2, 2, 1], [-2, 1, 2]))
d = det(A); AAt = mul(A, T(A)); x = mul(T(A), M([1], [1], [1]))
assert AAt == I(3) and mul(A, x) == M([1], [1], [1])
sol("Juliol 2019", 1, steps(
    "<strong>Apartat a) Determinant.</strong> Traiem el factor $\\tfrac13$ de cada fila (surt $\\left(\\tfrac13\\right)^3$): $$|A|=\\frac{1}{27}\\begin{vmatrix}1&-2&2\\\\2&2&1\\\\-2&1&2\\end{vmatrix}=\\frac{1}{27}\\cdot%s=%s$$" % (ft(27 * d), ft(d)),
    "<strong>Apartat b) És ortogonal.</strong> Com que $|A|\\neq0$, $A$ té inversa. Si $A\\cdot A^t=I$, aleshores $A^{-1}=A^t$: $$A\\cdot A^t=\\frac19\\begin{pmatrix}1&-2&2\\\\2&2&1\\\\-2&1&2\\end{pmatrix}\\begin{pmatrix}1&2&-2\\\\-2&2&1\\\\2&1&2\\end{pmatrix}=\\frac19\\begin{pmatrix}9&0&0\\\\0&9&0\\\\0&0&9\\end{pmatrix}=I$$",
    "<strong>Apartat c) Resolem el sistema.</strong> Com que $A^{-1}=A^t$, la solució és $X=A^t\\begin{pmatrix}1\\\\1\\\\1\\end{pmatrix}$: $$X=\\frac13\\begin{pmatrix}1&2&-2\\\\-2&2&1\\\\2&1&2\\end{pmatrix}\\begin{pmatrix}1\\\\1\\\\1\\end{pmatrix}=%s$$" % nice(x),
) + res("a) $|A|=%s$. b) $AA^t=I$, per tant $A^{-1}=A^t$. c) $x=%s,\\ y=%s,\\ z=%s$." % (ft(d), ft(x[0][0]), ft(x[1][0]), ft(x[2][0]))))

# ---------------- 24. Juliol 2020 ----------------
A = M([2, 5], [1, 2]); B = M([2, 4], [1, 2])
ih, Ai = inv_html(A)
AB = mul(A, B); BA = mul(B, A); X = mul(Ai, sub(AB, BA))
assert sub(AB, mul(A, X)) == BA
sol("Juliol 2020", 1, steps(
    "<strong>Apartat a) Inversa de $A$.</strong>" + ih,
    "<strong>Apartat b).</strong> $|B|=\\begin{vmatrix}2&4\\\\1&2\\end{vmatrix}=4-4=0$. Una matriu quadrada té inversa si i només si el seu determinant és diferent de zero, així que $B$ <strong>no</strong> té inversa (la 1a fila és el doble de la 2a).",
    "<strong>Apartat c).</strong> $|AB|=|A|\\cdot|B|=%s\\cdot0=0$, i per tant $AB$ tampoc no té inversa." % ft(det(A)),
    "<strong>Apartat d) Aïllem $X$.</strong> $$AX=AB-BA\\ \\Rightarrow\\ X=A^{-1}(AB-BA)$$ $$AB=%s;\\quad BA=%s;\\quad AB-BA=%s$$ $$X=%s%s=%s$$" % (tx(AB), tx(BA), tx(sub(AB, BA)), nice(Ai), tx(sub(AB, BA)), nice(X)),
    "<strong>Comprovació.</strong> $AB-AX=%s=BA$. ✓" % tx(sub(AB, mul(A, X))),
) + res("a) $A^{-1}=%s$. b) $|B|=0$. c) $|AB|=0$. d) $X=%s$" % (nice(Ai), nice(X))))

# ---------------- 25. Setembre 2020 ----------------
A = M([1, 2, 3], [2, 1, 1]); B = M([-1, 0], [2, 2], [-1, -1]); C = M([1, -1], [1, 0])
AB = mul(A, B); ih, ABi = inv_html(AB, "AB")
S = add(C, AB); ihC, Ci = inv_html(C, "C"); L = add(Ci, ABi)
Sd = det(S)
if Sd != 0:
    Si = inv(S); cmp = "$$(C+AB)^{-1}=%s$$" % nice(Si); eq = (Si == L)
else:
    cmp = "$|C+AB|=0$, així que $(C+AB)^{-1}$ ni tan sols existeix."; eq = False
assert eq and S == I(2)
sol("Setembre 2020", 1, steps(
    "<strong>Apartat a).</strong> $A$ és $2\\times3$ i $B$ és $3\\times2$, així que $AB$ és $2\\times2$: $$AB=%s%s=%s$$" % (tx(A), tx(B), tx(AB)) + ih,
    "<strong>Apartat b).</strong> $$C+AB=%s+%s=%s$$" % (tx(C), tx(AB), tx(S)),
    "<strong>Apartat c).</strong> Calculem $C^{-1}$:" + ihC + "$$C^{-1}+(AB)^{-1}=%s+%s=%s$$ $|C+AB|=%s$. " % (nice(Ci), nice(ABi), nice(L), ft(Sd)) + cmp,
) + "<p class=\"note\" style=\"margin:8px 0 0\">Compte: en general $(C+AB)^{-1}\\neq C^{-1}+(AB)^{-1}$; aquí coincideixen perquè les matrius d'aquest exercici són molt particulars ($C+AB=I$).</p>" + res("a) $(AB)^{-1}=%s$. b) $C+AB=%s=I$. c) <strong>Sí</strong>, en aquest cas són iguals: totes dues són la matriu identitat." % (nice(ABi), tx(S))))

# ---------------- 26. Juliol 2021 ----------------
A = M([2, 3, 4], [1, 1, 3], [1, 3, 1]); B = M([0, 0, 2], [1, 1, 1], [0, 3, 1]); C = M([5, 3, 0], [2, 1, 2])
D = sub(A, B); ih, Di = inv_html(D, "(A-B)")
X = sc(-1, mul(C, Di))
assert add(mul(X, A), C) == mul(X, B)
CB = mul(C, B)
sol("Juliol 2021", 1, steps(
    "<strong>Apartat a).</strong> $$A-B=%s$$" % tx(D) + ih,
    "<strong>Apartat b) Aïllem $X$.</strong> $$XA-XB=-C\\ \\Rightarrow\\ X(A-B)=-C\\ \\Rightarrow\\ X=-C\\,(A-B)^{-1}$$ $$X=-%s%s=%s$$" % (tx(C), nice(Di), nice(X)),
    "<strong>Comprovació.</strong> $XA+C=%s=XB$. ✓" % tx(add(mul(X, A), C)),
    "<strong>Apartat c).</strong> $BC$: $B$ és $3\\times3$ i $C$ és $2\\times3$. El nombre de columnes de $B$ (3) no coincideix amb el de files de $C$ (2): <strong>no</strong> es pot fer. <br>$CB$: $C$ és $2\\times3$ i $B$ és $3\\times3$, coincideixen (3 = 3) i el resultat és $2\\times3$: $$CB=%s%s=%s$$" % (tx(C), tx(B), tx(CB)),
) + res("a) $(A-B)^{-1}=%s$. b) $X=%s$. c) $BC$ no existeix; $CB=%s$." % (nice(Di), nice(X), tx(CB))))

# ---------------- 27. Juliol 2022 ----------------
A = M([6, 0], [2, 4]); B = M([-4], [6]); C = M([-2, -2])
BC = mul(B, C); R2 = sub(A, T(BC)); CAB = mul(C, A, B)
ih, Ai = inv_html(A)
rhs = sub(sc(5, T(C)), B); X = mul(Ai, rhs)
assert sc(Fr(1, 5), add(B, mul(A, X))) == T(C)
sol("Juliol 2022", 1, steps(
    "<strong>Apartat a) 1)</strong> $2CA$ és $(1\\times2)(2\\times2)=1\\times2$ i $B$ és $2\\times1$: no tenen la mateixa dimensió, així que $B+2CA$ <strong>no</strong> es pot calcular.",
    "<strong>Apartat a) 2)</strong> $BC$ és $(2\\times1)(1\\times2)=2\\times2$, i també $(BC)^T$: sí es pot. $$BC=%s%s=%s;\\qquad A-(BC)^T=%s-%s=%s$$" % (tx(B), tx(C), tx(BC), tx(A), tx(T(BC)), tx(R2)),
    "<strong>Apartat a) 3)</strong> $CAB$ és $(1\\times2)(2\\times2)(2\\times1)=1\\times1$: sí es pot. $$CA=%s;\\qquad CAB=%s%s=%s$$" % (tx(mul(C, A)), tx(mul(C, A)), tx(B), tx(CAB)),
    "<strong>Apartat b) Aïllem $X$.</strong> $$B+AX=5C^T\\ \\Rightarrow\\ AX=5C^T-B\\ \\Rightarrow\\ X=A^{-1}(5C^T-B)$$ $$5C^T-B=%s-%s=%s$$" % (tx(sc(5, T(C))), tx(B), tx(rhs)) + ih,
    "<strong>Calculem $X$.</strong> $$X=%s%s=%s$$" % (nice(Ai), tx(rhs), nice(X)),
    "<strong>Comprovació.</strong> $\\tfrac15(B+AX)=%s=C^T$. ✓" % tx(sc(Fr(1, 5), add(B, mul(A, X)))),
) + res("a) 1) no es pot; 2) $%s$; 3) $%s$. &nbsp; b) $X=%s$" % (tx(R2), tx(CAB), nice(X))))

# ---------------- 28. Juny 2023 ----------------
A2 = M([2, 1], [-1, 2])
assert mul(T(A2), A2) == mul(A2, T(A2))
A = M([1, 2], [-1, 0]); B = M([1, 0], [1, 1]); C = M([1, 2], [-3, -3])
D = sub(A, T(B)); ih, Di = inv_html(D, "(A-B^t)")
X = sc(-1, mul(Di, C))
assert mul(A, X) == sub(mul(T(B), X), C)
sol("Juny 2023", 1, steps(
    "<strong>Apartat a).</strong> $$A^tA=\\begin{pmatrix}2&-1\\\\1&x\\end{pmatrix}\\begin{pmatrix}2&1\\\\-1&x\\end{pmatrix}=\\begin{pmatrix}5&2-x\\\\2-x&1+x^2\\end{pmatrix};\\qquad AA^t=\\begin{pmatrix}2&1\\\\-1&x\\end{pmatrix}\\begin{pmatrix}2&-1\\\\1&x\\end{pmatrix}=\\begin{pmatrix}5&-2+x\\\\-2+x&1+x^2\\end{pmatrix}$$ Perquè siguen iguals cal $2-x=-2+x\\Rightarrow x=2$.",
    "<strong>Apartat b) Aïllem $X$.</strong> $$AX-B^tX=-C\\ \\Rightarrow\\ (A-B^t)X=-C\\ \\Rightarrow\\ X=-(A-B^t)^{-1}C$$ $$A-B^t=%s-%s=%s$$" % (tx(A), tx(T(B)), tx(D)) + ih,
    "<strong>Calculem $X$.</strong> $$X=-%s%s=%s$$" % (nice(Di), tx(C), nice(X)),
    "<strong>Comprovació.</strong> $AX=%s$ i $B^tX-C=%s$. ✓" % (tx(mul(A, X)), tx(sub(mul(T(B), X), C))),
) + res("a) $x=2$. &nbsp; b) $X=%s$" % nice(X)))

# ---------------- 29. Juny 2024 ----------------
A = M([1, 0, -1], [0, 1, 0], [0, 0, 1]); B = M([1, 1, 0], [0, 1, 1], [1, 0, 1])
D = sub(B, A); ih, Di = inv_html(D, "(B-A)")
X = mul(A, Di)
assert add(mul(inv(X), A), A) == B
ihB, Bi = inv_html(B, "B"); Y = sc(-1, Bi)
assert sub(mul(sub(A, B), Y), mul(A, Y)) == I(3)
sol("Juny 2024", 1, steps(
    "<strong>Apartat a) Aïllem $X$.</strong> $$X^{-1}A=B-A\\ \\Rightarrow\\ X^{-1}=(B-A)A^{-1}\\ \\Rightarrow\\ X=\\big[(B-A)A^{-1}\\big]^{-1}=A\\,(B-A)^{-1}$$ $$B-A=%s$$" % tx(D) + ih,
    "<strong>Calculem $X$.</strong> $$X=A(B-A)^{-1}=%s%s=%s$$" % (tx(A), nice(Di), nice(X)),
    "<strong>Apartat b) Aïllem $Y$.</strong> $$(A-B)Y-AY=I\\ \\Rightarrow\\ AY-BY-AY=I\\ \\Rightarrow\\ -BY=I\\ \\Rightarrow\\ Y=-B^{-1}$$" + ihB + "$$Y=-B^{-1}=%s$$" % nice(Y),
    "<strong>Apartat c).</strong> $$AZA^{-1}=I\\ \\Rightarrow\\ AZ=IA=A\\ \\Rightarrow\\ Z=A^{-1}A=I$$",
) + res("a) $X=%s$. b) $Y=%s$. c) $Z=I$." % (nice(X), nice(Y))))

# ---------------- 30. Juliol 2024 ----------------
A = M([1, 0], [0, 1], [-1, 3]); B = M([-1, 4, 0], [0, 2, 3]); C = M([3, 1], [1, 0])
AB = mul(A, B); E = sub(AB, sc(2, I(3))); dE = det(E)
ih, Ci = inv_html(C, "C")
X = sc(Fr(1, 2), mul(sub(T(B), A), Ci))
assert add(A, sc(2, mul(X, C))) == T(B)
sol("Juliol 2024", 1, steps(
    "<strong>Apartat a).</strong> $AB$ és $(3\\times2)(2\\times3)=3\\times3$: $$AB=%s;\\qquad AB-2I=%s$$ $$|AB-2I|=%s%s$$ %s" % (tx(AB), tx(E), tx(E, "vmatrix"), "=" + ft(dE), "Com que el determinant és diferent de zero, $AB-2I$ <strong>és invertible</strong>." if dE != 0 else "Com que el determinant és zero, $AB-2I$ <strong>no és invertible</strong>."),
    "<strong>Apartat b) Aïllem $X$.</strong> $$2XC=B^t-A\\ \\Rightarrow\\ X=\\tfrac12(B^t-A)C^{-1}$$ $$B^t-A=%s-%s=%s$$" % (tx(T(B)), tx(A), tx(sub(T(B), A))) + ih + "$$X=\\tfrac12%s%s=%s$$" % (tx(sub(T(B), A)), tx(Ci), nice(X)),
    "<strong>Comprovació.</strong> $A+2XC=%s=B^t$. ✓" % tx(add(A, sc(2, mul(X, C)))),
    "<strong>Apartat c).</strong> $$CD=\\begin{pmatrix}3&1\\\\1&0\\end{pmatrix}\\begin{pmatrix}1&-1\\\\-1&z\\end{pmatrix}=\\begin{pmatrix}2&-3+z\\\\1&-1\\end{pmatrix};\\qquad DC=\\begin{pmatrix}1&-1\\\\-1&z\\end{pmatrix}\\begin{pmatrix}3&1\\\\1&0\\end{pmatrix}=\\begin{pmatrix}2&1\\\\-3+z&-1\\end{pmatrix}$$ Han de coincidir: $-3+z=1\\Rightarrow z=4$.",
) + res("a) $|AB-2I|=%s\\neq0$: és invertible. b) $X=%s$. c) $z=4$." % (ft(dE), nice(X))))
for z in (4,):
    Dz = M([1, -1], [-1, z]); assert mul(C, Dz) == mul(Dz, C)
assert dE != 0

# ---------------- 31. Juliol 2025 (1) ----------------
A = M([1, 0, 2], [0, 1, -2], [0, 3, 0]); B = M([3, 1, 0], [-1, 0, -1]); C = M([-1, 0, 1], [4, 2, 0])
BtC = mul(T(B), C); E = sub(I(3), BtC)
ih, Ai = inv_html(A)
X = sc(Fr(1, 2), mul(E, Ai))
assert add(sc(2, mul(X, A)), BtC) == I(3)
sol("Juliol 2025", 1, steps(
    "<strong>Apartat a) Aïllem $X$.</strong> $$2XA=I-B^tC\\ \\Rightarrow\\ X=\\tfrac12(I-B^tC)A^{-1}$$ $$B^tC=%s%s=%s;\\qquad I-B^tC=%s$$" % (tx(T(B)), tx(C), tx(BtC), tx(E)),
    "<strong>Calculem $A^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=\\tfrac12%s%s=%s$$" % (tx(E), nice(Ai), nice(X)),
    "<strong>Comprovació.</strong> $2XA+B^tC=%s=I$. ✓" % tx(add(sc(2, mul(X, A)), BtC)),
    "<strong>Apartat b).</strong> $$AD=\\begin{pmatrix}1&0&2\\\\0&1&-2\\\\0&3&0\\end{pmatrix}\\begin{pmatrix}3&0&-1\\\\0&0&1\\\\0&0&z\\end{pmatrix}=\\begin{pmatrix}3&0&-1+2z\\\\0&0&1-2z\\\\0&0&3\\end{pmatrix}$$ Perquè siga diagonal, els elements fora de la diagonal han de ser 0: $-1+2z=0$ i $1-2z=0$, és a dir, $z=\\tfrac12$.",
) + res("a) $X=%s$. &nbsp; b) $z=\\tfrac12$." % nice(X)))
Dz = M([3, 0, -1], [0, 0, 1], [0, 0, Fr(1, 2)]); ADz = mul(A, Dz)
assert all(ADz[i][j] == 0 for i in range(3) for j in range(3) if i != j)

# ---------------- 32. Juliol 2025 (2) ----------------
A = M([2, 1, 0], [3, 5, 2], [1, 3, 1]); B = M([1, 2, 1], [0, 4, 2], [2, 1, 0]); C = M([1, 0, 1], [3, 2, 2], [0, 1, 0])
ACt = mul(A, T(C)); D = sub(B, A); ih, Di = inv_html(D, "(B-A)")
Xt = mul(C, Di); X = T(Xt)
assert add(mul(T(X), A), C) == mul(T(X), B)
sol("Juliol 2025", 2, steps(
    "<strong>Apartat a).</strong> $$AC^t=%s%s=%s$$" % (tx(A), tx(T(C)), tx(ACt)),
    "<strong>Apartat b).</strong> $$B-A=%s$$" % tx(D) + ih,
    "<strong>Apartat c) Aïllem $X^t$.</strong> $$X^tB-X^tA=C\\ \\Rightarrow\\ X^t(B-A)=C\\ \\Rightarrow\\ X^t=C(B-A)^{-1}$$ $$X^t=%s%s=%s$$ I transposant: $$X=%s$$" % (tx(C), nice(Di), nice(Xt), nice(X)),
    "<strong>Comprovació.</strong> $X^tA+C=%s=X^tB$. ✓" % tx(add(mul(T(X), A), C)),
) + res("a) $AC^t=%s$. b) $(B-A)^{-1}=%s$. c) $X=%s$." % (tx(ACt), nice(Di), nice(X))))

# ---------------- 33. Juny 2026 ----------------
B = M([4, -1], [-2, 3]); C = M([1, 0], [0, 1], [1, 0]); D = M([1, -1], [-2, 0], [1, 3])
CtD = mul(T(C), D); E = sub(I(2), CtD)
ih, Bi = inv_html(B, "B")
X = sc(Fr(1, 4), mul(E, Bi))
assert add(sc(4, mul(X, B)), CtD) == I(2)
F = M([1, 1, 0], [0, 0, 0]); FC = mul(F, C); assert mul(FC, FC) == FC
F = M([1, 1, 0], [0, 0, 2]); FC = mul(F, C); assert mul(FC, FC) != FC
sol("Juny 2026", 1, steps(
    "<strong>Apartat a) Aïllem $X$.</strong> $$4XB=I-C^tD\\ \\Rightarrow\\ X=\\tfrac14(I-C^tD)B^{-1}$$ $$C^tD=%s%s=%s;\\qquad I-C^tD=%s$$" % (tx(T(C)), tx(D), tx(CtD), tx(E)),
    "<strong>Calculem $B^{-1}$.</strong>" + ih,
    "<strong>Calculem $X$.</strong> $$X=\\tfrac14%s%s=%s$$" % (tx(E), nice(Bi), nice(X)),
    "<strong>Comprovació.</strong> $4XB+C^tD=%s=I$. ✓" % tx(add(sc(4, mul(X, B)), CtD)),
    "<strong>Apartat b).</strong> $$FC=\\begin{pmatrix}1&1&0\\\\0&0&z\\end{pmatrix}\\begin{pmatrix}1&0\\\\0&1\\\\1&0\\end{pmatrix}=\\begin{pmatrix}1&1\\\\z&0\\end{pmatrix};\\qquad (FC)^2=\\begin{pmatrix}1&1\\\\z&0\\end{pmatrix}\\begin{pmatrix}1&1\\\\z&0\\end{pmatrix}=\\begin{pmatrix}1+z&1\\\\z&z\\end{pmatrix}$$ Igualem $(FC)^2=FC$: $\\ 1+z=1$ i $z=0$ (la resta d'elements ja coincideixen). Per tant $z=0$.",
) + res("a) $X=%s$. &nbsp; b) $z=0$." % nice(X)))
F0 = M([1, 1], [0, 0]); assert mul(F0, F0) == F0
Fz1 = M([1, 1], [1, 0]); assert mul(Fz1, Fz1) != Fz1

open(sys.argv[2], "w", encoding="utf-8").write("\n\n".join(OUT) + "\n")
print(len(OUT), "solucions")
