# Apartat 9.6 dels apunts de la Unitat 9 de 4t ESO Matemàtiques A (Estadística): paràmetres de dispersió (rang,
# desviació mitjana, variància, desviació típica i coeficient de variació). El principi (Anna i Bea, rang i DM) és el
# 10.8 de ../1eso-t10/s789.py; la variància, la desviació típica i el coeficient de variació són nous.
import math
from comu import *
from s123 import TG, DIN

def dtab(data, sq=True):
    """taula amb xi, xi − x̄, |xi − x̄| i (xi − x̄)² (i la fila de totals)"""
    m = mean(data)
    rows = [[M(tn(x)), M(tn(x - m)), M(tn(abs(x - m)))] + ([M(tn((x - m) ** 2))] if sq else []) for x in data]
    rows.append(['<strong>Total</strong>', '', M(r'\textstyle\sum=%s' % tn(sum(abs(x - m) for x in data)))] + ([M(r'\textstyle\sum=%s' % tn(sum((x - m) ** 2 for x in data)))] if sq else []))
    return tbl([M('x_i'), M(r'x_i-\bar x'), M(r'|x_i-\bar x|')] + ([M(r'(x_i-\bar x)^2')] if sq else []), rows, 'c freq')
def vtab(tab, xl=None):
    """taula amb xi, fi, xi·fi i xi²·fi (i la fila de totals)"""
    N = sum(f for _, f in tab); S = sum(x * f for x, f in tab); S2 = sum(x * x * f for x, f in tab)
    rows = [[M(tn(x)), M(str(f)), M(tn(x * f)), M(tn(x * x * f))] for x, f in tab]
    rows.append(['<strong>Total</strong>', M('N=%d' % N), M(r'\textstyle\sum=%s' % tn(S)), M(r'\textstyle\sum=%s' % tn(S2))])
    return tbl([xl or M('x_i'), M('f_i'), M(r'x_i\cdot f_i'), M(r'x_i^2\cdot f_i')], rows, 'c freq')
def tstats(tab):
    N = sum(f for _, f in tab); m = Fr(sum(x * f for x, f in tab), N); v = Fr(sum(x * x * f for x, f in tab), N) - m * m
    return N, m, v, math.sqrt(v)

