# Genera t4-apunts-teoria.tex (2n Batxillerat CCSS, Unitat 4: Límits i continuïtat): apunts de teoria en PDF
# per a l'alumnat, a partir dels apunts interactius (_eines/apunts/2batx-ccss-t4/contingut.html, només el valencià).
# Deixa fora els ginys, les caixes «Practica», la calculadora i l'autoavaluació. Les gràfiques es redibuixen amb
# pgfplots a partir de les mateixes funcions que fa servir app.js (diccionari FIG).
# Ús: python3 apunts.py && pdflatex t4-apunts-teoria.tex (dues vegades, per l'índex)
import os, re
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', 'apunts', '2batx-ccss-t4', 'contingut.html')

# ---------- 1. HTML en valencià ----------
src = open(SRC, encoding='utf-8').read()
src = re.sub(r'⟦(.*?)‖.*?‖.*?⟧', r'\1', src, flags=re.S)
src = re.sub(r'⟪(.*?)‖.*?‖.*?⟫', r'\1', src, flags=re.S)
src = src.replace(r'\SI', r'\text{si }')
hero = re.search(r'<section class="hero">.*?<p>(.*?)</p>', src, re.S).group(1)
body = src[src.index('<section class="unit" id="s1">'):src.index('<section class="unit" id="lab">')]

def fix(a, b):
    global body
    assert body.count(a) == 1, a[:80]
    body = body.replace(a, b)
# primer requadre d'exemples: es compon a mà (fórmula dalt, límits i asímptota baix), vegeu INF_EXAMPLES
i = body.index('<div class="two">', body.index('Exemples: llegim els límits a la gràfica'))
j = body.index('<p class="note">', i)
body = body[:i] + '<div class="pdf-inf"></div>\n      ' + body[j:]
# 4.2, quocients, cas 4: els dos límits un davall de l'altre, sense «i»
fix(r'''<li>Amb arrels: \(\displaystyle\lim_{x\to+\infty}\frac{\sqrt{x^3+x-2}}{x+5}=\lim_{x\to+\infty}\frac{x^{3/2}}{x}=\lim_{x\to+\infty}\sqrt{x}=+\infty\) i \(\displaystyle\lim_{x\to+\infty}\frac{\sqrt{9x^2+1}}{x-4}=\lim_{x\to+\infty}\frac{3x}{x}=3\).</li>''',
    r'''<li>Amb arrels: \[\lim_{x\to+\infty}\frac{\sqrt{x^3+x-2}}{x+5}=\lim_{x\to+\infty}\frac{x^{3/2}}{x}=\lim_{x\to+\infty}\sqrt{x}=+\infty\]\[\lim_{x\to+\infty}\frac{\sqrt{9x^2+1}}{x-4}=\lim_{x\to+\infty}\frac{3x}{x}=3\]</li>''')
# 4.3, exemples: el 6 forma part del 5
fix(r'''=\frac13\).</li>
        <li>\(\displaystyle\lim_{x\to+\infty}\frac{3^x}{2^x}=\lim_{x\to+\infty}\left(\tfrac32\right)^x=+\infty\).</li>''',
    r'''=\frac13\]\[\lim_{x\to+\infty}\frac{3^x}{2^x}=\lim_{x\to+\infty}\left(\tfrac32\right)^x=+\infty\]</li>''')
fix(r'''<li>Mateix ordre: \(\displaystyle\lim_{x\to+\infty}\frac{e^x+x^5}{3e^x-x}''', r'''<li>Mateix ordre: \[\lim_{x\to+\infty}\frac{e^x+x^5}{3e^x-x}''')
# 4.6, exemples 2 i 3: com el cas 1 (Substituïm..., i després factoritzem)
fix(r'''<div class="step"><p>\(\dfrac{1-3+2}{1-1}=\dfrac00\ \ \text{IND.}\) Dividim''', r'''<div class="step"><p>Substituïm: \(\dfrac{1-3+2}{1-1}=\dfrac00\ \ \text{IND.}\) Dividim''')
fix(r'''<div class="step"><p>\(\dfrac00\ \ \text{IND.}\) \(\quad\displaystyle\lim_{x\to-1}\frac{x\cancel{(x+1)}}{(x+1)^{\cancel{2}}}=\lim_{x\to-1}\frac{x}{x+1}=\frac{-1}{0}\)</p></div>''',
    r'''<div class="step"><p>Substituïm: \(\dfrac{1-1}{1-2+1}=\dfrac00\ \ \text{IND.}\)</p></div>
            <div class="step"><p>Factoritzem (\(x^2+x=x(x+1)\) i \(x^2+2x+1=(x+1)^2\)): \[\lim_{x\to-1}\frac{x\cancel{(x+1)}}{(x+1)^{\cancel{2}}}=\lim_{x\to-1}\frac{x}{x+1}=\frac{-1}{0}\]</p></div>''')

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
    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag: n = n.parent
        if n is not None and n.parent is not None: self.cur = n.parent
    def handle_data(self, d): self.cur.kids.append(d)
