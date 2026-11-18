# Apartats 9.7 i 9.8 dels apunts de la Unitat 9 de 4t ESO Matemàtiques A (Estadística): paràmetres de posició (quartils
# i percentils) i diagrama de caixes. Són nous. Criteri per als quartils i percentils (el mateix de la mediana i dels apunts
# de 1r Batx MI): posició k·N/100; si no és entera, la dada de la posició següent; si és entera, la mitjana d'eixa dada i
# la següent (en una taula: el primer valor amb F_i ≥ k·N/100; si F_i = k·N/100 exactament, la mitjana amb el següent).
from comu import *
from s123 import NOT, DIN, FDIN, ivl, acc

def olist(data, marks):
    """llista ordenada en TeX; marks: {posició (1..N): color} encercla les dades d'aquestes posicions"""
    d = sorted(data)
    return r',\ '.join((r'\boxed{%s}' % tn(x)) if (i + 1) in marks else tn(x) for i, x in enumerate(d))
def poscell(data):
    """fila de posicions i dades (taula petita)"""
    d = sorted(data)
    return tbl([L('Posició', 'Posición', 'Position')] + [str(i + 1) for i in range(len(d))], [[L('Dada', 'Dato', 'Value')] + [M(tn(x)) for x in d]], 'c pos')
def ftabq(tab):
    F = acc(tab)
    rows = [[M(tn(x)), M(str(f)), M(str(Fi))] for (x, f), Fi in zip(tab, F)]
    return tbl([M('x_i'), M('f_i'), M('F_i')], rows, 'c freq')

# =====================================================================
# 9.7 Paràmetres de posició: quartils i percentils
# =====================================================================
E1 = [3, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 10]
assert five(E1) == (3, 5, Fr(13, 2), 8, 10) and pctl(E1, 90) == 9
DN = expand(NOT); FN = acc(NOT); assert FN == [2, 7, 13, 18, 22, 24, 25]
assert five(DN) == (4, 5, 6, 8, 10) and pctl(DN, 10) == 5 and pctl(DN, 90) == 9
ck(Fr(25, 4), '6.25'); ck(Fr(75, 4), '18.75'); ck(Fr(90 * 25, 100), '22.5'); ck(Fr(90 * 12, 100), '10.8')
s7 = box('def', L('Quartils i percentils', 'Cuartiles y percentiles', 'Quartiles and percentiles'),
  P(r"Els <strong>paràmetres de posició</strong> ens diuen quin lloc ocupa una dada dins del conjunt de dades <strong>ordenades</strong>. La mediana ja n'és un: deixa la meitat de les dades per davall i l'altra meitat per damunt.",
    r"Los <strong>parámetros de posición</strong> nos dicen qué lugar ocupa un dato dentro del conjunto de datos <strong>ordenados</strong>. La mediana ya es uno: deja la mitad de los datos por debajo y la otra mitad por encima.",
    r"<strong>Measures of position</strong> tell us where a value stands within the data <strong>in order</strong>. The median is already one: it has half the data below it and half above.")
  + ul(L(r"Els <strong>quartils</strong> divideixen les dades ordenades en <strong>quatre parts</strong> amb el mateix nombre de dades: \(Q_1\) deixa per davall el \(25\ \%\) de les dades; \(Q_2=Me\), el \(50\ \%\), i \(Q_3\), el \(75\ \%\).",
         r"Los <strong>cuartiles</strong> dividen los datos ordenados en <strong>cuatro partes</strong> con el mismo número de datos: \(Q_1\) deja por debajo el \(25\ \%\) de los datos; \(Q_2=Me\), el \(50\ \%\), y \(Q_3\), el \(75\ \%\).",
         r"The <strong>quartiles</strong> split the ordered data into <strong>four parts</strong> with the same number of values: \(Q_1\) has \(25\ \%\) of the data below it; \(Q_2=Me\), \(50\ \%\), and \(Q_3\), \(75\ \%\)."),
       L(r"Els <strong>percentils</strong> les divideixen en <strong>cent parts</strong>: el percentil \(P_k\) deixa per davall el \(k\ \%\) de les dades. Així, \(Q_1=P_{25}\), \(Me=P_{50}\) i \(Q_3=P_{75}\).",
         r"Los <strong>percentiles</strong> los dividen en <strong>cien partes</strong>: el percentil \(P_k\) deja por debajo el \(k\ \%\) de los datos. Así, \(Q_1=P_{25}\), \(Me=P_{50}\) y \(Q_3=P_{75}\).",
         r"<strong>Percentiles</strong> split them into <strong>a hundred parts</strong>: the percentile \(P_k\) has \(k\ \%\) of the data below it. So \(Q_1=P_{25}\), \(Me=P_{50}\) and \(Q_3=P_{75}\)."),
       L(r"El <strong>rang interquartílic</strong> és \(RI=Q_3-Q_1\): l'amplària on hi ha el \(50\ \%\) central de les dades. És una mesura de dispersió que <strong>no</strong> es veu afectada per les dades extremes.",
         r"El <strong>rango intercuartílico</strong> es \(RI=Q_3-Q_1\): la anchura donde está el \(50\ \%\) central de los datos. Es una medida de dispersión que <strong>no</strong> se ve afectada por los datos extremos.",
         r"The <strong>interquartile range</strong> is \(IQR=Q_3-Q_1\): the width that holds the middle \(50\ \%\) of the data. It's a measure of spread that is <strong>not</strong> affected by extreme values."))
  + note(r"Els percentils es fan servir molt en medicina: si un nadó està en el <strong>percentil 80</strong> de pes, vol dir que pesa més que el \(80\ \%\) dels nadons de la seua edat (i menys que el \(20\ \%\)).",
         r"Los percentiles se usan mucho en medicina: si un bebé está en el <strong>percentil 80</strong> de peso, quiere decir que pesa más que el \(80\ \%\) de los bebés de su edad (y menos que el \(20\ \%\)).",
         r"Percentiles are widely used in medicine: if a baby is on the <strong>80th percentile</strong> for weight, it weighs more than \(80\ \%\) of babies its age (and less than \(20\ \%\))."))
