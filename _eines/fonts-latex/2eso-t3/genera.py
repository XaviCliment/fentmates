# Genera t3-fitxa-exercicis.tex i t3-fitxa-solucions.tex (2n ESO, Unitat 3: Introducció a l'àlgebra. Polinomis)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 8 seccions segueixen els apartats dels apunts (3.1-3.8).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Les expressions s'escriuen en text («(2x-3)(x^2+4x-1)», «(-2x^3y)^4:(4x^5)») i sympy en calcula el resultat (pt) o
# comprova els resultats escrits a mà (chk); així no hi pot haver errades de càlcul.
# Ús: python3 genera.py && pdflatex t3-fitxa-exercicis.tex (dues vegades) && pdflatex t3-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re
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
x, y, z, a, b, n = sp.symbols('x y z a b n')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
LOC = {'x': x, 'y': y, 'z': z, 'a': a, 'b': b, 'n': n}
CHK = []
def S(s): return parse_expr(s.replace(':', '/'), transformations=TR, local_dict=LOC) if isinstance(s, str) else sp.sympify(s)
def chk(l, r):
    CHK.append((l, r)); assert sp.expand(S(l) - S(r)) == 0, (l, r, sp.expand(S(l)))
def ntex(c):
    c = sp.Rational(c)
    return str(c.p) if c.q == 1 else ('-' if c < 0 else '') + r'\tfrac{%d}{%d}' % (abs(c.p), c.q)
def pt(e):
    """polinomi en TeX, de grau més alt a més baix"""
    e = sp.expand(S(e))
    if e == 0: return '0'
    gens = sorted(e.free_symbols, key=str)
    if not gens: return ntex(e)
    out = ''
    for mon, c in sp.Poly(e, *gens).terms(order='grlex'):
        lit = ''.join(str(g) if k == 1 else '%s^{%d}' % (g, k) for g, k in zip(gens, mon) if k)
        q = abs(sp.Rational(c))
        out += ('-' if c < 0 else ('+' if out else '')) + (ntex(q) if q != 1 or not lit else '') + lit
    return out
def tx(s):
    """expressió escrita en text -> TeX (sense calcular)"""
    s = re.sub(r'\^(\d+)', r'^{\1}', s)
    s = re.sub(r'(?<![\w)])(\d+)/(\d+)', r'\\tfrac{\1}{\2}', s)
    return s.replace('*', r'\cdot ')
def ex(s, r=None):
    """enunciat i solució d'una expressió que es desenvolupa i es redueix"""
    if r is not None: chk(s, r)
    return '$%s$' % tx(s), r'$%s=\res{%s}$' % (tx(s), pt(s if r is None else r))
def ops(lst, ncol, scol=None, gap='6pt'):
    q, s = zip(*[ex(*e) if isinstance(e, tuple) else ex(e) for e in lst])
    return tasks(ncol, q, gap), tasks(scol or min(ncol, 2), s, gap)
def val(e, **v):
    return S(e).subs({LOC[k]: sp.Rational(w) for k, w in v.items()})
def fc(lst, ncol, scol=None):
    """factor comú: [(polinomi, factoritzat)]"""
    for p, f in lst: chk(f, p)
    return tasks(ncol, ['$%s$' % tx(p) for p, _ in lst], '6pt'), tasks(scol or min(ncol, 2), [r'$%s=\res{%s}$' % (tx(p), tx(f)) for p, f in lst], '6pt')

S_ = []
def sec(title): S_.append((title, [])); return S_[-1][1]

# =====================================================================
# 1. L'àlgebra: el llenguatge algebraic
X = sec(T("L'àlgebra: el llenguatge algebraic", 'El álgebra: el lenguaje algebraico'))
LG = [(T("El triple d'un nombre", 'El triple de un número'), '3x'), (T("Un nombre menys 8", 'Un número menos 8'), 'x-8'),
      (T("La meitat d'un nombre", 'La mitad de un número'), r'\tfrac{x}{2}'), (T("El quadrat d'un nombre més 1", 'El cuadrado de un número más 1'), 'x^2+1'),
      (T("El doble d'un nombre menys 5", 'El doble de un número menos 5'), '2x-5'), (T("El doble de la diferència d'un nombre i 5", 'El doble de la diferencia de un número y 5'), '2(x-5)'),
      (T("El següent d'un nombre", 'El siguiente de un número'), 'x+1'), (T("La suma d'un nombre i el seu quadrat", 'La suma de un número y su cuadrado'), 'x+x^2'),
      (T("El cub d'un nombre", 'El cubo de un número'), 'x^3'), (T("La quarta part d'un nombre menys 3", 'La cuarta parte de un número menos 3'), r'\tfrac{x}{4}-3')]
X.append((1, T("Escriu en llenguatge algebraic (fes servir $x$ per al nombre):", "Escribe en lenguaje algebraico (usa $x$ para el número):") + tasks(2, [t + '.' for t, _ in LG], '3pt')
    + recorda(T(r"l'ordre de les paraules importa: «el doble d'un nombre menys 5» és $2x-5$, però «el doble de la diferència d'un nombre i 5» és $2(x-5)$.", r"el orden de las palabras importa: «el doble de un número menos 5» es $2x-5$, pero «el doble de la diferencia de un número y 5» es $2(x-5)$.")),
    tasks(5, [r'$\res{%s}$' % e for _, e in LG], '4pt')))
X.append((1, T("Escriu amb paraules què expressa cada expressió algebraica:", "Escribe con palabras qué expresa cada expresión algebraica:") + tasks(4, ['$x+5$', '$4x$', '$x^2-3$', r'$\dfrac{x}{3}$', '$2x+1$', '$(x+2)^2$', '$x-y$', '$10-x$']),
    tasks(2, [T("Un nombre més 5.", "Un número más 5."), T("El quàdruple d'un nombre.", "El cuádruple de un número."), T("El quadrat d'un nombre menys 3.", "El cuadrado de un número menos 3."), T("La tercera part d'un nombre.", "La tercera parte de un número."),
              T("Un nombre senar (o el doble d'un nombre més 1).", "Un número impar (o el doble de un número más 1)."), T("El quadrat de la suma d'un nombre i 2.", "El cuadrado de la suma de un número y 2."),
              T("La diferència de dos nombres.", "La diferencia de dos números."), T("El que li falta a un nombre per a arribar a 10.", "Lo que le falta a un número para llegar a 10.")])))
X.append((1, T(r"Escriu l'expressió algebraica de: a) el perímetre d'un quadrat de costat $x$; b) l'àrea d'un rectangle de base $x$ i altura $5$; c) l'edat d'una persona d'ací a 7 anys si ara en té $x$; d) el preu de $x$ quilos de pomes a $1{,}80$ € el quilo.",
               r"Escribe la expresión algebraica de: a) el perímetro de un cuadrado de lado $x$; b) el área de un rectángulo de base $x$ y altura $5$; c) la edad de una persona dentro de 7 años si ahora tiene $x$; d) el precio de $x$ kilos de manzanas a $1{,}80$ € el kilo."),
    r"a) $\res{4x}$ \qquad b) $\res{5x}$ \qquad c) $\res{x+7}$ \qquad d) $\res{1{,}8x}$"))
