# Genera tN-apunts-teoria.tex per a les unitats 1-5 de 2n Batxillerat MII (Matrius i determinants, Sistemes d'equacions
# lineals, Vectors i aplicacions. Rectes, plans i feixos de plans, Problemes mètrics, Límits i continuïtat): apunts de
# teoria en PDF per a l'alumnat, a partir dels apunts interactius. Copia de ../2batx-ccss-t1/apunts.py (mateix disseny
# que els apunts de 2n Batx CCSS), amb els colors dels blocs d'Àlgebra (blau, U1-U2), Geometria (taronja, U3-U4) i
# Anàlisi (verd, U5). Llig les pàgines ja generades (text de cada idioma en <span data-l>, només es queda el triat):
#   U1, U2: materials/2batx-ccss/t1-..., t2-... (la còpia MII és idèntica però encara no té les 3 propietats noves de
#           la inversa: cal tornar a executar _eines/pau/mii/build.py quan es publique)
#   U3, U4, U5: materials/2batx-mii/t3-vectors-rectes-plans.html, t4-problemes-metrics.html, t5-limits-continuitat.html
# Deixa fora els ginys (i, per tant, tots els dibuixos 3D, que hi són dins), les caixes «Practica», el laboratori i
# l'autoavaluació. Les gràfiques de la U5 es redibuixen amb pgfplots a partir del diccionari FIGS d'app.js
# (_eines/apunts/2batx-mii-t5/app.js), com en ../2batx-ccss-t4/apunts.py.
# Ús: python3 apunts.py N [es]   (N = 1..5) → ../2batx-mii-tN/tN-apunts-teoria[-es].tex
#     i pdflatex dues vegades (per l'índex), amb logo-fentmates.pdf al costat.
import os, re, sys
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))

N = int(sys.argv[1])
ES = len(sys.argv) > 2 and sys.argv[2] == 'es'
LANG = 'es' if ES else 'va'
def T(va, es): return es if ES else va

ALG = dict(c='3D6AA0', cl='4E81BD', block=T("bloc d'Àlgebra: blau", 'bloque de Álgebra: azul'))
GEO = dict(c='DC7A29', cl='F79645', block=T('bloc de Geometria: taronja', 'bloque de Geometría: naranja'))
AN = dict(c='6A8A33', cl='7FA040', block=T("bloc d'Anàlisi: verd", 'bloque de Análisis: verde'))
U = {
 1: dict(ALG, src='2batx-ccss/t1-matrius-determinants.html', title=T('Matrius i determinants', 'Matrices y determinantes'),
         kw=T('matrius, operacions amb matrius, determinants, regla de Sarrus, adjunts, rang, matriu inversa, equacions matricials',
              'matrices, operaciones con matrices, determinantes, regla de Sarrus, adjuntos, rango, matriz inversa, ecuaciones matriciales')),
 2: dict(ALG, src='2batx-ccss/t2-sistemes-equacions.html', title=T("Sistemes d'equacions lineals", 'Sistemas de ecuaciones lineales'),
         kw=T('sistemes lineals, classificació, mètode de Gauss, expressió matricial, regla de Cramer, teorema de Rouché-Frobenius, discussió de sistemes, paràmetres',
              'sistemas lineales, clasificación, método de Gauss, expresión matricial, regla de Cramer, teorema de Rouché-Frobenius, discusión de sistemas, parámetros')),
 3: dict(GEO, src='2batx-mii/t3-vectors-rectes-plans.html', title=T('Vectors i aplicacions. Rectes, plans i feixos de plans', 'Vectores y aplicaciones. Rectas, planos y haces de planos'),
         short=T('Vectors, rectes i plans', 'Vectores, rectas y planos'),
         kw=T("vectors a l'espai, dependència lineal, bases, producte escalar, producte vectorial, producte mixt, equacions de la recta, equacions del pla, posicions relatives, feixos de plans",
              'vectores en el espacio, dependencia lineal, bases, producto escalar, producto vectorial, producto mixto, ecuaciones de la recta, ecuaciones del plano, posiciones relativas, haces de planos')),
 4: dict(GEO, src='2batx-mii/t4-problemes-metrics.html', title=T('Problemes mètrics', 'Problemas métricos'),
         kw=T('angles entre rectes i plans, distàncies, perpendicular comuna, projeccions, simètrics, àrees, volums, llocs geomètrics, pla mediador, plans bisectors, esfera',
              'ángulos entre rectas y planos, distancias, perpendicular común, proyecciones, simétricos, áreas, volúmenes, lugares geométricos, plano mediador, planos bisectores, esfera')),
 5: dict(AN, src='2batx-mii/t5-limits-continuitat.html', title=T('Límits i continuïtat', 'Límites y continuidad'),
         kw=T('límits, indeterminacions, límits trigonomètrics, infinitèsims equivalents, paràmetres, continuïtat, funcions a trossos, teorema de Bolzano, asímptotes',
              'límites, indeterminaciones, límites trigonométricos, infinitésimos equivalentes, parámetros, continuidad, funciones a trozos, teorema de Bolzano, asíntotas')),
 6: dict(AN, src='2batx-mii/t6-derivades.html', title=T("Càlcul de derivades. Derivabilitat d'una funció", 'Cálculo de derivadas. Derivabilidad de una función'),
         short=T('Derivades i derivabilitat', 'Derivadas y derivabilidad'),
         kw=T('derivada, taxa de variació, recta tangent, recta normal, regles de derivació, regla de la cadena, derivada logarítmica, derivació implícita, derivabilitat, funcions a trossos',
              'derivada, tasa de variación, recta tangente, recta normal, reglas de derivación, regla de la cadena, derivada logarítmica, derivación implícita, derivabilidad, funciones a trozos')),
 7: dict(AN, src='2batx-mii/t7-aplicacions-derivada.html', title=T('Aplicacions de la derivada', 'Aplicaciones de la derivada'),
         kw=T("monotonia, extrems relatius, curvatura, punts d'inflexió, teorema de Rolle, teorema del valor mitjà, regla de L'Hôpital, extrems absoluts, optimització",
              "monotonía, extremos relativos, curvatura, puntos de inflexión, teorema de Rolle, teorema del valor medio, regla de L'Hôpital, extremos absolutos, optimización")),
 8: dict(AN, src='2batx-mii/t8-representacio-funcions.html', title=T('Representació gràfica de funcions', 'Representación gráfica de funciones'),
         kw=T('domini, simetries, talls amb els eixos, asímptotes, monotonia, extrems, curvatura, representació gràfica',
              'dominio, simetrías, cortes con los ejes, asíntotas, monotonía, extremos, curvatura, representación gráfica')),
 9: dict(AN, src='2batx-mii/t9-integrals.html', title=T('Integrals', 'Integrales'),
         kw=T('primitiva, integral indefinida, integrals immediates, canvi de variable, integració per parts, integrals racionals, integral definida, regla de Barrow, àrees, volums',
              'primitiva, integral indefinida, integrales inmediatas, cambio de variable, integración por partes, integrales racionales, integral definida, regla de Barrow, áreas, volúmenes')),
 10: dict(c='684E88', cl='8064A1', block=T('bloc de Probabilitat: morat', 'bloque de Probabilidad: morado'),
         src='2batx-mii/t10-probabilitat.html', title=T('Probabilitat', 'Probabilidad'),
         kw=T('probabilitat, espai mostral, successos, regla de Laplace, taula de contingència, probabilitat condicionada, successos independents, diagrama d’arbre, probabilitat total, teorema de Bayes, distribució binomial, distribució normal',
              'probabilidad, espacio muestral, sucesos, regla de Laplace, tabla de contingencia, probabilidad condicionada, sucesos independientes, diagrama de árbol, probabilidad total, teorema de Bayes, distribución binomial, distribución normal')),
}[N]
SRC = os.path.join(HERE, '..', '..', '..', 'materials', U['src'])
OUTDIR = os.path.join(HERE, '..', '2batx-mii-t%d' % N)

# ---------- 1. HTML ----------
src = open(SRC, encoding='utf-8').read()
hero = re.search(r'<section class="hero">.*?<p>[^\n]*?<span data-l="%s">(.*?)</span>' % LANG, src, re.S).group(1)
tocnames = [re.search(r'<span data-l="%s">(.*?)</span>' % LANG, x).group(1)
            for x in re.findall(r'<span class="n">%d\.\d+</span>(.*?)<span class="ck">' % N, src)]
body = src[src.index('<article>') + len('<article>'):src.index('<section class="unit" id="lab">')]
body = re.sub(r'\\color\{#([0-9a-fA-F]{6})\}', r'\\color[HTML]{\1}', body)
if N == 3:  # la nota inicial només explica com funcionen els dibuixos 3D de la web
    body, k = re.subn(r'<p class="note"><span data-l="va"><span class="u-line">Com funcionen els dibuixos</span>.*?</p>', '', body, count=1, flags=re.S)
    assert k == 1
if N == 4:  # la nota «Abans de començar» fora (l'autor la va llevar en revisar, 23/11/2026)
    body, k = re.subn(r'<p class="note"><span data-l="va"><span class="u-line">Abans de començar</span>.*?</p>', '', body, count=1, flags=re.S)
    assert k == 1

def fix(a, b):
    global body
    assert body.count(a) == 1, a[:80]
    body = body.replace(a, b)

# ---------- 2. arbre DOM senzill ----------
VOID = {'input', 'br', 'img', 'hr'}
class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.a, self.kids, self.parent = tag, dict(attrs), [], parent
    def cls(self): return self.a.get('class', '').split()
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.root = Node('root', []); self.cur = self.root
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur); self.cur.kids.append(n)
        if tag not in VOID: self.cur = n
    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))
    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag: n = n.parent
        if n is not None and n.parent is not None: self.cur = n.parent
    def handle_data(self, d): self.cur.kids.append(d)
p = P(); p.feed(body); ROOT = p.root

# ---------- 3. figures ----------
# regla de Sarrus (els dos svg de .sarrus-fig): coordenades de l'svg (210 × 200, y cap avall)
def sarrus(col, paths, sign):
    s = r'\begin{tikzpicture}[x=0.0205cm,y=-0.0205cm,line join=round]'
    s += r'\draw[line width=0.9pt] (8,12)--(8,160) (202,12)--(202,160);'
    for ps in paths:
        s += r'\draw[%s,line width=1.6pt,opacity=0.85] %s;' % (col, '--'.join('(%d,%d)' % q for q in ps))
    for i in range(3):
        for j in range(3):
            s += r'\node[fill=white,fill opacity=0.8,text opacity=1,inner sep=1pt] at (%d,%d) {$a_{%d%d}$};' % (35 + 70 * j, 30 + 55 * i, i + 1, j + 1)
    s += r'\node[text=%s,font=\Large\bfseries] at (105,188) {$%s$};' % (col, sign)
    return s + r'\end{tikzpicture}'
SARRUS = (r'\begin{center}' + sarrus('fmok', [[(35, 30), (105, 85), (175, 140)], [(105, 30), (175, 85), (35, 140), (105, 30)], [(175, 30), (35, 85), (105, 140), (175, 30)]], '+')
          + r'\qquad\qquad' + sarrus('fmas', [[(175, 30), (105, 85), (35, 140)], [(105, 30), (35, 85), (175, 140), (105, 30)], [(35, 30), (175, 85), (105, 140), (35, 30)]], '-')
          + r'\end{center}')

# unitat 5: gràfiques (pgfplots), les mateixes de FIGS a _eines/apunts/2batx-mii-t5/app.js
def axis(v, body, w='6.4cm', h='4.6cm'):
    x0, x1, y0, y1 = v
    return (r'\begin{tikzpicture}\begin{axis}[fmaxis,width=%s,height=%s,xmin=%s,xmax=%s,ymin=%s,ymax=%s]%s\end{axis}\end{tikzpicture}'
            % (w, h, x0, x1, y0, y1, body))
