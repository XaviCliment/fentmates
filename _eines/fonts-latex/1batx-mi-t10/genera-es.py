# Versió en castellà de genera.py: escriu els -es.tex. Original: genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (1r Batxillerat MI, Unitat 10: Estadística)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# La fitxa segueix els apartats dels apunts (10.1-10.8): repàs d'estadística unidimensional i estadística bidimensional
# (taules de doble entrada, núvols de punts, covariància i correlació lineal; els altres tipus de relació, només amb núvols).
# Tots els resultats numèrics de les solucions es CALCULEN aquí (uni(), bi(), dbl() amb Fraction) i es formaten amb d():
# no s'escriuen a mà. Els núvols de punts es dibuixen amb TikZ (nuvol()).
# Ús: python3 genera.py && pdflatex t10-fitxa-exercicis.tex (dues vegades) && pdflatex t10-fitxa-solucions.tex (dues vegades)
import os, re, math, random
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
NCHK = [0]

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

def d(v, k=2):
    """nombre amb coma decimal, arredonit a k decimals (sense zeros finals); els enters es mostren sense decimals"""
    v = float(v)
    s = ('%.' + str(k) + 'f') % (round(v, k) + 0.0)
    if '.' in s: s = s.rstrip('0').rstrip('.')
    if s == '-0': s = '0'
    s = s.replace('.', '{,}')
    neg = s.startswith('-'); s = s.lstrip('-')
    ip, _, fp = s.partition('{,}')
    if len(ip) > 4: ip = re.sub(r'(?<=\d)(?=(\d{3})+$)', r'\\,', ip)
    return ('-' if neg else '') + ip + ('{,}' + fp if fp else '')
def ap(v, k=2):
    """«=» si el valor és exacte amb k decimals, «\\approx» si s'ha arredonit"""
    return '=' if abs(float(v) * 10 ** k - round(float(v) * 10 ** k)) < 1e-9 else r'\approx'

def uni(vals, fr=None):
    fr = fr or [1] * len(vals)
    N = sum(fr); s = sum(Fr(v) * f for v, f in zip(vals, fr)); s2 = sum(Fr(v) ** 2 * f for v, f in zip(vals, fr))
    m = s / N; var = s2 / N - m * m
    data = sorted(Fr(v) for v, f in zip(vals, fr) for _ in range(f))
    def q(k):  # primer valor amb F >= kN (si F = kN exactament, mitjana amb el següent)
        pos = k * N
        if pos == int(pos) and 0 < pos < N and data[int(pos) - 1] != data[int(pos)]:
            Fv = sum(1 for z in data if z <= data[int(pos) - 1])
            if Fv == pos: return (data[int(pos) - 1] + data[int(pos)]) / 2
        return data[math.ceil(pos - 1e-12) - 1] if pos > 0 else data[0]
    cnt = {}
    for z in data: cnt[z] = cnt.get(z, 0) + 1
    mx = max(cnt.values())
    NCHK[0] += 1
    return dict(N=N, s=s, s2=s2, m=m, v=var, sd=math.sqrt(var), me=q(Fr(1, 2)), q1=q(Fr(1, 4)), q3=q(Fr(3, 4)), mo=[z for z in sorted(cnt) if cnt[z] == mx], mn=data[0], mxv=data[-1])
def bi(x, y, f=None):
    f = f or [1] * len(x)
    N = sum(f); X = [Fr(v) for v in x]; Y = [Fr(v) for v in y]
    sx = sum(a * k for a, k in zip(X, f)); sy = sum(b * k for b, k in zip(Y, f))
    sx2 = sum(a * a * k for a, k in zip(X, f)); sy2 = sum(b * b * k for b, k in zip(Y, f)); sxy = sum(a * b * k for a, b, k in zip(X, Y, f))
    mx, my = sx / N, sy / N; vx, vy = sx2 / N - mx * mx, sy2 / N - my * my; c = sxy / N - mx * my
    r = float(c) / math.sqrt(vx * vy)
    # comprovació independent amb la definició (desviacions)
    c2 = sum((a - mx) * (b - my) * k for a, b, k in zip(X, Y, f)) / N
    assert c2 == c and -1 <= r <= 1
    NCHK[0] += 1
    return dict(N=N, sx=sx, sy=sy, sx2=sx2, sy2=sy2, sxy=sxy, mx=mx, my=my, vx=vx, vy=vy, c=c, r=r, sdx=math.sqrt(vx), sdy=math.sqrt(vy))
def dbl(T):
    """T: dict {(x, y): f} → (xs, ys, fs) per a bi()"""
    ks = sorted(T); return [k[0] for k in ks], [k[1] for k in ks], [T[k] for k in ks]
def desc(r):
    a = abs(r)
    if a < 0.2: return 'prácticamente nula (no hay correlación lineal)'
    return ('positiva' if r > 0 else 'negativa') + ' ' + ('muy fuerte' if a > 0.95 else 'fuerte' if a >= 0.8 else 'moderada' if a >= 0.5 else 'débil')

# ---------- taules ----------
def tsimple(x, y, nx='x_i', ny='y_i'):
    return r'{\small$\begin{array}{|c|' + 'c' * len(x) + r'|}\hline ' + nx + ' & ' + ' & '.join(d(v) for v in x) + r'\\\hline ' + ny + ' & ' + ' & '.join(d(v) for v in y) + r'\\\hline\end{array}$}'
