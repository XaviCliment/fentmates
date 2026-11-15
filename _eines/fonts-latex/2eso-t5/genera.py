# Genera t5-fitxa-exercicis.tex i t5-fitxa-solucions.tex (2n ESO, Unitat 5: Sistemes d'equacions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 7 seccions segueixen els apartats dels apunts (5.1-5.7).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Les resolucions pels tres mètodes les escriuen m_sub/m_igu/m_red (les de la fitxa de 3r ESO, ../3eso-t6/genera.py), que
# comproven cada pas amb sympy; les solucions escrites a mà es comproven amb cs/ok/nok/same.
# Ús: python3 genera.py && pdflatex t5-fitxa-exercicis.tex (dues vegades) && pdflatex t5-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re
from math import gcd
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- àlgebra i comprovacions ----------
x, y, k = sp.symbols('x y k')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s.replace(',', '.').replace('[', '(').replace(']', ')'), transformations=TR, local_dict={'x': x, 'y': y, 'k': k}) if isinstance(s, str) else s
def EQ(e): l, r = e.split('='); return sp.nsimplify(sp.expand(S(l) - S(r)), rational=True)
def solve2(e1, e2): return sp.solve([EQ(e1), EQ(e2)], [x, y], dict=True)
def cs(e1, e2, want):
    sol = solve2(e1, e2)
    if want == 'SI': assert sol == [], (e1, e2, sol); return
    if want == 'SCI': assert len(sol) == 1 and len(sol[0]) == 1, (e1, e2, sol); return
    assert sol == [{x: sp.nsimplify(want[0]), y: sp.nsimplify(want[1])}], (e1, e2, sol, want)
def ok(e, xv, yv): assert EQ(e).subs({x: sp.nsimplify(xv), y: sp.nsimplify(yv)}) == 0, (e, xv, yv)
def nok(e, xv, yv): assert EQ(e).subs({x: sp.nsimplify(xv), y: sp.nsimplify(yv)}) != 0, (e, xv, yv)
def same(a, b): assert sp.expand(EQ(a) - EQ(b)) == 0, (a, b)

# ---------- escriptura ----------
def fx(c):
    c = Fr(c)
    return str(c.numerator) if c.denominator == 1 else ('-' if c < 0 else '') + r'\tfrac{%d}{%d}' % (abs(c.numerator), c.denominator)
def par(c): c = Fr(c); return '(' + fx(c) + ')' if c < 0 else fx(c)
def term(c, v, first):
    c = Fr(c)
    if c == 0: return ''
    s = '-' if c < 0 else ('' if first else '+')
    a = abs(c)
    return s + (v if v and a == 1 else fx(a) + v)
def lin(a, b, c):
    t = term(a, 'x', True); t2 = term(b, 'y', not t)
    return (t + t2 or '0') + '=' + fx(c)
def tx(s):
    """equació escrita com a l'entrada -> TeX (fraccions a/b dels termes amb \\dfrac, decimals amb coma)"""
    def side(t):
        out = ''
        for j, (sg, p) in enumerate(split_terms(t)):
            m = re.match(r'^(.*)/(\d+)$', p)
            if m and m.group(1).count('(') == m.group(1).count(')'):
                num = m.group(1)
                if num.startswith('(') and num.endswith(')') and num.count('(') == 1: num = num[1:-1]
                p = r'\dfrac{%s}{%s}' % (num, m.group(2))
            out += ('-' if sg == '-' else ('+' if j else '')) + p
        return out
    l, r = s.split('=')
    return (side(l) + '=' + side(r)).replace('*', r'\cdot ').replace(',', '{,}')
def split_terms(t):
    parts, d, cur, sg = [], 0, '', ''
    for i, ch in enumerate(t):
        if ch in '([': d += 1
        if ch in ')]': d -= 1
        if ch in '+-' and d == 0 and i > 0 and t[i - 1] not in '^*/(':
            parts.append((sg, cur)); sg, cur = ch, ''
        elif ch in '+-' and i == 0: sg = ch
        else: cur += ch
    parts.append((sg, cur))
    return parts
def mside(t, m):
    """cada terme multiplicat pel m.c.m.: '(x+1)/2-(y-1)/3', 6 -> '3(x+1)-2(y-1)'"""
    out = ''
    for j, (sg, p) in enumerate(split_terms(t)):
        mm = re.match(r'^(.*)/(\d+)$', p)
        num, den = (mm.group(1), int(mm.group(2))) if mm else (p, 1)
        kq = m // den
        if re.fullmatch(r'\d+', num): q = str(kq * int(num))
        else:
            if len(split_terms(num)) > 1 and not (num.startswith('(') and num.endswith(')') and num.count('(') == 1): num = '(' + num + ')'
            md = re.match(r'^(\d+)([(a-z].*)$', num)
            q = num if kq == 1 else ('%d%s' % (kq * int(md.group(1)), md.group(2)) if md else '%d%s' % (kq, num))
        out += ('-' if sg == '-' else ('+' if j else '')) + q
    return out.replace('*', r'\cdot ')
def SYS(e1, e2): return r'\begin{cases}%s\\ %s\end{cases}' % (tx(e1), tx(e2))
def sysq(e1, e2): return '$' + SYS(e1, e2) + '$'

# ---------- forma reduïda ----------
def std(e):
    """(passos, (a, b, c)) amb a, b, c enters i sense divisor comú"""
    E = EQ(e)
    a, b, c = Fr(str(E.coeff(x))), Fr(str(E.coeff(y))), -Fr(str(E.subs({x: 0, y: 0})))
    assert sp.expand(E - (a * x + b * y - c)) == 0
    st = []
    l, r = e.split('=')
    m = 1
    for d in re.findall(r'/(\d+)', e): m = m * int(d) // gcd(m, int(d))
    if m > 1: st.append(r'\cdot%d:\ %s=%s' % (m, mside(l, m), mside(r, m)))
    dd = 1
    for v in (a, b, c): dd = dd * v.denominator // gcd(dd, v.denominator)
    a, b, c = a * dd, b * dd, c * dd
    g = gcd(gcd(int(a), int(b)), int(c))
    a, b, c = a / g, b / g, c / g
    reorder = m == 1 and re.fullmatch(r'[-+]?\d*[xy][-+]\d*[xy]=-?\d+', e)  # només canvia l'ordre dels termes
    if lin(a, b, c) != tx(e) and not reorder: st.append(lin(a, b, c))
    return st, (a, b, c)
def isov(e):
    """incògnita ja aïllada ('y=2x+1' -> 'y')"""
    m = re.match(r'^([xy])=(.*)$', e)
    return m.group(1) if m and m.group(1) not in m.group(2) else None
def pre(e1, e2, quiet=False):
    """passos per a passar el sistema a forma reduïda"""
    s1, E1 = std(e1); s2, E2 = std(e2)
    if quiet and isov(e1): s1 = []
    if quiet and isov(e2): s2 = []
    out = []
    if s1: out.append(r'$%s\Rightarrow %s$' % (tx(e1), r'\Rightarrow '.join(s1)))
    if s2: out.append(r'$%s\Rightarrow %s$' % (tx(e2), r'\Rightarrow '.join(s2)))
    return out, E1, E2

# ---------- mètodes (mateixa lògica que els apunts interactius) ----------
def co(e, v): return e[0] if v == 'x' else e[1]
def oth(v): return 'y' if v == 'x' else 'x'
def iso(e, v):
    kk, h, c = co(e, v), co(e, oth(v)), e[2]
    N0, N1, den = c, -h, kk
    if den < 0: N0, N1, den = -N0, -N1, -den
    g = gcd(gcd(int(N0), int(N1)), int(den)) or 1
    return dict(v=v, w=oth(v), k=kk, h=h, N0=N0 / g, N1=N1 / g, den=int(den / g), c=c)
