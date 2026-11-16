# Genera t6-fitxa-exercicis.tex i t6-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 6: Funcions. Característiques)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py (curs='4eso-a').
# Les 8 seccions segueixen els apartats dels apunts (6.1-6.8): concepte de funció, domini i recorregut, punts de tall, continuïtat,
# creixement i extrems, periodicitat, interpretació de gràfics i construcció de funcions.
# Parteix de la fitxa de la unitat 7 de 4t ESO B (4eso-b-t7), sense simetries ni funció inversa, amb els dominis només de
# polinòmiques, racionals i arrels quadrades de radicand de primer grau, i amb dues seccions noves de problemes (7 i 8).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es). Les gràfiques es dibuixen amb la classe Plot de _eines/apunts/4eso-b-t7/fig.py (la mateixa
# dels apunts) i amb fig6.py dels apunts d'aquesta unitat. Comprovacions: sympy calcula talls i solucions, els dominis es comproven
# numèricament (ckdom) i les dades dels problemes, amb ok().
# Els intervals s'escriuen com a la resta de 4t: (a,b) obert i [a,b] tancat. Els decimals, dins de les fórmules, amb {,}.
# Ús: python3 genera.py && pdflatex t6-fitxa-exercicis.tex (dues vegades) && pdflatex t6-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '4eso-b-t7'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '4eso-a-t6'))
from eso4b import *
from fig import Plot, piece, sq, PI
import fig6
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
IR = r'\mathbb{R}'
SI, NO = r'\text{Sí}', r'\text{No}'

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
def ckroots(expr, sols, msg=''):
    got = sorted(sp.solve(sp.sympify(expr, locals={'x': x}), x), key=float)
    want = sorted([sp.sympify(s) for s in sols], key=float)
    ok(len(got) == len(want) and all(sp.simplify(a - b) == 0 for a, b in zip(got, want)), (msg, got, want))
def poly(P, pts, col='a', dots=True):
    for (a, b), (c, d) in zip(pts, pts[1:]): P.seg(a, b, c, d, col)
    if dots:
        for q in pts: P.dot(*q, col=col)
    return P
def lin(pts, t):
    """valor de la poligonal pts en t"""
    for (a, b), (c, d) in zip(pts, pts[1:]):
        if a <= t <= c: return b + (d - b) * (t - a) / (c - a)
    raise ValueError(t)

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
X.append(E(1, T(r"En cada situació, indica quina és la variable independent i quina la dependent, i si els punts de la gràfica s'han d'unir o no:", r"En cada situación, indica cuál es la variable independiente y cuál la dependiente, y si los puntos de la gráfica se deben unir o no:") + tasks(1, [
    T("El preu que paguem segons el nombre de llibretes que comprem.", "El precio que pagamos según el número de libretas que compramos."),
    T("L'altura d'una planta al llarg dels dies.", "La altura de una planta a lo largo de los días."),
    T("El temps que tardem a fer un trajecte segons la velocitat del cotxe.", "El tiempo que tardamos en hacer un trayecto según la velocidad del coche.")]),
    tasks(1, [T(r"Independent: \rest{nombre de llibretes}; dependent: \rest{preu}. \rest{No s'uneixen}: no es poden comprar 2,5 llibretes.", r"Independiente: \rest{número de libretas}; dependiente: \rest{precio}. \rest{No se unen}: no se pueden comprar 2,5 libretas."),
              T(r"Independent: \rest{temps}; dependent: \rest{altura}. \rest{S'uneixen}: la planta creix contínuament.", r"Independiente: \rest{tiempo}; dependiente: \rest{altura}. \rest{Se unen}: la planta crece continuamente."),
              T(r"Independent: \rest{velocitat}; dependent: \rest{temps}. \rest{S'uneixen}: la velocitat pot prendre qualsevol valor.", r"Independiente: \rest{velocidad}; dependiente: \rest{tiempo}. \rest{Se unen}: la velocidad puede tomar cualquier valor.")])))
f3 = lambda t: t * t - 2 * t - 3
ok(f3(-2) == 5 and f3(0) == -3 and f3(.5) == -3.75)
ckroots('x**2-2*x-3', [-1, 3]); ckroots('x**2-2*x-3+4', [1]); ckroots('x**2-2*x-3+6', [])
X.append(E(2, T(r"Donada la funció $f(x)=x^2-2x-3$, calcula:", r"Dada la función $f(x)=x^2-2x-3$, calcula:") + tasks(2, [
    T(r"Les imatges $f(-2)$, $f(0)$ i $f\left(\frac12\right)$.", r"Las imágenes $f(-2)$, $f(0)$ y $f\left(\frac12\right)$."),
    T(r"Les antiimatges de $0$, de $-4$ i de $-6$.", r"Las antiimágenes de $0$, de $-4$ y de $-6$.")])
    + recorda(T(r"per a la imatge de $a$ substituïm $x$ per $a$; per a les antiimatges de $b$ resolem l'equació $f(x)=b$.", r"para la imagen de $a$ sustituimos $x$ por $a$; para las antiimágenes de $b$ resolvemos la ecuación $f(x)=b$.")),
    tasks(1, [r'$f(-2)=4+4-3=\res{5}$; \ $f(0)=\res{-3}$; \ $f\left(\frac12\right)=\frac14-1-3=\res{-\frac{15}{4}}$',
              T(r"$x^2-2x-3=0\Rightarrow\res{x=-1,\ x=3}$; \ $x^2-2x+1=0\Rightarrow\res{x=1}$; \ $x^2-2x+3=0$, $\Delta=-8<0$: $-6$ \rest{no té antiimatges}.",
                r"$x^2-2x-3=0\Rightarrow\res{x=-1,\ x=3}$; \ $x^2-2x+1=0\Rightarrow\res{x=1}$; \ $x^2-2x+3=0$, $\Delta=-8<0$: $-6$ \rest{no tiene antiimágenes}.")])))
ok([3 * t - 2 for t in (-2, -1, 0, 1, 2)] == [-8, -5, -2, 1, 4])
X.append(E(1, T(r"Completa la taula de valors de la funció $f(x)=3x-2$ i dibuixa'n la gràfica. Quin valor de $x$ té per imatge 10?", r"Completa la tabla de valores de la función $f(x)=3x-2$ y dibuja su gráfica. ¿Qué valor de $x$ tiene por imagen 10?")
    + r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $-2$ & $-1$ & $0$ & $1$ & $2$\\\hline $f(x)$ & & & & & \\\hline\end{tabular}\end{center}",
    r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline $x$ & $-2$ & $-1$ & $0$ & $1$ & $2$\\\hline $f(x)$ & $\res{-8}$ & $\res{-5}$ & $\res{-2}$ & $\res{1}$ & $\res{4}$\\\hline\end{tabular}\end{center}"
    + T(r"La gràfica és una recta. \ ", r"La gráfica es una recta. \ ") + r"$3x-2=10\Rightarrow\res{x=4}$"
    + G(poly(Plot(-3, 3, -9, 5, sy=1, ly=2, W=200), [(-2, -8), (-1, -5), (0, -2), (1, 1), (2, 4)], 'a'), 2.8)))
X.append(E(2, T(r"Escriu la fórmula de cada funció:", r"Escribe la fórmula de cada función:") + tasks(2, [
    T("A cada nombre li fem correspondre el seu triple més 5.", "A cada número le hacemos corresponder su triple más 5."),
    T(r"L'àrea d'un quadrat en funció del costat $x$.", r"El área de un cuadrado en función del lado $x$."),
    T(r"El preu de $x$ kg de taronges a 1,20 €/kg.", r"El precio de $x$ kg de naranjas a 1,20 €/kg."),
    T("A cada nombre li fem correspondre la meitat del seu quadrat.", "A cada número le hacemos corresponder la mitad de su cuadrado.")]),
    tasks(4, [R('f(x)=3x+5'), R('A(x)=x^2'), R('P(x)=1{,}2x'), R(r'f(x)=\dfrac{x^2}{2}')])))

