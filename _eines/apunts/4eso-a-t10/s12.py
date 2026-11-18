# Apartats 10.1 i 10.2 dels apunts de la Unitat 10 de 4t ESO Matemàtiques A (Estadística bidimensional): distribucions
# bidimensionals (parelles de dades, taules simples i de doble entrada, tipus de relació) i núvol de punts (amb el centre de gravetat).
from comu import *

# =====================================================================
# 10.1 Distribucions bidimensionals
# =====================================================================
# 10 alumnes: hores d'estudi (X) i nota (Y); fil conductor dels apartats 10.1-10.3
HX = [1, 2, 2, 3, 3, 4, 5, 5, 6, 7]
HY = [3, 3, 5, 4, 6, 6, 7, 8, 8, 9]
SH = bi(HX, HY)
ck(SH['sx'], 38); ck(SH['sy'], 59); ck(SH['mx'], '3.8'); ck(SH['my'], '5.9')
XL_H = L('Hores', 'Horas', 'Hours') + ' ' + M('(x_i)'); YL_H = L('Nota', 'Nota', 'Mark') + ' ' + M('(y_i)')

s1 = box('def', L('Variables estadístiques bidimensionals', 'Variables estadísticas bidimensionales', 'Two-variable (bivariate) data'),
  P(r"A la unitat anterior estudiàvem <strong>una sola</strong> característica de cada individu. Moltes vegades, però, ens interessa saber si <strong>dues característiques</strong> estan relacionades: si qui estudia més trau més bona nota, si les persones més altes pesen més, si quan fa més calor es venen més gelats…",
    r"En la unidad anterior estudiábamos <strong>una sola</strong> característica de cada individuo. Muchas veces, sin embargo, nos interesa saber si <strong>dos características</strong> están relacionadas: si quien estudia más saca mejor nota, si las personas más altas pesan más, si cuando hace más calor se venden más helados…",
    r"In the previous unit we studied <strong>a single</strong> feature of each individual. Often, though, we want to know whether <strong>two features</strong> are related: whether people who study more get better marks, whether taller people weigh more, whether more ice creams are sold when it's hotter…")
  + ul(L(r"Una <strong>variable estadística bidimensional</strong> \((X,\,Y)\) estudia <strong>dues variables</strong> \(X\) i \(Y\) sobre els <strong>mateixos individus</strong>.",
         r"Una <strong>variable estadística bidimensional</strong> \((X,\,Y)\) estudia <strong>dos variables</strong> \(X\) e \(Y\) sobre los <strong>mismos individuos</strong>.",
         r"A <strong>bivariate statistical variable</strong> \((X,\,Y)\) studies <strong>two variables</strong> \(X\) and \(Y\) on the <strong>same individuals</strong>."),
       L(r"Cada individu ens dona una <strong>parella de valors</strong> \((x_i,\,y_i)\): el primer és el valor de \(X\) i el segon, el de \(Y\).",
         r"Cada individuo nos da una <strong>pareja de valores</strong> \((x_i,\,y_i)\): el primero es el valor de \(X\) y el segundo, el de \(Y\).",
         r"Each individual gives us a <strong>pair of values</strong> \((x_i,\,y_i)\): the first is the value of \(X\) and the second the value of \(Y\)."),
       L(r"El conjunt de totes les parelles és una <strong>distribució bidimensional</strong>. El nombre de parelles és \(N\).",
         r"El conjunto de todas las parejas es una <strong>distribución bidimensional</strong>. El número de parejas es \(N\).",
         r"The set of all the pairs is a <strong>bivariate distribution</strong>. The number of pairs is \(N\)."))
  + box('ex', L("Exemple: hores d'estudi i nota", 'Ejemplo: horas de estudio y nota', 'Example: study hours and mark'),
        P(r"Hem preguntat a 10 alumnes quantes hores han estudiat per a un examen (\(X\)) i quina nota han tret (\(Y\)):",
          r"Hemos preguntado a 10 alumnos cuántas horas han estudiado para un examen (\(X\)) y qué nota han sacado (\(Y\)):",
          r"We asked 10 students how many hours they studied for a test (\(X\)) and what mark they got (\(Y\)):")
        + ptab(HX, HY, XL_H, YL_H)
        + P(r"La primera alumna ha estudiat 1 hora i ha tret un 3: la parella \((1,\,3)\). La darrera ha estudiat 7 hores i ha tret un 9: \((7,\,9)\). En total hi ha \(N=10\) parelles.",
            r"La primera alumna ha estudiado 1 hora y ha sacado un 3: la pareja \((1,\,3)\). La última ha estudiado 7 horas y ha sacado un 9: \((7,\,9)\). En total hay \(N=10\) parejas.",
            r"The first student studied for 1 hour and got a 3: the pair \((1,\,3)\). The last one studied for 7 hours and got a 9: \((7,\,9)\). Altogether there are \(N=10\) pairs."))
  + note(r"L'ordre importa: \((2,\,5)\) vol dir «2 hores i un 5», que no és el mateix que \((5,\,2)\), «5 hores i un 2».",
         r"El orden importa: \((2,\,5)\) quiere decir «2 horas y un 5», que no es lo mismo que \((5,\,2)\), «5 horas y un 2».",
         r"Order matters: \((2,\,5)\) means “2 hours and a 5”, which isn't the same as \((5,\,2)\), “5 hours and a 2”.", '⚠️'))

