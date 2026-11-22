# Genera t10-apunts-teoria.tex (2n Batxillerat CCSS, Unitat 10: Distribució binomial i normal): apunts de teoria en PDF
# per a l'alumnat, a partir dels apunts interactius (_eines/apunts/2batx-ccss-t10/contingut-*.html, en ordre).
# Adaptat de ../2batx-ccss-t9/apunts.py: mateix preàmbul i mateixa conversió, amb els colors del bloc de probabilitat
# (morat). Novetats: les campanes de Gauss (svg data-nf, com wFigs() d'app.js) redibuixades amb TikZ, i les dues
# taules de la PAU (binomial n=2..9 i normal N(0,1), calculades com a build.py) en un annex al final; les caixes
# interactives de les taules (.box.lab) es canvien per una nota que remet a l'annex.
# El .tex es copia a la carpeta de l'escriptori «Apunts teòrics 2n BAT CCSS/Unitat 10» (amb logo-fentmates.pdf)
# perquè l'autor el retoque i el compile. Deixa fora els ginys, les caixes «Practica», la calculadora i l'autoavaluació.
# Ús: python3 apunts.py [es] && pdflatex t10-apunts-teoria.tex (o t10-apunts-teoria-es.tex) (dues vegades, per l'índex)
import os, re, sys, glob, math
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sorted(glob.glob(os.path.join(HERE, '..', '..', 'apunts', '2batx-ccss-t10', 'contingut-*.html')))

# ---------- 1. HTML en valencià ----------
src = ''.join(open(f, encoding='utf-8').read() for f in SRC)
ES = len(sys.argv) > 1 and sys.argv[1] == 'es'
def T(va, es): return es if ES else va   # textos propis del generador
src = re.sub(r'⟦(.*?)‖(.*?)‖.*?⟧', r'\2' if ES else r'\1', src, flags=re.S)
src = re.sub(r'⟪(.*?)‖(.*?)‖.*?⟫', r'\2' if ES else r'\1', src, flags=re.S)
src = src.replace(r'\SI', r'\text{si }')
hero = re.search(r'<section class="hero">.*?<p>(.*?)</p>', src, re.S).group(1)
body = src[src.index('<article>') + len('<article>'):src.index('<section class="unit" id="lab">')]

def fix(a, b):
    global body
    assert body.count(a) == 1, a[:80]
    body = body.replace(a, b)
# noms curts de l'índex (els de la web)
tocnames = [re.sub(r'<.*?>', '', x) for x in re.findall(r'<span class="n">10\.\d+</span>(.*?)<span class="ck">', src)]

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
def axis(v, body, w='6.4cm', h='4.6cm', opt=''):
    x0, x1, y0, y1 = v
    return (r'\begin{tikzpicture}\begin{axis}[fmaxis,width=%s,height=%s,xmin=%s,xmax=%s,ymin=%s,ymax=%s%s]%s\end{axis}\end{tikzpicture}'
            % (w, h, x0, x1, y0, y1, ',' + opt if opt else '', body))
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
def pc(x, y, col='fmteal'): return r'\node[circle,fill=%s,inner sep=0pt,minimum size=5.5pt] at (axis cs:%s,%s) {};' % (col, x, y)
def seg(x0, y0, x1, y1, col='fmteal'): return r'\draw[%s,line width=1.2pt] (axis cs:%s,%s)--(axis cs:%s,%s);' % (col, x0, y0, x1, y1)
def lab(x, y, t, anc='center'): return r'\node[anchor=%s,font=\scriptsize,inner sep=1pt] at (axis cs:%s,%s) {$%s$};' % (anc, x, y, t)
# campanes de Gauss N(0,1) amb regions ombrejades (com wFigs() d'app.js): ombra, marques de l'eix, etiqueta
NF = {'dens': ([(-0.4, 1.3)], [(-0.4, 'a'), (1.3, 'b')], 'y=f(x)'),
      'le': ([(-9, 0.8)], [(0, '0'), (0.8, 'z')], ''),
      'ge': ([(0.8, 9)], [(0, '0'), (0.8, 'z')], ''),
      'neg': ([(-9, -0.8)], [(-0.8, '-z'), (0, '0')], ''),
      'ngt': ([(-0.8, 9)], [(-0.8, '-z'), (0, '0')], ''),
      'ab': ([(-0.6, 1.4)], [(-0.6, 'a'), (1.4, 'b')], ''),
      'sym': ([(-1.2, 1.2)], [(-1.2, '-z'), (1.2, 'z')], '')}
