# Apartat 9.4 dels apunts de la Unitat 9 de 4t ESO Matemàtiques A (Estadística): gràfics estadístics (barres, polígons,
# histogrames, sectors i pictogrames). Ajunta els apartats 10.4 i 10.5 de ../1eso-t10/s456.py.
from comu import *
from s123 import TG, NG, EDG, FA, S3B, EDB, FB, acc

FRU = [(L('Poma', 'Manzana', 'Apple'), 8), (L('Plàtan', 'Plátano', 'Banana'), 6), (L('Taronja', 'Naranja', 'Orange'), 5), (L('Maduixa', 'Fresa', 'Strawberry'), 4), (L('Pera', 'Pera', 'Pear'), 2)]
FRUs = [(Ls('Poma', 'Manzana', 'Apple'), 8), (Ls('Plàtan', 'Plátano', 'Banana'), 6), (Ls('Taronja', 'Naranja', 'Orange'), 5), (Ls('Maduixa', 'Fresa', 'Strawberry'), 4), (Ls('Pera', 'Pera', 'Pear'), 2)]
assert sum(f for _, f in FRU) == 25
FREQ = Ls('Freqüència', 'Frecuencia', 'Frequency')
NALU = Ls("Nre. d'alumnes", 'N.º de alumnos', 'Students')

# =====================================================================
# 9.4 Gràfics estadístics
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
                ['<p class="hint-s">' + L("Les 30 alçades de l'exemple de l'apartat 9.3. Si els intervals són massa estrets o massa amples, el gràfic ens diu menys coses.",
                                          "Las 30 alturas del ejemplo del apartado 9.3. Si los intervalos son demasiado estrechos o demasiado anchos, el gráfico nos dice menos cosas.",
                                          "The 30 heights from the example in section 9.3. If the intervals are too narrow or too wide, the chart tells us less.") + '</p>',
                 seg([('2', L('Amplària 2', 'Anchura 2', 'Width 2')), ('5', L('Amplària 5', 'Anchura 5', 'Width 5')), ('10', L('Amplària 10', 'Anchura 10', 'Width 10'))], 1),
                 seg([('0', L('Sense polígon', 'Sin polígono', 'No polygon')), ('1', L('Amb polígon', 'Con polígono', 'With polygon'))])])
       + drill('readbar', 'Entrena: llig el diagrama de barres', 'Entrena: lee el diagrama de barras', 'Train: read the bar chart'))

TRA = [(L('Caminant', 'Andando', 'Walking'), Ls('Caminant', 'Andando', 'Walking'), 10), (L('Autobús', 'Autobús', 'Bus'), Ls('Autobús', 'Autobús', 'Bus'), 6),
       (L('Cotxe', 'Coche', 'Car'), Ls('Cotxe', 'Coche', 'Car'), 5), (L('Bici', 'Bici', 'Bike'), Ls('Bici', 'Bici', 'Bike'), 3)]
