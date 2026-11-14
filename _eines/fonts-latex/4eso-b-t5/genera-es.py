# Versió en castellà de genera.py. Genera t5-fitxa-exercicis-es.tex i t5-fitxa-solucions-es.tex (4t ESO Matemàtiques B, Unitat 5: Trigonometria)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Recull els exercicis de les fitxes del departament de 4t ESO (Trigonometria, Trigonometria II i III, exercicis d'entrega i
# exercicis del llibre: 1-20 i 39-64) i n'afegeix de nous; les 8 seccions segueixen els apartats dels apunts (5.1-5.8).
# Els valors numèrics es calculen ací (math) i els exactes amb sympy; ap() i eq() comproven que cada resultat escrit a mà
# coincideix amb el calculat. Les figures són TikZ.
# Ús: python3 genera-es.py && pdflatex t5-fitxa-exercicis-es.tex (dues vegades) && pdflatex t5-fitxa-solucions-es.tex (dues vegades)
import os, sys, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

def r(d): return math.radians(d)
def sin(d): return math.sin(r(d))
def cos(d): return math.cos(r(d))
def tan(d): return math.tan(r(d))
def asin(x): return math.degrees(math.asin(x))
def acos(x): return math.degrees(math.acos(x))
def atan(x): return math.degrees(math.atan(x))
def DMS(d, m=0, s=0): return d + m / 60 + s / 3600
S2, S3 = math.sqrt(2), math.sqrt(3)

def ap(a, b, tol=1e-9):
    """comprova que dos valors numèrics coincideixen"""
    assert abs(a - b) <= tol * max(1, abs(b)), (a, b)
    ck(1, 1)
def d2(x, k=2): return dec(x, k)
def d4(x): return ('%.4f' % x).replace('.', ',').replace('-0,0000', '0,0000')
def dms(x):
    sg = '-' if x < 0 else ''; t = round(abs(x) * 3600)
    d, m, q = t // 3600, (t % 3600) // 60, t % 60
    return sg + '%d^\\circ' % d + ("%d'" % m if m or q else '') + ("%d''" % q if q else '')
def pifr(num, den):
    g = math.gcd(num, den); num //= g; den //= g
    if num == 0: return '0'
    top = ('' if abs(num) == 1 else str(abs(num))) + r'\pi'
    return ('-' if num < 0 else '') + (top if den == 1 else r'\frac{%s}{%d}' % (top, den))
def L(e): return sp.latex(sp.nsimplify(e) if not isinstance(e, sp.Basic) else e).replace(r'\frac', r'\tfrac')
def Ld(e): return sp.latex(e)
def items(*xs): return r'\begin{enumerate}[label=\alph*),leftmargin=*,itemsep=2pt]' + ''.join(r'\item ' + x for x in xs) + r'\end{enumerate}'

S = []

# =====================================================================
# 1. Mesura d'angles: graus i radians
D1 = [45, 30, 120, 150, 540, 1080, 1800, 240, 310, 70, 12, 720]
R2 = [(1, 1), (4, 1), (7, 1), (1, 6), (3, 4), (3, 2), (5, 3), (1, 2), (4, 3), (6, 5), (2, 5), (1, 9)]
g2 = [F(180 * a, b) for a, b in R2]
ck(g2, [180, 720, 1260, 30, 135, 270, 300, 90, 240, 216, 72, 20])
def rq(a, b): return '$%s$' % pifr(a, b) if not (a == 6 and b == 5) else r'$1{,}2\pi$'
tq = [('30', None), (None, (1, 4)), ('60', None), (None, (2, 3)), ('135', None), (None, (5, 6)), ('210', None), (None, (5, 4)), ('300', None), (None, (11, 6))]
def tab3(sol):
    g, rr = [], []
    for dg, rd in tq:
        if dg:
            g.append('$%s^\\circ$' % dg); rr.append(('$\\res{%s}$' % pifr(int(dg), 180)) if sol else '')
        else:
            v = F(180 * rd[0], rd[1]); assert v.denominator == 1
            g.append(('$\\res{%d^\\circ}$' % v) if sol else ''); rr.append('$%s$' % pifr(rd[0], rd[1]))
    return (r'\begin{center}\renewcommand{\arraystretch}{1.6}\begin{tabular}{|l|*{10}{C{1.05cm}|}}\hline\textbf{Grados} & ' + ' & '.join(g) +
            r'\\\hline\textbf{Radianes} & ' + ' & '.join(rr) + r'\\\hline\end{tabular}\end{center}')
hexa = r'''\begin{center}\begin{tikzpicture}[scale=1.25]
\foreach \i/\n in {0/D,1/E,2/F,3/A,4/B,5/C} \coordinate (\n) at (60*\i:1.2);
\coordinate (O) at (0,0);
\draw[navy, line width=1.2pt] (A)--(B)--(C)--(D)--(E)--(F)--cycle;
\draw[muted, dashed] (A)--(C) (A)--(D) (O)--(B);
\fill (O) circle (1.3pt) node[above right=-1pt,font=\small]{$O$};
\foreach \n/\p in {A/left,B/below left,C/below right,D/right,E/above right,F/above left} \node[\p,font=\small] at (\n) {$\n$};
\end{tikzpicture}\end{center}'''
ap(math.degrees(math.acos((1.2 ** 2 + (1.2 * S3) ** 2 - 1.2 ** 2) / (2 * 1.2 * 1.2 * S3))), 30)  # angle BAC = 30°
r6 = [math.degrees(1), math.degrees(0.75), math.degrees(2.5)]
ck([F(DMS(22, 30)).limit_denominator(1000) / 180, F(DMS(52, 30)).limit_denominator(1000) / 180, F(DMS(157, 30)).limit_denominator(1000) / 180], [F(1, 8), F(7, 24), F(7, 8)])
S.append(("Medida de ángulos: grados y radianes", [
 (1, r"Expresa en radianes estos ángulos (de manera exacta, en función de $\pi$):" + tasks(6, ['$%d^\\circ$' % d for d in D1]),
     tasks(6, [R(pifr(d, 180)) for d in D1])),
 (1, r"Expresa en grados sexagesimales estos ángulos en radianes:" + tasks(6, [rq(a, b) for a, b in R2]),
     tasks(6, [R('%d^\\circ' % v) for v in g2])),
 (1, r"Completa la tabla siguiente:" + tab3(False), tab3(True)),
 (1, r"Expresa, tanto en grados sexagesimales como en radianes, estas partes de una circunferencia:" + tasks(4, ["Una cuarta parte.", "Tres cuartas partes.", "Una sexta parte.", "Una tercera parte."]),
     tasks(4, [R(r'90^\circ=\frac{\pi}{2}'), R(r'270^\circ=\frac{3\pi}{2}'), R(r'60^\circ=\frac{\pi}{3}'), R(r'120^\circ=\frac{2\pi}{3}')])),
 (2, r"En el hexágono regular $ABCDEF$ de centro $O$, expresa en radianes los ángulos $\widehat{AOB}$, $\widehat{ABC}$, $\widehat{BAC}$ y $\widehat{ACD}$." + hexa,
     r"$\widehat{AOB}=\frac{360^\circ}{6}=" + Rm(r'\frac{\pi}{3}') + r"$; \ ángulo interior: $\widehat{ABC}=120^\circ=" + Rm(r'\frac{2\pi}{3}') +
     r"$; \ el triángulo $ABC$ es isósceles, y $\widehat{BAC}=\frac{180^\circ-120^\circ}{2}=30^\circ=" + Rm(r'\frac{\pi}{6}') +
     r"$; \ $AD$ es un diámetro y el ángulo inscrito $\widehat{ACD}$ es recto: $" + Rm(r'\frac{\pi}{2}') + "$."),
 (2, r"Pasa a grados, minutos y segundos: \ $1$ rad, \ $0{,}75$ rad \ y \ $2{,}5$ rad. Pasa a radianes, de manera exacta: \ $22^\circ30'$, \ $52^\circ30'$ \ y \ $157^\circ30'$.",
     tasks(3, [R(dms(x)) for x in r6] + [R(r'\frac{\pi}{8}'), R(r'\frac{7\pi}{24}'), R(r'\frac{7\pi}{8}')])),
 (3, r"La aguja de las horas de un reloj da una vuelta en 12 horas. ¿Qué ángulo, en grados y en radianes, recorre en una hora? ¿Y la aguja de los minutos en 20 minutos? ¿Qué ángulo forman las dos agujas a las 4 en punto?",
     r"Horas: $\frac{360^\circ}{12}=" + Rm(r'30^\circ=\frac{\pi}{6}') + r"$. Minutos: $\frac{20}{60}\cdot360^\circ=" + Rm(r'120^\circ=\frac{2\pi}{3}') + r"$. A las 4: $4\cdot30^\circ=" + Rm(r'120^\circ=\frac{2\pi}{3}') + "$."),
]))

# =====================================================================
# 2. Raons trigonomètriques d'un angle agut
def tri(op, ct, hip):
    """raons exactes (fraccions) de α (oposat op, contigu ct) i de β"""
    return [(F(op, hip), F(ct, hip), F(op, ct)), (F(ct, hip), F(op, hip), F(ct, op))]
T8 = [("Catetos de 30 cm y 16 cm; $\\alpha$ es opuesto al cateto de 16 cm.", 16, 30, None),
      ("Hipotenusa de 10 cm y cateto de 6 cm opuesto a $\\alpha$.", 6, None, 10),
      ("Catetos de 24 cm y 10 cm; $\\alpha$ es opuesto al cateto de 24 cm.", 24, 10, None),
      ("Hipotenusa de 25 cm y cateto de 7 cm contiguo a $\\alpha$.", None, 7, 25),
      ("Hipotenusa de 29 cm y cateto de 20 cm contiguo a $\\alpha$.", None, 20, 29)]