def cv(e, a, b, n=160): return r'\addplot[fmcurve,domain=%s:%s,samples=%d]{%s};' % (a, b, n, e)
def va(x): return r'\draw[fmasy] ({axis cs:%s,0}|-{rel axis cs:0,0}) -- ({axis cs:%s,0}|-{rel axis cs:0,1});' % (x, x)
def ha(y): return r'\draw[fmasy] ({rel axis cs:0,0}|-{axis cs:0,%s}) -- ({rel axis cs:1,0}|-{axis cs:0,%s});' % (y, y)
def ln(a, b, m, n): return r'\addplot[fmasy,domain=%s:%s]{%s*x+%s};' % (a, b, m, n)
def pt(x, y, o=False): return r'\node[%s] at (axis cs:%s,%s) {};' % ('fmopen' if o else 'fmdot', x, y)
def gd(x): return r'\draw[fmguide] ({axis cs:%s,0}|-{rel axis cs:0,0}) -- ({axis cs:%s,0}|-{rel axis cs:0,1});' % (x, x)
def lb(x, y, t): return r'\node[anchor=west,font=\small] at (axis cs:%s,%s) {$%s$};' % (x, y, t)
SM = ('4.4cm', '3.8cm')
FIG = {
 'inf1': axis([-6, 6, -1, 3.2], cv('2*x^2/(x^2+1)', -6, 6) + ha(2)),
 'inf2': axis([-6, 4, -2, 6], cv('2^x-1', -6, 3) + ha(-1)),
 'inf3': axis([-6, 6, -6, 6], cv('x^3/10-x', -6, 6)),
 'inf4': axis([-10, 10, -2, 2], cv('sin(deg(x))', -10, 10, 300)),
 'inf5': axis([-4, 10, -1, 4], cv('sqrt(max(x-2,0))', 2, 10, 300) + pt(2, 0)),
 'inf6': axis([-5, 5, -1, 4], cv('sqrt(max(9-x^2,0))', -3, 3, 300) + pt(-3, 0) + pt(3, 0)),
 'grafG': axis([-4, 6, -4, 6], va(-1) + cv('-1/(x+1)', -4, -1.1, 300) + cv('x', -1, 2) + cv('4-(x-2)^2/2', 2, 6)
               + pt(-1, -1, True) + pt(1, 1, True) + pt(1, 3) + pt(2, 2, True) + pt(2, 4), '8cm', '6cm'),
 'tev': axis([-1, 3, -1, 4], gd(1) + cv('x/2+1', -1, 3) + pt(1, 1.5, True) + pt(1, 3) + lb(1.05, -0.6, 'a'), *SM),
 'tsf': axis([-1, 3, -1, 4], gd(1) + cv('x+1', -1, 1) + cv('x/2', 1, 3) + pt(1, 2, True) + pt(1, 0.5) + lb(1.05, -0.6, 'a'), *SM),
 'tsi': axis([-1, 3, -2, 5], va(1) + cv('1/(2*(1-x))', -1, 0.9, 300) + cv('x-2', 1, 3) + pt(1, -1) + lb(1.05, -1.6, 'a'), *SM),
 'tas': axis([-1, 3, -5, 5], va(1) + cv('1/(x-1)', -1, 0.8, 300) + cv('1/(x-1)', 1.2, 3, 300) + lb(1.05, -4.4, 'a'), *SM),
 'rat1': axis([-3, 5, -6, 6], va(2) + ha(1) + cv('(x+1)/(x-2)', -3, 1.75, 300) + cv('(x+1)/(x-2)', 2.25, 5, 300) + pt(1, -2, True)),
 'asV': axis([-5, 5, -6, 6], va(-2) + va(2) + ha(0) + cv('(x+1)/(x^2-4)', -5, -2.02, 600) + cv('(x+1)/(x^2-4)', -1.985, 1.985, 900) + cv('(x+1)/(x^2-4)', 2.02, 5, 600)),
 'asH': axis([-8, 8, -1.5, 4.5], ha(3) + cv('(3*x^2-1)/(x^2+2)', -8, 8, 200)),
 'asO': axis([-6, 8, -8, 12], va(1) + ln(-6, 8, 1, 1) + cv('(x^2+3)/(x-1)', -6, 0.7, 300) + cv('(x^2+3)/(x-1)', 1.3, 8, 300)),
 'asR': axis([-7, 6, -1, 7], ln(-7, 6, 1, 1) + ln(-7, 6, -1, -1) + cv('sqrt(max(x^2+2*x,0))', -7, -2, 400) + cv('sqrt(max(x^2+2*x,0))', 0, 6, 400) + pt(-2, 0) + pt(0, 0)),
 'asE': axis([-6, 6, -1, 6], va(0) + ha(1) + cv('exp(1/x)', -6, -0.05, 300) + cv('exp(1/x)', 0.17, 6, 400) + pt(0, 0, True)),
}
# unitats 6 i 7: gràfiques de FIGS (_eines/apunts/2batx-mii-t6/app.js i 2batx-mii-t7/app.js)
def tl(a, b, m, x0, y0, col='fmteal'): return r'\addplot[%s,line width=1.2pt,domain=%s:%s]{%s*(x-(%s))+(%s)};' % (col, a, b, m, x0, y0)
def tx(x, y, t, anc='center'): return r'\node[anchor=%s,font=\footnotesize,align=center] at (axis cs:%s,%s) {%s};' % (anc, x, y, t)
def mk(x, y, col): return r'\node[circle,fill=%s,draw=white,line width=0.8pt,inner sep=0pt,minimum size=7pt] at (axis cs:%s,%s) {};' % (col, x, y)
def cc(e, a, b, col, n=160): return r'\addplot[%s,line width=1.6pt,smooth,domain=%s:%s,samples=%d]{%s};' % (col, a, b, n, e)
def hz(y, a, b, col='fmteal'): return r'\addplot[%s,line width=1.2pt,domain=%s:%s]{%s};' % (col, a, b, y)
def pc(x, y, col='fmteal'): return r'\node[circle,fill=%s,inner sep=0pt,minimum size=5.5pt] at (axis cs:%s,%s) {};' % (col, x, y)
def sgt(m, x0, y0, d, col='fmmuted'):  # tros de tangent centrat en (x0, y0)
    return tl(x0 - d, x0 + d, m, x0, y0, col)
def _f7a(x): return x ** 3 / 3 - x ** 2 - 3 * x + 4
def _lag(x): return x ** 3 / 6 - x / 2 + 1
_la, _lb = -1, 2.5
_lm = (_lag(_lb) - _lag(_la)) / (_lb - _la)
_lc = (2 * (_lm + 0.5)) ** 0.5
def _ab(x): return x ** 3 - 6 * x ** 2 + 9 * x + 1
FIG.update({
 'tvm': axis([-0.5, 7, -2, 28], cv('-x^2+10*x', -0.5, 7) + tl(-0.5, 7, 6, 1, 9) + gd(1) + gd(3) + pt(1, 9) + pt(3, 21)
             + r'\draw[fmguide] (axis cs:1,9)--(axis cs:3,9);\draw[fmguide] (axis cs:3,9)--(axis cs:3,21);'
             + lb(1.05, -1.2, 'a') + lb(3.05, -1.2, 'b') + lb(3.1, 15, 'f(b)-f(a)') + lb(1.6, 7.3, 'b-a'), '8cm', '5.6cm'),
 'tan': axis([-1, 4, -0.5, 7], cv('x^2/2+1', -1, 4) + tl(-1, 4, 1, 1, 1.5) + tl(-1, 4, 2.5, 1, 1.5, 'fmsi') + tl(-1, 4, 1.6, 1, 1.5, 'fmsi')
             + pt(1, 1.5) + pt(4, 9) + pt(2.2, 3.42) + lb(0.45, 2.2, 'P') + lb(2.35, 2.15, T(r'\text{tangent}', r'\text{tangente}')), '6.4cm', '5cm'),
 'abs': axis([-3, 3, -1, 3], cv('abs(x)', -3, 3, 161) + tl(-3, 0, -1, 0, 0) + tl(0, 3, 1, 0, 0, 'fmsi') + pt(0, 0), *SM),
 'cbrt': axis([-3, 3, -2, 2], r'\addplot[fmcurve,domain=-3:3,samples=301]{sign(x)*abs(x)^(1/3)};' + gd(0) + pt(0, 0), *SM),
 'cusp': axis([-3, 3, -0.5, 2.5], r'\addplot[fmcurve,domain=-3:3,samples=301]{abs(x)^(2/3)};' + gd(0) + pt(0, 0), *SM),
 'norm': r'\begin{tikzpicture}\begin{axis}[fmaxis,axis equal image,width=6.4cm,xmin=-1.5,xmax=3.5,ymin=-1,ymax=3]'
         + cv('x^2/2', -1.5, 3.5) + tl(-1.5, 3.5, 1, 1, 0.5) + tl(-1.5, 3.5, -1, 1, 0.5, 'fmsi') + pt(1, 0.5)
         + tx(1.15, 0.15, '$P$', 'west') + tx(2.75, 2.2, '$t$', 'west') + tx(-0.6, 2.4, '$n$', 'east') + r'\end{axis}\end{tikzpicture}',
 'jump': axis([-1, 4, -1, 5], cv('x+1', -1, 1) + cv('x+2', 1, 4) + pt(1, 2) + pt(1, 3, True), *SM),
 'res': axis([-1, 3.6, -1, 10], cv('x+1', -1, 2) + cv('x^2-1', 2, 3.6) + tl(1, 2, 1, 2, 3) + tl(2, 3, 4, 2, 3, 'fmsi') + pt(2, 3), '7cm', '5.2cm'),
 'mono': axis([-3.2, 5.2, -6, 8], cc('x^3/3-x^2-3*x+4', -3.2, -1, 'fmok') + cc('x^3/3-x^2-3*x+4', -1, 3, 'fmas') + cc('x^3/3-x^2-3*x+4', 3, 5.2, 'fmok')
              + sgt(5, -2, _f7a(-2), 0.5, 'fmteal') + sgt(-4, 1, _f7a(1), 0.5, 'fmteal') + sgt(0, -1, _f7a(-1), 0.9, 'fmteal') + sgt(0, 3, -5, 0.9, 'fmteal')
              + mk(-1, round(_f7a(-1), 4), 'fmok') + mk(3, -5, 'fmas') + tx(-1, _f7a(-1) + 1.1, "$f'=0$") + tx(3, -6.1, "$f'=0$", 'south')
              + tx(-2.5, 4.6, r"\color{fmok}$f'>0$", 'west') + tx(1.6, 3.2, r"\color{fmas}$f'<0$", 'west'), '7cm', '5.4cm'),
 'cvx': axis([-2.6, 2.6, -1, 3], cc('x^2/2', -2.6, 2.6, 'fmteal') + sgt(-1, -1, 0.5, 0.8) + sgt(1.5, 1.5, 1.125, 0.6) + pt(-1, 0.5) + pt(1.5, 1.125)
             + tx(0, 2.5, r"$f''>0\ \ \cup$"), *SM),
 'ccv': axis([-2.6, 2.6, -1, 3], cc('-x^2/2+2', -2.6, 2.6, 'fmsi') + sgt(1, -1, 1.5, 0.8) + sgt(-1.5, 1.5, 0.875, 0.6) + pt(-1, 1.5) + pt(1.5, 0.875)
             + tx(0, 2.6, r"$f''<0\ \ \cap$"), *SM),
 'infl': axis([-2.6, 2.6, -2, 2], cc('x^3/3-x', -2.6, 0, 'fmsi') + cc('x^3/3-x', 0, 2.6, 'fmteal') + tl(-1.6, 1.6, -1, 0, 0, 'fmmuted') + mk(0, 0, 'fmgold')
              + tx(-1.8, 1.5, r'$\cap$') + tx(1.8, -1.4, r'$\cup$') + tx(0.15, 0.4, 'P.I.', 'west'), *SM),
 'rolle': axis([0, 6, -0.5, 4], cv('-(x-1)*(x-5)/2+1', 1, 5) + hz(1, 1, 5, 'fmsi') + hz(3, 1.8, 4.2) + pt(1, 1) + pt(5, 1) + pc(3, 3) + gd(3)
               + tx(1, 0.55, '$a$') + tx(5, 0.55, '$b$') + tx(3.15, 0.2, '$c$', 'west') + tx(3, 3.45, "$f'(c)=0$"), '6.4cm', '4.6cm'),
 'lag': axis([-1.6, 3, -0.5, 3.5], cv('x^3/6-x/2+1', _la, _lb) + tl(_la, _lb, round(_lm, 5), _la, round(_lag(_la), 5), 'fmsi')
             + tl(round(_lc - 1.3, 4), round(_lc + 1.3, 4), round(_lm, 5), round(_lc, 5), round(_lag(_lc), 5)) + pt(_la, round(_lag(_la), 4)) + pt(_lb, round(_lag(_lb), 4))
             + pc(round(_lc, 4), round(_lag(_lc), 4)) + gd(round(_lc, 4))
             + tx(_la, round(_lag(_la) - 0.4, 3), '$a$') + tx(_lb + 0.1, round(_lag(_lb) - 0.3, 3), '$b$', 'west') + tx(round(_lc + 0.1, 3), -0.25, '$c$', 'west'), '6.4cm', '4.8cm'),
 'absx': axis([-0.7, 4.7, -3, 8], cv('x^3-6*x^2+9*x+1', -0.3, 4.2) + gd(-0.3) + gd(4.2) + mk(-0.3, round(_ab(-0.3), 4), 'fmas') + mk(4.2, round(_ab(4.2), 4), 'fmok')
              + mk(1, 5, 'fmok') + mk(3, 1, 'fmas') + tx(1, 5.8, T('màx. rel.', 'máx. rel.')) + tx(3, 0.2, T('mín. rel.', 'mín. rel.'))
              + tx(4.1, round(_ab(4.2), 3), T('màx. abs.', 'máx. abs.'), 'east') + tx(-0.15, round(_ab(-0.3), 3), T('mín. abs.', 'mín. abs.'), 'west'), '6.4cm', '5cm'),
 'pw': axis([-4.5, 4.5, -1.6, 4], cv('x^2+4*x+3', -4.5, 0) + cv('3*exp(-x)', 0, 4.5) + ha(0) + pc(-1, 0) + pc(-3, 0) + mk(-2, -1, 'fmas') + mk(0, 3, 'fmok'), '6.4cm', '4.6cm'),
})