# taula de doble entrada: 20 famílies, fills (X) i cotxes (Y)
DBL = {1: [2, 4, 1], 2: [1, 5, 3], 3: [0, 1, 3]}; DY = [0, 1, 2]
FX = {k: sum(v) for k, v in DBL.items()}; FY = [sum(DBL[k][j] for k in DBL) for j in range(3)]
assert FX == {1: 7, 2: 9, 3: 4} and FY == [3, 10, 7] and sum(FX.values()) == 20
def dtab2():
    head = ['<span class="dg">' + M(r'X\backslash Y') + '</span>'] + [M(str(y)) for y in DY] + [M('f_x')]
    rows = [[M(str(k))] + [M(str(f)) for f in DBL[k]] + [M(r'\mathbf{%d}' % FX[k])] for k in DBL]
    rows.append([M('f_y')] + [M(r'\mathbf{%d}' % f) for f in FY] + [M(r'\mathbf{20}')])
    return tbl(head, rows, 'c freq dbl')
s1 += box('prop', L('Taules de dades bidimensionals', 'Tablas de datos bidimensionales', 'Tables of bivariate data'),
  ul(L(r"Si hi ha poques dades, les posem en una <strong>taula simple</strong>, amb dues files (o dues columnes): una per a \(X\) i una altra per a \(Y\), com en l'exemple de les hores d'estudi.",
       r"Si hay pocos datos, los ponemos en una <strong>tabla simple</strong>, con dos filas (o dos columnas): una para \(X\) y otra para \(Y\), como en el ejemplo de las horas de estudio.",
       r"With few data we use a <strong>simple table</strong> with two rows (or two columns): one for \(X\) and another for \(Y\), as in the study-hours example."),
     L(r"Si hi ha moltes dades i les parelles es repeteixen, fem una <strong>taula de doble entrada</strong>: els valors de \(X\) en les files, els de \(Y\) en les columnes i, en cada casella, quantes vegades apareix eixa parella (la seua <strong>freqüència</strong>).",
       r"Si hay muchos datos y las parejas se repiten, hacemos una <strong>tabla de doble entrada</strong>: los valores de \(X\) en las filas, los de \(Y\) en las columnas y, en cada casilla, cuántas veces aparece esa pareja (su <strong>frecuencia</strong>).",
       r"With lots of data and repeated pairs we make a <strong>two-way table</strong>: the values of \(X\) in the rows, those of \(Y\) in the columns and, in each cell, how many times that pair appears (its <strong>frequency</strong>)."))
  + box('ex', L('Exemple: fills i cotxes de 20 famílies', 'Ejemplo: hijos y coches de 20 familias', 'Example: children and cars of 20 families'),
        P(r"Hem preguntat a 20 famílies quants fills tenen (\(X\)) i quants cotxes (\(Y\)):", r"Hemos preguntado a 20 familias cuántos hijos tienen (\(X\)) y cuántos coches (\(Y\)):", r"We asked 20 families how many children (\(X\)) and how many cars (\(Y\)) they have:")
        + dtab2()
        + ul(L(r"Hi ha <strong>5 famílies</strong> amb 2 fills i 1 cotxe (fila 2, columna 1).", r"Hay <strong>5 familias</strong> con 2 hijos y 1 coche (fila 2, columna 1).", r"There are <strong>5 families</strong> with 2 children and 1 car (row 2, column 1)."),
             L(r"La <strong>darrera columna</strong> (\(f_x\)) suma cada fila: 7 famílies tenen 1 fill, 9 en tenen 2 i 4 en tenen 3. És la distribució de \(X\) tota sola.",
               r"La <strong>última columna</strong> (\(f_x\)) suma cada fila: 7 familias tienen 1 hijo, 9 tienen 2 y 4 tienen 3. Es la distribución de \(X\) sola.",
               r"The <strong>last column</strong> (\(f_x\)) adds up each row: 7 families have 1 child, 9 have 2 and 4 have 3. It's the distribution of \(X\) on its own."),
             L(r"La <strong>darrera fila</strong> (\(f_y\)) suma cada columna: 3 famílies no tenen cotxe, 10 en tenen 1 i 7 en tenen 2. És la distribució de \(Y\). Totes dues sumen \(N=20\).",
               r"La <strong>última fila</strong> (\(f_y\)) suma cada columna: 3 familias no tienen coche, 10 tienen 1 y 7 tienen 2. Es la distribución de \(Y\). Las dos suman \(N=20\).",
               r"The <strong>last row</strong> (\(f_y\)) adds up each column: 3 families have no car, 10 have 1 and 7 have 2. It's the distribution of \(Y\). Both add up to \(N=20\)."))))