VN = [('3x+5', 2), ('7-2x', -3), ('x^2-4x', 5), ('2x^2+x-1', -2), ('-x^2+6', -3), ('x^3-x', -2)]
X.append((1, T("Calcula el valor numèric de cada expressió per al valor de $x$ indicat:", "Calcula el valor numérico de cada expresión para el valor de $x$ indicado:")
    + tasks(3, [r'$%s$ \ per a $x=%d$' % (tx(e), v) if not ES else r'$%s$ \ para $x=%d$' % (tx(e), v) for e, v in VN], '5pt')
    + recorda(T(r"els nombres negatius se substitueixen entre parèntesis: si $x=-3$, \ $x^2=(-3)^2=9$ però $-x^2=-(-3)^2=-9$.", r"los números negativos se sustituyen entre paréntesis: si $x=-3$, \ $x^2=(-3)^2=9$ pero $-x^2=-(-3)^2=-9$.")),
    tasks(3, [r'$\res{%s}$' % val(e, x=v) for e, v in VN], '4pt')))
assert [val(e, x=v) for e, v in VN] == [11, 13, 5, 5, -3, -6]
VN2 = [('2a+3b', dict(a=4, b=-1)), ('a^2-b^2', dict(a=-3, b=2)), ('5xy-x', dict(x=2, y=-1)), ('x^2y+xy^2', dict(x=-1, y=3))]
def vtx(d): return ',\\ '.join('%s=%s' % kv for kv in d.items())
X.append((2, T("Calcula el valor numèric:", "Calcula el valor numérico:") + tasks(2, [r'$%s$ \ %s $%s$' % (tx(e), T('per a', 'para'), vtx(d)) for e, d in VN2], '5pt'),
    tasks(2, [r'$%s$: \ $\res{%s}$' % (tx(e), val(e, **d)) for e, d in VN2], '4pt')))
assert [val(e, **d) for e, d in VN2] == [5, 5, -12, -6]
X.append((2, T(r"Una companyia de telefonia cobra una quota de 9 € al mes més $0{,}05$ € per cada minut de trucada. Escriu l'expressió del que paguem en un mes si parlem $x$ minuts i calcula quant paguem si parlem 120 minuts. I si parlem 3 hores?",
               r"Una compañía de telefonía cobra una cuota de 9 € al mes más $0{,}05$ € por cada minuto de llamada. Escribe la expresión de lo que pagamos en un mes si hablamos $x$ minutos y calcula cuánto pagamos si hablamos 120 minutos. ¿Y si hablamos 3 horas?"),
    r"$\res{0{,}05x+9}$; \quad $x=120$: $0{,}05\cdot120+9=\res{15\text{ €}}$; \quad $x=180$: $0{,}05\cdot180+9=\res{18\text{ €}}$"))
chk('0.05*120+9', 15); chk('0.05*180+9', 18)
X.append((2, T(r"Amb escuradents formem una filera de triangles: la figura 1 té 3 escuradents, la 2 en té 5, la 3 en té 7… Quants en té la figura 10? Escriu una expressió per als escuradents de la figura $n$. Quina figura té 51 escuradents?",
               r"Con palillos formamos una hilera de triángulos: la figura 1 tiene 3 palillos, la 2 tiene 5, la 3 tiene 7… ¿Cuántos tiene la figura 10? Escribe una expresión para los palillos de la figura $n$. ¿Qué figura tiene 51 palillos?"),
    T(r"Cada figura en suma 2: la figura $n$ en té $3+2(n-1)=\res{2n+1}$. \ Figura 10: $\res{21}$. \ $2n+1=51$ per a $n=\res{25}$.", r"Cada figura suma 2: la figura $n$ tiene $3+2(n-1)=\res{2n+1}$. \ Figura 10: $\res{21}$. \ $2n+1=51$ para $n=\res{25}$.")))
chk('3+2(n-1)', '2n+1'); assert val('2n+1', n=10) == 21 and val('2n+1', n=25) == 51
X.append((3, T(r"Escriu tres nombres consecutius qualssevol fent servir $x$ i demostra que la seua suma sempre és múltiple de 3. És cert també per a la suma de quatre nombres consecutius?",
               r"Escribe tres números consecutivos cualesquiera usando $x$ y demuestra que su suma siempre es múltiplo de 3. ¿Es cierto también para la suma de cuatro números consecutivos?"),
    T(r"$x+(x+1)+(x+2)=3x+3=\res{3(x+1)}$, \ que és múltiple de 3 per a qualsevol $x$. \ Amb quatre: $x+(x+1)+(x+2)+(x+3)=4x+6$, que \rest{no sempre} és múltiple de 4 (ni de 3): per a $x=1$, $1+2+3+4=10$.",
      r"$x+(x+1)+(x+2)=3x+3=\res{3(x+1)}$, \ que es múltiplo de 3 para cualquier $x$. \ Con cuatro: $x+(x+1)+(x+2)+(x+3)=4x+6$, que \rest{no siempre} es múltiplo de 4 (ni de 3): para $x=1$, $1+2+3+4=10$.")))
chk('x+(x+1)+(x+2)', '3(x+1)'); chk('x+(x+1)+(x+2)+(x+3)', '4x+6')

# =====================================================================
# 2. Monomis: parts i valor numèric
X = sec(T('Monomis: parts i valor numèric', 'Monomios: partes y valor numérico'))
MP = [('-7x^3', '-7', 'x^3', 3), ('xy^2', '1', 'xy^2', 3), (r'\tfrac{2}{3}a^2b', r'\tfrac{2}{3}', 'a^2b', 3), ('-x', '-1', 'x', 1), ('5x^2y^3z', '5', 'x^2y^3z', 6), ('12', '12', T('no en té', 'no tiene'), 0)]
for m, c, l, g in MP:
    e = sp.sympify(S(m.replace(r'\tfrac{2}{3}', '(2/3)')))
    assert sp.Poly(e, *sorted(e.free_symbols, key=str)).total_degree() == g if e.free_symbols else g == 0
HD = T(r'Monomi & Coeficient & Part literal & Grau', r'Monomio & Coeficiente & Parte literal & Grado')
def mtab(sol):
    rows = r'\\\hline '.join(('$%s$ & $\\res{%s}$ & %s & $\\res{%d}$' % (m, c, ('$\\res{%s}$' % l) if '$' not in l and l[0] not in 'nN' else '\\rest{%s}' % l, g)) if sol else '$%s$ & & & ' % m for m, c, l, g in MP)
    return r'\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.6cm}|C{2.6cm}|C{1.6cm}|}\hline ' + HD + r'\\\hline ' + rows + r'\\\hline\end{tabular}\par}'
X.append((1, T("Completa la taula:", "Completa la tabla:") + mtab(False)
    + recorda(T(r"el grau d'un monomi és la \textbf{suma} dels exponents de totes les lletres; si no veus el coeficient, és 1 (o $-1$).", r"el grado de un monomio es la \textbf{suma} de los exponentes de todas las letras; si no ves el coeficiente, es 1 (o $-1$).")),
    mtab(True)))
