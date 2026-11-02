# Apartats 10.7-10.9 dels apunts de la Unitat 10 de 1r ESO: paràmetres a partir d'una taula de freqüències,
# paràmetres de dispersió (rang i desviació mitjana) i problemes d'estadística.
from comu import *
from s123 import TG, NOT, EDG, FA, acc

def ttab(tab, xl=None):
    """taula amb xi, fi, Fi i xi·fi (i la fila de totals)"""
    N = sum(f for _, f in tab); F = acc(tab); S = sum(x * f for x, f in tab)
    rows = [[M(tn(x)), M(str(f)), M(str(Fi)), M(tn(x * f))] for (x, f), Fi in zip(tab, F)]
    rows.append(['<strong>Total</strong>', M('N=%d' % N), '', M(r'\textstyle\sum=%s' % tn(S))])
    return tbl([xl or M('x_i'), M('f_i'), M('F_i'), M(r'x_i\cdot f_i')], rows, 'c freq')

# =====================================================================
# 10.7 Paràmetres a partir d'una taula de freqüències
# =====================================================================
DG = expand(TG)
assert sum(x * f for x, f in TG) == 29 and mean(DG) == Fr(29, 20) and median(DG) == 1 and modes(DG) == [1]
DN = expand(NOT)
assert sum(x * f for x, f in NOT) == 164 and mean(DN) == Fr(164, 25) and median(DN) == 6 and modes(DN) == [6]
s7 = box('prop', L('Mitjana, mediana i moda en una taula', 'Media, mediana y moda en una tabla', 'Mean, median and mode from a table'),
  P(r"Quan les dades estan en una taula de freqüències no cal escriure-les totes una per una:",
    r"Cuando los datos están en una tabla de frecuencias no hace falta escribirlos todos uno por uno:",
    r"When the data are in a frequency table we don't need to write them all out one by one:")
  + ul(L(r"<strong>Mitjana</strong>: cada valor \(x_i\) apareix \(f_i\) vegades, així que en lloc de sumar-lo \(f_i\) vegades el <strong>multipliquem</strong>: \(\bar x=\dfrac{\sum x_i\cdot f_i}{N}\). Hi afegim una columna \(x_i\cdot f_i\).",
         r"<strong>Media</strong>: cada valor \(x_i\) aparece \(f_i\) veces, así que en lugar de sumarlo \(f_i\) veces lo <strong>multiplicamos</strong>: \(\bar x=\dfrac{\sum x_i\cdot f_i}{N}\). Añadimos una columna \(x_i\cdot f_i\).",
         r"<strong>Mean</strong>: each value \(x_i\) appears \(f_i\) times, so instead of adding it \(f_i\) times we <strong>multiply</strong>: \(\bar x=\dfrac{\sum x_i\cdot f_i}{N}\). We add a column \(x_i\cdot f_i\)."),
       L(r"<strong>Mediana</strong>: busquem quina posició ocupa la dada central (si \(N\) és parell, les dues centrals) i mirem en la columna \(F_i\) a quin valor correspon: és el primer valor amb \(F_i\) igual o més gran que aquesta posició.",
         r"<strong>Mediana</strong>: buscamos qué posición ocupa el dato central (si \(N\) es par, los dos centrales) y miramos en la columna \(F_i\) a qué valor corresponde: es el primer valor con \(F_i\) igual o mayor que esa posición.",
         r"<strong>Median</strong>: find the position of the middle value (if \(N\) is even, the two middle ones) and look in the \(F_i\) column to see which value it belongs to: it's the first value whose \(F_i\) is greater than or equal to that position."),
       L(r"<strong>Moda</strong>: el valor amb la \(f_i\) més gran.", r"<strong>Moda</strong>: el valor con la \(f_i\) más grande.", r"<strong>Mode</strong>: the value with the largest \(f_i\)."))
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"Nombre de germans de 20 alumnes (apartat 10.2):", r"Número de hermanos de 20 alumnos (apartado 10.2):", r"Number of siblings of 20 students (section 10.2):") + ttab(TG)
        + ul(L(r"Mitjana: \(\bar x=\dfrac{29}{20}=1\dc 45\) germans.", r"Media: \(\bar x=\dfrac{29}{20}=1\dc 45\) hermanos.", r"Mean: \(\bar x=\dfrac{29}{20}=1\dc 45\) siblings."),
             L(r"Mediana: \(N=20\) és parell, les centrals són la 10a i l'11a dada. Fins al valor 0 n'hi ha 3 i fins a l'1, 12: la 10a i l'11a són 1. \(Me=\dfrac{1+1}{2}=1\) germà.",
               r"Mediana: \(N=20\) es par, los centrales son el 10.º y el 11.º dato. Hasta el valor 0 hay 3 y hasta el 1, 12: el 10.º y el 11.º son 1. \(Me=\dfrac{1+1}{2}=1\) hermano.",
               r"Median: \(N=20\) is even, so the middle ones are the 10th and 11th values. Up to 0 there are 3, and up to 1 there are 12: the 10th and 11th are both 1. \(Me=\dfrac{1+1}{2}=1\) sibling."),
             L(r"Moda: \(Mo=1\) germà (\(f=9\), la més gran).", r"Moda: \(Mo=1\) hermano (\(f=9\), la mayor).", r"Mode: \(Mo=1\) sibling (\(f=9\), the largest).")))
  + note(r"La mitjana pot ser un nombre que no és cap de les dades (ningú té 1,45 germans!). Vol dir que, si repartírem tots els germans a parts iguals, en tocarien 1,45 per alumne.",
         r"La media puede ser un número que no es ninguno de los datos (¡nadie tiene 1,45 hermanos!). Quiere decir que, si repartiéramos todos los hermanos a partes iguales, tocarían 1,45 por alumno.",
         r"The mean can be a number that isn't any of the data (nobody has 1.45 siblings!). It means that if we shared all the siblings out equally, each student would get 1.45."))
