# Genera t4-fitxa-exercicis.tex i t4-fitxa-solucions.tex (2n ESO, Unitat 4: Equacions de 1r i 2n grau)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 9 seccions segueixen els apartats dels apunts (4.1-4.9).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Les equacions s'escriuen en text («(x+1)/2-(x-2)/3=2») i la resolució pas a pas la fa sol() (el resolutor de la fitxa de
# 3r ESO, ../3eso-t5/genera.py, sense Ruffini); ce() i checkall() comproven amb sympy totes les solucions.
# Ús: python3 genera.py && pdflatex t4-fitxa-exercicis.tex (dues vegades) && pdflatex t4-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re
from math import gcd
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

def tasks(n, items, gap=None):
    o = '[after-item-skip=%s]' % gap if gap else ''
    return '\\begin{tasks}%s(%d)\n' % (o, n) + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- àlgebra ----------
x, k = sp.symbols('x k')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
NCHK = [0]
def S(s): return parse_expr(s.replace('\\cdot', '*').replace('[', '(').replace(']', ')'), transformations=TR, local_dict={'x': x, 'k': k}) if isinstance(s, str) else s
def chk(l, r):
    NCHK[0] += 1; assert sp.expand(S(l) - S(r)) == 0, (l, r, sp.expand(S(l)))
def ce(eq, sols):
    """solucions reals d'una equació: llista, 'totes' (identitat) o [] (cap)"""
    NCHK[0] += 1
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
    t = side(l) + '=' + side(r)
    t = re.sub(r'\^(\d+)', r'^{\1}', t)
    return t.replace('*', r'\cdot ')

# ---------- resolució automàtica ----------
CAP = T('sense solució', 'sin solución')
INF = T('infinites solucions', 'infinitas soluciones')
DOBLE = T('doble', 'doble')
def rx(v): return ntex(v) if v.is_Rational else sp.latex(v)
def fsol(roots, irr=None):
    """{arrel: multiplicitat} -> \\res{x=..., x=...}; irr: parella irracional ja escrita amb ±"""
    rs = sorted(roots.items(), key=lambda kv: float(kv[0]))
    if not rs and not irr: return r'\res{\text{%s}}' % CAP
    out, done = [], set()
    for r, m in rs:
        if r in done: continue
        if r < 0 and -r in roots and m == 1 and roots[-r] == 1: out.append(r'x=\pm%s' % rx(-r)); done.add(-r); continue
        out.append('x=%s%s' % (rx(r), r'\ (\text{%s})' % DOBLE if m == 2 else ''))
    return r'\res{' + r',\ '.join(out + ([irr] if irr else [])) + '}'
def quad(a, b, c):
    """passos per a ax^2+bx+c=0 (enters, a>0); retorna (passos, arrels, parella irracional)"""
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
def sol(eq):
    """resolució pas a pas (en TeX) de qualsevol equació de primer o segon grau"""
    l, r = eq.split('=')
    L, R = S(l), S(r)
    m = 1
    for d in re.findall(r'/(\d+)', eq): m = m * int(d) // gcd(m, int(d))
    L2, R2 = sp.expand(L * m), sp.expand(R * m)
    st = []
    if m > 1:
        ms = '%s=%s' % (mside(l, m), mside(r, m))
        a_, b_ = ms.replace('\\cdot', '*').replace('{', '(').replace('}', ')').split('=')
        chk(a_, L2); chk(b_, R2)
        st.append(r'\text{m.c.m.}=%d:\ \ %s' % (m, ms))
        if ms != '%s=%s' % (pt(L2), pt(R2)): st.append('%s=%s' % (pt(L2), pt(R2)))
    elif '(' in eq or '[' in eq: st.append('%s=%s' % (pt(L2), pt(R2)))
    E = sp.expand(L2 - R2)
    if E == 0:
        st.append(r'0x=0'); res = r'\res{\text{%s}}' % INF
    else:
        P = sp.Poly(E, x); deg = P.degree()
        assert deg <= 2, eq
        if deg == 0:
            st.append(r'0x=%s' % ntex(-E)); res = r'\res{\text{%s}}' % CAP
        elif deg == 1:
            a, b = [sp.Rational(c) for c in P.all_coeffs()]
            b1 = sp.Rational(L2.coeff(x, 0))
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
            if gen != pt(L2) + '=' + pt(R2) and not (cs[1] == 0 and cs[2] != 0): st.append(gen)
            q2, rq, irr = quad(*cs)
            st += q2
            res = fsol({sp.nsimplify(k_): v for k_, v in rq.items()}, irr)
    return '$' + r'\ \Rightarrow\ '.join(st + ([res] if res else [])) + '$'
def eqs(lst, n, ns=None):
    """llista d'equacions -> (enunciats, solucions)"""
    return tasks(n, ['$%s$' % tx(e) for e in lst]), tasks(ns or 1, [sol(e) for e in lst])
def checkall(lst):
    """sol() i sympy han de donar el mateix conjunt de solucions"""
    for e in lst:
        NCHK[0] += 1
        l, r = e.split('=')
        E = sp.expand(S(l) - S(r))
        s = sol(e)
        if E == 0: assert INF in s; continue
        got = sorted(set(v for v in sp.solve(E, x) if v.is_real), key=float)
        if not got: assert CAP in s, (e, s); continue
        for v in got:
            t = rx(sp.nsimplify(v))
            assert ('x=%s' % t) in s or (r'\pm' in s) or ('sqrt' in t), (e, t, s)

S_ = []
def sec(title): S_.append((title, [])); return S_[-1][1]
REG = T('Identitat', 'Identidad'), T('Equació', 'Ecuación')

# =====================================================================
# 1. Equacions: elements i solucions
X = sec(T('Equacions: elements i solucions', 'Ecuaciones: elementos y soluciones'))
ID = [('3(x+2)=3x+6', 'totes'), ('3x+2=8', [2]), ('(x+1)^2=x^2+2x+1', 'totes'), ('x^2-1=0', [1, -1]), ('5x-2x=3x', 'totes'), ('5x-2=3x', [1]), ('(x-3)(x+3)=x^2-9', 'totes'), ('2(x-1)=2x-1', [])]
for e, s in ID: ce(e, s)
X.append((1, T("Indica quines igualtats són identitats i quines són equacions:", "Indica qué igualdades son identidades y cuáles son ecuaciones:") + tasks(2, ['$%s$' % tx(e) for e, _ in ID])
    + recorda(T(r"una \textbf{identitat} es compleix per a qualsevol valor de $x$; una \textbf{equació}, només per a alguns valors (o per a cap).", r"una \textbf{identidad} se cumple para cualquier valor de $x$; una \textbf{ecuación}, solo para algunos valores (o para ninguno).")),
    tasks(2, [r'\rest{%s}' % REG[0], r'\rest{%s} ($x=2$)' % REG[1], r'\rest{%s}' % REG[0], r'\rest{%s} ($x=\pm1$)' % REG[1], r'\rest{%s}' % REG[0], r'\rest{%s} ($x=1$)' % REG[1], r'\rest{%s}' % REG[0], r'\rest{%s} %s ($-2\neq-1$)' % (REG[1], T('sense solució', 'sin solución'))])))
CK = [('3x-5=x+1', '3'), ('x^2-4x=5', '-1'), ('2(x-1)=x+4', '5'), ('x/2+1=x-3', '8'), ('x^2+x=6', '-3'), ('7-x=2x+1', '3')]
CKs = [(r'$4=4$', True), (r'$5=5$', True), (r'$8\neq9$', False), (r'$5=5$', True), (r'$6=6$', True), (r'$4\neq7$', False)]
for (e, v), (_, ok) in zip(CK, CKs):
    l, r = e.split('='); assert (S(l).subs(x, int(v)) == S(r).subs(x, int(v))) == ok
