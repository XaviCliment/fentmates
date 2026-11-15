# Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (4t ESO Matemàtiques B, Unitat 8: Funcions elementals)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Recull TOTS els exercicis de la fitxa del departament («Fitxa 5 (3a Av.): Funcions 2», 8 exercicis; marcats amb (D) en aquest
# codi): rectes, paràboles, rectes i paràboles a partir de la gràfica, funcions a trossos (dibuixar-les i trobar-ne l'expressió),
# valor absolut i relacionar gràfiques amb funcions. Hi afig exercicis nous de cada família i una secció de problemes amb
# funcions (lineals, quadràtiques, de proporcionalitat inversa, a trossos i exponencials).
# Les 8 seccions segueixen els apartats dels apunts (8.1-8.8).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es). Les gràfiques es dibuixen amb la classe Plot de _eines/apunts/4eso-b-t7/fig.py.
# Els intervals s'escriuen com a la resta de 4t: (a,b) obert i [a,b] tancat. Els decimals, dins de les fórmules, amb {,}.
# Ús: python3 genera.py && pdflatex t8-fitxa-exercicis.tex (dues vegades) && pdflatex t8-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '4eso-b-t7'))
from eso4b import *
from fig import Plot, piece, sq, lg
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
def pw(*ps):
    """funció a trossos: pw((expressió, condició), ...)"""
    return r'\left\{\begin{array}{ll}' + r'\\[1pt] '.join(r'%s & \text{si }%s' % p for p in ps) + r'\end{array}\right.'
def ckroots(expr, sols, msg=''):
    got = sorted(sp.solve(sp.sympify(expr, locals={'x': x}), x), key=float)
    want = sorted([sp.sympify(s) for s in sols], key=float)
    ok(len(got) == len(want) and all(sp.simplify(a - b) == 0 for a, b in zip(got, want)), (msg, got, want))
def vert(a, b, c):
    """vèrtex de ax²+bx+c amb fraccions exactes"""
    vx = F(-b, 2 * a); return vx, a * vx * vx + b * vx + c
CRE, DEC = T('creixent', 'creciente'), T('decreixent', 'decreciente')
I_ = T('i', 'y')

S = []
def sec(title): S.append((title, [])); return S[-1][1]

# =====================================================================
# 1. Funcions lineals
X = sec(T('Funcions lineals', 'Funciones lineales'))
# (D1)
L1 = [('2x+1', lambda t: 2 * t + 1, (0, 1), (1, 3)), ('-x-2', lambda t: -t - 2, (0, -2), (-2, 0)), ('3x', lambda t: 3 * t, (0, 0), (1, 3)),
      ('-2x', lambda t: -2 * t, (0, 0), (1, -2)), ('-2', lambda t: -2, (0, -2), (3, -2)), ('0', lambda t: 0, (0, 0), (3, 0))]
for _, f, p, q in L1: ok(f(p[0]) == p[1] and f(q[0]) == q[1])
def lp(i): return Plot(-4, 4, -4, 4, W=180).fn(L1[i][1]).dot(*L1[i][2], 'b').dot(*L1[i][3], 'b')
X.append(E(1, T(r"Dibuixa les rectes següents:", r"Dibuja las rectas siguientes:") + tasks(3, ['$f(x)=%s$' % l[0] for l in L1])
    + recorda(T(r"per a dibuixar una recta n'hi ha prou amb dos punts: fes una taula de valors amb dos valors de $x$.", r"para dibujar una recta basta con dos puntos: haz una tabla de valores con dos valores de $x$.")),
    tasks(3, [Gi(lp(i), 2.6) + r'\\[2pt]$%s$, $%s$' % ('(%d,%d)' % L1[i][2], '(%d,%d)' % L1[i][3]) for i in range(6)])
    + T(r"La c) i la d) són de proporcionalitat directa (passen per l'origen); la e) i la f) són constants (la f) és l'eix $OX$).", r"La c) y la d) son de proporcionalidad directa (pasan por el origen); la e) y la f) son constantes (la f) es el eje $OX$).")))
X.append(E(1, T(r"Sense dibuixar-les, indica el pendent i l'ordenada en l'origen de cada recta, i digues si és creixent, decreixent o constant:", r"Sin dibujarlas, indica la pendiente y la ordenada en el origen de cada recta, y di si es creciente, decreciente o constante:")
    + tasks(4, ['$y=3x-5$', r'$y=-\dfrac x2+4$', '$y=7$', '$y=-4x$']),
    tasks(2, [r'$m=\res{3}$, $n=\res{-5}$; \rest{%s}' % CRE, r'$m=\res{-\frac12}$, $n=\res{4}$; \rest{%s}' % DEC, r'$m=\res{0}$, $n=\res{7}$; \rest{%s}' % T('constant', 'constante'), r'$m=\res{-4}$, $n=\res{0}$; \rest{%s}' % DEC])))
# (D3)
g3 = (Plot(-5, 6, -4, 4, W=330).fn(lambda t: 2, col='g').fn(lambda t: 2 * t + 1, col='b').fn(lambda t: -t - 1, col='a').fn(lambda t: t / 2, col='o')
      .text(5.6, 2.45, r'\normalsize$\boldsymbol{f}$', 'g').text(1.9, 3.5, r'\normalsize$\boldsymbol{g}$', 'b').text(-4.5, 3.0, r'\normalsize$\boldsymbol{h}$', 'a').text(5.5, 3.3, r'\normalsize$\boldsymbol{i}$', 'o'))
X.append(E(1, T(r"Donades les gràfiques de rectes següents, calcula les funcions corresponents:", r"Dadas las siguientes gráficas de rectas, calcula las funciones correspondientes:") + G(g3, 7),
    tasks(1, [T(r"$f$: horitzontal a altura 2: $\res{f(x)=2}$", r"$f$: horizontal a altura 2: $\res{f(x)=2}$"),
              T(r"$g$: passa per $(0,1)$ i $(1,3)$: $m=2$, $n=1$: $\res{g(x)=2x+1}$", r"$g$: pasa por $(0,1)$ y $(1,3)$: $m=2$, $n=1$: $\res{g(x)=2x+1}$"),
              T(r"$h$: passa per $(0,-1)$ i $(-1,0)$: $m=-1$, $n=-1$: $\res{h(x)=-x-1}$", r"$h$: pasa por $(0,-1)$ y $(-1,0)$: $m=-1$, $n=-1$: $\res{h(x)=-x-1}$"),
              T(r"$i$: passa per $(0,0)$ i $(2,1)$: $m=\frac12$, $n=0$: $\res{i(x)=\frac12x}$", r"$i$: pasa por $(0,0)$ y $(2,1)$: $m=\frac12$, $n=0$: $\res{i(x)=\frac12x}$")])))
ok(3 * 1 - 1 == 2 and 3 * 3 - 1 == 8 and 2 + 3 == 5 and -4 + 3 == -1 and 4 / 2 + 1 == 3)
X.append(E(1, T(r"Troba l'expressió de la funció lineal:", r"Halla la expresión de la función lineal:") + tasks(2, [
    T(r"Que passa pels punts $(1,2)$ i $(3,8)$.", r"Que pasa por los puntos $(1,2)$ y $(3,8)$."), T(r"Que passa pels punts $(-2,5)$ i $(4,-1)$.", r"Que pasa por los puntos $(-2,5)$ y $(4,-1)$."),
    T(r"De pendent $\frac12$ que passa per $(4,3)$.", r"De pendiente $\frac12$ que pasa por $(4,3)$."), T(r"Paral·lela a $y=2x-7$ que passa per $(0,4)$.", r"Paralela a $y=2x-7$ que pasa por $(0,4)$.")])
    + recorda(r"$m=\dfrac{y_2-y_1}{x_2-x_1}$ \ " + I_ + r" \ $y=y_1+m(x-x_1)$."),
    tasks(2, [r'$m=\frac{8-2}{3-1}=3$; \ $y=2+3(x-1)\Rightarrow\res{y=3x-1}$', r'$m=\frac{-1-5}{4+2}=-1$; \ $y=5-(x+2)\Rightarrow\res{y=-x+3}$',
              r'$y=3+\frac12(x-4)\Rightarrow\res{y=\frac12x+1}$', T(r'Mateix pendent, $m=2$, i $n=4$: $\res{y=2x+4}$', r'Misma pendiente, $m=2$, y $n=4$: $\res{y=2x+4}$')])))
