# Fitxa de repàs del Global de Programació lineal (2n Batxillerat CCSS) en PDF.
# Són els 4 problemes de la prova model del web (materials/2batx-ccss/global-pl-prova-model1.html),
# amb format de fitxa d'exercicis de repàs: sense puntuació, cronòmetre ni criteris, amb recordatoris
# i, al final, les solucions.
# Reutilitza les funcions de càlcul exacte i les gràfiques TikZ de ../2batx-ccss-t3/genera.py, i les dades
# (vèrtexs i òptims ja comprovats) de _eines/examens/2batx-global-pl/probs.py.
# Ús: python3 genera.py && pdflatex global-pl-repas.tex (dues vegades)
import os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
T3 = os.path.join(HERE, '..', '2batx-ccss-t3')

# funcions de la fitxa de la unitat 3 (fins a les dades dels seus exercicis)
src = open(os.path.join(T3, 'genera.py'), encoding='utf-8').read()
cut = src.index('# ---------- dades de les gràfiques i comprovacions ----------')
exec(compile(src[:cut], 'genera-t3', 'exec'))
a, b = src.index('def cell('), src.index('S = []  #')   # taules de valors
exec(compile(src[a:b], 'genera-t3-taules', 'exec'))

# dades i comprovacions de la prova del web
sys.path.insert(0, os.path.join(HERE, '..', '..', 'examens', '2batx-global-pl'))
import probs, lp  # noqa: E402
probs.run_checks()

def cons(key):
    return [C(a, b, op, c) for a, b, op, c in probs.P[key]['cons']]
def V(key):
    return [(fr(x), fr(y)) for x, y in probs.P[key]['verts']]
for k in ('m1', 'm2', 'm3', 'm4', 'm4b'):   # el solucionador de t3 dona els mateixos vèrtexs
    assert sorted(verts(cons(k))[0]) == sorted(V(k)), k

def P(k, n):
    return dict(zip(probs.P[k]['names'], V(k)))[n]
def taula2(key, fexpr, p, q, best, fname='f'):
    vs = V(key)
    return avalua(cons(key), p, q, vs, fname, fexpr, [P(key, b) for b in best])
def lletres(tikz, key):
    """Afegeix el nom (sense coordenades) dels vèrtexs a una figura feta amb labels=False."""
    nodes = ''
    vs = V(key)
    cx = sum(float(v[0]) for v in vs) / len(vs); cy = sum(float(v[1]) for v in vs) / len(vs)
    for n, v in zip(probs.P[key]['names'], vs):
        x, y = float(v[0]), float(v[1])
        nodes += r'\filldraw[fill=white,draw=navy] (%.3f,%.3f) circle (1.6pt);' % (x, y)
        nodes += r'\node[font=\scriptsize\bfseries,text=navy] at ($(%.3f,%.3f)+(%.1f:0.32cm)$) {%s};' % (
            x, y, math.degrees(math.atan2(y - cy, x - cx)), n)
    return tikz.replace(r'\end{tikzpicture}', nodes + r'\end{tikzpicture}')
def centre(s): return r'\begin{center}' + s + r'\end{center}'

# =====================================================================
# Enunciats i solucions
# =====================================================================
S = []