X.append((1, T("Comprova si el valor indicat és solució de cada equació:", "Comprueba si el valor indicado es solución de cada ecuación:") + tasks(2, [r'$%s$, \ $x=%s$' % (tx(e), v) for e, v in CK]),
    tasks(2, [r'%s: \rest{%s}' % (t, T('sí', 'sí') if ok else 'no') for t, ok in CKs])))
X.append((1, T(r"En l'equació $4x^2+x-3=2x+5$, indica el primer i el segon membre, els termes, la incògnita i el grau.", r"En la ecuación $4x^2+x-3=2x+5$, indica el primer y el segundo miembro, los términos, la incógnita y el grado."),
    T(r"1r membre: $4x^2+x-3$; 2n membre: $2x+5$; termes: $4x^2,\ x,\ -3,\ 2x,\ 5$; incògnita: $x$; \rest{grau 2}.", r"1.\textsuperscript{er} miembro: $4x^2+x-3$; 2.\textsuperscript{o} miembro: $2x+5$; términos: $4x^2,\ x,\ -3,\ 2x,\ 5$; incógnita: $x$; \rest{grado 2}.")))
GR = [('x(x+4)=x^2-8', 'x', '4x=-8', 1), ('(x-2)^2=x^2+4', 'x', '-4x=0', 1), ('x^2+3x=2x^2-1', 'x2', '-x^2+3x+1=0', 2), ('(x+1)(x-1)=3x', 'x2', 'x^2-3x-1=0', 2)]
for e, _, r, g in GR:
    l, rr = e.split('='); E = sp.expand(S(l) - S(rr)); assert sp.Poly(E, x).degree() == g
X.append((2, T("Indica el grau de cada equació un cop reduïda:", "Indica el grado de cada ecuación una vez reducida:") + tasks(2, ['$%s$' % tx(e) for e, *_ in GR])
    + recorda(T(r"abans de dir el grau, opera i redueix: els termes en $x^2$ es poden cancel·lar.", r"antes de decir el grado, opera y reduce: los términos en $x^2$ se pueden cancelar.")),
    tasks(2, [r'$%s$: \rest{%s %d}' % (r, T('grau', 'grado'), g) for _, _, r, g in GR])))
ce('x(x+4)=x^2-8', [-2]); ce('(x-2)^2=x^2+4', [0])
X.append((2, T(r"Escriu una equació de primer grau que tinga la solució $x=-2$ i una equació de segon grau que tinga les solucions $x=3$ i $x=-3$.", r"Escribe una ecuación de primer grado que tenga la solución $x=-2$ y una ecuación de segundo grado que tenga las soluciones $x=3$ y $x=-3$."),
    T(r"Per exemple, \rest{$x+2=0$} \ (o $3x+1=-5$\ldots) \ i \ \rest{$x^2-9=0$} \ (o $x^2=9$\ldots).", r"Por ejemplo, \rest{$x+2=0$} \ (o $3x+1=-5$\ldots) \ y \ \rest{$x^2-9=0$} \ (o $x^2=9$\ldots).")))
ce('x+2=0', [-2]); ce('3x+1=-5', [-2]); ce('x^2-9=0', [3, -3])
X.append((3, T("Troba el valor de $k$ en cada cas:", "Halla el valor de $k$ en cada caso:") + tasks(1, [T(r"$x=3$ és solució de $kx-4=2x+k$.", r"$x=3$ es solución de $kx-4=2x+k$."), T(r"$x=-1$ és solució de $x^2+kx=k+5$.", r"$x=-1$ es solución de $x^2+kx=k+5$.")]),
    tasks(1, [r"$3k-4=6+k\Rightarrow 2k=10\Rightarrow\res{k=5}$", r"$1-k=k+5\Rightarrow -2k=4\Rightarrow\res{k=-2}$"])))
assert sp.solve(3 * k - 4 - (6 + k), k) == [5] and sp.solve(1 - k - (k + 5), k) == [-2]

# =====================================================================
# 2. Equacions de primer grau
X = sec(T('Equacions de primer grau', 'Ecuaciones de primer grado'))
E1 = ['x+7=12', 'x-5=-3', '3x=-21', '-4x=20', 'x/5=3', '-x=6', '2x=7', 'x/4=-2']
q, s = eqs(E1, 4, 2)
X.append((1, T("Resol mentalment o en un sol pas:", "Resuelve mentalmente o en un solo paso:") + q
    + recorda(T(r"el que suma passa restant i el que resta passa sumant; el que multiplica tot un membre passa dividint (amb el seu signe) i el que divideix passa multiplicant.", r"lo que suma pasa restando y lo que resta pasa sumando; lo que multiplica a todo un miembro pasa dividiendo (con su signo) y lo que divide pasa multiplicando.")), s))
E2 = ['5x-4=11', '-2x+9=1', '3x+8=2', '7-x=10', '4x-3=-15', '6+5x=-4']
q, s = eqs(E2, 3, 3)
X.append((1, T("Resol:", "Resuelve:") + q, s))
E3 = ['4x+3=2x+11', '7-3x=x-13', '6x-5=9x+7', '2x-1=5x-1', '8x+2=3x-13', '10-x=4x']
q, s = eqs(E3, 3, 2)
X.append((1, T("Resol:", "Resuelve:") + q, s))
E4 = ['5x-3+2x=4x+9', '8-3x+x=2x-4-x', '2x+7-5x=x-9', 'x-4+3x=6x+2-x']
q, s = eqs(E4, 2, 2)
X.append((2, T("Redueix cada membre i resol:", "Reduce cada miembro y resuelve:") + q, s))
E5 = ['6x+1=2x+7', '5x-2=2x+3', '4-7x=x', '9x+4=3x-6']
q, s = eqs(E5, 4, 2)
X.append((2, T("Resol (les solucions són fraccions: simplifica-les):", "Resuelve (las soluciones son fracciones: simplifícalas):") + q, s))
E6 = ['3x-8+5x-1=4x+7-2x+2', '12-5x+3x=2x-9+x+1', '7x-2-x+5=4x+11-3x', '-x+6-4x=2-3x+x-10']
q, s = eqs(E6, 2, 1)
X.append((3, T("Resol i comprova la solució:", "Resuelve y comprueba la solución:") + q, s))
X.append((3, T(r"L'Aitana ha resolt l'equació $5x-3=2x+9$ així:\quad $5x+2x=9-3\ \Rightarrow\ 7x=6\ \Rightarrow\ x=\tfrac67$. \ Quins errors ha comés? Resol-la correctament i comprova-la.",
               r"Aitana ha resuelto la ecuación $5x-3=2x+9$ así:\quad $5x+2x=9-3\ \Rightarrow\ 7x=6\ \Rightarrow\ x=\tfrac67$. \ ¿Qué errores ha cometido? Resuélvela correctamente y compruébala."),
    T(r"El $2x$ suma, i ha de passar \textbf{restant}; el $-3$ resta, i ha de passar \textbf{sumant}. \ $5x-2x=9+3\Rightarrow 3x=12\Rightarrow\res{x=4}$. \ Comprovació: $5\cdot4-3=17=2\cdot4+9$.",
      r"El $2x$ suma, y tiene que pasar \textbf{restando}; el $-3$ resta, y tiene que pasar \textbf{sumando}. \ $5x-2x=9+3\Rightarrow 3x=12\Rightarrow\res{x=4}$. \ Comprobación: $5\cdot4-3=17=2\cdot4+9$.")))
