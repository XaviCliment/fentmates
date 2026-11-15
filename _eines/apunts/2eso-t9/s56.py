# 9.5 L'esfera · 9.6 Volum. Volum de prismes i cilindres
from comu import *
from fig11 import *

def solid(it, W=200, cap=None, maxh=210, pad=18): return G(it, W=W, cap=cap, maxh=maxh, pad=pad)

# =====================================================================
# 9.5 L'esfera
# =====================================================================
FS, _ = f_sphere(2)
ARQ = shift(cylinder(2, 4, top=True)[0], 0, -2) + sphere(2)[0]
s5 = box('def', L("L'esfera i la seua àrea", 'La esfera y su área', 'The sphere and its surface area'),
  P(r"La <strong>superfície esfèrica</strong> és el conjunt de punts de l'espai que estan a la mateixa distància, el <strong>radi</strong> \(r\), d'un punt, el <strong>centre</strong>. L'<strong>esfera</strong> és el cos que limita. Qualsevol pla que passa pel centre la talla en un <strong>cercle màxim</strong>.",
    r"La <strong>superficie esférica</strong> es el conjunto de puntos del espacio que están a la misma distancia, el <strong>radio</strong> \(r\), de un punto, el <strong>centro</strong>. La <strong>esfera</strong> es el cuerpo que limita. Cualquier plano que pasa por el centro la corta en un <strong>círculo máximo</strong>.",
    r"A <strong>spherical surface</strong> is the set of points in space at the same distance, the <strong>radius</strong> \(r\), from a point, the <strong>centre</strong>. The <strong>sphere</strong> (ball) is the solid it bounds. Any plane through the centre cuts it in a <strong>great circle</strong>.")
  + P(r"L'esfera no es pot desplegar sobre un pla (per això els mapes del món sempre deformen). La seua àrea és la de <strong>quatre cercles màxims</strong>:",
      r"La esfera no se puede desplegar sobre un plano (por eso los mapas del mundo siempre deforman). Su área es la de <strong>cuatro círculos máximos</strong>:",
      r"A sphere can't be unrolled flat (that's why world maps always distort). Its area equals that of <strong>four great circles</strong>:")
  + D(r"A=4\pi r^2")
  + figs(solid(FS, W=150, cap=L('Esfera', 'Esfera', 'Sphere')), solid(ARQ, W=150, cap=L('Esfera i cilindre circumscrit', 'Esfera y cilindro circunscrito', 'Sphere in its circumscribed cylinder')))
  + note(r"Arquimedes va descobrir que l'àrea de l'esfera és igual a l'àrea lateral del cilindre que l'envolta: \(2\pi r\cdot2r=4\pi r^2\). En va estar tan orgullós que va demanar que gravaren aquesta figura a la seua tomba.",
         r"Arquímedes descubrió que el área de la esfera es igual al área lateral del cilindro que la envuelve: \(2\pi r\cdot2r=4\pi r^2\). Estaba tan orgulloso que pidió que grabaran esta figura en su tumba.",
         r"Archimedes discovered that the area of a sphere equals the lateral area of the cylinder around it: \(2\pi r\cdot2r=4\pi r^2\). He was so proud of it that he asked for this figure to be carved on his tomb.", '🏺')
  + D(r"r=5\ \text{cm}:\quad A=4\pi\cdot25=100\pi\approx314{,}16\ \text{cm}^2")
  + drill('esfera', "Entrena: àrea de l'esfera", 'Entrena: área de la esfera', 'Train: surface area of a sphere'))