def numtex(N0, N1, w):
    if N1 == 0: return fx(N0)
    if N0 == 0: return term(N1, w, True)
    return term(N1, w, True) + term(N0, '', False) if N1 > 0 else fx(N0) + term(N1, w, False)
def isotex(I): n = numtex(I['N0'], I['N1'], I['w']); return n if I['den'] == 1 else r'\tfrac{%s}{%d}' % (n, I['den'])
def isoval(I, val): return (I['N0'] + I['N1'] * val) / I['den']
def isoshow(I):
    s = ''
    if I['k'] != 1: s = term(I['k'], I['v'], True) + '=' + numtex(I['c'], -I['h'], I['w']) + r'\Rightarrow '
    return s + I['v'] + '=' + isotex(I)
def ktimes(c, body, first):
    a = '' if abs(c) == 1 else fx(abs(c)) + (r'\cdot ' if body.startswith(r'\tfrac') else '')
    return ('-' if c < 0 else ('' if first else '+')) + a + body
def kval(c, val, first):
    a = par(val) if abs(c) == 1 else fx(abs(c)) + r'\cdot ' + par(val)
    return ('-' if c < 0 else ('' if first else '+')) + a
def jt(ts):
    out = ''
    for c, v in ts:
        if c: out += term(c, v, not out)
    return out or '0'
def isolate(A, B, w):
    if A == 1: return ''
    s = B / A
    return r'\Rightarrow %s=\tfrac{%s}{%s}' % (w, fx(B), fx(A)) + ('' if A > 0 and B.denominator == 1 and gcd(int(B), int(A)) == 1 else '=' + fx(s))
def back(I, val):
    if I['N1'] == 0: return None
    N0, N1 = I['N0'], I['N1']
    n = kval(N1, val, True) + (term(N0, '', False) if N0 else '') if N1 > 0 else (fx(N0) + kval(N1, val, False) if N0 else kval(N1, val, True))
    return I['v'] + '=' + (n if I['den'] == 1 else r'\tfrac{%s}{%d}' % (n, I['den'])) + '=' + fx(isoval(I, val))
def score(c): return abs(c) + (0.1 if c < 0 else 0)
def m_sub(E1, E2, hint=None):
    best = None
    for i, e in enumerate((E1, E2)):
        for v in ('x', 'y'):
            c = co(e, v)
            if c == 0: continue
            s = score(c) - (1 if hint == (i, v) else 0)
            if best is None or s < best[0]: best = (s, i, v)
    _, i, v = best
    e, o = (E1, E2)[i], (E1, E2)[1 - i]
    I = iso(e, v); w = I['w']
    kv_, kw = co(o, v), co(o, w)
    den = I['den']
    body = '(' + numtex(I['N0'], I['N1'], w) + ')' if den == 1 else isotex(I)
    tw = term(kw, w, True) if kw else ''
    subs = (tw + ktimes(kv_, body, not tw) if v == 'y' else ktimes(kv_, body, True) + (term(kw, w, False) if kw else '')) + '=' + fx(o[2])
    ch = [subs]
    if den > 1:
        b2 = '(' + numtex(I['N0'], I['N1'], w) + ')'; tw2 = term(kw * den, w, True) if kw else ''
        ch.append((tw2 + ktimes(kv_, b2, not tw2) if v == 'y' else ktimes(kv_, b2, True) + (term(kw * den, w, False) if kw else '')) + '=' + fx(o[2] * den))
    tn = [(kv_ * I['N0'], ''), (kv_ * I['N1'], w)] if I['N1'] < 0 else [(kv_ * I['N1'], w), (kv_ * I['N0'], '')]
    ts = ([(kw * den, w)] + tn) if v == 'y' else (tn + [(kw * den, w)])
    ex = jt(ts) + '=' + fx(o[2] * den)
    if ex != ch[-1]: ch.append(ex)
    A = kw * den + kv_ * I['N1']; B = o[2] * den - kv_ * I['N0']
    red = (term(A, w, True) if A else '0' + w) + '=' + fx(B)
    if red != ch[-1]: ch.append(red)
    # comprovació: l'equació substituïda és equivalent a A·w = B
    W, V = sp.Symbol(w), sp.Symbol(v)
    sub_expr = (o[0] * x + o[1] * y - o[2]).subs(V, (sp.Rational(I['N0']) + sp.Rational(I['N1']) * W) / den)
    assert sp.expand(sub_expr * den - (sp.Rational(A) * W - sp.Rational(B))) == 0
    out = ['$' + isoshow(I) + '$', '$' + r'\Rightarrow '.join(ch) + (isolate(A, B, w) if A else '') + '$']
    if A == 0: return out, ('SI' if B else 'SCI')
    val = B / A; vv = isoval(I, val); b = back(I, val)
    if b: out.append('$' + b + '$')
    r = {w: val, v: vv}
    return out, (r['x'], r['y'])
def m_igu(E1, E2):
    best = None
    for v in ('x', 'y'):
        c1, c2 = co(E1, v), co(E2, v)
        if c1 == 0 or c2 == 0: continue
        s = score(c1) + score(c2)
        if best is None or s < best[0]: best = (s, v)
    v = best[1]; I1, I2 = iso(E1, v), iso(E2, v); w = I1['w']
    ch = [isotex(I1) + '=' + isotex(I2)]
    m = I1['den'] * I2['den'] // gcd(I1['den'], I2['den']); k1, k2 = m // I1['den'], m // I2['den']
    if m > 1:
        s1 = numtex(I1['N0'], I1['N1'], w) if k1 == 1 else ktimes(k1, '(' + numtex(I1['N0'], I1['N1'], w) + ')', True)
        s2 = numtex(I2['N0'], I2['N1'], w) if k2 == 1 else ktimes(k2, '(' + numtex(I2['N0'], I2['N1'], w) + ')', True)
        ch.append(s1 + '=' + s2)
        def tl(I, kk): return [(kk * I['N0'], ''), (kk * I['N1'], w)] if I['N1'] < 0 else [(kk * I['N1'], w), (kk * I['N0'], '')]
        e2 = jt(tl(I1, k1)) + '=' + jt(tl(I2, k2))
        if e2 != ch[-1]: ch.append(e2)
    A = I1['N1'] * k1 - I2['N1'] * k2; B = I2['N0'] * k2 - I1['N0'] * k1
    ch.append((term(A, w, True) if A else '0' + w) + '=' + fx(B))
    W = sp.Symbol(w)
    assert sp.expand((sp.Rational(I1['N0']) + sp.Rational(I1['N1']) * W) / I1['den'] - (sp.Rational(I2['N0']) + sp.Rational(I2['N1']) * W) / I2['den'] - (sp.Rational(A) * W - sp.Rational(B)) / m) == 0
    out = ['$' + isoshow(I1) + r',\quad ' + isoshow(I2) + '$', '$' + r'\Rightarrow '.join(ch) + (isolate(A, B, w) if A else '') + '$']
    if A == 0: return out, ('SI' if B else 'SCI')
    val = B / A; b = back(I1, val)
    if b: out.append('$' + b + '$')
    r = {w: val, v: isoval(I1, val)}
    return out, (r['x'], r['y'])
