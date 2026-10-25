# Genera t4-fitxa-exercicis.tex i t4-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 4: Límits i continuïtat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Els exercicis marcats amb \pau{...} són de la PAU d'altres comunitats (recopilació de www.ebaumatematicas.com),
# traduïts al valencià. Al final, CHK comprova numèricament tots els límits i paràmetres de les solucions.
# Ús: python3 genera.py && pdflatex t4-fitxa-exercicis.tex (dues vegades) && pdflatex t4-fitxa-solucions.tex
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def L(a, e): return r'\displaystyle\lim_{x\to %s}%s' % (a, e)
def pw(*rows, name='f(x)'):
    return name + r'=\begin{cases}' + r'\\[3pt]'.join(r'%s&\text{si }%s' % r for r in rows) + r'\end{cases}'
def m(s): return '$' + s + '$'
def dm(s): return r'\[' + s + r'\]'
PI, MI = r'+\infty', r'-\infty'

# ---------- gràfiques ----------
def img(f, w='5.2cm'): return r'\includegraphics[width=%s]{%s}' % (w, f)
def tzg(x0, x1, y0, y1, body, sc=0.42):
    g = r'\draw[muted!30,very thin] (%s,%s) grid (%s,%s);' % (x0, y0, x1, y1)
    g += r'\draw[-latex,thick] (%s,0)--(%s,0);\draw[-latex,thick] (0,%s)--(0,%s);' % (x0, x1 + 0.4, y0, y1 + 0.4)
    return r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]\begin{scope}%s\clip (%s,%s) rectangle (%s,%s);%s\end{scope}\end{tikzpicture}' % (sc, g, x0, y0, x1, y1, body)
CV = r'\draw[accent,line width=1.5pt,smooth,samples=90,domain=%s] plot (\x,{%s});'
def dot(x, y, o=False): return (r'\filldraw[fill=white,draw=accent,line width=1.1pt] (%s,%s) circle (0.17);' if o else r'\fill[accent] (%s,%s) circle (0.17);') % (x, y)
def tk(x, y, t, pos='below'): return r'\node[%s,font=\scriptsize] at (%s,%s) {$%s$};' % (pos, x, y, t)
G_LN = tzg(-1, 5, -3, 2, CV % ('0.05:5', 'ln(\\x)') + tk(1, 0, '1') + tk(0, 1, '1', 'left'))
G_SQ = tzg(-4, 5, -1, 3, CV % ('-3:5', 'sqrt(\\x+3)') + dot(-3, 0) + tk(-3, 0, '-3') + tk(1, 0, '1'))
G_SC = tzg(-3, 3, -1, 3, r'\draw[accent,line width=1.5pt] (2,0) arc (0:180:2);' + dot(-2, 0) + dot(2, 0) + tk(-2, 0, '-2') + tk(2, 0, '2'))
G_SALT = tzg(-4, 4, -3, 4, CV % ('-3.46:0', '\\x*\\x/2-2') + CV % ('0:4', '1+1/(\\x+1)') + r'\draw[teal,dashed] (-4,1)--(4,1);' + dot(0, -2, True) + dot(0, 2) + tk(1, 0, '1') + tk(0, 1, '1', 'left'), sc=0.5)

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Límits a l'infinit", [
 (1, r"\label{ex:g1}Observa les gràfiques de les funcions $f$ i $g$ i calcula, per a cadascuna, el límit quan $x\to+\infty$ i quan $x\to-\infty$." + tasks(2, [r'$f(x)$:\par' + img('grafica1.jpg'), r'$g(x)$:\par' + img('grafica2.jpg')])
     + recorda(r"Per a $x\to+\infty$ mira el \textbf{final dret} de la gràfica; per a $x\to-\infty$, el \textbf{final esquerre}. Les rectes discontínues són asímptotes."),
     tasks(2, [r'$\displaystyle\lim_{x\to+\infty}f(x)=\res{+\infty}$, \ $\displaystyle\lim_{x\to-\infty}f(x)=\res{0}$', r'$\displaystyle\lim_{x\to+\infty}g(x)=\res{2}$, \ $\displaystyle\lim_{x\to-\infty}g(x)=\res{2}$ \ (asímptota $y=2$)'])),
 (2, r"Llig a cada gràfica el límit quan $x\to+\infty$ i quan $x\to-\infty$. Fixa't bé en el domini de cada funció:" + tasks(3, ['a)\\par' + G_LN, 'b)\\par' + G_SQ, 'c)\\par' + G_SC]).replace('\\task a)\\par', '\\task ').replace('\\task b)\\par', '\\task ').replace('\\task c)\\par', '\\task '),
     tasks(1, [r"Domini $(0,+\infty)$: \ $\displaystyle\lim_{x\to+\infty}=\res{+\infty}$; \ $\res{\nexists}\displaystyle\lim_{x\to-\infty}$ (la funció no està definida per a $x\leq0$).", r"Domini $[-3,+\infty)$: \ $\displaystyle\lim_{x\to+\infty}=\res{+\infty}$; \ $\res{\nexists}\displaystyle\lim_{x\to-\infty}$.", r"Domini $[-2,2]$: no arriba a cap infinit, $\res{\nexists}$ cap dels dos límits."])),
 (1, r"Calcula els límits següents:" + tasks(4, [m(L(PI, r'(3x^4-2x+7)')), m(L(MI, r'(-x^3+4x^2)')), m(L(MI, r'(2x^5-x^2)')), m(L(PI, r'(5-2x^2)'))])
     + recorda(r"El límit d'un polinomi quan $x\to\pm\infty$ és el del seu \textbf{terme de major grau}. Compte amb el signe: $(-\infty)^{\text{parell}}=+\infty$ i $(-\infty)^{\text{senar}}=-\infty$."),
     tasks(4, [r'$\lim 3x^4=\res{+\infty}$', r'$\lim(-x^3)=\res{+\infty}$', r'$\lim 2x^5=\res{-\infty}$', r'$\lim(-2x^2)=\res{-\infty}$'])),
 (1, r"Calcula comparant els graus del numerador i del denominador:" + tasks(3, [m(L(PI, r'\dfrac{2x^3-x}{5x^3+4}')), m(L(PI, r'\dfrac{x^2+1}{x^3-2}')), m(L(MI, r'\dfrac{4x^4-x}{3x^2+1}')), m(L(MI, r'\dfrac{1-3x^2}{x+2}')), m(L(PI, r'\dfrac{7x-2}{3-x}')), m(L(PI, r'\dfrac{x^5}{100x^4+1}'))])
     + recorda(r"$\displaystyle\lim_{x\to\pm\infty}\frac{P(x)}{Q(x)}=\lim_{x\to\pm\infty}\frac{a_nx^n}{b_mx^m}$: \ si $n>m$, $\pm\infty$; \ si $n=m$, $\frac{a_n}{b_m}$; \ si $n<m$, $0$."),
     tasks(3, [r'Mateix grau: $\res{\frac25}$', r'Grau de baix major: $\res{0}$', r'$\lim\frac{4x^2}{3}=\res{+\infty}$', r'$\lim(-3x)=\res{+\infty}$', r'$\frac{7}{-1}=\res{-7}$', r'$\lim\frac{x}{100}=\res{+\infty}$'])),
 (2, r"Calcula els límits següents amb arrels i exponencials:" + tasks(3, [m(L(PI, r'\dfrac{\sqrt{9x^2+1}}{2x-5}')), m(L(PI, r'\dfrac{\sqrt{x^3+x}}{x+4}')), m(L(PI, r'\dfrac{\sqrt[3]{8x^3-1}}{x}')), m(L(MI, r'\left(3^x+1\right)')), m(L(MI, r'0{,}4^{x}')), m(L(PI, r'\left(\tfrac{5}{2}\right)^{-x}'))]),
     tasks(3, [r'$\lim\frac{3x}{2x}=\res{\frac32}$', r'$\lim\frac{x^{3/2}}{x}=\lim\sqrt x=\res{+\infty}$', r'$\lim\frac{2x}{x}=\res{2}$', r'$3^{-\infty}+1=\res{1}$', r'$0{,}4^{-\infty}=\res{+\infty}$', r'$\left(\tfrac52\right)^{-\infty}=\res{0}$'])),
 (3, r"Calcula $%s$ i $%s$. Per què no donen el mateix?" % (L(PI, r'\dfrac{6x+1}{\sqrt{4x^2+3}}'), L(MI, r'\dfrac{6x+1}{\sqrt{4x^2+3}}')),
     r"$\sqrt{4x^2+3}\approx\sqrt{4x^2}=2|x|$. \ Quan $x\to+\infty$, $|x|=x$: \ $\lim\frac{6x}{2x}=\res{3}$. \ Quan $x\to-\infty$, $|x|=-x$: \ $\lim\frac{6x}{-2x}=\res{-3}$. L'arrel sempre és positiva, mentre que el numerador canvia de signe."),
 (3, r"\textbf{Repàs.} Calcula els límits següents. Compte amb el signe de $x$ quan $x\to-\infty$ i amb el domini de cada funció:" + tasks(2, [m(L(MI, r'\dfrac{\sqrt{x^4+1}}{2x^2-1}')), m(L(MI, r'\dfrac{\sqrt{x^2-5x+3}}{3x-2}')), m(L(MI, r'\left(\sqrt{x+1}-\sqrt{x+2}\right)')), m(L(MI, r'\dfrac{\sqrt{x^3-5x+3}}{x^2-2x}'))]),
     tasks(2, [r'$\lim\frac{x^2}{2x^2}=\res{\frac12}$', r'$\sqrt{x^2}=|x|=-x$: \ $\lim\frac{-x}{3x}=\res{-\frac13}$', r'Només està definida per a $x\geq-1$: \ $\res{\nexists}$', r'Si $x\to-\infty$, $x^3-5x+3<0$: l\'arrel no existeix, $\res{\nexists}$'.replace("l\\'", "l’")])),
]))

