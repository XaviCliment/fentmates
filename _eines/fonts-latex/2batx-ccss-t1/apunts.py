# Genera tN-apunts-teoria.tex per a les unitats 1, 2 i 3 de 2n Batxillerat CCSS (Matrius i determinants, Sistemes
# d'equacions lineals, Programació lineal): apunts de teoria en PDF per a l'alumnat, a partir dels apunts interactius
# (materials/2batx-ccss/t1-matrius-determinants.html, t2-sistemes-equacions.html, t3-programacio-lineal.html).
# Mateix disseny que els apunts de les unitats 4-10 (../2batx-ccss-t10/apunts.py), amb els colors del bloc
# d'Àlgebra (blau, unitats 1 i 2) i de Programació lineal (taronja, unitat 3). Aquestes pàgines són d'abans de
# _eines/apunts: el text de cada idioma va en <span data-l="va|es|en">, i ací només es queda el de l'idioma triat.
# Deixa fora els ginys, les caixes «Practica», el laboratori i l'autoavaluació. Les figures de la regla de Sarrus
# (svg) i de programació lineal (figure.plfig, diccionari FIG d'app) es redibuixen amb TikZ (../comu/pltikz.py).
# Les fórmules centrades massa amples per a la pàgina s'encongeixen soles (\fmdisp).
# Ús: python3 apunts.py N [es]   (N = 1, 2 o 3) → ../2batx-ccss-tN/tN-apunts-teoria[-es].tex
#     i pdflatex dues vegades (per l'índex), amb logo-fentmates.pdf al costat.
import os, re, sys
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from pltikz import C, fig

N = int(sys.argv[1])
ES = len(sys.argv) > 2 and sys.argv[2] == 'es'
LANG = 'es' if ES else 'va'
def T(va, es): return es if ES else va

U = {
 1: dict(src='t1-matrius-determinants.html', title=T('Matrius i determinants', 'Matrices y determinantes'), c='3D6AA0', cl='4E81BD',
         block=T("bloc d'Àlgebra: blau", 'bloque de Álgebra: azul'),
         kw=T('matrius, operacions amb matrius, determinants, regla de Sarrus, adjunts, rang, matriu inversa, equacions matricials',
              'matrices, operaciones con matrices, determinantes, regla de Sarrus, adjuntos, rango, matriz inversa, ecuaciones matriciales')),
 2: dict(src='t2-sistemes-equacions.html', title=T("Sistemes d'equacions lineals", 'Sistemas de ecuaciones lineales'), c='3D6AA0', cl='4E81BD',
         block=T("bloc d'Àlgebra: blau", 'bloque de Álgebra: azul'),
         kw=T('sistemes lineals, classificació, mètode de Gauss, expressió matricial, regla de Cramer, teorema de Rouché-Frobenius, discussió de sistemes, paràmetres',
              'sistemas lineales, clasificación, método de Gauss, expresión matricial, regla de Cramer, teorema de Rouché-Frobenius, discusión de sistemas, parámetros')),
 3: dict(src='t3-programacio-lineal.html', title=T('Programació lineal', 'Programación lineal'), c='DC7A29', cl='F79645',
         block=T('bloc de Programació lineal: taronja', 'bloque de Programación lineal: naranja'),
         kw=T('inequacions lineals, sistemes d\'inequacions, regió factible, vèrtexs, funció objectiu, rectes de nivell, màxim, mínim',
              'inecuaciones lineales, sistemas de inecuaciones, región factible, vértices, función objetivo, rectas de nivel, máximo, mínimo')),
}[N]
SRC = os.path.join(HERE, '..', '..', '..', 'materials', '2batx-ccss', U['src'])
OUTDIR = os.path.join(HERE, '..', '2batx-ccss-t%d' % N)

# ---------- 1. HTML ----------
src = open(SRC, encoding='utf-8').read()
hero = re.search(r'<section class="hero">.*?<p>[^\n]*?<span data-l="%s">(.*?)</span>' % LANG, src, re.S).group(1)
tocnames = [re.search(r'<span data-l="%s">(.*?)</span>' % LANG, x).group(1)
            for x in re.findall(r'<span class="n">%d\.\d+</span>(.*?)<span class="ck">' % N, src)]
body = src[src.index('<article>') + len('<article>'):src.index('<section class="unit" id="lab">')]
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

