# Apartats 10.1-10.2 dels apunts de la Unitat 10 de 2n ESO (Funcions): concepte de funció i funcions donades per taules
# de valors. Cada resultat es comprova amb ck() i lin() (fraccions exactes).
import math
from comu import *

# =====================================================================
# 10.1 Concepte de funció
# =====================================================================
KGT = [0, 1, 2, 3, 4]
F_TAR = pla((0, 4.6, 0, 9.6), fns=[(2, 0, 'c0', 0, 4.4)], pts=[(k, 2 * k, None, 'p0') for k in KGT], W=220, H=210, ys=2, xl='kg', yl='€')
[ck(lin(2)(k), v) for k, v in zip(KGT, [0, 2, 4, 6, 8])]
# una funció (cada x té una sola y) i una relació que no ho és (una circumferència)
FN_OK = [(-4, -1), (-2, 2), (0, 1), (2, 3), (4, -2)]
CIRC = [(1.5 * math.cos(math.radians(a)) * 2, 1.5 * math.sin(math.radians(a)) * 2) for a in range(0, 361, 10)]
F_SI = pla((-5, 5, -4, 4), curves=[(FN_OK, 'c0')], W=200, H=160)
F_NO = pla((-5, 5, -4, 4), curves=[(CIRC, 'c1')], proj=[], W=200, H=160, labs=[])
F_NOv = pla((-5, 5, -4, 4), curves=[(CIRC, 'c1')], pts=[(1, 2 * math.sqrt(2), None, 'bad'), (1, -2 * math.sqrt(2), None, 'bad')], W=200, H=160)
F_NOv = F_NOv.replace('</svg>', '<line class="cursor" x1="120.0" y1="0" x2="120.0" y2="160"/></svg>')

s1 = box('def', L('Què és una funció?', '¿Qué es una función?', 'What is a function?'),
  P(r"Moltes vegades dues <strong>magnituds</strong> estan relacionades: quan canvia una, canvia l'altra. El <strong>pes</strong> de taronges que comprem i el <strong>preu</strong> que paguem; el <strong>temps</strong> que fa que ha eixit un tren i la <strong>distància</strong> que ha recorregut; el <strong>costat</strong> d'un quadrat i la seua <strong>àrea</strong>…",
    r"Muchas veces dos <strong>magnitudes</strong> están relacionadas: cuando cambia una, cambia la otra. El <strong>peso</strong> de naranjas que compramos y el <strong>precio</strong> que pagamos; el <strong>tiempo</strong> que hace que ha salido un tren y la <strong>distancia</strong> que ha recorrido; el <strong>lado</strong> de un cuadrado y su <strong>área</strong>…",
    r"Two <strong>quantities</strong> are often related: when one changes, so does the other. The <strong>weight</strong> of oranges we buy and the <strong>price</strong> we pay; the <strong>time</strong> since a train left and the <strong>distance</strong> it has covered; the <strong>side</strong> of a square and its <strong>area</strong>…")
  + ul(L(r"La <strong>variable independent</strong> \(x\) és la que triem o la que passa sola (els kg, el temps, el costat). Va en l'<strong>eix horitzontal</strong>.",
         r"La <strong>variable independiente</strong> \(x\) es la que elegimos o la que pasa sola (los kg, el tiempo, el lado). Va en el <strong>eje horizontal</strong>.",
         r"The <strong>independent variable</strong> \(x\) is the one we choose or that just goes on (kg, time, the side). It goes on the <strong>horizontal axis</strong>."),
       L(r"La <strong>variable dependent</strong> \(y\) és la que <strong>depén</strong> de l'altra (el preu, la distància, l'àrea). Va en l'<strong>eix vertical</strong>.",
         r"La <strong>variable dependiente</strong> \(y\) es la que <strong>depende</strong> de la otra (el precio, la distancia, el área). Va en el <strong>eje vertical</strong>.",
         r"The <strong>dependent variable</strong> \(y\) is the one that <strong>depends</strong> on the other (the price, the distance, the area). It goes on the <strong>vertical axis</strong>."))
  + '<div class="defn">' + P(r"Una <strong>funció</strong> és una relació entre dues variables en què a <strong>cada valor</strong> de la variable independent \(x\) li correspon <strong>un únic valor</strong> de la variable dependent \(y\). Diem que \(y\) és <strong>funció</strong> de \(x\).",
    r"Una <strong>función</strong> es una relación entre dos variables en la que a <strong>cada valor</strong> de la variable independiente \(x\) le corresponde <strong>un único valor</strong> de la variable dependiente \(y\). Decimos que \(y\) es <strong>función</strong> de \(x\).",
    r"A <strong>function</strong> is a relation between two variables in which <strong>each value</strong> of the independent variable \(x\) gives <strong>exactly one value</strong> of the dependent variable \(y\). We say \(y\) is a <strong>function</strong> of \(x\).") + '</div>'
  + tbl([L('Relació', 'Relación', 'Relation'), L('És funció?', '¿Es función?', 'Function?')],
        [[L('pes de taronges → preu', 'peso de naranjas → precio', 'weight of oranges → price'), L('<strong>Sí</strong>: cada pes té un preu', '<strong>Sí</strong>: cada peso tiene un precio', '<strong>Yes</strong>: each weight has one price')],
         [L('costat d\'un quadrat → àrea', 'lado de un cuadrado → área', 'side of a square → area'), L('<strong>Sí</strong>: \\(A=l^2\\)', '<strong>Sí</strong>: \\(A=l^2\\)', '<strong>Yes</strong>: \\(A=l^2\\)')],
         [L('hora del dia → temperatura', 'hora del día → temperatura', 'time of day → temperature'), L('<strong>Sí</strong>: en cada moment hi ha una temperatura', '<strong>Sí</strong>: en cada momento hay una temperatura', '<strong>Yes</strong>: at each moment there is one temperature')],
         [L('nombre → els seus divisors', 'número → sus divisores', 'number → its divisors'), L('<strong>No</strong>: el 6 té quatre divisors (1, 2, 3 i 6)', '<strong>No</strong>: el 6 tiene cuatro divisores (1, 2, 3 y 6)', '<strong>No</strong>: 6 has four divisors (1, 2, 3 and 6)')]]))

