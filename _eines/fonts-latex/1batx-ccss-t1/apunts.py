# Genera tN-apunts-teoria.tex per a les unitats de 1r Batxillerat CCSS (Matemàtiques Aplicades a les Ciències Socials I):
# apunts de teoria en PDF per a l'alumnat, a partir dels apunts interactius materials/1batx-ccss/tN-....html.
# Copia de ../1batx-mi-t1/apunts.py (mateix disseny i mateixa conversió, amb el comportament de les unitats 5-10 de MI
# per a totes: figures en PDF vectorial amb Inkscape i blocs que es mesuren per no deixar títols sols ni forats).
# Les unitats 4 (Estudi de funcions) i 6 (Límits i continuïtat) són iguals que les unitats 6 i 8 de 1r BAT MI.
# Novetats respecte de MI: les rectes apilades de la U3 es lligen de la pàgina (STACKS); els diagrames de Venn, l'arbre
# (U9) i les campanes de Gauss (U10) es prenen del DOM que deixa Chrome i es passen a PDF; a la U10 les taules de la
# binomial i de la normal van en un annex al final (com en 2n BAT CCSS) i les caixes interactives es canvien per una nota.
# Ús: python3 apunts.py N [es]   (N = 1..10) → ../1batx-ccss-tN/tN-apunts-teoria[-es].tex
#     i pdflatex dues vegades (per l'índex), amb logo-fentmates.pdf (_eines/logo/pdf/horitzontal-clar.pdf) al costat.
import os, re, sys, math
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))

N = int(sys.argv[1])
ES = len(sys.argv) > 2 and sys.argv[2] == 'es'
LANG = 'es' if ES else 'va'
def T(va, es): return es if ES else va

ARI = dict(c='C99A2E', cl='E6B84A', block=T("bloc d'Aritmètica: groc", 'bloque de Aritmética: amarillo'))
ALG = dict(c='3D6AA0', cl='4E81BD', block=T("bloc d'Àlgebra: blau", 'bloque de Álgebra: azul'))
AN = dict(c='6A8A33', cl='7FA040', block=T("bloc d'Anàlisi: verd", 'bloque de Análisis: verde'))
PR = dict(c='684E88', cl='8064A1', block=T('bloc de Probabilitat i Estadística: morat', 'bloque de Probabilidad y Estadística: morado'))
GEO = dict(c='DC7A29', cl='F79645', block=T('bloc de Geometria: taronja', 'bloque de Geometría: naranja'))
U = {
 1: dict(ARI, src='t1-nombres-reals.html', title=T('Nombres reals', 'Números reales'), card=1,
         kw=T('nombres reals, fracció generatriu, valor absolut, intervals, potències, radicals, racionalització, logaritmes, notació científica',
              'números reales, fracción generatriz, valor absoluto, intervalos, potencias, radicales, racionalización, logaritmos, notación científica')),
 2: dict(ALG, src='t2-algebra.html', title=T('Àlgebra', 'Álgebra'), card=2,
         kw=T('polinomis, identitats notables, regla de Ruffini, teorema del residu, factorització, fraccions algebraiques, equacions, inequacions',
              'polinomios, identidades notables, regla de Ruffini, teorema del resto, factorización, fracciones algebraicas, ecuaciones, inecuaciones')),
 3: dict(ALG, src='t3-sistemes-inequacions.html', title=T("Sistemes d'equacions i inequacions", 'Sistemas de ecuaciones e inecuaciones'), card=3,
         kw=T("sistemes d'equacions, mètode de Gauss, sistemes no lineals, inequacions, sistemes d'inequacions, inequacions amb dues incògnites, semiplans",
              'sistemas de ecuaciones, método de Gauss, sistemas no lineales, inecuaciones, sistemas de inecuaciones, inecuaciones con dos incógnitas, semiplanos')),
 4: dict(AN, src='t4-estudi-funcions.html', title=T('Estudi de funcions', 'Estudio de funciones'), card=6,
         kw=T('funcions, domini, recorregut, talls amb els eixos, monotonia, extrems, continuïtat, simetries, periodicitat, translacions, composició, funció inversa',
              'funciones, dominio, recorrido, cortes con los ejes, monotonía, extremos, continuidad, simetrías, periodicidad, traslaciones, composición, función inversa')),
 5: dict(AN, src='t5-funcions-elementals.html', title=T('Funcions elementals', 'Funciones elementales'), card=7,
         kw=T('funcions lineals, funcions quadràtiques, funcions de proporcionalitat inversa, funcions racionals, funcions radicals, funcions exponencials, funcions logarítmiques, funcions a trossos, valor absolut',
              'funciones lineales, funciones cuadráticas, funciones de proporcionalidad inversa, funciones racionales, funciones radicales, funciones exponenciales, funciones logarítmicas, funciones a trozos, valor absoluto')),
 6: dict(AN, src='t6-limits-continuitat.html', title=T('Límits i continuïtat', 'Límites y continuidad'), card=8,
         kw=T('límits, límits laterals, límits a l\'infinit, indeterminacions, continuïtat, discontinuïtats, asímptotes, teorema de Bolzano',
              'límites, límites laterales, límites en el infinito, indeterminaciones, continuidad, discontinuidades, asíntotas, teorema de Bolzano')),
 7: dict(AN, src='t7-derivades.html', title=T('Derivades i aplicacions', 'Derivadas y aplicaciones'), card=9,
         kw=T('taxa de variació mitjana, derivada en un punt, recta tangent, funció derivada, regles de derivació, monotonia, màxims i mínims, representació de funcions, optimització',
              'tasa de variación media, derivada en un punto, recta tangente, función derivada, reglas de derivación, monotonía, máximos y mínimos, representación de funciones, optimización')),
 8: dict(PR, src='t8-distribucions-bidimensionals.html', title=T('Distribucions bidimensionals', 'Distribuciones bidimensionales'), card=10,
         kw=T('estadística bidimensional, taules de doble entrada, núvol de punts, covariància, correlació, coeficient de correlació, recta de regressió, estimacions',
              'estadística bidimensional, tablas de doble entrada, nube de puntos, covarianza, correlación, coeficiente de correlación, recta de regresión, estimaciones')),
 9: dict(PR, src='t9-combinatoria-probabilitat.html', title=T('Combinatòria i probabilitat', 'Combinatoria y probabilidad'), card='pr',
         kw=T('principi de multiplicació, variacions, permutacions, combinacions, nombres combinatoris, experiments aleatoris, esdeveniments, regla de Laplace, probabilitat condicionada, probabilitat total, teorema de Bayes',
              'principio de multiplicación, variaciones, permutaciones, combinaciones, números combinatorios, experimentos aleatorios, sucesos, regla de Laplace, probabilidad condicionada, probabilidad total, teorema de Bayes')),
 10: dict(PR, src='t10-distribucions-probabilitat.html', title=T('Distribucions de probabilitat', 'Distribuciones de probabilidad'), card='pr',
         kw=T('variable aleatòria, funció de probabilitat, esperança, variància, distribució binomial, distribució normal, campana de Gauss, normal típica, tipificació, aproximació de la binomial per la normal',
              'variable aleatoria, función de probabilidad, esperanza, varianza, distribución binomial, distribución normal, campana de Gauss, normal típica, tipificación, aproximación de la binomial por la normal')),
}[N]

SRC = os.path.join(HERE, '..', '..', '..', 'materials', '1batx-ccss', U['src'])
OUTDIR = os.path.join(HERE, '..', '1batx-ccss-t%d' % N)

# ---------- 1. HTML ----------
src = open(SRC, encoding='utf-8').read()
hero = re.search(r'<section class="hero">.*?<p>[^\n]*?<span data-l="%s">(.*?)</span>' % LANG, src, re.S).group(1)
tocnames = [re.search(r'<span data-l="%s">(.*?)</span>' % LANG, x).group(1)
            for x in re.findall(r'<span class="n">%d\.\d+</span>(.*?)<span class="ck">' % N, src)]
body = src[src.index('<article>') + len('<article>'):min(i for i in (src.find('<section class="unit" id="lab">'), src.find('<section class="unit quiz-sec"')) if i >= 0)]
body = re.sub(r'\\color\{#([0-9a-fA-F]{6})\}', r'\\color[HTML]{\1}', body)

def fix(a, b):
    global body
    assert body.count(a) == 1, a[:80]
    body = body.replace(a, b)
if N == 7:
    body, k = re.subn(r'<h3 class="sub"><span data-l="va">Estudi complet d\'una funció, pas a pas</span>.*?<div class="box lab">.*?</p>\s*</div>\s*</div>', '', body, count=1, flags=re.S)
    assert k == 1

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
        if tag == 'svg': n.pos = self.getpos()  # per a recuperar l'svg tal com és al text font
        if tag not in VOID: self.cur = n
    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))
    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag: n = n.parent
        if n is not None and n.parent is not None: self.cur = n.parent
    def handle_data(self, d): self.cur.kids.append(d)
p = P(); p.feed(body); ROOT = p.root
VNODES = []
def _walk(n):
    for k in n.kids:
        if isinstance(k, str): continue
        if (k.tag == 'figure' and (k.a.get('data-venn') is not None or k.a.get('data-fig'))) or (k.tag == 'svg' and k.a.get('data-nf')): VNODES.append(k)
        _walk(k)
_walk(ROOT)
def vraw(n): return VFIG[VNODES.index(n)]
LINE0 = [0] + [m.end() for m in re.finditer('\n', body)]
def svg_raw(n):  # l'svg original (HTMLParser posa els atributs en minúscula: viewBox, clipPath…)
    i = LINE0[n.pos[0] - 1] + n.pos[1]
    return body[i:body.index('</svg>', i) + 6]

