# Genera t5-fitxa-exercicis.tex i t5-fitxa-solucions.tex
# (1r ESO, Unitat 5: Proporcionalitat i percentatges. Nombres decimals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les operacions es calculen amb Decimal/Fraction (val/ops) i les asserts de CHK comproven
# els resultats escrits a mà.
import os, re
from decimal import Decimal as Dm, getcontext, ROUND_HALF_UP, ROUND_DOWN
from fractions import Fraction as Fr
getcontext().prec = 40
HERE = os.path.dirname(os.path.abspath(__file__))

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
    if dd == 1: return 'exacte'
    return 'periòdic pur' if per(n, d).split(',')[1].startswith(r'\overline') else 'periòdic mixt'
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
LECT = [('7.25', '7 unitats i 25 centèsimes'), ('0.408', '408 mil·lèsimes'), ('12.06', '12 unitats i 6 centèsimes'), ('3.5', '3 unitats i 5 dècimes'), ('100.001', '100 unitats i 1 mil·lèsima'), ('0.09', '9 centèsimes')]
ESCR = [('tres unitats i quaranta-cinc mil·lèsimes', '3.045'), ('dotze centèsimes', '0.12'), ('vint unitats i nou dècimes', '20.9'), ('set mil·lèsimes', '0.007'), ('cent unitats i cinc centèsimes', '100.05'), ('quatre unitats i tres-centes mil·lèsimes', '4.300')]
VALX = [('34.571', '7', '7 centèsimes = 0,07'), ('2.738', '3', '3 centèsimes = 0,03'), ('607.15', '7', '7 unitats'), ('0.0809', '8', '8 centèsimes = 0,08'), ('15.4', '4', '4 dècimes = 0,4'), ('9.206', '6', '6 mil·lèsimes = 0,006')]
S.append(("Nombres decimals", [
 (1, r"Escriu com es llegeixen aquests nombres:" + tasks(3, ['$%s$' % num(a) for a, _ in LECT])
     + recorda(r"Llegim la part entera, la paraula \emph{unitats} i la part decimal amb el nom de l'\textbf{última} xifra: $3,045$ són 3 unitats i 45 mil·lèsimes."),
     tasks(2, ['$%s$: %s' % (num(a), b) for a, b in LECT])),
 (1, r"Escriu amb xifres:" + tasks(2, [a.capitalize() for a, _ in ESCR]),
     tasks(3, [r'$\res{%s}$' % num(b) for _, b in ESCR])),
 (1, r"Quant val la xifra indicada en cada nombre?" + tasks(3, [r'El %s en $%s$' % (d, num(x)) for x, d, _ in VALX]),
     tasks(2, [r'El %s en $%s$: %s' % (d, num(x), v) for x, d, v in VALX])),
 (2, r"Completa:" + tasks(2, [r"$1$ unitat $=$ \rule{1cm}{0.4pt} dècimes", r"$1$ dècima $=$ \rule{1cm}{0.4pt} centèsimes", r"$3$ unitats $=$ \rule{1cm}{0.4pt} centèsimes", r"$45$ centèsimes $=$ \rule{1cm}{0.4pt} unitats", r"$250$ mil·lèsimes $=$ \rule{1cm}{0.4pt} dècimes", r"$7$ dècimes $=$ \rule{1cm}{0.4pt} mil·lèsimes"]),
     tasks(3, [r"$\res{10}$ dècimes", r"$\res{10}$ centèsimes", r"$\res{300}$ centèsimes", r"$\res{0,45}$ unitats", r"$\res{2,5}$ dècimes", r"$\res{700}$ mil·lèsimes"])),
 (2, r"Descompon cada nombre segons el valor de les seues xifres:" + tasks(3, ['$%s$' % num(x) for x in ['45.312', '7.09', '120.506']]),
     tasks(1, [r'$45,312=40+5+0,3+0,01+0,002$', r'$7,09=7+0,09$', r'$120,506=100+20+0,5+0,006$'])),
 (3, r"Escriu el nombre que té: a) 4 desenes, 6 dècimes i 2 mil·lèsimes; \ b) 8 centenes, 3 unitats i 5 centèsimes; \ c) 15 centèsimes i 3 mil·lèsimes. Quin d'aquests és igual a $0,15$: \ $0,150$, \ $0,015$ o \ $0,1500$?",
     r"a) $\res{40,602}$ \quad b) $\res{803,05}$ \quad c) $\res{0,153}$. \ Són iguals a $0,15$: $\res{0,150}$ i $\res{0,1500}$ (els zeros finals no canvien el valor)."),
]))
ck(Dm('40') + Dm('0.6') + Dm('0.002'), '40.602'); ck(800 + 3 + Dm('0.05'), '803.05'); ck(Dm('0.15') + Dm('0.003'), '0.153')
ck(40 + 5 + Dm('0.3') + Dm('0.01') + Dm('0.002'), '45.312'); ck(100 + 20 + Dm('0.5') + Dm('0.006'), '120.506')