# unitats 7 i 8: gràfiques de l'estudi complet (data-sf). sf-mii.json conté el que calcula fullStudy() d'app.js
# (FM7/FM8 al navegador): finestra, domini, asímptotes, extrems, inflexions i talls. La corba es mostreja ací.
import json, math
SFD = json.load(open(os.path.join(HERE, 'sf-mii.json'), encoding='utf-8'))
def pyfun(s):
    t = s.replace('^', '**')
    t = re.sub(r'(\d)([a-z(])', r'\1*\2', t)
    t = re.sub(r'\)([a-z0-9(])', r')*\1', t)
    t = re.sub(r'\be\*\*', 'E**', t).replace('ln(', 'log(').replace('arctan(', 'atan(')
    ns = dict(sin=math.sin, cos=math.cos, tan=math.tan, log=math.log, sqrt=math.sqrt, atan=math.atan, abs=abs, E=math.e)
    def f(x):
        try:
            v = eval(t, ns, {'x': x})
            return v if isinstance(v, float) or isinstance(v, int) else None
        except (ValueError, ZeroDivisionError, OverflowError, TypeError):
            return None
    return f
def sfplot(s, w, h):
    d = SFD[s]; f = pyfun(s)
    x0, x1, y0, y1 = d['view']; R = y1 - y0; T_ = d['T']
    def per(xs):
        if not T_: return [x for x in xs if x0 <= x <= x1]
        return sorted({round(x + k * T_, 4) for x in xs for k in range(-4, 5) if x0 - 1e-6 <= x + k * T_ <= x1 + 1e-6})
    bad = set(per(d['av'] + d['ex']))
    br = sorted({x0, x1} | {b for b in bad if x0 < b < x1} | {e for o in d['iv'] for e in o[:2] if e is not None and x0 < e < x1 and not T_})
    body = ''
    for p, q in zip(br, br[1:]):
        if f((p + q) / 2) is None: continue
        pts = []
        n = 500
        for k in range(n + 1):
            x = p + (q - p) * (1 - math.cos(math.pi * k / n)) / 2
            if k in (0, n) and (x in bad or f(x) is None):
                x += (1 if k == 0 else -1) * (q - p) * 1e-6
            y = f(x)
            if y is None: continue
            pts.append('(%.5f,%.5f)' % (x, max(y0 - 2 * R, min(y1 + 2 * R, y))))
        body += r'\addplot[fmaccent,line width=1.6pt] coordinates {%s};' % ' '.join(pts)
    for x in per(d['av']): body += va(x)
    seen = set()
    for k in ('-1', '1'):
        o = d['side'][k]
        if o[0] == 'h' and ('h', o[1]) not in seen: seen.add(('h', o[1])); body += ha(o[1])
        if o[0] == 'o' and ('o', o[1], o[2]) not in seen: seen.add(('o', o[1], o[2])); body += ln(x0, x1, o[1], o[2])
    for x in per([e for e in d['ex'] if e not in d['av']]):  # forats
        y = f(x + 1e-7)
        if y is not None: body += pt(x, round(y, 4), True)
    for x in per(d['ox']): body += pc(x, 0)
    if d['oy'] is not None: body += pc(0, d['oy'])
    def rep(L):
        return [(round(x + k * T_, 4), y) + tuple(r) for x, y, *r in L for k in (range(-4, 5) if T_ else [0]) if x0 - 1e-6 <= x + k * T_ <= x1 + 1e-6]
    for x, y, *r in rep(d['ext']): body += mk(x, y, 'fmok' if r[0] == 'max' else 'fmas')
    for x, y, *r in rep(d['inf']): body += mk(x, y, 'fmgold')
    return axis([round(v, 4) for v in d['view']], body, w, h)
SF = {s: None for s in SFD}
# unitat 10 (com en ../2batx-ccss-t9/apunts.py): # diagrames de Venn (com venn() d'app.js: viewBox 320x210; regions 0 cap, 1 només A, 2 A∩B, 3 només B)
from fractions import Fraction
ON = 'fmaccent!55!white'
def venn(on, w=4.2, disj=False, cond=False):
    A, B = ((100, 108, 60), (220, 108, 60)) if disj else ((128, 108, 72), (192, 108, 72))
    def col(r):
        if cond: return {'2': 'fmaccent!60!white', '3': 'fmteal!35!white'}.get(r, 'white')
        return ON if r in on else 'white'
    c = lambda p: '(%d,%d) circle[radius=%d]' % p
    u = w / 320
    h = r'\begin{tikzpicture}[x=%.5fcm,y=-%.5fcm]' % (u, u)
    h += r'\fill[%s,rounded corners=%.2fcm] (10,10) rectangle (310,200);' % (col('0'), 12 * u)
    h += r'\fill[%s] %s;\fill[%s] %s;' % (col('1'), c(A), col('3'), c(B))
    if not disj: h += r'\begin{scope}\clip %s;\fill[%s] %s;\end{scope}' % (c(A), col('2'), c(B))
    h += r'\draw[fmmuted,line width=0.8pt,rounded corners=%.2fcm] (10,10) rectangle (310,200);' % (12 * u)
    h += r'\draw[black!85,line width=0.9pt] %s %s;' % (c(A), c(B))
    fs = r'\small' if w > 3.6 else r'\footnotesize'
    h += r'\node[font=%s\bfseries] at (%.1f,%.1f) {$A$};' % (fs, A[0] - A[2] * 0.86, A[1] - A[2] * 0.84)
    h += r'\node[font=%s\bfseries] at (%.1f,%.1f) {$B$};' % (fs, B[0] + B[2] * 0.86, B[1] - B[2] * 0.84)
    h += r'\node[font=\scriptsize,text=fmmuted] at (26,26) {$E$};'
    return h + r'\end{tikzpicture}'
# arbre de l'urna amb 3 R i 2 B, dues extraccions sense reemplaçament (data-fig="tree")
def tree():
    RB = {'R': 'fmball0', 'B': 'fmball1'}
    h = r'\begin{tikzpicture}[x=1.15cm,y=0.68cm,br/.style={fmmuted,line width=0.9pt},lb/.style={font=\footnotesize,inner sep=1.5pt}]'
    h += r'\node[circle,draw=fmmuted,fill=fmsurface,inner sep=0pt,minimum size=6pt] (o) at (0,0) {};'
    for c1, n1, y1 in [('R', 3, 2), ('B', 2, -2)]:
        h += r'\node[circle,fill=%s,inner sep=0pt,minimum size=9pt] (%s) at (1.9,%d) {};' % (RB[c1], c1, y1)
        h += r'\draw[br] (o)--(%s) node[lb,pos=0.5,%s] {$\frac{%d}{5}$};' % (c1, 'above left' if y1 > 0 else 'below left', n1)
        rest = {'R': 3, 'B': 2}; rest[c1] -= 1
        for c2, dy in [('R', 1), ('B', -1)]:
            y2 = y1 + dy; n2 = rest[c2]; k = c1 + c2; f = Fraction(n1 * n2, 20)
            h += r'\node[circle,fill=%s,inner sep=0pt,minimum size=9pt] (%s) at (3.8,%d) {};' % (RB[c2], k, y2)
            h += r'\draw[br] (%s)--(%s) node[lb,pos=0.5,%s] {$\frac{%d}{4}$};' % (c1, k, 'above' if dy > 0 else 'below', n2)
            h += r'\node[anchor=west,font=\scriptsize] at (4.15,%d) {$\frac{%d}{5}\cdot\frac{%d}{4}=\frac{%d}{%d}$};' % (y2, n1, n2, f.numerator, f.denominator)
    return h + r'\end{tikzpicture}'
CMP = [0]
def conv_vfig(n, w, center=True):
    cap = next((k for k in n.kids if not isinstance(k, str) and k.tag == 'figcaption'), None)
    if n.a.get('data-fig') == 'tree': pic = tree()
    else: pic = venn(n.a['data-venn'], w, bool(n.a.get('data-disj')), bool(n.a.get('data-cond')))
    capt = r'\par\smallskip{\centering\footnotesize\color{fmmuted}%s\par}' % text(cap).strip() if cap else ''
    if not center: capt = capt.replace(r'\color{fmmuted}', ' ')
    return ('{\\centering %s\\par}' % pic) + capt


# 5.7: el per què de sin x / x → 1 (svg de contingut-c07.html, ací amb l'eix y cap amunt)
SANDWICH = r'''\begin{tikzpicture}[x=0.034cm,y=0.034cm,line cap=round,font=\small]
  \fill[fmaccent,fill opacity=0.18] (0,0)--(120,0) arc[start angle=0,end angle=34.4,radius=120]--cycle;
  \draw[fmmuted!70,line width=0.9pt] (120,0) arc[start angle=0,end angle=90,radius=120];
  \draw[line width=0.8pt] (0,0)--(132,0); \draw[line width=0.9pt] (0,0)--(120,82.1);
  \draw[fmaccent,line width=1.8pt] (99,67.7)--(99,0);
  \draw[fmex,line width=1.8pt] (120,0)--(120,82.1);
  \foreach \p in {(0,0),(99,67.7),(120,0),(120,82.1)} \fill \p circle[radius=2.6];
  \node[below left] at (0,0) {$O$}; \node[below] at (120,0) {$A$}; \node[above left] at (99,67.7) {$P$}; \node[right] at (120,82.1) {$T$};
  \node[fmaccent,left] at (99,30) {$\sin x$}; \node[fmex,right] at (120,40) {$\tan x$}; \node at (110,29) {$x$};
\end{tikzpicture}'''

