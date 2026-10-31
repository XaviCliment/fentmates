# 11.7 Volum de piràmides, cons i esferes · 11.8 Cossos compostos i problemes
from comu import *
from fig11 import *

def solid(it, W=200, cap=None, maxh=210, pad=18): return G(it, W=W, cap=cap, maxh=maxh, pad=pad)

# =====================================================================
# 11.7 Volum de piràmides, cons i esferes
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
 [prob(L(r"Calcula el volum d'un con de 5 cm de radi i 12 cm d'altura i el d'una esfera de 3 cm de radi.", r"Calcula el volumen de un cono de 5 cm de radio y 12 cm de altura y el de una esfera de 3 cm de radio.", r"Find the volume of a cone with a 5 cm radius and 12 cm height, and of a sphere with a 3 cm radius."),
       D(r"V=\frac{\pi\cdot25\cdot12}{3}=100\pi\approx\boxed{314{,}16\ \text{cm}^3}\qquad V=\frac43\pi\cdot27=36\pi\approx\boxed{113{,}10\ \text{cm}^3}"))],
 [prob(L(r"Una piràmide hexagonal regular té 6 cm d'aresta de la base i 10 cm d'altura. Calcula'n el volum.", r"Una pirámide hexagonal regular tiene 6 cm de arista de la base y 10 cm de altura. Calcula su volumen.", r"A regular hexagonal pyramid has 6 cm base edges and is 10 cm tall. Find its volume."),
       D(r"a_b=\sqrt{6^2-3^2}=\sqrt{27}\qquad A_{\text{base}}=\frac{36\cdot\sqrt{27}}{2}\approx93{,}53\ \text{cm}^2"),
       D(r"V=\frac{A_{\text{base}}\cdot h}{3}\approx\frac{93{,}53\cdot10}{3}\approx\boxed{311{,}77\ \text{cm}^3}"))],
 [prob(L(r"Un con té 13 cm de generatriu i 5 cm de radi. Calcula'n el volum. Quin radi ha de tenir una esfera perquè tinga el mateix volum?", r"Un cono tiene 13 cm de generatriz y 5 cm de radio. Calcula su volumen. ¿Qué radio debe tener una esfera para tener el mismo volumen?", r"A cone has a 13 cm slant height and a 5 cm radius. Find its volume. What radius must a sphere have to have the same volume?"),
       D(r"h=\sqrt{13^2-5^2}=12\qquad V=\frac{\pi\cdot25\cdot12}{3}=100\pi\approx\boxed{314{,}16\ \text{cm}^3}"),
       D(r"\frac43\pi R^3=100\pi\ \Rightarrow\ R^3=75\ \Rightarrow\ R=\sqrt[3]{75}\approx\boxed{4{,}22\ \text{cm}}"))])
ck(100 * pi, 314.16, 2); ck(36 * pi, 113.10, 2); ck(18 * S(27), 93.53, 2); ck(60 * S(27), 311.77, 2); ck(leg(13, 5), 12); ck(75 ** (1 / 3.0), 4.22, 2)
s7 += practice([
  ('★', L(r"a) Calcula el volum d'una piràmide quadrangular de 9 cm d'aresta de la base i 8 cm d'altura. b) I el d'una esfera de 6 cm de radi.", r"a) Calcula el volumen de una pirámide cuadrangular de 9 cm de arista de la base y 8 cm de altura. b) Y el de una esfera de 6 cm de radio.", r"a) Find the volume of a square pyramid with 9 cm base edges and 8 cm height. b) And of a sphere with a 6 cm radius.")),
  ('★★', L(r"c) Un cucurutxo cònic fa 4 cm de diàmetre i 12 cm d'altura. Quants mL de gelat hi caben (sense sobreeixir)? d) Un con i un cilindre tenen la mateixa base. Quina altura ha de tenir el con perquè tinguen el mateix volum?", r"c) Un cucurucho cónico mide 4 cm de diámetro y 12 cm de altura. ¿Cuántos mL de helado caben (sin rebosar)? d) Un cono y un cilindro tienen la misma base. ¿Qué altura debe tener el cono para que tengan el mismo volumen?", r"c) A cone-shaped wafer is 4 cm across and 12 cm tall. How many mL of ice cream fit inside (level)? d) A cone and a cylinder have the same base. How tall must the cone be to have the same volume?")),
  ('★★★', L(r"e) Una esfera té 288π cm³ de volum. Quin radi té? Quina és la seua àrea?", r"e) Una esfera tiene 288π cm³ de volumen. ¿Qué radio tiene? ¿Cuál es su área?", r"e) A sphere has a volume of 288π cm³. What is its radius? What is its surface area?"))],
  P(r"a) \(\frac{81\cdot8}{3}=216\) cm³. b) \(288\pi\approx904{,}78\) cm³. c) \(\frac{\pi\cdot4\cdot12}{3}=16\pi\approx50{,}27\) mL. d) El triple que el cilindre. e) \(\frac43r^3=288\Rightarrow r^3=216\Rightarrow r=6\) cm; \(A=144\pi\approx452{,}39\) cm².",
    r"a) \(\frac{81\cdot8}{3}=216\) cm³. b) \(288\pi\approx904{,}78\) cm³. c) \(\frac{\pi\cdot4\cdot12}{3}=16\pi\approx50{,}27\) mL. d) El triple que el cilindro. e) \(\frac43r^3=288\Rightarrow r^3=216\Rightarrow r=6\) cm; \(A=144\pi\approx452{,}39\) cm².",
    r"a) \(\frac{81\cdot8}{3}=216\) cm³. b) \(288\pi\approx904.78\) cm³. c) \(\frac{\pi\cdot4\cdot12}{3}=16\pi\approx50.27\) mL. d) Three times as tall as the cylinder. e) \(\frac43r^3=288\Rightarrow r^3=216\Rightarrow r=6\) cm; \(A=144\pi\approx452.39\) cm²."))
