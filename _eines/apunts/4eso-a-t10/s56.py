# Apartats 10.5 i 10.6 dels apunts de la Unitat 10 de 4t ESO Matemàtiques A (Estadística bidimensional): recta de regressió
# (a ull i amb la fórmula) i estimacions (interpolació, extrapolació i fiabilitat).
from comu import *
from s12 import HX, HY, SH, T2X, T2Y, S2T
from s4 import EX, EY, SE, PX, PY, SP, QX, QY, SQ, DX, DY, SD

AXH = (L('hores', 'horas', 'hours'), L('nota', 'nota', 'mark'))
mE, nE = rl(SE); assert (mE, nE) == (Fr(9, 10), Fr(13, 10))
mP, nP = rl(SP); assert (mP, nP) == (Fr(-32, 5), Fr(286, 5))

# =====================================================================
# 10.5 Recta de regressió
# =====================================================================
s5 = box('def', L('La recta de regressió', 'La recta de regresión', 'The regression line'),
  P(r"Quan la correlació és forta, els punts del núvol s'agrupen al voltant d'una recta. La recta que <strong>millor s'ajusta</strong> al núvol s'anomena <strong>recta de regressió</strong> (de \(Y\) sobre \(X\)). Ens serveix per a <strong>resumir</strong> la relació entre les variables i per a fer <strong>estimacions</strong>.",
    r"Cuando la correlación es fuerte, los puntos de la nube se agrupan alrededor de una recta. La recta que <strong>mejor se ajusta</strong> a la nube se llama <strong>recta de regresión</strong> (de \(Y\) sobre \(X\)). Nos sirve para <strong>resumir</strong> la relación entre las variables y para hacer <strong>estimaciones</strong>.",
    r"When the correlation is strong, the points of the cloud cluster around a straight line. The line that <strong>fits</strong> the cloud <strong>best</strong> is called the <strong>regression line</strong> (of \(Y\) on \(X\)). We use it to <strong>summarise</strong> the relationship between the variables and to make <strong>estimates</strong>.")
  + ul(L(r"<strong>A ull</strong>: traça una recta que passe pel <strong>centre de gravetat</strong> \((\bar x,\,\bar y)\), que seguisca la direcció del núvol i que deixe més o menys els mateixos punts per damunt que per davall. Cada persona obtindrà una recta un poc diferent.",
         r"<strong>A ojo</strong>: traza una recta que pase por el <strong>centro de gravedad</strong> \((\bar x,\,\bar y)\), que siga la dirección de la nube y que deje más o menos los mismos puntos por encima que por debajo. Cada persona obtendrá una recta un poco diferente.",
         r"<strong>By eye</strong>: draw a line through the <strong>centre of gravity</strong> \((\bar x,\,\bar y)\) that follows the direction of the cloud and leaves roughly as many points above it as below. Everyone will get a slightly different line."),
       L(r"<strong>Amb la fórmula</strong>: la recta de regressió exacta és la que fa <strong>més xicoteta la suma dels quadrats dels errors</strong> (les distàncies verticals de cada punt a la recta). Passa per \((\bar x,\,\bar y)\) i té pendent \(m=\dfrac{\sigma_{xy}}{\sigma_x^2}\):",
         r"<strong>Con la fórmula</strong>: la recta de regresión exacta es la que hace <strong>más pequeña la suma de los cuadrados de los errores</strong> (las distancias verticales de cada punto a la recta). Pasa por \((\bar x,\,\bar y)\) y tiene pendiente \(m=\dfrac{\sigma_{xy}}{\sigma_x^2}\):",
         r"<strong>With the formula</strong>: the exact regression line is the one that makes the <strong>sum of the squared errors</strong> (the vertical distances from each point to the line) <strong>as small as possible</strong>. It passes through \((\bar x,\,\bar y)\) and has gradient \(m=\dfrac{\sigma_{xy}}{\sigma_x^2}\):"))
  + D(r"y-\bar y=\frac{\sigma_{xy}}{\sigma_x^2}\,(x-\bar x)")
  + P(r"És l'equació punt-pendent d'una recta (unitat 7). Després l'escrivim com \(y=mx+n\).",
      r"Es la ecuación punto-pendiente de una recta (unidad 7). Después la escribimos como \(y=mx+n\).",
      r"It's the point-gradient equation of a line (unit 7). We then write it as \(y=mx+n\).")
  + note(r"El pendent \(m\) té el <strong>mateix signe</strong> que la covariància i que \(r\): si la correlació és positiva, la recta puja; si és negativa, baixa.",
         r"La pendiente \(m\) tiene el <strong>mismo signo</strong> que la covarianza y que \(r\): si la correlación es positiva, la recta sube; si es negativa, baja.",
         r"The gradient \(m\) has the <strong>same sign</strong> as the covariance and as \(r\): if the correlation is positive the line rises; if it's negative, it falls."))

s5 += box('ex', L("Exemple: hores d'estudi i nota de 5 alumnes (apartat 10.4)", 'Ejemplo: horas de estudio y nota de 5 alumnos (apartado 10.4)', 'Example: study hours and mark of 5 students (section 10.4)'),
  P(r"Ja sabem que \(\bar x=3\), \(\bar y=4\), \(\sigma_x^2=2\) i \(\sigma_{xy}=1\dc 8\). El pendent és:", r"Ya sabemos que \(\bar x=3\), \(\bar y=4\), \(\sigma_x^2=2\) y \(\sigma_{xy}=1\dc 8\). La pendiente es:", r"We already know that \(\bar x=3\), \(\bar y=4\), \(\sigma_x^2=2\) and \(\sigma_{xy}=1\dc 8\). The gradient is:")
  + D(r"m=\frac{\sigma_{xy}}{\sigma_x^2}=\frac{1\dc 8}{2}=0\dc 9")
  + D(r"y-4=0\dc 9\,(x-3)\ \Rightarrow\ y=0\dc 9x-2\dc 7+4\ \Rightarrow\ \boxed{y=0\dc 9x+1\dc 3}")
  + fig(nuvol(list(zip(EX, EY)), (0, 6, 1), (0, 7, 1), axes=AXH, means=True, reg=True))
  + P(r"El pendent ens diu que, per cada hora més d'estudi, la nota puja, de mitjana, \(0\dc 9\) punts.",
      r"La pendiente nos dice que, por cada hora más de estudio, la nota sube, de media, \(0\dc 9\) puntos.",
      r"The gradient tells us that, for each extra hour of study, the mark goes up by \(0\dc 9\) points on average."))