ok(sp.Rational(0 + 1, 0 - 2) == sp.Rational(-1, 2) and (3 + 1) / (3 - 2) == 4 and (-1 + 1) / (-1 - 2) == 0)
ckroots('(x+1)/(x-2)-2', [5]); ckroots('(x+1)/(x-2)-1', [])
X.append(E(2, T(r"Donada la funció $g(x)=\dfrac{x+1}{x-2}$:", r"Dada la función $g(x)=\dfrac{x+1}{x-2}$:") + tasks(2, [
    T(r"Calcula $g(0)$, $g(3)$ i $g(-1)$. Es pot calcular $g(2)$?", r"Calcula $g(0)$, $g(3)$ y $g(-1)$. ¿Se puede calcular $g(2)$?"),
    T(r"Calcula les antiimatges de 2 i d'1.", r"Calcula las antiimágenes de 2 y de 1.")]),
    tasks(1, [T(r"$g(0)=\res{-\frac12}$, \ $g(3)=\res{4}$, \ $g(-1)=\res{0}$. \ $g(2)=\frac30$ \rest{no existeix}: 2 no és del domini.", r"$g(0)=\res{-\frac12}$, \ $g(3)=\res{4}$, \ $g(-1)=\res{0}$. \ $g(2)=\frac30$ \rest{no existe}: 2 no es del dominio."),
              T(r"$\frac{x+1}{x-2}=2\Rightarrow x+1=2x-4\Rightarrow\res{x=5}$. \ $\frac{x+1}{x-2}=1\Rightarrow x+1=x-2\Rightarrow 1=-2$: l'1 \rest{no té antiimatges}.", r"$\frac{x+1}{x-2}=2\Rightarrow x+1=2x-4\Rightarrow\res{x=5}$. \ $\frac{x+1}{x-2}=1\Rightarrow x+1=x-2\Rightarrow 1=-2$: el 1 \rest{no tiene antiimágenes}.")])))

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
      (r'\dfrac{4}{2x+6}', lambda t: 4 / nz(2 * t + 6), lambda t: t != -3, (-3,), IR + r'-\{-3\}'),
      (r'\dfrac{x+2}{x^2-9}', lambda t: (t + 2) / nz(t * t - 9), lambda t: abs(t) != 3, (-3, 3), IR + r'-\{-3,3\}'),
      (r'\dfrac{x-1}{x^2+4}', lambda t: (t - 1) / (t * t + 4), lambda t: True, (), IR),
      (r'\dfrac{5}{x^2-6x}', lambda t: 5 / nz(t * t - 6 * t), lambda t: t not in (0, 6), (0, 6), IR + r'-\{0,6\}')]
e6 = [(r'\sqrt{x+7}', lambda t: math.sqrt(t + 7), lambda t: t >= -7, (-7,), co('-7', r'+\infty')),
      (r'\sqrt{2x-6}', lambda t: math.sqrt(2 * t - 6), lambda t: t >= 3, (3,), co('3', r'+\infty')),
      (r'\sqrt{10-5x}', lambda t: math.sqrt(10 - 5 * t), lambda t: t <= 2, (2,), oc(r'-\infty', '2')),
      (r'\dfrac{1}{\sqrt{x-2}}', lambda t: 1 / nz(math.sqrt(t - 2)), lambda t: t > 2, (2,), oo('2', r'+\infty')),
      (r'\dfrac{3}{\sqrt{4-x}}', lambda t: 3 / nz(math.sqrt(4 - t)), lambda t: t < 4, (4,), oo(r'-\infty', '4')),
      (r'\sqrt{x}+\dfrac{1}{x-9}', lambda t: math.sqrt(t) + 1 / nz(t - 9), lambda t: t >= 0 and t != 9, (0, 9), co('0', '9') + r'\cup' + oo('9', r'+\infty'))]
for tx, f, inD, ed, _ in e5 + e6: ckdom(f, inD, ed, tx)
X.append(E(1, T(r"Calcula el domini d'aquestes funcions polinòmiques i racionals:", r"Calcula el dominio de estas funciones polinómicas y racionales:") + tasks(3, ['$f(x)=%s$' % e[0] for e in e5], gap='8pt')
    + recorda(T(r"una funció polinòmica existeix sempre; en una racional, el denominador no pot valdre 0.", r"una función polinómica existe siempre; en una racional, el denominador no puede valer 0.")),
    tasks(3, [R(e[4]) for e in e5])))
X.append(E(2, T(r"Calcula el domini d'aquestes funcions amb arrels:", r"Calcula el dominio de estas funciones con raíces:") + tasks(3, ['$f(x)=%s$' % e[0] for e in e6], gap='8pt')
    + recorda(T(r"el radicand d'una arrel quadrada ha de ser $\geq0$, i $>0$ si l'arrel és en un denominador. En dividir per un nombre negatiu, la desigualtat canvia de sentit.", r"el radicando de una raíz cuadrada debe ser $\geq0$, y $>0$ si la raíz está en un denominador. Al dividir por un número negativo, la desigualdad cambia de sentido.")),
    tasks(3, [R(e[4]) for e in e6])))
ckdom(lambda t: math.sqrt(t - 3), lambda t: t >= 3, (3,))
X.append(E(1, T(r"Pertanyen $x=1$, $x=3$ i $x=7$ al domini de $f(x)=\sqrt{x-3}$? Justifica-ho substituint, i després calcula el domini complet.", r"¿Pertenecen $x=1$, $x=3$ y $x=7$ al dominio de $f(x)=\sqrt{x-3}$? Justifícalo sustituyendo, y después calcula el dominio completo."),
    T(r"$f(1)=\sqrt{-2}$ no existeix: $\res{1\notin D(f)}$. \ $f(3)=\sqrt0=0$: $\res{3\in D(f)}$. \ $f(7)=\sqrt4=2$: $\res{7\in D(f)}$. \ $x-3\geq0\Rightarrow D(f)=\res{[3,+\infty)}$",
      r"$f(1)=\sqrt{-2}$ no existe: $\res{1\notin D(f)}$. \ $f(3)=\sqrt0=0$: $\res{3\in D(f)}$. \ $f(7)=\sqrt4=2$: $\res{7\in D(f)}$. \ $x-3\geq0\Rightarrow D(f)=\res{[3,+\infty)}$")))
for t in [i / 7 for i in range(-200, 201)]: assert t * t + 2 >= 2 and 5 - t * t <= 5 and 2 * t + 1 == 2 * t + 1
X.append(E(2, T(r"Raonant quins valors pot prendre $y$, calcula el recorregut de:", r"Razonando qué valores puede tomar $y$, calcula el recorrido de:") + tasks(4, [r'$f(x)=2x+1$', r'$g(x)=x^2+2$', r'$h(x)=\sqrt{x-1}+3$', r'$k(x)=5-x^2$']),
    tasks(2, [T(r'una recta no horitzontal pren tots els valors: $R=\res{%s}$', r'una recta no horizontal toma todos los valores: $R=\res{%s}$') % IR, r'$x^2\geq0\Rightarrow R=\res{[2,+\infty)}$',
              r'$\sqrt{x-1}\geq0\Rightarrow R=\res{[3,+\infty)}$', r'$-x^2\le0\Rightarrow R=\res{(-\infty,5]}$'])))

ckdom(lambda t: 1 / nz(t - 4), lambda t: t != 4, (4,)); ckdom(lambda t: math.sqrt(t - 2), lambda t: t >= 2, (2,)); ckdom(lambda t: 1 / nz(math.sqrt(5 - t)), lambda t: t < 5, (5,))
X.append(E(3, T(r"Escriu la fórmula d'una funció que tinga per domini:", r"Escribe la fórmula de una función que tenga por dominio:") + tasks(3, [r'$\mathbb{R}-\{4\}$', r'$[2,+\infty)$', r'$(-\infty,5)$']),
    T(r"Per exemple (n'hi ha moltes): ", r"Por ejemplo (hay muchas): ") + tasks(3, [R(r'f(x)=\dfrac{1}{x-4}'), R(r'f(x)=\sqrt{x-2}'), R(r'f(x)=\dfrac{1}{\sqrt{5-x}}')])))

# =====================================================================
# 3. Punts de tall
X = sec(T('Punts de tall amb els eixos', 'Puntos de corte con los ejes'))
c3 = [('2x-6', '2*x-6', [3], '-6'), ('-3x+12', '-3*x+12', [4], '12'), ('x^2-16', 'x**2-16', [-4, 4], '-16'), ('x^2+5x', 'x**2+5*x', [-5, 0], '0'),
      ('x^2-5x+4', 'x**2-5*x+4', [1, 4], '4'), ('x^2+2x+5', 'x**2+2*x+5', [], '5'), (r'\dfrac{x+4}{x-2}', '(x+4)/(x-2)', [-4], '-2'), (r'\sqrt{x+9}-2', 'sqrt(x+9)-2', [-5], '1')]
for _, e, rr, y0 in c3:
    ckroots(e, rr, e); ok(sp.sympify(e, locals={'x': x}).subs(x, 0) == sp.sympify(y0), e)
def tall(rr, y0):
    return r'$OY$: $\res{(0,%s)}$; ' % y0 + (r'$OX$: $\res{' + r',\ '.join('(%d,0)' % v for v in rr) + '}$' if rr else r'$OX$: ' + T('no en té', 'no tiene'))
X.append(E(1, T(r"Troba els punts de tall amb els eixos de coordenades:", r"Halla los puntos de corte con los ejes de coordenadas:") + tasks(4, ['$f(x)=%s$' % c[0] for c in c3], gap='8pt')
    + recorda(T(r"tall amb $OY$: fem $x=0$; talls amb $OX$: resolem $f(x)=0$.", r"corte con $OY$: hacemos $x=0$; cortes con $OX$: resolvemos $f(x)=0$.")),
    tasks(2, [tall(c[2], c[3]) for c in c3])))