def m_red(E1, E2, elim=None):
    best = None
    for v in ('y', 'x'):
        c1, c2 = co(E1, v), co(E2, v)
        if c1 == 0 or c2 == 0: continue
        l = abs(c1) * abs(c2) / gcd(int(abs(c1)), int(abs(c2)))
        m1, m2 = l / abs(c1), l / abs(c2)
        if (c1 > 0) == (c2 > 0):
            if m1 == 1 and m2 != 1: m1 = -m1
            else: m2 = -m2
        s = abs(m1) + abs(m2) + (0.5 if m1 < 0 else 0) - (10 if elim == v else 0)
        if best is None or s < best[0]: best = (s, v, m1, m2)
    _, v, m1, m2 = best; w = oth(v)
    f1 = [m1 * t for t in E1]; f2 = [m2 * t for t in E2]; sm = [f1[i] + f2[i] for i in range(3)]
    A, B = co(sm, w), sm[2]
    def row(e, hide=None):
        txx = term(e[0], 'x', True) if e[0] and hide != 'x' else ''
        tyy = term(e[1], 'y', not txx) if e[1] and hide != 'y' else ''
        if hide == 'both': return '&0&=&' + fx(e[2])
        return txx + '&' + tyy + '&=&' + fx(e[2])
    lab = lambda m: '' if m == 1 else r'\scriptstyle(\cdot%s)' % par(m)
    arr = r'\begin{array}{lrrcr}' + lab(m1) + '&' + row(f1) + r'\\' + lab(m2) + '&' + row(f2) + r'\\\hline&' + row(sm, v if A else 'both') + r'\end{array}'
    assert co(sm, v) == 0
    if A == 0: return ['$' + arr + '$'], ('SI' if B else 'SCI')
    val = B / A
    i = 0 if score(co(E1, v)) <= score(co(E2, v)) else 1
    e = (E1, E2)[i]; kv_, kw = co(e, v), co(e, w)
    lhs = ((kval(kw, val, True) if kw else '') + term(kv_, v, not kw)) if v == 'y' else (term(kv_, v, True) + (kval(kw, val, False) if kw else ''))
    rhs = e[2] - kw * val
    ch = [lhs + '=' + fx(e[2])]
    if kw: ch.append(term(kv_, v, True) + '=' + fx(rhs))
    out = ['$' + arr + r'\Rightarrow ' + term(A, w, True) + '=' + fx(B) + isolate(A, B, w) + '$', '$' + r'\Rightarrow '.join(ch) + isolate(kv_, rhs, v) + '$']
    r = {w: val, v: rhs / kv_}
    return out, (r['x'], r['y'])
METH = {'sub': m_sub, 'igu': m_igu, 'red': m_red}
def solve(e1, e2, meth, **kw):
    """resolució completa (TeX) i comprovació amb sympy"""
    p, E1, E2 = pre(e1, e2, meth != 'red')
    if meth == 'sub' and 'hint' not in kw and (isov(e1) or isov(e2)): kw['hint'] = (0, isov(e1)) if isov(e1) else (1, isov(e2))
    st, res = METH[meth](E1, E2, **kw)
    want = solve2(e1, e2)
    if res in ('SI', 'SCI'):
        cs(e1, e2, res)
        fin = r'\rest{%s}' % (T('cap solució', 'ninguna solución') if res == 'SI' else T('infinites solucions', 'infinitas soluciones'))
    else:
        assert want == [{x: sp.Rational(res[0]), y: sp.Rational(res[1])}], (e1, e2, res, want)
        fin = r'$\res{x=%s,\ \ y=%s}$' % (fx(res[0]), fx(res[1]))
    return r'\newline '.join(p + st + [fin])
def sist(lst, meth, n=2, ns=1):
    """llista de sistemes -> (enunciats, solucions)"""
    return tasks(n, [sysq(a, b) for a, b, *_ in lst]), tasks(ns, [solve(a, b, meth, **(o[0] if o else {})) for a, b, *o in lst])

# ---------- gràfiques (TikZ) ----------
def graf(lines, pt=None, R=5, sc=0.34, lab=True):
    out = [r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]' % sc,
           r'\draw[muted!25,very thin] (-%d,-%d) grid (%d,%d);' % (R, R, R, R),
           r'\draw[-latex,muted] (-%d.4,0)--(%d.6,0) node[right,font=\scriptsize]{$x$};' % (R, R),
           r'\draw[-latex,muted] (0,-%d.4)--(0,%d.6) node[above,font=\scriptsize]{$y$};' % (R, R)]
    if lab:
        for t in range(-R + 1, R):
            if t and t % 2 == 0: out.append(r'\node[font=\tiny,muted,below] at (%d,0) {%d}; \node[font=\tiny,muted,left] at (0,%d) {%d};' % (t, t, t, t))
    out.append(r'\begin{scope}\clip (-%d,-%d) rectangle (%d,%d);' % (R, R, R, R))
    cols = ['accent', 'teal']
    for j, (a, b, c, *o) in enumerate(lines):
        X = R + 1
        p = ((-X, (c + a * X) / b), (X, (c - a * X) / b)) if b else ((c / a, -X), (c / a, X))
        st = 'dashed,line width=1.6pt' if o and o[0] else 'line width=1.1pt'
        out.append(r'\draw[%s,%s] (%.3f,%.3f)--(%.3f,%.3f);' % (cols[j % 2], st, p[0][0], p[0][1], p[1][0], p[1][1]))
    out.append(r'\end{scope}')
    if pt:
        out.append(r'\fill[navy] (%s,%s) circle (0.22);' % pt)
        out.append(r'\node[font=\scriptsize\bfseries,navy,fill=white,inner sep=1pt,above right] at (%s,%s) {$(%s,%s)$};' % (pt[0], pt[1], pt[0], pt[1]))
    out.append(r'\end{tikzpicture}')
    return '\n'.join(out)
def lineq(e):
    _, (a, b, c) = std(e); return (float(a), float(b), float(c))


S_ = []  # [(títol, [(estrelles, enunciat, solució)])]
SI_, NO_ = T('sí', 'sí'), T('no', 'no')

