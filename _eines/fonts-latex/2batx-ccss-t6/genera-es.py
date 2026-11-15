# Versió en castellà de genera.py. Genera t6-fitxa-exercicis.tex i t6-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 6: Aplicacions de la derivada)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Com a les unitats 4 i 5, els exercicis marcats amb \pau{...} són de la PAU d'altres comunitats (recopilació «Ejercicios
# de análisis en pruebas EBAU de España» de www.ebaumatematicas.com, curs 2021/22), traduïts al valencià i reduïts als
# apartats d'aquesta unitat. Al final, CHK comprova numèricament els resultats de les solucions.
# Ús: python3 genera.py && pdflatex t6-fitxa-exercicis.tex (dues vegades) && pdflatex t6-fitxa-solucions.tex
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def pw(*rows, name='f(x)'):
    return name + r'=\begin{cases}' + r'\\[3pt]'.join(r'%s&\text{si }%s' % r for r in rows) + r'\end{cases}'
def dm(s): return r'\[' + s + r'\]'
def fx(s, n='f'): return '$' + n + '(x)=' + s + '$'

# ---------- gràfica de l'exercici de lectura ----------
def tzg(x0, x1, y0, y1, body, sc=0.62):
    g = r'\draw[muted!30,very thin] (%s,%s) grid (%s,%s);' % (x0, y0, x1, y1)
    g += r'\draw[-latex,thick] (%s,0)--(%s,0);\draw[-latex,thick] (0,%s)--(0,%s);' % (x0, x1 + 0.4, y0, y1 + 0.4)
    return r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]\begin{scope}%s\clip (%s,%s) rectangle (%s,%s);%s\end{scope}\end{tikzpicture}' % (sc, g, x0, y0, x1, y1, body)
def tk(x, y, t, pos='below'): return r'\node[%s,font=\scriptsize] at (%s,%s) {$%s$};' % (pos, x, y, t)
G_LECT = tzg(-4, 4, -3, 4, r'\draw[accent,line width=1.5pt,smooth,samples=80,domain=-2.6:2.6] plot (\x,{(\x*\x*\x-3*\x)/1});'
             + r'\fill[accent] (-1,2) circle (0.12);\fill[accent] (1,-2) circle (0.12);'
             + tk(-1, 0, '-1') + tk(1, 0, '1', 'above') + tk(0, 2, '2', 'right') + tk(0, -2, '-2', 'left'))

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Recta tangente y recta normal", [
 (1, r"Calcula la ecuación de la recta tangente y de la recta normal a la gráfica de cada función en el punto indicado:" + tasks(2, [fx(r'x^3-2x^2+1') + r' en $x=2$', fx(r'\dfrac{2x-1}{x+1}') + r' en $x=0$', fx(r'x\ln x') + r' en $x=1$', fx(r'e^{x^2-1}') + r' en $x=1$'])
     + recorda(r"Tangente: $y-f(a)=f'(a)\,(x-a)$. \ Normal: $y-f(a)=-\dfrac{1}{f'(a)}\,(x-a)$ (si $f'(a)=0$, la normal es la recta vertical $x=a$)."),
     tasks(1, [r"$f(2)=1$, $f'(x)=3x^2-4x$, $f'(2)=4$: \ tangente $\res{y=4x-7}$; \ normal $y-1=-\frac14(x-2)\Rightarrow\res{y=-\frac14x+\frac32}$",
               r"$f(0)=-1$, $f'(x)=\frac{3}{(x+1)^2}$, $f'(0)=3$: \ tangente $\res{y=3x-1}$; \ normal $\res{y=-\frac13x-1}$",
               r"$f(1)=0$, $f'(x)=\ln x+1$, $f'(1)=1$: \ tangente $\res{y=x-1}$; \ normal $\res{y=-x+1}$",
               r"$f(1)=1$, $f'(x)=2x\,e^{x^2-1}$, $f'(1)=2$: \ tangente $\res{y=2x-1}$; \ normal $\res{y=-\frac12x+\frac32}$"])),
 (2, r"Halla los puntos de la gráfica de $f(x)=x^3-6x^2+8$ en los que la recta tangente es paralela a la recta $y=-9x+4$ y escribe la ecuación de estas tangentes."
     + recorda(r"Las rectas paralelas tienen la misma pendiente: resolvemos $f'(x)=m$."),
     r"$f'(x)=3x^2-12x=-9\Rightarrow x^2-4x+3=0\Rightarrow x=1,\ x=3$. \ $f(1)=3$: $\res{y=-9x+12}$; \ $f(3)=-19$: $\res{y=-9x+8}$."),
 (2, r"Calcula el punto de la gráfica de $f(x)=\sqrt{2x+1}$ en el que la recta normal es paralela a la recta $y=-3x$. Escribe la ecuación de esta recta normal.",
     r"$-\frac{1}{f'(a)}=-3\Rightarrow f'(a)=\frac13$. \ $f'(x)=\frac{1}{\sqrt{2x+1}}=\frac13\Rightarrow2x+1=9\Rightarrow x=4$, punto $\res{(4,3)}$. \ Normal: $y-3=-3(x-4)\Rightarrow\res{y=-3x+15}$."),
 (1, r"\pau{Madrid, EvAU julio 2019} Se considera la función $f(x)=2x^3-8x$. Determina en qué puntos la tangente a la curva $y=f(x)$ es horizontal.",
     r"$f'(x)=6x^2-8=0\Rightarrow x=\pm\frac{2}{\sqrt3}=\pm\frac{2\sqrt3}{3}$. \ Puntos $\res{\left(\frac{2\sqrt3}{3},-\frac{32\sqrt3}{9}\right)}$ y $\res{\left(-\frac{2\sqrt3}{3},\frac{32\sqrt3}{9}\right)}$."),
 (2, r"\pau{Cataluña, PAU junio 2019} La gráfica de la función $f(x)=ax+b+\dfrac8x$ pasa por el punto $(-2,-6)$ y la recta tangente en este punto es paralela al eje de abscisas. Calcula los valores de $a$ y de $b$.",
     r"Tangente horizontal: $f'(x)=a-\frac{8}{x^2}\Rightarrow f'(-2)=a-2=0\Rightarrow\res{a=2}$. \ $f(-2)=-4+b-4=-6\Rightarrow\res{b=2}$."),
 (2, r"\pau{Andalucía, PEvAU junio 2018} Considera la función" + dm(pw((r'x^3+ax^2', 'x<1'), (r'bx+\dfrac2x', r'x\geq1'))) + tasks(1, [r"Calcula los valores de $a$ y $b$ para que la función sea continua y derivable en $x=1$.", r"Para $b=3$, determina la ecuación de la recta tangente a la gráfica de la función en el punto de abscisa $x=2$."]),
     tasks(1, [r"Continuidad: $1+a=b+2$. \ Derivabilidad: $3+2a=b-2$. \ $\res{a=-6,\ b=-7}$.",
               r"En $x=2$ usamos $f(x)=3x+\frac2x$: $f(2)=7$, $f'(x)=3-\frac{2}{x^2}$, $f'(2)=\frac52$: \ $y-7=\frac52(x-2)\Rightarrow\res{5x-2y+4=0}$."])),
 (1, r"\pau{Murcia, EBAU septiembre 2019} Dada la función $f(x)=2e^{x+1}$, halla la ecuación de la recta tangente a la función en el punto $x=1$.",
     r"$f(1)=2e^2$, $f'(x)=2e^{x+1}$, $f'(1)=2e^2$: \ $y-2e^2=2e^2(x-1)\Rightarrow\res{y=2e^2x}$."),
]))

