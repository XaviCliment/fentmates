# Apartats 10.4-10.6 dels apunts de la Unitat 10 de 1r ESO: diagrames de barres, polígons de freqüències i histogrames,
# diagrames de sectors i pictogrames, i moda, mitjana i mediana.
from comu import *
from s123 import TG, NG, EDG, FA, S3B, EDB, FB, acc

FRU = [(L('Poma', 'Manzana', 'Apple'), 8), (L('Plàtan', 'Plátano', 'Banana'), 6), (L('Taronja', 'Naranja', 'Orange'), 5), (L('Maduixa', 'Fresa', 'Strawberry'), 4), (L('Pera', 'Pera', 'Pear'), 2)]
FRUs = [(Ls('Poma', 'Manzana', 'Apple'), 8), (Ls('Plàtan', 'Plátano', 'Banana'), 6), (Ls('Taronja', 'Naranja', 'Orange'), 5), (Ls('Maduixa', 'Fresa', 'Strawberry'), 4), (Ls('Pera', 'Pera', 'Pear'), 2)]
assert sum(f for _, f in FRU) == 25
FREQ = Ls('Freqüència', 'Frecuencia', 'Frequency')
NALU = Ls("Nre. d'alumnes", 'N.º de alumnos', 'Students')

# =====================================================================
# 10.4 Diagrames de barres, polígons de freqüències i histogrames
# =====================================================================
F_FRU = barres([c for c, _ in FRUs], [f for _, f in FRUs], yl=NALU, cls=['b%d' % (i % 4) for i in range(5)])
F_GB = barres([str(x) for x, _ in TG], [f for _, f in TG], yl=NALU, xl=Ls('germans', 'hermanos', 'siblings'))
F_GP = barres([str(x) for x, _ in TG], [f for _, f in TG], kind='both', yl=NALU, xl=Ls('germans', 'hermanos', 'siblings'))
F_H = hist(EDG, FA, yl=NALU, xl='cm')
F_HP = hist(EDG, FA, poly=True, yl=NALU, xl='cm')
s4 = box('def', L('Diagrama de barres', 'Diagrama de barras', 'Bar chart'),
  P(r"Els <strong>gràfics estadístics</strong> ens deixen veure d'un colp d'ull com es reparteixen les dades. En un <strong>diagrama de barres</strong>:",
    r"Los <strong>gráficos estadísticos</strong> nos dejan ver de un vistazo cómo se reparten los datos. En un <strong>diagrama de barras</strong>:",
    r"<strong>Statistical charts</strong> let us see at a glance how the data are spread out. In a <strong>bar chart</strong>:")
  + ul(L(r"en l'eix horitzontal posem els <strong>valors</strong> de la variable i en el vertical, les <strong>freqüències</strong>;", r"en el eje horizontal ponemos los <strong>valores</strong> de la variable y en el vertical, las <strong>frecuencias</strong>;", r"the horizontal axis shows the <strong>values</strong> of the variable and the vertical axis the <strong>frequencies</strong>;"),
       L(r"damunt de cada valor alcem una barra amb l'<strong>altura igual a la seua freqüència</strong>; totes les barres tenen la mateixa amplària i estan <strong>separades</strong>.", r"encima de cada valor levantamos una barra con la <strong>altura igual a su frecuencia</strong>; todas las barras tienen la misma anchura y están <strong>separadas</strong>.", r"above each value we draw a bar whose <strong>height equals its frequency</strong>; all bars are the same width and are <strong>separated</strong>."))
  + P(r"Serveix per a variables <strong>qualitatives</strong> i <strong>quantitatives discretes</strong>.", r"Sirve para variables <strong>cualitativas</strong> y <strong>cuantitativas discretas</strong>.", r"It's used for <strong>qualitative</strong> and <strong>discrete quantitative</strong> variables.")
  + figs(fig(F_FRU, L('Fruita preferida de 25 alumnes', 'Fruta preferida de 25 alumnos', 'Favourite fruit of 25 students')), fig(F_GB, L('Nombre de germans de 20 alumnes', 'Número de hermanos de 20 alumnos', 'Number of siblings of 20 students')))
  + note(r"Escriu sempre el títol del gràfic i el nom de cada eix, i comença l'eix vertical en 0: si no, les diferències entre barres semblen més grans del que són.",
         r"Escribe siempre el título del gráfico y el nombre de cada eje, y empieza el eje vertical en 0: si no, las diferencias entre barras parecen mayores de lo que son.",
         r"Always write the chart's title and the name of each axis, and start the vertical axis at 0: otherwise the differences between bars look bigger than they are.", '⚠️'))

