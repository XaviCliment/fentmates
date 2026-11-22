# Genera t6-apunts-teoria.tex (2n Batxillerat CCSS, Unitat 6: Aplicacions de la derivada): apunts de teoria en PDF
# per a l'alumnat, a partir dels apunts interactius (_eines/apunts/2batx-ccss-t6/contingut.html).
# Adaptat de ../2batx-ccss-t5/apunts.py: mateix preàmbul i mateixa conversió, més les taules de signes (table.sgn).
# El .tex es copia a la carpeta de l'escriptori «Apunts teòrics 2n BAT CCSS/Unitat 6» (amb logo-fentmates.pdf)
# perquè l'autor el retoque i el compile. Deixa fora els ginys, les caixes «Practica», l'eina d'estudi i l'autoavaluació.
# Les gràfiques es redibuixen amb pgfplots a partir de les figures estàtiques d'app.js (FIGS).
# Ús: python3 apunts.py [es] && pdflatex t6-apunts-teoria.tex (o t6-apunts-teoria-es.tex) (dues vegades, per l'índex)
import os, re, sys
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', 'apunts', '2batx-ccss-t6', 'contingut.html')

# ---------- 1. HTML en valencià ----------
src = open(SRC, encoding='utf-8').read()
ES = len(sys.argv) > 1 and sys.argv[1] == 'es'
def T(va, es): return es if ES else va   # textos propis del generador
src = re.sub(r'⟦(.*?)‖(.*?)‖.*?⟧', r'\2' if ES else r'\1', src, flags=re.S)
src = re.sub(r'⟪(.*?)‖(.*?)‖.*?⟫', r'\2' if ES else r'\1', src, flags=re.S)
src = src.replace(r'\SI', r'\text{si }')
hero = re.search(r'<section class="hero">.*?<p>(.*?)</p>', src, re.S).group(1)
body = src[src.index('<section class="unit" id="s1">'):src.index('<section class="unit" id="lab">')]

def fix(a, b):
    global body
    assert body.count(a) == 1, a[:80]
    body = body.replace(a, b)
# la fórmula de la recta tangent no cap en mitja columna: dues línies
fix(r'''\[y-f(a)=f'(a)\cdot(x-a)\qquad\Longleftrightarrow\qquad y=f(a)+f'(a)\cdot(x-a)\]''',
    r'''\[y-f(a)=f'(a)\cdot(x-a)\]\[\Longleftrightarrow\quad y=f(a)+f'(a)\cdot(x-a)\]''')
