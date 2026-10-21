"""Genera passos de Gauss (HTML + KaTeX) a partir d'una matriu ampliada entera."""
from fractions import Fraction as F
from math import gcd
import re

PARAMS = [r"\lambda", r"\mu"]


def ft(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ("-" if x < 0 else "") + r"\frac{%d}{%d}" % (abs(x.numerator), x.denominator)


def mtex(A):
    n = len(A[0]) - 1
    return r"\left(\begin{array}{" + "r" * n + "|r}" + r"\\ ".join("&".join(ft(x) for x in r) for r in A) + r"\end{array}\right)"


def coef(c):
    return "" if abs(c) == 1 else ft(abs(c))


def eq(row, V, sub=None):
    """Equació d'una fila; sub = {index: valor} substitueix incògnites conegudes."""
    s = ""
    for j, c in enumerate(row[:-1]):
        if c == 0:
            continue
        if sub and j in sub:
            v = sub[j]
            vt = "(" + ft(v) + ")" if v < 0 else ft(v)
            term = (ft(abs(c)) + r"\cdot " if abs(c) != 1 else "") + vt
        else:
            term = coef(c) + V[j]
        s += ("-" if c < 0 else ("+" if s else "")) + term
    return (s or "0") + "=" + ft(row[-1])


def lin(const, co):
    s = "" if const == 0 else ft(const)
    for i, k in enumerate(co):
        if k == 0:
            continue
        s += ("-" if k < 0 else ("+" if s else "")) + coef(k) + PARAMS[i]
    return s or "0"


def rref(M):
    A = [[F(x) for x in r] for r in M]
    rows, cols = len(A), len(A[0])
    piv, r = [], 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return A, piv


def rank(M):
    return len(rref(M)[1])


def gauss(M, V, names=None):
    """Retorna (html, solució) amb la cadena de matrius i la resolució."""
    A = [[F(x) for x in r] for r in M]
    rows, n = len(A), len(A[0]) - 1
    chain = [(None, [r[:] for r in A])]
    rk = 0
    for c in range(n):
        if rk >= rows:
            break
        cand = [r for r in range(rk, rows) if A[r][c] != 0]
        if not cand:
            continue
        p = cand[0]
        ones = [r for r in cand if abs(A[r][c]) == 1]
        if abs(A[p][c]) != 1 and ones:
            p = ones[0]
        if p != rk:
            A[p], A[rk] = A[rk], A[p]
            chain.append(([r"F_{%d}\leftrightarrow F_{%d}" % (rk + 1, p + 1)], [r[:] for r in A]))
        ops, changed = [], []
        for r in range(rk + 1, rows):
            if A[r][c] == 0:
                continue
            a, b = A[rk][c], A[r][c]
            if a < 0:
                a, b = -a, -b
            g = gcd(int(a), int(b))
            a, b = a / g, b / g
            A[r] = [a * x - b * y for x, y in zip(A[r], A[rk])]
            lab = "F_{%d}'=%sF_{%d}%s%sF_{%d}" % (r + 1, coef(a), r + 1, "-" if b > 0 else "+", coef(b), rk + 1)
            ops.append(lab)
            changed.append(r)
        if ops:
            chain.append((ops, [r[:] for r in A]))
        simp = []
        for r in changed:
            g = 0
            for x in A[r]:
                g = gcd(g, int(x))
            if A[r][:-1] == [0] * n and A[r][-1] != 0:
                continue
            lead = next((x for x in A[r] if x != 0), 0)
            if lead < 0:
                g = -g
            if abs(g) > 1 or g == -1:
                A[r] = [x / g for x in A[r]]
                k = "-" if g < 0 else ""
                simp.append(r"F_{%d}'=%sF_{%d}" % (r + 1, k + (r"\tfrac{1}{%d}" % abs(g) if abs(g) > 1 else ""), r + 1))
        if simp:
            chain.append((simp, [r[:] for r in A]))
        rk += 1
    # cadena en línies de dues fletxes
    parts, line = [], mtex(chain[0][1])
    for k, (ops, Mk) in enumerate(chain[1:]):
        arrow = r"\xrightarrow{%s}" % ops[0] if len(ops) == 1 else r"\xrightarrow{\substack{%s}}" % r"\\ ".join(ops)
        line += arrow + mtex(Mk)
        if k % 2 == 1 and k < len(chain) - 2:
            parts.append(line)
            line = ""
    parts.append(line)
    html = "".join("$$%s$$\n" % p for p in parts)
    E = chain[-1][1]
    ra = rank([r[:-1] for r in M])
    rs = rank(M)
    if ra != rs:
        bad = next(r for r in E if all(x == 0 for x in r[:-1]) and r[-1] != 0)
        html += r"La fila $(0\ \cdots\ 0\,|\,%s)$ correspon a l'equació $0=%s$, que és impossible: $\operatorname{rg}(A)=%d\neq\operatorname{rg}(A^*)=%d$ i el sistema és <strong>incompatible</strong>." % (ft(bad[-1]), ft(bad[-1]), ra, rs)
        return html, None
    eqs = [r for r in E if any(x != 0 for x in r[:-1])]
    if ra == n:
        html += r"$\operatorname{rg}(A)=\operatorname{rg}(A^*)=%d=$ nombre d'incògnites: sistema <strong>compatible determinat</strong>. Resolem de baix cap amunt:" % n
        known = {}
        lines = []
        for r in reversed(eqs):
            j = next(i for i, x in enumerate(r[:-1]) if x != 0)
            val = (r[-1] - sum(r[i] * known[i] for i in known)) / r[j]
            lines.append(eq(r, V, known) + r"\Rightarrow " + V[j] + "=" + ft(val))
            known[j] = val
        html += "\n$$" + r"\qquad ".join(lines) + "$$"
        return html, [known[i] for i in range(n)]
    R, piv = rref(M)
    free = [j for j in range(n) if j not in piv]
    html += r"$\operatorname{rg}(A)=\operatorname{rg}(A^*)=%d\lt %d$: sistema <strong>compatible indeterminat</strong> amb %d paràmetre%s. " % (ra, n, n - ra, "s" if n - ra > 1 else "")
    html += "Fem " + ", ".join("$%s=%s$" % (V[f], PARAMS[i]) for i, f in enumerate(free)) + " i aïllem:"
    sol = []
    for j in range(n):
        if j in free:
            sol.append(PARAMS[free.index(j)])
        else:
            r = R[piv.index(j)]
            sol.append(lin(r[-1], [-r[f] for f in free]))
    html += "\n$$" + r";\quad ".join("%s=%s" % (V[j], sol[j]) for j in range(n)) + r",\qquad " + ",".join(PARAMS[:len(free)]) + r"\in\mathbb{R}$$"
    return html, sol


def expand(text):
    """Substitueix [[G vars | fila ; fila ; ...]] per la resolució de Gauss."""
    def rep(m):
        vs, rows = m.group(1).split("|")
        V = [v.strip() for v in vs.split(",")]
        M = [[F(x) for x in r.split(",")] for r in rows.split(";")]
        return gauss(M, V)[0]
    return re.sub(r"\[\[G ([^\]]+)\]\]", rep, text)