s1 += widget('w-dbl', '🧮', L('Fes la taula de doble entrada', 'Haz la tabla de doble entrada', 'Build the two-way table'),
  ['<p class="hint-s">' + L("Escriu els valors de X i de Y en el mateix ordre (la 1a dada de X va amb la 1a de Y…). L'eina compta les parelles i fa la taula amb els totals.",
                            "Escribe los valores de X y de Y en el mismo orden (el 1.er dato de X va con el 1.º de Y…). La herramienta cuenta las parejas y hace la tabla con los totales.",
                            "Type the values of X and Y in the same order (the 1st X value goes with the 1st Y value…). The tool counts the pairs and builds the table with the totals.") + '</p>',
   '<div class="wrow">' + tin('x', 'X', '1 2 2 3 1 2 1 3 2 2 1 3', 'w') + '</div><div class="wrow">' + tin('y', 'Y', '0 1 1 2 1 2 1 2 1 0 2 1', 'w') + '</div>'], out='<div class="tout"></div>')

s1 += box('def', L('Tipus de relació entre dues variables', 'Tipos de relación entre dos variables', 'Types of relationship between two variables'),
  ul(L(r"<strong>Relació funcional</strong>: el valor de \(X\) <strong>determina exactament</strong> el de \(Y\); hi ha una fórmula. Exemple: el costat d'un quadrat i el seu perímetre (\(y=4x\)).",
       r"<strong>Relación funcional</strong>: el valor de \(X\) <strong>determina exactamente</strong> el de \(Y\); hay una fórmula. Ejemplo: el lado de un cuadrado y su perímetro (\(y=4x\)).",
       r"<strong>Functional relationship</strong>: the value of \(X\) <strong>determines exactly</strong> the value of \(Y\); there is a formula. Example: the side of a square and its perimeter (\(y=4x\))."),
     L(r"<strong>Relació estadística</strong>: hi ha una <strong>tendència</strong>, però no una fórmula exacta. Exemple: l'alçada i el pes. Les persones més altes solen pesar més, però dues persones amb la mateixa alçada poden pesar diferent.",
       r"<strong>Relación estadística</strong>: hay una <strong>tendencia</strong>, pero no una fórmula exacta. Ejemplo: la altura y el peso. Las personas más altas suelen pesar más, pero dos personas con la misma altura pueden pesar distinto.",
       r"<strong>Statistical relationship</strong>: there is a <strong>trend</strong> but no exact formula. Example: height and weight. Taller people tend to weigh more, but two people of the same height can weigh different amounts."),
     L(r"<strong>Cap relació</strong> (variables <strong>independents</strong>): conéixer \(X\) no ens diu res de \(Y\). Exemple: el número de calçat i la nota de matemàtiques.",
       r"<strong>Ninguna relación</strong> (variables <strong>independientes</strong>): conocer \(X\) no nos dice nada de \(Y\). Ejemplo: el número de calzado y la nota de matemáticas.",
       r"<strong>No relationship</strong> (<strong>independent</strong> variables): knowing \(X\) tells us nothing about \(Y\). Example: shoe size and maths mark."))
  + P(r"L'estadística bidimensional estudia sobretot les <strong>relacions estadístiques</strong>: com de forta és la relació i com podem fer-la servir per a fer <strong>previsions</strong>.",
      r"La estadística bidimensional estudia sobre todo las <strong>relaciones estadísticas</strong>: lo fuerte que es la relación y cómo podemos usarla para hacer <strong>previsiones</strong>.",
      r"Bivariate statistics mainly studies <strong>statistical relationships</strong>: how strong the relationship is and how we can use it to make <strong>predictions</strong>.")
  + drill('rel', 'Entrena: quin tipus de relació hi ha?', 'Entrena: ¿qué tipo de relación hay?', 'Train: what type of relationship is it?', 'opts'))

