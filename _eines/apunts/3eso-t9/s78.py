# 9.7 Àrea del cercle i figures circulars · 9.8 Figures compostes i problemes
from comu import *

def T_(P, t, **o): return ('txt', P, t, o)
def pol(C, r, a): return (C[0] + r * math.cos(math.radians(a)), C[1] + r * math.sin(math.radians(a)))
def ringfig(R_, r_, a0=0, a1=360, cls='sh'):
    """corona (o trapezi circular si a1-a0 < 360): sector gran ombrejat i sector petit «buit»"""
    if a1 - a0 >= 360: it = [('circ', (0, 0), R_, cls), ('circ', (0, 0), r_, 'hole')]
    else: it = [('sect', (0, 0), R_, a0, a1, cls), ('sect', (0, 0), r_, a0, a1, 'hole'), ('circ', (0, 0), R_, 'gc'), ('circ', (0, 0), r_, 'gc')]
    return it

# =====================================================================
# 9.7 Àrea del cercle i figures circulars
# =====================================================================
s7 = box('prop', L('Àrea del cercle', 'Área del círculo', 'Area of a disc'),
  D(r"A=\pi r^2")
  + P(r"D'on ix? Tallem el cercle en molts sectors iguals (com una pizza) i els col·loquem alternats, un cap amunt i un cap avall. Com més sectors fem, més s'assembla la figura a un <strong>rectangle</strong> de base la meitat de la circumferència, \(\pi r\), i d'altura el radi, \(r\): l'àrea és \(\pi r\cdot r=\pi r^2\).",
      r"¿De dónde sale? Cortamos el círculo en muchos sectores iguales (como una pizza) y los colocamos alternados, uno hacia arriba y otro hacia abajo. Cuantos más sectores hacemos, más se parece la figura a un <strong>rectángulo</strong> de base la mitad de la circunferencia, \(\pi r\), y de altura el radio, \(r\): el área es \(\pi r\cdot r=\pi r^2\).",
      r"Where does it come from? Cut the disc into many equal sectors (like a pizza) and lay them side by side, alternately pointing up and down. The more sectors, the more the shape looks like a <strong>rectangle</strong> whose base is half the circumference, \(\pi r\), and whose height is the radius, \(r\): the area is \(\pi r\cdot r=\pi r^2\).")
  + widget('w-pizza', '🍕', L('Del cercle al rectangle', 'Del círculo al rectángulo', 'From disc to rectangle'),
           ['<div class="wrow">' + rng('n', 4, 40, 2, 8, 'n') + '</div>'], out='<div class="gout"></div>'))
