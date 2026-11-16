# Genera t4-fitxa-exercicis.tex i t4-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 4: Equacions)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució), en valencià i castellà amb T(va, es).
# Les eines comunes (tasks, recorda, R, Rm, build) són a ../comu/eso4b.py; build(..., curs='4eso-a') posa la capçalera de
# Matemàtiques A. Les equacions s'escriuen una sola vegada en una notació senzilla, com al resolutor dels apunts
# (p. ex. '(x+1)/2-3(x-2)=x', 'sqrt(x+7)=x+1', '[ ]' per als claudàtors), i Q() en fa alhora el TeX de l'enunciat i
# l'expressió de sympy. Les solucions les calcula sympy: lin() les de primer grau (amb el m.c.m. i la forma ax=b),
# qd() les polinòmiques (forma reduïda ax^2+bx+c=0 i solucions), rac() les racionals (m.c.m., candidates i descartades)
# i chk() comprova les solucions escrites a mà (problemes i radicals).
# Ús: python3 genera.py (valencià) i python3 genera-es.py (castellà); després pdflatex dues vegades cada .tex.
import os, sys, re
from functools import reduce
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

LANG = 'es' if (len(sys.argv) > 1 and sys.argv[1] == 'es') else 'va'
def T(va, es): return es if LANG == 'es' else va

x = sp.symbols('x', real=True)

# ---------------------------------------------------------------------
# lector d'equacions: TeX + sympy
class Nd:
    def __init__(s, e, t, par=False, inner=None, dens=None): s.e, s.t, s.par, s.inner = e, t, par, inner
def Q(src):
    TK = r'\d+(?:[.,]\d+)?|sqrt|x|[-+*/^()\[\]]'
    toks = []
    st = {'i': 0, 'm': 1, 'dens': []}
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
                    if b.e.has(x): st['dens'].append(b.e)
                    else: st['m'] = sp.ilcm(st['m'], sp.Rational(b.e).p)
                    a = Nd(a.e / b.e, r'\dfrac{%s}{%s}' % (strip(a), strip(b)))
            elif p is not None and (p in ('x', '(', '[', 'sqrt') or re.match(r'\d', p)):
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
        if re.match(r'\d', q): return Nd(sp.Rational(q.replace(',', '.')), q.replace('.', ','))
        if q == 'x': return Nd(x, 'x')
        if q == 'sqrt':
            assert nx() == '('; e = expr(); assert nx() == ')'
            return Nd(sp.sqrt(e.e), r'\sqrt{%s}' % e.t)
        if q in '([':
            e = expr(); c = nx(); assert c == (')' if q == '(' else ']'), src
            big = r'\dfrac' in e.t or r'\sqrt' in e.t   # \left( només si cal: si no, deixa un espai després del coeficient
            L, Rr = ((r'\left(', r'\right)') if big else ('(', ')')) if q == '(' else ((r'\left[', r'\right]') if big else ('[', ']'))
            return Nd(e.e, L + e.t + Rr, True, e.t)
        raise ValueError(src)
    l, r = src.split('=')
    def side(t):
        st['i'] = 0; toks[:] = re.findall(TK, t.replace(' ', '')); assert ''.join(toks) == t.replace(' ', ''), src
        n = expr(); assert st['i'] == len(toks), src
        return n
    L = side(l); Rr = side(r)
    return {'t': L.t + '=' + Rr.t, 'L': L.e, 'R': Rr.e, 'm': st['m'], 'dens': st['dens'], 'src': src}
def D(src): return '$' + Q(src)['t'] + '$'

def tl(v):
    v = sp.nsimplify(v)
    if v.is_Rational:
        if v.q == 1: return str(v.p)
        return ('-' if v < 0 else '') + r'\frac{%d}{%d}' % (abs(v.p), v.q)
    return sp.latex(v)
def ptx(P):
    """polinomi amb coeficients racionals, de major a menor grau"""
    P = sp.Poly(sp.expand(P), x); n = P.degree(); out = ''
    for i, c in enumerate(P.all_coeffs()):
        c = sp.Rational(c); k = n - i
        if c == 0: continue
        s = '-' if c < 0 else ('+' if out else ''); a = abs(c)
        at = '' if (a == 1 and k > 0) else tl(a)
        out += s + at + ('' if k == 0 else 'x' if k == 1 else 'x^{%d}' % k)
    return out or '0'
def roots_tex(P):
    """solucions reals d'un polinomi (enters), juntant les parelles a ± b√c d'un factor de segon grau"""
    P = sp.Poly(P, x); out = []
    for f, mlt in sp.factor_list(P.as_expr())[1]:
        f = sp.Poly(f, x); d = f.degree()
        if d == 1:
            a, b = f.all_coeffs(); r = sp.Rational(-b, a); out.append((float(r), 'x=' + tl(r) + (r'\ \text{(doble)}' if mlt == 2 else '')))
        elif d == 2:
            A, B, C = [int(c) for c in f.all_coeffs()]; Dl = B * B - 4 * A * C
            if Dl < 0: continue
            k, rr = 1, Dl
            for p in range(2, int(Dl ** .5) + 1):
                while rr % (p * p) == 0: rr //= p * p; k *= p
            g = sp.igcd(sp.igcd(B, k), 2 * A); num_b, kk, den = -B // g, k // g, 2 * A // g
            if den < 0: num_b, den = -num_b, -den
            sq = (str(kk) if kk != 1 else '') + r'\sqrt{%d}' % rr
            top = (str(num_b) if num_b else '') + (r'\pm ' if num_b else r'\pm ') + sq
            out.append((float(-B / (2 * A)), 'x=' + (top if den == 1 else r'\frac{%s}{%d}' % (top, den))))
        else: raise ValueError(f)
    out.sort()
    return [t for _, t in out]
def Xs(L): return R(r',\ \ '.join(L))
NOSOL = lambda: T('no té solució', 'no tiene solución')

def realsols(e):
    S = sp.solveset(sp.Eq(e['L'], e['R']), x, domain=sp.S.Reals)
    return S
def chk(src, expected):
    """expected: llista de solucions reals ('R' = totes, [] = cap)"""
    ck(True, True)
    e = Q(src); S = realsols(e)
    if expected == 'R': assert S == sp.S.Reals, (src, S); return
    E = sp.FiniteSet(*[sp.sympify(v) for v in expected])
    if isinstance(S, sp.FiniteSet):   # en ESO, una arrel d'un nombre negatiu no existeix: es descarten
        S = sp.FiniteSet(*[a for a in S if sp.im(sp.N(e['L'].subs(x, a))) == 0 and sp.im(sp.N(e['R'].subs(x, a))) == 0])
    if S == sp.S.EmptySet: assert len(E) == 0, (src, S, E); return
    if isinstance(S, sp.FiniteSet):
        assert len(S) == len(E) and all(any(sp.simplify(a - b) == 0 for b in E) for a in S), (src, S, E)
    else:
        f = sp.lambdify(x, e['L'] - e['R'])
        for v in E: assert abs(complex(f(float(v)))) < 1e-9, (src, v)
        assert S.is_subset(sp.S.Reals) and E.is_subset(S) and False, (src, S)

