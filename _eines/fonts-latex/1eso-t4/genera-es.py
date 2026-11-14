# Versió en castellà de genera.py. Genera t4-fitxa-exercicis-es.tex i t4-fitxa-solucions-es.tex (1r ESO, Unitat 4: Fraccions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les solucions de les operacions es calculen amb fraccions exactes (vegeu op/ops).
import os, re, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'

def recorda(t): return '\\recorda{%s}' % t

# ---------- fraccions ----------
def fr(a, b): return r'\dfrac{%s}{%s}' % (a, b)
def ftex(f):
    f = Fr(f)
    if f.denominator == 1: return str(f.numerator)
    return ('-' if f < 0 else '') + fr(abs(f.numerator), f.denominator)
def tx(e):
    """'(1/4+2/3)*3:1/2' -> LaTeX"""
    s = re.sub(r'(\d+)/(\d+)', r'\\dfrac{\1}{\2}', e)
    s = s.replace('*', r'\cdot ').replace('(', r'\left(').replace(')', r'\right)')
    return s
def val(e):
    py = re.sub(r'(\d+)(?:/(\d+))?', lambda m: 'Fr(%s,%s)' % (m[1], m[2] or 1), e).replace(':', '/')
    return eval(py)
def op(e): return '$' + tx(e) + '$'
def ops(e): return '$' + tx(e) + r'=\res{' + ftex(val(e)) + '}$'
def lst(fs): return ',\\ '.join(fr(*f.split('/')) if '/' in f else f for f in fs)
def irr(a, b): return ftex(Fr(a, b))

