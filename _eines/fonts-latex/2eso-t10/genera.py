# Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (2n ESO, Unitat 10: Funcions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 8 seccions segueixen els apartats dels apunts (10.1-10.8).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Cada resultat es comprova amb CHK / ck (fraccions exactes). El pla cartesià en TikZ, tp(), és el de ../1eso-t9/genera.py.
# Ús: python3 genera.py && pdflatex t10-fitxa-exercicis.tex (dues vegades) && pdflatex t10-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def center(t): return r'\par\smallskip\begin{center}' + t + r'\end{center}'
def side(*figs): return r'\par\smallskip\begin{center}' + r'\hspace{0.7cm}'.join(figs) + r'\end{center}'

# ---------- comprovacions ----------
NCHK = [0]
def CHK(cond, *info):
    NCHK[0] += 1
    assert cond, info
def fr(v): return v if isinstance(v, Fr) else Fr(str(v).replace('{,}', '.').replace(',', '.'))
def ck(v, w):
    """v: valor calculat; w: el que escrivim (nombre o text «2,5»)"""
    CHK(fr(v) == fr(w), v, w)
    return v
def lin(m, n=0):
    m, n = fr(m), fr(n)
    return lambda x: m * fr(x) + n
def slope(A, B): return (fr(B[1]) - fr(A[1])) / (fr(B[0]) - fr(A[0]))

# ---------- nombres i taules ----------
def tn(v):
    v = fr(v)
    if v.denominator == 1: return str(v.numerator)
    t = ('%.6f' % float(v)).rstrip('0').rstrip('.')
    CHK(fr(t) == v, v)
    return t.replace('.', '{,}')
def pt(x, y):
    a, b = tn(x), tn(y)
    return '(%s;\\ %s)' % (a, b) if '{,}' in a + b else '(%s,\\ %s)' % (a, b)
def lab(t):
    return t[1:-1] if t.startswith('$') and t.endswith('$') else t if t in ('x', 'y') else r'\text{%s}' % t
def cell(a): return a if isinstance(a, str) else tn(a)
def tv(xs, ys, xl='x', yl='y'):
    xl, yl = lab(xl), lab(yl)
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('c' * len(xs), xl, '&'.join(cell(a) for a in xs), yl, '&'.join(cell(a) for a in ys)))
def tvb(xs, xl='x', yl='y'):
    xl, yl = lab(xl), lab(yl)
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('C{0.75cm}' * len(xs), xl, '&'.join(cell(a) for a in xs), yl, '&'.join([r'\phantom{00}'] * len(xs))))
def eq(m, n=0, v='x'):
    m, n = fr(m), fr(n)
    if m == 0: return 'y=' + tn(n)
    s = v if m == 1 else '-' + v if m == -1 else tn(m) + v
    if n: s += ('+' if n > 0 else '-') + tn(abs(n))
    return 'y=' + s

# ---------- pla cartesià (TikZ) ----------
COL = {'p0': 'accent', 'p1': 'teal', 'p2': 'navy'}
def tp(win, pts=(), polys=(), fns=(), curves=(), proj=(), labs=(), u=0.42, uy=None, xs=1, ys=1, gx=None, gy=None, xl='x', yl='y', zero=True):
    """win = (x0, x1, y0, y1); pts: (x, y, etiqueta, color[, posició]); fns: (m, n, color[, a, b]); curves: (punts, color);
    proj: (x, y) línies de projecció; labs: (x, y, text, posició)"""
    x0, x1, y0, y1 = [float(v) for v in win]
    uy = uy or u; gx = gx or xs; gy = gy or ys
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center),line cap=round,line join=round]' % (u, uy)]
    k = math.ceil(x0 / gx - 1e-9)
    while k * gx <= x1 + 1e-9: o.append(r'\draw[muted!30,line width=0.3pt] (%g,%g)--(%g,%g);' % (k * gx, y0, k * gx, y1)); k += 1
    k = math.ceil(y0 / gy - 1e-9)
    while k * gy <= y1 + 1e-9: o.append(r'\draw[muted!30,line width=0.3pt] (%g,%g)--(%g,%g);' % (x0, k * gy, x1, k * gy)); k += 1
    ax = min(max(0, y0), y1); ay = min(max(0, x0), x1)
    o.append(r'\draw[-latex,muted,line width=0.6pt] (%g,%g)--(%g,%g) node[right,font=\scriptsize,text=navy]{%s};' % (x0, ax, x1 + 0.3 * gx, ax, xl))
    o.append(r'\draw[-latex,muted,line width=0.6pt] (%g,%g)--(%g,%g) node[above,font=\scriptsize,text=navy]{%s};' % (ay, y0, ay, y1 + 0.3 * gy, yl))
    k = math.ceil(x0 / xs - 1e-9)
    while k * xs < x1 - 1e-9:
        v = k * xs
        if abs(v) > 1e-9 and v > x0 + 1e-9: o.append(r'\node[font=\tiny,text=muted,below,inner sep=1.5pt] at (%g,%g) {$%s$};' % (v, ax, tn(Fr(v).limit_denominator(100))))
        k += 1
    k = math.ceil(y0 / ys - 1e-9)
    while k * ys < y1 - 1e-9:
        v = k * ys
        if abs(v) > 1e-9 and v > y0 + 1e-9: o.append(r'\node[font=\tiny,text=muted,left,inner sep=1.5pt] at (%g,%g) {$%s$};' % (ay, v, tn(Fr(v).limit_denominator(100))))
        k += 1
    if zero: o.append(r'\node[font=\tiny,text=muted,below left,inner sep=1.5pt] at (%g,%g) {$0$};' % (ay, ax))
    for V, c in polys:
        o.append(r'\draw[%s,thick,fill=%s!15] %s--cycle;' % (c, c, '--'.join('(%g,%g)' % (float(p[0]), float(p[1])) for p in V)))
    for f in fns:
        m, n, c = float(fr(f[0])), float(fr(f[1])), f[2]
        lo = float(f[3]) if len(f) > 3 and f[3] is not None else x0
        hi = float(f[4]) if len(f) > 4 and f[4] is not None else x1
        if m != 0:
            xa, xb = (y0 - n) / m, (y1 - n) / m
            lo, hi = max(lo, min(xa, xb)), min(hi, max(xa, xb))
        if lo < hi: o.append(r'\draw[%s,line width=1.1pt] (%.3f,%.3f)--(%.3f,%.3f);' % (c, lo, m * lo + n, hi, m * hi + n))
    for P, c in curves:
        o.append(r'\draw[%s,line width=1.1pt] %s;' % (c, '--'.join('(%.3f,%.3f)' % (float(p[0]), float(p[1])) for p in P)))
    for px, py in proj:
        o.append(r'\draw[accent,dashed,thin] (%g,%g)--(%g,%g)--(%g,%g);' % (float(px), ax, float(px), float(py), ay, float(py)))
    for p in pts:
        px, py, lb, c = (tuple(p) + (None, 'p2'))[:4]
        pos = p[4] if len(p) > 4 else 'above right'
        o.append(r'\fill[%s] (%g,%g) circle (2.2pt)%s;' % (COL.get(c, c), float(px), float(py), (r' node[%s,font=\scriptsize,inner sep=1.5pt]{%s}' % (pos, lb)) if lb else ''))
    for px, py, t, pos in labs:
        o.append(r'\node[font=\scriptsize,%s] at (%g,%g) {%s};' % (pos, float(px), float(py), t))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def samp(f, a, b, n=48): return [(a + (b - a) * k / n, f(a + (b - a) * k / n)) for k in range(n + 1)]
def cap(t, f): return r'\begin{tabular}{c}' + f + r'\\[1pt]\small ' + t + r'\end{tabular}'

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]
W5 = (-5, 5, -5, 5)
SI, NO = T('sí', 'sí'), T('no', 'no')