# ---------- 3. figures ----------
FIG = {}
CMP = [0]
# unitats 5-8: les figures fixes de la pàgina (svg.tg-svg, i les gràfiques svg.lp-svg de la U8, que la pàgina dibuixa amb
# JavaScript) es passen a PDF vectorial amb Inkscape, amb els estils de la pàgina (colors del tema clar) dins de l'svg.
# Els PDF es guarden a tN/figs/<hash>.pdf i el .tex els inclou amb \includegraphics.
import hashlib, subprocess
INKSCAPE = '/Applications/Inkscape.app/Contents/MacOS/inkscape'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
FIGDIR = os.path.join(OUTDIR, 'figs')
ROOTVARS = dict(re.findall(r'--([\w-]+):\s*([^;]+);', re.search(r':root\s*\{([^}]*)\}', src).group(1)))
def unvar(x):
    for _ in range(3): x = re.sub(r'var\(--([\w-]+)\)', lambda m: ROOTVARS[m.group(1)].strip(), x)
    return x
def svg_css():
    css = '\n'.join(re.findall(r'<style>(.*?)</style>', src, re.S))
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    while '@media' in css:  # fora les regles del tema fosc i de pantalles menudes
        i = css.index('@media'); j = css.index('{', i); d = 1; k = j + 1
        while d: d += {'{': 1, '}': -1}.get(css[k], 0); k += 1
        css = css[:i] + css[k:]
    out = []
    for sel, decl in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        sels = [x.strip() for x in sel.split(',') if re.match(r'^\.(tg|lp|st|pr|dist)-svg[\s.]', x.strip()) and 'dark' not in x and ':hover' not in x and not re.match(r'^\.\w+-svg$', x.strip())]  # la regla de l'svg (width: 100 %…) no
        if sels: out.append('%s { %s }' % (', '.join(sels), unvar(decl).replace('"Inter"', '"Helvetica Neue"')))
    return '\n'.join(out)
SVGCSS = svg_css() if True else ''
SVGTODO = []
def svgpdf(raw):
    raw = unvar(raw).replace('&nbsp;', '&#160;')
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', raw).group(1).replace(',', ' ').split()]
    head = re.match(r'<svg[^>]*>', raw).group(0)
    new = head[:-1].replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1) if 'xmlns=' not in head else head[:-1]
    new += ' width="%g" height="%g">' % (vb[2], vb[3])
    # el fons arredonit de la figura, com a la web
    new += '<style>%s</style><rect x="%g" y="%g" width="%g" height="%g" rx="12" fill="%s" stroke="%s" stroke-width="1"/>' % (
        SVGCSS, vb[0] + 0.5, vb[1] + 0.5, vb[2] - 1, vb[3] - 1, ROOTVARS['bg'].strip(), ROOTVARS['border'].strip())
    svg = new + raw[len(head):]
    h = hashlib.md5(svg.encode()).hexdigest()[:12]
    os.makedirs(FIGDIR, exist_ok=True)
    f = os.path.join(FIGDIR, h)
    if not os.path.exists(f + '.pdf'):
        if f + '.svg' not in SVGTODO: open(f + '.svg', 'w', encoding='utf-8').write(svg); SVGTODO.append(f + '.svg')
    return 'figs/%s.pdf' % h, vb[2] / vb[3]
def run_inkscape():
    for i in range(0, len(SVGTODO), 40):
        subprocess.run([INKSCAPE, '--export-type=pdf', '--export-area-page', '--export-text-to-path'] + SVGTODO[i:i + 40], check=True, capture_output=True)
    for f in SVGTODO: os.remove(f)