s5 += box('ex', L('Exemple: preu i unitats venudes (apartat 10.4)', 'Ejemplo: precio y unidades vendidas (apartado 10.4)', 'Example: price and units sold (section 10.4)'),
  D(r"\bar x=3\qquad \bar y=38\qquad \sigma_x^2=2\qquad \sigma_{xy}=-12\dc 8\qquad m=\frac{-12\dc 8}{2}=-6\dc 4")
  + D(r"y-38=-6\dc 4\,(x-3)\ \Rightarrow\ y=-6\dc 4x+19\dc 2+38\ \Rightarrow\ \boxed{y=-6\dc 4x+57\dc 2}")
  + fig(nuvol(list(zip(PX, PY)), (0, 6, 1), (0, 60, 10), axes=('€', L('unitats', 'unidades', 'units')), means=True, reg=True))
  + P(r"El pendent és negatiu: per cada euro que puja el preu, es venen unes \(6\dc 4\) unitats menys.",
      r"La pendiente es negativa: por cada euro que sube el precio, se venden unas \(6\dc 4\) unidades menos.",
      r"The gradient is negative: for each euro the price goes up, about \(6\dc 4\) fewer units are sold.")
  + note(r"La calculadora, en el mode \(y=a+bx\), dona directament la recta de regressió: \(a\) és l'<strong>ordenada en l'origen</strong> (la nostra \(n\)) i \(b\), el <strong>pendent</strong> (la nostra \(m\)). En aquest exemple, \(a=57\dc 2\) i \(b=-6\dc 4\).",
         r"La calculadora, en el modo \(y=a+bx\), da directamente la recta de regresión: \(a\) es la <strong>ordenada en el origen</strong> (nuestra \(n\)) y \(b\), la <strong>pendiente</strong> (nuestra \(m\)). En este ejemplo, \(a=57\dc 2\) y \(b=-6\dc 4\).",
         r"In \(y=a+bx\) mode the calculator gives the regression line directly: \(a\) is the <strong>y-intercept</strong> (our \(n\)) and \(b\) the <strong>gradient</strong> (our \(m\)). In this example \(a=57\dc 2\) and \(b=-6\dc 4\).", '🧮'))

s5 += (widget('w-eye', '👁️', L('Ajusta la recta a ull', 'Ajusta la recta a ojo', 'Fit the line by eye'),
              ['<p class="hint-s">' + L("Mou els controls per a canviar el pendent i l'ordenada de la recta taronja fins que s'ajuste al núvol. L'eina compara la suma dels quadrats dels errors de la teua recta amb la de la recta de regressió.",
                                        "Mueve los controles para cambiar la pendiente y la ordenada de la recta naranja hasta que se ajuste a la nube. La herramienta compara la suma de los cuadrados de los errores de tu recta con la de la recta de regresión.",
                                        "Move the sliders to change the gradient and intercept of the orange line until it fits the cloud. The tool compares the sum of squared errors of your line with that of the regression line.") + '</p>',
               seg([('a', L('Núvol A', 'Nube A', 'Cloud A')), ('b', L('Núvol B', 'Nube B', 'Cloud B')), ('c', L('Núvol C', 'Nube C', 'Cloud C'))]),
               '<div class="wrow">' + rng('m', -3, 3, 0.05, 0.5, 'pendent') + '</div><div class="wrow">' + rng('n', -2, 10, 0.1, 2, 'ordenada') + '</div>'
               + '<div class="wrow"><button class="btn" type="button" data-a="show">' + L("Mostra la recta de regressió", "Mostrar la recta de regresión", "Show the regression line") + '</button></div>'],
              out='<div class="gout cl-wrap"><svg class="sgraf nv" viewBox="0 0 340 250" role="img" aria-label="núvol"></svg></div>')
       + widget('w-reg', '📈', L('Calcula la recta de regressió', 'Calcula la recta de regresión', 'Find the regression line'),
                ['<p class="hint-s">' + L("Escriu les dades de X i de Y en el mateix ordre. L'eina calcula els paràmetres, escriu la recta pas a pas i la dibuixa sobre el núvol.",
                                          "Escribe los datos de X y de Y en el mismo orden. La herramienta calcula los parámetros, escribe la recta paso a paso y la dibuja sobre la nube.",
                                          "Type the X and Y data in the same order. The tool works out the measures, writes the line step by step and draws it on the cloud.") + '</p>',
                 seg([('ex', L('Hores i nota', 'Horas y nota', 'Hours and mark')), ('pr', L('Preu i vendes', 'Precio y ventas', 'Price and sales')), ('gel', L('Gelats', 'Helados', 'Ice creams')), ('own', L('Les meues', 'Los míos', 'My own'))]),
                 '<div class="wrow">' + tin('x', 'X', '', 'w') + '</div><div class="wrow">' + tin('y', 'Y', '', 'w') + '</div>'], out='<div class="tout"></div>')
       + drill('recta', 'Entrena: troba la recta de regressió', 'Entrena: encuentra la recta de regresión', 'Train: find the regression line'))

