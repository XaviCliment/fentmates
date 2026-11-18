# Apartat 10.4 dels apunts de la Unitat 10 de 4t ESO Matemàtiques A (Estadística bidimensional): coeficient de correlació
# (covariància, càlcul de r amb una taula i interpretació).
from comu import *
from s12 import HX, HY, SH

# exemple guia: 5 alumnes, hores d'estudi i nota (r = 0,9; recta y = 0,9x + 1,3 a 10.5)
EX = [1, 2, 3, 4, 5]; EY = [2, 3, 5, 4, 6]; SE = bi(EX, EY)
assert (SE['sx2'], SE['sy2'], SE['sxy'], SE['mx'], SE['my'], SE['vx'], SE['vy'], SE['c']) == (55, 90, 69, 3, 4, 2, 2, Fr(9, 5))
ckr(SE['r'], '0.9'); ckr(SE['sdx'], '1.41')
# preu i unitats venudes (negativa)
PX = [1, 2, 3, 4, 5]; PY = [50, 44, 40, 32, 24]; SP = bi(PX, PY)
assert (SP['sy'], SP['sy2'], SP['sxy'], SP['my'], SP['vy'], SP['c']) == (190, 7636, 506, 38, Fr(416, 5), Fr(-64, 5))
ckr(SP['sdy'], '9.12'); ckr(SP['r'], '-0.99')

RSCALE = tbl([M('r'), L('Correlació', 'Correlación', 'Correlation'), L('Núvol', 'Nube', 'Cloud')],
  [[M('r=1'), L('positiva perfecta (funcional)', 'positiva perfecta (funcional)', 'perfect positive (functional)'), L('tots els punts en una recta que puja', 'todos los puntos en una recta que sube', 'all points on a rising line')],
   [M(r'0\dc 8\le r<1'), L('positiva forta', 'positiva fuerte', 'strong positive'), L('puja; punts molt a prop d\'una recta', 'sube; puntos muy cerca de una recta', 'rises; points very close to a line')],
   [M(r'0\dc 5\le r<0\dc 8'), L('positiva moderada', 'positiva moderada', 'moderate positive'), L('puja; punts bastant escampats', 'sube; puntos bastante dispersos', 'rises; points fairly scattered')],
   [M(r'0<r<0\dc 5'), L('positiva feble', 'positiva débil', 'weak positive'), L('puja una mica; molt escampats', 'sube un poco; muy dispersos', 'rises slightly; very scattered')],
   [M(r'r\approx0'), L('nul·la', 'nula', 'zero'), L('no puja ni baixa', 'no sube ni baja', 'neither rises nor falls')],
   [M(r'r<0'), L('negativa (feble, moderada o forta, igual que les positives)', 'negativa (débil, moderada o fuerte, igual que las positivas)', 'negative (weak, moderate or strong, as for positive)'), L('baixa', 'baja', 'falls')],
   [M('r=-1'), L('negativa perfecta (funcional)', 'negativa perfecta (funcional)', 'perfect negative (functional)'), L('tots els punts en una recta que baixa', 'todos los puntos en una recta que baja', 'all points on a falling line')]])

