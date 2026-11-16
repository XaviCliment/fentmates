# Genera t5-fitxa-exercicis.tex i t5-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 5: Sistemes d'equacions i inequacions)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució), en valencià i castellà amb T(va, es).
# Les eines comunes (tasks, recorda, R, Rm, RI, build) són a ../comu/eso4b.py i les figures del pla (rectes) a ../comu/regions.py;
# build(..., curs='4eso-a') posa la capçalera de Matemàtiques A. Les equacions i inequacions s'escriuen una sola vegada en una
# notació senzilla, com als resolutors dels apunts (p. ex. '(x+1)/2+y/3=2', '3(x-2)+1<x+5'), i Q() en fa alhora el TeX de
# l'enunciat i l'expressió de sympy. sympy calcula i comprova totes les solucions: lsr() la forma ax+by=c i la solució dels
# sistemes lineals (amb kind() per a classificar-los), nls() els no lineals, iq() les inequacions (forma reduïda i interval) i
# iqs() els sistemes d'inequacions; chk() comprova les solucions escrites a mà dels problemes.
# Ús: python3 genera.py (valencià) i python3 genera-es.py (castellà); després pdflatex dues vegades cada .tex.
import os, sys, re
from functools import reduce
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *
from regions import fig, verts, C

LANG = 'es' if (len(sys.argv) > 1 and sys.argv[1] == 'es') else 'va'
def T(va, es): return es if LANG == 'es' else va

x, y = sp.symbols('x y', real=True)
NCHK = [0]

# ---------------------------------------------------------------------
# lector d'equacions i inequacions: TeX + sympy
class Nd:
    def __init__(s, e, t, par=False, inner=None): s.e, s.t, s.par, s.inner = e, t, par, inner
OPS = {'<=': r'\le ', '>=': r'\ge ', '<': '<', '>': '>', '=': '='}
def Q(src):
    TK = r'\d+(?:[.,]\d+)?|x|y|[-+*/^()\[\]]'
    toks = []
    st = {'i': 0, 'm': 1}
    def pk(): return toks[st['i']] if st['i'] < len(toks) else None
    def nx(): st['i'] += 1; return toks[st['i'] - 1]
    def strip(n): return n.inner if n.par else n.t
    def expr():
        a = term()
        while pk() in ('+', '-'):
            o = nx(); b = term()
            a = Nd(a.e + b.e if o == '+' else a.e - b.e, a.t + o + b.t)
        return a
    def term():
        a = unary()
        while True:
            p = pk()
            if p in ('*', '/'):
                nx(); b = unary()
                if p == '*': a = Nd(a.e * b.e, a.t + r'\cdot ' + b.t)
                else:
                    st['m'] = sp.ilcm(st['m'], sp.Rational(b.e).p)
                    a = Nd(a.e / b.e, r'\dfrac{%s}{%s}' % (strip(a), strip(b)))
            elif p is not None and (p in ('x', 'y', '(', '[') or re.match(r'\d', p)):
                b = unary(); sep = r'\cdot ' if re.search(r'\d$', a.t) and re.match(r'\d', b.t) else ''
                a = Nd(a.e * b.e, a.t + sep + b.t)
            else: return a
    def unary():
        if pk() == '-': nx(); a = unary(); return Nd(-a.e, '-' + a.t)
        return power()
    def power():
        a = atom()
        if pk() == '^':
            nx(); k = nx(); a = Nd(a.e ** int(k), a.t + '^{%s}' % k)
        return a
    def atom():
        q = nx()
        if re.match(r'\d', q): return Nd(sp.Rational(q.replace(',', '.')), re.sub(r'[.,]', '{,}', q))
        if q == 'x': return Nd(x, 'x')
        if q == 'y': return Nd(y, 'y')
        if q in '([':
            e = expr(); c = nx(); assert c == (')' if q == '(' else ']'), src
            big = r'\dfrac' in e.t
            L, Rr = ((r'\left(', r'\right)') if big else ('(', ')')) if q == '(' else ((r'\left[', r'\right]') if big else ('[', ']'))
            return Nd(e.e, L + e.t + Rr, True, e.t)
        raise ValueError(src)
    m = re.match(r'^(.*?)(<=|>=|<|>|=)(.*)$', src.replace(' ', ''))
    l, op, r = m.group(1), m.group(2), m.group(3)
    def side(t):
        st['i'] = 0; toks[:] = re.findall(TK, t); assert ''.join(toks) == t, src
        n = expr(); assert st['i'] == len(toks), src
        return n
    L = side(l); Rr = side(r)
    return {'t': L.t + OPS[op] + Rr.t, 'L': L.e, 'R': Rr.e, 'op': op, 'm': st['m'], 'src': src}
def D(src): return '$' + Q(src)['t'] + '$'
def sis(*rows):
    """sistema; si hi ha fraccions, separa més les files"""
    sep = r'\\[9pt] ' if any('frac' in r for r in rows) else r'\\[2pt] '
    return r'\begin{cases}' + sep.join(rows) + r'\end{cases}'
def SY(*src): return '$' + sis(*[Q(s)['t'] for s in src]) + '$'
_tasks = tasks
def tasks(n, items, start=None, gap=None):
    """apartats amb sistemes: més espai entre files (més encara si hi ha fraccions)"""
    if gap is None and any('cases' in i for i in items): gap = '16pt' if any('frac' in i for i in items) else '9pt'
    return _tasks(n, items, start, gap)

def tl(v):
    v = sp.nsimplify(v)
    if v.is_Rational:
        if v.q == 1: return str(v.p)
        return ('-' if v < 0 else '') + r'\frac{%d}{%d}' % (abs(v.p), v.q)
    return sp.latex(v)
def XY(a, b): return R('x=%s,\\ y=%s' % (tl(a), tl(b)))
def mono(c, v, first):
    c = sp.Rational(c)
    if c == 0: return ''
    s = '-' if c < 0 else ('' if first else '+')
    a = abs(c)
    return s + ('' if (a == 1 and v) else tl(a)) + v