# =====================================================================
# 9.6 Paràmetres de dispersió
# =====================================================================
ANNA = [8, 9, 10, 11, 12]; BEA = [2, 6, 10, 14, 18]
assert mean(ANNA) == mean(BEA) == 10 and rang(ANNA) == 4 and rang(BEA) == 16 and dm(ANNA) == Fr(6, 5) and dm(BEA) == Fr(24, 5)
assert var(ANNA) == 2 and var(BEA) == 32
ckr(sd(ANNA), '1.41'); ckr(sd(BEA), '5.66'); ckr(100 * cv(ANNA), '14.1', 1); ckr(100 * cv(BEA), '56.6', 1)
F_AB = figs(fig(dots(ANNA, 0, 20, mean_=10, dev=True, step=2), 'Anna'), fig(dots(BEA, 0, 20, mean_=10, dev=True, step=2), 'Bea'))
s6 = box('def', L('Paràmetres de dispersió', 'Parámetros de dispersión', 'Measures of spread'),
  P(r"Dos grups de dades poden tindre la mateixa mitjana i ser molt diferents. Els punts que han fet Anna i Bea en cinc partits de bàsquet són:",
    r"Dos grupos de datos pueden tener la misma media y ser muy diferentes. Los puntos que han hecho Anna y Bea en cinco partidos de baloncesto son:",
    r"Two sets of data can have the same mean and still be very different. The points Anna and Bea scored in five basketball games are:")
  + D(r"\text{Anna: }8,\ 9,\ 10,\ 11,\ 12\qquad \text{Bea: }2,\ 6,\ 10,\ 14,\ 18")
  + P(r"Totes dues fan una mitjana de 10 punts, però Anna és molt més <strong>regular</strong>. Els <strong>paràmetres de dispersió</strong> mesuren com d'<strong>escampades</strong> estan les dades respecte de la mitjana:",
      r"Las dos hacen una media de 10 puntos, pero Anna es mucho más <strong>regular</strong>. Los <strong>parámetros de dispersión</strong> miden lo <strong>esparcidos</strong> que están los datos respecto de la media:",
      r"Both average 10 points, but Anna is much more <strong>consistent</strong>. <strong>Measures of spread</strong> tell us how <strong>spread out</strong> the data are around the mean:")
  + ul(L(r"El <strong>rang</strong> (o recorregut) és la diferència entre la dada més gran i la més xicoteta: \(\text{rang}=x_{\max}-x_{\min}\). És molt fàcil de calcular, però només depén de dues dades.",
         r"El <strong>rango</strong> (o recorrido) es la diferencia entre el dato mayor y el menor: \(\text{rango}=x_{\max}-x_{\min}\). Es muy fácil de calcular, pero solo depende de dos datos.",
         r"The <strong>range</strong> is the difference between the largest and smallest values: \(\text{range}=x_{\max}-x_{\min}\). It's very easy to work out, but it only depends on two values."),
       L(r"La <strong>desviació mitjana</strong> (\(DM\)) és la mitjana de les <strong>distàncies</strong> de cada dada a la mitjana: \(DM=\dfrac{\sum|x_i-\bar x|\cdot f_i}{N}\).",
         r"La <strong>desviación media</strong> (\(DM\)) es la media de las <strong>distancias</strong> de cada dato a la media: \(DM=\dfrac{\sum|x_i-\bar x|\cdot f_i}{N}\).",
         r"The <strong>mean deviation</strong> (\(MD\)) is the mean of the <strong>distances</strong> from each value to the mean: \(MD=\dfrac{\sum|x_i-\bar x|\cdot f_i}{N}\)."),
       L(r"La <strong>variància</strong> (\(\sigma^2\)) és la mitjana dels <strong>quadrats</strong> de les desviacions: \(\sigma^2=\dfrac{\sum(x_i-\bar x)^2\cdot f_i}{N}\). En elevar al quadrat, totes les desviacions són positives i les grans pesen més.",
         r"La <strong>varianza</strong> (\(\sigma^2\)) es la media de los <strong>cuadrados</strong> de las desviaciones: \(\sigma^2=\dfrac{\sum(x_i-\bar x)^2\cdot f_i}{N}\). Al elevar al cuadrado, todas las desviaciones son positivas y las grandes pesan más.",
         r"The <strong>variance</strong> (\(\sigma^2\)) is the mean of the <strong>squares</strong> of the deviations: \(\sigma^2=\dfrac{\sum(x_i-\bar x)^2\cdot f_i}{N}\). Squaring makes every deviation positive and gives more weight to the big ones."),
       L(r"La <strong>desviació típica</strong> (\(\sigma\)) és l'arrel quadrada de la variància: \(\sigma=\sqrt{\sigma^2}\). Té les <strong>mateixes unitats</strong> que les dades, i per això és el paràmetre de dispersió que més es fa servir.",
         r"La <strong>desviación típica</strong> (\(\sigma\)) es la raíz cuadrada de la varianza: \(\sigma=\sqrt{\sigma^2}\). Tiene las <strong>mismas unidades</strong> que los datos, y por eso es el parámetro de dispersión que más se usa.",
         r"The <strong>standard deviation</strong> (\(\sigma\)) is the square root of the variance: \(\sigma=\sqrt{\sigma^2}\). It has the <strong>same units</strong> as the data, which is why it's the most widely used measure of spread."))
  + P(r"Com <strong>més grans</strong> són aquests paràmetres, <strong>més escampades</strong> estan les dades i menys representativa és la mitjana. Si totes les dades són iguals, tots valen 0.",
      r"Cuanto <strong>mayores</strong> son estos parámetros, <strong>más esparcidos</strong> están los datos y menos representativa es la media. Si todos los datos son iguales, todos valen 0.",
      r"The <strong>larger</strong> these measures, the <strong>more spread out</strong> the data are and the less representative the mean is. If all the values are equal, they're all 0."))