p = P(); p.feed(body); ROOT = p.root

# ---------- 3. gràfiques (pgfplots) ----------
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
FIG = {
 'inf1': axis([-6, 6, -1, 3.2], cv('2*x^2/(x^2+1)', -6, 6) + ha(2)),
 'inf2': axis([-6, 4, -2, 6], cv('2^x-1', -6, 3) + ha(-1)),
 'inf3': axis([-6, 6, -6, 6], cv('x^3/10-x', -6, 6)),
 'inf4': axis([-10, 10, -2, 2], cv('sin(deg(x))', -10, 10, 300)),
 'inf5': axis([-4, 10, -1, 4], cv('sqrt(max(x-2,0))', 2, 10, 300) + pt(2, 0)),
 'inf6': axis([-5, 5, -1, 4], cv('sqrt(max(9-x^2,0))', -3, 3, 300) + pt(-3, 0) + pt(3, 0)),
 'pf': axis([-6, 6, -2, 4], cv('(3*x^2-2)/(x^2+2)', -6, 6) + ha(3)),
 'pg': axis([-6, 3, -5, 3], cv('2-exp(x)', -6, 3) + ha(2)),
 'ph': axis([-6, 6, -6, 6], cv('-x^3/8+x', -6, 6)),
 'grafG': axis([-4, 6, -4, 6], va(-1) + cv('-1/(x+1)', -4, -1.1, 300) + cv('x', -1, 2) + cv('4-(x-2)^2/2', 2, 6)
               + pt(-1, -1, True) + pt(1, 1, True) + pt(1, 3) + pt(2, 2, True) + pt(2, 4), '8cm', '6cm'),
 'tev': axis([-1, 3, -1, 4], gd(1) + cv('x/2+1', -1, 3) + pt(1, 1.5, True) + pt(1, 3) + lb(1.05, -0.6, 'a'), '4.4cm', '3.8cm'),
 'tsf': axis([-1, 3, -1, 4], gd(1) + cv('x+1', -1, 1) + cv('x/2', 1, 3) + pt(1, 2, True) + pt(1, 0.5) + lb(1.05, -0.6, 'a'), '4.4cm', '3.8cm'),
 'tsi': axis([-1, 3, -2, 5], va(1) + cv('1/(2*(1-x))', -1, 0.9, 300) + cv('x-2', 1, 3) + pt(1, -1) + lb(1.05, -1.6, 'a'), '4.4cm', '3.8cm'),
 'tas': axis([-1, 3, -5, 5], va(1) + cv('1/(x-1)', -1, 0.8, 300) + cv('1/(x-1)', 1.2, 3, 300) + lb(1.05, -4.4, 'a'), '4.4cm', '3.8cm'),
 'rat1': axis([-3, 5, -6, 6], va(2) + ha(1) + cv('(x+1)/(x-2)', -3, 1.75, 300) + cv('(x+1)/(x-2)', 2.25, 5, 300) + pt(1, -2, True)),
 'pau30': axis([-3.5, 3.5, -1, 5], cv('3*x+10', -3, -2) + cv('x^2', -2, 1) + cv('(x+3)/2', 1, 3) + pt(-3, 1) + pt(-2, 4) + pt(1, 1, True) + pt(1, 2) + pt(3, 3)),
 'asV': axis([-5, 5, -6, 6], va(-2) + va(2) + ha(0) + cv('(x+1)/(x^2-4)', -5, -2.02, 600) + cv('(x+1)/(x^2-4)', -1.985, 1.985, 900) + cv('(x+1)/(x^2-4)', 2.02, 5, 600)),
 'asH': axis([-8, 8, -1.5, 4.5], ha(3) + cv('(3*x^2-1)/(x^2+2)', -8, 8, 200)),
 'asO': axis([-6, 8, -8, 12], va(1) + ln(-6, 8, 1, 1) + cv('(x^2+3)/(x-1)', -6, 0.7, 300) + cv('(x^2+3)/(x-1)', 1.3, 8, 300)),
}

