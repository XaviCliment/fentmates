# Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 9: Estadística)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 8 seccions segueixen els apartats dels apunts (9.1-9.8): població, mostra i variables; taules amb dades aïllades;
# dades agrupades; gràfics; centralització; dispersió; quartils i percentils; diagrama de caixes. Les taules i els gràfics
# (barres, histogrames, sectors i caixes en TikZ) parteixen de ../1eso-t10/genera.py.
# Criteri dels quartils i percentils (el dels apunts): posició k·N/100; si no és entera, la dada de la posició següent; si
# és entera, la mitjana d'eixa dada i la següent.
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es). Cada resultat es comprova amb EQ (exacte, amb fraccions) o AP (arrodonit).
# Ús: python3 genera.py && pdflatex t9-fitxa-exercicis.tex (dues vegades) && pdflatex t9-fitxa-solucions.tex (dues vegades)
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
def side(*figs): return r'\par\smallskip\begin{center}' + r'\hspace{0.8cm}'.join(figs) + r'\end{center}'

# ---------- comprovacions i estadística exacta ----------
NCHK = [0]
def CHK(cond, *info):
    NCHK[0] += 1
    assert cond, info
def fr(v): return v if isinstance(v, Fr) else Fr(str(v).replace('{,}', '.').replace(',', '.'))
def EQ(a, b): CHK(fr(a) == fr(b), a, b)
def AP(a, b, d=2): CHK(abs(float(a) - float(fr(b))) <= 0.5 * 10 ** -d + 1e-9, float(a), b)
def freqs(data):
    return [(k, data.count(k)) for k in sorted(set(data))]
def expand(tab): return [x for x, f in tab for _ in range(f)]
def mean(d): return Fr(sum(fr(x) for x in d), len(d))
def median(d): return pctl(d, 50)
def modes(d):
    c = {x: d.count(x) for x in d}; m = max(c.values()); return sorted(k for k in c if c[k] == m)
def rang(d): return fr(max(d)) - fr(min(d))
def dm(d):
    m = mean(d); return Fr(sum(abs(fr(x) - m) for x in d), len(d))
def var(d):
    m = mean(d); return Fr(sum((fr(x) - m) ** 2 for x in d), len(d))
def pctl(d, k):
    s = sorted(fr(x) for x in d); n = len(s); pos = Fr(k * n, 100)
    if pos.denominator == 1:
        p = int(pos); return (s[p - 1] + s[p]) / 2 if p < n else s[-1]
    return s[math.ceil(pos) - 1]
def five(d): s = sorted(d); return (fr(s[0]), pctl(d, 25), pctl(d, 50), pctl(d, 75), fr(s[-1]))
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
    v = fr(v) if not isinstance(v, float) else v; t = ('%.*f' % (d, float(v))).rstrip('0').rstrip('.')
    return ('=' if not isinstance(v, float) and fr(t) == v else r'\approx ') + t.replace('.', '{,}')
def lst(d): return r',\ \allowbreak '.join(tn(x) for x in d)

# ---------- taules ----------
def ftab(xs, fs, cols=('f',), xl='$x_i$', N=None):
    """taula de freqüències vertical; cols: f, F (acumulada), h (relativa), p (%), xf (x·f), x2f (x²·f)"""
    N = N or sum(fs); F = acc(fs)
    H = {'f': '$f_i$', 'F': '$F_i$', 'h': '$h_i$', 'p': r'\%', 'xf': r'$x_i\cdot f_i$', 'x2f': r'$x_i^2\cdot f_i$'}
    head = xl + ' & ' + ' & '.join(H[c] for c in cols)
    def hcell(f):
        h = Fr(f, N)
        return tn(h) if h.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100) else r'%s' % tr(h)[1:] if tr(h)[0] == '=' else tr(h)
    def pcell(f):
        p = Fr(100 * f, N)
        return tn(p) if p.denominator in (1, 2, 4, 5, 10) else tr(p, 1)
    rows = []
    for i, (x, f) in enumerate(zip(xs, fs)):
        r = [x if isinstance(x, str) else '$%s$' % tn(x)]
        for c in cols:
            r.append({'f': '$%d$' % f, 'F': '$%d$' % F[i], 'h': '$%s$' % hcell(f), 'p': '$%s$' % pcell(f),
                      'xf': '$%s$' % tn(fr(x) * f) if not isinstance(x, str) else '', 'x2f': '$%s$' % tn(fr(x) ** 2 * f) if not isinstance(x, str) else ''}[c])
        rows.append(' & '.join(r))
    num = not isinstance(xs[0], str)
    tot = [r'\textbf{Total}'] + [{'f': '$%d$' % N, 'F': '', 'h': '$1$', 'p': '$100$', 'xf': '$%s$' % tn(sum(fr(x) * f for x, f in zip(xs, fs))) if num else '',
                                  'x2f': '$%s$' % tn(sum(fr(x) ** 2 * f for x, f in zip(xs, fs))) if num else ''}[c] for c in cols]
    return (r'{\renewcommand{\arraystretch}{1.2}\begin{tabular}{|c|%s|}\hline ' % '|'.join('c' * len(cols)) + head + r'\\\hline '
            + r'\\\hline '.join(rows) + r'\\\hline ' + ' & '.join(tot) + r'\\\hline\end{tabular}}')
def htab(xs, fs, xl='$x_i$', fl='$f_i$', w='0.9cm'):
    cell = lambda v: v if isinstance(v, str) else '$%s$' % tn(v)
    return (r'{\renewcommand{\arraystretch}{1.3}\begin{tabular}{|c|%s|}\hline %s & %s\\\hline %s & %s\\\hline\end{tabular}}'
            % ('|'.join(['C{%s}' % w] * len(xs)), xl, ' & '.join(cell(x) for x in xs), fl, ' & '.join(cell(f) for f in fs)))
def ivl(a, b): return '$[%s,\\ %s)$' % (tn(a), tn(b))
def gtab(edges, fs, cols=('m', 'f', 'F'), xl=None):
    """taula d'intervals: m (marca), f, F, p (%), mf (marca·f), m2f"""
    N = sum(fs); F = acc(fs); H = {'m': T('Marca', 'Marca') + ' $x_i$', 'f': '$f_i$', 'F': '$F_i$', 'p': r'\%', 'mf': r'$x_i\cdot f_i$', 'm2f': r'$x_i^2\cdot f_i$'}
    rows = []
    for i, f in enumerate(fs):
        m = Fr(edges[i] + edges[i + 1], 2)
        r = [ivl(edges[i], edges[i + 1])] + [{'m': '$%s$' % tn(m), 'f': '$%d$' % f, 'F': '$%d$' % F[i], 'p': '$%s$' % (tn(Fr(100 * f, N)) if Fr(100 * f, N).denominator in (1, 2, 4, 5, 10) else tr(Fr(100 * f, N), 1)),
                                             'mf': '$%s$' % tn(m * f), 'm2f': '$%s$' % tn(m * m * f)}[c] for c in cols]
        rows.append(' & '.join(r))
    S = sum(Fr(edges[i] + edges[i + 1], 2) * f for i, f in enumerate(fs)); S2 = sum(Fr(edges[i] + edges[i + 1], 2) ** 2 * f for i, f in enumerate(fs))
    tot = [r'\textbf{Total}'] + [{'m': '', 'f': '$%d$' % N, 'F': '', 'p': '$100$', 'mf': '$%s$' % tn(S), 'm2f': '$%s$' % tn(S2)}[c] for c in cols]
    return (r'{\renewcommand{\arraystretch}{1.2}\begin{tabular}{|c|%s|}\hline ' % '|'.join('c' * len(cols)) + (xl or T('Interval', 'Intervalo')) + ' & ' + ' & '.join(H[c] for c in cols) + r'\\\hline '
            + r'\\\hline '.join(rows) + r'\\\hline ' + ' & '.join(tot) + r'\\\hline\end{tabular}}')

# ---------- gràfics (TikZ) ----------
COLS = ['teal', 'accent', 'violet', 'gold', 'navy', 'muted']
def nice(top):
    for st in (1, 2, 5, 10, 20, 25, 50, 100):
        if top / st <= 8: return st
    return 200
def taxes(H, top, st, y0=0, yl='', xl='', W=None):
    o = []; k = y0
    while k <= top + 1e-9:
        y = H * (k - y0) / (top - y0)
        o.append(r'\draw[muted!30,line width=0.3pt] (0,%.3f)--(%.3f,%.3f); \node[left,font=\tiny,text=muted,inner sep=1.5pt] at (0,%.3f) {$%s$};' % (y, W, y, y, tn(k)))
        k += st
    o.append(r'\draw[-latex,muted,line width=0.6pt] (0,0)--(%.3f,0) node[right,font=\scriptsize,text=navy]{%s};' % (W + 0.3, xl))
    o.append(r'\draw[-latex,muted,line width=0.6pt] (0,0)--(0,%.3f) node[above,font=\scriptsize,text=navy]{%s};' % (H + 0.35, yl))
    return o
