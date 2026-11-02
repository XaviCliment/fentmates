# Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex
# (1r ESO, Unitat 9: Gràfics de funcions — coordenades cartesianes, aplicacions, taules i gràfics,
# interpretació de gràfics, funcions de proporcionalitat directa i funcions lineals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les comprovacions CHK (amb fraccions exactes) verifiquen cada resultat escrit.
import os, re, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def center(t): return r'\par\smallskip\begin{center}' + t + r'\end{center}'
def side(*figs):
    return r'\par\smallskip\begin{center}' + r'\hspace{0.8cm}'.join(figs) + r'\end{center}'

# ---------- comprovacions ----------
NCHK = [0]
def CHK(cond, *info):
    NCHK[0] += 1
    assert cond, info
def fr(v): return v if isinstance(v, Fr) else Fr(str(v).replace('{,}', '.').replace(',', '.'))
def lin(m, n=0):
    m, n = fr(m), fr(n)
    return lambda x: m * fr(x) + n
def at(P, x):
    for (a, ya), (b, yb) in zip(P, P[1:]):
        if a <= x <= b: return fr(ya) + (fr(yb) - fr(ya)) * (fr(x) - fr(a)) / (fr(b) - fr(a))
    raise ValueError(x)
def quad(x, y):
    if x == 0 and y == 0: return 'O'
    if y == 0: return 'X'
    if x == 0: return 'Y'
    return 'I' if x > 0 and y > 0 else 'II' if x < 0 < y else 'III' if x < 0 and y < 0 else 'IV'
QT = {'I': 'quadrant I', 'II': 'quadrant II', 'III': 'quadrant III', 'IV': 'quadrant IV', 'X': 'eix $X$', 'Y': 'eix $Y$'}

# ---------- nombres i taules ----------
def tn(v):
    v = fr(v)
    if v.denominator == 1: return str(v.numerator)
    t = ('%.6f' % float(v)).rstrip('0').rstrip('.')
    CHK(fr(t) == v, v)
    return t.replace('.', '{,}')
def pt(x, y):
    a, b = tn(x), tn(y)
    return '(%s;\\ %s)' % (a, b) if '{,}' in a + b else '(%s,\\ %s)' % (a, b)
def lab(t):
    """etiqueta d'una taula (dins de $...$): text normal o fórmula entre $"""
    return t[1:-1] if t.startswith('$') and t.endswith('$') else t if t in ('x', 'y') else r'\text{%s}' % t
def tv(xs, ys, xl='x', yl='y'):
    xl, yl = lab(xl), lab(yl)
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('c' * len(xs), xl, '&'.join(tn(a) if not isinstance(a, str) else a for a in xs), yl, '&'.join(tn(a) if not isinstance(a, str) else a for a in ys)))
def tvb(xs, xl='x', yl='y'):
    xl, yl = lab(xl), lab(yl)
    return (r'$\begin{array}{|c|%s|}\hline %s&%s\\\hline %s&%s\\\hline\end{array}$'
            % ('C{0.75cm}' * len(xs), xl, '&'.join(tn(a) for a in xs), yl, '&'.join([r'\phantom{00}'] * len(xs))))
def eq(m, n=0, v='x'):
    m, n = fr(m), fr(n)
    if m == 0: return 'y=' + tn(n)
    s = v if m == 1 else '-' + v if m == -1 else tn(m) + v
    if n: s += ('+' if n > 0 else '-') + tn(abs(n))
    return 'y=' + s

# ---------- pla cartesià (TikZ) ----------
COL = {'p0': 'accent', 'p1': 'teal', 'p2': 'navy'}
def tp(win, pts=(), polys=(), fns=(), curves=(), proj=(), labs=(), u=0.42, uy=None, xs=1, ys=1, gx=None, gy=None, xl='x', yl='y'):
    """win = (x0, x1, y0, y1); pts: (x, y, etiqueta, color[, posició]); polys: (vèrtexs, color); fns: (m, n, color[, a, b]);
    curves: (punts, color); proj: (x, y) línies de projecció; labs: (x, y, text, posició)"""
    x0, x1, y0, y1 = [float(v) for v in win]
    uy = uy or u; gx = gx or xs; gy = gy or ys
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center),line cap=round,line join=round]' % (u, uy)]
    k = math.ceil(x0 / gx - 1e-9)
    while k * gx <= x1 + 1e-9: o.append(r'\draw[muted!30,line width=0.3pt] (%g,%g)--(%g,%g);' % (k * gx, y0, k * gx, y1)); k += 1
    k = math.ceil(y0 / gy - 1e-9)
    while k * gy <= y1 + 1e-9: o.append(r'\draw[muted!30,line width=0.3pt] (%g,%g)--(%g,%g);' % (x0, k * gy, x1, k * gy)); k += 1
    ax = min(max(0, y0), y1); ay = min(max(0, x0), x1)
    o.append(r'\draw[-latex,muted,line width=0.6pt] (%g,%g)--(%g,%g) node[right,font=\scriptsize,text=navy]{%s};' % (x0, ax, x1 + 0.3 * gx, ax, xl))
    o.append(r'\draw[-latex,muted,line width=0.6pt] (%g,%g)--(%g,%g) node[above,font=\scriptsize,text=navy]{%s};' % (ay, y0, ay, y1 + 0.3 * gy, yl))
    k = math.ceil(x0 / xs - 1e-9)
    while k * xs < x1 - 1e-9:
        v = k * xs
        if abs(v) > 1e-9 and v > x0 + 1e-9: o.append(r'\node[font=\tiny,text=muted,below,inner sep=1.5pt] at (%g,%g) {$%s$};' % (v, ax, tn(Fr(v).limit_denominator(100))))
        k += 1
    k = math.ceil(y0 / ys - 1e-9)
    while k * ys < y1 - 1e-9:
        v = k * ys
        if abs(v) > 1e-9 and v > y0 + 1e-9: o.append(r'\node[font=\tiny,text=muted,left,inner sep=1.5pt] at (%g,%g) {$%s$};' % (ay, v, tn(Fr(v).limit_denominator(100))))
        k += 1
    o.append(r'\node[font=\tiny,text=muted,below left,inner sep=1.5pt] at (%g,%g) {$0$};' % (ay, ax))
    for V, c in polys:
        o.append(r'\draw[%s,thick,fill=%s!15] %s--cycle;' % (c, c, '--'.join('(%g,%g)' % (float(p[0]), float(p[1])) for p in V)))
    for f in fns:
        m, n, c = float(fr(f[0])), float(fr(f[1])), f[2]
        lo = float(f[3]) if len(f) > 3 and f[3] is not None else x0
        hi = float(f[4]) if len(f) > 4 and f[4] is not None else x1
        if m != 0:
            xa, xb = (y0 - n) / m, (y1 - n) / m
            lo, hi = max(lo, min(xa, xb)), min(hi, max(xa, xb))
        if lo < hi: o.append(r'\draw[%s,line width=1.1pt] (%.3f,%.3f)--(%.3f,%.3f);' % (c, lo, m * lo + n, hi, m * hi + n))
    for P, c in curves:
        o.append(r'\draw[%s,line width=1.1pt] %s;' % (c, '--'.join('(%g,%g)' % (float(p[0]), float(p[1])) for p in P)))
    for px, py in proj:
        o.append(r'\draw[accent,dashed,thin] (%g,%g)--(%g,%g)--(%g,%g);' % (float(px), ax, float(px), float(py), ay, float(py)))
    for p in pts:
        px, py, lab, c = (tuple(p) + (None, 'p2'))[:4]
        pos = p[4] if len(p) > 4 else 'above right'
        o.append(r'\fill[%s] (%g,%g) circle (2.2pt)%s;' % (COL.get(c, c), float(px), float(py), (r' node[%s,font=\scriptsize,inner sep=1.5pt]{%s}' % (pos, lab)) if lab else ''))
    for px, py, t, pos in labs:
        o.append(r'\node[font=\scriptsize,%s] at (%g,%g) {%s};' % (pos, float(px), float(py), t))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]
