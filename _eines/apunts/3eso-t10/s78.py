# 10.7 Aplicacions de la semblança: altures i distàncies · 10.8 Escales. Àrees i volums de figures semblants
from comu import *
from fig10 import *

# =====================================================================
# 10.7 Aplicacions de la semblança: altures i distàncies
# =====================================================================
s7 = box('prop', L('Altures amb ombres', 'Alturas con sombras', 'Heights from shadows'),
  P(r"Els rajos del Sol arriben pràcticament <strong>paral·lels</strong>. Al mateix moment, un pal vertical i un edifici formen amb les seues ombres dos triangles rectangles amb els mateixos angles: són <strong>semblants</strong>. Per tant, l'altura i l'ombra són proporcionals:",
    r"Los rayos del Sol llegan prácticamente <strong>paralelos</strong>. En el mismo momento, un palo vertical y un edificio forman con sus sombras dos triángulos rectángulos con los mismos ángulos: son <strong>semejantes</strong>. Por tanto, la altura y la sombra son proporcionales:",
    r"The Sun's rays arrive practically <strong>parallel</strong>. At the same moment, a vertical stick and a building form two right triangles with their shadows that have the same angles: they are <strong>similar</strong>. So height and shadow are proportional:")
  + D(r"\frac{h_{\text{%s}}}{s_{\text{%s}}}=\frac{H_{\text{%s}}}{S_{\text{%s}}}" % (Lt('pal', 'palo', 'stick'), Lt('pal', 'palo', 'stick'), Lt('edifici', 'edificio', 'building'), Lt('edifici', 'edificio', 'building')))
  + figs(G(shadow(1.5, 2, 9, 12, '1,5 m', 'H', '2 m', '12 m', hot='h2'), W=320, pad=26))
  + D(r"\frac{1{,}5}{2}=\frac{H}{12}\ \Rightarrow\ H=\frac{1{,}5\cdot12}{2}=9\ \text{m}")
  + note(r"Diuen que Tales de Milet (segle VI aC) va calcular així l'altura de la gran piràmide d'Egipte: va esperar el moment en què la seua ombra feia el mateix que la seua altura. En aquell moment, l'ombra de la piràmide també mesurava el mateix que la piràmide.",
         r"Dicen que Tales de Mileto (siglo VI a. C.) calculó así la altura de la gran pirámide de Egipto: esperó el momento en que su sombra medía lo mismo que su altura. En ese momento, la sombra de la pirámide también medía lo mismo que la pirámide.",
         r"Thales of Miletus (6th century BC) is said to have found the height of the Great Pyramid this way: he waited for the moment when his own shadow was as long as he was tall. At that moment, the pyramid's shadow was also as long as the pyramid was tall.", '🏛️')
  + widget('w-ombra', '☀️', L('Calcula una altura amb les ombres', 'Calcula una altura con las sombras', 'Find a height from shadows'),
           ['<div class="wrow">' + rng('h', 0.5, 3, 0.1, 1.5, 'h') + rng('s', 0.5, 5, 0.1, 2, 's') + '</div>',
            '<div class="wrow">' + rng('S', 2, 30, 0.5, 12, 'S') + '</div>'])
  + drill('ombra', 'Entrena: altures i ombres', 'Entrena: alturas y sombras', 'Train: heights and shadows'))
ck(R(15, 10) * 12 / 2, 9)
MIR = G([('seg', (-0.5, 0), (12, 0), 'axis'), ('seg', (0, 0), (0, 1.6), 'wall'), ('seg', (11, 0), (11, 7.2), 'wall'),
         ('seg', (0, 1.6), (2, 0), 'ray'), ('seg', (2, 0), (11, 7.2), 'ray'), ('poly', [(0, 0), (0, 1.6), (2, 0)], 'tr'), ('poly', [(2, 0), (11, 0), (11, 7.2)], 'gf'),
         ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (11, 0), (10, 0), (11, 1)), ('dot', (2, 0), 'pa'),
         ('txt', (0, 0.8), '1,6 m', {'dx': -8, 'a': 'end'}), ('txt', (1, 0), '2 m', {'dy': 15}), ('txt', (6.5, 0), '9 m', {'dy': 15}), ('txt', (11, 3.6), 'H', {'dx': 8, 'a': 'start', 'cls': 'hot'}),
         ('txt', (2, 0), Ls('mirall', 'espejo', 'mirror'), {'dy': -10})], W=300, pad=26)
