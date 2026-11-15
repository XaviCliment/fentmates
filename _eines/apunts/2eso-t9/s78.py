# 9.7 Volum de piràmides, cons i esferes · 9.8 Cossos compostos i problemes
from comu import *
from fig11 import *

def solid(it, W=200, cap=None, maxh=210, pad=18): return G(it, W=W, cap=cap, maxh=maxh, pad=pad)

# =====================================================================
# 9.7 Volum de piràmides, cons i esferes
# =====================================================================
FY, _ = polyhedron(pyramid(4, 3, 3.4))
FPR, _ = polyhedron(prism(4, 3, 3.4))
s7 = box('prop', L('Volum de la piràmide i del con', 'Volumen de la pirámide y del cono', 'Volume of pyramids and cones'),
  P(r"Si omplim d'aigua una piràmide i l'abocem en un prisma de la mateixa base i la mateixa altura, cal fer-ho <strong>tres vegades</strong> per a omplir el prisma. El mateix passa amb un con i un cilindre:",
    r"Si llenamos de agua una pirámide y la vaciamos en un prisma de la misma base y la misma altura, hay que hacerlo <strong>tres veces</strong> para llenar el prisma. Lo mismo pasa con un cono y un cilindro:",
    r"If you fill a pyramid with water and pour it into a prism with the same base and height, you need to do it <strong>three times</strong> to fill the prism. The same happens with a cone and a cylinder:")
  + figs(solid(FPR + shift(FY, 0, 0), W=150, cap=r'\(V_{\text{pir}}=\frac13V_{\text{prisma}}\)'), solid(cylinder(1.4, 3.2)[0] + cone(1.4, 3.2)[0], W=130, cap=r'\(V_{\text{con}}=\frac13V_{\text{cil}}\)'))
  + D(r"V_{\text{%s}}=\frac{A_{\text{base}}\cdot h}{3}\qquad\qquad V_{\text{%s}}=\frac{\pi r^2h}{3}" % (Lt('piràmide', 'pirámide', 'pyramid'), Lt('con', 'cono', 'cone')))
  + P(r"Exemple: una piràmide quadrangular de 6 cm d'aresta de la base i 4 cm d'altura té \(V=\frac{36\cdot4}{3}=48\) cm³. Un con de \(r=3\) cm i \(h=4\) cm té \(V=\frac{\pi\cdot9\cdot4}{3}=12\pi\approx37{,}70\) cm³.",
      r"Ejemplo: una pirámide cuadrangular de 6 cm de arista de la base y 4 cm de altura tiene \(V=\frac{36\cdot4}{3}=48\) cm³. Un cono de \(r=3\) cm y \(h=4\) cm tiene \(V=\frac{\pi\cdot9\cdot4}{3}=12\pi\approx37{,}70\) cm³.",
      r"Example: a square pyramid with 6 cm base edges and 4 cm height has \(V=\frac{36\cdot4}{3}=48\) cm³. A cone with \(r=3\) cm and \(h=4\) cm has \(V=\frac{\pi\cdot9\cdot4}{3}=12\pi\approx37.70\) cm³.")
  + widget('w-fill', '💧', L('Tres piràmides omplen un prisma', 'Tres pirámides llenan un prisma', 'Three pyramids fill a prism'),
           [seg([('pyr', L('Piràmide i prisma', 'Pirámide y prisma', 'Pyramid and prism')), ('con', L('Con i cilindre', 'Cono y cilindro', 'Cone and cylinder'))]),
            '<div class="wrow"><button class="btn primary" type="button" data-a="pour">' + L('Aboca una piràmide plena', 'Vierte una pirámide llena', 'Pour a full pyramid') + '</button><button class="btn" type="button" data-a="empty">↺ ' + L('Buida', 'Vacía', 'Empty') + '</button></div>']))