# primer requadre d'exemples de 4.1: fórmula dalt de cada gràfica; baix, els límits en una línia i l'asímptota en una altra
def cell(f, key, lims, note):
    return (r'\begin{minipage}[t]{0.48\linewidth}\centering $%s$\par\smallskip %s\par\smallskip $%s$\par %s\end{minipage}'
            % (f, FIG[key], lims, note))
INF = [
 (r'f(x)=\dfrac{2x^2}{x^2+1}', 'inf1', r'\displaystyle\lim_{x\to+\infty}f(x)=2,\qquad\lim_{x\to-\infty}f(x)=2', r'Asímptota horitzontal $y=2$ pels dos costats.'),
 (r'g(x)=2^x-1', 'inf2', r'\displaystyle\lim_{x\to-\infty}g(x)=-1,\qquad\lim_{x\to+\infty}g(x)=+\infty', r'Asímptota horitzontal $y=-1$ només per l’esquerra.'),
 (r'h(x)=\dfrac{x^3}{10}-x', 'inf3', r'\displaystyle\lim_{x\to-\infty}h(x)=-\infty,\qquad\lim_{x\to+\infty}h(x)=+\infty', r'No té asímptota horitzontal.'),
 (r'k(x)=\sin x', 'inf4', r'\displaystyle\nexists\lim_{x\to-\infty}\sin x,\qquad\nexists\lim_{x\to+\infty}\sin x', r'Osci\lgem{}a entre $-1$ i $1$ sense parar.'),
 (r'm(x)=\sqrt{x-2}', 'inf5', r'\displaystyle\nexists\lim_{x\to-\infty}m(x),\qquad\lim_{x\to+\infty}m(x)=+\infty', r'Domini $[2,+\infty)$: no està definida per a $x<2$.'),
 (r'n(x)=\sqrt{9-x^2}', 'inf6', r'\displaystyle\nexists\lim_{x\to-\infty}n(x),\qquad\nexists\lim_{x\to+\infty}n(x)', r'Domini $[-3,3]$: no arriba a cap dels dos infinits.'),
]
INF_EXAMPLES = '\n' + '\n\\vfill\n'.join(r'\noindent ' + cell(*INF[i]) + r'\hfill' + cell(*INF[i + 1]) + r'\par' for i in range(0, 6, 2)) + '\n\\vfill\n'

# ---------- 4. conversió a LaTeX ----------
UNI = {'→': r'$\to$', '∞': r'$\infty$', '≪': r'$\ll$', '≤': r'$\leq$', '≥': r'$\geq$', '−': '-', '○': r'$\circ$', '∄': r'$\nexists$',
       '✓': '', '✗': '', '✎': '', '✍': '', '🎓': '', '◉': '', '⚙': '', '…': r'\dots{}', '×': r'$\times$', '≠': r'$\neq$', '±': r'$\pm$'}
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
        for a, b in UNI.items(): part = part.replace(a, b)
        part = part.replace('l·l', r'\lgem{}').replace('L·L', r'\Lgem{}')
        part = re.sub(r'\$\$', '', part)
        out.append(part)
    return ''.join(out)

IN_TABLE = [False]
BADGE = {'ok': 'fmok', 'ev': 'fmev', 'sf': 'fmsf', 'si': 'fmsi', 'as': 'fmas'}
def text(n): return ''.join(conv(k) for k in n.kids)
def plain(n):
    return ''.join(k if isinstance(k, str) else plain(k) for k in n.kids)
def items(n):
    return ''.join(r'\item ' + text(k).strip() + '\n' for k in n.kids if not isinstance(k, str) and k.tag == 'li')