s1 += box('prop', L('Maneres de donar una funció', 'Formas de dar una función', 'Ways of giving a function'),
  P(r"Una mateixa funció es pot donar de quatre maneres. Exemple: <em>un quilo de taronges val 2 €</em>.",
    r"Una misma función se puede dar de cuatro formas. Ejemplo: <em>un kilo de naranjas vale 2 €</em>.",
    r"The same function can be given in four ways. Example: <em>a kilo of oranges costs €2</em>.")
  + '<div class="gout"><div class="gcol">'
  + ol(L(r"Amb un <strong>enunciat</strong> (paraules): «el preu és el doble dels quilos».", r"Con un <strong>enunciado</strong> (palabras): «el precio es el doble de los kilos».", r"In <strong>words</strong>: “the price is twice the number of kilos”."),
       L(r"Amb una <strong>taula de valors</strong> (la de davall).", r"Con una <strong>tabla de valores</strong> (la de debajo).", r"With a <strong>table of values</strong> (the one below)."),
       L(r"Amb un <strong>gràfic</strong> (el del costat).", r"Con una <strong>gráfica</strong> (la de al lado).", r"With a <strong>graph</strong> (the one alongside)."),
       L(r"Amb una <strong>equació</strong> o fórmula: \(y=2x\).", r"Con una <strong>ecuación</strong> o fórmula: \(y=2x\).", r"With an <strong>equation</strong> or formula: \(y=2x\)."))
  + '</div>' + F_TAR + '</div>'
  + tv(KGT, [0, 2, 4, 6, 8], L('pes (kg)', 'peso (kg)', 'weight (kg)'), L('preu (€)', 'precio (€)', 'price (€)'))
  + note(r"La fórmula és la manera més completa: amb ella podem calcular el preu de qualsevol pes. Per a 3,5 kg: \(y=2\cdot3{,}5=7\) €.",
         r"La fórmula es la forma más completa: con ella podemos calcular el precio de cualquier peso. Para 3,5 kg: \(y=2\cdot3{,}5=7\) €.",
         r"The formula is the most complete way: with it we can work out the price of any weight. For 3.5 kg: \(y=2\cdot3.5=7\) €."))
ck(2 * fr('3.5'), 7)

s1 += box('prop', L('Com sabem si un gràfic és d\'una funció?', '¿Cómo sabemos si una gráfica es de una función?', 'How can we tell whether a graph is a function?'),
  P(r"<strong>Prova de la recta vertical</strong>: imaginem rectes verticals que recorren el gràfic. Si alguna el talla en <strong>dos punts o més</strong>, hi ha un valor de \(x\) amb dos valors de \(y\) i <strong>no és una funció</strong>.",
    r"<strong>Prueba de la recta vertical</strong>: imaginamos rectas verticales que recorren la gráfica. Si alguna la corta en <strong>dos puntos o más</strong>, hay un valor de \(x\) con dos valores de \(y\) y <strong>no es una función</strong>.",
    r"<strong>Vertical line test</strong>: imagine vertical lines sweeping across the graph. If any of them meets it at <strong>two or more points</strong>, one value of \(x\) has two values of \(y\) and it is <strong>not a function</strong>.")
  + figs(fig(F_SI, L('És una funció', 'Es una función', 'It is a function')), fig(F_NOv, L('No és una funció: per a \\(x=1\\) hi ha dos valors de \\(y\\)', 'No es una función: para \\(x=1\\) hay dos valores de \\(y\\)', 'Not a function: \\(x=1\\) has two values of \\(y\\)')))
  + widget('w-vline', '📏', L('La prova de la recta vertical', 'La prueba de la recta vertical', 'The vertical line test'),
           [seg([('0', L('Muntanya', 'Montaña', 'Mountain')), ('1', L('Cercle', 'Círculo', 'Circle')), ('2', L('Recta', 'Recta', 'Line')), ('3', L('Lletra S', 'Letra S', 'Letter S'))]),
            '<div class="wrow">' + rng('x', -4.5, 4.5, 0.1, -2, 'x') + '</div>'], out='<div class="gout"></div>')
  + drill('isfn', 'Entrena: és una funció?', 'Entrena: ¿es una función?', 'Train: is it a function?', 'opts'))

