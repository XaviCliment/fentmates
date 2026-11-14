# Versió en castellà de genera.py. Genera t4-fitxa-exercicis.tex i t4-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 4: Límits i continuïtat)
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
S.append(("Límites en el infinito", [
 (1, r"\label{ex:g1}Observa las gráficas de las funciones $f$ y $g$ y calcula, para cada una, el límite cuando $x\to+\infty$ y cuando $x\to-\infty$." + tasks(2, [r'$f(x)$:\par' + img('grafica1.jpg'), r'$g(x)$:\par' + img('grafica2.jpg')])
     + recorda(r"Para $x\to+\infty$ mira el \textbf{extremo derecho} de la gráfica; para $x\to-\infty$, el \textbf{extremo izquierdo}. Las rectas discontinuas son asíntotas."),
     tasks(2, [r'$\displaystyle\lim_{x\to+\infty}f(x)=\res{+\infty}$, \ $\displaystyle\lim_{x\to-\infty}f(x)=\res{0}$', r'$\displaystyle\lim_{x\to+\infty}g(x)=\res{2}$, \ $\displaystyle\lim_{x\to-\infty}g(x)=\res{2}$ \ (asíntota $y=2$)'])),
 (2, r"Lee en cada gráfica el límite cuando $x\to+\infty$ y cuando $x\to-\infty$. Fíjate bien en el dominio de cada función:" + tasks(3, ['a)\\par' + G_LN, 'b)\\par' + G_SQ, 'c)\\par' + G_SC]).replace('\\task a)\\par', '\\task ').replace('\\task b)\\par', '\\task ').replace('\\task c)\\par', '\\task '),
     tasks(1, [r"Dominio $(0,+\infty)$: \ $\displaystyle\lim_{x\to+\infty}=\res{+\infty}$; \ $\res{\nexists}\displaystyle\lim_{x\to-\infty}$ (la función no está definida para $x\leq0$).", r"Dominio $[-3,+\infty)$: \ $\displaystyle\lim_{x\to+\infty}=\res{+\infty}$; \ $\res{\nexists}\displaystyle\lim_{x\to-\infty}$.", r"Dominio $[-2,2]$: no llega a ningún infinito, $\res{\nexists}$ ninguno de los dos límites."])),
 (1, r"Calcula los límites siguientes:" + tasks(4, [m(L(PI, r'(3x^4-2x+7)')), m(L(MI, r'(-x^3+4x^2)')), m(L(MI, r'(2x^5-x^2)')), m(L(PI, r'(5-2x^2)'))])
     + recorda(r"El límite de un polinomio cuando $x\to\pm\infty$ es el de su \textbf{término de mayor grado}. Cuidado con el signo: $(-\infty)^{\text{par}}=+\infty$ y $(-\infty)^{\text{impar}}=-\infty$."),
     tasks(4, [r'$\lim 3x^4=\res{+\infty}$', r'$\lim(-x^3)=\res{+\infty}$', r'$\lim 2x^5=\res{-\infty}$', r'$\lim(-2x^2)=\res{-\infty}$'])),
 (1, r"Calcula comparando los grados del numerador y del denominador:" + tasks(3, [m(L(PI, r'\dfrac{2x^3-x}{5x^3+4}')), m(L(PI, r'\dfrac{x^2+1}{x^3-2}')), m(L(MI, r'\dfrac{4x^4-x}{3x^2+1}')), m(L(MI, r'\dfrac{1-3x^2}{x+2}')), m(L(PI, r'\dfrac{7x-2}{3-x}')), m(L(PI, r'\dfrac{x^5}{100x^4+1}'))])
     + recorda(r"$\displaystyle\lim_{x\to\pm\infty}\frac{P(x)}{Q(x)}=\lim_{x\to\pm\infty}\frac{a_nx^n}{b_mx^m}$: \ si $n>m$, $\pm\infty$; \ si $n=m$, $\frac{a_n}{b_m}$; \ si $n<m$, $0$."),
     tasks(3, [r'Mismo grado: $\res{\frac25}$', r'Grado de abajo mayor: $\res{0}$', r'$\lim\frac{4x^2}{3}=\res{+\infty}$', r'$\lim(-3x)=\res{+\infty}$', r'$\frac{7}{-1}=\res{-7}$', r'$\lim\frac{x}{100}=\res{+\infty}$'])),
 (2, r"Calcula los límites siguientes con raíces y exponenciales:" + tasks(3, [m(L(PI, r'\dfrac{\sqrt{9x^2+1}}{2x-5}')), m(L(PI, r'\dfrac{\sqrt{x^3+x}}{x+4}')), m(L(PI, r'\dfrac{\sqrt[3]{8x^3-1}}{x}')), m(L(MI, r'\left(3^x+1\right)')), m(L(MI, r'0{,}4^{x}')), m(L(PI, r'\left(\tfrac{5}{2}\right)^{-x}'))]),
     tasks(3, [r'$\lim\frac{3x}{2x}=\res{\frac32}$', r'$\lim\frac{x^{3/2}}{x}=\lim\sqrt x=\res{+\infty}$', r'$\lim\frac{2x}{x}=\res{2}$', r'$3^{-\infty}+1=\res{1}$', r'$0{,}4^{-\infty}=\res{+\infty}$', r'$\left(\tfrac52\right)^{-\infty}=\res{0}$'])),
 (3, r"Calcula $%s$ y $%s$. ¿Por qué no dan lo mismo?" % (L(PI, r'\dfrac{6x+1}{\sqrt{4x^2+3}}'), L(MI, r'\dfrac{6x+1}{\sqrt{4x^2+3}}')),
     r"$\sqrt{4x^2+3}\approx\sqrt{4x^2}=2|x|$. \ Cuando $x\to+\infty$, $|x|=x$: \ $\lim\frac{6x}{2x}=\res{3}$. \ Cuando $x\to-\infty$, $|x|=-x$: \ $\lim\frac{6x}{-2x}=\res{-3}$. La raíz siempre es positiva, mientras que el numerador cambia de signo."),
 (3, r"\textbf{Repaso.} Calcula los límites siguientes. Cuidado con el signo de $x$ cuando $x\to-\infty$ y con el dominio de cada función:" + tasks(2, [m(L(MI, r'\dfrac{\sqrt{x^4+1}}{2x^2-1}')), m(L(MI, r'\dfrac{\sqrt{x^2-5x+3}}{3x-2}')), m(L(MI, r'\left(\sqrt{x+1}-\sqrt{x+2}\right)')), m(L(MI, r'\dfrac{\sqrt{x^3-5x+3}}{x^2-2x}'))]),
     tasks(2, [r'$\lim\frac{x^2}{2x^2}=\res{\frac12}$', r'$\sqrt{x^2}=|x|=-x$: \ $\lim\frac{-x}{3x}=\res{-\frac13}$', r'Solo está definida para $x\geq-1$: \ $\res{\nexists}$', r'Si $x\to-\infty$, $x^3-5x+3<0$: la raíz no existe, $\res{\nexists}$'])),
]))

