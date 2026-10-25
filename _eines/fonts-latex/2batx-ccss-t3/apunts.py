# Genera t3-apunts.tex: versió imprimible dels apunts de la Unitat 3 (Programació lineal, 2n Batxillerat CCSS).
# Mateix contingut teòric que els apunts interactius (materials/2batx-ccss/t3-programacio-lineal.html), sense les eines
# interactives, amb exemples resolts i gràfiques on la web tenia una eina, i amb la capçalera 6 («Apunts web»).
# Disseny pensat per no deixar grans buits: les definicions i propietats són quadres curts que no es parteixen;
# els exemples i la pràctica porten una franja lateral i, si cal, continuen a la pàgina següent.
# Les gràfiques es calculen amb aritmètica exacta (../comu/pltikz.py) i CHK comprova tots els vèrtexs i òptims.
# Ús: python3 apunts.py && lualatex t3-apunts.tex (dues vegades)
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from pltikz import C, F, fr, tn, pt, fig, verts, optim

CHK = []
def reg(cons, expect):
    CHK.append(('v', cons, expect)); return cons
def opt(cons, p, q, goal, val, pts):
    CHK.append(('o', cons, p, q, goal, val, pts)); return ''
NN = [C(1, 0, '>=', 0), C(0, 1, '>=', 0)]
def costat(a, b, k=0.56): return r'\costat[%s]{%s}{%s}' % (k, a, b)
def sist(*rows): return r'\left\{\begin{aligned}' + r'\\'.join(rows) + r'\end{aligned}\right.'

# ---------- regions dels exemples ----------
RPENT = reg([C(1, 1, '<=', 6), C(0, 1, '<=', 4), C(1, 0, '<=', 5), C(1, 0, '>=', 1), C(0, 1, '>=', 0)], [(1, 0), (5, 0), (5, 1), (2, 4), (1, 4)])
RNAC = reg([C(1, 1, '>=', 4), C(1, 0, '>=', 1), C(0, 1, '>=', 0)], [(1, 3), (4, 0)])
RBUI = reg([C(1, 1, '<=', 2), C(1, 1, '>=', 5)] + NN, [])
RBIC = reg([C(1, 2, '<=', 80), C(3, 2, '<=', 120)] + NN, [(0, 0), (40, 0), (20, 30), (0, 40)])
RDIE = reg([C(3, 1, '>=', 12), C(1, 2, '>=', 9)] + NN, [(0, 12), (3, 3), (9, 0)])
RTRA = reg([C(1, 1, '<=', 50), C(1, 1, '>=', 30), C(1, 0, '>=', 0), C(1, 0, '<=', 30), C(0, 1, '>=', 0), C(0, 1, '<=', 40)], [(30, 0), (30, 20), (10, 40), (0, 40), (0, 30)])
RINV = reg([C(1, 1, '<=', 10), C(1, 0, '>=', 2), C(0, 1, '<=', 6), C(-2, 1, '<=', 0), C(0, 1, '>=', 0)], [(2, 0), (10, 0), (4, 6), (3, 6), (2, 4)])
RCOL = reg([C(2, 1, '<=', 16), C(1, 2, '<=', 14)] + NN, [(0, 0), (8, 0), (6, 4), (0, 7)])
RBUI2 = reg([C(1, 1, '<=', 3), C(2, 3, '>=', 12)] + NN, [])
RRAIG = reg([C(1, 0, '>=', 2), C(0, 1, '>=', 1)], [(2, 1)])
RENT = reg([C(4, 5, '>=', 20), C(1, 0, '<=', 4), C(0, 1, '<=', 5), C(1, 1, '<=', 5)] + NN, [(0, 4), (0, 5), (4, 1), (4, F(4, 5))])
opt(RBIC, 20, 15, 'max', 850, [(20, 30)]); opt(RBIC, 20, 15, 'min', 0, [(0, 0)])
opt(RDIE, 5, 3, 'min', 24, [(3, 3)]); opt(RTRA, 2, -2, 'min', -80, [(0, 40)]); opt(RINV, 50, 80, 'max', 680, [(4, 6)])
opt(RCOL, 30, 20, 'max', 260, [(6, 4)]); opt(RCOL, 40, 20, 'max', 320, [(6, 4), (8, 0)])
opt(RDIE, 1, 2, 'min', 9, [(3, 3), (9, 0)]); opt(RDIE, 1, 1, 'min', 6, [(3, 3)])
opt(RENT, 72, 108, 'min', F(1872, 5), [(4, F(4, 5))])
assert optim(RDIE, 5, 3, 'max') == (None, []) and optim(RDIE, 1, 1, 'max') == (None, [])
assert verts(RRAIG)[1] is False and optim(RRAIG, 0, 1, 'min') == (1, [(2, 1)])

def V(cons): return ',\\ '.join(pt(v) for v in sorted(verts(cons)[0]))

B = []  # cos del document
def add(s): B.append(s)

# =====================================================================
add(r'\seccio{3.1}{Inequacions lineals amb dues incògnites}')
add(r'''
\begin{defi}{Inequació lineal amb dues incògnites}
És una desigualtat que es pot escriure d'alguna d'aquestes formes:
\[ax+by<c\qquad ax+by\leq c\qquad ax+by>c\qquad ax+by\geq c\]
on $a$, $b$ i $c$ són nombres reals coneguts ($a$ i $b$ no nuls alhora) i $x$, $y$ són les incògnites.
\begin{itemize}
\item Una \textbf{solució} és un parell $(x_0,y_0)$ que, en substituir-lo, fa certa la desigualtat: és un \textbf{punt del pla}.
\item \textbf{Resoldre} la inequació és trobar \emph{totes} les solucions. N'hi ha infinites i les representem gràficament.
\end{itemize}
Per exemple, $(1,\,1)$ és solució de $2x+y\leq4$ perquè $2\cdot1+1=3\leq4$; en canvi, $(2,\,3)$ no ho és: $2\cdot2+3=7>4$.
\end{defi}
''')
FRONT = fig([C(1, 1, '<=', 3)], (-2, 5, -2, 5), w=3.6, labels=False, shade=False,
            extra=r'\node[font=\scriptsize,text=teal!70!black] at (0.3,0.6) {$x+y<3$};\node[font=\scriptsize,text=accent] at (3.2,3.3) {$x+y>3$};\node[font=\tiny,text=accent,rotate=-45] at (3.9,-1.25) {$x+y=3$};')