ok(2 * 2 - 1 == 3 and -2 + 5 == 3)
X.append(E(2, T(r"Representa en uns mateixos eixos $f(x)=2x-1$ i $g(x)=-x+5$ i troba'n el punt de tall, gràficament i resolent una equació.", r"Representa en unos mismos ejes $f(x)=2x-1$ y $g(x)=-x+5$ y halla su punto de corte, gráficamente y resolviendo una ecuación."),
    r'$2x-1=-x+5\Rightarrow3x=6\Rightarrow x=2$, $y=3$: \ $\res{(2,3)}$' + G(Plot(-2, 6, -2, 6, W=200).fn(lambda t: 2 * t - 1).fn(lambda t: -t + 5, col='b').dot(2, 3, 'v'), 3.6)))
ok(all(2 * a + 3 == b for a, b in [(0, 3), (2, 7), (4, 11), (6, 15), (10, 23)]))
X.append(E(2, T(r"Comprova que aquesta taula correspon a una funció lineal, escriu-ne l'expressió i calcula $f(10)$.", r"Comprueba que esta tabla corresponde a una función lineal, escribe su expresión y calcula $f(10)$.")
    + r"\begin{center}\renewcommand{\arraystretch}{1.2}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $0$ & $2$ & $4$ & $6$\\\hline $f(x)$ & $3$ & $7$ & $11$ & $15$\\\hline\end{tabular}\end{center}",
    T(r"Cada vegada que $x$ augmenta 2, $y$ augmenta 4: el pendent és constant, $m=\frac42=2$. Com que $f(0)=3$, $n=3$: \ $\res{f(x)=2x+3}$; \ $f(10)=\res{23}$.",
      r"Cada vez que $x$ aumenta 2, $y$ aumenta 4: la pendiente es constante, $m=\frac42=2$. Como $f(0)=3$, $n=3$: \ $\res{f(x)=2x+3}$; \ $f(10)=\res{23}$.")))

# =====================================================================
# 2. Funcions quadràtiques
X = sec(T('Funcions quadràtiques', 'Funciones cuadráticas'))
# (D2)
Q2 = [('x^2', 1, 0, 0), ('x^2+1', 1, 0, 1), ('x^2-2x-3', 1, -2, -3), ('-3x^2+6x-3', -3, 6, -3), ('x^2+2x', 1, 2, 0), ('-x^2+3', -1, 0, 3)]
def qsol(tx, a, b, c):
    vx, vy = vert(a, b, c); d = b * b - 4 * a * c
    r = sorted(sp.solve(a * x ** 2 + b * x + c, x), key=float) if d >= 0 else []
    ox = (r'$OX$: $' + r',\ '.join('(%s,0)' % sp.latex(v) for v in r) + '$') if r else r'$OX$: ' + T('no en té', 'no tiene')
    p = Plot(-4, 5, -5, 6, W=180).fn(lambda t: a * t * t + b * t + c).dot(float(vx), float(vy), 'v')
    for v in r: p.dot(float(v), 0, 'b')
    return Gi(p, 2.6) + r'\\[2pt]$V\res{(%s,%s)}$\\ ' % (tn(vx), tn(vy)) + ox
ok(vert(1, -2, -3) == (1, -4) and vert(-3, 6, -3) == (1, 0) and vert(1, 2, 0) == (-1, -1) and vert(-1, 0, 3) == (0, 3))
X.append(E(1, T(r"Dibuixa les paràboles següents fent els càlculs necessaris:", r"Dibuja las parábolas siguientes haciendo los cálculos necesarios:") + tasks(3, ['$f(x)=%s$' % q[0] for q in Q2])
    + recorda(T(r"mira el signe de $a$ (∪ o ∩), calcula el vèrtex $V_x=\dfrac{-b}{2a}$, $V_y=f(V_x)$, i els talls amb els eixos; si cal, completa amb una taula de valors.", r"mira el signo de $a$ (∪ o ∩), calcula el vértice $V_x=\dfrac{-b}{2a}$, $V_y=f(V_x)$, y los cortes con los ejes; si hace falta, completa con una tabla de valores.").replace('∪', r'$\cup$').replace('∩', r'$\cap$')),
    tasks(3, [qsol(*q) for q in Q2])))
Q8 = [('x^2-6x+5', 1, -6, 5), ('-x^2+4x', -1, 4, 0), ('2x^2+4x+5', 2, 4, 5), ('-x^2-2x-1', -1, -2, -1)]
def q8sol(tx, a, b, c):
    vx, vy = vert(a, b, c); d = b * b - 4 * a * c
    r = sorted(sp.solve(a * x ** 2 + b * x + c, x), key=float) if d >= 0 else []
    ox = (r'$OX$: $\res{' + r',\ '.join('(%s,0)' % sp.latex(v) for v in r) + '}$') if r else r'$OX$: ' + T(r'no en té ($\Delta<0$)', r'no tiene ($\Delta<0$)')
    return r'$V\res{(%s,%s)}$, ' % (tn(vx), tn(vy)) + T('eix', 'eje') + r' $\res{x=%s}$; ' % tn(vx) + ox + r'; $OY$: $\res{(0,%d)}$; $R=\res{%s}$' % (c, '[%s,+\\infty)' % tn(vy) if a > 0 else '(-\\infty,%s]' % tn(vy))
ok(vert(1, -6, 5) == (3, -4) and vert(-1, 4, 0) == (2, 4) and vert(2, 4, 5) == (-1, 3) and vert(-1, -2, -1) == (-1, 0))
X.append(E(1, T(r"Sense dibuixar-les, troba el vèrtex, l'eix de simetria, els punts de tall amb els eixos i el recorregut de:", r"Sin dibujarlas, halla el vértice, el eje de simetría, los puntos de corte con los ejes y el recorrido de:") + tasks(4, ['$y=%s$' % q[0] for q in Q8]),
    tasks(1, [q8sol(*q) for q in Q8])))
# (D4)
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
X.append(E(2, T(r"Troba els punts on es tallen la paràbola $y=x^2-2x-3$ i la recta $y=x-3$. Representa-les per a comprovar-ho.", r"Halla los puntos donde se cortan la parábola $y=x^2-2x-3$ y la recta $y=x-3$. Represéntalas para comprobarlo."),
    r'$x^2-2x-3=x-3\Rightarrow x^2-3x=0\Rightarrow x=0,\ x=3$: \ $\res{(0,-3)}$ ' + I_ + r' $\res{(3,0)}$' + G(Plot(-3, 5, -5, 5, W=200).fn(lambda t: t * t - 2 * t - 3).fn(lambda t: t - 3, col='b').dot(0, -3, 'v').dot(3, 0, 'v'), 3.6)))
ok(sp.expand((x - 1) ** 2 - 4) == x ** 2 - 2 * x - 3 and vert(1, -4, 3)[0] == 2)
X.append(E(3, T(r"Troba l'expressió de la funció quadràtica en cada cas:", r"Halla la expresión de la función cuadrática en cada caso:") + tasks(1, [
    T(r"$y=x^2+bx+c$, sabent que passa pel punt $(0,3)$ i que té el vèrtex en $x=2$.", r"$y=x^2+bx+c$, sabiendo que pasa por el punto $(0,3)$ y que tiene el vértice en $x=2$."),
    T(r"La paràbola de vèrtex $(1,-4)$ que talla l'eix $OX$ en $x=3$. (Pista: per simetria, l'altre tall és $x=-1$.)", r"La parábola de vértice $(1,-4)$ que corta el eje $OX$ en $x=3$. (Pista: por simetría, el otro corte es $x=-1$.)")]),
    tasks(1, [r'$f(0)=c=3$; \ $V_x=\frac{-b}{2}=2\Rightarrow b=-4$: \ $\res{y=x^2-4x+3}$',
              r'$y=a(x-3)(x+1)$; \ $f(1)=a\cdot(-2)\cdot2=-4\Rightarrow a=1$: \ $\res{y=(x-3)(x+1)=x^2-2x-3}$'])))