s8 = []
for t, op, ct, hp in T8:
    if hp is None: hp = math.isqrt(op * op + ct * ct); assert hp * hp == op * op + ct * ct; falta = 'hipotenusa $%d$' % hp
    elif op is None: op = math.isqrt(hp * hp - ct * ct); assert op * op + ct * ct == hp * hp; falta = 'cateto opuesto $%d$' % op
    else: ct = math.isqrt(hp * hp - op * op); assert op * op + ct * ct == hp * hp; falta = 'cateto contiguo $%d$' % ct
    (a1, a2, a3), (b1, b2, b3) = tri(op, ct, hp)
    s8.append('Pitágoras: ' + falta + r' cm. \ $\sin\alpha=%s$, $\cos\alpha=%s$, $\tg\alpha=%s$; \ $\sin\beta=%s$, $\cos\beta=%s$, $\tg\beta=%s$' %
              tuple(Rm(tn(x)) for x in (a1, a2, a3, b1, b2, b3)))
figABD = r'''\begin{center}\begin{tikzpicture}[scale=0.27]
\coordinate (A) at (0,0); \coordinate (D) at (9,0); \coordinate (B) at (9,12); \coordinate (C) at (25,0);
\draw[navy, line width=1.1pt] (A)--(B)--(C)--cycle; \draw[muted, dashed] (B)--(D);
\draw (D)++(-0.9,0)--++(0,0.9)--++(0.9,0);
\node[below left] at (A) {$A$}; \node[above] at (B) {$B$}; \node[below right] at (C) {$C$}; \node[below] at (D) {$D$};
\node[above left, font=\small] at (4.5,6) {15 cm}; \node[right, font=\small] at (9,5) {12 cm}; \node[below, font=\small] at (17,0) {16 cm};
\end{tikzpicture}\end{center}'''
T10 = [DMS(15), DMS(55, 20), DMS(72, 25, 40), 85.5]
tab10 = r'''\begin{center}\renewcommand{\arraystretch}{1.45}\begin{tabular}{|c|*{4}{C{2.3cm}|}}\hline $\alpha$ & $15^\circ$ & $55^\circ20'$ & $72^\circ25'40''$ & $85{,}5^\circ$\\\hline
$\sin\alpha$ & %s\\\hline $\cos\alpha$ & %s\\\hline $\tg\alpha$ & %s\\\hline\end{tabular}\end{center}'''
t10s = tab10 % tuple(' & '.join(R(d4(f(a))) for a in T10) for f in (sin, cos, tan))
I11 = [(r'\sin\alpha=\frac{\sqrt3}{2}', asin(S3 / 2)), (r'\cos\alpha=\frac13', acos(1 / 3)), (r'\tg\alpha=2{,}5', atan(2.5)), (r'\sin\alpha=0{,}25', asin(.25)), (r'\cos\alpha=0{,}8', acos(.8))]
ap(I11[0][1], 60)
ck(math.isqrt(61) ** 2 == 61, False)
# exercici de la hipotenusa 10 i tg 7/12
x15 = sp.Symbol('x', positive=True)
c15 = sp.solve(sp.Eq((7 * x15) ** 2 + (12 * x15) ** 2, 100), x15)[0]
op15, ct15 = sp.radsimp(7 * c15), sp.radsimp(12 * c15)
eq(op15, '70*sqrt(193)/193'); eq(ct15, '120*sqrt(193)/193')
S.append(("Razones trigonométricas de un ángulo agudo", [
 (1, r"Calcula las razones trigonométricas (seno, coseno y tangente) del ángulo agudo $\alpha$ y del otro ángulo agudo, $\beta$, de estos triángulos rectángulos:" + items(*[t for t, _, _, _ in T8]),
     items(*s8)),
 (1, r"Calcula las razones trigonométricas de los ángulos $\hat A$, $\hat C$, $\widehat{ABD}$ y $\widehat{CBD}$." + figABD,
     r"Pitágoras: $\overline{AD}=\sqrt{15^2-12^2}=9$ cm y $\overline{BC}=\sqrt{12^2+16^2}=20$ cm." + items(
         r"$\sin\hat A=\frac{12}{15}=%s$, \ $\cos\hat A=\frac{9}{15}=%s$, \ $\tg\hat A=\frac{12}{9}=%s$" % (Rm(r'\frac45'), Rm(r'\frac35'), Rm(r'\frac43')),
         r"$\sin\hat C=\frac{12}{20}=%s$, \ $\cos\hat C=\frac{16}{20}=%s$, \ $\tg\hat C=\frac{12}{16}=%s$" % (Rm(r'\frac35'), Rm(r'\frac45'), Rm(r'\frac34')),
         r"$\sin\widehat{ABD}=\frac{9}{15}=%s$, \ $\cos\widehat{ABD}=\frac{12}{15}=%s$, \ $\tg\widehat{ABD}=\frac{9}{12}=%s$" % (Rm(r'\frac35'), Rm(r'\frac45'), Rm(r'\frac34')),
         r"$\sin\widehat{CBD}=\frac{16}{20}=%s$, \ $\cos\widehat{CBD}=\frac{12}{20}=%s$, \ $\tg\widehat{CBD}=\frac{16}{12}=%s$" % (Rm(r'\frac45'), Rm(r'\frac35'), Rm(r'\frac43')))),
 (1, r"Completa la tabla con la calculadora (con cuatro decimales):" + tab10 % (('& & & ',) * 3), t10s),
 (1, r"Halla, con la calculadora, el ángulo agudo $\alpha$ en cada caso:" + tasks(5, ['$%s$' % t for t, _ in I11]),
     tasks(3, ['$\\alpha=%s$' % (Rm('60^\\circ') if i == 0 else r'\approx' + Rm(dms(v))) for i, (_, v) in enumerate(I11)])),
 (2, r"Comprueba, para $\alpha=60^\circ$, a partir de los hexágonos regulares de lado 4 cm y de lado 6 cm (formados por seis triángulos equiláteros), que las razones trigonométricas no varían según la longitud del lado.",
     r"Medio triángulo equilátero de lado 4: catetos 2 y $\sqrt{16-4}=2\sqrt3$. Medio triángulo de lado 6: catetos 3 y $\sqrt{36-9}=3\sqrt3$. En los dos: $\sin60^\circ=\frac{2\sqrt3}{4}=\frac{3\sqrt3}{6}=" + Rm(r'\frac{\sqrt3}{2}') +
     r"$, \ $\cos60^\circ=\frac24=\frac36=" + Rm(r'\frac12') + r"$, \ $\tg60^\circ=\frac{2\sqrt3}{2}=\frac{3\sqrt3}{3}=" + Rm(r'\sqrt3') + r"$: \rest{no dependen del lado}."),
 (2, r"Calcula los lados que faltan en cada triángulo rectángulo y, si hace falta, las otras razones del ángulo:" + items(
         r"El cateto contiguo a un ángulo $\alpha$ mide 5 cm y $\tg\alpha=\frac65$.",
         r"El seno de un ángulo vale $\frac{12}{13}$ y el cateto opuesto mide 24 cm. Calcula también el coseno y la tangente.",
         r"El cateto opuesto a un ángulo mide 15 cm y la tangente de ese ángulo vale $\frac34$. Calcula también el seno y el coseno.",
         r"La hipotenusa mide 2 cm y la tangente de uno de los ángulos vale 1."),
     items(r"Cateto opuesto: $5\cdot\frac65=" + Rm(r'6\ \text{cm}') + r"$; \ hipotenusa: $\sqrt{25+36}=" + Rm(r'\sqrt{61}\approx' + d2(math.sqrt(61)) + r'\ \text{cm}') + "$.",
           r"Hipotenusa: $\frac{24}{12/13}=" + Rm(r'26\ \text{cm}') + r"$; \ cateto: $\sqrt{26^2-24^2}=" + Rm(r'10\ \text{cm}') + r"$; \ $\cos=" + Rm(r'\frac{5}{13}') + r"$, \ $\tg=" + Rm(r'\frac{12}{5}') + "$.",
           r"Cateto contiguo: $\frac{15}{3/4}=" + Rm(r'20\ \text{cm}') + r"$; \ hipotenusa: $\sqrt{15^2+20^2}=" + Rm(r'25\ \text{cm}') + r"$; \ $\sin=" + Rm(r'\frac35') + r"$, \ $\cos=" + Rm(r'\frac45') + "$.",
           r"Los dos catetos son iguales: $x^2+x^2=4\Rightarrow x=" + Rm(r'\sqrt2\ \text{cm}') + "$ cada uno.")),
 (3, r"La hipotenusa de un triángulo rectángulo mide 10 cm y la tangente de uno de los ángulos agudos vale $\frac{7}{12}$. Calcula los catetos y el seno y el coseno de ese ángulo.",
     r"Los catetos son $7x$ y $12x$: $49x^2+144x^2=100\Rightarrow x=\frac{10}{\sqrt{193}}$. Catetos: $" + Rm(r'\frac{70\sqrt{193}}{193}\approx' + d2(float(op15)) + r'\ \text{cm}') + r"$ y $" +
     Rm(r'\frac{120\sqrt{193}}{193}\approx' + d2(float(ct15)) + r'\ \text{cm}') + r"$. \ $\sin\alpha=" + Rm(r'\frac{7\sqrt{193}}{193}') + r"$, \ $\cos\alpha=" + Rm(r'\frac{12\sqrt{193}}{193}') + "$."),
]))
eq('7*sqrt(193)/193', op15 / 10); eq('12*sqrt(193)/193', ct15 / 10)

# =====================================================================
# 3. Raons de 30°, 45° i 60°
tab15 = r'''\begin{center}\renewcommand{\arraystretch}{1.6}\begin{tabular}{|l|*{5}{C{1.6cm}|}}\hline
& $0^\circ$ & $30^\circ$ & $45^\circ$ & $60^\circ$ & $90^\circ$\\\hline
$\sin$ & %s\\\hline $\cos$ & %s\\\hline $\tg$ & %s\\\hline\end{tabular}\end{center}'''
rows15 = [['0', r'\frac12', r'\frac{\sqrt2}{2}', r'\frac{\sqrt3}{2}', '1'], ['1', r'\frac{\sqrt3}{2}', r'\frac{\sqrt2}{2}', r'\frac12', '0'], ['0', r'\frac{\sqrt3}{3}', '1', r'\sqrt3', r'\nexists']]
num15 = [[0, .5, S2 / 2, S3 / 2, 1], [1, S3 / 2, S2 / 2, .5, 0], [0, S3 / 3, 1, S3, None]]
for i, dg in enumerate([0, 30, 45, 60, 90]):
    ap(sin(dg), num15[0][i]); ap(cos(dg), num15[1][i])
    if dg != 90: ap(tan(dg), num15[2][i])
