# Genera tN-apunts-teoria.tex per a les unitats 1-4 de 1r Batxillerat MI (Nombres reals, Àlgebra, Sistemes d'equacions
# i inequacions, Geometria analítica en el pla): apunts de teoria en PDF per a l'alumnat, a partir dels apunts interactius.
# Copia de ../2batx-mii-t1/apunts.py (mateix disseny), amb els colors dels blocs d'Aritmètica (groc, U1), Àlgebra
# (blau, U2-U3) i Geometria (taronja, U4). Llig les pàgines ja generades materials/1batx-mi/tN-....html (text de cada
# idioma en <span data-l>, només es queda el triat).
# Deixa fora els ginys, les caixes «Practica», el laboratori i l'autoavaluació. Les figures estàtiques que la pàgina
# dibuixa amb JavaScript es redibuixen ací amb TikZ: els intervals menuts de la taula de 1.3 (svg.nl-mini[data-iv]),
# les rectes reals apilades dels sistemes d'inequacions (svg[data-stack], dades de STACKS a la pàgina de la U3) i els
# semiplans solució (svg[data-half]).
# Ús: python3 apunts.py N [es]   (N = 1..4) → ../1batx-mi-tN/tN-apunts-teoria[-es].tex
#     i pdflatex dues vegades (per l'índex), amb logo-fentmates.pdf (_eines/logo/pdf/horitzontal-clar.pdf) al costat.
import os, re, sys
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))

N = int(sys.argv[1])
ES = len(sys.argv) > 2 and sys.argv[2] == 'es'
LANG = 'es' if ES else 'va'
def T(va, es): return es if ES else va

ARI = dict(c='C99A2E', cl='E6B84A', block=T("bloc d'Aritmètica: groc", 'bloque de Aritmética: amarillo'))
ALG = dict(c='3D6AA0', cl='4E81BD', block=T("bloc d'Àlgebra: blau", 'bloque de Álgebra: azul'))
GEO = dict(c='DC7A29', cl='F79645', block=T('bloc de Geometria: taronja', 'bloque de Geometría: naranja'))
U = {
 1: dict(ARI, src='t1-nombres-reals.html', title=T('Nombres reals', 'Números reales'),
         kw=T('nombres reals, fracció generatriu, valor absolut, entorns, intervals, unió, intersecció, potències, radicals, racionalització, logaritmes',
              'números reales, fracción generatriz, valor absoluto, entornos, intervalos, unión, intersección, potencias, radicales, racionalización, logaritmos')),
 2: dict(ALG, src='t2-algebra.html', title=T('Àlgebra. Equacions i inequacions', 'Álgebra. Ecuaciones e inecuaciones'),
         kw=T('polinomis, identitats notables, regla de Ruffini, teorema del residu, factorització, fraccions algebraiques, equacions, inequacions',
              'polinomios, identidades notables, regla de Ruffini, teorema del resto, factorización, fracciones algebraicas, ecuaciones, inecuaciones')),
 3: dict(ALG, src='t3-sistemes-inequacions.html', title=T("Sistemes d'equacions i inequacions", 'Sistemas de ecuaciones e inecuaciones'),
         kw=T("sistemes d'equacions, mètode de Gauss, sistemes no lineals, sistemes d'inequacions, inequacions amb dues incògnites, semiplans",
              'sistemas de ecuaciones, método de Gauss, sistemas no lineales, sistemas de inecuaciones, inecuaciones con dos incógnitas, semiplanos')),
 4: dict(GEO, src='t4-geometria-pla.html', title=T('Geometria analítica en el pla', 'Geometría analítica en el plano'),
         kw=T('vectors, producte escalar, angle entre vectors, equacions de la recta, posicions relatives, angles, distàncies, punt simètric, triangles',
              'vectores, producto escalar, ángulo entre vectores, ecuaciones de la recta, posiciones relativas, ángulos, distancias, punto simétrico, triángulos')),
}[N]