s7 += (widget('w-tmean', '🧾', L('Paràmetres d’una taula de freqüències', 'Parámetros de una tabla de frecuencias', 'Measures from a frequency table'),
              ['<p class="hint-s">' + L("Escriu els valors i les seues freqüències: l'eina fa la columna <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub>, la mitjana, la mediana amb les <i>F</i><sub>i</sub> i la moda.", "Escribe los valores y sus frecuencias: la herramienta hace la columna <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub>, la media, la mediana con las <i>F</i><sub>i</sub> y la moda.", "Type the values and their frequencies: the tool builds the <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub> column, the mean, the median from <i>F</i><sub>i</sub> and the mode.") + '</p>',
               seg([('germ', L('Germans', 'Hermanos', 'Siblings')), ('not', L('Notes', 'Notas', 'Marks')), ('own', L('Els meus', 'Los míos', 'My own'))]),
               '<div class="wrow">' + tin('x', '<i>x</i><sub>i</sub>', '', 'w') + '</div><div class="wrow">' + tin('f', '<i>f</i><sub>i</sub>', '', 'w') + '</div>'], out='<div class="tout"></div>')
       + drill('tmean', 'Entrena: la mitjana des d’una taula', 'Entrena: la media desde una tabla', 'Train: the mean from a table'))

PETS = [(0, 6), (1, 10), (2, 5), (3, 3)]
DP = expand(PETS)
assert mean(DP) == Fr(29, 24) and median(DP) == 1 and modes(DP) == [1]
CAL = [(36, 3), (37, 5), (38, 8), (39, 6), (40, 2)]
DC = expand(CAL)
assert len(DC) == 24 and sum(x * f for x, f in CAL) == 911 and median(DC) == 38 and modes(DC) == [38]
MK = [Fr(EDG[i] + EDG[i + 1], 2) for i in range(5)]
SA = sum(m * f for m, f in zip(MK, FA)); assert SA == 4580
s7 += levels(
 [prob(L(r"Calcula la mitjana de mascotes per alumne amb aquesta taula: " + ', '.join(f'{x} mascotes → {f} alumnes' for x, f in PETS) + ".",
         r"Calcula la media de mascotas por alumno con esta tabla: " + ', '.join(f'{x} mascotas → {f} alumnos' for x, f in PETS) + ".",
         r"Work out the mean number of pets per student from this table: " + ', '.join(f'{x} pets → {f} students' for x, f in PETS) + "."),
       ttab(PETS),
       D(r"\bar x=\frac{29}{24}\approx\boxed{1\dc 21}\ \tri{mascotes}{mascotas}{pets}"))],
 [prob(L(r"Aquesta taula recull el número de calçat de 24 alumnes. Calcula la mitjana, la mediana i la moda.",
         r"Esta tabla recoge el número de calzado de 24 alumnos. Calcula la media, la mediana y la moda.",
         r"This table shows the shoe size of 24 students. Find the mean, median and mode.") + tbl([L('Número', 'Número', 'Size')] + [str(x) for x, _ in CAL], [[M('f_i')] + [str(f) for _, f in CAL]], 'c'),
       ttab(CAL) + D(r"\bar x=\frac{911}{24}\approx\boxed{37\dc 96}"),
       P(r"\(N=24\): les centrals són la 12a i la 13a dada. Fins al 37 n'hi ha 8 i fins al 38, 16: totes dues són 38. \(\boxed{Me=38}\). La moda és el valor amb més freqüència: \(\boxed{Mo=38}\).",
         r"\(N=24\): los centrales son el 12.º y el 13.º dato. Hasta el 37 hay 8 y hasta el 38, 16: los dos son 38. \(\boxed{Me=38}\). La moda es el valor con más frecuencia: \(\boxed{Mo=38}\).",
         r"\(N=24\): the middle ones are the 12th and 13th values. Up to 37 there are 8 and up to 38 there are 16: both are 38. \(\boxed{Me=38}\). The mode is the most frequent value: \(\boxed{Mo=38}\)."))],
 [prob(L(r"Calcula la mitjana aproximada de les alçades dels 30 alumnes de l'apartat 10.3, que estan agrupades en intervals.",
         r"Calcula la media aproximada de las alturas de los 30 alumnos del apartado 10.3, que están agrupadas en intervalos.",
         r"Work out the approximate mean height of the 30 students in section 10.3, whose data are grouped into intervals."),
       P(r"Com que no sabem cada dada, fem servir la <strong>marca de classe</strong> de cada interval com a \(x_i\):", r"Como no sabemos cada dato, usamos la <strong>marca de clase</strong> de cada intervalo como \(x_i\):", r"As we don't know each value, we use the <strong>class mark</strong> of each interval as \(x_i\):")
       + ttab(list(zip(MK, FA)), L('Marca', 'Marca', 'Mark')),
       D(r"\bar x\approx\frac{4\,580}{30}\approx\boxed{152\dc 67\ \text{cm}}"),
       P(r"És una aproximació: amb les 30 dades originals la mitjana exacta és \(152\dc 13\) cm, molt pròxima.", r"Es una aproximación: con los 30 datos originales la media exacta es \(152\dc 13\) cm, muy próxima.", r"It's an approximation: with the 30 original values the exact mean is \(152\dc 13\) cm, very close."))])