s4 += box('prop', L('Polígon de freqüències i histograma', 'Polígono de frecuencias e histograma', 'Frequency polygon and histogram'),
  ul(L(r"El <strong>polígon de freqüències</strong> s'obté unint amb segments els extrems superiors de les barres. Va molt bé per a veure com <strong>puja i baixa</strong> la freqüència i per a comparar dues distribucions en el mateix gràfic.",
       r"El <strong>polígono de frecuencias</strong> se obtiene uniendo con segmentos los extremos superiores de las barras. Va muy bien para ver cómo <strong>sube y baja</strong> la frecuencia y para comparar dos distribuciones en el mismo gráfico.",
       r"The <strong>frequency polygon</strong> is made by joining the tops of the bars with line segments. It's great for seeing how the frequency <strong>rises and falls</strong> and for comparing two distributions on the same chart."),
     L(r"Quan les dades estan <strong>agrupades en intervals</strong> (variables contínues) fem un <strong>histograma</strong>: les barres ocupen tot l'interval i van <strong>juntes</strong>, sense espais. El polígon s'obté unint els punts mitjans de la part de dalt (les marques de classe).",
       r"Cuando los datos están <strong>agrupados en intervalos</strong> (variables continuas) hacemos un <strong>histograma</strong>: las barras ocupan todo el intervalo y van <strong>juntas</strong>, sin espacios. El polígono se obtiene uniendo los puntos medios de la parte de arriba (las marcas de clase).",
       r"When the data are <strong>grouped into intervals</strong> (continuous variables) we draw a <strong>histogram</strong>: the bars fill the whole interval and <strong>touch</strong>, with no gaps. The polygon joins the midpoints of the tops (the class marks)."))
  + figs(fig(F_GP, L('Barres i polígon de freqüències', 'Barras y polígono de frecuencias', 'Bars and frequency polygon')), fig(F_HP, L('Histograma de les alçades de 30 alumnes', 'Histograma de las alturas de 30 alumnos', 'Histogram of the heights of 30 students'))))
s4 += (widget('w-chart', '📊', L('Construeix el gràfic', 'Construye el gráfico', 'Build the chart'),
              ['<p class="hint-s">' + L("Escriu els valors i les seues freqüències (separats per espais) o tria un exemple.", "Escribe los valores y sus frecuencias (separados por espacios) o elige un ejemplo.", "Type the values and their frequencies (separated by spaces) or choose an example.") + '</p>',
               seg([('germ', L('Germans', 'Hermanos', 'Siblings')), ('fru', L('Fruita', 'Fruta', 'Fruit')), ('own', L('Els meus', 'Los míos', 'My own'))]),
               '<div class="wrow">' + tin('x', L('Valors', 'Valores', 'Values'), '', 'w') + '</div><div class="wrow">' + tin('f', '<i>f</i><sub>i</sub>', '', 'w') + '</div>',
               seg([('bar', L('Barres', 'Barras', 'Bars')), ('poly', L('Polígon', 'Polígono', 'Polygon')), ('both', L('Barres i polígon', 'Barras y polígono', 'Bars and polygon'))])])
       + widget('w-hist', '📶', L("Histograma: canvia l'amplària dels intervals", 'Histograma: cambia la anchura de los intervalos', 'Histogram: change the interval width'),
                ['<p class="hint-s">' + L("Les 30 alçades de l'exemple de l'apartat 10.3. Si els intervals són massa estrets o massa amples, el gràfic ens diu menys coses.",
                                          "Las 30 alturas del ejemplo del apartado 10.3. Si los intervalos son demasiado estrechos o demasiado anchos, el gráfico nos dice menos cosas.",
                                          "The 30 heights from the example in section 10.3. If the intervals are too narrow or too wide, the chart tells us less.") + '</p>',
                 seg([('2', L('Amplària 2', 'Anchura 2', 'Width 2')), ('5', L('Amplària 5', 'Anchura 5', 'Width 5')), ('10', L('Amplària 10', 'Anchura 10', 'Width 10'))], 1),
                 seg([('0', L('Sense polígon', 'Sin polígono', 'No polygon')), ('1', L('Amb polígon', 'Con polígono', 'With polygon'))])])
       + drill('readbar', 'Entrena: llig el diagrama de barres', 'Entrena: lee el diagrama de barras', 'Train: read the bar chart'))

