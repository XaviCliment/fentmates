# Apartats 9.1-9.3 dels apunts de la Unitat 9 de 1r ESO: el pla cartesià i les coordenades d'un punt,
# aplicacions de les coordenades (plànols, jocs, figures, moviments) i relacions entre magnituds (taules i gràfics).
from comu import *

def quadrant(x, y):
    if x == 0 and y == 0: return 'O'
    if y == 0: return 'X'
    if x == 0: return 'Y'
    return 'I' if x > 0 and y > 0 else 'II' if x < 0 < y else 'III' if x < 0 and y < 0 else 'IV'

# =====================================================================
# 9.1 El pla cartesià. Coordenades d'un punt
# =====================================================================
W5 = (-5, 5, -5, 5)
PTS1 = [(3, 2, 'A'), (-2, 4, 'B'), (-4, -1, 'C'), (2, -3, 'D'), (4, 0, 'E'), (0, -2, 'F')]
assert [quadrant(x, y) for x, y, _ in PTS1] == ['I', 'II', 'III', 'IV', 'X', 'Y']
F_EIXOS = pla(W5, quad=True, labs=[(0.6, -0.6, 'O', 'hot')], W=260)
F_A = pla(W5, pts=[(3, 2, 'A(3, 2)', 'p0')], proj=[(3, 2)], curves=[([(0, 0.08), (3, 0.08)], 'c1 mv'), ([(3, 0), (3, 2)], 'c1 mv')], W=260)
F_PTS = pla(W5, pts=[(x, y, n, 'p0') for x, y, n in PTS1], W=280)

s1 = box('def', L('El pla cartesià', 'El plano cartesiano', 'The Cartesian plane'),
  P(r"Per a situar punts en un pla dibuixem dues rectes numèriques perpendiculars, els <strong>eixos de coordenades</strong>:",
    r"Para situar puntos en un plano dibujamos dos rectas numéricas perpendiculares, los <strong>ejes de coordenadas</strong>:",
    r"To locate points on a plane we draw two perpendicular number lines, the <strong>coordinate axes</strong>:")
  + ul(L(r"L'<strong>eix d'abscisses</strong> (eix \(X\)) és l'horitzontal. Els positius van cap a la dreta.",
         r"El <strong>eje de abscisas</strong> (eje \(X\)) es el horizontal. Los positivos van hacia la derecha.",
         r"The <strong>x-axis</strong> is the horizontal one. Positive numbers go to the right."),
       L(r"L'<strong>eix d'ordenades</strong> (eix \(Y\)) és el vertical. Els positius van cap amunt.",
         r"El <strong>eje de ordenadas</strong> (eje \(Y\)) es el vertical. Los positivos van hacia arriba.",
         r"The <strong>y-axis</strong> is the vertical one. Positive numbers go up."),
       L(r"Els eixos es tallen en l'<strong>origen de coordenades</strong>, el punt \(O\), i divideixen el pla en quatre <strong>quadrants</strong>, que es numeren I, II, III i IV en sentit contrari a les agulles del rellotge.",
         r"Los ejes se cortan en el <strong>origen de coordenadas</strong>, el punto \(O\), y dividen el plano en cuatro <strong>cuadrantes</strong>, que se numeran I, II, III y IV en sentido contrario a las agujas del reloj.",
         r"The axes cross at the <strong>origin</strong>, the point \(O\), and split the plane into four <strong>quadrants</strong>, numbered I, II, III and IV anticlockwise."))
  + figs(fig(F_EIXOS, L('Eixos, origen i quadrants', 'Ejes, origen y cuadrantes', 'Axes, origin and quadrants'))))

s1 += box('prop', L("Coordenades d'un punt", 'Coordenadas de un punto', 'Coordinates of a point'),
  P(r"Cada punt del pla té dues <strong>coordenades</strong>, que s'escriuen entre parèntesis i <strong>en aquest ordre</strong>: \(P(x,\ y)\).",
    r"Cada punto del plano tiene dos <strong>coordenadas</strong>, que se escriben entre paréntesis y <strong>en este orden</strong>: \(P(x,\ y)\).",
    r"Every point on the plane has two <strong>coordinates</strong>, written in brackets and <strong>in this order</strong>: \(P(x,\ y)\).")
  + ul(L(r"La primera, \(x\), és l'<strong>abscissa</strong>: quant ens movem en horitzontal des de l'origen (dreta \(+\), esquerra \(-\)).",
         r"La primera, \(x\), es la <strong>abscisa</strong>: cuánto nos movemos en horizontal desde el origen (derecha \(+\), izquierda \(-\)).",
         r"The first one, \(x\), is the <strong>x-coordinate</strong>: how far we move horizontally from the origin (right \(+\), left \(-\))."),
       L(r"La segona, \(y\), és l'<strong>ordenada</strong>: quant ens movem després en vertical (amunt \(+\), avall \(-\)).",
         r"La segunda, \(y\), es la <strong>ordenada</strong>: cuánto nos movemos después en vertical (arriba \(+\), abajo \(-\)).",
         r"The second one, \(y\), is the <strong>y-coordinate</strong>: how far we then move vertically (up \(+\), down \(-\))."))
  + P(r"Per a dibuixar \(A(3,\ 2)\): eixim de l'origen, avancem <strong>3 cap a la dreta</strong> i després <strong>2 cap amunt</strong>.",
      r"Para dibujar \(A(3,\ 2)\): salimos del origen, avanzamos <strong>3 hacia la derecha</strong> y después <strong>2 hacia arriba</strong>.",
      r"To plot \(A(3,\ 2)\): start at the origin, move <strong>3 to the right</strong> and then <strong>2 up</strong>.")
  + figs(fig(F_A, r'\(A(3,\ 2)\)'))
  + note(r"L'ordre importa: \((3,\ 2)\) i \((2,\ 3)\) són punts <strong>diferents</strong>. Recorda-ho així: primer caminem pel terra (\(x\)) i després pugem o baixem per l'escala (\(y\)).",
         r"El orden importa: \((3,\ 2)\) y \((2,\ 3)\) son puntos <strong>diferentes</strong>. Recuérdalo así: primero caminamos por el suelo (\(x\)) y después subimos o bajamos por la escalera (\(y\)).",
         r"Order matters: \((3,\ 2)\) and \((2,\ 3)\) are <strong>different</strong> points. Remember it like this: first walk along the floor (\(x\)), then climb up or down the ladder (\(y\)).", '⚠️'))