def normfig(name, w=5.2, h=2.2):
    shade, ticks, label = NF[name]
    X0, X1 = -3.4, 3.4
    f = r'{exp(-\x*\x/2)}'
    s = r'\begin{tikzpicture}[x=%.4fcm,y=%.4fcm]' % (w / (X1 - X0), h)
    for a, b in shade:
        a, b = max(a, X0), min(b, X1)
        s += r'\fill[fmaccent,fill opacity=0.35] (%s,0) -- plot[domain=%s:%s,samples=70,smooth] (\x,%s) -- (%s,0) -- cycle;' % (a, a, b, f, b)
    s += r'\draw[fmmuted,line width=0.7pt] (%s,0) -- (%s,0);' % (X0, X1)
    s += r'\draw[fmgreen,line width=1.4pt] plot[domain=%s:%s,samples=120,smooth] (\x,%s);' % (X0, X1, f)
    for x, t in ticks:
        s += r'\draw[fmmuted,line width=0.7pt] (%s,0) -- (%s,-0.06) node[below,font=\footnotesize,inner sep=2pt,text=black] {$%s$};' % (x, x, t)
    if label: s += r'\node[anchor=north east,font=\footnotesize] at (%s,1.08) {$%s$};' % (X1, label)
    return s + r'\end{tikzpicture}'

# taules de la PAU (les mateixes que build.py de la unitat 10)
PS = [("0,01", 0.01), ("0,05", 0.05), ("0,10", 0.10), ("0,15", 0.15), ("0,20", 0.20), ("0,25", 0.25), ("0,30", 0.30),
      ("1/3", 1 / 3), ("0,35", 0.35), ("0,40", 0.40), ("0,45", 0.45), ("0,49", 0.49), ("0,50", 0.50)]
def c4(v): return ("%.4f" % v).replace(".", ",")
def Phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
assert c4(math.comb(9, 4) * (1 / 3) ** 4 * (2 / 3) ** 5) == "0,2048" and c4(Phi(1.96)) == "0,9750" and c4(Phi(2.33)) == "0,9901"
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

