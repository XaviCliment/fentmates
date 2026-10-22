# Genera t4-fitxa-exercicis.tex i t4-fitxa-solucions.tex (1r ESO, Unitat 4: Fraccions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les solucions de les operacions es calculen amb fraccions exactes (vegeu op/ops).
import os, re, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))

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
S.append(("El concepte de fracció", [
 (1, r"Quina fracció representa la part pintada de cada figura?" + tasks(3, [f for f, _ in FIG1])
     + recorda(r"El \textbf{denominador} indica en quantes parts \textbf{iguals} dividim la unitat; el \textbf{numerador}, quantes n'agafem."),
     tasks(6, ['$%s$' % fr(*a.split('/')) for _, a in FIG1])),
 (1, r"Indica el numerador i el denominador de cada fracció i escriu com es llegeix:" + tasks(4, ['$%s$' % fr(3, 5), '$%s$' % fr(4, 6), '$%s$' % fr(12, 15), '$%s$' % fr(4, 3)]),
     tasks(2, [r"num.\ 3, den.\ 5: tres cinquens", r"num.\ 4, den.\ 6: quatre sisens", r"num.\ 12, den.\ 15: dotze quinzens", r"num.\ 4, den.\ 3: quatre terços"])),
 (1, r"Pinta en cada figura la fracció indicada:" + tasks(3, [r'$%s$\ \ %s' % (fr(3, 5), tz_bar(5, 0, 3.5)), r'$%s$\ \ %s' % (fr(5, 8), tz_rect(2, 4, 0)), r'$%s$\ \ %s' % (fr(2, 3), tz_circ(3, 0, 0.65))]),
     tasks(3, [r'$%s$\ \ %s' % (fr(3, 5), tz_bar(5, 3, 3.5)), r'$%s$\ \ %s' % (fr(5, 8), tz_rect(2, 4, 5)), r'$%s$\ \ %s' % (fr(2, 3), tz_circ(3, 2, 0.65))])),
 (1, r"Representa en la recta numèrica les fraccions $%s$ i $%s$.\par\smallskip{\centering %s\par}" % (fr(6, 10), fr(7, 4), tz_line(2)),
     r"Dividim cada unitat en 10 parts per a $%s$ i en 4 per a $%s=1+%s$:\par\smallskip{\centering %s\par}" % (fr(6, 10), fr(7, 4), fr(3, 4), tz_line(2, 4, [(6, 10), (7, 4)]))),
 (2, r"Classifica les fraccions en pròpies, impròpies o iguals a la unitat. Escriu les impròpies com a unitats senceres més una fracció pròpia." + tasks(6, ['$%s$' % fr(*x) for x in [(7, 3), (5, 8), (9, 9), (13, 4), (2, 11), (20, 6)]]),
     tasks(3, [r"Impròpia: $2+%s$" % fr(1, 3), r"Pròpia", r"Igual a 1", r"Impròpia: $3+%s$" % fr(1, 4), r"Pròpia", r"Impròpia: $3+%s$" % fr(2, 6)])),
 (2, r"Quina fracció representa?" + tasks(2, [r"15 minuts d'una hora", r"4 mesos d'un any", r"5 dies d'una setmana", r"300 grams d'1 kg"]),
     tasks(4, ['$%s$' % fr(15, 60), '$%s$' % fr(4, 12), '$%s$' % fr(5, 7), '$%s$' % fr(300, 1000)])),
 (3, r"Escriu totes les fraccions de denominador $9$ que són impròpies però menors que $2$. Quines fraccions de denominador $6$ hi ha entre $2$ i $3$ (sense comptar-los)?",
     r"Entre $%s$ i $%s$: \ $\res{%s}$. \ Entre $%s$ i $%s$: \ $\res{%s}$." % (fr(9, 9), fr(18, 9), lst(['%d/9' % k for k in range(10, 18)]), fr(12, 6), fr(18, 6), lst(['%d/6' % k for k in range(13, 18)]))),
]))