ck(100 * pi, 314.16, 2)
s5 += levels(
 [prob(L(r"Calcula l'àrea d'una esfera de 4 cm de radi i la d'una pilota de bàsquet de 24 cm de diàmetre.", r"Calcula el área de una esfera de 4 cm de radio y la de un balón de baloncesto de 24 cm de diámetro.", r"Find the surface area of a sphere with a 4 cm radius and of a basketball 24 cm across."),
       D(r"4\pi\cdot4^2=64\pi\approx\boxed{201{,}06\ \text{cm}^2}\qquad r=12:\ 4\pi\cdot12^2=576\pi\approx\boxed{1809{,}56\ \text{cm}^2}"))],
 [prob(L(r"Una esfera té 2827,43 cm² d'àrea. Quin radi té?", r"Una esfera tiene 2827,43 cm² de área. ¿Qué radio tiene?", r"A sphere has a surface area of 2827.43 cm². What is its radius?"),
       D(r"4\pi r^2=2827{,}43\ \Rightarrow\ r^2=\frac{2827{,}43}{4\pi}\approx225\ \Rightarrow\ r=\sqrt{225}=\boxed{15\ \text{cm}}"))],
 [prob(L(r"Volem pintar per fora una cúpula semiesfèrica de 10 m de diàmetre. Si amb un pot de pintura pintem 20 m², quants pots necessitem?", r"Queremos pintar por fuera una cúpula semiesférica de 10 m de diámetro. Si con un bote de pintura pintamos 20 m², ¿cuántos botes necesitamos?", r"We want to paint the outside of a hemispherical dome 10 m across. If one tin of paint covers 20 m², how many tins do we need?"),
       P(r"La cúpula és la meitat d'una esfera de radi 5 m (sense el cercle de baix):", r"La cúpula es la mitad de una esfera de radio 5 m (sin el círculo de abajo):", r"The dome is half a sphere with a 5 m radius (without the disc at the bottom):"),
       D(r"A=\frac{4\pi\cdot5^2}{2}=50\pi\approx157{,}08\ \text{m}^2\qquad\frac{157{,}08}{20}\approx7{,}85\ \Rightarrow\ \boxed{8\ \text{%s}}" % Lt('pots', 'botes', 'tins')))])
ck(64 * pi, 201.06, 2); ck(576 * pi, 1809.56, 2); ck(900 * pi, 2827.43, 2); ck(R(282743, 100) / (4 * pi), 225, 1); ck(50 * pi, 157.08, 2); ck(R(15708, 100) / 20, 7.85, 2)
s5 += practice([
  ('★', L(r"a) Calcula l'àrea d'una esfera de 2 cm de radi. b) I la d'una bola de 30 cm de diàmetre.", r"a) Calcula el área de una esfera de 2 cm de radio. b) Y la de una bola de 30 cm de diámetro.", r"a) Find the area of a sphere with a 2 cm radius. b) And of a ball 30 cm across.")),
  ('★★', L(r"c) Quanta pell cal per a folrar una pilota de 66 cm de circumferència màxima? d) Quanta pell té una taronja (esfèrica) de 9 cm de diàmetre?", r"c) ¿Cuánto cuero hace falta para forrar un balón de 66 cm de circunferencia máxima? d) ¿Cuánta piel tiene una naranja (esférica) de 9 cm de diámetro?", r"c) How much leather is needed to cover a ball whose great circle is 66 cm long? d) How much peel does a (spherical) orange 9 cm across have?")),
  ('★★★', L(r"e) Si dupliquem el radi d'una esfera, per quant es multiplica la seua àrea? Comprova-ho amb \(r=1\) i \(r=2\).", r"e) Si duplicamos el radio de una esfera, ¿por cuánto se multiplica su área? Compruébalo con \(r=1\) y \(r=2\).", r"e) If a sphere's radius is doubled, what is its area multiplied by? Check with \(r=1\) and \(r=2\)."))],
  P(r"a) \(16\pi\approx50{,}27\) cm². b) \(900\pi\approx2827{,}43\) cm². c) \(r=\frac{66}{2\pi}\approx10{,}50\) cm; \(A=4\pi r^2=\frac{66^2}{\pi}\approx1386{,}56\) cm². d) \(r=4{,}5\): \(81\pi\approx254{,}47\) cm². e) Per 4: \(4\pi\) i \(16\pi\).",
    r"a) \(16\pi\approx50{,}27\) cm². b) \(900\pi\approx2827{,}43\) cm². c) \(r=\frac{66}{2\pi}\approx10{,}50\) cm; \(A=4\pi r^2=\frac{66^2}{\pi}\approx1386{,}56\) cm². d) \(r=4{,}5\): \(81\pi\approx254{,}47\) cm². e) Por 4: \(4\pi\) y \(16\pi\).",
    r"a) \(16\pi\approx50.27\) cm². b) \(900\pi\approx2827.43\) cm². c) \(r=\frac{66}{2\pi}\approx10.50\) cm; \(A=4\pi r^2=\frac{66^2}{\pi}\approx1386.56\) cm². d) \(r=4.5\): \(81\pi\approx254.47\) cm². e) By 4: \(4\pi\) and \(16\pi\)."))