add(r'''
\begin{propi}{Recta frontera i semiplans}
''' + costat(r'''La recta $ax+by=c$, anomenada \textbf{recta frontera}, divideix el pla en dos \textbf{semiplans}: en tots els punts d'un es compleix $ax+by<c$ i en tots els de l'altre, $ax+by>c$.

Per tant, \textbf{la solució d'una inequació lineal amb dues incògnites és sempre un semipla}:
\begin{itemize}
\item Desigualtat \textbf{no estricta} ($\leq$, $\geq$): la recta és part de la solució i la dibuixem \textbf{contínua} (semipla \emph{tancat}).
\item Desigualtat \textbf{estricta} ($<$, $>$): la recta no és part de la solució i la dibuixem \textbf{discontínua} (semipla \emph{obert}).
\end{itemize}''', FRONT, 0.64) + r'''
\end{propi}
''')
add(r'''
\begin{defi}{Resolució gràfica d'una inequació}
\begin{enumerate}
\item \textbf{Dibuixem la recta frontera} $ax+by=c$ amb dos punts (normalment, els talls amb els eixos: $x=0$ i $y=0$). Contínua si és $\leq,\geq$; discontínua si és $<,>$.
\item \textbf{Triem un punt de prova} que no siga de la recta. Si la recta no passa per l'origen, el més còmode és $(0,\,0)$.
\item \textbf{Substituïm} el punt en la inequació. Si la compleix, la solució és el semipla que el \underline{conté}; si no, el semipla \underline{contrari}.
\item \textbf{Ombregem} el semipla solució.
\end{enumerate}
\end{defi}
\begin{nota}\textbf{Truc:} si aïllem la $y$ i queda $y\geq mx+n$, la solució és el semipla de \textbf{damunt} de la recta; si queda $y\leq mx+n$, el de \textbf{davall}. Compte: si en aïllar dividim per un nombre negatiu, la desigualtat canvia de sentit.\end{nota}
''')
add(r'''
\begin{exemple}{Exemples de resolució gràfica}
''' + costat(r'''\textbf{a)} $2x+y\leq4$. \ Recta frontera $2x+y=4$, contínua: $x=0\Rightarrow y=4$; \ $y=0\Rightarrow x=2$. Passa per $(0,\,4)$ i $(2,\,0)$.

Punt de prova $(0,\,0)$: $2\cdot0+0=0\leq4$ \checkmark. La solució és el semipla que conté l'origen.''',
            fig([C(2, 1, '<=', 4)], (-2, 5, -2, 5), w=3.3, labels=False, test=((0, 0), True))) + r'''
\medskip
''' + costat(r'''\textbf{b)} $x-2y>2$. \ Recta frontera $x-2y=2$, discontínua, per $(0,\,-1)$ i $(2,\,0)$.

Punt de prova $(0,\,0)$: $0>2$ \texttimes. La solució és el semipla que \textbf{no} conté l'origen, sense la recta.''',
            fig([C(1, -2, '>', 2)], (-2, 6, -4, 3), w=3.3, labels=False, test=((0, 0), False))) + r'''
\medskip
''' + costat(r'''\textbf{c)} $y\geq2x$. \ La recta $y=2x$ \textbf{passa per l'origen}, per $(0,\,0)$ i $(1,\,2)$: no podem usar $(0,\,0)$ com a punt de prova.

Amb $(1,\,0)$: $0\geq2$ \texttimes. La solució és el semipla que no conté $(1,\,0)$, el de damunt de la recta (també ho diu el truc: $y\geq\dots$).''',
            fig([C(-2, 1, '>=', 0)], (-3, 3, -3, 4), w=3.0, labels=False, test=((1, 0), False))) + r'''
\end{exemple}
\begin{practica}
Resol gràficament: \quad a) $x+y\leq3$ \qquad b) $2x-3y>6$ \qquad c) $3x+2y\geq6$ \qquad d) $x-y\geq0$
\end{practica}
''')

