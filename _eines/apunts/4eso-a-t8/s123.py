# 8.1 Figures semblants · 8.2 Plànols, mapes i maquetes · 8.3 El teorema de Tales
# Apunts de la Unitat 8 de 4t ESO A (Semblança. Aplicacions), fets a partir dels de 2n ESO (../2eso-t8/s123.py) amb els volums
# de figures semblants i de maquetes (de ../3eso-t10/s78.py). Cada resultat es comprova amb ck().
from comu import *
from fig8 import *

# =====================================================================
# 8.1 Figures semblants
# =====================================================================
FL = [(0, 0), (4, 0), (4, 1), (1.5, 1), (1.5, 3), (0, 3)]
s1 = box('def', L('Què són dues figures semblants?', '¿Qué son dos figuras semejantes?', 'What are two similar figures?'),
  P(r"Quan fem una foto i l'ampliem, o quan dibuixem un objecte més menut en el quadern, obtenim una figura amb la <strong>mateixa forma</strong> però amb una <strong>grandària diferent</strong>. Diem que les dues figures són <strong>semblants</strong>: una és una <strong>ampliació</strong> o una <strong>reducció</strong> de l'altra.",
    r"Cuando hacemos una foto y la ampliamos, o cuando dibujamos un objeto más pequeño en el cuaderno, obtenemos una figura con la <strong>misma forma</strong> pero con un <strong>tamaño distinto</strong>. Decimos que las dos figuras son <strong>semejantes</strong>: una es una <strong>ampliación</strong> o una <strong>reducción</strong> de la otra.",
    r"When we enlarge a photo, or draw a smaller version of an object in our notebook, we get a figure with the <strong>same shape</strong> but a <strong>different size</strong>. We say the two figures are <strong>similar</strong>: one is an <strong>enlargement</strong> or a <strong>reduction</strong> of the other.")
  + P(r"Dos polígons són semblants si compleixen <strong>les dues</strong> condicions següents:",
      r"Dos polígonos son semejantes si cumplen <strong>las dos</strong> condiciones siguientes:",
      r"Two polygons are similar if they meet <strong>both</strong> of these conditions:")
  + ul(L(r"els angles corresponents són <strong>iguals</strong>;", r"los ángulos correspondientes son <strong>iguales</strong>;", r"corresponding angles are <strong>equal</strong>;"),
       L(r"els costats corresponents, que s'anomenen <strong>costats homòlegs</strong>, són <strong>proporcionals</strong>.", r"los lados correspondientes, que se llaman <strong>lados homólogos</strong>, son <strong>proporcionales</strong>.", r"corresponding sides (called <strong>corresponding</strong> or homologous sides) are <strong>proportional</strong>."))
  + P(r"El quocient constant entre cada costat de la figura nova i el seu homòleg de la figura original és la <strong>raó de semblança</strong>, \(k\):",
      r"El cociente constante entre cada lado de la figura nueva y su homólogo de la figura original es la <strong>razón de semejanza</strong>, \(k\):",
      r"The constant quotient between each side of the new figure and the matching side of the original is the <strong>scale factor</strong>, \(k\):")
  + D(r"k=\frac{a'}{a}=\frac{b'}{b}=\frac{c'}{c}=\dots")
  + figs(G(simpair(FL, 1.5, ['4', '1', '2,5', '2', '1,5', '3'], ['6', '1,5', '3,75', '3', '2,25', '4,5']), W=320, pad=24, cap=r"\(k=\frac{6}{4}=\frac{4{,}5}{3}=1{,}5\)"))
  + tbl([L('Raó de semblança', 'Razón de semejanza', 'Scale factor'), L('La figura nova és…', 'La figura nueva es…', 'The new figure is…'), L('Exemple', 'Ejemplo', 'Example')],
        [[r'\(k>1\)', L('una <strong>ampliació</strong>', 'una <strong>ampliación</strong>', 'an <strong>enlargement</strong>'), L(r'\(k=2\): els costats es dupliquen', r'\(k=2\): los lados se duplican', r'\(k=2\): sides are doubled')],
         [r'\(k=1\)', L('una figura <strong>igual</strong>', 'una figura <strong>igual</strong>', 'a <strong>congruent</strong> (identical) figure'), L('la mateixa grandària', 'el mismo tamaño', 'the same size')],
         [r'\(0<k<1\)', L('una <strong>reducció</strong>', 'una <strong>reducción</strong>', 'a <strong>reduction</strong>'), L(r'\(k=0{,}5\): els costats es fan la meitat', r'\(k=0{,}5\): los lados se reducen a la mitad', r'\(k=0.5\): sides are halved')]], 'narrow')
  + note(r"No n'hi ha prou amb una sola condició. Un quadrat i un rectangle tenen tots els angles rectes, però no són semblants (el rectangle és més allargat). Un quadrat i un rombe tenen els quatre costats iguals, però tampoc són semblants (els angles són diferents).",
         r"No basta con una sola condición. Un cuadrado y un rectángulo tienen todos los ángulos rectos, pero no son semejantes (el rectángulo es más alargado). Un cuadrado y un rombo tienen los cuatro lados iguales, pero tampoco son semejantes (los ángulos son distintos).",
         r"One condition alone isn't enough. A square and a rectangle both have right angles, but they aren't similar (the rectangle is longer). A square and a rhombus both have four equal sides, but they aren't similar either (their angles differ).", '⚠️'))
ck(R(6, 4), 1.5); ck(R(45, 10) / 3, 1.5); ck(R(25, 10) * R(3, 2), 3.75); ck(R(15, 10) * R(3, 2), 2.25)
s1 += box('prop', L('Com es calcula un costat que falta', 'Cómo se calcula un lado que falta', 'How to find a missing side'),
  ol(L(r"Busca una parella de <strong>costats homòlegs</strong> que conegues tots dos i calcula \(k=\dfrac{\text{costat nou}}{\text{costat original}}\).", r"Busca una pareja de <strong>lados homólogos</strong> que conozcas los dos y calcula \(k=\dfrac{\text{lado nuevo}}{\text{lado original}}\).", r"Find a pair of <strong>corresponding sides</strong> that you know both of and work out \(k=\dfrac{\text{new side}}{\text{original side}}\)."),
     L(r"Multiplica per \(k\) els altres costats de la figura original (o divideix per \(k\) si vas de la nova a l'original).", r"Multiplica por \(k\) los otros lados de la figura original (o divide por \(k\) si vas de la nueva a la original).", r"Multiply the other sides of the original by \(k\) (or divide by \(k\) to go from the new figure back to the original)."))
  + P(r"Exemple: un triangle de costats 4, 6 i 7 cm és semblant a un altre en què el costat homòleg del de 4 cm fa 10 cm.",
      r"Ejemplo: un triángulo de lados 4, 6 y 7 cm es semejante a otro en el que el lado homólogo del de 4 cm mide 10 cm.",
      r"Example: a triangle with sides 4, 6 and 7 cm is similar to another one in which the side matching the 4 cm side is 10 cm.")
  + D(r"k=\frac{10}{4}=2{,}5\qquad 6\cdot2{,}5=15\ \text{cm}\qquad 7\cdot2{,}5=17{,}5\ \text{cm}")
  + note(r"Compara sempre el costat menut amb el menut, el mitjà amb el mitjà i el gran amb el gran: són els costats homòlegs.",
         r"Compara siempre el lado pequeño con el pequeño, el mediano con el mediano y el grande con el grande: son los lados homólogos.",
         r"Always compare shortest with shortest, middle with middle and longest with longest: those are the corresponding sides."))
