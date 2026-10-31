# 9.3 Aplicacions del teorema de Pitàgores · 9.4 Perímetres i àrees de triangles i quadrilàters
from comu import *

def T_(P, t, **o): return ('txt', P, t, o)
# ---------- figures tipus (les mateixes que dibuixa el giny w-apl) ----------
F_RECT = [('poly', [(0, 0), (4, 0), (4, 3), (0, 3)], 'gf'), ('poly', [(0, 0), (4, 0), (4, 3)], 'tr'), ('ra', (4, 0), (0, 0), (4, 3)),
          T_((2, 0), 'b', dy=15), T_((4, 1.5), 'h', dx=10, a='start'), T_(off((0, 0), (4, 3), 0.35), 'd', cls='hy')]
F_SQ = [('poly', [(0, 0), (3, 0), (3, 3), (0, 3)], 'gf'), ('poly', [(0, 0), (3, 0), (3, 3)], 'tr'), ('ra', (3, 0), (0, 0), (3, 3)),
        T_((1.5, 0), 'l', dy=15), T_((3, 1.5), 'l', dx=10, a='start'), T_(off((0, 0), (3, 3), 0.35), 'd', cls='hy')]
F_ISO = [('poly', [(-2, 0), (2, 0), (0, 3.5)], 'gf'), ('poly', [(0, 0), (2, 0), (0, 3.5)], 'tr'), ('seg', (0, 0), (0, 3.5), 'd'), ('ra', (0, 0), (2, 0), (0, 3.5)),
         T_((1, 0), 'b/2', dy=15), T_((0, 1.6), 'h', dx=-9), T_(off((2, 0), (0, 3.5), -0.3), 'l')]
h3 = 2 * math.sqrt(3)
F_EQ = [('poly', [(-2, 0), (2, 0), (0, h3)], 'gf'), ('poly', [(0, 0), (2, 0), (0, h3)], 'tr'), ('seg', (0, 0), (0, h3), 'd'), ('ra', (0, 0), (2, 0), (0, h3)),
        T_((1, 0), 'l/2', dy=15), T_((0, 1.6), 'h', dx=-9), T_(off((2, 0), (0, h3), -0.3), 'l'), T_(off((-2, 0), (0, h3), 0.3), 'l')]
F_ROM = [('poly', [(-3, 0), (0, 2), (3, 0), (0, -2)], 'gf'), ('seg', (-3, 0), (3, 0), 'd'), ('seg', (0, -2), (0, 2), 'd'), ('poly', [(0, 0), (3, 0), (0, 2)], 'tr'), ('ra', (0, 0), (3, 0), (0, 2)),
         T_((1.5, 0), 'D/2', dy=15), T_((0, 1), 'd/2', dx=-6, a='end'), T_(off((3, 0), (0, 2), -0.3), 'l')]
F_TRAP = [('poly', [(-3, 0), (3, 0), (1.5, 2.5), (-1.5, 2.5)], 'gf'), ('poly', [(1.5, 0), (3, 0), (1.5, 2.5)], 'tr'), ('seg', (1.5, 0), (1.5, 2.5), 'd'), ('ra', (1.5, 0), (3, 0), (1.5, 2.5)),
          T_((0, 2.5), 'b', dy=-7), T_((0, 0), 'B', dy=15), T_((2.25, 0), '(B−b)/2', dy=15), T_((1.5, 1.1), 'h', dx=-8), T_(off((3, 0), (1.5, 2.5), -0.3), 'c', a='start')]

