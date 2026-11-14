# Versió en castellà de genera.py. Genera t5-fitxa-exercicis.tex i t5-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 5: Càlcul de derivades.
# Derivabilitat d'una funció) a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Com a la unitat 4, els exercicis marcats amb \pau{...} són de la PAU d'altres comunitats (recopilació «Análisis en
# pruebas de acceso a la universidad de España» de www.ebaumatematicas.com), traduïts al valencià i reduïts als apartats
# d'aquesta unitat. Al final, DER comprova numèricament totes les derivades de les solucions i PAR els paràmetres.
# Ús: python3 genera.py && pdflatex t5-fitxa-exercicis.tex (dues vegades) && pdflatex t5-fitxa-solucions.tex
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def pw(*rows, name='f(x)'):
    return name + r'=\begin{cases}' + r'\\[3pt]'.join(r'%s&\text{si }%s' % r for r in rows) + r'\end{cases}'
def m(s): return '$' + s + '$'
def dm(s): return r'\[' + s + r'\]'
def fx(s, n='f'): return m(n + '(x)=' + s)

# ---------- gràfica de l'exercici de lectura ----------
def tzg(x0, x1, y0, y1, body, sc=0.62):
    g = r'\draw[muted!30,very thin] (%s,%s) grid (%s,%s);' % (x0, y0, x1, y1)
    g += r'\draw[-latex,thick] (%s,0)--(%s,0);\draw[-latex,thick] (0,%s)--(0,%s);' % (x0, x1 + 0.4, y0, y1 + 0.4)
    return r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]\begin{scope}%s\clip (%s,%s) rectangle (%s,%s);%s\end{scope}\end{tikzpicture}' % (sc, g, x0, y0, x1, y1, body)
def dot(x, y, o=False): return (r'\filldraw[fill=white,draw=accent,line width=1.1pt] (%s,%s) circle (0.13);' if o else r'\fill[accent] (%s,%s) circle (0.13);') % (x, y)
def tk(x, y, t, pos='below'): return r'\node[%s,font=\scriptsize] at (%s,%s) {$%s$};' % (pos, x, y, t)
G_LECT = tzg(-4, 5, -1, 4, r'\draw[accent,line width=1.5pt] (-4,1)--(-2,3)--(0,1);'
             + r'\draw[accent,line width=1.5pt,smooth,samples=60,domain=0:2] plot (\x,{1-\x+\x*\x/2});'
             + r'\draw[accent,line width=1.5pt] (2,3)--(5,3);' + dot(2, 1, True) + dot(2, 3)
             + tk(-2, 0, '-2') + tk(2, 0, '2') + tk(1, 0, '1') + tk(0, 1, '1', 'left') + tk(0, 3, '3', 'left'))

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Tasa de variación media e interpretación de la derivada", [
 (1, r"Calcula la tasa de variación media de $f(x)=x^2-4x+1$ en los intervalos siguientes:" + tasks(3, ['$[0,2]$', '$[1,4]$', '$[2,5]$'])
     + recorda(r"$\text{TVM}[a,b]=\dfrac{f(b)-f(a)}{b-a}$: es la pendiente de la recta secante que pasa por $(a,f(a))$ y $(b,f(b))$."),
     r"$f(0)=1,\ f(1)=-2,\ f(2)=-3,\ f(4)=1,\ f(5)=6$." + tasks(3, [r'$\frac{-3-1}{2}=\res{-2}$', r'$\frac{1-(-2)}{3}=\res{1}$', r'$\frac{6-(-3)}{3}=\res{3}$'])),
 (1, r"Calcula la TVM de $g(x)=\sqrt x$ en $[1,4]$ y en $[4,9]$. ¿En cuál de los dos intervalos crece más rápidamente la función?",
     r"$\text{TVM}[1,4]=\frac{2-1}{3}=\res{\frac13}$; \ $\text{TVM}[4,9]=\frac{3-2}{5}=\res{\frac15}$. Crece más rápidamente en \rest{$[1,4]$}."),
 (2, r"\label{ex:cost}El coste, en euros, de fabricar $x$ unidades de un producto es $C(x)=0{,}01x^2+5x+200$. Calcula la TVM del coste entre 100 y 200 unidades y entre 200 y 300 unidades. ¿Qué significan estos valores?",
     r"$C(100)=800$, $C(200)=1600$, $C(300)=2600$. \ $\text{TVM}[100,200]=\frac{800}{100}=\res{8}$ €/unidad; \ $\text{TVM}[200,300]=\frac{1000}{100}=\res{10}$ €/unidad: es el coste medio de cada unidad de más en cada tramo, y va aumentando."),
 (1, r"Responde a las preguntas siguientes:" + tasks(1, [r"Sabemos que $f(3)=2$ y $f'(3)=-4$. Escribe la ecuación de la recta tangente a la gráfica de $f$ en $x=3$.", r"La recta tangente a $g$ en $x=1$ es $y=-2x+7$. ¿Cuánto valen $g(1)$ y $g'(1)$?", r"Si $f'(a)=0$, ¿cómo es la recta tangente en $x=a$?"])
     + recorda(r"$f'(a)$ es la pendiente de la recta tangente en $x=a$. Recta tangente: $y-f(a)=f'(a)\,(x-a)$."),
     tasks(1, [r"$y-2=-4(x-3)\Rightarrow\res{y=-4x+14}$", r"$\res{g'(1)=-2}$ (pendiente) y $\res{g(1)=-2+7=5}$.", r"La pendiente es 0: la tangente es \rest{horizontal}, $y=f(a)$."])),
]))