# costats exactes
C16 = [(r"Un ángulo de $60^\circ$ y el cateto opuesto, de 5 cm.", '5/sin(pi/3)', '5/tan(pi/3)', r'\frac{10\sqrt3}{3}', r'\frac{5\sqrt3}{3}', 'el cateto contiguo'),
       (r"Un ángulo de $30^\circ$ y el cateto opuesto, de 2 cm.", '2/sin(pi/6)', '2/tan(pi/6)', '4', r'2\sqrt3', 'el cateto contiguo'),
       (r"Un ángulo de $45^\circ$ y el cateto contiguo, de 7 cm.", '7/cos(pi/4)', '7*tan(pi/4)', r'7\sqrt2', '7', 'el cateto opuesto'),
       (r"Un ángulo de $60^\circ$ y el cateto contiguo, de 6 cm.", '6/cos(pi/3)', '6*tan(pi/3)', '12', r'6\sqrt3', 'el cateto opuesto'),
       (r"Un ángulo de $45^\circ$ y el cateto opuesto, de 12 cm.", '12/sin(pi/4)', '12/tan(pi/4)', r'12\sqrt2', '12', 'el cateto contiguo'),
       (r"Un ángulo de $30^\circ$ y la hipotenusa, de 30 cm.", None, None, None, None, None)]
s16 = []
for t, h, o, ht, ot, nm in C16:
    if h is None:
        eq('30*sin(pi/6)', 15); eq('30*cos(pi/6)', '15*sqrt(3)')
        s16.append(r"Cateto opuesto: $30\sin30^\circ=" + Rm(r'15\ \text{cm}') + r"$; \ contiguo: $30\cos30^\circ=" + Rm(r'15\sqrt3\ \text{cm}') + "$."); continue
    eq(h, ht.replace(r'\frac{10\sqrt3}{3}', '10*sqrt(3)/3').replace(r'\frac{5\sqrt3}{3}', '5*sqrt(3)/3').replace(r'7\sqrt2', '7*sqrt(2)').replace(r'12\sqrt2', '12*sqrt(2)'))
    eq(o, ot.replace(r'\frac{5\sqrt3}{3}', '5*sqrt(3)/3').replace(r'2\sqrt3', '2*sqrt(3)').replace(r'6\sqrt3', '6*sqrt(3)'))
    s16.append(r"Hipotenusa: $" + Rm(ht + r'\ \text{cm}') + r"$; \ " + nm + r": $" + Rm(ot + r'\ \text{cm}') + "$.")
E18 = [(r'\sin30^\circ+\cos60^\circ', '1', 1), (r'\tg45^\circ-2\sin^245^\circ', '0', 0), (r'\sin60^\circ\cos30^\circ-\sin30^\circ\cos60^\circ', r'\frac12', .5),
       (r'\tg60^\circ\cdot\tg30^\circ', '1', 1), (r'(\sin45^\circ+\cos45^\circ)^2', '2', 2), (r'\cos^230^\circ-\sin^230^\circ', r'\frac12', .5)]
v18 = [sin(30) + cos(60), tan(45) - 2 * sin(45) ** 2, sin(60) * cos(30) - sin(30) * cos(60), tan(60) * tan(30), (sin(45) + cos(45)) ** 2, cos(30) ** 2 - sin(30) ** 2]
for (_, _, v), w in zip(E18, v18): ap(w, v)
# antenes (fitxa del departament, exercici 9)
ant = r'''\begin{center}\begin{tikzpicture}[scale=0.62]
\coordinate (A) at (0,0); \coordinate (P) at (2.3,0); \coordinate (B) at (2.3,4); \coordinate (C) at (9.2,0); \coordinate (Q) at (12.2,0); \coordinate (D) at (12.2,3); \coordinate (E) at (13.9,0);
\draw[muted] (-0.6,0)--(14.6,0);
\draw[accent, line width=1.6pt] (P)--(B) (Q)--(D);
\draw[navy, dashed] (A)--(B)--(C)--(D)--(E);
\foreach \n/\p in {A/below,P/below,C/below,Q/below,E/below,B/above,D/above} \node[\p,font=\small] at (\n) {$\n$};
\node[left,font=\small] at (2.3,2) {100 m}; \node[left,font=\small] at (12.2,1.4) {75 m};
\draw (0.8,0) arc (0:60:0.8); \node[font=\scriptsize] at (1.15,0.4) {$60^\circ$};
\draw (8.2,0) arc (180:150:1); \node[font=\scriptsize] at (7.7,0.3) {$30^\circ$};
\draw (12.2,2.2) arc (270:225:0.8); \node[font=\scriptsize] at (11.7,1.9) {$45^\circ$};
\draw (12.2,2.2) arc (270:300:0.8); \node[font=\scriptsize] at (12.75,1.85) {$30^\circ$};
\end{tikzpicture}\end{center}'''
ant_v = dict(AB='200*sqrt(3)/3', AP='100*sqrt(3)/3', BC='200', PC='100*sqrt(3)', DC='75*sqrt(2)', CQ='75', DE='50*sqrt(3)', QE='25*sqrt(3)')
eq(ant_v['AB'], '100/sin(pi/3)'); eq(ant_v['AP'], '100/tan(pi/3)'); eq(ant_v['BC'], '100/sin(pi/6)'); eq(ant_v['PC'], '100/tan(pi/6)')
eq(ant_v['DC'], '75/cos(pi/4)'); eq(ant_v['CQ'], '75*tan(pi/4)'); eq(ant_v['DE'], '75/cos(pi/6)'); eq(ant_v['QE'], '75*tan(pi/6)')
AE = sp.nsimplify('100*sqrt(3)/3 + 100*sqrt(3) + 75 + 25*sqrt(3)')
eq(AE, '75 + 475*sqrt(3)/3')
S.append(("Razones trigonométricas de 30°, 45° y 60°", [
 (1, r"Completa la tabla siguiente sin calculadora, de manera exacta:" + tab15 % (('& & & & ',) * 3), tab15 % tuple(' & '.join('$%s$' % x for x in row) for row in rows15)),
 (1, r"En cada triángulo rectángulo se conocen un ángulo agudo y un lado. Calcula los otros dos lados de manera exacta:" + items(*[t for t, *_ in C16]), items(*s16)),
 (1, r"Calcula sin calculadora:" + tasks(3, ['$%s$' % t for t, _, _ in E18]), tasks(3, [R(x) for _, x, _ in E18])),
 (2, r"Sin utilizar el teorema de Pitágoras, calcula la altura de un triángulo equilátero de 8 cm de lado y la diagonal de un cuadrado de 5 cm de lado.",
     r"Altura: $8\sin60^\circ=8\cdot\frac{\sqrt3}{2}=" + Rm(r'4\sqrt3\approx' + d2(8 * sin(60)) + r'\ \text{cm}') + r"$. \ Diagonal: $\cos45^\circ=\frac5d\Rightarrow d=\frac{5}{\sqrt2/2}=" + Rm(r'5\sqrt2\approx' + d2(5 * S2) + r'\ \text{cm}') + "$."),
 (2, r"Un hexágono regular se puede dividir en 6 triángulos equiláteros. Si el lado del hexágono mide 4 cm, calcula su apotema y su área de manera exacta.",
     r"La apotema es la altura de un triángulo equilátero de lado 4: $\text{ap}=4\sin60^\circ=" + Rm(r'2\sqrt3\ \text{cm}') + r"$. \ Área: $6\cdot\frac{4\cdot2\sqrt3}{2}=" + Rm(r'24\sqrt3\approx' + d2(24 * S3) + r'\ \text{cm}^2') + "$."),
 (3, r"Dos antenas de radio, de 100 m y 75 m, están sujetas al suelo como se indica en la figura. Calcula la longitud de cada tramo de cable y la distancia $\overline{AE}$. Da los resultados de manera exacta." + ant,
     r"Antena $PB$: $\overline{AB}=\frac{100}{\sin60^\circ}=" + Rm(r'\frac{200\sqrt3}{3}\ \text{m}') + r"$, $\overline{AP}=\frac{100}{\tg60^\circ}=\frac{100\sqrt3}{3}$; \ $\overline{BC}=\frac{100}{\sin30^\circ}=" + Rm(r'200\ \text{m}') +
     r"$, $\overline{PC}=\frac{100}{\tg30^\circ}=100\sqrt3$. \ Antena $QD$ (los ángulos son los de $D$): $\overline{DC}=\frac{75}{\cos45^\circ}=" + Rm(r'75\sqrt2\ \text{m}') + r"$, $\overline{CQ}=75\tg45^\circ=75$; \ $\overline{DE}=\frac{75}{\cos30^\circ}=" +
     Rm(r'50\sqrt3\ \text{m}') + r"$, $\overline{QE}=75\tg30^\circ=25\sqrt3$. \ $\overline{AE}=\frac{100\sqrt3}{3}+100\sqrt3+75+25\sqrt3=" + Rm(r'75+\frac{475\sqrt3}{3}\approx' + d2(float(AE)) + r'\ \text{m}') + "$."),
]))

# =====================================================================
# 4. Relacions fonamentals
def others(kind, v):
    v = sp.nsimplify(v)
    if kind == 'sin': s = v; c = sp.sqrt(1 - s ** 2)
    elif kind == 'cos': c = v; s = sp.sqrt(1 - c ** 2)
    else: c = 1 / sp.sqrt(1 + v ** 2); s = v * c
    s, c = sp.radsimp(sp.simplify(s)), sp.radsimp(sp.simplify(c))
    return s, c, sp.radsimp(sp.simplify(s / c))
