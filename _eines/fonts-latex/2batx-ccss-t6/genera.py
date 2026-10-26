# Genera t6-fitxa-exercicis.tex i t6-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 6: Aplicacions de la derivada)
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
S.append(("Recta tangent i recta normal", [
 (1, r"Calcula l'equació de la recta tangent i de la recta normal a la gràfica de cada funció en el punt indicat:" + tasks(2, [fx(r'x^3-2x^2+1') + r' en $x=2$', fx(r'\dfrac{2x-1}{x+1}') + r' en $x=0$', fx(r'x\ln x') + r' en $x=1$', fx(r'e^{x^2-1}') + r' en $x=1$'])
     + recorda(r"Tangent: $y-f(a)=f'(a)\,(x-a)$. \ Normal: $y-f(a)=-\dfrac{1}{f'(a)}\,(x-a)$ (si $f'(a)=0$, la normal és la recta vertical $x=a$)."),
     tasks(1, [r"$f(2)=1$, $f'(x)=3x^2-4x$, $f'(2)=4$: \ tangent $\res{y=4x-7}$; \ normal $y-1=-\frac14(x-2)\Rightarrow\res{y=-\frac14x+\frac32}$",
               r"$f(0)=-1$, $f'(x)=\frac{3}{(x+1)^2}$, $f'(0)=3$: \ tangent $\res{y=3x-1}$; \ normal $\res{y=-\frac13x-1}$",
               r"$f(1)=0$, $f'(x)=\ln x+1$, $f'(1)=1$: \ tangent $\res{y=x-1}$; \ normal $\res{y=-x+1}$",
               r"$f(1)=1$, $f'(x)=2x\,e^{x^2-1}$, $f'(1)=2$: \ tangent $\res{y=2x-1}$; \ normal $\res{y=-\frac12x+\frac32}$"])),
 (2, r"Troba els punts de la gràfica de $f(x)=x^3-6x^2+8$ en què la recta tangent és paral·lela a la recta $y=-9x+4$ i escriu l'equació d'aquestes tangents."
     + recorda(r"Rectes paral·leles tenen el mateix pendent: resolem $f'(x)=m$."),
     r"$f'(x)=3x^2-12x=-9\Rightarrow x^2-4x+3=0\Rightarrow x=1,\ x=3$. \ $f(1)=3$: $\res{y=-9x+12}$; \ $f(3)=-19$: $\res{y=-9x+8}$."),
 (2, r"Calcula el punt de la gràfica de $f(x)=\sqrt{2x+1}$ en què la recta normal és paral·lela a la recta $y=-3x$. Escriu l'equació d'aquesta recta normal.",
     r"$-\frac{1}{f'(a)}=-3\Rightarrow f'(a)=\frac13$. \ $f'(x)=\frac{1}{\sqrt{2x+1}}=\frac13\Rightarrow2x+1=9\Rightarrow x=4$, punt $\res{(4,3)}$. \ Normal: $y-3=-3(x-4)\Rightarrow\res{y=-3x+15}$."),
 (1, r"\pau{Madrid, EvAU juliol 2019} Es considera la funció $f(x)=2x^3-8x$. Determina en quins punts la tangent a la corba $y=f(x)$ és horitzontal.",
     r"$f'(x)=6x^2-8=0\Rightarrow x=\pm\frac{2}{\sqrt3}=\pm\frac{2\sqrt3}{3}$. \ Punts $\res{\left(\frac{2\sqrt3}{3},-\frac{32\sqrt3}{9}\right)}$ i $\res{\left(-\frac{2\sqrt3}{3},\frac{32\sqrt3}{9}\right)}$."),
 (2, r"\pau{Catalunya, PAU juny 2019} La gràfica de la funció $f(x)=ax+b+\dfrac8x$ passa pel punt $(-2,-6)$ i la recta tangent en aquest punt és paral·lela a l'eix d'abscisses. Calcula els valors de $a$ i de $b$.",
     r"Tangent horitzontal: $f'(x)=a-\frac{8}{x^2}\Rightarrow f'(-2)=a-2=0\Rightarrow\res{a=2}$. \ $f(-2)=-4+b-4=-6\Rightarrow\res{b=2}$."),
 (2, r"\pau{Andalusia, PEvAU juny 2018} Considera la funció" + dm(pw((r'x^3+ax^2', 'x<1'), (r'bx+\dfrac2x', r'x\geq1'))) + tasks(1, [r"Calcula els valors de $a$ i $b$ perquè la funció siga contínua i derivable en $x=1$.", r"Per a $b=3$, determina l'equació de la recta tangent a la gràfica de la funció en el punt d'abscissa $x=2$."]),
     tasks(1, [r"Continuïtat: $1+a=b+2$. \ Derivabilitat: $3+2a=b-2$. \ $\res{a=-6,\ b=-7}$.",
               r"En $x=2$ fem servir $f(x)=3x+\frac2x$: $f(2)=7$, $f'(x)=3-\frac{2}{x^2}$, $f'(2)=\frac52$: \ $y-7=\frac52(x-2)\Rightarrow\res{5x-2y+4=0}$."])),
 (1, r"\pau{Múrcia, EBAU setembre 2019} Donada la funció $f(x)=2e^{x+1}$, troba l'equació de la recta tangent a la funció en el punt $x=1$.",
     r"$f(1)=2e^2$, $f'(x)=2e^{x+1}$, $f'(1)=2e^2$: \ $y-2e^2=2e^2(x-1)\Rightarrow\res{y=2e^2x}$."),
]))