from s123 import ALT
assert abs(float(mean(ALT)) - 152.13) < 0.005
s7 += practice([('★☆☆', L(r"Calcula la mitjana, la mediana i la moda de les notes de la taula de l'apartat 10.3 (25 alumnes).", r"Calcula la media, la mediana y la moda de las notas de la tabla del apartado 10.3 (25 alumnos).", r"Find the mean, median and mode of the marks in the table in section 10.3 (25 students).")),
                ('★★☆', L(r"En una taula, el valor 5 té \(f=4\) i el valor 8 té \(f=6\). Quina és la mitjana?", r"En una tabla, el valor 5 tiene \(f=4\) y el valor 8 tiene \(f=6\). ¿Cuál es la media?", r"In a table, the value 5 has \(f=4\) and the value 8 has \(f=6\). What is the mean?"))],
               L(r"1) \(\sum x_i f_i=164\), \(\bar x=\frac{164}{25}=6\dc 56\); la dada central és la 13a i \(F=13\) en el 6: \(Me=6\); \(Mo=6\). &nbsp; 2) \(\bar x=\frac{5\cdot4+8\cdot6}{10}=\frac{68}{10}=6\dc 8\).",
                 r"1) \(\sum x_i f_i=164\), \(\bar x=\frac{164}{25}=6\dc 56\); el dato central es el 13.º y \(F=13\) en el 6: \(Me=6\); \(Mo=6\). &nbsp; 2) \(\bar x=\frac{5\cdot4+8\cdot6}{10}=\frac{68}{10}=6\dc 8\).",
                 r"1) \(\sum x_i f_i=164\), \(\bar x=\frac{164}{25}=6\dc 56\); the middle value is the 13th and \(F=13\) at 6: \(Me=6\); \(Mo=6\). &nbsp; 2) \(\bar x=\frac{5\cdot4+8\cdot6}{10}=\frac{68}{10}=6\dc 8\)."))
ck(mean(expand([(5, 4), (8, 6)])), '6.8')

# =====================================================================
# 10.8 Rang i desviació mitjana
# =====================================================================
ANNA = [8, 9, 10, 11, 12]; BEA = [2, 6, 10, 14, 18]
assert mean(ANNA) == mean(BEA) == 10 and rang(ANNA) == 4 and rang(BEA) == 16 and dm(ANNA) == Fr(6, 5) and dm(BEA) == Fr(24, 5)
def dtab(data):
    m = mean(data)
    rows = [[M(tn(x)), M(r'|%s-%s|=%s' % (tn(x), tn(m), tn(abs(x - m))))] for x in data]
    rows.append(['<strong>Total</strong>', M(r'\textstyle\sum=%s' % tn(sum(abs(x - m) for x in data)))])
    return tbl([M('x_i'), M(r'|x_i-\bar x|')], rows, 'c freq')