def tbar(cats, vals, kind='bar', yl='$f_i$', xl='', H=2.8, dx=0.9, step=None, y0=0, top=None, multi=False):
    n = len(cats); top = top or max(vals); st = step or nice(top - y0); top = math.ceil(top / st) * st
    W = dx * n + 0.2
    o = [r'\begin{tikzpicture}[baseline=(current bounding box.center),line cap=round,line join=round]'] + taxes(H, top, st, y0, yl, xl, W)
    Y = lambda v: H * (float(v) - y0) / (top - y0)
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = dx * (i + 0.5) + 0.1
        if kind in ('bar', 'both'):
            col = COLS[i % 4] if multi else 'teal'
            o.append(r'\draw[%s,fill=%s!35] (%.3f,0) rectangle (%.3f,%.3f);' % (col, col, x - dx * 0.3, x + dx * 0.3, Y(v)))
        o.append(r'\node[below,font=\scriptsize,inner sep=2pt] at (%.3f,0) {%s};' % (x, c))
    if kind in ('poly', 'both'):
        P = ['(%.3f,%.3f)' % (dx * (i + 0.5) + 0.1, Y(v)) for i, v in enumerate(vals)]
        o.append(r'\draw[violet,line width=1.1pt] %s;' % '--'.join(P))
        o += [r'\fill[violet] %s circle (1.6pt);' % p for p in P]
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def thist(edges, vals, poly=False, yl='$f_i$', xl='', H=2.8, W=5.6, step=None):
    a, b = edges[0], edges[-1]; top = max(vals); st = step or nice(top); top = math.ceil(top / st) * st
    X = lambda x: 0.3 + (W - 0.6) * (float(x) - a) / (b - a); Y = lambda v: H * float(v) / top
    o = [r'\begin{tikzpicture}[baseline=(current bounding box.center),line cap=round,line join=round]'] + taxes(H, top, st, 0, yl, xl, W)
    for i, v in enumerate(vals):
        o.append(r'\draw[teal,fill=teal!30] (%.3f,0) rectangle (%.3f,%.3f);' % (X(edges[i]), X(edges[i + 1]), Y(v)))
    for e in edges: o.append(r'\node[below,font=\tiny,inner sep=2pt] at (%.3f,0) {$%s$};' % (X(e), tn(e)))
    if poly:
        d = edges[1] - edges[0]
        P = [(a - Fr(d, 2), 0)] + [(Fr(edges[i] + edges[i + 1], 2), v) for i, v in enumerate(vals)] + [(b + Fr(d, 2), 0)]
        P = [(max(min(fr(x), b + Fr(3, 10) * (b - a) / Fr(str(W - 0.6))), a - Fr(3, 10) * (b - a) / Fr(str(W - 0.6))), y) for x, y in P]
        Q = ['(%.3f,%.3f)' % (X(x), Y(y)) for x, y in P]
        o.append(r'\draw[violet,line width=1.1pt] %s;' % '--'.join(Q))
        o += [r'\fill[violet] %s circle (1.5pt);' % q for q in Q[1:-1]]
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def tpie(cats, vals, r=1.45, lab='angle'):
    N = sum(vals); o = [r'\begin{tikzpicture}[baseline=(current bounding box.center)]']; a0 = Fr(90)
    for i, v in enumerate(vals):
        a1 = a0 - Fr(360 * v, N); col = COLS[i % 6]
        o.append(r'\fill[%s!70,draw=white,line width=0.8pt] (0,0)--(%.3f:%s) arc[start angle=%.3f,end angle=%.3f,radius=%scm]--cycle;' % (col, float(a0), r, float(a0), float(a1), r))
        if lab and 360 * v >= 30 * N:
            t = ('$%s^\\circ$' % tn(Fr(360 * v, N))) if lab == 'angle' else ('$%s\\,\\%%$' % tn(Fr(100 * v, N)))
            o.append(r'\node[font=\scriptsize\bfseries,text=white] at (%.3f:%.3f) {%s};' % (float((a0 + a1) / 2), r * 0.62, t))
        a0 = a1
    for i, c in enumerate(cats):
        y = 0.35 * (len(cats) - 1) / 2 - 0.35 * i
        o.append(r'\fill[%s!70] (%.2f,%.3f) rectangle ++(0.22,0.22); \node[right,font=\scriptsize] at (%.2f,%.3f) {%s};' % (COLS[i % 6], r + 0.4, y - 0.11, r + 0.65, y, c))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def tbox(rows, lo, hi, step, W=8.0, lab=''):
    """diagrama de caixes: rows = [(etiqueta, (mín, Q1, Me, Q3, màx))]"""
    X = lambda v: W * (float(v) - lo) / (hi - lo); n = len(rows); rh = 0.85
    o = [r'\begin{tikzpicture}[baseline=(current bounding box.center),line cap=round]']
    k = lo
    while k <= hi + 1e-9:
        o.append(r'\draw[muted!30,line width=0.3pt] (%.3f,0)--(%.3f,%.3f); \draw[muted] (%.3f,0.06)--(%.3f,-0.06) node[below,font=\tiny,text=muted,inner sep=1.5pt]{$%s$};' % (X(k), X(k), rh * n + 0.1, X(k), X(k), tn(k)))
        k += step
    o.append(r'\draw[muted,line width=0.6pt] (0,0)--(%.3f,0);' % W)
    if lab: o.append(r'\node[right,font=\scriptsize,text=navy] at (%.3f,0) {%s};' % (W + 0.1, lab))
    for j, (t, (a, q1, me, q3, b)) in enumerate(rows):
        y = rh * (n - j) - 0.3; col = COLS[j % 4]
        o.append(r'\draw[thick] (%.3f,%.3f)--(%.3f,%.3f) (%.3f,%.3f)--(%.3f,%.3f);' % (X(a), y, X(q1), y, X(q3), y, X(b), y))
        o.append(r'\draw[thick] (%.3f,%.3f)--(%.3f,%.3f) (%.3f,%.3f)--(%.3f,%.3f);' % (X(a), y - 0.13, X(a), y + 0.13, X(b), y - 0.13, X(b), y + 0.13))
        o.append(r'\draw[%s,thick,fill=%s!25] (%.3f,%.3f) rectangle (%.3f,%.3f);' % (col, col, X(q1), y - 0.22, X(q3), y + 0.22))
        o.append(r'\draw[accent,line width=1.6pt] (%.3f,%.3f)--(%.3f,%.3f);' % (X(me), y - 0.22, X(me), y + 0.22))
        if t: o.append(r'\node[left,font=\small\bfseries] at (-0.15,%.3f) {%s};' % (y, t))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]
Q_, D_, C_ = T('qualitativa', 'cualitativa'), T('quantitativa discreta', 'cuantitativa discreta'), T('quantitativa contínua', 'cuantitativa continua')

# =====================================================================
# 1. Població, mostra i variables
# =====================================================================
V11 = [(T("nombre de missatges enviats en un dia", "número de mensajes enviados en un día"), D_), (T("pes d'una maleta", "peso de una maleta"), C_), (T("marca del cotxe familiar", "marca del coche familiar"), Q_),
       (T("temps d'espera a la parada de l'autobús", "tiempo de espera en la parada del autobús"), C_), (T("nombre de germans", "número de hermanos"), D_), (T("nivell d'estudis (ESO, Batxillerat…)", "nivel de estudios (ESO, Bachillerato…)"), Q_)]
EQ(Fr(120, 2400) * 600, 30); EQ(Fr(120, 2400) * 1200, 60); EQ(Fr(840, 60), 14); EQ(9 + 4 * 14, 65); EQ(9 + 59 * 14, 835)
S_.append((T("Població, mostra i variables estadístiques", "Población, muestra y variables estadísticas"), [
 (1, T(r"Classifica aquestes variables en qualitatives, quantitatives discretes o quantitatives contínues:", r"Clasifica estas variables en cualitativas, cuantitativas discretas o cuantitativas continuas:") + tasks(2, [v for v, _ in V11])
     + recorda(T(r"Si els valors no són nombres, és \textbf{qualitativa}. Si són nombres que es \textbf{compten}, és discreta; si es \textbf{mesuren}, és contínua.", r"Si los valores no son números, es \textbf{cualitativa}. Si son números que se \textbf{cuentan}, es discreta; si se \textbf{miden}, es continua.")),
     tasks(2, [r'\rest{%s}' % t for _, t in V11])),
 (1, T(r"Per a saber quantes hores d'esport fan a la setmana els 900 alumnes d'un institut, se n'enquesta 90 triats a l'atzar. Indica la població, la mostra i la seua grandària, un individu i la variable estudiada (i de quin tipus és).",
       r"Para saber cuántas horas de deporte hacen a la semana los 900 alumnos de un instituto, se encuesta a 90 elegidos al azar. Indica la población, la muestra y su tamaño, un individuo y la variable estudiada (y de qué tipo es)."),
     T(r"Població: \rest{els 900 alumnes}. Mostra: \rest{els 90 enquestats} (grandària 90). Individu: cada alumne. Variable: hores d'esport a la setmana, \rest{quantitativa contínua}.",
       r"Población: \rest{los 900 alumnos}. Muestra: \rest{los 90 encuestados} (tamaño 90). Individuo: cada alumno. Variable: horas de deporte a la semana, \rest{cuantitativa continua}.")),
 (2, T(r"Raona si aquestes mostres són representatives:", r"Razona si estas muestras son representativas:")
     + tasks(1, [T(r"Per a conéixer l'esport preferit dels joves d'una ciutat, es pregunta a 50 persones que ixen d'un camp de futbol.", r"Para conocer el deporte preferido de los jóvenes de una ciudad, se pregunta a 50 personas que salen de un campo de fútbol."),
                 T(r"Per a conéixer l'alçada mitjana de l'alumnat d'un institut, es trien a l'atzar 5 alumnes de cada grup.", r"Para conocer la altura media del alumnado de un instituto, se eligen al azar 5 alumnos de cada grupo.")]),
     tasks(1, [T(r"\rest{No}: els qui van al futbol segurament prefereixen el futbol; el resultat eixiria inflat.", r"\rest{No}: quienes van al fútbol seguramente prefieren el fútbol; el resultado saldría inflado."),
               T(r"\rest{Sí}: hi ha alumnes de tots els grups i triats a l'atzar.", r"\rest{Sí}: hay alumnos de todos los grupos y elegidos al azar.")])),
 (2, T(r"Un poble té 2\,400 habitants: 600 menors de 18 anys, 1\,200 d'entre 18 i 65 anys i 600 de més de 65. Es vol fer una enquesta a 120 persones amb un mostreig estratificat. Quantes persones s'han de triar de cada grup d'edat?",
       r"Un pueblo tiene 2\,400 habitantes: 600 menores de 18 años, 1\,200 de entre 18 y 65 años y 600 de más de 65. Se quiere hacer una encuesta a 120 personas con un muestreo estratificado. ¿Cuántas personas hay que elegir de cada grupo de edad?")
     + recorda(T(r"En el mostreig \textbf{estratificat}, cada grup aporta a la mostra la mateixa proporció que té en la població.", r"En el muestreo \textbf{estratificado}, cada grupo aporta a la muestra la misma proporción que tiene en la población.")),
     T(r"$\frac{120}{2\,400}=\frac1{20}$: \ menors \ $\frac{600}{20}=\res{30}$; \ de 18 a 65 \ $\frac{1\,200}{20}=\res{60}$; \ més de 65 \ $\frac{600}{20}=\res{30}$.",
       r"$\frac{120}{2\,400}=\frac1{20}$: \ menores \ $\frac{600}{20}=\res{30}$; \ de 18 a 65 \ $\frac{1\,200}{20}=\res{60}$; \ más de 65 \ $\frac{600}{20}=\res{30}$.")),
 (3, T(r"De la llista dels 840 alumnes d'un institut volem triar-ne 60 amb un mostreig sistemàtic. Cada quants alumnes n'hem d'agafar un? Si el primer triat a l'atzar és el número 9, quins són el segon, el cinqué i l'últim?",
       r"De la lista de los 840 alumnos de un instituto queremos elegir 60 con un muestreo sistemático. ¿Cada cuántos alumnos tenemos que coger uno? Si el primero elegido al azar es el número 9, ¿cuáles son el segundo, el quinto y el último?"),
     T(r"$840:60=\res{14}$: un de cada 14. \ Segon: $9+14=\res{23}$; \ cinqué: $9+4\cdot14=\res{65}$; \ últim (el 60é): $9+59\cdot14=\res{835}$.",
       r"$840:60=\res{14}$: uno de cada 14. \ Segundo: $9+14=\res{23}$; \ quinto: $9+4\cdot14=\res{65}$; \ último (el 60.\textsuperscript{o}): $9+59\cdot14=\res{835}$.")),
]))