def tdoble(xs, ys, T, nx='X', ny='Y', marg=False):
    cols = 'c|' * len(ys) + ('c|' if marg else '')
    h = r'{\small$\begin{array}{|c|' + cols + r'}\hline ' + nx + r'\backslash ' + ny + ' & ' + ' & '.join(d(b) for b in ys) + (r' & f_x' if marg else '') + r'\\\hline '
    for a in xs:
        row = [T.get((a, b), 0) for b in ys]
        h += d(a) + ' & ' + ' & '.join(str(v) for v in row) + ((' & ' + str(sum(row))) if marg else '') + r'\\'
        h += r'\hline ' if a == xs[-1] else ' '
    if marg:
        h += 'f_y & ' + ' & '.join(str(sum(T.get((a, b), 0) for a in xs)) for b in ys) + ' & ' + str(sum(T.values())) + r'\\\hline '
    return h + r'\end{array}$}'
def tcalc(x, y, B):
    """taula de càlculs x, y, x², y², xy amb les sumes"""
    rows = r'\\ '.join('%s & %s & %s & %s & %s' % (d(a), d(b), d(Fr(a) ** 2), d(Fr(b) ** 2), d(Fr(a) * Fr(b))) for a, b in zip(x, y))
    return (r'{\small$\begin{array}{|c|c|c|c|c|}\hline x_i & y_i & x_i^2 & y_i^2 & x_iy_i\\\hline ' + rows +
            r'\\\hline \textstyle\sum: %s & %s & %s & %s & %s\\\hline\end{array}$}' % (d(B['sx']), d(B['sy']), d(B['sx2']), d(B['sy2']), d(B['sxy'])))
def calc(B, ux='', uy=''):
    """passos: mitjanes, variàncies, desviacions, covariància i r"""
    N = B['N']
    return (r'$\bar x=\frac{%s}{%d}%s%s$, \ $\bar y=\frac{%s}{%d}%s%s$; \ ' % (d(B['sx']), N, ap(B['mx'], 3), d(B['mx'], 3), d(B['sy']), N, ap(B['my'], 3), d(B['my'], 3)) +
            r'$\sigma_x^2=\frac{%s}{%d}-\bar x^2%s%s$, \ $\sigma_y^2=\frac{%s}{%d}-\bar y^2%s%s$; \ ' % (d(B['sx2']), N, ap(B['vx'], 3), d(B['vx'], 3), d(B['sy2']), N, ap(B['vy'], 3), d(B['vy'], 3)) +
            r'$\sigma_x%s%s$, \ $\sigma_y%s%s$. \ ' % (ap(B['sdx'], 3), d(B['sdx'], 3), ap(B['sdy'], 3), d(B['sdy'], 3)) +
            r'$\sigma_{xy}=\frac{%s}{%d}-\bar x\,\bar y%s\res{%s}$.' % (d(B['sxy']), N, ap(B['c'], 3), d(B['c'], 3)))
def rr(B):
    return r'$r=\dfrac{\sigma_{xy}}{\sigma_x\sigma_y}%s\res{%s}$: correlación \rest{%s}.' % (ap(B['r'], 3), d(B['r'], 3), desc(B['r']))

# ---------- núvols (TikZ) ----------
def nuvol(pts, x0, x1, y0, y1, sx=1, sy=1, lx='X', ly='Y', sc=0.42, cg=None, step=(1, 1)):
    W = (x1 - x0) / sx; H = (y1 - y0) / sy
    X = lambda v: (v - x0) / sx; Y = lambda v: (v - y0) / sy
    g = r'\draw[muted!30,very thin] (0,0) grid (%s,%s);' % (W, H)
    g += r'\draw[-latex,thick] (0,0)--(%s,0) node[right,font=\scriptsize]{$%s$};\draw[-latex,thick] (0,0)--(0,%s) node[above,font=\scriptsize]{$%s$};' % (W + 0.5, lx, H + 0.5, ly)
    v = x0
    while v <= x1 + 1e-9:
        g += r'\node[below,font=\tiny] at (%s,0) {$%s$};' % (X(v), d(v)); v += step[0] * sx
    v = y0
    while v <= y1 + 1e-9:
        g += r'\node[left,font=\tiny] at (0,%s) {$%s$};' % (Y(v), d(v)); v += step[1] * sy
    for a, b in pts: g += r'\fill[accent] (%s,%s) circle (0.16);' % (round(X(a), 3), round(Y(b), 3))
    if cg: g += r'\draw[navy,thick,fill=white] (%s,%s) circle (0.2);' % (X(cg[0]), Y(cg[1]))
    return r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]%s\end{tikzpicture}' % (sc, g)
def gen(n, r, seed):
    """núvol de n punts amb coeficient de correlació r exacte (escala 0-10)"""
    rnd = random.Random(seed)
    z1 = [rnd.gauss(0, 1) for _ in range(n)]; z2 = [rnd.gauss(0, 1) for _ in range(n)]
    def st(a):
        m = sum(a) / n; s = math.sqrt(sum((v - m) ** 2 for v in a) / n); return [(v - m) / s for v in a]
    z1 = st(z1); dd = sum(a * b for a, b in zip(z1, z2)) / n; z2 = st([b - dd * a for a, b in zip(z1, z2)])
    return [(5 + 1.5 * a, 5 + 1.5 * (r * a + math.sqrt(1 - r * r) * b)) for a, b in zip(z1, z2)]
def rnum(pts):
    n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
    c = sum((p[0] - mx) * (p[1] - my) for p in pts) / n
    return c / math.sqrt(sum((p[0] - mx) ** 2 for p in pts) / n * sum((p[1] - my) ** 2 for p in pts) / n)
def nv(pts, sc=0.22): return nuvol([p for p in pts if 0 <= p[0] <= 10 and 0 <= p[1] <= 10], 0, 10, 0, 10, sc=sc, step=(2, 2))

S_ = []