# ---------- 4. conversió a LaTeX ----------
UNI = {'→': r'$\to$', '∞': r'$\infty$', '≪': r'$\ll$', '≤': r'$\leq$', '≥': r'$\geq$', '−': '-', '○': r'$\circ$', '∄': r'$\nexists$',
       '✓': '', '✗': '', '✎': '', '✍': '', '🎓': '', '◉': '', '⚙': '', '…': r'\dots{}', '×': r'$\times$', '≠': r'$\neq$', '±': r'$\pm$', '↗': r'$\nearrow$', '↘': r'$\searrow$', '∩': r'$\cap$', '∪': r'$\cup$', '–': '--', '⇒': r'$\Rightarrow$'}
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
    if t == 'svg' and n.a.get('data-nf'): return r'{\centering %s\par}' % normfig(n.a['data-nf'], *((3.6, 1.55) if MINI[0] else (5.6, 2.4)))
    if t in ('input', 'select', 'button', 'svg', 'summary', 'label', 'option'): return ''
    if 'box' in c and 'lab' in c:  # taules interactives de la PAU: ací només una nota, la taula va a l'annex
        lbl = 'tbin' if 'binomial' in plain(n) else 'tnorm'
        return '\n\\begin{fmnote}%s\\end{fmnote}\n' % (T(r"\textbf{La taula de la PAU.} La taula completa, la mateixa que s'adjunta a l'examen, és a l'annex (pàgina \pageref{%s}).",
                                                          r"\textbf{La tabla de la PAU.} La tabla completa, la misma que se adjunta al examen, está en el anexo (página \pageref{%s}).") % lbl)
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
    if t == 'br': return '\\newline '
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
    if 'mini-figs' in c:  # sis campanes, tres per fila
        figs = [k for k in n.kids if not isinstance(k, str)]
        MINI[0] = True
        rows = [figs[i:i + 3] for i in range(0, len(figs), 3)]
        out = '\n\\begin{center}' + '\\\\[10pt]'.join(r'\hfill'.join(r'\begin{minipage}[t]{0.32\linewidth}\centering %s\end{minipage}' % text(k) for k in row) for row in rows) + '\\end{center}\n'
        MINI[0] = False
        return out
    if 'cmp' in c:
        cols = [k for k in n.kids if not isinstance(k, str)]
        box = r'\begin{tcolorbox}[enhanced,colback=fmsurface,colframe=fmmuted!35,arc=2.5mm,boxrule=0.6pt,left=2.5mm,right=2.5mm,top=1.5mm,bottom=1.5mm,before upper=\raggedright,equal height group=cmp%d]%s\end{tcolorbox}'
        CMP[0] += 1
        return '\n\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{0.488\linewidth}\vspace{0pt}%s\end{minipage}' % (box % (CMP[0], text(k).strip())) for k in cols) + '\\par\\medskip\n'
    if t == 'h4': return '{\\color{fmnavy}\\bfseries %s}\\par\n' % text(n).strip()
    if t == 'figure' and 'lfig' not in c:  # dins de fig4
        return text(n)
    if 'ttl' in c: return r'{\centering %s\par}' % text(n)
    if t == 'figcaption': return r'{\centering\footnotesize %s\par}' % text(n)
    if 'fig4' in c:
        figs = [k for k in n.kids if not isinstance(k, str)]
        w = 0.98 / min(len(figs), 4)
        return '\n\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{%.3f\linewidth}\centering %s\end{minipage}' % (w - 0.01, conv_fig4(k)) for k in figs) + '\\par\\medskip\n'
    if 'two' in c:
        cols = [k for k in n.kids if not isinstance(k, str)]
        out = []
        for i in range(0, len(cols), 2):
            pair = cols[i:i + 2]
            out.append('\\par\\noindent ' + '\\hfill'.join(r'\begin{minipage}[t]{0.48\linewidth}\vspace{0pt}\raggedright %s\end{minipage}' % (conv(k) if k.tag == 'figure' else text(k)).strip() for k in pair) + '\\par\\medskip\n')
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

CMP = [0]
MINI = [False]

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
            if 'pt' in k: v = r'\cellcolor{fmsurface}' + v
            line.append(v)
        out.append(' & '.join(line) + r'\\')
    IN_TABLE[0] = False
    m = max(len([c for c in r.kids if not isinstance(c, str)]) for r in rows)
    s = r'\begin{tabular}{l|%s}\toprule' % ('c' * (m - 1)) + '\n' + '\n'.join(o + (r'\midrule' if i < len(out) - 1 else '') for i, o in enumerate(out)) + '\n' + r'\bottomrule\end{tabular}'
    return '\n\\begin{center}\\small\\renewcommand{\\arraystretch}{1.6}%s\\end{center}\n' % s
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
    if 'sgn' in n.cls(): return conv_sgn(n)
    if 'ct' in n.cls(): return conv_ct(n)
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
    if any(not isinstance(k, str) and k.tag == 'thead' for k in n.kids):  # taules de text: columnes que fan salt de línia
        IN_TABLE[0] = True
        L = '>{\\raggedright\\arraybackslash}'
        C = '>{\\centering\\arraybackslash}X'
        s = r'\small\begin{tabularx}{\linewidth}{%sp{%s}%s}\toprule' % (L, '2.4cm' if m > 2 else '5.2cm', (L + 'X') * (m - 1) if m > 2 else C) + '\n'
        for r in rows:
            cs = [c for c in r.kids if not isinstance(c, str)]
            head = all(c.tag == 'th' for c in cs)
            s += ' & '.join((r'\textbf{%s}' if head else '%s') % text(c).strip() for c in cs) + r'\\' + (r'\midrule' if head else r'[3pt]') + '\n'
        IN_TABLE[0] = False
        return '\n\\begin{center}\\renewcommand{\\arraystretch}{1.7}%s\\bottomrule\\end{tabularx}\\end{center}\n' % s
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
    IN_TABLE[0] = True  # fórmules del títol com a $...$
    title = text(next(k for k in h2.kids if not isinstance(k, str) and k.tag == 'h2')).strip()
    IN_TABLE[0] = False
    return '\n\\Needspace{18\\baselineskip}\n\\section{%s}\n' % title + ''.join(conv(k) for k in n.kids)