def lin(src, expect):
    """primer grau: (m.c.m. o ·10) i ax=b → x"""
    e = Q(src); chk(src, expect)
    P = sp.expand(e['L'] - e['R']); Pp = sp.Poly(P, x); assert Pp.degree() <= 1, src
    m = e['m'] if ',' not in src else sp.ilcm(e['m'], 10)   # amb decimals, per 10
    for c in Pp.all_coeffs(): m = sp.ilcm(m, sp.Rational(c).q)
    P = sp.expand(m * P); a = P.coeff(x, 1); c = P.subs(x, 0)
    pre = ''
    if m != 1:
        pre = (T(r'm.c.m.$=%d$: ', r'm.c.m.$=%d$: ') % m) if e['m'] != 1 else (r'$\cdot%d$: ' % m)
    if a == 0:
        if c == 0: return pre + '$0x=0$: ' + R(r'\text{%s}' % T('infinites solucions', 'infinitas soluciones'))
        return pre + '$0x=%s$: ' % tl(-c) + R(r'\text{%s}' % NOSOL())
    r = sp.Rational(-c, a)
    lhs = ('' if a == 1 else '-' if a == -1 else tl(a)) + 'x'
    return pre + ('$' + lhs + '=' + tl(-c) + r'\Rightarrow$ ' if a != 1 else '') + R('x=' + tl(r))
def red(e):
    """forma reduïda entera (coeficient principal positiu) d'una equació sense x al denominador"""
    P = sp.expand(e['L'] - e['R']); Pp = sp.Poly(P, x)
    cs = [sp.Rational(c) for c in Pp.all_coeffs()]; m = reduce(sp.ilcm, [c.q for c in cs], 1)
    cs = [c * m for c in cs]; g = reduce(sp.igcd, [int(c) for c in cs]);
    if cs[0] < 0: g = -g
    return sp.expand(P * m / g)
def qd(src, expect, show=True):
    e = Q(src); chk(src, expect); P = red(e); S = roots_tex(P)
    return ('$' + ptx(P) + '=0$: ' if show else '') + (Xs(S) if S else R(r'\text{%s}' % NOSOL()))
def rac(src, expect):
    e = Q(src); chk(src, expect)
    M = sp.factor(reduce(sp.lcm, [sp.factor(d) for d in e['dens']] + [e['m']]))
    P = sp.cancel(sp.expand((e['L'] - e['R']) * M)); assert P.is_polynomial(x), src
    Pp = sp.Poly(P, x); cs = [sp.Rational(c) for c in Pp.all_coeffs()]
    g = reduce(sp.igcd, [int(c) for c in cs]); g = -g if cs[0] < 0 else g; P = sp.expand(P / g)
    cand = sorted(set(sp.solveset(P, x, sp.S.Reals)), key=float)
    bad = [v for v in cand if any(sp.simplify(d.subs(x, v)) == 0 for d in e['dens'])]
    good = [v for v in cand if v not in bad]
    s = T('m.c.m.$=%s$: ', 'm.c.m.$=%s$: ') % sp.latex(M).replace(r'\left(', '(').replace(r'\right)', ')') + '$' + ptx(P) + '=0$'
    if bad:
        s += r'; ' + ', '.join('$x=%s$' % tl(v) for v in bad) + T(' anul·la un denominador', ' anula un denominador') if len(bad) == 1 else \
             r'; ' + ', '.join('$x=%s$' % tl(v) for v in bad) + T(' anul·len un denominador', ' anulan un denominador')
    s += ': ' + (Xs(['x=' + tl(v) for v in good]) if good else R(r'\text{%s}' % NOSOL()))
    assert set(good) == set(sp.FiniteSet(*[sp.sympify(v) for v in expect])) or not expect and not good, (src, good)
    return s

S = []

# =====================================================================
# 1. Equacions de primer grau
E11 = [('3x-7=2x+5', ['12']), ('5x+4=2x-11', ['-5']), ('2(x-3)=x+4', ['10']), ('4-(x+2)=3x-6', ['2']), ('3(2x-1)-2(x+4)=1', ['3']), ('7-2(3-x)=5(x-1)', ['2'])]
E12 = [('5(x-2)-3(2x+1)=2(x-8)', ['1']), ('2[x-3(x+1)]=4-x', ['-10/3']), ('x-2[x-(3-x)]=7', ['-1/3']), ('3(x+2)-(x-4)=2(x+5)', 'R'), ('4(x-1)-2(x+3)=2(x-6)', []), ('6-[2x-(x+5)]=3(x-1)', ['7/2'])]
E14 = ['3(x+4)=x+10', 'x^2-3x=2(3-x)', '(x+1)/3=(x-4)/2', '4-3x=5(x+4)']
def vx(src, v):
    e = Q(src); a, b = sp.nsimplify(e['L'].subs(x, v)), sp.nsimplify(e['R'].subs(x, v))
    return '$' + tl(a) + ('=' if a == b else r'\neq ') + tl(b) + '$: ' + R(r'\text{%s}' % (T('sí', 'sí') if a == b else 'no'))
E13 = [('0,2(x+5)-0,5x=0,1(x-6)', ['4']), ('1,5(x-2)=0,5x+3', ['6']), ('0,3x-1,2=0,1(x+4)', ['8'])]
S.append((T("Equacions de primer grau", "Ecuaciones de primer grado"), [
 (1, T("Resol:", "Resuelve:") + tasks(3, [D(s) for s, _ in E11])
     + recorda(T("Primer trau els parèntesis; després passa les $x$ a un membre i els nombres a l'altre.", "Primero quita los paréntesis; después pasa las $x$ a un miembro y los números al otro.")),
     tasks(3, [lin(s, v) for s, v in E11])),
 (2, T("Resol i indica si alguna equació no té solució o en té infinites:", "Resuelve e indica si alguna ecuación no tiene solución o tiene infinitas:") + tasks(2, [D(s) for s, _ in E12])
     + recorda(T(r"Compte amb el signe menys davant d'un parèntesi o d'un claudàtor: $-(x-3)=-x+3$. Comença pels parèntesis de dins.", r"Cuidado con el signo menos delante de un paréntesis o de un corchete: $-(x-3)=-x+3$. Empieza por los paréntesis de dentro.")),
     tasks(2, [lin(s, v) for s, v in E12])),
 (2, T("Resol (pots multiplicar per 10 per a eliminar els decimals):", "Resuelve (puedes multiplicar por 10 para eliminar los decimales):") + tasks(2, [D(s) for s, _ in E13]),
     tasks(2, [lin(s, v) for s, v in E13])),
 (2, T(r"Comprova, sense resoldre-les, si $x=-2$ és solució de cada equació:", r"Comprueba, sin resolverlas, si $x=-2$ es solución de cada ecuación:") + tasks(2, [D(s) for s in E14]),
     tasks(2, [vx(s, -2) for s in E14])),
 (3, T(r"Escriu una equació de primer grau amb parèntesis que tinga per solució $x=-3$, una que no tinga solució i una que en tinga infinites.", r"Escribe una ecuación de primer grado con paréntesis que tenga por solución $x=-3$, una que no tenga solución y una que tenga infinitas."),
     T(r"Per exemple: $2(x+5)=x+7$; \ $2(x+1)=2x+5$; \ $3(x-1)=3x-3$.", r"Por ejemplo: $2(x+5)=x+7$; \ $2(x+1)=2x+5$; \ $3(x-1)=3x-3$.")),
]))
chk('2(x+5)=x+7', ['-3']); chk('2(x+1)=2x+5', []); chk('3(x-1)=3x-3', 'R')