P1X = [150, 155, 160, 165, 170, 175]; P1Y = [45, 52, 54, 60, 63, 70]
s1 += levels(
 [prob(L(r"Digues quin tipus de relació (funcional, estadística o cap) hi ha entre les variables: a) quilos de taronges que comprem i preu que paguem, si costen 1,20 €/kg; b) temperatura d'un dia i persones que van a la platja; c) dia del mes en què has nascut i alçada.",
         r"Di qué tipo de relación (funcional, estadística o ninguna) hay entre las variables: a) kilos de naranjas que compramos y precio que pagamos, si cuestan 1,20 €/kg; b) temperatura de un día y personas que van a la playa; c) día del mes en que has nacido y altura.",
         r"Say what type of relationship (functional, statistical or none) there is between the variables: a) kilos of oranges we buy and the price we pay, at €1.20/kg; b) the temperature on a day and how many people go to the beach; c) the day of the month you were born and your height."),
       P(r"a) <strong>Funcional</strong>: \(y=1\dc 2\,x\). &nbsp; b) <strong>Estadística</strong>: quan fa més calor hi sol anar més gent, però no hi ha una fórmula exacta. &nbsp; c) <strong>Cap</strong>: són independents.",
         r"a) <strong>Funcional</strong>: \(y=1\dc 2\,x\). &nbsp; b) <strong>Estadística</strong>: cuando hace más calor suele ir más gente, pero no hay una fórmula exacta. &nbsp; c) <strong>Ninguna</strong>: son independientes.",
         r"a) <strong>Functional</strong>: \(y=1\dc 2\,x\). &nbsp; b) <strong>Statistical</strong>: more people tend to go when it's hotter, but there's no exact formula. &nbsp; c) <strong>None</strong>: they're independent.")),
  prob(L(r"Amb la taula dels fills i els cotxes de les 20 famílies: quantes famílies tenen 3 fills i 2 cotxes? Quantes tenen 2 cotxes? Quin percentatge de famílies té 1 fill?",
         r"Con la tabla de los hijos y los coches de las 20 familias: ¿cuántas familias tienen 3 hijos y 2 coches? ¿Cuántas tienen 2 coches? ¿Qué porcentaje de familias tiene 1 hijo?",
         r"Using the table of the 20 families' children and cars: how many families have 3 children and 2 cars? How many have 2 cars? What percentage of families have 1 child?"),
       P(r"3 fills i 2 cotxes: \(\boxed{3}\) famílies. Amb 2 cotxes (total de la columna 2): \(1+3+3=\boxed{7}\). Amb 1 fill: \(\frac{7}{20}=0\dc 35\to\boxed{35\ \%}\).",
         r"3 hijos y 2 coches: \(\boxed{3}\) familias. Con 2 coches (total de la columna 2): \(1+3+3=\boxed{7}\). Con 1 hijo: \(\frac{7}{20}=0\dc 35\to\boxed{35\ \%}\).",
         r"3 children and 2 cars: \(\boxed{3}\) families. With 2 cars (column 2 total): \(1+3+3=\boxed{7}\). With 1 child: \(\frac{7}{20}=0\dc 35\to\boxed{35\ \%}\)."))],
 [prob(L(r"En la taula de les 20 famílies, quantes famílies tenen més fills que cotxes?", r"En la tabla de las 20 familias, ¿cuántas familias tienen más hijos que coches?", r"In the table of the 20 families, how many families have more children than cars?"),
       P(r"Són les caselles amb \(x>y\): \((1,0)\), \((2,0)\), \((2,1)\), \((3,0)\), \((3,1)\) i \((3,2)\): \(2+1+5+0+1+3=\boxed{12}\) famílies.",
         r"Son las casillas con \(x>y\): \((1,0)\), \((2,0)\), \((2,1)\), \((3,0)\), \((3,1)\) y \((3,2)\): \(2+1+5+0+1+3=\boxed{12}\) familias.",
         r"They're the cells with \(x>y\): \((1,0)\), \((2,0)\), \((2,1)\), \((3,0)\), \((3,1)\) and \((3,2)\): \(2+1+5+0+1+3=\boxed{12}\) families.")),
  prob(L(r"Aquestes són les alçades (cm) i els pesos (kg) de sis persones. Escriu les parelles de dades. Hi ha relació funcional o estadística? Per què?",
         r"Estas son las alturas (cm) y los pesos (kg) de seis personas. Escribe las parejas de datos. ¿Hay relación funcional o estadística? ¿Por qué?",
         r"These are the heights (cm) and weights (kg) of six people. Write down the pairs of data. Is the relationship functional or statistical? Why?")
       + ptab(P1X, P1Y, L('Alçada', 'Altura', 'Height'), L('Pes', 'Peso', 'Weight')),
       P(r"\((150,\,45)\), \((155,\,52)\), \((160,\,54)\), \((165,\,60)\), \((170,\,63)\), \((175,\,70)\). És una relació <strong>estadística</strong>: el pes tendeix a créixer amb l'alçada, però cada 5 cm el pes no augmenta sempre el mateix (7, 2, 6, 3, 7 kg) i no hi ha cap fórmula que ho done exactament.",
         r"\((150,\,45)\), \((155,\,52)\), \((160,\,54)\), \((165,\,60)\), \((170,\,63)\), \((175,\,70)\). Es una relación <strong>estadística</strong>: el peso tiende a crecer con la altura, pero cada 5 cm el peso no aumenta siempre lo mismo (7, 2, 6, 3, 7 kg) y no hay ninguna fórmula que lo dé exactamente.",
         r"\((150,\,45)\), \((155,\,52)\), \((160,\,54)\), \((165,\,60)\), \((170,\,63)\), \((175,\,70)\). It's a <strong>statistical</strong> relationship: weight tends to go up with height, but each 5 cm the weight doesn't always rise by the same amount (7, 2, 6, 3, 7 kg) and there's no formula that gives it exactly."))],
 [prob(L(r"Inventa una situació en què hi haja una relació funcional, una altra amb una relació estadística i una tercera sense relació. Explica per què.",
         r"Inventa una situación en la que haya una relación funcional, otra con una relación estadística y una tercera sin relación. Explica por qué.",
         r"Make up one situation with a functional relationship, another with a statistical relationship and a third with no relationship. Explain why."),
       P(r"Per exemple: <strong>funcional</strong>, els minuts d'una cridada i el preu si cada minut costa 0,10 € (\(y=0\dc 1\,x\)); <strong>estadística</strong>, les hores que dorms i el cansament l'endemà (hi ha tendència, però depén de moltes altres coses); <strong>cap relació</strong>, el color dels ulls i el número del DNI. Hi ha moltes altres respostes.",
         r"Por ejemplo: <strong>funcional</strong>, los minutos de una llamada y el precio si cada minuto cuesta 0,10 € (\(y=0\dc 1\,x\)); <strong>estadística</strong>, las horas que duermes y el cansancio al día siguiente (hay tendencia, pero depende de muchas otras cosas); <strong>ninguna relación</strong>, el color de los ojos y el número del DNI. Hay muchas otras respuestas.",
         r"For example: <strong>functional</strong>, the minutes of a phone call and the price if each minute costs €0.10 (\(y=0\dc 1\,x\)); <strong>statistical</strong>, the hours you sleep and how tired you are the next day (there's a trend, but it depends on lots of other things); <strong>none</strong>, eye colour and your ID-card number. There are many other answers."))])