# ---------------------------------------------------------------------
# sistemes lineals
def lin2(src):
    """forma ax+by=c amb enters (a>0, o b>0 si a=0)"""
    e = Q(src); P = sp.expand(e['L'] - e['R'])
    a, b, c = P.coeff(x), P.coeff(y), -P.subs({x: 0, y: 0})
    assert sp.expand(a * x + b * y - c - P) == 0, src
    m = reduce(sp.ilcm, [sp.Rational(t).q for t in (a, b, c)], 1)
    a, b, c = [int(sp.Rational(t) * m) for t in (a, b, c)]
    g = reduce(sp.igcd, [a, b, c]) or 1
    if a < 0 or (a == 0 and b < 0): g = -g
    return a // g, b // g, c // g
def lt(a, b, c): return (mono(a, 'x', True) + mono(b, 'y', not a) or '0') + '=' + str(c)
def solve2(e1, e2):
    E = [Q(s) for s in (e1, e2)]
    return sp.solve([s['L'] - s['R'] for s in E], [x, y], dict=True)
def ls(e1, e2, sol):
    got = solve2(e1, e2)
    assert len(got) == 1 and got[0][x] == sp.sympify(sol[0]) and got[0][y] == sp.sympify(sol[1]), (e1, e2, got)
    NCHK[0] += 1
def kind(e1, e2, k):
    E = [Q(s) for s in (e1, e2)]
    A, b = sp.linear_eq_to_matrix([s['L'] - s['R'] for s in E], [x, y])
    r, ra = A.rank(), A.row_join(b).rank()
    got = 'SCD' if r == ra == 2 else 'SCI' if r == ra else 'SI'
    assert got == k, (e1, e2, got); NCHK[0] += 1
def lsr(e1, e2, sol, red=True):
    """solució d'un sistema lineal (amb la forma reduïda si cal)"""
    ls(e1, e2, sol)
    f = [lin2(s) for s in (e1, e2)]
    pre = '$' + sis(lt(*f[0]), lt(*f[1])) + r'$: ' if red else ''
    return pre + XY(*sol)

# sistemes no lineals
def nls(e1, e2, sols):
    got = solve2(e1, e2)
    got = {(sp.nsimplify(g[x]), sp.nsimplify(g[y])) for g in got if g[x].is_real and g[y].is_real}
    exp = {(sp.sympify(a), sp.sympify(b)) for a, b in sols}
    assert got == exp, (e1, e2, got, exp); NCHK[0] += 1
def pts(sols): return R(r',\ '.join('(%s,\\,%s)' % (tl(a), tl(b)) for a, b in sols)) if sols else R(r'\text{%s}' % T('no té solució', 'no tiene solución'))

# ---------------------------------------------------------------------
# inequacions
def toset(s):
    if s == 'R': return sp.S.Reals
    if s == '0': return sp.S.EmptySet
    out = sp.S.EmptySet
    for p in s.split('U'):
        mm = re.match(r'^([\[\(])([^,]+),([^,]+)([\]\)])$', p.strip())
        a = -sp.oo if mm.group(2) == '-inf' else sp.Rational(mm.group(2)); b = sp.oo if mm.group(3) == 'inf' else sp.Rational(mm.group(3))
        out = out.union(sp.Interval(a, b, mm.group(1) == '(', mm.group(4) == ')'))
    return out
REL = {'<': sp.StrictLessThan, '<=': sp.LessThan, '>': sp.StrictGreaterThan, '>=': sp.GreaterThan}
def isol(src):
    e = Q(src)
    return sp.solve_univariate_inequality(REL[e['op']](e['L'] - e['R'], 0), x, relational=False)
def ptx(P):
    P = sp.Poly(sp.expand(P), x); n = P.degree(); out = ''
    for i, c in enumerate(P.all_coeffs()):
        c = sp.Rational(c); k = n - i
        if c == 0: continue
        out += mono(c, '' if k == 0 else 'x' if k == 1 else 'x^{%d}' % k, out == '')
    return out or '0'
FLIP = {'<': '>', '<=': '>=', '>': '<', '>=': '<='}
def SET(s):
    """conjunt per a RI: 'R', '0' (buit) o intervals; 'R-a' = R menys un punt"""
    if s == 'R': return [(-INF, False, INF, False)]
    if s == '0': return []
    if s.startswith('R-'): a = F(s[2:]); return [(-INF, False, a, False), (a, False, INF, False)]
    return P(s)
def RIs(s, lo=None, hi=None):
    if s == '0': return R(r'\varnothing')
    if s == 'R': return R(r'\mathbb R')
    if s.startswith('R-'): return R(r'\mathbb R-\{%s\}' % s[2:]) + r'\\[2pt]' + recta(SET(s), lo, hi)
    return RI(s, lo, hi)
BR = r'\\[1pt] '
def iq(src, exp, lo=None, hi=None):
    """inequació: forma reduïda i solució (comprovada amb sympy)"""
    e = Q(src)
    target = toset(exp) if not exp.startswith('R-') else sp.S.Reals - sp.FiniteSet(sp.Rational(exp[2:]))
    assert isol(src) == target, (src, isol(src), exp); NCHK[0] += 1
    Pp = sp.Poly(sp.expand(e['L'] - e['R']), x); d = Pp.degree()
    m = reduce(sp.ilcm, [sp.Rational(c).q for c in Pp.all_coeffs()], e['m'])
    P = sp.expand(m * (e['L'] - e['R'])); op = e['op']
    if d <= 0:
        return '$%s%s0$:' % (tl(P), OPS[op]) + BR + RIs(exp, lo, hi)
    if d == 1:
        a, c = P.coeff(x, 1), P.subs(x, 0)
        s = '$' + mono(a, 'x', True) + OPS[op] + tl(-c) + '$'
        if a != 1:
            o2 = FLIP[op] if a < 0 else op
            s += r' $\Rightarrow x%s%s$' % (OPS[o2], tl(sp.Rational(-c, a)))
            if a < 0: s += T(' (canvia el sentit)', ' (cambia el sentido)')
        return s + ':' + BR + RIs(exp, lo, hi)
    # segon grau: coeficient principal positiu
    if Pp.LC() < 0: P = -P; op = FLIP[op]
    cs = [int(c) for c in sp.Poly(P, x).all_coeffs()]; g = reduce(sp.igcd, cs); P = sp.expand(P / g)
    r = sorted(set(sp.solveset(P, x, sp.S.Reals)), key=float)
    rt = (T('arrels ', 'raíces ') + ', '.join('$%s$' % tl(v) for v in r)) if r else T('sense arrels reals', 'sin raíces reales')
    return '$%s%s0$, %s:' % (ptx(P), OPS[op], rt) + BR + RIs(exp, lo, hi)