s6 += box('ex', L('Exemple: Anna i Bea', 'Ejemplo: Anna y Bea', 'Example: Anna and Bea'),
  '<div class="tv2">' + dtab(ANNA) + dtab(BEA) + '</div>'
  + ul(L(r"Anna: rang \(=12-8=4\); \(DM=\dfrac{6}{5}=1\dc 2\); \(\sigma^2=\dfrac{10}{5}=2\); \(\sigma=\sqrt2\approx1\dc 41\) punts.", r"Anna: rango \(=12-8=4\); \(DM=\dfrac{6}{5}=1\dc 2\); \(\sigma^2=\dfrac{10}{5}=2\); \(\sigma=\sqrt2\approx1\dc 41\) puntos.", r"Anna: range \(=12-8=4\); \(MD=\dfrac{6}{5}=1\dc 2\); \(\sigma^2=\dfrac{10}{5}=2\); \(\sigma=\sqrt2\approx1\dc 41\) points."),
       L(r"Bea: rang \(=18-2=16\); \(DM=\dfrac{24}{5}=4\dc 8\); \(\sigma^2=\dfrac{160}{5}=32\); \(\sigma=\sqrt{32}\approx5\dc 66\) punts.", r"Bea: rango \(=18-2=16\); \(DM=\dfrac{24}{5}=4\dc 8\); \(\sigma^2=\dfrac{160}{5}=32\); \(\sigma=\sqrt{32}\approx5\dc 66\) puntos.", r"Bea: range \(=18-2=16\); \(MD=\dfrac{24}{5}=4\dc 8\); \(\sigma^2=\dfrac{160}{5}=32\); \(\sigma=\sqrt{32}\approx5\dc 66\) points."))
  + F_AB
  + P(r"Tots els paràmetres diuen el mateix: les dades de Bea estan molt més escampades. Anna és més regular.",
      r"Todos los parámetros dicen lo mismo: los datos de Bea están mucho más esparcidos. Anna es más regular.",
      r"All the measures say the same thing: Bea's values are much more spread out. Anna is more consistent."))

# fórmula còmoda amb una taula: els germans de 9.2
NG_, MG, VG, SG = tstats(TG)
assert (NG_, MG, VG) == (20, Fr(29, 20), Fr(419, 400)); ck(sum(x * x * f for x, f in TG), 63)
ckr(SG, '1.02'); ckr(100 * SG / float(MG), '70.6', 1)
s6 += box('prop', L('Variància amb una taula de freqüències', 'Varianza con una tabla de frecuencias', 'Variance from a frequency table'),
  P(r"Restar la mitjana a cada dada és pesat quan la mitjana no és entera. Desenvolupant el quadrat s'arriba a una fórmula equivalent, molt més còmoda:",
    r"Restar la media a cada dato es pesado cuando la media no es entera. Desarrollando el cuadrado se llega a una fórmula equivalente, mucho más cómoda:",
    r"Subtracting the mean from every value is tedious when the mean isn't a whole number. Expanding the square gives an equivalent formula that's much easier to use:")
  + D(r"\sigma^2=\frac{\sum x_i^2\cdot f_i}{N}-\bar x^{\,2}")
  + P(r"És a dir: la <strong>mitjana dels quadrats</strong> menys el <strong>quadrat de la mitjana</strong>. A la taula hi afegim dues columnes, \(x_i\cdot f_i\) i \(x_i^2\cdot f_i\) (que és \(x_i\cdot(x_i\cdot f_i)\)).",
      r"Es decir: la <strong>media de los cuadrados</strong> menos el <strong>cuadrado de la media</strong>. En la tabla añadimos dos columnas, \(x_i\cdot f_i\) y \(x_i^2\cdot f_i\) (que es \(x_i\cdot(x_i\cdot f_i)\)).",
      r"That is: the <strong>mean of the squares</strong> minus the <strong>square of the mean</strong>. We add two columns to the table, \(x_i\cdot f_i\) and \(x_i^2\cdot f_i\) (which is \(x_i\cdot(x_i\cdot f_i)\)).")
  + box('ex', L('Exemple: nombre de germans de 20 alumnes (apartat 9.2)', 'Ejemplo: número de hermanos de 20 alumnos (apartado 9.2)', 'Example: number of siblings of 20 students (section 9.2)'),
        vtab(TG)
        + D(r"\bar x=\frac{29}{20}=1\dc 45\qquad \sigma^2=\frac{63}{20}-1\dc 45^2=3\dc 15-2\dc 1025=1\dc 0475\qquad \sigma=\sqrt{1\dc 0475}\approx1\dc 02\ \tri{germans}{hermanos}{siblings}"))
  + note(r"Compte amb l'ordre: primer divideix \(\sum x_i^2 f_i\) entre \(N\) i <strong>després</strong> resta \(\bar x^{\,2}\). Si et dona una variància negativa, t'has equivocat!",
         r"Cuidado con el orden: primero divide \(\sum x_i^2 f_i\) entre \(N\) y <strong>después</strong> resta \(\bar x^{\,2}\). Si te sale una varianza negativa, ¡te has equivocado!",
         r"Mind the order: first divide \(\sum x_i^2 f_i\) by \(N\) and <strong>then</strong> subtract \(\bar x^{\,2}\). If you get a negative variance, you've made a mistake!", '⚠️')
  + note(r"Amb la calculadora (mode estadístic), la desviació típica que fem servir és la que es diu \(\sigma_x\) (o \(\sigma_n\)). La \(s_x\) (o \(\sigma_{n-1}\)) divideix entre \(N-1\) i es fa servir en cursos posteriors.",
         r"Con la calculadora (modo estadístico), la desviación típica que usamos es la que se llama \(\sigma_x\) (o \(\sigma_n\)). La \(s_x\) (o \(\sigma_{n-1}\)) divide entre \(N-1\) y se usa en cursos posteriores.",
         r"On a calculator (statistics mode), the standard deviation we use is the one called \(\sigma_x\) (or \(\sigma_n\)). \(s_x\) (or \(\sigma_{n-1}\)) divides by \(N-1\) and is used in later courses.", '🧮'))