# =====================================================================
# 1. Variables i taules de freqüències
NOTES = [5, 7, 6, 4, 8, 6, 5, 7, 6, 9, 3, 6, 7, 5, 6, 8, 4, 7, 6, 5, 6, 8, 7, 6, 5]
vals1 = sorted(set(NOTES)); f1 = [NOTES.count(v) for v in vals1]; N1 = len(NOTES)
F1 = [sum(f1[:i + 1]) for i in range(len(f1))]
U1 = uni(vals1, f1)
assert sum(f1) == 25 and F1[-1] == 25
T1 = r'{\small$\begin{array}{|c|c|c|c|c|}\hline x_i & f_i & F_i & h_i & H_i\\\hline ' + r'\\ '.join(
    '%d & %d & %d & %s & %s' % (v, f, F, d(Fr(f, N1)), d(Fr(F, N1))) for v, f, F in zip(vals1, f1, F1)) + r'\\\hline\end{array}$}'
S_.append(("Estadística unidimensional: variables y tablas", [
 (1, r"Clasifica las variables estadísticas siguientes en cualitativas, cuantitativas discretas o cuantitativas continuas:" + tasks(2, ["El grupo sanguíneo.", "El número de libros leídos en un año.", "La temperatura a mediodía.", "El tiempo semanal dedicado al deporte.", "La marca del móvil.", "El número de goles en un partido."]),
     tasks(2, [r'\rest{cualitativa}', r'\rest{cuantitativa discreta}', r'\rest{cuantitativa continua}', r'\rest{cuantitativa continua}', r'\rest{cualitativa}', r'\rest{cuantitativa discreta}'])),
 (1, r"Las notas de un examen de 25 alumnos han sido: \ " + ', '.join('$%d$' % v for v in NOTES) + r". \ Haz la tabla de frecuencias absolutas, relativas y acumuladas. ¿Qué porcentaje de alumnos ha aprobado (nota 5 o más)?"
     + recorda(r"$h_i=\frac{f_i}{N}$; \ las frecuencias acumuladas $F_i$ y $H_i$ suman las de los valores menores o iguales que $x_i$."),
     r'\par{\centering ' + T1 + r'\par}\smallskip Han aprobado $25-%d=%d$ alumnos: el $\res{%s\,\%%}$.' % (F1[1], 25 - F1[1], d(Fr(25 - F1[1], 25) * 100))),
]))

# =====================================================================
# 2. Centralització i posició
Q2a = [2, 4, 4, 5, 6, 7, 7, 7, 9]; U2a = uni(Q2a)
Q2b = [12, 15, 15, 18, 20, 21, 25, 30]; U2b = uni(Q2b)
assert U2a['me'] == 6 and U2b['me'] == Fr(19)
U2c = uni(vals1, f1)
S_.append(("Parámetros de centralización y de posición", [
 (1, r"Calcula la media, la mediana, la moda y los cuartiles:" + tasks(1, ['$' + r',\ '.join(str(v) for v in Q2a) + '$', '$' + r',\ '.join(str(v) for v in Q2b) + '$'])
     + recorda(r"$\bar x=\frac{\sum x_if_i}{N}$. La mediana deja la mitad de los datos por debajo; $Q_1$, el 25\,\% y $Q_3$, el 75\,\%. Si $\frac N2$ cae justo entre dos datos diferentes, la mediana es la media de ambos."),
     tasks(1, [r'$\bar x=\frac{%s}{%d}%s\res{%s}$, \ $Me=\res{%s}$, \ $Mo=\res{%s}$, \ $Q_1=\res{%s}$, \ $Q_3=\res{%s}$' % (d(U2a['s']), U2a['N'], ap(U2a['m']), d(U2a['m']), d(U2a['me']), d(U2a['mo'][0]), d(U2a['q1']), d(U2a['q3'])),
               r'$\bar x=\frac{%s}{%d}%s\res{%s}$, \ $Me=\frac{18+20}{2}=\res{%s}$, \ $Mo=\res{%s}$, \ $Q_1=\res{%s}$, \ $Q_3=\res{%s}$' % (d(U2b['s']), U2b['N'], ap(U2b['m']), d(U2b['m']), d(U2b['me']), d(U2b['mo'][0]), d(U2b['q1']), d(U2b['q3']))])),
 (1, r"Con la tabla del ejercicio 2, calcula la nota media, la mediana, la moda y los cuartiles.",
     r'$\bar x=\frac{%s}{25}=\res{%s}$; \ $\frac N2=12{,}5$: $Me=\res{%s}$; \ $Mo=\res{%s}$; \ $Q_1=\res{%s}$ ($\frac N4=6{,}25$), \ $Q_3=\res{%s}$ ($\frac{3N}4=18{,}75$).' % (d(U2c['s']), d(U2c['m']), d(U2c['me']), d(U2c['mo'][0]), d(U2c['q1']), d(U2c['q3']))),
 (2, r"La media de 4 notas de una alumna es 6,5. ¿Qué nota tiene que sacar en el quinto examen para que la media sea 7?",
     r"Ahora suma $4\cdot6{,}5=26$; tiene que sumar $5\cdot7=35$: necesita un $\res{9}$."),
]))
assert 4 * Fr(13, 2) == 26 and 35 - 26 == 9; NCHK[0] += 1

