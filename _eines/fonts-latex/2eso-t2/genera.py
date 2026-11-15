# Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (2n ESO, Unitat 2: Decimals i fraccions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 11 seccions segueixen els apartats dels apunts (2.1-2.11).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Les expressions amb fraccions i decimals s'escriuen en text («1/2-(2/3)^2·3/4», «5.2-1.5·2.4») i el mini-analitzador
# d'aquest fitxer les escriu en TeX, les calcula amb Fraction i en genera els passos de la solució; així no hi pot haver
# errades de càlcul. La resta de resultats escrits a mà es comproven amb ck().
# Ús: python3 genera.py && pdflatex t2-fitxa-exercicis.tex (dues vegades) && pdflatex t2-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re
from fractions import Fraction as Fr
from decimal import Decimal as Dm, ROUND_HALF_UP, ROUND_DOWN
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

CHK = []
def ck(a, b):
    CHK.append((a, b)); assert Fr(a) == Fr(b), (a, b)

def tasks(n, items, gap=None):
    o = '[after-item-skip=%s]' % gap if gap else ''
    return '\\begin{tasks}%s(%d)\n' % (o, n) + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- nombres en TeX ----------
def fd(x):
    """decimal (Fraction o text) -> text amb coma, sense zeros sobrers; espai fi de milers a partir de 5 xifres"""
    x = Dm(x.numerator) / Dm(x.denominator) if isinstance(x, Fr) else Dm(x)
    s = format(x.normalize(), 'f') if x != x.to_integral() else str(int(x))
    neg = s.startswith('-'); s = s.lstrip('-')
    ip, _, fp = s.partition('.')
    if len(ip) > 4: ip = '{:,}'.format(int(ip)).replace(',', '\\,')
    return ('-' if neg else '') + ip + ('{,}' + fp if fp else '')
def exact(f):
    d = Fr(f).denominator
    for p in (2, 5):
        while d % p == 0: d //= p
    return d == 1
def tf(f, big=True):
    """Fraction -> TeX (\\dfrac)"""
    f = Fr(f)
    if f.denominator == 1: return str(f.numerator)
    c = r'\dfrac' if big else r'\frac'
    return ('-' if f < 0 else '') + c + '{%d}{%d}' % (abs(f.numerator), f.denominator)
