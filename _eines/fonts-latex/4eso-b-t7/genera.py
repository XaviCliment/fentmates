# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (4t ESO Matemàtiques B, Unitat 7: Estudi de funcions)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Les 9 seccions segueixen els apartats dels apunts (7.1-7.9): concepte de funció, domini i recorregut, punts de tall,
# creixement i extrems, continuïtat, simetries, periodicitat, funció inversa i estudi complet d'una gràfica.
# Parteix de la fitxa de la unitat 6 de 1r Batx MI (sense translacions ni composició, ni dominis amb exponencials o logaritmes,
# que són de la unitat 8) i hi afig exercicis nous de periodicitat, d'inversa, de gràfiques amb context i d'estudi complet.
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es). Les gràfiques es dibuixen amb la classe Plot de _eines/apunts/4eso-b-t7/fig.py (la mateixa
# dels apunts). Comprovacions: sympy calcula talls i inverses, i els dominis es comproven numèricament.
# Els intervals s'escriuen com a la resta de 4t: (a,b) obert i [a,b] tancat. Els decimals, dins de les fórmules, amb {,}.
# Ús: python3 genera.py && pdflatex t7-fitxa-exercicis.tex (dues vegades) && pdflatex t7-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '4eso-b-t7'))
from eso4b import *
from fig import Plot, piece, sq, PI
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
def oo(a, b): return '(%s,%s)' % (a, b)
def oc(a, b): return '(%s,%s]' % (a, b)
def co(a, b): return '[%s,%s)' % (a, b)
def cc(a, b): return '[%s,%s]' % (a, b)
IR = r'\mathbb{R}'
SI, NO = T(r'\text{Sí}', r'\text{Sí}'), r'\text{No}'
I_, Y_ = T('i', 'y'), T('i', 'e')

def defined(f, t):
    try: v = f(t)
    except OverflowError: return True
    except (ValueError, ZeroDivisionError): return False
    return v is not None and isinstance(v, (int, float)) and math.isfinite(v)
def ckdom(f, inD, edges=(), msg=''):
    """f està definida exactament on inD(t) és cert (malla fina i extrems ± 1e-6)"""
    for t in [i / 97 for i in range(-1500, 1501)] + [e + d for e in edges for d in (-1e-6, 0, 1e-6)]:
        assert defined(f, t) == bool(inD(t)), (msg, t, defined(f, t), inD(t))
    CHK.append((True, True))
def nz(d):
    if abs(d) < 1e-12: raise ZeroDivisionError
    return d
def cr(t): return math.copysign(abs(t) ** (1 / 3), t)
def ckroots(expr, sols, msg=''):
    got = sorted(sp.solve(sp.sympify(expr, locals={'x': x}), x), key=float)
    want = sorted([sp.sympify(s) for s in sols], key=float)
    ok(len(got) == len(want) and all(sp.simplify(a - b) == 0 for a, b in zip(got, want)), (msg, got, want))
def poly(P, pts, col='a'):
    for (a, b), (c, d) in zip(pts, pts[1:]): P.seg(a, b, c, d, col)
    return P

S = []
def sec(title): S.append((title, [])); return S[-1][1]

# =====================================================================
# 1. Concepte de funció
X = sec(T('Concepte de funció. Imatges i antiimatges', 'Concepto de función. Imágenes y antiimágenes'))
p1 = [Plot(-4, 4, -3, 4, W=200).fn(lambda t: t * t - 2),
      Plot(-4, 4, -4, 4, W=200).param(lambda t: 3 * math.cos(t), lambda t: 3 * math.sin(t), 0, 2 * PI),
      Plot(-4, 4, -1, 4, W=200).fn(abs),
      Plot(-3, 5, -3, 3, W=200).param(lambda t: t * t - 2, lambda t: t, -2.7, 2.7)]
X.append(E(1, T(r"Quines d'aquestes gràfiques corresponen a una funció? Justifica-ho amb la prova de la recta vertical.", r"¿Cuáles de estas gráficas corresponden a una función? Justifícalo con la prueba de la recta vertical.") + tasks(4, [Gi(p) for p in p1]),
    tasks(4, [R(SI), R(NO), R(SI), R(NO)]) + T(r"Les gràfiques b) i d) tenen valors de $x$ amb dues imatges: hi ha rectes verticals que les tallen dues vegades.", r"Las gráficas b) y d) tienen valores de $x$ con dos imágenes: hay rectas verticales que las cortan dos veces.")))
X.append(E(1, T(r"Indica si aquestes relacions són funcions:", r"Indica si estas relaciones son funciones:") + tasks(1, [
    T("A cada nombre real li fem correspondre el seu quadrat.", "A cada número real le hacemos corresponder su cuadrado."),
    T("A cada nombre positiu li fem correspondre les seues arrels quadrades.", "A cada número positivo le hacemos corresponder sus raíces cuadradas."),
    T("A cada persona li fem correspondre el número del seu DNI.", "A cada persona le hacemos corresponder el número de su DNI."),
    T("A cada alumne de la classe li fem correspondre els seus germans.", "A cada alumno de la clase le hacemos corresponder sus hermanos.")]),
    tasks(1, [R(SI), R(NO) + T(r': el 4 té dues arrels, $2$ i $-2$.', r': el 4 tiene dos raíces, $2$ y $-2$.'), R(SI), R(NO) + T(': un alumne pot tindre dos o més germans (o cap).', ': un alumno puede tener dos o más hermanos (o ninguno).')])))
f3 = lambda t: t * t - 2 * t - 3
ok(f3(-2) == 5 and f3(0) == -3 and f3(.5) == -3.75)
ckroots('x**2-2*x-3', [-1, 3]); ckroots('x**2-2*x-3+4', [1]); ckroots('x**2-2*x-3+6', [])
X.append(E(1, T(r"Donada la funció $f(x)=x^2-2x-3$, calcula:", r"Dada la función $f(x)=x^2-2x-3$, calcula:") + tasks(2, [
    T(r"Les imatges $f(-2)$, $f(0)$ i $f\left(\frac12\right)$.", r"Las imágenes $f(-2)$, $f(0)$ y $f\left(\frac12\right)$."),
    T(r"Les antiimatges de $0$, de $-4$ i de $-6$.", r"Las antiimágenes de $0$, de $-4$ y de $-6$.")])
    + recorda(T(r"per a la imatge de $a$ substituïm $x$ per $a$; per a les antiimatges de $b$ resolem l'equació $f(x)=b$.", r"para la imagen de $a$ sustituimos $x$ por $a$; para las antiimágenes de $b$ resolvemos la ecuación $f(x)=b$.")),
    tasks(1, [r'$f(-2)=4+4-3=\res{5}$; \ $f(0)=\res{-3}$; \ $f\left(\frac12\right)=\frac14-1-3=\res{-\frac{15}{4}}$',
              T(r"$x^2-2x-3=0\Rightarrow\res{x=-1,\ x=3}$; \ $x^2-2x+1=0\Rightarrow\res{x=1}$; \ $x^2-2x+3=0$, $\Delta=-8<0$: $-6$ \rest{no té antiimatges}.",
                r"$x^2-2x-3=0\Rightarrow\res{x=-1,\ x=3}$; \ $x^2-2x+1=0\Rightarrow\res{x=1}$; \ $x^2-2x+3=0$, $\Delta=-8<0$: $-6$ \rest{no tiene antiimágenes}.")])))
X.append(E(1, T(r"Completa la taula de valors de la funció $f(x)=3x-2$. Quin valor de $x$ té per imatge 10?", r"Completa la tabla de valores de la función $f(x)=3x-2$. ¿Qué valor de $x$ tiene por imagen 10?")
    + r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $-2$ & $-1$ & $0$ & $1$ & $2$\\\hline $f(x)$ & & & & & \\\hline\end{tabular}\end{center}",
    r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $-2$ & $-1$ & $0$ & $1$ & $2$\\\hline $f(x)$ & $\res{-8}$ & $\res{-5}$ & $\res{-2}$ & $\res{1}$ & $\res{4}$\\\hline\end{tabular}\end{center} $3x-2=10\Rightarrow\res{x=4}$"))
X.append(E(2, T(r"Escriu la fórmula de cada funció:", r"Escribe la fórmula de cada función:") + tasks(2, [
    T("A cada nombre li fem correspondre el seu triple més 5.", "A cada número le hacemos corresponder su triple más 5."),
    T(r"L'àrea d'un quadrat en funció del costat $x$.", r"El área de un cuadrado en función del lado $x$."),
    T(r"El preu de $x$ kg de taronges a 1,20 €/kg.", r"El precio de $x$ kg de naranjas a 1,20 €/kg."),
    T("A cada nombre (diferent de 0) li fem correspondre el seu invers.", "A cada número (distinto de 0) le hacemos corresponder su inverso.")]),
    tasks(4, [R('f(x)=3x+5'), R('A(x)=x^2'), R('P(x)=1{,}2x'), R(r'f(x)=\dfrac1x')])))
ok(5 * 15 == 75 and 10 * 10 == 100)
X.append(E(2, T(r"Amb 40 m de tela metàl·lica volem tancar un corral rectangular. Si un costat mesura $x$ metres, escriu la funció $A(x)$ que dona l'àrea del corral. Quins valors pot prendre $x$? Calcula $A(5)$ i $A(10)$.",
                r"Con 40 m de tela metálica queremos cerrar un corral rectangular. Si un lado mide $x$ metros, escribe la función $A(x)$ que da el área del corral. ¿Qué valores puede tomar $x$? Calcula $A(5)$ y $A(10)$."),
    T(r"L'altre costat mesura $20-x$: $\res{A(x)=x(20-x)=20x-x^2}$. Cal $0<x<20$: $D=\res{(0,20)}$. \ $A(5)=\res{75\text{ m}^2}$, $A(10)=\res{100\text{ m}^2}$.",
      r"El otro lado mide $20-x$: $\res{A(x)=x(20-x)=20x-x^2}$. Hace falta $0<x<20$: $D=\res{(0,20)}$. \ $A(5)=\res{75\text{ m}^2}$, $A(10)=\res{100\text{ m}^2}$.")))

# =====================================================================
# 2. Domini i recorregut
X = sec(T('Domini i recorregut', 'Dominio y recorrido'))
d1 = [piece(Plot(-2, 4, -3, 3, W=200), [(lambda t: (t - 1) ** 2 - 2, -1, 3, True, True)]),
      Plot(-5, 3, -3, 6, W=200, lx=2, ly=2).fn(lambda t: 2 + 1 / (t + 1) if t != -1 else None).vl(-1).hl(2),
      Plot(-3, 6, -2, 3, W=200).fn(lambda t: sq(t + 2) - 1 if t >= -2 else None, -2, 6).dot(-2, -1),
      Plot(-5, 3, -2, 4, W=200).fn(lambda t: t + 3, -4, -1).dot(-4, -1).dot(-1, 2, open=True).seg(-1, 3, 2, 3).dot(-1, 3).dot(2, 3)]
X.append(E(1, T(r"Escriu el domini i el recorregut de les funcions representades:", r"Escribe el dominio y el recorrido de las funciones representadas:") + tasks(4, [Gi(p) for p in d1]),
    tasks(2, [r'$D=\res{[-1,3]}$, $R=\res{[-2,2]}$', r'$D=\res{%s-\{-1\}}$, $R=\res{%s-\{2\}}$' % (IR, IR), r'$D=\res{[-2,+\infty)}$, $R=\res{[-1,+\infty)}$', r'$D=\res{[-4,2]}$, $R=\res{[-1,2)\cup\{3\}}$'])))
e5 = [('2x^3-5x+1', lambda t: 2 * t ** 3 - 5 * t + 1, lambda t: True, (), IR),
      (r'\dfrac{3x}{x-5}', lambda t: 3 * t / nz(t - 5), lambda t: t != 5, (5,), IR + r'-\{5\}'),
      (r'\dfrac{x+2}{x^2-9}', lambda t: (t + 2) / nz(t * t - 9), lambda t: abs(t) != 3, (-3, 3), IR + r'-\{-3,3\}'),
      (r'\dfrac{x-1}{x^2+4}', lambda t: (t - 1) / (t * t + 4), lambda t: True, (), IR),
      (r'\dfrac{2}{x^3-4x}', lambda t: 2 / nz(t ** 3 - 4 * t), lambda t: t not in (-2, 0, 2), (-2, 0, 2), IR + r'-\{-2,0,2\}'),
      (r'\dfrac{x+1}{x^2-5x+6}', lambda t: (t + 1) / nz(t * t - 5 * t + 6), lambda t: t not in (2, 3), (2, 3), IR + r'-\{2,3\}')]
e6 = [(r'\sqrt{2x-6}', lambda t: math.sqrt(2 * t - 6), lambda t: t >= 3, (3,), co('3', r'+\infty')),
      (r'\sqrt{9-x^2}', lambda t: math.sqrt(9 - t * t), lambda t: -3 <= t <= 3, (-3, 3), cc('-3', '3')),
      (r'\sqrt{x^2-4x+3}', lambda t: math.sqrt(t * t - 4 * t + 3), lambda t: t <= 1 or t >= 3, (1, 3), oc(r'-\infty', '1') + r'\cup' + co('3', r'+\infty')),
      (r'\sqrt[3]{x^2-1}', lambda t: cr(t * t - 1), lambda t: True, (), IR),
      (r'\dfrac{1}{\sqrt{x-2}}', lambda t: 1 / nz(math.sqrt(t - 2)), lambda t: t > 2, (2,), oo('2', r'+\infty')),
      (r'\dfrac{\sqrt{x+3}}{x-1}', lambda t: math.sqrt(t + 3) / nz(t - 1), lambda t: t >= -3 and t != 1, (-3, 1), co('-3', '1') + r'\cup' + oo('1', r'+\infty'))]
for tx, f, inD, ed, _ in e5 + e6: ckdom(f, inD, ed, tx)
X.append(E(1, T(r"Calcula el domini d'aquestes funcions polinòmiques i racionals:", r"Calcula el dominio de estas funciones polinómicas y racionales:") + tasks(3, ['$f(x)=%s$' % e[0] for e in e5], gap='8pt')
    + recorda(T(r"una funció polinòmica existeix sempre; en una racional, el denominador no pot valdre 0.", r"una función polinómica existe siempre; en una racional, el denominador no puede valer 0.")),
    tasks(3, [R(e[4]) for e in e5])))
X.append(E(2, T(r"Calcula el domini d'aquestes funcions amb radicals:", r"Calcula el dominio de estas funciones con radicales:") + tasks(3, ['$f(x)=%s$' % e[0] for e in e6], gap='8pt')
    + recorda(T(r"el radicand d'una arrel d'índex parell ha de ser $\geq0$ (i $>0$ si l'arrel és en un denominador); si l'índex és senar, no hi ha cap condició.", r"el radicando de una raíz de índice par debe ser $\geq0$ (y $>0$ si la raíz está en un denominador); si el índice es impar, no hay ninguna condición.")),
    tasks(3, [R(e[4]) for e in e6])))
ckdom(lambda t: math.sqrt(t * t - 5), lambda t: abs(t) >= math.sqrt(5), (-math.sqrt(5), math.sqrt(5)))
X.append(E(1, T(r"Pertanyen $x=2$ i $x=3$ al domini de $f(x)=\sqrt{x^2-5}$? Justifica-ho substituint, i després calcula el domini complet.", r"¿Pertenecen $x=2$ y $x=3$ al dominio de $f(x)=\sqrt{x^2-5}$? Justifícalo sustituyendo, y después calcula el dominio completo."),
    T(r"$f(2)=\sqrt{-1}$ no existeix: $\res{2\notin D(f)}$. \ $f(3)=\sqrt4=2$: $\res{3\in D(f)}$. \ $x^2-5\geq0\Rightarrow D(f)=\res{(-\infty,-\sqrt5\,]\cup[\,\sqrt5,+\infty)}$",
      r"$f(2)=\sqrt{-1}$ no existe: $\res{2\notin D(f)}$. \ $f(3)=\sqrt4=2$: $\res{3\in D(f)}$. \ $x^2-5\geq0\Rightarrow D(f)=\res{(-\infty,-\sqrt5\,]\cup[\,\sqrt5,+\infty)}$")))
for t in [i / 7 for i in range(-200, 201)]: assert t * t + 2 >= 2 and 5 - t * t <= 5 and (t == 0 or 2 / t != 0)
X.append(E(2, T(r"Raonant quins valors pot prendre $y$, calcula el recorregut de:", r"Razonando qué valores puede tomar $y$, calcula el recorrido de:") + tasks(4, [r'$f(x)=x^2+2$', r'$g(x)=\sqrt{x-1}+3$', r'$h(x)=\dfrac2x$', r'$k(x)=5-x^2$']),
    tasks(2, [r'$x^2\geq0\Rightarrow R=\res{[2,+\infty)}$', r'$\sqrt{x-1}\geq0\Rightarrow R=\res{[3,+\infty)}$', T(r'$\frac2x$ no val mai 0: $R=\res{%s-\{0\}}$', r'$\frac2x$ nunca vale 0: $R=\res{%s-\{0\}}$') % IR, r'$-x^2\le0\Rightarrow R=\res{(-\infty,5]}$'])))
ckroots('x**2-6*x+9', [3]); ok(36 - 4 * 10 < 0 and 36 - 4 * 9 == 0)
X.append(E(3, T(r"Considera la funció $f(x)=\dfrac{1}{x^2-6x+k}$. Troba el valor de $k$ perquè el seu domini siga $\mathbb{R}-\{3\}$. Per a quins valors de $k$ el domini és tot $\mathbb{R}$?",
                r"Considera la función $f(x)=\dfrac{1}{x^2-6x+k}$. Halla el valor de $k$ para que su dominio sea $\mathbb{R}-\{3\}$. ¿Para qué valores de $k$ el dominio es todo $\mathbb{R}$?"),
    T(r"El denominador només s'ha d'anul·lar en $x=3$ (arrel doble): $x^2-6x+k=(x-3)^2\Rightarrow\res{k=9}$. El domini és $\mathbb{R}$ si el denominador no s'anul·la mai: $\Delta=36-4k<0\Rightarrow\res{k>9}$.",
      r"El denominador solo debe anularse en $x=3$ (raíz doble): $x^2-6x+k=(x-3)^2\Rightarrow\res{k=9}$. El dominio es $\mathbb{R}$ si el denominador no se anula nunca: $\Delta=36-4k<0\Rightarrow\res{k>9}$.")))

# =====================================================================
# 3. Punts de tall
X = sec(T('Punts de tall amb els eixos', 'Puntos de corte con los ejes'))
c3 = [('x^2-5x+4', 'x**2-5*x+4', [1, 4], '4'), ('2x-6', '2*x-6', [3], '-6'), ('x^3-9x', 'x**3-9*x', [-3, 0, 3], '0'), (r'\dfrac{x+4}{x-2}', '(x+4)/(x-2)', [-4], '-2'),
      (r'\sqrt{x+9}-2', 'sqrt(x+9)-2', [-5], '1'), ('x^2+2x+5', 'x**2+2*x+5', [], '5'), ('x^4-5x^2+4', 'x**4-5*x**2+4', [-2, -1, 1, 2], '4'), (r'\dfrac{x^2-4}{x+1}', '(x**2-4)/(x+1)', [-2, 2], '-4')]
for _, e, rr, y0 in c3:
    ckroots(e, rr, e); ok(sp.sympify(e, locals={'x': x}).subs(x, 0) == sp.sympify(y0), e)
def tall(rr, y0):
    return r'$OY$: $\res{(0,%s)}$; ' % y0 + (r'$OX$: $\res{' + r',\ '.join('(%d,0)' % v for v in rr) + '}$' if rr else r'$OX$: ' + T('no en té', 'no tiene'))
X.append(E(1, T(r"Troba els punts de tall amb els eixos de coordenades:", r"Halla los puntos de corte con los ejes de coordenadas:") + tasks(4, ['$f(x)=%s$' % c[0] for c in c3], gap='8pt')
    + recorda(T(r"tall amb $OY$: fem $x=0$; talls amb $OX$: resolem $f(x)=0$.", r"corte con $OY$: hacemos $x=0$; cortes con $OX$: resolvemos $f(x)=0$.")),
    tasks(1, [tall(c[2], c[3]) for c in c3])))
ckroots('x**2+x-6', [-3, 2])
X.append(E(2, T(r"Troba el valor de $a$ perquè la funció $f(x)=x^2+ax-6$ talle l'eix $OX$ en $x=2$. On el talla l'altra vegada? I on talla l'eix $OY$?",
                r"Halla el valor de $a$ para que la función $f(x)=x^2+ax-6$ corte el eje $OX$ en $x=2$. ¿Dónde lo corta la otra vez? ¿Y dónde corta el eje $OY$?"),
    T(r"$f(2)=4+2a-6=0\Rightarrow\res{a=1}$. \ $x^2+x-6=0\Rightarrow$ l'altre tall és $\res{(-3,0)}$. \ $OY$: $\res{(0,-6)}$.", r"$f(2)=4+2a-6=0\Rightarrow\res{a=1}$. \ $x^2+x-6=0\Rightarrow$ el otro corte es $\res{(-3,0)}$. \ $OY$: $\res{(0,-6)}$.")))
ok(sp.expand(2 * (x + 1) * (x - 4)) == 2 * x ** 2 - 6 * x - 8)
X.append(E(3, T(r"Escriu l'expressió d'una funció quadràtica que talle l'eix $OX$ en $x=-1$ i en $x=4$, i l'eix $OY$ en el punt $(0,-8)$.",
                r"Escribe la expresión de una función cuadrática que corte el eje $OX$ en $x=-1$ y en $x=4$, y el eje $OY$ en el punto $(0,-8)$."),
    T(r"Si s'anul·la en $-1$ i en $4$, és $f(x)=a(x+1)(x-4)$. \ $f(0)=-4a=-8\Rightarrow a=2$: \ $\res{f(x)=2(x+1)(x-4)=2x^2-6x-8}$",
      r"Si se anula en $-1$ y en $4$, es $f(x)=a(x+1)(x-4)$. \ $f(0)=-4a=-8\Rightarrow a=2$: \ $\res{f(x)=2(x+1)(x-4)=2x^2-6x-8}$")))

# =====================================================================
# 4. Creixement, màxims i mínims
X = sec(T('Creixement i decreixement. Màxims i mínims', 'Crecimiento y decrecimiento. Máximos y mínimos'))
P4 = [(-5, -2), (-3, 3), (-1, 1), (1, 4), (3, -3), (6, 2)]
g4 = poly(Plot(-6, 7, -4, 5, W=300), P4)
for q in P4: g4.dot(*q)
X.append(E(1, T(r"Observa la gràfica i indica'n el domini, el recorregut, els intervals de creixement i de decreixement, i els màxims i mínims (relatius i absoluts).",
                r"Observa la gráfica e indica su dominio, el recorrido, los intervalos de crecimiento y de decrecimiento, y los máximos y mínimos (relativos y absolutos).") + G(g4, 6),
    T(r"$D=\res{[-5,6]}$, $R=\res{[-3,4]}$. Creixent en $\res{(-5,-3)\cup(-1,1)\cup(3,6)}$; decreixent en $\res{(-3,-1)\cup(1,3)}$. Màxims: $\res{(-3,3)}$ relatiu i $\res{(1,4)}$ absolut. Mínims: $\res{(-1,1)}$ relatiu i $\res{(3,-3)}$ absolut.",
      r"$D=\res{[-5,6]}$, $R=\res{[-3,4]}$. Creciente en $\res{(-5,-3)\cup(-1,1)\cup(3,6)}$; decreciente en $\res{(-3,-1)\cup(1,3)}$. Máximos: $\res{(-3,3)}$ relativo y $\res{(1,4)}$ absoluto. Mínimos: $\res{(-1,1)}$ relativo y $\res{(3,-3)}$ absoluto.")))
fc = lambda t: t ** 3 - 3 * t
ok(fc(-1) == 2 and fc(1) == -2)
X.append(E(1, T(r"La gràfica és la de $f(x)=x^3-3x$. Indica'n els intervals de creixement i de decreixement i els extrems relatius. Té màxim o mínim absolut?",
                r"La gráfica es la de $f(x)=x^3-3x$. Indica sus intervalos de crecimiento y de decrecimiento y los extremos relativos. ¿Tiene máximo o mínimo absoluto?") + G(Plot(-3, 3, -4, 4, W=230).fn(fc).dot(-1, 2).dot(1, -2), 4),
    T(r"Creixent en $\res{(-\infty,-1)\cup(1,+\infty)}$; decreixent en $\res{(-1,1)}$. Màxim relatiu $\res{(-1,2)}$ i mínim relatiu $\res{(1,-2)}$. No té extrems absoluts: per la dreta puja sense parar i per l'esquerra baixa sense parar.",
      r"Creciente en $\res{(-\infty,-1)\cup(1,+\infty)}$; decreciente en $\res{(-1,1)}$. Máximo relativo $\res{(-1,2)}$ y mínimo relativo $\res{(1,-2)}$. No tiene extremos absolutos: por la derecha sube sin parar y por la izquierda baja sin parar.")))
sol8 = lambda t: (t - 1) ** 2 / 2 - 2
ok(sol8(-1) == 0 and sol8(3) == 0 and sol8(1) == -2)
X.append(E(2, T(r"Dibuixa la gràfica d'una funció amb domini $\mathbb{R}$, decreixent en $(-\infty,1)$, creixent en $(1,+\infty)$, amb mínim absolut en $(1,-2)$ i que talle l'eix $OX$ en $x=-1$ i en $x=3$.",
                r"Dibuja la gráfica de una función con dominio $\mathbb{R}$, decreciente en $(-\infty,1)$, creciente en $(1,+\infty)$, con mínimo absoluto en $(1,-2)$ y que corte el eje $OX$ en $x=-1$ y en $x=3$."),
    T(r"Per exemple (n'hi ha moltes), la paràbola $f(x)=\frac12(x-1)^2-2$:", r"Por ejemplo (hay muchas), la parábola $f(x)=\frac12(x-1)^2-2$:") + G(Plot(-3, 5, -3, 4, W=220).fn(sol8).dot(1, -2, 'b').dot(-1, 0, 'b').dot(3, 0, 'b'))))
PD = [(0, 0), (2, 30), (5, 30), (7, 50), (10, 20), (12, 0)]
gd = poly(Plot(-1, 13, -5, 55, sx=1, sy=10, lx=2, ly=10, W=300), PD)
for q in PD: gd.dot(*q)
ok(50 - 10 * (9 - 7) == 30)
X.append(E(2, T(r"La gràfica mostra l'altura (en metres) d'un dron en funció del temps (en minuts) que fa que s'ha enlairat.", r"La gráfica muestra la altura (en metros) de un dron en función del tiempo (en minutos) que hace que ha despegado.") + G(gd, 6.4)
    + items(T("Indica el domini i el recorregut i explica què signifiquen.", "Indica el dominio y el recorrido y explica qué significan."),
            T("En quins intervals de temps puja, baixa o es manté a la mateixa altura?", "¿En qué intervalos de tiempo sube, baja o se mantiene a la misma altura?"),
            T("Quina és l'altura màxima i quan l'assoleix?", "¿Cuál es la altura máxima y cuándo la alcanza?"),
            T("Durant quant de temps està per damunt dels 30 m?", "¿Durante cuánto tiempo está por encima de los 30 m?")),
    items(T(r"$D=\res{[0,12]}$: el vol dura 12 min. $R=\res{[0,50]}$: l'altura va de 0 m a 50 m.", r"$D=\res{[0,12]}$: el vuelo dura 12 min. $R=\res{[0,50]}$: la altura va de 0 m a 50 m."),
          T(r"Puja en $\res{(0,2)\cup(5,7)}$, es manté en $\res{(2,5)}$ i baixa en $\res{(7,12)}$.", r"Sube en $\res{(0,2)\cup(5,7)}$, se mantiene en $\res{(2,5)}$ y baja en $\res{(7,12)}$."),
          T(r"Màxim absolut $\res{(7,50)}$: 50 m al cap de 7 min.", r"Máximo absoluto $\res{(7,50)}$: 50 m a los 7 min."),
          T(r"Des del minut 5 fins al minut 9 (de 7 a 10 baixa 10 m cada minut): \rest{4 minuts}.", r"Desde el minuto 5 hasta el minuto 9 (de 7 a 10 baja 10 m cada minuto): \rest{4 minutos}."))))

# =====================================================================
# 5. Continuïtat
X = sec(T('Continuïtat', 'Continuidad'))
g5 = Plot(-6, 6, -2, 5, W=320)
g5.fn(lambda t: t / 2 + 3, -6, 0).dot(-3, 1.5, open=True).dot(-3, 3.5).dot(0, 3, open=True)
g5.fn(lambda t: 1 - t / 2, 0, 2).dot(0, 1).dot(2, 0, open=True).fn(lambda t: 1 / (t - 2), 2.02, 6).vl(2)
g15 = Plot(-6, 7, -2, 7, W=320)
g15.fn(lambda t: t + 5, -6, -3).dot(-6, -1).dot(-3, 2, open=True).dot(-3, 4)
g15.fn(lambda t: 2 - (t + 3) / 2, -3, 1).dot(1, 0)
g15.fn(lambda t: 2 / (t - 1), 1.05, 3).dot(3, 1, open=True).vl(1)
g15.fn(lambda t: t - 1, 3, 7).dot(3, 2)
ok(-3 + 5 == 2 - 0 / 2 and 2 - (1 + 3) / 2 == 0 and 2 / (3 - 1) == 1 and 3 - 1 == 2)
def c16(): return Plot(-1, 5, -2, 5, W=170)
g16 = [c16().fn(lambda t: 3 + (t - 2) / 2 - (t - 2) ** 2 / 4).dot(2, 3, open=True),
       c16().fn(lambda t: (t - 2) / 2 + 1, -1, 2).dot(2, 1).fn(lambda t: 3 + (t - 2) ** 2 / 3, 2, 5).dot(2, 3, open=True),
       c16().fn(lambda t: abs(t - 2) + 1).dot(2, 1),
       c16().fn(lambda t: 1 / (t - 2) + 1 if abs(t - 2) > 1e-9 else None).vl(2)]
EV, SF, SIN, AS, CO = (T(r'\text{evitable}', r'\text{evitable}'), T(r'\text{salt finit}', r'\text{salto finito}'), T(r'\text{salt infinit}', r'\text{salto infinito}'),
                       T(r'\text{asimptòtica}', r'\text{asintótica}'), T(r'\text{Contínua}', r'\text{Continua}'))
X.append(E(1, T(r"Indica en quins punts és discontínua aquesta funció i classifica cada discontinuïtat.", r"Indica en qué puntos es discontinua esta función y clasifica cada discontinuidad.") + G(g5, 6.2),
    T(r"$x=-3$: $\res{%s}$ (el punt està fora de lloc). \ $x=0$: $\res{%s}$ (de 3 a 1). \ $x=2$: $\res{%s}$ (per l'esquerra arriba a 0 i per la dreta se'n va a $+\infty$).",
      r"$x=-3$: $\res{%s}$ (el punto está fuera de lugar). \ $x=0$: $\res{%s}$ (de 3 a 1). \ $x=2$: $\res{%s}$ (por la izquierda llega a 0 y por la derecha se va a $+\infty$).") % (EV, SF, SIN)))
X.append(E(2, T(r"Indica en quins punts és discontínua aquesta funció i classifica cada discontinuïtat. En quins intervals és contínua?", r"Indica en qué puntos es discontinua esta función y clasifica cada discontinuidad. ¿En qué intervalos es continua?") + G(g15, 6.2),
    T(r"$x=-3$: $\res{%s}$ (els dos costats arriben a 2, però $f(-3)=4$). \ $x=1$: $\res{%s}$ (per l'esquerra arriba a 0 i per la dreta se'n va a $+\infty$). \ $x=3$: $\res{%s}$ (per l'esquerra arriba a 1 i $f(3)=2$). És contínua en $\res{[-6,-3)\cup(-3,1)\cup(1,3)\cup[3,7]}$.",
      r"$x=-3$: $\res{%s}$ (los dos lados llegan a 2, pero $f(-3)=4$). \ $x=1$: $\res{%s}$ (por la izquierda llega a 0 y por la derecha se va a $+\infty$). \ $x=3$: $\res{%s}$ (por la izquierda llega a 1 y $f(3)=2$). Es continua en $\res{[-6,-3)\cup(-3,1)\cup(1,3)\cup[3,7]}$.") % (EV, SIN, SF)))
X.append(E(2, T(r"Estudia la continuïtat de cada funció en $x=2$. Si és discontínua, classifica la discontinuïtat i, si és evitable, indica quin valor hauria de tindre $f(2)$ perquè la funció fora contínua.",
                r"Estudia la continuidad de cada función en $x=2$. Si es discontinua, clasifica la discontinuidad y, si es evitable, indica qué valor debería tener $f(2)$ para que la función fuera continua.") + tasks(4, [Gi(p) for p in g16]),
    tasks(1, [T(r"Discontinuïtat $\res{%s}$: els dos costats arriben a 3, però $f(2)$ no existeix. Seria contínua si $\res{f(2)=3}$.", r"Discontinuidad $\res{%s}$: los dos lados llegan a 3, pero $f(2)$ no existe. Sería continua si $\res{f(2)=3}$.") % EV,
              T(r"Discontinuïtat de $\res{%s}$: per l'esquerra arriba a 1 (i $f(2)=1$) i per la dreta a 3.", r"Discontinuidad de $\res{%s}$: por la izquierda llega a 1 (y $f(2)=1$) y por la derecha a 3.") % SF,
              T(r"$\res{%s}$: els dos costats arriben a 1 i $f(2)=1$. Té un pic, però es dibuixa sense alçar el llapis.", r"$\res{%s}$: los dos lados llegan a 1 y $f(2)=1$. Tiene un pico, pero se dibuja sin levantar el lápiz.") % CO,
              T(r"Discontinuïtat $\res{%s}$: per l'esquerra se'n va a $-\infty$ i per la dreta a $+\infty$ (asímptota vertical $x=2$).", r"Discontinuidad $\res{%s}$: por la izquierda se va a $-\infty$ y por la derecha a $+\infty$ (asíntota vertical $x=2$).") % AS])))
g23 = Plot(-3, 7, -2, 6, W=260).fn(lambda t: t + 1, -3, 1).dot(1, 2).fn(lambda t: t - 1, 1, 7).dot(1, 0, open=True).dot(4, 3, open=True).dot(4, 5)
X.append(E(2, T(r"Dibuixa la gràfica d'una funció amb domini $\mathbb{R}$ que tinga una discontinuïtat de salt finit en $x=1$ i una d'evitable en $x=4$, i que siga contínua en la resta de punts.",
                r"Dibuja la gráfica de una función con dominio $\mathbb{R}$ que tenga una discontinuidad de salto finito en $x=1$ y una evitable en $x=4$, y que sea continua en el resto de puntos."),
    T(r"Per exemple (n'hi ha moltes):", r"Por ejemplo (hay muchas):") + G(g23, 4.6)))

# =====================================================================
# 6. Simetries
X = sec(T('Simetries: funcions parelles i senars', 'Simetrías: funciones pares e impares'))
p6 = [('x^4-2x^2+3', 'x**4-2*x**2+3', 'p'), ('x^3+5x', 'x**3+5*x', 's'), ('x^3+1', 'x**3+1', 'c'), (r'\dfrac{2x}{x^2+1}', '2*x/(x**2+1)', 's'),
      (r'\dfrac{x^2-1}{x^4+2}', '(x**2-1)/(x**4+2)', 'p'), ('|x|-x^2', 'Abs(x)-x**2', 'p'), (r'x^2-4x', 'x**2-4*x', 'c'), (r'\sqrt{x^2+1}', 'sqrt(x**2+1)', 'p')]
for _, e, k in p6:
    f = sp.sympify(e, locals={'x': x}); fm = f.subs(x, -x)
    ok((k == 'p') == (sp.simplify(fm - f) == 0) and (k == 's') == (sp.simplify(fm + f) == 0), e)
NOM = {'p': T('Parella', 'Par'), 's': T('Senar', 'Impar'), 'c': T('Cap', 'Ninguna')}
X.append(E(1, T(r"Estudia si aquestes funcions són parelles, senars o cap de les dues:", r"Estudia si estas funciones son pares, impares o ninguna de las dos:") + tasks(4, ['$f(x)=%s$' % c[0] for c in p6], gap='8pt')
    + recorda(T(r"calculem $f(-x)$. Si ix $f(x)$, és parella (simètrica respecte de l'eix $OY$); si ix $-f(x)$, és senar (simètrica respecte de l'origen).", r"calculamos $f(-x)$. Si sale $f(x)$, es par (simétrica respecto del eje $OY$); si sale $-f(x)$, es impar (simétrica respecto del origen).")),
    tasks(4, [r'\rest{' + NOM[c[2]] + '}' for c in p6])))
g25 = [Plot(-4, 4, -4, 4, W=190).fn(lambda t: t * t - 3), Plot(-4, 4, -4, 4, W=190).fn(lambda t: t ** 3 / 4),
       Plot(-3, 5, -3, 5, W=190).fn(lambda t: (t - 1) ** 2 - 2), Plot(-5, 5, -3, 3, W=190).fn(lambda t: 4 * t / (t * t + 1))]
X.append(E(1, T(r"Observa cada gràfica i indica si la funció és parella, senar o cap de les dues.", r"Observa cada gráfica e indica si la función es par, impar o ninguna de las dos.") + tasks(4, [Gi(p) for p in g25]),
    tasks(4, [r'\rest{' + NOM[k] + '}' for k in 'pscs'])))
half = [(0, 0), (1, 2), (3, -1), (4, 0)]
def halfplot(sym):
    p = Plot(-5, 5, -3, 3, W=210); poly(p, half)
    if sym: poly(p, [(-a, sym * b) for a, b in half], 'b')
    return p
X.append(E(2, T(r"La gràfica següent és la part d'una funció $f$ corresponent a $x\in[0,4]$. Completa-la en $[-4,0]$ si $f$ és parella i, en una altra gràfica, si $f$ és senar.",
                r"La gráfica siguiente es la parte de una función $f$ correspondiente a $x\in[0,4]$. Complétala en $[-4,0]$ si $f$ es par y, en otra gráfica, si $f$ es impar.") + G(halfplot(0), 4.2),
    tasks(2, [T("Parella (simetria respecte de $OY$):", "Par (simetría respecto de $OY$):") + G(halfplot(1), 3.6), T("Senar (simetria respecte de l'origen):", "Impar (simetría respecto del origen):") + G(halfplot(-1), 3.6)])))
X.append(E(3, T(r"Siguen $f$ i $g$ dues funcions senars. Demostra que la suma $f+g$ és senar i que el producte $f\cdot g$ és una funció parella. Comprova-ho amb $f(x)=x^3$ i $g(x)=x$.",
                r"Sean $f$ y $g$ dos funciones impares. Demuestra que la suma $f+g$ es impar y que el producto $f\cdot g$ es una función par. Compruébalo con $f(x)=x^3$ y $g(x)=x$."),
    T(r"$(f+g)(-x)=f(-x)+g(-x)=-f(x)-g(x)=-(f+g)(x)$: \rest{senar}. \ $(f\cdot g)(-x)=\big(-f(x)\big)\cdot\big(-g(x)\big)=f(x)\cdot g(x)$: \rest{parella}. \ Amb l'exemple: $x^3+x$ és senar i $x^3\cdot x=x^4$ és parella.",
      r"$(f+g)(-x)=f(-x)+g(-x)=-f(x)-g(x)=-(f+g)(x)$: \rest{impar}. \ $(f\cdot g)(-x)=\big(-f(x)\big)\cdot\big(-g(x)\big)=f(x)\cdot g(x)$: \rest{par}. \ Con el ejemplo: $x^3+x$ es impar y $x^3\cdot x=x^4$ es par.")))

# =====================================================================
# 7. Periodicitat
X = sec(T('Periodicitat', 'Periodicidad'))
def f28(t):
    u = t % 3
    return 1 + u if u <= 2 else 3 - 2 * (u - 2)
ok(f28(10) == 2 and f28(-1) == 3 and f28(30) == 1 and f28(47) == 3)
X.append(E(1, T(r"La gràfica següent correspon a una funció periòdica.", r"La gráfica siguiente corresponde a una función periódica.") + G(Plot(-4, 13, -1, 4, W=420).fn(f28, -3, 12, n=1500), 9)
    + tasks(2, [T("Quin és el seu període?", "¿Cuál es su periodo?"), T(r"Calcula $f(10)$, $f(-1)$, $f(30)$ i $f(47)$.", r"Calcula $f(10)$, $f(-1)$, $f(30)$ y $f(47)$.")]),
    tasks(1, [r'$\res{T=3}$', r'$f(10)=f(1+3\cdot3)=f(1)=\res{2}$; \ $f(-1)=f(-1+3)=f(2)=\res{3}$; \ $f(30)=f(0+10\cdot3)=f(0)=\res{1}$; \ $f(47)=f(2+15\cdot3)=f(2)=\res{3}$'])))
X.append(E(2, T(r"Una funció $f$ és periòdica de període 5, i sabem que $f(1)=4$ i $f(3)=-2$. Calcula $f(11)$, $f(-2)$, $f(23)$ i $f(101)$.",
                r"Una función $f$ es periódica de periodo 5, y sabemos que $f(1)=4$ y $f(3)=-2$. Calcula $f(11)$, $f(-2)$, $f(23)$ y $f(101)$."),
    r'$f(11)=f(1+2\cdot5)=\res{4}$; \ $f(-2)=f(-2+5)=f(3)=\res{-2}$; \ $f(23)=f(3+4\cdot5)=\res{-2}$; \ $f(101)=f(1+20\cdot5)=\res{4}$'))
ok(150 % 60 == 30 and 240 % 60 == 0 and 600 // 60 == 10)
X.append(E(2, T(r"Una sínia de 20 m de diàmetre fa una volta cada 60 segons. Una cabina comença a girar des del punt més baix, a 2 m de terra. L'altura de la cabina és una funció periòdica del temps.",
                r"Una noria de 20 m de diámetro da una vuelta cada 60 segundos. Una cabina empieza a girar desde el punto más bajo, a 2 m del suelo. La altura de la cabina es una función periódica del tiempo.")
    + items(T("Quin és el període? Quins són l'altura màxima i l'altura mínima de la cabina (el recorregut)?", "¿Cuál es el periodo? ¿Cuáles son la altura máxima y la altura mínima de la cabina (el recorrido)?"),
            T("A quina altura és la cabina al cap de 150 s? I al cap de 240 s?", "¿A qué altura está la cabina a los 150 s? ¿Y a los 240 s?"),
            T("Quantes vegades passa pel punt més alt en 10 minuts?", "¿Cuántas veces pasa por el punto más alto en 10 minutos?")),
    items(T(r"$\res{T=60\text{ s}}$. Altura mínima 2 m i màxima $2+20=22$ m: $R=\res{[2,22]}$.", r"$\res{T=60\text{ s}}$. Altura mínima 2 m y máxima $2+20=22$ m: $R=\res{[2,22]}$."),
          T(r"$150=2\cdot60+30$: com als 30 s (mitja volta), és dalt de tot: \rest{22 m}. \ $240=4\cdot60$: com a l'inici: \rest{2 m}.", r"$150=2\cdot60+30$: como a los 30 s (media vuelta), está arriba del todo: \rest{22 m}. \ $240=4\cdot60$: como al inicio: \rest{2 m}."),
          T(r"Fa $600:60=10$ voltes: \rest{10 vegades}.", r"Da $600:60=10$ vueltas: \rest{10 veces}."))))
f31 = lambda t: abs(t % 4 - 2)
ok(f31(13) == 1 and f31(0) == 2 and f31(2) == 0)
X.append(E(2, T(r"Una funció periòdica de període 4 val $f(x)=|x-2|$ en l'interval $[0,4]$. Dibuixa'n la gràfica entre $x=-4$ i $x=8$ i calcula $f(13)$.",
                r"Una función periódica de periodo 4 vale $f(x)=|x-2|$ en el intervalo $[0,4]$. Dibuja su gráfica entre $x=-4$ y $x=8$ y calcula $f(13)$."),
    G(Plot(-5, 9, -1, 3, W=380).fn(f31, -4, 8, n=1200).fn(f31, 0, 4, 'b', n=400), 8) + r'$f(13)=f(1+3\cdot4)=f(1)=|1-2|=\res{1}$'))

# =====================================================================
# 8. Funció inversa
X = sec(T('Funció inversa', 'Función inversa'))
X.append(E(1, T(r"D'una funció $f$ que té inversa sabem que $f(1)=3$, $f(2)=5$ i $f(4)=-1$. Calcula $f^{-1}(5)$, $f^{-1}(-1)$ i $f^{-1}\big(f(2)\big)$. Quins punts de la gràfica de $f^{-1}$ coneixes?",
                r"De una función $f$ que tiene inversa sabemos que $f(1)=3$, $f(2)=5$ y $f(4)=-1$. Calcula $f^{-1}(5)$, $f^{-1}(-1)$ y $f^{-1}\big(f(2)\big)$. ¿Qué puntos de la gráfica de $f^{-1}$ conoces?"),
    T(r"$f^{-1}(5)=\res{2}$, \ $f^{-1}(-1)=\res{4}$, \ $f^{-1}\big(f(2)\big)=\res{2}$. La gràfica de $f^{-1}$ passa per $\res{(3,1)}$, $\res{(5,2)}$, $\res{(-1,4)}$: s'intercanvien les coordenades.",
      r"$f^{-1}(5)=\res{2}$, \ $f^{-1}(-1)=\res{4}$, \ $f^{-1}\big(f(2)\big)=\res{2}$. La gráfica de $f^{-1}$ pasa por $\res{(3,1)}$, $\res{(5,2)}$, $\res{(-1,4)}$: se intercambian las coordenadas.")))
xp = sp.symbols('x', positive=True)
inv = [('5x-2', '5*x-2', '(x+2)/5', r'\dfrac{x+2}{5}'), (r'\dfrac{3x+1}{2}', '(3*x+1)/2', '(2*x-1)/3', r'\dfrac{2x-1}{3}'), ('x^3-4', 'x**3-4', None, r'\sqrt[3]{x+4}'),
       (r'\dfrac4x', '4/x', '4/x', r'\dfrac4x'), (r'\dfrac{x+2}{x-1}', '(x+2)/(x-1)', '(x+2)/(x-1)', r'\dfrac{x+2}{x-1}'), (r'\sqrt{x-1}', 'sqrt(x-1)', 'x**2+1', r'x^2+1\ \ (x\geq0)')]
for _, fs, gs, _ in inv:
    if gs is None: continue
    F_ = sp.sympify(fs, locals={'x': xp}); G_ = sp.sympify(gs, locals={'x': xp})
    ok(sp.simplify(F_.subs(xp, G_) - xp) == 0 and sp.simplify(G_.subs(xp, F_) - xp) == 0, fs)
for t in (-3.0, 0.5, 2.0, 7.0): ok(abs(cr(t ** 3 - 4 + 4) - t) < 1e-9)
X.append(E(2, T(r"Calcula la funció inversa de:", r"Calcula la función inversa de:") + tasks(3, ['$f(x)=%s$' % i[0] for i in inv], gap='8pt')
    + recorda(T(r"canvia $f(x)$ per $y$, intercanvia $x$ i $y$, i aïlla $y$.", r"cambia $f(x)$ por $y$, intercambia $x$ e $y$, y despeja $y$.")),
    tasks(3, [r'$f^{-1}(x)=\res{%s}$' % i[3] for i in inv], gap='8pt') + T(r"Les funcions d) i e) són la seua pròpia inversa. En e): $x(y-1)=y+2\Rightarrow xy-y=x+2\Rightarrow y=\frac{x+2}{x-1}$.", r"Las funciones d) y e) son su propia inversa. En e): $x(y-1)=y+2\Rightarrow xy-y=x+2\Rightarrow y=\frac{x+2}{x-1}$.")))
ok(sp.simplify(2 * (x / 2 + 3) - 6 - x) == 0 and sp.simplify((2 * x - 6) / 2 + 3 - x) == 0)
X.append(E(2, T(r"Comprova que $f(x)=2x-6$ i $g(x)=\dfrac x2+3$ són inverses l'una de l'altra calculant $f\big(g(x)\big)$ i $g\big(f(x)\big)$. Representa-les en uns mateixos eixos juntament amb la recta $y=x$. Què observes?",
                r"Comprueba que $f(x)=2x-6$ y $g(x)=\dfrac x2+3$ son inversas la una de la otra calculando $f\big(g(x)\big)$ y $g\big(f(x)\big)$. Represéntalas en unos mismos ejes junto con la recta $y=x$. ¿Qué observas?"),
    r"$f\big(g(x)\big)=2\left(\frac x2+3\right)-6=x+6-6=\res{x}$; \ $g\big(f(x)\big)=\frac{2x-6}{2}+3=x-3+3=\res{x}$. " + T(r"Les gràfiques són simètriques respecte de la recta $y=x$ i es tallen sobre ella, en $(6,6)$.", r"Las gráficas son simétricas respecto de la recta $y=x$ y se cortan sobre ella, en $(6,6)$.")
    + G(Plot(-4, 9, -4, 9, W=230, lx=2, ly=2).seg(-4, -4, 9, 9, 'm', True).fn(lambda t: 2 * t - 6).fn(lambda t: t / 2 + 3, col='g').dot(6, 6, 'b'), 4.2)))
ckdom(lambda t: math.sqrt(t + 4), lambda t: t >= -4, (-4,))
X.append(E(2, T(r"Considera $f(x)=x^2-4$ només per a $x\geq0$. Calcula'n la inversa i indica el domini i el recorregut de $f$ i de $f^{-1}$. Per què cal la condició $x\geq0$?",
                r"Considera $f(x)=x^2-4$ solo para $x\geq0$. Calcula su inversa e indica el dominio y el recorrido de $f$ y de $f^{-1}$. ¿Por qué hace falta la condición $x\geq0$?"),
    T(r"$x=y^2-4\Rightarrow y^2=x+4\Rightarrow\res{f^{-1}(x)=\sqrt{x+4}}$. \ $D(f)=[0,+\infty)$, $R(f)=[-4,+\infty)$; \ $D(f^{-1})=\res{[-4,+\infty)}$, $R(f^{-1})=\res{[0,+\infty)}$: s'intercanvien. Sense la condició, dos valors de $x$ tindrien la mateixa imatge ($f(2)=f(-2)=0$) i la inversa no seria una funció.",
      r"$x=y^2-4\Rightarrow y^2=x+4\Rightarrow\res{f^{-1}(x)=\sqrt{x+4}}$. \ $D(f)=[0,+\infty)$, $R(f)=[-4,+\infty)$; \ $D(f^{-1})=\res{[-4,+\infty)}$, $R(f^{-1})=\res{[0,+\infty)}$: se intercambian. Sin la condición, dos valores de $x$ tendrían la misma imagen ($f(2)=f(-2)=0$) y la inversa no sería una función.")))
ok(abs(1.8 * 25 + 32 - 77) < 1e-9 and abs((212 - 32) / 1.8 - 100) < 1e-9 and abs((50 - 32) / 1.8 - 10) < 1e-9)
X.append(E(3, T(r"La funció $F(c)=1{,}8c+32$ transforma una temperatura en graus Celsius ($c$) en graus Fahrenheit.",
                r"La función $F(c)=1{,}8c+32$ transforma una temperatura en grados Celsius ($c$) en grados Fahrenheit.")
    + items(T("Quants graus Fahrenheit són 25 °C?", "¿Cuántos grados Fahrenheit son 25 °C?"),
            T("Calcula la funció inversa. Què fa aquesta funció?", "Calcula la función inversa. ¿Qué hace esta función?"),
            T("Quants graus Celsius són 212 °F? I 50 °F?", "¿Cuántos grados Celsius son 212 °F? ¿Y 50 °F?")),
    items(r"$F(25)=45+32=\res{77}$ °F",
          T(r"$f=1{,}8c+32\Rightarrow\res{C(f)=\dfrac{f-32}{1{,}8}}$: passa de graus Fahrenheit a graus Celsius.", r"$f=1{,}8c+32\Rightarrow\res{C(f)=\dfrac{f-32}{1{,}8}}$: pasa de grados Fahrenheit a grados Celsius."),
          r"$C(212)=\frac{180}{1{,}8}=\res{100}$ °C; \ $C(50)=\frac{18}{1{,}8}=\res{10}$ °C")))

# =====================================================================
# 9. Estudi complet
X = sec(T("Estudi complet d'una funció a partir de la gràfica", "Estudio completo de una función a partir de la gráfica"))
g37 = poly(Plot(-6, 7, -3, 5, W=320), [(-5, 0), (-3, 2), (0, -1)]).dot(-5, 0).dot(0, -1)
poly(g37, [(0, -2), (3, 4), (6, -2)]).dot(0, -2, open=True).dot(6, -2)
X.append(E(2, T(r"Fes l'estudi complet de la funció de la gràfica: domini, recorregut, punts de tall, continuïtat, creixement i decreixement, màxims i mínims, simetria i periodicitat.",
                r"Haz el estudio completo de la función de la gráfica: dominio, recorrido, puntos de corte, continuidad, crecimiento y decrecimiento, máximos y mínimos, simetría y periodicidad.") + G(g37, 6.4),
    T(r"$D=\res{[-5,6]}$, $R=\res{[-2,4]}$. Talls: $OX$: $\res{(-5,0),\ (-1,0),\ (1,0),\ (5,0)}$; $OY$: $\res{(0,-1)}$. Discontínua en $x=0$ (\rest{salt finit}: per l'esquerra arriba a $-1=f(0)$ i per la dreta comença en $-2$). Creixent en $\res{(-5,-3)\cup(0,3)}$; decreixent en $\res{(-3,0)\cup(3,6)}$. Màxim relatiu $\res{(-3,2)}$ i màxim absolut $\res{(3,4)}$; mínim absolut $\res{(6,-2)}$. No és simètrica ni periòdica.",
      r"$D=\res{[-5,6]}$, $R=\res{[-2,4]}$. Cortes: $OX$: $\res{(-5,0),\ (-1,0),\ (1,0),\ (5,0)}$; $OY$: $\res{(0,-1)}$. Discontinua en $x=0$ (\rest{salto finito}: por la izquierda llega a $-1=f(0)$ y por la derecha empieza en $-2$). Creciente en $\res{(-5,-3)\cup(0,3)}$; decreciente en $\res{(-3,0)\cup(3,6)}$. Máximo relativo $\res{(-3,2)}$ y máximo absoluto $\res{(3,4)}$; mínimo absoluto $\res{(6,-2)}$. No es simétrica ni periódica.")))
PB = [(0, 0), (1, 20), (2, 20), (3, 40), (5, 0)]
gb = poly(Plot(-.4, 5.6, -4, 46, sx=.5, sy=10, lx=1, ly=10, W=300), PB)
for q in PB: gb.dot(*q)
ok(40 - 20 * (4.5 - 3) == 10 and 20 * .5 == 10 and 40 / 2 == 20)
X.append(E(2, T(r"La gràfica mostra la distància a casa (en km) d'una ciclista durant una eixida, en funció del temps (en hores).", r"La gráfica muestra la distancia a casa (en km) de una ciclista durante una salida, en función del tiempo (en horas).") + G(gb, 6.2)
    + items(T("Indica el domini i el recorregut. Quant dura l'eixida i fins on arriba?", "Indica el dominio y el recorrido. ¿Cuánto dura la salida y hasta dónde llega?"),
            T("Estudia'n el creixement. Què passa entre la primera i la segona hora?", "Estudia su crecimiento. ¿Qué pasa entre la primera y la segunda hora?"),
            T("A quina velocitat torna cap a casa?", "¿A qué velocidad vuelve a casa?"),
            T("En quins moments està a 10 km de casa?", "¿En qué momentos está a 10 km de casa?")),
    items(T(r"$D=\res{[0,5]}$ i $R=\res{[0,40]}$: l'eixida dura 5 h i arriba a 40 km de casa (màxim absolut $(3,40)$).", r"$D=\res{[0,5]}$ y $R=\res{[0,40]}$: la salida dura 5 h y llega a 40 km de casa (máximo absoluto $(3,40)$)."),
          T(r"Creixent en $\res{(0,1)\cup(2,3)}$, constant en $\res{(1,2)}$ (està parada) i decreixent en $\res{(3,5)}$ (torna).", r"Creciente en $\res{(0,1)\cup(2,3)}$, constante en $\res{(1,2)}$ (está parada) y decreciente en $\res{(3,5)}$ (vuelve)."),
          T(r"Fa 40 km en 2 h: \rest{20 km/h}.", r"Hace 40 km en 2 h: \rest{20 km/h}."),
          T(r"Al cap de \rest{mitja hora} (anada) i de \rest{4 hores i mitja} (tornada).", r"A la \rest{media hora} (ida) y a las \rest{4 horas y media} (vuelta)."))))
g39 = poly(Plot(-5, 5, -4, 4, W=240), [(-4, -1), (-2, 3), (2, -3), (4, 1)]).dot(-4, -1).dot(4, 1).dot(-2, 3, 'b').dot(2, -3, 'b')
X.append(E(3, T(r"Dibuixa la gràfica d'una funció contínua i senar amb domini $[-4,4]$, creixent en $(-4,-2)\cup(2,4)$ i decreixent en $(-2,2)$, amb un màxim en $(-2,3)$ i tal que $f(4)=1$. Quin és el seu mínim? Quant val $f(0)$?",
                r"Dibuja la gráfica de una función continua e impar con dominio $[-4,4]$, creciente en $(-4,-2)\cup(2,4)$ y decreciente en $(-2,2)$, con un máximo en $(-2,3)$ y tal que $f(4)=1$. ¿Cuál es su mínimo? ¿Cuánto vale $f(0)$?"),
    T(r"Com que és senar, cada punt $(a,b)$ té el simètric $(-a,-b)$: el mínim és $\res{(2,-3)}$, $f(-4)=-1$ i $f(0)=\res{0}$. Per exemple:", r"Como es impar, cada punto $(a,b)$ tiene el simétrico $(-a,-b)$: el mínimo es $\res{(2,-3)}$, $f(-4)=-1$ y $f(0)=\res{0}$. Por ejemplo:") + G(g39, 4.2)))
ckroots('x**4-4*x**2', [-2, 0, 2]); ckroots('x/(x**2-1)', [0]); ckroots('sqrt(4-x**2)', [-2, 2])
ckdom(lambda t: t / nz(t * t - 1), lambda t: abs(t) != 1, (-1, 1)); ckdom(lambda t: math.sqrt(4 - t * t), lambda t: abs(t) <= 2, (-2, 2))
X.append(E(3, T(r"Sense dibuixar-les, troba el domini, els punts de tall amb els eixos i la simetria de:", r"Sin dibujarlas, halla el dominio, los puntos de corte con los ejes y la simetría de:") + tasks(3, ['$f(x)=x^4-4x^2$', r'$g(x)=\dfrac{x}{x^2-1}$', r'$h(x)=\sqrt{4-x^2}$']),
    tasks(1, [T(r"$D=\res{%s}$; $OX$: $\res{(-2,0),\ (0,0),\ (2,0)}$, $OY$: $\res{(0,0)}$; \rest{parella}.", r"$D=\res{%s}$; $OX$: $\res{(-2,0),\ (0,0),\ (2,0)}$, $OY$: $\res{(0,0)}$; \rest{par}.") % IR,
              T(r"$D=\res{%s-\{-1,1\}}$; talla els dos eixos en $\res{(0,0)}$; \rest{senar}.", r"$D=\res{%s-\{-1,1\}}$; corta los dos ejes en $\res{(0,0)}$; \rest{impar}.") % IR,
              T(r"$D=\res{[-2,2]}$; $OX$: $\res{(-2,0),\ (2,0)}$, $OY$: $\res{(0,2)}$; \rest{parella}.", r"$D=\res{[-2,2]}$; $OX$: $\res{(-2,0),\ (2,0)}$, $OY$: $\res{(0,2)}$; \rest{par}.")])))

PRE = r'''\usetikzlibrary{calc}
\usepackage{enumitem}
\definecolor{violet}{HTML}{7C3AED}
\definecolor{orange}{HTML}{EA8A1F}
'''
TIT = T('Estudi de funcions', 'Estudio de funciones')
build(HERE, 7, TIT, S,
      T("funcions, imatge, antiimatge, domini, recorregut, punts de tall, creixement, màxims i mínims, continuïtat, simetria, periodicitat, funció inversa",
        "funciones, imagen, antiimagen, dominio, recorrido, puntos de corte, crecimiento, máximos y mínimos, continuidad, simetría, periodicidad, función inversa"),
      T(r"Resol-los al quadern mostrant tots els passos. Escriu els intervals com als apunts: $(a,b)$ obert i $[a,b]$ tancat. Les seccions segueixen l'ordre dels apunts de la unitat (7.1--7.9).",
        r"Resuélvelos en el cuaderno mostrando todos los pasos. Escribe los intervalos como en los apuntes: $(a,b)$ abierto y $[a,b]$ cerrado. Las secciones siguen el orden de los apuntes de la unidad (7.1--7.9)."),
      T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. En els exercicis de «dibuixa una funció…» hi ha moltes respostes correctes: comprova que la teua complisca totes les condicions. Pots comprovar dominis, talls, simetries i inverses amb les eines interactives dels apunts de la unitat.",
        r"Intenta resolver cada ejercicio antes de mirar su solución. En los ejercicios de «dibuja una función…» hay muchas respuestas correctas: comprueba que la tuya cumpla todas las condiciones. Puedes comprobar dominios, cortes, simetrías e inversas con las herramientas interactivas de los apuntes de la unidad."),
      PRE, lang='es' if ES else 'va')
