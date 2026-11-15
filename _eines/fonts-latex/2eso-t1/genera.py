# Genera t1-fitxa-exercicis.tex i t1-fitxa-solucions.tex (2n ESO, Unitat 1: Nombres naturals i enters).
# Els exercicis (en valencià i castellà) són a exercicis.py, que també calcula i comprova les solucions.
# La versió en castellà la fa genera-es.py a partir de la mateixa llista.
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exercicis import seccions
S = seccions('va')

pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={nombres naturals, divisió entera, múltiples, divisors, nombres primers, mcm, MCD, nombres enters, operacions combinades, potències, arrels}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% recta numèrica entera: \rectabuida{min}{max} i \recta{min}{max}{punts}
\newcommand{\rectabase}[2]{\draw[latex-latex,muted] (#1-0.8,0)--(#2+0.8,0);
  \foreach \i in {#1,...,#2}{\draw[muted] (\i,0.12)--(\i,-0.12) node[below=-1pt,font=\scriptsize,text=muted]{$\i$};}}
\newcommand{\rectabuida}[2]{\begin{tikzpicture}[x=0.78cm,baseline=0]\rectabase{#1}{#2}\end{tikzpicture}}
\newcommand{\recta}[3]{\begin{tikzpicture}[x=0.78cm,baseline=0]\rectabase{#1}{#2}
  \foreach \p in {#3}{\fill[accent] (\p,0) circle (0.11) node[above=1pt,font=\small\bfseries,text=navy]{$\p$};}\end{tikzpicture}}
'''

def tidy(t):
    """Valor absolut amb \lvert…\rvert i signe menys unari després d'un espai o d'una coma (−1 i no − 1)."""
    t = re.sub(r'\|([^|$]+)\|', r'\\lvert \1\\rvert ', t)
    return re.sub(r'(\\ |\\qquad |\\quad |,)-(\d+)', r'\1{-\2}', t)

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 1: Nombres naturals i enters. 2n d'ESO}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 1: Nombres naturals i enters · 2n d'ESO" % t)
    assert 'Nombres naturals i enters · 2n' in p and 'unitat 1: Nombres' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\ifmmode\\boxed{#1}\\else\\fbox{#1}\\fi}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{2n ESO}{''' + ('Solucions de la fitxa · Unitat 1' if sol else "Fitxa d'exercicis · Unitat 1") + r'''}{Nombres naturals i enters}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Fes els càlculs sense calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, tidy(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't1-fitxa-solucions.tex' if sol else 't1-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