# =====================================================================
# 3. Proporcionalitat inversa
X = sec(T('Funcions de proporcionalitat inversa', 'Funciones de proporcionalidad inversa'))
X.append(E(1, T(r"Les magnituds $x$ i $y$ són inversament proporcionals. Completa la taula, escriu la funció que les relaciona i representa-la per a $x>0$.", r"Las magnitudes $x$ e $y$ son inversamente proporcionales. Completa la tabla, escribe la función que las relaciona y represéntala para $x>0$.")
    + r"\begin{center}\renewcommand{\arraystretch}{1.2}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $1$ & $2$ & $3$ & $4$ & $6$ & $12$\\\hline $y$ & & $6$ & & & & \\\hline\end{tabular}\end{center}",
    r"$k=x\cdot y=2\cdot6=12$: \ $\res{y=\dfrac{12}{x}}$" + r"\begin{center}\renewcommand{\arraystretch}{1.2}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $1$ & $2$ & $3$ & $4$ & $6$ & $12$\\\hline $y$ & $\res{12}$ & $6$ & $\res{4}$ & $\res{3}$ & $\res{2}$ & $\res{1}$\\\hline\end{tabular}\end{center}"
    + G(Plot(-1, 13, -1, 13, W=220, lx=2, ly=2).fn(lambda t: 12 / t, .5, 13).dot(1, 12, 'b').dot(2, 6, 'b').dot(3, 4, 'b').dot(4, 3, 'b').dot(6, 2, 'b').dot(12, 1, 'b'), 4)))
def hy(f, av, ah, W=180): return Plot(-6, 6, -6, 6, W=W, lx=2, ly=2).fn(f, n=1200).vl(av).hl(ah)
X.append(E(1, T(r"Representa les funcions $y=\dfrac4x$ i $y=-\dfrac2x$ fent una taula de valors. Indica'n el domini, el recorregut i si són creixents o decreixents.", r"Representa las funciones $y=\dfrac4x$ e $y=-\dfrac2x$ haciendo una tabla de valores. Indica su dominio, el recorrido y si son crecientes o decrecientes."),
    tasks(2, [Gi(hy(lambda t: 4 / t if t else None, 0, 0), 3.2) + r'\\[2pt]$y=\frac4x$: $D=R=\res{%s-\{0\}}$; \rest{%s} ' % (IR, DEC) + T('a cada branca', 'en cada rama'),
              Gi(hy(lambda t: -2 / t if t else None, 0, 0), 3.2) + r'\\[2pt]$y=-\frac2x$: $D=R=\res{%s-\{0\}}$; \rest{%s} ' % (IR, CRE) + T('a cada branca', 'en cada rama')])))
H14 = [(r'\dfrac{2}{x-3}', lambda t: 2 / (t - 3) if t != 3 else None, 3, 0, 2), (r'\dfrac1x+2', lambda t: 1 / t + 2 if t else None, 0, 2, 1),
       (r'\dfrac{-3}{x+1}', lambda t: -3 / (t + 1) if t != -1 else None, -1, 0, -3), (r'\dfrac{4}{x-2}-1', lambda t: 4 / (t - 2) - 1 if t != 2 else None, 2, -1, 4)]
def brace(v): return IR + r'-\{%d\}' % v
X.append(E(2, T(r"Indica les asímptotes, el domini i el recorregut d'aquestes hipèrboles, digues si són creixents o decreixents i representa-les:", r"Indica las asíntotas, el dominio y el recorrido de estas hipérbolas, di si son crecientes o decrecientes y represéntalas:")
    + tasks(4, ['$y=%s$' % h[0] for h in H14]) + recorda(T(r"$y=\dfrac{k}{x-a}+b$ té l'asímptota vertical $x=a$ i l'horitzontal $y=b$.", r"$y=\dfrac{k}{x-a}+b$ tiene la asíntota vertical $x=a$ y la horizontal $y=b$.")),
    tasks(2, [Gi(hy(h[1], h[2], h[3]), 3.1) + r'\\[2pt]$\res{x=%d}$, $\res{y=%d}$; \rest{%s}\\[1pt] $D=\res{%s}$, $R=\res{%s}$' % (h[2], h[3], DEC if h[4] > 0 else CRE, brace(h[2]), brace(h[3])) for h in H14])))
ok(-6 / -4 == 1.5 and -6 / -.5 == 12)
X.append(E(2, T(r"La gràfica de la funció $f(x)=\dfrac kx$ passa pel punt $(2,-3)$. Troba $k$, calcula $f(-4)$ i troba el valor de $x$ per al qual $f(x)=12$.", r"La gráfica de la función $f(x)=\dfrac kx$ pasa por el punto $(2,-3)$. Halla $k$, calcula $f(-4)$ y halla el valor de $x$ para el que $f(x)=12$."),
    r'$k=x\cdot y=2\cdot(-3)=\res{-6}$: $f(x)=-\dfrac6x$. \ $f(-4)=\res{\frac32}$. \ $-\dfrac6x=12\Rightarrow\res{x=-\frac12}$'))
h15 = lambda t: 2 / (t - 1) + 3 if t != 1 else None
ok(h15(2) == 5 and h15(3) == 4 and h15(0) == 1 and h15(-1) == 2)
X.append(E(3, T(r"La gràfica següent és una hipèrbola del tipus $y=\dfrac{k}{x-a}+b$. Troba'n les asímptotes i l'expressió.", r"La gráfica siguiente es una hipérbola del tipo $y=\dfrac{k}{x-a}+b$. Halla sus asíntotas y su expresión.")
    + G(Plot(-4, 6, -2, 8, W=240).fn(h15, n=1200).vl(1).hl(3).dot(2, 5, 'b').dot(3, 4, 'b').dot(0, 1, 'b'), 4.4),
    T(r"Asímptotes $\res{x=1}$ i $\res{y=3}$: $a=1$, $b=3$. Passa per $(2,5)$: $\frac{k}{2-1}+3=5\Rightarrow k=2$: \ $\res{y=\dfrac{2}{x-1}+3}$ (comprovació: $f(3)=4$, $f(0)=1$).",
      r"Asíntotas $\res{x=1}$ e $\res{y=3}$: $a=1$, $b=3$. Pasa por $(2,5)$: $\frac{k}{2-1}+3=5\Rightarrow k=2$: \ $\res{y=\dfrac{2}{x-1}+3}$ (comprobación: $f(3)=4$, $f(0)=1$).")))

# =====================================================================
# 4. Funcions a trossos
X = sec(T('Funcions definides a trossos', 'Funciones definidas a trozos'))
X.append(E(1, T(r"Donada la funció $f(x)=" + pw(('2x+1', 'x<0'), ('x^2', r'0\le x\le3'), ('5', 'x>3')) + r"$, calcula $f(-2)$, $f(0)$, $f(2)$, $f(3)$ i $f(7)$.",
                r"Dada la función $f(x)=" + pw(('2x+1', 'x<0'), ('x^2', r'0\le x\le3'), ('5', 'x>3')) + r"$, calcula $f(-2)$, $f(0)$, $f(2)$, $f(3)$ y $f(7)$.")
    + recorda(T(r"primer mira en quin tros cau cada valor de $x$.", r"primero mira en qué trozo cae cada valor de $x$.")),
    r'$f(-2)=2\cdot(-2)+1=\res{-3}$; \ $f(0)=0^2=\res{0}$; \ $f(2)=\res{4}$; \ $f(3)=\res{9}$; \ $f(7)=\res{5}$'))
# (D5)
D5 = [(pw(('x-3', 'x<4'), ('-x', r'x\geq4')), [(lambda t: t - 3, None, 4, None, False), (lambda t: -t, 4, None, True, None)], (-3, 8, -8, 3)),
      (pw(('-5-x', 'x<-2'), ('1-x^2', r'-2\le x\le2'), ('5', 'x>2')), [(lambda t: -5 - t, None, -2, None, False), (lambda t: 1 - t * t, -2, 2, True, True), (lambda t: 5, 2, None, False, None)], (-6, 6, -4, 6)),
      (pw(('2x-3', 'x<2'), ('3-x', r'x\geq2')), [(lambda t: 2 * t - 3, None, 2, None, False), (lambda t: 3 - t, 2, None, True, None)], (-3, 7, -6, 3)),
      (pw(('-1', 'x<-3'), ('x^2-4', r'-3\le x\le3'), ('6-2x', 'x>3')), [(lambda t: -1, None, -3, None, False), (lambda t: t * t - 4, -3, 3, True, True), (lambda t: 6 - 2 * t, 3, None, False, None)], (-6, 6, -5, 6))]