NM = {'sin': r'\sin\alpha', 'cos': r'\cos\alpha', 'tan': r'\tg\alpha'}
def oth(kind, v):
    s, c, t = others(kind, v)
    out = []
    for k, x in (('sin', s), ('cos', c), ('tan', t)):
        if k != kind: out.append('$%s=%s$' % (NM[k], Rm(Ld(x))))
    return ', \\ '.join(out)
E22 = [('sin', '7/25'), ('sin', '12/37'), ('sin', '11/61'), ('cos', '20/29'), ('cos', '12/13'), ('sin', '3/8'), ('cos', '1/3'), ('sin', '15/34'), ('cos', '2/5'), ('sin', '4/7')]
ex22 = [others(k, v) for k, v in E22]
eq(ex22[0][1], '24/25'); eq(ex22[5][2], '3*sqrt(55)/55'); eq(ex22[6][0], '2*sqrt(2)/3'); eq(ex22[7][1], '7*sqrt(19)/34'); eq(ex22[7][2], '15*sqrt(19)/133')
for (k, v), (s, c, t) in zip(E22, ex22): eq(s ** 2 + c ** 2, 1); eq(t, s / c); assert s > 0 and c > 0
E23 = ['5/12', '3/4', '5/3', '5/13', '5/8', '3', '1']
ex23 = [others('tan', v) for v in E23]
eq(ex23[3][1], '13*sqrt(194)/194'); eq(ex23[4][0], '5*sqrt(89)/89'); eq(ex23[5][0], '3*sqrt(10)/10')
def tlv(v): return r'\frac{%s}{%s}' % tuple(v.split('/')) if '/' in v else v
E24 = [('cos', .1357), ('cos', .9531), ('cos', .2864), ('sin', .1827), ('sin', .9542), ('sin', .4531)]
def oth_d(k, v):
    o = math.sqrt(1 - v * v); s, c = (v, o) if k == 'sin' else (o, v)
    return ('$\\cos\\alpha\\approx%s$' % Rm(d4(c)) if k == 'sin' else '$\\sin\\alpha\\approx%s$' % Rm(d4(s))) + ', \\ $\\tg\\alpha\\approx%s$' % Rm(d4(s / c))
ap(math.sqrt(1 - .1357 ** 2), 0.9907, 1e-4); ap(math.sqrt(1 - .1827 ** 2), 0.9832, 1e-4); ap(math.sqrt(1 - .9542 ** 2), 0.2992, 1e-3)
# existència d'un angle
def exists(kind, a, b):
    a, b = sp.nsimplify(a), sp.nsimplify(b)
    if kind == 'sc': return sp.simplify(a ** 2 + b ** 2 - 1) == 0
    if kind == 'ct': return sp.simplify(1 + b ** 2 - 1 / a ** 2) == 0
    return sp.simplify(1 + 1 / b ** 2 - 1 / a ** 2) == 0
P25 = [('sc', '7/25', '11/25', r'\frac{49}{625}+\frac{121}{625}=\frac{170}{625}\neq1'), ('sc', '7/13', '12/13', r'\frac{49}{169}+\frac{144}{169}=\frac{193}{169}\neq1'),
       ('sc', 'sqrt(5)/5', '2*sqrt(5)/5', r'\frac{5}{25}+\frac{20}{25}=1'), ('sc', '3/5', '4/5', r'\frac{9}{25}+\frac{16}{25}=1'),
       ('st', '7/11', '6/11', r'\cos\alpha=\sqrt{1-\tfrac{49}{121}}=\tfrac{6\sqrt2}{11}\ \text{y}\ \tfrac{\sin\alpha}{\cos\alpha}=\tfrac{7}{6\sqrt2}\neq\tfrac{6}{11}'),
       ('ct', '5/13', '1', r'1^2+1=2\neq\tfrac{169}{25}=\tfrac{1}{\cos^2\alpha}'), ('ct', 'sqrt(3)/2', 'sqrt(3)/3', r'\tfrac39+1=\tfrac43=\tfrac{1}{3/4}'),
       ('ct', '3/5', '7/5', r'\tfrac{49}{25}+1=\tfrac{74}{25}\neq\tfrac{25}{9}')]
E25t = {'sc': (r'\sin\alpha', r'\cos\alpha'), 'st': (r'\sin\alpha', r'\tg\alpha'), 'ct': (r'\cos\alpha', r'\tg\alpha')}
def tv(s): return sp.latex(sp.nsimplify(s))
q25, s25 = [], []
for k, a, b, why in P25:
    e = exists(k, a, b)
    q25.append('$%s=%s$ \\ y \\ $%s=%s$' % (E25t[k][0], tv(a), E25t[k][1], tv(b)))
    s25.append('$%s$: \\rest{%s}' % (why, 'sí que hay' if e else 'no hay ninguno'))
assert [exists(k, a, b) for k, a, b, _ in P25] == [False, False, True, True, False, False, True, False]
P26 = [('ct', .1736, .4663), ('ct', .9397, .3640), ('sc', .1485, .2588), ('ct', .7313, .9325), ('sc', .2754, .6691)]
def ex_d(k, a, b):
    if k == 'sc': L_, R_ = a * a + b * b, 1
    else: L_, R_ = 1 + b * b, 1 / (a * a)
    return L_, R_, abs(L_ - R_) <= 0.002 * max(1, R_)
q26, s26 = [], []
for k, a, b in P26:
    L_, R_, e = ex_d(k, a, b)
    q26.append('$%s=%s$ \\ y \\ $%s=%s$' % (E25t[k][0], d4(a), E25t[k][1], d4(b)))
    if k == 'sc': s26.append('$%s^2+%s^2\\approx%s$: \\rest{%s}' % (d4(a), d4(b), d4(L_), 'sí' if e else 'no'))
    else: s26.append('$%s^2+1\\approx%s$, \\ $\\frac{1}{%s^2}\\approx%s$: \\rest{%s}' % (d4(b), d4(L_), d4(a), d4(R_), 'sí' if e else 'no'))
assert [ex_d(*p)[2] for p in P26] == [False, True, False, True, False]
S.append(("Relaciones fundamentales", [
 (1, r"Sabiendo que el ángulo $\alpha$ es agudo, calcula, en cada caso, sus otras razones trigonométricas de manera exacta:" + tasks(5, ['$%s=%s$' % (NM[k], tlv(v)) for k, v in E22])
     + recorda(r"$\sin^2\alpha+\cos^2\alpha=1$, \quad $\tg\alpha=\dfrac{\sin\alpha}{\cos\alpha}$, \quad $\tg^2\alpha+1=\dfrac{1}{\cos^2\alpha}$."),
     tasks(2, [oth(k, v) for k, v in E22])),
 (2, r"Si el ángulo $\alpha$ es agudo, calcula, en cada caso, el seno y el coseno del ángulo de manera exacta:" + tasks(7, [r'$\tg\alpha=%s$' % tlv(v) for v in E23]),
     tasks(2, [oth('tan', v) for v in E23])),
 (1, r"Sabiendo que el ángulo $\alpha$ es agudo, calcula las otras dos razones (con cuatro decimales):" + tasks(3, ['$%s=%s$' % (NM[k], d4(v)) for k, v in E24]),
     tasks(2, [oth_d(k, v) for k, v in E24])),
 (2, r"Comprueba si hay algún ángulo que tenga estas razones trigonométricas:" + tasks(2, q25), tasks(1, s25)),
 (2, r"Comprueba si estos pares de razones trigonométricas (redondeadas a cuatro decimales) pueden ser del mismo ángulo:" + tasks(2, q26)
     + recorda(r"con decimales redondeados, los dos miembros de la relación pueden diferir un poco en la última cifra."),
     tasks(1, s26)),
 (3, r"Utiliza las relaciones fundamentales para demostrar estas igualdades:" + tasks(1, [r"$\dfrac{1}{\tg^2\alpha}+1=\dfrac{1}{\sin^2\alpha}$", r"$(1+\tg^2\alpha)\cdot\cos^2\alpha=1$", r"$\sin\alpha\cdot\cos\alpha\cdot\tg\alpha+\cos^2\alpha=1$"]),
     tasks(1, [r"Dividimos $\sin^2\alpha+\cos^2\alpha=1$ entre $\sin^2\alpha$: $1+\dfrac{\cos^2\alpha}{\sin^2\alpha}=\dfrac{1}{\sin^2\alpha}$, y $\dfrac{\cos^2\alpha}{\sin^2\alpha}=\dfrac{1}{\tg^2\alpha}$.",
               r"$(1+\tg^2\alpha)\cos^2\alpha=\cos^2\alpha+\dfrac{\sin^2\alpha}{\cos^2\alpha}\cos^2\alpha=\cos^2\alpha+\sin^2\alpha=1$.",
               r"$\sin\alpha\cos\alpha\dfrac{\sin\alpha}{\cos\alpha}+\cos^2\alpha=\sin^2\alpha+\cos^2\alpha=1$."])),
]))
for a_ in (0.3, 0.7, 1.2):
    ap(1 / math.tan(a_) ** 2 + 1, 1 / math.sin(a_) ** 2); ap((1 + math.tan(a_) ** 2) * math.cos(a_) ** 2, 1); ap(math.sin(a_) * math.cos(a_) * math.tan(a_) + math.cos(a_) ** 2, 1)