W5 = (-5, 5, -5, 5)

# =====================================================================
# 1. El pla cartesià. Coordenades d'un punt
# =====================================================================
P11 = [('A', 2, 3), ('B', -4, 1), ('C', -3, -2), ('D', 3, -4), ('E', 0, 2), ('F', 4, 0), ('G', -1, 4), ('H', -2, 0)]
F11 = tp(W5, pts=[(x, y, '$%s$' % n, 'p2') for n, x, y in P11])
P12 = [('P', 3, 1), ('Q', -2, 4), ('R', -4, -3), ('S', 1, -2), ('T', 0, -4), ('U', 5, 0)]
F12 = tp((-5, 6, -5, 5), pts=[(x, y, '$%s$' % n, 'p2') for n, x, y in P12])
Q13 = [(6, -2), (-3, -8), (-1, 7), (0, -5), (9, 0), (4, 4), (-6, 0), (-2, -2)]
F15 = tp(W5, pts=[(-2, 4, '$(-2,\\,4)$', 'p0'), (4, -2, '$(4,\\,-2)$', 'p1', 'below left')], u=0.38)
CHK(quad(-2, 4) == 'II' and quad(4, -2) == 'IV')
F18 = tp(W5, pts=[(k, k, None, 'p0') for k in range(-4, 5)] + [(k, 2, None, 'p1') for k in range(-4, 5)], fns=[(1, 0, 'accent!60'), (0, 2, 'teal!60')], u=0.38,
         labs=[(4.3, 4.6, '$y=x$', 'right'), (4.3, 2, '$y=2$', 'right')])
SQ = [(-3, -2), (1, -2), (1, 2), (-3, 2)]
F19 = tp(W5, polys=[(SQ, 'accent')], pts=[(-3, -2, '$A$', 'p2', 'below left'), (1, -2, '$B$', 'p2', 'below right'), (1, 2, '$C$', 'p2', 'above right'), (-3, 2, '$D$', 'p2', 'above left'), (-1, 0, '$M$', 'p1', 'above')], u=0.38)
CHK(SQ[1][0] - SQ[0][0] == SQ[2][1] - SQ[1][1] == 4 and ((-3 + 1) / 2, (-2 + 2) / 2) == (-1, 0))
S_.append(("El pla cartesià. Coordenades d'un punt", [
 (1, r"Escriu les coordenades dels punts del dibuix:" + center(F11)
     + recorda(r"Les coordenades d'un punt s'escriuen $P(x,\ y)$: primer l'\textbf{abscissa} $x$ (horitzontal: dreta $+$, esquerra $-$) i després l'\textbf{ordenada} $y$ (vertical: amunt $+$, avall $-$)."),
     tasks(4, ['$%s%s$' % (n, ('\\res{' + pt(x, y) + '}')) for n, x, y in P11])),
 (1, r"Dibuixa en uns eixos de coordenades els punts $P(3,\ 1)$, $Q(-2,\ 4)$, $R(-4,\ -3)$, $S(1,\ -2)$, $T(0,\ -4)$ i $U(5,\ 0)$.",
     center(F12)),
 (1, r"Sense dibuixar-los, digues en quin quadrant o sobre quin eix està cada punt:" + tasks(4, ['$' + pt(x, y) + '$' for x, y in Q13])
     + recorda(r"Signes: quadrant I $(+,\,+)$, II $(-,\,+)$, III $(-,\,-)$, IV $(+,\,-)$. Si $y=0$, el punt és de l'eix $X$; si $x=0$, de l'eix $Y$."),
     tasks(4, [r'\rest{%s}' % QT[quad(x, y)] for x, y in Q13])),
 (1, r"Escriu les coordenades del punt:" + tasks(1, [r"que està 3 unitats a la dreta de l'eix $Y$ i 5 per damunt de l'eix $X$;", r"que està 2 unitats a l'esquerra de l'eix $Y$ i 4 per davall de l'eix $X$;",
                                                   r"que està sobre l'eix $X$, 6 unitats a l'esquerra de l'origen;", r"que està sobre l'eix $Y$, 1 unitat per damunt de l'origen."]),
     tasks(4, [r'$\res{(3,\ 5)}$', r'$\res{(-2,\ -4)}$', r'$\res{(-6,\ 0)}$', r'$\res{(0,\ 1)}$'])),
 (2, r"Dibuixa els punts $(-2,\ 4)$ i $(4,\ -2)$. Són el mateix punt? En quin quadrant està cadascun?",
     r"\rest{No}: l'ordre de les coordenades importa. $(-2,\ 4)$ està en el \rest{quadrant II} i $(4,\ -2)$, en el \rest{quadrant IV}." + center(F15)),
 (2, r"Respon:" + tasks(1, [r"Quin punt del quadrant II està a 4 unitats de cada eix?", r"Quins punts de l'eix $X$ estan a 3 unitats de l'origen?", r"Quin punt del quadrant III té l'abscissa $-5$ i l'ordenada la meitat de l'abscissa?"]),
     tasks(1, [r"En el II, $x<0$ i $y>0$: \ $\res{(-4,\ 4)}$", r"$\res{(3,\ 0)}$ i $\res{(-3,\ 0)}$", r"$y=-5:2=-2{,}5$: \ $\res{(-5;\ -2{,}5)}$"])),
 (2, r"El punt $(a,\ b)$ està en el quadrant IV. En quin quadrant estan els punts $(-a,\ b)$, \ $(a,\ -b)$ \ i \ $(b,\ a)$?",
     r"En el IV, $a>0$ i $b<0$. \ $(-a,\ b)$: $(-,\ -)$, \rest{quadrant III}. \ $(a,\ -b)$: $(+,\ +)$, \rest{quadrant I}. \ $(b,\ a)$: $(-,\ +)$, \rest{quadrant II}."),
 (3, r"Dibuixa tots els punts de coordenades enteres entre $-4$ i $4$ que tenen l'ordenada igual a l'abscissa. Fes el mateix amb els que tenen l'ordenada igual a 2. Què observes?",
     r"Els primers estan alineats en una recta inclinada que passa per l'origen (\rest{$y=x$}); els segons, en una recta \rest{horitzontal} (\rest{$y=2$})." + center(F18)),
 (3, r"Dibuixa els punts $A(-3,\ -2)$, $B(1,\ -2)$ i $C(1,\ 2)$. Troba el punt $D$ perquè $ABCD$ siga un quadrat i calcula les coordenades del centre del quadrat.",
     r"El costat fa 4: \ $D=\res{(-3,\ 2)}$. El centre està a la meitat de la diagonal: \ $M=\res{(-1,\ 0)}$." + center(F19)),
]))