# =====================================================================
# 3. Dispersió
A3 = [6, 7, 7, 8, 8, 8, 9, 9, 10]; B3 = [2, 4, 6, 8, 8, 8, 10, 12, 14]
UA, UB = uni(A3), uni(B3)
assert UA['m'] == UB['m'] == 8
INT = [(0, 10, 6), (10, 20, 10), (20, 30, 15), (30, 40, 7), (40, 50, 2)]
mk = [Fr(a + b, 2) for a, b, _ in INT]; fi = [f for _, _, f in INT]; UI3 = uni(mk, fi)
AT1 = [Fr(x) for x in ('12.1', '12.3', '12.0', '12.4', '12.2')]; AT2 = [Fr(x) for x in ('11.8', '12.6', '12.0', '12.9', '11.7')]
UA1, UA2 = uni(AT1), uni(AT2)
assert UA1['sd'] < UA2['sd']
G1 = dict(m=Fr(165), s=Fr(8)); G2 = dict(m=Fr(32), s=Fr(4))
cv1, cv2 = G1['s'] / G1['m'], G2['s'] / G2['m']
S_.append(("Parámetros de dispersión", [
 (1, r"Dos grupos han sacado estas notas. Calcula la media, el rango, la varianza y la desviación típica de cada grupo. ¿Qué observas?" + tasks(1, ['Grupo A: $' + r',\ '.join(map(str, A3)) + '$', 'Grupo B: $' + r',\ '.join(map(str, B3)) + '$'])
     + recorda(r"$\sigma^2=\frac{\sum x_i^2f_i}{N}-\bar x^2$, \ $\sigma=\sqrt{\sigma^2}$, \ $CV=\frac{\sigma}{\bar x}$."),
     tasks(1, [r'A: $\bar x=\res{8}$, rango $\res{%s}$, $\sigma^2=\frac{%s}{%d}-64%s\res{%s}$, $\sigma%s\res{%s}$' % (d(UA['mxv'] - UA['mn']), d(UA['s2']), UA['N'], ap(UA['v']), d(UA['v']), ap(UA['sd']), d(UA['sd'])),
               r'B: $\bar x=\res{8}$, rango $\res{%s}$, $\sigma^2=\frac{%s}{%d}-64%s\res{%s}$, $\sigma%s\res{%s}$' % (d(UB['mxv'] - UB['mn']), d(UB['s2']), UB['N'], ap(UB['v']), d(UB['v']), ap(UB['sd']), d(UB['sd']))])
     + r"\par Tienen la misma media, pero las notas del grupo B están \rest{mucho más dispersas}."),
 (2, r"Los minutos que 40 alumnos dedican a leer cada día se recogen en esta tabla. Calcula la media, la desviación típica y el coeficiente de variación.\par\smallskip{\centering\small$\begin{array}{|c|" + 'c' * len(INT) + r"|}\hline\text{Minutos}&" + '&'.join(r'[%d,%d)' % (a, b) for a, b, _ in INT) + r"\\\hline f_i&" + '&'.join(str(f) for f in fi) + r"\\\hline\end{array}$\par}",
     r'Marcas de clase $%s$. \ $\sum x_if_i=%s$, \ $\sum x_i^2f_i=%s$. \ $\bar x=\frac{%s}{40}%s\res{%s}$ min, \ $\sigma^2%s%s$, \ $\sigma%s\res{%s}$ min, \ $CV%s\res{%s}$ ($%s\,\%%$).' % (
         r',\ '.join(d(v) for v in mk), d(UI3['s']), d(UI3['s2']), d(UI3['s']), ap(UI3['m']), d(UI3['m']), ap(UI3['v']), d(UI3['v']), ap(UI3['sd']), d(UI3['sd']), ap(UI3['sd'] / float(UI3['m']), 3), d(UI3['sd'] / float(UI3['m']), 3), d(100 * UI3['sd'] / float(UI3['m']), 1))),
 (2, r"Dos atletas han hecho estos tiempos (s) en cinco carreras de 100 m. Calcula la media y la desviación típica de cada uno. ¿Cuál es más rápido de media? ¿Cuál es más regular?" + tasks(1, ['A: $' + r',\ '.join(d(v) for v in AT1) + '$', 'B: $' + r',\ '.join(d(v) for v in AT2) + '$']),
     tasks(1, [r'A: $\bar x=%s$ s, \ $\sigma%s%s$ s' % (d(UA1['m'], 3), ap(UA1['sd'], 3), d(UA1['sd'], 3)), r'B: $\bar x=%s$ s, \ $\sigma%s%s$ s' % (d(UA2['m'], 3), ap(UA2['sd'], 3), d(UA2['sd'], 3))])
     + r"\par " + (r"Tienen la misma media" if UA1['m'] == UA2['m'] else (r"Es más rápido de media \rest{%s}" % ('A' if UA1['m'] < UA2['m'] else 'B'))) + r"; el atleta \rest{A es más regular} (menos dispersión)."),
 (2, r"Las alturas de un grupo tienen $\bar x=165$ cm y $\sigma=8$ cm, y los pesos de otro grupo, $\bar x=32$ kg y $\sigma=4$ kg. ¿Cuál de los dos es relativamente más disperso? ¿Por qué no se pueden comparar directamente las desviaciones típicas?",
     r"Tienen unidades y medias diferentes: hace falta el coeficiente de variación. \ $CV_1=\frac{8}{165}%s%s$, \ $CV_2=\frac{4}{32}=%s$: es más disperso \rest{el segundo grupo} (pesos)." % (ap(cv1, 3), d(cv1, 3), d(cv2, 3))),
]))
assert cv2 > cv1; NCHK[0] += 1

