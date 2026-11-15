# Versió en castellà de genera.py. Genera t6-fitxa-exercicis-es.tex i t6-fitxa-solucions-es.tex
# (1r ESO, Unitat 6: Introducció a l'àlgebra. Equacions de 1r grau)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les resolucions de les equacions les escriu sol1() pas a pas (m.c.m., parèntesis, transposició, reducció i aïllament)
# i les asserts chk/cv/ce comproven amb sympy totes les reduccions, valors numèrics i solucions escrites a mà.
import os, re
from math import gcd
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- àlgebra i comprovacions ----------
x = sp.Symbol('x')
SY = {v: sp.Symbol(v) for v in 'abchlmnyz'}
SY['x'] = x
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
NCHK = [0]
def S(s): return parse_expr(s.replace('\\cdot', '*').replace('·', '*').replace('[', '(').replace(']', ')'), transformations=TR, local_dict=SY) if isinstance(s, str) else s
def chk(l, r):
    NCHK[0] += 1
    assert sp.expand(S(l) - S(r)) == 0, (l, r, sp.expand(S(l)))
def cv(e, vals, res):
    NCHK[0] += 1
    v = S(e).subs({SY[k]: sp.nsimplify(w) for k, w in vals.items()})
    assert sp.nsimplify(v) == sp.nsimplify(res), (e, vals, v, res)
def ce(eq, sol):
    """equació de primer grau (sol = valor) o 'totes' / 'cap'"""
    NCHK[0] += 1
    l, r = eq.split('=')
    e = sp.expand(S(l) - S(r))
    if sol == 'totes': assert e == 0, eq; return
    if sol == 'cap': assert e != 0 and not e.has(x), eq; return
    assert sp.degree(e, x) == 1 and sp.solve(e, x) == [sp.nsimplify(sol)], (eq, sp.solve(e, x), sol)
def ntex(c):
    c = sp.Rational(c)
    return str(c.p) if c.q == 1 else ('-' if c < 0 else '') + r'\tfrac{%d}{%d}' % (abs(c.p), c.q)
def pt(e):
    """polinomi en x en TeX, de grau més alt a més baix"""
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
            if kq == 1 and sg != '-' and num.startswith('(') and num.endswith(')') and num.count('(') == 1: num = num[1:-1]
            q = num if kq == 1 else ('%d%s' % (kq * int(md.group(1)), md.group(2)) if md else '%d%s' % (kq, num))
        out += ('-' if sg == '-' else ('+' if j else '')) + q
    return re.sub(r'\^(\d+)', r'^{\1}', out).replace('*', r'\cdot ')
def tside(t):
    parts = split_terms(t)
    out = ''
    for j, (sg, p) in enumerate(parts):
        m = re.match(r'^(.*)/(\d+)$', p)
        if m and m.group(1).count('(') == m.group(1).count(')'):
            num = m.group(1)
            if num.startswith('(') and num.endswith(')') and num.count('(') == 1: num = num[1:-1]
            p = r'\dfrac{%s}{%s}' % (num, m.group(2))
        out += ('-' if sg == '-' else ('+' if j else '')) + p
    out = re.sub(r'\^(\d+)', r'^{\1}', out).replace('*', r'\cdot ')
    return re.sub(r'(\d)\.(\d)', r'\1,\2', out)
def tx(s):
    """expressió o equació escrita com a l'entrada -> TeX (les fraccions a/b dels termes, amb \\dfrac)"""
    return '='.join(tside(t) for t in s.split('='))
def E(s): return '$' + tx(s) + '$'

# ---------- resolució automàtica de primer grau ----------
def tx_terms(cs, lit):
    """[3, -1] amb lit='x' -> 3x-x; amb lit='' -> 3-1"""
    out = ''
    for i, c in enumerate(cs):
        q = abs(sp.Rational(c))
        out += ('-' if c < 0 else ('+' if i else '')) + ((ntex(q) if q != 1 or not lit else '') + lit)
    return out or '0'
def coefs(side):
    """termes d'un membre: [(coef. de x, constant)] de cada terme"""
    out = []
    for sg, p in split_terms(side):
        e = sp.expand(S(p) * (-1 if sg == '-' else 1))
        out.append((sp.Rational(e.coeff(x, 1)), sp.Rational(e.coeff(x, 0))))
    return out
def sol1(eq):
    """resolució pas a pas (en TeX) d'una equació de primer grau"""
    l, r = eq.split('=')
    L, R = S(l), S(r)
    m = 1
    for d in re.findall(r'/(\d+)', eq): m = m * int(d) // gcd(m, int(d))
    L2, R2 = sp.expand(L * m), sp.expand(R * m)
    st = []
    if m > 1:
        ms = (mside(l, m), mside(r, m))
        chk(ms[0].replace(r'\cdot', '*').replace('{', '(').replace('}', ')'), L2); chk(ms[1].replace(r'\cdot', '*').replace('{', '(').replace('}', ')'), R2)
        st.append(r'\text{m.c.m.}=%d:\ \ %s=%s' % (m, ms[0], ms[1]))
        if '(' in ms[0] + ms[1]: st.append('%s=%s' % (pt(L2), pt(R2)))
        lt, rt = coefs(str(L2)), coefs(str(R2))
    elif '(' in eq:
        st.append('%s=%s' % (pt(L2), pt(R2)))
        lt, rt = coefs(str(L2)), coefs(str(R2))
    else:
        lt, rt = coefs(l), coefs(r)
    ax = [a for a, b in lt if a] + [-a for a, b in rt if a]
    bs = [b for a, b in rt if b] + [-b for a, b in lt if b]
    A, B = sum(ax), sum(bs)
    trans = any(a for a, b in rt) or any(b for a, b in lt)
    if trans: st.append('%s=%s' % (tx_terms(ax, 'x'), tx_terms(bs, '')))
    if A == 0:
        st.append('0x=%s' % ntex(B))
        res = r'\res{\text{todas las } x \text{ son solución (identidad)}}' if B == 0 else r'\res{\text{sin solución}}'
        ce(eq, 'totes' if B == 0 else 'cap')
        return '$' + r'\ \Rightarrow\ '.join(st + [res]) + '$'
    s = sp.Rational(B) / A
    if len(ax) > 1 or len(bs) > 1 or not trans:
        red = '%s=%s' % (tx_terms([A], 'x'), ntex(B))
        if A != 1 and not (st and (st[-1] == red or st[-1].endswith(r'\ ' + red))): st.append(red)
    if A == 1: res = r'\res{x=%s}' % ntex(s)
    elif A == -1: res = r'\res{x=%s}' % ntex(s)
    elif sp.Rational(B, A) == sp.Rational(B) / A and A > 0 and gcd(int(abs(B)), int(A)) == 1 and sp.Rational(B).q == 1: res = r'\res{x=%s}' % ntex(s)
    else: res = r'x=\tfrac{%s}{%s}=\res{%s}' % (ntex(B), ntex(A), ntex(s))
    ce(eq, s)
    if A == 1 and not trans and st and (st[-1] == 'x=%s' % ntex(s) or st[-1].endswith(r'\ x=%s' % ntex(s))):
        st[-1] = st[-1][:-len('x=%s' % ntex(s))] + res; res = None
    return '$' + r'\ \Rightarrow\ '.join(st + ([res] if res else [])) + '$'