NM = [('3x^4', True), (r'\dfrac{5}{x}', False), ('x+y', False), (r'-\dfrac{x^2}{4}', True), (r'\sqrt{x}', False), ('-2ab^3', True), ('x^{-1}', False), ('9', True)]
X.append((1, T("Quines d'aquestes expressions són monomis? Explica per què les altres no ho són.", "¿Cuáles de estas expresiones son monomios? Explica por qué las otras no lo son.") + tasks(4, ['$%s$' % e for e, _ in NM]),
    T(r"Són monomis: $\res{3x^4}$, $\res{-\dfrac{x^2}{4}}$, $\res{-2ab^3}$ i $\res{9}$. \ No ho són $\dfrac{5}{x}$ (lletra al denominador), $x+y$ (dos termes), $\sqrt{x}$ i $x^{-1}$ (exponents no naturals).",
      r"Son monomios: $\res{3x^4}$, $\res{-\dfrac{x^2}{4}}$, $\res{-2ab^3}$ y $\res{9}$. \ No lo son $\dfrac{5}{x}$ (letra en el denominador), $x+y$ (dos términos), $\sqrt{x}$ y $x^{-1}$ (exponentes no naturales).")))
X.append((1, T(r"Agrupa els monomis semblants: \ $4x^2,\ \ -3xy,\ \ 2x,\ \ -x^2,\ \ \tfrac{1}{2}xy,\ \ 7x,\ \ 5x^2y,\ \ -x,\ \ \tfrac{3}{4}x^2,\ \ x^2y$.", r"Agrupa los monomios semejantes: \ $4x^2,\ \ -3xy,\ \ 2x,\ \ -x^2,\ \ \tfrac{1}{2}xy,\ \ 7x,\ \ 5x^2y,\ \ -x,\ \ \tfrac{3}{4}x^2,\ \ x^2y$."),
    r"$\res{\{4x^2,\ -x^2,\ \tfrac{3}{4}x^2\}}$ \quad $\res{\{-3xy,\ \tfrac{1}{2}xy\}}$ \quad $\res{\{2x,\ 7x,\ -x\}}$ \quad $\res{\{5x^2y,\ x^2y\}}$"))
VM = [('-3x^2', dict(x=4)), ('2x^3', dict(x=-2)), ('-a^2b', dict(a=-3, b=2)), ('4xy^2', dict(x='1/2', y=-3))]
X.append((2, T("Calcula el valor numèric de cada monomi:", "Calcula el valor numérico de cada monomio:") + tasks(2, [r'$%s$ \ %s $%s$' % (tx(e), T('per a', 'para'), vtx({k: tx(str(v)) for k, v in d.items()})) for e, d in VM], '5pt'),
    tasks(2, [r'$\res{%s}$' % ntex(val(e, **d)) for e, d in VM], '4pt')))
assert [val(e, **d) for e, d in VM] == [-48, -16, -18, 18]
X.append((2, T("Escriu un monomi:", "Escribe un monomio:") + tasks(1, [T(r"semblant a $-6x^2y$ amb coeficient positiu;", r"semejante a $-6x^2y$ con coeficiente positivo;"), T(r"de grau 5 amb dues lletres i coeficient $-\tfrac{1}{2}$;", r"de grado 5 con dos letras y coeficiente $-\tfrac{1}{2}$;"), T(r"oposat a $3ab^2$;", r"opuesto a $3ab^2$;"), T("de grau 0.", "de grado 0.")], '3pt'),
    T("Per exemple:", "Por ejemplo:") + tasks(1, [r"$\res{4x^2y}$", r"$\res{-\tfrac{1}{2}x^3y^2}$", T(r"$\res{-3ab^2}$ (només n'hi ha un)", r"$\res{-3ab^2}$ (solo hay uno)"), T(r"$\res{7}$ (qualsevol nombre)", r"$\res{7}$ (cualquier número)")], '3pt')))
X.append((3, T(r"Troba $m$ i $n$ perquè els monomis $5x^{m}y^{3}$ i $-2x^{4}y^{n+1}$ siguen semblants. Quin grau tenen?", r"Halla $m$ y $n$ para que los monomios $5x^{m}y^{3}$ y $-2x^{4}y^{n+1}$ sean semejantes. ¿Qué grado tienen?"),
    T(r"Han de tindre la mateixa part literal: $m=4$ i $n+1=3$. \ $\res{m=4}$, $\res{n=2}$; \ grau $4+3=\res{7}$.", r"Deben tener la misma parte literal: $m=4$ y $n+1=3$. \ $\res{m=4}$, $\res{n=2}$; \ grado $4+3=\res{7}$.")))
X.append((3, T(r"Escriu un monomi de grau 4, en les lletres $x$ i $y$, amb coeficient 2, que valga 54 per a $x=3$, $y=1$.", r"Escribe un monomio de grado 4, en las letras $x$ e $y$, con coeficiente 2, que valga 54 para $x=3$, $y=1$."),
    T(r"És $2x^my^k$ amb $m+k=4$. Com que $y=1$: $2\cdot3^m=54$, \ $3^m=27$, \ $m=3$ i $k=1$: \ $\res{2x^3y}$.", r"Es $2x^my^k$ con $m+k=4$. Como $y=1$: $2\cdot3^m=54$, \ $3^m=27$, \ $m=3$ y $k=1$: \ $\res{2x^3y}$.")))
assert val('2x^3y', x=3, y=1) == 54

# =====================================================================
# 3. Operacions amb monomis
X = sec(T('Operacions amb monomis', 'Operaciones con monomios'))
R1 = [('5x+3x-2x', '6x'), ('4x^2-9x^2', '-5x^2'), ('-a+6a-8a', '-3a'), ('3xy-xy+5xy', '7xy'), ('x^3+x^3+x^3', '3x^3'), ('7ab^2-7ab^2', '0')]
q, s = ops(R1, 3, 3)
X.append((1, T("Redueix:", "Reduce:") + q + recorda(T(r"només se sumen i resten monomis \textbf{semblants}: sumem els coeficients i \textbf{deixem la mateixa part literal} ($5x^2+3x^2=8x^2$, mai $8x^4$).", r"solo se suman y restan monomios \textbf{semejantes}: sumamos los coeficientes y \textbf{dejamos la misma parte literal} ($5x^2+3x^2=8x^2$, nunca $8x^4$).")), s))
R2S = [('3x^2+5x', None), ('4x-x^2+2x', '-x^2+6x'), ('6ab-2a+ab', '7ab-2a'), ('2x^3-x^2+4x^3-x', '6x^3-x^2-x')]
for e, r in R2S:
    if r: chk(e, r)
X.append((1, T("Redueix quan siga possible. Si no es pot, explica per què:", "Reduce cuando sea posible. Si no se puede, explica por qué:") + tasks(4, ['$%s$' % tx(e) for e, _ in R2S]),
    tasks(2, [r'$%s=\res{%s}$' % (tx(e), tx(r)) if r else r'$%s$: \rest{%s}' % (tx(e), T('no es pot: no són semblants', 'no se puede: no son semejantes')) for e, r in R2S], '4pt')))