F_GA = pla((-4, 4, -3, 3), curves=[([(-3.5, -2), (-1, 2), (1, 0), (3.5, 2.5)], 'c0')], W=150, H=120)
F_GB = pla((-4, 4, -3, 3), curves=[([(-1, -2.5), (2, -1), (-1, 0.5), (2, 2.5)], 'c0')], W=150, H=120)
F_GC = pla((-4, 4, -3, 3), fns=[(0, 2, 'c0')], W=150, H=120)
TQ = ([1, 2, 2, 3], [5, 6, 8, 9])
s1 += levels(
 [prob(L(r"En cada situació, digues quina és la variable independent i quina la dependent: a) els litres de gasolina que posem i el preu que paguem; b) l'altura d'un ciri i el temps que fa que crema; c) el nombre d'amics que van al cine i el que costen les entrades.",
         r"En cada situación, di cuál es la variable independiente y cuál la dependiente: a) los litros de gasolina que echamos y el precio que pagamos; b) la altura de una vela y el tiempo que lleva encendida; c) el número de amigos que van al cine y lo que cuestan las entradas.",
         r"In each situation, say which is the independent variable and which is the dependent one: a) the litres of petrol we buy and the price we pay; b) the height of a candle and how long it has been burning; c) the number of friends who go to the cinema and the cost of the tickets."),
       P(r"Ens preguntem: <em>quina depén de l'altra?</em> La que depén és la \(y\).", r"Nos preguntamos: <em>¿cuál depende de la otra?</em> La que depende es la \(y\).", r"Ask: <em>which one depends on the other?</em> The one that depends is \(y\)."),
       ul(L(r"a) \(x\): litres; \(y\): preu (el preu depén dels litres).", r"a) \(x\): litros; \(y\): precio (el precio depende de los litros).", r"a) \(x\): litres; \(y\): price (the price depends on the litres)."),
          L(r"b) \(x\): temps; \(y\): altura del ciri (com més temps, més curt).", r"b) \(x\): tiempo; \(y\): altura de la vela (cuanto más tiempo, más corta).", r"b) \(x\): time; \(y\): height of the candle (the longer, the shorter)."),
          L(r"c) \(x\): nombre d'amics; \(y\): preu total de les entrades.", r"c) \(x\): número de amigos; \(y\): precio total de las entradas.", r"c) \(x\): number of friends; \(y\): total price of the tickets."))),
  prob(L(r"Aquesta taula relaciona dues variables. És una funció?", r"Esta tabla relaciona dos variables. ¿Es una función?", r"This table relates two variables. Is it a function?") + tv(*TQ),
       P(r"Mirem si algun valor de \(x\) es repeteix amb valors de \(y\) diferents: per a \(x=2\) tenim \(y=6\) i també \(y=8\).", r"Miramos si algún valor de \(x\) se repite con valores de \(y\) distintos: para \(x=2\) tenemos \(y=6\) y también \(y=8\).", r"Check whether any value of \(x\) appears with different values of \(y\): for \(x=2\) we have \(y=6\) and also \(y=8\)."),
       P(r"<strong>No és una funció</strong>: al 2 li corresponen dos valors.", r"<strong>No es una función</strong>: al 2 le corresponden dos valores.", r"<strong>It is not a function</strong>: 2 is paired with two values."))],
 [prob(L(r"Quins d'aquests gràfics són d'una funció?", r"¿Cuáles de estas gráficas son de una función?", r"Which of these graphs are functions?")
       + figs(fig(F_GA, 'A'), fig(F_GB, 'B'), fig(F_GC, 'C'), three=True),
       P(r"Fem la prova de la recta vertical en cada gràfic:", r"Hacemos la prueba de la recta vertical en cada gráfica:", r"Do the vertical line test on each graph:"),
       ul(L(r"A: cap recta vertical el talla dues vegades: <strong>sí</strong>.", r"A: ninguna recta vertical la corta dos veces: <strong>sí</strong>.", r"A: no vertical line meets it twice: <strong>yes</strong>."),
          L(r"B: el gràfic va cap avant i cap arrere; la recta \(x=0\) el talla tres vegades: <strong>no</strong>.", r"B: la gráfica va hacia delante y hacia atrás; la recta \(x=0\) la corta tres veces: <strong>no</strong>.", r"B: the graph goes forwards and backwards; the line \(x=0\) meets it three times: <strong>no</strong>."),
          L(r"C: una recta horitzontal; cada vertical la talla una vegada: <strong>sí</strong> (és una funció constant, apartat 10.7).", r"C: una recta horizontal; cada vertical la corta una vez: <strong>sí</strong> (es una función constante, apartado 10.7).", r"C: a horizontal line; each vertical line meets it once: <strong>yes</strong> (a constant function, section 10.7)."))),
  prob(L(r"Raona si aquestes relacions són funcions: a) a cada alumne de la classe li fem correspondre la seua altura; b) a cada altura (en cm) li fem correspondre els alumnes que la tenen.",
         r"Razona si estas relaciones son funciones: a) a cada alumno de la clase le hacemos corresponder su altura; b) a cada altura (en cm) le hacemos corresponder los alumnos que la tienen.",
         r"Decide whether these relations are functions: a) each student in the class is paired with their height; b) each height (in cm) is paired with the students who have it."),
       P(r"a) Cada alumne té <strong>una sola</strong> altura: <strong>és una funció</strong>.", r"a) Cada alumno tiene <strong>una sola</strong> altura: <strong>es una función</strong>.", r"a) Each student has <strong>just one</strong> height: <strong>it is a function</strong>."),
       P(r"b) Pot haver-hi dos alumnes que facen, per exemple, 158 cm: una altura amb dos valors. <strong>No és una funció</strong>.", r"b) Puede haber dos alumnos que midan, por ejemplo, 158 cm: una altura con dos valores. <strong>No es una función</strong>.", r"b) Two students might both be, say, 158 cm tall: one height with two values. <strong>It is not a function</strong>."))],
 [prob(L(r"Una pintora cobra 15 € per cada hora de treball. Dona aquesta funció de les quatre maneres: amb paraules, amb una taula, amb una fórmula i amb un gràfic.",
         r"Una pintora cobra 15 € por cada hora de trabajo. Da esta función de las cuatro formas: con palabras, con una tabla, con una fórmula y con una gráfica.",
         r"A painter charges €15 for each hour of work. Give this function in the four ways: in words, with a table, with a formula and with a graph."),
       P(r"<strong>Paraules</strong>: «el que cobra és 15 vegades les hores». \(x\) = hores, \(y\) = euros.", r"<strong>Palabras</strong>: «lo que cobra es 15 veces las horas». \(x\) = horas, \(y\) = euros.", r"<strong>Words</strong>: “what she earns is 15 times the hours”. \(x\) = hours, \(y\) = euros."),
       tv([0, 1, 2, 3, 4], [ck(15 * k, v) for k, v in zip(range(5), [0, 15, 30, 45, 60])], 'h', '€') + D(r"y=15x"),
       figs(fig(pla((0, 4.6, 0, 69), fns=[(15, 0, 'c0', 0, 4.4)], pts=[(k, 15 * k, None, 'p0') for k in range(5)], W=220, H=200, ys=15, gy=15, xl='h', yl='€')))
       + P(r"Unim els punts perquè també té sentit treballar mitja hora (7,50 €).", r"Unimos los puntos porque también tiene sentido trabajar media hora (7,50 €).", r"We join the points because half an hour of work also makes sense (€7.50)."))])