s7 += box('prop', L('Figures circulars', 'Figuras circulares', 'Circular shapes'),
  figs(G([('sect', (0, 0), 3, 20, 120, 'sh'), ('circ', (0, 0), 3, 'gc'), ('arc', (0, 0), 0.8, 20, 120, 'ang'), ('dot', (0, 0)), T_(pol((0, 0), 1.25, 70), 'n°'), T_(pol((0, 0), 1.6, -60), 'r')], W=160,
         cap=L(r'Sector circular: \(A=\dfrac{\pi r^2\cdot n}{360}\)', r'Sector circular: \(A=\dfrac{\pi r^2\cdot n}{360}\)', r'Sector: \(A=\dfrac{\pi r^2\cdot n}{360}\)')),
       G(ringfig(3, 1.8) + [('seg', (0, 0), pol((0, 0), 3, 30), ''), ('seg', (0, 0), pol((0, 0), 1.8, 150), 'd'), ('dot', (0, 0)), T_(pol((0, 0), 2.3, 42), 'R'), T_(pol((0, 0), 0.9, 168), 'r')], W=160,
         cap=L(r'Corona circular: \(A=\pi\left(R^2-r^2\right)\)', r'Corona circular: \(A=\pi\left(R^2-r^2\right)\)', r'Annulus: \(A=\pi\left(R^2-r^2\right)\)')),
       G(ringfig(3, 1.6, 30, 140) + [('dot', (0, 0)), T_(pol((0, 0), 2.3, 85), 'n°'), T_(pol((0, 0), 2.6, 15), 'R'), T_(pol((0, 0), 1.2, 15), 'r')], W=160,
         cap=L(r'Trapezi circular: \(A=\dfrac{\pi\left(R^2-r^2\right)\cdot n}{360}\)', r'Trapecio circular: \(A=\dfrac{\pi\left(R^2-r^2\right)\cdot n}{360}\)', r'Annular sector: \(A=\dfrac{\pi\left(R^2-r^2\right)\cdot n}{360}\)')), three=True)
  + P(r"El <strong>segment circular</strong> és la part del cercle compresa entre una corda i el seu arc. La seua àrea és la del sector menys la del triangle que formen els dos radis i la corda.",
      r"El <strong>segmento circular</strong> es la parte del círculo comprendida entre una cuerda y su arco. Su área es la del sector menos la del triángulo que forman los dos radios y la cuerda.",
      r"A <strong>segment</strong> is the part of the disc between a chord and its arc. Its area is the sector's minus the triangle formed by the two radii and the chord.")
  + widget('w-circa', '🎯', L('Àrees de figures circulars', 'Áreas de figuras circulares', 'Areas of circular shapes'),
           [seg([('c', L('Cercle', 'Círculo', 'Disc')), ('s', 'Sector'), ('k', 'Corona'), ('t', L('Trapezi circular', 'Trapecio circular', 'Annular sector'))]),
            '<div class="wrow">' + rng('R', 1, 10, 0.5, 5, 'R') + rng('r', 0.5, 9.5, 0.5, 3, 'r') + rng('n', 5, 355, 5, 90, 'n') + '</div>'], out='<div class="gout"></div>')
  + drill('circa', 'Entrena: àrees circulars', 'Entrena: áreas circulares', 'Train: circular areas'))
s7 += levels(
 [prob(L(r"Una pizza fa 30 cm de diàmetre. Quina és la seua superfície?", r"Una pizza mide 30 cm de diámetro. ¿Cuál es su superficie?", r"A pizza is 30 cm across. What is its area?"),
       D(r"r=15\qquad A=\pi\cdot15^2=225\pi\approx\boxed{706{,}86\ \text{cm}^2}")),
  prob(L(r"Calcula l'àrea d'un sector circular de 60° i 12 cm de radi.", r"Calcula el área de un sector circular de 60° y 12 cm de radio.", r"Find the area of a 60° sector with a 12 cm radius."),
       D(r"A=\frac{\pi\cdot12^2\cdot60}{360}=\frac{144\pi}{6}=24\pi\approx\boxed{75{,}40\ \text{cm}^2}"))],
 [prob(L(r"Calcula l'àrea d'una corona circular de radis 10 cm i 6 cm.", r"Calcula el área de una corona circular de radios 10 cm y 6 cm.", r"Find the area of an annulus with radii 10 cm and 6 cm."),
       D(r"A=\pi\left(10^2-6^2\right)=64\pi\approx\boxed{201{,}06\ \text{cm}^2}")),
  prob(L(r"Què té més pizza: una pizza de 40 cm de diàmetre o dues de 28 cm?", r"¿Qué tiene más pizza: una pizza de 40 cm de diámetro o dos de 28 cm?", r"Which has more pizza: one 40 cm pizza or two 28 cm pizzas?"),
       D(r"A_1=\pi\cdot20^2=400\pi\approx1256{,}64\ \text{cm}^2\qquad A_2=2\cdot\pi\cdot14^2=392\pi\approx1231{,}50\ \text{cm}^2"),
       P(r"La pizza <strong>gran</strong> té més superfície, encara que \(40<2\cdot28\): l'àrea depén del <strong>quadrat</strong> del radi.", r"La pizza <strong>grande</strong> tiene más superficie, aunque \(40<2\cdot28\): el área depende del <strong>cuadrado</strong> del radio.", r"The <strong>big</strong> pizza has more area, even though \(40<2\cdot28\): area depends on the <strong>square</strong> of the radius."))],
 [prob(L(r"Calcula l'àrea del segment circular determinat per un angle de 90° en un cercle de 4 cm de radi.", r"Calcula el área del segmento circular determinado por un ángulo de 90° en un círculo de 4 cm de radio.", r"Find the area of the segment cut off by a 90° angle in a disc with a 4 cm radius."),
       figs(G([('sect', (0, 0), 4, 0, 90, 'gf'), ('poly', [(0, 0), (4, 0), (0, 4)], 'hole'), ('circ', (0, 0), 4, 'gc'), ('seg', (0, 0), (4, 0), ''), ('seg', (0, 0), (0, 4), ''), ('seg', (4, 0), (0, 4), ''), ('ra', (0, 0), (1, 0), (0, 1)),
                ('dot', (0, 0)), T_((2, 0), '4', dy=-6), T_((0, 2), '4', dx=-8, a='end')], W=170)),
       D(r"A_{\text{sector}}=\frac{\pi\cdot4^2\cdot90}{360}=4\pi\qquad A_{\text{%s}}=\frac{4\cdot4}{2}=8" % Lt('triangle', 'triángulo', 'triangle')),
       D(r"A=4\pi-8\approx\boxed{4{,}57\ \text{cm}^2}")),
  prob(L(r"Un cercle té 50,27 cm² d'àrea. Calcula'n el radi i la longitud de la circumferència.", r"Un círculo tiene 50,27 cm² de área. Calcula su radio y la longitud de su circunferencia.", r"A disc has an area of 50.27 cm². Find its radius and its circumference."),
       D(r"\pi r^2=50{,}27\ \Rightarrow\ r^2=\frac{50{,}27}{\pi}\approx16{,}00\ \Rightarrow\ \boxed{r\approx4\ \text{cm}}\qquad L=2\pi\cdot4\approx\boxed{25{,}13\ \text{cm}}"))])