# programació lineal: les figures estàtiques d'app (FIG), amb les mateixes restriccions i finestres
def cons(L): return [C(a, b, op, c) for a, b, op, c in L]
PLF = {
 'h1': dict(view=(-2, 5, -2, 6), cons=[(2, 1, '<=', 4)], test=(0, 0)),
 'h2': dict(view=(-2, 6, -4, 3), cons=[(1, -2, '>', 2)], test=(0, 0)),
 'h3': dict(view=(-3, 3, -3, 5), cons=[(-2, 1, '>=', 0)], test=(1, 0)),
 's1': dict(view=(-1, 7, -1, 7), cons=[(1, 1, '<=', 6), (0, 1, '<=', 4), (1, 0, '<=', 5), (1, 0, '>=', 1), (0, 1, '>=', 0)], labels=True),
 's2': dict(view=(-1, 7, -1, 7), cons=[(1, 1, '>=', 4), (1, 0, '>=', 1), (0, 1, '>=', 0)], labels=True),
 's3': dict(view=(-1, 7, -1, 7), cons=[(1, 1, '<=', 2), (1, 1, '>=', 5), (1, 0, '>=', 0), (0, 1, '>=', 0)]),
 'bike': dict(view=(-4, 50, -4, 65), cons=[(1, 2, '<=', 80), (3, 2, '<=', 120), (1, 0, '>=', 0), (0, 1, '>=', 0)], obj=(20, 15), level=850, labels=True, opt=[(20, 30)]),
 'diet': dict(view=(-1, 11, -1, 14), cons=[(3, 1, '>=', 12), (1, 2, '>=', 9), (1, 0, '>=', 0), (0, 1, '>=', 0)], obj=(5, 3), level=24, labels=True, opt=[(3, 3)]),
 'trans': dict(view=(-4, 40, -4, 50), cons=[(1, 1, '<=', 50), (1, 1, '>=', 30), (1, 0, '>=', 0), (1, 0, '<=', 30), (0, 1, '>=', 0), (0, 1, '<=', 40)], obj=(2, -2), level=-80, labels=True, opt=[(0, 40)]),
 'inv': dict(view=(-1, 11, -1, 8), cons=[(1, 1, '<=', 10), (1, 0, '>=', 2), (0, 1, '<=', 6), (-2, 1, '<=', 0), (0, 1, '>=', 0)], obj=(50, 80), level=680, labels=True, opt=[(4, 6)]),
 'inf': dict(view=(-1, 10, -1, 10), cons=[(2, 1, '<=', 16), (1, 2, '<=', 14), (1, 0, '>=', 0), (0, 1, '>=', 0)], obj=(40, 20), level=320, labels=True, opt=[(6, 4), (8, 0)], seg=((6, 4), (8, 0))),
 'unb': dict(view=(-1, 13, -1, 14), cons=[(3, 1, '>=', 12), (1, 2, '>=', 9), (1, 0, '>=', 0), (0, 1, '>=', 0)], obj=(5, 3), level=60, labels=True),
 'empty': dict(view=(-1, 7, -1, 5), cons=[(1, 1, '<=', 3), (2, 3, '>=', 12), (1, 0, '>=', 0), (0, 1, '>=', 0)]),
}
def plfig(key, w=5.6, hmax=5.0):
    f = PLF[key]
    lv = [(f['obj'][0], f['obj'][1], f['level'], '')] if 'obj' in f else ()
    test = (f['test'], False) if 'test' in f else None
    if test:  # el punt de prova: verd si compleix la inequació
        a, b, op, c = f['cons'][0]; x, y = f['test']; v = a * x + b * y
        test = (f['test'], {'<=': v <= c, '<': v < c, '>=': v >= c, '>': v > c}[op])
    return fig(cons(f['cons']), f['view'], w=w, hmax=hmax, labels=f.get('labels', False), test=test, levels=lv,
               opt=f.get('opt', ()), seg=f.get('seg'), draw_axes_cons=key in ('h1', 'h2', 'h3'))

# ---------- 4. conversió a LaTeX ----------
UNI = {'→': r'$\to$', '∞': r'$\infty$', '≪': r'$\ll$', '≤': r'$\leq$', '≥': r'$\geq$', '−': '-', '○': r'$\circ$', '∄': r'$\nexists$',
       '✓': '', '✗': '', '✎': '', '✍': '', '🎓': '', '◉': '', '⚙': '', '⚠': '', '…': r'\dots{}', '×': r'$\times$', '≠': r'$\neq$', '±': r'$\pm$',
       '↗': r'$\nearrow$', '↘': r'$\searrow$', '∩': r'$\cap$', '∪': r'$\cup$', '–': '--', '⇒': r'$\Rightarrow$', '⟺': r'$\Leftrightarrow$',
       '←': r'$\leftarrow$', '∅': r'$\emptyset$', '●': r'$\bullet$', '₁': r'$_1$', '₂': r'$_2$', '₃': r'$_3$', '₄': r'$_4$',
       'ᵗ': r'$^t$', '⁻¹': r'$^{-1}$', '²': r'$^2$', '³': r'$^3$', '½': r'$\frac12$', '√': r'$\surd$', '∈': r'$\in$', '∀': r'$\forall$'}