# coeficient de variació
ck(Fr(4, 10) * 100, 40)
ckr(Fr(4, 32) * 100, '12.5', 1); ckr(Fr(8, 70) * 100, '11.4', 1)
s6 += box('def', L('Coeficient de variació', 'Coeficiente de variación', 'Coefficient of variation'),
  P(r"La desviació típica depén de les unitats i de la grandària de les dades: 4 kg de dispersió és molt per a nadons i poc per a elefants. Per a <strong>comparar la dispersió</strong> de dos grups amb mitjanes molt diferents (o amb unitats diferents) fem servir el <strong>coeficient de variació</strong>:",
    r"La desviación típica depende de las unidades y del tamaño de los datos: 4 kg de dispersión es mucho para bebés y poco para elefantes. Para <strong>comparar la dispersión</strong> de dos grupos con medias muy diferentes (o con unidades diferentes) usamos el <strong>coeficiente de variación</strong>:",
    r"The standard deviation depends on the units and on how big the data are: a spread of 4 kg is a lot for babies and very little for elephants. To <strong>compare the spread</strong> of two groups with very different means (or different units) we use the <strong>coefficient of variation</strong>:")
  + D(r"CV=\frac{\sigma}{\bar x}\qquad \tri{(sovint en percentatge: }{(a menudo en porcentaje: }{(often as a percentage: }CV\cdot100\ \%)")
  + P(r"No té unitats. Com <strong>més xicotet</strong> és el \(CV\), <strong>més agrupades</strong> estan les dades al voltant de la mitjana (i més representativa és la mitjana).",
      r"No tiene unidades. Cuanto <strong>más pequeño</strong> es el \(CV\), <strong>más agrupados</strong> están los datos alrededor de la media (y más representativa es la media).",
      r"It has no units. The <strong>smaller</strong> the \(CV\), the <strong>more tightly grouped</strong> the data are around the mean (and the more representative the mean is).")
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"El pes dels nadons d'un hospital té \(\bar x=3\dc 2\) kg i \(\sigma=0\dc 4\) kg; el de les persones adultes d'una empresa, \(\bar x=70\) kg i \(\sigma=8\) kg. Quin grup té més dispersió?",
          r"El peso de los bebés de un hospital tiene \(\bar x=3\dc 2\) kg y \(\sigma=0\dc 4\) kg; el de las personas adultas de una empresa, \(\bar x=70\) kg y \(\sigma=8\) kg. ¿Qué grupo tiene más dispersión?",
          r"The weight of the babies in a hospital has \(\bar x=3\dc 2\) kg and \(\sigma=0\dc 4\) kg; that of the adults in a company, \(\bar x=70\) kg and \(\sigma=8\) kg. Which group is more spread out?")
        + D(r"CV_{\tri{nadons}{bebés}{babies}}=\frac{0\dc 4}{3\dc 2}=0\dc 125\to12\dc 5\ \%\qquad CV_{\tri{adults}{adultos}{adults}}=\frac{8}{70}\approx0\dc 114\to11\dc 4\ \%")
        + P(r"Encara que la \(\sigma\) dels adults és 20 vegades més gran, en proporció a la seua mitjana els nadons tenen una dispersió <strong>una mica més gran</strong>.",
            r"Aunque la \(\sigma\) de los adultos es 20 veces mayor, en proporción a su media los bebés tienen una dispersión <strong>un poco mayor</strong>.",
            r"Although the adults' \(\sigma\) is 20 times bigger, relative to their mean the babies have a <strong>slightly larger</strong> spread.")))
ck(Fr(8, Fr(4, 10)), 20)