gc = poly(Plot(-6, 7, -4, 5, W=260), [(-5, -2), (-3, 2), (1, -2), (4, 4), (6, 2)])
ok(lin([(-5, -2), (-3, 2)], -4) == 0 and lin([(-3, 2), (1, -2)], -1) == 0 and lin([(-3, 2), (1, -2)], 0) == -1 and lin([(1, -2), (4, 4)], 2) == 0)
X.append(E(1, T(r"Escriu els punts de tall amb els eixos de la funció representada.", r"Escribe los puntos de corte con los ejes de la función representada.") + G(gc, 4.6),
    T(r"$OX$: $\res{(-4,0),\ (-1,0),\ (2,0)}$; \ $OY$: $\res{(0,-1)}$.", r"$OX$: $\res{(-4,0),\ (-1,0),\ (2,0)}$; \ $OY$: $\res{(0,-1)}$.")))
ckroots('x**2+x-6', [-3, 2])
X.append(E(2, T(r"Troba el valor de $a$ perquè la funció $f(x)=x^2+ax-6$ talle l'eix $OX$ en $x=2$. On el talla l'altra vegada? I on talla l'eix $OY$?",
                r"Halla el valor de $a$ para que la función $f(x)=x^2+ax-6$ corte el eje $OX$ en $x=2$. ¿Dónde lo corta la otra vez? ¿Y dónde corta el eje $OY$?"),
    T(r"$f(2)=4+2a-6=0\Rightarrow\res{a=1}$. \ $x^2+x-6=0\Rightarrow$ l'altre tall és $\res{(-3,0)}$. \ $OY$: $\res{(0,-6)}$.", r"$f(2)=4+2a-6=0\Rightarrow\res{a=1}$. \ $x^2+x-6=0\Rightarrow$ el otro corte es $\res{(-3,0)}$. \ $OY$: $\res{(0,-6)}$.")))
ok(sp.expand(2 * (x + 1) * (x - 4)) == 2 * x ** 2 - 6 * x - 8)
X.append(E(3, T(r"Escriu l'expressió d'una funció de segon grau que talle l'eix $OX$ en $x=-1$ i en $x=4$, i l'eix $OY$ en el punt $(0,-8)$.",
                r"Escribe la expresión de una función de segundo grado que corte el eje $OX$ en $x=-1$ y en $x=4$, y el eje $OY$ en el punto $(0,-8)$."),
    T(r"Si s'anul·la en $-1$ i en $4$, és $f(x)=a(x+1)(x-4)$. \ $f(0)=-4a=-8\Rightarrow a=2$: \ $\res{f(x)=2(x+1)(x-4)=2x^2-6x-8}$",
      r"Si se anula en $-1$ y en $4$, es $f(x)=a(x+1)(x-4)$. \ $f(0)=-4a=-8\Rightarrow a=2$: \ $\res{f(x)=2(x+1)(x-4)=2x^2-6x-8}$")))

ckroots('x**3-4*x', [-2, 0, 2]); ckroots('x**3-x**2-6*x', [-2, 0, 3]); ok(sp.factor(x ** 3 - x ** 2 - 6 * x) == x * (x - 3) * (x + 2))
X.append(E(2, T(r"Troba els punts de tall amb els eixos traient factor comú i factoritzant:", r"Halla los puntos de corte con los ejes sacando factor común y factorizando:") + tasks(2, [r'$f(x)=x^3-4x$', r'$g(x)=x^3-x^2-6x$']),
    tasks(1, [r'$x(x^2-4)=x(x-2)(x+2)=0$: $OX$: $\res{(-2,0),\ (0,0),\ (2,0)}$; $OY$: $\res{(0,0)}$',
              r'$x(x^2-x-6)=x(x-3)(x+2)=0$: $OX$: $\res{(-2,0),\ (0,0),\ (3,0)}$; $OY$: $\res{(0,0)}$'])))

# =====================================================================
# 4. Continuïtat
X = sec(T('Continuïtat i tipus de discontinuïtats', 'Continuidad y tipos de discontinuidades'))
g5 = Plot(-6, 6, -2, 5, W=320)
g5.fn(lambda t: t / 2 + 3, -6, 0).dot(-3, 1.5, open=True).dot(-3, 3.5).dot(0, 3, open=True)
g5.fn(lambda t: 1 - t / 2, 0, 2).dot(0, 1).dot(2, 0, open=True).fn(lambda t: 1 / (t - 2), 2.02, 6).vl(2)
def c16(): return Plot(-1, 5, -2, 5, W=170)
g16 = [c16().fn(lambda t: 3 + (t - 2) / 2 - (t - 2) ** 2 / 4).dot(2, 3, open=True),
       c16().fn(lambda t: (t - 2) / 2 + 1, -1, 2).dot(2, 1).fn(lambda t: 3 + (t - 2) ** 2 / 3, 2, 5).dot(2, 3, open=True),
       c16().fn(lambda t: abs(t - 2) + 1).dot(2, 1),
       c16().fn(lambda t: 1 / (t - 2) + 1 if abs(t - 2) > 1e-9 else None).vl(2)]
EV, SF, SIN, AS, CO = (T(r'\text{evitable}', r'\text{evitable}'), T(r'\text{salt finit}', r'\text{salto finito}'), T(r'\text{salt infinit}', r'\text{salto infinito}'),
                       T(r'\text{asimptòtica}', r'\text{asintótica}'), T(r'\text{Contínua}', r'\text{Continua}'))
X.append(E(1, T(r"Estudia la continuïtat de cada funció en $x=2$. Si és discontínua, classifica la discontinuïtat i, si és evitable, indica quin valor hauria de tindre $f(2)$ perquè la funció fora contínua.",
                r"Estudia la continuidad de cada función en $x=2$. Si es discontinua, clasifica la discontinuidad y, si es evitable, indica qué valor debería tener $f(2)$ para que la función fuera continua.") + tasks(4, [Gi(p) for p in g16]),
    tasks(1, [T(r"Discontinuïtat $\res{%s}$: els dos costats arriben a 3, però $f(2)$ no existeix. Seria contínua si $\res{f(2)=3}$.", r"Discontinuidad $\res{%s}$: los dos lados llegan a 3, pero $f(2)$ no existe. Sería continua si $\res{f(2)=3}$.") % EV,
              T(r"Discontinuïtat de $\res{%s}$: per l'esquerra arriba a 1 (i $f(2)=1$) i per la dreta a 3.", r"Discontinuidad de $\res{%s}$: por la izquierda llega a 1 (y $f(2)=1$) y por la derecha a 3.") % SF,
              T(r"$\res{%s}$: els dos costats arriben a 1 i $f(2)=1$. Té un pic, però es dibuixa sense alçar el llapis.", r"$\res{%s}$: los dos lados llegan a 1 y $f(2)=1$. Tiene un pico, pero se dibuja sin levantar el lápiz.") % CO,
              T(r"Discontinuïtat $\res{%s}$: per l'esquerra se'n va a $-\infty$ i per la dreta a $+\infty$ (asímptota vertical $x=2$).", r"Discontinuidad $\res{%s}$: por la izquierda se va a $-\infty$ y por la derecha a $+\infty$ (asíntota vertical $x=2$).") % AS])))
X.append(E(2, T(r"Indica en quins punts és discontínua aquesta funció i classifica cada discontinuïtat.", r"Indica en qué puntos es discontinua esta función y clasifica cada discontinuidad.") + G(g5, 6.2),
    T(r"$x=-3$: $\res{%s}$ (el punt està fora de lloc). \ $x=0$: $\res{%s}$ (de 3 a 1). \ $x=2$: $\res{%s}$ (per l'esquerra arriba a 0 i per la dreta se'n va a $+\infty$).",
      r"$x=-3$: $\res{%s}$ (el punto está fuera de lugar). \ $x=0$: $\res{%s}$ (de 3 a 1). \ $x=2$: $\res{%s}$ (por la izquierda llega a 0 y por la derecha se va a $+\infty$).") % (EV, SF, SIN)))
g23 = Plot(-3, 7, -2, 6, W=260).fn(lambda t: t + 1, -3, 1).dot(1, 2).fn(lambda t: t - 1, 1, 7).dot(1, 0, open=True).dot(4, 3, open=True).dot(4, 5)
X.append(E(2, T(r"Dibuixa la gràfica d'una funció amb domini $\mathbb{R}$ que tinga una discontinuïtat de salt finit en $x=1$ i una d'evitable en $x=4$, i que siga contínua en la resta de punts.",
                r"Dibuja la gráfica de una función con dominio $\mathbb{R}$ que tenga una discontinuidad de salto finito en $x=1$ y una evitable en $x=4$, y que sea continua en el resto de puntos."),
    T(r"Per exemple (n'hi ha moltes):", r"Por ejemplo (hay muchas):") + G(g23, 4.6)))