# =====================================================================
CMP = [('4.7', '4.68'), ('0.09', '0.1'), ('5.307', '5.37'), ('12.5', '12.50'), ('3.099', '3.1'), ('0.45', '0.405')]
def sym(a, b): c = Dm(a) - Dm(b); return '<' if c < 0 else '>' if c > 0 else '='
ORD = ['2.5', '2.05', '2.55', '2.505', '2.0', '2.15']
ROUND = ['3.4682', '15.8962', '0.7049', '29.996']
S.append(("Comparar, representar i aproximar decimals", [
 (1, r"Escriu $<$, $>$ o $=$:" + tasks(3, [r'$%s\ \square\ %s$' % (num(a), num(b)) for a, b in CMP])
     + recorda(r"Per a comparar, igualem el nombre de decimals afegint zeros: $\ 3,5\ \text{?}\ 3,48\ \to\ 3,50>3,48$."),
     tasks(3, [r'$%s\ \res{%s}\ %s$' % (num(a), sym(a, b), num(b)) for a, b in CMP])),
 (1, r"Ordena de menor a major: \ $%s$" % ';\\ '.join(num(x) for x in ORD),
     r"$\res{%s}$" % '<'.join(num(x) for x in sorted(ORD, key=Dm))),
 (2, r"Escriu el nombre decimal que correspon a cada punt:\par\smallskip{\centering %s\par}" % tz_line(3, 4, 10, [(3.2, 'A'), (3.7, 'B'), (3.9, 'C')]) + r"\par\smallskip{\centering %s\par}" % tz_line(0.5, 0.6, 10, [(0.53, 'D'), (0.58, 'E')], k=2),
     r"A $=\res{3,2}$, \ B $=\res{3,7}$, \ C $=\res{3,9}$, \ D $=\res{0,53}$, \ E $=\res{0,58}$."),
 (2, r"Representa en la recta $1,4$ \ i \ $1,75$ (la recta va de 1 a 2).\par\smallskip{\centering %s\par}" % tz_line(1, 2, 20),
     r"Dividim la unitat en 20 parts (cada una val $0,05$):\par\smallskip{\centering %s\par}" % tz_line(1, 2, 20, [(1.4, '$1,4$'), (1.75, '$1,75$')])),
 (2, r"Escriu tres nombres decimals compresos entre:" + tasks(3, [r'$0,3$ i $0,4$', r'$2,71$ i $2,72$', r'$5$ i $5,1$']),
     tasks(3, [r'Per exemple $0,31$; $0,35$; $0,39$', r'Per exemple $2,711$; $2,715$; $2,719$', r'Per exemple $5,01$; $5,05$; $5,09$']) + r"\par (Hi ha infinites respostes.)"),
 (2, r"Completa la taula aproximant cada nombre:\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.3cm}|C{2.3cm}|C{2.3cm}|}\hline Nombre & Truncat a les centèsimes & Arrodonit a les dècimes & Arrodonit a les centèsimes\\\hline "
     + r'\\\hline '.join('$%s$ & & & ' % num(x) for x in ROUND) + r'\\\hline\end{tabular}\par}'
     + recorda(r"Per a \textbf{arrodonir}, mirem la primera xifra que eliminem: si és $0,1,2,3,4$ la deixem igual; si és $5,6,7,8,9$ sumem 1 a l'última xifra que queda."),
     r"\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.3cm}|C{2.3cm}|C{2.3cm}|}\hline Nombre & Truncat a les centèsimes & Arrodonit a les dècimes & Arrodonit a les centèsimes\\\hline "
     + r'\\\hline '.join(r'$%s$ & $%s$ & $\res{%s}$ & $\res{%s}$' % (num(x), num(str(trn(x, 2))), num(str(rnd(x, 1))), num(str(rnd(x, 2)))) for x in ROUND) + r'\\\hline\end{tabular}\par}'),
 (3, r"Un article costa $12,4583$\,€ segons la calculadora. Quant pagarem? Escriu un nombre que, arrodonit a les dècimes, siga $2,5$ i que siga menor que $2,5$. Quin és el nombre més xicotet amb dues xifres decimals que arrodonit a les unitats dona 8?",
     r"Arrodonim a cèntims: $\res{12,46\text{\,€}}$. \ Per exemple $\res{2,47}$ (qualsevol des de $2,45$ fins a $2,5$ sense arribar-hi). \ El més xicotet és $\res{7,50}$."),
]))
ck(rnd('12.4583', 2), '12.46'); ck(rnd('7.50', 0), '8'); ck(rnd('7.49', 0), '7')
assert [rnd(x, 2) for x in ROUND] == [Dm('3.47'), Dm('15.90'), Dm('0.70'), Dm('30.00')]