# =====================================================================
# 2. Aplicacions de les coordenades
# =====================================================================
MAPA = [('E', 2, 3, 'escola'), ('P', -3, 2, 'parc'), ('H', 4, -2, 'hospital'), ('M', -2, -3, 'mercat'), ('B', 0, -1, 'biblioteca'), ('C', -4, 0, 'camp de futbol')]
F21 = tp(W5, pts=[(x, y, r'\textbf{%s}' % n, 'p0') for n, x, y, _ in MAPA], labs=[(0.25, 0.25, r'\faFlag', 'above right,text=muted')])
RV = [(1, 1), (6, 1), (6, 4), (1, 4)]
CHK(2 * 5 + 2 * 3 == 16 and 5 * 3 == 15)
F22 = tp((-1, 7, -1, 5), polys=[(RV, 'accent')], pts=[(1, 1, '$A$', 'p2', 'below left'), (6, 1, '$B$', 'p2', 'below right'), (6, 4, '$C$', 'p2', 'above right'), (1, 4, '$D$', 'p2', 'above left')], u=0.4)
D23 = [((-2, 3), (5, 3)), ((4, -1), (4, 6)), ((-6, -2), (-1, -2)), ((0, -4), (0, 3))]
R23 = [7, 7, 5, 7]
for (A, B), r in zip(D23, R23): CHK(abs(A[0] - B[0]) + abs(A[1] - B[1]) == r and (A[0] == B[0] or A[1] == B[1]))
ROB = [(0, 0), (4, 0), (4, 3), (-2, 3), (-2, -1), (1, -1)]
CHK(ROB[-1] == (4 - 6 + 3, 3 - 4))
F24 = tp(W5, curves=[(ROB, 'accent')], pts=[(0, 0, '$S$', 'p1', 'below right'), (1, -1, '$F$', 'p0', 'below')], u=0.36)
TR = [(-4, 1), (-1, 1), (-2, 4)]; TR2 = [(x + 5, y - 4) for x, y in TR]
CHK(TR2 == [(1, -3), (4, -3), (3, 0)])
F25 = tp(W5, polys=[(TR, 'accent'), (TR2, 'teal')], labs=[(-2.4, 2.1, '$T$', ''), (2.6, -1.9, "$T'$", '')], u=0.36)
P26 = [(3, 5), (-2, 4), (-1, -6), (5, -3)]
REC = [(-2, 1), (3, 1), (3, -2)]; D4 = (-2, -2)
CHK(5 * 3 == 15 and 2 * 5 + 2 * 3 == 16)
F27 = tp(W5, polys=[(REC + [D4], 'teal')], pts=[(-2, 1, '$A$', 'p2', 'above left'), (3, 1, '$B$', 'p2', 'above right'), (3, -2, '$C$', 'p2', 'below right'), (-2, -2, '$D$', 'p0', 'below left')], u=0.36)
TRI = [(-2, -1), (4, -1), (1, 3)]
CHK(Fr(6 * 4, 2) == 12)
F28 = tp((-3, 5, -2, 4), polys=[(TRI, 'accent')], proj=[], pts=[(-2, -1, '$A$', 'p2', 'below left'), (4, -1, '$B$', 'p2', 'below right'), (1, 3, '$C$', 'p2', 'above')], u=0.42)
CASA = [(0, 0), (4, 0), (4, 2), (2, 4), (0, 2)]
def shoelace(V): return abs(sum(V[i][0] * V[(i + 1) % len(V)][1] - V[(i + 1) % len(V)][0] * V[i][1] for i in range(len(V)))) / Fr(2)
CHK(shoelace(CASA) == 12 == 4 * 2 + Fr(4 * 2, 2) and shoelace(TRI) == 12 and shoelace(REC + [D4]) == 15)
F29 = tp((-1, 5, -1, 5), polys=[(CASA, 'accent')], curves=[([(0, 2), (4, 2)], 'muted')], u=0.42)
S_.append(("Aplicacions de les coordenades", [
 (1, r"En aquest plànol d'un poble, la bandera és la plaça (l'origen) i cada quadre és una illa de cases. Escriu les coordenades de l'escola ($E$), el parc ($P$), l'hospital ($H$) i el mercat ($M$). Què hi ha en $(0,\ -1)$? I en $(-4,\ 0)$?" + center(F21),
     r"$E\res{(2,\ 3)}$, \ $P\res{(-3,\ 2)}$, \ $H\res{(4,\ -2)}$, \ $M\res{(-2,\ -3)}$. \ En $(0,\ -1)$ hi ha la \rest{biblioteca} i en $(-4,\ 0)$, el \rest{camp de futbol}."),
 (1, r"Dibuixa el polígon de vèrtexs $A(1,\ 1)$, $B(6,\ 1)$, $C(6,\ 4)$ i $D(1,\ 4)$. Quin polígon és? Calcula'n el perímetre i l'àrea (la unitat és el cm)."
     + recorda(r"Si dos punts tenen la mateixa $y$, la distància entre ells és la diferència de les $x$; si tenen la mateixa $x$, la diferència de les $y$."),
     r"És un \rest{rectangle} de base $6-1=5$\,cm i altura $4-1=3$\,cm: \ $P=2\cdot5+2\cdot3=\res{16\text{ cm}}$, \ $A=5\cdot3=\res{15\text{ cm}^2}$." + center(F22)),
 (1, r"Calcula la distància entre els punts:" + tasks(2, [r"$(-2,\ 3)$ i $(5,\ 3)$", r"$(4,\ -1)$ i $(4,\ 6)$", r"$(-6,\ -2)$ i $(-1,\ -2)$", r"$(0,\ -4)$ i $(0,\ 3)$"]),
     tasks(2, [r"$5-(-2)=\res{7}$", r"$6-(-1)=\res{7}$", r"$-1-(-6)=\res{5}$", r"$3-(-4)=\res{7}$"])),
 (2, r"Un robot ix de l'origen i fa aquests moviments: 4 a la dreta, 3 amunt, 6 a l'esquerra, 4 avall i 3 a la dreta. On acaba? Dibuixa'n el camí.",
     r"$(0,\ 0)\to(4,\ 0)\to(4,\ 3)\to(-2,\ 3)\to(-2,\ -1)\to\res{(1,\ -1)}$" + center(F24)),
 (2, r"Desplaça el triangle de vèrtexs $(-4,\ 1)$, $(-1,\ 1)$ i $(-2,\ 4)$ 5 unitats a la dreta i 4 cap avall. Escriu els vèrtexs nous i dibuixa els dos triangles."
     + recorda(r"Desplaçar $a$ a la dreta i $b$ amunt: $(x,\ y)\to(x+a,\ y+b)$ (si va a l'esquerra o avall, restem)."),
     r"Sumem 5 a la $x$ i restem 4 a la $y$: \ $\res{(1,\ -3)}$, \ $\res{(4,\ -3)}$, \ $\res{(3,\ 0)}$." + center(F25)),
 (2, r"Completa la taula amb els simètrics de cada punt respecte dels eixos:" + center(r"\renewcommand{\arraystretch}{1.3}\begin{tabular}{|c|C{2.2cm}|C{2.2cm}|}\hline Punt & Simètric respecte de l'eix $X$ & Simètric respecte de l'eix $Y$\\\hline "
     + r'\\\hline '.join('$' + pt(x, y) + '$ & & ' for x, y in P26) + r'\\\hline\end{tabular}')
     + recorda(r"Respecte de l'eix $X$ canvia el signe de la $y$: $(x,\ -y)$. Respecte de l'eix $Y$ canvia el signe de la $x$: $(-x,\ y)$."),
     center(r'\renewcommand{\arraystretch}{1.25}\begin{tabular}{|c|c|c|}\hline Punt & Eix $X$ & Eix $Y$\\\hline ' + r'\\\hline '.join('$%s$ & $\\res{%s}$ & $\\res{%s}$' % (pt(x, y), pt(x, -y), pt(-x, y)) for x, y in P26) + r'\\\hline\end{tabular}')),
 (2, r"Tres vèrtexs d'un rectangle són $A(-2,\ 1)$, $B(3,\ 1)$ i $C(3,\ -2)$. Troba el quart vèrtex $D$ i calcula'n l'àrea i el perímetre.",
     r"$D=\res{(-2,\ -2)}$. Base $3-(-2)=5$, altura $1-(-2)=3$: \ $A=\res{15\text{ u}^2}$, \ $P=\res{16\text{ u}}$." + center(F27)),
 (3, r"Dibuixa el triangle de vèrtexs $A(-2,\ -1)$, $B(4,\ -1)$ i $C(1,\ 3)$ i calcula'n l'àrea.",
     r"La base $AB$ és horitzontal i fa $4-(-2)=6$. L'altura és la distància vertical de $C$ a la base: $3-(-1)=4$. \ $A=\dfrac{6\cdot4}{2}=\res{12\text{ u}^2}$" + center(F28)),
 (3, r"Dibuixa el pentàgon de vèrtexs $(0,\ 0)$, $(4,\ 0)$, $(4,\ 2)$, $(2,\ 4)$ i $(0,\ 2)$ i calcula'n l'àrea.",
     r"Té forma de caseta: un rectangle $4\times2$ i, damunt, un triangle de base 4 i altura 2. \ $A=8+\dfrac{4\cdot2}{2}=8+4=\res{12\text{ u}^2}$" + center(F29)),
]))

