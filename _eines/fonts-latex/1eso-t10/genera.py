# Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex
# (1r ESO, Unitat 10: Estadística — població, mostra i variables, freqüències i taules de freqüències,
# gràfics estadístics, moda, mitjana i mediana, rang i desviació mitjana)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les comprovacions CHK (amb fraccions exactes) verifiquen cada resultat escrit.
import os, re, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def center(t): return r'\par\smallskip\begin{center}' + t + r'\end{center}'
def side(*figs): return r'\par\smallskip\begin{center}' + r'\hspace{0.8cm}'.join(figs) + r'\end{center}'

# ---------- comprovacions i estadística exacta ----------
NCHK = [0]
def CHK(cond, *info):
    NCHK[0] += 1
    assert cond, info
def fr(v): return v if isinstance(v, Fr) else Fr(str(v).replace('{,}', '.').replace(',', '.'))
def EQ(a, b): CHK(fr(a) == fr(b), a, b)
def freqs(data, order=None):
    keys = order or sorted(set(data))
    return [(k, data.count(k)) for k in keys]
def expand(tab): return [x for x, f in tab for _ in range(f)]
def mean(d): return Fr(sum(fr(x) for x in d), len(d))
def median(d):
    s = sorted(fr(x) for x in d); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
def modes(d):
    c = {x: d.count(x) for x in d}; m = max(c.values()); return sorted(k for k in c if c[k] == m)
def rang(d): return fr(max(d)) - fr(min(d))
def dm(d):
    m = mean(d); return Fr(sum(abs(fr(x) - m) for x in d), len(d))
def acc(fs):
    s, o = 0, []
    for f in fs: s += f; o.append(s)
    return o

# ---------- nombres ----------
def tn(v):
    v = fr(v)
    if v.denominator == 1: return str(v.numerator)
    t = ('%.6f' % float(v)).rstrip('0').rstrip('.')
    CHK(fr(t) == v, v)
    return t.replace('.', '{,}')
def tr(v, d=2):
    """arrodonit (amb ≈ si cal)"""
    v = fr(v); t = ('%.*f' % (d, float(v))).rstrip('0').rstrip('.')
    return ('=' if fr(t) == v else r'\approx ') + t.replace('.', '{,}')
def lst(d): return r',\ \allowbreak '.join(tn(x) for x in d)  # les llistes llargues poden partir-se entre línies

# ---------- taules ----------
def ftab(xs, fs, cols=('f',), xl='$x_i$', N=None):
    """taula de freqüències vertical; cols: f, F (acumulada), h (relativa), p (%), xf (x·f)"""
    N = N or sum(fs); F = acc(fs)
    H = {'f': '$f_i$', 'F': '$F_i$', 'h': '$h_i$', 'p': r'\%', 'xf': r'$x_i\cdot f_i$'}
    head = xl + ' & ' + ' & '.join(H[c] for c in cols)
    rows = []
    for i, (x, f) in enumerate(zip(xs, fs)):
        r = [x if isinstance(x, str) else '$%s$' % tn(x)]
        for c in cols:
            r.append({'f': '$%d$' % f, 'F': '$%d$' % F[i], 'h': '$%s$' % (tn(Fr(f, N)) if Fr(f, N).denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100) else r'\frac{%d}{%d}%s' % (f, N, tr(Fr(f, N)))),
                      'p': '$%s$' % (tn(Fr(100 * f, N)) if Fr(100 * f, N).denominator in (1, 2, 4, 5, 10) else tr(Fr(100 * f, N), 1)[1:] if tr(Fr(100 * f, N), 1)[0] == '=' else tr(Fr(100 * f, N), 1)),
                      'xf': '$%s$' % tn(fr(x) * f) if not isinstance(x, str) else ''}[c])
        rows.append(' & '.join(r))
    tot = [r'\textbf{Total}'] + [{'f': '$%d$' % N, 'F': '', 'h': '$1$', 'p': '$100$', 'xf': '$%s$' % tn(sum(fr(x) * f for x, f in zip(xs, fs))) if not isinstance(xs[0], str) else ''}[c] for c in cols]
    return (r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|%s|}\hline ' % '|'.join('c' * len(cols)) + head + r'\\\hline '
            + r'\\\hline '.join(rows) + r'\\\hline ' + ' & '.join(tot) + r'\\\hline\end{tabular}}')
def htab(xs, fs, xl='$x_i$', fl='$f_i$', w='0.9cm'):
    """taula horitzontal (fs pot portar textos buits o «$a$»)"""
    cell = lambda v: v if isinstance(v, str) else '$%s$' % tn(v)
    return (r'{\renewcommand{\arraystretch}{1.3}\begin{tabular}{|c|%s|}\hline %s & %s\\\hline %s & %s\\\hline\end{tabular}}'
            % ('|'.join(['C{%s}' % w] * len(xs)), xl, ' & '.join(cell(x) for x in xs), fl, ' & '.join(cell(f) for f in fs)))
def ivl(a, b): return '$[%s,\\ %s)$' % (tn(a), tn(b))

# ---------- gràfics (TikZ) ----------
COLS = ['teal', 'accent', 'violet', 'gold', 'navy', 'muted']
def nice(top):
    for st in (1, 2, 5, 10, 20, 25, 50, 100):
        if top / st <= 8: return st
    return 200
def taxes(n_or_w, H, top, st, y0=0, yl='', xl='', W=None):
    o = []
    k = y0
    while k <= top + 1e-9:
        y = H * (k - y0) / (top - y0)
        o.append(r'\draw[muted!30,line width=0.3pt] (0,%.3f)--(%.3f,%.3f); \node[left,font=\tiny,text=muted,inner sep=1.5pt] at (0,%.3f) {$%s$};' % (y, W, y, y, tn(k)))
        k += st
    o.append(r'\draw[-latex,muted,line width=0.6pt] (0,0)--(%.3f,0) node[right,font=\scriptsize,text=navy]{%s};' % (W + 0.3, xl))
    o.append(r'\draw[-latex,muted,line width=0.6pt] (0,0)--(0,%.3f) node[above,font=\scriptsize,text=navy]{%s};' % (H + 0.35, yl))
    return o