# =====================================================================
# 2. Taules de freqüències amb dades aïllades
# =====================================================================
LLI = [1, 2, 4, 2, 0, 1, 3, 2, 2, 2, 5, 2, 1, 1, 3, 4, 0, 0, 2, 2, 1, 3, 3, 1]
TL = freqs(LLI); assert TL == [(0, 3), (1, 6), (2, 8), (3, 4), (4, 2), (5, 1)] and len(LLI) == 24
FL = acc([f for _, f in TL]); assert FL == [3, 9, 17, 21, 23, 24]
EQ(24 - 21, 3); EQ(Fr(21, 24) * 100, '87.5')
F34 = [2, 7, 15, 22, 26, 28]; f34 = [F34[0]] + [F34[i] - F34[i - 1] for i in range(1, 6)]; assert f34 == [2, 5, 8, 7, 4, 2]
DAU = [9, 11, 10, 8, 12]; EQ(60 - sum(DAU), 10); AP(Fr(100 * 29, 60), '48.3', 1); AP(Fr(100 * 22, 60), '36.7', 1)
EQ(Fr(16) / fr('0.4'), 40); EQ(1 - fr('0.25') - fr('0.4'), '0.35'); EQ(fr('0.25') * 40, 10); EQ(fr('0.35') * 40, 14)
EQ(Fr(100 * 13, 25), 52)
ESP = [(T('Futbol', 'Fútbol'), 14), (T('Bàsquet', 'Baloncesto'), 10), (T('Tenis', 'Tenis'), 6), (T('Natació', 'Natación'), 8), (T('Altres', 'Otros'), 2)]
EQ(fr('0.25') * 40, 10); EQ(fr('0.15') * 40, 6); EQ(40 - 14 - 10 - 6 - 8, 2)
TAB_ESP = (r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|C{1.2cm}|C{1.2cm}|C{1.2cm}|}\hline ' + T('Esport', 'Deporte') + r' & $f_i$ & $h_i$ & \%\\\hline '
           + T('Futbol', 'Fútbol') + r' & 14 & & \\\hline ' + T('Bàsquet', 'Baloncesto') + r' & & $0{,}25$ & \\\hline Tenis & & & 15\\\hline ' + T('Natació', 'Natación') + r' & 8 & & \\\hline ' + T('Altres', 'Otros') + r' & & & \\\hline \textbf{Total} & 40 & & \\\hline\end{tabular}}')
S_.append((T("Taules de freqüències amb dades aïllades", "Tablas de frecuencias con datos aislados"), [
 (1, T(r"Aquests són els llibres que han llegit en un mes 24 alumnes: \ $%s$. \ Fes la taula de freqüències amb $f_i$, $F_i$, $h_i$ i percentatges.", r"Estos son los libros que han leído en un mes 24 alumnos: \ $%s$. \ Haz la tabla de frecuencias con $f_i$, $F_i$, $h_i$ y porcentajes.") % lst(LLI),
     center(ftab([x for x, _ in TL], [f for _, f in TL], ('f', 'F', 'h', 'p')))),
 (1, T(r"Amb la taula de l'exercici anterior, respon:", r"Con la tabla del ejercicio anterior, responde:")
     + tasks(2, [T(r"Quants alumnes han llegit com a molt 2 llibres?", r"¿Cuántos alumnos han leído como mucho 2 libros?"), T(r"Quants n'han llegit més de 3?", r"¿Cuántos han leído más de 3?"),
                 T(r"Quin percentatge n'ha llegit 3 o menys?", r"¿Qué porcentaje ha leído 3 o menos?"), T(r"Quin percentatge no n'ha llegit cap?", r"¿Qué porcentaje no ha leído ninguno?")]),
     tasks(2, [r'$F=\res{17}$', r'$24-21=\res{3}$', r'$\frac{21}{24}=\res{87{,}5\,\%}$', r'$\frac{3}{24}=\res{12{,}5\,\%}$'])),
 (2, T(r"Completa la taula de l'esport preferit de 40 alumnes:", r"Completa la tabla del deporte preferido de 40 alumnos:") + center(TAB_ESP),
     center(ftab([e for e, _ in ESP], [f for _, f in ESP], ('f', 'h', 'p'), xl=T('Esport', 'Deporte')))),
 (2, T(r"En aquesta taula, $x_i$ és el nombre de visites al dentista en un any i $F_i$, la freqüència acumulada. Troba les freqüències absolutes. Quantes persones hi han anat exactament 3 vegades? I almenys 2 vegades?", r"En esta tabla, $x_i$ es el número de visitas al dentista en un año y $F_i$, la frecuencia acumulada. Encuentra las frecuencias absolutas. ¿Cuántas personas han ido exactamente 3 veces? ¿Y al menos 2 veces?")
     + center(htab(list(range(6)), F34, fl='$F_i$')),
     T(r"$f_i$: \ 2, 5, 8, 7, 4, 2. \ Exactament 3: $\res{7}$. \ Almenys 2: $28-7=\res{21}$.", r"$f_i$: \ 2, 5, 8, 7, 4, 2. \ Exactamente 3: $\res{7}$. \ Al menos 2: $28-7=\res{21}$.")),
 (2, T(r"Hem llançat un dau 60 vegades. Ha eixit l'1 nou vegades, el 2 onze, el 3 deu, el 4 huit, el 5 dotze i el 6 la resta. Quantes vegades ha eixit el 6? Quin percentatge dels llançaments ha eixit un nombre parell? I un nombre més gran que 4?",
       r"Hemos lanzado un dado 60 veces. Ha salido el 1 nueve veces, el 2 once, el 3 diez, el 4 ocho, el 5 doce y el 6 el resto. ¿Cuántas veces ha salido el 6? ¿Qué porcentaje de los lanzamientos ha salido un número par? ¿Y un número mayor que 4?"),
     T(r"$f_6=60-50=\res{10}$. \ Parell: $11+8+10=29$, \ $\frac{29}{60}\approx\res{48{,}3\,\%}$. \ Més gran que 4: $12+10=22$, \ $\frac{22}{60}\approx\res{36{,}7\,\%}$.",
       r"$f_6=60-50=\res{10}$. \ Par: $11+8+10=29$, \ $\frac{29}{60}\approx\res{48{,}3\,\%}$. \ Mayor que 4: $12+10=22$, \ $\frac{22}{60}\approx\res{36{,}7\,\%}$.")),
 (3, T(r"Una variable pren tres valors, $A$, $B$ i $C$. La freqüència relativa d'$A$ és $0{,}25$; la de $B$, $0{,}4$, i la freqüència absoluta de $B$ és 16. Calcula $N$, la freqüència relativa de $C$ i totes les freqüències absolutes.",
       r"Una variable toma tres valores, $A$, $B$ y $C$. La frecuencia relativa de $A$ es $0{,}25$; la de $B$, $0{,}4$, y la frecuencia absoluta de $B$ es 16. Calcula $N$, la frecuencia relativa de $C$ y todas las frecuencias absolutas."),
     T(r"$N=16:0{,}4=\res{40}$; \ $h_C=1-0{,}25-0{,}4=\res{0{,}35}$; \ $f_A=0{,}25\cdot40=\res{10}$, \ $f_B=16$, \ $f_C=0{,}35\cdot40=\res{14}$.",
       r"$N=16:0{,}4=\res{40}$; \ $h_C=1-0{,}25-0{,}4=\res{0{,}35}$; \ $f_A=0{,}25\cdot40=\res{10}$, \ $f_B=16$, \ $f_C=0{,}35\cdot40=\res{14}$.")),
 (3, T(r"En una taula de freqüències, $F_3=12$, $F_4=19$ i $F_5=25$, i 5 és el valor més gran. Quantes dades hi ha? Quina és la freqüència absoluta del 4? Quin percentatge de les dades és més gran que 3?",
       r"En una tabla de frecuencias, $F_3=12$, $F_4=19$ y $F_5=25$, y 5 es el valor mayor. ¿Cuántos datos hay? ¿Cuál es la frecuencia absoluta del 4? ¿Qué porcentaje de los datos es mayor que 3?"),
     T(r"$N=F_5=\res{25}$; \ $f_4=19-12=\res{7}$; \ més grans que 3: $25-12=13$, \ $\frac{13}{25}=\res{52\,\%}$.", r"$N=F_5=\res{25}$; \ $f_4=19-12=\res{7}$; \ mayores que 3: $25-12=13$, \ $\frac{13}{25}=\res{52\,\%}$.")),
]))