# U8: les gràfiques data-g, del DOM que deixa Chrome després d'executar el JavaScript de la pàgina
DOMG = {}
DOMR = {}
VFIG = []  # svg del DOM de les figures data-venn / data-fig / data-nf, en ordre
if re.search(r'data-(g|venn|fig|nf)="', body):
    dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + __import__('tempfile').mkdtemp(),
                          '--virtual-time-budget=5000', '--dump-dom', 'file://' + os.path.abspath(SRC)], capture_output=True, text=True).stdout
    for m in re.finditer(r'<(?:figure|div) class="[lc]fig[^"]*" data-g="([^"]+)"[^>]*>', dom):
        k = re.compile(r'<svg class="(?:lp|st)-svg".*?</svg>', re.S).search(dom, m.end())
        if k and 'data-g=' not in dom[m.end():k.start()]: DOMG.setdefault(m.group(1), k.group(0))
        e = dom.find('</figure>', m.end()); r = re.search(r'class="rcap">.*?<annotation encoding="application/x-tex">(.*?)</annotation>', dom[m.end():e], re.S)
        if r: DOMR.setdefault(m.group(1), r.group(1).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>'))
    for m in re.finditer(r'<figure[^>]*data-(?:venn|fig)="[^"]*"[^>]*>\s*(<svg class="pr-svg".*?</svg>)|(<svg class="dist-svg" data-nf="[^"]*".*?</svg>)', dom, re.S):
        VFIG.append(m.group(1) or m.group(2))
    assert DOMG or VFIG, 'Chrome no ha deixat cap gràfica'
def incfig(raw, maxw, maxh='5.2cm'):
    f, ar = svgpdf(raw)
    return r'\includegraphics[width=%s,height=%s,keepaspectratio]{%s}' % (maxw, maxh, f)
def figcap(fg):
    cap = next((k for k in elems(fg) if k.tag == 'figcaption'), None)
    return (r'\par\smallskip{\centering\footnotesize %s\par}' % text(cap).strip()) if cap else ''
# alçada (cm) d'un bloc amb figura que no es pot partir: per a reservar-ne l'espai abans (\Needspace) i que no quede
# un títol o el començament d'un requadre sol al final de la pàgina
IN_BOX = [0]
def vb_ar(raw):
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', raw).group(1).replace(',', ' ').split()]
    return vb[2] / vb[3]
def fig_raw(fg):
    if fg.a.get('data-g'): return DOMG.get(fg.a['data-g'])
    if fg in VNODES: return vraw(fg)
    sv = fg if fg.tag == 'svg' else next((k for k in elems(fg) if k.tag == 'svg'), None)
    return (vraw(sv) if sv in VNODES else svg_raw(sv)) if sv is not None else None
def est_h(n, colw=None):
    if isinstance(n, str) or False: return 0
    c = n.cls()
    if (n.tag == 'figure' and ('tfig' in c or 'cfig' in c)) or 'lfig' in c or (n.tag == 'svg' and ('tg-svg' in c or 'lp-svg' in c)):
        raw = fig_raw(n)
        if not raw: return 0
        w = colw or (8.6 if 'w' in c else 5.4 if 'sm' in c else 6.2 if 'tfig' in c or n.tag == 'svg' else 8)
        return min(w / vb_ar(raw), MAXH[0]) + (0.7 if any(k.tag == 'figcaption' for k in elems(n)) else 0) + 0.5
    if 'figs' in c or 'grid3' in c:
        figs = [k for k in elems(n) if k.tag == 'figure']
        per = 2 if 'c2' in c else min(3, len(figs))
        return max([est_h(k, (colw or 18) * 0.98 / per - 0.3) for k in figs[:per]] + [0])
    if 'two' in c or 'cmp' in c:  # dues columnes que no es parteixen: figures + text aproximat
        def col(k):  # figures (recursivament) + línies de text aproximades + capçalera de requadre
            if isinstance(k, str): return 0
            if k.tag == 'figure' or 'figs' in k.cls() or 'lfig' in k.cls(): return est_h(k, 8.6)
            if k.tag in ('p', 'li') or k.tag.startswith('h'): return len(re.sub(r'\s+', ' ', plain(k))) / 48 * 0.6 + 0.3
            return sum(col(x) for x in elems(k)) + (1.2 if 'box' in k.cls() else 0)
        def hasfig(k): return not isinstance(k, str) and (k.tag in ('figure', 'svg') or 'lfig' in k.cls() or any(hasfig(x) for x in elems(k)))
        if not hasfig(n): return 0
        return max([col(k) for k in elems(n)] + [0])
    if n.tag in ('div', 'figure'):
        ks = elems(n)
        hs = [est_h(k, colw) for k in ks]
        return sum(hs) if sum(1 for h in hs if h) > 1 else (hs[0] if hs else 0)  # figures apilades: se sumen
    return 0
def need(h): return ''
# bloc que no es pot partir (figures, dues columnes): LaTeX el mesura i reserva exactament el seu espai (\fmblock)
def hasfigure(k): return not isinstance(k, str) and (k.tag in ('figure', 'svg') or 'lfig' in k.cls() or any(hasfigure(x) for x in elems(k)))
LASTTWO = ['']
FIRSTROW = ['']
def alt(side, stacked):  # dues columnes: si no caben, apilades (el text omple la pàgina i es pot partir)
    LASTTWO[0] = side
    return ('\\fmtwoin{%s}{%s}' if IN_BOX[0] else '\\fmtwo{%s}{%s}') % (side, stacked)
def cellfml(x):  # cel·la d'una graella de fórmules
    if '\\[' in x:
        return re.sub(r'\\\[(.*?)\\\]', lambda m: '$\\displaystyle ' + m.group(1).strip() + '$', x, flags=re.S).strip()
    return x.replace('$', '$\\displaystyle ', 1)
def blk(x): return ('\\fmblock{%s}' % x) if not TWO[0] and not IN_BOX[0] else x
def isblock(k):
    if isinstance(k, str) or False: return False
    c = k.cls()
    return bool({'two', 'cmp', 'figs', 'tfig', 'lfig', 'fig4', 'cfig', 'grid3', 'venn6', 'venn-fig', 'mini-figs'} & set(c)) or (k.tag == 'svg' and ('tg-svg' in c or 'lp-svg' in c))
MAXH = [5.2]
def onefig(fg, maxw):  # <figure> amb un svg (o gràfica data-g) i, potser, un peu
    if fg.a.get('data-g'):
        raw = DOMG[fg.a['data-g']]
    elif fg in VNODES:
        raw = vraw(fg)
    else:
        sv = next((k for k in elems(fg) if k.tag == 'svg'), None)
        if sv is None: return text(fg)
        raw = vraw(sv) if sv in VNODES else svg_raw(sv)
    return '{\\centering %s\\par}%s' % (incfig(raw, maxw, '%.1fcm' % MAXH[0]), figcap(fg))
INF = float('inf')
def num(v): return ('%g' % v).replace('-', '-')
# 1.3: interval menut de la taula (com wMini() de la pàgina de la U1: viewBox 200 × 34, y cap avall)
def parse_iv(s):
    m = re.match(r'^([\[\(])\s*([^,]+?)\s*,\s*([^,]+?)\s*([\]\)])$', s.strip())
    f = lambda x: {'inf': INF, '+inf': INF, '-inf': -INF}.get(x, None) if 'inf' in x else float(x)
    return dict(a=f(m.group(2)), ac=m.group(1) == '[', b=f(m.group(3)), bc=m.group(4) == ']')
def nlmini(s):
    I = parse_iv(s); y, xa, xb, Lx, R = 14, 64, 136, 10, 186
    fa, fb = I['a'] not in (INF, -INF), I['b'] not in (INF, -INF)
    x1 = xa if fa else Lx + 4; x2 = xb if fb else R - 4
    if not fa and fb: x2 = 100
    if fa and not fb: x1 = 100
    g = r'\begin{tikzpicture}[x=0.0125cm,y=-0.0125cm,baseline=-0.2cm]'
    g += r'\draw[fmmuted,line width=0.8pt] (%d,%d)--(%d,%d);\fill[fmmuted] (%d,%d)--++(-8,-4)--++(0,8)--cycle;' % (Lx, y, R, y, R + 6, y)
    g += r'\draw[fmR,line width=2.2pt] (%d,%d)--(%d,%d);' % (x1, y, x2, y)
    if not fa: g += r'\fill[fmR] (%d,%d)--++(9,-6)--++(0,12)--cycle;' % (x1 - 6, y)
    if not fb: g += r'\fill[fmR] (%d,%d)--++(-9,-6)--++(0,12)--cycle;' % (x2 + 6, y)
    for fin, cl, x, t in ((fa, I['ac'], x1, 'a'), (fb, I['bc'], x2, 'b')):
        if not fin: continue
        g += r'\draw[fmR,line width=1.1pt,fill=%s] (%d,%d) circle[radius=4.5];' % ('fmR' if cl else 'white', x, y)
        g += r'\node[font=\footnotesize] at (%d,%d) {$%s$};' % (x, y + 15, t)
    return g + r'\end{tikzpicture}'
# 2.x / 3.3: rectes reals apilades (STACKS i nstack() de la pàgina de la U3); cada interval és [a, a inclòs, b, b inclòs]
def _stacks():
    m = re.search(r'STACKS = \{(.*?)\n  \};', src, re.S)
    if not m: return {}
    js = m.group(1).replace('-INF', '"-I"').replace('INF', '"I"')
    js = re.sub(r'(?m)^(\s*)(\w+):', r'\1"\2":', js); js = re.sub(r'([{,]\s*)(range|rows|sol|l|S):', r'\1"\2":', js)
    js = js.replace('&gt;', '>').replace('&lt;', '<')
    d = __import__('json').loads('{' + js + '}')
    f = lambda v: -INF if v == '-I' else INF if v == 'I' else v
    def tex(l):  # «3x − 2 ≤ x + 4» → 3x-2\leq x+4
        l = l.replace(' ', '').replace('−', '-').replace('≤', '\\leq ').replace('≥', '\\geq ').replace('²', '^2').replace('³', '^3')
        return l.strip()
    return {k: dict(range=tuple(v['range']), rows=[(tex(r['l']), [tuple(f(x) for x in I) for I in r['S']]) for r in v['rows']],
                    sol=[tuple(f(x) for x in I) for I in v['sol']]) for k, v in d.items()}
STACKS = _stacks()
def nstack(key, show):
    d = STACKS[key]; lo, hi = d['range']; Lx, R, rowH = 2.3, 13.0, 0.75
    rows = [(l, S, c, False) for (l, S), c in zip(d['rows'], ('fmA', 'fmB'))]
    if show: rows.append((T(r'\text{Solució}', r'\text{Solución}'), d['sol'], 'fmR', True))
    X = lambda v: Lx + (max(lo, min(hi, v)) - lo) / (hi - lo) * (R - Lx)
    ay = -(len(rows) * rowH + 0.2)
    g = r'\begin{tikzpicture}[line cap=round]'
    if show:
        for I in d['sol']: g += r'\fill[fmR,opacity=0.12] (%.3f,0.1) rectangle (%.3f,%.3f);' % (X(I[0]), X(I[2]), ay)
    marks = sorted({v for _, S in d['rows'] for I in S for v in (I[0], I[2]) if abs(v) != INF})
    for v in marks: g += r'\draw[fmmuted!60,dashed,line width=0.5pt] (%.3f,0.1)--(%.3f,%.3f);' % (X(v), X(v), ay)
    for i, (l, S, c, sol) in enumerate(rows):
        y = -(i * rowH + 0.4)
        g += r'\node[anchor=west,font=\small] at (0,%.3f) {$%s$};' % (y, l)
        g += r'\draw[fmmuted!50,line width=0.6pt] (%.3f,%.3f)--(%.3f,%.3f);' % (Lx, y, R, y)
        if sol and not S: g += r'\node[font=\small] at (%.3f,%.3f) {$\emptyset$};' % ((Lx + R) / 2, y + 0.25)
        for I in S:
            x1, x2 = X(I[0]), X(I[2])
            g += r'\draw[%s,line width=2.6pt] (%.3f,%.3f)--(%.3f,%.3f);' % (c, x1, y, x2, y)
            if I[0] == -INF: g += r'\fill[%s] (%.3f,%.3f)--++(0.3,0.19)--++(0,-0.38)--cycle;' % (c, Lx - 0.25, y)
            if I[2] == INF: g += r'\fill[%s] (%.3f,%.3f)--++(-0.3,0.19)--++(0,-0.38)--cycle;' % (c, R + 0.25, y)
            for v, cl, x in ((I[0], I[1], x1), (I[2], I[3], x2)):
                if abs(v) != INF: g += r'\draw[%s,line width=1.2pt,fill=%s] (%.3f,%.3f) circle[radius=0.13];' % (c, c if cl else 'white', x, y)
    g += r'\draw[fmmuted,line width=0.8pt,-latex] (%.3f,%.3f)--(%.3f,%.3f);' % (Lx - 0.2, ay, R + 0.4, ay)
    for v in range(lo, hi + 1):
        g += r'\draw[fmmuted,line width=0.6pt] (%.3f,%.3f)--++(0,0.12)--++(0,-0.24) node[below,font=\scriptsize,text=fmmuted] {$%d$};' % (X(v), ay, v)
    return g + r'\end{tikzpicture}'
# 3.4-3.5: semiplans solució (wFigs() de la pàgina de la U3): data-half = "a,b,op,c;..." (ax+by op c), data-view = x0,x1,y0,y1
def clip(P, a, b, c, ge):
    s = 1 if ge else -1
    inside = lambda p: s * (a * p[0] + b * p[1] - c) >= -1e-9
    out = []
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]
        if inside(p): out.append(p)
        if inside(p) != inside(q):
            fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
            t = fp / (fp - fq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out
def half(svg):
    V = [float(x) for x in svg.a['data-view'].split(',')]
    cons = [(float(a), float(b), op, float(c)) for a, b, op, c in (s.split(',') for s in svg.a['data-half'].split(';'))]
    P = [(V[0], V[2]), (V[1], V[2]), (V[1], V[3]), (V[0], V[3])]
    for a, b, op, c in cons: P = clip(P, a, b, c, op in ('ge', 'gt'))
    g = r'\begin{tikzpicture}\begin{axis}[fmaxis,axis equal image,width=4.6cm,height=4.6cm,xmin=%g,xmax=%g,ymin=%g,ymax=%g,' % tuple(V)
    g += r'xtick={%s},ytick={%s},minor xtick={%s},minor ytick={%s},grid=both,minor grid style={fmmuted!15},major grid style={fmmuted!15},tick label style={font=\tiny}]' % (
        ','.join('%d' % v for v in range(int(V[0]), int(V[1]) + 1) if v and v % 2 == 0), ','.join('%d' % v for v in range(int(V[2]), int(V[3]) + 1) if v and v % 2 == 0),
        ','.join('%d' % v for v in range(int(V[0]), int(V[1]) + 1)), ','.join('%d' % v for v in range(int(V[2]), int(V[3]) + 1)))
    if len(P) >= 3: g += r'\fill[fmR,opacity=0.22] %s--cycle;' % '--'.join('(axis cs:%.4f,%.4f)' % p for p in P)
    for i, (a, b, op, c) in enumerate(cons):
        col = ('fmA', 'fmB', 'fmV', 'fmK')[i % 4]; dash = ',dash pattern=on 5pt off 3.5pt' if op in ('lt', 'gt') else ''
        if abs(b) > 1e-12: pts = [(V[0] - 1, (c - a * (V[0] - 1)) / b), (V[1] + 1, (c - a * (V[1] + 1)) / b)]
        else: pts = [(c / a, V[2] - 1), (c / a, V[3] + 1)]
        g += r'\draw[%s,line width=1.5pt%s] (axis cs:%.4f,%.4f)--(axis cs:%.4f,%.4f);' % (col, dash, pts[0][0], pts[0][1], pts[1][0], pts[1][1])
    if svg.a.get('data-pt'):
        x, y, k = svg.a['data-pt'].split(',')
        g += r'\node[circle,fill=%s,inner sep=0pt,minimum size=6pt] at (axis cs:%s,%s) {};' % ('fmK' if k == '1' else 'fmR', x, y)
    return g + r'\end{axis}\end{tikzpicture}'

# ---------- 4. conversió a LaTeX ----------
UNI = {'→': r'$\to$', '∞': r'$\infty$', '≪': r'$\ll$', '≤': r'$\leq$', '≥': r'$\geq$', '−': '-', '○': r'$\circ$', '∄': r'$\nexists$',
       '✓': '', '✗': '', '✎': '', '✍': '', '🎓': '', '◉': '', '⚙': '', '⚠': '', '…': r'\dots{}', '×': r'$\times$', '≠': r'$\neq$', '±': r'$\pm$',
       '↗': r'$\nearrow$', '↘': r'$\searrow$', '∩': r'$\cap$', '∪': r'$\cup$', '–': '--', '⇒': r'$\Rightarrow$', '⟺': r'$\Leftrightarrow$',
       '←': r'$\leftarrow$', '∅': r'$\emptyset$', '●': r'$\bullet$', '₁': r'$_1$', '₂': r'$_2$', '₃': r'$_3$', '₄': r'$_4$',
       'ᵗ': r'$^t$', '⁻¹': r'$^{-1}$', '²': r'$^2$', '³': r'$^3$', '½': r'$\frac12$', '√': r'$\surd$', '∈': r'$\in$', '∀': r'$\forall$', '′': r"$'$", '″': r"$''$", '°': r'$^\circ$', 'Σ': r'$\Sigma$', '💡': ''}
if True: UNI['−'] = r'$-$'  # signe menys de veritat (a les taules de signes el guionet no es veu)
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
    if t == 'svg' and 'nl-mini' in c and n.a.get('data-iv'): return nlmini(n.a['data-iv'])
    if t == 'svg' and n.a.get('data-stack'): return '\n\\begin{center}%s\\end{center}\n' % nstack(n.a['data-stack'], n.a.get('data-sol') == '1')
    if t == 'svg' and n.a.get('data-half'): return '\n\\begin{center}%s\\end{center}\n' % half(n)
    if 'fig-half' in c: return text(n)
    if 'ids' in c:  # identitats notables, en dues columnes
        IN_TABLE[0] = True
        cells = [cellfml(text(k).strip()) for k in elems(n)]
        IN_TABLE[0] = False
        rows = [' & '.join(cells[i:i + 2]) + r'\\[4pt]' for i in range(0, len(cells), 2)]
        return '\n\\begin{center}\\renewcommand{\\arraystretch}{1.4}\\begin{tabularx}{\\linewidth}{XX}\n%s\n\\end{tabularx}\\end{center}\n' % '\n'.join(rows)
    if (t == 'figure' and ('tfig' in c or 'cfig' in c) or 'lfig' in c):
        w = {'tfig': '6.2cm', 'lfig': '8cm', 'cfig': '7cm'}['tfig' if 'tfig' in c else 'cfig' if 'cfig' in c else 'lfig']
        if 'w' in c: w = '8.6cm'
        if 'sm' in c: w = '5.4cm'
        if TWO[0] or any(p is not None and 'fig4' in p.cls() for p in (n.parent, n.parent.parent if n.parent else None)): w = '\\linewidth'
        if TWO[0] and MAXH[0] > 4.5:  # figura al costat d'un text: una mica més baixa
            MAXH[0] = 4.5; r = '\n\\par\\medskip\\begin{minipage}{\\linewidth}%s\\end{minipage}\\par\\medskip\n' % onefig(n, w); MAXH[0] = 5.2
            return r
        return '\n' + blk('\\par\\medskip\\begin{minipage}{\\linewidth}%s\\end{minipage}\\par\\medskip' % onefig(n, w)) + '\n'
    if ('figs' in c or 'grid3' in c):  # graella de figures: files de 3 (2 amb .c2)
        figs = [k for k in elems(n) if k.tag == 'figure']
        per = 2 if 'c2' in c else min(3, len(figs))
        rows = [figs[i:i + per] for i in range(0, len(figs), per)]
        MAXH[0] = 3.8 if per >= 3 else 4.6
        out = ''
        for ri, row in enumerate(rows):
            r0 = len(out)
            wd = 0.98 / per
            out += '\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{%.3f\linewidth}\centering %s\end{minipage}' % (wd - 0.015, onefig(k, '\\linewidth')) for k in row)
            out += ('\\hfill' + '\\hspace*{%.3f\\linewidth}' % (wd * (per - len(row)))) if len(row) < per else ''
            out += '\\par\\medskip'
            if ri == 0: FIRSTROW[0] = out[r0:]; out = out[:r0] + blk(out[r0:])
            out += '\n'
        MAXH[0] = 5.2
        return '\n' + out
    if t == 'svg' and ('tg-svg' in c or 'lp-svg' in c):
        return '\n\\begin{center}%s\\end{center}\n' % incfig(svg_raw(n), '6.2cm')
    if 'fml' in c:  # fórmules en dues columnes
        IN_TABLE[0] = True
        cells = [cellfml(text(k).strip()) for k in elems(n)]
        IN_TABLE[0] = False
        rows = [' & '.join(cells[i:i + 2]) + r'\\[4pt]' for i in range(0, len(cells), 2)]
        return '\n\\begin{center}\\renewcommand{\\arraystretch}{1.4}\\begin{tabularx}{\\linewidth}{XX}\n%s\n\\end{tabularx}\\end{center}\n' % '\n'.join(rows)
    if n.a.get('data-g'): return '\n\\begin{center}%s\\end{center}\n' % FIG.get(n.a['data-g'], r'\fbox{FIG %s}' % n.a['data-g'])
    if n.a.get('data-sf'): return '\n\\begin{center}%s\\end{center}\n' % sfplot(n.a['data-sf'], '6.4cm', '4.6cm')
    if 'sfig' in c:  # gràfiques dels exemples resolts, en una fila
        figs = elems(n); k = len(figs); w = 0.98 / k
        cell = lambda fg: sfplot(next(x for x in elems(fg) if x.a.get('data-sf')).a['data-sf'], '%.1fcm' % (17.5 * w), '%.1fcm' % (min(4.6, 13 * w))) + \
            r'\par{\footnotesize %s\par}' % ''.join(text(x) for x in elems(fg) if x.tag == 'figcaption').strip()
        return '\n\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{%.3f\linewidth}\centering %s\end{minipage}' % (w - 0.01, cell(fg)) for fg in figs) + '\\par\\medskip\n'
    if t == 'figure' and 'lfig' in c and any(not isinstance(k, str) and k.tag == 'svg' for k in n.kids):
        return '\n\\begin{center}%s\\end{center}\n' % SANDWICH
    if t == 'svg' and n.a.get('data-nf'):  # campana de Gauss soltada (sense <figure>)
        return '\n' + blk('\\par\\medskip{\\centering %s\\par}\\medskip' % incfig(vraw(n), '6.2cm')) + '\n'
    if t == 'figure' and n in VNODES:  # Venn o arbre
        w = '\\linewidth' if TWO[0] else ('7.4cm' if n.a.get('data-fig') == 'tree' else '6cm')
        return '\n' + blk('\\par\\medskip\\begin{minipage}{\\linewidth}%s\\end{minipage}\\par\\medskip' % onefig(n, w)) + '\n'
    if 'venn6' in c or 'mini-figs' in c:  # graella de diagrames de Venn o de campanes: files de 3
        figs = [k for k in elems(n) if k.tag == 'figure']
        rows = [figs[i:i + 3] for i in range(0, len(figs), 3)]
        MAXH[0] = 3.4
        out = ''
        for row in rows:
            out += blk('\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{0.31\linewidth}\centering %s\end{minipage}' % onefig(k, '\\linewidth') for k in row)
                       + ('\\hfill\\hspace*{%.3f\\linewidth}' % (0.33 * (3 - len(row))) if len(row) < 3 else '') + '\\par\\medskip') + '\n'
        MAXH[0] = 5.2
        return '\n' + out
    if 'cmp' in c:
        cols = elems(n)
        box = r'\begin{tcolorbox}[enhanced,colback=fmsurface,colframe=fmmuted!35,arc=2.5mm,boxrule=0.6pt,left=2.5mm,right=2.5mm,top=1.5mm,bottom=1.5mm,before upper=\raggedright,equal height group=cmp%d]%s\end{tcolorbox}'
        CMP[0] += 1
        side = '\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{0.488\linewidth}\vspace{0pt}%s\end{minipage}' % (box % (CMP[0], text(k).strip())) for k in cols) + '\\par\\medskip'
        if not TWO[0]:
            sbox = r'\begin{tcolorbox}[enhanced,breakable,colback=fmsurface,colframe=fmmuted!35,arc=2.5mm,boxrule=0.6pt,left=2.5mm,right=2.5mm,top=1.5mm,bottom=1.5mm,before upper=\raggedright]%s\end{tcolorbox}'
            return '\n' + alt(side, ''.join(sbox % text(k).strip() for k in cols)) + '\n'
        return '\n' + blk(side) + '\n'
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
    if t == 'h3': return '\n\\Needspace{6\\baselineskip}\n\\subsection*{%s}\n' % text(n).strip()
    if 'box' in c and 'lab' in c:
        if N == 10 and re.search(r'Taula de la distribució (binomial|normal)', plain(n)):  # taules: ací només una nota, la taula va a l'annex
            lbl = 'tbin' if 'binomial' in plain(n) else 'tnorm'
            return '\n\\begin{fmnote}%s\\end{fmnote}\n' % (T(r"\textbf{La taula.} La taula completa, la mateixa que s'adjunta a l'examen de la PAU, és a l'annex (pàgina \pageref{%s}).",
                                                              r"\textbf{La tabla.} La tabla completa, la misma que se adjunta al examen de la PAU, está en el anexo (página \pageref{%s}).") % lbl)
        return ''
    if 'box' in c:
        kind = [k for k in ('def', 'prop', 'ex', 'warn') if k in c][0]
        bh = next(k for k in elems(n) if 'bh' in k.cls())
        bb = next(k for k in elems(n) if 'bb' in k.cls())
        IN_TABLE[0] = True  # fórmules del títol com a $...$
        title = text(bh).strip()
        IN_TABLE[0] = False
        IN_BOX[0] += 1
        inner = text(bb).strip()
        IN_BOX[0] -= 1
        if TWO[0] or IN_BOX[0]: return '\n\\begin{fm%s}{%s}\n%s\n\\end{fm%s}\n' % (kind, title, inner, kind)
        if elems(bb) and isblock(elems(bb)[0]):
            IN_BOX[0] += 1; LASTTWO[0] = ''; fb = conv(elems(bb)[0]).strip(); IN_BOX[0] -= 1
            if fb.startswith('\\fmtwoin{'):
                return '\n\\fmboxneedalt{%s}\n\\begin{fm%s}{%s}\n%s\n\\end{fm%s}\\global\\fmstackfalse\n' % (LASTTWO[0], kind, title, inner, kind)
            if 'figs' in elems(bb)[0].cls() or 'grid3' in elems(bb)[0].cls(): fb = FIRSTROW[0]  # només la primera fila
            return '\n\\fmboxneed{%s}\n\\begin{fm%s}{%s}\n%s\n\\end{fm%s}\n' % (fb, kind, title, inner, kind)
        ns = '5\\baselineskip'
        return '\n\\Needspace{%s}\n\\begin{fm%s}{%s}\n%s\n\\end{fm%s}\n' % (ns, kind, title, inner, kind)
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
    if t in ('em', 'i'):
        if re.match(r'(Demostr|Proof)', plain(n).strip()): return r'\textbf{%s}' % text(n)
        return r'\emph{%s}' % text(n)
    if t == 'u': return r'\underline{%s}' % text(n)
    if t == 'sup': return r'\textsuperscript{%s}' % text(n)
    if t == 'sub': return r'\textsubscript{%s}' % text(n)
    if t == 'code': return r'\texttt{%s}' % text(n)
    if t == 'small': return r'{\footnotesize %s}' % text(n)
    if t == 'span':
        if 'key' in c: return r'\fmkey{%s}' % text(n)
        if 'rcap' in c:
            f = n
            while f is not None and not f.a.get('data-g'): f = f.parent
            return ('$%s$' % DOMR[f.a['data-g']]) if f is not None and f.a['data-g'] in DOMR else ''
        if 'sp' in c: return r'\textcolor{fmok}{\textbf{+}}'
        if 'sm' in c: return r'\textcolor{fmas}{$\boldsymbol{-}$}'
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
        was = TWO[0]; TWO[0] = True
        for i in range(0, len(cols), 2):
            pair = cols[i:i + 2]
            out.append('\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{0.48\linewidth}\vspace{0pt}\raggedright %s\end{minipage}' % conv_cell(k).strip() for k in pair) + '\\par\\medskip')
        TWO[0] = was
        if not was and len(cols) == 2 and any(hasfigure(k) for k in cols):
            figc = [k for k in cols if (k.tag == 'figure' or 'figs' in k.cls() or 'lfig' in k.cls()) or (hasfigure(k) and not plain(k).strip())]
            txtc = [k for k in cols if k not in figc]
            st = ''.join((conv(k) if 'box' in k.cls() else '\n\n' + text(k).strip() + '\n\n') for k in txtc)
            TWO[0] = True
            st += ''.join('\n\\begin{center}\\begin{minipage}{0.62\\linewidth}\\centering %s\\end{minipage}\\end{center}\n' % conv_cell(k).strip() for k in figc)
            TWO[0] = was
            return '\n' + alt(out[0], st) + '\n'
        return '\n' + ''.join(blk(x) + '\n' for x in out)
    if t == 'table': return conv_table(n)
    return text(n)