mQ, nQ = rl(SQ); assert (mQ, nQ) == (Fr(2, 5), Fr(17, 5))
mH, nH = rl(SH); assert (mH, nH) == (Fr(29, 28), Fr(55, 28)); ckr(mH, '1.04'); ckr(nH, '1.96'); ck(Fr(87, 25), '3.48'); ck(Fr(84, 25), '3.36')
mD, nD = rl(SD); assert (mD, nD) == (Fr(-14, 15), Fr(154, 15)); ckr(mD, '-0.93'); ckr(nD, '10.27')
s5 += levels(
 [prob(L(r"D'una distribució bidimensional sabem que \(\bar x=5\), \(\bar y=8\), \(\sigma_x^2=4\) i \(\sigma_{xy}=6\). Escriu la recta de regressió.",
         r"De una distribución bidimensional sabemos que \(\bar x=5\), \(\bar y=8\), \(\sigma_x^2=4\) y \(\sigma_{xy}=6\). Escribe la recta de regresión.",
         r"For a bivariate distribution we know that \(\bar x=5\), \(\bar y=8\), \(\sigma_x^2=4\) and \(\sigma_{xy}=6\). Write the regression line."),
       D(r"m=\frac{6}{4}=1\dc 5\qquad y-8=1\dc 5\,(x-5)\ \Rightarrow\ y=1\dc 5x-7\dc 5+8\ \Rightarrow\ \boxed{y=1\dc 5x+0\dc 5}")),
  prob(L(r"El centre de gravetat d'un núvol és \((2,\,5)\). Quina d'aquestes rectes pot ser la seua recta de regressió: \(y=2x+3\), \(y=2x+1\) o \(y=-2x+5\)?",
         r"El centro de gravedad de una nube es \((2,\,5)\). ¿Cuál de estas rectas puede ser su recta de regresión: \(y=2x+3\), \(y=2x+1\) o \(y=-2x+5\)?",
         r"The centre of gravity of a scatter plot is \((2,\,5)\). Which of these lines could be its regression line: \(y=2x+3\), \(y=2x+1\) or \(y=-2x+5\)?"),
       P(r"Ha de passar per \((2,\,5)\). Substituïm \(x=2\): \(2\cdot2+3=7\), \(\ 2\cdot2+1=5\), \(\ -2\cdot2+5=1\). Només ho compleix \(\boxed{y=2x+1}\).",
         r"Tiene que pasar por \((2,\,5)\). Sustituimos \(x=2\): \(2\cdot2+3=7\), \(\ 2\cdot2+1=5\), \(\ -2\cdot2+5=1\). Solo lo cumple \(\boxed{y=2x+1}\).",
         r"It must go through \((2,\,5)\). Substitute \(x=2\): \(2\cdot2+3=7\), \(\ 2\cdot2+1=5\), \(\ -2\cdot2+5=1\). Only \(\boxed{y=2x+1}\) works."))],
 [prob(L(r"Calcula la recta de regressió de \((1,3),\ (2,5),\ (4,4),\ (5,7),\ (8,6)\) (en l'apartat 10.4 vas calcular \(\bar x=4\), \(\bar y=5\), \(\sigma_x^2=6\) i \(\sigma_{xy}=2\dc 4\)). Dibuixa-la sobre el núvol.",
         r"Calcula la recta de regresión de \((1,3),\ (2,5),\ (4,4),\ (5,7),\ (8,6)\) (en el apartado 10.4 calculaste \(\bar x=4\), \(\bar y=5\), \(\sigma_x^2=6\) y \(\sigma_{xy}=2\dc 4\)). Dibújala sobre la nube.",
         r"Find the regression line of \((1,3),\ (2,5),\ (4,4),\ (5,7),\ (8,6)\) (in section 10.4 you found \(\bar x=4\), \(\bar y=5\), \(\sigma_x^2=6\) and \(\sigma_{xy}=2\dc 4\)). Draw it on the cloud."),
       D(r"m=\frac{2\dc 4}{6}=0\dc 4\qquad y-5=0\dc 4\,(x-4)\ \Rightarrow\ \boxed{y=0\dc 4x+3\dc 4}"),
       fig(nuvol(list(zip(QX, QY)), (0, 9, 1), (0, 8, 1), means=True, reg=True))
       + P(r"Per a dibuixar-la, n'hi ha prou amb dos punts: el centre de gravetat \((4,\,5)\) i, per exemple, \(x=0\to y=3\dc 4\).",
           r"Para dibujarla, basta con dos puntos: el centro de gravedad \((4,\,5)\) y, por ejemplo, \(x=0\to y=3\dc 4\).",
           r"To draw it, two points are enough: the centre of gravity \((4,\,5)\) and, for example, \(x=0\to y=3\dc 4\).")),
  prob(L(r"Troba la recta de regressió de les hores d'estudi i les notes dels 10 alumnes. En l'apartat 10.4 vas trobar \(\bar x=3\dc 8\), \(\bar y=5\dc 9\), \(\sigma_x^2=3\dc 36\) i \(\sigma_{xy}=3\dc 48\).",
         r"Encuentra la recta de regresión de las horas de estudio y las notas de los 10 alumnos. En el apartado 10.4 encontraste \(\bar x=3\dc 8\), \(\bar y=5\dc 9\), \(\sigma_x^2=3\dc 36\) y \(\sigma_{xy}=3\dc 48\).",
         r"Find the regression line of the study hours and marks of the 10 students. In section 10.4 you found \(\bar x=3\dc 8\), \(\bar y=5\dc 9\), \(\sigma_x^2=3\dc 36\) and \(\sigma_{xy}=3\dc 48\)."),
       D(r"m=\frac{3\dc 48}{3\dc 36}\approx1\dc 04\qquad y-5\dc 9=1\dc 04\,(x-3\dc 8)\ \Rightarrow\ \boxed{y\approx1\dc 04x+1\dc 96}"),
       fig(nuvol(list(zip(HX, HY)), (0, 8, 1), (0, 10, 1), axes=AXH, means=True, reg=True))
       + P(r"Fes els càlculs amb tots els decimals: \(m=\frac{29}{28}\) i \(n=5\dc 9-\frac{29}{28}\cdot3\dc 8=\frac{55}{28}\approx1\dc 96\).",
           r"Haz los cálculos con todos los decimales: \(m=\frac{29}{28}\) y \(n=5\dc 9-\frac{29}{28}\cdot3\dc 8=\frac{55}{28}\approx1\dc 96\).",
           r"Do the working with all the decimals: \(m=\frac{29}{28}\) and \(n=5\dc 9-\frac{29}{28}\cdot3\dc 8=\frac{55}{28}\approx1\dc 96\)."))],
 [prob(L(r"Calcula la recta de regressió de \((2,8),\ (3,8),\ (5,6),\ (6,4),\ (9,2)\) (apartat 10.4). Què indica el pendent?",
         r"Calcula la recta de regresión de \((2,8),\ (3,8),\ (5,6),\ (6,4),\ (9,2)\) (apartado 10.4). ¿Qué indica la pendiente?",
         r"Find the regression line of \((2,8),\ (3,8),\ (5,6),\ (6,4),\ (9,2)\) (section 10.4). What does the gradient tell you?"),
       D(r"\bar x=5\qquad \bar y=5\dc 6\qquad \sigma_x^2=6\qquad \sigma_{xy}=-5\dc 6\qquad m=\frac{-5\dc 6}{6}\approx-0\dc 93"),
       D(r"y-5\dc 6=-0\dc 93\ldots(x-5)\ \Rightarrow\ \boxed{y\approx-0\dc 93x+10\dc 27}"),
       P(r"El pendent és negatiu: quan \(x\) augmenta 1 unitat, \(y\) disminueix, de mitjana, unes \(0\dc 93\) unitats.",
         r"La pendiente es negativa: cuando \(x\) aumenta 1 unidad, \(y\) disminuye, de media, unas \(0\dc 93\) unidades.",
         r"The gradient is negative: when \(x\) goes up by 1, \(y\) goes down by about \(0\dc 93\) on average.")),
  prob(L(r"La recta de regressió d'una distribució és \(y=2x+3\) i la mitjana de la \(X\) és \(\bar x=4\). Quant val \(\bar y\)?",
         r"La recta de regresión de una distribución es \(y=2x+3\) y la media de la \(X\) es \(\bar x=4\). ¿Cuánto vale \(\bar y\)?",
         r"The regression line of a distribution is \(y=2x+3\) and the mean of \(X\) is \(\bar x=4\). What is \(\bar y\)?"),
       P(r"La recta passa pel centre de gravetat: \(\bar y=2\cdot4+3=\boxed{11}\).", r"La recta pasa por el centro de gravedad: \(\bar y=2\cdot4+3=\boxed{11}\).", r"The line passes through the centre of gravity: \(\bar y=2\cdot4+3=\boxed{11}\)."))])