ck(R(81 * 8, 3), 216); ck(288 * pi, 904.78, 2); ck(16 * pi, 50.27, 2); ck(144 * pi, 452.39, 2)

# =====================================================================
# 11.8 Cossos compostos i problemes
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
  + P(r"Un <strong>tronc de con</strong> (com un got o un cubell) és la diferència entre dos cons, el gran i el que llevem per dalt.",
      r"Un <strong>tronco de cono</strong> (como un vaso o un cubo) es la diferencia entre dos conos, el grande y el que quitamos por arriba.",
      r"A <strong>conical frustum</strong> (like a cup or a bucket) is the difference between two cones: the big one and the one removed from the top.")
  + widget('w-comp', '🏗️', L('Cossos compostos', 'Cuerpos compuestos', 'Composite solids'),
           [seg([('sitja', L('Sitja', 'Silo', 'Silo')), ('caps', L('Càpsula', 'Cápsula', 'Capsule')), ('gelat', L('Gelat', 'Helado', 'Ice-cream cone')), ('forat', L('Cub amb forat', 'Cubo con agujero', 'Cube with a hole'))]),
            '<div class="wrow">' + rng('a', 1, 10, 0.5, 2, 'a') + rng('b', 1, 15, 0.5, 6, 'b') + '</div>'],
           out='<div class="gout"></div><div class="hsteps"></div>')
  + drill('comp', 'Entrena: cossos compostos', 'Entrena: cuerpos compuestos', 'Train: composite solids'))
ck(28 * pi, 87.96, 2)
s8 += levels(
 [prob(L(r"Un gelat és un con de 3 cm de radi i 10 cm d'altura amb una semiesfera de gelat al damunt. Quin volum de gelat hi ha si el con també està ple?", r"Un helado es un cono de 3 cm de radio y 10 cm de altura con una semiesfera de helado encima. ¿Qué volumen de helado hay si el cono también está lleno?", r"An ice-cream cone is a cone with a 3 cm radius and 10 cm height with a hemisphere of ice cream on top. What volume of ice cream is there if the cone is full too?"),
       D(r"V=\frac{\pi\cdot9\cdot10}{3}+\frac12\cdot\frac43\pi\cdot27=30\pi+18\pi=48\pi\approx\boxed{150{,}80\ \text{cm}^3}"))],
 [prob(L(r"Un cub de fusta de 10 cm d'aresta té un forat cilíndric que el travessa, de 2 cm de radi. Quin volum de fusta té? Quina és la seua àrea total (comptant l'interior del forat)?", r"Un cubo de madera de 10 cm de arista tiene un agujero cilíndrico que lo atraviesa, de 2 cm de radio. ¿Qué volumen de madera tiene? ¿Cuál es su área total (contando el interior del agujero)?", r"A 10 cm wooden cube has a cylindrical hole with a 2 cm radius right through it. What volume of wood does it have? What is its total surface area (including inside the hole)?"),
       D(r"V=10^3-\pi\cdot2^2\cdot10=1000-40\pi\approx\boxed{874{,}34\ \text{cm}^3}"),
       D(r"A=6\cdot100-2\cdot\pi\cdot2^2+2\pi\cdot2\cdot10=600-8\pi+40\pi=600+32\pi\approx\boxed{700{,}53\ \text{cm}^2}"))],
 [prob(L(r"Un cubell té forma de tronc de con: el fons fa 10 cm de radi, la boca 15 cm de radi i l'altura és de 20 cm. Quants litres hi caben? (Pista: és un con gran al qual llevem un con menut; fes servir Tales.)", r"Un cubo tiene forma de tronco de cono: el fondo mide 10 cm de radio, la boca 15 cm de radio y la altura es de 20 cm. ¿Cuántos litros caben? (Pista: es un cono grande al que le quitamos un cono pequeño; usa Tales.)", r"A bucket is a conical frustum: the bottom has a 10 cm radius, the top a 15 cm radius and it's 20 cm tall. How many litres does it hold? (Hint: it's a big cone minus a small one; use Thales.)"),
       P(r"Si allarguem les parets fins al vèrtex, el con menut (radi 10, altura \(x\)) i el gran (radi 15, altura \(x+20\)) estan en posició de Tales:", r"Si alargamos las paredes hasta el vértice, el cono pequeño (radio 10, altura \(x\)) y el grande (radio 15, altura \(x+20\)) están en posición de Tales:", r"Extending the sides to the apex, the small cone (radius 10, height \(x\)) and the big one (radius 15, height \(x+20\)) are in Thales position:"),
       D(r"\frac{x}{10}=\frac{x+20}{15}\ \Rightarrow\ 15x=10x+200\ \Rightarrow\ x=40"),
       D(r"V=\frac{\pi\cdot15^2\cdot60}{3}-\frac{\pi\cdot10^2\cdot40}{3}=4500\pi-\frac{4000\pi}{3}=\frac{9500\pi}{3}\approx9948{,}38\ \text{cm}^3\approx\boxed{9{,}95\ \text{L}}"))])