# ---------- 4. conversió a LaTeX ----------
UNI = {'→': r'$\to$', '∞': r'$\infty$', '≪': r'$\ll$', '≤': r'$\leq$', '≥': r'$\geq$', '−': '-', '○': r'$\circ$', '∄': r'$\nexists$',
       '✓': '', '✗': '', '✎': '', '✍': '', '🎓': '', '◉': '', '⚙': '', '⚠': '', '…': r'\dots{}', '×': r'$\times$', '≠': r'$\neq$', '±': r'$\pm$',
       '↗': r'$\nearrow$', '↘': r'$\searrow$', '∩': r'$\cap$', '∪': r'$\cup$', '–': '--', '⇒': r'$\Rightarrow$', '⟺': r'$\Leftrightarrow$',
       '←': r'$\leftarrow$', '∅': r'$\emptyset$', '●': r'$\bullet$', '₁': r'$_1$', '₂': r'$_2$', '₃': r'$_3$', '₄': r'$_4$',
       'ᵗ': r'$^t$', '⁻¹': r'$^{-1}$', '²': r'$^2$', '³': r'$^3$', '½': r'$\frac12$', '√': r'$\surd$', '∈': r'$\in$', '∀': r'$\forall$', '′': r"$'$", '″': r"$''$", '°': r'$^\circ$'}
MATH = re.compile(r'(\\\[.*?\\\]|\\\(.*?\\\))', re.S)
def esc(t):
    out = []
    for i, part in enumerate(MATH.split(t)):
        if i % 2:
            part = part.replace('&lt;', '<').replace('&gt;', '>')
            part = part.replace('✓', r'\checkmark').replace('″', "''").replace('′', "'")
            if part.startswith('\\('):
                part = ('$%s$' if IN_TABLE[0] else r'\fmm{%s}') % part[2:-2]
            out.append(part)
            continue
        part = part.replace('\\', r'\textbackslash{}')
        for a, b in [('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}'), ('~', r'\~{}'), ('^', r'\^{}')]:
            part = part.replace(a, b)
        part = part.replace(r'\textbackslash\{\}', r'\textbackslash{}')
        part = part.replace('l·l', r'\lgem{}').replace('L·L', r'\Lgem{}')
        for a, b in UNI.items(): part = part.replace(a, b)
        part = re.sub(r'\$\$', '', part)
        out.append(part)
    return ''.join(out)

IN_TABLE = [False]
BADGE = {'ok': 'fmok', 'ev': 'fmev', 'sf': 'fmsf', 'si': 'fmsi', 'as': 'fmas',
         'scd': 'fmok', 'sci': 'fmev', 'uni': 'fmok', 'inf': 'fmev', 'none': 'fmas', 'acot': 'fmok', 'nacot': 'fmsf', 'buida': 'fmas'}
def text(n): return ''.join(conv(k) for k in n.kids)
def plain(n):
    return ''.join(k if isinstance(k, str) else plain(k) for k in n.kids)
def items(n):
    return ''.join(r'\item ' + text(k).strip() + '\n' for k in n.kids if not isinstance(k, str) and k.tag == 'li')
def elems(n): return [k for k in n.kids if not isinstance(k, str)]

def conv(n):
    if isinstance(n, str):
        return esc(n) if n.strip() or ' ' in n else ''
    t, c = n.tag, n.cls()
    if n.a.get('data-l') and n.a['data-l'] != LANG: return ''
    if 'sarrus-fig' in c: return '\n' + SARRUS + '\n'
    if n.a.get('data-g'): return '\n\\begin{center}%s\\end{center}\n' % FIG.get(n.a['data-g'], r'\fbox{FIG %s}' % n.a['data-g'])
    if n.a.get('data-sf'): return '\n\\begin{center}%s\\end{center}\n' % sfplot(n.a['data-sf'], '6.4cm', '4.6cm')
    if 'sfig' in c:  # gràfiques dels exemples resolts, en una fila
        figs = elems(n); k = len(figs); w = 0.98 / k
        cell = lambda fg: sfplot(next(x for x in elems(fg) if x.a.get('data-sf')).a['data-sf'], '%.1fcm' % (17.5 * w), '%.1fcm' % (min(4.6, 13 * w))) + \
            r'\par{\footnotesize %s\par}' % ''.join(text(x) for x in elems(fg) if x.tag == 'figcaption').strip()
        return '\n\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{%.3f\linewidth}\centering %s\end{minipage}' % (w - 0.01, cell(fg)) for fg in figs) + '\\par\\medskip\n'
    if t == 'figure' and 'lfig' in c and any(not isinstance(k, str) and k.tag == 'svg' for k in n.kids):
        return '\n\\begin{center}%s\\end{center}\n' % SANDWICH
    if t == 'figure' and (n.a.get('data-venn') is not None or n.a.get('data-fig') == 'tree'):
        return '\n\\begin{center}%s\\end{center}\n' % conv_vfig(n, 4.6)
    if 'venn6' in c:
        figs = elems(n)
        per = 3 if len(figs) > 2 else 2
        rows = [figs[i:i + per] for i in range(0, len(figs), per)]
        return '\n\\begin{center}' + '\\\\[8pt]'.join(r'\hspace{0.03\linewidth}'.join(r'\begin{minipage}[t]{0.3\linewidth}\centering %s\end{minipage}' % conv_vfig(k, 4.4, False) for k in row) for row in rows) + '\\end{center}\n'
    if 'cmp' in c:
        cols = elems(n)
        box = r'\begin{tcolorbox}[enhanced,colback=fmsurface,colframe=fmmuted!35,arc=2.5mm,boxrule=0.6pt,left=2.5mm,right=2.5mm,top=1.5mm,bottom=1.5mm,before upper=\raggedright,equal height group=cmp%d]%s\end{tcolorbox}'
        CMP[0] += 1
        return '\n\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{0.488\linewidth}\vspace{0pt}%s\end{minipage}' % (box % (CMP[0], text(k).strip())) for k in cols) + '\\par\\medskip\n'
    if 'fig4' in c:
        figs = elems(n)
        w = 0.98 / min(len(figs), 4)
        return '\n\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{%.3f\linewidth}\centering %s\end{minipage}' % (w - 0.01, text(k)) for k in figs) + '\\par\\medskip\n'
    if 'hier' in c:
        parts = []
        for k in elems(n):
            if 'lv' in k.cls():
                sm = next(x for x in elems(k) if x.tag == 'small')
                rest = ''.join(conv(x) for x in k.kids if x is not sm)
                parts.append(r'\fmlevel{%s}{%s}' % (text(sm).strip(), rest.strip()))  # text() només agafa l'idioma triat
            else: parts.append(r'{\Large\color{fmaccent}$\ll$}')
        return '\n\\begin{center}' + r'\quad'.join(parts) + '\\end{center}\n'
    if 'liate' in c:  # ordre per a triar u en la integració per parts
        return '\n\\begin{center}' + r'\ {\color{fmaccent}$\rightarrow$}\ '.join(r'\fmchip{%s}' % text(k) for k in elems(n)) + '\\end{center}\n'
    if 'indet' in c:
        return '\n\\begin{center}' + r'\ '.join(r'\fmchip{%s}' % text(k) for k in elems(n)) + '\\end{center}\n'
    if 'formula-grid' in c:  # 4.x: quadre resum de les distàncies, en dues columnes
        IN_TABLE[0] = True
        cells = []
        for k in elems(n):
            b = next(x for x in elems(k) if x.tag == 'b')
            f = ''.join(conv(x) for x in k.kids if x is not b).strip()
            cells.append(r'\textbf{%s}:\ \ %s' % (text(b).strip(), f.replace('$', '$\\displaystyle ', 1)))
        IN_TABLE[0] = False
        rows = [' & '.join(cells[i:i + 2]) + r'\\[6pt]' for i in range(0, len(cells), 2)]
        return '\n\\begin{center}\\renewcommand{\\arraystretch}{1.6}\\begin{tabularx}{\\linewidth}{XX}\n%s\n\\end{tabularx}\\end{center}\n' % '\n'.join(rows)
    if t in ('input', 'select', 'button', 'svg', 'summary', 'label', 'option', 'script', 'style'): return ''
    if 'widget' in c or 'box' in c and 'pr' in c or 'steps-ctl' in c or 'sec-head' in c: return ''
    if t == 'section': return conv_section(n)
    if t == 'h3': return '\n\\Needspace{16\\baselineskip}\n\\subsection*{%s}\n' % text(n).strip()
    if 'box' in c:
        kind = [k for k in ('def', 'prop', 'ex', 'warn') if k in c][0]
        bh = next(k for k in elems(n) if 'bh' in k.cls())
        bb = next(k for k in elems(n) if 'bb' in k.cls())
        IN_TABLE[0] = True  # fórmules del títol com a $...$
        title = text(bh).strip()
        IN_TABLE[0] = False
        inner = text(bb).strip()
        return '\n\\Needspace{7\\baselineskip}\n\\begin{fm%s}{%s}\n%s\n\\end{fm%s}\n' % (kind, title, inner, kind)
    if 'note' in c:
        inner = text(n).strip()
        return '\n\\begin{fmnote}%s\\end{fmnote}\n' % inner if inner else ''
    if t == 'p':
        inner = text(n).strip()
        if not inner: return ''
        if 'key' in c: return '\n\\begin{center}\\colorbox{fmyellow!45}{\\parbox{0.9\\linewidth}{\\centering\\strut %s\\strut}}\\end{center}\n' % inner
        return '\n\n' + inner + '\n\n'
    if t == 'ul': return '\n\\begin{itemize}\n%s\\end{itemize}\n' % items(n)
    if t == 'ol':
        if 'ex-list' in c and 'alpha' in c: return '\n\\begin{enumerate}[label=\\textbf{\\alph*)},leftmargin=*]\n%s\\end{enumerate}\n' % items(n)
        if 'alpha' in c: return '\n\\begin{enumerate}[label=\\alph*)]\n%s\\end{enumerate}\n' % items(n)
        if 'ex-list' in c: return '\n\\begin{enumerate}[label=\\textbf{\\arabic*.},leftmargin=*]\n%s\\end{enumerate}\n' % items(n)
        return '\n\\begin{enumerate}\n%s\\end{enumerate}\n' % items(n)
    if t == 'li': return text(n)
    if t == 'br': return '\\newline '
    if t in ('strong', 'b'): return r'\textbf{%s}' % text(n)
    if t in ('em', 'i'): return r'\emph{%s}' % text(n)
    if t == 'u': return r'\underline{%s}' % text(n)
    if t == 'sup': return r'\textsuperscript{%s}' % text(n)
    if t == 'sub': return r'\textsubscript{%s}' % text(n)
    if t == 'code': return r'\texttt{%s}' % text(n)
    if t == 'small': return r'{\footnotesize %s}' % text(n)
    if t == 'span':
        if 'key' in c: return r'\fmkey{%s}' % text(n)
        if 'u-line' in c: return r'\fmuline{%s}' % text(n)
        if 'badge' in c: return r'\fmbadge{%s}{%s}' % (BADGE[c[1]], text(n))
        if 'pau' in c: return r'\fmpau{%s}' % text(n)
        if 'lt' in c: return r' $\ll$ '
        return text(n)
    if t == 'details':  # solucions curtes fora de les caixes «Practica»: es mostren
        inner = ''.join(conv(k) for k in n.kids if not (not isinstance(k, str) and k.tag == 'summary'))
        return '\n\n' + T(r'\textit{Solució:} ', r'\textit{Solución:} ') + inner.strip() + '\n\n'
    if 'steps' in c:
        return '\n' + ''.join(conv(k) for k in n.kids) + '\n'
    if 'step' in c: return '\n\n' + text(n).strip() + '\n\n'
    if t == 'h4': return '{\\color{fmnavy}\\bfseries %s}\\par\n' % text(n).strip()
    if 'ttl' in c: return r'{\centering %s\par}' % text(n)
    if t == 'figcaption': return r'{\centering\footnotesize %s\par}' % text(n)
    if t == 'figure' and 'ttl' in ' '.join(sum((k.cls() for k in elems(n)), [])): return text(n)
    if 'two' in c or 'pl-wrap' in c:
        cols = elems(n)
        out = []
        TWO[0] = True
        for i in range(0, len(cols), 2):
            pair = cols[i:i + 2]
            out.append('\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{0.48\linewidth}\vspace{0pt}\raggedright %s\end{minipage}' % conv_cell(k).strip() for k in pair) + '\\par\\medskip\n')
        TWO[0] = False
        return '\n' + ''.join(out)
    if t == 'table': return conv_table(n)
    return text(n)