ck(Fr(6, 4) * -5 + 8, '0.5')
s5 += practice([('★☆☆', L(r"Escriu la recta de regressió si \(\bar x=10\), \(\bar y=20\), \(\sigma_x^2=5\) i \(\sigma_{xy}=-4\).", r"Escribe la recta de regresión si \(\bar x=10\), \(\bar y=20\), \(\sigma_x^2=5\) y \(\sigma_{xy}=-4\).", r"Write the regression line if \(\bar x=10\), \(\bar y=20\), \(\sigma_x^2=5\) and \(\sigma_{xy}=-4\).")),
                ('★★☆', L(r"Calcula la recta de regressió de \((1,3),\ (2,2),\ (3,4),\ (4,6),\ (5,5)\).", r"Calcula la recta de regresión de \((1,3),\ (2,2),\ (3,4),\ (4,6),\ (5,5)\).", r"Find the regression line of \((1,3),\ (2,2),\ (3,4),\ (4,6),\ (5,5)\)."))],
               L(r"1) \(m=\frac{-4}{5}=-0\dc 8\); \(y-20=-0\dc 8(x-10)\Rightarrow y=-0\dc 8x+28\). &nbsp; 2) \(\bar x=3\), \(\bar y=4\), \(\sigma_x^2=2\), \(\sigma_{xy}=\frac{68}{5}-12=1\dc 6\); \(m=\frac{1\dc 6}{2}=0\dc 8\); \(y-4=0\dc 8(x-3)\Rightarrow y=0\dc 8x+1\dc 6\).",
                 r"1) \(m=\frac{-4}{5}=-0\dc 8\); \(y-20=-0\dc 8(x-10)\Rightarrow y=-0\dc 8x+28\). &nbsp; 2) \(\bar x=3\), \(\bar y=4\), \(\sigma_x^2=2\), \(\sigma_{xy}=\frac{68}{5}-12=1\dc 6\); \(m=\frac{1\dc 6}{2}=0\dc 8\); \(y-4=0\dc 8(x-3)\Rightarrow y=0\dc 8x+1\dc 6\).",
                 r"1) \(m=\frac{-4}{5}=-0\dc 8\); \(y-20=-0\dc 8(x-10)\Rightarrow y=-0\dc 8x+28\). &nbsp; 2) \(\bar x=3\), \(\bar y=4\), \(\sigma_x^2=2\), \(\sigma_{xy}=\frac{68}{5}-12=1\dc 6\); \(m=\frac{1\dc 6}{2}=0\dc 8\); \(y-4=0\dc 8(x-3)\Rightarrow y=0\dc 8x+1\dc 6\)."))
