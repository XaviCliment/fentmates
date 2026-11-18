# Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 10: Estadística bidimensional)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 6 seccions segueixen els apartats dels apunts (10.1-10.6): distribucions bidimensionals; núvol de punts; correlació;
# coeficient de correlació; recta de regressió; estimacions. Els núvols de punts es dibuixen amb TikZ (nuvol); els càlculs de
# r i de la recta de regressió els escriuen pas a pas passos_r() i passos_recta() a partir de les dades (bi() amb fraccions).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es). Cada resultat es comprova amb EQ (exacte, amb fraccions) o AP (arrodonit).
# Ús: python3 genera.py && pdflatex t10-fitxa-exercicis.tex (dues vegades) && pdflatex t10-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math, random
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def center(t): return r'\par\smallskip\begin{center}' + t + r'\end{center}'
def side(*figs): return r'\par\smallskip\begin{center}' + r'\hspace{0.6cm}'.join(figs) + r'\end{center}'

# ---------- comprovacions i estadística exacta ----------
NCHK = [0]
def CHK(cond, *info):
    NCHK[0] += 1
    assert cond, info
def fr(v): return v if isinstance(v, Fr) else Fr(str(v).replace('{,}', '.').replace(',', '.'))
def EQ(a, b): CHK(fr(a) == fr(b), a, b)
def AP(a, b, d=2): CHK(abs(float(a) - float(fr(b))) <= 0.5 * 10 ** -d + 1e-9, float(a), b)
def bi(xs, ys):
    N = len(xs); X = [fr(x) for x in xs]; Y = [fr(y) for y in ys]
    S = dict(N=N, sx=sum(X), sy=sum(Y), sx2=sum(x * x for x in X), sy2=sum(y * y for y in Y), sxy=sum(x * y for x, y in zip(X, Y)))
    S['mx'] = S['sx'] / N; S['my'] = S['sy'] / N
    S['vx'] = S['sx2'] / N - S['mx'] ** 2; S['vy'] = S['sy2'] / N - S['my'] ** 2; S['c'] = S['sxy'] / N - S['mx'] * S['my']
    S['sdx'] = math.sqrt(S['vx']); S['sdy'] = math.sqrt(S['vy'])
    S['r'] = float(S['c']) / (S['sdx'] * S['sdy'])
    S['m'] = S['c'] / S['vx']; S['n'] = S['my'] - S['m'] * S['mx']
    return S

# ---------- nombres ----------
def exact(v):
    v = fr(v); d = v.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    return d == 1
def tn(v):
    v = fr(v)
    if v.denominator == 1: return str(v.numerator).replace('-', '-')
    t = ('%.10f' % float(v)).rstrip('0').rstrip('.')
    CHK(fr(t) == v, v)
    return t.replace('.', '{,}')
def big(v):
    """enters grans amb espai de milers"""
    t = tn(v)
    if '{,}' in t or len(t.lstrip('-')) < 5: return t
    s = t.lstrip('-'); g = []
    while len(s) > 3: g.insert(0, s[-3:]); s = s[:-3]
    return ('-' if t.startswith('-') else '') + s + r'\,' + r'\,'.join(g)
def rd(v, d=2):
    """arrodonit a d decimals (text, sense signe d'igual)"""
    t = ('%.*f' % (d, float(v))).rstrip('0').rstrip('.')
    return ('0' if t in ('-0', '') else t).replace('.', '{,}')
def eqv(v, d=2):
    """«=valor» si és exacte amb com a molt d decimals; si no, «≈valor arrodonit»"""
    if not isinstance(v, float) and exact(v):
        t = tn(v)
        if len(t.split('{,}')[1] if '{,}' in t else '') <= d: return '=' + big(v)
    return r'\approx ' + rd(v, d)
def par(v):
    t = tn(v) if not isinstance(v, float) and exact(v) and len(tn(v)) < 8 else rd(v)
    return '(' + t + ')' if t.startswith('-') else t
def lst(d): return r',\ \allowbreak '.join(tn(x) for x in d)
def pairs(xs, ys): return r',\ \allowbreak '.join('(%s,\\,%s)' % (tn(a), tn(b)) for a, b in zip(xs, ys))
def line(m, n, d=2):
    """y = mx + n amb els coeficients exactes o arrodonits"""
    mt = tn(m) if exact(m) and len(tn(m).split('{,}')[-1]) <= 3 else rd(m, d)
    nt = tn(abs(n)) if exact(n) and len(tn(n).split('{,}')[-1]) <= 3 else rd(abs(n), d)
    mt = '' if mt == '1' else '-' if mt == '-1' else mt
    return 'y=%sx%s' % (mt, '' if n == 0 else ('+' if n > 0 else '-') + nt)

# ---------- taules ----------
def ptab(xs, ys, xl='$x_i$', yl='$y_i$', w='0.8cm'):
    cell = lambda v: '$%s$' % tn(v)
    return (r'{\renewcommand{\arraystretch}{1.3}\begin{tabular}{|l|%s|}\hline %s & %s\\\hline %s & %s\\\hline\end{tabular}}'
            % ('|'.join(['C{%s}' % w] * len(xs)), xl, ' & '.join(cell(x) for x in xs), yl, ' & '.join(cell(y) for y in ys)))
def btab(xs, ys, xl='$x_i$', yl='$y_i$'):
    S = bi(xs, ys)
    rows = [' & '.join('$%s$' % big(v) for v in (x, y, fr(x) ** 2, fr(y) ** 2, fr(x) * fr(y))) for x, y in zip(xs, ys)]
    tot = ' & '.join('$%s$' % big(S[k]) for k in ('sx', 'sy', 'sx2', 'sy2', 'sxy'))
    return (r'{\renewcommand{\arraystretch}{1.15}\small\begin{tabular}{|c|c|c|c|c|}\hline %s & %s & $x_i^2$ & $y_i^2$ & $x_i\cdot y_i$\\\hline ' % (xl, yl)
            + r'\\ '.join(rows) + r'\\\hline ' + tot + r'\\\hline\end{tabular}}')
def dtab(xv, yv, F, xl='X', yl='Y', blanks=()):
    """taula de doble entrada: F[i][j] = freqüència de (xv[i], yv[j]); blanks: caselles que es deixen buides ((i, j); i = len(xv) és la fila de totals, j = len(yv) la columna)"""
    fx = [sum(r) for r in F]; fy = [sum(F[i][j] for i in range(len(xv))) for j in range(len(yv))]
    cell = lambda i, j, v: r'\phantom{00}' if (i, j) in blanks else '$%d$' % v
    head = r'$%s\backslash %s$ & ' % (xl, yl) + ' & '.join('$%s$' % tn(y) for y in yv) + r' & $f_x$'
    rows = ['$%s$ & ' % tn(x) + ' & '.join(cell(i, j, F[i][j]) for j in range(len(yv))) + ' & ' + cell(i, len(yv), fx[i]) for i, x in enumerate(xv)]
    rows.append('$f_y$ & ' + ' & '.join(cell(len(xv), j, fy[j]) for j in range(len(yv))) + ' & ' + cell(len(xv), len(yv), sum(fx)))
    return (r'{\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|%s|c|}\hline ' % '|'.join('c' * len(yv)) + head + r'\\\hline '
            + r'\\\hline '.join(rows) + r'\\\hline\end{tabular}}')

