# Genera t5-fitxa-exercicis.tex i t5-fitxa-solucions.tex (3r ESO, Unitat 5: Equacions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les resolucions de les equacions les escriu sympy (sol) i les solucions escrites a mà es comproven amb ce/chk.
import os, re
from math import gcd
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- àlgebra ----------
x, k = sp.symbols('x k')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s.replace('\\cdot', '*').replace('[', '(').replace(']', ')'), transformations=TR, local_dict={'x': x, 'k': k}) if isinstance(s, str) else s
def chk(l, r): assert sp.expand(S(l) - S(r)) == 0, (l, r, sp.expand(S(l)))
def ce(eq, sols):
    """solucions reals d'una equació: llista, 'totes' (identitat) o [] (cap)"""
    l, r = eq.split('=')
    e = sp.expand(S(l) - S(r))
    if sols == 'totes':
        assert e == 0, (eq, e); return
    assert e != 0, eq
    got = sorted(set(v for v in sp.solve(e, x) if v.is_real), key=float)
    want = sorted(set(sp.nsimplify(S(v) if isinstance(v, str) else sp.Rational(v)) for v in sols), key=float)
    assert got == want, (eq, got, want)
def ntex(c):
    c = sp.Rational(c)
    return str(c.p) if c.q == 1 else ('-' if c < 0 else '') + r'\tfrac{%d}{%d}' % (abs(c.p), c.q)
def pt(e):
    """polinomi en TeX, de grau més alt a més baix"""
    e = sp.expand(S(e))
    if e == 0: return '0'
    if not e.free_symbols: return ntex(e)
    out = ''
    for (m,), c in sp.Poly(e, x).terms():
        lit = '' if m == 0 else ('x' if m == 1 else 'x^{%d}' % m)
        q = abs(sp.Rational(c))
        out += ('-' if c < 0 else ('+' if out else '')) + (ntex(q) if q != 1 or not lit else '') + lit
    return out
def split_terms(t):
    """'(x+1)/2-3' -> [('', '(x+1)/2'), ('-', '3')]"""
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
    """cada terme multiplicat pel m.c.m.: '(x+1)/2-(x-1)/3', 6 -> '3(x+1)-2(x-1)'"""
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
    return re.sub(r'\^(\d+)', r'^{\1}', out).replace('*', r'\cdot ')
def tx(s):
    """equació escrita com a l'entrada -> TeX (les fraccions a/b dels termes, amb \\dfrac)"""
    def side(t):
        parts = split_terms(t)
        out = ''
        for j, (sg, p) in enumerate(parts):
            m = re.match(r'^(.*)/(\d+)$', p)
            if m and m.group(1).count('(') == m.group(1).count(')'):
                num = m.group(1)
                if num.startswith('(') and num.endswith(')') and num.count('(') == 1: num = num[1:-1]
                p = r'\dfrac{%s}{%s}' % (num, m.group(2))
            out += ('-' if sg == '-' else ('+' if j else '')) + p
        return out
    l, r = s.split('=')
    t = side(l) + '=' + side(r)
    t = re.sub(r'\^(\d+)', r'^{\1}', t)
    return t.replace('*', r'\cdot ')

# ---------- resolució automàtica ----------
def rx(v): return ntex(v) if v.is_Rational else sp.latex(v)
def fsol(roots, irr=None):
    """{arrel: multiplicitat} -> \\res{x=..., x=...}; irr: parella irracional ja escrita amb ±"""
    rs = sorted(roots.items(), key=lambda kv: float(kv[0]))
    if not rs and not irr: return r'\res{\text{sense solució}}'
    out, done = [], set()
    for r, m in rs:
        if r in done: continue
        if r < 0 and -r in roots and m == 1 and roots[-r] == 1: out.append(r'x=\pm%s' % rx(-r)); done.add(-r); continue
        out.append('x=%s%s' % (rx(r), r'\ (\text{doble})' if m == 2 else (r'\ (\text{triple})' if m == 3 else '')))
    return r'\res{' + r',\ '.join(out + ([irr] if irr else [])) + '}'
