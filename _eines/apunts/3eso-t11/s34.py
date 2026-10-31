# 11.3 Piràmides i troncs de piràmide · 11.4 Cilindre i con
from comu import *
from fig11 import *

def solid(it, W=200, cap=None, maxh=210, pad=18): return G(it, W=W, cap=cap, maxh=maxh, pad=pad)

# =====================================================================
# 11.3 Piràmides i troncs de piràmide
# =====================================================================
FY, _ = f_pyramid(4, 3, 3.6)
s3 = box('def', L('Piràmides', 'Pirámides', 'Pyramids'),
  P(r"Una <strong>piràmide</strong> és un poliedre que té per <strong>base</strong> un polígon qualsevol i per cares laterals triangles que es troben en un punt, el <strong>vèrtex</strong> (o cúspide). L'<strong>altura</strong> \(h\) és la distància del vèrtex a la base.",
    r"Una <strong>pirámide</strong> es un poliedro que tiene por <strong>base</strong> un polígono cualquiera y por caras laterales triángulos que se encuentran en un punto, el <strong>vértice</strong> (o cúspide). La <strong>altura</strong> \(h\) es la distancia del vértice a la base.",
    r"A <strong>pyramid</strong> is a polyhedron whose <strong>base</strong> is any polygon and whose lateral faces are triangles meeting at one point, the <strong>apex</strong>. The <strong>height</strong> \(h\) is the distance from the apex to the base.")
  + P(r"Una piràmide és <strong>regular</strong> si la base és un polígon regular i el peu de l'altura és el centre de la base. Aleshores totes les cares laterals són triangles isòsceles iguals, i l'altura de cadascun és l'<strong>apotema de la piràmide</strong>, \(a_p\). No la confongues amb l'<strong>apotema de la base</strong>, \(a_b\).",
      r"Una pirámide es <strong>regular</strong> si la base es un polígono regular y el pie de la altura es el centro de la base. Entonces todas las caras laterales son triángulos isósceles iguales, y la altura de cada uno es la <strong>apotema de la pirámide</strong>, \(a_p\). No la confundas con la <strong>apotema de la base</strong>, \(a_b\).",
      r"A pyramid is <strong>regular</strong> if its base is a regular polygon and the foot of the height is the centre of the base. Then all lateral faces are equal isosceles triangles, and the height of each is the <strong>slant height</strong> \(a_p\) (the pyramid's apothem). Don't confuse it with the <strong>base apothem</strong> \(a_b\).")
  + figs(solid(FY, W=260, maxh=250))
  + P(r"L'altura, l'apotema de la base i l'apotema de la piràmide formen un <strong>triangle rectangle</strong> (la hipotenusa és \(a_p\)):",
      r"La altura, la apotema de la base y la apotema de la pirámide forman un <strong>triángulo rectángulo</strong> (la hipotenusa es \(a_p\)):",
      r"The height, the base apothem and the slant height form a <strong>right triangle</strong> (with hypotenuse \(a_p\)):")
  + D(r"a_p^2=h^2+a_b^2"))
s3 += box('prop', L("Àrea d'una piràmide regular", 'Área de una pirámide regular', 'Surface area of a regular pyramid'),
  P(r"El desenvolupament és la base i \(n\) triangles iguals de base \(l\) i altura \(a_p\):", r"El desarrollo es la base y \(n\) triángulos iguales de base \(l\) y altura \(a_p\):", r"The net is the base and \(n\) equal triangles with base \(l\) and height \(a_p\):")
  + figs(G(net_pyramid(4, 3, 3.9), W=210, pad=10, cap=L('Desenvolupament d’una piràmide quadrangular', 'Desarrollo de una pirámide cuadrangular', 'Net of a square pyramid')))
  + D(r"A_L=\frac{P_{\text{base}}\cdot a_p}{2}\qquad\qquad A_T=A_L+A_{\text{base}}")
  + P(r"Exemple: piràmide quadrangular regular de \(l=6\) cm i \(h=4\) cm. L'apotema de la base és \(a_b=3\), i \(a_p=\sqrt{4^2+3^2}=5\) cm:",
      r"Ejemplo: pirámide cuadrangular regular de \(l=6\) cm y \(h=4\) cm. La apotema de la base es \(a_b=3\), y \(a_p=\sqrt{4^2+3^2}=5\) cm:",
      r"Example: a regular square pyramid with \(l=6\) cm and \(h=4\) cm. The base apothem is \(a_b=3\), and \(a_p=\sqrt{4^2+3^2}=5\) cm:")
  + D(r"A_L=\frac{24\cdot5}{2}=60\ \text{cm}^2\qquad A_T=60+36=96\ \text{cm}^2")
  + widget('w-pyr', '🔺', L('Piràmides regulars: apotema i àrea', 'Pirámides regulares: apotema y área', 'Regular pyramids: slant height and area'),
           ['<div class="wrow">' + rng('n', 3, 8, 1, 4, 'n') + rng('l', 1, 10, 0.5, 6, 'l') + rng('h', 1, 15, 0.5, 4, 'h') + '</div>'],
           out='<div class="gout"></div><div class="hsteps"></div>')
  + drill('piramide', "Entrena: àrea d'una piràmide", 'Entrena: área de una pirámide', 'Train: surface area of a pyramid'))