TWO = [False]
def conv_cell(k): return conv(k) if k.tag == 'figure' else text(k)

def rows_of(n):
    out = []
    for k in elems(n):
        if k.tag == 'tr': out.append(k)
        else: out += rows_of(k)
    return out
def cell(c, head):
    v = text(c).strip()
    if c.tag == 'th' and head: v = r'\textbf{%s}' % v
    elif c.tag == 'th': v = r'\textbf{%s}' % v
    if 'opt' in c.cls(): v = r'\cellcolor{fmyellow!45}' + v
    return v
def conv_ct(n):
    rows = rows_of(n)
    IN_TABLE[0] = True
    out = []
    for r in rows:
        cs = [c for c in r.kids if not isinstance(c, str)]
        line = []
        for c in cs:
            k, v = c.cls(), text(c).strip()
            if c.tag == 'th' or 'tot' in k: v = r'\textbf{%s}' % v
            if 'on' in k: v = r'\cellcolor{fmyellow!45}' + v
            line.append(v)
        out.append(' & '.join(line) + r'\\')
    IN_TABLE[0] = False
    m = len([c for c in rows[0].kids if not isinstance(c, str)])
    s = r'\begin{tabular}{l|%s|c}\toprule' % ('c' * (m - 2)) + '\n' + out[0] + r'\midrule' + '\n' + '\n'.join(out[1:-1]) + '\n' + r'\midrule' + out[-1] + '\n' + r'\bottomrule\end{tabular}'
    return '\n\\begin{center}\\renewcommand{\\arraystretch}{1.55}\\setlength{\\tabcolsep}{9pt}%s\\end{center}\n' % s
def conv_table(n):
    if 'ct' in n.cls(): return conv_ct(n)
    rows = rows_of(n)
    m = max(len(elems(r)) for r in rows)
    first = elems(rows[0]) if rows else []
    if 'rf' in n.cls() or (len(rows) == 3 and first and not plain(first[0]).strip() and not any(c.tag == 'th' for c in first)):  # Ruffini (també sense la classe rf)
        IN_TABLE[0] = True
        cells = [[text(c).strip() for c in elems(r)] for r in rows]
        IN_TABLE[0] = False
        cells = [[('$' + x.strip('$').replace('\\mathbf ', '') + '$') if x else '' for x in r] for r in cells]
        s = r'\begin{tabular}{r|%s}' % ('r' * (m - 1)) + '\n'
        s += ' & '.join(cells[0]) + r'\\' + '\n' + ' & '.join(cells[1]) + r'\\\hline' + '\n'
        last = cells[2]; last[-1] = r'\fbox{%s}' % last[-1]
        s += ' & '.join(last) + r'\\' + '\n' + r'\end{tabular}'
        return '\n\\begin{center}%s\\end{center}\n' % s
    if 'ops' in n.cls():  # operacions amb infinit: columnes que ocupen tot l'ample
        s = r'\small\begin{tabularx}{\linewidth}{%s}\toprule' % ('>{\\centering\\arraybackslash}X' * m) + '\n'
        for r in rows:
            cs = elems(r)
            head = all(c.tag == 'th' for c in cs)
            s += ' & '.join((r'\textbf{%s}' if head else '%s') % text(c).strip() for c in cs) + r'\\' + (r'\midrule' if head else r'[6pt]') + '\n'
        return '\n\\begin{center}%s\\bottomrule\\end{tabularx}\\end{center}\n' % s
    if max(len(plain(c)) for r in rows for c in elems(r)) > 28:  # taules de text: columnes que fan salt de línia
        IN_TABLE[0] = True
        L = '>{\\raggedright\\arraybackslash}'
        s = r'\small\begin{tabularx}{\linewidth}{%sp{3.2cm}%s}\toprule' % (L, (L + 'X') * (m - 1)) + '\n'
        for r in rows:
            cs = elems(r)
            head = all(c.tag == 'th' for c in cs) or r.parent.tag == 'thead'
            pad = ['&'] * (m - len(cs)) if any('rowspan' in c.a for r2 in rows for c in elems(r2)) else []  # files que continuen un rowspan: les cel·les buides van davant
            s += ''.join(x + ' ' for x in pad) + ' & '.join(cell(c, head) for c in cs) + r'\\' + (r'\midrule' if head else r'[3pt]') + '\n'
        IN_TABLE[0] = False
        return '\n\\begin{center}\\renewcommand{\\arraystretch}{1.5}%s\\bottomrule\\end{tabularx}\\end{center}\n' % s
    IN_TABLE[0] = True
    s = r'\begin{tabular}{%s}\toprule' % ('c' * m) + '\n'
    for r in rows:
        cs = elems(r)
        head = all(c.tag == 'th' for c in cs) or r.parent.tag == 'thead'
        s += ' & '.join(cell(c, head) for c in cs) + r'\\' + (r'\midrule' if head and r is not rows[-1] else '') + '\n'
    s += r'\bottomrule\end{tabular}'
    IN_TABLE[0] = False
    return '\n\\begin{center}\\renewcommand{\\arraystretch}{1.5}%s\\end{center}\n' % s

def conv_section(n):
    h2 = next(k for k in elems(n) if 'sec-head' in k.cls())
    IN_TABLE[0] = True
    title = text(next(k for k in elems(h2) if k.tag == 'h2')).strip()
    IN_TABLE[0] = False
    return '\n\\Needspace{18\\baselineskip}\n\\section{%s}\n' % title + ''.join(conv(k) for k in n.kids)

latex = conv(ROOT)
latex = re.sub(r'\n{3,}', '\n\n', latex)
latex = re.sub(r'(?<!\\)\\\[', '\n\\[', latex)
latex = re.sub(r'(?<!\\)\\\]', '\\]\n', latex)
latex = re.sub(r'\\\]\s*([.,;])', r'\\,\1\\]', latex)  # el punt final va dins de la fórmula centrada
latex = re.sub(r'[ \t]+\n', '\n', latex)
latex = re.sub(r'\n{3,}', '\n\n', latex)
# fórmules centrades: \fmdisp{...} (s'encongeix si no cap en l'amplada de la línia)
latex = re.sub(r'(?<!\\)\\\[(.*?)(?<!\\)\\\]', lambda m: r'\fmdisp{%s}' % m.group(1).strip(), latex, flags=re.S)

# ---------- 5. document ----------
CARD = {
 1: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=3pt,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw (70,16)--(58,16)--(58,104)--(70,104) (170,16)--(182,16)--(182,104)--(170,104);
  \draw[line width=2pt,opacity=0.35] (78,26)--(162,92);
  \foreach \x/\y/\t in {88/40/2,120/40/$-1$,152/40/0,88/70/3,120/70/4,152/70/1,88/100/0,120/100/5,152/100/2}
    \node[anchor=base,inner sep=0pt,font=\fontsize{30}{30}\sffamily\bfseries] at (\x,\y) {\t};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{26}{26}\selectfont] at (192,40) {$A^{-1}$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{26}{26}\selectfont] at (10,AY) {$|A|$};
  \end{scope}
\end{tikzpicture}''',
 2: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=4pt,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw (20,106)--(220,20);
  \draw[opacity=0.75] (20,26)--(220,96);
  \draw[opacity=0.55] (128,6)--(128,114);
  \fill (128,59.5) circle (7);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{21}{21}\selectfont] at (18,124) {$x+y+z=6$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{21}{21}\selectfont] at (150,12) {$2x-y=1$};
  \end{scope}
\end{tikzpicture}''',
 3: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=3.2pt,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=2.6pt,opacity=0.7] (110,70)--(110,8) (110,70)--(210,92) (110,70)--(40,108);
  \fill[opacity=0.14] (50,40)--(150,22)--(210,62)--(110,82)--cycle;
  \draw (50,40)--(150,22)--(210,62)--(110,82)--cycle;
  \draw (60,110)--(190,14);
  \fill (128,47) circle (5.5);
  \draw[line width=3.4pt] (128,47)--(128,18) (122,26)--(128,16)--(134,26);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{22}{22}\selectfont] at (136,22) {$\vec n$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{22}{22}\selectfont] at (196,112) {$\pi$};
  \end{scope}
\end{tikzpicture}''',
 5: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,104)--(226,104) (24,114)--(24,8);
  \draw[line width=4pt,dash pattern=on 10pt off 10pt] (24,36)--(226,36);
  \draw[line width=4.5pt] (32,100) .. controls (70,98) and (92,80) .. (112,64);
  \draw[line width=4.5pt] (122,58) .. controls (150,44) and (180,40) .. (222,38);
  \draw[line width=4.5pt] (117,61) circle (5.5);
  \node[anchor=base west,inner sep=0pt,scale=2.4,font=\large\itshape] at (138,84) {%s $f(x)=L$};
  \end{scope}
\end{tikzpicture}''' % T('lím', 'lím'),

 6: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,104)--(226,104) (24,114)--(24,8);
  \draw[line width=4.5pt] (24,92) .. controls (60,92) and (70,20) .. (110,22) .. controls (150,24) and (150,100) .. (186,86) .. controls (210,76) and (214,50) .. (226,40);
  \draw[line width=4pt,dash pattern=on 10pt off 10pt] (60,22)--(160,22);
  \fill (110,22) circle (6);
  \draw[line width=4pt,opacity=0.55] (150,108)--(222,38);
  \node[anchor=base west,inner sep=0pt,scale=2.4,font=\large\itshape] at (118,46) {$f'(x)=0$};
  \end{scope}
\end{tikzpicture}''',
 7: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,104)--(226,104) (24,114)--(24,8);
  \draw[line width=4.5pt] (30,98) .. controls (50,50) and (64,26) .. (82,26) .. controls (100,26) and (116,86) .. (146,86) .. controls (170,86) and (196,50) .. (222,16);
  \draw[line width=4pt,dash pattern=on 10pt off 10pt] (56,26)--(108,26) (120,86)--(172,86);
  \fill (82,26) circle (5.5) (146,86) circle (5.5);
  \node[anchor=base west,inner sep=0pt,scale=3] at (34,56) {$\nearrow$};
  \node[anchor=base west,inner sep=0pt,scale=3] at (112,48) {$\searrow$};
  \node[anchor=base west,inner sep=0pt,scale=3] at (196,62) {$\nearrow$};
  \end{scope}
\end{tikzpicture}''',
 8: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,98)--(226,98) (30,114)--(30,6);
  \draw[line width=3pt,dash pattern=on 10pt off 10pt] (110,6)--(110,114) (14,108)--(226,34);
  \draw[line width=4.5pt] (20,113) .. controls (48,100) and (66,88) .. (80,90) .. controls (94,92) and (101,102) .. (105,114);
  \draw[line width=4.5pt] (115,6) .. controls (118,34) and (128,54) .. (150,54) .. controls (178,54) and (202,38) .. (226,26);
  \fill (80,90) circle (5) (150,54) circle (5);
  \end{scope}