PETS = [(0, 6), (1, 10), (2, 5), (3, 3)]
F_PETS = barres([str(x) for x, _ in PETS], [f for _, f in PETS], yl=NALU, xl=Ls('mascotes', 'mascotas', 'pets'))
NP = sum(f for _, f in PETS); assert NP == 24
ck(sum(x * f for x, f in PETS), 29)
F_TB = hist(EDB, FB, poly=True, yl=NALU, xl='min')
VEND = [52, 48, 55, 50]
F_V1 = barres(['A', 'B', 'C', 'D'], VEND, yl=Ls('vendes', 'ventas', 'sales'), y0=45, step=1, H=170)
F_V2 = barres(['A', 'B', 'C', 'D'], VEND, yl=Ls('vendes', 'ventas', 'sales'), step=10, H=170)
s4 += levels(
 [prob(L(r"Aquest diagrama mostra quantes mascotes tenen els alumnes d'una classe. Fes la taula de freqüències. Quants alumnes hi ha? Quantes mascotes tenen en total?",
         r"Este diagrama muestra cuántas mascotas tienen los alumnos de una clase. Haz la tabla de frecuencias. ¿Cuántos alumnos hay? ¿Cuántas mascotas tienen en total?",
         r"This chart shows how many pets the students in a class have. Make the frequency table. How many students are there? How many pets do they have altogether?") + figs(fig(F_PETS)),
       P(r"Llegim l'altura de cada barra:", r"Leemos la altura de cada barra:", r"Read the height of each bar:") + tbl([M('x_i'), '0', '1', '2', '3', 'Total'], [[M('f_i'), '6', '10', '5', '3', '24']], 'c'),
       P(r"Hi ha \(\boxed{24}\) alumnes. Mascotes: \(0\cdot6+1\cdot10+2\cdot5+3\cdot3=0+10+10+9=\boxed{29}\).", r"Hay \(\boxed{24}\) alumnos. Mascotas: \(0\cdot6+1\cdot10+2\cdot5+3\cdot3=0+10+10+9=\boxed{29}\).", r"There are \(\boxed{24}\) students. Pets: \(0\cdot6+1\cdot10+2\cdot5+3\cdot3=0+10+10+9=\boxed{29}\)."))],
 [prob(L(r"Dibuixa l'histograma i el polígon de freqüències de la taula dels minuts que tarden els alumnes a arribar a l'institut (apartat 10.3, nivell 3).",
         r"Dibuja el histograma y el polígono de frecuencias de la tabla de los minutos que tardan los alumnos en llegar al instituto (apartado 10.3, nivel 3).",
         r"Draw the histogram and frequency polygon for the table of the minutes students take to get to school (section 10.3, level 3)."),
       P(r"Els intervals \([0,\ 10)\), \([10,\ 20)\), \([20,\ 30)\), \([30,\ 40)\) van en l'eix horitzontal, junts; les altures són \(4\), \(7\), \(6\) i \(3\). El polígon passa per les marques de classe \(5\), \(15\), \(25\), \(35\) i el tanquem en l'eix.",
         r"Los intervalos \([0,\ 10)\), \([10,\ 20)\), \([20,\ 30)\), \([30,\ 40)\) van en el eje horizontal, juntos; las alturas son \(4\), \(7\), \(6\) y \(3\). El polígono pasa por las marcas de clase \(5\), \(15\), \(25\), \(35\) y lo cerramos en el eje.",
         r"The intervals \([0,\ 10)\), \([10,\ 20)\), \([20,\ 30)\), \([30,\ 40)\) go side by side on the horizontal axis; the heights are \(4\), \(7\), \(6\) and \(3\). The polygon goes through the class marks \(5\), \(15\), \(25\), \(35\) and we close it on the axis.") + figs(fig(F_TB)))],
 [prob(L(r"Una empresa presenta les vendes (en milers d'euros) de les seues quatre botigues amb el gràfic de l'esquerra. Per què és enganyós? Sembla que la botiga C ven molt més que la B?",
         r"Una empresa presenta las ventas (en miles de euros) de sus cuatro tiendas con el gráfico de la izquierda. ¿Por qué es engañoso? ¿Parece que la tienda C vende mucho más que la B?",
         r"A company shows the sales (in thousands of euros) of its four shops with the chart on the left. Why is it misleading? Does shop C seem to sell much more than shop B?") + figs(fig(F_V1, L('Gràfic de l’empresa', 'Gráfico de la empresa', 'The company’s chart'))),
       P(r"L'eix vertical comença en 45, no en 0. Així, la barra de C (55) sembla més del triple que la de B (48), però en realitat C ven \(55-48=7\) mil euros més, només un \(15\ \%\) més aproximadament.",
         r"El eje vertical empieza en 45, no en 0. Así, la barra de C (55) parece más del triple que la de B (48), pero en realidad C vende \(55-48=7\) mil euros más, solo un \(15\ \%\) más aproximadamente.",
         r"The vertical axis starts at 45, not 0. So C's bar (55) looks more than three times B's (48), but C actually sells only \(55-48=7\) thousand euros more, roughly \(15\ \%\) more."),
       P(r"Si comencem l'eix en 0, les quatre botigues venen <strong>quasi el mateix</strong>:", r"Si empezamos el eje en 0, las cuatro tiendas venden <strong>casi lo mismo</strong>:", r"If we start the axis at 0, the four shops sell <strong>almost the same</strong>:") + figs(fig(F_V2, L('Gràfic correcte', 'Gráfico correcto', 'Correct chart'))))])