checkall(E1 + E2 + E3 + E4 + E5 + E6)
for e, v in [('x+7=12', 5), ('x-5=-3', 2), ('3x=-21', -7), ('-4x=20', -5), ('x/5=3', 15), ('-x=6', -6), ('2x=7', '7/2'), ('x/4=-2', -8), ('5x-4=11', 3), ('-2x+9=1', 4), ('3x+8=2', -2), ('7-x=10', -3),
             ('4x-3=-15', -3), ('6+5x=-4', -2), ('4x+3=2x+11', 4), ('7-3x=x-13', 5), ('6x-5=9x+7', -4), ('2x-1=5x-1', 0), ('8x+2=3x-13', -3), ('10-x=4x', 2), ('5x-3+2x=4x+9', 4),
             ('8-3x+x=2x-4-x', 4), ('2x+7-5x=x-9', 4), ('x-4+3x=6x+2-x', -6), ('6x+1=2x+7', '3/2'), ('5x-2=2x+3', '5/3'), ('4-7x=x', '1/2'), ('9x+4=3x-6', '-5/3'),
             ('3x-8+5x-1=4x+7-2x+2', 3), ('12-5x+3x=2x-9+x+1', 4), ('7x-2-x+5=4x+11-3x', '8/5'), ('-x+6-4x=2-3x+x-10', '14/3'), ('5x-3=2x+9', 4)]: ce(e, [v])

# =====================================================================
# 3. Equacions amb parèntesis
X = sec(T('Equacions amb parèntesis', 'Ecuaciones con paréntesis'))
P1 = ['3(x-2)=12', '5(x+1)=2x-7', '2(x-4)=x+1', '4(2x-1)=3x+6']
q, s = eqs(P1, 2, 2)
X.append((1, T("Resol traient primer els parèntesis:", "Resuelve quitando primero los paréntesis:") + q, s))
P2 = ['4-(x+3)=2x-5', 'x-(5-x)=3', '7-(2x-1)=x+2', '-(x-6)=2x']
q, s = eqs(P2, 4, 2)
X.append((1, T("Resol:", "Resuelve:") + q + recorda(T(r"un signe $-$ davant d'un parèntesi canvia el signe de \textbf{tots} els termes de dins: $-(2x-1)=-2x+1$.", r"un signo $-$ delante de un paréntesis cambia el signo de \textbf{todos} los términos de dentro: $-(2x-1)=-2x+1$.")), s))
P3 = ['3(2x-1)-2(x+4)=5x-13', '5-2(3-x)=4(x+1)-11', '4(x-3)-(x-5)=2(x+1)', '2(x+3)-3(x-1)=4x-6']
q, s = eqs(P3, 2, 1)
X.append((2, T("Resol:", "Resuelve:") + q, s))
P4 = ['3(x+2)-x=2(x+3)', '5x-2(x-1)=3x+4', '6x-2(3x+1)=-2', '7x-3(2x-1)=2x+1']
q, s = eqs(P4, 2, 1)
X.append((2, T("Resol i digues quines equacions no tenen solució i quines en tenen infinites:", "Resuelve y di qué ecuaciones no tienen solución y cuáles tienen infinitas:") + q, s))
P5 = ['(x+1)^2-(x-1)^2=12', 'x(x+3)-x^2=2x+5', '(x+2)(x-2)=x(x+1)-7']
q, s = eqs(P5, 3, 1)
X.append((2, T(r"Resol fent servir les identitats notables (veuràs que els termes en $x^2$ es cancel·len):", r"Resuelve usando las identidades notables (verás que los términos en $x^2$ se cancelan):") + q, s))
P6 = ['x-[2x-(3-x)]=7', '2[3-2(x+1)]=5-3(2x-1)-x']
q, s = eqs(P6, 2, 1)
X.append((3, T("Resol (comença pels parèntesis de dins):", "Resuelve (empieza por los paréntesis de dentro):") + q, s))
X.append((3, T(r"Troba el valor de $a$ perquè l'equació $2(x+a)=x+9$ tinga la solució $x=3$.", r"Halla el valor de $a$ para que la ecuación $2(x+a)=x+9$ tenga la solución $x=3$."),
    r"$2(3+a)=12\Rightarrow 6+2a=12\Rightarrow\res{a=3}$"))
checkall(P1 + P2 + P3 + P4 + P5 + P6)
for e, v in [('3(x-2)=12', [6]), ('5(x+1)=2x-7', [-4]), ('2(x-4)=x+1', [9]), ('4(2x-1)=3x+6', [2]), ('4-(x+3)=2x-5', [2]), ('x-(5-x)=3', [4]), ('7-(2x-1)=x+2', [2]), ('-(x-6)=2x', [2]),
             ('3(2x-1)-2(x+4)=5x-13', [2]), ('5-2(3-x)=4(x+1)-11', [3]), ('4(x-3)-(x-5)=2(x+1)', [9]), ('2(x+3)-3(x-1)=4x-6', [3]), ('3(x+2)-x=2(x+3)', 'totes'), ('5x-2(x-1)=3x+4', []),
             ('6x-2(3x+1)=-2', 'totes'), ('7x-3(2x-1)=2x+1', [2]), ('(x+1)^2-(x-1)^2=12', [3]), ('x(x+3)-x^2=2x+5', [5]), ('(x+2)(x-2)=x(x+1)-7', [3]), ('x-(2x-(3-x))=7', [-2]),
             ('2(3-2(x+1))=5-3(2x-1)-x', [2]), ('2(x+3)=x+9', [3])]: ce(e, v)

# =====================================================================
# 4. Equacions amb denominadors
X = sec(T('Equacions amb denominadors', 'Ecuaciones con denominadores'))
D1 = ['x/3=4', 'x/2+x/4=6', 'x-x/3=10', '2x/5-1=3']
q, s = eqs(D1, 4, 2)
X.append((1, T("Resol:", "Resuelve:") + q, s))
D2 = ['(x+2)/3=4', '(x-1)/2=(x+3)/4', '(3x-1)/4=2', 'x/6+1=x/4']
q, s = eqs(D2, 4, 2)
X.append((1, T("Resol:", "Resuelve:") + q + recorda(T(r"multiplica \textbf{tots} els termes pel m.c.m. dels denominadors (també els que no tenen denominador) i posa els numeradors entre parèntesis.", r"multiplica \textbf{todos} los términos por el m.c.m. de los denominadores (también los que no tienen denominador) y pon los numeradores entre paréntesis.")), s))
D3 = ['(x+1)/2-(x-1)/3=2', '(x-2)/4-(x-3)/6=1/2', '(2x+1)/3-(x-2)/2=3', 'x-(x+2)/5=(x+6)/2']
q, s = eqs(D3, 2, 1)
X.append((2, T("Resol:", "Resuelve:") + q, s))
D4 = ['(x-1)/3+(x+2)/6=x-2', '3-(x-1)/4=(x+5)/2']
q, s = eqs(D4, 2, 1)
X.append((2, T("Resol:", "Resuelve:") + q, s))
D5 = ['3(x-2)/4-2(x+1)/3=(x-10)/6', 'x/2-(x-1)/3-(x+1)/4=(1-x)/12', '(x+1)/2-(x+3)/4=x/4-1']
q, s = eqs(D5, 1, 1)
X.append((3, T("Resol i interpreta el resultat:", "Resuelve e interpreta el resultado:") + q, s))
X.append((3, T(r"Un alumne ha resolt l'equació $\dfrac{x-2}{3}-\dfrac{x+1}{2}=1$ així:\quad $2x-4-3x+3=6\ \Rightarrow\ -x=7\ \Rightarrow\ x=-7$. \ On s'ha equivocat? Resol-la correctament.",
               r"Un alumno ha resuelto la ecuación $\dfrac{x-2}{3}-\dfrac{x+1}{2}=1$ así:\quad $2x-4-3x+3=6\ \Rightarrow\ -x=7\ \Rightarrow\ x=-7$. \ ¿Dónde se ha equivocado? Resuélvela correctamente."),
    T(r"El $-$ davant de la segona fracció afecta tot el numerador: $-3(x+1)=-3x-3$. \ $2x-4-3x-3=6\Rightarrow -x=13\Rightarrow\res{x=-13}$.", r"El $-$ delante de la segunda fracción afecta a todo el numerador: $-3(x+1)=-3x-3$. \ $2x-4-3x-3=6\Rightarrow -x=13\Rightarrow\res{x=-13}$.")))