s1 += box('prop', L('Signes de les coordenades', 'Signos de las coordenadas', 'Signs of the coordinates'),
  P(r"Mirant els signes de les coordenades sabem en quin quadrant està un punt sense dibuixar-lo:",
    r"Mirando los signos de las coordenadas sabemos en qué cuadrante está un punto sin dibujarlo:",
    r"From the signs of the coordinates we know which quadrant a point is in without plotting it:")
  + tbl([L('Quadrant', 'Cuadrante', 'Quadrant'), 'I', 'II', 'III', 'IV'],
        [[L('Signes', 'Signos', 'Signs'), r'\((+,\ +)\)', r'\((-,\ +)\)', r'\((-,\ -)\)', r'\((+,\ -)\)'],
         [L('Exemple', 'Ejemplo', 'Example'), r'\(A(3,\ 2)\)', r'\(B(-2,\ 4)\)', r'\(C(-4,\ -1)\)', r'\(D(2,\ -3)\)']], 'c')
  + ul(L(r"Si l'<strong>ordenada és 0</strong>, el punt està sobre l'<strong>eix \(X\)</strong>: \(E(4,\ 0)\).",
         r"Si la <strong>ordenada es 0</strong>, el punto está sobre el <strong>eje \(X\)</strong>: \(E(4,\ 0)\).",
         r"If the <strong>y-coordinate is 0</strong>, the point lies on the <strong>x-axis</strong>: \(E(4,\ 0)\)."),
       L(r"Si l'<strong>abscissa és 0</strong>, el punt està sobre l'<strong>eix \(Y\)</strong>: \(F(0,\ -2)\). L'origen és \(O(0,\ 0)\).",
         r"Si la <strong>abscisa es 0</strong>, el punto está sobre el <strong>eje \(Y\)</strong>: \(F(0,\ -2)\). El origen es \(O(0,\ 0)\).",
         r"If the <strong>x-coordinate is 0</strong>, the point lies on the <strong>y-axis</strong>: \(F(0,\ -2)\). The origin is \(O(0,\ 0)\)."))
  + figs(fig(F_PTS, L('Els punts A, B, C, D, E i F', 'Los puntos A, B, C, D, E y F', 'The points A, B, C, D, E and F')))
  + widget('w-click', '📍', L('Explora el pla cartesià', 'Explora el plano cartesiano', 'Explore the Cartesian plane'),
           ['<p class="hint-s">' + L("Toca qualsevol lloc del pla o escriu les coordenades d'un punt.", "Toca cualquier lugar del plano o escribe las coordenadas de un punto.", "Tap anywhere on the plane or type a point's coordinates.") + '</p>',
            '<div class="wrow">' + tin('p', L('Punt', 'Punto', 'Point'), '(3, 2)', 'm') + f'<button class="btn" type="button" data-a="go">{L("Dibuixa", "Dibujar", "Plot")}</button></div>'],
           out='<div class="gout"></div>')
  + drill('read', 'Entrena: llig les coordenades', 'Entrena: lee las coordenadas', 'Train: read the coordinates', 'pair')
  + drill('place', 'Entrena: situa el punt', 'Entrena: sitúa el punto', 'Train: plot the point', 'click')
  + drill('quad', 'Entrena: on està el punt?', 'Entrena: ¿dónde está el punto?', 'Train: where is the point?', 'opts'))

PTS2 = [(1, 3, 'A'), (-3, 2, 'B'), (-1, -4, 'C'), (4, -2, 'D'), (0, 3, 'E'), (-5, 0, 'F')]
F_P1 = pla((-6, 5, -5, 4), pts=[(x, y, n, 'p0') for x, y, n in PTS2], W=280)
Q1 = [(3, -5), (-2, -7), (-4, 1), (0, 6), (5, 0), (8, 8)]
QN = {'I': L('quadrant I', 'cuadrante I', 'quadrant I'), 'II': L('quadrant II', 'cuadrante II', 'quadrant II'), 'III': L('quadrant III', 'cuadrante III', 'quadrant III'),
      'IV': L('quadrant IV', 'cuadrante IV', 'quadrant IV'), 'X': L('eix \\(X\\)', 'eje \\(X\\)', 'x-axis'), 'Y': L('eix \\(Y\\)', 'eje \\(Y\\)', 'y-axis')}
assert [quadrant(*p) for p in Q1] == ['IV', 'III', 'II', 'Y', 'X', 'I']
F_P3 = pla((-1, 6, -1, 6), pts=[(2, 5, 'P(2, 5)', 'p0'), (5, 2, 'Q(5, 2)', 'p1')], W=200)
F_P4 = pla((-5, 5, -5, 5), pts=[(k, k, None, 'p0') for k in range(-4, 5)], fns=[(1, 0, 'c0 dsh')], W=220)
s1 += levels(
 [prob(L(r"Escriu les coordenades dels punts de la figura.", r"Escribe las coordenadas de los puntos de la figura.", r"Write down the coordinates of the points in the figure.") + figs(fig(F_P1)),
       P(r"Per a cada punt, mirem primer quant està a la dreta o a l'esquerra de l'eix \(Y\) (abscissa) i després quant està amunt o avall de l'eix \(X\) (ordenada):",
         r"Para cada punto, miramos primero cuánto está a la derecha o a la izquierda del eje \(Y\) (abscisa) y después cuánto está arriba o abajo del eje \(X\) (ordenada):",
         r"For each point, first see how far it is right or left of the y-axis (x-coordinate) and then how far it is above or below the x-axis (y-coordinate):"),
       D(r"\boxed{A(1,\ 3)}\quad \boxed{B(-3,\ 2)}\quad \boxed{C(-1,\ -4)}\quad \boxed{D(4,\ -2)}\quad \boxed{E(0,\ 3)}\quad \boxed{F(-5,\ 0)}"),
       P(r"Fixa't que \(E\) està sobre l'eix \(Y\) (abscissa 0) i \(F\), sobre l'eix \(X\) (ordenada 0).", r"Fíjate en que \(E\) está sobre el eje \(Y\) (abscisa 0) y \(F\), sobre el eje \(X\) (ordenada 0).", r"Notice that \(E\) is on the y-axis (x-coordinate 0) and \(F\) is on the x-axis (y-coordinate 0).")),
  prob(L(r"Sense dibuixar-los, digues on està cada punt: \((3,\ -5)\), \((-2,\ -7)\), \((-4,\ 1)\), \((0,\ 6)\), \((5,\ 0)\), \((8,\ 8)\).",
         r"Sin dibujarlos, di dónde está cada punto: \((3,\ -5)\), \((-2,\ -7)\), \((-4,\ 1)\), \((0,\ 6)\), \((5,\ 0)\), \((8,\ 8)\).",
         r"Without plotting them, say where each point is: \((3,\ -5)\), \((-2,\ -7)\), \((-4,\ 1)\), \((0,\ 6)\), \((5,\ 0)\), \((8,\ 8)\)."),
       P(r"Mirem els signes \((x,\ y)\): \((+,\ +)\) I, \((-,\ +)\) II, \((-,\ -)\) III, \((+,\ -)\) IV; si una coordenada és 0, el punt està sobre un eix.",
         r"Miramos los signos \((x,\ y)\): \((+,\ +)\) I, \((-,\ +)\) II, \((-,\ -)\) III, \((+,\ -)\) IV; si una coordenada es 0, el punto está sobre un eje.",
         r"Look at the signs \((x,\ y)\): \((+,\ +)\) I, \((-,\ +)\) II, \((-,\ -)\) III, \((+,\ -)\) IV; if a coordinate is 0, the point is on an axis."),
       '<ul>' + ''.join(f'<li>\\(({x},\\ {y})\\) → <strong>{QN[quadrant(x, y)]}</strong></li>' for x, y in Q1) + '</ul>')],
 [prob(L(r"Dibuixa els punts \(P(2,\ 5)\) i \(Q(5,\ 2)\). Són el mateix punt?", r"Dibuja los puntos \(P(2,\ 5)\) y \(Q(5,\ 2)\). ¿Son el mismo punto?", r"Plot the points \(P(2,\ 5)\) and \(Q(5,\ 2)\). Are they the same point?"),
       P(r"\(P\): 2 a la dreta i 5 amunt. \(Q\): 5 a la dreta i 2 amunt.", r"\(P\): 2 a la derecha y 5 arriba. \(Q\): 5 a la derecha y 2 arriba.", r"\(P\): 2 right and 5 up. \(Q\): 5 right and 2 up.") + figs(fig(F_P3)),
       P(r"<strong>No</strong>: són punts diferents. En unes coordenades, l'ordre importa.", r"<strong>No</strong>: son puntos diferentes. En unas coordenadas, el orden importa.", r"<strong>No</strong>: they are different points. In coordinates, order matters.")),
  prob(L(r"Escriu les coordenades del punt: a) que està 4 unitats a l'esquerra de l'eix \(Y\) i 2 per damunt de l'eix \(X\); b) que està sobre l'eix \(Y\), 3 unitats per davall de l'origen; c) que té l'abscissa \(-1\) i l'ordenada el triple de l'abscissa.",
         r"Escribe las coordenadas del punto: a) que está 4 unidades a la izquierda del eje \(Y\) y 2 por encima del eje \(X\); b) que está sobre el eje \(Y\), 3 unidades por debajo del origen; c) que tiene la abscisa \(-1\) y la ordenada el triple de la abscisa.",
         r"Write the coordinates of the point: a) 4 units to the left of the y-axis and 2 above the x-axis; b) on the y-axis, 3 units below the origin; c) whose x-coordinate is \(-1\) and whose y-coordinate is three times the x-coordinate."),
       D(r"\text{a) } \boxed{(-4,\ 2)}\qquad \text{b) } \boxed{(0,\ -3)}\qquad \text{c) } y=3\cdot(-1)=-3\ \Rightarrow\ \boxed{(-1,\ -3)}"))],
 [prob(L(r"Dibuixa tots els punts de coordenades enteres que tenen <strong>l'ordenada igual a l'abscissa</strong>, entre \(-4\) i \(4\). Què observes?",
         r"Dibuja todos los puntos de coordenadas enteras que tienen <strong>la ordenada igual a la abscisa</strong>, entre \(-4\) y \(4\). ¿Qué observas?",
         r"Plot all the points with whole-number coordinates whose <strong>y-coordinate equals the x-coordinate</strong>, between \(-4\) and \(4\). What do you notice?"),
       P(r"Són \((-4,\ -4),\ (-3,\ -3),\ \dots,\ (0,\ 0),\ (1,\ 1),\ \dots,\ (4,\ 4)\).", r"Son \((-4,\ -4),\ (-3,\ -3),\ \dots,\ (0,\ 0),\ (1,\ 1),\ \dots,\ (4,\ 4)\).", r"They are \((-4,\ -4),\ (-3,\ -3),\ \dots,\ (0,\ 0),\ (1,\ 1),\ \dots,\ (4,\ 4)\).") + figs(fig(F_P4)),
       P(r"Tots estan <strong>alineats</strong> sobre una recta que passa per l'origen i travessa els quadrants I i III. Ho estudiarem a l'apartat 9.5: és la gràfica de \(y=x\).",
         r"Todos están <strong>alineados</strong> sobre una recta que pasa por el origen y atraviesa los cuadrantes I y III. Lo estudiaremos en el apartado 9.5: es la gráfica de \(y=x\).",
         r"They all lie <strong>in a straight line</strong> through the origin, crossing quadrants I and III. We'll study it in section 9.5: it's the graph of \(y=x\)."))])