TWO = [False]
def conv_cell(k):
    if k.tag == 'figure' or 'figs' in k.cls(): return conv(k)
    if 'box' in k.cls(): return conv(k)  # requadre dins d'una columna
    if sum(1 for x in elems(k) if x.tag == 'figure') > 1:  # dues figures o més una davall de l'altra
        MAXH[0] = 4.0
        r = text(k)
        MAXH[0] = 5.2
        return r
    return text(k)

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
        cells = [[('$' + x.replace('$-$', '-').strip('$').replace('\\mathbf ', '') + '$') if x else '' for x in r] for r in cells]
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
        if not any('rowspan' in c.a for r2 in rows for c in elems(r2)) and len(rows) >= 4:
            # una tabularx per fila (les columnes fan el mateix ample en totes): la taula es pot partir entre files
            # i no salta sencera a la pàgina següent deixant un forat
            head, *body = s.split('\n')[:-1]
            spec = head[:head.index(r'\toprule')]
            lines = [head + '\n' + body[0] + '\n' + body[1]] + [spec + x for x in body[2:]]
            lines = [x + ('\\bottomrule' if i == len(lines) - 1 else '') + '\\end{tabularx}' for i, x in enumerate(lines)]
            return ('\n\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\setlength{\\parskip}{0pt}'
                    + '\\par\\nointerlineskip\\vskip0pt\n'.join(lines) + '\\end{center}\n')
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
    return '\n\\Needspace{8\\baselineskip}\n\\section{%s}\n' % title + ''.join(conv(k) for k in n.kids)

