# Versió en castellà de genera.py. Genera t5-fitxa-exercicis-es.tex i t5-fitxa-solucions-es.tex
# (1r ESO, Unitat 5: Proporcionalitat i percentatges. Nombres decimals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les operacions es calculen amb Decimal/Fraction (val/ops) i les asserts de CHK comproven
# els resultats escrits a mà.
import os, re
from decimal import Decimal as Dm, getcontext, ROUND_HALF_UP, ROUND_DOWN
from fractions import Fraction as Fr
getcontext().prec = 40
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- nombres ----------
def fmt(x):
    """Decimal -> text amb coma, sense zeros sobrants; espai fi de milers a partir de 5 xifres"""
    x = Dm(x)
    s = format(x.normalize(), 'f') if x != x.to_integral() else str(int(x))
    neg = s.startswith('-'); s = s.lstrip('-')
    ip, _, fp = s.partition('.')
    if len(ip) > 4: ip = '{:,}'.format(int(ip)).replace(',', '\\,')
    return ('-' if neg else '') + ip + (',' + fp if fp else '')
def num(s): return s.replace('.', ',')
def eur(x):
    """preu: sense decimals si és enter; si no, amb cèntims"""
    x = Dm(x)
    return fmt(x) if x == x.to_integral() else format(x.quantize(Dm('0.01'), ROUND_HALF_UP), 'f').replace('.', ',')
def tx(e):
    return re.sub(r'(\d)\.(\d)', r'\1,\2', e).replace('*', r'\cdot ')
def val(e):
    py = re.sub(r'\d+(?:\.\d+)?', lambda m: "Dm('%s')" % m[0], e).replace(':', '/')
    return eval(py)
def ops(e): return '$' + tx(e) + r'=\res{' + fmt(val(e)) + '}$'
def op(e): return '$' + tx(e) + '$'
def fr(a, b): return r'\dfrac{%s}{%s}' % (a, b)
def ftex(f):
    f = Fr(f)
    return str(f.numerator) if f.denominator == 1 else fr(f.numerator, f.denominator)