S.append(("Derivada de una función por definición", [
 (2, r"Calcula, aplicando la definición de derivada:" + tasks(2, [r"$f'(1)$ si $f(x)=3x^2-x$", r"$f'(-1)$ si $f(x)=x^3-2x$", r"$f'(3)$ si $f(x)=\dfrac{2}{x-1}$", r"$f'(4)$ si $f(x)=\sqrt{2x+1}$"])
     + recorda(r"$f'(a)=\displaystyle\lim_{h\to0}\frac{f(a+h)-f(a)}{h}$. Simplifica $f(a+h)-f(a)$ hasta que aparezca el factor $h$; con raíces, multiplica por el conjugado."),
     tasks(1, [r"$\frac{3(1+h)^2-(1+h)-2}{h}=\frac{5h+3h^2}{h}=5+3h\to\res{5}$",
               r"$f(-1+h)=(-1+h)^3-2(-1+h)=1+h-3h^2+h^3$, \ $f(-1)=1$: \ $\frac{h-3h^2+h^3}{h}=1-3h+h^2\to\res{1}$",
               r"$\frac{\frac{2}{2+h}-1}{h}=\frac{\frac{-h}{2+h}}{h}=\frac{-1}{2+h}\to\res{-\frac12}$",
               r"$\frac{\sqrt{9+2h}-3}{h}=\frac{9+2h-9}{h(\sqrt{9+2h}+3)}=\frac{2}{\sqrt{9+2h}+3}\to\res{\frac13}$"])),
 (2, r"\pau{Navarra, EvAU extraordinaria 2023} Considera la función $g(x)=-x^2+4x+3$. Calcula la derivada de $g(x)$ en el punto $x=1$ aplicando la definición de derivada.",
     r"$g(1+h)=-(1+h)^2+4(1+h)+3=6+2h-h^2$, \ $g(1)=6$. \ $g'(1)=\displaystyle\lim_{h\to0}\frac{2h-h^2}{h}=\lim_{h\to0}(2-h)=\res{2}$."),
 (2, r"Calcula la función derivada aplicando la definición:" + tasks(3, [fx(r'x^2-3x+2'), fx(r'\dfrac{1}{x+2}'), fx(r'\sqrt x')]),
     tasks(1, [r"$\frac{(x+h)^2-3(x+h)+2-(x^2-3x+2)}{h}=\frac{2xh+h^2-3h}{h}=2x+h-3\to\res{2x-3}$",
               r"$\frac{\frac{1}{x+h+2}-\frac{1}{x+2}}{h}=\frac{-1}{(x+h+2)(x+2)}\to\res{-\frac{1}{(x+2)^2}}$",
               r"$\frac{\sqrt{x+h}-\sqrt x}{h}=\frac{1}{\sqrt{x+h}+\sqrt x}\to\res{\frac{1}{2\sqrt x}}$"])),
 (2, r"Calcula por definición la derivada de $f(x)=x^2$ en $x=3$ y escribe la ecuación de la recta tangente a la gráfica en ese punto.",
     r"$\frac{(3+h)^2-9}{h}=6+h\to f'(3)=6$. \ $f(3)=9$: \ $y-9=6(x-3)\Rightarrow\res{y=6x-9}$."),
]))

S.append(("Propiedades de la derivada: suma, producto y cociente", [
 (1, r"Deriva estas funciones polinómicas:" + tasks(2, [fx(r'5x^4-3x^3+2x-8'), fx(r'\dfrac{x^5}{5}-\dfrac{2x^3}{3}+x'), fx(r'\dfrac{3x^2-2x+1}{4}'), fx(r'-x^6+\dfrac x2-7')])
     + recorda(r"$(k)'=0$, \ $(x^n)'=n\,x^{n-1}$, \ $(f\pm g)'=f'\pm g'$, \ $(k\cdot f)'=k\cdot f'$."),
     tasks(2, [r'$\res{20x^3-9x^2+2}$', r'$\res{x^4-2x^2+1}$', r'$\frac{6x-2}{4}=\res{\frac{3x-1}{2}}$', r'$\res{-6x^5+\frac12}$'])),
 (1, r"Deriva aplicando la regla del producto y simplifica:" + tasks(3, [fx(r'(2x-1)(x^2+3)'), fx(r'(x^3+x)(1-x^2)'), fx(r'x^2(x-1)(x+1)')])
     + recorda(r"$(f\cdot g)'=f'\cdot g+f\cdot g'$. \ Cuidado: $(f\cdot g)'\neq f'\cdot g'$."),
     tasks(1, [r"$2(x^2+3)+(2x-1)\cdot2x=\res{6x^2-2x+6}$", r"$(3x^2+1)(1-x^2)+(x^3+x)(-2x)=\res{1-5x^4}$", r"$f(x)=x^4-x^2\Rightarrow\res{4x^3-2x}$"])),
 (2, r"Deriva aplicando la regla del cociente y simplifica:" + tasks(2, [fx(r'\dfrac{x+3}{x-2}'), fx(r'\dfrac{2x^2}{x+1}'), fx(r'\dfrac{x^2-1}{x^2+1}'), fx(r'\dfrac{3}{x^2-4}')])
     + recorda(r"$\left(\dfrac fg\right)'=\dfrac{f'\cdot g-f\cdot g'}{g^2}$. Simplifica el numerador, pero deja el denominador sin desarrollar."),
     tasks(2, [r"$\frac{(x-2)-(x+3)}{(x-2)^2}=\res{\frac{-5}{(x-2)^2}}$", r"$\frac{4x(x+1)-2x^2}{(x+1)^2}=\res{\frac{2x^2+4x}{(x+1)^2}}$",
               r"$\frac{2x(x^2+1)-(x^2-1)2x}{(x^2+1)^2}=\res{\frac{4x}{(x^2+1)^2}}$", r"$\res{\frac{-6x}{(x^2-4)^2}}$"])),
 (1, r"Dada $f(x)=x^4-2x^3+5x$, calcula $f'(x)$, $f''(x)$ y $f''(1)$.",
     r"$\res{f'(x)=4x^3-6x^2+5}$, \ $\res{f''(x)=12x^2-12x}$, \ $\res{f''(1)=0}$."),
 (2, r"El coste de fabricar $x$ unidades es $C(x)=0{,}01x^2+5x+200$ euros (ejercicio \ref{ex:cost}). Calcula el coste marginal $C'(x)$ y $C'(100)$. ¿Qué significa? Compáralo con la TVM del ejercicio \ref{ex:cost}.",
     r"$\res{C'(x)=0{,}02x+5}$, \ $\res{C'(100)=7}$: cuando ya se fabrican 100, fabricar una más cuesta aproximadamente 7 €. La TVM en $[100,200]$ (8 €) era una media de todo el tramo; la derivada mide el ritmo \emph{justo} en $x=100$."),
]))

S.append(("Derivadas de las funciones elementales", [
 (1, r"Escribe como potencia y deriva:" + tasks(3, [fx(r'\sqrt{x^3}'), fx(r'\dfrac{1}{x^2}'), fx(r'\sqrt[3]{x}'), fx(r'\dfrac{6}{\sqrt x}'), fx(r'x^2\sqrt x'), fx(r'\dfrac{2}{3x^3}')])
     + recorda(r"$\sqrt[n]{x^m}=x^{m/n}$ y $\dfrac{1}{x^n}=x^{-n}$. La regla $(x^n)'=n\,x^{n-1}$ vale para cualquier exponente."),
     tasks(3, [r'$x^{3/2}\to\res{\frac32\sqrt x}$', r'$x^{-2}\to\res{\frac{-2}{x^3}}$', r'$x^{1/3}\to\res{\frac{1}{3\sqrt[3]{x^2}}}$', r'$6x^{-1/2}\to\res{\frac{-3}{x\sqrt x}}$', r'$x^{5/2}\to\res{\frac52x\sqrt x}$', r'$\frac23x^{-3}\to\res{\frac{-2}{x^4}}$'])),
 (1, r"Deriva estas funciones exponenciales y logarítmicas:" + tasks(3, [fx(r'2e^x-3\ln x'), fx(r'4^x'), fx(r'\log_3x'), fx(r'x\,e^x'), fx(r'\dfrac{e^x}{x}'), fx(r'x^2\ln x')])
     + recorda(r"$(e^x)'=e^x$, \ $(a^x)'=a^x\ln a$, \ $(\ln x)'=\dfrac1x$, \ $(\log_ax)'=\dfrac{1}{x\ln a}$."),
     tasks(3, [r'$\res{2e^x-\frac3x}$', r'$\res{4^x\ln4}$', r'$\res{\frac{1}{x\ln3}}$', r'$e^x+xe^x=\res{(x+1)e^x}$', r'$\frac{e^xx-e^x}{x^2}=\res{\frac{e^x(x-1)}{x^2}}$', r'$\res{2x\ln x+x}$'])),
 (2, r"Deriva estas funciones trigonométricas:" + tasks(3, [fx(r'3\sin x-2\cos x'), fx(r'x\sin x'), fx(r'\tan x-x'), fx(r'\sin x\cos x'), fx(r'\arctan x-x'), fx(r'x\arcsin x')])
     + recorda(r"$(\sin x)'=\cos x$, \ $(\cos x)'=-\sin x$, \ $(\tan x)'=1+\tan^2x$, \ $(\arcsin x)'=\frac{1}{\sqrt{1-x^2}}$, \ $(\arctan x)'=\frac{1}{1+x^2}$."),
     tasks(2, [r'$\res{3\cos x+2\sin x}$', r'$\res{\sin x+x\cos x}$', r'$1+\tan^2x-1=\res{\tan^2x}$', r'$\res{\cos^2x-\sin^2x}$', r'$\frac{1}{1+x^2}-1=\res{\frac{-x^2}{1+x^2}}$', r'$\res{\arcsin x+\frac{x}{\sqrt{1-x^2}}}$'])),
]))