s4 = box('def', L('El coeficient de correlació', 'El coeficiente de correlación', 'The correlation coefficient'),
  P(r"Mirant el núvol podem dir si la correlació és forta o feble, però de manera aproximada. Per a <strong>mesurar-la</strong> amb un nombre fem servir el <strong>coeficient de correlació lineal</strong> (de Pearson), \(r\):",
    r"Mirando la nube podemos decir si la correlación es fuerte o débil, pero de manera aproximada. Para <strong>medirla</strong> con un número usamos el <strong>coeficiente de correlación lineal</strong> (de Pearson), \(r\):",
    r"Looking at the cloud we can say roughly whether the correlation is strong or weak. To <strong>measure</strong> it with a number we use the <strong>linear correlation coefficient</strong> (Pearson's), \(r\):")
  + ul(L(r"Sempre és un nombre entre \(-1\) i \(1\): \(\ -1\le r\le 1\).", r"Siempre es un número entre \(-1\) y \(1\): \(\ -1\le r\le 1\).", r"It's always a number between \(-1\) and \(1\): \(\ -1\le r\le 1\)."),
       L(r"El <strong>signe</strong> de \(r\) diu el <strong>sentit</strong>: si \(r>0\), la correlació és positiva; si \(r<0\), negativa.", r"El <strong>signo</strong> de \(r\) dice el <strong>sentido</strong>: si \(r>0\), la correlación es positiva; si \(r<0\), negativa.", r"The <strong>sign</strong> of \(r\) gives the <strong>direction</strong>: if \(r>0\) the correlation is positive; if \(r<0\), negative."),
       L(r"El <strong>valor absolut</strong> \(|r|\) diu la <strong>força</strong>: com més a prop de 1, més forta; com més a prop de 0, més feble.", r"El <strong>valor absoluto</strong> \(|r|\) dice la <strong>fuerza</strong>: cuanto más cerca de 1, más fuerte; cuanto más cerca de 0, más débil.", r"The <strong>absolute value</strong> \(|r|\) gives the <strong>strength</strong>: the closer to 1, the stronger; the closer to 0, the weaker."))
  + RSCALE
  + note(r"\(r=-0\dc 9\) indica una correlació <strong>més forta</strong> que \(r=0\dc 6\): la força la dona \(|r|\), no el signe.",
         r"\(r=-0\dc 9\) indica una correlación <strong>más fuerte</strong> que \(r=0\dc 6\): la fuerza la da \(|r|\), no el signo.",
         r"\(r=-0\dc 9\) shows a <strong>stronger</strong> correlation than \(r=0\dc 6\): strength comes from \(|r|\), not the sign.", '⚠️'))