latex = conv(ROOT)
latex = re.sub(r'\n{3,}', '\n\n', latex)
latex = re.sub(r'(?<!\\)\\\[', '\n\\[', latex)
latex = re.sub(r'(?<!\\)\\\]', '\\]\n', latex)
latex = re.sub(r'\\\]\s*([.,;])', r'\\,\1\\]', latex)  # el punt final va dins de la fórmula centrada
latex = re.sub(r'\n{3,}', '\n\n', latex)
# fórmules massa amples: en dues línies
m = re.search(r'\\\[P\(a\\leq X\\leq b\)=(\\text\{.*?\}f\\text\{.*?\}a\\text\{.*?\}b)=\\int_a\^b f\(x\)\\,dx\\\]', latex)
latex = latex.replace(m.group(0), r'\[\begin{aligned}P(a\leq X\leq b)&=\int_a^b f(x)\,dx\\&=%s\end{aligned}\]' % m.group(1))
a = r'\fmm{P(108\leq X\leq116)=P\!\left(\frac{108-100}{14}\leq Z\leq\frac{116-100}{14}\right)=P(0{,}57\leq Z\leq1{,}14)=0{,}8729-0{,}7157=0{,}1572}'
assert latex.count(a) == 1
latex = latex.replace(a, r'\[\begin{aligned}P(108\leq X\leq116)&=P\!\left(\frac{108-100}{14}\leq Z\leq\frac{116-100}{14}\right)=P(0{,}57\leq Z\leq1{,}14)\\&=0{,}8729-0{,}7157=0{,}1572\end{aligned}\]')

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
\usepackage{multirow}
\usepackage{needspace}
\usepackage[most]{tcolorbox}
\usepackage{titlesec}
\usepackage[hidelinks,pdftitle={Apunts de teoria. Unitat 10: Distribució binomial i normal. 2n de Batxillerat CCSS},pdfsubject={Matemàtiques Aplicades a les Ciències Socials II},pdfkeywords={variable aleatòria, funció de probabilitat, esperança, distribució binomial, nombre combinatori, distribució normal, campana de Gauss, normal típica, tipificació, aproximació de la binomial per la normal, correcció de continuïtat}]{hyperref}

% colors de la web (FentMates, bloc de probabilitat: morat; es manté el nom fmgreen dels apunts anteriors)
\definecolor{fmnavy}{HTML}{1B2748}
\definecolor{fmgreen}{HTML}{684E88}
\definecolor{fmgreenl}{HTML}{8064A1}
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
\renewcommand{\thesection}{10.\arabic{section}}
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
% dibuix de la targeta de la unitat a la web (illustrations.js, «normal»), en blanc
\newcommand{\fmcard}{\begin{tikzpicture}[x=0.058cm,y=-0.058cm,white,line width=4pt,line cap=round,line join=round]
  \draw[line width=3pt,opacity=0.7] (10,104)--(230,104);
  \begin{scope}\clip (14,104)--(14,103) .. controls (50,101) and (70,92) .. (88,64) .. controls (102,40) and (112,22) .. (120,22) .. controls (128,22) and (138,40) .. (152,64) .. controls (170,92) and (190,101) .. (226,103)--(226,104)--cycle;
    \fill[fill opacity=0.2] (134,0) rectangle (196,104);\end{scope}
  \draw (14,103) .. controls (50,101) and (70,92) .. (88,64) .. controls (102,40) and (112,22) .. (120,22) .. controls (128,22) and (138,40) .. (152,64) .. controls (170,92) and (190,101) .. (226,103);
  \draw[line width=3pt,dash pattern=on 6pt off 7pt] (120,22)--(120,104) (134,34)--(134,104);
  \fill[fill opacity=0.35] (20,88) rectangle (30,104) (32,74) rectangle (42,104) (44,66) rectangle (54,104) (56,78) rectangle (66,104);
  \node[anchor=base west,inner sep=0pt,font=\fontsize{22}{22}\selectfont\itshape] at (101,14) {N(\(\mu\),\(\sigma\))};
  \node[anchor=base west,inner sep=0pt,font=\fontsize{19}{19}\selectfont\itshape] at (20,60) {B(n,p)};
\end{tikzpicture}}
\newcommand{\fmbrand}{\raisebox{-0.25\height}{\includegraphics[height=0.5cm]{logo-fentmates.pdf}}}