ck(225 * pi, 706.86, 2); ck(144 * pi * 60 / 360, 75.40, 2); ck(64 * pi, 201.06, 2); ck(400 * pi, 1256.64, 2); ck(392 * pi, 1231.50, 2)
ck(4 * pi - 8, 4.57, 2); ck(R(5027, 100) / pi, 16.00, 2); ck(S(R(5027, 100) / pi), 4, 2); ck(8 * pi, 25.13, 2)
s7 += practice([
  ('★', L(r"a) Àrea d'un cercle de 7 cm de radi. b) Àrea d'un sector de 90° i 6 cm de radi.", r"a) Área de un círculo de 7 cm de radio. b) Área de un sector de 90° y 6 cm de radio.", r"a) Area of a disc with a 7 cm radius. b) Area of a 90° sector with a 6 cm radius.")),
  ('★★', L(r"c) Àrea d'una corona de diàmetres 20 cm i 16 cm. d) Àrea d'un trapezi circular de radis 8 cm i 5 cm i 120°.", r"c) Área de una corona de diámetros 20 cm y 16 cm. d) Área de un trapecio circular de radios 8 cm y 5 cm y 120°.", r"c) Area of an annulus with diameters 20 cm and 16 cm. d) Area of a 120° annular sector with radii 8 cm and 5 cm.")),
  ('★★★', L(r"e) Un cercle té la mateixa àrea que un quadrat de 10 cm de costat. Quant mesura el radi?", r"e) Un círculo tiene la misma área que un cuadrado de 10 cm de lado. ¿Cuánto mide el radio?", r"e) A disc has the same area as a square with 10 cm sides. How long is its radius?"))],
  P(r"a) \(49\pi\approx153{,}94\) cm². b) \(9\pi\approx28{,}27\) cm². c) \(\pi(100-64)=36\pi\approx113{,}10\) cm². d) \(\tfrac{\pi(64-25)\cdot120}{360}=13\pi\approx40{,}84\) cm². e) \(\pi r^2=100\Rightarrow r=\sqrt{100/\pi}\approx5{,}64\) cm.",
    r"a) \(49\pi\approx153{,}94\) cm². b) \(9\pi\approx28{,}27\) cm². c) \(\pi(100-64)=36\pi\approx113{,}10\) cm². d) \(\tfrac{\pi(64-25)\cdot120}{360}=13\pi\approx40{,}84\) cm². e) \(\pi r^2=100\Rightarrow r=\sqrt{100/\pi}\approx5{,}64\) cm.",
    r"a) \(49\pi\approx153.94\) cm². b) \(9\pi\approx28.27\) cm². c) \(\pi(100-64)=36\pi\approx113.10\) cm². d) \(\tfrac{\pi(64-25)\cdot120}{360}=13\pi\approx40.84\) cm². e) \(\pi r^2=100\Rightarrow r=\sqrt{100/\pi}\approx5.64\) cm."))
