# Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (1r Batxillerat CCSS, Unitat 8: Distribucions bidimensionals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Bilingüe: T(valencià, castellà); genera-es.py l'executa amb FM_LANG=es i escriu els -es.tex.
# Les eines i molts exercicis vénen de la part bidimensional de la fitxa de la unitat 10 de 1r Batx MI (_eines/fonts-latex/1batx-mi-t10),
# reorganitzats en les 6 seccions dels apunts (8.1-8.6) i amb exercicis nous: dades agrupades en intervals i distribucions condicionades,
# tipus de dependència, canvi d'unitats i les dues rectes de regressió (publicitat i vendes, a partir de r i de les desviacions,
# rectes donades sense dir quina és quina, rectes que no poden ser de regressió).
# Tots els resultats numèrics de les solucions es CALCULEN aquí (bi(), dbl() amb Fraction) i es formaten amb d(): no s'escriuen
# a mà; per a cada recta es comprova que passa per (x̄, ȳ), que fa mínima la suma de quadrats i que m_yx·m_xy = r².
# Els núvols de punts es dibuixen amb TikZ (nuvol()).
# Ús: python3 genera.py && python3 genera-es.py, i pdflatex (dues vegades) dels quatre .tex
import os, re, math, random
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va
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
    if a < 0.2: return T('pràcticament nul·la (no hi ha correlació lineal)', 'prácticamente nula (no hay correlación lineal)')
    return ('positiva' if r > 0 else 'negativa') + ' ' + (T('molt forta', 'muy fuerte') if a > 0.95 else T('forta', 'fuerte') if a >= 0.8 else 'moderada' if a >= 0.5 else T('feble', 'débil'))
CORR = T('correlació', 'correlación')

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
    return r'$r=\dfrac{\sigma_{xy}}{\sigma_x\sigma_y}%s\res{%s}$: %s \rest{%s}.' % (ap(B['r'], 3), d(B['r'], 3), CORR, desc(B['r']))

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
# 1. Distribucions bidimensionals. Taules de freqüències
TD = {(1, 0): 4, (1, 1): 2, (1, 2): 0, (2, 0): 3, (2, 1): 6, (2, 2): 3, (3, 0): 0, (3, 1): 3, (3, 2): 4}
xsD, ysD = [1, 2, 3], [0, 1, 2]; BD = bi(*dbl(TD))
fxD = [sum(TD[(a, b)] for b in ysD) for a in xsD]; fyD = [sum(TD[(a, b)] for a in xsD) for b in ysD]
PAIRS4 = [(2, 1), (3, 2), (2, 2), (1, 1), (3, 3), (2, 1), (1, 1), (2, 2), (3, 2), (2, 2), (1, 2), (3, 3)]
T4 = {}
for p in PAIRS4: T4[p] = T4.get(p, 0) + 1
x4 = sorted(set(p[0] for p in PAIRS4)); y4 = sorted(set(p[1] for p in PAIRS4)); B4 = bi(*dbl(T4))
# dades agrupades: hores d'estudi (X) i nota (Y) de 50 alumnes
XI = [(0, 2), (2, 4), (4, 6)]; YI = [(0, 5), (5, 7), (7, 10)]
FI = [[8, 4, 1], [5, 10, 6], [1, 5, 10]]
mxI = [Fr(a + b, 2) for a, b in XI]; myI = [Fr(a + b, 2) for a, b in YI]
TI = {(mxI[i], myI[j]): FI[i][j] for i in range(3) for j in range(3)}; BI = bi(*dbl(TI))
NI = sum(map(sum, FI)); fxI = [sum(r) for r in FI]; fyI = [sum(FI[i][j] for i in range(3)) for j in range(3)]
assert NI == 50 and BI['N'] == 50
def iv(a, b, last=False): return r'{[%s,%s%s}' % (d(a), d(b), ']' if last else ')')  # entre claus: un «[» darrere de \\ seria un argument opcional
def tint(marg=False):
    cols = 'c|' * 3 + ('c|' if marg else '')
    h = r'{\small$\begin{array}{|c|' + cols + r'}\hline X\backslash Y & ' + ' & '.join(iv(a, b, k == 2) for k, (a, b) in enumerate(YI)) + (r' & f_x' if marg else '') + r'\\\hline '
    for i, (a, b) in enumerate(XI):
        h += iv(a, b) + ' & ' + ' & '.join(str(v) for v in FI[i]) + ((' & ' + str(fxI[i])) if marg else '') + r'\\' + (r'\hline ' if i == 2 else ' ')
    if marg: h += 'f_y & ' + ' & '.join(str(v) for v in fyI) + ' & ' + str(NI) + r'\\\hline '
    return h + r'\end{array}$}'