def iqs(srcs, exp, lo=None, hi=None):
    """sistema d'inequacions: intersecció (comprovada amb sympy)"""
    S = sp.S.Reals
    for s in srcs: S = S.intersect(isol(s))
    assert S == toset(exp), (srcs, S, exp); NCHK[0] += 1
    return RIs(exp, lo, hi)
def chk(cond, *a):
    assert cond, a; NCHK[0] += 1

S = []

# =====================================================================
# 1. Sistemes lineals. Mètode gràfic
ls('3x+2y=4', 'x-y=3', ('2', '-1'))
chk(not (3 + 2 == 4))
G = [(('x+y=5', 'x-y=1'), ('3', '2'), [C(1, 1, '=', 5), C(1, -1, '=', 1)]), (('2x-y=1', 'x+y=5'), ('2', '3'), [C(2, -1, '=', 1), C(1, 1, '=', 5)]),
     (('x-2y=-4', 'x+y=2'), ('0', '2'), [C(1, -2, '=', -4), C(1, 1, '=', 2)])]
for s_, so, cs in G:
    ls(*s_, so); V, _ = verts(cs); chk(V == [(F(so[0]), F(so[1]))], V)
TV = [(0, 6), (1, 4), (2, 2), (3, 0)]
for a, b in TV: chk(2 * a + b == 6)
kind('2x+3y=5', '4x+6y=10', 'SCI'); kind('x-y=2', '3x-3y=1', 'SI'); kind('x+2y=3', '2x-y=1', 'SCD'); kind('6x+2y=4', '3x+y=5', 'SI')
S.append((T("Sistemes lineals. Mètode gràfic", "Sistemas lineales. Método gráfico"), [
 (1, T(r"Comprova si $(2,-1)$ i $(1,\,1)$ són solució del sistema ", r"Comprueba si $(2,-1)$ y $(1,\,1)$ son solución del sistema ") + SY('3x+2y=4', 'x-y=3') + ".",
     r"$(2,-1)$: $6-2=4$ " + T("i", "y") + r" $2+1=3$: " + R(r"\text{%s}" % T('sí', 'sí')) + r". \quad $(1,\,1)$: $3+2=5\neq4$: " + R(r"\text{no}") + "."),
 (1, T(r"Troba quatre solucions de l'equació $2x+y=6$ amb una taula de valors i representa-les. Què formen?", r"Halla cuatro soluciones de la ecuación $2x+y=6$ con una tabla de valores y represéntalas. ¿Qué forman?"),
     T(r"$y=6-2x$: ", r"$y=6-2x$: ") + R(r',\ '.join('(%d,\\,%d)' % p for p in TV)) + T(r". Totes estan sobre una recta.", r". Todas están sobre una recta.") + r'\\[2pt]' + fig([C(2, 1, '=', 6)], (-1, 5, -1, 7), wd=3.2, hmax=3.4, labels=False)),
 (2, T("Resol gràficament els sistemes:", "Resuelve gráficamente los sistemas:") + tasks(3, [SY(*s_) for s_, _, _ in G])
     + recorda(T(r"Fes una taula de valors amb dos punts de cada recta. La solució és el punt de tall.", r"Haz una tabla de valores con dos puntos de cada recta. La solución es el punto de corte.")),
     tasks(3, [XY(*so) + r'\\[2pt]' + fig(cs, (-2, 6, -2, 6), wd=3.6, hmax=3.6) for _, so, cs in G])),
 (2, T("Classifica els sistemes sense resoldre'ls:", "Clasifica los sistemas sin resolverlos:") + tasks(3, [SY('2x+3y=5', '4x+6y=10'), SY('x-y=2', '3x-3y=1'), SY('x+2y=3', '2x-y=1')]),
     tasks(3, [r"$\frac24=\frac36=\frac5{10}$: " + R(r"\text{SCI}"), r"$\frac13=\frac{-1}{-3}\neq\frac21$: " + R(r"\text{SI}"), r"$\frac12\neq\frac2{-1}$: " + R(r"\text{SCD}")])),
 (3, T(r"Troba el valor de $k$ perquè el sistema $" + sis('kx+2y=4', '3x+y=5') + "$ siga incompatible.", r"Halla el valor de $k$ para que el sistema $" + sis('kx+2y=4', '3x+y=5') + "$ sea incompatible."),
     T(r"Les rectes han de ser paral·leles: $\frac k3=\frac21\Rightarrow" + Rm("k=6") + r"$; i com que $\frac45\neq2$, no són la mateixa recta.",
       r"Las rectas tienen que ser paralelas: $\frac k3=\frac21\Rightarrow" + Rm("k=6") + r"$; y como $\frac45\neq2$, no son la misma recta.")),
]))