s1 += practice([('★☆☆', L(r"Dibuixa en uns eixos els punts \(A(2,\ 1)\), \(B(-3,\ 4)\), \(C(-2,\ -2)\), \(D(0,\ -4)\) i \(E(5,\ 0)\) i digues on està cadascun.",
                          r"Dibuja en unos ejes los puntos \(A(2,\ 1)\), \(B(-3,\ 4)\), \(C(-2,\ -2)\), \(D(0,\ -4)\) y \(E(5,\ 0)\) y di dónde está cada uno.",
                          r"Plot the points \(A(2,\ 1)\), \(B(-3,\ 4)\), \(C(-2,\ -2)\), \(D(0,\ -4)\) and \(E(5,\ 0)\) on a pair of axes and say where each one is.")),
                ('★★☆', L(r"Un punt està en el quadrant II i la distància a cada eix és 3. Quines són les seues coordenades?", r"Un punto está en el cuadrante II y su distancia a cada eje es 3. ¿Cuáles son sus coordenadas?", r"A point is in quadrant II and is 3 units from each axis. What are its coordinates?"))],
               L(r"1) \(A\): I; \(B\): II; \(C\): III; \(D\): eix \(Y\); \(E\): eix \(X\). &nbsp; 2) En el quadrant II, \(x\) és negativa i \(y\) positiva: \((-3,\ 3)\).",
                 r"1) \(A\): I; \(B\): II; \(C\): III; \(D\): eje \(Y\); \(E\): eje \(X\). &nbsp; 2) En el cuadrante II, \(x\) es negativa e \(y\) positiva: \((-3,\ 3)\).",
                 r"1) \(A\): I; \(B\): II; \(C\): III; \(D\): y-axis; \(E\): x-axis. &nbsp; 2) In quadrant II, \(x\) is negative and \(y\) positive: \((-3,\ 3)\)."))
assert quadrant(2, 1) == 'I' and quadrant(-3, 4) == 'II' and quadrant(-2, -2) == 'III' and quadrant(0, -4) == 'Y' and quadrant(5, 0) == 'X'

# =====================================================================
# 9.2 Aplicacions de les coordenades
# =====================================================================
LLOCS = [(1, 3, '🏫', L("l'institut", 'el instituto', 'the school')), (-3, 2, '🏠', L('casa de la Marta', 'casa de Marta', "Marta's house")), (4, -2, '⚽', L('el poliesportiu', 'el polideportivo', 'the sports centre')),
         (-2, -3, '🌳', L('el parc', 'el parque', 'the park')), (0, 0, '⛲', L('la plaça (origen)', 'la plaza (origen)', 'the square (origin)')), (3, 1, '📚', L('la biblioteca', 'la biblioteca', 'the library'))]
F_MAPA = pla((-5, 5, -4, 4), labs=[(x, y - 0.25, e, 'emo') for x, y, e, _ in LLOCS], W=300, arrows=False)
def poly_per(V):
    return sum(abs(V[i][0] - V[(i + 1) % len(V)][0]) + abs(V[i][1] - V[(i + 1) % len(V)][1]) for i in range(len(V)))
RV = [(-3, -1), (4, -1), (4, 3), (-3, 3)]
assert poly_per(RV) == 22 and 7 * 4 == 28
F_RECT = pla((-4, 5, -2, 4), polys=[(RV, 'pg0')], pts=[(-3, -1, 'A', 'p0', -8, 16), (4, -1, 'B', 'p0', 7, 16), (4, 3, 'C', 'p0'), (-3, 3, 'D', 'p0', -8, -8)], W=280)
TRI = [(1, 1), (4, 2), (2, 4)]
F_MOV = pla((-6, 6, -5, 5), polys=[(TRI, 'pg0'), ([(x, -y) for x, y in TRI], 'pg1'), ([(-x, y) for x, y in TRI], 'pg2')],
            labs=[(2.4, 2.4, 'T', ''), (2.4, -2.6, "T'", ''), (-2.4, 2.4, "T''", '')], W=280)