F_AB = figs(fig(dots(ANNA, 0, 20, mean_=10, dev=True, step=2), 'Anna'), fig(dots(BEA, 0, 20, mean_=10, dev=True, step=2), 'Bea'))
s8 = box('def', L('Paràmetres de dispersió', 'Parámetros de dispersión', 'Measures of spread'),
  P(r"Dos grups de dades poden tindre la mateixa mitjana i ser molt diferents. Els punts que han fet Anna i Bea en cinc partits de bàsquet són:",
    r"Dos grupos de datos pueden tener la misma media y ser muy diferentes. Los puntos que han hecho Anna y Bea en cinco partidos de baloncesto son:",
    r"Two sets of data can have the same mean and still be very different. The points Anna and Bea scored in five basketball games are:")
  + D(r"\text{Anna: }8,\ 9,\ 10,\ 11,\ 12\qquad \text{Bea: }2,\ 6,\ 10,\ 14,\ 18")
  + P(r"Totes dues fan una mitjana de 10 punts, però Anna és molt més <strong>regular</strong>. Els <strong>paràmetres de dispersió</strong> mesuren com d'<strong>escampades</strong> estan les dades:",
      r"Las dos hacen una media de 10 puntos, pero Anna es mucho más <strong>regular</strong>. Los <strong>parámetros de dispersión</strong> miden lo <strong>esparcidos</strong> que están los datos:",
      r"Both average 10 points, but Anna is much more <strong>consistent</strong>. <strong>Measures of spread</strong> tell us how <strong>spread out</strong> the data are:")
  + ul(L(r"El <strong>rang</strong> (o recorregut) és la diferència entre la dada més gran i la més xicoteta: \(\text{rang}=x_{\max}-x_{\min}\).",
         r"El <strong>rango</strong> (o recorrido) es la diferencia entre el dato mayor y el menor: \(\text{rango}=x_{\max}-x_{\min}\).",
         r"The <strong>range</strong> is the difference between the largest and smallest values: \(\text{range}=x_{\max}-x_{\min}\)."),
       L(r"La <strong>desviació mitjana</strong> (\(DM\)) és la mitjana de les <strong>distàncies</strong> de cada dada a la mitjana: \(DM=\dfrac{\sum|x_i-\bar x|}{N}\). Les distàncies sempre són positives (per això posem el valor absolut).",
         r"La <strong>desviación media</strong> (\(DM\)) es la media de las <strong>distancias</strong> de cada dato a la media: \(DM=\dfrac{\sum|x_i-\bar x|}{N}\). Las distancias siempre son positivas (por eso ponemos el valor absoluto).",
         r"The <strong>mean deviation</strong> (\(MD\)) is the mean of the <strong>distances</strong> from each value to the mean: \(MD=\dfrac{\sum|x_i-\bar x|}{N}\). Distances are always positive (that's why we use the absolute value)."))
  + P(r"Com <strong>més grans</strong> són el rang i la desviació mitjana, <strong>més escampades</strong> estan les dades i menys representativa és la mitjana.",
      r"Cuanto <strong>mayores</strong> son el rango y la desviación media, <strong>más esparcidos</strong> están los datos y menos representativa es la media.",
      r"The <strong>larger</strong> the range and the mean deviation, the <strong>more spread out</strong> the data are and the less representative the mean is."))
s8 += box('ex', L('Exemple: Anna i Bea', 'Ejemplo: Anna y Bea', 'Example: Anna and Bea'),
  '<div class="tv2">' + dtab(ANNA) + dtab(BEA) + '</div>'
  + ul(L(r"Anna: rang \(=12-8=4\) punts; \(DM=\dfrac{6}{5}=1\dc 2\) punts.", r"Anna: rango \(=12-8=4\) puntos; \(DM=\dfrac{6}{5}=1\dc 2\) puntos.", r"Anna: range \(=12-8=4\) points; \(MD=\dfrac{6}{5}=1\dc 2\) points."),
       L(r"Bea: rang \(=18-2=16\) punts; \(DM=\dfrac{24}{5}=4\dc 8\) punts.", r"Bea: rango \(=18-2=16\) puntos; \(DM=\dfrac{24}{5}=4\dc 8\) puntos.", r"Bea: range \(=18-2=16\) points; \(MD=\dfrac{24}{5}=4\dc 8\) points."))
  + F_AB
  + P(r"De mitjana, cada partit d'Anna s'allunya 1,2 punts de 10, i cada partit de Bea, 4,8 punts: Anna és més regular.",
      r"De media, cada partido de Anna se aleja 1,2 puntos de 10, y cada partido de Bea, 4,8 puntos: Anna es más regular.",
      r"On average, each of Anna's games is 1.2 points away from 10, and each of Bea's 4.8 points: Anna is more consistent."))