ck(hyp(4, 3), 5); ck(24 * 5 / 2, 60)
FT, PT = polyhedron(frustum(4, 3.4, 1.8, 2.2))
s3 += box('def', L('Tronc de piràmide', 'Tronco de pirámide', 'Frustum of a pyramid'),
  P(r"Si tallem una piràmide amb un pla paral·lel a la base, la part de baix és un <strong>tronc de piràmide</strong>. Té dues bases semblants i les cares laterals són trapezis. Si la piràmide és regular, els trapezis són isòsceles i la seua altura és l'apotema del tronc, \(a_p\):",
    r"Si cortamos una pirámide con un plano paralelo a la base, la parte de abajo es un <strong>tronco de pirámide</strong>. Tiene dos bases semejantes y las caras laterales son trapecios. Si la pirámide es regular, los trapecios son isósceles y su altura es la apotema del tronco, \(a_p\):",
    r"Cutting a pyramid with a plane parallel to its base leaves a <strong>frustum</strong> at the bottom. It has two similar bases and its lateral faces are trapezia. If the pyramid is regular, the trapezia are isosceles and their height is the frustum's slant height \(a_p\):")
  + figs(solid(FT, W=200))
  + D(r"A_L=\frac{(P+P')\cdot a_p}{2}\qquad\qquad A_T=A_L+A_{\text{%s}}+A_{\text{%s}}" % (Lt('base gran', 'base mayor', 'big base'), Lt('base menuda', 'base menor', 'small base'))))
s3 += levels(
 [prob(L(r"Una piràmide hexagonal regular té 8 cm d'aresta de la base i 12 cm d'apotema. Calcula'n l'àrea lateral.", r"Una pirámide hexagonal regular tiene 8 cm de arista de la base y 12 cm de apotema. Calcula su área lateral.", r"A regular hexagonal pyramid has 8 cm base edges and a 12 cm slant height. Find its lateral area."),
       D(r"A_L=\frac{48\cdot12}{2}=\boxed{288\ \text{cm}^2}"))],
 [prob(L(r"Una piràmide quadrangular regular té 10 cm d'aresta de la base i 12 cm d'altura. Calcula l'apotema i l'àrea total.", r"Una pirámide cuadrangular regular tiene 10 cm de arista de la base y 12 cm de altura. Calcula la apotema y el área total.", r"A regular square pyramid has 10 cm base edges and is 12 cm tall. Find its slant height and total area."),
       D(r"a_b=5\qquad a_p=\sqrt{12^2+5^2}=\sqrt{169}=\boxed{13\ \text{cm}}"),
       D(r"A_T=\frac{40\cdot13}{2}+10^2=260+100=\boxed{360\ \text{cm}^2}"))],
 [prob(L(r"Un tronc de piràmide quadrangular regular té les arestes de les bases de 10 cm i 4 cm i l'altura de 4 cm. Calcula'n l'àrea total.", r"Un tronco de pirámide cuadrangular regular tiene las aristas de las bases de 10 cm y 4 cm y la altura de 4 cm. Calcula su área total.", r"A regular square frustum has base edges of 10 cm and 4 cm and a height of 4 cm. Find its total area."),
       P(r"Tallant pel mig d'una cara lateral veiem un trapezi; l'apotema del tronc és la hipotenusa d'un triangle rectangle de catets \(h=4\) i \(\frac{10-4}{2}=3\):", r"Cortando por el medio de una cara lateral vemos un trapecio; la apotema del tronco es la hipotenusa de un triángulo rectángulo de catetos \(h=4\) y \(\frac{10-4}{2}=3\):", r"Cutting through the middle of a lateral face shows a trapezium; the slant height is the hypotenuse of a right triangle with legs \(h=4\) and \(\frac{10-4}{2}=3\):"),
       D(r"a_p=\sqrt{4^2+3^2}=5\ \text{cm}"),
       D(r"A_T=\frac{(40+16)\cdot5}{2}+10^2+4^2=140+100+16=\boxed{256\ \text{cm}^2}"))])