def conv(n):
    if isinstance(n, str):
        return esc(n) if n.strip() or ' ' in n else ''
    t, c = n.tag, n.cls()
    if t in ('input', 'select', 'button', 'svg', 'summary', 'label', 'option'): return ''
    if 'widget' in c or 'box' in c and 'pr' in c or 'steps-ctl' in c or 'sec-head' in c: return ''
    if t == 'section': return conv_section(n)
    if t == 'h3': return '\n\\Needspace{16\\baselineskip}\n\\subsection*{%s}\n' % text(n).strip()
    if 'box' in c:
        kind = [k for k in ('def', 'prop', 'ex') if k in c][0]
        bh = next(k for k in n.kids if not isinstance(k, str) and 'bh' in k.cls())
        bb = next(k for k in n.kids if not isinstance(k, str) and 'bb' in k.cls())
        title = text(bh).strip()
        inner = text(bb).strip()
        if 'pdf-inf' in plain_cls(bb):  # el requadre ocupa la resta de la pàgina
            return '\n\\newpage\n\\begin{fmexfill}{%s}\n\\begin{minipage}[t][\\tcbtextheight][s]{\\linewidth}\n%s\n\\end{minipage}\n\\end{fmexfill}\n' % (title, inner)
        return '\n\\Needspace{7\\baselineskip}\n\\begin{fm%s}{%s}\n%s\n\\end{fm%s}\n' % (kind, title, inner, kind)
    if t == 'p':
        inner = text(n).strip()
        if not inner: return ''
        if 'note' in c: return '\n\\begin{fmnote}%s\\end{fmnote}\n' % inner
        return '\n\n' + inner + '\n\n'
    if t == 'ul': return '\n\\begin{itemize}\n%s\\end{itemize}\n' % items(n)
    if t == 'ol':
        if 'alpha' in c: return '\n\\begin{enumerate}[label=\\alph*)]\n%s\\end{enumerate}\n' % items(n)
        if 'ex-list' in c: return '\n\\begin{enumerate}[label=\\textbf{\\arabic*.},leftmargin=*]\n%s\\end{enumerate}\n' % items(n)
        return '\n\\begin{enumerate}\n%s\\end{enumerate}\n' % items(n)
    if t == 'li': return text(n)
    if t in ('strong', 'b'): return r'\textbf{%s}' % text(n)
    if t == 'em': return r'\emph{%s}' % text(n)
    if t == 'u': return r'\underline{%s}' % text(n)
    if t == 'sup': return r'\textsuperscript{%s}' % text(n)
    if t == 'code': return r'\texttt{%s}' % text(n)
    if t == 'small': return r'{\footnotesize %s}' % text(n)
    if t == 'span':
        if 'key' in c: return r'\fmkey{%s}' % text(n)
        if 'u-line' in c: return r'\fmuline{%s}' % text(n)
        if 'badge' in c: return r'\fmbadge{%s}{%s}' % (BADGE[c[1]], text(n))
        if 'pau' in c: return r'\fmpau{%s}' % text(n)
        if 'lt' in c: return r' $\ll$ '
        return text(n)
    if t == 'details':  # solucions curtes: es mostren
        inner = ''.join(conv(k) for k in n.kids if not (not isinstance(k, str) and k.tag == 'summary'))
        return '\n\n' + r'\textit{Solució:} ' + inner.strip() + '\n\n'
    if 'steps' in c:
        return '\n' + ''.join(conv(k) for k in n.kids) + '\n'
    if 'step' in c: return '\n\n' + text(n).strip() + '\n\n'
    if t in ('figure', 'div') and n.a.get('data-g'):
        return '\n\\begin{center}%s\\end{center}\n' % FIG[n.a['data-g']]
    if t == 'figure' and 'lfig' not in c:  # dins de fig4
        return text(n)
    if 'ttl' in c: return r'{\centering %s\par}' % text(n)
    if t == 'figcaption': return r'{\centering\footnotesize %s\par}' % text(n)
    if 'fig4' in c:
        figs = [k for k in n.kids if not isinstance(k, str)]
        w = 0.98 / min(len(figs), 4)
        return '\n\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{%.3f\linewidth}\centering %s\end{minipage}' % (w - 0.01, conv_fig4(k)) for k in figs) + '\\par\n'
    if 'two' in c:
        cols = [k for k in n.kids if not isinstance(k, str)]
        out = []
        for i in range(0, len(cols), 2):
            pair = cols[i:i + 2]
            out.append('\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{0.48\linewidth}\vspace{0pt}\raggedright %s\end{minipage}' % (conv(k) if k.a.get('data-g') else text(k)).strip() for k in pair) + '\\par\\medskip\n')
        return '\n' + ''.join(out)
    if 'pdf-inf' in c: return INF_EXAMPLES
    if 'hier' in c:
        parts = []
        for k in n.kids:
            if isinstance(k, str): continue
            if 'lv' in k.cls():
                sm = next(x for x in k.kids if not isinstance(x, str) and x.tag == 'small')
                rest = ''.join(conv(x) for x in k.kids if x is not sm)
                parts.append(r'\fmlevel{%s}{%s}' % (plain(sm), rest.strip()))
            else: parts.append(r'{\Large\color{fmaccent}$\ll$}')
        return '\n\\begin{center}' + r'\quad'.join(parts) + '\\end{center}\n'
    if 'indet' in c:
        return '\n\\begin{center}' + r'\ '.join(r'\fmchip{%s}' % text(k) for k in n.kids if not isinstance(k, str)) + '\\end{center}\n'
    if t == 'table': return conv_table(n)
    return text(n)