\end{tikzpicture}''',
 9: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,104)--(226,104) (30,114)--(30,8);
  \begin{scope}
    \clip (30,90) .. controls (60,80) and (90,34) .. (130,34) .. controls (170,34) and (190,60) .. (226,56)--(226,104)--(30,104)--cycle;
    \fill[fill opacity=0.5] (70,0) rectangle (170,104);
    \draw[line width=4.5pt,dash pattern=on 7pt off 9pt] (70,104)--(70,0) (170,104)--(170,0);
  \end{scope}
  \draw[line width=4.5pt] (30,90) .. controls (60,80) and (90,34) .. (130,34) .. controls (170,34) and (190,60) .. (226,56);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{34}{34}\selectfont] at (90,88) {$\int$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{22}{22}\selectfont\itshape] at (108,88) {f(x)dx};
  \end{scope}
\end{tikzpicture}''',
 10: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=4pt,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \fill (20,60) circle[radius=5];
  \draw (20,60)--(80,26) (20,60)--(80,94) (80,26)--(130,12) (80,26)--(130,40) (80,94)--(130,80) (80,94)--(130,108);
  \fill (80,26) circle[radius=4] (80,94) circle[radius=4] (130,12) circle[radius=3.5] (130,40) circle[radius=3.5] (130,80) circle[radius=3.5] (130,108) circle[radius=3.5];
  \node[anchor=base west,inner sep=0pt,font=\fontsize{20}{20}\selectfont\itshape] at (38,36) {0,6};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{20}{20}\selectfont\itshape] at (38,92) {0,4};
  \begin{scope}[rotate around={-12:(190,58)}]
    \draw[rounded corners=0.74cm] (162,30) rectangle (218,86);
    \fill (176,44) circle[radius=4.5] (190,58) circle[radius=4.5] (204,72) circle[radius=4.5];
  \end{scope}
  \end{scope}
\end{tikzpicture}''',
}
CARD[4] = CARD[3]
CARD = CARD[N]

PRE = r'''\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[BABEL]{babel}
\usepackage{lmodern}
\linespread{1.22}
\usepackage[a4paper,top=2.4cm,bottom=2.2cm,left=1.5cm,right=1.5cm,headheight=1.1cm,headsep=0.5cm,footskip=1cm]{geometry}
\usepackage{amsmath,amssymb,cancel}
\usepackage{icomma}
\usepackage{graphicx}
\usepackage[table]{xcolor}
\usepackage{tikz}\usetikzlibrary{calc}
\usepackage{pgfplots}\pgfplotsset{compat=1.17}
\usepackage{fontawesome5}
\usepackage{ccicons}
\usepackage{fancyhdr}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{needspace}
\usepackage[most]{tcolorbox}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdftitle={PDFTITLE},pdfsubject={PDFSUBJ},pdfkeywords={PDFKW}}

% colors de la web (FentMates, BLOCKCOL; es manté el nom fmgreen dels apunts de les altres unitats)
\definecolor{fmnavy}{HTML}{1B2748}
\definecolor{fmgreen}{HTML}{COLC}
\definecolor{fmgreenl}{HTML}{COLL}
\definecolor{fmyellow}{HTML}{FFC94D}
\definecolor{fmgold}{HTML}{E9A919}
\definecolor{fmaccent}{HTML}{FF7A50}
\definecolor{fmteal}{HTML}{2BB3A3}
\definecolor{fmdef}{HTML}{1D4F73}\definecolor{fmdefbg}{HTML}{EEF4F9}
\definecolor{fmprop}{HTML}{3B4252}\definecolor{fmpropbg}{HTML}{F3F4F7}
\definecolor{fmex}{HTML}{A3203A}\definecolor{fmexbg}{HTML}{FBF0F2}
\definecolor{fmmuted}{HTML}{5D6685}\definecolor{fmball0}{HTML}{E2483D}\definecolor{fmball1}{HTML}{2F6FD6}
\definecolor{fmsurface}{HTML}{EEF1F8}