assert (55 - 45) / (48 - 45) > 3 and abs((55 - 48) / 48 - 0.146) < 0.01
s4 += practice([('★☆☆', L(r"Dibuixa el diagrama de barres i el polígon de freqüències dels gols d'un equip: 0 gols en 2 partits, 1 en 5, 2 en 5, 3 en 2 i 4 en 1.",
                          r"Dibuja el diagrama de barras y el polígono de frecuencias de los goles de un equipo: 0 goles en 2 partidos, 1 en 5, 2 en 5, 3 en 2 y 4 en 1.",
                          r"Draw the bar chart and frequency polygon for a team's goals: 0 goals in 2 matches, 1 in 5, 2 in 5, 3 in 2 and 4 in 1.")),
                ('★★☆', L(r"Quin tipus de gràfic faries per a: a) l'esport preferit; b) el pes de 40 persones; c) el nombre de cotxes de cada família?",
                          r"¿Qué tipo de gráfico harías para: a) el deporte preferido; b) el peso de 40 personas; c) el número de coches de cada familia?",
                          r"What kind of chart would you draw for: a) favourite sport; b) the weight of 40 people; c) the number of cars each family has?"))],
               L(r"1) Barres d'altures 2, 5, 5, 2 i 1 sobre 0, 1, 2, 3 i 4; el polígon uneix els extrems de dalt. &nbsp; 2) a) diagrama de barres (o de sectors); b) histograma (variable contínua, agrupada en intervals); c) diagrama de barres.",
                 r"1) Barras de alturas 2, 5, 5, 2 y 1 sobre 0, 1, 2, 3 y 4; el polígono une los extremos de arriba. &nbsp; 2) a) diagrama de barras (o de sectores); b) histograma (variable continua, agrupada en intervalos); c) diagrama de barras.",
                 r"1) Bars of heights 2, 5, 5, 2 and 1 over 0, 1, 2, 3 and 4; the polygon joins the tops. &nbsp; 2) a) bar chart (or pie chart); b) histogram (continuous variable, grouped into intervals); c) bar chart."))

# =====================================================================
# 10.5 Diagrames de sectors i pictogrames
# =====================================================================
TRA = [(L('Caminant', 'Andando', 'Walking'), Ls('Caminant', 'Andando', 'Walking'), 10), (L('Autobús', 'Autobús', 'Bus'), Ls('Autobús', 'Autobús', 'Bus'), 6),
       (L('Cotxe', 'Coche', 'Car'), Ls('Cotxe', 'Coche', 'Car'), 5), (L('Bici', 'Bici', 'Bike'), Ls('Bici', 'Bici', 'Bike'), 3)]