def pc(a, b): return d(Fr(a, b) * 100, 1)
def pq(a, b): return r'\frac{%d}{%d}%s\res{%s\,\%%}' % (a, b, ap(Fr(a, b) * 100, 1), pc(a, b))
S_.append((T("Distribucions bidimensionals. Taules de freqüències", "Distribuciones bidimensionales. Tablas de frecuencias"), [
 (1, T(r"S'ha preguntat a 25 famílies el nombre de fills ($X$) i el nombre de cotxes ($Y$) que tenen:", r"Se ha preguntado a 25 familias el número de hijos ($X$) y el número de coches ($Y$) que tienen:") + r"\par\smallskip{\centering " + tdoble(xsD, ysD, TD) + r"\par}\smallskip"
     + tasks(1, [T("Afegeix les distribucions marginals a la taula.", "Añade las distribuciones marginales a la tabla."), T("Quantes famílies tenen 2 fills i 1 cotxe? Quantes en tenen més d'un?", "¿Cuántas familias tienen 2 hijos y 1 coche? ¿Cuántas tienen más de uno?"), T("Calcula les mitjanes marginals $\\bar x$ i $\\bar y$.", "Calcula las medias marginales $\\bar x$ y $\\bar y$.")])
     + recorda(T(r"En una taula de doble entrada, les sumes de les files donen la distribució marginal de $X$ i les de les columnes, la de $Y$. La suma de totes les caselles és $N$.", r"En una tabla de doble entrada, las sumas de las filas dan la distribución marginal de $X$ y las de las columnas, la de $Y$. La suma de todas las casillas es $N$.")),
     r'\par{\centering ' + tdoble(xsD, ysD, TD, marg=True) + r'\par}\smallskip' + tasks(1, [T(r'Vegeu la taula.', r'Véase la tabla.'), T(r"$\res{%d}$ famílies amb 2 fills i 1 cotxe; \ $\res{%d}$ amb més d'un cotxe (2 cotxes).", r'$\res{%d}$ familias con 2 hijos y 1 coche; \ $\res{%d}$ con más de un coche (2 coches).') % (TD[(2, 1)], fyD[2]),
         r'$\bar x=\frac{%s}{25}=\res{%s}$, \ $\bar y=\frac{%s}{25}=\res{%s}$' % (d(BD['sx']), d(BD['mx']), d(BD['sy']), d(BD['my']))])),
 (2, T(r"Les notes de Matemàtiques ($X$) i de Física ($Y$) de 12 alumnes, en una escala d'1 a 3 (1 = insuficient, 2 = aprovat, 3 = notable o més), han sigut: \ ", r"Las notas de Matemáticas ($X$) y de Física ($Y$) de 12 alumnos, en una escala de 1 a 3 (1 = insuficiente, 2 = aprobado, 3 = notable o más), han sido: \ ") + ', '.join('$(%d,%d)$' % p for p in PAIRS4) + T(r". \ Construeix la taula de doble entrada i calcula les mitjanes marginals.", r". \ Construye la tabla de doble entrada y calcula las medias marginales."),
     r'\par{\centering ' + tdoble(x4, y4, T4, marg=True) + r'\par}\smallskip $\bar x=\frac{%s}{12}%s\res{%s}$, \ $\bar y=\frac{%s}{12}%s\res{%s}$.' % (d(B4['sx']), ap(B4['mx']), d(B4['mx']), d(B4['sy']), ap(B4['my']), d(B4['my']))),
 (2, T(r"Les hores d'estudi setmanals ($X$) i la nota final ($Y$) de 50 alumnes, agrupades en intervals, es recullen en aquesta taula:", r"Las horas de estudio semanales ($X$) y la nota final ($Y$) de 50 alumnos, agrupadas en intervalos, se recogen en esta tabla:") + r"\par\smallskip{\centering " + tint() + r"\par}\smallskip"
     + tasks(1, [T("Afegeix les distribucions marginals i calcula les mitjanes marginals (fes servir les marques de classe).", "Añade las distribuciones marginales y calcula las medias marginales (usa las marcas de clase)."),
                 T("Quin percentatge d'alumnes estudia entre 2 i 4 hores i trau un 7 o més?", "¿Qué porcentaje de alumnos estudia entre 2 y 4 horas y saca un 7 o más?"),
                 T("Dels alumnes que estudien 4 hores o més, quin percentatge trau un 7 o més? I dels que estudien menys de 2 hores?", "De los alumnos que estudian 4 horas o más, ¿qué porcentaje saca un 7 o más? ¿Y de los que estudian menos de 2 horas?"),
                 T("Dels alumnes que han suspés (nota menor que 5), quin percentatge estudia menys de 2 hores?", "De los alumnos que han suspendido (nota menor que 5), ¿qué porcentaje estudia menos de 2 horas?")])
     + recorda(T(r"La marca de classe és el punt mitjà de l'interval. Una distribució condicionada és una fila o una columna: els percentatges es calculen respecte del total d'aquella fila o columna.", r"La marca de clase es el punto medio del intervalo. Una distribución condicionada es una fila o una columna: los porcentajes se calculan respecto del total de esa fila o columna.")),
     r'\par{\centering ' + tint(True) + r'\par}\smallskip' + tasks(1, [
         T(r'Marques de classe: $X$: $%s$; \ $Y$: $%s$. \ $\bar x=\frac{%s}{50}=\res{%s}$ h, \ $\bar y=\frac{%s}{50}=\res{%s}$', r'Marcas de clase: $X$: $%s$; \ $Y$: $%s$. \ $\bar x=\frac{%s}{50}=\res{%s}$ h, \ $\bar y=\frac{%s}{50}=\res{%s}$') % (r',\ '.join(d(v) for v in mxI), r';\ '.join(d(v) for v in myI), d(BI['sx']), d(BI['mx']), d(BI['sy']), d(BI['my'])),
         r'$\frac{%d}{50}=%s$: \ $\res{%s\,\%%}$' % (FI[1][2], d(Fr(FI[1][2], 50)), pc(FI[1][2], 50)),
         T(r'$%s$; \ dels que estudien menys de 2 h, $%s$.', r'$%s$; \ de los que estudian menos de 2 h, $%s$.') % (pq(FI[2][2], fxI[2]), pq(FI[0][2], fxI[0])),
         r'$%s$' % pq(FI[0][0], fyI[0])])),
]))
assert sum(TD.values()) == 25 and sum(T4.values()) == 12

# =====================================================================
# 2. Núvol de punts
X5 = [1, 2, 3, 4, 5, 6, 7, 8]; Y5 = [62, 60, 55, 53, 50, 46, 44, 40]
B5 = bi(X5, Y5)
CL = [(gen(25, 0.9, 1), 0.9), (gen(25, -0.95, 2), -0.95), (gen(25, 0.0, 3), 0.0), (gen(25, -0.5, 4), -0.5)]
for pts, r in CL: assert abs(rnum(pts) - r) < 1e-9; NCHK[0] += 1
ORD = [2, 0, 3, 1]  # ordre en què es mostren els valors de r a l'enunciat
S_.append((T("Núvol de punts", "Nube de puntos"), [
 (1, T(r"Un cotxe gasta gasolina i anotem el combustible que queda al dipòsit ($Y$, en litres) al final de cada hora de viatge ($X$):", r"Un coche gasta gasolina y anotamos el combustible que queda en el depósito ($Y$, en litros) al final de cada hora de viaje ($X$):") + r" \par\smallskip{\centering " + tsimple(X5, Y5) + r"\par}\smallskip " + T("Representa el núvol de punts i el centre de gravetat. Quin tipus de correlació s'hi observa?", "Representa la nube de puntos y el centro de gravedad. ¿Qué tipo de correlación se observa?")
     + recorda(T(r"Cada parell $(x_i,y_i)$ és un punt. El centre de gravetat és $(\bar x,\bar y)$.", r"Cada par $(x_i,y_i)$ es un punto. El centro de gravedad es $(\bar x,\bar y)$.")),
     r'$(\bar x,\bar y)=(%s;\ %s)$. \ ' % (d(B5['mx']), d(B5['my'])) + T(r"Els punts baixen gairebé en línia recta: correlació \rest{negativa i molt forta}.", r"Los puntos bajan casi en línea recta: correlación \rest{negativa y muy fuerte}.") + r'\par\smallskip{\centering ' + nuvol(list(zip(X5, Y5)), 0, 9, 35, 65, sy=5, lx='h', ly='l', cg=(B5['mx'], B5['my'])) + r'\par}'),
 (1, T(r"Associa cada núvol amb un d'aquests coeficients de correlació:", r"Asocia cada nube con uno de estos coeficientes de correlación:") + r" \ $r=%s$, \ $r=%s$, \ $r=%s$, \ $r=%s$." % tuple(d(CL[i][1]) for i in ORD) + tasks(4, [r'\par' + nv(p) for p, _ in CL]),
     tasks(4, [r'$\res{r=%s}$' % d(r) for _, r in CL])),
 (1, T(r"Indica, per a cada parell de variables, si esperes una correlació positiva, negativa o cap correlació:", r"Indica, para cada par de variables, si esperas una correlación positiva, negativa o ninguna correlación:")
     + tasks(1, T(["L'altura i el pes de 30 adolescents.", "El preu d'una entrada de cinema i el nombre d'espectadors.", "La nota d'anglés i el número de sabata.", "Els quilòmetres recorreguts i la gasolina gastada.", "La temperatura exterior i el consum de calefacció.", "La renda d'una família i la seua despesa en viatges."],
                  ["La altura y el peso de 30 adolescentes.", "El precio de una entrada de cine y el número de espectadores.", "La nota de inglés y el número de zapato.", "Los kilómetros recorridos y la gasolina gastada.", "La temperatura exterior y el consumo de calefacción.", "La renta de una familia y su gasto en viajes."])),
     tasks(2, [r'\rest{positiva}', r'\rest{negativa}', T(r'\rest{cap}', r'\rest{ninguna}'), r'\rest{positiva}', r'\rest{negativa}', r'\rest{positiva}'])),
]))