S.append(("Monotonia d'una funció", [
 (1, r"Estudia la monotonia (intervals de creixement i de decreixement) de les funcions polinòmiques següents:" + tasks(2, [fx(r'x^3-3x^2-9x+5'), fx(r'x^4-8x^2'), fx(r'-x^3+3x+1'), fx(r'x^3+3x')])
     + recorda(r"1) Domini. 2) Calculem $f'(x)$ i la factoritzem. 3) Resolem $f'(x)=0$ i hi afegim els punts fora del domini. 4) Mirem el signe de $f'$ en cada interval amb un valor de prova: $f'>0\Rightarrow$ creixent, $f'<0\Rightarrow$ decreixent."),
     tasks(1, [r"$f'(x)=3(x+1)(x-3)$: creixent en $\res{(-\infty,-1)\cup(3,+\infty)}$, decreixent en $\res{(-1,3)}$.",
               r"$f'(x)=4x(x+2)(x-2)$: decreixent en $\res{(-\infty,-2)\cup(0,2)}$, creixent en $\res{(-2,0)\cup(2,+\infty)}$.",
               r"$f'(x)=-3(x+1)(x-1)$: decreixent en $\res{(-\infty,-1)\cup(1,+\infty)}$, creixent en $\res{(-1,1)}$.",
               r"$f'(x)=3x^2+3>0$ sempre: \rest{creixent en tot $\mathbb R$}."])),
 (2, r"Estudia la monotonia de les funcions racionals següents (compte amb els punts que no són del domini):" + tasks(2, [fx(r'\dfrac{x}{x-2}'), fx(r'\dfrac{x^2+1}{x}'), fx(r'\dfrac{1}{x^2+1}'), fx(r'\dfrac{x^2}{x^2-1}')]),
     tasks(1, [r"$f'(x)=\frac{-2}{(x-2)^2}<0$: decreixent en $\res{(-\infty,2)}$ i en $\res{(2,+\infty)}$.",
               r"$f'(x)=\frac{x^2-1}{x^2}$: creixent en $\res{(-\infty,-1)\cup(1,+\infty)}$, decreixent en $\res{(-1,0)\cup(0,1)}$.",
               r"$f'(x)=\frac{-2x}{(x^2+1)^2}$: creixent en $\res{(-\infty,0)}$, decreixent en $\res{(0,+\infty)}$.",
               r"$f'(x)=\frac{-2x}{(x^2-1)^2}$: creixent en $\res{(-\infty,-1)\cup(-1,0)}$, decreixent en $\res{(0,1)\cup(1,+\infty)}$."])),
 (2, r"Estudia la monotonia de les funcions exponencials i logarítmiques següents:" + tasks(2, [fx(r'x^2e^x'), fx(r'\dfrac{e^x}{x}'), fx(r'\ln(x^2+4)'), fx(r'x^2-2\ln x')])
     + recorda(r"$e^{g(x)}>0$ sempre i els quadrats del denominador també: no canvien el signe de $f'$."),
     tasks(1, [r"$f'(x)=x(x+2)e^x$: creixent en $\res{(-\infty,-2)\cup(0,+\infty)}$, decreixent en $\res{(-2,0)}$.",
               r"$f'(x)=\frac{e^x(x-1)}{x^2}$: decreixent en $\res{(-\infty,0)\cup(0,1)}$, creixent en $\res{(1,+\infty)}$.",
               r"$f'(x)=\frac{2x}{x^2+4}$: decreixent en $\res{(-\infty,0)}$, creixent en $\res{(0,+\infty)}$.",
               r"Domini $(0,+\infty)$. $f'(x)=2x-\frac2x=\frac{2(x^2-1)}{x}$: decreixent en $\res{(0,1)}$, creixent en $\res{(1,+\infty)}$."])),
 (1, r"Observa la gràfica de la funció $f$ i respon:" + '\n\n\\begin{center}' + G_LECT + '\\end{center}' + tasks(1, [r"En quins intervals és creixent? I decreixent?", r"Quins són els màxims i els mínims relatius?", r"Quin signe tenen $f'(0)$ i $f'(2)$? Quant val $f'(-1)$?"]),
     tasks(1, [r"Creixent en $\res{(-\infty,-1)\cup(1,+\infty)}$ i decreixent en $\res{(-1,1)}$.", r"Màxim relatiu $\res{(-1,2)}$ i mínim relatiu $\res{(1,-2)}$.", r"$\res{f'(0)<0}$ (decreix), $\res{f'(2)>0}$ (creix) i $\res{f'(-1)=0}$ (tangent horitzontal)."])),
 (2, r"\pau{Madrid, EvAU juny 2018} Es considera la funció $f(x)=\dfrac{x^3}{(x+1)^2}$." + tasks(1, [r"Calcula'n el domini.", r"Determina'n els intervals de creixement i de decreixement."]),
     tasks(1, [r"$\res{\mathbb R-\{-1\}}$", r"$f'(x)=\frac{3x^2(x+1)^2-2x^3(x+1)}{(x+1)^4}=\frac{x^2(x+3)}{(x+1)^3}$. Creixent en $\res{(-\infty,-3)\cup(-1,+\infty)}$ i decreixent en $\res{(-3,-1)}$. (En $x=0$, $f'=0$ però no canvia de signe.)"])),
 (2, r"\pau{Balears, PBAU ordinària 2021} Donada la funció $f(x)=ax^3+bx^2+x$, definida per a tot $x\in\mathbb R$:" + tasks(1, [r"Troba $a$ i $b$ sabent que $f(x)$ té un punt crític en $x=1$ i que la seua gràfica passa pel punt $(3,0)$.", r"Estudia el creixement i el decreixement de $f(x)$ per a $a=3$ i $b=3$."]),
     tasks(1, [r"$f'(1)=3a+2b+1=0$ i $f(3)=27a+9b+3=0$: \ $\res{a=\frac19,\ b=-\frac23}$.", r"$f'(x)=9x^2+6x+1=(3x+1)^2\geq0$: \rest{creixent en tot $\mathbb R$} (en $x=-\frac13$ la tangent és horitzontal, però no hi ha extrem)."])),
 (2, r"\pau{Canàries, EBAU juny 2017} Una màquina de revelat passa a paper 13 fotografies per minut, però les seues qualitats es deterioren amb el temps. El nombre de fotografies per minut, en funció dels anys $x$ transcorreguts des de la compra, és" + dm(pw((r'-0{,}5x+13', r'0\leq x\leq6'), (r'\dfrac{5(x+14)}{x+4}', 'x>6'))) + tasks(1, [r"Comprova que el nombre de fotografies per minut decreix amb el pas dels anys.", r"Justifica que a partir dels 6 anys revelarà menys de 10 fotografies per minut i que no en revelarà menys de 5 per molt vella que siga la màquina."]),
     tasks(1, [r"$f'(x)=-0{,}5<0$ si $0<x<6$ i $f'(x)=\frac{5(x+4)-5(x+14)}{(x+4)^2}=\frac{-50}{(x+4)^2}<0$ si $x>6$: \rest{sempre decreix}.", r"$f(6)=10$ i és decreixent: després revela \rest{menys de 10}. $\lim_{x\to+\infty}\frac{5(x+14)}{x+4}=5$ i s'hi acosta per dalt: \rest{mai menys de 5}."])),
]))