ok([1.5 + 1 * k for k in range(4)] == [1.5, 2.5, 3.5, 4.5])
pk = Plot(-.4, 4.6, -.8, 5.5, W=260)
for a, y in ((0, 1.5), (1, 2.5), (2, 3.5), (3, 4.5)): pk.seg(a, y, a + 1, y).dot(a, y, open=True).dot(a + 1, y)
X.append(E(2, T(r"Un servei de lloguer de patinets cobra 1,50 € per la primera hora (o fracció) i 1 € per cada hora més (o fracció), fins a un màxim de 4 hores.",
                r"Un servicio de alquiler de patinetes cobra 1,50 € por la primera hora (o fracción) y 1 € por cada hora más (o fracción), hasta un máximo de 4 horas.")
    + items(T("Quant es paga per 40 minuts? I per 1 hora i 20 minuts? I per 3 hores justes?", "¿Cuánto se paga por 40 minutos? ¿Y por 1 hora y 20 minutos? ¿Y por 3 horas justas?"),
            T("Dibuixa la gràfica del preu en funció del temps (en hores).", "Dibuja la gráfica del precio en función del tiempo (en horas)."),
            T("És contínua? Quin tipus de discontinuïtats té? Quin és el recorregut?", "¿Es continua? ¿Qué tipo de discontinuidades tiene? ¿Cuál es el recorrido?")),
    items(T(r"40 min: \rest{1,50 €}; \ 1 h 20 min (dues hores començades): \rest{2,50 €}; \ 3 h justes: \rest{3,50 €}.", r"40 min: \rest{1,50 €}; \ 1 h 20 min (dos horas empezadas): \rest{2,50 €}; \ 3 h justas: \rest{3,50 €}."),
          T(r"És una funció «a escalons»:", r"Es una función «a escalones»:") + G(pk, 3.8),
          T(r"No: té \rest{discontinuïtats de salt finit} en $x=1$, $x=2$ i $x=3$ (el preu puja 1 € de colp). $R=\res{\{1{,}5;\ 2{,}5;\ 3{,}5;\ 4{,}5\}}$.", r"No: tiene \rest{discontinuidades de salto finito} en $x=1$, $x=2$ y $x=3$ (el precio sube 1 € de golpe). $R=\res{\{1{,}5;\ 2{,}5;\ 3{,}5;\ 4{,}5\}}$."))))

g15 = Plot(-6, 7, -2, 7, W=320)
g15.fn(lambda t: t + 5, -6, -3).dot(-6, -1).dot(-3, 2, open=True).dot(-3, 4)
g15.fn(lambda t: 2 - (t + 3) / 2, -3, 1).dot(1, 0)
g15.fn(lambda t: 2 / (t - 1), 1.05, 3).dot(3, 1, open=True).vl(1)
g15.fn(lambda t: t - 1, 3, 7).dot(3, 2)
ok(-3 + 5 == 2 - 0 / 2 and 2 - (1 + 3) / 2 == 0 and 2 / (3 - 1) == 1 and 3 - 1 == 2)
X.append(E(3, T(r"Indica en quins punts és discontínua aquesta funció i classifica cada discontinuïtat. Quin és el seu domini?", r"Indica en qué puntos es discontinua esta función y clasifica cada discontinuidad. ¿Cuál es su dominio?") + G(g15, 6.2),
    T(r"$D=\res{[-6,7]}$. \ $x=-3$: $\res{%s}$ (els dos costats arriben a 2, però $f(-3)=4$). \ $x=1$: $\res{%s}$ (per l'esquerra arriba a 0 i per la dreta se'n va a $+\infty$). \ $x=3$: $\res{%s}$ (per l'esquerra arriba a 1 i $f(3)=2$).",
      r"$D=\res{[-6,7]}$. \ $x=-3$: $\res{%s}$ (los dos lados llegan a 2, pero $f(-3)=4$). \ $x=1$: $\res{%s}$ (por la izquierda llega a 0 y por la derecha se va a $+\infty$). \ $x=3$: $\res{%s}$ (por la izquierda llega a 1 y $f(3)=2$).") % (EV, SIN, SF)))

# =====================================================================
# 5. Creixement, màxims i mínims
X = sec(T('Creixement i decreixement. Màxims i mínims', 'Crecimiento y decrecimiento. Máximos y mínimos'))
P4 = [(-5, -2), (-3, 3), (-1, 1), (1, 4), (3, -3), (6, 2)]
g4 = poly(Plot(-6, 7, -4, 5, W=300), P4)
X.append(E(1, T(r"Observa la gràfica i indica'n el domini, el recorregut, els intervals de creixement i de decreixement, i els màxims i mínims (relatius i absoluts).",
                r"Observa la gráfica e indica su dominio, el recorrido, los intervalos de crecimiento y de decrecimiento, y los máximos y mínimos (relativos y absolutos).") + G(g4, 6),
    T(r"$D=\res{[-5,6]}$, $R=\res{[-3,4]}$. Creixent en $\res{(-5,-3)\cup(-1,1)\cup(3,6)}$; decreixent en $\res{(-3,-1)\cup(1,3)}$. Màxims: $\res{(-3,3)}$ relatiu i $\res{(1,4)}$ absolut. Mínims: $\res{(-1,1)}$ relatiu i $\res{(3,-3)}$ absolut.",
      r"$D=\res{[-5,6]}$, $R=\res{[-3,4]}$. Creciente en $\res{(-5,-3)\cup(-1,1)\cup(3,6)}$; decreciente en $\res{(-3,-1)\cup(1,3)}$. Máximos: $\res{(-3,3)}$ relativo y $\res{(1,4)}$ absoluto. Mínimos: $\res{(-1,1)}$ relativo y $\res{(3,-3)}$ absoluto.")))
fp = lambda t: -t * t + 4 * t
ok(fp(2) == 4 and fp(0) == 0 and fp(4) == 0)
X.append(E(1, T(r"La gràfica és la de $f(x)=-x^2+4x$. Indica'n els intervals de creixement i de decreixement i el màxim. Comprova amb la fórmula les coordenades del màxim i dels talls amb l'eix $OX$.",
                r"La gráfica es la de $f(x)=-x^2+4x$. Indica sus intervalos de crecimiento y de decrecimiento y el máximo. Comprueba con la fórmula las coordenadas del máximo y de los cortes con el eje $OX$.") + G(Plot(-2, 6, -4, 5, W=230).fn(fp).dot(2, 4), 3.8),
    T(r"Creixent en $\res{(-\infty,2)}$ i decreixent en $\res{(2,+\infty)}$; màxim absolut en $\res{(2,4)}$: $f(2)=-4+8=4$. No té mínims. Talls: $-x^2+4x=0\Rightarrow x(4-x)=0\Rightarrow(0,0)$ i $(4,0)$.",
      r"Creciente en $\res{(-\infty,2)}$ y decreciente en $\res{(2,+\infty)}$; máximo absoluto en $\res{(2,4)}$: $f(2)=-4+8=4$. No tiene mínimos. Cortes: $-x^2+4x=0\Rightarrow x(4-x)=0\Rightarrow(0,0)$ y $(4,0)$.")))
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
TT = [(0, 8), (2, 6), (4, 5), (6, 7), (8, 12), (10, 16), (12, 19), (14, 21), (16, 20), (18, 16), (20, 13), (22, 11), (24, 9)]
ok(max(v for _, v in TT) == 21 and min(v for _, v in TT) == 5)
X.append(E(2, T(r"La taula dona la temperatura (en °C) mesurada cada 2 hores al llarg d'un dia. Representa-la i descriu com varia la temperatura: quan puja, quan baixa, quina és la màxima i quina la mínima.",
                r"La tabla da la temperatura (en °C) medida cada 2 horas a lo largo de un día. Represéntala y describe cómo varía la temperatura: cuándo sube, cuándo baja, cuál es la máxima y cuál la mínima.")
    + r"\begin{center}\small\renewcommand{\arraystretch}{1.25}\setlength{\tabcolsep}{4pt}\begin{tabular}{|c|" + "c|" * len(TT) + r"}\hline " + T('Hora', 'Hora') + " & " + " & ".join(str(a) for a, _ in TT) + r"\\\hline °C & " + " & ".join(str(b) for _, b in TT) + r"\\\hline\end{tabular}\end{center}",
    G(poly(Plot(-1, 25, -1, 23, sx=2, sy=2, lx=4, ly=4, W=320), TT), 6)
    + T(r"Baixa de les 0 h a les \rest{4 h}, puja de les 4 h a les \rest{14 h} i torna a baixar fins a les 24 h. Mínima: \rest{5 °C a les 4 h}; màxima: \rest{21 °C a les 14 h}. Unim els punts perquè la temperatura canvia contínuament (les dades són aproximades entre les mesures).",
        r"Baja de las 0 h a las \rest{4 h}, sube de las 4 h a las \rest{14 h} y vuelve a bajar hasta las 24 h. Mínima: \rest{5 °C a las 4 h}; máxima: \rest{21 °C a las 14 h}. Unimos los puntos porque la temperatura cambia continuamente (los datos son aproximados entre las medidas).")))