assert [b - a for a, b in zip(P1Y, P1Y[1:])] == [7, 2, 6, 3, 7]
assert sum(DBL[k][j] for k in DBL for j in range(3) if k > DY[j]) == 12
s1 += practice([('★☆☆', L(r"Amb la taula de les 20 famílies, quantes famílies no tenen cotxe? Quantes tenen exactament 2 fills i 2 cotxes?", r"Con la tabla de las 20 familias, ¿cuántas familias no tienen coche? ¿Cuántas tienen exactamente 2 hijos y 2 coches?", r"Using the table of the 20 families, how many families have no car? How many have exactly 2 children and 2 cars?")),
                ('★★☆', L(r"Fes la taula de doble entrada de les parelles \((1,1),\ (2,1),\ (1,0),\ (2,2),\ (1,1),\ (2,1),\ (2,1),\ (1,0)\).", r"Haz la tabla de doble entrada de las parejas \((1,1),\ (2,1),\ (1,0),\ (2,2),\ (1,1),\ (2,1),\ (2,1),\ (1,0)\).", r"Make the two-way table for the pairs \((1,1),\ (2,1),\ (1,0),\ (2,2),\ (1,1),\ (2,1),\ (2,1),\ (1,0)\)."))],
               L(r"1) Sense cotxe: \(3\) famílies. Amb 2 fills i 2 cotxes: \(3\). &nbsp; 2) Fila \(x=1\): \(y=0\to2\), \(y=1\to2\), \(y=2\to0\) (total 4); fila \(x=2\): \(0,\ 3,\ 1\) (total 4); totals de les columnes: \(2,\ 5,\ 1\); \(N=8\).",
                 r"1) Sin coche: \(3\) familias. Con 2 hijos y 2 coches: \(3\). &nbsp; 2) Fila \(x=1\): \(y=0\to2\), \(y=1\to2\), \(y=2\to0\) (total 4); fila \(x=2\): \(0,\ 3,\ 1\) (total 4); totales de las columnas: \(2,\ 5,\ 1\); \(N=8\).",
                 r"1) No car: \(3\) families. 2 children and 2 cars: \(3\). &nbsp; 2) Row \(x=1\): \(y=0\to2\), \(y=1\to2\), \(y=2\to0\) (total 4); row \(x=2\): \(0,\ 3,\ 1\) (total 4); column totals: \(2,\ 5,\ 1\); \(N=8\)."))