S.append(("Regla de la cadena", [
 (2, r"Deriva estas potencias y raíces de funciones:" + tasks(2, [fx(r'(3x^2-1)^4'), fx(r'\sqrt{x^2-2x}'), fx(r'\dfrac{1}{(x^2+1)^3}'), fx(r'\sqrt[3]{2x+5}')])
     + recorda(r"Regla de la cadena: $[f(g(x))]'=f'(g(x))\cdot g'(x)$. Por ejemplo, $[g^n]'=n\,g^{n-1}\cdot g'$ y $\left[\sqrt g\right]'=\dfrac{g'}{2\sqrt g}$."),
     tasks(2, [r'$4(3x^2-1)^3\cdot6x=\res{24x(3x^2-1)^3}$', r'$\frac{2x-2}{2\sqrt{x^2-2x}}=\res{\frac{x-1}{\sqrt{x^2-2x}}}$', r'$-3(x^2+1)^{-4}\cdot2x=\res{\frac{-6x}{(x^2+1)^4}}$', r'$\frac13(2x+5)^{-2/3}\cdot2=\res{\frac{2}{3\sqrt[3]{(2x+5)^2}}}$'])),
 (2, r"Deriva estas funciones compuestas exponenciales y logarítmicas:" + tasks(3, [fx(r'e^{3x-1}'), fx(r'2^{x^2}'), fx(r'\ln(x^2-3x)'), fx(r'\log(5x)'), fx(r'\ln\sqrt x'), fx(r'e^{\sqrt x}')])
     + recorda(r"$\left[e^{g}\right]'=e^{g}\cdot g'$, \ $\left[a^{g}\right]'=a^{g}\cdot g'\cdot\ln a$, \ $\left[\ln g\right]'=\dfrac{g'}{g}$. Antes de derivar un logaritmo, aplica sus propiedades si simplifican."),
     tasks(3, [r'$\res{3e^{3x-1}}$', r'$\res{2x\cdot2^{x^2}\ln2}$', r'$\res{\frac{2x-3}{x^2-3x}}$', r'$\frac{5}{5x\ln10}=\res{\frac{1}{x\ln10}}$', r'$\frac12\ln x\to\res{\frac{1}{2x}}$', r'$\res{\frac{e^{\sqrt x}}{2\sqrt x}}$'])),
 (2, r"Deriva estas funciones trigonométricas compuestas:" + tasks(3, [fx(r'\sin(5x+1)'), fx(r'\cos(x^2)'), fx(r'\tan(3x)'), fx(r'\sin^3x'), fx(r'\arctan(2x)'), fx(r'\arcsin(x^2)')]),
     tasks(3, [r'$\res{5\cos(5x+1)}$', r'$\res{-2x\sin(x^2)}$', r'$\res{\frac{3}{\cos^2(3x)}}$', r'$\res{3\sin^2x\cos x}$', r'$\res{\frac{2}{1+4x^2}}$', r'$\res{\frac{2x}{\sqrt{1-x^4}}}$'])),
 (2, r"Deriva y simplifica (hay más de una regla en cada función):" + tasks(2, [fx(r'x\,e^{-x^2}'), fx(r'\ln\dfrac{x+1}{x^2+1}'), fx(r'(x-1)^2(x+2)^3'), fx(r'\dfrac{e^x}{e^x+1}')]),
     tasks(1, [r"$e^{-x^2}+x\,e^{-x^2}(-2x)=\res{(1-2x^2)\,e^{-x^2}}$", r"$\ln(x+1)-\ln(x^2+1)\Rightarrow\res{\frac{1}{x+1}-\frac{2x}{x^2+1}}=\frac{1-2x-x^2}{(x+1)(x^2+1)}$",
               r"$2(x-1)(x+2)^3+3(x-1)^2(x+2)^2=\res{(x-1)(x+2)^2(5x+1)}$", r"$\frac{e^x(e^x+1)-e^xe^x}{(e^x+1)^2}=\res{\frac{e^x}{(e^x+1)^2}}$"])),
 (2, r"\pau{Murcia, EBAU septiembre 2020} Calcula las derivadas de las funciones siguientes:" + tasks(2, [fx(r'(x^2-2)\ln x'), fx(r'e^{4x^3+2}')]),
     tasks(2, [r'$\res{2x\ln x+\frac{x^2-2}{x}}$', r'$\res{12x^2e^{4x^3+2}}$'])),
 (2, r"\pau{Murcia, EBAU junio 2018} Halla las derivadas de las funciones siguientes:" + tasks(2, [fx(r'x^2\ln(x^2)', 'g'), fx(r'e^{-3x+x^2}', 'h')]),
     tasks(2, [r"$2x\ln(x^2)+x^2\cdot\frac{2x}{x^2}=\res{2x\ln(x^2)+2x}$", r"$\res{(2x-3)\,e^{-3x+x^2}}$"])),
 (2, r"\pau{Andalucía, PEvAU ordinaria 2021} Calcula la derivada de las funciones siguientes:" + tasks(2, [fx(r'\ln\left(\dfrac{x-1}{x+1}\right)'), fx(r'x^3\cdot e^{2x^2}', 'g')]),
     tasks(2, [r"$\frac{1}{x-1}-\frac{1}{x+1}=\res{\frac{2}{x^2-1}}$", r"$3x^2e^{2x^2}+x^3e^{2x^2}\cdot4x=\res{e^{2x^2}(3x^2+4x^4)}$"])),
 (2, r"\pau{Andalucía, ordinaria (suplente) 2025} Calcula la derivada de las funciones siguientes:" + tasks(2, [fx(r'\ln\left(\dfrac{x^2-1}{x^2+1}\right)', 'g'), fx(r'(2x-1)\,e^{x^2-x}', 'h')]),
     tasks(1, [r"$g'(x)=\frac{2x}{x^2-1}-\frac{2x}{x^2+1}=\res{\frac{4x}{(x^2-1)(x^2+1)}}$", r"$h'(x)=2e^{x^2-x}+(2x-1)^2e^{x^2-x}=\res{(4x^2-4x+3)\,e^{x^2-x}}$"])),
 (3, r"\pau{Andalucía, PEvAU ordinaria 2024} Calcula la derivada de las funciones siguientes:" + tasks(2, [fx(r'(x^2+2)^3\cdot e^{-2x}'), fx(r'\dfrac{\ln(1-x^3)}{(1-2x^2)^2}', 'g')]),
     tasks(1, [r"$f'(x)=6x(x^2+2)^2e^{-2x}-2(x^2+2)^3e^{-2x}=\res{-2(x^2-3x+2)(x^2+2)^2e^{-2x}}$",
               r"$g'(x)=\dfrac{\frac{-3x^2}{1-x^3}(1-2x^2)^2-\ln(1-x^3)\cdot2(1-2x^2)(-4x)}{(1-2x^2)^4}=\res{\dfrac{-3x^2(1-2x^2)+8x(1-x^3)\ln(1-x^3)}{(1-2x^2)^3(1-x^3)}}$"])),
 (2, r"\pau{Murcia, EBAU septiembre 2018} Dada la función $f(x)=5x^3e^{2x}+\dfrac{1}{x^2+1}$:" + tasks(1, [r"Calcula $f'(0)$.", r"Halla la ecuación de la recta tangente a la gráfica de la función en el punto $(0,1)$."]),
     tasks(1, [r"$f'(x)=15x^2e^{2x}+10x^3e^{2x}-\frac{2x}{(x^2+1)^2}\Rightarrow\res{f'(0)=0}$", r"$y-1=0\cdot(x-0)\Rightarrow\res{y=1}$"])),
 (2, r"Halla la ecuación de la recta tangente a la gráfica de cada función en el punto indicado:" + tasks(1, [r"\pau{Murcia, EBAU julio 2020} $f(x)=\dfrac{1}{x+1}$ en $x=1$.", r"\pau{Navarra, EvAU ordinaria 2023} $f(x)=\sqrt{5+x^2}$ en $x=-2$.", r"\pau{Navarra, EvAU ordinaria 2022} $f(x)=\dfrac{x}{x^2-4}$ en $x=1$."]),
     tasks(1, [r"$f(1)=\frac12$, $f'(x)=\frac{-1}{(x+1)^2}$, $f'(1)=-\frac14$: \ $y-\frac12=-\frac14(x-1)\Rightarrow\res{y=-0{,}25x+0{,}75}$",
               r"$f(-2)=3$, $f'(x)=\frac{x}{\sqrt{5+x^2}}$, $f'(-2)=-\frac23$: \ $y-3=-\frac23(x+2)\Rightarrow\res{y=-\frac23x+\frac53}$",
               r"$f(1)=-\frac13$, $f'(x)=\frac{-x^2-4}{(x^2-4)^2}$, $f'(1)=-\frac59$: \ $y+\frac13=-\frac59(x-1)\Rightarrow\res{5x+9y-2=0}$"])),
 (3, r"\pau{Islas Baleares, PBAU extraordinaria 2021} Considera la función $f(x)=\dfrac3x+8$." + tasks(1, [r"Halla los puntos de la gráfica en los que la recta tangente es paralela a la recta $3x+4y+5=0$.", "Calcula las ecuaciones de las rectas tangentes en los puntos hallados en el apartado anterior."]),
     tasks(1, [r"La recta tiene pendiente $-\frac34$. \ $f'(x)=-\frac{3}{x^2}=-\frac34\Rightarrow x^2=4\Rightarrow x=\pm2$: \ puntos $\res{(-2;\ 6{,}5)}$ y $\res{(2;\ 9{,}5)}$.",
               r"En $x=-2$: $\res{y=-\frac34x+5}$; \ en $x=2$: $\res{y=-\frac34x+11}$."])),
 (2, r"Halla los parámetros en cada caso:" + tasks(1, [r"\pau{Madrid, EvAU extraordinaria 2022} $a$ y $b$ para que $f(x)=ax+\dfrac bx$ verifique $f(2)=4$ y $f'(2)=0$.",
                                                    r"\pau{Murcia, EBAU septiembre 2017} $a$ y $b$ para que $f(x)=\dfrac{ax+b}{x^2+1}$ cumpla $f(0)=1$ y $f'(0)=1$.",
                                                    r"\pau{Murcia, EBAU septiembre 2018} $a$ y $b$ para que $f(x)=x^3\ln(2x+5)+ax+b$ cumpla $f(0)=2$ y $f'(0)=1$.",
                                                    r"\pau{Andalucía, PEvAU ordinaria 2024} $a$ y $b$ para que sea horizontal la recta tangente a la gráfica de $h(x)=x^3+ax^2+3x+b$ en el punto $P(1,2)$."]),
     tasks(1, [r"$f'(x)=a-\frac{b}{x^2}$: \ $2a+\frac b2=4$, \ $a-\frac b4=0\Rightarrow\res{a=1,\ b=4}$",
               r"$f(0)=b=1$; \ $f'(x)=\frac{a(x^2+1)-(ax+b)2x}{(x^2+1)^2}\Rightarrow f'(0)=a=1$: \ $\res{a=b=1}$",
               r"$f(0)=b=2$; \ $f'(x)=3x^2\ln(2x+5)+\frac{2x^3}{2x+5}+a\Rightarrow f'(0)=a=1$: \ $\res{a=1,\ b=2}$",
               r"$h'(1)=3+2a+3=0\Rightarrow a=-3$; \ $h(1)=1-3+3+b=2\Rightarrow b=1$: \ $\res{a=-3,\ b=1}$"])),
]))