ck(15 * fr('0.5'), '7.5')
s1 += practice([('★☆☆', L(r"És funció la relació que a cada persona li assigna la seua data de naixement? I la que a cada data li assigna les persones nascudes eixe dia?", r"¿Es función la relación que a cada persona le asigna su fecha de nacimiento? ¿Y la que a cada fecha le asigna las personas nacidas ese día?", r"Is the relation that pairs each person with their date of birth a function? And the one that pairs each date with the people born that day?")),
                ('★★☆', L(r"El perímetre d'un quadrat és 4 vegades el costat. Escriu la fórmula i calcula el perímetre si el costat fa 2,5 cm.", r"El perímetro de un cuadrado es 4 veces el lado. Escribe la fórmula y calcula el perímetro si el lado mide 2,5 cm.", r"A square's perimeter is 4 times its side. Write the formula and work out the perimeter if the side is 2.5 cm."))],
               L(r"1) La primera sí (cada persona té una data); la segona no (molta gent naix el mateix dia). &nbsp; 2) \(P=4l\); \(P=4\cdot2{,}5=10\) cm.", r"1) La primera sí (cada persona tiene una fecha); la segunda no (mucha gente nace el mismo día). &nbsp; 2) \(P=4l\); \(P=4\cdot2{,}5=10\) cm.", r"1) The first one is (each person has one date); the second isn't (many people are born on the same day). &nbsp; 2) \(P=4l\); \(P=4\cdot2.5=10\) cm."))
ck(4 * fr('2.5'), 10)

# =====================================================================
# 10.2 Funcions donades per taules de valors
# =====================================================================
ENT = [1, 2, 3, 4, 5]
F_ENT = pla((0, 5.6, 0, 42), pts=[(k, 8 * k, None, 'p0') for k in ENT], W=220, H=200, xl=Ls('entrades', 'entradas', 'tickets'), yl='€', ys=8, gy=8)
HORES = [0, 4, 8, 12, 16, 20, 24]
TEMP = [6, 4, 9, 17, 19, 12, 7]
F_TEMP = pla((0, 25, 0, 21), curves=[(list(zip(HORES, TEMP)), 'c0')], pts=[(h, t, None, 'p0') for h, t in zip(HORES, TEMP)], W=260, H=200, xs=4, gx=2, ys=4, gy=2, xl='h', yl='°C')
F_TEMPq = pla((0, 25, 0, 21), curves=[(list(zip(HORES, TEMP)), 'c0')], pts=[(14, 18, None, 'p1')], proj=[(14, 18)], W=260, H=200, xs=4, gx=2, ys=4, gy=2, xl='h', yl='°C')
assert (17 + 19) / 2 == 18  # entre les 12 h (17 °C) i les 16 h (19 °C): a les 14 h, uns 18 °C
TX = [0, 1, 2, 3, 4]
TY = [ck(lin(2, 3)(k), v) for k, v in zip(TX, [3, 5, 7, 9, 11])]