S.append(("Màxims i mínims relatius", [
 (1, r"Calcula els màxims i mínims relatius de les funcions següents fent servir la segona derivada:" + tasks(2, [fx(r'2x^3-9x^2+12x-4'), fx(r'x^4-2x^2+3'), fx(r'x+\dfrac1x'), fx(r'x\,e^{-x}')])
     + recorda(r"Candidats: $f'(x)=0$. \ Si $f''(a)<0$, màxim; si $f''(a)>0$, mínim; si $f''(a)=0$, estudiem el canvi de signe de $f'$. Doneu el resultat com a punt $(a,f(a))$."),
     tasks(1, [r"$f'(x)=6(x-1)(x-2)$, $f''(x)=12x-18$: \ màxim $\res{(1,1)}$, mínim $\res{(2,0)}$.",
               r"$f'(x)=4x(x^2-1)$, $f''(x)=12x^2-4$: \ màxim $\res{(0,3)}$, mínims $\res{(-1,2)}$ i $\res{(1,2)}$.",
               r"$f'(x)=1-\frac{1}{x^2}$, $f''(x)=\frac{2}{x^3}$: \ màxim $\res{(-1,-2)}$, mínim $\res{(1,2)}$.",
               r"$f'(x)=e^{-x}(1-x)$, $f''(x)=e^{-x}(x-2)$, $f''(1)=-\frac1e<0$: \ màxim $\res{\left(1,\frac1e\right)}$."])),
 (2, r"Estudia els extrems relatius de $f(x)=3x^4-4x^3$. Què passa en $x=0$?",
     r"$f'(x)=12x^3-12x^2=12x^2(x-1)=0\Rightarrow x=0,\ x=1$. \ $f''(x)=36x^2-24x$: $f''(1)=12>0$, mínim $\res{(1,-1)}$. \ $f''(0)=0$ no decideix: $f'<0$ a l'esquerra i a la dreta de 0 (no canvia de signe), així que en $x=0$ \rest{no hi ha extrem}."),
 (1, r"\pau{La Rioja, EBAU juliol 2017} Sigui $f(x)=2x^3-3x^2-12x-7$." + tasks(1, [r"Estudia els intervals de creixement i de decreixement de la funció.", r"Determina els extrems relatius de la funció."]),
     tasks(1, [r"$f'(x)=6(x+1)(x-2)$: creixent en $\res{(-\infty,-1)\cup(2,+\infty)}$, decreixent en $\res{(-1,2)}$.", r"Màxim relatiu $\res{(-1,0)}$ i mínim relatiu $\res{(2,-27)}$."])),
 (1, r"\pau{Navarra, EvAU ordinària 2020} Sigui la funció $y=x^3-3x^2$. Calcula els intervals de creixement i de decreixement, i els màxims i mínims.",
     r"$y'=3x(x-2)$: creixent en $\res{(-\infty,0)\cup(2,+\infty)}$, decreixent en $\res{(0,2)}$. Màxim $\res{(0,0)}$ i mínim $\res{(2,-4)}$."),
 (1, r"\pau{País Basc, EAU juny 2019} Es considera la corba $f(x)=x^3-6x^2+9x$." + tasks(1, [r"Estudia els intervals de creixement i de decreixement de la funció.", r"Determina els màxims i mínims relatius."]),
     tasks(1, [r"$f'(x)=3(x-1)(x-3)$: creixent en $\res{(-\infty,1)\cup(3,+\infty)}$, decreixent en $\res{(1,3)}$.", r"Màxim relatiu $\res{(1,4)}$ i mínim relatiu $\res{(3,0)}$."])),
 (2, r"\pau{Catalunya, PAU ordinària 2021} Considera la funció $f(x)=4x^3+ax^2-2$." + tasks(1, [r"Determina el valor del paràmetre $a$ perquè la funció tinga un extrem relatiu en el punt d'abscissa $x=-1$.", r"Calcula els intervals de creixement i de decreixement de $f(x)$ quan $a=12$. Indica també els extrems relatius i classifica'ls."]),
     tasks(1, [r"$f'(x)=12x^2+2ax$, $f'(-1)=12-2a=0\Rightarrow\res{a=6}$.", r"$f'(x)=12x(x+2)$: creixent en $\res{(-\infty,-2)\cup(0,+\infty)}$, decreixent en $\res{(-2,0)}$. Màxim $\res{(-2,14)}$ i mínim $\res{(0,-2)}$."])),
 (2, r"\pau{Múrcia, EBAU juliol 2020} Sigui la funció $f(x)=x^3+ax^2+bx+1$." + tasks(1, [r"Determina els valors de $a$ i $b$ perquè la funció tinga un extrem relatiu en $x=1$ i la recta tangent a la gràfica en el punt d'abscissa $x=0$ tinga pendent $m=-1$.", r"Si $a=-2$ i $b=-4$, determina els intervals de creixement i de decreixement i els extrems relatius."]),
     tasks(1, [r"$f'(0)=b=-1$ i $f'(1)=3+2a+b=0$: \ $\res{a=-1,\ b=-1}$.", r"$f'(x)=3x^2-4x-4=(3x+2)(x-2)$: creixent en $\res{\left(-\infty,-\frac23\right)\cup(2,+\infty)}$, decreixent en $\res{\left(-\frac23,2\right)}$. Màxim $\res{\left(-\frac23,\frac{67}{27}\right)}$ i mínim $\res{(2,-7)}$."])),
 (2, r"\pau{País Basc, EAU juliol 2019} Sigui la funció $f(x)=x^3+ax^2+bx+c$. Troba els valors de $a$, $b$ i $c$ perquè la funció passe pel punt $(0,0)$ i tinga un extrem relatiu en el punt $(2,-4)$. Determina'n després els màxims i mínims.",
     r"$f(0)=c=0$; \ $f(2)=8+4a+2b=-4$; \ $f'(2)=12+4a+b=0$. \ $\res{a=-3,\ b=0,\ c=0}$. \ $f'(x)=3x(x-2)$: màxim $\res{(0,0)}$ i mínim $\res{(2,-4)}$."),
 (2, r"\pau{La Rioja, EBAU ordinària 2020} Considerem la funció $f(x)=x^4-ax^2+b$." + tasks(1, [r"Quins valors han de prendre $a$ i $b$ perquè la funció tinga un mínim en el punt $(1,0)$?", r"Amb aquests valors, calcula els punts en què $f(x)$ té tangent paral·lela a la recta $y=1$.", r"Calcula la recta tangent a la funció en el punt $x=1$."]),
     tasks(1, [r"$f'(1)=4-2a=0\Rightarrow a=2$; \ $f(1)=1-2+b=0\Rightarrow b=1$: \ $\res{a=2,\ b=1}$.", r"Pendent 0: $f'(x)=4x^3-4x=0\Rightarrow x=0,\pm1$: punts $\res{(0,1)}$, $\res{(-1,0)}$ i $\res{(1,0)}$.", r"$f(1)=0$ i $f'(1)=0$: $\res{y=0}$."])),
 (3, r"\pau{Múrcia, EBAU setembre 2019} Determina el punt de la gràfica de la funció $f(x)=-x^3+6x^2-7x+5$ en què el pendent de la recta tangent és màxim. Quina és l'equació de la recta tangent en aquest punt?",
     r"El pendent és $m(x)=f'(x)=-3x^2+12x-7$. $m'(x)=-6x+12=0\Rightarrow x=2$ i $m''=-6<0$: màxim. \ $f(2)=7$, $f'(2)=5$: punt $\res{(2,7)}$ i tangent $\res{y=5x-3}$."),
]))