# =====================================================================
# 1. Concepte de funció
# =====================================================================
TA, TB, TC = ([1, 2, 3, 4], [3, 6, 9, 12]), ([1, 1, 2, 3], [2, 5, 4, 7]), ([-2, -1, 1, 2], [4, 1, 1, 4])
def isfn(Tb): return all(not (a == c and b != d) for a, b in zip(*Tb) for c, d in zip(*Tb))
CHK(isfn(TA) and not isfn(TB) and isfn(TC))
CIR = [(2.2 * math.cos(math.radians(a)), 2.2 * math.sin(math.radians(a))) for a in range(0, 361, 10)]
GA = tp((-4, 4, -3, 3), curves=[([(-3.5, -2), (-1.5, 1.5), (0.5, 0), (3.5, 2.5)], 'accent')], u=0.3, xs=2, ys=2, gx=1, gy=1)
GB = tp((-4, 4, -3, 3), curves=[(CIR, 'accent')], u=0.3, xs=2, ys=2, gx=1, gy=1)
GC = tp((-4, 4, -3, 3), curves=[([(t * t - 2.5, t) for t in [k / 10 for k in range(-25, 26)]], 'accent')], u=0.3, xs=2, ys=2, gx=1, gy=1)
GD = tp((-4, 4, -3, 3), fns=[(0, -1.5, 'accent')], u=0.3, xs=2, ys=2, gx=1, gy=1)
IMP = [ck(20 * k, v) for k, v in zip(range(5), [0, 20, 40, 60, 80])]
FIMP = tp((0, 4.6, 0, 92), fns=[(20, 0, 'accent', 0, 4.4)], pts=[(k, 20 * k, None, 'p2') for k in range(5)], u=0.8, uy=0.04, ys=20, gy=10, xl='min', yl=T('pàg.', 'pág.'))
RB = [1, 2, 3, 4, 6, 8, 12, 24]
RH = [ck(Fr(24, b), v) for b, v in zip(RB, [24, 12, 8, 6, 4, 3, 2, 1])]
S_.append((T("Concepte de funció", "Concepto de función"), [
 (1, T(r"En cada situació, digues quina és la variable independent ($x$) i quina la dependent ($y$):", r"En cada situación, di cuál es la variable independiente ($x$) y cuál la dependiente ($y$):")
     + tasks(2, [T(r"El preu d'una pizza i el nombre d'ingredients.", r"El precio de una pizza y sus ingredientes."), T(r"L'àrea d'un cercle i el seu radi.", r"El área de un círculo y su radio."),
                 T(r"Els minuts parlats per telèfon i el preu.", r"Los minutos hablados por teléfono y el precio."), T(r"La temperatura d'un forn i el temps que fa que està encés.", r"La temperatura de un horno y el tiempo que lleva encendido.")])
     + recorda(T(r"La variable \textbf{independent} $x$ és la que triem o la que passa sola; la \textbf{dependent} $y$ és la que depén de l'altra. Una relació és una \textbf{funció} si a cada valor de $x$ li correspon \textbf{un únic} valor de $y$.",
                 r"La variable \textbf{independiente} $x$ es la que elegimos o la que pasa sola; la \textbf{dependiente} $y$ es la que depende de la otra. Una relación es una \textbf{función} si a cada valor de $x$ le corresponde \textbf{un único} valor de $y$.")),
     tasks(2, [T(r"$x$: ingredients; $y$: \rest{preu}.", r"$x$: ingredientes; $y$: \rest{precio}."), T(r"$x$: radi; $y$: \rest{àrea}.", r"$x$: radio; $y$: \rest{área}."),
               T(r"$x$: minuts; $y$: \rest{el que paguem}.", r"$x$: minutos; $y$: \rest{lo que pagamos}."), T(r"$x$: temps; $y$: \rest{temperatura}.", r"$x$: tiempo; $y$: \rest{temperatura}.")])),
 (1, T(r"Digues si aquestes relacions són funcions i explica per què:", r"Di si estas relaciones son funciones y explica por qué:")
     + tasks(1, [T(r"A cada alumne de la classe, el seu dia de naixement.", r"A cada alumno de la clase, su día de nacimiento."),
                 T(r"A cada nombre natural, els seus múltiples.", r"A cada número natural, sus múltiplos."),
                 T(r"A cada quantitat de litres de gasolina, el preu que paguem.", r"A cada cantidad de litros de gasolina, el precio que pagamos."),
                 T(r"A cada edat, les persones de la classe que la tenen.", r"A cada edad, las personas de la clase que la tienen.")]),
     tasks(1, [T(r"\rest{Sí}: cada alumne té un sol dia de naixement.", r"\rest{Sí}: cada alumno tiene un solo día de nacimiento."),
               T(r"\rest{No}: cada nombre té infinits múltiples.", r"\rest{No}: cada número tiene infinitos múltiplos."),
               T(r"\rest{Sí}: cada quantitat de litres té un preu.", r"\rest{Sí}: cada cantidad de litros tiene un precio."),
               T(r"\rest{No}: una edat pot correspondre a moltes persones.", r"\rest{No}: una edad puede corresponder a muchas personas.")])),
 (1, T(r"Quines d'aquestes taules són d'una funció? Raona-ho.", r"¿Cuáles de estas tablas son de una función? Razónalo.")
     + side(tv(*TA), tv(*TB), tv(*TC)),
     T(r"La primera i la tercera \rest{sí}: cap $x$ es repeteix amb dues $y$ (que dues $x$ tinguen la mateixa $y$ no és cap problema). La segona \rest{no}: per a $x=1$ hi ha $y=2$ i $y=5$.",
       r"La primera y la tercera \rest{sí}: ninguna $x$ se repite con dos $y$ (que dos $x$ tengan la misma $y$ no es ningún problema). La segunda \rest{no}: para $x=1$ hay $y=2$ e $y=5$.")),
 (2, T(r"Quins d'aquests gràfics són d'una funció? Fes la prova de la recta vertical.", r"¿Cuáles de estas gráficas son de una función? Haz la prueba de la recta vertical.")
     + side(cap('A', GA), cap('B', GB), cap('C', GC), cap('D', GD))
     + recorda(T(r"Si alguna recta vertical talla el gràfic en dos punts o més, \textbf{no} és una funció.", r"Si alguna recta vertical corta la gráfica en dos puntos o más, \textbf{no} es una función.")),
     T(r"A \rest{sí} i D \rest{sí} (cada recta vertical els talla una vegada); B \rest{no} i C \rest{no}: hi ha rectes verticals que els tallen dues vegades.",
       r"A \rest{sí} y D \rest{sí} (cada recta vertical las corta una vez); B \rest{no} y C \rest{no}: hay rectas verticales que las cortan dos veces.")),
 (2, T(r"Una impressora imprimeix 20 pàgines cada minut. Dona aquesta funció amb una taula (de 0 a 4 minuts), amb una fórmula i amb un gràfic. Unim els punts?",
       r"Una impresora imprime 20 páginas cada minuto. Da esta función con una tabla (de 0 a 4 minutos), con una fórmula y con una gráfica. ¿Unimos los puntos?"),
     tv(range(5), IMP, 'min', T('pàg.', 'pág.')) + r'\qquad $\res{y=20x}$' + center(FIMP)
     + T(r"Els unim: també té sentit mig minut (10 pàgines).", r"Los unimos: también tiene sentido medio minuto (10 páginas).")),
 (3, T(r"Els rectangles d'àrea 24\,cm$^2$ poden tindre bases diferents. a) Completa la taula de l'altura $h$ segons la base $b$. b) És una funció? c) Quina fórmula té? d) Quan la base es duplica, què passa amb l'altura?",
       r"Los rectángulos de área 24\,cm$^2$ pueden tener bases distintas. a) Completa la tabla de la altura $h$ según la base $b$. b) ¿Es una función? c) ¿Qué fórmula tiene? d) Cuando la base se duplica, ¿qué pasa con la altura?")
     + center(tvb(RB, 'b', 'h')),
     center(tv(RB, [r'\res{%s}' % tn(v) for v in RH], 'b', 'h'))
     + T(r"b) \rest{Sí}: per a cada base hi ha una sola altura. c) $b\cdot h=24\Rightarrow \res{h=\frac{24}{b}}$. d) L'altura es fa la \rest{meitat}: és una proporcionalitat inversa i el gràfic no és una recta.",
         r"b) \rest{Sí}: para cada base hay una sola altura. c) $b\cdot h=24\Rightarrow \res{h=\frac{24}{b}}$. d) La altura se hace la \rest{mitad}: es una proporcionalidad inversa y la gráfica no es una recta.")),
]))
CHK(Fr(24, 2) == 2 * Fr(24, 4))