s6 += (widget('w-var', '🧮', L('Variància i desviació típica pas a pas', 'Varianza y desviación típica paso a paso', 'Variance and standard deviation step by step'),
              ['<p class="hint-s">' + L("Escriu els valors (o les marques de classe) i les seues freqüències. L'eina fa les columnes <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub> i <i>x</i><sub>i</sub><sup>2</sup>·<i>f</i><sub>i</sub> i calcula la mitjana, σ², σ i el CV.",
                                        "Escribe los valores (o las marcas de clase) y sus frecuencias. La herramienta hace las columnas <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub> y <i>x</i><sub>i</sub><sup>2</sup>·<i>f</i><sub>i</sub> y calcula la media, σ², σ y el CV.",
                                        "Type the values (or class marks) and their frequencies. The tool builds the <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub> and <i>x</i><sub>i</sub><sup>2</sup>·<i>f</i><sub>i</sub> columns and works out the mean, σ², σ and the CV.") + '</p>',
               seg([('germ', L('Germans', 'Hermanos', 'Siblings')), ('din', L('Diners (marques)', 'Dinero (marcas)', 'Money (marks)')), ('own', L('Els meus', 'Los míos', 'My own'))]),
               '<div class="wrow">' + tin('x', '<i>x</i><sub>i</sub>', '', 'w') + '</div><div class="wrow">' + tin('f', '<i>f</i><sub>i</sub>', '', 'w') + '</div>'], out='<div class="tout"></div>')
       + widget('w-disp', '↔️', L('Compara la dispersió de dos grups', 'Compara la dispersión de dos grupos', 'Compare the spread of two sets'),
                ['<p class="hint-s">' + L("Escriu dos grups de dades: l'eina dibuixa la distància de cada dada a la mitjana i calcula el rang, la desviació mitjana, la desviació típica i el coeficient de variació.", "Escribe dos grupos de datos: la herramienta dibuja la distancia de cada dato a la media y calcula el rango, la desviación media, la desviación típica y el coeficiente de variación.", "Type two sets of data: the tool draws each value's distance to the mean and works out the range, mean deviation, standard deviation and coefficient of variation.") + '</p>',
                 '<div class="wrow">' + tin('a', 'A', '8 9 10 11 12', 'w') + '</div><div class="wrow">' + tin('b', 'B', '2 6 10 14 18', 'w') + '</div>'], out='<div class="tout"></div>')
       + drill('rang', 'Entrena: calcula el rang', 'Entrena: calcula el rango', 'Train: find the range')
       + drill('dm', 'Entrena: calcula la desviació mitjana', 'Entrena: calcula la desviación media', 'Train: find the mean deviation')
       + drill('var', 'Entrena: calcula la variància i la desviació típica', 'Entrena: calcula la varianza y la desviación típica', 'Train: find the variance and standard deviation')
       + drill('cv', 'Entrena: el coeficient de variació', 'Entrena: el coeficiente de variación', 'Train: the coefficient of variation'))