# =====================================================================
# 4. Taules de doble entrada
TD = {(1, 0): 4, (1, 1): 2, (1, 2): 0, (2, 0): 3, (2, 1): 6, (2, 2): 3, (3, 0): 0, (3, 1): 3, (3, 2): 4}
xsD, ysD = [1, 2, 3], [0, 1, 2]; BD = bi(*dbl(TD))
fxD = [sum(TD[(a, b)] for b in ysD) for a in xsD]; fyD = [sum(TD[(a, b)] for a in xsD) for b in ysD]
PAIRS4 = [(2, 1), (3, 2), (2, 2), (1, 1), (3, 3), (2, 1), (1, 1), (2, 2), (3, 2), (2, 2), (1, 2), (3, 3)]
T4 = {}
for p in PAIRS4: T4[p] = T4.get(p, 0) + 1
x4 = sorted(set(p[0] for p in PAIRS4)); y4 = sorted(set(p[1] for p in PAIRS4)); B4 = bi(*dbl(T4))
S_.append(("Variables bidimensionales. Tablas de doble entrada", [
 (1, r"Se ha preguntado a 25 familias el número de hijos ($X$) y el número de coches ($Y$) que tienen:\par\smallskip{\centering " + tdoble(xsD, ysD, TD) + r"\par}\smallskip" + tasks(1, ["Añade las distribuciones marginales a la tabla.", "¿Cuántas familias tienen 2 hijos y 1 coche? ¿Cuántas tienen más de un coche?", "Calcula las medias marginales $\\bar x$ y $\\bar y$."])
     + recorda(r"En una tabla de doble entrada, las sumas de las filas dan la distribución marginal de $X$ y las de las columnas, la de $Y$. La suma de todas las casillas es $N$."),
     r'\par{\centering ' + tdoble(xsD, ysD, TD, marg=True) + r'\par}\smallskip' + tasks(1, [r'Véase la tabla.', r'$\res{%d}$ familias con 2 hijos y 1 coche; \ $\res{%d}$ con más de un coche (2 coches).' % (TD[(2, 1)], fyD[2]),
         r'$\bar x=\frac{%s}{25}=\res{%s}$, \ $\bar y=\frac{%s}{25}=\res{%s}$' % (d(BD['sx']), d(BD['mx']), d(BD['sy']), d(BD['my']))])),
 (2, r"Las notas de Matemáticas ($X$) y de Física ($Y$) de 12 alumnos, en una escala de 1 a 3 (1 = insuficiente, 2 = aprobado, 3 = notable o más), han sido: \ " + ', '.join('$(%d,%d)$' % p for p in PAIRS4) + r". \ Construye la tabla de doble entrada y calcula las medias marginales.",
     r'\par{\centering ' + tdoble(x4, y4, T4, marg=True) + r'\par}\smallskip $\bar x=\frac{%s}{12}%s\res{%s}$, \ $\bar y=\frac{%s}{12}%s\res{%s}$.' % (d(B4['sx']), ap(B4['mx']), d(B4['mx']), d(B4['sy']), ap(B4['my']), d(B4['my']))),
]))
assert sum(TD.values()) == 25 and sum(T4.values()) == 12

# =====================================================================
# 5. Núvol de punts
X5 = [1, 2, 3, 4, 5, 6, 7, 8]; Y5 = [62, 60, 55, 53, 50, 46, 44, 40]
B5 = bi(X5, Y5)
CL = [(gen(25, 0.9, 1), 0.9), (gen(25, -0.95, 2), -0.95), (gen(25, 0.0, 3), 0.0), (gen(25, -0.5, 4), -0.5)]
for pts, r in CL: assert abs(rnum(pts) - r) < 1e-9; NCHK[0] += 1
ORD = [2, 0, 3, 1]  # ordre en què es mostren els valors de r a l'enunciat
S_.append(("Nube de puntos", [
 (1, r"Un coche gasta gasolina y anotamos el combustible que queda en el depósito ($Y$, en litros) al final de cada hora de viaje ($X$): \par\smallskip{\centering " + tsimple(X5, Y5) + r"\par}\smallskip Representa la nube de puntos y el centro de gravedad. ¿Qué tipo de correlación se observa?"
     + recorda(r"Cada par $(x_i,y_i)$ es un punto. El centro de gravedad es $(\bar x,\bar y)$."),
     r'$(\bar x,\bar y)=(%s,\ %s)$. \ Los puntos bajan casi en línea recta: correlación \rest{negativa y muy fuerte}.\par\smallskip{\centering ' % (d(B5['mx']), d(B5['my'])) + nuvol(list(zip(X5, Y5)), 0, 9, 35, 65, sy=5, lx='h', ly='l', cg=(B5['mx'], B5['my'])) + r'\par}'),
 (1, r"Asocia cada nube con uno de estos coeficientes de correlación: \ $r=%s$, \ $r=%s$, \ $r=%s$, \ $r=%s$." % tuple(d(CL[i][1]) for i in ORD) + tasks(4, [r'\par' + nv(p) for p, _ in CL]),
     tasks(4, [r'$\res{r=%s}$' % d(r) for _, r in CL])),
 (1, r"Indica, para cada par de variables, si esperas una correlación positiva, negativa o ninguna correlación:" + tasks(1, ["La altura y el peso de 30 adolescentes.", "El precio de una entrada de cine y el número de espectadores.", "La nota de inglés y el número de zapato.", "Los kilómetros recorridos y la gasolina gastada.", "La temperatura exterior y el consumo de calefacción.", "El mes de nacimiento y el número de hermanos."]),
     tasks(2, [r'\rest{positiva}', r'\rest{negativa}', r'\rest{ninguna}', r'\rest{positiva}', r'\rest{negativa}', r'\rest{ninguna}'])),
]))