# =====================================================================
# 3. Taules amb dades agrupades
# =====================================================================
PUN = [52, 67, 45, 73, 38, 61, 55, 80, 49, 64, 58, 71, 43, 66, 59, 35, 77, 62, 50, 69, 57, 84, 47, 63, 54, 74, 41, 68, 60, 56, 31, 79, 65, 51, 88, 70, 46, 58, 62, 53]
EDP = [30, 40, 50, 60, 70, 80, 90]; FP = [sum(1 for x in PUN if EDP[i] <= x < EDP[i + 1]) for i in range(6)]
assert len(PUN) == 40 and min(PUN) == 31 and max(PUN) == 88 and FP == [3, 6, 11, 11, 6, 3], FP
EQ(88 - 31, 57); AP(math.sqrt(40), '6.3', 1); EQ(Fr(57, 6), '9.5'); EQ(Fr(100 * 9, 40), '22.5')
PES = [48, 55, 61, 44, 52, 58, 63, 47, 50, 56, 59, 66, 45, 53, 57, 60, 49, 54, 62, 51, 58, 64, 46, 55]
EDW = [40, 45, 50, 55, 60, 65, 70]; FW = [sum(1 for x in PES if EDW[i] <= x < EDW[i + 1]) for i in range(6)]
assert len(PES) == 24 and FW == [1, 5, 5, 7, 5, 1], FW
AP(Fr(100 * (1 + 5 + 5), 24), "45.8", 1)
ALT = [150, 155, 160, 165, 170, 175, 180]; FAL = [4, 9, 15, 12, 7, 3]; assert sum(FAL) == 50 and acc(FAL) == [4, 13, 28, 40, 47, 50]
EQ(Fr(100 * 10, 50), 20)
S_.append((T("Taules amb dades agrupades en intervals", "Tablas con datos agrupados en intervalos"), [
 (1, T(r"Els intervals d'una taula són $[10,\ 15)$, $[15,\ 20)$, $[20,\ 25)$ i $[25,\ 30)$. En quin interval va cadascuna d'aquestes dades? Quina és la marca de classe de cada interval?", r"Los intervalos de una tabla son $[10,\ 15)$, $[15,\ 20)$, $[20,\ 25)$ y $[25,\ 30)$. ¿En qué intervalo va cada uno de estos datos? ¿Cuál es la marca de clase de cada intervalo?")
     + tasks(4, ['$15$', '$24{,}9$', '$25$', '$10$']),
     tasks(4, [r'$\res{[15,\ 20)}$', r'$\res{[20,\ 25)}$', r'$\res{[25,\ 30)}$', r'$\res{[10,\ 15)}$']) + T(r"Marques: \ $12{,}5$, \ $17{,}5$, \ $22{,}5$ \ i \ $27{,}5$.", r"Marcas: \ $12{,}5$, \ $17{,}5$, \ $22{,}5$ \ y \ $27{,}5$.")),
 (1, T(r"Aquests són els pesos (en kg) de 24 alumnes: \ $%s$. \ Agrupa'ls en intervals d'amplitud 5 des de 40\,kg i fes la taula amb les marques de classe, $f_i$, $F_i$ i percentatges. Quin percentatge pesa menys de 55\,kg?", r"Estos son los pesos (en kg) de 24 alumnos: \ $%s$. \ Agrúpalos en intervalos de amplitud 5 desde 40\,kg y haz la tabla con las marcas de clase, $f_i$, $F_i$ y porcentajes. ¿Qué porcentaje pesa menos de 55\,kg?") % lst(PES)
     + recorda(T(r"L'interval $[a,\ b)$ conté les dades $\geq a$ i $<b$. La \textbf{marca de classe} és el punt mitjà: $\frac{a+b}{2}$.", r"El intervalo $[a,\ b)$ contiene los datos $\geq a$ y $<b$. La \textbf{marca de clase} es el punto medio: $\frac{a+b}{2}$.")),
     center(gtab(EDW, FW, ('m', 'f', 'F', 'p'), xl=T('Pes (kg)', 'Peso (kg)'))) + T(r"Menys de 55\,kg: $F=11$, \ $\frac{11}{24}\approx\res{45{,}8\,\%}$.", r"Menos de 55\,kg: $F=11$, \ $\frac{11}{24}\approx\res{45{,}8\,\%}$.")),
 (2, T(r"Les puntuacions de 40 alumnes en un test han sigut: \ $%s$. \ Decideix quants intervals fas i de quina amplitud (fes servir la regla de l'arrel) i fes la taula de freqüències. Quin percentatge ha tret menys de 50 punts?", r"Las puntuaciones de 40 alumnos en un test han sido: \ $%s$. \ Decide cuántos intervalos haces y de qué amplitud (usa la regla de la raíz) y haz la tabla de frecuencias. ¿Qué porcentaje ha sacado menos de 50 puntos?") % lst(PUN)
     + recorda(T(r"Rang $=x_{\max}-x_{\min}$. \ Nombre d'intervals $\approx\sqrt N$. \ Amplitud $\approx\frac{\text{rang}}{\text{nre. d'intervals}}$, arrodonida cap amunt.", r"Rango $=x_{\max}-x_{\min}$. \ Número de intervalos $\approx\sqrt N$. \ Amplitud $\approx\frac{\text{rango}}{\text{n.\textsuperscript{o} de intervalos}}$, redondeada hacia arriba.")),
     T(r"Rang: $88-31=57$. \ $\sqrt{40}\approx6{,}3\to$ \rest{6 intervals}; \ $57:6=9{,}5\to$ amplitud \res{10}, des de 30:", r"Rango: $88-31=57$. \ $\sqrt{40}\approx6{,}3\to$ \rest{6 intervalos}; \ $57:6=9{,}5\to$ amplitud \res{10}, desde 30:")
     + center(gtab(EDP, FP, ('m', 'f', 'F', 'p'), xl=T('Punts', 'Puntos'))) + T(r"Menys de 50: $F=9$, \ $\frac{9}{40}=\res{22{,}5\,\%}$.", r"Menos de 50: $F=9$, \ $\frac{9}{40}=\res{22{,}5\,\%}$.")),
 (2, T(r"La taula recull les alçades (en cm) de 50 alumnes. Fes la columna de les $F_i$ i respon: quants alumnes fan menys de 165\,cm? Quin percentatge fa 170\,cm o més? Quants fan entre 155 i 170\,cm?", r"La tabla recoge las alturas (en cm) de 50 alumnos. Haz la columna de las $F_i$ y responde: ¿cuántos alumnos miden menos de 165\,cm? ¿Qué porcentaje mide 170\,cm o más? ¿Cuántos miden entre 155 y 170\,cm?")
     + center(htab([ivl(ALT[i], ALT[i + 1]) for i in range(6)], FAL, xl=T('Alçada', 'Altura'), w='1.6cm')),
     center(gtab(ALT, FAL, ('m', 'f', 'F'))) + T(r"Menys de 165: $F=\res{28}$. \ 170 o més: $7+3=10$, \ $\res{20\,\%}$. \ Entre 155 i 170: $9+15+12=\res{36}$.", r"Menos de 165: $F=\res{28}$. \ 170 o más: $7+3=10$, \ $\res{20\,\%}$. \ Entre 155 y 170: $9+15+12=\res{36}$.")),
 (3, T(r"Les marques de classe d'una taula són 4, 8, 12 i 16, i tots els intervals tenen la mateixa amplitud. Quins són els intervals? I si un interval té marca $32{,}5$ i amplitud 5?", r"Las marcas de clase de una tabla son 4, 8, 12 y 16, y todos los intervalos tienen la misma amplitud. ¿Cuáles son los intervalos? ¿Y si un intervalo tiene marca $32{,}5$ y amplitud 5?"),
     T(r"Les marques es separen 4: amplitud 4, i cada interval comença 2 abans de la marca: \ $\res{[2,\ 6)}$, $\res{[6,\ 10)}$, $\res{[10,\ 14)}$, $\res{[14,\ 18)}$. \ Amb marca $32{,}5$ i amplitud 5: $\res{[30,\ 35)}$.",
       r"Las marcas se separan 4: amplitud 4, y cada intervalo empieza 2 antes de la marca: \ $\res{[2,\ 6)}$, $\res{[6,\ 10)}$, $\res{[10,\ 14)}$, $\res{[14,\ 18)}$. \ Con marca $32{,}5$ y amplitud 5: $\res{[30,\ 35)}$.")),
]))

# =====================================================================
# 4. Gràfics estadístics
# =====================================================================
VIA = [(0, 5), (1, 8), (2, 6), (3, 4), (4, 2)]; EQ(sum(f for _, f in VIA), 25); EQ(4 + 2, 6)
TRA = [(T('A peu', 'A pie'), 15), (T('Autobús', 'Autobús'), 12), (T('Cotxe', 'Coche'), 6), (T('Bici', 'Bici'), 3)]
EQ(sum(f for _, f in TRA), 36); EQ(Fr(360, 36), 10)
P53 = [(T('Platja', 'Playa'), 108), (T('Muntanya', 'Montaña'), 90), (T('Ciutat', 'Ciudad'), 72), (T('Poble', 'Pueblo'), 60), (T('Estranger', 'Extranjero'), 30)]
assert sum(a for _, a in P53) == 360
for (_, a), n in zip(P53, [36, 30, 24, 20, 10]): EQ(Fr(a, 360) * 120, n)
S_.append((T("Gràfics estadístics", "Gráficos estadísticos"), [
 (1, T(r"Dibuixa el diagrama de barres i el polígon de freqüències dels llibres llegits pels 24 alumnes de la secció 2 (exercici 6).", r"Dibuja el diagrama de barras y el polígono de frecuencias de los libros leídos por los 24 alumnos de la sección 2 (ejercicio 6).")
     + recorda(T(r"En un \textbf{diagrama de barres}, les barres van separades i tenen l'altura de la freqüència. El \textbf{polígon} uneix els extrems de dalt de les barres.", r"En un \textbf{diagrama de barras}, las barras van separadas y tienen la altura de la frecuencia. El \textbf{polígono} une los extremos de arriba de las barras.")),
     center(tbar([str(x) for x, _ in TL], [f for _, f in TL], kind='both', yl=T('Alumnes', 'Alumnos'), xl=T('Llibres', 'Libros')))),
 (1, T(r"Els 36 alumnes d'una classe vénen a l'institut així: a peu 15, en autobús 12, en cotxe 6 i en bici 3. Calcula l'angle de cada sector i dibuixa el diagrama de sectors.", r"Los 36 alumnos de una clase vienen al instituto así: a pie 15, en autobús 12, en coche 6 y en bici 3. Calcula el ángulo de cada sector y dibuja el diagrama de sectores.")
     + recorda(T(r"Angle del sector $=\dfrac{f_i}{N}\cdot360^\circ$.", r"Ángulo del sector $=\dfrac{f_i}{N}\cdot360^\circ$.")),
     T(r"Cada alumne val $360^\circ:36=10^\circ$: \ $\res{150^\circ}$, \ $\res{120^\circ}$, \ $\res{60^\circ}$, \ $\res{30^\circ}$.", r"Cada alumno vale $360^\circ:36=10^\circ$: \ $\res{150^\circ}$, \ $\res{120^\circ}$, \ $\res{60^\circ}$, \ $\res{30^\circ}$.") + center(tpie([c for c, _ in TRA], [f for _, f in TRA]))),
 (2, T(r"Aquest diagrama mostra quantes vegades han viatjat en avió els alumnes d'una classe. Fes la taula de freqüències. Quants alumnes hi ha? Quina és la moda? Quants han viatjat 3 o més vegades?", r"Este diagrama muestra cuántas veces han viajado en avión los alumnos de una clase. Haz la tabla de frecuencias. ¿Cuántos alumnos hay? ¿Cuál es la moda? ¿Cuántos han viajado 3 o más veces?")
     + center(tbar([str(x) for x, _ in VIA], [f for _, f in VIA], yl=T('Alumnes', 'Alumnos'), xl=T('Viatges', 'Viajes'))),
     center(htab([x for x, _ in VIA], [f for _, f in VIA])) + T(r"$N=\res{25}$ alumnes; \ $Mo=\res{1}$ viatge; \ 3 o més: $4+2=\res{6}$.", r"$N=\res{25}$ alumnos; \ $Mo=\res{1}$ viaje; \ 3 o más: $4+2=\res{6}$.")),
 (2, T(r"Dibuixa l'histograma i el polígon de freqüències de les alçades dels 50 alumnes de la secció 3 (exercici 16).", r"Dibuja el histograma y el polígono de frecuencias de las alturas de los 50 alumnos de la sección 3 (ejercicio 16).")
     + recorda(T(r"En un \textbf{histograma} les barres ocupen tot l'interval i van juntes. El polígon uneix els punts de dalt sobre les marques de classe i es tanca en l'eix.", r"En un \textbf{histograma} las barras ocupan todo el intervalo y van juntas. El polígono une los puntos de arriba sobre las marcas de clase y se cierra en el eje.")),
     center(thist(ALT, FAL, poly=True, yl=T('Alumnes', 'Alumnos'), xl='cm'))),
 (2, T(r"S'ha preguntat a 120 persones on prefereixen passar les vacances. Quantes persones han triat cada lloc?", r"Se ha preguntado a 120 personas dónde prefieren pasar las vacaciones. ¿Cuántas personas han elegido cada lugar?") + center(tpie([c for c, _ in P53], [a for _, a in P53])),
     T(r"$f_i=\frac{\text{angle}}{360^\circ}\cdot120$: \ platja $\res{36}$, \ muntanya $\res{30}$, \ ciutat $\res{24}$, \ poble $\res{20}$, \ estranger $\res{10}$.", r"$f_i=\frac{\text{ángulo}}{360^\circ}\cdot120$: \ playa $\res{36}$, \ montaña $\res{30}$, \ ciudad $\res{24}$, \ pueblo $\res{20}$, \ extranjero $\res{10}$.")),
 (3, T(r"Quin gràfic triaries per a representar cada variable? Justifica-ho.", r"¿Qué gráfico elegirías para representar cada variable? Justifícalo.")
     + tasks(1, [T(r"el nombre de germans de 30 alumnes;", r"el número de hermanos de 30 alumnos;"), T(r"l'alçada de 200 persones;", r"la altura de 200 personas;"),
                 T(r"el partit que voten 500 persones;", r"el partido que votan 500 personas;"), T(r"els minuts que tarden 50 alumnes a fer els deures.", r"los minutos que tardan 50 alumnos en hacer los deberes.")]),
     tasks(1, [T(r"\rest{diagrama de barres} (discreta);", r"\rest{diagrama de barras} (discreta);"), T(r"\rest{histograma} (contínua, agrupada en intervals);", r"\rest{histograma} (continua, agrupada en intervalos);"),
               T(r"\rest{diagrama de sectors} o de barres (qualitativa: interessa la part del total);", r"\rest{diagrama de sectores} o de barras (cualitativa: interesa la parte del total);"), T(r"\rest{histograma} (contínua).", r"\rest{histograma} (continua).")])),
 (3, T(r"Tres candidats han tret 96, 92 i 98 vots. Un cartell els representa amb un diagrama de barres en què l'eix vertical comença en 90. Per què és enganyós? Dibuixa'l bé.", r"Tres candidatos han sacado 96, 92 y 98 votos. Un cartel los representa con un diagrama de barras en el que el eje vertical empieza en 90. ¿Por qué es engañoso? Dibújalo bien."),
     T(r"Començant en 90, la barra de 98 sembla \rest{quatre vegades} la de 92 ($8$ contra $2$), però la diferència real és de 6 vots sobre uns 95 (un $6\,\%$ aprox.). L'eix ha de començar en 0:", r"Empezando en 90, la barra de 98 parece \rest{cuatro veces} la de 92 ($8$ contra $2$), pero la diferencia real es de 6 votos sobre unos 95 (un $6\,\%$ aprox.). El eje tiene que empezar en 0:")
     + center(tbar(['A', 'B', 'C'], [96, 92, 98], yl=T('Vots', 'Votos'), H=2.2, step=20, top=100))),
]))
EQ(98 - 90, 8); EQ(92 - 90, 2)