S.append(("Comparació d'infinits", [
 (1, r"Ordena de menor a major ordre d'infinit (quan $x\to+\infty$): \quad $x^3,\ \ 2^x,\ \ \ln x,\ \ \sqrt{x},\ \ e^x,\ \ x^{10}$."
     + recorda(r"Quan $x\to+\infty$: \ logaritmes $\ll$ potències $\ll$ exponencials. Entre potències guanya l'exponent major i entre exponencials, la base major."),
     r"$\res{\ln x\ll\sqrt x\ll x^3\ll x^{10}\ll 2^x\ll e^x}$"),
 (2, r"Calcula els límits següents comparant infinits:" + tasks(3, [m(L(PI, r'\dfrac{x^3}{e^x}')), m(L(PI, r'\dfrac{2^x+x^4}{3\cdot2^x}')), m(L(PI, r'\dfrac{\ln x}{x^2}')), m(L(PI, r'\left(x^{10}-1{,}5^x\right)')), m(L(PI, r'\dfrac{e^x}{x^5+x}')), m(L(PI, r'\dfrac{3^x+2^x}{3^x-x^2}'))]),
     tasks(3, [r'$\res{0}$', r'$\lim\frac{2^x}{3\cdot2^x}=\res{\frac13}$', r'$\res{0}$', r'$\res{-\infty}$', r'$\res{+\infty}$', r'$\lim\frac{3^x}{3^x}=\res{1}$'])),
]))