# =====================================================================
# 6. Covariància
X6 = [2, 4, 5, 6, 8]; Y6 = [3, 5, 4, 7, 9]; B6 = bi(X6, Y6)
X6b = [10, 20, 30, 40, 50]; Y6b = [9, 8, 6, 5, 2]; B6b = bi(X6b, Y6b)
S_.append(("Varianzas y covarianza", [
 (2, r"Para la variable bidimensional siguiente, haz la tabla de cálculos y halla las medias, las varianzas, las desviaciones típicas y la covarianza:\par\smallskip{\centering " + tsimple(X6, Y6) + r"\par}"
     + recorda(r"$\sigma_x^2=\frac{\sum x_i^2}{N}-\bar x^2$, \ $\sigma_y^2=\frac{\sum y_i^2}{N}-\bar y^2$, \ $\sigma_{xy}=\frac{\sum x_iy_i}{N}-\bar x\,\bar y$."),
     r'\par{\centering ' + tcalc(X6, Y6, B6) + r'\par}\smallskip ' + calc(B6)),
 (2, r"Calcula la covarianza de los datos siguientes e interpreta su signo:\par\smallskip{\centering " + tsimple(X6b, Y6b) + r"\par}",
     calc(B6b) + r" \ Es negativa: cuando $X$ aumenta, $Y$ tiende a \rest{disminuir}."),
 (2, r"Calcula la covarianza de las notas de Matemáticas y de Física de la sección 4 (la tabla de doble entrada de 12 alumnos).",
     r'$\sum x_iy_jf_{ij}=%s$: \ $\sigma_{xy}=\frac{%s}{12}-\bar x\,\bar y%s\res{%s}$' % (d(B4['sxy']), d(B4['sxy']), ap(B4['c'], 3), d(B4['c'], 3))),
 (2, r"Calcula la covarianza de la variable bidimensional del ejercicio sobre hijos y coches (sección 4).",
     r'$\sum x_iy_jf_{ij}=%s$: \ $\sigma_{xy}=\frac{%s}{25}-%s\cdot%s%s\res{%s}$' % (d(BD['sxy']), d(BD['sxy']), d(BD['mx']), d(BD['my']), ap(BD['c'], 3), d(BD['c'], 3))),
]))

# =====================================================================
# 7. Correlació lineal
X7 = [150, 155, 160, 165, 170, 175, 180]; Y7 = [48, 52, 55, 61, 63, 70, 72]; B7 = bi(X7, Y7)
X7d = [18, 21, 24, 27, 30, 33]; Y7d = [35, 52, 58, 75, 84, 102]; B7d = bi(X7d, Y7d)
X7b = [0, 1, 2, 3, 4, 5]; Y7b = [10, 8, 9, 6, 4, 3]; B7b = bi(X7b, Y7b)
S_.append(("Correlación lineal", [
 (2, r"Calcula el coeficiente de correlación de los datos de los ejercicios de la sección 6 e interprétalo." + tasks(1, ['Los datos del primer ejercicio de la sección 6.', 'Los datos del segundo ejercicio de la sección 6.', 'Hijos y coches (sección 4).'])
     + recorda(r"$r=\dfrac{\sigma_{xy}}{\sigma_x\,\sigma_y}$, \ $-1\leq r\leq 1$. El signo da el sentido de la relación y $|r|$, la fuerza: cerca de 1, fuerte; cerca de 0, no hay correlación lineal."),
     tasks(1, [rr(B6), rr(B6b), r'$r=\dfrac{%s}{\sqrt{%s}\cdot\sqrt{%s}}%s\res{%s}$: correlación \rest{%s}.' % (d(BD['c'], 3), d(BD['vx'], 3), d(BD['vy'], 3), ap(BD['r'], 3), d(BD['r'], 3), desc(BD['r']))])),
 (2, r"La altura (cm) y el peso (kg) de 7 personas han sido:\par\smallskip{\centering " + tsimple(X7, Y7, 'x_i\\ (\\text{cm})', 'y_i\\ (\\text{kg})') + r"\par}\smallskip Representa la nube de puntos, calcula el coeficiente de correlación e interprétalo.",
     calc(B7) + ' ' + rr(B7) + r'\par\smallskip{\centering ' + nuvol(list(zip(X7, Y7)), 145, 185, 45, 75, sx=5, sy=5, lx='cm', ly='kg', step=(2, 1)) + r'\par}'),
 (2, r"Las horas semanales de videojuegos ($X$) y la nota de un examen ($Y$) de 6 alumnos han sido:\par\smallskip{\centering " + tsimple(X7b, Y7b) + r"\par}\smallskip Calcula el coeficiente de correlación. ¿Podemos afirmar que jugar a videojuegos hace bajar la nota?",
     calc(B7b) + ' ' + rr(B7b) + r" \ Pero una correlación, aunque sea fuerte, \rest{no demuestra que haya una relación de causa y efecto}: puede haber otras variables (el tiempo de estudio, por ejemplo)."),
 (2, r"Una heladería anota la temperatura máxima ($X$, en °C) y los helados vendidos ($Y$) durante seis días:\par\smallskip{\centering " + tsimple(X7d, Y7d) + r"\par}\smallskip Calcula el coeficiente de correlación e interprétalo.",
     calc(B7d) + ' ' + rr(B7d)),
 (2, r"Calcula el coeficiente de correlación entre las notas de Matemáticas y de Física de la sección 4.",
     r'$\sigma_x^2%s%s$, \ $\sigma_y^2%s%s$, \ $\sigma_{xy}%s%s$. \ $r%s\res{%s}$: correlación \rest{%s}.' % (ap(B4['vx'], 3), d(B4['vx'], 3), ap(B4['vy'], 3), d(B4['vy'], 3), ap(B4['c'], 3), d(B4['c'], 3), ap(B4['r'], 3), d(B4['r'], 3), desc(B4['r']))),
 (1, r"Si el coeficiente de correlación entre dos variables es $r=0{,}8$ y las desviaciones típicas son $\sigma_x=2$ y $\sigma_y=5$, ¿cuánto vale la covarianza?",
     r"$\sigma_{xy}=r\,\sigma_x\,\sigma_y=0{,}8\cdot2\cdot5=\res{8}$."),
 (1, r"Si $\sigma_{xy}=-12$, $\sigma_x=4$ y $\sigma_y=5$, ¿cuánto vale $r$? ¿Y si $\sigma_{xy}=3$, $\sigma_x=2$ y $\sigma_y=1$? ¿Es posible?",
     r"$r=\frac{-12}{4\cdot5}=\res{-0{,}6}$ (negativa moderada). \ En el segundo caso saldría $r=\frac{3}{2}=1{,}5>1$: \rest{no es posible}, hay un error en los datos."),
 (3, r"Una variable bidimensional tiene $N=10$, $\sum x_i=50$, $\sum y_i=80$, $\sum x_i^2=290$, $\sum y_i^2=730$ y $\sum x_iy_i=440$. Calcula $r$.",
     r''),
]))
B7c = dict(N=10, sx=Fr(50), sy=Fr(80), sx2=Fr(290), sy2=Fr(730), sxy=Fr(440))
B7c.update(mx=B7c['sx'] / 10, my=B7c['sy'] / 10); B7c.update(vx=B7c['sx2'] / 10 - B7c['mx'] ** 2, vy=B7c['sy2'] / 10 - B7c['my'] ** 2, c=B7c['sxy'] / 10 - B7c['mx'] * B7c['my'])
B7c.update(sdx=math.sqrt(B7c['vx']), sdy=math.sqrt(B7c['vy'])); B7c['r'] = float(B7c['c']) / (B7c['sdx'] * B7c['sdy']); NCHK[0] += 1
assert abs(Fr(-12, 20)) == Fr(3, 5)
S_[-1][1][-1] = (3, S_[-1][1][-1][1], calc(B7c) + ' ' + rr(B7c))