SRC = os.path.join(HERE, '..', '..', '..', 'materials', '1batx-mi', U['src'])
OUTDIR = os.path.join(HERE, '..', '1batx-mi-t%d' % N)

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
FIG = {}
CMP = [0]
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
STACKS = {
 'a': dict(range=(-4, 5), rows=[(r'2x-1<5', [(-INF, 0, 3, 0)]), (r'x^2-4\geq0', [(-INF, 0, -2, 1), (2, 1, INF, 0)])], sol=[(-INF, 0, -2, 1), (2, 1, 3, 0)]),
 'b': dict(range=(-3, 4), rows=[(r'x-2>0', [(2, 0, INF, 0)]), (r'x+1<0', [(-INF, 0, -1, 0)])], sol=[]),
}
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
    g = r'\begin{tikzpicture}\begin{axis}[fmaxis,axis equal image,width=5.6cm,height=5.6cm,xmin=%g,xmax=%g,ymin=%g,ymax=%g,' % tuple(V)
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
    if t == 'svg' and 'nl-mini' in c and n.a.get('data-iv'): return nlmini(n.a['data-iv'])
    if t == 'svg' and n.a.get('data-stack'): return '\n\\begin{center}%s\\end{center}\n' % nstack(n.a['data-stack'], n.a.get('data-sol') == '1')
    if t == 'svg' and n.a.get('data-half'): return '\n\\begin{center}%s\\end{center}\n' % half(n)
    if 'fig-half' in c: return text(n)
    if 'ids' in c:  # identitats notables, en dues columnes
        IN_TABLE[0] = True
        cells = [text(k).strip().replace('$', '$\\displaystyle ', 1) for k in elems(n)]
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
    if t == 'h3': return '\n\\Needspace{6\\baselineskip}\n\\subsection*{%s}\n' % text(n).strip()
    if 'box' in c:
        kind = [k for k in ('def', 'prop', 'ex', 'warn') if k in c][0]
        bh = next(k for k in elems(n) if 'bh' in k.cls())
        bb = next(k for k in elems(n) if 'bb' in k.cls())
        IN_TABLE[0] = True  # fórmules del títol com a $...$
        title = text(bh).strip()
        IN_TABLE[0] = False
        inner = text(bb).strip()
        return '\n\\Needspace{5\\baselineskip}\n\\begin{fm%s}{%s}\n%s\n\\end{fm%s}\n' % (kind, title, inner, kind)
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
while re.search(HEADR, latex):
    latex = re.sub(HEADR, lambda m: '\\Needspace{%d\\baselineskip}' % (10 if m.group(2).count('section') > 1 else 8 if '\\section{' in m.group(2) else 7) + m.group(2), latex)

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
}
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
             ('PDFTITLE', T('Apunts de teoria. Unitat %d: %s. 1r de Batxillerat MI', 'Apuntes de teoría. Unidad %d: %s. 1.º de Bachillerato MI') % (N, U['title'])),
             ('PDFSUBJ', T('Matemàtiques I', 'Matemáticas I')), ('PDFKW', U['kw']),
             ('BLOCKCOL', U['block']), ('COLC', U['c']), ('COLL', U['cl']), ('UNITN', str(N)), ('CARD', CARD),
             ('HEADTXT', T('1r Batxillerat MI · Unitat %d: %s', '1.º Bachillerato MI · Unidad %d: %s') % (N, U.get('short', U['title'])))]:
    pre = pre.replace(a, b)
hero_tex = re.sub(r'</?strong>', '', hero_tex)  # la descripció del web porta etiquetes HTML
title = TITLE.replace('HERO', hero_tex).replace('TOC1', '\n'.join(toc[:half])).replace('TOC2', '\n'.join(toc[half:]))
for a, b in [('KICKER', T('Apunts de teoria · 1r Batxillerat · Matemàtiques I', 'Apuntes de teoría · 1.º Bachillerato · Matemáticas I')),
             ('UNITNUM', unit), ('UNUMCOL', 'fmnavy' if U['c'] == 'C99A2E' else 'fmyellow'), ('CARDY', '-1.3'), ('UNITTITLE', U['title']), ('TOCWORD', T('Índex', 'Índice'))]:
    title = title.replace(a, b)
doc = pre + title + latex + '\n\\end{document}\n'