TMP = [-2, 5, 3, -4, 1, 6, 0]
assert rang(TMP) == 10
D82 = [4, 7, 8, 10, 11]; assert mean(D82) == 8 and dm(D82) == 2 and var(D82) == 6; ckr(sd(D82), '2.45')
ARA = [7, 8, 8, 9, 8]; ARB = [10, 6, 9, 5, 10]
assert mean(ARA) == mean(ARB) == 8 and var(ARA) == Fr(2, 5) and var(ARB) == Fr(22, 5) and rang(ARA) == 2 and rang(ARB) == 5
ckr(sd(ARA), '0.63'); ckr(sd(ARB), '2.10')
GOLT = [(0, 2), (1, 5), (2, 5), (3, 2), (4, 1)]
NGo, MGo, VGo, SGo = tstats(GOLT); assert (NGo, MGo, VGo) == (15, Fr(5, 3), Fr(52, 45)); ck(sum(x * x * f for x, f in GOLT), 59)
ckr(MGo, '1.67'); ckr(Fr(59, 15), '3.93'); ckr(VGo, '1.16'); ckr(SGo, '1.07'); ckr(100 * SGo / float(MGo), '64.5', 1)
DM_ = [(Fr(a + b, 2), f) for a, b, f in DIN]
NDi, MDi, VDi, SDi = tstats(DM_); assert (NDi, MDi, VDi) == (40, Fr(47, 4), Fr(571, 16)); ck(sum(x * x * f for x, f in DM_), 6950)
ckr(SDi, '5.97'); ckr(100 * SDi / float(MDi), '50.8', 1)
ckr(Fr(6, 198) * 100, '3.0', 1); ckr(Fr(5, 110) * 100, '4.5', 1)
s6 += levels(
 [prob(L(r"Les temperatures mínimes d'una setmana d'hivern han sigut \(-2,\ 5,\ 3,\ -4,\ 1,\ 6,\ 0\) °C. Calcula el rang.",
         r"Las temperaturas mínimas de una semana de invierno han sido \(-2,\ 5,\ 3,\ -4,\ 1,\ 6,\ 0\) °C. Calcula el rango.",
         r"The minimum temperatures of a winter week were \(-2,\ 5,\ 3,\ -4,\ 1,\ 6,\ 0\) °C. Find the range."),
       D(r"\text{\tri{rang}{rango}{range}}=6-(-4)=6+4=\boxed{10\ ^\circ\text{C}}")),
  prob(L(r"Calcula la desviació mitjana, la variància i la desviació típica de les dades \(4,\ 7,\ 8,\ 10,\ 11\).", r"Calcula la desviación media, la varianza y la desviación típica de los datos \(4,\ 7,\ 8,\ 10,\ 11\).", r"Find the mean deviation, the variance and the standard deviation of the data \(4,\ 7,\ 8,\ 10,\ 11\)."),
       D(r"\bar x=\frac{40}{5}=8"),
       dtab(D82) + D(r"DM=\frac{10}{5}=\boxed{2}\qquad \sigma^2=\frac{30}{5}=\boxed{6}\qquad \sigma=\sqrt6\approx\boxed{2\dc 45}"))],
 [prob(L(r"Dos arquers han fet aquestes puntuacions en cinc tirades. A: \(7,\ 8,\ 8,\ 9,\ 8\); B: \(10,\ 6,\ 9,\ 5,\ 10\). Calcula la mitjana, el rang i la desviació típica de cadascun. Qui és més regular?",
         r"Dos arqueros han hecho estas puntuaciones en cinco tiradas. A: \(7,\ 8,\ 8,\ 9,\ 8\); B: \(10,\ 6,\ 9,\ 5,\ 10\). Calcula la media, el rango y la desviación típica de cada uno. ¿Quién es más regular?",
         r"Two archers scored these points in five shots. A: \(7,\ 8,\ 8,\ 9,\ 8\); B: \(10,\ 6,\ 9,\ 5,\ 10\). Find each one's mean, range and standard deviation. Who is more consistent?"),
       D(r"\bar x_A=\frac{40}{5}=8\qquad \bar x_B=\frac{40}{5}=8"),
       '<div class="tv2">' + dtab(ARA) + dtab(ARB) + '</div>',
       P(r"A: rang \(9-7=2\), \(\sigma^2=\frac{2}{5}=0\dc 4\), \(\sigma\approx0\dc 63\). &nbsp; B: rang \(10-5=5\), \(\sigma^2=\frac{22}{5}=4\dc 4\), \(\sigma\approx2\dc 10\). Tenen la mateixa mitjana, però <strong>A és més regular</strong> (menys dispersió).",
         r"A: rango \(9-7=2\), \(\sigma^2=\frac{2}{5}=0\dc 4\), \(\sigma\approx0\dc 63\). &nbsp; B: rango \(10-5=5\), \(\sigma^2=\frac{22}{5}=4\dc 4\), \(\sigma\approx2\dc 10\). Tienen la misma media, pero <strong>A es más regular</strong> (menos dispersión).",
         r"A: range \(9-7=2\), \(\sigma^2=\frac{2}{5}=0\dc 4\), \(\sigma\approx0\dc 63\). &nbsp; B: range \(10-5=5\), \(\sigma^2=\frac{22}{5}=4\dc 4\), \(\sigma\approx2\dc 10\). They have the same mean, but <strong>A is more consistent</strong> (less spread).")),
  prob(L(r"Un equip ha marcat 0 gols en 2 partits, 1 gol en 5, 2 gols en 5, 3 gols en 2 i 4 gols en 1. Calcula la mitjana, la variància, la desviació típica i el coeficient de variació.",
         r"Un equipo ha marcado 0 goles en 2 partidos, 1 gol en 5, 2 goles en 5, 3 goles en 2 y 4 goles en 1. Calcula la media, la varianza, la desviación típica y el coeficiente de variación.",
         r"A team scored 0 goals in 2 matches, 1 goal in 5, 2 goals in 5, 3 goals in 2 and 4 goals in 1. Find the mean, the variance, the standard deviation and the coefficient of variation."),
       vtab(GOLT),
       D(r"\bar x=\frac{25}{15}\approx1\dc 67\qquad \sigma^2=\frac{59}{15}-\Big(\frac{25}{15}\Big)^2\approx3\dc 93-2\dc 78\approx\boxed{1\dc 16}\qquad \sigma\approx\boxed{1\dc 07\ \tri{gols}{goles}{goals}}"),
       D(r"CV=\frac{1\dc 07\ldots}{1\dc 67\ldots}\approx\boxed{0\dc 645\to64\dc 5\ \%}"),
       P(r"Fes els càlculs amb tots els decimals (o amb fraccions) i arrodoneix només al final: \(\sigma^2=\frac{52}{45}\).", r"Haz los cálculos con todos los decimales (o con fracciones) y redondea solo al final: \(\sigma^2=\frac{52}{45}\).", r"Do the working with all the decimals (or with fractions) and only round at the end: \(\sigma^2=\frac{52}{45}\)."))],
 [prob(L(r"Les alçades dels jugadors d'un equip de bàsquet tenen \(\bar x=198\) cm i \(\sigma=6\) cm. Les dels xiquets d'una classe d'infantil, \(\bar x=110\) cm i \(\sigma=5\) cm. Quin grup té les alçades més disperses?",
         r"Las alturas de los jugadores de un equipo de baloncesto tienen \(\bar x=198\) cm y \(\sigma=6\) cm. Las de los niños de una clase de infantil, \(\bar x=110\) cm y \(\sigma=5\) cm. ¿Qué grupo tiene las alturas más dispersas?",
         r"The heights of a basketball team's players have \(\bar x=198\) cm and \(\sigma=6\) cm. Those of the children in a nursery class, \(\bar x=110\) cm and \(\sigma=5\) cm. Which group's heights are more spread out?"),
       P(r"Les mitjanes són molt diferents: comparem els coeficients de variació.", r"Las medias son muy diferentes: comparamos los coeficientes de variación.", r"The means are very different: compare the coefficients of variation."),
       D(r"CV_{\tri{bàsquet}{baloncesto}{basketball}}=\frac{6}{198}\approx0\dc 030\to3\dc 0\ \%\qquad CV_{\tri{infantil}{infantil}{nursery}}=\frac{5}{110}\approx0\dc 045\to4\dc 5\ \%"),
       P(r"Encara que la \(\sigma\) dels jugadors és més gran, <strong>els xiquets tenen més dispersió relativa</strong>.", r"Aunque la \(\sigma\) de los jugadores es mayor, <strong>los niños tienen más dispersión relativa</strong>.", r"Even though the players' \(\sigma\) is bigger, <strong>the children have more relative spread</strong>.")),
  prob(L(r"Calcula la desviació típica i el coeficient de variació dels diners setmanals dels 40 alumnes (apartat 9.3), que estan agrupats en intervals.",
         r"Calcula la desviación típica y el coeficiente de variación del dinero semanal de los 40 alumnos (apartado 9.3), que están agrupados en intervalos.",
         r"Find the standard deviation and coefficient of variation of the weekly money of the 40 students (section 9.3), which is grouped into intervals."),
       P(r"Fem servir les marques de classe com a \(x_i\):", r"Usamos las marcas de clase como \(x_i\):", r"Use the class marks as \(x_i\):") + vtab(DM_, L('Marca', 'Marca', 'Mark') + ' ' + M('x_i')),
       D(r"\bar x=\frac{470}{40}=11\dc 75\qquad \sigma^2=\frac{6\,950}{40}-11\dc 75^2=173\dc 75-138\dc 0625=35\dc 6875"),
       D(r"\sigma=\sqrt{35\dc 6875}\approx\boxed{5\dc 97\ \text{€}}\qquad CV=\frac{5\dc 97\ldots}{11\dc 75}\approx\boxed{0\dc 508\to50\dc 8\ \%}")),
  prob(L(r"Inventa cinc dades amb mitjana 6 i desviació típica 0. I cinc dades amb mitjana 6 i rang 10.", r"Inventa cinco datos con media 6 y desviación típica 0. Y cinco datos con media 6 y rango 10.", r"Make up five values with mean 6 and standard deviation 0. And five values with mean 6 and range 10."),
       P(r"Si \(\sigma=0\), cap dada s'allunya de la mitjana: totes són iguals a 6: \(\boxed{6,\ 6,\ 6,\ 6,\ 6}\).",
         r"Si \(\sigma=0\), ningún dato se aleja de la media: todos son iguales a 6: \(\boxed{6,\ 6,\ 6,\ 6,\ 6}\).",
         r"If \(\sigma=0\), no value is away from the mean: they're all equal to 6: \(\boxed{6,\ 6,\ 6,\ 6,\ 6}\)."),
       P(r"Per al rang 10 posem, per exemple, \(1\) i \(11\) (que se separen 5 de la mitjana per cada costat) i la resta iguals a 6: \(\boxed{1,\ 6,\ 6,\ 6,\ 11}\). Comprovem: suma \(30\), \(\bar x=6\); rang \(11-1=10\). Hi ha moltes altres solucions.",
         r"Para el rango 10 ponemos, por ejemplo, \(1\) y \(11\) (que se separan 5 de la media por cada lado) y el resto iguales a 6: \(\boxed{1,\ 6,\ 6,\ 6,\ 11}\). Comprobamos: suma \(30\), \(\bar x=6\); rango \(11-1=10\). Hay muchas otras soluciones.",
         r"For range 10 we can take, for example, \(1\) and \(11\) (5 away from the mean on each side) and the rest equal to 6: \(\boxed{1,\ 6,\ 6,\ 6,\ 11}\). Check: sum \(30\), \(\bar x=6\); range \(11-1=10\). There are many other answers."))])