# =====================================================================
# 2. Funcions donades per taules de valors
# =====================================================================
PK = ['0,5', 1, 2, 3, 4]
PV = [ck(fr('1.2') * fr(k), v) for k, v in zip(PK, ['0.6', '1.2', '2.4', '3.6', '4.8'])]
HR = [0, 3, 6, 9, 12, 15, 18, 21, 24]
TM = [8, 6, 7, 13, 18, 20, 16, 11, 9]
FTM = tp((0, 25, 0, 22), curves=[(list(zip(HR, TM)), 'accent')], pts=[(h, t, None, 'p2') for h, t in zip(HR, TM)], u=0.3, uy=0.2, xs=3, ys=4, gy=2, xl='h', yl='°C')
T1 = ([0, 1, 2, 3, 4], [ck(lin(3, 1)(k), v) for k, v in zip(range(5), [1, 4, 7, 10, 13])])
T2 = ([0, 1, 2, 3, 4], [ck(lin(-3, 20)(k), v) for k, v in zip(range(5), [20, 17, 14, 11, 8])])
f25 = lin(2, -5)
PIS = ([0, 2, 4, 6, 8], [ck(lin(-10, 90)(k), v) for k, v in zip([0, 2, 4, 6, 8], [90, 70, 50, 30, 10])])
QL = [1, 2, 3, 4, 5]
QA = [ck(Fr(l) ** 2, v) for l, v in zip(QL, [1, 4, 9, 16, 25])]
FQA = tp((0, 5.6, 0, 27), curves=[([(k / 10, (k / 10) ** 2) for k in range(0, 53)], 'accent')], pts=[(l, l * l, None, 'p2') for l in QL], u=0.6, uy=0.12, ys=5, gy=5, xl='$l$', yl='$A$')
MI = [1, 2, 3, 4]
MP = [ck(lin(2, 1)(k), v) for k, v in zip(MI, [3, 5, 7, 9])]
TRI = r'\begin{tikzpicture}[x=0.5cm,y=0.5cm,line width=1pt,accent]' + ''.join(r'\draw (%g,0)--(%g,0.87)--(%g,0);' % (i, i + 0.5, i + 1) + (r'\draw (%g,0.87)--(%g,0.87);' % (i + 0.5, i + 1.5) if i < 3 else '') for i in range(4)) + r'\end{tikzpicture}'
S_.append((T("Funcions donades per taules de valors", "Funciones dadas por tablas de valores"), [
 (1, T(r"Les mandarines valen 1,20\,€ el quilo. Completa la taula del preu ($y$) segons el pes ($x$) i digues si en el gràfic unim els punts.", r"Las mandarinas valen 1,20\,€ el kilo. Completa la tabla del precio ($y$) según el peso ($x$) y di si en la gráfica unimos los puntos.")
     + center(tvb(PK, 'kg', '€'))
     + recorda(T(r"Cada columna de la taula és un punt $(x,\ y)$ del gràfic. Unim els punts si també tenen sentit els valors intermedis; si només hi ha valors solts (persones, entrades…), no els unim.",
                 r"Cada columna de la tabla es un punto $(x,\ y)$ de la gráfica. Unimos los puntos si también tienen sentido los valores intermedios; si solo hay valores sueltos (personas, entradas…), no los unimos.")),
     center(tv(PK, [r'\res{%s}' % tn(v) for v in PV], 'kg', '€')) + T(r"Sí que els unim: podem comprar qualsevol pes.", r"Sí los unimos: podemos comprar cualquier peso.")),
 (1, T(r"Digues si en el gràfic d'aquestes funcions s'han d'unir els punts:", r"Di si en la gráfica de estas funciones se tienen que unir los puntos:")
     + tasks(1, [T(r"Nombre de germans d'un alumne → nombre de regals que fa per Nadal.", r"Número de hermanos de un alumno → número de regalos que hace en Navidad."),
                 T(r"Temps que fa que corre un atleta → distància recorreguda.", r"Tiempo que lleva corriendo un atleta → distancia recorrida."),
                 T(r"Nombre de llibres comprats → preu total.", r"Número de libros comprados → precio total."),
                 T(r"Litres d'aigua d'un dipòsit → altura de l'aigua.", r"Litros de agua de un depósito → altura del agua.")]),
     tasks(1, [T(r"\rest{No}: valors solts.", r"\rest{No}: valores sueltos."), T(r"\rest{Sí}: el temps passa de manera contínua.", r"\rest{Sí}: el tiempo pasa de forma continua."),
               T(r"\rest{No}: no es compra mig llibre.", r"\rest{No}: no se compra medio libro."), T(r"\rest{Sí}: hi pot haver qualsevol quantitat d'aigua.", r"\rest{Sí}: puede haber cualquier cantidad de agua.")])),
 (1, T(r"La taula dona la temperatura d'un dia cada 3 hores. Representa-la i respon: a) A quina hora va fer més calor? I més fred? b) Entre quines hores va pujar la temperatura? c) Quina temperatura aproximada feia a les 10 h?",
       r"La tabla da la temperatura de un día cada 3 horas. Represéntala y responde: a) ¿A qué hora hizo más calor? ¿Y más frío? b) ¿Entre qué horas subió la temperatura? c) ¿Qué temperatura aproximada hacía a las 10 h?")
     + center(tv(HR, TM, 'h', '°C')),
     center(FTM) + T(r"a) Més calor a les \rest{15 h} (20\,°C); més fred a les \rest{3 h} (6\,°C). b) Va pujar \rest{de les 3 h a les 15 h}. c) Entre 13\,°C (9 h) i 18\,°C (12 h): unes $\res{15\text{ °C}}$.",
                     r"a) Más calor a las \rest{15 h} (20\,°C); más frío a las \rest{3 h} (6\,°C). b) Subió \rest{de las 3 h a las 15 h}. c) Entre 13\,°C (9 h) y 18\,°C (12 h): unos $\res{15\text{ °C}}$.")),
 (2, T(r"Troba la fórmula de la funció que dona cada taula:", r"Halla la fórmula de la función que da cada tabla:") + side(tv(*T1), tv(*T2))
     + recorda(T(r"Si $x$ va d'1 en 1 i $y$ augmenta (o disminueix) sempre igual, la fórmula és $y=mx+n$: $m$ és el que canvia $y$ cada vegada i $n$ és el valor de $y$ per a $x=0$.",
                 r"Si $x$ va de 1 en 1 e $y$ aumenta (o disminuye) siempre igual, la fórmula es $y=mx+n$: $m$ es lo que cambia $y$ cada vez y $n$ es el valor de $y$ para $x=0$.")),
     T(r"a) Augmenta 3 i comença en 1: $\res{y=3x+1}$.\newline b) Disminueix 3 i comença en 20: $\res{y=-3x+20}$.", r"a) Aumenta 3 y empieza en 1: $\res{y=3x+1}$.\newline b) Disminuye 3 y empieza en 20: $\res{y=-3x+20}$.")),
 (2, T(r"Completa la taula de la funció $y=2x-5$:", r"Completa la tabla de la función $y=2x-5$:") + center(tv([-1, 0, 2, r'\phantom{00}', r'\phantom{00}', 10], [r'\phantom{00}', r'\phantom{00}', r'\phantom{00}', 3, 0, r'\phantom{00}'])),
     center(tv([-1, 0, 2, r'\res{4}', r'\res{2{,}5}', 10], [r'\res{-7}', r'\res{-5}', r'\res{-1}', 3, 0, r'\res{15}']))
     + T(r"Per a les $x$ que falten resolem una equació: $2x-5=3\Rightarrow x=4$; \ $2x-5=0\Rightarrow x=2{,}5$.", r"Para las $x$ que faltan resolvemos una ecuación: $2x-5=3\Rightarrow x=4$; \ $2x-5=0\Rightarrow x=2{,}5$.")),
 (2, T(r"Una piscina es buida. La taula dona l'altura de l'aigua (cm) segons les hores. a) Quanta aigua baixa cada hora? b) Quina altura hi havia a les 5 h? c) Quan quedaran 20\,cm? d) Escriu la fórmula.",
       r"Una piscina se vacía. La tabla da la altura del agua (cm) según las horas. a) ¿Cuánta agua baja cada hora? b) ¿Qué altura había a las 5 h? c) ¿Cuándo quedarán 20\,cm? d) Escribe la fórmula.")
     + center(tv(*PIS, 'h', 'cm')),
     T(r"a) Cada 2 hores baixa 20\,cm: \rest{10\,cm cada hora}. b) $50-10=\res{40\text{ cm}}$. c) $90-10x=20\Rightarrow x=\res{7\text{ h}}$. d) $\res{y=-10x+90}$.",
       r"a) Cada 2 horas baja 20\,cm: \rest{10\,cm cada hora}. b) $50-10=\res{40\text{ cm}}$. c) $90-10x=20\Rightarrow x=\res{7\text{ h}}$. d) $\res{y=-10x+90}$.")),
 (3, T(r"Fes la taula de l'àrea $A$ d'un quadrat segons el costat $l$ per a $l=1,\ 2,\ 3,\ 4,\ 5$ i representa-la. És una recta? Quina àrea té un quadrat de 2,5\,cm de costat?",
       r"Haz la tabla del área $A$ de un cuadrado según el lado $l$ para $l=1,\ 2,\ 3,\ 4,\ 5$ y represéntala. ¿Es una recta? ¿Qué área tiene un cuadrado de 2,5\,cm de lado?"),
     tv(QL, QA, '$l$', '$A$') + center(FQA)
     + T(r"Les diferències són 3, 5, 7, 9: no són iguals, així que \rest{no és una recta} ($A=l^2$). Per a $l=2{,}5$: $A=2{,}5^2=\res{6{,}25\text{ cm}^2}$.",
         r"Las diferencias son 3, 5, 7, 9: no son iguales, así que \rest{no es una recta} ($A=l^2$). Para $l=2{,}5$: $A=2{,}5^2=\res{6{,}25\text{ cm}^2}$.")),
 (3, T(r"Amb escuradents fem una filera de triangles:", r"Con palillos hacemos una fila de triángulos:") + center(TRI)
     + T(r"a) Completa la taula del nombre d'escuradents $y$ segons el nombre de triangles $x$. b) Troba'n la fórmula. c) Quants escuradents calen per a 20 triangles? d) Quants triangles fem amb 61 escuradents?",
         r"a) Completa la tabla del número de palillos $y$ según el número de triángulos $x$. b) Halla su fórmula. c) ¿Cuántos palillos hacen falta para 20 triángulos? d) ¿Cuántos triángulos hacemos con 61 palillos?")
     + center(tvb(MI, T('triangles', 'triángulos'), T('escuradents', 'palillos'))),
     center(tv(MI, [r'\res{%d}' % v for v in MP], T('triangles', 'triángulos'), T('escuradents', 'palillos')))
     + T(r"b) Cada triangle nou n'afig 2 i per a $x=0$ quedaria 1: $\res{y=2x+1}$. c) $2\cdot20+1=\res{41}$. d) $2x+1=61\Rightarrow x=\res{30}$ triangles.",
         r"b) Cada triángulo nuevo añade 2 y para $x=0$ quedaría 1: $\res{y=2x+1}$. c) $2\cdot20+1=\res{41}$. d) $2x+1=61\Rightarrow x=\res{30}$ triángulos.")),
]))
CHK(f25(4) == 3 and f25(Fr(5, 2)) == 0 and [f25(k) for k in (-1, 0, 2, 10)] == [-7, -5, -1, 15])
CHK(lin(-10, 90)(5) == 40 and lin(-10, 90)(7) == 20 and fr('2.5') ** 2 == fr('6.25') and lin(2, 1)(20) == 41 and lin(2, 1)(30) == 61)
CHK(TM.index(max(TM)) == 5 and TM.index(min(TM)) == 1 and Fr(13 + 18, 2) > 15 > 13)