S.append(("Regió factible, optimització i infinites solucions", [(
 r"Es considera la regió del pla determinada pel sistema d'inequacions"
 + dm(r"-x+y\leq 3,\qquad x+2y\leq 12,\qquad 2x-y\leq 9,\qquad y\geq -1.")
 + tasks(1, [r"Representa gràficament la regió i calcula'n els vèrtexs.",
             r"Justifica si els punts $P(0,4)$ i $Q(3,2)$ pertanyen a la regió.",
             r"Determina el valor màxim i el valor mínim de $f(x,y)=3x+2y$ en la regió i els punts on s'assoleixen.",
             r"Es considera la funció $g(x,y)=kx+2y$, amb $k\in\mathbb{R}$. Troba els valors de $k$ perquè el \textbf{màxim} de $g$ en la regió s'assolisca en tots els punts d'un costat. Per a cada valor, indica el costat i el valor màxim."])
 + recorda(r"Si les rectes de nivell de la funció objectiu són paral·leles a un costat de la regió, l'òptim pot assolir-se en tots els punts d'aquest costat: hi ha infinites solucions."),
 # solució
 r"\textbf{a)} Amb el punt de prova $(0,0)$ es compleixen totes les inequacions: la regió és el costat de cada recta on queda l'origen."
 + dm(sist(r"-x+y&=3", r"y&=-1") + r"\Rightarrow A(-4,-1)\qquad" + sist(r"y&=-1", r"2x-y&=9") + r"\Rightarrow B(4,-1)")
 + dm(sist(r"2x-y&=9", r"x+2y&=12") + r"\Rightarrow C(6,3)\qquad" + sist(r"x+2y&=12", r"-x+y&=3") + r"\Rightarrow D(2,5)")
 + centre(fig(cons('m1'), (-5, 8, -2, 7), w=6.2))
 + r"\textbf{b)} $P(0,4)$: $-0+4=4\not\leq3$, \rest{no} és de la regió. \quad $Q(3,2)$: $-1\leq3$, $7\leq12$, $4\leq9$, $2\geq-1$: \rest{sí} que hi és.\par "
 + r"\textbf{c)} La regió és fitada; avaluem $f$ en els vèrtexs:"
 + taula2('m1', '3x+2y', 3, 2, ['C', 'A'])
 + r"Màxim: $\res{f(6,3)=24}$. \quad Mínim: $\res{f(-4,-1)=-14}$.\par "
 + r"\textbf{d)} Les rectes de nivell $kx+2y=c$ tenen pendent $-\frac k2$: han de ser paral·leles a un costat."
 + r"\begin{itemize}\setlength\itemsep{1pt}"
 + r"\item Costat $CD$ ($x+2y=12$, pendent $-\frac12$): $k=1$. $g(A)=-6$, $g(B)=2$, $g(C)=g(D)=12$: \res{\text{màxim } 12 \text{ en tot el segment } CD}."
 + r"\item Costat $DA$ ($-x+y=3$, pendent $1$): $k=-2$. $g(A)=g(D)=6$, $g(B)=-10$, $g(C)=-6$: \res{\text{màxim } 6 \text{ en tot el segment } DA}."
 + r"\item Costats $AB$ ($k=0$) i $BC$ ($k=-4$): donen el \emph{mínim}, no el màxim. No serveixen."
 + r"\end{itemize}"
 + centre(fig(cons('m1'), (-5, 8, -2, 7), w=5.4, level=(1, 2, 12), seg=(P('m1', 'C'), P('m1', 'D')), opt=[P('m1', 'C'), P('m1', 'D')]))
)]))

S.append(("Problema de maximitzar amb solucions enteres", [(
 r"Una cooperativa citrícola prepara dos tipus de caixes de regal. Cada caixa del tipus A porta 2~kg de taronges i 1~kg de mandarines, "
 r"i cada caixa del tipus B porta 1~kg de taronges i 2~kg de mandarines. La cooperativa disposa de 100~kg de taronges i de 80~kg de mandarines. "
 r"Per a atendre les comandes ha de preparar, com a mínim, 20 caixes en total, i almenys 10 han de ser del tipus B. "
 r"Per cada caixa del tipus A guanya 5~€ i per cada caixa del tipus B, 4~€."
 + tasks(1, [r"Planteja el problema de programació lineal que permet maximitzar el benefici: defineix les variables, la funció objectiu i les restriccions.",
             r"Representa la regió factible i calcula'n els vèrtexs.",
             r"Quantes caixes de cada tipus ha de preparar per a obtindre el benefici màxim? Quin és aquest benefici?",
             r"Si el benefici passara a ser de 6~€ per caixa A i de 3~€ per caixa B, de quantes maneres es podria obtindre el benefici màxim? Indica-les totes i el benefici."])
 + recorda(r"Si les variables compten objectes (caixes, persones…), les solucions han de ser nombres enters: quan l'òptim és tot un segment, busca'n els punts amb coordenades enteres."),
 r"\textbf{a)} $x$ = caixes A, $y$ = caixes B. Maximitzar $B(x,y)=5x+4y$ subjecte a:"
 + dm(sist(r"2x+y&\leq100 \quad\text{(taronges)}", r"x+2y&\leq80 \quad\text{(mandarines)}", r"x+y&\geq20", r"y&\geq10", r"x&\geq0"))
 + r"\textbf{b)} Vèrtexs: $A(0,20)$, $B(10,10)$, $C(45,10)$, $D(40,20)$ (tall de $2x+y=100$ i $x+2y=80$), $E(0,40)$."
 + centre(fig(cons('m2'), (0, 60, 0, 50), w=6.2, hmax=5))
 + r"\textbf{c)}" + taula2('m2', '5x+4y', 5, 4, ['D'], 'B')
 + r"\res{40 \text{ caixes A i } 20 \text{ caixes B}}, amb un benefici màxim de \res{280\ \text{€}}.\par "
 + r"\textbf{d)} Ara $B=6x+3y=3(2x+y)$, paral·lela a $2x+y=100$:"
 + taula2('m2', '6x+3y', 6, 3, ['C', 'D'], 'B')
 + r"El màxim, 300~€, s'assoleix en tot el segment $CD$. Les solucions enteres són els punts de $2x+y=100$ amb $40\leq x\leq45$:"
 + dm(r"(40,20),\ (41,18),\ (42,16),\ (43,14),\ (44,12),\ (45,10)")
 + r"Hi ha \res{6 \text{ maneres}} d'obtindre el benefici màxim de \res{300\ \text{€}}."
)]))