PD = [(0, 0), (2, 30), (5, 30), (7, 50), (10, 20), (12, 0)]
gd = poly(Plot(-1, 13, -5, 55, sx=1, sy=10, lx=2, ly=10, W=300), PD)
ok(lin(PD, 9) == 30 and lin(PD, 1) == 15)
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
# 6. Periodicitat
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
X.append(E(3, T(r"Una funció periòdica de període 4 val $f(x)=|x-2|$ en l'interval $[0,4]$. Dibuixa'n la gràfica entre $x=-4$ i $x=8$ i calcula $f(13)$.",
                r"Una función periódica de periodo 4 vale $f(x)=|x-2|$ en el intervalo $[0,4]$. Dibuja su gráfica entre $x=-4$ y $x=8$ y calcula $f(13)$."),
    G(Plot(-5, 9, -1, 3, W=380).fn(f31, -4, 8, n=1200).fn(f31, 0, 4, 'b', n=400), 8) + r'$f(13)=f(1+3\cdot4)=f(1)=|1-2|=\res{1}$'))

X.append(E(1, T(r"Quines d'aquestes situacions es poden descriure amb una funció periòdica? Si ho és, indica'n el període.", r"¿Cuáles de estas situaciones se pueden describir con una función periódica? Si lo es, indica su periodo.") + tasks(1, [
    T("La posició de l'agulla dels minuts d'un rellotge al llarg del dia.", "La posición de la aguja de los minutos de un reloj a lo largo del día."),
    T("L'altura d'una persona al llarg de la seua vida.", "La altura de una persona a lo largo de su vida."),
    T("El color d'un semàfor que està 40 s en roig, 5 s en ambre i 35 s en verd.", "El color de un semáforo que está 40 s en rojo, 5 s en ámbar y 35 s en verde."),
    T("El preu de la gasolina al llarg d'un any.", "El precio de la gasolina a lo largo de un año.")]),
    tasks(1, [T(r"\rest{Sí}: es repeteix cada hora, $T=\res{60\text{ min}}$.", r"\rest{Sí}: se repite cada hora, $T=\res{60\text{ min}}$."),
              T(r"\rest{No}: creix fins a l'edat adulta i no es repeteix.", r"\rest{No}: crece hasta la edad adulta y no se repite."),
              T(r"\rest{Sí}: $T=40+5+35=\res{80\text{ s}}$.", r"\rest{Sí}: $T=40+5+35=\res{80\text{ s}}$."),
              T(r"\rest{No}: puja i baixa, però no es repeteix de manera regular.", r"\rest{No}: sube y baja, pero no se repite de manera regular.")])))

# =====================================================================
# 7. Interpretació de gràfics
X = sec(T('Interpretació de gràfics', 'Interpretación de gráficos'))
DIP = fig6.DIP
ok(lin(DIP, 5) == 100 and lin(DIP, 20) == 100 and lin(DIP, 12) == 200 and 200 / 10 == 20)
X.append(E(1, T(r"La gràfica mostra el volum d'aigua (en litres) d'un dipòsit en funció del temps (en minuts).", r"La gráfica muestra el volumen de agua (en litros) de un depósito en función del tiempo (en minutos).") + G(fig6.dip(), 6)
    + items(T("Quines són les variables? Indica el domini i el recorregut i explica què signifiquen.", "¿Cuáles son las variables? Indica el dominio y el recorrido y explica qué significan."),
            T("Explica què passa en cada tram i a quin ritme (litres per minut).", "Explica qué pasa en cada tramo y a qué ritmo (litros por minuto)."),
            T("Quants litres hi ha al cap de 12 minuts? Quan hi ha 100 litres?", "¿Cuántos litros hay a los 12 minutos? ¿Cuándo hay 100 litros?")),
    items(T(r"Independent: temps (min); dependent: volum (L). $D=\res{[0,25]}$: tot dura 25 minuts. $R=\res{[0,200]}$: el dipòsit té entre 0 i 200 L.", r"Independiente: tiempo (min); dependiente: volumen (L). $D=\res{[0,25]}$: todo dura 25 minutos. $R=\res{[0,200]}$: el depósito tiene entre 0 y 200 L."),
          T(r"En $(0,10)$ \rest{s'omple a 20 L/min}; en $(10,15)$ \rest{es manté ple} (200 L); en $(15,25)$ \rest{es buida a 20 L/min}.", r"En $(0,10)$ \rest{se llena a 20 L/min}; en $(10,15)$ \rest{se mantiene lleno} (200 L); en $(15,25)$ \rest{se vacía a 20 L/min}."),
          T(r"Als 12 min: \rest{200 L}. Hi ha 100 L \rest{als 5 min} i \rest{als 20 min}.", r"A los 12 min: \rest{200 L}. Hay 100 L \rest{a los 5 min} y \rest{a los 20 min}."))))
PB = [(0, 0), (1, 20), (2, 20), (3, 40), (5, 0)]
gb = poly(Plot(-.4, 5.6, -4, 46, sx=.5, sy=10, lx=1, ly=10, W=300), PB)
ok(lin(PB, .5) == 10 and lin(PB, 4.5) == 10 and 40 / 2 == 20)
X.append(E(2, T(r"La gràfica mostra la distància a casa (en km) d'una ciclista durant una eixida, en funció del temps (en hores).", r"La gráfica muestra la distancia a casa (en km) de una ciclista durante una salida, en función del tiempo (en horas).") + G(gb, 6.2)
    + items(T("Indica el domini i el recorregut. Quant dura l'eixida i fins on arriba?", "Indica el dominio y el recorrido. ¿Cuánto dura la salida y hasta dónde llega?"),
            T("Estudia'n el creixement. Què passa entre la primera i la segona hora?", "Estudia su crecimiento. ¿Qué pasa entre la primera y la segunda hora?"),
            T("A quina velocitat torna cap a casa?", "¿A qué velocidad vuelve a casa?"),
            T("En quins moments està a 10 km de casa?", "¿En qué momentos está a 10 km de casa?")),
    items(T(r"$D=\res{[0,5]}$ i $R=\res{[0,40]}$: l'eixida dura 5 h i arriba a 40 km de casa (màxim absolut $(3,40)$).", r"$D=\res{[0,5]}$ y $R=\res{[0,40]}$: la salida dura 5 h y llega a 40 km de casa (máximo absoluto $(3,40)$)."),
          T(r"Creixent en $\res{(0,1)\cup(2,3)}$, constant en $\res{(1,2)}$ (està parada) i decreixent en $\res{(3,5)}$ (torna).", r"Creciente en $\res{(0,1)\cup(2,3)}$, constante en $\res{(1,2)}$ (está parada) y decreciente en $\res{(3,5)}$ (vuelve)."),
          T(r"Fa 40 km en 2 h: \rest{20 km/h}.", r"Hace 40 km en 2 h: \rest{20 km/h}."),
          T(r"Al cap de \rest{mitja hora} (anada) i de \rest{4 hores i mitja} (tornada).", r"A la \rest{media hora} (ida) y a las \rest{4 horas y media} (vuelta)."))))
def mini(pts):
    p = Plot(-.4, 6.4, -.6, 4.6, ticks=False, grid=False, W=170)
    return poly(p, pts, dots=False).text(5.9, -.35, 't').text(-.1, 4.35, 'd')
GR4 = [mini([(0, 0), (2, 3), (4, 3), (6, 0)]), mini([(0, 0), (3, 3.5), (6, 3.5)]), mini([(0, 1), (3, 1), (6, 4)]), mini([(0, 0), (3, 3), (6, 0)])]
X.append(E(1, T(r"Les gràfiques representen la distància a casa ($d$) en funció del temps ($t$). Relaciona cada situació amb la seua gràfica:", r"Las gráficas representan la distancia a casa ($d$) en función del tiempo ($t$). Relaciona cada situación con su gráfica:")
    + '\\begin{tasks}[label=\\arabic*.](4)\n' + ''.join('  \\task %s\n' % Gi(p, 2.7) for p in GR4) + '\\end{tasks}'
    + items(T("La Laia ix de casa, va a casa d'una amiga i s'hi queda.", "Laia sale de casa, va a casa de una amiga y se queda allí."),
            T("En Pau baixa a comprar el pa i torna de seguida.", "Pau baja a comprar el pan y vuelve enseguida."),
            T("L'Àlex espera l'autobús a la parada, a prop de casa, i després el bus el porta a l'institut.", "Álex espera el autobús en la parada, cerca de casa, y después el autobús lo lleva al instituto."),
            T("La Sara va a la biblioteca, s'hi està una estona i torna a casa.", "Sara va a la biblioteca, está allí un rato y vuelve a casa.")),
    tasks(4, [T(r'gràfica \rest{2}', r'gráfica \rest{2}'), T(r'gràfica \rest{4}', r'gráfica \rest{4}'), T(r'gràfica \rest{3}', r'gráfica \rest{3}'), T(r'gràfica \rest{1}', r'gráfica \rest{1}')])))