# =====================================================================
# 3. Funcions donades per la seua equació
# =====================================================================
f43 = lin(4, -3)
X31 = [-2, 0, Fr(1, 2), 3]; Y31 = [ck(f43(k), v) for k, v in zip(X31, [-11, -3, -1, 9])]
g2 = lin(-1, 2); X32 = [-2, -1, 0, 1, 2, 3, 4]; Y32 = [ck(g2(k), v) for k, v in zip(X32, [4, 3, 2, 1, 0, -1, -2])]
F32 = tp((-3, 5, -3, 5), fns=[(-1, 2, 'accent')], pts=[(a, b, None, 'p2') for a, b in zip(X32, Y32)], u=0.38)
q2 = lambda x: Fr(x) ** 2 - 2; X33 = [-3, -2, -1, 0, 1, 2, 3]; Y33 = [ck(q2(k), v) for k, v in zip(X33, [7, 2, -1, -2, -1, 2, 7])]
F33 = tp((-3.6, 3.6, -3, 8), curves=[(samp(lambda x: x * x - 2, -3.15, 3.15), 'accent')], pts=[(a, b, None, 'p2') for a, b in zip(X33, Y33)], u=0.42, uy=0.3)
h31 = lin(3, -1)
P34 = [((2, 5), True), ((-1, -4), True), ((0, 1), False), ((Fr(1, 3), 0), True)]
for (a, b), ok in P34: CHK((h31(a) == b) == ok)
X35 = [1, 2, 3, 4, 6, 12]; Y35 = [ck(Fr(12, k), v) for k, v in zip(X35, [12, 6, 4, 3, 2, 1])]
F35 = tp((0, 13, 0, 13), curves=[(samp(lambda x: 12 / x, 0.95, 12.6), 'accent')], pts=[(a, b, None, 'p2') for a, b in zip(X35, Y35)], u=0.3, xs=2, ys=2, gx=1, gy=1)
RX = list(range(1, 8)); RA = [ck(Fr(x) * (8 - x), v) for x, v in zip(RX, [7, 12, 15, 16, 15, 12, 7])]
FRA = tp((0, 8.5, 0, 18), curves=[(samp(lambda x: x * (8 - x), 0, 8), 'accent')], pts=[(a, b, None, 'p2') for a, b in zip(RX, RA)], u=0.55, uy=0.17, ys=4, gy=2, xl='$x$', yl='$A$')
V36 = [30, 50, 80, 100, 120]; D36 = [ck(Fr(v * v, 100), d) for v, d in zip(V36, [9, 25, 64, 100, 144])]
S_.append((T("Funcions donades per la seua equació", "Funciones dadas por su ecuación"), [
 (1, T(r"Calcula el valor de $y=4x-3$ per a:", r"Calcula el valor de $y=4x-3$ para:") + tasks(4, ['$x=%s$' % tn(v) if not isinstance(v, Fr) or v.denominator == 1 else r'$x=\frac12$' for v in X31])
     + recorda(T(r"Substituïm la $x$ pel seu valor (entre parèntesis si és negatiu) i fem les operacions. El punt $(x,\ y)$ obtingut és del gràfic.", r"Sustituimos la $x$ por su valor (entre paréntesis si es negativo) y hacemos las operaciones. El punto $(x,\ y)$ obtenido es de la gráfica.")),
     tasks(4, [r'$4\cdot(-2)-3=\res{-11}$', r'$4\cdot0-3=\res{-3}$', r'$4\cdot\frac12-3=\res{-1}$', r'$4\cdot3-3=\res{9}$'])),
 (1, T(r"Fes una taula de valors de $y=-x+2$ per a $x$ de $-2$ a $4$ i representa-la.", r"Haz una tabla de valores de $y=-x+2$ para $x$ de $-2$ a $4$ y represéntala."),
     tv(X32, Y32) + center(F32) + T(r"Els punts estan alineats: és una recta decreixent.", r"Los puntos están alineados: es una recta decreciente.")),
 (1, T(r"Fes la taula de valors de $y=x^2-2$ per a $x=-3,\ -2,\ \ldots,\ 3$ i dibuixa'n el gràfic.", r"Haz la tabla de valores de $y=x^2-2$ para $x=-3,\ -2,\ \ldots,\ 3$ y dibuja su gráfica."),
     tv(X33, Y33) + center(F33) + T(r"Compte: $(-3)^2-2=9-2=7$. Els punts no estan alineats: els unim amb una corba suau (una paràbola).", r"Cuidado: $(-3)^2-2=9-2=7$. Los puntos no están alineados: los unimos con una curva suave (una parábola).")),
 (2, T(r"Quins d'aquests punts són del gràfic de $y=3x-1$?", r"¿Cuáles de estos puntos son de la gráfica de $y=3x-1$?") + tasks(4, [r'$A(2,\ 5)$', r'$B(-1,\ -4)$', r'$C(0,\ 1)$', r'$D\left(\frac13,\ 0\right)$']),
     tasks(4, [r'$3\cdot2-1=5$: \rest{sí}', r'$3\cdot(-1)-1=-4$: \rest{sí}', r'$3\cdot0-1=-1\neq1$: \rest{no}', r'$3\cdot\frac13-1=0$: \rest{sí}'])),
 (2, T(r"Troba el valor de $x$ en cada cas:", r"Halla el valor de $x$ en cada caso:")
     + tasks(1, [T(r"Per a quin valor de $x$ la funció $y=5x+2$ val 17?", r"¿Para qué valor de $x$ la función $y=5x+2$ vale 17?"),
                 T(r"Per a quin valor de $x$ la funció $y=-2x+3$ val 9?", r"¿Para qué valor de $x$ la función $y=-2x+3$ vale 9?"),
                 T(r"Per a quins valors de $x$ la funció $y=x^2$ val 16?", r"¿Para qué valores de $x$ la función $y=x^2$ vale 16?")]),
     tasks(1, [r'$5x+2=17\Rightarrow 5x=15\Rightarrow \res{x=3}$', r'$-2x+3=9\Rightarrow -2x=6\Rightarrow \res{x=-3}$', r'$x^2=16\Rightarrow \res{x=4}$ ' + T('o', 'o') + r' $\res{x=-4}$'])),
 (2, T(r"Fes la taula de $y=\frac{12}{x}$ per a $x=1,\ 2,\ 3,\ 4,\ 6,\ 12$ i dibuixa'n el gràfic. Quant val $y$ per a $x=0$?", r"Haz la tabla de $y=\frac{12}{x}$ para $x=1,\ 2,\ 3,\ 4,\ 6,\ 12$ y dibuja su gráfica. ¿Cuánto vale $y$ para $x=0$?"),
     tv(X35, Y35) + center(F35) + T(r"Per a $x=0$ \rest{no hi ha valor}: no es pot dividir entre 0.", r"Para $x=0$ \rest{no hay valor}: no se puede dividir entre 0.")),
 (3, T(r"Un rectangle té 16\,m de perímetre i base $x$. a) Comprova que l'altura és $8-x$ i escriu l'equació de l'àrea $A$. b) Fes la taula per a $x=1,\ \ldots,\ 7$ i el gràfic. c) Quines dimensions donen l'àrea màxima?",
       r"Un rectángulo tiene 16\,m de perímetro y base $x$. a) Comprueba que la altura es $8-x$ y escribe la ecuación del área $A$. b) Haz la tabla para $x=1,\ \ldots,\ 7$ y la gráfica. c) ¿Qué dimensiones dan el área máxima?"),
     T(r"a) Base més altura és la meitat del perímetre, 8: $h=8-x$ i $\res{A=x\,(8-x)}$.", r"a) Base más altura es la mitad del perímetro, 8: $h=8-x$ y $\res{A=x\,(8-x)}$.")
     + center(tv(RX, RA, 'x', 'A')) + center(FRA)
     + T(r"c) L'àrea màxima és 16\,m$^2$ per a $x=4$: \rest{un quadrat de 4\,m de costat}.", r"c) El área máxima es 16\,m$^2$ para $x=4$: \rest{un cuadrado de 4\,m de lado}.")),
 (3, T(r"La distància que necessita un cotxe per a frenar (en m) es pot calcular amb $d=\frac{v^2}{100}$, on $v$ és la velocitat en km/h. a) Fes la taula per a 30, 50, 80, 100 i 120\,km/h. b) Si la velocitat es duplica de 50 a 100\,km/h, la distància també es duplica? c) Quina distància necessita a 90\,km/h?",
       r"La distancia que necesita un coche para frenar (en m) se puede calcular con $d=\frac{v^2}{100}$, donde $v$ es la velocidad en km/h. a) Haz la tabla para 30, 50, 80, 100 y 120\,km/h. b) Si la velocidad se duplica de 50 a 100\,km/h, ¿la distancia también se duplica? c) ¿Qué distancia necesita a 90\,km/h?"),
     tv(V36, D36, 'v', 'd')
     + T(r" \quad b) \rest{No}: passa de 25\,m a 100\,m, es multiplica per 4. \quad c) $d=\frac{90^2}{100}=\frac{8100}{100}=\res{81\text{ m}}$.", r" \quad b) \rest{No}: pasa de 25\,m a 100\,m, se multiplica por 4. \quad c) $d=\frac{90^2}{100}=\frac{8100}{100}=\res{81\text{ m}}$.")),
]))
CHK(lin(5, 2)(3) == 17 and lin(-2, 3)(-3) == 9 and 4 ** 2 == (-4) ** 2 == 16 and Fr(90 ** 2, 100) == 81 and Fr(100 ** 2, 100) == 4 * Fr(50 ** 2, 100))
CHK(max(RA) == 16 == RA[3])

# =====================================================================
# 4. Funció de proporcionalitat
# =====================================================================
P41 = [([1, 2, 4], [5, 10, 20]), ([2, 3, 5], [6, 8, 12]), ([2, 4, 6], [-1, -2, -3])]
def isprop(Tb): return len({fr(y) / x for x, y in zip(*Tb)}) == 1
CHK(isprop(P41[0]) and not isprop(P41[1]) and isprop(P41[2]))
F42 = tp(W5, fns=[(2, 0, 'accent'), (-3, 0, 'teal'), (Fr(1, 3), 0, 'navy')], labs=[(2.3, 4.6, '$y=2x$', 'right'), (-1.4, 4.6, '$y=-3x$', 'left'), (4.2, 1.8, r'$y=\frac x3$', 'above')], u=0.4)
TEL = fr('4.5')
X44 = [1, 2, 4, 6]; Y44 = [ck(TEL * k, v) for k, v in zip(X44, ['4.5', '9', '18', '27'])]
F44 = tp((0, 6.6, 0, 30), fns=[('4.5', 0, 'accent', 0, 6.4)], pts=[(a, b, None, 'p2') for a, b in zip(X44, Y44)], u=0.7, uy=0.12, ys=5, gy=5, xl='m', yl='€')
CON = fr('0.06')
LIB = fr('0.85')
S_.append((T("Funció de proporcionalitat: $y=mx$", "Función de proporcionalidad: $y=mx$"), [
 (1, T(r"Quines taules corresponen a una funció de proporcionalitat? Escriu-ne l'equació.", r"¿Qué tablas corresponden a una función de proporcionalidad? Escribe su ecuación.") + side(*[tv(*t_) for t_ in P41])
     + recorda(T(r"En una funció de proporcionalitat $y=mx$, el quocient $\frac yx$ és sempre $m$. El gràfic és una recta que passa per l'origen.", r"En una función de proporcionalidad $y=mx$, el cociente $\frac yx$ es siempre $m$. La gráfica es una recta que pasa por el origen.")),
     T(r"a) $\frac51=\frac{10}2=\frac{20}4=5$: $\res{y=5x}$. \quad b) $\frac62=3\neq\frac83$: \rest{no}. \quad c) $\frac{-1}2=\frac{-2}4=\frac{-3}6=-0{,}5$: $\res{y=-0{,}5x}$.",
       r"a) $\frac51=\frac{10}2=\frac{20}4=5$: $\res{y=5x}$. \quad b) $\frac62=3\neq\frac83$: \rest{no}. \quad c) $\frac{-1}2=\frac{-2}4=\frac{-3}6=-0{,}5$: $\res{y=-0{,}5x}$.")),
 (1, T(r"Representa en els mateixos eixos $y=2x$, $y=-3x$ i $y=\frac x3$. Quines són creixents? Quina és la més inclinada?", r"Representa en los mismos ejes $y=2x$, $y=-3x$ e $y=\frac x3$. ¿Cuáles son crecientes? ¿Cuál es la más inclinada?"),
     center(F42) + T(r"Creixents: $y=2x$ i $y=\frac x3$ ($m>0$). La més inclinada és $\res{y=-3x}$ (3 és el pendent més gran sense el signe).", r"Crecientes: $y=2x$ e $y=\frac x3$ ($m>0$). La más inclinada es $\res{y=-3x}$ (3 es la pendiente más grande sin el signo).")),
 (1, T(r"Escriu l'equació de la recta que passa per l'origen i pel punt:", r"Escribe la ecuación de la recta que pasa por el origen y por el punto:") + tasks(3, [r'$(3,\ 12)$', r'$(-2,\ 5)$', r'$(4,\ -2)$']),
     tasks(3, [r'$m=\frac{12}3=4$: $\res{y=4x}$', r'$m=\frac{5}{-2}$: $\res{y=-2{,}5x}$', r'$m=\frac{-2}{4}$: $\res{y=-0{,}5x}$'])),
 (2, T(r"Una tela costa 4,50\,€ el metre. Escriu la funció del preu $y$ segons els metres $x$, fes una taula i el gràfic. Quants metres comprem amb 27\,€?", r"Una tela cuesta 4,50\,€ el metro. Escribe la función del precio $y$ según los metros $x$, haz una tabla y la gráfica. ¿Cuántos metros compramos con 27\,€?"),
     r'$\res{y=4{,}5x}$\qquad ' + tv(X44, Y44, 'm', '€') + center(F44) + T(r"$4{,}5x=27\Rightarrow x=\frac{27}{4{,}5}=\res{6\text{ m}}$.", r"$4{,}5x=27\Rightarrow x=\frac{27}{4{,}5}=\res{6\text{ m}}$.")),
 (2, T(r"Un cotxe gasta 6 litres de gasolina cada 100\,km. a) Escriu la funció dels litres $y$ que gasta segons els km $x$. b) Quant gasta en 350\,km? c) Quants km pot fer amb 45 litres?",
       r"Un coche gasta 6 litros de gasolina cada 100\,km. a) Escribe la función de los litros $y$ que gasta según los km $x$. b) ¿Cuánto gasta en 350\,km? c) ¿Cuántos km puede hacer con 45 litros?"),
     T(r"a) $m=\frac{6}{100}=0{,}06$: $\res{y=0{,}06x}$. \quad b) $0{,}06\cdot350=\res{21\text{ L}}$. \quad c) $0{,}06x=45\Rightarrow x=\res{750\text{ km}}$.", r"a) $m=\frac{6}{100}=0{,}06$: $\res{y=0{,}06x}$. \quad b) $0{,}06\cdot350=\res{21\text{ L}}$. \quad c) $0{,}06x=45\Rightarrow x=\res{750\text{ km}}$.")),
 (2, T(r"Sense dibuixar-les, digues si aquestes rectes són creixents o decreixents i ordena-les de menys a més inclinada: $y=-5x$, \ $y=\frac12x$, \ $y=2x$, \ $y=-x$.", r"Sin dibujarlas, di si estas rectas son crecientes o decrecientes y ordénalas de menos a más inclinada: $y=-5x$, \ $y=\frac12x$, \ $y=2x$, \ $y=-x$."),
     T(r"Creixents: $y=\frac12x$ i $y=2x$; decreixents: $y=-5x$ i $y=-x$.\newline Ordre: $\res{y=\frac12x}$, \ $\res{y=-x}$, \ $\res{y=2x}$, \ $\res{y=-5x}$.", r"Crecientes: $y=\frac12x$ e $y=2x$; decrecientes: $y=-5x$ e $y=-x$.\newline Orden: $\res{y=\frac12x}$, \ $\res{y=-x}$, \ $\res{y=2x}$, \ $\res{y=-5x}$.")),
 (3, T(r"Un dia, 1 euro equival a 0,85 lliures. a) Escriu la funció que passa d'euros ($x$) a lliures ($y$). b) Quantes lliures són 60\,€? c) Quants euros són 34 lliures? d) Escriu també la funció que passa de lliures a euros. És de proporcionalitat?",
       r"Un día, 1 euro equivale a 0,85 libras. a) Escribe la función que pasa de euros ($x$) a libras ($y$). b) ¿Cuántas libras son 60\,€? c) ¿Cuántos euros son 34 libras? d) Escribe también la función que pasa de libras a euros. ¿Es de proporcionalidad?"),
     T(r"a) $\res{y=0{,}85x}$. \quad b) $0{,}85\cdot60=\res{51}$ lliures. \quad c) $0{,}85x=34\Rightarrow x=\res{40\text{ €}}$. \quad d) $x=\frac{y}{0{,}85}$, és a dir, euros $=\frac{1}{0{,}85}\cdot$ lliures $\approx1{,}18\cdot$ lliures: \rest{sí}, també és de proporcionalitat.",
       r"a) $\res{y=0{,}85x}$. \quad b) $0{,}85\cdot60=\res{51}$ libras. \quad c) $0{,}85x=34\Rightarrow x=\res{40\text{ €}}$. \quad d) $x=\frac{y}{0{,}85}$, es decir, euros $=\frac{1}{0{,}85}\cdot$ libras $\approx1{,}18\cdot$ libras: \rest{sí}, también es de proporcionalidad.")),
]))
CHK(Fr(27) / TEL == 6 and CON * 350 == 21 and Fr(45) / CON == 750 and LIB * 60 == 51 and Fr(34) / LIB == 40 and abs(1 / 0.85 - 1.18) < 0.005)