ck(49 * pi, 153.94, 2); ck(36 * pi / 4, 28.27, 2); ck(36 * pi, 113.10, 2); ck(pi * 39 * 120 / 360, 40.84, 2); ck(S(100 / pi), 5.64, 2)

# =====================================================================
# 9.8 Figures compostes i problemes
# =====================================================================
LSH = [('poly', [(0, 0), (10, 0), (10, 3), (4, 3), (4, 8), (0, 8)], 'gf'), ('seg', (4, 0), (4, 3), 'd'),
       T_((5, 0), '10', dy=15), T_((0, 4), '8', dx=-8, a='end'), T_((2, 8), '4', dy=-7), T_((10, 1.5), '3', dx=8, a='start')]
SQC = [('poly', [(0, 0), (10, 0), (10, 10), (0, 10)], 'sh'), ('circ', (5, 5), 5, 'hole'), ('circ', (5, 5), 5, 'gc'), ('dot', (5, 5)), ('seg', (5, 5), (10, 5), 'd'), T_((5, 0), '10', dy=15), T_((7.5, 5), '5', dy=-6)]
WIN = [('poly', [(0, 0), (1.2, 0), (1.2, 1.5), (0, 1.5)], 'gf'), ('sect', (0.6, 1.5), 0.6, 0, 180, 'gf'), ('dot', (0.6, 1.5)), T_((0.6, 0), '1,2 m', dy=15), T_((1.2, 0.75), '1,5 m', dx=8, a='start')]
LEAF = [('poly', [(0, 0), (6, 0), (6, 6), (0, 6)], 'gf'), ('lens', (6, 0), (0, 6), 6, 'sh'), ('arc', (0, 0), 6, 0, 90, ''), ('arc', (6, 6), 6, 180, 270, ''), ('seg', (6, 0), (0, 6), 'd'), T_((3, 0), '6', dy=15), T_((0, 3), '6', dx=-8, a='end')]
s8 = box('prop', L('Àrees de figures compostes', 'Áreas de figuras compuestas', 'Areas of composite shapes'),
  P(r"Per a calcular l'àrea d'una figura que no té fórmula pròpia hi ha dues estratègies:", r"Para calcular el área de una figura que no tiene fórmula propia hay dos estrategias:", r"To find the area of a shape with no formula of its own there are two strategies:")
  + ol(L(r"<strong>Descompondre</strong> la figura en figures conegudes (rectangles, triangles, sectors…) i <strong>sumar</strong> les seues àrees.", r"<strong>Descomponer</strong> la figura en figuras conocidas (rectángulos, triángulos, sectores…) y <strong>sumar</strong> sus áreas.", r"<strong>Split</strong> the shape into known shapes (rectangles, triangles, sectors…) and <strong>add</strong> their areas."),
       L(r"Veure-la com una figura més gran a la qual <strong>llevem</strong> trossos, i <strong>restar</strong>.", r"Verla como una figura más grande a la que le <strong>quitamos</strong> trozos, y <strong>restar</strong>.", r"See it as a bigger shape with pieces <strong>removed</strong>, and <strong>subtract</strong>."))
  + figs(G(LSH, W=170, cap=r'\(A=4\cdot8+6\cdot3=50\)'), G(SQC, W=170, cap=r'\(A=10^2-\pi\cdot5^2\approx21{,}46\)'), three=True)
  + note(r"El <strong>perímetre</strong> d'una figura composta és només la longitud del seu contorn exterior: no compten les línies que hem traçat per dins per a descompondre-la.",
         r"El <strong>perímetro</strong> de una figura compuesta es solo la longitud de su contorno exterior: no cuentan las líneas que hemos trazado por dentro para descomponerla.",
         r"The <strong>perimeter</strong> of a composite shape is only the length of its outer boundary: the lines we drew inside to split it don't count.", '⚠️')
  + widget('w-comp', '🧱', L('Figures compostes', 'Figuras compuestas', 'Composite shapes'),
           [seg([('fin', L('Finestra', 'Ventana', 'Window')), ('forat', L('Quadrat menys cercle', 'Cuadrado menos círculo', 'Square minus disc')), ('fulla', L('Fulla', 'Hoja', 'Leaf')), ('cami', L('Camí al voltant d\'un jardí', 'Camino alrededor de un jardín', 'Path around a garden'))]),
            '<div class="wrow">' + rng('a', 1, 12, 0.5, 6, 'a') + rng('b', 0.5, 12, 0.5, 4, 'b') + rng('c', 0.5, 3, 0.25, 1, 'c') + '</div>'], out='<div class="gout"></div>')
  + drill('comp', 'Entrena: figures compostes', 'Entrena: figuras compuestas', 'Train: composite shapes'))