ck(48 * pi, 150.80, 2); ck(1000 - 40 * pi, 874.34, 2); ck(600 + 32 * pi, 700.53, 2); x_ = sp.Symbol('x'); assert sp.solve(15 * x_ - 10 * (x_ + 20), x_) == [40]
ck(4500 * pi - R(4000, 3) * pi, R(9500, 3) * pi); ck(R(9500, 3) * pi, 9948.38, 2); ck(R(9500, 3) * pi / 1000, 9.95, 2)
s8 += practice([
  ('★', L(r"a) Una peça és un cub de 4 cm d'aresta amb una piràmide de 3 cm d'altura al damunt, de la mateixa base. Calcula'n el volum.", r"a) Una pieza es un cubo de 4 cm de arista con una pirámide de 3 cm de altura encima, de la misma base. Calcula su volumen.", r"a) A piece is a 4 cm cube with a 3 cm tall pyramid on top, with the same base. Find its volume.")),
  ('★★', L(r"b) Una càpsula és un cilindre de 1 cm de radi i 3 cm de llarg amb dues semiesferes als extrems. Calcula'n el volum i l'àrea. c) Un tub cilíndric té 10 cm de radi exterior, 8 cm de radi interior i 2 m de llarg. Quin volum de material té?", r"b) Una cápsula es un cilindro de 1 cm de radio y 3 cm de largo con dos semiesferas en los extremos. Calcula su volumen y su área. c) Un tubo cilíndrico tiene 10 cm de radio exterior, 8 cm de radio interior y 2 m de largo. ¿Qué volumen de material tiene?", r"b) A capsule is a cylinder with a 1 cm radius and 3 cm length with two hemispheres at the ends. Find its volume and area. c) A pipe has a 10 cm outer radius, an 8 cm inner radius and is 2 m long. What volume of material does it have?")),
  ('★★★', L(r"d) Una bola d'acer de 3 cm de radi es deixa caure en un got cilíndric de 5 cm de radi amb aigua. Quant puja el nivell de l'aigua?", r"d) Una bola de acero de 3 cm de radio se deja caer en un vaso cilíndrico de 5 cm de radio con agua. ¿Cuánto sube el nivel del agua?", r"d) A steel ball with a 3 cm radius is dropped into a cylindrical glass of water with a 5 cm radius. How much does the water level rise?"))],
  P(r"a) \(64+\frac{16\cdot3}{3}=80\) cm³. b) \(V=3\pi+\frac43\pi=\frac{13\pi}{3}\approx13{,}61\) cm³; \(A=6\pi+4\pi=10\pi\approx31{,}42\) cm². c) \(\pi(100-64)\cdot200=7200\pi\approx22\,619{,}47\) cm³. d) \(25\pi h=36\pi\Rightarrow h=1{,}44\) cm.",
    r"a) \(64+\frac{16\cdot3}{3}=80\) cm³. b) \(V=3\pi+\frac43\pi=\frac{13\pi}{3}\approx13{,}61\) cm³; \(A=6\pi+4\pi=10\pi\approx31{,}42\) cm². c) \(\pi(100-64)\cdot200=7200\pi\approx22\,619{,}47\) cm³. d) \(25\pi h=36\pi\Rightarrow h=1{,}44\) cm.",
    r"a) \(64+\frac{16\cdot3}{3}=80\) cm³. b) \(V=3\pi+\frac43\pi=\frac{13\pi}{3}\approx13.61\) cm³; \(A=6\pi+4\pi=10\pi\approx31.42\) cm². c) \(\pi(100-64)\cdot200=7200\pi\approx22\,619.47\) cm³. d) \(25\pi h=36\pi\Rightarrow h=1.44\) cm."))
ck(64 + 16, 80); ck(R(13, 3) * pi, 13.61, 2); ck(10 * pi, 31.42, 2); ck(7200 * pi, 22619.47, 2); ck(R(36, 25), 1.44)