MATH = re.compile(r'(\\\[.*?\\\]|\\\(.*?\\\))', re.S)
def esc(t):
    out = []
    for i, part in enumerate(MATH.split(t)):
        if i % 2:
            part = part.replace('&lt;', '<').replace('&gt;', '>')
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
    if t == 'figure' and 'plfig' in c: return r'\par\smallskip{\centering %s\par}\smallskip ' % plfig(n.a['data-fig'], *(PLSIZE.get(n.a['data-fig']) or ((4.6, 4.4) if TWO[0] else (5.6, 5.0))))
    if t in ('input', 'select', 'button', 'svg', 'summary', 'label', 'option', 'script', 'style'): return ''
    if 'widget' in c or 'box' in c and 'pr' in c or 'steps-ctl' in c or 'sec-head' in c: return ''
    if t == 'section': return conv_section(n)
    if t == 'h3': return '\n\\Needspace{16\\baselineskip}\n\\subsection*{%s}\n' % text(n).strip()
    if 'box' in c:
        kind = [k for k in ('def', 'prop', 'ex') if k in c][0]
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
# mides especials d'algunes figures: en castellà, la figura de la regió buida (3.5) un poc més baixa perquè l'últim exemple càpiga en la pàgina 14
PLSIZE = {'empty': (4.0, 3.2)} if (N == 3 and ES) else {}
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
def conv_table(n):
    rows = rows_of(n)
    m = max(len(elems(r)) for r in rows)
    if max(len(plain(c)) for r in rows for c in elems(r)) > 28:  # taules de text: columnes que fan salt de línia
        IN_TABLE[0] = True
        L = '>{\\raggedright\\arraybackslash}'
        s = r'\small\begin{tabularx}{\linewidth}{%sp{3.2cm}%s}\toprule' % (L, (L + 'X') * (m - 1)) + '\n'
        for r in rows:
            cs = elems(r)
            head = all(c.tag == 'th' for c in cs) or r.parent.tag == 'thead'
            s += ' & '.join(cell(c, head) for c in cs) + r'\\' + (r'\midrule' if head else r'[3pt]') + '\n'
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
 3: r'''\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line width=3.6pt,line cap=round,line join=round]
  \begin{scope}[transparency group,opacity=0.15]
  \draw[line width=3pt] (30,106)--(226,106) (30,106)--(30,6);
  \fill[fill opacity=0.18] (30,106)--(30,34)--(92,22)--(160,56)--(180,106)--cycle;
  \draw (30,106)--(30,34)--(92,22)--(160,56)--(180,106)--cycle;
  \draw[opacity=0.6] (22,38)--(120,18) (80,0)--(200,66) (168,0)--(190,120);
  \fill (30,34) circle (5) (92,22) circle (5) (160,56) circle (6.5) (180,106) circle (5);
  \draw[dash pattern=on 9pt off 9pt] (120,120)--(232,50);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{23}{23}\itshape] at (198,40) {%s};
  \end{scope}
\end{tikzpicture}''' % T('màx', 'máx'),
}[N]

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
\definecolor{fmmuted}{HTML}{5D6685}
\definecolor{fmsurface}{HTML}{EEF1F8}
% noms que fan servir les gràfiques de programació lineal (../comu/pltikz.py)
\colorlet{accent}{fmaccent}\colorlet{navy}{fmnavy}\colorlet{muted}{fmmuted}\colorlet{teal}{fmteal}