def tbar(cats, vals, kind='bar', yl='$f_i$', xl='', H=2.8, dx=0.9, step=None, y0=0, top=None, multi=False, series=None):
    """diagrama de barres ('bar'), polígon ('poly') o els dos ('both'); series: [(vals, color)] per a diversos polígons"""
    n = len(cats); allv = list(vals) + [v for s, _ in (series or []) for v in s]
    top = top or max(allv); st = step or nice(top - y0); top = math.ceil(top / st) * st
    W = dx * n + 0.2
    o = [r'\begin{tikzpicture}[baseline=(current bounding box.center),line cap=round,line join=round]'] + taxes(n, H, top, st, y0, yl, xl, W)
    Y = lambda v: H * (float(v) - y0) / (top - y0)
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = dx * (i + 0.5) + 0.1
        if kind in ('bar', 'both'):
            col = COLS[i % 4] if multi else 'teal'
            o.append(r'\draw[%s,fill=%s!35] (%.3f,0) rectangle (%.3f,%.3f);' % (col, col, x - dx * 0.3, x + dx * 0.3, Y(v)))
        o.append(r'\node[below,font=\scriptsize,inner sep=2pt] at (%.3f,0) {%s};' % (x, c))
    for s, col in ([(vals, 'violet')] if kind in ('poly', 'both') else []) + (series or []):
        P = ['(%.3f,%.3f)' % (dx * (i + 0.5) + 0.1, Y(v)) for i, v in enumerate(s)]
        o.append(r'\draw[%s,line width=1.1pt] %s;' % (col, '--'.join(P)))
        o += [r'\fill[%s] %s circle (1.6pt);' % (col, p) for p in P]
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def thist(edges, vals, poly=False, yl='$f_i$', xl='', H=2.8, W=5.2, step=None):
    a, b = edges[0], edges[-1]; top = max(vals); st = step or nice(top); top = math.ceil(top / st) * st
    X = lambda x: 0.3 + (W - 0.6) * (float(x) - a) / (b - a); Y = lambda v: H * float(v) / top
    o = [r'\begin{tikzpicture}[baseline=(current bounding box.center),line cap=round,line join=round]'] + taxes(0, H, top, st, 0, yl, xl, W)
    for i, v in enumerate(vals):
        o.append(r'\draw[teal,fill=teal!30] (%.3f,0) rectangle (%.3f,%.3f);' % (X(edges[i]), X(edges[i + 1]), Y(v)))
    for e in edges: o.append(r'\node[below,font=\tiny,inner sep=2pt] at (%.3f,0) {$%s$};' % (X(e), tn(e)))
    if poly:
        d = edges[1] - edges[0]
        P = [(a - Fr(d, 2), 0)] + [(Fr(edges[i] + edges[i + 1], 2), v) for i, v in enumerate(vals)] + [(b + Fr(d, 2), 0)]
        P = [(max(min(fr(x), b + Fr(3, 10) * (b - a) / (W - 0.6)), a - Fr(3, 10) * (b - a) / (W - 0.6)), y) for x, y in P]
        Q = ['(%.3f,%.3f)' % (X(x), Y(y)) for x, y in P]
        o.append(r'\draw[violet,line width=1.1pt] %s;' % '--'.join(Q))
        o += [r'\fill[violet] %s circle (1.5pt);' % q for q in Q[1:-1]]
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def tpie(cats, vals, r=1.45, lab='angle', N=None):
    """diagrama de sectors; lab: 'angle', 'pct' o None"""
    N = N or sum(vals); o = [r'\begin{tikzpicture}[baseline=(current bounding box.center)]']; a0 = Fr(90)
    for i, v in enumerate(vals):
        a1 = a0 - Fr(360 * v, N); col = COLS[i % 6]
        o.append(r'\fill[%s!70,draw=white,line width=0.8pt] (0,0)--(%.3f:%s) arc[start angle=%.3f,end angle=%.3f,radius=%scm]--cycle;' % (col, float(a0), r, float(a0), float(a1), r))
        if lab and 360 * v >= 30 * N:
            t = ('$%s^\\circ$' % tn(Fr(360 * v, N))) if lab == 'angle' else ('$%s\\,\\%%$' % tn(Fr(100 * v, N)))
            o.append(r'\node[font=\scriptsize\bfseries,text=white] at (%.3f:%.3f) {%s};' % (float((a0 + a1) / 2), r * 0.62, t))
        a0 = a1
    for i, c in enumerate(cats):
        y = 0.35 * (len(cats) - 1) / 2 * 1.0 - 0.35 * i
        o.append(r'\fill[%s!70] (%.2f,%.3f) rectangle ++(0.22,0.22); \node[right,font=\scriptsize] at (%.2f,%.3f) {%s};' % (COLS[i % 6], r + 0.4, y - 0.11, r + 0.65, y, c))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def tpicto(cats, vals, unit, icon=r'\faBicycle', col='accent'):
    o = [r'\begin{tikzpicture}[baseline=(current bounding box.center)]']
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = -0.55 * i; q = Fr(v, unit); k = 0
        o.append(r'\node[left,font=\small] at (0,%.2f) {%s};' % (y, c))
        while q > 0:
            part = min(q, 1); x = 0.25 + 0.6 * k
            if part == 1: o.append(r'\node[text=%s,font=\large] at (%.2f,%.2f) {%s};' % (col, x, y, icon))
            else: o.append(r'\begin{scope}\clip (%.2f,%.2f) rectangle (%.3f,%.2f); \node[text=%s,font=\large] at (%.2f,%.2f) {%s};\end{scope}' % (x - 0.3, y - 0.3, x - 0.25 + 0.5 * float(part), y + 0.3, col, x, y, icon))
            q -= part; k += 1
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Població, mostra i variables estadístiques
# =====================================================================
V11 = [('nombre de fills', 'discreta'), ('color preferit', 'qualitativa'), ('temps a córrer 100\\,m', 'contínua'), ("pàgines d'un llibre", 'discreta'),
       ('professió', 'qualitativa'), ("temperatura d'una ciutat", 'contínua'), ('número de calçat', 'discreta'), ('idioma matern', 'qualitativa'), ("capacitat d'una botella", 'contínua')]
S_.append(("Població, mostra i variables estadístiques", [
 (1, r"Classifica aquestes variables en qualitatives, quantitatives discretes o quantitatives contínues:" + tasks(3, [v for v, _ in V11])
     + recorda(r"Si els valors no són nombres, la variable és \textbf{qualitativa}. Si són nombres: es \textbf{compten} $\to$ \textbf{discreta}; es \textbf{mesuren} $\to$ \textbf{contínua}."),
     tasks(3, [r'\rest{%s}' % t for _, t in V11])),
 (1, r"Per a conéixer quantes hores de televisió veuen a la setmana els 450 alumnes d'un institut, se n'enquesta 60 triats a l'atzar. Indica la població, la mostra, la grandària de la mostra, un individu i la variable estudiada (i de quin tipus és).",
     r"Població: \rest{els 450 alumnes de l'institut}. Mostra: \rest{els 60 alumnes enquestats}; grandària \rest{60}. Individu: \rest{cada alumne}. Variable: \rest{hores de televisió setmanals}, quantitativa \rest{contínua}."),
 (1, r"En cada cas, digues si s'estudia tota la població o una mostra:" + tasks(1, [r"La tutora calcula la nota mitjana de la seua classe amb les notes de tots els alumnes.",
                                                                                     r"Per a saber quant duren les piles d'una fàbrica, se'n proven 50.",
                                                                                     r"Una empresa pregunta a 2\,000 persones a qui votaran en les eleccions.",
                                                                                     r"L'entrenador mesura l'alçada de tots els jugadors del seu equip."]),
     tasks(4, [r'\rest{Població}', r'\rest{Mostra}', r'\rest{Mostra}', r'\rest{Població}'])),
 (2, r"Explica per què, en aquests estudis, cal treballar amb una mostra i no amb tota la població:" + tasks(1, [r"la qualitat dels iogurts que fa una fàbrica;", r"l'opinió de tots els joves d'Espanya sobre les xarxes socials;", r"el temps que tarden a fondre's les bombetes d'un lot de 10\,000."]),
     tasks(1, [r"Per a provar un iogurt cal obrir-lo: si els provàrem tots, \rest{no en quedaria cap per a vendre}.", r"Són \rest{massa persones}: costaria molts diners i molt de temps.", r"La prova \rest{destrueix} les bombetes, i a més és lenta i cara."])),
 (2, r"Raona si aquestes mostres són representatives:" + tasks(1, [r"Per a saber quantes hores d'esport fan els alumnes d'un institut, es pregunta a 30 persones que ixen del gimnàs.",
                                                                    r"Per a saber el plat preferit dels alumnes d'un institut, es trien a l'atzar 10 alumnes de cada curs.",
                                                                    r"Per a saber quina música agrada més a la gent del poble, Laura pregunta als seus amics."]),
     tasks(1, [r"\rest{No}: els qui ixen del gimnàs segurament fan més esport que la resta.", r"\rest{Sí}: hi ha alumnes de tots els cursos triats a l'atzar.", r"\rest{No}: els amics de Laura tenen gustos semblants i són de la mateixa edat."])),
 (2, r"Escriu tres valors possibles de cada variable i classifica-la:" + tasks(3, [r"pes d'un gos", r"nacionalitat", r"nombre de cosins"]),
     tasks(3, [r"12,5\,kg; 30\,kg; 7,2\,kg: \rest{contínua}", r"italiana, xinesa, marroquina: \rest{qualitativa}", r"0, 3, 8: \rest{discreta}"])),
 (3, r"Vols saber quant de temps dediquen a llegir cada setmana els 600 alumnes del teu institut. Descriu com faries l'estudi: quina és la població, com triaries una mostra representativa de 60 alumnes, quina pregunta faries i de quin tipus seria la variable.",
     r"Resposta oberta. Per exemple: població, \rest{els 600 alumnes}; mostra, \rest{6 alumnes triats a l'atzar de cadascun dels 10 grups} (així hi ha alumnes de tots els cursos); pregunta: «Quantes hores llegeixes a la setmana?»; variable quantitativa \rest{contínua}."),
]))