P1 = [('3x^2*5x^4', '15x^6'), ('(-2a)*(7a^3)', '-14a^4'), ('(-4xy)*(-3x^2y)', '12x^3y^2'), ('6x^2*(1/3)x', '2x^3'), ('x^3y*(-xy^4)', '-x^4y^5'), ('2a*3b*(-a^2)', '-6a^3b')]
q, s = ops(P1, 3, 3)
X.append((1, T("Multiplica:", "Multiplica:") + q + recorda(T(r"multipliquem els coeficients i \textbf{sumem} els exponents de cada lletra: $x^m\cdot x^n=x^{m+n}$.", r"multiplicamos los coeficientes y \textbf{sumamos} los exponentes de cada letra: $x^m\cdot x^n=x^{m+n}$.")), s))
D1 = [('12x^5:(4x^2)', '3x^3'), ('(-20a^4):(5a)', '-4a^3'), ('18x^3y^2:(-6xy)', '-3x^2y'), ('(-9x^6):(-9x^6)', '1'), ('7x^4y:(14x^2)', 'x^2y/2'), ('(-15a^3b^4):(3ab^4)', '-5a^2')]
q, s = ops(D1, 3, 3)
X.append((1, T("Divideix:", "Divide:") + q + recorda(T(r"dividim els coeficients i \textbf{restem} els exponents: $x^m:x^n=x^{m-n}$; i $x^0=1$.", r"dividimos los coeficientes y \textbf{restamos} los exponentes: $x^m:x^n=x^{m-n}$; y $x^0=1$.")), s))
W1 = [('(2x^3)^2', '4x^6'), ('(-3a^2)^3', '-27a^6'), ('(x^2y^3)^4', 'x^8y^12'), ('(-2xy^2)^4', '16x^4y^8'), ('(-a^3b)^5', '-a^15b^5'), ('(1/2x^2)^3', 'x^6/8')]
q, s = ops(W1, 3, 3)
X.append((2, T("Calcula les potències:", "Calcula las potencias:") + q + recorda(T(r"elevem el coeficient i \textbf{multipliquem} els exponents: $(-2x^3y)^2=(-2)^2x^{6}y^{2}=4x^6y^2$. Compte amb el signe si l'exponent és senar.", r"elevamos el coeficiente y \textbf{multiplicamos} los exponentes: $(-2x^3y)^2=(-2)^2x^{6}y^{2}=4x^6y^2$. Cuidado con el signo si el exponente es impar.")), s))
R3 = ['5x^2-3x+2-x^2+7x-6', '-2a+4b-a-3b+5a', 'x^3-2x+x^2-4x^3+3x+x^2', '3xy-x^2+2xy+4x^2-y']
q, s = ops(R3, 2, 1)
X.append((2, T("Redueix agrupant els termes semblants:", "Reduce agrupando los términos semejantes:") + q, s))
QD = [('8x^4:(2x)', True), ('6x^2:(3x^5)', False), ('10a^3b:(5ab)', True), ('4xy:(2y^2)', False)]
X.append((2, T(r"Quins d'aquests quocients són monomis? Calcula'ls.", r"¿Cuáles de estos cocientes son monomios? Calcúlalos.") + tasks(4, ['$%s$' % tx(e) for e, _ in QD]),
    tasks(2, [(r'$%s=\res{%s}$' % (tx(e), pt(e))) if ok else (r'$%s=%s$: \rest{%s}' % (tx(e), sp.latex(sp.simplify(S(e))).replace('\\frac', '\\dfrac'), T('no és monomi', 'no es monomio'))) for e, ok in QD], '4pt')))
chk('8x^4/(2x)', '4x^3'); chk('10a^3b/(5a*b)', '2a^2')
C1 = [('3x*4x^2-5x^3', '7x^3'), ('2a^2*(-3a)+10a^4:(2a)', '-a^3'), ('(2x)^3-x*6x^2', '2x^3'), ('15x^4:(3x^2)-(2x)^2', 'x^2'), ('-x^2*x^3+(x^2)^2*3x', '2x^5'), ('(-3x)^2*x-4x^3', '5x^3')]
q, s = ops(C1, 2, 2)
X.append((2, T("Opera i redueix (respecta la jerarquia de les operacions):", "Opera y reduce (respeta la jerarquía de las operaciones):") + q, s))
C2 = [('(-2x^2y)^3:(4x^4y^2)', '-2x^2y'), ('(3a^2b)^2*(-ab)^3:(9a^5b^4)', '-a^2b'), ('(-x^2)^3+2x^4*(-x)^2-(2x^3)^2:4', '0'), ('(2x)^4:(-x)^2-3x*(-2x)', '22x^2')]
q, s = ops(C2, 2, 1)
X.append((3, T("Opera i redueix:", "Opera y reduce:") + q, s))
X.append((3, T(r"Un ortoedre té les arestes $2x$, $3x$ i $x^2$ cm. Escriu com a monomis o polinomis:", r"Un ortoedro tiene las aristas $2x$, $3x$ y $x^2$ cm. Escribe como monomios o polinomios:")
    + tasks(1, [T("el volum;", "el volumen;"), T("l'àrea total.", "el área total."), T("Què li passa al volum si totes les arestes es fan el doble de llargues?", "¿Qué le pasa al volumen si todas las aristas se hacen el doble de largas?")], '3pt'),
    tasks(1, [r"$V=2x\cdot3x\cdot x^2=\res{6x^4}$ cm$^3$", T(r"$A=2(6x^2+2x^3+3x^3)=\res{10x^3+12x^2}$ cm$^2$ (no són semblants: queda un binomi)", r"$A=2(6x^2+2x^3+3x^3)=\res{10x^3+12x^2}$ cm$^2$ (no son semejantes: queda un binomio)"),
              T(r"$4x\cdot6x\cdot2x^2=48x^4=8\cdot6x^4$: es fa \rest{8 vegades més gran}.", r"$4x\cdot6x\cdot2x^2=48x^4=8\cdot6x^4$: se hace \rest{8 veces mayor}.")], '4pt')))
chk('2x*3x*x^2', '6x^4'); chk('2*(2x*3x+2x*x^2+3x*x^2)', '10x^3+12x^2'); chk('4x*6x*2x^2', '8*6x^4')

# =====================================================================
# 4. Polinomis: parts
X = sec(T('Polinomis: parts', 'Polinomios: partes'))
PP = ['3x^2-5x+1', '7-2x^4+x', 'x^3-8', '-x^5+4x^3-x^2+2x', '6x', '4x^2-x+3x^3-2']
def pinfo(p):
    e = sp.Poly(S(p), x); cs = e.all_coeffs(); g = e.degree()
    return pt(p), g, ntex(cs[0]), ntex(cs[-1]), len(e.terms()), all(c != 0 for c in cs)
HP = T(r'Polinomi & Ordenat & Grau & Coef. principal & Terme indep. & Termes', r'Polinomio & Ordenado & Grado & Coef. principal & Término indep. & Términos')
def ptab(sol):
    rows = r'\\\hline '.join(('$%s$ & $\\res{%s}$ & $\\res{%d}$ & $\\res{%s}$ & $\\res{%s}$ & $\\res{%d}$' % ((tx(p),) + pinfo(p)[:5])) if sol else '$%s$ & & & & & ' % tx(p) for p in PP)
    return r'\par\smallskip{\centering\renewcommand{\arraystretch}{1.4}\small\begin{tabular}{|c|C{3.8cm}|C{1cm}|C{1.7cm}|C{1.7cm}|C{1.5cm}|}\hline ' + HP + r'\\\hline ' + rows + r'\\\hline\end{tabular}\par}'