ck(48 * 12 / 2, 288); ck(hyp(12, 5), 13); ck(40 * 13 / 2 + 100, 360); ck(hyp(4, 3), 5); ck(56 * 5 / 2 + 116, 256)
s3 += practice([
  ('★', L(r"a) Una piràmide triangular regular té 6 cm d'aresta de la base i 10 cm d'apotema. Calcula'n l'àrea lateral.", r"a) Una pirámide triangular regular tiene 6 cm de arista de la base y 10 cm de apotema. Calcula su área lateral.", r"a) A regular triangular pyramid has 6 cm base edges and a 10 cm slant height. Find its lateral area.")),
  ('★★', L(r"b) Una piràmide quadrangular regular té 16 cm d'aresta de la base i 6 cm d'altura. Calcula l'apotema i l'àrea total. c) Quant fa l'aresta lateral?", r"b) Una pirámide cuadrangular regular tiene 16 cm de arista de la base y 6 cm de altura. Calcula la apotema y el área total. c) ¿Cuánto mide la arista lateral?", r"b) A regular square pyramid has 16 cm base edges and is 6 cm tall. Find its slant height and total area. c) How long is a lateral edge?")),
  ('★★★', L(r"d) Una piràmide hexagonal regular té 6 cm d'aresta de la base i 10 cm d'altura. Calcula l'apotema de la base, l'apotema de la piràmide i l'àrea total.", r"d) Una pirámide hexagonal regular tiene 6 cm de arista de la base y 10 cm de altura. Calcula la apotema de la base, la apotema de la pirámide y el área total.", r"d) A regular hexagonal pyramid has 6 cm base edges and is 10 cm tall. Find the base apothem, the slant height and the total area."))],
  P(r"a) \(\frac{18\cdot10}{2}=90\) cm². b) \(a_p=\sqrt{36+64}=10\) cm; \(A_T=\frac{64\cdot10}{2}+256=576\) cm². c) Aresta: hipotenusa d'apotema i mig costat, \(\sqrt{100+64}\approx12{,}81\) cm. d) \(a_b=\sqrt{27}\approx5{,}20\) cm; \(a_p=\sqrt{100+27}\approx11{,}27\) cm; \(A_T\approx202{,}85+93{,}53=296{,}38\) cm².",
    r"a) \(\frac{18\cdot10}{2}=90\) cm². b) \(a_p=\sqrt{36+64}=10\) cm; \(A_T=\frac{64\cdot10}{2}+256=576\) cm². c) Arista: hipotenusa de apotema y medio lado, \(\sqrt{100+64}\approx12{,}81\) cm. d) \(a_b=\sqrt{27}\approx5{,}20\) cm; \(a_p=\sqrt{100+27}\approx11{,}27\) cm; \(A_T\approx202{,}85+93{,}53=296{,}38\) cm².",
    r"a) \(\frac{18\cdot10}{2}=90\) cm². b) \(a_p=\sqrt{36+64}=10\) cm; \(A_T=\frac{64\cdot10}{2}+256=576\) cm². c) Lateral edge: hypotenuse of slant height and half side, \(\sqrt{100+64}\approx12.81\) cm. d) \(a_b=\sqrt{27}\approx5.20\) cm; \(a_p=\sqrt{100+27}\approx11.27\) cm; \(A_T\approx202.85+93.53=296.38\) cm²."))