def trp(pcs, box, W=200):
    p = Plot(*box, W=W)
    for f, a, b, ac, bc in pcs:
        p.fn(f, box[0] if a is None else a, box[1] if b is None else b)
        if a is not None: p.dot(a, f(a), open=not ac)
        if b is not None: p.dot(b, f(b), open=not bc)
    return p
ok(4 - 3 == 1 and -5 + 2 == -3 and 1 - 4 == -3 and 2 * 2 - 3 == 1 and 3 - 2 == 1 and 9 - 4 == 5 and 6 - 6 == 0)
s5 = [T(r"En $x=4$: salt finit (d'1 a $-4$).", r"En $x=4$: salto finito (de 1 a $-4$)."), T(r"Contínua en $x=-2$ (tots dos trossos valen $-3$); salt finit en $x=2$ (de $-3$ a 5).", r"Continua en $x=-2$ (ambos trozos valen $-3$); salto finito en $x=2$ (de $-3$ a 5)."),
      T(r"Contínua: en $x=2$ tots dos trossos valen 1.", r"Continua: en $x=2$ ambos trozos valen 1."), T(r"Salts finits en $x=-3$ (de $-1$ a 5) i en $x=3$ (de 5 a 0).", r"Saltos finitos en $x=-3$ (de $-1$ a 5) y en $x=3$ (de 5 a 0).")]
X.append(E(2, T(r"Dibuixa les gràfiques d'aquestes funcions definides a trossos i estudia'n la continuïtat:", r"Dibuja las gráficas de estas funciones definidas a trozos y estudia su continuidad:") + tasks(2, ['$f(x)=%s$' % d[0] for d in D5], gap='10pt'),
    tasks(2, [Gi(trp(d[1], d[2]), 3.4) + r'\\[2pt]' + s for d, s in zip(D5, s5)])))
# (D6)
g6 = Plot(-5, 6, -3, 6, W=280).fn(lambda t: -2 * t - 3, -5, -2).seg(-2, 1, 2, 1).dot(2, 1).fn(lambda t: -t + 2, 2, 6).dot(2, 0, open=True)
ok(-2 * -2 - 3 == 1 and -2 * -4 - 3 == 5 and -2 + 2 == 0 and -5 + 2 == -3)
X.append(E(2, T(r"Donada la gràfica següent, escriu la funció definida a trossos corresponent:", r"Dada la siguiente gráfica, escribe la función definida a trozos correspondiente:") + G(g6, 5.6),
    T(r"Primer tros: recta per $(-4,5)$ i $(-2,1)$, $m=-2$: $y=-2x-3$. Segon: $y=1$. Tercer: recta per $(3,-1)$ i $(4,-2)$, $m=-1$: $y=-x+2$, amb punt buit en $x=2$.",
      r"Primer trozo: recta por $(-4,5)$ y $(-2,1)$, $m=-2$: $y=-2x-3$. Segundo: $y=1$. Tercero: recta por $(3,-1)$ y $(4,-2)$, $m=-1$: $y=-x+2$, con punto vacío en $x=2$.")
    + r'$$\res{f(x)=' + pw(('-2x-3', 'x<-2'), ('1', r'-2\le x\le2'), ('-x+2', 'x>2')) + '}$$'))
g20 = Plot(-4, 6, -2, 7, W=250).fn(lambda t: t * t, -4, 1).dot(1, 1).fn(lambda t: -t + 4, 1, 6).dot(1, 3, open=True)
X.append(E(2, T(r"La gràfica següent està formada per un tros de paràbola i un tros de recta. Escriu-ne l'expressió i estudia'n la continuïtat.", r"La gráfica siguiente está formada por un trozo de parábola y un trozo de recta. Escribe su expresión y estudia su continuidad.") + G(g20, 4.8),
    T(r"La paràbola té el vèrtex en $(0,0)$ i passa per $(1,1)$ i $(-2,4)$: $y=x^2$. La recta passa per $(2,2)$ i $(4,0)$: $m=-1$, $y=-x+4$.", r"La parábola tiene el vértice en $(0,0)$ y pasa por $(1,1)$ y $(-2,4)$: $y=x^2$. La recta pasa por $(2,2)$ y $(4,0)$: $m=-1$, $y=-x+4$.")
    + r'$$\res{f(x)=' + pw(('x^2', r'x\le1'), ('-x+4', 'x>1')) + '}$$' + T(r"Discontínua en $x=1$: salt finit (d'1 a 3).", r"Discontinua en $x=1$: salto finito (de 1 a 3).")))
ok(4 - 1 == 3 and 6 / 2 == 3)
X.append(E(2, T(r"Considera la funció $f(x)=" + pw(('x^2-1', 'x<2'), (r'\dfrac6x', r'x\geq2')) + r"$. Calcula $f(-2)$, $f(2)$ i $f(6)$, representa-la i estudia'n la continuïtat. Quin és el seu recorregut?",
                r"Considera la función $f(x)=" + pw(('x^2-1', 'x<2'), (r'\dfrac6x', r'x\geq2')) + r"$. Calcula $f(-2)$, $f(2)$ y $f(6)$, represéntala y estudia su continuidad. ¿Cuál es su recorrido?"),
    r'$f(-2)=\res{3}$, \ $f(2)=\frac62=\res{3}$, \ $f(6)=\res{1}$. ' + T(r"En $x=2$ la paràbola arriba a $2^2-1=3$ i la hipèrbola comença en 3: és \rest{contínua}. \ $R=\res{[-1,+\infty)}$.", r"En $x=2$ la parábola llega a $2^2-1=3$ y la hipérbola empieza en 3: es \rest{continua}. \ $R=\res{[-1,+\infty)}$.")
    + G(Plot(-4, 8, -2, 7, W=250).fn(lambda t: t * t - 1, -4, 2).fn(lambda t: 6 / t, 2, 8).dot(2, 3), 4.6)))

# =====================================================================
# 5. Valor absolut
X = sec(T('Funció valor absolut', 'Función valor absoluto'))
# (D7)
A7 = [('-2x-2', lambda t: -2 * t - 2, pw(('-2x-2', 'x<-1'), ('2x+2', r'x\geq-1')), (-5, 3, -1, 7)),
      ('x^2-9', lambda t: t * t - 9, pw(('x^2-9', 'x<-3'), ('-x^2+9', r'-3\le x\le3'), ('x^2-9', 'x>3')), (-5, 5, -1, 11)),
      ('x^2+2x-3', lambda t: t * t + 2 * t - 3, pw(('x^2+2x-3', 'x<-3'), ('-x^2-2x+3', r'-3\le x\le1'), ('x^2+2x-3', 'x>1')), (-5, 3, -1, 7)),
      ('x+5', lambda t: t + 5, pw(('-x-5', 'x<-5'), ('x+5', r'x\geq-5')), (-10, 1, -1, 7)),
      ('2x+1', lambda t: 2 * t + 1, pw(('-2x-1', r'x<-\frac12'), ('2x+1', r'x\geq-\frac12')), (-4, 3, -1, 7)),
      ('-x^2+3', lambda t: -t * t + 3, pw(('x^2-3', r'x<-\sqrt3'), ('-x^2+3', r'-\sqrt3\le x\le\sqrt3'), ('x^2-3', r'x>\sqrt3')), (-4, 4, -1, 7))]
ckroots('x**2+2*x-3', [-3, 1])
def ap(i):
    _, f, _, box = A7[i]
    sy = 2 if box[3] > 8 else 1
    return Plot(*box, W=180, sy=sy, ly=2, lx=2 if box[1] - box[0] > 9 else 1).fn(f, col='v', dash=True).fn(lambda t: abs(f(t)), n=900)
X.append(E(2, T(r"Dibuixa la gràfica de les funcions següents:", r"Dibuja la gráfica de las funciones siguientes:") + tasks(3, [r'$f(x)=|%s|$' % a[0] for a in A7])
    + recorda(T(r"dibuixa la funció de dins del valor absolut i reflecteix cap amunt la part que queda per davall de l'eix $OX$.", r"dibuja la función de dentro del valor absoluto y refleja hacia arriba la parte que queda por debajo del eje $OX$.")),
    tasks(3, [Gi(ap(i), 2.7) + r'\\[3pt]{\scriptsize$' + A7[i][2] + '$}' for i in range(6)], gap='8pt')))