# =====================================================================
# 5. Paràmetres de centralització
# =====================================================================
D51 = [7, 4, 9, 7, 3, 8, 7, 5, 6]; CHK(modes(D51) == [7] and mean(D51) == Fr(56, 9) and median(D51) == 7); AP(mean(D51), '6.22')
D52 = [12, 15, 9, 20, 14, 16, 11, 15]; CHK(modes(D52) == [15] and mean(D52) == 14 and median(D52) == Fr(29, 2))
T53 = [(1, 4), (2, 7), (3, 9), (4, 6), (5, 4)]; D53 = expand(T53); CHK(len(D53) == 30 and sum(D53) == 89 and median(D53) == 3 and modes(D53) == [3] and acc([f for _, f in T53]) == [4, 11, 20, 26, 30]); AP(mean(D53), '2.97')
SM = sum(Fr(ALT[i] + ALT[i + 1], 2) * f for i, f in enumerate(FAL)); EQ(SM, 8215); EQ(SM / 50, '164.3')
EQ(fr('6.5') * 4 - (6 + 7 + 5), 8); EQ(Fr(fr('6.4') * 25 + fr('7.2') * 15, 40), '6.7')
SOU = [1100, 1200, 1250, 1300, 4650]; CHK(mean(SOU) == 1900 and median(SOU) == 1250)
CHK(mean(expand([(0, 4), (1, 3), (2, 6), (3, 2)])) == fr('1.4'))
EQ(fr('1.4') * 15 - 18, 3)
S_.append((T("Paràmetres de centralització", "Parámetros de centralización"), [
 (1, T(r"Calcula la moda, la mitjana i la mediana de: \ $%s$.", r"Calcula la moda, la media y la mediana de: \ $%s$.") % lst(D51)
     + recorda(T(r"\textbf{Moda}: el valor més repetit. \textbf{Mitjana}: $\bar x=\dfrac{\text{suma de les dades}}{N}$. \textbf{Mediana}: el valor central de les dades \textbf{ordenades}; si n'hi ha dos, la seua mitjana.", r"\textbf{Moda}: el valor más repetido. \textbf{Media}: $\bar x=\dfrac{\text{suma de los datos}}{N}$. \textbf{Mediana}: el valor central de los datos \textbf{ordenados}; si hay dos, su media.")),
     T(r"$Mo=\res{7}$; \ $\bar x=\frac{56}{9}\approx\res{6{,}22}$; \ ordenades: $3,\ 4,\ 5,\ 6,\ 7,\ 7,\ 7,\ 8,\ 9$ \ $\Rightarrow$ \ $Me=\res{7}$.", r"$Mo=\res{7}$; \ $\bar x=\frac{56}{9}\approx\res{6{,}22}$; \ ordenados: $3,\ 4,\ 5,\ 6,\ 7,\ 7,\ 7,\ 8,\ 9$ \ $\Rightarrow$ \ $Me=\res{7}$.")),
 (1, T(r"Calcula la moda, la mitjana i la mediana de: \ $%s$.", r"Calcula la moda, la media y la mediana de: \ $%s$.") % lst(D52),
     T(r"$Mo=\res{15}$; \ $\bar x=\frac{112}{8}=\res{14}$; \ ordenades: $9,\ 11,\ 12,\ 14,\ 15,\ 15,\ 16,\ 20$ \ $\Rightarrow$ \ $Me=\frac{14+15}{2}=\res{14{,}5}$.", r"$Mo=\res{15}$; \ $\bar x=\frac{112}{8}=\res{14}$; \ ordenados: $9,\ 11,\ 12,\ 14,\ 15,\ 15,\ 16,\ 20$ \ $\Rightarrow$ \ $Me=\frac{14+15}{2}=\res{14{,}5}$.")),
 (2, T(r"La taula recull quantes vegades han anat al cine en els últims tres mesos 30 alumnes. Calcula la moda, la mitjana i la mediana.", r"La tabla recoge cuántas veces han ido al cine en los últimos tres meses 30 alumnos. Calcula la moda, la media y la mediana.")
     + center(htab([x for x, _ in T53], [f for _, f in T53]))
     + recorda(T(r"Amb una taula: $\bar x=\dfrac{\sum x_i\cdot f_i}{N}$. Per a la mediana, mira en la columna $F_i$ on arriba la posició central.", r"Con una tabla: $\bar x=\dfrac{\sum x_i\cdot f_i}{N}$. Para la mediana, mira en la columna $F_i$ dónde llega la posición central.")),
     center(ftab([x for x, _ in T53], [f for _, f in T53], ('f', 'F', 'xf'))) + T(r"$\bar x=\frac{89}{30}\approx\res{2{,}97}$; \ centrals: 15a i 16a $\to F=20$: $Me=\res{3}$; \ $Mo=\res{3}$.", r"$\bar x=\frac{89}{30}\approx\res{2{,}97}$; \ centrales: 15.\textsuperscript{o} y 16.\textsuperscript{o} $\to F=20$: $Me=\res{3}$; \ $Mo=\res{3}$.")),
 (2, T(r"Calcula la mitjana aproximada de les alçades dels 50 alumnes de la secció 3 (exercici 16). Quin és l'interval modal? I l'interval medià?", r"Calcula la media aproximada de las alturas de los 50 alumnos de la sección 3 (ejercicio 16). ¿Cuál es el intervalo modal? ¿Y el intervalo mediano?"),
     center(gtab(ALT, FAL, ('m', 'f', 'F', 'mf'))) + T(r"$\bar x\approx\frac{8\,215}{50}=\res{164{,}3\text{ cm}}$. \ Interval modal: $\res{[160,\ 165)}$. \ $\frac N2=25\to F=28$: interval medià $\res{[160,\ 165)}$.", r"$\bar x\approx\frac{8\,215}{50}=\res{164{,}3\text{ cm}}$. \ Intervalo modal: $\res{[160,\ 165)}$. \ $\frac N2=25\to F=28$: intervalo mediano $\res{[160,\ 165)}$.")),
 (2, T(r"Pau ha tret 6, 7 i 5 en tres exàmens. Quina nota necessita en el quart per a tindre una mitjana de $6{,}5$?", r"Pau ha sacado 6, 7 y 5 en tres exámenes. ¿Qué nota necesita en el cuarto para tener una media de $6{,}5$?")
     + recorda(T(r"Si coneixem la mitjana i el nombre de dades, coneixem la suma: \ $\text{suma}=\bar x\cdot N$.", r"Si conocemos la media y el número de datos, conocemos la suma: \ $\text{suma}=\bar x\cdot N$.")),
     T(r"Suma necessària: $6{,}5\cdot4=26$; \ ja té $18$: \ necessita un $\res{8}$.", r"Suma necesaria: $6{,}5\cdot4=26$; \ ya tiene $18$: \ necesita un $\res{8}$.")),
 (2, T(r"En una classe de 25 alumnes la nota mitjana d'un examen ha sigut $6{,}4$ i en una altra de 15 alumnes, $7{,}2$. Quina és la nota mitjana dels 40 alumnes?", r"En una clase de 25 alumnos la nota media de un examen ha sido $6{,}4$ y en otra de 15 alumnos, $7{,}2$. ¿Cuál es la nota media de los 40 alumnos?"),
     T(r"$6{,}4\cdot25=160$; \ $7{,}2\cdot15=108$; \ $\bar x=\frac{268}{40}=\res{6{,}7}$ \ (no és la mitjana de les mitjanes, $6{,}8$).", r"$6{,}4\cdot25=160$; \ $7{,}2\cdot15=108$; \ $\bar x=\frac{268}{40}=\res{6{,}7}$ \ (no es la media de las medias, $6{,}8$).")),
 (3, T(r"En una empresa xicoteta, quatre persones cobren 1\,100, 1\,200, 1\,250 i 1\,300\,€ al mes, i el gerent, 4\,650\,€. Calcula la mitjana i la mediana dels sous. Quin paràmetre representa millor el sou d'un treballador?", r"En una empresa pequeña, cuatro personas cobran 1\,100, 1\,200, 1\,250 y 1\,300\,€ al mes, y el gerente, 4\,650\,€. Calcula la media y la mediana de los sueldos. ¿Qué parámetro representa mejor el sueldo de un trabajador?"),
     T(r"$\bar x=\frac{9\,500}{5}=\res{1\,900\text{ €}}$; \ $Me=\res{1\,250\text{ €}}$. \ La \rest{mediana}: el sou del gerent és una dada extrema que estira la mitjana cap amunt.", r"$\bar x=\frac{9\,500}{5}=\res{1\,900\text{ €}}$; \ $Me=\res{1\,250\text{ €}}$. \ La \rest{mediana}: el sueldo del gerente es un dato extremo que estira la media hacia arriba.")),
 (3, T(r"En aquesta taula falta una freqüència. Troba-la sabent que la mitjana és $1{,}4$.", r"En esta tabla falta una frecuencia. Encuéntrala sabiendo que la media es $1{,}4$.") + center(htab([0, 1, 2, 3], ['$4$', '$a$', '$6$', '$2$'])),
     T(r"$\frac{0\cdot4+1\cdot a+2\cdot6+3\cdot2}{12+a}=1{,}4\Rightarrow a+18=16{,}8+1{,}4a\Rightarrow1{,}2=0{,}4a\Rightarrow\res{a=3}$.", r"$\frac{0\cdot4+1\cdot a+2\cdot6+3\cdot2}{12+a}=1{,}4\Rightarrow a+18=16{,}8+1{,}4a\Rightarrow1{,}2=0{,}4a\Rightarrow\res{a=3}$.")),
]))