_S = bi([1, 2, 3, 4, 5], [3, 2, 4, 6, 5]); assert (_S['mx'], _S['my'], _S['vx'], _S['sxy'], _S['c']) == (3, 4, 2, 68, Fr(8, 5)) and rl(_S) == (Fr(4, 5), Fr(8, 5))
ck(Fr(-4, 5) * -10 + 20, 28)

# =====================================================================
# 10.6 Estimacions
# =====================================================================
yE = mE * Fr(7, 2) + nE; ck(yE, '4.45'); y12 = mE * 12 + nE; ck(y12, '12.1')
yP = mP * Fr(7, 2) + nP; ck(yP, '34.8'); y10 = mP * 10 + nP; ck(y10, '-6.8')
xP = (45 - nP) / mP; ckr(xP, '1.91')
s6 = box('def', L('Estimacions amb la recta de regressió', 'Estimaciones con la recta de regresión', 'Estimates with the regression line'),
  P(r"Si coneixem la recta de regressió \(y=mx+n\), podem <strong>estimar</strong> (preveure) quin valor tindrà \(Y\) per a un valor \(x_0\) de \(X\) que no està en les dades: n'hi ha prou amb substituir.",
    r"Si conocemos la recta de regresión \(y=mx+n\), podemos <strong>estimar</strong> (prever) qué valor tendrá \(Y\) para un valor \(x_0\) de \(X\) que no está en los datos: basta con sustituir.",
    r"If we know the regression line \(y=mx+n\), we can <strong>estimate</strong> (predict) the value of \(Y\) for a value \(x_0\) of \(X\) that isn't in the data: just substitute.")
  + D(r"\hat y=m\cdot x_0+n")
  + P(r"El valor \(\hat y\) («i barret») és una <strong>estimació</strong>: no és el valor exacte que tindrà un individu, sinó el valor que <strong>esperem</strong> de mitjana.",
      r"El valor \(\hat y\) («y gorro») es una <strong>estimación</strong>: no es el valor exacto que tendrá un individuo, sino el valor que <strong>esperamos</strong> de media.",
      r"The value \(\hat y\) (“y hat”) is an <strong>estimate</strong>: it isn't the exact value an individual will have, but the value we <strong>expect</strong> on average.")
  + box('ex', L("Exemple: hores d'estudi i nota", 'Ejemplo: horas de estudio y nota', 'Example: study hours and mark'),
        P(r"Amb la recta \(y=0\dc 9x+1\dc 3\) (\(r=0\dc 9\)), quina nota esperem per a un alumne que estudie 3,5 hores?",
          r"Con la recta \(y=0\dc 9x+1\dc 3\) (\(r=0\dc 9\)), ¿qué nota esperamos para un alumno que estudie 3,5 horas?",
          r"With the line \(y=0\dc 9x+1\dc 3\) (\(r=0\dc 9\)), what mark do we expect for a student who studies 3.5 hours?")
        + D(r"\hat y=0\dc 9\cdot3\dc 5+1\dc 3=3\dc 15+1\dc 3=\boxed{4\dc 45}")
        + fig(nuvol(list(zip(EX, EY)), (0, 6, 1), (0, 7, 1), axes=AXH, reg=True, est=(Fr(7, 2), yE)))
        + P(r"I si estudiara 12 hores? \(\hat y=0\dc 9\cdot12+1\dc 3=12\dc 1\): una nota impossible! Les dades només van d'1 a 5 hores i no sabem si la relació continua igual tan lluny.",
            r"¿Y si estudiara 12 horas? \(\hat y=0\dc 9\cdot12+1\dc 3=12\dc 1\): ¡una nota imposible! Los datos solo van de 1 a 5 horas y no sabemos si la relación sigue igual tan lejos.",
            r"And if they studied 12 hours? \(\hat y=0\dc 9\cdot12+1\dc 3=12\dc 1\): an impossible mark! The data only go from 1 to 5 hours and we don't know whether the relationship holds that far out.")))