s8 += (widget('w-disp', '↔️', L('Compara la dispersió de dos grups', 'Compara la dispersión de dos grupos', 'Compare the spread of two sets'),
              ['<p class="hint-s">' + L("Escriu dos grups de dades: l'eina dibuixa la distància de cada dada a la mitjana i calcula el rang i la desviació mitjana.", "Escribe dos grupos de datos: la herramienta dibuja la distancia de cada dato a la media y calcula el rango y la desviación media.", "Type two sets of data: the tool draws each value's distance to the mean and works out the range and mean deviation.") + '</p>',
               '<div class="wrow">' + tin('a', 'A', '8 9 10 11 12', 'w') + '</div><div class="wrow">' + tin('b', 'B', '2 6 10 14 18', 'w') + '</div>'], out='<div class="tout"></div>')
       + drill('rang', 'Entrena: calcula el rang', 'Entrena: calcula el rango', 'Train: find the range')
       + drill('dm', 'Entrena: calcula la desviació mitjana', 'Entrena: calcula la desviación media', 'Train: find the mean deviation'))

TMP = [-2, 5, 3, -4, 1, 6, 0]
assert rang(TMP) == 10
D82 = [4, 7, 8, 10, 11]; assert mean(D82) == 8 and dm(D82) == 2
ARA = [7, 8, 8, 9, 8]; ARB = [10, 6, 9, 5, 10]
assert mean(ARA) == mean(ARB) == 8 and dm(ARA) == Fr(2, 5) and dm(ARB) == 2 and rang(ARA) == 2 and rang(ARB) == 5
s8 += levels(
 [prob(L(r"Les temperatures mínimes d'una setmana d'hivern han sigut \(-2,\ 5,\ 3,\ -4,\ 1,\ 6,\ 0\) °C. Calcula el rang.",
         r"Las temperaturas mínimas de una semana de invierno han sido \(-2,\ 5,\ 3,\ -4,\ 1,\ 6,\ 0\) °C. Calcula el rango.",
         r"The minimum temperatures of a winter week were \(-2,\ 5,\ 3,\ -4,\ 1,\ 6,\ 0\) °C. Find the range."),
       D(r"\text{\tri{rang}{rango}{range}}=6-(-4)=6+4=\boxed{10\ ^\circ\text{C}}")),
  prob(L(r"Calcula la desviació mitjana de les dades \(4,\ 7,\ 8,\ 10,\ 11\).", r"Calcula la desviación media de los datos \(4,\ 7,\ 8,\ 10,\ 11\).", r"Find the mean deviation of the data \(4,\ 7,\ 8,\ 10,\ 11\)."),
       D(r"\bar x=\frac{40}{5}=8"),
       dtab(D82) + D(r"DM=\frac{10}{5}=\boxed{2}"))],
 [prob(L(r"Dos arquers han fet aquestes puntuacions en cinc tirades. A: \(7,\ 8,\ 8,\ 9,\ 8\); B: \(10,\ 6,\ 9,\ 5,\ 10\). Calcula la mitjana, el rang i la desviació mitjana de cadascun. Qui és més regular?",
         r"Dos arqueros han hecho estas puntuaciones en cinco tiradas. A: \(7,\ 8,\ 8,\ 9,\ 8\); B: \(10,\ 6,\ 9,\ 5,\ 10\). Calcula la media, el rango y la desviación media de cada uno. ¿Quién es más regular?",
         r"Two archers scored these points in five shots. A: \(7,\ 8,\ 8,\ 9,\ 8\); B: \(10,\ 6,\ 9,\ 5,\ 10\). Find each one's mean, range and mean deviation. Who is more consistent?"),
       D(r"\bar x_A=\frac{40}{5}=8\qquad \bar x_B=\frac{40}{5}=8"),
       '<div class="tv2">' + dtab(ARA) + dtab(ARB) + '</div>',
       P(r"A: rang \(9-7=2\), \(DM=\frac{2}{5}=0\dc 4\). &nbsp; B: rang \(10-5=5\), \(DM=\frac{10}{5}=2\). Tenen la mateixa mitjana, però <strong>A és més regular</strong> (menys dispersió).",
         r"A: rango \(9-7=2\), \(DM=\frac{2}{5}=0\dc 4\). &nbsp; B: rango \(10-5=5\), \(DM=\frac{10}{5}=2\). Tienen la misma media, pero <strong>A es más regular</strong> (menos dispersión).",
         r"A: range \(9-7=2\), \(MD=\frac{2}{5}=0\dc 4\). &nbsp; B: range \(10-5=5\), \(MD=\frac{10}{5}=2\). They have the same mean, but <strong>A is more consistent</strong> (less spread)."))],
 [prob(L(r"Inventa cinc dades amb mitjana 6 i rang 0. I cinc dades amb mitjana 6 i rang 10.", r"Inventa cinco datos con media 6 y rango 0. Y cinco datos con media 6 y rango 10.", r"Make up five values with mean 6 and range 0. And five values with mean 6 and range 10."),
       P(r"Si el rang és 0, la més gran i la més xicoteta són iguals: totes les dades són iguals, i han de ser la mitjana: \(\boxed{6,\ 6,\ 6,\ 6,\ 6}\).",
         r"Si el rango es 0, el mayor y el menor son iguales: todos los datos son iguales, y tienen que ser la media: \(\boxed{6,\ 6,\ 6,\ 6,\ 6}\).",
         r"If the range is 0, the largest and smallest are equal: all the values are the same, so they must equal the mean: \(\boxed{6,\ 6,\ 6,\ 6,\ 6}\)."),
       P(r"Per al rang 10 posem, per exemple, \(1\) i \(11\) (que se separen 5 de la mitjana per cada costat) i la resta iguals a 6: \(\boxed{1,\ 6,\ 6,\ 6,\ 11}\). Comprovem: suma \(30\), \(\bar x=6\); rang \(11-1=10\). Hi ha moltes altres solucions.",
         r"Para el rango 10 ponemos, por ejemplo, \(1\) y \(11\) (que se separan 5 de la media por cada lado) y el resto iguales a 6: \(\boxed{1,\ 6,\ 6,\ 6,\ 11}\). Comprobamos: suma \(30\), \(\bar x=6\); rango \(11-1=10\). Hay muchas otras soluciones.",
         r"For range 10 we can take, for example, \(1\) and \(11\) (5 away from the mean on each side) and the rest equal to 6: \(\boxed{1,\ 6,\ 6,\ 6,\ 11}\). Check: sum \(30\), \(\bar x=6\); range \(11-1=10\). There are many other answers."))])