assert mean([1, 6, 6, 6, 11]) == 6 and rang([1, 6, 6, 6, 11]) == 10 and var([6] * 5) == 0
P8P = [3, 5, 6, 9, 12]; assert mean(P8P) == 7 and dm(P8P) == fr('2.8') and rang(P8P) == 9 and var(P8P) == 10
ckr(sd(P8P), '3.16'); ckr(100 * cv(P8P), '45.2', 1)
P8Q = [x + 10 for x in P8P]; assert mean(P8Q) == 17 and var(P8Q) == 10; ckr(100 * cv(P8Q), '18.6', 1)
s6 += practice([('★☆☆', L(r"Calcula el rang, la desviació mitjana, la variància i la desviació típica de \(3,\ 5,\ 6,\ 9,\ 12\).", r"Calcula el rango, la desviación media, la varianza y la desviación típica de \(3,\ 5,\ 6,\ 9,\ 12\).", r"Find the range, mean deviation, variance and standard deviation of \(3,\ 5,\ 6,\ 9,\ 12\).")),
                ('★★☆', L(r"Si sumem 10 a totes les dades anteriors, què els passa a la mitjana, a la desviació típica i al coeficient de variació?", r"Si sumamos 10 a todos los datos anteriores, ¿qué les pasa a la media, a la desviación típica y al coeficiente de variación?", r"If we add 10 to each of the values above, what happens to the mean, the standard deviation and the coefficient of variation?"))],
               L(r"1) Rang \(12-3=9\); \(\bar x=7\); distàncies 4, 2, 1, 2, 5: \(DM=\frac{14}{5}=2\dc 8\); \(\sigma^2=\frac{16+4+1+4+25}{5}=10\); \(\sigma=\sqrt{10}\approx3\dc 16\). &nbsp; 2) La mitjana passa a 17, però \(\sigma\) no canvia (les dades continuen igual d'escampades). El \(CV\) baixa de \(\frac{3\dc 16}{7}\approx45\dc 2\ \%\) a \(\frac{3\dc 16}{17}\approx18\dc 6\ \%\).",
                 r"1) Rango \(12-3=9\); \(\bar x=7\); distancias 4, 2, 1, 2, 5: \(DM=\frac{14}{5}=2\dc 8\); \(\sigma^2=\frac{16+4+1+4+25}{5}=10\); \(\sigma=\sqrt{10}\approx3\dc 16\). &nbsp; 2) La media pasa a 17, pero \(\sigma\) no cambia (los datos siguen igual de esparcidos). El \(CV\) baja de \(\frac{3\dc 16}{7}\approx45\dc 2\ \%\) a \(\frac{3\dc 16}{17}\approx18\dc 6\ \%\).",
                 r"1) Range \(12-3=9\); \(\bar x=7\); distances 4, 2, 1, 2, 5: \(MD=\frac{14}{5}=2\dc 8\); \(\sigma^2=\frac{16+4+1+4+25}{5}=10\); \(\sigma=\sqrt{10}\approx3\dc 16\). &nbsp; 2) The mean becomes 17, but \(\sigma\) doesn't change (the data are just as spread out). The \(CV\) drops from \(\frac{3\dc 16}{7}\approx45\dc 2\ \%\) to \(\frac{3\dc 16}{17}\approx18\dc 6\ \%\)."))
