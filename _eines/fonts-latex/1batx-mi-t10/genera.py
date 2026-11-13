# Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (1r Batxillerat MI, Unitat 10: Estadística)
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
    if a < 0.2: return 'pràcticament nul·la (no hi ha correlació lineal)'
    return ('positiva' if r > 0 else 'negativa') + ' ' + ('molt forta' if a > 0.95 else 'forta' if a >= 0.8 else 'moderada' if a >= 0.5 else 'feble')

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
    return r'$r=\dfrac{\sigma_{xy}}{\sigma_x\sigma_y}%s\res{%s}$: correlació \rest{%s}.' % (ap(B['r'], 3), d(B['r'], 3), desc(B['r']))

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
S_.append(("Estadística unidimensional: variables i taules", [
 (1, r"Classifica les variables estadístiques següents en qualitatives, quantitatives discretes o quantitatives contínues:" + tasks(2, ["El grup sanguini.", "El nombre de llibres llegits en un any.", "La temperatura a migdia.", "El temps setmanal dedicat a l'esport.", "La marca del mòbil.", "El nombre de gols en un partit."]),
     tasks(2, [r'\rest{qualitativa}', r'\rest{quantitativa discreta}', r'\rest{quantitativa contínua}', r'\rest{quantitativa contínua}', r'\rest{qualitativa}', r'\rest{quantitativa discreta}'])),
 (1, r"Les notes d'un examen de 25 alumnes han sigut: \ " + ', '.join('$%d$' % v for v in NOTES) + r". \ Fes la taula de freqüències absolutes, relatives i acumulades. Quin percentatge d'alumnes ha aprovat (nota 5 o més)?"
     + recorda(r"$h_i=\frac{f_i}{N}$; \ les freqüències acumulades $F_i$ i $H_i$ sumen les dels valors menors o iguals que $x_i$."),
     r'\par{\centering ' + T1 + r'\par}\smallskip Han aprovat $25-%d=%d$ alumnes: el $\res{%s\,\%%}$.' % (F1[1], 25 - F1[1], d(Fr(25 - F1[1], 25) * 100))),
]))