s7 += box('prop', L('Com es calculen?', '¿Cómo se calculan?', 'How do we find them?'),
  ol(L(r"<strong>Ordenem</strong> les \(N\) dades de menor a major.", r"<strong>Ordenamos</strong> los \(N\) datos de menor a mayor.", r"<strong>Put</strong> the \(N\) values in order from smallest to largest."),
     L(r"Calculem la <strong>posició</strong> \(\dfrac{k\cdot N}{100}\) (per a \(Q_1\), \(\frac N4\); per a \(Q_3\), \(\frac{3N}4\)).", r"Calculamos la <strong>posición</strong> \(\dfrac{k\cdot N}{100}\) (para \(Q_1\), \(\frac N4\); para \(Q_3\), \(\frac{3N}4\)).", r"Work out the <strong>position</strong> \(\dfrac{k\cdot N}{100}\) (for \(Q_1\), \(\frac N4\); for \(Q_3\), \(\frac{3N}4\))."),
     L(r"Si la posició <strong>no és entera</strong>, \(P_k\) és la dada de la posició següent (arrodonim cap amunt). Si <strong>és entera</strong>, \(P_k\) és la mitjana de la dada d'eixa posició i la següent. És el mateix que fem amb la mediana.",
       r"Si la posición <strong>no es entera</strong>, \(P_k\) es el dato de la posición siguiente (redondeamos hacia arriba). Si <strong>es entera</strong>, \(P_k\) es la media del dato de esa posición y el siguiente. Es lo mismo que hacemos con la mediana.",
       r"If the position is <strong>not a whole number</strong>, \(P_k\) is the value in the next position (round up). If it <strong>is a whole number</strong>, \(P_k\) is the mean of the value in that position and the next. It's what we already do for the median."))
  + box('ex', L('Exemple: dades soltes', 'Ejemplo: datos sueltos', 'Example: raw data'),
        P(r"Notes de 12 alumnes, ja ordenades:", r"Notas de 12 alumnos, ya ordenadas:", r"Marks of 12 students, already in order:") + poscell(E1)
        + ul(L(r"\(Q_1\): \(\frac{12}{4}=3\) és entera → mitjana de la 3a i la 4a dada: \(Q_1=\frac{5+5}{2}=5\).", r"\(Q_1\): \(\frac{12}{4}=3\) es entera → media del 3.º y el 4.º dato: \(Q_1=\frac{5+5}{2}=5\).", r"\(Q_1\): \(\frac{12}{4}=3\) is whole → mean of the 3rd and 4th values: \(Q_1=\frac{5+5}{2}=5\)."),
             L(r"\(Me\): \(\frac{12}{2}=6\) → mitjana de la 6a i la 7a: \(Me=\frac{6+7}{2}=6\dc 5\).", r"\(Me\): \(\frac{12}{2}=6\) → media del 6.º y el 7.º: \(Me=\frac{6+7}{2}=6\dc 5\).", r"\(Me\): \(\frac{12}{2}=6\) → mean of the 6th and 7th: \(Me=\frac{6+7}{2}=6\dc 5\)."),
             L(r"\(Q_3\): \(\frac{3\cdot12}{4}=9\) → mitjana de la 9a i la 10a: \(Q_3=\frac{8+8}{2}=8\). &nbsp; \(RI=8-5=3\).", r"\(Q_3\): \(\frac{3\cdot12}{4}=9\) → media del 9.º y el 10.º: \(Q_3=\frac{8+8}{2}=8\). &nbsp; \(RI=8-5=3\).", r"\(Q_3\): \(\frac{3\cdot12}{4}=9\) → mean of the 9th and 10th: \(Q_3=\frac{8+8}{2}=8\). &nbsp; \(IQR=8-5=3\)."),
             L(r"\(P_{90}\): \(\frac{90\cdot12}{100}=10\dc 8\), no és entera → la dada 11a: \(P_{90}=9\).", r"\(P_{90}\): \(\frac{90\cdot12}{100}=10\dc 8\), no es entera → el dato 11.º: \(P_{90}=9\).", r"\(P_{90}\): \(\frac{90\cdot12}{100}=10\dc 8\), not whole → the 11th value: \(P_{90}=9\).")))
  + box('ex', L('Exemple: amb una taula de freqüències', 'Ejemplo: con una tabla de frecuencias', 'Example: from a frequency table'),
        P(r"Amb la taula de les notes de 25 alumnes (apartat 9.2) busquem en la columna \(F_i\) el <strong>primer valor que arriba a la posició</strong>. Si una \(F_i\) coincideix exactament amb la posició, fem la mitjana d'eixe valor i el següent.",
          r"Con la tabla de las notas de 25 alumnos (apartado 9.2) buscamos en la columna \(F_i\) el <strong>primer valor que llega a la posición</strong>. Si una \(F_i\) coincide exactamente con la posición, hacemos la media de ese valor y el siguiente.",
          r"With the table of the 25 students' marks (section 9.2) we look down the \(F_i\) column for the <strong>first value that reaches the position</strong>. If an \(F_i\) equals the position exactly, take the mean of that value and the next.")
        + '<div class="tv2">' + ftabq(NOT) + ul(
            L(r"\(Q_1\): \(\frac{25}{4}=6\dc 25\). La primera \(F_i\geq6\dc 25\) és \(7\): \(Q_1=5\).", r"\(Q_1\): \(\frac{25}{4}=6\dc 25\). La primera \(F_i\geq6\dc 25\) es \(7\): \(Q_1=5\).", r"\(Q_1\): \(\frac{25}{4}=6\dc 25\). The first \(F_i\geq6\dc 25\) is \(7\): \(Q_1=5\)."),
            L(r"\(Me\): \(\frac{25}{2}=12\dc 5\) → \(F=13\): \(Me=6\).", r"\(Me\): \(\frac{25}{2}=12\dc 5\) → \(F=13\): \(Me=6\).", r"\(Me\): \(\frac{25}{2}=12\dc 5\) → \(F=13\): \(Me=6\)."),
            L(r"\(Q_3\): \(\frac{75}{4}=18\dc 75\) → \(F=22\): \(Q_3=8\).", r"\(Q_3\): \(\frac{75}{4}=18\dc 75\) → \(F=22\): \(Q_3=8\).", r"\(Q_3\): \(\frac{75}{4}=18\dc 75\) → \(F=22\): \(Q_3=8\)."),
            L(r"\(P_{90}\): \(\frac{90\cdot25}{100}=22\dc 5\) → \(F=24\): \(P_{90}=9\). El \(90\ \%\) ha tret un 9 o menys.", r"\(P_{90}\): \(\frac{90\cdot25}{100}=22\dc 5\) → \(F=24\): \(P_{90}=9\). El \(90\ \%\) ha sacado un 9 o menos.", r"\(P_{90}\): \(\frac{90\cdot25}{100}=22\dc 5\) → \(F=24\): \(P_{90}=9\). \(90\ \%\) got 9 or less.")) + '</div>')
  + note(r"Amb dades agrupades, el quartil o percentil és dins del <strong>primer interval amb \(F_i\geq\frac{k\cdot N}{100}\)</strong>, igual que l'interval medià. Per exemple, amb els diners de 40 alumnes (apartat 9.3), \(\frac{40}{4}=10\): \(Q_1\) és en \([5,\ 10)\); \(\frac{3\cdot40}{4}=30\): \(Q_3\) és en \([15,\ 20)\).",
         r"Con datos agrupados, el cuartil o percentil está dentro del <strong>primer intervalo con \(F_i\geq\frac{k\cdot N}{100}\)</strong>, igual que el intervalo mediano. Por ejemplo, con el dinero de 40 alumnos (apartado 9.3), \(\frac{40}{4}=10\): \(Q_1\) está en \([5,\ 10)\); \(\frac{3\cdot40}{4}=30\): \(Q_3\) está en \([15,\ 20)\).",
         r"With grouped data, the quartile or percentile lies in the <strong>first interval with \(F_i\geq\frac{k\cdot N}{100}\)</strong>, just like the median class. For example, with the money of 40 students (section 9.3), \(\frac{40}{4}=10\): \(Q_1\) is in \([5,\ 10)\); \(\frac{3\cdot40}{4}=30\): \(Q_3\) is in \([15,\ 20)\)."))