assert mean([1, 6, 6, 6, 11]) == 6 and rang([1, 6, 6, 6, 11]) == 10
P8P = [3, 5, 6, 9, 12]; assert mean(P8P) == 7 and dm(P8P) == fr('2.8') and rang(P8P) == 9
s8 += practice([('★☆☆', L(r"Calcula el rang i la desviació mitjana de \(3,\ 5,\ 6,\ 9,\ 12\).", r"Calcula el rango y la desviación media de \(3,\ 5,\ 6,\ 9,\ 12\).", r"Find the range and mean deviation of \(3,\ 5,\ 6,\ 9,\ 12\).")),
                ('★★☆', L(r"Si sumem 10 a totes les dades, què els passa a la mitjana, al rang i a la desviació mitjana?", r"Si sumamos 10 a todos los datos, ¿qué les pasa a la media, al rango y a la desviación media?", r"If we add 10 to every value, what happens to the mean, the range and the mean deviation?"))],
               L(r"1) Rang \(12-3=9\); \(\bar x=7\); distàncies 4, 2, 1, 2, 5: \(DM=\frac{14}{5}=2\dc 8\). &nbsp; 2) La mitjana augmenta 10, però el rang i la desviació mitjana no canvien: totes les dades es desplacen igual i continuen igual d'escampades.",
                 r"1) Rango \(12-3=9\); \(\bar x=7\); distancias 4, 2, 1, 2, 5: \(DM=\frac{14}{5}=2\dc 8\). &nbsp; 2) La media aumenta 10, pero el rango y la desviación media no cambian: todos los datos se desplazan igual y siguen igual de esparcidos.",
                 r"1) Range \(12-3=9\); \(\bar x=7\); distances 4, 2, 1, 2, 5: \(MD=\frac{14}{5}=2\dc 8\). &nbsp; 2) The mean goes up by 10, but the range and mean deviation don't change: all the data move the same amount and stay just as spread out."))
P8Q = [x + 10 for x in P8P]; assert mean(P8Q) == 17 and rang(P8Q) == 9 and dm(P8Q) == dm(P8P)