checkall(D1 + D2 + D3 + D4 + D5)
for e, v in [('x/3=4', [12]), ('x/2+x/4=6', [8]), ('x-x/3=10', [15]), ('2x/5-1=3', [10]), ('(x+2)/3=4', [10]), ('(x-1)/2=(x+3)/4', [5]), ('(3x-1)/4=2', [3]), ('x/6+1=x/4', [12]),
             ('(x+1)/2-(x-1)/3=2', [7]), ('(x-2)/4-(x-3)/6=1/2', [6]), ('(2x+1)/3-(x-2)/2=3', [10]), ('x-(x+2)/5=(x+6)/2', ['34/3']), ('(x-1)/3+(x+2)/6=x-2', [4]), ('3-(x-1)/4=(x+5)/2', [1]),
             ('3(x-2)/4-2(x+1)/3=(x-10)/6', [-6]), ('x/2-(x-1)/3-(x+1)/4=(1-x)/12', 'totes'), ('(x+1)/2-(x+3)/4=x/4-1', []), ('(x-2)/3-(x+1)/2=1', [-13])]: ce(e, v)

# =====================================================================
# 5. Problemes amb equacions de primer grau
PB = [
 (1, T(r"La suma de dos nombres consecutius és 75. Quins són?", r"La suma de dos números consecutivos es 75. ¿Cuáles son?"),
     T(r"$x+(x+1)=75\Rightarrow 2x=74\Rightarrow x=37$: \ \rest{37 i 38}", r"$x+(x+1)=75\Rightarrow 2x=74\Rightarrow x=37$: \ \rest{37 y 38}"), ('x+(x+1)=75', [37])),
 (1, T(r"Si a un nombre li sumem el seu triple, obtenim 56. Quin és el nombre?", r"Si a un número le sumamos su triple, obtenemos 56. ¿Cuál es el número?"),
     r"$x+3x=56\Rightarrow 4x=56\Rightarrow\res{x=14}$", ('x+3x=56', [14])),
 (1, T(r"L'Anna té 12 anys i son pare, 40. D'ací a quants anys l'edat del pare serà el doble que la de l'Anna?", r"Ana tiene 12 años y su padre, 40. ¿Dentro de cuántos años la edad del padre será el doble que la de Ana?"),
     T(r"$40+x=2(12+x)\Rightarrow 40+x=24+2x\Rightarrow\res{x=16\text{ anys}}$", r"$40+x=2(12+x)\Rightarrow 40+x=24+2x\Rightarrow\res{x=16\text{ años}}$"), ('40+x=2(12+x)', [16])),
 (2, T(r"La llargària d'un rectangle és 3 m més que el doble de l'amplària i el perímetre fa 54 m. Quines dimensions té?", r"El largo de un rectángulo es 3 m más que el doble del ancho y el perímetro mide 54 m. ¿Qué dimensiones tiene?"),
     T(r"$2x+2(2x+3)=54\Rightarrow 6x+6=54\Rightarrow x=8$: \ \rest{8 m i 19 m}", r"$2x+2(2x+3)=54\Rightarrow 6x+6=54\Rightarrow x=8$: \ \rest{8 m y 19 m}"), ('2x+2(2x+3)=54', [8])),
 (2, T(r"En un corral hi ha gallines i conills. En total hi ha 40 caps i 110 potes. Quants animals hi ha de cada tipus?", r"En un corral hay gallinas y conejos. En total hay 40 cabezas y 110 patas. ¿Cuántos animales hay de cada tipo?"),
     T(r"Gallines $x$: \ $2x+4(40-x)=110\Rightarrow -2x=-50\Rightarrow x=25$: \ \rest{25 gallines i 15 conills}", r"Gallinas $x$: \ $2x+4(40-x)=110\Rightarrow -2x=-50\Rightarrow x=25$: \ \rest{25 gallinas y 15 conejos}"), ('2x+4(40-x)=110', [25])),
 (2, T(r"En una guardiola hi ha 30 monedes, unes d'1 € i altres de 2 €, que sumen 46 €. Quantes monedes hi ha de cada tipus?", r"En una hucha hay 30 monedas, unas de 1 € y otras de 2 €, que suman 46 €. ¿Cuántas monedas hay de cada tipo?"),
     T(r"Monedes de 2 €: $x$. \ $2x+(30-x)=46\Rightarrow\res{x=16}$: \ \rest{16 de 2 € i 14 d'1 €}", r"Monedas de 2 €: $x$. \ $2x+(30-x)=46\Rightarrow\res{x=16}$: \ \rest{16 de 2 € y 14 de 1 €}"), ('2x+(30-x)=46', [16])),
 (2, T(r"L'edat d'una mare és el triple de la del seu fill, i d'ací a 12 anys només serà el doble. Quants anys tenen ara?", r"La edad de una madre es el triple de la de su hijo, y dentro de 12 años solo será el doble. ¿Cuántos años tienen ahora?"),
     T(r"$3x+12=2(x+12)\Rightarrow\res{x=12}$: \ fill \rest{12 anys}, mare \rest{36 anys}", r"$3x+12=2(x+12)\Rightarrow\res{x=12}$: \ hijo \rest{12 años}, madre \rest{36 años}"), ('3x+12=2(x+12)', [12])),
 (2, T(r"Després d'un descompte del 15 \%, un abric costa 68 €. Quant costava abans del descompte?", r"Después de un descuento del 15 \%, un abrigo cuesta 68 €. ¿Cuánto costaba antes del descuento?"),
     r"$0{,}85x=68\Rightarrow x=\tfrac{68}{0{,}85}=\res{80\text{ €}}$", ('85x/100=68', [80])),
 (3, T(r"Una persona gasta la tercera part dels seus diners en roba i la quarta part en llibres, i encara li queden 25 €. Quants diners tenia?", r"Una persona gasta la tercera parte de su dinero en ropa y la cuarta parte en libros, y aún le quedan 25 €. ¿Cuánto dinero tenía?"),
     r"$x-\tfrac{x}{3}-\tfrac{x}{4}=25\xrightarrow{\cdot12}12x-4x-3x=300\Rightarrow 5x=300\Rightarrow\res{60\text{ €}}$", ('x-x/3-x/4=25', [60])),
 (3, T(r"Repartim 150 € entre tres germans: el segon rep el doble que el primer, i el tercer, 30 € més que el segon. Quant rep cadascun?", r"Repartimos 150 € entre tres hermanos: el segundo recibe el doble que el primero, y el tercero, 30 € más que el segundo. ¿Cuánto recibe cada uno?"),
     T(r"$x+2x+(2x+30)=150\Rightarrow 5x=120\Rightarrow x=24$: \ \rest{24 €, 48 € i 78 €}", r"$x+2x+(2x+30)=150\Rightarrow 5x=120\Rightarrow x=24$: \ \rest{24 €, 48 € y 78 €}"), ('x+2x+(2x+30)=150', [24])),
 (3, T(r"Volem 20 kg d'una mescla de cafè a 9,50 €/kg barrejant cafè de 12 €/kg amb cafè de 8 €/kg. Quants quilos de cada tipus hem de posar?", r"Queremos 20 kg de una mezcla de café a 9,50 €/kg mezclando café de 12 €/kg con café de 8 €/kg. ¿Cuántos kilos de cada tipo tenemos que poner?"),
     T(r"$12x+8(20-x)=9{,}5\cdot20\Rightarrow 4x+160=190\Rightarrow x=7{,}5$: \ \rest{7,5 kg de 12 € i 12,5 kg de 8 €}", r"$12x+8(20-x)=9{,}5\cdot20\Rightarrow 4x+160=190\Rightarrow x=7{,}5$: \ \rest{7,5 kg de 12 € y 12,5 kg de 8 €}"), ('12x+8(20-x)=190', ['15/2'])),
 (3, T(r"Dos ciclistes ixen alhora de dues ciutats separades 90 km i van l'un cap a l'altre a 20 km/h i a 25 km/h. Quant de temps tarden a trobar-se? A quina distància de la primera ciutat?", r"Dos ciclistas salen a la vez de dos ciudades separadas 90 km y van el uno hacia el otro a 20 km/h y a 25 km/h. ¿Cuánto tardan en encontrarse? ¿A qué distancia de la primera ciudad?"),
     r"$20t+25t=90\Rightarrow\res{t=2\text{ h}}$; \ a $20\cdot2=\res{40\text{ km}}$", ('20x+25x=90', [2])),
]
for _, _, _, (e, s) in PB: ce(e, s)
X = sec(T('Problemes amb equacions de primer grau', 'Problemas con ecuaciones de primer grado'))
for i, (st, q, s, _) in enumerate(PB):
    X.append((st, q + (recorda(T(r"tria la incògnita i escriu què representa, planteja l'equació, resol-la i comprova que la solució té sentit en el problema.", r"elige la incógnita y escribe qué representa, plantea la ecuación, resuélvela y comprueba que la solución tiene sentido en el problema.")) if i == 0 else ''), s))