ck(R(36 * 4, 3), 48); ck(12 * pi, 37.70, 2)
s7 += box('prop', L("Volum de l'esfera", 'Volumen de la esfera', 'Volume of a sphere'),
  P(r"Arquimedes també va descobrir que el volum de l'esfera és \(\frac23\) del volum del cilindre que l'envolta (\(\pi r^2\cdot2r=2\pi r^3\)):",
    r"Arquímedes también descubrió que el volumen de la esfera es \(\frac23\) del volumen del cilindro que la envuelve (\(\pi r^2\cdot2r=2\pi r^3\)):",
    r"Archimedes also found that the volume of a sphere is \(\frac23\) of the volume of the cylinder around it (\(\pi r^2\cdot2r=2\pi r^3\)):")
  + D(r"V_{\text{%s}}=\frac23\cdot2\pi r^3=\frac43\pi r^3" % Lt('esfera', 'esfera', 'sphere'))
  + P(r"Exemple: una pilota de 11 cm de radi té \(V=\frac43\pi\cdot11^3\approx5575{,}28\) cm³ \(\approx5{,}6\) L.",
      r"Ejemplo: un balón de 11 cm de radio tiene \(V=\frac43\pi\cdot11^3\approx5575{,}28\) cm³ \(\approx5{,}6\) L.",
      r"Example: a ball with an 11 cm radius has \(V=\frac43\pi\cdot11^3\approx5575.28\) cm³ \(\approx5.6\) L.")
  + widget('w-vol', '📐', L('Calculadora de volums', 'Calculadora de volúmenes', 'Volume calculator'),
           [seg([('pr', L('Prisma', 'Prisma', 'Prism')), ('py', L('Piràmide', 'Pirámide', 'Pyramid')), ('ci', L('Cilindre', 'Cilindro', 'Cylinder')), ('co', L('Con', 'Cono', 'Cone')), ('es', L('Esfera', 'Esfera', 'Sphere'))]),
            '<div class="wrow">' + rng('n', 3, 8, 1, 4, 'n') + rng('l', 0.5, 10, 0.5, 4, 'l') + rng('h', 0.5, 15, 0.5, 6, 'h') + '</div>'],
           out='<div class="gout"></div><div class="hsteps"></div>')
  + drill('vpir', 'Entrena: volum de piràmides i cons', 'Entrena: volumen de pirámides y conos', 'Train: volume of pyramids and cones')
  + drill('vesf', "Entrena: volum de l'esfera", 'Entrena: volumen de la esfera', 'Train: volume of a sphere'))
ck(R(4, 3) * pi * 11 ** 3, 5575.28, 2)
s7 += levels(
 [prob(L(r"Calcula el volum d'un con de 3 cm de radi i 8 cm d'altura i el d'una esfera de 6 cm de radi.", r"Calcula el volumen de un cono de 3 cm de radio y 8 cm de altura y el de una esfera de 6 cm de radio.", r"Find the volume of a cone with a 3 cm radius and 8 cm height, and of a sphere with a 6 cm radius."),
       D(r"V=\frac{\pi\cdot9\cdot8}{3}=24\pi\approx\boxed{75{,}40\ \text{cm}^3}\qquad V=\frac43\pi\cdot216=288\pi\approx\boxed{904{,}78\ \text{cm}^3}"))],
 [prob(L(r"Una piràmide hexagonal regular té 4 cm d'aresta de la base i 9 cm d'altura. Calcula'n el volum.", r"Una pirámide hexagonal regular tiene 4 cm de arista de la base y 9 cm de altura. Calcula su volumen.", r"A regular hexagonal pyramid has 4 cm base edges and is 9 cm tall. Find its volume."),
       D(r"a_b=\sqrt{4^2-2^2}=\sqrt{12}\approx3{,}46\ \text{cm}\qquad A_{\text{base}}=\frac{24\cdot\sqrt{12}}{2}=12\sqrt{12}\approx41{,}57\ \text{cm}^2"),
       D(r"V=\frac{A_{\text{base}}\cdot h}{3}=\frac{12\sqrt{12}\cdot9}{3}=36\sqrt{12}\approx\boxed{124{,}71\ \text{cm}^3}"))],
 [prob(L(r"Un con té 10 cm de generatriu i 6 cm de radi. Calcula'n el volum. Quin radi ha de tenir una esfera perquè tinga el mateix volum?", r"Un cono tiene 10 cm de generatriz y 6 cm de radio. Calcula su volumen. ¿Qué radio debe tener una esfera para tener el mismo volumen?", r"A cone has a 10 cm slant height and a 6 cm radius. Find its volume. What radius must a sphere have to have the same volume?"),
       D(r"h=\sqrt{10^2-6^2}=8\qquad V=\frac{\pi\cdot36\cdot8}{3}=96\pi\approx\boxed{301{,}59\ \text{cm}^3}"),
       D(r"\frac43\pi R^3=96\pi\ \Rightarrow\ R^3=72\ \Rightarrow\ R=\sqrt[3]{72}\approx\boxed{4{,}16\ \text{cm}}"))])