# =====================================================================
# 10.2 Núvol de punts
# =====================================================================
NV_H = nuvol(list(zip(HX, HY)), (0, 8, 1), (0, 10, 1), axes=(L('hores', 'horas', 'hours'), L('nota', 'nota', 'mark')))
NV_HM = nuvol(list(zip(HX, HY)), (0, 8, 1), (0, 10, 1), axes=(L('hores', 'horas', 'hours'), L('nota', 'nota', 'mark')), means=True)
s2 = box('def', L('Núvol de punts (diagrama de dispersió)', 'Nube de puntos (diagrama de dispersión)', 'Scatter plot'),
  P(r"Per a veure d'un colp d'ull si dues variables estan relacionades, representem cada parella \((x_i,\,y_i)\) com un <strong>punt</strong> en uns eixos de coordenades: \(X\) en l'eix horitzontal i \(Y\) en el vertical. El dibuix que s'obté és el <strong>núvol de punts</strong> (o diagrama de dispersió).",
    r"Para ver de un vistazo si dos variables están relacionadas, representamos cada pareja \((x_i,\,y_i)\) como un <strong>punto</strong> en unos ejes de coordenadas: \(X\) en el eje horizontal e \(Y\) en el vertical. El dibujo que se obtiene es la <strong>nube de puntos</strong> (o diagrama de dispersión).",
    r"To see at a glance whether two variables are related, we plot each pair \((x_i,\,y_i)\) as a <strong>point</strong> on a set of axes: \(X\) on the horizontal axis and \(Y\) on the vertical one. The picture we get is a <strong>scatter plot</strong>.")
  + ol(L(r"Tria una <strong>escala</strong> per a cada eix que permeta dibuixar totes les dades (no cal que siga la mateixa en els dos eixos). Posa el nom de cada variable en el seu eix.",
         r"Elige una <strong>escala</strong> para cada eje que permita dibujar todos los datos (no hace falta que sea la misma en los dos ejes). Pon el nombre de cada variable en su eje.",
         r"Choose a <strong>scale</strong> for each axis that fits all the data (it needn't be the same on both axes). Label each axis with its variable."),
       L(r"Dibuixa un punt per a cada parella, com quan representes punts en el pla.", r"Dibuja un punto para cada pareja, como cuando representas puntos en el plano.", r"Plot a point for each pair, just as when you plot points on a grid."),
       L(r"Si una parella es repeteix, pots escriure al costat del punt quantes vegades apareix (o fer el punt més gros).", r"Si una pareja se repite, puedes escribir al lado del punto cuántas veces aparece (o hacer el punto más grande).", r"If a pair is repeated, write next to the point how many times it appears (or make the dot bigger)."))
  + box('ex', L("Exemple: el núvol de les hores d'estudi i les notes", 'Ejemplo: la nube de las horas de estudio y las notas', 'Example: the scatter plot of study hours and marks'),
        ptab(HX, HY, XL_H, YL_H) + fig(NV_H)
        + P(r"Els punts «pugen» cap a la dreta: els alumnes que han estudiat més hores han tret, en general, més bona nota. No estan exactament en una recta, però s'hi acosten bastant.",
            r"Los puntos «suben» hacia la derecha: los alumnos que han estudiado más horas han sacado, en general, mejor nota. No están exactamente en una recta, pero se acercan bastante.",
            r"The points “climb” to the right: the students who studied more hours generally got better marks. They aren't exactly on a straight line, but they're fairly close to one."))
  + note(r"Si les dades són grans (alçades de 150 a 190 cm, per exemple), els eixos no han de començar en 0: comença un poc abans de la dada més xicoteta i indica el tall de l'eix amb un zigzag.",
         r"Si los datos son grandes (alturas de 150 a 190 cm, por ejemplo), los ejes no tienen que empezar en 0: empieza un poco antes del dato más pequeño e indica el corte del eje con un zigzag.",
         r"If the data are large (heights from 150 to 190 cm, say), the axes needn't start at 0: start a little below the smallest value and show the break in the axis with a zigzag."))