S.append(("Problema de minimitzar en una regió no fitada", [(
 r"Un ramader alimenta el seu bestiar amb dos pinsos, P1 i P2. Cada sac de P1 aporta 3 unitats de proteïnes, 1 de fibra i 1 de minerals; "
 r"cada sac de P2 aporta 1 unitat de proteïnes, 1 de fibra i 3 de minerals. Cada setmana el bestiar necessita, com a mínim, 15 unitats de proteïnes, "
 r"9 de fibra i 15 de minerals. Un sac de P1 costa 40~€ i un sac de P2, 30~€."
 + tasks(1, [r"Planteja el problema que permet trobar quants sacs de cada pinso ha de comprar setmanalment per a cobrir les necessitats amb el cost mínim.",
             r"Representa la regió factible i calcula'n els vèrtexs. És una regió fitada?",
             r"Resol el problema: quants sacs de cada tipus ha de comprar i quin és el cost mínim?",
             r"Té sentit preguntar-se pel cost màxim? Raona-ho. Si el ramader comprara 4 sacs de cada pinso, cobriria les necessitats?"])
 + recorda(r"En una regió no fitada l'òptim pot no existir. Si els coeficients de la funció objectiu són positius i la regió s'estén cap amunt i cap a la dreta, hi ha mínim però no màxim."),
 r"\textbf{a)} $x$ = sacs de P1, $y$ = sacs de P2. Minimitzar $C(x,y)=40x+30y$ subjecte a:"
 + dm(sist(r"3x+y&\geq15 \quad\text{(proteïnes)}", r"x+y&\geq9 \quad\text{(fibra)}", r"x+3y&\geq15 \quad\text{(minerals)}", r"x\geq0,\ y&\geq0"))
 + r"\textbf{b)} Vèrtexs: $A(0,15)$, $B(3,6)$, $C(6,3)$, $D(15,0)$. La regió \rest{no és fitada}."
 + centre(fig(cons('m3'), (0, 18, 0, 17), w=5.6, level=(40, 30, 300), opt=[P('m3', 'B')]))
 + r"\textbf{c)}" + taula2('m3', '40x+30y', 40, 30, ['B'], 'C')
 + r"Com que la funció creix en allunyar-se de l'origen, el mínim existeix i és en un vèrtex (la recta de nivell $40x+30y=300$, discontínua, deixa tota la regió al costat de cost més gran): "
 + r"\res{3 \text{ sacs de P1 i } 6 \text{ de P2}}, amb un cost mínim de \res{300\ \text{€}}.\par "
 + r"\textbf{d)} \rest{No hi ha cost màxim}: la regió no és fitada i $40x+30y$ creix indefinidament. "
 + r"Amb $(4,4)$: proteïnes $16\geq15$, fibra $8\not\geq9$, minerals $16\geq15$: \rest{no} cobriria la fibra."
)]))