# =====================================================================
# 5. Resolució de triangles rectangles (notació del departament: Â = 90°, a és la hipotenusa)
t28 = []
# a) b = 4, B = 30
a_a, c_a = 4 / sin(30), 4 / tan(30); ap(a_a, 8); ap(c_a, 4 * S3)
t28.append(r"$\hat C=" + Rm('60^\\circ') + r"$, \ $a=\frac{4}{\sin30^\circ}=" + Rm(r'8\ \text{m}') + r"$, \ $c=\frac{4}{\tg30^\circ}=" + Rm(r'4\sqrt3\approx' + d2(c_a) + r'\ \text{m}') + "$")
# b) a = 7, b = 5
c_b = math.sqrt(49 - 25); B_b = asin(5 / 7); ap(c_b, 2 * math.sqrt(6))
t28.append(r"$c=\sqrt{7^2-5^2}=" + Rm(r'2\sqrt6\approx' + d2(c_b) + r'\ \text{m}') + r"$, \ $\sin\hat B=\frac57\Rightarrow\hat B\approx" + Rm(dms(B_b)) + r"$, \ $\hat C\approx" + Rm(dms(90 - B_b)) + "$")
# c) a = 10, B = 40
t28.append(r"$\hat C=" + Rm('50^\\circ') + r"$, \ $b=10\sin40^\circ\approx" + Rm(d2(10 * sin(40)) + r'\ \text{m}') + r"$, \ $c=10\cos40^\circ\approx" + Rm(d2(10 * cos(40)) + r'\ \text{m}') + "$")
# d) c = 5, sin C = 0,25
a_d = 5 / .25; b_d = math.sqrt(a_d ** 2 - 25); C_d = asin(.25); ap(b_d, 5 * math.sqrt(15))
t28.append(r"$a=\frac{5}{0{,}25}=" + Rm(r'20\ \text{cm}') + r"$, \ $b=\sqrt{20^2-5^2}=" + Rm(r'5\sqrt{15}\approx' + d2(b_d) + r'\ \text{cm}') + r"$, \ $\hat C\approx" + Rm(dms(C_d)) + r"$, \ $\hat B\approx" + Rm(dms(90 - C_d)) + "$")
esc = acos(1.2 / 3); omb = atan(20 / 25); iso = atan(10 / 9); pend = 480 / 3000; avio = asin(2160 / 18410); compas = 2 * 12 * sin(25)
amic_AC, amic_AB = 120 / tan(37), 120 / sin(37)
S.append(("Resolución de triángulos rectángulos", [
 (1, r"Resuelve los triángulos rectángulos siguientes. En todos, $\hat A=90^\circ$; por tanto, $a$ es la hipotenusa." + tasks(2, [r"$b=4$ m, \ $\hat B=30^\circ$", r"$a=7$ m, \ $b=5$ m", r"$a=10$ m, \ $\hat B=40^\circ$", r"$c=5$ cm, \ $\sin\hat C=0{,}25$"]),
     tasks(1, t28)),
 (1, r"Calcula la altura $h$, trazada desde el vértice $B$, de cada triángulo $ABC$:" + tasks(2, [r"$\overline{AB}=18$ cm y $\hat A=62^\circ$.", r"$\overline{BC}=28$ cm y $\hat C=35^\circ$."]),
     tasks(2, [r"$h=18\sin62^\circ\approx" + Rm(d2(18 * sin(62)) + r'\ \text{cm}') + "$", r"$h=28\sin35^\circ\approx" + Rm(d2(28 * sin(35)) + r'\ \text{cm}') + "$"])),
 (1, r"Una escalera de 3 m está apoyada en una pared. ¿Qué ángulo forma la escalera con el suelo si la base está a 1,2 m de la pared?",
     r"$\cos\alpha=\frac{1{,}2}{3}=0{,}4\Rightarrow\alpha\approx" + Rm(dms(esc)) + "$"),
 (1, r"Una torre de 20 m de altura proyecta una sombra de 25 m de longitud. Calcula la inclinación de los rayos solares en ese momento.",
     r"$\tg\alpha=\frac{20}{25}=0{,}8\Rightarrow\alpha\approx" + Rm(dms(omb)) + "$"),
 (2, r"En un triángulo isósceles, el lado desigual mide 18 m y la altura, 10 m. ¿Cuánto miden sus ángulos?",
     r"La altura lo divide en dos triángulos rectángulos de catetos 9 y 10: $\tg\hat B=\frac{10}{9}\Rightarrow$ ángulos iguales $\approx" + Rm(dms(iso)) + r"$; \ ángulo desigual $\approx180^\circ-2\cdot" + dms(iso) + "=" + Rm(dms(180 - 2 * iso)) + "$."),
 (2, r"En una ruta de montaña, una señal indica una altitud de 785 m. Tres kilómetros más adelante (en horizontal), la altitud es de 1\,265 m. Halla la pendiente media de la ruta y el ángulo que forma con la horizontal.",
     r"Desnivel: $1265-785=480$ m. Pendiente: $\frac{480}{3000}=" + Rm(r'0{,}16=16\,\%') + r"$. \ Ángulo: $\tg^{-1}0{,}16\approx" + Rm(dms(atan(pend))) + "$."),
 (2, r"Un avión que está a punto de aterrizar desciende 2\,160 m al recorrer una distancia de 18,41 km. ¿Cuál es el ángulo $\alpha$ con el que desciende?",
     r"La distancia recorrida es la hipotenusa: $\sin\alpha=\frac{2\,160}{18\,410}\Rightarrow\alpha\approx" + Rm(dms(avio)) + "$."),
 (2, r"Los brazos de un compás, que miden 12 cm, forman un ángulo de $50^\circ$. ¿Cuál es el radio de la circunferencia que se puede trazar con esa abertura?",
     r"El triángulo es isósceles: la altura divide el ángulo en dos de $25^\circ$. \ $r=2\cdot12\sin25^\circ\approx" + Rm(d2(compas) + r'\ \text{cm}') + "$."),
 (2, r"Dos amigos salen del punto $A$. Uno se dirige al punto $B$ y el otro al punto $C$, siguiendo trayectorias rectilíneas que forman entre sí un ángulo de $37^\circ$. Si los puntos $B$ y $C$ están separados 120 m y la dirección $BC$ es perpendicular a la dirección $AC$, ¿cuántos metros recorre uno de los amigos más que el otro?",
     r"El ángulo recto está en $C$: $\overline{AC}=\frac{120}{\tg37^\circ}\approx" + d2(amic_AC) + r"$ m, \ $\overline{AB}=\frac{120}{\sin37^\circ}\approx" + d2(amic_AB) + r"$ m. Diferencia: $\approx" + Rm(d2(amic_AB - amic_AC) + r'\ \text{m}') + "$."),
]))
ap(compas, 10.1428, 1e-4)

# =====================================================================
# 6. Problemes de trigonometria
def dob(mode, a, b, d):
    x = d * tan(b) / (tan(a) - tan(b)) if mode == 's' else d * tan(b) / (tan(a) + tan(b))
    return x, x * tan(a)