# =====================================================================
# 6. Paràmetres de dispersió
# =====================================================================
D61 = [3, 7, 8, 10, 12]; CHK(mean(D61) == 8 and rang(D61) == 9 and dm(D61) == Fr(12, 5))
D62 = [2, 4, 5, 7, 7]; CHK(mean(D62) == 5 and var(D62) == Fr(18, 5)); AP(math.sqrt(var(D62)), '1.90')
T63 = [(0, 5), (1, 8), (2, 4), (3, 2), (4, 1)]; D63 = expand(T63); CHK(mean(D63) == fr('1.3') and var(D63) == fr('1.21')); EQ(sum(x * x * f for x, f in T63), 58)
A64 = [6, 7, 7, 8, 7]; B64 = [10, 4, 9, 5, 7]; CHK(mean(A64) == mean(B64) == 7 and var(A64) == Fr(2, 5) and var(B64) == Fr(26, 5))
AP(math.sqrt(var(A64)), '0.63'); AP(math.sqrt(var(B64)), '2.28')
EQ(Fr(8, 160) * 100, 5); EQ(Fr(4, 40) * 100, 10)
S2A = sum(Fr(ALT[i] + ALT[i + 1], 2) ** 2 * f for i, f in enumerate(FAL)); EQ(S2A, Fr(2703725, 2)); EQ(S2A / 50 - (SM / 50) ** 2, '42.76')
AP(math.sqrt(42.76), '6.54'); AP(100 * math.sqrt(42.76) / 164.3, '3.98')
D2x = [2 * x for x in D62]; D5 = [x + 5 for x in D62]
CHK(mean(D5) == 10 and var(D5) == var(D62) and mean(D2x) == 10 and var(D2x) == 4 * var(D62))
AP(100 * math.sqrt(var(D62)) / 5, '37.95'); AP(100 * math.sqrt(var(D5)) / 10, '18.97'); AP(100 * math.sqrt(var(D2x)) / 10, '37.95')
AP(Fr(3, 1002) * 100, '0.30'); AP(Fr(8, 998) * 100, '0.80')
S_.append((T("Paràmetres de dispersió", "Parámetros de dispersión"), [
 (1, T(r"Calcula el rang i la desviació mitjana de: \ $%s$.", r"Calcula el rango y la desviación media de: \ $%s$.") % lst(D61)
     + recorda(T(r"Rang $=x_{\max}-x_{\min}$. \ $DM=\dfrac{\sum|x_i-\bar x|}{N}$.", r"Rango $=x_{\max}-x_{\min}$. \ $DM=\dfrac{\sum|x_i-\bar x|}{N}$.")),
     T(r"Rang $=12-3=\res{9}$; \ $\bar x=8$; \ distàncies 5, 1, 0, 2, 4: \ $DM=\frac{12}{5}=\res{2{,}4}$.", r"Rango $=12-3=\res{9}$; \ $\bar x=8$; \ distancias 5, 1, 0, 2, 4: \ $DM=\frac{12}{5}=\res{2{,}4}$.")),
 (1, T(r"Calcula la variància i la desviació típica de: \ $%s$.", r"Calcula la varianza y la desviación típica de: \ $%s$.") % lst(D62)
     + recorda(T(r"$\sigma^2=\dfrac{\sum(x_i-\bar x)^2}{N}$ \ o bé \ $\sigma^2=\dfrac{\sum x_i^2}{N}-\bar x^{\,2}$. \ $\sigma=\sqrt{\sigma^2}$.", r"$\sigma^2=\dfrac{\sum(x_i-\bar x)^2}{N}$ \ o bien \ $\sigma^2=\dfrac{\sum x_i^2}{N}-\bar x^{\,2}$. \ $\sigma=\sqrt{\sigma^2}$.")),
     r"$\bar x=5$; \ $\sigma^2=\frac{9+1+0+4+4}{5}=\frac{18}{5}=\res{3{,}6}$; \ $\sigma=\sqrt{3{,}6}\approx\res{1{,}90}$."),
 (2, T(r"Calcula la mitjana, la variància i la desviació típica del nombre de germans de 20 alumnes:", r"Calcula la media, la varianza y la desviación típica del número de hermanos de 20 alumnos:") + center(htab([x for x, _ in T63], [f for _, f in T63])),
     center(ftab([x for x, _ in T63], [f for _, f in T63], ('f', 'xf', 'x2f'))) + r"$\bar x=\frac{26}{20}=\res{1{,}3}$; \ $\sigma^2=\frac{58}{20}-1{,}3^2=2{,}9-1{,}69=\res{1{,}21}$; \ $\sigma=\sqrt{1{,}21}=\res{1{,}1}$."),
 (2, T(r"Dos jugadors de bàsquet han fet aquests punts en cinc partits. A: $6,\ 7,\ 7,\ 8,\ 7$; \ B: $10,\ 4,\ 9,\ 5,\ 7$. Calcula la mitjana i la desviació típica de cadascun. Qui és més regular?", r"Dos jugadores de baloncesto han hecho estos puntos en cinco partidos. A: $6,\ 7,\ 7,\ 8,\ 7$; \ B: $10,\ 4,\ 9,\ 5,\ 7$. Calcula la media y la desviación típica de cada uno. ¿Quién es más regular?"),
     T(r"Tots dos: $\bar x=7$. \ A: $\sigma^2=\frac{2}{5}=0{,}4$, \ $\sigma\approx\res{0{,}63}$. \ B: $\sigma^2=\frac{9+9+4+4+0}{5}=5{,}2$, \ $\sigma\approx\res{2{,}28}$. \ \rest{A és més regular}.", r"Los dos: $\bar x=7$. \ A: $\sigma^2=\frac{2}{5}=0{,}4$, \ $\sigma\approx\res{0{,}63}$. \ B: $\sigma^2=\frac{9+9+4+4+0}{5}=5{,}2$, \ $\sigma\approx\res{2{,}28}$. \ \rest{A es más regular}.")),
 (2, T(r"L'alçada d'un grup de persones té $\bar x=160$\,cm i $\sigma=8$\,cm. El pes d'un grup de gossos té $\bar x=40$\,kg i $\sigma=4$\,kg. Quin grup té més dispersió relativa?", r"La altura de un grupo de personas tiene $\bar x=160$\,cm y $\sigma=8$\,cm. El peso de un grupo de perros tiene $\bar x=40$\,kg y $\sigma=4$\,kg. ¿Qué grupo tiene más dispersión relativa?")
     + recorda(T(r"Per a comparar dispersions amb mitjanes o unitats diferents: $CV=\dfrac{\sigma}{\bar x}$ (en \%).", r"Para comparar dispersiones con medias o unidades diferentes: $CV=\dfrac{\sigma}{\bar x}$ (en \%).")),
     T(r"$CV_{\text{persones}}=\frac{8}{160}=\res{5\,\%}$; \ $CV_{\text{gossos}}=\frac{4}{40}=\res{10\,\%}$: \ \rest{els gossos} tenen més dispersió relativa.", r"$CV_{\text{personas}}=\frac{8}{160}=\res{5\,\%}$; \ $CV_{\text{perros}}=\frac{4}{40}=\res{10\,\%}$: \ \rest{los perros} tienen más dispersión relativa.")),
 (3, T(r"Calcula la desviació típica i el coeficient de variació de les alçades dels 50 alumnes (secció 3, exercici 16).", r"Calcula la desviación típica y el coeficiente de variación de las alturas de los 50 alumnos (sección 3, ejercicio 16)."),
     center(gtab(ALT, FAL, ('m', 'f', 'mf', 'm2f'))) + r"$\bar x=\frac{8\,215}{50}=164{,}3$; \ $\sigma^2=\frac{1\,351\,862{,}5}{50}-164{,}3^2=27\,037{,}25-26\,994{,}49=42{,}76$; \ $\sigma\approx\res{6{,}54\text{ cm}}$; \ $CV=\frac{6{,}54\ldots}{164{,}3}\approx\res{3{,}98\,\%}$."),
 (3, T(r"Les dades $2,\ 4,\ 5,\ 7,\ 7$ tenen $\bar x=5$ i $\sigma\approx1{,}90$. Sense tornar a fer tots els càlculs, troba la mitjana, la desviació típica i el coeficient de variació si:", r"Los datos $2,\ 4,\ 5,\ 7,\ 7$ tienen $\bar x=5$ y $\sigma\approx1{,}90$. Sin volver a hacer todos los cálculos, encuentra la media, la desviación típica y el coeficiente de variación si:")
     + tasks(2, [T(r"sumem 5 a totes les dades;", r"sumamos 5 a todos los datos;"), T(r"multipliquem totes les dades per 2.", r"multiplicamos todos los datos por 2.")]),
     tasks(1, [T(r"La mitjana puja 5 ($\res{10}$), però les dades estan igual d'escampades: $\sigma\approx\res{1{,}90}$. El $CV$ baixa de $38\,\%$ a $\frac{1{,}90}{10}\approx\res{19\,\%}$.", r"La media sube 5 ($\res{10}$), pero los datos están igual de esparcidos: $\sigma\approx\res{1{,}90}$. El $CV$ baja de $38\,\%$ a $\frac{1{,}90}{10}\approx\res{19\,\%}$."),
               T(r"Tot es duplica: $\bar x=\res{10}$ i $\sigma\approx\res{3{,}79}$. El $CV$ no canvia: $\res{38\,\%}$.", r"Todo se duplica: $\bar x=\res{10}$ y $\sigma\approx\res{3{,}79}$. El $CV$ no cambia: $\res{38\,\%}$.")])),
 (3, T(r"Dues màquines omplin botelles d'un litre. La A ompli de mitjana 1\,002\,ml amb $\sigma=3$\,ml i la B, 998\,ml amb $\sigma=8$\,ml. Quina màquina funciona millor? Raona-ho amb el coeficient de variació.", r"Dos máquinas llenan botellas de un litro. La A llena de media 1\,002\,ml con $\sigma=3$\,ml y la B, 998\,ml con $\sigma=8$\,ml. ¿Qué máquina funciona mejor? Razónalo con el coeficiente de variación."),
     T(r"Totes dues s'acosten a 1\,000\,ml de mitjana, però $CV_A=\frac{3}{1\,002}\approx\res{0{,}30\,\%}$ i $CV_B=\frac{8}{998}\approx\res{0{,}80\,\%}$: \rest{la A} és molt més regular (les botelles ixen més iguals).", r"Las dos se acercan a 1\,000\,ml de media, pero $CV_A=\frac{3}{1\,002}\approx\res{0{,}30\,\%}$ y $CV_B=\frac{8}{998}\approx\res{0{,}80\,\%}$: \rest{la A} es mucho más regular (las botellas salen más iguales).")),
]))
AP(2 * math.sqrt(var(D62)), '3.79'); EQ(S2A, fr('1351862.5')); EQ((SM / 50) ** 2, fr('26994.49'))