FIG4 = lletres(fig(cons('m4'), (-1, 9, -1, 7), w=4.6, hmax=3.6, labels=False), 'm4')
S.append(("Regió donada en un gràfic", [(
 r"La regió ombrejada és la regió factible d'un problema de programació lineal. Els vèrtexs tenen coordenades enteres."
 + centre(FIG4)
 + tasks(1, [r"Determina el sistema d'inequacions que defineix la regió.",
             r"Calcula el màxim i el mínim de $f(x,y)=2x+y$ en la regió i on s'assoleixen.",
             r"Estudia en quins punts de la regió assoleix el màxim i el mínim la funció $h(x,y)=x+2y$. Alguna de les dues solucions és única?",
             r"S'afegeix la restricció $x\leq5$. Dibuixa la nova regió, calcula els vèrtexs nous i troba el nou màxim de $f$."])
 + recorda(r"Per a escriure la inequació d'un costat, calcula la recta que passa per dos vèrtexs i tria el sentit de la desigualtat amb un punt de dins de la regió."),
 r"\textbf{a)} Vèrtexs: $A(0,2)$, $B(4,0)$, $C(7,3)$, $D(4,6)$, $E(0,6)$. Amb el punt interior $(2,3)$:"
 + dm(r"AB:\ x+2y\geq4,\quad BC:\ x-y\leq4,\quad CD:\ x+y\leq10,\quad DE:\ y\leq6,\quad EA:\ x\geq0")
 + r"\textbf{b)} i \textbf{c)}"
 + r'\begin{center}\small\begin{tabular}{ccc}\hline Vèrtex & $f=2x+y$ & $h=x+2y$\\\hline '
 + ''.join(r'$%s$ & $%s$ & $%s$\\' % (n + pt(v), tn(2 * v[0] + v[1]), tn(v[0] + 2 * v[1])) for n, v in zip('ABCDE', V('m4')))
 + r'\hline\end{tabular}\end{center}'
 + r"Màxim de $f$: $\res{17}$ en $C(7,3)$. Mínim de $f$: $\res{2}$ en $A(0,2)$.\par "
 + r"Màxim de $h$: $\res{16}$ només en $D(4,6)$ (solució única). Mínim de $h$: $\res{4}$ en $A$ i en $B$: com que $h$ és paral·lela al costat $x+2y=4$, "
 + r"el mínim s'assoleix en \rest{tots els punts del segment $AB$} (infinites solucions)."
 + centre(fig(cons('m4'), (-1, 9, -1, 7), w=5.2, seg=(P('m4', 'A'), P('m4', 'B')), opt=[P('m4', 'D')]))
 + r"\textbf{d)} La recta $x=5$ retalla la punta $C$. Vèrtexs nous: $x=5$ amb $x-y=4\Rightarrow F(5,1)$; \ $x=5$ amb $x+y=10\Rightarrow G(5,5)$."
 + centre(fig(cons('m4b'), (-1, 9, -1, 7), w=5.2, opt=[P('m4b', 'G')]))
 + taula2('m4b', '2x+y', 2, 1, ['G'])
 + r"El nou màxim de $f$ és $\res{15}$, en $G(5,5)$."
)]))

# =====================================================================
pre = open(os.path.join(T3, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: "pdfkeywords={programació lineal, regió factible, vèrtexs, infinites solucions, regions no fitades, PAU, repàs}", pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
pre = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                  "pdftitle={Fitxa de repàs: Global de Programació lineal. 2n de Batxillerat CCSS}")
pre = pre.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "Fitxa de repàs · Global de Programació lineal · 2n Batxillerat CCSS")
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
pre = pre.replace(r'\usepackage{tikz}', r'\usepackage{tikz}' + '\n' + r'\usetikzlibrary{calc}')
assert 'Global de Programació lineal' in pre and 'estrelles{#1}}' not in pre and 'calc' in pre
pre += r'''
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

out = [pre, r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}
\newcommand{\res}[1]{\boxed{#1}}\newcommand{\rest}[1]{\fbox{#1}}
\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{2n Batx}{Fitxa de repàs · Global}{Programació lineal}

\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}

\vspace{8pt}
\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small Quatre problemes de repàs de tota la unitat 3, amb el nivell de la PAU: regions factibles i vèrtexs, optimització en regions fitades i no fitades, infinites solucions, solucions enteres, plantejament de problemes i lectura d'una regió a partir d'un gràfic. Fes les gràfiques amb regle i paper quadriculat, justifica cada pas i, quan acabes, comprova-ho amb les solucions del final.
\end{tcolorbox}
''']
for i, (title, exs) in enumerate(S, 1):
    out.append('\n\\seccio{%d}{%s}\n\n' % (i, title))
    for q, s in exs:
        out.append('\\ex{1} %s\n\n' % q)
out.append(r'''
\newpage
\begin{tcolorbox}[colback=teal,colframe=teal,coltext=white,arc=2mm,boxrule=0pt,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
{\Large\bfseries\faCheckCircle\ \ Solucions}
\end{tcolorbox}
\setcounter{exer}{0}
''')
for i, (title, exs) in enumerate(S, 1):
    out.append('\n\\seccio{%d}{%s}\n\n' % (i, title))
    for q, s in exs:
        out.append('\\ex{1} %s\n\n' % s)
out.append('\n\\end{document}\n')
open(os.path.join(HERE, 'global-pl-repas.tex'), 'w', encoding='utf-8').write(''.join(out))
print('ok: 4 problemes;', lp.CHECKS[0], 'comprovacions')