S.append(("Indeterminacions", [
 (2, r"Indeterminació $\infty-\infty$ amb fraccions:" + tasks(3, [m(L(PI, r'\left(\dfrac{x^2}{x+1}-x\right)')), m(L(PI, r'\left(\dfrac{2x^2+1}{x-1}-2x\right)')), m(L(PI, r'\left(\dfrac{x^3}{x^2+1}-\dfrac{x^2}{x+1}\right)'))])
     + recorda(r"Si la indeterminació $\infty-\infty$ ve d'una resta de fraccions, \textbf{fem la resta} amb denominador comú i calculem el límit del resultat."),
     tasks(1, [r'$\dfrac{x^2-x(x+1)}{x+1}=\dfrac{-x}{x+1}\to\res{-1}$', r'$\dfrac{2x^2+1-2x(x-1)}{x-1}=\dfrac{2x+1}{x-1}\to\res{2}$', r'$\dfrac{x^3(x+1)-x^2(x^2+1)}{(x^2+1)(x+1)}=\dfrac{x^3-x^2}{x^3+x^2+x+1}\to\res{1}$'])),
 (2, r"Indeterminació $\infty-\infty$ amb arrels:" + tasks(2, [m(L(PI, r'\left(\sqrt{x^2+8x}-x\right)')), m(L(PI, r'\left(\sqrt{4x^2+x}-2x\right)')), m(L(PI, r'\left(\sqrt{x^2+3x}-\sqrt{x^2-x}\right)')), m(L(PI, r'\left(\sqrt{x^2+1}-3x\right)'))])
     + recorda(r"Multipliquem i dividim pel \textbf{conjugat}: $(\sqrt A-B)(\sqrt A+B)=A-B^2$. Abans, comprova si els termes principals es cancel·len: si no ho fan, no cal el conjugat."),
     tasks(1, [r'$\dfrac{8x}{\sqrt{x^2+8x}+x}\to\dfrac{8x}{2x}=\res{4}$', r'$\dfrac{x}{\sqrt{4x^2+x}+2x}\to\dfrac{x}{4x}=\res{\frac14}$', r'$\dfrac{4x}{\sqrt{x^2+3x}+\sqrt{x^2-x}}\to\dfrac{4x}{2x}=\res{2}$', r'$\sqrt{x^2+1}\approx x$, i $x-3x=-2x\to\res{-\infty}$ (no hi ha indeterminació real).'])),
 (2, r"Indeterminació $1^{\infty}$:" + tasks(3, [m(L(PI, r'\left(1+\dfrac5x\right)^{x}')), m(L(PI, r'\left(\dfrac{x+2}{x-1}\right)^{2x}')), m(L(PI, r'\left(\dfrac{2x-1}{2x+3}\right)^{x+1}')), m(L(PI, r'\left(\dfrac{x^2+3}{x^2-1}\right)^{x^2}')), m(L(PI, r'\left(\dfrac{3x+1}{x+2}\right)^{x}')), m(L(MI, r'\left(\dfrac{x-4}{x}\right)^{3x}'))])
     + recorda(r"Si $\lim f(x)=1$ i $\lim g(x)=\pm\infty$: \ $\lim f(x)^{g(x)}=e^{\lim\,(f(x)-1)\cdot g(x)}$. Si la base no tendeix a 1, no hi ha indeterminació."),
     tasks(2, [r'$e^{\lim\frac5x\cdot x}=\res{e^5}$', r'$e^{\lim\frac{3}{x-1}\cdot2x}=\res{e^6}$', r'$e^{\lim\frac{-4}{2x+3}(x+1)}=\res{e^{-2}}$', r'$e^{\lim\frac{4}{x^2-1}\cdot x^2}=\res{e^4}$', r'$3^{+\infty}=\res{+\infty}$ (no és $1^\infty$)', r'$e^{\lim\frac{-4}{x}\cdot3x}=\res{e^{-12}}$'])),
 (2, r"Indeterminació $\frac{\infty}{\infty}$ amb arrels:" + tasks(2, [m(L(PI, r'\dfrac{\sqrt{x^2+5}+3x}{2x-1}')), m(L(PI, r'\dfrac{\sqrt{x^4+1}-x}{x^2+3}'))]),
     tasks(2, [r'$\lim\frac{x+3x}{2x}=\res{2}$', r'$\lim\frac{x^2}{x^2}=\res{1}$'])),
 (2, r"\pau{Aragó, EvAU extraordinària 2020} Donada la funció" + dm(pw((r'\dfrac{3}{x+1}', 'x<-1'), (r'x^3-4x^2+2x-10', r'-1\leq x\leq4'), (r'\sqrt{4x^2-7x}-2x', 'x>4'))) + r"calcula $\displaystyle\lim_{x\to+\infty}f(x)$. (La continuïtat d'aquesta funció es demana a la secció 6.)",
     r"Per a $x>4$: $+\infty-\infty$. Pel conjugat: \ $\dfrac{4x^2-7x-4x^2}{\sqrt{4x^2-7x}+2x}=\dfrac{-7x}{\sqrt{4x^2-7x}+2x}\to\dfrac{-7x}{4x}=\res{-\frac74}$."),
 (2, r"\pau{Balears, PBAU extraordinària 2021} El nombre d'individus, en milions, d'una població ve determinat per la funció $P(t)=\dfrac{2+t+t^2}{t^2+2t+1}$, on $t\geq0$ mesura el nombre d'anys transcorreguts." + tasks(1, [r"Quina és la població inicial ($t=0$) i la població després de 5 anys?", "A partir de quin moment la població serà inferior a un milió d'individus?", "Amb el pas dels anys, cap a quin valor tendirà el nombre d'individus de la població?"]),
     tasks(1, [r"$P(0)=\res{2}$ milions; \ $P(5)=\frac{32}{36}=\frac89\approx\res{0{,}889}$ milions ($\approx888\,889$ individus).", r"$\frac{2+t+t^2}{(t+1)^2}<1\iff2+t+t^2<t^2+2t+1\iff t>1$: \ \rest{a partir del primer any}.", r"$\displaystyle\lim_{t\to+\infty}P(t)=\res{1}$: tendeix a \rest{un milió} d'individus."])),
 (2, r"\pau{Castella i Lleó, EBAU juny 2017} El benefici, en milers d'euros, d'una empresa transcorreguts $x$ mesos és" + dm(pw((r'20x^2-20x+32', r'0<x\leq1'), (r'\dfrac{90x-45}{x+8}+27', 'x>1'))) + "Determina el benefici de l'empresa a molt llarg termini.",
     r"$\displaystyle\lim_{x\to+\infty}\left(\frac{90x-45}{x+8}+27\right)=90+27=117$: \ el benefici s'acosta a \rest{117\,000\,€}."),
 (3, r"\pau{Catalunya, PAU setembre 2018} Se sap que la funció $f(x)=\dfrac{ax+b}{cx+1}$ passa pel punt $(2,-5)$ i que les rectes $x=1$ i $y=2$ són, respectivament, la seua asímptota vertical i horitzontal. Calcula $a$, $b$ i $c$.",
     r"Asímptota vertical $x=1$: el denominador s'anul·la en 1, $c+1=0\Rightarrow c=-1$. \ Horitzontal: $\displaystyle\lim_{x\to\pm\infty}\frac{ax+b}{cx+1}=\frac ac=2\Rightarrow a=-2$. \ Punt: $\frac{-4+b}{-2+1}=-5\Rightarrow b=9$. \ $\res{a=-2,\ b=9,\ c=-1}$: \ $f(x)=\frac{-2x+9}{1-x}$."),
 (2, r"\textbf{Repàs.} Calcula els límits següents quan $x\to-\infty$. Abans de res, comprova si de veritat hi ha una indeterminació:" + tasks(2, [m(L(MI, r'\left(\dfrac{x^2}{x-3}-\dfrac{x^2}{5-x}\right)')), m(L(MI, r'\left(\dfrac{3x^2}{x+1}-\dfrac{x^3}{x^2+1}\right)')), m(L(MI, r'\left(\sqrt{x^2+x}-\sqrt{x^2+1}\right)')), m(L(MI, r'\left(2x-\sqrt{x^2+x}\right)'))]),
     tasks(1, [r'$(-\infty)-(+\infty)=\res{-\infty}$: no hi ha indeterminació.', r'$(-\infty)-(-\infty)$, IND. \ $\dfrac{3x^2(x^2+1)-x^3(x+1)}{(x+1)(x^2+1)}=\dfrac{2x^4-x^3+3x^2}{x^3+x^2+x+1}\to\lim 2x=\res{-\infty}$', r'Conjugat: $\dfrac{x-1}{\sqrt{x^2+x}+\sqrt{x^2+1}}\to\dfrac{x}{2|x|}=\dfrac{x}{-2x}=\res{-\frac12}$', r'$(-\infty)-(+\infty)=\res{-\infty}$: no hi ha indeterminació.'])),
 (2, r"\textbf{Repàs.} Calcula:" + tasks(3, [m(L(MI, r'\left(\dfrac{3x+4}{2x+5}\right)^{x-1}')), m(L(MI, r'\left(\dfrac{2x+1}{2x-1}\right)^{x-1}')), m(L(MI, r'\left(\dfrac{x^2+1}{x^2-1}\right)^{\frac{x^2-4}{x-1}}'))]),
     tasks(1, [r'La base tendeix a $\frac32\neq1$: \ $\left(\frac32\right)^{-\infty}=\res{0}$', r'$1^{-\infty}$: \ $\frac{2x+1}{2x-1}-1=\frac{2}{2x-1}$; \ $\lim\frac{2(x-1)}{2x-1}=1\Rightarrow\res{e}$', r'$1^{-\infty}$: \ $\frac{x^2+1}{x^2-1}-1=\frac{2}{x^2-1}$; \ $\lim\frac{2(x^2-4)}{(x^2-1)(x-1)}=0\Rightarrow e^0=\res{1}$'])),
]))