assert FDIN == [6, 16, 28, 36, 40]
s7 += (widget('w-quart', '📍', L('Quartils i percentils pas a pas', 'Cuartiles y percentiles paso a paso', 'Quartiles and percentiles step by step'),
              ['<p class="hint-s">' + L("Escriu les dades separades per espais i tria el percentil amb el control lliscant. L'eina ordena les dades, calcula la posició i encercla les dades que fa servir.",
                                        "Escribe los datos separados por espacios y elige el percentil con el control deslizante. La herramienta ordena los datos, calcula la posición y rodea los datos que usa.",
                                        "Type the data separated by spaces and choose the percentile with the slider. The tool sorts the data, works out the position and circles the values it uses.") + '</p>',
               '<div class="wrow">' + tin('d', L('Dades', 'Datos', 'Data'), '7 3 8 5 10 6 9 4 8 6 5 7', 'w') + '</div>',
               '<div class="wrow">' + rng('k', 1, 99, 1, 90, 'k') + '</div>'], out='<div class="tout"></div>')
       + drill('quart', 'Entrena: calcula un quartil', 'Entrena: calcula un cuartil', 'Train: find a quartile')
       + drill('perc', 'Entrena: un percentil des d’una taula', 'Entrena: un percentil desde una tabla', 'Train: a percentile from a table'))