# ---------- núvols de punts (TikZ) ----------
def nuvol(pts, xr, yr, lx='X', ly='Y', W=5.0, H=3.6, cg=False, reg=None, eye=None, est=None, lab=None, dot=0.085):
    """xr, yr = (mín, màx, pas); reg/eye: recta (m, n); est: (x0, y0) amb línies de lectura; lab: etiquetes al costat dels punts"""
    (x0, x1, xs), (y0, y1, ys) = xr, yr
    X = lambda v: W * (float(v) - x0) / (x1 - x0); Y = lambda v: H * (float(v) - y0) / (y1 - y0)
    o = [r'\begin{tikzpicture}[baseline=(current bounding box.center),line cap=round]']
    v = x0
    while v <= x1 + 1e-9:
        o.append(r'\draw[muted!25,line width=0.3pt] (%.3f,0)--(%.3f,%.3f); \node[below,font=\tiny,text=muted,inner sep=1.5pt] at (%.3f,0) {$%s$};' % (X(v), X(v), H, X(v), tn(Fr(v).limit_denominator(1000))))
        v += xs
    v = y0
    while v <= y1 + 1e-9:
        o.append(r'\draw[muted!25,line width=0.3pt] (0,%.3f)--(%.3f,%.3f); \node[left,font=\tiny,text=muted,inner sep=1.5pt] at (0,%.3f) {$%s$};' % (Y(v), W, Y(v), Y(v), tn(Fr(v).limit_denominator(1000))))
        v += ys
    o.append(r'\draw[-latex,muted,line width=0.6pt] (0,0)--(%.3f,0) node[right,font=\scriptsize,text=navy]{%s};' % (W + 0.3, lx))
    o.append(r'\draw[-latex,muted,line width=0.6pt] (0,0)--(0,%.3f) node[above,font=\scriptsize,text=navy]{%s};' % (H + 0.3, ly))
    def seg(m, n, sty):
        m, n = float(m), float(n); a, b = x0, x1
        if m:
            c1, c2 = (y0 - n) / m, (y1 - n) / m; a = max(a, min(c1, c2)); b = min(b, max(c1, c2))
        if b > a: o.append(r'\draw[%s] (%.3f,%.3f)--(%.3f,%.3f);' % (sty, X(a), Y(m * a + n), X(b), Y(m * b + n)))
    if eye: seg(eye[0], eye[1], 'accent,line width=1pt,dashed')
    if reg: seg(reg[0], reg[1], 'violet,line width=1.2pt')
    if est:
        o.append(r'\draw[gold,line width=0.8pt,dashed] (%.3f,0)--(%.3f,%.3f)--(0,%.3f);' % (X(est[0]), X(est[0]), Y(est[1]), Y(est[1])))
    for i, (a, b) in enumerate(pts):
        o.append(r'\fill[teal] (%.3f,%.3f) circle (%.3f);' % (X(a), Y(b), dot))
        if lab: o.append(r'\node[above right,font=\tiny,inner sep=1pt] at (%.3f,%.3f) {%s};' % (X(a), Y(b), lab[i]))
    if cg:
        S = bi([p[0] for p in pts], [p[1] for p in pts])
        o.append(r'\draw[navy,line width=1pt,fill=white] (%.3f,%.3f) circle (0.09);' % (X(S['mx']), Y(S['my'])))
    if est: o.append(r'\draw[gold,line width=1.2pt] (%.3f,%.3f) circle (0.1);' % (X(est[0]), Y(est[1])))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def gen(n, r, seed):
    """n punts (escala 0-10) amb coeficient de correlació exactament r"""
    rnd = random.Random(seed)
    z1 = [rnd.gauss(0, 1) for _ in range(n)]; z2 = [rnd.gauss(0, 1) for _ in range(n)]
    def st(a):
        m = sum(a) / n; s = math.sqrt(sum((v - m) ** 2 for v in a) / n); return [(v - m) / s for v in a]
    z1 = st(z1); dd = sum(a * b for a, b in zip(z1, z2)) / n; z2 = st([b - dd * a for a, b in zip(z1, z2)])
    return [(5 + 1.5 * a, 5 + 1.5 * (r * a + math.sqrt(max(0, 1 - r * r)) * b)) for a, b in zip(z1, z2)]
def rfl(pts):
    S = bi([Fr(p[0]).limit_denominator(10 ** 6) for p in pts], [Fr(p[1]).limit_denominator(10 ** 6) for p in pts]); return S['r']
def nv(pts, t=None):
    pts = [p for p in pts if 0 <= p[0] <= 10 and 0 <= p[1] <= 10]
    g = nuvol(pts, (0, 10, 2), (0, 10, 2), lx='', ly='', W=2.8, H=2.4, dot=0.055)
    return (r'\begin{tabular}{c}' + g + r'\\[-1pt] \small\textbf{' + t + r'}\end{tabular}') if t else g

# ---------- càlculs escrits pas a pas ----------
def passos_r(xs, ys, taula=True, xl='$x_i$', yl='$y_i$', sx=None, sy=None):
    """taula + mitjanes + desviacions típiques + covariància + r (escrits amb els valors exactes o arrodonits)"""
    S = bi(xs, ys); N = S['N']
    def sq(v): return r'\sqrt{%s}' % tn(v) if exact(v) and len(tn(v)) <= 7 else r'\sqrt{%s}' % rd(v)
    out = (center(btab(xs, ys, xl, yl)) if taula else '')
    out += r'$\bar x=\frac{%s}{%d}%s$, \ $\bar y=\frac{%s}{%d}%s$. \ ' % (big(S['sx']), N, eqv(S['mx']), big(S['sy']), N, eqv(S['my']))
    out += r'$\sigma_x=\sqrt{\frac{%s}{%d}-%s^2}=%s%s$, \ ' % (big(S['sx2']), N, par(S['mx']), sq(S['vx']), eqv(S['sdx']))
    out += r'$\sigma_y=\sqrt{\frac{%s}{%d}-%s^2}=%s%s$. \ ' % (big(S['sy2']), N, par(S['my']), sq(S['vy']), eqv(S['sdy']))
    out += r'$\sigma_{xy}=\frac{%s}{%d}-%s\cdot %s%s$. \ ' % (big(S['sxy']), N, par(S['mx']), par(S['my']), eqv(S['c']))
    out += r'$r=\frac{%s}{%s\cdot %s}\approx\res{%s}$' % (tn(S['c']) if exact(S['c']) else rd(S['c']), rd(S['sdx']), rd(S['sdy']), rd(S['r']))
    for k in ('mx', 'my', 'c'):
        if not exact(S[k]): pass
    return S, out
def passos_recta(S, d=2):
    m, n = S['m'], S['n']
    mt = tn(m) if exact(m) and len(tn(m).split('{,}')[-1]) <= 3 else rd(m, d)
    out = r'$m=\frac{\sigma_{xy}}{\sigma_x^2}=\frac{%s}{%s}%s$; \ ' % (tn(S['c']) if exact(S['c']) else rd(S['c']), tn(S['vx']) if exact(S['vx']) else rd(S['vx']), eqv(m, 3 if exact(m) else d))
    out += r'$y-%s=%s\,(x-%s)\ \Rightarrow\ \res{%s}$' % (par(S['my']), mt, par(S['mx']), line(m, n, d))
    return out