s7 += box('prop', L('Altures i distàncies amb un mirall o una estaca', 'Alturas y distancias con un espejo o una estaca', 'Heights and distances with a mirror or a stake'),
  P(r"<strong>Mirall:</strong> posem un mirall a terra i ens allunyem fins que hi veiem la punta de l'arbre. Com que el raig de llum es reflecteix amb el mateix angle amb què arriba, els dos triangles rectangles són semblants:",
    r"<strong>Espejo:</strong> ponemos un espejo en el suelo y nos alejamos hasta que vemos en él la punta del árbol. Como el rayo de luz se refleja con el mismo ángulo con que llega, los dos triángulos rectángulos son semejantes:",
    r"<strong>Mirror:</strong> put a mirror on the ground and step back until you see the top of the tree in it. Since light is reflected at the same angle at which it arrives, the two right triangles are similar:")
  + figs(MIR)
  + D(r"\frac{H}{9}=\frac{1{,}6}{2}\ \Rightarrow\ H=\frac{9\cdot1{,}6}{2}=7{,}2\ \text{m}")
  + P(r"<strong>Estaca o regle:</strong> si alineem la vista amb la punta d'una estaca i la d'un objecte llunyà, també es formen dos triangles en posició de Tales. En tots aquests mètodes la clau és la mateixa: <strong>trobar dos triangles semblants</strong> i escriure la proporció entre costats homòlegs.",
      r"<strong>Estaca o regla:</strong> si alineamos la vista con la punta de una estaca y la de un objeto lejano, también se forman dos triángulos en posición de Tales. En todos estos métodos la clave es la misma: <strong>encontrar dos triángulos semejantes</strong> y escribir la proporción entre lados homólogos.",
      r"<strong>Stake or ruler:</strong> lining up your eye with the top of a stake and the top of a distant object also gives two triangles in Thales position. In all these methods the key is the same: <strong>find two similar triangles</strong> and write the proportion between corresponding sides."))
ck(R(9) * R(16, 10) / 2, 7.2)
s7 += levels(
 [prob(L(r"Un arbre fa una ombra de 6 m. Al mateix moment, una persona d'1,7 m fa una ombra d'1,2 m. Quina altura té l'arbre?", r"Un árbol da una sombra de 6 m. En el mismo momento, una persona de 1,7 m da una sombra de 1,2 m. ¿Qué altura tiene el árbol?", r"A tree casts a 6 m shadow. At the same moment, a 1.7 m tall person casts a 1.2 m shadow. How tall is the tree?"),
       D(r"\frac{H}{6}=\frac{1{,}7}{1{,}2}\ \Rightarrow\ H=\frac{6\cdot1{,}7}{1{,}2}=\boxed{8{,}5\ \text{m}}"))],
 [prob(L(r"La Laia (els ulls a 1,5 m de terra) posa un mirall a terra a 1,2 m d'ella i a 8 m de la base d'una paret. Quan mira el mirall hi veu just el capdamunt de la paret. Quina altura té la paret?", r"Laia (los ojos a 1,5 m del suelo) pone un espejo en el suelo a 1,2 m de ella y a 8 m de la base de una pared. Cuando mira el espejo ve justo lo alto de la pared. ¿Qué altura tiene la pared?", r"Laia (eyes 1.5 m above the ground) puts a mirror on the ground 1.2 m from her and 8 m from the foot of a wall. Looking into it she sees exactly the top of the wall. How high is the wall?"),
       D(r"\frac{H}{8}=\frac{1{,}5}{1{,}2}\ \Rightarrow\ H=\frac{8\cdot1{,}5}{1{,}2}=\boxed{10\ \text{m}}"))],
 [prob(L(r"Una persona d'1,8 m està a 4 m d'un fanal de 6 m d'altura. Quant fa la seua ombra?", r"Una persona de 1,8 m está a 4 m de una farola de 6 m de altura. ¿Cuánto mide su sombra?", r"A 1.8 m tall person stands 4 m from a 6 m street lamp. How long is their shadow?"),
       P(r"Ara la llum ix d'un punt (la bombeta): el raig que passa pel cap de la persona forma dos triangles en posició de Tales. Si l'ombra fa \(s\):", r"Ahora la luz sale de un punto (la bombilla): el rayo que pasa por la cabeza de la persona forma dos triángulos en posición de Tales. Si la sombra mide \(s\):", r"Now the light comes from a point (the bulb): the ray through the person's head forms two triangles in Thales position. If the shadow is \(s\):")
       + figs(G([('seg', (-0.5, 0), (6.6, 0), 'axis'), ('poly', [(0, 0), (0, 6), (40 / 7, 0)], 'gf'), ('poly', [(4, 0), (4, 1.8), (40 / 7, 0)], 'tr'), ('seg', (0, 0), (0, 6), 'wall'), ('seg', (4, 0), (4, 1.8), 'wall'),
                 ('seg', (0, 6), (40 / 7, 0), 'ray'), ('dot', (0, 6), 'pa'), ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (4, 0), (5, 0), (4, 1)),
                 ('txt', (0, 3), '6 m', {'dx': -8, 'a': 'end'}), ('txt', (4, 0.9), '1,8', {'dx': -6, 'a': 'end'}), ('txt', (2, 0), '4 m', {'dy': 15}), ('txt', (4 + 6 / 7, 0), 's', {'dy': 15, 'cls': 'hot'})], W=260, pad=26)),
       D(r"\frac{1{,}8}{s}=\frac{6}{s+4}\ \Rightarrow\ 1{,}8(s+4)=6s\ \Rightarrow\ 7{,}2=4{,}2s\ \Rightarrow\ s=\frac{7{,}2}{4{,}2}\approx\boxed{1{,}71\ \text{m}}"))])