def eqs(lst, n, ns=None):
    """llista d'equacions -> (enunciats, solucions)"""
    return tasks(n, [E(e) for e in lst]), tasks(ns or 1, [sol1(e) for e in lst])

# ---------- figures TikZ ----------
def punts(n):
    """figura n de la sèrie 3n+2: una columna de 2 punts i n columnes de 3"""
    g = r'\fill[accent] (0,0.2) circle (0.09); \fill[accent] (0,0.6) circle (0.09);'
    for i in range(1, n + 1):
        for j in range(3): g += r'\fill[navy] (%.2f,%.2f) circle (0.09);' % (i * 0.4, j * 0.4)
    return r'\begin{tikzpicture}[baseline=0]%s\end{tikzpicture}' % g
def balanca(a, b, c, d):
    """balança amb a capses i b pesos d'1 kg a l'esquerra i c capses i d pesos a la dreta"""
    def plat(cx, nx, nu):
        g = r'\draw[muted] (%.2f,2.2)--(%.2f,0.5) (%.2f,2.2)--(%.2f,0.5);' % (cx, cx - 1.3, cx, cx + 1.3)
        g += r'\draw[thick,fill=soft] (%.2f,0.5) arc (180:360:1.3 and 0.25);' % (cx - 1.3)
        items = ['x'] * nx + ['1'] * nu
        for k, it in enumerate(items):
            row, col = divmod(k, 5)
            px, py = cx - 0.96 + col * 0.48, 0.72 + row * 0.46
            if it == 'x': g += r'\draw[fill=navy!80,draw=navy] (%.2f,%.2f) rectangle +(0.38,0.38); \node[text=white,font=\small\itshape] at (%.2f,%.2f) {x};' % (px - 0.19, py - 0.19, px, py)
            else: g += r'\draw[fill=accent!60,draw=accent] (%.2f,%.2f) circle (0.18); \node[font=\tiny] at (%.2f,%.2f) {1};' % (px, py, px, py)
        return g
    g = r'\draw[fill=soft,draw=muted] (3,2.2)--(2.6,-0.4)--(3.4,-0.4)--cycle; \draw[line width=2pt] (0.6,2.2)--(5.4,2.2); \fill[accent] (3,2.2) circle (0.09);'
    return r'\begin{tikzpicture}[scale=0.85]%s%s%s\end{tikzpicture}' % (g, plat(1.2, a, b), plat(4.8, c, d))

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
TR1 = [("El doble de un número", '2x'), ('Un número más 7', 'x+7'), ("El triple de un número menos 2", '3x-2'), ("La mitad de un número", r'\dfrac{x}{2}'),
       ("El cuadrado de un número", 'x^2'), ("Un número menos su cuarta parte", r'x-\dfrac{x}{4}'), ("El consecutivo de un número", 'x+1'), ("El doble de un número más su triple", '2x+3x')]
PAR = [('x+5', 'Un número más 5'), ('3x', "El triple de un número"), ('x-1', "El anterior de un número ($x$ menos 1)"), (r'\dfrac{x}{3}', "La tercera parte de un número"),
       ('2(x+4)', "El doble de la suma de un número y 4"), ('x^2-1', "El cuadrado de un número menos 1")]