# =====================================================================
# 2. Mètodes de substitució, igualació i reducció
E21 = [('y=2x-3', '3x+y=7', (2, 1)), ('x+3y=10', '2x-y=6', (4, 2)), ('x=3y-1', '2x+y=12', (5, 2)), ('y=5-x', '3x-2y=5', (3, 2))]
E22 = [('y=x+4', 'y=3x', (2, 6)), ('x=2y-1', 'x=8-y', (5, 3)), ('y=2x-1', 'y=-x+5', (2, 3)), ('x=4-y', 'x=2y+1', (3, 1))]
E23 = [('2x+3y=12', '2x-y=4', (3, 2)), ('3x+2y=7', '5x-3y=18', (3, -1)), ('4x+3y=1', '3x-2y=5', (1, -1)), ('5x+2y=1', '3x-4y=11', (1, -2))]
for a, b, so in E21 + E22 + E23: ls(a, b, so)
ls('x+y=9', 'x-y=3', (6, 3)); kind('2x-4y=6', '-x+2y=-3', 'SCI'); kind('x+y=3', '2x+2y=7', 'SI')
S.append((T("Mètodes de substitució, igualació i reducció", "Métodos de sustitución, igualación y reducción"), [
 (1, T("Resol pel mètode de substitució:", "Resuelve por el método de sustitución:") + tasks(4, [SY(a, b) for a, b, _ in E21]),
     tasks(2, [r"$3x+2x-3=7$: " + XY(2, 1), r"$x=10-3y\Rightarrow 20-6y-y=6$: " + XY(4, 2), r"$2(3y-1)+y=12\Rightarrow7y=14$: " + XY(5, 2), r"$3x-2(5-x)=5\Rightarrow5x=15$: " + XY(3, 2)])),
 (1, T("Resol pel mètode d'igualació:", "Resuelve por el método de igualación:") + tasks(4, [SY(a, b) for a, b, _ in E22]),
     tasks(2, [r"$x+4=3x$: " + XY(2, 6), r"$2y-1=8-y$: " + XY(5, 3), r"$2x-1=-x+5$: " + XY(2, 3), r"$4-y=2y+1$: " + XY(3, 1)])),
 (2, T("Resol pel mètode de reducció:", "Resuelve por el método de reducción:") + tasks(4, [SY(a, b) for a, b, _ in E23])
     + recorda(T(r"Multiplica les equacions perquè una incògnita tinga el mateix coeficient (o l'oposat) i resta-les (o suma-les).", r"Multiplica las ecuaciones para que una incógnita tenga el mismo coeficiente (o el opuesto) y réstalas (o súmalas).")),
     tasks(2, [T("Restant", "Restando") + r": $4y=8$; " + XY(3, 2), r"$3E_1+2E_2$: $19x=57$; " + XY(3, -1), r"$2E_1+3E_2$: $17x=17$; " + XY(1, -1), r"$2E_1+E_2$: $13x=13$; " + XY(1, -2)])),
 (2, T(r"Resol el sistema ", r"Resuelve el sistema ") + SY('x+y=9', 'x-y=3') + T(r" pels tres mètodes algebraics i comprova que obtens la mateixa solució.", r" por los tres métodos algebraicos y comprueba que obtienes la misma solución."),
     T(r"Substitució: $x=9-y\Rightarrow9-2y=3$. Igualació: $9-y=3+y$. Reducció: sumant, $2x=12$. En tots tres: ", r"Sustitución: $x=9-y\Rightarrow9-2y=3$. Igualación: $9-y=3+y$. Reducción: sumando, $2x=12$. En los tres: ") + XY(6, 3) + "."),
 (2, T("Resol i classifica:", "Resuelve y clasifica:") + tasks(2, [SY('2x-4y=6', '-x+2y=-3'), SY('x+y=3', '2x+2y=7')]),
     tasks(1, [T(r"La 1a és $-2$ per la 2a: ", r"La 1ª es $-2$ por la 2ª: ") + R(r"\text{SCI}") + T(r", amb infinites solucions $x=3+2y$ (per exemple, $(3,\,0)$, $(5,\,1)$\ldots).", r", con infinitas soluciones $x=3+2y$ (por ejemplo, $(3,\,0)$, $(5,\,1)$\ldots)."),
               T(r"Restant el doble de la 1a: $0=1$, impossible: ", r"Restando el doble de la 1ª: $0=1$, imposible: ") + R(r"\text{SI}") + "."])),
]))

# =====================================================================
# 3. Sistemes amb parèntesis i denominadors
E31 = [('3(x-1)+y=6', 'x-2(y+1)=-6', (2, 3)), ('2(x+1)-y=7', 'x+3(y-2)=0', (3, 1)), ('5(x-y)+2y=13', '2(x+y)-3x=-4', (2, -1))]
E32 = [('x/3+y/2=4', 'x/2-y/4=2', (6, 4)), ('x/2+y/3=3', 'x-y=1', (4, 3)), ('x/2+y=5', '(x+2)/3-(y-1)/2=1', (4, 3))]
E33 = [('(x+1)/2+y/3=2', '2(x-y)=x-3', ('3/2', '9/4')), ('(x-1)/2+(y+1)/3=2', '2(x+y)-(x-3)=10', (3, 2)),
       ('(x-y)/2+y=4', '(x+y)/3-(x-y)/6=1', (9, -1)), ('x/5-y/2=0', '(x+1)/3+(y-2)/4=2', (5, 2))]
E34 = [('(x+2)/3=(y+1)/2', '2x-y=5', (4, 3)), ('(x+y)/2+(x-y)/4=5/2', '2(x+1)-3(y-1)=8', (3, 1)), ('(x-1)/3+(y+3)/2=4/3', '3(x+y)-2(x-y)=-3', (2, -1))]
S.append((T("Sistemes amb parèntesis i denominadors", "Sistemas con paréntesis y denominadores"), [
 (2, T("Resol (primer trau els parèntesis):", "Resuelve (primero quita los paréntesis):") + tasks(3, [SY(a, b) for a, b, _ in E31]),
     tasks(1, [lsr(a, b, so) for a, b, so in E31])),
 (2, T("Resol (primer elimina els denominadors):", "Resuelve (primero elimina los denominadores):") + tasks(3, [SY(a, b) for a, b, _ in E32])
     + recorda(T(r"Multiplica cada equació pel m.c.m. dels seus denominadors i reduïx-la a la forma $ax+by=c$.", r"Multiplica cada ecuación por el m.c.m. de sus denominadores y redúcela a la forma $ax+by=c$.")),
     tasks(1, [lsr(a, b, so) for a, b, so in E32])),
 (3, T("Resol:", "Resuelve:") + tasks(2, [SY(a, b) for a, b, _ in E33]),
     tasks(1, [lsr(a, b, so) for a, b, so in E33])),
 (3, T("Resol:", "Resuelve:") + tasks(3, [SY(a, b) for a, b, _ in E34]),
     tasks(1, [lsr(a, b, so) for a, b, so in E34])),
]))