def plain_cls(n):
    return ' '.join(n.cls() + [plain_cls(k) for k in n.kids if not isinstance(k, str)])
def conv_fig4(fig):
    return ''.join(conv(k) for k in fig.kids)

def rows_of(n):
    out = []
    for k in n.kids:
        if isinstance(k, str): continue
        if k.tag == 'tr': out.append(k)
        else: out += rows_of(k)
    return out
def conv_table(n):
    rows = rows_of(n)
    first = [c for c in rows[0].kids if not isinstance(c, str)] if rows else []
    ruffini = len(rows) == 3 and first and not plain(first[0]).strip() and not any(c.tag == 'th' for c in first)
    if 'rf' in n.cls() or ruffini:  # Ruffini (també les taules sense capçalera amb la forma de Ruffini)
        IN_TABLE[0] = True
        cells = [[text(c).strip() for c in r.kids if not isinstance(c, str)] for r in rows]
        IN_TABLE[0] = False
        cells = [[('$' + x.strip('$').replace('\\mathbf ', '').replace('−', '-') + '$') if x else '' for x in r] for r in cells]
        m = len(cells[0])
        s = r'\begin{tabular}{r|%s}' % ('r' * (m - 1)) + '\n'
        s += ' & '.join(cells[0]) + r'\\' + '\n' + ' & '.join(cells[1]) + r'\\\hline' + '\n'
        last = cells[2]; last[-1] = r'\fbox{%s}' % last[-1]
        s += ' & '.join(last) + r'\\' + '\n' + r'\end{tabular}'
        return '\n\\begin{center}%s\\end{center}\n' % s
    m = max(len([c for c in r.kids if not isinstance(c, str)]) for r in rows)
    if 'ops' in n.cls():  # operacions amb infinit: columnes que ocupen tot l'ample
        s = r'\small\begin{tabularx}{\linewidth}{%s}\toprule' % ('>{\\centering\\arraybackslash}X' * m) + '\n'
        for r in rows:
            cs = [c for c in r.kids if not isinstance(c, str)]
            head = all(c.tag == 'th' for c in cs)
            s += ' & '.join((r'\textbf{%s}' if head else '%s') % text(c).strip() for c in cs) + r'\\' + (r'\midrule' if head else r'[4pt]') + '\n'
        return '\n\\begin{center}%s\\bottomrule\\end{tabularx}\\end{center}\n' % s
    IN_TABLE[0] = True
    s = r'\begin{tabular}{%s}\toprule' % ('c' * m) + '\n'
    for i, r in enumerate(rows):
        cs = [c for c in r.kids if not isinstance(c, str)]
        head = all(c.tag == 'th' for c in cs)
        line = ' & '.join((r'\textbf{%s}' if head else '%s') % text(c).strip() for c in cs)
        s += line + r'\\' + (r'\midrule' if head else '') + '\n'
    s += r'\bottomrule\end{tabular}'
    IN_TABLE[0] = False
    return '\n\\begin{center}\\renewcommand{\\arraystretch}{1.5}%s\\end{center}\n' % s