# =====================================================================
# 6. Equacions de segon grau incompletes
X = sec(T('Equacions de segon grau incompletes', 'Ecuaciones de segundo grado incompletas'))
FG = [('5x-x^2=6', 'x^2-5x+6=0', 1, -5, 6), ('3x^2=12', '3x^2-12=0', 3, 0, -12), ('x(x-4)=0', 'x^2-4x=0', 1, -4, 0), ('(x+1)^2=2x+5', 'x^2-4=0', 1, 0, -4)]
for e, g, a, b, c in FG:
    l, r = e.split('='); E = sp.expand(S(l) - S(r)); assert sp.expand(E - S(g.split('=')[0])) == 0 or sp.expand(E + S(g.split('=')[0])) == 0
def cinc(b, c): return T('completa', 'completa') if b and c else T('incompleta', 'incompleta')
X.append((1, T(r"Escriu cada equació en la forma general $ax^2+bx+c=0$, indica els coeficients $a$, $b$ i $c$ i digues si és completa o incompleta:", r"Escribe cada ecuación en la forma general $ax^2+bx+c=0$, indica los coeficientes $a$, $b$ y $c$ y di si es completa o incompleta:") + tasks(2, ['$%s$' % tx(e) for e, *_ in FG]),
    tasks(1, [r'$%s$: \rest{$a=%d,\ b=%d,\ c=%d$, %s}' % (re.sub(r'\^(\d)', r'^{\1}', g), a, b, c, cinc(b, c)) for _, g, a, b, c in FG])))
I1 = ['x^2-36=0', '2x^2-50=0', 'x^2+9=0', '4x^2-9=0', '3x^2=27', 'x^2-7=0']
q, s = eqs(I1, 3, 2)
X.append((1, T("Resol:", "Resuelve:") + q + recorda(T(r"en $ax^2+c=0$ aïllem $x^2$ i fem l'arrel: hi ha \textbf{dues} solucions, $x=\pm\sqrt{\ }$, o cap si el nombre és negatiu.", r"en $ax^2+c=0$ despejamos $x^2$ y hacemos la raíz: hay \textbf{dos} soluciones, $x=\pm\sqrt{\ }$, o ninguna si el número es negativo.")), s))
I2 = ['x^2-5x=0', '3x^2+12x=0', '2x^2=7x', '-x^2+6x=0']
q, s = eqs(I2, 4, 1)
X.append((1, T("Resol:", "Resuelve:") + q + recorda(T(r"en $ax^2+bx=0$ traiem factor comú $x$: una solució sempre és $x=0$. No dividisques entre $x$!", r"en $ax^2+bx=0$ sacamos factor común $x$: una solución siempre es $x=0$. ¡No dividas entre $x$!")), s))
I3 = ['(x+3)(x-3)=7', 'x(x-2)=4-2x', '(2x-1)^2=1', '(x+2)^2-4=3x']
q, s = eqs(I3, 2, 1)
X.append((2, T("Redueix i resol:", "Reduce y resuelve:") + q, s))
I4 = ['x^2/3=12', 'x^2/4-x/2=0', '(x^2+1)/5=2', '(x^2-2)/2-(x^2+1)/3=1']
q, s = eqs(I4, 2, 1)
X.append((2, T("Resol:", "Resuelve:") + q, s))
X.append((3, T(r"La Marta resol $5x^2=3x$ dividint els dos membres entre $x$ i obté $5x=3$, és a dir, $x=\tfrac35$. Què ha fet malament? Resol-la correctament.", r"Marta resuelve $5x^2=3x$ dividiendo los dos miembros entre $x$ y obtiene $5x=3$, es decir, $x=\tfrac35$. ¿Qué ha hecho mal? Resuélvela correctamente."),
    T(r"En dividir entre $x$ perd la solució $x=0$. \ $5x^2-3x=0\Rightarrow x(5x-3)=0\Rightarrow\res{x=0,\ x=\tfrac35}$.", r"Al dividir entre $x$ pierde la solución $x=0$. \ $5x^2-3x=0\Rightarrow x(5x-3)=0\Rightarrow\res{x=0,\ x=\tfrac35}$.")))
X.append((3, T("Escriu una equació de segon grau incompleta que tinga per solucions:", "Escribe una ecuación de segundo grado incompleta que tenga por soluciones:") + tasks(3, [T(r'$4$ i $-4$', r'$4$ y $-4$'), T(r'$0$ i $3$', r'$0$ y $3$'), T(r'$0$ i $-\tfrac12$', r'$0$ y $-\tfrac12$')]),
    tasks(3, [T(r'P. ex.\ \rest{$x^2-16=0$}', r'P. ej.\ \rest{$x^2-16=0$}'), T(r'P. ex.\ \rest{$x^2-3x=0$}', r'P. ej.\ \rest{$x^2-3x=0$}'), T(r'P. ex.\ \rest{$2x^2+x=0$}', r'P. ej.\ \rest{$2x^2+x=0$}')])))
checkall(I1 + I2 + I3 + I4)
for e, v in [('5x-x^2=6', [2, 3]), ('3x^2=12', [2, -2]), ('x(x-4)=0', [0, 4]), ('(x+1)^2=2x+5', [2, -2]), ('x^2-36=0', [6, -6]), ('2x^2-50=0', [5, -5]), ('x^2+9=0', []), ('4x^2-9=0', ['3/2', '-3/2']),
             ('3x^2=27', [3, -3]), ('x^2-7=0', ['sqrt(7)', '-sqrt(7)']), ('x^2-5x=0', [0, 5]), ('3x^2+12x=0', [0, -4]), ('2x^2=7x', [0, '7/2']), ('-x^2+6x=0', [0, 6]),
             ('(x+3)(x-3)=7', [4, -4]), ('x(x-2)=4-2x', [2, -2]), ('(2x-1)^2=1', [0, 1]), ('(x+2)^2-4=3x', [0, -1]), ('x^2/3=12', [6, -6]), ('x^2/4-x/2=0', [0, 2]), ('(x^2+1)/5=2', [3, -3]),
             ('(x^2-2)/2-(x^2+1)/3=1', ['sqrt(14)', '-sqrt(14)']), ('5x^2=3x', [0, '3/5']), ('x^2-16=0', [4, -4]), ('x^2-3x=0', [0, 3]), ('2x^2+x=0', [0, '-1/2'])]: ce(e, v)

