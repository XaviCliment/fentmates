# Eines comunes de les fitxes de 4t ESO Matemàtiques B (carpetes 4eso-b-tN): una sola llista d'exercicis genera la fitxa
# i les solucions. Cada exercici és (estrelles, enunciat, solució) i, com a les fitxes d'ESO, es mostren les estrelles.
# Inclou els intervals i la recta real de la fitxa de la unitat 1 de 1r Batx MI (aritmètica exacta amb fraccions),
# i CHK/ck/eq per a comprovar els resultats escrits a mà (eq compara numèricament dues expressions de sympy).
import os, re, math
from fractions import Fraction as F

INF = float('inf')

def tasks(n, items, start=None, gap=None):
    """gap: espai extra entre files (p. ex. '12pt') per a enunciats amb fraccions o sistemes"""
    o = (['start=%d' % start] if start else []) + (['after-item-skip=%s' % gap] if gap else [])
    opt = '[' + ','.join(o) + ']' if o else ''
    return '\\begin{tasks}%s(%d)\n' % (opt, n) + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def R(t): return r'$\res{' + t + '}$'
def Rm(t): return r'\res{' + t + '}'   # dins d'una fórmula que ja té $...$
def tn(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{%d}{%d}' % (abs(x.numerator), x.denominator)
def dec(x, k=3):
    """decimal amb coma (icomma), sense zeros sobrers"""
    s = ('%.*f' % (k, x)).rstrip('0').rstrip('.')
    return s.replace('.', ',').replace('-', '-')

CHK = []
def ck(x, y):
    CHK.append((x, y)); return x

def eq(a, b, subs=None):
    """comprova numèricament (amb sympy) que dues expressions són iguals"""
    import sympy as sp
    A, B = sp.sympify(a), sp.sympify(b)
    vals = subs or {}
    syms = (A.free_symbols | B.free_symbols)
    defaults = [1.37, 2.71, 0.83, 3.19, 1.91]
    for i, s in enumerate(sorted(syms, key=str)):
        vals.setdefault(s, defaults[i % len(defaults)])
    va, vb = complex(A.evalf(subs=vals)), complex(B.evalf(subs=vals))
    assert abs(va - vb) < 1e-9 * max(1, abs(va)), (a, b, va, vb)

def per(ent, ante, peri):
    """valor exacte de ent,ante(peri)"""
    if not peri: return F(int(ent + ante), 10 ** len(ante))
    full, part = int(ent + ante + peri), int(ent + ante)
    return F(full - part, int('9' * len(peri) + '0' * len(ante)))

# ---------- intervals: (a, tancat_a, b, tancat_b) ----------
def norm(L):
    L = sorted([I for I in L if I[0] < I[2] or (I[0] == I[2] and I[1] and I[3])], key=lambda I: (I[0], not I[1]))
    out = []
    for a, ac, b, bc in L:
        if out and (a < out[-1][2] or (a == out[-1][2] and (out[-1][3] or ac))):
            pa, pac, pb, pbc = out[-1]
            if b > pb: out[-1] = (pa, pac, b, bc)
            elif b == pb: out[-1] = (pa, pac, pb, pbc or bc)
        else: out.append((a, ac, b, bc))
    return out
def cap(S, T):
    r = []
    for a, ac, b, bc in S:
        for c, cc, d, dc in T:
            r.append((max(a, c), ac if a > c else cc if c > a else ac and cc, min(b, d), bc if b < d else dc if d < b else bc and dc))
    return norm(r)
def cup(S, T): return norm(S + T)
def P(s):
    """'[-3,2)U(5,inf)' -> conjunt"""
    out = []
    for p in s.split('U'):
        m = re.match(r'^([\[\(])([^,]+),([^,]+)([\]\)])$', p.strip())
        def num(t): return -INF if t == '-inf' else INF if t == 'inf' else F(t)
        out.append((num(m.group(2)), m.group(1) == '[', num(m.group(3)), m.group(4) == ']'))
    return norm(out)
def ivt(I):
    a, ac, b, bc = I
    if a == b: return r'\{%s\}' % tn(a)
    if a == -INF and b == INF: return r'\mathbb R'
    ta = r'-\infty' if a == -INF else tn(a)
    tb = r'+\infty' if b == INF else tn(b)
    return ('[' if ac else '(') + ta + ', ' + tb + (']' if bc else ')')
def st(S): return r'\cup'.join(ivt(I) for I in norm(S)) if norm(S) else r'\varnothing'

def recta(S, lo=None, hi=None):
    """dibuix TikZ d'un conjunt de la recta real"""
    S = norm(S)
    pts = [float(v) for I in S for v in (I[0], I[2]) if abs(v) != INF] or [0]
    if lo is None: lo = math.floor(min(pts)) - 1
    if hi is None: hi = math.ceil(max(pts)) + 1
    if hi - lo < 6: c = (hi + lo) / 2; lo, hi = math.floor(c - 3), math.ceil(c + 3)
    step = 2 if hi - lo > 14 else 1
    sc = min(0.42, 7.2 / (hi - lo + 1.4))
    o = [r'\begin{tikzpicture}[x=%.3fcm,baseline=-3pt]' % sc,
         r'\draw[-latex,muted] (%g,0)--(%g,0);' % (lo - 0.6, hi + 0.7)]
    v = math.ceil(lo / step) * step
    while v <= hi:
        o.append(r'\draw[muted] (%d,0.1)--(%d,-0.1) node[below=-1pt,font=\scriptsize,text=muted]{$%d$};' % (v, v, v)); v += step
    for a, ac, b, bc in S:
        xa = lo - 0.45 if a == -INF else float(a); xb = hi + 0.45 if b == INF else float(b)
        if a != b: o.append(r'\draw[accent,line width=2.6pt] (%g,0)--(%g,0);' % (xa, xb))
        if a == -INF: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xa - 0.3, xa + 0.1, xa + 0.1))
        if b == INF: o.append(r'\fill[accent] (%g,0)--(%g,0.17)--(%g,-0.17)--cycle;' % (xb + 0.3, xb - 0.1, xb - 0.1))
        for x, c, lab in ((a, ac, True), (b, bc, a != b)):
            if abs(x) == INF or not lab: continue
            o.append((r'\fill[accent] (%g,0) circle (2.3pt);' if c else r'\filldraw[fill=white,draw=accent,line width=1.1pt] (%g,0) circle (2.3pt);') % float(x))
            if F(x).denominator != 1: o.append(r'\node[above=1pt,font=\scriptsize,text=accent] at (%g,0) {$%s$};' % (float(x), tn(x)))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def RI(s, lo=None, hi=None):
    """solució d'interval: el conjunt emmarcat i la recta"""
    S = P(s) if isinstance(s, str) else s
    return R(st(S)) + r'\\[2pt]' + recta(S, lo, hi)