S.append(("Límits en un punt i indeterminació 0/0", [
 (1, r"Torna a les gràfiques de $f$ i $g$ de l'exercici \ref{ex:g1} i calcula els límits següents, estudiant els límits laterals quan calga:" + tasks(3, [m(L('-1', 'f(x)')), m(L('1', 'f(x)')), m(L('0', 'f(x)')), m(L('-2', 'g(x)')), m(L('2', 'g(x)')), m(L('0', 'g(x)'))]),
     tasks(2, [r'$\lim_{x\to-1^-}f=+\infty$, \ $\lim_{x\to-1^+}f=-\infty$: \ $\res{\nexists}$', r'$\lim_{x\to1^-}f=\lim_{x\to1^+}f=+\infty$: \ $\res{+\infty}$', r'$\res{0}$', r'$\lim_{x\to-2^-}g=+\infty$, \ $\lim_{x\to-2^+}g=-\infty$: \ $\res{\nexists}$', r'$\lim_{x\to2^-}g=-\infty$, \ $\lim_{x\to2^+}g=+\infty$: \ $\res{\nexists}$', r'$\res{0}$'])),
 (1, r"\label{ex:g4}Donada la gràfica de la funció $f(x)$, calcula $\displaystyle\lim_{x\to+\infty}f(x)$, $\displaystyle\lim_{x\to-\infty}f(x)$ i $\displaystyle\lim_{x\to0}f(x)$.\par\smallskip{\centering " + G_SALT + r"\par}",
     r"$\displaystyle\lim_{x\to+\infty}f(x)=\res{1}$, \ $\displaystyle\lim_{x\to-\infty}f(x)=\res{+\infty}$. \ $\lim_{x\to0^-}f=-2$ i $\lim_{x\to0^+}f=2$: \ $\res{\nexists}\displaystyle\lim_{x\to0}f(x)$."),
 (1, r"Calcula els límits següents. Quan siga necessari, estudia els límits laterals:" + tasks(3, [m(L('2', r'(x^3-2x+1)')), m(L('-1', r'\dfrac{x^2+3}{x-1}')), m(L('3', r'\dfrac{2x}{x-3}')), m(L('0', r'\dfrac{x-1}{x^2}')), m(L('4^+', r'\sqrt{x-4}')), m(L('1', r'\dfrac{x+1}{(x-1)^3}'))])
     + recorda(r"Si en substituir ix $\frac{k}{0}$ amb $k\neq0$, el límit és infinit: estudiem el signe per l'esquerra i per la dreta."),
     tasks(3, [r'$8-4+1=\res{5}$', r'$\frac{4}{-2}=\res{-2}$', r'$\frac60$: \ $\res{-\infty}$ per l’esquerra, $\res{+\infty}$ per la dreta: $\nexists$', r'$\frac{-1}{0^+}$: \ $\res{-\infty}$ pels dos costats', r'$\sqrt{0^+}=\res{0}$', r'$\frac20$: \ $\res{-\infty}$ per l’esquerra, $\res{+\infty}$ per la dreta: $\nexists$'])),
 (2, r"Calcula $\displaystyle\lim_{x\to2}f(x)$ i $\displaystyle\lim_{x\to-1}f(x)$, si existeixen, per a" + dm(pw((r'x^2-3', 'x<-1'), (r'2x', r'-1\leq x<2'), (r'\dfrac{8}{x}', r'x\geq2'))),
     r"$x=2$: $\lim_{x\to2^-}2x=4$, $\lim_{x\to2^+}\frac8x=4\Rightarrow\res{\lim_{x\to2}f(x)=4}$. \ \ $x=-1$: $\lim_{x\to-1^-}(x^2-3)=-2$, $\lim_{x\to-1^+}2x=-2\Rightarrow\res{\lim_{x\to-1}f(x)=-2}$."),
 (2, r"Resol les indeterminacions $\frac00$ factoritzant:" + tasks(3, [m(L('3', r'\dfrac{x^2-5x+6}{x^2-9}')), m(L('2', r'\dfrac{x^3-8}{x-2}')), m(L('1', r'\dfrac{x^3-x^2-x+1}{x^2-1}')), m(L('1', r'\dfrac{x^4-1}{x^2-x}')), m(L('-3', r'\dfrac{x^2+3x}{x^2+6x+9}')), m(L('4', r'\dfrac{\sqrt{x+5}-3}{x-4}'))])
     + recorda(r"Si $P(a)=Q(a)=0$, tots dos són divisibles per $(x-a)$: factoritzem (Ruffini, identitats notables, factor comú), simplifiquem i tornem a substituir."),
     tasks(2, [r'$\frac{(x-2)(x-3)}{(x+3)(x-3)}=\frac{x-2}{x+3}\to\res{\frac16}$', r'$\frac{(x-2)(x^2+2x+4)}{x-2}\to\res{12}$', r'$\frac{(x-1)^2(x+1)}{(x-1)(x+1)}=x-1\to\res{0}$', r'$\frac{(x-1)(x+1)(x^2+1)}{x(x-1)}\to\frac{2\cdot2}{1}=\res{4}$', r'$\frac{x(x+3)}{(x+3)^2}=\frac{x}{x+3}\to\frac{-3}{0}$: \ $\res{+\infty}$ per l’esquerra i $\res{-\infty}$ per la dreta, $\nexists$', r'$\frac{(x+5)-9}{(x-4)(\sqrt{x+5}+3)}=\frac{1}{\sqrt{x+5}+3}\to\res{\frac16}$'])),
 (2, r"\textbf{Repàs.} Calcula els límits següents:" + tasks(3, [m(L('3', r'\dfrac{x-3}{x^3-5x^2+3x+9}')), m(L('2', r'\left(\dfrac{2}{x-2}-\dfrac{x+1}{x^2-2x}\right)')), m(L('2', r'\dfrac{x^2+x-6}{x^2-x-1}')), m(L('2', r'\left(\dfrac{x+2}{2x}\right)^{\frac{x^2-4}{x-1}}')), m(L('-1', r'\dfrac{x^3-2x^2+2x+5}{x^2-6x-7}')), m(L('2', r'\dfrac{2x^2+x-10}{x^3-3x^2+4}'))]),
     tasks(2, [r'$\frac00$: \ $\frac{x-3}{(x-3)^2(x+1)}=\frac{1}{(x-3)(x+1)}\to\frac10$: \ $\res{-\infty}$ per l’esquerra, $\res{+\infty}$ per la dreta, $\nexists$', r'$\frac{2x-(x+1)}{x(x-2)}=\frac{x-1}{x(x-2)}\to\frac10$: \ $\res{-\infty}$ per l’esquerra, $\res{+\infty}$ per la dreta, $\nexists$', r'$\frac{0}{1}=\res{0}$ \ (no hi ha indeterminació)', r'$1^{0}=\res{1}$ \ (no hi ha indeterminació)', r'Ruffini: $\frac{(x+1)(x^2-3x+5)}{(x+1)(x-7)}\to\frac{9}{-8}=\res{-\frac98}$', r'$\frac{(x-2)(2x+5)}{(x-2)^2(x+1)}=\frac{2x+5}{(x-2)(x+1)}\to\frac90$: \ $\res{-\infty}$ per l’esquerra, $\res{+\infty}$ per la dreta, $\nexists$'])),
]))