s6 += box('prop', L('Són fiables les estimacions?', '¿Son fiables las estimaciones?', 'Are the estimates reliable?'),
  P(r"Una estimació és més fiable com més es complisquen aquestes condicions:", r"Una estimación es más fiable cuanto más se cumplan estas condiciones:", r"An estimate is more reliable the more these conditions are met:")
  + ul(L(r"La correlació és <strong>forta</strong>: \(|r|\) és pròxim a 1. Si \(|r|\ge0\dc 8\), les estimacions són bones; si \(|r|\) està entre \(0\dc 5\) i \(0\dc 8\), només són aproximades; si \(|r|<0\dc 5\), <strong>no</strong> són fiables.",
         r"La correlación es <strong>fuerte</strong>: \(|r|\) está cerca de 1. Si \(|r|\ge0\dc 8\), las estimaciones son buenas; si \(|r|\) está entre \(0\dc 5\) y \(0\dc 8\), solo son aproximadas; si \(|r|<0\dc 5\), <strong>no</strong> son fiables.",
         r"The correlation is <strong>strong</strong>: \(|r|\) is close to 1. If \(|r|\ge0\dc 8\) the estimates are good; if \(|r|\) is between \(0\dc 5\) and \(0\dc 8\) they're only rough; if \(|r|<0\dc 5\) they're <strong>not</strong> reliable."),
       L(r"El valor \(x_0\) està <strong>dins</strong> de l'interval de les dades (o molt a prop). Estimar dins de les dades és <strong>interpolar</strong>; estimar fora, <strong>extrapolar</strong>, i com més lluny, menys fiable.",
         r"El valor \(x_0\) está <strong>dentro</strong> del intervalo de los datos (o muy cerca). Estimar dentro de los datos es <strong>interpolar</strong>; estimar fuera, <strong>extrapolar</strong>, y cuanto más lejos, menos fiable.",
         r"The value \(x_0\) is <strong>inside</strong> the range of the data (or very close). Estimating inside the data is <strong>interpolating</strong>; estimating outside is <strong>extrapolating</strong>, and the further out, the less reliable."),
       L(r"Hi ha <strong>moltes dades</strong>: amb poques parelles, la recta pot canviar molt si n'afegim una altra.",
         r"Hay <strong>muchos datos</strong>: con pocas parejas, la recta puede cambiar mucho si añadimos otra.",
         r"There are <strong>lots of data</strong>: with few pairs, the line can change a lot if we add another one."))
  + box('ex', L('Exemple: preu i unitats venudes', 'Ejemplo: precio y unidades vendidas', 'Example: price and units sold'),
        P(r"Amb \(y=-6\dc 4x+57\dc 2\) i \(r\approx-0\dc 99\), quantes unitats esperem vendre si el preu és de 3,50 €? I si és de 10 €?",
          r"Con \(y=-6\dc 4x+57\dc 2\) y \(r\approx-0\dc 99\), ¿cuántas unidades esperamos vender si el precio es de 3,50 €? ¿Y si es de 10 €?",
          r"With \(y=-6\dc 4x+57\dc 2\) and \(r\approx-0\dc 99\), how many units do we expect to sell at a price of €3.50? And at €10?")
        + D(r"\hat y(3\dc 5)=-6\dc 4\cdot3\dc 5+57\dc 2=34\dc 8\approx\boxed{35\ \tri{unitats}{unidades}{units}}")
        + P(r"És una estimació <strong>molt fiable</strong>: \(|r|\) és quasi 1 i 3,50 € està entre 1 i 5 €. En canvi, per a 10 € dona \(-6\dc 4\cdot10+57\dc 2=-6\dc 8\) unitats, cosa impossible: extrapolem massa lluny.",
            r"Es una estimación <strong>muy fiable</strong>: \(|r|\) es casi 1 y 3,50 € está entre 1 y 5 €. En cambio, para 10 € da \(-6\dc 4\cdot10+57\dc 2=-6\dc 8\) unidades, algo imposible: extrapolamos demasiado lejos.",
            r"It's a <strong>very reliable</strong> estimate: \(|r|\) is almost 1 and €3.50 is between €1 and €5. At €10, however, it gives \(-6\dc 4\cdot10+57\dc 2=-6\dc 8\) units, which is impossible: we're extrapolating too far."))
  + box('ex', L('Estimar x a partir de y', 'Estimar x a partir de y', 'Estimating x from y'),
        P(r"A quin preu hauríem de vendre el producte per a vendre'n 45 unitats? Ara coneixem \(y\): posem \(y=45\) i aïllem \(x\).",
          r"¿A qué precio deberíamos vender el producto para vender 45 unidades? Ahora conocemos \(y\): ponemos \(y=45\) y despejamos \(x\).",
          r"At what price should we sell the product to sell 45 units? Now we know \(y\): set \(y=45\) and solve for \(x\).")
        + D(r"45=-6\dc 4x+57\dc 2\ \Rightarrow\ 6\dc 4x=12\dc 2\ \Rightarrow\ x=\frac{12\dc 2}{6\dc 4}\approx\boxed{1\dc 91\ \text{€}}")
        + note(r"Aquesta manera d'estimar \(x\) només dona bons resultats quan la correlació és <strong>molt forta</strong> (\(|r|\) pròxim a 1), com en aquest cas.",
               r"Esta manera de estimar \(x\) solo da buenos resultados cuando la correlación es <strong>muy fuerte</strong> (\(|r|\) cerca de 1), como en este caso.",
               r"This way of estimating \(x\) only works well when the correlation is <strong>very strong</strong> (\(|r|\) close to 1), as here.", '⚠️')))

s6 += (widget('w-est', '🔮', L('Fes estimacions', 'Haz estimaciones', 'Make estimates'),
              ['<p class="hint-s">' + L("Tria unes dades i un valor de x: l'eina calcula l'estimació amb la recta de regressió, la marca en el núvol i et diu si és fiable.",
                                        "Elige unos datos y un valor de x: la herramienta calcula la estimación con la recta de regresión, la marca en la nube y te dice si es fiable.",
                                        "Choose some data and a value of x: the tool works out the estimate with the regression line, marks it on the cloud and tells you whether it's reliable.") + '</p>',
               seg([('ex', L('Hores i nota', 'Horas y nota', 'Hours and mark')), ('gel', L('Gelats', 'Helados', 'Ice creams')), ('feb', L('Correlació feble', 'Correlación débil', 'Weak correlation'))]),
               '<div class="wrow">' + rng('x0', 0, 10, 0.1, 3.5, 'x0') + '</div>'], out='<div class="tout"></div>')
       + drill('est', "Entrena: fes l'estimació", 'Entrena: haz la estimación', 'Train: make the estimate')
       + drill('fiab', 'Entrena: és fiable l’estimació?', 'Entrena: ¿es fiable la estimación?', 'Train: is the estimate reliable?', 'opts'))