NT = sum(f for *_, f in TRA); assert NT == 24
ANG = [Fr(f * 360, NT) for *_, f in TRA]; assert ANG == [150, 90, 75, 45] and sum(ANG) == 360
F_TRA = sectors([s for _, s, _ in TRA], [f for *_, f in TRA], angles=True)
LIB = [(Ls('Gener', 'Enero', 'January'), 40), (Ls('Febrer', 'Febrero', 'February'), 35), (Ls('Març', 'Marzo', 'March'), 50), (Ls('Abril', 'Abril', 'April'), 25)]
F_LIB = picto([c for c, _ in LIB], [v for _, v in LIB], 10, '📘')
s4 += box('def', L('Diagrama de sectors', 'Diagrama de sectores', 'Pie chart'),
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
s4 += box('prop', L('Pictogrames', 'Pictogramas', 'Pictograms'),
  P(r"Un <strong>pictograma</strong> representa les freqüències amb <strong>dibuixos</strong> relacionats amb el tema. Cal indicar quant val cada dibuix; un tros de dibuix val la part corresponent.",
    r"Un <strong>pictograma</strong> representa las frecuencias con <strong>dibujos</strong> relacionados con el tema. Hay que indicar cuánto vale cada dibujo; un trozo de dibujo vale la parte correspondiente.",
    r"A <strong>pictogram</strong> shows the frequencies with <strong>pictures</strong> related to the topic. We must say what each picture is worth; part of a picture is worth that part.")
  + figs(fig(F_LIB, L('Llibres prestats per la biblioteca (📘 = 10 llibres)', 'Libros prestados por la biblioteca (📘 = 10 libros)', 'Books lent by the library (📘 = 10 books)')))
  + P(r"Al febrer hi ha tres llibres i mig: \(3\dc 5\cdot10=35\) llibres prestats.", r"En febrero hay tres libros y medio: \(3\dc 5\cdot10=35\) libros prestados.", r"In February there are three and a half books: \(3\dc 5\cdot10=35\) books lent."))
s4 += (widget('w-pie', '🥧', L('Diagrama de sectors pas a pas', 'Diagrama de sectores paso a paso', 'Pie chart step by step'),
              ['<p class="hint-s">' + L("Escriu els valors i les freqüències o tria un exemple: l'eina calcula l'angle de cada sector.", "Escribe los valores y las frecuencias o elige un ejemplo: la herramienta calcula el ángulo de cada sector.", "Type the values and frequencies or choose an example: the tool works out each slice's angle.") + '</p>',
               seg([('tra', L('Transport', 'Transporte', 'Transport')), ('fru', L('Fruita', 'Fruta', 'Fruit')), ('own', L('Els meus', 'Los míos', 'My own'))]),
               '<div class="wrow">' + tin('x', L('Valors', 'Valores', 'Values'), '', 'w') + '</div><div class="wrow">' + tin('f', '<i>f</i><sub>i</sub>', '', 'w') + '</div>',
               seg([('pie', L('Sectors', 'Sectores', 'Pie chart')), ('pic', L('Pictograma', 'Pictograma', 'Pictogram'))])])
       + drill('angle', "Entrena: calcula l'angle del sector", 'Entrena: calcula el ángulo del sector', 'Train: work out the slice angle')
       + drill('pieread', 'Entrena: del sector a la freqüència', 'Entrena: del sector a la frecuencia', 'Train: from slice to frequency'))

PETS = [(0, 6), (1, 10), (2, 5), (3, 3)]
F_PETS = barres([str(x) for x, _ in PETS], [f for _, f in PETS], yl=NALU, xl=Ls('mascotes', 'mascotas', 'pets'))
NP = sum(f for _, f in PETS); assert NP == 24
ck(sum(x * f for x, f in PETS), 29)
F_TB = hist(EDB, FB, poly=True, yl=NALU, xl='min')
VEND = [52, 48, 55, 50]
F_V1 = barres(['A', 'B', 'C', 'D'], VEND, yl=Ls('vendes', 'ventas', 'sales'), y0=45, step=1, H=170)
F_V2 = barres(['A', 'B', 'C', 'D'], VEND, yl=Ls('vendes', 'ventas', 'sales'), step=10, H=170)
S4L = (
 [prob(L(r"Aquest diagrama mostra quantes mascotes tenen els alumnes d'una classe. Fes la taula de freqüències. Quants alumnes hi ha? Quantes mascotes tenen en total?",
         r"Este diagrama muestra cuántas mascotas tienen los alumnos de una clase. Haz la tabla de frecuencias. ¿Cuántos alumnos hay? ¿Cuántas mascotas tienen en total?",
         r"This chart shows how many pets the students in a class have. Make the frequency table. How many students are there? How many pets do they have altogether?") + figs(fig(F_PETS)),
       P(r"Llegim l'altura de cada barra:", r"Leemos la altura de cada barra:", r"Read the height of each bar:") + tbl([M('x_i'), '0', '1', '2', '3', 'Total'], [[M('f_i'), '6', '10', '5', '3', '24']], 'c'),
       P(r"Hi ha \(\boxed{24}\) alumnes. Mascotes: \(0\cdot6+1\cdot10+2\cdot5+3\cdot3=0+10+10+9=\boxed{29}\).", r"Hay \(\boxed{24}\) alumnos. Mascotas: \(0\cdot6+1\cdot10+2\cdot5+3\cdot3=0+10+10+9=\boxed{29}\).", r"There are \(\boxed{24}\) students. Pets: \(0\cdot6+1\cdot10+2\cdot5+3\cdot3=0+10+10+9=\boxed{29}\)."))],
 [prob(L(r"Dibuixa l'histograma i el polígon de freqüències de la taula dels minuts que tarden els alumnes a arribar a l'institut (apartat 9.3).",
         r"Dibuja el histograma y el polígono de frecuencias de la tabla de los minutos que tardan los alumnos en llegar al instituto (apartado 9.3).",
         r"Draw the histogram and frequency polygon for the table of the minutes students take to get to school (section 9.3)."),
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
MAS = [(L('Gos', 'Perro', 'Dog'), Ls('Gos', 'Perro', 'Dog'), 12), (L('Gat', 'Gato', 'Cat'), Ls('Gat', 'Gato', 'Cat'), 9), (L('Peix', 'Pez', 'Fish'), Ls('Peix', 'Pez', 'Fish'), 6), (L('Cap', 'Ninguna', 'None'), Ls('Cap', 'Ninguna', 'None'), 3)]
AM = [Fr(f * 360, 30) for *_, f in MAS]; assert AM == [144, 108, 72, 36]
F_MAS = sectors([s for _, s, _ in MAS], [f for *_, f in MAS], angles=True)
ESP = [(Ls('Futbol', 'Fútbol', 'Football'), 150), (Ls('Bàsquet', 'Baloncesto', 'Basketball'), 90), (Ls('Natació', 'Natación', 'Swimming'), 72), (Ls('Altres', 'Otros', 'Other'), 48)]
assert sum(a for _, a in ESP) == 360
F_ESP = sectors([c for c, _ in ESP], [a for _, a in ESP], angles=True)
FE = [Fr(a, 360) * 120 for _, a in ESP]; assert FE == [50, 30, 24, 16]
S5L = (
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
s4 += levels(S4L[0] + S5L[0], S4L[1] + S5L[1], S4L[2] + S5L[2])
s4 += practice([('★☆☆', L(r"Dibuixa el diagrama de barres i el polígon de freqüències dels gols d'un equip: 0 gols en 2 partits, 1 en 5, 2 en 5, 3 en 2 i 4 en 1.",
                          r"Dibuja el diagrama de barras y el polígono de frecuencias de los goles de un equipo: 0 goles en 2 partidos, 1 en 5, 2 en 5, 3 en 2 y 4 en 1.",
                          r"Draw the bar chart and frequency polygon for a team's goals: 0 goals in 2 matches, 1 in 5, 2 in 5, 3 in 2 and 4 in 1.")),
                ('★☆☆', L(r"En una votació de 36 alumnes, A ha tret 15 vots, B 12 i C 9. Calcula els angles del diagrama de sectors.", r"En una votación de 36 alumnos, A ha sacado 15 votos, B 12 y C 9. Calcula los ángulos del diagrama de sectores.", r"In a vote of 36 students, A got 15 votes, B 12 and C 9. Work out the angles of the pie chart.")),
                ('★★☆', L(r"Quin tipus de gràfic faries per a: a) l'esport preferit; b) el pes de 40 persones; c) el nombre de cotxes de cada família?",
                          r"¿Qué tipo de gráfico harías para: a) el deporte preferido; b) el peso de 40 personas; c) el número de coches de cada familia?",
                          r"What kind of chart would you draw for: a) favourite sport; b) the weight of 40 people; c) the number of cars each family has?"))],
               L(r"1) Barres d'altures 2, 5, 5, 2 i 1 sobre 0, 1, 2, 3 i 4; el polígon uneix els extrems de dalt. &nbsp; 2) Cada vot val \(10^\circ\): A \(150^\circ\), B \(120^\circ\), C \(90^\circ\). &nbsp; 3) a) diagrama de barres o de sectors; b) histograma (variable contínua, agrupada en intervals); c) diagrama de barres.",
                 r"1) Barras de alturas 2, 5, 5, 2 y 1 sobre 0, 1, 2, 3 y 4; el polígono une los extremos de arriba. &nbsp; 2) Cada voto vale \(10^\circ\): A \(150^\circ\), B \(120^\circ\), C \(90^\circ\). &nbsp; 3) a) diagrama de barras o de sectores; b) histograma (variable continua, agrupada en intervalos); c) diagrama de barras.",
                 r"1) Bars of heights 2, 5, 5, 2 and 1 over 0, 1, 2, 3 and 4; the polygon joins the tops. &nbsp; 2) Each vote is worth \(10^\circ\): A \(150^\circ\), B \(120^\circ\), C \(90^\circ\). &nbsp; 3) a) bar chart or pie chart; b) histogram (continuous variable, grouped into intervals); c) bar chart."))