# =====================================================================
SUM = ['23.45+7.8', '40-12.35', '0.9+0.35', '15-6.47', '3.06+12.9+0.4', '100-0.01']
MUL = ['4.6*3', '2.35*0.4', '0.6*0.05', '12.5*1.2', '3.25*1.4', '0.07*0.3']
P10 = ['3.7*100', '0.052*1000', '45.2:1000', '8:100', '6.15*10', '0.3:10', '250*0.1', '1.4*0.01']
S.append(("Sumar, restar i multiplicar decimals", [
 (1, r"Calcula:" + tasks(3, [op(e) for e in SUM])
     + recorda(r"Per a sumar i restar, col·loquem les \textbf{comes alineades} i completem amb zeros."),
     tasks(3, [ops(e) for e in SUM])),
 (1, r"Calcula:" + tasks(3, [op(e) for e in MUL])
     + recorda(r"Per a multiplicar, ho fem com si no hi haguera comes i separem tants decimals com \textbf{sumen} els dos factors."),
     tasks(3, [ops(e) for e in MUL])),
 (1, r"Calcula mentalment:" + tasks(4, [op(e) for e in P10]),
     tasks(4, [ops(e) for e in P10])),
 (2, r"Col·loca la coma en el resultat sense fer l'operació: \ $3,8\cdot2,5=950$; \ $0,45\cdot1,2=540$; \ $12,6\cdot0,03=378$. Comprova-ho estimant.",
     r"$3,8\cdot2,5=\res{9,50}$ (prop de $4\cdot2=8$); \ $0,45\cdot1,2=\res{0,540}$ (prop de $0,5$); \ $12,6\cdot0,03=\res{0,378}$ (2+1 decimals sumen 3)."),
 (2, r"Completa amb el nombre que falta:" + tasks(3, [r'$2,75+\square=5$', r'$\square-1,8=3,45$', r'$0,6\cdot\square=60$']),
     tasks(3, [r'$\res{2,25}$', r'$\res{5,25}$', r'$\res{100}$'])),
 (2, r"Comprem $2,5$ kg de pomes a $1,80$\,€/kg i $1,5$ kg de cireres a $6,40$\,€/kg. Paguem amb un bitllet de 20\,€. Quant ens tornen?",
     r"Pomes: $2,5\cdot1,80=4,50$\,€; \ cireres: $1,5\cdot6,40=9,60$\,€; \ total $14,10$\,€. \ Ens tornen $20-14,10=\res{5,90\text{\,€}}$."),
 (3, r"Una piscina fa $25$ m de llarg. La Laia fa $8$ llargs i el seu germà, $5,5$ llargs. Quants metres més ha nadat la Laia? Si la Laia nada cada llarg en $0,45$ minuts, quant tarda en total?",
     r"Laia: $25\cdot8=200$ m; \ germà: $25\cdot5,5=137,5$ m; \ diferència $\res{62,5\text{ m}}$. \ Temps: $8\cdot0,45=\res{3,6\text{ minuts}}$."),
 (3, r"El perímetre d'un triangle és $17,25$ cm. Dos costats mesuren $4,8$ cm i $6,07$ cm. Quant mesura el tercer costat? Quant mesuraria el perímetre d'un triangle amb tots els costats 10 vegades més llargs?",
     r"Tercer costat: $17,25-(4,8+6,07)=17,25-10,87=\res{6,38\text{ cm}}$. \ Perímetre: $17,25\cdot10=\res{172,5\text{ cm}}$."),
]))
ck(Dm('3.8') * Dm('2.5'), '9.5'); ck(Dm('0.45') * Dm('1.2'), '0.54'); ck(Dm('12.6') * Dm('0.03'), '0.378')
ck(5 - Dm('2.75'), '2.25'); ck(Dm('3.45') + Dm('1.8'), '5.25'); ck(Dm(60) / Dm('0.6'), '100')
ck(Dm('2.5') * Dm('1.80') + Dm('1.5') * Dm('6.40'), '14.10'); ck(25 * 8 - 25 * Dm('5.5'), '62.5'); ck(8 * Dm('0.45'), '3.6')
ck(Dm('17.25') - Dm('4.8') - Dm('6.07'), '6.38')