ck(R(10, 4), 2.5); ck(6 * R(5, 2), 15); ck(7 * R(5, 2), 17.5)
s1 += box('prop', L('Perímetres i àrees de figures semblants', 'Perímetros y áreas de figuras semejantes', 'Perimeters and areas of similar figures'),
  P(r"Si dues figures són semblants amb raó \(k\):", r"Si dos figuras son semejantes con razón \(k\):", r"If two figures are similar with scale factor \(k\):")
  + ul(L(r"el <strong>perímetre</strong> (i qualsevol altra longitud: altures, diagonals…) es multiplica per \(k\);", r"el <strong>perímetro</strong> (y cualquier otra longitud: alturas, diagonales…) se multiplica por \(k\);", r"the <strong>perimeter</strong> (and any other length: heights, diagonals…) is multiplied by \(k\);"),
       L(r"l'<strong>àrea</strong> es multiplica per \(k^2\).", r"el <strong>área</strong> se multiplica por \(k^2\).", r"the <strong>area</strong> is multiplied by \(k^2\)."))
  + D(r"P'=k\cdot P\qquad\qquad A'=k^2\cdot A")
  + P(r"Per què \(k^2\)? Si dupliquem els costats d'un quadrat de 3 cm, el nou fa 6 cm de costat i la seua àrea és \(6\cdot6=36\) cm², que és \(4=2^2\) vegades l'àrea original (\(9\) cm²): hi caben quatre quadrats com l'original.",
      r"¿Por qué \(k^2\)? Si duplicamos los lados de un cuadrado de 3 cm, el nuevo mide 6 cm de lado y su área es \(6\cdot6=36\) cm², que es \(4=2^2\) veces el área original (\(9\) cm²): caben cuatro cuadrados como el original.",
      r"Why \(k^2\)? If we double the sides of a 3 cm square, the new one has 6 cm sides and its area is \(6\cdot6=36\) cm², which is \(4=2^2\) times the original area (\(9\) cm²): four copies of the original fit inside it.")
  + figs(G([('poly', [(0, 0), (3, 0), (3, 3), (0, 3)], 'gf'), ('txt', (1.5, 1.5), '9 cm²', {}), ('txt', (1.5, 0), '3', {'dy': 15}),
            ('poly', [(5, 0), (11, 0), (11, 6), (5, 6)], 'tr'), ('seg', (8, 0), (8, 6), 'gl'), ('seg', (5, 3), (11, 3), 'gl'),
            ('txt', (8, 0), '6', {'dy': 15}), ('txt', (6.5, 1.5), '9', {}), ('txt', (9.5, 1.5), '9', {}), ('txt', (6.5, 4.5), '9', {}), ('txt', (9.5, 4.5), '9', {})], W=300, pad=22, cap=r"\(k=2\Rightarrow A'=2^2\cdot9=36\ \text{cm}^2\)"))
  + widget('w-sem', '🔍', L('Amplia o redueix una figura', 'Amplía o reduce una figura', 'Enlarge or reduce a shape'),
           [seg([('L', L('Forma de L', 'Forma de L', 'L shape')), ('T', L('Triangle', 'Triángulo', 'Triangle')), ('R', L('Rectangle', 'Rectángulo', 'Rectangle'))]),
            '<div class="wrow">' + rng('k', 0.25, 3, 0.25, 2, 'k') + '</div>'])
  + drill('sem', 'Entrena: figures semblants', 'Entrena: figuras semejantes', 'Train: similar figures'))
ck(6 * 6, 36); ck(R(36, 9), 4)
s1 += box('prop', L('Volums de cossos semblants', 'Volúmenes de cuerpos semejantes', 'Volumes of similar solids'),
  P(r"La semblança també es pot aplicar a <strong>cossos</strong> (cubs, prismes, ampolles, maquetes…). Si dos cossos són semblants amb raó \(k\), les longituds es multipliquen per \(k\), les <strong>àrees</strong> per \(k^2\) i els <strong>volums</strong> per \(k^3\):",
    r"La semejanza también se puede aplicar a <strong>cuerpos</strong> (cubos, prismas, botellas, maquetas…). Si dos cuerpos son semejantes con razón \(k\), las longitudes se multiplican por \(k\), las <strong>áreas</strong> por \(k^2\) y los <strong>volúmenes</strong> por \(k^3\):",
    r"Similarity also applies to <strong>solids</strong> (cubes, prisms, bottles, scale models…). If two solids are similar with factor \(k\), lengths are multiplied by \(k\), <strong>areas</strong> by \(k^2\) and <strong>volumes</strong> by \(k^3\):")
  + D(r"\frac{L'}{L}=k\qquad\frac{A'}{A}=k^2\qquad\frac{V'}{V}=k^3")
  + P(r"Per a un cub de costat 1 ampliat amb \(k=2\): el costat val 2, cada cara té \(2^2=4\) quadrets i el cub sencer està fet de \(2^3=8\) cubets.",
      r"Para un cubo de lado 1 ampliado con \(k=2\): el lado vale 2, cada cara tiene \(2^2=4\) cuadraditos y el cubo entero está hecho de \(2^3=8\) cubitos.",
      r"For a cube of side 1 enlarged with \(k=2\): the side is 2, each face has \(2^2=4\) small squares and the whole cube is made of \(2^3=8\) small cubes.")
  + widget('w-k', '🧊', L('Longituds, àrees i volums', 'Longitudes, áreas y volúmenes', 'Lengths, areas and volumes'),
           ['<div class="wrow">' + rng('k', 1, 5, 1, 2, 'k') + '</div>'])
  + P(r"<strong>Exemple.</strong> Dues gerres semblants tenen altures de 20 cm i 30 cm. Si la menuda té una capacitat d'1,6 L, la raó és \(k=\frac{30}{20}=1{,}5\) i la gran té \(1{,}6\cdot1{,}5^3=1{,}6\cdot3{,}375=5{,}4\) L.",
      r"<strong>Ejemplo.</strong> Dos jarras semejantes tienen alturas de 20 cm y 30 cm. Si la pequeña tiene una capacidad de 1,6 L, la razón es \(k=\frac{30}{20}=1{,}5\) y la grande tiene \(1{,}6\cdot1{,}5^3=1{,}6\cdot3{,}375=5{,}4\) L.",
      r"<strong>Example.</strong> Two similar jugs are 20 cm and 30 cm tall. If the small one holds 1.6 L, the factor is \(k=\frac{30}{20}=1.5\) and the big one holds \(1.6\cdot1.5^3=1.6\cdot3.375=5.4\) L.")
  + note(r"Si dupliquem les mesures d'una caixa, no hi cap el doble: hi cap \(2^3=8\) vegades més!",
         r"Si duplicamos las medidas de una caja, no cabe el doble: ¡cabe \(2^3=8\) veces más!",
         r"If we double the measurements of a box, it doesn't hold twice as much: it holds \(2^3=8\) times as much!", '⚠️')
  + drill('k23', 'Entrena: àrees i volums semblants', 'Entrena: áreas y volúmenes semejantes', 'Train: areas and volumes of similar figures'))