x37, h37 = dob('s', 35, 20, 200); ap(x37 * tan(35), (x37 + 200) * tan(20))
x38, h38 = dob('s', 46, 33, 100)
x39, h39 = dob('s', 76, 45, 480)
x40, h40 = dob('s', 50, 40, 5)
x41, h41 = dob('o', 36, 12, 75); ap(x41 * tan(36), (75 - x41) * tan(12))
x42, h42 = dob('o', 60, 40, 140); corda = h42 / sin(60) + h42 / sin(40)
# antena (Trigonometria II, exercici 5): A = 60°, C = 30°, AC = 126 m
xA, hA = dob('o', 60, 30, 126); ap(xA, 31.5); ap(hA, 63 * S3 / 2)
eq('63*sqrt(3)/2', '31.5*tan(pi/3)'); eq('63', '31.5/cos(pi/3)'); eq('63*sqrt(3)', '(126-31.5)/cos(pi/6)')
llum = r'''\begin{center}\begin{tikzpicture}[scale=0.032]
\draw[navy, line width=1.2pt] (-10,0)--(150,0); \foreach \x in {-6,4,...,146} \draw[navy] (\x,0)--++(4,4);
\coordinate (P) at (0,0); \coordinate (Q) at (140,0); \coordinate (L) at (%.2f,-%.2f);
\draw[muted, line width=0.9pt] (P)--(L)--(Q); \draw[muted, dashed] (L)--(%.2f,0);
\fill[accent] (L) circle (2.6);
\draw (12,0) arc (0:-60:12); \node[font=\scriptsize] at (19,-9) {$60^\circ$};
\draw (128,0) arc (180:220:12); \node[font=\scriptsize] at (117,-7) {$40^\circ$};
\draw[<->, muted] (0,14)--(140,14); \node[above, font=\small] at (70,14) {140 cm};
\end{tikzpicture}\end{center}''' % (x42, h42, x42)
antena = r'''\begin{center}\begin{tikzpicture}[scale=0.055]
\coordinate (A) at (0,0); \coordinate (C) at (126,0); \coordinate (H) at (31.5,0); \coordinate (B) at (31.5,54.56);
\draw[muted] (-6,0)--(132,0); \draw[navy] (A)--(B)--(C); \draw[accent, line width=1.6pt] (H)--(B);
\node[left] at (A) {$A$}; \node[right] at (C) {$C$}; \node[above] at (B) {$B$};
\draw (9,0) arc (0:60:9); \node[font=\scriptsize] at (13,6) {$60^\circ$};
\draw (114,0) arc (180:150:12); \node[font=\scriptsize] at (104,3.5) {$30^\circ$};
\draw[<->, muted] (0,-6)--(126,-6); \node[below, font=\small] at (63,-6) {126 m};
\end{tikzpicture}\end{center}'''
tunel = r'''\begin{center}\begin{tikzpicture}[scale=0.11]
\coordinate (A) at (0,0); \coordinate (P) at ($(A)+(-30:25)$); \coordinate (Q) at ($(P)+(10,0)$); \coordinate (B) at ($(Q)+(-50:30)$);
\draw[navy, line width=1.6pt, line join=round] (A)--(P)--(Q)--(B);
\draw[muted, dashed] (P)--++(-7,0) (B)--++(-8,0);
\node[above left] at (A) {$A$}; \node[below right] at (B) {$B$};
\node[above right, font=\small] at ($(A)!0.5!(P)$) {25 m}; \node[above, font=\small] at ($(P)!0.5!(Q)$) {10 m}; \node[right, font=\small] at ($(Q)!0.5!(B)+(0.6,0)$) {30 m};
\draw ($(P)+(-4,0)$) arc (180:150:4); \node[font=\scriptsize] at ($(P)+(-6.5,1.4)$) {$30^\circ$};
\draw ($(B)+(-4,0)$) arc (180:130:4); \node[font=\scriptsize] at ($(B)+(-6.5,2.4)$) {$50^\circ$};
\end{tikzpicture}\end{center}'''
prof = 25 * sin(30) + 30 * sin(50)
camp = r'''\begin{center}\begin{tikzpicture}[scale=0.055]
\fill[teal!15] (0,0) rectangle (100,60); \draw[navy, line width=1pt] (0,0) rectangle (100,60);
\draw[navy!50] (50,0)--(50,60) (50,30) circle (9);
\coordinate (A) at (50,0); \coordinate (B) at (100,27.5); \coordinate (C) at (100,32.5);
\draw[accent, line width=0.9pt] (A)--(B) (A)--(C); \fill (A) circle (0.9) (B) circle (0.9) (C) circle (0.9);
\node[below] at (A) {$A$}; \node[right] at (B) {$B$}; \node[right] at (C) {$C$};
\node[font=\scriptsize] at (84,23) {$\alpha$};
\draw[<->, muted] (0,64)--(100,64); \node[above, font=\small] at (50,64) {100 m};
\draw[<->, muted] (-4,0)--(-4,60); \node[left, font=\small] at (-4,30) {60 m};
\end{tikzpicture}\end{center}'''
alpha_camp = atan(32.5 / 50) - atan(27.5 / 50)
pent_ap = 5 / tan(36); pent_S = 5 * 6 * 6 * sin(72) / 2
iso1_h = 2.5 / tan(27.5); iso2_l = 17 / sin(25); iso2_h = 17 / tan(25)
rombe_S = 144 * sin(43); rombe_ang = 2 * atan(6 / 4); rombe_l = math.sqrt(52)
par_h = 10 * sin(35); par_p = 10 * cos(35); par_d = math.sqrt(par_h ** 2 + (15 - par_p) ** 2); par_S = 150 * sin(35)
tun_h = 245 * sin(57); tun_x = 245 * cos(57); tun_AB = math.sqrt(tun_h ** 2 + (658 - tun_x) ** 2)
carrer = 10 * cos(45) + 10 * cos(30)
S.append(("Problemas de trigonometría", [
 (2, r"Desde cierto lugar se ve el punto más alto de una torre con un ángulo de elevación de $35^\circ$. Si retrocedemos 200 m, se ve la misma torre con un ángulo de $20^\circ$. Calcula la altura de la torre.",
     r"$h=x\tg35^\circ=(x+200)\tg20^\circ\Rightarrow x=\dfrac{200\tg20^\circ}{\tg35^\circ-\tg20^\circ}\approx" + d2(x37) + r"$ m; \ $h\approx" + Rm(d2(h37) + r'\ \text{m}') + "$."),
 (2, r"Para calcular la altura de un edificio se miden los ángulos de elevación desde dos puntos alineados con el pie del edificio y situados a una distancia de 100 m el uno del otro. ¿Cuál es la altura del edificio si los ángulos son $33^\circ$ y $46^\circ$?",
     r"Desde el punto más próximo el ángulo es mayor: $h=x\tg46^\circ=(x+100)\tg33^\circ\Rightarrow x\approx" + d2(x38) + r"$ m; \ $h\approx" + Rm(d2(h38) + r'\ \text{m}') + "$."),
 (2, r"Para medir la altura de una montaña se miden los ángulos de elevación desde dos puntos alineados con la cima, situados a una distancia de 480 m el uno del otro y a una altitud de 1\,200 m sobre el nivel del mar. ¿Cuál es la altura de la montaña si los ángulos son $45^\circ$ y $76^\circ$?",
     r"$h=x\tg76^\circ=(x+480)\tg45^\circ\Rightarrow x\approx" + d2(x39) + r"$ m, \ $h\approx" + d2(h39) + r"$ m sobre los puntos de observación. Altitud de la cima: $1200+h\approx" + Rm(d2(1200 + h39) + r'\ \text{m}') + "$."),
 (2, r"Para hallar la altura a la que se encuentra un globo, Rosa se coloca en un punto $B$, y yo en un punto $A$, a 5 metros de ella, de manera que $A$, $B$ y el pie $C$ de la vertical del globo quedan alineados ($B$ entre $A$ y $C$). Si desde $A$ veo el globo con un ángulo de $40^\circ$ y Rosa lo ve con un ángulo de $50^\circ$, ¿a qué altura se encuentra el globo?",
     r"$h=x\tg50^\circ=(x+5)\tg40^\circ\Rightarrow x\approx" + d2(x40) + r"$ m; \ $h\approx" + Rm(d2(h40) + r'\ \text{m}') + "$."),
 (2, r"Un avión vuela entre dos ciudades, $A$ y $B$, que están a 75 km la una de la otra. Las visuales desde $A$ y desde $B$ hacia el avión forman con la horizontal ángulos de $36^\circ$ y $12^\circ$, respectivamente. Calcula la altura a la que vuela el avión y las distancias a las que se encuentra de $A$ y de $B$ (el avión y las ciudades están en el mismo plano vertical).",
     r"Las ciudades están a lados opuestos: $h=x\tg36^\circ=(75-x)\tg12^\circ\Rightarrow x\approx" + d2(x41) + r"$ km; \ $h\approx" + Rm(d2(h41) + r'\ \text{km}') +
     r"$. \ Distancias: $\frac{h}{\sin36^\circ}\approx" + Rm(d2(h41 / sin(36)) + r'\ \text{km}') + r"$ de $A$ y $\frac{h}{\sin12^\circ}\approx" + Rm(d2(h41 / sin(12)) + r'\ \text{km}') + "$ de $B$."),
 (2, r"Queremos colgar una lámpara del techo de una habitación con una cuerda atada en dos puntos del techo separados 140 cm, de manera que los ángulos entre la cuerda y el techo sean de $60^\circ$ y $40^\circ$. ¿Cuál será la longitud total de la cuerda? ¿A qué distancia del techo quedará la lámpara?" + llum,
     r"$h=x\tg60^\circ=(140-x)\tg40^\circ\Rightarrow x\approx" + d2(x42) + r"$ cm; \ la lámpara queda a $h\approx" + Rm(d2(h42) + r'\ \text{cm}') + r"$ del techo. \ Cuerda: $\frac{h}{\sin60^\circ}+\frac{h}{\sin40^\circ}\approx" + Rm(d2(corda) + r'\ \text{cm}') + "$."),
 (2, r"Una antena de radio está sujeta al suelo por dos cables de acero, como indica la figura. Calcula, de manera exacta, la altura de la antena, la longitud de los cables y el ángulo $\widehat{ABC}$." + antena,
     r"$h=x\tg60^\circ=(126-x)\tg30^\circ\Rightarrow\sqrt3\,x=\frac{126-x}{\sqrt3}\Rightarrow x=31{,}5$ m. \ Altura: $" + Rm(r'\frac{63\sqrt3}{2}\approx' + d2(hA) + r'\ \text{m}') +
     r"$. \ Cables: $\overline{AB}=\frac{31{,}5}{\cos60^\circ}=" + Rm(r'63\ \text{m}') + r"$, \ $\overline{BC}=\frac{94{,}5}{\cos30^\circ}=" + Rm(r'63\sqrt3\approx' + d2(63 * S3) + r'\ \text{m}') + r"$. \ $\widehat{ABC}=180^\circ-60^\circ-30^\circ=" + Rm('90^\\circ') + "$."),
 (2, r"Una escalera de bomberos de 10 m de longitud se ha fijado en un punto de una calle. Si se apoya sobre una de las fachadas, forma con el suelo un ángulo de $45^\circ$, y si se apoya sobre la otra fachada, el ángulo es de $30^\circ$. ¿Cuál es la anchura de la calle?",
     r"$10\cos45^\circ+10\cos30^\circ=5\sqrt2+5\sqrt3\approx" + Rm(d2(carrer) + r'\ \text{m}') + "$"),
 (2, r"Una escalera para acceder a un túnel tiene la forma y las dimensiones de la figura. Calcula la profundidad a la que está el punto $B$ respecto del punto $A$." + tunel,
     r"$25\sin30^\circ+30\sin50^\circ\approx12{,}5+" + d2(30 * sin(50)) + r"\approx" + Rm(d2(prof) + r'\ \text{m}') + "$ (el tramo horizontal no cuenta)."),
 (2, r"Polígonos regulares:" + items(r"¿Cuánto mide la apotema de un pentágono regular de 10 cm de lado?", r"Calcula el área de un pentágono regular inscrito en una circunferencia de 6 cm de radio."),
     items(r"$\tg36^\circ=\frac{5}{\text{ap}}\Rightarrow\text{ap}=\frac{5}{\tg36^\circ}\approx" + Rm(d2(pent_ap) + r'\ \text{cm}') + "$",
           r"Son 5 triángulos isósceles de lados 6 y 6 y ángulo $72^\circ$: altura $6\sin72^\circ$; \ $S=5\cdot\frac{6\cdot6\sin72^\circ}{2}\approx" + Rm(d2(pent_S) + r'\ \text{cm}^2') + "$")),
 (2, r"Triángulos isósceles:" + items(r"La base de un triángulo isósceles mide 5 cm y el ángulo opuesto a esa base es de $55^\circ$. Calcula la altura y el área del triángulo.",
                                    r"El lado desigual de un triángulo isósceles mide 34 cm y el ángulo opuesto, $50^\circ$. Calcula el perímetro del triángulo y su área."),
     items(r"$h=\frac{2{,}5}{\tg27{,}5^\circ}\approx" + Rm(d2(iso1_h) + r'\ \text{cm}') + r"$; \ $S=\frac{5h}{2}\approx" + Rm(d2(5 * iso1_h / 2) + r'\ \text{cm}^2') + "$",
           r"Lados iguales: $\frac{17}{\sin25^\circ}\approx" + d2(iso2_l) + r"$ cm; \ $P\approx" + Rm(d2(34 + 2 * iso2_l) + r'\ \text{cm}') + r"$; \ $h=\frac{17}{\tg25^\circ}\approx" + d2(iso2_h) + r"$ cm, \ $S\approx" + Rm(d2(17 * iso2_h) + r'\ \text{cm}^2') + "$")),
 (2, r"Rombos:" + items(r"Calcula el área de un rombo de 12 cm de lado sabiendo que uno de sus ángulos mide $43^\circ$.", r"Halla los ángulos de un rombo cuyas diagonales miden 12 cm y 8 cm. Calcula también su perímetro y su área."),
     items(r"$S=12\cdot12\sin43^\circ\approx" + Rm(d2(rombe_S) + r'\ \text{cm}^2') + "$",
           r"Las diagonales se cortan perpendicularmente en el punto medio: $\tg\frac{\alpha}{2}=\frac64\Rightarrow\alpha\approx" + Rm(dms(rombe_ang)) + r"$ y $\beta\approx" + Rm(dms(180 - rombe_ang)) +
           r"$; \ lado $\sqrt{6^2+4^2}=2\sqrt{13}$, \ $P=" + Rm(r'8\sqrt{13}\approx' + d2(4 * rombe_l) + r'\ \text{cm}') + r"$; \ $S=\frac{12\cdot8}{2}=" + Rm(r'48\ \text{cm}^2') + "$")),
 (3, r"Calcula la longitud de la diagonal menor y el área de un paralelogramo de lados 10 cm y 15 cm, sabiendo que uno de sus ángulos mide $35^\circ$.",
     r"Trazando la altura sobre el lado de 15 cm: $h=10\sin35^\circ\approx" + d2(par_h) + r"$, proyección $10\cos35^\circ\approx" + d2(par_p) + r"$. \ Diagonal menor: $\sqrt{h^2+(15-" + d2(par_p) + r")^2}\approx" +
     Rm(d2(par_d) + r'\ \text{cm}') + r"$. \ Área: $15\cdot h\approx" + Rm(d2(par_S) + r'\ \text{cm}^2') + "$."),
 (3, r"Para construir un túnel de $A$ hasta $B$ se localiza una roca $C$ visible desde los dos puntos. Se miden las distancias $\overline{AC}=245$ m y $\overline{BC}=658$ m, y el ángulo $\widehat{ACB}=57^\circ$. ¿Cuál será la longitud del túnel?",
     r"Trazamos la altura desde $A$ sobre $BC$: $h=245\sin57^\circ\approx" + d2(tun_h) + r"$ m, $\overline{CH}=245\cos57^\circ\approx" + d2(tun_x) + r"$ m, $\overline{HB}\approx" + d2(658 - tun_x) +
     r"$ m. \ $\overline{AB}=\sqrt{h^2+\overline{HB}^2}\approx" + Rm(d2(tun_AB) + r'\ \text{m}') + "$."),
 (3, r"Calcula el ángulo de tiro $\alpha$ del jugador que está en el punto $A$, en el centro de la línea de banda, si la portería $BC$ mide 5 m y está centrada en la línea de fondo." + camp,
     r"La portería va de 27,5 m a 32,5 m de altura sobre la línea de banda y $A$ está a 50 m de la línea de fondo. Ángulo de $AB$ con la línea de banda: $\tg^{-1}\frac{27{,}5}{50}\approx" + dms(atan(.55)) + r"$; \ ángulo de $AC$: $\tg^{-1}\frac{32{,}5}{50}\approx" + dms(atan(.65)) + r"$. \ $\alpha\approx" + Rm(dms(alpha_camp)) + "$."),
]))
ap(prof, 35.4813, 1e-4); ap(carrer, 15.7313, 1e-4)