# =====================================================================
# 8. Recta de regressió
def reg(B, inv=False):
    """recta de Y sobre X (o de X sobre Y si inv): pendent i ordenada exactes"""
    if inv: m = B['c'] / B['vy']; n = B['mx'] - m * B['my']
    else: m = B['c'] / B['vx']; n = B['my'] - m * B['mx']
    NCHK[0] += 1
    return m, n
def eqr(m, n, v='y', w='x', k=3):
    c = '' if m == 1 else '-' if m == -1 else d(m, k)
    return r'%s%s%s%s%s' % (v, ap(m, k), c, w, ('' if n == 0 else ('-' + d(-n, k)) if n < 0 else ('+' + d(n, k))))
def est(m, n, x0): return m * Fr(x0) + n
m6, n6 = reg(B6); m6i, n6i = reg(B6, True)
m7, n7 = reg(B7); m7d, n7d = reg(B7d); m7c, n7c = reg(B7c)
# comprovació: la recta passa per (x̄, ȳ) i fa mínima la suma de quadrats (derivades nul·les)
for B, (m, n), xs, ys in [(B6, (m6, n6), X6, Y6), (B7, (m7, n7), X7, Y7), (B7d, (m7d, n7d), X7d, Y7d)]:
    assert m * B['mx'] + n == B['my']
    assert sum((Fr(y) - m * x - n) for x, y in zip(xs, ys)) == 0 and sum((Fr(y) - m * x - n) * x for x, y in zip(xs, ys)) == 0
    NCHK[0] += 1
# dues rectes donades: y = 0,5x + 2 i x = 1,2y − 1
cx = Fr(14, 10) / Fr(4, 10); cy = Fr(1, 2) * cx + 2
assert cx == 1.2 * cy - 1 or abs(float(cx) - (1.2 * float(cy) - 1)) < 1e-12; r2 = math.sqrt(0.5 * 1.2); NCHK[0] += 1
S_.append(("Recta de regresión", [
 (2, r"Con los datos del primer ejercicio de la sección 6, halla la recta de regresión de $Y$ sobre $X$ y la de $X$ sobre $Y$. Estima el valor de $y$ para $x=7$ y el de $x$ para $y=6$."
     + recorda(r"Recta de regresión de $Y$ sobre $X$: \ $y-\bar y=\dfrac{\sigma_{xy}}{\sigma_x^2}(x-\bar x)$. \ De $X$ sobre $Y$: \ $x-\bar x=\dfrac{\sigma_{xy}}{\sigma_y^2}(y-\bar y)$. Las estimaciones son fiables si $|r|$ está cerca de 1 y no nos salimos del intervalo de los datos."),
     r'$Y$ sobre $X$: $y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$; \ $\hat y(7)%s\res{%s}$. \ $X$ sobre $Y$: $x-%s=\frac{%s}{%s}(y-%s)\Rightarrow\res{%s}$; \ $\hat x(6)%s\res{%s}$. \ Son fiables: $r%s%s$ y los valores están dentro de los datos.' % (
         d(B6['my'], 3), d(B6['c'], 3), d(B6['vx'], 3), d(B6['mx'], 3), eqr(m6, n6), ap(est(m6, n6, 7), 3), d(est(m6, n6, 7), 3),
         d(B6['mx'], 3), d(B6['c'], 3), d(B6['vy'], 3), d(B6['my'], 3), eqr(m6i, n6i, 'x', 'y'), ap(est(m6i, n6i, 6), 3), d(est(m6i, n6i, 6), 3), ap(B6['r'], 3), d(B6['r'], 3))),
 (2, r"Con las alturas y los pesos de la sección 7, halla la recta de regresión del peso sobre la altura. ¿Qué peso se estima para una persona de 168 cm? ¿Y para un niño de 120 cm? ¿Son fiables las dos estimaciones?",
     r'$y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$. \ $\hat y(168)%s\res{%s\text{ kg}}$: \rest{fiable} ($r%s%s$ y 168 está dentro de los datos). \ $\hat y(120)%s%s$ kg: \rest{no es fiable}, 120 cm queda muy lejos del intervalo $[150,180]$.' % (
         d(B7['my'], 3), d(B7['c'], 3), d(B7['vx'], 3), d(B7['mx'], 3), eqr(m7, n7), ap(est(m7, n7, 168), 2), d(est(m7, n7, 168), 2), ap(B7['r'], 3), d(B7['r'], 3), ap(est(m7, n7, 120), 2), d(est(m7, n7, 120), 2))),
 (2, r"Con los datos de la heladería de la sección 7, ¿cuántos helados se estima que se venderán un día con una máxima de 25 °C?",
     r'Recta: $\res{%s}$. \ $\hat y(25)%s%s$: unos $\res{%d}$ helados. Muy fiable: $r%s%s$.' % (eqr(m7d, n7d), ap(est(m7d, n7d, 25), 2), d(est(m7d, n7d, 25), 2), round(est(m7d, n7d, 25)), ap(B7d['r'], 3), d(B7d['r'], 3))),
 (2, r"Con las sumas del último ejercicio de la sección 7 ($N=10$, $\sum x_i=50$, $\sum y_i=80$, $\sum x_i^2=290$, $\sum x_iy_i=440$), halla la recta de regresión de $Y$ sobre $X$ y estima $y$ para $x=6$.",
     r'$\bar x=5$, $\bar y=8$, $\sigma_x^2=4$, $\sigma_{xy}=4$: \ $y-8=\frac44(x-5)\Rightarrow\res{%s}$; \ $\hat y(6)=\res{%s}$ (poco precisa: $r%s%s$ es moderado).' % (eqr(m7c, n7c), d(est(m7c, n7c, 6)), ap(B7c['r'], 3), d(B7c['r'], 3))),
 (3, r"Las rectas de regresión de una variable bidimensional son $y=0{,}5x+2$ (de $Y$ sobre $X$) y $x=1{,}2y-1$ (de $X$ sobre $Y$). Calcula $\bar x$, $\bar y$ y el coeficiente de correlación. (Pista: las dos rectas pasan por $(\bar x,\bar y)$, y el producto de sus pendientes es $\frac{\sigma_{xy}}{\sigma_x^2}\cdot\frac{\sigma_{xy}}{\sigma_y^2}=r^2$.)",
     r'Sustituyendo: $x=1{,}2(0{,}5x+2)-1=0{,}6x+1{,}4\Rightarrow\bar x=\res{%s}$, \ $\bar y=\res{%s}$. \ $r^2=0{,}5\cdot1{,}2=0{,}6$ y, como las pendientes son positivas, $r=\sqrt{0{,}6}%s\res{%s}$.' % (d(cx), d(cy), ap(r2, 3), d(r2, 3))),
]))
assert B7c['c'] == 4 and B7c['vx'] == 4