# =====================================================================
# 7. Equacions de segon grau completes
X = sec(T('Equacions de segon grau completes', 'Ecuaciones de segundo grado completas'))
C1 = ['x^2-6x+8=0', 'x^2+2x-8=0', 'x^2-4x-5=0', 'x^2+7x+12=0']
q, s = eqs(C1, 4, 2)
X.append((1, T("Resol amb la fórmula:", "Resuelve con la fórmula:") + q + recorda(T(r"$x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$. \ Compte amb els signes: si $b=-6$, aleshores $-b=6$ i $b^2=36$.", r"$x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$. \ Cuidado con los signos: si $b=-6$, entonces $-b=6$ y $b^2=36$.")), s))
C2 = ['2x^2-5x+2=0', '3x^2+x-2=0', '6x^2-x-1=0', '4x^2+4x-3=0']
q, s = eqs(C2, 4, 2)
X.append((1, T("Resol:", "Resuelve:") + q, s))
C3 = ['-x^2+x+6=0', '2x^2+4x-6=0', 'x^2-x-20=0', '3x^2-3x-18=0']
q, s = eqs(C3, 4, 1)
X.append((2, T(r"Resol (si $a$ és negatiu, multiplica per $-1$; si tots els coeficients tenen un divisor comú, simplifica):", r"Resuelve (si $a$ es negativo, multiplica por $-1$; si todos los coeficientes tienen un divisor común, simplifica):") + q, s))
C4 = ['(x-1)(x+4)=6', '(x+2)^2=3x+10', 'x(x+3)=2(x+3)', '3x(x-2)-(x-1)(x+1)=9']
q, s = eqs(C4, 2, 1)
X.append((2, T("Redueix a la forma general i resol:", "Reduce a la forma general y resuelve:") + q, s))
C5 = ['x^2/2-x/3=4/3', '(x^2-1)/3+x/2=2']
q, s = eqs(C5, 2, 1)
X.append((3, T("Resol:", "Resuelve:") + q, s))
C6 = ['x(x-1)/3=x-1', 'x(x+1)/2-(x-1)(x+2)/3=1']
q, s = eqs(C6, 2, 1)
X.append((3, T("Resol:", "Resuelve:") + q, s))
X.append((3, T("Escriu una equació de segon grau, en forma general, que tinga per solucions:", "Escribe una ecuación de segundo grado, en forma general, que tenga por soluciones:") + tasks(2, [T(r'$2$ i $-5$', r'$2$ y $-5$'), T(r'$\tfrac12$ i $3$', r'$\tfrac12$ y $3$')]) + recorda(T(r"si les solucions són $r$ i $s$, l'equació $(x-r)(x-s)=0$ les té.", r"si las soluciones son $r$ y $s$, la ecuación $(x-r)(x-s)=0$ las tiene.")),
    tasks(2, [r'$(x-2)(x+5)=0\Rightarrow\res{x^2+3x-10=0}$', r'$(2x-1)(x-3)=0\Rightarrow\res{2x^2-7x+3=0}$'])))
checkall(C1 + C2 + C3 + C4 + C5 + C6)
for e, v in [('x^2-6x+8=0', [2, 4]), ('x^2+2x-8=0', [2, -4]), ('x^2-4x-5=0', [5, -1]), ('x^2+7x+12=0', [-3, -4]), ('2x^2-5x+2=0', [2, '1/2']), ('3x^2+x-2=0', ['2/3', -1]), ('6x^2-x-1=0', ['1/2', '-1/3']),
             ('4x^2+4x-3=0', ['1/2', '-3/2']), ('-x^2+x+6=0', [3, -2]), ('2x^2+4x-6=0', [1, -3]), ('x^2-x-20=0', [5, -4]), ('3x^2-3x-18=0', [3, -2]), ('(x-1)(x+4)=6', [2, -5]), ('(x+2)^2=3x+10', [2, -3]),
             ('x(x+3)=2(x+3)', [2, -3]), ('3x(x-2)-(x-1)(x+1)=9', [4, -1]), ('x^2/2-x/3=4/3', [2, '-4/3']), ('(x^2-1)/3+x/2=2', [2, '-7/2']), ('x(x-1)/3=x-1', [1, 3]), ('x(x+1)/2-(x-1)(x+2)/3=1', [1, -2])]: ce(e, v)
chk('(x-2)(x+5)', 'x^2+3x-10'); chk('(2x-1)(x-3)', '2x^2-7x+3')

# =====================================================================
# 8. El discriminant
X = sec(T('El discriminant', 'El discriminante'))
NS = [T('cap solució', 'ninguna solución'), T('una solució', 'una solución'), T('dues solucions', 'dos soluciones')]
def ds(lst):
    out = []
    for e, a, b, c in lst:
        D = b * b - 4 * a * c; n = 2 if D > 0 else 1 if D == 0 else 0
        assert len(set(v for v in sp.solve(S(e.split('=')[0]), x) if v.is_real)) == n; NCHK[0] += 1
        out.append(r'$\Delta=%s$: \rest{%s}' % (D, NS[n]))
    return out
DS1 = [('x^2-10x+25=0', 1, -10, 25), ('2x^2+3x+4=0', 2, 3, 4), ('x^2-x-1=0', 1, -1, -1), ('-3x^2+2x+1=0', -3, 2, 1)]
X.append((1, T("Calcula el discriminant i digues quantes solucions té cada equació, sense resoldre-la:", "Calcula el discriminante y di cuántas soluciones tiene cada ecuación, sin resolverla:") + tasks(4, ['$%s$' % tx(e) for e, *_ in DS1])
    + recorda(T(r"$\Delta=b^2-4ac$. \ Si $\Delta>0$, dues solucions; si $\Delta=0$, una (doble); si $\Delta<0$, cap.", r"$\Delta=b^2-4ac$. \ Si $\Delta>0$, dos soluciones; si $\Delta=0$, una (doble); si $\Delta<0$, ninguna.")), tasks(2, ds(DS1))))
DS2 = [('x^2+4x+4=0', 1, 4, 4), ('x^2+x-12=0', 1, 1, -12), ('5x^2-2x+1=0', 5, -2, 1), ('x^2-9=0', 1, 0, -9), ('4x^2-12x+9=0', 4, -12, 9), ('x^2+3x=0', 1, 3, 0)]
X.append((1, T("Quantes solucions té cada equació?", "¿Cuántas soluciones tiene cada ecuación?") + tasks(3, ['$%s$' % tx(e) for e, *_ in DS2]), tasks(2, ds(DS2))))
Q3 = ['9x^2-6x+1=0', 'x^2+3x+5=0', 'x^2-2x-2=0', 'x^2+4x+1=0']
q, s = eqs(Q3, 4, 1)
X.append((2, T("Resol (fixa't en el discriminant abans de continuar):", "Resuelve (fíjate en el discriminante antes de continuar):") + q, s))
X.append((2, T(r"Escriu un valor de $c$ perquè l'equació $x^2+6x+c=0$ tinga: a) dues solucions; b) una sola solució; c) cap solució.", r"Escribe un valor de $c$ para que la ecuación $x^2+6x+c=0$ tenga: a) dos soluciones; b) una sola solución; c) ninguna solución."),
    T(r"$\Delta=36-4c$. \ a) $c<9$, per exemple \rest{$c=0$} \quad b) \rest{$c=9$} \quad c) $c>9$, per exemple \rest{$c=10$}", r"$\Delta=36-4c$. \ a) $c<9$, por ejemplo \rest{$c=0$} \quad b) \rest{$c=9$} \quad c) $c>9$, por ejemplo \rest{$c=10$}")))