NT = sum(f for *_, f in TRA); assert NT == 24
ANG = [Fr(f * 360, NT) for *_, f in TRA]; assert ANG == [150, 90, 75, 45] and sum(ANG) == 360
F_TRA = sectors([s for _, s, _ in TRA], [f for *_, f in TRA], angles=True)
LIB = [(Ls('Gener', 'Enero', 'January'), 40), (Ls('Febrer', 'Febrero', 'February'), 35), (Ls('Març', 'Marzo', 'March'), 50), (Ls('Abril', 'Abril', 'April'), 25)]
F_LIB = picto([c for c, _ in LIB], [v for _, v in LIB], 10, '📘')
s5 = box('def', L('Diagrama de sectors', 'Diagrama de sectores', 'Pie chart'),
  P(r"En un <strong>diagrama de sectors</strong> el cercle representa el total de les dades i cada valor ocupa un sector <strong>proporcional a la seua freqüència</strong>. Per a dibuixar-lo calculem l'angle de cada sector:",
    r"En un <strong>diagrama de sectores</strong> el círculo representa el total de los datos y cada valor ocupa un sector <strong>proporcional a su frecuencia</strong>. Para dibujarlo calculamos el ángulo de cada sector:",
    r"In a <strong>pie chart</strong> the circle stands for all the data and each value takes up a slice <strong>proportional to its frequency</strong>. To draw it we work out the angle of each slice:")
  + D(r"\text{angle}=\frac{f_i}{N}\cdot 360^\circ=h_i\cdot 360^\circ")
  + P(r"Després el dibuixem amb el transportador. Serveix sobretot per a variables <strong>qualitatives</strong> i per a veure quina <strong>part del total</strong> és cada valor.",
      r"Después lo dibujamos con el transportador. Sirve sobre todo para variables <strong>cualitativas</strong> y para ver qué <strong>parte del total</strong> es cada valor.",
      r"Then we draw it with a protractor. It's mainly used for <strong>qualitative</strong> variables and to see what <strong>part of the total</strong> each value is.")
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"Com vénen a l'institut els 24 alumnes d'una classe:", r"Cómo vienen al instituto los 24 alumnos de una clase:", r"How the 24 students in a class get to school:")
        + tbl([L('Transport', 'Transporte', 'Transport'), M('f_i'), L('Angle', 'Ángulo', 'Angle')],
              [[c, M(str(f)), M(r'\frac{%d}{24}\cdot360^\circ=%s^\circ' % (f, tn(a)))] for (c, _, f), a in zip(TRA, ANG)] + [['<strong>Total</strong>', M('24'), M(r'360^\circ')]], 'c')
        + figs(fig(F_TRA)))
  + note(r"Truc: si \(N\) és un divisor de 360, cada dada val \(360:N\) graus. Ací, \(360:24=15^\circ\) per alumne: caminant, \(10\cdot15=150^\circ\).",
         r"Truco: si \(N\) es un divisor de 360, cada dato vale \(360:N\) grados. Aquí, \(360:24=15^\circ\) por alumno: andando, \(10\cdot15=150^\circ\).",
         r"Tip: if \(N\) divides 360, each data value is worth \(360:N\) degrees. Here \(360:24=15^\circ\) per student: walking, \(10\cdot15=150^\circ\)."))
s5 += box('prop', L('Pictogrames', 'Pictogramas', 'Pictograms'),
  P(r"Un <strong>pictograma</strong> representa les freqüències amb <strong>dibuixos</strong> relacionats amb el tema. Cal indicar quant val cada dibuix; un tros de dibuix val la part corresponent.",
    r"Un <strong>pictograma</strong> representa las frecuencias con <strong>dibujos</strong> relacionados con el tema. Hay que indicar cuánto vale cada dibujo; un trozo de dibujo vale la parte correspondiente.",
    r"A <strong>pictogram</strong> shows the frequencies with <strong>pictures</strong> related to the topic. We must say what each picture is worth; part of a picture is worth that part.")
  + figs(fig(F_LIB, L('Llibres prestats per la biblioteca (📘 = 10 llibres)', 'Libros prestados por la biblioteca (📘 = 10 libros)', 'Books lent by the library (📘 = 10 books)')))
  + P(r"Al febrer hi ha tres llibres i mig: \(3\dc 5\cdot10=35\) llibres prestats.", r"En febrero hay tres libros y medio: \(3\dc 5\cdot10=35\) libros prestados.", r"In February there are three and a half books: \(3\dc 5\cdot10=35\) books lent."))