# =====================================================================
# 2. Equacions de primer grau amb denominadors
E21 = [('x/2+x/3=10', ['12']), ('x-x/4=9', ['12']), ('(x+1)/3=(x-1)/2', ['5']), ('x/3-1/2=x/4', ['6'])]
E22 = [('(x-2)/3-(x+1)/4=1', ['23']), ('(3x-1)/2-(x+3)/5=x+1', ['7']), ('x-(x-2)/6=(2x+1)/3+1/2', ['3']), ('(5x+1)/4-(x-1)/2=(x+5)/4', ['1'])]
E23 = [('2(x-1)/3-(3x+1)/4=(x-5)/6-1', ['11/3']), ('(x+1)/2-(2x-3)/3=(x+3)/6-(x-1)/3', []), ('3(x-2)/4-(x+1)/2=(x-8)/4', 'R'), ('x/2-(x-(x+1)/3)/4=1', ['11/4'])]
E24 = [('(x+4)/5-(x-2)/10=(x+1)/2-(2x-1)/4', ['-5/2']), ('1-(x-3)/6=(2-x)/4+(x+5)/12', [])]
S.append((T("Equacions de primer grau amb denominadors", "Ecuaciones de primer grado con denominadores"), [
 (1, T("Resol:", "Resuelve:") + tasks(2, [D(s) for s, _ in E21], gap='12pt'),
     tasks(2, [lin(s, v) for s, v in E21])),
 (2, T("Resol:", "Resuelve:") + tasks(2, [D(s) for s, _ in E22], gap='14pt')
     + recorda(T(r"Multiplica tots els termes pel m.c.m. dels denominadors. Si el numerador té diversos termes, posa'l entre parèntesis: $-\dfrac{x-1}{2}\cdot4=-2(x-1)$.", r"Multiplica todos los términos por el m.c.m. de los denominadores. Si el numerador tiene varios términos, ponlo entre paréntesis: $-\dfrac{x-1}{2}\cdot4=-2(x-1)$.")),
     tasks(2, [lin(s, v) for s, v in E22])),
 (3, T("Resol i indica si alguna equació no té solució o en té infinites:", "Resuelve e indica si alguna ecuación no tiene solución o tiene infinitas:") + tasks(2, [D(s) for s, _ in E23], gap='14pt'),
     tasks(2, [lin(s, v) for s, v in E23])),
 (3, T("Resol:", "Resuelve:") + tasks(1, [D(s) for s, _ in E24], gap='14pt'),
     tasks(2, [lin(s, v) for s, v in E24])),
]))

# =====================================================================
# 3. Problemes de primer grau
chk('x+(x+1)+(x+2)=147', ['48']); chk('41-x=4(14-x)', ['5']); chk('x-x/3-(2/5)(2x/3)=240', ['600']); chk('8*30+12x=9,5(30+x)', ['18'])
chk('120x=90(x+1,5)', ['9/2']); chk('x+2x+(2x+200)=1400', ['240']); chk('0,8x=68', ['85']); chk('x/6+x/3=1', ['2']); chk('2x+(x-4)=50', ['18'])
S.append((T("Problemes de primer grau", "Problemas de primer grado"), [
 (1, T("La suma de tres nombres consecutius és 147. Quins són?", "La suma de tres números consecutivos es 147. ¿Cuáles son?"),
     r"$x+(x+1)+(x+2)=147\Rightarrow3x=144\Rightarrow x=48$: " + R(r"48,\ 49,\ 50")),
 (1, T("Un abric rebaixat un 20\\,\\% costa 68 €. Quant costava abans de la rebaixa?", "Un abrigo rebajado un 20\\,\\% cuesta 68 €. ¿Cuánto costaba antes de la rebaja?"),
     r"$0,8x=68\Rightarrow x=" + Rm(r"85\ \text{€}") + "$."),
 (2, T("Laura té 14 anys i sa mare, 41. Fa quants anys l'edat de la mare era el quàdruple de la de Laura?", "Laura tiene 14 años y su madre, 41. ¿Hace cuántos años la edad de la madre era el cuádruple de la de Laura?"),
     r"$41-x=4(14-x)\Rightarrow3x=15\Rightarrow x=5$: " + R(r"\text{%s}" % T("fa 5 anys", "hace 5 años")) + T(" (36 i 9 anys).", " (36 y 9 años).")),
 (2, T("Un triangle isòsceles té 50 cm de perímetre. El costat desigual fa 4 cm menys que cadascun dels costats iguals. Quant fa cada costat?", "Un triángulo isósceles tiene 50 cm de perímetro. El lado desigual mide 4 cm menos que cada uno de los lados iguales. ¿Cuánto mide cada lado?"),
     r"$2x+(x-4)=50\Rightarrow x=18$: " + R(r"18,\ 18\ \text{%s}\ 14\ \text{cm}" % T("i", "y"))),
 (2, T("D'un dipòsit d'aigua se'n gasta $\\frac13$ dilluns i dimarts, $\\frac25$ del que quedava. Encara queden 240 L. Quina capacitat té el dipòsit?", "De un depósito de agua se gasta $\\frac13$ el lunes y el martes, $\\frac25$ de lo que quedaba. Todavía quedan 240 L. ¿Qué capacidad tiene el depósito?"),
     T(r"Després de dilluns queden $\frac23x$; dimarts se'n gasten $\frac25\cdot\frac23x=\frac4{15}x$: ", r"Después del lunes quedan $\frac23x$; el martes se gastan $\frac25\cdot\frac23x=\frac4{15}x$: ")
     + r"$x-\dfrac x3-\dfrac{4x}{15}=240\Rightarrow\dfrac{6x}{15}=240\Rightarrow x=" + Rm(r"600\ \text{L}") + "$."),
 (2, T("Mesclem 30 kg de cafè de 8 €/kg amb cafè de 12 €/kg i obtenim una mescla que ix a 9,50 €/kg. Quants quilos del segon cafè hem posat?", "Mezclamos 30 kg de café de 8 €/kg con café de 12 €/kg y obtenemos una mezcla que sale a 9,50 €/kg. ¿Cuántos kilos del segundo café hemos puesto?"),
     r"$8\cdot30+12x=9,5(30+x)\Rightarrow240+12x=285+9,5x\Rightarrow2,5x=45\Rightarrow x=" + Rm(r"18\ \text{kg}") + "$."),
 (2, T("Un pare reparteix 1\\,400 € entre tres fills. El segon rep el doble que el primer, i el tercer, 200 € més que el segon. Quant rep cadascú?", "Un padre reparte 1\\,400 € entre tres hijos. El segundo recibe el doble que el primero, y el tercero, 200 € más que el segundo. ¿Cuánto recibe cada uno?"),
     r"$x+2x+(2x+200)=1400\Rightarrow5x=1200\Rightarrow x=240$: " + R(r"240\ \text{€},\ 480\ \text{€}\ \text{%s}\ 680\ \text{€}" % T("i", "y"))),
 (3, T("Un cotxe ix d'una ciutat a 90 km/h. Una hora i mitja després n'ix un altre pel mateix camí a 120 km/h. Quant de temps tarda el segon a atrapar el primer? A quina distància de la ciutat l'atrapa?", "Un coche sale de una ciudad a 90 km/h. Una hora y media después sale otro por el mismo camino a 120 km/h. ¿Cuánto tarda el segundo en alcanzar al primero? ¿A qué distancia de la ciudad lo alcanza?"),
     T(r"Si el segon tarda $x$ hores, ", r"Si el segundo tarda $x$ horas, ") + r"$120x=90(x+1,5)\Rightarrow30x=135\Rightarrow x=4,5$: " + R(r"4\ \text{h}\ 30\ \text{min}") + T(", a ", ", a ") + R(r"540\ \text{km}") + "."),
 (3, T("Una aixeta omple un dipòsit en 6 hores i una altra, en 3 hores. Quant de temps tarden a omplir-lo si les obrim totes dues alhora?", "Un grifo llena un depósito en 6 horas y otro, en 3 horas. ¿Cuánto tardan en llenarlo si los abrimos los dos a la vez?"),
     T(r"En una hora omplin $\frac16$ i $\frac13$ del dipòsit. En $x$ hores: ", r"En una hora llenan $\frac16$ y $\frac13$ del depósito. En $x$ horas: ") + r"$\dfrac x6+\dfrac x3=1\Rightarrow x+2x=6\Rightarrow x=" + Rm(r"2\ \text{h}") + "$."),
]))

