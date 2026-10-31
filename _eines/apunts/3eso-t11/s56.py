# 11.5 L'esfera. La Terra · 11.6 Volum. Volum de prismes i cilindres
from comu import *
from fig11 import *

def solid(it, W=200, cap=None, maxh=210, pad=18): return G(it, W=W, cap=cap, maxh=maxh, pad=pad)

# =====================================================================
# 11.5 L'esfera. La Terra
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
def globe():
    it = [('circ', (0, 0), 2, 'fr')]
    f = math.radians(PH)
    for lat in (-60, -30, 0, 30, 60):
        r = 2 * math.cos(math.radians(lat)); y = 2 * math.sin(math.radians(lat)) * math.cos(f); b = r * math.sin(f)
        pts = [(r * math.cos(t), y + b * math.sin(t)) for t in [math.pi + math.pi * k / 40 for k in range(41)]]
        it.append(('pl', pts, 'ed' if lat else 'hl'))
    for lon in (-60, -30, 0, 30, 60):
        pts = []
        for k in range(41):
            la = -90 + 180 * k / 40; x, y, z = math.cos(math.radians(la)) * math.sin(math.radians(lon)), -math.cos(math.radians(la)) * math.cos(math.radians(lon)), math.sin(math.radians(la))
            pts.append((2 * x, 2 * (z * math.cos(f) + y * math.sin(f))))
        it.append(('pl', pts, 'hl2' if lon == 0 else 'ed'))
    it += [('txt', (2, 0), Ls('equador', 'ecuador', 'equator'), {'dx': 6, 'a': 'start', 'cls': 'hot'}), ('txt', (0, 2 * math.cos(f)), Ls('meridià de Greenwich', 'meridiano de Greenwich', 'Greenwich meridian'), {'dy': -8, 'cls': 'ax'})]
    return it
s5 += box('def', L('La Terra: paral·lels, meridians i coordenades', 'La Tierra: paralelos, meridianos y coordenadas', 'The Earth: parallels, meridians and coordinates'),
  P(r"La Terra és pràcticament una esfera de radi 6371 km. Els <strong>meridians</strong> són semicircumferències màximes que van d'un pol a l'altre; els <strong>paral·lels</strong>, circumferències perpendiculars a l'eix. L'<strong>equador</strong> és el paral·lel màxim. Un punt es localitza amb dues coordenades:",
    r"La Tierra es prácticamente una esfera de radio 6371 km. Los <strong>meridianos</strong> son semicircunferencias máximas que van de un polo a otro; los <strong>paralelos</strong>, circunferencias perpendiculares al eje. El <strong>ecuador</strong> es el paralelo máximo. Un punto se localiza con dos coordenadas:",
    r"The Earth is almost a sphere with a radius of 6371 km. <strong>Meridians</strong> are half great circles from pole to pole; <strong>parallels</strong> are circles perpendicular to the axis. The <strong>equator</strong> is the largest parallel. A point is located with two coordinates:")
  + ul(L(r"<strong>Latitud</strong>: angle amb l'equador, de 0° a 90° nord (N) o sud (S).", r"<strong>Latitud</strong>: ángulo con el ecuador, de 0° a 90° norte (N) o sur (S).", r"<strong>Latitude</strong>: angle from the equator, 0° to 90° north (N) or south (S)."),
       L(r"<strong>Longitud</strong>: angle amb el meridià de Greenwich, de 0° a 180° est (E) o oest (O).", r"<strong>Longitud</strong>: ángulo con el meridiano de Greenwich, de 0° a 180° este (E) u oeste (O).", r"<strong>Longitude</strong>: angle from the Greenwich meridian, 0° to 180° east (E) or west (W)."))
  + figs(solid(globe(), W=210, maxh=220))
  + P(r"València està aproximadament a 39,5° N i 0,4° O. Com que la Terra fa una volta (360°) en 24 hores, cada 15° de longitud hi ha una hora de diferència solar.",
      r"Valencia está aproximadamente a 39,5° N y 0,4° O. Como la Tierra da una vuelta (360°) en 24 horas, cada 15° de longitud hay una hora de diferencia solar.",
      r"Valencia is at about 39.5° N, 0.4° W. Since the Earth turns 360° in 24 hours, every 15° of longitude means one hour of solar time difference."))