ck(24 * pi, 75.40, 2); ck(288 * pi, 904.78, 2); ck(S(12), 3.46, 2); ck(12 * S(12), 41.57, 2); ck(36 * S(12), 124.71, 2); ck(leg(10, 6), 8); ck(96 * pi, 301.59, 2); ck(72 ** (1 / 3.0), 4.16, 2)
s7 += practice([
  ('★', L(r"a) Calcula el volum d'una piràmide quadrangular de 6 cm d'aresta de la base i 10 cm d'altura. b) I el d'una esfera de 9 cm de radi.", r"a) Calcula el volumen de una pirámide cuadrangular de 6 cm de arista de la base y 10 cm de altura. b) Y el de una esfera de 9 cm de radio.", r"a) Find the volume of a square pyramid with 6 cm base edges and 10 cm height. b) And of a sphere with a 9 cm radius.")),
  ('★★', L(r"c) Un cucurutxo cònic fa 6 cm de diàmetre i 10 cm d'altura. Quants mL de gelat hi caben (sense sobreeixir)? d) Un con i un cilindre tenen la mateixa base. Quina altura ha de tenir el con perquè tinguen el mateix volum?", r"c) Un cucurucho cónico mide 6 cm de diámetro y 10 cm de altura. ¿Cuántos mL de helado caben (sin rebosar)? d) Un cono y un cilindro tienen la misma base. ¿Qué altura debe tener el cono para que tengan el mismo volumen?", r"c) A cone-shaped wafer is 6 cm across and 10 cm tall. How many mL of ice cream fit inside (level with the top)? d) A cone and a cylinder have the same base. How tall must the cone be for them to have the same volume?")),
  ('★★★', L(r"e) Una esfera té \(36\pi\) cm³ de volum. Quin radi té? Quina és la seua àrea?", r"e) Una esfera tiene \(36\pi\) cm³ de volumen. ¿Qué radio tiene? ¿Cuál es su área?", r"e) A sphere has a volume of \(36\pi\) cm³. What is its radius? What is its surface area?"))],
  P(r"a) \(\frac{36\cdot10}{3}=120\) cm³. b) \(972\pi\approx3053{,}63\) cm³. c) \(\frac{\pi\cdot9\cdot10}{3}=30\pi\approx94{,}25\) mL. d) El triple que el cilindre. e) \(\frac43r^3=36\Rightarrow r^3=27\Rightarrow r=3\) cm; \(A=36\pi\approx113{,}10\) cm².",
    r"a) \(\frac{36\cdot10}{3}=120\) cm³. b) \(972\pi\approx3053{,}63\) cm³. c) \(\frac{\pi\cdot9\cdot10}{3}=30\pi\approx94{,}25\) mL. d) El triple que el cilindro. e) \(\frac43r^3=36\Rightarrow r^3=27\Rightarrow r=3\) cm; \(A=36\pi\approx113{,}10\) cm².",
    r"a) \(\frac{36\cdot10}{3}=120\) cm³. b) \(972\pi\approx3053.63\) cm³. c) \(\frac{\pi\cdot9\cdot10}{3}=30\pi\approx94.25\) mL. d) Three times as tall as the cylinder. e) \(\frac43r^3=36\Rightarrow r^3=27\Rightarrow r=3\) cm; \(A=36\pi\approx113.10\) cm²."))