s2 = box('def', L('De la taula al gràfic', 'De la tabla a la gráfica', 'From the table to the graph'),
  P(r"En una <strong>taula de valors</strong> escrivim alguns valors de \(x\) i els valors de \(y\) que els corresponen. Cada columna de la taula és un <strong>punt</strong> \((x,\ y)\) del gràfic. Per a fer el gràfic:",
    r"En una <strong>tabla de valores</strong> escribimos algunos valores de \(x\) y los valores de \(y\) que les corresponden. Cada columna de la tabla es un <strong>punto</strong> \((x,\ y)\) de la gráfica. Para hacer la gráfica:",
    r"In a <strong>table of values</strong> we write some values of \(x\) and the values of \(y\) that go with them. Each column of the table is a <strong>point</strong> \((x,\ y)\) of the graph. To draw the graph:")
  + ol(L(r"Dibuixem els eixos i hi escrivim el <strong>nom de cada variable</strong> i la seua <strong>unitat</strong> (h, °C, kg, €…).", r"Dibujamos los ejes y escribimos el <strong>nombre de cada variable</strong> y su <strong>unidad</strong> (h, °C, kg, €…).", r"Draw the axes and label them with the <strong>name of each variable</strong> and its <strong>unit</strong> (h, °C, kg, €…)."),
       L(r"Triem una <strong>escala</strong> per a cada eix (cada quadre pot valdre 1, 2, 5, 10…). Els dos eixos poden tindre escales diferents, però en cada eix les divisions han de ser <strong>iguals</strong>.",
         r"Elegimos una <strong>escala</strong> para cada eje (cada cuadro puede valer 1, 2, 5, 10…). Los dos ejes pueden tener escalas distintas, pero en cada eje las divisiones tienen que ser <strong>iguales</strong>.",
         r"Choose a <strong>scale</strong> for each axis (each square can stand for 1, 2, 5, 10…). The two axes can have different scales, but on each axis the divisions must be <strong>equal</strong>."),
       L(r"Dibuixem els <strong>punts</strong> de la taula.", r"Dibujamos los <strong>puntos</strong> de la tabla.", r"Plot the <strong>points</strong> from the table."),
       L(r"Decidim si <strong>unim els punts</strong>: els unim si també tenen sentit els valors intermedis (les 10 h, 1,5 kg); no els unim si només hi ha valors solts (nombre d'entrades, de persones…).",
         r"Decidimos si <strong>unimos los puntos</strong>: los unimos si también tienen sentido los valores intermedios (las 10 h, 1,5 kg); no los unimos si solo hay valores sueltos (número de entradas, de personas…).",
         r"Decide whether to <strong>join the points</strong>: join them if in-between values make sense too (10 o'clock, 1.5 kg); don't join them if only separate values are possible (number of tickets, of people…)."))
  + tv(HORES, TEMP, 'h', '°C') + P(r"Temperatura d'un dia de primavera, cada 4 hores. Té sentit la temperatura a qualsevol hora: <strong>unim els punts</strong>.", r"Temperatura de un día de primavera, cada 4 horas. Tiene sentido la temperatura a cualquier hora: <strong>unimos los puntos</strong>.", r"Temperature on a spring day, every 4 hours. The temperature makes sense at any time: <strong>we join the points</strong>.")
  + tv(ENT, [8 * k for k in ENT], L('entrades', 'entradas', 'tickets'), '€') + P(r"Entrades de cine a 8 €. No es pot comprar mitja entrada: <strong>punts solts</strong>.", r"Entradas de cine a 8 €. No se puede comprar media entrada: <strong>puntos sueltos</strong>.", r"Cinema tickets at €8. You can't buy half a ticket: <strong>separate points</strong>.")
  + figs(fig(F_TEMP), fig(F_ENT))
  + widget('w-table', '📋', L('De la taula al gràfic', 'De la tabla a la gráfica', 'From the table to the graph'),
           [seg([('tmp', L('Temperatura', 'Temperatura', 'Temperature')), ('ent', L('Entrades', 'Entradas', 'Tickets')), ('pis', L('Piscina', 'Piscina', 'Pool')), ('own', L('La meua taula', 'Mi tabla', 'My table'))]),
            '<div class="wrow">' + tin('x', 'x', '0 4 8 12 16 20 24', 'w') + '</div>', '<div class="wrow">' + tin('y', 'y', '6 4 9 17 19 12 7', 'w') + '</div>',
            seg([('1', L('Uneix els punts', 'Unir los puntos', 'Join the points')), ('0', L('Punts solts', 'Puntos sueltos', 'Separate points'))])],
           out='<div class="gout"></div>'))

s2 += box('prop', L('Llegir valors que no són a la taula', 'Leer valores que no están en la tabla', 'Reading values that aren\'t in the table'),
  P(r"Quan els punts estan units, el gràfic ens dona també els valors <strong>intermedis</strong>. Quina temperatura feia a les 14 h? Busquem 14 en l'eix horitzontal, pugem fins al gràfic i anem a l'eix vertical: unes <strong>18 °C</strong>.",
    r"Cuando los puntos están unidos, la gráfica nos da también los valores <strong>intermedios</strong>. ¿Qué temperatura hacía a las 14 h? Buscamos 14 en el eje horizontal, subimos hasta la gráfica y vamos al eje vertical: unos <strong>18 °C</strong>.",
    r"When the points are joined, the graph also gives us the values <strong>in between</strong>. What was the temperature at 2 pm (14 h)? Find 14 on the horizontal axis, go up to the graph and across to the vertical axis: about <strong>18 °C</strong>.")
  + figs(fig(F_TEMPq))
  + note(r"És un valor <strong>aproximat</strong>: només sabem segur les temperatures de la taula. Entre dues mesures, suposem que la temperatura canvia de manera regular.",
         r"Es un valor <strong>aproximado</strong>: solo sabemos seguro las temperaturas de la tabla. Entre dos medidas, suponemos que la temperatura cambia de forma regular.",
         r"It is an <strong>approximate</strong> value: we only know the temperatures in the table for sure. Between two readings, we assume the temperature changes steadily."))