\newcommand{\lt}{<}\newcommand{\gt}{>}
% fórmula en línia que no es parteix mai; si no cap en una línia, es posa centrada
\newcommand{\fmm}[1]{\setbox0=\hbox{$#1$}\ifdim\wd0>\linewidth\fmdisp{#1}\else\mbox{\box0}\fi}
% fórmula centrada; si és més ampla que la línia, s'encongeix fins que hi cap
\newcommand{\fmdisp}[1]{\[\setbox2=\hbox{$\displaystyle #1$}\ifdim\wd2>\linewidth\resizebox{\linewidth}{!}{\box2}\else\box2\fi\]}
\DeclareUnicodeCharacter{2212}{-}
\DeclareUnicodeCharacter{2225}{\ensuremath{\parallel}}\DeclareUnicodeCharacter{22A5}{\ensuremath{\perp}}\DeclareUnicodeCharacter{2226}{\ensuremath{\nparallel}}
\DeclareUnicodeCharacter{207A}{\ensuremath{^{+}}}\DeclareUnicodeCharacter{207B}{\ensuremath{^{-}}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{12pt}
\setlength{\lineskip}{5pt}\setlength{\lineskiplimit}{5pt}  % més aire al voltant de les fraccions en línia
\setlength{\emergencystretch}{3em}
\setlist{itemsep=4pt,topsep=4pt}
\renewcommand{\thesection}{UNITN.\arabic{section}}
\titleformat{\section}{\color{fmnavy}\Large\bfseries}{\colorbox{fmdef}{\color{white}\strut\ \thesection\ }}{0.6em}{}[{\color{fmdef}\titlerule[1.2pt]}]
\titlespacing*{\section}{0pt}{16pt}{8pt}
\titleformat*{\subsection}{\color{fmgreen}\large\bfseries}
\allowdisplaybreaks

% dibuix de la targeta de la unitat a la web (illustrations.js), en blanc
\newcommand{\fmcard}{CARD}
\newcommand{\fmbrand}{\raisebox{-0.25\height}{\includegraphics[height=0.5cm]{logo-fentmates.pdf}}}

% capçalera i peu
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\fmbrand}
\fancyhead[R]{\small\color{fmmuted}HEADTXT}
\fancyfoot[L]{\scriptsize\color{fmmuted}\href{https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ca}{\ccbyncsa}\ \ FentMates · fentmates.org · CC BY-NC-SA 4.0}
\fancyfoot[R]{\small\color{fmmuted}\thepage}
\renewcommand{\headrulewidth}{0.4pt}\renewcommand{\headrule}{\color{fmmuted!40}\hrule height \headrulewidth}
\fancypagestyle{primera}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}
  \fancyfoot[L]{\scriptsize\color{fmmuted}\href{https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ca}{\ccbyncsa}\ \ FentMates · fentmates.org · CC BY-NC-SA 4.0}
  \fancyfoot[R]{\small\color{fmmuted}\thepage}}

% caixes (mateixos colors que la web)
% quan una caixa es parteix entre dues pàgines, la vora del tall és discontínua
\tcbset{fmbase/.style={enhanced,breakable,arc=3mm,boxrule=1pt,left=3.5mm,right=3.5mm,top=2mm,bottom=2.5mm,before skip=10pt,after skip=10pt,fonttitle=\bfseries,
  frame style={fill=tcbcolframe},
  overlay first={\fill[tcbcolback] ([xshift=1pt]frame.south west) rectangle ([xshift=-1pt,yshift=1.2pt]frame.south east);
    \draw[tcbcolframe,line width=1pt,dash pattern=on 5pt off 3pt] (frame.south west)--(frame.south east);},
  overlay middle={\fill[tcbcolback] ([xshift=1pt]frame.south west) rectangle ([xshift=-1pt,yshift=1.2pt]frame.south east);
    \fill[tcbcolback] ([xshift=1pt]frame.north west) rectangle ([xshift=-1pt,yshift=-1.2pt]frame.north east);
    \draw[tcbcolframe,line width=1pt,dash pattern=on 5pt off 3pt] (frame.south west)--(frame.south east) (frame.north west)--(frame.north east);},
  overlay last={\fill[tcbcolback] ([xshift=1pt]frame.north west) rectangle ([xshift=-1pt,yshift=-1.2pt]frame.north east);
    \draw[tcbcolframe,line width=1pt,dash pattern=on 5pt off 3pt] (frame.north west)--(frame.north east);}}}
\newtcolorbox{fmdef}[1]{fmbase,colback=fmdefbg,colframe=fmdef,coltitle=white,title={#1}}
\newtcolorbox{fmprop}[1]{fmbase,colback=fmpropbg,colframe=fmprop,coltitle=white,title={#1},halign title=center}
\newtcolorbox{fmex}[1]{fmbase,before upper=\raggedright,colback=fmexbg,colframe=fmex,colbacktitle=fmexbg,coltitle=fmex,title={\faPencil*\ #1},
  titlerule=0.4pt,titlerule style={fmex!40,dashed}}
\newtcolorbox{fmwarn}[1]{fmbase,colback=fmsf!6,colframe=fmsf,coltitle=white,title={#1}}
\newtcolorbox{fmnote}{enhanced,breakable,colback=white,colframe=white,borderline west={3pt}{0pt}{fmaccent},arc=0pt,left=3mm,right=2mm,top=1mm,bottom=1mm,before skip=6pt,after skip=6pt,before upper=\raggedright}
\newcommand{\fmkey}[1]{\colorbox{fmyellow!45}{\strut #1}}
\newcommand{\fmuline}[1]{\textbf{\color{fmaccent}#1}}
\definecolor{fmok}{HTML}{15803D}\definecolor{fmev}{HTML}{2563EB}\definecolor{fmsf}{HTML}{C2410C}\definecolor{fmsi}{HTML}{7C3AED}\definecolor{fmas}{HTML}{A3203A}
\newcommand{\fmbadge}[2]{\tcbox[on line,colback=#1,colframe=#1,arc=2mm,boxsep=0pt,left=4pt,right=4pt,top=1.5pt,bottom=1.5pt]{\color{white}\footnotesize\bfseries #2}}
\newcommand{\fmchip}[1]{\tcbox[on line,colback=fmsf!10,colframe=fmsf!50,arc=2mm,boxsep=1pt,left=4pt,right=4pt]{#1}}
\newcommand{\fmlevel}[2]{\tcbox[on line,colback=white,colframe=fmmuted!40,arc=2mm,boxsep=2pt,halign=center]{\begin{tabular}{c}{\scriptsize\color{fmmuted}\MakeUppercase{#1}}\\#2\end{tabular}}}
% gràfiques
\pgfplotsset{fmaxis/.style={axis lines=middle,grid=major,grid style={fmmuted!15},axis line style={fmmuted,-latex},
  tick label style={font=\scriptsize,color=fmmuted},clip=true,unbounded coords=jump,restrict y to domain=-200:200,
  every axis plot/.append style={line join=round}},
  fmcurve/.style={fmaccent,line width=1.6pt,smooth}}
\tikzset{fmasy/.style={fmmuted,dashed,line width=0.9pt},fmguide/.style={fmaccent,dotted,line width=0.8pt},
  fmdot/.style={circle,fill=fmaccent,inner sep=0pt,minimum size=5pt},fmopen/.style={circle,draw=fmaccent,fill=white,line width=1pt,inner sep=0pt,minimum size=5pt}}
\newcommand{\fmpau}[1]{\tcbox[on line,colback=fmnavy,colframe=fmnavy,arc=2mm,boxsep=0pt,left=4pt,right=4pt,top=1.5pt,bottom=1.5pt]{\color{white}\scriptsize\bfseries\MakeUppercase{#1}}\ }
'''

TITLE = r'''
\begin{document}
\thispagestyle{primera}
\begin{tikzpicture}[remember picture,overlay]
  \fill[fmgreen] (current page.north west) rectangle ([yshift=-10.1cm]current page.north east);
  \begin{scope}
    \clip (current page.north west) rectangle ([yshift=-10.1cm]current page.north east);
    \node[anchor=north west,inner sep=0pt] at ([xshift=6.6cm,yshift=CARDYcm]current page.north west) {\fmcard};
  \end{scope}
  \node[anchor=north west,inner sep=0pt] at ([xshift=1.5cm,yshift=-1.1cm]current page.north west) {\tcbox[colback=white,colframe=white,arc=2.5mm,boxsep=0pt,left=7pt,right=7pt,top=5pt,bottom=5pt]{\includegraphics[height=0.75cm]{logo-fentmates.pdf}}};
\end{tikzpicture}
\vspace*{0.55cm}
\tcbox[colback=white!15!fmgreen,colframe=white!15!fmgreen,arc=2.5mm,boxsep=0pt,left=6pt,right=6pt,top=3pt,bottom=3pt]{\color{white}\small\bfseries KICKER}

\vspace{4pt}
{\raggedright\color{white}\fontsize{25}{30}\selectfont\bfseries{\color{fmyellow}UNITNUM} · UNITTITLE\par}
\vspace{6pt}
\begin{minipage}{\linewidth}\color{white!88!fmgreen}\small HERO\end{minipage}\par
% l'índex comença sempre a la mateixa altura, per davall de la franja (com en les unitats 5-10)
\vspace*{\dimexpr 8.6cm-\pagetotal\relax}

\begin{tcolorbox}[colback=fmsurface,colframe=fmsurface,arc=3mm,left=4mm,right=4mm,top=2mm,bottom=2mm]
\small\textbf{TOCWORD}\par\smallskip
\begin{minipage}[t]{0.49\linewidth}\small TOC1\end{minipage}\hfill\begin{minipage}[t]{0.49\linewidth}\small TOC2\end{minipage}
\end{tcolorbox}
'''

secs = re.findall(r'\\section\{(.*?)\}\n', latex)
assert len(tocnames) == len(secs), (len(tocnames), len(secs))
toc = [(r'\mbox{%s}\\[3pt]' if len(tocnames[i]) < 38 else r'%s\\[3pt]') % (r'\hyperlink{sec%d}{\textbf{\color{fmgreen}%d.%d}\ \ %s}' % (i + 1, N, i + 1, esc(tocnames[i]))) for i in range(len(secs))]  # els noms llargs poden fer dues línies
half = (len(toc) + 1) // 2
k = [0]
def anchor(m):
    k[0] += 1
    return '\\section{%s}\\hypertarget{sec%d}{}\n' % (m.group(1), k[0])
latex = re.sub(r'\\section\{(.*?)\}\n', anchor, latex)
hero_tex = esc(re.sub(T(r'(,| i) eines interactives( en 3D)?', r'(,| y) herramientas interactivas( en 3D)?'), '', hero)
               .replace(T('resolts pas a pas:', 'resueltos paso a paso:'), T('resolts pas a pas:', 'resueltos paso a paso:')))
hero_tex = hero_tex.replace(T('Teoria, exemples', 'Teoría, ejemplos'), T('Teoria i exemples', 'Teoría y ejemplos'))
unit = T('Unitat %d', 'Unidad %d') % N
pre = PRE
for a, b in [('BABEL', T('catalan', 'spanish,es-minimal,es-noshorthands')),
             ('PDFTITLE', T('Apunts de teoria. Unitat %d: %s. 2n de Batxillerat MII', 'Apuntes de teoría. Unidad %d: %s. 2.º de Bachillerato MII') % (N, U['title'])),
             ('PDFSUBJ', T('Matemàtiques II', 'Matemáticas II')), ('PDFKW', U['kw']),
             ('BLOCKCOL', U['block']), ('COLC', U['c']), ('COLL', U['cl']), ('UNITN', str(N)), ('CARD', CARD.replace('AY', '34')),
             ('HEADTXT', T('2n Batxillerat MII · Unitat %d: %s', '2.º Bachillerato MII · Unidad %d: %s') % (N, U.get('short', U['title'])))]:
    pre = pre.replace(a, b)
hero_tex = re.sub(r'</?strong>', '', hero_tex)  # la descripció del web porta etiquetes HTML
title = TITLE.replace('HERO', hero_tex).replace('TOC1', '\n'.join(toc[:half])).replace('TOC2', '\n'.join(toc[half:]))
for a, b in [('KICKER', T('Apunts de teoria · 2n Batxillerat · Matemàtiques II', 'Apuntes de teoría · 2.º Bachillerato · Matemáticas II')),
             ('UNITNUM', unit), ('CARDY', {1: '-0.85'}.get(N, '-1.3')), ('UNITTITLE', U['title']), ('TOCWORD', T('Índex', 'Índice'))]:
    title = title.replace(a, b)
doc = pre + title + latex + '\n\\end{document}\n'

# retocs de l'autor sobre el .tex de l'escriptori dels apunts de CCSS (unitats 1 i 2, 22/11/2026; el contingut és el mateix):
# valen per als dos idiomes
def retoc(a, b, regex=False):
    global doc
    if regex:
        doc, k = re.subn(a, b, doc, flags=re.S)
        assert k == 1, a[:80]
    else:
        assert doc.count(a) == 1, a[:80]
        doc = doc.replace(a, b)
if N == 1:
    retoc('\\usepackage{fancyhdr}\n', '\\usepackage{fancyhdr}\n\\usepackage{multicol}\n')
    # nota de A·I=I·A: una mica d'aire abans, i les fórmules més a prop del seu text
    retoc(r'(\n\\textbf\{[^\n]*\\fmm\{A\\cdot B=B\\cdot A\}[^\n]*permutables\.\}\n)', r'\1\n\\vspace*{0.2cm}\n', True)
    retoc('\n\n\\fmdisp{(A+I)\\cdot(A-I)=A\\cdot A', '\n\\vspace*{-0.2cm}\n\\fmdisp{(A+I)\\cdot(A-I)=A\\cdot A')
    retoc('\n\n\\fmdisp{(A\\pm I)^2=(A\\pm I)\\cdot(A\\pm I)=A\\cdot A\\pm A\\cdot I\\pm I\\cdot A+I\\cdot I\\overset{A\\cdot I=I\\cdot A}{=}A^2\\pm A\\cdot I\\pm A\\cdot I+I^2=A^2\\pm2AI+I=A^2\\pm2A+I}',
          '\n\\vspace*{-0.2cm}\n\\fmdisp{(A\\pm I)^2=(A\\pm I)\\cdot(A\\pm I)=A\\cdot A\\pm A\\cdot I\\pm I\\cdot A+I\\cdot I\\overset{A\\cdot I=I\\cdot A}{=}A^2\\pm A\\cdot I\\pm A\\cdot I+I^2=}\n\\fmdisp{=A^2\\pm2AI+I=A^2\\pm2A+I}')
    # propietats de la matriu inversa en dues columnes
    retoc(r'(\\begin\{fmprop\}\{[^}]*\}\n)(\\begin\{itemize\}\n\\item \\fmm\{\(A\\cdot B\)\^\{-1\}.*?\\end\{itemize\}\n)', r'\1\\begin{multicols}{2}\n\2\\end{multicols}\n', True)
    if True:  # salts de pàgina (en castellà cauen al mateix lloc)
        retoc('\\rightarrow a=\\pm2}\n\n', '\\rightarrow a=\\pm2}\n\n\\newpage\n')
        retoc('\\fmdisp{XA-2X=A}\n\n', '\\fmdisp{XA-2X=A}\n\n\\newpage\n')
if N == 2:  # retocs de l'autor sobre el .tex de l'escriptori (22/11/2026)
    retoc('z=\\frac{-41+19\\lambda}{11},\\quad\\lambda\\in\\mathbb{R}}}\n\n', 'z=\\frac{-41+19\\lambda}{11},\\quad\\lambda\\in\\mathbb{R}}}\n\n\\vspace*{0.2cm}\n\n')
    retoc(r'(\\fmdisp\{\\left\\\{\\begin\{array\}\{ccccccccc\} a_\{11\}x_1 &\+& a_\{12\}x_2[^\n]*\n\n)', r'\1\\vspace*{0.2cm}\n\n', True)
    retoc(r'(\\fmm\{\\boxed\{x_1=x_2=\\cdots=x_n=0\}\}[^\n]*\n\n)', r'\1\\newpage\n', True)
    retoc('\\lambda,\\mu\\in\\mathbb{R}}}\n\n', '\\lambda,\\mu\\in\\mathbb{R}}}\n\\newpage\n')

if N == 3:  # el títol fa dues línies: tot el text de la franja puja perquè l'última línia no quede apegada a la vora
    retoc('\\vspace*{0.55cm}\n\\tcbox', '\\vspace*{0.0cm}\n\\tcbox')
    # 3.2 no salta a pàgina nova (deixava mitja pàgina en blanc): el títol i el principi del requadre caben baix
    retoc('\\Needspace{18\\baselineskip}\n\\section{Aplica', '\\Needspace{5\\baselineskip}\n\\section{Aplica')
    # retocs de l'autor sobre el .tex de l'escriptori (22/11/2026): valen per als dos idiomes
    retoc(r':\n(          \\fmm\{\\ \\dfrac\{c_1-a_1\}\{b_1-a_1\}[^\n]*\n)', r':\\\\[2ex]\n\1          \\newpage\n', True)
    for k in (4, 6):  # 3.4 i 3.6 comencen on acaba l'apartat anterior
        retoc(r'\\Needspace\{18\\baselineskip\}(\n\\section\{[^\n]*\}\\hypertarget\{sec%d\}\{\})' % k, r'\\Needspace{7\\baselineskip}\1', True)
    retoc('\\end{vmatrix}}\n\n\\begin{itemize}\n\\item ', '\\end{vmatrix}}\n\\newpage\n\\begin{itemize}\n\\item ')
    retoc('z=3-\\lambda\\end{cases}}\n\n', 'z=3-\\lambda\\end{cases}}\\\\\n\n\\vspace*{0.2cm}\n')
    # taules (per ordre d'aparició): equacions de la recta, casos del pla, recta i pla, dos plans
    TB = '\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\small\\begin{tabularx}{\\linewidth}{>{\\raggedright\\arraybackslash}p{3.2cm}'
    pos = [m.start() for m in re.finditer(re.escape(TB), doc)]
    assert len(pos) >= 6, len(pos)
    for i, (st, w) in reversed(list(enumerate([('1.5', '4.2cm'), ('1.5', '7.2cm'), ('2.5', '3.2cm'), ('2.5', '5.2cm')]))):
        j = pos[[0, 2, 4, 5][i]]
        doc = doc[:j] + TB.replace('{1.5}', '{%s}' % st).replace('3.2cm', w) + doc[j + len(TB):]
    # una mica d'aire abans de les notes «Notació» (3.7) i «Compte» (3.11), que van just després d'una llista
    assert doc.count('\\end{itemize}\n\n\\begin{fmnote}\\fmuline{') == 2
    doc = doc.replace('\\end{itemize}\n\n\\begin{fmnote}\\fmuline{', '\\end{itemize}\n\\vspace*{0.2cm}\n\\begin{fmnote}\\fmuline{')
if N == 4:  # l'apartat 4.1 i el primer requadre comencen a la portada
    retoc('\\vspace*{\\dimexpr 8.6cm-\\pagetotal\\relax}', '\\vspace*{\\dimexpr 8.2cm-\\pagetotal\\relax}')
    doc = doc.replace('}}\\\\[3pt]\n', '}}\\\\[1pt]\n')
    retoc('\\Needspace{18\\baselineskip}\n\\section{Angle entre dues', '\\Needspace{4\\baselineskip}\n\\section{Angle entre dues') if not ES else retoc('\\Needspace{18\\baselineskip}\n\\section{Ángulo entre dos', '\\Needspace{4\\baselineskip}\n\\section{Ángulo entre dos')
    # retocs de l'autor sobre el .tex de l'escriptori (23/11/2026): valen per als dos idiomes
    retoc('\\fmm{|\\vec n\\cdot P+D|}.\n', '\\fmm{|\\vec n\\cdot P+D|}.\\\\\n\n')
    retoc(r"(\\pi'_2:2x-y\+2z-15=0\}\}\.) ", r'\1 \\\\[2ex]\n', True)
    retoc('\\text{u}}}. ', '\\text{u}}}. \\\\[2ex]\n')
    TB = '\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\small\\begin{tabularx}{\\linewidth}{>{\\raggedright\\arraybackslash}p{3.2cm}'
    pos = [m.start() for m in re.finditer(re.escape(TB), doc)]
    assert len(pos) == 2, len(pos)
    doc = doc[:pos[1]] + TB.replace('3.2cm', '7.2cm') + doc[pos[1] + len(TB):]  # taula d'àrees i volums (4.11)
if N == 10:  # unió de tres successos: no cap en una línia
    retoc('\\fmm{P(A\\cup B\\cup C)=P(A)+P(B)+P(C)-P(A\\cap B)-P(A\\cap C)-P(B\\cap C)+P(A\\cap B\\cap C)}.',
          '\n\\[\\begin{aligned}P(A\\cup B\\cup C)&=P(A)+P(B)+P(C)-P(A\\cap B)\\\\&\\quad-P(A\\cap C)-P(B\\cap C)+P(A\\cap B\\cap C)\\,.\\end{aligned}\\]\n')
if N == 5:  # retocs de l'autor (Desktop, revisió 2026-11-23)
    retoc('\\newtcolorbox{fmnote}', '\\newtcolorbox{fmexfill}[1]{fmbase,breakable=false,height fill,colback=fmexbg,colframe=fmex,colbacktitle=fmexbg,coltitle=fmex,title={\\faPencil*\\ #1},\n  titlerule=0.4pt,titlerule style={fmex!40,dashed}}\n\\newtcolorbox{fmnote}')
    retoc('\\vspace*{\\dimexpr 8.6cm-\\pagetotal\\relax}', '\\vspace*{\\dimexpr 8.2cm-\\pagetotal\\relax}')
    retoc(r'\\Needspace\{18\\baselineskip\}\n(\\section\{[^\n]*\\hypertarget\{sec1\}\{\})\n\n\\Needspace\{7\\baselineskip\}', r'\\Needspace{4\\baselineskip}\n\1\n\\Needspace{3\\baselineskip}', True)
    # quadre «llegim els límits a la gràfica»: el de CCSS U4 (fórmula dalt, límits baix l'un al costat de l'altre, omple la pàgina)
    box = open(os.path.join(HERE, 't5-grafica%s.tex' % ('-es' if ES else '')), encoding='utf-8').read().rstrip('\n')
    doc, k = re.subn(r'\\begin\{fmex\}\{(Exemples: llegim|Ejemplos: leemos)[^\n]*\n.*?\\end\{fmex\}', lambda m: box, doc, count=1, flags=re.S)
    assert k == 1
    # taula d'operacions amb infinit: les aclaracions en una fila nova
    retoc(r'(\\fmm\{\(\\pm\\infty\)\\cdot\(\\pm\\infty\)=\\pm\\infty\}) (\([^()]*\)) & (\\fmm\{\\dfrac\{k\}\{0\}=\\pm\\infty\\ \\ \(k\\neq0\)\}) (\([^()]*\))\\\\\[6pt\]',
          r'\1 & \3 \\\\[6pt]\n&\2&\4\\\\[6pt]', True)
    retoc(r'(\n\\item Exponencia[^\n]*?\.) (\\fmm\{\\displaystyle\\lim_\{x\\to\+\\infty\}\\frac\{3e\^\{2x\}-e\^x\})', r'\1\\\\[2ex]\n \2', True)
    retoc(r'(\\frac\{A-B\}\{\\sqrt\{A\}\+\\sqrt\{B\}\}\})\n\n(\\begin\{fmnote\})', r'\1\n\2', True)
    retoc(r'(\\left\(\\sqrt\{x\^2\+4x\}-x\\right\))\}\n\n\\fmm\{(\\sqrt\{\+\\infty\}-\\infty=\+\\infty-\\infty\\ \\ \\text\{IND\.\})\}( \([^\n]*?\)\.)\n',
          r'\1=\2}\3\\\\[2ex]\n', True)
    retoc(r'(\\item \\fmm\{\\displaystyle\\lim_\{x\\to\+\\infty\}\\left\(\\sqrt\{x\^2\+x\}-\\sqrt\{x\^2-x\}\\right\))\}\n\n\\fmm\{(\+\\infty-\\infty\\ \\ \\text\{IND\.\})\}', r'\1=\2}', True)
    retoc(r'(\\fmm\{0\\cdot\\infty\} \$\\to\$ [^;\n]*;) (\\fmm\{1\^\\infty\} \$\\to\$)', r'\1\\\\[2ex]\n \2', True)
    retoc(r'\\Needspace\{16\\baselineskip\}\n(\\subsection\*\{Indetermina[^\n]*\\fmm\{1\^\\infty\} en un )', r'\\Needspace{2\\baselineskip}\n\1', True)
    TB = '\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\small\\begin{tabularx}{\\linewidth}{>{\\raggedright\\arraybackslash}p{3.2cm}'
    pos = [m.start() for m in re.finditer(re.escape(TB), doc)]
    assert len(pos) == 4, len(pos)
    for i in (3, 2, 1):
        doc = doc[:pos[i]] + TB.replace('3.2cm', '5.2cm') + doc[pos[i] + len(TB):]
if N == 6:  # retocs de l'autor (Desktop, revisió 2026-11-23)
    retoc('\\DeclareUnicodeCharacter{207A}{\\ensuremath{^{+}}}\\DeclareUnicodeCharacter{207B}{\\ensuremath{^{-}}}\n', '')
    retoc('\\vspace{6pt}\n\\begin{minipage}{\\linewidth}\\color{white!88!fmgreen}', '\\vspace{4pt}\n\\begin{minipage}{\\linewidth}\\color{white!88!fmgreen}')
    # pilota: més aire entre els passos
    retoc(r'(\\fmm\{\[0,4\]\} [^\n]*?\.)\n\n(\\fmm\{s\(0\)=0,[^\n]*?\}\.)\n\n(\\fmm\{\\text\{TVM\}\[0,1\][^\n]*?\.)\n',
          r'\1\\\\[2ex]\n\n\n\2\\\\[2ex]\n\n\3\\\\[2ex]\n', True)
    retoc(r"(\\textbf\{funci[óo]n? derivada\}) \\fmm\{(f'\(x\)=\\displaystyle\\lim_\{h\\to0\}\\frac\{f\(x\+h\)-f\(x\)\}\{h\})\}\.", r'\1 \\[\2\\]', True)
    retoc('\\fmm{\\ln y=2\\ln(x+1)+\\tfrac12\\ln(x-1)-4\\ln(x+3)}\n', '\\fmm{\\ln y=2\\ln(x+1)+\\tfrac12\\ln(x-1)-4\\ln(x+3)}\\\\[2ex]\n')
    retoc('-\\dfrac{4}{x+3}\\right)} (', '-\\dfrac{4}{x+3}\\right)}\\\\[2ex] (')
    retoc(r'(\\fmm\{f\(x\)=x\^2-4\} [^\n]*?\\fmm\{x\\geq2\}:) (\\fmm\{\\ f\'\(2\^-\)=-4\\neq4=f\'\(2\^\+\)\})', r'\1\\\\[2ex] \2', True)
    TB = '\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\small\\begin{tabularx}{\\linewidth}{>{\\raggedright\\arraybackslash}p{3.2cm}'
    pos = [m.start() for m in re.finditer(re.escape(TB), doc)]
    assert len(pos) == 4, len(pos)
    doc = doc[:pos[0]] + TB.replace('3.2cm', '3.8cm') + doc[pos[0] + len(TB):]

if N == 7:  # retocs de l'autor (Desktop, revisió 2026-11-23)
    retoc(r'(\\hyperlink\{sec11\}\{[^\n]*?Representaci[óo]n? \(II\): radical(?:s|es), )exponencial(?:s|es) (i|y) logarítmi(?:ques|cas)\}', r'\1exp. \2 logarítm.}', True)
    retoc(r'(\(\\fmm\{x=a\}\)\.) (Recorda|Recuerda):', r'\1 \\\\[2ex]\n\2:', True)
    retoc('\\Rightarrow f\'(1)=\\dfrac{24}{36}=\\dfrac23}.\n', '\\Rightarrow f\'(1)=\\dfrac{24}{36}=\\dfrac23}.\\\\[2ex]\n')
    retoc('\\fmm{y-f(a)=f\'(a)(x-a)}, \\fmm{\\ f\'(x)=\\frac x2+4}', '\\fmm{y-f(a)=f\'(a)(x-a)}, \\\\[2ex]\n\\fmm{\\ f\'(x)=\\frac x2+4}')
    retoc(r'\n\\item \\fmpau\{PAU M[úu]rcia 2026\}[^\n]*?\\ln\\frac\{25\}\{2\}\}\.', '', True)
    retoc(r'\\Needspace\{7\\baselineskip\}\n(\\begin\{fmdef\}\{M[àá]xim)', r'\\Needspace{1\\baselineskip}\n\1', True)
    i = doc.index('\\hypertarget{sec8}'); j = doc.index('\\end{fmdef}', i)
    b = doc[i:j]
    assert b.count('\\begin{minipage}[t]{0.48\\linewidth}') == 2 and b.count('width=6.4cm,height=5cm') == 1
    b = b.replace('\\begin{minipage}[t]{0.48\\linewidth}', '\\begin{minipage}[t]{0.6\\linewidth}', 1).replace('\\begin{minipage}[t]{0.48\\linewidth}', '\\begin{minipage}[t]{0.37\\linewidth}', 1)
    doc = doc[:i] + b.replace('width=6.4cm,height=5cm', 'width=5.6cm,height=4.6cm') + doc[j:]  # el quadre cap davall del títol 7.8
    retoc(r"(\\fmm\{f''\(x\)=4x\\,e\^\{-2x\^2\}\(4x\^2-3\)\}[^\n]*)\n", r'\1\n\\newpage\n', True)
    TB = '\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\small\\begin{tabularx}{\\linewidth}{>{\\raggedright\\arraybackslash}p{3.2cm}'
    pos = [m.start() for m in re.finditer(re.escape(TB), doc)]
    assert len(pos) == 3, len(pos)
    for k, w in reversed(list(zip(pos, ('5.5cm', '2.2cm', '9.2cm')))):
        doc = doc[:k] + TB.replace('3.2cm', w) + doc[k + len(TB):]

if N == 8:  # títol de dues línies i text llarg: tot el text de la franja puja perquè no se n'isca de la franja verda
    retoc('\\vspace*{0.55cm}\n\\tcbox', '\\vspace*{0.0cm}\n\\tcbox')
    retoc('\\vspace{6pt}\n\\begin{minipage}{\\linewidth}\\color{white!88!fmgreen}', '\\vspace{2pt}\n\\begin{minipage}{\\linewidth}\\color{white!88!fmgreen}')
    # retocs de l'autor (Desktop, revisió 2026-11-23)
    retoc(r'\\end\{tcolorbox\}\n\n\\Needspace\{7\\baselineskip\}\n(\\begin\{fmdef\}\{Gui)', r'\\end{tcolorbox}\n\\vspace*{0.3cm}\n\\Needspace{10\\baselineskip}\n\1', True)
    retoc(r'(\n\$\\dfrac\{1\}\{\\sqrt\{g\(x\)\}\}\$ & [^\n]*?)\\\\\[3pt\]\n', r'\1\\\\[5pt]\n', True)
    if ES:  # l'última línia del document no passa a una pàgina 17 tota sola
        retoc(r'(\\hypertarget\{sec12\}\{\})', r'\1\\enlargethispage{\\baselineskip}', True)
    retoc(r'\n(\\item [^\n]*\\fmm\{f\(x\)=\\sin 2x\+\\cos 3x\})', r'\n\\newpage\n\1', True)
    TB = '\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\small\\begin{tabularx}{\\linewidth}{>{\\raggedright\\arraybackslash}p{3.2cm}'
    pos = [m.start() for m in re.finditer(re.escape(TB), doc)]
    assert len(pos) == 6, len(pos)
    for k, w in ((5, '5.8cm' if ES else '5.2cm'), (2, '7.2cm'), (0, '6.2cm')):  # en castellà, la 1a fila de la taula de 8.12 no es parteix
        doc = doc[:pos[k]] + TB.replace('3.2cm', w) + doc[pos[k] + len(TB):]

out = os.path.join(OUTDIR, 't%d-apunts-teoria%s.tex' % (N, '-es' if ES else ''))
open(out, 'w', encoding='utf-8').write(doc)
print(os.path.relpath(out, HERE), len(secs), 'apartats,', len(doc), 'caràcters')