\newcommand{\lt}{<}\newcommand{\gt}{>}
% fórmula en línia que no es parteix mai; si no cap en una línia, es posa centrada
\newcommand{\fmm}[1]{\setbox0=\hbox{$#1$}\ifdim\wd0>\linewidth\fmdisp{#1}\else\mbox{\box0}\fi}
% fórmula centrada; si és més ampla que la línia, s'encongeix fins que hi cap
\newcommand{\fmdisp}[1]{\[\setbox2=\hbox{$\displaystyle #1$}\ifdim\wd2>\linewidth\resizebox{\linewidth}{!}{\box2}\else\box2\fi\]}
\DeclareUnicodeCharacter{2212}{-}
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
\newtcolorbox{fmnote}{enhanced,breakable,colback=white,colframe=white,borderline west={3pt}{0pt}{fmaccent},arc=0pt,left=3mm,right=2mm,top=1mm,bottom=1mm,before skip=6pt,after skip=6pt,before upper=\raggedright}
\newcommand{\fmkey}[1]{\colorbox{fmyellow!45}{\strut #1}}
\newcommand{\fmuline}[1]{\textbf{\color{fmaccent}#1}}
\definecolor{fmok}{HTML}{15803D}\definecolor{fmev}{HTML}{2563EB}\definecolor{fmsf}{HTML}{C2410C}\definecolor{fmsi}{HTML}{7C3AED}\definecolor{fmas}{HTML}{A3203A}
\newcommand{\fmbadge}[2]{\tcbox[on line,colback=#1,colframe=#1,arc=2mm,boxsep=0pt,left=4pt,right=4pt,top=1.5pt,bottom=1.5pt]{\color{white}\footnotesize\bfseries #2}}
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
toc = [r'\mbox{\hyperlink{sec%d}{\textbf{\color{fmgreen}%d.%d}\ \ %s}}\\[3pt]' % (i + 1, N, i + 1, esc(tocnames[i])) for i in range(len(secs))]
half = (len(toc) + 1) // 2
k = [0]
def anchor(m):
    k[0] += 1
    return '\\section{%s}\\hypertarget{sec%d}{}\n' % (m.group(1), k[0])
latex = re.sub(r'\\section\{(.*?)\}\n', anchor, latex)
hero_tex = esc(re.sub(T(r'(,| i) eines interactives', r'(,| y) herramientas interactivas'), '', hero)
               .replace(T('resolts pas a pas:', 'resueltos paso a paso:'), T('resolts pas a pas:', 'resueltos paso a paso:')))
hero_tex = hero_tex.replace(T('Teoria, exemples', 'Teoría, ejemplos'), T('Teoria i exemples', 'Teoría y ejemplos'))
unit = T('Unitat %d', 'Unidad %d') % N
pre = PRE
for a, b in [('BABEL', T('catalan', 'spanish,es-minimal,es-noshorthands')),
             ('PDFTITLE', T('Apunts de teoria. Unitat %d: %s. 2n de Batxillerat CCSS', 'Apuntes de teoría. Unidad %d: %s. 2.º de Bachillerato CCSS') % (N, U['title'])),
             ('PDFSUBJ', T('Matemàtiques Aplicades a les Ciències Socials II', 'Matemáticas Aplicadas a las Ciencias Sociales II')), ('PDFKW', U['kw']),
             ('BLOCKCOL', U['block']), ('COLC', U['c']), ('COLL', U['cl']), ('UNITN', str(N)), ('CARD', CARD.replace('AY', '34')),
             ('HEADTXT', T('2n Batxillerat CCSS · Unitat %d: %s', '2.º Bachillerato CCSS · Unidad %d: %s') % (N, U['title']))]:
    pre = pre.replace(a, b)
title = TITLE.replace('HERO', hero_tex).replace('TOC1', '\n'.join(toc[:half])).replace('TOC2', '\n'.join(toc[half:]))
for a, b in [('KICKER', T('Apunts de teoria · 2n Batxillerat CCSS II', 'Apuntes de teoría · 2.º Bachillerato CCSS II')),
             ('UNITNUM', unit), ('CARDY', {1: '-0.85'}.get(N, '-1.3')), ('UNITTITLE', U['title']), ('TOCWORD', T('Índex', 'Índice'))]:
    title = title.replace(a, b)
doc = pre + title + latex + '\n\\end{document}\n'

# retocs de l'autor sobre el .tex de l'escriptori (unitat 1, 22/11/2026): valen per als dos idiomes
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

if N == 3 and ES:  # en castellà, la nota final de 3.5 quedava sola en una pàgina 15
    retoc('\\begin{fmex}{Ejemplo 3: región factible vacía}', '\\enlargethispage{\\baselineskip}\n\\begin{fmex}{Ejemplo 3: región factible vacía}')

out = os.path.join(OUTDIR, 't%d-apunts-teoria%s.tex' % (N, '-es' if ES else ''))
open(out, 'w', encoding='utf-8').write(doc)
print(os.path.relpath(out, HERE), len(secs), 'apartats,', len(doc), 'caràcters')