s2 = box('def', L('Plànols, mapes i jocs', 'Planos, mapas y juegos', 'Maps, plans and games'),
  P(r"Les coordenades serveixen per a dir <strong>on està</strong> una cosa amb només dos nombres. Si posem l'origen en la plaça del poble i cada quadre és una illa de cases, podem localitzar cada lloc:",
    r"Las coordenadas sirven para decir <strong>dónde está</strong> una cosa con solo dos números. Si ponemos el origen en la plaza del pueblo y cada cuadro es una manzana de casas, podemos localizar cada lugar:",
    r"Coordinates let us say <strong>where</strong> something is with just two numbers. If we put the origin in the town square and each square of the grid is a block of houses, we can locate every place:")
  + '<div class="gout">' + F_MAPA + '<div class="gcol">' + ''.join(f'<p>{e} {n}: \\(({x},\\ {y})\\)</p>' for x, y, e, n in LLOCS) + '</div></div>'
  + ul(L(r"En el joc d'<strong>enfonsar la flota</strong> o en els <strong>escacs</strong>, cada casella té una lletra (columna) i un nombre (fila): B4, E7…",
         r"En el juego de <strong>hundir la flota</strong> o en el <strong>ajedrez</strong>, cada casilla tiene una letra (columna) y un número (fila): B4, E7…",
         r"In <strong>Battleships</strong> or <strong>chess</strong>, each square has a letter (column) and a number (row): B4, E7…"),
       L(r"En un <strong>cine</strong> o un <strong>teatre</strong>, l'entrada diu la fila i el seient. En una <strong>full de càlcul</strong>, cada cel·la té una columna i una fila.",
         r"En un <strong>cine</strong> o un <strong>teatro</strong>, la entrada dice la fila y el asiento. En una <strong>hoja de cálculo</strong>, cada celda tiene una columna y una fila.",
         r"In a <strong>cinema</strong> or a <strong>theatre</strong>, the ticket gives the row and the seat. In a <strong>spreadsheet</strong>, each cell has a column and a row."),
       L(r"Els <strong>GPS</strong> situen qualsevol lloc de la Terra amb dues coordenades: la <strong>latitud</strong> i la <strong>longitud</strong>. València està, més o menys, en \((39^\circ\text{ N},\ 0{,}4^\circ\text{ O})\).",
         r"Los <strong>GPS</strong> sitúan cualquier lugar de la Tierra con dos coordenadas: la <strong>latitud</strong> y la <strong>longitud</strong>. Valencia está, más o menos, en \((39^\circ\text{ N},\ 0{,}4^\circ\text{ O})\).",
         r"<strong>GPS</strong> locates any place on Earth with two coordinates: <strong>latitude</strong> and <strong>longitude</strong>. Valencia is roughly at \((39^\circ\text{ N},\ 0.4^\circ\text{ W})\)."))
  + widget('w-treasure', '🏴‍☠️', L('Busca el tresor', 'Busca el tesoro', 'Find the treasure'),
           ['<p class="hint-s">' + L("Hi ha un tresor amagat en un punt de coordenades enteres. Toca el pla o escriu un punt: et direm cap a on has d'anar.", "Hay un tesoro escondido en un punto de coordenadas enteras. Toca el plano o escribe un punto: te diremos hacia dónde tienes que ir.", "A treasure is hidden at a point with whole-number coordinates. Tap the plane or type a point: we'll tell you which way to go.") + '</p>',
            '<div class="wrow">' + tin('p', L('Punt', 'Punto', 'Point'), '', 'm') + f'<button class="btn primary" type="button" data-a="go">{L("Busca", "Buscar", "Search")}</button><button class="btn" type="button" data-a="new">🎲 {L("Un altre tresor", "Otro tesoro", "Another treasure")}</button></div>'],
           out='<div class="gout"></div>'))

s2 += box('prop', L('Figures en el pla', 'Figuras en el plano', 'Shapes on the plane'),
  P(r"Un polígon queda determinat per les coordenades dels seus <strong>vèrtexs</strong>. Si dos punts estan en la mateixa <strong>horitzontal</strong> (mateixa \(y\)), la distància entre ells és la diferència de les abscisses; si estan en la mateixa <strong>vertical</strong> (mateixa \(x\)), la diferència de les ordenades.",
    r"Un polígono queda determinado por las coordenadas de sus <strong>vértices</strong>. Si dos puntos están en la misma <strong>horizontal</strong> (misma \(y\)), la distancia entre ellos es la diferencia de las abscisas; si están en la misma <strong>vertical</strong> (misma \(x\)), la diferencia de las ordenadas.",
    r"A polygon is fixed by the coordinates of its <strong>vertices</strong>. If two points are on the same <strong>horizontal</strong> line (same \(y\)), the distance between them is the difference of the x-coordinates; if they're on the same <strong>vertical</strong> line (same \(x\)), the difference of the y-coordinates.")
  + '<div class="gout">' + F_RECT + '<div class="gcol"><p>' + L(r"Rectangle \(A(-3,\ -1)\), \(B(4,\ -1)\), \(C(4,\ 3)\), \(D(-3,\ 3)\):", r"Rectángulo \(A(-3,\ -1)\), \(B(4,\ -1)\), \(C(4,\ 3)\), \(D(-3,\ 3)\):", r"Rectangle \(A(-3,\ -1)\), \(B(4,\ -1)\), \(C(4,\ 3)\), \(D(-3,\ 3)\):")
  + r'</p><p>\(AB=4-(-3)=7\)</p><p>\(BC=3-(-1)=4\)</p><p>\(P=2\cdot7+2\cdot4=22\)</p><p>\(A=7\cdot4=28\)</p></div></div>'
  + P(r"Les coordenades també descriuen els <strong>moviments</strong> d'una figura:", r"Las coordenadas también describen los <strong>movimientos</strong> de una figura:", r"Coordinates also describe how a shape <strong>moves</strong>:")
  + ul(L(r"<strong>Desplaçar</strong> (translació) 3 a la dreta i 2 cap avall: sumem 3 a la \(x\) i restem 2 a la \(y\): \((x,\ y)\to(x+3,\ y-2)\).",
         r"<strong>Desplazar</strong> (traslación) 3 a la derecha y 2 hacia abajo: sumamos 3 a la \(x\) y restamos 2 a la \(y\): \((x,\ y)\to(x+3,\ y-2)\).",
         r"<strong>Slide</strong> (translation) 3 right and 2 down: add 3 to \(x\) and subtract 2 from \(y\): \((x,\ y)\to(x+3,\ y-2)\)."),
       L(r"<strong>Simetria respecte de l'eix \(X\)</strong> (com un espill horitzontal): canvia el signe de la \(y\): \((x,\ y)\to(x,\ -y)\).",
         r"<strong>Simetría respecto del eje \(X\)</strong> (como un espejo horizontal): cambia el signo de la \(y\): \((x,\ y)\to(x,\ -y)\).",
         r"<strong>Reflection in the x-axis</strong> (like a horizontal mirror): the sign of \(y\) changes: \((x,\ y)\to(x,\ -y)\)."),
       L(r"<strong>Simetria respecte de l'eix \(Y\)</strong>: canvia el signe de la \(x\): \((x,\ y)\to(-x,\ y)\).",
         r"<strong>Simetría respecto del eje \(Y\)</strong>: cambia el signo de la \(x\): \((x,\ y)\to(-x,\ y)\).",
         r"<strong>Reflection in the y-axis</strong>: the sign of \(x\) changes: \((x,\ y)\to(-x,\ y)\)."))
  + figs(fig(F_MOV, L(r"El triangle \(T\) i els seus simètrics respecte de l'eix \(X\) (\(T'\)) i de l'eix \(Y\) (\(T''\))", r"El triángulo \(T\) y sus simétricos respecto del eje \(X\) (\(T'\)) y del eje \(Y\) (\(T''\))", r"Triangle \(T\) and its reflections in the x-axis (\(T'\)) and the y-axis (\(T''\))")))
  + widget('w-poly', '🔷', L('Polígons i moviments', 'Polígonos y movimientos', 'Polygons and moves'),
           ['<div class="wrow">' + tin('v', L('Vèrtexs', 'Vértices', 'Vertices'), '(1, 1) (4, 1) (4, 3) (1, 3)', 'w') + f'<button class="btn" type="button" data-a="go">{L("Dibuixa", "Dibujar", "Plot")}</button></div>',
            seg([('mv', L('Desplaça', 'Desplaza', 'Slide')), ('sx', L('Simètric eix X', 'Simétrico eje X', 'Reflect in x-axis')), ('sy', L('Simètric eix Y', 'Simétrico eje Y', 'Reflect in y-axis'))]),
            '<div class="wrow rmv">' + rng('dx', -6, 6, 1, -5, 'dx') + rng('dy', -6, 6, 1, -4, 'dy') + '</div>'],
           out='<div class="gout"></div>')
  + drill('dist', 'Entrena: distància en horitzontal o en vertical', 'Entrena: distancia en horizontal o en vertical', 'Train: horizontal or vertical distance'))