# =====================================================================
# 3. Relacions entre magnituds: taules i gràfics
# =====================================================================
PA = [1, 2, 3, 4, 5, 6]; PAv = [lin('0.4')(k) for k in PA]
CHK(PAv == [fr(v) for v in ('0.4', '0.8', '1.2', '1.6', '2', '2.4')])
F31 = tp((0, 6.6, 0, 2.7), pts=[(k, v, None, 'p0') for k, v in zip(PA, PAv)], u=0.62, uy=1.3, ys=0.4, xl='panets', yl='€')
F33 = tp((-1, 5, 0, 12.5), fns=[(2, 3, 'accent', 0, 4)], pts=[(k, 2 * k + 3, None, 'p2') for k in range(5)], u=0.5, uy=0.3, ys=2, gy=1)
H34 = [0, 3, 6, 9, 12, 15, 18, 21, 24]; T34 = [8, 6, 7, 12, 16, 18, 15, 11, 9]
F34 = tp((0, 25, 0, 20), curves=[(list(zip(H34, T34)), 'accent')], pts=[(h, t, None, 'p2') for h, t in zip(H34, T34)], u=0.26, uy=0.22, xs=3, ys=2, xl='h', yl=r'$^\circ$C')
T35 = [([1, 2, 3, 4], [5, 10, 15, 20]), ([1, 1, 2, 3], [4, 6, 8, 9]), ([0, 2, 4, 6], [3, 3, 3, 3])]
def isfun(T): return all(T[1][i] == T[1][j] for i in range(len(T[0])) for j in range(len(T[0])) if T[0][i] == T[0][j])
CHK([isfun(T) for T in T35] == [True, False, True])
T36a = ([0, 1, 2, 3], [5, 7, 9, 11]); T36b = ([1, 2, 3, 4], [10, 20, 30, 40]); T36c = ([0, 1, 2, 3], [9, 8, 7, 6])
for (X, Y), (m, n) in zip([T36a, T36b, T36c], [(2, 5), (10, 0), (-1, 9)]): CHK([lin(m, n)(x) for x in X] == Y)
MOB = lin(3, 10); CHK([MOB(k) for k in (0, 1, 2, 5, 10)] == [10, 13, 16, 25, 40])
F38 = tp((0, 5.5, 0, 26), pts=[(l, 4 * l, None, 'p0') for l in range(1, 6)] + [(l, l * l, None, 'p1') for l in range(1, 6)], curves=[([(l / 10, 4 * l / 10) for l in range(0, 53)], 'accent'), ([(l / 10, (l / 10) ** 2) for l in range(0, 51)], 'teal')],
         u=0.7, uy=0.15, ys=5, gy=5, xl='$l$', yl='', labs=[(5.3, 21, '$P$', 'right,text=accent'), (5, 25, '$A$', 'left,text=teal')])
CHK([4 * l for l in range(1, 6)] == [4, 8, 12, 16, 20] and [l * l for l in range(1, 6)] == [1, 4, 9, 16, 25])
F39 = tp((0, 10.5, 0, 10.5), pts=[(b, 10 - b, None, 'p0') for b in range(1, 10)], u=0.36, xs=1, ys=1, xl='base', yl='altura')
CHK(all(2 * b + 2 * (10 - b) == 20 for b in range(1, 10)))
S_.append(("Relacions entre magnituds: taules i gràfics", [
 (1, r"Un panet val 0,40\,€. Completa la taula, dibuixa el gràfic i digues si s'han d'unir els punts." + center(tvb(PA, 'Panets', 'Preu (€)'))
     + recorda(r"Cada parell $(x,\ y)$ de la taula és un punt del gràfic. Unim els punts només si també tenen sentit els valors intermedis."),
     center(tv(PA, PAv, 'Panets', 'Preu (€)')) + r"\rest{No} s'uneixen: no es pot comprar mig panet." + center(F31)),
 (1, r"Digues quina és la variable independent i quina la dependent:" + tasks(1, [r"el temps que està oberta una aixeta i els litres d'aigua que ixen;", r"el nombre de fotocòpies i el preu que paguem;", r"l'hora del dia i la temperatura;", r"els km que fa un cotxe i la gasolina que li queda."]),
     tasks(1, [r"independent: \rest{temps}; dependent: \rest{litres}", r"independent: \rest{fotocòpies}; dependent: \rest{preu}", r"independent: \rest{hora}; dependent: \rest{temperatura}", r"independent: \rest{km}; dependent: \rest{gasolina}"])),
 (1, r"Completa la taula de la funció $y=2x+3$, escriu els punts i dibuixa'ls." + center(tvb([0, 1, 2, 3, 4])),
     center(tv([0, 1, 2, 3, 4], [2 * k + 3 for k in range(5)])) + r"Punts: $(0,\ 3)$, $(1,\ 5)$, $(2,\ 7)$, $(3,\ 9)$, $(4,\ 11)$. Estan alineats:" + center(F33)),
 (1, r"La taula dona la temperatura d'un dia de primavera. Dibuixa el gràfic (unint els punts) i digues a quina hora va fer més calor i a quina més fred." + center(tv(H34, T34, 'Hora', r'$^\circ\text{C}$')),
     center(F34) + r"Més calor: a les \rest{15 h} (18\,$^\circ$C). Més fred: a les \rest{3 h} (6\,$^\circ$C)."),
 (2, r"Quines d'aquestes taules corresponen a una funció? Explica per què." + center(r'\quad '.join(tv(*T) for T in T35)),
     r"La 1a i la 3a \rest{sí}; la 2a \rest{no}, perquè per a $x=1$ hi ha dos valors de $y$ (4 i 6). La 3a és una funció constant."),
 (2, r"Troba la fórmula de cada taula:" + center(r'\quad '.join(tv(*T) for T in (T36a, T36b, T36c))),
     tasks(3, [r"Comença en 5 i suma 2: \ $\res{y=2x+5}$", r"$y$ és 10 vegades $x$: \ $\res{y=10x}$", r"Comença en 9 i resta 1: \ $\res{y=9-x}$"])),
 (2, r"Una tarifa de mòbil costa 10\,€ al mes més 3\,€ per cada GB de dades. Escriu la fórmula del preu $y$ si gastem $x$ GB i fes una taula per a 0, 1, 2, 5 i 10 GB.",
     r"$\res{y=3x+10}$ \qquad " + tv([0, 1, 2, 5, 10], [10, 13, 16, 25, 40], 'GB', '€')),
 (3, r"Fes una taula del perímetre $P$ i una de l'àrea $A$ d'un quadrat de costat $l=1,\ 2,\ 3,\ 4,\ 5$\,cm. Escriu-ne les fórmules i dibuixa els gràfics. Quin és una recta?",
     tv([1, 2, 3, 4, 5], [4, 8, 12, 16, 20], '$l$', '$P$') + r'\quad ' + tv([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], '$l$', '$A$') + r"\quad $\res{P=4l}$, \ $\res{A=l^2}$" + center(F38)
     + r"El del \rest{perímetre} és una recta (suma sempre 4); el de l'àrea és una corba (suma 3, 5, 7, 9…)."),
 (3, r"Volem fer rectangles de 20\,cm de perímetre amb costats de cm enters. Fes una taula amb la base $x$ i l'altura $y$, escriu-ne la fórmula i dibuixa el gràfic. És creixent o decreixent?",
     r"La base i l'altura sumen 10: \ $\res{y=10-x}$. \quad " + tv(list(range(1, 10)), [10 - b for b in range(1, 10)], 'base', 'alt.') + center(F39) + r"És \rest{decreixent}: com més base, menys altura. No s'uneixen els punts (costats enters)."),
]))