s4 += box('prop', L('Com es calcula r', 'Cómo se calcula r', 'How to calculate r'),
  P(r"Necessitem les mitjanes i les desviacions típiques de cada variable (com en la unitat 9) i un paràmetre nou, la <strong>covariància</strong> \(\sigma_{xy}\), que mesura si les dues variables creixen juntes (\(\sigma_{xy}>0\)) o una creix quan l'altra decreix (\(\sigma_{xy}<0\)):",
    r"Necesitamos las medias y las desviaciones típicas de cada variable (como en la unidad 9) y un parámetro nuevo, la <strong>covarianza</strong> \(\sigma_{xy}\), que mide si las dos variables crecen juntas (\(\sigma_{xy}>0\)) o una crece cuando la otra decrece (\(\sigma_{xy}<0\)):",
    r"We need the mean and standard deviation of each variable (as in unit 9) and a new measure, the <strong>covariance</strong> \(\sigma_{xy}\), which tells us whether the two variables increase together (\(\sigma_{xy}>0\)) or one increases as the other decreases (\(\sigma_{xy}<0\)):")
  + ol(L(r"Fes una taula amb les columnes \(x_i\), \(y_i\), \(x_i^2\), \(y_i^2\) i \(x_i\cdot y_i\), i suma-les.", r"Haz una tabla con las columnas \(x_i\), \(y_i\), \(x_i^2\), \(y_i^2\) y \(x_i\cdot y_i\), y súmalas.", r"Make a table with columns \(x_i\), \(y_i\), \(x_i^2\), \(y_i^2\) and \(x_i\cdot y_i\), and add them up."),
       L(r"Mitjanes: \(\bar x=\dfrac{\sum x_i}{N}\), \(\ \bar y=\dfrac{\sum y_i}{N}\).", r"Medias: \(\bar x=\dfrac{\sum x_i}{N}\), \(\ \bar y=\dfrac{\sum y_i}{N}\).", r"Means: \(\bar x=\dfrac{\sum x_i}{N}\), \(\ \bar y=\dfrac{\sum y_i}{N}\)."),
       L(r"Desviacions típiques: \(\sigma_x=\sqrt{\dfrac{\sum x_i^2}{N}-\bar x^{\,2}}\), \(\ \sigma_y=\sqrt{\dfrac{\sum y_i^2}{N}-\bar y^{\,2}}\).", r"Desviaciones típicas: \(\sigma_x=\sqrt{\dfrac{\sum x_i^2}{N}-\bar x^{\,2}}\), \(\ \sigma_y=\sqrt{\dfrac{\sum y_i^2}{N}-\bar y^{\,2}}\).", r"Standard deviations: \(\sigma_x=\sqrt{\dfrac{\sum x_i^2}{N}-\bar x^{\,2}}\), \(\ \sigma_y=\sqrt{\dfrac{\sum y_i^2}{N}-\bar y^{\,2}}\)."),
       L(r"Covariància: \(\sigma_{xy}=\dfrac{\sum x_i\cdot y_i}{N}-\bar x\cdot\bar y\).", r"Covarianza: \(\sigma_{xy}=\dfrac{\sum x_i\cdot y_i}{N}-\bar x\cdot\bar y\).", r"Covariance: \(\sigma_{xy}=\dfrac{\sum x_i\cdot y_i}{N}-\bar x\cdot\bar y\)."),
       L(r"Coeficient de correlació:", r"Coeficiente de correlación:", r"Correlation coefficient:") + D(r"r=\frac{\sigma_{xy}}{\sigma_x\cdot\sigma_y}"))
  + box('ex', L("Exemple: hores d'estudi i nota de 5 alumnes", 'Ejemplo: horas de estudio y nota de 5 alumnos', 'Example: study hours and mark of 5 students'),
        ptab(EX, EY, L('Hores', 'Horas', 'Hours') + ' ' + M('(x_i)'), L('Nota', 'Nota', 'Mark') + ' ' + M('(y_i)'))
        + btab(EX, EY)
        + D(r"\bar x=\frac{15}{5}=3\qquad \bar y=\frac{20}{5}=4")
        + D(r"\sigma_x=\sqrt{\frac{55}{5}-3^2}=\sqrt{2}\approx1\dc 41\qquad \sigma_y=\sqrt{\frac{90}{5}-4^2}=\sqrt{2}\approx1\dc 41")
        + D(r"\sigma_{xy}=\frac{69}{5}-3\cdot4=13\dc 8-12=1\dc 8")
        + D(r"r=\frac{1\dc 8}{\sqrt2\cdot\sqrt2}=\frac{1\dc 8}{2}=\boxed{0\dc 9}")
        + P(r"\(r=0\dc 9\): correlació <strong>positiva i forta</strong>. Com més hores estudien, més bona nota solen traure.",
            r"\(r=0\dc 9\): correlación <strong>positiva y fuerte</strong>. Cuantas más horas estudian, mejor nota suelen sacar.",
            r"\(r=0\dc 9\): <strong>strong positive</strong> correlation. The more hours they study, the better the mark they tend to get.")
        + fig(nuvol(list(zip(EX, EY)), (0, 6, 1), (0, 7, 1), axes=(L('hores', 'horas', 'hours'), L('nota', 'nota', 'mark')), means=True)))
  + box('ex', L('Exemple: preu i unitats venudes', 'Ejemplo: precio y unidades vendidas', 'Example: price and units sold'),
        P(r"Una botiga ha provat cinc preus diferents (€) per a un mateix producte i ha apuntat quantes unitats ha venut en una setmana:",
          r"Una tienda ha probado cinco precios diferentes (€) para un mismo producto y ha apuntado cuántas unidades ha vendido en una semana:",
          r"A shop tried five different prices (€) for the same product and recorded how many units it sold in a week:")
        + btab(PX, PY, xl=L('Preu', 'Precio', 'Price') + ' ' + M('x_i'), yl=L('Unitats', 'Unidades', 'Units') + ' ' + M('y_i'))
        + D(r"\bar x=3\qquad \bar y=\frac{190}{5}=38\qquad \sigma_x=\sqrt{\frac{55}{5}-9}=\sqrt2\qquad \sigma_y=\sqrt{\frac{7\,636}{5}-38^2}=\sqrt{83\dc 2}\approx9\dc 12")
        + D(r"\sigma_{xy}=\frac{506}{5}-3\cdot38=101\dc 2-114=-12\dc 8\qquad r=\frac{-12\dc 8}{\sqrt2\cdot\sqrt{83\dc 2}}\approx\boxed{-0\dc 99}")
        + P(r"La covariància és negativa i \(r\) és molt pròxim a \(-1\): correlació <strong>negativa i molt forta</strong>. Com més car és el producte, menys se'n ven.",
            r"La covarianza es negativa y \(r\) está muy cerca de \(-1\): correlación <strong>negativa y muy fuerte</strong>. Cuanto más caro es el producto, menos se vende.",
            r"The covariance is negative and \(r\) is very close to \(-1\): <strong>very strong negative</strong> correlation. The dearer the product, the fewer are sold."))
  + note(r"Amb la calculadora, en el mode estadístic de <strong>dues variables</strong> (el que es diu \(y=a+bx\)), introdueix les parelles i la calculadora et dona directament \(\bar x\), \(\bar y\), \(\sigma_x\), \(\sigma_y\) i \(r\). Fes-la servir per a comprovar els teus càlculs.",
         r"Con la calculadora, en el modo estadístico de <strong>dos variables</strong> (el que se llama \(y=a+bx\)), introduce las parejas y la calculadora te da directamente \(\bar x\), \(\bar y\), \(\sigma_x\), \(\sigma_y\) y \(r\). Úsala para comprobar tus cálculos.",
         r"On a calculator, in the <strong>two-variable</strong> statistics mode (the one called \(y=a+bx\)), enter the pairs and it gives you \(\bar x\), \(\bar y\), \(\sigma_x\), \(\sigma_y\) and \(r\) directly. Use it to check your working.", '🧮'))