# =====================================================================
# 2. Centralització i posició
Q2a = [2, 4, 4, 5, 6, 7, 7, 7, 9]; U2a = uni(Q2a)
Q2b = [12, 15, 15, 18, 20, 21, 25, 30]; U2b = uni(Q2b)
assert U2a['me'] == 6 and U2b['me'] == Fr(19)
U2c = uni(vals1, f1)
S_.append(("Paràmetres de centralització i de posició", [
 (1, r"Calcula la mitjana, la mediana, la moda i els quartils:" + tasks(1, ['$' + r',\ '.join(str(v) for v in Q2a) + '$', '$' + r',\ '.join(str(v) for v in Q2b) + '$'])
     + recorda(r"$\bar x=\frac{\sum x_if_i}{N}$. La mediana deixa la meitat de les dades per davall; $Q_1$, el 25\,\% i $Q_3$, el 75\,\%. Si $\frac N2$ cau just entre dues dades diferents, la mediana és la mitjana de totes dues."),
     tasks(1, [r'$\bar x=\frac{%s}{%d}%s\res{%s}$, \ $Me=\res{%s}$, \ $Mo=\res{%s}$, \ $Q_1=\res{%s}$, \ $Q_3=\res{%s}$' % (d(U2a['s']), U2a['N'], ap(U2a['m']), d(U2a['m']), d(U2a['me']), d(U2a['mo'][0]), d(U2a['q1']), d(U2a['q3'])),
               r'$\bar x=\frac{%s}{%d}%s\res{%s}$, \ $Me=\frac{18+20}{2}=\res{%s}$, \ $Mo=\res{%s}$, \ $Q_1=\res{%s}$, \ $Q_3=\res{%s}$' % (d(U2b['s']), U2b['N'], ap(U2b['m']), d(U2b['m']), d(U2b['me']), d(U2b['mo'][0]), d(U2b['q1']), d(U2b['q3']))])),
 (1, r"Amb la taula de l'exercici 2, calcula la nota mitjana, la mediana, la moda i els quartils.",
     r'$\bar x=\frac{%s}{25}=\res{%s}$; \ $\frac N2=12{,}5$: $Me=\res{%s}$; \ $Mo=\res{%s}$; \ $Q_1=\res{%s}$ ($\frac N4=6{,}25$), \ $Q_3=\res{%s}$ ($\frac{3N}4=18{,}75$).' % (d(U2c['s']), d(U2c['m']), d(U2c['me']), d(U2c['mo'][0]), d(U2c['q1']), d(U2c['q3']))),
 (2, r"La mitjana de 4 notes d'una alumna és 6,5. Quina nota ha de traure en el cinqué examen perquè la mitjana siga 7?",
     r"Ara suma $4\cdot6{,}5=26$; ha de sumar $5\cdot7=35$: necessita un $\res{9}$."),
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
S_.append(("Paràmetres de dispersió", [
 (1, r"Dos grups han tret aquestes notes. Calcula la mitjana, el rang, la variància i la desviació típica de cada grup. Què observes?" + tasks(1, ['Grup A: $' + r',\ '.join(map(str, A3)) + '$', 'Grup B: $' + r',\ '.join(map(str, B3)) + '$'])
     + recorda(r"$\sigma^2=\frac{\sum x_i^2f_i}{N}-\bar x^2$, \ $\sigma=\sqrt{\sigma^2}$, \ $CV=\frac{\sigma}{\bar x}$."),
     tasks(1, [r'A: $\bar x=\res{8}$, rang $\res{%s}$, $\sigma^2=\frac{%s}{%d}-64%s\res{%s}$, $\sigma%s\res{%s}$' % (d(UA['mxv'] - UA['mn']), d(UA['s2']), UA['N'], ap(UA['v']), d(UA['v']), ap(UA['sd']), d(UA['sd'])),
               r'B: $\bar x=\res{8}$, rang $\res{%s}$, $\sigma^2=\frac{%s}{%d}-64%s\res{%s}$, $\sigma%s\res{%s}$' % (d(UB['mxv'] - UB['mn']), d(UB['s2']), UB['N'], ap(UB['v']), d(UB['v']), ap(UB['sd']), d(UB['sd']))])
     + r"\par Tenen la mateixa mitjana, però les notes del grup B estan \rest{molt més disperses}."),
 (2, r"Els minuts que 40 alumnes dediquen a llegir cada dia es recullen en aquesta taula. Calcula la mitjana, la desviació típica i el coeficient de variació.\par\smallskip{\centering\small$\begin{array}{|c|" + 'c' * len(INT) + r"|}\hline\text{Minuts}&" + '&'.join(r'[%d,%d)' % (a, b) for a, b, _ in INT) + r"\\\hline f_i&" + '&'.join(str(f) for f in fi) + r"\\\hline\end{array}$\par}",
     r'Marques de classe $%s$. \ $\sum x_if_i=%s$, \ $\sum x_i^2f_i=%s$. \ $\bar x=\frac{%s}{40}%s\res{%s}$ min, \ $\sigma^2%s%s$, \ $\sigma%s\res{%s}$ min, \ $CV%s\res{%s}$ ($%s\,\%%$).' % (
         r',\ '.join(d(v) for v in mk), d(UI3['s']), d(UI3['s2']), d(UI3['s']), ap(UI3['m']), d(UI3['m']), ap(UI3['v']), d(UI3['v']), ap(UI3['sd']), d(UI3['sd']), ap(UI3['sd'] / float(UI3['m']), 3), d(UI3['sd'] / float(UI3['m']), 3), d(100 * UI3['sd'] / float(UI3['m']), 1))),
 (2, r"Dos atletes han fet aquests temps (s) en cinc curses de 100 m. Calcula la mitjana i la desviació típica de cadascun. Quin és més ràpid de mitjana? Quin és més regular?" + tasks(1, ['A: $' + r',\ '.join(d(v) for v in AT1) + '$', 'B: $' + r',\ '.join(d(v) for v in AT2) + '$']),
     tasks(1, [r'A: $\bar x=%s$ s, \ $\sigma%s%s$ s' % (d(UA1['m'], 3), ap(UA1['sd'], 3), d(UA1['sd'], 3)), r'B: $\bar x=%s$ s, \ $\sigma%s%s$ s' % (d(UA2['m'], 3), ap(UA2['sd'], 3), d(UA2['sd'], 3))])
     + r"\par " + (r"Tenen la mateixa mitjana" if UA1['m'] == UA2['m'] else (r"És més ràpid de mitjana \rest{%s}" % ('A' if UA1['m'] < UA2['m'] else 'B'))) + r"; l'atleta \rest{A és més regular} (menys dispersió)."),
 (2, r"Les altures d'un grup tenen $\bar x=165$ cm i $\sigma=8$ cm, i els pesos d'un altre grup, $\bar x=32$ kg i $\sigma=4$ kg. Quin dels dos és relativament més dispers? Per què no es poden comparar directament les desviacions típiques?",
     r"Tenen unitats i mitjanes diferents: cal el coeficient de variació. \ $CV_1=\frac{8}{165}%s%s$, \ $CV_2=\frac{4}{32}=%s$: és més dispers \rest{el segon grup} (pesos)." % (ap(cv1, 3), d(cv1, 3), d(cv2, 3))),
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
S_.append(("Variables bidimensionals. Taules de doble entrada", [
 (1, r"S'ha preguntat a 25 famílies el nombre de fills ($X$) i el nombre de cotxes ($Y$) que tenen:\par\smallskip{\centering " + tdoble(xsD, ysD, TD) + r"\par}\smallskip" + tasks(1, ["Afegeix les distribucions marginals a la taula.", "Quantes famílies tenen 2 fills i 1 cotxe? Quantes tenen més d'un cotxe?", "Calcula les mitjanes marginals $\\bar x$ i $\\bar y$."])
     + recorda(r"En una taula de doble entrada, les sumes de les files donen la distribució marginal de $X$ i les de les columnes, la de $Y$. La suma de totes les caselles és $N$."),
     r'\par{\centering ' + tdoble(xsD, ysD, TD, marg=True) + r'\par}\smallskip' + tasks(1, [r'Vegeu la taula.', r'$\res{%d}$ famílies amb 2 fills i 1 cotxe; \ $\res{%d}$ amb més d\'un cotxe (2 cotxes).' % (TD[(2, 1)], fyD[2]),
         r'$\bar x=\frac{%s}{25}=\res{%s}$, \ $\bar y=\frac{%s}{25}=\res{%s}$' % (d(BD['sx']), d(BD['mx']), d(BD['sy']), d(BD['my']))])),
 (2, r"Les notes de Matemàtiques ($X$) i de Física ($Y$) de 12 alumnes, en una escala d'1 a 3 (1 = insuficient, 2 = aprovat, 3 = notable o més), han sigut: \ " + ', '.join('$(%d,%d)$' % p for p in PAIRS4) + r". \ Construeix la taula de doble entrada i calcula les mitjanes marginals.",
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
S_.append(("Núvol de punts", [
 (1, r"Un cotxe gasta gasolina i anotem el combustible que queda al dipòsit ($Y$, en litres) al final de cada hora de viatge ($X$): \par\smallskip{\centering " + tsimple(X5, Y5) + r"\par}\smallskip Representa el núvol de punts i el centre de gravetat. Quin tipus de correlació s'hi observa?"
     + recorda(r"Cada parell $(x_i,y_i)$ és un punt. El centre de gravetat és $(\bar x,\bar y)$."),
     r'$(\bar x,\bar y)=(%s,\ %s)$. \ Els punts baixen gairebé en línia recta: correlació \rest{negativa i molt forta}.\par\smallskip{\centering ' % (d(B5['mx']), d(B5['my'])) + nuvol(list(zip(X5, Y5)), 0, 9, 35, 65, sy=5, lx='h', ly='l', cg=(B5['mx'], B5['my'])) + r'\par}'),
 (1, r"Associa cada núvol amb un d'aquests coeficients de correlació: \ $r=%s$, \ $r=%s$, \ $r=%s$, \ $r=%s$." % tuple(d(CL[i][1]) for i in ORD) + tasks(4, [r'\par' + nv(p) for p, _ in CL]),
     tasks(4, [r'$\res{r=%s}$' % d(r) for _, r in CL])),
 (1, r"Indica, per a cada parell de variables, si esperes una correlació positiva, negativa o cap correlació:" + tasks(1, ["L'altura i el pes de 30 adolescents.", "El preu d'una entrada de cinema i el nombre d'espectadors.", "La nota d'anglés i el número de sabata.", "Els quilòmetres recorreguts i la gasolina gastada.", "La temperatura exterior i el consum de calefacció.", "El mes de naixement i el nombre de germans."]),
     tasks(2, [r'\rest{positiva}', r'\rest{negativa}', r'\rest{cap}', r'\rest{positiva}', r'\rest{negativa}', r'\rest{cap}'])),
]))

# =====================================================================
# 6. Covariància
X6 = [2, 4, 5, 6, 8]; Y6 = [3, 5, 4, 7, 9]; B6 = bi(X6, Y6)
X6b = [10, 20, 30, 40, 50]; Y6b = [9, 8, 6, 5, 2]; B6b = bi(X6b, Y6b)
S_.append(("Variàncies i covariància", [
 (2, r"Per a la variable bidimensional següent, fes la taula de càlculs i troba les mitjanes, les variàncies, les desviacions típiques i la covariància:\par\smallskip{\centering " + tsimple(X6, Y6) + r"\par}"
     + recorda(r"$\sigma_x^2=\frac{\sum x_i^2}{N}-\bar x^2$, \ $\sigma_y^2=\frac{\sum y_i^2}{N}-\bar y^2$, \ $\sigma_{xy}=\frac{\sum x_iy_i}{N}-\bar x\,\bar y$."),
     r'\par{\centering ' + tcalc(X6, Y6, B6) + r'\par}\smallskip ' + calc(B6)),
 (2, r"Calcula la covariància de les dades següents i interpreta'n el signe:\par\smallskip{\centering " + tsimple(X6b, Y6b) + r"\par}",
     calc(B6b) + r" \ És negativa: quan $X$ augmenta, $Y$ tendeix a \rest{disminuir}."),
 (2, r"Calcula la covariància de les notes de Matemàtiques i de Física de la secció 4 (la taula de doble entrada de 12 alumnes).",
     r'$\sum x_iy_jf_{ij}=%s$: \ $\sigma_{xy}=\frac{%s}{12}-\bar x\,\bar y%s\res{%s}$' % (d(B4['sxy']), d(B4['sxy']), ap(B4['c'], 3), d(B4['c'], 3))),
 (2, r"Calcula la covariància de la variable bidimensional de l'exercici sobre fills i cotxes (secció 4).",
     r'$\sum x_iy_jf_{ij}=%s$: \ $\sigma_{xy}=\frac{%s}{25}-%s\cdot%s%s\res{%s}$' % (d(BD['sxy']), d(BD['sxy']), d(BD['mx']), d(BD['my']), ap(BD['c'], 3), d(BD['c'], 3))),
]))

# =====================================================================
# 7. Correlació lineal
X7 = [150, 155, 160, 165, 170, 175, 180]; Y7 = [48, 52, 55, 61, 63, 70, 72]; B7 = bi(X7, Y7)
X7d = [18, 21, 24, 27, 30, 33]; Y7d = [35, 52, 58, 75, 84, 102]; B7d = bi(X7d, Y7d)
X7b = [0, 1, 2, 3, 4, 5]; Y7b = [10, 8, 9, 6, 4, 3]; B7b = bi(X7b, Y7b)
S_.append(("Correlació lineal", [
 (2, r"Calcula el coeficient de correlació de les dades dels exercicis de la secció 6 i interpreta'l." + tasks(1, ['Les dades del primer exercici de la secció 6.', 'Les dades del segon exercici de la secció 6.', 'Fills i cotxes (secció 4).'])
     + recorda(r"$r=\dfrac{\sigma_{xy}}{\sigma_x\,\sigma_y}$, \ $-1\leq r\leq 1$. El signe dona el sentit de la relació i $|r|$, la força: prop d'1, forta; prop de 0, no hi ha correlació lineal."),
     tasks(1, [rr(B6), rr(B6b), r'$r=\dfrac{%s}{\sqrt{%s}\cdot\sqrt{%s}}%s\res{%s}$: correlació \rest{%s}.' % (d(BD['c'], 3), d(BD['vx'], 3), d(BD['vy'], 3), ap(BD['r'], 3), d(BD['r'], 3), desc(BD['r']))])),
 (2, r"L'altura (cm) i el pes (kg) de 7 persones han sigut:\par\smallskip{\centering " + tsimple(X7, Y7, 'x_i\\ (\\text{cm})', 'y_i\\ (\\text{kg})') + r"\par}\smallskip Representa el núvol de punts, calcula el coeficient de correlació i interpreta'l.",
     calc(B7) + ' ' + rr(B7) + r'\par\smallskip{\centering ' + nuvol(list(zip(X7, Y7)), 145, 185, 45, 75, sx=5, sy=5, lx='cm', ly='kg', step=(2, 1)) + r'\par}'),
 (2, r"Les hores setmanals de videojocs ($X$) i la nota d'un examen ($Y$) de 6 alumnes han sigut:\par\smallskip{\centering " + tsimple(X7b, Y7b) + r"\par}\smallskip Calcula el coeficient de correlació. Podem afirmar que jugar a videojocs fa baixar la nota?",
     calc(B7b) + ' ' + rr(B7b) + r" \ Però una correlació, encara que siga forta, \rest{no demostra que hi haja una relació de causa i efecte}: hi pot haver altres variables (el temps d'estudi, per exemple)."),
 (2, r"Una gelateria anota la temperatura màxima ($X$, en °C) i els gelats venuts ($Y$) durant sis dies:\par\smallskip{\centering " + tsimple(X7d, Y7d) + r"\par}\smallskip Calcula el coeficient de correlació i interpreta'l.",
     calc(B7d) + ' ' + rr(B7d)),
 (2, r"Calcula el coeficient de correlació entre les notes de Matemàtiques i de Física de la secció 4.",
     r'$\sigma_x^2%s%s$, \ $\sigma_y^2%s%s$, \ $\sigma_{xy}%s%s$. \ $r%s\res{%s}$: correlació \rest{%s}.' % (ap(B4['vx'], 3), d(B4['vx'], 3), ap(B4['vy'], 3), d(B4['vy'], 3), ap(B4['c'], 3), d(B4['c'], 3), ap(B4['r'], 3), d(B4['r'], 3), desc(B4['r']))),
 (1, r"Si el coeficient de correlació entre dues variables és $r=0{,}8$ i les desviacions típiques són $\sigma_x=2$ i $\sigma_y=5$, quant val la covariància?",
     r"$\sigma_{xy}=r\,\sigma_x\,\sigma_y=0{,}8\cdot2\cdot5=\res{8}$."),
 (1, r"Si $\sigma_{xy}=-12$, $\sigma_x=4$ i $\sigma_y=5$, quant val $r$? I si $\sigma_{xy}=3$, $\sigma_x=2$ i $\sigma_y=1$? És possible?",
     r"$r=\frac{-12}{4\cdot5}=\res{-0{,}6}$ (negativa moderada). \ En el segon cas eixiria $r=\frac{3}{2}=1{,}5>1$: \rest{no és possible}, hi ha un error en les dades."),
 (3, r"Una variable bidimensional té $N=10$, $\sum x_i=50$, $\sum y_i=80$, $\sum x_i^2=290$, $\sum y_i^2=730$ i $\sum x_iy_i=440$. Calcula $r$.",
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
S_.append(("Recta de regressió", [
 (2, r"Amb les dades del primer exercici de la secció 6, troba la recta de regressió de $Y$ sobre $X$ i la de $X$ sobre $Y$. Estima el valor de $y$ per a $x=7$ i el de $x$ per a $y=6$."
     + recorda(r"Recta de regressió de $Y$ sobre $X$: \ $y-\bar y=\dfrac{\sigma_{xy}}{\sigma_x^2}(x-\bar x)$. \ De $X$ sobre $Y$: \ $x-\bar x=\dfrac{\sigma_{xy}}{\sigma_y^2}(y-\bar y)$. Les estimacions són fiables si $|r|$ és prop d'1 i no ens n'eixim de l'interval de les dades."),
     r'$Y$ sobre $X$: $y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$; \ $\hat y(7)%s\res{%s}$. \ $X$ sobre $Y$: $x-%s=\frac{%s}{%s}(y-%s)\Rightarrow\res{%s}$; \ $\hat x(6)%s\res{%s}$. \ Són fiables: $r%s%s$ i els valors són dins de les dades.' % (
         d(B6['my'], 3), d(B6['c'], 3), d(B6['vx'], 3), d(B6['mx'], 3), eqr(m6, n6), ap(est(m6, n6, 7), 3), d(est(m6, n6, 7), 3),
         d(B6['mx'], 3), d(B6['c'], 3), d(B6['vy'], 3), d(B6['my'], 3), eqr(m6i, n6i, 'x', 'y'), ap(est(m6i, n6i, 6), 3), d(est(m6i, n6i, 6), 3), ap(B6['r'], 3), d(B6['r'], 3))),
 (2, r"Amb les altures i els pesos de la secció 7, troba la recta de regressió del pes sobre l'altura. Quin pes s'estima per a una persona de 168 cm? I per a un xiquet de 120 cm? Són fiables les dues estimacions?",
     r'$y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$. \ $\hat y(168)%s\res{%s\text{ kg}}$: \rest{fiable} ($r%s%s$ i 168 és dins de les dades). \ $\hat y(120)%s%s$ kg: \rest{no és fiable}, 120 cm queda molt lluny de l\'interval $[150,180]$.' % (
         d(B7['my'], 3), d(B7['c'], 3), d(B7['vx'], 3), d(B7['mx'], 3), eqr(m7, n7), ap(est(m7, n7, 168), 2), d(est(m7, n7, 168), 2), ap(B7['r'], 3), d(B7['r'], 3), ap(est(m7, n7, 120), 2), d(est(m7, n7, 120), 2))),
 (2, r"Amb les dades de la gelateria de la secció 7, quants gelats s'estima que es vendran un dia amb una màxima de 25 °C?",
     r'Recta: $\res{%s}$. \ $\hat y(25)%s%s$: uns $\res{%d}$ gelats. Molt fiable: $r%s%s$.' % (eqr(m7d, n7d), ap(est(m7d, n7d, 25), 2), d(est(m7d, n7d, 25), 2), round(est(m7d, n7d, 25)), ap(B7d['r'], 3), d(B7d['r'], 3))),
 (2, r"Amb les sumes de l'últim exercici de la secció 7 ($N=10$, $\sum x_i=50$, $\sum y_i=80$, $\sum x_i^2=290$, $\sum x_iy_i=440$), troba la recta de regressió de $Y$ sobre $X$ i estima $y$ per a $x=6$.",
     r'$\bar x=5$, $\bar y=8$, $\sigma_x^2=4$, $\sigma_{xy}=4$: \ $y-8=\frac44(x-5)\Rightarrow\res{%s}$; \ $\hat y(6)=\res{%s}$ (poc precisa: $r%s%s$ és moderat).' % (eqr(m7c, n7c), d(est(m7c, n7c, 6)), ap(B7c['r'], 3), d(B7c['r'], 3))),
 (3, r"Les rectes de regressió d'una variable bidimensional són $y=0{,}5x+2$ (de $Y$ sobre $X$) i $x=1{,}2y-1$ (de $X$ sobre $Y$). Calcula $\bar x$, $\bar y$ i el coeficient de correlació. (Pista: les dues rectes passen per $(\bar x,\bar y)$, i el producte dels seus pendents és $\frac{\sigma_{xy}}{\sigma_x^2}\cdot\frac{\sigma_{xy}}{\sigma_y^2}=r^2$.)",
     r'Substituint: $x=1{,}2(0{,}5x+2)-1=0{,}6x+1{,}4\Rightarrow\bar x=\res{%s}$, \ $\bar y=\res{%s}$. \ $r^2=0{,}5\cdot1{,}2=0{,}6$ i, com que els pendents són positius, $r=\sqrt{0{,}6}%s\res{%s}$.' % (d(cx), d(cy), ap(r2, 3), d(r2, 3))),
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
S_.append(("Altres tipus de relació. Correlació i causalitat", [
 (2, r"Observa aquests núvols de punts. Descriu la relació que hi ha entre les variables i digues si el coeficient de correlació lineal serà pròxim a 0 o no." + tasks(3, [r'\par' + nv(p) for p in NL]),
     tasks(1, [r'Relació \rest{parabòlica} (creix i després decreix): és forta, però no és lineal i $r\approx%s$, \rest{pròxim a 0}.' % d(rNL[0]),
               r'Relació \rest{exponencial}: creixent, $r\approx%s$ és alt, però els punts no segueixen una recta.' % d(rNL[1]),
               r'Els punts de baix no tenen cap relació, però el \rest{valor atípic} $(9,9)$ fa que $r\approx%s$. Cal revisar-lo abans de traure conclusions.' % d(rNL[2])])),
 (2, r"En un estudi de diverses ciutats s'ha trobat una correlació positiva forta entre el nombre de bombers que actuen en un incendi i els danys que causa. Vol dir que els bombers causen els danys? Quina explicació hi pot haver?",
     r"\rest{No}: la correlació no implica causalitat. Hi ha una tercera variable, la \rest{grandària de l'incendi}: com més gran és, més bombers hi van i més danys causa."),
 (1, r"Raona si són vertaderes o falses: \ a) Si $r=0$, les variables no tenen cap relació. \ b) Si $r=-0{,}98$, la relació és molt feble perquè $r$ és negatiu. \ c) Si tots els punts són sobre una recta creixent, $r=1$.",
     r"a) \rest{Falsa}: només vol dir que no hi ha relació lineal (pot ser parabòlica, per exemple). \ b) \rest{Falsa}: és molt forta; el signe indica que és inversa. \ c) \rest{Vertadera}."),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={estadística, freqüències, mitjana, mediana, quartils, variància, desviació típica, coeficient de variació, variable bidimensional, taula de doble entrada, núvol de punts, covariància, correlació lineal}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
pre += r'''\providecommand{\gt}{>}\providecommand{\lt}{<}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def fix(t):
    """Fora dels dibuixos: l'espai després de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = "Estadística"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 10: %s. 1r de Batxillerat MI}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 10: %s · 1r Batxillerat MI" % (t, TIT))
    assert 'Estadística · 1r' in p and 'unitat 10: Estadística' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques I}{1r Batx}{''' + ('Solucions de la fitxa · Unitat 10' if sol else "Fitxa d'exercicis · Unitat 10") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb les calculadores dels apunts interactius de la unitat."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos: per a les variables bidimensionals, fes sempre la taula amb les columnes $x_i$, $y_i$, $x_i^2$, $y_i^2$ i $x_iy_i$. Arredoneix els resultats a dues o tres xifres decimals. Pots comprovar-los amb les calculadores dels apunts interactius.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb la calculadora bidimensional dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't10-fitxa-solucions.tex' if sol else 't10-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis;', NCHK[0], 'comprovacions')
