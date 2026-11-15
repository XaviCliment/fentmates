# Versió en castellà de genera.py. Genera t10-fitxa-exercicis-es.tex i t10-fitxa-solucions-es.tex
# (1r ESO, Unitat 10: Estadística — població, mostra i variables, freqüències i taules de freqüències,
# gràfics estadístics, moda, mitjana i mediana, rang i desviació mitjana)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les comprovacions CHK (amb fraccions exactes) verifiquen cada resultat escrit.
import os, re, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

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
V11 = [('número de hijos', 'discreta'), ('color preferido', 'cualitativa'), ('tiempo en correr 100\\,m', 'continua'), ("páginas de un libro", 'discreta'),
       ('profesión', 'cualitativa'), ("temperatura de una ciudad", 'continua'), ('número de calzado', 'discreta'), ('lengua materna', 'cualitativa'), ("capacidad de una botella", 'continua')]
S_.append(("Población, muestra y variables estadísticas", [
 (1, r"Clasifica estas variables en cualitativas, cuantitativas discretas o cuantitativas continuas:" + tasks(3, [v for v, _ in V11])
     + recorda(r"Si los valores no son números, la variable es \textbf{cualitativa}. Si son números: se \textbf{cuentan} $\to$ \textbf{discreta}; se \textbf{miden} $\to$ \textbf{continua}."),
     tasks(3, [r'\rest{%s}' % t for _, t in V11])),
 (1, r"Para conocer cuántas horas de televisión ven a la semana los 450 alumnos de un instituto, se encuesta a 60 elegidos al azar. Indica la población, la muestra, el tamaño de la muestra, un individuo y la variable estudiada (y de qué tipo es).",
     r"Población: \rest{los 450 alumnos del instituto}. Muestra: \rest{los 60 alumnos encuestados}; tamaño \rest{60}. Individuo: \rest{cada alumno}. Variable: \rest{horas de televisión semanales}, cuantitativa \rest{continua}."),
 (1, r"En cada caso, di si se estudia toda la población o una muestra:" + tasks(1, [r"La tutora calcula la nota media de su clase con las notas de todos los alumnos.",
                                                                                     r"Para saber cuánto duran las pilas de una fábrica, se prueban 50.",
                                                                                     r"Una empresa pregunta a 2\,000 personas a quién votarán en las elecciones.",
                                                                                     r"El entrenador mide la altura de todos los jugadores de su equipo."]),
     tasks(4, [r'\rest{Población}', r'\rest{Muestra}', r'\rest{Muestra}', r'\rest{Población}'])),
 (2, r"Explica por qué, en estos estudios, hay que trabajar con una muestra y no con toda la población:" + tasks(1, [r"la calidad de los yogures que hace una fábrica;", r"la opinión de todos los jóvenes de España sobre las redes sociales;", r"el tiempo que tardan en fundirse las bombillas de un lote de 10\,000."]),
     tasks(1, [r"Para probar un yogur hay que abrirlo: si los probáramos todos, \rest{no quedaría ninguno} para vender.", r"Son \rest{demasiadas personas}: costaría mucho dinero y mucho tiempo.", r"La prueba \rest{destruye} las bombillas, y además es lenta y cara."])),
 (2, r"Razona si estas muestras son representativas:" + tasks(1, [r"Para saber cuántas horas de deporte hacen los alumnos de un instituto, se pregunta a 30 personas que salen del gimnasio.",
                                                                    r"Para saber el plato preferido de los alumnos de un instituto, se eligen al azar 10 alumnos de cada curso.",
                                                                    r"Para saber qué música gusta más a la gente del pueblo, Laura pregunta a sus amigos."]),
     tasks(1, [r"\rest{No}: los que salen del gimnasio seguramente hacen más deporte que el resto.", r"\rest{Sí}: hay alumnos de todos los cursos elegidos al azar.", r"\rest{No}: los amigos de Laura tienen gustos parecidos y son de la misma edad."])),
 (2, r"Escribe tres valores posibles de cada variable y clasifícala:" + tasks(3, [r"peso de un perro", r"nacionalidad", r"número de primos"]),
     tasks(3, [r"12,5\,kg; 30\,kg; 7,2\,kg: \rest{continua}", r"italiana, china, rusa:\par\rest{cualitativa}", r"0, 3, 8: \rest{discreta}"])),
 (3, r"Quieres saber cuánto tiempo dedican a leer cada semana los 600 alumnos de tu instituto. Describe cómo harías el estudio: cuál es la población, cómo elegirías una muestra representativa de 60 alumnos, qué pregunta harías y de qué tipo sería la variable.",
     r"Respuesta abierta. Por ejemplo:\par Población, \rest{los 600 alumnos}; muestra, \rest{6 alumnos por grupo}, elegidos al azar en cada uno de los 10 grupos (así hay alumnos de todos los cursos); pregunta: «¿Cuántas horas lees a la semana?»; variable cuantitativa \rest{continua}."),
]))

