# Apartat 9.5 dels apunts de la Unitat 9 de 4t ESO Matemàtiques A (Estadística): paràmetres de centralització (moda,
# mitjana i mediana) amb dades soltes, en una taula i agrupades en intervals (interval modal i interval medià). Ajunta
# els apartats 10.6, 10.7 i 10.9 de ../1eso-t10 i hi afig les dades agrupades.
from comu import *
from s123 import TG, NOT, EDG, FA, ALT, DIN, FDIN, acc, ivl

def ttab(tab, xl=None):
    """taula amb xi, fi, Fi i xi·fi (i la fila de totals)"""
    N = sum(f for _, f in tab); F = acc(tab); S = sum(x * f for x, f in tab)
    rows = [[M(tn(x)), M(str(f)), M(str(Fi)), M(tn(x * f))] for (x, f), Fi in zip(tab, F)]
    rows.append(['<strong>Total</strong>', M('N=%d' % N), '', M(r'\textstyle\sum=%s' % tn(S))])
    return tbl([xl or M('x_i'), M('f_i'), M('F_i'), M(r'x_i\cdot f_i')], rows, 'c freq')

# =====================================================================
# 9.5 Paràmetres de centralització
# =====================================================================
LEC = [20, 40, 15, 46, 20, 30, 25]
assert mean(LEC) == 28 and median(LEC) == 25 and modes(LEC) == [20]
EV = [7, 9, 3, 8, 10, 6, 8, 5]
assert mean(EV) == 7 and median(EV) == Fr(15, 2) and modes(EV) == [8]
SAL = [1200, 1350, 1250, 5900, 1300]
assert mean(SAL) == 2200 and median(SAL) == 1300
F_LEC = dots(LEC, 10, 50, mean_=28, med=25, step=5, lab='min')
s5 = box('def', L('Paràmetres de centralització', 'Parámetros de centralización', 'Measures of central tendency'),
  P(r"Els <strong>paràmetres de centralització</strong> són nombres que resumeixen totes les dades en un sol valor «del mig», que les representa:",
    r"Los <strong>parámetros de centralización</strong> son números que resumen todos los datos en un solo valor «del medio», que los representa:",
    r"<strong>Measures of central tendency</strong> are numbers that sum up all the data in a single “middle” value that represents them:")
  + ul(L(r"La <strong>moda</strong> (\(Mo\)) és el valor que <strong>més es repeteix</strong>, el de freqüència més gran. Pot haver-hi més d'una moda. És l'únic paràmetre que serveix per a variables <strong>qualitatives</strong>.",
         r"La <strong>moda</strong> (\(Mo\)) es el valor que <strong>más se repite</strong>, el de frecuencia más grande. Puede haber más de una moda. Es el único parámetro que sirve para variables <strong>cualitativas</strong>.",
         r"The <strong>mode</strong> (\(Mo\)) is the value that <strong>appears most often</strong>, the one with the highest frequency. There can be more than one mode. It's the only measure that works for <strong>qualitative</strong> variables."),
       L(r"La <strong>mitjana</strong> (\(\bar x\)) és el resultat de <strong>sumar totes les dades i dividir</strong> entre el nombre de dades: \(\bar x=\dfrac{\text{suma de les dades}}{N}\).",
         r"La <strong>media</strong> (\(\bar x\)) es el resultado de <strong>sumar todos los datos y dividir</strong> entre el número de datos: \(\bar x=\dfrac{\text{suma de los datos}}{N}\).",
         r"The <strong>mean</strong> (\(\bar x\)) is what you get by <strong>adding up all the data and dividing</strong> by the number of data: \(\bar x=\dfrac{\text{sum of the data}}{N}\)."),
       L(r"La <strong>mediana</strong> (\(Me\)) és el valor que queda <strong>en el centre</strong> quan ordenem les dades de menor a major: la meitat de les dades són menors o iguals i l'altra meitat, majors o iguals.",
         r"La <strong>mediana</strong> (\(Me\)) es el valor que queda <strong>en el centro</strong> cuando ordenamos los datos de menor a mayor: la mitad de los datos son menores o iguales y la otra mitad, mayores o iguales.",
         r"The <strong>median</strong> (\(Me\)) is the value <strong>in the middle</strong> when the data are put in order from smallest to largest: half the data are less than or equal to it and half greater than or equal."))
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"Minuts que Laia ha llegit cada dia d'una setmana: \(20,\ 40,\ 15,\ 46,\ 20,\ 30,\ 25\).", r"Minutos que Laia ha leído cada día de una semana: \(20,\ 40,\ 15,\ 46,\ 20,\ 30,\ 25\).", r"Minutes Laia read each day of a week: \(20,\ 40,\ 15,\ 46,\ 20,\ 30,\ 25\).")
        + ul(L(r"Moda: el 20 apareix dues vegades i els altres, una: \(Mo=20\) minuts.", r"Moda: el 20 aparece dos veces y los demás, una: \(Mo=20\) minutos.", r"Mode: 20 appears twice and the others once: \(Mo=20\) minutes."),
             L(r"Mitjana: \(\bar x=\dfrac{20+40+15+46+20+30+25}{7}=\dfrac{196}{7}=28\) minuts.", r"Media: \(\bar x=\dfrac{20+40+15+46+20+30+25}{7}=\dfrac{196}{7}=28\) minutos.", r"Mean: \(\bar x=\dfrac{20+40+15+46+20+30+25}{7}=\dfrac{196}{7}=28\) minutes."),
             L(r"Mediana: ordenem \(15,\ 20,\ 20,\ \boxed{25},\ 30,\ 40,\ 46\). Hi ha 7 dades i la del centre és la 4a: \(Me=25\) minuts.", r"Mediana: ordenamos \(15,\ 20,\ 20,\ \boxed{25},\ 30,\ 40,\ 46\). Hay 7 datos y el del centro es el 4.º: \(Me=25\) minutos.", r"Median: order them \(15,\ 20,\ 20,\ \boxed{25},\ 30,\ 40,\ 46\). There are 7 values and the middle one is the 4th: \(Me=25\) minutes."))
        + figs(fig(F_LEC, L('El triangle marca la mitjana (el punt d’equilibri) i la línia, la mediana', 'El triángulo marca la media (el punto de equilibrio) y la línea, la mediana', 'The triangle marks the mean (the balance point) and the line the median')))))