# =====================================================================
DIV1 = ['8.4:4', '9.75:3', '6.24:3', '0.8:2', '15.3:5', '1.26:6']
DIV2 = ['7:4', '15:8', '9:4', '3:5', '1:8', '21:12']
DIV3 = ['4.5:0.9', '2.73:0.7', '6:0.12', '12.6:0.35', '1.44:1.2', '0.9:0.03']
S.append(("Dividir amb decimals", [
 (1, r"Calcula:" + tasks(3, [op(e) for e in DIV1]),
     tasks(3, [ops(e) for e in DIV1])),
 (1, r"Calcula traient decimals al quocient fins que la divisió siga exacta:" + tasks(3, [op(e) for e in DIV2])
     + recorda(r"Si sobra residu, posem una coma al quocient, afegim un 0 al residu i continuem dividint."),
     tasks(3, [ops(e) for e in DIV2])),
 (2, r"Calcula (si el divisor té decimals, multiplica dividend i divisor per 10, 100…):" + tasks(3, [op(e) for e in DIV3]),
     tasks(3, ['$%s=%s=\\res{%s}$' % (tx(e), tx(conv), fmt(val(e))) for e, conv in zip(DIV3, ['45:9', '27.3:7', '600:12', '1260:35', '14.4:12', '90:3'])])),
 (2, r"Calcula amb dues xifres decimals i indica el residu: \ a) $10:3$ \quad b) $5:7$ \quad c) $25,4:6$",
     r"a) $\res{3,33}$, residu $0,01$ \quad b) $\res{0,71}$, residu $0,03$ \quad c) $\res{4,23}$, residu $0,02$."),
 (2, r"Amb una botella de $1,5$ L, quants gots de $0,25$ L podem omplir? I amb una garrafa de 5 L?",
     r"$1,5:0,25=150:25=\res{6\text{ gots}}$; \ $5:0,25=500:25=\res{20\text{ gots}}$."),
 (3, r"Un tros de formatge de $0,85$ kg costa $11,39$\,€. Quin és el preu d'un quilo? Quant costaria un tros de $1,2$ kg?",
     r"$11,39:0,85=1139:85=\res{13,40\text{\,€/kg}}$. \ $1,2\cdot13,40=\res{16,08\text{\,€}}$."),
 (3, r"Un cotxe ha gastat $31,5$ L de gasolina en un viatge de 450 km. Quants litres gasta cada 100 km? Si la gasolina costa $1,56$\,€/L, quant ha costat el viatge?",
     r"$31,5:4,5=\res{7\text{ L}}$ cada 100 km. \ Cost: $31,5\cdot1,56=\res{49,14\text{\,€}}$."),
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
S.append(("Decimals i fraccions", [
 (1, r"Escriu com a fracció decimal i després com a fracció irreductible:" + tasks(4, ['$%s$' % num(x) for x in D2F])
     + recorda(r"Al numerador posem el nombre sense coma; al denominador, un 1 seguit de tants zeros com decimals té: \ $0,35=%s=%s$." % (fr(35, 100), fr(7, 20))),
     tasks(4, [r'$%s=%s=\res{%s}$' % (num(x), fr(Dm(x).scaleb(len(x.split('.')[1])).to_integral(), 10 ** len(x.split('.')[1])), ftex(Fr(x))) for x in D2F])),
 (1, r"Escriu en forma decimal:" + tasks(4, ['$%s$' % fr(n, 10 ** k) for n, k in [(7, 1), (35, 2), (4, 3), (125, 2)]]),
     tasks(4, [r'$\res{0,7}$', r'$\res{0,35}$', r'$\res{0,004}$', r'$\res{1,25}$'])),
 (2, r"Escriu en forma decimal i classifica en exacte, periòdic pur o periòdic mixt:" + tasks(4, ['$%s$' % fr(n, d) for n, d in F2D])
     + recorda(r"Dividim el numerador entre el denominador. Si les xifres es repeteixen, el decimal és \textbf{periòdic} i marquem el període: \ $%s=0,8333\ldots=0,8\overline{3}$." % fr(5, 6)),
     tasks(2, [r'$%s=\res{%s}$ \ (%s)' % (fr(n, d), per(n, d), kind(n, d)) for n, d in F2D])),
 (2, r"Ordena de menor a major passant-ho tot a decimal: \ $0,7;\ \ %s;\ \ 0,67;\ \ %s;\ \ 0,6$" % (fr(2, 3), fr(3, 4)),
     r"$%s=0,\overline{6}$ \ i \ $%s=0,75$: \qquad $0,6<\res{%s}<0,67<0,7<%s$" % (fr(2, 3), fr(3, 4), fr(2, 3), fr(3, 4))),
 (2, r"Quin és més gran?" + tasks(3, [r'$%s$ o $0,62$' % fr(5, 8), r'$%s$ o $0,33$' % fr(1, 3), r'$%s$ o $1,4$' % fr(7, 5)]),
     tasks(3, [r'$%s=0,625>0,62$' % fr(5, 8), r'$%s=0,333\ldots>0,33$' % fr(1, 3), r'$%s=1,4$: són iguals' % fr(7, 5)])),
 (3, r"Escriu una fracció de denominador 3 compresa entre $1,5$ i $2$, i una fracció de denominador 8 compresa entre $0,3$ i $0,4$.",
     r"$\res{%s}=1,\overline{6}$; \qquad $\res{%s}=0,375$." % (fr(5, 3), fr(3, 8))),
 (3, r"Un pastís es divideix en 8 porcions iguals. La Marta se'n menja $0,25$ del pastís i el Pau 3 porcions. Qui n'ha menjat més? Quina part del pastís queda, en fracció i en decimal?",
     r"Marta: $0,25=%s$ (2 porcions); Pau: $%s=0,375$. \ \rest{El Pau} n'ha menjat més. \ Queda $1-%s-%s=\res{%s=0,375}$." % (fr(2, 8), fr(3, 8), fr(2, 8), fr(3, 8), fr(3, 8))),
]))
for x in D2F: assert Fr(x) == Fr(Dm(x))
assert [kind(n, d) for n, d in F2D] == ['exacte', 'periòdic pur', 'periòdic mixt', 'exacte', 'periòdic pur', 'periòdic mixt', 'exacte', 'periòdic pur']
assert per(5, 9) == r'0,\overline{5}' and per(7, 12) == r'0,58\overline{3}' and per(4, 11) == r'0,\overline{36}' and per(13, 5) == '2,6'
ck(Fr(1) - Fr(2, 8) - Fr(3, 8), Fr(3, 8))

# =====================================================================
S.append(("Raons i proporcions", [
 (1, r"En una cistella hi ha 18 pomes i 24 peres. Calcula la raó entre pomes i peres i la raó entre peres i fruites totals. Què signifiquen?",
     r"Pomes/peres: $%s=\res{%s}=0,75$: per cada 3 pomes hi ha 4 peres. \ Peres/total: $%s=\res{%s}$: 4 de cada 7 fruites són peres." % (fr(18, 24), fr(3, 4), fr(24, 42), fr(4, 7))),
 (1, r"Comprova si formen proporció:" + tasks(4, [r'$%s$ i $%s$' % (fr(*a), fr(*b)) for a, b in [((6, 9), (8, 12)), ((4, 10), (6, 15)), ((2.5, 4), (5, 9)), ((3, 7), (12, 28))]]).replace('2.5', '2,5')
     + recorda(r"$%s=%s$ són proporció si $a\cdot d=b\cdot c$." % (fr('a', 'b'), fr('c', 'd'))),
     tasks(2, [r'$6\cdot12=72=9\cdot8$: \rest{sí}', r'$4\cdot15=60=10\cdot6$: \rest{sí}', r'$2,5\cdot9=22,5\neq4\cdot5=20$: \rest{no}', r'$3\cdot28=84=7\cdot12$: \rest{sí}'])),
 (2, r"Calcula el terme desconegut:" + tasks(3, [r'$%s=%s$' % (fr(*a), fr(*b)) for a, b in [((3, 5), (12, 'x')), (('x', 8), (15, 24)), ((4, 'x'), (10, 25)), (('2,5', 4), ('x', 12)), (('1,2', '0,3'), (8, 'x')), ((7, 'x'), (21, 6))]]),
     tasks(3, [r'$x=%s=\res{%s}$' % (e, r) for e, r in [(fr(r'5\cdot12', 3), '20'), (fr(r'8\cdot15', 24), '5'), (fr(r'4\cdot25', 10), '10'), (fr(r'2,5\cdot12', 4), '7,5'), (fr(r'0,3\cdot8', '1,2'), '2'), (fr(r'7\cdot6', 21), '2')]])),
 (2, r"Per a fer una massa de pizza fan falta 300 g de farina per cada 180 mL d'aigua. Quanta aigua necessitem per a 750 g de farina?",
     r"$%s=%s\ \Rightarrow\ x=%s=\res{450\text{ mL}}$" % (fr(300, 180), fr(750, 'x'), fr(r'180\cdot750', 300))),
 (3, r"La raó entre l'edat d'una mare i la de la seua filla és $%s$. Si la filla té 12 anys, quants en té la mare? I quants anys tenia la mare quan la filla en tenia 4? Es manté la raó?" % fr(7, 2),
     r"$%s=%s\Rightarrow x=\res{42\text{ anys}}$. \ Fa 8 anys: mare 34, filla 4; \ $%s=%s\neq%s$: \rest{la raó no es manté} (les edats no són proporcionals)." % (fr('x', 12), fr(7, 2), fr(34, 4), fr(17, 2), fr(7, 2))),
]))
ck(Fr(5 * 12, 3), 20); ck(Fr(8 * 15, 24), 5); ck(Fr(100, 10), 10); ck(Dm('2.5') * 12 / 4, '7.5'); ck(Dm('0.3') * 8 / Dm('1.2'), '2'); ck(Fr(42, 21), 2)
ck(Fr(180 * 750, 300), 450); ck(Fr(7 * 12, 2), 42)

# =====================================================================
S.append(("Proporcionalitat directa", [
 (1, r"Completa la taula de proporcionalitat directa i calcula la constant de proporcionalitat:\par\smallskip{\centering %s\par}" % taula(['1', '2', '4', '', '10'], ['', '13', '', '45,50', ''], 'Entrades', 'Preu (€)'),
     r"Constant: $13:2=\res{6,50}$\,€ per entrada.\par\smallskip{\centering %s\par}" % taula(['1', '2', '4', r'$\res{7}$', '10'], [r'$\res{6,50}$', '13', r'$\res{26}$', '45,50', r'$\res{65}$'], 'Entrades', 'Preu (€)')),
 (1, r"Indica si són directament proporcionals:" + tasks(2, ["Les barres de pa que comprem i el preu que paguem.", "L'edat d'una persona i la seua altura.", "El costat d'un quadrat i el seu perímetre.", "Els litres de gasolina i els km recorreguts (amb el mateix cotxe)."]),
     tasks(2, [r"\rest{Sí}", r"\rest{No}: augmenten junts però no en la mateixa proporció.", r"\rest{Sí}: perímetre $=4\cdot$ costat.", r"\rest{Sí}"])),
 (1, r"Si 4 bolígrafs costen $3,20$\,€, quant costen 9 bolígrafs? I 15?",
     r"Un bolígraf: $3,20:4=0,80$\,€. \ 9 bolígrafs: $\res{7,20\text{\,€}}$; \ 15 bolígrafs: $\res{12\text{\,€}}$."),
 (2, r"Un cotxe gasta $6,5$ L de gasolina cada 100 km. Quants litres gastarà en un viatge de 340 km?",
     r"$\begin{array}{rcl}100\text{ km}&\to&6,5\text{ L}\\340\text{ km}&\to&x\end{array}\qquad x=%s=\res{22,1\text{ L}}$" % fr(r'6,5\cdot340', 100)),
 (2, r"Una aixeta omple 120 L en 8 minuts. Quant tardarà a omplir un dipòsit de 450 L? Quants litres haurà abocat en mitja hora?",
     r"$x=%s=\res{30\text{ min}}$. \ En 30 min, $120:8=15$ L/min, \ $15\cdot30=\res{450\text{ L}}$ (justament el dipòsit)." % fr(r'8\cdot450', 120)),
 (2, r"Una recepta de pa de pessic per a 6 persones porta 250 g de farina, 4 ous i $0,15$ L de llet. Quines quantitats necessitem per a 9 persones?",
     r"Multipliquem per $9:6=1,5$: \ $\res{375\text{ g}}$ de farina, \ $\res{6}$ ous \ i \ $\res{0,225\text{ L}}$ de llet."),
 (3, r"En un mapa, 2 cm representen 15 km reals. Quina distància real hi ha entre dues ciutats que en el mapa estan a $9,4$ cm? A quants cm del mapa estan dos pobles separats per 6 km?",
     r"1 cm $\to 7,5$ km. \ $9,4\cdot7,5=\res{70,5\text{ km}}$; \ $6:7,5=\res{0,8\text{ cm}}$."),
 (3, r"Un taxi cobra 3\,€ per pujar-hi i $1,20$\,€ per km. Completa la taula i digues si el preu és directament proporcional als km.\par\smallskip{\centering %s\par}" % taula(['1', '2', '5', '10'], ['', '', '', ''], 'km', 'Preu (€)'),
     r"\par\smallskip{\centering %s\par}\smallskip \rest{No és proporcional}: $%s\neq%s$ (el doble de km no costa el doble)." % (taula(['1', '2', '5', '10'], ['4,20', '5,40', '9', '15'], 'km', 'Preu (€)'), fr('4,20', 1), fr('5,40', 2))),
]))
ck(Dm(13) / 2, '6.5'); ck(Dm('45.50') / Dm('6.5'), '7'); ck(Dm('3.20') / 4 * 9, '7.2'); ck(Dm('3.20') / 4 * 15, '12')
ck(Dm('6.5') * 340 / 100, '22.1'); ck(Fr(8 * 450, 120), 30); ck(250 * Dm('1.5'), '375'); ck(Dm('0.15') * Dm('1.5'), '0.225')
ck(Dm('9.4') * Dm('7.5'), '70.5'); ck(Dm(6) / Dm('7.5'), '0.8')
for k, v in [(1, '4.2'), (2, '5.4'), (5, '9'), (10, '15')]: ck(3 + Dm('1.2') * k, v)

# =====================================================================
S.append(("Proporcionalitat inversa", [
 (1, r"Completa la taula de proporcionalitat inversa i calcula la constant:\par\smallskip{\centering %s\par}" % taula(['40', '60', '80', '', '120'], ['6', '', '', '2,5', ''], 'Velocitat (km/h)', 'Temps (h)'),
     r"Constant: $40\cdot6=\res{240}$ (la distància).\par\smallskip{\centering %s\par}" % taula(['40', '60', '80', r'$\res{96}$', '120'], ['6', r'$\res{4}$', r'$\res{3}$', '2,5', r'$\res{2}$'], 'Velocitat (km/h)', 'Temps (h)')
),
 (1, r"Indica si són directament proporcionals, inversament proporcionals o cap de les dues:" + tasks(2, ["El nombre d'obrers i el temps que tarden a fer una paret.", "Els litres de pintura i els m$^2$ pintats.", "El nombre d'amics que paguen un regal i el que paga cadascun.", "El pes d'una persona i la seua edat."]),
     tasks(2, [r"\rest{Inversa}", r"\rest{Directa}", r"\rest{Inversa}", r"\rest{Cap de les dues}"])),
 (1, r"Si 3 aixetes omplin una piscina en 10 hores, quant tardaran 5 aixetes iguals? I 2 aixetes?",
     r"Una aixeta: $3\cdot10=30$ h. \ 5 aixetes: $30:5=\res{6\text{ h}}$; \ 2 aixetes: $30:2=\res{15\text{ h}}$."),
 (2, r"Un grup de 12 persones té menjar per a 30 dies. Si se n'hi afegeixen 8 més, per a quants dies tindran menjar?",
     r"$\begin{array}{rcl}12\text{ pers.}&\to&30\text{ dies}\\20\text{ pers.}&\to&x\end{array}\qquad x=%s=\res{18\text{ dies}}$" % fr(r'12\cdot30', 20)),
 (2, r"Un tren a 90 km/h tarda 2 hores a fer un trajecte. Quant tardaria a 120 km/h? A quina velocitat hauria d'anar per a tardar-ne 3?",
     r"$x=%s=\res{1,5\text{ h}}$ (1 h 30 min). \ Velocitat: $%s=\res{60\text{ km/h}}$." % (fr(r'90\cdot2', 120), fr(r'90\cdot2', 3))),
 (3, r"5 màquines fan una faena en 12 hores. Quantes màquines calen per a fer-la en 4 hores? Si només en tenim 3, quant tardaran?",
     r"Inversa: $%s=\res{15\text{ màquines}}$. \ Amb 3: $%s=\res{20\text{ h}}$." % (fr(r'5\cdot12', 4), fr(r'5\cdot12', 3))),
 (3, r"Per a repartir l'aigua d'un dipòsit fan falta 60 garrafes de 5 L. Quantes garrafes de $1,5$ L farien falta? Si només tenim 25 garrafes iguals, de quina capacitat haurien de ser?",
     r"Capacitat: $60\cdot5=300$ L. \ $300:1,5=\res{200\text{ garrafes}}$; \ $300:25=\res{12\text{ L}}$."),
]))
ck(Fr(240, Fr(5, 2)), 96); ck(Fr(30, 5), 6); ck(Fr(30, 2), 15); ck(Fr(360, 20), 18); ck(Dm(180) / 120, '1.5'); ck(Fr(180, 3), 60); ck(Fr(60, 4), 15); ck(Fr(60, 3), 20); ck(Dm(300) / Dm('1.5'), '200')

# =====================================================================
PFD = [(40, '2/5', '0.4'), (5, '1/20', '0.05'), (75, '3/4', '0.75'), (12, '3/25', '0.12'), (120, '6/5', '1.2'), (2.5, '1/40', '0.025')]
PCT = [(20, 45), (75, 120), (15, 60), (8, 350), (12, 250), (7.5, 60)]
S.append(("Percentatges", [
 (1, r"Completa la taula:\par\smallskip{\centering\renewcommand{\arraystretch}{1.5}\begin{tabular}{|c|C{2.4cm}|C{2.4cm}|}\hline Percentatge & Fracció irreductible & Decimal\\\hline "
     + r'\\\hline '.join(r'$%s\,\%%$ & & ' % num(str(p)) for p, _, _ in PFD) + r'\\\hline\end{tabular}\par}',
     r"\par\smallskip{\centering\renewcommand{\arraystretch}{1.5}\begin{tabular}{|c|C{2.4cm}|C{2.4cm}|}\hline Percentatge & Fracció irreductible & Decimal\\\hline "
     + r'\\\hline '.join(r'$%s\,\%%$ & $\res{%s}$ & $\res{%s}$' % (num(str(p)), fr(*f.split('/')), num(d)) for p, f, d in PFD) + r'\\\hline\end{tabular}\par}'),
 (1, r"Calcula:" + tasks(3, [r'El $%s\,\%%$ de $%s$' % (num(str(p)), n) for p, n in PCT])
     + recorda(r"El $p\,\%$ de $N$ és $N\cdot\dfrac{p}{100}$. Per exemple, el $35\,\%$ de $80$ és $80\cdot0,35=28$."),
     tasks(3, [r'$%s\cdot%s=\res{%s}$' % (n, fmt(Dm(str(p)) / 100), fmt(Dm(str(p)) * n / 100)) for p, n in PCT])),
 (1, r"Expressa en percentatge:" + tasks(6, ['$%s$' % x for x in [r'0,35', r'0,06', r'1,5', fr(3, 5), fr(7, 20), fr(1, 8)]]),
     tasks(6, [r'$\res{35\,\%}$', r'$\res{6\,\%}$', r'$\res{150\,\%}$', r'$\res{60\,\%}$', r'$\res{35\,\%}$', r'$\res{12,5\,\%}$'])),
 (2, r"En un institut de 650 alumnes, 91 vénen amb bicicleta. Quin percentatge representen? I en una classe de 25 alumnes, si 6 porten ulleres?",
     r"$%s=0,14=\res{14\,\%%}$; \qquad $%s=0,24=\res{24\,\%%}$." % (fr(91, 650), fr(6, 25))),
 (2, r"En una classe de 28 alumnes, el $25\,\%$ ha tret excel·lent i el $50\,\%$ notable. Quants alumnes han tret cada nota? Quin percentatge no ha tret ni excel·lent ni notable?",
     r"Excel·lent: $28\cdot0,25=\res{7}$; \ notable: $28\cdot0,5=\res{14}$; \ la resta: $100-75=\res{25\,\%}$ (7 alumnes)."),
 (3, r"Hem llegit 135 pàgines d'un llibre, que són el $45\,\%$ del total. Quantes pàgines té el llibre?",
     r"$135:0,45=13\,500:45=\res{300\text{ pàgines}}$. \ Comprovació: $300\cdot0,45=135$."),
 (3, r"Què és més, el $30\,\%$ de 50 o el $50\,\%$ de 30? I el $20\,\%$ de 80 o el $80\,\%$ de 20? Explica per què passa.",
     r"$50\cdot0,3=15=30\cdot0,5$ \ i \ $80\cdot0,2=16=20\cdot0,8$: \rest{són iguals}. \ Sempre passa perquè $%s=%s$ (l'ordre dels factors no altera el producte)." % (fr(r'30\cdot50', 100), fr(r'50\cdot30', 100))),
]))
for p, f, d in PFD: assert Fr(Dm(str(p))) / 100 == Fr(f) == Fr(d)
ck(Dm(91) / 650, '0.14'); ck(Dm(6) / 25, '0.24'); ck(28 * Dm('0.25'), '7'); ck(Dm(135) / Dm('0.45'), '300'); ck(Fr(1, 8) * 100, Fr(25, 2))

# =====================================================================
IDX = [('augment del 30 %', '1.3'), ('disminució del 8 %', '0.92'), ('augment del 4 %', '1.04'), ('rebaixa del 50 %', '0.5'), ('IVA del 21 %', '1.21'), ('descompte del 15 %', '0.85')]
VAR = [('80', '-', 15), ('50', '+', 21), ('650', '-', 12), ('18', '+', 4), ('2400', '+', 5), ('64.90', '-', 30)]
def fv(q, s, p): return Dm(q) * (1 + (Dm(p) / 100 if s == '+' else -Dm(p) / 100))
S.append(("Augments i disminucions percentuals", [
 (1, r"Escriu l'índex de variació:" + tasks(3, [a.replace('%', r'\%') for a, _ in IDX])
     + recorda(r"Augment del $p\,\%%$: multipliquem per $1+%s$. \ Disminució del $p\,\%%$: multipliquem per $1-%s$." % (fr('p', 100), fr('p', 100))),
     tasks(3, [r'%s: $\res{%s}$' % (a.replace('%', r'\%'), num(i)) for a, i in IDX])),
 (1, r"Calcula la quantitat final:" + tasks(2, [r'$%s$\,€ amb %s del $%d\,\%%$' % (num(q), 'una pujada' if s == '+' else 'un descompte', p) for q, s, p in VAR]),
     tasks(2, [r'$%s\cdot%s=\res{%s}$\,€' % (num(q), fmt(1 + (Dm(p) / 100 if s == '+' else -Dm(p) / 100)), eur(fv(q, s, p))) for q, s, p in VAR])),
 (2, r"Una samarreta passa de 25\,€ a 20\,€. Quin percentatge de descompte li han fet? I si un abric passa de 120\,€ a 138\,€, quin percentatge ha pujat?",
     r"Descompte: $5$\,€, \ $%s=0,2=\res{20\,\%%}$. \ Pujada: $18$\,€, \ $%s=0,15=\res{15\,\%%}$." % (fr(5, 25), fr(18, 120))),
 (2, r"En una botiga, un televisor costa 450\,€ sense IVA. Quant costa amb l'IVA del 21\,\%? Si a més ens fan un descompte del 10\,\% sobre el preu amb IVA, quant paguem?",
     r"Amb IVA: $450\cdot1,21=\res{544,50\text{\,€}}$. \ Amb descompte: $544,50\cdot0,9=\res{490,05\text{\,€}}$."),
 (3, r"Després d'aplicar l'IVA del 21\,\%, una factura és de $108,90$\,€. Quant valia sense IVA? I si després d'una rebaixa del 15\,\% paguem 68\,€, quin era el preu inicial?",
     r"$108,90:1,21=\res{90\text{\,€}}$; \qquad $68:0,85=\res{80\text{\,€}}$."),
 (3, r"El preu d'un patinet de 200\,€ puja un 10\,\% i, al cap d'un mes, baixa un 10\,\%. Quant costa al final? Torna al preu inicial? Què passaria si primer baixara un 20\,\% i després pujara un 20\,\%?",
     r"$200\cdot1,1=220$; \ $220\cdot0,9=\res{198\text{\,€}}$: no torna a 200\,€. \ Amb $-20\,\%$ i $+20\,\%$: $200\cdot0,8\cdot1,2=\res{192\text{\,€}}$ (un 4\,\% menys)."),
 (3, r"La població d'un poble era de 2400 habitants. El primer any augmenta un 5\,\% i el segon any disminueix un 5\,\%. Quants habitants té al final? Quin percentatge ha variat respecte a l'inici?",
     r"$2400\cdot1,05=2520$; \ $2520\cdot0,95=\res{2394}$ habitants. \ Variació: $%s=0,9975$: \ ha disminuït un $\res{0,25\,\%%}$." % fr(2394, 2400)),
]))
ck(Dm(5) / 25, '0.2'); ck(Dm(18) / 120, '0.15'); ck(450 * Dm('1.21'), '544.5'); ck(Dm('544.50') * Dm('0.9'), '490.05')
ck(Dm('108.90') / Dm('1.21'), '90'); ck(Dm(68) / Dm('0.85'), '80'); ck(200 * Dm('1.1') * Dm('0.9'), '198'); ck(200 * Dm('0.8') * Dm('1.2'), '192')
ck(2400 * Dm('1.05') * Dm('0.95'), '2394'); ck(Dm(2394) / 2400, '0.9975')
assert [eur(fv(*v)) for v in VAR] == ['68', '60,50', '572', '18,72', '2520', '45,43']

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={nombres decimals, aproximació, operacions amb decimals, decimals i fraccions, raons, proporcions, proporcionalitat directa, proporcionalitat inversa, regla de tres, percentatges}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
TIT = 'Proporcionalitat i percentatges. Nombres decimals'

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 5: %s. 1r d'ESO}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 5 · 1r d'ESO" % t)
    assert 'Unitat 5' in p and 'unitat 5' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{1r ESO}{''' + ('Solucions de la fitxa · Unitat 5' if sol else "Fitxa d'exercicis · Unitat 5") + r'''}{''' + TIT + r'''}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat. Recorda que les fraccions s'han de donar en forma irreductible i els preus, arrodonits als cèntims."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Les taules i les rectes es poden completar directament en la fitxa. Fes els càlculs sense calculadora.") + r'''
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
    name = 't5-fitxa-solucions.tex' if sol else 't5-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis,', len(CHK), 'comprovacions')