F_Q1 = pla((-1, 7, -1, 6), polys=[([(0, 0), (6, 0), (2, 4)], 'pg0')], pts=[(0, 0, 'A', 'p0', -8, 16), (6, 0, 'B', 'p0', 7, 16), (2, 4, 'C', 'p0')], proj=[(2, 4)], W=240)
assert 6 * 4 / 2 == 12
ROB = [(0, 0), (3, 0), (3, 2), (-2, 2), (-2, -2)]
F_ROB = pla((-4, 5, -3, 4), curves=[(ROB, 'c0')], pts=[(0, 0, 'S', 'p1', -8, 16), (-2, -2, 'F', 'p0', -8, 16)], W=240)
TRI2 = [(-4, 1), (-1, 1), (-3, 4)]
TRI2b = [(x + 5, y - 3) for x, y in TRI2]
assert TRI2b == [(1, -2), (4, -2), (2, 1)]
F_TR = pla((-5, 5, -3, 5), polys=[(TRI2, 'pg0'), (TRI2b, 'pg1')], labs=[(-2.7, 1.9, 'T', ''), (2.3, -1.1, "T'", '')], W=260)
s2 += levels(
 [prob(L(r"Mira el plànol del principi de l'apartat. Quin lloc hi ha en \((-2,\ -3)\)? Quines són les coordenades de la biblioteca? I de l'institut?",
         r"Mira el plano del principio del apartado. ¿Qué lugar hay en \((-2,\ -3)\)? ¿Cuáles son las coordenadas de la biblioteca? ¿Y del instituto?",
         r"Look at the map at the start of the section. What place is at \((-2,\ -3)\)? What are the coordinates of the library? And of the school?"),
       P(r"\((-2,\ -3)\): 2 a l'esquerra i 3 avall: hi ha el <strong>parc</strong> 🌳.", r"\((-2,\ -3)\): 2 a la izquierda y 3 abajo: está el <strong>parque</strong> 🌳.", r"\((-2,\ -3)\): 2 left and 3 down: it's the <strong>park</strong> 🌳."),
       P(r"Biblioteca: \(\boxed{(3,\ 1)}\). Institut: \(\boxed{(1,\ 3)}\). Fixa't que s'intercanvien els nombres i són llocs diferents.", r"Biblioteca: \(\boxed{(3,\ 1)}\). Instituto: \(\boxed{(1,\ 3)}\). Fíjate en que se intercambian los números y son lugares diferentes.", r"Library: \(\boxed{(3,\ 1)}\). School: \(\boxed{(1,\ 3)}\). Notice the numbers are swapped and they're different places.")),
  prob(L(r"Dibuixa el rectangle de vèrtexs \(A(-3,\ -1)\), \(B(4,\ -1)\), \(C(4,\ 3)\) i \(D(-3,\ 3)\) i calcula'n el perímetre i l'àrea (la unitat és el cm).",
         r"Dibuja el rectángulo de vértices \(A(-3,\ -1)\), \(B(4,\ -1)\), \(C(4,\ 3)\) y \(D(-3,\ 3)\) y calcula su perímetro y su área (la unidad es el cm).",
         r"Plot the rectangle with vertices \(A(-3,\ -1)\), \(B(4,\ -1)\), \(C(4,\ 3)\) and \(D(-3,\ 3)\) and find its perimeter and area (the unit is the cm)."),
       P(r"És el rectangle dibuixat més amunt. \(A\) i \(B\) tenen la mateixa \(y\): la base fa \(4-(-3)=7\) cm. \(B\) i \(C\) tenen la mateixa \(x\): l'altura fa \(3-(-1)=4\) cm.",
         r"Es el rectángulo dibujado más arriba. \(A\) y \(B\) tienen la misma \(y\): la base mide \(4-(-3)=7\) cm. \(B\) y \(C\) tienen la misma \(x\): la altura mide \(3-(-1)=4\) cm.",
         r"It's the rectangle drawn above. \(A\) and \(B\) have the same \(y\): the base is \(4-(-3)=7\) cm. \(B\) and \(C\) have the same \(x\): the height is \(3-(-1)=4\) cm."),
       D(r"P=2\cdot7+2\cdot4=\boxed{22\ \text{cm}}\qquad A=7\cdot4=\boxed{28\ \text{cm}^2}"))],
 [prob(L(r"Tres vèrtexs d'un quadrat són \((1,\ 1)\), \((4,\ 1)\) i \((4,\ 4)\). Quin és el quart vèrtex?", r"Tres vértices de un cuadrado son \((1,\ 1)\), \((4,\ 1)\) y \((4,\ 4)\). ¿Cuál es el cuarto vértice?", r"Three vertices of a square are \((1,\ 1)\), \((4,\ 1)\) and \((4,\ 4)\). What is the fourth vertex?"),
       P(r"El costat fa 3. El quart vèrtex ha d'estar damunt de \((1,\ 1)\), a la mateixa altura que \((4,\ 4)\):", r"El lado mide 3. El cuarto vértice tiene que estar encima de \((1,\ 1)\), a la misma altura que \((4,\ 4)\):", r"The side is 3. The fourth vertex must be above \((1,\ 1)\), at the same height as \((4,\ 4)\):"),
       D(r"\boxed{(1,\ 4)}")),
  prob(L(r"Un robot ix de l'origen i fa aquests moviments: 3 cap a la dreta, 2 cap amunt, 5 cap a l'esquerra i 4 cap avall. On acaba?", r"Un robot sale del origen y hace estos movimientos: 3 hacia la derecha, 2 hacia arriba, 5 hacia la izquierda y 4 hacia abajo. ¿Dónde termina?", r"A robot starts at the origin and moves: 3 right, 2 up, 5 left and 4 down. Where does it end up?"),
       P(r"Anem sumant: a la dreta \(+\), a l'esquerra \(-\) (en la \(x\)); amunt \(+\), avall \(-\) (en la \(y\)):", r"Vamos sumando: a la derecha \(+\), a la izquierda \(-\) (en la \(x\)); arriba \(+\), abajo \(-\) (en la \(y\)):", r"Keep adding: right \(+\), left \(-\) (for \(x\)); up \(+\), down \(-\) (for \(y\)):"),
       D(r"(0,\ 0)\to(3,\ 0)\to(3,\ 2)\to(-2,\ 2)\to\boxed{(-2,\ -2)}") + figs(fig(F_ROB))),
  prob(L(r"El triangle \(T\) té els vèrtexs \((-4,\ 1)\), \((-1,\ 1)\) i \((-3,\ 4)\). Desplaça'l 5 unitats a la dreta i 3 cap avall. Quins són els vèrtexs nous?",
         r"El triángulo \(T\) tiene los vértices \((-4,\ 1)\), \((-1,\ 1)\) y \((-3,\ 4)\). Desplázalo 5 unidades a la derecha y 3 hacia abajo. ¿Cuáles son los nuevos vértices?",
         r"Triangle \(T\) has vertices \((-4,\ 1)\), \((-1,\ 1)\) and \((-3,\ 4)\). Slide it 5 units right and 3 down. What are the new vertices?"),
       P(r"Sumem 5 a cada abscissa i restem 3 a cada ordenada:", r"Sumamos 5 a cada abscisa y restamos 3 a cada ordenada:", r"Add 5 to each x-coordinate and subtract 3 from each y-coordinate:"),
       D(r"(-4,\ 1)\to\boxed{(1,\ -2)}\qquad (-1,\ 1)\to\boxed{(4,\ -2)}\qquad (-3,\ 4)\to\boxed{(2,\ 1)}") + figs(fig(F_TR)))],
 [prob(L(r"Calcula l'àrea del triangle de vèrtexs \(A(0,\ 0)\), \(B(6,\ 0)\) i \(C(2,\ 4)\).", r"Calcula el área del triángulo de vértices \(A(0,\ 0)\), \(B(6,\ 0)\) y \(C(2,\ 4)\).", r"Find the area of the triangle with vertices \(A(0,\ 0)\), \(B(6,\ 0)\) and \(C(2,\ 4)\).") + figs(fig(F_Q1)),
       P(r"La base \(AB\) està sobre l'eix \(X\) i fa 6. L'altura és la distància de \(C\) a l'eix \(X\): la seua ordenada, 4.", r"La base \(AB\) está sobre el eje \(X\) y mide 6. La altura es la distancia de \(C\) al eje \(X\): su ordenada, 4.", r"The base \(AB\) lies on the x-axis and is 6 long. The height is the distance from \(C\) to the x-axis: its y-coordinate, 4."),
       D(r"A=\frac{b\cdot h}{2}=\frac{6\cdot4}{2}=\boxed{12\ \text{u}^2}"))])