ck(sum(LEC), 196)
s5 += box('prop', L('Com cal interpretar-los?', '¿Cómo hay que interpretarlos?', 'How to interpret them'),
  ul(L(r"La mitjana és el valor que tindria cada dada si les <strong>repartírem a parts iguals</strong>. Si les dades foren pesos damunt d'una barra, la mitjana seria el <strong>punt d'equilibri</strong>.",
       r"La media es el valor que tendría cada dato si los <strong>repartiéramos a partes iguales</strong>. Si los datos fueran pesos encima de una barra, la media sería el <strong>punto de equilibrio</strong>.",
       r"The mean is the value each data point would have if we <strong>shared them out equally</strong>. If the data were weights on a bar, the mean would be the <strong>balance point</strong>."),
     L(r"Si el nombre de dades és <strong>parell</strong>, en el centre n'hi ha dues: la mediana és la <strong>mitjana d'aquestes dues</strong>. Per exemple, amb \(3,\ 5,\ 6,\ \boxed{7,\ 8},\ 8,\ 9,\ 10\): \(Me=\dfrac{7+8}{2}=7\dc 5\).",
       r"Si el número de datos es <strong>par</strong>, en el centro hay dos: la mediana es la <strong>media de estos dos</strong>. Por ejemplo, con \(3,\ 5,\ 6,\ \boxed{7,\ 8},\ 8,\ 9,\ 10\): \(Me=\dfrac{7+8}{2}=7\dc 5\).",
       r"If the number of data is <strong>even</strong>, there are two in the middle: the median is the <strong>mean of those two</strong>. For example, with \(3,\ 5,\ 6,\ \boxed{7,\ 8},\ 8,\ 9,\ 10\): \(Me=\dfrac{7+8}{2}=7\dc 5\)."),
     L(r"La mitjana es veu molt afectada per les <strong>dades extremes</strong> (molt grans o molt xicotetes); la mediana, no. Si hi ha alguna dada molt diferent de les altres, la mediana representa millor el conjunt.",
       r"La media se ve muy afectada por los <strong>datos extremos</strong> (muy grandes o muy pequeños); la mediana, no. Si hay algún dato muy diferente de los demás, la mediana representa mejor el conjunto.",
       r"The mean is strongly affected by <strong>extreme values</strong> (very large or very small); the median isn't. If one value is very different from the rest, the median represents the data better."))
  + note(r"Abans de calcular la mediana, <strong>ordena</strong> les dades! I no t'oblides de les repetides: cada dada es compta tantes vegades com aparega.",
         r"Antes de calcular la mediana, ¡<strong>ordena</strong> los datos! Y no te olvides de los repetidos: cada dato se cuenta tantas veces como aparezca.",
         r"Before finding the median, <strong>put the data in order</strong>! And don't forget repeated values: each one counts as many times as it appears.", '⚠️'))