g37 = poly(Plot(-6, 7, -3, 5, W=320), [(-5, 0), (-3, 2), (0, -1)])
poly(g37, [(0, -2), (3, 4), (6, -2)], dots=False).dot(0, -2, open=True).dot(3, 4).dot(6, -2)
ok(lin([(-3, 2), (0, -1)], -1) == 0 and lin([(0, -2), (3, 4)], 1) == 0 and lin([(3, 4), (6, -2)], 5) == 0)
X.append(E(2, T(r"Fes l'estudi complet de la funció de la gràfica: domini, recorregut, punts de tall, continuïtat, creixement i decreixement, i màxims i mínims.",
                r"Haz el estudio completo de la función de la gráfica: dominio, recorrido, puntos de corte, continuidad, crecimiento y decrecimiento, y máximos y mínimos.") + G(g37, 6.4),
    T(r"$D=\res{[-5,6]}$, $R=\res{[-2,4]}$. Talls: $OX$: $\res{(-5,0),\ (-1,0),\ (1,0),\ (5,0)}$; $OY$: $\res{(0,-1)}$. Discontínua en $x=0$ (\rest{salt finit}: per l'esquerra arriba a $-1=f(0)$ i per la dreta comença en $-2$). Creixent en $\res{(-5,-3)\cup(0,3)}$; decreixent en $\res{(-3,0)\cup(3,6)}$. Màxim relatiu $\res{(-3,2)}$ i màxim absolut $\res{(3,4)}$; mínim absolut $\res{(6,-2)}$.",
      r"$D=\res{[-5,6]}$, $R=\res{[-2,4]}$. Cortes: $OX$: $\res{(-5,0),\ (-1,0),\ (1,0),\ (5,0)}$; $OY$: $\res{(0,-1)}$. Discontinua en $x=0$ (\rest{salto finito}: por la izquierda llega a $-1=f(0)$ y por la derecha empieza en $-2$). Creciente en $\res{(-5,-3)\cup(0,3)}$; decreciente en $\res{(-3,0)\cup(3,6)}$. Máximo relativo $\res{(-3,2)}$ y máximo absoluto $\res{(3,4)}$; mínimo absoluto $\res{(6,-2)}$.")))
MV = [(0, 0), (15, 1.5), (25, 1.5), (40, 4.5), (70, 0)]
ok(1.5 / (15 / 60) == 6 and 3 / (15 / 60) == 12 and abs(4.5 / (30 / 60) - 9) < 1e-12)
X.append(E(3, T(r"El Marc ix de casa i camina 15 minuts a 6 km/h fins a casa d'un amic. S'hi està 10 minuts i després van junts amb bicicleta 3 km més, en 15 minuts, fins al poliesportiu. En acabar, torna directament a casa amb bicicleta en mitja hora. Dibuixa la gràfica de la distància a casa (en km) en funció del temps (en minuts) i calcula la velocitat de cada tram.",
                r"Marc sale de casa y camina 15 minutos a 6 km/h hasta casa de un amigo. Está allí 10 minutos y después van juntos en bicicleta 3 km más, en 15 minutos, hasta el polideportivo. Al acabar, vuelve directamente a casa en bicicleta en media hora. Dibuja la gráfica de la distancia a casa (en km) en función del tiempo (en minutos) y calcula la velocidad de cada tramo."),
    T(r"En 15 min a 6 km/h fa $6\cdot\frac14=1{,}5$ km. Punts: $(0,0)$, $(15;\ 1{,}5)$, $(25;\ 1{,}5)$, $(40;\ 4{,}5)$, $(70,0)$ (el temps del poliesportiu no compta). Velocitats: \rest{6 km/h}, \rest{0} (parat), $3:\frac14=$ \rest{12 km/h} i $4{,}5:\frac12=$ \rest{9 km/h}.",
      r"En 15 min a 6 km/h hace $6\cdot\frac14=1{,}5$ km. Puntos: $(0,0)$, $(15;\ 1{,}5)$, $(25;\ 1{,}5)$, $(40;\ 4{,}5)$, $(70,0)$ (el tiempo del polideportivo no cuenta). Velocidades: \rest{6 km/h}, \rest{0} (parado), $3:\frac14=$ \rest{12 km/h} y $4{,}5:\frac12=$ \rest{9 km/h}.")
    + G(poly(Plot(-4, 76, -.5, 5.5, sx=5, sy=.5, lx=10, ly=1, W=320), MV), 5)))

VC = [(0, 0), (2, 60), (6, 60), (7, 0), (8, 0), (10, 40)]
ok(max(v for _, v in VC) == 60 and lin(VC, 9) == 20)
X.append(E(1, T(r"La gràfica mostra la velocitat (en km/h) d'un cotxe durant els primers 10 minuts d'un trajecte per la ciutat.", r"La gráfica muestra la velocidad (en km/h) de un coche durante los primeros 10 minutos de un trayecto por la ciudad.") + G(poly(Plot(-.5, 10.6, -6, 70, sx=1, sy=10, lx=1, ly=10, W=300), VC), 4.6)
    + items(T("En quins intervals augmenta la velocitat? En quins va a velocitat constant? Quan frena?", "¿En qué intervalos aumenta la velocidad? ¿En cuáles va a velocidad constante? ¿Cuándo frena?"),
            T("Quina és la velocitat màxima? Està parat en algun moment? Què pot haver passat?", "¿Cuál es la velocidad máxima? ¿Está parado en algún momento? ¿Qué puede haber pasado?"),
            T("A quina velocitat va al minut 9?", "¿A qué velocidad va en el minuto 9?")),
    items(T(r"Accelera en $\res{(0,2)\cup(8,10)}$; velocitat constant en $\res{(2,6)}$; frena en $\res{(6,7)}$.", r"Acelera en $\res{(0,2)\cup(8,10)}$; velocidad constante en $\res{(2,6)}$; frena en $\res{(6,7)}$."),
          T(r"Màxima: \rest{60 km/h}, de 2 a 6 min. Està parat \rest{del minut 7 al 8}: potser un semàfor en roig.", r"Máxima: \rest{60 km/h}, de 2 a 6 min. Está parado \rest{del minuto 7 al 8}: quizá un semáforo en rojo."),
          r"$\res{20\text{ km/h}}$")))
hp = lambda t: 20 * t - 5 * t * t
ckroots('20*x-5*x**2', [0, 4]); ckroots('20*x-5*x**2-15', [1, 3]); ok(hp(2) == 20 and hp(1) == 15 and hp(3) == 15)
X.append(E(2, T(r"Llancem una pilota cap amunt. La seua altura (en metres) al cap de $t$ segons és $h(t)=20t-5t^2$.", r"Lanzamos una pelota hacia arriba. Su altura (en metros) a los $t$ segundos es $h(t)=20t-5t^2$.") + G(Plot(-.4, 4.6, -2, 23, sx=.5, sy=5, lx=1, ly=5, W=240).fn(hp, 0, 4), 3.2)
    + items(T("Quan torna a terra? Quin és el domini de la funció en aquest context?", "¿Cuándo vuelve al suelo? ¿Cuál es el dominio de la función en este contexto?"),
            T("Quina altura màxima arriba i quan?", "¿Qué altura máxima alcanza y cuándo?"),
            T("En quins moments està a 15 m d'altura?", "¿En qué momentos está a 15 m de altura?")),
    items(T(r"$20t-5t^2=0\Rightarrow 5t(4-t)=0\Rightarrow t=0,\ t=4$: torna a terra als \rest{4 s}; $D=\res{[0,4]}$.", r"$20t-5t^2=0\Rightarrow 5t(4-t)=0\Rightarrow t=0,\ t=4$: vuelve al suelo a los \rest{4 s}; $D=\res{[0,4]}$."),
          T(r"Màxim $\res{(2,20)}$: \rest{20 m als 2 s} (a la meitat del vol, per simetria).", r"Máximo $\res{(2,20)}$: \rest{20 m a los 2 s} (a la mitad del vuelo, por simetría)."),
          T(r"$20t-5t^2=15\Rightarrow t^2-4t+3=0\Rightarrow$ \rest{1 s} (pujant) i \rest{3 s} (baixant).", r"$20t-5t^2=15\Rightarrow t^2-4t+3=0\Rightarrow$ \rest{1 s} (subiendo) y \rest{3 s} (bajando)."))))