# =====================================================================
# 2. Freqüències absolutes i relatives
# =====================================================================
MAS = [0, 1, 2, 1, 0, 3, 1, 1, 2, 0, 1, 4, 2, 1, 0, 1, 2, 1, 3, 1]
TM = freqs(MAS); CHK(TM == [(0, 4), (1, 9), (2, 4), (3, 2), (4, 1)] and len(MAS) == 20)
SANG = ['A', 'O', 'O', 'A', 'B', 'O', 'A', 'AB', 'O', 'O', 'A', 'B', 'O', 'A', 'O', 'O', 'A', 'B', 'O', 'A', 'AB', 'O', 'A', 'O', 'A']
TS = freqs(SANG, ['A', 'O', 'B', 'AB']); CHK(TS == [('A', 9), ('O', 11), ('B', 3), ('AB', 2)] and len(SANG) == 25)
C24 = [('Fútbol', 14, None, None), ('Baloncesto', None, '0{,}25', None), ('Tenis', None, None, 15), ('Natación', 8, None, None), ('Otros', None, None, None)]
# N = 40: futbol 14, bàsquet 10, tenis 6, natació 8, altres 2
C24s = [14, 10, 6, 8, 2]; CHK(sum(C24s) == 40 and Fr(10, 40) == Fr(1, 4) and Fr(6, 40) * 100 == 15)
D25 = [9, 11, 10, 8, 12]; CHK(60 - sum(D25) == 10 and Fr(11 + 8 + 10, 60) * 100 == Fr(145, 3))
S_.append(("Frecuencias absolutas y relativas", [
 (1, r"@@MAS@@Estas son las mascotas que tienen 20 alumnos: \ $%s$. \ Haz el recuento y la tabla con las frecuencias absolutas, relativas y los porcentajes." % lst(MAS)
     + recorda(r"Frecuencia absoluta $f_i$: veces que aparece un valor. Frecuencia relativa: $h_i=\dfrac{f_i}{N}$. Porcentaje: $h_i\cdot100$."),
     center(ftab([x for x, _ in TM], [f for _, f in TM], ('f', 'h', 'p')))),
 (1, r"@@SANG@@Estos son los grupos sanguíneos de 25 personas: \ %s. \ Haz la tabla de frecuencias absolutas, relativas y porcentajes." % ', '.join(SANG),
     center(ftab([x for x, _ in TS], [f for _, f in TS], ('f', 'h', 'p'), xl='Grupo'))),
 (1, r"Escribe como porcentaje:" + tasks(4, [r'$0{,}3$', r'$0{,}05$', r'$\frac{3}{4}$', r'$\frac{7}{20}$']) + r"\par Y como frecuencia relativa decimal:" + tasks(4, [r'$12\,\%$', r'$60\,\%$', r'$7{,}5\,\%$', r'$100\,\%$']),
     tasks(4, [r'$\res{30\,\%}$', r'$\res{5\,\%}$', r'$\res{75\,\%}$', r'$\res{35\,\%}$']) + tasks(4, [r'$\res{0{,}12}$', r'$\res{0{,}6}$', r'$\res{0{,}075}$', r'$\res{1}$'])),
 (2, r"Completa la tabla del deporte preferido de 40 alumnos:" + center(r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|C{1.2cm}|C{1.2cm}|C{1.2cm}|}\hline Deporte & $f_i$ & $h_i$ & \%\\\hline Fútbol & 14 & & \\\hline Baloncesto & & $0{,}25$ & \\\hline Tenis & & & 15\\\hline Natación & 8 & & \\\hline Otros & & & \\\hline \textbf{Total} & 40 & & \\\hline\end{tabular}}'),
     center(ftab(['Fútbol', 'Baloncesto', 'Tenis', 'Natación', 'Otros'], C24s, ('f', 'h', 'p'), xl='Deporte')) + r"Baloncesto: $0{,}25\cdot40=10$; tenis: $0{,}15\cdot40=6$; otros: $40-(14+10+6+8)=\res{2}$."),
 (2, r"Hemos lanzado un dado 60 veces. Ha salido el 1 nueve veces, el 2 once, el 3 diez, el 4 ocho, el 5 doce y el 6 el resto. ¿Cuántas veces ha salido el 6? ¿En qué porcentaje de los lanzamientos ha salido un número par? ¿Y un número mayor que 4?",
     r"$f_6=60-50=\res{10}$. \ Pares: $11+8+10=29$; \ $\frac{29}{60}\approx\res{48{,}3\,\%}$. \ Mayor que 4: $12+10=22$; \ $\frac{22}{60}\approx\res{36{,}7\,\%}$."),
 (2, r"En un instituto de 120 alumnos, el $35\,\%$ va a pie. ¿Cuántos alumnos son? Si 18 alumnos van en bici, ¿cuál es la frecuencia relativa de este valor?",
     r"$0{,}35\cdot120=\res{42}$ alumnos. \ $h=\frac{18}{120}=\res{0{,}15}$ (el $15\,\%$)."),
 (3, r"En una clase, la frecuencia relativa de los alumnos que llevan gafas es $0{,}2$, y son 6. ¿Cuántos alumnos hay en la clase? ¿Cuántos no llevan gafas?",
     r"$0{,}2\cdot N=6\Rightarrow N=6:0{,}2=\res{30}$ alumnos. \ No llevan: $30-6=\res{24}$."),
 (3, r"Una variable toma tres valores, $A$, $B$ y $C$. La frecuencia relativa de $A$ es $0{,}25$; la de $B$, $0{,}4$, y la frecuencia absoluta de $B$ es 16. Calcula $N$, la frecuencia relativa de $C$ y todas las frecuencias absolutas.",
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
S_.append(("Tablas de frecuencias", [
 (1, r"@@NOT@@Estas son las notas de un examen de 30 alumnos: \ $%s$. \ Haz la tabla de frecuencias con $f_i$, $F_i$, $h_i$ y porcentajes." % lst(NOT)
     + recorda(r"La frecuencia absoluta acumulada $F_i$ es el número de datos menores o iguales que $x_i$: se suman las $f_i$ hasta esa fila. La última es $N$."),
     center(ftab(XN, FN, ('f', 'F', 'h', 'p')))),
 (1, r"Con la tabla del ejercicio anterior, responde:" + tasks(2, [r"¿Cuántos alumnos han sacado un 6 o menos?", r"¿Cuántos han aprobado (5 o más)?", r"¿Cuántos han sacado más de un 7?", r"¿Qué porcentaje ha sacado un 9 o más?"]),
     tasks(2, [r"$F=\res{19}$", r"$30-6=\res{24}$", r"$30-24=\res{6}$", r"$\frac{3}{30}=\res{10\,\%}$"])),
 (2, r"En esta tabla, $x_i$ es el número de libros leídos en un mes y $F_i$, la frecuencia acumulada. Halla las frecuencias absolutas. ¿Cuántos alumnos han leído exactamente 3 libros? ¿Y al menos 2?" + center(htab(list(range(6)), F34, fl='$F_i$')),
     r"Restamos a cada $F_i$ la anterior:" + center(htab(list(range(6)), [F34[0]] + [F34[i] - F34[i - 1] for i in range(1, 6)])) + r"Exactamente 3: $f=\res{6}$. \ Al menos 2: $20-5=\res{15}$."),
 (2, r"@@PES@@Estos son los pesos (en kg) de 24 alumnos: \ $%s$. \ Agrúpalos en intervalos de amplitud 5 desde 35\,kg y haz la tabla con las marcas de clase, $f_i$, $F_i$ y porcentajes." % lst(PES)
     + recorda(r"El intervalo $[40,\ 45)$ contiene los datos mayores o iguales que 40 y menores que 45. La marca de clase es el punto medio: $\frac{40+45}{2}=42{,}5$."),
     center(r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|c|c|c|c|}\hline Peso (kg) & Marca & $f_i$ & $F_i$ & \%\\\hline '
            + r'\\\hline '.join('%s & $%s$ & $%d$ & $%d$ & $%s$' % (ivl(EP[i], EP[i + 1]), tn(Fr(EP[i] + EP[i + 1], 2)), f, F, tn(Fr(100 * f, 24)) if Fr(100 * f, 24).denominator in (1, 2) else tr(Fr(100 * f, 24), 1)) for i, (f, F) in enumerate(zip(FP, acc(FP))))
            + r'\\\hline \textbf{Total} & & $24$ & & $100$\\\hline\end{tabular}}')),
 (2, r"¿En qué intervalo del ejercicio anterior pondrías cada uno de estos datos?" + tasks(4, [r'$45$\,kg', r'$44{,}9$\,kg', r'$55$\,kg', r'$35$\,kg']),
     tasks(4, [r'\rest{$[45,\ 50)$}', r'\rest{$[40,\ 45)$}', r'\rest{$[55,\ 60)$}', r'\rest{$[35,\ 40)$}'])),
 (3, r"Estos son los tiempos (en segundos) de 20 alumnos en una carrera de 100\,m: \ $%s$. \ Agrúpalos en intervalos de 1 segundo desde 12\,s y haz la tabla con $f_i$ y $F_i$. ¿Qué porcentaje ha tardado menos de 14\,s? ¿Cuántos han tardado 15\,s o más?" % lst(CUR),
     center(r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|c|c|c|}\hline Tiempo (s) & Marca & $f_i$ & $F_i$\\\hline '
            + r'\\\hline '.join('%s & $%s$ & $%d$ & $%d$' % (ivl(EC[i], EC[i + 1]), tn(Fr(2 * EC[i] + 1, 2)), f, F) for i, (f, F) in enumerate(zip(FC, acc(FC))))
            + r'\\\hline\end{tabular}}') + r"Menos de 14\,s: $F=7$, \ $\frac{7}{20}=\res{35\,\%}$. \ 15\,s o más: $5+2=\res{7}$ alumnos."),
 (3, r"En una tabla de frecuencias, $F_3=12$, $F_4=19$ y $F_5=25$, y 5 es el valor más grande. ¿Cuántos datos hay? ¿Cuál es la frecuencia absoluta del 4? ¿Qué porcentaje de los datos es mayor que 3?",
     r"$N=F_5=\res{25}$. \ $f_4=F_4-F_3=19-12=\res{7}$. \ Mayores que 3: $25-12=13$, \ $\frac{13}{25}=\res{52\,\%}$."),
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
S_.append(("Diagramas de barras, polígonos e histogramas", [
 (1, r"Dibuja el diagrama de barras de los grupos sanguíneos del ejercicio @SANG@ (A: 9, O: 11, B: 3, AB: 2)."
     + recorda(r"En un \textbf{diagrama de barras} ponemos los valores en el eje horizontal y, encima de cada uno, una barra de altura igual a su frecuencia. Las barras van separadas."),
     center(tbar(['A', 'O', 'B', 'AB'], [9, 11, 3, 2], yl='Personas', xl='Grupo', multi=True))),
 (1, r"Este diagrama muestra cuántos viajes en avión han hecho los alumnos de una clase. Haz la tabla de frecuencias. ¿Cuántos alumnos hay? ¿Cuál es la moda? ¿Cuántos han viajado en avión alguna vez?" + center(tbar([x for x, _ in VIA], [f for _, f in VIA], yl='Alumnos', xl='Viajes')),
     center(htab([int(x) for x, _ in VIA], [f for _, f in VIA])) + r"$N=\res{24}$ alumnos. \ $Mo=\res{1}$ viaje. \ Alguna vez: $24-3=\res{21}$."),
 (1, r"Dibuja el diagrama de barras y el polígono de frecuencias del número de mascotas del ejercicio @MAS@.",
     center(tbar([str(x) for x, _ in TM], [f for _, f in TM], kind='both', yl='Alumnos', xl='Mascotas'))),
 (2, r"Dibuja el histograma y el polígono de frecuencias de los pesos agrupados en intervalos del ejercicio @PES@."
     + recorda(r"En un \textbf{histograma} las barras ocupan todo el intervalo y van juntas. El polígono une los puntos de arriba sobre las marcas de clase y se cierra en el eje."),
     center(thist(EP, FP, poly=True, yl='Alumnos', xl='kg'))),
 (2, r"¿Qué gráfico elegirías para representar cada variable?" + tasks(1, [r"el número de hermanos de 30 alumnos;", r"la altura de 200 personas;", r"el medio de transporte preferido para ir de vacaciones;", r"los minutos que tardan 50 alumnos en hacer los deberes."]),
     tasks(1, [r"\rest{diagrama de barras} (discreta)", r"\rest{histograma} (continua, en intervalos)", r"\rest{diagrama de barras} o \rest{de sectores} (cualitativa)", r"\rest{histograma} (continua, en intervalos)"])),
 (2, r"Las notas de un examen de dos clases de 30 alumnos están en la tabla. Dibuja los dos polígonos de frecuencias en el mismo gráfico. ¿Qué clase ha sacado mejores notas?" + center(r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|' + 'c|' * 7 + r'}\hline Nota & ' + ' & '.join(str(x) for x in range(4, 11)) + r'\\\hline Clase A & ' + ' & '.join(map(str, M4A)) + r'\\\hline Clase B & ' + ' & '.join(map(str, M4B)) + r'\\\hline\end{tabular}}'),
     center(tbar([str(x) for x in range(4, 11)], M4A, kind='poly', yl='Alumnos', xl='Nota', series=[(M4B, 'accent')])) + r"El polígono de B (naranja) está desplazado hacia la derecha: la clase \rest{B} ha sacado mejores notas."),
 (3, r"Tres candidatos de unas elecciones han obtenido 96, 92 y 98 votos. Un cartel los representa con un diagrama de barras en el que el eje vertical empieza en 90. ¿Por qué es engañoso? Dibújalo bien.",
     r"Si el eje empieza en 90, la barra de C (8 unidades de altura) parece \rest{cuatro veces} la de B (2 unidades), pero en realidad C solo tiene 6 votos más ($98-92$). Hay que empezar el eje en \rest{0}:" + center(tbar(['A', 'B', 'C'], [96, 92, 98], yl='Votos', step=20, multi=True, H=2.4))),
]))

# =====================================================================
# 5. Diagrames de sectors i pictogrames
# =====================================================================
E51 = [('Fútbol', 15), ('Baloncesto', 9), ('Tenis', 6), ('Natación', 4), ('Otros', 2)]
A51 = [Fr(360 * f, 36) for _, f in E51]; CHK(A51 == [150, 90, 60, 40, 20] and sum(A51) == 360)
A52 = [Fr(360 * f, 25) for _, f in TS]; CHK(sum(A52) == 360 and A52 == [Fr(648, 5), Fr(792, 5), Fr(216, 5), Fr(144, 5)])
P53 = [('Móvil', 40), ('Consola', 25), ('Ordenador', 20), ('Tableta', 15)]; F53 = [Fr(p * 200, 100) for _, p in P53]; CHK(F53 == [80, 50, 40, 30])
A54 = [('Playa', 100), ('Montaña', 120), ('Ciudad', 80), ('Pueblo', 60)]; F54 = [Fr(a * 72, 360) for _, a in A54]; CHK(sum(a for _, a in A54) == 360 and F54 == [20, 24, 16, 12])
B55 = [('Enero', 3), ('Febrero', Fr(5, 2)), ('Marzo', 4), ('Abril', Fr(11, 2))]; F55 = [4 * v for _, v in B55]; CHK(F55 == [12, 10, 16, 22] and sum(F55) == 60)
D56 = [(r'1\textsuperscript{o} A', 20), (r'1\textsuperscript{o} B', 35), (r'1\textsuperscript{o} C', 15), (r'1\textsuperscript{o} D', 30)]
S_.append(("Diagramas de sectores y pictogramas", [
 (1, r"Se ha preguntado a 36 alumnos por su deporte preferido: fútbol 15, baloncesto 9, tenis 6, natación 4 y otros 2. Calcula el ángulo de cada sector y dibuja el diagrama de sectores."
     + recorda(r"Ángulo del sector $=\dfrac{f_i}{N}\cdot360^\circ$. Si $N$ es divisor de 360, cada dato vale $360^\circ:N$."),
     r"Cada alumno vale $360^\circ:36=10^\circ$: \ " + ', '.join(r'%s $\res{%s^\circ}$' % (c, tn(a)) for (c, _), a in zip(E51, A51)) + '.' + center(tpie([c for c, _ in E51], [f for _, f in E51]))),
 (1, r"Calcula los ángulos del diagrama de sectores de los grupos sanguíneos del ejercicio @SANG@ (A: 9, O: 11, B: 3, AB: 2) y dibújalo.",
     r"Cada persona vale $360^\circ:25=14{,}4^\circ$: \ " + ', '.join(r'%s: $%d\cdot14{,}4=\res{%s^\circ}$' % (c, f, tn(a)) for (c, f), a in zip(TS, A52)) + '.' + center(tpie([c for c, _ in TS], [f for _, f in TS]))),
 (2, r"Se ha preguntado a 200 jóvenes qué aparato usan más para jugar. ¿Cuántas personas han elegido cada aparato?" + center(tpie([c for c, _ in P53], [p for _, p in P53], lab='pct')),
     ', '.join(r'%s: $%s\cdot200=\res{%d}$' % (c, tn(Fr(p, 100)), f) for (c, p), f in zip(P53, F53)) + r'. \ Comprobamos: $80+50+40+30=200$.'),
 (2, r"En un diagrama de sectores sobre el lugar de vacaciones preferido de 72 personas, los ángulos son: playa $100^\circ$, montaña $120^\circ$, ciudad $80^\circ$ y pueblo $60^\circ$. ¿Cuántas personas han elegido cada lugar?"
     + recorda(r"Del sector a la frecuencia: $f_i=\dfrac{\text{ángulo}}{360^\circ}\cdot N$."),
     ', '.join(r'%s: $\frac{%d}{360}\cdot72=\res{%d}$' % (c, a, f) for (c, a), f in zip(A54, F54)) + '.'),
 (2, r"Este pictograma muestra las bicis que ha vendido una tienda cada mes. Cada icono representa 4 bicis. ¿Cuántas ha vendido cada mes? ¿Y en total?" + center(tpicto([c for c, _ in B55], [v * 4 for _, v in B55], 4)),
     ', '.join(r'%s: $\res{%d}$' % (c, f) for (c, _), f in zip(B55, F55)) + r'. \ Total: $\res{60}$ bicis.'),
 (2, r"Los alumnos de cuatro grupos de 1\textsuperscript{o} de ESO han recogido tapones para una campaña solidaria: 1\textsuperscript{o} A, 20 bolsas; 1\textsuperscript{o} B, 35; 1\textsuperscript{o} C, 15, y 1\textsuperscript{o} D, 30. Haz un pictograma en el que cada icono valga 5 bolsas.",
     r"Hay que dibujar $20:5=\res{4}$, \ $35:5=\res{7}$, \ $15:5=\res{3}$ \ y \ $30:5=\res{6}$ iconos." + center(tpicto([c for c, _ in D56], [v for _, v in D56], 5, r'\faShoppingBag', 'teal'))),
 (3, r"En un diagrama de sectores, el sector de las personas que prefieren el verano mide $72^\circ$ y corresponde a 18 personas. ¿Cuántas personas se han encuestado? Si el $30\,\%$ prefiere la primavera, ¿cuántas personas son y qué ángulo tiene su sector?",
     r"Cada persona vale $72^\circ:18=4^\circ$, \ $N=360:4=\res{90}$ personas. \ Primavera: $0{,}3\cdot90=\res{27}$ personas, \ $27\cdot4=\res{108^\circ}$."),
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
S_.append(("Moda, media y mediana", [
 (1, r"Calcula la moda, la media y la mediana de: \ $%s$." % lst(D61)
     + recorda(r"\textbf{Moda}: el valor más repetido. \textbf{Media}: $\bar x=\dfrac{\text{suma de los datos}}{N}$. \textbf{Mediana}: el valor central de los datos \textbf{ordenados}; si hay dos, su media."),
     r"$Mo=\res{8}$. \ $\bar x=\frac{46}{7}\res{\approx6{,}57}$. \ Ordenados: $3,\ 5,\ 6,\ \underline{7},\ 8,\ 8,\ 9$: \ $Me=\res{7}$."),
 (1, r"Calcula la moda, la media y la mediana de: \ $%s$." % lst(D62),
     r"$Mo=\res{15}$. \ $\bar x=\frac{80}{6}\res{\approx13{,}33}$. \ Ordenados: $9,\ 11,\ \underline{12,\ 15},\ 15,\ 18$: \ $Me=\frac{12+15}{2}=\res{13{,}5}$."),
 (1, r"Se ha preguntado a 30 alumnos por su estación preferida: primavera 9, verano 13, otoño 3 e invierno 5. ¿Cuál es la moda? ¿Se pueden calcular la media y la mediana?",
     r"$Mo=$ \rest{verano}. La variable es cualitativa: \rest{no} se puede calcular ni la media ni la mediana."),
 (2, r"Calcula la moda, la media y la mediana de cada conjunto de datos:" + tasks(1, ['$' + lst(d) + '$' for d in D64]),
     tasks(1, [r"$Mo=\res{9}$; \ $\bar x=\frac{30}{5}=\res{6}$; \ $2,\ 4,\ \underline{6},\ 9,\ 9$: $Me=\res{6}$",
               r"Dos modas: $\res{3}$ y $\res{8}$; \ $\bar x=\frac{30}{6}=\res{5}$; \ $Me=\frac{3+7}{2}=\res{5}$",
               r"\rest{No hay moda} (todos aparecen una vez); \ $\bar x=\frac{100}{4}=\res{25}$; \ $Me=\frac{20+30}{2}=\res{25}$"])),
 (2, r"Los goles que ha marcado un equipo en los últimos 8 partidos son: \ $%s$. \ Calcula la moda, la media y la mediana." % lst(G65),
     r"$Mo=\res{2}$. \ $\bar x=\frac{15}{8}=\res{1{,}875}$ goles. \ Ordenados: $0,\ 1,\ 1,\ \underline{2,\ 2},\ 2,\ 3,\ 4$: \ $Me=\res{2}$."),
 (2, r"Los precios (en miles de euros) de las casas vendidas en una calle han sido: 150, 160, 155, 170, 165 y 900. Calcula la media y la mediana. ¿Cuál de los dos parámetros representa mejor el precio de una casa de la calle? ¿Por qué?",
     r"$\bar x=\frac{1\,700}{6}\res{\approx283{,}33}$ mil €. \ Ordenados: $150,\ 155,\ \underline{160,\ 165},\ 170,\ 900$: \ $Me=\res{162{,}5}$ mil €. \ La \rest{mediana}: la casa de 900 mil € es un dato extremo que tira de la media hacia arriba."),
 (3, r"Escribe cinco números que tengan media 6, mediana 5 y moda 4.",
     r"Por ejemplo, $\res{4,\ 4,\ 5,\ 8,\ 9}$: suman 30, \ $\bar x=6$; el central es el 5; el 4 es el más repetido. (Hay otras soluciones.)"),
 (3, r"Las notas de Juan son 4, 6, 7 y 9. ¿Cuál es la media? ¿Qué nota tiene que sacar en el siguiente examen para que la media sea 7?",
     r"$\bar x=\frac{26}{4}=\res{6{,}5}$. \ Con 5 exámenes, la suma tiene que ser $7\cdot5=35$: \ $35-26=\res{9}$."),
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
S_.append(("Parámetros a partir de una tabla de frecuencias", [
 (1, r"El número de hermanos de 25 alumnos es el de la tabla. Calcula la media, la mediana y la moda." + center(htab([x for x, _ in T71], [f for _, f in T71]))
     + recorda(r"$\bar x=\dfrac{\sum x_i\cdot f_i}{N}$. Para la mediana, busca la posición central y mira en qué fila la $F_i$ llega a ella."),
     center(ftab([x for x, _ in T71], [f for _, f in T71], ('f', 'F', 'xf'))) + r"$\bar x=\frac{39}{25}=\res{1{,}56}$. \ El dato central es el 13.\textsuperscript{o}: $F=14$ en el 1, \ $Me=\res{1}$. \ $Mo=\res{1}$."),
 (1, r"Calcula la media, la mediana y la moda de las notas del ejercicio @NOT@ a partir de su tabla de frecuencias.",
     center(ftab(XN, FN, ('f', 'F', 'xf'))) + r"$\bar x=\frac{179}{30}\res{\approx5{,}97}$. \ Los centrales son el 15.\textsuperscript{o} y el 16.\textsuperscript{o}: los dos valen 6 ($F$ pasa de 12 a 19), \ $Me=\res{6}$. \ $Mo=\res{6}$ ($f=7$)."),
 (2, r"Esta tabla recoge el número de calzado de 28 alumnos. Calcula la media, la mediana y la moda." + center(htab([x for x, _ in T73], [f for _, f in T73], xl='Número')),
     center(ftab([x for x, _ in T73], [f for _, f in T73], ('f', 'F', 'xf'))) + r"$\bar x=\frac{1\,049}{28}\res{\approx37{,}46}$. \ Los centrales son el 14.\textsuperscript{o} ($37$, porque $F=14$) y el 15.\textsuperscript{o} ($38$): \ $Me=\frac{37+38}{2}=\res{37{,}5}$. \ $Mo=\res{38}$."),
 (2, r"Los goles marcados por un equipo en 30 partidos han sido: 0 goles en 5 partidos, 1 gol en 8, 2 en 9, 3 en 6 y 4 en 2. Calcula la media de goles por partido, la mediana y la moda.",
     center(ftab([x for x, _ in T74], [f for _, f in T74], ('f', 'F', 'xf'))) + r"$\bar x=\frac{52}{30}\res{\approx1{,}73}$. \ Los centrales (15.\textsuperscript{o} y 16.\textsuperscript{o}) valen 2: $Me=\res{2}$. \ $Mo=\res{2}$."),
 (2, r"Calcula la media aproximada de los pesos agrupados del ejercicio @PES@ usando las marcas de clase.",
     center(ftab([tn(m) for m in MK], FP, ('f', 'xf'), xl='Marca').replace(r'\textbf{Total} & $24$ & ', r'\textbf{Total} & $24$ & $1\,140$')) + r"$\bar x\approx\frac{1\,140}{24}=\res{47{,}5}$\,kg."),
 (3, r"En esta tabla falta una frecuencia. Hállala sabiendo que la media es $1{,}5$." + center(htab([0, 1, 2, 3], [4, '$a$', 6, 4])),
     r"Sin el 1: $0\cdot4+2\cdot6+3\cdot4=24$ y hay 14 datos. \ $\frac{24+a}{14+a}=1{,}5\Rightarrow24+a=21+1{,}5a\Rightarrow3=0{,}5a\Rightarrow\res{a=6}$. \ Comprobamos: $\frac{30}{20}=1{,}5$."),
 (3, r"Este diagrama de barras muestra la nota (de 1 a 5) que 20 clientes han puesto a un restaurante. Calcula la media, la mediana y la moda." + center(tbar([str(x) for x, _ in B77], [f for _, f in B77], yl='Clientes', xl='Nota')),
     center(ftab([x for x, _ in B77], [f for _, f in B77], ('f', 'F', 'xf'))) + r"$\bar x=\frac{58}{20}=\res{2{,}9}$. \ Los centrales (10.\textsuperscript{o} y 11.\textsuperscript{o}) valen 3: $Me=\res{3}$. \ $Mo=\res{3}$."),
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
S_.append(("Rango y desviación media", [
 (1, r"Calcula el rango de cada conjunto de datos:" + tasks(3, ['$' + lst(d) + '$' for d in R81])
     + recorda(r"Rango $=x_{\max}-x_{\min}$. \ Desviación media: $DM=\dfrac{\sum|x_i-\bar x|}{N}$ (la media de las distancias a la media)."),
     tasks(3, [r"$15-3=\res{12}$", r"$8-(-4)=\res{12}$", r"$4{,}8-1{,}3=\res{3{,}5}$"])),
 (1, r"Calcula la desviación media de: \ $%s$." % lst(D82),
     r"$\bar x=\frac{35}{5}=7$. \ Distancias: $4,\ 2,\ 0,\ 2,\ 4$. \ $DM=\frac{12}{5}=\res{2{,}4}$."),
 (2, r"Calcula la media, el rango y la desviación media de: \ $%s$." % lst(D83),
     r"$\bar x=\frac{36}{6}=\res{6}$. \ Rango $=12-2=\res{10}$. \ Distancias: $4,\ 2,\ 2,\ 0,\ 2,\ 6$; \ $DM=\frac{16}{6}\res{\approx2{,}67}$."),
 (2, r"Las notas de dos alumnos en seis exámenes han sido: Ana, $%s$; Gabriel, $%s$. Calcula la media, el rango y la desviación media de cada uno. ¿Quién es más regular?" % (lst(NA), lst(NB)),
     r"Los dos tienen $\bar x=\frac{33}{6}=5{,}5$. \ Ana: rango $\res{1}$, \ $DM=\frac{6\cdot0{,}5}{6}=\res{0{,}5}$. \ Gabriel: rango $9-2=\res{7}$, distancias $3{,}5;\ 3{,}5;\ 2{,}5;\ 2{,}5;\ 1{,}5;\ 1{,}5$, \ $DM=\frac{15}{6}=\res{2{,}5}$. \ \rest{Ana} es más regular."),
 (2, r"Las temperaturas máximas de una semana de cinco días en dos ciudades han sido: ciudad X, $%s$\,°C; ciudad Y, $%s$\,°C. Compáralas con la media, el rango y la desviación media." % (lst(CX), lst(CY)),
     r"Las dos tienen $\bar x=\res{14}$\,°C. \ X: rango $\res{4}$, \ $DM=\frac{6}{5}=\res{1{,}2}$. \ Y: rango $\res{14}$, \ $DM=\frac{8+6+4+4+2}{5}=\frac{24}{5}=\res{4{,}8}$. \ En la ciudad \rest{Y} las temperaturas varían mucho más."),
 (3, r"Calcula la media y la desviación media de los datos de esta tabla." + center(htab([x for x, _ in T86], [f for _, f in T86])),
     r"$\bar x=\frac{2+6+15+12+10}{15}=\frac{45}{15}=\res{3}$. \ $DM=\frac{2\cdot2+1\cdot3+0\cdot5+1\cdot3+2\cdot2}{15}=\frac{14}{15}\res{\approx0{,}93}$."),
 (3, r"Razona si es verdadero o falso:" + tasks(1, [r"Si el rango es 0, todos los datos son iguales.", r"Si sumamos 5 a todos los datos, la desviación media aumenta 5.", r"Dos conjuntos con la misma media tienen la misma desviación media.", r"La desviación media nunca puede ser negativa."]),
     tasks(1, [r"\rest{Verdadero}: el mayor y el menor coinciden.", r"\rest{Falso}: todos los datos se desplazan igual y las distancias a la media no cambian.", r"\rest{Falso}: por ejemplo, $5,\ 5$ y $0,\ 10$ tienen media 5 pero $DM=0$ y $DM=5$.", r"\rest{Verdadero}: es una media de distancias, que son positivas o cero."])),
]))
CHK(dm([5, 5]) == 0 and dm([0, 10]) == 5 and dm([x + 5 for x in D82]) == dm(D82))

# =====================================================================
# 9. Problemes d'estadística
# =====================================================================
FAM = [0, 1, 2, 2, 1, 3, 2, 1, 1, 2, 0, 2, 3, 1, 2, 4, 2, 1, 2, 1]
TF = freqs(FAM); CHK(TF == [(0, 2), (1, 7), (2, 8), (3, 2), (4, 1)] and sum(FAM) == 33 and median(FAM) == 2 and modes(FAM) == [2] and rang(FAM) == 4)
CHK(Fr(8, 20) * 360 == 144)
S_.append(("Problemas de estadística", [
 (1, r"Marina ha sacado $6{,}5$; $7$ y $5{,}5$ en los tres primeros exámenes. ¿Qué nota necesita en el cuarto para tener una media de $6{,}5$?"
     + recorda(r"Si conocemos la media y el número de datos, conocemos la suma: \ $\text{suma}=\bar x\cdot N$."),
     r"Suma necesaria: $6{,}5\cdot4=26$. \ Ya tiene $6{,}5+7+5{,}5=19$. \ Necesita un $26-19=\res{7}$."),
 (1, r"La media de cuatro números es 12. Tres de ellos son 10, 15 y 9. ¿Cuál es el cuarto?",
     r"Suma: $12\cdot4=48$. \ $48-(10+15+9)=\res{14}$."),
 (2, r"En una clase de 25 alumnos la nota media de un examen ha sido $6{,}4$ y en otra de 15 alumnos, $7{,}2$. ¿Cuál es la nota media de los 40 alumnos? ¿Por qué no es $6{,}8$?",
     r"$6{,}4\cdot25=160$; \ $7{,}2\cdot15=108$; \ $\bar x=\frac{160+108}{40}=\frac{268}{40}=\res{6{,}7}$. \ No es la media de las medias porque las clases \rest{no tienen el mismo número de alumnos}."),
 (2, r"Se ha preguntado a 20 familias cuántos hijos tienen: \ $%s$." % lst(FAM) + tasks(1, [r"Haz la tabla de frecuencias (con $f_i$, $F_i$ y $h_i$).", r"Dibuja su diagrama de barras.", r"Calcula la moda, la media, la mediana y el rango.", r"¿Qué porcentaje de familias tiene más de un hijo? ¿Qué ángulo tendría el sector «2 hijos» en un diagrama de sectores?"]),
     center(ftab([x for x, _ in TF], [f for _, f in TF], ('f', 'F', 'h'))) + center(tbar([str(x) for x, _ in TF], [f for _, f in TF], yl='Familias', xl='Hijos'))
     + r"$Mo=\res{2}$; \ $\bar x=\frac{33}{20}=\res{1{,}65}$; \ los centrales (10.\textsuperscript{o} y 11.\textsuperscript{o}) valen 2: $Me=\res{2}$; \ rango $=4-0=\res{4}$. \ Más de un hijo: $8+2+1=11$, \ $\frac{11}{20}=\res{55\,\%}$. \ Sector: $\frac{8}{20}\cdot360^\circ=\res{144^\circ}$."),
 (2, r"La edad media de los 11 jugadores de un equipo es de 22 años. Si añadimos al entrenador, la edad media de los 12 es de 24 años. ¿Cuántos años tiene el entrenador?",
     r"$22\cdot11=242$; \ $24\cdot12=288$; \ $288-242=\res{46}$ años."),
 (3, r"Un profesor ha calculado que la media de las notas de los 10 alumnos de un grupo es $6{,}3$, pero después se da cuenta de que ha copiado un 9 en lugar de un 4. ¿Cuál es la media correcta? ¿Cambia la mediana si las notas eran 3, 4, 5, 5, 6, 7, 7, 8, 9, 9 (con el 9 equivocado)?",
     r"Suma errónea: $63$; correcta: $63-9+4=58$; \ $\bar x=\res{5{,}8}$. \ Mediana errónea: $\frac{6+7}{2}=6{,}5$. Correcta (3, 4, 4, 5, 5, 6, 7, 7, 8, 9): $\frac{5+6}{2}=\res{5{,}5}$. Sí que cambia."),
 (3, r"De dos clases se conocen estos resultados de un examen: clase A, $\bar x=6$, $Me=6$, $DM=0{,}8$; clase B, $\bar x=6$, $Me=7$, $DM=2{,}5$. Razona si es verdadero o falso:" + tasks(1, [r"Las dos clases han sacado, de media, la misma nota.", r"En la clase B, al menos la mitad de los alumnos ha sacado un 7 o más.", r"Las notas de la clase A son más parecidas entre sí.", r"En la clase A hay alumnos con un 10."]),
     tasks(1, [r"\rest{Verdadero}: $\bar x=6$ en las dos.", r"\rest{Verdadero}: la mediana es 7.", r"\rest{Verdadero}: tiene menos desviación media.", r"\rest{No se puede saber} con estos datos."])),
]))
EQ(fr('6.5') * 4 - (fr('6.5') + 7 + fr('5.5')), 7); EQ(48 - 34, 14); EQ(Fr(268, 40), '6.7'); EQ(24 * 12 - 22 * 11, 46)
W9 = [3, 4, 5, 5, 6, 7, 7, 8, 9, 9]; W9c = [3, 4, 4, 5, 5, 6, 7, 7, 8, 9]
CHK(sum(W9) == 63 and sum(W9c) == 58 and median(W9) == Fr(13, 2) and median(W9c) == Fr(11, 2))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\definecolor{violet}{HTML}{7C6CF0}\n\\definecolor{gold}{HTML}{E0A21B}\n'
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TIT = "Estadística"

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 10: %s' % (t, TIT), capcalera='%s · Unidad 10' % t,
                 pdfkeywords='estadística, población, muestra, variables estadísticas, frecuencias, tablas de frecuencias, diagrama de barras, polígono de frecuencias, histograma, diagrama de sectores, pictograma, moda, media, mediana, rango, desviación media',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 10' if sol else 'Ficha de ejercicios · Unidad 10') + '}{' + TIT + '}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás un laboratorio de datos que hace tablas de frecuencias y herramientas para construir gráficos y para calcular la moda, la media, la mediana y la desviación media."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Para hacer gráficos, usa papel cuadriculado, regla y transportador, y pon siempre el título y el nombre de cada eje.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't10-fitxa-solucions-es.tex' if sol else 't10-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
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
print(n, 'ejercicios,', NCHK[0], 'comprobaciones')
print(LAB)