# =====================================================================
add(r'\seccio{3.2}{Sistemes d’inequacions amb dues incògnites}')
add(r'''
\begin{defi}{Sistema d'inequacions i regió factible}
Un \textbf{sistema d'inequacions lineals amb dues incògnites} és un conjunt d'inequacions que s'han de complir \textbf{alhora}. Les solucions són els punts comuns a \textbf{tots} els semiplans (la seua \textbf{intersecció}). En programació lineal aquest conjunt s'anomena \textbf{regió factible}. Si no és buida, és un conjunt \textbf{convex} i pot ser:
\begin{itemize}
\item \textbf{acotada}: un polígon convex tancat; \quad \textbf{no acotada}: s'estén indefinidament en alguna direcció;
\item \textbf{buida}: cap punt compleix totes les inequacions i el sistema no té solució.
\end{itemize}
Els \textbf{vèrtexs} són els punts de tall de dues rectes frontera que compleixen \emph{totes} les inequacions. Es calculen resolent el sistema format per les dues rectes.
\end{defi}
\begin{defi}{Resolució gràfica d'un sistema}
1) Resolem cada inequació per separat (recta frontera i punt de prova) sobre els mateixos eixos. \ 2) La solució és la \textbf{zona comuna} a tots els semiplans. \ 3) Calculem els \textbf{vèrtexs} resolent els sistemes de les rectes que s'hi tallen.

\smallskip
\emph{Consell:} acoloreix cada recta i marca amb una fletxa cap a quin costat queda el seu semipla.
\end{defi}
''')
MINI = lambda c, t: r'\begin{minipage}[t]{0.235\linewidth}\centering ' + fig([c], (-3, 4, -3, 4), w=2.9, labels=False, draw_axes_cons=True) + r'\par\small ' + t + r'\end{minipage}'
add(r'''
\begin{propi}{Cas particular: inequacions $x\geq k$, $x\leq k$, $y\geq k$, $y\leq k$}
Si en la inequació només apareix una incògnita, la recta frontera és paral·lela a un eix i \textbf{no cal punt de prova}:
\begin{center}\small\renewcommand{\arraystretch}{1.25}\begin{tabular}{lll}\hline
\textbf{Inequació} & \textbf{Recta frontera} & \textbf{Semipla solució}\\\hline
$x\geq k$ \ / \ $x\leq k$ & $x=k$: vertical, per $(k,\,0)$ & a la \textbf{dreta} \ / \ a l'\textbf{esquerra} de la recta\\
$y\geq k$ \ / \ $y\leq k$ & $y=k$: horitzontal, per $(0,\,k)$ & per \textbf{damunt} \ / \ per \textbf{davall} de la recta\\\hline
\end{tabular}\end{center}
\begin{itemize}
\item \textbf{Compte:} $x\geq3$ no és un punt ni una recta horitzontal: $x=3$ és la recta \textbf{vertical} dels punts d'abscissa 3.
\item Les \textbf{condicions de no negativitat} $x\geq0$ (dreta de l'eix $OY$) i $y\geq0$ (damunt de l'eix $OX$) apareixen en quasi tots els problemes; juntes, limiten la regió al \textbf{primer quadrant}.
\item Una doble desigualtat com $1\leq x\leq5$ són dues inequacions, $x\geq1$ i $x\leq5$: una \textbf{franja vertical}.
\end{itemize}
\end{propi}
\begin{exemple}{Exemples d'inequacions amb una sola incògnita}
\noindent''' + MINI(C(1, 0, '>=', 2), r'$x\geq2$: dreta de $x=2$') + r'\hfill' + MINI(C(1, 0, '<', -1), r'$x<-1$: esquerra, recta discontínua') + r'\hfill'
    + MINI(C(0, 1, '<=', 3), r'$y\leq3$: davall de $y=3$') + r'\hfill' + MINI(C(0, 1, '>', -2), r'$y>-2$: damunt, discontínua') + r'''
\end{exemple}
''')
add(r'''
\begin{exemple}{Sistema amb regió acotada}
''' + costat(r'''\raggedright Resolem gràficament i calculem els vèrtexs:\par\smallskip $''' + sist(r'x+y&\leq6', r'y&\leq4', r'x&\leq5', r'x&\geq1', r'y&\geq0') + r'''$

$x+y\leq6$: recta per $(0,\,6)$ i $(6,\,0)$; amb $(0,\,0)$: $0\leq6$ \checkmark, semipla de l'origen. Les altres quatre són del tipus particular: davall de $y=4$, esquerra de $x=5$, dreta de $x=1$ i damunt de l'eix $OX$. La regió és un pentàgon (\textbf{acotada}).''',
            fig(RPENT, (-1, 7, -1, 6.5), w=4.4, names={(1, 0): 'A', (5, 0): 'B', (5, 1): 'C', (2, 4): 'D', (1, 4): 'E'}), 0.55) + r'''
\[A:\ \sist{x&=1\\y&=0}\Rightarrow(1,\,0)\quad B:\ \sist{x&=5\\y&=0}\Rightarrow(5,\,0)\quad C:\ \sist{x&=5\\x+y&=6}\Rightarrow(5,\,1)\]\[D:\ \sist{y&=4\\x+y&=6}\Rightarrow(2,\,4)\quad E:\ \sist{x&=1\\y&=4}\Rightarrow(1,\,4)\]
El tall de $y=4$ i $x=5$, el punt $(5,\,4)$, \textbf{no} és vèrtex: no compleix $x+y\leq6$ ($9>6$).
\end{exemple}
''')
add(r'''
\begin{exemple}{Regió no acotada i regió buida}
\begin{minipage}[t]{0.48\linewidth}
$\sist{x+y&\geq4\\x&\geq1\\y&\geq0}$ \ L'origen no compleix $x+y\geq4$: el semipla és el de damunt. La regió és \textbf{no acotada} i té dos vèrtexs, $(1,\,3)$ i $(4,\,0)$.
\begin{center}''' + fig(RNAC, (-1, 7, -1, 6), w=3.8) + r'''\end{center}
\end{minipage}\hfill
\begin{minipage}[t]{0.48\linewidth}
$\sist{x+y&\leq2\\x+y&\geq5\\x\geq0,\ y&\geq0}$ \ Les rectes $x+y=2$ i $x+y=5$ són paral·leles i cap punt no compleix alhora les dues inequacions: la regió és \textbf{buida}.
\begin{center}''' + fig(RBUI, (-1, 7, -1, 6), w=3.8) + r'''\end{center}
\end{minipage}
\end{exemple}
\begin{practica}
Resol gràficament, digues si la regió és acotada, no acotada o buida i calcula'n els vèrtexs:
\begin{tasks}(4)
\task $\sist{x+2y&\leq8\\x-y&\leq2\\x\geq0,\ y&\geq0}$
\task $\sist{x&\leq4\\y&\geq1\\y&\leq x+1\\x&\geq0}$
\task $\sist{2x+y&\geq4\\x+y&\geq3\\x\geq0,\ y&\geq0}$
\task $\sist{x+y&\geq5\\x&\leq2\\y&\leq2}$
\end{tasks}
\end{practica}
''')