% capçalera i peu
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\fmbrand}
\fancyhead[R]{\small\color{fmmuted}2n Batxillerat CCSS · Unitat 10: Distribució binomial i normal}
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
    \node[anchor=north west,inner sep=0pt,opacity=0.15] at ([xshift=6.6cm,yshift=-1.75cm]current page.north west) {\fmcard};
  \end{scope}
  \node[anchor=north west,inner sep=0pt] at ([xshift=1.5cm,yshift=-1.1cm]current page.north west) {\tcbox[colback=white,colframe=white,arc=2.5mm,boxsep=0pt,left=7pt,right=7pt,top=5pt,bottom=5pt]{\includegraphics[height=0.75cm]{logo-fentmates.pdf}}};
\end{tikzpicture}
\vspace*{0.55cm}
\tcbox[colback=white!15!fmgreen,colframe=white!15!fmgreen,arc=2.5mm,boxsep=0pt,left=6pt,right=6pt,top=3pt,bottom=3pt]{\color{white}\small\bfseries Apunts de teoria · 2n Batxillerat CCSS II}

\vspace{4pt}
{\raggedright\color{white}\fontsize{25}{30}\selectfont\bfseries{\color{fmyellow}Unitat 10} · Distribució binomial i normal\par}
\vspace{6pt}
\begin{minipage}{\linewidth}\color{white!88!fmgreen}\small HERO\end{minipage}
\vspace{0.7cm}