# =====================================================================
# 4. Sistemes no lineals
N41 = [('x+y=5', 'x^2+y^2=13', [(2, 3), (3, 2)]), ('x-y=2', 'xy=15', [(5, 3), (-3, -5)]), ('y=x^2-4', 'y=2x-1', [(3, 5), (-1, -3)])]
N42 = [('x^2+y^2=25', 'x^2-y^2=7', [(4, 3), (4, -3), (-4, 3), (-4, -3)]), ('x^2+2y^2=6', '3x^2-y^2=11', [(2, 1), (2, -1), (-2, 1), (-2, -1)])]
N43 = [('x^2+y^2=10', 'x+y=4', [(1, 3), (3, 1)]), ('y=x^2-2x', 'y=x+4', [(4, 8), (-1, 3)]), ('x-y=1', 'xy=6', [(3, 2), (-2, -3)]), ('x+y=6', 'x^2-y=6', [(3, 3), (-4, 10)])]
for a, b, so in N41 + N42 + N43: nls(a, b, so)
nls('x^2+y^2=4', 'y=x+3', [])
S.append((T("Sistemes no lineals", "Sistemas no lineales"), [
 (2, T("Resol pel mètode de substitució:", "Resuelve por el método de sustitución:") + tasks(3, [SY(a, b) for a, b, _ in N41]),
     tasks(1, [r"$x^2+(5-x)^2=13\Rightarrow x^2-5x+6=0$: " + pts(N41[0][2]), r"$(y+2)y=15\Rightarrow y^2+2y-15=0$: " + pts(N41[1][2]), r"$x^2-4=2x-1\Rightarrow x^2-2x-3=0$: " + pts(N41[2][2])])),
 (2, T("Resol pel mètode de reducció:", "Resuelve por el método de reducción:") + tasks(2, [SY(a, b) for a, b, _ in N42]),
     tasks(1, [T("Sumant", "Sumando") + r": $2x^2=32\Rightarrow x=\pm4$, $y=\pm3$: " + pts(N42[0][2]), T("La 1a més el doble de la 2a", "La 1ª más el doble de la 2ª") + r": $7x^2=28\Rightarrow x=\pm2$, $y=\pm1$: " + pts(N42[1][2])])),
 (2, T("Resol:", "Resuelve:") + tasks(4, [SY(a, b) for a, b, _ in N43]),
     tasks(1, [r"$x^2+(4-x)^2=10\Rightarrow x^2-4x+3=0$: " + pts(N43[0][2]), r"$x^2-2x=x+4\Rightarrow x^2-3x-4=0$: " + pts(N43[1][2]),
               r"$(y+1)y=6\Rightarrow y^2+y-6=0$: " + pts(N43[2][2]), r"$x^2-(6-x)=6\Rightarrow x^2+x-12=0$: " + pts(N43[3][2])])),
 (2, T(r"Sense dibuixar, esbrina si la recta $y=x+3$ talla la circumferència $x^2+y^2=4$.", r"Sin dibujar, averigua si la recta $y=x+3$ corta a la circunferencia $x^2+y^2=4$."),
     r"$x^2+(x+3)^2=4\Rightarrow2x^2+6x+5=0$, $\Delta=36-40<0$: " + R(r"\text{%s}" % T('no la talla', 'no la corta')) + T(r" (el sistema no té solució).", r" (el sistema no tiene solución).")),
]))

# =====================================================================
# 5. Problemes amb sistemes lineals
for a, b, so in [('x+y=28', 'x-y=4', (16, 12)), ('3x+2y=33', '2x+3y=27', (9, 3)), ('x+y=30', '4x+2y=100', (20, 10)), ('x+y=11', '9x-9y=27', (7, 4)),
                 ('x+y=20', '8x+12y=188', (13, 7)), ('x-y=30', 'x+10=2(y+10)', (50, 20)), ('x+y=25', 'x+2y=38', (12, 13))]:
    ls(a, b, so)