# =====================================================================
add(r'\seccio{3.3}{Problemes de programació lineal}')
add(r'''
\begin{defi}{Problema de programació lineal}
Consisteix a \textbf{optimitzar} (maximitzar o minimitzar) una funció lineal $f(x,y)=ax+by$ quan les variables han de complir un sistema d'inequacions lineals. Vocabulari:
\begin{itemize}
\item \textbf{Variables de decisió}: les incògnites $x$, $y$ (què hem de decidir).
\item \textbf{Funció objectiu}: $f(x,y)=ax+by$, que volem fer màxima (beneficis, ingressos…) o mínima (costos, temps…).
\item \textbf{Restriccions}: les inequacions que han de complir les variables (recursos, mínims exigits, no negativitat…).
\item \textbf{Regió factible}: els punts que compleixen totes les restriccions; cadascun és una \textbf{solució factible}.
\item \textbf{Solució òptima}: la solució factible on $f$ pren el valor màxim (o mínim), anomenat \textbf{valor òptim}.
\end{itemize}
\end{defi}
\begin{propi}{Teorema fonamental de la programació lineal}
\begin{enumerate}
\item Si la regió factible és \textbf{no buida i acotada}, la funció objectiu té sempre màxim i mínim, i s'assoleixen en \textbf{vèrtexs}.
\item Si l'òptim s'assoleix en \textbf{dos vèrtexs}, també s'assoleix en \textbf{tots els punts del segment} que els uneix.
\item Si la regió és \textbf{no acotada}, pot ser que no hi haja màxim (o mínim); si n'hi ha, també és en un vèrtex.
\end{enumerate}
\emph{Conseqüència:} no cal provar tots els punts de la regió (n'hi ha infinits): n'hi ha prou amb avaluar $f$ en els vèrtexs.
\end{propi}
\begin{defi}{Passos per resoldre un problema de programació lineal}
\begin{enumerate}
\item Llegim l'enunciat, triem les \textbf{variables} i organitzem les dades en una \textbf{taula}.
\item Escrivim la \textbf{funció objectiu} i diem si s'ha de maximitzar o minimitzar.
\item Escrivim les \textbf{restriccions} (sense oblidar $x\geq0$, $y\geq0$ quan calga).
\item Dibuixem la \textbf{regió factible} i calculem els \textbf{vèrtexs}.
\item \textbf{Avaluem} la funció objectiu en els vèrtexs (mètode analític) o usem les \textbf{rectes de nivell} (mètode gràfic).
\item \textbf{Interpretem} el resultat i responem la pregunta amb les unitats corresponents.
\end{enumerate}
\end{defi}
''')
add(r'''
\begin{exemple}{Exemple resolt pas a pas: producció de bicicletes}
Una empresa fabrica bicicletes de passeig i de muntanya. Cada bicicleta de passeig necessita 1 kg d'acer i 3 kg d'alumini, i cada bicicleta de muntanya, 2 kg d'acer i 2 kg d'alumini. Disposa de 80 kg d'acer i 120 kg d'alumini. Guanya 20 € per cada bicicleta de passeig i 15 € per cada bicicleta de muntanya. Quantes n'ha de fabricar de cada tipus per obtenir el màxim benefici?

\smallskip
\costat[0.5]{\textbf{1. Variables i dades.} $x$ = bicicletes de passeig, $y$ = bicicletes de muntanya.

\textbf{2. Funció objectiu:} \ $\max\ B(x,y)=20x+15y$

\textbf{3. Restriccions:} \ $''' + sist(r'x+2y&\leq80&&\text{(acer)}', r'3x+2y&\leq120&&\text{(alumini)}', r'x\geq0,\ y&\geq0') + r'''$}{\small\renewcommand{\arraystretch}{1.15}\begin{tabular}{lccc}\hline & Acer & Alumini & Benefici\\\hline Passeig $(x)$ & 1 kg & 3 kg & 20 €\\ Muntanya $(y)$ & 2 kg & 2 kg & 15 €\\ Disponible & 80 kg & 120 kg & \\\hline\end{tabular}}

\smallskip
''' + costat(r'''\textbf{4. Regió factible i vèrtexs.} \ $x+2y=80$ passa per $(0,\,40)$ i $(80,\,0)$; \ $3x+2y=120$, per $(0,\,60)$ i $(40,\,0)$. L'origen compleix les dues inequacions. Vèrtexs: $O(0,\,0)$, $A(40,\,0)$, $C(0,\,40)$ i
\[B:\ \sist{x+2y&=80\\3x+2y&=120}\xrightarrow{E_2-E_1}2x=40\Rightarrow x=20,\ y=30\]

\textbf{5. Avaluem $B$ en els vèrtexs:}
\begin{center}\small\begin{tabular}{ccccc}\hline Vèrtex & $O(0,\,0)$ & $A(40,\,0)$ & $B(20,\,30)$ & $C(0,\,40)$\\ $20x+15y$ & 0 & 800 & \textbf{850} & 600\\\hline\end{tabular}\end{center}''',
            fig(RBIC, (-4, 48, -4, 63), w=4.2, hmax=5.2, names={(0, 0): 'O', (40, 0): 'A', (20, 30): 'B', (0, 40): 'C'}, opt=[(20, 30)]), 0.6) + r'''
\textbf{6. Resposta.} S'han de fabricar \textbf{20 bicicletes de passeig i 30 de muntanya}; el benefici màxim és de \textbf{850 €}.
\end{exemple}
''')
add(r'''
\begin{defi}{Mètode gràfic: rectes de nivell}
Per a cada valor $k$, els punts on $f$ val $k$ formen la recta $ax+by=k$, anomenada \textbf{recta de nivell}. Totes són \textbf{paral·leles} a $ax+by=0$.
1) Dibuixem $ax+by=0$. \ 2) La desplacem paral·lelament en el sentit en què $f$ creix. \ 3) Per \textbf{maximitzar} busquem l'\textbf{últim} punt de la regió que toca la recta; per \textbf{minimitzar}, el \textbf{primer}.
\end{defi}
\begin{exemple}{Rectes de nivell en el problema de les bicicletes}
''' + costat(r'''Dibuixem les rectes de nivell $20x+15y=k$ per a diversos valors de $k$:
\begin{itemize}
\item $k=300$ i $k=600$ tallen la regió: hi ha solucions factibles amb aquests beneficis.
\item En augmentar $k$, la recta es desplaça cap amunt i a la dreta. L'\textbf{última} posició en què toca la regió és $k=850$, i només la toca en $B(20,\,30)$: és el \textbf{màxim}.
\item Per a $k>850$ la recta ja no toca la regió.
\item La \textbf{primera} recta que toca la regió és $k=0$, en $O(0,\,0)$: és el \textbf{mínim}.
\end{itemize}''', fig(RBIC, (-4, 48, -4, 63), w=4.2, hmax=5.2, labels=False, opt=[(20, 30)],
                     levels=[(20, 15, 300, 'k=300'), (20, 15, 600, 'k=600'), (20, 15, 850, 'k=850'), (20, 15, 1100, 'k=1100')],
                     extra=r'\fill[accent] (20,30) circle (2.3pt);\node[font=\tiny,above right] at (20,30) {$B$};'), 0.56) + r'''
\end{exemple}
\begin{nota}\textbf{Solucions enteres.} Quan les variables compten objectes (bicicletes, persones, autobusos…) la solució ha de tenir coordenades enteres. Si el vèrtex òptim no és enter, cal estudiar els punts enters de la regió més pròxims. Per exemple, si el mínim de $72x+108y$ (autobusos xicotets i grans) està en el vèrtex $(4;\ 0{,}8)$, provem els punts enters pròxims de la regió: $(4,\,1)$ costa 396 € i $(3,\,2)$, 432 €; la solució és $(4,\,1)$.\end{nota}
''')

