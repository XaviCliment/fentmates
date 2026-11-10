# Eines per a les solucions PAU d'anàlisi de 2n Batx MII (unitats 5-9).
# Reutilitza ../../an/anlib.py (CCSS: SOL, st, plot, taula_m, nm, ...) i hi afig comprovacions amb sympy:
#   ok(a, b)    a i b són iguals (expressions o nombres exactes)
#   okn(a, b)   iguals numèricament (tol 1e-6 relativa)
#   der(f, fp)  fp és la derivada de f;  pri(f, F) F és una primitiva de f
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'an'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pr'))
from anlib import SOL, st, plot, taula_m, nm, ap, P, F, CHK  # noqa: E402,F401
import sympy as sp  # noqa: E402

x, t, a, b, c, k, m, r, h, y = sp.symbols('x t a b c k m r h y', real=True)
pi, E, sqrt, ln, sin, cos, tan, exp, atan, asin, acos, Abs, oo = (sp.pi, sp.E, sp.sqrt, sp.log, sp.sin, sp.cos,
                                                                  sp.tan, sp.exp, sp.atan, sp.asin, sp.acos, sp.Abs, sp.oo)
R = sp.Rational
integrate, diff, limit, solve, simplify = sp.integrate, sp.diff, sp.limit, sp.solve, sp.simplify


def ok(u, v):
    if isinstance(u, (list, tuple)):
        key = lambda e: float(sp.N(e)) if sp.sympify(e).is_number else 0
        U = sorted(u, key=sp.default_sort_key); V = sorted(v, key=sp.default_sort_key)
        U = sorted(U, key=key); V = sorted(V, key=key)
        assert len(U) == len(V), (u, v)
        for p, q in zip(U, V): ok(p, q)
        return u
    d = sp.simplify(sp.sympify(u) - sp.sympify(v))
    if d != 0:
        d = sp.nsimplify(sp.N(sp.sympify(u) - sp.sympify(v), 50), rational=False)
        assert abs(sp.N(sp.sympify(u) - sp.sympify(v), 40)) < 1e-30, (u, v)
    CHK.append(1)
    return u


def okn(u, v, tol=1e-6):
    U, V = float(sp.N(u)), float(sp.N(v))
    assert abs(U - V) <= tol * max(1, abs(V)), (u, v, U, V)
    CHK.append(1)
    return u


def der(f, fp, var=None):
    var = var or x
    assert sp.simplify(sp.diff(f, var) - fp) == 0 or abs(sp.N((sp.diff(f, var) - fp).subs(var, sp.Rational(7, 10)))) < 1e-12, (f, fp)
    CHK.append(1)


def pri(f, Fp, var=None, at=(R(7, 10), R(23, 10))):
    var = var or x
    d = sp.diff(Fp, var) - f
    if sp.simplify(d) != 0:
        for p in at: assert abs(sp.N(d.subs(var, p))) < 1e-12, (f, Fp, p)
    CHK.append(1)


def I(f, lo, hi, var=None):
    """integral definida exacta (sympy)"""
    return sp.simplify(sp.integrate(f, (var or x, lo, hi)))


def fl(expr, var=None):
    """funció float->float per a les gràfiques"""
    g = sp.lambdify(var or x, expr, 'math')
    def h_(v):
        try: return float(g(v))
        except (ValueError, ZeroDivisionError, OverflowError, TypeError): return float('nan')
    return h_


def gr(fs, **kw):
    """gràfica: fs = expressions sympy o (expr, [a,b])"""
    out = []
    for f in fs:
        if isinstance(f, tuple): out.append((fl(f[0]), [float(f[1][0]), float(f[1][1])]))
        else: out.append(fl(f))
    sh = []
    for s in kw.pop('shade', ()):
        f_, g_, a_, b_ = s
        sh.append((fl(f_), fl(g_) if g_ is not None else None, float(a_), float(b_)))
    pts = [tuple(float(v) if not isinstance(v, str) else v for v in p) for p in kw.pop('pts', ())]
    return plot(out, shade=sh, pts=pts, **kw)


def dd(v, k=2):
    """aproximació decimal amb coma"""
    return ap(float(sp.N(v)), k)


def pos(e, var=None):
    """arrels reals positives de e=0"""
    return [s_ for s_ in sp.solve(e, var or x) if s_.is_real and s_ > 0]