# =====================================================================
# 9.3 Aplicacions del teorema de Pitàgores
# =====================================================================
s3 = box('prop', L('Triangles rectangles amagats', 'Triángulos rectángulos escondidos', 'Hidden right triangles'),
  P(r"Moltes figures amaguen triangles rectangles que apareixen en traçar una <strong>diagonal</strong>, una <strong>altura</strong> o una <strong>apotema</strong>. Amb el teorema de Pitàgores podem calcular longituds que no sabem mesurar directament.",
    r"Muchas figuras esconden triángulos rectángulos que aparecen al trazar una <strong>diagonal</strong>, una <strong>altura</strong> o una <strong>apotema</strong>. Con el teorema de Pitágoras podemos calcular longitudes que no sabemos medir directamente.",
    r"Many shapes hide right triangles that appear when we draw a <strong>diagonal</strong>, a <strong>height</strong> or an <strong>apothem</strong>. With Pythagoras' theorem we can work out lengths we can't measure directly.")
  + figs(G(F_RECT, W=200, cap=L(r'Diagonal del rectangle: \(d=\sqrt{b^2+h^2}\)', r'Diagonal del rectángulo: \(d=\sqrt{b^2+h^2}\)', r'Diagonal of a rectangle: \(d=\sqrt{b^2+h^2}\)')),
         G(F_SQ, W=160, cap=L(r'Diagonal del quadrat: \(d=\sqrt{l^2+l^2}=l\sqrt2\)', r'Diagonal del cuadrado: \(d=\sqrt{l^2+l^2}=l\sqrt2\)', r'Diagonal of a square: \(d=\sqrt{l^2+l^2}=l\sqrt2\)')),
         G(F_ISO, W=170, cap=L(r'Altura del triangle isòsceles: \(h=\sqrt{l^2-\left(\tfrac b2\right)^2}\)', r'Altura del triángulo isósceles: \(h=\sqrt{l^2-\left(\tfrac b2\right)^2}\)', r'Height of an isosceles triangle: \(h=\sqrt{l^2-\left(\tfrac b2\right)^2}\)')),
         G(F_EQ, W=170, cap=L(r'Altura del triangle equilàter: \(h=\sqrt{l^2-\left(\tfrac l2\right)^2}\)', r'Altura del triángulo equilátero: \(h=\sqrt{l^2-\left(\tfrac l2\right)^2}\)', r'Height of an equilateral triangle: \(h=\sqrt{l^2-\left(\tfrac l2\right)^2}\)')),
         G(F_ROM, W=200, cap=L(r'Costat del rombe: \(l=\sqrt{\left(\tfrac D2\right)^2+\left(\tfrac d2\right)^2}\)', r'Lado del rombo: \(l=\sqrt{\left(\tfrac D2\right)^2+\left(\tfrac d2\right)^2}\)', r'Side of a rhombus: \(l=\sqrt{\left(\tfrac D2\right)^2+\left(\tfrac d2\right)^2}\)')),
         G(F_TRAP, W=210, cap=L(r'Altura del trapezi isòsceles: \(h=\sqrt{c^2-\left(\tfrac{B-b}2\right)^2}\)', r'Altura del trapecio isósceles: \(h=\sqrt{c^2-\left(\tfrac{B-b}2\right)^2}\)', r'Height of an isosceles trapezium: \(h=\sqrt{c^2-\left(\tfrac{B-b}2\right)^2}\)')), three=True)
  + note(r"La clau és sempre la mateixa: localitza el triangle rectangle, decideix quin costat és la hipotenusa i aplica Pitàgores. En el triangle equilàter, \(h=\sqrt{l^2-\tfrac{l^2}{4}}=\tfrac{\sqrt3}{2}\,l\approx0{,}87\,l\).",
         r"La clave es siempre la misma: localiza el triángulo rectángulo, decide qué lado es la hipotenusa y aplica Pitágoras. En el triángulo equilátero, \(h=\sqrt{l^2-\tfrac{l^2}{4}}=\tfrac{\sqrt3}{2}\,l\approx0{,}87\,l\).",
         r"The key is always the same: find the right triangle, decide which side is the hypotenuse and apply Pythagoras. In an equilateral triangle, \(h=\sqrt{l^2-\tfrac{l^2}{4}}=\tfrac{\sqrt3}{2}\,l\approx0.87\,l\).", '🔑')
  + widget('w-apl', '🔍', L('Busca el triangle rectangle', 'Busca el triángulo rectángulo', 'Find the right triangle'),
           [seg([('rect', 'Rectangle'), ('sq', L('Quadrat', 'Cuadrado', 'Square')), ('iso', L('Isòsceles', 'Isósceles', 'Isosceles')), ('eq', L('Equilàter', 'Equilátero', 'Equilateral')), ('rom', L('Rombe', 'Rombo', 'Rhombus')), ('trap', L('Trapezi isòsceles', 'Trapecio isósceles', 'Isosceles trapezium'))]),
            '<div class="wrow">' + rng('p', 1, 20, 0.5, 8) + rng('q', 1, 20, 0.5, 6) + rng('r', 1, 20, 0.5, 10) + '</div>'],
           out='<div class="gout"></div>')
  + drill('apl', 'Entrena: Pitàgores en figures planes', 'Entrena: Pitágoras en figuras planas', 'Train: Pythagoras in plane shapes'))