s2 += box('prop', L('De la taula a la fórmula', 'De la tabla a la fórmula', 'From the table to the formula'),
  P(r"Si en una taula la \(x\) va d'1 en 1 i la \(y\) augmenta (o disminueix) <strong>sempre la mateixa quantitat</strong>, la fórmula és de la forma \(y=m\,x+n\): \(m\) és el que augmenta \(y\) cada vegada i \(n\) és el valor de \(y\) per a \(x=0\).",
    r"Si en una tabla la \(x\) va de 1 en 1 y la \(y\) aumenta (o disminuye) <strong>siempre la misma cantidad</strong>, la fórmula es de la forma \(y=m\,x+n\): \(m\) es lo que aumenta \(y\) cada vez y \(n\) es el valor de \(y\) para \(x=0\).",
    r"If in a table \(x\) goes up 1 at a time and \(y\) goes up (or down) by <strong>the same amount every time</strong>, the formula has the form \(y=m\,x+n\): \(m\) is how much \(y\) goes up each time and \(n\) is the value of \(y\) when \(x=0\).")
  + '<div class="gout"><div class="gcol">' + tv(TX, TY)
  + P(r"Cada vegada que \(x\) augmenta 1, \(y\) augmenta 2 \(\Rightarrow m=2\). Per a \(x=0\), \(y=3\) \(\Rightarrow n=3\).", r"Cada vez que \(x\) aumenta 1, \(y\) aumenta 2 \(\Rightarrow m=2\). Para \(x=0\), \(y=3\) \(\Rightarrow n=3\).", r"Each time \(x\) goes up by 1, \(y\) goes up by 2 \(\Rightarrow m=2\). When \(x=0\), \(y=3\) \(\Rightarrow n=3\).")
  + D(r"y=2x+3") + P(r"Comprovem-ho amb una altra columna: \(x=4\): \(2\cdot4+3=11\) ✓.", r"Lo comprobamos con otra columna: \(x=4\): \(2\cdot4+3=11\) ✓.", r"Check with another column: \(x=4\): \(2\cdot4+3=11\) ✓.") + '</div>'
  + pla((-0.5, 4.6, 0, 12.6), fns=[(2, 3, 'c0')], pts=[(a, b, None, 'p0') for a, b in zip(TX, TY)], curves=[([(1, 5), (2, 5), (2, 7)], 'c1 stp')], W=200, H=230, ys=2)
  + '</div>'
  + P(r"Si la \(y\) no augmenta sempre igual, la fórmula no és d'aquest tipus. Per exemple, l'àrea d'un quadrat (\(l\): 1, 2, 3, 4 → \(A\): 1, 4, 9, 16) augmenta 3, 5, 7…: la fórmula és \(A=l^2\) i el gràfic no és una recta.",
      r"Si la \(y\) no aumenta siempre igual, la fórmula no es de este tipo. Por ejemplo, el área de un cuadrado (\(l\): 1, 2, 3, 4 → \(A\): 1, 4, 9, 16) aumenta 3, 5, 7…: la fórmula es \(A=l^2\) y la gráfica no es una recta.",
      r"If \(y\) doesn't always go up by the same amount, the formula is not of this type. For example, the area of a square (\(l\): 1, 2, 3, 4 → \(A\): 1, 4, 9, 16) goes up by 3, 5, 7…: the formula is \(A=l^2\) and the graph isn't a straight line.")
  + drill('formula', 'Entrena: quina fórmula té la taula?', 'Entrena: ¿qué fórmula tiene la tabla?', 'Train: which formula fits the table?', 'opts')
  + drill('gap', 'Entrena: completa la taula', 'Entrena: completa la tabla', 'Train: complete the table'))