# =====================================================================
# 7. Raons d'un angle qualsevol
T52 = [120, 220, 135, 300, 240, 75]
def quad(d): d %= 360; return ['I', 'II', 'III', 'IV'][int(d // 90)]
tab52 = r'''\begin{center}\renewcommand{\arraystretch}{1.35}\begin{tabular}{|c|C{2.2cm}|C{2.2cm}|C{2.2cm}|C{2cm}|}\hline $\alpha$ & $\sin\alpha$ & $\cos\alpha$ & $\tg\alpha$ & \textbf{Cuadrante}\\\hline %s\end{tabular}\end{center}'''
t52q = tab52 % ''.join(r'$%d^\circ$ & & & & \\\hline ' % d for d in T52)
t52s = tab52 % ''.join(r'$%d^\circ$ & %s & %s & %s & %s\\\hline ' % (d, R(d4(sin(d))), R(d4(cos(d))), R(d4(tan(d))), R(r'\text{%s}' % quad(d))) for d in T52)
E54 = [(r'3\sin270^\circ-2\cos180^\circ', '-1', 3 * sin(270) - 2 * cos(180)), (r'\cos0^\circ+\sin180^\circ-\tg180^\circ', '1', cos(0) + sin(180) - tan(180)),
       (r'\sin90^\circ\cdot\cos360^\circ', '1', sin(90) * cos(360)), (r'2\cos90^\circ-\sin270^\circ', '1', 2 * cos(90) - sin(270))]
for _, a, b in E54: ap(b, float(a))
# entrega 1 i nous
s55a = math.sqrt(1 - .49); ap(s55a, 0.71414, 1e-4)
eq('-sqrt(10)/10', '-1/sqrt(1+9)'); eq('3*sqrt(10)/10', '(-3)*(-sqrt(10)/10)')
c19 = math.sqrt(1 - .34 ** 2)
A57 = [(r'\sin x=-\frac12', [210, 330], lambda x: sin(x) + .5), (r'\tg x=-1', [135, 315], lambda x: tan(x) + 1),
       (r'\cos x=0{,}8', [acos(.8), 360 - acos(.8)], lambda x: cos(x) - .8), (r'\sin x=0{,}9', [asin(.9), 180 - asin(.9)], lambda x: sin(x) - .9)]
for _, xs, f in A57:
    for x in xs: ap(f(x) + 1, 1)
    # cap altre angle entre 0 i 360 (pas de mig grau)
    roots_ = [k / 2 for k in range(720) if (f(k / 2) * f(k / 2 + .5) < 0 and abs(f(k / 2 + .5)) > 1e-12 and min(abs(f(k / 2)), abs(f(k / 2 + .5))) < 0.1) or abs(f(k / 2)) < 1e-12]
    assert len(roots_) == 2, roots_
def volta(a):
    """a = k·360° + b, amb 0 <= b < 360"""
    k, b = a // 360, a % 360
    co = '' if k == 1 else '-' if k == -1 else '%d\\cdot' % k
    return '%d^\\circ=%s360^\\circ+%d^\\circ' % (a, co, b)
def angs(xs): return ', \\ '.join(R(dms(x)) for x in sorted(xs))
red59 = [(1750, 310), (1920, 120), (-800, 280), (3825, 225)]
for a, b in red59: assert a % 360 == b
S.append(("Razones trigonométricas de un ángulo cualquiera", [
 (1, r"Utiliza la calculadora para calcular las razones trigonométricas de estos ángulos (con cuatro decimales) e indica en qué cuadrante está cada uno:" + t52q, t52s),
 (1, r"Responde:" + tasks(1, [r"Si $\sin\alpha=-0{,}8$, ¿en qué cuadrante puede estar el ángulo $\alpha$?", r"Si $\cos\beta=-0{,}3$, ¿en qué cuadrante puede estar el ángulo $\beta$?", r"Si $\tg\gamma=-1{,}5$, ¿en qué cuadrante puede estar el ángulo $\gamma$?"]),
     tasks(3, [r"\rest{III o IV}", r"\rest{II o III}", r"\rest{II o IV}"])),
 (1, r"Calcula sin calculadora:" + tasks(2, ['$%s$' % t for t, _, _ in E54]), tasks(4, [R(a) for _, a, _ in E54])),
 (2, r"Calcula las otras razones trigonométricas del ángulo en cada caso:" + tasks(2, [r"$\cos\alpha=0{,}7$ \ y \ $\alpha$ en el primer cuadrante.", r"$\tg\beta=-3$ \ y \ $\beta$ en el segundo cuadrante.",
                                                                                     r"$\sin\gamma=-\frac35$ \ y \ $\gamma$ en el tercer cuadrante.", r"$\cos\delta=\frac{5}{13}$ \ y \ $\delta$ en el cuarto cuadrante."]),
     tasks(1, [r"$\sin\alpha=\sqrt{1-0{,}49}\approx" + Rm(d4(s55a)) + r"$, \ $\tg\alpha\approx" + Rm(d4(s55a / .7)) + "$",
               r"$\frac{1}{\cos^2\beta}=9+1=10$, \ $\cos\beta=" + Rm(r'-\frac{\sqrt{10}}{10}') + r"$ (negativo en el II), \ $\sin\beta=\tg\beta\cdot\cos\beta=" + Rm(r'\frac{3\sqrt{10}}{10}') + "$",
               r"$\cos\gamma=-\sqrt{1-\frac{9}{25}}=" + Rm(r'-\frac45') + r"$ (negativo en el III), \ $\tg\gamma=\frac{-3/5}{-4/5}=" + Rm(r'\frac34') + "$",
               r"$\sin\delta=-\sqrt{1-\frac{25}{169}}=" + Rm(r'-\frac{12}{13}') + r"$ (negativo en el IV), \ $\tg\delta=" + Rm(r'-\frac{12}{5}') + "$"])),
 (2, r"Calcula las razones trigonométricas de $\alpha$ sabiendo que $\sin\alpha=0{,}34$. ¿Cuántos casos hay?",
     r"$\cos^2\alpha=1-0{,}34^2=0{,}8844\Rightarrow\cos\alpha=\pm" + d4(c19) + r"$. Como el seno es positivo, $\alpha$ puede ser del I o del II cuadrante: \ " +
     r"I: $\cos\alpha\approx" + Rm(d4(c19)) + r"$, $\tg\alpha\approx" + Rm(d4(.34 / c19)) + r"$ \ ($\alpha\approx" + dms(asin(.34)) + r"$); \ II: $\cos\alpha\approx" + Rm('-' + d4(c19)) + r"$, $\tg\alpha\approx" + Rm('-' + d4(.34 / c19)) + r"$ \ ($\alpha\approx" + dms(180 - asin(.34)) + "$)."),
 (2, r"Halla los dos ángulos de $[0^\circ,360^\circ)$ que cumplen cada condición:" + tasks(4, ['$%s$' % t for t, _, _ in A57])
     + recorda(r"la calculadora da un solo ángulo. El otro es $180^\circ-x$ (seno), $360^\circ-x$ (coseno) o $x+180^\circ$ (tangente)."),
     tasks(2, [angs(xs) for _, xs, _ in A57])),
 (2, r"Un ángulo $\beta$ tal que $0^\circ<\beta<360^\circ$ verifica $\sin\beta=-\sin30^\circ$ y $\cos\beta=\cos30^\circ$. ¿A qué cuadrante pertenece? ¿Cuánto mide?",
     r"Seno negativo y coseno positivo: \rest{cuarto cuadrante}. \ $\beta=360^\circ-30^\circ=" + Rm('330^\\circ') + "$."),
 (1, r"¿A qué ángulo entre $0^\circ$ y $360^\circ$ corresponde cada uno de estos ángulos?" + tasks(4, ['$%d^\\circ$' % a for a, _ in red59]),
     tasks(2, ['$%s$: \\ %s' % (volta(a), R('%d^\\circ' % b)) for a, b in red59])),
]))
assert sin(330) < 0 and cos(330) > 0 and abs(sin(330) + .5) < 1e-12

# =====================================================================
# 8. Reducció al primer quadrant
E61 = [155, 240, 390, 225, 1920, -30]
def redu(b):
    b0 = b % 360; q = int(b0 // 90)
    a = [b0, 180 - b0, b0 - 180, 360 - b0][q]
    sg = [('', '', ''), ('', '-', '-'), ('-', '-', ''), ('-', '', '-')][q]
    rel = ['', '180^\\circ-%d^\\circ' % a, '180^\\circ+%d^\\circ' % a, '360^\\circ-%d^\\circ' % a][q]
    for f, s_ in zip((sin, cos, tan), sg):
        ap(f(b), (-1 if s_ else 1) * f(a))
    return b0, a, sg, rel
EXA = {30: (r'\frac12', r'\frac{\sqrt3}{2}', r'\frac{\sqrt3}{3}'), 45: (r'\frac{\sqrt2}{2}', r'\frac{\sqrt2}{2}', '1'), 60: (r'\frac{\sqrt3}{2}', r'\frac12', r'\sqrt3')}
def sol_red(b, exact=True):
    b0, a, sg, rel = redu(b)
    parts = []
    if b >= 360 or b < 0: parts.append('$%s$' % volta(b))
    if rel: parts.append('$%d^\\circ=%s$' % (b0, rel))
    pre = '; \\ '.join(parts) + ': \\ ' if parts else ''
    fb = '(%d^\\circ)' % b if b < 0 else '%d^\\circ' % b
    if exact and a in EXA:
        vals = [s_ + v if v != '0' else v for s_, v in zip(sg, EXA[a])]
        for f, v in zip((sin, cos, tan), vals): ap(f(b), float(sp.nsimplify(v.replace(r'\frac{\sqrt3}{2}', 'sqrt(3)/2').replace(r'\frac{\sqrt2}{2}', 'sqrt(2)/2').replace(r'\frac{\sqrt3}{3}', 'sqrt(3)/3').replace(r'\frac12', '1/2').replace(r'\sqrt3', 'sqrt(3)'))))
        return pre + r'$\sin=%s$, $\cos=%s$, $\tg=%s$' % tuple(Rm(v) for v in vals)
    return pre + r'$\sin%s=%s$, $\cos%s=%s$, $\tg%s=%s$' % (fb, Rm(sg[0] + r'\sin%d^\circ' % a), fb, Rm(sg[1] + r'\cos%d^\circ' % a), fb, Rm(sg[2] + r'\tg%d^\circ' % a))
E62 = [-40, 385, -185, 835, 934]
E63 = [145, 215, 325, 55, -35, 395]
s35, c35, t35 = .57, .82, .70
def v63(b):
    if b == 55: return (c35, s35, 1 / t35)
    b0, a, sg, _ = redu(b); assert a == 35
    return tuple((-1 if s_ else 1) * v for s_, v in zip(sg, (s35, c35, t35)))
for b in E63:
    vv = v63(b)
    for f, v in zip((sin, cos, tan), vv): ap(f(b), v, 0.012)
S.append(("Reducción al primer cuadrante", [
 (1, r"Utiliza la relación entre los ángulos para calcular, de manera exacta:" + tasks(1, [r"Las razones de $135^\circ$, sabiendo las de $45^\circ$.", r"Las razones de $240^\circ$, sabiendo las de $60^\circ$.", r"Las razones de $-30^\circ$, sabiendo las de $30^\circ$."]),
     tasks(1, [sol_red(135), sol_red(240), sol_red(-30)])),
 (2, r"Calcula las razones trigonométricas (seno, coseno y tangente) de los ángulos siguientes, relacionándolas con las de un ángulo del primer cuadrante. Si el ángulo del primer cuadrante es $30^\circ$, $45^\circ$ o $60^\circ$, da su valor exacto." + tasks(6, ['$%d^\\circ$' % b for b in E61]),
     tasks(1, [sol_red(b) for b in E61])),
 (2, r"Expresa las razones trigonométricas de los ángulos siguientes en función de las de un ángulo del primer cuadrante. ¡Cuidado con los signos!" + tasks(5, ['$%d^\\circ$' % b for b in E62]),
     tasks(1, [sol_red(b, False) for b in E62])),
 (2, r"Sabiendo que $\sin35^\circ\approx0{,}57$, $\cos35^\circ\approx0{,}82$ y $\tg35^\circ\approx0{,}70$, calcula sin calculadora las razones trigonométricas de:" + tasks(6, ['$%d^\\circ$' % b for b in E63]),
     tasks(2, [r'$%d^\circ$: \ $\sin\approx%s$, $\cos\approx%s$, $\tg\approx%s$' % ((b,) + tuple(Rm(d2(v)) for v in v63(b))) for b in E63])),
 (3, r"Expresa las razones trigonométricas de los ángulos siguientes en función de las de un ángulo $\alpha$ tal que $0^\circ\le\alpha\le45^\circ$:" + tasks(4, [r'$120^\circ$', r'$430^\circ$', r'$-800^\circ$', r'$180^\circ$'])
     + recorda(r"si el ángulo del primer cuadrante es mayor de $45^\circ$, pasa al complementario: $\sin(90^\circ-\alpha)=\cos\alpha$, $\cos(90^\circ-\alpha)=\sin\alpha$, $\tg(90^\circ-\alpha)=\dfrac{1}{\tg\alpha}$."),
     tasks(1, [r"$120^\circ=180^\circ-60^\circ$: \ $\sin120^\circ=\sin60^\circ=" + Rm(r'\cos30^\circ') + r"$, \ $\cos120^\circ=-\cos60^\circ=" + Rm(r'-\sin30^\circ') + r"$, \ $\tg120^\circ=-\tg60^\circ=" + Rm(r'-\dfrac{1}{\tg30^\circ}') + "$",
               r"$430^\circ=360^\circ+70^\circ$: \ $\sin430^\circ=\sin70^\circ=" + Rm(r'\cos20^\circ') + r"$, \ $\cos430^\circ=" + Rm(r'\sin20^\circ') + r"$, \ $\tg430^\circ=" + Rm(r'\dfrac{1}{\tg20^\circ}') + "$",
               r"$-800^\circ=-3\cdot360^\circ+280^\circ$ y $280^\circ=360^\circ-80^\circ$: \ $\sin(-800^\circ)=-\sin80^\circ=" + Rm(r'-\cos10^\circ') + r"$, \ $\cos(-800^\circ)=\cos80^\circ=" + Rm(r'\sin10^\circ') + r"$, \ $\tg(-800^\circ)=-\tg80^\circ=" + Rm(r'-\dfrac{1}{\tg10^\circ}') + "$",
               r"$\sin180^\circ=" + Rm(r'\sin0^\circ=0') + r"$, \ $\cos180^\circ=" + Rm(r'-\cos0^\circ=-1') + r"$, \ $\tg180^\circ=" + Rm(r'\tg0^\circ=0') + "$"])),
 (3, r"Simplifica: \ $\sin(180^\circ-\alpha)+\sin(180^\circ+\alpha)+\cos(360^\circ-\alpha)+\cos(180^\circ-\alpha)$.",
     r"$\sin\alpha-\sin\alpha+\cos\alpha-\cos\alpha=" + Rm('0') + "$"),
]))
ap(sin(120), cos(30)); ap(cos(120), -sin(30)); ap(tan(120), -1 / tan(30)); ap(sin(430), cos(20)); ap(cos(430), sin(20)); ap(tan(430), 1 / tan(20))
ap(sin(-800), -cos(10)); ap(cos(-800), sin(10)); ap(tan(-800), -1 / tan(10))
for a_ in (17, 52, 200):
    ap(sin(180 - a_) + sin(180 + a_) + cos(360 - a_) + cos(180 - a_) + 1, 1)

PRE = r'''\usetikzlibrary{calc}
\usepackage{enumitem}
\providecommand{\tg}{\operatorname{tg}}
'''
build(HERE, 5, "Trigonometría", S,
      "trigonometría, radianes, seno, coseno, tangente, relaciones fundamentales, triángulos rectángulos, circunferencia goniométrica, reducción al primer cuadrante",
      r"Resuélvelos en el cuaderno mostrando todos los pasos y haciendo un dibujo en los problemas. Usa la calculadora en modo \texttt{D} (grados) y da los ángulos en grados, minutos y segundos y las longitudes con dos decimales, salvo que el enunciado pida el resultado exacto. La ficha recoge los ejercicios de las fichas del departamento y añade otros nuevos.",
      r"Intenta resolver cada ejercicio antes de mirar su solución. Los ángulos se han redondeado al segundo y las longitudes, a la centésima (calculando siempre con los valores sin redondear). Puedes comprobar muchos resultados con las herramientas interactivas de los apuntes de la unidad.",
      PRE, lang='es')