s3 += box('prop', L('Distància entre dos punts del pla', 'Distancia entre dos puntos del plano', 'Distance between two points'),
  P(r"El segment que uneix \(A(x_1,\,y_1)\) i \(B(x_2,\,y_2)\) és la hipotenusa d'un triangle rectangle de catets \(|x_2-x_1|\) (horitzontal) i \(|y_2-y_1|\) (vertical):",
    r"El segmento que une \(A(x_1,\,y_1)\) y \(B(x_2,\,y_2)\) es la hipotenusa de un triángulo rectángulo de catetos \(|x_2-x_1|\) (horizontal) y \(|y_2-y_1|\) (vertical):",
    r"The segment joining \(A(x_1,\,y_1)\) and \(B(x_2,\,y_2)\) is the hypotenuse of a right triangle with legs \(|x_2-x_1|\) (horizontal) and \(|y_2-y_1|\) (vertical):")
  + D(r"d(A,\,B)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}")
  + D(r"A(1,\,2),\ B(7,\,10):\quad d=\sqrt{6^2+8^2}=\sqrt{100}=10")
  + widget('w-dist', '📏', L('Distància entre dos punts', 'Distancia entre dos puntos', 'Distance between two points'),
           ['<div class="wrow">' + tin('p', 'A =', '(1, 2)', 'm') + tin('q', 'B =', '(7, 10)', 'm') + '</div>',
            quick([('(1, 2)|(7, 10)', '(1, 2), (7, 10)'), ('(-2, 1)|(4, 9)', '(−2, 1), (4, 9)'), ('(-3, -2)|(2, 1)', '(−3, −2), (2, 1)'), ('(0, 0)|(5, -5)', '(0, 0), (5, −5)')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('dist', 'Entrena: distància entre dos punts', 'Entrena: distancia entre dos puntos', 'Train: distance between two points'))
ck(hyp(6, 8), 10)
s3 += levels(
 [prob(L(r"Calcula la diagonal d'un rectangle de 16 cm × 12 cm.", r"Calcula la diagonal de un rectángulo de 16 cm × 12 cm.", r"Find the diagonal of a 16 cm × 12 cm rectangle."),
       D(r"d=\sqrt{16^2+12^2}=\sqrt{256+144}=\sqrt{400}=\boxed{20\ \text{cm}}")),
  prob(L(r"Calcula l'altura d'un triangle isòsceles que té els dos costats iguals de 10 cm i la base de 12 cm.", r"Calcula la altura de un triángulo isósceles que tiene los dos lados iguales de 10 cm y la base de 12 cm.", r"Find the height of an isosceles triangle whose two equal sides are 10 cm and whose base is 12 cm."),
       P(r"L'altura divideix la base en dues meitats de 6 cm. El costat de 10 cm és la hipotenusa:", r"La altura divide la base en dos mitades de 6 cm. El lado de 10 cm es la hipotenusa:", r"The height splits the base into two 6 cm halves. The 10 cm side is the hypotenuse:"),
       D(r"h=\sqrt{10^2-6^2}=\sqrt{64}=\boxed{8\ \text{cm}}"))],
 [prob(L(r"Calcula l'altura d'un triangle equilàter de 6 cm de costat.", r"Calcula la altura de un triángulo equilátero de 6 cm de lado.", r"Find the height of an equilateral triangle with 6 cm sides."),
       D(r"h=\sqrt{6^2-3^2}=\sqrt{27}\approx\boxed{5{,}20\ \text{cm}}")),
  prob(L(r"Les diagonals d'un rombe mesuren 16 cm i 12 cm. Calcula'n el costat i el perímetre.", r"Las diagonales de un rombo miden 16 cm y 12 cm. Calcula su lado y su perímetro.", r"The diagonals of a rhombus are 16 cm and 12 cm. Find its side and its perimeter."),
       P(r"Les diagonals es tallen per la meitat i perpendicularment: formen quatre triangles rectangles de catets 8 i 6.", r"Las diagonales se cortan por la mitad y perpendicularmente: forman cuatro triángulos rectángulos de catetos 8 y 6.", r"The diagonals bisect each other at right angles: they form four right triangles with legs 8 and 6."),
       D(r"l=\sqrt{8^2+6^2}=\sqrt{100}=10\ \text{cm}\qquad P=4\cdot10=\boxed{40\ \text{cm}}"))],
 [prob(L(r"Un trapezi isòsceles té les bases de 20 cm i 8 cm i els costats no paral·lels de 10 cm. Calcula'n l'altura.", r"Un trapecio isósceles tiene las bases de 20 cm y 8 cm y los lados no paralelos de 10 cm. Calcula su altura.", r"An isosceles trapezium has bases of 20 cm and 8 cm and non-parallel sides of 10 cm. Find its height."),
       P(r"Si tracem les altures des dels extrems de la base menor, la base gran queda dividida en \(6+8+6\). Cada triangle rectangle té hipotenusa 10 i un catet 6:", r"Si trazamos las alturas desde los extremos de la base menor, la base mayor queda dividida en \(6+8+6\). Cada triángulo rectángulo tiene hipotenusa 10 y un cateto 6:", r"Drawing the heights from the ends of the shorter base splits the longer base into \(6+8+6\). Each right triangle has hypotenuse 10 and one leg 6:"),
       D(r"\frac{20-8}{2}=6\qquad h=\sqrt{10^2-6^2}=\sqrt{64}=\boxed{8\ \text{cm}}")),
  prob(L(r"Calcula el perímetre del triangle de vèrtexs \(A(-2,\,1)\), \(B(4,\,9)\) i \(C(4,\,1)\) i comprova que és rectangle.", r"Calcula el perímetro del triángulo de vértices \(A(-2,\,1)\), \(B(4,\,9)\) y \(C(4,\,1)\) y comprueba que es rectángulo.", r"Find the perimeter of the triangle with vertices \(A(-2,\,1)\), \(B(4,\,9)\) and \(C(4,\,1)\) and check that it's a right triangle."),
       D(r"AC=4-(-2)=6\qquad BC=9-1=8\qquad AB=\sqrt{6^2+8^2}=10"),
       D(r"P=6+8+10=\boxed{24}\qquad 10^2=6^2+8^2\ \Rightarrow\ \text{%s}" % Lt('rectangle en C', 'rectángulo en C', 'right-angled at C')))])
ck(hyp(16, 12), 20); ck(leg(10, 6), 8); ck(leg(6, 3), 5.20, 2); ck(hyp(8, 6), 10); ck(leg(10, 6), 8); ck(hyp(6, 8), 10)
s3 += practice([
  ('★', L(r"a) Diagonal d'un quadrat de 5 cm de costat. b) Altura d'un triangle isòsceles de costats iguals 13 cm i base 10 cm.", r"a) Diagonal de un cuadrado de 5 cm de lado. b) Altura de un triángulo isósceles de lados iguales 13 cm y base 10 cm.", r"a) Diagonal of a square with 5 cm sides. b) Height of an isosceles triangle with equal sides of 13 cm and a 10 cm base.")),
  ('★★', L(r"c) Costat d'un rombe de diagonals 10 cm i 24 cm. d) Distància entre els punts \((1,\,-3)\) i \((4,\,1)\).", r"c) Lado de un rombo de diagonales 10 cm y 24 cm. d) Distancia entre los puntos \((1,\,-3)\) y \((4,\,1)\).", r"c) Side of a rhombus with diagonals of 10 cm and 24 cm. d) Distance between the points \((1,\,-3)\) and \((4,\,1)\).")),
  ('★★★', L(r"e) Calcula l'altura d'un triangle equilàter de 24 cm de perímetre.", r"e) Calcula la altura de un triángulo equilátero de 24 cm de perímetro.", r"e) Find the height of an equilateral triangle with a 24 cm perimeter."))],
  P(r"a) \(\sqrt{50}=5\sqrt2\approx7{,}07\) cm. b) \(\sqrt{169-25}=12\) cm. c) \(\sqrt{25+144}=13\) cm. d) \(\sqrt{9+16}=5\). e) \(l=8\): \(h=\sqrt{64-16}=\sqrt{48}\approx6{,}93\) cm.",
    r"a) \(\sqrt{50}=5\sqrt2\approx7{,}07\) cm. b) \(\sqrt{169-25}=12\) cm. c) \(\sqrt{25+144}=13\) cm. d) \(\sqrt{9+16}=5\). e) \(l=8\): \(h=\sqrt{64-16}=\sqrt{48}\approx6{,}93\) cm.",
    r"a) \(\sqrt{50}=5\sqrt2\approx7.07\) cm. b) \(\sqrt{169-25}=12\) cm. c) \(\sqrt{25+144}=13\) cm. d) \(\sqrt{9+16}=5\). e) \(l=8\): \(h=\sqrt{64-16}=\sqrt{48}\approx6.93\) cm."))
ck(hyp(5, 5), 7.07, 2); ck(leg(13, 5), 12); ck(hyp(5, 12), 13); ck(hyp(3, 4), 5); ck(leg(8, 4), 6.93, 2)

# =====================================================================
# 9.4 Perímetres i àrees de triangles i quadrilàters
# =====================================================================
def fa(it, cap, W=170): return G(it, W=W, cap=cap)
A_SQ = [('poly', [(0, 0), (3, 0), (3, 3), (0, 3)], 'gf'), T_((1.5, 0), 'l', dy=15), T_((3, 1.5), 'l', dx=9, a='start')]
A_RE = [('poly', [(0, 0), (4.5, 0), (4.5, 2.6), (0, 2.6)], 'gf'), T_((2.25, 0), 'b', dy=15), T_((4.5, 1.3), 'h', dx=9, a='start')]
A_RO = [('poly', [(0, 0), (3.6, 0), (4.8, 2.6), (1.2, 2.6)], 'gf'), ('seg', (1.2, 0), (1.2, 2.6), 'd'), ('ra', (1.2, 0), (2, 0), (1.2, 1)), T_((1.8, 0), 'b', dy=15), T_((1.2, 1.3), 'h', dx=8, a='start')]
A_RB = [('poly', [(-2.4, 0), (0, 1.6), (2.4, 0), (0, -1.6)], 'gf'), ('seg', (-2.4, 0), (2.4, 0), 'd'), ('seg', (0, -1.6), (0, 1.6), 'd'), T_((-1.2, 0), 'D', dy=-6), T_((0, -0.8), 'd', dx=8, a='start')]
A_TP = [('poly', [(0, 0), (4.6, 0), (3.4, 2.4), (1, 2.4)], 'gf'), ('seg', (1, 0), (1, 2.4), 'd'), ('ra', (1, 0), (2, 0), (1, 1)), T_((2.3, 0), 'B', dy=15), T_((2.2, 2.4), 'b', dy=-7), T_((1, 1.2), 'h', dx=8, a='start')]
A_TR = [('poly', [(0, 0), (4.2, 0), (2.9, 2.8)], 'gf'), ('seg', (2.9, 0), (2.9, 2.8), 'd'), ('ra', (2.9, 0), (4, 0), (2.9, 1)), T_((1.45, 0), 'b', dy=15), T_((2.9, 1.3), 'h', dx=-8, a='end')]
s4 = box('def', L('Perímetre i àrea', 'Perímetro y área', 'Perimeter and area'),
  ul(L(r"El <strong>perímetre</strong> d'una figura plana és la longitud del seu contorn: en un polígon, la <strong>suma dels costats</strong>. Es mesura en unitats de longitud (cm, m, km…).", r"El <strong>perímetro</strong> de una figura plana es la longitud de su contorno: en un polígono, la <strong>suma de los lados</strong>. Se mide en unidades de longitud (cm, m, km…).", r"The <strong>perimeter</strong> of a plane shape is the length of its boundary: for a polygon, the <strong>sum of its sides</strong>. It is measured in units of length (cm, m, km…)."),
     L(r"L'<strong>àrea</strong> és la mesura de la superfície que ocupa. Es mesura en <strong>unitats quadrades</strong>: \(1\ \text{cm}^2\) és l'àrea d'un quadrat d'1 cm de costat.", r"El <strong>área</strong> es la medida de la superficie que ocupa. Se mide en <strong>unidades cuadradas</strong>: \(1\ \text{cm}^2\) es el área de un cuadrado de 1 cm de lado.", r"The <strong>area</strong> measures the surface it covers. It is measured in <strong>square units</strong>: \(1\ \text{cm}^2\) is the area of a square with 1 cm sides."))
  + note(r"Cada unitat de superfície és 100 vegades l'anterior: \(1\ \text{m}^2=100\ \text{dm}^2=10\,000\ \text{cm}^2\). Una hectàrea és \(1\ \text{ha}=10\,000\ \text{m}^2\) (un quadrat de 100 m de costat).",
         r"Cada unidad de superficie es 100 veces la anterior: \(1\ \text{m}^2=100\ \text{dm}^2=10\,000\ \text{cm}^2\). Una hectárea es \(1\ \text{ha}=10\,000\ \text{m}^2\) (un cuadrado de 100 m de lado).",
         r"Each unit of area is 100 times the previous one: \(1\ \text{m}^2=100\ \text{dm}^2=10\,000\ \text{cm}^2\). A hectare is \(1\ \text{ha}=10\,000\ \text{m}^2\) (a square with 100 m sides).", '📏'))
s4 += box('prop', L('Fórmules de les àrees', 'Fórmulas de las áreas', 'Area formulas'),
  figs(fa(A_SQ, L(r'Quadrat: \(A=l^2\)', r'Cuadrado: \(A=l^2\)', r'Square: \(A=l^2\)'), 130), fa(A_RE, L(r'Rectangle: \(A=b\cdot h\)', r'Rectángulo: \(A=b\cdot h\)', r'Rectangle: \(A=b\cdot h\)')),
       fa(A_RO, L(r'Romboide: \(A=b\cdot h\)', r'Romboide: \(A=b\cdot h\)', r'Parallelogram: \(A=b\cdot h\)')), fa(A_RB, L(r'Rombe: \(A=\dfrac{D\cdot d}{2}\)', r'Rombo: \(A=\dfrac{D\cdot d}{2}\)', r'Rhombus: \(A=\dfrac{D\cdot d}{2}\)')),
       fa(A_TP, L(r'Trapezi: \(A=\dfrac{(B+b)\cdot h}{2}\)', r'Trapecio: \(A=\dfrac{(B+b)\cdot h}{2}\)', r'Trapezium: \(A=\dfrac{(B+b)\cdot h}{2}\)')), fa(A_TR, L(r'Triangle: \(A=\dfrac{b\cdot h}{2}\)', r'Triángulo: \(A=\dfrac{b\cdot h}{2}\)', r'Triangle: \(A=\dfrac{b\cdot h}{2}\)')), three=True)
  + ul(L(r"El <strong>romboide</strong> es transforma en un rectangle de la mateixa base i altura si retallem un triangle d'un costat i el posem a l'altre.", r"El <strong>romboide</strong> se transforma en un rectángulo de la misma base y altura si recortamos un triángulo de un lado y lo ponemos en el otro.", r"A <strong>parallelogram</strong> becomes a rectangle with the same base and height if we cut a triangle off one side and stick it on the other."),
       L(r"Un <strong>triangle</strong> és la meitat d'un romboide de la mateixa base i altura.", r"Un <strong>triángulo</strong> es la mitad de un romboide de la misma base y altura.", r"A <strong>triangle</strong> is half a parallelogram with the same base and height."),
       L(r"El <strong>rombe</strong> és la meitat del rectangle que té per costats les dues diagonals.", r"El <strong>rombo</strong> es la mitad del rectángulo que tiene por lados las dos diagonales.", r"A <strong>rhombus</strong> is half the rectangle whose sides are its two diagonals."),
       L(r"Dos <strong>trapezis</strong> iguals, un d'ells capgirat, formen un romboide de base \(B+b\) i altura \(h\).", r"Dos <strong>trapecios</strong> iguales, uno de ellos girado, forman un romboide de base \(B+b\) y altura \(h\).", r"Two equal <strong>trapeziums</strong>, one turned upside down, form a parallelogram with base \(B+b\) and height \(h\)."))
  + note(r"L'<strong>altura</strong> sempre és <strong>perpendicular</strong> a la base. Si no la coneixem, sovint la podem calcular amb Pitàgores (apartat 9.3).", r"La <strong>altura</strong> siempre es <strong>perpendicular</strong> a la base. Si no la conocemos, a menudo la podemos calcular con Pitágoras (apartado 9.3).", r"The <strong>height</strong> is always <strong>perpendicular</strong> to the base. If we don't know it, we can often find it with Pythagoras (section 9.3).", '⚠️')
  + widget('w-area', '🟧', L('Àrea i perímetre de polígons', 'Área y perímetro de polígonos', 'Area and perimeter of polygons'),
           [seg([('sq', L('Quadrat', 'Cuadrado', 'Square')), ('re', L('Rectangle', 'Rectángulo', 'Rectangle')), ('ro', 'Romboide'), ('rb', L('Rombe', 'Rombo', 'Rhombus')), ('tp', L('Trapezi isòsceles', 'Trapecio isósceles', 'Isosceles trapezium')), ('tr', L('Triangle isòsceles', 'Triángulo isósceles', 'Isosceles triangle'))]),
            '<div class="wrow">' + rng('p', 1, 20, 0.5, 10) + rng('q', 1, 20, 0.5, 6) + rng('r', 1, 20, 0.5, 4) + '</div>'],
           out='<div class="gout"></div>')
  + drill('area', 'Entrena: calcula àrees', 'Entrena: calcula áreas', 'Train: work out areas'))
s4 += levels(
 [prob(L(r"Calcula l'àrea i el perímetre d'un rectangle de 12 m × 7,5 m.", r"Calcula el área y el perímetro de un rectángulo de 12 m × 7,5 m.", r"Find the area and the perimeter of a 12 m × 7.5 m rectangle."),
       D(r"A=12\cdot7{,}5=\boxed{90\ \text{m}^2}\qquad P=2\cdot12+2\cdot7{,}5=\boxed{39\ \text{m}}")),
  prob(L(r"Calcula l'àrea d'un triangle de 9 cm de base i 6 cm d'altura.", r"Calcula el área de un triángulo de 9 cm de base y 6 cm de altura.", r"Find the area of a triangle with a 9 cm base and a 6 cm height."),
       D(r"A=\frac{9\cdot6}{2}=\boxed{27\ \text{cm}^2}"))],
 [prob(L(r"Un trapezi rectangle té les bases de 14 cm i 8 cm i l'altura de 8 cm. Calcula'n l'àrea i el perímetre.", r"Un trapecio rectángulo tiene las bases de 14 cm y 8 cm y la altura de 8 cm. Calcula su área y su perímetro.", r"A right trapezium has bases of 14 cm and 8 cm and a height of 8 cm. Find its area and perimeter."),
       figs(G([('poly', [(0, 0), (14, 0), (8, 8), (0, 8)], 'gf'), ('poly', [(8, 0), (14, 0), (8, 8)], 'tr'), ('seg', (8, 0), (8, 8), 'd'), ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (8, 0), (14, 0), (8, 8)),
                T_((7, 0), '14', dy=15), T_((4, 8), '8', dy=-7), T_((0, 4), '8', dx=-8, a='end'), T_((11, 0), '6', dy=-6), T_(off((14, 0), (8, 8), -0.9), 'c', a='start')], W=200)),
       D(r"A=\frac{(14+8)\cdot8}{2}=\boxed{88\ \text{cm}^2}"),
       P(r"Per al perímetre ens falta el costat oblic \(c\): és la hipotenusa d'un triangle de catets \(14-8=6\) i 8.", r"Para el perímetro nos falta el lado oblicuo \(c\): es la hipotenusa de un triángulo de catetos \(14-8=6\) y 8.", r"For the perimeter we need the slanted side \(c\): it's the hypotenuse of a triangle with legs \(14-8=6\) and 8."),
       D(r"c=\sqrt{6^2+8^2}=10\qquad P=14+8+8+10=\boxed{40\ \text{cm}}")),
  prob(L(r"Un rombe té 52 cm de perímetre i una diagonal de 24 cm. Calcula'n l'àrea.", r"Un rombo tiene 52 cm de perímetro y una diagonal de 24 cm. Calcula su área.", r"A rhombus has a 52 cm perimeter and a 24 cm diagonal. Find its area."),
       D(r"l=\frac{52}{4}=13\qquad \frac d2=\sqrt{13^2-12^2}=\sqrt{25}=5\ \Rightarrow\ d=10"),
       D(r"A=\frac{24\cdot10}{2}=\boxed{120\ \text{cm}^2}"))],
 [prob(L(r"Calcula l'àrea d'un triangle equilàter de 10 cm de costat.", r"Calcula el área de un triángulo equilátero de 10 cm de lado.", r"Find the area of an equilateral triangle with 10 cm sides."),
       D(r"h=\sqrt{10^2-5^2}=\sqrt{75}\approx8{,}66\ \text{cm}\qquad A=\frac{10\cdot\sqrt{75}}{2}\approx\boxed{43{,}30\ \text{cm}^2}")),
  prob(L(r"Volem enrajolar el terra d'una habitació de 5 m × 4,2 m amb rajoles quadrades de 30 cm de costat. Quantes rajoles caldran, com a mínim?", r"Queremos embaldosar el suelo de una habitación de 5 m × 4,2 m con baldosas cuadradas de 30 cm de lado. ¿Cuántas baldosas harán falta, como mínimo?", r"We want to tile the floor of a 5 m × 4.2 m room with square tiles with 30 cm sides. How many tiles will we need, at least?"),
       P(r"Treballem en les mateixes unitats (cm):", r"Trabajamos en las mismas unidades (cm):", r"Work in the same units (cm):"),
       D(r"A_{\text{%s}}=500\cdot420=210\,000\ \text{cm}^2\qquad A_{\text{%s}}=30^2=900\ \text{cm}^2" % (Lt('terra', 'suelo', 'floor'), Lt('rajola', 'baldosa', 'tile'))),
       D(r"\frac{210\,000}{900}=233{,}3\ \Rightarrow\ \boxed{234\ \text{%s}}" % Lt('rajoles', 'baldosas', 'tiles')))])
ck(12 * R(15, 2), 90); ck(9 * 6 / 2, 27); ck(R(14 + 8, 2) * 8, 88); ck(hyp(6, 8), 10); ck(leg(13, 12), 5); ck(R(24 * 10, 2), 120)
ck(leg(10, 5), 8.66, 2); ck(10 * leg(10, 5) / 2, 43.30, 2); ck(R(210000, 900), 233.3, 1); assert math.ceil(210000 / 900) == 234
s4 += practice([
  ('★', L(r"a) Àrea i perímetre d'un quadrat de 7,5 cm de costat. b) Àrea d'un romboide de 12 cm de base i 5 cm d'altura.", r"a) Área y perímetro de un cuadrado de 7,5 cm de lado. b) Área de un romboide de 12 cm de base y 5 cm de altura.", r"a) Area and perimeter of a square with 7.5 cm sides. b) Area of a parallelogram with a 12 cm base and a 5 cm height.")),
  ('★★', L(r"c) Àrea i perímetre d'un trapezi isòsceles de bases 16 cm i 10 cm i altura 4 cm. d) Un rectangle de 96 cm² té 12 cm de base. Quant mesura la diagonal?", r"c) Área y perímetro de un trapecio isósceles de bases 16 cm y 10 cm y altura 4 cm. d) Un rectángulo de 96 cm² tiene 12 cm de base. ¿Cuánto mide la diagonal?", r"c) Area and perimeter of an isosceles trapezium with bases of 16 cm and 10 cm and a 4 cm height. d) A 96 cm² rectangle has a 12 cm base. How long is its diagonal?")),
  ('★★★', L(r"e) Un triangle isòsceles té 36 cm de perímetre i 10 cm de base. Calcula'n l'àrea.", r"e) Un triángulo isósceles tiene 36 cm de perímetro y 10 cm de base. Calcula su área.", r"e) An isosceles triangle has a 36 cm perimeter and a 10 cm base. Find its area."))],
  P(r"a) \(A=56{,}25\) cm², \(P=30\) cm. b) \(60\) cm². c) \(A=\tfrac{(16+10)\cdot4}{2}=52\) cm²; costat \(\sqrt{3^2+4^2}=5\), \(P=36\) cm. d) \(h=8\), \(d=\sqrt{208}\approx14{,}42\) cm. e) Costats iguals de 13 cm, \(h=\sqrt{169-25}=12\), \(A=60\) cm².",
    r"a) \(A=56{,}25\) cm², \(P=30\) cm. b) \(60\) cm². c) \(A=\tfrac{(16+10)\cdot4}{2}=52\) cm²; lado \(\sqrt{3^2+4^2}=5\), \(P=36\) cm. d) \(h=8\), \(d=\sqrt{208}\approx14{,}42\) cm. e) Lados iguales de 13 cm, \(h=\sqrt{169-25}=12\), \(A=60\) cm².",
    r"a) \(A=56.25\) cm², \(P=30\) cm. b) \(60\) cm². c) \(A=\tfrac{(16+10)\cdot4}{2}=52\) cm²; side \(\sqrt{3^2+4^2}=5\), \(P=36\) cm. d) \(h=8\), \(d=\sqrt{208}\approx14.42\) cm. e) Equal sides of 13 cm, \(h=\sqrt{169-25}=12\), \(A=60\) cm²."))
ck(R(15, 2) ** 2, 56.25); ck(26 * 4 / 2, 52); ck(hyp(3, 4), 5); ck(16 + 10 + 2 * 5, 36); ck(hyp(12, 8), 14.42, 2); ck(leg(13, 5), 12); ck(10 * 12 / 2, 60)