def rnd(x, k): return Dm(x).quantize(Dm(1).scaleb(-k), ROUND_HALF_UP)
def trn(x, k): return Dm(x).quantize(Dm(1).scaleb(-k), ROUND_DOWN)
def per(n, d):
    """n/d en decimal amb el període marcat"""
    q, r = divmod(n, d); f = ''; seen = {}
    while r and r not in seen:
        seen[r] = len(f); r *= 10; f += str(r // d); r %= d
    if not r: return str(q) + (',' + f if f else '')
    i = seen[r]
    return str(q) + ',' + f[:i] + r'\overline{' + f[i:] + '}'
def kind(n, d):
    f = Fr(n, d); dd = f.denominator
    for p in (2, 5):
        while dd % p == 0: dd //= p
    if dd == 1: return 'exacto'
    return 'periódico puro' if per(n, d).split(',')[1].startswith(r'\overline') else 'periódico mixto'
CHK = []
def ck(a, b): CHK.append((a, b)); assert (Dm(str(a)) if not isinstance(a, Fr) else a) == (Dm(str(b)) if not isinstance(a, Fr) else Fr(b)), (a, b)

# ---------- figures TikZ ----------
def tz_line(a, b, parts, pts=(), labels=True, w=12.0, k=1):
    """recta de a a b amb «parts» divisions; pts = [(valor, etiqueta)]"""
    a, b = float(a), float(b)
    X = lambda v: (v - a) / (b - a) * w
    g = r'\draw[-latex,thick] (-0.3,0)--(%.2f,0);' % (w + 0.5)
    for j in range(parts + 1):
        v = a + (b - a) * j / parts; big = j in (0, parts)
        g += r'\draw[%s] (%.3f,%.2f)--(%.3f,%.2f);' % ('thick' if big else 'muted', X(v), 0.2 if big else 0.12, X(v), -0.2 if big else -0.12)
        if big or labels == 'all':
            g += r'\node[below=2pt,font=\%s] at (%.3f,-0.1) {$%s$};' % ('small' if big else 'scriptsize', X(v), ('%.*f' % (k - (1 if big and labels != 'all' else 0) if k else 0, v)).replace('.', ','))
    for i, (v, t) in enumerate(pts):
        g += r'\fill[accent] (%.3f,0) circle (0.09) node[above=3pt,text=accent,font=\small]{%s};' % (X(float(v)), t)
    return r'\begin{tikzpicture}[baseline=0]%s\end{tikzpicture}' % g
def taula(fil1, fil2, h1, h2):
    cols = len(fil1)
    return (r'{\renewcommand{\arraystretch}{1.35}\begin{tabular}{|l|' + 'C{1.25cm}|' * cols + r'}\hline ' + h1 + ' & ' + ' & '.join(fil1) + r'\\\hline '
            + h2 + ' & ' + ' & '.join(fil2) + r'\\\hline\end{tabular}}')

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
LECT = [('7.25', '7 unidades y 25 centésimas'), ('0.408', '408 milésimas'), ('12.06', '12 unidades y 6 centésimas'), ('3.5', '3 unidades y 5 décimas'), ('100.001', '100 unidades y 1 milésima'), ('0.09', '9 centésimas')]
ESCR = [('tres unidades y cuarenta y cinco milésimas', '3.045'), ('doce centésimas', '0.12'), ('veinte unidades y nueve décimas', '20.9'), ('siete milésimas', '0.007'), ('cien unidades y cinco centésimas', '100.05'), ('cuatro unidades y trescientas milésimas', '4.300')]
VALX = [('34.571', '7', '7 centésimas = 0,07'), ('2.738', '3', '3 centésimas = 0,03'), ('607.15', '7', '7 unidades'), ('0.0809', '8', '8 centésimas = 0,08'), ('15.4', '4', '4 décimas = 0,4'), ('9.206', '6', '6 milésimas = 0,006')]
S.append(("Números decimales", [
 (1, r"Escribe cómo se leen estos números:" + tasks(3, ['$%s$' % num(a) for a, _ in LECT])
     + recorda(r"Leemos la parte entera, la palabra \emph{unidades} y la parte decimal con el nombre de la \textbf{última} cifra: $3,045$ son 3 unidades y 45 milésimas."),
     tasks(2, ['$%s$: %s' % (num(a), b) for a, b in LECT])),
 (1, r"Escribe con cifras:" + tasks(2, [a.capitalize() for a, _ in ESCR]),
     tasks(3, [r'$\res{%s}$' % num(b) for _, b in ESCR])),
 (1, r"¿Cuánto vale la cifra indicada en cada número?" + tasks(3, [r'El %s en $%s$' % (d, num(x)) for x, d, _ in VALX]),
     tasks(2, [r'El %s en $%s$: %s' % (d, num(x), v) for x, d, v in VALX])),
 (2, r"Completa:" + tasks(2, [r"$1$ unidad $=$ \rule{1cm}{0.4pt} décimas", r"$1$ décima $=$ \rule{1cm}{0.4pt} centésimas", r"$3$ unidades $=$ \rule{1cm}{0.4pt} centésimas", r"$45$ centésimas $=$ \rule{1cm}{0.4pt} unidades", r"$250$ milésimas $=$ \rule{1cm}{0.4pt} décimas", r"$7$ décimas $=$ \rule{1cm}{0.4pt} milésimas"]),
     tasks(3, [r"$\res{10}$ décimas", r"$\res{10}$ centésimas", r"$\res{300}$ centésimas", r"$\res{0,45}$ unidades", r"$\res{2,5}$ décimas", r"$\res{700}$ milésimas"])),
 (2, r"Descompón cada número según el valor de sus cifras:" + tasks(3, ['$%s$' % num(x) for x in ['45.312', '7.09', '120.506']]),
     tasks(1, [r'$45,312=40+5+0,3+0,01+0,002$', r'$7,09=7+0,09$', r'$120,506=100+20+0,5+0,006$'])),
 (3, r"Escribe el número que tiene: a) 4 decenas, 6 décimas y 2 milésimas; \ b) 8 centenas, 3 unidades y 5 centésimas; \ c) 15 centésimas y 3 milésimas. ¿Cuál de estos es igual a $0,15$: \ $0,150$, \ $0,015$ o \ $0,1500$?",
     r"a) $\res{40,602}$ \quad b) $\res{803,05}$ \quad c) $\res{0,153}$. \ Son iguales a $0,15$: $\res{0,150}$ y $\res{0,1500}$ (los ceros finales no cambian el valor)."),
]))
ck(Dm('40') + Dm('0.6') + Dm('0.002'), '40.602'); ck(800 + 3 + Dm('0.05'), '803.05'); ck(Dm('0.15') + Dm('0.003'), '0.153')
ck(40 + 5 + Dm('0.3') + Dm('0.01') + Dm('0.002'), '45.312'); ck(100 + 20 + Dm('0.5') + Dm('0.006'), '120.506')

# =====================================================================
CMP = [('4.7', '4.68'), ('0.09', '0.1'), ('5.307', '5.37'), ('12.5', '12.50'), ('3.099', '3.1'), ('0.45', '0.405')]
def sym(a, b): c = Dm(a) - Dm(b); return '<' if c < 0 else '>' if c > 0 else '='
ORD = ['2.5', '2.05', '2.55', '2.505', '2.0', '2.15']
ROUND = ['3.4682', '15.8962', '0.7049', '29.996']
S.append(("Comparar, representar y aproximar decimales", [
 (1, r"Escribe $<$, $>$ o $=$:" + tasks(3, [r'$%s\ \square\ %s$' % (num(a), num(b)) for a, b in CMP])
     + recorda(r"Para comparar, igualamos el número de decimales añadiendo ceros: $\ 3,5\ \text{?}\ 3,48\ \to\ 3,50>3,48$."),
     tasks(3, [r'$%s\ \res{%s}\ %s$' % (num(a), sym(a, b), num(b)) for a, b in CMP])),
 (1, r"Ordena de menor a mayor: \ $%s$" % ';\\ '.join(num(x) for x in ORD),
     r"$\res{%s}$" % '<'.join(num(x) for x in sorted(ORD, key=Dm))),
 (2, r"Escribe el número decimal que corresponde a cada punto:\par\smallskip{\centering %s\par}" % tz_line(3, 4, 10, [(3.2, 'A'), (3.7, 'B'), (3.9, 'C')]) + r"\par\smallskip{\centering %s\par}" % tz_line(0.5, 0.6, 10, [(0.53, 'D'), (0.58, 'E')], k=2),
     r"A $=\res{3,2}$, \ B $=\res{3,7}$, \ C $=\res{3,9}$, \ D $=\res{0,53}$, \ E $=\res{0,58}$."),
 (2, r"Representa en la recta $1,4$ \ y \ $1,75$ (la recta va de 1 a 2).\par\smallskip{\centering %s\par}" % tz_line(1, 2, 20),
     r"Dividimos la unidad en 20 partes (cada una vale $0,05$):\par\smallskip{\centering %s\par}" % tz_line(1, 2, 20, [(1.4, '$1,4$'), (1.75, '$1,75$')])),
 (2, r"Escribe tres números decimales comprendidos entre:" + tasks(3, [r'$0,3$ y $0,4$', r'$2,71$ y $2,72$', r'$5$ y $5,1$']),
     tasks(3, [r'Por ejemplo $0,31$; $0,35$; $0,39$', r'Por ejemplo $2,711$; $2,715$; $2,719$', r'Por ejemplo $5,01$; $5,05$; $5,09$']) + r"\par (Hay infinitas respuestas.)"),
 (2, r"Completa la tabla aproximando cada número:\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.3cm}|C{2.3cm}|C{2.3cm}|}\hline Número & Truncado a las centésimas & Redondeado a las décimas & Redondeado a las centésimas\\\hline "
     + r'\\\hline '.join('$%s$ & & & ' % num(x) for x in ROUND) + r'\\\hline\end{tabular}\par}'
     + recorda(r"Para \textbf{redondear}, miramos la primera cifra que eliminamos: si es $0,1,2,3,4$ la dejamos igual; si es $5,6,7,8,9$ sumamos 1 a la última cifra que queda."),
     r"\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.3cm}|C{2.3cm}|C{2.3cm}|}\hline Número & Truncado a las centésimas & Redondeado a las décimas & Redondeado a las centésimas\\\hline "
     + r'\\\hline '.join(r'$%s$ & $%s$ & $\res{%s}$ & $\res{%s}$' % (num(x), num(str(trn(x, 2))), num(str(rnd(x, 1))), num(str(rnd(x, 2)))) for x in ROUND) + r'\\\hline\end{tabular}\par}'),
 (3, r"Un artículo cuesta $12,4583$\,€ según la calculadora. ¿Cuánto pagaremos? Escribe un número que, redondeado a las décimas, sea $2,5$ y que sea menor que $2,5$. ¿Cuál es el número más pequeño con dos cifras decimales que redondeado a las unidades da 8?",
     r"Redondeamos a céntimos: $\res{12,46\text{\,€}}$. \ Por ejemplo $\res{2,47}$ (cualquiera desde $2,45$ hasta $2,5$ sin llegar). \ El más pequeño es $\res{7,50}$."),
]))
ck(rnd('12.4583', 2), '12.46'); ck(rnd('7.50', 0), '8'); ck(rnd('7.49', 0), '7')
assert [rnd(x, 2) for x in ROUND] == [Dm('3.47'), Dm('15.90'), Dm('0.70'), Dm('30.00')]

# =====================================================================
SUM = ['23.45+7.8', '40-12.35', '0.9+0.35', '15-6.47', '3.06+12.9+0.4', '100-0.01']
MUL = ['4.6*3', '2.35*0.4', '0.6*0.05', '12.5*1.2', '3.25*1.4', '0.07*0.3']
P10 = ['3.7*100', '0.052*1000', '45.2:1000', '8:100', '6.15*10', '0.3:10', '250*0.1', '1.4*0.01']
S.append(("Sumar, restar y multiplicar decimales", [
 (1, r"Calcula:" + tasks(3, [op(e) for e in SUM])
     + recorda(r"Para sumar y restar, colocamos las \textbf{comas alineadas} y completamos con ceros."),
     tasks(3, [ops(e) for e in SUM])),
 (1, r"Calcula:" + tasks(3, [op(e) for e in MUL])
     + recorda(r"Para multiplicar, lo hacemos como si no hubiera comas y separamos tantos decimales como \textbf{suman} los dos factores."),
     tasks(3, [ops(e) for e in MUL])),
 (1, r"Calcula mentalmente:" + tasks(4, [op(e) for e in P10]),
     tasks(4, [ops(e) for e in P10])),
 (2, r"Coloca la coma en el resultado sin hacer la operación: \ $3,8\cdot2,5=950$; \ $0,45\cdot1,2=540$; \ $12,6\cdot0,03=378$. Compruébalo estimando.",
     r"$3,8\cdot2,5=\res{9,50}$ (cerca de $4\cdot2=8$); \ $0,45\cdot1,2=\res{0,540}$ (cerca de $0,5$); \ $12,6\cdot0,03=\res{0,378}$ (2+1 decimales suman 3)."),
 (2, r"Completa con el número que falta:" + tasks(3, [r'$2,75+\square=5$', r'$\square-1,8=3,45$', r'$0,6\cdot\square=60$']),
     tasks(3, [r'$\res{2,25}$', r'$\res{5,25}$', r'$\res{100}$'])),
 (2, r"Compramos $2,5$ kg de manzanas a $1,80$\,€/kg y $1,5$ kg de cerezas a $6,40$\,€/kg. Pagamos con un billete de 20\,€. ¿Cuánto nos devuelven?",
     r"Manzanas: $2,5\cdot1,80=4,50$\,€; \ cerezas: $1,5\cdot6,40=9,60$\,€; \ total $14,10$\,€. \ Nos devuelven $20-14,10=\res{5,90\text{\,€}}$."),
 (3, r"Una piscina mide $25$ m de largo. Lucía hace $8$ largos y su hermano, $5,5$ largos. ¿Cuántos metros más ha nadado Lucía? Si Lucía nada cada largo en $0,45$ minutos, ¿cuánto tarda en total?",
     r"Lucía: $25\cdot8=200$ m; \ hermano: $25\cdot5,5=137,5$ m; \ diferencia $\res{62,5\text{ m}}$. \ Tiempo: $8\cdot0,45=\res{3,6\text{ minutos}}$."),
 (3, r"El perímetro de un triángulo es $17,25$ cm. Dos lados miden $4,8$ cm y $6,07$ cm. ¿Cuánto mide el tercer lado? ¿Cuánto mediría el perímetro de un triángulo con todos los lados 10 veces más largos?",
     r"Tercer lado: $17,25-(4,8+6,07)=17,25-10,87=\res{6,38\text{ cm}}$. \ Perímetro: $17,25\cdot10=\res{172,5\text{ cm}}$."),
]))
ck(Dm('3.8') * Dm('2.5'), '9.5'); ck(Dm('0.45') * Dm('1.2'), '0.54'); ck(Dm('12.6') * Dm('0.03'), '0.378')
ck(5 - Dm('2.75'), '2.25'); ck(Dm('3.45') + Dm('1.8'), '5.25'); ck(Dm(60) / Dm('0.6'), '100')
ck(Dm('2.5') * Dm('1.80') + Dm('1.5') * Dm('6.40'), '14.10'); ck(25 * 8 - 25 * Dm('5.5'), '62.5'); ck(8 * Dm('0.45'), '3.6')
ck(Dm('17.25') - Dm('4.8') - Dm('6.07'), '6.38')

# =====================================================================
DIV1 = ['8.4:4', '9.75:3', '6.24:3', '0.8:2', '15.3:5', '1.26:6']
DIV2 = ['7:4', '15:8', '9:4', '3:5', '1:8', '21:12']
DIV3 = ['4.5:0.9', '2.73:0.7', '6:0.12', '12.6:0.35', '1.44:1.2', '0.9:0.03']
S.append(("Dividir con decimales", [
 (1, r"Calcula:" + tasks(3, [op(e) for e in DIV1]),
     tasks(3, [ops(e) for e in DIV1])),
 (1, r"Calcula sacando decimales en el cociente hasta que la división sea exacta:" + tasks(3, [op(e) for e in DIV2])
     + recorda(r"Si sobra resto, ponemos una coma en el cociente, añadimos un 0 al resto y seguimos dividiendo."),
     tasks(3, [ops(e) for e in DIV2])),
 (2, r"Calcula (si el divisor tiene decimales, multiplica dividendo y divisor por 10, 100…):" + tasks(3, [op(e) for e in DIV3]),
     tasks(3, ['$%s=%s=\\res{%s}$' % (tx(e), tx(conv), fmt(val(e))) for e, conv in zip(DIV3, ['45:9', '27.3:7', '600:12', '1260:35', '14.4:12', '90:3'])])),
 (2, r"Calcula con dos cifras decimales e indica el resto: \ a) $10:3$ \quad b) $5:7$ \quad c) $25,4:6$",
     r"a) $\res{3,33}$, resto $0,01$ \quad b) $\res{0,71}$, resto $0,03$ \quad c) $\res{4,23}$, resto $0,02$."),
 (2, r"Con una botella de $1,5$ L, ¿cuántos vasos de $0,25$ L podemos llenar? ¿Y con una garrafa de 5 L?",
     r"$1,5:0,25=150:25=\res{6\text{ vasos}}$; \ $5:0,25=500:25=\res{20\text{ vasos}}$."),
 (3, r"Un trozo de queso de $0,85$ kg cuesta $11,39$\,€. ¿Cuál es el precio de un kilo? ¿Cuánto costaría un trozo de $1,2$ kg?",
     r"$11,39:0,85=1139:85=\res{13,40\text{\,€/kg}}$. \ $1,2\cdot13,40=\res{16,08\text{\,€}}$."),
 (3, r"Un coche ha gastado $31,5$ L de gasolina en un viaje de 450 km. ¿Cuántos litros gasta cada 100 km? Si la gasolina cuesta $1,56$\,€/L, ¿cuánto ha costado el viaje?",
     r"$31,5:4,5=\res{7\text{ L}}$ cada 100 km. \ Coste: $31,5\cdot1,56=\res{49,14\text{\,€}}$."),
]))
for e, conv in zip(DIV3, ['45:9', '27.3:7', '600:12', '1260:35', '14.4:12', '90:3']): ck(val(e), val(conv))
for e in DIV1 + DIV2 + DIV3: assert val(e) == val(e).quantize(Dm('0.0001')), e   # divisions exactes
ck(trn(Dm(10) / 3, 2), '3.33'); ck(10 - 3 * Dm('3.33'), '0.01'); ck(trn(Dm(5) / 7, 2), '0.71'); ck(5 - 7 * Dm('0.71'), '0.03')
ck(trn(Dm('25.4') / 6, 2), '4.23'); ck(Dm('25.4') - 6 * Dm('4.23'), '0.02')
ck(Dm('1.5') / Dm('0.25'), '6'); ck(Dm(5) / Dm('0.25'), '20'); ck(Dm('11.39') / Dm('0.85'), '13.4'); ck(Dm('1.2') * Dm('13.40'), '16.08')
ck(Dm('31.5') / Dm('4.5'), '7'); ck(Dm('31.5') * Dm('1.56'), '49.14')

# =====================================================================
D2F = ['0.6', '0.45', '1.2', '0.004', '0.125', '2.75', '0.08', '3.5']
F2D = [(9, 20), (5, 9), (7, 12), (3, 8), (4, 11), (1, 6), (13, 5), (2, 3)]
S.append(("Decimales y fracciones", [
 (1, r"Escribe como fracción decimal y después como fracción irreducible:" + tasks(4, ['$%s$' % num(x) for x in D2F])
     + recorda(r"En el numerador ponemos el número sin coma; en el denominador, un 1 seguido de tantos ceros como decimales tiene: \ $0,35=%s=%s$." % (fr(35, 100), fr(7, 20))),
     tasks(4, [r'$%s=%s=\res{%s}$' % (num(x), fr(Dm(x).scaleb(len(x.split('.')[1])).to_integral(), 10 ** len(x.split('.')[1])), ftex(Fr(x))) for x in D2F])),
 (1, r"Escribe en forma decimal:" + tasks(4, ['$%s$' % fr(n, 10 ** k) for n, k in [(7, 1), (35, 2), (4, 3), (125, 2)]]),
     tasks(4, [r'$\res{0,7}$', r'$\res{0,35}$', r'$\res{0,004}$', r'$\res{1,25}$'])),
 (2, r"Escribe en forma decimal y clasifica en exacto, periódico puro o periódico mixto:" + tasks(4, ['$%s$' % fr(n, d) for n, d in F2D])
     + recorda(r"Dividimos el numerador entre el denominador. Si las cifras se repiten, el decimal es \textbf{periódico} y marcamos el período: \ $%s=0,8333\ldots=0,8\overline{3}$." % fr(5, 6)),
     tasks(2, [r'$%s=\res{%s}$ \ (%s)' % (fr(n, d), per(n, d), kind(n, d)) for n, d in F2D])),
 (2, r"Ordena de menor a mayor pasándolo todo a decimal: \ $0,7;\ \ %s;\ \ 0,67;\ \ %s;\ \ 0,6$" % (fr(2, 3), fr(3, 4)),
     r"$%s=0,\overline{6}$ \ y \ $%s=0,75$: \qquad $0,6<\res{%s}<0,67<0,7<%s$" % (fr(2, 3), fr(3, 4), fr(2, 3), fr(3, 4))),
 (2, r"¿Cuál es mayor?" + tasks(3, [r'$%s$ o $0,62$' % fr(5, 8), r'$%s$ o $0,33$' % fr(1, 3), r'$%s$ o $1,4$' % fr(7, 5)]),
     tasks(3, [r'$%s=0,625>0,62$' % fr(5, 8), r'$%s=0,333\ldots>0,33$' % fr(1, 3), r'$%s=1,4$: son iguales' % fr(7, 5)])),
 (3, r"Escribe una fracción de denominador 3 comprendida entre $1,5$ y $2$, y una fracción de denominador 8 comprendida entre $0,3$ y $0,4$.",
     r"$\res{%s}=1,\overline{6}$; \qquad $\res{%s}=0,375$." % (fr(5, 3), fr(3, 8))),
 (3, r"Un pastel se divide en 8 porciones iguales. Marta se come $0,25$ del pastel y Pablo 3 porciones. ¿Quién ha comido más? ¿Qué parte del pastel queda, en fracción y en decimal?",
     r"Marta: $0,25=%s$ (2 porciones); Pablo: $%s=0,375$. \ \rest{Pablo} ha comido más. \ Queda $1-%s-%s=\res{%s=0,375}$." % (fr(2, 8), fr(3, 8), fr(2, 8), fr(3, 8), fr(3, 8))),
]))
for x in D2F: assert Fr(x) == Fr(Dm(x))
assert [kind(n, d) for n, d in F2D] == ['exacto', 'periódico puro', 'periódico mixto', 'exacto', 'periódico puro', 'periódico mixto', 'exacto', 'periódico puro']
assert per(5, 9) == r'0,\overline{5}' and per(7, 12) == r'0,58\overline{3}' and per(4, 11) == r'0,\overline{36}' and per(13, 5) == '2,6'
ck(Fr(1) - Fr(2, 8) - Fr(3, 8), Fr(3, 8))

# =====================================================================
S.append(("Razones y proporciones", [
 (1, r"En una cesta hay 18 manzanas y 24 peras. Calcula la razón entre manzanas y peras y la razón entre peras y frutas totales. ¿Qué significan?",
     r"Manzanas/peras: $%s=\res{%s}=0,75$: por cada 3 manzanas hay 4 peras. \ Peras/total: $%s=\res{%s}$: 4 de cada 7 frutas son peras." % (fr(18, 24), fr(3, 4), fr(24, 42), fr(4, 7))),
 (1, r"Comprueba si forman proporción:" + tasks(4, [r'$%s$ y $%s$' % (fr(*a), fr(*b)) for a, b in [((6, 9), (8, 12)), ((4, 10), (6, 15)), ((2.5, 4), (5, 9)), ((3, 7), (12, 28))]]).replace('2.5', '2,5')
     + recorda(r"$%s=%s$ forman proporción si $a\cdot d=b\cdot c$." % (fr('a', 'b'), fr('c', 'd'))),
     tasks(2, [r'$6\cdot12=72=9\cdot8$: \rest{sí}', r'$4\cdot15=60=10\cdot6$: \rest{sí}', r'$2,5\cdot9=22,5\neq4\cdot5=20$: \rest{no}', r'$3\cdot28=84=7\cdot12$: \rest{sí}'])),
 (2, r"Calcula el término desconocido:" + tasks(3, [r'$%s=%s$' % (fr(*a), fr(*b)) for a, b in [((3, 5), (12, 'x')), (('x', 8), (15, 24)), ((4, 'x'), (10, 25)), (('2,5', 4), ('x', 12)), (('1,2', '0,3'), (8, 'x')), ((7, 'x'), (21, 6))]]),
     tasks(3, [r'$x=%s=\res{%s}$' % (e, r) for e, r in [(fr(r'5\cdot12', 3), '20'), (fr(r'8\cdot15', 24), '5'), (fr(r'4\cdot25', 10), '10'), (fr(r'2,5\cdot12', 4), '7,5'), (fr(r'0,3\cdot8', '1,2'), '2'), (fr(r'7\cdot6', 21), '2')]])),
 (2, r"Para hacer una masa de pizza hacen falta 300 g de harina por cada 180 mL de agua. ¿Cuánta agua necesitamos para 750 g de harina?",
     r"$%s=%s\ \Rightarrow\ x=%s=\res{450\text{ mL}}$" % (fr(300, 180), fr(750, 'x'), fr(r'180\cdot750', 300))),
 (3, r"La razón entre la edad de una madre y la de su hija es $%s$. Si la hija tiene 12 años, ¿cuántos tiene la madre? ¿Y cuántos años tenía la madre cuando la hija tenía 4? ¿Se mantiene la razón?" % fr(7, 2),
     r"$%s=%s\Rightarrow x=\res{42\text{ años}}$. \ Hace 8 años: madre 34, hija 4; \ $%s=%s\neq%s$: la razón \rest{no se mantiene} (las edades no son proporcionales)." % (fr('x', 12), fr(7, 2), fr(34, 4), fr(17, 2), fr(7, 2))),
]))
ck(Fr(5 * 12, 3), 20); ck(Fr(8 * 15, 24), 5); ck(Fr(100, 10), 10); ck(Dm('2.5') * 12 / 4, '7.5'); ck(Dm('0.3') * 8 / Dm('1.2'), '2'); ck(Fr(42, 21), 2)
ck(Fr(180 * 750, 300), 450); ck(Fr(7 * 12, 2), 42)

# =====================================================================
S.append(("Proporcionalidad directa", [
 (1, r"Completa la tabla de proporcionalidad directa y calcula la constante de proporcionalidad:\par\smallskip{\centering %s\par}" % taula(['1', '2', '4', '', '10'], ['', '13', '', '45,50', ''], 'Entradas', 'Precio (€)'),
     r"Constante: $13:2=\res{6,50}$\,€ por entrada.\par\smallskip{\centering %s\par}" % taula(['1', '2', '4', r'$\res{7}$', '10'], [r'$\res{6,50}$', '13', r'$\res{26}$', '45,50', r'$\res{65}$'], 'Entradas', 'Precio (€)')),
 (1, r"Indica si son directamente proporcionales:" + tasks(2, ["Las barras de pan que compramos y el precio que pagamos.", "La edad de una persona y su altura.", "El lado de un cuadrado y su perímetro.", "Los litros de gasolina y los km recorridos (con el mismo coche)."]),
     tasks(2, [r"\rest{Sí}", r"\rest{No}: aumentan juntas pero no en la misma proporción.", r"\rest{Sí}: perímetro $=4\cdot$ lado.", r"\rest{Sí}"])),
 (1, r"Si 4 bolígrafos cuestan $3,20$\,€, ¿cuánto cuestan 9 bolígrafos? ¿Y 15?",
     r"Un bolígrafo: $3,20:4=0,80$\,€. \ 9 bolígrafos: $\res{7,20\text{\,€}}$; \ 15 bolígrafos: $\res{12\text{\,€}}$."),
 (2, r"Un coche gasta $6,5$ L de gasolina cada 100 km. ¿Cuántos litros gastará en un viaje de 340 km?",
     r"$\begin{array}{rcl}100\text{ km}&\to&6,5\text{ L}\\340\text{ km}&\to&x\end{array}\qquad x=%s=\res{22,1\text{ L}}$" % fr(r'6,5\cdot340', 100)),
 (2, r"Un grifo llena 120 L en 8 minutos. ¿Cuánto tardará en llenar un depósito de 450 L? ¿Cuántos litros habrá echado en media hora?",
     r"$x=%s=\res{30\text{ min}}$. \ En 30 min, $120:8=15$ L/min, \ $15\cdot30=\res{450\text{ L}}$ (justo el depósito)." % fr(r'8\cdot450', 120)),
 (2, r"Una receta de bizcocho para 6 personas lleva 250 g de harina, 4 huevos y $0,15$ L de leche. ¿Qué cantidades necesitamos para 9 personas?",
     r"Multiplicamos por $9:6=1,5$: \ $\res{375\text{ g}}$ de harina, \ $\res{6}$ huevos \ y \ $\res{0,225\text{ L}}$ de leche."),
 (3, r"En un mapa, 2 cm representan 15 km reales. ¿Qué distancia real hay entre dos ciudades que en el mapa están a $9,4$ cm? ¿A cuántos cm del mapa están dos pueblos separados por 6 km?",
     r"1 cm $\to 7,5$ km. \ $9,4\cdot7,5=\res{70,5\text{ km}}$; \ $6:7,5=\res{0,8\text{ cm}}$."),
 (3, r"Un taxi cobra 3\,€ por subir y $1,20$\,€ por km. Completa la tabla y di si el precio es directamente proporcional a los km.\par\smallskip{\centering %s\par}" % taula(['1', '2', '5', '10'], ['', '', '', ''], 'km', 'Precio (€)'),
     r"\par\smallskip{\centering %s\par}\smallskip \rest{No es proporcional}: $%s\neq%s$ (el doble de km no cuesta el doble)." % (taula(['1', '2', '5', '10'], ['4,20', '5,40', '9', '15'], 'km', 'Precio (€)'), fr('4,20', 1), fr('5,40', 2))),
]))
ck(Dm(13) / 2, '6.5'); ck(Dm('45.50') / Dm('6.5'), '7'); ck(Dm('3.20') / 4 * 9, '7.2'); ck(Dm('3.20') / 4 * 15, '12')
ck(Dm('6.5') * 340 / 100, '22.1'); ck(Fr(8 * 450, 120), 30); ck(250 * Dm('1.5'), '375'); ck(Dm('0.15') * Dm('1.5'), '0.225')
ck(Dm('9.4') * Dm('7.5'), '70.5'); ck(Dm(6) / Dm('7.5'), '0.8')
for k, v in [(1, '4.2'), (2, '5.4'), (5, '9'), (10, '15')]: ck(3 + Dm('1.2') * k, v)

# =====================================================================
S.append(("Proporcionalidad inversa", [
 (1, r"Completa la tabla de proporcionalidad inversa y calcula la constante:\par\smallskip{\centering %s\par}" % taula(['40', '60', '80', '', '120'], ['6', '', '', '2,5', ''], 'Velocidad (km/h)', 'Tiempo (h)'),
     r"Constante: $40\cdot6=\res{240}$ (la distancia).\par\smallskip{\centering %s\par}" % taula(['40', '60', '80', r'$\res{96}$', '120'], ['6', r'$\res{4}$', r'$\res{3}$', '2,5', r'$\res{2}$'], 'Velocidad (km/h)', 'Tiempo (h)')
),
 (1, r"Indica si son directamente proporcionales, inversamente proporcionales o ninguna de las dos cosas:" + tasks(2, ["El número de obreros y el tiempo que tardan en hacer una pared.", "Los litros de pintura y los m$^2$ pintados.", "El número de amigos que pagan un regalo y lo que paga cada uno.", "El peso de una persona y su edad."]),
     tasks(2, [r"\rest{Inversa}", r"\rest{Directa}", r"\rest{Inversa}", r"\rest{Ninguna de las dos}"])),
 (1, r"Si 3 grifos llenan una piscina en 10 horas, ¿cuánto tardarán 5 grifos iguales? ¿Y 2 grifos?",
     r"Un grifo: $3\cdot10=30$ h. \ 5 grifos: $30:5=\res{6\text{ h}}$; \ 2 grifos: $30:2=\res{15\text{ h}}$."),
 (2, r"Un grupo de 12 personas tiene comida para 30 días. Si se añaden 8 más, ¿para cuántos días tendrán comida?",
     r"$\begin{array}{rcl}12\text{ pers.}&\to&30\text{ días}\\20\text{ pers.}&\to&x\end{array}\qquad x=%s=\res{18\text{ días}}$" % fr(r'12\cdot30', 20)),
 (2, r"Un tren a 90 km/h tarda 2 horas en hacer un trayecto. ¿Cuánto tardaría a 120 km/h? ¿A qué velocidad tendría que ir para tardar 3?",
     r"$x=%s=\res{1,5\text{ h}}$ (1 h 30 min). \ Velocidad: $%s=\res{60\text{ km/h}}$." % (fr(r'90\cdot2', 120), fr(r'90\cdot2', 3))),
 (3, r"5 máquinas hacen un trabajo en 12 horas. ¿Cuántas máquinas hacen falta para hacerlo en 4 horas? Si solo tenemos 3, ¿cuánto tardarán?",
     r"Inversa: $%s=\res{15\text{ máquinas}}$. \ Con 3: $%s=\res{20\text{ h}}$." % (fr(r'5\cdot12', 4), fr(r'5\cdot12', 3))),
 (3, r"Para repartir el agua de un depósito hacen falta 60 garrafas de 5 L. ¿Cuántas garrafas de $1,5$ L harían falta? Si solo tenemos 25 garrafas iguales, ¿de qué capacidad tendrían que ser?",
     r"Capacidad: $60\cdot5=300$ L. \ $300:1,5=\res{200\text{ garrafas}}$; \ $300:25=\res{12\text{ L}}$."),
]))
ck(Fr(240, Fr(5, 2)), 96); ck(Fr(30, 5), 6); ck(Fr(30, 2), 15); ck(Fr(360, 20), 18); ck(Dm(180) / 120, '1.5'); ck(Fr(180, 3), 60); ck(Fr(60, 4), 15); ck(Fr(60, 3), 20); ck(Dm(300) / Dm('1.5'), '200')

# =====================================================================
PFD = [(40, '2/5', '0.4'), (5, '1/20', '0.05'), (75, '3/4', '0.75'), (12, '3/25', '0.12'), (120, '6/5', '1.2'), (2.5, '1/40', '0.025')]
PCT = [(20, 45), (75, 120), (15, 60), (8, 350), (12, 250), (7.5, 60)]
S.append(("Porcentajes", [
 (1, r"Completa la tabla:\par\smallskip{\centering\renewcommand{\arraystretch}{1.5}\begin{tabular}{|c|C{2.4cm}|C{2.4cm}|}\hline Porcentaje & Fracción irreducible & Decimal\\\hline "
     + r'\\\hline '.join(r'$%s\,\%%$ & & ' % num(str(p)) for p, _, _ in PFD) + r'\\\hline\end{tabular}\par}',
     r"\par\smallskip{\centering\renewcommand{\arraystretch}{1.5}\begin{tabular}{|c|C{2.4cm}|C{2.4cm}|}\hline Porcentaje & Fracción irreducible & Decimal\\\hline "
     + r'\\\hline '.join(r'$%s\,\%%$ & $\res{%s}$ & $\res{%s}$' % (num(str(p)), fr(*f.split('/')), num(d)) for p, f, d in PFD) + r'\\\hline\end{tabular}\par}'),
 (1, r"Calcula:" + tasks(3, [r'El $%s\,\%%$ de $%s$' % (num(str(p)), n) for p, n in PCT])
     + recorda(r"El $p\,\%$ de $N$ es $N\cdot\dfrac{p}{100}$. Por ejemplo, el $35\,\%$ de $80$ es $80\cdot0,35=28$."),
     tasks(3, [r'$%s\cdot%s=\res{%s}$' % (n, fmt(Dm(str(p)) / 100), fmt(Dm(str(p)) * n / 100)) for p, n in PCT])),
 (1, r"Expresa en porcentaje:" + tasks(6, ['$%s$' % x for x in [r'0,35', r'0,06', r'1,5', fr(3, 5), fr(7, 20), fr(1, 8)]]),
     tasks(6, [r'$\res{35\,\%}$', r'$\res{6\,\%}$', r'$\res{150\,\%}$', r'$\res{60\,\%}$', r'$\res{35\,\%}$', r'$\res{12,5\,\%}$'])),
 (2, r"En un instituto de 650 alumnos, 91 vienen en bicicleta. ¿Qué porcentaje representan? ¿Y en una clase de 25 alumnos, si 6 llevan gafas?",
     r"$%s=0,14=\res{14\,\%%}$; \qquad $%s=0,24=\res{24\,\%%}$." % (fr(91, 650), fr(6, 25))),
 (2, r"En una clase de 28 alumnos, el $25\,\%$ ha sacado sobresaliente y el $50\,\%$ notable. ¿Cuántos alumnos han sacado cada nota? ¿Qué porcentaje no ha sacado ni sobresaliente ni notable?",
     r"Sobresaliente: $28\cdot0,25=\res{7}$; \ notable: $28\cdot0,5=\res{14}$; \ el resto: $100-75=\res{25\,\%}$ (7 alumnos)."),
 (3, r"Hemos leído 135 páginas de un libro, que son el $45\,\%$ del total. ¿Cuántas páginas tiene el libro?",
     r"$135:0,45=13\,500:45=\res{300\text{ páginas}}$. \ Comprobación: $300\cdot0,45=135$."),
 (3, r"¿Qué es más, el $30\,\%$ de 50 o el $50\,\%$ de 30? ¿Y el $20\,\%$ de 80 o el $80\,\%$ de 20? Explica por qué pasa.",
     r"$50\cdot0,3=15=30\cdot0,5$ \ y \ $80\cdot0,2=16=20\cdot0,8$: \rest{son iguales}. \ Siempre pasa porque $%s=%s$ (el orden de los factores no altera el producto)." % (fr(r'30\cdot50', 100), fr(r'50\cdot30', 100))),
]))
for p, f, d in PFD: assert Fr(Dm(str(p))) / 100 == Fr(f) == Fr(d)
ck(Dm(91) / 650, '0.14'); ck(Dm(6) / 25, '0.24'); ck(28 * Dm('0.25'), '7'); ck(Dm(135) / Dm('0.45'), '300'); ck(Fr(1, 8) * 100, Fr(25, 2))

# =====================================================================
IDX = [('aumento del 30 %', '1.3'), ('disminución del 8 %', '0.92'), ('aumento del 4 %', '1.04'), ('rebaja del 50 %', '0.5'), ('IVA del 21 %', '1.21'), ('descuento del 15 %', '0.85')]
VAR = [('80', '-', 15), ('50', '+', 21), ('650', '-', 12), ('18', '+', 4), ('2400', '+', 5), ('64.90', '-', 30)]
def fv(q, s, p): return Dm(q) * (1 + (Dm(p) / 100 if s == '+' else -Dm(p) / 100))
S.append(("Aumentos y disminuciones porcentuales", [
 (1, r"Escribe el índice de variación:" + tasks(3, [a.replace('%', r'\%') for a, _ in IDX])
     + recorda(r"Aumento del $p\,\%%$: multiplicamos por $1+%s$. \ Disminución del $p\,\%%$: multiplicamos por $1-%s$." % (fr('p', 100), fr('p', 100))),
     tasks(3, [r'%s: $\res{%s}$' % (a.replace('%', r'\%'), num(i)) for a, i in IDX])),
 (1, r"Calcula la cantidad final:" + tasks(2, [r'$%s$\,€ con %s del $%d\,\%%$' % (num(q), 'una subida' if s == '+' else 'un descuento', p) for q, s, p in VAR]),
     tasks(2, [r'$%s\cdot%s=\res{%s}$\,€' % (num(q), fmt(1 + (Dm(p) / 100 if s == '+' else -Dm(p) / 100)), eur(fv(q, s, p))) for q, s, p in VAR])),
 (2, r"Una camiseta pasa de 25\,€ a 20\,€. ¿Qué porcentaje de descuento le han hecho? ¿Y si un abrigo pasa de 120\,€ a 138\,€, qué porcentaje ha subido?",
     r"Descuento: $5$\,€, \ $%s=0,2=\res{20\,\%%}$. \ Subida: $18$\,€, \ $%s=0,15=\res{15\,\%%}$." % (fr(5, 25), fr(18, 120))),
 (2, r"En una tienda, un televisor cuesta 450\,€ sin IVA. ¿Cuánto cuesta con el IVA del 21\,\%? Si además nos hacen un descuento del 10\,\% sobre el precio con IVA, ¿cuánto pagamos?",
     r"Con IVA: $450\cdot1,21=\res{544,50\text{\,€}}$. \ Con descuento: $544,50\cdot0,9=\res{490,05\text{\,€}}$."),
 (3, r"Después de aplicar el IVA del 21\,\%, una factura es de $108,90$\,€. ¿Cuánto valía sin IVA? ¿Y si después de una rebaja del 15\,\% pagamos 68\,€, cuál era el precio inicial?",
     r"$108,90:1,21=\res{90\text{\,€}}$; \qquad $68:0,85=\res{80\text{\,€}}$."),
 (3, r"El precio de un patinete de 200\,€ sube un 10\,\% y, al cabo de un mes, baja un 10\,\%. ¿Cuánto cuesta al final? ¿Vuelve al precio inicial? ¿Qué pasaría si primero bajara un 20\,\% y después subiera un 20\,\%?",
     r"$200\cdot1,1=220$; \ $220\cdot0,9=\res{198\text{\,€}}$: no vuelve a 200\,€. \ Con $-20\,\%$ y $+20\,\%$: $200\cdot0,8\cdot1,2=\res{192\text{\,€}}$ (un 4\,\% menos)."),
 (3, r"La población de un pueblo era de 2400 habitantes. El primer año aumenta un 5\,\% y el segundo año disminuye un 5\,\%. ¿Cuántos habitantes tiene al final? ¿Qué porcentaje ha variado respecto al inicio?",
     r"$2400\cdot1,05=2520$; \ $2520\cdot0,95=\res{2394}$ habitantes. \ Variación: $%s=0,9975$: \ ha disminuido un $\res{0,25\,\%%}$." % fr(2394, 2400)),
]))
ck(Dm(5) / 25, '0.2'); ck(Dm(18) / 120, '0.15'); ck(450 * Dm('1.21'), '544.5'); ck(Dm('544.50') * Dm('0.9'), '490.05')
ck(Dm('108.90') / Dm('1.21'), '90'); ck(Dm(68) / Dm('0.85'), '80'); ck(200 * Dm('1.1') * Dm('0.9'), '198'); ck(200 * Dm('0.8') * Dm('1.2'), '192')
ck(2400 * Dm('1.05') * Dm('0.95'), '2394'); ck(Dm(2394) / 2400, '0.9975')
assert [eur(fv(*v)) for v in VAR] == ['68', '60,50', '572', '18,72', '2520', '45,43']

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TIT = 'Proporcionalidad y porcentajes. Números decimales'

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 5: %s' % (t, TIT), capcalera='%s · Unidad 5' % t,
                 pdfkeywords='números decimales, aproximación, operaciones con decimales, decimales y fracciones, razones, proporciones, proporcionalidad directa, proporcionalidad inversa, regla de tres, porcentajes',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 5' if sol else 'Ficha de ejercicios · Unidad 5') + '}{' + TIT + '}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad. Recuerda que las fracciones se tienen que dar en forma irreducible y los precios, redondeados a los céntimos."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Las tablas y las rectas se pueden completar directamente en la ficha. Haz los cálculos sin calculadora.") + r'''
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
    name = 't5-fitxa-solucions-es.tex' if sol else 't5-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios,', len(CHK), 'comprobaciones')