def kind(r):
    a = abs(r); s = T('positiva', 'positiva') if r > 0 else T('negativa', 'negativa')
    if a > 0.9999: return s + T(' perfecta', ' perfecta')
    if a < 0.1: return T('pràcticament nul·la', 'prácticamente nula')
    return s + (T(' i forta', ' y fuerte') if a >= 0.8 else T(' moderada', ' moderada') if a >= 0.5 else T(' i feble', ' y débil'))

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Distribucions bidimensionals
# =====================================================================
F3 = [[3, 4, 1], [5, 6, 3], [2, 4, 2]]; X3 = [0, 1, 2]; Y3 = [0, 1, 2]
CHK([sum(r) for r in F3] == [8, 14, 8] and [sum(F3[i][j] for i in range(3)) for j in range(3)] == [10, 14, 6])
DK = [1, 2, 2.5, 3, 4, 5, 6, 8]; DM = [10, 12, 15, 14, 20, 22, 25, 30]
L4 = [(1, 0), (2, 1), (1, 1), (3, 2), (2, 1), (1, 0), (2, 2), (3, 1), (2, 1), (1, 1), (3, 2), (2, 0), (1, 1), (2, 1), (3, 2), (2, 2)]
F4 = [[sum(1 for p in L4 if p == (x, y)) for y in (0, 1, 2)] for x in (1, 2, 3)]
CHK(F4 == [[2, 3, 0], [1, 4, 2], [0, 1, 3]] and len(L4) == 16, F4)
F6 = [[4, 2, 1], [3, 5, 2], [1, 3, 4]]; FX6 = [sum(r) for r in F6]; FY6 = [sum(F6[i][j] for i in range(3)) for j in range(3)]
CHK(FX6 == [7, 10, 8] and FY6 == [8, 10, 7])
S_.append((T("Distribucions bidimensionals", "Distribuciones bidimensionales"), [
 (1, T(r"Digues si la relació entre les variables és funcional, estadística o si no hi ha relació:", r"Di si la relación entre las variables es funcional, estadística o si no hay relación:")
     + recorda(T(r"\textbf{Funcional}: hi ha una fórmula exacta. \textbf{Estadística}: hi ha una tendència, però no una fórmula. \textbf{Cap}: una variable no diu res de l'altra.", r"\textbf{Funcional}: hay una fórmula exacta. \textbf{Estadística}: hay una tendencia, pero no una fórmula. \textbf{Ninguna}: una variable no dice nada de la otra."))
     + tasks(2, [T("Radi d'un cercle i àrea.", "Radio de un círculo y área."), T("Pes i alçada d'unes persones.", "Peso y altura de unas personas."),
                 T("Nota de música i número de calçat.", "Nota de música y número de calzado."), T("Km d'un taxi i preu (2 € més 1,10 €/km).", "Km de un taxi y precio (2 € más 1,10 €/km)."),
                 T("Hores de son i rendiment en un examen.", "Horas de sueño y rendimiento en un examen."), T("Any de naixement i edat a 31 de desembre.", "Año de nacimiento y edad a 31 de diciembre.")]),
     tasks(2, [T(r"\rest{Funcional}: $A=\pi r^2$.", r"\rest{Funcional}: $A=\pi r^2$."), T(r"\rest{Estadística}.", r"\rest{Estadística}."), T(r"\rest{Cap relació}.", r"\rest{Ninguna relación}."),
               T(r"\rest{Funcional}: $y=2+1{,}1x$.", r"\rest{Funcional}: $y=2+1{,}1x$."), T(r"\rest{Estadística}.", r"\rest{Estadística}."), T(r"\rest{Funcional}: $y=2026-x$, per exemple.", r"\rest{Funcional}: $y=2026-x$, por ejemplo.")])),
 (1, T(r"Aquesta taula dona la distància (km) entre la casa i l'institut de 8 alumnes i el temps (minuts) que tarden a arribar-hi:", r"Esta tabla da la distancia (km) entre la casa y el instituto de 8 alumnos y el tiempo (minutos) que tardan en llegar:")
     + center(ptab(DK, DM, T('Distància (km)', 'Distancia (km)'), T('Temps (min)', 'Tiempo (min)')))
     + tasks(1, [T(r"Escriu les parelles de dades. Quant val $N$?", r"Escribe las parejas de datos. ¿Cuánto vale $N$?"), T(r"Quants alumnes viuen a més de 3 km? Quants tarden més d'un quart d'hora?", r"¿Cuántos alumnos viven a más de 3 km? ¿Cuántos tardan más de un cuarto de hora?"),
                 T(r"La relació entre les variables és funcional o estadística? Per què?", r"¿La relación entre las variables es funcional o estadística? ¿Por qué?")]),
     tasks(1, [r'$%s$; \ $N=\res{8}$.' % pairs(DK, DM), T(r"A més de 3 km: $\res{4}$ alumnes. Més de 15 minuts: $\res{4}$ alumnes.", r"A más de 3 km: $\res{4}$ alumnos. Más de 15 minutos: $\res{4}$ alumnos."),
               T(r"\rest{Estadística}: els que viuen més lluny solen tardar més, però no sempre (qui viu a 2,5 km tarda més que qui viu a 3 km).", r"\rest{Estadística}: los que viven más lejos suelen tardar más, pero no siempre (quien vive a 2,5 km tarda más que quien vive a 3 km).")])),
 (1, T(r"S'ha preguntat a 30 alumnes quants germans tenen ($X$) i quantes mascotes ($Y$):", r"Se ha preguntado a 30 alumnos cuántos hermanos tienen ($X$) y cuántas mascotas ($Y$):")
     + center(dtab(X3, Y3, F3))
     + tasks(1, [T("Quants alumnes tenen 1 germà i 2 mascotes?", "¿Cuántos alumnos tienen 1 hermano y 2 mascotas?"), T("Quants alumnes no tenen mascota?", "¿Cuántos alumnos no tienen mascota?"),
                 T("Quants tenen tants germans com mascotes?", "¿Cuántos tienen tantos hermanos como mascotas?"), T("Quin percentatge té 2 germans?", "¿Qué porcentaje tiene 2 hermanos?")]),
     tasks(2, [r'$\res{3}$', r'$\res{10}$', r'$3+6+2=\res{11}$', r'$\frac{8}{30}\approx\res{26{,}7\,\%}$'])),
 (2, T(r"Fes la taula de doble entrada d'aquestes 16 parelles, amb els totals de les files i de les columnes:", r"Haz la tabla de doble entrada de estas 16 parejas, con los totales de las filas y de las columnas:")
     + center('$' + r',\ '.join('(%d,%d)' % p for p in L4) + '$'),
     center(dtab([1, 2, 3], [0, 1, 2], F4))),
 (2, T(r"Amb la taula de l'exercici 3, calcula el nombre mitjà de germans i el nombre mitjà de mascotes dels 30 alumnes.", r"Con la tabla del ejercicio 3, calcula el número medio de hermanos y el número medio de mascotas de los 30 alumnos.")
     + recorda(T(r"La darrera columna ($f_x$) és la distribució de $X$ i la darrera fila ($f_y$), la de $Y$.", r"La última columna ($f_x$) es la distribución de $X$ y la última fila ($f_y$), la de $Y$.")),
     r'$\bar x=\frac{0\cdot8+1\cdot14+2\cdot8}{30}=\frac{30}{30}=\res{1}$ ' + T('germà', 'hermano') + r'; \ $\bar y=\frac{0\cdot10+1\cdot14+2\cdot6}{30}=\frac{26}{30}\approx\res{0{,}87}$ ' + T('mascotes', 'mascotas') + '.'),
 (3, T(r"Completa la taula de doble entrada:", r"Completa la tabla de doble entrada:")
     + center(dtab([1, 2, 3], [0, 1, 2], F6, blanks={(0, 1), (1, 0), (2, 2), (3, 0), (3, 3)})),
     T(r"Fila 1: $7-4-1=\res{2}$. Fila 2: $10-5-2=\res{3}$. Fila 3: $8-1-3=\res{4}$. Total de la columna $y=0$: $4+3+1=\res{8}$. Total: $7+10+8=\res{25}$ (o bé $8+10+7$).",
       r"Fila 1: $7-4-1=\res{2}$. Fila 2: $10-5-2=\res{3}$. Fila 3: $8-1-3=\res{4}$. Total de la columna $y=0$: $4+3+1=\res{8}$. Total: $7+10+8=\res{25}$ (o bien $8+10+7$).")
     + center(dtab([1, 2, 3], [0, 1, 2], F6))),
]))
CHK(sum(1 for d in DK if d > 3) == 4 and sum(1 for t in DM if t > 15) == 4 and F3[1][2] == 3 and F3[0][0] + F3[1][1] + F3[2][2] == 11)
EQ(Fr(0 * 8 + 14 + 16, 30), 1); AP(Fr(26, 30), '0.87'); AP(Fr(800, 30), '26.7', 1)
EQ(FX6[0] - F6[0][0] - F6[0][2], 2); EQ(FX6[1] - F6[1][1] - F6[1][2], 3); EQ(FX6[2] - F6[2][0] - F6[2][1], 4)
CHK(F6[0][1] == 2 and F6[1][0] == 3 and F6[2][2] == 4 and FY6[0] == 8 and sum(FX6) == 25)