# =====================================================================
# 2. Freqüències absolutes i relatives
# =====================================================================
MAS = [0, 1, 2, 1, 0, 3, 1, 1, 2, 0, 1, 4, 2, 1, 0, 1, 2, 1, 3, 1]
TM = freqs(MAS); CHK(TM == [(0, 4), (1, 9), (2, 4), (3, 2), (4, 1)] and len(MAS) == 20)
SANG = ['A', 'O', 'O', 'A', 'B', 'O', 'A', 'AB', 'O', 'O', 'A', 'B', 'O', 'A', 'O', 'O', 'A', 'B', 'O', 'A', 'AB', 'O', 'A', 'O', 'A']
TS = freqs(SANG, ['A', 'O', 'B', 'AB']); CHK(TS == [('A', 9), ('O', 11), ('B', 3), ('AB', 2)] and len(SANG) == 25)
C24 = [('Futbol', 14, None, None), ('Bàsquet', None, '0{,}25', None), ('Tenis', None, None, 15), ('Natació', 8, None, None), ('Altres', None, None, None)]
# N = 40: futbol 14, bàsquet 10, tenis 6, natació 8, altres 2
C24s = [14, 10, 6, 8, 2]; CHK(sum(C24s) == 40 and Fr(10, 40) == Fr(1, 4) and Fr(6, 40) * 100 == 15)
D25 = [9, 11, 10, 8, 12]; CHK(60 - sum(D25) == 10 and Fr(11 + 8 + 10, 60) * 100 == Fr(145, 3))
S_.append(("Freqüències absolutes i relatives", [
 (1, r"@@MAS@@Aquestes són les mascotes que tenen 20 alumnes: \ $%s$. \ Fes el recompte i la taula amb les freqüències absolutes, relatives i els percentatges." % lst(MAS)
     + recorda(r"Freqüència absoluta $f_i$: vegades que apareix un valor. Freqüència relativa: $h_i=\dfrac{f_i}{N}$. Percentatge: $h_i\cdot100$."),
     center(ftab([x for x, _ in TM], [f for _, f in TM], ('f', 'h', 'p')))),
 (1, r"@@SANG@@Aquests són els grups sanguinis de 25 persones: \ %s. \ Fes la taula de freqüències absolutes, relatives i percentatges." % ', '.join(SANG),
     center(ftab([x for x, _ in TS], [f for _, f in TS], ('f', 'h', 'p'), xl='Grup'))),
 (1, r"Escriu com a percentatge:" + tasks(4, [r'$0{,}3$', r'$0{,}05$', r'$\frac{3}{4}$', r'$\frac{7}{20}$']) + r"\par I com a freqüència relativa decimal:" + tasks(4, [r'$12\,\%$', r'$60\,\%$', r'$7{,}5\,\%$', r'$100\,\%$']),
     tasks(4, [r'$\res{30\,\%}$', r'$\res{5\,\%}$', r'$\res{75\,\%}$', r'$\res{35\,\%}$']) + tasks(4, [r'$\res{0{,}12}$', r'$\res{0{,}6}$', r'$\res{0{,}075}$', r'$\res{1}$'])),
 (2, r"Completa la taula de l'esport preferit de 40 alumnes:" + center(r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|C{1.2cm}|C{1.2cm}|C{1.2cm}|}\hline Esport & $f_i$ & $h_i$ & \%\\\hline Futbol & 14 & & \\\hline Bàsquet & & $0{,}25$ & \\\hline Tenis & & & 15\\\hline Natació & 8 & & \\\hline Altres & & & \\\hline \textbf{Total} & 40 & & \\\hline\end{tabular}}'),
     center(ftab(['Futbol', 'Bàsquet', 'Tenis', 'Natació', 'Altres'], C24s, ('f', 'h', 'p'), xl='Esport')) + r"Bàsquet: $0{,}25\cdot40=10$; tenis: $0{,}15\cdot40=6$; altres: $40-(14+10+6+8)=\res{2}$."),
 (2, r"Hem llançat un dau 60 vegades. Ha eixit l'1 nou vegades, el 2 onze, el 3 deu, el 4 huit, el 5 dotze i el 6 la resta. Quantes vegades ha eixit el 6? Quin percentatge dels llançaments ha eixit un nombre parell? I un nombre més gran que 4?",
     r"$f_6=60-50=\res{10}$. \ Parells: $11+8+10=29$; \ $\frac{29}{60}\approx\res{48{,}3\,\%}$. \ Més gran que 4: $12+10=22$; \ $\frac{22}{60}\approx\res{36{,}7\,\%}$."),
 (2, r"En un institut de 120 alumnes, el $35\,\%$ va a peu. Quants alumnes són? Si 18 alumnes van en bici, quina és la freqüència relativa d'aquest valor?",
     r"$0{,}35\cdot120=\res{42}$ alumnes. \ $h=\frac{18}{120}=\res{0{,}15}$ (el $15\,\%$)."),
 (3, r"En una classe, la freqüència relativa dels alumnes que porten ulleres és $0{,}2$, i en són 6. Quants alumnes hi ha a la classe? Quants no porten ulleres?",
     r"$0{,}2\cdot N=6\Rightarrow N=6:0{,}2=\res{30}$ alumnes. \ No en porten: $30-6=\res{24}$."),
 (3, r"Una variable pren tres valors, $A$, $B$ i $C$. La freqüència relativa d'$A$ és $0{,}25$; la de $B$, $0{,}4$, i la freqüència absoluta de $B$ és 16. Calcula $N$, la freqüència relativa de $C$ i totes les freqüències absolutes.",
     r"$0{,}4\cdot N=16\Rightarrow N=\res{40}$. \ $h_C=1-0{,}25-0{,}4=\res{0{,}35}$. \ $f_A=0{,}25\cdot40=\res{10}$, \ $f_B=\res{16}$, \ $f_C=0{,}35\cdot40=\res{14}$."),
]))
EQ(fr('0.35') * 120, 42); EQ(Fr(18, 120), '0.15'); EQ(6 / fr('0.2'), 30); EQ(16 / fr('0.4'), 40); EQ(fr('0.35') * 40, 14); EQ(fr('0.25') * 40, 10)
CHK(round(29 / 60 * 100, 1) == 48.3 and round(22 / 60 * 100, 1) == 36.7)