s2 += practice([('★☆☆', L(r"Escriu els vèrtexs del simètric respecte de l'eix \(Y\) del triangle \((1,\ 2)\), \((5,\ 2)\), \((3,\ 6)\).", r"Escribe los vértices del simétrico respecto del eje \(Y\) del triángulo \((1,\ 2)\), \((5,\ 2)\), \((3,\ 6)\).", r"Write the vertices of the reflection in the y-axis of the triangle \((1,\ 2)\), \((5,\ 2)\), \((3,\ 6)\).")),
                ('★★☆', L(r"Quina distància hi ha entre \((-2,\ 5)\) i \((-2,\ -3)\)? I entre \((-6,\ 1)\) i \((3,\ 1)\)?", r"¿Qué distancia hay entre \((-2,\ 5)\) y \((-2,\ -3)\)? ¿Y entre \((-6,\ 1)\) y \((3,\ 1)\)?", r"How far apart are \((-2,\ 5)\) and \((-2,\ -3)\)? And \((-6,\ 1)\) and \((3,\ 1)\)?"))],
               L(r"1) \((-1,\ 2)\), \((-5,\ 2)\), \((-3,\ 6)\). &nbsp; 2) Mateixa \(x\): \(5-(-3)=8\). Mateixa \(y\): \(3-(-6)=9\).",
                 r"1) \((-1,\ 2)\), \((-5,\ 2)\), \((-3,\ 6)\). &nbsp; 2) Misma \(x\): \(5-(-3)=8\). Misma \(y\): \(3-(-6)=9\).",
                 r"1) \((-1,\ 2)\), \((-5,\ 2)\), \((-3,\ 6)\). &nbsp; 2) Same \(x\): \(5-(-3)=8\). Same \(y\): \(3-(-6)=9\)."))
ck(5 - (-3), 8); ck(3 - (-6), 9)

# =====================================================================
# 9.3 Relacions entre magnituds: taules i gràfics
# =====================================================================
KG = [0, 1, 2, 3, 4, 5]
EUR = [ck(fr('1.5') * k, v) for k, v in zip(KG, ['0', '1.5', '3', '4.5', '6', '7.5'])]
F_POMES = pla((0, 5.6, 0, 8.4), fns=[('1.5', 0, 'c0', 0, 5)], pts=[(k, fr('1.5') * k, None, 'p0') for k in KG], W=240, xl='kg', yl='€', ys=1.5, gy=1.5, H=240)
ENT = [1, 2, 3, 4, 5]
F_ENT = pla((0, 5.6, 0, 42), pts=[(k, 8 * k, None, 'p0') for k in ENT], W=240, H=220, xl=Ls('entrades', 'entradas', 'tickets'), yl='€', ys=8, gy=8)
HORES = [0, 4, 8, 12, 16, 20, 24]
TEMP = [6, 4, 9, 17, 19, 12, 7]
F_TEMP = pla((0, 25, 0, 21), curves=[([(h, t) for h, t in zip(HORES, TEMP)], 'c0')], pts=[(h, t, None, 'p0') for h, t in zip(HORES, TEMP)], W=300, H=220, xs=4, gx=2, ys=4, gy=2, xl='h', yl='°C')

s3 = box('def', L('Magnituds relacionades', 'Magnitudes relacionadas', 'Related quantities'),
  P(r"Moltes vegades dues <strong>magnituds</strong> estan relacionades: quan canvia una, canvia l'altra. Per exemple, el <strong>pes</strong> de pomes que comprem i el <strong>preu</strong> que paguem, o l'<strong>hora</strong> del dia i la <strong>temperatura</strong>.",
    r"Muchas veces dos <strong>magnitudes</strong> están relacionadas: cuando cambia una, cambia la otra. Por ejemplo, el <strong>peso</strong> de manzanas que compramos y el <strong>precio</strong> que pagamos, o la <strong>hora</strong> del día y la <strong>temperatura</strong>.",
    r"Two <strong>quantities</strong> are often related: when one changes, so does the other. For example, the <strong>weight</strong> of apples we buy and the <strong>price</strong> we pay, or the <strong>time</strong> of day and the <strong>temperature</strong>.")
  + ul(L(r"La <strong>variable independent</strong> (\(x\)) és la que triem o la que passa sola (els kg, l'hora). Va en l'<strong>eix horitzontal</strong>.",
         r"La <strong>variable independiente</strong> (\(x\)) es la que elegimos o la que pasa sola (los kg, la hora). Va en el <strong>eje horizontal</strong>.",
         r"The <strong>independent variable</strong> (\(x\)) is the one we choose or that just goes on (kg, time of day). It goes on the <strong>horizontal axis</strong>."),
       L(r"La <strong>variable dependent</strong> (\(y\)) és la que <strong>depén</strong> de l'altra (el preu, la temperatura). Va en l'<strong>eix vertical</strong>.",
         r"La <strong>variable dependiente</strong> (\(y\)) es la que <strong>depende</strong> de la otra (el precio, la temperatura). Va en el <strong>eje vertical</strong>.",
         r"The <strong>dependent variable</strong> (\(y\)) is the one that <strong>depends</strong> on the other (price, temperature). It goes on the <strong>vertical axis</strong>."))
  + P(r"Escrivim la relació en una <strong>taula de valors</strong>, cada parell de la taula és un <strong>punt</strong> \((x,\ y)\) i els punts formen el <strong>gràfic</strong>. Les pomes valen 1,50 € el kg:",
      r"Escribimos la relación en una <strong>tabla de valores</strong>, cada pareja de la tabla es un <strong>punto</strong> \((x,\ y)\) y los puntos forman la <strong>gráfica</strong>. Las manzanas valen 1,50 € el kg:",
      r"We write the relation in a <strong>table of values</strong>; each pair in the table is a <strong>point</strong> \((x,\ y)\) and the points make up the <strong>graph</strong>. Apples cost €1.50 per kg:")
  + '<div class="gout"><div class="gcol">' + tv(KG, [tn(v) for v in EUR], L('Pes (kg)', 'Peso (kg)', 'Weight (kg)'), L('Preu (€)', 'Precio (€)', 'Price (€)')) + '<p>'
  + L(r"Punts: \((0,\ 0)\), \((1;\ 1{,}5)\), \((2,\ 3)\), \((3;\ 4{,}5)\)…", r"Puntos: \((0,\ 0)\), \((1;\ 1{,}5)\), \((2,\ 3)\), \((3;\ 4{,}5)\)…", r"Points: \((0,\ 0)\), \((1,\ 1.5)\), \((2,\ 3)\), \((3,\ 4.5)\)…") + '</p></div>' + F_POMES + '</div>'
  + note(r"Quan una coordenada té decimals, separem les dues coordenades amb punt i coma: \((1;\ 1{,}5)\). Així no es confon la coma decimal.",
         r"Cuando una coordenada tiene decimales, separamos las dos coordenadas con punto y coma: \((1;\ 1{,}5)\). Así no se confunde la coma decimal.",
         r"In Spanish and Valencian, where the decimal mark is a comma, the two coordinates are separated with a semicolon when there are decimals: \((1;\ 1{,}5)\). In English we just write \((1,\ 1.5)\)."))

