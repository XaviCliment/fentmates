# Versió en castellà de genera.py: escriu els -es.tex. Original: genera t5-fitxa-exercicis.tex i t5-fitxa-solucions.tex (1r Batxillerat MI, Unitat 5: Trigonometria)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# La unitat ajunta les dues fitxes del departament: els exercicis 1-41 són els de «Trigonometria 1» i els 42-60, els de
# «Trigonometria 2», en el mateix ordre; la secció 13 n'afegeix 13 de nous (61-73).
# Els valors numèrics de les solucions es calculen ací (math); les solucions exactes s'escriuen a mà i CHK les compara amb el
# valor numèric. Les equacions i els sistemes es comproven buscant totes les arrels en [0°, 360°) (no en falta ni en sobra cap).
# Ús: python3 genera.py && pdflatex t5-fitxa-exercicis.tex (dues vegades) && pdflatex t5-fitxa-solucions.tex (dues vegades)
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
PI = math.pi
def r(d): return math.radians(d)
def sin(d): return math.sin(r(d))
def cos(d): return math.cos(r(d))
def tan(d): return math.tan(r(d))
def asin(x): return math.degrees(math.asin(x))
def acos(x): return math.degrees(math.acos(x))
def atan(x): return math.degrees(math.atan(x))
def DMS(d, m=0, s=0): return d + m / 60 + s / 3600
S2, S3, S5, S6 = math.sqrt(2), math.sqrt(3), math.sqrt(5), math.sqrt(6)

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def dec(x, k=2, strip=True):
    s = '%.*f' % (k, x)
    if strip and '.' in s: s = s.rstrip('0').rstrip('.')
    if s in ('-0', '-0.0'): s = '0'
    return s.replace('.', '{,}')
def dms(x, sec=True):
    sg = '-' if x < 0 else ''; x = abs(x)
    t = round(x * 3600) if sec else round(x * 60) * 60
    d, m, q = t // 3600, (t % 3600) // 60, t % 60
    return sg + '%d^\\circ' % d + ("%d'" % m if m or q else '') + ("%d''" % q if q else '')
def degs(l): return r',\ '.join(dms(x) for x in l)
def degsR(l): return ', '.join(r'$\res{%s}$' % dms(x) for x in sorted(l))
def sist(*rows): return r'\left\{\begin{array}{l}' + r'\\'.join(rows) + r'\end{array}\right.'

CHK = []
def ck(a, b, tol=1e-9, msg=''):
    ok = abs(a - b) <= tol * max(1, abs(b))
    CHK.append(ok); assert ok, (msg, a, b)

# ---------- arrels d'equacions en [0, 360) ----------
def roots(f, a=0, b=360, step=0.02):
    """totes les arrels de f (graus) en [a, b): mínims locals de |f| que valen ~0"""
    n = int(round((b - a) / step)); xs = [a + i * step for i in range(n + 1)]
    def g(x):
        try: v = f(x)
        except (ZeroDivisionError, ValueError): return float('inf')
        return abs(v) if v == v else float('inf')
    gs = [g(x) for x in xs]; out = []
    for i in range(n + 1):
        l = gs[i - 1] if i else gs[1]; rr = gs[i + 1] if i < n else gs[n - 1]
        if gs[i] <= l and gs[i] <= rr and gs[i] < 0.05:
            lo, hi = xs[max(0, i - 1)], xs[min(n, i + 1)]
            for _ in range(80):
                m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
                if g(m1) < g(m2): hi = m2
                else: lo = m1
            x = (lo + hi) / 2
            if g(x) < 1e-7 and x < b - 1e-6 and not any(abs(x - y) < 1e-3 for y in out): out.append(x)
    return sorted(round(x, 6) % 360 for x in out)
def ckeq(f, sol, msg=''):
    got = roots(f)
    sol = sorted(x % 360 for x in sol)
    assert len(got) == len(sol) and all(abs(p - q) < 1e-3 for p, q in zip(got, sol)), (msg, got, sol)
    CHK.append(True)
def cksys(eqs, sol, msg='', step=1):
    got = [(x, y) for x in range(0, 360, step) for y in range(0, 360, step) if all(abs(e(x, y)) < 1e-9 for e in eqs)]
    assert sorted(got) == sorted(sol), (msg, got, sol)
    CHK.append(True)

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Mesura d'angles
def pifr(num, den):
    g = math.gcd(num, den); num //= g; den //= g
    top = ('' if abs(num) == 1 else str(abs(num))) + r'\pi'
    return ('-' if num < 0 else '') + (top if den == 1 else r'\frac{%s}{%d}' % (top, den))
e1 = [r'$225^\circ$', r'$75^\circ$', r'$160^\circ$', r'$-1{,}5$ rad', r'$2$ rad', r'$540^\circ$', r'$-270^\circ$', r"$140^\circ40'$", r'$\frac{\pi}{3}$ rad', r'$0{,}3$ rad', r'$-\frac{6\pi}{5}$ rad', r'$315^\circ$']
s1 = [R(pifr(225, 180)), R(pifr(75, 180)), R(pifr(160, 180)), R(dms(math.degrees(-1.5))), R(dms(math.degrees(2))), R(pifr(540, 180)), R(pifr(-270, 180)),
      R(pifr(8440, 10800)) + r'$\approx%s$' % dec(r(DMS(140, 40)), 4), R('60^\\circ'), R(dms(math.degrees(0.3))), R('-216^\\circ'), R(pifr(315, 180))]
ck(r(DMS(140, 40)), 211 * PI / 270)
S.append(("Medida de ángulos", [
 (1, r"Transforma estos ángulos en grados o radianes, según corresponda." + tasks(4, e1), tasks(4, s1)),
]))

# =====================================================================
# 2. Trigonometria amb la calculadora
c2 = [(r"\sin(319^\circ12'52'')", sin(DMS(319, 12, 52))), (r"\cos(434^\circ26')", cos(DMS(434, 26))), (r'\text{tg}\,\frac{11\pi}{8}', math.tan(11 * PI / 8)),
      (r'\sec135^\circ', 1 / cos(135)), (r'\text{tg}\,7{,}03', math.tan(7.03)), (r'\text{cosec}\,5{,}24', 1 / math.sin(5.24)), (r'\sin\frac{8\pi}{5}', math.sin(8 * PI / 5)),
      (r"\text{cosec}\,(55'45'')", 1 / sin(DMS(0, 55, 45))), (r'\cos\frac{\pi}{3}', 0.5), (r"\text{cosec}\,(200^\circ16')", 1 / sin(DMS(200, 16))), (r'\sec\frac{5\pi}{4}', 1 / math.cos(5 * PI / 4)),
      (r"\text{tg}\,(183^\circ13'53'')", tan(DMS(183, 13, 53))), (r"\sin(333^\circ0'55'')", sin(DMS(333, 0, 55))), (r'\cos3{,}845', math.cos(3.845)), (r'\text{cotg}\,\frac{11\pi}{6}', 1 / math.tan(11 * PI / 6))]
a3 = [('\\cos x=0{,}4539', 'cos', 0.4539), ('\\sin x=0{,}9284', 'sin', 0.9284), ('\\text{tg}\\,x=-0{,}5459', 'tan', -0.5459), ('\\cos x=-0{,}3996', 'cos', -0.3996),
      ('\\text{cotg}\\,x=2{,}1618', 'cot', 2.1618), ('\\cos x=-0{,}2926', 'cos', -0.2926), ('\\sin x=0{,}6862', 'sin', 0.6862), ('\\sin x=-0{,}3308', 'sin', -0.3308)]
def two(kind, v):
    if kind == 'sin': a = asin(v); return sorted([a % 360, (180 - a) % 360])
    if kind == 'cos': a = acos(v); return sorted([a, 360 - a])
    if kind == 'tan': a = atan(v); return sorted([a % 360, (a + 180) % 360])
    a = atan(1 / v); return sorted([a % 360, (a + 180) % 360])
s3 = []
for t, kind, v in a3:
    xs = two(kind, v)
    fn = {'sin': sin, 'cos': cos, 'tan': tan, 'cot': lambda d: 1 / tan(d)}[kind]
    for x in xs: ck(fn(x), v, 1e-9, t)
    s3.append(r'$%s$: $\res{%s}$' % (t.split('=')[0], degs(xs)))
S.append(("Trigonometría con la calculadora", [
 (1, r"Con la calculadora, halla estas razones (con cuatro decimales). Comprueba antes si debe estar en modo \texttt{D} (grados) o \texttt{R} (radianes)." + tasks(3, ['$%s$' % t for t, _ in c2]),
     tasks(3, [r'$%s\approx\res{%s}$' % (t, dec(v, 4, False)) for t, v in c2])),
 (1, r"Halla los ángulos de $[0^\circ,360^\circ)$ que cumplen:" + tasks(4, ['$%s$' % t for t, _, _ in a3])
     + recorda(r"la calculadora da un solo ángulo. El otro: $180^\circ-\alpha$ (seno), $360^\circ-\alpha$ (coseno) o $\alpha+180^\circ$ (tangente)."),
     tasks(2, s3)),
]))

# =====================================================================
# 3. Raons d'un angle agut
tab4 = r'''\begin{center}\renewcommand{\arraystretch}{1.5}\begin{tabular}{|l|*{5}{C{1.55cm}|}}\hline
\textbf{Grados} & $0^\circ$ & $30^\circ$ & $45^\circ$ & $60^\circ$ & $90^\circ$\\\hline
\textbf{Radianes} & %s\\\hline
$\sin$ & %s\\\hline $\cos$ & %s\\\hline $\text{tg}$ & %s\\\hline $\text{cosec}$ & %s\\\hline $\sec$ & %s\\\hline $\text{cotg}$ & %s\\\hline
\end{tabular}\end{center}'''
blank = ' & '.join([''] * 5)
rows4 = [['$0$', r'$\frac{\pi}{6}$', r'$\frac{\pi}{4}$', r'$\frac{\pi}{3}$', r'$\frac{\pi}{2}$'],
         ['$0$', r'$\frac12$', r'$\frac{\sqrt2}{2}$', r'$\frac{\sqrt3}{2}$', '$1$'],
         ['$1$', r'$\frac{\sqrt3}{2}$', r'$\frac{\sqrt2}{2}$', r'$\frac12$', '$0$'],
         ['$0$', r'$\frac{\sqrt3}{3}$', '$1$', r'$\sqrt3$', r'$\nexists$'],
         [r'$\nexists$', '$2$', r'$\sqrt2$', r'$\frac{2\sqrt3}{3}$', '$1$'],
         ['$1$', r'$\frac{2\sqrt3}{3}$', r'$\sqrt2$', '$2$', r'$\nexists$'],
         [r'$\nexists$', r'$\sqrt3$', '$1$', r'$\frac{\sqrt3}{3}$', '$0$']]
num4 = [[0, PI / 6, PI / 4, PI / 3, PI / 2], [0, .5, S2 / 2, S3 / 2, 1], [1, S3 / 2, S2 / 2, .5, 0], [0, S3 / 3, 1, S3, None], [None, 2, S2, 2 * S3 / 3, 1], [1, 2 * S3 / 3, S2, 2, None], [None, S3, 1, S3 / 3, 0]]
for i, d in enumerate([0, 30, 45, 60, 90]):
    vals = [r(d), sin(d), cos(d), tan(d) if d != 90 else None, 1 / sin(d) if d else None, 1 / cos(d) if d != 90 else None, cos(d) / sin(d) if d else None]
    for j in range(7):
        if num4[j][i] is None: assert vals[j] is None
        else: ck(vals[j], num4[j][i], 1e-9, 'tab4')