mT, nT = rl(S2T); ckr(mT, '4.79'); ckr(nT, '-51.18'); ckr(S2T['r'], '0.99'); ck(S2T['vx'], '33.6875'); ck(S2T['c'], '161.25')
yT27 = mT * 27 + nT; ckr(yT27, '78.06'); yT40 = mT * 40 + nT; ckr(yT40, '140.28')
yH45 = mH * Fr(9, 2) + nH; ckr(yH45, '6.6', 1); ckr(Fr(104, 100) * Fr(9, 2) + Fr(196, 100), '6.64')
x8 = (8 - nH) / mH; ckr(x8, '5.83')
s6 += levels(
 [prob(L(r"La recta de regressió entre l'alçada dels pares (\(X\), en cm) i la dels fills adults (\(Y\), en cm) d'una mostra és \(y=0\dc 5x+88\), amb \(r=0\dc 82\). Les alçades dels pares de la mostra van de 160 a 190 cm. Quina alçada esperem per al fill d'un pare de 176 cm? És fiable?",
         r"La recta de regresión entre la altura de los padres (\(X\), en cm) y la de los hijos adultos (\(Y\), en cm) de una muestra es \(y=0\dc 5x+88\), con \(r=0\dc 82\). Las alturas de los padres de la muestra van de 160 a 190 cm. ¿Qué altura esperamos para el hijo de un padre de 176 cm? ¿Es fiable?",
         r"The regression line between fathers' heights (\(X\), in cm) and their adult sons' heights (\(Y\), in cm) in a sample is \(y=0\dc 5x+88\), with \(r=0\dc 82\). The fathers' heights in the sample range from 160 to 190 cm. What height do we expect for the son of a 176 cm father? Is it reliable?"),
       D(r"\hat y=0\dc 5\cdot176+88=88+88=\boxed{176\ \text{cm}}"),
       P(r"És <strong>fiable</strong>: la correlació és forta (\(r=0\dc 82\)) i 176 cm està dins de l'interval de les dades.", r"Es <strong>fiable</strong>: la correlación es fuerte (\(r=0\dc 82\)) y 176 cm está dentro del intervalo de los datos.", r"It's <strong>reliable</strong>: the correlation is strong (\(r=0\dc 82\)) and 176 cm is inside the range of the data.")),
  prob(L(r"Digues si aquestes estimacions són fiables: a) \(r=0\dc 95\) i estimem dins de les dades; b) \(r=-0\dc 3\) i estimem dins de les dades; c) \(r=0\dc 97\), les dades de \(X\) van de 2 a 8 i estimem per a \(x=50\); d) \(r=-0\dc 88\) i estimem per a un valor proper a \(\bar x\).",
         r"Di si estas estimaciones son fiables: a) \(r=0\dc 95\) y estimamos dentro de los datos; b) \(r=-0\dc 3\) y estimamos dentro de los datos; c) \(r=0\dc 97\), los datos de \(X\) van de 2 a 8 y estimamos para \(x=50\); d) \(r=-0\dc 88\) y estimamos para un valor cercano a \(\bar x\).",
         r"Say whether these estimates are reliable: a) \(r=0\dc 95\) and we estimate inside the data; b) \(r=-0\dc 3\) and we estimate inside the data; c) \(r=0\dc 97\), the \(X\) data go from 2 to 8 and we estimate for \(x=50\); d) \(r=-0\dc 88\) and we estimate for a value close to \(\bar x\)."),
       P(r"a) <strong>Sí</strong>. &nbsp; b) <strong>No</strong>: la correlació és feble. &nbsp; c) <strong>No</strong>: encara que \(r\) és alt, 50 està molt lluny de les dades (extrapolació). &nbsp; d) <strong>Sí</strong>: \(|r|=0\dc 88\) és alt (el signe negatiu no importa).",
         r"a) <strong>Sí</strong>. &nbsp; b) <strong>No</strong>: la correlación es débil. &nbsp; c) <strong>No</strong>: aunque \(r\) es alto, 50 está muy lejos de los datos (extrapolación). &nbsp; d) <strong>Sí</strong>: \(|r|=0\dc 88\) es alto (el signo negativo no importa).",
         r"a) <strong>Yes</strong>. &nbsp; b) <strong>No</strong>: the correlation is weak. &nbsp; c) <strong>No</strong>: although \(r\) is high, 50 is far outside the data (extrapolation). &nbsp; d) <strong>Yes</strong>: \(|r|=0\dc 88\) is high (the minus sign doesn't matter)."))],
 [prob(L(r"Amb la recta de les hores d'estudi i les notes dels 10 alumnes, \(y\approx1\dc 04x+1\dc 96\) (\(r\approx0\dc 94\)), quina nota esperem per a qui estudie 4 hores i mitja? Quantes hores hauria d'estudiar una alumna per a traure un 8?",
         r"Con la recta de las horas de estudio y las notas de los 10 alumnos, \(y\approx1\dc 04x+1\dc 96\) (\(r\approx0\dc 94\)), ¿qué nota esperamos para quien estudie 4 horas y media? ¿Cuántas horas debería estudiar una alumna para sacar un 8?",
         r"With the line for the 10 students' study hours and marks, \(y\approx1\dc 04x+1\dc 96\) (\(r\approx0\dc 94\)), what mark do we expect for someone who studies four and a half hours? How many hours should a student study to get an 8?"),
       D(r"\hat y=1\dc 04\cdot4\dc 5+1\dc 96\approx\boxed{6\dc 6}"),
       D(r"8=1\dc 04x+1\dc 96\ \Rightarrow\ x=\frac{8-1\dc 96}{1\dc 04}\approx\boxed{5\dc 8\ \tri{hores}{horas}{hours}}"),
       P(r"Totes dues estimacions són fiables: \(r\) és alt i els valors estan dins de les dades (d'1 a 7 hores).", r"Las dos estimaciones son fiables: \(r\) es alto y los valores están dentro de los datos (de 1 a 7 horas).", r"Both estimates are reliable: \(r\) is high and the values are inside the data (1 to 7 hours).")),
  prob(L(r"Amb les dades de la gelateria (apartat 10.2) s'obté \(r\approx0\dc 99\) i la recta de regressió \(y\approx4\dc 79x-51\dc 18\). Quants gelats esperem vendre un dia a 27 °C? I un dia a 40 °C? Quina estimació és més fiable?",
         r"Con los datos de la heladería (apartado 10.2) se obtiene \(r\approx0\dc 99\) y la recta de regresión \(y\approx4\dc 79x-51\dc 18\). ¿Cuántos helados esperamos vender un día a 27 °C? ¿Y un día a 40 °C? ¿Qué estimación es más fiable?",
         r"With the ice-cream shop data (section 10.2) we get \(r\approx0\dc 99\) and the regression line \(y\approx4\dc 79x-51\dc 18\). How many ice creams do we expect to sell on a 27 °C day? And on a 40 °C day? Which estimate is more reliable?"),
       D(r"\hat y(27)\approx4\dc 79\cdot27-51\dc 18\approx\boxed{78}\qquad \hat y(40)\approx4\dc 79\cdot40-51\dc 18\approx\boxed{140}"),
       P(r"La de 27 °C és més fiable: està dins de les dades (de 14 a 32 °C). La de 40 °C és una extrapolació: potser amb tanta calor la gent no ix de casa i se'n venen menys.",
         r"La de 27 °C es más fiable: está dentro de los datos (de 14 a 32 °C). La de 40 °C es una extrapolación: quizá con tanto calor la gente no sale de casa y se venden menos.",
         r"The 27 °C one is more reliable: it's inside the data (14 to 32 °C). The 40 °C one is an extrapolation: maybe in such heat people stay indoors and fewer are sold.")
       + fig(nuvol(list(zip(T2X, T2Y)), (10, 45, 5), (0, 160, 20), axes=('°C', L('gelats', 'helados', 'ice creams')), reg=True, est=(27, yT27))))],
 [prob(L(r"En una botiga d'informàtica han observat que, quan el preu (\(X\), en €) d'un tipus d'auriculars és 20, 25, 30, 35 i 40 €, en venen 50, 46, 39, 33 i 27 al mes. Calcula el coeficient de correlació i la recta de regressió, i estima quants en vendrien a 32 €.",
         r"En una tienda de informática han observado que, cuando el precio (\(X\), en €) de un tipo de auriculares es 20, 25, 30, 35 y 40 €, venden 50, 46, 39, 33 y 27 al mes. Calcula el coeficiente de correlación y la recta de regresión, y estima cuántos venderían a 32 €.",
         r"A computer shop has noticed that when the price (\(X\), in €) of a type of headphones is €20, 25, 30, 35 and 40, they sell 50, 46, 39, 33 and 27 a month. Find the correlation coefficient and the regression line, and estimate how many they'd sell at €32."),
       btab([20, 25, 30, 35, 40], [50, 46, 39, 33, 27]),
       D(r"\bar x=30\qquad \bar y=39\qquad \sigma_x^2=\frac{4\,750}{5}-900=50\qquad \sigma_y^2=\frac{7\,955}{5}-1\,521=70\qquad \sigma_{xy}=\frac{5\,555}{5}-1\,170=-59"),
       D(r"r=\frac{-59}{\sqrt{50}\cdot\sqrt{70}}\approx\boxed{-0\dc 997}\qquad m=\frac{-59}{50}=-1\dc 18\qquad y-39=-1\dc 18\,(x-30)\Rightarrow\boxed{y=-1\dc 18x+74\dc 4}"),
       D(r"\hat y(32)=-1\dc 18\cdot32+74\dc 4=36\dc 64\approx\boxed{37\ \tri{auriculars}{auriculares}{headphones}}"),
       P(r"És una estimació molt fiable: la correlació és negativa i quasi perfecta, i 32 € està dins de les dades.", r"Es una estimación muy fiable: la correlación es negativa y casi perfecta, y 32 € está dentro de los datos.", r"It's a very reliable estimate: the correlation is negative and almost perfect, and €32 is inside the data."))])