# retocs sobre el .tex (valen per als dos idiomes)
def retoc(a, b, regex=False):
    global doc
    if regex:
        doc, k = re.subn(a, b, doc, flags=re.S)
        assert k == 1, a[:80]
    else:
        assert doc.count(a) == 1, a[:80]
        doc = doc.replace(a, b)
if N == 1:  # el requadre de les propietats dels logaritmes (dues columnes, no es pot partir) cap al final de la pàgina 6
    retoc(r'(\\Needspace\{\d+\\baselineskip\}\n\\begin\{fmprop\}\{Propi\w+ (?:dels|de los) logaritm\w+\})', r'\\enlargethispage{1cm}\n\1', True)
if N == 1:  # retocs de l'autor (Desktop, revisió 2026-11-24): valen per als dos idiomes
    retoc(r'(\\fmdisp\{\|A\|\\gt r\\iff [^\n]*\}\n\n\\begin\{enumerate\}\[label=\\textbf\{\\arabic\*\.\},leftmargin=\*\]\n)', r'\1\\newpage\n', True)
    for t in ('Extracci', 'Operaci', 'Racionali'):
        retoc(r'\\Needspace\{7\\baselineskip\}(\n\\subsection\*\{%s)' % t, r'\\Needspace{6\\baselineskip}\1', True)
    if ES:  # en castellà el text és més llarg: «Expresiones decimales» comença a la pàgina 1, com en valencià
        retoc('\\Needspace{7\\baselineskip}\n\\subsection*{Expresiones decimales', '\\enlargethispage{1cm}\n\\Needspace{4\\baselineskip}\n\\subsection*{Expresiones decimales')
    # passos que van en una sola línia
    retoc('\\cdot 2\\cdot 7}}\n\n\\fmm{=\\sqrt[3]{2^{13}', '\\cdot 2\\cdot 7}=\\sqrt[3]{2^{13}')
    retoc('\\fmm{\\sqrt[4]{2^7\\cdot 3^2\\cdot 5^8}}: \\fmm{\\quad 7=1\\cdot4+3,\\quad 2\\lt4,\\quad 8=2\\cdot4+0}\n\n\\fmm{=2\\cdot 5^2\\sqrt[4]{2^3\\cdot 3^2}=50\\sqrt[4]{72}}',
          '\\fmm{\\sqrt[4]{2^7\\cdot 3^2\\cdot 5^8}=2\\cdot 5^2\\sqrt[4]{2^3\\cdot 3^2}=50\\sqrt[4]{72}} \\,\\,\\,\\,\\,\\,' + T('ja que', 'ya que')
          + '  \\fmm{\\quad 7=1\\cdot4+3,\\quad 2\\lt4,\\quad 8=2\\cdot4+0}')
    i = doc.index('\\item \\fmm{\\dfrac{2}{\\sqrt[3]{5}}}'); j = doc.index('\\end{enumerate}', i)  # racionalització: cada exemple en una línia
    assert doc[i:j].count('}\n\n\\fmm{=') == 6
    doc = doc[:i] + doc[i:j].replace('}\n\n\\fmm{=', '=').replace('}\n\\item', '}\n\n\\item') + '\n' + doc[j:]
    for x in ('2^{2x}=2^5}\n\n\\fmm{2x=5', '\\log3=\\log20}\n\n\\fmm{x=\\dfrac{\\log20}', '1000\\Rightarrow t\\log3=3}\n\n\\fmm{t=\\dfrac{3}'):
        retoc(x, x.replace('}\n\n\\fmm{', '\\Rightarrow ' if x.startswith('2^') else ' \\Rightarrow '))
    for x in ('2x=5\\Rightarrow x=\\dfrac52}\n\\item', '\\approx 2{,}727}\n\\item'):
        retoc(x, x.replace('}\n\\item', '}\n\n\\item'))
    # 1.4: les propietats de les potències i dels radicals i el pont entre les dues, dins d'un requadre blau
    def compact(x):  # les fórmules de cada columna sense l'espai de fórmula centrada, perquè el requadre no passe a la pàgina següent
        x = x.strip()
        assert x.startswith('\\fmdisp{') and x.endswith('}')
        return '\\par $\\displaystyle ' + x[len('\\fmdisp{'):-1].replace('\\\\[2pt]', '\\\\[0pt]') + '$\\par\n'
    retoc(r'\\par\\noindent \\begin\{minipage\}\[t\]\{0\.48\\linewidth\}\\vspace\{0pt\}\\raggedright (Propi[^\n]*)\n(.*?)\\end\{minipage\}\\hfill\\begin\{minipage\}\[t\]\{0\.48\\linewidth\}\\vspace\{0pt\}\\raggedright (Propi[^\n]*)\n(.*?)\\end\{minipage\}\\par\\medskip\n\n(El (?:pont|puente)[^:\n]*:) (\\fmm\{[^\n]*\})\n',
          lambda m: ('\\Needspace{5\\baselineskip}\n\\begin{fmdef}{%s}\n' % T('Propietats de les potències i dels radicals', 'Propiedades de las potencias y de los radicales')
                     + '\\par\\noindent \\begin{minipage}[t]{0.48\\linewidth}\\vspace{0pt}\\centering\\textbf{%s}\n%s\\end{minipage}\\hfill' % (m.group(1), compact(m.group(2)))
                     + '\\begin{minipage}[t]{0.48\\linewidth}\\vspace{0pt}\\centering\\textbf{%s}\n%s\\end{minipage}\\par\n' % (m.group(3), compact(m.group(4)))
                     + '\\begin{fmnote}[before skip=4pt,after skip=0pt,top=0.5mm,bottom=0.5mm]\\fmuline{%s} %s\\end{fmnote}\n\\end{fmdef}\n' % (m.group(5), m.group(6))), True)