S.append(("Continuïtat en un punt. Funcions racionals", [
 (1, r"Torna a la gràfica de $f$ de l'exercici \ref{ex:g1}. Existeix $\displaystyle\lim_{x\to1}f(x)$? Per què la funció no és contínua en $x=1$? I la funció de l'exercici \ref{ex:g4}, és contínua en $x=0$? Justifica les respostes.",
     r"$\lim_{x\to1^-}f=\lim_{x\to1^+}f=+\infty$: el límit és $+\infty$ (no és un nombre) i $\nexists f(1)$: \rest{discontinuïtat asimptòtica}. \ A l'exercici \ref{ex:g4}: $f(0)=2$, laterals $-2$ i $2$: \rest{salt finit} en $x=0$."),
 (1, r"Estudia la continuïtat de cada funció en el punt indicat i, si és discontínua, digues de quin tipus és:" + tasks(2, [r'$f(x)=\dfrac{x^2-4}{x+2}$ \ en $x=-2$', r'$g(x)=\dfrac{3}{x-4}$ \ en $x=4$', r'$h(x)=\begin{cases}x^2+1&\text{si }x<0\\x+1&\text{si }x\geq0\end{cases}$ \ en $x=0$', r'$k(x)=\begin{cases}2x&\text{si }x\leq1\\x^2+3&\text{si }x>1\end{cases}$ \ en $x=1$'])
     + recorda(r"$f$ és contínua en $a$ si: \ 1) $\exists f(a)$; \ 2) $\exists\lim_{x\to a}f(x)$; \ 3) $\lim_{x\to a}f(x)=f(a)$. Tipus: evitable, de salt finit, de salt infinit i asimptòtica."),
     tasks(2, [r'$\nexists f(-2)$, $\lim(x-2)=-4$: \ \rest{evitable}', r'Laterals $-\infty$ i $+\infty$: \ \rest{asimptòtica}', r'$h(0)=1$, laterals $1$ i $1$: \ \rest{contínua}', r'$k(1)=2$, laterals $2$ i $4$: \ \rest{salt finit}'])),
 (2, r"Estudia la continuïtat de $f(x)=\dfrac{x^2+x-2}{x^2-4x+3}$ i classifica'n les discontinuïtats.",
     r"$x^2-4x+3=0\Rightarrow x=1,\ x=3$. \ $f(x)=\frac{(x-1)(x+2)}{(x-1)(x-3)}$. \ $x=1$: $\lim\frac{x+2}{x-3}=-\frac32$ \ $\Rightarrow$ \rest{evitable}. \ $x=3$: $\frac50$ \ $\Rightarrow$ \rest{asimptòtica}. Contínua en $\mathbb R-\{1,3\}$."),
 (2, r"\pau{Cantàbria, EBAU juliol 2019} Siga la funció $f(x)=\dfrac{x^2-x-12}{x^2-2x-15}$. En quins punts és discontínua? Es pot definir de nou aquesta funció per a evitar alguna discontinuïtat?",
     r"$x^2-2x-15=(x-5)(x+3)$ i $x^2-x-12=(x-4)(x+3)$: discontínua en $\res{x=-3}$ i $\res{x=5}$. \ En $x=-3$: $\lim\frac{x-4}{x-5}=\frac{-7}{-8}=\frac78$ \ (evitable): definint $\res{f(-3)=\frac78}$ deixa de ser discontínua. En $x=5$ ($\frac{1}{0}$) la discontinuïtat és asimptòtica i no es pot evitar."),
 (2, r"\pau{Cantàbria, EBAU ordinària 2020} Donada la funció $f(x)=\dfrac{2x+4}{x^2+5x+6}$:" + tasks(1, ["En quins punts és discontínua?", "Es pot definir de nou la funció per a evitar alguna discontinuïtat?", "Calcula els dos límits laterals en $x=-3$ i interpreta gràficament què passa al voltant d'aquest valor."]),
     tasks(1, [r"$x^2+5x+6=(x+2)(x+3)$: discontínua en $\res{x=-2}$ i $\res{x=-3}$.", r"$f(x)=\frac{2(x+2)}{(x+2)(x+3)}$; \ $\lim_{x\to-2}\frac{2}{x+3}=2$: \ definint $\res{f(-2)=2}$ s'evita la discontinuïtat de $x=-2$.", r"$\lim_{x\to-3^-}f(x)=\res{-\infty}$, \ $\lim_{x\to-3^+}f(x)=\res{+\infty}$: \ $x=-3$ és una asímptota vertical; la gràfica baixa per l'esquerra i puja per la dreta."])),
 (2, r"\pau{Navarra, EvAU ordinària 2021} Estudia la continuïtat de la funció $f(x)=\dfrac{x^2+4x+3}{2x-2}$ i, si escau, indica el tipus de discontinuïtat.",
     r"És racional: contínua excepte on $2x-2=0$, és a dir, en $x=1$. \ $\lim_{x\to1}f(x)=\frac{8}{0}$: \ $\lim_{x\to1^-}=-\infty$, \ $\lim_{x\to1^+}=+\infty$. \ Contínua en $\mathbb R-\{1\}$; en $x=1$, \rest{discontinuïtat asimptòtica} (inevitable, de salt infinit segons la terminologia de Navarra)."),
]))