s4 += (widget('w-cov', '🧮', L('Coeficient de correlació pas a pas', 'Coeficiente de correlación paso a paso', 'Correlation coefficient step by step'),
              ['<p class="hint-s">' + L("Escriu les dades de X i de Y en el mateix ordre. L'eina fa la taula, calcula les mitjanes, les desviacions típiques, la covariància i r, i dibuixa el núvol.",
                                        "Escribe los datos de X y de Y en el mismo orden. La herramienta hace la tabla, calcula las medias, las desviaciones típicas, la covarianza y r, y dibuja la nube.",
                                        "Type the X and Y data in the same order. The tool builds the table, works out the means, standard deviations, covariance and r, and draws the cloud.") + '</p>',
               seg([('ex', L('Hores i nota', 'Horas y nota', 'Hours and mark')), ('pr', L('Preu i vendes', 'Precio y ventas', 'Price and sales')), ('h10', L('10 alumnes', '10 alumnos', '10 students')), ('own', L('Les meues', 'Los míos', 'My own'))]),
               '<div class="wrow">' + tin('x', 'X', '', 'w') + '</div><div class="wrow">' + tin('y', 'Y', '', 'w') + '</div>'], out='<div class="tout"></div>')
       + widget('w-guess', '🎯', L('Endevina el coeficient de correlació', 'Adivina el coeficiente de correlación', 'Guess the correlation coefficient'),
                ['<p class="hint-s">' + L("Mira el núvol i tria el valor de r que creus que té.", "Mira la nube y elige el valor de r que crees que tiene.", "Look at the cloud and pick the value of r you think it has.") + '</p>'],
                out='<div class="gout cl-wrap"><svg class="sgraf nv" viewBox="0 0 340 250" role="img" aria-label="núvol"></svg></div><div class="wrow dopts gopts"></div><div class="wrow"><button class="btn" type="button" data-a="new">↻ ' + L("Un altre núvol", "Otra nube", "Another cloud") + '</button><span class="dscore"></span></div>')
       + drill('cov', 'Entrena: calcula la covariància', 'Entrena: calcula la covarianza', 'Train: find the covariance')
       + drill('rcalc', 'Entrena: calcula el coeficient de correlació', 'Entrena: calcula el coeficiente de correlación', 'Train: find the correlation coefficient')
       + drill('rint', 'Entrena: què indica el coeficient de correlació?', 'Entrena: ¿qué indica el coeficiente de correlación?', 'Train: what does the correlation coefficient tell you?', 'opts'))