# =====================================================================
# 5. Pendent d'una recta
# =====================================================================
PP = [((1, 2), (4, 11)), ((-2, 5), (1, -1)), ((0, 3), (6, 7)), ((-3, 4), (5, 4))]
MP5 = [ck(slope(*p_), v) for p_, v in zip(PP, [3, -2, Fr(2, 3), 0])]
LG = [(2, -1), (Fr(-1, 2), 2), (Fr(3, 4), -1), (-3, 3)]
FG = [tp((-4, 4, -4, 4), fns=[(m, n, 'accent')], u=0.3) for m, n in LG]
F53 = tp((-1, 5, -1, 6), fns=[(3, -1, 'accent'), (Fr(-1, 2), 4, 'teal')], pts=[(1, 2, '$A$', 'p0', 'left'), (2, 5, None, 'p0'), (0, 4, '$B$', 'p1', 'above right'), (2, 3, None, 'p1'), (4, 2, None, 'p1')], u=0.5)
CHK(lin(3, -1)(1) == 2 and lin(3, -1)(2) == 5 and lin(Fr(-1, 2), 4)(2) == 3 and lin(Fr(-1, 2), 4)(4) == 2)
S_.append((T("Pendent d'una recta", "Pendiente de una recta"), [
 (1, T(r"Calcula el pendent de la recta que passa per cada parell de punts i digues si és creixent, decreixent o constant:", r"Calcula la pendiente de la recta que pasa por cada par de puntos y di si es creciente, decreciente o constante:")
     + tasks(2, [r'$(1,\ 2)$ ' + T('i', 'y') + r' $(4,\ 11)$', r'$(-2,\ 5)$ ' + T('i', 'y') + r' $(1,\ -1)$', r'$(0,\ 3)$ ' + T('i', 'y') + r' $(6,\ 7)$', r'$(-3,\ 4)$ ' + T('i', 'y') + r' $(5,\ 4)$'])
     + recorda(T(r"$m=\dfrac{y_2-y_1}{x_2-x_1}$: és el que augmenta $y$ quan $x$ augmenta 1. Si $m>0$ la recta puja; si $m<0$, baixa; si $m=0$, és horitzontal.", r"$m=\dfrac{y_2-y_1}{x_2-x_1}$: es lo que aumenta $y$ cuando $x$ aumenta 1. Si $m>0$ la recta sube; si $m<0$, baja; si $m=0$, es horizontal.")),
     tasks(2, [r'$m=\frac{11-2}{4-1}=\frac93=\res{3}$: ' + T('creixent', 'creciente'), r'$m=\frac{-1-5}{1+2}=\frac{-6}3=\res{-2}$: ' + T('decreixent', 'decreciente'),
               r'$m=\frac{7-3}{6-0}=\frac46=\res{\frac23}$: ' + T('creixent', 'creciente'), r'$m=\frac{4-4}{5+3}=\res{0}$: ' + T('constant', 'constante')])),
 (1, T(r"Llig el pendent de cada recta en el gràfic (busca dos punts que caiguen en la quadrícula):", r"Lee la pendiente de cada recta en la gráfica (busca dos puntos que caigan en la cuadrícula):")
     + side(*[cap('%s)' % 'abcd'[i], f) for i, f in enumerate(FG)]),
     tasks(4, [r'$\res{m=2}$', r'$\res{m=-\frac12}$', r'$\res{m=\frac34}$', r'$\res{m=-3}$'])),
 (2, T(r"Dibuixa la recta que passa per $A(1,\ 2)$ i té pendent 3, i la recta que passa per $B(0,\ 4)$ i té pendent $-\frac12$.", r"Dibuja la recta que pasa por $A(1,\ 2)$ y tiene pendiente 3, y la recta que pasa por $B(0,\ 4)$ y tiene pendiente $-\frac12$."),
     T(r"Des d'$A$ avancem 1 i pugem 3: $(2,\ 5)$. Des de $B$ avancem 2 i baixem 1: $(2,\ 3)$, $(4,\ 2)$\ldots", r"Desde $A$ avanzamos 1 y subimos 3: $(2,\ 5)$. Desde $B$ avanzamos 2 y bajamos 1: $(2,\ 3)$, $(4,\ 2)$\ldots") + center(F53)),
 (2, T(r"Una carretera té un pendent del 12\,\%: puja 12\,m per cada 100\,m en horitzontal. a) Quant puja en 3\,km? b) Una rampa té un pendent del 8\,\% i ha de pujar 0,6\,m. Quina longitud horitzontal ha de tindre?",
       r"Una carretera tiene una pendiente del 12\,\%: sube 12\,m por cada 100\,m en horizontal. a) ¿Cuánto sube en 3\,km? b) Una rampa tiene una pendiente del 8\,\% y tiene que subir 0,6\,m. ¿Qué longitud horizontal tiene que tener?"),
     T(r"a) $m=0{,}12$; \ $0{,}12\cdot3000=\res{360\text{ m}}$. \quad b) $0{,}08\cdot x=0{,}6\Rightarrow x=\frac{0{,}6}{0{,}08}=\res{7{,}5\text{ m}}$.", r"a) $m=0{,}12$; \ $0{,}12\cdot3000=\res{360\text{ m}}$. \quad b) $0{,}08\cdot x=0{,}6\Rightarrow x=\frac{0{,}6}{0{,}08}=\res{7{,}5\text{ m}}$.")),
 (2, T(r"Comprova amb els pendents si els punts estan alineats:", r"Comprueba con las pendientes si los puntos están alineados:") + tasks(1, [r'$A(0,\ 1)$, $B(2,\ 7)$, $C(5,\ 16)$', r'$P(-1,\ 3)$, $Q(1,\ 2)$, $R(5,\ -1)$']),
     tasks(1, [r'$m_{AB}=\frac62=3$, \ $m_{BC}=\frac93=3$: \rest{' + T('sí', 'sí') + '}', r'$m_{PQ}=\frac{-1}{2}$, \ $m_{QR}=\frac{-3}{4}$: \rest{no}'])),
 (2, T(r"Sense dibuixar-les, ordena les rectes de menys a més inclinada: $r$: passa per $(0,\ 0)$ i $(2,\ 6)$; \ $s$: passa per $(1,\ 1)$ i $(5,\ 3)$; \ $t$: passa per $(0,\ 4)$ i $(1,\ 0)$.",
       r"Sin dibujarlas, ordena las rectas de menos a más inclinada: $r$: pasa por $(0,\ 0)$ y $(2,\ 6)$; \ $s$: pasa por $(1,\ 1)$ y $(5,\ 3)$; \ $t$: pasa por $(0,\ 4)$ y $(1,\ 0)$."),
     T(r"$m_r=3$, \ $m_s=\frac24=0{,}5$, \ $m_t=-4$. Sense el signe: $0{,}5<3<4$. Ordre: \rest{$s$, $r$, $t$}.", r"$m_r=3$, \ $m_s=\frac24=0{,}5$, \ $m_t=-4$. Sin el signo: $0{,}5<3<4$. Orden: \rest{$s$, $r$, $t$}.")),
 (3, T(r"a) Quin valor ha de tindre $k$ perquè els punts $(0,\ 1)$, $(2,\ 5)$ i $(4,\ k)$ estiguen alineats? b) Quin valor ha de tindre $a$ perquè el pendent de la recta que passa per $(a,\ 3)$ i $(2,\ 7)$ siga 2?",
       r"a) ¿Qué valor tiene que tener $k$ para que los puntos $(0,\ 1)$, $(2,\ 5)$ y $(4,\ k)$ estén alineados? b) ¿Qué valor tiene que tener $a$ para que la pendiente de la recta que pasa por $(a,\ 3)$ y $(2,\ 7)$ sea 2?"),
     T(r"a) El pendent és $\frac{5-1}{2}=2$: de $x=2$ a $x=4$ ha de pujar 4, $k=5+4=\res{9}$. \quad b) $\frac{7-3}{2-a}=2\Rightarrow 4=2\,(2-a)\Rightarrow 2-a=2\Rightarrow \res{a=0}$.",
       r"a) La pendiente es $\frac{5-1}{2}=2$: de $x=2$ a $x=4$ tiene que subir 4, $k=5+4=\res{9}$. \quad b) $\frac{7-3}{2-a}=2\Rightarrow 4=2\,(2-a)\Rightarrow 2-a=2\Rightarrow \res{a=0}$.")),
]))
for (m, n), (A, B) in zip(LG, [((0, -1), (1, 1)), ((0, 2), (2, 1)), ((0, -1), (4, 2)), ((0, 3), (1, 0))]):
    CHK(lin(m, n)(A[0]) == A[1] and lin(m, n)(B[0]) == B[1] and slope(A, B) == m)