def conv_section(n):
    h2 = next(k for k in n.kids if not isinstance(k, str) and 'sec-head' in k.cls())
    title = text(next(k for k in h2.kids if not isinstance(k, str) and k.tag == 'h2')).strip()
    return '\n\\Needspace{12\\baselineskip}\n\\section{%s}\n' % title + ''.join(conv(k) for k in n.kids)

latex = conv(ROOT)
latex = re.sub(r'\n{3,}', '\n\n', latex)
latex = re.sub(r'(?<!\\)\\\[', '\n\\[', latex)
latex = re.sub(r'(?<!\\)\\\]', '\\]\n', latex)
latex = re.sub(r'\\\]\s*([.,;])', r'\\,\1\\]', latex)  # el punt final va dins de la fórmula centrada
latex = re.sub(r'\n{3,}', '\n\n', latex)

# ---------- 5. document ----------
PRE = r'''\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[catalan]{babel}
\usepackage{lmodern}
\linespread{1.22}
\usepackage[a4paper,top=2.4cm,bottom=2.2cm,left=1.5cm,right=1.5cm,headheight=1.1cm,headsep=0.5cm,footskip=1cm]{geometry}
\usepackage{amsmath,amssymb,cancel}
\usepackage{icomma}
\usepackage{graphicx}
\usepackage[table]{xcolor}
\usepackage{tikz}
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
\usepackage[hidelinks,pdftitle={Apunts de teoria. Unitat 4: Límits i continuïtat. 2n de Batxillerat CCSS},pdfsubject={Matemàtiques Aplicades a les Ciències Socials II},pdfkeywords={límits, indeterminacions, continuïtat, asímptotes}]{hyperref}

% colors de la web (FentMates, bloc d'anàlisi)
\definecolor{fmnavy}{HTML}{1B2748}
\definecolor{fmgreen}{HTML}{6A8A33}
\definecolor{fmgreenl}{HTML}{7FA040}
\definecolor{fmyellow}{HTML}{FFC94D}
\definecolor{fmgold}{HTML}{E9A919}
\definecolor{fmaccent}{HTML}{FF7A50}
\definecolor{fmteal}{HTML}{2BB3A3}
\definecolor{fmdef}{HTML}{1D4F73}\definecolor{fmdefbg}{HTML}{EEF4F9}
\definecolor{fmprop}{HTML}{3B4252}\definecolor{fmpropbg}{HTML}{F3F4F7}
\definecolor{fmex}{HTML}{A3203A}\definecolor{fmexbg}{HTML}{FBF0F2}
\definecolor{fmmuted}{HTML}{5D6685}
\definecolor{fmsurface}{HTML}{EEF1F8}

\newcommand{\lt}{<}\newcommand{\gt}{>}
% fórmula en línia que no es parteix mai; si no cap en una línia, es posa centrada
\newcommand{\fmm}[1]{\setbox0=\hbox{$#1$}\ifdim\wd0>\linewidth\[#1\]\else\mbox{\box0}\fi}
\DeclareUnicodeCharacter{2212}{-}
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\setlength{\lineskip}{5pt}\setlength{\lineskiplimit}{5pt}  % més aire al voltant de les fraccions en línia
\setlength{\emergencystretch}{3em}
\setlist{itemsep=4pt,topsep=4pt}
\renewcommand{\thesection}{4.\arabic{section}}
\titleformat{\section}{\color{fmnavy}\Large\bfseries}{\colorbox{fmdef}{\color{white}\strut\ \thesection\ }}{0.6em}{}[{\color{fmdef}\titlerule[1.2pt]}]
\titlespacing*{\section}{0pt}{16pt}{8pt}
\titleformat*{\subsection}{\color{fmgreen}\large\bfseries}
\allowdisplaybreaks

% logo de la web: adhesiu verd amb la gràfica + «Fent» «Mates»
\newcommand{\fmlogo}[1]{\begin{tikzpicture}[x=#1/124,y=#1/124,baseline=-0.35*#1]
  \fill[fmgreenl,rounded corners=#1*0.24] (-62,-62) rectangle (62,62);
  \begin{scope}[yscale=-1,scale=1.15,line width=#1*0.045,line cap=round,line join=round,draw=white]
  \draw (-36,24)--(36,24) (-28,32)--(-28,-32);
  \draw (-34,18) .. controls (-14,18) and (-10,-24) .. (6,-24) .. controls (22,-24) and (24,10) .. (36,-6);
  \end{scope}\end{tikzpicture}}
% dibuix de la targeta de la unitat a la web (illustrations.js, «limits»), en blanc
\newcommand{\fmcard}{\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round]
  \draw[line width=3pt] (14,104)--(226,104) (24,114)--(24,8);
  \draw[line width=4pt,dash pattern=on 10pt off 10pt] (24,36)--(226,36);
  \draw[line width=4.5pt] (32,100) .. controls (70,98) and (92,80) .. (112,64);
  \draw[line width=4.5pt] (122,58) .. controls (150,44) and (180,40) .. (222,38);
  \draw[line width=4.5pt] (117,61) circle (5.5);
  \node[anchor=base west,inner sep=0pt,scale=2.4,font=\large\itshape] at (138,84) {lím $f(x)=L$};
\end{tikzpicture}}
\newcommand{\fmbrand}{\raisebox{-0.25\height}{\includegraphics[height=0.5cm]{../../logo/pdf/horitzontal-clar.pdf}}}

% capçalera i peu
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\fmbrand}
\fancyhead[R]{\small\color{fmmuted}2n Batxillerat CCSS · Unitat 4: Límits i continuïtat}
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
\newtcolorbox{fmex}[1]{fmbase,colback=fmexbg,colframe=fmex,colbacktitle=fmexbg,coltitle=fmex,title={\faPencil*\ #1},
  titlerule=0.4pt,titlerule style={fmex!40,dashed}}
\newtcolorbox{fmexfill}[1]{fmbase,breakable=false,height fill,colback=fmexbg,colframe=fmex,colbacktitle=fmexbg,coltitle=fmex,title={\faPencil*\ #1},
  titlerule=0.4pt,titlerule style={fmex!40,dashed}}
\newtcolorbox{fmnote}{enhanced,breakable,colback=white,colframe=white,borderline west={3pt}{0pt}{fmaccent},arc=0pt,left=3mm,right=2mm,top=1mm,bottom=1mm,before skip=6pt,after skip=6pt,before upper=\raggedright}
\newcommand{\fmkey}[1]{\colorbox{fmyellow!45}{\strut #1}}
\newcommand{\fmuline}[1]{\textbf{\color{fmaccent}#1}}
\definecolor{fmok}{HTML}{15803D}\definecolor{fmev}{HTML}{2563EB}\definecolor{fmsf}{HTML}{C2410C}\definecolor{fmsi}{HTML}{7C3AED}\definecolor{fmas}{HTML}{A3203A}
\newcommand{\fmbadge}[2]{\tcbox[on line,colback=#1,colframe=#1,arc=2mm,boxsep=0pt,left=4pt,right=4pt,top=1.5pt,bottom=1.5pt]{\color{white}\footnotesize\bfseries #2}}
\newcommand{\fmpau}[1]{\tcbox[on line,colback=fmnavy,colframe=fmnavy,arc=2mm,boxsep=0pt,left=4pt,right=4pt,top=1.5pt,bottom=1.5pt]{\color{white}\scriptsize\bfseries\MakeUppercase{#1}}\ }
\newcommand{\fmchip}[1]{\tcbox[on line,colback=fmsf!10,colframe=fmsf!50,arc=2mm,boxsep=1pt,left=4pt,right=4pt]{#1}}
\newcommand{\fmlevel}[2]{\tcbox[on line,colback=white,colframe=fmmuted!40,arc=2mm,boxsep=2pt,halign=center]{\begin{tabular}{c}{\scriptsize\color{fmmuted}\MakeUppercase{#1}}\\#2\end{tabular}}}

% gràfiques
\pgfplotsset{fmaxis/.style={axis lines=middle,grid=major,grid style={fmmuted!15},axis line style={fmmuted,-latex},
  tick label style={font=\scriptsize,color=fmmuted},clip=true,unbounded coords=jump,restrict y to domain=-200:200,
  every axis plot/.append style={line join=round}},
  fmcurve/.style={fmaccent,line width=1.6pt,smooth}}
\tikzset{fmasy/.style={fmmuted,dashed,line width=0.9pt},fmguide/.style={fmaccent,dotted,line width=0.8pt},
  fmdot/.style={circle,fill=fmaccent,inner sep=0pt,minimum size=5pt},fmopen/.style={circle,draw=fmaccent,fill=white,line width=1pt,inner sep=0pt,minimum size=5pt}}
'''