# =====================================================================
# 10.9 Problemes d'estadística
# =====================================================================
s9 = box('prop', L('Estratègies útils', 'Estrategias útiles', 'Useful strategies'),
  ul(L(r"Si coneixem la mitjana i el nombre de dades, coneixem la <strong>suma</strong> de totes: \(\text{suma}=\bar x\cdot N\). Així podem trobar una dada que falta.",
       r"Si conocemos la media y el número de datos, conocemos la <strong>suma</strong> de todos: \(\text{suma}=\bar x\cdot N\). Así podemos encontrar un dato que falta.",
       r"If we know the mean and the number of data, we know their <strong>sum</strong>: \(\text{sum}=\bar x\cdot N\). That lets us find a missing value."),
     L(r"Per a ajuntar dos grups, <strong>no</strong> fem la mitjana de les mitjanes: sumem les sumes i dividim entre el total de dades.",
       r"Para juntar dos grupos, <strong>no</strong> hacemos la media de las medias: sumamos las sumas y dividimos entre el total de datos.",
       r"To combine two groups we do <strong>not</strong> average the means: we add the sums and divide by the total number of data."),
     L(r"Abans de triar un paràmetre, pensa què vols dir: la <strong>moda</strong> diu el més freqüent; la <strong>mitjana</strong>, el repartiment a parts iguals; la <strong>mediana</strong>, el valor del centre (no la mouen les dades extremes); el <strong>rang</strong> i la <strong>DM</strong>, com d'escampades estan.",
       r"Antes de elegir un parámetro, piensa qué quieres decir: la <strong>moda</strong> dice lo más frecuente; la <strong>media</strong>, el reparto a partes iguales; la <strong>mediana</strong>, el valor del centro (no la mueven los datos extremos); el <strong>rango</strong> y la <strong>DM</strong>, lo esparcidos que están.",
       r"Before choosing a measure, think about what you want to say: the <strong>mode</strong> tells you the most common; the <strong>mean</strong>, the equal share; the <strong>median</strong>, the middle value (extreme values don't move it); the <strong>range</strong> and <strong>MD</strong>, how spread out the data are."))
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"Marta ha tret \(6\), \(7\) i \(5\) en tres exàmens. Quina nota necessita en el quart per a tindre una mitjana de \(6\dc 5\)?",
          r"Marta ha sacado \(6\), \(7\) y \(5\) en tres exámenes. ¿Qué nota necesita en el cuarto para tener una media de \(6\dc 5\)?",
          r"Marta got \(6\), \(7\) and \(5\) in three tests. What mark does she need in the fourth to have a mean of \(6\dc 5\)?")
        + D(r"\text{\tri{suma necessària}{suma necesaria}{sum needed}}=6\dc 5\cdot4=26\qquad \text{\tri{ja té}{ya tiene}{she has}}\ 6+7+5=18\qquad 26-18=\boxed{8}")))
ck(fr('6.5') * 4 - 18, 8)
s9 += (widget('w-target', '🏁', L('Quina nota necessite?', '¿Qué nota necesito?', 'What mark do I need?'),
              ['<p class="hint-s">' + L("Escriu les notes que ja tens i la mitjana que vols aconseguir.", "Escribe las notas que ya tienes y la media que quieres conseguir.", "Type the marks you already have and the mean you want to reach.") + '</p>',
               '<div class="wrow">' + tin('d', L('Notes', 'Notas', 'Marks'), '6 7 5', 'w') + '</div><div class="wrow">' + tin('m', L('Mitjana desitjada', 'Media deseada', 'Target mean'), '6,5') + tin('k', L('Exàmens que queden', 'Exámenes que quedan', 'Tests left'), '1') + '</div>'], out='<div class="tout"></div>')
       + drill('falta', 'Entrena: troba la dada que falta', 'Entrena: encuentra el dato que falta', 'Train: find the missing value'))