s3 += box('prop', L('Com es fa un gràfic', 'Cómo se hace una gráfica', 'How to draw a graph'),
  ol(L(r"Dibuixem els eixos i hi escrivim el <strong>nom de cada magnitud</strong> i la <strong>unitat</strong> (kg, €, h, °C…).", r"Dibujamos los ejes y escribimos el <strong>nombre de cada magnitud</strong> y la <strong>unidad</strong> (kg, €, h, °C…).", r"Draw the axes and label them with the <strong>name of each quantity</strong> and its <strong>unit</strong> (kg, €, h, °C…)."),
     L(r"Triem una <strong>escala</strong> per a cada eix: cada quadre pot valdre 1, 2, 5, 10… L'escala d'un eix no ha de ser igual que la de l'altre, però en cada eix les divisions han de ser <strong>iguals</strong>.",
       r"Elegimos una <strong>escala</strong> para cada eje: cada cuadro puede valer 1, 2, 5, 10… La escala de un eje no tiene que ser igual que la del otro, pero en cada eje las divisiones tienen que ser <strong>iguales</strong>.",
       r"Choose a <strong>scale</strong> for each axis: each square can stand for 1, 2, 5, 10… The two axes can have different scales, but on each axis the divisions must be <strong>equal</strong>."),
     L(r"Dibuixem els <strong>punts</strong> de la taula.", r"Dibujamos los <strong>puntos</strong> de la tabla.", r"Plot the <strong>points</strong> from the table."),
     L(r"Decidim si <strong>unim els punts</strong>: els unim si també tenen sentit els valors intermedis (1,5 kg de pomes, les 10 h); no els unim si només hi ha valors solts (nombre d'entrades, de persones…).",
       r"Decidimos si <strong>unimos los puntos</strong>: los unimos si también tienen sentido los valores intermedios (1,5 kg de manzanas, las 10 h); no los unimos si solo hay valores sueltos (número de entradas, de personas…).",
       r"Decide whether to <strong>join the points</strong>: join them if in-between values make sense too (1.5 kg of apples, 10 o'clock); don't join them if only separate values are possible (number of tickets, of people…)."))
  + '<div class="figs">' + fig(F_ENT, L('Entrades a 8 €: punts solts', 'Entradas a 8 €: puntos sueltos', 'Tickets at €8: separate points')) + fig(F_TEMP, L('Temperatura al llarg d\'un dia: punts units', 'Temperatura a lo largo de un día: puntos unidos', 'Temperature over a day: points joined')) + '</div>'
  + widget('w-table', '📋', L('De la taula al gràfic', 'De la tabla a la gráfica', 'From table to graph'),
           [seg([('pom', L('Pomes', 'Manzanas', 'Apples')), ('ent', L('Entrades', 'Entradas', 'Tickets')), ('tmp', L('Temperatura', 'Temperatura', 'Temperature')), ('own', L('La meua taula', 'Mi tabla', 'My table'))]),
            '<div class="wrow">' + tin('x', 'x', '0 1 2 3 4 5', 'w') + '</div>', '<div class="wrow">' + tin('y', 'y', '0 1,5 3 4,5 6 7,5', 'w') + '</div>',
            seg([('1', L('Uneix els punts', 'Unir los puntos', 'Join the points')), ('0', L('Punts solts', 'Puntos sueltos', 'Separate points'))])],
           out='<div class="gout"></div>'))

s3 += box('def', L('Funcions', 'Funciones', 'Functions'),
  P(r"Una relació entre dues variables és una <strong>funció</strong> si a cada valor de \(x\) li correspon <strong>un únic</strong> valor de \(y\). Una funció es pot donar de quatre maneres:",
    r"Una relación entre dos variables es una <strong>función</strong> si a cada valor de \(x\) le corresponde <strong>un único</strong> valor de \(y\). Una función se puede dar de cuatro maneras:",
    r"A relation between two variables is a <strong>function</strong> if each value of \(x\) gives <strong>exactly one</strong> value of \(y\). A function can be given in four ways:")
  + tbl([L('Manera', 'Forma', 'Form'), L('Exemple: les pomes', 'Ejemplo: las manzanas', 'Example: the apples')],
        [[L('<strong>Enunciat</strong> (amb paraules)', '<strong>Enunciado</strong> (con palabras)', '<strong>In words</strong>'), L('«Cada kg val 1,50 €»', '«Cada kg vale 1,50 €»', '“Each kg costs €1.50”')],
         [L('<strong>Taula</strong> de valors', '<strong>Tabla</strong> de valores', '<strong>Table</strong> of values'), r'\(\begin{array}{c|c|c|c}x&1&2&3\\\hline y&1{,}5&3&4{,}5\end{array}\)'],
         [L('<strong>Gràfic</strong>', '<strong>Gráfica</strong>', '<strong>Graph</strong>'), L('la recta de més amunt', 'la recta de más arriba', 'the line above')],
         [L('<strong>Fórmula</strong> (expressió algebraica)', '<strong>Fórmula</strong> (expresión algebraica)', '<strong>Formula</strong> (algebraic expression)'), r'\(y=1{,}5\cdot x\)']])
  + P(r"Amb la fórmula calculem qualsevol valor: per a \(x=8\) kg, \(y=1{,}5\cdot8=12\) €.", r"Con la fórmula calculamos cualquier valor: para \(x=8\) kg, \(y=1{,}5\cdot8=12\) €.", r"With the formula we can work out any value: for \(x=8\) kg, \(y=1.5\cdot8=12\) €.")
  + note(r"No totes les relacions són funcions: si en una taula el mateix \(x\) apareix amb dos \(y\) diferents, no és una funció. Per exemple, l'edat i l'altura dels alumnes d'una classe: dos alumnes de 12 anys poden tindre altures diferents.",
         r"No todas las relaciones son funciones: si en una tabla el mismo \(x\) aparece con dos \(y\) diferentes, no es una función. Por ejemplo, la edad y la altura de los alumnos de una clase: dos alumnos de 12 años pueden tener alturas diferentes.",
         r"Not every relation is a function: if the same \(x\) appears in a table with two different \(y\) values, it isn't a function. For example, the age and height of the pupils in a class: two 12-year-olds may have different heights.", '⚠️')
  + drill('tab', 'Entrena: calcula amb la fórmula', 'Entrena: calcula con la fórmula', 'Train: use the formula')
  + drill('formula', 'Entrena: quina fórmula correspon a la taula?', 'Entrena: ¿qué fórmula corresponde a la tabla?', 'Train: which formula matches the table?', 'opts'))
ck(fr('1.5') * 8, 12)

LL = [1, 2, 3, 4, 5]
F_LL = pla((0, 5.6, 0, 3.4), pts=[(k, fr('0.6') * k, None, 'p0') for k in LL], W=240, H=200, xl=Ls('llapis', 'lápices', 'pencils'), yl='€', ys=0.6, gy=0.6)
LLv = [ck(fr('0.6') * k, v) for k, v in zip(LL, ['0.6', '1.2', '1.8', '2.4', '3'])]
F_QUA = pla((0, 5.6, 0, 22), pts=[(l, 4 * l, None, 'p0') for l in range(1, 6)] + [(l, l * l, None, 'p1') for l in range(1, 5)],
            fns=[(4, 0, 'c0', 0, 5)], curves=[([(t / 10, (t / 10) ** 2) for t in range(0, 47)], 'c1')], W=260, H=240, xs=1, ys=4, gy=2, xl='l', yl='')