S.append(("Continuidad y derivabilidad. Derivadas laterales", [
 (2, r"Calcula las derivadas laterales en el punto indicado y di si la función es derivable en él:" + tasks(2, [r"$f(x)=|x+1|$ en $x=-1$", r"$f(x)=|x^2-9|$ en $x=3$", r"$f(x)=x\,|x-1|$ en $x=1$", r"$f(x)=\sqrt[3]{x^2}$ en $x=0$"])
     + recorda(r"$f'(a^-)=\displaystyle\lim_{h\to0^-}\frac{f(a+h)-f(a)}{h}$ y $f'(a^+)=\displaystyle\lim_{h\to0^+}\frac{f(a+h)-f(a)}{h}$. \ $f$ es derivable en $a$ si las dos existen, son finitas y coinciden. Un valor absoluto se escribe primero a trozos."),
     tasks(1, [r"$f'(-1^-)=-1$, $f'(-1^+)=1$: \rest{no derivable} (punto anguloso).",
               r"Cerca de 3: $9-x^2$ por la izquierda y $x^2-9$ por la derecha: $f'(3^-)=-6$, $f'(3^+)=6$: \rest{no derivable}.",
               r"Cerca de 1: $x(1-x)$ por la izquierda y $x(x-1)$ por la derecha: $f'(1^-)=1-2=-1$, $f'(1^+)=2-1=1$: \rest{no derivable}.",
               r"$\displaystyle\lim_{h\to0}\frac{\sqrt[3]{h^2}}{h}=\lim_{h\to0}\frac{1}{\sqrt[3]{h}}$: $-\infty$ por la izquierda y $+\infty$ por la derecha: \rest{no derivable}."])),
 (1, r"Razona si son verdaderas o falsas las afirmaciones siguientes. Si son falsas, pon un contraejemplo:" + tasks(1, [r"Si $f$ es continua en $x=a$, entonces es derivable en $x=a$.", r"Si $f$ no es continua en $x=a$, entonces no es derivable en $x=a$.", r"Si $f$ no es derivable en $x=a$, entonces no es continua en $x=a$.", r"Si en una función a trozos las derivadas de los dos trozos valen lo mismo en el punto de cambio $a$, la función es derivable en $a$."])
     + recorda(r"Derivable $\Rightarrow$ continua. El recíproco no es cierto."),
     tasks(1, [r"\rest{Falsa}: $|x|$ es continua en 0 pero no es derivable en él.", r"\rest{Verdadera}: si fuera derivable, sería continua.", r"\rest{Falsa}: $|x|$ no es derivable en 0 y sí es continua.",
               r"\rest{Falsa}: hace falta, además, que sea continua. Por ejemplo, $f(x)=x$ si $x<0$ y $f(x)=x+1$ si $x\geq0$: los dos trozos tienen derivada 1, pero hay un salto en $x=0$."])),
 (2, r"Observa la gráfica de la función $f$ e indica en qué puntos no es continua y en cuáles no es derivable. Justifícalo. (En $x=0$ la recta y la curva se unen sin formar pico.)" + '\n\n\\begin{center}' + G_LECT + '\\end{center}',
     r"En $x=2$ hay un salto: \rest{no es continua} y, por tanto, \rest{no es derivable}. En $x=-2$ es continua, pero hay un punto anguloso (pendientes $1$ y $-1$): \rest{no es derivable}. En $x=0$ es continua y derivable (unión suave). $f$ es continua en $\res{\mathbb R-\{2\}}$ y derivable en $\res{\mathbb R-\{-2,2\}}$."),
]))