ck(fr('6.2') * 20 + fr('7.1') * 10, 195); ck(Fr(195, 30), '6.5')
ck(16 * 6 - 13 * 5, 31)
# taula amb una freqüència desconeguda: valors 1, 2, 3, 4 amb f 3, x, 5, 2 i mitjana 2,5
assert mean(expand([(1, 3), (2, 2), (3, 5), (4, 2)])) == Fr(5, 2)
s9 += levels(
 [prob(L(r"La mitjana d'edat dels 5 membres d'un grup de música és de 13 anys. Quan hi entra la monitora, la mitjana dels 6 passa a ser de 16 anys. Quants anys té la monitora?",
         r"La media de edad de los 5 miembros de un grupo de música es de 13 años. Cuando entra la monitora, la media de los 6 pasa a ser de 16 años. ¿Cuántos años tiene la monitora?",
         r"The mean age of the 5 members of a music group is 13. When the instructor joins, the mean of the 6 becomes 16. How old is the instructor?"),
       P(r"Passem de mitjanes a sumes:", r"Pasamos de medias a sumas:", r"Turn the means into sums:"),
       D(r"5\cdot13=65\qquad 6\cdot16=96\qquad 96-65=\boxed{31\ \tri{anys}{años}{years}}"))],
 [prob(L(r"En una classe de 20 alumnes la nota mitjana d'un examen ha sigut \(6\dc 2\) i en una altra classe de 10 alumnes, \(7\dc 1\). Quina és la nota mitjana dels 30 alumnes?",
         r"En una clase de 20 alumnos la nota media de un examen ha sido \(6\dc 2\) y en otra clase de 10 alumnos, \(7\dc 1\). ¿Cuál es la nota media de los 30 alumnos?",
         r"In a class of 20 students the mean test mark was \(6\dc 2\), and in another class of 10 students it was \(7\dc 1\). What is the mean mark of all 30 students?"),
       D(r"6\dc 2\cdot20=124\qquad 7\dc 1\cdot10=71\qquad \bar x=\frac{124+71}{30}=\frac{195}{30}=\boxed{6\dc 5}"),
       P(r"Compte: la mitjana de les mitjanes, \(\frac{6\dc 2+7\dc 1}{2}=6\dc 65\), <strong>no</strong> és correcta, perquè la primera classe té el doble d'alumnes.",
         r"Cuidado: la media de las medias, \(\frac{6\dc 2+7\dc 1}{2}=6\dc 65\), <strong>no</strong> es correcta, porque la primera clase tiene el doble de alumnos.",
         r"Careful: the mean of the means, \(\frac{6\dc 2+7\dc 1}{2}=6\dc 65\), is <strong>not</strong> correct, because the first class has twice as many students."))],
 [prob(L(r"En aquesta taula falta una freqüència. Troba-la sabent que la mitjana és \(2\dc 5\).", r"En esta tabla falta una frecuencia. Encuéntrala sabiendo que la media es \(2\dc 5\).", r"One frequency is missing from this table. Find it, given that the mean is \(2\dc 5\).")
       + tbl([M('x_i'), '1', '2', '3', '4'], [[M('f_i'), '3', M('a'), '5', '2']], 'c'),
       P(r"Sense \(a\), les altres dades sumen \(1\cdot3+3\cdot5+4\cdot2=26\) i són \(10\). Amb les \(a\) dades de valor 2:", r"Sin \(a\), los demás datos suman \(1\cdot3+3\cdot5+4\cdot2=26\) y son \(10\). Con los \(a\) datos de valor 2:", r"Without \(a\), the other data add up to \(1\cdot3+3\cdot5+4\cdot2=26\) and there are \(10\). With the \(a\) values equal to 2:"),
       D(r"\frac{26+2a}{10+a}=2\dc 5\ \Rightarrow\ 26+2a=25+2\dc 5a\ \Rightarrow\ 1=0\dc 5a\ \Rightarrow\ \boxed{a=2}"),
       P(r"Comprovem: \(\frac{26+4}{12}=\frac{30}{12}=2\dc 5\). ✓", r"Comprobamos: \(\frac{26+4}{12}=\frac{30}{12}=2\dc 5\). ✓", r"Check: \(\frac{26+4}{12}=\frac{30}{12}=2\dc 5\). ✓"))])
s9 += practice([('★☆☆', L(r"La mitjana de 4 nombres és 9. Tres d'ells són 7, 12 i 8. Quin és el quart?", r"La media de 4 números es 9. Tres de ellos son 7, 12 y 8. ¿Cuál es el cuarto?", r"The mean of 4 numbers is 9. Three of them are 7, 12 and 8. What is the fourth?")),
                ('★★☆', L(r"Un equip ha marcat de mitjana 2 gols en 9 partits. Quants gols ha de marcar en el 10è partit perquè la mitjana siga \(2\dc 2\)?", r"Un equipo ha marcado de media 2 goles en 9 partidos. ¿Cuántos goles tiene que marcar en el 10.º partido para que la media sea \(2\dc 2\)?", r"A team has scored a mean of 2 goals in 9 matches. How many goals must it score in the 10th match for the mean to be \(2\dc 2\)?"))],
               L(r"1) Suma \(9\cdot4=36\); \(36-(7+12+8)=9\). &nbsp; 2) Ara en porta \(2\cdot9=18\) i en necessita \(2\dc 2\cdot10=22\): ha de marcar \(4\) gols.",
                 r"1) Suma \(9\cdot4=36\); \(36-(7+12+8)=9\). &nbsp; 2) Ahora lleva \(2\cdot9=18\) y necesita \(2\dc 2\cdot10=22\): tiene que marcar \(4\) goles.",
                 r"1) Sum \(9\cdot4=36\); \(36-(7+12+8)=9\). &nbsp; 2) It has \(2\cdot9=18\) so far and needs \(2\dc 2\cdot10=22\): it must score \(4\) goals."))
ck(36 - 27, 9); ck(fr('2.2') * 10 - 18, 4)