L71 = [2, 4, 4, 5, 7, 8, 9, 10, 12]; assert five(L71) == (2, 4, 7, 9, 12)
CAL = [(36, 3), (37, 5), (38, 8), (39, 6), (40, 2)]; DC = expand(CAL); assert acc(CAL) == [3, 8, 16, 22, 24]
assert five(DC) == (36, 37, 38, 39, 40) and pctl(DC, 10) == 36 and pctl(DC, 95) == 40
ck(Fr(10 * 24, 100), '2.4'); ck(Fr(95 * 24, 100), '22.8')
T16 = [18, 25, 21, 30, 24, 19, 27, 22, 35, 26, 20, 23, 28, 31, 24, 29]
assert five(T16) == (18, Fr(43, 2), Fr(49, 2), Fr(57, 2), 35); ck(Fr(57, 2) - Fr(43, 2), 7)
ck(Fr(18, 25) * 100, 72); ck(Fr(20 * 30, 100), 6)
s7 += levels(
 [prob(L(r"Calcula els quartils i el rang interquartílic de les dades \(5,\ 9,\ 2,\ 12,\ 4,\ 8,\ 10,\ 4,\ 7\).", r"Calcula los cuartiles y el rango intercuartílico de los datos \(5,\ 9,\ 2,\ 12,\ 4,\ 8,\ 10,\ 4,\ 7\).", r"Find the quartiles and the interquartile range of the data \(5,\ 9,\ 2,\ 12,\ 4,\ 8,\ 10,\ 4,\ 7\)."),
       P(r"Ordenem les \(N=9\) dades:", r"Ordenamos los \(N=9\) datos:", r"Put the \(N=9\) values in order:") + poscell(L71),
       P(r"\(\frac94=2\dc 25\to\) 3a dada: \(\boxed{Q_1=4}\). &nbsp; \(\frac92=4\dc 5\to\) 5a: \(\boxed{Me=7}\). &nbsp; \(\frac{27}{4}=6\dc 75\to\) 7a: \(\boxed{Q_3=9}\). &nbsp; \(RI=9-4=\boxed{5}\).",
         r"\(\frac94=2\dc 25\to\) 3.er dato: \(\boxed{Q_1=4}\). &nbsp; \(\frac92=4\dc 5\to\) 5.º: \(\boxed{Me=7}\). &nbsp; \(\frac{27}{4}=6\dc 75\to\) 7.º: \(\boxed{Q_3=9}\). &nbsp; \(RI=9-4=\boxed{5}\).",
         r"\(\frac94=2\dc 25\to\) 3rd value: \(\boxed{Q_1=4}\). &nbsp; \(\frac92=4\dc 5\to\) 5th: \(\boxed{Me=7}\). &nbsp; \(\frac{27}{4}=6\dc 75\to\) 7th: \(\boxed{Q_3=9}\). &nbsp; \(IQR=9-4=\boxed{5}\).")),
  prob(L(r"Laia està en el percentil 85 de l'alçada de la seua classe i Marc, en el quartil 1. Què vol dir? Qui és més alt?", r"Laia está en el percentil 85 de la altura de su clase y Marc, en el cuartil 1. ¿Qué quiere decir? ¿Quién es más alto?", r"Laia is on the 85th percentile for height in her class and Marc is at the first quartile. What does that mean? Who is taller?"),
       P(r"Laia és més alta que el \(85\ \%\) de la classe (i només un \(15\ \%\) la supera). Marc és més alt que el \(25\ \%\) i més baix que el \(75\ \%\). <strong>Laia és més alta.</strong>",
         r"Laia es más alta que el \(85\ \%\) de la clase (y solo un \(15\ \%\) la supera). Marc es más alto que el \(25\ \%\) y más bajo que el \(75\ \%\). <strong>Laia es más alta.</strong>",
         r"Laia is taller than \(85\ \%\) of the class (only \(15\ \%\) are taller). Marc is taller than \(25\ \%\) and shorter than \(75\ \%\). <strong>Laia is taller.</strong>"))],
 [prob(L(r"Aquesta taula recull el número de calçat de 24 alumnes. Calcula els quartils i els percentils 10 i 95.", r"Esta tabla recoge el número de calzado de 24 alumnos. Calcula los cuartiles y los percentiles 10 y 95.", r"This table shows the shoe size of 24 students. Find the quartiles and the 10th and 95th percentiles.")
       + tbl([L('Número', 'Número', 'Size')] + [str(x) for x, _ in CAL], [[M('f_i')] + [str(f) for _, f in CAL]], 'c'),
       ftabq(CAL),
       P(r"\(\frac{24}{4}=6\to F=8\): \(\boxed{Q_1=37}\). &nbsp; \(12\to F=16\): \(\boxed{Me=38}\). &nbsp; \(18\to F=22\): \(\boxed{Q_3=39}\). &nbsp; \(\frac{10\cdot24}{100}=2\dc 4\to F=3\): \(\boxed{P_{10}=36}\). &nbsp; \(\frac{95\cdot24}{100}=22\dc 8\to F=24\): \(\boxed{P_{95}=40}\).",
         r"\(\frac{24}{4}=6\to F=8\): \(\boxed{Q_1=37}\). &nbsp; \(12\to F=16\): \(\boxed{Me=38}\). &nbsp; \(18\to F=22\): \(\boxed{Q_3=39}\). &nbsp; \(\frac{10\cdot24}{100}=2\dc 4\to F=3\): \(\boxed{P_{10}=36}\). &nbsp; \(\frac{95\cdot24}{100}=22\dc 8\to F=24\): \(\boxed{P_{95}=40}\).",
         r"\(\frac{24}{4}=6\to F=8\): \(\boxed{Q_1=37}\). &nbsp; \(12\to F=16\): \(\boxed{Me=38}\). &nbsp; \(18\to F=22\): \(\boxed{Q_3=39}\). &nbsp; \(\frac{10\cdot24}{100}=2\dc 4\to F=3\): \(\boxed{P_{10}=36}\). &nbsp; \(\frac{95\cdot24}{100}=22\dc 8\to F=24\): \(\boxed{P_{95}=40}\).")),
  prob(L(r"Els temps (en minuts) que han tardat 16 corredors en una cursa són: \(18,\ 25,\ 21,\ 30,\ 24,\ 19,\ 27,\ 22,\ 35,\ 26,\ 20,\ 23,\ 28,\ 31,\ 24,\ 29\). Calcula els quartils i el rang interquartílic.",
         r"Los tiempos (en minutos) que han tardado 16 corredores en una carrera son: \(18,\ 25,\ 21,\ 30,\ 24,\ 19,\ 27,\ 22,\ 35,\ 26,\ 20,\ 23,\ 28,\ 31,\ 24,\ 29\). Calcula los cuartiles y el rango intercuartílico.",
         r"The times (in minutes) of 16 runners in a race are: \(18,\ 25,\ 21,\ 30,\ 24,\ 19,\ 27,\ 22,\ 35,\ 26,\ 20,\ 23,\ 28,\ 31,\ 24,\ 29\). Find the quartiles and the interquartile range."),
       poscell(T16),
       P(r"Les tres posicions són enteres (\(4\), \(8\) i \(12\)): \(Q_1=\frac{21+22}{2}=\boxed{21\dc 5}\); \(Me=\frac{24+25}{2}=\boxed{24\dc 5}\); \(Q_3=\frac{28+29}{2}=\boxed{28\dc 5}\) minuts; \(RI=\boxed{7}\) minuts.",
         r"Las tres posiciones son enteras (\(4\), \(8\) y \(12\)): \(Q_1=\frac{21+22}{2}=\boxed{21\dc 5}\); \(Me=\frac{24+25}{2}=\boxed{24\dc 5}\); \(Q_3=\frac{28+29}{2}=\boxed{28\dc 5}\) minutos; \(RI=\boxed{7}\) minutos.",
         r"All three positions are whole numbers (\(4\), \(8\) and \(12\)): \(Q_1=\frac{21+22}{2}=\boxed{21\dc 5}\); \(Me=\frac{24+25}{2}=\boxed{24\dc 5}\); \(Q_3=\frac{28+29}{2}=\boxed{28\dc 5}\) minutes; \(IQR=\boxed{7}\) minutes."))],
 [prob(L(r"Amb la taula de les notes de 25 alumnes (apartat 9.2), quin percentil correspon, aproximadament, a una nota de 7? Quina nota cal traure per a estar en el quartil 3 o per damunt?",
         r"Con la tabla de las notas de 25 alumnos (apartado 9.2), ¿qué percentil corresponde, aproximadamente, a una nota de 7? ¿Qué nota hay que sacar para estar en el cuartil 3 o por encima?",
         r"Using the table of the 25 students' marks (section 9.2), which percentile does a mark of 7 roughly correspond to? What mark do you need to be at the third quartile or above?"),
       P(r"Fins al 7 hi ha \(F=18\) alumnes de 25: \(\frac{18}{25}=0\dc 72\). Un 7 és, aproximadament, el <strong>percentil 72</strong>: el \(72\ \%\) ha tret un 7 o menys.",
         r"Hasta el 7 hay \(F=18\) alumnos de 25: \(\frac{18}{25}=0\dc 72\). Un 7 es, aproximadamente, el <strong>percentil 72</strong>: el \(72\ \%\) ha sacado un 7 o menos.",
         r"Up to 7 there are \(F=18\) students out of 25: \(\frac{18}{25}=0\dc 72\). A 7 is roughly the <strong>72nd percentile</strong>: \(72\ \%\) got 7 or less."),
       P(r"\(Q_3=8\): cal traure un <strong>8 o més</strong>.", r"\(Q_3=8\): hay que sacar un <strong>8 o más</strong>.", r"\(Q_3=8\): you need <strong>8 or more</strong>.")),
  prob(L(r"En una classe de 30 alumnes, quants tenen una nota per davall del percentil 20? I entre el quartil 1 i el quartil 3?", r"En una clase de 30 alumnos, ¿cuántos tienen una nota por debajo del percentil 20? ¿Y entre el cuartil 1 y el cuartil 3?", r"In a class of 30 students, how many have a mark below the 20th percentile? And between the first and third quartiles?"),
       P(r"Per davall del \(P_{20}\) queda, aproximadament, el \(20\ \%\): \(0\dc 2\cdot30=\boxed{6}\) alumnes. Entre \(Q_1\) i \(Q_3\) hi ha el \(50\ \%\) central: uns \(\boxed{15}\) alumnes.",
         r"Por debajo del \(P_{20}\) queda, aproximadamente, el \(20\ \%\): \(0\dc 2\cdot30=\boxed{6}\) alumnos. Entre \(Q_1\) y \(Q_3\) está el \(50\ \%\) central: unos \(\boxed{15}\) alumnos.",
         r"Roughly \(20\ \%\) are below \(P_{20}\): \(0\dc 2\cdot30=\boxed{6}\) students. Between \(Q_1\) and \(Q_3\) lies the middle \(50\ \%\): about \(\boxed{15}\) students."))])