# problemes 10.4
ck(Fr(210, 8) - 4 * 6, '2.25'); ck(Fr(9, 4) / 6, '0.375')
DX = [2, 3, 5, 6, 9]; DY = [8, 8, 6, 4, 2]; SD = bi(DX, DY)
assert (SD['sx2'], SD['sy2'], SD['sxy'], SD['mx'], SD['my'], SD['vx'], SD['vy'], SD['c']) == (155, 184, 112, 5, Fr(28, 5), 6, Fr(136, 25), Fr(-28, 5))
ckr(SD['sdx'], '2.45'); ckr(SD['sdy'], '2.33'); ckr(SD['r'], '-0.98')
assert (SH['sx2'], SH['sy2'], SH['sxy'], SH['vx'], SH['vy'], SH['c']) == (178, 389, 259, Fr(84, 25), Fr(409, 100), Fr(87, 25))
ckr(SH['sdx'], '1.83'); ckr(SH['sdy'], '2.02'); ckr(SH['r'], '0.94')
FX_ = [1, 2, 3, 4, 5]; FY_ = [3, 5, 7, 9, 11]; SF = bi(FX_, FY_); assert (SF['vx'], SF['vy'], SF['c']) == (2, 8, 4) and abs(SF['r'] - 1) < 1e-12
s4 += levels(
 [prob(L(r"Digues quin tipus de correlació indica cada valor de \(r\): a) \(0\dc 92\); b) \(-0\dc 15\); c) \(-0\dc 78\); d) \(0\dc 45\); e) \(-1\).",
         r"Di qué tipo de correlación indica cada valor de \(r\): a) \(0\dc 92\); b) \(-0\dc 15\); c) \(-0\dc 78\); d) \(0\dc 45\); e) \(-1\).",
         r"Say what kind of correlation each value of \(r\) shows: a) \(0\dc 92\); b) \(-0\dc 15\); c) \(-0\dc 78\); d) \(0\dc 45\); e) \(-1\)."),
       P(r"a) Positiva i forta. &nbsp; b) Quasi nul·la (negativa molt feble). &nbsp; c) Negativa moderada (quasi forta). &nbsp; d) Positiva feble. &nbsp; e) Negativa perfecta: relació funcional, tots els punts estan en una recta que baixa.",
         r"a) Positiva y fuerte. &nbsp; b) Casi nula (negativa muy débil). &nbsp; c) Negativa moderada (casi fuerte). &nbsp; d) Positiva débil. &nbsp; e) Negativa perfecta: relación funcional, todos los puntos están en una recta que baja.",
         r"a) Strong positive. &nbsp; b) Almost zero (very weak negative). &nbsp; c) Moderate negative (almost strong). &nbsp; d) Weak positive. &nbsp; e) Perfect negative: a functional relationship, all the points lie on a falling line.")),
  prob(L(r"D'una distribució bidimensional amb \(N=8\) parelles sabem que \(\bar x=4\), \(\bar y=6\), \(\sigma_x=2\), \(\sigma_y=3\) i \(\sum x_i y_i=210\). Calcula la covariància i el coeficient de correlació. Com és la correlació?",
         r"De una distribución bidimensional con \(N=8\) parejas sabemos que \(\bar x=4\), \(\bar y=6\), \(\sigma_x=2\), \(\sigma_y=3\) y \(\sum x_i y_i=210\). Calcula la covarianza y el coeficiente de correlación. ¿Cómo es la correlación?",
         r"For a bivariate distribution with \(N=8\) pairs we know \(\bar x=4\), \(\bar y=6\), \(\sigma_x=2\), \(\sigma_y=3\) and \(\sum x_i y_i=210\). Find the covariance and the correlation coefficient. What is the correlation like?"),
       D(r"\sigma_{xy}=\frac{210}{8}-4\cdot6=26\dc 25-24=\boxed{2\dc 25}\qquad r=\frac{2\dc 25}{2\cdot3}=\boxed{0\dc 375}"),
       P(r"Correlació <strong>positiva i feble</strong>.", r"Correlación <strong>positiva y débil</strong>.", r"<strong>Weak positive</strong> correlation."))],
 [prob(L(r"Calcula el coeficient de correlació d'aquesta distribució i interpreta'l:", r"Calcula el coeficiente de correlación de esta distribución e interprétalo:", r"Find the correlation coefficient of this distribution and interpret it:") + ptab(DX, DY, M('x_i'), M('y_i')),
       btab(DX, DY),
       D(r"\bar x=\frac{25}{5}=5\qquad \bar y=\frac{28}{5}=5\dc 6\qquad \sigma_x=\sqrt{\frac{155}{5}-5^2}=\sqrt6\approx2\dc 45\qquad \sigma_y=\sqrt{\frac{184}{5}-5\dc 6^2}=\sqrt{5\dc 44}\approx2\dc 33"),
       D(r"\sigma_{xy}=\frac{112}{5}-5\cdot5\dc 6=22\dc 4-28=-5\dc 6\qquad r=\frac{-5\dc 6}{\sqrt6\cdot\sqrt{5\dc 44}}\approx\boxed{-0\dc 98}"),
       P(r"Correlació <strong>negativa i molt forta</strong>: els punts estan quasi en una recta que baixa.", r"Correlación <strong>negativa y muy fuerte</strong>: los puntos están casi en una recta que baja.", r"<strong>Very strong negative</strong> correlation: the points are almost on a falling line.")),
  prob(L(r"Calcula el coeficient de correlació de les hores d'estudi i les notes dels 10 alumnes de l'apartat 10.1. Coincideix amb el que deies mirant el núvol?",
         r"Calcula el coeficiente de correlación de las horas de estudio y las notas de los 10 alumnos del apartado 10.1. ¿Coincide con lo que decías mirando la nube?",
         r"Find the correlation coefficient of the study hours and marks of the 10 students in section 10.1. Does it match what you said from the scatter plot?"),
       btab(HX, HY),
       D(r"\bar x=3\dc 8\qquad \bar y=5\dc 9\qquad \sigma_x=\sqrt{\frac{178}{10}-3\dc 8^2}=\sqrt{3\dc 36}\approx1\dc 83\qquad \sigma_y=\sqrt{\frac{389}{10}-5\dc 9^2}=\sqrt{4\dc 09}\approx2\dc 02"),
       D(r"\sigma_{xy}=\frac{259}{10}-3\dc 8\cdot5\dc 9=25\dc 9-22\dc 42=3\dc 48\qquad r=\frac{3\dc 48}{1\dc 83\ldots\cdot2\dc 02\ldots}\approx\boxed{0\dc 94}"),
       P(r"Sí: correlació <strong>positiva i forta</strong>, com ja es veia en el núvol.", r"Sí: correlación <strong>positiva y fuerte</strong>, como ya se veía en la nube.", r"Yes: <strong>strong positive</strong> correlation, as the scatter plot already suggested."))],
 [prob(L(r"Calcula \(r\) per a les parelles \((1,3),\ (2,5),\ (3,7),\ (4,9),\ (5,11)\). Per què dona aquest resultat?", r"Calcula \(r\) para las parejas \((1,3),\ (2,5),\ (3,7),\ (4,9),\ (5,11)\). ¿Por qué da este resultado?", r"Find \(r\) for the pairs \((1,3),\ (2,5),\ (3,7),\ (4,9),\ (5,11)\). Why do you get this result?"),
       D(r"\bar x=3\qquad \bar y=7\qquad \sigma_x^2=\frac{55}{5}-9=2\qquad \sigma_y^2=\frac{285}{5}-49=8\qquad \sigma_{xy}=\frac{125}{5}-3\cdot7=4"),
       D(r"r=\frac{4}{\sqrt2\cdot\sqrt8}=\frac{4}{\sqrt{16}}=\frac44=\boxed{1}"),
       P(r"Totes les parelles compleixen \(y=2x+1\): estan <strong>exactament</strong> en una recta que puja. És una relació funcional i per això \(r=1\).",
         r"Todas las parejas cumplen \(y=2x+1\): están <strong>exactamente</strong> en una recta que sube. Es una relación funcional y por eso \(r=1\).",
         r"Every pair satisfies \(y=2x+1\): they lie <strong>exactly</strong> on a rising line. It's a functional relationship, which is why \(r=1\).")),
  prob(L(r"Un alumne ha calculat el coeficient de correlació entre l'edat i l'alçada d'uns xiquets i li ha eixit \(r=1\dc 3\). Què li diries?",
         r"Un alumno ha calculado el coeficiente de correlación entre la edad y la altura de unos niños y le ha salido \(r=1\dc 3\). ¿Qué le dirías?",
         r"A student worked out the correlation coefficient between some children's age and height and got \(r=1\dc 3\). What would you tell them?"),
       P(r"Que s'ha equivocat: \(r\) <strong>sempre</strong> està entre \(-1\) i \(1\). Ha de repassar els càlculs (sovint l'error és oblidar l'arrel quadrada de les variàncies, o restar \(\bar x\cdot\bar y\)).",
         r"Que se ha equivocado: \(r\) <strong>siempre</strong> está entre \(-1\) y \(1\). Tiene que repasar los cálculos (a menudo el error es olvidar la raíz cuadrada de las varianzas, o restar \(\bar x\cdot\bar y\)).",
         r"That they've made a mistake: \(r\) is <strong>always</strong> between \(-1\) and \(1\). They should check the working (the usual slip is forgetting the square root of the variances, or forgetting to subtract \(\bar x\cdot\bar y\))."))])