# =====================================================================
# 1. Equacions de primer grau amb dues incògnites
S_.append((T("Equacions de primer grau amb dues incògnites", "Ecuaciones de primer grado con dos incógnitas"), [
 (1, T(r"Quines d'aquestes equacions són de primer grau amb dues incògnites?", r"¿Cuáles de estas ecuaciones son de primer grado con dos incógnitas?") + tasks(3, [r'$3x-y=2$', r'$x^2+y=1$', r'$xy=4$', r'$x+y=10$', r'$2x+5=3x$', r'$y=4x-1$']),
     tasks(3, [r'\rest{%s}' % SI_, r'no ($x^2$)', r'no ($xy$)', r'\rest{%s}' % SI_, T(r'no (una incògnita)', r'no (una incógnita)'), r'\rest{%s}' % SI_])),
 (1, T(r"Comprova quins d'aquests parells són solució de $2x+3y=12$:", r"Comprueba cuáles de estos pares son solución de $2x+3y=12$:") + tasks(4, [r'$(3,\,2)$', r'$(0,\,4)$', r'$(6,\,1)$', r'$(-3,\,6)$']),
     tasks(4, [r'$6+6=12$: \rest{%s}' % SI_, r'$0+12=12$: \rest{%s}' % SI_, r'$12+3=15$: \rest{%s}' % NO_, r'$-6+18=12$: \rest{%s}' % SI_])),
 (1, T(r"Aïlla la $y$ i completa una taula de valors amb $x=-2,\,-1,\,0,\,1,\,2$:", r"Despeja la $y$ y completa una tabla de valores con $x=-2,\,-1,\,0,\,1,\,2$:") + tasks(2, [r'$x+y=5$', r'$2x-y=1$'])
     + recorda(T(r"Cada parell $(x,\,y)$ de la taula és una solució de l'equació. Una equació amb dues incògnites té infinites solucions.", r"Cada par $(x,\,y)$ de la tabla es una solución de la ecuación. Una ecuación con dos incógnitas tiene infinitas soluciones.")),
     tasks(2, [r'$y=5-x$: \ $y=7,\ 6,\ 5,\ 4,\ 3$', r'$y=2x-1$: \ $y=-5,\ -3,\ -1,\ 1,\ 3$'])),
 (2, T(r"Escriu tres solucions de cada equació:", r"Escribe tres soluciones de cada ecuación:") + tasks(2, [r'$x-3y=6$', r'$4x+2y=10$']),
     tasks(2, [T(r'$x=6+3y$: \ p. ex.\ \rest{$(6,0),\ (9,1),\ (3,-1)$}', r'$x=6+3y$: \ p. ej.\ \rest{$(6,0),\ (9,1),\ (3,-1)$}'), T(r'$y=5-2x$: \ p. ex.\ \rest{$(0,5),\ (1,3),\ (2,1)$}', r'$y=5-2x$: \ p. ej.\ \rest{$(0,5),\ (1,3),\ (2,1)$}')])),
 (2, T("Respon:", "Responde:") + tasks(1, [T(r"Troba $k$ perquè $(-1,\,3)$ siga solució de $4x+ky=8$.", r"Halla $k$ para que $(-1,\,3)$ sea solución de $4x+ky=8$."), T(r"Troba $m$ perquè $(2,\,m)$ siga solució de $5x-2y=4$.", r"Halla $m$ para que $(2,\,m)$ sea solución de $5x-2y=4$.")]),
     tasks(1, [r"$-4+3k=8\Rightarrow 3k=12\Rightarrow\res{k=4}$", r"$10-2m=4\Rightarrow -2m=-6\Rightarrow\res{m=3}$"])),
 (2, T(r"Fes una taula de valors i representa cada recta en uns eixos:", r"Haz una tabla de valores y representa cada recta en unos ejes:") + tasks(2, [r'$x+2y=4$', r'$3x-y=3$']),
     tasks(2, [r'$(0,2),\ (2,1),\ (4,0)$\\[2pt]' + graf([lineq('x+2y=4')]), r'$(0,-3),\ (1,0),\ (2,3)$\\[2pt]' + graf([lineq('3x-y=3')])])),
 (3, T("Respon:", "Responde:") + tasks(1, [T(r"Troba la solució de $3x+2y=21$ en què la $y$ val 3 unitats més que la $x$.", r"Halla la solución de $3x+2y=21$ en la que la $y$ vale 3 unidades más que la $x$."), T(r"En quins punts talla la recta $x-2y=6$ els eixos de coordenades?", r"¿En qué puntos corta la recta $x-2y=6$ los ejes de coordenadas?")]),
     tasks(1, [r"$y=x+3$: \ $3x+2x+6=21\Rightarrow 5x=15\Rightarrow x=3$: \ \rest{$(3,\,6)$}", T(r"Si $y=0$, $x=6$; si $x=0$, $y=-3$: \ \rest{$(6,\,0)$ i $(0,\,-3)$}", r"Si $y=0$, $x=6$; si $x=0$, $y=-3$: \ \rest{$(6,\,0)$ y $(0,\,-3)$}")])),
]))
for p in [(3, 2), (0, 4), (-3, 6)]: ok('2x+3y=12', *p)
nok('2x+3y=12', 6, 1)
for xv in range(-2, 3): ok('x+y=5', xv, 5 - xv); ok('2x-y=1', xv, 2 * xv - 1)
for p in [(6, 0), (9, 1), (3, -1)]: ok('x-3y=6', *p)
for p in [(0, 5), (1, 3), (2, 1)]: ok('4x+2y=10', *p)
ok('4x+4y=8', -1, 3); ok('5x-2y=4', 2, 3)
for p in [(0, 2), (2, 1), (4, 0)]: ok('x+2y=4', *p)
for p in [(0, -3), (1, 0), (2, 3)]: ok('3x-y=3', *p)
cs('3x+2y=21', 'y=x+3', (3, 6)); ok('x-2y=6', 6, 0); ok('x-2y=6', 0, -3)

# =====================================================================
# 2. Sistemes: què són i què representen
S_.append((T("Sistemes de dues equacions amb dues incògnites", "Sistemas de dos ecuaciones con dos incógnitas"), [
 (1, T(r"Comprova si el parell $(2,\,-1)$ és solució de cada sistema:", r"Comprueba si el par $(2,\,-1)$ es solución de cada sistema:") + tasks(2, [sysq('x+y=1', '2x-y=5'), sysq('3x+y=5', 'x-2y=3')])
     + recorda(T(r"Un parell és solució del sistema si compleix \textbf{les dues} equacions alhora.", r"Un par es solución del sistema si cumple \textbf{las dos} ecuaciones a la vez.")),
     tasks(2, [T(r'$2-1=1$ i $4+1=5$: \rest{sí}', r'$2-1=1$ y $4+1=5$: \rest{sí}'), T(r'$6-1=5$, però $2+2=4\neq3$: \rest{no}', r'$6-1=5$, pero $2+2=4\neq3$: \rest{no}')])),
 (1, T(r"Quin d'aquests parells és la solució del sistema ", r"¿Cuál de estos pares es la solución del sistema ") + sysq('x+y=3', '2x-y=3') + r"? \quad $(1,\,2)$, \ $(2,\,1)$, \ $(3,\,0)$",
     T(r"$(1,2)$: $2-2=0\neq3$; \ $(2,1)$: $3$ i $3$ \checkmark; \ $(3,0)$: $6\neq3$. \ La solució és \rest{$(2,\,1)$}.", r"$(1,2)$: $2-2=0\neq3$; \ $(2,1)$: $3$ y $3$ \checkmark; \ $(3,0)$: $6\neq3$. \ La solución es \rest{$(2,\,1)$}.")),
 (1, T(r"Escriu el sistema que correspon a cada enunciat (no cal resoldre'l):", r"Escribe el sistema que corresponde a cada enunciado (no hace falta resolverlo):")
     + tasks(1, [T(r"Dos nombres sumen 15 i la seua diferència és 3.", r"Dos números suman 15 y su diferencia es 3."),
                 T(r"Un nombre és el doble d'un altre i entre els dos sumen 27.", r"Un número es el doble de otro y entre los dos suman 27."),
                 T(r"Dos bolígrafs i un quadern costen 5 €; un bolígraf i tres quaderns, 10 €.", r"Dos bolígrafos y un cuaderno cuestan 5 €; un bolígrafo y tres cuadernos, 10 €.")]),
     tasks(3, [sysq('x+y=15', 'x-y=3'), sysq('x=2y', 'x+y=27'), sysq('2x+y=5', 'x+3y=10')])),
 (2, T(r"Fes una taula de valors de cada equació amb $x=0,\,1,\,2,\,3,\,4,\,5$ i busca la solució comuna del sistema ", r"Haz una tabla de valores de cada ecuación con $x=0,\,1,\,2,\,3,\,4,\,5$ y busca la solución común del sistema ") + sysq('x+y=6', 'x-y=2') + '.',
     T(r"$x+y=6$: $y=6,\,5,\,4,\,3,\,2,\,1$; \ $x-y=2$: $y=-2,\,-1,\,0,\,1,\,2,\,3$. \ El parell comú és \rest{$(4,\,2)$}.", r"$x+y=6$: $y=6,\,5,\,4,\,3,\,2,\,1$; \ $x-y=2$: $y=-2,\,-1,\,0,\,1,\,2,\,3$. \ El par común es \rest{$(4,\,2)$}.")),
 (2, T(r"Escriu un sistema de dues equacions que tinga per solució $x=-2,\ y=5$.", r"Escribe un sistema de dos ecuaciones que tenga por solución $x=-2,\ y=5$."),
     T(r"Per exemple, \rest{$x+y=3$ i $x-y=-7$} (hi ha infinites respostes).", r"Por ejemplo, \rest{$x+y=3$ y $x-y=-7$} (hay infinitas respuestas).")),
 (3, T(r"Troba $a$ i $b$ perquè $(3,\,-2)$ siga la solució del sistema ", r"Halla $a$ y $b$ para que $(3,\,-2)$ sea la solución del sistema ") + r'$\begin{cases}ax+2y=5\\ 4x+by=6\end{cases}$.',
     r"$3a-4=5\Rightarrow\res{a=3}$; \ $12-2b=6\Rightarrow\res{b=3}$"),
]))
cs('x+y=1', '2x-y=5', (2, -1)); ok('3x+y=5', 2, -1); nok('x-2y=3', 2, -1); cs('x+y=3', '2x-y=3', (2, 1)); nok('2x-y=3', 1, 2); nok('2x-y=3', 3, 0)
cs('x+y=15', 'x-y=3', (9, 6)); cs('x=2y', 'x+y=27', (18, 9)); cs('2x+y=5', 'x+3y=10', (1, 3)); cs('x+y=6', 'x-y=2', (4, 2))
cs('x+y=3', 'x-y=-7', (-2, 5)); cs('3x+2y=5', '4x+3y=6', (3, -2))