s7 += practice([('★☆☆', L(r"Calcula \(Q_1\), \(Me\) i \(Q_3\) de \(1,\ 3,\ 3,\ 4,\ 6,\ 7,\ 8,\ 8,\ 9,\ 11\).", r"Calcula \(Q_1\), \(Me\) y \(Q_3\) de \(1,\ 3,\ 3,\ 4,\ 6,\ 7,\ 8,\ 8,\ 9,\ 11\).", r"Find \(Q_1\), \(Me\) and \(Q_3\) of \(1,\ 3,\ 3,\ 4,\ 6,\ 7,\ 8,\ 8,\ 9,\ 11\).")),
                ('★★☆', L(r"En la taula \(x_i\): 0, 1, 2, 3; \(f_i\): 5, 8, 4, 3, calcula \(P_{40}\) i \(P_{80}\).", r"En la tabla \(x_i\): 0, 1, 2, 3; \(f_i\): 5, 8, 4, 3, calcula \(P_{40}\) y \(P_{80}\).", r"In the table \(x_i\): 0, 1, 2, 3; \(f_i\): 5, 8, 4, 3, find \(P_{40}\) and \(P_{80}\)."))],
               L(r"1) \(N=10\): \(\frac{10}4=2\dc 5\to\) 3a: \(Q_1=3\); \(Me=\frac{6+7}{2}=6\dc 5\); \(7\dc 5\to\) 8a: \(Q_3=8\). &nbsp; 2) \(N=20\), \(F_i\): 5, 13, 17, 20. \(P_{40}\): posició 8 → \(F=13\): \(P_{40}=1\). \(P_{80}\): posició 16 → \(F=17\): \(P_{80}=2\).",
                 r"1) \(N=10\): \(\frac{10}4=2\dc 5\to\) 3.º: \(Q_1=3\); \(Me=\frac{6+7}{2}=6\dc 5\); \(7\dc 5\to\) 8.º: \(Q_3=8\). &nbsp; 2) \(N=20\), \(F_i\): 5, 13, 17, 20. \(P_{40}\): posición 8 → \(F=13\): \(P_{40}=1\). \(P_{80}\): posición 16 → \(F=17\): \(P_{80}=2\).",
                 r"1) \(N=10\): \(\frac{10}4=2\dc 5\to\) 3rd: \(Q_1=3\); \(Me=\frac{6+7}{2}=6\dc 5\); \(7\dc 5\to\) 8th: \(Q_3=8\). &nbsp; 2) \(N=20\), \(F_i\): 5, 13, 17, 20. \(P_{40}\): position 8 → \(F=13\): \(P_{40}=1\). \(P_{80}\): position 16 → \(F=17\): \(P_{80}=2\)."))
PR1 = [1, 3, 3, 4, 6, 7, 8, 8, 9, 11]; assert five(PR1)[1:4] == (3, Fr(13, 2), 8)
PR2 = expand([(0, 5), (1, 8), (2, 4), (3, 3)]); assert pctl(PR2, 40) == 1 and pctl(PR2, 80) == 2

# =====================================================================
# 9.8 Diagrama de caixes
# =====================================================================
F5N = five(DN)
BX_NOT = caixes([('', F5N)], 3, 11, 1, lab=Ls('nota', 'nota', 'mark'))
CA = [4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 9, 9]; CB = [2, 3, 4, 5, 6, 7, 7, 8, 9, 10, 10, 10]
assert five(CA) == (4, Fr(11, 2), 7, 8, 9) and five(CB) == (2, Fr(9, 2), 7, Fr(19, 2), 10) and mean(CA) == mean(CB) == Fr(27, 4)
BX_AB = caixes([('A', five(CA)), ('B', five(CB))], 1, 11, 1, lab=Ls('nota', 'nota', 'mark'))
s8 = box('def', L('El diagrama de caixes', 'El diagrama de cajas', 'The box plot'),
  P(r"El <strong>diagrama de caixes</strong> (o de caixa i bigotis) resumeix la distribució de les dades amb cinc nombres: el <strong>mínim</strong>, \(Q_1\), la <strong>mediana</strong>, \(Q_3\) i el <strong>màxim</strong>. Per a dibuixar-lo:",
    r"El <strong>diagrama de cajas</strong> (o de caja y bigotes) resume la distribución de los datos con cinco números: el <strong>mínimo</strong>, \(Q_1\), la <strong>mediana</strong>, \(Q_3\) y el <strong>máximo</strong>. Para dibujarlo:",
    r"The <strong>box plot</strong> (or box-and-whisker plot) sums up the distribution of the data with five numbers: the <strong>minimum</strong>, \(Q_1\), the <strong>median</strong>, \(Q_3\) and the <strong>maximum</strong>. To draw it:")
  + ol(L(r"dibuixem una <strong>escala</strong> horitzontal que arreplegue totes les dades;", r"dibujamos una <strong>escala</strong> horizontal que recoja todos los datos;", r"draw a horizontal <strong>scale</strong> that covers all the data;"),
       L(r"fem una <strong>caixa</strong> des de \(Q_1\) fins a \(Q_3\) i hi marquem la <strong>mediana</strong> amb una línia;", r"hacemos una <strong>caja</strong> desde \(Q_1\) hasta \(Q_3\) y marcamos la <strong>mediana</strong> con una línea;", r"draw a <strong>box</strong> from \(Q_1\) to \(Q_3\) and mark the <strong>median</strong> with a line;"),
       L(r"dibuixem els <strong>bigotis</strong>: dos segments des de la caixa fins al mínim i fins al màxim.", r"dibujamos los <strong>bigotes</strong>: dos segmentos desde la caja hasta el mínimo y hasta el máximo.", r"draw the <strong>whiskers</strong>: two segments from the box to the minimum and to the maximum."))
  + box('ex', L('Exemple: les notes de 25 alumnes', 'Ejemplo: las notas de 25 alumnos', 'Example: the marks of 25 students'),
        P(r"Amb els paràmetres de l'apartat 9.7: mínim \(4\), \(Q_1=5\), \(Me=6\), \(Q_3=8\), màxim \(10\).", r"Con los parámetros del apartado 9.7: mínimo \(4\), \(Q_1=5\), \(Me=6\), \(Q_3=8\), máximo \(10\).", r"Using the measures from section 9.7: minimum \(4\), \(Q_1=5\), \(Me=6\), \(Q_3=8\), maximum \(10\).")
        + figs(fig(BX_NOT)))
  + P(r"Cadascuna de les quatre parts (bigoti, mitja caixa, mitja caixa, bigoti) conté aproximadament el <strong>\(25\ \%\) de les dades</strong>. La longitud de la caixa és el rang interquartílic i la longitud total, el rang.",
      r"Cada una de las cuatro partes (bigote, media caja, media caja, bigote) contiene aproximadamente el <strong>\(25\ \%\) de los datos</strong>. La longitud de la caja es el rango intercuartílico y la longitud total, el rango.",
      r"Each of the four parts (whisker, half-box, half-box, whisker) holds roughly <strong>\(25\ \%\) of the data</strong>. The length of the box is the interquartile range and the total length is the range."))