# =====================================================================
# 3. Taules de freqüències
# =====================================================================
NOT = [5, 7, 6, 4, 6, 8, 5, 6, 3, 7, 5, 9, 6, 2, 7, 6, 5, 8, 4, 6, 10, 7, 5, 3, 6, 8, 4, 7, 5, 9]
TN = freqs(NOT); CHK(TN == [(2, 1), (3, 2), (4, 3), (5, 6), (6, 7), (7, 5), (8, 3), (9, 2), (10, 1)] and len(NOT) == 30)
XN, FN = [x for x, _ in TN], [f for _, f in TN]; AN = acc(FN)
PES = [42, 51, 38, 47, 55, 44, 49, 36, 52, 46, 41, 58, 48, 45, 50, 39, 53, 47, 43, 56, 49, 40, 45, 51]
EP = [35, 40, 45, 50, 55, 60]; FP = [sum(1 for p in PES if EP[i] <= p < EP[i + 1]) for i in range(5)]
CHK(len(PES) == 24 and FP == [3, 5, 8, 5, 3], FP)
CUR = [13.8, 15.2, 14.1, 12.6, 16.3, 14.9, 13.2, 15.7, 14.4, 13.9, 15.1, 12.9, 14.6, 16.8, 13.5, 14.2, 15.5, 14.8, 13.1, 15.9]
EC = [12, 13, 14, 15, 16, 17]; FC = [sum(1 for c in CUR if EC[i] <= c < EC[i + 1]) for i in range(5)]
CHK(len(CUR) == 20 and FC == [2, 5, 6, 5, 2], FC)
F34 = [2, 5, 9, 15, 18, 20]  # acumulades d'una taula amb x = 0..5
S_.append(("Taules de freqüències", [
 (1, r"@@NOT@@Aquestes són les notes d'un examen de 30 alumnes: \ $%s$. \ Fes la taula de freqüències amb $f_i$, $F_i$, $h_i$ i percentatges." % lst(NOT)
     + recorda(r"La freqüència absoluta acumulada $F_i$ és el nombre de dades menors o iguals que $x_i$: se sumen les $f_i$ fins a eixa fila. L'última és $N$."),
     center(ftab(XN, FN, ('f', 'F', 'h', 'p')))),
 (1, r"Amb la taula de l'exercici anterior, respon:" + tasks(2, [r"Quants alumnes han tret un 6 o menys?", r"Quants han aprovat (5 o més)?", r"Quants han tret més d'un 7?", r"Quin percentatge ha tret un 9 o més?"]),
     tasks(2, [r"$F=\res{19}$", r"$30-6=\res{24}$", r"$30-24=\res{6}$", r"$\frac{3}{30}=\res{10\,\%}$"])),
 (2, r"En aquesta taula, $x_i$ és el nombre de llibres llegits en un mes i $F_i$, la freqüència acumulada. Troba les freqüències absolutes. Quants alumnes han llegit exactament 3 llibres? I almenys 2?" + center(htab(list(range(6)), F34, fl='$F_i$')),
     r"Restem cada $F_i$ de l'anterior:" + center(htab(list(range(6)), [F34[0]] + [F34[i] - F34[i - 1] for i in range(1, 6)])) + r"Exactament 3: $f=\res{6}$. \ Almenys 2: $20-5=\res{15}$."),
 (2, r"@@PES@@Aquests són els pesos (en kg) de 24 alumnes: \ $%s$. \ Agrupa'ls en intervals d'amplària 5 des de 35\,kg i fes la taula amb les marques de classe, $f_i$, $F_i$ i percentatges." % lst(PES)
     + recorda(r"L'interval $[40,\ 45)$ conté les dades majors o iguals que 40 i menors que 45. La marca de classe és el punt mitjà: $\frac{40+45}{2}=42{,}5$."),
     center(r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|c|c|c|c|}\hline Pes (kg) & Marca & $f_i$ & $F_i$ & \%\\\hline '
            + r'\\\hline '.join('%s & $%s$ & $%d$ & $%d$ & $%s$' % (ivl(EP[i], EP[i + 1]), tn(Fr(EP[i] + EP[i + 1], 2)), f, F, tn(Fr(100 * f, 24)) if Fr(100 * f, 24).denominator in (1, 2) else tr(Fr(100 * f, 24), 1)) for i, (f, F) in enumerate(zip(FP, acc(FP))))
            + r'\\\hline \textbf{Total} & & $24$ & & $100$\\\hline\end{tabular}}')),
 (2, r"En quin interval de l'exercici anterior posaries cadascuna d'aquestes dades?" + tasks(4, [r'$45$\,kg', r'$44{,}9$\,kg', r'$55$\,kg', r'$35$\,kg']),
     tasks(4, [r'\rest{$[45,\ 50)$}', r'\rest{$[40,\ 45)$}', r'\rest{$[55,\ 60)$}', r'\rest{$[35,\ 40)$}'])),
 (3, r"Aquests són els temps (en segons) de 20 alumnes en una cursa de 100\,m: \ $%s$. \ Agrupa'ls en intervals d'1 segon des de 12\,s i fes la taula amb $f_i$ i $F_i$. Quin percentatge ha tardat menys de 14\,s? Quants han tardat 15\,s o més?" % lst(CUR),
     center(r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|c|c|c|}\hline Temps (s) & Marca & $f_i$ & $F_i$\\\hline '
            + r'\\\hline '.join('%s & $%s$ & $%d$ & $%d$' % (ivl(EC[i], EC[i + 1]), tn(Fr(2 * EC[i] + 1, 2)), f, F) for i, (f, F) in enumerate(zip(FC, acc(FC))))
            + r'\\\hline\end{tabular}}') + r"Menys de 14\,s: $F=7$, \ $\frac{7}{20}=\res{35\,\%}$. \ 15\,s o més: $5+2=\res{7}$ alumnes."),
 (3, r"En una taula de freqüències, $F_3=12$, $F_4=19$ i $F_5=25$, i 5 és el valor més gran. Quantes dades hi ha? Quina és la freqüència absoluta del 4? Quin percentatge de les dades és més gran que 3?",
     r"$N=F_5=\res{25}$. \ $f_4=F_4-F_3=19-12=\res{7}$. \ Més grans que 3: $25-12=13$, \ $\frac{13}{25}=\res{52\,\%}$."),
]))
CHK(AN == [1, 3, 6, 12, 19, 24, 27, 29, 30] and AN[4] == 19 and 30 - AN[2] == 24 and 30 - AN[5] == 6 and FN[-1] + FN[-2] == 3)
CHK(sum(1 for c in CUR if c < 14) == 7 and sum(1 for c in CUR if c >= 15) == 7)
CHK(F34[5] - F34[1] == 15 and F34[3] - F34[2] == 6)
EQ(Fr(13, 25) * 100, 52)