S.append(("Comparación de infinitos", [
 (1, r"Ordena de menor a mayor orden de infinito (cuando $x\to+\infty$): \quad $x^3,\ \ 2^x,\ \ \ln x,\ \ \sqrt{x},\ \ e^x,\ \ x^{10}$."
     + recorda(r"Cuando $x\to+\infty$: \ logaritmos $\ll$ potencias $\ll$ exponenciales. Entre potencias gana el exponente mayor y entre exponenciales, la base mayor."),
     r"$\res{\ln x\ll\sqrt x\ll x^3\ll x^{10}\ll 2^x\ll e^x}$"),
 (2, r"Calcula los límites siguientes comparando infinitos:" + tasks(3, [m(L(PI, r'\dfrac{x^3}{e^x}')), m(L(PI, r'\dfrac{2^x+x^4}{3\cdot2^x}')), m(L(PI, r'\dfrac{\ln x}{x^2}')), m(L(PI, r'\left(x^{10}-1{,}5^x\right)')), m(L(PI, r'\dfrac{e^x}{x^5+x}')), m(L(PI, r'\dfrac{3^x+2^x}{3^x-x^2}'))]),
     tasks(3, [r'$\res{0}$', r'$\lim\frac{2^x}{3\cdot2^x}=\res{\frac13}$', r'$\res{0}$', r'$\res{-\infty}$', r'$\res{+\infty}$', r'$\lim\frac{3^x}{3^x}=\res{1}$'])),
]))

S.append(("Indeterminaciones", [
 (2, r"Indeterminación $\infty-\infty$ con fracciones:" + tasks(3, [m(L(PI, r'\left(\dfrac{x^2}{x+1}-x\right)')), m(L(PI, r'\left(\dfrac{2x^2+1}{x-1}-2x\right)')), m(L(PI, r'\left(\dfrac{x^3}{x^2+1}-\dfrac{x^2}{x+1}\right)'))])
     + recorda(r"Si la indeterminación $\infty-\infty$ viene de una resta de fracciones, \textbf{hacemos la resta} con denominador común y calculamos el límite del resultado."),
     tasks(1, [r'$\dfrac{x^2-x(x+1)}{x+1}=\dfrac{-x}{x+1}\to\res{-1}$', r'$\dfrac{2x^2+1-2x(x-1)}{x-1}=\dfrac{2x+1}{x-1}\to\res{2}$', r'$\dfrac{x^3(x+1)-x^2(x^2+1)}{(x^2+1)(x+1)}=\dfrac{x^3-x^2}{x^3+x^2+x+1}\to\res{1}$'])),
 (2, r"Indeterminación $\infty-\infty$ con raíces:" + tasks(2, [m(L(PI, r'\left(\sqrt{x^2+8x}-x\right)')), m(L(PI, r'\left(\sqrt{4x^2+x}-2x\right)')), m(L(PI, r'\left(\sqrt{x^2+3x}-\sqrt{x^2-x}\right)')), m(L(PI, r'\left(\sqrt{x^2+1}-3x\right)'))])
     + recorda(r"Multiplicamos y dividimos por el \textbf{conjugado}: $(\sqrt A-B)(\sqrt A+B)=A-B^2$. Antes, comprueba si los términos principales se cancelan: si no lo hacen, no hace falta el conjugado."),
     tasks(1, [r'$\dfrac{8x}{\sqrt{x^2+8x}+x}\to\dfrac{8x}{2x}=\res{4}$', r'$\dfrac{x}{\sqrt{4x^2+x}+2x}\to\dfrac{x}{4x}=\res{\frac14}$', r'$\dfrac{4x}{\sqrt{x^2+3x}+\sqrt{x^2-x}}\to\dfrac{4x}{2x}=\res{2}$', r'$\sqrt{x^2+1}\approx x$, y $x-3x=-2x\to\res{-\infty}$ (no hay indeterminación real).'])),
 (2, r"Indeterminación $1^{\infty}$:" + tasks(3, [m(L(PI, r'\left(1+\dfrac5x\right)^{x}')), m(L(PI, r'\left(\dfrac{x+2}{x-1}\right)^{2x}')), m(L(PI, r'\left(\dfrac{2x-1}{2x+3}\right)^{x+1}')), m(L(PI, r'\left(\dfrac{x^2+3}{x^2-1}\right)^{x^2}')), m(L(PI, r'\left(\dfrac{3x+1}{x+2}\right)^{x}')), m(L(MI, r'\left(\dfrac{x-4}{x}\right)^{3x}'))])
     + recorda(r"Si $\lim f(x)=1$ y $\lim g(x)=\pm\infty$: \ $\lim f(x)^{g(x)}=e^{\lim\,(f(x)-1)\cdot g(x)}$. Si la base no tiende a 1, no hay indeterminación."),
     tasks(2, [r'$e^{\lim\frac5x\cdot x}=\res{e^5}$', r'$e^{\lim\frac{3}{x-1}\cdot2x}=\res{e^6}$', r'$e^{\lim\frac{-4}{2x+3}(x+1)}=\res{e^{-2}}$', r'$e^{\lim\frac{4}{x^2-1}\cdot x^2}=\res{e^4}$', r'$3^{+\infty}=\res{+\infty}$ (no es $1^\infty$)', r'$e^{\lim\frac{-4}{x}\cdot3x}=\res{e^{-12}}$'])),
 (2, r"Indeterminación $\frac{\infty}{\infty}$ con raíces:" + tasks(2, [m(L(PI, r'\dfrac{\sqrt{x^2+5}+3x}{2x-1}')), m(L(PI, r'\dfrac{\sqrt{x^4+1}-x}{x^2+3}'))]),
     tasks(2, [r'$\lim\frac{x+3x}{2x}=\res{2}$', r'$\lim\frac{x^2}{x^2}=\res{1}$'])),
 (2, r"\pau{Aragón, EvAU extraordinaria 2020} Dada la función" + dm(pw((r'\dfrac{3}{x+1}', 'x<-1'), (r'x^3-4x^2+2x-10', r'-1\leq x\leq4'), (r'\sqrt{4x^2-7x}-2x', 'x>4'))) + r"calcula $\displaystyle\lim_{x\to+\infty}f(x)$. (La continuidad de esta función se pide en la sección 6.)",
     r"Para $x>4$: $+\infty-\infty$. Por el conjugado: \ $\dfrac{4x^2-7x-4x^2}{\sqrt{4x^2-7x}+2x}=\dfrac{-7x}{\sqrt{4x^2-7x}+2x}\to\dfrac{-7x}{4x}=\res{-\frac74}$."),
 (2, r"\pau{Islas Baleares, PBAU extraordinaria 2021} El número de individuos, en millones, de una población viene determinado por la función $P(t)=\dfrac{2+t+t^2}{t^2+2t+1}$, donde $t\geq0$ mide el número de años transcurridos." + tasks(1, [r"¿Cuál es la población inicial ($t=0$) y la población después de 5 años?", "¿A partir de qué momento la población será inferior a un millón de individuos?", "Con el paso de los años, ¿hacia qué valor tenderá el número de individuos de la población?"]),
     tasks(1, [r"$P(0)=\res{2}$ millones; \ $P(5)=\frac{32}{36}=\frac89\approx\res{0{,}889}$ millones ($\approx888\,889$ individuos).", r"$\frac{2+t+t^2}{(t+1)^2}<1\iff2+t+t^2<t^2+2t+1\iff t>1$: \ \rest{a partir del primer año}.", r"$\displaystyle\lim_{t\to+\infty}P(t)=\res{1}$: tiende a \rest{un millón} de individuos."])),
 (2, r"\pau{Castilla y León, EBAU junio 2017} El beneficio, en miles de euros, de una empresa transcurridos $x$ meses es" + dm(pw((r'20x^2-20x+32', r'0<x\leq1'), (r'\dfrac{90x-45}{x+8}+27', 'x>1'))) + "Determina el beneficio de la empresa a muy largo plazo.",
     r"$\displaystyle\lim_{x\to+\infty}\left(\frac{90x-45}{x+8}+27\right)=90+27=117$: \ el beneficio se acerca a \rest{117\,000\,€}."),
 (3, r"\pau{Cataluña, PAU septiembre 2018} Se sabe que la función $f(x)=\dfrac{ax+b}{cx+1}$ pasa por el punto $(2,-5)$ y que las rectas $x=1$ e $y=2$ son, respectivamente, su asíntota vertical y horizontal. Calcula $a$, $b$ y $c$.",
     r"Asíntota vertical $x=1$: el denominador se anula en 1, $c+1=0\Rightarrow c=-1$. \ Horizontal: $\displaystyle\lim_{x\to\pm\infty}\frac{ax+b}{cx+1}=\frac ac=2\Rightarrow a=-2$. \ Punto: $\frac{-4+b}{-2+1}=-5\Rightarrow b=9$. \ $\res{a=-2,\ b=9,\ c=-1}$: \ $f(x)=\frac{-2x+9}{1-x}$."),
 (2, r"\textbf{Repaso.} Calcula los límites siguientes cuando $x\to-\infty$. Antes de nada, comprueba si de verdad hay una indeterminación:" + tasks(2, [m(L(MI, r'\left(\dfrac{x^2}{x-3}-\dfrac{x^2}{5-x}\right)')), m(L(MI, r'\left(\dfrac{3x^2}{x+1}-\dfrac{x^3}{x^2+1}\right)')), m(L(MI, r'\left(\sqrt{x^2+x}-\sqrt{x^2+1}\right)')), m(L(MI, r'\left(2x-\sqrt{x^2+x}\right)'))]),
     tasks(1, [r'$(-\infty)-(+\infty)=\res{-\infty}$: no hay indeterminación.', r'$(-\infty)-(-\infty)$, IND. \ $\dfrac{3x^2(x^2+1)-x^3(x+1)}{(x+1)(x^2+1)}=\dfrac{2x^4-x^3+3x^2}{x^3+x^2+x+1}\to\lim 2x=\res{-\infty}$', r'Conjugado: $\dfrac{x-1}{\sqrt{x^2+x}+\sqrt{x^2+1}}\to\dfrac{x}{2|x|}=\dfrac{x}{-2x}=\res{-\frac12}$', r'$(-\infty)-(+\infty)=\res{-\infty}$: no hay indeterminación.'])),
 (2, r"\textbf{Repaso.} Calcula:" + tasks(3, [m(L(MI, r'\left(\dfrac{3x+4}{2x+5}\right)^{x-1}')), m(L(MI, r'\left(\dfrac{2x+1}{2x-1}\right)^{x-1}')), m(L(MI, r'\left(\dfrac{x^2+1}{x^2-1}\right)^{\frac{x^2-4}{x-1}}'))]),
     tasks(1, [r'La base tiende a $\frac32\neq1$: \ $\left(\frac32\right)^{-\infty}=\res{0}$', r'$1^{-\infty}$: \ $\frac{2x+1}{2x-1}-1=\frac{2}{2x-1}$; \ $\lim\frac{2(x-1)}{2x-1}=1\Rightarrow\res{e}$', r'$1^{-\infty}$: \ $\frac{x^2+1}{x^2-1}-1=\frac{2}{x^2-1}$; \ $\lim\frac{2(x^2-4)}{(x^2-1)(x-1)}=0\Rightarrow e^0=\res{1}$'])),
]))