S.append(("Continuïtat de funcions a trossos", [
 (1, r"\pau{Navarra, EvAU extraordinària 2021} Estudia la continuïtat de la funció" + dm(pw((r'x^2-2x', r'x\leq2'), (r'-x^2+6x-8', 'x>2')))
     + recorda(r"Primer estudiem la continuïtat de cada tros per separat i després mirem els punts on la funció es trenca: $f(a)$, $\lim_{x\to a^-}f$ i $\lim_{x\to a^+}f$."),
     r"Trossos polinòmics: continus. \ En $x=2$: $f(2)=0$, \ $\lim_{x\to2^-}(x^2-2x)=0$, \ $\lim_{x\to2^+}(-x^2+6x-8)=0$. \ \rest{Contínua en tot $\mathbb R$}."),
 (2, r"\pau{Castella i Lleó, EBAU setembre 2017} Estudia raonadament la continuïtat de" + dm(pw((r'\dfrac{1}{4-x^2}', r'0<x<2'), (r'2x', r'2\leq x<4'))),
     r"El primer tros no està definit en $x=\pm2$, que no són de $(0,2)$: continu. \ En $x=2$: $f(2)=4$, \ $\lim_{x\to2^-}\frac{1}{4-x^2}=\frac{1}{0^+}=+\infty$, \ $\lim_{x\to2^+}2x=4$. \ Contínua en $\res{(0,2)\cup(2,4)}$; en $x=2$, \rest{salt infinit}."),
 (2, r"\pau{Madrid, EvAU juny 2018} Estudia si és contínua en $x=2$ la funció" + dm(pw((r'\dfrac{x+2}{x-1}', r'x\leq2'), (r'\dfrac{3x^2-2x}{x+2}', 'x>2'))) + r"Estudia'n també la continuïtat en tot $\mathbb R$.",
     r"$f(2)=\frac41=4$, \ $\lim_{x\to2^-}f=4$, \ $\lim_{x\to2^+}f=\frac{12-4}{4}=2$: \ \rest{no és contínua en $x=2$} (salt finit). \ A més, el primer tros no existeix en $x=1$ ($\frac30$): \rest{asimptòtica en $x=1$}. ($x=-2$ no és de $x>2$.) \ Contínua en $\mathbb R-\{1,2\}$."),
 (2, r"\pau{Madrid, EvAU juliol 2018} Determina el domini de $f$ i estudia'n la continuïtat:" + dm(pw((r'x^3+2e^x', 'x<0'), (r'\dfrac{2}{3+x}', r'x\geq0'))),
     r"El denominador $3+x$ s'anul·la en $-3$, que no és de $x\geq0$: domini $\res{\mathbb R}$. \ En $x=0$: $f(0)=\frac23$, \ $\lim_{x\to0^-}(x^3+2e^x)=2$, \ $\lim_{x\to0^+}\frac{2}{3+x}=\frac23$: \ salt finit. \ Contínua en $\res{\mathbb R-\{0\}}$."),
 (2, r"\pau{Aragó, EvAU extraordinària 2020} Estudia la continuïtat de" + dm(pw((r'\dfrac{3}{x+1}', 'x<-1'), (r'x^3-4x^2+2x-10', r'-1\leq x\leq4'), (r'\sqrt{4x^2-7x}-2x', 'x>4'))),
     r"Trossos: el primer, continu en $x<-1$; el segon, polinòmic; el tercer, $4x^2-7x=x(4x-7)>0$ si $x>4$: continu. \ $x=-1$: $\lim_{x\to-1^-}\frac{3}{x+1}=-\infty$, $\lim_{x\to-1^+}=-1-4-2-10=-17=f(-1)$: \ salt infinit. \ $x=4$: $f(4)=64-64+8-10=-2$, $\lim_{x\to4^+}=\sqrt{36}-8=-2$: contínua. \ \rest{Contínua en $\mathbb R-\{-1\}$}."),
 (3, r"\pau{Madrid, EvAU juny 2019} Analitza la continuïtat de la funció en tot el seu domini segons els valors de $k$:" + dm(pw((r'e^x+k', r'x\leq0'), (r'1-x^2', r'0<x\leq3'), (r'\dfrac{1}{x-3}', 'x>3'))),
     r"$x=0$: $f(0)=\lim_{x\to0^-}f=1+k$, \ $\lim_{x\to0^+}(1-x^2)=1$: contínua només si $k=0$. \ $x=3$: $f(3)=-8$, \ $\lim_{x\to3^+}\frac{1}{x-3}=+\infty$: sempre discontínua (salt infinit). \ \rest{Si $k=0$, contínua en $\mathbb R-\{3\}$; si $k\neq0$, contínua en $\mathbb R-\{0,3\}$}."),
 (2, r"\textbf{Repàs.} Estudia la continuïtat de les funcions següents en el seu domini:" + tasks(2, ['$' + pw((r'1', 'x<0'), (r'x+1', r'0<x<1'), (r'x^2-2x', r'1\leq x')) + '$', '$' + pw((r'3x-x^2', r'x\leq3'), (r'x-3', r'3<x<6'), (r'0', r'x\geq6'), name='g(x)') + '$']),
     tasks(1, [r"$f$: \ $x=0$: $\nexists f(0)$ i els laterals valen $1$ i $1$: \rest{evitable}. \ $x=1$: $f(1)=-1$, $\lim_{x\to1^-}f=2$: \rest{salt finit}. Contínua en $\mathbb R-\{0,1\}$.", r"$g$: \ $x=3$: $g(3)=0$, $\lim_{x\to3^+}g=0$: contínua. \ $x=6$: $\lim_{x\to6^-}g=3$, $g(6)=0$: \rest{salt finit}. Contínua en $\mathbb R-\{6\}$."])),
]))