PIS = ([0, 1, 2, 3, 4, 5], [ck(lin(-15, 80)(k), v) for k, v in zip(range(6), [80, 65, 50, 35, 20, 5])])
F_PIS = pla((0, 6.4, 0, 92), curves=[(list(zip(*PIS)), 'c0')], pts=[(a, b, None, 'p0') for a, b in zip(*PIS)], W=220, H=200, ys=20, gy=10, xl='h', yl=Ls('altura (cm)', 'altura (cm)', 'height (cm)'))
DIA = ([3, 4, 5, 6, 7, 8], [ck(Fr(n * (n - 3), 2), v) for n, v in zip(range(3, 9), [0, 2, 5, 9, 14, 20])])
F_DIA = pla((0, 8.8, 0, 23), pts=[(a, b, None, 'p0') for a, b in zip(*DIA)], W=220, H=200, ys=4, gy=2, xl='n', yl='d')
PE = [ck(fr('1.8') * k, v) for k, v in zip([0.5, 1, 2, 3, 5], ['0.9', '1.8', '3.6', '5.4', '9'])]
PEs = ['0{,}9', '1{,}8', '3{,}6', '5{,}4', '9']
TB = ([1, 2, 3, 4], [ck(lin(3, 4)(k), v) for k, v in zip(range(1, 5), [7, 10, 13, 16])])
s2 += levels(
 [prob(L(r"Un quilo de peres val 1,80 €. Completa la taula del preu (\(y\)) segons el pes (\(x\)) i digues si unim els punts del gràfic.", r"Un kilo de peras vale 1,80 €. Completa la tabla del precio (\(y\)) según el peso (\(x\)) y di si unimos los puntos de la gráfica.", r"A kilo of pears costs €1.80. Complete the table of the price (\(y\)) against the weight (\(x\)) and say whether we join the points of the graph.")
       + tv(['0{,}5', 1, 2, 3, 5], ['', '', '', '', ''], L('pes (kg)', 'peso (kg)', 'weight (kg)'), L('preu (€)', 'precio (€)', 'price (€)')),
       P(r"Multipliquem cada pes per 1,80: \(0{,}5\cdot1{,}8=0{,}9\); \(2\cdot1{,}8=3{,}6\)…", r"Multiplicamos cada peso por 1,80: \(0{,}5\cdot1{,}8=0{,}9\); \(2\cdot1{,}8=3{,}6\)…", r"Multiply each weight by 1.80: \(0.5\cdot1.8=0.9\); \(2\cdot1.8=3.6\)…"),
       tv(['0{,}5', 1, 2, 3, 5], PEs, L('pes (kg)', 'peso (kg)', 'weight (kg)'), L('preu (€)', 'precio (€)', 'price (€)'))
       + P(r"Té sentit comprar qualsevol pes (1,3 kg, 2,75 kg…): <strong>unim els punts</strong>.", r"Tiene sentido comprar cualquier peso (1,3 kg, 2,75 kg…): <strong>unimos los puntos</strong>.", r"It makes sense to buy any weight (1.3 kg, 2.75 kg…): <strong>we join the points</strong>.")),
  prob(L(r"Una piscina inflable es buida. La taula dona l'altura de l'aigua cada hora. Representa-la i digues quanta aigua quedava a les 2 h 30 min.", r"Una piscina hinchable se vacía. La tabla da la altura del agua cada hora. Represéntala y di cuánta agua quedaba a las 2 h 30 min.", r"An inflatable pool is emptying. The table gives the height of the water every hour. Plot it and say how much water was left at 2 h 30 min.")
       + tv(*PIS, L('temps (h)', 'tiempo (h)', 'time (h)'), L('altura (cm)', 'altura (cm)', 'height (cm)')),
       figs(fig(F_PIS)),
       P(r"Cada hora baixa 15 cm. A les 2 h 30 min estem a mig camí entre 50 i 35: \(50-7{,}5=\boxed{42{,}5\ \text{cm}}\).", r"Cada hora baja 15 cm. A las 2 h 30 min estamos a medio camino entre 50 y 35: \(50-7{,}5=\boxed{42{,}5\ \text{cm}}\).", r"It drops 15 cm every hour. At 2 h 30 min we're halfway between 50 and 35: \(50-7.5=\boxed{42.5\ \text{cm}}\)."))],
 [prob(L(r"Troba la fórmula de la funció que dona aquesta taula i calcula el valor de \(y\) per a \(x=10\).", r"Halla la fórmula de la función que da esta tabla y calcula el valor de \(y\) para \(x=10\).", r"Find the formula of the function given by this table and work out \(y\) when \(x=10\).") + tv(*TB),
       P(r"La \(x\) va d'1 en 1 i la \(y\) augmenta sempre 3: \(m=3\). Per a saber \(n\), tornem enrere una columna: per a \(x=0\), \(y=7-3=4\).", r"La \(x\) va de 1 en 1 y la \(y\) aumenta siempre 3: \(m=3\). Para saber \(n\), volvemos atrás una columna: para \(x=0\), \(y=7-3=4\).", r"\(x\) goes up 1 at a time and \(y\) always goes up by 3: \(m=3\). To find \(n\), go back one column: for \(x=0\), \(y=7-3=4\)."),
       D(r"y=3x+4\qquad x=10:\ y=3\cdot10+4=\boxed{34}")),
  prob(L(r"La taula dona la temperatura d'un dia. a) A quina hora va fer més calor? b) Entre quines hores va pujar la temperatura? c) Quina temperatura aproximada feia a les 10 h?", r"La tabla da la temperatura de un día. a) ¿A qué hora hizo más calor? b) ¿Entre qué horas subió la temperatura? c) ¿Qué temperatura aproximada hacía a las 10 h?", r"The table gives a day's temperature. a) At what time was it hottest? b) Between which times did the temperature rise? c) Roughly what was the temperature at 10 am?") + tv(HORES, TEMP, 'h', '°C'),
       P(r"a) El valor més gran de la taula és 19 °C, a les <strong>16 h</strong>.", r"a) El valor más grande de la tabla es 19 °C, a las <strong>16 h</strong>.", r"a) The biggest value in the table is 19 °C, at <strong>16 h</strong> (4 pm)."),
       P(r"b) Va pujar <strong>de les 4 h a les 16 h</strong> (de 4 °C a 19 °C).", r"b) Subió <strong>de las 4 h a las 16 h</strong> (de 4 °C a 19 °C).", r"b) It rose <strong>from 4 h to 16 h</strong> (from 4 °C to 19 °C)."),
       P(r"c) Les 10 h estan a mig camí entre les 8 h (9 °C) i les 12 h (17 °C): unes \(\boxed{13\ °\text{C}}\).", r"c) Las 10 h están a medio camino entre las 8 h (9 °C) y las 12 h (17 °C): unos \(\boxed{13\ °\text{C}}\).", r"c) 10 h is halfway between 8 h (9 °C) and 12 h (17 °C): about \(\boxed{13\ °\text{C}}\)."))],
 [prob(L(r"Un polígon de \(n\) costats té \(d\) diagonals. Representa la taula. Unim els punts? És una recta? Quantes diagonals tindrà un polígon de 9 costats?", r"Un polígono de \(n\) lados tiene \(d\) diagonales. Representa la tabla. ¿Unimos los puntos? ¿Es una recta? ¿Cuántas diagonales tendrá un polígono de 9 lados?", r"A polygon with \(n\) sides has \(d\) diagonals. Plot the table. Do we join the points? Is it a straight line? How many diagonals does a 9-sided polygon have?") + tv(*DIA, 'n', 'd'),
       figs(fig(F_DIA)) + P(r"No hi ha polígons de 4,5 costats: <strong>punts solts</strong>.", r"No hay polígonos de 4,5 lados: <strong>puntos sueltos</strong>.", r"There are no polygons with 4.5 sides: <strong>separate points</strong>."),
       P(r"La \(d\) augmenta 2, 3, 4, 5, 6…: no augmenta sempre igual, així que <strong>no és una recta</strong>. Seguint la regularitat, de 8 a 9 costats augmentarà 7: \(20+7=\boxed{27}\) diagonals.", r"La \(d\) aumenta 2, 3, 4, 5, 6…: no aumenta siempre igual, así que <strong>no es una recta</strong>. Siguiendo la regularidad, de 8 a 9 lados aumentará 7: \(20+7=\boxed{27}\) diagonales.", r"\(d\) goes up by 2, 3, 4, 5, 6…: not always the same, so it is <strong>not a straight line</strong>. Following the pattern, from 8 to 9 sides it goes up by 7: \(20+7=\boxed{27}\) diagonals."),
       P(r"La fórmula és \(d=\frac{n\,(n-3)}{2}\): per a \(n=9\), \(d=\frac{9\cdot6}{2}=27\) ✓.", r"La fórmula es \(d=\frac{n\,(n-3)}{2}\): para \(n=9\), \(d=\frac{9\cdot6}{2}=27\) ✓.", r"The formula is \(d=\frac{n\,(n-3)}{2}\): for \(n=9\), \(d=\frac{9\cdot6}{2}=27\) ✓."))])