S.append(("Derivabilidad de funciones a trozos", [
 (2, r"Estudia la continuidad y la derivabilidad de las funciones siguientes:" + tasks(2, ['$' + pw((r'e^x', 'x<0'), (r'x+1', r'x\geq0')) + '$', '$' + pw((r'3-x^2', 'x<1'), (r'\dfrac2x', r'x\geq1'), name='g(x)') + '$'])
     + recorda(r"1) Continuidad en el punto de cambio (si no es continua, no es derivable). 2) Derivamos cada trozo \textbf{sin el igual}. 3) Comparamos $f'(a^-)$ y $f'(a^+)$."),
     tasks(1, [r"$f$: \ $\lim_{x\to0^-}e^x=1=f(0)$: continua. \ $f'(x)=e^x$ si $x<0$ y $1$ si $x>0$: $f'(0^-)=1=f'(0^+)$. \ \rest{Continua y derivable en $\mathbb R$}.",
               r"$g$: \ $\lim_{x\to1^-}(3-x^2)=2=g(1)$: continua ($\frac2x$ solo falla en $0$, fuera de $x\geq1$). \ $g'(1^-)=-2$, \ $g'(1^+)=-\frac{2}{1^2}=-2$. \ \rest{Continua y derivable en $\mathbb R$}."])),
 (2, r"\pau{Andalucía, PEvAU extraordinaria 2024} Considera la función" + dm(pw((r'-x^2+4x+3', 'x<4'), (r'2x-5', r'x\geq4'))) + "Estudia su continuidad y su derivabilidad.",
     r"Trozos polinómicos. $x=4$: $f(4)=3$, $\lim_{x\to4^-}f=-16+16+3=3$: continua en $\mathbb R$. \ $f'(x)=-2x+4$ si $x<4$, $2$ si $x>4$: $f'(4^-)=-4\neq2=f'(4^+)$. \ \rest{Continua en $\mathbb R$ y derivable en $\mathbb R-\{4\}$}."),
 (2, r"\pau{Andalucía, ordinaria (suplente) 2025} Considera la función" + dm(pw((r'10+\dfrac{5x}{2}', r'x\leq-2'), (r'x^2+1', r'-2<x<2'), (r'10-\dfrac{5x}{2}', r'x\geq2'))) + r"Estudia la continuidad y la derivabilidad de $f$ en el punto de abscisa $x=-2$.",
     r"$f(-2)=10-5=5$, \ $\lim_{x\to-2^+}(x^2+1)=5$: \rest{continua} en $x=-2$. \ $f'(-2^-)=\frac52$, \ $f'(-2^+)=2\cdot(-2)=-4$: \rest{no es derivable} en $x=-2$."),
 (2, r"\pau{Andalucía, PEvAU ordinaria 2024} La velocidad del viento, en km/h, prevista para cierto día en una zona de Sierra Nevada viene dada por la función" + dm(pw((r't^2-8t+60', r'0\leq t\leq10'), (r'-t^2+32t-140', r'10<t\leq24'), name='v(t)')) + r"donde $t$ es el tiempo en horas. Comprueba que la función $v$ es continua y derivable.",
     r"$t=10$: $v(10)=80$, $\lim_{t\to10^+}v=-100+320-140=80$: continua. \ $v'(t)=2t-8$ si $0<t<10$ y $-2t+32$ si $10<t<24$: $v'(10^-)=12=v'(10^+)$. \ \rest{Continua en $[0,24]$ y derivable en $(0,24)$}."),
 (2, r"\pau{Navarra, EvAU ordinaria 2024} Sea la función" + dm(pw((r'-x^2-4x', r'x<-1'), (r'4-x', r'-1\leq x<1'), (r'x^2-6x+8', r'x\geq1'))) + tasks(1, [r"Estudia la continuidad de $f(x)$, clasificando sus puntos de discontinuidad.", r"Estudia la derivabilidad de $f(x)$."]),
     tasks(1, [r"$x=-1$: $\lim_{x\to-1^-}f=3$, $\lim_{x\to-1^+}f=5=f(-1)$: \rest{salto finito}. \ $x=1$: $3=3=f(1)$: continua. \ Continua en $\res{\mathbb R-\{-1\}}$.",
               r"En $x=-1$ no es derivable (no es continua). \ $f'(1^-)=-1$, $f'(1^+)=2-6=-4$: no derivable. \ Derivable en $\res{\mathbb R-\{-1,1\}}$."])),
 (2, r"\pau{Andalucía, PEvAU extraordinaria 2021} Considera la función" + dm(pw((r'2^{x+1}', 'x<0'), (r'x^2-2x', r'x\geq0'))) + r"Estudia la continuidad y la derivabilidad de la función $f$ en su dominio.",
     r"$\lim_{x\to0^-}2^{x+1}=2$, \ $\lim_{x\to0^+}(x^2-2x)=0$: no es continua en $x=0$ y, por tanto, \rest{no es derivable en $x=0$}. Los trozos son continuos y derivables: $f$ es continua y derivable en $\res{\mathbb R-\{0\}}$."),
 (3, r"\pau{Andalucía, PEvAU extraordinaria 2021} El número de diagnosticados por PCR en Andalucía, en miles de personas, se aproxima por la función" + dm(pw((r'-t^2+2t-0{,}3', r'0{,}2\leq t\leq1{,}8'), (r'0{,}1t-0{,}12', r'1{,}8<t\leq5'), (r'-0{,}5t^2+8{,}3t-28{,}62', r'5<t\leq10'), name='f(t)')) + r"donde $t$ es el tiempo en meses. Estudia la continuidad y la derivabilidad de la función $f$ en su dominio.",
     r"$t=1{,}8$: $f(1{,}8)=0{,}06$ y $\lim_{t\to1{,}8^+}f=0{,}06$; \ $t=5$: $f(5)=0{,}38$ y $\lim_{t\to5^+}f=0{,}38$: \rest{continua en $[0{,}2;\ 10]$}. \ $f'(1{,}8^-)=-1{,}6\neq0{,}1=f'(1{,}8^+)$; \ $f'(5^-)=0{,}1\neq3{,}3=f'(5^+)$. \ Derivable en $\res{(0{,}2;\ 1{,}8)\cup(1{,}8;\ 5)\cup(5;\ 10)}$."),
 (3, r"Escribe a trozos y estudia la derivabilidad de $f(x)=|x-1|+|x+1|$ y de $g(x)=|x^2-4x|$.",
     tasks(1, [r"$f(x)=-2x$ si $x<-1$; \ $2$ si $-1\leq x\leq1$; \ $2x$ si $x>1$. Continua; $f'(-1^-)=-2\neq0=f'(-1^+)$ y $f'(1^-)=0\neq2=f'(1^+)$: derivable en $\res{\mathbb R-\{-1,1\}}$.",
               r"$g(x)=x^2-4x$ si $x<0$ o $x>4$; \ $-x^2+4x$ si $0\leq x\leq4$. Continua; $g'(0^-)=-4\neq4=g'(0^+)$ y $g'(4^-)=-4\neq4=g'(4^+)$: derivable en $\res{\mathbb R-\{0,4\}}$."])),
]))