ck(90, 90); ck(hyp(6, 8), 10); ck(64 * 10 / 2 + 256, 576); ck(S(164), 12.81, 2); ck(S(127), 11.27, 2); ck(36 * S(127) / 2, 202.85, 2); ck(36 * S(27) / 2, 93.53, 2); ck(18 * S(127) + 18 * S(27), 296.38, 2)

# =====================================================================
# 11.4 Cilindre i con
# =====================================================================
FC, _ = f_cylinder(1.6, 3.2)
FK, _ = f_cone(1.8, 3.4)
s4 = box('def', L('Cossos de revolució: cilindre i con', 'Cuerpos de revolución: cilindro y cono', 'Solids of revolution: cylinder and cone'),
  P(r"Un <strong>cos de revolució</strong> s'obté fent girar una figura plana al voltant d'una recta, l'<strong>eix</strong>. Si gira un rectangle al voltant d'un costat, obtenim un <strong>cilindre</strong>; si gira un triangle rectangle al voltant d'un catet, un <strong>con</strong>; i si gira un semicercle al voltant del diàmetre, una <strong>esfera</strong>.",
    r"Un <strong>cuerpo de revolución</strong> se obtiene haciendo girar una figura plana alrededor de una recta, el <strong>eje</strong>. Si gira un rectángulo alrededor de un lado, obtenemos un <strong>cilindro</strong>; si gira un triángulo rectángulo alrededor de un cateto, un <strong>cono</strong>; y si gira un semicírculo alrededor del diámetro, una <strong>esfera</strong>.",
    r"A <strong>solid of revolution</strong> is made by spinning a flat shape around a line, the <strong>axis</strong>. Spinning a rectangle around one side gives a <strong>cylinder</strong>; a right triangle around a leg, a <strong>cone</strong>; and a semicircle around its diameter, a <strong>sphere</strong>.")
  + figs(solid(FC, W=150, cap=L('Cilindre', 'Cilindro', 'Cylinder')), solid(FK, W=150, cap=L('Con', 'Cono', 'Cone')))
  + P(r"En el cilindre, \(r\) és el radi de les bases i \(h\) l'altura. En el con, el segment que va del vèrtex a la vora de la base és la <strong>generatriu</strong> \(g\). L'altura, el radi i la generatriu formen un triangle rectangle:",
      r"En el cilindro, \(r\) es el radio de las bases y \(h\) la altura. En el cono, el segmento que va del vértice al borde de la base es la <strong>generatriz</strong> \(g\). La altura, el radio y la generatriz forman un triángulo rectángulo:",
      r"In a cylinder, \(r\) is the radius of the bases and \(h\) the height. In a cone, the segment from the apex to the edge of the base is the <strong>slant height</strong> \(g\). Height, radius and slant height form a right triangle:")
  + D(r"g^2=h^2+r^2"))