def quad(a, b, c):
    """passos per a ax^2+bx+c=0 (enters, a>0); retorna (passos, arrels)"""
    st = []
    if b == 0 and c == 0: return ['x^{2}=0'], {sp.Integer(0): 2}, None
    if b == 0:
        q = sp.Rational(-c, a)
        st.append('x^{2}=%s' % ntex(q))
        if q < 0: return st, {}, None
        r = sp.sqrt(q)
        if r.is_Rational: return st, {r: 1, -r: 1}, None
        return st, {}, r'x=\pm%s' % sp.latex(r)
    if c == 0:
        st.append(r'x\,(%s)=0' % pt(a * x + b))
        return st, {sp.Integer(0): 1, sp.Rational(-b, a): 1}, None
    D = b * b - 4 * a * c
    st.append(r'\Delta=%s' % D)
    if D < 0: return st, {}, None
    if D == 0:
        r = sp.Rational(-b, 2 * a)
        st.append(r'x=\tfrac{%d}{%d}' % (-b, 2 * a)); return st, {r: 2}, None
    s = sp.sqrt(D)
    if s.is_Integer:
        st.append(r'x=\tfrac{%d\pm%d}{%d}' % (-b, s, 2 * a))
        return st, {sp.Rational(-b + s, 2 * a): 1, sp.Rational(-b - s, 2 * a): 1}, None
    kk, m = s.as_coeff_Mul()
    kk = int(kk); m2 = int(m ** 2)
    g = gcd(gcd(abs(b), kk), 2 * a)
    st.append(r'x=\tfrac{%d\pm\sqrt{%d}}{%d}' % (-b, D, 2 * a))
    num = r'%d\pm%s\sqrt{%d}' % (-b // g, '' if kk // g == 1 else kk // g, m2)
    return st, {}, 'x=' + (num if 2 * a // g == 1 else r'\tfrac{%s}{%d}' % (num, 2 * a // g))
def rufarr(cs, r):
    bot = [cs[0]]; mid = ['']
    for c in cs[1:]:
        m = bot[-1] * r; mid.append(m); bot.append(c + m)
    f = lambda v: '' if v == '' else str(v)
    n = len(cs)
    tab = (r'\begin{array}{r|%s|r}' % ('r' * (n - 1)) + ' & ' + ' & '.join(f(c) for c in cs) + r'\\ '
           + f(r) + ' & ' + ' & '.join(f(m) for m in mid) + r'\\ \hline & ' + ' & '.join(f(c) for c in bot) + r'\end{array}')
    assert bot[-1] == 0
    return tab, bot[:-1]
def sol(eq, show=True):
    """resolució pas a pas (en TeX) de qualsevol equació polinòmica fins a grau 4"""
    l, r = eq.split('=')
    L, R = S(l), S(r)
    m = 1
    for d in re.findall(r'/(\d+)', eq): m = m * int(d) // gcd(m, int(d))
    L2, R2 = sp.expand(L * m), sp.expand(R * m)
    st = []
    if m > 1:
        ms = '%s=%s' % (mside(l, m), mside(r, m))
        chk(ms.replace('\\cdot', '*').replace('{', '(').replace('}', ')').split('=')[0], L2); chk(ms.replace('\\cdot', '*').replace('{', '(').replace('}', ')').split('=')[1], R2)
        st.append(r'\text{m.c.m.}=%d:\ \ %s' % (m, ms))
        if ms != '%s=%s' % (pt(L2), pt(R2)): st.append('%s=%s' % (pt(L2), pt(R2)))
    elif '(' in eq or '[' in eq: st.append('%s=%s' % (pt(L2), pt(R2)))
    E = sp.expand(L2 - R2)
    if E == 0:
        st.append(r'0x=0'); res = r'\res{\text{infinites solucions}}'
    else:
        P = sp.Poly(E, x); deg = P.degree()
        if deg == 0:
            st.append(r'0x=%s' % ntex(-E)); res = r'\res{\text{sense solució}}'
        elif deg == 1:
            a, b = [sp.Rational(c) for c in P.all_coeffs()]
            a1, b1 = sp.Rational(L2.coeff(x, 1)), sp.Rational(L2.coeff(x, 0))
            if not (R2.coeff(x, 1) == 0 and b1 == 0) and a != 1: st.append('%s=%s' % (pt(a * x), ntex(-b)))
            res = r'\res{x=%s}' % ntex(-b / a)
            tail = 'x=%s' % ntex(-b / a)
            if st and (st[-1] == tail or st[-1].endswith(r'\ ' + tail)):
                st[-1] = st[-1][:-len(tail)] + res; res = None
        else:
            cs = [int(c) for c in P.all_coeffs()]
            if cs[0] < 0: cs = [-c for c in cs]
            g = 0
            for c in cs: g = gcd(g, c)
            cs = [c // g for c in cs]
            gen = pt(sum(c * x ** (len(cs) - 1 - i) for i, c in enumerate(cs))) + '=0'
            if gen != pt(L2) + '=' + pt(R2) and not (len(cs) == 3 and cs[1] == 0 and cs[2] != 0): st.append(gen)
            roots, irr = {}, None
            while len(cs) - 1 > 2:
                if cs[-1] == 0:
                    z = 0
                    while cs[-1] == 0 and len(cs) > 2: cs = cs[:-1]; z += 1
                    roots[sp.Integer(0)] = roots.get(sp.Integer(0), 0) + z
                    st.append(r'%s\,(%s)=0' % ('x' if z == 1 else 'x^{%d}' % z, pt(sum(c * x ** (len(cs) - 1 - i) for i, c in enumerate(cs)))))
                    continue
                Pp = sum(c * x ** (len(cs) - 1 - i) for i, c in enumerate(cs))
                cand = [s * d for d in range(1, abs(cs[-1]) + 1) if cs[-1] % d == 0 for s in (1, -1)]
                rr = next(c for c in cand if Pp.subs(x, c) == 0)
                tab, q = rufarr(cs, rr)
                st.append(tab)
                cs = q; roots[sp.Integer(rr)] = roots.get(sp.Integer(rr), 0) + 1
                st.append(r'(%s)(%s)=0' % (pt(x - rr), pt(sum(c * x ** (len(cs) - 1 - i) for i, c in enumerate(cs)))))
            if len(cs) == 3:
                q2, rq, irr = quad(*cs)
                st += [t for t in q2 if not any(u == t or u.endswith(' ' + t) or u.endswith('=0') and False for u in st)]
                for rt, mu in rq.items(): roots[rt] = roots.get(rt, 0) + mu
            if len(cs) == 2: rt = sp.Rational(-cs[1], cs[0]); roots[rt] = roots.get(rt, 0) + 1
            res = fsol({sp.nsimplify(k_): v for k_, v in roots.items()}, irr)
    return '$' + r'\ \Rightarrow\ '.join(st + ([res] if res else [])) + '$'
def eqs(lst, n, ns=None):
    """llista d'equacions -> (enunciats, solucions)"""
    return tasks(n, ['$%s$' % tx(e) for e in lst]), tasks(ns or 1, [sol(e) for e in lst])
def checkall(lst):
    """sol() i sympy han de donar el mateix conjunt de solucions"""
    for e in lst:
        l, r = e.split('=')
        E = sp.expand(S(l) - S(r))
        if E == 0: assert 'infinites' in sol(e); continue
        got = sorted(set(v for v in sp.solve(E, x) if v.is_real), key=float)
        s = sol(e)
        if not got: assert 'sense solució' in s, (e, s); continue
        for v in got:
            t = rx(sp.nsimplify(v))
            assert ('x=%s' % t) in s or (r'\pm' in s) or ('sqrt' in t), (e, t, s)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S_.append(("Equacions i identitats", [
 (1, r"Indica quines igualtats són identitats i quines són equacions:" + tasks(2, [r'$3(x+2)=3x+6$', r'$3x+2=8$', r'$(x+1)^2=x^2+2x+1$', r'$x^2-1=0$', r'$5x-2x=3x$', r'$5x-2=3x$', r'$(x-3)(x+3)=x^2-9$', r'$2(x-1)=2x-1$'])
     + recorda(r"Una \textbf{identitat} es compleix per a qualsevol valor de $x$; una \textbf{equació}, només per a alguns valors (o per a cap)."),
     tasks(2, [r"\rest{Identitat}", r"\rest{Equació} ($x=3$)", r"\rest{Identitat}", r"\rest{Equació} ($x=\pm1$)", r"\rest{Identitat}", r"\rest{Equació} ($x=1$)", r"\rest{Identitat}", r"\rest{Equació} sense solució ($-2\neq-1$)"])),
 (1, r"Comprova si els valors indicats són solució de cada equació:" + tasks(2, [r'$3x-5=x+1$, \ $x=3$', r'$x^2-4x=5$, \ $x=-1$ i $x=5$', r'$2(x-1)=x+4$, \ $x=5$', r'$x^3-2x=4$, \ $x=2$']),
     tasks(2, [r'$4=4$: \rest{sí}', r'$5=5$ i $5=5$: \rest{totes dues}', r'$8\neq9$: \rest{no}', r'$8-4=4$: \rest{sí}'])),
 (1, r"En l'equació $5x^2-3x+1=2x-7$, indica el primer i el segon membre, els termes, la incògnita i el grau.",
     r"1r membre: $5x^2-3x+1$; 2n membre: $2x-7$; termes: $5x^2,\ -3x,\ 1,\ 2x,\ -7$; incògnita: $x$; \rest{grau 2}."),
 (2, r"Indica el grau de cada equació un cop reduïda:" + tasks(2, [r'$x(x+4)=x^2-8$', r'$(x-2)^2=x^2+4$', r'$x^3-x(x^2+1)=2$', r'$(x+1)(x-1)=3x$'])
     + recorda(r"Abans de dir el grau, opera i redueix: els termes de grau alt es poden cancel·lar."),
     tasks(2, [r'$4x=-8$: \rest{grau 1}', r'$-4x=0$: \rest{grau 1}', r'$-x=2$: \rest{grau 1}', r'$x^2-3x-1=0$: \rest{grau 2}'])),
 (2, r"Són equivalents aquestes parelles d'equacions? Justifica-ho." + tasks(1, [r'$2x-3=7$ \ i \ $3x+1=16$', r'$x^2=25$ \ i \ $x=5$']),
     tasks(1, [r"Les dues tenen la solució $x=5$: \rest{sí}.", r"La primera també té la solució $x=-5$: \rest{no}."])),
 (2, r"Escriu una equació de primer grau que tinga la solució $x=-2$ i una equació de segon grau que tinga les solucions $x=3$ i $x=-3$.",
     r"Per exemple, \rest{$x+2=0$} \ (o $3x+1=-5$\ldots) \ i \ \rest{$x^2-9=0$}."),
 (3, r"Troba el valor de $k$ en cada cas:" + tasks(1, [r"$x=3$ és solució de $2x^2-kx+3=0$.", r"$x=-1$ és solució de $kx^3+2x=k-6$."]),
     tasks(1, [r"$18-3k+3=0\Rightarrow\res{k=7}$", r"$-k-2=k-6\Rightarrow -2k=-4\Rightarrow\res{k=2}$"])),
]))
for e, s in [('3x+2=8', [2]), ('x^2-1=0', [1, -1]), ('5x-2=3x', [1]), ('2(x-1)=2x-1', []), ('x^2-4x=5', [-1, 5]), ('3x-5=x+1', [3]), ('x^3-2x=4', [2]),
             ('x(x+4)=x^2-8', [-2]), ('(x-2)^2=x^2+4', [0]), ('x^3-x(x^2+1)=2', [-2]), ('2x-3=7', [5]), ('3x+1=16', [5]), ('x^2=25', [5, -5])]: ce(e, s)
for e in ['3(x+2)=3x+6', '(x+1)^2=x^2+2x+1', '5x-2x=3x', '(x-3)(x+3)=x^2-9']: ce(e, 'totes')
assert sp.solve(18 - 3 * k + 3, k) == [7] and sp.solve(-k - 2 - (k - 6), k) == [2]
assert S('2(5-1)') == 8 and S('5+4') == 9

# =====================================================================
E8 = ['x+7=12', '3x=-21', '5x-4=11', '-2x+9=1', '4x+3=2x+11', '7-3x=x-13', '6x-5=9x+7', '2x-1=5x-1']
E9 = ['3(x-2)=12', '5(x+1)=2x-7', '4-(x+3)=2x-5', '2(3x-1)=4(x+2)']
E10 = ['3(2x-1)-2(x+4)=5x-13', '5-2(3-x)=4(x+1)-11', 'x-[2x-(3-x)]=7', '4(x-3)-(x-5)=2(x+1)']
E11 = ['3(x+2)-x=2(x+3)', '5x-2(x-1)=3x+4', '6x-2(3x+1)=-2', '7x-3(2x-1)=2x+1']
E12 = ['(x+1)^2-(x-1)^2=12', 'x(x+3)-x^2=2x+5']
E13 = ['2[3-2(x+1)]=5-3(2x-1)-x', '(x-3)(x+3)-(x-1)^2=2(x+1)']
S_.append(("Equacions de primer grau", [
 (1, r"Resol:" + eqs(E8, 4)[0] + recorda(r"El que suma passa restant i el que resta passa sumant; el que multiplica tot un membre passa dividint (amb el seu signe)."), eqs(E8, 4, 2)[1]),
 (1, r"Resol traient primer els parèntesis:" + eqs(E9, 2)[0], eqs(E9, 2, 1)[1]),
 (2, r"Resol:" + eqs(E10, 2)[0] + recorda(r"Un signe $-$ davant d'un parèntesi canvia el signe de \textbf{tots} els termes de dins."), eqs(E10, 2, 1)[1]),
 (2, r"Resol i digues quines equacions no tenen solució i quines en tenen infinites:" + eqs(E11, 2)[0], eqs(E11, 2, 1)[1]),
 (2, r"Resol i comprova la solució:" + eqs(E12, 2)[0],
     tasks(1, [sol(E12[0]) + r'. \ Comprovació: $16-4=12$', sol(E12[1]) + r'. \ Comprovació: $40-25=15=2\cdot5+5$'])),
 (3, r"Resol:" + eqs(E13, 1)[0], eqs(E13, 1, 1)[1]),
 (3, r"Troba el valor de $a$ perquè l'equació $3(x-a)=2x+1$ tinga la solució $x=5$.",
     r"$3(5-a)=11\Rightarrow 15-3a=11\Rightarrow\res{a=\tfrac43}$"),
]))
ce('x+7=12', [5]); ce('3x=-21', [-7]); ce('5x-4=11', [3]); ce('-2x+9=1', [4]); ce('4x+3=2x+11', [4]); ce('7-3x=x-13', [5]); ce('6x-5=9x+7', [-4]); ce('2x-1=5x-1', [0])
ce('3(x-2)=12', [6]); ce('5(x+1)=2x-7', [-4]); ce('4-(x+3)=2x-5', [2]); ce('2(3x-1)=4(x+2)', [5])
ce('3(2x-1)-2(x+4)=5x-13', [2]); ce('5-2(3-x)=4(x+1)-11', [3]); ce('x-(2x-(3-x))=7', [-2]); ce('4(x-3)-(x-5)=2(x+1)', [9])
ce('3(x+2)-x=2(x+3)', 'totes'); ce('5x-2(x-1)=3x+4', []); ce('6x-2(3x+1)=-2', 'totes'); ce('7x-3(2x-1)=2x+1', [2])
ce('(x+1)^2-(x-1)^2=12', [3]); ce('x(x+3)-x^2=2x+5', [5]); ce('2(3-2(x+1))=5-3(2x-1)-x', [2]); ce('(x-3)(x+3)-(x-1)^2=2(x+1)', [])
ce('3(x-4/3)=2x+1', [5])

# =====================================================================
E15 = ['x/3=4', 'x/2+x/4=6', 'x-x/3=10', '2x/5-1=3']
E16 = ['(x+2)/3=4', '(x-1)/2=(x+3)/4', '(3x-1)/4=2', 'x/6+1=x/4']
E17 = ['(x+1)/2-(x-1)/3=2', '(x-2)/4-(x-3)/6=1/2', '(2x+1)/3-(x-2)/2=3', 'x-(x+2)/5=(x+6)/2']
E18 = ['(x-1)/3+(x+2)/6=x-2', '3-(x-1)/4=(x+5)/2']
E19 = ['3(x-2)/4-2(x+1)/3=(x-10)/6', 'x/2-(x-1)/3-(x+1)/4=(1-x)/12', '(x+1)/2-(x+3)/4=x/4-1']
S_.append(("Equacions de primer grau amb denominadors", [
 (1, r"Resol:" + eqs(E15, 4)[0], eqs(E15, 4, 2)[1]),
 (1, r"Resol:" + eqs(E16, 4)[0] + recorda(r"Multiplica \textbf{tots} els termes pel m.c.m. dels denominadors (també els que no tenen denominador) i posa els numeradors entre parèntesis."), eqs(E16, 4, 2)[1]),
 (2, r"Resol:" + eqs(E17, 2)[0], eqs(E17, 2, 1)[1]),
 (2, r"Resol:" + eqs(E18, 2)[0], eqs(E18, 2, 1)[1]),
 (3, r"Resol i interpreta el resultat:" + eqs(E19, 1)[0], eqs(E19, 1, 1)[1]),
 (3, r"Un alumne ha resolt l'equació $\dfrac{x-2}{3}-\dfrac{x+1}{2}=1$ així:\quad $2x-4-3x+3=6\ \Rightarrow\ -x=7\ \Rightarrow\ x=-7$. \ On s'ha equivocat? Resol-la correctament.",
     r"El $-$ davant de la segona fracció afecta tot el numerador: $-3(x+1)=-3x-3$. \ $2x-4-3x-3=6\Rightarrow -x=13\Rightarrow\res{x=-13}$."),
]))
ce('x/3=4', [12]); ce('x/2+x/4=6', [8]); ce('x-x/3=10', [15]); ce('2x/5-1=3', [10]); ce('(x+2)/3=4', [10]); ce('(x-1)/2=(x+3)/4', [5]); ce('(3x-1)/4=2', [3]); ce('x/6+1=x/4', [12])
ce('(x+1)/2-(x-1)/3=2', [7]); ce('(x-2)/4-(x-3)/6=1/2', [6]); ce('(2x+1)/3-(x-2)/2=3', [10]); ce('x-(x+2)/5=(x+6)/2', ['34/3'])
ce('(x-1)/3+(x+2)/6=x-2', [4]); ce('3-(x-1)/4=(x+5)/2', [1]); ce('3(x-2)/4-2(x+1)/3=(x-10)/6', [-6]); ce('x/2-(x-1)/3-(x+1)/4=(1-x)/12', 'totes'); ce('(x+1)/2-(x+3)/4=x/4-1', [])
ce('(x-2)/3-(x+1)/2=1', [-13])

# =====================================================================
E23 = ['x^2-36=0', '2x^2-50=0', 'x^2+9=0', '4x^2-9=0', '3x^2=27', 'x^2-7=0']
E24 = ['x^2-5x=0', '3x^2+12x=0', '2x^2=7x', '-x^2+6x=0']
E25 = ['(x+3)(x-3)=7', 'x(x-2)=4-2x', '(2x-1)^2=1', '(x+2)^2-4=3x']
E26 = ['x^2/3=12', 'x^2/4-x/2=0', '(x^2+1)/5=2', '(x^2-2)/2-(x^2+1)/3=1']
E27 = ['(2x+3)(2x-3)-(x+1)^2=2(x^2-x)-10', 'x(x-3)/2-x(x+1)/3=x']
S_.append(("Equacions de segon grau incompletes", [
 (1, r"Escriu cada equació en la forma general $ax^2+bx+c=0$, indica els coeficients $a$, $b$ i $c$ i digues si és completa o incompleta:" + tasks(2, [r'$5x-x^2=6$', r'$3x^2=12$', r'$x(x-4)=0$', r'$(x+1)^2=2x+5$']),
     tasks(1, [r'$x^2-5x+6=0$: \rest{$a=1,\ b=-5,\ c=6$, completa}', r'$3x^2-12=0$: \rest{$a=3,\ b=0,\ c=-12$, incompleta}', r'$x^2-4x=0$: \rest{$a=1,\ b=-4,\ c=0$, incompleta}', r'$x^2-4=0$: \rest{$a=1,\ b=0,\ c=-4$, incompleta}'])),
 (1, r"Resol:" + eqs(E23, 3)[0] + recorda(r"En $ax^2+c=0$ aïllem $x^2$ i fem l'arrel: hi ha \textbf{dues} solucions, $x=\pm\sqrt{\ }$, o cap si el nombre és negatiu."), eqs(E23, 3, 2)[1]),
 (1, r"Resol:" + eqs(E24, 4)[0] + recorda(r"En $ax^2+bx=0$ traiem factor comú $x$: una solució sempre és $x=0$. No dividisques entre $x$!"), eqs(E24, 4, 1)[1]),
 (2, r"Redueix i resol:" + eqs(E25, 2)[0], eqs(E25, 2, 1)[1]),
 (2, r"Resol:" + eqs(E26, 2)[0], eqs(E26, 2, 1)[1]),
 (3, r"Resol:" + eqs(E27, 1)[0], eqs(E27, 1, 1)[1]),
 (3, r"La Marta resol $5x^2=3x$ dividint els dos membres entre $x$ i obté $5x=3$, és a dir, $x=\tfrac35$. Què ha fet malament? Resol-la correctament.",
     r"En dividir entre $x$ perd la solució $x=0$. \ $5x^2-3x=0\Rightarrow x(5x-3)=0\Rightarrow\res{x=0,\ x=\tfrac35}$."),
 (3, r"Escriu una equació de segon grau incompleta que tinga per solucions:" + tasks(2, [r'$4$ i $-4$', r'$0$ i $3$']),
     tasks(2, [r'P. ex.\ \rest{$x^2-16=0$}', r'P. ex.\ \rest{$x^2-3x=0$}'])),
]))
checkall(E23 + E24 + E25 + E26 + E27)
ce('5x-x^2=6', [2, 3]); ce('3x^2=12', [2, -2]); ce('(x+1)^2=2x+5', [2, -2]); chk('(x+1)^2-2x-5', 'x^2-4')
ce('x^2-36=0', [6, -6]); ce('2x^2-50=0', [5, -5]); ce('x^2+9=0', []); ce('4x^2-9=0', ['3/2', '-3/2']); ce('3x^2=27', [3, -3]); ce('x^2-7=0', ['sqrt(7)', '-sqrt(7)'])
ce('x^2-5x=0', [0, 5]); ce('3x^2+12x=0', [0, -4]); ce('2x^2=7x', [0, '7/2']); ce('-x^2+6x=0', [0, 6])
ce('(x+3)(x-3)=7', [4, -4]); ce('x(x-2)=4-2x', [2, -2]); ce('(2x-1)^2=1', [0, 1]); ce('(x+2)^2-4=3x', [0, -1])
ce('x^2/3=12', [6, -6]); ce('x^2/4-x/2=0', [0, 2]); ce('(x^2+1)/5=2', [3, -3]); ce('(x^2-2)/2-(x^2+1)/3=1', ['sqrt(14)', '-sqrt(14)'])
ce('(2x+3)(2x-3)-(x+1)^2=2(x^2-x)-10', [0]); ce('x(x-3)/2-x(x+1)/3=x', [0, 17]); ce('5x^2=3x', [0, '3/5'])

# =====================================================================
E30 = ['x^2-6x+8=0', 'x^2+2x-8=0', 'x^2-4x-5=0', 'x^2+7x+12=0']
E31 = ['2x^2-5x+2=0', '3x^2+x-2=0', '6x^2-x-1=0', '4x^2+4x-3=0']
E33 = ['-x^2+x+6=0', '9x^2-6x+1=0', 'x^2+3x+5=0', 'x^2-2x-2=0']
E34 = ['(x-1)(x+4)=6', '(x+2)^2=3x+10', 'x(2x-1)=(x+1)^2-4', '3x(x-2)-(x-1)(x+1)=9']
E35 = ['x^2/2-x/3=4/3', '(x^2-1)/3+x/2=2']
E36 = ['(x-1)^2/4-(x+2)/6=(x-3)/3', 'x(x+1)/2-(x-1)(x+2)/3=1']
DS = [('x^2-10x+25=0', 1, 1, -10, 25), ('2x^2+3x+4=0', 0, 2, 3, 4), ('x^2-x-1=0', 2, 1, -1, -1), ('-3x^2+2x+1=0', 2, -3, 2, 1)]
S_.append(("Equacions de segon grau completes", [
 (1, r"Resol amb la fórmula:" + eqs(E30, 4)[0] + recorda(r"$x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$. \ Compte amb els signes: si $b=-6$, aleshores $-b=6$ i $b^2=36$."), eqs(E30, 4, 2)[1]),
 (1, r"Resol:" + eqs(E31, 4)[0], eqs(E31, 4, 2)[1]),
 (1, r"Calcula el discriminant i digues quantes solucions té cada equació, sense resoldre-la:" + tasks(4, ['$%s$' % tx(e) for e, *_ in DS]),
     tasks(2, [r'$\Delta=%s$: \rest{%s}' % (b * b - 4 * a * c, ['cap solució', 'una solució', 'dues solucions'][n]) for _, n, a, b, c in DS])),
 (2, r"Resol:" + eqs(E33, 4)[0], eqs(E33, 4, 1)[1]),
 (2, r"Redueix a la forma general i resol:" + eqs(E34, 2)[0], eqs(E34, 2, 1)[1]),
 (2, r"Resol:" + eqs(E35, 2)[0], eqs(E35, 2, 1)[1]),
 (3, r"Resol:" + eqs(E36, 1)[0], eqs(E36, 1, 1)[1]),
 (3, r"Respon:" + tasks(1, [r"Troba $k$ perquè l'equació $x^2-4x+k=0$ tinga una única solució. Quina és?", r"Troba $k$ perquè $x=3$ siga solució de $x^2+kx-6=0$ i calcula l'altra solució."]),
     tasks(1, [r"$\Delta=16-4k=0\Rightarrow\res{k=4}$; \ $x^2-4x+4=0\Rightarrow\res{x=2}$ (doble)", r"$9+3k-6=0\Rightarrow\res{k=-1}$; \ $x^2-x-6=0\Rightarrow x=3,\ \res{x=-2}$"])),
 (3, r"Escriu una equació de segon grau, en forma general, que tinga per solucions:" + tasks(2, [r'$2$ i $-5$', r'$\tfrac12$ i $3$']),
     tasks(2, [r'$(x-2)(x+5)=0\Rightarrow\res{x^2+3x-10=0}$', r'$(2x-1)(x-3)=0\Rightarrow\res{2x^2-7x+3=0}$'])),
]))
checkall(E30 + E31 + E33 + E34 + E35 + E36)
for e, n, a, b, c in DS:
    D = b * b - 4 * a * c; assert n == (2 if D > 0 else 1 if D == 0 else 0) and len(set(v for v in sp.solve(S(e.split('=')[0]), x) if v.is_real)) == n
ce('x^2-6x+8=0', [2, 4]); ce('x^2+2x-8=0', [2, -4]); ce('x^2-4x-5=0', [5, -1]); ce('x^2+7x+12=0', [-3, -4])
ce('2x^2-5x+2=0', [2, '1/2']); ce('3x^2+x-2=0', ['2/3', -1]); ce('6x^2-x-1=0', ['1/2', '-1/3']); ce('4x^2+4x-3=0', ['1/2', '-3/2'])
ce('-x^2+x+6=0', [3, -2]); ce('9x^2-6x+1=0', ['1/3']); ce('x^2+3x+5=0', []); ce('x^2-2x-2=0', ['1+sqrt(3)', '1-sqrt(3)'])
ce('(x-1)(x+4)=6', [2, -5]); ce('(x+2)^2=3x+10', [2, -3]); ce('x(2x-1)=(x+1)^2-4', []); ce('3x(x-2)-(x-1)(x+1)=9', [4, -1])
ce('x^2/2-x/3=4/3', [2, '-4/3']); ce('(x^2-1)/3+x/2=2', [2, '-7/2']); ce('(x-1)^2/4-(x+2)/6=(x-3)/3', ['(6+sqrt(3))/3', '(6-sqrt(3))/3']); ce('x(x+1)/2-(x-1)(x+2)/3=1', [1, -2])
ce('x^2-4x+4=0', [2]); ce('x^2-x-6=0', [3, -2]); chk('(x-2)(x+5)', 'x^2+3x-10'); chk('(2x-1)(x-3)', '2x^2-7x+3')

# =====================================================================
E40 = ['x^3-16x=0', 'x^3+3x^2-10x=0', '2x^3-8x^2=0', 'x^3+x^2+x=0']
E41 = ['x^3-7x+6=0', 'x^3-4x^2+x+6=0', 'x^3+2x^2-5x-6=0', 'x^3-3x^2-4x+12=0']
E42 = ['x^3-x^2-8x+12=0', 'x^3+3x^2+3x+1=0', 'x^3-2x^2+x-2=0', 'x^3+x^2-2=0']
E43 = ['x^3+12=4x^2+3x', 'x(x-1)(x+1)=24']
E44 = ['2x^3-5x^2-4x+3=0', '3x^3+4x^2-5x-2=0']
E45 = ['x^4-10x^2+9=0', 'x^4-x^3-7x^2+x+6=0']
S_.append(("Equacions de tercer grau (Ruffini)", [
 (1, r"Resol, sense desenvolupar els productes:" + tasks(2, [r'$(x-2)(x+3)(x-5)=0$', r'$x(x+1)(2x-3)=0$', r'$(x-4)(x^2-9)=0$', r'$(x+1)(x^2+4)=0$'])
     + recorda(r"Si un producte val 0, algun dels factors ha de valdre 0."),
     tasks(2, [r'$\res{x=2,\ x=-3,\ x=5}$', r'$\res{x=0,\ x=-1,\ x=\tfrac32}$', r'$\res{x=4,\ x=3,\ x=-3}$', r'$x^2+4=0$ no té solució: \ $\res{x=-1}$'])),
 (1, r"Resol traient factor comú:" + eqs(E40, 2)[0], eqs(E40, 2, 1)[1]),
 (2, r"Resol amb la regla de Ruffini:" + eqs(E41, 2)[0] + recorda(r"Les solucions enteres són divisors del terme independent. Quan en trobes una, $x=a$, divideix per $x-a$ amb Ruffini i resol l'equació de segon grau que queda."), eqs(E41, 2, 1)[1]),
 (2, r"Resol. Atenció a les solucions dobles i a les equacions de segon grau sense solució:" + eqs(E42, 2)[0], eqs(E42, 2, 1)[1]),
 (2, r"Passa-ho tot al primer membre i resol:" + eqs(E43, 2)[0], eqs(E43, 2, 1)[1]),
 (3, r"Resol (alguna solució és una fracció):" + eqs(E44, 2)[0], eqs(E44, 2, 1)[1]),
 (3, r"Aplica Ruffini dues vegades per a resoldre aquestes equacions de quart grau:" + eqs(E45, 2)[0], eqs(E45, 2, 1)[1]),
 (3, r"Troba $k$ perquè $x=2$ siga solució de $x^3-kx^2+2x+4=0$ i, amb aquest valor, troba les altres solucions.",
     r"$8-4k+4+4=0\Rightarrow\res{k=4}$. \ $\begin{array}{r|rrr|r} & 1 & -4 & 2 & 4\\ 2 & & 2 & -4 & -4\\ \hline & 1 & -2 & -2 & 0\end{array}$ \ $x^2-2x-2=0\Rightarrow\res{x=1\pm\sqrt3}$"),
]))
checkall(E40 + E41 + E42 + E43 + E44 + E45)
ce('(x-2)(x+3)(x-5)=0', [2, -3, 5]); ce('x(x+1)(2x-3)=0', [0, -1, '3/2']); ce('(x-4)(x^2-9)=0', [4, 3, -3]); ce('(x+1)(x^2+4)=0', [-1])
ce('x^3-16x=0', [0, 4, -4]); ce('x^3+3x^2-10x=0', [0, 2, -5]); ce('2x^3-8x^2=0', [0, 4]); ce('x^3+x^2+x=0', [0])
ce('x^3-7x+6=0', [1, 2, -3]); ce('x^3-4x^2+x+6=0', [-1, 2, 3]); ce('x^3+2x^2-5x-6=0', [-1, 2, -3]); ce('x^3-3x^2-4x+12=0', [2, -2, 3])
ce('x^3-x^2-8x+12=0', [2, -3]); ce('x^3+3x^2+3x+1=0', [-1]); ce('x^3-2x^2+x-2=0', [2]); ce('x^3+x^2-2=0', [1])
ce('x^3+12=4x^2+3x', [4, 'sqrt(3)', '-sqrt(3)']); ce('x(x-1)(x+1)=24', [3]); ce('2x^3-5x^2-4x+3=0', [-1, 3, '1/2']); ce('3x^3+4x^2-5x-2=0', [1, '-1/3', -2])
ce('x^4-10x^2+9=0', [1, -1, 3, -3]); ce('x^4-x^3-7x^2+x+6=0', [1, -1, 3, -2]); assert sp.solve(8 - 4 * k + 4 + 4, k) == [4]; ce('x^3-4x^2+2x+4=0', [2, '1+sqrt(3)', '1-sqrt(3)'])

# =====================================================================
PB = [
 (1, r"La suma de dos nombres consecutius és 75. Quins són?", r"$x+(x+1)=75\Rightarrow 2x=74\Rightarrow x=37$: \ \rest{37 i 38}", ('x+(x+1)=75', [37])),
 (1, r"Si a un nombre li sumem el seu triple, obtenim 56. Quin és el nombre?", r"$x+3x=56\Rightarrow 4x=56\Rightarrow\res{x=14}$", ('x+3x=56', [14])),
 (1, r"Una persona gasta la tercera part dels seus diners en roba i la quarta part en llibres, i encara li queden 25 €. Quants diners tenia?", r"$x-\tfrac{x}{3}-\tfrac{x}{4}=25\xrightarrow{\cdot12}12x-4x-3x=300\Rightarrow 5x=300\Rightarrow\res{60\text{ €}}$", ('x-x/3-x/4=25', [60])),
 (1, r"L'Anna té 12 anys i son pare, 40. D'ací a quants anys l'edat del pare serà el doble que la de l'Anna?", r"$40+x=2(12+x)\Rightarrow 40+x=24+2x\Rightarrow\res{x=16\text{ anys}}$", ('40+x=2(12+x)', [16])),
 (2, r"La llargària d'un rectangle és 3 m més que el doble de l'amplària i el perímetre fa 54 m. Quines dimensions té?", r"$2x+2(2x+3)=54\Rightarrow 6x+6=54\Rightarrow x=8$: \ \rest{8 m i 19 m}", ('2x+2(2x+3)=54', [8])),
 (2, r"En un corral hi ha gallines i conills. En total hi ha 40 caps i 110 potes. Quants animals hi ha de cada tipus?", r"Gallines $x$: \ $2x+4(40-x)=110\Rightarrow -2x=-50\Rightarrow x=25$: \ \rest{25 gallines i 15 conills}", ('2x+4(40-x)=110', [25])),
 (2, r"En una guardiola hi ha 30 monedes, unes d'1 € i altres de 2 €, que sumen 46 €. Quantes monedes hi ha de cada tipus?", r"Monedes de 2 €: $x$. \ $2x+(30-x)=46\Rightarrow\res{x=16}$: \ \rest{16 de 2 € i 14 d'1 €}", ('2x+(30-x)=46', [16])),
 (2, r"L'edat d'una mare és el triple de la del seu fill, i d'ací a 12 anys només serà el doble. Quants anys tenen ara?", r"$3x+12=2(x+12)\Rightarrow\res{x=12}$: \ fill \rest{12 anys}, mare \rest{36 anys}", ('3x+12=2(x+12)', [12])),
 (2, r"Troba dos nombres naturals consecutius el producte dels quals siga 156.", r"$x(x+1)=156\Rightarrow x^2+x-156=0\Rightarrow x=\tfrac{-1\pm25}{2}$: \ $x=12$ ($-13$ no és natural): \ \rest{12 i 13}", ('x(x+1)=156', [12, -13])),
 (2, r"Si al quadrat d'un nombre li restem el seu triple, obtenim 40. Quin pot ser el nombre?", r"$x^2-3x-40=0\Rightarrow x=\tfrac{3\pm13}{2}$: \ \rest{$x=8$ o $x=-5$}", ('x^2-3x=40', [8, -5])),
 (2, r"Si augmentem en 3 cm el costat d'un quadrat, la seua àrea augmenta 51 cm². Quant fa el costat?", r"$(x+3)^2-x^2=51\Rightarrow 6x+9=51\Rightarrow\res{x=7\text{ cm}}$", ('(x+3)^2-x^2=51', [7])),
 (3, r"La hipotenusa d'un triangle rectangle fa 10 cm i un catet fa 2 cm més que l'altre. Quant fan els catets?", r"$x^2+(x+2)^2=100\Rightarrow x^2+2x-48=0\Rightarrow x=\tfrac{-2\pm14}{2}$: \ $x=6$ ($-8$ no val): \ \rest{6 cm i 8 cm}", ('x^2+(x+2)^2=100', [6, -8])),
 (3, r"Un rectangle té 34 m de perímetre i 60 m² d'àrea. Quines dimensions té?", r"Si un costat fa $x$, l'altre fa $17-x$: \ $x(17-x)=60\Rightarrow x^2-17x+60=0\Rightarrow x=\tfrac{17\pm7}{2}$: \ \rest{12 m i 5 m}", ('x(17-x)=60', [12, 5])),
 (3, r"Volem 20 kg d'una mescla de cafè a 9,50 €/kg barrejant cafè de 12 €/kg amb cafè de 8 €/kg. Quants quilos de cada tipus hem de posar?", r"$12x+8(20-x)=9{,}5\cdot20\Rightarrow 4x+160=190\Rightarrow x=7{,}5$: \ \rest{7,5 kg de 12 € i 12,5 kg de 8 €}", ('12x+8(20-x)=190', ['15/2'])),
 (3, r"Dos ciclistes ixen alhora de dues ciutats separades 90 km i van l'un cap a l'altre a 20 km/h i a 25 km/h. Quant de temps tarden a trobar-se? A quina distància de la primera ciutat?", r"$20t+25t=90\Rightarrow\res{t=2\text{ h}}$; \ a $20\cdot2=\res{40\text{ km}}$", ('20x+25x=90', [2])),
 (3, r"Una caixa de base quadrada té una altura 3 cm més gran que el costat de la base, i el seu volum és 112 cm³. Quines dimensions té?", r"$x^2(x+3)=112\Rightarrow x^3+3x^2-112=0$. \ $\begin{array}{r|rrr|r} & 1 & 3 & 0 & -112\\ 4 & & 4 & 28 & 112\\ \hline & 1 & 7 & 28 & 0\end{array}$ \ ($x^2+7x+28=0$ no té solució): \ \rest{base de 4 cm × 4 cm i altura 7 cm}", ('x^2*(x+3)=112', [4])),
 (3, r"El producte de tres nombres naturals consecutius és 8 vegades la seua suma. Quins són?", r"$x(x+1)(x+2)=8(3x+3)\Rightarrow x^3+3x^2-22x-24=0\Rightarrow (x+1)(x^2+2x-24)=0$: \ $x=-1,\ 4,\ -6$; només $x=4$ és natural: \ \rest{4, 5 i 6}", ('x(x+1)(x+2)=8(3x+3)', [-1, 4, -6])),
]
for _, _, _, (e, s) in PB: ce(e, s)
chk('x(x+1)(x+2)-8(3x+3)', 'x^3+3x^2-22x-24'); chk('(x+1)(x^2+2x-24)', 'x^3+3x^2-22x-24')
S_.append(("Problemes amb equacions", [(st, q + (recorda(r"Tria la incògnita i escriu què representa, planteja l'equació, resol-la i comprova que la solució té sentit en el problema.") if i == 0 else ''), s) for i, (st, q, s, _) in enumerate(PB)]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={equacions, identitats, equacions de primer grau, denominadors, equacions de segon grau, discriminant, equacions de tercer grau, regla de Ruffini, problemes}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def build(sol_):
    t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 5: Equacions. 3r d'ESO}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 5: Equacions · 3r d'ESO" % t)
    assert 'Unitat 5' in p and 'unitat 5' in p
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{3r ESO}{''' + ('Solucions de la fitxa · Unitat 5' if sol_ else "Fitxa d'exercicis · Unitat 5") + r'''}{Equacions}
''')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs calculadores que resolen pas a pas qualsevol equació."
             if sol_ else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i comprova les solucions sempre que pugues. Fes els càlculs sense calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't5-fitxa-solucions.tex' if sol_ else 't5-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