# =====================================================================
# 2. Núvol de punts
# =====================================================================
X7 = [1, 2, 3, 4, 5, 6]; Y7 = [2, 4, 3, 6, 5, 7]; S7 = bi(X7, Y7); EQ(S7['mx'], '3.5'); EQ(S7['my'], '4.5')
P8 = [(1, 8), (2, 6), (4, 5), (5, 3), (8, 3)]; S8 = bi(*zip(*P8)); EQ(S8['mx'], 4); EQ(S8['my'], 5)
AX = [150, 155, 160, 165, 170, 175]; AY = [45, 52, 54, 60, 63, 70]; SA = bi(AX, AY); EQ(SA['mx'], '162.5'); AP(SA['my'], '57.33')
P11 = [(2, 7), (3, 5), (5, 6), (6, 2)]; EQ(5 * Fr(21, 5) - sum(p[0] for p in P11), 5); EQ(5 * 5 - sum(p[1] for p in P11), 5)
P12 = [(2, 3), (4, 7), (6, 5)]
S_.append((T("Núvol de punts", "Nube de puntos"), [
 (1, T(r"Dibuixa el núvol de punts d'aquesta distribució i calcula'n el centre de gravetat:", r"Dibuja la nube de puntos de esta distribución y calcula su centro de gravedad:") + center(ptab(X7, Y7))
     + recorda(T(r"El \textbf{centre de gravetat} és el punt $(\bar x,\,\bar y)$, amb $\bar x=\frac{\sum x_i}{N}$ i $\bar y=\frac{\sum y_i}{N}$.", r"El \textbf{centro de gravedad} es el punto $(\bar x,\,\bar y)$, con $\bar x=\frac{\sum x_i}{N}$ e $\bar y=\frac{\sum y_i}{N}$.")),
     r'$\bar x=\frac{21}{6}=3{,}5$, \ $\bar y=\frac{27}{6}=4{,}5$: \ ' + T('centre de gravetat', 'centro de gravedad') + r' $\res{(3{,}5,\ 4{,}5)}$.' + center(nuvol(list(zip(X7, Y7)), (0, 7, 1), (0, 8, 1), cg=True))),
 (1, T(r"Escriu la taula de dades d'aquest núvol de punts i calcula'n el centre de gravetat.", r"Escribe la tabla de datos de esta nube de puntos y calcula su centro de gravedad.") + center(nuvol(P8, (0, 9, 1), (0, 9, 1))),
     center(ptab([p[0] for p in P8], [p[1] for p in P8])) + r'$\bar x=\frac{20}{5}=4$, \ $\bar y=\frac{25}{5}=5$: \ $\res{(4,\ 5)}$.'),
 (2, T(r"Dibuixa el núvol de punts de les alçades (cm) i els pesos (kg) de sis persones. Fes que els eixos no comencen en 0 i calcula el centre de gravetat.", r"Dibuja la nube de puntos de las alturas (cm) y los pesos (kg) de seis personas. Haz que los ejes no empiecen en 0 y calcula el centro de gravedad.")
     + center(ptab(AX, AY, T('Alçada', 'Altura'), T('Pes', 'Peso'))),
     r'$\bar x=\frac{975}{6}=162{,}5$ cm, \ $\bar y=\frac{344}{6}\approx57{,}33$ kg: \ $\res{(162{,}5;\ 57{,}33)}$.' + center(nuvol(list(zip(AX, AY)), (145, 180, 5), (40, 75, 5), lx='cm', ly='kg', cg=True))),
 (2, T(r"Dibuixa el núvol de punts de la taula de l'exercici 3. Escriu al costat de cada punt la seua freqüència. Quin és el centre de gravetat?", r"Dibuja la nube de puntos de la tabla del ejercicio 3. Escribe al lado de cada punto su frecuencia. ¿Cuál es el centro de gravedad?"),
     center(nuvol([(x, y) for x in X3 for y in Y3], (0, 3, 1), (0, 3, 1), lab=['$%d$' % F3[i][j] for i in range(3) for j in range(3)], W=3.2, H=3.0))
     + T(r"Amb les mitjanes de l'exercici 5: $\res{(1;\ 0{,}87)}$.", r"Con las medias del ejercicio 5: $\res{(1;\ 0{,}87)}$.")),
 (2, T(r"En una distribució de 5 parelles, quatre són $%s$ i el centre de gravetat és $(4{,}2;\ 5)$. Troba la parella que falta.", r"En una distribución de 5 parejas, cuatro son $%s$ y el centro de gravedad es $(4{,}2;\ 5)$. Encuentra la pareja que falta.") % pairs(*zip(*P11)),
     T(r"Les $x$ han de sumar $5\cdot4{,}2=21$ i les $y$, $5\cdot5=25$: \ $x=21-16=5$, \ $y=25-20=5$: \ $\res{(5,\ 5)}$.", r"Las $x$ tienen que sumar $5\cdot4{,}2=21$ y las $y$, $5\cdot5=25$: \ $x=21-16=5$, \ $y=25-20=5$: \ $\res{(5,\ 5)}$.")),
 (3, T(r"Quin punt s'ha d'afegir a $%s$ perquè el centre de gravetat no canvie? I perquè passe a ser $(5,\ 6)$?", r"¿Qué punto hay que añadir a $%s$ para que el centro de gravedad no cambie? ¿Y para que pase a ser $(5,\ 6)$?") % pairs(*zip(*P12)),
     T(r"Ara és $(\frac{12}{3},\frac{15}{3})=(4,\ 5)$. Si afegim el mateix punt $\res{(4,\ 5)}$, les mitjanes no canvien. Per a $(5,\ 6)$ amb 4 punts, les $x$ han de sumar $20$ i les $y$, $24$: hem d'afegir $\res{(8,\ 9)}$.",
       r"Ahora es $(\frac{12}{3},\frac{15}{3})=(4,\ 5)$. Si añadimos el mismo punto $\res{(4,\ 5)}$, las medias no cambian. Para $(5,\ 6)$ con 4 puntos, las $x$ tienen que sumar $20$ y las $y$, $24$: hay que añadir $\res{(8,\ 9)}$.")),
]))
EQ(sum(AX), 975); EQ(sum(AY), 344); CHK(bi(*zip(*(P11 + [(5, 5)])))['mx'] == Fr(21, 5)); CHK(bi(*zip(*(P12 + [(4, 5)])))['my'] == 5)
S12b = bi(*zip(*(P12 + [(8, 9)]))); CHK((S12b['mx'], S12b['my']) == (5, 6))