# =====================================================================
# 4. Interpretació de gràfics
# =====================================================================
EXC = [(0, 0), (1, 6), (2, 6), (4, 14), (5, 14), (7, 0)]
CHK(at(EXC, 3) == 10 and at(EXC, 6) == 7 and 14 + 14 == 28)
F41 = tp((0, 7.5, 0, 16), curves=[(EXC, 'accent')], pts=[(x, y, None, 'p2') for x, y in EXC], u=0.75, uy=0.3, ys=2, xl='temps (h)', yl='distància (km)')
TA = [(0, 6), (2, 4), (6, 4), (10, 12), (14, 18), (18, 14), (22, 8), (24, 7)]
F42 = tp((0, 25, 0, 20), curves=[(TA, 'accent')], u=0.26, uy=0.2, xs=2, ys=2, xl='h', yl=r'$^\circ$C')
PL = [(0, 2), (1, 5), (2, 9), (3, 12), (4, 14), (5, 15), (6, 15)]
F43 = tp((0, 6.6, 0, 16.5), curves=[(PL, 'teal')], pts=[(x, y, None, 'p2') for x, y in PL], u=0.6, uy=0.22, ys=2, xl='setmanes', yl='cm')
CHK(PL[4][1] == 14 and PL[1][1] - PL[0][1] == 3 and PL[2][1] - PL[1][1] == 4 and PL[6][1] - PL[5][1] == 0)
BOT = [(0, 0), (5, 20), (6, 26), (16, 26), (17, 20), (22, 0)]
F44 = tp((0, 23, 0, 30), curves=[(BOT, 'accent')], u=0.33, uy=0.14, xs=2, ys=5, gy=5, xl='min', yl='cm')
CHK(Fr(20, 5) == 4)
GR = {'A': [(0, 0), (2, 4), (4, 4), (6, 0)], 'B': [(0, 0), (6, 8)], 'C': [(0, 0), (2, 4), (4, 4), (6, 8)], 'D': [(0, 8), (3, 2), (6, 2)]}
def mini(P, cap): return r'\begin{tabular}{c}' + tp((0, 6.5, 0, 9), curves=[(P, 'accent')], u=0.3, uy=0.22, xs=2, ys=2, xl='$t$', yl='$d$') + r'\\ \textbf{' + cap + r'}\end{tabular}'
F45 = center(r'\hspace{0.3cm}'.join(mini(GR[k], k) for k in 'ABCD'))
TREN = [(0, 0), (20, 30), (25, 30), (45, 60), (50, 60), (70, 90)]
CHK(Fr(30, 20) == Fr(3, 2) and 90 == TREN[-1][1])
F46 = tp((0, 75, 0, 100), curves=[(TREN, 'accent')], u=0.12, uy=0.05, xs=10, gx=5, ys=20, gy=10, xl='min', yl='km')
CA = [(0, 0), (5, 75)]; CP = [(1, 0), (5, 100)]
CHK(lin(15)(4) == 60 and lin(25, -25)(4) == 75 and lin(15)(Fr(5, 2)) == lin(25, -25)(Fr(5, 2)) == Fr(75, 2))
F47 = tp((0, 5.5, 0, 105), curves=[(CA, 'accent'), (CP, 'teal')], pts=[(2.5, 37.5, None, 'p2')], u=0.9, uy=0.04, ys=20, gy=10, xl='h', yl='km', labs=[(5, 75, 'Anna', 'right,text=accent'), (4.6, 100, 'Pau', 'left,text=teal')])
MARC = [(0, 0), (20, 1), (50, 1), (60, 0)]
F48 = tp((0, 65, 0, 1.4), curves=[(MARC, 'accent')], u=0.13, uy=3, xs=10, ys=0.5, gy=0.25, gx=5, xl='min', yl='km')
S_.append(("Interpretació de gràfics", [
 (1, r"El gràfic mostra l'excursió en bici de la Núria (distància a casa al llarg del temps)." + center(F41)
     + tasks(1, [r"A quina distància de casa estava a les 3 hores? I a les 6 hores?", r"Quantes vegades va parar i quant de temps cada vegada?", r"Quina és la distància màxima a què va arribar? A quina hora?", r"Quant va tardar a tornar? Quina distància va recórrer en total?"])
     + recorda(r"Gràfic de distància i temps: si puja, s'allunya; si és horitzontal, està parat; si baixa, torna. Com més inclinat, més de pressa."),
     tasks(1, [r"$\res{10\text{ km}}$ i $\res{7\text{ km}}$", r"\rest{dues} vegades, d'\res{1 hora} cada una (de 1 a 2 h i de 4 a 5 h)", r"$\res{14\text{ km}}$, de les 4 a les 5 h", r"de 5 a 7 h: $\res{2\text{ hores}}$; en total, $14+14=\res{28\text{ km}}$"])),
 (1, r"El gràfic dona la temperatura al llarg d'un dia." + center(F42) + tasks(1, [r"Quina va ser la temperatura màxima? I la mínima?", r"En quins intervals de temps la temperatura puja? En quins baixa? Quan es manté constant?"]),
     tasks(1, [r"Màxima: $\res{18\ ^\circ\text{C}}$ (a les 14 h). Mínima: $\res{4\ ^\circ\text{C}}$ (de 2 a 6 h).", r"Puja de \rest{6 a 14 h}; baixa de \rest{0 a 2 h} i de \rest{14 a 24 h}; és constant de \rest{2 a 6 h}."])),
 (1, r"El gràfic mostra l'altura d'una planta durant 6 setmanes." + center(F43) + tasks(1, [r"Quant feia en començar? I a la 4a setmana?", r"En quina setmana va créixer més?", r"Què passa entre la 5a i la 6a setmana?"]),
     tasks(1, [r"$\res{2\text{ cm}}$ i $\res{14\text{ cm}}$", r"en la \rest{2a setmana} (de 5 a 9 cm: 4 cm)", r"\rest{no creix}: el gràfic és horitzontal"])),
 (2, r"El gràfic mostra l'altura de l'aigua d'una banyera. Explica què passa en cada tram." + center(F44),
     r"De 0 a 5 min \rest{s'ompli} (4\,cm per minut). De 5 a 6 min l'aigua puja de colp: algú \rest{s'hi fica}. De 6 a 16 min es \rest{banya} (constant). De 16 a 17 min \rest{ix} i l'aigua baixa. De 17 a 22 min \rest{es buida}."),
 (2, r"Quin gràfic (temps, distància a casa) correspon a cada història? N'hi ha un que sobra." + F45
     + tasks(1, [r"La Sara va a casa d'una amiga sense parar.", r"L'Òscar ix de casa, para a comprar el pa i continua fins a l'escola.", r"La Lucía va al quiosc, s'hi queda una estona i torna a casa."]),
     tasks(3, [r"\rest{B}", r"\rest{C}", r"\rest{A}"]) + r"Sobra el D (comença lluny de casa i s'acosta)."),
 (2, r"El gràfic mostra el viatge d'un tren." + center(F46) + tasks(1, [r"Quantes parades fa i quant duren?", r"Quants km fa entre parada i parada? Quant tarda?", r"Quina distància total recorre i quant de temps tarda?"]),
     tasks(1, [r"\rest{2 parades} de \res{5 min}", r"\res{30\text{ km}} en \res{20\text{ min}}", r"\res{90\text{ km}} en \res{70\text{ min}}"])),
 (3, r"L'Anna i el Pau fan la mateixa ruta en bici. Observa el gràfic i respon." + center(F47)
     + tasks(1, [r"Qui ix primer? Quanta estona abans?", r"Quants km fa cadascun en una hora? Qui va més de pressa?", r"On i quan atrapa el Pau l'Anna?"]),
     tasks(1, [r"L'\rest{Anna}, \res{1 hora} abans.", r"Anna: $75:5=\res{15\text{ km}}$; Pau: $100:4=\res{25\text{ km}}$. El \rest{Pau} va més de pressa.", r"Les línies es tallen a les $\res{2{,}5\text{ h}}$, a $\res{37{,}5\text{ km}}$ de l'eixida."])),
 (3, r"En Marc ix de casa, camina 1\,km en 20 minuts fins a la biblioteca, hi està mitja hora i torna a casa en 10 minuts. Dibuixa el gràfic (temps en minuts, distància a casa en km). En quin tram va més de pressa?",
     center(F48) + r"Punts: $(0,\ 0)$, $(20,\ 1)$, $(50,\ 1)$, $(60,\ 0)$. Va més de pressa a la \rest{tornada}: el tram és més inclinat."),
]))