# =====================================================================
# 4. Equacions de segon grau incompletes
E41 = [('x^2-49=0', ['7', '-7']), ('3x^2-27=0', ['3', '-3']), ('x^2+16=0', []), ('5x^2-20x=0', ['0', '4']), ('2x^2=7x', ['0', '7/2']), ('4x^2-25=0', ['5/2', '-5/2']),
       ('x^2=5', ['sqrt(5)', '-sqrt(5)']), ('-x^2+6x=0', ['0', '6']), ('9x^2+4=0', [])]
E42 = [('(x+3)^2=6x+18', ['3', '-3']), ('x(x-4)=2x(x+1)', ['0', '-6']), ('(2x-1)(2x+1)=15', ['2', '-2']), ('(x-2)^2+(x+2)^2=26', ['3', '-3']), ('x^2/3-x/2=0', ['0', '3/2']), ('(x+5)(x-5)=x^2/2-5', ['2*sqrt(10)', '-2*sqrt(10)'])]
def inc(src, v):
    e = Q(src); chk(src, v); P = red(e); a, b, c = [sp.Rational(P.coeff(x, k)) for k in (2, 1, 0)]
    if c == 0: return '$' + ptx(P) + '=0$: ' + Xs(roots_tex(P))
    q = -c / a
    if q < 0: return '$x^2=' + tl(q) + '$: ' + R(r'\text{%s}' % NOSOL())
    return '$x^2=' + tl(q) + '$: ' + R(r'x=\pm' + sp.latex(sp.sqrt(q)))
S.append((T("Equacions de segon grau incompletes", "Ecuaciones de segundo grado incompletas"), [
 (1, T("Resol les equacions incompletes:", "Resuelve las ecuaciones incompletas:") + tasks(3, [D(s) for s, _ in E41])
     + recorda(T(r"$ax^2+c=0\Rightarrow x^2=-\frac ca$ (dues solucions oposades o cap). \ $ax^2+bx=0\Rightarrow x(ax+b)=0\Rightarrow x=0,\ x=-\frac ba$.", r"$ax^2+c=0\Rightarrow x^2=-\frac ca$ (dos soluciones opuestas o ninguna). \ $ax^2+bx=0\Rightarrow x(ax+b)=0\Rightarrow x=0,\ x=-\frac ba$.")),
     tasks(3, [inc(s, v) for s, v in E41])),
 (2, T("Opera i resol (totes acaben en una equació incompleta):", "Opera y resuelve (todas acaban en una ecuación incompleta):") + tasks(2, [D(s) for s, _ in E42], gap='10pt'),
     tasks(2, [inc(s, v) for s, v in E42])),
 (3, T(r"Per a quins valors de $c$ té solucions l'equació $x^2+c=0$? I l'equació $2x^2+bx=0$, quantes en té segons el valor de $b$?", r"¿Para qué valores de $c$ tiene soluciones la ecuación $x^2+c=0$? Y la ecuación $2x^2+bx=0$, ¿cuántas tiene según el valor de $b$?"),
     T(r"$x^2=-c$ té solucions si ", r"$x^2=-c$ tiene soluciones si ") + R(r"c\le0") + T(r" (si $c=0$, només $x=0$). \ $x(2x+b)=0$: ", r" (si $c=0$, solo $x=0$). \ $x(2x+b)=0$: ")
     + T(r"dues solucions si $b\neq0$ ($x=0$ i $x=-\frac b2$) i una (doble) si $b=0$.", r"dos soluciones si $b\neq0$ ($x=0$ y $x=-\frac b2$) y una (doble) si $b=0$.")),
]))