# ---------- generació dels dos .tex ----------
def check():
    for l, r in CHK:
        assert l == r, (l, r)

def build(here, num, titol, S, keywords, intro_ex, intro_sol, extra_pre='', lang='va'):
    """escriu tN-fitxa-exercicis.tex i tN-fitxa-solucions.tex (lang='es': tN-fitxa-exercicis-es.tex i tN-fitxa-solucions-es.tex,
    amb titol, keywords, intro_ex i intro_sol ja en castellà)"""
    es = lang == 'es'
    check()
    pre = open(os.path.join(here, 'preamble.tex'), encoding='utf-8').read()
    pre = pre.split('% ---------- recta real ----------')[0]
    pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: 'pdfkeywords={%s}' % keywords, pre)
    pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques B 4t ESO}')
    pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
    pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
    pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
    pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }' + '\n'
    pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
''' + extra_pre
    if es: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
    def sp_(t): return re.sub(r'\$[^$]*\$', lambda m: m.group(0).replace(', ', r',\, '), t)
    for sol in (False, True):
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        if es:
            from castella import preambul, assignatura
            t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
            p = preambul(pre, pdftitle='%s de la unidad %d: %s' % (t, num, titol), capcalera='%s · Unidad %d: %s' % (t, num, titol),
                         pdfkeywords=keywords, curs='4eso-b')
            a = r'\textsuperscript{o} ESO}' + '\n'
            assert p.count(a) == 1
            p = p.replace(a, r'\textsuperscript{o} ESO B}' + '\n')   # com a la versió valenciana: «4º ESO B» a la capçalera
        else:
          p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                        "pdftitle={%s de la unitat %d: %s. 4t d'ESO Matemàtiques B}" % (t, num, titol))
          p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat %d: %s · 4t ESO B" % (t, num, titol))
          assert ('Unitat %d' % num) in p and ('unitat %d' % num) in p
        out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
        out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{4eso-b}

\begin{document}
\thispagestyle{primera}

''' + (assignatura('4eso-b') + '{' + ('Soluciones de la ficha · Unidad %d' % num if sol else 'Ficha de ejercicios · Unidad %d' % num) if es else
       '\\capcalera{Matemàtiques B}{4t ESO}{' + ('Solucions de la fitxa · Unitat %d' % num if sol else "Fitxa d'exercicis · Unitat %d" % num)) + r'''}{\raggedright ''' + titol + r'''}
''')
        if not sol:
            if es: out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
            else: out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
        out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (intro_sol if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] " + intro_ex if es else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] " + intro_ex) + r'''
\end{tcolorbox}
''')
        for i, (title, exs) in enumerate(S, 1):
            out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
            for j, (st_, q, s) in enumerate(exs):
                out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, sp_(s if sol else q)))
        if not sol and es:
            out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
        elif not sol:
            out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.\\end{center}\n')
        out.append('\n\\end{document}\n')
        name = 't%d-fitxa-%s%s.tex' % (num, 'solucions' if sol else 'exercicis', '-es' if es else '')
        open(os.path.join(here, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    n = sum(len(x[1]) for x in S)
    print(n, 'ejercicios;' if es else 'exercicis;', len(CHK), 'comprobaciones' if es else 'comprovacions')
    return n