# =====================================================================
# 3. Correlació i regressió. Tipus de dependència
DEP = [[(0.5 + 0.45 * i, 0.5 + 0.1 * (0.5 + 0.45 * i) ** 2) for i in range(21)], gen(25, 0.85, 6), gen(25, 0.0, 7)]
assert abs(rnum(DEP[1]) - 0.85) < 1e-9 and abs(rnum(DEP[2])) < 1e-9 and max(p[1] for p in DEP[0]) <= 10; NCHK[0] += 1
S_.append((T("Correlació i regressió. Tipus de dependència", "Correlación y regresión. Tipos de dependencia"), [
 (1, T(r"Digues si la dependència entre les variables és funcional, estadística o si són independents:", r"Di si la dependencia entre las variables es funcional, estadística o si son independientes:")
     + tasks(1, T(["El costat d'un quadrat i el seu perímetre.", "Les hores de sol d'un dia i les vendes de crema solar.", "El número de DNI i l'altura.", "Els anys d'experiència i el sou d'un treballador.", "El preu d'un trajecte en taxi i els quilòmetres (tarifa fixa).", "Les hores d'entrenament i el temps en una cursa."],
                  ["El lado de un cuadrado y su perímetro.", "Las horas de sol de un día y las ventas de crema solar.", "El número de DNI y la altura.", "Los años de experiencia y el sueldo de un trabajador.", "El precio de un trayecto en taxi y los kilómetros (tarifa fija).", "Las horas de entrenamiento y el tiempo en una carrera."]))
     + recorda(T(r"\textbf{Funcional}: una variable determina exactament l'altra ($y=f(x)$). \textbf{Estadística}: hi ha relació, però no exacta (núvol al voltant d'una línia). \textbf{Independents}: no hi ha cap relació.", r"\textbf{Funcional}: una variable determina exactamente la otra ($y=f(x)$). \textbf{Estadística}: hay relación, pero no exacta (nube alrededor de una línea). \textbf{Independientes}: no hay ninguna relación.")),
     tasks(3, [r'\rest{funcional} ($y=4x$)', r'\rest{estadística}', T(r'\rest{independents}', r'\rest{independientes}'), r'\rest{estadística}', r'\rest{funcional}', r'\rest{estadística}'])),
 (1, T(r"Quin tipus de dependència mostra cada núvol de punts? En quin té sentit buscar una recta de regressió per a fer estimacions?", r"¿Qué tipo de dependencia muestra cada nube de puntos? ¿En cuál tiene sentido buscar una recta de regresión para hacer estimaciones?") + tasks(3, [r'\par' + nv(p) for p in DEP]),
     tasks(1, [T(r"\rest{Funcional}: els punts són exactament sobre una corba (no és una recta: la regressió lineal no és l'adequada).", r'\rest{Funcional}: los puntos están exactamente sobre una curva (no es una recta: la regresión lineal no es la adecuada).'),
               T(r"\rest{Estadística}: núvol allargat al voltant d'una recta creixent. Ací sí que té sentit buscar una recta de regressió.", r'\rest{Estadística}: nube alargada alrededor de una recta creciente. Aquí sí tiene sentido buscar una recta de regresión.'),
               T(r'\rest{Independència}: el núvol no té cap forma.', r'\rest{Independencia}: la nube no tiene ninguna forma.')])),
 (2, T(r"En un estudi de diverses ciutats s'ha trobat una correlació positiva forta entre el nombre de bombers que actuen en un incendi i els danys que causa. Vol dir que els bombers causen els danys? Quina explicació hi pot haver?", r"En un estudio de varias ciudades se ha encontrado una correlación positiva fuerte entre el número de bomberos que actúan en un incendio y los daños que causa. ¿Quiere decir que los bomberos causan los daños? ¿Qué explicación puede haber?"),
     T(r"\rest{No}: la correlació no implica causalitat. Hi ha una tercera variable, la \rest{grandària de l'incendi}: com més gran és, més bombers hi van i més danys causa.", r"\rest{No}: la correlación no implica causalidad. Hay una tercera variable, el \rest{tamaño del incendio}: cuanto mayor es, más bomberos van y más daños causa.")),
]))

# =====================================================================
# 4. Correlació lineal. Covariància
X6 = [2, 4, 5, 6, 8]; Y6 = [3, 5, 4, 7, 9]; B6 = bi(X6, Y6)
X6b = [10, 20, 30, 40, 50]; Y6b = [9, 8, 6, 5, 2]; B6b = bi(X6b, Y6b)
S_.append((T("Correlació lineal. Covariància", "Correlación lineal. Covarianza"), [
 (2, T(r"Per a la variable bidimensional següent, fes la taula de càlculs i troba les mitjanes, les variàncies, les desviacions típiques i la covariància:", r"Para la variable bidimensional siguiente, haz la tabla de cálculos y halla las medias, las varianzas, las desviaciones típicas y la covarianza:") + r"\par\smallskip{\centering " + tsimple(X6, Y6) + r"\par}"
     + recorda(r"$\sigma_x^2=\frac{\sum x_i^2}{N}-\bar x^2$, \ $\sigma_y^2=\frac{\sum y_i^2}{N}-\bar y^2$, \ $\sigma_{xy}=\frac{\sum x_iy_i}{N}-\bar x\,\bar y$."),
     r'\par{\centering ' + tcalc(X6, Y6, B6) + r'\par}\smallskip ' + calc(B6)),
 (2, T(r"Calcula la covariància de les dades següents i interpreta'n el signe:", r"Calcula la covarianza de los datos siguientes e interpreta su signo:") + r"\par\smallskip{\centering " + tsimple(X6b, Y6b) + r"\par}",
     calc(B6b) + T(r" \ És negativa: quan $X$ augmenta, $Y$ tendeix a \rest{disminuir}.", r" \ Es negativa: cuando $X$ aumenta, $Y$ tiende a \rest{disminuir}.")),
 (2, T(r"Calcula la covariància de les notes de Matemàtiques i de Física de l'exercici 2 (la taula de doble entrada de 12 alumnes).", r"Calcula la covarianza de las notas de Matemáticas y de Física del ejercicio 2 (la tabla de doble entrada de 12 alumnos)."),
     r'$\sum x_iy_jf_{ij}=%s$: \ $\sigma_{xy}=\frac{%s}{12}-\bar x\,\bar y%s\res{%s}$' % (d(B4['sxy']), d(B4['sxy']), ap(B4['c'], 3), d(B4['c'], 3))),
 (2, T(r"Calcula la covariància de la variable bidimensional de l'exercici 1 (fills i cotxes).", r"Calcula la covarianza de la variable bidimensional del ejercicio 1 (hijos y coches)."),
     r'$\sum x_iy_jf_{ij}=%s$: \ $\sigma_{xy}=\frac{%s}{25}-%s\cdot%s%s\res{%s}$' % (d(BD['sxy']), d(BD['sxy']), d(BD['mx']), d(BD['my']), ap(BD['c'], 3), d(BD['c'], 3))),
 (3, T(r"Calcula les variàncies i la covariància de les hores d'estudi i les notes de l'exercici 3 (dades agrupades). Com és la relació?", r"Calcula las varianzas y la covarianza de las horas de estudio y las notas del ejercicio 3 (datos agrupados). ¿Cómo es la relación?")
     + recorda(T(r"Amb dades agrupades, cada casella aporta $x_i\,y_j\,f_{ij}$ (amb les marques de classe): $\sigma_{xy}=\frac{\sum x_iy_jf_{ij}}{N}-\bar x\,\bar y$.", r"Con datos agrupados, cada casilla aporta $x_i\,y_j\,f_{ij}$ (con las marcas de clase): $\sigma_{xy}=\frac{\sum x_iy_jf_{ij}}{N}-\bar x\,\bar y$.")),
     r'$\sum x_i^2f_x=%s$, \ $\sum y_j^2f_y=%s$, \ $\sum x_iy_jf_{ij}=%s$. \ $\sigma_x^2=\frac{%s}{50}-%s^2%s\res{%s}$, \ $\sigma_y^2=\frac{%s}{50}-%s^2%s\res{%s}$, \ $\sigma_{xy}=\frac{%s}{50}-%s\cdot%s%s\res{%s}$. \ ' % (
         d(BI['sx2']), d(BI['sy2']), d(BI['sxy']), d(BI['sx2']), d(BI['mx']), ap(BI['vx'], 3), d(BI['vx'], 3), d(BI['sy2']), d(BI['my'], 3), ap(BI['vy'], 3), d(BI['vy'], 3), d(BI['sxy']), d(BI['mx']), d(BI['my'], 3), ap(BI['c'], 3), d(BI['c'], 3))
     + T(r"És positiva: \rest{com més hores d'estudi, més nota} (tendència).", r"Es positiva: \rest{cuantas más horas de estudio, más nota} (tendencia).")),
]))
assert BI['c'] > 0