# ---------- figures TikZ ----------
SH = 'accent!75'
def tz_rect(rows, cols, on, s=0.42):
    g = ''.join(r'\fill[%s] (%d,%d) rectangle ++(1,1);' % (SH, k % cols, rows - 1 - k // cols) for k in range(on))
    return r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]%s\draw[thick] (0,0) grid (%d,%d);\end{tikzpicture}' % (s, g, cols, rows)
def tz_circ(n, on, r=0.75):
    g = ''
    for k in range(on):
        a0 = 90 - 360 * k / n; a1 = a0 - 360 / n
        g += r'\fill[%s] (0,0) -- (%.2f:%s) arc[start angle=%.2f,end angle=%.2f,radius=%s] -- cycle;' % (SH, a0, r, a0, a1, r)
    g += r'\draw[thick] (0,0) circle (%s);' % r
    if n > 1: g += ''.join(r'\draw[thick] (0,0) -- (%.2f:%s);' % (90 - 360 * k / n, r) for k in range(n))
    return r'\begin{tikzpicture}[baseline=(current bounding box.center)]%s\end{tikzpicture}' % g
def tz_bar(n, on, w=4.2, h=0.55):
    c = w / n
    g = ''.join(r'\fill[%s] (%.3f,0) rectangle ++(%.3f,%s);' % (SH, k * c, c, h) for k in range(on))
    g += ''.join(r'\draw (%.3f,0)--(%.3f,%s);' % (k * c, k * c, h) for k in range(1, n))
    return r'\begin{tikzpicture}[baseline=(current bounding box.center)]%s\draw[thick] (0,0) rectangle (%s,%s);\end{tikzpicture}' % (g, w, h)
def tz_line(units, den=0, pts=(), w=9.0):
    u = w / units
    g = r'\draw[-latex,thick] (-0.3,0)--(%.2f,0);' % (w + 0.5)
    if den:
        g += ''.join(r'\draw[muted] (%.3f,0.1)--(%.3f,-0.1);' % (k * u / den, k * u / den) for k in range(units * den + 1) if k % den)
    g += ''.join(r'\draw[thick] (%.2f,0.18)--(%.2f,-0.18) node[below=1pt,font=\small]{$%d$};' % (i * u, i * u, i) for i in range(units + 1))
    for i, (num, d) in enumerate(pts):
        x = num / d * u
        g += r'\fill[accent] (%.3f,0) circle (0.09) node[%s=3pt,text=accent]{$\frac{%d}{%d}$};' % (x, 'above' if i % 2 == 0 else 'below=10pt', num, d)
    return r'\begin{tikzpicture}[baseline=0]%s\end{tikzpicture}' % g

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
FIG1 = [(tz_rect(2, 5, 4), '4/10'), (tz_rect(2, 2, 3), '3/4'), (tz_circ(7, 1), '1/7'), (tz_rect(2, 2, 2), '2/4'), (tz_circ(7, 5), '5/7'), (tz_rect(2, 3, 4), '4/6')]
S.append(("El concepto de fracción", [
 (1, r"¿Qué fracción representa la parte pintada de cada figura?" + tasks(3, [f for f, _ in FIG1])
     + recorda(r"El \textbf{denominador} indica en cuántas partes \textbf{iguales} dividimos la unidad; el \textbf{numerador}, cuántas tomamos."),
     tasks(6, ['$%s$' % fr(*a.split('/')) for _, a in FIG1])),
 (1, r"Indica el numerador y el denominador de cada fracción y escribe cómo se lee:" + tasks(4, ['$%s$' % fr(3, 5), '$%s$' % fr(4, 6), '$%s$' % fr(12, 15), '$%s$' % fr(4, 3)]),
     tasks(2, [r"num.\ 3, den.\ 5: tres quintos", r"num.\ 4, den.\ 6: cuatro sextos", r"num.\ 12, den.\ 15: doce quinceavos", r"num.\ 4, den.\ 3: cuatro tercios"])),
 (1, r"Pinta en cada figura la fracción indicada:" + tasks(3, [r'$%s$\ \ %s' % (fr(3, 5), tz_bar(5, 0, 3.5)), r'$%s$\ \ %s' % (fr(5, 8), tz_rect(2, 4, 0)), r'$%s$\ \ %s' % (fr(2, 3), tz_circ(3, 0, 0.65))]),
     tasks(3, [r'$%s$\ \ %s' % (fr(3, 5), tz_bar(5, 3, 3.5)), r'$%s$\ \ %s' % (fr(5, 8), tz_rect(2, 4, 5)), r'$%s$\ \ %s' % (fr(2, 3), tz_circ(3, 2, 0.65))])),
 (1, r"Representa en la recta numérica las fracciones $%s$ y $%s$.\par\smallskip{\centering %s\par}" % (fr(6, 10), fr(7, 4), tz_line(2)),
     r"Dividimos cada unidad en 10 partes para $%s$ y en 4 para $%s=1+%s$:\par\smallskip{\centering %s\par}" % (fr(6, 10), fr(7, 4), fr(3, 4), tz_line(2, 4, [(6, 10), (7, 4)]))),
 (2, r"Clasifica las fracciones en propias, impropias o iguales a la unidad. Escribe las impropias como unidades enteras más una fracción propia." + tasks(6, ['$%s$' % fr(*x) for x in [(7, 3), (5, 8), (9, 9), (13, 4), (2, 11), (20, 6)]]),
     tasks(3, [r"Impropia: $2+%s$" % fr(1, 3), r"Propia", r"Igual a 1", r"Impropia: $3+%s$" % fr(1, 4), r"Propia", r"Impropia: $3+%s$" % fr(2, 6)])),
 (2, r"¿Qué fracción representa?" + tasks(2, [r"15 minutos de una hora", r"4 meses de un año", r"5 días de una semana", r"300 gramos de 1 kg"]),
     tasks(4, ['$%s$' % fr(15, 60), '$%s$' % fr(4, 12), '$%s$' % fr(5, 7), '$%s$' % fr(300, 1000)])),
 (3, r"Escribe todas las fracciones de denominador $9$ que son impropias pero menores que $2$. ¿Qué fracciones de denominador $6$ hay entre $2$ y $3$ (sin contarlos)?",
     r"Entre $%s$ y $%s$: \ $\res{%s}$. \ Entre $%s$ y $%s$: \ $\res{%s}$." % (fr(9, 9), fr(18, 9), lst(['%d/9' % k for k in range(10, 18)]), fr(12, 6), fr(18, 6), lst(['%d/6' % k for k in range(13, 18)]))),
]))

S.append(("Fracción de un número", [
 (1, r"Calcula:" + tasks(3, [r'$%s$ de $%s$' % (fr(a, b), n) for a, b, n in [(5, 6, 48), (4, 7, 490), (3, 5, 200), (7, 8, 32), (2, 5, 60), (3, 6, 180)]])
     + recorda(r"$%s$ de $40$: dividimos entre el denominador y multiplicamos por el numerador: \ $(40:5)\cdot3=24$." % fr(3, 5)),
     tasks(3, [r'$(%d:%d)\cdot%d=\res{%d}$' % (n, b, a, n // b * a) for a, b, n in [(5, 6, 48), (4, 7, 490), (3, 5, 200), (7, 8, 32), (2, 5, 60), (3, 6, 180)]])),
 (1, r"En una clase de 30 alumnos, $%s$ son chicos. ¿Cuántos chicos y cuántas chicas hay?" % fr(2, 5),
     r"Chicos: $(30:5)\cdot2=\res{12}$. \ Chicas: $30-12=\res{18}$."),
 (2, r"Un depósito de $2400$ litros está lleno hasta los $%s$. ¿Cuántos litros tiene? ¿Cuántos faltan para llenarlo?" % fr(3, 8),
     r"$(2400:8)\cdot3=\res{900\text{ L}}$. \ Faltan $2400-900=\res{1500\text{ L}}$."),
 (2, r"Calcula el número:" + tasks(2, [r"Los $%s$ de un número son $36$." % fr(3, 4), r"Los $%s$ de un número son $18$." % fr(2, 7)]),
     tasks(2, [r"$36:3=12$; \ $12\cdot4=\res{48}$", r"$18:2=9$; \ $9\cdot7=\res{63}$"])),
 (2, r"Pablo se ha gastado $%s$ de la paga y todavía le quedan $14$\,€. ¿Cuánto dinero tenía?" % fr(3, 5),
     r"Le quedan $%s$ de la paga, que son 14\,€: \ $14:2=7$; \ $7\cdot5=\res{35\text{\,€}}$." % fr(2, 5)),
 (3, r"Calcula $%s$ de $%s$ de $360$." % (fr(2, 3), fr(3, 4)),
     r"$%s$ de $360=270$; \ $%s$ de $270=\res{180}$." % (fr(3, 4), fr(2, 3))),
 (3, r"Van de excursión 84 alumnos: $%s$ son de 1\textsuperscript{o}, $%s$ de 2\textsuperscript{o} y el resto de 3\textsuperscript{o}. ¿Cuántos hay de cada curso?" % (fr(3, 7), fr(1, 4)),
     r"1\textsuperscript{o}: $(84:7)\cdot3=\res{36}$. \ 2\textsuperscript{o}: $84:4=\res{21}$. \ 3\textsuperscript{o}: $84-36-21=\res{27}$."),
]))

PCT = [(20, 180), (45, 80), (12, 350), (85, 1300), (50, 64), (25, 120)]
PF = [50, 25, 75, 20, 10, 40, 5, 35]
FP = [(1, 2), (3, 4), (2, 5), (7, 10), (9, 20), (3, 25)]
S.append(("Porcentajes y fracciones", [
 (1, r"Calcula:" + tasks(3, [r'$%d\,\%%$ de $%d$' % (p, n) for p, n in PCT])
     + recorda(r"$p\,\%%=%s$. \ El $p\,\%%$ de $N$ es $%s$." % (fr('p', 100), fr(r'p\cdot N', 100))),
     tasks(3, [r'$%s=\res{%s}$' % (fr(r'%d\cdot%d' % (p, n), 100), ftex(Fr(p * n, 100))) for p, n in PCT])),
 (1, r"Escribe cada porcentaje como fracción irreducible:" + tasks(4, [r'$%d\,\%%$' % p for p in PF]),
     tasks(4, [r'$%s=%s$' % (fr(p, 100), ftex(Fr(p, 100))) for p in PF])),
 (1, r"Expresa en porcentaje:" + tasks(6, ['$%s$' % fr(a, b) for a, b in FP]),
     tasks(3, [r'$%s=%s=\res{%d\,\%%}$' % (fr(a, b), fr(a * 100 // b, 100), a * 100 // b) for a, b in FP])),
 (2, r"Una chaqueta cuesta $80$\,€ y la rebajan un $25\,\%$. ¿Cuántos euros nos descuentan? ¿Cuánto pagamos?",
     r"$25\,\%%=%s$: \ descuento $80:4=\res{20\text{\,€}}$; \ pagamos $80-20=\res{60\text{\,€}}$." % fr(1, 4)),
 (2, r"En un instituto de 650 alumnos, el $52\,\%$ son chicas. ¿Cuántas chicas y cuántos chicos hay?",
     r"Chicas: $%s=\res{338}$. \ Chicos: $650-338=\res{312}$." % fr(r'52\cdot650', 100)),
 (3, r"En una provincia de $378\,000$ personas, el $7\,\%$ son de Marruecos, el $25\,\%$ del este de Europa, el $12\,\%$ de Alemania y el resto son de aquí. ¿Qué porcentaje son de aquí? ¿Cuántas personas hay de cada grupo?",
     r"De aquí: $100-7-25-12=\res{56\,\%}$. \ Personas: $\res{26\,460}$, \ $\res{94\,500}$, \ $\res{45\,360}$ \ y \ $\res{211\,680}$."),
 (3, r"En una clase de 25 alumnos, 8 han suspendido el examen. ¿Qué porcentaje ha aprobado?",
     r"Han aprobado $17$: \ $%s=%s=\res{68\,\%%}$." % (fr(17, 25), fr(68, 100))),
]))

AMP = [(1, 4), (2, 5), (5, 15), (7, 13), (11, 17), (1, 10)]
RED = [(4, 12, '2/6', '1/3'), (12, 20, '6/10', '3/5'), (66, 84, '33/42', '11/14'), (15, 45, '5/15', '1/3'), (50, 100, '25/50', '1/2')]
SIMP = [(4, 6), (4, 20), (3, 12), (2, 6), (35, 40), (75, 100), (4, 16), (14, 21), (10, 15), (25, 45), (13, 52), (33, 34), (705, 120), (170, 105), (256, 512)]
EQ11 = [(54, 24), (40, 88), (81, 36), (72, 32), (75, 185), (50, 110)]
S.append(("Fracciones equivalentes", [
 (1, r"Escribe, por amplificación, cuatro fracciones equivalentes a cada una:" + tasks(6, ['$%s$' % fr(a, b) for a, b in AMP])
     + recorda(r"\textbf{Amplificar}: multiplicar numerador y denominador por el mismo número. \textbf{Simplificar}: dividirlos entre un divisor común. La fracción \textbf{irreducible} se obtiene dividiendo entre el m.c.d."),
     tasks(2, ['$%s$' % '='.join([fr(a, b)] + [fr(a * k, b * k) for k in range(2, 6)]) for a, b in AMP])),
 (1, r"Halla dos fracciones simplificadas de cada una:" + tasks(5, ['$%s$' % fr(a, b) for a, b, _, _ in RED]),
     tasks(3, ['$%s=%s=%s$' % (fr(a, b), fr(*x.split('/')), fr(*y.split('/'))) for a, b, x, y in RED]) + r"\par (Hay otras respuestas posibles.)"),
 (1, r"¿Son irreducibles?" + tasks(3, ['$%s$' % fr(a, b) for a, b in [(25, 35), (5, 7), (98, 49)]]),
     tasks(3, [r"No: $%s$" % fr(5, 7), r"Sí: $\text{m.c.d.}(5,7)=1$", r"No: $%s=2$" % fr(2, 1)])),
 (2, r"Simplifica hasta llegar a la fracción irreducible:" + tasks(5, ['$%s$' % fr(a, b) for a, b in SIMP]),
     tasks(5, ['$%s=\\res{%s}$' % (fr(a, b), irr(a, b)) for a, b in SIMP])),
 (2, r"Calcula la fracción irreducible de cada una e indica cuáles son equivalentes entre sí:" + tasks(3, ['$%s$' % fr(a, b) for a, b in EQ11]),
     tasks(3, ['$%s=%s$' % (fr(a, b), irr(a, b)) for a, b in EQ11]) + r"\par Equivalentes: $%s$, $%s$ y $%s$ (todas valen $%s$); \ $%s$ y $%s$ (valen $%s$)." % (fr(54, 24), fr(81, 36), fr(72, 32), fr(9, 4), fr(40, 88), fr(50, 110), fr(5, 11))),
 (3, r"Halla una fracción equivalente a $%s$ que tenga denominador $16$, y una equivalente a $%s$ que tenga numerador $80$." % (fr(15, 24), fr(5, 8)),
     r"$%s=%s=\res{%s}$ \qquad $%s=%s=\res{%s}$" % (fr(15, 24), fr(5, 8), fr(10, 16), fr(5, 8), fr(r'5\cdot16', r'8\cdot16'), fr(80, 128))),
 (3, r"Escribe todas las fracciones equivalentes a $%s$ que tienen el denominador entre $20$ y $30$." % fr(2, 3),
     r"$\res{%s}$" % lst(['14/21', '16/24', '18/27', '20/30'])),
]))

CHK = [(8, 32, 3, 12), (6, 15, 26, 34), (7, 23, 14, 46), (1, 2, 15, 30), (68, 52, 17, 13), (3, 29, 33, 67)]
XS = [('3/14', 'x/42', 9), ('6/8', '24/x', 32), ('x/5', '12/20', 3), ('14/3', 'x/21', 98), ('5/11', '15/x', 33)]
def xf(s): a, b = s.split('/'); return fr(a, b)
S.append(("Comprobar si dos fracciones son equivalentes", [
 (1, r"Comprueba si son equivalentes:" + tasks(3, [r'$%s$ y $%s$' % (fr(a, b), fr(c, d)) for a, b, c, d in CHK])
     + recorda(r"$%s=%s$ \ si y solo si \ $a\cdot d=b\cdot c$ \ (productos cruzados)." % (fr('a', 'b'), fr('c', 'd'))),
     tasks(2, [r'$%d\cdot%d=%d$, \ $%d\cdot%d=%d$: \ \res{\text{%s}}' % (a, d, a * d, b, c, b * c, 'sí' if a * d == b * c else 'no') for a, b, c, d in CHK])),
 (1, r"Calcula el valor de $x$ para que las fracciones sean equivalentes:" + tasks(5, [r'$%s=%s$' % (xf(p), xf(q)) for p, q, _ in XS]),
     tasks(5, [r'$x=\res{%d}$' % x for _, _, x in XS])),
 (2, r"Completa para que sean equivalentes: \quad $%s=%s=%s=%s$" % (fr(2, 5), fr(r'\square', 20), fr(12, r'\square'), fr(r'\square', 45)),
     r"$%s=%s=%s=%s$" % (fr(2, 5), fr(r'\res{8}', 20), fr(12, r'\res{30}'), fr(r'\res{18}', 45))),
 (2, r"¿Cuál de estas fracciones no es equivalente a las demás? \quad $%s$" % lst(['6/9', '10/15', '14/20', '16/24']),
     r"$\res{%s}$ ($=%s$); \ las demás valen $%s$." % (fr(14, 20), fr(7, 10), fr(2, 3))),
 (3, r"Halla $x$ e $y$ para que \ $%s=%s=%s$." % (fr('x', 12), fr(15, 20), fr(9, 'y')),
     r"$%s=%s$: \ $x=\res{9}$, \ $y=\res{12}$." % (fr(15, 20), fr(3, 4))),
 (3, r"Halla una fracción equivalente a $%s$ que tenga el denominador $24$ unidades mayor que el numerador." % fr(3, 5),
     r"En $%s$ la diferencia es $2$; amplificamos por $24:2=12$: \ $\res{%s}$." % (fr(3, 5), fr(36, 60))),
]))

def cd(fs):
    ds = [Fr(f).denominator if '/' not in f else int(f.split('/')[1]) for f in fs]
    m = 1
    for d in ds: m = m * d // math.gcd(m, d)
    out = []
    for f, d in zip(fs, ds):
        n = int(f.split('/')[0]) if '/' in f else int(f)
        out.append(fr(n * m // d, m))
    return m, ',\\ '.join(out)
CD1 = [['1/5', '3/7'], ['2/9', '1/6'], ['3/4', '3/8'], ['2/7', '1/4'], ['5/21', '3/2'], ['3/5', '1/10'], ['1/4', '1/6'], ['3/7', '5']]
CD2 = [['7/24', '3/16'], ['1/2', '2/3', '5/8'], ['7/2', '6/15', '3/10'], ['5/8', '1/2', '7/12'], ['4/7', '1/3', '5/14'], ['3/18', '4/30', '7/36'], ['6/7', '2/14', '12/28'], ['5/3', '5/12', '3/4', '9/20']]
S.append(("Reducción a común denominador", [
 (1, r"Reduce a común denominador:" + tasks(4, ['$%s$' % lst(f) for f in CD1])
     + recorda(r"Nuevo denominador: el \textbf{m.c.m.} de los denominadores. Para cada fracción, dividimos el m.c.m. entre su denominador y multiplicamos el numerador por el resultado."),
     tasks(2, ['$%s$' % cd(f)[1] for f in CD1])),
 (2, r"Reduce a común denominador:" + tasks(4, ['$%s$' % lst(f) for f in CD2]),
     tasks(2, [r'$\text{m.c.m.}=%d$: \ $%s$' % cd(f) for f in CD2])),
 (2, r"Escribe las fracciones $%s$ con denominador $36$." % lst(['5/6', '7/12', '4/9']),
     r"$\res{%s}$" % lst(['30/36', '21/36', '16/36'])),
 (3, r"Simplifica primero y después reduce a común denominador con el denominador más pequeño posible: \ $%s$." % lst(['6/9', '10/15', '9/12']),
     r"$%s$ \ $\to$ \ $\text{m.c.m.}(3,3,4)=12$: \ $\res{%s}$." % (lst(['2/3', '2/3', '3/4']), lst(['8/12', '8/12', '9/12']))),
]))

def cmpsym(a, b):
    x, y = Fr(*map(int, a.split('/'))), Fr(*map(int, b.split('/')))
    return '<' if x < y else '>' if x > y else '='
CMP = [('9/5', '9/8'), ('6/11', '10/11'), ('3/7', '3/4'), ('4/8', '2/16'), ('2/5', '5/6'), ('1/3', '3/7'), ('8/9', '11/12'), ('3/4', '24/32')]
def order(fs):
    v = sorted(fs, key=lambda f: Fr(*map(int, f.split('/'))))
    s = xf(v[0])
    for p, q in zip(v, v[1:]):
        s += ('=' if Fr(*map(int, p.split('/'))) == Fr(*map(int, q.split('/'))) else '<') + xf(q)
    return s
ORD1 = [['3/5', '2/7', '11/2'], ['4/9', '5/6', '2/3'], ['5/4', '2/6', '1/10'], ['18/3', '14/7', '23/21'], ['2/12', '4/15', '3/24'], ['12/14', '6/7', '3/28']]
ORD2 = [['4/5', '2/8', '3/10', '7/20'], ['5/2', '2/3', '4/7', '5/4'], ['7/12', '2/6', '1/4', '3/2']]
S.append(("Comparar y ordenar fracciones", [
 (1, r"Escribe una fracción mayor y una menor que la dada:" + tasks(3, ['$%s$' % fr(*x) for x in [(5, 7), (4, 9), (3, 13)]]),
     tasks(3, [r'$%s<%s<%s$' % (fr(4, 7), fr(5, 7), fr(6, 7)), r'$%s<%s<%s$' % (fr(3, 9), fr(4, 9), fr(5, 9)), r'$%s<%s<%s$' % (fr(2, 13), fr(3, 13), fr(4, 13))]) + r"\par (Hay muchas respuestas posibles.)"),
 (1, r"Compara (escribe $<$, $>$ o $=$):" + tasks(4, [r'$%s\ \square\ %s$' % (xf(a), xf(b)) for a, b in CMP])
     + recorda(r"Mismo denominador: es mayor la de numerador mayor. Mismo numerador: es mayor la de denominador menor. Si no, reduce a común denominador."),
     tasks(4, [r'$%s\ \res{%s}\ %s$' % (xf(a), cmpsym(a, b), xf(b)) for a, b in CMP])),
 (2, r"Ordena de menor a mayor:" + tasks(3, ['$%s$' % lst(f) for f in ORD1]),
     tasks(3, ['$%s$' % order(f) for f in ORD1])),
 (2, r"Ordena de menor a mayor:" + tasks(3, ['$%s$' % lst(f) for f in ORD2]),
     tasks(2, ['$%s$' % order(f) for f in ORD2])),
 (2, r"Marca en la recta las fracciones $%s$.\par\smallskip{\centering %s\par}" % (lst(['1/4', '3/4', '5/4', '3/2']), tz_line(2, 4)),
     r"{\centering %s\par}" % tz_line(2, 4, [(1, 4), (3, 4), (5, 4), (3, 2)])),
 (3, r"Escribe una fracción comprendida entre $%s$ y $%s$, y otra entre $%s$ y $%s$." % (fr(2, 5), fr(3, 5), fr(1, 3), fr(1, 2)),
     r"$%s=%s$ y $%s=%s$: \ $\res{%s}$. \qquad $%s=%s$ y $%s=%s$: \ $\res{%s}$." % (fr(2, 5), fr(4, 10), fr(3, 5), fr(6, 10), fr(5, 10), fr(1, 3), fr(4, 12), fr(1, 2), fr(6, 12), fr(5, 12))),
 (3, r"Tres amigos leen el mismo libro: Ana ha leído $%s$, Gabriel $%s$ y Clara $%s$. ¿Quién ha leído más? Ordénalos." % (fr(3, 4), fr(5, 8), fr(7, 10)),
     r"$\text{m.c.m.}=40$: \ $%s$. \ Ha leído más \res{\text{Ana}}, después Clara y después Gabriel." % lst(['30/40', '25/40', '28/40'])),
]))

SR1 = ['4/7+8/7', '2/3+1/5', '5/2-1/8', '3/6-4/12', '5/8+1/5', '14/15-2/3']
SR2 = ['12/15+8/9', '7/12-3/10', '7/6+8/12', '18/5-3/10', '5/3-9/24', '35/36+2/9']
SR3 = ['3/4+6/8', '4+25/9', '25/8-2', '3/5+1', '5-3/25', '13/6+2/7']
SR4 = ['4/5+2/7-1/2', '6/8+4/3-8/12', '3/2+6/7-2/4', '6-1/2-4/12', '2/3+1/5-1/6', '4/3+1/6-2/7']
SR5 = ['2/10+5/60-1/30', '12/5+2-1/25', '6/9+1/3-2/6', '10/3-2/6-4/5+1/2', '4-1/2+1/3+2', '7/9+1/3-2/5']
S.append(("Sumas y restas", [
 (1, r"Calcula y simplifica el resultado:" + tasks(3, [op(e) for e in SR1])
     + recorda(r"Si los denominadores son diferentes, primero reducimos a \textbf{común denominador}. \textbf{Nunca} sumamos los denominadores: $%s+%s=%s+%s=%s$." % (fr(1, 2), fr(1, 3), fr(3, 6), fr(2, 6), fr(5, 6))),
     tasks(3, [ops(e) for e in SR1])),
 (1, r"Calcula y simplifica (los números naturales tienen denominador 1):" + tasks(3, [op(e) for e in SR3]),
     tasks(3, [ops(e) for e in SR3])),
 (2, r"Calcula y simplifica el resultado:" + tasks(3, [op(e) for e in SR2]),
     tasks(3, [ops(e) for e in SR2])),
 (2, r"Calcula y simplifica:" + tasks(2, [op(e) for e in SR4]),
     tasks(2, [ops(e) for e in SR4])),
 (3, r"Calcula y simplifica:" + tasks(2, [op(e) for e in SR5]),
     tasks(2, [ops(e) for e in SR5])),
 (3, r"Llenamos una piscina en tres días: el primer día, $%s$; el segundo, $%s$, y el tercero, $%s$. ¿Qué fracción de la piscina falta por llenar?" % (fr(1, 4), fr(2, 5), fr(1, 6)),
     r"$%s+%s+%s=%s$, \ falta $1-%s=\res{%s}$." % (fr(1, 4), fr(2, 5), fr(1, 6), ftex(val('1/4+2/5+1/6')), ftex(val('1/4+2/5+1/6')), ftex(1 - val('1/4+2/5+1/6')))),
]))

MU = ['6/4*2/5', '3/2*2/3', '2*5/6', '3/2*4/7*3', '3/4*10/2*1/6', '4/3*2/8*6/2']
INV = [('2/5', '5/3'), ('4/3', '12/16'), ('7/9', '9/7'), ('2/4', '4/2'), ('5/6', '36/30'), ('12/13', '26/12')]
DIV = ['4/3:5/6', '5/4:2', '4/8:6/3', '2/6:5/4:1/3', '3/4:12/5:2/5', '6:2/3:1/5']
MD = ['3/4*5/8:2/5', '5/4:1/3*6/5', '5/12*3/2:1/6', '6/5:7/4*2/10']
FF = [('2/3', '3/5'), ('4/10', '1/2'), ('4/3', '6/2'), ('3/5', '5/7')]
S.append(("Multiplicación y división", [
 (1, r"Calcula y simplifica:" + tasks(3, [op(e) for e in MU])
     + recorda(r"$%s\cdot%s=%s$. \qquad $%s:%s=%s$ \ (productos cruzados). \ La \textbf{inversa} de $%s$ es $%s$." % (fr('a', 'b'), fr('c', 'd'), fr(r'a\cdot c', r'b\cdot d'), fr('a', 'b'), fr('c', 'd'), fr(r'a\cdot d', r'b\cdot c'), fr('a', 'b'), fr('b', 'a'))),
     tasks(3, [ops(e) for e in MU]) + r"\par En el b) y el f) el producto es 1: las fracciones son \textbf{inversas}."),
 (1, r"Calcula (la fracción de una fracción es un producto):" + tasks(4, [r'$%s$ de $%s$' % (xf(a), xf(b)) for a, b in FF]),
     tasks(4, [r'$\res{%s}$' % ftex(val(a + '*' + b)) for a, b in FF])),
 (1, r"¿Qué parejas son fracciones inversas? (Su producto tiene que ser 1.)" + tasks(3, [r'$%s,\ %s$' % (xf(a), xf(b)) for a, b in INV]),
     tasks(3, [r'$%s\cdot%s=%s$: \ \res{\text{%s}}' % (xf(a), xf(b), ftex(val(a + '*' + b)), 'sí' if val(a + '*' + b) == 1 else 'no') for a, b in INV])),
 (1, r"Escribe la inversa de:" + tasks(4, ['$%s$' % x for x in [fr(4, 13), fr(3, 7), fr(15, 8), '6']]),
     tasks(4, ['$%s$' % x for x in [fr(13, 4), fr(7, 3), fr(8, 15), fr(1, 6)]])),
 (2, r"Calcula y simplifica (con divisiones seguidas, de izquierda a derecha):" + tasks(3, [op(e) for e in DIV]),
     tasks(3, [ops(e) for e in DIV])),
 (2, r"Calcula y simplifica:" + tasks(2, [op(e) for e in MD]),
     tasks(2, [ops(e) for e in MD])),
 (3, r"Con $12$ litros de zumo, ¿cuántas botellas de $%s$ de litro podemos llenar? ¿Y qué fracción hay que multiplicar por $%s$ para obtener $%s$?" % (fr(3, 4), fr(3, 4), fr(9, 10)),
     r"$12:%s=%s=\res{16}$ botellas. \qquad $%s:%s=%s=\res{%s}$." % (fr(3, 4), fr(48, 3), fr(9, 10), fr(3, 4), fr(36, 30), fr(6, 5))),
]))

CB1 = ['5/2+1/3*4/5', '21/4-2/5:4/3', '4/3:2/6+1/3*5/4', '4/3*(2/5+1/3)', '(2/5+1):8/3', '(5/4+1)*6/7']
CB2 = ['(2/5+3/7)*1/2-4/10', '(5/4+2/3+1/12)*5/4-1', '5/4:(6/4-1)+2/5', '4/3-(1/2+2/7)+4/5*2/4']
CB3 = ['(1/4+2/3-1/12)*3+(3/2-5/4):1/2', '4*(2/3+4/6-1)+2/3', '(3/2+1/7)*(5/3-7/15)', '12/10:5/4+1/2*13/5', '(4/3+2/5*1/3):4/12', '3/2:1/4*4/20+3/2*7/5']
CB4 = ['(5/4+2/3-1)*3/5+(2/5+4/3)*2', '3/8+4/5*1/3+(2/6-1/4)*3']
S.append(("Operaciones combinadas", [
 (2, r"Calcula y simplifica:" + tasks(2, [op(e) for e in CB1])
     + recorda(r"Orden: primero, \textbf{paréntesis}; después, \textbf{multiplicaciones y divisiones} (de izquierda a derecha); por último, \textbf{sumas y restas} (de izquierda a derecha)."),
     tasks(2, [ops(e) for e in CB1])),
 (2, r"Calcula y simplifica:" + tasks(2, [op(e) for e in CB2]),
     tasks(2, [ops(e) for e in CB2])),
 (3, r"Calcula y simplifica:" + tasks(2, [op(e) for e in CB3]),
     tasks(2, [ops(e) for e in CB3])),
 (3, r"Calcula y simplifica:" + tasks(1, [op(e) for e in CB4]),
     tasks(1, [ops(e) for e in CB4])),
]))

S.append(("Problemas con fracciones", [
 (1, r"De una cena, Juan se ha comido $%s$, Elena $%s$ y Maite $%s$." % (fr(1, 7), fr(2, 5), fr(1, 8)) + tasks(1, ["¿Cuánto se han comido entre los tres?", "¿Cuánto ha sobrado?", "¿Quién ha comido más y quién menos?"])
     + recorda(r"Lee el enunciado dos veces, haz un \textbf{dibujo} (una barra que representa el total) y, al final, \textbf{comprueba} que el resultado tiene sentido."),
     tasks(1, [r"$\text{m.c.m.}=280$: \ $%s=\res{%s}$" % (lst(['40/280', '112/280', '35/280']).replace(',\\ ', '+'), fr(187, 280)), r"$1-%s=\res{%s}$" % (fr(187, 280), fr(93, 280)), r"Más: \res{\text{Elena}} ($%s$); \ menos: \res{\text{Maite}} ($%s$)." % (fr(112, 280), fr(35, 280))])),
 (1, r"De un pastel de 24 porciones nos hemos comido $%s$. ¿Cuántas porciones quedan?" % fr(5, 8),
     r"Nos hemos comido $(24:8)\cdot5=15$: \ quedan $\res{9}$ porciones."),
 (2, r"De una pizza, Carlos se come $%s$, Miguel $%s$ y Lorena $%s$." % (fr(3, 6), fr(3, 21), fr(4, 14)) + tasks(1, ["¿Qué fracción de la pizza ha sobrado?", r"Llega Marta con otra pizza igual. Como los demás ya están llenos, ella se come lo que había sobrado y $%s$ de su pizza. ¿Cuánta pizza se ha comido ella?" % fr(3, 5)]),
     tasks(1, [r"$%s+%s+%s=%s$: \ sobra $\res{%s}$." % (fr(1, 2), fr(1, 7), fr(2, 7), fr(13, 14), fr(1, 14)), r"$%s+%s=%s+%s=\res{%s}$ de pizza." % (fr(1, 14), fr(3, 5), fr(5, 70), fr(42, 70), fr(47, 70))])),
 (2, r"En un pueblo de 5250 habitantes, la mitad tienen más de 65 años y $%s$ tienen menos de 18." % fr(1, 5) + tasks(1, ["¿Qué fracción representan los que tienen entre 18 y 65 años?", "¿Cuántos habitantes hay en cada franja de edad?"]),
     tasks(1, [r"$1-%s-%s=\res{%s}$" % (fr(1, 2), fr(1, 5), fr(3, 10)), r"Más de 65: $\res{2625}$; \ menos de 18: $\res{1050}$; \ entre 18 y 65: $\res{1575}$."])),
 (2, r"Un bidón de 60 litros está lleno. Primero se gastan $%s$ y después $%s$ de lo que quedaba. Finalmente, el bidón vuelca y se derrama la mitad de lo que hay. ¿Cuántos litros quedan al final?" % (fr(2, 4), fr(1, 3)),
     r"Se gastan 30 L (quedan 30); \ después $%s$ de 30 $=10$ L (quedan 20); \ se derrama la mitad: quedan $\res{10\text{ L}}$." % fr(1, 3)),
 (3, r"Una familia gasta $%s$ del sueldo en la hipoteca, $%s$ en comida, $%s$ en el coche y el resto en otros gastos. ¿Qué fracción representan los otros gastos?" % (fr(2, 6), fr(1, 5), fr(2, 7)),
     r"$%s+%s+%s=%s$ \ $\Rightarrow$ \ $1-%s=\res{%s}$." % (fr(35, 105), fr(21, 105), fr(30, 105), fr(86, 105), fr(86, 105), fr(19, 105))),
 (3, r"Una familia ingresa $5400$\,€ al mes. Gasta $%s$ en la hipoteca, $%s$ en comida y $%s$ en el coche." % (fr(2, 6), fr(1, 5), fr(1, 9)) + tasks(1, ["¿Cuánto dinero gasta en cada cosa y cuánto le queda para otros gastos?", "¿Qué fracción del total representa el dinero que sobra?"]),
     tasks(1, [r"Hipoteca $\res{1800\text{\,€}}$, comida $\res{1080\text{\,€}}$, coche $\res{600\text{\,€}}$; \ quedan $\res{1920\text{\,€}}$.", r"$%s=\res{%s}$" % (fr(1920, 5400), fr(16, 45))])),
 (3, r"Un depósito está lleno hasta los $%s$. Gastamos $%s$ de lo que hay y quedan 50 litros. ¿Qué capacidad tiene el depósito?" % (fr(3, 4), fr(2, 3)),
     r"Queda $%s$ de $%s$, es decir, $%s$ del depósito, que son 50 L: \ capacidad $50\cdot4=\res{200\text{ L}}$." % (fr(1, 3), fr(3, 4), fr(1, 4))),
]))

# comprovacions dels resultats escrits a mà
assert val('1/7+2/5+1/8') == Fr(187, 280) and val('1/2+1/7+2/7') == Fr(13, 14) and val('1/14+3/5') == Fr(47, 70)
assert val('1-1/2-1/5') == Fr(3, 10) and val('1-(2/6+1/5+2/7)') == Fr(19, 105) and val('1-(2/6+1/5+1/9)') == Fr(16, 45)
assert Fr(1920, 5400) == Fr(16, 45) and 5400 - 1800 - 1080 - 600 == 1920

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 4: Fracciones' % t, capcalera='%s · Unidad 4: Fracciones' % t,
                 pdfkeywords='fracciones, fracción de un número, porcentajes, fracciones equivalentes, común denominador, comparar fracciones, operaciones con fracciones, problemas',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 4' if sol else 'Ficha de ejercicios · Unidad 4') + '}{Fracciones}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad. Recuerda que los resultados se tienen que dar siempre en forma de fracción irreducible."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y da los resultados en forma de fracción irreducible. Las figuras y las rectas se pueden completar directamente en la ficha. Haz los cálculos sin calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't4-fitxa-solucions-es.tex' if sol else 't4-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
