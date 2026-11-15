# 9.3 Piràmides: elements i àrea · 9.4 Cilindre i con
from comu import *
from fig11 import *

def solid(it, W=200, cap=None, maxh=210, pad=18): return G(it, W=W, cap=cap, maxh=maxh, pad=pad)

# =====================================================================
# 9.3 Piràmides: elements i àrea
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
s3 += levels(
 [prob(L(r"Una piràmide quadrangular regular té 10 cm d'aresta de la base i 15 cm d'apotema. Calcula'n l'àrea lateral i l'àrea total.", r"Una pirámide cuadrangular regular tiene 10 cm de arista de la base y 15 cm de apotema. Calcula su área lateral y su área total.", r"A regular square pyramid has 10 cm base edges and a 15 cm slant height. Find its lateral and total area."),
       D(r"A_L=\frac{40\cdot15}{2}=\boxed{300\ \text{cm}^2}\qquad A_T=300+10^2=\boxed{400\ \text{cm}^2}"))],
 [prob(L(r"Una piràmide quadrangular regular té 12 cm d'aresta de la base i 8 cm d'altura. Calcula l'apotema i l'àrea total.", r"Una pirámide cuadrangular regular tiene 12 cm de arista de la base y 8 cm de altura. Calcula la apotema y el área total.", r"A regular square pyramid has 12 cm base edges and is 8 cm tall. Find its slant height and total area."),
       P(r"L'apotema de la base és la meitat del costat, \(a_b=6\) cm. L'altura, \(a_b\) i \(a_p\) formen un triangle rectangle:", r"La apotema de la base es la mitad del lado, \(a_b=6\) cm. La altura, \(a_b\) y \(a_p\) forman un triángulo rectángulo:", r"The base apothem is half the side, \(a_b=6\) cm. The height, \(a_b\) and \(a_p\) form a right triangle:"),
       D(r"a_p=\sqrt{8^2+6^2}=\sqrt{100}=\boxed{10\ \text{cm}}"),
       D(r"A_T=\frac{48\cdot10}{2}+12^2=240+144=\boxed{384\ \text{cm}^2}"))],
 [prob(L(r"La gran piràmide de Gizeh és (aproximadament) una piràmide quadrangular regular de 230 m de costat de la base i 146 m d'altura. Calcula'n l'apotema i la superfície de les quatre cares laterals.", r"La gran pirámide de Guiza es (aproximadamente) una pirámide cuadrangular regular de 230 m de lado de la base y 146 m de altura. Calcula su apotema y la superficie de las cuatro caras laterales.", r"The Great Pyramid of Giza is (roughly) a regular square pyramid with 230 m base sides and a height of 146 m. Find its slant height and the area of its four lateral faces."),
       D(r"a_b=\frac{230}{2}=115\ \text{m}\qquad a_p=\sqrt{146^2+115^2}=\sqrt{34\,541}\approx\boxed{185{,}85\ \text{m}}"),
       D(r"A_L=\frac{920\cdot185{,}85}{2}\approx\boxed{85\,491\ \text{m}^2}"),
       P(r"Són unes 8,5 hectàrees: com dotze camps de futbol!", r"Son unas 8,5 hectáreas: ¡como doce campos de fútbol!", r"That's about 8.5 hectares: like twelve football pitches!"))])