S.append(("Funciones a trozos con parámetros", [
 (2, r"\pau{Andalucía, PEvAU ordinaria 2022} Considera la función" + dm(pw((r'6x-3', r'x\leq1'), (r'ax^2+bx+2', 'x>1'))) + r"con $a$ y $b$ números reales. Determina los valores de $a$ y $b$ para que $f$ sea continua y derivable en todo su dominio."
     + recorda(r"En el punto de cambio planteamos dos ecuaciones: continuidad ($\lim_{x\to a^-}f=\lim_{x\to a^+}f=f(a)$) y derivabilidad ($f'(a^-)=f'(a^+)$)."),
     r"Continuidad en $x=1$: $3=a+b+2$. \ Derivabilidad: $f'(1^-)=6$, $f'(1^+)=2a+b\Rightarrow2a+b=6$. \ $\begin{cases}a+b=1\\2a+b=6\end{cases}\Rightarrow\res{a=5,\ b=-4}$."),
 (2, r"\pau{Andalucía, PEvAU extraordinaria 2020} Considera la función" + dm(pw((r'2+\dfrac{a}{x-1}', 'x<0'), (r'a+be^x', r'x\geq0'))) + r"Calcula los valores de $a$ y $b$ para que la función sea continua y derivable en su dominio.",
     r"Continuidad en $x=0$: $2-a=a+b$. \ $f'(x)=\frac{-a}{(x-1)^2}$ si $x<0$ y $be^x$ si $x>0$: $-a=b$. \ Sustituyendo: $2-a=0\Rightarrow\res{a=2,\ b=-2}$ ($x=1$ no es de $x<0$)."),
 (2, r"\pau{Islas Baleares, PBAU ordinaria 2022} Consideremos la función a trozos" + dm(pw((r'x^2-3x+2', 'x<0'), (r'x^2+ax+2', r'x\geq0'))) + r"Calcula los valores de $a$ para que $f(x)$ sea continua y derivable.",
     r"Continuidad: $2=2$, continua para cualquier $a$. \ $f'(0^-)=-3$, $f'(0^+)=a\Rightarrow\res{a=-3}$."),
 (2, r"\pau{Islas Baleares, PBAU ordinaria 2021} Considera la función a trozos" + dm(pw((r'x^2-3x+2', 'x<0'), (r'e^{ax}+1', r'x\geq0'))) + r"Calcula los valores de $a$ para que $f$ sea continua y derivable.",
     r"Continuidad: $2=e^0+1=2$, para cualquier $a$. \ $f'(0^-)=-3$, $f'(0^+)=a\,e^{0}=a\Rightarrow\res{a=-3}$."),
 (2, r"\pau{Islas Baleares, PBAU extraordinaria 2021} Considera la función definida a trozos" + dm(pw((r'-4x+a', r'x\leq-2'), (r'x^2-5', r'-2<x<1'), (r'-7x+3', r'x\geq1'))) + tasks(1, [r"Calcula los valores de $a$ para que $f(x)$ sea continua.", r"¿Es $f(x)$ derivable para $a=1$?"]),
     tasks(1, [r"$x=-2$: $8+a=4-5\Rightarrow\res{a=-9}$. \ ($x=1$: $-4=-4$ siempre.)", r"Para $a=1$ no es continua en $x=-2$ ($9\neq-1$): no es derivable. En $x=1$: $f'(1^-)=2\neq-7=f'(1^+)$. \ \rest{No es derivable en $x=-2$ ni en $x=1$}."])),
 (3, r"\pau{Aragón, EvAU ordinaria 2022} Siendo $a$, $b$ parámetros reales, se considera la función" + dm(pw((r'x^2+2\sqrt3', r'x\leq0'), (r'\sqrt{ax+b}', r'0<x\leq3'), (r'\dfrac72-\dfrac x6', 'x>3'))) + tasks(1, [r"Determina el valor de los parámetros para que $f(x)$ sea continua.", r"Para estos valores, analiza si $f(x)$ es derivable en $x=0$ y en $x=3$."]),
     tasks(1, [r"$x=0$: $2\sqrt3=\sqrt b\Rightarrow b=12$. \ $x=3$: $\sqrt{3a+12}=\frac72-\frac12=3\Rightarrow\res{a=-1,\ b=12}$.",
               r"$f'(x)=\frac{-1}{2\sqrt{12-x}}$ si $0<x<3$. \ $f'(0^-)=0\neq-\frac{1}{2\sqrt{12}}=f'(0^+)$: \rest{no derivable en $x=0$}. \ $f'(3^-)=-\frac16=f'(3^+)$: \rest{derivable en $x=3$}."])),
 (2, r"\pau{Andalucía, ordinaria (suplente) 2025} El nivel de concentración de un alumno durante un examen de 5 horas viene dado por la función" + dm(pw((r'-t^2+2t+10', r'0\leq t\leq2{,}5'), (r't^2+at+b', r'2{,}5<t\leq5'), name='f(t)')) + r"donde $t$ es el tiempo en horas y $a$ y $b$ son números reales. ¿Con qué nivel de concentración empieza el alumno el examen? Determina los valores de $a$ y $b$ para que la función sea continua y derivable en $t=2{,}5$.",
     r"$f(0)=\res{10}$. \ Continuidad: $-6{,}25+5+10=8{,}75=6{,}25+2{,}5a+b$. \ Derivabilidad: $-2\cdot2{,}5+2=-3=5+a\Rightarrow a=-8$, \ y $b=8{,}75-6{,}25+20=22{,}5$: \ $\res{a=-8,\ b=22{,}5}$."),
 (2, r"Halla los parámetros para que cada función sea derivable en $\mathbb R$:" + tasks(2, ['$' + pw((r'ax^2+bx+1', r'x\leq2'), (r'3x-3', 'x>2')) + '$', '$' + pw((r'e^{2x}', r'x\leq0'), (r'x^2+ax+b', 'x>0'), name='g(x)') + '$']),
     tasks(1, [r"$f$: \ $4a+2b+1=3$ y $4a+b=3\Rightarrow\res{a=1,\ b=-1}$.", r"$g$: \ $1=b$ y $g'(0^-)=2e^0=2=a\Rightarrow\res{a=2,\ b=1}$."])),
]))