latex = conv(ROOT)
run_inkscape()
latex = re.sub(r'\n{3,}', '\n\n', latex)
latex = re.sub(r'(?<!\\)\\\[', '\n\\[', latex)
latex = re.sub(r'(?<!\\)\\\]', '\\]\n', latex)
latex = re.sub(r'\\\]\s*([.,;])', r'\\,\1\\]', latex)  # el punt final va dins de la fórmula centrada
latex = re.sub(r'[ \t]+\n', '\n', latex)
latex = re.sub(r'\n{3,}', '\n\n', latex)
# fórmules centrades: \fmdisp{...} (s'encongeix si no cap en l'amplada de la línia)
latex = re.sub(r'(?<!\\)\\\[(.*?)(?<!\\)\\\]', lambda m: r'\fmdisp{%s}' % m.group(1).strip(), latex, flags=re.S)
# un títol seguit directament d'una caixa: una sola reserva d'espai abans del títol (si no, el \Needspace de la caixa
# fa saltar de pàgina just després del títol i el deixa sol al final de la pàgina)
# (també una cadena apartat + subapartat + caixa); la reserva compta el títol i les primeres línies de la caixa
HEADR = r'\\Needspace\{(\d+)\\baselineskip\}(\n(?:\\(?:sub)?section\*?\{[^\n]*\n)+)\s*\\Needspace\{\d+\\baselineskip\}\n'
def _cm(x): return float(x[:-2]) if x.endswith('cm') else int(x.split('\\')[0]) * 0.57
HEADR2 = r'\\Needspace\{([^}]+)\}(\n(?:\\(?:sub)?section\*?\{[^\n]*\n)+)\s*\\Needspace\{([^}]+)\}\n'
if True:
    HB = r'\\Needspace\{[^}]+\}(\n(?:\\(?:sub)?section\*?\{[^\n]*\n)+)\s*\\fm(block|boxneedalt|boxneed|two)\{'
    latex = re.sub(HB, lambda m: '\\fmhead%s{%s}{' % ({'block': 'block', 'boxneed': 'box', 'boxneedalt': 'boxalt', 'two': 'two'}[m.group(2)], m.group(1)), latex)
    while re.search(HEADR2, latex):
        latex = re.sub(HEADR2, lambda m: '\\Needspace{%.1fcm}' % max(_cm(m.group(1)) + (0 if 'cm' in m.group(1) else 0), (11 if m.group(2).count('section') > 1 else 10 if '\\section{' in m.group(2) else 9) * 0.57,
                                                                   _cm(m.group(3)) + m.group(2).count('\\section{') * 1.6 + m.group(2).count('\\subsection') * 1.0) + m.group(2), latex)
while re.search(HEADR, latex):
    latex = re.sub(HEADR, lambda m: '\\Needspace{%d\\baselineskip}' % (10 if m.group(2).count('section') > 1 else 8 if '\\section{' in m.group(2) else 7) + m.group(2), latex)

# títols d'apartat de dues línies: la reserva d'espai compta la segona línia (si no, el títol queda sol al final de la pàgina)
def _long(m):
    v, title = m.group(1), m.group(2)
    if len(title) < 52: return m.group(0)
    cm = float(v[:-2]) if v.endswith('cm') else int(v.split('\\')[0]) * 0.57
    return '\\Needspace{%.1fcm}\n\\section{%s}' % (cm + 1.6, title)
latex = re.sub(r'\\Needspace\{([^}]+)\}\n\\section\{([^\n]*?)\}', _long, latex)