ck(R(30, 20), 1.5); ck(R(3, 2) ** 3, 3.375); ck(R(16, 10) * R(3, 2) ** 3, 5.4)
s1 += levels(
 [prob(L(r"Un rectangle de 5 cm × 8 cm és semblant a un altre que té el costat menut de 15 cm. Calcula la raó de semblança i el costat gran del segon rectangle.", r"Un rectángulo de 5 cm × 8 cm es semejante a otro que tiene el lado pequeño de 15 cm. Calcula la razón de semejanza y el lado grande del segundo rectángulo.", r"A 5 cm × 8 cm rectangle is similar to another whose short side is 15 cm. Find the scale factor and the long side of the second rectangle."),
       D(r"k=\frac{15}{5}=\boxed{3}\qquad 8\cdot3=\boxed{24\ \text{cm}}")),
  prob(L(r"Redueix amb raó \(k=0{,}5\) un triangle de costats 6, 8 i 10 cm. Quins costats té el triangle nou?", r"Reduce con razón \(k=0{,}5\) un triángulo de lados 6, 8 y 10 cm. ¿Qué lados tiene el triángulo nuevo?", r"Reduce a triangle with sides 6, 8 and 10 cm by a factor \(k=0.5\). What are the new sides?"),
       D(r"6\cdot0{,}5=3\qquad8\cdot0{,}5=4\qquad10\cdot0{,}5=5\ \Rightarrow\ \boxed{3,\ 4\ \text{%s}\ 5\ \text{cm}}" % Lt('i', 'y', 'and')))],
 [prob(L(r"Són semblants un rectangle de 4 cm × 6 cm i un altre de 6 cm × 9 cm? I un de 4 cm × 6 cm i un altre de 6 cm × 8 cm?", r"¿Son semejantes un rectángulo de 4 cm × 6 cm y otro de 6 cm × 9 cm? ¿Y uno de 4 cm × 6 cm y otro de 6 cm × 8 cm?", r"Are a 4 cm × 6 cm rectangle and a 6 cm × 9 cm one similar? And a 4 cm × 6 cm one and a 6 cm × 8 cm one?"),
       P(r"Tots els angles són rectes: només cal comparar els costats homòlegs (menut amb menut i gran amb gran).", r"Todos los ángulos son rectos: solo hay que comparar los lados homólogos (pequeño con pequeño y grande con grande).", r"All the angles are right angles: we just compare corresponding sides (short with short, long with long)."),
       D(r"\frac64=1{,}5\quad\frac96=1{,}5\ \Rightarrow\ \boxed{\text{%s},\ k=1{,}5}" % Lt('semblants', 'semejantes', 'similar')),
       D(r"\frac64=1{,}5\quad\frac86\approx1{,}33\ \Rightarrow\ \boxed{\text{%s}}" % Lt('no són semblants', 'no son semejantes', 'not similar'))),
  prob(L(r"Un quadrat té 5 cm de costat. L'ampliem amb raó \(k=3\). Calcula el perímetre i l'àrea dels dos quadrats. Per quant s'ha multiplicat cada cosa?", r"Un cuadrado tiene 5 cm de lado. Lo ampliamos con razón \(k=3\). Calcula el perímetro y el área de los dos cuadrados. ¿Por cuánto se ha multiplicado cada cosa?", r"A square has 5 cm sides. We enlarge it with \(k=3\). Find the perimeter and area of both squares. By how much has each been multiplied?"),
       D(r"P=4\cdot5=20\ \text{cm}\qquad A=5^2=25\ \text{cm}^2"),
       D(r"\text{%s } 15\ \text{cm}:\quad P'=60\ \text{cm}\ (\times3)\qquad A'=225\ \text{cm}^2\ (\times9=3^2)" % Lt('costat', 'lado', 'side')))],
 [prob(L(r"Una foto de 9 cm × 13 cm s'amplia fins que el costat menut fa 27 cm. Quant fa el costat gran? Quantes vegades és més gran l'àrea de la foto ampliada?", r"Una foto de 9 cm × 13 cm se amplía hasta que el lado pequeño mide 27 cm. ¿Cuánto mide el lado grande? ¿Cuántas veces es mayor el área de la foto ampliada?", r"A 9 cm × 13 cm photo is enlarged until its short side is 27 cm. How long is the long side? How many times bigger is the area of the enlarged photo?"),
       D(r"k=\frac{27}{9}=3\qquad 13\cdot3=\boxed{39\ \text{cm}}"),
       D(r"A=9\cdot13=117\ \text{cm}^2\qquad A'=27\cdot39=1053\ \text{cm}^2\qquad\frac{1053}{117}=\boxed{9}=3^2"),
       P(r"Compte: si els costats es multipliquen per 3, l'àrea no es multiplica per 3, sinó per 9.", r"Cuidado: si los lados se multiplican por 3, el área no se multiplica por 3, sino por 9.", r"Careful: if the sides are multiplied by 3, the area isn't multiplied by 3 but by 9."))])
ck(R(15, 5), 3); ck(8 * 3, 24); ck(R(6, 4), 1.5); ck(R(9, 6), 1.5); ck(R(8, 6), 1.33, 2); ck(4 * 15, 60); ck(15 ** 2, 225); ck(R(225, 25), 9)
ck(R(27, 9), 3); ck(13 * 3, 39); ck(9 * 13, 117); ck(27 * 39, 1053); ck(R(1053, 117), 9)
s1 += practice([
  ('★', L(r"a) Un triangle té costats de 2, 3 i 4 cm. Calcula els costats d'un triangle semblant amb raó \(k=2{,}5\). b) Un rectangle de 12 cm × 20 cm es redueix amb raó \(k=0{,}25\). Quines dimensions té?", r"a) Un triángulo tiene lados de 2, 3 y 4 cm. Calcula los lados de un triángulo semejante con razón \(k=2{,}5\). b) Un rectángulo de 12 cm × 20 cm se reduce con razón \(k=0{,}25\). ¿Qué dimensiones tiene?", r"a) A triangle has sides 2, 3 and 4 cm. Find the sides of a similar triangle with \(k=2.5\). b) A 12 cm × 20 cm rectangle is reduced with \(k=0.25\). What are its dimensions?")),
  ('★★', L(r"c) Dos hexàgons regulars tenen costats de 3 cm i 6 cm. Quina és la raó de semblança? Per quant es multiplica l'àrea? d) Un polígon té 30 cm de perímetre i 40 cm² d'àrea. Calcula el perímetre i l'àrea d'un polígon semblant amb \(k=2\).", r"c) Dos hexágonos regulares tienen lados de 3 cm y 6 cm. ¿Cuál es la razón de semejanza? ¿Por cuánto se multiplica el área? d) Un polígono tiene 30 cm de perímetro y 40 cm² de área. Calcula el perímetro y el área de un polígono semejante con \(k=2\).", r"c) Two regular hexagons have 3 cm and 6 cm sides. What is the scale factor? By how much is the area multiplied? d) A polygon has a 30 cm perimeter and a 40 cm² area. Find the perimeter and area of a similar polygon with \(k=2\).")),
  ('★★★', L(r"e) Dos quadrats semblants tenen àrees de 16 cm² i 100 cm². Quant fa el costat de cadascun? Quina és la raó de semblança?", r"e) Dos cuadrados tienen áreas de 16 cm² y 100 cm². ¿Cuánto mide el lado de cada uno? ¿Cuál es la razón de semejanza?", r"e) Two squares have areas 16 cm² and 100 cm². How long is each side? What is the scale factor?"))],
  P(r"a) 5, 7,5 i 10 cm. b) 3 cm × 5 cm. c) \(k=2\); l'àrea es multiplica per 4. d) \(P'=60\) cm, \(A'=160\) cm². e) Costats de 4 cm i 10 cm; \(k=\frac{10}{4}=2{,}5\).",
    r"a) 5, 7,5 y 10 cm. b) 3 cm × 5 cm. c) \(k=2\); el área se multiplica por 4. d) \(P'=60\) cm, \(A'=160\) cm². e) Lados de 4 cm y 10 cm; \(k=\frac{10}{4}=2{,}5\).",
    r"a) 5, 7.5 and 10 cm. b) 3 cm × 5 cm. c) \(k=2\); the area is multiplied by 4. d) \(P'=60\) cm, \(A'=160\) cm². e) Sides 4 cm and 10 cm; \(k=\frac{10}{4}=2.5\)."))