X.append((1, T("Completa la taula:", "Completa la tabla:") + ptab(False)
    + recorda(T(r"el \textbf{grau} d'un polinomi és el grau més alt dels seus termes; el \textbf{coeficient principal}, el del terme de grau més alt; el \textbf{terme independent}, el que no té lletra (amb el seu signe).", r"el \textbf{grado} de un polinomio es el grado más alto de sus términos; el \textbf{coeficiente principal}, el del término de mayor grado; el \textbf{término independiente}, el que no tiene letra (con su signo).")),
    ptab(True)))
assert [pinfo(p)[1] for p in PP] == [2, 4, 3, 5, 1, 3]
RD = ['2x^2+3x-x^2+5-x', 'x^3-4x+2x^3+x^2-3x^3+4x', '5-x+3x^2-7+x-x^2', '-x^4+2x+x^4-3x^2+x^3']
q, s = ops(RD, 2, 2)
X.append((1, T("Redueix i ordena aquests polinomis. Quin grau té cada un?", "Reduce y ordena estos polinomios. ¿Qué grado tiene cada uno?") + q,
    tasks(2, [r'$\res{%s}$, \ %s $\res{%d}$' % (pt(e), T('grau', 'grado'), sp.Poly(S(e), x).degree()) for e in RD], '4pt')))
CM = [('x^3+2x^2-x+5', True), ('4x^2-1', False), ('x^4-x^3+x^2-x+1', True), ('2x^3+x', False)]
X.append((1, T("Quins d'aquests polinomis són complets? Escriu els que no ho són posant zeros als termes que falten.", "¿Cuáles de estos polinomios son completos? Escribe los que no lo son poniendo ceros en los términos que faltan.") + tasks(2, ['$%s$' % tx(p) for p, _ in CM]),
    T(r"Són complets el primer i el tercer.\par $4x^2-1=\res{4x^2+0x-1}$; \ $2x^3+x=\res{2x^3+0x^2+x+0}$.", r"Son completos el primero y el tercero.\par $4x^2-1=\res{4x^2+0x-1}$; \ $2x^3+x=\res{2x^3+0x^2+x+0}$.")))
assert [pinfo(p)[5] for p, _ in CM] == [c for _, c in CM]
VP = [('x^2-3x+2', [0, 1, -1, 2]), ('2x^3-x^2+4', [0, 1, -2, '1/2'])]
X.append((2, T(r"Calcula el valor numèric de $P(x)=x^2-3x+2$ i de $Q(x)=2x^3-x^2+4$ per als valors indicats:", r"Calcula el valor numérico de $P(x)=x^2-3x+2$ y de $Q(x)=2x^3-x^2+4$ para los valores indicados:")
    + tasks(4, ['$P(0)$', '$P(1)$', '$P(-1)$', '$P(2)$', '$Q(0)$', '$Q(1)$', '$Q(-2)$', r'$Q\!\left(\tfrac{1}{2}\right)$'], '5pt'),
    tasks(4, [r'$%s(%s)=\res{%s}$' % (nm, tx(str(v)), ntex(val(p, x=v))) for nm, (p, vs) in zip('PQ', VP) for v in vs], '4pt')))
assert [val('x^2-3x+2', x=v) for v in [0, 1, -1, 2]] == [2, 0, 6, 0] and val('2x^3-x^2+4', x=-2) == -16
X.append((2, T("Escriu un polinomi que complisca cada condició:", "Escribe un polinomio que cumpla cada condición:")
    + tasks(1, [T("de grau 3 i amb tres termes;", "de grado 3 y con tres términos;"), T(r"de grau 2, complet i amb terme independent $-4$;", r"de grado 2, completo y con término independiente $-4$;"), T(r"de grau 4, amb coeficient principal $-2$ i sense terme independent.", r"de grado 4, con coeficiente principal $-2$ y sin término independiente.")], '3pt'),
    T("Per exemple (hi ha moltes respostes):", "Por ejemplo (hay muchas respuestas):") + tasks(1, [r"$\res{x^3-2x+5}$", r"$\res{3x^2+x-4}$", r"$\res{-2x^4+x^2+3x}$"], '3pt')))
X.append((3, T(r"a) Troba $k$ perquè $P(x)=x^3-2x^2+kx+6$ complisca $P(2)=0$. \ b) Troba $a$ si $Q(x)=ax^2+3x-1$ i $Q(2)=13$.", r"a) Halla $k$ para que $P(x)=x^3-2x^2+kx+6$ cumpla $P(2)=0$. \ b) Halla $a$ si $Q(x)=ax^2+3x-1$ y $Q(2)=13$."),
    T(r"a) $P(2)=8-8+2k+6=2k+6=0$, \ $\res{k=-3}$. \quad b) $Q(2)=4a+6-1=4a+5=13$, \ $4a=8$, \ $\res{a=2}$.", r"a) $P(2)=8-8+2k+6=2k+6=0$, \ $\res{k=-3}$. \quad b) $Q(2)=4a+6-1=4a+5=13$, \ $4a=8$, \ $\res{a=2}$.")))
assert val('x^3-2x^2-3x+6', x=2) == 0 and val('2x^2+3x-1', x=2) == 13
X.append((3, T(r"Un polinomi de grau 2 té el terme independent igual a 5, el coeficient de $x$ igual a $-4$ i compleix $P(1)=3$. Quin és? Quant val $P(-1)$?", r"Un polinomio de grado 2 tiene el término independiente igual a 5, el coeficiente de $x$ igual a $-4$ y cumple $P(1)=3$. ¿Cuál es? ¿Cuánto vale $P(-1)$?"),
    T(r"$P(x)=ax^2-4x+5$ i $P(1)=a-4+5=a+1=3$, \ $a=2$: \ $\res{P(x)=2x^2-4x+5}$; \ $P(-1)=2+4+5=\res{11}$.", r"$P(x)=ax^2-4x+5$ y $P(1)=a-4+5=a+1=3$, \ $a=2$: \ $\res{P(x)=2x^2-4x+5}$; \ $P(-1)=2+4+5=\res{11}$.")))
assert val('2x^2-4x+5', x=1) == 3 and val('2x^2-4x+5', x=-1) == 11

# =====================================================================
# 5. Suma i resta de polinomis
X = sec(T('Suma i resta de polinomis', 'Suma y resta de polinomios'))
PQR = r"$P(x)=3x^2-5x+2$, \ \ $Q(x)=x^3-2x^2+4x-1$ \ \ i \ \ $R(x)=-x^2+x-6$" if not ES else r"$P(x)=3x^2-5x+2$, \ \ $Q(x)=x^3-2x^2+4x-1$ \ \ y \ \ $R(x)=-x^2+x-6$"
P_, Q_, R_ = '(3x^2-5x+2)', '(x^3-2x^2+4x-1)', '(-x^2+x-6)'
def pqr(e): return e.replace('P', P_).replace('Q', Q_).replace('R', R_)
L1 = ['P+Q', 'P+R', 'Q+R', 'P+Q+R']
X.append((1, T("Donats ", "Dados ") + PQR + T(", calcula:", ", calcula:") + tasks(4, ['$%s$' % e for e in L1]),
    tasks(2, [r'$%s=\res{%s}$' % (e, pt(pqr(e))) for e in L1], '4pt')))