\begin{tcolorbox}[colback=fmsurface,colframe=fmsurface,arc=3mm,left=4mm,right=4mm,top=2mm,bottom=2mm]
\small\textbf{Índex}\par\smallskip
\begin{minipage}[t]{0.42\linewidth}\small TOC1\end{minipage}\hfill\begin{minipage}[t]{0.56\linewidth}\small TOC2\end{minipage}
\end{tcolorbox}
'''

secs = re.findall(r'\\section\{(.*?)\}\n', latex)
assert len(tocnames) == len(secs) == 8, (len(tocnames), len(secs))
toc = [r'\mbox{\hyperlink{sec%d}{\textbf{\color{fmgreen}10.%d}\ \ %s}}\\[3pt]' % (i + 1, i + 1, esc(tocnames[i])) for i in range(len(secs))]
half = (len(toc) + 1) // 2
toc.append(r'\mbox{\hyperlink{annex}{\textbf{\color{fmgreen}%s}\ \ %s}}\\[3pt]' % (T('Annex', 'Anexo'), T('Taules de la PAU', 'Tablas de la PAU')))
ANNEX = r'''
\clearpage
\hypertarget{annex}{}\phantomsection
{\color{fmnavy}\Large\bfseries\colorbox{fmdef}{\color{white}\strut\ %s\ }\hspace{0.6em}%s\par}\vspace{2pt}{\color{fmdef}\titlerule[1.2pt]}
\addcontentsline{toc}{section}{%s}
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
''' % (T('Annex', 'Anexo'), T('Taules de la PAU', 'Tablas de la PAU'), T('Annex. Taules de la PAU', 'Anexo. Tablas de la PAU'),
       T('Taula de la distribució binomial', 'Tabla de la distribución binomial'),
       T(r"Dona \fmm{P[X=x]=\binom nx\,p^x(1-p)^{n-x}} per a \fmm{n=2,\dots,9}.\newline Si \fmm{p\gt0{,}5}, compta els fracassos: \fmm{Y=n-X\sim B(n,1-p)} (apartat 10.3).",
         r"Da \fmm{P[X=x]=\binom nx\,p^x(1-p)^{n-x}} para \fmm{n=2,\dots,9}.\newline Si \fmm{p\gt0{,}5}, cuenta los fracasos: \fmm{Y=n-X\sim B(n,1-p)} (apartado 10.3)."),
       taula_binomial(),
       T('Taula de la distribució normal \\(N(0,1)\\)', 'Tabla de la distribución normal \\(N(0,1)\\)').replace('\\(', '$').replace('\\)', '$'),
       T(r"Dona \fmm{F(z)=P(Z\leq z)}, l'àrea a l'esquerra de \fmm{z}. La fila dona les unitats i les dècimes de \fmm{z}; la columna, les centèsimes (apartat 10.6).",
         r"Da \fmm{F(z)=P(Z\leq z)}, el área a la izquierda de \fmm{z}. La fila da las unidades y las décimas de \fmm{z}; la columna, las centésimas (apartado 10.6)."),
       taula_normal())
k = [0]
def anchor(m):
    k[0] += 1
    return '\\section{%s}\\hypertarget{sec%d}{}\n' % (m.group(1), k[0])
latex = re.sub(r'\\section\{(.*?)\}\n', anchor, latex)
hero_tex = esc(hero.replace(T(' i eines interactives:', ' y herramientas interactivas:'), ':'))
title = TITLE.replace('HERO', hero_tex).replace('TOC1', '\n'.join(toc[:half])).replace('TOC2', '\n'.join(toc[half:]))
# retocs de l'autor després de revisar el PDF en valencià (22/11/2026)
def retoc(va, es, nva, nes):
    global latex
    a, b = (es, nes) if ES else (va, nva)
    assert latex.count(a) == 1, a
    latex = latex.replace(a, b)
retoc(" d'aquestes maneres. Recorda:", " de esas maneras. Recuerda:", " d'aquestes maneres. \\\\\nRecorda:", " de esas maneras. \\\\\nRecuerda:")
for _ in range(2):
    a, b = (("se adjunta al examen, está en el anexo", "se adjunta al examen de selectividad, se encuentra en el anexo") if ES else
            ("s'adjunta a l'examen, és a l'annex", "s'adjunta a l'examen de selectivitat, es troba a l'annex"))
    latex = latex.replace(a, b, 1)
doc = PRE + title + latex + ANNEX + '\n\\end{document}\n'
if ES:
    for a, b in [(r'\usepackage[catalan]{babel}', r'\usepackage[spanish,es-minimal,es-noshorthands]{babel}'),
                 ("pdftitle={Apunts de teoria. Unitat 10: Distribució binomial i normal. 2n de Batxillerat CCSS}", 'pdftitle={Apuntes de teoría. Unidad 10: Distribución binomial y normal. 2.º de Bachillerato CCSS}'),
                 ('pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}', 'pdfsubject={Matemáticas Aplicadas a las Ciencias Sociales II}'),
                 ('pdfkeywords={variable aleatòria, funció de probabilitat, esperança, distribució binomial, nombre combinatori, distribució normal, campana de Gauss, normal típica, tipificació, aproximació de la binomial per la normal, correcció de continuïtat}', 'pdfkeywords={variable aleatoria, función de probabilidad, esperanza, distribución binomial, número combinatorio, distribución normal, campana de Gauss, normal tipificada, tipificación, aproximación de la binomial por la normal, corrección de continuidad}'),
                 ('2n Batxillerat CCSS · Unitat 10: Distribució binomial i normal}', '2.º Bachillerato CCSS · Unidad 10: Distribución binomial y normal}'),
                 ('Apunts de teoria · 2n Batxillerat CCSS II}', 'Apuntes de teoría · 2.º Bachillerato CCSS II}'),
                 (r"{\color{fmyellow}Unitat 10} · Distribució binomial i normal\par}", r"{\color{fmyellow}Unidad 10} · Distribución binomial y normal\par}"),
                 (r'\textbf{Índex}', r'\textbf{Índice}')]:
        assert doc.count(a) == 1, a
        doc = doc.replace(a, b)
    # amb el castellà de babel, les metadades dins de les opcions de hyperref fan petar pdflatex: van a \hypersetup
    m = re.search(r'\\usepackage\[hidelinks,(.*)\]\{hyperref\}\n', doc)
    doc = doc.replace(m.group(0), '\\usepackage[hidelinks]{hyperref}\n\\hypersetup{%s}\n' % m.group(1))
open(os.path.join(HERE, 't10-apunts-teoria-es.tex' if ES else 't10-apunts-teoria.tex'), 'w', encoding='utf-8').write(doc)
print(len(secs), 'apartats,', len(doc), 'caràcters')