S.append(("Monotonía de una función", [
 (1, r"Estudia la monotonía (intervalos de crecimiento y de decrecimiento) de las funciones polinómicas siguientes:" + tasks(2, [fx(r'x^3-3x^2-9x+5'), fx(r'x^4-8x^2'), fx(r'-x^3+3x+1'), fx(r'x^3+3x')])
     + recorda(r"1) Dominio. 2) Calculamos $f'(x)$ y la factorizamos. 3) Resolvemos $f'(x)=0$ y añadimos los puntos fuera del dominio. 4) Miramos el signo de $f'$ en cada intervalo con un valor de prueba: $f'>0\Rightarrow$ creciente, $f'<0\Rightarrow$ decreciente."),
     tasks(1, [r"$f'(x)=3(x+1)(x-3)$: creciente en $\res{(-\infty,-1)\cup(3,+\infty)}$, decreciente en $\res{(-1,3)}$.",
               r"$f'(x)=4x(x+2)(x-2)$: decreciente en $\res{(-\infty,-2)\cup(0,2)}$, creciente en $\res{(-2,0)\cup(2,+\infty)}$.",
               r"$f'(x)=-3(x+1)(x-1)$: decreciente en $\res{(-\infty,-1)\cup(1,+\infty)}$, creciente en $\res{(-1,1)}$.",
               r"$f'(x)=3x^2+3>0$ siempre: \rest{creciente en todo $\mathbb R$}."])),
 (2, r"Estudia la monotonía de las funciones racionales siguientes (cuidado con los puntos que no son del dominio):" + tasks(2, [fx(r'\dfrac{x}{x-2}'), fx(r'\dfrac{x^2+1}{x}'), fx(r'\dfrac{1}{x^2+1}'), fx(r'\dfrac{x^2}{x^2-1}')]),
     tasks(1, [r"$f'(x)=\frac{-2}{(x-2)^2}<0$: decreciente en $\res{(-\infty,2)}$ y en $\res{(2,+\infty)}$.",
               r"$f'(x)=\frac{x^2-1}{x^2}$: creciente en $\res{(-\infty,-1)\cup(1,+\infty)}$, decreciente en $\res{(-1,0)\cup(0,1)}$.",
               r"$f'(x)=\frac{-2x}{(x^2+1)^2}$: creciente en $\res{(-\infty,0)}$, decreciente en $\res{(0,+\infty)}$.",
               r"$f'(x)=\frac{-2x}{(x^2-1)^2}$: creciente en $\res{(-\infty,-1)\cup(-1,0)}$, decreciente en $\res{(0,1)\cup(1,+\infty)}$."])),
 (2, r"Estudia la monotonía de las funciones exponenciales y logarítmicas siguientes:" + tasks(2, [fx(r'x^2e^x'), fx(r'\dfrac{e^x}{x}'), fx(r'\ln(x^2+4)'), fx(r'x^2-2\ln x')])
     + recorda(r"$e^{g(x)}>0$ siempre y los cuadrados del denominador también: no cambian el signo de $f'$."),
     tasks(1, [r"$f'(x)=x(x+2)e^x$: creciente en $\res{(-\infty,-2)\cup(0,+\infty)}$, decreciente en $\res{(-2,0)}$.",
               r"$f'(x)=\frac{e^x(x-1)}{x^2}$: decreciente en $\res{(-\infty,0)\cup(0,1)}$, creciente en $\res{(1,+\infty)}$.",
               r"$f'(x)=\frac{2x}{x^2+4}$: decreciente en $\res{(-\infty,0)}$, creciente en $\res{(0,+\infty)}$.",
               r"Dominio $(0,+\infty)$. $f'(x)=2x-\frac2x=\frac{2(x^2-1)}{x}$: decreciente en $\res{(0,1)}$, creciente en $\res{(1,+\infty)}$."])),
 (1, r"Observa la gráfica de la función $f$ y responde:" + '\n\n\\begin{center}' + G_LECT + '\\end{center}' + tasks(1, [r"¿En qué intervalos es creciente? ¿Y decreciente?", r"¿Cuáles son los máximos y los mínimos relativos?", r"¿Qué signo tienen $f'(0)$ y $f'(2)$? ¿Cuánto vale $f'(-1)$?"]),
     tasks(1, [r"Creciente en $\res{(-\infty,-1)\cup(1,+\infty)}$ y decreciente en $\res{(-1,1)}$.", r"Máximo relativo $\res{(-1,2)}$ y mínimo relativo $\res{(1,-2)}$.", r"$\res{f'(0)<0}$ (decrece), $\res{f'(2)>0}$ (crece) y $\res{f'(-1)=0}$ (tangente horizontal)."])),
 (2, r"\pau{Madrid, EvAU junio 2018} Se considera la función $f(x)=\dfrac{x^3}{(x+1)^2}$." + tasks(1, [r"Calcula su dominio.", r"Determina sus intervalos de crecimiento y de decrecimiento."]),
     tasks(1, [r"$\res{\mathbb R-\{-1\}}$", r"$f'(x)=\frac{3x^2(x+1)^2-2x^3(x+1)}{(x+1)^4}=\frac{x^2(x+3)}{(x+1)^3}$. Creciente en $\res{(-\infty,-3)\cup(-1,+\infty)}$ y decreciente en $\res{(-3,-1)}$. (En $x=0$, $f'=0$ pero no cambia de signo.)"])),
 (2, r"\pau{Islas Baleares, PBAU ordinaria 2021} Dada la función $f(x)=ax^3+bx^2+x$, definida para todo $x\in\mathbb R$:" + tasks(1, [r"Halla $a$ y $b$ sabiendo que $f(x)$ tiene un punto crítico en $x=1$ y que su gráfica pasa por el punto $(3,0)$.", r"Estudia el crecimiento y el decrecimiento de $f(x)$ para $a=3$ y $b=3$."]),
     tasks(1, [r"$f'(1)=3a+2b+1=0$ y $f(3)=27a+9b+3=0$: \ $\res{a=\frac19,\ b=-\frac23}$.", r"$f'(x)=9x^2+6x+1=(3x+1)^2\geq0$: \rest{creciente en todo $\mathbb R$} (en $x=-\frac13$ la tangente es horizontal, pero no hay extremo)."])),
 (2, r"\pau{Canarias, EBAU junio 2017} Una máquina de revelado pasa a papel 13 fotografías por minuto, pero sus cualidades se deterioran con el tiempo. El número de fotografías por minuto, en función de los años $x$ transcurridos desde la compra, es" + dm(pw((r'-0{,}5x+13', r'0\leq x\leq6'), (r'\dfrac{5(x+14)}{x+4}', 'x>6'))) + tasks(1, [r"Comprueba que el número de fotografías por minuto decrece con el paso de los años.", r"Justifica que a partir de los 6 años revelará menos de 10 fotografías por minuto y que no revelará menos de 5 por muy vieja que sea la máquina."]),
     tasks(1, [r"$f'(x)=-0{,}5<0$ si $0<x<6$ y $f'(x)=\frac{5(x+4)-5(x+14)}{(x+4)^2}=\frac{-50}{(x+4)^2}<0$ si $x>6$: \rest{siempre decrece}.", r"$f(6)=10$ y es decreciente: después revela \rest{menos de 10}. $\lim_{x\to+\infty}\frac{5(x+14)}{x+4}=5$ y se acerca por arriba: \rest{nunca menos de 5}."])),
]))