S.append(("Límites en un punto e indeterminación 0/0", [
 (1, r"Vuelve a las gráficas de $f$ y $g$ del ejercicio \ref{ex:g1} y calcula los límites siguientes, estudiando los límites laterales cuando sea necesario:" + tasks(3, [m(L('-1', 'f(x)')), m(L('1', 'f(x)')), m(L('0', 'f(x)')), m(L('-2', 'g(x)')), m(L('2', 'g(x)')), m(L('0', 'g(x)'))]),
     tasks(2, [r'$\lim_{x\to-1^-}f=+\infty$, \ $\lim_{x\to-1^+}f=-\infty$: \ $\res{\nexists}$', r'$\lim_{x\to1^-}f=\lim_{x\to1^+}f=+\infty$: \ $\res{+\infty}$', r'$\res{0}$', r'$\lim_{x\to-2^-}g=+\infty$, \ $\lim_{x\to-2^+}g=-\infty$: \ $\res{\nexists}$', r'$\lim_{x\to2^-}g=-\infty$, \ $\lim_{x\to2^+}g=+\infty$: \ $\res{\nexists}$', r'$\res{0}$'])),
 (1, r"\label{ex:g4}Dada la gráfica de la función $f(x)$, calcula $\displaystyle\lim_{x\to+\infty}f(x)$, $\displaystyle\lim_{x\to-\infty}f(x)$ y $\displaystyle\lim_{x\to0}f(x)$.\par\smallskip{\centering " + G_SALT + r"\par}",
     r"$\displaystyle\lim_{x\to+\infty}f(x)=\res{1}$, \ $\displaystyle\lim_{x\to-\infty}f(x)=\res{+\infty}$. \ $\lim_{x\to0^-}f=-2$ y $\lim_{x\to0^+}f=2$: \ $\res{\nexists}\displaystyle\lim_{x\to0}f(x)$."),
 (1, r"Calcula los límites siguientes. Cuando sea necesario, estudia los límites laterales:" + tasks(3, [m(L('2', r'(x^3-2x+1)')), m(L('-1', r'\dfrac{x^2+3}{x-1}')), m(L('3', r'\dfrac{2x}{x-3}')), m(L('0', r'\dfrac{x-1}{x^2}')), m(L('4^+', r'\sqrt{x-4}')), m(L('1', r'\dfrac{x+1}{(x-1)^3}'))])
     + recorda(r"Si al sustituir sale $\frac{k}{0}$ con $k\neq0$, el límite es infinito: estudiamos el signo por la izquierda y por la derecha."),
     tasks(3, [r'$8-4+1=\res{5}$', r'$\frac{4}{-2}=\res{-2}$', r'$\frac60$: \ $\res{-\infty}$ por la izquierda, $\res{+\infty}$ por la derecha: $\nexists$', r'$\frac{-1}{0^+}$: \ $\res{-\infty}$ por los dos lados', r'$\sqrt{0^+}=\res{0}$', r'$\frac20$: \ $\res{-\infty}$ por la izquierda, $\res{+\infty}$ por la derecha: $\nexists$'])),
 (2, r"Calcula $\displaystyle\lim_{x\to2}f(x)$ y $\displaystyle\lim_{x\to-1}f(x)$, si existen, para" + dm(pw((r'x^2-3', 'x<-1'), (r'2x', r'-1\leq x<2'), (r'\dfrac{8}{x}', r'x\geq2'))),
     r"$x=2$: $\lim_{x\to2^-}2x=4$, $\lim_{x\to2^+}\frac8x=4\Rightarrow\res{\lim_{x\to2}f(x)=4}$. \ \ $x=-1$: $\lim_{x\to-1^-}(x^2-3)=-2$, $\lim_{x\to-1^+}2x=-2\Rightarrow\res{\lim_{x\to-1}f(x)=-2}$."),
 (2, r"Resuelve las indeterminaciones $\frac00$ factorizando:" + tasks(3, [m(L('3', r'\dfrac{x^2-5x+6}{x^2-9}')), m(L('2', r'\dfrac{x^3-8}{x-2}')), m(L('1', r'\dfrac{x^3-x^2-x+1}{x^2-1}')), m(L('1', r'\dfrac{x^4-1}{x^2-x}')), m(L('-3', r'\dfrac{x^2+3x}{x^2+6x+9}')), m(L('4', r'\dfrac{\sqrt{x+5}-3}{x-4}'))])
     + recorda(r"Si $P(a)=Q(a)=0$, ambos son divisibles por $(x-a)$: factorizamos (Ruffini, identidades notables, factor común), simplificamos y volvemos a sustituir."),
     tasks(2, [r'$\frac{(x-2)(x-3)}{(x+3)(x-3)}=\frac{x-2}{x+3}\to\res{\frac16}$', r'$\frac{(x-2)(x^2+2x+4)}{x-2}\to\res{12}$', r'$\frac{(x-1)^2(x+1)}{(x-1)(x+1)}=x-1\to\res{0}$', r'$\frac{(x-1)(x+1)(x^2+1)}{x(x-1)}\to\frac{2\cdot2}{1}=\res{4}$', r'$\frac{x(x+3)}{(x+3)^2}=\frac{x}{x+3}\to\frac{-3}{0}$: \ $\res{+\infty}$ por la izquierda y $\res{-\infty}$ por la derecha, $\nexists$', r'$\frac{(x+5)-9}{(x-4)(\sqrt{x+5}+3)}=\frac{1}{\sqrt{x+5}+3}\to\res{\frac16}$'])),
 (2, r"\textbf{Repaso.} Calcula los límites siguientes:" + tasks(3, [m(L('3', r'\dfrac{x-3}{x^3-5x^2+3x+9}')), m(L('2', r'\left(\dfrac{2}{x-2}-\dfrac{x+1}{x^2-2x}\right)')), m(L('2', r'\dfrac{x^2+x-6}{x^2-x-1}')), m(L('2', r'\left(\dfrac{x+2}{2x}\right)^{\frac{x^2-4}{x-1}}')), m(L('-1', r'\dfrac{x^3-2x^2+2x+5}{x^2-6x-7}')), m(L('2', r'\dfrac{2x^2+x-10}{x^3-3x^2+4}'))]),
     tasks(2, [r'$\frac00$: \ $\frac{x-3}{(x-3)^2(x+1)}=\frac{1}{(x-3)(x+1)}\to\frac10$: \ $\res{-\infty}$ por la izquierda, $\res{+\infty}$ por la derecha, $\nexists$', r'$\frac{2x-(x+1)}{x(x-2)}=\frac{x-1}{x(x-2)}\to\frac10$: \ $\res{-\infty}$ por la izquierda, $\res{+\infty}$ por la derecha, $\nexists$', r'$\frac{0}{1}=\res{0}$ \ (no hay indeterminación)', r'$1^{0}=\res{1}$ \ (no hay indeterminación)', r'Ruffini: $\frac{(x+1)(x^2-3x+5)}{(x+1)(x-7)}\to\frac{9}{-8}=\res{-\frac98}$', r'$\frac{(x-2)(2x+5)}{(x-2)^2(x+1)}=\frac{2x+5}{(x-2)(x+1)}\to\frac90$: \ $\res{-\infty}$ por la izquierda, $\res{+\infty}$ por la derecha, $\nexists$'])),
]))