ck(4 * 8 + 6 * 3, 50); ck(10 * 8 - 6 * 5, 50); ck(100 - 25 * pi, 21.46, 2)
s8 += levels(
 [prob(L(r"Calcula l'àrea i el perímetre de la figura en forma de L (mesures en metres).", r"Calcula el área y el perímetro de la figura en forma de L (medidas en metros).", r"Find the area and the perimeter of the L-shaped figure (lengths in metres).") + figs(G(LSH, W=170)),
       P(r"La dividim en dos rectangles (línia discontínua):", r"La dividimos en dos rectángulos (línea discontinua):", r"Split it into two rectangles (dashed line):"),
       D(r"A=4\cdot8+6\cdot3=32+18=\boxed{50\ \text{m}^2}"),
       D(r"P=10+3+6+5+4+8=\boxed{36\ \text{m}}"))],
 [prob(L(r"Una finestra té forma de rectangle d'1,2 m d'amplària i 1,5 m d'altura acabat en un semicercle. Calcula'n la superfície i la longitud del marc.", r"Una ventana tiene forma de rectángulo de 1,2 m de ancho y 1,5 m de alto acabado en un semicírculo. Calcula su superficie y la longitud del marco.", r"A window is a 1.2 m wide, 1.5 m tall rectangle topped by a semicircle. Find its area and the length of its frame.") + figs(G(WIN, W=120)),
       D(r"A=1{,}2\cdot1{,}5+\frac{\pi\cdot0{,}6^2}{2}=1{,}8+0{,}18\pi\approx\boxed{2{,}37\ \text{m}^2}"),
       D(r"P=1{,}2+2\cdot1{,}5+\frac{2\pi\cdot0{,}6}{2}=4{,}2+0{,}6\pi\approx\boxed{6{,}08\ \text{m}}")),
  prob(L(r"Calcula l'àrea de la zona ombrejada: un quadrat de 10 cm de costat amb un cercle inscrit.", r"Calcula el área de la zona sombreada: un cuadrado de 10 cm de lado con un círculo inscrito.", r"Find the shaded area: a square with 10 cm sides with an inscribed disc.") + figs(G(SQC, W=150)),
       D(r"A=10^2-\pi\cdot5^2=100-25\pi\approx\boxed{21{,}46\ \text{cm}^2}"))],
 [prob(L(r"Calcula l'àrea de la «fulla» ombrejada dins del quadrat de 6 cm de costat. Els arcs són quarts de circumferència amb centre en dos vèrtexs oposats.", r"Calcula el área de la «hoja» sombreada dentro del cuadrado de 6 cm de lado. Los arcos son cuartos de circunferencia con centro en dos vértices opuestos.", r"Find the area of the shaded “leaf” inside the square with 6 cm sides. The arcs are quarter circles centred at two opposite corners.") + figs(G(LEAF, W=150)),
       P(r"La diagonal divideix la fulla en dues meitats iguals. Cada meitat és un quart de cercle menys un triangle (mig quadrat):", r"La diagonal divide la hoja en dos mitades iguales. Cada mitad es un cuarto de círculo menos un triángulo (medio cuadrado):", r"The diagonal splits the leaf into two equal halves. Each half is a quarter disc minus a triangle (half the square):"),
       D(r"\frac{\pi\cdot6^2}{4}-\frac{6\cdot6}{2}=9\pi-18\qquad A=2\,(9\pi-18)=18\pi-36\approx\boxed{20{,}55\ \text{cm}^2}")),
  prob(L(r"Un televisor de 55 polzades té una pantalla de proporció 16:9 (l'amplària i l'altura són proporcionals a 16 i 9). La mida en polzades és la de la diagonal, i 1 polzada són 2,54 cm. Quant mesura la pantalla?", r"Un televisor de 55 pulgadas tiene una pantalla de proporción 16:9 (el ancho y el alto son proporcionales a 16 y 9). La medida en pulgadas es la de la diagonal, y 1 pulgada son 2,54 cm. ¿Cuánto mide la pantalla?", r"A 55-inch TV has a 16:9 screen (width and height are proportional to 16 and 9). The size in inches is the diagonal, and 1 inch is 2.54 cm. How big is the screen?"),
       D(r"d=55\cdot2{,}54=139{,}7\ \text{cm}"),
       P(r"Si l'amplària és \(16k\) i l'altura \(9k\):", r"Si el ancho es \(16k\) y el alto \(9k\):", r"If the width is \(16k\) and the height \(9k\):"),
       D(r"(16k)^2+(9k)^2=139{,}7^2\ \Rightarrow\ 337k^2=19\,516{,}09\ \Rightarrow\ k\approx7{,}61"),
       D(r"16k\approx\boxed{121{,}8\ \text{cm}}\qquad 9k\approx\boxed{68{,}5\ \text{cm}}")),
  prob(L(r"Un jardí rectangular de 20 m × 12 m està envoltat per un camí d'1,5 m d'amplària. Calcula la superfície del camí.", r"Un jardín rectangular de 20 m × 12 m está rodeado por un camino de 1,5 m de ancho. Calcula la superficie del camino.", r"A 20 m × 12 m rectangular garden is surrounded by a 1.5 m wide path. Find the area of the path."),
       P(r"El rectangle exterior fa \(20+2\cdot1{,}5=23\) m per \(12+2\cdot1{,}5=15\) m. Restem el jardí:", r"El rectángulo exterior mide \(20+2\cdot1{,}5=23\) m por \(12+2\cdot1{,}5=15\) m. Restamos el jardín:", r"The outer rectangle is \(20+2\cdot1.5=23\) m by \(12+2\cdot1.5=15\) m. Subtract the garden:"),
       D(r"A=23\cdot15-20\cdot12=345-240=\boxed{105\ \text{m}^2}"))])