S_.append(("Lenguaje algebraico", [
 (1, r"Expresa en lenguaje algebraico (usa la letra $x$):" + tasks(2, [a for a, _ in TR1])
     + recorda(r"Entre un número y una letra no escribimos el punto de multiplicar: $3\cdot x=3x$. «El doble de un número más 3» es $2x+3$, pero «el doble de la suma de un número y 3» es $2(x+3)$."),
     tasks(2, [r'%s: $\res{%s}$' % (a, b) for a, b in TR1])),
 (1, r"Escribe con palabras qué expresa cada expresión algebraica:" + tasks(3, ['$%s$' % a for a, _ in PAR]),
     tasks(2, [r'$%s$: \rest{%s}' % (a, b) for a, b in PAR]) + r"\par (Hay otras maneras correctas de decirlo.)"),
 (2, r"La edad de Nuria es $x$ años. Expresa en lenguaje algebraico:" + tasks(2, ["La edad de Nuria dentro de 6 años.", "La edad de Nuria hace 4 años.", "La edad de su abuela, que tiene 5 veces la de Nuria.", "La edad de su primo, que tiene la mitad de años que ella.", "La suma de las edades de Nuria y su abuela.", "La edad de la abuela dentro de 10 años."]),
     tasks(3, [r'$\res{x+6}$', r'$\res{x-4}$', r'$\res{5x}$', r'$\res{\dfrac{x}{2}}$', r'$\res{x+5x}$', r'$\res{5x+10}$'])),
 (2, r"Expresa en lenguaje algebraico:" + tasks(2, ["Dos números consecutivos.", "Un número par y el par siguiente.", "Un número impar.", "La suma de tres números consecutivos.", "El precio de $x$ cuadernos si cada uno cuesta $1,50$\\,€.", "Los céntimos de $x$ monedas de 20 céntimos."]),
     tasks(2, [r'$\res{x}$ y $\res{x+1}$', r'$\res{2x}$ y $\res{2x+2}$', r'$\res{2x+1}$', r'$\res{x+(x+1)+(x+2)}$', r'$\res{1,5x}$\,€', r'$\res{20x}$ céntimos'])),
 (2, r"Escribe una fórmula para:" + tasks(1, ["Los euros que pagamos por $n$ entradas de cine a 8\\,€ cada una.", "El número de ruedas que hay en $c$ coches y $m$ motos.", "Los minutos que hay en $h$ horas.", "El perímetro y el área de un cuadrado de lado $l$."]),
     tasks(2, [r'$\res{8n}$', r'$\res{4c+2m}$', r'$\res{60h}$', r'$P=\res{4l}$, \ $A=\res{l^2}$'])),
 (3, r"Observa la serie de figuras hechas con puntos:\par\smallskip{\centering %s\qquad\qquad %s\qquad\qquad %s\par}\smallskip " % (punts(1), punts(2), punts(3))
     + r"a) ¿Cuántos puntos tiene cada figura? ¿Cuántos tendrá la figura 4? \ b) Escribe una expresión para los puntos de la figura $n$. \ c) ¿Cuántos puntos tendrá la figura 10? ¿Y la figura 50?",
     r"a) $5,\ 8,\ 11$; la figura 4 tiene $\res{14}$ (cada figura añade 3). \ b) $\res{3n+2}$ (2 puntos a la izquierda y 3 por cada columna). \ c) $3\cdot10+2=\res{32}$; \ $3\cdot50+2=\res{152}$."),
 (3, r"Traduce al lenguaje algebraico:" + tasks(1, ["La diferencia entre el triple de un número y su mitad.", "El doble de la suma de un número y su consecutivo.", "La suma de los cuadrados de dos números $a$ y $b$.", "El cuadrado de la suma de dos números $a$ y $b$."]),
     tasks(2, [r'$\res{3x-\dfrac{x}{2}}$', r'$\res{2\bigl(x+(x+1)\bigr)}$', r'$\res{a^2+b^2}$', r'$\res{(a+b)^2}$'])),
]))
for k, v in [(1, 5), (2, 8), (3, 11), (4, 14), (10, 32), (50, 152)]: cv('3n+2', {'n': k}, v)