s8 += box('prop', L('Com s’interpreta?', '¿Cómo se interpreta?', 'How do we read it?'),
  ul(L(r"Una part <strong>curta</strong> vol dir que eixe \(25\ \%\) de les dades està molt <strong>concentrat</strong>; una part <strong>llarga</strong>, que està <strong>escampat</strong>. En l'exemple, les notes entre 5 i 6 estan molt juntes i les de 6 a 10, més escampades.",
       r"Una parte <strong>corta</strong> quiere decir que ese \(25\ \%\) de los datos está muy <strong>concentrado</strong>; una parte <strong>larga</strong>, que está <strong>esparcido</strong>. En el ejemplo, las notas entre 5 y 6 están muy juntas y las de 6 a 10, más esparcidas.",
       r"A <strong>short</strong> part means that \(25\ \%\) of the data is tightly <strong>packed</strong>; a <strong>long</strong> part, that it's <strong>spread out</strong>. In the example, the marks between 5 and 6 are close together and those from 6 to 10 more spread out."),
     L(r"Si la mediana està al centre de la caixa i els bigotis són iguals, la distribució és <strong>simètrica</strong>. Si no, és <strong>asimètrica</strong> (cap al costat de la part més llarga).",
       r"Si la mediana está en el centro de la caja y los bigotes son iguales, la distribución es <strong>simétrica</strong>. Si no, es <strong>asimétrica</strong> (hacia el lado de la parte más larga).",
       r"If the median is in the middle of the box and the whiskers are equal, the distribution is <strong>symmetric</strong>. If not, it's <strong>skewed</strong> (towards the longer side)."),
     L(r"Els diagrames de caixes són molt útils per a <strong>comparar</strong> dos o més grups: es dibuixen un damunt de l'altre amb la mateixa escala.",
       r"Los diagramas de cajas son muy útiles para <strong>comparar</strong> dos o más grupos: se dibujan uno encima del otro con la misma escala.",
       r"Box plots are very useful for <strong>comparing</strong> two or more groups: they're drawn one above the other on the same scale."))
  + box('ex', L('Exemple: dues classes', 'Ejemplo: dos clases', 'Example: two classes'),
        P(r"Notes de dues classes de 12 alumnes. Totes dues tenen la mateixa mitjana (\(6\dc 75\)) i la mateixa mediana (7):", r"Notas de dos clases de 12 alumnos. Las dos tienen la misma media (\(6\dc 75\)) y la misma mediana (7):", r"Marks of two classes of 12 students. Both have the same mean (\(6\dc 75\)) and the same median (7):")
        + figs(fig(BX_AB))
        + P(r"La caixa de B és el doble de llarga (\(RI_B=9\dc 5-4\dc 5=5\)) que la d'A (\(RI_A=8-5\dc 5=2\dc 5\)): les notes de la classe A són molt més <strong>homogènies</strong>. A la classe B hi ha notes molt baixes i molt altes.",
            r"La caja de B es el doble de larga (\(RI_B=9\dc 5-4\dc 5=5\)) que la de A (\(RI_A=8-5\dc 5=2\dc 5\)): las notas de la clase A son mucho más <strong>homogéneas</strong>. En la clase B hay notas muy bajas y muy altas.",
            r"B's box is twice as long (\(IQR_B=9\dc 5-4\dc 5=5\)) as A's (\(IQR_A=8-5\dc 5=2\dc 5\)): class A's marks are much more <strong>consistent</strong>. Class B has some very low and some very high marks.")))
ck(Fr(19, 2) - Fr(9, 2), 5); ck(8 - Fr(11, 2), '2.5')
OUT = [12, 14, 15, 15, 16, 17, 18, 19, 35]; assert five(OUT) == (12, 15, 16, 18, 35)
ck(18 - 15, 3); ck(15 - Fr(3, 2) * 3, '10.5'); ck(18 + Fr(3, 2) * 3, '22.5')
s8 += box('prop', L('Per a saber-ne més: valors atípics', 'Para saber más: valores atípicos', 'Going further: outliers'),
  P(r"Una dada molt allunyada de les altres s'anomena <strong>valor atípic</strong>. Se sol considerar atípica una dada menor que \(Q_1-1\dc 5\cdot RI\) o major que \(Q_3+1\dc 5\cdot RI\). Molts programes i calculadores la dibuixen com un punt solt i allarguen el bigoti només fins a l'última dada que no és atípica.",
    r"Un dato muy alejado de los demás se llama <strong>valor atípico</strong>. Se suele considerar atípico un dato menor que \(Q_1-1\dc 5\cdot RI\) o mayor que \(Q_3+1\dc 5\cdot RI\). Muchos programas y calculadoras lo dibujan como un punto suelto y alargan el bigote solo hasta el último dato que no es atípico.",
    r"A value far away from the rest is called an <strong>outlier</strong>. A value is usually considered an outlier if it's less than \(Q_1-1\dc 5\cdot IQR\) or greater than \(Q_3+1\dc 5\cdot IQR\). Many programs and calculators draw it as a separate dot and only extend the whisker to the last value that isn't an outlier.")
  + P(r"Per exemple, en \(12,\ 14,\ 15,\ 15,\ 16,\ 17,\ 18,\ 19,\ 35\): \(Q_1=15\), \(Q_3=18\), \(RI=3\). Els límits són \(15-4\dc 5=10\dc 5\) i \(18+4\dc 5=22\dc 5\): el <strong>35 és un valor atípic</strong>.",
      r"Por ejemplo, en \(12,\ 14,\ 15,\ 15,\ 16,\ 17,\ 18,\ 19,\ 35\): \(Q_1=15\), \(Q_3=18\), \(RI=3\). Los límites son \(15-4\dc 5=10\dc 5\) y \(18+4\dc 5=22\dc 5\): el <strong>35 es un valor atípico</strong>.",
      r"For example, in \(12,\ 14,\ 15,\ 15,\ 16,\ 17,\ 18,\ 19,\ 35\): \(Q_1=15\), \(Q_3=18\), \(IQR=3\). The limits are \(15-4\dc 5=10\dc 5\) and \(18+4\dc 5=22\dc 5\): <strong>35 is an outlier</strong>."))
s8 += (widget('w-box', '📦', L('Construeix i compara diagrames de caixes', 'Construye y compara diagramas de cajas', 'Build and compare box plots'),
              ['<p class="hint-s">' + L("Escriu un o dos grups de dades (deixa B en blanc si només en vols un). L'eina calcula els cinc nombres de cada grup i dibuixa les caixes amb la mateixa escala.",
                                        "Escribe uno o dos grupos de datos (deja B en blanco si solo quieres uno). La herramienta calcula los cinco números de cada grupo y dibuja las cajas con la misma escala.",
                                        "Type one or two sets of data (leave B blank if you only want one). The tool works out each set's five numbers and draws the boxes on the same scale.") + '</p>',
               '<div class="wrow">' + tin('a', 'A', ' '.join(map(str, CA)), 'w') + '</div><div class="wrow">' + tin('b', 'B', ' '.join(map(str, CB)), 'w') + '</div>'], out='<div class="tout"></div>')
       + drill('boxread', 'Entrena: llig el diagrama de caixes', 'Entrena: lee el diagrama de cajas', 'Train: read the box plot')
       + drill('boxpct', 'Entrena: quin percentatge de les dades?', 'Entrena: ¿qué porcentaje de los datos?', 'Train: what percentage of the data?', 'opts'))