CHK(fr('0.12') * 3000 == 360 and fr('0.6') / fr('0.08') == fr('7.5'))
CHK(slope((0, 1), (2, 7)) == slope((2, 7), (5, 16)) == 3 and slope((-1, 3), (1, 2)) == Fr(-1, 2) and slope((1, 2), (5, -1)) == Fr(-3, 4))
CHK(slope((0, 0), (2, 6)) == 3 and slope((1, 1), (5, 3)) == Fr(1, 2) and slope((0, 4), (1, 0)) == -4)
CHK(slope((0, 1), (4, 9)) == 2 and slope((0, 3), (2, 7)) == 2)

# =====================================================================
# 6. Funcions lineals
# =====================================================================
L61 = [(r'y=3x-2', 3, -2), (r'y=-x+5', -1, 5), (r'y=4-2x', -2, 4), (r'y=\frac x2+3', Fr(1, 2), 3), (r'y=-6x', -6, 0)]
F62 = tp((-2, 4, -2, 5), fns=[(1, 1, 'accent'), (-1, 3, 'teal')], pts=[(1, 2, '$(1,\\,2)$', 'p2', 'above')], labs=[(3.2, 4.6, '$y=x+1$', 'left'), (-1.6, 4.2, '$y=-x+3$', 'right')], u=0.5)
CHK(lin(1, 1)(1) == lin(-1, 3)(1) == 2)
F63 = tp((-4, 4, -4, 4), fns=[(2, -1, 'accent'), (Fr(-2, 3), 2, 'teal'), (0, -3, 'navy')], labs=[(2.2, 3.6, '$r$', 'right'), (-3.6, 3.6, '$s$', 'below'), (3.6, -3, '$t$', 'above')], u=0.42)
CHK(lin(Fr(-2, 3), 2)(3) == 0 and lin(Fr(-2, 3), 2)(-3) == 4)
S_.append((T("Funcions lineals: $y=mx+n$", "Funciones lineales: $y=mx+n$"), [
 (1, T(r"Escriu el pendent $m$ i l'ordenada en l'origen $n$ de cada recta:", r"Escribe la pendiente $m$ y la ordenada en el origen $n$ de cada recta:") + tasks(5, ['$%s$' % e for e, _, _ in L61])
     + recorda(T(r"En $y=mx+n$, $m$ és el \textbf{pendent} i $n$ l'\textbf{ordenada en l'origen}: la recta talla l'eix $Y$ en $(0,\ n)$. Les rectes amb el mateix pendent són paral·leles.", r"En $y=mx+n$, $m$ es la \textbf{pendiente} y $n$ la \textbf{ordenada en el origen}: la recta corta el eje $Y$ en $(0,\ n)$. Las rectas con la misma pendiente son paralelas.")),
     tasks(3, [r'$\res{m=3}$, $\res{n=-2}$', r'$\res{m=-1}$, $\res{n=5}$', r'$\res{m=-2}$, $\res{n=4}$', r'$\res{m=\frac12}$, $\res{n=3}$', r'$\res{m=-6}$, $\res{n=0}$'])),
 (1, T(r"Representa en els mateixos eixos $y=x+1$ i $y=-x+3$. En quin punt es tallen?", r"Representa en los mismos ejes $y=x+1$ e $y=-x+3$. ¿En qué punto se cortan?"),
     center(F62) + T(r"Es tallen en $\res{(1,\ 2)}$: per a $x=1$ totes dues donen $y=2$.", r"Se cortan en $\res{(1,\ 2)}$: para $x=1$ las dos dan $y=2$.")),
 (1, T(r"Escriu l'equació de les rectes $r$, $s$ i $t$:", r"Escribe la ecuación de las rectas $r$, $s$ y $t$:") + center(F63),
     tasks(1, [r'$r$: $n=-1$, $m=2$: $\res{y=2x-1}$', r'$s$: $n=2$, $m=-\frac23$: $\res{y=-\frac23x+2}$', r'$t$: $\res{y=-3}$'])),
 (2, T(r"Escriu l'equació de la recta que:", r"Escribe la ecuación de la recta que:")
     + tasks(1, [T(r"té pendent 3 i passa pel punt $(1,\ -2)$;", r"tiene pendiente 3 y pasa por el punto $(1,\ -2)$;"),
                 T(r"té pendent $-\frac12$ i passa pel punt $(4,\ 1)$;", r"tiene pendiente $-\frac12$ y pasa por el punto $(4,\ 1)$;"),
                 T(r"és paral·lela a $y=-2x+1$ i passa per $(3,\ 0)$.", r"es paralela a $y=-2x+1$ y pasa por $(3,\ 0)$.")]),
     tasks(1, [r'$-2=3\cdot1+n\Rightarrow n=-5$: $\res{y=3x-5}$', r'$1=-\frac12\cdot4+n\Rightarrow n=3$: $\res{y=-\frac12x+3}$', r'$m=-2$; \ $0=-6+n\Rightarrow n=6$: $\res{y=-2x+6}$'])),
 (2, T(r"Troba l'equació de la recta que passa per cada parell de punts:", r"Halla la ecuación de la recta que pasa por cada par de puntos:") + tasks(2, [r'$(-1,\ 4)$ ' + T('i', 'y') + r' $(2,\ -2)$', r'$(0,\ -3)$ ' + T('i', 'y') + r' $(4,\ 3)$']),
     tasks(1, [r'$m=\frac{-2-4}{2+1}=-2$; \ $4=-2\cdot(-1)+n\Rightarrow n=2$: $\res{y=-2x+2}$', r'$m=\frac{3+3}{4-0}=\frac32$; \ $n=-3$: $\res{y=\frac32x-3}$'])),
 (2, T(r"Comprova si els punts $A(4,\ 7)$, $B(-1,\ -8)$ i $C(0{,}5;\ -3{,}5)$ són de la recta $y=3x-5$.", r"Comprueba si los puntos $A(4,\ 7)$, $B(-1,\ -8)$ y $C(0{,}5;\ -3{,}5)$ son de la recta $y=3x-5$."),
     tasks(3, [r'$12-5=7$: \rest{' + SI + '}', r'$-3-5=-8$: \rest{' + SI + '}', r'$1{,}5-5=-3{,}5$: \rest{' + SI + '}'])),
 (3, T(r"La recta $y=2x-6$ talla els eixos en dos punts. Troba'ls i calcula l'àrea del triangle que forma la recta amb els eixos.", r"La recta $y=2x-6$ corta los ejes en dos puntos. Hállalos y calcula el área del triángulo que forma la recta con los ejes."),
     T(r"Eix $Y$ ($x=0$): $\res{(0,\ -6)}$. Eix $X$ ($y=0$): $2x-6=0\Rightarrow\res{(3,\ 0)}$. El triangle té catets 3 i 6: $A=\frac{3\cdot6}{2}=\res{9}$ unitats quadrades.",
       r"Eje $Y$ ($x=0$): $\res{(0,\ -6)}$. Eje $X$ ($y=0$): $2x-6=0\Rightarrow\res{(3,\ 0)}$. El triángulo tiene catetos 3 y 6: $A=\frac{3\cdot6}{2}=\res{9}$ unidades cuadradas.")),
 (3, T(r"L'aigua es congela a 0\,°C, que són 32\,°F (graus Fahrenheit), i bull a 100\,°C, que són 212\,°F. La relació és lineal. a) Troba la fórmula $F=mC+n$. b) Quants °F són 25\,°C? c) Quants °C són 50\,°F?",
       r"El agua se congela a 0\,°C, que son 32\,°F (grados Fahrenheit), y hierve a 100\,°C, que son 212\,°F. La relación es lineal. a) Halla la fórmula $F=mC+n$. b) ¿Cuántos °F son 25\,°C? c) ¿Cuántos °C son 50\,°F?"),
     T(r"a) $m=\frac{212-32}{100-0}=1{,}8$ i $n=32$: $\res{F=1{,}8\,C+32}$. \quad b) $1{,}8\cdot25+32=\res{77\text{ °F}}$. \quad c) $1{,}8\,C+32=50\Rightarrow C=\frac{18}{1{,}8}=\res{10\text{ °C}}$.",
       r"a) $m=\frac{212-32}{100-0}=1{,}8$ y $n=32$: $\res{F=1{,}8\,C+32}$. \quad b) $1{,}8\cdot25+32=\res{77\text{ °F}}$. \quad c) $1{,}8\,C+32=50\Rightarrow C=\frac{18}{1{,}8}=\res{10\text{ °C}}$.")),
]))
CHK(lin(3, -5)(1) == -2 and lin(Fr(-1, 2), 3)(4) == 1 and lin(-2, 6)(3) == 0)
CHK(slope((-1, 4), (2, -2)) == -2 and lin(-2, 2)(-1) == 4 and slope((0, -3), (4, 3)) == Fr(3, 2))
CHK(lin(3, -5)(4) == 7 and lin(3, -5)(-1) == -8 and lin(3, -5)(fr('0.5')) == fr('-3.5'))
CHK(lin(2, -6)(3) == 0 and Fr(3 * 6, 2) == 9)
CHK(slope((0, 32), (100, 212)) == fr('1.8') and lin('1.8', 32)(25) == 77 and (Fr(50) - 32) / fr('1.8') == 10)