s5 += levels(
 [prob(L(r"Calcula l'àrea d'una esfera de 6 cm de radi i la d'una pilota de 22 cm de diàmetre.", r"Calcula el área de una esfera de 6 cm de radio y la de un balón de 22 cm de diámetro.", r"Find the surface area of a sphere with a 6 cm radius and of a ball 22 cm across."),
       D(r"4\pi\cdot6^2=144\pi\approx\boxed{452{,}39\ \text{cm}^2}\qquad r=11:\ 4\pi\cdot11^2=484\pi\approx\boxed{1520{,}53\ \text{cm}^2}"))],
 [prob(L(r"Una esfera té 1256,64 cm² d'àrea. Quin radi té?", r"Una esfera tiene 1256,64 cm² de área. ¿Qué radio tiene?", r"A sphere has a surface area of 1256.64 cm². What is its radius?"),
       D(r"4\pi r^2=1256{,}64\ \Rightarrow\ r^2=\frac{1256{,}64}{4\pi}\approx100\ \Rightarrow\ r=\boxed{10\ \text{cm}}"))],
 [prob(L(r"Calcula la superfície de la Terra (radi 6371 km). Si el 71 % és aigua, quants km² de terra ferma hi ha?", r"Calcula la superficie de la Tierra (radio 6371 km). Si el 71 % es agua, ¿cuántos km² de tierra firme hay?", r"Find the Earth's surface area (radius 6371 km). If 71 % is water, how many km² of land are there?"),
       D(r"A=4\pi\cdot6371^2\approx\boxed{510\,064\,472\ \text{km}^2}"),
       D(r"0{,}29\cdot510\,064\,472\approx\boxed{147\,918\,697\ \text{km}^2}"),
       P(r"(Uns 510 milions de km², dels quals uns 148 milions són terra ferma.)", r"(Unos 510 millones de km², de los cuales unos 148 millones son tierra firme.)", r"(About 510 million km², of which about 148 million are land.)"))])
ck(144 * pi, 452.39, 2); ck(484 * pi, 1520.53, 2); ck(S(R(125664, 100) / (4 * pi)), 10, 1); ck(4 * pi * 6371 ** 2, 510064472, 0); ck(R(29, 100) * 4 * pi * 6371 ** 2, 147918697, 0)
s5 += practice([
  ('★', L(r"a) Calcula l'àrea d'una esfera de 3 cm de radi. b) I la d'una bola de 40 cm de diàmetre.", r"a) Calcula el área de una esfera de 3 cm de radio. b) Y la de una bola de 40 cm de diámetro.", r"a) Find the area of a sphere with a 3 cm radius. b) And of a ball 40 cm across.")),
  ('★★', L(r"c) Quanta pell cal per a folrar una pilota de 70 cm de circumferència màxima? d) Quina diferència horària solar hi ha entre dues ciutats de longituds 15° E i 75° O?", r"c) ¿Cuánto cuero hace falta para forrar un balón de 70 cm de circunferencia máxima? d) ¿Qué diferencia horaria solar hay entre dos ciudades de longitudes 15° E y 75° O?", r"c) How much leather is needed to cover a ball whose great circle is 70 cm long? d) What is the solar time difference between two cities at longitudes 15° E and 75° W?")),
  ('★★★', L(r"e) Si dupliquem el radi d'una esfera, per quant es multiplica la seua àrea? Comprova-ho amb \(r=1\) i \(r=2\).", r"e) Si duplicamos el radio de una esfera, ¿por cuánto se multiplica su área? Compruébalo con \(r=1\) y \(r=2\).", r"e) If a sphere's radius is doubled, what is its area multiplied by? Check with \(r=1\) and \(r=2\)."))],
  P(r"a) \(36\pi\approx113{,}10\) cm². b) \(1600\pi\approx5026{,}55\) cm². c) \(r=\frac{70}{2\pi}\approx11{,}14\) cm; \(A=4\pi r^2=\frac{4900}{\pi}\approx1559{,}72\) cm². d) \(90^\circ\): 6 hores. e) Per 4: \(4\pi\) i \(16\pi\).",
    r"a) \(36\pi\approx113{,}10\) cm². b) \(1600\pi\approx5026{,}55\) cm². c) \(r=\frac{70}{2\pi}\approx11{,}14\) cm; \(A=4\pi r^2=\frac{4900}{\pi}\approx1559{,}72\) cm². d) \(90^\circ\): 6 horas. e) Por 4: \(4\pi\) y \(16\pi\).",
    r"a) \(36\pi\approx113.10\) cm². b) \(1600\pi\approx5026.55\) cm². c) \(r=\frac{70}{2\pi}\approx11.14\) cm; \(A=4\pi r^2=\frac{4900}{\pi}\approx1559.72\) cm². d) \(90^\circ\): 6 hours. e) By 4: \(4\pi\) and \(16\pi\)."))
ck(36 * pi, 113.10, 2); ck(1600 * pi, 5026.55, 2); ck(70 / (2 * pi), 11.14, 2); ck(4900 / pi, 1559.72, 2)