L2 = ['P-Q', 'Q-P', 'P-R', 'R-Q']
X.append((1, T("Amb els mateixos polinomis, calcula:", "Con los mismos polinomios, calcula:") + tasks(4, ['$%s$' % e for e in L2])
    + recorda(T(r"per a restar, canviem el signe de \textbf{tots} els termes del polinomi que restem: $-(x^3-2x^2+4x-1)=-x^3+2x^2-4x+1$.", r"para restar, cambiamos el signo de \textbf{todos} los términos del polinomio que restamos: $-(x^3-2x^2+4x-1)=-x^3+2x^2-4x+1$.")),
    tasks(2, [r'$%s=\res{%s}$' % (e, pt(pqr(e))) for e in L2], '4pt')))
OP = ['2x^2-7x+1', '-x^3+x-5', '4x^4-3x^2']
X.append((1, T("Escriu l'oposat de cada polinomi i comprova que la seua suma és 0:", "Escribe el opuesto de cada polinomio y comprueba que su suma es 0:") + tasks(3, ['$%s$' % tx(p) for p in OP]),
    tasks(3, [r'$\res{%s}$' % pt('-(%s)' % p) for p in OP], '4pt')))
L3 = ['P+Q-R', 'P-(Q+R)', 'Q-P-R', '2P-R']
X.append((2, T("Amb els polinomis de l'exercici %d, calcula:", "Con los polinomios del ejercicio %d, calcula:") % (sum(len(v) for _, v in S_[:-1]) + 1) + tasks(4, ['$%s$' % e for e in L3]),
    tasks(2, [r'$%s=\res{%s}$' % (e, pt(pqr(e).replace('2(', '2*('))) for e in L3], '4pt')))
SM = ['(x^2-4x+3)-(2x^2+x-5)+(x^2-1)', '(5x^3-2x)-(x^3+x^2-2x+4)', '-(x^2-3)+(4x^2-x)-(2x+7)', '(2x^2y-xy+3)-(x^2y+4xy-1)']
q, s = ops(SM, 1, 1)
X.append((2, T("Opera i redueix:", "Opera y reduce:") + q, s))
chk('(x^2-4x+3)-(2x^2+x-5)+(x^2-1)', '-5x+7')
X.append((3, T(r"Troba el polinomi $X(x)$ en cada cas:", r"Halla el polinomio $X(x)$ en cada caso:") + tasks(1, [r"$X(x)+(2x^2-3x+1)=5x^2+x-4$", r"$(x^3-x+2)-X(x)=3x^2+x$"], '4pt'),
    tasks(1, [r"$X=(5x^2+x-4)-(2x^2-3x+1)=\res{%s}$" % pt('(5x^2+x-4)-(2x^2-3x+1)'), r"$X=(x^3-x+2)-(3x^2+x)=\res{%s}$" % pt('(x^3-x+2)-(3x^2+x)')], '4pt')))
chk('(3x^2+4x-5)+(2x^2-3x+1)', '5x^2+x-4'); chk('(x^3-x+2)-(x^3-3x^2-2x+2)', '3x^2+x')
X.append((3, T(r"Els costats d'un pentàgon fan $x^2+1$, $2x$, $x^2-x+3$, $3x+2$ i $2x^2-4$ cm. Escriu-ne el perímetre i calcula'l per a $x=4$. Quant més llarg és el costat més llarg que el més curt quan $x=4$?",
               r"Los lados de un pentágono miden $x^2+1$, $2x$, $x^2-x+3$, $3x+2$ y $2x^2-4$ cm. Escribe su perímetro y calcúlalo para $x=4$. ¿Cuánto más largo es el lado más largo que el más corto cuando $x=4$?"),
    T(r"$P=\res{4x^2+4x+2}$; \ per a $x=4$: $64+16+2=\res{82\text{ cm}}$. \ Costats: 17, 8, 15, 14 i 28 cm: la diferència és $28-8=\res{20\text{ cm}}$.", r"$P=\res{4x^2+4x+2}$; \ para $x=4$: $64+16+2=\res{82\text{ cm}}$. \ Lados: 17, 8, 15, 14 y 28 cm: la diferencia es $28-8=\res{20\text{ cm}}$.")))
chk('(x^2+1)+2x+(x^2-x+3)+(3x+2)+(2x^2-4)', '4x^2+4x+2'); assert [val(e, x=4) for e in ['x^2+1', '2x', 'x^2-x+3', '3x+2', '2x^2-4']] == [17, 8, 15, 14, 28]

# =====================================================================
# 6. Producte de polinomis
X = sec(T('Producte de polinomis', 'Producto de polinomios'))
N1 = ['3(x^2-2x+5)', '-2(4x^3-x+1)', '5(x^2-3x)', '-(2x^2-x-7)', '1/2(4x^2-6x+2)', '-4(-x^3+2x^2-3)']
q, s = ops(N1, 3, 2)
X.append((1, T("Multiplica:", "Multiplica:") + q + recorda(T(r"propietat distributiva: multipliquem el nombre o el monomi per \textbf{cada} terme del polinomi.", r"propiedad distributiva: multiplicamos el número o el monomio por \textbf{cada} término del polinomio.")), s))
M1 = ['2x(x^2-3x+4)', '-3x^2(2x-5)', 'x^3(x^2+x-1)', '-4x(x^3-2x+3)', '5xy(x-2y+1)', '-x^2(-x^2+3x-6)']
q, s = ops(M1, 3, 2)
X.append((1, T("Multiplica:", "Multiplica:") + q, s))
B1 = ['(x+2)(x+5)', '(x-3)(x+4)', '(x-1)(x-6)', '(2x+1)(x-3)', '(3x-2)(2x+5)', '(x^2+1)(x-2)']
q, s = ops(B1, 3, 2)
X.append((1, T("Multiplica i redueix:", "Multiplica y reduce:") + q + recorda(T(r"cada terme del primer per cada terme del segon: $(x+3)(2x-5)=2x^2-5x+6x-15=2x^2+x-15$.", r"cada término del primero por cada término del segundo: $(x+3)(2x-5)=2x^2-5x+6x-15=2x^2+x-15$.")), s))
B2 = ['(x+2)(x^2-3x+1)', '(2x-1)(x^2+4x-3)', '(x^2-x+2)(3x+1)', '(x^2+2x-1)(x^2-2)']
q, s = ops(B2, 2, 1)
X.append((2, T("Multiplica i redueix:", "Multiplica y reduce:") + q, s))
SP2 = ['3(x+2)-2(x-1)', 'x(x+4)-2(x^2-3x)', '(x+1)(x-2)+(x+3)(x-1)', '2x(x-5)-(x+2)(x-3)']
q, s = ops(SP2, 2, 1)
X.append((2, T("Opera i redueix:", "Opera y reduce:") + q, s))
X.append((2, T(r"Escriu, com a polinomi reduït, l'àrea de: a) un rectangle de costats $x+4$ i $2x-1$; b) un quadrat de costat $x+3$ al qual llevem un quadrat de costat $x$; c) un triangle de base $2x+6$ i altura $x$.",
               r"Escribe, como polinomio reducido, el área de: a) un rectángulo de lados $x+4$ y $2x-1$; b) un cuadrado de lado $x+3$ al que quitamos un cuadrado de lado $x$; c) un triángulo de base $2x+6$ y altura $x$."),
    tasks(1, [r"$(x+4)(2x-1)=\res{%s}$" % pt('(x+4)(2x-1)'), r"$(x+3)(x+3)-x^2=\res{%s}$" % pt('(x+3)(x+3)-x^2'), r"$\dfrac{(2x+6)\cdot x}{2}=\res{%s}$" % pt('(2x+6)x/2')], '4pt')))