ck(R(360, 3), 120); ck(R(4, 3) * 729 * pi, 972 * pi); ck(972 * pi, 3053.63, 2); ck(30 * pi, 94.25, 2); ck(36 * pi, 113.10, 2)


# =====================================================================
# 9.8 Cossos compostos i problemes
# =====================================================================
HC = math.cos(math.radians(PH))
SITJA = cylinder(1.4, 2.6, top=False)[0] + shift(cone(1.4, 1.4)[0], 0, 2.6 * HC)
SITJA += [('seg', (0, 0), (1.4, 0), 'ax'), ('txt', (0.7, 0), '2 m', {'dy': -5, 'cls': 'ax'}), ('txt', (1.4, 1.3 * HC), '6 m', {'dx': 8, 'a': 'start'}),
          ('seg', (0, 2.6 * HC), (0, 4 * HC), 'ax'), ('txt', (0, 3.3 * HC), '3 m', {'dx': -6, 'a': 'end', 'cls': 'ax'})]
CAPS = capsule(1.2, 3)[0]
s8 = box('prop', L('Cossos compostos', 'Cuerpos compuestos', 'Composite solids'),
  P(r"Molts objectes són combinacions dels cossos que coneixem. Per a calcular-ne el volum, el <strong>descomponem</strong> en cossos simples i sumem (o restem, si hi ha forats) els volums. Per a l'àrea, sumem només les superfícies que queden <strong>per fora</strong>.",
    r"Muchos objetos son combinaciones de los cuerpos que conocemos. Para calcular su volumen, lo <strong>descomponemos</strong> en cuerpos simples y sumamos (o restamos, si hay agujeros) los volúmenes. Para el área, sumamos solo las superficies que quedan <strong>por fuera</strong>.",
    r"Many objects are combinations of the solids we know. To find their volume, <strong>split</strong> them into simple solids and add the volumes (or subtract, for holes). For the surface area, add only the surfaces that are on the <strong>outside</strong>.")
  + figs(solid(SITJA, W=150, cap=L('Sitja: cilindre + con', 'Silo: cilindro + cono', 'Silo: cylinder + cone')), solid(CAPS, W=120, cap=L('Càpsula: cilindre + esfera', 'Cápsula: cilindro + esfera', 'Capsule: cylinder + sphere')))
  + P(r"Exemple: una sitja és un cilindre de 2 m de radi i 6 m d'altura amb una teulada cònica de 3 m d'altura:",
      r"Ejemplo: un silo es un cilindro de 2 m de radio y 6 m de altura con un tejado cónico de 3 m de altura:",
      r"Example: a silo is a cylinder with a 2 m radius and 6 m height topped by a 3 m tall conical roof:")
  + D(r"V=\pi\cdot2^2\cdot6+\frac{\pi\cdot2^2\cdot3}{3}=24\pi+4\pi=28\pi\approx87{,}96\ \text{m}^3")
  + widget('w-comp', '🏗️', L('Cossos compostos', 'Cuerpos compuestos', 'Composite solids'),
           [seg([('sitja', L('Sitja', 'Silo', 'Silo')), ('caps', L('Càpsula', 'Cápsula', 'Capsule')), ('gelat', L('Gelat', 'Helado', 'Ice-cream cone')), ('forat', L('Cub amb forat', 'Cubo con agujero', 'Cube with a hole'))]),
            '<div class="wrow">' + rng('a', 1, 10, 0.5, 2, 'a') + rng('b', 1, 15, 0.5, 6, 'b') + '</div>'],
           out='<div class="gout"></div><div class="hsteps"></div>')
  + drill('comp', 'Entrena: cossos compostos', 'Entrena: cuerpos compuestos', 'Train: composite solids'))