# noms curts de l'índex (els de la web)
tocnames = [re.sub(r'<.*?>', '', x) for x in re.findall(r'<span class="n">6\.\d</span>(.*?)<span class="ck">', src)]

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
def tl(a, b, m, x0, y0, col='fmteal'): return r'\addplot[%s,line width=1.2pt,domain=%s:%s]{%s*(x-(%s))+(%s)};' % (col, a, b, m, x0, y0)
def tx(x, y, t, anc='center'): return r'\node[anchor=%s,font=\footnotesize,align=center] at (axis cs:%s,%s) {%s};' % (anc, x, y, t)
def mk(x, y, col): return r'\node[circle,fill=%s,draw=white,line width=0.8pt,inner sep=0pt,minimum size=7pt] at (axis cs:%s,%s) {};' % (col, x, y)
def cc(e, a, b, col, n=120): return r'\addplot[%s,line width=1.6pt,smooth,domain=%s:%s,samples=%d]{%s};' % (col, a, b, n, e)
def hz(y, a, b, col='fmteal'): return r'\addplot[%s,line width=1.2pt,domain=%s:%s]{%s};' % (col, a, b, y)
def gpt(x, y): return (r'\draw[fmguide] (axis cs:%s,0)--(axis cs:%s,%s);' % (x, x, y)) + (r'\draw[fmguide] (axis cs:0,%s)--(axis cs:%s,%s);' % (y, x, y))
FIG = {
 'tan': axis([-1, 4, -0.5, 7], cv('x^2/2+1', -1, 4) + tl(-1, 4, 1, 1, 1.5) + gpt(1, 1.5) + pt(1, 1.5)
             + tx(0.85, 2.2, '$P(a,f(a))$', 'east') + tx(4, 2.6, "$m=f'(a)$", 'north east'), '6.4cm', '5cm'),
 'tn': r'\begin{tikzpicture}\begin{axis}[fmaxis,axis equal image,width=6.4cm,xmin=-2,xmax=6,ymin=-1.4,ymax=6.2]'
       + cv('x^2/4+1', -2, 6) + tl(-2, 6, 1, 2, 2) + tl(-2, 6, -1, 2, 2, 'fmsi') + pt(2, 2)
       + tx(4.4, 3.6, T('tangent', 'tangente'), 'west') + tx(-0.2, 4.6, 'normal', 'west') + tx(2.25, 1.55, '$P$', 'west')
       + r'\end{axis}\end{tikzpicture}',
 'mono': axis([-2.6, 2.6, -4, 4], cc('x^3-3*x', -2.6, -1, 'fmok') + cc('x^3-3*x', -1, 1, 'fmas') + cc('x^3-3*x', 1, 2.6, 'fmok')
              + tx(-1.75, 3.3, r"\color{fmok}$f'>0\ \nearrow$") + tx(0.75, 3.3, r"\color{fmas}$f'<0\ \searrow$") + tx(1.75, -3.3, r"\color{fmok}$f'>0\ \nearrow$"), '6.4cm', '5cm'),
 'ext': axis([-2.6, 2.6, -4, 4], cv('x^3-3*x', -2.6, 2.6) + hz(2, -1.8, -0.2) + hz(-2, 0.2, 1.8) + mk(-1, 2, 'fmok') + mk(1, -2, 'fmas')
             + tx(-1.25, 2.75, T('màxim relatiu', 'máximo relativo')) + tx(1.25, -2.85, T('mínim relatiu', 'mínimo relativo')), '6.4cm', '5cm'),
 'x3': axis([-2, 2, -3, 3], cv('x^3', -2, 2) + hz(0, -1, 1) + pt(0, 0)
            + tx(0.15, -0.9, T(r"$f'(0)=0$, però\\no és extrem", r"$f'(0)=0$, pero\\no es extremo"), 'north west'), '6.4cm', '5cm'),
 'absf': axis([-0.6, 5.8, -5, 25], cc('x^3-6*x^2+9*x+2', -0.6, 5.8, 'fmmuted!35') + cv('x^3-6*x^2+9*x+2', 0, 5) + gd(0) + gd(5) + pt(1, 6)
              + mk(5, 22, 'fmok') + mk(0, 2, 'fmas') + mk(3, 2, 'fmas')
              + tx(1, 8.4, T('màx. relatiu', 'máx. relativo')) + tx(4.7, 22, T('màx. absolut', 'máx. absoluto'), 'east') + tx(3, 0.6, T('mín. absolut', 'mín. absoluto'), 'north'), '6.4cm', '5cm'),
}

# ---------- 4. conversió a LaTeX ----------
UNI = {'→': r'$\to$', '∞': r'$\infty$', '≪': r'$\ll$', '≤': r'$\leq$', '≥': r'$\geq$', '−': '-', '○': r'$\circ$', '∄': r'$\nexists$',
       '✓': '', '✗': '', '✎': '', '✍': '', '🎓': '', '◉': '', '⚙': '', '…': r'\dots{}', '×': r'$\times$', '≠': r'$\neq$', '±': r'$\pm$', '↗': r'$\nearrow$', '↘': r'$\searrow$', '∩': r'$\cap$', '∪': r'$\cup$', '–': '--'}
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
        return '\n\\Needspace{7\\baselineskip}\n\\begin{fm%s}{%s}\n%s\n\\end{fm%s}\n' % (kind, title, inner, kind)
    if t == 'p':
        inner = text(n).strip()
        if not inner: return ''
        if 'note' in c: return '\n\\begin{fmnote}%s\\end{fmnote}\n' % inner
        if 'key' in c: return '\n\\begin{center}\\colorbox{fmyellow!45}{\\parbox{0.9\\linewidth}{\\centering\\strut %s\\strut}}\\end{center}\n' % inner
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
        return '\n\n' + T(r'\textit{Solució:} ', r'\textit{Solución:} ') + inner.strip() + '\n\n'
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
def conv_sgn(n):
    rows = rows_of(n)
    IN_TABLE[0] = True
    out = []
    for r in rows:
        cs = [c for c in r.kids if not isinstance(c, str)]
        line = []
        for c in cs:
            k, v = c.cls(), text(c).strip()
            if c.tag == 'th': v = r'\textbf{%s}' % v
            elif 'ar' in k: v = r'{\Large\color{%s}%s}' % ('fmok' if 'p' in k else 'fmas', v)
            elif 'p' in k: v = r'\textbf{\color{fmok}$+$}'
            elif 'm' in k: v = r'\textbf{\color{fmas}$-$}'
            line.append(v)
        out.append(' & '.join(line) + r'\\')
    IN_TABLE[0] = False
    m = max(len([c for c in r.kids if not isinstance(c, str)]) for r in rows)
    s = r'\begin{tabular}{l|%s}\toprule' % ('c' * (m - 1)) + '\n' + '\n'.join(o + (r'\midrule' if i < len(out) - 1 else '') for i, o in enumerate(out)) + '\n' + r'\bottomrule\end{tabular}'
    return '\n\\begin{center}\\small\\renewcommand{\\arraystretch}{1.6}%s\\end{center}\n' % s