S.append((T("Problemes amb sistemes lineals", "Problemas con sistemas lineales"), [
 (1, T(r"En una classe hi ha 28 alumnes, i el nombre de xiques supera en 4 el de xics. Quantes xiques i quants xics hi ha?", r"En una clase hay 28 alumnos, y el número de chicas supera en 4 al de chicos. ¿Cuántas chicas y cuántos chicos hay?"),
     SY('x+y=28', 'x-y=4') + ": " + R(r"16\ \text{%s}\ 12\ \text{%s}" % (T('xiques i', 'chicas y'), T('xics', 'chicos'))) + "."),
 (1, T(r"En un aparcament hi ha 30 vehicles entre cotxes i motos, i en total 100 rodes. Quants n'hi ha de cada tipus?", r"En un aparcamiento hay 30 vehículos entre coches y motos, y en total 100 ruedas. ¿Cuántos hay de cada tipo?"),
     SY('x+y=30', '4x+2y=100') + ": " + R(r"20\ \text{%s}\ 10\ \text{motos}" % T('cotxes i', 'coches y')) + "."),
 (1, T(r"Tinc 25 monedes d'1 € i de 2 €, que fan 38 €. Quantes en tinc de cada classe?", r"Tengo 25 monedas de 1 € y de 2 €, que suman 38 €. ¿Cuántas tengo de cada clase?"),
     SY('x+y=25', 'x+2y=38') + ": " + R(r"12\ \text{%s}\ 13\ \text{%s}" % (T("d'1 € i", 'de 1 € y'), T('de 2 €', 'de 2 €'))) + "."),
 (2, T(r"Tres entrades d'adult i dues d'infant costen 33 €, i dues d'adult i tres d'infant, 27 €. Quant costa cada entrada?", r"Tres entradas de adulto y dos de niño cuestan 33 €, y dos de adulto y tres de niño, 27 €. ¿Cuánto cuesta cada entrada?"),
     SY('3x+2y=33', '2x+3y=27') + ": " + R(r"\text{%s}\ 9\ \text{€, %s}\ 3\ \text{€}" % (T('adult', 'adulto'), T('infant', 'niño'))) + "."),
 (2, T(r"Un pare té 30 anys més que el seu fill. D'ací a 10 anys, l'edat del pare serà el doble de la del fill. Quants anys té cadascun?", r"Un padre tiene 30 años más que su hijo. Dentro de 10 años, la edad del padre será el doble de la del hijo. ¿Cuántos años tiene cada uno?"),
     SY('x-y=30', 'x+10=2(y+10)') + ": " + R(r"\text{%s}\ 50\ \text{%s}\ 20" % (T('pare', 'padre'), T('anys, fill', 'años, hijo'))) + "."),
 (2, T(r"Les xifres d'un nombre de dues xifres sumen 11. Si les intercanviem, el nombre disminueix 27. Quin és el nombre?", r"Las cifras de un número de dos cifras suman 11. Si las intercambiamos, el número disminuye 27. ¿Cuál es el número?"),
     T(r"$x$ desenes, $y$ unitats: ", r"$x$ decenas, $y$ unidades: ") + r"$" + sis('x+y=11', '(10x+y)-(10y+x)=27') + r"\Rightarrow x-y=3$: " + T("el nombre és ", "el número es ") + R("74") + "."),
 (3, T(r"Volem fer 20 kg d'una mescla de cafè a 9,40 €/kg amb cafè de 8 €/kg i cafè de 12 €/kg. Quants quilos n'hem de posar de cada classe?", r"Queremos hacer 20 kg de una mezcla de café a 9,40 €/kg con café de 8 €/kg y café de 12 €/kg. ¿Cuántos kilos tenemos que poner de cada clase?"),
     r"$" + sis('x+y=20', r'8x+12y=20\cdot9{,}40=188') + r"$: " + R(r"13\ \text{kg %s}\ 7\ \text{kg %s}" % (T('de 8 € i', 'de 8 € y'), T('de 12 €', 'de 12 €'))) + "."),
]))

# =====================================================================
# 6. Problemes amb sistemes no lineals
nls('x+y=14', 'x^2+y^2=100', [(8, 6), (6, 8)]); nls('x+y=16', 'xy=60', [(10, 6), (6, 10)]); nls('x-y=3', 'x^2+y^2=117', [(9, 6), (-6, -9)])
nls('x^2+y^2=169', 'xy=60', [(12, 5), (5, 12), (-12, -5), (-5, -12)]); chk((12 + 5) ** 2 == 169 + 120)
S.append((T("Problemes amb sistemes no lineals", "Problemas con sistemas no lineales"), [
 (2, T(r"Un rectangle té 32 cm de perímetre i 60 cm$^2$ d'àrea. Quant fan els costats?", r"Un rectángulo tiene 32 cm de perímetro y 60 cm$^2$ de área. ¿Cuánto miden los lados?"),
     r"$" + sis('2x+2y=32', 'xy=60') + r"\Rightarrow x(16-x)=60\Rightarrow x^2-16x+60=0$: " + R(r"10\ \text{cm %s}\ 6\ \text{cm}" % T('i', 'y')) + "."),
 (2, T(r"El perímetre d'un rectangle és de 28 m i la diagonal fa 10 m. Quant fan els costats?", r"El perímetro de un rectángulo es de 28 m y la diagonal mide 10 m. ¿Cuánto miden los lados?"),
     r"$" + sis('x+y=14', 'x^2+y^2=100') + r"\Rightarrow x^2-14x+48=0$: " + R(r"8\ \text{m %s}\ 6\ \text{m}" % T('i', 'y')) + "."),
 (2, T(r"Dos nombres es diferencien en 3 i la suma dels seus quadrats és 117. Quins són?", r"Dos números se diferencian en 3 y la suma de sus cuadrados es 117. ¿Cuáles son?"),
     r"$" + sis('x-y=3', 'x^2+y^2=117') + r"\Rightarrow y^2+3y-54=0$: " + R(r"9\ \text{%s}\ 6" % T('i', 'y')) + T(r", o bé ", r", o bien ") + R(r"-6\ \text{%s}\ -9" % T('i', 'y')) + "."),
 (3, T(r"La hipotenusa d'un triangle rectangle fa 13 cm i l'àrea, 30 cm$^2$. Quant fan els catets?", r"La hipotenusa de un triángulo rectángulo mide 13 cm y el área, 30 cm$^2$. ¿Cuánto miden los catetos?"),
     r"$" + sis('x^2+y^2=169', r'\frac{xy}{2}=30') + T(r"$; com que $(x+y)^2=x^2+y^2+2xy=169+120=289$, $x+y=17$ i $xy=60$: ", r"$; como $(x+y)^2=x^2+y^2+2xy=169+120=289$, $x+y=17$ y $xy=60$: ") + R(r"12\ \text{cm %s}\ 5\ \text{cm}" % T('i', 'y')) + "."),
]))