# =====================================================================
V2 = [('x^2+1', {'x': 3}, 10, 'x=3'), ('2a+b', {'a': 4, 'b': -3}, 5, 'a=4,\\ b=-3'), ('10-3x', {'x': -2}, 16, 'x=-2'), ('x/2+5', {'x': 8}, 9, 'x=8'), ('3(x-1)', {'x': 4}, 9, 'x=4'), ('a*b-a', {'a': -2, 'b': 5}, -8, 'a=-2,\\ b=5')]
for e, vv, r, _ in V2: cv(e, vv, r)
XS = [-2, -1, 0, 1, 2, 3]
def fila(e): return [str(S(e).subs(x, v)) for v in XS]
S_.append(("Expresiones algebraicas. Valor numérico", [
 (1, r"Calcula el valor numérico de $4x-3$ para: \quad a) $x=2$ \quad b) $x=0$ \quad c) $x=-1$ \quad d) $x=5$"
     + recorda(r"Para calcular el valor numérico, sustituimos la letra por el número y hacemos las operaciones respetando la jerarquía. Los números negativos, siempre entre paréntesis: si $x=-3$, \ $x^2=(-3)^2=9$."),
     tasks(4, [r'$4\cdot2-3=\res{5}$', r'$4\cdot0-3=\res{-3}$', r'$4\cdot(-1)-3=\res{-7}$', r'$4\cdot5-3=\res{17}$'])),
 (1, r"Calcula el valor numérico de cada expresión para los valores indicados:" + tasks(2, [r'%s \ para \ $%s$' % (E(e), t) for e, _, _, t in V2]),
     tasks(2, [r'$3^2+1=\res{10}$', r'$2\cdot4+(-3)=\res{5}$', r'$10-3\cdot(-2)=10+6=\res{16}$', r'$\dfrac{8}{2}+5=\res{9}$', r'$3\cdot(4-1)=\res{9}$', r'$(-2)\cdot5-(-2)=-10+2=\res{-8}$'])),
 (2, r"Copia y completa la tabla de valores:\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|%s|}\hline $x$ & %s\\\hline $2x+1$ & %s\\\hline $x^2-x$ & %s\\\hline\end{tabular}\par}"
     % ('C{0.9cm}|' * len(XS), ' & '.join('$%d$' % v for v in XS), ' & '.join([''] * len(XS)), ' & '.join([''] * len(XS))),
     r"{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|%s|}\hline $x$ & %s\\\hline $2x+1$ & %s\\\hline $x^2-x$ & %s\\\hline\end{tabular}\par}"
     % ('C{0.9cm}|' * len(XS), ' & '.join('$%d$' % v for v in XS), ' & '.join(r'$\res{%s}$' % v for v in fila('2x+1')), ' & '.join(r'$\res{%s}$' % v for v in fila('x^2-x')))),
 (2, r"Usa las fórmulas para calcular:" + tasks(1, [r"El área de un triángulo, $A=\dfrac{b\cdot h}{2}$, si $b=10$\,cm y $h=7$\,cm.", r"El perímetro de un rectángulo, $P=2b+2h$, si $b=12$\,cm y $h=4,5$\,cm.", r"El volumen de un cubo, $V=a^3$, si $a=4$\,cm."]),
     tasks(1, [r'$A=\dfrac{10\cdot7}{2}=\res{35\text{\,cm}^2}$', r'$P=2\cdot12+2\cdot4,5=24+9=\res{33\text{\,cm}}$', r'$V=4^3=\res{64\text{\,cm}^3}$'])),
 (2, r"Una compañía de teléfono cobra 5\,€ al mes más $0,10$\,€ por cada minuto de llamada. Escribe la expresión de lo que pagamos en un mes si hablamos $m$ minutos. ¿Cuánto pagamos si hablamos 120 minutos? ¿Y si hablamos 45?",
     r"$P=\res{5+0,1m}$. \quad $m=120$: \ $5+0,1\cdot120=5+12=\res{17\text{\,€}}$. \quad $m=45$: \ $5+0,1\cdot45=5+4,5=\res{9,50\text{\,€}}$."),
 (3, r"¿Qué expresión da el valor de $y$ en cada tabla?\par\smallskip{\centering\renewcommand{\arraystretch}{1.3}\begin{tabular}{|c|C{0.8cm}|C{0.8cm}|C{0.8cm}|C{0.8cm}|}\hline $x$ & 1 & 2 & 3 & 4\\\hline $y$ & 2 & 6 & 10 & 14\\\hline\end{tabular}\qquad\begin{tabular}{|c|C{0.8cm}|C{0.8cm}|C{0.8cm}|C{0.8cm}|}\hline $x$ & 0 & 1 & 2 & 3\\\hline $y$ & 1 & 2 & 5 & 10\\\hline\end{tabular}\par}",
     r"Primera: $y$ aumenta de 4 en 4, así que empieza por $4x$; para $x=1$, $4-2=2$: \ $y=\res{4x-2}$. \quad Segunda: cada $y$ es el cuadrado de $x$ más 1: \ $y=\res{x^2+1}$."),
 (3, r"Busca probando un valor de $x$ que haga que: \ a) $3x+2$ valga 20; \ b) $x^2$ valga 49; \ c) $2x+5$ y $x+9$ tengan el mismo valor.",
     r"a) $x=\res{6}$ ($3\cdot6+2=20$). \ b) $x=\res{7}$ o $x=\res{-7}$ ($(-7)^2=49$). \ c) $x=\res{4}$ (los dos valen 13)."),
]))
cv('4x-3', {'x': 2}, 5); cv('4x-3', {'x': 0}, -3); cv('4x-3', {'x': -1}, -7); cv('4x-3', {'x': 5}, 17)
cv('b*h/2', {'b': 10, 'h': 7}, 35); cv('2b+2h', {'b': 12, 'h': sp.Rational(9, 2)}, 33); cv('a^3', {'a': 4}, 64)
cv('5+m/10', {'m': 120}, 17); cv('5+m/10', {'m': 45}, sp.Rational(19, 2))
for k, v in zip([1, 2, 3, 4], [2, 6, 10, 14]): cv('4x-2', {'x': k}, v)
for k, v in zip([0, 1, 2, 3], [1, 2, 5, 10]): cv('x^2+1', {'x': k}, v)
ce('3x+2=20', 6); cv('x^2', {'x': -7}, 49); ce('2x+5=x+9', 4)