# =====================================================================
add(r'\seccio{3.4}{Tipus de problemes clàssics}')
add(r'''
\begin{propi}{Problemes clàssics de programació lineal}
\begin{center}\small\renewcommand{\arraystretch}{1.2}\begin{tabular}{p{2.6cm}p{5.4cm}p{7.2cm}}\hline
\textbf{Tipus} & \textbf{Objectiu} & \textbf{Restriccions típiques}\\\hline
Producció & Maximitzar beneficis o ingressos & Recursos limitats (matèria primera, hores…): $\leq$\\
Dieta & Minimitzar el cost & Necessitats mínimes de nutrients: $\geq$\\
Transport & Minimitzar el cost d'enviament & Existències dels orígens i demandes dels destins\\
Inversió / mescla & Maximitzar el rendiment o minimitzar el cost & Capital total, límits i proporcions\\\hline
\end{tabular}\end{center}
El problema de les bicicletes és de \textbf{producció}. Ara en veiem un de cada un dels altres tipus.
\end{propi}
''')
add(r'''
\begin{exemple}{Problema de dieta}
Un ramader barreja dos productes, A i B. Cada kg de A aporta 3 unitats de proteïnes i 1 de minerals; cada kg de B, 1 unitat de proteïnes i 2 de minerals. El bestiar necessita cada dia almenys 12 unitats de proteïnes i 9 de minerals. El kg de A costa 5 € i el de B, 3 €. Quants kg de cada producte ha de barrejar perquè el cost siga mínim?

\smallskip
''' + costat(r'''$x$ = kg de A, $y$ = kg de B. \qquad $\min\ C(x,y)=5x+3y$ \qquad $\sist{3x+y&\geq12&&\text{(proteïnes)}\\x+2y&\geq9&&\text{(minerals)}\\x\geq0,\ y&\geq0}$

En els problemes de dieta les restriccions són de tipus $\geq$ i l'origen no les compleix: la regió queda per damunt de les rectes i és \textbf{no acotada}. Vèrtexs: $(0,\,12)$, $(9,\,0)$ i el tall de les dues rectes, $(3,\,3)$.

$C(0,\,12)=36$, \ $C(3,\,3)=\mathbf{24}$, \ $C(9,\,0)=45$. Com que els coeficients de $C$ són positius, allunyar-se de l'origen només encareix el cost: el mínim existeix (el màxim, no).

\textbf{Resposta:} 3 kg de A i 3 kg de B, amb un cost mínim de \textbf{24 €} diaris.''',
            fig(RDIE, (-1, 12, -1, 14), w=3.8, hmax=4.6, opt=[(3, 3)], levels=[(5, 3, 24, '')]), 0.6) + r'''
\end{exemple}
''')
add(r'''
\begin{exemple}{Problema de transport}
Una empresa té dos magatzems, M1 amb 50 tones i M2 amb 40 tones, i ha de servir 30 tones a la botiga B1 i 40 a la B2. Els costos per tona (en €) són: de M1 a B1, 3; de M1 a B2, 2; de M2 a B1, 1; de M2 a B2, 4. Com s'ha d'organitzar l'enviament perquè el cost siga mínim?

\smallskip
''' + costat(r'''\textbf{Clau:} n'hi ha prou amb dues variables. Si $x$ i $y$ són les tones que van de M1 a B1 i a B2, M2 envia $30-x$ a B1 i $40-y$ a B2. Totes les quantitats són $\geq0$ i cap magatzem no pot enviar més del que té:
\[\sist{0\leq x&\leq30\\0\leq y&\leq40\\x+y&\leq50&&\text{(M1)}\\x+y&\geq30&&\text{(M2)}}\]
La de M2 surt de $(30-x)+(40-y)\leq40$.
Cost: $3x+2y+(30-x)+4(40-y)=2x-2y+190$. En els vèrtexs val: $(30,\,0)\to250$, \ $(30,\,20)\to210$, \ $(10,\,40)\to130$, \ $(0,\,40)\to\mathbf{110}$, \ $(0,\,30)\to130$.

\textbf{Resposta:} M1 envia 0 t a B1 i 40 t a B2; M2 envia 30 t a B1 i res a B2. Cost mínim: \textbf{110 €}.''',
            fig(RTRA, (-4, 36, -4, 46), w=3.8, hmax=4.6, opt=[(0, 40)]), 0.6) + r'''
\end{exemple}
''')
add(r'''
\begin{exemple}{Problema d'inversió}
Una persona vol invertir com a màxim 10\,000 € en dos productes: A, amb una rendibilitat anual del 5\,\%, i B, del 8\,\%. Vol invertir almenys 2000 € en A, com a màxim 6000 € en B, i en B no més del doble del que invertisca en A. Com ha de repartir els diners?

\smallskip
''' + costat(r'''$x$, $y$ = milers d'euros en A i en B. Cada miler rendeix 50 € en A i 80 € en B:
\[\max\ R(x,y)=50x+80y\qquad\sist{x+y&\leq10\\x&\geq2\\y&\leq6\\y&\leq2x\\y&\geq0}\]
Vèrtexs i valors: $(2,\,0)\to100$, \ $(10,\,0)\to500$, \ $(4,\,6)\to\mathbf{680}$, \ $(3,\,6)\to630$, \ $(2,\,4)\to420$.

\textbf{Resposta:} 4000 € en A i 6000 € en B; rendiment màxim de \textbf{680 €} anuals.''',
            fig(RINV, (-1, 11.5, -1, 8), w=3.8, opt=[(4, 6)], levels=[(50, 80, 680, '')]), 0.6) + r'''
\end{exemple}
\begin{practica}
\begin{enumerate}
\item \textbf{(Producció)} Un artesà fa collars i polseres. Un collar requereix 2 hores de treball i 1 unitat de material; una polsera, 1 hora i 2 unitats de material. Disposa de 16 hores i 14 unitats de material a la setmana i guanya 30 € per collar i 20 € per polsera. Quants n'ha de fer de cada per maximitzar el benefici?
\item \textbf{(Dieta)} Una persona ha de prendre cada dia almenys 8 unitats de vitamina A i 9 de vitamina B. Un sobre del preparat X conté 1 unitat de A i 3 de B i costa 3 €; un sobre de Y conté 2 unitats de A i 1 de B i costa 2 €. Quants sobres de cada ha de prendre per gastar el mínim?
\end{enumerate}
\end{practica}
''')