S.append(("Continuidad en un punto. Funciones racionales", [
 (1, r"Vuelve a la gráfica de $f$ del ejercicio \ref{ex:g1}. ¿Existe $\displaystyle\lim_{x\to1}f(x)$? ¿Por qué la función no es continua en $x=1$? Y la función del ejercicio \ref{ex:g4}, ¿es continua en $x=0$? Justifica las respuestas.",
     r"$\lim_{x\to1^-}f=\lim_{x\to1^+}f=+\infty$: el límite es $+\infty$ (no es un número) y $\nexists f(1)$: \rest{discontinuidad asintótica}. \ En el ejercicio \ref{ex:g4}: $f(0)=2$, laterales $-2$ y $2$: \rest{salto finito} en $x=0$."),
 (1, r"Estudia la continuidad de cada función en el punto indicado y, si es discontinua, di de qué tipo es:" + tasks(2, [r'$f(x)=\dfrac{x^2-4}{x+2}$ \ en $x=-2$', r'$g(x)=\dfrac{3}{x-4}$ \ en $x=4$', r'$h(x)=\begin{cases}x^2+1&\text{si }x<0\\x+1&\text{si }x\geq0\end{cases}$ \ en $x=0$', r'$k(x)=\begin{cases}2x&\text{si }x\leq1\\x^2+3&\text{si }x>1\end{cases}$ \ en $x=1$'])
     + recorda(r"$f$ es continua en $a$ si: \ 1) $\exists f(a)$; \ 2) $\exists\lim_{x\to a}f(x)$; \ 3) $\lim_{x\to a}f(x)=f(a)$. Tipos: evitable, de salto finito, de salto infinito y asintótica."),
     tasks(2, [r'$\nexists f(-2)$, $\lim(x-2)=-4$: \ \rest{evitable}', r'Laterales $-\infty$ y $+\infty$: \ \rest{asintótica}', r'$h(0)=1$, laterales $1$ y $1$: \ \rest{continua}', r'$k(1)=2$, laterales $2$ y $4$: \ \rest{salto finito}'])),
 (2, r"Estudia la continuidad de $f(x)=\dfrac{x^2+x-2}{x^2-4x+3}$ y clasifica sus discontinuidades.",
     r"$x^2-4x+3=0\Rightarrow x=1,\ x=3$. \ $f(x)=\frac{(x-1)(x+2)}{(x-1)(x-3)}$. \ $x=1$: $\lim\frac{x+2}{x-3}=-\frac32$ \ $\Rightarrow$ \rest{evitable}. \ $x=3$: $\frac50$ \ $\Rightarrow$ \rest{asintótica}. Continua en $\mathbb R-\{1,3\}$."),
 (2, r"\pau{Cantabria, EBAU julio 2019} Sea la función $f(x)=\dfrac{x^2-x-12}{x^2-2x-15}$. ¿En qué puntos es discontinua? ¿Se puede definir de nuevo esta función para evitar alguna discontinuidad?",
     r"$x^2-2x-15=(x-5)(x+3)$ y $x^2-x-12=(x-4)(x+3)$: discontinua en $\res{x=-3}$ y $\res{x=5}$. \ En $x=-3$: $\lim\frac{x-4}{x-5}=\frac{-7}{-8}=\frac78$ \ (evitable): definiendo $\res{f(-3)=\frac78}$ deja de ser discontinua. En $x=5$ ($\frac{1}{0}$) la discontinuidad es asintótica y no se puede evitar."),
 (2, r"\pau{Cantabria, EBAU ordinaria 2020} Dada la función $f(x)=\dfrac{2x+4}{x^2+5x+6}$:" + tasks(1, ["¿En qué puntos es discontinua?", "¿Se puede definir de nuevo la función para evitar alguna discontinuidad?", "Calcula los dos límites laterales en $x=-3$ e interpreta gráficamente qué ocurre alrededor de este valor."]),
     tasks(1, [r"$x^2+5x+6=(x+2)(x+3)$: discontinua en $\res{x=-2}$ y $\res{x=-3}$.", r"$f(x)=\frac{2(x+2)}{(x+2)(x+3)}$; \ $\lim_{x\to-2}\frac{2}{x+3}=2$: \ definiendo $\res{f(-2)=2}$ se evita la discontinuidad de $x=-2$.", r"$\lim_{x\to-3^-}f(x)=\res{-\infty}$, \ $\lim_{x\to-3^+}f(x)=\res{+\infty}$: \ $x=-3$ es una asíntota vertical; la gráfica baja por la izquierda y sube por la derecha."])),
 (2, r"\pau{Navarra, EvAU ordinaria 2021} Estudia la continuidad de la función $f(x)=\dfrac{x^2+4x+3}{2x-2}$ y, si procede, indica el tipo de discontinuidad.",
     r"Es racional: continua excepto donde $2x-2=0$, es decir, en $x=1$. \ $\lim_{x\to1}f(x)=\frac{8}{0}$: \ $\lim_{x\to1^-}=-\infty$, \ $\lim_{x\to1^+}=+\infty$. \ Continua en $\mathbb R-\{1\}$; en $x=1$, \rest{discontinuidad asintótica} (inevitable, de salto infinito según la terminología de Navarra)."),
]))