TITLE = r'''
\begin{document}
\thispagestyle{primera}
\begin{tikzpicture}[remember picture,overlay]
  \fill[fmgreen] (current page.north west) rectangle ([yshift=-8.9cm]current page.north east);
  \begin{scope}
    \clip (current page.north west) rectangle ([yshift=-8.9cm]current page.north east);
    \node[anchor=north west,inner sep=0pt,opacity=0.15] at ([xshift=6.13cm,yshift=-0.41cm]current page.north west) {\fmcard};
  \end{scope}
  \node[anchor=north west,inner sep=0pt] at ([xshift=1.5cm,yshift=-1.1cm]current page.north west) {\tcbox[colback=white,colframe=white,arc=2.5mm,boxsep=0pt,left=7pt,right=7pt,top=5pt,bottom=5pt]{\includegraphics[height=0.75cm]{../../logo/pdf/horitzontal-clar.pdf}}};
\end{tikzpicture}
\vspace*{0.55cm}
\tcbox[colback=white!15!fmgreen,colframe=white!15!fmgreen,arc=2.5mm,boxsep=0pt,left=6pt,right=6pt,top=3pt,bottom=3pt]{\color{white}\small\bfseries Apunts de teoria · 2n Batxillerat CCSS II}

\vspace{4pt}
{\color{white}\fontsize{28}{32}\selectfont\bfseries{\color{fmyellow}Unitat 4} · Límits i continuïtat\par}
\vspace{6pt}
\begin{minipage}{\linewidth}\color{white!88!fmgreen}\small HERO\end{minipage}
\vspace{1.1cm}

\begin{tcolorbox}[colback=fmsurface,colframe=fmsurface,arc=3mm,left=4mm,right=4mm,top=2mm,bottom=2mm]
\small\textbf{Índex}\par\smallskip
\begin{minipage}[t]{0.49\linewidth}\small TOC1\end{minipage}\hfill\begin{minipage}[t]{0.49\linewidth}\small TOC2\end{minipage}
\end{tcolorbox}
'''