# =====================================================================
# 3. Substitució
SB1 = [('x=3y', 'x+y=8'), ('y=2x+1', '3x+y=11')]
SB2 = [('x+y=7', '2x-y=2'), ('x-y=1', '3x+2y=13')]
SB3 = [('3x+y=1', '5x-2y=20'), ('2x-y=-4', '4x+3y=2')]
SB4 = [('x+4y=-5', '3x-2y=13'), ('5x-y=13', '2x+3y=12')]
SB5 = [('x+3y=-4', '2x-y=6'), ('3x-y=-7', '5x+2y=3')]
S_.append((T("Mètode de substitució", "Método de sustitución"), [
 (1, T(r"Resol per substitució (una incògnita ja està aïllada):", r"Resuelve por sustitución (una incógnita ya está despejada):") + sist(SB1, 'sub')[0], sist(SB1, 'sub')[1]),
 (1, T(r"Resol per substitució:", r"Resuelve por sustitución:") + sist(SB2, 'sub')[0] + recorda(T(r"Aïlla la incògnita que té coeficient 1 o $-1$ i substitueix-la, \textbf{entre parèntesis}, en l'altra equació.", r"Despeja la incógnita que tiene coeficiente 1 o $-1$ y sustitúyela, \textbf{entre paréntesis}, en la otra ecuación.")), sist(SB2, 'sub')[1]),
 (2, T(r"Resol per substitució:", r"Resuelve por sustitución:") + sist(SB3, 'sub')[0], sist(SB3, 'sub')[1]),
 (2, T(r"Resol per substitució i comprova la solució:", r"Resuelve por sustitución y comprueba la solución:") + sist(SB4, 'sub')[0], sist(SB4, 'sub')[1]),
 (3, T(r"Resol per substitució (compte amb els signes):", r"Resuelve por sustitución (cuidado con los signos):") + sist(SB5, 'sub')[0], sist(SB5, 'sub')[1]),
 (3, T(r"En resoldre ", r"Al resolver ") + sysq('y=3-x', '2x-3y=1') + T(r" un alumne escriu $2x-9-3x=1$. Quin error ha comés? Resol el sistema correctament.", r" un alumno escribe $2x-9-3x=1$. ¿Qué error ha cometido? Resuelve el sistema correctamente."),
     T(r"$-3(3-x)=-9+3x$: el $-3$ multiplica els dos termes. \ ", r"$-3(3-x)=-9+3x$: el $-3$ multiplica los dos términos. \ ") + solve('y=3-x', '2x-3y=1', 'sub')),
]))
for a, b, s in [('x=3y', 'x+y=8', (6, 2)), ('y=2x+1', '3x+y=11', (2, 5)), ('x+y=7', '2x-y=2', (3, 4)), ('x-y=1', '3x+2y=13', (3, 2)), ('3x+y=1', '5x-2y=20', (2, -5)), ('2x-y=-4', '4x+3y=2', (-1, 2)),
                ('x+4y=-5', '3x-2y=13', (3, -2)), ('5x-y=13', '2x+3y=12', (3, 2)), ('x+3y=-4', '2x-y=6', (2, -2)), ('3x-y=-7', '5x+2y=3', (-1, 4)), ('y=3-x', '2x-3y=1', (2, 1))]: cs(a, b, s)

# =====================================================================
# 4. Igualació
IG1 = [('y=x+5', 'y=3x-1'), ('x=2y-3', 'x=y+1')]
IG2 = [('x+y=6', 'x-y=2'), ('y-2x=1', 'y+x=7')]
IG3 = [('2x+y=8', '3x+y=11'), ('x+3y=10', 'x-2y=0')]
IG4 = [('3x-y=7', 'x+2y=0'), ('4x+y=-2', '2x-y=-4')]
IG5 = [('2x+3y=7', '3x-2y=4'), ('5x-2y=1', '3x+4y=11')]
S_.append((T("Mètode d'igualació", "Método de igualación"), [
 (1, T(r"Resol per igualació:", r"Resuelve por igualación:") + sist(IG1, 'igu')[0] + recorda(T(r"Aïlla \textbf{la mateixa} incògnita en les dues equacions i iguala les expressions.", r"Despeja \textbf{la misma} incógnita en las dos ecuaciones e iguala las expresiones.")), sist(IG1, 'igu')[1]),
 (1, T(r"Resol per igualació:", r"Resuelve por igualación:") + sist(IG2, 'igu')[0], sist(IG2, 'igu')[1]),
 (2, T(r"Resol per igualació:", r"Resuelve por igualación:") + sist(IG3, 'igu')[0], sist(IG3, 'igu')[1]),
 (2, T(r"Resol per igualació i comprova la solució:", r"Resuelve por igualación y comprueba la solución:") + sist(IG4, 'igu')[0], sist(IG4, 'igu')[1]),
 (3, T(r"Resol per igualació (apareixeran denominadors):", r"Resuelve por igualación (aparecerán denominadores):") + sist(IG5, 'igu')[0], sist(IG5, 'igu')[1]),
 (3, T(r"Resol el sistema ", r"Resuelve el sistema ") + r'$\begin{cases}y=\dfrac{x+1}{2}\\[6pt] y=\dfrac{2x-1}{3}\end{cases}$' + T(r" pel mètode més adequat.", r" por el método más adecuado."),
     T(r"Igualació: ", r"Igualación: ") + r"$\tfrac{x+1}{2}=\tfrac{2x-1}{3}\Rightarrow 3(x+1)=2(2x-1)\Rightarrow 3x+3=4x-2\Rightarrow x=5$; \ $y=\tfrac{5+1}{2}=3$. \ $\res{x=5,\ \ y=3}$"),
]))
for a, b, s in [('y=x+5', 'y=3x-1', (3, 8)), ('x=2y-3', 'x=y+1', (5, 4)), ('x+y=6', 'x-y=2', (4, 2)), ('y-2x=1', 'y+x=7', (2, 5)), ('2x+y=8', '3x+y=11', (3, 2)), ('x+3y=10', 'x-2y=0', (4, 2)),
                ('3x-y=7', 'x+2y=0', (2, -1)), ('4x+y=-2', '2x-y=-4', (-1, 2)), ('2x+3y=7', '3x-2y=4', (2, 1)), ('5x-2y=1', '3x+4y=11', (1, 2)), ('y=(x+1)/2', 'y=(2x-1)/3', (5, 3))]: cs(a, b, s)
same('3(x+1)=2(2x-1)', '-x=-5')