ck(R(6) * R(17, 10) / R(12, 10), 8.5); ck(R(8) * R(15, 10) / R(12, 10), 10); ck(R(72, 42), 1.71, 2)
s7 += practice([
  ('★', L(r"a) Un pal d'1 m fa una ombra de 0,8 m. Quina altura té una torre que fa una ombra de 20 m?", r"a) Un palo de 1 m da una sombra de 0,8 m. ¿Qué altura tiene una torre que da una sombra de 20 m?", r"a) A 1 m stick casts a 0.8 m shadow. How tall is a tower that casts a 20 m shadow?")),
  ('★★', L(r"b) Un edifici de 15 m fa una ombra de 10 m. Quina ombra fa al mateix moment un arbre de 4,5 m? c) Tenim els ulls a 1,6 m de terra i, amb un mirall a 1,5 m de nosaltres, veiem la punta d'un pi que està a 6 m del mirall. Quina altura té el pi?", r"b) Un edificio de 15 m da una sombra de 10 m. ¿Qué sombra da en el mismo momento un árbol de 4,5 m? c) Tenemos los ojos a 1,6 m del suelo y, con un espejo a 1,5 m de nosotros, vemos la punta de un pino que está a 6 m del espejo. ¿Qué altura tiene el pino?", r"b) A 15 m building casts a 10 m shadow. What shadow does a 4.5 m tree cast at the same moment? c) Our eyes are 1.6 m above the ground and, with a mirror 1.5 m from us, we see the top of a pine 6 m from the mirror. How tall is the pine?")),
  ('★★★', L(r"d) Per a saber l'amplària d'un riu, des d'un punt veiem alineats un arbre de l'altra riba i la punta d'un regle vertical de 30 cm que tenim a 50 cm dels ulls. L'arbre fa 12 m d'altura i el veiem just de la mateixa altura que el regle. A quina distància està l'arbre?", r"d) Para saber la anchura de un río, desde un punto vemos alineados un árbol de la otra orilla y la punta de una regla vertical de 30 cm que tenemos a 50 cm de los ojos. El árbol mide 12 m de altura y lo vemos justo de la misma altura que la regla. ¿A qué distancia está el árbol?", r"d) To find a river's width, we hold a 30 cm vertical ruler 50 cm from our eyes and see that it exactly covers a 12 m tall tree on the other bank. How far away is the tree?"))],
  P(r"a) \(\frac{H}{20}=\frac{1}{0{,}8}\Rightarrow H=25\) m. b) \(\frac{4{,}5}{s}=\frac{15}{10}\Rightarrow s=3\) m. c) \(H=\frac{6\cdot1{,}6}{1{,}5}=6{,}4\) m. d) \(\frac{d}{12}=\frac{0{,}5}{0{,}3}\Rightarrow d=20\) m.",
    r"a) \(\frac{H}{20}=\frac{1}{0{,}8}\Rightarrow H=25\) m. b) \(\frac{4{,}5}{s}=\frac{15}{10}\Rightarrow s=3\) m. c) \(H=\frac{6\cdot1{,}6}{1{,}5}=6{,}4\) m. d) \(\frac{d}{12}=\frac{0{,}5}{0{,}3}\Rightarrow d=20\) m.",
    r"a) \(\frac{H}{20}=\frac{1}{0.8}\Rightarrow H=25\) m. b) \(\frac{4.5}{s}=\frac{15}{10}\Rightarrow s=3\) m. c) \(H=\frac{6\cdot1.6}{1.5}=6.4\) m. d) \(\frac{d}{12}=\frac{0.5}{0.3}\Rightarrow d=20\) m."))