S.append(("Máximos y mínimos relativos", [
 (1, r"Calcula los máximos y mínimos relativos de las funciones siguientes usando la segunda derivada:" + tasks(2, [fx(r'2x^3-9x^2+12x-4'), fx(r'x^4-2x^2+3'), fx(r'x+\dfrac1x'), fx(r'x\,e^{-x}')])
     + recorda(r"Candidatos: $f'(x)=0$. \ Si $f''(a)<0$, máximo; si $f''(a)>0$, mínimo; si $f''(a)=0$, estudiamos el cambio de signo de $f'$. Da el resultado como punto $(a,f(a))$."),
     tasks(1, [r"$f'(x)=6(x-1)(x-2)$, $f''(x)=12x-18$: \ máximo $\res{(1,1)}$, mínimo $\res{(2,0)}$.",
               r"$f'(x)=4x(x^2-1)$, $f''(x)=12x^2-4$: \ máximo $\res{(0,3)}$, mínimos $\res{(-1,2)}$ y $\res{(1,2)}$.",
               r"$f'(x)=1-\frac{1}{x^2}$, $f''(x)=\frac{2}{x^3}$: \ máximo $\res{(-1,-2)}$, mínimo $\res{(1,2)}$.",
               r"$f'(x)=e^{-x}(1-x)$, $f''(x)=e^{-x}(x-2)$, $f''(1)=-\frac1e<0$: \ máximo $\res{\left(1,\frac1e\right)}$."])),
 (2, r"Estudia los extremos relativos de $f(x)=3x^4-4x^3$. ¿Qué ocurre en $x=0$?",
     r"$f'(x)=12x^3-12x^2=12x^2(x-1)=0\Rightarrow x=0,\ x=1$. \ $f''(x)=36x^2-24x$: $f''(1)=12>0$, mínimo $\res{(1,-1)}$. \ $f''(0)=0$ no decide: $f'<0$ a la izquierda y a la derecha de 0 (no cambia de signo), así que en $x=0$ \rest{no hay extremo}."),
 (1, r"\pau{La Rioja, EBAU julio 2017} Sea $f(x)=2x^3-3x^2-12x-7$." + tasks(1, [r"Estudia los intervalos de crecimiento y de decrecimiento de la función.", r"Determina los extremos relativos de la función."]),
     tasks(1, [r"$f'(x)=6(x+1)(x-2)$: creciente en $\res{(-\infty,-1)\cup(2,+\infty)}$, decreciente en $\res{(-1,2)}$.", r"Máximo relativo $\res{(-1,0)}$ y mínimo relativo $\res{(2,-27)}$."])),
 (1, r"\pau{Navarra, EvAU ordinaria 2020} Sea la función $y=x^3-3x^2$. Calcula los intervalos de crecimiento y de decrecimiento, y los máximos y mínimos.",
     r"$y'=3x(x-2)$: creciente en $\res{(-\infty,0)\cup(2,+\infty)}$, decreciente en $\res{(0,2)}$. Máximo $\res{(0,0)}$ y mínimo $\res{(2,-4)}$."),
 (1, r"\pau{País Vasco, EAU junio 2019} Se considera la curva $f(x)=x^3-6x^2+9x$." + tasks(1, [r"Estudia los intervalos de crecimiento y de decrecimiento de la función.", r"Determina los máximos y mínimos relativos."]),
     tasks(1, [r"$f'(x)=3(x-1)(x-3)$: creciente en $\res{(-\infty,1)\cup(3,+\infty)}$, decreciente en $\res{(1,3)}$.", r"Máximo relativo $\res{(1,4)}$ y mínimo relativo $\res{(3,0)}$."])),
 (2, r"\pau{Cataluña, PAU ordinaria 2021} Considera la función $f(x)=4x^3+ax^2-2$." + tasks(1, [r"Determina el valor del parámetro $a$ para que la función tenga un extremo relativo en el punto de abscisa $x=-1$.", r"Calcula los intervalos de crecimiento y de decrecimiento de $f(x)$ cuando $a=12$. Indica también los extremos relativos y clasifícalos."]),
     tasks(1, [r"$f'(x)=12x^2+2ax$, $f'(-1)=12-2a=0\Rightarrow\res{a=6}$.", r"$f'(x)=12x(x+2)$: creciente en $\res{(-\infty,-2)\cup(0,+\infty)}$, decreciente en $\res{(-2,0)}$. Máximo $\res{(-2,14)}$ y mínimo $\res{(0,-2)}$."])),
 (2, r"\pau{Murcia, EBAU julio 2020} Sea la función $f(x)=x^3+ax^2+bx+1$." + tasks(1, [r"Determina los valores de $a$ y $b$ para que la función tenga un extremo relativo en $x=1$ y la recta tangente a la gráfica en el punto de abscisa $x=0$ tenga pendiente $m=-1$.", r"Si $a=-2$ y $b=-4$, determina los intervalos de crecimiento y de decrecimiento y los extremos relativos."]),
     tasks(1, [r"$f'(0)=b=-1$ y $f'(1)=3+2a+b=0$: \ $\res{a=-1,\ b=-1}$.", r"$f'(x)=3x^2-4x-4=(3x+2)(x-2)$: creciente en $\res{\left(-\infty,-\frac23\right)\cup(2,+\infty)}$, decreciente en $\res{\left(-\frac23,2\right)}$. Máximo $\res{\left(-\frac23,\frac{67}{27}\right)}$ y mínimo $\res{(2,-7)}$."])),
 (2, r"\pau{País Vasco, EAU julio 2019} Sea la función $f(x)=x^3+ax^2+bx+c$. Halla los valores de $a$, $b$ y $c$ para que la función pase por el punto $(0,0)$ y tenga un extremo relativo en el punto $(2,-4)$. Determina después sus máximos y mínimos.",
     r"$f(0)=c=0$; \ $f(2)=8+4a+2b=-4$; \ $f'(2)=12+4a+b=0$. \ $\res{a=-3,\ b=0,\ c=0}$. \ $f'(x)=3x(x-2)$: máximo $\res{(0,0)}$ y mínimo $\res{(2,-4)}$."),
 (2, r"\pau{La Rioja, EBAU ordinaria 2020} Consideremos la función $f(x)=x^4-ax^2+b$." + tasks(1, [r"¿Qué valores deben tomar $a$ y $b$ para que la función tenga un mínimo en el punto $(1,0)$?", r"Con estos valores, calcula los puntos en los que $f(x)$ tiene tangente paralela a la recta $y=1$.", r"Calcula la recta tangente a la función en el punto $x=1$."]),
     tasks(1, [r"$f'(1)=4-2a=0\Rightarrow a=2$; \ $f(1)=1-2+b=0\Rightarrow b=1$: \ $\res{a=2,\ b=1}$.", r"Pendiente 0: $f'(x)=4x^3-4x=0\Rightarrow x=0,\pm1$: puntos $\res{(0,1)}$, $\res{(-1,0)}$ y $\res{(1,0)}$.", r"$f(1)=0$ y $f'(1)=0$: $\res{y=0}$."])),
 (3, r"\pau{Murcia, EBAU septiembre 2019} Determina el punto de la gráfica de la función $f(x)=-x^3+6x^2-7x+5$ en el que la pendiente de la recta tangente es máxima. ¿Cuál es la ecuación de la recta tangente en este punto?",
     r"La pendiente es $m(x)=f'(x)=-3x^2+12x-7$. $m'(x)=-6x+12=0\Rightarrow x=2$ y $m''=-6<0$: máximo. \ $f(2)=7$, $f'(2)=5$: punto $\res{(2,7)}$ y tangente $\res{y=5x-3}$."),
]))