# =====================================================================
# 5. Coeficient de correlació
X7 = [150, 155, 160, 165, 170, 175, 180]; Y7 = [48, 52, 55, 61, 63, 70, 72]; B7 = bi(X7, Y7)
X7d = [18, 21, 24, 27, 30, 33]; Y7d = [35, 52, 58, 75, 84, 102]; B7d = bi(X7d, Y7d)
X7b = [0, 1, 2, 3, 4, 5]; Y7b = [10, 8, 9, 6, 4, 3]; B7b = bi(X7b, Y7b)
B7c = dict(N=10, sx=Fr(50), sy=Fr(80), sx2=Fr(290), sy2=Fr(730), sxy=Fr(440))
B7c.update(mx=B7c['sx'] / 10, my=B7c['sy'] / 10); B7c.update(vx=B7c['sx2'] / 10 - B7c['mx'] ** 2, vy=B7c['sy2'] / 10 - B7c['my'] ** 2, c=B7c['sxy'] / 10 - B7c['mx'] * B7c['my'])
B7c.update(sdx=math.sqrt(B7c['vx']), sdy=math.sqrt(B7c['vy'])); B7c['r'] = float(B7c['c']) / (B7c['sdx'] * B7c['sdy']); NCHK[0] += 1
assert abs(Fr(-12, 20)) == Fr(3, 5)
# canvi d'unitats: altura en metres
B7m = bi([Fr(v, 100) for v in X7], Y7)
assert B7m['c'] == B7['c'] / 100 and abs(B7m['r'] - B7['r']) < 1e-12
rnd = random.Random(5)
NL = [[(x, 9 - 0.35 * (x - 5) ** 2 + rnd.uniform(-0.6, 0.6)) for x in [0.3 + 0.4 * i for i in range(24)]],
      [(x, 0.15 * math.exp(0.42 * x) + rnd.uniform(-0.25, 0.25)) for x in [0.3 + 0.4 * i for i in range(24)]],
      [(1 + 0.15 * i, 1.2 + rnd.uniform(-0.6, 0.6)) for i in range(8)] + [(9, 9)]]
