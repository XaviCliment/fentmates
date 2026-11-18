# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 7: Funcions elementals)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py (curs='4eso-a').
# Les 9 seccions segueixen els apartats dels apunts (7.1-7.9): funcions lineals (proporcionalitat directa, afins i constants),
# equació punt-pendent, funció quadràtica, representació de funcions quadràtiques, funcions radicals, proporcionalitat inversa,
# translacions de la hipèrbola, funcions exponencials i problemes amb funcions.
# Parteix de la fitxa de la unitat 8 de 4t ESO B (4eso-b-t8), sense funcions a trossos, valor absolut ni logaritmes, amb menys
# profunditat i amb seccions noves de punt-pendent, representació de paràboles i funcions radicals.
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es). Les gràfiques es dibuixen amb la classe Plot de _eines/apunts/4eso-b-t7/fig.py (la mateixa
# dels apunts). Comprovacions: sympy calcula talls, vèrtexs i solucions, i les dades dels problemes es comproven amb ok().
# Els intervals s'escriuen com a la resta de 4t: (a,b) obert i [a,b] tancat. Els decimals, dins de les fórmules, amb {,}.
# Ús: python3 genera.py && pdflatex t7-fitxa-exercicis.tex (dues vegades) && pdflatex t7-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '4eso-b-t7'))
from eso4b import *
from fig import Plot, sq
import sympy as sp

ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va
x = sp.symbols('x', real=True)

def ok(cond, msg=''):
    assert cond, msg
    CHK.append((True, True))
def G(p, w=3.7): return '\n\n\\begin{center}' + p.tikz(w) + '\\end{center}\n'
def Gi(p, w=2.95): return p.tikz(w)
def items(*xs): return r'\begin{enumerate}[label=\alph*),leftmargin=*,itemsep=2pt,topsep=2pt]' + ''.join(r'\item ' + t for t in xs) + r'\end{enumerate}'
def fixm(t):
    """dins de les fórmules (i fora dels dibuixos), espai fi després de les comes de punts i intervals: (2,-1) -> (2,\\,-1)"""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    def m(mm): return re.sub(r',(?=[-\d+a-zA-Z(\[]|\\(?![,; ]))', r',\\,', mm.group(0))
    for i in range(0, len(parts), 2): parts[i] = re.sub(r'\$[^$]*\$', m, parts[i])
    return ''.join(parts)
def E(st, q, s): return (st, fixm(q), fixm(s))
IR = r'\mathbb{R}'
def ckroots(expr, sols, msg=''):
    got = sorted(sp.solve(sp.sympify(expr, locals={'x': x}), x), key=float)
    want = sorted([sp.sympify(s) for s in sols], key=float)
    ok(len(got) == len(want) and all(sp.simplify(a - b) == 0 for a, b in zip(got, want)), (msg, got, want))
def vert(a, b, c):
    """vèrtex de ax²+bx+c amb fraccions exactes"""
    vx = F(-b, 2 * a); return vx, a * vx * vx + b * vx + c
def line2(p, q):
    """recta per dos punts: (m, n) amb fraccions exactes"""
    m = F(q[1] - p[1], q[0] - p[0]); return m, p[1] - m * p[0]
def lin_t(m, n):
    """y = mx + n en LaTeX"""
    s = '' if m == 0 else ('x' if m == 1 else '-x' if m == -1 else tn(m) + 'x')
    if n or not s: s += ('+' if n > 0 and s else '') + tn(n)
    return s.replace(r'\frac', r'\frac', 1)
TB = lambda row1, row2, n: (r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|" + 'C{1cm}|' * n + r"}\hline " + row1 + r"\\\hline " + row2 + r"\\\hline\end{tabular}\end{center}")
CRE, DEC = T('creixent', 'creciente'), T('decreixent', 'decreciente')
I_ = T('i', 'y')

S = []
def sec(title): S.append((title, [])); return S[-1][1]

# =====================================================================
# 1. Funcions lineals
X = sec(T('Funcions lineals', 'Funciones lineales'))
L1 = [('2x+1', lambda t: 2 * t + 1, (0, 1), (1, 3)), ('-x-2', lambda t: -t - 2, (0, -2), (-2, 0)), ('3x', lambda t: 3 * t, (0, 0), (1, 3)),
      ('-2x', lambda t: -2 * t, (0, 0), (1, -2)), ('-2', lambda t: -2, (0, -2), (3, -2)), (r'\frac12x+2', lambda t: t / 2 + 2, (0, 2), (2, 3))]
for _, f, p, q in L1: ok(f(p[0]) == p[1] and f(q[0]) == q[1])
def lp(i): return Plot(-4, 4, -4, 4, W=180).fn(L1[i][1]).dot(*L1[i][2], 'b').dot(*L1[i][3], 'b')
X.append(E(1, T(r"Dibuixa les rectes següents i digues de quin tipus és cadascuna (de proporcionalitat directa, afí o constant):", r"Dibuja las rectas siguientes y di de qué tipo es cada una (de proporcionalidad directa, afín o constante):") + tasks(3, ['$f(x)=%s$' % l[0] for l in L1])
    + recorda(T(r"per a dibuixar una recta n'hi ha prou amb dos punts: fes una taula de valors amb dos valors de $x$.", r"para dibujar una recta basta con dos puntos: haz una tabla de valores con dos valores de $x$.")),
    tasks(3, [Gi(lp(i), 2.6) + r'\\[2pt]$%s$, $%s$' % ('(%d,%d)' % L1[i][2], '(%d,%d)' % L1[i][3]) for i in range(6)])
    + T(r"La c) i la d) són de \rest{proporcionalitat directa} (passen per l'origen); la e) és \rest{constant}; la a), la b) i la f) són \rest{afins}.",
        r"La c) y la d) son de \rest{proporcionalidad directa} (pasan por el origen); la e) es \rest{constante}; la a), la b) y la f) son \rest{afines}.")))
AF, PD, CO = T('afí', 'afín'), T('prop. directa', 'prop. directa'), T('constant', 'constante')
X.append(E(1, T(r"Sense dibuixar-les, indica el pendent, l'ordenada en l'origen i el tipus de cada recta, i digues si és creixent, decreixent o constant:", r"Sin dibujarlas, indica la pendiente, la ordenada en el origen y el tipo de cada recta, y di si es creciente, decreciente o constante:")
    + tasks(4, ['$y=3x-5$', r'$y=-\dfrac x2+4$', '$y=7$', '$y=-4x$']),
    tasks(1, [r'$m=\res{3}$, $n=\res{-5}$; \rest{%s}, \rest{%s}' % (AF, CRE), r'$m=\res{-\frac12}$, $n=\res{4}$; \rest{%s}, \rest{%s}' % (AF, DEC),
              r'$m=\res{0}$, $n=\res{7}$; \rest{%s}' % CO, r'$m=\res{-4}$, $n=\res{0}$; \rest{%s}, \rest{%s}' % (PD, DEC)])))
ok(1.2 * 2.5 == 3 and 20 - 2 * 4 == 12)
X.append(E(1, T(r"Escriu la funció que relaciona les dues magnituds i digues de quin tipus és:", r"Escribe la función que relaciona las dos magnitudes y di de qué tipo es:") + tasks(1, [
    T(r"El preu $y$ de $x$ kg de taronges a 1,20 € el quilo.", r"El precio $y$ de $x$ kg de naranjas a 1,20 € el kilo."),
    T(r"El que paguem cada mes, $y$, en una tarifa plana de 25 € al mes, segons les hores $x$ que ens connectem.", r"Lo que pagamos cada mes, $y$, en una tarifa plana de 25 € al mes, según las horas $x$ que nos conectamos."),
    T(r"El preu $y$ d'una carrera de taxi de $x$ km si cobra 3 € per la baixada de bandera i 1 € per km.", r"El precio $y$ de una carrera de taxi de $x$ km si cobra 3 € por la bajada de bandera y 1 € por km."),
    T(r"L'altura $y$ (en cm) d'una espelma de 20 cm que es consumeix 2 cm cada hora, al cap de $x$ hores.", r"La altura $y$ (en cm) de una vela de 20 cm que se consume 2 cm cada hora, al cabo de $x$ horas.")]),
    tasks(2, [r'$\res{y=1{,}2x}$: \rest{%s}' % T('proporcionalitat directa', 'proporcionalidad directa'), r'$\res{y=25}$: \rest{%s}' % CO,
              r'$\res{y=x+3}$: \rest{%s}' % AF, r'$\res{y=20-2x}$: \rest{%s} %s' % (AF, T('(decreixent)', '(decreciente)'))])))
ok(all(3 * a == b for a, b in [(1, 3), (2, 6), (3, 9), (5, 15)]) and all(2 * a + 3 == b for a, b in [(0, 3), (2, 7), (4, 11), (6, 15)]))
X.append(E(2, T(r"Digues si cada taula correspon a una funció de proporcionalitat directa o afí i escriu-ne l'expressió:", r"Di si cada tabla corresponde a una función de proporcionalidad directa o afín y escribe su expresión:")
    + tasks(2, [TB(r'$x$ & $1$ & $2$ & $3$ & $5$', r'$y$ & $3$ & $6$ & $9$ & $15$', 4), TB(r'$x$ & $0$ & $2$ & $4$ & $6$', r'$y$ & $3$ & $7$ & $11$ & $15$', 4)]),
    tasks(1, [T(r"$\frac yx=3$ sempre: \rest{proporcionalitat directa}, $\res{y=3x}$.", r"$\frac yx=3$ siempre: \rest{proporcionalidad directa}, $\res{y=3x}$."),
              T(r"Cada vegada que $x$ augmenta 2, $y$ augmenta 4: $m=\frac42=2$. Com que $f(0)=3$, $n=3$: \rest{afí}, $\res{y=2x+3}$.", r"Cada vez que $x$ aumenta 2, $y$ aumenta 4: $m=\frac42=2$. Como $f(0)=3$, $n=3$: \rest{afín}, $\res{y=2x+3}$.")])))
X.append(E(2, T(r"Representa en uns mateixos eixos $y=2x$, $y=2x+3$ i $y=2x-1$. Què tenen en comú? En què es diferencien?", r"Representa en unos mismos ejes $y=2x$, $y=2x+3$ e $y=2x-1$. ¿Qué tienen en común? ¿En qué se diferencian?"),
    G(Plot(-4, 4, -5, 7, W=200).fn(lambda t: 2 * t, col='g').fn(lambda t: 2 * t + 3, col='b').fn(lambda t: 2 * t - 1).dot(0, 0, 'g').dot(0, 3, 'b').dot(0, -1), 3.4)
    + T(r"Tenen el mateix pendent, $m=2$: són \rest{paral·leles}. Es diferencien en l'ordenada en l'origen: tallen l'eix $OY$ en $(0,0)$, $(0,3)$ i $(0,-1)$.",
        r"Tienen la misma pendiente, $m=2$: son \rest{paralelas}. Se diferencian en la ordenada en el origen: cortan el eje $OY$ en $(0,0)$, $(0,3)$ y $(0,-1)$.")))

# =====================================================================
# 2. Equació punt-pendent
X = sec(T('Equació punt-pendent', 'Ecuación punto-pendiente'))
P6 = [((1, 2), (3, 8)), ((-2, 5), (4, -1)), ((0, 4), (6, 1)), ((-3, -2), (1, 6))]
M6 = [line2(*p)[0] for p in P6]
ok(M6 == [3, -1, F(-1, 2), 2])
def mfrac(p, q): return r'm=\dfrac{%d-%s}{%d-%s}' % (q[1], '(%d)' % p[1] if p[1] < 0 else str(p[1]), q[0], '(%d)' % p[0] if p[0] < 0 else str(p[0]))
X.append(E(1, T(r"Calcula el pendent de la recta que passa pels punts:", r"Calcula la pendiente de la recta que pasa por los puntos:") + tasks(4, [r'$(%d,%d)$ %s $(%d,%d)$' % (p + (I_,) + q) for p, q in P6])
    + recorda(r"$m=\dfrac{y_2-y_1}{x_2-x_1}$."),
    tasks(2, [r'$%s=\res{%s}$' % (mfrac(p, q), tn(m)) for (p, q), m in zip(P6, M6)])))
P7 = [(3, (2, 1)), (-2, (-1, 4)), (F(1, 2), (4, 3)), (0, (5, -2))]
def pp_t(m, p):
    """equació punt-pendent y = y1 + m(x - x1)"""
    if m == 0: return 'y=%d' % p[1]
    ms = '' if abs(m) == 1 else tn(abs(m))
    if p[0] == 0: return 'y=%d%s%sx' % (p[1], '+' if m > 0 else '-', ms)
    return 'y=%d%s%s(x%+d)' % (p[1], '+' if m > 0 else '-', ms, -p[0])
for m, p in P7: ok(m * p[0] + (p[1] - m * p[0]) == p[1])
X.append(E(1, T(r"Escriu l'equació punt-pendent i l'equació explícita ($y=mx+n$) de la recta:", r"Escribe la ecuación punto-pendiente y la ecuación explícita ($y=mx+n$) de la recta:") + tasks(2, [
    T(r"De pendent $3$ que passa per $(2,1)$.", r"De pendiente $3$ que pasa por $(2,1)$."), T(r"De pendent $-2$ que passa per $(-1,4)$.", r"De pendiente $-2$ que pasa por $(-1,4)$."),
    T(r"De pendent $\frac12$ que passa per $(4,3)$.", r"De pendiente $\frac12$ que pasa por $(4,3)$."), T(r"De pendent $0$ que passa per $(5,-2)$.", r"De pendiente $0$ que pasa por $(5,-2)$.")])
    + recorda(r"$y=y_1+m(x-x_1)$."),
    tasks(2, [r'$%s\Rightarrow\res{y=%s}$' % (pp_t(m, p), lin_t(m, p[1] - m * p[0])) if m else r'$\res{y=-2}$ ' + T('(constant)', '(constante)') for m, p in P7])))
P8 = [((1, 2), (3, 8)), ((-2, 5), (4, -1)), ((0, -3), (2, 1)), ((-1, -4), (3, 4))]
X.append(E(1, T(r"Troba l'equació de la recta que passa pels punts:", r"Halla la ecuación de la recta que pasa por los puntos:") + tasks(4, [r'$(%d,%d)$ %s $(%d,%d)$' % (p + (I_,) + q) for p, q in P8]),
    tasks(1, [r'$%s=%s$; \ $%s\Rightarrow\res{y=%s}$' % (mfrac(p, q), tn(line2(p, q)[0]), pp_t(line2(p, q)[0], p), lin_t(*line2(p, q))) for p, q in P8])))
ok([line2(*p) for p in P8] == [(3, -1), (-1, 3), (2, -3), (2, -2)])
g3 = (Plot(-5, 6, -4, 4, W=330).fn(lambda t: 2, col='g').fn(lambda t: 2 * t + 1, col='b').fn(lambda t: -t - 1, col='a').fn(lambda t: t / 2, col='o')
      .text(5.6, 2.45, r'\normalsize$\boldsymbol{f}$', 'g').text(1.9, 3.5, r'\normalsize$\boldsymbol{g}$', 'b').text(-4.5, 3.0, r'\normalsize$\boldsymbol{h}$', 'a').text(5.5, 3.3, r'\normalsize$\boldsymbol{i}$', 'o'))
X.append(E(2, T(r"Troba l'expressió de cada recta a partir de la gràfica i digues de quin tipus és:", r"Halla la expresión de cada recta a partir de la gráfica y di de qué tipo es:") + G(g3, 7),
    tasks(1, [T(r"$f$: horitzontal a altura 2: $\res{f(x)=2}$ (constant)", r"$f$: horizontal a altura 2: $\res{f(x)=2}$ (constante)"),
              T(r"$g$: passa per $(0,1)$ i $(1,3)$: $m=2$, $n=1$: $\res{g(x)=2x+1}$ (afí)", r"$g$: pasa por $(0,1)$ y $(1,3)$: $m=2$, $n=1$: $\res{g(x)=2x+1}$ (afín)"),
              T(r"$h$: passa per $(0,-1)$ i $(-1,0)$: $m=-1$, $n=-1$: $\res{h(x)=-x-1}$ (afí)", r"$h$: pasa por $(0,-1)$ y $(-1,0)$: $m=-1$, $n=-1$: $\res{h(x)=-x-1}$ (afín)"),
              T(r"$i$: passa per $(0,0)$ i $(2,1)$: $m=\frac12$, $n=0$: $\res{i(x)=\frac12x}$ (proporcionalitat directa)", r"$i$: pasa por $(0,0)$ y $(2,1)$: $m=\frac12$, $n=0$: $\res{i(x)=\frac12x}$ (proporcionalidad directa)")])))
ok(-3 * 2 + 5 == -1 and 2 * 0 + 4 == 4)
X.append(E(2, T(r"Troba l'equació de la recta:", r"Halla la ecuación de la recta:") + tasks(1, [
    T(r"Paral·lela a $y=2x-7$ que passa per $(0,4)$.", r"Paralela a $y=2x-7$ que pasa por $(0,4)$."),
    T(r"Paral·lela a $y=-3x+1$ que passa per $(2,-1)$.", r"Paralela a $y=-3x+1$ que pasa por $(2,-1)$."),
    T(r"Paral·lela a l'eix $OX$ que passa per $(3,5)$.", r"Paralela al eje $OX$ que pasa por $(3,5)$.")]),
    tasks(1, [T(r'Mateix pendent, $m=2$, i $n=4$: $\res{y=2x+4}$', r'Misma pendiente, $m=2$, y $n=4$: $\res{y=2x+4}$'),
              r'$m=-3$: \ $y=-1-3(x-2)\Rightarrow\res{y=-3x+5}$',
              T(r'Recta horitzontal ($m=0$): $\res{y=5}$', r'Recta horizontal ($m=0$): $\res{y=5}$')])))
ok(line2((1, 1), (3, 5)) == (2, -1) and 2 * 5 - 1 == 9 and line2((0, 2), (2, 5)) == (F(3, 2), 2) and F(3, 2) * 4 + 2 == 8)
X.append(E(2, T(r"Comprova si els tres punts estan alineats (si són de la mateixa recta):", r"Comprueba si los tres puntos están alineados (si son de la misma recta):") + tasks(2, ['$(1,1)$, $(3,5)$ %s $(5,9)$' % I_, '$(0,2)$, $(2,5)$ %s $(4,9)$' % I_]),
    tasks(1, [T(r"Recta per $(1,1)$ i $(3,5)$: $m=2$, $y=2x-1$. Com que $2\cdot5-1=9$, \rest{sí que estan alineats}.", r"Recta por $(1,1)$ y $(3,5)$: $m=2$, $y=2x-1$. Como $2\cdot5-1=9$, \rest{sí están alineados}."),
              T(r"Recta per $(0,2)$ i $(2,5)$: $m=\frac32$, $y=\frac32x+2$. Com que $\frac32\cdot4+2=8\neq9$, \rest{no estan alineats}.", r"Recta por $(0,2)$ y $(2,5)$: $m=\frac32$, $y=\frac32x+2$. Como $\frac32\cdot4+2=8\neq9$, \rest{no están alineados}.")])))
ok(2 * 2 - 1 == 3 and -2 + 5 == 3)
X.append(E(2, T(r"Representa en uns mateixos eixos $f(x)=2x-1$ i $g(x)=-x+5$ i troba'n el punt de tall, gràficament i resolent una equació.", r"Representa en unos mismos ejes $f(x)=2x-1$ y $g(x)=-x+5$ y halla su punto de corte, gráficamente y resolviendo una ecuación."),
    r'$2x-1=-x+5\Rightarrow3x=6\Rightarrow x=2$, $y=3$: \ $\res{(2,3)}$' + G(Plot(-2, 6, -2, 6, W=200).fn(lambda t: 2 * t - 1).fn(lambda t: -t + 5, col='b').dot(2, 3, 'v'), 3.6)))
ok(line2((2, 3), (6, 5)) == (F(1, 2), 2) and F(1, 2) * 10 + 2 == 7)
X.append(E(3, T(r"Una recta passa pels punts $A(2,3)$ i $B(6,5)$. Troba'n l'equació, els punts de tall amb els eixos i comprova si el punt $(10,7)$ és de la recta.", r"Una recta pasa por los puntos $A(2,3)$ y $B(6,5)$. Halla su ecuación, los puntos de corte con los ejes y comprueba si el punto $(10,7)$ es de la recta."),
    r'$m=\frac{5-3}{6-2}=\frac12$; \ $y=3+\frac12(x-2)\Rightarrow\res{y=\frac12x+2}$. \ $OY$: $\res{(0,2)}$; \ $OX$: $\frac12x+2=0\Rightarrow\res{(-4,0)}$. \ '
    + T(r'$\frac12\cdot10+2=7$: \rest{sí que hi és}.', r'$\frac12\cdot10+2=7$: \rest{sí está}.')))

# =====================================================================
# 3. Funció quadràtica
X = sec(T('Funció quadràtica', 'Función cuadrática'))
Q8 = [('x^2-6x+5', 1, -6, 5), ('-x^2+4x', -1, 4, 0), ('2x^2+4x+5', 2, 4, 5), ('-x^2-2x-1', -1, -2, -1)]
def roots(a, b, c): return sorted(sp.solve(a * x ** 2 + b * x + c, x), key=float) if b * b - 4 * a * c >= 0 else []
def q8sol(tx, a, b, c):
    vx, vy = vert(a, b, c); r = roots(a, b, c)
    ox = (r'$OX$: $\res{' + r',\ '.join('(%s,0)' % sp.latex(v) for v in r) + '}$') if r else r'$OX$: ' + T(r'no en té ($\Delta<0$)', r'no tiene ($\Delta<0$)')
    return (r'$\%s$; ' % ('cup' if a > 0 else 'cap') + r'$V\res{(%s,%s)}$, ' % (tn(vx), tn(vy)) + T('eix', 'eje') + r' $\res{x=%s}$; ' % tn(vx) + r'$OY$: $\res{(0,%d)}$; ' % c + ox
            + r'; $R=\res{%s}$' % ('[%s,+\\infty)' % tn(vy) if a > 0 else '(-\\infty,%s]' % tn(vy)))
ok(vert(1, -6, 5) == (3, -4) and vert(-1, 4, 0) == (2, 4) and vert(2, 4, 5) == (-1, 3) and vert(-1, -2, -1) == (-1, 0))
X.append(E(1, T(r"Sense dibuixar-les, indica la forma ($\cup$ o $\cap$), el vèrtex, l'eix de simetria, els punts de tall amb els eixos i el recorregut de:", r"Sin dibujarlas, indica la forma ($\cup$ o $\cap$), el vértice, el eje de simetría, los puntos de corte con los ejes y el recorrido de:")
    + tasks(4, ['$y=%s$' % q[0] for q in Q8]) + recorda(r"$V_x=\dfrac{-b}{2a}$, \ $V_y=f(V_x)$."),
    tasks(1, [q8sol(*q) for q in Q8])))
X.append(E(1, T(r"Sense fer càlculs, digues quines d'aquestes paràboles tenen les branques cap amunt i quines cap avall. Quina és la més tancada? Quina té el vèrtex en $(0,1)$?", r"Sin hacer cálculos, di cuáles de estas parábolas tienen las ramas hacia arriba y cuáles hacia abajo. ¿Cuál es la más cerrada? ¿Cuál tiene el vértice en $(0,1)$?")
    + tasks(4, ['$y=3x^2$', '$y=-x^2$', r'$y=\frac12x^2$', '$y=-2x^2+1$']),
    T(r"Cap amunt ($a>0$): \rest{a) i c)}. Cap avall ($a<0$): \rest{b) i d)}. La més tancada és \rest{a)} ($|a|=3$ és el més gran). La d) té el vèrtex en $(0,1)$.",
      r"Hacia arriba ($a>0$): \rest{a) y c)}. Hacia abajo ($a<0$): \rest{b) y d)}. La más cerrada es \rest{a)} ($|a|=3$ es el mayor). La d) tiene el vértice en $(0,1)$.")))
Q16 = [('x^2-x-6', 1, -1, -6), ('x^2-9', 1, 0, -9), ('2x^2-8x', 2, -8, 0), ('x^2+4x+4', 1, 4, 4)]
ckroots('x**2-x-6', [-2, 3]); ckroots('x**2-9', [-3, 3]); ckroots('2*x**2-8*x', [0, 4]); ckroots('x**2+4*x+4', [-2])
X.append(E(2, T(r"Troba els punts de tall amb els eixos de les paràboles:", r"Halla los puntos de corte con los ejes de las parábolas:") + tasks(4, ['$y=%s$' % q[0] for q in Q16]),
    tasks(2, [r'$OX$: $\res{' + r',\ '.join('(%s,0)' % sp.latex(v) for v in roots(*q[1:])) + r'}$; \ $OY$: $\res{(0,%d)}$' % q[3] for q in Q16])
    + T(r"La d) només toca l'eix $OX$ en un punt, que és el vèrtex.", r"La d) solo toca el eje $OX$ en un punto, que es el vértice.")))
f17 = lambda t: t * t - 3 * t + 2
ok(f17(0) == 2 and f17(1) == 0 and f17(2) == 0 and f17(-1) == 6)
X.append(E(2, T(r"Comprova quins d'aquests punts són de la paràbola $y=x^2-3x+2$:", r"Comprueba cuáles de estos puntos son de la parábola $y=x^2-3x+2$:") + tasks(4, ['$(0,2)$', '$(1,0)$', '$(2,1)$', '$(-1,6)$']),
    tasks(2, [r'$f(0)=2$: \rest{%s}' % T('sí', 'sí'), r'$f(1)=1-3+2=0$: \rest{%s}' % T('sí', 'sí'), r'$f(2)=4-6+2=0\neq1$: \rest{no}', r'$f(-1)=1+3+2=6$: \rest{%s}' % T('sí', 'sí')])))
ok(sp.expand((x - 3) * (x + 1)) == x ** 2 - 2 * x - 3 and vert(1, -4, 3)[0] == 2 and vert(1, -2, -3) == (1, -4))
X.append(E(3, T(r"Troba l'expressió de la funció quadràtica en cada cas:", r"Halla la expresión de la función cuadrática en cada caso:") + tasks(1, [
    T(r"$y=x^2+bx+c$, sabent que passa pel punt $(0,3)$ i que té el vèrtex en $x=2$.", r"$y=x^2+bx+c$, sabiendo que pasa por el punto $(0,3)$ y que tiene el vértice en $x=2$."),
    T(r"$y=x^2+bx+c$, sabent que talla l'eix $OX$ en $x=3$ i en $x=-1$.", r"$y=x^2+bx+c$, sabiendo que corta el eje $OX$ en $x=3$ y en $x=-1$.")]),
    tasks(1, [r'$f(0)=c=3$; \ $V_x=\frac{-b}{2}=2\Rightarrow b=-4$: \ $\res{y=x^2-4x+3}$',
              T(r'$y=(x-3)(x+1)$: \ $\res{y=x^2-2x-3}$ (comprovació: $9-6-3=0$ i $1+2-3=0$)', r'$y=(x-3)(x+1)$: \ $\res{y=x^2-2x-3}$ (comprobación: $9-6-3=0$ y $1+2-3=0$)')])))

# =====================================================================
# 4. Representació de funcions quadràtiques
X = sec(T('Representació de funcions quadràtiques', 'Representación de funciones cuadráticas'))
Q2 = [('x^2', 1, 0, 0), ('x^2+1', 1, 0, 1), ('x^2-2x-3', 1, -2, -3), ('-x^2+4x-3', -1, 4, -3), ('x^2+2x', 1, 2, 0), ('-x^2+3', -1, 0, 3)]
def qsol(tx, a, b, c):
    vx, vy = vert(a, b, c); r = roots(a, b, c)
    ox = (r'$OX$: $' + r',\ '.join('(%s,0)' % sp.latex(v) for v in r) + '$') if r else r'$OX$: ' + T('no en té', 'no tiene')
    p = Plot(-4, 5, -5, 6, W=180).fn(lambda t: a * t * t + b * t + c).dot(float(vx), float(vy), 'v')
    for v in r: p.dot(float(v), 0, 'b')
    return Gi(p, 2.6) + r'\\[2pt]$V\res{(%s,%s)}$\\ ' % (tn(vx), tn(vy)) + ox
ok(vert(1, -2, -3) == (1, -4) and vert(-1, 4, -3) == (2, 1) and vert(1, 2, 0) == (-1, -1) and vert(-1, 0, 3) == (0, 3))
X.append(E(1, T(r"Representa les paràboles següents fent els càlculs necessaris:", r"Representa las parábolas siguientes haciendo los cálculos necesarios:") + tasks(3, ['$f(x)=%s$' % q[0] for q in Q2])
    + recorda(T(r"forma ($\cup$ si $a>0$, $\cap$ si $a<0$), vèrtex i eix, tall amb $OY$ i el seu simètric, talls amb $OX$ i, si cal, una taula de valors al voltant del vèrtex.",
                r"forma ($\cup$ si $a>0$, $\cap$ si $a<0$), vértice y eje, corte con $OY$ y su simétrico, cortes con $OX$ y, si hace falta, una tabla de valores alrededor del vértice.")),
    tasks(3, [qsol(*q) for q in Q2])))
f20 = lambda t: -t * t + 2 * t + 3
ok(vert(-1, 2, 3) == (1, 4) and f20(-1) == 0 and f20(3) == 0 and f20(2) == 3)
X.append(E(2, T(r"Representa $f(x)=-x^2+2x+3$ i indica'n el domini, el recorregut, on creix i on decreix, i el màxim o el mínim.", r"Representa $f(x)=-x^2+2x+3$ e indica su dominio, el recorrido, dónde crece y dónde decrece, y el máximo o el mínimo."),
    T(r"$a=-1<0$: $\cap$. $V(1,4)$, eix $x=1$; $OY$: $(0,3)$ i el simètric $(2,3)$; $OX$: $-x^2+2x+3=0\Rightarrow x=-1,\ x=3$.",
      r"$a=-1<0$: $\cap$. $V(1,4)$, eje $x=1$; $OY$: $(0,3)$ y el simétrico $(2,3)$; $OX$: $-x^2+2x+3=0\Rightarrow x=-1,\ x=3$.")
    + G(Plot(-3, 5, -3, 5, W=200).gd(1, -3, 1, 5).fn(f20).dot(1, 4, 'v').dot(-1, 0, 'b').dot(3, 0, 'b').dot(0, 3, 'g').dot(2, 3, 'g'), 3.4)
    + T(r"$D=\res{%s}$, $R=\res{(-\infty,4]}$. \rest{Creixent} en $(-\infty,1)$ i \rest{decreixent} en $(1,+\infty)$. \rest{Màxim} en $(1,4)$.",
        r"$D=\res{%s}$, $R=\res{(-\infty,4]}$. \rest{Creciente} en $(-\infty,1)$ y \rest{decreciente} en $(1,+\infty)$. \rest{Máximo} en $(1,4)$.") % IR))
f21 = lambda t: t * t - 4 * t + 5
ok(vert(1, -4, 5) == (2, 1) and 16 - 20 < 0 and f21(1) == 2 and f21(3) == 2 and f21(0) == 5 and f21(4) == 5)
X.append(E(2, T(r"Representa $f(x)=x^2-4x+5$. Talla l'eix $OX$? Completa la representació amb una taula de valors.", r"Representa $f(x)=x^2-4x+5$. ¿Corta el eje $OX$? Completa la representación con una tabla de valores."),
    T(r"$\cup$; $V(2,1)$, eix $x=2$; $OY$: $(0,5)$ i el simètric $(4,5)$. $\Delta=16-20<0$: \rest{no talla l'eix $OX$}.",
      r"$\cup$; $V(2,1)$, eje $x=2$; $OY$: $(0,5)$ y el simétrico $(4,5)$. $\Delta=16-20<0$: \rest{no corta el eje $OX$}.")
    + TB(r'$x$ & $0$ & $1$ & $2$ & $3$ & $4$', r'$y$ & $5$ & $2$ & $1$ & $2$ & $5$', 5)
    + G(Plot(-2, 6, -1, 7, W=200).gd(2, -1, 2, 7).fn(f21).dot(2, 1, 'v').dot(0, 5, 'g').dot(4, 5, 'g').dot(1, 2, 'o').dot(3, 2, 'o'), 3.2) + r'$R=\res{[1,+\infty)}$'))
g4 = (Plot(-6, 8, -6, 6, W=330).fn(lambda t: -t * t - 4 * t - 2, col='m').fn(lambda t: (t - 2) * (t + 1), col='v').fn(lambda t: -t * t / 2 + 3 * t - 1, col='o').fn(lambda t: (t - 3) ** 2, col='g')
      .text(-3.9, -2.2, r'\normalsize$\boldsymbol{f}$', 'm').text(-1.9, 3.8, r'\normalsize$\boldsymbol{g}$', 'v').text(5.9, 0.7, r'\normalsize$\boldsymbol{h}$', 'o').text(5.3, 3.8, r'\normalsize$\boldsymbol{i}$', 'g'))
ok(vert(-1, -4, -2) == (-2, 2) and vert(1, -1, -2) == (F(1, 2), F(-9, 4)) and vert(F(-1, 2), 3, -1) == (3, F(7, 2)) and vert(1, -6, 9) == (3, 0))
X.append(E(2, T(r"Relaciona les gràfiques de paràboles següents amb les funcions corresponents, justificant la resposta:", r"Relaciona las siguientes gráficas de parábolas con las funciones correspondientes, justificando la respuesta:") + G(g4, 7)
    + tasks(4, ['$y=(x-3)^2$', r'$y=(x-2)\cdot(x+1)$', '$y=-x^2-4x-2$', r'$y=-\frac12x^2+3x-1$']),
    tasks(1, [T(r"\rest{a) $\leftrightarrow i$}: $(x-3)^2=0$ només en $x=3$: toca l'eix $OX$ en $(3,0)$, que és el vèrtex.", r"\rest{a) $\leftrightarrow i$}: $(x-3)^2=0$ solo en $x=3$: toca el eje $OX$ en $(3,0)$, que es el vértice."),
              T(r"\rest{b) $\leftrightarrow g$}: branques cap amunt i talls amb $OX$ en $x=2$ i $x=-1$; $OY$: $(0,-2)$.", r"\rest{b) $\leftrightarrow g$}: ramas hacia arriba y cortes con $OX$ en $x=2$ y $x=-1$; $OY$: $(0,-2)$."),
              T(r"\rest{c) $\leftrightarrow f$}: branques cap avall i vèrtex $V_x=\frac{4}{-2}=-2$, $V_y=2$.", r"\rest{c) $\leftrightarrow f$}: ramas hacia abajo y vértice $V_x=\frac{4}{-2}=-2$, $V_y=2$."),
              T(r"\rest{d) $\leftrightarrow h$}: branques cap avall, més oberta ($|a|=\frac12$), amb vèrtex $V_x=\frac{-3}{-1}=3$, $V_y=\frac72$.", r"\rest{d) $\leftrightarrow h$}: ramas hacia abajo, más abierta ($|a|=\frac12$), con vértice $V_x=\frac{-3}{-1}=3$, $V_y=\frac72$.")])))
ckroots('x**2-2*x-3-(x-3)', [0, 3])
X.append(E(3, T(r"Troba els punts on es tallen la paràbola $y=x^2-2x-3$ i la recta $y=x-3$. Representa-les per a comprovar-ho.", r"Halla los puntos donde se cortan la parábola $y=x^2-2x-3$ y la recta $y=x-3$. Represéntalas para comprobarlo."),
    r'$x^2-2x-3=x-3\Rightarrow x^2-3x=0\Rightarrow x(x-3)=0\Rightarrow x=0,\ x=3$: \ $\res{(0,-3)}$ ' + I_ + r' $\res{(3,0)}$' + G(Plot(-3, 5, -5, 5, W=200).fn(lambda t: t * t - 2 * t - 3).fn(lambda t: t - 3, col='b').dot(0, -3, 'v').dot(3, 0, 'v'), 3.6)))

# =====================================================================
# 5. Funcions radicals
X = sec(T('Funcions radicals', 'Funciones radicales'))
X.append(E(1, T(r"Completa la taula de valors de $y=\sqrt x$ i representa la funció. Quins són el domini i el recorregut? És creixent o decreixent?", r"Completa la tabla de valores de $y=\sqrt x$ y representa la función. ¿Cuáles son el dominio y el recorrido? ¿Es creciente o decreciente?")
    + TB(r'$x$ & $0$ & $1$ & $4$ & $9$ & $16$', r'$y$ & & & & & ', 5),
    TB(r'$x$ & $0$ & $1$ & $4$ & $9$ & $16$', r'$y$ & $\res{0}$ & $\res{1}$ & $\res{2}$ & $\res{3}$ & $\res{4}$', 5)
    + G(Plot(-1, 17, -1, 5, sx=2, lx=2, W=240).fn(sq, 0, 17).dot(0, 0, 'b').dot(1, 1, 'b').dot(4, 2, 'b').dot(9, 3, 'b').dot(16, 4, 'b'), 3.8)
    + T(r"$D=\res{[0,+\infty)}$, $R=\res{[0,+\infty)}$; \rest{creixent} (cada vegada més a poc a poc).", r"$D=\res{[0,+\infty)}$, $R=\res{[0,+\infty)}$; \rest{creciente} (cada vez más despacio).")))
X.append(E(1, T(r"Calcula el domini de les funcions:", r"Calcula el dominio de las funciones:") + tasks(4, [r'$y=\sqrt{x-5}$', r'$y=\sqrt{x+3}$', r'$y=\sqrt{2x-6}$', r'$y=\sqrt{4-x}$'])
    + recorda(T(r"el radicand d'una arrel quadrada no pot ser negatiu: ha de ser $\geq0$.", r"el radicando de una raíz cuadrada no puede ser negativo: debe ser $\geq0$.")),
    tasks(2, [r'$x-5\geq0\Rightarrow D=\res{[5,+\infty)}$', r'$x+3\geq0\Rightarrow D=\res{[-3,+\infty)}$', r'$2x-6\geq0\Rightarrow x\geq3\Rightarrow D=\res{[3,+\infty)}$', r'$4-x\geq0\Rightarrow x\leq4\Rightarrow D=\res{(-\infty,4]}$'])))
R26 = [(r'\sqrt{x-2}', lambda t: sq(t - 2), (2, 0), '[2,+\\infty)', '[0,+\\infty)'), (r'\sqrt x+1', lambda t: sq(t) + 1 if t >= 0 else None, (0, 1), '[0,+\\infty)', '[1,+\\infty)'),
       (r'\sqrt{x+3}-2', lambda t: sq(t + 3) - 2 if t >= -3 else None, (-3, -2), '[-3,+\\infty)', '[-2,+\\infty)'), (r'-\sqrt{x-1}', lambda t: -sq(t - 1) if t >= 1 else None, (1, 0), '[1,+\\infty)', '(-\\infty,0]')]
ok(all(abs(r[1](r[2][0]) - r[2][1]) < 1e-12 for r in R26))
X.append(E(2, T(r"Indica el punt on comença cada gràfica, el domini i el recorregut, i representa-les amb una taula de valors:", r"Indica el punto donde empieza cada gráfica, el dominio y el recorrido, y represéntalas con una tabla de valores:")
    + tasks(4, ['$y=%s$' % r[0] for r in R26]),
    tasks(2, [Gi(Plot(-4, 8, -4, 5, W=180, lx=2, ly=2).fn(r[1], r[2][0], 8, n=600).dot(*r[2], 'b'), 2.9) + r'\\[2pt]$\res{(%d,%d)}$\\[1pt] $D=\res{%s}$, $R=\res{%s}$' % (r[2] + (r[3], r[4])) for r in R26])))
X.append(E(2, T(r"Escriu l'expressió de la funció que s'obté en desplaçar la gràfica de $y=\sqrt x$:", r"Escribe la expresión de la función que se obtiene al desplazar la gráfica de $y=\sqrt x$:") + tasks(1, [
    T("4 unitats cap avall.", "4 unidades hacia abajo."), T("2 unitats cap a l'esquerra.", "2 unidades hacia la izquierda."),
    T("3 unitats cap a la dreta i 1 cap amunt.", "3 unidades hacia la derecha y 1 hacia arriba.")]),
    tasks(3, [r'$\res{y=\sqrt x-4}$', r'$\res{y=\sqrt{x+2}}$', r'$\res{y=\sqrt{x-3}+1}$'])))
ok(math.sqrt(0 + 4) == 2 and math.sqrt(5 + 4) == 3 and 25 - 4 == 21)
X.append(E(2, T(r"Donada la funció $f(x)=\sqrt{x+4}$, calcula $f(0)$, $f(5)$, $f(-4)$ i $f(-5)$. Quin valor de $x$ té per imatge 5?", r"Dada la función $f(x)=\sqrt{x+4}$, calcula $f(0)$, $f(5)$, $f(-4)$ y $f(-5)$. ¿Qué valor de $x$ tiene por imagen 5?"),
    r'$f(0)=\sqrt4=\res{2}$; \ $f(5)=\sqrt9=\res{3}$; \ $f(-4)=\sqrt0=\res{0}$; \ $f(-5)=\sqrt{-1}$: \rest{%s}. \ $\sqrt{x+4}=5\Rightarrow x+4=25\Rightarrow\res{x=21}$' % T('no existeix', 'no existe')))

# =====================================================================
# 6. Funcions de proporcionalitat inversa
X = sec(T('Funcions de proporcionalitat inversa', 'Funciones de proporcionalidad inversa'))
X.append(E(1, T(r"Les magnituds $x$ i $y$ són inversament proporcionals. Completa la taula, escriu la funció que les relaciona i representa-la per a $x>0$.", r"Las magnitudes $x$ e $y$ son inversamente proporcionales. Completa la tabla, escribe la función que las relaciona y represéntala para $x>0$.")
    + TB(r'$x$ & $1$ & $2$ & $3$ & $4$ & $6$ & $12$', r'$y$ & & $6$ & & & & ', 6),
    r"$k=x\cdot y=2\cdot6=12$: \ $\res{y=\dfrac{12}{x}}$" + TB(r'$x$ & $1$ & $2$ & $3$ & $4$ & $6$ & $12$', r'$y$ & $\res{12}$ & $6$ & $\res{4}$ & $\res{3}$ & $\res{2}$ & $\res{1}$', 6)
    + G(Plot(-1, 13, -1, 13, W=220, lx=2, ly=2).fn(lambda t: 12 / t, .5, 13).dot(1, 12, 'b').dot(2, 6, 'b').dot(3, 4, 'b').dot(4, 3, 'b').dot(6, 2, 'b').dot(12, 1, 'b'), 4)))
def hy(f, av, ah, W=180): return Plot(-6, 6, -6, 6, W=W, lx=2, ly=2).fn(f, n=1200).vl(av).hl(ah)
X.append(E(1, T(r"Representa les funcions $y=\dfrac4x$ i $y=-\dfrac2x$ fent una taula de valors. Indica'n el domini, el recorregut, les asímptotes i si són creixents o decreixents.", r"Representa las funciones $y=\dfrac4x$ e $y=-\dfrac2x$ haciendo una tabla de valores. Indica su dominio, el recorrido, las asíntotas y si son crecientes o decrecientes."),
    tasks(2, [Gi(hy(lambda t: 4 / t if t else None, 0, 0), 3.2) + r'\\[2pt]$y=\frac4x$: $D=R=\res{%s-\{0\}}$; \rest{%s} ' % (IR, DEC) + T('a cada branca', 'en cada rama'),
              Gi(hy(lambda t: -2 / t if t else None, 0, 0), 3.2) + r'\\[2pt]$y=-\frac2x$: $D=R=\res{%s-\{0\}}$; \rest{%s} ' % (IR, CRE) + T('a cada branca', 'en cada rama')])
    + T(r"Totes dues tenen les asímptotes $\res{x=0}$ i $\res{y=0}$ (els eixos).", r"Las dos tienen las asíntotas $\res{x=0}$ e $\res{y=0}$ (los ejes).")))
ok(all(a * b == 12 for a, b in [(1, 12), (2, 6), (3, 4), (6, 2)]) and all(5 * a == b for a, b in [(1, 5), (2, 10), (3, 15), (4, 20)])
   and all(2 * a + 1 == b for a, b in [(1, 3), (2, 5), (4, 9), (5, 11)]) and all(a * b == 20 for a, b in [(2, 10), (4, 5), (5, 4), (10, 2)]))
X.append(E(1, T(r"Digues si cada taula correspon a una proporcionalitat directa, a una proporcionalitat inversa o a cap de les dues, i escriu-ne la fórmula:", r"Di si cada tabla corresponde a una proporcionalidad directa, a una proporcionalidad inversa o a ninguna de las dos, y escribe su fórmula:")
    + tasks(2, [TB(r'$x$ & $1$ & $2$ & $3$ & $6$', r'$y$ & $12$ & $6$ & $4$ & $2$', 4), TB(r'$x$ & $1$ & $2$ & $3$ & $4$', r'$y$ & $5$ & $10$ & $15$ & $20$', 4),
                TB(r'$x$ & $1$ & $2$ & $4$ & $5$', r'$y$ & $3$ & $5$ & $9$ & $11$', 4), TB(r'$x$ & $2$ & $4$ & $5$ & $10$', r'$y$ & $10$ & $5$ & $4$ & $2$', 4)]),
    tasks(2, [T(r"$x\cdot y=12$: \rest{inversa}, $\res{y=\frac{12}{x}}$", r"$x\cdot y=12$: \rest{inversa}, $\res{y=\frac{12}{x}}$"), T(r"$\frac yx=5$: \rest{directa}, $\res{y=5x}$", r"$\frac yx=5$: \rest{directa}, $\res{y=5x}$"),
              T(r"\rest{Cap de les dues}: és afí, $\res{y=2x+1}$", r"\rest{Ninguna de las dos}: es afín, $\res{y=2x+1}$"), T(r"$x\cdot y=20$: \rest{inversa}, $\res{y=\frac{20}{x}}$", r"$x\cdot y=20$: \rest{inversa}, $\res{y=\frac{20}{x}}$")])))
ok(-6 / -4 == 1.5 and -6 / -.5 == 12)
X.append(E(2, T(r"La gràfica de la funció $f(x)=\dfrac kx$ passa pel punt $(2,-3)$. Troba $k$, calcula $f(-4)$ i troba el valor de $x$ per al qual $f(x)=12$.", r"La gráfica de la función $f(x)=\dfrac kx$ pasa por el punto $(2,-3)$. Halla $k$, calcula $f(-4)$ y halla el valor de $x$ para el que $f(x)=12$."),
    r'$k=x\cdot y=2\cdot(-3)=\res{-6}$: $f(x)=-\dfrac6x$. \ $f(-4)=\res{\frac32}$. \ $-\dfrac6x=12\Rightarrow\res{x=-\frac12}$'))
X.append(E(2, T(r"Quines d'aquestes funcions són de proporcionalitat inversa? Per a les que ho siguen, indica si són creixents o decreixents a cada branca.", r"¿Cuáles de estas funciones son de proporcionalidad inversa? Para las que lo sean, indica si son crecientes o decrecientes en cada rama.")
    + tasks(4, [r'$y=\dfrac5x$', r'$y=\dfrac x5$', r'$x\cdot y=-8$', '$y=5-x$']),
    tasks(2, [T(r"\rest{Sí} ($k=5>0$): decreixent", r"\rest{Sí} ($k=5>0$): decreciente"), T(r"\rest{No}: és de proporcionalitat directa ($y=\frac15x$)", r"\rest{No}: es de proporcionalidad directa ($y=\frac15x$)"),
              T(r"\rest{Sí}: $y=-\frac8x$ ($k=-8<0$): creixent", r"\rest{Sí}: $y=-\frac8x$ ($k=-8<0$): creciente"), T(r"\rest{No}: és afí", r"\rest{No}: es afín")])))

# =====================================================================
# 7. Translacions de la funció de proporcionalitat inversa
X = sec(T('Translacions de la funció de proporcionalitat inversa', 'Traslaciones de la función de proporcionalidad inversa'))
H14 = [(r'\dfrac{2}{x-3}', lambda t: 2 / (t - 3) if t != 3 else None, 3, 0, 2), (r'\dfrac1x+2', lambda t: 1 / t + 2 if t else None, 0, 2, 1),
       (r'\dfrac{-3}{x+1}', lambda t: -3 / (t + 1) if t != -1 else None, -1, 0, -3), (r'\dfrac{4}{x-2}-1', lambda t: 4 / (t - 2) - 1 if t != 2 else None, 2, -1, 4)]
def brace(v): return IR + r'-\{%d\}' % v
X.append(E(1, T(r"Indica les asímptotes, el domini i el recorregut d'aquestes hipèrboles, digues si són creixents o decreixents i representa-les:", r"Indica las asíntotas, el dominio y el recorrido de estas hipérbolas, di si son crecientes o decrecientes y represéntalas:")
    + tasks(4, ['$y=%s$' % h[0] for h in H14]) + recorda(T(r"l'asímptota vertical és on s'anul·la el denominador i l'horitzontal és el nombre que se suma a la fracció.", r"la asíntota vertical está donde se anula el denominador y la horizontal es el número que se suma a la fracción.")),
    tasks(2, [Gi(hy(h[1], h[2], h[3]), 3.1) + r'\\[2pt]$\res{x=%d}$, $\res{y=%d}$; \rest{%s}\\[1pt] $D=\res{%s}$, $R=\res{%s}$' % (h[2], h[3], DEC if h[4] > 0 else CRE, brace(h[2]), brace(h[3])) for h in H14])))
X.append(E(1, T(r"Explica com s'obté la gràfica de cada funció a partir de la de $y=\dfrac3x$:", r"Explica cómo se obtiene la gráfica de cada función a partir de la de $y=\dfrac3x$:") + tasks(4, [r'$y=\dfrac3x+4$', r'$y=\dfrac3{x-5}$', r'$y=\dfrac3{x+2}$', r'$y=\dfrac3{x+1}-3$']),
    tasks(2, [T(r"\rest{4 cap amunt}", r"\rest{4 hacia arriba}"), T(r"\rest{5 cap a la dreta}", r"\rest{5 hacia la derecha}"),
              T(r"\rest{2 cap a l'esquerra}", r"\rest{2 hacia la izquierda}"), T(r"\rest{1 cap a l'esquerra i 3 cap avall}", r"\rest{1 hacia la izquierda y 3 hacia abajo}")])))
X.append(E(2, T(r"Escriu l'expressió de la funció que s'obté en desplaçar la gràfica de $y=\dfrac2x$:", r"Escribe la expresión de la función que se obtiene al desplazar la gráfica de $y=\dfrac2x$:") + tasks(1, [
    T("3 unitats cap a la dreta.", "3 unidades hacia la derecha."), T("1 unitat cap avall.", "1 unidad hacia abajo."), T("4 unitats cap a l'esquerra i 2 cap amunt.", "4 unidades hacia la izquierda y 2 hacia arriba.")]),
    tasks(3, [r'$\res{y=\dfrac2{x-3}}$', r'$\res{y=\dfrac2x-1}$', r'$\res{y=\dfrac2{x+4}+2}$'])))
h36 = lambda t: 2 / (t - 1) + 1 if t != 1 else None
ok([h36(t) for t in (-3, -1, 0, 2, 3, 5)] == [.5, 0, -1, 3, 2, 1.5])
X.append(E(2, T(r"Representa $f(x)=\dfrac{2}{x-1}+1$: dibuixa primer les asímptotes i després fes una taula de valors a banda i banda de l'asímptota vertical. On talla els eixos?", r"Representa $f(x)=\dfrac{2}{x-1}+1$: dibuja primero las asíntotas y después haz una tabla de valores a ambos lados de la asíntota vertical. ¿Dónde corta los ejes?"),
    T(r"Asímptotes: $\res{x=1}$ i $\res{y=1}$ (és $y=\frac2x$ desplaçada 1 cap a la dreta i 1 cap amunt).", r"Asíntotas: $\res{x=1}$ e $\res{y=1}$ (es $y=\frac2x$ desplazada 1 hacia la derecha y 1 hacia arriba).")
    + TB(r'$x$ & $-3$ & $-1$ & $0$ & $2$ & $3$ & $5$', r'$y$ & $0{,}5$ & $0$ & $-1$ & $3$ & $2$ & $1{,}5$', 6)
    + G(Plot(-5, 7, -4, 6, W=220, lx=2, ly=2).fn(h36, n=1500).vl(1).hl(1).dot(-1, 0, 'b').dot(0, -1, 'b').dot(2, 3, 'b').dot(3, 2, 'b'), 3.6)
    + T(r"$OX$: $\res{(-1,0)}$; \ $OY$: $\res{(0,-1)}$. \ $D=\res{%s-\{1\}}$, $R=\res{%s-\{1\}}$; \rest{decreixent} a cada branca.", r"$OX$: $\res{(-1,0)}$; \ $OY$: $\res{(0,-1)}$. \ $D=\res{%s-\{1\}}$, $R=\res{%s-\{1\}}$; \rest{decreciente} en cada rama.") % (IR, IR)))
h15 = lambda t: 2 / (t - 1) + 3 if t != 1 else None
ok(h15(2) == 5 and h15(3) == 4 and h15(0) == 1 and h15(-1) == 2)
X.append(E(3, T(r"La gràfica següent és una hipèrbola del tipus $y=\dfrac{k}{x-a}+b$. Troba'n les asímptotes i l'expressió.", r"La gráfica siguiente es una hipérbola del tipo $y=\dfrac{k}{x-a}+b$. Halla sus asíntotas y su expresión.")
    + G(Plot(-4, 6, -2, 8, W=240).fn(h15, n=1200).vl(1).hl(3).dot(2, 5, 'b').dot(3, 4, 'b').dot(0, 1, 'b'), 4.4),
    T(r"Asímptotes $\res{x=1}$ i $\res{y=3}$: $a=1$, $b=3$. Passa per $(2,5)$: $\frac{k}{2-1}+3=5\Rightarrow k=2$: \ $\res{y=\dfrac{2}{x-1}+3}$ (comprovació: $f(3)=4$, $f(0)=1$).",
      r"Asíntotas $\res{x=1}$ e $\res{y=3}$: $a=1$, $b=3$. Pasa por $(2,5)$: $\frac{k}{2-1}+3=5\Rightarrow k=2$: \ $\res{y=\dfrac{2}{x-1}+3}$ (comprobación: $f(3)=4$, $f(0)=1$).")))

# =====================================================================
# 8. Funcions exponencials
X = sec(T('Funcions exponencials', 'Funciones exponenciales'))
TE = r"\begin{center}\renewcommand{\arraystretch}{1.3}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $-2$ & $-1$ & $0$ & $1$ & $2$\\\hline %s\\\hline %s\\\hline\end{tabular}\end{center}"
X.append(E(1, T(r"Completa la taula de valors i representa en uns mateixos eixos $y=3^x$ i $y=\left(\frac13\right)^x$. Indica'n el domini, el recorregut, l'asímptota i si són creixents o decreixents.",
                r"Completa la tabla de valores y representa en unos mismos ejes $y=3^x$ e $y=\left(\frac13\right)^x$. Indica su dominio, el recorrido, la asíntota y si son crecientes o decrecientes.")
    + TE % (r'$3^x$ & & & & & ', r'$\left(\frac13\right)^x$ & & & & & '),
    TE % (r'$3^x$ & $\res{\frac19}$ & $\res{\frac13}$ & $\res{1}$ & $\res{3}$ & $\res{9}$', r'$\left(\frac13\right)^x$ & $\res{9}$ & $\res{3}$ & $\res{1}$ & $\res{\frac13}$ & $\res{\frac19}$')
    + G(Plot(-4, 4, -1, 10, W=220, ly=2).fn(lambda t: 3 ** t).fn(lambda t: 3 ** -t, col='b').dot(0, 1, 'v'), 4)
    + T(r"Totes dues: $D=\res{%s}$, $R=\res{(0,+\infty)}$, asímptota horitzontal $\res{y=0}$ i passen per $(0,1)$. $y=3^x$ és \rest{creixent} i $y=\left(\frac13\right)^x$, \rest{decreixent}.",
        r"Ambas: $D=\res{%s}$, $R=\res{(0,+\infty)}$, asíntota horizontal $\res{y=0}$ y pasan por $(0,1)$. $y=3^x$ es \rest{creciente} e $y=\left(\frac13\right)^x$, \rest{decreciente}.") % IR))
X.append(E(1, T(r"Sense dibuixar-les, digues si aquestes funcions exponencials són creixents o decreixents:", r"Sin dibujarlas, di si estas funciones exponenciales son crecientes o decrecientes:") + tasks(4, ['$y=5^x$', '$y=0{,}4^x$', r'$y=\left(\frac32\right)^x$', r'$y=\left(\frac14\right)^x$']),
    tasks(2, [r'\rest{%s}' % CRE.capitalize() + ' ($a>1$)', r'\rest{%s}' % DEC.capitalize() + ' ($a<1$)', r'\rest{%s}' % CRE.capitalize() + ' ($a>1$)', r'\rest{%s}' % DEC.capitalize() + ' ($a<1$)'])))
X.append(E(1, T(r"Per quin nombre es multiplica cada any una quantitat que…", r"¿Por qué número se multiplica cada año una cantidad que…") + tasks(2, [
    T("augmenta un 6 \\%?", "aumenta un 6 \\%?"), T("disminueix un 25 \\%?", "disminuye un 25 \\%?"), T("es duplica?", "se duplica?"), T("es redueix a la meitat?", "se reduce a la mitad?")]),
    tasks(4, [r'$1+\frac{6}{100}=\res{1{,}06}$', r'$1-\frac{25}{100}=\res{0{,}75}$', r'$\res{2}$', r'$\res{0{,}5}$'])))
ok(2 ** 5 == 32 and F(2) ** -3 == F(1, 8) and 2 ** 6 == 64 and F(2) ** -2 == F(1, 4))
X.append(E(2, T(r"Donada la funció $f(x)=2^x$, calcula $f(5)$, $f(-3)$ i $f(0)$. Quin valor de $x$ té per imatge 64? I $\frac14$?", r"Dada la función $f(x)=2^x$, calcula $f(5)$, $f(-3)$ y $f(0)$. ¿Qué valor de $x$ tiene por imagen 64? ¿Y $\frac14$?"),
    r'$f(5)=\res{32}$; \ $f(-3)=\frac1{2^3}=\res{\frac18}$; \ $f(0)=\res{1}$. \ $2^x=64=2^6\Rightarrow\res{x=6}$; \ $2^x=\frac14=2^{-2}\Rightarrow\res{x=-2}$'))
ok(3 ** 2 == 9 and F(1, 4) ** -1 == 4 and 5 * 2 ** 3 == 40)
X.append(E(2, T(r"Troba el valor de la lletra en cada cas:", r"Halla el valor de la letra en cada caso:") + tasks(1, [
    T(r"La funció $y=a^x$ passa pel punt $(2,9)$.", r"La función $y=a^x$ pasa por el punto $(2,9)$."), T(r"La funció $y=a^x$ passa pel punt $(-1,4)$.", r"La función $y=a^x$ pasa por el punto $(-1,4)$."),
    T(r"La funció $y=C\cdot2^x$ passa pel punt $(3,40)$.", r"La función $y=C\cdot2^x$ pasa por el punto $(3,40)$.")]),
    tasks(3, [r'$a^2=9\Rightarrow\res{a=3}$', r'$a^{-1}=4\Rightarrow\res{a=\frac14}$', r'$C\cdot2^3=40\Rightarrow\res{C=5}$'])))

# =====================================================================
# 9. Problemes amb funcions
X = sec(T('Problemes amb funcions', 'Problemas con funciones'))
X.append(E(1, T(r"Indica quin tipus de funció descriu cada situació i escriu-ne l'expressió:", r"Indica qué tipo de función describe cada situación y escribe su expresión:") + tasks(1, [
    T(r"El preu d'entrar a una fira que cobra 5 € per l'entrada i 2 € per cada atracció ($x$ atraccions).", r"El precio de entrar en una feria que cobra 5 € por la entrada y 2 € por cada atracción ($x$ atracciones)."),
    T(r"El temps que es tarda a recórrer 300 km segons la velocitat $x$ (en km/h).", r"El tiempo que se tarda en recorrer 300 km según la velocidad $x$ (en km/h)."),
    T(r"L'àrea d'un quadrat de costat $x$.", r"El área de un cuadrado de lado $x$."),
    T(r"El costat d'un quadrat d'àrea $x$.", r"El lado de un cuadrado de área $x$."),
    T(r"El nombre de seguidors d'un compte que en té 100 i es duplica cada mes ($x$ mesos).", r"El número de seguidores de una cuenta que tiene 100 y se duplica cada mes ($x$ meses).")]),
    tasks(2, [T('Afí', 'Afín') + r': $\res{y=2x+5}$', T('Proporcionalitat inversa', 'Proporcionalidad inversa') + r': $\res{y=\dfrac{300}{x}}$', T('Quadràtica', 'Cuadrática') + r': $\res{y=x^2}$',
              'Radical' + r': $\res{y=\sqrt x}$', 'Exponencial' + r': $\res{y=100\cdot2^x}$'])))
ok(abs(1.2 * 8 + 3.5 - 13.1) < 1e-9 and abs((21.5 - 3.5) / 1.2 - 15) < 1e-9)
X.append(E(1, T(r"Un taxi cobra 3,50 € per la baixada de bandera i 1,20 € per cada quilòmetre. Escriu la funció que dona el preu segons els quilòmetres recorreguts. Quant costa un trajecte de 8 km? Quants quilòmetres s'han fet si s'han pagat 21,50 €?",
                r"Un taxi cobra 3,50 € por la bajada de bandera y 1,20 € por cada kilómetro. Escribe la función que da el precio según los kilómetros recorridos. ¿Cuánto cuesta un trayecto de 8 km? ¿Cuántos kilómetros se han hecho si se han pagado 21,50 €?"),
    r'$\res{P(x)=1{,}2x+3{,}5}$. \ $P(8)=9{,}6+3{,}5=\res{13{,}10\text{ €}}$. \ $1{,}2x+3{,}5=21{,}5\Rightarrow x=\dfrac{18}{1{,}2}=\res{15\text{ km}}$'))
ok(20 + 25 * 2 == 35 * 2 and 20 + 25 * 12 == 320 and 35 * 12 == 420)
X.append(E(2, T(r"El gimnàs A cobra 20 € de matrícula i 25 € cada mes. El gimnàs B no cobra matrícula, però la quota és de 35 € cada mes. Escriu la funció que dona el que s'ha pagat en total en cada gimnàs al cap de $x$ mesos. Quan s'ha pagat el mateix? Quin convé més per a un any sencer?",
                r"El gimnasio A cobra 20 € de matrícula y 25 € cada mes. El gimnasio B no cobra matrícula, pero la cuota es de 35 € cada mes. Escribe la función que da lo que se ha pagado en total en cada gimnasio al cabo de $x$ meses. ¿Cuándo se ha pagado lo mismo? ¿Cuál conviene más para un año entero?"),
    r'$\res{A(x)=25x+20}$ (' + T('afí', 'afín') + r'), \ $\res{B(x)=35x}$ (' + T('proporcionalitat directa', 'proporcionalidad directa') + r'). \ $25x+20=35x\Rightarrow\res{x=2}$ ' + T('mesos (70 €). Per a un any:', 'meses (70 €). Para un año:') + r' $A(12)=320$ €, $B(12)=420$ €: ' + T(r'convé \rest{el gimnàs A}.', r'conviene \rest{el gimnasio A}.')
    + G(Plot(-.5, 13, -20, 460, sx=1, sy=50, lx=2, ly=100, W=230).fn(lambda t: 25 * t + 20, 0, 13, 'o').fn(lambda t: 35 * t, 0, 13, 'b').dot(2, 70, 'v'), 3.4)))
h37 = lambda t: -5 * t * t + 30 * t
ok(h37(3) == 45 and h37(6) == 0 and h37(1) == 25 and h37(5) == 25)
X.append(E(2, T(r"Llancem una pilota cap amunt des de terra. La seua altura (en metres) al cap de $t$ segons és $h(t)=-5t^2+30t$.", r"Lanzamos una pelota hacia arriba desde el suelo. Su altura (en metros) al cabo de $t$ segundos es $h(t)=-5t^2+30t$.")
    + items(T("Quina altura màxima assoleix i en quin instant?", "¿Qué altura máxima alcanza y en qué instante?"), T("Quan torna a terra?", "¿Cuándo vuelve al suelo?"), T("En quins instants està a 25 m d'altura?", "¿En qué instantes está a 25 m de altura?")),
    items(T(r"Paràbola $\cap$: el màxim és el vèrtex. $t=\frac{-30}{-10}=3$, $h(3)=-45+90=45$: \rest{45 m als 3 s}.", r"Parábola $\cap$: el máximo es el vértice. $t=\frac{-30}{-10}=3$, $h(3)=-45+90=45$: \rest{45 m a los 3 s}."),
          r"$-5t^2+30t=0\Rightarrow-5t(t-6)=0\Rightarrow\res{t=6\text{ s}}$",
          r"$-5t^2+30t=25\Rightarrow t^2-6t+5=0\Rightarrow\res{t=1\text{ s}}$ " + I_ + r" $\res{t=5\text{ s}}$")))
ok(9 * (18 - 9) == 81 and vert(-1, 18, 0) == (9, 81))
X.append(E(2, T(r"De tots els rectangles de perímetre 36 cm, quin té l'àrea més gran? (Si un costat mesura $x$, quant mesura l'altre?)", r"De todos los rectángulos de perímetro 36 cm, ¿cuál tiene el área más grande? (Si un lado mide $x$, ¿cuánto mide el otro?)"),
    T(r"L'altre costat mesura $18-x$: $\res{A(x)=x(18-x)=-x^2+18x}$. Paràbola $\cap$, vèrtex en $x=\frac{-18}{-2}=9$: \rest{el quadrat de 9 cm de costat}, amb $A(9)=\res{81\text{ cm}^2}$.",
      r"El otro lado mide $18-x$: $\res{A(x)=x(18-x)=-x^2+18x}$. Parábola $\cap$, vértice en $x=\frac{-18}{-2}=9$: \rest{el cuadrado de 9 cm de lado}, con $A(9)=\res{81\text{ cm}^2}$.")))
ok(15 * (60 - 30) == 450 and vert(-2, 60, 0) == (15, 450))
X.append(E(3, T(r"Amb 60 m de tanca volem tancar un hort rectangular aprofitant una paret (només cal tancar tres costats). Si els dos costats perpendiculars a la paret mesuren $x$ metres, escriu la funció que dona l'àrea de l'hort. Quines dimensions fan que l'àrea siga màxima? Quant val?",
                r"Con 60 m de valla queremos cerrar un huerto rectangular aprovechando una pared (solo hay que cerrar tres lados). Si los dos lados perpendiculares a la pared miden $x$ metros, escribe la función que da el área del huerto. ¿Qué dimensiones hacen que el área sea máxima? ¿Cuánto vale?"),
    T(r"El costat paral·lel a la paret mesura $60-2x$: $\res{A(x)=x(60-2x)=-2x^2+60x}$. Vèrtex: $x=\frac{-60}{-4}=15$: \rest{15 m $\times$ 30 m}, amb una àrea de $A(15)=\res{450\text{ m}^2}$.",
      r"El lado paralelo a la pared mide $60-2x$: $\res{A(x)=x(60-2x)=-2x^2+60x}$. Vértice: $x=\frac{-60}{-4}=15$: \rest{15 m $\times$ 30 m}, con un área de $A(15)=\res{450\text{ m}^2}$.")))
ok(60 / 4 == 15 and 60 / 5 == 12)
X.append(E(2, T(r"Sis pintors tarden 10 dies a pintar un edifici. Escriu la funció que dona els dies que tardarien $n$ pintors treballant al mateix ritme. Quant tardarien 4 pintors? Quants pintors calen per a acabar en 5 dies?",
                r"Seis pintores tardan 10 días en pintar un edificio. Escribe la función que da los días que tardarían $n$ pintores trabajando al mismo ritmo. ¿Cuánto tardarían 4 pintores? ¿Cuántos pintores hacen falta para acabar en 5 días?"),
    r'$k=6\cdot10=60$: \ $\res{t(n)=\dfrac{60}{n}}$ (' + T('proporcionalitat inversa', 'proporcionalidad inversa') + r'). \ $t(4)=\res{15}$ ' + T('dies', 'días') + r'. \ $\dfrac{60}{n}=5\Rightarrow\res{n=12}$ ' + T('pintors', 'pintores') + '.'))
ok(math.sqrt(20 * 5) == 10 and math.sqrt(20 * 20) == 20 and math.sqrt(20 * 45) == 30 and 40 ** 2 / 20 == 80)
X.append(E(2, T(r"La velocitat (en m/s) amb què arriba a terra un objecte que cau des d'una altura de $h$ metres és, aproximadament, $v(h)=\sqrt{20h}$. Amb quina velocitat arriba si cau des de 5 m? I des de 20 m i 45 m? Des de quina altura ha caigut si arriba a 40 m/s?",
                r"La velocidad (en m/s) con que llega al suelo un objeto que cae desde una altura de $h$ metros es, aproximadamente, $v(h)=\sqrt{20h}$. ¿Con qué velocidad llega si cae desde 5 m? ¿Y desde 20 m y 45 m? ¿Desde qué altura ha caído si llega a 40 m/s?"),
    r'$v(5)=\sqrt{100}=\res{10\text{ m/s}}$; \ $v(20)=\sqrt{400}=\res{20\text{ m/s}}$; \ $v(45)=\sqrt{900}=\res{30\text{ m/s}}$. \ $\sqrt{20h}=40\Rightarrow20h=1\,600\Rightarrow\res{h=80\text{ m}}$. '
    + T("Fixa't que per a duplicar la velocitat cal quadruplicar l'altura.", "Fíjate en que para duplicar la velocidad hay que cuadruplicar la altura.")))
ok(200 * 2 ** 5 == 6400 and 200 * 2 ** 8 == 51200)
X.append(E(2, T(r"Un cultiu té 200 bacteris i es duplica cada hora. Escriu la funció que dona el nombre de bacteris al cap de $t$ hores. Quants n'hi haurà al cap de 5 hores? Quant de temps ha de passar perquè n'hi haja 51 200?",
                r"Un cultivo tiene 200 bacterias y se duplica cada hora. Escribe la función que da el número de bacterias al cabo de $t$ horas. ¿Cuántas habrá al cabo de 5 horas? ¿Cuánto tiempo tiene que pasar para que haya 51 200?"),
    r'$\res{N(t)=200\cdot2^t}$. \ $N(5)=200\cdot32=\res{6\,400}$. \ $200\cdot2^t=51\,200\Rightarrow2^t=256=2^8\Rightarrow\res{t=8\text{ h}}$'))
ok(round(5000 * 1.02 ** 3, 2) == 5306.04 and round(5000 * 1.02 ** 10, 2) == 6094.97)
X.append(E(2, T(r"Depositem 5 000 € en un compte que dona un 2 \% d'interés compost anual. Escriu la funció que dona el capital al cap de $t$ anys i calcula quant hi haurà al cap de 3 anys i de 10 anys.",
                r"Depositamos 5 000 € en una cuenta que da un 2 \% de interés compuesto anual. Escribe la función que da el capital al cabo de $t$ años y calcula cuánto habrá al cabo de 3 años y de 10 años."),
    T(r"Cada any el capital es multiplica per $1+\frac{2}{100}=1{,}02$: ", r"Cada año el capital se multiplica por $1+\frac{2}{100}=1{,}02$: ") + r'$\res{C(t)=5\,000\cdot1{,}02^t}$. \ $C(3)\approx\res{5\,306{,}04\text{ €}}$; \ $C(10)\approx\res{6\,094{,}97\text{ €}}$'))
ok(abs(18000 * .85 ** 2 - 13005) < 1e-6 and .85 ** 4 > .5 > .85 ** 5)
X.append(E(3, T(r"Un cotxe que val 18 000 € perd cada any el 15 \% del valor que tenia l'any anterior. Escriu la funció que dona el valor del cotxe al cap de $t$ anys. Quant valdrà d'ací a 2 anys? Quants anys han de passar perquè valga menys de la meitat?",
                r"Un coche que vale 18 000 € pierde cada año el 15 \% del valor que tenía el año anterior. Escribe la función que da el valor del coche al cabo de $t$ años. ¿Cuánto valdrá dentro de 2 años? ¿Cuántos años tienen que pasar para que valga menos de la mitad?"),
    T(r"Cada any es multiplica per $1-\frac{15}{100}=0{,}85$: ", r"Cada año se multiplica por $1-\frac{15}{100}=0{,}85$: ") + r'$\res{V(t)=18\,000\cdot0{,}85^t}$. \ $V(2)=\res{13\,005\text{ €}}$. \ '
    + T(r"Cal $0{,}85^t<0{,}5$. Provem amb la calculadora: $0{,}85^4\approx0{,}522$ i $0{,}85^5\approx0{,}444$: han de passar \rest{5 anys}.", r"Hace falta $0{,}85^t<0{,}5$. Probamos con la calculadora: $0{,}85^4\approx0{,}522$ y $0{,}85^5\approx0{,}444$: tienen que pasar \rest{5 años}.")))
ok(sp.expand((12 - x) * (200 + 40 * x)) == -40 * x ** 2 + 280 * x + 2400 and vert(-40, 280, 2400) == (F(7, 2), 2890) and 200 + 40 * 3.5 == 340)
X.append(E(3, T(r"Una botiga ven 200 samarretes al mes a 12 € cadascuna. Ha comprovat que, per cada euro que rebaixa el preu, en ven 40 més. Si rebaixa el preu $x$ euros, escriu la funció que dona els ingressos mensuals. Quin preu fa màxims els ingressos? Quants diners ingressa aleshores?",
                r"Una tienda vende 200 camisetas al mes a 12 € cada una. Ha comprobado que, por cada euro que rebaja el precio, vende 40 más. Si rebaja el precio $x$ euros, escribe la función que da los ingresos mensuales. ¿Qué precio hace máximos los ingresos? ¿Cuánto dinero ingresa entonces?"),
    T(r"Ingressos = preu $\times$ unitats: $\res{I(x)=(12-x)(200+40x)=-40x^2+280x+2\,400}$. Vèrtex: $x=\frac{-280}{-80}=3{,}5$: preu de \rest{8,50 €}, amb el qual ven 340 samarretes i ingressa $I(3{,}5)=\res{2\,890\text{ €}}$.",
      r"Ingresos = precio $\times$ unidades: $\res{I(x)=(12-x)(200+40x)=-40x^2+280x+2\,400}$. Vértice: $x=\frac{-280}{-80}=3{,}5$: precio de \rest{8,50 €}, con el que vende 340 camisetas e ingresa $I(3{,}5)=\res{2\,890\text{ €}}$.")))

PRE = r'''\usetikzlibrary{calc}
\usepackage{enumitem}
\definecolor{violet}{HTML}{7C3AED}
\definecolor{orange}{HTML}{EA8A1F}
'''
TIT = T('Funcions elementals', 'Funciones elementales')
build(HERE, 7, TIT, S,
      T("funcions lineals, proporcionalitat directa, funció afí, funció constant, pendent, equació punt-pendent, funció quadràtica, paràbola, vèrtex, funcions radicals, proporcionalitat inversa, hipèrbola, asímptotes, translacions, funció exponencial, problemes amb funcions",
        "funciones lineales, proporcionalidad directa, función afín, función constante, pendiente, ecuación punto-pendiente, función cuadrática, parábola, vértice, funciones radicales, proporcionalidad inversa, hipérbola, asíntotas, traslaciones, función exponencial, problemas con funciones"),
      T(r"Resol-los al quadern mostrant tots els passos i dibuixa les gràfiques en paper quadriculat. Escriu els intervals com als apunts: $(a,b)$ obert i $[a,b]$ tancat. Les seccions segueixen l'ordre dels apunts de la unitat (7.1--7.9).",
        r"Resuélvelos en el cuaderno mostrando todos los pasos y dibuja las gráficas en papel cuadriculado. Escribe los intervalos como en los apuntes: $(a,b)$ abierto y $[a,b]$ cerrado. Las secciones siguen el orden de los apuntes de la unidad (7.1--7.9)."),
      T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Pots comprovar les gràfiques amb les eines interactives dels apunts de la unitat (rectes, paràboles pas a pas, radicals, hipèrboles i exponencials).",
        r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar las gráficas con las herramientas interactivas de los apuntes de la unidad (rectas, parábolas paso a paso, radicales, hipérbolas y exponenciales)."),
      PRE, lang='es' if ES else 'va', curs='4eso-a')