# =====================================================================
# 5. Equacions de segon grau completes
E51 = [('x^2-8x+15=0', ['3', '5']), ('x^2+3x-10=0', ['2', '-5']), ('2x^2-5x+2=0', ['2', '1/2']), ('x^2-10x+25=0', ['5']), ('3x^2+x+2=0', []), ('6x^2+x-2=0', ['1/2', '-2/3'])]
E53 = [('0,5x^2-1,5x+1=0', ['1', '2']), ('x^2/4-x+1=0', ['2']), ('0,2x^2+0,6x=2', ['2', '-5'])]
E52 = [('x^2-4x+1=0', ['2+sqrt(3)', '2-sqrt(3)']), ('x^2+2x-4=0', ['-1+sqrt(5)', '-1-sqrt(5)']), ('2x^2-6x+3=0', ['(3+sqrt(3))/2', '(3-sqrt(3))/2'])]
def disc(src):
    e = Q(src); P = red(e); a, b, c = [sp.Rational(P.coeff(x, k)) for k in (2, 1, 0)]; d = b * b - 4 * a * c
    return r'$\Delta=%s$: ' % tl(d) + R(r'\text{%s}' % (T('cap', 'ninguna') if d < 0 else T('una (doble)', 'una (doble)') if d == 0 else T('dues', 'dos')))
assert [sp.Rational(-31), 0, 13] == [9 - 40, 144 - 144, 1 + 12]
S.append((T("Equacions de segon grau completes", "Ecuaciones de segundo grado completas"), [
 (1, T("Resol:", "Resuelve:") + tasks(3, [D(s) for s, _ in E51])
     + recorda(r"$ax^2+bx+c=0\Rightarrow x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$."),
     tasks(3, [qd(s, v, False) for s, v in E51])),
 (2, T("Resol i deixa les solucions amb radicals:", "Resuelve y deja las soluciones con radicales:") + tasks(3, [D(s) for s, _ in E52]),
     tasks(3, [qd(s, v, False) for s, v in E52])),
 (2, T("Elimina els decimals o els denominadors i resol:", "Elimina los decimales o los denominadores y resuelve:") + tasks(3, [D(s) for s, _ in E53], gap='10pt'),
     tasks(2, [qd(s, v) for s, v in E53])),
 (2, T("Sense resoldre-les, calcula el discriminant i indica quantes solucions té cada equació:", "Sin resolverlas, calcula el discriminante e indica cuántas soluciones tiene cada ecuación:") + tasks(3, [D('2x^2-3x+5=0'), D('x^2+12x+36=0'), D('3x^2-x-1=0')]),
     tasks(3, [disc('2x^2-3x+5=0'), disc('x^2+12x+36=0'), disc('3x^2-x-1=0')])),
 (3, T(r"Troba el valor de $k$ perquè l'equació $x^2+kx+9=0$ tinga una solució doble, i calcula-la.", r"Halla el valor de $k$ para que la ecuación $x^2+kx+9=0$ tenga una solución doble, y calcúlala."),
     r"$\Delta=k^2-36=0\Rightarrow" + Rm(r"k=\pm6") + r"$; \ " + T("amb $k=6$, ", "con $k=6$, ") + R("x=-3") + T("; amb $k=-6$, ", "; con $k=-6$, ") + R("x=3") + "."),
 (3, T(r"Escriu una equació de segon grau amb coeficients enters que tinga per solucions $x=2$ i $x=-\frac32$.", r"Escribe una ecuación de segundo grado con coeficientes enteros que tenga por soluciones $x=2$ y $x=-\frac32$."),
     r"$(x-2)(2x+3)=0\Rightarrow" + Rm("2x^2-x-6=0") + T("$ (o qualsevol múltiple).", "$ (o cualquier múltiplo).")),
]))
chk('x^2+6x+9=0', ['-3']); chk('x^2-6x+9=0', ['3']); chk('2x^2-x-6=0', ['2', '-3/2'])

# =====================================================================
# 6. Segon grau amb parèntesis i denominadors
E61 = [('(x-3)^2=2x-6', ['3', '5']), ('(2x+1)(x-2)=x^2-4', ['1', '2']), ('x(x+2)-3(x-1)=9', ['3', '-2']), ('(x+1)^2-(x-2)(x+2)=x^2-3', ['4', '-2'])]
E62 = [('x^2/2-x/3=x/6+1', ['2', '-1']), ('x(x+1)/3-(x+2)/2=0', ['2', '-3/2']), ('(x+3)(x-3)/4-(x-1)^2/2=-2', ['1', '3']), ('(x-2)^2/3-(x+1)/2=(x-11)/6', ['2', '4'])]
E63 = [('(x+1)^2/2-(x-1)^2/3=(x+11)/6+x', ['-5', '2']), ('(2x-1)^2/3-(x+1)(x-1)/2=(x+7)/6', ['2', '-1/5']), ('(x-1)^2/2-(x+1)(x-3)/3=(x+9)/6', ['0', '3']), ('2(x-1)^2-3(x+1)(x-2)=x(x-5)-4', ['1+sqrt(7)', '1-sqrt(7)'])]
S.append((T("Segon grau amb parèntesis i denominadors", "Segundo grado con paréntesis y denominadores"), [
 (2, T("Opera fins a obtindre la forma $ax^2+bx+c=0$ i resol:", "Opera hasta obtener la forma $ax^2+bx+c=0$ y resuelve:") + tasks(2, [D(s) for s, _ in E61], gap='6pt'),
     tasks(2, [qd(s, v) for s, v in E61])),
 (2, T("Elimina els denominadors i resol:", "Elimina los denominadores y resuelve:") + tasks(2, [D(s) for s, _ in E62], gap='14pt')
     + recorda(T(r"Primer desenvolupa els productes i les identitats notables, i després multiplica pel m.c.m. Compte amb el signe menys davant d'una fracció!", r"Primero desarrolla los productos y las identidades notables, y después multiplica por el m.c.m. ¡Cuidado con el signo menos delante de una fracción!")),
     tasks(1, [qd(s, v) for s, v in E62])),
 (3, T("Resol:", "Resuelve:") + tasks(1, [D(s) for s, _ in E63], gap='14pt'),
     tasks(1, [qd(s, v) for s, v in E63])),
]))