# =====================================================================
# 9. Altres tipus de relació
rnd = random.Random(5)
NL = [[(x, 9 - 0.35 * (x - 5) ** 2 + rnd.uniform(-0.6, 0.6)) for x in [0.3 + 0.4 * i for i in range(24)]],
      [(x, 0.15 * math.exp(0.42 * x) + rnd.uniform(-0.25, 0.25)) for x in [0.3 + 0.4 * i for i in range(24)]],
      [(1 + 0.15 * i, 1.2 + rnd.uniform(-0.6, 0.6)) for i in range(8)] + [(9, 9)]]
rNL = [rnum(p) for p in NL]
assert abs(rNL[0]) < 0.3 and rNL[1] > 0.8 and rNL[2] > 0.9; NCHK[0] += 1
S_.append(("Otros tipos de relación. Correlación y causalidad", [
 (2, r"Observa estas nubes de puntos. Describe la relación que hay entre las variables y di si el coeficiente de correlación lineal será próximo a 0 o no." + tasks(3, [r'\par' + nv(p) for p in NL]),
     tasks(1, [r'Relación \rest{parabólica} (crece y luego decrece): es fuerte pero no lineal, y $r\approx%s$, \rest{próximo a 0}.' % d(rNL[0]),
               r'Relación \rest{exponencial}: creciente, $r\approx%s$ es alto, pero los puntos no siguen una recta.' % d(rNL[1]),
               r'Los puntos de abajo no tienen ninguna relación, pero el \rest{valor atípico} $(9,9)$ hace que $r\approx%s$. Hay que revisarlo antes de sacar conclusiones.' % d(rNL[2])])),
 (2, r"En un estudio de varias ciudades se ha encontrado una correlación positiva fuerte entre el número de bomberos que actúan en un incendio y los daños que causa. ¿Quiere decir que los bomberos causan los daños? ¿Qué explicación puede haber?",
     r"\rest{No}: la correlación no implica causalidad. Hay una tercera variable, el \rest{tamaño del incendio}: cuanto mayor es, más bomberos van y más daños causa."),
 (1, r"Razona si son verdaderas o falsas: \ a) Si $r=0$, las variables no tienen ninguna relación. \ b) Si $r=-0{,}98$, la relación es muy débil porque $r$ es negativo. \ c) Si todos los puntos están sobre una recta creciente, $r=1$.",
     r"a) \rest{Falsa}: solo quiere decir que no hay relación lineal (puede ser parabólica, por ejemplo). \ b) \rest{Falsa}: es muy fuerte; el signo indica que es inversa. \ c) \rest{Verdadera}."),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "estadística, frecuencias, media, mediana, cuartiles, varianza, desviación típica, coeficiente de variación, variable bidimensional, tabla de doble entrada, nube de puntos, covarianza, correlación lineal"
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
pre += r'''\providecommand{\gt}{>}\providecommand{\lt}{<}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

def fix(t):
    """Fora dels dibuixos: l'espai després de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = "Estadística"
def build(sol):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 10: %s' % (t, TIT), capcalera='%s · Unidad 10: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-mi')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1batx-mi') + '{' + ('Soluciones de la ficha · Unidad 10' if sol else 'Ficha de ejercicios · Unidad 10') + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con las calculadoras de los apuntes interactivos de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos: para las variables bidimensionales, haz siempre la tabla con las columnas $x_i$, $y_i$, $x_i^2$, $y_i^2$ y $x_iy_i$. Redondea los resultados a dos o tres cifras decimales. Puedes comprobarlos con las calculadoras de los apuntes interactivos.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            if sol:
                lab = re.search(r'\\label\{[^}]*\}', q)
                s = (lab.group(0) if lab else '') + s
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con la calculadora bidimensional de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't10-fitxa-solucions-es.tex' if sol else 't10-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis;', NCHK[0], 'comprovacions')