# =====================================================================
MON = [('6x^3', '6', 'x^3', '3'), ('-a^2b', '-1', 'a^2b', '3'), ('xy', '1', 'xy', '2'), ('-7', '-7', r'\text{—}', '0'), (r'\tfrac{3}{4}x^2y^2', r'\tfrac{3}{4}', 'x^2y^2', '4'), ('-z', '-1', 'z', '1')]
POL = [('3x^2-5x+1', 3, 2, '1'), ('7-x^3', 2, 3, '7'), ('x^4+2x^2-x', 3, 4, '0'), ('5x-8', 2, 1, '-8')]
S_.append(("Monomios y polinomios", [
 (1, r"Copia y completa la tabla:\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.2cm}|C{2.2cm}|C{1.4cm}|}\hline Monomio & Coeficiente & Parte literal & Grado\\\hline "
     + r'\\\hline '.join('$%s$ & & & ' % m for m, _, _, _ in MON) + r'\\\hline\end{tabular}\par}'
     + recorda(r"En el monomio $-5x^2y$: el coeficiente es $-5$, la parte literal es $x^2y$ y el grado es la suma de los exponentes, $2+1=3$. Si no hay número, el coeficiente es 1 (o $-1$)."),
     r"{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.2cm}|C{2.2cm}|C{1.4cm}|}\hline Monomio & Coeficiente & Parte literal & Grado\\\hline "
     + r'\\\hline '.join(r'$%s$ & $\res{%s}$ & $\res{%s}$ & $\res{%s}$' % r for r in MON) + r'\\\hline\end{tabular}\par}'),
 (1, r"¿Cuáles de estas expresiones son monomios?" + tasks(4, ['$5x^2$', '$x+1$', '$-3ab$', r'$\dfrac{4}{x}$', '$8$', '$x^2y^3$', '$2^x$', r'$\dfrac{x}{5}$']),
     r"Son monomios: \ $\res{5x^2}$, \ $\res{-3ab}$, \ $\res{8}$, \ $\res{x^2y^3}$ \ y \ $\res{\dfrac{x}{5}}$ (es $\frac{1}{5}x$). \ No lo son: $x+1$ (es una suma), $\frac{4}{x}$ (la letra divide) y $2^x$ (la letra está en el exponente)."),
 (2, r"Agrupa los monomios semejantes: \quad $4x,\ \ -2x^2,\ \ 3xy,\ \ x,\ \ 5x^2,\ \ -xy,\ \ 7,\ \ -3x$",
     r"Con $x$: \ $\res{4x,\ x,\ -3x}$. \quad Con $x^2$: \ $\res{-2x^2,\ 5x^2}$. \quad Con $xy$: \ $\res{3xy,\ -xy}$. \quad Sin letra: \ $\res{7}$."),
 (2, r"Escribe: \ a) dos monomios semejantes a $-2x^3$; \ b) un monomio de grado 5 con coeficiente 4; \ c) un monomio de grado 0; \ d) un monomio de grado 2 con dos letras diferentes.",
     r"Por ejemplo: \ a) $\res{5x^3}$ y $\res{x^3}$; \ b) $\res{4x^5}$ (o $4x^2y^3$); \ c) $\res{9}$; \ d) $\res{-xy}$. \ (Hay muchas respuestas correctas.)"),
 (2, r"Indica el número de términos, el grado y el término independiente de cada polinomio:" + tasks(2, ['$%s$' % p for p, _, _, _ in POL]),
     tasks(2, [r'$%s$: \ \res{%d} términos, grado \res{%d}, término indep. $\res{%s}$' % r for r in POL])),
 (3, r"Escribe un monomio semejante a $6x^2y$ que: \ a) sumado con él dé 0; \ b) sumado con él dé $10x^2y$; \ c) restado de él dé $x^2y$.",
     r"a) $\res{-6x^2y}$ \quad b) $\res{4x^2y}$ \quad c) $\res{5x^2y}$ \ (porque $6x^2y-5x^2y=x^2y$)."),
 (3, r"Calcula el valor numérico: \ a) del monomio $-3x^2y$ para $x=-2$, $y=5$; \ b) del polinomio $x^3-2x+1$ para $x=-1$; \ c) del polinomio $2x^2-3x$ para $x=\frac{1}{2}$.",
     r"a) $-3\cdot(-2)^2\cdot5=-3\cdot4\cdot5=\res{-60}$ \quad b) $(-1)^3-2\cdot(-1)+1=-1+2+1=\res{2}$ \quad c) $2\cdot\frac{1}{4}-\frac{3}{2}=\frac{1}{2}-\frac{3}{2}=\res{-1}$"),
]))
for p, nt_, g, ti in POL:
    e = sp.Poly(S(p), x); assert len(e.terms()) == nt_ and e.degree() == g and str(S(p).subs(x, 0)) == ti, p
chk('6x^2*y-6x^2*y', 0); chk('6x^2*y+4x^2*y', '10x^2*y'); chk('6x^2*y-5x^2*y', 'x^2*y')
cv('-3x^2*y', {'x': -2, 'y': 5}, -60); cv('x^3-2x+1', {'x': -1}, 2); cv('2x^2-3x', {'x': sp.Rational(1, 2)}, -1)

# =====================================================================
SUM = [('5x+3x', '8x'), ('9a-4a', '5a'), ('x+x+x', '3x'), ('2x-7x', '-5x'), ('4x^2+x^2', '5x^2'), ('-3ab+8ab', '5ab'), ('6y-y', '5y'), ('-x-x', '-2x')]
RED = [('3x+2+5x-1', '8x+1'), ('7-2x+4-x', '-3x+11'), ('x^2+3x-2x^2+x', '-x^2+4x'), ('5a+2b-3a+b', '2a+3b')]
PRO = [('3*5x', '15x'), ('2x*4x', '8x^2'), ('(-3a)*2a', '-6a^2'), ('x*x^2', 'x^3'), ('5x*(-2y)', '-10xy'), ('(-4x^2)*(-x)', '4x^3')]
DIS = [('4(x+3)', '4x+12'), ('2(5x-1)', '10x-2'), ('-3(x+2)', '-3x-6'), ('-(4x-7)', '-4x+7'), ('x(x+5)', 'x^2+5x'), ('2x(3x-1)', '6x^2-2x')]
TP = [('2(x+4)+3x', '2x+8+3x', '5x+8'), ('5x-(2x+3)', '5x-2x-3', '3x-3'), ('3(x-2)+2(x+5)', '3x-6+2x+10', '5x+4'), ('4(2x+1)-(x-6)', '8x+4-x+6', '7x+10')]
T3 = [('3(2x-1)-2(x-4)+x', '6x-3-2x+8+x', '5x+5'), ('5-2(3x+1)+4(x-2)', '5-6x-2+4x-8', '-2x-5'), ('x(x+2)-3(x-1)', 'x^2+2x-3x+3', 'x^2-x+3')]
for l, r in SUM + RED + PRO + DIS: chk(l, r)
for l, m, r in TP + T3: chk(l, m); chk(m, r)
def txp(s): return tx(s).replace('*', r'\cdot ')
S_.append(("Operaciones con monomios. Reducir expresiones", [
 (1, r"Calcula:" + tasks(4, ['$%s$' % txp(a) for a, _ in SUM])
     + recorda(r"Solo podemos sumar o restar monomios semejantes: sumamos los coeficientes y dejamos la parte literal. $3x+5x=8x$, pero $3x+2$ no se puede reducir."),
     tasks(4, [r'$%s=\res{%s}$' % (txp(a), txp(b)) for a, b in SUM])),
 (1, r"Reduce:" + tasks(2, ['$%s$' % txp(a) for a, _ in RED]),
     tasks(2, [r'$%s=\res{%s}$' % (txp(a), txp(b)) for a, b in RED])),
 (1, r"Multiplica:" + tasks(3, ['$%s$' % txp(a) for a, _ in PRO]),
     tasks(3, [r'$%s=\res{%s}$' % (txp(a), txp(b)) for a, b in PRO])),
 (2, r"Aplica la propiedad distributiva:" + tasks(3, ['$%s$' % txp(a) for a, _ in DIS])
     + recorda(r"$a(b+c)=ab+ac$: multiplicamos por \emph{cada} término del paréntesis. Un signo menos delante cambia todos los signos: $-(x-5)=-x+5$."),
     tasks(3, [r'$%s=\res{%s}$' % (txp(a), txp(b)) for a, b in DIS])),
 (2, r"Quita paréntesis y reduce:" + tasks(2, ['$%s$' % txp(a) for a, _, _ in TP]),
     tasks(2, [r'$%s=%s=\res{%s}$' % (txp(a), txp(m), txp(b)) for a, m, b in TP])),
 (2, r"Halla el error en cada igualdad y corrígela:" + tasks(2, ['$3x+4=7x$', '$2(x+5)=2x+5$', '$-(x-3)=-x-3$', r'$x\cdot x=2x$']),
     tasks(2, [r"$3x+4$ \rest{no es reducible} (no son semejantes)", r'$2(x+5)=\res{2x+10}$', r'$-(x-3)=\res{-x+3}$', r'$x\cdot x=\res{x^2}$ \ ($x+x=2x$)'])),
 (3, r"Reduce:" + tasks(1, ['$%s$' % txp(a) for a, _, _ in T3]),
     tasks(1, [r'$%s=%s=\res{%s}$' % (txp(a), txp(m), txp(b)) for a, m, b in T3])),
 (3, r"Escribe de forma reducida el perímetro de: \ a) un rectángulo de base $2x+1$ y altura $x-1$; \ b) un triángulo de lados $x$, $x+3$ y $2x-1$. Calcúlalos para $x=4$.",
     r"a) $2(2x+1)+2(x-1)=4x+2+2x-2=\res{6x}$; para $x=4$: $\res{24}$. \quad b) $x+(x+3)+(2x-1)=\res{4x+2}$; para $x=4$: $\res{18}$."),
 (3, r"Adivinanza: piensa un número, súmale 5, multiplica el resultado por 2, réstale 10 y divide entre 2. ¿Qué obtienes? Explica por qué pasa siempre usando el álgebra.",
     r"Siempre obtienes \rest{el número que has pensado}: \ $\dfrac{2(x+5)-10}{2}=\dfrac{2x+10-10}{2}=\dfrac{2x}{2}=\res{x}$."),
]))
chk('2(2x+1)+2(x-1)', '6x'); cv('6x', {'x': 4}, 24); chk('x+(x+3)+(2x-1)', '4x+2'); cv('4x+2', {'x': 4}, 18); chk('(2(x+5)-10)/2', 'x')