# =====================================================================
# 4. Diagrames de barres, polígons i histogrames
# =====================================================================
VIA = [('0', 3), ('1', 8), ('2', 6), ('3', 4), ('4', 2), ('5', 1)]
CHK(sum(f for _, f in VIA) == 24 and sum(int(x) * f for x, f in VIA) == 45)
M4A = [1, 2, 5, 7, 8, 4, 3]; M4B = [0, 1, 3, 6, 9, 7, 4]  # notes 4..10 de dues classes
CHK(sum(M4A) == 30 and sum(M4B) == 30)
CHK(sum(x * f for x, f in zip(range(4, 11), M4A)) < sum(x * f for x, f in zip(range(4, 11), M4B)))
VOTS = [('A', 96), ('B', 92), ('C', 98)]
S_.append(("Diagrames de barres, polígons i histogrames", [
 (1, r"Dibuixa el diagrama de barres dels grups sanguinis de l'exercici @SANG@ (A: 9, O: 11, B: 3, AB: 2)."
     + recorda(r"En un \textbf{diagrama de barres} posem els valors en l'eix horitzontal i, damunt de cadascun, una barra d'altura igual a la seua freqüència. Les barres van separades."),
     center(tbar(['A', 'O', 'B', 'AB'], [9, 11, 3, 2], yl='Persones', xl='Grup', multi=True))),
 (1, r"Aquest diagrama mostra quants viatges han fet en avió els alumnes d'una classe. Fes la taula de freqüències. Quants alumnes hi ha? Quina és la moda? Quants han viatjat en avió alguna vegada?" + center(tbar([x for x, _ in VIA], [f for _, f in VIA], yl='Alumnes', xl='Viatges')),
     center(htab([int(x) for x, _ in VIA], [f for _, f in VIA])) + r"$N=\res{24}$ alumnes. \ $Mo=\res{1}$ viatge. \ Alguna vegada: $24-3=\res{21}$."),
 (1, r"Dibuixa el diagrama de barres i el polígon de freqüències del nombre de mascotes de l'exercici @MAS@.",
     center(tbar([str(x) for x, _ in TM], [f for _, f in TM], kind='both', yl='Alumnes', xl='Mascotes'))),
 (2, r"Dibuixa l'histograma i el polígon de freqüències dels pesos agrupats en intervals de l'exercici @PES@."
     + recorda(r"En un \textbf{histograma} les barres ocupen tot l'interval i van juntes. El polígon uneix els punts de dalt sobre les marques de classe i es tanca en l'eix."),
     center(thist(EP, FP, poly=True, yl='Alumnes', xl='kg'))),
 (2, r"Quin gràfic triaries per a representar cada variable?" + tasks(1, [r"el nombre de germans de 30 alumnes;", r"l'alçada de 200 persones;", r"el mitjà de transport preferit per a anar de vacances;", r"els minuts que tarden 50 alumnes a fer els deures."]),
     tasks(1, [r"\rest{diagrama de barres} (discreta)", r"\rest{histograma} (contínua, en intervals)", r"\rest{diagrama de barres} o \rest{de sectors} (qualitativa)", r"\rest{histograma} (contínua, en intervals)"])),
 (2, r"Les notes d'un examen de dues classes de 30 alumnes estan en la taula. Dibuixa els dos polígons de freqüències en el mateix gràfic. Quina classe ha tret millors notes?" + center(r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|' + 'c|' * 7 + r'}\hline Nota & ' + ' & '.join(str(x) for x in range(4, 11)) + r'\\\hline Classe A & ' + ' & '.join(map(str, M4A)) + r'\\\hline Classe B & ' + ' & '.join(map(str, M4B)) + r'\\\hline\end{tabular}}'),
     center(tbar([str(x) for x in range(4, 11)], M4A, kind='poly', yl='Alumnes', xl='Nota', series=[(M4B, 'accent')])) + r"El polígon de B (taronja) està desplaçat cap a la dreta: la classe \rest{B} ha tret millors notes."),
 (3, r"Tres candidats d'unes eleccions han tret 96, 92 i 98 vots. Un cartell els representa amb un diagrama de barres en què l'eix vertical comença en 90. Per què és enganyós? Dibuixa'l bé.",
     r"Si l'eix comença en 90, la barra de C (8 unitats d'altura) sembla \rest{quatre vegades} la de B (2 unitats), però en realitat C només té 6 vots més ($98-92$). Cal començar l'eix en \rest{0}:" + center(tbar(['A', 'B', 'C'], [96, 92, 98], yl='Vots', step=20, multi=True, H=2.4))),
]))

# =====================================================================
# 5. Diagrames de sectors i pictogrames
# =====================================================================
E51 = [('Futbol', 15), ('Bàsquet', 9), ('Tenis', 6), ('Natació', 4), ('Altres', 2)]
A51 = [Fr(360 * f, 36) for _, f in E51]; CHK(A51 == [150, 90, 60, 40, 20] and sum(A51) == 360)
A52 = [Fr(360 * f, 25) for _, f in TS]; CHK(sum(A52) == 360 and A52 == [Fr(648, 5), Fr(792, 5), Fr(216, 5), Fr(144, 5)])
P53 = [('Mòbil', 40), ('Consola', 25), ('Ordinador', 20), ('Tauleta', 15)]; F53 = [Fr(p * 200, 100) for _, p in P53]; CHK(F53 == [80, 50, 40, 30])
A54 = [('Platja', 100), ('Muntanya', 120), ('Ciutat', 80), ('Poble', 60)]; F54 = [Fr(a * 72, 360) for _, a in A54]; CHK(sum(a for _, a in A54) == 360 and F54 == [20, 24, 16, 12])
B55 = [('Gener', 3), ('Febrer', Fr(5, 2)), ('Març', 4), ('Abril', Fr(11, 2))]; F55 = [4 * v for _, v in B55]; CHK(F55 == [12, 10, 16, 22] and sum(F55) == 60)
D56 = [('1r A', 20), ('1r B', 35), ('1r C', 15), ('1r D', 30)]
S_.append(("Diagrames de sectors i pictogrames", [
 (1, r"S'ha preguntat a 36 alumnes pel seu esport preferit: futbol 15, bàsquet 9, tenis 6, natació 4 i altres 2. Calcula l'angle de cada sector i dibuixa el diagrama de sectors."
     + recorda(r"Angle del sector $=\dfrac{f_i}{N}\cdot360^\circ$. Si $N$ és divisor de 360, cada dada val $360^\circ:N$."),
     r"Cada alumne val $360^\circ:36=10^\circ$: \ " + ', '.join(r'%s $\res{%s^\circ}$' % (c, tn(a)) for (c, _), a in zip(E51, A51)) + '.' + center(tpie([c for c, _ in E51], [f for _, f in E51]))),
 (1, r"Calcula els angles del diagrama de sectors dels grups sanguinis de l'exercici @SANG@ (A: 9, O: 11, B: 3, AB: 2) i dibuixa'l.",
     r"Cada persona val $360^\circ:25=14{,}4^\circ$: \ " + ', '.join(r'%s: $%d\cdot14{,}4=\res{%s^\circ}$' % (c, f, tn(a)) for (c, f), a in zip(TS, A52)) + '.' + center(tpie([c for c, _ in TS], [f for _, f in TS]))),
 (2, r"S'ha preguntat a 200 joves quin aparell fan servir més per a jugar. Quantes persones han triat cada aparell?" + center(tpie([c for c, _ in P53], [p for _, p in P53], lab='pct')),
     ', '.join(r'%s: $%s\cdot200=\res{%d}$' % (c, tn(Fr(p, 100)), f) for (c, p), f in zip(P53, F53)) + r'. \ Comprovem: $80+50+40+30=200$.'),
 (2, r"En un diagrama de sectors sobre el lloc de vacances preferit de 72 persones, els angles són: platja $100^\circ$, muntanya $120^\circ$, ciutat $80^\circ$ i poble $60^\circ$. Quantes persones han triat cada lloc?"
     + recorda(r"Del sector a la freqüència: $f_i=\dfrac{\text{angle}}{360^\circ}\cdot N$."),
     ', '.join(r'%s: $\frac{%d}{360}\cdot72=\res{%d}$' % (c, a, f) for (c, a), f in zip(A54, F54)) + '.'),
 (2, r"Aquest pictograma mostra les bicis que ha venut una botiga cada mes. Cada icona representa 4 bicis. Quantes n'ha venut cada mes? I en total?" + center(tpicto([c for c, _ in B55], [v * 4 for _, v in B55], 4)),
     ', '.join(r'%s: $\res{%d}$' % (c, f) for (c, _), f in zip(B55, F55)) + r'. \ Total: $\res{60}$ bicis.'),
 (2, r"Els alumnes de quatre grups de 1r d'ESO han recollit taps per a una campanya solidària: 1r A, 20 bosses; 1r B, 35; 1r C, 15, i 1r D, 30. Fes un pictograma en què cada icona valga 5 bosses.",
     r"Cal dibuixar $20:5=\res{4}$, \ $35:5=\res{7}$, \ $15:5=\res{3}$ \ i \ $30:5=\res{6}$ icones." + center(tpicto([c for c, _ in D56], [v for _, v in D56], 5, r'\faShoppingBag', 'teal'))),
 (3, r"En un diagrama de sectors, el sector de les persones que prefereixen l'estiu fa $72^\circ$ i correspon a 18 persones. Quantes persones s'han enquestat? Si el $30\,\%$ prefereix la primavera, quantes persones són i quin angle té el seu sector?",
     r"Cada persona val $72^\circ:18=4^\circ$, \ $N=360:4=\res{90}$ persones. \ Primavera: $0{,}3\cdot90=\res{27}$ persones, \ $27\cdot4=\res{108^\circ}$."),
]))
EQ(Fr(72, 18), 4); EQ(360 / Fr(72, 18), 90); EQ(fr('0.3') * 90, 27); EQ(27 * 4, 108); EQ(Fr(108, 360), '0.3')