ckroots('-x**2+4*x', [0, 4])
X.append(E(1, T(r"Escriu com a funcions definides a trossos:", r"Escribe como funciones definidas a trozos:") + tasks(4, ['$y=|x-4|$', '$y=|3x+6|$', '$y=|x^2-1|$', '$y=|-x^2+4x|$']),
    tasks(2, ['$' + pw(('-x+4', 'x<4'), ('x-4', r'x\geq4')) + '$', '$' + pw(('-3x-6', 'x<-2'), ('3x+6', r'x\geq-2')) + '$',
              '$' + pw(('x^2-1', 'x<-1'), ('-x^2+1', r'-1\le x\le1'), ('x^2-1', 'x>1')) + '$', '$' + pw(('x^2-4x', 'x<0'), ('-x^2+4x', r'0\le x\le4'), ('x^2-4x', 'x>4')) + '$'], gap='10pt')))
ok(abs(-1 - 2) == 3 and abs(5 - 2) == 3)
X.append(E(2, T(r"Representa en uns mateixos eixos $y=|x-2|$ i la recta $y=3$. Amb l'ajuda de la gràfica, resol l'equació $|x-2|=3$ i la inequació $|x-2|<3$.", r"Representa en unos mismos ejes $y=|x-2|$ y la recta $y=3$. Con la ayuda de la gráfica, resuelve la ecuación $|x-2|=3$ y la inecuación $|x-2|<3$."),
    G(Plot(-3, 7, -1, 6, W=230).fn(lambda t: abs(t - 2)).fn(lambda t: 3, col='b').dot(-1, 3, 'v').dot(5, 3, 'v'), 4.2)
    + T(r"Es tallen en $x=-1$ i $x=5$: $|x-2|=3\Rightarrow\res{x=-1,\ x=5}$. La «V» queda per davall de la recta entre els dos talls: $|x-2|<3\Rightarrow\res{(-1,5)}$.",
        r"Se cortan en $x=-1$ y $x=5$: $|x-2|=3\Rightarrow\res{x=-1,\ x=5}$. La «V» queda por debajo de la recta entre los dos cortes: $|x-2|<3\Rightarrow\res{(-1,5)}$.")))

# =====================================================================
# 6. Funcions exponencials
X = sec(T('Funcions exponencials', 'Funciones exponenciales'))
TB = r"\begin{center}\renewcommand{\arraystretch}{1.3}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $-2$ & $-1$ & $0$ & $1$ & $2$\\\hline %s\\\hline %s\\\hline\end{tabular}\end{center}"
X.append(E(1, T(r"Completa la taula de valors i representa en uns mateixos eixos $y=3^x$ i $y=\left(\frac13\right)^x$. Indica'n el domini, el recorregut, l'asímptota i si són creixents o decreixents.",
                r"Completa la tabla de valores y representa en unos mismos ejes $y=3^x$ e $y=\left(\frac13\right)^x$. Indica su dominio, el recorrido, la asíntota y si son crecientes o decrecientes.")
    + TB % (r'$3^x$ & & & & & ', r'$\left(\frac13\right)^x$ & & & & & '),
    TB % (r'$3^x$ & $\res{\frac19}$ & $\res{\frac13}$ & $\res{1}$ & $\res{3}$ & $\res{9}$', r'$\left(\frac13\right)^x$ & $\res{9}$ & $\res{3}$ & $\res{1}$ & $\res{\frac13}$ & $\res{\frac19}$')
    + G(Plot(-4, 4, -1, 10, W=220, ly=2).fn(lambda t: 3 ** t).fn(lambda t: 3 ** -t, col='b').dot(0, 1, 'v'), 4)
    + T(r"Totes dues: $D=\res{%s}$, $R=\res{(0,+\infty)}$, asímptota horitzontal $\res{y=0}$ i passen per $(0,1)$. $y=3^x$ és \rest{creixent} i $y=\left(\frac13\right)^x$, \rest{decreixent}.",
        r"Ambas: $D=\res{%s}$, $R=\res{(0,+\infty)}$, asíntota horizontal $\res{y=0}$ y pasan por $(0,1)$. $y=3^x$ es \rest{creciente} e $y=\left(\frac13\right)^x$, \rest{decreciente}.") % IR))
X.append(E(1, T(r"Sense dibuixar-les, digues si aquestes funcions exponencials són creixents o decreixents:", r"Sin dibujarlas, di si estas funciones exponenciales son crecientes o decrecientes:") + tasks(4, ['$y=5^x$', '$y=0{,}4^x$', r'$y=\left(\frac32\right)^x$', '$y=2^{-x}$']),
    tasks(4, [r'\rest{%s}' % CRE.capitalize() + ' ($a>1$)', r'\rest{%s}' % DEC.capitalize() + ' ($a<1$)', r'\rest{%s}' % CRE.capitalize(), r'\rest{%s}' % DEC.capitalize() + r': $2^{-x}=\left(\frac12\right)^x$'])))
E27 = [('2^x-3', lambda t: 2 ** t - 3, -3, (0, -2), CRE), ('2^{x-1}', lambda t: 2 ** (t - 1), 0, (1, 1), CRE), (r'\left(\frac12\right)^x+1', lambda t: .5 ** t + 1, 1, (0, 2), DEC), ('3^{x+2}-1', lambda t: 3 ** (t + 2) - 1, -1, (-2, 0), CRE)]
for _, f, _, p, _ in E27: ok(abs(f(p[0]) - p[1]) < 1e-12)
X.append(E(2, T(r"Indica l'asímptota, el punt de referència (la imatge del punt $(0,1)$ de $y=a^x$) i el recorregut d'aquestes funcions, i representa-les:", r"Indica la asíntota, el punto de referencia (la imagen del punto $(0,1)$ de $y=a^x$) y el recorrido de estas funciones, y represéntalas:")
    + tasks(4, ['$y=%s$' % e[0] for e in E27]),
    tasks(2, [Gi(Plot(-5, 5, -4, 6, W=180, lx=2, ly=2).fn(e[1], n=800).hl(e[2]).dot(*e[3], 'b'), 3) + r'\\[2pt]$\res{y=%d}$; $\res{(%d,%d)}$\\[1pt] $R=\res{(%d,+\infty)}$; \rest{%s}' % (e[2], e[3][0], e[3][1], e[2], e[4]) for e in E27])))
ok(3 ** 2 == 9 and F(1, 4) ** -1 == 4 and 5 * 2 ** 3 == 40)
X.append(E(2, T(r"Troba el valor de la lletra en cada cas:", r"Halla el valor de la letra en cada caso:") + tasks(1, [
    T(r"La funció $y=a^x$ passa pel punt $(2,9)$.", r"La función $y=a^x$ pasa por el punto $(2,9)$."), T(r"La funció $y=a^x$ passa pel punt $(-1,4)$.", r"La función $y=a^x$ pasa por el punto $(-1,4)$."),
    T(r"La funció $y=C\cdot2^x$ passa pel punt $(3,40)$.", r"La función $y=C\cdot2^x$ pasa por el punto $(3,40)$.")]),
    tasks(3, [r'$a^2=9\Rightarrow\res{a=3}$', r'$a^{-1}=4\Rightarrow\res{a=\frac14}$', r'$C\cdot2^3=40\Rightarrow\res{C=5}$'])))
ok(2 ** 3 == 8 and F(3) ** -2 == F(1, 9) and 2 ** 4 == 16 and F(1, 2) ** -2 == 4)
X.append(E(2, T(r"Escrivint els dos membres com a potències de la mateixa base, troba el valor de $x$:", r"Escribiendo los dos miembros como potencias de la misma base, halla el valor de $x$:") + tasks(4, ['$2^x=8$', r'$3^x=\dfrac19$', '$2^{x-1}=16$', r'$\left(\frac12\right)^x=4$']),
    tasks(2, [r'$2^x=2^3\Rightarrow\res{x=3}$', r'$3^x=3^{-2}\Rightarrow\res{x=-2}$', r'$2^{x-1}=2^4\Rightarrow\res{x=5}$', r'$2^{-x}=2^2\Rightarrow\res{x=-2}$'])))