# =====================================================================
# 7. Funcions constants
# =====================================================================
F71 = tp((-4, 4, -4, 4), fns=[(0, 2, 'accent'), (0, -3, 'teal'), (0, 0, 'navy')], labs=[(3.5, 2, '$y=2$', 'above'), (3.5, -3, '$y=-3$', 'above'), (-3.3, 0, '$y=0$', 'above')], u=0.4)
F71b = tp((-4, 5, -2, 6), fns=[(0, -1, 'accent')], curves=[([(-2, -2), (-2, 6)], 'teal')], pts=[(4, -1, '$(4,\\,-1)$', 'p0', 'above'), (-2, 5, '$(-2,\\,5)$', 'p1', 'right')], u=0.4)
ENV = [([(0, 4), (2, 4)], 'accent'), ([(2, 7), (5, 7)], 'accent'), ([(5, 10), (10, 10)], 'accent')]
F74 = tp((0, 10.6, 0, 11.5), curves=ENV, pts=[(2, 4, None, 'p0'), (5, 7, None, 'p0')], u=0.5, uy=0.3, xs=1, ys=2, gy=1, xl='kg', yl='€')
FL = fr('0.08')
F75 = tp((0, 520, 0, 42), fns=[(0, 30, 'accent', 0, 520), ('0.08', 0, 'teal', 0, 520)], pts=[(375, 30, None, 'p2')], proj=[(375, 30)], u=0.012, uy=0.11, xs=100, gx=50, ys=10, gy=5, xl='min', yl='€')
S_.append((T("Funcions constants: $y=k$", "Funciones constantes: $y=k$"), [
 (1, T(r"Representa en els mateixos eixos les funcions $y=2$, $y=-3$ i $y=0$. Quin pendent tenen?", r"Representa en los mismos ejes las funciones $y=2$, $y=-3$ e $y=0$. ¿Qué pendiente tienen?")
     + recorda(T(r"Una \textbf{funció constant} $y=k$ val sempre el mateix: el gràfic és una recta \textbf{horitzontal} i el pendent és 0. Una recta vertical $x=a$ \textbf{no} és una funció.", r"Una \textbf{función constante} $y=k$ vale siempre lo mismo: la gráfica es una recta \textbf{horizontal} y la pendiente es 0. Una recta vertical $x=a$ \textbf{no} es una función.")),
     center(F71) + T(r"Són rectes horitzontals ($y=0$ és l'eix $X$). Totes tenen pendent $\res{m=0}$.", r"Son rectas horizontales ($y=0$ es el eje $X$). Todas tienen pendiente $\res{m=0}$.")),
 (1, T(r"Escriu l'equació de la recta horitzontal que passa per $(4,\ -1)$ i de la recta vertical que passa per $(-2,\ 5)$. Quina és una funció?", r"Escribe la ecuación de la recta horizontal que pasa por $(4,\ -1)$ y de la recta vertical que pasa por $(-2,\ 5)$. ¿Cuál es una función?"),
     center(F71b) + T(r"Horitzontal: $\res{y=-1}$ (funció constant). Vertical: $\res{x=-2}$, que \rest{no és una funció}.", r"Horizontal: $\res{y=-1}$ (función constante). Vertical: $\res{x=-2}$, que \rest{no es una función}.")),
 (1, T(r"Classifica les funcions en de proporcionalitat, lineals (amb $n\neq0$), constants o cap d'aquestes:", r"Clasifica las funciones en de proporcionalidad, lineales (con $n\neq0$), constantes o ninguna de estas:")
     + tasks(4, [r'$y=-4x$', r'$y=7$', r'$y=2x+1$', r'$y=x^2+1$', r'$y=\frac{x}{5}$', r'$y=3-x$', r'$y=\frac{6}{x}$', r'$y=-2$']),
     tasks(4, [r'\rest{' + T('proporc.', 'proporc.') + '}', r'\rest{' + T('constant', 'constante') + '}', r'\rest{lineal}', r'\rest{' + T('cap', 'ninguna') + '}',
               r'\rest{' + T('proporc.', 'proporc.') + '}', r'\rest{lineal}', r'\rest{' + T('cap', 'ninguna') + '}', r'\rest{' + T('constant', 'constante') + '}'])),
 (2, T(r"Enviar un paquet costa 4\,€ fins a 2\,kg, 7\,€ de 2 a 5\,kg i 10\,€ de 5 a 10\,kg. a) Dibuixa el gràfic. b) Quant costa enviar un paquet de 3,5\,kg? c) Què ix més barat: enviar dos paquets de 3\,kg o un de 6\,kg?",
       r"Enviar un paquete cuesta 4\,€ hasta 2\,kg, 7\,€ de 2 a 5\,kg y 10\,€ de 5 a 10\,kg. a) Dibuja la gráfica. b) ¿Cuánto cuesta enviar un paquete de 3,5\,kg? c) ¿Qué sale más barato: enviar dos paquetes de 3\,kg o uno de 6\,kg?"),
     center(F74) + T(r"b) $\res{7\text{ €}}$. \quad c) Dos de 3\,kg: $7+7=14$\,€; un de 6\,kg: 10\,€. Ix més barat \rest{un paquet de 6\,kg}.", r"b) $\res{7\text{ €}}$. \quad c) Dos de 3\,kg: $7+7=14$\,€; uno de 6\,kg: 10\,€. Sale más barato \rest{un paquete de 6\,kg}.")),
 (2, T(r"Una companyia telefònica ofereix una tarifa plana de 30\,€ al mes i una altra cobra 0,08\,€ per minut. a) Escriu les dues funcions. b) Quant paguem amb cada una si parlem 200 minuts? c) A partir de quants minuts convé la tarifa plana?",
       r"Una compañía telefónica ofrece una tarifa plana de 30\,€ al mes y otra cobra 0,08\,€ por minuto. a) Escribe las dos funciones. b) ¿Cuánto pagamos con cada una si hablamos 200 minutos? c) ¿A partir de cuántos minutos conviene la tarifa plana?"),
     T(r"a) $\res{y=30}$ \ i \ $\res{y=0{,}08x}$. \quad b) 30\,€ i $0{,}08\cdot200=16$\,€. \quad c) $0{,}08x=30\Rightarrow x=375$: a partir de \rest{375 minuts}.", r"a) $\res{y=30}$ \ y \ $\res{y=0{,}08x}$. \quad b) 30\,€ y $0{,}08\cdot200=16$\,€. \quad c) $0{,}08x=30\Rightarrow x=375$: a partir de \rest{375 minutos}.") + center(F75)),
 (3, T(r"La taula correspon a una funció lineal. Troba'n l'equació i explica com és el gràfic. Quin valor tindrà $y$ per a $x=100$?", r"La tabla corresponde a una función lineal. Halla su ecuación y explica cómo es la gráfica. ¿Qué valor tendrá $y$ para $x=100$?") + center(tv([-2, -1, 0, 1, 2], [5] * 5)),
     T(r"$m=\frac{5-5}{-1+2}=0$ i $n=5$: $\res{y=5}$, una recta horitzontal. Per a $x=100$, $y=\res{5}$.", r"$m=\frac{5-5}{-1+2}=0$ y $n=5$: $\res{y=5}$, una recta horizontal. Para $x=100$, $y=\res{5}$.")),
]))
CHK(FL * 200 == 16 and Fr(30) / FL == 375)