# =====================================================================
# 8. Construcció de funcions
X = sec(T('Construcció de funcions a partir d\'un enunciat', 'Construcción de funciones a partir de un enunciado'))
bici = lambda h: 5 + 2 * h
ok([bici(h) for h in (0, 1, 2, 3, 4)] == [5, 7, 9, 11, 13] and bici(7) == 19)
X.append(E(1, T(r"Un lloguer de bicicletes cobra 5 € fixos més 2 € per hora.", r"Un alquiler de bicicletas cobra 5 € fijos más 2 € por hora.")
    + items(T("Fes una taula amb el preu de 0, 1, 2, 3 i 4 hores i escriu la fórmula de la funció.", "Haz una tabla con el precio de 0, 1, 2, 3 y 4 horas y escribe la fórmula de la función."),
            T("Dibuixa'n la gràfica. Quin tipus de funció és?", "Dibuja su gráfica. ¿Qué tipo de función es?"),
            T("Quantes hores podem llogar una bicicleta amb 19 €?", "¿Cuántas horas podemos alquilar una bicicleta con 19 €?")),
    items(r"$\begin{array}{c|ccccc}x&0&1&2&3&4\\\hline y&5&7&9&11&13\end{array}$ \quad $\res{y=5+2x}$",
          T(r"Una \rest{funció lineal}: la gràfica és una recta que talla l'eix $OY$ en 5 i puja 2 per cada hora.", r"Una \rest{función lineal}: la gráfica es una recta que corta el eje $OY$ en 5 y sube 2 por cada hora.") + G(Plot(-.5, 8, -1, 22, sy=2, ly=4, W=220).fn(bici, 0, 8).dot(0, 5, 'b').dot(4, 13, 'b').dot(7, 19, 'b'), 3.2),
          r"$5+2x=19\Rightarrow\res{x=7}$ " + T("hores", "horas"))))