# =====================================================================
# 7. Funcions logarítmiques
X = sec(T('Funcions logarítmiques', 'Funciones logarítmicas'))
TL = r"\begin{center}\renewcommand{\arraystretch}{1.3}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $\frac19$ & $\frac13$ & $1$ & $3$ & $9$\\\hline $\log_3x$ & %s\\\hline\end{tabular}\end{center}"
X.append(E(1, T(r"Completa la taula de valors de $y=\log_3x$ i representa-la. Indica'n el domini, el recorregut i l'asímptota. Quina relació té amb la funció $y=3^x$?",
                r"Completa la tabla de valores de $y=\log_3x$ y represéntala. Indica su dominio, el recorrido y la asíntota. ¿Qué relación tiene con la función $y=3^x$?") + TL % '& & & & ',
    TL % r'$\res{-2}$ & $\res{-1}$ & $\res{0}$ & $\res{1}$ & $\res{2}$' + G(Plot(-2, 10, -3, 4, W=240, lx=2).fn(lambda t: lg(3, t), .02, 10).dot(1, 0, 'b').dot(3, 1, 'b').dot(9, 2, 'b').vl(0), 4.4)
    + T(r"$D=\res{(0,+\infty)}$, $R=\res{%s}$, asímptota vertical $\res{x=0}$; creixent. És la \rest{funció inversa} de $y=3^x$: les taules tenen les files intercanviades i les gràfiques són simètriques respecte de $y=x$.",
        r"$D=\res{(0,+\infty)}$, $R=\res{%s}$, asíntota vertical $\res{x=0}$; creciente. Es la \rest{función inversa} de $y=3^x$: las tablas tienen las filas intercambiadas y las gráficas son simétricas respecto de $y=x$.") % IR))
X.append(E(1, T(r"Calcula el domini de les funcions següents:", r"Calcula el dominio de las funciones siguientes:")
    + tasks(3, [r'$f(x)=\log(x-4)$', r'$f(x)=\log_2(3x+6)$', r'$f(x)=\log(5-2x)$', r'$f(x)=\log_3(x^2-4)$', r'$f(x)=\ln(x^2+1)$', r'$f(x)=\log_2(4-x^2)$'])
    + recorda(T(r"l'argument d'un logaritme ha de ser estrictament positiu.", r"el argumento de un logaritmo debe ser estrictamente positivo.")),
    tasks(2, [r'$x-4>0$: $\res{(4,+\infty)}$', r'$3x+6>0$: $\res{(-2,+\infty)}$', r'$5-2x>0$: $\res{\left(-\infty,\frac52\right)}$', r'$x^2-4>0$: $\res{(-\infty,-2)\cup(2,+\infty)}$', r'$x^2+1>0$ ' + T('sempre', 'siempre') + r': $\res{%s}$' % IR, r'$4-x^2>0$: $\res{(-2,2)}$'])))
L32 = [(r'\log_2x-2', lambda t: lg(2, t) - 2, 0, (1, -2), CRE), (r'\log_2(x+3)', lambda t: lg(2, t + 3), -3, (-2, 0), CRE), (r'\log_{\frac12}x', lambda t: -lg(2, t), 0, (1, 0), DEC), (r'\log_3(x-1)+1', lambda t: lg(3, t - 1) + 1, 1, (2, 1), CRE)]
for _, f, _, p, _ in L32: ok(abs(f(p[0]) - p[1]) < 1e-12)
X.append(E(2, T(r"Indica l'asímptota, el punt de referència (la imatge del punt $(1,0)$ de $y=\log_ax$) i el domini d'aquestes funcions, i representa-les:", r"Indica la asíntota, el punto de referencia (la imagen del punto $(1,0)$ de $y=\log_ax$) y el dominio de estas funciones, y represéntalas:")
    + tasks(4, ['$y=%s$' % l[0] for l in L32]),
    tasks(2, [Gi(Plot(-4, 7, -5, 4, W=180, lx=2, ly=2).fn(l[1], l[2] + .01, 7, n=900).vl(l[2]).dot(*l[3], 'b'), 3) + r'\\[2pt]$\res{x=%d}$; $\res{(%d,%d)}$\\[1pt] $D=\res{(%d,+\infty)}$; \rest{%s}' % (l[2], l[3][0], l[3][1], l[2], l[4]) for l in L32])))
# (D8)
def m8(f, box=(-4, 4, -3, 4), a=None, b=None): return Plot(*box, W=170, lx=2, ly=2).fn(f, box[0] if a is None else a, box[1] if b is None else b, n=900)
G8 = [m8(lambda t: 2 ** t), m8(lambda t: 1 / t if t else None), m8(lambda t: lg(2, t), (-1, 7, -3, 4), .01), m8(lambda t: .5 ** t),
      m8(lambda t: sq(t), (-1, 7, -1, 4), 0), m8(abs, (-4, 4, -1, 5)), m8(lambda t: -1 / t if t else None)]
X.append(E(2, T(r"Relaciona les gràfiques següents amb les funcions corresponents:", r"Relaciona las siguientes gráficas con las funciones correspondientes:") + tasks(4, [Gi(p, 2.9) for p in G8])
    + r"\begin{center}1) $y=\left(\frac12\right)^x$ \quad 2) $y=|x|$ \quad 3) $y=\dfrac1x$ \quad 4) $y=\log_2x$ \quad 5) $y=2^x$ \quad 6) $y=\dfrac{-1}{x}$ \quad 7) $y=\sqrt x$\end{center}"
    + recorda(T(r"$y=\sqrt x$ és la inversa de $y=x^2$ (amb $x\geq0$): el seu domini és $[0,+\infty)$ i passa per $(0,0)$, $(1,1)$ i $(4,2)$.", r"$y=\sqrt x$ es la inversa de $y=x^2$ (con $x\geq0$): su dominio es $[0,+\infty)$ y pasa por $(0,0)$, $(1,1)$ y $(4,2)$.")),
    tasks(1, [T(r"\rest{a $\leftrightarrow$ 5}: exponencial creixent, passa per $(0,1)$.", r"\rest{a $\leftrightarrow$ 5}: exponencial creciente, pasa por $(0,1)$."),
              T(r"\rest{b $\leftrightarrow$ 3}: hipèrbola amb $k>0$ (branques al 1r i al 3r quadrant).", r"\rest{b $\leftrightarrow$ 3}: hipérbola con $k>0$ (ramas en el primer y el tercer cuadrante)."),
              T(r"\rest{c $\leftrightarrow$ 4}: logarítmica, passa per $(1,0)$ i té l'asímptota vertical $x=0$.", r"\rest{c $\leftrightarrow$ 4}: logarítmica, pasa por $(1,0)$ y tiene la asíntota vertical $x=0$."),
              T(r"\rest{d $\leftrightarrow$ 1}: exponencial decreixent (base $\frac12<1$).", r"\rest{d $\leftrightarrow$ 1}: exponencial decreciente (base $\frac12<1$)."),
              T(r"\rest{e $\leftrightarrow$ 7}: comença en $(0,0)$ i només existeix per a $x\geq0$.", r"\rest{e $\leftrightarrow$ 7}: empieza en $(0,0)$ y solo existe para $x\geq0$."),
              T(r"\rest{f $\leftrightarrow$ 2}: «V» amb el vèrtex en l'origen.", r"\rest{f $\leftrightarrow$ 2}: «V» con el vértice en el origen."),
              T(r"\rest{g $\leftrightarrow$ 6}: hipèrbola amb $k<0$ (branques al 2n i al 4t quadrant).", r"\rest{g $\leftrightarrow$ 6}: hipérbola con $k<0$ (ramas en el segundo y el cuarto cuadrante).")])))