if N == 4:  # retocs de l'autor (Desktop, revisió 2026-11-24): salt de pàgina després de l'exemple de rectes paral·leles
    retoc(r'(\\fmm\{\\ 5=3-6\\mu\\Rightarrow\\mu=-\\tfrac13\}\. [^\n]*\n)', r'\1\\newpage\n', True)
if N in (2, 3):  # títol de dues línies: tot el text de la franja puja perquè no isca de la franja
    retoc('\\vspace*{0.55cm}\n\\tcbox', '\\vspace*{0.0cm}\n\\tcbox')
if N == 2:  # la fórmula del grau de la suma, en una línia a part (evita els buits del text justificat)
    retoc(r'(\\item \\textbf\{Suma (?:i|y) resta\}: [^\n]*?\.) (\\fmm\{\\ \\text\{gra(?:u|do)\}\(P\\pm Q\))', r'\1\\newline \2', True)
if N == 2:  # retocs de l'autor (Desktop, revisió 2026-11-24): la factorització de Q(x) acaba en la mateixa línia
    retoc('(x+2)=(2x-1)(x+2)}\n\n\\fmm{Q(x)=x\\,(x-1)(2x-1)(x+2)}', '(x+2)=(2x-1)(x+2) \\Rightarrow Q(x)=x\\,(x-1)(2x-1)(x+2)}')
if N == 2 and ES:  # en castellà l'exemple d'equacions logarítmiques cap al final de la pàgina 9 (11 pàgines, com en valencià)
    retoc('\\Needspace{5\\baselineskip}\n\\begin{fmex}{Ejemplo resuelto: ecuaciones logarítmicas}', '\\enlargethispage{1cm}\n\\Needspace{5\\baselineskip}\n\\begin{fmex}{Ejemplo resuelto: ecuaciones logarítmicas}')
    retoc(r'(\\hypertarget\{sec11\}\{\})', r'\1\\enlargethispage{\\baselineskip}', True)  # l'última línia no passa a una pàgina 12 tota sola
if N == 2:  # les propietats de les potències no caben en la línia: van centrades
    retoc(r'(potències|potencias): \\fmm\{\\ (a\^m\\cdot a\^n=a\^\{m\+n\}.*?a\^0=1)\}\.', r'\1:\n\\fmdisp{\2.}', True)

out = os.path.join(OUTDIR, 't%d-apunts-teoria%s.tex' % (N, '-es' if ES else ''))
open(out, 'w', encoding='utf-8').write(doc)
print(os.path.relpath(out, HERE), len(secs), 'apartats,', len(doc), 'caràcters')