S.append(("Fracció d'un nombre", [
 (1, r"Calcula:" + tasks(3, [r'$%s$ de $%s$' % (fr(a, b), n) for a, b, n in [(5, 6, 48), (4, 7, 490), (3, 5, 200), (7, 8, 32), (2, 5, 60), (3, 6, 180)]])
     + recorda(r"$%s$ de $40$: dividim entre el denominador i multipliquem pel numerador: \ $(40:5)\cdot3=24$." % fr(3, 5)),
     tasks(3, [r'$(%d:%d)\cdot%d=\res{%d}$' % (n, b, a, n // b * a) for a, b, n in [(5, 6, 48), (4, 7, 490), (3, 5, 200), (7, 8, 32), (2, 5, 60), (3, 6, 180)]])),
 (1, r"En una classe de 30 alumnes, $%s$ són xics. Quants xics i quantes xiques hi ha?" % fr(2, 5),
     r"Xics: $(30:5)\cdot2=\res{12}$. \ Xiques: $30-12=\res{18}$."),
 (2, r"Un dipòsit de $2400$ litres està ple fins als $%s$. Quants litres té? Quants en falten per a omplir-lo?" % fr(3, 8),
     r"$(2400:8)\cdot3=\res{900\text{ L}}$. \ Falten $2400-900=\res{1500\text{ L}}$."),
 (2, r"Calcula el nombre:" + tasks(2, [r"Els $%s$ d'un nombre són $36$." % fr(3, 4), r"Els $%s$ d'un nombre són $18$." % fr(2, 7)]),
     tasks(2, [r"$36:3=12$; \ $12\cdot4=\res{48}$", r"$18:2=9$; \ $9\cdot7=\res{63}$"])),
 (2, r"En Pau s'ha gastat $%s$ de la paga i encara li queden $14$\,€. Quants diners tenia?" % fr(3, 5),
     r"Li queden $%s$ de la paga, que són 14\,€: \ $14:2=7$; \ $7\cdot5=\res{35\text{\,€}}$." % fr(2, 5)),
 (3, r"Calcula $%s$ de $%s$ de $360$." % (fr(2, 3), fr(3, 4)),
     r"$%s$ de $360=270$; \ $%s$ de $270=\res{180}$." % (fr(3, 4), fr(2, 3))),
 (3, r"Van d'excursió 84 alumnes: $%s$ són de 1r, $%s$ de 2n i la resta de 3r. Quants n'hi ha de cada curs?" % (fr(3, 7), fr(1, 4)),
     r"1r: $(84:7)\cdot3=\res{36}$. \ 2n: $84:4=\res{21}$. \ 3r: $84-36-21=\res{27}$."),
]))

PCT = [(20, 180), (45, 80), (12, 350), (85, 1300), (50, 64), (25, 120)]
PF = [50, 25, 75, 20, 10, 40, 5, 35]
FP = [(1, 2), (3, 4), (2, 5), (7, 10), (9, 20), (3, 25)]
S.append(("Percentatges i fraccions", [
 (1, r"Calcula:" + tasks(3, [r'$%d\,\%%$ de $%d$' % (p, n) for p, n in PCT])
     + recorda(r"$p\,\%%=%s$. \ El $p\,\%%$ de $N$ és $%s$." % (fr('p', 100), fr(r'p\cdot N', 100))),
     tasks(3, [r'$%s=\res{%s}$' % (fr(r'%d\cdot%d' % (p, n), 100), ftex(Fr(p * n, 100))) for p, n in PCT])),
 (1, r"Escriu cada percentatge com a fracció irreductible:" + tasks(4, [r'$%d\,\%%$' % p for p in PF]),
     tasks(4, [r'$%s=%s$' % (fr(p, 100), ftex(Fr(p, 100))) for p in PF])),
 (1, r"Expressa en percentatge:" + tasks(6, ['$%s$' % fr(a, b) for a, b in FP]),
     tasks(3, [r'$%s=%s=\res{%d\,\%%}$' % (fr(a, b), fr(a * 100 // b, 100), a * 100 // b) for a, b in FP])),
 (2, r"Una jaqueta costa $80$\,€ i la rebaixen un $25\,\%$. Quants euros ens descompten? Quant paguem?",
     r"$25\,\%%=%s$: \ descompte $80:4=\res{20\text{\,€}}$; \ paguem $80-20=\res{60\text{\,€}}$." % fr(1, 4)),
 (2, r"En un institut de 650 alumnes, el $52\,\%$ són xiques. Quantes xiques i quants xics hi ha?",
     r"Xiques: $%s=\res{338}$. \ Xics: $650-338=\res{312}$." % fr(r'52\cdot650', 100)),
 (3, r"En una província de $378\,000$ persones, el $7\,\%$ són del Marroc, el $25\,\%$ de l'est d'Europa, el $12\,\%$ d'Alemanya i la resta són d'ací. Quin percentatge són d'ací? Quantes persones hi ha de cada grup?",
     r"D'ací: $100-7-25-12=\res{56\,\%}$. \ Persones: $\res{26\,460}$, \ $\res{94\,500}$, \ $\res{45\,360}$ \ i \ $\res{211\,680}$."),
 (3, r"En una classe de 25 alumnes, 8 han suspés l'examen. Quin percentatge ha aprovat?",
     r"Han aprovat $17$: \ $%s=%s=\res{68\,\%%}$." % (fr(17, 25), fr(68, 100))),
]))

AMP = [(1, 4), (2, 5), (5, 15), (7, 13), (11, 17), (1, 10)]
RED = [(4, 12, '2/6', '1/3'), (12, 20, '6/10', '3/5'), (66, 84, '33/42', '11/14'), (15, 45, '5/15', '1/3'), (50, 100, '25/50', '1/2')]
SIMP = [(4, 6), (4, 20), (3, 12), (2, 6), (35, 40), (75, 100), (4, 16), (14, 21), (10, 15), (25, 45), (13, 52), (33, 34), (705, 120), (170, 105), (256, 512)]
EQ11 = [(54, 24), (40, 88), (81, 36), (72, 32), (75, 185), (50, 110)]
S.append(("Fraccions equivalents", [
 (1, r"Escriu, per amplificació, quatre fraccions equivalents a cadascuna:" + tasks(6, ['$%s$' % fr(a, b) for a, b in AMP])
     + recorda(r"\textbf{Amplificar}: multiplicar numerador i denominador pel mateix nombre. \textbf{Simplificar}: dividir-los entre un divisor comú. La fracció \textbf{irreductible} s'obté dividint entre el MCD."),
     tasks(2, ['$%s$' % '='.join([fr(a, b)] + [fr(a * k, b * k) for k in range(2, 6)]) for a, b in AMP])),
 (1, r"Troba dues fraccions simplificades de cadascuna:" + tasks(5, ['$%s$' % fr(a, b) for a, b, _, _ in RED]),
     tasks(3, ['$%s=%s=%s$' % (fr(a, b), fr(*x.split('/')), fr(*y.split('/'))) for a, b, x, y in RED]) + r"\par (Hi ha altres respostes possibles.)"),
 (1, r"Són irreductibles?" + tasks(3, ['$%s$' % fr(a, b) for a, b in [(25, 35), (5, 7), (98, 49)]]),
     tasks(3, [r"No: $%s$" % fr(5, 7), r"Sí: $\text{MCD}(5,7)=1$", r"No: $%s=2$" % fr(2, 1)])),
 (2, r"Simplifica fins a arribar a la fracció irreductible:" + tasks(5, ['$%s$' % fr(a, b) for a, b in SIMP]),
     tasks(5, ['$%s=\\res{%s}$' % (fr(a, b), irr(a, b)) for a, b in SIMP])),
 (2, r"Calcula la fracció irreductible de cadascuna i indica quines són equivalents entre si:" + tasks(3, ['$%s$' % fr(a, b) for a, b in EQ11]),
     tasks(3, ['$%s=%s$' % (fr(a, b), irr(a, b)) for a, b in EQ11]) + r"\par Equivalents: $%s$, $%s$ i $%s$ (totes valen $%s$); \ $%s$ i $%s$ (valen $%s$)." % (fr(54, 24), fr(81, 36), fr(72, 32), fr(9, 4), fr(40, 88), fr(50, 110), fr(5, 11))),
 (3, r"Troba una fracció equivalent a $%s$ que tinga denominador $16$, i una d'equivalent a $%s$ que tinga numerador $80$." % (fr(15, 24), fr(5, 8)),
     r"$%s=%s=\res{%s}$ \qquad $%s=%s=\res{%s}$" % (fr(15, 24), fr(5, 8), fr(10, 16), fr(5, 8), fr(r'5\cdot16', r'8\cdot16'), fr(80, 128))),
 (3, r"Escriu totes les fraccions equivalents a $%s$ que tenen el denominador entre $20$ i $30$." % fr(2, 3),
     r"$\res{%s}$" % lst(['14/21', '16/24', '18/27', '20/30'])),
]))

CHK = [(8, 32, 3, 12), (6, 15, 26, 34), (7, 23, 14, 46), (1, 2, 15, 30), (68, 52, 17, 13), (3, 29, 33, 67)]
XS = [('3/14', 'x/42', 9), ('6/8', '24/x', 32), ('x/5', '12/20', 3), ('14/3', 'x/21', 98), ('5/11', '15/x', 33)]
def xf(s): a, b = s.split('/'); return fr(a, b)
S.append(("Comprovar si dues fraccions són equivalents", [
 (1, r"Comprova si són equivalents:" + tasks(3, [r'$%s$ i $%s$' % (fr(a, b), fr(c, d)) for a, b, c, d in CHK])
     + recorda(r"$%s=%s$ \ si i només si \ $a\cdot d=b\cdot c$ \ (productes creuats)." % (fr('a', 'b'), fr('c', 'd'))),
     tasks(2, [r'$%d\cdot%d=%d$, \ $%d\cdot%d=%d$: \ \res{\text{%s}}' % (a, d, a * d, b, c, b * c, 'sí' if a * d == b * c else 'no') for a, b, c, d in CHK])),
 (1, r"Calcula el valor de $x$ perquè les fraccions siguen equivalents:" + tasks(5, [r'$%s=%s$' % (xf(p), xf(q)) for p, q, _ in XS]),
     tasks(5, [r'$x=\res{%d}$' % x for _, _, x in XS])),
 (2, r"Completa perquè siguen equivalents: \quad $%s=%s=%s=%s$" % (fr(2, 5), fr(r'\square', 20), fr(12, r'\square'), fr(r'\square', 45)),
     r"$%s=%s=%s=%s$" % (fr(2, 5), fr(r'\res{8}', 20), fr(12, r'\res{30}'), fr(r'\res{18}', 45))),
 (2, r"Quina d'aquestes fraccions no és equivalent a les altres? \quad $%s$" % lst(['6/9', '10/15', '14/20', '16/24']),
     r"$\res{%s}$ ($=%s$); \ les altres valen $%s$." % (fr(14, 20), fr(7, 10), fr(2, 3))),
 (3, r"Troba $x$ i $y$ perquè \ $%s=%s=%s$." % (fr('x', 12), fr(15, 20), fr(9, 'y')),
     r"$%s=%s$: \ $x=\res{9}$, \ $y=\res{12}$." % (fr(15, 20), fr(3, 4))),
 (3, r"Troba una fracció equivalent a $%s$ que tinga el denominador $24$ unitats més gran que el numerador." % fr(3, 5),
     r"En $%s$ la diferència és $2$; amplifiquem per $24:2=12$: \ $\res{%s}$." % (fr(3, 5), fr(36, 60))),
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
S.append(("Reducció a comú denominador", [
 (1, r"Redueix a comú denominador:" + tasks(4, ['$%s$' % lst(f) for f in CD1])
     + recorda(r"Nou denominador: el \textbf{mcm} dels denominadors. Per a cada fracció, dividim el mcm entre el seu denominador i multipliquem el numerador pel resultat."),
     tasks(2, ['$%s$' % cd(f)[1] for f in CD1])),
 (2, r"Redueix a comú denominador:" + tasks(4, ['$%s$' % lst(f) for f in CD2]),
     tasks(2, [r'$\text{mcm}=%d$: \ $%s$' % cd(f) for f in CD2])),
 (2, r"Escriu les fraccions $%s$ amb denominador $36$." % lst(['5/6', '7/12', '4/9']),
     r"$\res{%s}$" % lst(['30/36', '21/36', '16/36'])),
 (3, r"Simplifica primer i després redueix a comú denominador amb el denominador més xicotet possible: \ $%s$." % lst(['6/9', '10/15', '9/12']),
     r"$%s$ \ $\to$ \ $\text{mcm}(3,3,4)=12$: \ $\res{%s}$." % (lst(['2/3', '2/3', '3/4']), lst(['8/12', '8/12', '9/12']))),
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
S.append(("Comparar i ordenar fraccions", [
 (1, r"Escriu una fracció més gran i una de més xicoteta que la donada:" + tasks(3, ['$%s$' % fr(*x) for x in [(5, 7), (4, 9), (3, 13)]]),
     tasks(3, [r'$%s<%s<%s$' % (fr(4, 7), fr(5, 7), fr(6, 7)), r'$%s<%s<%s$' % (fr(3, 9), fr(4, 9), fr(5, 9)), r'$%s<%s<%s$' % (fr(2, 13), fr(3, 13), fr(4, 13))]) + r"\par (Hi ha moltes respostes possibles.)"),
 (1, r"Compara (escriu $<$, $>$ o $=$):" + tasks(4, [r'$%s\ \square\ %s$' % (xf(a), xf(b)) for a, b in CMP])
     + recorda(r"Mateix denominador: més gran el de numerador més gran. Mateix numerador: més gran el de denominador més xicotet. Si no, redueix a comú denominador."),
     tasks(4, [r'$%s\ \res{%s}\ %s$' % (xf(a), cmpsym(a, b), xf(b)) for a, b in CMP])),
 (2, r"Ordena de menor a major:" + tasks(3, ['$%s$' % lst(f) for f in ORD1]),
     tasks(3, ['$%s$' % order(f) for f in ORD1])),
 (2, r"Ordena de menor a major:" + tasks(3, ['$%s$' % lst(f) for f in ORD2]),
     tasks(2, ['$%s$' % order(f) for f in ORD2])),
 (2, r"Marca en la recta les fraccions $%s$.\par\smallskip{\centering %s\par}" % (lst(['1/4', '3/4', '5/4', '3/2']), tz_line(2, 4)),
     r"{\centering %s\par}" % tz_line(2, 4, [(1, 4), (3, 4), (5, 4), (3, 2)])),
 (3, r"Escriu una fracció compresa entre $%s$ i $%s$, i una altra entre $%s$ i $%s$." % (fr(2, 5), fr(3, 5), fr(1, 3), fr(1, 2)),
     r"$%s=%s$ i $%s=%s$: \ $\res{%s}$. \qquad $%s=%s$ i $%s=%s$: \ $\res{%s}$." % (fr(2, 5), fr(4, 10), fr(3, 5), fr(6, 10), fr(5, 10), fr(1, 3), fr(4, 12), fr(1, 2), fr(6, 12), fr(5, 12))),
 (3, r"Tres amics llegeixen el mateix llibre: l'Anna n'ha llegit $%s$, en Biel $%s$ i la Clara $%s$. Qui n'ha llegit més? Ordena'ls." % (fr(3, 4), fr(5, 8), fr(7, 10)),
     r"$\text{mcm}=40$: \ $%s$. \ L'ha llegit més l'\res{\text{Anna}}, després la Clara i després en Biel." % lst(['30/40', '25/40', '28/40'])),
]))

SR1 = ['4/7+8/7', '2/3+1/5', '5/2-1/8', '3/6-4/12', '5/8+1/5', '14/15-2/3']
SR2 = ['12/15+8/9', '7/12-3/10', '7/6+8/12', '18/5-3/10', '5/3-9/24', '35/36+2/9']
SR3 = ['3/4+6/8', '4+25/9', '25/8-2', '3/5+1', '5-3/25', '13/6+2/7']
SR4 = ['4/5+2/7-1/2', '6/8+4/3-8/12', '3/2+6/7-2/4', '6-1/2-4/12', '2/3+1/5-1/6', '4/3+1/6-2/7']
SR5 = ['2/10+5/60-1/30', '12/5+2-1/25', '6/9+1/3-2/6', '10/3-2/6-4/5+1/2', '4-1/2+1/3+2', '7/9+1/3-2/5']
S.append(("Sumes i restes", [
 (1, r"Calcula i simplifica el resultat:" + tasks(3, [op(e) for e in SR1])
     + recorda(r"Si els denominadors són diferents, primer reduïm a \textbf{comú denominador}. \textbf{Mai} sumem els denominadors: $%s+%s=%s+%s=%s$." % (fr(1, 2), fr(1, 3), fr(3, 6), fr(2, 6), fr(5, 6))),
     tasks(3, [ops(e) for e in SR1])),
 (1, r"Calcula i simplifica (els nombres naturals tenen denominador 1):" + tasks(3, [op(e) for e in SR3]),
     tasks(3, [ops(e) for e in SR3])),
 (2, r"Calcula i simplifica el resultat:" + tasks(3, [op(e) for e in SR2]),
     tasks(3, [ops(e) for e in SR2])),
 (2, r"Calcula i simplifica:" + tasks(2, [op(e) for e in SR4]),
     tasks(2, [ops(e) for e in SR4])),
 (3, r"Calcula i simplifica:" + tasks(2, [op(e) for e in SR5]),
     tasks(2, [ops(e) for e in SR5])),
 (3, r"Omplim una piscina en tres dies: el primer dia, $%s$; el segon, $%s$, i el tercer, $%s$. Quina fracció de la piscina falta per omplir?" % (fr(1, 4), fr(2, 5), fr(1, 6)),
     r"$%s+%s+%s=%s$, \ falta $1-%s=\res{%s}$." % (fr(1, 4), fr(2, 5), fr(1, 6), ftex(val('1/4+2/5+1/6')), ftex(val('1/4+2/5+1/6')), ftex(1 - val('1/4+2/5+1/6')))),
]))

MU = ['6/4*2/5', '3/2*2/3', '2*5/6', '3/2*4/7*3', '3/4*10/2*1/6', '4/3*2/8*6/2']
INV = [('2/5', '5/3'), ('4/3', '12/16'), ('7/9', '9/7'), ('2/4', '4/2'), ('5/6', '36/30'), ('12/13', '26/12')]
DIV = ['4/3:5/6', '5/4:2', '4/8:6/3', '2/6:5/4:1/3', '3/4:12/5:2/5', '6:2/3:1/5']
MD = ['3/4*5/8:2/5', '5/4:1/3*6/5', '5/12*3/2:1/6', '6/5:7/4*2/10']
FF = [('2/3', '3/5'), ('4/10', '1/2'), ('4/3', '6/2'), ('3/5', '5/7')]
S.append(("Multiplicació i divisió", [
 (1, r"Calcula i simplifica:" + tasks(3, [op(e) for e in MU])
     + recorda(r"$%s\cdot%s=%s$. \qquad $%s:%s=%s$ \ (productes creuats). \ La \textbf{inversa} de $%s$ és $%s$." % (fr('a', 'b'), fr('c', 'd'), fr(r'a\cdot c', r'b\cdot d'), fr('a', 'b'), fr('c', 'd'), fr(r'a\cdot d', r'b\cdot c'), fr('a', 'b'), fr('b', 'a'))),
     tasks(3, [ops(e) for e in MU]) + r"\par En el b) i el f) el producte és 1: les fraccions són \textbf{inverses}."),
 (1, r"Calcula (la fracció d'una fracció és un producte):" + tasks(4, [r'$%s$ de $%s$' % (xf(a), xf(b)) for a, b in FF]),
     tasks(4, [r'$\res{%s}$' % ftex(val(a + '*' + b)) for a, b in FF])),
 (1, r"Quines parelles són fraccions inverses? (El seu producte ha de ser 1.)" + tasks(3, [r'$%s,\ %s$' % (xf(a), xf(b)) for a, b in INV]),
     tasks(3, [r'$%s\cdot%s=%s$: \ \res{\text{%s}}' % (xf(a), xf(b), ftex(val(a + '*' + b)), 'sí' if val(a + '*' + b) == 1 else 'no') for a, b in INV])),
 (1, r"Escriu la inversa de:" + tasks(4, ['$%s$' % x for x in [fr(4, 13), fr(3, 7), fr(15, 8), '6']]),
     tasks(4, ['$%s$' % x for x in [fr(13, 4), fr(7, 3), fr(8, 15), fr(1, 6)]])),
 (2, r"Calcula i simplifica (amb divisions seguides, d'esquerra a dreta):" + tasks(3, [op(e) for e in DIV]),
     tasks(3, [ops(e) for e in DIV])),
 (2, r"Calcula i simplifica:" + tasks(2, [op(e) for e in MD]),
     tasks(2, [ops(e) for e in MD])),
 (3, r"Amb $12$ litres de suc, quantes ampolles de $%s$ de litre podem omplir? I quina fracció cal multiplicar per $%s$ per a obtindre $%s$?" % (fr(3, 4), fr(3, 4), fr(9, 10)),
     r"$12:%s=%s=\res{16}$ ampolles. \qquad $%s:%s=%s=\res{%s}$." % (fr(3, 4), fr(48, 3), fr(9, 10), fr(3, 4), fr(36, 30), fr(6, 5))),
]))

CB1 = ['5/2+1/3*4/5', '21/4-2/5:4/3', '4/3:2/6+1/3*5/4', '4/3*(2/5+1/3)', '(2/5+1):8/3', '(5/4+1)*6/7']
CB2 = ['(2/5+3/7)*1/2-4/10', '(5/4+2/3+1/12)*5/4-1', '5/4:(6/4-1)+2/5', '4/3-(1/2+2/7)+4/5*2/4']
CB3 = ['(1/4+2/3-1/12)*3+(3/2-5/4):1/2', '4*(2/3+4/6-1)+2/3', '(3/2+1/7)*(5/3-7/15)', '12/10:5/4+1/2*13/5', '(4/3+2/5*1/3):4/12', '3/2:1/4*4/20+3/2*7/5']
CB4 = ['(5/4+2/3-1)*3/5+(2/5+4/3)*2', '3/8+4/5*1/3+(2/6-1/4)*3']
S.append(("Operacions combinades", [
 (2, r"Calcula i simplifica:" + tasks(2, [op(e) for e in CB1])
     + recorda(r"Ordre: 1r \textbf{parèntesis}; 2n \textbf{multiplicacions i divisions} (d'esquerra a dreta); 3r \textbf{sumes i restes} (d'esquerra a dreta)."),
     tasks(2, [ops(e) for e in CB1])),
 (2, r"Calcula i simplifica:" + tasks(2, [op(e) for e in CB2]),
     tasks(2, [ops(e) for e in CB2])),
 (3, r"Calcula i simplifica:" + tasks(2, [op(e) for e in CB3]),
     tasks(2, [ops(e) for e in CB3])),
 (3, r"Calcula i simplifica:" + tasks(1, [op(e) for e in CB4]),
     tasks(1, [ops(e) for e in CB4])),
]))

S.append(("Problemes amb fraccions", [
 (1, r"D'un sopar, en Joan se n'ha menjat $%s$, l'Elena $%s$ i la Maite $%s$." % (fr(1, 7), fr(2, 5), fr(1, 8)) + tasks(1, ["Quant s'han menjat entre tots tres?", "Quant n'ha sobrat?", "Qui ha menjat més i qui menys?"])
     + recorda(r"Llig l'enunciat dues vegades, fes un \textbf{dibuix} (una barra que representa el total) i, al final, \textbf{comprova} que el resultat té sentit."),
     tasks(1, [r"$\text{mcm}=280$: \ $%s=\res{%s}$" % (lst(['40/280', '112/280', '35/280']).replace(',\\ ', '+'), fr(187, 280)), r"$1-%s=\res{%s}$" % (fr(187, 280), fr(93, 280)), r"Més: l'\res{\text{Elena}} ($%s$); \ menys: la \res{\text{Maite}} ($%s$)." % (fr(112, 280), fr(35, 280))])),
 (1, r"D'un pastís de 24 porcions ens n'hem menjat $%s$. Quantes porcions queden?" % fr(5, 8),
     r"Ens n'hem menjat $(24:8)\cdot5=15$: \ queden $\res{9}$ porcions."),
 (2, r"D'una pizza, en Carles se'n menja $%s$, en Miquel $%s$ i la Lorena $%s$." % (fr(3, 6), fr(3, 21), fr(4, 14)) + tasks(1, ["Quina fracció de la pizza ha sobrat?", r"Arriba la Mireia amb una altra pizza igual. Com que els altres ja estan farts, ella es menja el que havia sobrat i $%s$ de la seua pizza. Quanta pizza s'ha menjat ella?" % fr(3, 5)]),
     tasks(1, [r"$%s+%s+%s=%s$: \ sobra $\res{%s}$." % (fr(1, 2), fr(1, 7), fr(2, 7), fr(13, 14), fr(1, 14)), r"$%s+%s=%s+%s=\res{%s}$ de pizza." % (fr(1, 14), fr(3, 5), fr(5, 70), fr(42, 70), fr(47, 70))])),
 (2, r"En un poble de 5250 habitants, la meitat tenen més de 65 anys i $%s$ en tenen menys de 18." % fr(1, 5) + tasks(1, ["Quina fracció representen els que tenen entre 18 i 65 anys?", "Quants habitants hi ha en cada franja d'edat?"]),
     tasks(1, [r"$1-%s-%s=\res{%s}$" % (fr(1, 2), fr(1, 5), fr(3, 10)), r"Més de 65: $\res{2625}$; \ menys de 18: $\res{1050}$; \ entre 18 i 65: $\res{1575}$."])),
 (2, r"Un bidó de 60 litres està ple. Primer se'n gasten $%s$ i després $%s$ del que quedava. Finalment, el bidó bolca i es vessa la meitat del que hi ha. Quants litres queden al final?" % (fr(2, 4), fr(1, 3)),
     r"Es gasten 30 L (queden 30); \ després $%s$ de 30 $=10$ L (queden 20); \ es vessa la meitat: queden $\res{10\text{ L}}$." % fr(1, 3)),
 (3, r"Una família gasta $%s$ del sou en la hipoteca, $%s$ en menjar, $%s$ en el cotxe i la resta en altres despeses. Quina fracció representen les altres despeses?" % (fr(2, 6), fr(1, 5), fr(2, 7)),
     r"$%s+%s+%s=%s$ \ $\Rightarrow$ \ $1-%s=\res{%s}$." % (fr(35, 105), fr(21, 105), fr(30, 105), fr(86, 105), fr(86, 105), fr(19, 105))),
 (3, r"Una família ingressa $5400$\,€ al mes. Se'n gasta $%s$ en la hipoteca, $%s$ en menjar i $%s$ en el cotxe." % (fr(2, 6), fr(1, 5), fr(1, 9)) + tasks(1, ["Quants diners gasta en cada cosa i quants li'n queden per a altres despeses?", "Quina fracció del total representen els diners que sobren?"]),
     tasks(1, [r"Hipoteca $\res{1800\text{\,€}}$, menjar $\res{1080\text{\,€}}$, cotxe $\res{600\text{\,€}}$; \ queden $\res{1920\text{\,€}}$.", r"$%s=\res{%s}$" % (fr(1920, 5400), fr(16, 45))])),
 (3, r"Un dipòsit està ple fins als $%s$. Gastem $%s$ del que hi ha i hi queden 50 litres. Quina capacitat té el dipòsit?" % (fr(3, 4), fr(2, 3)),
     r"Queda $%s$ de $%s$, és a dir, $%s$ del dipòsit, que són 50 L: \ capacitat $50\cdot4=\res{200\text{ L}}$." % (fr(1, 3), fr(3, 4), fr(1, 4))),
]))

# comprovacions dels resultats escrits a mà
assert val('1/7+2/5+1/8') == Fr(187, 280) and val('1/2+1/7+2/7') == Fr(13, 14) and val('1/14+3/5') == Fr(47, 70)
assert val('1-1/2-1/5') == Fr(3, 10) and val('1-(2/6+1/5+2/7)') == Fr(19, 105) and val('1-(2/6+1/5+1/9)') == Fr(16, 45)
assert Fr(1920, 5400) == Fr(16, 45) and 5400 - 1800 - 1080 - 600 == 1920

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={fraccions, fracció d\'un nombre, percentatges, fraccions equivalents, comú denominador, comparar fraccions, operacions amb fraccions, problemes}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 4: Fraccions. 1r d'ESO}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 4: Fraccions · 1r d'ESO" % t)
    assert 'Unitat 4' in p and 'unitat 4' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\begin{document}
\thispagestyle{primera}

\begin{minipage}[c]{0.25\textwidth}\includegraphics[width=\linewidth]{logo-gva.png}\end{minipage}%
\begin{minipage}[c]{0.5\textwidth}\centering
  {\color{navy}\Large\bfseries ''' + ('Solucions de la fitxa de la unitat 4:' if sol else "Fitxa d'exercicis de la unitat 4:") + r'''\\[2pt] Fraccions}\\[5pt]
  {\color{accent}\large\bfseries 1r d'ESO}
\end{minipage}%
\begin{minipage}[c]{0.25\textwidth}\hfill\includegraphics[width=0.85\linewidth]{logo-vermellar.png}\end{minipage}

\vspace{6pt}
{\color{navy}\hrule height 1.2pt}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat. Recorda que els resultats s'han de donar sempre en forma de fracció irreductible."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i dona els resultats en forma de fracció irreductible. Les figures i les rectes es poden completar directament en la fitxa. Fes els càlculs sense calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't4-fitxa-solucions.tex' if sol else 't4-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