s5 = [r'$\alpha$: $\sin\alpha=\res{\frac23}$, $\text{tg}\,\alpha=\res{\frac{2\sqrt5}{5}}$; $\sec\alpha=\frac{3\sqrt5}{5}$, $\text{cosec}\,\alpha=\frac32$, $\text{cotg}\,\alpha=\frac{\sqrt5}{2}$',
      r'$\beta$: $\cos\beta=\res{\frac45}$, $\text{tg}\,\beta=\res{\frac34}$; $\sec\beta=\frac54$, $\text{cosec}\,\beta=\frac53$, $\text{cotg}\,\beta=\frac43$',
      r'$\gamma$: $\cos\gamma=\res{\frac{\sqrt{10}}{10}}$, $\sin\gamma=\res{\frac{3\sqrt{10}}{10}}$; $\sec\gamma=\sqrt{10}$, $\text{cosec}\,\gamma=\frac{\sqrt{10}}{3}$, $\text{cotg}\,\gamma=\frac13$']
ck(math.sqrt(1 - 5 / 9), 2 / 3); ck((2 / 3) / (S5 / 3), 2 * S5 / 5); ck(1 / math.sqrt(10), math.sqrt(10) / 10)
def allr(sn, cs):
    return r'$\sin\approx\res{%s}$, $\cos\approx\res{%s}$, $\text{tg}\approx\res{%s}$' % (dec(sn, 4, False), dec(cs, 4, False), dec(sn / cs, 4, False))
sd = math.sqrt(1 - .86 ** 2); ce = 1 / math.sqrt(1 + 2.83 ** 2)
s5 += [r'$\alpha$: ' + allr(sd, .86), r'$\beta$: ' + allr(2.83 * ce, ce), r'$\gamma=45^\circ$: $\sin\gamma=\cos\gamma=\res{\frac{\sqrt2}{2}}$']
S.append(("Razones trigonométricas de un ángulo agudo", [
 (1, r"Completa la tabla siguiente sin calculadora:" + tab4 % ((blank,) * 7), tab4 % tuple(' & '.join(x) for x in rows4)),
 (1, r"Utiliza las relaciones fundamentales para hallar las otras razones trigonométricas de los ángulos agudos $\alpha$, $\beta$ y $\gamma$:"
     + tasks(3, [r'$\cos\alpha=\frac{\sqrt5}{3}$', r'$\sin\beta=\frac35$', r'$\text{tg}\,\gamma=3$', r'$\cos\alpha=0{,}86$', r'$\text{tg}\,\beta=2{,}83$', r'$\text{tg}\,\gamma=1$'])
     + recorda(r"$\sin^2\alpha+\cos^2\alpha=1$, \ $\text{tg}\,\alpha=\dfrac{\sin\alpha}{\cos\alpha}$, \ $1+\text{tg}^2\alpha=\dfrac{1}{\cos^2\alpha}$."),
     tasks(1, s5)),
]))