# =====================================================================
# 6. Moda, mitjana i mediana
# =====================================================================
D61 = [5, 8, 3, 8, 6, 9, 7]; CHK(sum(D61) == 46 and median(D61) == 7 and modes(D61) == [8])
D62 = [12, 15, 9, 18, 15, 11]; CHK(sum(D62) == 80 and median(D62) == Fr(27, 2) and modes(D62) == [15])
D64 = [[4, 9, 6, 9, 2], [1, 3, 3, 7, 8, 8], [10, 20, 30, 40]]
R64 = [(6, 6, [9]), (5, 5, [3, 8]), (25, 25, None)]
for d, (m, me, mo) in zip(D64, R64):
    CHK(mean(d) == m and median(d) == me and (mo is None and len(modes(d)) == len(d) or modes(d) == mo), d)
G65 = [2, 1, 0, 3, 2, 2, 1, 4]; CHK(sum(G65) == 15 and mean(G65) == Fr(15, 8) and median(G65) == 2 and modes(G65) == [2])
CA = [150, 160, 155, 170, 165, 900]; CHK(sum(CA) == 1700 and median(CA) == Fr(325, 2))
D67 = [4, 4, 5, 8, 9]; CHK(mean(D67) == 6 and median(D67) == 5 and modes(D67) == [4])
D68 = [4, 6, 7, 9]; CHK(mean(D68) == Fr(13, 2) and mean(D68 + [9]) == 7)
S_.append(("Moda, mitjana i mediana", [
 (1, r"Calcula la moda, la mitjana i la mediana de: \ $%s$." % lst(D61)
     + recorda(r"\textbf{Moda}: el valor més repetit. \textbf{Mitjana}: $\bar x=\dfrac{\text{suma de les dades}}{N}$. \textbf{Mediana}: el valor central de les dades \textbf{ordenades}; si n'hi ha dos, la seua mitjana."),
     r"$Mo=\res{8}$. \ $\bar x=\frac{46}{7}\res{\approx6{,}57}$. \ Ordenades: $3,\ 5,\ 6,\ \underline{7},\ 8,\ 8,\ 9$: \ $Me=\res{7}$."),
 (1, r"Calcula la moda, la mitjana i la mediana de: \ $%s$." % lst(D62),
     r"$Mo=\res{15}$. \ $\bar x=\frac{80}{6}\res{\approx13{,}33}$. \ Ordenades: $9,\ 11,\ \underline{12,\ 15},\ 15,\ 18$: \ $Me=\frac{12+15}{2}=\res{13{,}5}$."),
 (1, r"S'ha preguntat a 30 alumnes per la seua estació preferida: primavera 9, estiu 13, tardor 3 i hivern 5. Quina és la moda? Es poden calcular la mitjana i la mediana?",
     r"$Mo=$ \rest{estiu}. La variable és qualitativa: \rest{no} es pot calcular ni la mitjana ni la mediana."),
 (2, r"Calcula la moda, la mitjana i la mediana de cada conjunt de dades:" + tasks(1, ['$' + lst(d) + '$' for d in D64]),
     tasks(1, [r"$Mo=\res{9}$; \ $\bar x=\frac{30}{5}=\res{6}$; \ $2,\ 4,\ \underline{6},\ 9,\ 9$: $Me=\res{6}$",
               r"Dues modes: $\res{3}$ i $\res{8}$; \ $\bar x=\frac{30}{6}=\res{5}$; \ $Me=\frac{3+7}{2}=\res{5}$",
               r"\rest{No hi ha moda} (totes apareixen una vegada); \ $\bar x=\frac{100}{4}=\res{25}$; \ $Me=\frac{20+30}{2}=\res{25}$"])),
 (2, r"Els gols que ha marcat un equip en els últims 8 partits són: \ $%s$. \ Calcula la moda, la mitjana i la mediana." % lst(G65),
     r"$Mo=\res{2}$. \ $\bar x=\frac{15}{8}=\res{1{,}875}$ gols. \ Ordenades: $0,\ 1,\ 1,\ \underline{2,\ 2},\ 2,\ 3,\ 4$: \ $Me=\res{2}$."),
 (2, r"Els preus (en milers d'euros) de les cases venudes en un carrer han sigut: 150, 160, 155, 170, 165 i 900. Calcula la mitjana i la mediana. Quin dels dos paràmetres representa millor el preu d'una casa del carrer? Per què?",
     r"$\bar x=\frac{1\,700}{6}\res{\approx283{,}33}$ mil €. \ Ordenades: $150,\ 155,\ \underline{160,\ 165},\ 170,\ 900$: \ $Me=\res{162{,}5}$ mil €. \ La \rest{mediana}: la casa de 900 mil € és una dada extrema que estira la mitjana cap amunt."),
 (3, r"Escriu cinc nombres que tinguen la mitjana 6, la mediana 5 i la moda 4.",
     r"Per exemple, $\res{4,\ 4,\ 5,\ 8,\ 9}$: suma 30, \ $\bar x=6$; el central és el 5; el 4 és el més repetit. (Hi ha altres solucions.)"),
 (3, r"Les notes de Jan són 4, 6, 7 i 9. Quina és la mitjana? Quina nota ha de traure en el següent examen perquè la mitjana siga 7?",
     r"$\bar x=\frac{26}{4}=\res{6{,}5}$. \ Amb 5 exàmens, la suma ha de ser $7\cdot5=35$: \ $35-26=\res{9}$."),
]))
for d in D64: CHK(sum(d) in (30, 100))