s5 += (widget('w-params', '🎯', L('Calcula moda, mitjana i mediana', 'Calcula moda, media y mediana', 'Find the mode, mean and median'),
              ['<p class="hint-s">' + L("Escriu les dades separades per espais (pots fer servir decimals).", "Escribe los datos separados por espacios (puedes usar decimales).", "Type the data separated by spaces (decimals are fine).") + '</p>',
               '<div class="wrow">' + tin('d', L('Dades', 'Datos', 'Data'), '20 40 15 46 20 30 25', 'w') + '</div>'])
       + widget('w-balance', '⚖️', L('La mitjana és el punt d’equilibri', 'La media es el punto de equilibrio', 'The mean is the balance point'),
                ['<p class="hint-s">' + L("Mou les cinc dades i mira com canvien la mitjana (triangle) i la mediana (línia). Prova a portar una dada molt lluny!", "Mueve los cinco datos y mira cómo cambian la media (triángulo) y la mediana (línea). ¡Prueba a llevar un dato muy lejos!", "Move the five values and watch the mean (triangle) and the median (line) change. Try moving one value far away!") + '</p>']
                + ['<div class="wrow">' + rng('v%d' % i, 0, 20, 1, v, 'dada %d' % (i + 1)) + '</div>' for i, v in enumerate([4, 6, 7, 9, 9])])
       + drill('mitjana', 'Entrena: calcula la mitjana', 'Entrena: calcula la media', 'Train: find the mean')
       + drill('mediana', 'Entrena: calcula la mediana', 'Entrena: calcula la mediana', 'Train: find the median')
       + drill('moda', 'Entrena: troba la moda', 'Entrena: encuentra la moda', 'Train: find the mode', 'opts'))

DG = expand(TG)
assert sum(x * f for x, f in TG) == 29 and mean(DG) == Fr(29, 20) and median(DG) == 1 and modes(DG) == [1]
DN = expand(NOT)
assert sum(x * f for x, f in NOT) == 164 and mean(DN) == Fr(164, 25) and median(DN) == 6 and modes(DN) == [6]
s5 += box('prop', L('Mitjana, mediana i moda en una taula', 'Media, mediana y moda en una tabla', 'Mean, median and mode from a table'),
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
        P(r"Nombre de germans de 20 alumnes (apartat 9.2):", r"Número de hermanos de 20 alumnos (apartado 9.2):", r"Number of siblings of 20 students (section 9.2):") + ttab(TG)
        + ul(L(r"Mitjana: \(\bar x=\dfrac{29}{20}=1\dc 45\) germans.", r"Media: \(\bar x=\dfrac{29}{20}=1\dc 45\) hermanos.", r"Mean: \(\bar x=\dfrac{29}{20}=1\dc 45\) siblings."),
             L(r"Mediana: \(N=20\) és parell, les centrals són la 10a i l'11a dada. Fins al valor 0 n'hi ha 3 i fins a l'1, 12: la 10a i l'11a són 1. \(Me=\dfrac{1+1}{2}=1\) germà.",
               r"Mediana: \(N=20\) es par, los centrales son el 10.º y el 11.º dato. Hasta el valor 0 hay 3 y hasta el 1, 12: el 10.º y el 11.º son 1. \(Me=\dfrac{1+1}{2}=1\) hermano.",
               r"Median: \(N=20\) is even, so the middle ones are the 10th and 11th values. Up to 0 there are 3, and up to 1 there are 12: the 10th and 11th are both 1. \(Me=\dfrac{1+1}{2}=1\) sibling."),
             L(r"Moda: \(Mo=1\) germà (\(f=9\), la més gran).", r"Moda: \(Mo=1\) hermano (\(f=9\), la mayor).", r"Mode: \(Mo=1\) sibling (\(f=9\), the largest).")))
  + note(r"La mitjana pot ser un nombre que no és cap de les dades (ningú té 1,45 germans!). Vol dir que, si repartírem tots els germans a parts iguals, en tocarien 1,45 per alumne.",
         r"La media puede ser un número que no es ninguno de los datos (¡nadie tiene 1,45 hermanos!). Quiere decir que, si repartiéramos todos los hermanos a partes iguales, tocarían 1,45 por alumno.",
         r"The mean can be a number that isn't any of the data (nobody has 1.45 siblings!). It means that if we shared all the siblings out equally, each student would get 1.45."))
s5 += (widget('w-tmean', '🧾', L('Paràmetres d’una taula de freqüències', 'Parámetros de una tabla de frecuencias', 'Measures from a frequency table'),
              ['<p class="hint-s">' + L("Escriu els valors i les seues freqüències: l'eina fa la columna <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub>, la mitjana, la mediana amb les <i>F</i><sub>i</sub> i la moda.", "Escribe los valores y sus frecuencias: la herramienta hace la columna <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub>, la media, la mediana con las <i>F</i><sub>i</sub> y la moda.", "Type the values and their frequencies: the tool builds the <i>x</i><sub>i</sub>·<i>f</i><sub>i</sub> column, the mean, the median from <i>F</i><sub>i</sub> and the mode.") + '</p>',
               seg([('germ', L('Germans', 'Hermanos', 'Siblings')), ('not', L('Notes', 'Notas', 'Marks')), ('own', L('Els meus', 'Los míos', 'My own'))]),
               '<div class="wrow">' + tin('x', '<i>x</i><sub>i</sub>', '', 'w') + '</div><div class="wrow">' + tin('f', '<i>f</i><sub>i</sub>', '', 'w') + '</div>'], out='<div class="tout"></div>')
       + drill('tmean', 'Entrena: la mitjana des d’una taula', 'Entrena: la media desde una tabla', 'Train: the mean from a table'))