s4 += box('prop', L("Àrees del cilindre i del con", 'Áreas del cilindro y del cono', 'Surface areas of cylinders and cones'),
  P(r"El desenvolupament del <strong>cilindre</strong> és un rectangle (de base la longitud de la circumferència, \(2\pi r\), i d'altura \(h\)) i dos cercles. El del <strong>con</strong> és un sector circular de radi \(g\), amb un arc de longitud \(2\pi r\), i un cercle:",
    r"El desarrollo del <strong>cilindro</strong> es un rectángulo (de base la longitud de la circunferencia, \(2\pi r\), y de altura \(h\)) y dos círculos. El del <strong>cono</strong> es un sector circular de radio \(g\), con un arco de longitud \(2\pi r\), y un círculo:",
    r"The net of a <strong>cylinder</strong> is a rectangle (\(2\pi r\) wide, the circumference, and \(h\) tall) and two discs. The net of a <strong>cone</strong> is a sector of radius \(g\) whose arc is \(2\pi r\) long, and a disc:")
  + figs(G(net_cylinder(1, 2.6), W=200, pad=10, cap=L('Cilindre', 'Cilindro', 'Cylinder')), G(net_cone(1.2, 3), W=170, pad=10, cap=L('Con', 'Cono', 'Cone')))
  + tbl(['', L('Àrea lateral', 'Área lateral', 'Lateral area'), L('Àrea total', 'Área total', 'Total area')],
        [[L('<strong>Cilindre</strong>', '<strong>Cilindro</strong>', '<strong>Cylinder</strong>'), r'\(A_L=2\pi r h\)', r'\(A_T=2\pi r h+2\pi r^2\)'],
         [L('<strong>Con</strong>', '<strong>Cono</strong>', '<strong>Cone</strong>'), r'\(A_L=\pi r g\)', r'\(A_T=\pi r g+\pi r^2\)']])
  + P(r"Exemple: un con de \(r=3\) cm i \(h=4\) cm té \(g=\sqrt{16+9}=5\) cm, \(A_L=\pi\cdot3\cdot5=15\pi\approx47{,}12\) cm² i \(A_T=15\pi+9\pi=24\pi\approx75{,}40\) cm².",
      r"Ejemplo: un cono de \(r=3\) cm y \(h=4\) cm tiene \(g=\sqrt{16+9}=5\) cm, \(A_L=\pi\cdot3\cdot5=15\pi\approx47{,}12\) cm² y \(A_T=15\pi+9\pi=24\pi\approx75{,}40\) cm².",
      r"Example: a cone with \(r=3\) cm and \(h=4\) cm has \(g=\sqrt{16+9}=5\) cm, \(A_L=\pi\cdot3\cdot5=15\pi\approx47.12\) cm² and \(A_T=15\pi+9\pi=24\pi\approx75.40\) cm².")
  + widget('w-rev', '🥫', L('Cilindre i con: desenvolupament i àrea', 'Cilindro y cono: desarrollo y área', 'Cylinder and cone: net and area'),
           [seg([('cil', L('Cilindre', 'Cilindro', 'Cylinder')), ('con', L('Con', 'Cono', 'Cone'))]),
            '<div class="wrow">' + rng('r', 0.5, 10, 0.5, 3, 'r') + rng('h', 0.5, 20, 0.5, 4, 'h') + '</div>'],
           out='<div class="gout"></div><div class="hsteps"></div>')
  + drill('cilindre', "Entrena: àrea d'un cilindre", 'Entrena: área de un cilindro', 'Train: surface area of a cylinder')
  + drill('con', "Entrena: àrea d'un con", 'Entrena: área de un cono', 'Train: surface area of a cone'))
ck(15 * pi, 47.12, 2); ck(24 * pi, 75.40, 2)
s4 += levels(
 [prob(L(r"Calcula l'àrea total d'un cilindre de 5 cm de radi i 12 cm d'altura.", r"Calcula el área total de un cilindro de 5 cm de radio y 12 cm de altura.", r"Find the total surface area of a cylinder with a 5 cm radius and 12 cm height."),
       D(r"A_T=2\pi\cdot5\cdot12+2\pi\cdot5^2=120\pi+50\pi=170\pi\approx\boxed{534{,}07\ \text{cm}^2}"))],
 [prob(L(r"Un con té 8 cm de diàmetre i 10 cm d'altura. Calcula la generatriu i l'àrea total.", r"Un cono tiene 8 cm de diámetro y 10 cm de altura. Calcula la generatriz y el área total.", r"A cone is 8 cm across and 10 cm tall. Find its slant height and total area."),
       D(r"r=4\qquad g=\sqrt{10^2+4^2}=\sqrt{116}\approx\boxed{10{,}77\ \text{cm}}"),
       D(r"A_T=\pi\cdot4\cdot\sqrt{116}+\pi\cdot4^2\approx135{,}34+50{,}27=\boxed{185{,}61\ \text{cm}^2}"))],
 [prob(L(r"Una llanda de tomaca té 7,4 cm de diàmetre i 11 cm d'altura. Quanta xapa cal per a fer-la (sense comptar les soldadures)? I quant paper per a l'etiqueta, que cobreix tota la superfície lateral?", r"Una lata de tomate tiene 7,4 cm de diámetro y 11 cm de altura. ¿Cuánta chapa hace falta para hacerla (sin contar las soldaduras)? ¿Y cuánto papel para la etiqueta, que cubre toda la superficie lateral?", r"A tin of tomatoes is 7.4 cm across and 11 cm tall. How much metal is needed to make it (ignoring joins)? And how much paper for the label, which covers the whole side?"),
       D(r"A_L=2\pi\cdot3{,}7\cdot11=81{,}4\pi\approx\boxed{255{,}73\ \text{cm}^2}\ (\text{%s})" % Lt('etiqueta', 'etiqueta', 'label')),
       D(r"A_T=81{,}4\pi+2\pi\cdot3{,}7^2=81{,}4\pi+27{,}38\pi=108{,}78\pi\approx\boxed{341{,}74\ \text{cm}^2}"))])