# =====================================================================
S_.append(("Ecuaciones. Elementos y solución", [
 (1, r"Indica los miembros, los términos, la incógnita y el grado de cada ecuación: \quad a) $5x-3=2x+9$ \quad b) $4(a+1)=a-2$"
     + recorda(r"Los \textbf{miembros} son las expresiones de cada lado del signo $=$; los \textbf{términos}, cada sumando; la \textbf{incógnita}, la letra; y la \textbf{solución}, el valor que hace cierta la igualdad."),
     r"a) Miembros: $\res{5x-3}$ y $\res{2x+9}$; términos: $\res{5x,\ -3,\ 2x,\ 9}$; incógnita: $\res{x}$; grado \res{1}. \par b) Miembros: $\res{4(a+1)}$ y $\res{a-2}$; términos: $\res{4(a+1),\ a,\ -2}$; incógnita: $\res{a}$; grado \res{1}."),
 (1, r"Comprueba si el valor indicado es solución de la ecuación:" + tasks(2, [r'$3x-1=8$, \ $x=3$', r'$2x+5=x+1$, \ $x=-4$', r'$5-x=2x$, \ $x=2$', r'$\dfrac{x}{3}+1=x-3$, \ $x=6$']),
     tasks(2, [r'$3\cdot3-1=8$: \rest{sí}', r'$2\cdot(-4)+5=-3$ y $-4+1=-3$: \rest{sí}', r'$5-2=3$ y $2\cdot2=4$: \rest{no}', r'$\frac{6}{3}+1=3$ y $6-3=3$: \rest{sí}'])),
 (1, r"Halla mentalmente la solución:" + tasks(3, [E(e) for e in ['x+4=10', 'x-3=8', '5x=30', 'x/2=7', '12-x=5', '2x+1=11']]),
     tasks(3, [r'$x=\res{%s}$' % s for s in ['6', '11', '6', '14', '7', '5']])),
 (2, r"¿Cuál de los valores $-2$, $0$, $1$ o $3$ es la solución de cada ecuación?" + tasks(2, [E(e) for e in ['4x-3=2x+3', '2(x+1)=x', '7x=x', '3-x=2x']]),
     tasks(2, [r'$x=\res{3}$: \ $9=9$', r'$x=\res{-2}$: \ $-2=-2$', r'$x=\res{0}$: \ $0=0$', r'$x=\res{1}$: \ $2=2$'])),
 (2, r"Di si cada igualdad es una identidad o una ecuación:" + tasks(2, ['$2(x+1)=2x+2$', '$3x+1=3x+2$', '$x+x=2x$', '$4x-x=12$']),
     tasks(2, [r'\rest{Identidad} (al operar, $2x+2=2x+2$)', r'\rest{Ecuación} sin solución ($1\neq2$)', r'\rest{Identidad}', r'\rest{Ecuación}, con solución $x=4$'])),
 (3, r"Escribe una ecuación de primer grado: \ a) que tenga por solución $x=5$; \ b) que tenga por solución $x=-2$ y un paréntesis; \ c) que no tenga solución.",
     r"Por ejemplo: \ a) $\res{2x=10}$; \ b) $\res{3(x+4)=6}$; \ c) $\res{x+1=x+3}$. \ (Hay muchas respuestas correctas.)"),
]))
for e, s in [('x+4=10', 6), ('x-3=8', 11), ('5x=30', 6), ('x/2=7', 14), ('12-x=5', 7), ('2x+1=11', 5), ('4x-3=2x+3', 3), ('2(x+1)=x', -2), ('7x=x', 0), ('3-x=2x', 1),
             ('3x-1=8', 3), ('2x+5=x+1', -4), ('x/3+1=x-3', 6), ('4x-x=12', 4), ('2x=10', 5), ('3(x+4)=6', -2)]: ce(e, s)