ck(R(12, 10) * R(15, 10) + pi * R(36, 100) / 2, 2.37, 2); ck(R(42, 10) + R(6, 10) * pi, 6.08, 2); ck(18 * pi - 36, 20.55, 2)
k_ = R(1397, 10) / S(337); ck(k_, 7.61, 2); ck(16 * k_, 121.8, 1); ck(9 * k_, 68.5, 1); ck(R(1397, 10) ** 2, 19516.09); ck(23 * 15 - 240, 105)
s8 += practice([
  ('★', L(r"a) Una «caseta» està formada per un rectangle de 8 cm × 5 cm i un triangle damunt, de 8 cm de base i 3 cm d'altura. Calcula'n l'àrea. b) A un quadrat de 4 cm de costat li afegim un semicercle en dos costats oposats (per fora). Calcula l'àrea total.", r"a) Una «casita» está formada por un rectángulo de 8 cm × 5 cm y un triángulo encima, de 8 cm de base y 3 cm de altura. Calcula su área. b) A un cuadrado de 4 cm de lado le añadimos un semicírculo en dos lados opuestos (por fuera). Calcula el área total.", r"a) A “little house” is an 8 cm × 5 cm rectangle with a triangle on top, with an 8 cm base and a 3 cm height. Find its area. b) A square with 4 cm sides has a semicircle added on two opposite sides (outside). Find the total area.")),
  ('★★', L(r"c) Un rellotge circular de 30 cm de diàmetre té un marc de 2 cm d'amplària. Calcula l'àrea del marc. d) Un camp de futbol fa 100 m × 64 m. Quina distància hi ha d'un córner al córner oposat?", r"c) Un reloj circular de 30 cm de diámetro tiene un marco de 2 cm de ancho. Calcula el área del marco. d) Un campo de fútbol mide 100 m × 64 m. ¿Qué distancia hay de un córner al córner opuesto?", r"c) A round clock 30 cm across has a 2 cm wide frame. Find the area of the frame. d) A football pitch is 100 m × 64 m. How far is it from one corner flag to the opposite one?")),
  ('★★★', L(r"e) Calcula l'àrea compresa entre un hexàgon regular de 6 cm de costat i la circumferència que passa pels seus vèrtexs.", r"e) Calcula el área comprendida entre un hexágono regular de 6 cm de lado y la circunferencia que pasa por sus vértices.", r"e) Find the area between a regular hexagon with 6 cm sides and the circle through its vertices."))],
  P(r"a) \(40+12=52\) cm². b) Dos semicercles fan un cercle de radi 2: \(16+4\pi\approx28{,}57\) cm². c) \(\pi(15^2-13^2)=56\pi\approx175{,}93\) cm². d) \(\sqrt{100^2+64^2}=\sqrt{14\,096}\approx118{,}73\) m. e) \(r=6\), \(a=\sqrt{27}\approx5{,}20\): \(36\pi-\tfrac{36\cdot\sqrt{27}}{2}\approx113{,}10-93{,}53=19{,}57\) cm².",
    r"a) \(40+12=52\) cm². b) Dos semicírculos forman un círculo de radio 2: \(16+4\pi\approx28{,}57\) cm². c) \(\pi(15^2-13^2)=56\pi\approx175{,}93\) cm². d) \(\sqrt{100^2+64^2}=\sqrt{14\,096}\approx118{,}73\) m. e) \(r=6\), \(a=\sqrt{27}\approx5{,}20\): \(36\pi-\tfrac{36\cdot\sqrt{27}}{2}\approx113{,}10-93{,}53=19{,}57\) cm².",
    r"a) \(40+12=52\) cm². b) The two semicircles make a disc of radius 2: \(16+4\pi\approx28.57\) cm². c) \(\pi(15^2-13^2)=56\pi\approx175.93\) cm². d) \(\sqrt{100^2+64^2}=\sqrt{14{,}096}\approx118.73\) m. e) \(r=6\), \(a=\sqrt{27}\approx5.20\): \(36\pi-\tfrac{36\cdot\sqrt{27}}{2}\approx113.10-93.53=19.57\) cm²."))
ck(40 + 12, 52); ck(16 + 4 * pi, 28.57, 2); ck(56 * pi, 175.93, 2); ck(hyp(100, 64), 118.73, 2); ck(36 * pi, 113.10, 2); ck(18 * S(27), 93.53, 2); ck(36 * pi - 18 * S(27), 19.57, 2)