s2 += box('prop', L('El centre de gravetat', 'El centro de gravedad', 'The centre of gravity'),
  P(r"El punt que té com a coordenades les dues <strong>mitjanes</strong>, \((\bar x,\,\bar y)\), s'anomena <strong>centre de gravetat</strong> del núvol. És el «punt mitjà» del núvol: els punts es reparteixen al seu voltant.",
    r"El punto que tiene como coordenadas las dos <strong>medias</strong>, \((\bar x,\,\bar y)\), se llama <strong>centro de gravedad</strong> de la nube. Es el «punto medio» de la nube: los puntos se reparten a su alrededor.",
    r"The point whose coordinates are the two <strong>means</strong>, \((\bar x,\,\bar y)\), is called the <strong>centre of gravity</strong> of the scatter plot. It's the “middle point” of the cloud: the points are spread around it.")
  + D(r"\bar x=\frac{\sum x_i}{N}\qquad \bar y=\frac{\sum y_i}{N}")
  + box('ex', L("Exemple: hores d'estudi i notes", 'Ejemplo: horas de estudio y notas', 'Example: study hours and marks'),
        D(r"\bar x=\frac{1+2+2+3+3+4+5+5+6+7}{10}=\frac{38}{10}=3\dc 8\qquad \bar y=\frac{3+3+5+4+6+6+7+8+8+9}{10}=\frac{59}{10}=5\dc 9")
        + P(r"El centre de gravetat és \(\boxed{(3\dc 8,\ 5\dc 9)}\). En el núvol l'hem marcat amb un cercle buit; les línies discontínues són \(x=\bar x\) i \(y=\bar y\).",
            r"El centro de gravedad es \(\boxed{(3\dc 8,\ 5\dc 9)}\). En la nube lo hemos marcado con un círculo vacío; las líneas discontinuas son \(x=\bar x\) e \(y=\bar y\).",
            r"The centre of gravity is \(\boxed{(3\dc 8,\ 5\dc 9)}\). We've marked it with a hollow circle; the dashed lines are \(x=\bar x\) and \(y=\bar y\).")
        + fig(NV_HM)
        + P(r"Les dues línies divideixen el núvol en quatre zones. Quasi tots els punts estan a la zona de baix a l'esquerra (poques hores i nota baixa) o a la de dalt a la dreta (moltes hores i nota alta): això indica que les variables «van juntes». Ho estudiarem a l'apartat següent.",
            r"Las dos líneas dividen la nube en cuatro zonas. Casi todos los puntos están en la zona de abajo a la izquierda (pocas horas y nota baja) o en la de arriba a la derecha (muchas horas y nota alta): eso indica que las variables «van juntas». Lo estudiaremos en el apartado siguiente.",
            r"The two lines split the cloud into four zones. Almost every point is in the bottom-left zone (few hours, low mark) or the top-right one (many hours, high mark): this shows the variables “go together”. We'll study this in the next section.")))

s2 += (widget('w-cloud', '✨', L('Dibuixa el teu núvol de punts', 'Dibuja tu nube de puntos', 'Draw your own scatter plot'),
              ['<p class="hint-s">' + L("Toca el pla per a afegir un punt; toca un punt per a esborrar-lo. L'eina calcula les mitjanes i dibuixa el centre de gravetat.",
                                        "Toca el plano para añadir un punto; toca un punto para borrarlo. La herramienta calcula las medias y dibuja el centro de gravedad.",
                                        "Tap the grid to add a point; tap a point to delete it. The tool works out the means and draws the centre of gravity.") + '</p>',
               '<div class="wrow"><button class="btn" type="button" data-a="ex">' + L("Hores i notes", "Horas y notas", "Hours and marks") + '</button><button class="btn" type="button" data-a="clear">' + L("Esborra-ho tot", "Borrarlo todo", "Clear all") + '</button></div>'],
              out='<div class="gout cl-wrap"><svg class="sgraf nv" viewBox="0 0 340 250" role="img" aria-label="núvol"></svg></div>')
       + drill('cg', 'Entrena: calcula el centre de gravetat', 'Entrena: calcula el centro de gravedad', 'Train: find the centre of gravity', 'pair'))