# =====================================================================
# 8. Interpretació de gràfics i problemes
# =====================================================================
EXC = [(0, 0), (1, 6), (2, 6), (3, 10), (5, 0)]
FEX = tp((0, 5.6, 0, 11.5), curves=[(EXC, 'accent')], pts=[(a, b, None, 'p2') for a, b in EXC], u=0.9, uy=0.3, ys=2, gy=1, xl='t (h)', yl='d (km)')
TMP = [(0, 10), (4, 6), (8, 8), (12, 16), (16, 18), (20, 12), (24, 9)]
FTMP = tp((0, 25, 0, 20), curves=[(TMP, 'accent')], pts=[(a, b, None, 'p2') for a, b in TMP], u=0.3, uy=0.2, xs=4, gx=2, ys=4, gy=2, xl='h', yl='°C')
def mini(P, l): return cap(l, tp((0, 6.5, 0, 6.5), curves=[(P, 'accent')], u=0.28, xs=2, ys=2, xl='t', yl='d'))
M1, M2, M3 = [(0, 0), (2, 5), (4, 5), (6, 0)], [(0, 0), (3, 3), (6, 6)], [(0, 0), (1, 5), (3, 5), (6, 6)]
TX = lin('1.1', '3.5')
DIP = lin(-25, 800)
GA_, GB_ = lin(15, 30), lin(10, 45)
CA, CB = lin(18), lin(24, -24)
VA, VB = lin(-2, 30), lin(fr('-1.5'), 24)
FCI = tp((0, 5.6, 0, 100), fns=[(18, 0, 'accent', 0, 5.4), (24, -24, 'teal', 1, 5.1)], pts=[(4, 72, None, 'p2')], proj=[(4, 72)], u=0.8, uy=0.04, ys=20, gy=10, xl='t (h)', yl='d (km)')
S_.append((T("Interpretació de gràfics i problemes", "Interpretación de gráficas y problemas"), [
 (1, T(r"El gràfic mostra la distància a casa d'un excursionista. a) A quina distància estava a la 1\,h i mitja? b) Quant de temps va descansar? c) Quina distància màxima es va allunyar? d) Quants km va recórrer en total? e) Va més de pressa a l'anada o a la tornada?",
       r"La gráfica muestra la distancia a casa de un excursionista. a) ¿A qué distancia estaba a la 1\,h y media? b) ¿Cuánto tiempo descansó? c) ¿Qué distancia máxima se alejó? d) ¿Cuántos km recorrió en total? e) ¿Va más deprisa a la ida o a la vuelta?") + center(FEX)
     + recorda(T(r"Llegim el gràfic d'esquerra a dreta: on puja s'allunya, on és horitzontal està parat i on baixa torna. Com més inclinat, més de pressa.", r"Leemos la gráfica de izquierda a derecha: donde sube se aleja, donde es horizontal está parado y donde baja vuelve. Cuanto más inclinada, más deprisa.")),
     T(r"a) $\res{6\text{ km}}$. \ b) De 1 a 2\,h: $\res{1\text{ h}}$. \ c) $\res{10\text{ km}}$ (a les 3\,h). \ d) $10+10=\res{20\text{ km}}$. \ e) Al primer tram fa 6\,km/h i a la tornada, $\frac{10}{2}=5$\,km/h: \rest{més de pressa al principi}.",
       r"a) $\res{6\text{ km}}$. \ b) De 1 a 2\,h: $\res{1\text{ h}}$. \ c) $\res{10\text{ km}}$ (a las 3\,h). \ d) $10+10=\res{20\text{ km}}$. \ e) En el primer tramo hace 6\,km/h y a la vuelta, $\frac{10}{2}=5$\,km/h: \rest{más deprisa al principio}.")),
 (1, T(r"El gràfic dona la temperatura d'un dia. Digues on és creixent i on és decreixent, i quines són la temperatura màxima i la mínima i quan es van assolir.", r"La gráfica da la temperatura de un día. Di dónde es creciente y dónde es decreciente, y cuáles son la temperatura máxima y la mínima y cuándo se alcanzaron.") + center(FTMP),
     T(r"Creixent \rest{de 4 a 16 h}; decreixent \rest{de 0 a 4 h i de 16 a 24 h}. Màxim: \rest{18\,°C a les 16 h}; mínim: \rest{6\,°C a les 4 h}.", r"Creciente \rest{de 4 a 16 h}; decreciente \rest{de 0 a 4 h y de 16 a 24 h}. Máximo: \rest{18\,°C a las 16 h}; mínimo: \rest{6\,°C a las 4 h}.")),
 (2, T(r"Relaciona cada història amb el seu gràfic (temps, distància a casa):", r"Relaciona cada historia con su gráfica (tiempo, distancia a casa):")
     + tasks(1, [T(r"Vaig en bici a casa d'una amiga, m'hi quede una estona i torne.", r"Voy en bici a casa de una amiga, me quedo un rato y vuelvo."),
                 T(r"Isc corrent, pare a descansar i després continue caminant a poc a poc.", r"Salgo corriendo, paro a descansar y después sigo andando despacio."),
                 T(r"Camine sempre a la mateixa velocitat, sense parar.", r"Camino siempre a la misma velocidad, sin parar.")])
     + side(mini(M1, 'A'), mini(M2, 'B'), mini(M3, 'C')),
     T(r"1 → \rest{A}; \ 2 → \rest{C} (puja molt, és horitzontal i puja poc); \ 3 → \rest{B} (una recta).", r"1 → \rest{A}; \ 2 → \rest{C} (sube mucho, es horizontal y sube poco); \ 3 → \rest{B} (una recta).")),
 (2, T(r"Un taxi cobra 3,50\,€ per la baixada de bandera i 1,10\,€ per km. a) Escriu la funció del preu. b) Quant costa un viatge de 12\,km? c) Quants km hem fet si hem pagat 25,50\,€?", r"Un taxi cobra 3,50\,€ por la bajada de bandera y 1,10\,€ por km. a) Escribe la función del precio. b) ¿Cuánto cuesta un viaje de 12\,km? c) ¿Cuántos km hemos hecho si hemos pagado 25,50\,€?")
     + recorda(T(r"Moltes situacions tenen una part fixa $n$ i una part que augmenta (o disminueix) sempre igual per cada unitat, $m$: són funcions lineals $y=mx+n$.", r"Muchas situaciones tienen una parte fija $n$ y una parte que aumenta (o disminuye) siempre igual por cada unidad, $m$: son funciones lineales $y=mx+n$.")),
     T(r"a) $\res{y=1{,}1x+3{,}5}$. \quad b) $1{,}1\cdot12+3{,}5=\res{16{,}70\text{ €}}$. \quad c) $1{,}1x+3{,}5=25{,}5\Rightarrow 1{,}1x=22\Rightarrow x=\res{20\text{ km}}$.", r"a) $\res{y=1{,}1x+3{,}5}$. \quad b) $1{,}1\cdot12+3{,}5=\res{16{,}70\text{ €}}$. \quad c) $1{,}1x+3{,}5=25{,}5\Rightarrow 1{,}1x=22\Rightarrow x=\res{20\text{ km}}$.")),
 (2, T(r"Un dipòsit té 800 litres i se'n buiden 25 cada minut. a) Escriu la funció dels litres que queden. b) Quants litres queden als 12 minuts? c) Quan es buidarà?", r"Un depósito tiene 800 litros y se vacían 25 cada minuto. a) Escribe la función de los litros que quedan. b) ¿Cuántos litros quedan a los 12 minutos? c) ¿Cuándo se vaciará?"),
     T(r"a) $\res{y=-25x+800}$. \quad b) $-300+800=\res{500\text{ L}}$. \quad c) $-25x+800=0\Rightarrow x=\res{32\text{ min}}$.", r"a) $\res{y=-25x+800}$. \quad b) $-300+800=\res{500\text{ L}}$. \quad c) $-25x+800=0\Rightarrow x=\res{32\text{ min}}$.")),
 (2, T(r"La Clara ix de casa a les 10\,h i camina 3\,km en 45 minuts fins a la piscina. Hi està 1\,h 30\,min i torna amb autobús en 15 minuts. Dibuixa el gràfic (hora, distància a casa).", r"Clara sale de casa a las 10\,h y camina 3\,km en 45 minutos hasta la piscina. Está allí 1\,h 30\,min y vuelve en autobús en 15 minutos. Dibuja la gráfica (hora, distancia a casa)."),
     T(r"Els punts on canvia la història són $(10;\ 0)$, $(10{,}75;\ 3)$, $(12{,}25;\ 3)$ i $(12{,}5;\ 0)$:", r"Los puntos donde cambia la historia son $(10;\ 0)$, $(10{,}75;\ 3)$, $(12{,}25;\ 3)$ y $(12{,}5;\ 0)$:")
     + center(tp((9.5, 13, 0, 3.8), curves=[([(10, 0), (10.75, 3), (12.25, 3), (12.5, 0)], 'accent')], u=1.4, uy=0.5, xs=0.5, ys=1, xl='h', yl='km', zero=False))),
 (3, T(r"El gimnàs A cobra 30\,€ de matrícula i 15\,€ al mes, i el gimnàs B, 45\,€ de matrícula i 10\,€ al mes. a) Escriu les dues funcions. b) Quant costa cada un si hi anem 6 mesos? c) Per a quants mesos costen el mateix?",
       r"El gimnasio A cobra 30\,€ de matrícula y 15\,€ al mes, y el gimnasio B, 45\,€ de matrícula y 10\,€ al mes. a) Escribe las dos funciones. b) ¿Cuánto cuesta cada uno si vamos 6 meses? c) ¿Para cuántos meses cuestan lo mismo?"),
     T(r"a) $\res{A:\ y=15x+30}$, \ $\res{B:\ y=10x+45}$. \quad b) A: 120\,€; B: 105\,€ (convé B). \quad c) $15x+30=10x+45\Rightarrow 5x=15\Rightarrow x=\res{3\text{ mesos}}$ (75\,€). Abans de 3 mesos convé A; després, B.",
       r"a) $\res{A:\ y=15x+30}$, \ $\res{B:\ y=10x+45}$. \quad b) A: 120\,€; B: 105\,€ (conviene B). \quad c) $15x+30=10x+45\Rightarrow 5x=15\Rightarrow x=\res{3\text{ meses}}$ (75\,€). Antes de 3 meses conviene A; después, B.")),
 (3, T(r"Un ciclista ix d'un poble a 18\,km/h. Una hora després n'ix un altre pel mateix camí a 24\,km/h. a) Escriu la distància recorreguda per cada un en funció del temps $t$ que fa que ha eixit el primer. b) Quan i on l'atrapa?",
       r"Un ciclista sale de un pueblo a 18\,km/h. Una hora después sale otro por el mismo camino a 24\,km/h. a) Escribe la distancia recorrida por cada uno en función del tiempo $t$ que hace que ha salido el primero. b) ¿Cuándo y dónde lo alcanza?"),
     T(r"a) Primer: $\res{d=18t}$; segon: $\res{d=24\,(t-1)=24t-24}$ (per a $t\geq1$). \quad b) $18t=24t-24\Rightarrow 6t=24\Rightarrow t=4$: l'atrapa a les $\res{4\text{ h}}$, a $\res{72\text{ km}}$ del poble.",
       r"a) Primero: $\res{d=18t}$; segundo: $\res{d=24\,(t-1)=24t-24}$ (para $t\geq1$). \quad b) $18t=24t-24\Rightarrow 6t=24\Rightarrow t=4$: lo alcanza a las $\res{4\text{ h}}$, a $\res{72\text{ km}}$ del pueblo.") + center(FCI)),
 (3, T(r"Encenem alhora dues espelmes: una fa 30\,cm i es crema 2\,cm cada hora; l'altra fa 24\,cm i es crema 1,5\,cm cada hora. a) Escriu les dues funcions. b) Quan tindran la mateixa altura? Quina? c) Quina s'acaba abans?",
       r"Encendemos a la vez dos velas: una mide 30\,cm y se quema 2\,cm cada hora; la otra mide 24\,cm y se quema 1,5\,cm cada hora. a) Escribe las dos funciones. b) ¿Cuándo tendrán la misma altura? ¿Cuál? c) ¿Cuál se acaba antes?"),
     T(r"a) $\res{y=-2x+30}$ \ i \ $\res{y=-1{,}5x+24}$. \quad b) $30-2x=24-1{,}5x\Rightarrow 6=0{,}5x\Rightarrow x=\res{12\text{ h}}$, amb $\res{6\text{ cm}}$. \quad c) La primera s'acaba a les $\frac{30}{2}=15$\,h i la segona, a les $\frac{24}{1{,}5}=16$\,h: \rest{la primera}.",
       r"a) $\res{y=-2x+30}$ \ y \ $\res{y=-1{,}5x+24}$. \quad b) $30-2x=24-1{,}5x\Rightarrow 6=0{,}5x\Rightarrow x=\res{12\text{ h}}$, con $\res{6\text{ cm}}$. \quad c) La primera se acaba a las $\frac{30}{2}=15$\,h y la segunda, a las $\frac{24}{1{,}5}=16$\,h: \rest{la primera}.")),
]))
CHK(EXC[1][1] == 6 and max(b for _, b in EXC) == 10 and slope(EXC[3], EXC[4]) == -5)
CHK(TX(12) == fr('16.7') and (fr('25.5') - fr('3.5')) / fr('1.1') == 20)
CHK(DIP(12) == 500 and Fr(800, 25) == 32)
CHK(GA_(6) == 120 and GB_(6) == 105 and GA_(3) == GB_(3) == 75)
CHK(CA(4) == CB(4) == 72)
CHK(VA(12) == VB(12) == 6 and Fr(30, 2) == 15 and Fr(24) / fr('1.5') == 16)
CHK(fr('0.75') * 60 == 45 and fr('12.25') - fr('10.75') == fr('1.5'))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = T("funcions, variable independent, variable dependent, taules de valors, gràfics, equació d'una funció, funció de proporcionalitat, pendent, funció lineal, ordenada en l'origen, funció constant, interpretació de gràfics",
       'funciones, variable independiente, variable dependiente, tablas de valores, gráficas, ecuación de una función, función de proporcionalidad, pendiente, función lineal, ordenada en el origen, función constante, interpretación de gráficas')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T("Funcions", 'Funciones')
NU = 10

def build(sol_):
    if ES:
        sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad %d: %s' % (t, NU, TIT), capcalera='%s · Unidad %d: %s' % (t, NU, TIT), pdfkeywords=KW, curs='2eso')
        cap_ = assignatura('2eso') + '{' + ('Soluciones de la ficha · Unidad %d' % NU if sol_ else 'Ficha de ejercicios · Unidad %d' % NU) + '}{' + TIT + '}'
    else:
        t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat %d: %s. 2n d'ESO}" % (t, NU, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat %d: %s · 2n d'ESO" % (t, NU, TIT))
        assert "2n d'ESO" in p and 'Unitat %d' % NU in p and 'unitat %d' % NU in p
        cap_ = r'\capcalera{Matemàtiques}{2n ESO}{' + ('Solucions de la fitxa · Unitat %d' % NU if sol_ else "Fitxa d'exercicis · Unitat %d" % NU) + '}{' + TIT + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol_ else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{14}\n\\input{../comu/fentmates.tex}\n\\fmcurs{2eso}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap_ + '\n')
    if not sol_:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs eines per a passar de la taula al gràfic, per a dibuixar el gràfic d'una equació, per a calcular pendents i per a explorar les rectes $y=mx+n$.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás herramientas para pasar de la tabla a la gráfica, para dibujar la gráfica de una ecuación, para calcular pendientes y para explorar las rectas $y=mx+n$.") if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Per a dibuixar gràfics fes servir paper quadriculat i escriu el nom i la unitat de cada eix. Les seccions segueixen l'ordre dels apunts de la unitat (10.1--10.8).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Para dibujar gráficas usa papel cuadriculado y escribe el nombre y la unidad de cada eje. Las secciones siguen el orden de los apuntes de la unidad (10.1--10.8)."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            out.append('\\ex{%d} %s\n\n' % (st, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't%d-fitxa-%s%s.tex' % (NU, 'solucions' if sol_ else 'exercicis', '-es' if ES else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(x[1]) for x in S_), T('exercicis', 'ejercicios'), NCHK[0], 'comprovacions')