# =====================================================================
# 11.6 Volum. Volum de prismes i cilindres
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
 [prob(L(r"Expressa en litres: a) 3,5 m³; b) 750 cm³; c) 0,2 dm³. Expressa en cm³: d) 1,5 L.", r"Expresa en litros: a) 3,5 m³; b) 750 cm³; c) 0,2 dm³. Expresa en cm³: d) 1,5 L.", r"Write in litres: a) 3.5 m³; b) 750 cm³; c) 0.2 dm³. Write in cm³: d) 1.5 L."),
       D(r"\text{a) }3500\ \text{L}\qquad\text{b) }0{,}75\ \text{L}\qquad\text{c) }0{,}2\ \text{L}\qquad\text{d) }1500\ \text{cm}^3")),
  prob(L(r"Calcula el volum d'un cub de 7 cm d'aresta i el d'un cilindre de 4 cm de radi i 9 cm d'altura.", r"Calcula el volumen de un cubo de 7 cm de arista y el de un cilindro de 4 cm de radio y 9 cm de altura.", r"Find the volume of a cube with 7 cm edges and of a cylinder with a 4 cm radius and 9 cm height."),
       D(r"V=7^3=\boxed{343\ \text{cm}^3}\qquad V=\pi\cdot4^2\cdot9=144\pi\approx\boxed{452{,}39\ \text{cm}^3}"))],
 [prob(L(r"Una piscina fa 25 m de llarg, 12 m d'ample i 1,8 m de fondària. Quants litres d'aigua hi caben? Si la omplim amb una aixeta que aboca 500 L per minut, quant de temps tardarà?", r"Una piscina mide 25 m de largo, 12 m de ancho y 1,8 m de profundidad. ¿Cuántos litros de agua caben? Si la llenamos con un grifo que echa 500 L por minuto, ¿cuánto tardará?", r"A pool is 25 m long, 12 m wide and 1.8 m deep. How many litres does it hold? If a tap fills it at 500 L per minute, how long will it take?"),
       D(r"V=25\cdot12\cdot1{,}8=540\ \text{m}^3=\boxed{540\,000\ \text{L}}"),
       D(r"\frac{540\,000}{500}=1080\ \text{min}=\boxed{18\ \text{%s}}" % Lt('hores', 'horas', 'hours')))],
 [prob(L(r"Calcula el volum d'un prisma hexagonal regular de 4 cm d'aresta de la base i 10 cm d'altura.", r"Calcula el volumen de un prisma hexagonal regular de 4 cm de arista de la base y 10 cm de altura.", r"Find the volume of a regular hexagonal prism with 4 cm base edges and 10 cm height."),
       D(r"a_b=\sqrt{4^2-2^2}=\sqrt{12}\qquad A_{\text{base}}=\frac{24\cdot\sqrt{12}}{2}\approx41{,}57\ \text{cm}^2"),
       D(r"V=A_{\text{base}}\cdot h\approx41{,}57\cdot10\approx\boxed{415{,}69\ \text{cm}^3}"))])
ck(343, 343); ck(144 * pi, 452.39, 2); ck(25 * 12 * R(18, 10), 540); ck(R(540000, 500), 1080); ck(120 * S(12), 415.69, 2)
s6 += practice([
  ('★', L(r"a) Expressa 2,4 m³ en dm³ i en litres. b) Calcula el volum d'un ortoedre de 6 × 5 × 2 cm.", r"a) Expresa 2,4 m³ en dm³ y en litros. b) Calcula el volumen de un ortoedro de 6 × 5 × 2 cm.", r"a) Write 2.4 m³ in dm³ and in litres. b) Find the volume of a 6 × 5 × 2 cm cuboid.")),
  ('★★', L(r"c) Un dipòsit cilíndric té 1 m de radi i 2 m d'altura. Quants litres hi caben? d) Un prisma triangular té de base un triangle rectangle de catets 3 cm i 4 cm i fa 10 cm d'altura. Quin volum té?", r"c) Un depósito cilíndrico tiene 1 m de radio y 2 m de altura. ¿Cuántos litros caben? d) Un prisma triangular tiene de base un triángulo rectángulo de catetos 3 cm y 4 cm y mide 10 cm de altura. ¿Qué volumen tiene?", r"c) A cylindrical tank has a 1 m radius and is 2 m tall. How many litres does it hold? d) A triangular prism has a right-triangle base with 3 cm and 4 cm legs and is 10 cm tall. What is its volume?")),
  ('★★★', L(r"e) Un got cilíndric de 3 cm de radi conté 0,25 L de suc. Fins a quina altura arriba el suc?", r"e) Un vaso cilíndrico de 3 cm de radio contiene 0,25 L de zumo. ¿Hasta qué altura llega el zumo?", r"e) A cylindrical glass with a 3 cm radius holds 0.25 L of juice. How high does the juice come?"))],
  P(r"a) 2400 dm³ = 2400 L. b) 60 cm³. c) \(V=2\pi\approx6{,}28\) m³ \(\approx6283\) L. d) \(\frac{3\cdot4}{2}\cdot10=60\) cm³. e) \(9\pi h=250\Rightarrow h\approx8{,}84\) cm.",
    r"a) 2400 dm³ = 2400 L. b) 60 cm³. c) \(V=2\pi\approx6{,}28\) m³ \(\approx6283\) L. d) \(\frac{3\cdot4}{2}\cdot10=60\) cm³. e) \(9\pi h=250\Rightarrow h\approx8{,}84\) cm.",
    r"a) 2400 dm³ = 2400 L. b) 60 cm³. c) \(V=2\pi\approx6.28\) m³ \(\approx6283\) L. d) \(\frac{3\cdot4}{2}\cdot10=60\) cm³. e) \(9\pi h=250\Rightarrow h\approx8.84\) cm."))
ck(2 * pi, 6.28, 2); ck(2000 * pi, 6283, 0); ck(250 / (9 * pi), 8.84, 2)