S.append(("Extremos absolutos en un intervalo cerrado", [
 (1, r"Calcula el máximo y el mínimo absolutos de cada función en el intervalo indicado:" + tasks(1, [fx(r'x^3-3x') + r' en $[0,2]$', fx(r'x^2-6x+5') + r' en $[-1,4]$', fx(r'x+\dfrac4x') + r' en $[1,5]$'])
     + recorda(r"Comparamos el valor de $f$ en los puntos críticos de dentro del intervalo y en los extremos del intervalo."),
     tasks(1, [r"$f'(x)=3(x^2-1)\Rightarrow x=1$. \ $f(0)=0$, $f(1)=-2$, $f(2)=2$: máximo $\res{2}$ en $x=2$ y mínimo $\res{-2}$ en $x=1$.",
               r"$f'(x)=2x-6\Rightarrow x=3$. \ $f(-1)=12$, $f(3)=-4$, $f(4)=-3$: máximo $\res{12}$ en $x=-1$ y mínimo $\res{-4}$ en $x=3$.",
               r"$f'(x)=1-\frac{4}{x^2}\Rightarrow x=2$ ($-2$ no es del intervalo). \ $f(1)=5$, $f(2)=4$, $f(5)=5{,}8$: máximo $\res{5{,}8}$ en $x=5$ y mínimo $\res{4}$ en $x=2$."])),
 (2, r"\pau{Andalucía, PEvAU septiembre 2018} El consumo de cereales en una ciudad, en miles de toneladas, viene dado por la función $c(t)=t^3-15t^2+63t+10$, para $0\leq t\leq12$, donde $t$ representa el tiempo." + tasks(1, [r"¿En qué instante se alcanza el máximo consumo de cereales y cuántas toneladas se consumen en ese momento?", r"¿En qué intervalo de tiempo decrece el consumo de cereales?"]),
     tasks(1, [r"$c'(t)=3(t-3)(t-7)$. \ $c(0)=10$, $c(3)=91$, $c(7)=59$, $c(12)=334$: el máximo es en $\res{t=12}$, con $\res{334\,000}$ toneladas.", r"Decrece en $\res{(3,7)}$."])),
 (2, r"\pau{Extremadura, EBAU ordinaria 2020} El gasto $G$ (en euros) por el consumo de energía eléctrica en un taller durante las 8 horas de funcionamiento varía de acuerdo con la función $G(t)=2t^3-27t^2+84t+60$, $0\leq t\leq8$, donde $t$ es el tiempo transcurrido en horas. Determina a qué horas se producen los gastos máximo y mínimo y los valores de estos gastos.",
     r"$G'(t)=6(t-2)(t-7)$. \ $G(0)=60$, $G(2)=136$, $G(7)=11$, $G(8)=28$. \ Gasto máximo a las $\res{2\text{ h}}$ ($\res{136}$ €) y mínimo a las $\res{7\text{ h}}$ ($\res{11}$ €)."),
 (2, r"\pau{Extremadura, EBAU julio 2019} La potencia requerida por la maquinaria eléctrica de una empresa durante las 10 horas de funcionamiento viene dada por $P(t)=-t^3+15t^2-48t+50$, $0\leq t\leq10$, donde $t$ es el tiempo en horas y $P(t)$ la potencia en kilovatios. Determina a qué horas se producen el máximo y el mínimo de esta potencia y calcula sus valores.",
     r"$P'(t)=-3(t-2)(t-8)$. \ $P(0)=50$, $P(2)=6$, $P(8)=114$, $P(10)=70$. \ Mínimo a las $\res{2\text{ h}}$ ($\res{6}$ kW) y máximo a las $\res{8\text{ h}}$ ($\res{114}$ kW)."),
 (2, r"\pau{Aragón, EvAU ordinaria 2020} El coste unitario de fabricación de un producto (en euros) depende del volumen de producción según la fórmula $C(x)=\dfrac{1}{10}\left(x^2-16x+100\right)$, donde $x\in[2,15]$ es el volumen de producción (en miles de unidades)." + tasks(1, [r"Si se producen 5\,000 unidades, ¿cuánto vale el coste unitario?", r"¿Para qué volumen de producción se alcanza el coste unitario mínimo? ¿Y el máximo? ¿Cuánto valen estos costes?"]),
     tasks(1, [r"$C(5)=\res{4{,}5}$ €.", r"$C'(x)=\frac{2x-16}{10}=0\Rightarrow x=8$. \ $C(2)=7{,}2$, $C(8)=3{,}6$, $C(15)=8{,}5$: mínimo con $\res{8\,000}$ unidades ($\res{3{,}6}$ €) y máximo con $\res{15\,000}$ unidades ($\res{8{,}5}$ €)."])),
 (2, r"\pau{Navarra, EvAU junio 2019} El beneficio de una empresa, en miles de euros, viene dado por $f(x)=-3x^2+30x+20$, con $0\leq x\leq8$, donde $x$ es el gasto en publicidad, en miles de euros." + tasks(1, [r"¿Cuál es el beneficio si la empresa no gasta en publicidad? ¿Y si gasta 1\,000 euros?", r"Determina el gasto en publicidad que produce el beneficio máximo. ¿Cuál es ese beneficio?", r"Explica cómo aumenta o disminuye el beneficio en función del gasto en publicidad.", r"¿Cuánto gasta la empresa en publicidad cuando el beneficio es mínimo? ¿A cuánto asciende?"]),
     tasks(1, [r"$f(0)=\res{20\,000}$ €; \ $f(1)=\res{47\,000}$ €.", r"$f'(x)=-6x+30=0\Rightarrow x=5$, $f''=-6<0$: gastando $\res{5\,000}$ € el beneficio es máximo, $\res{95\,000}$ €.", r"Crece en $\res{(0,5)}$ y decrece en $\res{(5,8)}$.", r"$f(0)=20$, $f(8)=68$: el mínimo es sin gastar en publicidad ($\res{x=0}$), $\res{20\,000}$ €."])),
 (3, r"\pau{Andalucía, PEvAU septiembre 2018} El beneficio, en miles de euros, que ha obtenido una almazara a lo largo de 50 años viene dado por la función continua" + dm(pw((r"-0{,}04t^2+2{,}4t", r'0\leq t\leq40'), (r"\dfrac{40t-320}{t}", r'40<t\leq50'), name='B(t)')) + r"donde $t$ es el tiempo transcurrido. Estudia la monotonía de $B(t)$ y determina en qué momento fueron mayores los beneficios de la almazara, así como el beneficio máximo.",
     r"$B'(t)=-0{,}08t+2{,}4$ si $0<t<40$ (cero en $t=30$) y $B'(t)=\frac{320}{t^2}>0$ si $40<t<50$. Crece en $\res{(0,30)\cup(40,50)}$ y decrece en $\res{(30,40)}$. \ $B(0)=0$, $B(30)=36$, $B(40)=32$, $B(50)=33{,}6$: máximo en el año $\res{t=30}$, con $\res{36\,000}$ €."),
 (2, r"\pau{Canarias, EBAU julio 2019} El beneficio de un parque acuático, en millones de euros, a lo largo del último año dividido en meses es" + dm(pw((r'\dfrac{x+8}{2}', r'0\leq x\leq4'), (r'-x^2+12x-26', r'4<x\leq8'), (r'6', r'8<x\leq12'))) + tasks(1, [r"¿Cuándo ha crecido y cuándo ha decrecido el beneficio?", r"¿En qué momentos se obtuvieron los beneficios máximo y mínimo y a cuánto ascendían?"]),
     tasks(1, [r"$f'(x)=\frac12>0$ en $(0,4)$ y $f'(x)=-2x+12$ en $(4,8)$: crece en $\res{(0,6)}$, decrece en $\res{(6,8)}$ y es constante en $(8,12)$.", r"$f(0)=4$, $f(6)=10$: máximo en el mes $\res{6}$ ($\res{10}$ millones de €) y mínimo en el mes $\res{0}$ ($\res{4}$ millones de €)."])),
 (2, r"\pau{Islas Baleares, PBAU julio 2018} Los beneficios (en miles de euros) por la venta de un producto en función de la inversión en promoción $x$ (en miles de euros) vienen dados por la función continua" + dm(pw((r'5x+15', r'0\leq x\leq3'), (r'-(x-3)^2+30', r'3<x\leq8'), name='B(x)')) + tasks(1, [r"Determina sus intervalos de crecimiento y de decrecimiento.", r"Determina su beneficio máximo y su beneficio mínimo."]),
     tasks(1, [r"$B'(x)=5>0$ en $(0,3)$ y $B'(x)=-2(x-3)<0$ en $(3,8)$: crece en $\res{(0,3)}$ y decrece en $\res{(3,8)}$.", r"$B(0)=15$, $B(3)=30$, $B(8)=5$: máximo en $x=3$ ($\res{30\,000}$ €) y mínimo en $x=8$ ($\res{5\,000}$ €)."])),
]))