ck(50 - fr('7.5'), '42.5'); ck(Fr(9 + 17, 2), 13); ck(Fr(9 * 6, 2), 27); ck(20 + 7, 27)
s2 += practice([('★☆☆', L(r"Completa la taula de \(y=4x-1\) per a \(x=0,\ 1,\ 2,\ 3\). Quins punts del gràfic obtens?", r"Completa la tabla de \(y=4x-1\) para \(x=0,\ 1,\ 2,\ 3\). ¿Qué puntos de la gráfica obtienes?", r"Complete the table of \(y=4x-1\) for \(x=0,\ 1,\ 2,\ 3\). Which points of the graph do you get?")),
                ('★★☆', L(r"Troba la fórmula de la taula \(x\): 0, 1, 2, 3; \(y\): 10, 8, 6, 4.", r"Halla la fórmula de la tabla \(x\): 0, 1, 2, 3; \(y\): 10, 8, 6, 4.", r"Find the formula for the table \(x\): 0, 1, 2, 3; \(y\): 10, 8, 6, 4."))],
               L(r"1) \(y=-1,\ 3,\ 7,\ 11\): \((0,\ -1)\), \((1,\ 3)\), \((2,\ 7)\), \((3,\ 11)\). &nbsp; 2) Disminueix 2 cada vegada i val 10 per a \(x=0\): \(y=-2x+10\).", r"1) \(y=-1,\ 3,\ 7,\ 11\): \((0,\ -1)\), \((1,\ 3)\), \((2,\ 7)\), \((3,\ 11)\). &nbsp; 2) Disminuye 2 cada vez y vale 10 para \(x=0\): \(y=-2x+10\).", r"1) \(y=-1,\ 3,\ 7,\ 11\): \((0,\ -1)\), \((1,\ 3)\), \((2,\ 7)\), \((3,\ 11)\). &nbsp; 2) It goes down by 2 each time and is 10 when \(x=0\): \(y=-2x+10\)."))
[ck(lin(4, -1)(k), v) for k, v in zip(range(4), [-1, 3, 7, 11])]; [ck(lin(-2, 10)(k), v) for k, v in zip(range(4), [10, 8, 6, 4])]
