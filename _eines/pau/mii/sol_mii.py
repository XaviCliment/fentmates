#!/usr/bin/env python3
"""Genera sol.txt: solucions pas a pas dels exercicis PAU d'àlgebra de 2n Batx MII.

Els càlculs numèrics es fan amb fraccions exactes i es comproven amb assert; les discussions
amb paràmetres estan escrites a mà (i verificades a part). Cada bloc correspon a un exercici
de alg.txt: (tipus, convocatòria, ordre dins d'aquella convocatòria i tipus).
"""
from fractions import Fraction as Fr
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gauss_gen  # noqa: E402
from gauss_gen import gauss, ft  # noqa: E402

# en MII el paràmetre dels sistemes sol ser λ: els paràmetres de les solucions seran t i s
gauss_gen.PARAMS = ["t", "s"]

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
    if len(A) == 2:
        return sc(1 / d, [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]])
    return sc(1 / d, T(cof(A)))


def pw(A, n):
    R = I(len(A))
    for _ in range(n):
        R = mul(R, A)
    return R


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
    s = "$$|%s|=%s=%s\\neq0$$" % (name, tx(A, "vmatrix"), ft(d))
    if len(A) == 2:
        a, b = A[0]
        c, e = A[1]
        adjT = [[e, -b], [-c, a]]
        s += "Per tant, $%s$ té inversa. Per a una matriu $2\\times2$, $\\ %s^{-1}=\\frac{1}{|%s|}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$:" % (name, name, name)
    else:
        adjT = T(cof(A))
        s += "Per tant, $%s$ té inversa. Calculem la matriu d'adjunts i la transposem:" % name
        adj = name if name.startswith("(") else "(%s)" % name
        s += "$$\\mathrm{Adj}%s=%s\\qquad \\mathrm{Adj}%s^t=%s$$" % (adj, tx(cof(A)), adj, tx(adjT))
    R = inv(A)
    s += "$$%s^{-1}=\\frac{1}{%s}%s" % (name, ft(d), tx(adjT))
    s += "=%s" % (tx(R) if ints(R) or d == 1 else nice(R))
    return s + "$$", R


def G(rows, V="x,y,z"):
    """Resolució de Gauss d'un sistema numèric (matriu ampliada de fraccions)."""
    return gauss([[Fr(x) for x in r] for r in rows], [v.strip() for v in V.split(",")])


def dsc(Atex, calc, roots, p=r"\lambda"):
    """Pas de discussió: determinant de la matriu de coeficients i valors crítics."""
    rs = " o ".join("$%s=%s$" % (p, r) for r in roots)
    return ("<strong>Determinant de la matriu de coeficients.</strong> $$|A|=%s=%s$$" % (mt(Atex, "vmatrix"), calc)
            + ("$|A|=0\\iff$ %s." % rs if roots else "$|A|\\neq0$ per a qualsevol valor del paràmetre."))


def cdcase(roots, p=r"\lambda", n=3):
    cond = r"\ \text{i}\ ".join("%s\\neq%s" % (p, r) for r in roots) if roots else r"%s\in\mathbb{R}" % p
    return ("<strong>Cas $%s$.</strong> $|A|\\neq0\\Rightarrow %s(A)=%s(A^*)=%d=$ nombre d'incògnites: sistema %s (solució única)."
            % (cond, RG, RG, n, CD))


def crit(p, val, rows, V="x,y,z"):
    """Cas crític: substituïm el valor i resolem/discutim per Gauss."""
    return "<strong>Cas $%s=%s$.</strong> La matriu ampliada és:" % (p, val) + G(rows, V)[0]


def sol(kind, conv, n, html):
    OUT.append("## %s | %s | %d\n%s" % (kind, conv, n, html.strip()))


def steps(*items):
    return '<ol class="steps">' + "".join("<li>%s</li>" % i for i in items) + "</ol>"


def res(t): return '<p class="res"><strong>Solució:</strong> %s</p>' % t


def sysm(*eqs):
    return r"\left\{\begin{aligned}" + r"\\ ".join(eqs) + r"\end{aligned}\right."


def amp(A, b):
    """Matriu ampliada (A|b) en LaTeX, amb entrades com a text."""
    n = len(A[0])
    return r"\left(\begin{array}{" + "c" * n + "|c}" + r"\\ ".join("&".join(r) + "&" + c for r, c in zip(A, b)) + r"\end{array}\right)"


def mt(A, env="pmatrix"):
    """Matriu en LaTeX amb entrades com a text."""
    return r"\begin{%s}" % env + r"\\ ".join("&".join(r) for r in A) + r"\end{%s}" % env


RG = r"\operatorname{rg}"
CD = "<strong>compatible determinat</strong>"
CI = "<strong>compatible indeterminat</strong>"
SI = "<strong>incompatible</strong>"
ROUCHE = r"Pel teorema de Rouché-Frobenius, comparem $%s(A)$ i $%s(A^*)$ amb el nombre d'incògnites." % (RG, RG)

exec(open(os.path.join(HERE, "sol_s.py"), encoding="utf-8").read())
exec(open(os.path.join(HERE, "sol_m.py"), encoding="utf-8").read())

open(os.path.join(HERE, "sol.txt"), "w", encoding="utf-8").write(
    "Solucions dels exercicis PAU d'àlgebra de 2n Batx MII. FITXER GENERAT per sol_mii.py: no l'editeu a mà.\n\n"
    + "\n\n".join(OUT) + "\n")
print(len(OUT), "solucions")