xp = sp.symbols('x', positive=True)
ok(sp.simplify(2 ** (sp.log(xp - 1, 2)) + 1 - xp) == 0 and sp.simplify(sp.log(3 ** (xp + 2), 3) - 2 - xp) == 0)
X.append(E(3, T(r"Calcula la funció inversa de $f(x)=2^x+1$ i de $g(x)=\log_3x-2$.", r"Calcula la función inversa de $f(x)=2^x+1$ y de $g(x)=\log_3x-2$.")
    + recorda(T(r"$a^y=x\iff y=\log_ax$.", r"$a^y=x\iff y=\log_ax$.")),
    r'$x=2^y+1\Rightarrow2^y=x-1\Rightarrow\res{f^{-1}(x)=\log_2(x-1)}$; \ $x=\log_3y-2\Rightarrow\log_3y=x+2\Rightarrow\res{g^{-1}(x)=3^{x+2}}$'))

# =====================================================================
# 8. Problemes amb funcions
X = sec(T('Problemes amb funcions', 'Problemas con funciones'))
X.append(E(1, T(r"Indica quin tipus de funció (lineal, quadràtica, de proporcionalitat inversa o exponencial) descriu cada situació i escriu-ne l'expressió:", r"Indica qué tipo de función (lineal, cuadrática, de proporcionalidad inversa o exponencial) describe cada situación y escribe su expresión:") + tasks(1, [
    T(r"El preu d'entrar a una fira que cobra 5 € per l'entrada i 2 € per cada atracció ($x$ atraccions).", r"El precio de entrar en una feria que cobra 5 € por la entrada y 2 € por cada atracción ($x$ atracciones)."),
    T(r"El temps que es tarda a recórrer 300 km segons la velocitat $x$ (en km/h).", r"El tiempo que se tarda en recorrer 300 km según la velocidad $x$ (en km/h)."),
    T(r"L'àrea d'un quadrat de costat $x$.", r"El área de un cuadrado de lado $x$."),
    T(r"El nombre de seguidors d'un compte que en té 100 i es duplica cada mes ($x$ mesos).", r"El número de seguidores de una cuenta que tiene 100 y se duplica cada mes ($x$ meses).")]),
    tasks(2, [T('Lineal', 'Lineal') + r': $\res{y=2x+5}$', T('Proporcionalitat inversa', 'Proporcionalidad inversa') + r': $\res{y=\dfrac{300}{x}}$', T('Quadràtica', 'Cuadrática') + r': $\res{y=x^2}$', 'Exponencial' + r': $\res{y=100\cdot2^x}$'])))
ok(abs(1.2 * 8 + 3.5 - 13.1) < 1e-9 and abs((21.5 - 3.5) / 1.2 - 15) < 1e-9)
X.append(E(1, T(r"Un taxi cobra 3,50 € per la baixada de bandera i 1,20 € per cada quilòmetre. Escriu la funció que dona el preu segons els quilòmetres recorreguts. Quant costa un trajecte de 8 km? Quants quilòmetres s'han fet si s'han pagat 21,50 €?",
                r"Un taxi cobra 3,50 € por la bajada de bandera y 1,20 € por cada kilómetro. Escribe la función que da el precio según los kilómetros recorridos. ¿Cuánto cuesta un trayecto de 8 km? ¿Cuántos kilómetros se han hecho si se han pagado 21,50 €?"),
    r'$\res{P(x)=1{,}2x+3{,}5}$. \ $P(8)=9{,}6+3{,}5=\res{13{,}10\text{ €}}$. \ $1{,}2x+3{,}5=21{,}5\Rightarrow x=\dfrac{18}{1{,}2}=\res{15\text{ km}}$'))
ok(20 + 25 * 2 == 35 * 2 and 20 + 25 * 12 == 320 and 35 * 12 == 420)
X.append(E(2, T(r"El gimnàs A cobra 20 € de matrícula i 25 € cada mes. El gimnàs B no cobra matrícula, però la quota és de 35 € cada mes. Escriu la funció que dona el que s'ha pagat en total en cada gimnàs al cap de $x$ mesos. Quan s'ha pagat el mateix? Quin convé més per a un any sencer?",
                r"El gimnasio A cobra 20 € de matrícula y 25 € cada mes. El gimnasio B no cobra matrícula, pero la cuota es de 35 € cada mes. Escribe la función que da lo que se ha pagado en total en cada gimnasio al cabo de $x$ meses. ¿Cuándo se ha pagado lo mismo? ¿Cuál conviene más para un año entero?"),
    r'$\res{A(x)=25x+20}$, \ $\res{B(x)=35x}$. \ $25x+20=35x\Rightarrow\res{x=2}$ ' + T('mesos (70 €). Per a un any:', 'meses (70 €). Para un año:') + r' $A(12)=320$ €, $B(12)=420$ €: ' + T(r'convé \rest{el gimnàs A} (a partir del tercer mes ja és més barat).', r'conviene \rest{el gimnasio A} (a partir del tercer mes ya es más barato).')))
h37 = lambda t: -5 * t * t + 30 * t
ok(h37(3) == 45 and h37(6) == 0 and h37(1) == 25 and h37(5) == 25)
X.append(E(2, T(r"Llancem una pilota cap amunt des de terra. La seua altura (en metres) al cap de $t$ segons és $h(t)=-5t^2+30t$.", r"Lanzamos una pelota hacia arriba desde el suelo. Su altura (en metros) al cabo de $t$ segundos es $h(t)=-5t^2+30t$.")
    + items(T("Quina altura màxima assoleix i en quin instant?", "¿Qué altura máxima alcanza y en qué instante?"), T("Quan torna a terra?", "¿Cuándo vuelve al suelo?"), T("En quins instants està a 25 m d'altura?", "¿En qué instantes está a 25 m de altura?")),
    items(T(r"Paràbola $\cap$: el màxim és el vèrtex. $t=\frac{-30}{-10}=3$, $h(3)=-45+90=45$: \rest{45 m als 3 s}.", r"Parábola $\cap$: el máximo es el vértice. $t=\frac{-30}{-10}=3$, $h(3)=-45+90=45$: \rest{45 m a los 3 s}."),
          r"$-5t^2+30t=0\Rightarrow-5t(t-6)=0\Rightarrow\res{t=6\text{ s}}$",
          r"$-5t^2+30t=25\Rightarrow t^2-6t+5=0\Rightarrow\res{t=1\text{ s}}$ " + I_ + r" $\res{t=5\text{ s}}$")))
ok(15 * (60 - 30) == 450 and vert(-2, 60, 0) == (15, 450))
X.append(E(2, T(r"Amb 60 m de tanca volem tancar un hort rectangular aprofitant una paret (només cal tancar tres costats). Si els dos costats perpendiculars a la paret mesuren $x$ metres, escriu la funció que dona l'àrea de l'hort. Quines dimensions fan que l'àrea siga màxima? Quant val?",
                r"Con 60 m de valla queremos cerrar un huerto rectangular aprovechando una pared (solo hay que cerrar tres lados). Si los dos lados perpendiculares a la pared miden $x$ metros, escribe la función que da el área del huerto. ¿Qué dimensiones hacen que el área sea máxima? ¿Cuánto vale?"),
    T(r"El costat paral·lel a la paret mesura $60-2x$: $\res{A(x)=x(60-2x)=-2x^2+60x}$. Vèrtex: $x=\frac{-60}{-4}=15$: \rest{15 m $\times$ 30 m}, amb una àrea de $A(15)=\res{450\text{ m}^2}$.",
      r"El lado paralelo a la pared mide $60-2x$: $\res{A(x)=x(60-2x)=-2x^2+60x}$. Vértice: $x=\frac{-60}{-4}=15$: \rest{15 m $\times$ 30 m}, con un área de $A(15)=\res{450\text{ m}^2}$.")))
ok(sp.expand((12 - x) * (200 + 40 * x)) == -40 * x ** 2 + 280 * x + 2400 and vert(-40, 280, 2400) == (F(7, 2), 2890) and 200 + 40 * 3.5 == 340)
X.append(E(3, T(r"Una botiga ven 200 samarretes al mes a 12 € cadascuna. Ha comprovat que, per cada euro que rebaixa el preu, en ven 40 més. Si rebaixa el preu $x$ euros, escriu la funció que dona els ingressos mensuals. Quin preu fa màxims els ingressos? Quants diners ingressa aleshores?",
                r"Una tienda vende 200 camisetas al mes a 12 € cada una. Ha comprobado que, por cada euro que rebaja el precio, vende 40 más. Si rebaja el precio $x$ euros, escribe la función que da los ingresos mensuales. ¿Qué precio hace máximos los ingresos? ¿Cuánto dinero ingresa entonces?"),
    T(r"Ingressos = preu $\times$ unitats: $\res{I(x)=(12-x)(200+40x)=-40x^2+280x+2\,400}$. Vèrtex: $x=\frac{-280}{-80}=3{,}5$: preu de \rest{8,50 €}, amb el qual ven 340 samarretes i ingressa $I(3{,}5)=\res{2\,890\text{ €}}$.",
      r"Ingresos = precio $\times$ unidades: $\res{I(x)=(12-x)(200+40x)=-40x^2+280x+2\,400}$. Vértice: $x=\frac{-280}{-80}=3{,}5$: precio de \rest{8,50 €}, con el que vende 340 camisetas e ingresa $I(3{,}5)=\res{2\,890\text{ €}}$.")))