# =====================================================================
# 7. Paràmetres de posició: quartils i percentils
# =====================================================================
D71 = [4, 8, 15, 16, 23, 42, 7, 10, 12, 19, 30]; CHK(five(D71) == (4, 8, 15, 23, 42))
D72 = [21, 25, 18, 30, 27, 22, 19, 26, 24, 28, 20, 23]; CHK(five(D72)[1:4] == (Fr(41, 2), Fr(47, 2), Fr(53, 2)) and pctl(D72, 10) == 19 and pctl(D72, 90) == 28)
T73 = [(0, 3), (1, 8), (2, 10), (3, 6), (4, 2), (5, 1)]; D73 = expand(T73); CHK(acc([f for _, f in T73]) == [3, 11, 21, 27, 29, 30])
CHK(pctl(D73, 25) == 1 and pctl(D73, 50) == 2 and pctl(D73, 75) == 3 and pctl(D73, 10) == Fr(1, 2) and pctl(D73, 90) == Fr(7, 2))
EQ(Fr(21, 30) * 100, 70); EQ(Fr(20 * 250, 100), 50)
S_.append((T("Paràmetres de posició: quartils i percentils", "Parámetros de posición: cuartiles y percentiles"), [
 (1, T(r"Calcula els quartils i el rang interquartílic de: \ $%s$.", r"Calcula los cuartiles y el rango intercuartílico de: \ $%s$.") % lst(D71)
     + recorda(T(r"Ordena les dades i calcula la posició $\frac{k\cdot N}{100}$ ($Q_1$: $\frac N4$; $Q_3$: $\frac{3N}{4}$). Si no és entera, agafa la dada de la posició següent; si és entera, fes la mitjana d'eixa dada i la següent.", r"Ordena los datos y calcula la posición $\frac{k\cdot N}{100}$ ($Q_1$: $\frac N4$; $Q_3$: $\frac{3N}{4}$). Si no es entera, coge el dato de la posición siguiente; si es entera, haz la media de ese dato y el siguiente.")),
     T(r"Ordenades: $4,\ 7,\ 8,\ 10,\ 12,\ 15,\ 16,\ 19,\ 23,\ 30,\ 42$. \ $\frac{11}{4}=2{,}75\to$ 3a: $Q_1=\res{8}$; \ $5{,}5\to$ 6a: $Me=\res{15}$; \ $8{,}25\to$ 9a: $Q_3=\res{23}$; \ $RI=\res{15}$.",
       r"Ordenados: $4,\ 7,\ 8,\ 10,\ 12,\ 15,\ 16,\ 19,\ 23,\ 30,\ 42$. \ $\frac{11}{4}=2{,}75\to$ 3.\textsuperscript{o}: $Q_1=\res{8}$; \ $5{,}5\to$ 6.\textsuperscript{o}: $Me=\res{15}$; \ $8{,}25\to$ 9.\textsuperscript{o}: $Q_3=\res{23}$; \ $RI=\res{15}$.")),
 (1, T(r"Explica què vol dir cada frase:", r"Explica qué quiere decir cada frase:")
     + tasks(1, [T(r"Un nadó està en el percentil 70 de pes.", r"Un bebé está en el percentil 70 de peso."), T(r"La nota de Lluís és el primer quartil de la classe.", r"La nota de Lluís es el primer cuartil de la clase.")]),
     tasks(1, [T(r"Pesa \rest{més que el $70\,\%$} dels nadons de la seua edat (i menys que el $30\,\%$).", r"Pesa \rest{más que el $70\,\%$} de los bebés de su edad (y menos que el $30\,\%$)."),
               T(r"Un \rest{$25\,\%$} de la classe té una nota igual o menor i un $75\,\%$, igual o major.", r"Un \rest{$25\,\%$} de la clase tiene una nota igual o menor y un $75\,\%$, igual o mayor.")])),
 (2, T(r"Les edats dels 12 membres d'un club són: \ $%s$. \ Calcula els quartils i els percentils 10 i 90.", r"Las edades de los 12 miembros de un club son: \ $%s$. \ Calcula los cuartiles y los percentiles 10 y 90.") % lst(D72),
     T(r"Ordenades: $18,\ 19,\ 20,\ 21,\ 22,\ 23,\ 24,\ 25,\ 26,\ 27,\ 28,\ 30$. \ $Q_1$: posició 3 (entera) $\to\frac{20+21}{2}=\res{20{,}5}$; \ $Me=\frac{23+24}{2}=\res{23{,}5}$; \ $Q_3$: posició 9 $\to\frac{26+27}{2}=\res{26{,}5}$; \ $P_{10}$: $1{,}2\to$ 2a: $\res{19}$; \ $P_{90}$: $10{,}8\to$ 11a: $\res{28}$.",
       r"Ordenados: $18,\ 19,\ 20,\ 21,\ 22,\ 23,\ 24,\ 25,\ 26,\ 27,\ 28,\ 30$. \ $Q_1$: posición 3 (entera) $\to\frac{20+21}{2}=\res{20{,}5}$; \ $Me=\frac{23+24}{2}=\res{23{,}5}$; \ $Q_3$: posición 9 $\to\frac{26+27}{2}=\res{26{,}5}$; \ $P_{10}$: $1{,}2\to$ 2.\textsuperscript{o}: $\res{19}$; \ $P_{90}$: $10{,}8\to$ 11.\textsuperscript{o}: $\res{28}$.")),
 (2, T(r"La taula recull els gols marcats per un equip en 30 partits. Calcula els quartils i els percentils 10 i 90.", r"La tabla recoge los goles marcados por un equipo en 30 partidos. Calcula los cuartiles y los percentiles 10 y 90.") + center(htab([x for x, _ in T73], [f for _, f in T73]))
     + recorda(T(r"En una taula, busca el primer valor amb $F_i\geq\frac{k\cdot N}{100}$. Si una $F_i$ coincideix exactament, fes la mitjana d'eixe valor i el següent.", r"En una tabla, busca el primer valor con $F_i\geq\frac{k\cdot N}{100}$. Si una $F_i$ coincide exactamente, haz la media de ese valor y el siguiente.")),
     center(ftab([x for x, _ in T73], [f for _, f in T73], ('f', 'F'))) + r"$Q_1$: $7{,}5\to F=11$: $\res{1}$; \ $Me$: $15\to F=21$: $\res{2}$; \ $Q_3$: $22{,}5\to F=27$: $\res{3}$; \ $P_{10}$: $3=F_1$ \ $\to\frac{0+1}{2}=\res{0{,}5}$; \ $P_{90}$: $27=F_4$ \ $\to\frac{3+4}{2}=\res{3{,}5}$."),
 (2, T(r"Amb la taula de l'exercici anterior, a quin percentil correspon, aproximadament, marcar 2 gols? Quants gols cal marcar per a estar en el quartil 3 o per damunt?", r"Con la tabla del ejercicio anterior, ¿a qué percentil corresponde, aproximadamente, marcar 2 goles? ¿Cuántos goles hay que marcar para estar en el cuartil 3 o por encima?"),
     T(r"Fins al 2 hi ha $F=21$ de 30: $\frac{21}{30}=0{,}7\to$ \rest{percentil 70}. \ $Q_3=3$: cal marcar \rest{3 gols o més}.", r"Hasta el 2 hay $F=21$ de 30: $\frac{21}{30}=0{,}7\to$ \rest{percentil 70}. \ $Q_3=3$: hay que marcar \rest{3 goles o más}.")),
 (3, T(r"En quin interval estan el primer quartil, el tercer quartil i el percentil 90 de les alçades dels 50 alumnes de la secció 3 (exercici 16)?", r"¿En qué intervalo están el primer cuartil, el tercer cuartil y el percentil 90 de las alturas de los 50 alumnos de la sección 3 (ejercicio 16)?"),
     r"$F_i$: 4, 13, 28, 40, 47, 50. \ $Q_1$: $12{,}5\to F=13$: $\res{[155,\ 160)}$; \ $Q_3$: $37{,}5\to F=40$: $\res{[165,\ 170)}$; \ $P_{90}$: $45\to F=47$: $\res{[170,\ 175)}$."),
 (3, T(r"En unes oposicions amb 250 aspirants, només aproven els que tenen una nota igual o superior al percentil 80. Quants aspirants aproven, aproximadament? Si Marta ha tret una nota que és el percentil 75, aprova?", r"En unas oposiciones con 250 aspirantes, solo aprueban quienes tienen una nota igual o superior al percentil 80. ¿Cuántos aspirantes aprueban, aproximadamente? Si Marta ha sacado una nota que es el percentil 75, ¿aprueba?"),
     T(r"Per damunt del $P_{80}$ queda el $20\,\%$: $0{,}2\cdot250=\res{50}$ aspirants. \ Marta \rest{no aprova}: la seua nota està per davall del $P_{80}$.", r"Por encima del $P_{80}$ queda el $20\,\%$: $0{,}2\cdot250=\res{50}$ aspirantes. \ Marta \rest{no aprueba}: su nota está por debajo del $P_{80}$.")),
]))
EQ(Fr(50 * 25, 100), '12.5'); EQ(Fr(50 * 75, 100), '37.5'); EQ(Fr(50 * 90, 100), 45)