ce('2(x+1)=2x+2', 'totes'); ce('x+x=2x', 'totes'); ce('3x+1=3x+2', 'cap'); ce('x+1=x+3', 'cap'); cv('5-x', {'x': 2}, 3); cv('2x', {'x': 2}, 4)

# =====================================================================
E1 = ['x+8=15', 'x-6=-2', 'x+9=4', '-5+x=-11']
E2 = ['6x=42', '-4x=20', '9x=-27', 'x/5=3', 'x/4=-3', '-x=8']
E3 = ['2x+3=11', '5x-4=21', '3x+10=1', '7-2x=13']
E4 = ['5x+2=3x+10', '8x-5=6x+1', '4x+7=x-8', '2x-9=5x+3']
E5 = ['3x+4-x=x+9', '6-2x+5=3x+1', 'x+2x+3x=4x+10', '9x-3-4x=2x+12']
E6 = ['4x=10', '6x+1=2x+3', '3x-2=5', '10x=-4']
E7 = ['2x+5-7x=3-x-6', '12-3x+x=4x-6', 'x+1=x+5', '3x+6-x=2x+6']
a1, b1 = eqs(E1, 4, 2); a2, b2 = eqs(E2, 3, 3); a3, b3 = eqs(E3, 4, 2); a4, b4 = eqs(E4, 2, 2); a5, b5 = eqs(E5, 2, 1); a6, b6 = eqs(E6, 4, 2); a7, b7 = eqs(E7, 2, 1)
S_.append(("Ecuaciones equivalentes. Resolución", [
 (1, r"Resuelve:" + a1 + recorda(r"Transposición: lo que \emph{suma} pasa \emph{restando} y lo que \emph{resta} pasa \emph{sumando}; lo que \emph{multiplica} pasa \emph{dividiendo} (con su signo) y lo que \emph{divide} pasa \emph{multiplicando}."), b1),
 (1, r"Resuelve:" + a2, b2),
 (1, r"Resuelve:" + a3, b3),
 (2, r"Resuelve y comprueba la solución:" + a4, b4),
 (2, r"Resuelve:" + a5, b5),
 (2, r"Resuelve (la solución puede ser una fracción: dala irreducible):" + a6, b6),
 (3, r"Resuelve. ¿Qué pasa en las dos últimas?" + a7, b7 + r"\par En c) llegamos a $0x=4$: ningún número multiplicado por 0 da 4. En d), los dos miembros son iguales: es una identidad."),
 (3, r"Escribe la ecuación que representa la balanza y halla cuánto pesa cada caja $x$ (las bolas pesan 1\,kg).\par\smallskip{\centering %s\par}" % balanca(3, 4, 1, 10),
     r"$\res{3x+4=x+10}$; \ " + sol1('3x+4=x+10') + r" \ Cada caja pesa \rest{3\,kg}."),
]))

# =====================================================================
P1 = ['3(x+2)=18', '5(x-1)=20', '2(x+7)=x+12', '-2(x-3)=10']
P2 = ['4(x-1)=2(x+3)', '3(2x+1)=5x+7', '6-(x+2)=x', '2x-(5-x)=10']
P3 = ['5(x+2)-3x=16', '7x-2(x+4)=12', '3(x-4)+2(x+1)=5', '4(2x-3)=5(x+3)']
P4 = ['2(3x-1)-3(x+2)=x+4', '5-2(x-3)=3(x-8)+5', '4(x+1)-3(x-2)=2(x+5)', '3(x-1)-(2x+5)=x-8']
P5 = ['x-2(x-5)=3(4-x)+6', '6(x+1)-4(2x-1)=0']
c1, d1 = eqs(P1, 2, 1); c2, d2 = eqs(P2, 2, 1); c3, d3 = eqs(P3, 2, 1); c4, d4 = eqs(P4, 1, 1); c5, d5 = eqs(P5, 1, 1)
S_.append(("Ecuaciones con paréntesis", [
 (1, r"Resuelve:" + c1 + recorda(r"Primero quitamos paréntesis (propiedad distributiva) y después resolvemos como siempre. Cuidado con el signo menos: $-2(x-3)=-2x+6$."), d1),
 (2, r"Resuelve:" + c2, d2),
 (2, r"Resuelve:" + c3, d3),
 (3, r"Resuelve. ¿Qué pasa en la última ecuación?" + c4, d4 + r"\par En d) los dos miembros quedan iguales: es una identidad y cualquier número es solución."),
 (3, r"Resuelve:" + c5, d5),
]))

# =====================================================================
Q1 = ['x/3=5', 'x/4+2=5', '2x/3=8', 'x/2-1=4']
Q2 = ['x/2+x/4=6', 'x/3-x/6=2', 'x/2+x/3=10', 'x-x/5=8']
Q3 = ['(x+3)/2=5', '(x-1)/3=x-5', '(2x+1)/5=3', 'x/2=(x+6)/5']
Q4 = ['x/2+3=x/3+5', '(x+1)/4=(x-1)/2']
Q5 = ['(x+2)/3-(x-1)/4=2', 'x-(x+2)/3=6', '(3x-1)/2-(x+5)/4=x/4']
Q6 = ['x/2+x/4+x/8=14', '2(x-1)/3=(x+4)/2']
e1, f1 = eqs(Q1, 4, 2); e2, f2 = eqs(Q2, 4, 1); e3, f3 = eqs(Q3, 4, 1); e4, f4 = eqs(Q4, 2, 1); e5, f5 = eqs(Q5, 3, 1); e6, f6 = eqs(Q6, 2, 1)
S_.append(("Ecuaciones con denominadores", [
 (1, r"Resuelve:" + e1 + recorda(r"Multiplicamos \emph{todos} los términos de los dos miembros por el m.c.m. de los denominadores (también los que no tienen denominador). Si un numerador tiene más de un término, lo ponemos entre paréntesis."), f1),
 (2, r"Resuelve:" + e2, f2),
 (2, r"Resuelve:" + e3, f3),
 (2, r"Resuelve:" + e4, f4),
 (3, r"Resuelve:" + e5, f5),
 (3, r"Resuelve:" + e6, f6),
]))