# =====================================================================
# 3. Correlació
# =====================================================================
C13 = [(0.95, 3), (-0.6, 21), (0.0, 9), (0.6, 5), (-0.95, 4)]
G13 = {r: gen(30, r, s) for r, s in C13}
for r, s in C13: AP(rfl(G13[r]), r)
PAR = [(x, 9 - 0.35 * (x - 5) ** 2 + 0.6 * (random.Random(i).random() * 2 - 1)) for i, x in enumerate([0.6 + 0.37 * k for k in range(24)])]
C15 = [(0.9, 31), (-0.9, 32), (0.4, 33), (0.0, 34)]; G15 = {r: gen(25, r, s) for r, s in C15}
for r, s in C15: AP(rfl(G15[r]), r)
O15 = [(-0.9, 'A'), (0.4, 'B'), (0.9, 'C'), (0.0, 'D')]
X16 = [1, 2, 3, 4, 5]; Y16 = [50, 44, 40, 32, 24]
S_.append((T("Correlació", "Correlación"), [
 (1, T(r"Descriu la correlació (sentit i força) de cada núvol de punts:", r"Describe la correlación (sentido y fuerza) de cada nube de puntos:")
     + recorda(T(r"\textbf{Sentit}: positiva si el núvol puja, negativa si baixa, nul·la si ni puja ni baixa. \textbf{Força}: forta si els punts estan prop d'una recta, feble si estan escampats.", r"\textbf{Sentido}: positiva si la nube sube, negativa si baja, nula si ni sube ni baja. \textbf{Fuerza}: fuerte si los puntos están cerca de una recta, débil si están dispersos."))
     + center(nv(G13[0.95], 'A') + r'\quad ' + nv(G13[-0.6], 'B') + r'\quad ' + nv(G13[0.0], 'C')) + center(nv(G13[0.6], 'D') + r'\quad ' + nv(G13[-0.95], 'E') + r'\quad ' + nv(PAR, 'F')),
     tasks(3, [T(r"\rest{Positiva i forta}", r"\rest{Positiva y fuerte}"), T(r"\rest{Negativa i feble}", r"\rest{Negativa y débil}"), T(r"\rest{Nul·la}", r"\rest{Nula}"),
               T(r"\rest{Positiva i feble}", r"\rest{Positiva y débil}"), T(r"\rest{Negativa i forta}", r"\rest{Negativa y fuerte}"), T(r"\rest{No lineal}: els punts segueixen una corba (paràbola).", r"\rest{No lineal}: los puntos siguen una curva (parábola).")])),
 (1, T(r"Quina correlació (positiva, negativa o nul·la) esperes entre aquestes variables?", r"¿Qué correlación (positiva, negativa o nula) esperas entre estas variables?")
     + tasks(2, [T("Temperatura i consum de calefacció.", "Temperatura y consumo de calefacción."), T("Hores d'entrenament i marca en una cursa de 100 m.", "Horas de entrenamiento y marca en una carrera de 100 m."),
                 T("Superfície d'un pis i preu.", "Superficie de un piso y precio."), T("Edat i nombre de dents d'un xiquet de 2 a 6 anys.", "Edad y número de dientes de un niño de 2 a 6 años."),
                 T("Número de telèfon i alçada.", "Número de teléfono y altura."), T("Velocitat d'un cotxe i temps per a fer un trajecte.", "Velocidad de un coche y tiempo para hacer un trayecto.")]),
     tasks(2, [T(r"\rest{Negativa}", r"\rest{Negativa}"), T(r"\rest{Negativa} (menys temps)", r"\rest{Negativa} (menos tiempo)"), T(r"\rest{Positiva}", r"\rest{Positiva}"),
               T(r"\rest{Positiva}", r"\rest{Positiva}"), T(r"\rest{Nul·la}", r"\rest{Nula}"), T(r"\rest{Negativa}", r"\rest{Negativa}")])),
 (1, T(r"Associa cada núvol amb el seu coeficient de correlació: $r=0{,}9$; \ $r=-0{,}9$; \ $r=0{,}4$; \ $r=0$.", r"Asocia cada nube con su coeficiente de correlación: $r=0{,}9$; \ $r=-0{,}9$; \ $r=0{,}4$; \ $r=0$.")
     + center(r'\quad '.join(nv(G15[r], t) for r, t in O15)),
     tasks(4, [r'A: $\res{r=-0{,}9}$', r'B: $\res{r=0{,}4}$', r'C: $\res{r=0{,}9}$', r'D: $\res{r=0}$'])),
 (2, T(r"Una botiga ha provat cinc preus (€) per a un producte i ha apuntat les unitats venudes en una setmana. Dibuixa el núvol de punts i descriu-ne la correlació.", r"Una tienda ha probado cinco precios (€) para un producto y ha apuntado las unidades vendidas en una semana. Dibuja la nube de puntos y describe su correlación.")
     + center(ptab(X16, Y16, T('Preu (€)', 'Precio (€)'), T('Unitats', 'Unidades'))),
     center(nuvol(list(zip(X16, Y16)), (0, 6, 1), (0, 60, 10), lx='€', ly=T('unitats', 'unidades'))) + T(r"Els punts baixen i estan quasi en una recta: correlació \rest{negativa i forta}.", r"Los puntos bajan y están casi en una recta: correlación \rest{negativa y fuerte}.")),
 (2, T(r"En els incendis en què treballen més bombers hi ha més danys. Vol dir això que els bombers causen els danys? Explica-ho.", r"En los incendios en los que trabajan más bomberos hay más daños. ¿Quiere decir esto que los bomberos causan los daños? Explícalo."),
     T(r"\rest{No}. Hi ha correlació positiva, però no és causa-efecte: les dues variables depenen d'una tercera, la \textbf{grandària de l'incendi}. Com més gran és, més bombers hi van i més danys hi ha.", r"\rest{No}. Hay correlación positiva, pero no es causa-efecto: las dos variables dependen de una tercera, el \textbf{tamaño del incendio}. Cuanto más grande es, más bomberos van y más daños hay.")),
 (3, T(r"Inventa cinc parelles de dades amb una correlació negativa i forta, i cinc més amb correlació nul·la. Dibuixa'n els núvols.", r"Inventa cinco parejas de datos con una correlación negativa y fuerte, y cinco más con correlación nula. Dibuja sus nubes."),
     T(r"Per exemple, negativa i forta: $(1,\,9),\ (2,\,8),\ (3,\,6),\ (4,\,5),\ (5,\,2)$ (els punts baixen quasi en línia recta). Nul·la: $(1,\,3),\ (2,\,7),\ (3,\,1),\ (4,\,6),\ (5,\,3)$ (no pugen ni baixen). Hi ha moltes altres respostes.",
       r"Por ejemplo, negativa y fuerte: $(1,\,9),\ (2,\,8),\ (3,\,6),\ (4,\,5),\ (5,\,2)$ (los puntos bajan casi en línea recta). Nula: $(1,\,3),\ (2,\,7),\ (3,\,1),\ (4,\,6),\ (5,\,3)$ (no suben ni bajan). Hay muchas otras respuestas.")
     + side(nuvol([(1, 9), (2, 8), (3, 6), (4, 5), (5, 2)], (0, 6, 1), (0, 10, 2), W=3.2, H=2.6), nuvol([(1, 3), (2, 7), (3, 1), (4, 6), (5, 3)], (0, 6, 1), (0, 10, 2), W=3.2, H=2.6))),
 (3, T(r"Les notes de matemàtiques i de física de 8 alumnes són $(4,\,5),\ \allowbreak (5,\,5),\ \allowbreak (6,\,7),\ \allowbreak (7,\,6),\ \allowbreak (8,\,8),\ \allowbreak (9,\,9),\ \allowbreak (3,\,4)$ i $(9,\,2)$. Dibuixa el núvol. Quin punt trenca la tendència? Com seria la correlació sense eixe punt?", r"Las notas de matemáticas y de física de 8 alumnos son $(4,\,5),\ \allowbreak (5,\,5),\ \allowbreak (6,\,7),\ \allowbreak (7,\,6),\ \allowbreak (8,\,8),\ \allowbreak (9,\,9),\ \allowbreak (3,\,4)$ y $(9,\,2)$. Dibuja la nube. ¿Qué punto rompe la tendencia? ¿Cómo sería la correlación sin ese punto?"),
     center(nuvol([(4, 5), (5, 5), (6, 7), (7, 6), (8, 8), (9, 9), (3, 4), (9, 2)], (0, 10, 1), (0, 10, 1), lx=T('mat.', 'mat.'), ly=T('física', 'física')))
     + T(r"El punt $\res{(9,\,2)}$ és una dada atípica. Amb ell la correlació és positiva però feble ($r\approx%s$); sense ell, és \rest{positiva i forta} ($r\approx%s$).", r"El punto $\res{(9,\,2)}$ es un dato atípico. Con él la correlación es positiva pero débil ($r\approx%s$); sin él, es \rest{positiva y fuerte} ($r\approx%s$).")
       % (rd(bi([4, 5, 6, 7, 8, 9, 3, 9], [5, 5, 7, 6, 8, 9, 4, 2])['r']), rd(bi([4, 5, 6, 7, 8, 9, 3], [5, 5, 7, 6, 8, 9, 4])['r']))),
]))
r17a = bi([4, 5, 6, 7, 8, 9, 3, 9], [5, 5, 7, 6, 8, 9, 4, 2])['r']; r17b = bi([4, 5, 6, 7, 8, 9, 3], [5, 5, 7, 6, 8, 9, 4])['r']
CHK(0 < r17a < 0.5 and r17b > 0.9, r17a, r17b)
CHK(bi([1, 2, 3, 4, 5], [9, 8, 6, 5, 2])['r'] < -0.95 and abs(bi([1, 2, 3, 4, 5], [3, 7, 1, 6, 3])['r']) < 0.1)
CHK(bi(X16, Y16)['r'] < -0.98)