# =====================================================================
# 8. Diagrama de caixes
# =====================================================================
RD8 = (20, 35, 45, 50, 70); EQ(70 - 20, 50); EQ(50 - 35, 15); EQ(Fr(80, 4), 20); EQ(Fr(80 * 3, 4), 60)
CA8 = (3, 5, 6, 7, 9); CB8 = (1, 4, 6, 8, 10)
O8 = [3, 21, 22, 24, 25, 26, 27, 28, 30]; CHK(five(O8) == (3, 22, 25, 27, 30)); EQ(22 - Fr(3, 2) * 5, '14.5'); EQ(27 + Fr(3, 2) * 5, '34.5')
K8 = [1, 2, 4, 4, 6, 7, 9, 12]; CHK(five(K8) == (1, 3, 5, 8, 12))
F73 = (0, 1, 2, 3, 5)
S_.append((T("Diagrama de caixes", "Diagrama de cajas"), [
 (1, T(r"Dibuixa el diagrama de caixes de les dades de l'exercici 41 (secció 7).", r"Dibuja el diagrama de cajas de los datos del ejercicio 41 (sección 7).")
     + recorda(T(r"Cinc nombres: mínim, $Q_1$, $Me$, $Q_3$ i màxim. La \textbf{caixa} va de $Q_1$ a $Q_3$ amb una línia en la mediana; els \textbf{bigotis} arriben al mínim i al màxim.", r"Cinco números: mínimo, $Q_1$, $Me$, $Q_3$ y máximo. La \textbf{caja} va de $Q_1$ a $Q_3$ con una línea en la mediana; los \textbf{bigotes} llegan al mínimo y al máximo.")),
     T(r"Mínim 4, $Q_1=8$, $Me=15$, $Q_3=23$, màxim 42:", r"Mínimo 4, $Q_1=8$, $Me=15$, $Q_3=23$, máximo 42:") + center(tbox([('', five(D71))], 0, 45, 5))),
 (1, T(r"Aquest diagrama de caixes representa les edats de 80 persones que han anat a un concert. Troba el rang i el rang interquartílic. Quantes persones tenen més de 50 anys? I entre 35 i 70 anys?", r"Este diagrama de cajas representa las edades de 80 personas que han ido a un concierto. Encuentra el rango y el rango intercuartílico. ¿Cuántas personas tienen más de 50 años? ¿Y entre 35 y 70 años?")
     + center(tbox([('', RD8)], 15, 75, 5, lab=T('anys', 'años'))),
     T(r"Rang $=70-20=\res{50}$; \ $RI=50-35=\res{15}$. \ Més de 50 ($Q_3$): el $25\,\%$, $\res{20}$ persones. \ Entre 35 i 70: el $75\,\%$, $\res{60}$ persones.", r"Rango $=70-20=\res{50}$; \ $RI=50-35=\res{15}$. \ Más de 50 ($Q_3$): el $25\,\%$, $\res{20}$ personas. \ Entre 35 y 70: el $75\,\%$, $\res{60}$ personas.")),
 (2, T(r"Les notes d'un examen de dues classes es resumeixen en aquests diagrames de caixes. Respon i raona:", r"Las notas de un examen de dos clases se resumen en estos diagramas de cajas. Responde y razona:")
     + center(tbox([('A', CA8), ('B', CB8)], 0, 10, 1, lab=T('nota', 'nota')))
     + tasks(1, [T(r"Quina classe té la mediana més alta?", r"¿Qué clase tiene la mediana más alta?"), T(r"Quina classe té les notes més homogènies?", r"¿Qué clase tiene las notas más homogéneas?"),
                 T(r"En quina classe ha aprovat (5 o més) un percentatge més gran d'alumnes?", r"¿En qué clase ha aprobado (5 o más) un porcentaje mayor de alumnos?")]),
     tasks(1, [T(r"\rest{Cap}: totes dues tenen $Me=6$.", r"\rest{Ninguna}: las dos tienen $Me=6$."), T(r"\rest{A}: la caixa és més curta ($RI_A=2$, $RI_B=4$) i el rang també ($6$ contra $9$).", r"\rest{A}: la caja es más corta ($RI_A=2$, $RI_B=4$) y el rango también ($6$ contra $9$)."),
               T(r"\rest{A}: en A, $Q_1=5$, i aprova almenys el $75\,\%$; en B, $Q_1=4$, i aprova menys del $75\,\%$.", r"\rest{A}: en A, $Q_1=5$, y aprueba al menos el $75\,\%$; en B, $Q_1=4$, y aprueba menos del $75\,\%$.")])),
 (2, T(r"Dibuixa el diagrama de caixes dels gols de l'exercici 44 (secció 7). Què indica que la mitja caixa de la dreta i la de l'esquerra siguen iguals?", r"Dibuja el diagrama de cajas de los goles del ejercicio 44 (sección 7). ¿Qué indica que la media caja de la derecha y la de la izquierda sean iguales?"),
     T(r"Mínim 0, $Q_1=1$, $Me=2$, $Q_3=3$, màxim 5:", r"Mínimo 0, $Q_1=1$, $Me=2$, $Q_3=3$, máximo 5:") + center(tbox([('', F73)], 0, 6, 1))
     + T(r"El $50\,\%$ central és \rest{simètric} respecte de la mediana; el bigoti dret, més llarg, indica que hi ha pocs partits amb molts gols.", r"El $50\,\%$ central es \rest{simétrico} respecto de la mediana; el bigote derecho, más largo, indica que hay pocos partidos con muchos goles.")),
 (2, T(r"D'unes dades sabem que el mínim és 12, $Q_1=18$, $Me=21$, $Q_3=30$ i el màxim, 34. Quin percentatge de les dades és:", r"De unos datos sabemos que el mínimo es 12, $Q_1=18$, $Me=21$, $Q_3=30$ y el máximo, 34. ¿Qué porcentaje de los datos es:")
     + tasks(4, [T(r"menor que 21?", r"menor que 21?"), T(r"entre 18 i 30?", r"entre 18 y 30?"), T(r"major que 18?", r"mayor que 18?"), T(r"entre 30 i 34?", r"entre 30 y 34?")]),
     tasks(4, [r'$\res{50\,\%}$', r'$\res{50\,\%}$', r'$\res{75\,\%}$', r'$\res{25\,\%}$'])),
 (3, T(r"Comprova si hi ha valors atípics en les dades $%s$. Dibuixa'n el diagrama de caixes i calcula'n la mitjana i la mediana. Quin paràmetre representa millor les dades?", r"Comprueba si hay valores atípicos en los datos $%s$. Dibuja su diagrama de cajas y calcula su media y su mediana. ¿Qué parámetro representa mejor los datos?") % lst(O8)
     + recorda(T(r"Una dada és \textbf{atípica} si és menor que $Q_1-1{,}5\cdot RI$ o major que $Q_3+1{,}5\cdot RI$.", r"Un dato es \textbf{atípico} si es menor que $Q_1-1{,}5\cdot RI$ o mayor que $Q_3+1{,}5\cdot RI$.")),
     T(r"$Q_1=22$, $Me=25$, $Q_3=27$, $RI=5$. Límits: $22-7{,}5=14{,}5$ i $27+7{,}5=34{,}5$: el \rest{3 és atípic}. \ $\bar x=\frac{206}{9}\approx\res{22{,}89}$; \ $Me=\res{25}$: la \rest{mediana} representa millor les dades (el 3 estira la mitjana cap avall).",
       r"$Q_1=22$, $Me=25$, $Q_3=27$, $RI=5$. Límites: $22-7{,}5=14{,}5$ y $27+7{,}5=34{,}5$: el \rest{3 es atípico}. \ $\bar x=\frac{206}{9}\approx\res{22{,}89}$; \ $Me=\res{25}$: la \rest{mediana} representa mejor los datos (el 3 estira la media hacia abajo).")
     + center(tbox([('', five(O8))], 0, 32, 2))),
 (3, T(r"Inventa vuit dades que tinguen aquest resum: mínim 1, $Q_1=3$, $Me=5$, $Q_3=8$, màxim 12.", r"Inventa ocho datos que tengan este resumen: mínimo 1, $Q_1=3$, $Me=5$, $Q_3=8$, máximo 12."),
     T(r"Amb $N=8$: $Q_1=\frac{x_2+x_3}{2}$, $Me=\frac{x_4+x_5}{2}$, $Q_3=\frac{x_6+x_7}{2}$. Per exemple: $\res{1,\ 2,\ 4,\ 4,\ 6,\ 7,\ 9,\ 12}$ (hi ha moltes altres solucions).", r"Con $N=8$: $Q_1=\frac{x_2+x_3}{2}$, $Me=\frac{x_4+x_5}{2}$, $Q_3=\frac{x_6+x_7}{2}$. Por ejemplo: $\res{1,\ 2,\ 4,\ 4,\ 6,\ 7,\ 9,\ 12}$ (hay muchas otras soluciones).")),
]))
EQ(sum(O8), 206); AP(mean(O8), '22.89')
# referències creuades entre exercicis (numeració global)
NUM = {}; n = 0
for _t, _e in S_:
    for _ in _e: n += 1
assert n == 54, n
starts = [1]
for _t, _e in S_[:-1]: starts.append(starts[-1] + len(_e))
assert starts == [1, 6, 13, 18, 25, 33, 41, 48], starts  # referències: exercici 6 (llibres), 16 (alçades, 4t de la secció 3), 41 i 44 (secció 7)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("estadística, població, mostra, mostreig, variables, taules de freqüències, dades agrupades, gràfics estadístics, moda, mitjana, mediana, rang, desviació mitjana, variància, desviació típica, coeficient de variació, quartils, percentils, diagrama de caixes",
       'estadística, población, muestra, muestreo, variables, tablas de frecuencias, datos agrupados, gráficos estadísticos, moda, media, mediana, rango, desviación media, varianza, desviación típica, coeficiente de variación, cuartiles, percentiles, diagrama de cajas')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques A 4t ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\definecolor{violet}{HTML}{7C6CF0}
\definecolor{gold}{HTML}{E0A21B}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T("Estadística Unidimensional", 'Estadística Unidimensional')
NU = 9

def build(sol_):
    if ES:
        sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad %d: %s' % (t, NU, TIT), capcalera='%s · Unidad %d: %s' % (t, NU, TIT), pdfkeywords=KW, curs='4eso-a')
        cap = assignatura('4eso-a') + '{' + ('Soluciones de la ficha · Unidad %d' % NU if sol_ else 'Ficha de ejercicios · Unidad %d' % NU) + '}{' + TIT + '}'
    else:
        t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat %d: %s. 4t d'ESO Matemàtiques A}" % (t, NU, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat %d: %s · 4t ESO A" % (t, NU, TIT))
        assert "4t d'ESO Matemàtiques A" in p and 'Unitat %d' % NU in p and 'unitat %d' % NU in p
        cap = r'\capcalera{Matemàtiques A}{4t ESO}{' + ('Solucions de la fitxa · Unitat %d' % NU if sol_ else "Fitxa d'exercicis · Unitat %d" % NU) + '}{' + TIT + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol_ else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{14}\n\\input{../comu/fentmates.tex}\n\\fmcurs{4eso-a}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol_:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs eines per a fer taules de freqüències i agrupar dades, construir gràfics, calcular la variància i la desviació típica pas a pas, els quartils i els percentils i dibuixar diagrames de caixes. Els resultats aproximats estan arrodonits a les centèsimes (els percentatges, a les dècimes).",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás herramientas para hacer tablas de frecuencias y agrupar datos, construir gráficos, calcular la varianza y la desviación típica paso a paso, los cuartiles y los percentiles y dibujar diagramas de cajas. Los resultados aproximados están redondeados a las centésimas (los porcentajes, a las décimas).") if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Pots fer servir la calculadora en mode estadístic per a comprovar els resultats. Les seccions segueixen l'ordre dels apunts de la unitat (9.1--9.8).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Puedes usar la calculadora en modo estadístico para comprobar los resultados. Las secciones siguen el orden de los apuntes de la unidad (9.1--9.8)."))
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
print(n, T('exercicis', 'ejercicios'), '·', NCHK[0], T('comprovacions', 'comprobaciones'))