ok([360 // n for n in (1, 2, 3, 4, 5, 6)] == [360, 180, 120, 90, 72, 60] and all(360 % n == 0 for n in (1, 2, 3, 4, 5, 6)) and abs(360 / 7 - 51.43) < .005)
X.append(E(1, T(r"Un grup d'amics guanya un premi de 360 € i el reparteix a parts iguals.", r"Un grupo de amigos gana un premio de 360 € y lo reparte a partes iguales.")
    + items(T(r"Fes una taula amb els diners que rep cadascú si són 1, 2, 3, 4, 5 o 6 amics, i escriu la fórmula.", r"Haz una tabla con el dinero que recibe cada uno si son 1, 2, 3, 4, 5 o 6 amigos, y escribe la fórmula."),
            T("Quins valors pot prendre la variable independent? Unim els punts de la gràfica?", "¿Qué valores puede tomar la variable independiente? ¿Unimos los puntos de la gráfica?"),
            T("Si són 7 amics, quant rep cadascú?", "Si son 7 amigos, ¿cuánto recibe cada uno?")),
    items(r"$\begin{array}{c|cccccc}x&1&2&3&4&5&6\\\hline y&360&180&120&90&72&60\end{array}$ \quad $\res{y=\dfrac{360}{x}}$",
          T(r"Només \rest{nombres naturals} (1, 2, 3…): \rest{no s'uneixen}. És de proporcionalitat inversa.", r"Solo \rest{números naturales} (1, 2, 3…): \rest{no se unen}. Es de proporcionalidad inversa."),
          T(r"$360:7\approx\res{51{,}43\text{ €}}$ (i sobra algun cèntim).", r"$360:7\approx\res{51{,}43\text{ €}}$ (y sobra algún céntimo)."))))
ok(1000 + 25 * 200 == 6000 and 1000 + 25 * 60 == 2500 and (4000 - 1000) / 25 == 120)
X.append(E(2, T(r"Una piscina de 6\,000 L té ja 1\,000 L d'aigua. Obrim una aixeta que hi aboca 25 L per minut.", r"Una piscina de 6\,000 L tiene ya 1\,000 L de agua. Abrimos un grifo que vierte 25 L por minuto.")
    + items(T(r"Escriu la funció que dona els litres que hi ha en funció del temps $x$ (en minuts).", r"Escribe la función que da los litros que hay en función del tiempo $x$ (en minutos)."),
            T("Quant de temps tarda a omplir-se? Quins són el domini i el recorregut?", "¿Cuánto tiempo tarda en llenarse? ¿Cuáles son el dominio y el recorrido?"),
            T("Quants litres hi ha al cap d'una hora? Quan hi haurà 4\,000 L?", "¿Cuántos litros hay al cabo de una hora? ¿Cuándo habrá 4\,000 L?")),
    items(r"$\res{y=1\,000+25x}$",
          T(r"$1\,000+25x=6\,000\Rightarrow x=200$ min (\rest{3 h 20 min}). $D=\res{[0,200]}$, $R=\res{[1\,000;\ 6\,000]}$.", r"$1\,000+25x=6\,000\Rightarrow x=200$ min (\rest{3 h 20 min}). $D=\res{[0,200]}$, $R=\res{[1\,000;\ 6\,000]}$."),
          T(r"$y(60)=\res{2\,500\text{ L}}$. \ $1\,000+25x=4\,000\Rightarrow x=\res{120}$ min (2 hores).", r"$y(60)=\res{2\,500\text{ L}}$. \ $1\,000+25x=4\,000\Rightarrow x=\res{120}$ min (2 horas)."))))
ok(45 - .06 * 750 == 0 and abs(45 - .06 * 300 - 27) < 1e-9)
X.append(E(2, T(r"Un cotxe ix amb 45 L de gasolina al dipòsit i gasta 6 L cada 100 km.", r"Un coche sale con 45 L de gasolina en el depósito y gasta 6 L cada 100 km.")
    + items(T("Escriu la funció que dona els litres que queden en funció dels km recorreguts.", "Escribe la función que da los litros que quedan en función de los km recorridos."),
            T("Quants litres queden després de 300 km?", "¿Cuántos litros quedan después de 300 km?"),
            T("Quin és el domini de la funció? I el recorregut?", "¿Cuál es el dominio de la función? ¿Y el recorrido?")),
    items(T(r"Gasta $6:100=0{,}06$ L per km: $\res{y=45-0{,}06x}$.", r"Gasta $6:100=0{,}06$ L por km: $\res{y=45-0{,}06x}$."),
          r"$45-0{,}06\cdot300=\res{27\text{ L}}$",
          T(r"S'acaba quan $45-0{,}06x=0\Rightarrow x=750$ km: $D=\res{[0,750]}$, $R=\res{[0,45]}$.", r"Se acaba cuando $45-0{,}06x=0\Rightarrow x=750$ km: $D=\res{[0,750]}$, $R=\res{[0,45]}$."))))
ok([24 / b for b in (1, 2, 3, 4, 6, 8)] == [24, 12, 8, 6, 4, 3])
X.append(E(2, T(r"Un rectangle té 24 cm$^2$ d'àrea. Expressa l'altura $y$ en funció de la base $x$, fes una taula de valors i dibuixa la gràfica. Quin tipus de funció és? Quin és el domini?",
                r"Un rectángulo tiene 24 cm$^2$ de área. Expresa la altura $y$ en función de la base $x$, haz una tabla de valores y dibuja la gráfica. ¿Qué tipo de función es? ¿Cuál es el dominio?"),
    r"$x\cdot y=24\Rightarrow\res{y=\dfrac{24}{x}}$ \quad $\begin{array}{c|cccccc}x&1&2&3&4&6&8\\\hline y&24&12&8&6&4&3\end{array}$"
    + T(r" \ És de \rest{proporcionalitat inversa} (si la base es duplica, l'altura es redueix a la meitat). $D=\res{(0,+\infty)}$: la base ha de ser positiva.",
        r" \ Es de \rest{proporcionalidad inversa} (si la base se duplica, la altura se reduce a la mitad). $D=\res{(0,+\infty)}$: la base debe ser positiva.")
    + G(Plot(-1, 13, -1, 26, sx=1, sy=2, lx=2, ly=4, W=220).fn(lambda t: 24 / t if t > .9 else None, .9, 13).dot(2, 12, 'b').dot(4, 6, 'b').dot(8, 3, 'b'), 3.4)))
A60 = lambda t: t * (30 - t)
ok(A60(15) == 225 and A60(10) == 200 and A60(20) == 200 and all(A60(t / 10) <= 225 for t in range(1, 300)))
X.append(E(2, T(r"Amb 60 m de tanca volem fer un corral rectangular.", r"Con 60 m de valla queremos hacer un corral rectangular.")
    + items(T(r"Si un costat mesura $x$ m, quant mesura l'altre? Escriu la funció $A(x)$ que dona l'àrea del corral.", r"Si un lado mide $x$ m, ¿cuánto mide el otro? Escribe la función $A(x)$ que da el área del corral."),
            T(r"Quins valors pot prendre $x$? Calcula $A(5)$, $A(10)$, $A(15)$, $A(20)$ i $A(25)$.", r"¿Qué valores puede tomar $x$? Calcula $A(5)$, $A(10)$, $A(15)$, $A(20)$ y $A(25)$."),
            T("Quines dimensions té el corral d'àrea màxima?", "¿Qué dimensiones tiene el corral de área máxima?")),
    items(T(r"L'altre costat mesura $\frac{60-2x}{2}=30-x$: $\res{A(x)=x(30-x)=30x-x^2}$.", r"El otro lado mide $\frac{60-2x}{2}=30-x$: $\res{A(x)=x(30-x)=30x-x^2}$."),
          r"$D=\res{(0,30)}$. \ $A(5)=125$, $A(10)=200$, $A(15)=225$, $A(20)=200$, $A(25)=125$ (m$^2$).",
          T(r"La gràfica és una paràbola amb el màxim en $(15,225)$: un \rest{quadrat de 15 m de costat}, amb 225 m$^2$.", r"La gráfica es una parábola con el máximo en $(15,225)$: un \rest{cuadrado de 15 m de lado}, con 225 m$^2$."))))
ok(A60(5) == 125 and A60(25) == 125)
ckroots('10+x/20-x/10', [200])
ok(10 + .05 * 100 == 15 and .1 * 100 == 10 and 10 + .05 * 300 == 25 and .1 * 300 == 30)
X.append(E(2, T(r"Una companyia de telefonia ofereix dues tarifes: la A, amb una quota de 10 € al mes més 5 cèntims per minut, i la B, sense quota i a 10 cèntims per minut.",
                r"Una compañía de telefonía ofrece dos tarifas: la A, con una cuota de 10 € al mes más 5 céntimos por minuto, y la B, sin cuota y a 10 céntimos por minuto.")
    + items(T(r"Escriu la funció que dona el preu mensual de cada tarifa segons els minuts $x$ parlats.", r"Escribe la función que da el precio mensual de cada tarifa según los minutos $x$ hablados."),
            T("Quant es paga amb cada tarifa per 100 minuts? I per 300?", "¿Cuánto se paga con cada tarifa por 100 minutos? ¿Y por 300?"),
            T("Per a quants minuts costen igual? Quan convé cada tarifa?", "¿Para cuántos minutos cuestan lo mismo? ¿Cuándo conviene cada tarifa?")),
    items(r"$\res{y_A=10+0{,}05x}$, \ $\res{y_B=0{,}1x}$",
          T(r"100 min: A \rest{15 €}, B \rest{10 €}. \ 300 min: A \rest{25 €}, B \rest{30 €}.", r"100 min: A \rest{15 €}, B \rest{10 €}. \ 300 min: A \rest{25 €}, B \rest{30 €}."),
          T(r"$10+0{,}05x=0{,}1x\Rightarrow x=\res{200}$ minuts (20 € totes dues). Per a menys de 200 minuts convé la \rest{B}; per a més, la \rest{A}.", r"$10+0{,}05x=0{,}1x\Rightarrow x=\res{200}$ minutos (20 € las dos). Para menos de 200 minutos conviene la \rest{B}; para más, la \rest{A}.")
          + G(Plot(-20, 420, -3, 45, sx=50, sy=5, lx=100, ly=10, W=260).fn(lambda t: 10 + .05 * t, 0, 420, 'b').fn(lambda t: .1 * t, 0, 420, 'o').dot(200, 20, 'v').text(400, 26, 'A', 'b').text(330, 37, 'B', 'o'), 4))))
ok(900 + .05 * 6000 == 1200 and (1500 - 900) / .05 == 12000)
X.append(E(3, T(r"Un comercial cobra un sou fix de 900 € al mes més un 5\,\% de les vendes que fa. Escriu la funció que dona el sou segons les vendes. Quant cobra un mes que ven per valor de 6\,000 €? Quant ha de vendre per a cobrar 1\,500 €?",
                r"Un comercial cobra un sueldo fijo de 900 € al mes más un 5\,\% de las ventas que hace. Escribe la función que da el sueldo según las ventas. ¿Cuánto cobra un mes que vende por valor de 6\,000 €? ¿Cuánto tiene que vender para cobrar 1\,500 €?"),
    T(r"El 5\,\% de $x$ és $0{,}05x$: $\res{y=900+0{,}05x}$. \ $y(6\,000)=900+300=\res{1\,200\text{ €}}$. \ $900+0{,}05x=1\,500\Rightarrow x=\dfrac{600}{0{,}05}=\res{12\,000\text{ €}}$.",
      r"El 5\,\% de $x$ es $0{,}05x$: $\res{y=900+0{,}05x}$. \ $y(6\,000)=900+300=\res{1\,200\text{ €}}$. \ $900+0{,}05x=1\,500\Rightarrow x=\dfrac{600}{0{,}05}=\res{12\,000\text{ €}}$.")))

ok([5 * n + 3 for n in (1, 2, 3, 4, 10)] == [8, 13, 18, 23, 53] and (98 - 3) / 5 == 19)
X.append(E(2, T(r"La taula dona el preu (en €) d'unes entrades de cine comprades per Internet, segons el nombre d'entrades.", r"La tabla da el precio (en €) de unas entradas de cine compradas por Internet, según el número de entradas.")
    + r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}\hline " + T("Entrades", "Entradas") + r" & 1 & 2 & 3 & 4\\\hline " + T("Preu (€)", "Precio (€)") + r" & 8 & 13 & 18 & 23\\\hline\end{tabular}\end{center}"
    + items(T("Quant augmenta el preu per cada entrada? Hi ha alguna despesa fixa (de gestió)?", "¿Cuánto aumenta el precio por cada entrada? ¿Hay algún gasto fijo (de gestión)?"),
            T("Escriu la fórmula de la funció. Quant costen 10 entrades?", "Escribe la fórmula de la función. ¿Cuánto cuestan 10 entradas?"),
            T("Quantes entrades hem comprat si paguem 98 €? Hem d'unir els punts de la gràfica?", "¿Cuántas entradas hemos comprado si pagamos 98 €? ¿Debemos unir los puntos de la gráfica?")),
    items(T(r"Cada entrada val \rest{5 €}; la despesa fixa és $8-5=$ \rest{3 €}.", r"Cada entrada vale \rest{5 €}; el gasto fijo es $8-5=$ \rest{3 €}."),
          r"$\res{y=5x+3}$; \ $y(10)=\res{53\text{ €}}$",
          T(r"$5x+3=98\Rightarrow\res{x=19}$ entrades. \rest{No}: el nombre d'entrades és un nombre natural.", r"$5x+3=98\Rightarrow\res{x=19}$ entradas. \rest{No}: el número de entradas es un número natural."))))

PRE = r'''\usetikzlibrary{calc}
\usepackage{enumitem}
\definecolor{violet}{HTML}{7C3AED}
\definecolor{orange}{HTML}{EA8A1F}
'''
TIT = T('Funcions. Característiques', 'Funciones. Características')
build(HERE, 6, TIT, S,
      T("funcions, variables, imatge, antiimatge, domini, recorregut, punts de tall, continuïtat, discontinuïtats, creixement, màxims i mínims, periodicitat, interpretació de gràfics, construcció de funcions",
        "funciones, variables, imagen, antiimagen, dominio, recorrido, puntos de corte, continuidad, discontinuidades, crecimiento, máximos y mínimos, periodicidad, interpretación de gráficos, construcción de funciones"),
      T(r"Resol-los al quadern mostrant tots els passos. Escriu els intervals com als apunts: $(a,b)$ obert i $[a,b]$ tancat. Les seccions segueixen l'ordre dels apunts de la unitat (6.1--6.8).",
        r"Resuélvelos en el cuaderno mostrando todos los pasos. Escribe los intervalos como en los apuntes: $(a,b)$ abierto y $[a,b]$ cerrado. Las secciones siguen el orden de los apuntes de la unidad (6.1--6.8)."),
      T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. En els exercicis de «dibuixa una funció…» hi ha moltes respostes correctes: comprova que la teua complisca totes les condicions. Pots comprovar dominis i talls amb les eines interactives dels apunts de la unitat.",
        r"Intenta resolver cada ejercicio antes de mirar su solución. En los ejercicios de «dibuja una función…» hay muchas respuestas correctas: comprueba que la tuya cumpla todas las condiciones. Puedes comprobar dominios y cortes con las herramientas interactivas de los apuntes de la unidad."),
      PRE, lang='es' if ES else 'va', curs='4eso-a')