ck(40 * 15 / 2, 300); ck(hyp(8, 6), 10); ck(240 + 144, 384); ck(146 ** 2 + 115 ** 2, 34541); ck(S(34541), 185.85, 2); ck(460 * R(18585, 100), 85491, 0)
s3 += practice([
  ('★', L(r"a) Una piràmide pentagonal regular té 4 cm d'aresta de la base i 7 cm d'apotema. Calcula'n l'àrea lateral.", r"a) Una pirámide pentagonal regular tiene 4 cm de arista de la base y 7 cm de apotema. Calcula su área lateral.", r"a) A regular pentagonal pyramid has 4 cm base edges and a 7 cm slant height. Find its lateral area.")),
  ('★★', L(r"b) Una piràmide quadrangular regular té 14 cm d'aresta de la base i 24 cm d'altura. Calcula l'apotema i l'àrea total. c) Quant fa l'aresta lateral?", r"b) Una pirámide cuadrangular regular tiene 14 cm de arista de la base y 24 cm de altura. Calcula la apotema y el área total. c) ¿Cuánto mide la arista lateral?", r"b) A regular square pyramid has 14 cm base edges and is 24 cm tall. Find its slant height and total area. c) How long is a lateral edge?")),
  ('★★★', L(r"d) Calcula l'àrea total d'un tetraedre regular de 6 cm d'aresta (les quatre cares són triangles equilàters).", r"d) Calcula el área total de un tetraedro regular de 6 cm de arista (las cuatro caras son triángulos equiláteros).", r"d) Find the total area of a regular tetrahedron with 6 cm edges (its four faces are equilateral triangles)."))],
  P(r"a) \(\frac{20\cdot7}{2}=70\) cm². b) \(a_p=\sqrt{576+49}=25\) cm; \(A_T=\frac{56\cdot25}{2}+196=896\) cm². c) Aresta: hipotenusa de l'apotema i mig costat, \(\sqrt{625+49}=\sqrt{674}\approx25{,}96\) cm. d) Altura de cada triangle: \(\sqrt{36-9}=\sqrt{27}\approx5{,}20\) cm; \(A=4\cdot\frac{6\cdot\sqrt{27}}{2}=12\sqrt{27}\approx62{,}35\) cm².",
    r"a) \(\frac{20\cdot7}{2}=70\) cm². b) \(a_p=\sqrt{576+49}=25\) cm; \(A_T=\frac{56\cdot25}{2}+196=896\) cm². c) Arista: hipotenusa de la apotema y medio lado, \(\sqrt{625+49}=\sqrt{674}\approx25{,}96\) cm. d) Altura de cada triángulo: \(\sqrt{36-9}=\sqrt{27}\approx5{,}20\) cm; \(A=4\cdot\frac{6\cdot\sqrt{27}}{2}=12\sqrt{27}\approx62{,}35\) cm².",
    r"a) \(\frac{20\cdot7}{2}=70\) cm². b) \(a_p=\sqrt{576+49}=25\) cm; \(A_T=\frac{56\cdot25}{2}+196=896\) cm². c) Lateral edge: hypotenuse of slant height and half side, \(\sqrt{625+49}=\sqrt{674}\approx25.96\) cm. d) Height of each triangle: \(\sqrt{36-9}=\sqrt{27}\approx5.20\) cm; \(A=4\cdot\frac{6\cdot\sqrt{27}}{2}=12\sqrt{27}\approx62.35\) cm²."))
ck(70, 70); ck(hyp(24, 7), 25); ck(56 * 25 / 2 + 196, 896); ck(S(674), 25.96, 2); ck(S(27), 5.20, 2); ck(12 * S(27), 62.35, 2)


# =====================================================================
# 9.4 Cilindre i con
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
 [prob(L(r"Calcula l'àrea lateral i l'àrea total d'un cilindre de 4 cm de radi i 10 cm d'altura.", r"Calcula el área lateral y el área total de un cilindro de 4 cm de radio y 10 cm de altura.", r"Find the lateral and total surface area of a cylinder with a 4 cm radius and 10 cm height."),
       D(r"A_L=2\pi\cdot4\cdot10=80\pi\approx\boxed{251{,}33\ \text{cm}^2}"),
       D(r"A_T=80\pi+2\pi\cdot4^2=80\pi+32\pi=112\pi\approx\boxed{351{,}86\ \text{cm}^2}"))],
 [prob(L(r"Un con té 10 cm de diàmetre i 12 cm d'altura. Calcula la generatriu i l'àrea total.", r"Un cono tiene 10 cm de diámetro y 12 cm de altura. Calcula la generatriz y el área total.", r"A cone is 10 cm across and 12 cm tall. Find its slant height and total area."),
       D(r"r=5\qquad g=\sqrt{12^2+5^2}=\sqrt{169}=\boxed{13\ \text{cm}}"),
       D(r"A_T=\pi\cdot5\cdot13+\pi\cdot5^2=65\pi+25\pi=90\pi\approx\boxed{282{,}74\ \text{cm}^2}"))],
 [prob(L(r"Volem fer un barret de bruixa de cartolina en forma de con (sense base), de 12 cm de radi i 35 cm d'altura, i un got cilíndric de cartó (sense tapa) de 4 cm de radi i 10 cm d'altura. Quanta cartolina cal per a cada objecte?", r"Queremos hacer un sombrero de bruja de cartulina con forma de cono (sin base), de 12 cm de radio y 35 cm de altura, y un vaso cilíndrico de cartón (sin tapa) de 4 cm de radio y 10 cm de altura. ¿Cuánta cartulina hace falta para cada objeto?", r"We want to make a witch's hat out of card shaped like a cone (no base), with a 12 cm radius and 35 cm height, and a cylindrical card cup (no lid) with a 4 cm radius and 10 cm height. How much card is needed for each?"),
       P(r"El barret només té superfície lateral. Primer, la generatriu:", r"El sombrero solo tiene superficie lateral. Primero, la generatriz:", r"The hat only has a lateral surface. First, the slant height:"),
       D(r"g=\sqrt{35^2+12^2}=\sqrt{1369}=37\ \text{cm}\qquad A_L=\pi\cdot12\cdot37=444\pi\approx\boxed{1394{,}87\ \text{cm}^2}"),
       P(r"El got té la superfície lateral i <strong>un sol</strong> cercle (el fons):", r"El vaso tiene la superficie lateral y <strong>un solo</strong> círculo (el fondo):", r"The cup has the lateral surface and <strong>only one</strong> disc (the bottom):"),
       D(r"A=2\pi\cdot4\cdot10+\pi\cdot4^2=80\pi+16\pi=96\pi\approx\boxed{301{,}59\ \text{cm}^2}"))])