rNL = [rnum(p) for p in NL]
assert abs(rNL[0]) < 0.3 and rNL[1] > 0.8 and rNL[2] > 0.9; NCHK[0] += 1
def rq(B): return r'$r=\dfrac{%s}{\sqrt{%s}\cdot\sqrt{%s}}%s\res{%s}$: %s \rest{%s}.' % (d(B['c'], 3), d(B['vx'], 3), d(B['vy'], 3), ap(B['r'], 3), d(B['r'], 3), CORR, desc(B['r']))
S_.append((T("Coeficient de correlació lineal", "Coeficiente de correlación lineal"), [
 (2, T(r"Calcula el coeficient de correlació de les dades dels exercicis de la secció 4 i interpreta'l.", r"Calcula el coeficiente de correlación de los datos de los ejercicios de la sección 4 e interprétalo.")
     + tasks(1, T(['Les dades del primer exercici de la secció 4.', 'Les dades del segon exercici de la secció 4.', 'Fills i cotxes (exercici 1).', "Hores d'estudi i notes agrupades (exercici 3)."], ['Los datos del primer ejercicio de la sección 4.', 'Los datos del segundo ejercicio de la sección 4.', 'Hijos y coches (ejercicio 1).', 'Horas de estudio y notas agrupadas (ejercicio 3).']))
     + recorda(T(r"$r=\dfrac{\sigma_{xy}}{\sigma_x\,\sigma_y}$, \ $-1\leq r\leq 1$. El signe dona el sentit de la relació i $|r|$, la força: prop d'1, forta; prop de 0, no hi ha correlació lineal.", r"$r=\dfrac{\sigma_{xy}}{\sigma_x\,\sigma_y}$, \ $-1\leq r\leq 1$. El signo da el sentido de la relación y $|r|$, la fuerza: cerca de 1, fuerte; cerca de 0, no hay correlación lineal.")),
     tasks(1, [rr(B6), rr(B6b), rq(BD), rq(BI)])),
 (2, T(r"L'altura (cm) i el pes (kg) de 7 persones han sigut:", r"La altura (cm) y el peso (kg) de 7 personas han sido:") + r"\par\smallskip{\centering " + tsimple(X7, Y7, 'x_i\\ (\\text{cm})', 'y_i\\ (\\text{kg})') + r"\par}\smallskip " + T("Representa el núvol de punts, calcula el coeficient de correlació i interpreta'l.", "Representa la nube de puntos, calcula el coeficiente de correlación e interprétalo."),
     calc(B7) + ' ' + rr(B7) + r'\par\smallskip{\centering ' + nuvol(list(zip(X7, Y7)), 145, 185, 45, 75, sx=5, sy=5, lx='cm', ly='kg', step=(2, 1)) + r'\par}'),
 (1, T(r"Si en l'exercici anterior expressem l'altura en metres en lloc de centímetres, què els passa a la covariància i al coeficient de correlació?", r"Si en el ejercicio anterior expresamos la altura en metros en lugar de centímetros, ¿qué les pasa a la covarianza y al coeficiente de correlación?"),
     T(r"Tots els $x_i$ es divideixen entre 100 i la covariància també: $\sigma_{xy}%s\res{%s}$. En canvi, $r$ \rest{no canvia} ($r%s%s$), perquè no depén de les unitats.", r"Todos los $x_i$ se dividen entre 100 y la covarianza también: $\sigma_{xy}%s\res{%s}$. En cambio, $r$ \rest{no cambia} ($r%s%s$), porque no depende de las unidades.") % (ap(B7m['c'], 4), d(B7m['c'], 4), ap(B7m['r'], 3), d(B7m['r'], 3))),
 (2, T(r"Les hores setmanals de videojocs ($X$) i la nota d'un examen ($Y$) de 6 alumnes han sigut:", r"Las horas semanales de videojuegos ($X$) y la nota de un examen ($Y$) de 6 alumnos han sido:") + r"\par\smallskip{\centering " + tsimple(X7b, Y7b) + r"\par}\smallskip " + T("Calcula el coeficient de correlació. Podem afirmar que jugar a videojocs fa baixar la nota?", "Calcula el coeficiente de correlación. ¿Podemos afirmar que jugar a videojuegos hace bajar la nota?"),
     calc(B7b) + ' ' + rr(B7b) + T(r" \ Però una correlació, encara que siga forta, \rest{no demostra que hi haja una relació de causa i efecte}: hi pot haver altres variables (el temps d'estudi, per exemple).", r" \ Pero una correlación, aunque sea fuerte, \rest{no demuestra que haya una relación de causa y efecto}: puede haber otras variables (el tiempo de estudio, por ejemplo).")),
 (2, T(r"Una gelateria anota la temperatura màxima ($X$, en °C) i els gelats venuts ($Y$) durant sis dies:", r"Una heladería anota la temperatura máxima ($X$, en °C) y los helados vendidos ($Y$) durante seis días:") + r"\par\smallskip{\centering " + tsimple(X7d, Y7d) + r"\par}\smallskip " + T("Calcula el coeficient de correlació i interpreta'l.", "Calcula el coeficiente de correlación e interprétalo."),
     calc(B7d) + ' ' + rr(B7d)),
 (2, T(r"Calcula el coeficient de correlació entre les notes de Matemàtiques i de Física de l'exercici 2.", r"Calcula el coeficiente de correlación entre las notas de Matemáticas y de Física del ejercicio 2."),
     r'$\sigma_x^2%s%s$, \ $\sigma_y^2%s%s$, \ $\sigma_{xy}%s%s$. \ $r%s\res{%s}$: %s \rest{%s}.' % (ap(B4['vx'], 3), d(B4['vx'], 3), ap(B4['vy'], 3), d(B4['vy'], 3), ap(B4['c'], 3), d(B4['c'], 3), ap(B4['r'], 3), d(B4['r'], 3), CORR, desc(B4['r']))),
 (1, T(r"Si el coeficient de correlació entre dues variables és $r=0{,}8$ i les desviacions típiques són $\sigma_x=2$ i $\sigma_y=5$, quant val la covariància?", r"Si el coeficiente de correlación entre dos variables es $r=0{,}8$ y las desviaciones típicas son $\sigma_x=2$ y $\sigma_y=5$, ¿cuánto vale la covarianza?"),
     r"$\sigma_{xy}=r\,\sigma_x\,\sigma_y=0{,}8\cdot2\cdot5=\res{8}$."),
 (1, T(r"Si $\sigma_{xy}=-12$, $\sigma_x=4$ i $\sigma_y=5$, quant val $r$? I si $\sigma_{xy}=3$, $\sigma_x=2$ i $\sigma_y=1$? És possible?", r"Si $\sigma_{xy}=-12$, $\sigma_x=4$ y $\sigma_y=5$, ¿cuánto vale $r$? ¿Y si $\sigma_{xy}=3$, $\sigma_x=2$ y $\sigma_y=1$? ¿Es posible?"),
     T(r"$r=\frac{-12}{4\cdot5}=\res{-0{,}6}$ (negativa moderada). \ En el segon cas eixiria $r=\frac{3}{2}=1{,}5>1$: \rest{no és possible}, hi ha un error en les dades.", r"$r=\frac{-12}{4\cdot5}=\res{-0{,}6}$ (negativa moderada). \ En el segundo caso saldría $r=\frac{3}{2}=1{,}5>1$: \rest{no es posible}, hay un error en los datos.")),
 (3, T(r"Una variable bidimensional té $N=10$, $\sum x_i=50$, $\sum y_i=80$, $\sum x_i^2=290$, $\sum y_i^2=730$ i $\sum x_iy_i=440$. Calcula $r$.", r"Una variable bidimensional tiene $N=10$, $\sum x_i=50$, $\sum y_i=80$, $\sum x_i^2=290$, $\sum y_i^2=730$ y $\sum x_iy_i=440$. Calcula $r$."),
     calc(B7c) + ' ' + rr(B7c)),
 (2, T(r"Observa aquests núvols de punts. Descriu la relació que hi ha entre les variables i digues si el coeficient de correlació lineal serà pròxim a 0 o no.", r"Observa estas nubes de puntos. Describe la relación que hay entre las variables y di si el coeficiente de correlación lineal será próximo a 0 o no.") + tasks(3, [r'\par' + nv(p) for p in NL]),
     tasks(1, [T(r'Relació \rest{parabòlica} (creix i després decreix): és forta, però no és lineal i $r\approx%s$, \rest{pròxim a 0}.', r'Relación \rest{parabólica} (crece y luego decrece): es fuerte pero no lineal, y $r\approx%s$, \rest{próximo a 0}.') % d(rNL[0]),
               T(r'Relació \rest{exponencial}: creixent, $r\approx%s$ és alt, però els punts no segueixen una recta.', r'Relación \rest{exponencial}: creciente, $r\approx%s$ es alto, pero los puntos no siguen una recta.') % d(rNL[1]),
               T(r'Els punts de baix no tenen cap relació, però el \rest{valor atípic} $(9,9)$ fa que $r\approx%s$. Cal revisar-lo abans de traure conclusions.', r'Los puntos de abajo no tienen ninguna relación, pero el \rest{valor atípico} $(9,9)$ hace que $r\approx%s$. Hay que revisarlo antes de sacar conclusiones.') % d(rNL[2])])),
 (1, T(r"Raona si són vertaderes o falses: \ a) Si $r=0$, les variables no tenen cap relació. \ b) Si $r=-0{,}98$, la relació és molt feble perquè $r$ és negatiu. \ c) Si tots els punts són sobre una recta creixent, $r=1$.", r"Razona si son verdaderas o falsas: \ a) Si $r=0$, las variables no tienen ninguna relación. \ b) Si $r=-0{,}98$, la relación es muy débil porque $r$ es negativo. \ c) Si todos los puntos están sobre una recta creciente, $r=1$."),
     T(r"a) \rest{Falsa}: només vol dir que no hi ha relació lineal (pot ser parabòlica, per exemple). \ b) \rest{Falsa}: és molt forta; el signe indica que és inversa. \ c) \rest{Vertadera}.", r"a) \rest{Falsa}: solo quiere decir que no hay relación lineal (puede ser parabólica, por ejemplo). \ b) \rest{Falsa}: es muy fuerte; el signo indica que es inversa. \ c) \rest{Verdadera}.")),
]))

# =====================================================================
# 6. Rectes de regressió
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
m7, n7 = reg(B7); m7i, n7i = reg(B7, True); m7d, n7d = reg(B7d); m7c, n7c = reg(B7c)
mD, nD = reg(BD)
# publicitat i vendes
XP = [1, 2, 3, 4, 5, 6, 7, 8]; YP = [12, 15, 15, 19, 22, 22, 26, 27]; BP = bi(XP, YP)
mP, nP = reg(BP); mPi, nPi = reg(BP, True)
# comprovació: cada recta passa per (x̄, ȳ) i fa mínima la suma de quadrats (derivades nul·les), i m_yx·m_xy = r²
for B, xs, ys in [(B6, X6, Y6), (B7, X7, Y7), (B7d, X7d, Y7d), (BP, XP, YP)]:
    (m, n), (mi, ni) = reg(B), reg(B, True)
    assert m * B['mx'] + n == B['my'] and mi * B['my'] + ni == B['mx']
    assert sum((Fr(y) - m * x - n) for x, y in zip(xs, ys)) == 0 and sum((Fr(y) - m * x - n) * x for x, y in zip(xs, ys)) == 0
    assert sum((Fr(x) - mi * y - ni) for x, y in zip(xs, ys)) == 0 and sum((Fr(x) - mi * y - ni) * y for x, y in zip(xs, ys)) == 0
    assert abs(float(m * mi) - B['r'] ** 2) < 1e-12
    NCHK[0] += 1