# =====================================================================
# 4. Coeficient de correlació
# =====================================================================
X24 = [1, 2, 3, 4, 5]; Y24 = [1, 3, 2, 5, 4]; S24, R24 = passos_r(X24, Y24)
CHK((S24['sxy'], S24['vx'], S24['vy'], S24['c']) == (53, 2, 2, Fr(8, 5))); AP(S24['r'], '0.8')
X25 = [2, 4, 6, 8, 10]; Y25 = [9, 7, 6, 4, 4]; S25, R25 = passos_r(X25, Y25)
CHK((S25['mx'], S25['my'], S25['vx'], S25['c']) == (6, 6, 8, Fr(-26, 5))); AP(S25['r'], '-0.97')
S27, R27 = passos_r(DK, DM, xl='km', yl='min'); AP(S27['r'], '0.99')
GX = [14, 18, 20, 23, 25, 28, 30, 32]; GY = [20, 35, 40, 60, 65, 80, 95, 105]
S_.append((T("Coeficient de correlació", "Coeficiente de correlación"), [
 (1, T(r"Digues quin tipus de correlació indica cada coeficient:", r"Di qué tipo de correlación indica cada coeficiente:")
     + recorda(T(r"$-1\le r\le1$. El \textbf{signe} de $r$ diu el sentit i $|r|$, la força: $|r|\ge0{,}8$ forta; $0{,}5\le|r|<0{,}8$ moderada; $|r|<0{,}5$ feble; $r\approx0$ nul·la.", r"$-1\le r\le1$. El \textbf{signo} de $r$ dice el sentido y $|r|$, la fuerza: $|r|\ge0{,}8$ fuerte; $0{,}5\le|r|<0{,}8$ moderada; $|r|<0{,}5$ débil; $r\approx0$ nula."))
     + tasks(6, [r'$r=0{,}87$', r'$r=-0{,}35$', r'$r=0{,}02$', r'$r=-0{,}96$', r'$r=0{,}61$', r'$r=1$']),
     tasks(3, [T(r"\rest{Positiva i forta}", r"\rest{Positiva y fuerte}"), T(r"\rest{Negativa i feble}", r"\rest{Negativa y débil}"), T(r"\rest{Nul·la}", r"\rest{Nula}"),
               T(r"\rest{Negativa i forta}", r"\rest{Negativa y fuerte}"), T(r"\rest{Positiva moderada}", r"\rest{Positiva moderada}"), T(r"\rest{Positiva perfecta}", r"\rest{Positiva perfecta}")])),
 (1, T(r"Calcula el coeficient de correlació i digues com és la correlació:", r"Calcula el coeficiente de correlación y di cómo es la correlación:")
     + recorda(T(r"$\sigma_{xy}=\frac{\sum x_iy_i}{N}-\bar x\cdot\bar y$ \quad i \quad $r=\frac{\sigma_{xy}}{\sigma_x\cdot\sigma_y}$.", r"$\sigma_{xy}=\frac{\sum x_iy_i}{N}-\bar x\cdot\bar y$ \quad y \quad $r=\frac{\sigma_{xy}}{\sigma_x\cdot\sigma_y}$."))
     + tasks(1, [r'$\sigma_{xy}=-6$, \ $\sigma_x=2{,}5$, \ $\sigma_y=3$', r'$N=8$, \ $\sum x_iy_i=210$, \ $\bar x=4$, \ $\bar y=6$, \ $\sigma_x=2$, \ $\sigma_y=3$', r'$N=10$, \ $\sum x_iy_i=420$, \ $\bar x=5$, \ $\bar y=8$, \ $\sigma_x=1{,}5$, \ $\sigma_y=2{,}2$']),
     tasks(1, [r'$r=\frac{-6}{2{,}5\cdot3}=\frac{-6}{7{,}5}=\res{-0{,}8}$: ' + T('negativa i forta.', 'negativa y fuerte.'),
               r'$\sigma_{xy}=\frac{210}{8}-24=2{,}25$; \ $r=\frac{2{,}25}{6}=\res{0{,}375}$: ' + T('positiva i feble.', 'positiva y débil.'),
               r'$\sigma_{xy}=\frac{420}{10}-40=2$; \ $r=\frac{2}{3{,}3}\approx\res{0{,}61}$: ' + T('positiva moderada.', 'positiva moderada.')])),
 (2, T(r"Calcula el coeficient de correlació de la distribució $%s$ i interpreta'l.", r"Calcula el coeficiente de correlación de la distribución $%s$ e interprétalo.") % pairs(X24, Y24),
     R24 + '. ' + T(r"Correlació \rest{positiva i forta}.", r"Correlación \rest{positiva y fuerte}.")),
 (2, T(r"Calcula el coeficient de correlació de la distribució $%s$ i interpreta'l.", r"Calcula el coeficiente de correlación de la distribución $%s$ e interprétalo.") % pairs(X25, Y25),
     R25 + '. ' + T(r"Correlació \rest{negativa i forta}.", r"Correlación \rest{negativa y fuerte}.")),
 (2, T(r"Calcula el coeficient de correlació entre la distància i el temps de l'exercici 2. Coincideix amb el que esperaves?", r"Calcula el coeficiente de correlación entre la distancia y el tiempo del ejercicio 2. ¿Coincide con lo que esperabas?"),
     R27 + '. ' + T(r"Sí: correlació \rest{positiva i molt forta}, encara que no és funcional.", r"Sí: correlación \rest{positiva y muy fuerte}, aunque no es funcional.")),
 (3, T(r"Totes les parelles d'una distribució compleixen $y=-3x+2$. Quant val $r$? I si compleixen $y=5$ (amb valors de $x$ diferents)?", r"Todas las parejas de una distribución cumplen $y=-3x+2$. ¿Cuánto vale $r$? ¿Y si cumplen $y=5$ (con valores de $x$ distintos)?"),
     T(r"Si estan en una recta que baixa, la correlació és negativa perfecta: $\res{r=-1}$. Si totes tenen $y=5$, $Y$ no varia ($\sigma_y=0$) i \rest{no es pot calcular} $r$: $Y$ no depén de $X$.", r"Si están en una recta que baja, la correlación es negativa perfecta: $\res{r=-1}$. Si todas tienen $y=5$, $Y$ no varía ($\sigma_y=0$) y \rest{no se puede calcular} $r$: $Y$ no depende de $X$.")),
 (3, T(r"Multiplica per 10 tots els valors de $x$ de l'exercici 22 i calcula de nou $r$. Què observes? Per què passa?", r"Multiplica por 10 todos los valores de $x$ del ejercicio 22 y calcula de nuevo $r$. ¿Qué observas? ¿Por qué pasa?"),
     T(r"Amb $x=10,20,30,40,50$: $\sigma_x=10\sqrt2$, $\sigma_{xy}=16$ (també es multiplica per 10) i $r=\frac{16}{10\sqrt2\cdot\sqrt2}=\res{0{,}8}$, \textbf{igual}. Canviar d'unitats (de cm a mm, per exemple) no canvia la forma del núvol i, per tant, tampoc $r$.",
       r"Con $x=10,20,30,40,50$: $\sigma_x=10\sqrt2$, $\sigma_{xy}=16$ (también se multiplica por 10) y $r=\frac{16}{10\sqrt2\cdot\sqrt2}=\res{0{,}8}$, \textbf{igual}. Cambiar de unidades (de cm a mm, por ejemplo) no cambia la forma de la nube y, por tanto, tampoco $r$.")),
]))
EQ(Fr(-6) / Fr('7.5'), '-0.8'); EQ(Fr(210, 8) - 24, '2.25'); EQ(Fr(9, 4) / 6, '0.375'); EQ(Fr(420, 10) - 40, 2); AP(Fr(2) / Fr('3.3'), '0.61')
S29 = bi([10 * x for x in X24], Y24); CHK(S29['c'] == 16 and S29['vx'] == 200); AP(S29['r'], '0.8')