s5 += (widget('w-pie', '🥧', L('Diagrama de sectors pas a pas', 'Diagrama de sectores paso a paso', 'Pie chart step by step'),
              ['<p class="hint-s">' + L("Escriu els valors i les freqüències o tria un exemple: l'eina calcula l'angle de cada sector.", "Escribe los valores y las frecuencias o elige un ejemplo: la herramienta calcula el ángulo de cada sector.", "Type the values and frequencies or choose an example: the tool works out each slice's angle.") + '</p>',
               seg([('tra', L('Transport', 'Transporte', 'Transport')), ('fru', L('Fruita', 'Fruta', 'Fruit')), ('own', L('Els meus', 'Los míos', 'My own'))]),
               '<div class="wrow">' + tin('x', L('Valors', 'Valores', 'Values'), '', 'w') + '</div><div class="wrow">' + tin('f', '<i>f</i><sub>i</sub>', '', 'w') + '</div>',
               seg([('pie', L('Sectors', 'Sectores', 'Pie chart')), ('pic', L('Pictograma', 'Pictograma', 'Pictogram'))])])
       + drill('angle', "Entrena: calcula l'angle del sector", 'Entrena: calcula el ángulo del sector', 'Train: work out the slice angle')
       + drill('pieread', 'Entrena: del sector a la freqüència', 'Entrena: del sector a la frecuencia', 'Train: from slice to frequency'))

MAS = [(L('Gos', 'Perro', 'Dog'), Ls('Gos', 'Perro', 'Dog'), 12), (L('Gat', 'Gato', 'Cat'), Ls('Gat', 'Gato', 'Cat'), 9), (L('Peix', 'Pez', 'Fish'), Ls('Peix', 'Pez', 'Fish'), 6), (L('Cap', 'Ninguna', 'None'), Ls('Cap', 'Ninguna', 'None'), 3)]
AM = [Fr(f * 360, 30) for *_, f in MAS]; assert AM == [144, 108, 72, 36]
F_MAS = sectors([s for _, s, _ in MAS], [f for *_, f in MAS], angles=True)
ESP = [(Ls('Futbol', 'Fútbol', 'Football'), 150), (Ls('Bàsquet', 'Baloncesto', 'Basketball'), 90), (Ls('Natació', 'Natación', 'Swimming'), 72), (Ls('Altres', 'Otros', 'Other'), 48)]
assert sum(a for _, a in ESP) == 360
F_ESP = sectors([c for c, _ in ESP], [a for _, a in ESP], angles=True)
FE = [Fr(a, 360) * 120 for _, a in ESP]; assert FE == [50, 30, 24, 16]
s5 += levels(
 [prob(L(r"Els 30 alumnes d'una classe tenen aquestes mascotes: gos 12, gat 9, peix 6 i cap 3. Calcula l'angle de cada sector i dibuixa el diagrama.",
         r"Los 30 alumnos de una clase tienen estas mascotas: perro 12, gato 9, pez 6 y ninguna 3. Calcula el ángulo de cada sector y dibuja el diagrama.",
         r"The 30 students in a class have these pets: dog 12, cat 9, fish 6 and none 3. Work out the angle of each slice and draw the chart."),
       P(r"Cada alumne val \(360:30=12^\circ\):", r"Cada alumno vale \(360:30=12^\circ\):", r"Each student is worth \(360:30=12^\circ\):")
       + D(r"12\cdot12=\boxed{144^\circ}\qquad 9\cdot12=\boxed{108^\circ}\qquad 6\cdot12=\boxed{72^\circ}\qquad 3\cdot12=\boxed{36^\circ}"),
       P(r"Comprovem: \(144+108+72+36=360^\circ\).", r"Comprobamos: \(144+108+72+36=360^\circ\).", r"Check: \(144+108+72+36=360^\circ\).") + figs(fig(F_MAS)))],
 [prob(L(r"S'ha preguntat a 120 persones pel seu esport preferit i el resultat és aquest diagrama. Quantes persones han triat cada esport?",
         r"Se ha preguntado a 120 personas por su deporte preferido y el resultado es este diagrama. ¿Cuántas personas han elegido cada deporte?",
         r"120 people were asked about their favourite sport and this is the result. How many people chose each sport?") + figs(fig(F_ESP)),
       P(r"Ara fem el camí al revés: \(f_i=\dfrac{\text{angle}}{360^\circ}\cdot N\).", r"Ahora hacemos el camino al revés: \(f_i=\dfrac{\text{ángulo}}{360^\circ}\cdot N\).", r"Now we go the other way: \(f_i=\dfrac{\text{angle}}{360^\circ}\cdot N\)."),
       D(r"\tfrac{150}{360}\cdot120=\boxed{50}\qquad \tfrac{90}{360}\cdot120=\boxed{30}\qquad \tfrac{72}{360}\cdot120=\boxed{24}\qquad \tfrac{48}{360}\cdot120=\boxed{16}"),
       P(r"Comprovem: \(50+30+24+16=120\).", r"Comprobamos: \(50+30+24+16=120\).", r"Check: \(50+30+24+16=120\)."))],
 [prob(L(r"En un diagrama de sectors sobre el lloc de vacances, el sector «platja» fa \(162^\circ\) i correspon a 45 persones. Quantes persones s'han enquestat? Quin percentatge ha triat la platja?",
         r"En un diagrama de sectores sobre el lugar de vacaciones, el sector «playa» mide \(162^\circ\) y corresponde a 45 personas. ¿Cuántas personas se han encuestado? ¿Qué porcentaje ha elegido la playa?",
         r"In a pie chart about holiday destinations, the “beach” slice measures \(162^\circ\) and stands for 45 people. How many people were surveyed? What percentage chose the beach?"),
       P(r"Si 45 persones ocupen \(162^\circ\), cada persona ocupa \(162:45=3\dc 6^\circ\). Tot el cercle:", r"Si 45 personas ocupan \(162^\circ\), cada persona ocupa \(162:45=3\dc 6^\circ\). Todo el círculo:", r"If 45 people take up \(162^\circ\), each person takes up \(162:45=3\dc 6^\circ\). The whole circle:")
       + D(r"N=360:3\dc 6=\boxed{100}\ \tri{persones}{personas}{people}"),
       P(r"Percentatge: \(\dfrac{45}{100}=\boxed{45\ \%}\) (o també \(\dfrac{162}{360}=0\dc 45\)).", r"Porcentaje: \(\dfrac{45}{100}=\boxed{45\ \%}\) (o también \(\dfrac{162}{360}=0\dc 45\)).", r"Percentage: \(\dfrac{45}{100}=\boxed{45\ \%}\) (or \(\dfrac{162}{360}=0\dc 45\))."))])