# ---------- comprovacions numèriques ----------
ln, e, sq, sin, cos, tan, atan, asin = math.log, math.exp, math.sqrt, math.sin, math.cos, math.tan, math.atan, math.asin
def nd(f, x, h=1e-6): return (f(x + h) - f(x - h)) / (2 * h)
cb = lambda x: math.copysign(abs(x) ** (1 / 3), x)
DER = [  # (f, derivada de la solució, punts)
 (lambda x: 3*x*x - x, lambda x: 6*x - 1, [1]), (lambda x: x**3 - 2*x, lambda x: 3*x*x - 2, [-1]), (lambda x: 2/(x-1), lambda x: -2/(x-1)**2, [3]),
 (lambda x: sq(2*x+1), lambda x: 1/sq(2*x+1), [4]), (lambda x: -x*x + 4*x + 3, lambda x: 2, [1]),
 (lambda x: x*x - 3*x + 2, lambda x: 2*x - 3, [0.7, 2]), (lambda x: 1/(x+2), lambda x: -1/(x+2)**2, [0.7, 2]), (sq, lambda x: 1/(2*sq(x)), [0.7, 2]),
 (lambda x: 5*x**4 - 3*x**3 + 2*x - 8, lambda x: 20*x**3 - 9*x*x + 2, [0.7, 2]), (lambda x: x**5/5 - 2*x**3/3 + x, lambda x: x**4 - 2*x*x + 1, [0.7]),
 (lambda x: (3*x*x - 2*x + 1)/4, lambda x: (3*x - 1)/2, [0.7]), (lambda x: -x**6 + x/2 - 7, lambda x: -6*x**5 + .5, [0.7]),
 (lambda x: (2*x-1)*(x*x+3), lambda x: 6*x*x - 2*x + 6, [0.7]), (lambda x: (x**3+x)*(1-x*x), lambda x: 1 - 5*x**4, [0.7]), (lambda x: x*x*(x-1)*(x+1), lambda x: 4*x**3 - 2*x, [0.7]),
 (lambda x: (x+3)/(x-2), lambda x: -5/(x-2)**2, [0.7]), (lambda x: 2*x*x/(x+1), lambda x: (2*x*x + 4*x)/(x+1)**2, [0.7]), (lambda x: (x*x-1)/(x*x+1), lambda x: 4*x/(x*x+1)**2, [0.7]), (lambda x: 3/(x*x-4), lambda x: -6*x/(x*x-4)**2, [0.7]),
 (lambda x: x**4 - 2*x**3 + 5*x, lambda x: 4*x**3 - 6*x*x + 5, [1]), (lambda x: 4*x**3 - 6*x*x + 5, lambda x: 12*x*x - 12*x, [1, 2]),
 (lambda x: .01*x*x + 5*x + 200, lambda x: .02*x + 5, [100]),
 (lambda x: x**1.5, lambda x: 1.5*sq(x), [0.7]), (lambda x: x**-2, lambda x: -2/x**3, [0.7]), (cb, lambda x: 1/(3*cb(x*x)), [0.7]), (lambda x: 6/sq(x), lambda x: -3/(x*sq(x)), [0.7]),
 (lambda x: x*x*sq(x), lambda x: 2.5*x*sq(x), [0.7]), (lambda x: 2/(3*x**3), lambda x: -2/x**4, [0.7]),
 (lambda x: 2*e(x) - 3*ln(x), lambda x: 2*e(x) - 3/x, [0.7]), (lambda x: 4**x, lambda x: 4**x*ln(4), [0.7]), (lambda x: ln(x)/ln(3), lambda x: 1/(x*ln(3)), [0.7]),
 (lambda x: x*e(x), lambda x: (x+1)*e(x), [0.7]), (lambda x: e(x)/x, lambda x: e(x)*(x-1)/x**2, [0.7]), (lambda x: x*x*ln(x), lambda x: 2*x*ln(x) + x, [0.7]),
 (lambda x: 3*sin(x) - 2*cos(x), lambda x: 3*cos(x) + 2*sin(x), [0.7]), (lambda x: x*sin(x), lambda x: sin(x) + x*cos(x), [0.7]), (lambda x: tan(x) - x, lambda x: tan(x)**2, [0.7]),
 (lambda x: sin(x)*cos(x), lambda x: cos(x)**2 - sin(x)**2, [0.7]), (lambda x: atan(x) - x, lambda x: -x*x/(1+x*x), [0.7]), (lambda x: x*asin(x), lambda x: asin(x) + x/sq(1-x*x), [0.5]),
 (lambda x: (3*x*x-1)**4, lambda x: 24*x*(3*x*x-1)**3, [0.7]), (lambda x: sq(x*x-2*x), lambda x: (x-1)/sq(x*x-2*x), [2.7]), (lambda x: (x*x+1)**-3, lambda x: -6*x/(x*x+1)**4, [0.7]),
 (lambda x: cb(2*x+5), lambda x: 2/(3*cb((2*x+5)**2)), [0.7]),
 (lambda x: e(3*x-1), lambda x: 3*e(3*x-1), [0.7]), (lambda x: 2**(x*x), lambda x: 2*x*2**(x*x)*ln(2), [0.7]), (lambda x: ln(x*x-3*x), lambda x: (2*x-3)/(x*x-3*x), [3.7]),
 (lambda x: math.log10(5*x), lambda x: 1/(x*ln(10)), [0.7]), (lambda x: ln(sq(x)), lambda x: 1/(2*x), [0.7]), (lambda x: e(sq(x)), lambda x: e(sq(x))/(2*sq(x)), [0.7]),
 (lambda x: sin(5*x+1), lambda x: 5*cos(5*x+1), [0.7]), (lambda x: cos(x*x), lambda x: -2*x*sin(x*x), [0.7]), (lambda x: tan(3*x), lambda x: 3/cos(3*x)**2, [0.3]),
 (lambda x: sin(x)**3, lambda x: 3*sin(x)**2*cos(x), [0.7]), (lambda x: atan(2*x), lambda x: 2/(1+4*x*x), [0.7]), (lambda x: asin(x*x), lambda x: 2*x/sq(1-x**4), [0.7]),
 (lambda x: x*e(-x*x), lambda x: (1-2*x*x)*e(-x*x), [0.7]), (lambda x: ln((x+1)/(x*x+1)), lambda x: (1-2*x-x*x)/((x+1)*(x*x+1)), [0.7]),
 (lambda x: (x-1)**2*(x+2)**3, lambda x: (x-1)*(x+2)**2*(5*x+1), [0.7]), (lambda x: e(x)/(e(x)+1), lambda x: e(x)/(e(x)+1)**2, [0.7]),
 (lambda x: (x*x-2)*ln(x), lambda x: 2*x*ln(x) + (x*x-2)/x, [0.7]), (lambda x: e(4*x**3+2), lambda x: 12*x*x*e(4*x**3+2), [0.3]),
 (lambda x: x*x*ln(x*x), lambda x: 2*x*ln(x*x) + 2*x, [0.7]), (lambda x: e(-3*x+x*x), lambda x: (2*x-3)*e(-3*x+x*x), [0.7]),
 (lambda x: ln((x-1)/(x+1)), lambda x: 2/(x*x-1), [2.5]), (lambda x: x**3*e(2*x*x), lambda x: e(2*x*x)*(3*x*x + 4*x**4), [0.7]),
 (lambda x: ln((x*x-1)/(x*x+1)), lambda x: 4*x/((x*x-1)*(x*x+1)), [2.5]), (lambda x: (2*x-1)*e(x*x-x), lambda x: (4*x*x-4*x+3)*e(x*x-x), [0.7]),
 (lambda x: (x*x+2)**3*e(-2*x), lambda x: -2*(x*x-3*x+2)*(x*x+2)**2*e(-2*x), [0.7]),
 (lambda x: ln(1-x**3)/(1-2*x*x)**2, lambda x: (-3*x*x*(1-2*x*x) + 8*x*(1-x**3)*ln(1-x**3))/((1-2*x*x)**3*(1-x**3)), [0.3, -0.8]),
 (lambda x: 5*x**3*e(2*x) + 1/(x*x+1), lambda x: 15*x*x*e(2*x) + 10*x**3*e(2*x) - 2*x/(x*x+1)**2, [0, 0.7]),
 (lambda x: 1/(x+1), lambda x: -1/(x+1)**2, [1]), (lambda x: sq(5+x*x), lambda x: x/sq(5+x*x), [-2]), (lambda x: x/(x*x-4), lambda x: (-x*x-4)/(x*x-4)**2, [1]),
 (lambda x: 3/x + 8, lambda x: -3/x**2, [-2, 2]), (lambda x: x**3*ln(2*x+5) + x + 2, lambda x: 3*x*x*ln(2*x+5) + 2*x**3/(2*x+5) + 1, [0, 0.7]),
 (lambda x: (x+1)/(x*x+1), lambda x: ((x*x+1) - (x+1)*2*x)/(x*x+1)**2, [0]), (lambda x: x + 4/x, lambda x: 1 - 4/x**2, [2]),
 (lambda x: sq(12-x), lambda x: -1/(2*sq(12-x)), [0.5, 3]),
]
for f, fp, xs in DER:
    for x in xs: assert abs(nd(f, x) - fp(x)) < 1e-5 * (1 + abs(fp(x))), (x, nd(f, x), fp(x))