# =====================================================================
# 7. Problemes de segon grau
chk('x+x^2=110', ['10', '-11']); chk('x(17-x)=60', ['5', '12']); chk('x^2+(x+7)^2=169', ['5', '-12']); chk('x(x+2)=168', ['12', '-14'])
chk('(20+2x)(15+2x)=594', ['7/2', '-21']); chk('120/x-120/(x+2)=5', ['6', '-8']); chk('(x+3)(x-2)=66', ['8', '-9']); chk('x^2+(x+1)^2=(x+2)^2', ['3', '-1'])
S.append((T("Problemes de segon grau", "Problemas de segundo grado"), [
 (2, T("Si a un nombre natural li sumem el seu quadrat obtenim 110. Quin és el nombre?", "Si a un número natural le sumamos su cuadrado obtenemos 110. ¿Cuál es el número?"),
     r"$x^2+x-110=0\Rightarrow x=10,\ x=-11$; " + T("ha de ser natural: ", "tiene que ser natural: ") + R("x=10") + "."),
 (2, T("El producte de les edats de dos germans és 168, i un té 2 anys més que l'altre. Quants anys tenen?", "El producto de las edades de dos hermanos es 168, y uno tiene 2 años más que el otro. ¿Cuántos años tienen?"),
     r"$x(x+2)=168\Rightarrow x^2+2x-168=0\Rightarrow x=12,\ x=-14$: " + R(r"12\ \text{%s}\ 14\ \text{%s}" % (T("i", "y"), T("anys", "años")))),
 (2, T("Un rectangle té 34 m de perímetre i 60 m² d'àrea. Quines dimensions té?", "Un rectángulo tiene 34 m de perímetro y 60 m² de área. ¿Qué dimensiones tiene?"),
     T(r"Els costats sumen 17: ", r"Los lados suman 17: ") + r"$x(17-x)=60\Rightarrow x^2-17x+60=0\Rightarrow x=12,\ x=5$: " + R(r"12\ \text{m}\times5\ \text{m}")),
 (2, T("La diagonal d'un rectangle fa 13 cm i un costat fa 7 cm més que l'altre. Calcula'n els costats i l'àrea.", "La diagonal de un rectángulo mide 13 cm y un lado mide 7 cm más que el otro. Calcula sus lados y el área."),
     r"$x^2+(x+7)^2=169\Rightarrow x^2+7x-60=0\Rightarrow x=5,\ x=-12$: " + R(r"5\ \text{cm}\ \text{%s}\ 12\ \text{cm}" % T("i", "y")) + "; " + R(r"A=60\ \text{cm}^2")),
 (2, T("Si un costat d'un jardí quadrat l'allarguem 3 m i l'altre l'escurcem 2 m, obtenim un rectangle de 66 m². Quant fa el costat del jardí?", "Si un lado de un jardín cuadrado lo alargamos 3 m y el otro lo acortamos 2 m, obtenemos un rectángulo de 66 m². ¿Cuánto mide el lado del jardín?"),
     r"$(x+3)(x-2)=66\Rightarrow x^2+x-72=0\Rightarrow x=8,\ x=-9$: " + R(r"8\ \text{m}")),
 (3, T("Una foto de $20\\times15$ cm té un marc de la mateixa amplada per tots els costats. L'àrea de la foto amb el marc és de 594 cm². Quina amplada té el marc?", "Una foto de $20\\times15$ cm tiene un marco de la misma anchura por todos los lados. El área de la foto con el marco es de 594 cm². ¿Qué anchura tiene el marco?"),
     r"$(20+2x)(15+2x)=594\Rightarrow4x^2+70x-294=0\Rightarrow2x^2+35x-147=0\Rightarrow x=\dfrac{-35\pm49}{4}$: " + R(r"x=3,5\ \text{cm}") + T(" (la negativa no val).", " (la negativa no vale).")),
 (3, T("Un grup d'amics ha de pagar 120 € a parts iguals. Si foren 2 amics més, cadascú pagaria 5 € menys. Quants amics són?", "Un grupo de amigos tiene que pagar 120 € a partes iguales. Si fueran 2 amigos más, cada uno pagaría 5 € menos. ¿Cuántos amigos son?"),
     r"$\dfrac{120}{x}-\dfrac{120}{x+2}=5\Rightarrow240=5x(x+2)\Rightarrow x^2+2x-48=0\Rightarrow x=6,\ x=-8$: " + R(r"6\ \text{%s}" % T("amics", "amigos")) + T(" (20 € cadascú).", " (20 € cada uno).")),
 (3, T("Els costats d'un triangle rectangle són tres nombres naturals consecutius. Quant fan?", "Los lados de un triángulo rectángulo son tres números naturales consecutivos. ¿Cuánto miden?"),
     r"$x^2+(x+1)^2=(x+2)^2\Rightarrow x^2-2x-3=0\Rightarrow x=3,\ x=-1$: " + R(r"3,\ 4\ \text{%s}\ 5" % T("i", "y"))),
]))

# =====================================================================
# 8. Equacions factoritzades
E81 = [('(x-3)(x+5)=0', ['3', '-5']), ('x(2x-7)=0', ['0', '7/2']), ('(x+1)(x-2)(3x+4)=0', ['-1', '2', '-4/3']), ('5(x-6)^2=0', ['6']), ('x(4x-1)(x+4)=0', ['0', '1/4', '-4']), ('(x^2-9)(x-1)=0', ['3', '-3', '1'])]
E82 = [('(x^2-5x+6)(x+4)=0', ['2', '3', '-4']), ('(x^2+4)(x^2-16)=0', ['4', '-4']), ('x^2(x^2-3x-10)=0', ['0', '5', '-2']), ('(2x-1)^2(x^2-2)=0', ['1/2', 'sqrt(2)', '-sqrt(2)'])]
E83 = [('x^3-9x=0', ['0', '3', '-3']), ('2x^3-8x^2=0', ['0', '4']), ('x^3-10x^2+25x=0', ['0', '5']), ('x^4-x^2=0', ['0', '1', '-1']), ('x^3+x^2-6x=0', ['0', '2', '-3']), ('3x^3-12x=0', ['0', '2', '-2'])]
F83 = [r"x(x+3)(x-3)", r"2x^2(x-4)", r"x(x-5)^2", r"x^2(x+1)(x-1)", r"x(x+3)(x-2)", r"3x(x+2)(x-2)"]
for (s, _), f in zip(E83, F83): assert sp.expand(Q(s)['L'] - Q(f + '=0')['L']) == 0, s
def fsol(src, v):
    chk(src, v); return Xs(['x=' + tl(sp.sympify(t)) for t in sorted(v, key=lambda t: float(sp.sympify(t)))])