ck(Fr(162, 45), '3.6'); ck(360 / Fr(162, 45), 100); ck(Fr(162, 360), '0.45')
s5 += practice([('★☆☆', L(r"En una votació de 36 alumnes, A ha tret 15 vots, B 12 i C 9. Calcula els angles del diagrama de sectors.", r"En una votación de 36 alumnos, A ha sacado 15 votos, B 12 y C 9. Calcula los ángulos del diagrama de sectores.", r"In a vote of 36 students, A got 15 votes, B 12 and C 9. Work out the angles of the pie chart.")),
                ('★★☆', L(r"En un pictograma, cada 🍎 val 20 pomes. Quantes icones dibuixaries per a 90 pomes?", r"En un pictograma, cada 🍎 vale 20 manzanas. ¿Cuántos iconos dibujarías para 90 manzanas?", r"In a pictogram, each 🍎 stands for 20 apples. How many icons would you draw for 90 apples?"))],
               L(r"1) Cada vot val \(10^\circ\): A \(150^\circ\), B \(120^\circ\), C \(90^\circ\). &nbsp; 2) \(90:20=4\dc 5\): quatre pomes i mitja.",
                 r"1) Cada voto vale \(10^\circ\): A \(150^\circ\), B \(120^\circ\), C \(90^\circ\). &nbsp; 2) \(90:20=4\dc 5\): cuatro manzanas y media.",
                 r"1) Each vote is worth \(10^\circ\): A \(150^\circ\), B \(120^\circ\), C \(90^\circ\). &nbsp; 2) \(90:20=4\dc 5\): four and a half apples."))
ck(Fr(90, 20), '4.5')