# =====================================================================
# 5. Recta de regressió
# =====================================================================
S33 = bi(X7, Y7); CHK((S33['vx'], S33['c']) == (Fr(35, 12), Fr(31, 12)))
S_.append((T("Recta de regressió", "Recta de regresión"), [
 (1, T(r"Escriu la recta de regressió en cada cas:", r"Escribe la recta de regresión en cada caso:")
     + recorda(T(r"$y-\bar y=\frac{\sigma_{xy}}{\sigma_x^2}\,(x-\bar x)$: passa pel centre de gravetat i té pendent $m=\frac{\sigma_{xy}}{\sigma_x^2}$.", r"$y-\bar y=\frac{\sigma_{xy}}{\sigma_x^2}\,(x-\bar x)$: pasa por el centro de gravedad y tiene pendiente $m=\frac{\sigma_{xy}}{\sigma_x^2}$."))
     + tasks(2, [r'$\bar x=5$, \ $\bar y=8$, \ $\sigma_x^2=4$, \ $\sigma_{xy}=6$', r'$\bar x=10$, \ $\bar y=20$, \ $\sigma_x^2=5$, \ $\sigma_{xy}=-4$']),
     tasks(1, [r'$m=\frac{6}{4}=1{,}5$; \ $y-8=1{,}5(x-5)\Rightarrow\res{y=1{,}5x+0{,}5}$', r'$m=\frac{-4}{5}=-0{,}8$; \ $y-20=-0{,}8(x-10)\Rightarrow\res{y=-0{,}8x+28}$'])),
 (1, T(r"El centre de gravetat d'un núvol és $(3,\,7)$. Quina d'aquestes rectes pot ser la seua recta de regressió? \quad $y=2x+3$; \quad $y=2x+1$; \quad $y=-x+4$.", r"El centro de gravedad de una nube es $(3,\,7)$. ¿Cuál de estas rectas puede ser su recta de regresión? \quad $y=2x+3$; \quad $y=2x+1$; \quad $y=-x+4$."),
     T(r"Ha de passar per $(3,\,7)$: $2\cdot3+3=9$, \ $2\cdot3+1=7$, \ $-3+4=1$. Només $\res{y=2x+1}$.", r"Tiene que pasar por $(3,\,7)$: $2\cdot3+3=9$, \ $2\cdot3+1=7$, \ $-3+4=1$. Solo $\res{y=2x+1}$.")),
 (2, T(r"Calcula la recta de regressió de la distribució de l'exercici 22 i dibuixa-la sobre el núvol de punts.", r"Calcula la recta de regresión de la distribución del ejercicio 22 y dibújala sobre la nube de puntos."),
     T(r"Amb $\bar x=3$, $\bar y=3$, $\sigma_x^2=2$ i $\sigma_{xy}=1{,}6$: ", r"Con $\bar x=3$, $\bar y=3$, $\sigma_x^2=2$ y $\sigma_{xy}=1{,}6$: ") + passos_recta(S24) + '.'
     + center(nuvol(list(zip(X24, Y24)), (0, 6, 1), (0, 6, 1), cg=True, reg=(S24['m'], S24['n'])))),
 (2, T(r"Calcula la recta de regressió de la distribució de l'exercici 23. Què indica el pendent?", r"Calcula la recta de regresión de la distribución del ejercicio 23. ¿Qué indica la pendiente?"),
     T(r"Amb $\bar x=6$, $\bar y=6$, $\sigma_x^2=8$ i $\sigma_{xy}=-5{,}2$: ", r"Con $\bar x=6$, $\bar y=6$, $\sigma_x^2=8$ y $\sigma_{xy}=-5{,}2$: ") + passos_recta(S25) + '. '
     + T(r"Quan $x$ augmenta 1 unitat, $y$ disminueix, de mitjana, $0{,}65$ unitats.", r"Cuando $x$ aumenta 1 unidad, $y$ disminuye, de media, $0{,}65$ unidades.")),
 (2, T(r"Calcula el coeficient de correlació i la recta de regressió del preu i les unitats venudes de l'exercici 16. Què vol dir el pendent?", r"Calcula el coeficiente de correlación y la recta de regresión del precio y las unidades vendidas del ejercicio 16. ¿Qué quiere decir la pendiente?"),
     passos_r(X16, Y16, xl=T('Preu', 'Precio'), yl=T('Unitats', 'Unidades'))[1] + '. ' + passos_recta(bi(X16, Y16)) + '. '
     + T(r"Per cada euro que puja el preu, es venen unes $6{,}4$ unitats menys.", r"Por cada euro que sube el precio, se venden unas $6{,}4$ unidades menos.")),
 (2, T(r"Dibuixa el núvol de l'exercici 7, traça-hi a ull una recta que s'hi ajuste (que passe pel centre de gravetat) i escriu-ne l'equació. Després calcula la recta de regressió i compara-les.", r"Dibuja la nube del ejercicio 7, traza a ojo una recta que se ajuste (que pase por el centro de gravedad) y escribe su ecuación. Después calcula la recta de regresión y compáralas."),
     T(r"Una recta a ull pot ser la que passa per $(3{,}5;\ 4{,}5)$ i $(0;\ 1{,}5)$: $y\approx0{,}86x+1{,}5$ (discontínua). Amb la fórmula: $\sigma_x^2=\frac{91}{6}-3{,}5^2\approx2{,}92$, \ $\sigma_{xy}=\frac{110}{6}-3{,}5\cdot4{,}5\approx2{,}58$; ",
       r"Una recta a ojo puede ser la que pasa por $(3{,}5;\ 4{,}5)$ y $(0;\ 1{,}5)$: $y\approx0{,}86x+1{,}5$ (discontinua). Con la fórmula: $\sigma_x^2=\frac{91}{6}-3{,}5^2\approx2{,}92$, \ $\sigma_{xy}=\frac{110}{6}-3{,}5\cdot4{,}5\approx2{,}58$; ")
     + r'$m=\frac{2{,}58\ldots}{2{,}92\ldots}\approx0{,}89$; \ $y-4{,}5=0{,}89(x-3{,}5)\Rightarrow\res{y\approx0{,}89x+1{,}4}$. ' + T('Són molt semblants.', 'Son muy parecidas.')
     + center(nuvol(list(zip(X7, Y7)), (0, 7, 1), (0, 8, 1), cg=True, reg=(S33['m'], S33['n']), eye=(Fr(6, 7), Fr(3, 2))))),
 (3, T(r"La recta de regressió d'una distribució és $y=-1{,}5x+20$ i $\bar y=11$. Quant val $\bar x$? La correlació és positiva o negativa?", r"La recta de regresión de una distribución es $y=-1{,}5x+20$ e $\bar y=11$. ¿Cuánto vale $\bar x$? ¿La correlación es positiva o negativa?"),
     T(r"Passa per $(\bar x,\,11)$: $11=-1{,}5\bar x+20\Rightarrow\bar x=\frac{9}{1{,}5}=\res{6}$. El pendent és negatiu, i $r$ té el mateix signe: correlació \rest{negativa}.", r"Pasa por $(\bar x,\,11)$: $11=-1{,}5\bar x+20\Rightarrow\bar x=\frac{9}{1{,}5}=\res{6}$. La pendiente es negativa, y $r$ tiene el mismo signo: correlación \rest{negativa}.")),
 (3, T(r"D'una distribució sabem que $r=0{,}8$, $\sigma_x=2$, $\sigma_y=5$, $\bar x=10$ i $\bar y=30$. Troba la covariància i la recta de regressió.", r"De una distribución sabemos que $r=0{,}8$, $\sigma_x=2$, $\sigma_y=5$, $\bar x=10$ e $\bar y=30$. Encuentra la covarianza y la recta de regresión."),
     T(r"De $r=\frac{\sigma_{xy}}{\sigma_x\sigma_y}$: $\sigma_{xy}=0{,}8\cdot2\cdot5=\res{8}$. \ $m=\frac{8}{2^2}=2$; \ $y-30=2(x-10)\Rightarrow\res{y=2x+10}$.", r"De $r=\frac{\sigma_{xy}}{\sigma_x\sigma_y}$: $\sigma_{xy}=0{,}8\cdot2\cdot5=\res{8}$. \ $m=\frac{8}{2^2}=2$; \ $y-30=2(x-10)\Rightarrow\res{y=2x+10}$.")),
]))
CHK((S24['m'], S24['n']) == (Fr(4, 5), Fr(3, 5))); CHK((S25['m'], S25['n']) == (Fr(-13, 20), Fr(99, 10)))
S16 = bi(X16, Y16); CHK((S16['m'], S16['n']) == (Fr(-32, 5), Fr(286, 5)))
CHK((S33['sx2'], S33['sxy']) == (91, 110)); AP(S33['vx'], '2.92'); AP(S33['c'], '2.58'); AP(S33['m'], '0.89'); AP(S33['n'], '1.4', 1)
EQ(Fr(9) / Fr('1.5'), 6); EQ(Fr('0.8') * 10, 8)