ck(16 * pi, 50.27, 2); ck(900 * pi, 2827.43, 2); ck(66 / (2 * pi), 10.50, 2); ck(4356 / pi, 1386.56, 2); ck(81 * pi, 254.47, 2)


# =====================================================================
# 9.6 Volum. Volum de prismes i cilindres
# =====================================================================
s6 = box('def', L('Volum i capacitat', 'Volumen y capacidad', 'Volume and capacity'),
  P(r"El <strong>volum</strong> d'un cos és l'espai que ocupa. La unitat principal és el <strong>metre cúbic</strong> (m³), el volum d'un cub d'1 m d'aresta. Cada unitat és <strong>1000 vegades</strong> més gran que la següent:",
    r"El <strong>volumen</strong> de un cuerpo es el espacio que ocupa. La unidad principal es el <strong>metro cúbico</strong> (m³), el volumen de un cubo de 1 m de arista. Cada unidad es <strong>1000 veces</strong> mayor que la siguiente:",
    r"The <strong>volume</strong> of a solid is the space it takes up. The main unit is the <strong>cubic metre</strong> (m³), the volume of a cube with 1 m edges. Each unit is <strong>1000 times</strong> bigger than the next:")
  + D(r"1\ \text{km}^3\ \xrightarrow{\cdot1000}\ \dots\ \xrightarrow{\cdot1000}\ 1\ \text{m}^3=1000\ \text{dm}^3\qquad1\ \text{dm}^3=1000\ \text{cm}^3\qquad1\ \text{cm}^3=1000\ \text{mm}^3")
  + P(r"La <strong>capacitat</strong> és el que hi cap a dins d'un recipient, i es mesura en litres. La relació clau és:",
      r"La <strong>capacidad</strong> es lo que cabe dentro de un recipiente, y se mide en litros. La relación clave es:",
      r"<strong>Capacity</strong> is how much a container holds, measured in litres. The key relationship is:")
  + D(r"1\ \text{dm}^3=1\ \text{L}\qquad1\ \text{cm}^3=1\ \text{mL}\qquad1\ \text{m}^3=1000\ \text{L}")
  + widget('w-units', '🔁', L('Converteix unitats de volum i capacitat', 'Convierte unidades de volumen y capacidad', 'Convert units of volume and capacity'),
           ['<div class="wrow">' + tin('v', L('Quantitat', 'Cantidad', 'Amount'), '2,5', 'm') + '<label><select data-k="from" aria-label="from"></select></label> → <label><select data-k="to" aria-label="to"></select></label></div>'],
           out='<div class="hsteps"></div>')
  + drill('unitats', 'Entrena: unitats de volum i capacitat', 'Entrena: unidades de volumen y capacidad', 'Train: units of volume and capacity'))