ce('x^2+6x=0', [0, -6]); ce('x^2+6x+9=0', [-3]); ce('x^2+6x+10=0', [])
X.append((3, T("Respon:", "Responde:") + tasks(1, [T(r"Troba $k$ perquè l'equació $x^2-4x+k=0$ tinga una única solució. Quina és?", r"Halla $k$ para que la ecuación $x^2-4x+k=0$ tenga una única solución. ¿Cuál es?"),
                                                  T(r"Troba $m$ perquè $x^2+mx+16=0$ tinga una solució doble.", r"Halla $m$ para que $x^2+mx+16=0$ tenga una solución doble.")]),
    tasks(1, [T(r"$\Delta=16-4k=0\Rightarrow\res{k=4}$; \ $x^2-4x+4=0\Rightarrow\res{x=2}$ (doble)", r"$\Delta=16-4k=0\Rightarrow\res{k=4}$; \ $x^2-4x+4=0\Rightarrow\res{x=2}$ (doble)"),
              T(r"$m^2-64=0\Rightarrow\res{m=\pm8}$ \ ($x=-4$ o $x=4$, respectivament)", r"$m^2-64=0\Rightarrow\res{m=\pm8}$ \ ($x=-4$ o $x=4$, respectivamente)")])))
ce('x^2-4x+4=0', [2]); ce('x^2+8x+16=0', [-4]); ce('x^2-8x+16=0', [4])
X.append((3, T("Respon:", "Responde:") + tasks(1, [T(r"Per a quins valors de $m$ l'equació $x^2-2x+m=0$ té dues solucions?", r"¿Para qué valores de $m$ la ecuación $x^2-2x+m=0$ tiene dos soluciones?"),
                                                  T(r"Troba $k$ perquè $x=3$ siga solució de $x^2+kx-6=0$ i calcula l'altra solució.", r"Halla $k$ para que $x=3$ sea solución de $x^2+kx-6=0$ y calcula la otra solución.")]),
    tasks(1, [r"$\Delta=4-4m>0\Rightarrow 4>4m\Rightarrow\res{m<1}$", r"$9+3k-6=0\Rightarrow\res{k=-1}$; \ $x^2-x-6=0\Rightarrow x=3,\ \res{x=-2}$"])))
ce('x^2-x-6=0', [3, -2]); assert sp.solve(9 + 3 * k - 6, k) == [-1]
checkall(Q3)
ce('9x^2-6x+1=0', ['1/3']); ce('x^2+3x+5=0', []); ce('x^2-2x-2=0', ['1+sqrt(3)', '1-sqrt(3)']); ce('x^2+4x+1=0', ['-2+sqrt(3)', '-2-sqrt(3)'])