ok(60 / 4 == 15 and 60 / 5 == 12)
X.append(E(2, T(r"Sis pintors tarden 10 dies a pintar un edifici. Escriu la funció que dona els dies que tardarien $n$ pintors treballant al mateix ritme. Quant tardarien 4 pintors? Quants pintors calen per a acabar en 5 dies?",
                r"Seis pintores tardan 10 días en pintar un edificio. Escribe la función que da los días que tardarían $n$ pintores trabajando al mismo ritmo. ¿Cuánto tardarían 4 pintores? ¿Cuántos pintores hacen falta para acabar en 5 días?"),
    r'$k=6\cdot10=60$: \ $\res{t(n)=\dfrac{60}{n}}$. \ $t(4)=\res{15}$ ' + T('dies', 'días') + r'. \ $\dfrac{60}{n}=5\Rightarrow\res{n=12}$ ' + T('pintors', 'pintores') + '.'))
ok(5 + 1.5 * (6 - 2) == 11 and 5 + 1.5 * 8 == 17)
X.append(E(2, T(r"Una empresa de missatgeria cobra 5 € per enviar un paquet de fins a 2 kg. Si el paquet pesa més de 2 kg (fins a un màxim de 10 kg), cobra, a més, 1,50 € per cada quilo que passe de 2. Escriu la funció que dona el preu segons el pes i calcula quant costa enviar paquets d'1,5 kg, de 6 kg i de 10 kg.",
                r"Una empresa de mensajería cobra 5 € por enviar un paquete de hasta 2 kg. Si el paquete pesa más de 2 kg (hasta un máximo de 10 kg), cobra, además, 1,50 € por cada kilo que pase de 2. Escribe la función que da el precio según el peso y calcula cuánto cuesta enviar paquetes de 1,5 kg, de 6 kg y de 10 kg."),
    r'$$\res{P(x)=' + pw(('5', r'0<x\le2'), ('5+1{,}5(x-2)', r'2<x\le10')) + r'}$$ $P(1{,}5)=\res{5\text{ €}}$; \ $P(6)=5+1{,}5\cdot4=\res{11\text{ €}}$; \ $P(10)=5+1{,}5\cdot8=\res{17\text{ €}}$. '
    + T("És contínua: en $x=2$ tots dos trossos valen 5.", "Es continua: en $x=2$ ambos trozos valen 5.")))
ok(200 * 2 ** 5 == 6400 and 200 * 2 ** 8 == 51200)
X.append(E(2, T(r"Un cultiu té 200 bacteris i es duplica cada hora. Escriu la funció que dona el nombre de bacteris al cap de $t$ hores. Quants n'hi haurà al cap de 5 hores? Quant de temps ha de passar perquè n'hi haja 51 200?",
                r"Un cultivo tiene 200 bacterias y se duplica cada hora. Escribe la función que da el número de bacterias al cabo de $t$ horas. ¿Cuántas habrá al cabo de 5 horas? ¿Cuánto tiempo tiene que pasar para que haya 51 200?"),
    r'$\res{N(t)=200\cdot2^t}$. \ $N(5)=200\cdot32=\res{6\,400}$. \ $200\cdot2^t=51\,200\Rightarrow2^t=256=2^8\Rightarrow\res{t=8\text{ h}}$'))
ok(round(5000 * 1.02 ** 3, 2) == 5306.04 and round(5000 * 1.02 ** 10, 2) == 6094.97)
X.append(E(2, T(r"Depositem 5 000 € en un compte que dona un 2 % d'interès compost anual. Escriu la funció que dona el capital al cap de $t$ anys i calcula quant hi haurà al cap de 3 anys i de 10 anys.",
                r"Depositamos 5 000 € en una cuenta que da un 2 % de interés compuesto anual. Escribe la función que da el capital al cabo de $t$ años y calcula cuánto habrá al cabo de 3 años y de 10 años."),
    T(r"Cada any el capital es multiplica per $1+\frac{2}{100}=1{,}02$: ", r"Cada año el capital se multiplica por $1+\frac{2}{100}=1{,}02$: ") + r'$\res{C(t)=5\,000\cdot1{,}02^t}$. \ $C(3)\approx\res{5\,306{,}04\text{ €}}$; \ $C(10)\approx\res{6\,094{,}97\text{ €}}$'))
ok(abs(18000 * .85 ** 2 - 13005) < 1e-6 and .85 ** 4 > .5 > .85 ** 5)
X.append(E(3, T(r"Un cotxe que val 18 000 € perd cada any el 15 % del valor que tenia l'any anterior. Escriu la funció que dona el valor del cotxe al cap de $t$ anys. Quant valdrà d'ací a 2 anys? Quants anys han de passar perquè valga menys de la meitat?",
                r"Un coche que vale 18 000 € pierde cada año el 15 % del valor que tenía el año anterior. Escribe la función que da el valor del coche al cabo de $t$ años. ¿Cuánto valdrá dentro de 2 años? ¿Cuántos años tienen que pasar para que valga menos de la mitad?"),
    T(r"Cada any es multiplica per $1-\frac{15}{100}=0{,}85$: ", r"Cada año se multiplica por $1-\frac{15}{100}=0{,}85$: ") + r'$\res{V(t)=18\,000\cdot0{,}85^t}$. \ $V(2)=\res{13\,005\text{ €}}$. \ '
    + T(r"Cal $0{,}85^t<0{,}5$. Provem: $0{,}85^4\approx0{,}522$ i $0{,}85^5\approx0{,}444$: han de passar \rest{5 anys}.", r"Hace falta $0{,}85^t<0{,}5$. Probamos: $0{,}85^4\approx0{,}522$ y $0{,}85^5\approx0{,}444$: tienen que pasar \rest{5 años}.")))

PRE = r'''\usetikzlibrary{calc}
\usepackage{enumitem}
\definecolor{violet}{HTML}{7C3AED}
\definecolor{orange}{HTML}{EA8A1F}
'''
TIT = T('Funcions elementals', 'Funciones elementales')
build(HERE, 8, TIT, S,
      T("funcions lineals, funcions quadràtiques, paràbola, proporcionalitat inversa, hipèrbola, funcions a trossos, valor absolut, funció exponencial, funció logarítmica, problemes amb funcions",
        "funciones lineales, funciones cuadráticas, parábola, proporcionalidad inversa, hipérbola, funciones a trozos, valor absoluto, función exponencial, función logarítmica, problemas con funciones"),
      T(r"Resol-los al quadern mostrant tots els passos i dibuixa les gràfiques en paper quadriculat. La fitxa recull tots els exercicis de la fitxa del departament i n'afegeix de nous, amb una secció final de problemes. Les seccions segueixen l'ordre dels apunts de la unitat (8.1--8.8).",
        r"Resuélvelos en el cuaderno mostrando todos los pasos y dibuja las gráficas en papel cuadriculado. La ficha recoge todos los ejercicios de la ficha del departamento y añade otros nuevos, con una sección final de problemas. Las secciones siguen el orden de los apuntes de la unidad (8.1--8.8)."),
      T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Pots comprovar les gràfiques amb els laboratoris dels apunts interactius de la unitat (rectes, paràboles, hipèrboles, funcions a trossos, valor absolut, exponencials i logarítmiques).",
        r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar las gráficas con los laboratorios de los apuntes interactivos de la unidad (rectas, parábolas, hipérbolas, funciones a trozos, valor absoluto, exponenciales y logarítmicas)."),
      PRE, lang='es' if ES else 'va')