s6 += box('prop', L('Principi de Cavalieri. Volum del prisma i del cilindre', 'Principio de Cavalieri. Volumen del prisma y del cilindro', "Cavalieri's principle. Volume of prisms and cylinders"),
  P(r"Una pila de monedes ocupa el mateix volum si està recta o si la torcem. <strong>Principi de Cavalieri:</strong> si dos cossos tenen la mateixa altura i, a qualsevol altura, les seccions tenen la mateixa àrea, aleshores tenen el mateix volum.",
    r"Una pila de monedas ocupa el mismo volumen si está recta o si la torcemos. <strong>Principio de Cavalieri:</strong> si dos cuerpos tienen la misma altura y, a cualquier altura, las secciones tienen la misma área, entonces tienen el mismo volumen.",
    r"A stack of coins takes up the same volume whether it's straight or slanted. <strong>Cavalieri's principle:</strong> if two solids have the same height and, at every height, their cross-sections have the same area, then they have the same volume.")
  + widget('w-cav', '🪙', L('Inclina la pila de monedes', 'Inclina la pila de monedas', 'Slant the stack of coins'),
           ['<div class="wrow">' + rng('s', 0, 1.2, 0.05, 0.5, 's') + '</div>'])
  + P(r"Un ortoedre d'arestes \(a,\,b,\,c\) conté \(a\cdot b\cdot c\) cubets unitat: el volum és l'àrea de la base per l'altura. Per Cavalieri, això val per a <strong>qualsevol prisma</strong> (recte o oblic) i per al <strong>cilindre</strong>:",
      r"Un ortoedro de aristas \(a,\,b,\,c\) contiene \(a\cdot b\cdot c\) cubitos unidad: el volumen es el área de la base por la altura. Por Cavalieri, esto vale para <strong>cualquier prisma</strong> (recto u oblicuo) y para el <strong>cilindro</strong>:",
      r"A cuboid with edges \(a,\,b,\,c\) holds \(a\cdot b\cdot c\) unit cubes: its volume is base area times height. By Cavalieri, this holds for <strong>any prism</strong> (right or oblique) and for the <strong>cylinder</strong>:")
  + D(r"V_{\text{%s}}=A_{\text{base}}\cdot h\qquad\qquad V_{\text{%s}}=\pi r^2h" % (Lt('prisma', 'prisma', 'prism'), Lt('cilindre', 'cilindro', 'cylinder')))
  + P(r"Exemples: un ortoedre de 5 × 4 × 3 cm té \(V=60\) cm³; un cilindre de \(r=3\) cm i \(h=10\) cm, \(V=\pi\cdot9\cdot10=90\pi\approx282{,}74\) cm³ \(\approx0{,}28\) L.",
      r"Ejemplos: un ortoedro de 5 × 4 × 3 cm tiene \(V=60\) cm³; un cilindro de \(r=3\) cm y \(h=10\) cm, \(V=\pi\cdot9\cdot10=90\pi\approx282{,}74\) cm³ \(\approx0{,}28\) L.",
      r"Examples: a 5 × 4 × 3 cm cuboid has \(V=60\) cm³; a cylinder with \(r=3\) cm and \(h=10\) cm has \(V=\pi\cdot9\cdot10=90\pi\approx282.74\) cm³ \(\approx0.28\) L.")
  + drill('vprisma', 'Entrena: volum de prismes i cilindres', 'Entrena: volumen de prismas y cilindros', 'Train: volume of prisms and cylinders'))
ck(90 * pi, 282.74, 2)
s6 += levels(
 [prob(L(r"Expressa en litres: a) 4,2 m³; b) 350 cm³; c) 0,8 dm³. Expressa en cm³: d) 2,5 L.", r"Expresa en litros: a) 4,2 m³; b) 350 cm³; c) 0,8 dm³. Expresa en cm³: d) 2,5 L.", r"Write in litres: a) 4.2 m³; b) 350 cm³; c) 0.8 dm³. Write in cm³: d) 2.5 L."),
       D(r"\text{a) }4200\ \text{L}\qquad\text{b) }0{,}35\ \text{L}\qquad\text{c) }0{,}8\ \text{L}\qquad\text{d) }2500\ \text{cm}^3")),
  prob(L(r"Calcula el volum d'un cub de 9 cm d'aresta i el d'un cilindre de 5 cm de radi i 8 cm d'altura.", r"Calcula el volumen de un cubo de 9 cm de arista y el de un cilindro de 5 cm de radio y 8 cm de altura.", r"Find the volume of a cube with 9 cm edges and of a cylinder with a 5 cm radius and 8 cm height."),
       D(r"V=9^3=\boxed{729\ \text{cm}^3}\qquad V=\pi\cdot5^2\cdot8=200\pi\approx\boxed{628{,}32\ \text{cm}^3}"))],
 [prob(L(r"Una piscina fa 20 m de llarg, 10 m d'ample i 1,5 m de fondària. Quants litres d'aigua hi caben? Si la omplim amb una aixeta que aboca 250 L per minut, quant de temps tardarà?", r"Una piscina mide 20 m de largo, 10 m de ancho y 1,5 m de profundidad. ¿Cuántos litros de agua caben? Si la llenamos con un grifo que echa 250 L por minuto, ¿cuánto tardará?", r"A pool is 20 m long, 10 m wide and 1.5 m deep. How many litres does it hold? If a tap fills it at 250 L per minute, how long will it take?"),
       D(r"V=20\cdot10\cdot1{,}5=300\ \text{m}^3=\boxed{300\,000\ \text{L}}"),
       D(r"\frac{300\,000}{250}=1200\ \text{min}=\boxed{20\ \text{%s}}" % Lt('hores', 'horas', 'hours')))],
 [prob(L(r"Calcula el volum d'un prisma hexagonal regular de 6 cm d'aresta de la base i 12 cm d'altura.", r"Calcula el volumen de un prisma hexagonal regular de 6 cm de arista de la base y 12 cm de altura.", r"Find the volume of a regular hexagonal prism with 6 cm base edges and 12 cm height."),
       P(r"L'hexàgon regular està format per 6 triangles equilàters de costat 6; l'apotema és l'altura d'un d'ells:", r"El hexágono regular está formado por 6 triángulos equiláteros de lado 6; la apotema es la altura de uno de ellos:", r"The regular hexagon is made of 6 equilateral triangles with side 6; the apothem is the height of one of them:"),
       D(r"a_b=\sqrt{6^2-3^2}=\sqrt{27}\approx5{,}20\ \text{cm}\qquad A_{\text{base}}=\frac{36\cdot\sqrt{27}}{2}=18\sqrt{27}\approx93{,}53\ \text{cm}^2"),
       D(r"V=A_{\text{base}}\cdot h=18\sqrt{27}\cdot12=216\sqrt{27}\approx\boxed{1122{,}37\ \text{cm}^3}"))])