S.append(("Extrems absoluts en un interval tancat", [
 (1, r"Calcula el màxim i el mínim absoluts de cada funció en l'interval indicat:" + tasks(1, [fx(r'x^3-3x') + r' en $[0,2]$', fx(r'x^2-6x+5') + r' en $[-1,4]$', fx(r'x+\dfrac4x') + r' en $[1,5]$'])
     + recorda(r"Comparem el valor de $f$ en els punts crítics de dins de l'interval i en els extrems de l'interval."),
     tasks(1, [r"$f'(x)=3(x^2-1)\Rightarrow x=1$. \ $f(0)=0$, $f(1)=-2$, $f(2)=2$: màxim $\res{2}$ en $x=2$ i mínim $\res{-2}$ en $x=1$.",
               r"$f'(x)=2x-6\Rightarrow x=3$. \ $f(-1)=12$, $f(3)=-4$, $f(4)=-3$: màxim $\res{12}$ en $x=-1$ i mínim $\res{-4}$ en $x=3$.",
               r"$f'(x)=1-\frac{4}{x^2}\Rightarrow x=2$ ($-2$ no és de l'interval). \ $f(1)=5$, $f(2)=4$, $f(5)=5{,}8$: màxim $\res{5{,}8}$ en $x=5$ i mínim $\res{4}$ en $x=2$."])),
 (2, r"\pau{Andalusia, PEvAU setembre 2018} El consum de cereals en una ciutat, en milers de tones, ve donat per la funció $c(t)=t^3-15t^2+63t+10$, per a $0\leq t\leq12$, on $t$ representa el temps." + tasks(1, [r"En quin instant s'assoleix el màxim consum de cereals i quantes tones es consumeixen en aquest moment?", r"En quin interval de temps decreix el consum de cereals?"]),
     tasks(1, [r"$c'(t)=3(t-3)(t-7)$. \ $c(0)=10$, $c(3)=91$, $c(7)=59$, $c(12)=334$: el màxim és en $\res{t=12}$, amb $\res{334\,000}$ tones.", r"Decreix en $\res{(3,7)}$."])),
 (2, r"\pau{Extremadura, EBAU ordinària 2020} La despesa $G$ (en euros) pel consum d'energia elèctrica en un taller durant les 8 hores de funcionament varia d'acord amb la funció $G(t)=2t^3-27t^2+84t+60$, $0\leq t\leq8$, on $t$ és el temps transcorregut en hores. Determina a quines hores es produeixen les despeses màxima i mínima i els valors d'aquestes despeses.",
     r"$G'(t)=6(t-2)(t-7)$. \ $G(0)=60$, $G(2)=136$, $G(7)=11$, $G(8)=28$. \ Despesa màxima a les $\res{2\text{ h}}$ ($\res{136}$ €) i mínima a les $\res{7\text{ h}}$ ($\res{11}$ €)."),
 (2, r"\pau{Extremadura, EBAU juliol 2019} La potència requerida per la maquinària elèctrica d'una empresa durant les 10 hores de funcionament ve donada per $P(t)=-t^3+15t^2-48t+50$, $0\leq t\leq10$, on $t$ és el temps en hores i $P(t)$ la potència en quilowatts. Determina a quines hores es produeixen el màxim i el mínim d'aquesta potència i calcula'n els valors.",
     r"$P'(t)=-3(t-2)(t-8)$. \ $P(0)=50$, $P(2)=6$, $P(8)=114$, $P(10)=70$. \ Mínim a les $\res{2\text{ h}}$ ($\res{6}$ kW) i màxim a les $\res{8\text{ h}}$ ($\res{114}$ kW)."),
 (2, r"\pau{Aragó, EvAU ordinària 2020} El cost unitari de fabricació d'un producte (en euros) depèn del volum de producció segons la fórmula $C(x)=\dfrac{1}{10}\left(x^2-16x+100\right)$, on $x\in[2,15]$ és el volum de producció (en milers d'unitats)." + tasks(1, [r"Si es produeixen 5\,000 unitats, quant val el cost unitari?", r"Per a quin volum de producció s'assoleix el cost unitari mínim? I el màxim? Quant valen aquests costos?"]),
     tasks(1, [r"$C(5)=\res{4{,}5}$ €.", r"$C'(x)=\frac{2x-16}{10}=0\Rightarrow x=8$. \ $C(2)=7{,}2$, $C(8)=3{,}6$, $C(15)=8{,}5$: mínim amb $\res{8\,000}$ unitats ($\res{3{,}6}$ €) i màxim amb $\res{15\,000}$ unitats ($\res{8{,}5}$ €)."])),
 (2, r"\pau{Navarra, EvAU juny 2019} El benefici d'una empresa, en milers d'euros, ve donat per $f(x)=-3x^2+30x+20$, amb $0\leq x\leq8$, on $x$ és la despesa en publicitat, en milers d'euros." + tasks(1, [r"Quin és el benefici si l'empresa no gasta en publicitat? I si en gasta 1\,000 euros?", r"Determina la despesa en publicitat que produeix el benefici màxim. Quin és aquest benefici?", r"Explica com augmenta o disminueix el benefici en funció de la despesa en publicitat.", r"Quant gasta l'empresa en publicitat quan el benefici és mínim? A quant ascendeix?"]),
     tasks(1, [r"$f(0)=\res{20\,000}$ €; \ $f(1)=\res{47\,000}$ €.", r"$f'(x)=-6x+30=0\Rightarrow x=5$, $f''=-6<0$: gastant $\res{5\,000}$ € el benefici és màxim, $\res{95\,000}$ €.", r"Creix en $\res{(0,5)}$ i decreix en $\res{(5,8)}$.", r"$f(0)=20$, $f(8)=68$: el mínim és sense gastar en publicitat ($\res{x=0}$), $\res{20\,000}$ €."])),
 (3, r"\pau{Andalusia, PEvAU setembre 2018} El benefici, en milers d'euros, que ha obtingut una almàssera al llarg de 50 anys ve donat per la funció contínua" + dm(pw((r"-0{,}04t^2+2{,}4t", r'0\leq t\leq40'), (r"\dfrac{40t-320}{t}", r'40<t\leq50'), name='B(t)')) + r"on $t$ és el temps transcorregut. Estudia la monotonia de $B(t)$ i determina en quin moment van ser més grans els beneficis de l'almàssera, així com el benefici màxim.",
     r"$B'(t)=-0{,}08t+2{,}4$ si $0<t<40$ (zero en $t=30$) i $B'(t)=\frac{320}{t^2}>0$ si $40<t<50$. Creix en $\res{(0,30)\cup(40,50)}$ i decreix en $\res{(30,40)}$. \ $B(0)=0$, $B(30)=36$, $B(40)=32$, $B(50)=33{,}6$: màxim en l'any $\res{t=30}$, amb $\res{36\,000}$ €."),
 (2, r"\pau{Canàries, EBAU juliol 2019} El benefici d'un parc aquàtic, en milions d'euros, al llarg de l'últim any dividit en mesos és" + dm(pw((r'\dfrac{x+8}{2}', r'0\leq x\leq4'), (r'-x^2+12x-26', r'4<x\leq8'), (r'6', r'8<x\leq12'))) + tasks(1, [r"Quan ha crescut i quan ha decrescut el benefici?", r"En quins moments es van obtenir els beneficis màxim i mínim i a quant ascendien?"]),
     tasks(1, [r"$f'(x)=\frac12>0$ en $(0,4)$ i $f'(x)=-2x+12$ en $(4,8)$: creix en $\res{(0,6)}$, decreix en $\res{(6,8)}$ i és constant en $(8,12)$.", r"$f(0)=4$, $f(6)=10$: màxim en el mes $\res{6}$ ($\res{10}$ milions d'€) i mínim en el mes $\res{0}$ ($\res{4}$ milions d'€)."])),
 (2, r"\pau{Balears, PBAU juliol 2018} Els beneficis (en milers d'euros) per la venda d'un producte en funció de la inversió en promoció $x$ (en milers d'euros) venen donats per la funció contínua" + dm(pw((r'5x+15', r'0\leq x\leq3'), (r'-(x-3)^2+30', r'3<x\leq8'), name='B(x)')) + tasks(1, [r"Determina'n els intervals de creixement i de decreixement.", r"Determina'n el benefici màxim i el mínim."]),
     tasks(1, [r"$B'(x)=5>0$ en $(0,3)$ i $B'(x)=-2(x-3)<0$ en $(3,8)$: creix en $\res{(0,3)}$ i decreix en $\res{(3,8)}$.", r"$B(0)=15$, $B(3)=30$, $B(8)=5$: màxim en $x=3$ ($\res{30\,000}$ €) i mínim en $x=8$ ($\res{5\,000}$ €)."])),
]))