S.append(("Continuidad de funciones a trozos", [
 (1, r"\pau{Navarra, EvAU extraordinaria 2021} Estudia la continuidad de la función" + dm(pw((r'x^2-2x', r'x\leq2'), (r'-x^2+6x-8', 'x>2')))
     + recorda(r"Primero estudiamos la continuidad de cada trozo por separado y después miramos los puntos donde la función se parte: $f(a)$, $\lim_{x\to a^-}f$ y $\lim_{x\to a^+}f$."),
     r"Trozos polinómicos: continuos. \ En $x=2$: $f(2)=0$, \ $\lim_{x\to2^-}(x^2-2x)=0$, \ $\lim_{x\to2^+}(-x^2+6x-8)=0$. \ \rest{Continua en todo $\mathbb R$}."),
 (2, r"\pau{Castilla y León, EBAU septiembre 2017} Estudia razonadamente la continuidad de" + dm(pw((r'\dfrac{1}{4-x^2}', r'0<x<2'), (r'2x', r'2\leq x<4'))),
     r"El primer trozo no está definido en $x=\pm2$, que no son de $(0,2)$: continuo. \ En $x=2$: $f(2)=4$, \ $\lim_{x\to2^-}\frac{1}{4-x^2}=\frac{1}{0^+}=+\infty$, \ $\lim_{x\to2^+}2x=4$. \ Continua en $\res{(0,2)\cup(2,4)}$; en $x=2$, \rest{salto infinito}."),
 (2, r"\pau{Madrid, EvAU junio 2018} Estudia si es continua en $x=2$ la función" + dm(pw((r'\dfrac{x+2}{x-1}', r'x\leq2'), (r'\dfrac{3x^2-2x}{x+2}', 'x>2'))) + r"Estudia también su continuidad en todo $\mathbb R$.",
     r"$f(2)=\frac41=4$, \ $\lim_{x\to2^-}f=4$, \ $\lim_{x\to2^+}f=\frac{12-4}{4}=2$: \ \rest{no es continua en $x=2$} (salto finito). \ Además, el primer trozo no existe en $x=1$ ($\frac30$): \rest{asintótica en $x=1$}. ($x=-2$ no es de $x>2$.) \ Continua en $\mathbb R-\{1,2\}$."),
 (2, r"\pau{Madrid, EvAU julio 2018} Determina el dominio de $f$ y estudia su continuidad:" + dm(pw((r'x^3+2e^x', 'x<0'), (r'\dfrac{2}{3+x}', r'x\geq0'))),
     r"El denominador $3+x$ se anula en $-3$, que no es de $x\geq0$: dominio $\res{\mathbb R}$. \ En $x=0$: $f(0)=\frac23$, \ $\lim_{x\to0^-}(x^3+2e^x)=2$, \ $\lim_{x\to0^+}\frac{2}{3+x}=\frac23$: \ salto finito. \ Continua en $\res{\mathbb R-\{0\}}$."),
 (2, r"\pau{Aragón, EvAU extraordinaria 2020} Estudia la continuidad de" + dm(pw((r'\dfrac{3}{x+1}', 'x<-1'), (r'x^3-4x^2+2x-10', r'-1\leq x\leq4'), (r'\sqrt{4x^2-7x}-2x', 'x>4'))),
     r"Trozos: el primero, continuo en $x<-1$; el segundo, polinómico; el tercero, $4x^2-7x=x(4x-7)>0$ si $x>4$: continuo. \ $x=-1$: $\lim_{x\to-1^-}\frac{3}{x+1}=-\infty$, $\lim_{x\to-1^+}=-1-4-2-10=-17=f(-1)$: \ salto infinito. \ $x=4$: $f(4)=64-64+8-10=-2$, $\lim_{x\to4^+}=\sqrt{36}-8=-2$: continua. \ \rest{Continua en $\mathbb R-\{-1\}$}."),
 (3, r"\pau{Madrid, EvAU junio 2019} Analiza la continuidad de la función en todo su dominio según los valores de $k$:" + dm(pw((r'e^x+k', r'x\leq0'), (r'1-x^2', r'0<x\leq3'), (r'\dfrac{1}{x-3}', 'x>3'))),
     r"$x=0$: $f(0)=\lim_{x\to0^-}f=1+k$, \ $\lim_{x\to0^+}(1-x^2)=1$: continua solo si $k=0$. \ $x=3$: $f(3)=-8$, \ $\lim_{x\to3^+}\frac{1}{x-3}=+\infty$: siempre discontinua (salto infinito). \ \rest{Si $k=0$, continua en $\mathbb R-\{3\}$; si $k\neq0$, continua en $\mathbb R-\{0,3\}$}."),
 (2, r"\textbf{Repaso.} Estudia la continuidad de las funciones siguientes en su dominio:" + tasks(2, ['$' + pw((r'1', 'x<0'), (r'x+1', r'0<x<1'), (r'x^2-2x', r'1\leq x')) + '$', '$' + pw((r'3x-x^2', r'x\leq3'), (r'x-3', r'3<x<6'), (r'0', r'x\geq6'), name='g(x)') + '$']),
     tasks(1, [r"$f$: \ $x=0$: $\nexists f(0)$ y los laterales valen $1$ y $1$: \rest{evitable}. \ $x=1$: $f(1)=-1$, $\lim_{x\to1^-}f=2$: \rest{salto finito}. Continua en $\mathbb R-\{0,1\}$.", r"$g$: \ $x=3$: $g(3)=0$, $\lim_{x\to3^+}g=0$: continua. \ $x=6$: $\lim_{x\to6^-}g=3$, $g(6)=0$: \rest{salto finito}. Continua en $\mathbb R-\{6\}$."])),
]))

