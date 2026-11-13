# Comprovacions amb sympy per a la fitxa de la unitat 9 de 1r Batx MI (Derivades i aplicacions). Les importa genera.py.
# Cada derivada, valor, punt crític i extrem que apareix a les solucions es comprova amb sympy (DER, VAL, CRIT, EQL).
from sympy import symbols, sympify, diff, simplify, solve, sqrt, Rational, S, exp, log, sin, cos, tan, atan, E, nsimplify
x, h, t = symbols("x h t", real=True)
NCHK = [0]
LOC = {"x": x, "h": h, "t": t, "e": E, "ln": log}
def P(s): return sympify(s, locals=LOC)
def DER(f, d):
    """d = f' (com a text sympy)"""
    diffe = simplify(diff(P(f), x) - P(d))
    if diffe != 0:  # algunes identitats trigonomètriques/arrels: comprovació numèrica
        for v in (0.37, 0.81, 1.3, 2.2, 3.1):
            val = complex(diffe.subs(x, v).evalf())
            assert abs(val) < 1e-9, (f, d, diffe)
    NCHK[0] += 1
def VAL(f, a, v):
    assert simplify(P(f).subs(x, P(a)) - P(v)) == 0, (f, a, v, P(f).subs(x, P(a)))
    NCHK[0] += 1
def EQL(a, b):
    assert simplify(P(a) - P(b)) == 0, (a, b)
    NCHK[0] += 1
def CRIT(f, xs):
    got = sorted(solve(diff(P(f), x), x), key=lambda v: float(v))
    want = sorted([P(s) for s in xs], key=lambda v: float(v))
    assert len(got) == len(want) and all(simplify(a - b) == 0 for a, b in zip(got, want)), (f, got, want)
    NCHK[0] += 1
def SIGN(f, pts):
    """pts: [(x, '+'|'-')] signe de f' en punts de prova"""
    d = diff(P(f), x)
    for a, s in pts:
        v = float(d.subs(x, P(a)))
        assert (v > 0) == (s == '+') and v != 0, (f, a, v)
    NCHK[0] += 1
def TVM(f, a, b, v):
    assert simplify((P(f).subs(x, P(b)) - P(f).subs(x, P(a))) / (P(b) - P(a)) - P(v)) == 0, (f, a, b, v)
    NCHK[0] += 1