# dues rectes donades: y = 0,5x + 2 (Y/X) i x = 1,2y − 1 (X/Y)
cx = Fr(14, 10) / Fr(4, 10); cy = Fr(1, 2) * cx + 2
assert cx == Fr(6, 5) * cy - 1; r2 = math.sqrt(0.5 * 1.2); NCHK[0] += 1
# rectes sense dir quina és quina: 4x − 5y = 0 i 2x − y = 6
A1, A2 = (4, -5, 0), (2, -1, 6)
det = A1[0] * A2[1] - A1[1] * A2[0]; gx = Fr(A1[2] * A2[1] - A1[1] * A2[2], det); gy = Fr(A1[0] * A2[2] - A1[2] * A2[0], det)
myxQ = Fr(-A1[0], A1[1]); mxyQ = Fr(-A2[1], A2[0]); rQ = math.sqrt(myxQ * mxyQ)
assert (gx, gy) == (5, 4) and myxQ == Fr(4, 5) and mxyQ == Fr(1, 2) and Fr(-A2[0], A2[1]) * Fr(-A1[1], A1[0]) == Fr(5, 2)
assert myxQ * 6 == Fr(24, 5) and mxyQ * 5 + 3 == Fr(11, 2); NCHK[0] += 1
# a partir de r i de les desviacions típiques
cR = Fr(-3, 4) * 2 * 4; mR, nR = cR / 4, 15 - cR / 4 * 8; mRi, nRi = cR / 16, 8 - cR / 16 * 15
assert cR == -6 and (mR, nR) == (Fr(-3, 2), 27) and (mRi, nRi) == (Fr(-3, 8), Fr(109, 8)) and mR * mRi == Fr(9, 16); NCHK[0] += 1
YX, XY = T('Y sobre X', 'Y sobre X'), T('X sobre Y', 'X sobre Y')
S_.append((T("Rectes de regressió", "Rectas de regresión"), [
 (2, T(r"Amb les dades del primer exercici de la secció 4, troba la recta de regressió de $Y$ sobre $X$ i la de $X$ sobre $Y$. Estima el valor de $y$ per a $x=7$ i el de $x$ per a $y=6$.", r"Con los datos del primer ejercicio de la sección 4, halla la recta de regresión de $Y$ sobre $X$ y la de $X$ sobre $Y$. Estima el valor de $y$ para $x=7$ y el de $x$ para $y=6$.")
     + recorda(T(r"Recta de regressió de $Y$ sobre $X$: \ $y-\bar y=\dfrac{\sigma_{xy}}{\sigma_x^2}(x-\bar x)$ (per a estimar $y$). \ De $X$ sobre $Y$: \ $x-\bar x=\dfrac{\sigma_{xy}}{\sigma_y^2}(y-\bar y)$ (per a estimar $x$). Les estimacions són fiables si $|r|$ és prop d'1 i no ens n'eixim de l'interval de les dades.", r"Recta de regresión de $Y$ sobre $X$: \ $y-\bar y=\dfrac{\sigma_{xy}}{\sigma_x^2}(x-\bar x)$ (para estimar $y$). \ De $X$ sobre $Y$: \ $x-\bar x=\dfrac{\sigma_{xy}}{\sigma_y^2}(y-\bar y)$ (para estimar $x$). Las estimaciones son fiables si $|r|$ está cerca de 1 y no nos salimos del intervalo de los datos.")),
     (r'$Y$ %s $X$: $y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$; \ $\hat y(7)%s\res{%s}$. \ $X$ %s $Y$: $x-%s=\frac{%s}{%s}(y-%s)\Rightarrow\res{%s}$; \ $\hat x(6)%s\res{%s}$. \ ' % (
         'sobre', d(B6['my'], 3), d(B6['c'], 3), d(B6['vx'], 3), d(B6['mx'], 3), eqr(m6, n6), ap(est(m6, n6, 7), 3), d(est(m6, n6, 7), 3),
         'sobre', d(B6['mx'], 3), d(B6['c'], 3), d(B6['vy'], 3), d(B6['my'], 3), eqr(m6i, n6i, 'x', 'y'), ap(est(m6i, n6i, 6), 3), d(est(m6i, n6i, 6), 3)))
     + T(r'Són fiables: $r%s%s$ i els valors són dins de les dades.', r'Son fiables: $r%s%s$ y los valores están dentro de los datos.') % (ap(B6['r'], 3), d(B6['r'], 3))),
 (2, T(r"Una empresa ha anotat durant 8 mesos la inversió en publicitat ($X$, en milers d'euros) i les vendes ($Y$, en milers d'euros):", r"Una empresa ha anotado durante 8 meses la inversión en publicidad ($X$, en miles de euros) y las ventas ($Y$, en miles de euros):") + r"\par\smallskip{\centering " + tsimple(XP, YP) + r"\par}\smallskip"
     + tasks(1, [T("Calcula el coeficient de correlació i interpreta'l.", "Calcula el coeficiente de correlación e interprétalo."),
                 T("Troba la recta de regressió de $Y$ sobre $X$. Què significa el seu pendent?", "Halla la recta de regresión de $Y$ sobre $X$. ¿Qué significa su pendiente?"),
                 T("Quines vendes s'esperen si s'inverteixen 5500 € en publicitat?", "¿Qué ventas se esperan si se invierten 5500 € en publicidad?"),
                 T("Quant cal invertir en publicitat per a vendre 24\\,000 €? (Fes servir la recta adequada.)", "¿Cuánto hay que invertir en publicidad para vender 24\\,000 €? (Usa la recta adecuada.)")]),
     tasks(1, [calc(BP) + ' ' + rr(BP),
               T(r'$y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$. Per cada 1000 € més de publicitat, les vendes augmenten, de mitjana, uns $\res{%s}$ €.', r'$y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$. Por cada 1000 € más de publicidad, las ventas aumentan, de media, unos $\res{%s}$ €.') % (d(BP['my'], 3), d(BP['c'], 3), d(BP['vx'], 3), d(BP['mx'], 3), eqr(mP, nP), d(1000 * mP, 0)),
               T(r'$\hat y(5{,}5)%s%s$: unes vendes de $\res{%s}$ €.', r'$\hat y(5{,}5)%s%s$: unas ventas de $\res{%s}$ €.') % (ap(est(mP, nP, Fr(11, 2)), 3), d(est(mP, nP, Fr(11, 2)), 3), d(1000 * est(mP, nP, Fr(11, 2)), 0)),
               T(r'Recta de $X$ sobre $Y$: $x-%s=\frac{%s}{%s}(y-%s)\Rightarrow\res{%s}$; \ $\hat x(24)%s%s$: cal invertir uns $\res{%s}$ €. Fiable: $r%s%s$.', r'Recta de $X$ sobre $Y$: $x-%s=\frac{%s}{%s}(y-%s)\Rightarrow\res{%s}$; \ $\hat x(24)%s%s$: hay que invertir unos $\res{%s}$ €. Fiable: $r%s%s$.') % (d(BP['mx'], 3), d(BP['c'], 3), d(BP['vy'], 3), d(BP['my'], 3), eqr(mPi, nPi, 'x', 'y'), ap(est(mPi, nPi, 24), 3), d(est(mPi, nPi, 24), 3), d(1000 * est(mPi, nPi, 24), 0), ap(BP['r'], 3), d(BP['r'], 3))])),
 (2, T(r"Amb les altures i els pesos de la secció 5, troba la recta de regressió del pes sobre l'altura i la de l'altura sobre el pes. Quin pes s'estima per a una persona de 168 cm? I per a un xiquet de 120 cm? Quina altura s'estima per a una persona de 65 kg?", r"Con las alturas y los pesos de la sección 5, halla la recta de regresión del peso sobre la altura y la de la altura sobre el peso. ¿Qué peso se estima para una persona de 168 cm? ¿Y para un niño de 120 cm? ¿Qué altura se estima para una persona de 65 kg?"),
     T(r"$y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$. \ $\hat y(168)%s\res{%s\text{ kg}}$: \rest{fiable} ($r%s%s$ i 168 és dins de les dades). \ $\hat y(120)%s%s$ kg: \rest{no és fiable}, 120 cm queda molt lluny de l'interval $[150,180]$. \ Altura sobre pes: $\res{%s}$; \ $\hat x(65)%s\res{%s\text{ cm}}$.",
       r'$y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$. \ $\hat y(168)%s\res{%s\text{ kg}}$: \rest{fiable} ($r%s%s$ y 168 está dentro de los datos). \ $\hat y(120)%s%s$ kg: \rest{no es fiable}, 120 cm queda muy lejos del intervalo $[150,180]$. \ Altura sobre peso: $\res{%s}$; \ $\hat x(65)%s\res{%s\text{ cm}}$.') % (
         d(B7['my'], 3), d(B7['c'], 3), d(B7['vx'], 3), d(B7['mx'], 3), eqr(m7, n7), ap(est(m7, n7, 168), 2), d(est(m7, n7, 168), 2), ap(B7['r'], 3), d(B7['r'], 3), ap(est(m7, n7, 120), 2), d(est(m7, n7, 120), 2),
         eqr(m7i, n7i, 'x', 'y'), ap(est(m7i, n7i, 65), 1), d(est(m7i, n7i, 65), 1))),
 (2, T(r"Amb les dades de la gelateria de la secció 5, quants gelats s'estima que es vendran un dia amb una màxima de 25 °C?", r"Con los datos de la heladería de la sección 5, ¿cuántos helados se estima que se venderán un día con una máxima de 25 °C?"),
     T(r'Recta: $\res{%s}$. \ $\hat y(25)%s%s$: uns $\res{%d}$ gelats. Molt fiable: $r%s%s$.', r'Recta: $\res{%s}$. \ $\hat y(25)%s%s$: unos $\res{%d}$ helados. Muy fiable: $r%s%s$.') % (eqr(m7d, n7d), ap(est(m7d, n7d, 25), 2), d(est(m7d, n7d, 25), 2), round(est(m7d, n7d, 25)), ap(B7d['r'], 3), d(B7d['r'], 3))),
 (2, T(r"Amb la taula de fills i cotxes de l'exercici 1, troba la recta de regressió de $Y$ sobre $X$ i estima el nombre de cotxes d'una família amb 2 fills. És fiable?", r"Con la tabla de hijos y coches del ejercicio 1, halla la recta de regresión de $Y$ sobre $X$ y estima el número de coches de una familia con 2 hijos. ¿Es fiable?"),
     T(r'$y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$; \ $\hat y(2)%s\res{%s}$ cotxes. Poc fiable: $r%s%s$ només indica una correlació moderada.', r'$y-%s=\frac{%s}{%s}(x-%s)\Rightarrow\res{%s}$; \ $\hat y(2)%s\res{%s}$ coches. Poco fiable: $r%s%s$ solo indica una correlación moderada.') % (d(BD['my'], 3), d(BD['c'], 3), d(BD['vx'], 3), d(BD['mx'], 3), eqr(mD, nD), ap(est(mD, nD, 2), 3), d(est(mD, nD, 2), 3), ap(BD['r'], 3), d(BD['r'], 3))),
 (2, T(r"Amb les sumes de l'exercici de la secció 5 ($N=10$, $\sum x_i=50$, $\sum y_i=80$, $\sum x_i^2=290$, $\sum x_iy_i=440$), troba la recta de regressió de $Y$ sobre $X$ i estima $y$ per a $x=6$.", r"Con las sumas del ejercicio de la sección 5 ($N=10$, $\sum x_i=50$, $\sum y_i=80$, $\sum x_i^2=290$, $\sum x_iy_i=440$), halla la recta de regresión de $Y$ sobre $X$ y estima $y$ para $x=6$."),
     T(r'$\bar x=5$, $\bar y=8$, $\sigma_x^2=4$, $\sigma_{xy}=4$: \ $y-8=\frac44(x-5)\Rightarrow\res{%s}$; \ $\hat y(6)=\res{%s}$ (poc precisa: $r%s%s$ és moderat).', r'$\bar x=5$, $\bar y=8$, $\sigma_x^2=4$, $\sigma_{xy}=4$: \ $y-8=\frac44(x-5)\Rightarrow\res{%s}$; \ $\hat y(6)=\res{%s}$ (poco precisa: $r%s%s$ es moderado).') % (eqr(m7c, n7c), d(est(m7c, n7c, 6)), ap(B7c['r'], 3), d(B7c['r'], 3))),
 (2, T(r"D'una distribució bidimensional sabem que $\bar x=8$, $\bar y=15$, $\sigma_x=2$, $\sigma_y=4$ i $r=-0{,}75$. Troba les dues rectes de regressió i estima $y$ per a $x=9$ i $x$ per a $y=12$.", r"De una distribución bidimensional sabemos que $\bar x=8$, $\bar y=15$, $\sigma_x=2$, $\sigma_y=4$ y $r=-0{,}75$. Halla las dos rectas de regresión y estima $y$ para $x=9$ y $x$ para $y=12$."),
     r'$\sigma_{xy}=r\,\sigma_x\sigma_y=-0{,}75\cdot2\cdot4=-6$. \ ' + YX + r': $y-15=\frac{-6}{4}(x-8)\Rightarrow\res{%s}$; \ $\hat y(9)=\res{%s}$. \ ' % (eqr(mR, nR), d(est(mR, nR, 9))) + XY + r': $x-8=\frac{-6}{16}(y-15)\Rightarrow\res{%s}$; \ $\hat x(12)%s\res{%s}$.' % (eqr(mRi, nRi, 'x', 'y'), ap(est(mRi, nRi, 12), 3), d(est(mRi, nRi, 12), 3))),
 (3, T(r"Les rectes de regressió d'una variable bidimensional són $y=0{,}5x+2$ (de $Y$ sobre $X$) i $x=1{,}2y-1$ (de $X$ sobre $Y$). Calcula $\bar x$, $\bar y$ i el coeficient de correlació.", r"Las rectas de regresión de una variable bidimensional son $y=0{,}5x+2$ (de $Y$ sobre $X$) y $x=1{,}2y-1$ (de $X$ sobre $Y$). Calcula $\bar x$, $\bar y$ y el coeficiente de correlación.")
     + recorda(T(r"Les dues rectes passen per $(\bar x,\bar y)$ i el producte dels coeficients de regressió és $m_{yx}\cdot m_{xy}=\frac{\sigma_{xy}}{\sigma_x^2}\cdot\frac{\sigma_{xy}}{\sigma_y^2}=r^2$.", r"Las dos rectas pasan por $(\bar x,\bar y)$ y el producto de los coeficientes de regresión es $m_{yx}\cdot m_{xy}=\frac{\sigma_{xy}}{\sigma_x^2}\cdot\frac{\sigma_{xy}}{\sigma_y^2}=r^2$.")),
     T(r'Substituint: $x=1{,}2(0{,}5x+2)-1=0{,}6x+1{,}4\Rightarrow\bar x=\res{%s}$, \ $\bar y=\res{%s}$. \ $r^2=0{,}5\cdot1{,}2=0{,}6$ i, com que els coeficients són positius, $r=\sqrt{0{,}6}%s\res{%s}$.', r'Sustituyendo: $x=1{,}2(0{,}5x+2)-1=0{,}6x+1{,}4\Rightarrow\bar x=\res{%s}$, \ $\bar y=\res{%s}$. \ $r^2=0{,}5\cdot1{,}2=0{,}6$ y, como los coeficientes son positivos, $r=\sqrt{0{,}6}%s\res{%s}$.') % (d(cx), d(cy), ap(r2, 3), d(r2, 3))),
 (3, T(r"Les rectes de regressió d'una distribució són $4x-5y=0$ i $2x-y=6$. Troba el centre de gravetat, esbrina quina recta és la de $Y$ sobre $X$ i calcula $r$. Estima $y$ per a $x=6$ i $x$ per a $y=5$.", r"Las rectas de regresión de una distribución son $4x-5y=0$ y $2x-y=6$. Halla el centro de gravedad, averigua qué recta es la de $Y$ sobre $X$ y calcula $r$. Estima $y$ para $x=6$ y $x$ para $y=5$."),
     T(r"Resolent el sistema: $(\bar x,\bar y)=\res{(%s;\ %s)}$. \ En la forma $y=ax+b$: $y=0{,}8x$ i $y=2x-6$. La més plana, $\res{y=0{,}8x}$, és la de $Y$ sobre $X$ ($m_{yx}=0{,}8$); l'altra, $\res{x=0{,}5y+3}$, és la de $X$ sobre $Y$ ($m_{xy}=0{,}5$). (A l'inrevés eixiria $r^2=2\cdot1{,}25=2{,}5>1$.) \ $r^2=0{,}8\cdot0{,}5=0{,}4\Rightarrow r=\sqrt{0{,}4}%s\res{%s}$. \ $\hat y(6)=\res{4{,}8}$, \ $\hat x(5)=\res{5{,}5}$.",
       r'Resolviendo el sistema: $(\bar x,\bar y)=\res{(%s;\ %s)}$. \ En la forma $y=ax+b$: $y=0{,}8x$ e $y=2x-6$. La más plana, $\res{y=0{,}8x}$, es la de $Y$ sobre $X$ ($m_{yx}=0{,}8$); la otra, $\res{x=0{,}5y+3}$, es la de $X$ sobre $Y$ ($m_{xy}=0{,}5$). (Al revés saldría $r^2=2\cdot1{,}25=2{,}5>1$.) \ $r^2=0{,}8\cdot0{,}5=0{,}4\Rightarrow r=\sqrt{0{,}4}%s\res{%s}$. \ $\hat y(6)=\res{4{,}8}$, \ $\hat x(5)=\res{5{,}5}$.') % (d(gx), d(gy), ap(rQ, 3), d(rQ, 3))),
 (2, T(r"Raona si poden ser les rectes de regressió d'una distribució: \ a) $y=2x+1$ i $y=-x+4$; \ b) $y=-0{,}4x+6$ (de $Y$ sobre $X$) i $x=-0{,}9y+10$ (de $X$ sobre $Y$).", r"Razona si pueden ser las rectas de regresión de una distribución: \ a) $y=2x+1$ e $y=-x+4$; \ b) $y=-0{,}4x+6$ (de $Y$ sobre $X$) y $x=-0{,}9y+10$ (de $X$ sobre $Y$)."),
     T(r"a) \rest{No}: els dos coeficients de regressió han de tindre el mateix signe (el de $\sigma_{xy}$), i ací un és positiu i l'altre negatiu. \ b) \rest{Sí}: tots dos són negatius i $r^2=(-0{,}4)(-0{,}9)=0{,}36\leq1$, \ $r=\res{-0{,}6}$.", r"a) \rest{No}: los dos coeficientes de regresión deben tener el mismo signo (el de $\sigma_{xy}$), y aquí uno es positivo y el otro negativo. \ b) \rest{Sí}: los dos son negativos y $r^2=(-0{,}4)(-0{,}9)=0{,}36\leq1$, \ $r=\res{-0{,}6}$.")),
]))
assert B7c['c'] == 4 and B7c['vx'] == 4 and Fr(-4, 10) * Fr(-9, 10) == Fr(36, 100); NCHK[0] += 1

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("pdfkeywords={distribucions bidimensionals, taula de doble entrada, núvol de punts, correlació, regressió, covariància, coeficient de correlació lineal, rectes de regressió}",
       "pdfkeywords={distribuciones bidimensionales, tabla de doble entrada, nube de puntos, correlación, regresión, covarianza, coeficiente de correlación lineal, rectas de regresión}")
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les CCSS I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
pre += (r'\providecommand{\gt}{>}\providecommand{\lt}{<}' + '\n% quadre de recordatori (només a la fitxa d\'exercicis)\n'
        r'\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{'
        + T('Recorda', 'Recuerda') + r':}\ #1\end{tcolorbox}}' + '\n')