S.append(("Funciones a trozos con parámetros", [
 (1, r"\pau{Madrid, EvAU septiembre 2017} Calcula el valor del parámetro real $a$ para que $f$ sea continua en todo su dominio:" + dm(pw((r'ax+1', 'x<-1'), (r'x^2+x-2', r'x\geq-1')))
     + recorda(r"Igualamos los límites laterales (y $f(a)$) en cada punto donde cambia la expresión. Con dos parámetros, obtenemos un sistema."),
     r"$\lim_{x\to-1^-}(ax+1)=-a+1$, \ $\lim_{x\to-1^+}=f(-1)=1-1-2=-2$. \ $-a+1=-2\Rightarrow\res{a=3}$."),
 (1, r"\pau{Andalucía, PEvAU junio 2019} Determina el valor del parámetro $a$ para que $f$ sea continua en todo su dominio:" + dm(pw((r'\dfrac{1}{x-1}', 'x<0'), (r'x^2+a', r'x\geq0'))),
     r"El primer trozo solo falla en $x=1$, que no es de $x<0$. \ $\lim_{x\to0^-}\frac{1}{x-1}=-1$, \ $\lim_{x\to0^+}(x^2+a)=a=f(0)$ \ $\Rightarrow\res{a=-1}$."),
 (2, r"\pau{Castilla-La Mancha, EvAU extraordinaria 2020} Halla el valor de $t$ para el que es continua en $x=0$ la función" + dm(pw((r'x-t', r'x\leq0'), (r'(x-t)^2-5(x+t)+4', 'x>0'))),
     r"$f(0)=\lim_{x\to0^-}f=-t$, \ $\lim_{x\to0^+}f=t^2-5t+4$. \ $t^2-5t+4=-t\Rightarrow t^2-4t+4=0\Rightarrow(t-2)^2=0\Rightarrow\res{t=2}$."),
 (2, r"\pau{Castilla-La Mancha, EvAU extraordinaria 2020} Se considera la función " + dm(pw((r'-4x+4', r'x\leq c'), (r'x^2-4x', 'x>c'))) + r"¿Para qué valores de $c$ es continua en $x=c$?",
     r"$f(c)=\lim_{x\to c^-}f=-4c+4$, \ $\lim_{x\to c^+}f=c^2-4c$. \ $c^2-4c=-4c+4\Rightarrow c^2=4\Rightarrow\res{c=-2\ \text{o}\ c=2}$."),
 (2, r"\pau{Islas Baleares, PBAU extraordinaria 2021} Calcula los valores de $a$ para que $f(x)$ sea continua:" + dm(pw((r'-4x+a', r'x\leq-2'), (r'x^2-5', r'-2<x<1'), (r'-7x+3', r'x\geq1'))),
     r"$x=-2$: $8+a=4-5=-1\Rightarrow\res{a=-9}$. \ $x=1$: $\lim_{x\to1^-}(x^2-5)=-4$ y $f(1)=\lim_{x\to1^+}(-7x+3)=-4$: continua para cualquier $a$."),
 (2, r"\pau{Cataluña, PAU septiembre 2018} Halla el valor de $a$ y $b$ para que la función sea continua para todos los números reales:" + dm(pw((r'2x+3', r'x\leq-1'), (r'ax+b', r'-1<x<2'), (r'x^2', r'x\geq2'))),
     r"$x=-1$: $1=-a+b$. \ $x=2$: $2a+b=4$. \ Restando: $3a=3\Rightarrow\res{a=1,\ b=2}$."),
 (3, r"\pau{Aragón, EvAU septiembre 2018} Calcula $a$ y $b$ sabiendo que $f$ es continua en todos los puntos:" + dm(pw((r'ax+1', 'x<-2'), (r'\dfrac{x+b}{x^2+1}', r'-2\leq x<0'), (r'x^3-9x^2+24x+4', r'x\geq0'))),
     r"$x=0$: $\lim_{x\to0^-}\frac{x+b}{x^2+1}=b$, \ $f(0)=4\Rightarrow b=4$. \ $x=-2$: $-2a+1=\frac{-2+4}{5}=\frac25\Rightarrow\res{a=\frac{3}{10},\ b=4}$."),
 (3, r"\pau{Cantabria, EBAU ordinaria 2020} Determina los valores de $a$ y $b$ para los que la función es continua en $x=-1$ y en $x=3$:" + dm(pw((r'ax^2+2x-1', r'x\leq-1'), (r'x^2-5', r'-1<x\leq3'), (r'\dfrac{b+x}{3x-2}', 'x>3'))),
     r"$x=-1$: $a-2-1=1-5\Rightarrow a-3=-4\Rightarrow a=-1$. \ $x=3$: $f(3)=4=\frac{b+3}{7}\Rightarrow b=25$. \ $\res{a=-1,\ b=25}$ \ ($3x-2=0$ en $x=\frac23$, fuera de $x>3$)."),
 (3, r"\pau{Cantabria, EBAU julio 2019} Determina los valores de $a$ y $b$ para los que la función es continua en $x=-2$ y en $x=0$:" + dm(pw((r'-6x+3', r'-4<x<-2'), (r'x^2+ax+5', r'-2\leq x<0'), (r'\dfrac{x+15}{x+b}', r'0\leq x<3'))),
     r"$x=-2$: $15=4-2a+5\Rightarrow a=-3$. \ $x=0$: $5=\frac{15}{b}\Rightarrow b=3$. \ $\res{a=-3,\ b=3}$ \ (con $b=3$ el denominador $x+3$ no se anula en $[0,3)$)."),
 (2, r"\textbf{Repaso.} Dada la función" + dm(pw((r'-\dfrac{1}{x^2}', 'x<1'), (r'x^2+ax', r'x\geq1'))) + tasks(1, ["Calcula el valor de $a$ para que la función sea continua en $x=1$.", "Para el valor de $a$ obtenido, estudia la continuidad de la función en su dominio."]),
     tasks(1, [r"$\lim_{x\to1^-}\left(-\frac{1}{x^2}\right)=-1$, \ $f(1)=1+a$ \ $\Rightarrow\res{a=-2}$.", r"El primer trozo no está definido en $x=0$: $\lim_{x\to0}\left(-\frac{1}{x^2}\right)=-\infty$ por los dos lados, \rest{asintótica}. Continua en $\mathbb R-\{0\}$."])),
 (3, r"\textbf{Repaso.} Calcula los valores de los parámetros $a$ y $b$ para que las funciones siguientes sean continuas en su dominio:" + tasks(2, ['$' + pw((r'\dfrac{1}{x^2}+a', r'x\leq-1'), (r'3x^2+4', r'-1<x<1'), (r'-x^2+b', r'x\geq1')) + '$', '$' + pw((r'-2x+a', r'x\leq-2'), (r'x^2-5', r'-2<x<1'), (r'bx+3', r'1\leq x'), name='g(x)') + '$']),
     tasks(1, [r"$f$: \ $x=-1$: $1+a=7\Rightarrow a=6$; \ $x=1$: $7=-1+b\Rightarrow b=8$. \ $\res{a=6,\ b=8}$ ($x=0$ no es de $x\leq-1$).", r"$g$: \ $x=-2$: $4+a=-1\Rightarrow a=-5$; \ $x=1$: $-4=b+3\Rightarrow b=-7$. \ $\res{a=-5,\ b=-7}$."])),
]))