# =====================================================================
# 5. Funció de proporcionalitat directa: y = m·x
# =====================================================================
F51 = ['y=4x', 'y=x+4', r'y=-\tfrac{x}{2}', 'y=4', 'y=0{,}6x', 'y=-3x']
R51 = [r'\rest{sí}, $m=\res{4}$', r'\rest{no}', r'\rest{sí}, $m=\res{-\tfrac12}$', r'\rest{no}', r'\rest{sí}, $m=\res{0{,}6}$', r'\rest{sí}, $m=\res{-3}$']
X5 = [-2, -1, 0, 1, 2]
F52 = tp((-3, 3, -7, 7), fns=[(3, 0, 'accent')], pts=[(k, 3 * k, None, 'p2') for k in X5], u=0.42, uy=0.3, ys=2)
F53 = tp(W5, fns=[(-2, 0, 'accent'), (Fr(1, 2), 0, 'teal')], pts=[(-2, 4, None, 'p0'), (2, -4, None, 'p0'), (-4, -2, None, 'p1'), (4, 2, None, 'p1')], u=0.38, labs=[(-2.6, 4.6, '$y=-2x$', 'left,text=accent'), (4.4, 2.8, r'$y=\frac x2$', 'text=teal')])
CHK(fr(-6) / 3 == -2 and lin(-2)(-4) == 8 and lin(-2)(5) == -10)
T55 = ([2, 4, 6, 8], [3, 6, 9, 12])
CHK(len({Fr(y, x) for x, y in zip(*T55)}) == 1 and Fr(3, 2) * 10 == 15)
F55 = tp((-1, 9, -1, 13), fns=[(Fr(3, 2), 0, 'accent', 0, 8.6)], pts=[(x, y, None, 'p2') for x, y in zip(*T55)], u=0.38, uy=0.3, ys=2)
L56 = [('a', 5), ('b', Fr(-1, 2)), ('c', Fr(1, 3)), ('d', -2)]
F57 = tp((0, 55, 0, 60), fns=[(Fr(11, 10), 0, 'accent', 0, 54)], pts=[(20, 22, None, 'p2'), (50, 55, None, 'p0')], proj=[(20, 22), (50, 55)], u=0.13, uy=0.11, xs=10, gx=5, ys=10, gy=5, xl='€', yl='\\$')
CHK(fr('1.1') * 20 == 22 and 55 / fr('1.1') == 50 and fr('1.1') * 35 == fr('38.5'))
F58 = tp((0, 4.3, 0, 400), fns=[(90, 0, 'accent', 0, 4.2)], pts=[(fr('2.5'), 225, None, 'p0')], proj=[(2.5, 225)], u=1, uy=0.012, xs=1, gx=0.5, ys=50, gy=50, xl='$t$ (h)', yl='$d$ (km)')
CHK(lin(90)(3) == 270 and Fr(225, 90) == fr('2.5'))
S_.append(("Funció de proporcionalitat directa: $y=m\\cdot x$", [
 (1, r"Quines d'aquestes funcions són de proporcionalitat directa? Escriu-ne el pendent $m$." + tasks(6, ['$' + f + '$' for f in F51])
     + recorda(r"Una funció de proporcionalitat directa és de la forma $y=m\cdot x$. El seu gràfic és una recta que passa per l'origen. El pendent $m$ és el que augmenta $y$ quan $x$ augmenta 1."),
     tasks(3, R51)),
 (1, r"Completa la taula de $y=3x$ i dibuixa'n el gràfic." + center(tvb(X5)),
     center(tv(X5, [3 * k for k in X5]) + r'\qquad ' + F52)),
 (1, r"Dibuixa en els mateixos eixos $y=-2x$ i $y=\dfrac{x}{2}$. Quina és creixent? Quina és més inclinada?",
     center(F53) + r"$y=\frac x2$ és \rest{creixent} ($m>0$). $y=-2x$ és decreixent i \rest{més inclinada} ($2>0{,}5$)."),
 (2, r"Una recta passa per l'origen i pel punt $(3,\ -6)$. Escriu-ne la fórmula i comprova si els punts $(-4,\ 8)$ i $(5,\ -12)$ són de la recta.",
     r"$m=\dfrac{-6}{3}=-2$: \ $\res{y=-2x}$. \ $-2\cdot(-4)=8$: $(-4,\ 8)$ \rest{sí}. \ $-2\cdot5=-10\neq-12$: $(5,\ -12)$ \rest{no}."),
 (2, r"Comprova que aquesta taula és de proporcionalitat directa, escriu-ne la fórmula i dibuixa el gràfic. Quant val $y$ si $x=10$?" + center(tv(*T55)),
     r"$\frac32=\frac64=\frac96=\frac{12}{8}=1{,}5$: \ $\res{y=1{,}5x}$. \ Per a $x=10$: $y=\res{15}$." + center(F55)),
 (2, r"Ordena aquestes rectes de més inclinada a menys i digues quines són decreixents: \ $a$: $y=5x$, \ $b$: $y=-\frac12x$, \ $c$: $y=\frac13x$, \ $d$: $y=-2x$.",
     r"Mirem $m$ sense signe: $5>2>\frac12>\frac13$. \ Ordre: \rest{$a$, $d$, $b$, $c$}. Decreixents ($m<0$): \rest{$b$ i $d$}."),
 (3, r"Un dia, 1\,€ val 1,10 dòlars. Escriu la fórmula que passa d'euros ($x$) a dòlars ($y$) i dibuixa'n el gràfic. Quants dòlars són 20\,€? I 35\,€? Quants euros són 55\,\$?",
     r"$\res{y=1{,}1x}$. \ $1{,}1\cdot20=\res{22\ \$}$; \ $1{,}1\cdot35=\res{38{,}5\ \$}$; \ $55:1{,}1=\res{50\text{ €}}$." + center(F57)),
 (3, r"Un cotxe va a 90\,km/h sempre a la mateixa velocitat. Escriu la fórmula de la distància $d$ que recorre en $t$ hores, dibuixa'n el gràfic i calcula quina distància fa en 3 hores i quant tarda a fer 225\,km.",
     r"$\res{d=90t}$. \ $90\cdot3=\res{270\text{ km}}$. \ $225:90=\res{2{,}5\text{ h}}$ (2 hores i mitja)." + center(F58)),
]))