BX_L71 = caixes([('', five(L71))], 0, 14, 2)
RD = (10, 14, 17, 22, 30)
BX_RD = caixes([('', RD)], 8, 32, 2, lab='min')
RA = [21, 23, 24, 25, 26, 26, 27, 28, 29, 31]; RB = [18, 20, 22, 24, 27, 28, 30, 33, 36, 40]
assert five(RA) == (21, 24, 26, 28, 31) and five(RB) == (18, 22, Fr(55, 2), 33, 40)
BX_R = caixes([('A', five(RA)), ('B', five(RB))], 16, 42, 2, lab='min')
B8 = [2, 3, 5, 5, 7, 7, 7, 10]; assert five(B8) == (2, 4, 6, 7, 10)
BX_CAL = caixes([('', five(DC))], 35, 41, 1)
s8 += levels(
 [prob(L(r"Dibuixa el diagrama de caixes de les dades \(5,\ 9,\ 2,\ 12,\ 4,\ 8,\ 10,\ 4,\ 7\) (apartat 9.7, nivell 1).", r"Dibuja el diagrama de cajas de los datos \(5,\ 9,\ 2,\ 12,\ 4,\ 8,\ 10,\ 4,\ 7\) (apartado 9.7, nivel 1).", r"Draw the box plot of the data \(5,\ 9,\ 2,\ 12,\ 4,\ 8,\ 10,\ 4,\ 7\) (section 9.7, level 1)."),
       P(r"Els cinc nombres: mínim \(2\), \(Q_1=4\), \(Me=7\), \(Q_3=9\), màxim \(12\).", r"Los cinco números: mínimo \(2\), \(Q_1=4\), \(Me=7\), \(Q_3=9\), máximo \(12\).", r"The five numbers: minimum \(2\), \(Q_1=4\), \(Me=7\), \(Q_3=9\), maximum \(12\).") + figs(fig(BX_L71))),
  prob(L(r"Aquest diagrama de caixes representa els minuts que tarden 200 alumnes a arribar a l'institut. Troba el rang i el rang interquartílic. Quants alumnes tarden més de 22 minuts? I entre 14 i 30 minuts?",
         r"Este diagrama de cajas representa los minutos que tardan 200 alumnos en llegar al instituto. Encuentra el rango y el rango intercuartílico. ¿Cuántos alumnos tardan más de 22 minutos? ¿Y entre 14 y 30 minutos?",
         r"This box plot shows the minutes 200 students take to get to school. Find the range and the interquartile range. How many students take more than 22 minutes? And between 14 and 30 minutes?") + figs(fig(BX_RD)),
       P(r"Llegim: mínim 10, \(Q_1=14\), \(Me=17\), \(Q_3=22\), màxim 30. Rang \(=30-10=\boxed{20}\); \(RI=22-14=\boxed{8}\) minuts.", r"Leemos: mínimo 10, \(Q_1=14\), \(Me=17\), \(Q_3=22\), máximo 30. Rango \(=30-10=\boxed{20}\); \(RI=22-14=\boxed{8}\) minutos.", r"Reading off: minimum 10, \(Q_1=14\), \(Me=17\), \(Q_3=22\), maximum 30. Range \(=30-10=\boxed{20}\); \(IQR=22-14=\boxed{8}\) minutes."),
       P(r"Per damunt de \(Q_3\) hi ha el \(25\ \%\): \(0\dc 25\cdot200=\boxed{50}\) alumnes. Entre \(Q_1\) i el màxim, el \(75\ \%\): \(\boxed{150}\) alumnes.", r"Por encima de \(Q_3\) está el \(25\ \%\): \(0\dc 25\cdot200=\boxed{50}\) alumnos. Entre \(Q_1\) y el máximo, el \(75\ \%\): \(\boxed{150}\) alumnos.", r"Above \(Q_3\) lie \(25\ \%\): \(0\dc 25\cdot200=\boxed{50}\) students. Between \(Q_1\) and the maximum, \(75\ \%\): \(\boxed{150}\) students."))],
 [prob(L(r"Dos grups de 10 corredors han fet aquests temps (en minuts). A: \(21,\ 23,\ 24,\ 25,\ 26,\ 26,\ 27,\ 28,\ 29,\ 31\); B: \(18,\ 20,\ 22,\ 24,\ 27,\ 28,\ 30,\ 33,\ 36,\ 40\). Dibuixa els dos diagrames de caixes i compara'ls.",
         r"Dos grupos de 10 corredores han hecho estos tiempos (en minutos). A: \(21,\ 23,\ 24,\ 25,\ 26,\ 26,\ 27,\ 28,\ 29,\ 31\); B: \(18,\ 20,\ 22,\ 24,\ 27,\ 28,\ 30,\ 33,\ 36,\ 40\). Dibuja los dos diagramas de cajas y compáralos.",
         r"Two groups of 10 runners recorded these times (in minutes). A: \(21,\ 23,\ 24,\ 25,\ 26,\ 26,\ 27,\ 28,\ 29,\ 31\); B: \(18,\ 20,\ 22,\ 24,\ 27,\ 28,\ 30,\ 33,\ 36,\ 40\). Draw both box plots and compare them."),
       P(r"\(N=10\): \(Q_1\) és la 3a dada, \(Q_3\) la 8a i \(Me\) la mitjana de la 5a i la 6a. A: \(21,\ 24,\ 26,\ 28,\ 31\). B: \(18,\ 22,\ 27\dc 5,\ 33,\ 40\).",
         r"\(N=10\): \(Q_1\) es el 3.er dato, \(Q_3\) el 8.º y \(Me\) la media del 5.º y el 6.º. A: \(21,\ 24,\ 26,\ 28,\ 31\). B: \(18,\ 22,\ 27\dc 5,\ 33,\ 40\).",
         r"\(N=10\): \(Q_1\) is the 3rd value, \(Q_3\) the 8th and \(Me\) the mean of the 5th and 6th. A: \(21,\ 24,\ 26,\ 28,\ 31\). B: \(18,\ 22,\ 27\dc 5,\ 33,\ 40\).") + figs(fig(BX_R)),
       P(r"Les medianes són semblants, però el grup B té molta més dispersió (\(RI_B=11\) i \(RI_A=4\)): hi ha corredors molt ràpids i molt lents. El grup A és més <strong>homogeni</strong>.",
         r"Las medianas son parecidas, pero el grupo B tiene mucha más dispersión (\(RI_B=11\) y \(RI_A=4\)): hay corredores muy rápidos y muy lentos. El grupo A es más <strong>homogéneo</strong>.",
         r"The medians are similar, but group B is much more spread out (\(IQR_B=11\) and \(IQR_A=4\)): there are some very fast and some very slow runners. Group A is more <strong>consistent</strong>.")),
  prob(L(r"Dibuixa el diagrama de caixes del número de calçat dels 24 alumnes (apartat 9.7, nivell 2). Per què la caixa és tan curta?", r"Dibuja el diagrama de cajas del número de calzado de los 24 alumnos (apartado 9.7, nivel 2). ¿Por qué la caja es tan corta?", r"Draw the box plot of the shoe sizes of the 24 students (section 9.7, level 2). Why is the box so short?"),
       P(r"Mínim 36, \(Q_1=37\), \(Me=38\), \(Q_3=39\), màxim 40:", r"Mínimo 36, \(Q_1=37\), \(Me=38\), \(Q_3=39\), máximo 40:", r"Minimum 36, \(Q_1=37\), \(Me=38\), \(Q_3=39\), maximum 40:") + figs(fig(BX_CAL)),
       P(r"La variable només pren cinc valors i molts alumnes en tenen el mateix: la meitat central està entre el 37 i el 39.", r"La variable solo toma cinco valores y muchos alumnos tienen el mismo: la mitad central está entre el 37 y el 39.", r"The variable only takes five values and many students share the same one: the middle half lies between 37 and 39."))],
 [prob(L(r"Comprova si hi ha valors atípics en les dades \(12,\ 14,\ 15,\ 15,\ 16,\ 17,\ 18,\ 19,\ 35\) i calcula la mitjana i la mediana. Quin dels dos paràmetres representa millor les dades?",
         r"Comprueba si hay valores atípicos en los datos \(12,\ 14,\ 15,\ 15,\ 16,\ 17,\ 18,\ 19,\ 35\) y calcula la media y la mediana. ¿Cuál de los dos parámetros representa mejor los datos?",
         r"Check whether there are any outliers in the data \(12,\ 14,\ 15,\ 15,\ 16,\ 17,\ 18,\ 19,\ 35\) and find the mean and the median. Which of the two represents the data better?"),
       P(r"\(Q_1=15\), \(Q_3=18\), \(RI=3\), \(1\dc 5\cdot RI=4\dc 5\). Límits: \(10\dc 5\) i \(22\dc 5\). El \(\boxed{35}\) és atípic.", r"\(Q_1=15\), \(Q_3=18\), \(RI=3\), \(1\dc 5\cdot RI=4\dc 5\). Límites: \(10\dc 5\) y \(22\dc 5\). El \(\boxed{35}\) es atípico.", r"\(Q_1=15\), \(Q_3=18\), \(IQR=3\), \(1\dc 5\cdot IQR=4\dc 5\). Limits: \(10\dc 5\) and \(22\dc 5\). \(\boxed{35}\) is an outlier."),
       D(r"\bar x=\frac{161}{9}\approx17\dc 89\qquad Me=16"),
       P(r"La mitjana s'acosta al valor atípic; la mediana no es mou. Ací la <strong>mediana</strong> representa millor les dades.", r"La media se acerca al valor atípico; la mediana no se mueve. Aquí la <strong>mediana</strong> representa mejor los datos.", r"The mean is pulled towards the outlier; the median isn't. Here the <strong>median</strong> represents the data better.")),
  prob(L(r"Inventa vuit dades que tinguen aquest resum: mínim 2, \(Q_1=4\), \(Me=6\), \(Q_3=7\), màxim 10.", r"Inventa ocho datos que tengan este resumen: mínimo 2, \(Q_1=4\), \(Me=6\), \(Q_3=7\), máximo 10.", r"Make up eight values with this summary: minimum 2, \(Q_1=4\), \(Me=6\), \(Q_3=7\), maximum 10."),
       P(r"Amb \(N=8\) les posicions 2, 4 i 6 són enteres: \(Q_1\) és la mitjana de la 2a i la 3a dada, \(Me\) de la 4a i la 5a i \(Q_3\) de la 6a i la 7a. Per exemple: \(\boxed{2,\ 3,\ 5,\ 5,\ 7,\ 7,\ 7,\ 10}\): \(Q_1=\frac{3+5}{2}=4\), \(Me=\frac{5+7}{2}=6\), \(Q_3=\frac{7+7}{2}=7\). Hi ha moltes altres solucions.",
         r"Con \(N=8\) las posiciones 2, 4 y 6 son enteras: \(Q_1\) es la media del 2.º y el 3.er dato, \(Me\) del 4.º y el 5.º y \(Q_3\) del 6.º y el 7.º. Por ejemplo: \(\boxed{2,\ 3,\ 5,\ 5,\ 7,\ 7,\ 7,\ 10}\): \(Q_1=\frac{3+5}{2}=4\), \(Me=\frac{5+7}{2}=6\), \(Q_3=\frac{7+7}{2}=7\). Hay muchas otras soluciones.",
         r"With \(N=8\) positions 2, 4 and 6 are whole numbers: \(Q_1\) is the mean of the 2nd and 3rd values, \(Me\) of the 4th and 5th and \(Q_3\) of the 6th and 7th. For example: \(\boxed{2,\ 3,\ 5,\ 5,\ 7,\ 7,\ 7,\ 10}\): \(Q_1=\frac{3+5}{2}=4\), \(Me=\frac{5+7}{2}=6\), \(Q_3=\frac{7+7}{2}=7\). There are many other answers."))])