def conv_table(n):
    if 'sgn' in n.cls(): return conv_sgn(n)
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
    return '\n\\Needspace{18\\baselineskip}\n\\section{%s}\n' % title + ''.join(conv(k) for k in n.kids)

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
\usepackage[hidelinks,pdftitle={Apunts de teoria. Unitat 6: Aplicacions de la derivada. 2n de Batxillerat CCSS},pdfsubject={Matemàtiques Aplicades a les Ciències Socials II},pdfkeywords={recta tangent, recta normal, monotonia, creixement, màxims i mínims, extrems absoluts, optimització}]{hyperref}

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
\setlength{\parskip}{12pt}
\setlength{\lineskip}{5pt}\setlength{\lineskiplimit}{5pt}  % més aire al voltant de les fraccions en línia
\setlength{\emergencystretch}{3em}
\setlist{itemsep=4pt,topsep=4pt}
\renewcommand{\thesection}{6.\arabic{section}}
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
% dibuix de la targeta de la unitat a la web (illustrations.js, «aplicacions»), en blanc
\newcommand{\fmcard}{\begin{tikzpicture}[x=0.062cm,y=-0.062cm,white,line cap=round,line join=round]
  \draw[line width=3pt] (14,104)--(226,104) (24,114)--(24,8);
  \draw[line width=4.5pt] (30,98) .. controls (50,50) and (64,26) .. (82,26) .. controls (100,26) and (116,86) .. (146,86) .. controls (170,86) and (196,50) .. (222,16);
  \draw[line width=4pt,dash pattern=on 10pt off 10pt] (56,26)--(108,26) (120,86)--(172,86);
  \fill (82,26) circle (5.5) (146,86) circle (5.5);
  \node[anchor=base west,inner sep=0pt,scale=3] at (34,56) {$\nearrow$};
  \node[anchor=base west,inner sep=0pt,scale=3] at (112,48) {$\searrow$};
  \node[anchor=base west,inner sep=0pt,scale=3] at (196,62) {$\nearrow$};
\end{tikzpicture}}
\newcommand{\fmbrand}{\raisebox{-0.25\height}{\includegraphics[height=0.5cm]{logo-fentmates.pdf}}}

% capçalera i peu
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\fmbrand}
\fancyhead[R]{\small\color{fmmuted}2n Batxillerat CCSS · Unitat 6: Aplicacions de la derivada}
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
  \fill[fmgreen] (current page.north west) rectangle ([yshift=-10.1cm]current page.north east);
  \begin{scope}
    \clip (current page.north west) rectangle ([yshift=-10.1cm]current page.north east);
    \node[anchor=north west,inner sep=0pt,opacity=0.15] at ([xshift=6.13cm,yshift=-0.41cm]current page.north west) {\fmcard};
  \end{scope}
  \node[anchor=north west,inner sep=0pt] at ([xshift=1.5cm,yshift=-1.1cm]current page.north west) {\tcbox[colback=white,colframe=white,arc=2.5mm,boxsep=0pt,left=7pt,right=7pt,top=5pt,bottom=5pt]{\includegraphics[height=0.75cm]{logo-fentmates.pdf}}};