ck(R(20) / R(8, 10), 25); ck(R(45, 10) * 10 / 15, 3); ck(R(6) * R(16, 10) / R(15, 10), 6.4); ck(R(12) * R(5, 10) / R(3, 10), 20)

# =====================================================================
# 10.8 Escales. Àrees i volums de figures semblants
# =====================================================================
s8 = box('def', L("L'escala d'un plànol o d'un mapa", 'La escala de un plano o de un mapa', 'The scale of a plan or a map'),
  P(r"Un plànol, un mapa o una maqueta són figures <strong>semblants</strong> a la realitat. L'<strong>escala</strong> és la raó entre una longitud del dibuix i la longitud real corresponent, en la mateixa unitat:",
    r"Un plano, un mapa o una maqueta son figuras <strong>semejantes</strong> a la realidad. La <strong>escala</strong> es la razón entre una longitud del dibujo y la longitud real correspondiente, en la misma unidad:",
    r"A plan, a map or a scale model is <strong>similar</strong> to reality. The <strong>scale</strong> is the ratio between a length on the drawing and the corresponding real length, in the same unit:")
  + D(r"\text{%s}=\frac{\text{%s}}{\text{%s}}\qquad 1:50\,000\ \ \Rightarrow\ \ 1\ \text{cm}\ \text{%s}\ \to\ 50\,000\ \text{cm}=500\ \text{m}" % (Lt('escala', 'escala', 'scale'), Lt('mesura en el plànol', 'medida en el plano', 'length on the map'), Lt('mesura real', 'medida real', 'real length'), Lt('del mapa', 'del mapa', 'on the map')))
  + ul(L(r"<strong>Escala numèrica</strong> \(1:n\): 1 unitat del plànol representa \(n\) unitats reals. Plànols de cases: 1:50, 1:100; mapes de carreteres: 1:200 000…", r"<strong>Escala numérica</strong> \(1:n\): 1 unidad del plano representa \(n\) unidades reales. Planos de casas: 1:50, 1:100; mapas de carreteras: 1:200 000…", r"<strong>Numerical scale</strong> \(1:n\): 1 unit on the plan stands for \(n\) real units. House plans: 1:50, 1:100; road maps: 1:200 000…"),
       L(r"<strong>Escala gràfica</strong>: un segment dibuixat amb la distància real que representa.", r"<strong>Escala gráfica</strong>: un segmento dibujado con la distancia real que representa.", r"<strong>Graphic scale</strong>: a drawn segment labelled with the real distance it represents."))
  + P(r"Real = plànol \(\times\,n\); plànol = real \(:\,n\). Al final, passa el resultat a una unitat adequada (m o km).",
      r"Real = plano \(\times\,n\); plano = real \(:\,n\). Al final, pasa el resultado a una unidad adecuada (m o km).",
      r"Real = map \(\times\,n\); map = real \(\div\,n\). Finally, convert the result to a sensible unit (m or km).")
  + widget('w-escala', '🗺️', L("Calculadora d'escales", 'Calculadora de escalas', 'Scale calculator'),
           [seg([('r', L('Del plànol a la realitat', 'Del plano a la realidad', 'From map to reality')), ('p', L('De la realitat al plànol', 'De la realidad al plano', 'From reality to map')), ('e', L("Calcula l'escala", 'Calcula la escala', 'Find the scale'))]),
            '<div class="wrow">' + tin('n', L('Escala 1 :', 'Escala 1 :', 'Scale 1 :'), '50000', 'm') + tin('p', L('Plànol (cm) =', 'Plano (cm) =', 'Map (cm) ='), '4,2') + tin('r', L('Real (km) =', 'Real (km) =', 'Real (km) ='), '') + '</div>'],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('escala', 'Entrena: escales', 'Entrena: escalas', 'Train: scales'))
ck(R(42, 10) * 50000 / 100000, 2.1)
s8 += box('prop', L('Raó de les àrees i dels volums', 'Razón de las áreas y de los volúmenes', 'Ratio of areas and volumes'),
  P(r"Si dues figures (planes o cossos) són semblants amb raó \(k\), les longituds es multipliquen per \(k\), les <strong>àrees</strong> per \(k^2\) i els <strong>volums</strong> per \(k^3\):",
    r"Si dos figuras (planas o cuerpos) son semejantes con razón \(k\), las longitudes se multiplican por \(k\), las <strong>áreas</strong> por \(k^2\) y los <strong>volúmenes</strong> por \(k^3\):",
    r"If two figures (flat or solid) are similar with factor \(k\), lengths are multiplied by \(k\), <strong>areas</strong> by \(k^2\) and <strong>volumes</strong> by \(k^3\):")
  + D(r"\frac{L'}{L}=k\qquad\frac{A'}{A}=k^2\qquad\frac{V'}{V}=k^3")
  + P(r"Per a un cub de costat 1 ampliat amb \(k=2\): el costat val 2, cada cara té \(2^2=4\) quadrets i el cub sencer està fet de \(2^3=8\) cubets.",
      r"Para un cubo de lado 1 ampliado con \(k=2\): el lado vale 2, cada cara tiene \(2^2=4\) cuadraditos y el cubo entero está hecho de \(2^3=8\) cubitos.",
      r"For a cube of side 1 enlarged with \(k=2\): the side is 2, each face has \(2^2=4\) small squares and the whole cube is made of \(2^3=8\) small cubes.")
  + widget('w-k', '🧊', L('Longituds, àrees i volums', 'Longitudes, áreas y volúmenes', 'Lengths, areas and volumes'),
           ['<div class="wrow">' + rng('k', 1, 5, 1, 2, 'k') + '</div>'])
  + P(r"En un plànol a escala \(1:n\), les àrees reals són \(n^2\) vegades les del plànol. Una maqueta a escala \(1:n\) té un volum \(n^3\) vegades menor que l'objecte real.",
      r"En un plano a escala \(1:n\), las áreas reales son \(n^2\) veces las del plano. Una maqueta a escala \(1:n\) tiene un volumen \(n^3\) veces menor que el objeto real.",
      r"On a \(1:n\) plan, real areas are \(n^2\) times the areas on the plan. A \(1:n\) scale model has a volume \(n^3\) times smaller than the real object.")
  + drill('k23', 'Entrena: àrees i volums semblants', 'Entrena: áreas y volúmenes semejantes', 'Train: areas and volumes of similar figures'))
s8 += levels(
 [prob(L(r"En un mapa a escala 1:200 000, dues ciutats estan a 7,5 cm. Quina és la distància real?", r"En un mapa a escala 1:200 000, dos ciudades están a 7,5 cm. ¿Cuál es la distancia real?", r"On a 1:200 000 map, two towns are 7.5 cm apart. What is the real distance?"),
       D(r"7{,}5\cdot200\,000=1\,500\,000\ \text{cm}=\boxed{15\ \text{km}}")),
  prob(L(r"Una habitació fa 4,2 m × 3,5 m. Quines dimensions té en un plànol a escala 1:50?", r"Una habitación mide 4,2 m × 3,5 m. ¿Qué dimensiones tiene en un plano a escala 1:50?", r"A room is 4.2 m × 3.5 m. What are its dimensions on a 1:50 plan?"),
       D(r"420:50=\boxed{8{,}4\ \text{cm}}\qquad350:50=\boxed{7\ \text{cm}}"))],
 [prob(L(r"Dos pobles que estan a 12 km es troben a 4 cm en un mapa. Quina és l'escala? Si un llac ocupa 3 cm² en el mapa, quina superfície real té?", r"Dos pueblos que están a 12 km se encuentran a 4 cm en un mapa. ¿Cuál es la escala? Si un lago ocupa 3 cm² en el mapa, ¿qué superficie real tiene?", r"Two villages 12 km apart are 4 cm apart on a map. What is the scale? If a lake covers 3 cm² on the map, what is its real area?"),
       D(r"12\ \text{km}=1\,200\,000\ \text{cm}\qquad\frac{4}{1\,200\,000}=\frac{1}{300\,000}\ \Rightarrow\ \boxed{1:300\,000}"),
       P(r"Les àrees es multipliquen per \(300\,000^2\). Més fàcil: 1 cm del mapa són 3 km reals, així que 1 cm² del mapa són \(3\cdot3=9\) km² reals:", r"Las áreas se multiplican por \(300\,000^2\). Más fácil: 1 cm del mapa son 3 km reales, así que 1 cm² del mapa son \(3\cdot3=9\) km² reales:", r"Areas are multiplied by \(300\,000^2\). Easier: 1 cm on the map is 3 km, so 1 cm² on the map is \(3\cdot3=9\) km²:"),
       D(r"3\cdot9=\boxed{27\ \text{km}^2}"))],
 [prob(L(r"Una maqueta d'un vaixell està feta a escala 1:100. La coberta de la maqueta té 0,6 m² i el casc té un volum de 0,04 m³. Calcula la superfície real de la coberta i el volum real del casc.", r"Una maqueta de un barco está hecha a escala 1:100. La cubierta de la maqueta tiene 0,6 m² y el casco tiene un volumen de 0,04 m³. Calcula la superficie real de la cubierta y el volumen real del casco.", r"A model ship is built at 1:100. The model's deck is 0.6 m² and its hull has a volume of 0.04 m³. Find the real deck area and the real hull volume."),
       D(r"k=100:\qquad A=0{,}6\cdot100^2=0{,}6\cdot10\,000=\boxed{6000\ \text{m}^2}"),
       D(r"V=0{,}04\cdot100^3=0{,}04\cdot1\,000\,000=\boxed{40\,000\ \text{m}^3}"))])
ck(R(75, 10) * 200000 / 100000, 15); ck(R(420, 50), 8.4); ck(R(350, 50), 7); ck(R(1200000, 4), 300000); ck(R(6, 10) * 10 ** 4, 6000); ck(R(4, 100) * 10 ** 6, 40000)
s8 += practice([
  ('★', L(r"a) En un plànol a escala 1:100, una paret fa 6,5 cm. Quant fa en realitat? b) Quina distància hi haurà en un mapa 1:25 000 entre dos punts que estan a 2 km?", r"a) En un plano a escala 1:100, una pared mide 6,5 cm. ¿Cuánto mide en realidad? b) ¿Qué distancia habrá en un mapa 1:25 000 entre dos puntos que están a 2 km?", r"a) On a 1:100 plan a wall is 6.5 cm long. How long is it really? b) How far apart on a 1:25 000 map are two points that are 2 km apart?")),
  ('★★', L(r"c) Un cub de 3 cm d'aresta s'amplia amb raó 4. Calcula l'aresta, l'àrea d'una cara i el volum del cub nou. Per quant s'han multiplicat?", r"c) Un cubo de 3 cm de arista se amplía con razón 4. Calcula la arista, el área de una cara y el volumen del cubo nuevo. ¿Por cuánto se han multiplicado?", r"c) A cube with 3 cm edges is enlarged with factor 4. Find the new edge, the area of one face and the volume. By how much has each been multiplied?")),
  ('★★★', L(r"d) Dues gerres semblants tenen altures de 20 cm i 30 cm. Si la menuda té una capacitat d'1,6 litres, quina capacitat té la gran?", r"d) Dos jarras semejantes tienen alturas de 20 cm y 30 cm. Si la pequeña tiene una capacidad de 1,6 litros, ¿qué capacidad tiene la grande?", r"d) Two similar jugs are 20 cm and 30 cm tall. If the small one holds 1.6 litres, how much does the big one hold?"))],
  P(r"a) 650 cm = 6,5 m. b) \(200\,000:25\,000=8\) cm. c) Aresta 12 cm (×4), cara 144 cm² (×16), volum 1728 cm³ (×64). d) \(k=1{,}5\), \(k^3=3{,}375\): \(1{,}6\cdot3{,}375=5{,}4\) L.",
    r"a) 650 cm = 6,5 m. b) \(200\,000:25\,000=8\) cm. c) Arista 12 cm (×4), cara 144 cm² (×16), volumen 1728 cm³ (×64). d) \(k=1{,}5\), \(k^3=3{,}375\): \(1{,}6\cdot3{,}375=5{,}4\) L.",
    r"a) 650 cm = 6.5 m. b) \(200\,000\div25\,000=8\) cm. c) Edge 12 cm (×4), face 144 cm² (×16), volume 1728 cm³ (×64). d) \(k=1.5\), \(k^3=3.375\): \(1.6\cdot3.375=5.4\) L."))
assert 12 ** 2 == 144 and 12 ** 3 == 1728 and 144 // 9 == 16 and 1728 // 27 == 64; ck(R(16, 10) * R(3, 2) ** 3, 5.4)