S.append(("Funcions a trossos amb paràmetres", [
 (1, r"\pau{Madrid, EvAU setembre 2017} Calcula el valor del paràmetre real $a$ perquè $f$ siga contínua en tot el seu domini:" + dm(pw((r'ax+1', 'x<-1'), (r'x^2+x-2', r'x\geq-1')))
     + recorda(r"Igualem els límits laterals (i $f(a)$) en cada punt on canvia l'expressió. Amb dos paràmetres, obtenim un sistema."),
     r"$\lim_{x\to-1^-}(ax+1)=-a+1$, \ $\lim_{x\to-1^+}=f(-1)=1-1-2=-2$. \ $-a+1=-2\Rightarrow\res{a=3}$."),
 (1, r"\pau{Andalusia, PEvAU juny 2019} Determina el valor del paràmetre $a$ perquè $f$ siga contínua en tot el seu domini:" + dm(pw((r'\dfrac{1}{x-1}', 'x<0'), (r'x^2+a', r'x\geq0'))),
     r"El primer tros només falla en $x=1$, que no és de $x<0$. \ $\lim_{x\to0^-}\frac{1}{x-1}=-1$, \ $\lim_{x\to0^+}(x^2+a)=a=f(0)$ \ $\Rightarrow\res{a=-1}$."),
 (2, r"\pau{Castella-la Manxa, EvAU extraordinària 2020} Per a quin valor de $t$ és contínua en $x=0$ la funció" + dm(pw((r'x-t', r'x\leq0'), (r'(x-t)^2-5(x+t)+4', 'x>0'))),
     r"$f(0)=\lim_{x\to0^-}f=-t$, \ $\lim_{x\to0^+}f=t^2-5t+4$. \ $t^2-5t+4=-t\Rightarrow t^2-4t+4=0\Rightarrow(t-2)^2=0\Rightarrow\res{t=2}$."),
 (2, r"\pau{Castella-la Manxa, EvAU extraordinària 2020} Es considera la funció " + dm(pw((r'-4x+4', r'x\leq c'), (r'x^2-4x', 'x>c'))) + r"Per a quins valors de $c$ és contínua en $x=c$?",
     r"$f(c)=\lim_{x\to c^-}f=-4c+4$, \ $\lim_{x\to c^+}f=c^2-4c$. \ $c^2-4c=-4c+4\Rightarrow c^2=4\Rightarrow\res{c=-2\ \text{o}\ c=2}$."),
 (2, r"\pau{Balears, PBAU extraordinària 2021} Calculau els valors de $a$ perquè $f(x)$ sigui contínua:" + dm(pw((r'-4x+a', r'x\leq-2'), (r'x^2-5', r'-2<x<1'), (r'-7x+3', r'x\geq1'))),
     r"$x=-2$: $8+a=4-5=-1\Rightarrow\res{a=-9}$. \ $x=1$: $\lim_{x\to1^-}(x^2-5)=-4$ i $f(1)=\lim_{x\to1^+}(-7x+3)=-4$: contínua per a qualsevol $a$."),
 (2, r"\pau{Catalunya, PAU setembre 2018} Trobeu el valor de $a$ i $b$ perquè la funció sigui contínua per a tots els nombres reals:" + dm(pw((r'2x+3', r'x\leq-1'), (r'ax+b', r'-1<x<2'), (r'x^2', r'x\geq2'))),
     r"$x=-1$: $1=-a+b$. \ $x=2$: $2a+b=4$. \ Restant: $3a=3\Rightarrow\res{a=1,\ b=2}$."),
 (3, r"\pau{Aragó, EvAU setembre 2018} Calcula $a$ i $b$ sabent que $f$ és contínua en tots els punts:" + dm(pw((r'ax+1', 'x<-2'), (r'\dfrac{x+b}{x^2+1}', r'-2\leq x<0'), (r'x^3-9x^2+24x+4', r'x\geq0'))),
     r"$x=0$: $\lim_{x\to0^-}\frac{x+b}{x^2+1}=b$, \ $f(0)=4\Rightarrow b=4$. \ $x=-2$: $-2a+1=\frac{-2+4}{5}=\frac25\Rightarrow\res{a=\frac{3}{10},\ b=4}$."),
 (3, r"\pau{Cantàbria, EBAU ordinària 2020} Determina els valors de $a$ i $b$ per als quals la funció és contínua en $x=-1$ i en $x=3$:" + dm(pw((r'ax^2+2x-1', r'x\leq-1'), (r'x^2-5', r'-1<x\leq3'), (r'\dfrac{b+x}{3x-2}', 'x>3'))),
     r"$x=-1$: $a-2-1=1-5\Rightarrow a-3=-4\Rightarrow a=-1$. \ $x=3$: $f(3)=4=\frac{b+3}{7}\Rightarrow b=25$. \ $\res{a=-1,\ b=25}$ \ ($3x-2=0$ en $x=\frac23$, fora de $x>3$)."),
 (3, r"\pau{Cantàbria, EBAU juliol 2019} Determina els valors de $a$ i $b$ per als quals la funció és contínua en $x=-2$ i en $x=0$:" + dm(pw((r'-6x+3', r'-4<x<-2'), (r'x^2+ax+5', r'-2\leq x<0'), (r'\dfrac{x+15}{x+b}', r'0\leq x<3'))),
     r"$x=-2$: $15=4-2a+5\Rightarrow a=-3$. \ $x=0$: $5=\frac{15}{b}\Rightarrow b=3$. \ $\res{a=-3,\ b=3}$ \ (amb $b=3$ el denominador $x+3$ no s'anul·la en $[0,3)$)."),
 (2, r"\textbf{Repàs.} Donada la funció" + dm(pw((r'-\dfrac{1}{x^2}', 'x<1'), (r'x^2+ax', r'x\geq1'))) + tasks(1, ["Calcula el valor de $a$ perquè la funció siga contínua en $x=1$.", "Per al valor de $a$ obtingut, estudia la continuïtat de la funció en el seu domini."]),
     tasks(1, [r"$\lim_{x\to1^-}\left(-\frac{1}{x^2}\right)=-1$, \ $f(1)=1+a$ \ $\Rightarrow\res{a=-2}$.", r"El primer tros no està definit en $x=0$: $\lim_{x\to0}\left(-\frac{1}{x^2}\right)=-\infty$ pels dos costats, \rest{asimptòtica}. Contínua en $\mathbb R-\{0\}$."])),
 (3, r"\textbf{Repàs.} Calcula els valors dels paràmetres $a$ i $b$ perquè les funcions següents siguen contínues en el seu domini:" + tasks(2, ['$' + pw((r'\dfrac{1}{x^2}+a', r'x\leq-1'), (r'3x^2+4', r'-1<x<1'), (r'-x^2+b', r'x\geq1')) + '$', '$' + pw((r'-2x+a', r'x\leq-2'), (r'x^2-5', r'-2<x<1'), (r'bx+3', r'1\leq x'), name='g(x)') + '$']),
     tasks(1, [r"$f$: \ $x=-1$: $1+a=7\Rightarrow a=6$; \ $x=1$: $7=-1+b\Rightarrow b=8$. \ $\res{a=6,\ b=8}$ ($x=0$ no és de $x\leq-1$).", r"$g$: \ $x=-2$: $4+a=-1\Rightarrow a=-5$; \ $x=1$: $-4=b+3\Rightarrow b=-7$. \ $\res{a=-5,\ b=-7}$."])),
]))

# ---------- comprovacions numèriques ----------
def lim(f, a, side=1):
    """Estimació: a pot ser ±inf; es queda amb el valor més estable."""
    if math.isinf(a): xs = [math.copysign(10 ** k, a) for k in (3, 4, 5, 6)]
    else: xs = [a + side * 10 ** -k for k in (4, 5, 6, 7)]
    v = []
    for x in xs:
        try: v.append(f(x))
        except (OverflowError, ZeroDivisionError, ValueError): pass
    return v[-1] if abs(v[-1]) > 1e7 or abs(v[-1] - v[-2]) < 1e-3 * (1 + abs(v[-1])) else v[-2]
def ok(f, a, exp, side=1, tol=2e-3):
    r = lim(f, a, side)
    if math.isinf(exp): return (r > 1e5) if exp > 0 else (r < -1e5)
    return abs(r - exp) <= tol * (1 + abs(exp))