# =====================================================================
add(r'\seccio{3.5}{Casos especials: infinites solucions i sense solució}')
add(r'''
\begin{propi}{Possibles resultats d'un problema de programació lineal}
\begin{enumerate}
\item \textbf{Solució única}: l'òptim s'assoleix en un sol vèrtex. És el cas més habitual.
\item \textbf{Infinites solucions}: l'òptim s'assoleix en dos vèrtexs consecutius i, per tant, en tot el costat que els uneix. Passa quan la funció objectiu és \textbf{paral·lela a un costat} de la regió i eixe costat és el de l'òptim.
\item \textbf{Sense solució}: la \textbf{regió factible és buida} (restriccions incompatibles), o la regió és \textbf{no acotada} i la funció objectiu pot créixer (o decréixer) indefinidament.
\end{enumerate}
\emph{Paral·lelisme:} $f=ax+by$ és paral·lela a la restricció $px+qy\leq r$ si els coeficients són proporcionals, $\dfrac ap=\dfrac bq$.
\end{propi}
''')
add(r'''
\begin{exemple}{Infinites solucions}
''' + costat(r'''Collars i polseres amb un benefici de 40 € per collar i 20 € per polsera:
\[\max\ f=40x+20y\qquad\sist{2x+y&\leq16\\x+2y&\leq14\\x\geq0,\ y&\geq0}\]
$f(0,\,0)=0$, \ $f(8,\,0)=320$, \ $f(6,\,4)=320$, \ $f(0,\,7)=140$. El màxim, 320, s'assoleix en dos vèrtexs: $40x+20y=20(2x+y)$ és paral·lela a $2x+y=16$.

Són òptims tots els punts del segment: \ $y=16-2x$, \ $6\leq x\leq8$. Com que es fabriquen unitats senceres, les solucions vàlides són $(8,\,0)$, $(7,\,2)$ i $(6,\,4)$.''',
            fig(RCOL, (-1, 10, -1, 9), w=3.8, opt=[(6, 4), (8, 0)], seg=((6, 4), (8, 0)), levels=[(40, 20, 320, '')]), 0.6) + r'''
\end{exemple}
\begin{exemple}{Regió no acotada sense òptim}
''' + costat(r'''Amb les restriccions del problema de la dieta volem \textbf{maximitzar} $f=5x+3y$. Als vèrtexs: $f(0,\,12)=36$, $f(3,\,3)=24$, $f(9,\,0)=45$; però $(100,\,0)$ també és de la regió i $f(100,\,0)=500$.

Les rectes de nivell $5x+3y=k$ es poden desplaçar cap amunt indefinidament i sempre tallen la regió: $f$ \textbf{no té màxim}. (El mínim sí que existeix: és 24, en $(3,\,3)$.)

\textbf{Compte:} en una regió no acotada no n'hi ha prou amb avaluar els vèrtexs; cal comprovar, gràficament o amb un punt allunyat, si la funció pot millorar sense límit.''',
            fig(RDIE, (-1, 14, -1, 14), w=3.8, levels=[(5, 3, 45, 'k=45'), (5, 3, 70, 'k=70'), (5, 3, 95, '')]), 0.6) + r'''
\end{exemple}
\begin{exemple}{Regió factible buida i òptim en una semirecta}
\begin{minipage}[t]{0.48\linewidth}
\textbf{Regió buida.} Maximitzem $f=x+y$ amb $x+y\leq3$, $2x+3y\geq12$, $x,y\geq0$. La recta $2x+3y=12$ passa per $(6,\,0)$ i $(0,\,4)$ i tot el triangle $x+y\leq3$ queda per davall: cap punt no compleix totes les restriccions. El problema \textbf{no té solució}.
\begin{center}''' + fig(RBUI2, (-1, 7, -1, 5), w=3.6) + r'''\end{center}
\end{minipage}\hfill
\begin{minipage}[t]{0.48\linewidth}
\textbf{Semirecta.} En una regió no acotada l'òptim es pot assolir en tota una semirecta. Si minimitzem $f=y$ en la regió $x\geq2$, $y\geq1$, el mínim val 1 i s'assoleix en tots els punts $(x,\,1)$ amb $x\geq2$: \textbf{infinites solucions}.
\begin{center}''' + fig(RRAIG, (-1, 7, -1, 5), w=3.6, draw_axes_cons=True, extra=r'\draw[accent,line width=3pt] (2,1)--(7,1);\fill[accent] (2,1) circle (2.3pt);') + r'''\end{center}
\end{minipage}
\end{exemple}
\begin{practica}
En la regió $3x+y\geq12$, $x+2y\geq9$, $x\geq0$, $y\geq0$ (la de la dieta), estudia quina solució té cada problema:
\begin{tasks}(4)
\task $\min\ f=x+2y$ \task $\min\ f=x+y$ \task $\max\ f=-x-y$ \task $\max\ f=x+y$
\end{tasks}
\end{practica}
''')