# =====================================================================
# 7. Paràmetres a partir d'una taula de freqüències
# =====================================================================
T71 = [(0, 4), (1, 10), (2, 6), (3, 3), (4, 2)]; d71 = expand(T71)
CHK(len(d71) == 25 and sum(d71) == 39 and median(d71) == 1 and modes(d71) == [1])
dN = NOT; CHK(sum(dN) == 179 and median(dN) == 6 and modes(dN) == [6])
T73 = [(35, 2), (36, 5), (37, 7), (38, 8), (39, 4), (40, 2)]; d73 = expand(T73)
CHK(len(d73) == 28 and sum(d73) == 1049 and median(d73) == Fr(75, 2) and modes(d73) == [38])
T74 = [(0, 5), (1, 8), (2, 9), (3, 6), (4, 2)]; d74 = expand(T74)
CHK(len(d74) == 30 and sum(d74) == 52 and median(d74) == 2 and modes(d74) == [2])
MK = [Fr(EP[i] + EP[i + 1], 2) for i in range(5)]; SP = sum(m * f for m, f in zip(MK, FP)); CHK(SP == 1140)
T76 = [(0, 4), (2, 6), (3, 4)]  # x=1 té freqüència a desconeguda
CHK(mean(expand([(0, 4), (1, 6), (2, 6), (3, 4)])) == Fr(3, 2))
B77 = [(1, 2), (2, 5), (3, 8), (4, 3), (5, 2)]; d77 = expand(B77)
CHK(len(d77) == 20 and sum(d77) == 58 and median(d77) == 3 and modes(d77) == [3])
S_.append(("Paràmetres a partir d'una taula de freqüències", [
 (1, r"El nombre de germans de 25 alumnes és el de la taula. Calcula la mitjana, la mediana i la moda." + center(htab([x for x, _ in T71], [f for _, f in T71]))
     + recorda(r"$\bar x=\dfrac{\sum x_i\cdot f_i}{N}$. Per a la mediana, busca la posició central i mira en quina fila l'$F_i$ hi arriba."),
     center(ftab([x for x, _ in T71], [f for _, f in T71], ('f', 'F', 'xf'))) + r"$\bar x=\frac{39}{25}=\res{1{,}56}$. \ La dada central és la 13a: $F=14$ en l'1, \ $Me=\res{1}$. \ $Mo=\res{1}$."),
 (1, r"Calcula la mitjana, la mediana i la moda de les notes de l'exercici @NOT@ a partir de la seua taula de freqüències.",
     center(ftab(XN, FN, ('f', 'F', 'xf'))) + r"$\bar x=\frac{179}{30}\res{\approx5{,}97}$. \ Les centrals són la 15a i la 16a: totes dues valen 6 ($F$ passa de 12 a 19), \ $Me=\res{6}$. \ $Mo=\res{6}$ ($f=7$)."),
 (2, r"Aquesta taula recull el número de calçat de 28 alumnes. Calcula la mitjana, la mediana i la moda." + center(htab([x for x, _ in T73], [f for _, f in T73], xl='Número')),
     center(ftab([x for x, _ in T73], [f for _, f in T73], ('f', 'F', 'xf'))) + r"$\bar x=\frac{1\,049}{28}\res{\approx37{,}46}$. \ Les centrals són la 14a ($37$, perquè $F=14$) i la 15a ($38$): \ $Me=\frac{37+38}{2}=\res{37{,}5}$. \ $Mo=\res{38}$."),
 (2, r"Els gols marcats per un equip en 30 partits han sigut: 0 gols en 5 partits, 1 gol en 8, 2 en 9, 3 en 6 i 4 en 2. Calcula la mitjana de gols per partit, la mediana i la moda.",
     center(ftab([x for x, _ in T74], [f for _, f in T74], ('f', 'F', 'xf'))) + r"$\bar x=\frac{52}{30}\res{\approx1{,}73}$. \ Les centrals (15a i 16a) valen 2: $Me=\res{2}$. \ $Mo=\res{2}$."),
 (2, r"Calcula la mitjana aproximada dels pesos agrupats de l'exercici @PES@ fent servir les marques de classe.",
     center(ftab([tn(m) for m in MK], FP, ('f', 'xf'), xl='Marca').replace(r'\textbf{Total} & $24$ & ', r'\textbf{Total} & $24$ & $1\,140$')) + r"$\bar x\approx\frac{1\,140}{24}=\res{47{,}5}$\,kg."),
 (3, r"En aquesta taula falta una freqüència. Troba-la sabent que la mitjana és $1{,}5$." + center(htab([0, 1, 2, 3], [4, '$a$', 6, 4])),
     r"Sense l'1: $0\cdot4+2\cdot6+3\cdot4=24$ i hi ha 14 dades. \ $\frac{24+a}{14+a}=1{,}5\Rightarrow24+a=21+1{,}5a\Rightarrow3=0{,}5a\Rightarrow\res{a=6}$. \ Comprovem: $\frac{30}{20}=1{,}5$."),
 (3, r"Aquest diagrama de barres mostra la nota (de 1 a 5) que 20 clients han posat a un restaurant. Calcula la mitjana, la mediana i la moda." + center(tbar([str(x) for x, _ in B77], [f for _, f in B77], yl='Clients', xl='Nota')),
     center(ftab([x for x, _ in B77], [f for _, f in B77], ('f', 'F', 'xf'))) + r"$\bar x=\frac{58}{20}=\res{2{,}9}$. \ Les centrals (10a i 11a) valen 3: $Me=\res{3}$. \ $Mo=\res{3}$."),
]))
CHK(acc([f for _, f in T73])[1] == 7 and acc([f for _, f in T73])[2] == 14)

# =====================================================================
# 8. Rang i desviació mitjana
# =====================================================================
R81 = [[3, 12, 7, 15, 9], [-4, 6, 2, -1, 8], [fr('2.5'), fr('4.8'), fr('1.3'), fr('3.6')]]
for d, r in zip(R81, [12, 12, '3.5']): EQ(rang(d), r)
D82 = [3, 5, 7, 9, 11]; CHK(mean(D82) == 7 and dm(D82) == Fr(12, 5))
D83 = [2, 4, 4, 6, 8, 12]; CHK(mean(D83) == 6 and dm(D83) == Fr(16, 6) and rang(D83) == 10)
NA = [5, 6, 5, 6, 5, 6]; NB = [2, 9, 3, 8, 4, 7]
CHK(mean(NA) == mean(NB) == Fr(11, 2) and dm(NA) == Fr(1, 2) and dm(NB) == Fr(5, 2) and rang(NA) == 1 and rang(NB) == 7)
CX = [12, 14, 15, 13, 16]; CY = [6, 20, 10, 18, 16]
CHK(mean(CX) == 14 and mean(CY) == 14 and dm(CX) == Fr(6, 5) and dm(CY) == Fr(24, 5) and rang(CX) == 4 and rang(CY) == 14)
T86 = [(1, 2), (2, 3), (3, 5), (4, 3), (5, 2)]; d86 = expand(T86); CHK(mean(d86) == 3 and dm(d86) == Fr(14, 15))
S_.append(("Rang i desviació mitjana", [
 (1, r"Calcula el rang de cada conjunt de dades:" + tasks(3, ['$' + lst(d) + '$' for d in R81])
     + recorda(r"Rang $=x_{\max}-x_{\min}$. \ Desviació mitjana: $DM=\dfrac{\sum|x_i-\bar x|}{N}$ (la mitjana de les distàncies a la mitjana)."),
     tasks(3, [r"$15-3=\res{12}$", r"$8-(-4)=\res{12}$", r"$4{,}8-1{,}3=\res{3{,}5}$"])),
 (1, r"Calcula la desviació mitjana de: \ $%s$." % lst(D82),
     r"$\bar x=\frac{35}{5}=7$. \ Distàncies: $4,\ 2,\ 0,\ 2,\ 4$. \ $DM=\frac{12}{5}=\res{2{,}4}$."),
 (2, r"Calcula la mitjana, el rang i la desviació mitjana de: \ $%s$." % lst(D83),
     r"$\bar x=\frac{36}{6}=\res{6}$. \ Rang $=12-2=\res{10}$. \ Distàncies: $4,\ 2,\ 2,\ 0,\ 2,\ 6$; \ $DM=\frac{16}{6}\res{\approx2{,}67}$."),
 (2, r"Les notes de dos alumnes en sis exàmens han sigut: Aina, $%s$; Biel, $%s$. Calcula la mitjana, el rang i la desviació mitjana de cadascun. Qui és més regular?" % (lst(NA), lst(NB)),
     r"Tots dos tenen $\bar x=\frac{33}{6}=5{,}5$. \ Aina: rang $\res{1}$, \ $DM=\frac{6\cdot0{,}5}{6}=\res{0{,}5}$. \ Biel: rang $9-2=\res{7}$, distàncies $3{,}5;\ 3{,}5;\ 2{,}5;\ 2{,}5;\ 1{,}5;\ 1{,}5$, \ $DM=\frac{15}{6}=\res{2{,}5}$. \ \rest{Aina} és més regular."),
 (2, r"Les temperatures màximes d'una setmana de cinc dies a dues ciutats han sigut: ciutat X, $%s$\,°C; ciutat Y, $%s$\,°C. Compara-les amb la mitjana, el rang i la desviació mitjana." % (lst(CX), lst(CY)),
     r"Totes dues tenen $\bar x=\res{14}$\,°C. \ X: rang $\res{4}$, \ $DM=\frac{6}{5}=\res{1{,}2}$. \ Y: rang $\res{14}$, \ $DM=\frac{8+6+4+4+2}{5}=\frac{24}{5}=\res{4{,}8}$. \ A la ciutat \rest{Y} les temperatures varien molt més."),
 (3, r"Calcula la mitjana i la desviació mitjana de les dades d'aquesta taula." + center(htab([x for x, _ in T86], [f for _, f in T86])),
     r"$\bar x=\frac{2+6+15+12+10}{15}=\frac{45}{15}=\res{3}$. \ $DM=\frac{2\cdot2+1\cdot3+0\cdot5+1\cdot3+2\cdot2}{15}=\frac{14}{15}\res{\approx0{,}93}$."),
 (3, r"Raona si és vertader o fals:" + tasks(1, [r"Si el rang és 0, totes les dades són iguals.", r"Si sumem 5 a totes les dades, la desviació mitjana augmenta 5.", r"Dos conjunts amb la mateixa mitjana tenen la mateixa desviació mitjana.", r"La desviació mitjana mai no pot ser negativa."]),
     tasks(1, [r"\rest{Vertader}: la més gran i la més xicoteta coincideixen.", r"\rest{Fals}: totes les dades es desplacen igual i les distàncies a la mitjana no canvien.", r"\rest{Fals}: per exemple, $5,\ 5$ i $0,\ 10$ tenen mitjana 5 però $DM=0$ i $DM=5$.", r"\rest{Vertader}: és una mitjana de distàncies, que són positives o zero."])),
]))
CHK(dm([5, 5]) == 0 and dm([0, 10]) == 5 and dm([x + 5 for x in D82]) == dm(D82))

