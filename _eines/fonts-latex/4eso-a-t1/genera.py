# Genera t1-fitxa-exercicis.tex i t1-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 1: Nombres naturals, enters i fraccionaris).
# Els exercicis (en valencià i castellà) són a exercicis.py, que també calcula i comprova les solucions.
# La versió en castellà la fa genera-es.py a partir de la mateixa llista (amb lang='es').
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
sys.path.insert(0, HERE)
from exercicis import seccions

TITOL = {'va': 'Nombres naturals, enters i fraccionaris', 'es': 'Números naturales, enteros y fraccionarios'}
KW = {'va': 'nombres naturals, operacions combinades, potències, arrels, nombres enters, valor absolut, fraccions, fraccions equivalents, simplificació, amplificació, problemes amb fraccions, propietats de les potències',
      'es': 'números naturales, operaciones combinadas, potencias, raíces, números enteros, valor absoluto, fracciones, fracciones equivalentes, simplificación, amplificación, problemas con fracciones, propiedades de las potencias'}

def preambul(lang):
    pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
    pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
    pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: 'pdfkeywords={%s}' % KW['va'], pre)
    pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques A 4t ESO}')
    pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
    if lang == 'es': pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
    return pre

def tidy(t):
    """Valor absolut amb \\lvert…\\rvert i signe menys unari després d'un espai o d'una coma (−1 i no − 1)."""
    t = re.sub(r'\|([^|$]+)\|', r'\\lvert \1\\rvert ', t)
    return re.sub(r'(\\ |\\qquad |\\quad |,)-(\d+)', r'\1{-\2}', t)

def build(sol, lang='va'):
    es = lang == 'es'
    S = seccions(lang)
    pre = preambul(lang)
    if es:
        from castella import preambul as pre_es, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = pre_es(pre, pdftitle='%s de la unidad 1: %s' % (t, TITOL['es']), capcalera='%s · Unidad 1: %s' % (t, TITOL['es']), pdfkeywords=KW['es'], curs='4eso-a')
        a = r'\textsuperscript{o} ESO}' + '\n'
        assert p.count(a) == 1
        p = p.replace(a, r'\textsuperscript{o} ESO A}' + '\n')   # «4º ESO A» a la capçalera de les pàgines
        cap = assignatura('4eso-a') + '{' + ('Soluciones de la ficha · Unidad 1' if sol else 'Ficha de ejercicios · Unidad 1') + '}{\\raggedright ' + TITOL['es'] + '}\n'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                        "pdftitle={%s de la unitat 1: %s. 4t d'ESO Matemàtiques A}" % (t, TITOL['va']))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 1: %s · 4t ESO A" % (t, TITOL['va']))
        assert 'fraccionaris · 4t ESO A' in p and 'unitat 1: Nombres' in p
        cap = '\\capcalera{Matemàtiques A}{4t ESO}{' + ('Solucions de la fitxa · Unitat 1' if sol else "Fitxa d'exercicis · Unitat 1") + '}{\\raggedright ' + TITOL['va'] + '}\n'
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\ifmmode\\boxed{#1}\\else\\fbox{#1}\\fi}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{4eso-a}

\begin{document}
\thispagestyle{primera}

''' + cap)
    if not sol:
        out.append('\\vspace{10pt}\n' + ('Nombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n' if es else
                   'Nom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n'))
    if es:
        intro = (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad." if sol else
                 r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Haz los cálculos sin calculadora.")
    else:
        intro = (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat." if sol else
                 r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Fes els càlculs sense calculadora.")
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + intro + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, tidy(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' +
                   ('¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.' if es else
                    'Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.') + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't1-fitxa-%s%s.tex' % ('solucions' if sol else 'exercicis', '-es' if es else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

if __name__ == '__main__':
    n = build(False); build(True)
    print(n, 'exercicis')