QX = [1, 2, 4, 5, 8]; QY = [3, 5, 4, 7, 6]; SQ = bi(QX, QY); assert (SQ['mx'], SQ['my'], SQ['vx'], SQ['vy'], SQ['c']) == (4, 5, 6, 2, Fr(12, 5)); ckr(SQ['r'], '0.69')
s4 += practice([('★★☆', L(r"Calcula el coeficient de correlació de \((1,3),\ (2,5),\ (4,4),\ (5,7),\ (8,6)\) i interpreta'l.", r"Calcula el coeficiente de correlación de \((1,3),\ (2,5),\ (4,4),\ (5,7),\ (8,6)\) e interprétalo.", r"Find the correlation coefficient of \((1,3),\ (2,5),\ (4,4),\ (5,7),\ (8,6)\) and interpret it.")),
                ('★★☆', L(r"Què és més fort, una correlació amb \(r=-0\dc 85\) o una amb \(r=0\dc 7\)?", r"¿Qué es más fuerte, una correlación con \(r=-0\dc 85\) o una con \(r=0\dc 7\)?", r"Which is stronger, a correlation with \(r=-0\dc 85\) or one with \(r=0\dc 7\)?"))],
               L(r"1) \(\bar x=4\), \(\bar y=5\), \(\sigma_x=\sqrt6\), \(\sigma_y=\sqrt2\), \(\sigma_{xy}=\frac{112}{5}-20=2\dc 4\); \(r=\frac{2\dc 4}{\sqrt6\cdot\sqrt2}\approx0\dc 69\): positiva moderada. &nbsp; 2) La de \(r=-0\dc 85\), perquè \(|-0\dc 85|>0\dc 7\).",
                 r"1) \(\bar x=4\), \(\bar y=5\), \(\sigma_x=\sqrt6\), \(\sigma_y=\sqrt2\), \(\sigma_{xy}=\frac{112}{5}-20=2\dc 4\); \(r=\frac{2\dc 4}{\sqrt6\cdot\sqrt2}\approx0\dc 69\): positiva moderada. &nbsp; 2) La de \(r=-0\dc 85\), porque \(|-0\dc 85|>0\dc 7\).",
                 r"1) \(\bar x=4\), \(\bar y=5\), \(\sigma_x=\sqrt6\), \(\sigma_y=\sqrt2\), \(\sigma_{xy}=\frac{112}{5}-20=2\dc 4\); \(r=\frac{2\dc 4}{\sqrt6\cdot\sqrt2}\approx0\dc 69\): moderate positive. &nbsp; 2) The one with \(r=-0\dc 85\), because \(|-0\dc 85|>0\dc 7\)."))
ck(SQ['sxy'], 112)