# =====================================================================
# 5. Reducció
RD1 = [('x+y=9', 'x-y=3'), ('3x+2y=13', 'x-2y=-1')]
RD2 = [('2x+y=7', '2x-3y=-5'), ('5x+3y=11', '2x-3y=-4')]
RD3 = [('x+2y=4', '3x-y=5'), ('4x+3y=10', '2x+5y=12')]
RD4 = [('3x+4y=18', '5x-2y=4'), ('2x-5y=-1', '3x+2y=8')]
RD5 = [('4x+3y=-1', '5x+2y=4'), ('6x-5y=7', '4x-3y=5')]
S_.append((T("Mètode de reducció", "Método de reducción"), [
 (1, T(r"Resol per reducció (els coeficients d'una incògnita ja són oposats):", r"Resuelve por reducción (los coeficientes de una incógnita ya son opuestos):") + sist(RD1, 'red')[0] + recorda(T(r"Si els coeficients d'una incògnita són oposats, en sumar les equacions aquesta incògnita desapareix.", r"Si los coeficientes de una incógnita son opuestos, al sumar las ecuaciones esa incógnita desaparece.")), sist(RD1, 'red')[1]),
 (1, T(r"Resol per reducció:", r"Resuelve por reducción:") + sist(RD2, 'red')[0], sist(RD2, 'red')[1]),
 (2, T(r"Resol per reducció (cal multiplicar una de les equacions):", r"Resuelve por reducción (hay que multiplicar una de las ecuaciones):") + sist(RD3, 'red')[0], sist(RD3, 'red')[1]),
 (2, T(r"Resol per reducció (cal multiplicar les dues equacions):", r"Resuelve por reducción (hay que multiplicar las dos ecuaciones):") + sist(RD4, 'red')[0], sist(RD4, 'red')[1]),
 (3, T(r"Resol per reducció:", r"Resuelve por reducción:") + sist(RD5, 'red')[0], sist(RD5, 'red')[1]),
 (3, T(r"Quin mètode és el més adequat per a cada sistema? Justifica-ho i resol-los.", r"¿Qué método es el más adecuado para cada sistema? Justifícalo y resuélvelos.") + tasks(3, [sysq('y=3x-2', 'y=x+4'), sysq('x+5y=9', '2x-3y=5'), sysq('4x+3y=6', '5x-3y=21')]),
     tasks(1, [T(r'Igualació (la $y$ ja està aïllada en les dues): ', r'Igualación (la $y$ ya está despejada en las dos): ') + solve('y=3x-2', 'y=x+4', 'igu'),
               T(r'Substitució (la $x$ té coeficient 1): ', r'Sustitución (la $x$ tiene coeficiente 1): ') + solve('x+5y=9', '2x-3y=5', 'sub'),
               T(r'Reducció (els coeficients de la $y$ són oposats): ', r'Reducción (los coeficientes de la $y$ son opuestos): ') + solve('4x+3y=6', '5x-3y=21', 'red')])),
]))
for a, b, s in [('x+y=9', 'x-y=3', (6, 3)), ('3x+2y=13', 'x-2y=-1', (3, 2)), ('2x+y=7', '2x-3y=-5', (2, 3)), ('5x+3y=11', '2x-3y=-4', (1, 2)), ('x+2y=4', '3x-y=5', (2, 1)), ('4x+3y=10', '2x+5y=12', (1, 2)),
                ('3x+4y=18', '5x-2y=4', (2, 3)), ('2x-5y=-1', '3x+2y=8', (2, 1)), ('4x+3y=-1', '5x+2y=4', (2, -3)), ('6x-5y=7', '4x-3y=5', (2, 1)),
                ('y=3x-2', 'y=x+4', (3, 7)), ('x+5y=9', '2x-3y=5', (4, 1)), ('4x+3y=6', '5x-3y=21', (3, -2))]: cs(a, b, s)

# =====================================================================
# 6. Mètode gràfic
GR1 = [('x+y=4', 'x-y=-2', (1, 3)), ('2x-y=3', 'x+2y=-1', (1, -1))]
GR2 = [('x+y=6', 'x-y=2', (4, 2)), ('y=x+1', 'y=-x+5', (2, 3))]
GR3 = [('2x+y=4', 'x-y=-1', (1, 2)), ('x+2y=0', '3x-y=7', (2, -1))]
GR4 = [('y=2x-4', 'x+y=-1', (1, -2)), ('x-3y=3', '2x+y=-8', (-3, -2))]
for a, b, s in GR1 + GR2 + GR3 + GR4: cs(a, b, s)
def gsol(a, b, s, R=5): return graf([lineq(a), lineq(b)], s, R=R) + r'\\[2pt] \rest{$x=%d,\ y=%d$}' % s
S_.append((T("Mètode gràfic", "Método gráfico"), [
 (1, T(r"Llig la solució de cada sistema a partir del punt de tall de les dues rectes:", r"Lee la solución de cada sistema a partir del punto de corte de las dos rectas:")
     + tasks(2, [graf([lineq(a), lineq(b)], None, R=5, sc=0.4) for a, b, _ in GR1]),
     tasks(2, [T(r'Les rectes es tallen en $(1,\,3)$: \rest{$x=1,\ y=3$}', r'Las rectas se cortan en $(1,\,3)$: \rest{$x=1,\ y=3$}'), T(r'Les rectes es tallen en $(1,\,-1)$: \rest{$x=1,\ y=-1$}', r'Las rectas se cortan en $(1,\,-1)$: \rest{$x=1,\ y=-1$}')])),
 (1, T(r"Resol gràficament:", r"Resuelve gráficamente:") + tasks(2, [sysq(a, b) for a, b, _ in GR2]) + recorda(T(r"Fes una taula de valors per a cada equació (dos o tres punts), dibuixa les dues rectes en els mateixos eixos i busca el punt de tall.", r"Haz una tabla de valores para cada ecuación (dos o tres puntos), dibuja las dos rectas en los mismos ejes y busca el punto de corte.")),
     tasks(2, [gsol(a, b, s) for a, b, s in GR2])),
 (2, T(r"Resol gràficament i comprova la solució:", r"Resuelve gráficamente y comprueba la solución:") + tasks(2, [sysq(a, b) for a, b, _ in GR3]), tasks(2, [gsol(a, b, s) for a, b, s in GR3])),
 (2, T(r"Resol gràficament:", r"Resuelve gráficamente:") + tasks(2, [sysq(a, b) for a, b, _ in GR4]), tasks(2, [gsol(a, b, s) for a, b, s in GR4])),
 (3, T(r"Representa aquests sistemes. Què hi observes? Quantes solucions tenen?", r"Representa estos sistemas. ¿Qué observas? ¿Cuántas soluciones tienen?") + tasks(2, [sysq('x+y=2', '2x+2y=6'), sysq('x-2y=2', '3x-6y=6')]),
     tasks(2, [graf([lineq('x+y=2'), lineq('2x+2y=6')]) + T(r'\\[2pt] Rectes paral·leles: \rest{cap solució}', r'\\[2pt] Rectas paralelas: \rest{ninguna solución}'),
               graf([lineq('x-2y=2'), lineq('3x-6y=6') + (True,)]) + T(r'\\[2pt] La mateixa recta: \rest{infinites solucions}', r'\\[2pt] La misma recta: \rest{infinitas soluciones}')])),
 (3, T(r"Sense dibuixar-los, digues si aquests sistemes tenen una solució, cap o infinites. Justifica-ho.", r"Sin dibujarlos, di si estos sistemas tienen una solución, ninguna o infinitas. Justifícalo.") + tasks(3, [sysq('x+y=5', 'x+y=8'), sysq('x-y=1', '3x-3y=3'), sysq('x+y=5', 'x-y=1')]),
     tasks(1, [T(r"Dos nombres no poden sumar 5 i 8 alhora: \rest{cap solució} (rectes paral·leles).", r"Dos números no pueden sumar 5 y 8 a la vez: \rest{ninguna solución} (rectas paralelas)."),
               T(r"La segona equació és la primera multiplicada per 3: \rest{infinites solucions} (la mateixa recta).", r"La segunda ecuación es la primera multiplicada por 3: \rest{infinitas soluciones} (la misma recta)."),
               T(r"Sumant: $2x=6$, $x=3$, $y=2$: \rest{una solució} (rectes que es tallen en $(3,\,2)$).", r"Sumando: $2x=6$, $x=3$, $y=2$: \rest{una solución} (rectas que se cortan en $(3,\,2)$).")])),
]))
cs('x+y=2', '2x+2y=6', 'SI'); cs('x-2y=2', '3x-6y=6', 'SCI'); cs('x+y=5', 'x+y=8', 'SI'); cs('x-y=1', '3x-3y=3', 'SCI'); cs('x+y=5', 'x-y=1', (3, 2))