def fix(t):
    """Fora dels dibuixos: l'espai després de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = T("Distribucions bidimensionals", "Distribuciones bidimensionales")
def build(sol):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 8: %s' % (t, TIT), capcalera='%s · Unidad 8: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-ccss')
        cap = assignatura('1batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 8' if sol else 'Ficha de ejercicios · Unidad 8') + '}'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                        "pdftitle={%s de la unitat 8: %s. 1r de Batxillerat CCSS}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 8: %s · 1r Batxillerat CCSS" % (t, TIT))
        assert 'Unitat 8' in p and 'unitat 8' in p
        cap = r'\capcalera{Matemàtiques CCSS}{1r Batx}{' + ('Solucions de la fitxa · Unitat 8' if sol else "Fitxa d'exercicis · Unitat 8") + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{11}% que el títol d\'una secció no quede sol al final del full\n\\input{../comu/fentmates.tex}\n\\fmcurs{1batx-ccss}\n\n'
               '\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '{\\raggedright ' + TIT + '}\n')
    if not sol:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb les calculadores dels apunts interactius de la unitat.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con las calculadoras de los apuntes interactivos de la unidad.")
             if sol else T(r"Resol els exercicis al quadern mostrant tots els passos: per a les variables bidimensionals, fes sempre la taula amb les columnes $x_i$, $y_i$, $x_i^2$, $y_i^2$ i $x_iy_i$. Arredoneix els resultats a dues o tres xifres decimals. Pots comprovar-los amb les calculadores dels apunts interactius.",
                           r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos: para las variables bidimensionales, haz siempre la tabla con las columnas $x_i$, $y_i$, $x_i^2$, $y_i^2$ y $x_iy_i$. Redondea los resultados a dos o tres cifras decimales. Puedes comprobarlos con las calculadoras de los apuntes interactivos."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb la calculadora bidimensional dels apunts interactius.", "¡Ánimo! Comprueba tus resultados con la calculadora bidimensional de los apuntes interactivos.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = ('t8-fitxa-solucions' if sol else 't8-fitxa-exercicis') + ('-es' if ES else '') + '.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis;', NCHK[0], 'comprovacions')