S.append((T("Equacions factoritzades", "Ecuaciones factorizadas"), [
 (1, T("Resol sense multiplicar els factors:", "Resuelve sin multiplicar los factores:") + tasks(3, [D(s) for s, _ in E81])
     + recorda(T("Un producte val zero si algun dels factors val zero: iguala cada factor a 0.", "Un producto vale cero si alguno de los factores vale cero: iguala cada factor a 0.")),
     tasks(3, [fsol(s, v) for s, v in E81])),
 (2, T("Resol:", "Resuelve:") + tasks(2, [D(s) for s, _ in E82]),
     tasks(2, [fsol(s, v) + (T(" ($x^2+4=0$ no en dona)", " ($x^2+4=0$ no da ninguna)") if '(x^2+4)' in s else '') for s, v in E82])),
 (2, T("Factoritza traient factor comú (i, si cal, amb una identitat notable) i resol:", "Factoriza sacando factor común (y, si hace falta, con una identidad notable) y resuelve:") + tasks(3, [D(s) for s, _ in E83]),
     tasks(2, ['$' + f + '=0$: ' + fsol(s, v) for (s, v), f in zip(E83, F83)])),
 (3, T("Resol (compte: no estan igualades a zero):", "Resuelve (cuidado: no están igualadas a cero):") + tasks(2, [D('(x-1)(x+2)=x-1'), D('x(x-3)=2(x-3)')]),
     tasks(1, [r"$(x-1)(x+2)-(x-1)=0\Rightarrow(x-1)(x+1)=0$: " + fsol('(x-1)(x+2)=x-1', ['-1', '1']), r"$x(x-3)-2(x-3)=0\Rightarrow(x-3)(x-2)=0$: " + fsol('x(x-3)=2(x-3)', ['2', '3'])])),
]))

# =====================================================================
# 9. Equacions racionals
E91 = [('5/x-1=4', ['1']), ('x/(x-2)=3', ['3']), ('(x+1)/(x-1)=3', ['2']), ('2/(x+1)=3/(x-1)', ['-5']), ('x/4=9/x', ['6', '-6']), ('(x+2)/x=(x+8)/(x+2)', ['1'])]
E92 = [('x+8/x=6', ['2', '4']), ('1/x+1/(x+3)=1/2', ['3', '-2']), ('x/(x-1)+2/x=3', ['2', '1/2']), ('3/(x-1)+2/(x+1)=2', ['3', '-1/2'])]
E93 = [('x/(x-1)-2/(x+1)=4/(x^2-1)', ['2']), ('x/(x-3)+1=3/(x-3)', []), ('6/(x^2-4)-1/(x-2)=1/(x+2)', ['3']), ('(x+1)/x-x/(x+1)=5/6', ['2', '-3/5'])]
S.append((T("Equacions racionals", "Ecuaciones racionales"), [
 (1, T("Resol:", "Resuelve:") + tasks(3, [D(s) for s, _ in E91], gap='12pt')
     + recorda(T(r"En una proporció $\dfrac AB=\dfrac CD$ es pot multiplicar en creu: $A\cdot D=B\cdot C$.", r"En una proporción $\dfrac AB=\dfrac CD$ se puede multiplicar en cruz: $A\cdot D=B\cdot C$.")),
     tasks(2, [rac(s, v) for s, v in E91])),
 (2, T("Resol:", "Resuelve:") + tasks(2, [D(s) for s, _ in E92], gap='12pt'),
     tasks(1, [rac(s, v) for s, v in E92])),
 (3, T("Resol i comprova les solucions:", "Resuelve y comprueba las soluciones:") + tasks(2, [D(s) for s, _ in E93], gap='14pt')
     + recorda(T("Abans de donar les solucions, descarta les que anul·len algun denominador.", "Antes de dar las soluciones, descarta las que anulan algún denominador.")),
     tasks(1, [rac(s, v) for s, v in E93])),
 (3, T(r"La suma d'un nombre i el seu invers és $\frac{10}{3}$. Quin és el nombre?", r"La suma de un número y su inverso es $\frac{10}{3}$. ¿Cuál es el número?"),
     r"$x+\dfrac1x=\dfrac{10}{3}$; " + rac('x+1/x=10/3', ['3', '1/3']) + T(" (dues possibilitats).", " (dos posibilidades).")),
]))

# =====================================================================
# 10. Equacions amb radicals
E101 = [('sqrt(x+3)=4', ['13']), ('sqrt(2x-1)=3', ['5']), ('sqrt(x^2+9)=5', ['4', '-4']), ('sqrt(3x+1)=-2', []), ('2sqrt(x)=6', ['9']), ('sqrt(5x-1)=2', ['1'])]
S101 = [r"$x+3=16$: " + R("x=13"), r"$2x-1=9$: " + R("x=5"), r"$x^2=16$: " + R(r"x=\pm4"), T("Una arrel no pot ser negativa: ", "Una raíz no puede ser negativa: ") + R(r"\text{%s}" % NOSOL()), r"$\sqrt x=3$: " + R("x=9"), r"$5x-1=4$: " + R("x=1")]
E102 = [('sqrt(x+7)=x+1', ['2']), ('x-sqrt(x+2)=4', ['7']), ('sqrt(2x+1)+1=x', ['4']), ('sqrt(3x-2)=x', ['1', '2']), ('x+sqrt(x-1)=3', ['2']), ('2sqrt(x+1)=x+1', ['-1', '3'])]
S102 = [T(r"$x+7=x^2+2x+1\Rightarrow x^2+x-6=0\Rightarrow x=2,\ x=-3$; $x=-3$ no val ($\sqrt4\neq-2$): ", r"$x+7=x^2+2x+1\Rightarrow x^2+x-6=0\Rightarrow x=2,\ x=-3$; $x=-3$ no vale ($\sqrt4\neq-2$): ") + R("x=2"),
        T(r"$x-4=\sqrt{x+2}\Rightarrow x^2-9x+14=0\Rightarrow x=7,\ x=2$; $x=2$ no val ($2-2\neq4$): ", r"$x-4=\sqrt{x+2}\Rightarrow x^2-9x+14=0\Rightarrow x=7,\ x=2$; $x=2$ no vale ($2-2\neq4$): ") + R("x=7"),
        T(r"$\sqrt{2x+1}=x-1\Rightarrow x^2-4x=0\Rightarrow x=0,\ x=4$; $x=0$ no val ($1+1\neq0$): ", r"$\sqrt{2x+1}=x-1\Rightarrow x^2-4x=0\Rightarrow x=0,\ x=4$; $x=0$ no vale ($1+1\neq0$): ") + R("x=4"),
        T(r"$3x-2=x^2\Rightarrow x^2-3x+2=0$; totes dues valen: ", r"$3x-2=x^2\Rightarrow x^2-3x+2=0$; las dos valen: ") + R(r"x=1,\ \ x=2"),
        T(r"$\sqrt{x-1}=3-x\Rightarrow x^2-7x+10=0\Rightarrow x=2,\ x=5$; $x=5$ no val ($5+2\neq3$): ", r"$\sqrt{x-1}=3-x\Rightarrow x^2-7x+10=0\Rightarrow x=2,\ x=5$; $x=5$ no vale ($5+2\neq3$): ") + R("x=2"),
        T(r"$4(x+1)=(x+1)^2\Rightarrow x^2-2x-3=0$; totes dues valen: ", r"$4(x+1)=(x+1)^2\Rightarrow x^2-2x-3=0$; las dos valen: ") + R(r"x=-1,\ \ x=3")]