# tangents, punts i paràmetres: (valor de l'esquerra, valor de la dreta)
PAR = [(1/(1+1), -.25*1 + .75), (3 - (-2/3*-2 + 5/3), 0), (5*1 + 9*(-1/3) - 2, 0), (3/-2 + 8, 6.5), (3/2 + 8, 9.5), (6.5, -.75*-2 + 5), (9.5, -.75*2 + 11),
       (1*2 + 4/2, 4), (1 - 4/4, 0), (3 + 2*-3 + 3, 0), (1 - 3 + 3 + 1, 2)]
PAR += [(-16 + 16 + 3, 8 - 5), (-2*4 + 4, -4), (10 - 5, 4 + 1), (100 - 80 + 60, -100 + 320 - 140), (2*10 - 8, -20 + 32), (-1 + 4, 3), (4 - 1, 1 - 6 + 8),
        (-3.24 + 3.6 - .3, .18 - .12), (.5 - .12, -12.5 + 41.5 - 28.62), (-2*1.8 + 2, -1.6), (-5 + 8.3, 3.3),
        (6 - 3, 5 + -4 + 2), (6, 2*5 - 4), (2 + 2/(0 - 1), 2 + -2), (-2, -(-2) * -1), (-3, -3), (-4*-2 - 9, 4 - 5), (-4*-2 + 1, 9), (2, -7 + 9),
        (2*sq(3), sq(12)), (sq(3*-1 + 12), 3.5 - .5), (-1/(2*sq(9)), -1/6), (-6.25 + 5 + 10, 6.25 + 2.5*-8 + 22.5), (-2*2.5 + 2, 2*2.5 - 8),
        (4*1 + 2*-1 + 1, 3), (4*1 - 1, 3), (e(0), 1), (2*e(0), 2), (-2 + 1, -1), (0, 0)]
for l, r in PAR: assert abs(l - r) < 1e-9, (l, r)


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

TIT = "Cálculo de derivadas. Derivabilidad de una función"
KW = "derivadas, tasa de variación media, definición de derivada, recta tangente, reglas de derivación, regla de la cadena, derivadas laterales, derivabilidad, funciones a trozos, parámetros, PAU"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 5: %s' % (t, TIT), capcalera='%s · Unidad 5: Cálculo de derivadas' % t, pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 5' if sol else 'Ficha de ejercicios · Unidad 5') + '}{' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con la calculadora de derivadas de los apuntes interactivos de la unidad. Una derivada puede estar escrita de maneras diferentes y ser igualmente correcta."
             if sol else r"Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas. Resuélvelos en el cuaderno mostrando todos los pasos y simplifica las derivadas.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            lab = re.search(r'\\label\{[^}]*\}', q)
            if sol:
                head = re.sub(r'(\\pau\{[^}]*\}).*', r'\1', q, flags=re.S) if q.startswith('\\pau{') else ''
                out.append('\\ex{%d} %s%s\n\n' % (st, (lab.group(0) if lab else '') + head, s))
            else:
                out.append('\\ex{%d} %s\n\n' % (st, q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con la calculadora de derivadas de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't5-fitxa-solucions-es.tex' if sol else 't5-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'ejercicios,', npau, 'enunciados de la PAU de otras comunidades')