# =====================================================================
# 9. Problemes amb equacions de segon grau
PB2 = [
 (1, T(r"Si al quadrat d'un nombre li restem 5, obtenim 44. Quin pot ser el nombre?", r"Si al cuadrado de un número le restamos 5, obtenemos 44. ¿Qué número puede ser?"),
     T(r"$x^2-5=44\Rightarrow x^2=49$: \ \rest{$x=7$ o $x=-7$}", r"$x^2-5=44\Rightarrow x^2=49$: \ \rest{$x=7$ o $x=-7$}"), ('x^2-5=44', [7, -7])),
 (1, T(r"L'àrea d'un quadrat és 144 cm². Quant fa el costat? I si l'àrea fóra 50 cm²?", r"El área de un cuadrado es 144 cm². ¿Cuánto mide el lado? ¿Y si el área fuera 50 cm²?"),
     T(r"$x^2=144\Rightarrow\res{x=12\text{ cm}}$ ($-12$ no val); \ $x^2=50\Rightarrow\res{x=\sqrt{50}\approx7{,}07\text{ cm}}$", r"$x^2=144\Rightarrow\res{x=12\text{ cm}}$ ($-12$ no vale); \ $x^2=50\Rightarrow\res{x=\sqrt{50}\approx7{,}07\text{ cm}}$"), ('x^2=144', [12, -12])),
 (1, T(r"Un rectangle fa 3 m més de llarg que d'ample i la seua àrea és 40 m². Quines dimensions té?", r"Un rectángulo mide 3 m más de largo que de ancho y su área es 40 m². ¿Qué dimensiones tiene?"),
     T(r"$x(x+3)=40\Rightarrow x^2+3x-40=0\Rightarrow x=\tfrac{-3\pm13}{2}$: \ $x=5$ ($-8$ no val): \ \rest{5 m i 8 m}", r"$x(x+3)=40\Rightarrow x^2+3x-40=0\Rightarrow x=\tfrac{-3\pm13}{2}$: \ $x=5$ ($-8$ no vale): \ \rest{5 m y 8 m}"), ('x(x+3)=40', [5, -8])),
 (2, T(r"Troba dos nombres naturals consecutius el producte dels quals siga 156.", r"Halla dos números naturales consecutivos cuyo producto sea 156."),
     T(r"$x(x+1)=156\Rightarrow x^2+x-156=0\Rightarrow x=\tfrac{-1\pm25}{2}$: \ $x=12$ ($-13$ no és natural): \ \rest{12 i 13}", r"$x(x+1)=156\Rightarrow x^2+x-156=0\Rightarrow x=\tfrac{-1\pm25}{2}$: \ $x=12$ ($-13$ no es natural): \ \rest{12 y 13}"), ('x(x+1)=156', [12, -13])),
 (2, T(r"Si al quadrat d'un nombre li restem el seu triple, obtenim 40. Quin pot ser el nombre?", r"Si al cuadrado de un número le restamos su triple, obtenemos 40. ¿Qué número puede ser?"),
     T(r"$x^2-3x-40=0\Rightarrow x=\tfrac{3\pm13}{2}$: \ \rest{$x=8$ o $x=-5$}", r"$x^2-3x-40=0\Rightarrow x=\tfrac{3\pm13}{2}$: \ \rest{$x=8$ o $x=-5$}"), ('x^2-3x=40', [8, -5])),
 (2, T(r"Els catets d'un triangle rectangle mesuren $x$ i $x+7$ cm, i la hipotenusa 13 cm. Quant mesuren els catets?", r"Los catetos de un triángulo rectángulo miden $x$ y $x+7$ cm, y la hipotenusa 13 cm. ¿Cuánto miden los catetos?"),
     T(r"$x^2+(x+7)^2=169\Rightarrow x^2+7x-60=0\Rightarrow x=\tfrac{-7\pm17}{2}$: \ $x=5$: \ \rest{5 cm i 12 cm}", r"$x^2+(x+7)^2=169\Rightarrow x^2+7x-60=0\Rightarrow x=\tfrac{-7\pm17}{2}$: \ $x=5$: \ \rest{5 cm y 12 cm}"), ('x^2+(x+7)^2=169', [5, -12])),
 (2, T(r"Si al quadrat de l'edat d'en Pau li restem el triple de la seua edat, obtenim 130. Quants anys té?", r"Si al cuadrado de la edad de Pau le restamos el triple de su edad, obtenemos 130. ¿Cuántos años tiene?"),
     T(r"$x^2-3x-130=0\Rightarrow x=\tfrac{3\pm23}{2}$: \ $x=13$ ($-10$ no val): \ \rest{13 anys}", r"$x^2-3x-130=0\Rightarrow x=\tfrac{3\pm23}{2}$: \ $x=13$ ($-10$ no vale): \ \rest{13 años}"), ('x^2-3x=130', [13, -10])),
 (2, T(r"Si augmentem en 3 cm el costat d'un quadrat, la seua àrea augmenta 51 cm². Quant fa el costat?", r"Si aumentamos en 3 cm el lado de un cuadrado, su área aumenta 51 cm². ¿Cuánto mide el lado?"),
     T(r"$(x+3)^2-x^2=51\Rightarrow 6x+9=51\Rightarrow\res{x=7\text{ cm}}$ (els $x^2$ es cancel·len: és de primer grau!)", r"$(x+3)^2-x^2=51\Rightarrow 6x+9=51\Rightarrow\res{x=7\text{ cm}}$ (los $x^2$ se cancelan: ¡es de primer grado!)"), ('(x+3)^2-x^2=51', [7])),
 (3, T(r"La suma dels quadrats de dos nombres consecutius és 85. Quins poden ser?", r"La suma de los cuadrados de dos números consecutivos es 85. ¿Cuáles pueden ser?"),
     T(r"$x^2+(x+1)^2=85\Rightarrow x^2+x-42=0\Rightarrow x=\tfrac{-1\pm13}{2}$: \ \rest{6 i 7} \ o \ \rest{$-7$ i $-6$}", r"$x^2+(x+1)^2=85\Rightarrow x^2+x-42=0\Rightarrow x=\tfrac{-1\pm13}{2}$: \ \rest{6 y 7} \ o \ \rest{$-7$ y $-6$}"), ('x^2+(x+1)^2=85', [6, -7])),
 (3, T(r"Un rectangle té 34 m de perímetre i 60 m² d'àrea. Quines dimensions té?", r"Un rectángulo tiene 34 m de perímetro y 60 m² de área. ¿Qué dimensiones tiene?"),
     T(r"Si un costat fa $x$, l'altre fa $17-x$: \ $x(17-x)=60\Rightarrow x^2-17x+60=0\Rightarrow x=\tfrac{17\pm7}{2}$: \ \rest{12 m i 5 m}", r"Si un lado mide $x$, el otro mide $17-x$: \ $x(17-x)=60\Rightarrow x^2-17x+60=0\Rightarrow x=\tfrac{17\pm7}{2}$: \ \rest{12 m y 5 m}"), ('x(17-x)=60', [12, 5])),
 (3, T(r"La hipotenusa d'un triangle rectangle fa 10 cm i un catet fa 2 cm més que l'altre. Quant fan els catets?", r"La hipotenusa de un triángulo rectángulo mide 10 cm y un cateto mide 2 cm más que el otro. ¿Cuánto miden los catetos?"),
     T(r"$x^2+(x+2)^2=100\Rightarrow x^2+2x-48=0\Rightarrow x=\tfrac{-2\pm14}{2}$: \ $x=6$ ($-8$ no val): \ \rest{6 cm i 8 cm}", r"$x^2+(x+2)^2=100\Rightarrow x^2+2x-48=0\Rightarrow x=\tfrac{-2\pm14}{2}$: \ $x=6$ ($-8$ no vale): \ \rest{6 cm y 8 cm}"), ('x^2+(x+2)^2=100', [6, -8])),
 (3, T(r"Una piscina rectangular de 10 m × 6 m està envoltada per una vorera d'amplària constant. L'àrea total (piscina i vorera) és 96 m². Quina amplària té la vorera?", r"Una piscina rectangular de 10 m × 6 m está rodeada por una acera de anchura constante. El área total (piscina y acera) es 96 m². ¿Qué anchura tiene la acera?"),
     T(r"$(10+2x)(6+2x)=96\Rightarrow 4x^2+32x-36=0\Rightarrow x^2+8x-9=0\Rightarrow x=\tfrac{-8\pm10}{2}$: \ $x=1$ ($-9$ no val): \ \rest{1 m}", r"$(10+2x)(6+2x)=96\Rightarrow 4x^2+32x-36=0\Rightarrow x^2+8x-9=0\Rightarrow x=\tfrac{-8\pm10}{2}$: \ $x=1$ ($-9$ no vale): \ \rest{1 m}"), ('(10+2x)(6+2x)=96', [1, -9])),
]
for _, _, _, (e, s) in PB2: ce(e, s)
ce('x^2=50', ['sqrt(50)', '-sqrt(50)']); chk('x^2+(x+7)^2-169', '2(x^2+7x-60)'); chk('x^2+(x+1)^2-85', '2(x^2+x-42)'); chk('x^2+(x+2)^2-100', '2(x^2+2x-48)'); chk('(10+2x)(6+2x)-96', '4(x^2+8x-9)')
X = sec(T('Problemes amb equacions de segon grau', 'Problemas con ecuaciones de segundo grado'))
for i, (st, q, s, _) in enumerate(PB2):
    X.append((st, q + (recorda(T(r"l'equació pot tindre dues solucions: comprova quines tenen sentit en el problema (una longitud o una edat no poden ser negatives).", r"la ecuación puede tener dos soluciones: comprueba cuáles tienen sentido en el problema (una longitud o una edad no pueden ser negativas).")) if i == 0 else ''), s))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("equacions, identitats, equacions de primer grau, parèntesis, denominadors, problemes, equacions de segon grau, incompletes, fórmula, discriminant",
       'ecuaciones, identidades, ecuaciones de primer grado, paréntesis, denominadores, problemas, ecuaciones de segundo grado, incompletas, fórmula, discriminante')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T('Equacions de 1r i 2n grau', r'Ecuaciones de 1.\textsuperscript{er} y 2.\textsuperscript{o} grado')
TITM = T('Equacions de 1r i 2n grau', 'Ecuaciones de 1.er y 2.º grado')  # metadades del PDF (sense ordres)

def build(sol_):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 4: %s' % (t, TITM), capcalera='%s · Unidad 4: %s' % (t, TIT), pdfkeywords=KW, curs='2eso')
        cap = assignatura('2eso') + '{' + ('Soluciones de la ficha · Unidad 4' if sol_ else 'Ficha de ejercicios · Unidad 4') + '}{' + TIT + '}'
    else:
        t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat 4: %s. 2n d'ESO}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 4: %s · 2n d'ESO" % (t, TIT))
        assert "2n d'ESO" in p and 'Unitat 4' in p and 'unitat 4' in p
        cap = r'\capcalera{Matemàtiques}{2n ESO}{' + ('Solucions de la fitxa · Unitat 4' if sol_ else "Fitxa d'exercicis · Unitat 4") + '}{' + TIT + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol_ else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{12}\n\\input{../comu/fentmates.tex}\n\\fmcurs{2eso}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol_:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs calculadores que resolen pas a pas qualsevol equació de primer o de segon grau.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás calculadoras que resuelven paso a paso cualquier ecuación de primer o de segundo grado.") if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i comprova les solucions sempre que pugues. Fes els càlculs sense calculadora. Les seccions segueixen l'ordre dels apunts de la unitat (4.1--4.9).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y comprueba las soluciones siempre que puedas. Haz los cálculos sin calculadora. Las secciones siguen el orden de los apuntes de la unidad (4.1--4.9)."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            out.append('\\ex{%d} %s\n\n' % (st, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't4-fitxa-%s%s.tex' % ('solucions' if sol_ else 'exercicis', '-es' if ES else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
n_ = sum(len(x[1]) for x in S_)
print(n_, T('exercicis,', 'ejercicios,'), NCHK[0], T('comprovacions', 'comprobaciones'))