# =====================================================================
# 7. Problemes
PB = [
 (1, T(r"La suma de dos nombres és 56 i la seua diferència és 12. Quins són?", r"La suma de dos números es 56 y su diferencia es 12. ¿Cuáles son?"),
     T(r"$\begin{cases}x+y=56\\ x-y=12\end{cases}\Rightarrow 2x=68\Rightarrow x=34,\ y=22$: \ \rest{34 i 22}", r"$\begin{cases}x+y=56\\ x-y=12\end{cases}\Rightarrow 2x=68\Rightarrow x=34,\ y=22$: \ \rest{34 y 22}"), ('x+y=56', 'x-y=12', (34, 22))),
 (1, T(r"Un nombre és el triple d'un altre i entre els dos sumen 48. Quins són?", r"Un número es el triple de otro y entre los dos suman 48. ¿Cuáles son?"),
     T(r"$\begin{cases}x=3y\\ x+y=48\end{cases}\Rightarrow 4y=48\Rightarrow y=12,\ x=36$: \ \rest{36 i 12}", r"$\begin{cases}x=3y\\ x+y=48\end{cases}\Rightarrow 4y=48\Rightarrow y=12,\ x=36$: \ \rest{36 y 12}"), ('x=3y', 'x+y=48', (36, 12))),
 (1, T(r"En un corral hi ha gallines i conills. En total hi ha 40 caps i 112 potes. Quants animals hi ha de cada tipus?", r"En un corral hay gallinas y conejos. En total hay 40 cabezas y 112 patas. ¿Cuántos animales hay de cada tipo?"),
     T(r"$\begin{cases}x+y=40\\ 2x+4y=112\end{cases}\Rightarrow 2y=32\Rightarrow y=16,\ x=24$: \ \rest{24 gallines i 16 conills}", r"$\begin{cases}x+y=40\\ 2x+4y=112\end{cases}\Rightarrow 2y=32\Rightarrow y=16,\ x=24$: \ \rest{24 gallinas y 16 conejos}"), ('x+y=40', '2x+4y=112', (24, 16))),
 (1, T(r"En un aparcament hi ha cotxes i motos: 30 vehicles i 100 rodes en total. Quants cotxes i quantes motos hi ha?", r"En un aparcamiento hay coches y motos: 30 vehículos y 100 ruedas en total. ¿Cuántos coches y cuántas motos hay?"),
     T(r"$\begin{cases}x+y=30\\ 4x+2y=100\end{cases}\Rightarrow 2x=40\Rightarrow x=20,\ y=10$: \ \rest{20 cotxes i 10 motos}", r"$\begin{cases}x+y=30\\ 4x+2y=100\end{cases}\Rightarrow 2x=40\Rightarrow x=20,\ y=10$: \ \rest{20 coches y 10 motos}"), ('x+y=30', '4x+2y=100', (20, 10))),
 (1, T(r"3 kg de pomes i 2 kg de peres costen 8 €, i 1 kg de pomes i 3 kg de peres costen 5 €. Quant costa el quilo de cada fruita?", r"3 kg de manzanas y 2 kg de peras cuestan 8 €, y 1 kg de manzanas y 3 kg de peras cuestan 5 €. ¿Cuánto cuesta el kilo de cada fruta?"),
     T(r"$\begin{cases}3x+2y=8\\ x+3y=5\end{cases}\Rightarrow x=5-3y\Rightarrow 15-7y=8\Rightarrow y=1,\ x=2$: \ \rest{pomes 2 €/kg, peres 1 €/kg}", r"$\begin{cases}3x+2y=8\\ x+3y=5\end{cases}\Rightarrow x=5-3y\Rightarrow 15-7y=8\Rightarrow y=1,\ x=2$:\newline \rest{manzanas 2 €/kg, peras 1 €/kg}"), ('3x+2y=8', 'x+3y=5', (2, 1))),
 (2, T(r"En una guardiola hi ha 22 monedes, unes de 2 € i altres de 50 cèntims, que sumen 26 €. Quantes n'hi ha de cada tipus?", r"En una hucha hay 22 monedas, unas de 2 € y otras de 50 céntimos, que suman 26 €. ¿Cuántas hay de cada tipo?"),
     T(r"$\begin{cases}x+y=22\\ 2x+0{,}5y=26\end{cases}\Rightarrow 1{,}5x=15\Rightarrow x=10,\ y=12$: \ \rest{10 de 2 € i 12 de 50 cèntims}", r"$\begin{cases}x+y=22\\ 2x+0{,}5y=26\end{cases}\Rightarrow 1{,}5x=15\Rightarrow x=10,\ y=12$: \ \rest{10 de 2 € y 12 de 50 céntimos}"), ('x+y=22', '2x+0,5y=26', (10, 12))),
 (2, T(r"L'entrada d'un cine costa 7 € per als adults i 4 € per als xiquets. Un dia es van vendre 85 entrades i es van recaptar 445 €. Quantes entrades de cada tipus es van vendre?", r"La entrada de un cine cuesta 7 € para los adultos y 4 € para los niños. Un día se vendieron 85 entradas y se recaudaron 445 €. ¿Cuántas entradas de cada tipo se vendieron?"),
     T(r"$\begin{cases}x+y=85\\ 7x+4y=445\end{cases}\Rightarrow 3x=105\Rightarrow x=35,\ y=50$: \ \rest{35 d'adult i 50 de xiquet}", r"$\begin{cases}x+y=85\\ 7x+4y=445\end{cases}\Rightarrow 3x=105\Rightarrow x=35,\ y=50$: \ \rest{35 de adulto y 50 de niño}"), ('x+y=85', '7x+4y=445', (35, 50))),
 (2, T(r"L'edat d'una mare és el quàdruple de la del seu fill. D'ací a 5 anys només serà el triple. Quants anys tenen ara?", r"La edad de una madre es el cuádruple de la de su hijo. Dentro de 5 años solo será el triple. ¿Cuántos años tienen ahora?"),
     T(r"$\begin{cases}x=4y\\ x+5=3(y+5)\end{cases}\Rightarrow 4y+5=3y+15\Rightarrow y=10$: \ \rest{mare 40 anys, fill 10 anys}", r"$\begin{cases}x=4y\\ x+5=3(y+5)\end{cases}\Rightarrow 4y+5=3y+15\Rightarrow y=10$: \ \rest{madre 40 años, hijo 10 años}"), ('x=4y', 'x+5=3(y+5)', (40, 10))),
 (2, T(r"El perímetre d'un rectangle fa 46 m i la base fa 7 m més que l'altura. Quines dimensions té?", r"El perímetro de un rectángulo mide 46 m y la base mide 7 m más que la altura. ¿Qué dimensiones tiene?"),
     T(r"$\begin{cases}2x+2y=46\\ x-y=7\end{cases}\Rightarrow x+y=23\Rightarrow 2x=30$: \ \rest{base 15 m, altura 8 m}", r"$\begin{cases}2x+2y=46\\ x-y=7\end{cases}\Rightarrow x+y=23\Rightarrow 2x=30$: \ \rest{base 15 m, altura 8 m}"), ('2x+2y=46', 'x-y=7', (15, 8))),
 (2, T(r"Un test té 30 preguntes i les has contestades totes. Cada encert val 2 punts i cada errada en resta 1. Si has tret 39 punts, quantes n'has encertat?", r"Un test tiene 30 preguntas y las has contestado todas. Cada acierto vale 2 puntos y cada fallo resta 1. Si has sacado 39 puntos, ¿cuántas has acertado?"),
     T(r"$\begin{cases}x+y=30\\ 2x-y=39\end{cases}\Rightarrow 3x=69\Rightarrow x=23,\ y=7$: \ \rest{23 encerts (i 7 errades)}", r"$\begin{cases}x+y=30\\ 2x-y=39\end{cases}\Rightarrow 3x=69\Rightarrow x=23,\ y=7$: \ \rest{23 aciertos (y 7 fallos)}"), ('x+y=30', '2x-y=39', (23, 7))),
 (2, T(r"En una classe hi ha 28 alumnes. Si arribaren 2 xiques més, hi hauria tantes xiques com xics. Quants xics i quantes xiques hi ha?", r"En una clase hay 28 alumnos. Si llegaran 2 chicas más, habría tantas chicas como chicos. ¿Cuántos chicos y cuántas chicas hay?"),
     T(r"$\begin{cases}x+y=28\\ y+2=x\end{cases}\Rightarrow 2y+2=28\Rightarrow y=13$: \ \rest{15 xics i 13 xiques}", r"$\begin{cases}x+y=28\\ y+2=x\end{cases}\Rightarrow 2y+2=28\Rightarrow y=13$: \ \rest{15 chicos y 13 chicas}"), ('x+y=28', 'y+2=x', (15, 13))),
 (3, T(r"Volem 60 kg de cafè de 7 €/kg barrejant cafè de 9 €/kg amb cafè de 6 €/kg. Quants quilos de cada tipus hi hem de posar?", r"Queremos 60 kg de café de 7 €/kg mezclando café de 9 €/kg con café de 6 €/kg. ¿Cuántos kilos de cada tipo tenemos que poner?"),
     T(r"$\begin{cases}x+y=60\\ 9x+6y=420\end{cases}\Rightarrow 3x=60\Rightarrow x=20,\ y=40$: \ \rest{20 kg de 9 € i 40 kg de 6 €}", r"$\begin{cases}x+y=60\\ 9x+6y=420\end{cases}\Rightarrow 3x=60\Rightarrow x=20,\ y=40$: \ \rest{20 kg de 9 € y 40 kg de 6 €}"), ('x+y=60', '9x+6y=420', (20, 40))),
 (3, T(r"Les xifres d'un nombre de dues xifres sumen 11. Si les intercanviem, el nombre que resulta és 27 unitats menor. Quin és el nombre?", r"Las cifras de un número de dos cifras suman 11. Si las intercambiamos, el número que resulta es 27 unidades menor. ¿Cuál es el número?"),
     r"$\begin{cases}x+y=11\\ 10y+x=10x+y-27\end{cases}\Rightarrow\begin{cases}x+y=11\\ x-y=3\end{cases}\Rightarrow x=7,\ y=4$: \ \rest{74}", ('x+y=11', '10y+x=10x+y-27', (7, 4))),
 (3, T(r"Dues ciutats estan a 75 km. Dos ciclistes ixen alhora, cadascun d'una ciutat, i van l'un cap a l'altre. Un va 5 km/h més ràpid que l'altre i es troben al cap de 3 hores. A quina velocitat va cadascun?", r"Dos ciudades están a 75 km. Dos ciclistas salen a la vez, cada uno de una ciudad, y van el uno hacia el otro. Uno va 5 km/h más rápido que el otro y se encuentran al cabo de 3 horas. ¿A qué velocidad va cada uno?"),
     T(r"$\begin{cases}3x+3y=75\\ x-y=5\end{cases}\Rightarrow x+y=25\Rightarrow x=15,\ y=10$: \ \rest{15 km/h i 10 km/h}", r"$\begin{cases}3x+3y=75\\ x-y=5\end{cases}\Rightarrow x+y=25\Rightarrow x=15,\ y=10$: \ \rest{15 km/h y 10 km/h}"), ('3x+3y=75', 'x-y=5', (15, 10))),
 (3, T(r"Un hotel té 50 habitacions, unes dobles i altres individuals, i en total 87 llits. Quantes habitacions hi ha de cada tipus?", r"Un hotel tiene 50 habitaciones, unas dobles y otras individuales, y en total 87 camas. ¿Cuántas habitaciones hay de cada tipo?"),
     T(r"$\begin{cases}x+y=50\\ 2x+y=87\end{cases}\Rightarrow x=37,\ y=13$: \ \rest{37 dobles i 13 individuals}", r"$\begin{cases}x+y=50\\ 2x+y=87\end{cases}\Rightarrow x=37,\ y=13$: \ \rest{37 dobles y 13 individuales}"), ('x+y=50', '2x+y=87', (37, 13))),
 (3, T(r"El perímetre d'un triangle isòsceles fa 40 cm i cadascun dels costats iguals fa 5 cm més que la base. Quant fan els costats?", r"El perímetro de un triángulo isósceles mide 40 cm y cada uno de los lados iguales mide 5 cm más que la base. ¿Cuánto miden los lados?"),
     T(r"$\begin{cases}2x+y=40\\ x=y+5\end{cases}\Rightarrow 3y+10=40\Rightarrow y=10$: \ \rest{costats iguals 15 cm, base 10 cm}", r"$\begin{cases}2x+y=40\\ x=y+5\end{cases}\Rightarrow 3y+10=40\Rightarrow y=10$: \ \rest{lados iguales 15 cm, base 10 cm}"), ('2x+y=40', 'x=y+5', (15, 10))),
]
for _, _, _, (a, b, s) in PB: cs(a, b, s)
same('10y+x=10x+y-27', '-9x+9y=-27'); same('3(5-3y)+2y=8', '-7y=-7'); same('4y+5=3y+15', 'y=10')
S_.append((T("Problemes amb sistemes d'equacions", "Problemas con sistemas de ecuaciones"), [(st, q + (recorda(T(r"Tria les dues incògnites i escriu què representen, busca dues relacions per a plantejar el sistema, resol-lo i comprova que la solució té sentit en el problema.", r"Elige las dos incógnitas y escribe qué representan, busca dos relaciones para plantear el sistema, resuélvelo y comprueba que la solución tiene sentido en el problema.")) if i == 0 else ''), s) for i, (st, q, s, _) in enumerate(PB)]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("sistemes d'equacions, equacions de primer grau amb dues incògnites, substitució, igualació, reducció, mètode gràfic, problemes",
       'sistemas de ecuaciones, ecuaciones de primer grado con dos incógnitas, sustitución, igualación, reducción, método gráfico, problemas')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW.replace("'", "'"), pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\usepackage{pifont}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T("Sistemes d'equacions", 'Sistemas de ecuaciones')

def build(sol_):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 5: %s' % (t, TIT), capcalera='%s · Unidad 5: %s' % (t, TIT), pdfkeywords=KW, curs='2eso')
        cap = assignatura('2eso') + '{' + ('Soluciones de la ficha · Unidad 5' if sol_ else 'Ficha de ejercicios · Unidad 5') + '}{' + TIT + '}'
    else:
        t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat 5: %s. 2n d'ESO}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 5: %s · 2n d'ESO" % (t, TIT))
        assert "2n d'ESO" in p and 'Unitat 5' in p and 'unitat 5' in p
        cap = r'\capcalera{Matemàtiques}{2n ESO}{' + ('Solucions de la fitxa · Unitat 5' if sol_ else "Fitxa d'exercicis · Unitat 5") + '}{' + TIT + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol_ else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{14}\n\\input{../comu/fentmates.tex}\n\\fmcurs{2eso}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol_:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs calculadores que resolen pas a pas qualsevol sistema pels tres mètodes i el dibuixen.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás calculadoras que resuelven paso a paso cualquier sistema por los tres métodos y lo dibujan.") if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i comprova sempre la solució en les dues equacions. Per al mètode gràfic, fes servir paper quadriculat. Les seccions segueixen l'ordre dels apunts de la unitat (5.1--5.7).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y comprueba siempre la solución en las dos ecuaciones. Para el método gráfico, usa papel cuadriculado. Las secciones siguen el orden de los apuntes de la unidad (5.1--5.7)."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            out.append('\\ex{%d} %s\n\n' % (st, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't5-fitxa-%s%s.tex' % ('solucions' if sol_ else 'exercicis', '-es' if ES else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(x[1]) for x in S_), T('exercicis', 'ejercicios'))