# =====================================================================
# 7. Inequacions de primer grau
I71 = [('3x-7<5', '(-inf,4)'), ('2x+5>=x+3', '[-2,inf)'), ('4-3x>=10', '(-inf,-2]'), ('5x+3>2x-6', '(-3,inf)')]
I72 = [('3(x-2)+1<x+5', '(-inf,5)'), ('2-(x+4)>=3x+6', '(-inf,-2]'), ('2(x-3)-(x+1)>3x-5', '(-inf,-1)'), ('4(x+1)-3(2x-1)<=x+1', '[2,inf)')]
I73 = [('(x+1)/2-(x-3)/3<=1', '(-inf,-3]'), ('x/4-(2x-1)/6>x/3+1', '(-inf,-2)'), ('(x-1)/2-(x+2)/3>=1', '[13,inf)'), ('(x+3)/4-(x-1)/6>=1', '[1,inf)')]
I74 = [('2(x+3)>2x+1', 'R'), ('3(x-1)<3x-5', '0')]
chk(isol('(4+6.5+x)/3>=5') == sp.Interval(sp.Rational(9, 2), sp.oo)); chk(isol('15+0.1x<0.25x') == sp.Interval.open(100, sp.oo))
S.append((T("Inequacions de primer grau", "Inecuaciones de primer grado"), [
 (1, T("Resol i representa la solució:", "Resuelve y representa la solución:") + tasks(4, [D(s) for s, _ in I71])
     + recorda(T(r"Si multipliques o divideixes per un nombre negatiu, la desigualtat canvia de sentit.", r"Si multiplicas o divides por un número negativo, la desigualdad cambia de sentido.")),
     tasks(2, [iq(s, e) for s, e in I71])),
 (2, T("Resol (primer trau els parèntesis):", "Resuelve (primero quita los paréntesis):") + tasks(2, [D(s) for s, _ in I72]),
     tasks(2, [iq(s, e) for s, e in I72])),
 (2, T("Resol (primer elimina els denominadors):", "Resuelve (primero elimina los denominadores):") + tasks(2, [D(s) for s, _ in I73], gap='12pt'),
     tasks(2, [iq(s, e, *((-1, 15) if '13' in e else (None, None))) for s, e in I73])),
 (2, T("Resol i explica què passa:", "Resuelve y explica qué pasa:") + tasks(2, [D(s) for s, _ in I74]),
     tasks(2, [iq(I74[0][0], 'R') + T(": tots els nombres", ": todos los números"), iq(I74[1][0], '0') + T(": cap nombre", ": ningún número")])),
 (2, T(r"En els dos primers exàmens he tret un 4 i un 6,5. Quina nota he de traure com a mínim en el tercer perquè la mitjana siga almenys un 5?", r"En los dos primeros exámenes he sacado un 4 y un 6,5. ¿Qué nota tengo que sacar como mínimo en el tercero para que la media sea al menos un 5?"),
     r"$\dfrac{4+6{,}5+x}{3}\ge5\Rightarrow 10{,}5+x\ge15\Rightarrow" + Rm(r"x\ge4{,}5") + "$."),
 (3, T(r"La companyia A cobra 15 € al mes més 0,10 € per minut, i la B, 0,25 € per minut. A partir de quants minuts al mes és més barata la companyia A?", r"La compañía A cobra 15 € al mes más 0,10 € por minuto, y la B, 0,25 € por minuto. ¿A partir de cuántos minutos al mes es más barata la compañía A?"),
     r"$15+0{,}10x<0{,}25x\Rightarrow15<0{,}15x\Rightarrow" + Rm(r"x>100") + T(r"$: a partir de 100 minuts.", r"$: a partir de 100 minutos.")),
]))

# =====================================================================
# 8. Inequacions de segon grau
I81 = [('x^2-5x+6<0', '(2,3)'), ('x^2-9>=0', '(-inf,-3]U[3,inf)'), ('x^2+3x<=0', '[-3,0]'), ('x^2-x-6>0', '(-inf,-2)U(3,inf)')]
I82 = [('-x^2+2x+3>0', '(-1,3)'), ('-x^2+4x-3>=0', '[1,3]'), ('2x^2+6x>0', '(-inf,-3)U(0,inf)'), ('3x^2-12<=0', '[-2,2]')]
I83 = [('(x-1)^2>=x+5', '(-inf,-1]U[4,inf)'), ('x(x+2)<3', '(-3,1)'), ('(x+2)(x-2)>3x', '(-inf,-1)U(4,inf)'), ('(x+1)^2<2(x+5)', '(-3,3)')]
I84 = [('x^2-6x+9<=0', '[3,3]'), ('x^2+2x+1>0', 'R--1'), ('x^2+4>0', 'R'), ('x^2+2x+5<0', '0')]
chk(isol('x(x+2)<15').intersect(sp.Interval.open(0, sp.oo)) == sp.Interval.open(0, 3))
S.append((T("Inequacions de segon grau", "Inecuaciones de segundo grado"), [
 (2, T("Resol:", "Resuelve:") + tasks(4, [D(s) for s, _ in I81])
     + recorda(T(r"Calcula les arrels i estudia el signe en cada interval. Si $a>0$, la paràbola és negativa entre les arrels i positiva fora.", r"Calcula las raíces y estudia el signo en cada intervalo. Si $a>0$, la parábola es negativa entre las raíces y positiva fuera.")),
     tasks(2, [iq(s, e) for s, e in I81])),
 (2, T("Resol:", "Resuelve:") + tasks(4, [D(s) for s, _ in I82]),
     tasks(2, [iq(s, e) for s, e in I82])),
 (3, T("Resol (primer trau els parèntesis):", "Resuelve (primero quita los paréntesis):") + tasks(2, [D(s) for s, _ in I83]),
     tasks(2, [iq(s, e) for s, e in I83])),
 (3, T("Resol (compte: el polinomi té una arrel doble o no en té):", "Resuelve (cuidado: el polinomio tiene una raíz doble o no tiene):") + tasks(4, [D(s) for s, _ in I84]),
     tasks(2, [iq(s, e) for s, e in I84])),
 (3, T(r"Els costats d'un rectangle fan $x$ i $x+2$ cm. Per a quins valors de $x$ l'àrea és menor que 15 cm$^2$?", r"Los lados de un rectángulo miden $x$ y $x+2$ cm. ¿Para qué valores de $x$ el área es menor que 15 cm$^2$?"),
     r"$x(x+2)<15\Rightarrow x^2+2x-15<0$, " + T("arrels", "raíces") + r" $-5$, $3$: $(-5,\,3)$; " + T(r"com que $x$ és una longitud, ", r"como $x$ es una longitud, ") + R(r"0<x<3") + "."),
]))