# ---------- 5. document ----------
CARD = {
 1: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=3.2pt,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw (14,80)--(226,80) (216,72)--(228,80)--(216,88);
  \draw[line width=2.4pt] (40,74)--(40,86) (100,74)--(100,86) (160,74)--(160,86);
  \foreach \x/\t in {40/0,100/1,160/2} \node[anchor=base,inner sep=0pt,font=\fontsize{18}{18}\sffamily\bfseries] at (\x,106) {\t};
  \draw[line width=2.2pt,opacity=0.6] (40,80)--(40,20)--(100,20);
  \draw[line width=2.4pt] (40,80)--(100,20);
  \draw[dash pattern=on 6pt off 6pt] (100,20) arc[start angle=45,end angle=0,radius=84.85];
  \fill (125,80) circle (6.5) (194,80) circle (5);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{20}{20}\selectfont] at (108,62) {$\sqrt2$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{20}{20}\selectfont] at (186,50) {$\pi$};
  \end{scope}
\end{tikzpicture}''',
 2: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=3pt,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \node[anchor=base west,inner sep=0pt,font=\fontsize{26}{26}\selectfont] at (14,44) {$P(x)=x^2+3x-4$};
  \draw[line width=2.4pt] (40,62) rectangle (84,106) (88,62) rectangle (106,106);
  \fill[opacity=0.3] (40,62) rectangle (84,106);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{17}{17}\selectfont] at (52,90) {$x^2$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{17}{17}\selectfont] at (91,90) {$x$};
  \draw[line width=3.2pt] (140,106) .. controls (160,106) and (166,66) .. (186,66) .. controls (206,66) and (214,100) .. (226,74);
  \draw[line width=2pt,opacity=0.6] (134,106)--(230,106);
  \end{scope}
\end{tikzpicture}''',
 3: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=4pt,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw (20,106)--(220,20);
  \draw[opacity=0.75] (20,26)--(220,96);
  \draw[opacity=0.55] (128,6)--(128,114);
  \fill (128,59.5) circle (7);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{21}{21}\selectfont] at (18,124) {$x+y+z=6$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{21}{21}\selectfont] at (150,12) {$2x-y=1$};
  \end{scope}
\end{tikzpicture}''',
 4: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=3pt,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=2.4pt,opacity=0.7] (14,100)--(226,100) (40,114)--(40,6);
  \draw[line width=3.6pt] (24,112)--(224,18);
  \fill (76,87.6) circle (6) (172,42.5) circle (6);
  \draw[line width=3.6pt] (76,87.6)--(150,52.8) (140,50)--(150,52.8)--(144,61);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{22}{22}\selectfont] at (112,92) {$\vec v$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{22}{22}\selectfont] at (196,64) {$r$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{19}{19}\selectfont] at (50,34) {$ax+by+c=0$};
  \end{scope}
\end{tikzpicture}''',
 5: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=3pt,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=2.2pt,opacity=0.7] (20,64)--(220,64) (120,4)--(120,124);
  \draw (120,64) circle (52);
  \draw[line width=3.6pt] (120,64)--(159.8,30.6);
  \draw[line width=3.6pt,dash pattern=on 7pt off 6pt] (159.8,30.6)--(159.8,64);
  \fill[opacity=0.4] (120,64)--(140,64) arc[start angle=0,end angle=40,radius=20]--cycle;
  \fill (159.8,30.6) circle (5.5);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{20}{20}\selectfont] at (146,84) {$\alpha$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{18}{18}\selectfont] at (166,52) {$\sin\alpha$};
  \end{scope}
\end{tikzpicture}''',
 6: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round,line join=round]
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
 7: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,104)--(226,104) (110,114)--(110,6);
  \draw[line width=4.5pt] (30,100) .. controls (90,100) and (120,80) .. (150,40) .. controls (160,26) and (166,14) .. (172,6);
  \draw[line width=4.5pt,opacity=0.75] (122,114) .. controls (126,70) and (150,56) .. (226,48);
  \draw[line width=4.5pt,opacity=0.55] (40,10) .. controls (80,140) and (140,140) .. (180,10);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{20}{20}\selectfont] at (176,30) {$e^x$};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{20}{20}\selectfont] at (190,72) {$\ln x$};
  \end{scope}
\end{tikzpicture}''',
 8: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,104)--(226,104) (24,114)--(24,8);
  \draw[line width=4pt,dash pattern=on 10pt off 10pt] (24,36)--(226,36);
  \draw[line width=4.5pt] (32,100) .. controls (70,98) and (92,80) .. (112,64);
  \draw[line width=4.5pt] (122,58) .. controls (150,44) and (180,40) .. (222,38);
  \draw[line width=4.5pt] (117,61) circle (5.5);
  \node[anchor=base west,inner sep=0pt,scale=2.4,font=\large\itshape] at (138,84) {lím $f(x)=L$};
  \end{scope}
\end{tikzpicture}''',
 9: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,104)--(226,104) (24,114)--(24,8);
  \draw[line width=4.5pt] (30,96) .. controls (70,94) and (110,70) .. (140,44) .. controls (160,26) and (180,14) .. (220,8);
  \draw[line width=4pt,opacity=0.6] (60,112)--(220,4);
  \fill (128,54) circle (6);
  \node[anchor=base west,inner sep=0pt,scale=2.4,font=\large\itshape] at (138,90) {$f'(a)=m$};
  \end{scope}
\end{tikzpicture}''',
 10: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (14,104)--(226,104) (24,114)--(24,8);
  \foreach \x/\y in {40/92,58/84,66/90,80/74,92/78,104/64,116/68,128/56,140/60,152/46,166/50,178/38,192/34,206/26}
    \fill (\x,\y) circle (5);
  \draw[line width=4pt,opacity=0.7] (30,98)--(222,22);
  \node[anchor=base west,inner sep=0pt,scale=2.2,font=\large\itshape] at (150,96) {$r\approx0{,}9$};
  \end{scope}
\end{tikzpicture}''',
}
CARD['pr'] = r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=3pt,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \fill (20,60) circle[radius=5];
  \draw (20,60)--(80,26) (20,60)--(80,94) (80,26)--(130,12) (80,26)--(130,40) (80,94)--(130,80) (80,94)--(130,108);
  \fill (80,26) circle[radius=4] (80,94) circle[radius=4] (130,12) circle[radius=3.5] (130,40) circle[radius=3.5] (130,80) circle[radius=3.5] (130,108) circle[radius=3.5];
  \node[anchor=base west,inner sep=0pt,font=\fontsize{18}{18}\selectfont\itshape] at (36,36) {0,6};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{18}{18}\selectfont\itshape] at (36,92) {0,4};
  \begin{scope}[rotate around={-12:(190,58)}]
    \draw[rounded corners=0.74cm] (162,30) rectangle (218,86);
    \fill (176,44) circle[radius=4.5] (190,58) circle[radius=4.5] (204,72) circle[radius=4.5];
  \end{scope}
  \end{scope}
\end{tikzpicture}'''
CARD = CARD[U['card']]

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
\definecolor{fmA}{HTML}{3B82F6}\definecolor{fmB}{HTML}{F97316}\definecolor{fmR}{HTML}{E11D48}\definecolor{fmK}{HTML}{16A34A}\definecolor{fmV}{HTML}{7C3AED}

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
\titlespacing*{\section}{0pt}{10pt}{4pt}
\titleformat*{\subsection}{\color{fmgreen}\large\bfseries}
\titlespacing*{\subsection}{0pt}{6pt plus 2pt}{0pt}
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
\newtcolorbox{fmnote}[1][]{enhanced,breakable,colback=white,colframe=white,borderline west={3pt}{0pt}{fmaccent},arc=0pt,left=3mm,right=2mm,top=1mm,bottom=1mm,before skip=6pt,after skip=6pt,before upper=\raggedright,#1}
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
{\raggedright\color{white}\fontsize{25}{30}\selectfont\bfseries{\color{UNUMCOL}UNITNUM} · UNITTITLE\par}
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
             ('PDFTITLE', T('Apunts de teoria. Unitat %d: %s. 1r de Batxillerat CCSS', 'Apuntes de teoría. Unidad %d: %s. 1.º de Bachillerato CCSS') % (N, U['title'])),
             ('PDFSUBJ', T('Matemàtiques Aplicades a les Ciències Socials I', 'Matemáticas Aplicadas a las Ciencias Sociales I')), ('PDFKW', U['kw']),
             ('BLOCKCOL', U['block']), ('COLC', U['c']), ('COLL', U['cl']), ('UNITN', str(N)), ('CARD', CARD),
             ('HEADTXT', T('1r Batxillerat CCSS · Unitat %d: %s', '1.º Bachillerato CCSS · Unidad %d: %s') % (N, U.get('short', U['title'])))]:
    pre = pre.replace(a, b)