# =====================================================================
# 6. Estimacions
# =====================================================================
SG = bi(GX, GY); AP(SG['r'], '0.99'); AP(SG['m'], '4.79'); AP(SG['n'], '-51.18')
CX = [1, 2, 3, 5, 9]; CY = [19, 17, 15, 12, 7]; SC = bi(CX, CY)
CHK((SC['mx'], SC['my'], SC['vx'], SC['c'], SC['m'], SC['n']) == (4, 14, 8, Fr(-59, 5), Fr(-59, 40), Fr(199, 10)))
S_.append((T("Estimacions", "Estimaciones"), [
 (1, T(r"La recta de regressió d'una distribució és $y=2{,}5x+10$ i $r=0{,}92$. Les dades de $x$ van de 2 a 9. Estima el valor de $y$ per a $x=4$ i per a $x=6{,}2$.", r"La recta de regresión de una distribución es $y=2{,}5x+10$ y $r=0{,}92$. Los datos de $x$ van de 2 a 9. Estima el valor de $y$ para $x=4$ y para $x=6{,}2$.")
     + recorda(T(r"L'estimació és $\hat y=m\cdot x_0+n$. És fiable si $|r|$ és pròxim a 1 i $x_0$ està dins de les dades.", r"La estimación es $\hat y=m\cdot x_0+n$. Es fiable si $|r|$ está cerca de 1 y $x_0$ está dentro de los datos.")),
     r'$\hat y(4)=2{,}5\cdot4+10=\res{20}$; \ $\hat y(6{,}2)=2{,}5\cdot6{,}2+10=\res{25{,}5}$. ' + T('Totes dues són fiables.', 'Las dos son fiables.')),
 (1, T(r"Digues si aquestes estimacions són fiables i per què:", r"Di si estas estimaciones son fiables y por qué:")
     + tasks(1, [T(r"$r=0{,}96$; les dades de $x$ van de 10 a 30 i estimem per a $x=18$.", r"$r=0{,}96$; los datos de $x$ van de 10 a 30 y estimamos para $x=18$."), T(r"$r=0{,}28$; estimem per a un valor de $x$ dins de les dades.", r"$r=0{,}28$; estimamos para un valor de $x$ dentro de los datos."),
                 T(r"$r=-0{,}91$; les dades de $x$ van de 1 a 6 i estimem per a $x=40$.", r"$r=-0{,}91$; los datos de $x$ van de 1 a 6 y estimamos para $x=40$."), T(r"$r=-0{,}85$; estimem per a $x=\bar x$.", r"$r=-0{,}85$; estimamos para $x=\bar x$.")]),
     tasks(1, [T(r"\rest{Sí}: correlació forta i interpolació.", r"\rest{Sí}: correlación fuerte e interpolación."), T(r"\rest{No}: correlació feble.", r"\rest{No}: correlación débil."),
               T(r"\rest{No}: extrapolació molt lluny de les dades.", r"\rest{No}: extrapolación muy lejos de los datos."), T(r"\rest{Sí}: $|r|=0{,}85$ i $\bar x$ és al centre de les dades (l'estimació és $\bar y$).", r"\rest{Sí}: $|r|=0{,}85$ y $\bar x$ está en el centro de los datos (la estimación es $\bar y$).")])),
 (2, T(r"Amb la recta de l'exercici 29, estima $y$ per a $x=3{,}5$ i per a $x=20$. Són fiables?", r"Con la recta del ejercicio 29, estima $y$ para $x=3{,}5$ y para $x=20$. ¿Son fiables?"),
     r'$\hat y(3{,}5)=0{,}8\cdot3{,}5+0{,}6=\res{3{,}4}$: ' + T(r'fiable ($r=0{,}8$ i $x$ dins de les dades). ', r'fiable ($r=0{,}8$ y $x$ dentro de los datos). ')
     + r'$\hat y(20)=0{,}8\cdot20+0{,}6=\res{16{,}6}$: ' + T(r'\rest{no fiable}: 20 està molt lluny de les dades (d\textquotesingle1 a 5).', r'\rest{no fiable}: 20 está muy lejos de los datos (de 1 a 5).')),
 (2, T(r"Amb les dades de l'exercici 2, troba la recta de regressió i estima quant tardarà un alumne que viu a 7 km. I un que viu a 50 km?", r"Con los datos del ejercicio 2, encuentra la recta de regresión y estima cuánto tardará un alumno que vive a 7 km. ¿Y uno que vive a 50 km?"),
     T(r"Amb els paràmetres de l'exercici 24: ", r"Con los parámetros del ejercicio 24: ") + passos_recta(S27) + '. '
     + r'$\hat y(7)\approx%s$ min ' % rd(S27['m'] * 7 + S27['n'], 1) + T(r'(fiable). ', r'(fiable). ')
     + r'$\hat y(50)\approx%s$ min: ' % rd(S27['m'] * 50 + S27['n'], 0) + T(r'\rest{no és fiable}: una persona que viu a 50 km no hi va caminant o en bici, sinó en autobús o en cotxe.', r'\rest{no es fiable}: una persona que vive a 50 km no va andando o en bici, sino en autobús o en coche.')),
 (2, T(r"Amb la recta $y=-6{,}4x+57{,}2$ de l'exercici 31 ($r\approx-0{,}99$), a quin preu cal vendre el producte per a vendre'n 40 unitats?", r"Con la recta $y=-6{,}4x+57{,}2$ del ejercicio 31 ($r\approx-0{,}99$), ¿a qué precio hay que vender el producto para vender 40 unidades?"),
     r'$40=-6{,}4x+57{,}2\Rightarrow6{,}4x=17{,}2\Rightarrow x=\frac{17{,}2}{6{,}4}\approx\res{2{,}69\ \text{€}}$. ' + T(r'Com que la correlació és molt forta, l\textquotesingle estimació és bona.', r'Como la correlación es muy fuerte, la estimación es buena.')),
 (3, T(r"Una gelateria ha apuntat la temperatura màxima (°C) i els gelats venuts durant 8 dies:", r"Una heladería ha apuntado la temperatura máxima (°C) y los helados vendidos durante 8 días:") + center(ptab(GX, GY, T('Temperatura', 'Temperatura'), T('Gelats', 'Helados'), w='0.7cm'))
     + tasks(1, [T(r"Calcula el coeficient de correlació i interpreta'l.", r"Calcula el coeficiente de correlación e interprétalo."), T(r"Troba la recta de regressió.", r"Encuentra la recta de regresión."),
                 T(r"Quants gelats esperen vendre un dia a 27 °C? I un dia a 40 °C? Quina estimació és més fiable?", r"¿Cuántos helados esperan vender un día a 27 °C? ¿Y un día a 40 °C? ¿Qué estimación es más fiable?")]),
     tasks(1, [passos_r(GX, GY, xl='$x_i$ (°C)', yl=T('$y_i$ (gelats)', '$y_i$ (helados)'))[1] + '. ' + T(r'Positiva i molt forta.', r'Positiva y muy fuerte.'),
               passos_recta(SG),
               r'$\hat y(27)\approx\res{78}$ ' + T('gelats', 'helados') + r'; \ $\hat y(40)\approx\res{140}$. ' + T(r"La de 27 °C, que està dins de les dades (de 14 a 32 °C); la de 40 °C és una extrapolació.", r"La de 27 °C, que está dentro de los datos (de 14 a 32 °C); la de 40 °C es una extrapolación.")
               + center(nuvol(list(zip(GX, GY)), (10, 45, 5), (0, 160, 20), lx='°C', ly=T('gelats', 'helados'), reg=(SG['m'], SG['n']), est=(27, SG['m'] * 27 + SG['n'])))])),
 (3, T(r"L'edat (anys) i el preu (milers d'euros) de cinc cotxes de segona mà del mateix model són:", r"La edad (años) y el precio (miles de euros) de cinco coches de segunda mano del mismo modelo son:") + center(ptab(CX, CY, T('Edat', 'Edad'), T('Preu', 'Precio')))
     + tasks(1, [T(r"Calcula el coeficient de correlació i la recta de regressió.", r"Calcula el coeficiente de correlación y la recta de regresión."), T(r"Estima el preu d'un cotxe de 6 anys i el d'un de 20 anys. Té sentit el segon resultat?", r"Estima el precio de un coche de 6 años y el de uno de 20 años. ¿Tiene sentido el segundo resultado?")]),
     tasks(1, [passos_r(CX, CY)[1] + '. ' + passos_recta(SC),
               r'$\hat y(6)\approx%s$ ' % rd(SC['m'] * 6 + SC['n']) + T(r'milers d\textquotesingle euros, uns $\res{11\,050}$ €. ', r'miles de euros, unos $\res{11\,050}$ €. ')
               + r'$\hat y(20)\approx%s$: ' % rd(SC['m'] * 20 + SC['n']) + T(r'\rest{un preu negatiu, que no té sentit}: és una extrapolació massa llunyana (els cotxes no perden valor sempre al mateix ritme).', r'\rest{un precio negativo, que no tiene sentido}: es una extrapolación demasiado lejana (los coches no pierden valor siempre al mismo ritmo).')])),
]))
EQ(Fr('2.5') * 4 + 10, 20); EQ(Fr('2.5') * Fr('6.2') + 10, '25.5'); EQ(Fr('0.8') * Fr('3.5') + Fr('0.6'), '3.4'); EQ(Fr('0.8') * 20 + Fr('0.6'), '16.6')
AP(Fr('17.2') / Fr('6.4'), '2.69'); AP(SG['m'] * 27 + SG['n'], 78, 0); AP(SG['m'] * 40 + SG['n'], 140, 0)
EQ(SC['m'] * 6 + SC['n'], '11.05'); EQ(SC['m'] * 20 + SC['n'], '-9.6'); AP(SC['r'], '-0.99')

# referències creuades entre exercicis (numeració global)
n = sum(len(e) for _t, e in S_)
starts = [1]
for _t, _e in S_[:-1]: starts.append(starts[-1] + len(_e))
assert starts == [1, 7, 13, 20, 27, 35], starts  # referències: 2, 3, 5 i 7 (seccions 1-2), 16 (secció 3), 22-24 (secció 4), 29 i 31 (secció 5)
assert n == 41, n

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("estadística bidimensional, distribucions bidimensionals, taula de doble entrada, núvol de punts, centre de gravetat, correlació, covariància, coeficient de correlació, recta de regressió, estimacions",
       'estadística bidimensional, distribuciones bidimensionales, tabla de doble entrada, nube de puntos, centro de gravedad, correlación, covarianza, coeficiente de correlación, recta de regresión, estimaciones')
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
TIT = T("Estadística bidimensional", 'Estadística bidimensional')
NU = 10

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
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs eines per a fer taules de doble entrada, dibuixar núvols de punts, calcular el coeficient de correlació i la recta de regressió pas a pas i fer estimacions. Els resultats aproximats estan arrodonits a les centèsimes; fes els càlculs amb tots els decimals i arrodoneix només al final.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás herramientas para hacer tablas de doble entrada, dibujar nubes de puntos, calcular el coeficiente de correlación y la recta de regresión paso a paso y hacer estimaciones. Los resultados aproximados están redondeados a las centésimas; haz los cálculos con todos los decimales y redondea solo al final.") if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Pots fer servir la calculadora en mode estadístic de dues variables ($y=a+bx$) per a comprovar els resultats. Les seccions segueixen l'ordre dels apunts de la unitat (10.1--10.6).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Puedes usar la calculadora en modo estadístico de dos variables ($y=a+bx$) para comprobar los resultados. Las secciones siguen el orden de los apuntes de la unidad (10.1--10.6)."))
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