ck(28 * pi, 87.96, 2)
s8 += levels(
 [prob(L(r"Un gelat és un con de 2 cm de radi i 9 cm d'altura, ple de gelat, amb una semiesfera de gelat al damunt. Quin volum de gelat hi ha?", r"Un helado es un cono de 2 cm de radio y 9 cm de altura, lleno de helado, con una semiesfera de helado encima. ¿Qué volumen de helado hay?", r"An ice-cream cone is a cone with a 2 cm radius and 9 cm height, full of ice cream, with a hemisphere of ice cream on top. What volume of ice cream is there?"),
       D(r"V=\frac{\pi\cdot4\cdot9}{3}+\frac12\cdot\frac43\pi\cdot8=12\pi+\frac{16\pi}{3}=\frac{52\pi}{3}\approx\boxed{54{,}45\ \text{cm}^3}"))],
 [prob(L(r"Un cub de fusta de 8 cm d'aresta té un forat cilíndric d'1 cm de radi que el travessa de dalt a baix. Quin volum de fusta té? Quina és la seua àrea total (comptant l'interior del forat)?", r"Un cubo de madera de 8 cm de arista tiene un agujero cilíndrico de 1 cm de radio que lo atraviesa de arriba abajo. ¿Qué volumen de madera tiene? ¿Cuál es su área total (contando el interior del agujero)?", r"An 8 cm wooden cube has a cylindrical hole with a 1 cm radius going right through it from top to bottom. What volume of wood does it have? What is its total surface area (including the inside of the hole)?"),
       D(r"V=8^3-\pi\cdot1^2\cdot8=512-8\pi\approx\boxed{486{,}87\ \text{cm}^3}"),
       P(r"A l'àrea del cub li llevem els dos cercles del forat i li sumem la paret del forat (l'àrea lateral d'un cilindre):", r"Al área del cubo le quitamos los dos círculos del agujero y le sumamos la pared del agujero (el área lateral de un cilindro):", r"From the cube's area we remove the two discs of the hole and add the wall of the hole (the lateral area of a cylinder):"),
       D(r"A=6\cdot64-2\pi\cdot1^2+2\pi\cdot1\cdot8=384-2\pi+16\pi=384+14\pi\approx\boxed{427{,}98\ \text{cm}^2}"))],
 [prob(L(r"Un dipòsit de gas és un cilindre de 2 m de diàmetre i 6 m de llarg amb una semiesfera a cada extrem. Quants litres hi caben? Si amb 1 L de pintura pintem 8 m², quanta pintura cal per a pintar-lo per fora?", r"Un depósito de gas es un cilindro de 2 m de diámetro y 6 m de largo con una semiesfera en cada extremo. ¿Cuántos litros caben? Si con 1 L de pintura pintamos 8 m², ¿cuánta pintura hace falta para pintarlo por fuera?", r"A gas tank is a cylinder 2 m across and 6 m long with a hemisphere at each end. How many litres does it hold? If 1 L of paint covers 8 m², how much paint is needed to paint its outside?"),
       P(r"Les dues semiesferes formen una esfera sencera de radi 1 m:", r"Las dos semiesferas forman una esfera entera de radio 1 m:", r"The two hemispheres make a whole sphere with a 1 m radius:"),
       D(r"V=\pi\cdot1^2\cdot6+\frac43\pi\cdot1^3=6\pi+\frac{4\pi}{3}=\frac{22\pi}{3}\approx23{,}04\ \text{m}^3\approx\boxed{23\,038\ \text{L}}"),
       D(r"A=2\pi\cdot1\cdot6+4\pi\cdot1^2=16\pi\approx50{,}27\ \text{m}^2\qquad\frac{50{,}27}{8}\approx\boxed{6{,}28\ \text{L}}"))])