def per(n, d=1):
    """n/d en decimal amb el període marcat"""
    f = Fr(n, d); neg = f < 0; n, d = abs(f.numerator), f.denominator
    q, r = divmod(n, d); s = ''; seen = {}
    while r and r not in seen:
        seen[r] = len(s); r *= 10; s += str(r // d); r %= d
    out = str(q)
    if not r: out += ('{,}' + s if s else '')
    else:
        i = seen[r]; out += '{,}' + s[:i] + r'\overline{' + s[i:] + '}'
    return ('-' if neg else '') + out
def gen(ent, ante, peri):
    full, part = int(str(ent) + ante + peri), int(str(ent) + ante)
    return Fr(full - part, int('9' * len(peri) + '0' * len(ante)))
def dx(ent, ante, peri): return str(ent) + '{,}' + ante + r'\overline{' + peri + '}'
def kind(f):
    f = Fr(f)
    if exact(f): return T('exacte', 'exacto')
    s = per(f.numerator, f.denominator)
    return T('periòdic pur', 'periódico puro') if '{,}\\overline' in s else T('periòdic mixt', 'periódico mixto')

# ---------- mini-analitzador d'expressions ----------
# nodes: ('n', Fraction, raw) | ('g', '(' o '[', e) | ('w', base, exp) | ('s', [(signe, terme)]) | ('p', [(op, factor)])
def tokens(s):
    s = s.replace(' ', '').replace('*', '·').replace('{', '[').replace('}', ']')
    out, i = [], 0
    while i < len(s):
        m = re.match(r'(\d+(?:\.\d+)?)(?:/(\d+))?', s[i:])
        if m:
            v = Fr(m[1]) / (int(m[2]) if m[2] else 1)
            out.append(('n', v, bool(m[2]) or '.' in m[1])); i += len(m[0]); continue
        assert s[i] in '+-·:^()[]', s
        out.append((s[i],)); i += 1
    return out
def parse(s):
    t = tokens(s); i = [0]
    def pk(): return t[i[0]][0] if i[0] < len(t) else None
    def nx(): i[0] += 1; return t[i[0] - 1]
    def expr():
        terms = []
        sg = '+'
        if pk() == '-': nx(); sg = '-'
        terms.append((sg, term()))
        while pk() in ('+', '-'): sg = nx()[0]; terms.append((sg, term()))
        return terms[0][1] if len(terms) == 1 and terms[0][0] == '+' else ('s', terms)
    def term():
        fs = [('·', power())]
        while pk() in ('·', ':'): op = nx()[0]; fs.append((op, power()))
        return fs[0][1] if len(fs) == 1 else ('p', fs)
    def power():
        b = prim()
        if pk() == '^':
            nx(); e = nx(); assert e[0] == 'n' and e[1].denominator == 1
            assert not (b[0] == 'n' and b[2] and len(b) == 3 and b[1].denominator != 1), 'fracció elevada sense parèntesis: ' + s
            return ('w', b, int(e[1]))
        return b
    def prim():
        k = pk()
        if k == 'n': return nx()
        assert k in ('(', '['), s
        nx(); e = expr(); c = nx()[0]; assert c == (')' if k == '(' else ']'), s
        # un nombre entre parèntesis, (2/3) o (-1/2), és directament un nombre (els parèntesis es tornen a posar en escriure'l)
        if e[0] == 'n': return ('n', e[1], e[2], 'par')
        if e[0] == 's' and len(e[1]) == 1 and e[1][0][0] == '-' and e[1][0][1][0] == 'n': return ('n', -e[1][0][1][1], e[1][0][1][2], 'par')
        return ('g', k, e)
    e = expr(); assert i[0] == len(t), s
    return e
def val(e):
    k = e[0]
    if k == 'n': return e[1]
    if k == 'g': return val(e[2])
    if k == 'w': return val(e[1]) ** e[2]
    if k == 's':
        v = Fr(0)
        for sg, x in e[1]: v += val(x) if sg == '+' else -val(x)
        return v
    v = val(e[1][0][1])
    for op, x in e[1][1:]: v = v * val(x) if op == '·' else v / val(x)
    return v
DEC = [False]
def nt(v, big=True):
    if DEC[0] and exact(v): return fd(v)
    return tf(v, big)
def tex(e, top=True, big=True):
    k = e[0]
    if k == 'n':
        if e[2] and DEC[0]: return fd(e[1])
        return nt(e[1], big)
    if k == 'g':
        a, b = (r'\left(', r'\right)') if e[1] == '(' else (r'\left[', r'\right]')
        return a + tex(e[2], True, big) + b
    if k == 'w':
        b = e[1]; s = tex(b, False, big)
        if b[0] == 'n' and (b[1] < 0 or b[1].denominator != 1): s = r'\left(' + s + r'\right)'
        return '{' + s + '}^{%d}' % e[2]
    if k == 's':
        out = ''
        for j, (sg, x) in enumerate(e[1]):
            s = tex(x, False, big)
            if x[0] == 'n' and x[1] < 0 and (j > 0 or len(x) == 4): s = r'\left(' + s + r'\right)'
            out += ('-' if sg == '-' else ('' if j == 0 else '+')) + s
        return out
    out = ''
    for j, (op, x) in enumerate(e[1]):
        s = tex(x, False, big)
        if x[0] == 'n' and x[1] < 0 and (j > 0 or not top or len(x) == 4): s = r'\left(' + s + r'\right)'
        out += ('' if j == 0 else (r'\cdot ' if op == '·' else ':')) + s
    return out
def isn(e): return e[0] == 'n'
def red(e):
    """un pas: resol a la vegada totes les operacions que ja es poden fer, segons la jerarquia"""
    k = e[0]
    if k == 'n': return e
    if k == 'g':
        r = red(e[2]); return r if isn(r) else ('g', e[1], r)
    if k == 'w':
        if isn(e[1]): return ('n', e[1][1] ** e[2], False)
        b = red(e[1]); return ('w', b, e[2])
    xs = [x for _, x in e[1]]
    if all(isn(x) for x in xs): return ('n', val(e), False)
    return (k, [(o, red(x)) for o, x in e[1]])
def steps(s, dec=False, pre=''):
    """«expr = pas = pas = \\res{resultat}»"""
    DEC[0] = dec
    e = parse(s); v = val(e); chain = [tex(e)]
    while not isn(e):
        e = red(e); chain.append(tex(e))
    chain[-1] = r'\res{' + nt(v) + '}'
    if not dec and v.denominator != 1 and Fr(v) != v: pass
    DEC[0] = False
    return '$' + pre + '='.join(chain) + '$', v
def ex(s, dec=False):
    DEC[0] = dec; t = '$' + tex(parse(s)) + '$'; DEC[0] = False; return t
def res(s, dec=False):
    DEC[0] = dec; e = parse(s); t = '$' + tex(e) + r'=\res{' + nt(val(e)) + '}$'; DEC[0] = False; return t
def V(s): return val(parse(s))

S = []
def sec(title): S.append((title, [])); return S[-1][1]

# =====================================================================
# 1. Nombres decimals
X = sec(T('Nombres decimals', 'Números decimales'))
LECT = [('7.25', '7 unitats i 25 centèsimes', '7 unidades y 25 centésimas'), ('0.408', '408 mil·lèsimes', '408 milésimas'), ('12.06', '12 unitats i 6 centèsimes', '12 unidades y 6 centésimas'),
        ('3.5', '3 unitats i 5 dècimes', '3 unidades y 5 décimas'), ('100.001', '100 unitats i 1 mil·lèsima', '100 unidades y 1 milésima'), ('0.09', '9 centèsimes', '9 centésimas')]
X.append((1, T("Escriu com es llegeixen aquests nombres:", "Escribe cómo se leen estos números:") + tasks(3, ['$%s$' % fd(a) for a, _, _ in LECT])
    + recorda(T(r"llegim la part entera, la paraula \emph{unitats} i la part decimal amb el nom de l'\textbf{última} xifra: $3{,}045$ són 3 unitats i 45 mil·lèsimes.", r"leemos la parte entera, la palabra \emph{unidades} y la parte decimal con el nombre de la \textbf{última} cifra: $3{,}045$ son 3 unidades y 45 milésimas.")),
    tasks(2, ['$%s$: %s' % (fd(a), T(b, c)) for a, b, c in LECT])))
VALX = [('34.571', '7', T('7 centèsimes', '7 centésimas'), '0.07'), ('2.738', '3', T('3 centèsimes', '3 centésimas'), '0.03'), ('607.15', '7', T('7 unitats', '7 unidades'), '7'),
        ('0.0809', '8', T('8 centèsimes', '8 centésimas'), '0.08'), ('15.4', '4', T('4 dècimes', '4 décimas'), '0.4'), ('9.206', '6', T('6 mil·lèsimes', '6 milésimas'), '0.006')]
X.append((1, T("Quant val la xifra indicada en cada nombre?", "¿Cuánto vale la cifra indicada en cada número?") + tasks(3, [T(r'El %s en $%s$', r'El %s en $%s$') % (d, fd(x)) for x, d, _, _ in VALX]),
    tasks(3, [r'%s $=\res{%s}$' % (w, fd(v)) for _, _, w, v in VALX])))
CMP = [('4.7', '4.68'), ('0.09', '0.1'), ('5.307', '5.37'), ('12.5', '12.50'), ('3.099', '3.1'), ('0.45', '0.405')]
def sym(a, b): c = Dm(a) - Dm(b); return '<' if c < 0 else '>' if c > 0 else '='
X.append((1, T(r"Escriu $<$, $>$ o $=$:", r"Escribe $<$, $>$ o $=$:") + tasks(3, [r'$%s\ \square\ %s$' % (fd(a), fd(b)) for a, b in CMP]),
    tasks(3, [r'$%s\ \res{%s}\ %s$' % (fd(a), sym(a, b), fd(b)) for a, b in CMP])))
ORD = ['2.5', '2.05', '2.55', '2.505', '2.15', '2.501']
X.append((2, T(r"Ordena de menor a major: ", r"Ordena de menor a mayor: ") + '$%s$' % r';\ '.join(fd(x) for x in ORD),
    r'$\res{%s}$' % '<'.join(fd(x) for x in sorted(ORD, key=Dm))))
ROUND = ['3.4682', '15.8962', '0.7049', '29.996']
def rnd(x, k): return Dm(x).quantize(Dm(1).scaleb(-k), ROUND_HALF_UP)
def trn(x, k): return Dm(x).quantize(Dm(1).scaleb(-k), ROUND_DOWN)
def rs(x, k): return format(rnd(x, k), 'f').replace('.', '{,}')
def ts(x, k): return format(trn(x, k), 'f').replace('.', '{,}')
HD = T(r'Nombre & Truncat a les centèsimes & Arrodonit a les dècimes & Arrodonit a les centèsimes', r'Número & Truncado a las centésimas & Redondeado a las décimas & Redondeado a las centésimas')
X.append((2, T("Completa la taula:", "Completa la tabla:") + r'\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.4cm}|C{2.4cm}|C{2.4cm}|}\hline ' + HD + r'\\\hline '
    + r'\\\hline '.join('$%s$ & & & ' % fd(x) for x in ROUND) + r'\\\hline\end{tabular}\par}'
    + recorda(T(r"per a \textbf{arrodonir}, mirem la primera xifra que eliminem: si és 0, 1, 2, 3 o 4, l'última xifra es queda igual; si és 5, 6, 7, 8 o 9, li sumem 1.", r"para \textbf{redondear}, miramos la primera cifra que eliminamos: si es 0, 1, 2, 3 o 4, la última cifra se queda igual; si es 5, 6, 7, 8 o 9, le sumamos 1.")),
    r'\par\smallskip{\centering\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.4cm}|C{2.4cm}|C{2.4cm}|}\hline ' + HD + r'\\\hline '
    + r'\\\hline '.join(r'$%s$ & $%s$ & $\res{%s}$ & $\res{%s}$' % (fd(x), ts(x, 2), rs(x, 1), rs(x, 2)) for x in ROUND) + r'\\\hline\end{tabular}\par}'))
assert [rs(x, 2) for x in ROUND] == ['3{,}47', '15{,}90', '0{,}70', '30{,}00']
X.append((3, T(r"Escriu tres nombres compresos entre $4{,}7$ i $4{,}71$. Quin és el nombre més xicotet amb dues xifres decimals que, arrodonit a les unitats, dona 8? I el més gran?",
               r"Escribe tres números comprendidos entre $4{,}7$ y $4{,}71$. ¿Cuál es el número más pequeño con dos cifras decimales que, redondeado a las unidades, da 8? ¿Y el mayor?"),
    T(r"Per exemple $4{,}701$; $4{,}705$; $4{,}7099$ (n'hi ha infinits). \ El més xicotet és $\res{7{,}50}$ i el més gran, $\res{8{,}49}$.", r"Por ejemplo $4{,}701$; $4{,}705$; $4{,}7099$ (hay infinitos). \ El más pequeño es $\res{7{,}50}$ y el mayor, $\res{8{,}49}$.")))
assert rnd('7.50', 0) == 8 and rnd('7.49', 0) == 7 and rnd('8.49', 0) == 8 and rnd('8.50', 0) == 9

# =====================================================================
# 2. Tipus de nombres decimals
X = sec(T('Tipus de nombres decimals', 'Tipos de números decimales'))
CL = [(r'4{,}252525\ldots', T(r'periòdic pur: $\res{4{,}\overline{25}}$', r'periódico puro: $\res{4{,}\overline{25}}$')), (r'0{,}125', T('exacte', 'exacto')),
      (r'7{,}31666\ldots', T(r'periòdic mixt: $\res{7{,}31\overline{6}}$', r'periódico mixto: $\res{7{,}31\overline{6}}$')), (r'1{,}010010001\ldots', T('no exacte i no periòdic', 'no exacto y no periódico')),
      (r'0{,}777\ldots', T(r'periòdic pur: $\res{0{,}\overline{7}}$', r'periódico puro: $\res{0{,}\overline{7}}$')), (r'12{,}408408\ldots', T(r'periòdic pur: $\res{12{,}\overline{408}}$', r'periódico puro: $\res{12{,}\overline{408}}$')),
      (r'3{,}1252525\ldots', T(r'periòdic mixt: $\res{3{,}1\overline{25}}$', r'periódico mixto: $\res{3{,}1\overline{25}}$')), (r'\pi=3{,}14159\ldots', T('no exacte i no periòdic', 'no exacto y no periódico'))]
X.append((1, T(r"Classifica els nombres següents i, si són periòdics, escriu-los amb la ratlla del període:", r"Clasifica los números siguientes y, si son periódicos, escríbelos con la raya del periodo:")
    + tasks(2, ['$%s$' % a for a, _ in CL]) + recorda(T(r"periòdic \textbf{pur}: el període comença just després de la coma; \textbf{mixt}: abans del període hi ha xifres que no es repeteixen (l'anteperíode).", r"periódico \textbf{puro}: el periodo empieza justo después de la coma; \textbf{mixto}: antes del periodo hay cifras que no se repiten (el anteperiodo).")),
    tasks(2, [r'$%s$: \rest{%s}' % (a, b) if '$' not in b else r'$%s$: %s' % (a, b) for a, b in CL])))
PA = [('5', '', '6'), ('0', '0', '9'), ('2', '13', '4'), ('0', '', '142857')]
X.append((1, T("Indica la part entera, l'anteperíode i el període de cada nombre:", "Indica la parte entera, el anteperiodo y el periodo de cada número:") + tasks(4, ['$%s$' % dx(*p) for p in PA]),
    tasks(2, ['$%s$: %s $\\res{%s}$; %s %s; %s $\\res{%s}$' % (dx(*p), T('part entera', 'parte entera'), p[0], T('anteperíode', 'anteperiodo'), r'$\res{%s}$' % p[1] if p[1] else T('no en té', 'no tiene'), T('període', 'periodo'), p[2]) for p in PA])))
O2 = [('0', '', '3'), ('0', '3', ''), ('0', '3', '4'), ('0', '', '34'), ('0', '33', '')]
def o2v(p): return gen(*p) if p[2] else Fr(Dm('0.' + p[1]))
def o2t(p): return dx(*p) if p[2] else '0{,}' + p[1]
o2s = sorted(O2, key=o2v)
X.append((2, T(r"Ordena de menor a major: ", r"Ordena de menor a mayor: ") + '$' + r';\ \ '.join(o2t(p) for p in O2) + '$',
    T("Escrivim unes quantes xifres de cada un: ", "Escribimos unas cuantas cifras de cada uno: ") + r'$0{,}3000\ldots$; \ $0{,}3300\ldots$; \ $0{,}3333\ldots$; \ $0{,}3434\ldots$; \ $0{,}3444\ldots$\par' + r'$\res{' + '<'.join(o2t(p) for p in o2s) + '}$'))
assert [o2t(p) for p in o2s] == ['0{,}3', '0{,}33', r'0{,}\overline{3}', r'0{,}\overline{34}', r'0{,}3\overline{4}']
X.append((3, T(r"Escriu un nombre decimal periòdic pur, un de periòdic mixt, un d'exacte i un de no exacte i no periòdic que estiguen tots entre $2{,}1$ i $2{,}2$.",
               r"Escribe un número decimal periódico puro, uno periódico mixto, uno exacto y uno no exacto y no periódico que estén todos entre $2{,}1$ y $2{,}2$."),
    T(r"Per exemple: $\res{2{,}\overline{15}}$, \ $\res{2{,}1\overline{7}}$, \ $\res{2{,}125}$ \ i \ $\res{2{,}101001000\ldots}$ (hi ha infinites respostes).", r"Por ejemplo: $\res{2{,}\overline{15}}$, \ $\res{2{,}1\overline{7}}$, \ $\res{2{,}125}$ \ y \ $\res{2{,}101001000\ldots}$ (hay infinitas respuestas).")))
assert Fr(21, 10) < 2 + Fr(15, 99) < Fr(22, 10) and Fr(21, 10) < gen(2, '1', '7') < Fr(22, 10)

# =====================================================================
# 3. Sumar, restar i multiplicar decimals
X = sec(T('Sumar, restar i multiplicar decimals', 'Sumar, restar y multiplicar decimales'))
SUM = ['23.45+7.8', '40-12.35', '0.9+0.35', '15-6.47', '3.06+12.9+0.4', '100-0.01']
X.append((1, T("Calcula:", "Calcula:") + tasks(3, [ex(e, True) for e in SUM])
    + recorda(T(r"per a sumar i restar, col·loquem les \textbf{comes alineades} i completem amb zeros.", r"para sumar y restar, colocamos las \textbf{comas alineadas} y completamos con ceros.")),
    tasks(3, [res(e, True) for e in SUM])))
MUL = ['4.6·3', '2.35·0.4', '0.6·0.05', '12.5·1.2', '3.25·1.4', '0.07·0.3']
X.append((1, T("Calcula:", "Calcula:") + tasks(3, [ex(e, True) for e in MUL])
    + recorda(T(r"multipliquem com si no hi haguera comes i separem tants decimals com \textbf{sumen} els dos factors.", r"multiplicamos como si no hubiera comas y separamos tantos decimales como \textbf{suman} los dos factores.")),
    tasks(3, [res(e, True) for e in MUL])))
P10 = ['3.7·100', '0.052·1000', '45.2:1000', '8:100', '6.15·10', '0.3:10', '250·0.1', '1.4·0.01']
X.append((1, T("Calcula mentalment:", "Calcula mentalmente:") + tasks(4, [ex(e, True) for e in P10]),
    tasks(3, [res(e, True) for e in P10])))
X.append((2, T(r"Compre $2{,}5$ kg de pomes a $1{,}86$ €/kg i $0{,}75$ kg de formatge a $14{,}20$ €/kg. Pague amb un bitllet de 20 €. Quant em tornen?", r"Compro $2{,}5$ kg de manzanas a $1{,}86$ €/kg y $0{,}75$ kg de queso a $14{,}20$ €/kg. Pago con un billete de 20 €. ¿Cuánto me devuelven?"),
    r"$2{,}5\cdot1{,}86=4{,}65$ €; \ $0{,}75\cdot14{,}20=10{,}65$ €; \ $4{,}65+10{,}65=15{,}30$ €; \ $20-15{,}30=\res{4{,}70\text{ €}}$"))
ck(V('2.5·1.86'), Fr('4.65')); ck(V('0.75·14.2'), Fr('10.65')); ck(V('20-4.65-10.65'), Fr('4.7'))
X.append((2, T(r"Un full de paper fa $0{,}012$ cm de gruix. Quant fa un paquet de 500 fulls? I una pila de 1000 paquets, en metres?", r"Una hoja de papel tiene $0{,}012$ cm de grosor. ¿Cuánto mide un paquete de 500 hojas? ¿Y una pila de 1000 paquetes, en metros?"),
    r"$0{,}012\cdot500=\res{6\text{ cm}}$; \ $6\cdot1000=6000\text{ cm}=\res{60\text{ m}}$"))
ck(V('0.012·500'), 6)
X.append((3, T(r"Troba el nombre que falta: \ a) $3{,}75+\square=10$ \quad b) $\square-2{,}08=5{,}3$ \quad c) $\square\cdot100=4{,}5$ \quad d) $0{,}4\cdot\square=0{,}12$",
               r"Halla el número que falta: \ a) $3{,}75+\square=10$ \quad b) $\square-2{,}08=5{,}3$ \quad c) $\square\cdot100=4{,}5$ \quad d) $0{,}4\cdot\square=0{,}12$"),
    r"a) $\res{6{,}25}$ \quad b) $\res{7{,}38}$ \quad c) $\res{0{,}045}$ \quad d) $\res{0{,}3}$"))
ck(V('10-3.75'), Fr('6.25')); ck(V('5.3+2.08'), Fr('7.38')); ck(V('4.5:100'), Fr('0.045')); ck(V('0.12:0.4'), Fr('0.3'))

# =====================================================================
# 4. Dividir amb decimals
X = sec(T('Dividir amb decimals', 'Dividir con decimales'))
DIV = ['8.4:4', '15:8', '9.75:3', '4.5:0.9', '2.73:0.7', '6:0.12']
X.append((1, T("Calcula:", "Calcula:") + tasks(3, [ex(e, True) for e in DIV])
    + recorda(T(r"si el divisor té decimals, multipliquem dividend i divisor per 10, 100, 1000… fins que el divisor siga un nombre natural: $4{,}5:0{,}9=45:9$.", r"si el divisor tiene decimales, multiplicamos dividendo y divisor por 10, 100, 1000… hasta que el divisor sea un número natural: $4{,}5:0{,}9=45:9$.")),
    tasks(3, [res(e, True) for e in DIV])))
APX = [('10', '3', 2), ('7', '6', 2), ('2', '7', 3), ('5.3', '0.9', 2)]
X.append((2, T("Calcula el quocient amb les xifres decimals indicades (arrodoneix l'última):", "Calcula el cociente con las cifras decimales indicadas (redondea la última):")
    + tasks(4, [r'$%s:%s$ \ (%d)' % (fd(a), fd(b), k) for a, b, k in APX]),
    tasks(4, [r'$%s:%s\approx\res{%s}$' % (fd(a), fd(b), rs(Dm(a) / Dm(b), k)) for a, b, k in APX])))
assert [rs(Dm(a) / Dm(b), k) for a, b, k in APX] == ['3{,}33', '1{,}17', '0{,}286', '5{,}89']
CD = ['5.2-1.5·2.4+0.6:0.2', '(3.5-1.25)·0.4+2.7:0.09', '1.2·(4-2.5)+0.8:4', '10-(0.5+1.5)^2·2']
X.append((2, T("Calcula respectant la jerarquia de les operacions:", "Calcula respetando la jerarquía de las operaciones:") + tasks(2, [ex(e, True) for e in CD], '6pt'),
    tasks(1, [steps(e, True)[0] for e in CD], '4pt')))
X.append((2, T(r"Un tros de formatge de $0{,}85$ kg costa $11{,}39$ €. Quin és el preu del quilo? Quant costaria un tros de $1{,}2$ kg?", r"Un trozo de queso de $0{,}85$ kg cuesta $11{,}39$ €. ¿Cuál es el precio del kilo? ¿Cuánto costaría un trozo de $1{,}2$ kg?"),
    r"$11{,}39:0{,}85=1139:85=\res{13{,}40\text{ €/kg}}$; \ $13{,}40\cdot1{,}2=\res{16{,}08\text{ €}}$"))
ck(V('11.39:0.85'), Fr('13.4')); ck(V('13.4·1.2'), Fr('16.08'))
X.append((3, T(r"Un cotxe gasta $31{,}5$ L de gasolina en 450 km. Quants litres gasta cada 100 km? Si el litre costa $1{,}58$ €, quant costa un viatge de 260 km?", r"Un coche gasta $31{,}5$ L de gasolina en 450 km. ¿Cuántos litros gasta cada 100 km? Si el litro cuesta $1{,}58$ €, ¿cuánto cuesta un viaje de 260 km?"),
    T(r"$31{,}5:4{,}5=\res{7\text{ L}}$ cada 100 km. \ En 260 km: $7\cdot2{,}6=18{,}2$ L; \ $18{,}2\cdot1{,}58=28{,}756\approx\res{28{,}76\text{ €}}$", r"$31{,}5:4{,}5=\res{7\text{ L}}$ cada 100 km. \ En 260 km: $7\cdot2{,}6=18{,}2$ L; \ $18{,}2\cdot1{,}58=28{,}756\approx\res{28{,}76\text{ €}}$")))
ck(V('31.5:4.5'), 7); ck(V('7·2.6·1.58'), Fr('28.756'))
X.append((3, T(r"Amb una ampolla de $1{,}5$ L, quants gots de $0{,}25$ L podem omplir? I quants de $0{,}2$ L? Quant sobra en cada cas?", r"Con una botella de $1{,}5$ L, ¿cuántos vasos de $0{,}25$ L podemos llenar? ¿Y cuántos de $0{,}2$ L? ¿Cuánto sobra en cada caso?"),
    T(r"$1{,}5:0{,}25=\res{6}$ gots i no en sobra res. \ $1{,}5:0{,}2=7{,}5$: \ $\res{7}$ gots plens i sobren $1{,}5-7\cdot0{,}2=\res{0{,}1\text{ L}}$.", r"$1{,}5:0{,}25=\res{6}$ vasos y no sobra nada. \ $1{,}5:0{,}2=7{,}5$: \ $\res{7}$ vasos llenos y sobran $1{,}5-7\cdot0{,}2=\res{0{,}1\text{ L}}$.")))
ck(V('1.5:0.25'), 6); ck(V('1.5-7·0.2'), Fr('0.1'))

# =====================================================================
# 5. Fraccions
X = sec(T('Fraccions', 'Fracciones'))
OF = [(Fr(2, 7), 63), (Fr(3, 4), 80), (Fr(5, 6), 108), (Fr(3, 8), 240)]
X.append((1, T("Calcula:", "Calcula:") + tasks(4, [r'$%s$ %s $%d$' % (tf(f), T('de', 'de'), n) for f, n in OF]),
    tasks(4, [r'$%s\cdot%d=\res{%s}$' % (tf(f), n, tf(f * n)) for f, n in OF])))
SIMP = [(84, 126), (105, 180), (36, 48), (75, 100), (240, 360), (98, 140)]
X.append((1, T("Simplifica fins a obtindre la fracció irreductible:", "Simplifica hasta obtener la fracción irreducible:") + tasks(6, ['$%s$' % r'\dfrac{%d}{%d}' % p for p in SIMP])
    + recorda(T(r"dividim numerador i denominador pel seu màxim comú divisor (MCD).", r"dividimos numerador y denominador por su máximo común divisor (MCD).")),
    tasks(3, [r'$\dfrac{%d}{%d}=\res{%s}$ \ (MCD $=%d$)' % (a, b, tf(Fr(a, b)), __import__('math').gcd(a, b)) for a, b in SIMP])))
EQV = [((14, 21), (22, 33)), ((3, 4), (12, 15)), ((-6, 8), (9, -12)), ((5, 7), (15, 20))]
def eqs(a, b): return a[0] * b[1] == a[1] * b[0]
def fq(p): return r'\dfrac{%d}{%d}' % p
X.append((2, T("Comprova si són equivalents:", "Comprueba si son equivalentes:") + tasks(4, ['$%s\\ \\text{%s}\\ %s$' % (fq(a), T('i', 'y'), fq(b)) for a, b in EQV]),
    tasks(2, [r'$%d\cdot%s=%d$, \ $%s\cdot%d=%d$: \rest{%s}' % (a[0], '(%d)' % b[1] if b[1] < 0 else b[1], a[0] * b[1], '(%d)' % a[1] if a[1] < 0 else a[1], b[0], a[1] * b[0], T('sí', 'sí') if eqs(a, b) else 'no') for a, b in EQV])))
XQ = [('x', 12, 15, 36), (8, 'x', -2, 5), (6, 9, 'x', 15), (3, 5, 27, 'x')]
def xsol(q):
    a, b, c, d = q
    if a == 'x': return Fr(b * c, d)
    if b == 'x': return Fr(a * d, c)
    if c == 'x': return Fr(a * d, b)
    return Fr(b * c, a)
def xq(q): return r'\dfrac{%s}{%s}=\dfrac{%s}{%s}' % q
X.append((2, T("Troba $x$ perquè les fraccions siguen equivalents:", "Halla $x$ para que las fracciones sean equivalentes:") + tasks(4, ['$%s$' % xq(q) for q in XQ]),
    tasks(4, [r'$x=\res{%s}$' % tf(xsol(q)) for q in XQ])))
for q in XQ:
    v = [xsol(q) if t == 'x' else Fr(t) for t in q]; assert v[0] / v[1] == v[2] / v[3]
ORDF = [Fr(5, 6), Fr(-3, 4), Fr(7, 9), Fr(-2, 3), Fr(3, 4)]
X.append((2, T("Ordena de menor a major:", "Ordena de menor a mayor:") + r' $%s$' % r';\ \ '.join(tf(f) for f in ORDF),
    T("Amb denominador comú 36: ", "Con denominador común 36: ") + '$' + r';\ '.join(tf(f).replace('{%d}' % f.denominator, '{36}').replace('{%d}{' % abs(f.numerator), '{%d}{' % abs(f.numerator * 36 // f.denominator), 1) for f in ORDF) + '$.\\par'
    + r'$\res{%s}$' % '<'.join(tf(f) for f in sorted(ORDF))))
X.append((3, T(r"Escriu tres fraccions compreses entre $\dfrac{1}{3}$ i $\dfrac{1}{2}$. Quina fracció de denominador 20 està just a la meitat entre $\dfrac{2}{5}$ i $\dfrac{1}{2}$?", r"Escribe tres fracciones comprendidas entre $\dfrac{1}{3}$ y $\dfrac{1}{2}$. ¿Qué fracción de denominador 20 está justo en la mitad entre $\dfrac{2}{5}$ y $\dfrac{1}{2}$?"),
    T(r"Amb denominador 24: $\dfrac{8}{24}$ i $\dfrac{12}{24}$; per exemple $\res{\dfrac{9}{24},\ \dfrac{10}{24},\ \dfrac{11}{24}}$. \ Amb denominador 20: $\dfrac{8}{20}$ i $\dfrac{10}{20}$: la del mig és $\res{\dfrac{9}{20}}$.", r"Con denominador 24: $\dfrac{8}{24}$ y $\dfrac{12}{24}$; por ejemplo $\res{\dfrac{9}{24},\ \dfrac{10}{24},\ \dfrac{11}{24}}$. \ Con denominador 20: $\dfrac{8}{20}$ y $\dfrac{10}{20}$: la del medio es $\res{\dfrac{9}{20}}$.")))
ck((Fr(2, 5) + Fr(1, 2)) / 2, Fr(9, 20))

# =====================================================================
# 6. Fraccions i decimals
X = sec(T('Fraccions i decimals', 'Fracciones y decimales'))
FD = [Fr(9, 20), Fr(5, 9), Fr(7, 30), Fr(21, 28), Fr(4, 11), Fr(7, 12), Fr(13, 40), Fr(1, 6)]
def fac(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0: out.append(p); n //= p
        p += 1
    return out
def ftex(n):
    from collections import Counter
    c = Counter(fac(n)); return r'\cdot '.join('%d^{%d}' % (p, k) if k > 1 else str(p) for p, k in sorted(c.items())) or '1'
X.append((1, T("Sense fer la divisió, digues si cada fracció dona un decimal exacte, periòdic pur o periòdic mixt. Després, comprova-ho dividint:", "Sin hacer la división, di si cada fracción da un decimal exacto, periódico puro o periódico mixto. Después, compruébalo dividiendo:")
    + tasks(4, [r'$\dfrac{%d}{%d}$' % (f.numerator, f.denominator) if f != Fr(21, 28) else r'$\dfrac{21}{28}$' for f in FD])
    + recorda(T(r"mira el denominador de la fracció \textbf{irreductible}: si només té els factors 2 i 5, és exacte; si no en té cap, periòdic pur; si en té i també d'altres, periòdic mixt.", r"mira el denominador de la fracción \textbf{irreducible}: si solo tiene los factores 2 y 5, es exacto; si no tiene ninguno, periódico puro; si tiene alguno y también otros, periódico mixto.")),
    tasks(2, [(r'$\dfrac{21}{28}=\dfrac{3}{4}$, ' if f == Fr(21, 28) else r'$\dfrac{%d}{%d}$, ' % (f.numerator, f.denominator)) + r'$%d=%s$: \rest{%s}, $\res{%s}$' % (f.denominator, ftex(f.denominator), kind(f), per(f.numerator, f.denominator)) for f in FD])))
EXD = ['0.8', '0.45', '1.2', '0.004', '2.35', '0.125']
X.append((1, T("Escriu com a fracció irreductible:", "Escribe como fracción irreducible:") + tasks(6, ['$%s$' % fd(x) for x in EXD]),
    tasks(3, [r'$%s=\dfrac{%d}{%d}=\res{%s}$' % (fd(x), int(x.replace('.', '')), 10 ** len(x.split('.')[1]), tf(Fr(x))) for x in EXD])))
GEN = [('0', '', '6'), ('3', '', '12'), ('0', '8', '3'), ('2', '1', '45'), ('5', '', '4'), ('0', '', '27'), ('0', '1', '6'), ('1', '2', '3')]
def gsol(p):
    e, a, q = p; full, part = int(e + a + q), int(e + a); den = int('9' * len(q) + '0' * len(a)); f = gen(e, a, q)
    s = r'$%s=\dfrac{%d%s}{%d}' % (dx(e, a, q), full, '-%d' % part if part else '', den)
    if part: s += r'=\dfrac{%d}{%d}' % (full - part, den)
    return s + (r'=\res{%s}$' % tf(f))
X.append((2, T("Calcula la fracció generatriu i simplifica-la:", "Calcula la fracción generatriz y simplifícala:") + tasks(4, ['$%s$' % dx(*p) for p in GEN])
    + recorda(T(r"numerador: el nombre sense coma fins al final del període menys la part que no es repeteix; denominador: tants 9 com xifres té el període i tants 0 com xifres té l'anteperíode. \ $1{,}2\overline{3}=\dfrac{123-12}{90}$", r"numerador: el número sin coma hasta el final del periodo menos la parte que no se repite; denominador: tantos 9 como cifras tiene el periodo y tantos 0 como cifras tiene el anteperiodo. \ $1{,}2\overline{3}=\dfrac{123-12}{90}$")),
    tasks(2, [gsol(p) for p in GEN], '4pt')))
for p in GEN:
    f = gen(*p); assert per(f.numerator, f.denominator) == dx(*p) or (p == ('0', '', '6')), (p, per(f.numerator, f.denominator))
X.append((2, T(r"Comprova, dividint, que $\dfrac{37}{30}=1{,}2\overline{3}$. Després, demostra-ho multiplicant $x=1{,}2\overline{3}$ per 100 i per 10 i restant.", r"Comprueba, dividiendo, que $\dfrac{37}{30}=1{,}2\overline{3}$. Después, demuéstralo multiplicando $x=1{,}2\overline{3}$ por 100 y por 10 y restando."),
    T(r"$37:30=1{,}2333\ldots$ \quad $100x=123{,}333\ldots$; \ $10x=12{,}333\ldots$; \ restant: $90x=111\Rightarrow x=\dfrac{111}{90}=\res{\dfrac{37}{30}}$", r"$37:30=1{,}2333\ldots$ \quad $100x=123{,}333\ldots$; \ $10x=12{,}333\ldots$; \ restando: $90x=111\Rightarrow x=\dfrac{111}{90}=\res{\dfrac{37}{30}}$")))
ck(Fr(111, 90), Fr(37, 30)); assert per(37, 30) == r'1{,}2\overline{3}'
X.append((2, T(r"Ordena de menor a major passant-ho tot a decimal: \ $0{,}7;\ \ \dfrac{2}{3};\ \ 0{,}67;\ \ \dfrac{3}{4};\ \ 0{,}6\overline{8}$", r"Ordena de menor a mayor pasándolo todo a decimal: \ $0{,}7;\ \ \dfrac{2}{3};\ \ 0{,}67;\ \ \dfrac{3}{4};\ \ 0{,}6\overline{8}$"),
    r"$\dfrac{2}{3}=0{,}666\ldots$, \ $\dfrac{3}{4}=0{,}75$, \ $0{,}6\overline{8}=0{,}688\ldots$: \quad $\res{\dfrac{2}{3}<0{,}67<0{,}6\overline{8}<0{,}7<\dfrac{3}{4}}$"))
assert Fr(2, 3) < Fr('0.67') < gen(0, '6', '8') < Fr('0.7') < Fr(3, 4)
X.append((3, T(r"Calcula passant a fracció: \ a) $0{,}\overline{3}+0{,}\overline{6}$ \quad b) $0{,}\overline{9}$ \quad c) $1{,}\overline{3}\cdot0{,}75$ \quad d) $0{,}1\overline{6}:0{,}\overline{5}$. Què observes en a) i b)?", r"Calcula pasando a fracción: \ a) $0{,}\overline{3}+0{,}\overline{6}$ \quad b) $0{,}\overline{9}$ \quad c) $1{,}\overline{3}\cdot0{,}75$ \quad d) $0{,}1\overline{6}:0{,}\overline{5}$. ¿Qué observas en a) y b)?"),
    T(r"a) $\dfrac{3}{9}+\dfrac{6}{9}=\res{1}$ \quad b) $\dfrac{9}{9}=\res{1}$ \quad c) $\dfrac{4}{3}\cdot\dfrac{3}{4}=\res{1}$ \quad d) $\dfrac{1}{6}:\dfrac{5}{9}=\res{\dfrac{3}{10}}$. \ En a) i b) veiem que $0{,}999\ldots$ i 1 són el mateix nombre.", r"a) $\dfrac{3}{9}+\dfrac{6}{9}=\res{1}$ \quad b) $\dfrac{9}{9}=\res{1}$ \quad c) $\dfrac{4}{3}\cdot\dfrac{3}{4}=\res{1}$ \quad d) $\dfrac{1}{6}:\dfrac{5}{9}=\res{\dfrac{3}{10}}$. \ En a) y b) vemos que $0{,}999\ldots$ y 1 son el mismo número.")))
ck(gen(0, '', '3') + gen(0, '', '6'), 1); ck(gen(0, '', '9'), 1); ck(gen(1, '', '3') * Fr(3, 4), 1); ck(gen(0, '1', '6') / gen(0, '', '5'), Fr(3, 10))

# =====================================================================
# 7. Suma i resta de fraccions
X = sec(T('Suma i resta de fraccions', 'Suma y resta de fracciones'))
SR1 = ['4/7+8/7', '3/10+2/5', '5/6-1/4', '7/12+5/18', '3-5/4', '1+2/7']
X.append((1, T("Calcula i simplifica:", "Calcula y simplifica:") + tasks(3, [ex(e) for e in SR1], '6pt')
    + recorda(T(r"si els denominadors són diferents, reduïm a comú denominador amb el mcm: $\dfrac{5}{6}-\dfrac{1}{4}=\dfrac{10}{12}-\dfrac{3}{12}$.", r"si los denominadores son distintos, reducimos a común denominador con el mcm: $\dfrac{5}{6}-\dfrac{1}{4}=\dfrac{10}{12}-\dfrac{3}{12}$.")),
    tasks(3, [res(e) for e in SR1], '6pt')))
SR2 = ['1/2-2/3+1/6', '-3/4-1/6+2', '5/6-3/4+1/3', '2/5-7/10-1', '-1/2-1/3-1/4', '3/8-5/12+1/6']
X.append((2, T("Calcula i simplifica:", "Calcula y simplifica:") + tasks(3, [ex(e) for e in SR2], '6pt'),
    tasks(3, [res(e) for e in SR2], '6pt')))
SR3 = ['2/5-(1/2-3/4)-1', '2/3-[1/4-(5/6-1)]', '(1-1/3)-(1/2-1/5)', '3/4-[2-(1/3+5/6)]']
X.append((2, T("Calcula (primer els parèntesis):", "Calcula (primero los paréntesis):") + tasks(2, [ex(e) for e in SR3], '8pt'),
    tasks(1, [steps(e)[0] for e in SR3], '6pt')))
X.append((3, T(r"Quina fracció cal sumar a $\dfrac{3}{8}$ per a obtindre $\dfrac{5}{6}$? Quina cal restar a $\dfrac{1}{4}$ per a obtindre $-\dfrac{2}{3}$?", r"¿Qué fracción hay que sumar a $\dfrac{3}{8}$ para obtener $\dfrac{5}{6}$? ¿Cuál hay que restar a $\dfrac{1}{4}$ para obtener $-\dfrac{2}{3}$?"),
    r"$\dfrac{5}{6}-\dfrac{3}{8}=\dfrac{20}{24}-\dfrac{9}{24}=\res{\dfrac{11}{24}}$; \qquad $\dfrac{1}{4}+\dfrac{2}{3}=\dfrac{3}{12}+\dfrac{8}{12}=\res{\dfrac{11}{12}}$"))
ck(Fr(5, 6) - Fr(3, 8), Fr(11, 24)); ck(Fr(1, 4) - Fr(11, 12), Fr(-2, 3))
X.append((3, T(r"Troba l'error i corregeix-lo: \ $\dfrac{2}{3}+\dfrac{1}{5}=\dfrac{2+1}{3+5}=\dfrac{3}{8}$", r"Encuentra el error y corrígelo: \ $\dfrac{2}{3}+\dfrac{1}{5}=\dfrac{2+1}{3+5}=\dfrac{3}{8}$"),
    T(r"No es poden sumar els denominadors. Cal reduir a comú denominador: $\dfrac{10}{15}+\dfrac{3}{15}=\res{\dfrac{13}{15}}$.", r"No se pueden sumar los denominadores. Hay que reducir a común denominador: $\dfrac{10}{15}+\dfrac{3}{15}=\res{\dfrac{13}{15}}$.")))
ck(Fr(2, 3) + Fr(1, 5), Fr(13, 15))

# =====================================================================
# 8. Multiplicació i divisió de fraccions
X = sec(T('Multiplicació i divisió de fraccions', 'Multiplicación y división de fracciones'))
MD1 = ['2/3·5/7', '6/4·2/5', '3/7·14', '4/3:5/6', '3/5:9/10', '6:3/4']
X.append((1, T("Calcula i simplifica:", "Calcula y simplifica:") + tasks(3, [ex(e) for e in MD1], '6pt')
    + recorda(T(r"per a dividir, multipliquem per la \textbf{inversa}: $\dfrac{a}{b}:\dfrac{c}{d}=\dfrac{a}{b}\cdot\dfrac{d}{c}=\dfrac{a\cdot d}{b\cdot c}$.", r"para dividir, multiplicamos por la \textbf{inversa}: $\dfrac{a}{b}:\dfrac{c}{d}=\dfrac{a}{b}\cdot\dfrac{d}{c}=\dfrac{a\cdot d}{b\cdot c}$.")),
    tasks(3, [res(e) for e in MD1], '6pt')))
INV = [Fr(2, 5), Fr(-7, 4), Fr(3), Fr(-1, 6), Fr(1)]
X.append((1, T("Escriu la inversa de cada nombre:", "Escribe la inversa de cada número:") + tasks(5, ['$%s$' % tf(f) for f in INV]),
    tasks(5, [r'$\res{%s}$' % tf(1 / f) for f in INV])))
MD2 = ['(-8/15)·(-25/12)', '(-5/6):10/9', '7/10:(-14)', '14/15·25/21', '3/4·8/9:2/3', '2/5:(4/5·3/8)']
X.append((2, T("Calcula i simplifica:", "Calcula y simplifica:") + tasks(3, [ex(e) for e in MD2], '6pt'),
    tasks(3, [res(e) for e in MD2], '6pt')))
X.append((2, T(r"Calcula: \ a) $\dfrac{2}{3}$ de $\dfrac{9}{10}$ \quad b) la meitat de $\dfrac{4}{5}$ \quad c) el triple de $\dfrac{5}{12}$ \quad d) $\dfrac{\;\frac{3}{4}\;}{\frac{9}{2}}$", r"Calcula: \ a) $\dfrac{2}{3}$ de $\dfrac{9}{10}$ \quad b) la mitad de $\dfrac{4}{5}$ \quad c) el triple de $\dfrac{5}{12}$ \quad d) $\dfrac{\;\frac{3}{4}\;}{\frac{9}{2}}$"),
    r"a) $\dfrac{2}{3}\cdot\dfrac{9}{10}=\res{\dfrac{3}{5}}$ \quad b) $\dfrac{1}{2}\cdot\dfrac{4}{5}=\res{\dfrac{2}{5}}$ \quad c) $3\cdot\dfrac{5}{12}=\res{\dfrac{5}{4}}$ \quad d) $\dfrac{3}{4}:\dfrac{9}{2}=\dfrac{6}{36}=\res{\dfrac{1}{6}}$"))
ck(Fr(2, 3) * Fr(9, 10), Fr(3, 5)); ck(Fr(4, 5) / 2, Fr(2, 5)); ck(3 * Fr(5, 12), Fr(5, 4)); ck(Fr(3, 4) / Fr(9, 2), Fr(1, 6))
X.append((3, T(r"Per quina fracció cal multiplicar $\dfrac{4}{9}$ per a obtindre $\dfrac{2}{3}$? Entre quina fracció cal dividir $\dfrac{5}{8}$ per a obtindre 5?", r"¿Por qué fracción hay que multiplicar $\dfrac{4}{9}$ para obtener $\dfrac{2}{3}$? ¿Entre qué fracción hay que dividir $\dfrac{5}{8}$ para obtener 5?"),
    r"$\dfrac{2}{3}:\dfrac{4}{9}=\dfrac{18}{12}=\res{\dfrac{3}{2}}$; \qquad $\dfrac{5}{8}:5=\res{\dfrac{1}{8}}$"))
ck(Fr(4, 9) * Fr(3, 2), Fr(2, 3)); ck(Fr(5, 8) / Fr(1, 8), 5)

# =====================================================================
# 9. Potències de fraccions
X = sec(T('Potències de fraccions', 'Potencias de fracciones'))
P1 = ['(3/4)^3', '(-2/5)^2', '(-1/3)^3', '(7/9)^0', '(1/2)^5', '(-3/2)^4', '(-2/3)^1', '(5/2)^2']
X.append((1, T("Calcula:", "Calcula:") + tasks(4, [ex(e) for e in P1], '6pt')
    + recorda(T(r"$\left(\dfrac{a}{b}\right)^n=\dfrac{a^n}{b^n}$. Amb base negativa, el resultat és positiu si l'exponent és parell i negatiu si és senar.", r"$\left(\dfrac{a}{b}\right)^n=\dfrac{a^n}{b^n}$. Con base negativa, el resultado es positivo si el exponente es par y negativo si es impar.")),
    tasks(4, [res(e) for e in P1], '6pt')))
X.append((1, T(r"Calcula i compara: \ $\left(-\dfrac{2}{3}\right)^2$, \ $-\left(\dfrac{2}{3}\right)^2$, \ $\dfrac{2^2}{3}$ \ i \ $\dfrac{-2^2}{3^2}$.", r"Calcula y compara: \ $\left(-\dfrac{2}{3}\right)^2$, \ $-\left(\dfrac{2}{3}\right)^2$, \ $\dfrac{2^2}{3}$ \ y \ $\dfrac{-2^2}{3^2}$."),
    r"$\res{\dfrac{4}{9}}$, \ $\res{-\dfrac{4}{9}}$, \ $\res{\dfrac{4}{3}}$, \ $\res{-\dfrac{4}{9}}$. " + T("Els parèntesis canvien el resultat!", "¡Los paréntesis cambian el resultado!")))
ck(Fr(-2, 3) ** 2, Fr(4, 9)); ck(-Fr(2, 3) ** 2, Fr(-4, 9))
P2 = [('(2/3)^5·(2/3)^2:(2/3)^4', r'\left(\dfrac{2}{3}\right)^{5+2-4}=\left(\dfrac{2}{3}\right)^{3}'), ('(3/5)^7:(3/5)^5', r'\left(\dfrac{3}{5}\right)^{7-5}=\left(\dfrac{3}{5}\right)^{2}'),
      ('((-1/2)^3)^2:(-1/2)^4', r'\left(-\dfrac{1}{2}\right)^{6-4}=\left(-\dfrac{1}{2}\right)^{2}'), ('(4/7)^6:(4/7)^5', r'\left(\dfrac{4}{7}\right)^{6-5}=\dfrac{4}{7}'),
      ('((1/3)^2)^2', r'\left(\dfrac{1}{3}\right)^{2\cdot2}=\left(\dfrac{1}{3}\right)^{4}'), ('(5/4)^3·(5/4)^0', r'\left(\dfrac{5}{4}\right)^{3+0}=\left(\dfrac{5}{4}\right)^{3}')]
def pex(e): return ex(e.replace('((', '[(').replace(')^3)^2', ')^3]^2').replace(')^2)^2', ')^2]^2'))
X.append((2, T("Escriu com una sola potència i calcula:", "Escribe como una sola potencia y calcula:") + tasks(2, [pex(e) for e, _ in P2], '8pt')
    + recorda(T(r"amb la mateixa base: $x^m\cdot x^n=x^{m+n}$, \ $x^m:x^n=x^{m-n}$, \ $(x^m)^n=x^{m\cdot n}$.", r"con la misma base: $x^m\cdot x^n=x^{m+n}$, \ $x^m:x^n=x^{m-n}$, \ $(x^m)^n=x^{m\cdot n}$.")),
    tasks(2, [r'$%s=\res{%s}$' % (s, tf(V(e.replace('((', '[(').replace(')^3)^2', ')^3]^2').replace(')^2)^2', ')^2]^2')))) for e, s in P2], '8pt')))
assert V('[(-1/2)^3]^2:(-1/2)^4') == Fr(1, 4) and V('[(1/3)^2]^2') == Fr(1, 81)
X.append((2, T(r"Calcula de la manera més ràpida, fent servir les propietats:", r"Calcula de la manera más rápida, usando las propiedades:")
    + tasks(2, [r"$\left(\dfrac{5}{6}\right)^4\cdot\left(\dfrac{3}{10}\right)^4\cdot4^4$", r"$\left(\dfrac{9}{4}\right)^3:\left(\dfrac{3}{2}\right)^3$"], '6pt'),
    tasks(2, [r"$\left(\dfrac{5}{6}\cdot\dfrac{3}{10}\cdot4\right)^4=1^4=\res{1}$", r"$\left(\dfrac{9}{4}:\dfrac{3}{2}\right)^3=\left(\dfrac{3}{2}\right)^3=\res{\dfrac{27}{8}}$"], '6pt')))
ck(V('(5/6)^4·(3/10)^4·4^4'), 1); ck(V('(9/4)^3:(3/2)^3'), Fr(27, 8))
# operacions combinades amb potències: s'han de fer servir les propietats (els nombres serien massa grans per a fer-ho directament)
PC = [
  (r"\left(\dfrac{2}{3}\right)^5\cdot\left(\dfrac{2}{3}\right)^2:\left(\dfrac{2}{3}\right)^6+\left(\dfrac{1}{2}\right)^2",
   r"\left(\dfrac{2}{3}\right)^{5+2-6}+\dfrac{1}{4}=\dfrac{2}{3}+\dfrac{1}{4}", '(2/3)^5·(2/3)^2:(2/3)^6+(1/2)^2', Fr(11, 12)),
  (r"\left[\left(\dfrac{2}{5}\right)^3\right]^2:\left(\dfrac{2}{5}\right)^4-\left(\dfrac{1}{5}\right)^2\cdot\left(\dfrac{5}{2}\right)^0",
   r"\left(\dfrac{2}{5}\right)^{6-4}-\dfrac{1}{25}\cdot1=\dfrac{4}{25}-\dfrac{1}{25}", '[(2/5)^3]^2:(2/5)^4-(1/5)^2·(5/2)^0', Fr(3, 25)),
  (r"\left(\dfrac{6}{7}\right)^3\cdot\left(\dfrac{7}{3}\right)^3:2^2+\left(-\dfrac{1}{2}\right)^3",
   r"\left(\dfrac{6}{7}\cdot\dfrac{7}{3}\right)^3:2^2-\dfrac{1}{8}=2^3:2^2-\dfrac{1}{8}=2-\dfrac{1}{8}", '(6/7)^3·(7/3)^3:2^2+(-1/2)^3', Fr(15, 8)),
  (r"\left[\left(-\dfrac{2}{3}\right)^2\right]^3:\left(-\dfrac{2}{3}\right)^5-\left(\dfrac{1}{2}-\dfrac{3}{4}\right)^2",
   r"\left(-\dfrac{2}{3}\right)^{6-5}-\left(-\dfrac{1}{4}\right)^2=-\dfrac{2}{3}-\dfrac{1}{16}", '[(-2/3)^2]^3:(-2/3)^5-(1/2-3/4)^2', Fr(-35, 48)),
  (r"\left(\dfrac{5}{4}\right)^4\cdot\left(\dfrac{8}{5}\right)^4:2^4+\left(1-\dfrac{4}{5}\right)^2\cdot5^2",
   r"\left(\dfrac{5}{4}\cdot\dfrac{8}{5}\right)^4:2^4+\left(\dfrac{1}{5}\cdot5\right)^2=2^4:2^4+1^2=1+1", '(5/4)^4·(8/5)^4:2^4+(1-4/5)^2·5^2', Fr(2)),
  (r"\left[\left(\dfrac{1}{2}\right)^3-\left(\dfrac{1}{2}\right)^2\right]:\left(-\dfrac{1}{2}\right)^3-\left(\dfrac{9}{10}\right)^3\cdot\left(\dfrac{5}{3}\right)^3:\left(\dfrac{3}{2}\right)^3",
   r"\left(\dfrac{1}{8}-\dfrac{1}{4}\right):\left(-\dfrac{1}{8}\right)-\left(\dfrac{9}{10}\cdot\dfrac{5}{3}\right)^3:\left(\dfrac{3}{2}\right)^3=\left(-\dfrac{1}{8}\right):\left(-\dfrac{1}{8}\right)-\left(\dfrac{3}{2}\right)^3:\left(\dfrac{3}{2}\right)^3=1-1", '[(1/2)^3-(1/2)^2]:(-1/2)^3-(9/10)^3·(5/3)^3:(3/2)^3', Fr(0)),
]
for _, _, e, v in PC: ck(V(e), v)
X.append((3, T(r"Calcula fent servir les propietats de les potències (sense calcular potències amb exponents grans):", r"Calcula usando las propiedades de las potencias (sin calcular potencias con exponentes grandes):")
    + tasks(2, ['$%s$' % q for q, _, _, _ in PC], '10pt')
    + recorda(T(r"busca bases iguals (sumes o restes els exponents) o exponents iguals (multipliques o divideixes les bases): $\left(\dfrac{6}{7}\right)^3\cdot\left(\dfrac{7}{3}\right)^3=\left(\dfrac{6}{7}\cdot\dfrac{7}{3}\right)^3=2^3$.",
                r"busca bases iguales (sumas o restas los exponentes) o exponentes iguales (multiplicas o divides las bases): $\left(\dfrac{6}{7}\right)^3\cdot\left(\dfrac{7}{3}\right)^3=\left(\dfrac{6}{7}\cdot\dfrac{7}{3}\right)^3=2^3$.")),
    tasks(1, ['$%s=%s=\\res{%s}$' % (q, s, tf(v)) for q, s, _, v in PC], '6pt')))
X.append((3, T(r"Simplifica: \ $\dfrac{\left(\frac{2}{5}\right)^3\cdot\left(\frac{2}{5}\right)^4}{\left[\left(\frac{2}{5}\right)^2\right]^3}$ \qquad i \qquad $\dfrac{\left(-\frac{3}{4}\right)^5\cdot\left(-\frac{3}{4}\right)}{\left(-\frac{3}{4}\right)^3\cdot\left(-\frac{3}{4}\right)^2}$", r"Simplifica: \ $\dfrac{\left(\frac{2}{5}\right)^3\cdot\left(\frac{2}{5}\right)^4}{\left[\left(\frac{2}{5}\right)^2\right]^3}$ \qquad y \qquad $\dfrac{\left(-\frac{3}{4}\right)^5\cdot\left(-\frac{3}{4}\right)}{\left(-\frac{3}{4}\right)^3\cdot\left(-\frac{3}{4}\right)^2}$"),
    r"$\left(\dfrac{2}{5}\right)^{7-6}=\res{\dfrac{2}{5}}$ \qquad $\left(-\dfrac{3}{4}\right)^{6-5}=\res{-\dfrac{3}{4}}$"))
ck(V('(2/5)^3·(2/5)^4:[(2/5)^2]^3'), Fr(2, 5)); ck(V('(-3/4)^5·(-3/4):(-3/4)^3:(-3/4)^2'), Fr(-3, 4))

# =====================================================================
# 10. Operacions combinades
X = sec(T('Operacions combinades', 'Operaciones combinadas'))
C1 = ['1/2+1/3·3/4', '(1/2+1/3)·3/4', '1-2/3:4/9', '3/5+2/5·10/3', '5/2+1/3·4/5', '4/3·(2/5+1/3)']
X.append((1, T("Calcula respectant la jerarquia de les operacions:", "Calcula respetando la jerarquía de las operaciones:") + tasks(3, [ex(e) for e in C1], '8pt')
    + recorda(T(r"ordre: 1) parèntesis; 2) potències; 3) multiplicacions i divisions, d'esquerra a dreta; 4) sumes i restes.", r"orden: 1) paréntesis; 2) potencias; 3) multiplicaciones y divisiones, de izquierda a derecha; 4) sumas y restas.")),
    tasks(1, [steps(e)[0] for e in C1], '4pt')))
C2 = ['1/2-(2/3)^2·3/4', '(2/3)^2-1/3·(2-1/2)', '5/6:(1/2-1/3)-2^2', '(-1/2)^3+3/4:(1-1/3)', '(3/4-1)^2·8+1/2', '21/4-2/5:4/3']
X.append((2, T("Calcula:", "Calcula:") + tasks(2, [ex(e) for e in C2], '8pt'),
    tasks(1, [steps(e)[0] for e in C2], '4pt')))
C3 = ['2-[1/3+(1/2)^2]:5/6', '[3/4-(1/2)^2]^2:(-1/2)^3+5/3·6/5', '(1/4+2/3-1/12)·3+(3/2-5/4):1/2', '3/2:1/4·4/20+3/2·7/5']
X.append((2, T("Calcula:", "Calcula:") + tasks(2, [ex(e) for e in C3], '8pt'),
    tasks(1, [steps(e)[0] for e in C3], '4pt')))
X.append((3, T(r"Calcula: \ $\dfrac{\frac{2}{3}-\frac{1}{4}}{1+\frac{1}{6}}-\left(\dfrac{3}{4}-1\right)^2\cdot8$", r"Calcula: \ $\dfrac{\frac{2}{3}-\frac{1}{4}}{1+\frac{1}{6}}-\left(\dfrac{3}{4}-1\right)^2\cdot8$"),
    r"$\dfrac{\frac{5}{12}}{\frac{7}{6}}-\left(-\dfrac{1}{4}\right)^2\cdot8=\dfrac{30}{84}-\dfrac{1}{16}\cdot8=\dfrac{5}{14}-\dfrac{1}{2}=\res{-\dfrac{1}{7}}$"))
ck(V('(2/3-1/4):(1+1/6)-(3/4-1)^2·8'), Fr(-1, 7))
X.append((3, T(r"Posa els parèntesis necessaris perquè cada igualtat siga certa: \ a) $\dfrac{1}{2}+\dfrac{1}{2}\cdot\dfrac{2}{3}=\dfrac{2}{3}$ \quad b) $1-\dfrac{1}{3}:\dfrac{1}{3}+1=\dfrac{1}{2}$", r"Pon los paréntesis necesarios para que cada igualdad sea cierta: \ a) $\dfrac{1}{2}+\dfrac{1}{2}\cdot\dfrac{2}{3}=\dfrac{2}{3}$ \quad b) $1-\dfrac{1}{3}:\dfrac{1}{3}+1=\dfrac{1}{2}$"),
    r"a) $\res{\left(\dfrac{1}{2}+\dfrac{1}{2}\right)\cdot\dfrac{2}{3}}=\dfrac{2}{3}$ \quad b) $\res{\left(1-\dfrac{1}{3}\right):\left(\dfrac{1}{3}+1\right)}=\dfrac{2}{3}:\dfrac{4}{3}=\dfrac{1}{2}$"))
ck(V('(1/2+1/2)·2/3'), Fr(2, 3)); ck(V('(1-1/3):(1/3+1)'), Fr(1, 2))

# =====================================================================
# 11. Problemes amb fraccions
X = sec(T('Problemes amb fraccions', 'Problemas con fracciones'))
X.append((1, T(r"Dels 28 alumnes d'una classe, $\dfrac{3}{7}$ són xics. Quants xics i quantes xiques hi ha?", r"De los 28 alumnos de una clase, $\dfrac{3}{7}$ son chicos. ¿Cuántos chicos y cuántas chicas hay?"),
    T(r"$\dfrac{3}{7}\cdot28=\res{12\text{ xics}}$; \ $28-12=\res{16\text{ xiques}}$", r"$\dfrac{3}{7}\cdot28=\res{12\text{ chicos}}$; \ $28-12=\res{16\text{ chicas}}$")))
ck(Fr(3, 7) * 28, 12)
X.append((1, T(r"He llegit 120 pàgines d'un llibre, que són els $\dfrac{3}{5}$ del total. Quantes pàgines té el llibre? Quantes me'n queden?", r"He leído 120 páginas de un libro, que son los $\dfrac{3}{5}$ del total. ¿Cuántas páginas tiene el libro? ¿Cuántas me quedan?"),
    T(r"$120:\dfrac{3}{5}=\dfrac{120\cdot5}{3}=\res{200\text{ pàgines}}$; \ me'n queden $\res{80}$.", r"$120:\dfrac{3}{5}=\dfrac{120\cdot5}{3}=\res{200\text{ páginas}}$; \ me quedan $\res{80}$.")))
ck(120 / Fr(3, 5), 200)
X.append((1, T(r"Un entrepà costa $3{,}60$ € i el pa en representa $\dfrac{1}{4}$; el pernil, $\dfrac{2}{3}$. Quant costa el pa? I el pernil? Quant costa la resta?", r"Un bocadillo cuesta $3{,}60$ € y el pan representa $\dfrac{1}{4}$; el jamón, $\dfrac{2}{3}$. ¿Cuánto cuesta el pan? ¿Y el jamón? ¿Cuánto cuesta el resto?"),
    T(r"Pa: $\res{0{,}90\text{ €}}$; \ pernil: $\res{2{,}40\text{ €}}$; \ resta: $3{,}60-0{,}90-2{,}40=\res{0{,}30\text{ €}}$", r"Pan: $\res{0{,}90\text{ €}}$; \ jamón: $\res{2{,}40\text{ €}}$; \ resto: $3{,}60-0{,}90-2{,}40=\res{0{,}30\text{ €}}$")))
ck(Fr('3.6') / 4, Fr('0.9')); ck(Fr('3.6') * Fr(2, 3), Fr('2.4')); ck(Fr('3.6') - Fr('0.9') - Fr('2.4'), Fr('0.3'))
X.append((2, T(r"De tot un sopar, en Joan s'ha menjat $\dfrac{1}{7}$, l'Elena $\dfrac{2}{5}$ i la Maite $\dfrac{1}{8}$. Quina fracció s'han menjat entre tots tres? Quina fracció n'ha sobrat? Qui ha menjat més?", r"De toda una cena, Joan se ha comido $\dfrac{1}{7}$, Elena $\dfrac{2}{5}$ y Maite $\dfrac{1}{8}$. ¿Qué fracción se han comido entre los tres? ¿Qué fracción ha sobrado? ¿Quién ha comido más?"),
    T(r"$\dfrac{40+112+35}{280}=\res{\dfrac{187}{280}}$; \ sobra $\res{\dfrac{93}{280}}$. \ Ha menjat més \rest{l'Elena}.", r"$\dfrac{40+112+35}{280}=\res{\dfrac{187}{280}}$; \ sobra $\res{\dfrac{93}{280}}$. \ Ha comido más \rest{Elena}.")))
ck(Fr(1, 7) + Fr(2, 5) + Fr(1, 8), Fr(187, 280)); assert Fr(2, 5) > Fr(1, 7) and Fr(2, 5) > Fr(1, 8)
X.append((2, T(r"Un dipòsit de 240 L està ple. El dilluns se'n gasta $\dfrac{1}{4}$ i el dimarts, $\dfrac{2}{3}$ del que quedava. Quants litres queden? Quina fracció del dipòsit és?", r"Un depósito de 240 L está lleno. El lunes se gasta $\dfrac{1}{4}$ y el martes, $\dfrac{2}{3}$ de lo que quedaba. ¿Cuántos litros quedan? ¿Qué fracción del depósito es?"),
    T(r"Dilluns: 60 L, queden 180 L. \ Dimarts: $\dfrac{2}{3}\cdot180=120$ L. \ Queden $\res{60\text{ L}}$, \ que és $\res{\dfrac{1}{4}}$ del dipòsit.", r"Lunes: 60 L, quedan 180 L. \ Martes: $\dfrac{2}{3}\cdot180=120$ L. \ Quedan $\res{60\text{ L}}$, \ que es $\res{\dfrac{1}{4}}$ del depósito.")))
ck(240 - 60 - Fr(2, 3) * 180, 60)
X.append((2, T(r"En una votació, $\dfrac{3}{8}$ dels votants voten sí, $\dfrac{1}{3}$ voten no i la resta, 14 persones, s'abstenen. Quantes persones han votat?", r"En una votación, $\dfrac{3}{8}$ de los votantes votan sí, $\dfrac{1}{3}$ votan no y el resto, 14 personas, se abstienen. ¿Cuántas personas han votado?"),
    T(r"$\dfrac{3}{8}+\dfrac{1}{3}=\dfrac{17}{24}$; \ s'abstenen $\dfrac{7}{24}$, que són 14: \ $14:\dfrac{7}{24}=\res{48\text{ persones}}$", r"$\dfrac{3}{8}+\dfrac{1}{3}=\dfrac{17}{24}$; \ se abstienen $\dfrac{7}{24}$, que son 14: \ $14:\dfrac{7}{24}=\res{48\text{ personas}}$")))
ck(14 / (1 - Fr(3, 8) - Fr(1, 3)), 48)
X.append((2, T(r"Una ampolla plena pesa $1{,}2$ kg i, quan n'hem buidat $\dfrac{3}{4}$, pesa $0{,}48$ kg. Quant pesa l'ampolla buida?", r"Una botella llena pesa $1{,}2$ kg y, cuando hemos vaciado $\dfrac{3}{4}$, pesa $0{,}48$ kg. ¿Cuánto pesa la botella vacía?"),
    T(r"$\dfrac{3}{4}$ del líquid pesen $1{,}2-0{,}48=0{,}72$ kg; \ tot el líquid: $0{,}72:\dfrac{3}{4}=0{,}96$ kg; \ ampolla: $1{,}2-0{,}96=\res{0{,}24\text{ kg}}$", r"$\dfrac{3}{4}$ del líquido pesan $1{,}2-0{,}48=0{,}72$ kg; \ todo el líquido: $0{,}72:\dfrac{3}{4}=0{,}96$ kg; \ botella: $1{,}2-0{,}96=\res{0{,}24\text{ kg}}$")))
ck(Fr('0.72') / Fr(3, 4), Fr('0.96')); ck(Fr('1.2') - Fr('0.96'), Fr('0.24'))
X.append((3, T(r"La Marta gasta $\dfrac{2}{5}$ de la paga en roba i $\dfrac{1}{3}$ del que li queda en el cine. Encara li queden 24 €. Quant cobrava de paga?", r"Marta gasta $\dfrac{2}{5}$ de la paga en ropa y $\dfrac{1}{3}$ de lo que le queda en el cine. Todavía le quedan 24 €. ¿Cuánto cobraba de paga?"),
    T(r"Cine: $\dfrac{1}{3}\cdot\dfrac{3}{5}=\dfrac{1}{5}$. \ Gasta $\dfrac{2}{5}+\dfrac{1}{5}=\dfrac{3}{5}$ i li queden $\dfrac{2}{5}$, que són 24 €: \ $24:\dfrac{2}{5}=\res{60\text{ €}}$", r"Cine: $\dfrac{1}{3}\cdot\dfrac{3}{5}=\dfrac{1}{5}$. \ Gasta $\dfrac{2}{5}+\dfrac{1}{5}=\dfrac{3}{5}$ y le quedan $\dfrac{2}{5}$, que son 24 €: \ $24:\dfrac{2}{5}=\res{60\text{ €}}$")))
ck(24 / (1 - Fr(2, 5) - Fr(1, 3) * Fr(3, 5)), 60)
X.append((3, T(r"Un ciclista fa $\dfrac{2}{7}$ d'una etapa al matí i $\dfrac{3}{5}$ del que li queda a la vesprada. Encara li falten 40 km. Quants quilòmetres té l'etapa? Quants n'ha fet al matí?", r"Un ciclista hace $\dfrac{2}{7}$ de una etapa por la mañana y $\dfrac{3}{5}$ de lo que le queda por la tarde. Todavía le faltan 40 km. ¿Cuántos kilómetros tiene la etapa? ¿Cuántos ha hecho por la mañana?"),
    T(r"Falten $\dfrac{2}{5}\cdot\dfrac{5}{7}=\dfrac{2}{7}$ de l'etapa, que són 40 km: \ $40:\dfrac{2}{7}=\res{140\text{ km}}$. \ Al matí: $\dfrac{2}{7}\cdot140=\res{40\text{ km}}$", r"Faltan $\dfrac{2}{5}\cdot\dfrac{5}{7}=\dfrac{2}{7}$ de la etapa, que son 40 km: \ $40:\dfrac{2}{7}=\res{140\text{ km}}$. \ Por la mañana: $\dfrac{2}{7}\cdot140=\res{40\text{ km}}$")))
ck(40 / (Fr(2, 5) * Fr(5, 7)), 140); ck(Fr(2, 7) * 140, 40)
X.append((3, T(r"Un pare reparteix 180 € entre els seus tres fills: al major li dona $\dfrac{2}{5}$, al mitjà $\dfrac{5}{8}$ del que queda i al menor, la resta. Quant rep cada un? Quina fracció del total rep el menor?", r"Un padre reparte 180 € entre sus tres hijos: al mayor le da $\dfrac{2}{5}$, al mediano $\dfrac{5}{8}$ de lo que queda y al pequeño, el resto. ¿Cuánto recibe cada uno? ¿Qué fracción del total recibe el pequeño?"),
    T(r"Major: $\dfrac{2}{5}\cdot180=\res{72\text{ €}}$; queden 108 €. \ Mitjà: $\dfrac{5}{8}\cdot108=\res{67{,}50\text{ €}}$. \ Menor: $108-67{,}50=\res{40{,}50\text{ €}}$, \ que és $\dfrac{40{,}5}{180}=\res{\dfrac{9}{40}}$ del total.", r"Mayor: $\dfrac{2}{5}\cdot180=\res{72\text{ €}}$; quedan 108 €. \ Mediano: $\dfrac{5}{8}\cdot108=\res{67{,}50\text{ €}}$. \ Pequeño: $108-67{,}50=\res{40{,}50\text{ €}}$, \ que es $\dfrac{40{,}5}{180}=\res{\dfrac{9}{40}}$ del total.")))
ck(Fr(2, 5) * 180, 72); ck(Fr(5, 8) * 108, Fr('67.5')); ck(Fr('40.5') / 180, Fr(9, 40)); ck(Fr(3, 8) * Fr(3, 5), Fr(9, 40))
X.append((3, T(r"En una pastisseria fan 150 croissants. Al matí en venen $\dfrac{3}{5}$ i a la vesprada, $\dfrac{3}{4}$ dels que queden. Els que sobren es venen a meitat de preu, a $0{,}60$ € cada un. Quants en sobren i quant es recapta per ells?", r"En una pastelería hacen 150 cruasanes. Por la mañana venden $\dfrac{3}{5}$ y por la tarde, $\dfrac{3}{4}$ de los que quedan. Los que sobran se venden a mitad de precio, a $0{,}60$ € cada uno. ¿Cuántos sobran y cuánto se recauda por ellos?"),
    T(r"Matí: 90, queden 60. \ Vesprada: $\dfrac{3}{4}\cdot60=45$. \ Sobren $\res{15}$ croissants: $15\cdot0{,}60=\res{9\text{ €}}$", r"Mañana: 90, quedan 60. \ Tarde: $\dfrac{3}{4}\cdot60=45$. \ Sobran $\res{15}$ cruasanes: $15\cdot0{,}60=\res{9\text{ €}}$")))
ck(Fr(3, 5) * 150, 90); ck(Fr(3, 4) * 60, 45); ck(15 * Fr('0.6'), 9)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T('nombres decimals, decimals exactes i periòdics, operacions amb decimals, fraccions equivalents, fracció generatriu, operacions amb fraccions, potències de fraccions, operacions combinades, problemes amb fraccions',
       'números decimales, decimales exactos y periódicos, operaciones con decimales, fracciones equivalentes, fracción generatriz, operaciones con fracciones, potencias de fracciones, operaciones combinadas, problemas con fracciones')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T('Decimals i fraccions', 'Decimales y fracciones')

def build(sol):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 2: %s' % (t, TIT), capcalera='%s · Unidad 2: %s' % (t, TIT), pdfkeywords=KW, curs='2eso')
        cap = assignatura('2eso') + '{' + ('Soluciones de la ficha · Unidad 2' if sol else 'Ficha de ejercicios · Unidad 2') + '}{' + TIT + '}'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat 2: %s. 2n d'ESO}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 2: %s · 2n d'ESO" % (t, TIT))
        assert 'Unitat 2' in p and 'unitat 2' in p
        cap = r'\capcalera{Matemàtiques}{2n ESO}{' + ('Solucions de la fitxa · Unitat 2' if sol else "Fitxa d'exercicis · Unitat 2") + '}{' + TIT + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{12}\n\\input{../comu/fentmates.tex}\n\\fmcurs{2eso}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb les eines interactives dels apunts de la unitat. Les fraccions s'han de donar en forma irreductible.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con las herramientas interactivas de los apuntes de la unidad. Las fracciones se tienen que dar en forma irreducible.") if sol else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i sense calculadora. Dona les fraccions en forma irreductible. Les seccions segueixen l'ordre dels apunts de la unitat (2.1--2.11).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y sin calculadora. Da las fracciones en forma irreducible. Las secciones siguen el orden de los apuntes de la unidad (2.1--2.11)."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't2-fitxa-%s%s.tex' % ('solucions' if sol else 'exercicis', '-es' if ES else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
n = sum(len(x[1]) for x in S)
print(n, T('exercicis,', 'ejercicios,'), len(CHK), T('comprovacions', 'comprobaciones'))