ck(sum(OUT), 161); ckr(mean(OUT), '17.89'); ck(Fr(25, 100) * 200, 50); ck(28 - 24, 4); ck(33 - 22, 11)
s8 += practice([('★☆☆', L(r"Dibuixa el diagrama de caixes de \(1,\ 3,\ 3,\ 4,\ 6,\ 7,\ 8,\ 8,\ 9,\ 11\) (practica de l'apartat 9.7).", r"Dibuja el diagrama de cajas de \(1,\ 3,\ 3,\ 4,\ 6,\ 7,\ 8,\ 8,\ 9,\ 11\) (práctica del apartado 9.7).", r"Draw the box plot of \(1,\ 3,\ 3,\ 4,\ 6,\ 7,\ 8,\ 8,\ 9,\ 11\) (practice in section 9.7).")),
                ('★★☆', L(r"En un diagrama de caixes, \(Q_1=20\), \(Me=25\) i \(Q_3=40\). Les dades són simètriques? Quin percentatge de dades hi ha entre 20 i 40?", r"En un diagrama de cajas, \(Q_1=20\), \(Me=25\) y \(Q_3=40\). ¿Los datos son simétricos? ¿Qué porcentaje de datos hay entre 20 y 40?", r"In a box plot, \(Q_1=20\), \(Me=25\) and \(Q_3=40\). Are the data symmetric? What percentage of the data lies between 20 and 40?"))],
               L(r"1) Mínim 1, \(Q_1=3\), \(Me=6\dc 5\), \(Q_3=8\), màxim 11. &nbsp; 2) No: la mediana està molt més a prop de \(Q_1\) que de \(Q_3\) (asimètrica cap a la dreta). Entre \(Q_1\) i \(Q_3\) hi ha el \(50\ \%\).",
                 r"1) Mínimo 1, \(Q_1=3\), \(Me=6\dc 5\), \(Q_3=8\), máximo 11. &nbsp; 2) No: la mediana está mucho más cerca de \(Q_1\) que de \(Q_3\) (asimétrica hacia la derecha). Entre \(Q_1\) y \(Q_3\) está el \(50\ \%\).",
                 r"1) Minimum 1, \(Q_1=3\), \(Me=6\dc 5\), \(Q_3=8\), maximum 11. &nbsp; 2) No: the median is much closer to \(Q_1\) than to \(Q_3\) (skewed to the right). The middle \(50\ \%\) lies between \(Q_1\) and \(Q_3\)."))