ck(80 * pi, 251.33, 2); ck(112 * pi, 351.86, 2); ck(hyp(12, 5), 13); ck(90 * pi, 282.74, 2); ck(hyp(35, 12), 37); ck(444 * pi, 1394.87, 2); ck(96 * pi, 301.59, 2)
s4 += practice([
  ('★', L(r"a) Calcula l'àrea lateral i total d'un cilindre de 3 cm de radi i 7 cm d'altura.", r"a) Calcula el área lateral y total de un cilindro de 3 cm de radio y 7 cm de altura.", r"a) Find the lateral and total area of a cylinder with a 3 cm radius and 7 cm height.")),
  ('★★', L(r"b) Un con té 8 cm de radi i 6 cm d'altura. Calcula la generatriu i l'àrea total. c) Un con té 17 cm de generatriu i 8 cm de radi. Quina altura té?", r"b) Un cono tiene 8 cm de radio y 6 cm de altura. Calcula la generatriz y el área total. c) Un cono tiene 17 cm de generatriz y 8 cm de radio. ¿Qué altura tiene?", r"b) A cone has an 8 cm radius and is 6 cm tall. Find its slant height and total area. c) A cone has a 17 cm slant height and an 8 cm radius. How tall is it?")),
  ('★★★', L(r"d) Un cilindre de 5 cm de radi té una àrea lateral de \(80\pi\) cm². Quina altura té? Quina és l'àrea total?", r"d) Un cilindro de 5 cm de radio tiene un área lateral de \(80\pi\) cm². ¿Qué altura tiene? ¿Cuál es el área total?", r"d) A cylinder with a 5 cm radius has a lateral area of \(80\pi\) cm². How tall is it? What is its total area?"))],
  P(r"a) \(A_L=42\pi\approx131{,}95\) cm²; \(A_T=60\pi\approx188{,}50\) cm². b) \(g=10\) cm; \(A_T=80\pi+64\pi=144\pi\approx452{,}39\) cm². c) \(h=\sqrt{289-64}=15\) cm. d) \(10\pi h=80\pi\Rightarrow h=8\) cm; \(A_T=80\pi+50\pi=130\pi\approx408{,}41\) cm².",
    r"a) \(A_L=42\pi\approx131{,}95\) cm²; \(A_T=60\pi\approx188{,}50\) cm². b) \(g=10\) cm; \(A_T=80\pi+64\pi=144\pi\approx452{,}39\) cm². c) \(h=\sqrt{289-64}=15\) cm. d) \(10\pi h=80\pi\Rightarrow h=8\) cm; \(A_T=80\pi+50\pi=130\pi\approx408{,}41\) cm².",
    r"a) \(A_L=42\pi\approx131.95\) cm²; \(A_T=60\pi\approx188.50\) cm². b) \(g=10\) cm; \(A_T=80\pi+64\pi=144\pi\approx452.39\) cm². c) \(h=\sqrt{289-64}=15\) cm. d) \(10\pi h=80\pi\Rightarrow h=8\) cm; \(A_T=80\pi+50\pi=130\pi\approx408.41\) cm²."))
ck(42 * pi, 131.95, 2); ck(60 * pi, 188.50, 2); ck(hyp(8, 6), 10); ck(144 * pi, 452.39, 2); ck(leg(17, 8), 15); ck(130 * pi, 408.41, 2)