ck(2 * R(5, 2), 5); ck(3 * R(5, 2), 7.5); ck(4 * R(5, 2), 10); ck(12 * R(1, 4), 3); ck(20 * R(1, 4), 5); ck(30 * 2, 60); ck(40 * 4, 160); ck(S(16), 4); ck(S(100), 10); ck(R(10, 4), 2.5)

# =====================================================================
# 8.2 Plànols, mapes i maquetes
# =====================================================================
def escgraf(n, unit, W=300):
    """escala gràfica de n trams d'1 cm"""
    it = [('poly', [(0, 0), (n, 0), (n, 0.32), (0, 0.32)], 'gf')]
    for i in range(n):
        if i % 2 == 0: it.append(('poly', [(i, 0), (i + 1, 0), (i + 1, 0.32), (i, 0.32)], 'tr'))
        it.append(('txt', (i, 0), str(i * unit[0]) if i else '0', {'dy': 15}))
    it.append(('txt', (n, 0), '%d %s' % (n * unit[0], unit[1]), {'dy': 15}))
    return G(it, W=W, pad=26)
s2 = box('def', L("L'escala d'un plànol o d'un mapa", 'La escala de un plano o de un mapa', 'The scale of a plan or a map'),
  P(r"Un <strong>plànol</strong> (d'una casa, d'un institut…), un <strong>mapa</strong> o una <strong>maqueta</strong> són figures <strong>semblants</strong> a la realitat: tenen la mateixa forma, però són molt més menuts. L'<strong>escala</strong> ens diu quantes vegades s'ha reduït la realitat:",
    r"Un <strong>plano</strong> (de una casa, de un instituto…), un <strong>mapa</strong> o una <strong>maqueta</strong> son figuras <strong>semejantes</strong> a la realidad: tienen la misma forma, pero son mucho más pequeños. La <strong>escala</strong> nos dice cuántas veces se ha reducido la realidad:",
    r"A <strong>plan</strong> (of a house, a school…), a <strong>map</strong> or a <strong>scale model</strong> is <strong>similar</strong> to the real thing: it has the same shape but is much smaller. The <strong>scale</strong> tells us how many times reality has been reduced:")
  + D(r"\text{%s}\ 1:n\ \Rightarrow\ 1\ \text{cm %s}\ =\ n\ \text{cm %s}" % (Lt('escala', 'escala', 'scale'), Lt('del plànol', 'del plano', 'on the map'), Lt('reals', 'reales', 'in reality')))
  + P(r"Per exemple, en un mapa a escala \(1:50\,000\), cada centímetre del mapa representa \(50\,000\) cm \(=500\) m \(=0{,}5\) km de la realitat.",
      r"Por ejemplo, en un mapa a escala \(1:50\,000\), cada centímetro del mapa representa \(50\,000\) cm \(=500\) m \(=0{,}5\) km de la realidad.",
      r"For example, on a \(1:50\,000\) map, each centimetre on the map stands for \(50\,000\) cm \(=500\) m \(=0.5\) km in reality.")
  + tbl([L('Per a calcular…', 'Para calcular…', 'To find…'), L('Fem', 'Hacemos', 'We do')],
        [[L('la distància <strong>real</strong>', 'la distancia <strong>real</strong>', 'the <strong>real</strong> distance'), L(r'plànol \(\times\ n\)', r'plano \(\times\ n\)', r'map \(\times\ n\)')],
         [L('la distància en el <strong>plànol</strong>', 'la distancia en el <strong>plano</strong>', 'the distance on the <strong>map</strong>'), L(r'real \(:\ n\)', r'real \(:\ n\)', r'real \(\div\ n\)')],
         [L("l'<strong>escala</strong>", 'la <strong>escala</strong>', 'the <strong>scale</strong>'), L(r"\(n=\) real \(:\) plànol (en la mateixa unitat)", r"\(n=\) real \(:\) plano (en la misma unidad)", r"\(n=\) real \(\div\) map (in the same unit)")]], 'narrow')
  + note(r"Les dues mesures han d'estar en la <strong>mateixa unitat</strong>. Recorda: 1 m = 100 cm i 1 km = 1000 m = 100 000 cm. Al final, passa el resultat a m o a km perquè s'entenga millor.",
         r"Las dos medidas tienen que estar en la <strong>misma unidad</strong>. Recuerda: 1 m = 100 cm y 1 km = 1000 m = 100 000 cm. Al final, pasa el resultado a m o a km para que se entienda mejor.",
         r"Both lengths must be in the <strong>same unit</strong>. Remember: 1 m = 100 cm and 1 km = 1000 m = 100 000 cm. At the end, convert the result to m or km so it's easier to understand.", '⚠️')
  + P(r"Moltes vegades els mapes porten una <strong>escala gràfica</strong>: un segment dividit en trams, amb la distància real que representa cada tram. En aquesta, cada centímetre són 2 km (escala \(1:200\,000\)):",
      r"Muchas veces los mapas llevan una <strong>escala gráfica</strong>: un segmento dividido en tramos, con la distancia real que representa cada tramo. En esta, cada centímetro son 2 km (escala \(1:200\,000\)):",
      r"Maps often carry a <strong>graphic scale</strong>: a bar split into sections, each labelled with the real distance it stands for. In this one, each centimetre is 2 km (scale \(1:200\,000\)):")
  + figs(escgraf(4, (2, 'km')))
  + widget('w-escala', '🗺️', L("Calculadora d'escales", 'Calculadora de escalas', 'Scale calculator'),
           [seg([('r', L('Del plànol a la realitat', 'Del plano a la realidad', 'From map to reality')), ('p', L('De la realitat al plànol', 'De la realidad al plano', 'From reality to map')), ('e', L("Calcula l'escala", 'Calcula la escala', 'Find the scale'))]),
            '<div class="wrow">' + tin('n', L('Escala 1 :', 'Escala 1 :', 'Scale 1 :'), '50000', 'm') + tin('p', L('Plànol (cm) =', 'Plano (cm) =', 'Map (cm) ='), '4,2') + tin('r', L('Real (km) =', 'Real (km) =', 'Real (km) ='), '') + '</div>'],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('escala', 'Entrena: escales', 'Entrena: escalas', 'Train: scales'))
ck(R(200000, 100000), 2)
s2 += box('prop', L('Maquetes i superfícies en un plànol', 'Maquetas y superficies en un plano', 'Scale models and areas on a plan'),
  P(r"Una <strong>maqueta</strong> és una reproducció en tres dimensions a escala: d'un edifici, d'un tren, d'un avió… En una maqueta a escala \(1:87\), cada centímetre de la maqueta són 87 cm de l'objecte real. També hi ha escales d'<strong>ampliació</strong>, com \(5:1\) (el dibuix d'un insecte cinc vegades més gran que el real).",
    r"Una <strong>maqueta</strong> es una reproducción en tres dimensiones a escala: de un edificio, de un tren, de un avión… En una maqueta a escala \(1:87\), cada centímetro de la maqueta son 87 cm del objeto real. También hay escalas de <strong>ampliación</strong>, como \(5:1\) (el dibujo de un insecto cinco veces más grande que el real).",
    r"A <strong>scale model</strong> is a 3D reproduction at scale: of a building, a train, a plane… On a \(1:87\) model, each centimetre of the model is 87 cm of the real object. There are also <strong>enlargement</strong> scales, such as \(5:1\) (a drawing of an insect five times bigger than real life).")
  + P(r"Per a calcular una <strong>superfície</strong> real a partir d'un plànol, el més fàcil és passar primer les <strong>longituds</strong> a la realitat i després calcular l'àrea. Una habitació que en un plànol \(1:100\) fa 4 cm × 3 cm fa en realitat 4 m × 3 m, és a dir, 12 m².",
      r"Para calcular una <strong>superficie</strong> real a partir de un plano, lo más fácil es pasar primero las <strong>longitudes</strong> a la realidad y después calcular el área. Una habitación que en un plano \(1:100\) mide 4 cm × 3 cm mide en realidad 4 m × 3 m, es decir, 12 m².",
      r"To find a real <strong>area</strong> from a plan, it's easiest to first convert the <strong>lengths</strong> to real ones and then work out the area. A room that measures 4 cm × 3 cm on a \(1:100\) plan is really 4 m × 3 m, that is, 12 m².")
  + note(r"Compte: l'àrea real no és l'àrea del plànol per \(n\), sinó per \(n^2\) (com en qualsevol figura semblant). En l'exemple, \(12\) cm² \(\cdot\,100^2=120\,000\) cm² \(=12\) m².",
         r"Cuidado: el área real no es el área del plano por \(n\), sino por \(n^2\) (como en cualquier figura semejante). En el ejemplo, \(12\) cm² \(\cdot\,100^2=120\,000\) cm² \(=12\) m².",
         r"Careful: the real area isn't the plan's area times \(n\) but times \(n^2\) (as with any similar figures). In the example, \(12\) cm² \(\cdot\,100^2=120\,000\) cm² \(=12\) m².", '⚠️'))
ck(12 * 100 ** 2, 120000); ck(R(120000, 10000), 12)
s2 += box('prop', L('Volums en una maqueta', 'Volúmenes en una maqueta', 'Volumes in a scale model'),
  P(r"Una maqueta a escala \(1:n\) és un cos semblant a l'objecte real amb raó \(n\). Per tant, les superfícies reals són \(n^2\) vegades les de la maqueta i els volums reals, \(n^3\) vegades:",
    r"Una maqueta a escala \(1:n\) es un cuerpo semejante al objeto real con razón \(n\). Por tanto, las superficies reales son \(n^2\) veces las de la maqueta y los volúmenes reales, \(n^3\) veces:",
    r"A \(1:n\) scale model is similar to the real object with factor \(n\). So real areas are \(n^2\) times the model's and real volumes \(n^3\) times:")
  + D(r"A_{\text{real}}=n^2\cdot A_{\text{%s}}\qquad V_{\text{real}}=n^3\cdot V_{\text{%s}}" % (Lt('maqueta', 'maqueta', 'model'), Lt('maqueta', 'maqueta', 'model')))
  + P(r"<strong>Exemple.</strong> Una maqueta d'un vaixell a escala \(1:100\) té una coberta de 0,6 m² i un casc de 0,04 m³. La coberta real fa \(0{,}6\cdot100^2=6000\) m² i el casc real, \(0{,}04\cdot100^3=40\,000\) m³.",
      r"<strong>Ejemplo.</strong> Una maqueta de un barco a escala \(1:100\) tiene una cubierta de 0,6 m² y un casco de 0,04 m³. La cubierta real mide \(0{,}6\cdot100^2=6000\) m² y el casco real, \(0{,}04\cdot100^3=40\,000\) m³.",
      r"<strong>Example.</strong> A \(1:100\) model ship has a 0.6 m² deck and a 0.04 m³ hull. The real deck is \(0.6\cdot100^2=6000\) m² and the real hull \(0.04\cdot100^3=40\,000\) m³."))
ck(R(6, 10) * 10 ** 4, 6000); ck(R(4, 100) * 10 ** 6, 40000)
s2 += levels(
 [prob(L(r"En un mapa a escala \(1:50\,000\), dos pobles estan a 6 cm. Quina és la distància real?", r"En un mapa a escala \(1:50\,000\), dos pueblos están a 6 cm. ¿Cuál es la distancia real?", r"On a \(1:50\,000\) map, two villages are 6 cm apart. What is the real distance?"),
       D(r"6\cdot50\,000=300\,000\ \text{cm}=\boxed{3\ \text{km}}")),
  prob(L(r"Una aula fa 7,5 m × 6 m. Quines dimensions té en un plànol a escala \(1:100\)?", r"Un aula mide 7,5 m × 6 m. ¿Qué dimensiones tiene en un plano a escala \(1:100\)?", r"A classroom is 7.5 m × 6 m. What are its dimensions on a \(1:100\) plan?"),
       D(r"750:100=\boxed{7{,}5\ \text{cm}}\qquad600:100=\boxed{6\ \text{cm}}"))],
 [prob(L(r"En un mapa, 8 cm representen 2 km. Quina és l'escala del mapa?", r"En un mapa, 8 cm representan 2 km. ¿Cuál es la escala del mapa?", r"On a map, 8 cm stand for 2 km. What is the map's scale?"),
       D(r"2\ \text{km}=200\,000\ \text{cm}\qquad n=200\,000:8=25\,000\ \Rightarrow\ \boxed{1:25\,000}")),
  prob(L(r"Una maqueta de tren està feta a escala \(1:87\). La locomotora real fa 17,4 m. Quant fa la de la maqueta?", r"Una maqueta de tren está hecha a escala \(1:87\). La locomotora real mide 17,4 m. ¿Cuánto mide la de la maqueta?", r"A model train is built at \(1:87\). The real locomotive is 17.4 m long. How long is the model one?"),
       D(r"17{,}4\ \text{m}=1740\ \text{cm}\qquad1740:87=\boxed{20\ \text{cm}}"))],
 [prob(L(r"En el plànol d'un pis a escala \(1:200\), el saló és un rectangle de 3 cm × 2,5 cm. Calcula les dimensions reals del saló i la seua superfície.", r"En el plano de un piso a escala \(1:200\), el salón es un rectángulo de 3 cm × 2,5 cm. Calcula las dimensiones reales del salón y su superficie.", r"On a \(1:200\) flat plan, the living room is a 3 cm × 2.5 cm rectangle. Find the real dimensions of the room and its area."),
       D(r"3\cdot200=600\ \text{cm}=6\ \text{m}\qquad2{,}5\cdot200=500\ \text{cm}=5\ \text{m}"),
       D(r"A=6\cdot5=\boxed{30\ \text{m}^2}"),
       P(r"Comprovació: en el plànol, \(3\cdot2{,}5=7{,}5\) cm², i \(7{,}5\cdot200^2=300\,000\) cm² \(=30\) m² ✓", r"Comprobación: en el plano, \(3\cdot2{,}5=7{,}5\) cm², y \(7{,}5\cdot200^2=300\,000\) cm² \(=30\) m² ✓", r"Check: on the plan, \(3\cdot2.5=7.5\) cm², and \(7.5\cdot200^2=300\,000\) cm² \(=30\) m² ✓"))])
ck(6 * 50000 / 100000, 3); ck(R(750, 100), 7.5); ck(R(600, 100), 6); ck(R(200000, 8), 25000); ck(R(1740, 87), 20)
ck(3 * 200, 600); ck(R(25, 10) * 200, 500); ck(6 * 5, 30); ck(R(75, 10) * 200 ** 2, 300000)
s2 += practice([
  ('★', L(r"a) En un plànol a escala \(1:50\), una taula fa 3 cm. Quant fa la taula de veritat? b) Dues ciutats estan a 40 km. A quina distància estan en un mapa \(1:1\,000\,000\)?", r"a) En un plano a escala \(1:50\), una mesa mide 3 cm. ¿Cuánto mide la mesa de verdad? b) Dos ciudades están a 40 km. ¿A qué distancia están en un mapa \(1:1\,000\,000\)?", r"a) On a \(1:50\) plan a table is 3 cm long. How long is the real table? b) Two cities are 40 km apart. How far apart are they on a \(1:1\,000\,000\) map?")),
  ('★★', L(r"c) Un camp de futbol de 100 m de llarg fa 5 cm en un plànol. Quina és l'escala? d) L'escala gràfica d'un mapa diu que 1 cm són 500 m. Quina distància real hi ha entre dos punts que estan a 4,6 cm en el mapa?", r"c) Un campo de fútbol de 100 m de largo mide 5 cm en un plano. ¿Cuál es la escala? d) La escala gráfica de un mapa dice que 1 cm son 500 m. ¿Qué distancia real hay entre dos puntos que están a 4,6 cm en el mapa?", r"c) A 100 m long football pitch is 5 cm long on a plan. What is the scale? d) A map's graphic scale says 1 cm is 500 m. What is the real distance between two points 4.6 cm apart on the map?")),
  ('★★★', L(r"e) En un plànol a escala \(1:100\), un jardí quadrat fa 8 cm de costat. Quina superfície real té? Quantes vegades és més gran que la del plànol?", r"e) En un plano a escala \(1:100\), un jardín cuadrado mide 8 cm de lado. ¿Qué superficie real tiene? ¿Cuántas veces es mayor que la del plano?", r"e) On a \(1:100\) plan, a square garden has 8 cm sides. What is its real area? How many times bigger than on the plan is it?"))],
  P(r"a) 150 cm = 1,5 m. b) \(4\,000\,000:1\,000\,000=4\) cm. c) \(10\,000:5=2000\Rightarrow1:2000\). d) \(4{,}6\cdot500=2300\) m = 2,3 km. e) Costat real 8 m, superfície 64 m²; \(100^2=10\,000\) vegades més gran.",
    r"a) 150 cm = 1,5 m. b) \(4\,000\,000:1\,000\,000=4\) cm. c) \(10\,000:5=2000\Rightarrow1:2000\). d) \(4{,}6\cdot500=2300\) m = 2,3 km. e) Lado real 8 m, superficie 64 m²; \(100^2=10\,000\) veces mayor.",
    r"a) 150 cm = 1.5 m. b) \(4\,000\,000\div1\,000\,000=4\) cm. c) \(10\,000\div5=2000\Rightarrow1:2000\). d) \(4.6\cdot500=2300\) m = 2.3 km. e) Real side 8 m, area 64 m²; \(100^2=10\,000\) times bigger."))
ck(3 * 50, 150); ck(R(4000000, 1000000), 4); ck(R(10000, 5), 2000); ck(R(46, 10) * 500, 2300); ck(R(64 * 10000, 64), 10000)

# =====================================================================
# 8.3 El teorema de Tales
# =====================================================================
s3 = box('def', L('Segments proporcionals', 'Segmentos proporcionales', 'Proportional segments'),
  P(r"Recorda que una <strong>proporció</strong> és una igualtat de dues raons, \(\frac ab=\frac cd\), i que en una proporció el producte en creu és igual: \(a\cdot d=b\cdot c\). Per això, si en coneixem tres termes, podem calcular el quart:",
    r"Recuerda que una <strong>proporción</strong> es una igualdad de dos razones, \(\frac ab=\frac cd\), y que en una proporción el producto en cruz es igual: \(a\cdot d=b\cdot c\). Por eso, si conocemos tres términos, podemos calcular el cuarto:",
    r"Remember that a <strong>proportion</strong> is an equality of two ratios, \(\frac ab=\frac cd\), and that the cross products are equal: \(a\cdot d=b\cdot c\). So if we know three of the terms, we can find the fourth:")
  + D(r"\frac{4}{6}=\frac{10}{x}\ \Rightarrow\ 4\cdot x=6\cdot10\ \Rightarrow\ x=\frac{60}{4}=15")
  + P(r"Quatre segments \(a\), \(b\), \(c\) i \(d\) són <strong>proporcionals</strong> si les seues longituds formen una proporció.",
      r"Cuatro segmentos \(a\), \(b\), \(c\) y \(d\) son <strong>proporcionales</strong> si sus longitudes forman una proporción.",
      r"Four segments \(a\), \(b\), \(c\) and \(d\) are <strong>proportional</strong> if their lengths form a proportion.")
  + widget('w-quart', '🧮', L('Calculadora de proporcions', 'Calculadora de proporciones', 'Proportion calculator'),
           ['<div class="wrow">' + tin('a', 'a =', '4') + tin('b', 'b =', '6') + tin('c', 'c =', '10') + tin('d', 'd =', '') + '</div>',
            '<p class="hint-s">' + L(r"Proporció a/b = c/d. Escriu tres valors i deixa en blanc el que vols calcular.", r"Proporción a/b = c/d. Escribe tres valores y deja en blanco el que quieres calcular.", r"Proportion a/b = c/d. Type three values and leave blank the one you want to find.") + '</p>',
            quick([('4|6|10|', '4/6 = 10/x'), ('3|5||12', '3/5 = x/12'), ('|8|6|16', 'x/8 = 6/16'), ('2,5|4|6|', '2,5/4 = 6/x'), ('3|5|6|10', '3/5 = 6/10 ?')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('quart', 'Entrena: calcula el valor que falta', 'Entrena: calcula el valor que falta', 'Train: find the missing value'))
ck(R(6 * 10, 4), 15)
s3 += box('def', L('El teorema de Tales', 'El teorema de Tales', "Thales' theorem"),
  P(r"Si tres o més rectes <strong>paral·leles</strong> (\(r\), \(s\), \(t\)…) tallen dues rectes qualssevol \(a\) i \(b\), els segments que determinen sobre la recta \(a\) són <strong>proporcionals</strong> als segments corresponents que determinen sobre la recta \(b\):",
    r"Si tres o más rectas <strong>paralelas</strong> (\(r\), \(s\), \(t\)…) cortan dos rectas cualesquiera \(a\) y \(b\), los segmentos que determinan sobre la recta \(a\) son <strong>proporcionales</strong> a los segmentos correspondientes que determinan sobre la recta \(b\):",
    r"If three or more <strong>parallel</strong> lines (\(r\), \(s\), \(t\)…) cut any two lines \(a\) and \(b\), the segments they mark on line \(a\) are <strong>proportional</strong> to the corresponding segments they mark on line \(b\):")
  + figs(G(tales(2, 3, labs={'AB': '2', 'BC': '3', 'A1B1': '2,4', 'B1C1': '3,6'}), W=280))
  + D(r"\frac{\overline{AB}}{\overline{BC}}=\frac{\overline{A'B'}}{\overline{B'C'}}\qquad\text{%s}\qquad\frac{\overline{AB}}{\overline{A'B'}}=\frac{\overline{BC}}{\overline{B'C'}}" % Lt('o també', 'o también', 'or also'))
  + P(r"En la figura: \(\frac{2}{3}=\frac{2{,}4}{3{,}6}\), perquè \(2\cdot3{,}6=3\cdot2{,}4=7{,}2\). Les rectes \(a\) i \(b\) es poden tallar o no, i les paral·leles poden estar a qualsevol distància: la proporció sempre es compleix.",
      r"En la figura: \(\frac{2}{3}=\frac{2{,}4}{3{,}6}\), porque \(2\cdot3{,}6=3\cdot2{,}4=7{,}2\). Las rectas \(a\) y \(b\) pueden cortarse o no, y las paralelas pueden estar a cualquier distancia: la proporción siempre se cumple.",
      r"In the figure: \(\frac{2}{3}=\frac{2.4}{3.6}\), because \(2\cdot3.6=3\cdot2.4=7.2\). Lines \(a\) and \(b\) may or may not cross, and the parallels can be any distance apart: the proportion always holds.")
  + widget('w-tales', '📏', L('Mou les paral·leles i les secants', 'Mueve las paralelas y las secantes', 'Move the parallels and the transversals'),
           ['<div class="wrow">' + rng('d1', 1, 5, 0.5, 2, 'd1') + rng('d2', 1, 5, 0.5, 3, 'd2') + '</div>',
            '<div class="wrow">' + rng('ga', 40, 140, 2, 60, 'a') + rng('gb', 40, 140, 2, 80, 'b') + '</div>'])
  + note(r"Tales de Milet (segle VI aC) va ser un dels primers matemàtics grecs. Se li atribueix aquest teorema i la idea de mesurar altures amb ombres, que veurem en l'apartat 8.5.",
         r"Tales de Mileto (siglo VI a. C.) fue uno de los primeros matemáticos griegos. Se le atribuye este teorema y la idea de medir alturas con sombras, que veremos en el apartado 8.5.",
         r"Thales of Miletus (6th century BC) was one of the first Greek mathematicians. This theorem is attributed to him, as is the idea of measuring heights with shadows, which we'll see in section 8.5.", '🏛️'))
ck(R(2, 3), R(24, 36)); ck(2 * R(36, 10), 7.2); ck(3 * R(24, 10), 7.2)
s3 += box('prop', L('Calcular un segment amb el teorema de Tales', 'Calcular un segmento con el teorema de Tales', "Finding a segment with Thales' theorem"),
  ol(L(r"Escriu la proporció posant els segments de cada recta <strong>en el mateix ordre</strong>.", r"Escribe la proporción poniendo los segmentos de cada recta <strong>en el mismo orden</strong>.", r"Write the proportion with the segments of each line <strong>in the same order</strong>."),
     L(r"Multiplica en creu i aïlla la incògnita.", r"Multiplica en cruz y despeja la incógnita.", r"Cross-multiply and solve for the unknown."))
  + P(r"Si \(\overline{AB}=4\), \(\overline{BC}=6\) i \(\overline{A'B'}=5\):", r"Si \(\overline{AB}=4\), \(\overline{BC}=6\) y \(\overline{A'B'}=5\):", r"If \(\overline{AB}=4\), \(\overline{BC}=6\) and \(\overline{A'B'}=5\):")
  + D(r"\frac{4}{6}=\frac{5}{x}\ \Rightarrow\ 4x=30\ \Rightarrow\ x=\frac{30}{4}=7{,}5")
  + P(r"<strong>I al revés:</strong> si unes rectes determinen sobre dues secants segments que <em>no</em> són proporcionals, aquestes rectes <strong>no</strong> són paral·leles.",
      r"<strong>Y al revés:</strong> si unas rectas determinan sobre dos secantes segmentos que <em>no</em> son proporcionales, esas rectas <strong>no</strong> son paralelas.",
      r"<strong>And the other way round:</strong> if some lines mark segments on two transversals that are <em>not</em> proportional, those lines are <strong>not</strong> parallel.")
  + drill('tales', 'Entrena: el teorema de Tales', 'Entrena: el teorema de Tales', "Train: Thales' theorem"))
ck(R(30, 4), 7.5)
s3 += box('prop', L('Dividir un segment en parts iguals', 'Dividir un segmento en partes iguales', 'Dividing a segment into equal parts'),
  P(r"Amb el teorema de Tales podem dividir un segment \(AB\) en parts iguals amb regle i escaire, sense mesurar-lo:",
    r"Con el teorema de Tales podemos dividir un segmento \(AB\) en partes iguales con regla y escuadra, sin medirlo:",
    r"With Thales' theorem we can divide a segment \(AB\) into equal parts with a ruler and set square, without measuring it:")
  + ol(L(r"Des d'\(A\), traça una semirecta auxiliar qualsevol.", r"Desde \(A\), traza una semirrecta auxiliar cualquiera.", r"From \(A\), draw any auxiliary ray."),
       L(r"Marca-hi, amb el compàs, tants segments iguals com parts vulgues (de qualsevol llargària).", r"Marca en ella, con el compás, tantos segmentos iguales como partes quieras (de cualquier longitud).", r"Use compasses to mark on it as many equal segments as parts you want (of any length)."),
       L(r"Uneix l'última marca amb \(B\) i traça paral·leles a aquesta recta per les altres marques.", r"Une la última marca con \(B\) y traza paralelas a esa recta por las otras marcas.", r"Join the last mark to \(B\) and draw parallels to that line through the other marks."))
  + P(r"Les paral·leles tallen \(AB\) en parts iguals, perquè els segments de la semirecta són iguals (teorema de Tales). Si en la semirecta marquem segments proporcionals a uns nombres, obtenim parts <strong>proporcionals</strong> a aquests nombres.",
      r"Las paralelas cortan \(AB\) en partes iguales, porque los segmentos de la semirrecta son iguales (teorema de Tales). Si en la semirrecta marcamos segmentos proporcionales a unos números, obtenemos partes <strong>proporcionales</strong> a esos números.",
      r"The parallels cut \(AB\) into equal parts, because the segments on the ray are equal (Thales' theorem). If we mark segments on the ray proportional to some numbers, we get parts <strong>proportional</strong> to those numbers.")
  + figs(G(divseg(10, [1, 1, 1, 1, 1]), W=280, pad=24, cap=L(r"\(AB=10\) en 5 parts iguals de 2", r"\(AB=10\) en 5 partes iguales de 2", r"\(AB=10\) in 5 equal parts of 2")))
  + widget('w-div', '✂️', L('Divideix un segment', 'Divide un segmento', 'Divide a segment'),
           [seg([('eq', L('Parts iguals', 'Partes iguales', 'Equal parts')), ('pr', L('Parts proporcionals', 'Partes proporcionales', 'Proportional parts'))]),
            '<div class="wrow">' + tin('L', L('Longitud de AB =', 'Longitud de AB =', 'Length of AB ='), '12') + tin('n', L('Nombre de parts =', 'Número de partes =', 'Number of parts ='), '5', 'eqonly') + tin('k', L('Proporcionals a', 'Proporcionales a', 'Proportional to'), '2, 3, 4', 'm pronly') + '</div>',
            '<div class="wrow">' + '<button class="btn" type="button" data-a="step">' + L('Pas següent de la construcció', 'Paso siguiente de la construcción', 'Next construction step') + '</button></div>'],
           out='<div class="gout"></div><div class="hsteps"></div>'))
s3 += levels(
 [prob(L(r"Les rectes \(r\), \(s\) i \(t\) són paral·leles. Sobre la recta \(a\) determinen \(\overline{AB}=4\) cm i \(\overline{BC}=6\) cm, i sobre la recta \(b\), \(\overline{A'B'}=6\) cm. Calcula \(\overline{B'C'}\).", r"Las rectas \(r\), \(s\) y \(t\) son paralelas. Sobre la recta \(a\) determinan \(\overline{AB}=4\) cm y \(\overline{BC}=6\) cm, y sobre la recta \(b\), \(\overline{A'B'}=6\) cm. Calcula \(\overline{B'C'}\).", r"Lines \(r\), \(s\) and \(t\) are parallel. On line \(a\) they mark \(\overline{AB}=4\) cm and \(\overline{BC}=6\) cm, and on line \(b\), \(\overline{A'B'}=6\) cm. Find \(\overline{B'C'}\)."),
       D(r"\frac{4}{6}=\frac{6}{x}\ \Rightarrow\ 4x=36\ \Rightarrow\ x=\boxed{9\ \text{cm}}"))],
 [prob(L(r"En la figura, les rectes morades són paral·leles. Calcula \(x\) i la longitud total \(\overline{AC}\).", r"En la figura, las rectas moradas son paralelas. Calcula \(x\) y la longitud total \(\overline{AC}\).", r"In the figure the purple lines are parallel. Find \(x\) and the total length \(\overline{AC}\).")
       + figs(G(tales(3, 2, labs={'AB': '7,5', 'BC': 'x', 'A1B1': '6', 'B1C1': '4'}, hot='BC'), W=270)),
       D(r"\frac{7{,}5}{x}=\frac{6}{4}\ \Rightarrow\ 6x=30\ \Rightarrow\ x=\boxed{5}"),
       D(r"\overline{AC}=7{,}5+5=\boxed{12{,}5}")),
  prob(L(r"Unes rectes tallen dues secants i determinen sobre una segments de 3 cm i 5 cm, i sobre l'altra, de 4,5 cm i 7 cm. Són paral·leles aquestes rectes?", r"Unas rectas cortan dos secantes y determinan sobre una segmentos de 3 cm y 5 cm, y sobre la otra, de 4,5 cm y 7 cm. ¿Son paralelas esas rectas?", r"Some lines cut two transversals, marking segments of 3 cm and 5 cm on one and 4.5 cm and 7 cm on the other. Are those lines parallel?"),
       D(r"3\cdot7=21\qquad5\cdot4{,}5=22{,}5\qquad21\neq22{,}5"),
       P(r"Els segments no són proporcionals: les rectes <strong>no són paral·leles</strong>.", r"Los segmentos no son proporcionales: las rectas <strong>no son paralelas</strong>.", r"The segments aren't proportional: the lines are <strong>not parallel</strong>."))],
 [prob(L(r"Tres solars estan entre dos carrers i les partions entre ells són paral·leles. Al carrer de dalt, les façanes fan 15 m, 25 m i 30 m. Al carrer de baix, les tres façanes fan en total 98 m. Quant fa cada façana al carrer de baix?", r"Tres solares están entre dos calles y las lindes entre ellos son paralelas. En la calle de arriba, las fachadas miden 15 m, 25 m y 30 m. En la calle de abajo, las tres fachadas miden en total 98 m. ¿Cuánto mide cada fachada en la calle de abajo?", r"Three plots lie between two streets and the boundaries between them are parallel. On the upper street, the fronts are 15 m, 25 m and 30 m. On the lower street, the three fronts total 98 m. How long is each front on the lower street?"),
       P(r"Pel teorema de Tales, cada façana de baix s'obté multiplicant la de dalt pel mateix nombre:", r"Por el teorema de Tales, cada fachada de abajo se obtiene multiplicando la de arriba por el mismo número:", r"By Thales' theorem, each lower front is the upper one multiplied by the same number:"),
       D(r"\frac{98}{15+25+30}=\frac{98}{70}=1{,}4"),
       D(r"15\cdot1{,}4=\boxed{21\ \text{m}}\qquad25\cdot1{,}4=\boxed{35\ \text{m}}\qquad30\cdot1{,}4=\boxed{42\ \text{m}}"),
       P(r"Comprovació: \(21+35+42=98\) ✓", r"Comprobación: \(21+35+42=98\) ✓", r"Check: \(21+35+42=98\) ✓"))])
ck(R(36, 4), 9); ck(R(30, 6), 5); ck(R(75, 10) / 5, R(6, 4)); ck(R(75, 10) + 5, 12.5); assert 3 * 7 != 5 * R(45, 10)
ck(R(98, 70), 1.4); assert [15 * R(7, 5), 25 * R(7, 5), 30 * R(7, 5)] == [21, 35, 42] and 21 + 35 + 42 == 98
s3 += practice([
  ('★', L(r"a) Calcula \(x\): \(\frac{5}{8}=\frac{x}{24}\). b) Amb rectes paral·leles, \(\overline{AB}=3\), \(\overline{BC}=9\) i \(\overline{A'B'}=2\). Calcula \(\overline{B'C'}\).", r"a) Calcula \(x\): \(\frac{5}{8}=\frac{x}{24}\). b) Con rectas paralelas, \(\overline{AB}=3\), \(\overline{BC}=9\) y \(\overline{A'B'}=2\). Calcula \(\overline{B'C'}\).", r"a) Find \(x\): \(\frac{5}{8}=\frac{x}{24}\). b) With parallel lines, \(\overline{AB}=3\), \(\overline{BC}=9\) and \(\overline{A'B'}=2\). Find \(\overline{B'C'}\).")),
  ('★★', L(r"c) Amb rectes paral·leles, \(\overline{AB}=2{,}5\), \(\overline{A'B'}=4\) i \(\overline{B'C'}=6\). Calcula \(\overline{BC}\). d) Segments de 4 i 6 sobre una recta i de 5 i 7,5 sobre l'altra: poden ser paral·leles les rectes que els determinen?", r"c) Con rectas paralelas, \(\overline{AB}=2{,}5\), \(\overline{A'B'}=4\) y \(\overline{B'C'}=6\). Calcula \(\overline{BC}\). d) Segmentos de 4 y 6 sobre una recta y de 5 y 7,5 sobre la otra: ¿pueden ser paralelas las rectas que los determinan?", r"c) With parallel lines, \(\overline{AB}=2.5\), \(\overline{A'B'}=4\) and \(\overline{B'C'}=6\). Find \(\overline{BC}\). d) Segments of 4 and 6 on one line and 5 and 7.5 on the other: can the lines that mark them be parallel?")),
  ('★★★', L(r"e) Dividim un segment de 36 cm en parts proporcionals a 2, 3 i 4. Quant fa cada part?", r"e) Dividimos un segmento de 36 cm en partes proporcionales a 2, 3 y 4. ¿Cuánto mide cada parte?", r"e) A 36 cm segment is divided into parts proportional to 2, 3 and 4. How long is each part?"))],
  P(r"a) \(8x=120\Rightarrow x=15\). b) \(\frac39=\frac2x\Rightarrow x=6\). c) \(\frac{2{,}5}{x}=\frac46\Rightarrow x=3{,}75\). d) Sí: \(4\cdot7{,}5=6\cdot5=30\). e) \(\frac{36}{2+3+4}=4\): parts de 8, 12 i 16 cm.",
    r"a) \(8x=120\Rightarrow x=15\). b) \(\frac39=\frac2x\Rightarrow x=6\). c) \(\frac{2{,}5}{x}=\frac46\Rightarrow x=3{,}75\). d) Sí: \(4\cdot7{,}5=6\cdot5=30\). e) \(\frac{36}{2+3+4}=4\): partes de 8, 12 y 16 cm.",
    r"a) \(8x=120\Rightarrow x=15\). b) \(\frac39=\frac2x\Rightarrow x=6\). c) \(\frac{2.5}{x}=\frac46\Rightarrow x=3.75\). d) Yes: \(4\cdot7.5=6\cdot5=30\). e) \(\frac{36}{2+3+4}=4\): parts of 8, 12 and 16 cm."))
ck(R(120, 8), 15); ck(R(9 * 2, 3), 6); ck(R(25, 10) * 6 / 4, 3.75); assert 4 * R(75, 10) == 6 * 5 == 30; ck(R(36, 9), 4)