# =====================================================================
# 6. Funció lineal: y = m·x + n
# =====================================================================
M61 = [('3x-4', 3, -4), ('-x+5', -1, 5), (r'\tfrac{x}{2}+1', Fr(1, 2), 1), ('-2x', -2, 0), ('7', 0, 7), ('6-4x', -4, 6)]
F62 = tp(W5, fns=[(2, -1, 'accent')], pts=[(k, 2 * k - 1, None, 'p2') for k in (-1, 0, 1, 2, 3)], u=0.38)
CHK([lin(2, -1)(k) for k in (-1, 0, 1, 2, 3)] == [-3, -1, 1, 3, 5])
P63 = [(2, 1), (-1, 7), (3, -2), (0, 3)]
CHK([lin(-2, 3)(x) == y for x, y in P63] == [False, False, False, True])
CHK([lin(-2, 3)(x) for x, _ in P63] == [-1, 5, -3, 3])
F64 = tp(W5, fns=[(1, 2, 'accent'), (-1, 4, 'teal')], pts=[(1, 3, '$(1,\\,3)$', 'p2')], u=0.38, labs=[(-4.4, -2.4, '$y=x+2$', 'above left,text=accent'), (-0.8, 4.9, '$y=-x+4$', 'left,text=teal')])
CHK(lin(1, 2)(1) == lin(-1, 4)(1) == 3)
L65 = [('a', 2, -1), ('b', -1, 3), ('c', Fr(1, 2), 1), ('d', 0, -3)]
F65 = tp(W5, fns=[(m, n, c) for (_, m, n), c in zip(L65, ['accent', 'teal', 'navy', 'violet'])],
         labs=[(2.8, 4.6, '$a$', 'right,text=accent'), (-1.8, 4.6, '$b$', 'left,text=teal'), (4.4, 3.2, '$c$', 'above,text=navy'), (-4.5, -3, '$d$', 'above,text=violet')], u=0.4)
for _, m, n in L65: CHK(lin(m, n)(0) == n and lin(m, n)(2) - lin(m, n)(0) == 2 * fr(m))
L66 = ['y=3x+1', 'y=-x', 'y=3x-4', 'y=5', 'y=-x+2', 'y=2']
T67 = ([0, 1, 2, 3], [4, 1, -2, -5])
CHK([lin(-3, 4)(x) for x in T67[0]] == T67[1])
CHK(lin(2, 3)(0) == 3 and lin(2, 3)(2) == 7 and lin(2, -3)(1) == -1 and lin(2, -3)(3) == 3)
CHK(lin(-3, 5)(2) == -1 and lin(2, 5)(3) == 11)
S_.append(("Funció lineal: $y=m\\cdot x+n$", [
 (1, r"Escriu el pendent $m$ i l'ordenada en l'origen $n$ de cada funció:" + tasks(6, ['$y=' + s + '$' for s, _, _ in M61])
     + recorda(r"En $y=mx+n$, $m$ és el \textbf{pendent} (el que canvia $y$ quan $x$ augmenta 1) i $n$ és l'\textbf{ordenada en l'origen}: la recta talla l'eix $Y$ en $(0,\ n)$."),
     tasks(3, [r'$m=\res{%s}$, $n=\res{%s}$' % (tn(m), tn(n)) for _, m, n in M61])),
 (1, r"Completa la taula de $y=2x-1$ i dibuixa'n el gràfic. On talla l'eix $Y$?" + center(tvb([-1, 0, 1, 2, 3])),
     center(tv([-1, 0, 1, 2, 3], [-3, -1, 1, 3, 5]) + r'\qquad ' + F62) + r"Talla l'eix $Y$ en $\res{(0,\ -1)}$."),
 (1, r"Quins d'aquests punts són de la recta $y=-2x+3$? \ $(2,\ 1)$, \ $(-1,\ 7)$, \ $(3,\ -2)$, \ $(0,\ 3)$.",
     r"Substituïm la $x$: \ $x=2$: $-1\neq1$ \rest{no}; \ $x=-1$: $5\neq7$ \rest{no}; \ $x=3$: $-3\neq-2$ \rest{no}; \ $x=0$: $3$ \rest{sí}."),
 (2, r"Dibuixa en els mateixos eixos $y=x+2$ i $y=-x+4$. En quin punt es tallen? Comprova-ho amb les fórmules.",
     center(F64) + r"Es tallen en $\res{(1,\ 3)}$: \ $1+2=3$ \ i \ $-1+4=3$."),
 (2, r"Escriu la fórmula de cadascuna de les rectes del dibuix." + center(F65),
     tasks(4, [r"$\res{%s}$" % eq(m, n) for _, m, n in L65])),
 (2, r"Observa aquestes funcions: \ " + ', \ '.join('$' + s + '$' for s in L66) + r". Quines són paral·leles? Quines passen per l'origen? Quines són constants?",
     r"Paral·leles (mateix $m$): \rest{$y=3x+1$ i $y=3x-4$}; \rest{$y=-x$ i $y=-x+2$}; \rest{$y=5$ i $y=2$}. Per l'origen: \rest{$y=-x$}. Constants: \rest{$y=5$ i $y=2$}."),
 (2, r"Troba la fórmula de la funció lineal d'aquesta taula:" + center(tv(*T67)),
     r"Per a $x=0$, $y=4$: $n=4$. Cada vegada que $x$ augmenta 1, $y$ disminueix 3: $m=-3$. \ $\res{y=-3x+4}$"),
 (3, r"Troba la fórmula de la recta que passa per:" + tasks(2, [r"$(0,\ 3)$ i $(2,\ 7)$", r"$(1,\ -1)$ i $(3,\ 3)$"]),
     tasks(1, [r"$n=3$; de $x=0$ a $x=2$, $y$ puja 4: $m=4:2=2$. \ $\res{y=2x+3}$",
               r"De $x=1$ a $x=3$, $y$ puja 4: $m=2$. Tornant un pas enrere des de $(1,\ -1)$: $n=-1-2=-3$. \ $\res{y=2x-3}$"])),
 (3, r"Respon:" + tasks(1, [r"Quin valor ha de tindre $k$ perquè el punt $(2,\ k)$ siga de la recta $y=-3x+5$?", r"Quin valor ha de tindre $a$ perquè el punt $(a,\ 11)$ siga de la recta $y=2x+5$?"]),
     tasks(1, [r"$k=-3\cdot2+5=\res{-1}$", r"$2a+5=11\Rightarrow2a=6\Rightarrow a=\res{3}$"])),
]))

# =====================================================================
# 7. Problemes amb funcions lineals
# =====================================================================
TX = lin('1.5', '3.5'); CHK(TX(8) == fr('15.5') and (fr(26) - fr('3.5')) / fr('1.5') == 15)
F71 = tp((0, 16.5, 0, 28), fns=[(fr('1.5'), fr('3.5'), 'accent', 0, 16.5)], pts=[(0, 3.5, None, 'p2'), (8, 15.5, None, 'p2'), (15, 26, None, 'p0')], proj=[(8, 15.5), (15, 26)], u=0.36, uy=0.2, xs=2, gx=1, ys=4, gy=2, xl='km', yl='€')
ESP = lin(-3, 24); CHK(ESP(5) == 9 and Fr(24, 3) == 8)
F72 = tp((0, 8.8, 0, 26), fns=[(-3, 24, 'accent', 0, 8)], u=0.5, uy=0.16, xs=1, ys=4, gy=2, xl='h', yl='cm')
MB = lin('0.08', 6); CHK(MB(50) == 10 and (fr(9) - 6) / fr('0.08') == fr('37.5'))
DP = lin(25, 100); CHK(DP(6) == 250 and (fr(600) - 100) / 25 == 20)
LP = [(1, 55), (2, 90), (3, 125)]; LF = lin(35, 20)
for h, p in LP: CHK(LF(h) == p)
CHK(LF(6) == 230 and (fr(300) - 20) / 35 == 8)
FA = lin('1.8', 32); CHK(FA(0) == 32 and FA(100) == 212 and FA(25) == 77 and (fr(50) - 32) / fr('1.8') == 10)
PK = lin(2, 3); CHK(PK(5) == 13 and (fr(19) - 3) / 2 == 8)
LA, LB = lin('0.25', 30), lin('0.15', 50); CHK(LA(150) == fr('67.5') and LB(150) == fr('72.5') and LA(200) == LB(200) == 80)
F79 = tp((0, 330, 0, 140), fns=[(fr('0.25'), 30, 'accent', 0, 330), (fr('0.15'), 50, 'teal', 0, 330)], pts=[(200, 80, None, 'p2')], proj=[(200, 80)], u=0.03, uy=0.045, xs=50, gx=25, ys=20, gy=10, xl='km', yl='€',
         labs=[(320, 110, 'A', 'right,text=accent'), (320, 98, 'B', 'right,text=teal')])