secs = re.findall(r'\\section\{(.*?)\}\n', latex)
TOCNAME = {8: "Estudi de la continuïtat d'una funció", 9: "Funcions a trossos depenents d'un paràmetre"}
toc = [r'\mbox{\hyperlink{sec%d}{\textbf{\color{fmgreen}4.%d}\ \ %s}}\\[3pt]' % (i + 1, i + 1, (esc(TOCNAME[i + 1]) if i + 1 in TOCNAME else s)) for i, s in enumerate(secs)]
half = (len(toc) + 1) // 2
k = [0]
def anchor(m):
    k[0] += 1
    return '\\section{%s}\\hypertarget{sec%d}{}\n' % (m.group(1), k[0])
latex = re.sub(r'\\section\{(.*?)\}\n', anchor, latex)
hero_tex = esc(re.sub(r'\s*,?\s*eines interactives', '', hero).replace('Teoria, exemples resolts pas a pas i:', 'Teoria i exemples resolts pas a pas:'))
title = TITLE.replace('HERO', hero_tex).replace('TOC1', '\n'.join(toc[:half])).replace('TOC2', '\n'.join(toc[half:]))
doc = PRE + title + latex + '\n\\end{document}\n'
open(os.path.join(HERE, 't4-apunts-teoria.tex'), 'w', encoding='utf-8').write(doc)
print(len(secs), 'apartats,', len(doc), 'caràcters')