S.append(("Problemas de optimización: conocemos la función", [
 (1, r"\pau{Andalucía, PEvAU junio 2018} La función de costes de una empresa es $f(x)=40-6x+x^2$, para $x\geq0$, donde $x$ representa la cantidad producida de un artículo. ¿Disminuye el coste alguna vez? Determina la cantidad producida cuando el coste es mínimo y cuál es ese coste."
     + recorda(r"Derivamos, igualamos a cero, justificamos si es máximo o mínimo (segunda derivada o monotonía) y respondemos a la pregunta con las unidades."),
     r"$f'(x)=2x-6$: el coste disminuye para $\res{0<x<3}$. \ $f''=2>0$: el coste es mínimo con $\res{x=3}$ artículos, y vale $\res{f(3)=31}$."),
 (1, r"\pau{Castilla y León, EBAU julio 2019} La capacidad de atención de un alumno en una clase de 60 minutos viene dada por $f(t)=-2t^2+120t+5$, con $t\in[0,60]$." + tasks(1, [r"Calcula la capacidad de atención cuando lleva una hora de clase.", r"¿En qué instante la capacidad de atención es máxima? ¿Cuál es esa capacidad máxima?"]),
     tasks(1, [r"$f(60)=\res{5}$.", r"$f'(t)=-4t+120=0\Rightarrow t=30$, $f''=-4<0$: a los $\res{30}$ minutos, con una atención de $\res{1\,805}$."])),
 (1, r"\pau{Murcia, EBAU julio 2020} El beneficio semanal de una empresa de ordenadores viene dado por $B(x)=-2x^2+24x-36$, donde $x$ es el número de ordenadores vendidos cada semana. Calcula el número de ordenadores que hay que vender cada semana para que el beneficio sea máximo. ¿Cuál es ese beneficio?",
     r"$B'(x)=-4x+24=0\Rightarrow x=6$, $B''=-4<0$: vendiendo $\res{6}$ ordenadores, beneficio máximo $\res{36}$."),
 (1, r"\pau{Islas Baleares, PBAU ordinaria 2021} El beneficio, en euros, que obtiene una empresa por la venta de $x$ unidades de un producto es $B(x)=-x^2+300x-16\,100$, para $x\geq0$." + tasks(1, [r"Calcula el beneficio si se venden 110 unidades.", r"¿Cuántas unidades debe vender para que el beneficio sea máximo? ¿Cuál es ese beneficio?"]),
     tasks(1, [r"$B(110)=\res{4\,800}$ €.", r"$B'(x)=-2x+300=0\Rightarrow x=150$, $B''<0$: $\res{150}$ unidades y $\res{6\,400}$ €."])),
 (2, r"\pau{Islas Baleares, PBAU ordinaria 2020} En una empresa se pueden producir hasta 500 mesas al mes. El coste de producir $q$ mesas es $C(q)=\dfrac{q^3}{50}+8q+40$, y el coste medio de cada mesa es $Q(q)=\dfrac{C(q)}{q}$." + tasks(1, [r"Calcula el coste medio de cada mesa si la empresa produce 5. ¿Y si produce 20?", r"Determina cuántas mesas hay que producir para que el coste medio sea mínimo. Justifica que se trata de un mínimo y calcula ese coste medio."]),
     tasks(1, [r"$Q(q)=\frac{q^2}{50}+8+\frac{40}{q}$: \ $Q(5)=\res{16{,}5}$ €, \ $Q(20)=\res{18}$ €.", r"$Q'(q)=\frac{q}{25}-\frac{40}{q^2}=0\Rightarrow q^3=1000\Rightarrow q=10$; \ $Q''(q)=\frac{1}{25}+\frac{80}{q^3}>0$: mínimo con $\res{10}$ mesas, coste medio $\res{14}$ €."])),
 (2, r"\pau{Cataluña, PAU ordinaria 2021} Una fábrica estima que el beneficio mensual, en miles de euros, por cada tonelada de confeti vendida es $f(x)=\dfrac{-0{,}2x^2+5x-20}{x}$, donde $x$ es el número de toneladas vendidas." + tasks(1, [r"Determina en qué intervalo de valores debe estar $x$ para que la fábrica no tenga pérdidas.", r"Calcula la cantidad de toneladas que proporciona el beneficio máximo y cuál es ese beneficio."]),
     tasks(1, [r"$-0{,}2x^2+5x-20\geq0\Leftrightarrow x^2-25x+100\leq0$: entre $\res{5}$ y $\res{20}$ toneladas.", r"$f(x)=-0{,}2x+5-\frac{20}{x}$, $f'(x)=-0{,}2+\frac{20}{x^2}=0\Rightarrow x=10$, $f''(10)<0$: $\res{10}$ toneladas, $\res{f(10)=1}$ (1\,000 €)."])),
 (2, r"\pau{Aragón, EvAU ordinaria 2021} Unos emprendedores estiman que los beneficios, en cientos de miles de euros, vendrán dados por $B(t)=\dfrac{2t-6}{t+4}$, donde $t$ son los años transcurridos desde la apertura." + tasks(1, [r"¿En qué intervalo tendrá pérdidas la empresa?", r"¿En qué momento $t\in[3,10]$ se alcanza el beneficio máximo y a cuántos euros asciende? Justifícalo.", r"¿Cuánto tiempo debe pasar para obtener un beneficio de 150\,000 €?"]),
     tasks(1, [r"$B(t)<0\Leftrightarrow 2t-6<0$: durante los $\res{3}$ primeros años.", r"$B'(t)=\frac{14}{(t+4)^2}>0$: es creciente, así que el máximo es en $\res{t=10}$, con $B(10)=1$, es decir, $\res{100\,000}$ €.", r"$\frac{2t-6}{t+4}=1{,}5\Rightarrow t=\res{24}$ años."])),
 (2, r"\pau{Aragón, EvAU junio 2018} Una empresa debe decidir el precio de venta $x$ de un juguete, entre 1 y 10 euros. El beneficio, en millones de euros, será $B(x)=\dfrac9x-\dfrac{18}{x^2}-1$." + tasks(1, [r"¿Para qué valores de $x\in[1,10]$ el beneficio es positivo?", r"¿Qué precio de venta maximiza el beneficio? ¿Cuál es el beneficio máximo?"]),
     tasks(1, [r"$B(x)>0\Leftrightarrow x^2-9x+18<0$: $\res{x\in(3,6)}$.", r"$B'(x)=-\frac{9}{x^2}+\frac{36}{x^3}=0\Rightarrow x=4$. \ $B(1)=-10$, $B(4)=0{,}125$, $B(10)=-0{,}28$: precio de $\res{4}$ €, beneficio de $\res{125\,000}$ €."])),
 (2, r"\pau{Galicia, ABAU julio 2019} El precio de venta de un electrodoméstico (en cientos de euros) viene dado por $P(t)=\dfrac{44}{t^2-4t+16}+2$, donde $t$ es el tiempo en años desde que se puso a la venta." + tasks(1, [r"Calcula el precio de lanzamiento. ¿En qué momento el precio vuelve a ser el de lanzamiento?", r"Determina los períodos en los que el precio ha aumentado y ha disminuido. ¿Cuál ha sido el precio máximo y cuándo se ha producido?", r"Estudia la tendencia del precio con el paso del tiempo."]),
     tasks(1, [r"$P(0)=4{,}75$: $\res{475}$ €. \ $P(t)=4{,}75\Leftrightarrow t^2-4t=0$: a los $\res{4}$ años.", r"$P'(t)=\frac{-44(2t-4)}{(t^2-4t+16)^2}$: aumenta en $\res{(0,2)}$ y disminuye a partir de $\res{t=2}$. Máximo a los 2 años: $P(2)=\frac{17}{3}$, unos $\res{566{,}67}$ €.", r"$\lim_{t\to+\infty}P(t)=2$: tiende a $\res{200}$ €."])),
 (2, r"\pau{Asturias, EBAU julio 2019} Dos fuentes de energía A y B producen electricidad a la vez durante 6 horas. En un instante $x\in[0,6]$, la fuente A produce $f(x)=-x^2+6x+3$ y la fuente B, $g(x)=x+9$." + tasks(1, [r"¿En qué momentos producen ambas la misma cantidad de electricidad? ¿Cuál es esa producción?", r"¿En qué momentos decrece la producción de la fuente A?", r"¿En qué instante es máxima la producción conjunta de las dos fuentes?"]),
     tasks(1, [r"$-x^2+6x+3=x+9\Rightarrow x^2-5x+6=0$: a las $\res{2}$ h (11 unidades) y a las $\res{3}$ h (12 unidades).", r"$f'(x)=-2x+6<0$ si $x>3$: decrece en $\res{(3,6)}$.", r"$h(x)=f(x)+g(x)=-x^2+7x+12$, $h'(x)=-2x+7=0$: a las $\res{3{,}5}$ h."])),
]))