S.append(("Problemes d'optimització: coneixem la funció", [
 (1, r"\pau{Andalusia, PEvAU juny 2018} La funció de costos d'una empresa és $f(x)=40-6x+x^2$, per a $x\geq0$, on $x$ representa la quantitat produïda d'un article. Disminueix el cost alguna vegada? Determina la quantitat produïda quan el cost és mínim i quin és aquest cost."
     + recorda(r"Derivem, igualem a zero, justifiquem si és màxim o mínim (segona derivada o monotonia) i responem la pregunta amb les unitats."),
     r"$f'(x)=2x-6$: el cost disminueix per a $\res{0<x<3}$. \ $f''=2>0$: el cost és mínim amb $\res{x=3}$ articles, i val $\res{f(3)=31}$."),
 (1, r"\pau{Castella i Lleó, EBAU juliol 2019} La capacitat d'atenció d'un alumne en una classe de 60 minuts ve donada per $f(t)=-2t^2+120t+5$, amb $t\in[0,60]$." + tasks(1, [r"Calcula la capacitat d'atenció quan porta una hora de classe.", r"En quin instant la capacitat d'atenció és màxima? Quina és aquesta capacitat màxima?"]),
     tasks(1, [r"$f(60)=\res{5}$.", r"$f'(t)=-4t+120=0\Rightarrow t=30$, $f''=-4<0$: als $\res{30}$ minuts, amb una atenció de $\res{1\,805}$."])),
 (1, r"\pau{Múrcia, EBAU juliol 2020} El benefici setmanal d'una empresa d'ordinadors ve donat per $B(x)=-2x^2+24x-36$, on $x$ és el nombre d'ordinadors venuts cada setmana. Calcula el nombre d'ordinadors que cal vendre cada setmana perquè el benefici siga màxim. Quin és aquest benefici?",
     r"$B'(x)=-4x+24=0\Rightarrow x=6$, $B''=-4<0$: venent $\res{6}$ ordinadors, benefici màxim $\res{36}$."),
 (1, r"\pau{Balears, PBAU ordinària 2021} El benefici, en euros, que obté una empresa per la venda de $x$ unitats d'un producte és $B(x)=-x^2+300x-16\,100$, per a $x\geq0$." + tasks(1, [r"Calcula el benefici si se'n venen 110 unitats.", r"Quantes unitats ha de vendre perquè el benefici siga màxim? Quin és aquest benefici?"]),
     tasks(1, [r"$B(110)=\res{4\,800}$ €.", r"$B'(x)=-2x+300=0\Rightarrow x=150$, $B''<0$: $\res{150}$ unitats i $\res{6\,400}$ €."])),
 (2, r"\pau{Balears, PBAU ordinària 2020} En una empresa es poden produir fins a 500 taules al mes. El cost de produir-ne $q$ és $C(q)=\dfrac{q^3}{50}+8q+40$, i el cost mitjà de cada taula és $Q(q)=\dfrac{C(q)}{q}$." + tasks(1, [r"Calcula el cost mitjà de cada taula si l'empresa en produeix 5. I si en produeix 20?", r"Determina quantes taules cal produir perquè el cost mitjà siga mínim. Justifica que es tracta d'un mínim i calcula aquest cost mitjà."]),
     tasks(1, [r"$Q(q)=\frac{q^2}{50}+8+\frac{40}{q}$: \ $Q(5)=\res{16{,}5}$ €, \ $Q(20)=\res{18}$ €.", r"$Q'(q)=\frac{q}{25}-\frac{40}{q^2}=0\Rightarrow q^3=1000\Rightarrow q=10$; \ $Q''(q)=\frac{1}{25}+\frac{80}{q^3}>0$: mínim amb $\res{10}$ taules, cost mitjà $\res{14}$ €."])),
 (2, r"\pau{Catalunya, PAU ordinària 2021} Una fàbrica estima que el benefici mensual, en milers d'euros, per cada tona de confeti venuda és $f(x)=\dfrac{-0{,}2x^2+5x-20}{x}$, on $x$ és el nombre de tones venudes." + tasks(1, [r"Determina en quin interval de valors ha d'estar $x$ perquè la fàbrica no tinga pèrdues.", r"Calcula la quantitat de tones que proporciona el benefici màxim i quin és aquest benefici."]),
     tasks(1, [r"$-0{,}2x^2+5x-20\geq0\Leftrightarrow x^2-25x+100\leq0$: entre $\res{5}$ i $\res{20}$ tones.", r"$f(x)=-0{,}2x+5-\frac{20}{x}$, $f'(x)=-0{,}2+\frac{20}{x^2}=0\Rightarrow x=10$, $f''(10)<0$: $\res{10}$ tones, $\res{f(10)=1}$ (1\,000 €)."])),
 (2, r"\pau{Aragó, EvAU ordinària 2021} Uns emprenedors estimen que els beneficis, en centenars de milers d'euros, vindran donats per $B(t)=\dfrac{2t-6}{t+4}$, on $t$ són els anys transcorreguts des de l'obertura." + tasks(1, [r"En quin interval l'empresa tindrà pèrdues?", r"En quin moment $t\in[3,10]$ s'assoleix el benefici màxim i a quants euros ascendeix? Justifica-ho.", r"Quant de temps ha de passar per obtindre un benefici de 150\,000 €?"]),
     tasks(1, [r"$B(t)<0\Leftrightarrow 2t-6<0$: durant els $\res{3}$ primers anys.", r"$B'(t)=\frac{14}{(t+4)^2}>0$: és creixent, així que el màxim és en $\res{t=10}$, amb $B(10)=1$, és a dir, $\res{100\,000}$ €.", r"$\frac{2t-6}{t+4}=1{,}5\Rightarrow t=\res{24}$ anys."])),
 (2, r"\pau{Aragó, EvAU juny 2018} Una empresa ha de decidir el preu de venda $x$ d'un joguet, entre 1 i 10 euros. El benefici, en milions d'euros, serà $B(x)=\dfrac9x-\dfrac{18}{x^2}-1$." + tasks(1, [r"Per a quins valors de $x\in[1,10]$ el benefici és positiu?", r"Quin preu de venda maximitza el benefici? Quin és el benefici màxim?"]),
     tasks(1, [r"$B(x)>0\Leftrightarrow x^2-9x+18<0$: $\res{x\in(3,6)}$.", r"$B'(x)=-\frac{9}{x^2}+\frac{36}{x^3}=0\Rightarrow x=4$. \ $B(1)=-10$, $B(4)=0{,}125$, $B(10)=-0{,}28$: preu de $\res{4}$ €, benefici de $\res{125\,000}$ €."])),
 (2, r"\pau{Galícia, ABAU juliol 2019} El preu de venda d'un electrodomèstic (en centenars d'euros) ve donat per $P(t)=\dfrac{44}{t^2-4t+16}+2$, on $t$ és el temps en anys des que es va posar a la venda." + tasks(1, [r"Calcula el preu de llançament. En quin moment el preu torna a ser el de llançament?", r"Determina els períodes en què el preu ha augmentat i ha disminuït. Quin ha sigut el preu màxim i quan s'ha produït?", r"Estudia la tendència del preu amb el pas del temps."]),
     tasks(1, [r"$P(0)=4{,}75$: $\res{475}$ €. \ $P(t)=4{,}75\Leftrightarrow t^2-4t=0$: als $\res{4}$ anys.", r"$P'(t)=\frac{-44(2t-4)}{(t^2-4t+16)^2}$: augmenta en $\res{(0,2)}$ i disminueix a partir de $\res{t=2}$. Màxim als 2 anys: $P(2)=\frac{17}{3}$, uns $\res{566{,}67}$ €.", r"$\lim_{t\to+\infty}P(t)=2$: tendeix a $\res{200}$ €."])),
 (2, r"\pau{Astúries, EBAU juliol 2019} Dues fonts d'energia A i B produeixen electricitat alhora durant 6 hores. En un instant $x\in[0,6]$, la font A produeix $f(x)=-x^2+6x+3$ i la font B, $g(x)=x+9$." + tasks(1, [r"En quins moments produeixen totes dues la mateixa quantitat d'electricitat? Quina és aquesta producció?", r"En quins moments decreix la producció de la font A?", r"En quin instant és màxima la producció conjunta de les dues fonts?"]),
     tasks(1, [r"$-x^2+6x+3=x+9\Rightarrow x^2-5x+6=0$: a les $\res{2}$ h (11 unitats) i a les $\res{3}$ h (12 unitats).", r"$f'(x)=-2x+6<0$ si $x>3$: decreix en $\res{(3,6)}$.", r"$h(x)=f(x)+g(x)=-x^2+7x+12$, $h'(x)=-2x+7=0$: a les $\res{3{,}5}$ h."])),
]))