if True:
    i = pre.index(r'\newcommand{\fmm}[1]'); j = pre.index('\n', i)
    pre = pre[:i] + r'''% fórmula en línia; si ocupa més del 80 % de la línia, va centrada (amb la puntuació que la segueix)
\makeatletter
\newcommand{\fmm}[1]{\setbox0=\hbox{$#1$}\ifdim\wd0>0.8\linewidth\def\fmmnext{\fmmdisp{#1}}\else\def\fmmnext{\mbox{\box0}}\fi\fmmnext}
\def\fmmdisp#1{\@ifnextchar.{\fmmdispp{#1}}{\@ifnextchar,{\fmmdispc{#1}}{\@ifnextchar;{\fmmdisps{#1}}{\fmdisp{#1}}}}}
\def\fmmdispp#1.{\fmdisp{#1\,.}}\def\fmmdispc#1,{\fmdisp{#1\,,}}\def\fmmdisps#1;{\fmdisp{#1\,;}}
\makeatother''' + pre[j:]
    pre = pre.replace('\\newcommand{\\lt}', r'''% blocs que no es poden partir: es mesuren i es reserva exactament el seu espai (amb el títol o la capçalera del requadre)
\newsavebox{\fmkb}
\newcommand{\fmmeasure}[2]{\setbox\fmkb=\vbox{\hsize=\dimexpr\linewidth-#1\relax\linewidth=\hsize #2}}
\newcommand{\fmblock}[1]{\fmmeasure{0pt}{#1}\Needspace{\dimexpr\ht\fmkb+\dp\fmkb\relax}#1}
\newcommand{\fmheadblock}[2]{\fmmeasure{0pt}{#2}\Needspace{\dimexpr\ht\fmkb+\dp\fmkb+2.2cm\relax}#1#2}
\newcommand{\fmboxneed}[1]{\fmmeasure{9mm}{#1}\Needspace{\dimexpr\ht\fmkb+\dp\fmkb+1.6cm\relax}}
\newif\iffmstack\newif\iffmfit
\newcommand{\fmfits}[1]{\par\ifdim\dimexpr\pagegoal-\pagetotal\relax<\dimexpr\ht\fmkb+\dp\fmkb+#1\relax\global\fmfitfalse\else\global\fmfittrue\fi}
\newcommand{\fmtwo}[2]{\fmmeasure{0pt}{#1}\fmfits{0pt}\iffmfit #1\else #2\fi}
\newcommand{\fmheadtwo}[3]{\fmmeasure{0pt}{#2}\fmfits{2.2cm}\iffmfit #1#2\else\Needspace{\dimexpr1.6cm+7\baselineskip\relax}#1#3\fi}
\newcommand{\fmtwoin}[2]{\iffmstack #2\else #1\fi}
\newcommand{\fmboxneedalt}[1]{\fmmeasure{9mm}{#1}\fmfits{1.6cm}\iffmfit\global\fmstackfalse\else\global\fmstacktrue\Needspace{8\baselineskip}\fi}
\newcommand{\fmheadboxalt}[2]{\fmmeasure{9mm}{#2}\fmfits{3.4cm}\iffmfit\global\fmstackfalse\else\global\fmstacktrue\Needspace{\dimexpr2.4cm+5\baselineskip\relax}\fi#1}
\newcommand{\fmheadbox}[2]{\fmmeasure{9mm}{#2}\Needspace{\dimexpr\ht\fmkb+\dp\fmkb+3.4cm\relax}#1}
\newcommand{\lt}''', 1)
hero_tex = re.sub(r'</?strong>', '', hero_tex)  # la descripció del web porta etiquetes HTML
title = TITLE.replace('HERO', hero_tex).replace('TOC1', '\n'.join(toc[:half])).replace('TOC2', '\n'.join(toc[half:]))
for a, b in [('KICKER', T('Apunts de teoria · 1r Batxillerat · Matemàtiques Aplicades a les Ciències Socials I', 'Apuntes de teoría · 1.º Bachillerato · Matemáticas Aplicadas a las Ciencias Sociales I')),
             ('UNITNUM', unit), ('UNUMCOL', 'fmnavy' if U['c'] == 'C99A2E' else 'fmyellow'), ('CARDY', '-1.3'), ('UNITTITLE', U['title']), ('TOCWORD', T('Índex', 'Índice'))]:
    title = title.replace(a, b)
ANNEX = ''
if N == 10:
    PS = [("0,01", 0.01), ("0,05", 0.05), ("0,10", 0.10), ("0,15", 0.15), ("0,20", 0.20), ("0,25", 0.25), ("0,30", 0.30),
          ("1/3", 1 / 3), ("0,35", 0.35), ("0,40", 0.40), ("0,45", 0.45), ("0,49", 0.49), ("0,50", 0.50)]
    def c4(v): return ("%.4f" % v).replace(".", ",")
    def Phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
    def taula_binomial():
        s = r'\begin{tabular}{cc|%s}\toprule' % ('c' * len(PS)) + '\n'
        s += r'\multirow{2}{*}{$n$} & \multirow{2}{*}{$x$} & \multicolumn{%d}{c}{$p$}\\' % len(PS) + '\n'
        s += r' & & ' + ' & '.join(r'\textbf{%s}' % l for l, _ in PS) + r'\\' + '\n'
        for n in range(2, 10):
            s += r'\midrule' + '\n'
            for x in range(n + 1):
                s += (r'\multirow{%d}{*}{\textbf{%d}}' % (n + 1, n) if x == 0 else '') + ' & \\textbf{%d} & ' % x
                s += ' & '.join(c4(math.comb(n, x) * p ** x * (1 - p) ** (n - x)) for _, p in PS) + r'\\' + '\n'
        return s + r'\bottomrule\end{tabular}'
    def taula_normal():
        s = r'\begin{tabular}{c|cccccccccc}\toprule' + '\n'
        s += r'$z$ & ' + ' & '.join(r'\textbf{0,0%d}' % c for c in range(10)) + r'\\\midrule' + '\n'
        for r in range(40):
            s += r'\textbf{%s} & ' % ("%.1f" % (r / 10)).replace(".", ",") + ' & '.join(c4(Phi(r / 10 + c / 100)) for c in range(10)) + r'\\'
            s += (r'[2pt]' if r % 5 == 4 and r < 39 else '') + '\n'
        return s + r'\bottomrule\end{tabular}'
    # els valors de la taula de la pàgina (data-c) han de coincidir amb els calculats
    pag = set(re.findall(r'<td[^>]*data-c[^>]*>(0,\d{4})</td>', src))
    assert pag and pag <= set(re.findall(r'0,\d{4}', taula_binomial() + taula_normal())), 'les taules no coincideixen amb la pàgina'
    ANNEX = r'''
\clearpage
\hypertarget{annex}{}\phantomsection
{\color{fmnavy}\Large\bfseries\colorbox{fmdef}{\color{white}\strut\ %s\ }\hspace{0.6em}%s\par}\vspace{2pt}{\color{fmdef}\titlerule[1.2pt]}
\vspace{6pt}
\label{tbin}{\color{fmgreen}\large\bfseries %s}\par\smallskip
%s\par\smallskip
\begin{center}\linespread{1}\selectfont\scriptsize\setlength{\tabcolsep}{4.2pt}\renewcommand{\arraystretch}{1.0}
%s
\end{center}
\clearpage
\label{tnorm}{\color{fmgreen}\large\bfseries %s}\par\smallskip
%s\par\smallskip
\begin{center}\linespread{1}\selectfont\small\setlength{\tabcolsep}{6pt}\renewcommand{\arraystretch}{1.08}
%s
\end{center}
''' % (T('Annex', 'Anexo'), T('Taules de la binomial i de la normal', 'Tablas de la binomial y de la normal'),
       T('Taula de la distribució binomial', 'Tabla de la distribución binomial'),
       T(r"Dona \fmm{P[X=x]=\binom nx\,p^x(1-p)^{n-x}} per a \fmm{n=2,\dots,9}.\newline Si \fmm{p\gt0{,}5}, compta els fracassos: \fmm{Y=n-X\sim B(n,1-p)} (apartat 10.4).",
         r"Da \fmm{P[X=x]=\binom nx\,p^x(1-p)^{n-x}} para \fmm{n=2,\dots,9}.\newline Si \fmm{p\gt0{,}5}, cuenta los fracasos: \fmm{Y=n-X\sim B(n,1-p)} (apartado 10.4)."),
       taula_binomial(),
       T('Taula de la distribució normal $N(0,1)$', 'Tabla de la distribución normal $N(0,1)$'),
       T(r"Dona \fmm{F(z)=P(Z\leq z)}, l'àrea a l'esquerra de \fmm{z}. La fila dona les unitats i les dècimes de \fmm{z}; la columna, les centèsimes (apartat 10.7).",
         r"Da \fmm{F(z)=P(Z\leq z)}, el área a la izquierda de \fmm{z}. La fila da las unidades y las décimas de \fmm{z}; la columna, las centésimas (apartado 10.7)."),
       taula_normal())
    pre = pre.replace('\\usepackage{booktabs}', '\\usepackage{booktabs,multirow}')
    title = title.replace('\\end{minipage}\n\\end{tcolorbox}', '\\mbox{\\hyperlink{annex}{\\textbf{\\color{fmgreen}%s}\\ \\ %s}}\\end{minipage}\n\\end{tcolorbox}' % (T('Annex', 'Anexo'), T('Taules', 'Tablas')), 1)
doc = pre + title + latex + ANNEX + '\n\\end{document}\n'

# retocs sobre el .tex (valen per als dos idiomes)
def retoc(a, b, regex=False):
    global doc
    if regex:
        doc, k = re.subn(a, b, doc, flags=re.S)
        assert k == 1, a[:80]
    else:
        assert doc.count(a) == 1, a[:80]
        doc = doc.replace(a, b)