# dades agrupades (nou a 4t): taula dels diners de 9.3
MD = [Fr(a + b, 2) for a, b, _ in DIN]; SD = sum(m * f for m, (*_, f) in zip(MD, DIN))
ck(SD, 470); ck(Fr(SD, 40), '11.75'); ck(10 + Fr(20 - 16, 12) * 5, Fr(35, 3))
def gtab(rows, lab):
    """taula d'intervals amb marca, fi, Fi i mi·fi"""
    F = acc([(0, f) for *_, f in rows]); S = sum(Fr(a + b, 2) * f for a, b, f in rows)
    out = [[ivl(a, b), M(tn(Fr(a + b, 2))), M(str(f)), M(str(Fi)), M(tn(Fr(a + b, 2) * f))] for (a, b, f), Fi in zip(rows, F)]
    out.append(['<strong>Total</strong>', '', M('N=%d' % sum(f for *_, f in rows)), '', M(r'\textstyle\sum=%s' % tn(S))])
    return tbl([lab, L('Marca', 'Marca', 'Mark') + ' ' + M('x_i'), M('f_i'), M('F_i'), M(r'x_i\cdot f_i')], out, 'c freq')
s5 += box('prop', L('Paràmetres amb dades agrupades', 'Parámetros con datos agrupados', 'Measures with grouped data'),
  P(r"Si les dades estan agrupades en intervals, no sabem el valor exacte de cada dada. Treballem amb les <strong>marques de classe</strong> i obtenim valors <strong>aproximats</strong>:",
    r"Si los datos están agrupados en intervalos, no sabemos el valor exacto de cada dato. Trabajamos con las <strong>marcas de clase</strong> y obtenemos valores <strong>aproximados</strong>:",
    r"If the data are grouped into intervals, we don't know the exact value of each one. We work with the <strong>class marks</strong> and get <strong>approximate</strong> values:")
  + ul(L(r"<strong>Mitjana</strong>: com en una taula, però amb la marca de classe com a \(x_i\): \(\bar x\approx\dfrac{\sum x_i\cdot f_i}{N}\).",
         r"<strong>Media</strong>: como en una tabla, pero con la marca de clase como \(x_i\): \(\bar x\approx\dfrac{\sum x_i\cdot f_i}{N}\).",
         r"<strong>Mean</strong>: as in a table, but using the class mark as \(x_i\): \(\bar x\approx\dfrac{\sum x_i\cdot f_i}{N}\)."),
       L(r"<strong>Interval modal</strong>: l'interval amb la freqüència més gran (si tots tenen la mateixa amplitud). Com a moda aproximada podem donar-ne la marca de classe.",
         r"<strong>Intervalo modal</strong>: el intervalo con la frecuencia más grande (si todos tienen la misma amplitud). Como moda aproximada podemos dar su marca de clase.",
         r"<strong>Modal class</strong>: the interval with the highest frequency (if all intervals have the same width). Its class mark can be given as an approximate mode."),
       L(r"<strong>Interval medià</strong>: el primer interval amb \(F_i\geq\dfrac N2\). La mediana és dins d'aquest interval.",
         r"<strong>Intervalo mediano</strong>: el primer intervalo con \(F_i\geq\dfrac N2\). La mediana está dentro de este intervalo.",
         r"<strong>Median class</strong>: the first interval with \(F_i\geq\dfrac N2\). The median lies inside this interval."))
  + box('ex', L('Exemple: diners setmanals de 40 alumnes (apartat 9.3)', 'Ejemplo: dinero semanal de 40 alumnos (apartado 9.3)', 'Example: weekly money of 40 students (section 9.3)'),
        gtab(DIN, L('Diners (€)', 'Dinero (€)', 'Money (€)'))
        + ul(L(r"Mitjana: \(\bar x\approx\dfrac{470}{40}=11\dc 75\) €.", r"Media: \(\bar x\approx\dfrac{470}{40}=11\dc 75\) €.", r"Mean: \(\bar x\approx\dfrac{470}{40}=11\dc 75\) €."),
             L(r"Interval modal: \([10,\ 15)\), amb \(f=12\). Moda aproximada: \(12\dc 5\) €.", r"Intervalo modal: \([10,\ 15)\), con \(f=12\). Moda aproximada: \(12\dc 5\) €.", r"Modal class: \([10,\ 15)\), with \(f=12\). Approximate mode: \(12\dc 5\) €."),
             L(r"Interval medià: \(\frac N2=20\). La primera \(F_i\) que arriba a 20 és \(F=28\): la mediana és en \([10,\ 15)\).", r"Intervalo mediano: \(\frac N2=20\). La primera \(F_i\) que llega a 20 es \(F=28\): la mediana está en \([10,\ 15)\).", r"Median class: \(\frac N2=20\). The first \(F_i\) to reach 20 is \(F=28\): the median is in \([10,\ 15)\).")))
  + box('prop', L('Per a saber-ne més: la mediana dins de l’interval', 'Para saber más: la mediana dentro del intervalo', 'Going further: the median inside the interval'),
        P(r"Si suposem que les dades estan repartides per igual dins de l'interval medià \([L,\ L+a)\), la mediana és aproximadament \(Me\approx L+\dfrac{\frac N2-F_{i-1}}{f_i}\cdot a\), on \(F_{i-1}\) és la freqüència acumulada de l'interval anterior. Ací: \(Me\approx10+\dfrac{20-16}{12}\cdot5\approx11\dc 67\) €.",
          r"Si suponemos que los datos están repartidos por igual dentro del intervalo mediano \([L,\ L+a)\), la mediana es aproximadamente \(Me\approx L+\dfrac{\frac N2-F_{i-1}}{f_i}\cdot a\), donde \(F_{i-1}\) es la frecuencia acumulada del intervalo anterior. Aquí: \(Me\approx10+\dfrac{20-16}{12}\cdot5\approx11\dc 67\) €.",
          r"If we assume the data are spread evenly inside the median class \([L,\ L+a)\), the median is roughly \(Me\approx L+\dfrac{\frac N2-F_{i-1}}{f_i}\cdot a\), where \(F_{i-1}\) is the cumulative frequency of the previous interval. Here: \(Me\approx10+\dfrac{20-16}{12}\cdot5\approx11\dc 67\) €.")))