ck(12 * pi + R(16, 3) * pi, R(52, 3) * pi); ck(R(52, 3) * pi, 54.45, 2); ck(512 - 8 * pi, 486.87, 2); ck(384 + 14 * pi, 427.98, 2)
ck(R(22, 3) * pi, 23.04, 2); ck(R(22000, 3) * pi, 23038, 0); ck(16 * pi, 50.27, 2); ck(R(5027, 100) / 8, 6.28, 2)
s8 += practice([
  ('★', L(r"a) Una peça és un cub de 6 cm d'aresta amb una piràmide de 4 cm d'altura al damunt, de la mateixa base. Calcula'n el volum.", r"a) Una pieza es un cubo de 6 cm de arista con una pirámide de 4 cm de altura encima, de la misma base. Calcula su volumen.", r"a) A piece is a 6 cm cube with a 4 cm tall pyramid on top, with the same base. Find its volume.")),
  ('★★', L(r"b) Una torre és un cilindre de 2 m de radi i 5 m d'altura amb una teulada cònica de 3 m d'altura. Quin volum té? c) Un tub cilíndric té 5 cm de radi exterior, 4 cm de radi interior i 1 m de llarg. Quin volum de material té?", r"b) Una torre es un cilindro de 2 m de radio y 5 m de altura con un tejado cónico de 3 m de altura. ¿Qué volumen tiene? c) Un tubo cilíndrico tiene 5 cm de radio exterior, 4 cm de radio interior y 1 m de largo. ¿Qué volumen de material tiene?", r"b) A tower is a cylinder with a 2 m radius and 5 m height with a 3 m tall conical roof. What is its volume? c) A cylindrical pipe has a 5 cm outer radius, a 4 cm inner radius and is 1 m long. What volume of material does it have?")),
  ('★★★', L(r"d) Deixem caure una bola d'acer de 2 cm de radi dins d'un got cilíndric de 4 cm de radi amb aigua. Quant puja el nivell de l'aigua?", r"d) Dejamos caer una bola de acero de 2 cm de radio dentro de un vaso cilíndrico de 4 cm de radio con agua. ¿Cuánto sube el nivel del agua?", r"d) We drop a steel ball with a 2 cm radius into a cylindrical glass of water with a 4 cm radius. How much does the water level rise?"))],
  P(r"a) \(216+\frac{36\cdot4}{3}=264\) cm³. b) \(20\pi+4\pi=24\pi\approx75{,}40\) m³. c) \(\pi(25-16)\cdot100=900\pi\approx2827{,}43\) cm³. d) L'aigua puja el volum de la bola: \(16\pi h=\frac{32\pi}{3}\Rightarrow h=\frac23\approx0{,}67\) cm.",
    r"a) \(216+\frac{36\cdot4}{3}=264\) cm³. b) \(20\pi+4\pi=24\pi\approx75{,}40\) m³. c) \(\pi(25-16)\cdot100=900\pi\approx2827{,}43\) cm³. d) El agua sube el volumen de la bola: \(16\pi h=\frac{32\pi}{3}\Rightarrow h=\frac23\approx0{,}67\) cm.",
    r"a) \(216+\frac{36\cdot4}{3}=264\) cm³. b) \(20\pi+4\pi=24\pi\approx75.40\) m³. c) \(\pi(25-16)\cdot100=900\pi\approx2827.43\) cm³. d) The water rises by the ball's volume: \(16\pi h=\frac{32\pi}{3}\Rightarrow h=\frac23\approx0.67\) cm."))
ck(216 + 48, 264); ck(24 * pi, 75.40, 2); ck(900 * pi, 2827.43, 2); ck(R(32, 3) / 16, R(2, 3)); ck(R(2, 3), 0.67, 2)