T3 = ['(x+1)(x-1)(x+3)', '(x-2)(2x+1)(x+2)']
q, s = ops(T3, 2, 1)
X.append((3, T("Multiplica (fes primer el producte de dos factors i després multiplica pel tercer):", "Multiplica (haz primero el producto de dos factores y después multiplica por el tercero):") + q, s))
H2 = ['(2x-1)(x+3)-(x-2)(x^2+x)+x^3', '(x^2-2x+3)(x+1)-x(x^2-x+1)']
q, s = ops(H2, 1, 1)
X.append((3, T("Opera i redueix:", "Opera y reduce:") + q, s))
chk('(2x-1)(x+3)-(x-2)(x^2+x)+x^3', '3x^2+7x-3'); chk('(x^2-2x+3)(x+1)-x(x^2-x+1)', '3')

# =====================================================================
# 7. Identitats notables
X = sec(T('Identitats notables', 'Identidades notables'))
I1 = ['(x+3)^2', '(x+7)^2', '(2x+1)^2', '(a+5b)^2']
q, s = ops(I1, 4, 2)
X.append((1, T("Desenvolupa (quadrat d'una suma):", "Desarrolla (cuadrado de una suma):") + q + recorda(T(r"$(a+b)^2=a^2+2ab+b^2$: \ el quadrat del primer, \textbf{més el doble del primer pel segon}, més el quadrat del segon.", r"$(a+b)^2=a^2+2ab+b^2$: \ el cuadrado del primero, \textbf{más el doble del primero por el segundo}, más el cuadrado del segundo.")), s))
I2 = ['(x-4)^2', '(x-1)^2', '(3x-2)^2', '(5-x)^2']
q, s = ops(I2, 4, 2)
X.append((1, T("Desenvolupa (quadrat d'una diferència):", "Desarrolla (cuadrado de una diferencia):") + q + recorda(T(r"$(a-b)^2=a^2-2ab+b^2$.", r"$(a-b)^2=a^2-2ab+b^2$.")), s))
I3 = ['(x+5)(x-5)', '(x-9)(x+9)', '(2x+3)(2x-3)', '(4+x)(4-x)']
q, s = ops(I3, 4, 2)
X.append((1, T("Desenvolupa (suma per diferència):", "Desarrolla (suma por diferencia):") + q + recorda(T(r"$(a+b)(a-b)=a^2-b^2$: suma per diferència és igual a diferència de quadrats.", r"$(a+b)(a-b)=a^2-b^2$: suma por diferencia es igual a diferencia de cuadrados.")), s))
I4 = ['(3x+4)^2', '(2x-5y)^2', '(x^2+3)^2', '(x^2-2x)^2', '(3a+2b)(3a-2b)', '(1/2x-2)^2']
q, s = ops(I4, 3, 2)
X.append((2, T("Desenvolupa fent servir les identitats notables:", "Desarrolla usando las identidades notables:") + q, s))
F1 = [('x^2+10x+25', '(x+5)^2'), ('x^2-6x+9', '(x-3)^2'), ('x^2-16', '(x+4)(x-4)'), ('4x^2+4x+1', '(2x+1)^2'), ('9x^2-25', '(3x+5)(3x-5)'), ('x^2-2x+1', '(x-1)^2')]
q, s = fc(F1, 3, 2)
X.append((2, T("Escriu com a quadrat d'un binomi o com a producte d'una suma per una diferència:", "Escribe como cuadrado de un binomio o como producto de una suma por una diferencia:") + q, s))
CP = [(r'(x+\square)^2=x^2+\square+16', r'(x+4)^2=x^2+8x+16'), (r'(x-\square)^2=x^2-10x+\square', r'(x-5)^2=x^2-10x+25'),
      (r'(\square+3)^2=4x^2+\square+9', r'(2x+3)^2=4x^2+12x+9'), (r'(x+\square)(x-\square)=x^2-49', r'(x+7)(x-7)=x^2-49')]
chk('(x+4)^2', 'x^2+8x+16'); chk('(x-5)^2', 'x^2-10x+25'); chk('(2x+3)^2', '4x^2+12x+9'); chk('(x+7)(x-7)', 'x^2-49')
X.append((2, T("Completa les caselles:", "Completa las casillas:") + tasks(2, ['$%s$' % q for q, _ in CP], '6pt'),
    tasks(2, [r'$\res{%s}$' % s for _, s in CP], '4pt')))
I5 = ['(x+2)^2-(x-2)^2', '(2x-1)^2-(2x+1)(2x-1)', '(x+3)^2-2(x-1)(x+1)-x(x+6)']
q, s = ops(I5, 1, 1)
X.append((3, T("Simplifica:", "Simplifica:") + q, s))
NUM = [('41^2', '(40+1)^2=1600+80+1', 1681), ('29^2', '(30-1)^2=900-60+1', 841), ('103\\cdot97', '(100+3)(100-3)=10\\,000-9', 9991), ('55^2-45^2', '(55+45)(55-45)=100\\cdot10', 1000)]
X.append((3, T("Calcula sense calculadora, fent servir les identitats notables:", "Calcula sin calculadora, usando las identidades notables:") + tasks(4, ['$%s$' % q for q, _, _ in NUM]),
    tasks(2, [r'$%s=%s=\res{%s}$' % (q, w, v) for q, w, v in NUM], '4pt')))
assert [41 ** 2, 29 ** 2, 103 * 97, 55 ** 2 - 45 ** 2] == [v for _, _, v in NUM]
X.append((3, T(r"a) Demostra que $(a+b)^2-(a-b)^2=4ab$. \ b) Fes-la servir per a calcular $(x+5)^2-(x-5)^2$ i $\ 1001^2-999^2$.", r"a) Demuestra que $(a+b)^2-(a-b)^2=4ab$. \ b) Úsala para calcular $(x+5)^2-(x-5)^2$ y $\ 1001^2-999^2$."),
    r"a) $a^2+2ab+b^2-(a^2-2ab+b^2)=a^2+2ab+b^2-a^2+2ab-b^2=\res{4ab}$ \quad b) $4\cdot x\cdot5=\res{20x}$; \ $4\cdot1000\cdot1=\res{4000}$"))
chk('(a+b)^2-(a-b)^2', '4a*b'); chk('(x+5)^2-(x-5)^2', '20x'); chk('1001**2-999**2', 4000)