# =====================================================================
# 10.6 Moda, mitjana i mediana
# =====================================================================
LEC = [20, 40, 15, 46, 20, 30, 25]
assert mean(LEC) == 28 and median(LEC) == 25 and modes(LEC) == [20]
EV = [7, 9, 3, 8, 10, 6, 8, 5]
assert mean(EV) == 7 and median(EV) == Fr(15, 2) and modes(EV) == [8]
SAL = [1200, 1350, 1250, 5900, 1300]
assert mean(SAL) == 2200 and median(SAL) == 1300
F_LEC = dots(LEC, 10, 50, mean_=28, med=25, step=5, lab='min')
s6 = box('def', L('Paràmetres de centralització', 'Parámetros de centralización', 'Measures of central tendency'),
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
s6 += box('prop', L('Com cal interpretar-los?', '¿Cómo hay que interpretarlos?', 'How to interpret them'),
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
s6 += (widget('w-params', '🎯', L('Calcula moda, mitjana i mediana', 'Calcula moda, media y mediana', 'Find the mode, mean and median'),
              ['<p class="hint-s">' + L("Escriu les dades separades per espais (pots fer servir decimals).", "Escribe los datos separados por espacios (puedes usar decimales).", "Type the data separated by spaces (decimals are fine).") + '</p>',
               '<div class="wrow">' + tin('d', L('Dades', 'Datos', 'Data'), '20 40 15 46 20 30 25', 'w') + '</div>'])
       + widget('w-balance', '⚖️', L('La mitjana és el punt d’equilibri', 'La media es el punto de equilibrio', 'The mean is the balance point'),
                ['<p class="hint-s">' + L("Mou les cinc dades i mira com canvien la mitjana (triangle) i la mediana (línia). Prova a portar una dada molt lluny!", "Mueve los cinco datos y mira cómo cambian la media (triángulo) y la mediana (línea). ¡Prueba a llevar un dato muy lejos!", "Move the five values and watch the mean (triangle) and the median (line) change. Try moving one value far away!") + '</p>']
                + ['<div class="wrow">' + rng('v%d' % i, 0, 20, 1, v, 'dada %d' % (i + 1)) + '</div>' for i, v in enumerate([4, 6, 7, 9, 9])])
       + drill('mitjana', 'Entrena: calcula la mitjana', 'Entrena: calcula la media', 'Train: find the mean')
       + drill('mediana', 'Entrena: calcula la mediana', 'Entrena: calcula la mediana', 'Train: find the median')
       + drill('moda', 'Entrena: troba la moda', 'Entrena: encuentra la moda', 'Train: find the mode', 'opts'))

P61 = [6, 8, 5, 9, 6, 7, 4, 6, 9]
assert mean(P61) == Fr(60, 9) and median(P61) == 6 and modes(P61) == [6]
P62 = [12, 15, 11, 14, 18, 15, 13, 16, 12, 14]
assert mean(P62) == 14 and median(P62) == 14 and modes(P62) == [12, 14, 15]
s6 += levels(
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
s6 += practice([('★☆☆', L(r"Calcula la moda, la mitjana i la mediana de: \(3,\ 7,\ 4,\ 7,\ 9\).", r"Calcula la moda, la media y la mediana de: \(3,\ 7,\ 4,\ 7,\ 9\).", r"Find the mode, mean and median of: \(3,\ 7,\ 4,\ 7,\ 9\).")),
                ('★★☆', L(r"Afig una dada a la llista anterior perquè la mediana passe a ser \(5\dc 5\).", r"Añade un dato a la lista anterior para que la mediana pase a ser \(5\dc 5\).", r"Add one value to the list above so that the median becomes \(5\dc 5\)."))],
               L(r"1) \(Mo=7\), \(\bar x=\frac{30}{5}=6\), \(Me=7\) (\(3,\ 4,\ 7,\ 7,\ 9\)). &nbsp; 2) Amb sis dades, les centrals han de sumar 11: si afegim un 4, queda \(3,\ 4,\ 4,\ 7,\ 7,\ 9\) i \(Me=\frac{4+7}{2}=5\dc 5\).",
                 r"1) \(Mo=7\), \(\bar x=\frac{30}{5}=6\), \(Me=7\) (\(3,\ 4,\ 7,\ 7,\ 9\)). &nbsp; 2) Con seis datos, los centrales tienen que sumar 11: si añadimos un 4, queda \(3,\ 4,\ 4,\ 7,\ 7,\ 9\) y \(Me=\frac{4+7}{2}=5\dc 5\).",
                 r"1) \(Mo=7\), \(\bar x=\frac{30}{5}=6\), \(Me=7\) (\(3,\ 4,\ 7,\ 7,\ 9\)). &nbsp; 2) With six values, the middle two must add up to 11: adding a 4 gives \(3,\ 4,\ 4,\ 7,\ 7,\ 9\) and \(Me=\frac{4+7}{2}=5\dc 5\)."))
assert median(P6P + [4]) == Fr(11, 2)