S.append(("Problemas de optimización: construimos la función", [
 (1, r"\pau{Castilla y León, EBAU septiembre 2017} Halla razonadamente dos números reales positivos sabiendo que su suma es 10 y que el producto de sus cuadrados es máximo."
     + recorda(r"1) Variables y ecuación que las relaciona (despejamos una). 2) Función que hay que optimizar, de una sola variable. 3) Derivamos e igualamos a 0. 4) Comprobamos si es máximo o mínimo. 5) Calculamos la otra variable e interpretamos el resultado."),
     r"$y=10-x$, \ $P(x)=x^2(10-x)^2$. \ $P'(x)=2x(10-x)^2-2x^2(10-x)=2x(10-x)(10-2x)=0\Rightarrow x=5$ (los otros valores hacen $P=0$). Los números son $\res{5}$ y $\res{5}$."),
 (1, r"\pau{Cataluña, PAU ordinaria 2021} Un granjero quiere construir un corral rectangular para los conejos y solo dispone de 40 m de valla. Llamamos $x$ a la anchura del corral e $y$ a la longitud." + tasks(1, [r"Escribe la función que da el área del corral en función solo de la anchura $x$.", r"¿Cuáles deben ser la anchura y la longitud para que el área sea máxima? ¿Cuál es esa área?"]),
     tasks(1, [r"$2x+2y=40\Rightarrow y=20-x$: \ $\res{A(x)=20x-x^2}$.", r"$A'(x)=20-2x=0\Rightarrow x=10$, $A''<0$: un cuadrado de $\res{10\times10}$ m, con $\res{100}$ m²."])),
 (2, r"\pau{La Rioja, EBAU julio 2017} Queremos construir un campo rectangular de 3\,200 m² a lo largo de un río; no hace falta vallar el lado de la orilla." + tasks(1, [r"¿Qué dimensiones debe tener el campo para que se necesite el mínimo posible de metros de valla?", r"Determina el coste del vallado si cada metro perpendicular al río cuesta 500 € y cada metro paralelo al río, 400 €."]),
     tasks(1, [r"$x$: lados perpendiculares, $y$: lado paralelo. $xy=3200$, $L(x)=2x+\frac{3200}{x}$, $L'(x)=2-\frac{3200}{x^2}=0\Rightarrow x=40$, $L''>0$: $\res{40}$ m perpendicular y $\res{80}$ m paralelo al río.", r"$2\cdot40\cdot500+80\cdot400=\res{72\,000}$ €."])),
 (3, r"\pau{La Rioja, EBAU junio 2018} Consideremos un rectángulo de lados $x$ e $y$." + tasks(1, [r"Halla el rectángulo de perímetro mínimo si los lados verifican la relación $xy^2=4$.", r"Halla el rectángulo de área máxima si los lados verifican la relación $x+3y^2=1$."]),
     tasks(1, [r"$x=\frac{4}{y^2}$, $P(y)=\frac{8}{y^2}+2y$, $P'(y)=-\frac{16}{y^3}+2=0\Rightarrow y=2$: $\res{x=1,\ y=2}$.", r"$x=1-3y^2$, $A(y)=y-3y^3$, $A'(y)=1-9y^2=0\Rightarrow y=\frac13$: $\res{x=\frac23,\ y=\frac13}$."])),
 (2, r"\pau{Murcia, EBAU junio 2019} Una empresa vende un artículo a 40 euros la unidad y tiene la función de coste $C(x)=2x^2+4x+98$, donde $x$ es el número de unidades producidas. Calcula el número de unidades que debe vender para que el beneficio (ingresos menos costes) sea máximo y ese beneficio máximo.",
     r"$B(x)=40x-(2x^2+4x+98)=-2x^2+36x-98$, $B'(x)=-4x+36=0\Rightarrow x=9$, $B''<0$: $\res{9}$ unidades y $\res{64}$ €."),
 (2, r"\pau{Murcia, EBAU junio 2018} Una empresa vende un producto a 15 euros la unidad. La función de costes es $C(x)=2x^2-45x+100$, donde $x$ es el número de unidades. Halla el número de unidades que debe vender para obtener el beneficio máximo y calcula ese beneficio.",
     r"$B(x)=15x-C(x)=-2x^2+60x-100$, $B'(x)=-4x+60=0\Rightarrow x=15$, $B''<0$: $\res{15}$ unidades y $\res{350}$ u.m."),
 (2, r"\pau{Murcia, EBAU ordinaria 2021} El coste de producción de $x$ unidades de un producto es $C(x)=\dfrac14x^2+35x+25$ y el precio de venta es $p=50-\dfrac x4$ euros. Halla:" + tasks(1, [r"El número de unidades que hay que vender diariamente para que el beneficio sea máximo.", r"El precio al que se deben vender estas unidades.", r"El beneficio máximo."]),
     tasks(1, [r"$B(x)=x\left(50-\frac x4\right)-\frac{x^2}{4}-35x-25=-\frac{x^2}{2}+15x-25$, $B'(x)=-x+15=0$: $\res{15}$ unidades.", r"$p=50-\frac{15}{4}=\res{46{,}25}$ €.", r"$B(15)=\res{87{,}5}$ €."])),
 (2, r"\pau{Galicia, ABAU extraordinaria 2021} Una empresa puede vender $x$ unidades al mes de un producto al precio de $518-x^2$ euros la unidad. Tiene unos gastos mensuales fijos de 225 € y otros de $275x$ euros." + tasks(1, [r"Determina las funciones $I(x)$ y $B(x)$ de los ingresos y de los beneficios. ¿Qué beneficio se obtiene si se venden 10 unidades?", r"Calcula el número de unidades que se deben producir para obtener el beneficio máximo. ¿A cuánto ascendería? ¿Cuál sería el precio de una unidad?"]),
     tasks(1, [r"$\res{I(x)=518x-x^3}$, \ $\res{B(x)=-x^3+243x-225}$; \ $B(10)=\res{1\,205}$ €.", r"$B'(x)=-3x^2+243=0\Rightarrow x=9$, $B''(9)=-54<0$: $\res{9}$ unidades, beneficio $\res{1\,233}$ €, precio $\res{437}$ €."])),
 (3, r"\pau{Cataluña, PAU ordinaria 2020} Elaborar un menú en un restaurante cuesta 8 €. Si el precio del menú es de 18 €, comen 120 clientes, y por cada euro que se sube (o se baja) el precio, hay 4 clientes menos (o más)." + tasks(1, [r"Obtén la función que expresa el beneficio en función de los euros $x$ en que se sube o se baja el precio inicial.", r"¿Cuánto hay que subir o bajar el precio para que el beneficio sea máximo? ¿Cuál sería el precio final y el beneficio?"]),
     tasks(1, [r"$B(x)=(18+x-8)(120-4x)=\res{-4x^2+80x+1200}$.", r"$B'(x)=-8x+80=0\Rightarrow x=10$: hay que \rest{subirlo 10 €}; precio $\res{28}$ € y beneficio $\res{1\,600}$ €."])),
 (2, r"Queremos construir un depósito abierto por arriba, con base cuadrada y un volumen de 4 m³. ¿Qué dimensiones debe tener para que se necesite la mínima cantidad de material?",
     r"$x$: lado de la base, $h$: altura. $x^2h=4\Rightarrow h=\frac{4}{x^2}$. \ $S(x)=x^2+4xh=x^2+\frac{16}{x}$, $S'(x)=2x-\frac{16}{x^2}=0\Rightarrow x=2$, $S''(2)=6>0$: base de $\res{2\times2}$ m y altura $\res{1}$ m ($12$ m² de material)."),
 (3, r"De una cartulina rectangular de 16 cm × 10 cm recortamos un cuadrado de lado $x$ en cada esquina y doblamos para hacer una caja sin tapa. ¿Cuál debe ser $x$ para que el volumen sea máximo? ¿Cuál es ese volumen?",
     r"$V(x)=x(16-2x)(10-2x)=4x^3-52x^2+160x$, $0<x<5$. \ $V'(x)=12x^2-104x+160=4(3x-20)(x-2)=0\Rightarrow x=2$ ($\frac{20}{3}$ no es válido). $V''(2)=-56<0$: $\res{x=2}$ cm y $\res{V=144}$ cm³ (caja de $12\times6\times2$)."),
]))