# =====================================================================
# 9. Problemes d'estadística
# =====================================================================
FAM = [0, 1, 2, 2, 1, 3, 2, 1, 1, 2, 0, 2, 3, 1, 2, 4, 2, 1, 2, 1]
TF = freqs(FAM); CHK(TF == [(0, 2), (1, 7), (2, 8), (3, 2), (4, 1)] and sum(FAM) == 33 and median(FAM) == 2 and modes(FAM) == [2] and rang(FAM) == 4)
CHK(Fr(8, 20) * 360 == 144)
S_.append(("Problemes d'estadística", [
 (1, r"Marina ha tret $6{,}5$; $7$ i $5{,}5$ en els tres primers exàmens. Quina nota necessita en el quart per a tindre una mitjana de $6{,}5$?"
     + recorda(r"Si coneixem la mitjana i el nombre de dades, coneixem la suma: \ $\text{suma}=\bar x\cdot N$."),
     r"Suma necessària: $6{,}5\cdot4=26$. \ Ja té $6{,}5+7+5{,}5=19$. \ Necessita un $26-19=\res{7}$."),
 (1, r"La mitjana de quatre nombres és 12. Tres d'ells són 10, 15 i 9. Quin és el quart?",
     r"Suma: $12\cdot4=48$. \ $48-(10+15+9)=\res{14}$."),
 (2, r"En una classe de 25 alumnes la nota mitjana d'un examen ha sigut $6{,}4$ i en una altra de 15 alumnes, $7{,}2$. Quina és la nota mitjana dels 40 alumnes? Per què no és $6{,}8$?",
     r"$6{,}4\cdot25=160$; \ $7{,}2\cdot15=108$; \ $\bar x=\frac{160+108}{40}=\frac{268}{40}=\res{6{,}7}$. \ No és la mitjana de les mitjanes perquè les classes \rest{no tenen el mateix nombre d'alumnes}."),
 (2, r"S'ha preguntat a 20 famílies quants fills tenen: \ $%s$." % lst(FAM) + tasks(1, [r"Fes la taula de freqüències (amb $f_i$, $F_i$ i $h_i$).", r"Dibuixa'n el diagrama de barres.", r"Calcula la moda, la mitjana, la mediana i el rang.", r"Quin percentatge de famílies té més d'un fill? Quin angle tindria el sector «2 fills» en un diagrama de sectors?"]),
     center(ftab([x for x, _ in TF], [f for _, f in TF], ('f', 'F', 'h'))) + center(tbar([str(x) for x, _ in TF], [f for _, f in TF], yl='Famílies', xl='Fills'))
     + r"$Mo=\res{2}$; \ $\bar x=\frac{33}{20}=\res{1{,}65}$; \ les centrals (10a i 11a) valen 2: $Me=\res{2}$; \ rang $=4-0=\res{4}$. \ Més d'un fill: $8+2+1=11$, \ $\frac{11}{20}=\res{55\,\%}$. \ Sector: $\frac{8}{20}\cdot360^\circ=\res{144^\circ}$."),
 (2, r"L'edat mitjana dels 11 jugadors d'un equip és de 22 anys. Si hi afegim l'entrenador, l'edat mitjana dels 12 és de 24 anys. Quants anys té l'entrenador?",
     r"$22\cdot11=242$; \ $24\cdot12=288$; \ $288-242=\res{46}$ anys."),
 (3, r"Un professor ha calculat que la mitjana de les notes dels 10 alumnes d'un grup és $6{,}3$, però després s'adona que ha copiat un 9 en lloc d'un 4. Quina és la mitjana correcta? Canvia la mediana si les notes eren 3, 4, 5, 5, 6, 7, 7, 8, 9, 9 (amb el 9 equivocat)?",
     r"Suma errònia: $63$; correcta: $63-9+4=58$; \ $\bar x=\res{5{,}8}$. \ Mediana errònia: $\frac{6+7}{2}=6{,}5$. Correcta (3, 4, 4, 5, 5, 6, 7, 7, 8, 9): $\frac{5+6}{2}=\res{5{,}5}$. Sí que canvia."),
 (3, r"De dues classes es coneixen aquests resultats d'un examen: classe A, $\bar x=6$, $Me=6$, $DM=0{,}8$; classe B, $\bar x=6$, $Me=7$, $DM=2{,}5$. Raona si és vertader o fals:" + tasks(1, [r"Les dues classes han tret, de mitjana, la mateixa nota.", r"En la classe B, almenys la meitat dels alumnes ha tret un 7 o més.", r"Les notes de la classe A són més semblants entre si.", r"En la classe A hi ha alumnes amb un 10."]),
     tasks(1, [r"\rest{Vertader}: $\bar x=6$ en totes dues.", r"\rest{Vertader}: la mediana és 7.", r"\rest{Vertader}: té menys desviació mitjana.", r"\rest{No es pot saber} amb aquestes dades."])),
]))
EQ(fr('6.5') * 4 - (fr('6.5') + 7 + fr('5.5')), 7); EQ(48 - 34, 14); EQ(Fr(268, 40), '6.7'); EQ(24 * 12 - 22 * 11, 46)
W9 = [3, 4, 5, 5, 6, 7, 7, 8, 9, 9]; W9c = [3, 4, 4, 5, 5, 6, 7, 7, 8, 9]
CHK(sum(W9) == 63 and sum(W9c) == 58 and median(W9) == Fr(13, 2) and median(W9c) == Fr(11, 2))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\definecolor{violet}{HTML}{7C6CF0}\n\\definecolor{gold}{HTML}{E0A21B}\n'
KW = 'pdfkeywords={estadística, població, mostra, variables estadístiques, freqüències, taules de freqüències, diagrama de barres, polígon de freqüències, histograma, diagrama de sectors, pictograma, moda, mitjana, mediana, rang, desviació mitjana}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
TIT = "Estadística"

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 10: %s. 1r d'ESO}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 10 · 1r d'ESO" % t)
    assert 'Unitat 10' in p and 'unitat 10' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{1r ESO}{''' + ('Solucions de la fitxa · Unitat 10' if sol else "Fitxa d'exercicis · Unitat 10") + r'''}{''' + TIT + r'''}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs un laboratori de dades que fa taules de freqüències, eines per a construir gràfics i per a calcular la moda, la mitjana, la mediana i la desviació mitjana."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Per a fer gràfics, fes servir paper quadriculat, regle i transportador, i posa sempre el títol i el nom de cada eix.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't10-fitxa-solucions.tex' if sol else 't10-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

# referències creuades: @@NOM@@ marca l'exercici i @NOM@ s'hi refereix
LAB, k = {}, 0
for title, exs in S_:
    for st, q, sl in exs:
        k += 1
        for m in re.findall(r'@@(\w+)@@', q): LAB[m] = k
def refs(t):
    t = re.sub(r'@@\w+@@', '', t)
    return re.sub(r'@(\w+)@', lambda m: str(LAB[m.group(1)]), t)
S_ = [(title, [(st, refs(q), refs(sl)) for st, q, sl in exs]) for title, exs in S_]
CHK(all('@' not in q + sl for _, exs in S_ for _, q, sl in exs))
n = build(False); build(True)
print(n, 'exercicis,', NCHK[0], 'comprovacions')
print(LAB)