# =====================================================================
# 9. Sistemes d'inequacions
I91 = [(['x-3<0', 'x+1>=0'], '[-1,3)'), (['2x+1>5', '3x-2<=10'], '(2,4]'), (['x+4<1', '2x>-2'], '0'), (['5-x<=2', '4x+1>=9'], '[3,inf)')]
I92 = [(['3(x-1)>=x+1', '(x+2)/3<2'], '[2,4)'), (['2x-5<x+1', 'x/2+1>0'], '(-2,6)'), (['2(x-1)>=x-3', '(x+4)/2>x'], '[-1,4)')]
I93 = [(['x^2-9<=0', '2x-1>0'], '(1/2,3]'), (['x^2-4x>0', 'x+2>=0'], '[-2,0)U(4,inf)')]
chk(isol('3+1.2x>=9').intersect(isol('3+1.2x<=15')) == sp.Interval(5, 10))
chk(isol('2x-3>7').intersect(isol('3x+1<25')) == sp.Interval.open(5, 8))
def ss(L): return '$' + sis(*[Q(s)['t'] for s in L]) + '$'
S.append((T("Sistemes d'inequacions", "Sistemas de inecuaciones"), [
 (1, T("Resol els sistemes i representa la solució:", "Resuelve los sistemas y representa la solución:") + tasks(4, [ss(L) for L, _ in I91])
     + recorda(T(r"Resol cada inequació i fes la intersecció de les solucions: dibuixa-les una damunt de l'altra.", r"Resuelve cada inecuación y haz la intersección de las soluciones: dibújalas una encima de la otra.")),
     tasks(2, [iqs(L, e) if e != '0' else T(r"$x<-3$ i $x>-1$: ", r"$x<-3$ y $x>-1$: ") + iqs(L, e) for L, e in I91])),
 (2, T("Resol:", "Resuelve:") + tasks(3, [ss(L) for L, _ in I92]),
     tasks(1, [T(r"$x\ge2$ i $x<4$: ", r"$x\ge2$ y $x<4$: ") + iqs(*I92[0]), T(r"$x<6$ i $x>-2$: ", r"$x<6$ y $x>-2$: ") + iqs(*I92[1]), T(r"$x\ge-1$ i $x<4$: ", r"$x\ge-1$ y $x<4$: ") + iqs(*I92[2])])),
 (3, T("Resol (alguna inequació és de segon grau):", "Resuelve (alguna inecuación es de segundo grado):") + tasks(2, [ss(L) for L, _ in I93]),
     tasks(1, [r"$[-3, 3]\cap\left(\frac12, +\infty\right)$: " + iqs(*I93[0], -1, 4), r"$\big((-\infty, 0)\cup(4, +\infty)\big)\cap[-2, +\infty)$: " + iqs(*I93[1])])),
 (2, T(r"Un taxi cobra 3 € per la baixada de bandera i 1,20 € per quilòmetre. Si volem gastar com a mínim 9 € i com a màxim 15 €, quants quilòmetres podem fer?", r"Un taxi cobra 3 € por la bajada de bandera y 1,20 € por kilómetro. Si queremos gastar como mínimo 9 € y como máximo 15 €, ¿cuántos kilómetros podemos hacer?"),
     r"$" + sis(r'3+1{,}2x\ge9', r'3+1{,}2x\le15') + r"\Rightarrow" + Rm(r"5\le x\le10") + T(r"$: entre 5 i 10 km.", r"$: entre 5 y 10 km.")),
 (3, T(r"Troba els nombres naturals que compleixen alhora que el seu doble menys 3 és major que 7 i que el seu triple més 1 és menor que 25.", r"Halla los números naturales que cumplen a la vez que su doble menos 3 es mayor que 7 y que su triple más 1 es menor que 25."),
     r"$" + sis('2x-3>7', '3x+1<25') + r"\Rightarrow 5<x<8$: " + R(r"x=6,\ x=7") + "."),
]))

# =====================================================================
TITOL = T("Sistemes d'equacions i inequacions", "Sistemas de ecuaciones e inecuaciones")
KW = T("sistemes d'equacions, mètode gràfic, substitució, igualació, reducció, parèntesis, denominadors, sistemes no lineals, problemes, inequacions de primer grau, inequacions de segon grau, sistemes d'inequacions",
       "sistemas de ecuaciones, método gráfico, sustitución, igualación, reducción, paréntesis, denominadores, sistemas no lineales, problemas, inecuaciones de primer grado, inecuaciones de segundo grado, sistemas de inecuaciones")
INTRO_EX = T(r"Resol-los al quadern mostrant tots els passos. Comprova les solucions dels sistemes en les dues equacions i, en els problemes, respon amb una frase.",
             r"Resuélvelos en el cuaderno mostrando todos los pasos. Comprueba las soluciones de los sistemas en las dos ecuaciones y, en los problemas, responde con una frase.")
INTRO_SOL = T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Pots comprovar els sistemes i les inequacions amb els resolutors pas a pas dels apunts interactius de la unitat.",
              r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar los sistemas y las inecuaciones con los resolutores paso a paso de los apuntes interactivos de la unidad.")
build(HERE, 5, TITOL, S, KW, INTRO_EX, INTRO_SOL, extra_pre=r'\usetikzlibrary{calc}' + '\n', lang=LANG, curs='4eso-a')
print(LANG, sum(len(s[1]) for s in S), 'exercicis,', NCHK[0], 'comprovacions')