# ---------- comprovacions numèriques ----------
ln, e, sq = math.log, math.exp, math.sqrt
def nd(f, x, h=1e-6): return (f(x + h) - f(x - h)) / (2 * h)
CHK = [  # (valor de l'esquerra, valor de la dreta)
 (2**3 - 2*4 + 1, 1), (nd(lambda x: x**3 - 2*x*x + 1, 2), 4), (nd(lambda x: (2*x-1)/(x+1), 0), 3), (nd(lambda x: x*ln(x), 1), 1), (nd(lambda x: e(x*x-1), 1), 2),
 (1 - 6 + 8, 3), (27 - 54 + 8, -19), (3 + 9*1, 12), (-19 + 9*3, 8), (nd(lambda x: sq(2*x+1), 4), 1/3), (3 + 12, 15),
 (2*(2/sq(3))**3 - 8*(2/sq(3)), -32*sq(3)/9), (2*-2 + 2 + 8/-2, -6), (1 - 6, -7 + 2), (3 - 12, -7 - 2), (3*2 + 2/2, 7), (nd(lambda x: 3*x + 2/x, 2), 2.5), (5*2 - 2*7 + 4, 0),
 (nd(lambda x: x**3/(x+1)**2, -3), 0), (nd(lambda x: x**3/(x+1)**2, 0.5), 0.25*3.5/1.5**3), (3/9 - 4/3 + 1, 0), (27/9 - 6 + 3, 0), (-0.5*6 + 13, 10), (5*20/10, 10),
 (2 - 9 + 12 - 4, 1), (16 - 36 + 24 - 4, 0), (1 - 2 + 3, 2), (1/e(1), e(-1)), (3 - 4, -1), (-2 - 3 + 12 - 7, 0), (16 - 12 - 24 - 7, -27), (8 - 12, -4), (1 - 6 + 9, 4), (27 - 54 + 27, 0),
 (12 - 2*6, 0), (4*-8 + 12*4 - 2, 14), (3 + 2*-1 - 1, 0), (-8/27 - 8/9 + 8/3 + 1, 67/27), (8 - 8 - 8 + 1, -7), (8 - 12 + 0, -4), (12 - 12 + 0, 0), (1 - 2 + 1, 0),
 (-12 + 24 - 7, 5), (-8 + 24 - 14 + 5, 7), (7 - 5*2, -3),
 (8 - 6, 2), (1 + 6 + 5, 12), (9 - 18 + 5, -4), (16 - 24 + 5, -3), (5 + 4/5, 5.8), (27 - 135 + 189 + 10, 91), (343 - 735 + 441 + 10, 59), (1728 - 2160 + 756 + 10, 334),
 (16 - 108 + 168 + 60, 136), (686 - 1323 + 588 + 60, 11), (1024 - 1728 + 672 + 60, 28), (-8 + 60 - 96 + 50, 6), (-512 + 960 - 384 + 50, 114), (-1000 + 1500 - 480 + 50, 70),
 ((25 - 80 + 100)/10, 4.5), ((4 - 32 + 100)/10, 7.2), ((64 - 128 + 100)/10, 3.6), ((225 - 240 + 100)/10, 8.5), (-3 + 30 + 20, 47), (-75 + 150 + 20, 95), (-192 + 240 + 20, 68),
 (-0.04*900 + 72, 36), (-0.04*1600 + 96, 32), ((1600 - 320)/40, 32), ((2000 - 320)/50, 33.6), ((4 + 8)/2, 6), (-16 + 48 - 26, 6), (-36 + 72 - 26, 10), (-64 + 96 - 26, 6),
 (5*3 + 15, 30), (-25 + 30, 5), (40 - 18 + 9, 31), (-7200 + 7200 + 5, 5), (-1800 + 3600 + 5, 1805), (-72 + 144 - 36, 36), (-12100 + 33000 - 16100, 4800), (-22500 + 45000 - 16100, 6400),
 (25/50 + 8 + 8, 16.5), (400/50 + 8 + 2, 18), (100/50 + 8 + 4, 14), (-2 + 5 - 2, 1), (14/14, 1), ((48 - 6)/28, 1.5), (9/4 - 18/16 - 1, 0.125), (9 - 18 - 1, -10), (0.9 - 0.18 - 1, -0.28),
 (44/16 + 2, 4.75), (44/12 + 2, 17/3), (-4 + 12 + 3, 2 + 9), (-9 + 18 + 3, 3 + 9),
 (nd(lambda x: x*x*(10-x)**2, 5), 0), (20*10 - 100, 100), (2*40 + 3200/40, 160), (2*40*500 + 80*400, 72000), (1*2*2, 4), (2/3 + 3/9, 1),
 (-162 + 324 - 98, 64), (-450 + 900 - 100, 350), (15*(50 - 15/4) - 225/4 - 525 - 25, 87.5), (-1000 + 2430 - 225, 1205), (-729 + 2187 - 225, 1233), (518 - 81, 437),
 (20*80, 1600), (-400 + 800 + 1200, 1600), (4 + 16/2, 12), (2*12*6, 144), (nd(lambda x: x*(16-2*x)*(10-2*x), 2), 0),
]
for l, r in CHK: assert abs(l - r) < 1e-6 * (1 + abs(r)), (l, r)


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

TIT = "Aplicaciones de la derivada"
KW = "aplicaciones de la derivada, recta tangente, recta normal, monotonía, crecimiento, decrecimiento, máximos, mínimos, extremos absolutos, optimización, PAU"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 6: %s' % (t, TIT), capcalera='%s · Unidad 6: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 6' if sol else 'Ficha de ejercicios · Unidad 6') + '}{' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con la herramienta de estudio de la monotonía y los extremos de los apuntes interactivos de la unidad."
             if sol else r"Los ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas. Resuélvelos en el cuaderno mostrando todos los pasos: en los problemas de optimización, justifica siempre que el resultado es un máximo o un mínimo y responde a la pregunta con las unidades.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con la herramienta de estudio de la monotonía y los extremos de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't6-fitxa-solucions-es.tex' if sol else 't6-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'ejercicios,', npau, 'enunciados de la PAU de otras comunidades')