s5 += box('prop', L('Estratègies útils', 'Estrategias útiles', 'Useful strategies'),
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
s5 += (widget('w-target', '🏁', L('Quina nota necessite?', '¿Qué nota necesito?', 'What mark do I need?'),
              ['<p class="hint-s">' + L("Escriu les notes que ja tens i la mitjana que vols aconseguir.", "Escribe las notas que ya tienes y la media que quieres conseguir.", "Type the marks you already have and the mean you want to reach.") + '</p>',
               '<div class="wrow">' + tin('d', L('Notes', 'Notas', 'Marks'), '6 7 5', 'w') + '</div><div class="wrow">' + tin('m', L('Mitjana desitjada', 'Media deseada', 'Target mean'), '6,5') + tin('k', L('Exàmens que queden', 'Exámenes que quedan', 'Tests left'), '1') + '</div>'], out='<div class="tout"></div>')
       + drill('falta', 'Entrena: troba la dada que falta', 'Entrena: encuentra el dato que falta', 'Train: find the missing value'))

P61 = [6, 8, 5, 9, 6, 7, 4, 6, 9]
assert mean(P61) == Fr(60, 9) and median(P61) == 6 and modes(P61) == [6]
P62 = [12, 15, 11, 14, 18, 15, 13, 16, 12, 14]
assert mean(P62) == 14 and median(P62) == 14 and modes(P62) == [12, 14, 15]
S6L = (
 [prob(L(r"Aquestes són les notes de Pau en les nou activitats d'un trimestre: \(6,\ 8,\ 5,\ 9,\ 6,\ 7,\ 4,\ 6,\ 9\). Calcula la moda, la mitjana i la mediana.",
         r"Estas son las notas de Pau en las nueve actividades de un trimestre: \(6,\ 8,\ 5,\ 9,\ 6,\ 7,\ 4,\ 6,\ 9\). Calcula la moda, la media y la mediana.",
         r"These are Pau's marks in the nine activities of a term: \(6,\ 8,\ 5,\ 9,\ 6,\ 7,\ 4,\ 6,\ 9\). Find the mode, the mean and the median."),
       P(r"Moda: el 6 apareix tres vegades, més que cap altre: \(\boxed{Mo=6}\).", r"Moda: el 6 aparece tres veces, más que ningún otro: \(\boxed{Mo=6}\).", r"Mode: 6 appears three times, more than any other: \(\boxed{Mo=6}\)."),
       D(r"\bar x=\frac{6+8+5+9+6+7+4+6+9}{9}=\frac{60}{9}\approx\boxed{6\dc 67}"),
       P(r"Mediana: ordenem \(4,\ 5,\ 6,\ 6,\ \boxed{6},\ 7,\ 8,\ 9,\ 9\). Hi ha 9 dades i la del centre és la 5a: \(\boxed{Me=6}\).", r"Mediana: ordenamos \(4,\ 5,\ 6,\ 6,\ \boxed{6},\ 7,\ 8,\ 9,\ 9\). Hay 9 datos y el del centro es el 5.º: \(\boxed{Me=6}\).", r"Median: order them \(4,\ 5,\ 6,\ 6,\ \boxed{6},\ 7,\ 8,\ 9,\ 9\). There are 9 values and the middle one is the 5th: \(\boxed{Me=6}\).")),
  prob(L(r"En una enquesta sobre el color preferit, 8 alumnes han dit blau, 5 verd, 11 roig i 6 negre. Quina és la moda? Es pot calcular la mitjana?",
         r"En una encuesta sobre el color preferido, 8 alumnos han dicho azul, 5 verde, 11 rojo y 6 negro. ¿Cuál es la moda? ¿Se puede calcular la media?",
         r"In a survey about favourite colours, 8 students said blue, 5 green, 11 red and 6 black. What is the mode? Can we work out the mean?"),
       P(r"La moda és el valor amb més freqüència: \(\boxed{Mo=\text{\tri{roig}{rojo}{red}}}\) (11 alumnes).", r"La moda es el valor con más frecuencia: \(\boxed{Mo=\text{\tri{roig}{rojo}{red}}}\) (11 alumnos).", r"The mode is the value with the highest frequency: \(\boxed{Mo=\text{\tri{roig}{rojo}{red}}}\) (11 students)."),
       P(r"<strong>No</strong>: la variable és qualitativa i els colors no es poden sumar ni ordenar. No hi ha mitjana ni mediana.", r"<strong>No</strong>: la variable es cualitativa y los colores no se pueden sumar ni ordenar. No hay media ni mediana.", r"<strong>No</strong>: the variable is qualitative and colours can't be added or put in order. There is no mean or median."))],
 [prob(L(r"Les temperatures mínimes de deu dies han sigut: \(12,\ 15,\ 11,\ 14,\ 18,\ 15,\ 13,\ 16,\ 12,\ 14\) °C. Calcula la mitjana, la mediana i la moda.",
         r"Las temperaturas mínimas de diez días han sido: \(12,\ 15,\ 11,\ 14,\ 18,\ 15,\ 13,\ 16,\ 12,\ 14\) °C. Calcula la media, la mediana y la moda.",
         r"The minimum temperatures over ten days were: \(12,\ 15,\ 11,\ 14,\ 18,\ 15,\ 13,\ 16,\ 12,\ 14\) °C. Find the mean, median and mode."),
       D(r"\bar x=\frac{140}{10}=\boxed{14\ ^\circ\text{C}}"),
       P(r"Ordenem: \(11,\ 12,\ 12,\ 13,\ \boxed{14,\ 14},\ 15,\ 15,\ 16,\ 18\). Com que hi ha 10 dades (parell), les centrals són la 5a i la 6a: \(Me=\dfrac{14+14}{2}=\boxed{14\ ^\circ\text{C}}\).",
         r"Ordenamos: \(11,\ 12,\ 12,\ 13,\ \boxed{14,\ 14},\ 15,\ 15,\ 16,\ 18\). Como hay 10 datos (par), los centrales son el 5.º y el 6.º: \(Me=\dfrac{14+14}{2}=\boxed{14\ ^\circ\text{C}}\).",
         r"Order them: \(11,\ 12,\ 12,\ 13,\ \boxed{14,\ 14},\ 15,\ 15,\ 16,\ 18\). With 10 values (even), the middle ones are the 5th and 6th: \(Me=\dfrac{14+14}{2}=\boxed{14\ ^\circ\text{C}}\)."),
       P(r"Moda: 12, 14 i 15 apareixen dues vegades cadascun. Hi ha <strong>tres modes</strong>: \(\boxed{12,\ 14\ \text{\tri{i}{y}{and}}\ 15\ ^\circ\text{C}}\).", r"Moda: 12, 14 y 15 aparecen dos veces cada uno. Hay <strong>tres modas</strong>: \(\boxed{12,\ 14\ \text{\tri{i}{y}{and}}\ 15\ ^\circ\text{C}}\).", r"Mode: 12, 14 and 15 each appear twice. There are <strong>three modes</strong>: \(\boxed{12,\ 14\ \text{\tri{i}{y}{and}}\ 15\ ^\circ\text{C}}\)."))],
 [prob(L(r"En una botiga treballen quatre dependents, que cobren \(1\,200\), \(1\,350\), \(1\,250\) i \(1\,300\) € al mes, i la propietària, que cobra \(5\,900\) €. Calcula la mitjana i la mediana dels sous. Quina representa millor el que cobra un treballador de la botiga?",
         r"En una tienda trabajan cuatro dependientes, que cobran \(1\,200\), \(1\,350\), \(1\,250\) y \(1\,300\) € al mes, y la propietaria, que cobra \(5\,900\) €. Calcula la media y la mediana de los sueldos. ¿Cuál representa mejor lo que cobra un trabajador de la tienda?",
         r"A shop has four assistants who earn \(1\,200\), \(1\,350\), \(1\,250\) and \(1\,300\) € a month, and the owner, who earns \(5\,900\) €. Find the mean and median salary. Which one better represents what a worker in the shop earns?"),
       D(r"\bar x=\frac{1\,200+1\,350+1\,250+5\,900+1\,300}{5}=\frac{11\,000}{5}=\boxed{2\,200\ \text{€}}"),
       P(r"Ordenem: \(1\,200,\ 1\,250,\ \boxed{1\,300},\ 1\,350,\ 5\,900\): \(\boxed{Me=1\,300\ \text{€}}\).", r"Ordenamos: \(1\,200,\ 1\,250,\ \boxed{1\,300},\ 1\,350,\ 5\,900\): \(\boxed{Me=1\,300\ \text{€}}\).", r"Order them: \(1\,200,\ 1\,250,\ \boxed{1\,300},\ 1\,350,\ 5\,900\): \(\boxed{Me=1\,300\ \text{€}}\)."),
       P(r"Quatre de les cinc persones cobren menys de \(1\,400\) €, però la mitjana diu \(2\,200\) € perquè el sou de la propietària (una dada extrema) l'estira cap amunt. Aquí la <strong>mediana</strong> representa millor el conjunt.",
         r"Cuatro de las cinco personas cobran menos de \(1\,400\) €, pero la media dice \(2\,200\) € porque el sueldo de la propietaria (un dato extremo) la estira hacia arriba. Aquí la <strong>mediana</strong> representa mejor el conjunto.",
         r"Four of the five people earn less than \(1\,400\) €, but the mean says \(2\,200\) € because the owner's salary (an extreme value) pulls it up. Here the <strong>median</strong> represents the data better."))])
ck(sum(P62), 140); ck(sum(SAL), 11000)
P6P = [3, 7, 4, 7, 9]
assert mean(P6P) == 6 and median(P6P) == 7 and modes(P6P) == [7]
PETS = [(0, 6), (1, 10), (2, 5), (3, 3)]
DP = expand(PETS)
assert mean(DP) == Fr(29, 24) and median(DP) == 1 and modes(DP) == [1]
CAL = [(36, 3), (37, 5), (38, 8), (39, 6), (40, 2)]
DC = expand(CAL)
assert len(DC) == 24 and sum(x * f for x, f in CAL) == 911 and median(DC) == 38 and modes(DC) == [38]
MK = [Fr(EDG[i] + EDG[i + 1], 2) for i in range(5)]
SA = sum(m * f for m, f in zip(MK, FA)); assert SA == 4580
S7L = (
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
 [prob(L(r"Calcula la mitjana aproximada de les alçades dels 30 alumnes de l'apartat 9.3, que estan agrupades en intervals.",
         r"Calcula la media aproximada de las alturas de los 30 alumnos del apartado 9.3, que están agrupadas en intervalos.",
         r"Work out the approximate mean height of the 30 students in section 9.3, whose data are grouped into intervals."),
       P(r"Com que no sabem cada dada, fem servir la <strong>marca de classe</strong> de cada interval com a \(x_i\):", r"Como no sabemos cada dato, usamos la <strong>marca de clase</strong> de cada intervalo como \(x_i\):", r"As we don't know each value, we use the <strong>class mark</strong> of each interval as \(x_i\):")
       + ttab(list(zip(MK, FA)), L('Marca', 'Marca', 'Mark')),
       D(r"\bar x\approx\frac{4\,580}{30}\approx\boxed{152\dc 67\ \text{cm}}"),
       P(r"És una aproximació: amb les 30 dades originals la mitjana exacta és \(152\dc 13\) cm, molt pròxima.", r"Es una aproximación: con los 30 datos originales la media exacta es \(152\dc 13\) cm, muy próxima.", r"It's an approximation: with the 30 original values the exact mean is \(152\dc 13\) cm, very close."))])
ck(fr('6.2') * 20 + fr('7.1') * 10, 195); ck(Fr(195, 30), '6.5')
ck(16 * 6 - 13 * 5, 31)
# taula amb una freqüència desconeguda: valors 1, 2, 3, 4 amb f 3, x, 5, 2 i mitjana 2,5
assert mean(expand([(1, 3), (2, 2), (3, 5), (4, 2)])) == Fr(5, 2)
S9L = (
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
# nivell 3: dades agrupades (temps de deures de 9.3)
from s123 import DEU, EDD, FDEU
GD = [(EDD[i], EDD[i + 1], f) for i, f in enumerate(FDEU)]
SDE = sum(Fr(a + b, 2) * f for a, b, f in GD); ck(SDE, 1390); ck(Fr(SDE, 36), Fr(695, 18))
assert acc([(0, f) for f in FDEU]) == [3, 10, 20, 29, 33, 36]
PL3 = [prob(L(r"Amb la taula dels minuts de deures de 36 alumnes (apartat 9.3, nivell 3), calcula la mitjana aproximada i troba l'interval modal i l'interval medià. Compara la mitjana aproximada amb l'exacta, que és \(38\dc 33\) minuts (arrodonida).",
              r"Con la tabla de los minutos de deberes de 36 alumnos (apartado 9.3, nivel 3), calcula la media aproximada y encuentra el intervalo modal y el intervalo mediano. Compara la media aproximada con la exacta, que es \(38\dc 33\) minutos (redondeada).",
              r"Using the table of homework minutes for 36 students (section 9.3, level 3), work out the approximate mean and find the modal class and the median class. Compare the approximate mean with the exact one, which is \(38\dc 33\) minutes (rounded)."),
            gtab(GD, L('Temps (min)', 'Tiempo (min)', 'Time (min)')),
            D(r"\bar x\approx\frac{1\,390}{36}\approx\boxed{38\dc 61\ \text{min}}"),
            P(r"Interval modal: \(\boxed{[30,\ 40)}\) (\(f=10\)). &nbsp; \(\frac N2=18\): la primera \(F_i\geq18\) és \(F=20\), interval medià \(\boxed{[30,\ 40)}\). La mitjana aproximada només s'allunya uns \(0\dc 28\) minuts de l'exacta.",
              r"Intervalo modal: \(\boxed{[30,\ 40)}\) (\(f=10\)). &nbsp; \(\frac N2=18\): la primera \(F_i\geq18\) es \(F=20\), intervalo mediano \(\boxed{[30,\ 40)}\). La media aproximada solo se aleja unos \(0\dc 28\) minutos de la exacta.",
              r"Modal class: \(\boxed{[30,\ 40)}\) (\(f=10\)). &nbsp; \(\frac N2=18\): the first \(F_i\geq18\) is \(F=20\), so the median class is \(\boxed{[30,\ 40)}\). The approximate mean is only about \(0\dc 28\) minutes away from the exact one."))]
ck(mean(DEU), Fr(115, 3)); assert abs(float(Fr(695, 18)) - 38.61) < 0.005 and abs(float(Fr(695, 18) - Fr(115, 3)) - 0.28) < 0.005
s5 += levels(S6L[0] + S7L[0], S6L[1] + S7L[1] + S9L[0] + S9L[1], S6L[2] + S9L[2] + S7L[2] + PL3)
s5 += practice([('★☆☆', L(r"Calcula la moda, la mitjana i la mediana de: \(3,\ 7,\ 4,\ 7,\ 9\).", r"Calcula la moda, la media y la mediana de: \(3,\ 7,\ 4,\ 7,\ 9\).", r"Find the mode, mean and median of: \(3,\ 7,\ 4,\ 7,\ 9\).")),
                ('★★☆', L(r"Calcula la mitjana, la mediana i la moda de les notes de la taula de l'apartat 9.2 (25 alumnes).", r"Calcula la media, la mediana y la moda de las notas de la tabla del apartado 9.2 (25 alumnos).", r"Find the mean, median and mode of the marks in the table in section 9.2 (25 students).")),
                ('★★☆', L(r"La mitjana de 4 nombres és 9. Tres d'ells són 7, 12 i 8. Quin és el quart?", r"La media de 4 números es 9. Tres de ellos son 7, 12 y 8. ¿Cuál es el cuarto?", r"The mean of 4 numbers is 9. Three of them are 7, 12 and 8. What is the fourth?"))],
               L(r"1) \(Mo=7\), \(\bar x=\frac{30}{5}=6\), \(Me=7\) (\(3,\ 4,\ 7,\ 7,\ 9\)). &nbsp; 2) \(\sum x_i f_i=164\), \(\bar x=\frac{164}{25}=6\dc 56\); la dada central és la 13a i \(F=13\) en el 6: \(Me=6\); \(Mo=6\). &nbsp; 3) Suma \(9\cdot4=36\); \(36-(7+12+8)=9\).",
                 r"1) \(Mo=7\), \(\bar x=\frac{30}{5}=6\), \(Me=7\) (\(3,\ 4,\ 7,\ 7,\ 9\)). &nbsp; 2) \(\sum x_i f_i=164\), \(\bar x=\frac{164}{25}=6\dc 56\); el dato central es el 13.º y \(F=13\) en el 6: \(Me=6\); \(Mo=6\). &nbsp; 3) Suma \(9\cdot4=36\); \(36-(7+12+8)=9\).",
                 r"1) \(Mo=7\), \(\bar x=\frac{30}{5}=6\), \(Me=7\) (\(3,\ 4,\ 7,\ 7,\ 9\)). &nbsp; 2) \(\sum x_i f_i=164\), \(\bar x=\frac{164}{25}=6\dc 56\); the middle value is the 13th and \(F=13\) at 6: \(Me=6\); \(Mo=6\). &nbsp; 3) Sum \(9\cdot4=36\); \(36-(7+12+8)=9\)."))
ck(36 - 27, 9); assert mean(DN) == Fr(164, 25)