# problemes 10.2
A2X = [2, 4, 5, 6, 8]; A2Y = [7, 6, 4, 3, 0]; S2A = bi(A2X, A2Y); ck(S2A['mx'], 5); ck(S2A['my'], 4)
T2X = [14, 18, 20, 23, 25, 28, 30, 32]; T2Y = [20, 35, 40, 60, 65, 80, 95, 105]; S2T = bi(T2X, T2Y); ck(S2T['mx'], 23.75); ck(S2T['my'], 62.5)
B2X = [1, 2, 3, 4, 6]; B2Y = [5, 3, 2, 4, 1]
s2 += levels(
 [prob(L(r"Dibuixa el núvol de punts i calcula el centre de gravetat de la distribució:", r"Dibuja la nube de puntos y calcula el centro de gravedad de la distribución:", r"Draw the scatter plot and find the centre of gravity of the distribution:") + ptab(A2X, A2Y, M('x_i'), M('y_i')),
       D(r"\bar x=\frac{2+4+5+6+8}{5}=\frac{25}{5}=5\qquad \bar y=\frac{7+6+4+3+0}{5}=\frac{20}{5}=4"),
       P(r"Centre de gravetat: \(\boxed{(5,\ 4)}\).", r"Centro de gravedad: \(\boxed{(5,\ 4)}\).", r"Centre of gravity: \(\boxed{(5,\ 4)}\).")
       + fig(nuvol(list(zip(A2X, A2Y)), (0, 9, 1), (0, 8, 1), means=True))
       + P(r"Aquesta vegada els punts «baixen»: quan \(x\) creix, \(y\) decreix.", r"Esta vez los puntos «bajan»: cuando \(x\) crece, \(y\) decrece.", r"This time the points “go down”: as \(x\) increases, \(y\) decreases."))],
 [prob(L(r"Una gelateria ha apuntat la temperatura màxima (°C) i el nombre de gelats venuts durant 8 dies. Dibuixa el núvol de punts (fes servir escales diferents en cada eix) i calcula'n el centre de gravetat.",
         r"Una heladería ha apuntado la temperatura máxima (°C) y el número de helados vendidos durante 8 días. Dibuja la nube de puntos (usa escalas diferentes en cada eje) y calcula su centro de gravedad.",
         r"An ice-cream shop wrote down the maximum temperature (°C) and the number of ice creams sold on 8 days. Draw the scatter plot (use different scales on each axis) and find its centre of gravity.")
       + ptab(T2X, T2Y, L('Temperatura', 'Temperatura', 'Temperature'), L('Gelats', 'Helados', 'Ice creams')),
       D(r"\bar x=\frac{190}{8}=23\dc 75\ ^\circ\text{C}\qquad \bar y=\frac{500}{8}=62\dc 5\ \tri{gelats}{helados}{ice creams}"),
       fig(nuvol(list(zip(T2X, T2Y)), (10, 35, 5), (0, 120, 20), axes=('°C', L('gelats', 'helados', 'ice creams')), means=True))
       + P(r"Centre de gravetat: \(\boxed{(23\dc 75,\ 62\dc 5)}\). L'eix horitzontal comença en 10 °C perquè no hi ha cap dada més xicoteta.",
           r"Centro de gravedad: \(\boxed{(23\dc 75,\ 62\dc 5)}\). El eje horizontal empieza en 10 °C porque no hay ningún dato más pequeño.",
           r"Centre of gravity: \(\boxed{(23\dc 75,\ 62\dc 5)}\). The horizontal axis starts at 10 °C because there's no smaller value."))],
 [prob(L(r"En una distribució de 5 parelles, quatre són \((1,\,5)\), \((2,\,3)\), \((3,\,2)\) i \((4,\,4)\), i el centre de gravetat és \((3{,}2,\ 3)\). Quina és la parella que falta?",
         r"En una distribución de 5 parejas, cuatro son \((1,\,5)\), \((2,\,3)\), \((3,\,2)\) y \((4,\,4)\), y el centro de gravedad es \((3{,}2,\ 3)\). ¿Cuál es la pareja que falta?",
         r"In a distribution of 5 pairs, four of them are \((1,\,5)\), \((2,\,3)\), \((3,\,2)\) and \((4,\,4)\), and the centre of gravity is \((3.2,\ 3)\). What is the missing pair?").replace('3{,}2', r'3\dc 2'),
       P(r"La suma de les \(x\) ha de ser \(5\cdot3\dc 2=16\), i la de les \(y\), \(5\cdot3=15\).", r"La suma de las \(x\) tiene que ser \(5\cdot3\dc 2=16\), y la de las \(y\), \(5\cdot3=15\).", r"The \(x\) values must add up to \(5\cdot3\dc 2=16\), and the \(y\) values to \(5\cdot3=15\)."),
       D(r"x=16-(1+2+3+4)=6\qquad y=15-(5+3+2+4)=1\qquad\Rightarrow\qquad\boxed{(6,\ 1)}"))])
S2B = bi(B2X, B2Y); ck(S2B['mx'], '3.2'); ck(S2B['my'], 3)
P2X = [3, 5, 6, 8, 8]; P2Y = [10, 8, 9, 5, 3]; S2P = bi(P2X, P2Y); ck(S2P['mx'], 6); ck(S2P['my'], 7)
s2 += practice([('★☆☆', L(r"Calcula el centre de gravetat de les parelles \((3,10),\ (5,8),\ (6,9),\ (8,5),\ (8,3)\).", r"Calcula el centro de gravedad de las parejas \((3,10),\ (5,8),\ (6,9),\ (8,5),\ (8,3)\).", r"Find the centre of gravity of the pairs \((3,10),\ (5,8),\ (6,9),\ (8,5),\ (8,3)\).")),
                ('★★☆', L(r"Dibuixa'n el núvol de punts. Els punts pugen o baixen?", r"Dibuja su nube de puntos. ¿Los puntos suben o bajan?", r"Draw its scatter plot. Do the points go up or down?"))],
               L(r"1) \(\bar x=\frac{30}{5}=6\), \(\bar y=\frac{35}{5}=7\): \((6,\ 7)\). &nbsp; 2) Baixen: quan \(x\) creix, \(y\) tendeix a decréixer.",
                 r"1) \(\bar x=\frac{30}{5}=6\), \(\bar y=\frac{35}{5}=7\): \((6,\ 7)\). &nbsp; 2) Bajan: cuando \(x\) crece, \(y\) tiende a decrecer.",
                 r"1) \(\bar x=\frac{30}{5}=6\), \(\bar y=\frac{35}{5}=7\): \((6,\ 7)\). &nbsp; 2) They go down: as \(x\) increases, \(y\) tends to decrease.") + fig(nuvol(list(zip(P2X, P2Y)), (0, 10, 1), (0, 12, 2), means=True)))