S.append(("Problemes d'optimització: construïm la funció", [
 (1, r"\pau{Castella i Lleó, EBAU setembre 2017} Troba raonadament dos nombres reals positius sabent que la seua suma és 10 i que el producte dels seus quadrats és màxim."
     + recorda(r"1) Variables i equació que les relaciona (aïllem una). 2) Funció a optimitzar d'una sola variable. 3) Derivem i igualem a 0. 4) Comprovem si és màxim o mínim. 5) Calculem l'altra variable i interpretem el resultat."),
     r"$y=10-x$, \ $P(x)=x^2(10-x)^2$. \ $P'(x)=2x(10-x)^2-2x^2(10-x)=2x(10-x)(10-2x)=0\Rightarrow x=5$ (els altres valors fan $P=0$). Els nombres són $\res{5}$ i $\res{5}$."),
 (1, r"\pau{Catalunya, PAU ordinària 2021} Un granger vol construir un corral rectangular per als conills i només disposa de 40 m de tanca. Anomenem $x$ l'amplària del corral i $y$ la llargària." + tasks(1, [r"Escriu la funció que dona l'àrea del corral en funció només de l'amplària $x$.", r"Quines han de ser l'amplària i la llargària perquè l'àrea siga màxima? Quina és aquesta àrea?"]),
     tasks(1, [r"$2x+2y=40\Rightarrow y=20-x$: \ $\res{A(x)=20x-x^2}$.", r"$A'(x)=20-2x=0\Rightarrow x=10$, $A''<0$: un quadrat de $\res{10\times10}$ m, amb $\res{100}$ m²."])),
 (2, r"\pau{La Rioja, EBAU juliol 2017} Volem construir un camp rectangular de 3\,200 m² al llarg d'un riu; no cal tancar el costat de la vora." + tasks(1, [r"Quines dimensions ha de tindre el camp perquè calga el mínim possible de metres de tanca?", r"Determina el cost del tancat si cada metre perpendicular al riu costa 500 € i cada metre paral·lel al riu, 400 €."]),
     tasks(1, [r"$x$: costats perpendiculars, $y$: costat paral·lel. $xy=3200$, $L(x)=2x+\frac{3200}{x}$, $L'(x)=2-\frac{3200}{x^2}=0\Rightarrow x=40$, $L''>0$: $\res{40}$ m perpendicular i $\res{80}$ m paral·lel al riu.", r"$2\cdot40\cdot500+80\cdot400=\res{72\,000}$ €."])),
 (3, r"\pau{La Rioja, EBAU juny 2018} Considerem un rectangle de costats $x$ i $y$." + tasks(1, [r"Troba el rectangle de perímetre mínim si els costats verifiquen la relació $xy^2=4$.", r"Troba el rectangle d'àrea màxima si els costats verifiquen la relació $x+3y^2=1$."]),
     tasks(1, [r"$x=\frac{4}{y^2}$, $P(y)=\frac{8}{y^2}+2y$, $P'(y)=-\frac{16}{y^3}+2=0\Rightarrow y=2$: $\res{x=1,\ y=2}$.", r"$x=1-3y^2$, $A(y)=y-3y^3$, $A'(y)=1-9y^2=0\Rightarrow y=\frac13$: $\res{x=\frac23,\ y=\frac13}$."])),
 (2, r"\pau{Múrcia, EBAU juny 2019} Una empresa ven un article a 40 euros la unitat i té la funció de cost $C(x)=2x^2+4x+98$, on $x$ és el nombre d'unitats produïdes. Calcula el nombre d'unitats que ha de vendre perquè el benefici (ingressos menys costos) siga màxim i aquest benefici màxim.",
     r"$B(x)=40x-(2x^2+4x+98)=-2x^2+36x-98$, $B'(x)=-4x+36=0\Rightarrow x=9$, $B''<0$: $\res{9}$ unitats i $\res{64}$ €."),
 (2, r"\pau{Múrcia, EBAU juny 2018} Una empresa ven un producte a 15 euros la unitat. La funció de costos és $C(x)=2x^2-45x+100$, on $x$ és el nombre d'unitats. Troba el nombre d'unitats que ha de vendre per obtindre el benefici màxim i calcula aquest benefici.",
     r"$B(x)=15x-C(x)=-2x^2+60x-100$, $B'(x)=-4x+60=0\Rightarrow x=15$, $B''<0$: $\res{15}$ unitats i $\res{350}$ u.m."),
 (2, r"\pau{Múrcia, EBAU ordinària 2021} El cost de producció de $x$ unitats d'un producte és $C(x)=\dfrac14x^2+35x+25$ i el preu de venda és $p=50-\dfrac x4$ euros. Troba:" + tasks(1, [r"El nombre d'unitats que cal vendre diàriament perquè el benefici siga màxim.", r"El preu al qual s'han de vendre aquestes unitats.", r"El benefici màxim."]),
     tasks(1, [r"$B(x)=x\left(50-\frac x4\right)-\frac{x^2}{4}-35x-25=-\frac{x^2}{2}+15x-25$, $B'(x)=-x+15=0$: $\res{15}$ unitats.", r"$p=50-\frac{15}{4}=\res{46{,}25}$ €.", r"$B(15)=\res{87{,}5}$ €."])),
 (2, r"\pau{Galícia, ABAU extraordinària 2021} Una empresa pot vendre $x$ unitats al mes d'un producte al preu de $518-x^2$ euros la unitat. Té unes despeses mensuals fixes de 225 € i unes altres de $275x$ euros." + tasks(1, [r"Determina les funcions $I(x)$ i $B(x)$ dels ingressos i dels beneficis. Quin benefici s'obté si se'n venen 10 unitats?", r"Calcula el nombre d'unitats que s'han de produir per obtindre el benefici màxim. A quant ascendiria? Quin seria el preu d'una unitat?"]),
     tasks(1, [r"$\res{I(x)=518x-x^3}$, \ $\res{B(x)=-x^3+243x-225}$; \ $B(10)=\res{1\,205}$ €.", r"$B'(x)=-3x^2+243=0\Rightarrow x=9$, $B''(9)=-54<0$: $\res{9}$ unitats, benefici $\res{1\,233}$ €, preu $\res{437}$ €."])),
 (3, r"\pau{Catalunya, PAU ordinària 2020} Elaborar un menú en un restaurant costa 8 €. Si el preu del menú és de 18 €, hi dinen 120 clients, i per cada euro que s'apuja (o s'abaixa) el preu, hi ha 4 clients menys (o més)." + tasks(1, [r"Obtín la funció que expressa el benefici en funció dels euros $x$ en què s'apuja o s'abaixa el preu inicial.", r"Quant cal apujar o abaixar el preu perquè el benefici siga màxim? Quin seria el preu final i el benefici?"]),
     tasks(1, [r"$B(x)=(18+x-8)(120-4x)=\res{-4x^2+80x+1200}$.", r"$B'(x)=-8x+80=0\Rightarrow x=10$: cal \rest{apujar-lo 10 €}; preu $\res{28}$ € i benefici $\res{1\,600}$ €."])),
 (2, r"Volem construir un dipòsit obert per dalt, amb base quadrada i un volum de 4 m³. Quines dimensions ha de tindre perquè calga la mínima quantitat de material?",
     r"$x$: costat de la base, $h$: altura. $x^2h=4\Rightarrow h=\frac{4}{x^2}$. \ $S(x)=x^2+4xh=x^2+\frac{16}{x}$, $S'(x)=2x-\frac{16}{x^2}=0\Rightarrow x=2$, $S''(2)=6>0$: base de $\res{2\times2}$ m i altura $\res{1}$ m ($12$ m² de material)."),
 (3, r"D'una cartolina rectangular de 16 cm × 10 cm retallem un quadrat de costat $x$ en cada cantó i dobleguem per fer una caixa sense tapa. Quin ha de ser $x$ perquè el volum siga màxim? Quin és aquest volum?",
     r"$V(x)=x(16-2x)(10-2x)=4x^3-52x^2+160x$, $0<x<5$. \ $V'(x)=12x^2-104x+160=4(3x-20)(x-2)=0\Rightarrow x=2$ ($\frac{20}{3}$ no és vàlid). $V''(2)=-56<0$: $\res{x=2}$ cm i $\res{V=144}$ cm³ (caixa de $12\times6\times2$)."),
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
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={aplicacions de la derivada, recta tangent, recta normal, monotonia, creixement, decreixement, màxims, mínims, extrems absoluts, optimització, PAU}"
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

TIT = "Aplicacions de la derivada"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 6: %s. 2n de Batxillerat CCSS}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 6: %s · 2n Batxillerat CCSS" % (t, TIT))
    assert 'Unitat 6' in p and 'unitat 6' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 6' if sol else "Fitxa d'exercicis · Unitat 6") + r'''}{''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb l'eina d'estudi de la monotonia i els extrems dels apunts interactius de la unitat."
             if sol else r"Els exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes (traduïts al valencià). Resol-los al quadern mostrant tots els passos: en els problemes d'optimització, justifica sempre que el resultat és un màxim o un mínim i respon la pregunta amb les unitats.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb l\'eina d\'estudi de la monotonia i els extrems dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't6-fitxa-solucions.tex' if sol else 't6-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
npau = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
print(n, 'exercicis,', npau, 'enunciats de la PAU d\'altres comunitats')