# (retocs de l'autor de cada unitat, després de revisar el PDF en valencià)
if N == 1:  # retocs de l'autor (Desktop, revisió 2026-11-25): salt de pàgina abans de l'exemple d'equacions amb valor absolut
    retoc(r'\\Needspace\{5\\baselineskip\}\n(\\begin\{fmex\}\{E\w+ res\w+: (?:equacions|ecuaciones) (?:amb|con) valor absoluto?\})', r'\\newpage\n%\\Needspace{5\\baselineskip}\n\1' if not ES else r'\\Needspace{5\\baselineskip}\n\1', True)  # en castellà el salt deixava la pàgina 4 quasi buida
    # tot l'apartat 1.4 a la pàgina 4: els passos curts dels exemples, en una sola línia
    retoc('\\fmm{2x-3=7\\ \\Rightarrow\\ x=5}\n\n\\fmm{2x-3=-7\\ \\Rightarrow\\ x=-2}\n\n', '\\fmm{2x-3=7\\ \\Rightarrow\\ x=5}\\ \\ o\\ \\ \\fmm{2x-3=-7\\ \\Rightarrow\\ x=-2}. ')
    retoc(r'(\\fmm\{-9\\le 3x-6\\le 9\})\n\n', r'\1. ', True)
    retoc(r'(\\fmm\{\\ -3\\le 3x\\le 15\})\n\n', r'\1. ', True)
    retoc('\\fmm{-2x+4\\gt 6\\ \\ \\text{o}\\ \\ -2x+4\\lt -6}\n\n\\fmm{', '\\fmm{-2x+4\\gt 6\\ \\ \\text{o}\\ \\ -2x+4\\lt -6\\ \\ \\Rightarrow\\ \\ ')
    retoc(r'(-2x\\lt -10\})\n\n', r'\1. ', True)
    retoc('\\ x\\lt -1\\ \\ \\text{o}\\ \\ x\\gt 5}\n\n\\fmm{x\\in', '\\ x\\lt -1\\ \\ \\text{o}\\ \\ x\\gt 5\\ \\Rightarrow\\ x\\in')
    retoc('\\fmm{A\\cup B=[-3,\\,5]}\n\n\\fmm{B\\cap C=[4,\\,5]}\n\n', '\\fmm{A\\cup B=[-3,\\,5]}\\qquad \\fmm{B\\cap C=[4,\\,5]}\\qquad ')
    retoc(r'(\\fmm\{A\\cap B=\(0,\\,2\]\}: [^\n]*)\n\n(\\fmm\{A\\cup B)', r'\1 \2', True)
    # la pàgina 4 (de l'exemple d'equacions a l'exemple de 1.4), amb menys espai entre requadres perquè 1.4 hi càpiga sencer
    retoc(r'(\\begin\{fmex\}\{E\w+ res\w+: (?:equacions|ecuaciones) (?:amb|con) valor absoluto?\})', r'\\begingroup\\tcbset{before skip=5pt,after skip=5pt}\\setlist{itemsep=2pt,topsep=0pt}\n\1', True)
    retoc(r'(\\end\{fmdef\}\n\n)\\Needspace\{5\\baselineskip\}\n(\\begin\{fmex\}\{E\w+ res\w+\}\n\\begin\{enumerate\}[^\n]*\n\\item \w+ \\fmm\{A=\[-3,2\]\}.*?\\end\{fmex\}\n)', r'\1\2\\endgroup\n', True)
    retoc(r'(\\Needspace\{[\d.]+cm\}\n\\section\{Uni\w+ (?:i|e) intersecci)', r'\\enlargethispage{0.4cm}\1', True)
    # l'exemple de logaritmes amb la definició, cada exemple en una línia (1.8 torna a començar a la pàgina 8)
    retoc('\\item \\fmm{\\log_2\\dfrac18}\n\n', '\\item \\fmm{\\log_2\\dfrac18}. ')
    retoc('=2^{-3}}\n\n\\fmm{\\log_2\\dfrac18=-3}', '=2^{-3}\\ \\Rightarrow\\ \\log_2\\dfrac18=-3}')
    retoc('\\item \\fmm{\\log_3\\sqrt[5]{9}}\n\n\\fmm{', '\\item \\fmm{\\log_3\\sqrt[5]{9}}: \\fmm{')
    retoc('=3^{\\frac25}}\n\n\\fmm{\\log_3 3^{\\frac25}', '=3^{\\frac25}\\ \\Rightarrow\\ \\log_3 3^{\\frac25}')
    retoc(r'(\\fmm\{\\log_x 125=3\})\.\n\n', r'\1: ', True)
    for f in ('|2x-3|=7', '|3x-6|\\le9', '|-2x+4|\\gt6'):  # l'enunciat i el primer pas, en la mateixa línia
        retoc(r'(\\item \w+ \\fmm\{%s\})\.\n\n' % re.escape(f), r'\1: ', True)
    retoc(r'(\\fmm\{C=\[4,\+\\infty\)\}\. \w+ \\fmm\{A\\cap B\}, \\fmm\{A\\cup B\}, \\fmm\{B\\cap C\} \w \\fmm\{A\\cap C\}\.)\n\n', r'\1 ', True)
if N == 1:  # retocs de l'autor (Desktop, revisió final 2026-11-25)
    retoc(r'(Extraiem factors|Extraemos factores): (\\fmm\{\\ 3\\cdot5\\sqrt2-2\\cdot3\\sqrt2\+2\\sqrt2)\}\n\n(?:Són semblants: sumem els coeficients|Son semejantes: sumamos los coeficientes)\. \\fmm\{\\ (\(15-6\+2\)\\sqrt2=11\\sqrt2\})\n',
          lambda m: m.group(1) + T(' i sumem', ' y sumamos') + ': ' + m.group(2) + '=' + m.group(3) + '\n\n', True)
    retoc(r'(\\fmm\{\(4,2,3\)=12\})\. \\fmm\{\\ (\\dfrac\{\\sqrt\[12\]\{2\^9\}[^\n]*?)\}\n\n\\fmm\{=', r'\1:\\\\[2ex]\n\n\\fmm{\2=', True)
    i = doc.index('\\item \\fmm{\\dfrac{2}{\\sqrt[3]{5}}}'); j = doc.index('\\end{enumerate}', i)  # racionalització: cada exemple en una línia
    assert doc[i:j].count('}\n\n\\fmm{=') == 6
    doc = doc[:i] + doc[i:j].replace('}\n\n\\fmm{=', '=').replace('}\n\\item', '}\n\n\n\\item') + '\n' + doc[j:]
    if not ES:  # en castellà l'exemple ja cap sencer a la pàgina 9
        retoc(r'(\\fmm\{\\log 1\{,\}5=[^\n]*\}\n)(\\item \w+ \\fmm\{\\log\\dfrac\{100)', r'\1\\newpage\n\2', True)
if N == 2:  # retocs de l'autor (Desktop, revisió 2026-11-25)
    # les identitats notables, com un punt més de la llista d'operacions, amb més aire entre files
    retoc(r'\\end\{itemize\}\n\n(\\textbf\{Identi\w+ notables\})\n\n\\begin\{center\}\\renewcommand\{\\arraystretch\}\{1\.4\}(\\begin\{tabularx\}\{\\linewidth\}\{XX\}\n.*?\\end\{tabularx\}\\end\{center\}\n)',
          lambda m: '\n\n\\item ' + m.group(1) + '\n\n\\begin{center}\\renewcommand{\\arraystretch}{0.4}' + m.group(2).replace('\\\\[4pt]', '\\\\[3ex]') + '\\end{itemize}\n', True)
    retoc(r'\n\n\\Needspace\{5\.1cm\}\n(\\subsection\*\{Divisi\w+ de polinomi)', r'\n\\vspace*{0.3cm}\n\\Needspace{6.1cm}\n\1', True)
    retoc(r'(x=\\frac12,\\ x=-2\})\. (\w+) (\\fmm\{2x\^2\+3x-2=2\\left\(x-\\frac12\\right\)\(x\+2\)=\(2x-1\)\(x\+2\))\}\n\n\\fmm\{(Q\(x\)=x\\,\(x-1\)\(2x-1\)\(x\+2\)\})',
          r'\1.\\\\\n \2 \3 \\Rightarrow \4', True)
    retoc(r'(\n)(\\item \w+ \w+ \w+ \\fmm\{\\dfrac\{x\^2-9\}\{x\^2\+2x\})', r'\1\\newpage\n\2', True)
    retoc(r'(\n)(\\item \\fmm\{5\^x=12\})', r'\1\\newpage\n\2', True)
if N == 3:  # títol de dues línies: tot el text de la franja puja perquè no isca de la franja
    retoc('\\vspace*{0.55cm}\n\\tcbox', '\\vspace*{0.0cm}\n\\tcbox')
if N == 3:  # retocs de l'autor (Desktop, revisió 2026-11-25): la taula dels tipus de sistemes amb la primera columna més ampla
    j = doc.index('\\fmbadge{fmas}{SI} Incompatible'); i = doc.rindex('\\begin{center}', 0, j); j = doc.index('\\end{center}', j)
    assert doc[i:j].count('p{3.2cm}') == 3
    doc = doc[:i] + doc[i:j].replace('p{3.2cm}', 'p{4.2cm}') + doc[j:]
if N == 5:  # l'exemple de la funció a trossos: les quatre gràfiques dels passos, més menudes (no deixen un forat de 5 cm)
    i = doc.index(T('\\begin{fmex}{Exemple resolt: representa $f(x)=\\begin{cases}', '\\begin{fmex}{Ejemplo resuelto: representa $f(x)=\\begin{cases}')); j = doc.index('\\end{fmex}', i)
    assert doc[i:j].count('width=6.2cm,height=5.2cm') == 4
    doc = doc[:i] + doc[i:j].replace('width=6.2cm,height=5.2cm', 'width=6.2cm,height=3.9cm') + doc[j:]
if N == 10:  # el títol de 10.2 (dues línies) i el començament del requadre caben al final de la pàgina 2
    retoc(r'\\Needspace\{[\d.]+cm\}(\n\\section\{Variables aleat\w+ discret)', r'\\enlargethispage{1cm}\\Needspace{4cm}\1', True)
if N == 7:  # «Regla de la cadena» comença al final de la pàgina 6 (no hi deixa un forat de 5 cm)
    retoc(r'\\Needspace\{5.7cm\}(\n\\section\{Regla de la cadena)', r'\\enlargethispage{1cm}\\Needspace{4cm}\1', True)

out = os.path.join(OUTDIR, 't%d-apunts-teoria%s.tex' % (N, '-es' if ES else ''))
open(out, 'w', encoding='utf-8').write(doc)
print(os.path.relpath(out, HERE), len(secs), 'apartats,', len(doc), 'caràcters')