S.append(("Asíntotas", [
 (1, r"Calcula las asíntotas verticales y horizontales de las funciones siguientes. En cada asíntota vertical, estudia los límites laterales:" + tasks(3, [m(r'f(x)=\dfrac{3x+2}{x-1}'), m(r'f(x)=\dfrac{4}{x^2-16}'), m(r'f(x)=\dfrac{2x^2}{x^2+3}'), m(r'f(x)=\dfrac{x+1}{(x-2)^2}'), m(r'f(x)=\dfrac{1-x^2}{x^2+x-2}'), m(r'f(x)=\dfrac{x^2-9}{x+3}')])
     + recorda(r"AV $x=a$: si $\lim_{x\to a^\pm}f(x)=\pm\infty$ (en una racional, donde el límite da $\frac{k}{0}$, $k\neq0$; si da $\frac00$, simplificamos). AH $y=b$: si $\lim_{x\to\pm\infty}f(x)=b$."),
     tasks(1, [r"AV $\res{x=1}$ ($\lim_{x\to1^-}f=-\infty$, $\lim_{x\to1^+}f=+\infty$); \ AH $\res{y=3}$.",
               r"AV $\res{x=-4}$ ($+\infty$ por la izquierda, $-\infty$ por la derecha) y $\res{x=4}$ ($-\infty$ por la izquierda, $+\infty$ por la derecha); \ AH $\res{y=0}$.",
               r"Ninguna AV ($x^2+3\neq0$); \ AH $\res{y=2}$.",
               r"AV $\res{x=2}$ ($\frac{3}{0^+}$: $+\infty$ por los dos lados); \ AH $\res{y=0}$.",
               r"$x^2+x-2=(x-1)(x+2)$. En $x=1$: $\frac00$, $\frac{-(x-1)(x+1)}{(x-1)(x+2)}=\frac{-(x+1)}{x+2}\to-\frac23$: no hay AV. \ AV $\res{x=-2}$ ($\frac{-3}{0}$: $-\infty$ por la izquierda, $+\infty$ por la derecha); \ AH $\res{y=-1}$.",
               r"$\frac{(x+3)(x-3)}{x+3}=x-3$: en $x=-3$ hay un agujero, \rest{no tiene AV}. Grados $2>1$: \rest{no tiene AH} (la gráfica es la recta $y=x-3$ sin el punto $(-3,-6)$)."])),
 (2, r"Calcula las asíntotas horizontales de las funciones siguientes, cuando $x\to+\infty$ y cuando $x\to-\infty$:" + tasks(3, [m(r'f(x)=3^x+2'), m(r'f(x)=4-e^{-x}'), m(r'f(x)=\dfrac{6\cdot2^x}{2^x+1}')]),
     tasks(1, [r"$\lim_{x\to-\infty}(3^x+2)=0+2$: \ AH $\res{y=2}$ por la izquierda; por la derecha $+\infty$, no hay.",
               r"$\lim_{x\to+\infty}(4-e^{-x})=4-0$: \ AH $\res{y=4}$ por la derecha; por la izquierda $-\infty$, no hay.",
               r"$x\to+\infty$: $\lim\frac{6\cdot2^x}{2^x}=6$, \ AH $\res{y=6}$. \ $x\to-\infty$: $2^x\to0$, $\frac{0}{0+1}=0$, \ AH $\res{y=0}$. Tiene una AH diferente por cada lado."])),
 (2, r"Calcula las asíntotas oblicuas por el método del cociente y también las verticales. Estudia la posición de la gráfica respecto de la asíntota oblicua:" + tasks(2, [m(r'f(x)=\dfrac{x^2+2}{x-1}'), m(r'f(x)=\dfrac{3x^2-x}{x+2}'), m(r'f(x)=\dfrac{x^3+2}{x^2}'), m(r'f(x)=\dfrac{-x^2+4x}{x-3}')])
     + recorda(r"Si grado $P=$ grado $Q+1$, dividimos: $P(x)=Q(x)\cdot C(x)+R(x)\Rightarrow f(x)=C(x)+\dfrac{R(x)}{Q(x)}$. La asíntota oblicua es $y=C(x)$ y el signo de $\frac{R(x)}{Q(x)}$ nos dice si la gráfica queda por encima o por debajo."),
     tasks(1, [r"$x^2+2=(x-1)(x+1)+3$: \ AO $\res{y=x+1}$, \ AV $\res{x=1}$. \ $\frac{3}{x-1}>0$ si $x\to+\infty$ (por encima) y $<0$ si $x\to-\infty$ (por debajo).",
               r"$3x^2-x=(x+2)(3x-7)+14$: \ AO $\res{y=3x-7}$, \ AV $\res{x=-2}$. \ $\frac{14}{x+2}$: por encima cuando $x\to+\infty$ y por debajo cuando $x\to-\infty$.",
               r"$f(x)=x+\frac{2}{x^2}$: \ AO $\res{y=x}$, \ AV $\res{x=0}$ ($+\infty$ por los dos lados). \ $\frac{2}{x^2}>0$: siempre por encima.",
               r"$-x^2+4x=(x-3)(-x+1)+3$: \ AO $\res{y=-x+1}$, \ AV $\res{x=3}$. \ $\frac{3}{x-3}$: por encima cuando $x\to+\infty$ y por debajo cuando $x\to-\infty$."])),
 (2, r"Calcula todas las asíntotas de las funciones siguientes:" + tasks(3, [m(r'f(x)=\dfrac{x^2-x}{x^2-1}'), m(r'f(x)=\dfrac{x^3}{x^2-4}'), m(r'f(x)=\dfrac{x^3+1}{x-1}')]),
     tasks(1, [r"$\frac{x(x-1)}{(x-1)(x+1)}$: en $x=1$, $\frac x{x+1}\to\frac12$ (agujero, no es AV). \ AV $\res{x=-1}$; \ AH $\res{y=1}$.",
               r"AV $\res{x=-2}$ y $\res{x=2}$; \ $x^3=(x^2-4)\cdot x+4x$: \ AO $\res{y=x}$.",
               r"AV $\res{x=1}$. Grados 3 y 1: el cociente $x^2+x+1$ es de grado 2, \rest{no tiene AH ni AO}."])),
 (3, r"Dada la función $f(x)=\dfrac{ax^2+1}{x+b}$:" + tasks(1, [r"Calcula $a$ y $b$ para que $f$ tenga una asíntota vertical en $x=-2$ y una asíntota oblicua de pendiente $3$.", r"Para estos valores, ¿cuál es la ecuación de la asíntota oblicua?"]),
     tasks(1, [r"AV en $x=-2$: el denominador se anula en $-2$ $\Rightarrow\res{b=2}$ (el numerador $4a+1\neq0$). \ El cociente de $(ax^2+1):(x+2)$ empieza por $ax$: pendiente $\res{a=3}$.",
               r"$3x^2+1=(x+2)(3x-6)+13$: \ AO $\res{y=3x-6}$."])),
 (2, r"Las ventas de un nuevo producto, en miles de unidades, $t$ meses después del lanzamiento vienen dadas por $V(t)=\dfrac{50t}{t+4}$, con $t\geq0$." + tasks(1, [r"Calcula las ventas a los 6 meses.", r"Calcula $\displaystyle\lim_{t\to+\infty}V(t)$. ¿Qué asíntota tiene la función? Interprétala en el contexto del problema."]),
     tasks(1, [r"$V(6)=\frac{300}{10}=\res{30}$ miles de unidades.", r"$\displaystyle\lim_{t\to+\infty}\frac{50t}{t+4}=\res{50}$: AH $y=50$. A largo plazo las ventas se acercan a \rest{50\,000 unidades}, sin llegar a alcanzarlas."])),
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
 # asímptotes
 (lambda x: (3*x+2)/(x-1), 1, -I, -1), (lambda x: (3*x+2)/(x-1), 1, I), (lambda x: (3*x+2)/(x-1), I, 3),
 (lambda x: 4/(x*x-16), -4, I, -1), (lambda x: 4/(x*x-16), -4, -I), (lambda x: 4/(x*x-16), 4, -I, -1), (lambda x: 4/(x*x-16), 4, I), (lambda x: 4/(x*x-16), I, 0),
 (lambda x: 2*x*x/(x*x+3), I, 2), (lambda x: (x+1)/(x-2)**2, 2, I, -1), (lambda x: (x+1)/(x-2)**2, 2, I), (lambda x: (x+1)/(x-2)**2, I, 0),
 (lambda x: (1-x*x)/(x*x+x-2), 1, -2/3), (lambda x: (1-x*x)/(x*x+x-2), -2, -I, -1), (lambda x: (1-x*x)/(x*x+x-2), -2, I), (lambda x: (1-x*x)/(x*x+x-2), I, -1),
 (lambda x: (x*x-9)/(x+3), -3, -6), (lambda x: 3**x+2, -I, 2), (lambda x: 4-e(-x), I, 4), (lambda x: 6*2**x/(2**x+1), 900, 6), (lambda x: 6*2**x/(2**x+1), -900, 0),
 (lambda x: (x*x+2)/(x-1)-(x+1), I, 0), (lambda x: (3*x*x-x)/(x+2)-(3*x-7), I, 0), (lambda x: (x**3+2)/x**2-x, I, 0), (lambda x: (-x*x+4*x)/(x-3)-(-x+1), I, 0),
 (lambda x: (3*x*x-x)/(x+2), -2, -I, -1), (lambda x: (x**3+2)/x**2, 0, I, -1), (lambda x: (-x*x+4*x)/(x-3), 3, I),
 (lambda x: (x*x-x)/(x*x-1), 1, .5), (lambda x: (x*x-x)/(x*x-1), I, 1), (lambda x: (x*x-x)/(x*x-1), -1, I, -1), (lambda x: x**3/(x*x-4)-x, I, 0),
 (lambda x: (3*x*x+1)/(x+2)-(3*x-6), I, 0), (lambda t: 50*t/(t+4), I, 50),
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
# asímptotes obliqües: P = Q·C + R en uns quants valors de x
for x in (-3, 0.5, 2, 7):
    for P, Q, C, R in [(x*x+2, x-1, x+1, 3), (3*x*x-x, x+2, 3*x-7, 14), (-x*x+4*x, x-3, -x+1, 3), (x**3, x*x-4, x, 4*x), (3*x*x+1, x+2, 3*x-6, 13), (x**3+1, x-1, x*x+x+1, 2)]:
        assert abs(P - (Q*C + R)) < 1e-9, (x, P, Q, C, R)
assert abs(50*6/10 - 30) < 1e-12


# =====================================================================
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
assert 'refstepcounter{exer}' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Límites y continuidad"
KW = "límites, límites en el infinito, comparación de infinitos, indeterminaciones, límites laterales, continuidad, funciones a trozos, parámetros, asíntotas, PAU"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 4: %s' % (t, TIT), capcalera='%s · Unidad 4: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 4' if sol else 'Ficha de ejercicios · Unidad 4') + '}{' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con la calculadora de límites de los apuntes interactivos de la unidad."
             if sol else r"Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas. Resuélvelos en el cuaderno mostrando todos los pasos.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con la calculadora de límites de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't4-fitxa-solucions-es.tex' if sol else 't4-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios,', sum(1 for _, ex in S for e in ex if '\\pau{' in e[1]), 'de la PAU de otras comunidades')