s3 += levels(
 [prob(L(r"Un llapis val 0,60 €. Fes una taula amb el preu d'1, 2, 3, 4 i 5 llapis i dibuixa'n el gràfic. Has d'unir els punts?", r"Un lápiz vale 0,60 €. Haz una tabla con el precio de 1, 2, 3, 4 y 5 lápices y dibuja su gráfica. ¿Tienes que unir los puntos?", r"A pencil costs €0.60. Make a table of the price of 1, 2, 3, 4 and 5 pencils and draw its graph. Should you join the points?"),
       P(r"Multipliquem per 0,60 el nombre de llapis:", r"Multiplicamos por 0,60 el número de lápices:", r"Multiply the number of pencils by 0.60:") + tv(LL, [tn(v) for v in LLv], L('Llapis', 'Lápices', 'Pencils'), L('Preu (€)', 'Precio (€)', 'Price (€)')),
       P(r"En l'eix vertical cada quadre val 0,60 €. <strong>No</strong> unim els punts: no es pot comprar mig llapis.", r"En el eje vertical cada cuadro vale 0,60 €. <strong>No</strong> unimos los puntos: no se puede comprar medio lápiz.", r"On the vertical axis each square is €0.60. We <strong>don't</strong> join the points: you can't buy half a pencil.") + figs(fig(F_LL))),
  prob(L(r"Mira el gràfic de la temperatura d'un dia (més amunt). Quina temperatura feia a les 12 h? A quina hora feia més calor? I més fred?", r"Mira la gráfica de la temperatura de un día (más arriba). ¿Qué temperatura hacía a las 12 h? ¿A qué hora hacía más calor? ¿Y más frío?", r"Look at the graph of the temperature over a day (above). What was the temperature at 12:00? When was it hottest? And coldest?"),
       P(r"Busquem 12 en l'eix horitzontal, pugem fins a la línia i mirem l'altura: \(\boxed{17\ ^\circ\text{C}}\).", r"Buscamos 12 en el eje horizontal, subimos hasta la línea y miramos la altura: \(\boxed{17\ ^\circ\text{C}}\).", r"Find 12 on the horizontal axis, go up to the line and read the height: \(\boxed{17\ ^\circ\text{C}}\)."),
       P(r"El punt més alt és el de les <strong>16 h</strong> (19 °C) i el més baix, el de les <strong>4 h</strong> (4 °C).", r"El punto más alto es el de las <strong>16 h</strong> (19 °C) y el más bajo, el de las <strong>4 h</strong> (4 °C).", r"The highest point is at <strong>16:00</strong> (19 °C) and the lowest at <strong>4:00</strong> (4 °C)."))],
 [prob(L(r"Fes una taula de valors de la funció \(y=3x+2\) per a \(x=0,\ 1,\ 2,\ 3\) i escriu els punts.", r"Haz una tabla de valores de la función \(y=3x+2\) para \(x=0,\ 1,\ 2,\ 3\) y escribe los puntos.", r"Make a table of values for the function \(y=3x+2\) for \(x=0,\ 1,\ 2,\ 3\) and write down the points."),
       D(r"x=0:\ y=3\cdot0+2=2\qquad x=1:\ y=3\cdot1+2=5\qquad x=2:\ y=3\cdot2+2=8\qquad x=3:\ y=3\cdot3+2=11"),
       tv([0, 1, 2, 3], [2, 5, 8, 11]) + P(r"Punts: \((0,\ 2)\), \((1,\ 5)\), \((2,\ 8)\), \((3,\ 11)\).", r"Puntos: \((0,\ 2)\), \((1,\ 5)\), \((2,\ 8)\), \((3,\ 11)\).", r"Points: \((0,\ 2)\), \((1,\ 5)\), \((2,\ 8)\), \((3,\ 11)\).")),
  prob(L(r"Digues quina és la variable independent i quina la dependent: a) els litres de gasolina i el preu; b) els minuts que parles per telèfon i el que pagues; c) l'edat d'un arbre i la seua altura.",
         r"Di cuál es la variable independiente y cuál la dependiente: a) los litros de gasolina y el precio; b) los minutos que hablas por teléfono y lo que pagas; c) la edad de un árbol y su altura.",
         r"Say which is the independent and which the dependent variable: a) litres of petrol and price; b) minutes on the phone and what you pay; c) a tree's age and its height."),
       P(r"La dependent és la que <strong>depén</strong> de l'altra:", r"La dependiente es la que <strong>depende</strong> de la otra:", r"The dependent one is the one that <strong>depends</strong> on the other:"),
       ul(L(r"a) independent: litres; dependent: preu.", r"a) independiente: litros; dependiente: precio.", r"a) independent: litres; dependent: price."),
          L(r"b) independent: minuts; dependent: el que pagues.", r"b) independiente: minutos; dependiente: lo que pagas.", r"b) independent: minutes; dependent: what you pay."),
          L(r"c) independent: edat; dependent: altura.", r"c) independiente: edad; dependiente: altura.", r"c) independent: age; dependent: height.")))],
 [prob(L(r"Fes una taula del <strong>perímetre</strong> i una de l'<strong>àrea</strong> d'un quadrat de costat \(l=1,\ 2,\ 3,\ 4\) cm, escriu-ne les fórmules i dibuixa els dos gràfics. Són rectes?",
         r"Haz una tabla del <strong>perímetro</strong> y una del <strong>área</strong> de un cuadrado de lado \(l=1,\ 2,\ 3,\ 4\) cm, escribe sus fórmulas y dibuja las dos gráficas. ¿Son rectas?",
         r"Make a table of the <strong>perimeter</strong> and one of the <strong>area</strong> of a square with side \(l=1,\ 2,\ 3,\ 4\) cm, write their formulas and draw both graphs. Are they straight lines?"),
       tv([1, 2, 3, 4], [4, 8, 12, 16], 'l', 'P') + tv([1, 2, 3, 4], [1, 4, 9, 16], 'l', 'A'),
       D(r"P=4\cdot l\qquad A=l^2") + figs(fig(F_QUA, L('<span class="key k0"></span>perímetre &nbsp; <span class="key k1"></span>àrea', '<span class="key k0"></span>perímetro &nbsp; <span class="key k1"></span>área', '<span class="key k0"></span>perimeter &nbsp; <span class="key k1"></span>area'))),
       P(r"Els punts del perímetre estan <strong>alineats</strong>: el gràfic és una recta (cada cm més de costat suma sempre 4 cm). Els de l'àrea <strong>no</strong>: el gràfic és una corba que puja cada vegada més de pressa (suma 3, 5, 7…).",
         r"Los puntos del perímetro están <strong>alineados</strong>: la gráfica es una recta (cada cm más de lado suma siempre 4 cm). Los del área <strong>no</strong>: la gráfica es una curva que sube cada vez más deprisa (suma 3, 5, 7…).",
         r"The perimeter points are <strong>in a line</strong>: the graph is straight (each extra cm of side always adds 4 cm). The area points are <strong>not</strong>: the graph is a curve that rises faster and faster (adding 3, 5, 7…)."))])
s3 += practice([('★☆☆', L(r"Completa la taula de \(y=2x-1\) per a \(x=0,\ 1,\ 2,\ 3,\ 4\).", r"Completa la tabla de \(y=2x-1\) para \(x=0,\ 1,\ 2,\ 3,\ 4\).", r"Complete the table of \(y=2x-1\) for \(x=0,\ 1,\ 2,\ 3,\ 4\).")),
                ('★★☆', L(r"Una entrada al museu val 6 € i l'aparcament, 3 € per cotxe. Escriu la fórmula del preu \(y\) per a una família de \(x\) persones que va en un cotxe.", r"Una entrada al museo vale 6 € y el aparcamiento, 3 € por coche. Escribe la fórmula del precio \(y\) para una familia de \(x\) personas que va en un coche.", r"A museum ticket costs €6 and parking is €3 per car. Write the formula for the price \(y\) for a family of \(x\) people who go in one car."))],
               L(r"1) \(y=-1,\ 1,\ 3,\ 5,\ 7\). &nbsp; 2) \(y=6x+3\) (per a 4 persones: \(y=27\) €).", r"1) \(y=-1,\ 1,\ 3,\ 5,\ 7\). &nbsp; 2) \(y=6x+3\) (para 4 personas: \(y=27\) €).", r"1) \(y=-1,\ 1,\ 3,\ 5,\ 7\). &nbsp; 2) \(y=6x+3\) (for 4 people: \(y=27\) €)."))
assert [2 * k - 1 for k in range(5)] == [-1, 1, 3, 5, 7] and 6 * 4 + 3 == 27 and [3 * k + 2 for k in range(4)] == [2, 5, 8, 11]