GA_, GB_ = lin(20, 45), lin(35); CHK(GA_(3) == GB_(3) == 105 and GA_(2) > GB_(2) and GA_(6) < GB_(6))
F710 = tp((0, 6.5, 0, 240), fns=[(20, 45, 'accent', 0, 6.5), (35, 0, 'teal', 0, 6.5)], pts=[(3, 105, None, 'p2')], proj=[(3, 105)], u=0.9, uy=0.022, ys=40, gy=20, xl='mesos', yl='€',
          labs=[(6.5, 175, 'A', 'right,text=accent'), (6.4, 227, 'B', 'right,text=teal')])
S_.append(("Problemes amb funcions lineals", [
 (1, r"Un taxi cobra 3,50\,€ de baixada de bandera i 1,50\,€ per km. Escriu la fórmula del preu, dibuixa'n el gràfic i calcula quant costa un viatge de 8\,km. Quants km hem fet si paguem 26\,€?"
     + recorda(r"En molts problemes hi ha una \textbf{part fixa} $n$ i una quantitat $m$ que se suma (o es resta) per cada unitat: $y=mx+n$."),
     r"$\res{y=1{,}5x+3{,}5}$. \ $1{,}5\cdot8+3{,}5=\res{15{,}50\text{ €}}$. \ $1{,}5x+3{,}5=26\Rightarrow1{,}5x=22{,}5\Rightarrow x=\res{15\text{ km}}$." + center(F71)),
 (1, r"Una espelma fa 24\,cm i es crema 3\,cm cada hora. Escriu la fórmula de l'altura $y$ al cap de $x$ hores i dibuixa'n el gràfic. Quant farà al cap de 5\,h? Quan s'acabarà?",
     r"$\res{y=-3x+24}$. \ $-15+24=\res{9\text{ cm}}$. \ $-3x+24=0\Rightarrow x=\res{8\text{ h}}$." + center(F72)),
 (1, r"Una tarifa de telèfon costa 6\,€ al mes més 0,08\,€ per minut. Quant paguem si parlem 50 minuts? Quants minuts hem parlat si paguem 9\,€?",
     r"$y=0{,}08x+6$. \ $0{,}08\cdot50+6=\res{10\text{ €}}$. \ $0{,}08x=3\Rightarrow x=\res{37{,}5\text{ min}}$."),
 (2, r"Un dipòsit té 100\,L d'aigua i una aixeta hi aboca 25\,L cada minut. Escriu la fórmula. Quants litres hi haurà al cap de 6 minuts? Si hi caben 600\,L, quan s'omplirà?",
     r"$\res{y=25x+100}$. \ $150+100=\res{250\text{ L}}$. \ $25x+100=600\Rightarrow25x=500\Rightarrow x=\res{20\text{ min}}$."),
 (2, r"Un lampista cobra segons aquesta taula. Troba la fórmula i calcula quant cobrarà per 6 hores. Quantes hores ha treballat si cobra 300\,€?" + center(tv([h for h, _ in LP], [p for _, p in LP], 'Hores', 'Preu (€)')),
     r"Cada hora més suma 35\,€: $m=35$; per a 0 hores, $55-35=20$\,€: $n=20$. \ $\res{y=35x+20}$. \ $35\cdot6+20=\res{230\text{ €}}$. \ $35x+20=300\Rightarrow x=\res{8\text{ h}}$."),
 (2, r"Per a passar de graus Celsius ($x$) a graus Fahrenheit ($y$) es fa servir la fórmula $y=1{,}8x+32$. A quants $^\circ$F equivalen 0\,$^\circ$C, 25\,$^\circ$C i 100\,$^\circ$C? A quants $^\circ$C equivalen 50\,$^\circ$F?",
     r"$\res{32\ ^\circ\text{F}}$, \ $1{,}8\cdot25+32=\res{77\ ^\circ\text{F}}$, \ $\res{212\ ^\circ\text{F}}$. \ $1{,}8x+32=50\Rightarrow1{,}8x=18\Rightarrow x=\res{10\ ^\circ\text{C}}$."),
 (2, r"Un aparcament cobra 3\,€ per entrar i 2\,€ per cada hora. Escriu la fórmula i fes una taula per a 1, 2, 3, 4 i 5 hores. Quantes hores hi hem deixat el cotxe si paguem 19\,€?",
     r"$\res{y=2x+3}$ \quad " + tv([1, 2, 3, 4, 5], [PK(k) for k in range(1, 6)], 'h', '€') + r" \quad $2x+3=19\Rightarrow x=\res{8\text{ h}}$."),
 (3, r"Per a llogar una furgoneta, l'empresa A cobra 30\,€ més 0,25\,€ per km i l'empresa B, 50\,€ més 0,15\,€ per km. Quina convé si fem 150\,km? Per a quants km costen el mateix? Fes el gràfic de les dues.",
     r"A: $y=0{,}25x+30$; \ B: $y=0{,}15x+50$. \ Per a 150\,km: A $=67{,}50$\,€, B $=72{,}50$\,€: convé l'\rest{A}. Cada km, A cobra 0,10\,€ més, però comença 20\,€ per davall: costen igual quan $0{,}10x=20$, \ $x=\res{200\text{ km}}$ (80\,€)." + center(F79)),
 (3, r"El gimnàs A cobra 45\,€ de matrícula i 20\,€ al mes; el gimnàs B no té matrícula i cobra 35\,€ al mes. Fes el gràfic de les dues tarifes. Quan costen el mateix? Quin convé si vols anar-hi 6 mesos?",
     r"A: $y=20x+45$; \ B: $y=35x$. \ Costen el mateix als $\res{3\text{ mesos}}$ (105\,€). Per a 6 mesos: A $=165$\,€ i B $=210$\,€: convé l'\rest{A}." + center(F710)),
]))
CHK(GA_(6) == 165 and GB_(6) == 210)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\definecolor{violet}{HTML}{7C6CF0}\n'
KW = 'pdfkeywords={coordenades cartesianes, eixos, quadrants, abscissa, ordenada, plànols, desplaçaments, simetries, taules de valors, gràfics, funcions, creixement, màxims i mínims, proporcionalitat directa, pendent, funció lineal, ordenada en l\'origen}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
TIT = "Gràfics de funcions"

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 9: %s. 1r d'ESO}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 9 · 1r d'ESO" % t)
    assert 'Unitat 9' in p and 'unitat 9' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{1r ESO}{''' + ('Solucions de la fitxa · Unitat 9' if sol else "Fitxa d'exercicis · Unitat 9") + r'''}{''' + TIT + r'''}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs un pla cartesià per a situar punts, eines per a passar de la taula al gràfic i per a explorar les rectes $y=mx+n$."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Per a dibuixar punts, rectes i gràfics fes servir paper quadriculat i escriu sempre el nom i la unitat de cada eix.") + r'''
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
    name = 't9-fitxa-solucions.tex' if sol else 't9-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis,', NCHK[0], 'comprovacions')