# =====================================================================
add(r'\seccio{}{Solucions dels exercicis de pràctica}')
add(r'''\small
\textbf{3.1.} a) Recta contínua per $(3,\,0)$ i $(0,\,3)$; semipla de l'origen. \ b) Recta discontínua per $(3,\,0)$ i $(0,\,-2)$; semipla que no conté l'origen. \ c) Recta contínua per $(2,\,0)$ i $(0,\,3)$; semipla que no conté l'origen. \ d) Recta $y=x$; amb $(1,\,0)$: $1\geq0$ \checkmark, semipla de davall de la bisectriu.

\textbf{3.2.} a) Acotada; vèrtexs ''' + V(reg([C(1, 2, '<=', 8), C(1, -1, '<=', 2)] + NN, [(0, 0), (2, 0), (4, 2), (0, 4)])) + r'''. \ b) Acotada (triangle); vèrtexs ''' + V(reg([C(1, 0, '<=', 4), C(0, 1, '>=', 1), C(-1, 1, '<=', 1), C(1, 0, '>=', 0)], [(0, 1), (4, 1), (4, 5)])) + r'''. \ c) No acotada; vèrtexs ''' + V(reg([C(2, 1, '>=', 4), C(1, 1, '>=', 3)] + NN, [(0, 4), (1, 2), (3, 0)])) + r'''. \ d) Buida: amb $x\leq2$ i $y\leq2$, $x+y\leq4<5$.''' + (reg([C(1, 1, '>=', 5), C(1, 0, '<=', 2), C(0, 1, '<=', 2)], []) and '') + r'''

\textbf{3.4.} 1) $\max\ 30x+20y$ amb $2x+y\leq16$, $x+2y\leq14$, $x,y\geq0$: 6 collars i 4 polseres, benefici màxim 260 €. \ 2) $\min\ 3x+2y$ amb $x+2y\geq8$, $3x+y\geq9$, $x,y\geq0$: 2 sobres de X i 3 de Y, cost mínim 12 €.''' + opt(reg([C(1, 2, '>=', 8), C(3, 1, '>=', 9)] + NN, [(0, 9), (2, 3), (8, 0)]), 3, 2, 'min', 12, [(2, 3)]) + r'''

\textbf{3.5.} a) Mínim 9 en tot el segment d'extrems $(3,\,3)$ i $(9,\,0)$ (infinites solucions). \ b) Mínim 6 en $(3,\,3)$. \ c) Màxim $-6$ en $(3,\,3)$ (equival a minimitzar $x+y$). \ d) No té màxim (regió no acotada).
\normalsize''')

# ---------- comprovacions ----------
for c in CHK:
    if c[0] == 'v':
        Vs, _, _ = verts(c[1])
        assert sorted(Vs) == sorted((fr(a), fr(b)) for a, b in c[2]), (Vs, c[2])
    else:
        _, cons, p, q, goal, val, pts = c
        best, at = optim(cons, p, q, goal)
        assert best == fr(val) and at == sorted((fr(a), fr(b)) for a, b in pts), (p, q, goal, best, at)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read().split('% ---------- recta real ----------')[0]
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: "pdfkeywords={programació lineal, inequacions, regió factible, vèrtexs, funció objectiu, rectes de nivell}", pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
pre = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={Apunts de la unitat 3: Programació lineal. 2n de Batxillerat CCSS}")
pre = pre.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "Apunts · Unitat 3: Programació lineal · 2n Batxillerat CCSS")
pre = pre.replace(r'\usepackage{tikz}', r'\usepackage{tikz}' + '\n' + r'\usetikzlibrary{calc}')
# la lletra de la web (Inter, de la TeX Live) amb LuaLaTeX
pre = pre.replace(r'\usepackage[utf8]{inputenc}' + '\n', '').replace(r'\usepackage[T1]{fontenc}' + '\n', '')
pre = pre.replace(r'\usepackage[sfdefault,lining]{FiraSans}', r'''\usepackage{fontspec}
\setsansfont{Inter}[Extension=.otf,UprightFont=*-Regular,BoldFont=*-Bold,ItalicFont=*-Italic,BoldItalicFont=*-BoldItalic,Scale=0.94]
\renewcommand{\familydefault}{\sfdefault}''')
assert 'fontspec' in pre and 'inputenc' not in pre
pre = pre.replace(r'\setlength{\parskip}{3pt}', r'\setlength{\parskip}{3pt}\raggedbottom')
assert 'Apunts · Unitat 3' in pre and 'Apunts de la unitat 3' in pre and 'usetikzlibrary{calc}' in pre
pre += r'''
\usepackage{enumitem}
\usepackage{textcase}
\setlist{itemsep=1pt,topsep=2pt,parsep=0pt}
\definecolor{defc}{HTML}{1D4F73}\definecolor{defbg}{HTML}{EEF4F9}
\definecolor{propc}{HTML}{3B4252}\definecolor{propbg}{HTML}{F3F4F7}
\definecolor{exc}{HTML}{A3203A}\definecolor{exbg}{HTML}{FBF0F2}
\definecolor{prc}{HTML}{B7791F}\definecolor{prbg}{HTML}{FFF8E8}
\definecolor{navyb}{HTML}{2C4475}\definecolor{navyl}{HTML}{C3CBE2}
% quadres curts que no es parteixen
\newtcolorbox{defi}[1]{enhanced,colback=defbg,colframe=defc,arc=2mm,boxrule=0.7pt,fonttitle=\bfseries,coltitle=white,colbacktitle=defc,
  title={#1},left=3mm,right=3mm,top=1.2mm,bottom=1.2mm,before skip=7pt,after skip=7pt}
\newtcolorbox{propi}[1]{enhanced,colback=propbg,colframe=propc,arc=2mm,boxrule=0.7pt,fonttitle=\bfseries\small,coltitle=white,colbacktitle=propc,
  title={\MakeTextUppercase{#1}},halign title=center,left=3mm,right=3mm,top=1.2mm,bottom=1.2mm,before skip=7pt,after skip=7pt}
\newtcolorbox{nota}{enhanced,colback=white,colframe=accent,boxrule=0pt,leftrule=2.5pt,arc=0pt,outer arc=0pt,left=3mm,right=2mm,top=1mm,bottom=1mm,before skip=6pt,after skip=6pt}
% exemples i pràctica: franja lateral; poden continuar a la pàgina següent
\newtcolorbox{exemple}[1]{enhanced,breakable,colback=exbg,colframe=exc,boxrule=0pt,leftrule=2.5pt,arc=0pt,outer arc=0pt,
  left=3mm,right=3mm,top=1mm,bottom=1.5mm,before skip=7pt,after skip=7pt,before upper={{\color{exc}\bfseries\faPen\ #1}\par\nobreak\smallskip}}
\newtcolorbox{practica}{enhanced,breakable,colback=prbg,colframe=prc,boxrule=0pt,leftrule=2.5pt,arc=0pt,outer arc=0pt,
  left=3mm,right=3mm,top=1mm,bottom=1.5mm,before skip=7pt,after skip=7pt,before upper={{\color{prc}\bfseries\faEdit[regular]\ Practica}\par\nobreak\smallskip}}
\providecommand{\sist}{}\renewcommand{\sist}[1]{\left\{\begin{aligned}#1\end{aligned}\right.}
\newcommand{\costat}[3][0.56]{\par\noindent\begin{minipage}[c]{#1\linewidth}#2\end{minipage}\hfill\begin{minipage}[c]{\dimexpr0.96\linewidth-#1\linewidth\relax}\centering #3\end{minipage}\par}
'''