for p, v in [('x^2+x-6', [2, -3]), ('x^2-9*x+14', [7, 2]), ('x^2-4*x', [0, 4]), ('x^2-3*x+2', [1, 2]), ('x^2-7*x+10', [2, 5]), ('x^2-2*x-3', [-1, 3])]:
    assert set(sp.solve(sp.sympify(p.replace('x', 'X')).subs('X', x), x)) == set(v), p
assert sp.expand((x - 4) ** 2 - (x + 2)) == x ** 2 - 9 * x + 14 and sp.expand((x - 1) ** 2 - (2 * x + 1)) == x ** 2 - 4 * x and sp.expand((3 - x) ** 2 - (x - 1)) == x ** 2 - 7 * x + 10
assert sp.expand((x + 1) ** 2 - (x + 7)) == x ** 2 + x - 6 and sp.expand((x + 1) ** 2 - 4 * (x + 1)) == x ** 2 - 2 * x - 3
E103 = [('sqrt(2x+3)=sqrt(x+5)', ['2']), ('sqrt(5x-4)-sqrt(x+8)=0', ['3']), ('3sqrt(x-1)=sqrt(x+7)', ['2']), ('sqrt(x^2-7)=sqrt(x+5)', ['4', '-3']), ('sqrt(x^2+3x)=2sqrt(x)', ['0', '1']), ('sqrt(x^2-3)=sqrt(2x)', ['3'])]
S103 = [r"$2x+3=x+5$: " + R("x=2"), r"$5x-4=x+8$: " + R("x=3"), r"$9(x-1)=x+7$: " + R("x=2"),
        T(r"$x^2-x-12=0$; totes dues valen ($\sqrt9=\sqrt9$, $\sqrt2=\sqrt2$): ", r"$x^2-x-12=0$; las dos valen ($\sqrt9=\sqrt9$, $\sqrt2=\sqrt2$): ") + R(r"x=4,\ \ x=-3"),
        T(r"$x^2+3x=4x\Rightarrow x^2-x=0$; totes dues valen: ", r"$x^2+3x=4x\Rightarrow x^2-x=0$; las dos valen: ") + R(r"x=0,\ \ x=1"),
        T(r"$x^2-2x-3=0\Rightarrow x=3,\ x=-1$; $x=-1$ no val ($\sqrt{-2}$ no existeix): ", r"$x^2-2x-3=0\Rightarrow x=3,\ x=-1$; $x=-1$ no vale ($\sqrt{-2}$ no existe): ") + R("x=3")]
for s, v in E101 + E102 + E103: chk(s, v)
chk('sqrt(x+2)=x-4', ['7']); chk('x-sqrt(25-x^2)=1', ['4']); chk('sqrt(x^2+5)+1=2x', ['2'])
assert sp.expand((x - 1) ** 2 - (25 - x ** 2)) == 2 * (x ** 2 - x - 12) and sp.expand((2 * x - 1) ** 2 - (x ** 2 + 5)) == 3 * x ** 2 - 4 * x - 4
S.append((T("Equacions amb radicals", "Ecuaciones con radicales"), [
 (1, T("Resol:", "Resuelve:") + tasks(3, [D(s) for s, _ in E101]),
     tasks(3, S101)),
 (2, T("Resol i comprova les solucions:", "Resuelve y comprueba las soluciones:") + tasks(3, [D(s) for s, _ in E102])
     + recorda(T("Aïlla el radical, eleva els dos membres al quadrat i comprova totes les solucions en l'equació inicial.", "Aísla el radical, eleva los dos miembros al cuadrado y comprueba todas las soluciones en la ecuación inicial.")),
     tasks(1, S102)),
 (2, T("Resol (dos radicals: posa'n un a cada membre i eleva al quadrat):", "Resuelve (dos radicales: pon uno en cada miembro y eleva al cuadrado):") + tasks(3, [D(s) for s, _ in E103]),
     tasks(1, S103)),
 (3, T("Resol i comprova les solucions:", "Resuelve y comprueba las soluciones:") + tasks(2, [D('x-sqrt(25-x^2)=1'), D('sqrt(x^2+5)+1=2x')]),
     tasks(1, [T(r"$\sqrt{25-x^2}=x-1\Rightarrow 25-x^2=x^2-2x+1\Rightarrow x^2-x-12=0\Rightarrow x=4,\ x=-3$; $x=-3$ no val ($-3-4\neq1$): ", r"$\sqrt{25-x^2}=x-1\Rightarrow 25-x^2=x^2-2x+1\Rightarrow x^2-x-12=0\Rightarrow x=4,\ x=-3$; $x=-3$ no vale ($-3-4\neq1$): ") + R("x=4"),
               T(r"$\sqrt{x^2+5}=2x-1\Rightarrow x^2+5=4x^2-4x+1\Rightarrow3x^2-4x-4=0\Rightarrow x=2,\ x=-\frac23$; $x=-\frac23$ no val ($\frac73+1\neq-\frac43$): ", r"$\sqrt{x^2+5}=2x-1\Rightarrow x^2+5=4x^2-4x+1\Rightarrow3x^2-4x-4=0\Rightarrow x=2,\ x=-\frac23$; $x=-\frac23$ no vale ($\frac73+1\neq-\frac43$): ") + R("x=2")])),
 (3, T("Si a un nombre li sumem 2 i en fem l'arrel quadrada, obtenim el mateix nombre menys 4. Quin és el nombre?", "Si a un número le sumamos 2 y hacemos su raíz cuadrada, obtenemos el mismo número menos 4. ¿Cuál es el número?"),
     T(r"$\sqrt{x+2}=x-4\Rightarrow x^2-9x+14=0\Rightarrow x=7,\ x=2$; $x=2$ no val: ", r"$\sqrt{x+2}=x-4\Rightarrow x^2-9x+14=0\Rightarrow x=7,\ x=2$; $x=2$ no vale: ") + R("x=7")),
]))

# =====================================================================
TITOL = T("Equacions", "Ecuaciones")
KW = T("equacions, equacions de primer grau, denominadors, problemes, equacions de segon grau, completes, incompletes, discriminant, equacions factoritzades, equacions racionals, equacions amb radicals",
       "ecuaciones, ecuaciones de primer grado, denominadores, problemas, ecuaciones de segundo grado, completas, incompletas, discriminante, ecuaciones factorizadas, ecuaciones racionales, ecuaciones con radicales")
INTRO_EX = T(r"Resol-los al quadern mostrant tots els passos. Pots comprovar els resultats amb el resolutor pas a pas dels apunts interactius.", r"Resuélvelos en el cuaderno mostrando todos los pasos. Puedes comprobar los resultados con el resolutor paso a paso de los apuntes interactivos.")
INTRO_SOL = T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat.",
              r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad.")
build(HERE, 4, TITOL, S, KW, INTRO_EX, INTRO_SOL, lang=LANG, curs='4eso-a')