ck(729, 729); ck(200 * pi, 628.32, 2); ck(20 * 10 * R(15, 10), 300); ck(R(300000, 250), 1200); ck(S(27), 5.20, 2); ck(18 * S(27), 93.53, 2); ck(216 * S(27), 1122.37, 2)
s6 += practice([
  ('★', L(r"a) Expressa 3,6 m³ en dm³ i en litres. b) Calcula el volum d'un ortoedre de 8 × 5 × 3 cm.", r"a) Expresa 3,6 m³ en dm³ y en litros. b) Calcula el volumen de un ortoedro de 8 × 5 × 3 cm.", r"a) Write 3.6 m³ in dm³ and in litres. b) Find the volume of an 8 × 5 × 3 cm cuboid.")),
  ('★★', L(r"c) Un dipòsit cilíndric té 0,5 m de radi i 2 m d'altura. Quants litres hi caben? d) Un prisma té de base un triangle rectangle de catets 6 cm i 8 cm i fa 12 cm d'altura. Quin volum té?", r"c) Un depósito cilíndrico tiene 0,5 m de radio y 2 m de altura. ¿Cuántos litros caben? d) Un prisma tiene de base un triángulo rectángulo de catetos 6 cm y 8 cm y mide 12 cm de altura. ¿Qué volumen tiene?", r"c) A cylindrical tank has a 0.5 m radius and is 2 m tall. How many litres does it hold? d) A prism has a right-triangle base with 6 cm and 8 cm legs and is 12 cm tall. What is its volume?")),
  ('★★★', L(r"e) Un got cilíndric de 4 cm de radi conté 0,3 L d'aigua. Fins a quina altura arriba l'aigua?", r"e) Un vaso cilíndrico de 4 cm de radio contiene 0,3 L de agua. ¿Hasta qué altura llega el agua?", r"e) A cylindrical glass with a 4 cm radius holds 0.3 L of water. How high does the water come?"))],
  P(r"a) 3600 dm³ = 3600 L. b) 120 cm³. c) \(V=\pi\cdot0{,}25\cdot2=0{,}5\pi\approx1{,}57\) m³ \(\approx1571\) L. d) \(\frac{6\cdot8}{2}\cdot12=288\) cm³. e) 0,3 L = 300 cm³: \(16\pi h=300\Rightarrow h\approx5{,}97\) cm.",
    r"a) 3600 dm³ = 3600 L. b) 120 cm³. c) \(V=\pi\cdot0{,}25\cdot2=0{,}5\pi\approx1{,}57\) m³ \(\approx1571\) L. d) \(\frac{6\cdot8}{2}\cdot12=288\) cm³. e) 0,3 L = 300 cm³: \(16\pi h=300\Rightarrow h\approx5{,}97\) cm.",
    r"a) 3600 dm³ = 3600 L. b) 120 cm³. c) \(V=\pi\cdot0.25\cdot2=0.5\pi\approx1.57\) m³ \(\approx1571\) L. d) \(\frac{6\cdot8}{2}\cdot12=288\) cm³. e) 0.3 L = 300 cm³: \(16\pi h=300\Rightarrow h\approx5.97\) cm."))
ck(R(1, 2) * pi, 1.57, 2); ck(500 * pi, 1571, 0); ck(24 * 12, 288); ck(300 / (16 * pi), 5.97, 2)