CAP = r'''
% ---------- capçalera 6 («Apunts web») ----------
\makeatletter
\newcommand{\capcaleraweb}[3]{\gdef\fm@cursnom{2n Batx}%
  \par\noindent\begin{tikzpicture}
    \shade[left color=navy,right color=navyb,rounded corners=3mm] (0,0) rectangle (\linewidth,2.95cm);
    \begin{scope}\clip[rounded corners=3mm] (0,0) rectangle (\linewidth,2.95cm);
      \begin{scope}[transparency group,opacity=.08]
        \node[anchor=south east,inner sep=0] at ([xshift=-0.6cm,yshift=-1.4cm]\linewidth,0) {\includegraphics[height=3.3cm]{../../logo/pdf/marca-blanc.pdf}};
      \end{scope}\end{scope}
    \node[anchor=north west,inner sep=0] at (0.65cm,2.55cm) {\includegraphics[height=0.72cm]{../../logo/pdf/horitzontal-fosc.pdf}};
    \node[anchor=north east,inner sep=0,font=\small,text=navyl] at ([xshift=-0.65cm]\linewidth,2.42cm) {#1};
    \node[anchor=west,fill=curs!30!navy,text=curs!45!white,rounded corners=1.6mm,font=\scriptsize\bfseries,inner xsep=2.2mm,inner ysep=0.9mm] at (0.65cm,1.42cm) {#2};
    \node[anchor=south west,inner sep=0,text=white,font=\fontsize{23}{25}\selectfont\bfseries] at (0.65cm,0.3cm) {#3};
  \end{tikzpicture}\par\vspace{4pt}}
\makeatother
'''

body = '\n'.join(B).replace('\\begin{exemple}', '\\espai{9\\baselineskip}\\begin{exemple}').replace('\\begin{practica}', '\\espai{6\\baselineskip}\\begin{practica}')
doc = [pre, CAP, r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}
% \espai: com \needspace, però sense el \penalty-100 que convida a saltar de pàgina encara que hi haja lloc
\makeatletter
\newcommand{\espai}[1]{\par\begingroup\setlength{\dimen@}{#1}\dimen@ii\pagegoal\advance\dimen@ii-\pagetotal
  \ifdim\dimen@>\dimen@ii\ifdim\dimen@ii>\z@\vfil\fi\penalty-\@M\fi\endgroup}
\renewcommand{\seccio}[2]{\espai{12\baselineskip}\bigskip\par\noindent
  \if\relax\detokenize{#1}\relax\else\tikz[baseline=(n.base)]\node[fill=defc,text=white,rounded corners=1.8mm,minimum width=1.05cm,minimum height=0.95cm,font=\bfseries](n){#1};\hspace{3mm}\fi
  {\color{defc}\fontsize{16}{19}\selectfont\bfseries #2}\par\vspace{1.5mm}{\color{black!13}\hrule height 1.1pt}\vspace{1mm}}
% capçalera de les pàgines 2 i següents: logo blau i groc, títol al centre i curs en el blau fosc del logo
\fancyhead[L]{\raisebox{-0.3\height}{\includegraphics[height=0.62cm]{../../logo/pdf/marca-clar.pdf}}}
\fancyhead[R]{\small\bfseries\color{navy}\fm@cursnom}
\renewcommand{\headrule}{\color{navy!35}\hrule height \headrulewidth}
\makeatother

\begin{document}
\thispagestyle{primera}
\capcaleraweb{2n Batxillerat CCSS · Unitat 3}{Apunts}{Programació lineal}
''', body, '\n\\end{document}\n']
open(os.path.join(HERE, 't3-apunts.tex'), 'w', encoding='utf-8').write(''.join(doc))
print(len(CHK), 'comprovacions correctes')