SA = bi([20, 25, 30, 35, 40], [50, 46, 39, 33, 27])
assert (SA['mx'], SA['my'], SA['sx2'], SA['sy2'], SA['sxy'], SA['vx'], SA['vy'], SA['c']) == (30, 39, 4750, 7955, 5555, 50, 70, -59)
ckr(SA['r'], '-0.997', 3); assert rl(SA) == (Fr(-59, 50), Fr(372, 5)); ck(Fr(-59, 50) * 32 + Fr(372, 5), '36.64')
s6 += practice([('★☆☆', L(r"Amb la recta \(y=-0\dc 8x+28\), estima \(y\) per a \(x=12\) i per a \(x=7\dc 5\).", r"Con la recta \(y=-0\dc 8x+28\), estima \(y\) para \(x=12\) y para \(x=7\dc 5\).", r"Using the line \(y=-0\dc 8x+28\), estimate \(y\) for \(x=12\) and for \(x=7\dc 5\).")),
                ('★★☆', L(r"Entre les hores de son i la nota d'un examen d'uns alumnes s'ha obtingut \(r=0\dc 25\). Té sentit fer servir la recta de regressió per a estimar la nota d'un alumne que ha dormit 8 hores?", r"Entre las horas de sueño y la nota de un examen de unos alumnos se ha obtenido \(r=0\dc 25\). ¿Tiene sentido usar la recta de regresión para estimar la nota de un alumno que ha dormido 8 horas?", r"Between hours of sleep and a test mark for some students we got \(r=0\dc 25\). Does it make sense to use the regression line to estimate the mark of a student who slept 8 hours?"))],
               L(r"1) \(\hat y(12)=-9\dc 6+28=18\dc 4\); \(\ \hat y(7\dc 5)=-6+28=22\). &nbsp; 2) No: la correlació és molt feble i l'estimació no seria fiable.",
                 r"1) \(\hat y(12)=-9\dc 6+28=18\dc 4\); \(\ \hat y(7\dc 5)=-6+28=22\). &nbsp; 2) No: la correlación es muy débil y la estimación no sería fiable.",
                 r"1) \(\hat y(12)=-9\dc 6+28=18\dc 4\); \(\ \hat y(7\dc 5)=-6+28=22\). &nbsp; 2) No: the correlation is very weak and the estimate wouldn't be reliable."))
ck(Fr(-8, 10) * 12 + 28, '18.4'); ck(Fr(-8, 10) * Fr(15, 2) + 28, 22)