\end{tikzpicture}
\vspace*{0.55cm}
\tcbox[colback=white!15!fmgreen,colframe=white!15!fmgreen,arc=2.5mm,boxsep=0pt,left=6pt,right=6pt,top=3pt,bottom=3pt]{\color{white}\small\bfseries Apunts de teoria · 2n Batxillerat CCSS II}

\vspace{4pt}
{\color{white}\fontsize{28}{32}\selectfont\bfseries{\color{fmyellow}Unitat 6} · Aplicacions\\[2pt] de la derivada\par}
\vspace{6pt}
\begin{minipage}{\linewidth}\color{white!88!fmgreen}\small HERO\end{minipage}
\vspace{1.1cm}

\begin{tcolorbox}[colback=fmsurface,colframe=fmsurface,arc=3mm,left=4mm,right=4mm,top=2mm,bottom=2mm]
\small\textbf{Índex}\par\smallskip
\begin{minipage}[t]{0.49\linewidth}\small TOC1\end{minipage}\hfill\begin{minipage}[t]{0.49\linewidth}\small TOC2\end{minipage}
\end{tcolorbox}
'''

secs = re.findall(r'\\section\{(.*?)\}\n', latex)
assert len(tocnames) == len(secs) == 7, (len(tocnames), len(secs))
toc = [r'\mbox{\hyperlink{sec%d}{\textbf{\color{fmgreen}6.%d}\ \ %s}}\\[3pt]' % (i + 1, i + 1, esc(tocnames[i])) for i in range(len(secs))]
half = (len(toc) + 1) // 2
k = [0]
def anchor(m):
    k[0] += 1
    return '\\section{%s}\\hypertarget{sec%d}{}\n' % (m.group(1), k[0])
latex = re.sub(r'\\section\{(.*?)\}\n', anchor, latex)
hero_tex = esc(re.sub(T(r'\s*,?\s*i eines interactives', r'\s*,?\s*y herramientas interactivas'), '', hero).replace(T('Teoria, exemples resolts pas a pas:', 'Teoría, ejemplos resueltos paso a paso:'), T('Teoria i exemples resolts pas a pas:', 'Teoría y ejemplos resueltos paso a paso:')))
title = TITLE.replace('HERO', hero_tex).replace('TOC1', '\n'.join(toc[:half])).replace('TOC2', '\n'.join(toc[half:]))
doc = PRE + title + latex + '\n\\end{document}\n'
def post(a, b, n=1):
    global doc
    assert doc.count(a) >= 1, a[:80]
    doc = doc.replace(a, b, n)
post(T(r'\fmuline{Mètode}:', r'\fmuline{Método}:'), r'\newpage' + '\n\n' + T(r'\fmuline{Mètode}:', r'\fmuline{Método}:'))
post('\\end{fmdef}\n', '\\end{fmdef}\n\n\\vspace*{0.2cm}')
post('\\Needspace{7\\baselineskip}\n\\begin{fmprop}{' + T("Altres tipus d'exercicis de tangents", 'Otros tipos de ejercicios de tangentes'),
     '\\vspace*{0.2cm}\n\\Needspace{7\\baselineskip}\n\\begin{fmprop}{' + T("Altres tipus d'exercicis de tangents", 'Otros tipos de ejercicios de tangentes'))
post(T(r"ve donat per \fmm{f(x)=-0{,}1x^2+2{,}5x-10}, on", r"viene dado por \fmm{f(x)=-0{,}1x^2+2{,}5x-10}, donde"),
     T(r"ve donat per: \[f(x)=-0{,}1x^2+2{,}5x-10,\]on", r"viene dado por: \[f(x)=-0{,}1x^2+2{,}5x-10,\]donde"))
post(T(r"milions d'euros. \textbf{a)}", r"millones de euros. \textbf{a)}"), T("milions d'euros. \\\\ \n\\textbf{a)}", "millones de euros. \\\\ \n\\textbf{a)}"))
post(T(r"ve donat per \fmm{C(t)=t^3-15t^2+63t+40}, \fmm{t\in[0,8]} (en hores).", r"viene dado por \fmm{C(t)=t^3-15t^2+63t+40}, \fmm{t\in[0,8]} (en horas)."),
     T(r"ve donat per: \[C(t)=t^3-15t^2+63t+40,\,\, t\in[0,8] \text{(en hores)}.\]", r"viene dado por: \[C(t)=t^3-15t^2+63t+40,\,\, t\in[0,8] \text{(en horas)}.\]"))
post(T(r"És un interval tancat: comparem amb els extrems. \fmm{\ C(0)=40,\ C(3)=121,\ C(7)=89,\ C(8)=96}", r"Es un intervalo cerrado: comparamos con los extremos. \fmm{\ C(0)=40,\ C(3)=121,\ C(7)=89,\ C(8)=96}"),
     T(r"És un interval tancat, comparem amb els extrems:\[\ C(0)=40,\ C(3)=121,\ C(7)=89,\ C(8)=96\]", r"Es un intervalo cerrado, comparamos con los extremos:\[\ C(0)=40,\ C(3)=121,\ C(7)=89,\ C(8)=96\]"))
post('\\Needspace{18\\baselineskip}\n\\section{' + T("Problemes d'optimització (II)", 'Problemas de optimización (II)'), '\\Needspace{10\\baselineskip}\n\\section{' + T("Problemes d'optimització (II)", 'Problemas de optimización (II)'))
if ES:
    for a, b in [(r'\usepackage[catalan]{babel}', r'\usepackage[spanish,es-minimal,es-noshorthands]{babel}'),
                 ("pdftitle={Apunts de teoria. Unitat 6: Aplicacions de la derivada. 2n de Batxillerat CCSS}", 'pdftitle={Apuntes de teoría. Unidad 6: Aplicaciones de la derivada. 2.º de Bachillerato CCSS}'),
                 ('pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}', 'pdfsubject={Matemáticas Aplicadas a las Ciencias Sociales II}'),
                 ('pdfkeywords={recta tangent, recta normal, monotonia, creixement, màxims i mínims, extrems absoluts, optimització}', 'pdfkeywords={recta tangente, recta normal, monotonía, crecimiento, máximos y mínimos, extremos absolutos, optimización}'),
                 ('2n Batxillerat CCSS · Unitat 6: Aplicacions de la derivada}', '2.º Bachillerato CCSS · Unidad 6: Aplicaciones de la derivada}'),
                 ('Apunts de teoria · 2n Batxillerat CCSS II}', 'Apuntes de teoría · 2.º Bachillerato CCSS II}'),
                 (r"{\color{fmyellow}Unitat 6} · Aplicacions\\[2pt] de la derivada\par}", r"{\color{fmyellow}Unidad 6} · Aplicaciones\\[2pt] de la derivada\par}"),
                 (r'\textbf{Índex}', r'\textbf{Índice}'),
                 # la introducció en castellà fa una línia més: franja verda més alta
                 ('rectangle ([yshift=-10.1cm]current page.north east);\n  \\begin{scope}', 'rectangle ([yshift=-10.6cm]current page.north east);\n  \\begin{scope}'),
                 ('\\clip (current page.north west) rectangle ([yshift=-10.1cm]', '\\clip (current page.north west) rectangle ([yshift=-10.6cm]'),
                 ('\\vspace{1.1cm}', '\\vspace{1.6cm}')]:
        assert doc.count(a) == 1, a
        doc = doc.replace(a, b)
    # amb el castellà de babel, les metadades dins de les opcions de hyperref fan petar pdflatex: van a \hypersetup
    m = re.search(r'\\usepackage\[hidelinks,(.*)\]\{hyperref\}\n', doc)
    doc = doc.replace(m.group(0), '\\usepackage[hidelinks]{hyperref}\n\\hypersetup{%s}\n' % m.group(1))
open(os.path.join(HERE, 't6-apunts-teoria-es.tex' if ES else 't6-apunts-teoria.tex'), 'w', encoding='utf-8').write(doc)
print(len(secs), 'apartats,', len(doc), 'caràcters')