ck(170 * pi, 534.07, 2); ck(S(116), 10.77, 2); ck(4 * pi * S(116), 135.34, 2); ck(16 * pi, 50.27, 2); ck(4 * pi * S(116) + 16 * pi, 185.61, 2)
ck(R(814, 10) * pi, 255.73, 2); ck(2 * R(37, 10) ** 2, 27.38); ck(R(10878, 100) * pi, 341.74, 2)
s4 += practice([
  ('★', L(r"a) Calcula l'àrea lateral i total d'un cilindre de 2 cm de radi i 6 cm d'altura.", r"a) Calcula el área lateral y total de un cilindro de 2 cm de radio y 6 cm de altura.", r"a) Find the lateral and total area of a cylinder with a 2 cm radius and 6 cm height.")),
  ('★★', L(r"b) Un con té 6 cm de radi i 8 cm d'altura. Calcula la generatriu i l'àrea total. c) Un con té 13 cm de generatriu i 5 cm de radi. Quina altura té?", r"b) Un cono tiene 6 cm de radio y 8 cm de altura. Calcula la generatriz y el área total. c) Un cono tiene 13 cm de generatriz y 5 cm de radio. ¿Qué altura tiene?", r"b) A cone has a 6 cm radius and is 8 cm tall. Find its slant height and total area. c) A cone has a 13 cm slant height and a 5 cm radius. How tall is it?")),
  ('★★★', L(r"d) Un cilindre té una àrea lateral de \(60\pi\) cm² i una altura de 6 cm. Quin radi té? Quina és l'àrea total?", r"d) Un cilindro tiene un área lateral de \(60\pi\) cm² y una altura de 6 cm. ¿Qué radio tiene? ¿Cuál es el área total?", r"d) A cylinder has a lateral area of \(60\pi\) cm² and a height of 6 cm. What is its radius? What is its total area?"))],
  P(r"a) \(A_L=24\pi\approx75{,}40\) cm²; \(A_T=32\pi\approx100{,}53\) cm². b) \(g=10\) cm; \(A_T=60\pi+36\pi=96\pi\approx301{,}59\) cm². c) \(h=\sqrt{169-25}=12\) cm. d) \(12\pi r=60\pi\Rightarrow r=5\) cm; \(A_T=60\pi+50\pi=110\pi\approx345{,}58\) cm².",
    r"a) \(A_L=24\pi\approx75{,}40\) cm²; \(A_T=32\pi\approx100{,}53\) cm². b) \(g=10\) cm; \(A_T=60\pi+36\pi=96\pi\approx301{,}59\) cm². c) \(h=\sqrt{169-25}=12\) cm. d) \(12\pi r=60\pi\Rightarrow r=5\) cm; \(A_T=60\pi+50\pi=110\pi\approx345{,}58\) cm².",
    r"a) \(A_L=24\pi\approx75.40\) cm²; \(A_T=32\pi\approx100.53\) cm². b) \(g=10\) cm; \(A_T=60\pi+36\pi=96\pi\approx301.59\) cm². c) \(h=\sqrt{169-25}=12\) cm. d) \(12\pi r=60\pi\Rightarrow r=5\) cm; \(A_T=60\pi+50\pi=110\pi\approx345.58\) cm²."))
ck(24 * pi, 75.40, 2); ck(32 * pi, 100.53, 2); ck(96 * pi, 301.59, 2); ck(leg(13, 5), 12); ck(110 * pi, 345.58, 2)