I, E, sq, e = math.inf, math.e, math.sqrt, math.exp
CHK = [
 (lambda x: sq(x**4+1)/(2*x*x-1), -I, .5), (lambda x: sq(x*x-5*x+3)/(3*x-2), -I, -1/3),
 (lambda x: x*x/(x-3)-x*x/(5-x), -I, -I), (lambda x: 3*x*x/(x+1)-x**3/(x*x+1), -I, -I), (lambda x: sq(x*x+x)-sq(x*x+1), -I, -.5), (lambda x: 2*x-sq(x*x+x), -I, -I),
 (lambda x: ((3*x+4)/(2*x+5))**(x-1), -I, 0), (lambda x: ((2*x+1)/(2*x-1))**(x-1), -I, E), (lambda x: ((x*x+1)/(x*x-1))**((x*x-4)/(x-1)), -I, 1),
 (lambda x: (x-3)/(x**3-5*x*x+3*x+9), 3, -I, -1), (lambda x: (x-3)/(x**3-5*x*x+3*x+9), 3, I, 1), (lambda x: 2/(x-2)-(x+1)/(x*x-2*x), 2, -I, -1), (lambda x: 2/(x-2)-(x+1)/(x*x-2*x), 2, I, 1),
 (lambda x: (x*x+x-6)/(x*x-x-1), 2, 0), (lambda x: ((x+2)/(2*x))**((x*x-4)/(x-1)), 2, 1), (lambda x: (x**3-2*x*x+2*x+5)/(x*x-6*x-7), -1, -9/8),
 (lambda x: (2*x*x+x-10)/(x**3-3*x*x+4), 2, -I, -1), (lambda x: (2*x*x+x-10)/(x**3-3*x*x+4), 2, I, 1), (lambda x: -1/x**2, 0, -I, -1), (lambda x: -1/x**2, 0, -I, 1),
 (lambda x: (2*x**3-x)/(5*x**3+4), I, .4), (lambda x: (4*x**4-x)/(3*x**2+1), -I, I), (lambda x: (1-3*x**2)/(x+2), -I, I), (lambda x: (7*x-2)/(3-x), I, -7),
 (lambda x: sq(9*x*x+1)/(2*x-5), I, 1.5), (lambda x: (8*x**3-1)**(1/3)/x, I, 2), (lambda x: (6*x+1)/sq(4*x*x+3), I, 3), (lambda x: (6*x+1)/sq(4*x*x+3), -I, -3),
 (lambda x: (2**x+x**4)/(3*2**x), 900, 1/3), (lambda x: (3**x+2**x)/(3**x-x*x), 600, 1),
 (lambda x: x*x/(x+1)-x, I, -1), (lambda x: (2*x*x+1)/(x-1)-2*x, I, 2), (lambda x: x**3/(x*x+1)-x*x/(x+1), I, 1),
 (lambda x: sq(x*x+8*x)-x, I, 4), (lambda x: sq(4*x*x+x)-2*x, I, .25), (lambda x: sq(x*x+3*x)-sq(x*x-x), I, 2), (lambda x: sq(x*x+1)-3*x, I, -I),
 (lambda x: (1+5/x)**x, I, E**5), (lambda x: ((x+2)/(x-1))**(2*x), I, E**6), (lambda x: ((2*x-1)/(2*x+3))**(x+1), I, E**-2), (lambda x: ((x*x+3)/(x*x-1))**(x*x), 1e3, E**4), (lambda x: ((x-4)/x)**(3*x), -I, E**-12),
 (lambda x: (sq(x*x+5)+3*x)/(2*x-1), I, 2), (lambda x: (sq(x**4+1)-x)/(x*x+3), I, 1), (lambda x: sq(4*x*x-7*x)-2*x, I, -1.75),
 (lambda t: (2+t+t*t)/(t*t+2*t+1), I, 1), (lambda x: (90*x-45)/(x+8)+27, I, 117),
 (lambda x: (x*x-5*x+6)/(x*x-9), 3, 1/6), (lambda x: (x**3-8)/(x-2), 2, 12), (lambda x: (x**3-x*x-x+1)/(x*x-1), 1, 0), (lambda x: (x**4-1)/(x*x-x), 1, 4),
 (lambda x: (x*x+3*x)/(x*x+6*x+9), -3, I, -1), (lambda x: (x*x+3*x)/(x*x+6*x+9), -3, -I, 1), (lambda x: (sq(x+5)-3)/(x-4), 4, 1/6),
 (lambda x: (x*x+x-2)/(x*x-4*x+3), 1, -1.5), (lambda x: (x*x-x-12)/(x*x-2*x-15), -3, 7/8), (lambda x: (2*x+4)/(x*x+5*x+6), -2, 2),
 (lambda x: (2*x+4)/(x*x+5*x+6), -3, -I, -1), (lambda x: (2*x+4)/(x*x+5*x+6), -3, I, 1), (lambda x: (x*x+4*x+3)/(2*x-2), 1, -I, -1),
 (lambda x: 1/(4-x*x), 2, I, -1), (lambda x: (3*x*x-2*x)/(x+2), 2, 2, 1), (lambda x: x**3+2*e(x), 0, 2, -1), (lambda x: 3/(x+1), -1, -I, -1),
]
for c in CHK:
    f, a, exp = c[:3]; side = c[3] if len(c) > 3 else 1
    assert ok(f, a, exp, side), (a, exp, lim(f, a, side))
# paràmetres: cada parella (esquerra, dreta) ha de coincidir
P = [(-3 + 1, 1 - 1 - 2), (1 / (0 - 1), -1), (-2, 2**2 - 5*2 + 4), (-4*2 + 4, 4 - 8), (-4*-2 + 4, 4 + 8), (8 - 9, 4 - 5), (2*-1 + 3, -1 + 2), (2*1 + 2, 4),
     (-2*.3 + 1, (-2 + 4) / 5), (-1*1 + 2*-1 - 1, 1 - 5), (9 - 5, (25 + 3) / 7), (-6*-2 + 3, 4 - 2*-3 + 5), (5, 15 / 3), (4, (0 + 4) / 1),
     (2*2 - 4, -4 + 12 - 8), (64 - 64 + 8 - 10, sq(64 - 28) - 8), (20 - 20 + 32, 45 / 9 + 27)]
P += [(-1, 1 - 2), (1 + 6, 3 + 4), (3 + 4, -1 + 8), (4 - 5, 4 - 5), (1 - 5, -7 + 3), (0 + 1, 1), (2, -1), (9 - 9, 0), (3, 0)][:5]
for l, r in P: assert abs(l - r) < 1e-12, (l, r)
assert abs((-2*2 + 9) / (-1*2 + 1) + 5) < 1e-12  # Catalunya 2018: passa per (2, -5)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={límits, límits a l'infinit, comparació d'infinits, indeterminacions, límits laterals, continuïtat, funcions a trossos, paràmetres, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 4: Límits i continuïtat. 2n de Batxillerat CCSS}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 4: Límits i continuïtat · 2n Batxillerat CCSS" % t)
    assert 'Unitat 4' in p and 'unitat 4' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\begin{document}
\thispagestyle{primera}

\begin{minipage}[c]{0.25\textwidth}\includegraphics[width=\linewidth]{logo-gva.png}\end{minipage}%
\begin{minipage}[c]{0.5\textwidth}\centering
  {\color{navy}\Large\bfseries ''' + ('Solucions de la fitxa de la unitat 4:' if sol else "Fitxa d'exercicis de la unitat 4:") + r'''\\[2pt] Límits i continuïtat}\\[5pt]
  {\color{accent}\large\bfseries 2n de Batxillerat CCSS}
\end{minipage}%
\begin{minipage}[c]{0.25\textwidth}\hfill\includegraphics[width=0.85\linewidth]{logo-vermellar.png}\end{minipage}

\vspace{6pt}
{\color{navy}\hrule height 1.2pt}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb la calculadora de límits dels apunts interactius de la unitat."
             if sol else r"Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes (traduïts al valencià). Resol-los al quadern mostrant tots els passos.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            lab = re.search(r'\\label\{[^}]*\}', q)
            if sol:
                head = re.sub(r'(\\pau\{[^}]*\}).*', r'\1', q, flags=re.S) if '\\pau{' in q else ''
                out.append('\\ex{%d} %s%s\n\n' % (st, (lab.group(0) if lab else '') + head, s))
            else:
                out.append('\\ex{%d} %s\n\n' % (st, q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb la calculadora de límits dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't4-fitxa-solucions.tex' if sol else 't4-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis,', sum(1 for _, ex in S for e in ex if '\\pau{' in e[1]), 'de la PAU d\'altres comunitats')