# =====================================================================
# 8. Extracció de factor comú
X = sec(T('Extracció de factor comú', 'Extracción de factor común'))
K1 = [('3x+12', '3(x+4)'), ('5x^2-10x', '5x(x-2)'), ('x^3+x^2', 'x^2(x+1)'), ('8x-12', '4(2x-3)'), ('7x^2+14x^3', '7x^2(1+2x)'), ('6x^3-4x^2+2x', '2x(3x^2-2x+1)')]
q, s = fc(K1, 3, 2)
X.append((1, T("Trau factor comú:", "Saca factor común:") + q + recorda(T(r"el factor comú és el MCD dels coeficients per les lletres comunes a tots els termes amb el \textbf{menor} exponent. Dins del parèntesi va el que queda en dividir cada terme entre el factor comú (si un terme és igual al factor comú, hi queda un 1).",
                                                                                  r"el factor común es el MCD de los coeficientes por las letras comunes a todos los términos con el \textbf{menor} exponente. Dentro del paréntesis va lo que queda al dividir cada término entre el factor común (si un término es igual al factor común, queda un 1).")), s))
NQ = [('34\\cdot 18+34\\cdot 82', '34\\cdot(18+82)=34\\cdot100', 3400), ('125\\cdot 7-125\\cdot 3', '125\\cdot(7-3)=125\\cdot4', 500), ('9\\cdot 47+9\\cdot 53', '9\\cdot(47+53)=9\\cdot100', 900), ('56^2-56\\cdot 46', '56\\cdot(56-46)=56\\cdot10', 560)]
assert [34 * 18 + 34 * 82, 125 * 7 - 125 * 3, 9 * 47 + 9 * 53, 56 ** 2 - 56 * 46] == [v for _, _, v in NQ]
X.append((1, T("Calcula de la manera més ràpida, traient factor comú:", "Calcula de la manera más rápida, sacando factor común:") + tasks(4, ['$%s$' % q for q, _, _ in NQ]),
    tasks(2, [r'$%s=%s=\res{%s}$' % (q, w, v) for q, w, v in NQ], '4pt')))
K2 = [('4a^2b-6ab^2', '2ab(2a-3b)'), ('9x^4-6x^3+3x^2', '3x^2(3x^2-2x+1)'), ('10x^3y^2+15x^2y^3', '5x^2y^2(2x+3y)'), ('x^5-x^4+x^3-x^2', 'x^2(x^3-x^2+x-1)'), ('-8x^3-12x', '-4x(2x^2+3)'), ('12a^2b^3-18a^3b^2+6a^2b^2', '6a^2b^2(2b-3a+1)')]
q, s = fc(K2, 2, 2)
X.append((2, T("Trau factor comú:", "Saca factor común:") + q, s))
CF = [(r'6x^3-9x^2=3x^2(\square-\square)', r'3x^2(2x-3)'), (r'10x^4+5x^2=5x^2(\square+\square)', r'5x^2(2x^2+1)'), (r'x^2y-xy^2=\square(x-y)', r'xy(x-y)'), (r'14a^3-21a^2b=\square(2a-3b)', r'7a^2(2a-3b)')]
chk('3x^2(2x-3)', '6x^3-9x^2'); chk('5x^2(2x^2+1)', '10x^4+5x^2'); chk('x*y*(x-y)', 'x^2y-x*y^2'); chk('7a^2(2a-3b)', '14a^3-21a^2b')
X.append((2, T("Completa les caselles:", "Completa las casillas:") + tasks(2, ['$%s$' % q for q, _ in CF], '6pt'), tasks(2, [r'$\res{%s}$' % s for _, s in CF], '4pt')))
K3 = [('2x^3-8x', '2x(x+2)(x-2)'), ('3x^3+6x^2+3x', '3x(x+1)^2'), ('x^4-9x^2', 'x^2(x+3)(x-3)'), ('5x^3-20x^2+20x', '5x(x-2)^2')]
q, s = fc(K3, 2, 2)
X.append((3, T("Factoritza tant com pugues (primer el factor comú i després una identitat notable):", "Factoriza tanto como puedas (primero el factor común y después una identidad notable):") + q, s))
K4 = [('x(x+2)+3(x+2)', '(x+2)(x+3)'), ('2x(x-5)-(x-5)', '(x-5)(2x-1)'), ('(x+1)^2+4(x+1)', '(x+1)(x+5)')]
q, s = fc(K4, 3, 1)
X.append((3, T("Trau factor comú (el factor comú és un binomi):", "Saca factor común (el factor común es un binomio):") + q, s))
X.append((3, T("Sense calculadora:", "Sin calculadora:") + tasks(1, [r"$99^2+99$", r"$13\cdot87+13^2$", T(r"Demostra que $n^2+n$ sempre és parell per a qualsevol nombre natural $n$.", r"Demuestra que $n^2+n$ siempre es par para cualquier número natural $n$.")], '4pt'),
    tasks(1, [r"$99\cdot(99+1)=\res{9900}$", r"$13\cdot(87+13)=\res{1300}$", T(r"$n^2+n=\res{n(n+1)}$: és el producte de dos nombres consecutius i un dels dos sempre és parell.", r"$n^2+n=\res{n(n+1)}$: es el producto de dos números consecutivos y uno de los dos siempre es par.")], '4pt')))
assert 99 ** 2 + 99 == 9900 and 13 * 87 + 13 ** 2 == 1300; chk('n(n+1)', 'n^2+n')

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("llenguatge algebraic, valor numèric, monomis, monomis semblants, operacions amb monomis, potència d'un monomi, polinomis, suma i resta de polinomis, producte de polinomis, identitats notables, factor comú",
       'lenguaje algebraico, valor numérico, monomios, monomios semejantes, operaciones con monomios, potencia de un monomio, polinomios, suma y resta de polinomios, producto de polinomios, identidades notables, factor común')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T("Introducció a l'àlgebra. Polinomis", 'Introducción al álgebra. Polinomios')
TITC = TIT.replace('. ', '.\\\\ ')  # a la capçalera, «Polinomis» en una línia nova (sense partir paraules)

def build(sol):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 3: %s' % (t, TIT), capcalera='%s · Unidad 3: %s' % (t, TIT), pdfkeywords=KW, curs='2eso')
        cap = assignatura('2eso') + '{' + ('Soluciones de la ficha · Unidad 3' if sol else 'Ficha de ejercicios · Unidad 3') + '}{' + TITC + '}'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat 3: %s. 2n d'ESO}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 3: %s · 2n d'ESO" % (t, TIT))
        assert "2n d'ESO" in p and 'Polinomis' in p
        cap = r'\capcalera{Matemàtiques}{2n ESO}{' + ('Solucions de la fitxa · Unitat 3' if sol else "Fitxa d'exercicis · Unitat 3") + '}{' + TITC + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{12}\n\\input{../comu/fentmates.tex}\n\\fmcurs{2eso}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb les eines interactives dels apunts de la unitat. Els polinomis dels resultats estan reduïts i ordenats de grau més alt a més baix.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con las herramientas interactivas de los apuntes de la unidad. Los polinomios de los resultados están reducidos y ordenados de mayor a menor grado.") if sol else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i sense calculadora. Dona els resultats reduïts i ordenats. Les seccions segueixen l'ordre dels apunts de la unitat (3.1--3.8).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y sin calculadora. Da los resultados reducidos y ordenados. Las secciones siguen el orden de los apuntes de la unidad (3.1--3.8)."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't3-fitxa-%s%s.tex' % ('solucions' if sol else 'exercicis', '-es' if ES else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
n_ = sum(len(x[1]) for x in S_)
print(n_, T('exercicis,', 'ejercicios,'), len(CHK), T('comprovacions', 'comprobaciones'))