# =====================================================================
# 4. Raons d'angles qualssevol
ANG6 = [120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
EX = {0: ('0', '1', '0'), 30: (r'\frac12', r'\frac{\sqrt3}{2}', r'\frac{\sqrt3}{3}'), 45: (r'\frac{\sqrt2}{2}', r'\frac{\sqrt2}{2}', '1'),
      60: (r'\frac{\sqrt3}{2}', r'\frac12', r'\sqrt3'), 90: ('1', '0', r'\nexists')}
def exact(d):
    d %= 360
    q = 0 if d <= 90 else 1 if d <= 180 else 2 if d <= 270 else 3
    ref = [d, 180 - d, d - 180, 360 - d][q]
    s, c, t = EX[ref]
    neg = lambda x: x if x in ('0', r'\nexists') else '-' + x
    if q in (1,): c, t = neg(c), neg(t)
    if q == 2: s, c = neg(s), neg(c)
    if q == 3: s, t = neg(s), neg(t)
    if d in (90, 270): t = r'\nexists'
    return s, c, t
def num(sx):
    sx = sx.replace(r'\frac{\sqrt3}{2}', str(S3 / 2)).replace(r'\frac{\sqrt2}{2}', str(S2 / 2)).replace(r'\frac{\sqrt3}{3}', str(S3 / 3)).replace(r'\frac12', '0.5').replace(r'\sqrt3', str(S3))
    return float(sx.replace('--', ''))
for d in ANG6 + [0, 30, 45, 60, 90]:
    s, c, t = exact(d)
    ck(num(s), sin(d), 1e-9, d); ck(num(c), cos(d), 1e-9, d)
    if t != r'\nexists': ck(num(t), tan(d), 1e-9, d)
    else: assert abs(cos(d)) < 1e-12
def radT(d): return pifr(d, 180) if d else '0'
tab6 = r'\begin{center}\renewcommand{\arraystretch}{1.45}\begin{tabular}{|C{1.4cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|}\hline\textbf{Grados} & \textbf{Radianes} & $\sin$ & $\cos$ & $\text{tg}$\\\hline' + \
    '%s\\end{tabular}\\end{center}'
t6q = tab6 % ''.join(r'$%d^\circ$ & & & & \\\hline ' % d for d in ANG6)
t6s = tab6 % ''.join(r'$%d^\circ$ & $%s$ & $%s$ & $%s$ & $%s$\\\hline ' % ((d, radT(d)) + exact(d)) for d in ANG6)
e7 = [(r'\sin\pi-\text{tg}\,\pi+2\cos\pi', -2, math.sin(PI) - math.tan(PI) + 2 * math.cos(PI)), (r'\cos\frac{\pi}{2}-\sin\frac{3\pi}{2}', 1, math.cos(PI / 2) - math.sin(3 * PI / 2)),
      (r'\text{tg}\,2\pi-\sin\frac{\pi}{2}-2\cos\frac{3\pi}{2}', -1, math.tan(2 * PI) - 1 - 2 * math.cos(3 * PI / 2)), (r'\cos2\pi-\sin2\pi', 1, 1 - math.sin(2 * PI))]
for _, a, b in e7: ck(b, a, 1e-9)
# exercici 8
t8 = [('Segundo', 'sin', .6702), ('Tercero', 'cos', -.4539), ('Cuarto', 'tan', -.7459), ('Tercero', 'sin', -.7822), ('Segundo', 'tan', -1.9004), ('Cuarto', 'cos', .6983)]
QS = {'Segundo': (1, -1), 'Tercero': (-1, -1), 'Cuarto': (-1, 1)}
r8 = []
for qn, k, v in t8:
    ss, cs = QS[qn]
    if k == 'sin': sn = v; c = cs * math.sqrt(1 - v * v)
    elif k == 'cos': c = v; sn = ss * math.sqrt(1 - v * v)
    else: c = cs / math.sqrt(1 + v * v); sn = v * c
    ck(sn * sn + c * c, 1); assert (sn > 0) == (ss > 0) and (c > 0) == (cs > 0)
    cells = {'sin': dec(sn, 4, False), 'cos': dec(c, 4, False), 'tan': dec(sn / c, 4, False)}
    r8.append((qn, k, cells))
def tab8(sol):
    o = r'\begin{center}\renewcommand{\arraystretch}{1.3}\begin{tabular}{|l|C{2.4cm}|C{2.4cm}|C{2.4cm}|}\hline\textbf{Cuadrante} & $\sin$ & $\cos$ & $\text{tg}$\\\hline '
    for qn, k, cells in r8:
        o += qn + ''.join(' & ' + ('$%s$' % cells[c] if c == k else (r'$\res{%s}$' % cells[c] if sol else '')) for c in ('sin', 'cos', 'tan')) + r'\\\hline '
    return o + r'\end{tabular}\end{center}'
# 10-12: totes les raons
def six(sn, c):
    return r'$\sin\alpha\approx%s$, $\cos\alpha\approx%s$, $\text{tg}\,\alpha\approx%s$, $\text{cosec}\,\alpha\approx%s$, $\sec\alpha\approx%s$, $\text{cotg}\,\alpha\approx%s$' % tuple(
        r'\res{%s}' % dec(x, 2, False) for x in (sn, c, sn / c, 1 / sn, 1 / c, c / sn))
c10 = -math.sqrt(1 - .62 ** 2); s11 = -math.sqrt(1 - .83 ** 2); c12 = 1 / math.sqrt(1 + .92 ** 2)
e13 = [(r'\sin13290^\circ', 13290, 'sin', r'\sin330^\circ=-\frac12'), (r'\cos(-1680^\circ)', -1680, 'cos', r'\cos120^\circ=-\frac12'), (r'\text{tg}\,3825^\circ', 3825, 'tan', r'\text{tg}\,225^\circ=1'),
       (r'\cos4995^\circ', 4995, 'cos', r'\cos315^\circ=\frac{\sqrt2}{2}'), (r'\sin(-1710^\circ)', -1710, 'sin', r'\sin90^\circ=1'), (r'\text{tg}\,3630^\circ', 3630, 'tan', r'\text{tg}\,30^\circ=\frac{\sqrt3}{3}'),
       (r'\cos(-36000^\circ)', -36000, 'cos', r'\cos0^\circ=1'), (r'\sin(-330^\circ)', -330, 'sin', r'\sin30^\circ=\frac12')]
for t, d, k, s in e13:
    v = {'sin': sin, 'cos': cos, 'tan': tan}[k](d)
    ck(v, num(s.split('=')[-1]), 1e-9, t)
S.append(("Razones trigonométricas de ángulos cualesquiera", [
 (1, r"Completa la tabla siguiente sin calculadora:" + t6q, t6s),
 (1, r"Sin utilizar la calculadora, calcula:" + tasks(2, ['$%s$' % t for t, _, _ in e7]), tasks(4, [R(str(a)) for _, a, _ in e7])),
 (2, r"La tabla muestra razones trigonométricas de ángulos de cuadrantes diferentes. Sin determinarlos, complétala con las razones que faltan." + tab8(False), tab8(True)),
 (1, r"Calcula el seno, el coseno y la tangente del ángulo $\alpha$:" + tasks(2, [r'$\sec\alpha=4$ \ y \ $270^\circ<\alpha<360^\circ$', r'$\text{cotg}\,\alpha=-\frac12$ \ y \ $\frac{\pi}{2}<\alpha<\pi$']),
     tasks(1, [r'$\cos\alpha=\frac14$, $\sin\alpha=\res{-\frac{\sqrt{15}}{4}}$ (negativo en el cuarto cuadrante), $\text{tg}\,\alpha=\res{-\sqrt{15}}$',
               r'$\text{tg}\,\alpha=-2$, $\cos\alpha=-\frac{1}{\sqrt{1+4}}=\res{-\frac{\sqrt5}{5}}$, $\sin\alpha=\text{tg}\,\alpha\cdot\cos\alpha=\res{\frac{2\sqrt5}{5}}$'])),
 (1, r"Sabiendo que el ángulo $\alpha$ está en el segundo cuadrante ($90^\circ<\alpha<180^\circ$) y $\sin\alpha=0{,}62$, calcula las otras razones trigonométricas.", six(.62, c10)),
 (1, r"Sabiendo que el ángulo $\alpha$ está en el tercer cuadrante ($180^\circ<\alpha<270^\circ$) y $\cos\alpha=-0{,}83$, calcula las otras razones trigonométricas.", six(s11, -.83)),
 (1, r"Sabiendo que el ángulo $\alpha$ está en el cuarto cuadrante ($270^\circ<\alpha<360^\circ$) y $\text{tg}\,\alpha=-0{,}92$, calcula las otras razones trigonométricas.", six(-.92 * c12, c12)),
 (1, r"Determina el valor exacto de estas razones trigonométricas:" + tasks(4, ['$%s$' % t for t, _, _, _ in e13]),
     tasks(2, [r'$%s=%s$' % (t, s.rsplit('=', 1)[0] + r'=\res{' + s.rsplit('=', 1)[1] + '}') for t, _, _, s in e13])),
]))
ck(math.sqrt(15) / 4, math.sqrt(1 - 1 / 16)); ck(-2 * S5 / 5 / (-S5 / 5) * -1, -2)

# =====================================================================
# 5. Relacions entre raons
a14 = 180 - atan(S5 / 2)
ck(math.tan(r(a14)), -S5 / 2); ck(cos(a14), -2 / 3); ck(sin(a14), S5 / 3)
e16 = [(r'\cos48^\circ', r'\sin42^\circ', '0{,}67', cos(48), sin(42)), (r'\sin(-48^\circ)', r'-\cos42^\circ', '-0{,}74', sin(-48), -cos(42)), (r'\sin138^\circ', r'\sin42^\circ', '0{,}67', sin(138), sin(42)),
       (r'\text{tg}\,318^\circ', r'-\text{tg}\,42^\circ', '-0{,}9', tan(318), -tan(42)), (r'\cos222^\circ', r'-\cos42^\circ', '-0{,}74', cos(222), -cos(42)), (r'\text{tg}\,858^\circ', r'\text{tg}\,138^\circ=-\text{tg}\,42^\circ', '-0{,}9', tan(858), -tan(42))]
for _, _, _, a, b in e16: ck(a, b, 1e-9)
S.append(("Relaciones entre las razones trigonométricas de algunos ángulos", [
 (2, r"\begin{tasks}(1)\task Halla $\sin\alpha$, $\cos\alpha$, $\sin(180^\circ-\alpha)$, $\cos(90^\circ+\alpha)$ y $\text{tg}\,(180^\circ+\alpha)$, sin calcular el ángulo $\alpha$, sabiendo que $\text{tg}\,\alpha=-\frac{\sqrt5}{2}$ y $90^\circ<\alpha<180^\circ$. \task Halla con la calculadora el valor del ángulo $\alpha$.\end{tasks}",
     tasks(1, [r'$\cos\alpha=\res{-\frac23}$, $\sin\alpha=\res{\frac{\sqrt5}{3}}$, $\sin(180^\circ-\alpha)=\sin\alpha=\res{\frac{\sqrt5}{3}}$, $\cos(90^\circ+\alpha)=-\sin\alpha=\res{-\frac{\sqrt5}{3}}$, $\text{tg}\,(180^\circ+\alpha)=\text{tg}\,\alpha=\res{-\frac{\sqrt5}{2}}$',
               r'$\alpha=180^\circ-\text{tg}^{-1}\frac{\sqrt5}{2}\approx\res{%s}$' % dms(a14)])),
 (1, r"Sabiendo que $\cos\alpha=0{,}8$ y $\sin\alpha=0{,}6$, calcula:" + tasks(3, [r'$\cos(180^\circ+\alpha)$', r'$\sin(180^\circ-\alpha)$', r'$\text{tg}\,(-\alpha)$', r'$\sin(90^\circ-\alpha)$', r'$\cos(90^\circ+\alpha)$', r'$\text{tg}\,(90^\circ-\alpha)$']),
     tasks(3, [R('-0{,}8'), R('0{,}6'), R(r'-0{,}75'), R('0{,}8'), R('-0{,}6'), R(r'\frac43')])),
 (1, r"Si $\sin42^\circ=0{,}67$, $\cos42^\circ=0{,}74$ y $\text{tg}\,42^\circ=0{,}9$, halla las razones trigonométricas siguientes sin utilizar la calculadora:" + tasks(3, ['$%s$' % t for t, _, _, _, _ in e16]),
     tasks(2, [r'$%s=%s=\res{%s}$' % (t, a, v) for t, a, v, _, _ in e16])),
]))

# =====================================================================
# 6. Triangles rectangles
a17, b17 = 32 * cos(57), 32 * sin(57); c17b = math.hypot(250, 308); A17b = atan(250 / 308); b17c, c17c = 35 / tan(32), 35 / sin(32)
h18, d18 = 12 * sin(50), 12 * cos(50)
AB19 = 4 * cos(60) + 1.7 * cos(30) + 3.5 * cos(20) + 4.2 * cos(50)
h20 = 6 * tan(15) + 5 * tan(25)
l21 = 5 / sin(20); hh21 = 5 / tan(20)
roof = r'''\begin{center}\begin{tikzpicture}[scale=0.62]
\coordinate (A) at (0,0); \coordinate (P) at ($(A)+(60:4)$); \coordinate (Q) at ($(P)+(-30:1.7)$); \coordinate (R) at ($(Q)+(20:3.5)$); \coordinate (B) at ($(R|-A)+(2.7,0)$);
\draw[muted, dashed] (A)--(B); \draw[muted, dashed] (P)--++(1.6,0); \draw[muted, dashed] (Q)--++(1.5,0);
\draw[navy, line width=2.2pt, line join=round] (A)--(P)--(Q)--(R)--(B);
\node[below left] at (A) {$A$}; \node[below right] at (B) {$B$};
\node[font=\small, rotate=60] at ($(A)!0.5!(P)+(-0.4,0.22)$) {4 m}; \node[font=\small, rotate=-30] at ($(P)!0.5!(Q)+(-0.25,-0.45)$) {1,7 m};
\node[font=\small, rotate=20] at ($(Q)!0.5!(R)+(-0.15,0.42)$) {3,5 m}; \node[font=\small, rotate=-55] at ($(R)!0.5!(B)+(0.45,0.3)$) {4,2 m};
\draw (A)++(0.7,0) arc (0:60:0.7); \node[font=\scriptsize] at (1.05,0.4) {$60^\circ$};
\draw (P)++(0.75,0) arc (0:-30:0.75); \node[font=\scriptsize] at ($(P)+(1.35,-0.2)$) {$30^\circ$};
\draw (Q)++(0.75,0) arc (0:20:0.75); \node[font=\scriptsize] at ($(Q)+(1.3,0.12)$) {$20^\circ$};
\draw (B)++(-0.7,0) arc (180:125:0.7); \node[font=\scriptsize] at ($(B)+(-1.05,0.35)$) {$50^\circ$};
\end{tikzpicture}\end{center}'''
S.append(("Resolución de triángulos rectángulos", [
 (1, r"Los triángulos siguientes son rectángulos y se llaman $ABC$, con el ángulo recto en $C$. Resuélvelos:" + tasks(1, [r"Datos: $c=32$ cm, $\hat B=57^\circ$. Calcula $a$ y $b$.", r"Datos: $a=250$ m, $b=308$ m. Calcula $c$ y $\hat A$.", r"Datos: $a=35$ cm, $\hat A=32^\circ$. Calcula $b$ y $c$."]),
     tasks(1, [r'$a=c\cos\hat B\approx\res{%s\ \text{cm}}$, \ $b=c\sin\hat B\approx\res{%s\ \text{cm}}$ \ ($\hat A=33^\circ$)' % (dec(a17), dec(b17)),
               r'$c=\sqrt{250^2+308^2}\approx\res{%s\ \text{m}}$, \ $\text{tg}\,\hat A=\frac{250}{308}\Rightarrow\hat A\approx\res{%s}$' % (dec(c17b), dms(A17b)),
               r'$b=\dfrac{a}{\text{tg}\,\hat A}\approx\res{%s\ \text{cm}}$, \ $c=\dfrac{a}{\sin\hat A}\approx\res{%s\ \text{cm}}$ \ ($\hat B=58^\circ$)' % (dec(b17c), dec(c17c))])),
 (1, r"Un mástil está sujeto al suelo con dos cables de 12 m que forman ángulos de $50^\circ$ con el suelo. Calcula la altura del mástil y la distancia de la base a los puntos de sujeción.",
     r'Altura: $12\sin50^\circ\approx\res{%s\ \text{m}}$. Distancia: $12\cos50^\circ\approx\res{%s\ \text{m}}$.' % (dec(h18), dec(d18))),
 (2, r"El tejado de una casa tiene la forma y las medidas que se indican en la figura. Calcula la distancia $\overline{AB}$." + roof,
     r'Con $A$ y $B$ a la misma altura, como en la figura, sumamos las proyecciones horizontales de los cuatro tramos: $4\cos60^\circ+1{,}7\cos30^\circ+3{,}5\cos20^\circ+4{,}2\cos50^\circ\approx2+%s+%s+%s\approx\res{%s\ \text{m}}$' % (dec(1.7 * cos(30)), dec(3.5 * cos(20)), dec(4.2 * cos(50)), dec(AB19))),
 (2, r"Un avión despega formando un ángulo de $15^\circ$ con el suelo. A 6 km del punto de salida (en horizontal) aumenta $10^\circ$ la inclinación, de manera que sube con un ángulo de $25^\circ$ con el suelo. Una montaña de 2\,500 m se encuentra a 11 km del punto de partida. ¿Volará el avión por encima de la montaña o tendrá que cambiar la dirección?",
     r'Altura a los 6 km: $6\,\text{tg}\,15^\circ\approx%s$ km. A los 11 km: $%s+5\,\text{tg}\,25^\circ\approx\res{%s\ \text{km}}>2{,}5$ km: \rest{pasa por encima de la montaña}.' % (dec(6 * tan(15), 3), dec(6 * tan(15), 3), dec(h20, 3))),
 (2, r"En un triángulo isósceles, el lado desigual mide 10 m y el ángulo opuesto es de $40^\circ$. Calcula su perímetro y su área.",
     r"La altura lo divide en dos triángulos rectángulos con un cateto de 5 m y un ángulo de $20^\circ$: lado igual $=\dfrac{5}{\sin20^\circ}\approx%s$ m, altura $=\dfrac{5}{\text{tg}\,20^\circ}\approx%s$ m. Perímetro $\approx\res{%s\ \text{m}}$, área $\approx\res{%s\ \text{m}^2}$." % (dec(l21), dec(hh21), dec(10 + 2 * l21), dec(5 * hh21))),
 (1, r"Calcula el área de un paralelogramo cuyos lados, de 9 cm y 16 cm, forman un ángulo de $65^\circ$.",
     r'$S=9\cdot16\cdot\sin65^\circ\approx\res{%s\ \text{cm}^2}$' % dec(144 * sin(65))),
]))

# =====================================================================
# 7. Teoremes del sinus i del cosinus
def SSS(a, b, c):
    A = acos((b * b + c * c - a * a) / (2 * b * c)); B = acos((a * a + c * c - b * b) / (2 * a * c)); return A, B, 180 - A - B
def SAS(b, c, A):
    a = math.sqrt(b * b + c * c - 2 * b * c * cos(A)); B = acos((a * a + c * c - b * b) / (2 * a * c)); return a, B, 180 - A - B
A23a = SSS(10, 14, 8)
a23b, B23b, C23b = SAS(6, 9, DMS(39, 12))
A23c = 180 - DMS(38, 49) - DMS(66, 40); b23c = 7 * sin(DMS(38, 49)) / sin(A23c); c23c = 7 * sin(DMS(66, 40)) / sin(A23c)
A23d = asin(8 * sin(DMS(36, 38)) / 10); assert A23d + 180 - A23d > 0 and (180 - A23d) + DMS(36, 38) > 180; C23d = 180 - A23d - DMS(36, 38); c23d = 10 * sin(C23d) / sin(DMS(36, 38))
b23e = math.sqrt(81 + 25 - 90 * cos(DMS(103, 27))); A23e = asin(9 * sin(DMS(103, 27)) / b23e); C23e = 180 - A23e - DMS(103, 27)
ck(A23e + C23e + DMS(103, 27), 180)
def typ(a, b, c):
    x = sorted([a, b, c])
    if x[2] >= x[0] + x[1]: return r'\rest{no es un triángulo} ($%d\geq%d+%d$)' % (x[2], x[0], x[1])
    q = x[2] ** 2 - x[0] ** 2 - x[1] ** 2
    return r'$%d^2=%d$ %s $%d^2+%d^2=%d$: \rest{%s}' % (x[2], x[2] ** 2, '<' if q < 0 else '=' if q == 0 else '>', x[0], x[1], x[0] ** 2 + x[1] ** 2, 'acutángulo' if q < 0 else 'rectángulo' if q == 0 else 'obtusángulo')
S.append(("Teorema del seno y teorema del coseno", [
 (2, r"Resuelve los triángulos siguientes:" + tasks(1, [r'$a=10$ cm, \ $b=14$ cm, \ $c=8$ cm', r"$b=6$ cm, \ $c=9$ cm, \ $\hat A=39^\circ12'$", r"$a=7$ cm, \ $\hat B=38^\circ49'$, \ $\hat C=66^\circ40'$",
                                                         r"$a=8$ cm, \ $b=10$ cm, \ $\hat B=36^\circ38'$", r"$a=9$ cm, \ $c=5$ cm, \ $\hat B=103^\circ27'$"]),
     tasks(1, [r'Teorema del coseno: $\hat A\approx\res{%s}$, $\hat B\approx\res{%s}$, $\hat C\approx\res{%s}$' % tuple(dms(x) for x in A23a),
               r'Teorema del coseno: $a\approx\res{%s\ \text{cm}}$; $\hat B\approx\res{%s}$, $\hat C\approx\res{%s}$' % (dec(a23b), dms(B23b), dms(C23b)),
               r'$\hat A=\res{%s}$; teorema del seno: $b\approx\res{%s\ \text{cm}}$, $c\approx\res{%s\ \text{cm}}$' % (dms(A23c), dec(b23c), dec(c23c)),
               r"Teorema del seno: $\sin\hat A\approx%s\Rightarrow\hat A\approx\res{%s}$ (el obtuso no cabe); $\hat C\approx\res{%s}$, $c\approx\res{%s\ \text{cm}}$" % (dec(8 * sin(DMS(36, 38)) / 10, 4), dms(A23d), dms(C23d), dec(c23d)),
               r'Teorema del coseno: $b\approx\res{%s\ \text{cm}}$; $\hat A\approx\res{%s}$, $\hat C\approx\res{%s}$' % (dec(b23e), dms(A23e), dms(C23e))])),
 (1, r"Decide si las medidas siguientes corresponden a las longitudes de los lados de un triángulo y, si es así, indica si es acutángulo, rectángulo u obtusángulo." + tasks(4, ['12, 11 y 9 cm', '23, 14 y 8 cm', '26, 24 y 10 cm', '40, 30 y 20 m']),
     tasks(2, [typ(12, 11, 9), typ(23, 14, 8), typ(26, 24, 10), typ(40, 30, 20)])),
]))

# =====================================================================
# 8. Resolució de triangles (problemes)
ang27 = acos((36 + 144 - 64) / 144)
x28 = 30 * tan(28) / (tan(40) - tan(28)); h28 = x28 * tan(40)
w29 = 25 * tan(atan(50 / 25) + 15) - 50
d30 = 40 / sin(15)
h31 = 15 / (1 / tan(43) + 1 / tan(DMS(57, 50)))
a32 = math.sqrt(2 * 28 / S3); b32 = a32 * S3; c32 = 2 * a32
ang33 = atan(1.7 / .5)
area34 = 12 * 8 / cos(18)
d35 = [math.sqrt((5 * t) ** 2 + (4 * t) ** 2 - 2 * 20 * t * t * cos(54)) for t in (2, 6)]
s36a, s36b = 8 * sin(37) / sin(93), 8 * sin(50) / sin(93); dist36 = s36a * sin(50)
ck(s36b * sin(37), dist36, 1e-9)
h37 = 8 * sin(65); p37 = 8 * cos(65); B37 = math.sqrt(225 - h37 ** 2) + p37; b37 = B37 - 2 * p37; area37 = (B37 + b37) / 2 * h37
ang38 = acos(3 / 5)
ang39 = 2 * atan(6 / 10)
ap40 = acos((100 + 100 - 225) / 200); bs40 = (180 - ap40) / 2
ang41 = acos((25 + 64 - 100) / 80)
S.append(("Resolución de triángulos: problemas", [
 (1, r"Una barca está atada a la orilla de un canal con una cuerda de 8 metros. En un determinado momento, esta cuerda forma un ángulo de $38^\circ$ con la orilla. ¿A qué distancia de la orilla está la barca?",
     r'$8\sin38^\circ\approx\res{%s\ \text{m}}$' % dec(8 * sin(38))),
 (1, r"Si nos situamos a 40 metros de la chimenea de una fábrica, la vemos bajo un ángulo de $26^\circ$. ¿Qué altura tiene? Considera que los ojos del observador están situados a 175 cm del suelo.",
     r'$40\,\text{tg}\,26^\circ+1{,}75\approx%s+1{,}75\approx\res{%s\ \text{m}}$' % (dec(40 * tan(26)), dec(40 * tan(26) + 1.75))),
 (2, r"La anchura de un escenario de teatro es de 8 metros. Las localidades que hemos comprado están situadas a una distancia de 6 m y de 12 m de cada uno de los extremos laterales del escenario. ¿Cuál es el ángulo de visión que tendremos para ver la representación?",
     r'Teorema del coseno: $\cos\theta=\dfrac{6^2+12^2-8^2}{2\cdot6\cdot12}=\dfrac{116}{144}\Rightarrow\theta\approx\res{%s}$' % dms(ang27)),
 (2, r"Desde un punto del suelo medimos el ángulo bajo el que se ve un edificio y obtenemos $40^\circ$. Nos alejamos 30 m y el ángulo es ahora de $28^\circ$. Calcula la altura del edificio y la distancia desde la que se hizo la primera observación.",
     r'$h=x\,\text{tg}\,40^\circ=(x+30)\,\text{tg}\,28^\circ\Rightarrow x=\dfrac{30\,\text{tg}\,28^\circ}{\text{tg}\,40^\circ-\text{tg}\,28^\circ}\approx\res{%s\ \text{m}}$, \ $h\approx\res{%s\ \text{m}}$' % (dec(x28), dec(h28))),
 (3, r"Desde una torre de vigilancia de 25 m de altura observamos dos árboles situados en orillas opuestas de un río bajo un ángulo de $15^\circ$. Los dos árboles están alineados con el pie de la torre y la distancia de esta al río es de 50 m. Calcula la anchura del río.",
     r"La visual al árbol cercano forma con la vertical un ángulo $\alpha$ con $\text{tg}\,\alpha=\frac{50}{25}=2$, es decir, $\alpha\approx%s$. La del árbol lejano forma $\alpha+15^\circ$: $50+x=25\,\text{tg}\,(\alpha+15^\circ)\Rightarrow x\approx\res{%s\ \text{m}}$" % (dms(atan(2)), dec(w29))),
 (1, r"El radar de un barco detecta un objeto no identificado a 40 m de profundidad y en una dirección que forma $15^\circ$ con la horizontal. ¿Qué distancia tiene que recorrer un buzo para llegar desde el barco hasta el objeto?",
     r'$d=\dfrac{40}{\sin15^\circ}\approx\res{%s\ \text{m}}$' % dec(d30)),
 (2, r"Un árbol se sujeta al suelo con dos cables de acero, uno a cada lado, que forman ángulos de $43^\circ$ y de $57^\circ50'$ con el suelo. Si las distancias de los cables al pie del árbol suman 15 m, ¿cuál es la altura del árbol?",
     r"$\dfrac{h}{\text{tg}\,43^\circ}+\dfrac{h}{\text{tg}\,57^\circ50'}=15\Rightarrow h\approx\res{%s\ \text{m}}$" % dec(h31)),
 (2, r"El área de un triángulo rectángulo es de 28 cm$^2$ y uno de sus ángulos mide $60^\circ$." + tasks(1, ["¿Cuánto mide cada uno de sus ángulos?", "Calcula la longitud de los lados y el perímetro del triángulo."]),
     tasks(1, [r'$\res{30^\circ,\ 60^\circ\ \text{y}\ 90^\circ}$', r'Catetos $x$ y $x\sqrt3$: $\frac{x^2\sqrt3}{2}=28\Rightarrow x\approx\res{%s}$, el otro cateto $\approx\res{%s}$, hipotenusa $\approx\res{%s}$ cm; perímetro $\approx\res{%s\ \text{cm}}$' % (dec(a32), dec(b32), dec(c32), dec(a32 + b32 + c32))])),
 (1, r"Salvador mide 1,70 m y observa que su sombra es de 50 cm a una determinada hora del día. ¿Con qué inclinación llegan los rayos solares a esa hora?",
     r'$\text{tg}\,\alpha=\frac{1{,}70}{0{,}50}=3{,}4\Rightarrow\alpha\approx\res{%s}$' % dms(ang33)),
 (2, r"Una casa de planta rectangular mide 12 m de largo y 8 m de ancho. El techo, con una inclinación de $18^\circ$, es una superficie plana inclinada cuya parte más elevada está situada sobre uno de los lados mayores del rectángulo. Calcula el área del tejado.",
     r"La anchura del tejado es $\dfrac{8}{\cos18^\circ}\approx%s$ m: área $\approx12\cdot%s\approx\res{%s\ \text{m}^2}$" % (dec(8 / cos(18)), dec(8 / cos(18)), dec(area34))),
 (2, r"Dos exploradores se han perdido y deciden seguir caminos diferentes para conseguir ayuda; sus trayectorias forman un ángulo de $54^\circ$. Si uno camina a 5 km/h y el otro a 4 km/h, ¿a qué distancia están al cabo de 2 horas? ¿Y después de 6 horas?",
     r'Después de 2 h han recorrido 10 y 8 km: $d=\sqrt{10^2+8^2-2\cdot10\cdot8\cos54^\circ}\approx\res{%s\ \text{km}}$. Después de 6 h (el triple): $\approx\res{%s\ \text{km}}$.' % (dec(d35[0]), dec(d35[1]))),
 (3, r"En una pared hay dos argollas separadas 8 m entre sí. Un niño ata cada extremo de una cuerda a las argollas y se aleja de la pared hasta que la cuerda queda tensa. En ese momento, la cuerda forma ángulos de $50^\circ$ y $37^\circ$ con la pared." + tasks(2, ["¿Cuánto mide la cuerda?", "¿A qué distancia de la pared está el niño?"]),
     tasks(1, [r'El tercer ángulo es $93^\circ$. Teorema del seno: tramos de $\dfrac{8\sin37^\circ}{\sin93^\circ}\approx%s$ m y $\dfrac{8\sin50^\circ}{\sin93^\circ}\approx%s$ m: cuerda $\approx\res{%s\ \text{m}}$' % (dec(s36a), dec(s36b), dec(s36a + s36b)),
               r'$d=%s\cdot\sin50^\circ\approx\res{%s\ \text{m}}$' % (dec(s36a), dec(dist36))])),
 (3, r"Uno de los ángulos de un trapecio isósceles mide $65^\circ$, los lados iguales miden 8 cm y la diagonal mide 15 cm. Determina su área.",
     r"Altura $h=8\sin65^\circ\approx%s$; proyección del lado $8\cos65^\circ\approx%s$. Por Pitágoras con la diagonal, la base mayor es $B\approx%s+%s\approx%s$ y la menor $b\approx%s$ cm. Área $=\frac{B+b}{2}\,h\approx\res{%s\ \text{cm}^2}$" % (dec(h37), dec(p37), dec(math.sqrt(225 - h37 ** 2)), dec(p37), dec(B37), dec(b37), dec(area37))),
 (2, r"Las bases de un trapecio isósceles miden 8 cm y 14 cm, y los lados iguales, 5 cm. Calcula la medida de los ángulos del trapecio.",
     r'Proyección del lado: $\frac{14-8}{2}=3$ cm: $\cos\alpha=\frac35\Rightarrow\alpha\approx\res{%s}$ (dos ángulos) y $180^\circ-\alpha\approx\res{%s}$ (los otros dos)' % (dms(ang38), dms(180 - ang38))),
 (1, r"¿Qué ángulo forman entre sí las diagonales de un rectángulo de 10 cm de base y 6 cm de altura?",
     r'$2\,\text{tg}^{-1}\frac{6}{10}\approx\res{%s}$ \ (y el suplementario, $\res{%s}$)' % (dms(ang39), dms(180 - ang39))),
 (2, r"En una construcción, dos vigas de 10 m están soldadas por los extremos y forman un triángulo con otra viga de 15 m. Halla los ángulos que forman entre ellas.",
     r'$\cos\theta=\dfrac{10^2+10^2-15^2}{2\cdot10\cdot10}=-0{,}125\Rightarrow\theta\approx\res{%s}$; los otros dos: $\res{%s}$' % (dms(ap40), dms(bs40))),
 (2, r"En un romboide, los lados miden 5 cm y 8 cm y una de las diagonales mide 10 cm. Calcula la medida de sus cuatro ángulos.",
     r'$\cos\alpha=\dfrac{5^2+8^2-10^2}{2\cdot5\cdot8}=-\frac{11}{80}\Rightarrow\alpha\approx\res{%s}$ (dos ángulos) y $\res{%s}$ (los otros dos)' % (dms(ang41), dms(180 - ang41))),
]))

# =====================================================================
# 9. Fórmules trigonomètriques  (Trigonometria 2, exercicis 1-10)
sa, ca, sb, cb = .6, .8, .8, .6
ck(sa * cb + ca * sb, 1); ck(sa * cb - ca * sb, -.28); ck(ca * cb - sa * sb, 0, 1e-12); ck(ca * cb + sa * sb, .96); ck((.75 - 4 / 3) / (1 + .75 * 4 / 3), -7 / 24)
s10, c10_, s40, c40 = math.sqrt((1 - .94) / 2), math.sqrt((1 + .94) / 2), 2 * .34 * .94, .94 ** 2 - .34 ** 2
# 6
ca6, sb6 = -4 / 5, -math.sqrt(15) / 4
ck(ca6 * -.25 - .6 * sb6, (4 + 3 * math.sqrt(15)) / 20); ck(.6 * -.25 - ca6 * sb6, (-3 - 4 * math.sqrt(15)) / 20)
a6 = 180 - asin(.6); b6 = 180 + acos(.25)
ck(cos(a6 + b6), (4 + 3 * math.sqrt(15)) / 20); ck(sin(a6 - b6), (-3 - 4 * math.sqrt(15)) / 20); ck(tan(2 * a6), -24 / 7); ck(tan(b6 / 2), -math.sqrt(15) / 3)
for a7 in (atan(3), atan(3) + 180): ck(sin(2 * a7), .6); ck(cos(2 * a7), -.8); ck(tan(2 * a7), -.75)
a8 = acos(-2 / 3); ck(sin(a8 / 2), math.sqrt(30) / 6); ck(cos(a8 / 2), S6 / 6); ck(tan(a8 / 2), S5)
a5 = 180 - asin(.6); ck(sin(a5 / 2), 3 * math.sqrt(10) / 10); ck(cos(a5 / 2), math.sqrt(10) / 10); ck(tan(a5 / 2), 3)
ck(sin(15), (S6 - S2) / 4); ck(cos(15), (S6 + S2) / 4); ck(tan(15), 2 - S3); ck(sin(75), (S6 + S2) / 4); ck(cos(75), (S6 - S2) / 4); ck(tan(75), 2 + S3)
ids9 = [
 (r'\dfrac{\sin\alpha-\cos\alpha}{\text{tg}\,\alpha-1}=\cos\alpha', lambda a: (sin(a) - cos(a)) / (tan(a) - 1) - cos(a), r'$\dfrac{\sin\alpha-\cos\alpha}{\frac{\sin\alpha-\cos\alpha}{\cos\alpha}}=\cos\alpha$'),
 (r'\text{tg}^2\alpha-\sin^2\alpha=\text{tg}^2\alpha\cdot\sin^2\alpha', lambda a: tan(a) ** 2 - sin(a) ** 2 - tan(a) ** 2 * sin(a) ** 2, r'$\dfrac{\sin^2\alpha-\sin^2\alpha\cos^2\alpha}{\cos^2\alpha}=\dfrac{\sin^2\alpha(1-\cos^2\alpha)}{\cos^2\alpha}=\text{tg}^2\alpha\sin^2\alpha$'),
 (r'\dfrac{1+\text{cotg}\,\alpha}{\sin\alpha+\cos\alpha}=\text{cosec}\,\alpha', lambda a: (1 + 1 / tan(a)) / (sin(a) + cos(a)) - 1 / sin(a), r'$\dfrac{\frac{\sin\alpha+\cos\alpha}{\sin\alpha}}{\sin\alpha+\cos\alpha}=\dfrac{1}{\sin\alpha}$'),
 (r'\sec^2\alpha-1=\text{tg}^2\alpha', lambda a: 1 / cos(a) ** 2 - 1 - tan(a) ** 2, r'$\dfrac{1-\cos^2\alpha}{\cos^2\alpha}=\dfrac{\sin^2\alpha}{\cos^2\alpha}$'),
 (r'\dfrac{1+\sin2\alpha}{1+\cos2\alpha}=\tfrac12(1+\text{tg}\,\alpha)^2', lambda a: (1 + sin(2 * a)) / (1 + cos(2 * a)) - (1 + tan(a)) ** 2 / 2, r'$\dfrac{\sin^2\alpha+\cos^2\alpha+2\sin\alpha\cos\alpha}{2\cos^2\alpha}=\dfrac{(\sin\alpha+\cos\alpha)^2}{2\cos^2\alpha}=\frac12(\text{tg}\,\alpha+1)^2$'),
 (r'2\,\text{tg}\,\alpha\sin^2\tfrac{\alpha}{2}+\sin\alpha=\text{tg}\,\alpha', lambda a: 2 * tan(a) * sin(a / 2) ** 2 + sin(a) - tan(a), r'$2\,\text{tg}\,\alpha\cdot\dfrac{1-\cos\alpha}{2}+\sin\alpha=\text{tg}\,\alpha-\sin\alpha+\sin\alpha$'),
 (r'\cos3\alpha=4\cos^3\alpha-3\cos\alpha', lambda a: cos(3 * a) - 4 * cos(a) ** 3 + 3 * cos(a), r'$\cos2\alpha\cos\alpha-\sin2\alpha\sin\alpha=(2\cos^2\alpha-1)\cos\alpha-2(1-\cos^2\alpha)\cos\alpha$'),
 (r'\dfrac{\text{tg}\,\alpha}{\cos2\alpha}=\text{tg}\,2\alpha-\text{tg}\,\alpha', lambda a: tan(a) / cos(2 * a) - tan(2 * a) + tan(a), r'$\dfrac{\sin2\alpha}{\cos2\alpha}-\dfrac{\sin\alpha}{\cos\alpha}=\dfrac{\sin(2\alpha-\alpha)}{\cos2\alpha\cos\alpha}=\dfrac{\text{tg}\,\alpha}{\cos2\alpha}$'),
 (r'\text{tg}\,\alpha+\text{cotg}\,\alpha=\sec\alpha\cdot\text{cosec}\,\alpha', lambda a: tan(a) + 1 / tan(a) - 1 / (cos(a) * sin(a)), r'$\dfrac{\sin^2\alpha+\cos^2\alpha}{\sin\alpha\cos\alpha}=\dfrac{1}{\cos\alpha}\cdot\dfrac{1}{\sin\alpha}$'),
 (r'\dfrac{\sin2\alpha}{1+\cos2\alpha}=\text{tg}\,\alpha', lambda a: sin(2 * a) / (1 + cos(2 * a)) - tan(a), r'$\dfrac{2\sin\alpha\cos\alpha}{2\cos^2\alpha}=\dfrac{\sin\alpha}{\cos\alpha}$'),
 (r'\dfrac{1}{\text{tg}^2\alpha}=\cos^2\alpha+\left(\dfrac{\cos\alpha}{\text{tg}\,\alpha}\right)^2', lambda a: 1 / tan(a) ** 2 - cos(a) ** 2 - (cos(a) / tan(a)) ** 2, r'$\cos^2\alpha+\dfrac{\cos^4\alpha}{\sin^2\alpha}=\dfrac{\cos^2\alpha(\sin^2\alpha+\cos^2\alpha)}{\sin^2\alpha}=\dfrac{1}{\text{tg}^2\alpha}$')]
for _, f, _ in ids9:
    for a in (17, 33.3, 71, 128, 200, 301.5): ck(f(a), 0, 1e-8)
ids10 = [
 (r'\cos\alpha\cos(\alpha-\beta)+\sin\alpha\sin(\alpha-\beta)=\cos\beta', lambda a, b: cos(a) * cos(a - b) + sin(a) * sin(a - b) - cos(b), r'Es $\cos\big(\alpha-(\alpha-\beta)\big)=\cos\beta$.'),
 (r'\sin(\alpha+\beta)\cdot\sin(\alpha-\beta)=\sin^2\alpha-\sin^2\beta', lambda a, b: sin(a + b) * sin(a - b) - sin(a) ** 2 + sin(b) ** 2, r'$\sin^2\alpha\cos^2\beta-\cos^2\alpha\sin^2\beta=\sin^2\alpha(1-\sin^2\beta)-(1-\sin^2\alpha)\sin^2\beta$'),
 (r'\dfrac{\cos(\alpha+\beta)+\cos(\alpha-\beta)}{\sin(\alpha+\beta)+\sin(\alpha-\beta)}=\dfrac{1}{\text{tg}\,\alpha}', lambda a, b: (cos(a + b) + cos(a - b)) / (sin(a + b) + sin(a - b)) - 1 / tan(a), r'$\dfrac{2\cos\alpha\cos\beta}{2\sin\alpha\cos\beta}$'),
 (r'(\cos\alpha-\cos\beta)^2+(\sin\alpha+\sin\beta)^2=4\sin^2\dfrac{\alpha+\beta}{2}', lambda a, b: (cos(a) - cos(b)) ** 2 + (sin(a) + sin(b)) ** 2 - 4 * sin((a + b) / 2) ** 2, r'$2-2(\cos\alpha\cos\beta-\sin\alpha\sin\beta)=2-2\cos(\alpha+\beta)=4\sin^2\frac{\alpha+\beta}{2}$')]
for _, f, _ in ids10:
    for a, b in ((17, 40), (100, 33), (250, 71)): ck(f(a, b), 0, 1e-8)
S.append(("Fórmulas trigonométricas", [
 (1, r"Escribe $15^\circ$ y $\frac{5\pi}{12}$ rad como una suma o diferencia de ángulos notables y calcula sus razones trigonométricas de manera exacta.",
     r'$15^\circ=45^\circ-30^\circ$: $\sin=\res{\frac{\sqrt6-\sqrt2}{4}}$, $\cos=\res{\frac{\sqrt6+\sqrt2}{4}}$, $\text{tg}=\res{2-\sqrt3}$. \quad $\frac{5\pi}{12}=75^\circ=45^\circ+30^\circ$: $\sin=\res{\frac{\sqrt6+\sqrt2}{4}}$, $\cos=\res{\frac{\sqrt6-\sqrt2}{4}}$, $\text{tg}=\res{2+\sqrt3}$.'),
 (1, r"Si $\sin\alpha=0{,}6$ y $\sin\beta=0{,}8$, siendo ambos ángulos del primer cuadrante, calcula el valor de:" + tasks(3, [r'$\sin(\alpha+\beta)$', r'$\sin(\alpha-\beta)$', r'$\cos(\alpha+\beta)$', r'$\cos(\alpha-\beta)$', r'$\text{tg}\,(\alpha+\beta)$', r'$\text{tg}\,(\alpha-\beta)$']),
     r'$\cos\alpha=0{,}8$, $\cos\beta=0{,}6$.' + tasks(3, [R('1'), R('-0{,}28'), R('0'), R('0{,}96'), r'$\res{\nexists}$ ($\cos=0$)', R(r'-\frac{7}{24}')])),
 (1, r"Demuestra que $\sin\left(\alpha+\frac{3\pi}{2}\right)=-\cos\alpha$.", r'$\sin\alpha\cos\frac{3\pi}{2}+\cos\alpha\sin\frac{3\pi}{2}=\sin\alpha\cdot0+\cos\alpha\cdot(-1)=\res{-\cos\alpha}$'),
 (2, r"El seno de $20^\circ$ vale 0,34 y el coseno, 0,94. Calcula el seno y el coseno de los ángulos de $10^\circ$ y de $40^\circ$.",
     r'$\sin10^\circ=\sqrt{\frac{1-0{,}94}{2}}\approx\res{%s}$, $\cos10^\circ=\sqrt{\frac{1+0{,}94}{2}}\approx\res{%s}$; \ $\sin40^\circ=2\cdot0{,}34\cdot0{,}94\approx\res{%s}$, $\cos40^\circ=0{,}94^2-0{,}34^2=\res{%s}$' % (dec(s10, 4), dec(c10_, 4), dec(s40, 4), dec(c40, 4))),
 (2, r"Si $\alpha$ es un ángulo del segundo cuadrante y $\sin\alpha=\frac35$, calcula las razones de $\frac{\alpha}{2}$.",
     r'$\cos\alpha=-\frac45$; $45^\circ<\frac\alpha2<90^\circ$: $\sin\frac\alpha2=\res{\frac{3\sqrt{10}}{10}}$, $\cos\frac\alpha2=\res{\frac{\sqrt{10}}{10}}$, $\text{tg}\,\frac\alpha2=\res{3}$'),
 (3, r"Si $\sin\alpha=\frac35$ con $90^\circ<\alpha<180^\circ$, y $\cos\beta=-\frac14$ con $180^\circ<\beta<270^\circ$, halla: \ $\cos(\alpha+\beta)$, \ $\sin(\alpha-\beta)$, \ $\text{tg}\,2\alpha$ \ y \ $\text{tg}\,\frac{\beta}{2}$.",
     r'$\cos\alpha=-\frac45$, $\text{tg}\,\alpha=-\frac34$, $\sin\beta=-\frac{\sqrt{15}}{4}$. \ $\cos(\alpha+\beta)=\res{\frac{4+3\sqrt{15}}{20}}$, \ $\sin(\alpha-\beta)=\res{-\frac{3+4\sqrt{15}}{20}}$, \ $\text{tg}\,2\alpha=\res{-\frac{24}{7}}$, \ $\text{tg}\,\frac\beta2=\res{-\frac{\sqrt{15}}{3}}$ ($\frac\beta2$ es del segundo cuadrante)'),
 (2, r"Sabiendo que $\text{tg}\,\alpha=3$, calcula las razones trigonométricas del ángulo $2\alpha$ si $\alpha$ es un ángulo:" + tasks(2, ['Del primer cuadrante.', 'Del tercer cuadrante.']),
     r'En los dos casos: $\sin2\alpha=\res{\frac35}$, $\cos2\alpha=\res{-\frac45}$, $\text{tg}\,2\alpha=\res{-\frac34}$ (los dos valores de $2\alpha$ difieren en $360^\circ$).'),
 (2, r"Si $\cos\alpha=-\frac23$ y $90^\circ<\alpha<180^\circ$, calcula las razones trigonométricas de $\frac{\alpha}{2}$.",
     r'$45^\circ<\frac\alpha2<90^\circ$: $\sin\frac\alpha2=\sqrt{\frac56}=\res{\frac{\sqrt{30}}{6}}$, $\cos\frac\alpha2=\sqrt{\frac16}=\res{\frac{\sqrt6}{6}}$, $\text{tg}\,\frac\alpha2=\res{\sqrt5}$'),
 (3, r"Demuestra las identidades siguientes:" + tasks(2, ['$%s$' % t for t, _, _ in ids9]), tasks(1, [s for _, _, s in ids9])),
 (3, r"Demuestra las identidades siguientes:" + tasks(1, ['$%s$' % t for t, _, _ in ids10]), tasks(1, [s for _, _, s in ids10])),
]))

# =====================================================================
# 10. Equacions trigonomètriques (Trigonometria 2, exercicis 11-13)
E11 = [
 (r'\sin x=\frac12', lambda x: sin(x) - .5, [30, 150], r'30^\circ+360^\circ k,\ 150^\circ+360^\circ k'),
 (r'\cos x=\frac{\sqrt3}{2}', lambda x: cos(x) - S3 / 2, [30, 330], r'\pm30^\circ+360^\circ k'),
 (r'\text{tg}\,x=1', lambda x: tan(x) - 1, [45, 225], r'45^\circ+180^\circ k'),
 (r'\sin x=-\frac{\sqrt2}{2}', lambda x: sin(x) + S2 / 2, [225, 315], r'225^\circ+360^\circ k,\ 315^\circ+360^\circ k'),
 (r'\cos x=-\frac12', lambda x: cos(x) + .5, [120, 240], r'\pm120^\circ+360^\circ k'),
 (r'1+\cos x=0', lambda x: 1 + cos(x), [180], r'180^\circ+360^\circ k'),
 (r'\sin4x=-\frac{\sqrt3}{2}', lambda x: sin(4 * x) + S3 / 2, [60 + 90 * k for k in range(4)] + [75 + 90 * k for k in range(4)], r'60^\circ+90^\circ k,\ 75^\circ+90^\circ k'),
 (r'\cos2x=\frac{\sqrt2}{2}', lambda x: cos(2 * x) - S2 / 2, [22.5, 157.5, 202.5, 337.5], r'\pm22^\circ30^{\prime}+180^\circ k'),
 (r'\text{tg}\,3x=-1', lambda x: tan(3 * x) + 1, [45 + 60 * k for k in range(6)], r'45^\circ+60^\circ k'),
 (r'\sin\frac x2=0', lambda x: sin(x / 2), [0], r'360^\circ k'),
 (r'\cos\frac x3=-\frac12', lambda x: cos(x / 3) + .5, [], r'360^\circ+1080^\circ k,\ 720^\circ+1080^\circ k'),
 (r'\text{tg}\,\frac{3x}{4}=-\frac{\sqrt3}{3}', lambda x: tan(3 * x / 4) + S3 / 3, [200], r'200^\circ+240^\circ k')]
for t, f, s, _ in E11: ckeq(f, s, t)
def eqsol(s, gen):
    return (degsR(s) if s else r'\rest{ninguna} en $[0^\circ,360^\circ)$') + r'\ \ \small($x=%s$)' % gen
s12 = [
 (r'\cos^2(2x+30^\circ)=\frac12', lambda x: cos(2 * x + 30) ** 2 - .5, [7.5 + 45 * k for k in range(8)], r'$\cos(2x+30^\circ)=\pm\frac{\sqrt2}{2}\Rightarrow2x+30^\circ=45^\circ+90^\circ k\Rightarrow x=7^\circ30^{\prime}+45^\circ k$: '),
 (r'\cos^2x-\sqrt3\sin x\cos x=0', lambda x: cos(x) ** 2 - S3 * sin(x) * cos(x), [30, 90, 210, 270], r'$\cos x(\cos x-\sqrt3\sin x)=0$: $\cos x=0$ o $\text{tg}\,x=\frac{\sqrt3}{3}$: '),
 (r'\sqrt3\cos x-\sin x=1', lambda x: S3 * cos(x) - sin(x) - 1, [30, 270], r'$2\cos(x+30^\circ)=1\Rightarrow x+30^\circ=60^\circ$ o $300^\circ$: '),
 (r'\frac{1-\cos2x}{2}=2\left(\sin^2\frac x2-\cos^2\frac x2\right)', lambda x: (1 - cos(2 * x)) / 2 - 2 * (sin(x / 2) ** 2 - cos(x / 2) ** 2), [acos(1 - S2), 360 - acos(1 - S2)], r'$\sin^2x=-2\cos x\Rightarrow\cos^2x-2\cos x-1=0\Rightarrow\cos x=1-\sqrt2$: '),
 (r'\frac{\sin3x+\sin x}{\cos3x+\cos x}=\sqrt3', lambda x: (sin(3 * x) + sin(x)) / (cos(3 * x) + cos(x)) - S3, [30, 120, 210, 300], r'$\dfrac{2\sin2x\cos x}{2\cos2x\cos x}=\text{tg}\,2x=\sqrt3$: '),
 (r'\sin^3x-\sin x\cos^2x=0', lambda x: sin(x) ** 3 - sin(x) * cos(x) ** 2, [0, 45, 135, 180, 225, 315], r'$\sin x(\sin^2x-\cos^2x)=-\sin x\cos2x=0$: '),
 (r'\sqrt3\sin x+\cos x=2', lambda x: S3 * sin(x) + cos(x) - 2, [60], r'$2\sin(x+30^\circ)=2\Rightarrow x+30^\circ=90^\circ$: '),
 (r'\text{tg}^2\frac x2=1-\cos x', lambda x: tan(x / 2) ** 2 - 1 + cos(x), [0, 90, 270], r'$\dfrac{1-\cos x}{1+\cos x}=1-\cos x\Rightarrow\cos x=1$ o $\cos x=0$: '),
 (r'\frac{\cos4x+\cos2x}{\sin4x-\sin2x}=1', lambda x: (cos(4 * x) + cos(2 * x)) / (sin(4 * x) - sin(2 * x)) - 1, [45, 225], r'$\dfrac{2\cos3x\cos x}{2\cos3x\sin x}=\text{cotg}\,x=1$: '),
 (r'4\sin x+4\cos^2x\,\text{tg}\,x+\text{tg}\,x=0,\ \text{con}\ \text{tg}\,x\neq0', lambda x: (4 * sin(x) + 4 * cos(x) ** 2 * tan(x) + tan(x)) / (1 if abs(sin(x)) > 1e-9 else 0), [120, 240], r'Dividiendo entre $\sin x\neq0$: $4\cos^2x+4\cos x+1=0\Rightarrow\cos x=-\frac12$: ')]
def f12j(x):
    if abs(sin(x)) < 1e-6: return 1.0
    return 4 * sin(x) + 4 * cos(x) ** 2 * tan(x) + tan(x)
s12[9] = s12[9][:1] + (f12j,) + s12[9][2:]
for t, f, s, _ in s12: ckeq(f, s, t)
s13 = [
 (r'3\,\text{cotg}\,x=4-\text{tg}\,x', lambda x: 3 / tan(x) - 4 + tan(x), [45, atan(3), 225, 180 + atan(3)], r'$\text{tg}^2x-4\,\text{tg}\,x+3=0\Rightarrow\text{tg}\,x=1$ o $3$: '),
 (r'\sin2x\cdot\cos x=6\sin^3x', lambda x: sin(2 * x) * cos(x) - 6 * sin(x) ** 3, [0, 30, 150, 180, 210, 330], r'$2\sin x(\cos^2x-3\sin^2x)=0$: $\sin x=0$ o $\text{tg}^2x=\frac13$: '),
 (r'\sin x-2\cos2x=-\frac12', lambda x: sin(x) - 2 * cos(2 * x) + .5, [30, 150, 180 - asin(-.75), 360 + asin(-.75)], r'$8\sin^2x+2\sin x-3=0\Rightarrow\sin x=\frac12$ o $-\frac34$: '),
 (r'\cos(30^\circ+x)=\sin x', lambda x: cos(30 + x) - sin(x), [30, 210], r'$\text{tg}\,x=\frac{\sqrt3}{3}$: '),
 (r'\sin2x=\text{tg}\,x', lambda x: sin(2 * x) - tan(x), [0, 45, 135, 180, 225, 315], r'$\sin x(2\cos^2x-1)=0$: '),
 (r'\cos3x+\cos x=0', lambda x: cos(3 * x) + cos(x), [45, 90, 135, 225, 270, 315], r'$2\cos2x\cos x=0$: '),
 (r'3\sin^2x+\cos^2x+\cos x=0', lambda x: 3 * sin(x) ** 2 + cos(x) ** 2 + cos(x), [180], r'$2\cos^2x-\cos x-3=0\Rightarrow\cos x=-1$ ($\frac32$ no vale): '),
 (r'\text{tg}\,x=\sqrt2\cos x', lambda x: tan(x) - S2 * cos(x), [45, 135], r'$\sqrt2\sin^2x+\sin x-\sqrt2=0\Rightarrow\sin x=\frac{\sqrt2}{2}$: '),
 (r'\sin^2x-\cos^2x=\cos2x-7\sin x', lambda x: sin(x) ** 2 - cos(x) ** 2 - cos(2 * x) + 7 * sin(x), [asin(.25), 180 - asin(.25)], r'$2\cos2x=7\sin x\Rightarrow4\sin^2x+7\sin x-2=0\Rightarrow\sin x=\frac14$ ($-2$ no vale): '),
 (r'5\sec x-4\cos x=8', lambda x: 5 / cos(x) - 4 * cos(x) - 8, [60, 300], r'$4\cos^2x+8\cos x-5=0\Rightarrow\cos x=\frac12$ ($-\frac52$ no vale): '),
 (r'\cos2x=1+4\sin x', lambda x: cos(2 * x) - 1 - 4 * sin(x), [0, 180], r'$-2\sin^2x-4\sin x=0\Rightarrow\sin x=0$ ($-2$ no vale): ')]
for t, f, s, _ in s13: ckeq(f, s, t)
S.append(("Ecuaciones trigonométricas", [
 (1, r"Resuelve las ecuaciones trigonométricas siguientes. Da las soluciones de $[0^\circ,360^\circ)$ y la solución general." + tasks(3, ['$%s$' % t for t, _, _, _ in E11]),
     tasks(1, ['$%s$: ' % t + eqsol(s, g) for t, _, s, g in E11])),
 (2, r"Resuelve en $[0^\circ,360^\circ)$ las ecuaciones trigonométricas siguientes:" + tasks(2, ['$%s$' % t for t, _, _, _ in s12]),
     tasks(1, [p + degsR(s) for _, _, s, p in s12])),
 (2, r"Resuelve en $[0^\circ,360^\circ)$ las ecuaciones trigonométricas siguientes:" + tasks(2, ['$%s$' % t for t, _, _, _ in s13]),
     tasks(1, [p + degsR(s) for _, _, s, p in s13])),
]))

# =====================================================================
# 11. Sistemes (Trigonometria 2, exercicis 14-15)
cksys([lambda x, y: cos(y) - sin(x) - 1, lambda x, y: 4 * sin(x) * cos(y) + 1], [(210, 60), (210, 300), (330, 60), (330, 300)], '14a')
cksys([lambda x, y: cos(x) + cos(y) + .5, lambda x, y: cos(x) * cos(y) + .5], [(60, 180), (300, 180), (180, 60), (180, 300)], '14b')
sol14c = [(x, y) for x in (0, 180) for y in (60, 120)] + [(y, x) for x in (0, 180) for y in (60, 120)]
cksys([lambda x, y: sin(x) + sin(y) - S3 / 2, lambda x, y: sin(x) ** 2 + sin(y) ** 2 - .75], sol14c, '14c')
cksys([lambda x, y: x + y - 90, lambda x, y: S3 * cos(x) - cos(y) - 1], [(30, 60)], '14d')
sol14e = [(x, y) for x in range(360) for y in range(360) if abs(sin(x) * cos(y) - .25) < 1e-9 and abs(cos(x) * sin(y) - .25) < 1e-9]
assert sorted(sol14e) == sorted([(15, 15), (75, 75), (105, 285), (165, 345), (195, 195), (255, 255), (285, 105), (345, 165)]), sol14e
cksys([lambda x, y: sin(x) * cos(y) - .25, lambda x, y: cos(x) * sin(y) - .25], sol14e, '14e')
def pairs(l): return ', '.join(r'$\res{(%d^\circ,%d^\circ)}$' % p for p in sorted(l))
# 15 (radians, en [0, 2π))
for x, y in ((0, 90), (90, 0)): ck(sin(x) + sin(y), 1)
for x, y in ((90, 30), (270, 210)): ck(sin(x), 2 * sin(y)); ck(x - y, 60)
for x, y in ((30, S3), (210, S3), (120, -S3), (300, -S3)): ck(4 * y * sin(x) * cos(x), 3); ck(2 * y * cos(2 * x), S3)
S.append(("Sistemas de ecuaciones trigonométricas", [
 (2, r"Resuelve los sistemas de ecuaciones siguientes en el intervalo $[0^\circ,360^\circ)$:" + tasks(2, ['$%s$' % sist(r'\cos y-\sin x=1', r'4\sin x\cos y+1=0'), '$%s$' % sist(r'\cos x+\cos y=-\frac12', r'\cos x\cos y=-\frac12'),
                                                                                                   '$%s$' % sist(r'\sin x+\sin y=\frac{\sqrt3}{2}', r'\sin^2x+\sin^2y=\frac34'), '$%s$' % sist(r'x+y=\frac{\pi}{2}', r'\sqrt3\cos x-\cos y=1'),
                                                                                                   '$%s$' % sist(r'\sin x\cdot\cos y=\frac14', r'\cos x\cdot\sin y=\frac14')]),
     tasks(1, [r'$\cos y=1+\sin x\Rightarrow(2\sin x+1)^2=0$: $\sin x=-\frac12$, $\cos y=\frac12$: ' + pairs([(210, 60), (210, 300), (330, 60), (330, 300)]),
               r'$\cos x$ y $\cos y$ son las raíces de $t^2+\frac12t-\frac12=0$: $\frac12$ y $-1$: ' + pairs([(60, 180), (300, 180), (180, 60), (180, 300)]),
               r'$\sin x\sin y=\frac{(\sin x+\sin y)^2-(\sin^2x+\sin^2y)}{2}=0$: un seno vale 0 y el otro $\frac{\sqrt3}{2}$: ' + pairs(sol14c),
               r'$\cos y=\sin x\Rightarrow\sqrt3\cos x-\sin x=1\Rightarrow\cos(x+30^\circ)=\frac12$: $\res{x=\frac{\pi}{6},\ y=\frac{\pi}{3}}$ (con $x=\frac{3\pi}{2}$, $y=-\pi$ quedaría fuera del intervalo)',
               r'Sumando y restando: $\sin(x+y)=\frac12$, $\sin(x-y)=0$: ' + pairs(sol14e)])),
 (3, r"Resuelve los sistemas de ecuaciones siguientes, con $x,y\in[0,2\pi)$ en los dos primeros:" + tasks(3, ['$%s$' % sist(r'\sin x+\sin y=1', r'2x+2y=\pi'), '$%s$' % sist(r'\sin x=2\sin y', r'x-y=\frac{\pi}{3}'), '$%s$' % sist(r'4y\sin x\cos x=3', r'2y\cos2x=\sqrt3')]),
     tasks(1, [r'$y=\frac\pi2-x\Rightarrow\sin x+\cos x=1$: $\res{(0,\tfrac\pi2)}$ y $\res{(\tfrac\pi2,0)}$',
               r'$\sin\left(y+\frac\pi3\right)=2\sin y\Rightarrow\text{tg}\,y=\frac{\sqrt3}{3}$: $\res{y=\frac\pi6,\ x=\frac\pi2}$ y $\res{y=\frac{7\pi}{6},\ x=\frac{3\pi}{2}}$',
               r'$2y\sin2x=3$ y $2y\cos2x=\sqrt3$: dividiendo, $\text{tg}\,2x=\sqrt3$; sumando los cuadrados, $4y^2=12$. En $[0,2\pi)$: $\res{x=\frac\pi6,\frac{7\pi}{6}\ \text{con}\ y=\sqrt3}$ y $\res{x=\frac{2\pi}{3},\frac{5\pi}{3}\ \text{con}\ y=-\sqrt3}$'])),
]))

# =====================================================================
# 12. Funcions trigonomètriques (Trigonometria 2, exercicis 16-19)
FUN = {'a': ('2\\cos x', lambda x: 2 * math.cos(x), '2*cos(\\x r)'), 'b': ('\\cos2x', lambda x: math.cos(2 * x), 'cos(2*\\x r)'), 'c': ('\\frac12\\sin x', lambda x: .5 * math.sin(x), '0.5*sin(\\x r)'),
       'd': ('\\cos\\frac x2', lambda x: math.cos(x / 2), 'cos(\\x/2 r)'), 'e': ('\\sin2x', lambda x: math.sin(2 * x), 'sin(2*\\x r)'), 'f': ('2\\sin x', lambda x: 2 * math.sin(x), '2*sin(\\x r)'),
       'g': ('\\frac12\\cos x', lambda x: .5 * math.cos(x), '0.5*cos(\\x r)'), 'h': ('\\sin\\frac x2', lambda x: math.sin(x / 2), 'sin(\\x/2 r)')}
ORDER = ['f', 'd', 'a', 'h', 'g', 'e', 'b', 'c']   # gràfica número i -> funció
def gplot(i, key):
    o = [r'\begin{tikzpicture}[x=0.36cm,y=0.42cm]',
         r'\draw[muted!25,very thin] (-3.1416,-2.4) grid[xstep=1.5708,ystep=1] (12.566,2.4);',
         r'\draw[-latex,muted] (-3.4,0)--(13,0); \draw[-latex,muted] (0,-2.5)--(0,2.6);',
         r'\foreach \k/\l in {-1/-\pi,1/\pi,2/2\pi,3/3\pi,4/4\pi}{\draw[muted] (\k*3.1416,0.1)--(\k*3.1416,-0.1) node[below,font=\tiny,text=muted]{$\l$};}',
         r'\foreach \v in {-2,-1,1,2}{\draw[muted] (0.1,\v)--(-0.1,\v) node[left,font=\tiny,text=muted]{$\v$};}',
         r'\draw[navy,thick,domain=-3.1416:12.566,samples=180,smooth] plot (\x,{%s});' % FUN[key][2],
         r'\node[font=\small\bfseries,fill=white,inner sep=1pt] at (-2.4,2.0) {(%d)};' % i, r'\end{tikzpicture}']
    return '\n'.join(o)
# cada gràfica s'ha de poder distingir: comprovem que les vuit funcions són diferents en algun punt
for i, k1 in enumerate(ORDER):
    for k2 in ORDER[i + 1:]: assert max(abs(FUN[k1][1](x / 10) - FUN[k2][1](x / 10)) for x in range(-31, 126)) > .3
graphs = '\n\n\\begin{center}' + '\\\\[4pt]\n'.join(gplot(2 * j + 1, ORDER[2 * j]) + '\\hspace{0.6cm}' + gplot(2 * j + 2, ORDER[2 * j + 1]) for j in range(4)) + '\\end{center}\n'
match = [r'%s) $y=%s$ $\to$ \res{(%d)}' % (k, FUN[k][0], ORDER.index(k) + 1) for k in 'abcdefgh']
S.append(("Funciones trigonométricas", [
 (1, r"¿Verdadero o falso?" + tasks(1, ["Las funciones trigonométricas son periódicas.", r"Las funciones $\sin$ y $\cos$ tienen un período de $2\pi$.", r"La función $\text{tg}\,x$ tiene período $\pi$.", r"La función $\cos x$ es como $\sin x$ desplazada $\frac{\pi}{2}$ a la izquierda."]),
     tasks(4, [r'\rest{V}', r'\rest{V}', r'\rest{V}', r'\rest{V} ($\cos x=\sin(x+\frac\pi2)$)'])),
 (1, r"¿En qué puntos del intervalo $[0,4\pi]$ corta al eje $X$ cada una de las funciones siguientes?" + tasks(3, [r'$y=\cos\frac x2$', r'$y=\sin(x-\pi)$', r'$y=\cos(x+\pi)$']),
     tasks(1, [r'$\frac x2=\frac\pi2+k\pi$: $\res{x=\pi,\ 3\pi}$', r'$x-\pi=k\pi$: $\res{x=0,\ \pi,\ 2\pi,\ 3\pi,\ 4\pi}$', r'$x+\pi=\frac\pi2+k\pi$: $\res{x=\frac\pi2,\ \frac{3\pi}2,\ \frac{5\pi}2,\ \frac{7\pi}2}$'])),
 (2, r"¿Qué relación hay entre las gráficas de $y=\sin x$ e $y=\cos x$ y la de cada una de las funciones siguientes?" + tasks(4, [r'$y=\sin\left(x+\frac\pi2\right)$', r'$y=\cos\left(x+\frac\pi2\right)$', r'$y=\sin\left(\frac\pi2-x\right)$', r'$y=\cos\left(\frac\pi2-x\right)$']),
     tasks(2, [r'$=\cos x$: \rest{la gráfica del coseno}', r'$=-\sin x$: \rest{la del seno reflejada en el eje $X$}', r'$=\cos x$: \rest{la gráfica del coseno}', r'$=\sin x$: \rest{la gráfica del seno}'])),
 (2, r"Asocia a cada una de las funciones siguientes la gráfica que le corresponde:" + tasks(4, [r'$y=%s$' % FUN[k][0] for k in 'abcdefgh']) + graphs,
     tasks(4, match) + r'Fíjate en la amplitud (el valor máximo) y en el período: $2\pi$, $\pi$ (si hay $2x$) o $4\pi$ (si hay $\frac x2$).'),
]))
for x in (0.3, 1.7, 4): ck(math.sin(x + PI / 2), math.cos(x)); ck(math.cos(x + PI / 2), -math.sin(x)); ck(math.sin(PI / 2 - x), math.cos(x)); ck(math.cos(PI / 2 - x), math.sin(x))

# =====================================================================
# 13. Ampliació (exercicis nous)
l61, A61 = 12 * 5 * PI / 6, .5 * 144 * 5 * PI / 6
ck(math.sqrt(3) / 2 * S2 / 2 + S3 / 3, sin(120) * cos(315) + tan(210))
B64 = asin(8 * sin(40) / 6); sols64 = []
for Bx in (B64, 180 - B64):
    Cx = 180 - 40 - Bx; sols64.append((Bx, Cx, 6 * sin(Cx) / sin(40)))
A65, B65, C65 = SSS(13, 14, 15); ck(.5 * 14 * 15 * sin(A65), 84)
d66 = math.sqrt(27 ** 2 + 36 ** 2 - 2 * 27 * 36 * cos(70))
x67 = 20 * tan(22) / (tan(35) - tan(22)); h67 = x67 * tan(35)
side68, area68 = 20 * sin(36), 5 * .5 * 100 * sin(72)
# 69: tg α = 2 (3r quadrant), cos β = -3/5 (2n quadrant)
sa69, ca69, sb69, cb69 = -2 / S5, -1 / S5, 4 / 5, -3 / 5
a69 = 180 + atan(2); b69 = 180 - acos(3 / 5)
ck(sin(a69), sa69); ck(cos(a69), ca69); ck(sin(b69), sb69); ck(cos(b69), cb69)
ck(sin(a69 + b69), 2 * S5 / 25); ck(cos(a69 - b69), -S5 / 5); ck(tan(a69 + b69), 2 / 11); ck(sin(2 * a69), .8)
S.append(("Ampliación y problemas (ejercicios nuevos)", [
 (1, r"El minutero de un reloj mide 12 cm. ¿Qué distancia recorre la punta en 25 minutos? ¿Qué área barre el minutero? (El área de un sector circular de ángulo $\alpha$ radianes es $\frac12r^2\alpha$.)",
     r'25 min $=150^\circ=\frac{5\pi}{6}$ rad: $l=12\cdot\frac{5\pi}{6}=\res{10\pi\approx%s\ \text{cm}}$; \ $S=\frac12\cdot144\cdot\frac{5\pi}{6}=\res{60\pi\approx%s\ \text{cm}^2}$' % (dec(l61), dec(A61))),
 (1, r"Calcula de manera exacta, sin calculadora: \ $\sin120^\circ\cdot\cos315^\circ+\text{tg}\,210^\circ$ \ y \ $\dfrac{\cos\frac{5\pi}{3}-\sin\frac{7\pi}{6}}{\text{tg}\,\frac{3\pi}{4}}$.",
     r'$\frac{\sqrt3}{2}\cdot\frac{\sqrt2}{2}+\frac{\sqrt3}{3}=\res{\frac{\sqrt6}{4}+\frac{\sqrt3}{3}}$; \quad $\dfrac{\frac12+\frac12}{-1}=\res{-1}$'),
 (2, r"Simplifica las expresiones: \ $\sin(\pi-x)+\cos\left(\frac\pi2+x\right)+\sin(-x)$ \ y \ $\dfrac{\cos(\pi+x)\cdot\text{tg}\,(\pi-x)}{\sin(2\pi-x)}$.",
     r'$\sin x-\sin x-\sin x=\res{-\sin x}$; \quad $\dfrac{(-\cos x)(-\text{tg}\,x)}{-\sin x}=\dfrac{\sin x}{-\sin x}=\res{-1}$'),
 (2, r"Resuelve el triángulo con $a=6$ cm, $b=8$ cm y $\hat A=40^\circ$. ¿Cuántas soluciones hay?",
     r'$\sin\hat B=\frac{8\sin40^\circ}{6}\approx%s$: \rest{dos soluciones}. \ $\hat B_1\approx\res{%s}$, $\hat C_1\approx%s$, $c_1\approx\res{%s}$ cm; \ $\hat B_2\approx\res{%s}$, $\hat C_2\approx%s$, $c_2\approx\res{%s}$ cm.' % (
         dec(8 * sin(40) / 6, 4), dms(sols64[0][0]), dms(sols64[0][1]), dec(sols64[0][2]), dms(sols64[1][0]), dms(sols64[1][1]), dec(sols64[1][2]))),
 (2, r"Un triángulo tiene lados de 13, 14 y 15 cm. Calcula sus ángulos y su área de dos maneras: con $S=\frac12bc\sin\hat A$ y con la fórmula de Herón.",
     r'$\hat A\approx\res{%s}$, $\hat B\approx\res{%s}$, $\hat C\approx\res{%s}$. \ $p=21$, $S=\sqrt{21\cdot8\cdot7\cdot6}=\res{84\ \text{cm}^2}$' % (dms(A65), dms(B65), dms(C65))),
 (2, r"Dos barcos salen a la vez de un puerto con rumbos que forman un ángulo de $70^\circ$, a 18 km/h y a 24 km/h. ¿A qué distancia están al cabo de una hora y media?",
     r'Han recorrido 27 y 36 km: $d=\sqrt{27^2+36^2-2\cdot27\cdot36\cos70^\circ}\approx\res{%s\ \text{km}}$' % dec(d66)),
 (2, r"Desde la orilla de un río vemos la copa de un árbol de la otra orilla con un ángulo de elevación de $35^\circ$. Si nos alejamos 20 m del río, perpendicularmente a la orilla, el ángulo es de $22^\circ$. Calcula la altura del árbol y la anchura del río.",
     r'$h=x\,\text{tg}\,35^\circ=(x+20)\,\text{tg}\,22^\circ\Rightarrow$ anchura $x\approx\res{%s\ \text{m}}$, altura $h\approx\res{%s\ \text{m}}$' % (dec(x67), dec(h67))),
 (2, r"Calcula el lado y el área de un pentágono regular inscrito en una circunferencia de 10 cm de radio.",
     r'Cada triángulo central tiene un ángulo de $72^\circ$: lado $=2\cdot10\sin36^\circ\approx\res{%s\ \text{cm}}$; área $=5\cdot\frac12\cdot10^2\sin72^\circ\approx\res{%s\ \text{cm}^2}$' % (dec(side68), dec(area68))),
 (3, r"Si $\text{tg}\,\alpha=2$ con $180^\circ<\alpha<270^\circ$ y $\cos\beta=-\frac35$ con $90^\circ<\beta<180^\circ$, calcula de manera exacta $\sin(\alpha+\beta)$, $\cos(\alpha-\beta)$, $\text{tg}\,(\alpha+\beta)$ y $\sin2\alpha$.",
     r'$\sin\alpha=-\frac{2\sqrt5}{5}$, $\cos\alpha=-\frac{\sqrt5}{5}$, $\sin\beta=\frac45$, $\text{tg}\,\beta=-\frac43$. \ $\sin(\alpha+\beta)=\res{\frac{2\sqrt5}{25}}$, $\cos(\alpha-\beta)=\res{-\frac{\sqrt5}{5}}$, $\text{tg}\,(\alpha+\beta)=\res{\frac{2}{11}}$, $\sin2\alpha=\res{\frac45}$'),
 (2, r"Demuestra que $\cos^4\alpha-\sin^4\alpha=\cos2\alpha$ y que $\dfrac{1-\cos2\alpha}{\sin2\alpha}=\text{tg}\,\alpha$.",
     r'$(\cos^2\alpha+\sin^2\alpha)(\cos^2\alpha-\sin^2\alpha)=1\cdot\cos2\alpha$; \quad $\dfrac{2\sin^2\alpha}{2\sin\alpha\cos\alpha}=\text{tg}\,\alpha$'),
 (2, r"Resuelve en $[0^\circ,360^\circ)$: \ $2\sin^2x+3\cos x=3$.", r'$2\cos^2x-3\cos x+1=0\Rightarrow\cos x=1$ o $\frac12$: $\res{0^\circ,\ 60^\circ,\ 300^\circ}$'),
 (2, r"Resuelve en $[0^\circ,360^\circ)$: \ $\sin2x=\cos x$.", r'$\cos x(2\sin x-1)=0$: $\res{30^\circ,\ 90^\circ,\ 150^\circ,\ 270^\circ}$'),
 (2, r"Para la función $y=2\sin\left(2x-\frac\pi2\right)+1$, indica la amplitud, el período, el recorrido y el desplazamiento respecto de $y=2\sin2x+1$. ¿En qué puntos de $[0,\pi]$ alcanza el máximo?",
     r'Amplitud $\res{2}$, período $\res{\pi}$, recorrido $\res{[-1,3]}$, desplazada $\res{\frac\pi4}$ hacia la derecha. Máximo ($y=3$) cuando $2x-\frac\pi2=\frac\pi2$: $\res{x=\frac\pi2}$'),
]))
ckeq(lambda x: 2 * sin(x) ** 2 + 3 * cos(x) - 3, [0, 60, 300]); ckeq(lambda x: sin(2 * x) - cos(x), [30, 90, 150, 270])
for a in (20, 110, 250): ck(cos(a) ** 4 - sin(a) ** 4, cos(2 * a)); ck((1 - cos(2 * a)) / sin(2 * a), tan(a))
for x in (.3, 2): ck(math.sin(PI - x) + math.cos(PI / 2 + x) + math.sin(-x), -math.sin(x)); ck(math.cos(PI + x) * math.tan(PI - x) / math.sin(2 * PI - x), -1)
ck((math.cos(5 * PI / 3) - math.sin(7 * PI / 6)) / math.tan(3 * PI / 4), -1)
ck(max(2 * math.sin(2 * x / 1000 - PI / 2) + 1 for x in range(0, 3142)), 3, 1e-6); ck(2 * math.sin(2 * PI / 2 - PI / 2) + 1, 3)

assert all(CHK)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "trigonometría, radianes, razones trigonométricas, circunferencia goniométrica, resolución de triángulos, teorema del seno, teorema del coseno, fórmulas trigonométricas, ecuaciones trigonométricas, funciones trigonométricas"
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'''\usetikzlibrary{calc}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

TIT = "Trigonometría"
def build(sol):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 5: %s' % (t, TIT), capcalera='%s · Unidad 5: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-mi')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-mi}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1batx-mi') + '{' + ('Soluciones de la ficha · Unidad 5' if sol else 'Ficha de ejercicios · Unidad 5') + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.8cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Los resultados se dan de manera exacta cuando es posible y, si no, con dos decimales; los ángulos, en grados, minutos y segundos. Puedes comprobar los triángulos, las razones y las ecuaciones con las herramientas de los apuntes interactivos de la unidad."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos y haz un dibujo siempre que te ayude. Comprueba el modo de la calculadora (grados o radianes) y, en las ecuaciones, comprueba siempre las soluciones. Los ejercicios 1--41 son los de la ficha «Trigonometría 1» del departamento y los 42--60, los de «Trigonometría 2», en el mismo orden; la sección 13 tiene otros nuevos para ampliar y aplicar lo que has aprendido.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't5-fitxa-solucions-es.tex' if sol else 't5-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S), 'ejercicios;', len(CHK), 'comprobaciones')