# =====================================================================
def pr(eq, txt):
    return '$' + tx(eq) + r'\ \Rightarrow\ ' + sol1(eq)[1:] + r'\par ' + txt
S_.append(("Resolución de problemas con ecuaciones", [
 (1, r"Si a un número le sumamos 12, obtenemos 30. ¿Cuál es el número?"
     + recorda(r"Pasos: 1) lee y entiende el enunciado; 2) elige la incógnita ($x=\ldots$); 3) plantea la ecuación; 4) resuélvela; 5) comprueba la solución y responde a la pregunta."),
     pr('x+12=30', r"El número es el \rest{18}.")),
 (1, r"El triple de un número menos 8 es 25. ¿Cuál es el número?", pr('3x-8=25', r"El número es el \rest{11}. ($33-8=25$)")),
 (1, r"La suma de dos números consecutivos es 73. ¿Cuáles son?", pr('x+(x+1)=73', r"Los números son el \rest{36 y el 37}.")),
 (2, r"La suma de tres números consecutivos es 159. ¿Cuáles son?", pr('x+(x+1)+(x+2)=159', r"Los números son \rest{52, 53 y 54}.")),
 (2, r"Laura tiene 6 años más que su hermano. Entre los dos suman 30 años. ¿Cuántos años tiene cada uno?", r"Hermano: $x$; Laura: $x+6$. \ " + pr('x+(x+6)=30', r"El hermano tiene \rest{12 años} y Laura, \rest{18 años}.")),
 (2, r"Un bolígrafo y una libreta cuestan juntos $4,50$\,€. La libreta cuesta el doble que el bolígrafo. ¿Cuánto cuesta cada cosa?", r"Trabajamos en céntimos ($4,50$\,€ $=450$ céntimos). Bolígrafo: $x$; libreta: $2x$. \ " + pr('x+2x=450', r"El bolígrafo cuesta \rest{150 céntimos $=1,50$\,€} y la libreta, \rest{3\,€}.")),
 (2, r"El perímetro de un rectángulo es 46\,cm y la base mide 5\,cm más que la altura. ¿Cuánto miden los lados?", r"Altura: $x$; base: $x+5$. \ " + pr('2x+2(x+5)=46', r"La altura mide \rest{9\,cm} y la base, \rest{14\,cm}.")),
 (2, r"Repartimos 90 cromos entre tres amigos. El segundo recibe el doble que el primero y el tercero, el triple que el primero. ¿Cuántos recibe cada uno?", r"Primero: $x$; segundo: $2x$; tercero: $3x$. \ " + pr('x+2x+3x=90', r"Reciben \rest{15, 30 y 45 cromos}.")),
 (3, r"Una madre tiene 42 años y su hijo, 10. ¿Dentro de cuántos años la madre tendrá el triple de edad que el hijo?", r"Dentro de $x$ años: madre $42+x$, hijo $10+x$. \ " + pr('42+x=3(10+x)', r"Dentro de \rest{6 años} (48 y 16 años).")),
 (3, r"La mitad de un número más su cuarta parte es 21. ¿Cuál es el número?", pr('x/2+x/4=21', r"El número es el \rest{28}.")),
 (3, r"En una clase hay 28 alumnos. Si hubiera 4 chicas más, habría tantas chicas como chicos. ¿Cuántas chicas y cuántos chicos hay?", r"Chicas: $x$; chicos: $28-x$. \ " + pr('x+4=28-x', r"Hay \rest{12 chicas y 16 chicos}.")),
 (3, r"En un aparcamiento hay coches y motos: en total, 30 vehículos y 96 ruedas. ¿Cuántos coches y cuántas motos hay?", r"Coches: $x$; motos: $30-x$. \ " + pr('4x+2(30-x)=96', r"Hay \rest{18 coches y 12 motos}.")),
 (3, r"Los ángulos de un triángulo miden $x$, $2x$ y $3x$. ¿Cuánto mide cada ángulo? (Recuerda que los tres ángulos de un triángulo suman $180^\circ$.)", pr('x+2x+3x=180', r"Los ángulos miden \rest{$30^\circ$, $60^\circ$ y $90^\circ$}.")),
]))
cv('x+6', {'x': 12}, 18); cv('2x', {'x': 150}, 300); cv('x+5', {'x': 9}, 14); cv('42+x', {'x': 6}, 48); cv('28-x', {'x': 12}, 16); cv('30-x', {'x': 18}, 12)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TIT = "Introducción al álgebra. Ecuaciones de primer grado"

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 6: %s' % (t, TIT), capcalera='%s · Unidad 6' % t,
                 pdfkeywords='lenguaje algebraico, expresiones algebraicas, valor numérico, monomios, polinomios, propiedad distributiva, ecuaciones de primer grado, paréntesis, denominadores, problemas',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 6' if sol else 'Ficha de ejercicios · Unidad 6') + '}{' + TIT.replace('. ', r'.\\ ') + '}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás herramientas que resuelven paso a paso cualquier ecuación de primer grado. Las soluciones fraccionarias se dan en forma irreducible."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y comprueba las soluciones de las ecuaciones. Haz los cálculos sin calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't6-fitxa-solucions-es.tex' if sol else 't6-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios,', NCHK[0], 'comprobaciones')
