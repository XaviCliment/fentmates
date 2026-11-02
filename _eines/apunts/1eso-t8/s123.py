# Apartats 8.1-8.3 dels apunts de la Unitat 8 de 1r ESO: perímetre i àrea (unitats de longitud i de superfície),
# perímetre dels polígons, àrea del quadrat i del rectangle.
from comu import *

def T_(P, t, **o): return ('txt', P, t, o)
def useg(lab, items, first=0):
    """grup de botons amb etiqueta (el giny en llig el valor amb segs())"""
    return (f'<div class="wrow"><span class="wl">{lab}</span><div class="seg" role="group">'
            + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{str(i == first).lower()}">{t}</button>' for i, (k, t) in enumerate(items)) + '</div></div>')

# =====================================================================
# 8.1 Perímetre i àrea. Unitats de mesura
# =====================================================================
C_L = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (0, 2)]
C_A = [(x, y) for x in range(6) for y in range(2)]
C_B = [(x, y) for x in range(4) for y in range(3)]
C_C = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1), (2, 2), (1, 2), (3, 2), (2, 3), (0, 1), (4, 1)]
def gfig(cs, w, h, cap, W=170):
    return G(cells(cs) + grid(0, 0, w, h), W=W, pad=10, cap=cap)
assert len(C_L) == 7 and cellper(C_L) == 14 and len(C_A) == len(C_B) == len(C_C) == 12
assert cellper(C_A) == 16 and cellper(C_B) == 14 and cellper(C_C) == 26

s1 = box('def', L('Perímetre i àrea', 'Perímetro y área', 'Perimeter and area'),
  ul(L(r"El <strong>perímetre</strong> d'una figura plana és la <strong>longitud del seu contorn</strong>: el camí que faríem si la vorejàrem una volta sencera. Es mesura en unitats de <strong>longitud</strong>: m, cm, km…",
       r"El <strong>perímetro</strong> de una figura plana es la <strong>longitud de su contorno</strong>: el camino que haríamos si la rodeáramos una vuelta entera. Se mide en unidades de <strong>longitud</strong>: m, cm, km…",
       r"The <strong>perimeter</strong> of a plane shape is the <strong>length of its boundary</strong>: the distance you'd walk going once all the way round it. It's measured in units of <strong>length</strong>: m, cm, km…"),
     L(r"L'<strong>àrea</strong> és la mesura de la <strong>superfície</strong> que ocupa la figura: quant de lloc hi ha dins. Es mesura en unitats de <strong>superfície</strong>, que són quadrats: \(1\ \text{cm}^2\) és l'àrea d'un quadrat d'1 cm de costat.",
       r"El <strong>área</strong> es la medida de la <strong>superficie</strong> que ocupa la figura: cuánto sitio hay dentro. Se mide en unidades de <strong>superficie</strong>, que son cuadrados: \(1\ \text{cm}^2\) es el área de un cuadrado de 1 cm de lado.",
       r"The <strong>area</strong> measures the <strong>surface</strong> the shape covers: how much room there is inside. It's measured in units of <strong>area</strong>, which are squares: \(1\ \text{cm}^2\) is the area of a square with 1 cm sides."))
  + P(r"En una quadrícula de quadrets d'1 cm, l'àrea és el <strong>nombre de quadrets</strong> de dins i el perímetre, el <strong>nombre de costats de quadret</strong> del contorn:",
      r"En una cuadrícula de cuadraditos de 1 cm, el área es el <strong>número de cuadraditos</strong> de dentro y el perímetro, el <strong>número de lados de cuadradito</strong> del contorno:",
      r"On a grid of 1 cm squares, the area is the <strong>number of squares</strong> inside and the perimeter is the <strong>number of square sides</strong> along the boundary:")
  + figs(gfig(C_L, 4, 3, L(r'\(A=7\ \text{cm}^2\), \(P=14\ \text{cm}\)', r'\(A=7\ \text{cm}^2\), \(P=14\ \text{cm}\)', r'\(A=7\ \text{cm}^2\), \(P=14\ \text{cm}\)')))
  + note(r"Àrea i perímetre són coses diferents. Les tres figures següents tenen la <strong>mateixa àrea</strong> (12 quadrets) però <strong>perímetres diferents</strong>:",
         r"Área y perímetro son cosas diferentes. Las tres figuras siguientes tienen la <strong>misma área</strong> (12 cuadraditos) pero <strong>perímetros diferentes</strong>:",
         r"Area and perimeter are different things. The three shapes below have the <strong>same area</strong> (12 squares) but <strong>different perimeters</strong>:", '⚠️')
  + figs(gfig(C_A, 6, 2, r'\(A=12,\ P=16\)', 200), gfig(C_B, 4, 3, r'\(A=12,\ P=14\)', 140), gfig(C_C, 5, 4, r'\(A=12,\ P=26\)', 160), three=True)
  + widget('w-grid', '🟩', L('Dibuixa una figura i mesura-la', 'Dibuja una figura y mídela', 'Draw a shape and measure it'),
           ['<p class="hint-s">' + L("Toca els quadrets per pintar-los o esborrar-los. Cada quadret fa 1 cm de costat.", "Toca los cuadraditos para pintarlos o borrarlos. Cada cuadradito mide 1 cm de lado.", "Tap the squares to colour or clear them. Each square has 1 cm sides.") + '</p>',
            ('<div class="wrow"><button class="btn" type="button" data-a="rnd">🎲 ' + L("Una figura a l'atzar", "Una figura al azar", "A random shape") + '</button><button class="btn" type="button" data-a="rect">▭ ' + L("Un rectangle", "Un rectángulo", "A rectangle") + '</button><button class="btn" type="button" data-a="clr">✕ ' + L("Esborra", "Borrar", "Clear") + '</button></div>')],
           out='<div class="gout"></div>')
  + drill('quad', 'Entrena: compta quadrets i costats', 'Entrena: cuenta cuadraditos y lados', 'Train: count squares and sides'))

UL = ['km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm']
s1 += box('prop', L('Unitats de longitud i de superfície', 'Unidades de longitud y de superficie', 'Units of length and of area'),
  P(r"Les unitats de <strong>longitud</strong> van de 10 en 10: cada unitat és 10 vegades la següent.",
    r"Las unidades de <strong>longitud</strong> van de 10 en 10: cada unidad es 10 veces la siguiente.",
    r"Units of <strong>length</strong> go in tens: each unit is 10 times the next one.")
  + tbl(UL, [['1 000 m', '100 m', '10 m', '1 m', '0,1 m', '0,01 m', '0,001 m']], 'c')
  + D(r"\text{km}\ \underset{\times10}{\longrightarrow}\ \text{hm}\ \underset{\times10}{\longrightarrow}\ \text{dam}\ \underset{\times10}{\longrightarrow}\ \text{m}\ \underset{\times10}{\longrightarrow}\ \text{dm}\ \underset{\times10}{\longrightarrow}\ \text{cm}\ \underset{\times10}{\longrightarrow}\ \text{mm}")
  + P(r"Les unitats de <strong>superfície</strong> van de <strong>100 en 100</strong>. Per què? Un quadrat d'1 m de costat fa 10 dm de costat, i per tant conté \(10\times10=100\) quadrats d'1 dm de costat:",
      r"Las unidades de <strong>superficie</strong> van de <strong>100 en 100</strong>. ¿Por qué? Un cuadrado de 1 m de lado mide 10 dm de lado, y por tanto contiene \(10\times10=100\) cuadrados de 1 dm de lado:",
      r"Units of <strong>area</strong> go in <strong>hundreds</strong>. Why? A square with 1 m sides is 10 dm long on each side, so it holds \(10\times10=100\) squares with 1 dm sides:")
  + figs(G([('poly', [(0, 0), (10, 0), (10, 10), (0, 10)], 'gf')] + grid(0, 0, 10, 10) + [('poly', [(0, 0), (1, 0), (1, 1), (0, 1)], 'tr'),
           T_((5, 0), '1 m = 10 dm', dy=16), T_((0.5, 1), r'1 dm²', dy=-6, a='start', cls='hot')], W=200, pad=22,
           cap=L(r'\(1\ \text{m}^2=100\ \text{dm}^2\)', r'\(1\ \text{m}^2=100\ \text{dm}^2\)', r'\(1\ \text{m}^2=100\ \text{dm}^2\)')))
  + tbl([u + '²' for u in UL], [['1 000 000 m²', '10 000 m²', '100 m²', '1 m²', '0,01 m²', '0,0001 m²', '0,000001 m²'],
                               ['', L('hectàrea (ha)', 'hectárea (ha)', 'hectare (ha)'), L('àrea (a)', 'área (a)', 'are (a)'), L('centiàrea (ca)', 'centiárea (ca)', 'centiare (ca)'), '', '', '']], 'c')
  + D(r"\text{km}^2\ \underset{\times100}{\longrightarrow}\ \text{hm}^2\ \underset{\times100}{\longrightarrow}\ \text{dam}^2\ \underset{\times100}{\longrightarrow}\ \text{m}^2\ \underset{\times100}{\longrightarrow}\ \text{dm}^2\ \underset{\times100}{\longrightarrow}\ \text{cm}^2\ \underset{\times100}{\longrightarrow}\ \text{mm}^2")
  + ul(L(r"Per a passar a una unitat <strong>més menuda</strong>, <strong>multipliquem</strong> (per 10 o per 100 a cada pas). Per a passar a una <strong>més gran</strong>, <strong>dividim</strong>.",
         r"Para pasar a una unidad <strong>más pequeña</strong>, <strong>multiplicamos</strong> (por 10 o por 100 en cada paso). Para pasar a una <strong>más grande</strong>, <strong>dividimos</strong>.",
         r"To change to a <strong>smaller</strong> unit, <strong>multiply</strong> (by 10 or by 100 for each step). To change to a <strong>bigger</strong> one, <strong>divide</strong>."),
       L(r"Les <strong>unitats agràries</strong> serveixen per a mesurar camps: \(1\ \text{ha}=1\ \text{hm}^2=10\,000\ \text{m}^2\) (un quadrat de 100 m de costat) i \(1\ \text{a}=1\ \text{dam}^2=100\ \text{m}^2\).",
         r"Las <strong>unidades agrarias</strong> sirven para medir campos: \(1\ \text{ha}=1\ \text{hm}^2=10\,000\ \text{m}^2\) (un cuadrado de 100 m de lado) y \(1\ \text{a}=1\ \text{dam}^2=100\ \text{m}^2\).",
         r"<strong>Land units</strong> are used to measure fields: \(1\ \text{ha}=1\ \text{hm}^2=10\,000\ \text{m}^2\) (a square with 100 m sides) and \(1\ \text{a}=1\ \text{dam}^2=100\ \text{m}^2\)."))
  + D(r"3{,}5\ \text{m}=3{,}5\cdot100=350\ \text{cm}\qquad 3{,}5\ \text{m}^2=3{,}5\cdot10\,000=35\,000\ \text{cm}^2")
  + widget('w-conv', '🔁', L("Canvi d'unitats", 'Cambio de unidades', 'Unit converter'),
           [seg([('l', L('Longitud', 'Longitud', 'Length')), ('s', L('Superfície', 'Superficie', 'Area'))]),
            '<div class="wrow">' + tin('v', L('Quantitat', 'Cantidad', 'Amount'), '3,5', 'm') + '</div>',
            useg(L('De:', 'De:', 'From:'), [(str(i), u) for i, u in enumerate(UL)], 3), useg(L('A:', 'A:', 'To:'), [(str(i), u) for i, u in enumerate(UL)], 5)],
           out='<div class="hsteps"></div>')
  + drill('conv', "Entrena: canvis d'unitats", 'Entrena: cambios de unidades', 'Train: unit conversions'))
ck(R(35, 10) * 100, 350); ck(R(35, 10) * 10000, 35000)

F_P1 = G(cells([(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1), (3, 2)]) + grid(0, 0, 4, 3), W=150, pad=10)
s1 += levels(
 [prob(L(r"Expressa en metres: a) 3,5 km; b) 245 cm; c) 8 dam; d) 62 mm.", r"Expresa en metros: a) 3,5 km; b) 245 cm; c) 8 dam; d) 62 mm.", r"Write in metres: a) 3.5 km; b) 245 cm; c) 8 dam; d) 62 mm."),
       P(r"Del km al m hi ha 3 passos (×1000); del cm al m, 2 passos cap amunt (:100):", r"Del km al m hay 3 pasos (×1000); del cm al m, 2 pasos hacia arriba (:100):", r"From km to m is 3 steps (×1000); from cm to m is 2 steps up (÷100):"),
       D(r"\text{a) } 3{,}5\cdot1000=\boxed{3500\ \text{m}}\qquad \text{b) } 245:100=\boxed{2{,}45\ \text{m}}\qquad \text{c) } 8\cdot10=\boxed{80\ \text{m}}\qquad \text{d) } 62:1000=\boxed{0{,}062\ \text{m}}")),
  prob(L(r"Compta l'àrea i el perímetre d'aquesta figura (cada quadret fa 1 cm de costat).", r"Cuenta el área y el perímetro de esta figura (cada cuadradito mide 1 cm de lado).", r"Count the area and the perimeter of this shape (each square has 1 cm sides).") + figs(F_P1),
       P(r"Hi ha 8 quadrets pintats i, si vorejem la figura, comptem 14 costats de quadret:", r"Hay 8 cuadraditos pintados y, si rodeamos la figura, contamos 14 lados de cuadradito:", r"There are 8 shaded squares and going round the shape we count 14 square sides:"),
       D(r"A=\boxed{8\ \text{cm}^2}\qquad P=\boxed{14\ \text{cm}}"))],
 [prob(L(r"Expressa en m²: a) 4 dam²; b) 25 000 cm²; c) 2,3 ha; d) 0,05 km².", r"Expresa en m²: a) 4 dam²; b) 25 000 cm²; c) 2,3 ha; d) 0,05 km².", r"Write in m²: a) 4 dam²; b) 25 000 cm²; c) 2.3 ha; d) 0.05 km²."),
       P(r"Ara cada pas és ×100 o :100. Una hectàrea és un hm² (2 passos per damunt del m²):", r"Ahora cada paso es ×100 o :100. Una hectárea es un hm² (2 pasos por encima del m²):", r"Now each step is ×100 or ÷100. A hectare is one hm² (2 steps above m²):"),
       D(r"\text{a) } 4\cdot100=\boxed{400\ \text{m}^2}\qquad \text{b) } 25\,000:10\,000=\boxed{2{,}5\ \text{m}^2}"),
       D(r"\text{c) } 2{,}3\cdot10\,000=\boxed{23\,000\ \text{m}^2}\qquad \text{d) } 0{,}05\cdot1\,000\,000=\boxed{50\,000\ \text{m}^2}")),
  prob(L(r"Una cinta de 3 m es talla en trossos de 15 cm. Quants trossos s'obtenen?", r"Una cinta de 3 m se corta en trozos de 15 cm. ¿Cuántos trozos se obtienen?", r"A 3 m ribbon is cut into 15 cm pieces. How many pieces do we get?"),
       P(r"Primer ho passem tot a la mateixa unitat:", r"Primero lo pasamos todo a la misma unidad:", r"First put everything in the same unit:"),
       D(r"3\ \text{m}=300\ \text{cm}\qquad 300:15=\boxed{20\ \text{%s}}" % Lt('trossos', 'trozos', 'pieces')))],
 [prob(L(r"Un camp de 3,6 ha es dividix en parcel·les de 450 m². Quantes parcel·les hi ha?", r"Un campo de 3,6 ha se divide en parcelas de 450 m². ¿Cuántas parcelas hay?", r"A 3.6 ha field is split into 450 m² plots. How many plots are there?"),
       D(r"3{,}6\ \text{ha}=3{,}6\cdot10\,000=36\,000\ \text{m}^2\qquad 36\,000:450=\boxed{80\ \text{%s}}" % Lt('parcel·les', 'parcelas', 'plots'))),
  prob(L(r"Amb 24 quadrets volem formar rectangles (sense trencar cap quadret). Quins rectangles es poden fer? Quin té el perímetre més menut?", r"Con 24 cuadraditos queremos formar rectángulos (sin romper ningún cuadradito). ¿Qué rectángulos se pueden hacer? ¿Cuál tiene el perímetro más pequeño?", r"We want to make rectangles with 24 squares (without breaking any). Which rectangles can we make? Which one has the smallest perimeter?"),
       P(r"Les dimensions són parelles de divisors de 24. Tots tenen la mateixa àrea, 24 cm², però no el mateix perímetre:", r"Las dimensiones son parejas de divisores de 24. Todos tienen la misma área, 24 cm², pero no el mismo perímetro:", r"The sides are pairs of divisors of 24. They all have the same area, 24 cm², but not the same perimeter:"),
       D(r"1\times24:\ P=50\qquad 2\times12:\ P=28\qquad 3\times8:\ P=22\qquad 4\times6:\ P=20"),
       P(r"El de perímetre més menut és el \(\boxed{4\times6}\): com més s'assembla a un quadrat, menys perímetre té.", r"El de perímetro más pequeño es el \(\boxed{4\times6}\): cuanto más se parece a un cuadrado, menos perímetro tiene.", r"The one with the smallest perimeter is \(\boxed{4\times6}\): the closer to a square, the smaller the perimeter."))])
assert len(F_P1) and cellper([(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1), (3, 2)]) == 14
ck(R(35, 10) * 1000, 3500); ck(R(245, 100), 2.45); ck(R(62, 1000), 0.062); ck(25000 / 10000, 2.5); ck(R(23, 10) * 10000, 23000); ck(R(5, 100) * 10**6, 50000)
ck(R(36, 10) * 10000 / 450, 80); assert [2 * (a + 24 // a) for a in (1, 2, 3, 4)] == [50, 28, 22, 20]
s1 += practice([
  ('★', L(r"a) 7,2 m en cm. b) 0,35 km en m. c) 3 m² en cm². d) 5600 dm² en m².", r"a) 7,2 m en cm. b) 0,35 km en m. c) 3 m² en cm². d) 5600 dm² en m².", r"a) 7.2 m in cm. b) 0.35 km in m. c) 3 m² in cm². d) 5600 dm² in m².")),
  ('★★', L(r"e) 1,2 ha en m². f) 850 m² en àrees. g) Quants quadrets d'1 cm² caben en un quadrat d'1 dm²?", r"e) 1,2 ha en m². f) 850 m² en áreas. g) ¿Cuántos cuadraditos de 1 cm² caben en un cuadrado de 1 dm²?", r"e) 1.2 ha in m². f) 850 m² in ares. g) How many 1 cm² squares fit in a 1 dm² square?")),
  ('★★★', L(r"h) Ordena de menor a major: 0,3 km², 25 ha, 400 000 m².", r"h) Ordena de menor a mayor: 0,3 km², 25 ha, 400 000 m².", r"h) Put in order from smallest to largest: 0.3 km², 25 ha, 400 000 m²."))],
  P(r"a) 720 cm. b) 350 m. c) 30 000 cm². d) 56 m². e) 12 000 m². f) 8,5 a. g) \(10\times10=100\). h) En m²: 300 000, 250 000 i 400 000: \(25\ \text{ha}<0{,}3\ \text{km}^2<400\,000\ \text{m}^2\).",
    r"a) 720 cm. b) 350 m. c) 30 000 cm². d) 56 m². e) 12 000 m². f) 8,5 a. g) \(10\times10=100\). h) En m²: 300 000, 250 000 y 400 000: \(25\ \text{ha}<0{,}3\ \text{km}^2<400\,000\ \text{m}^2\).",
    r"a) 720 cm. b) 350 m. c) 30 000 cm². d) 56 m². e) 12 000 m². f) 8.5 a. g) \(10\times10=100\). h) In m²: 300 000, 250 000 and 400 000: \(25\ \text{ha}<0.3\ \text{km}^2<400\,000\ \text{m}^2\)."))
ck(R(72, 10) * 100, 720); ck(R(35, 100) * 1000, 350); ck(3 * 10000, 30000); ck(R(5600, 100), 56); ck(R(12, 10) * 10000, 12000); ck(R(850, 100), 8.5)
ck(R(3, 10) * 10**6, 300000); ck(25 * 10000, 250000)

# =====================================================================
# 8.2 Perímetre dels polígons
# =====================================================================
def tk(V, n=1):
    return [('tick', V[i], V[(i + 1) % len(V)], n) for i in range(len(V))]
PQ = [(0, 0), (3, 0), (3, 3), (0, 3)]
PR = [(0, 0), (4.6, 0), (4.6, 2.6), (0, 2.6)]
PT = [(0, 0), (4.4, 0), (1.4, 2.8)]
PH = reg(6, 1.7)
PB = [(0, 0), (3, 0), (4.6, 2.2), (1.6, 2.2)]
s2 = box('def', L('Perímetre d\'un polígon', 'Perímetro de un polígono', 'Perimeter of a polygon'),
  P(r"El perímetre d'un polígon és la <strong>suma de les longituds de tots els seus costats</strong>. Quan hi ha costats iguals, podem multiplicar:",
    r"El perímetro de un polígono es la <strong>suma de las longitudes de todos sus lados</strong>. Cuando hay lados iguales, podemos multiplicar:",
    r"The perimeter of a polygon is the <strong>sum of the lengths of all its sides</strong>. When some sides are equal we can multiply:")
  + figs(G([('poly', PT, 'gf'), T_(off(PT[0], PT[1], -0.3), 'a'), T_(off(PT[1], PT[2], -0.3), 'b'), T_(off(PT[2], PT[0], -0.3), 'c')], W=170, cap=L(r'Triangle: \(P=a+b+c\)', r'Triángulo: \(P=a+b+c\)', r'Triangle: \(P=a+b+c\)')),
         G([('poly', PQ, 'gf')] + tk(PQ) + [T_((1.5, 0), 'l', dy=16)], W=120, cap=L(r'Quadrat: \(P=4\cdot l\)', r'Cuadrado: \(P=4\cdot l\)', r'Square: \(P=4\cdot l\)')),
         G([('poly', PR, 'gf'), ('tick', PR[0], PR[1], 1), ('tick', PR[2], PR[3], 1), ('tick', PR[1], PR[2], 2), ('tick', PR[3], PR[0], 2), T_((2.3, 0), 'b', dy=16), T_((4.6, 1.3), 'h', dx=9, a='start')], W=170,
           cap=L(r'Rectangle: \(P=2\cdot b+2\cdot h\)', r'Rectángulo: \(P=2\cdot b+2\cdot h\)', r'Rectangle: \(P=2\cdot b+2\cdot h\)')),
         G([('poly', PB, 'gf'), ('tick', PB[0], PB[1], 1), ('tick', PB[2], PB[3], 1), ('tick', PB[1], PB[2], 2), ('tick', PB[3], PB[0], 2), T_((1.5, 0), 'b', dy=16), T_(off(PB[1], PB[2], -0.3), 'c', a='start')], W=170,
           cap=L(r'Romboide: \(P=2\cdot b+2\cdot c\)', r'Romboide: \(P=2\cdot b+2\cdot c\)', r'Parallelogram: \(P=2\cdot b+2\cdot c\)')),
         G([('poly', PH, 'gf')] + tk(PH) + [T_(off(PH[0], PH[1], -0.3), 'l')], W=140, cap=L(r'Polígon regular de \(n\) costats: \(P=n\cdot l\)', r'Polígono regular de \(n\) lados: \(P=n\cdot l\)', r'Regular polygon with \(n\) sides: \(P=n\cdot l\)')), three=True)
  + note(r"Abans de sumar, comprova que <strong>tots els costats estan en la mateixa unitat</strong>. Un rectangle de 1,2 m × 80 cm té \(P=2\cdot120+2\cdot80=400\ \text{cm}=4\ \text{m}\).",
         r"Antes de sumar, comprueba que <strong>todos los lados están en la misma unidad</strong>. Un rectángulo de 1,2 m × 80 cm tiene \(P=2\cdot120+2\cdot80=400\ \text{cm}=4\ \text{m}\).",
         r"Before adding, check that <strong>all the sides are in the same unit</strong>. A 1.2 m × 80 cm rectangle has \(P=2\cdot120+2\cdot80=400\ \text{cm}=4\ \text{m}\).", '⚠️')
  + P(r"També podem fer el camí al revés: si coneixem el perímetre d'un polígon regular, el costat és \(l=P:n\).",
      r"También podemos hacer el camino al revés: si conocemos el perímetro de un polígono regular, el lado es \(l=P:n\).",
      r"We can also work backwards: if we know the perimeter of a regular polygon, its side is \(l=P\div n\).")
  + widget('w-per', '⬠', L('Perímetre dels polígons regulars', 'Perímetro de los polígonos regulares', 'Perimeter of regular polygons'),
           ['<div class="wrow">' + rng('n', 3, 10, 1, 5, 'n') + rng('l', 0.5, 12, 0.5, 4, 'l') + '</div>'], out='<div class="gout"></div>')
  + drill('per', 'Entrena: calcula perímetres', 'Entrena: calcula perímetros', 'Train: work out perimeters'))
ck(2 * 120 + 2 * 80, 400)
s2 += levels(
 [prob(L(r"Calcula el perímetre d'un triangle de costats 6 cm, 8 cm i 11 cm.", r"Calcula el perímetro de un triángulo de lados 6 cm, 8 cm y 11 cm.", r"Find the perimeter of a triangle with sides of 6 cm, 8 cm and 11 cm."),
       D(r"P=6+8+11=\boxed{25\ \text{cm}}")),
  prob(L(r"Calcula el perímetre d'un rectangle de 12 m × 7,5 m i el d'un hexàgon regular de 4,2 cm de costat.", r"Calcula el perímetro de un rectángulo de 12 m × 7,5 m y el de un hexágono regular de 4,2 cm de lado.", r"Find the perimeter of a 12 m × 7.5 m rectangle and of a regular hexagon with 4.2 cm sides."),
       D(r"P_{\text{%s}}=2\cdot12+2\cdot7{,}5=24+15=\boxed{39\ \text{m}}\qquad P_{\text{%s}}=6\cdot4{,}2=\boxed{25{,}2\ \text{cm}}" % (Lt('rect.', 'rect.', 'rect.'), Lt('hex.', 'hex.', 'hex.'))))],
 [prob(L(r"Un pentàgon regular té 42,5 cm de perímetre. Quant fa cada costat?", r"Un pentágono regular tiene 42,5 cm de perímetro. ¿Cuánto mide cada lado?", r"A regular pentagon has a 42.5 cm perimeter. How long is each side?"),
       D(r"l=P:n=42{,}5:5=\boxed{8{,}5\ \text{cm}}")),
  prob(L(r"Un rectangle té 50 cm de perímetre i la base fa 15 cm. Quant fa l'altura?", r"Un rectángulo tiene 50 cm de perímetro y la base mide 15 cm. ¿Cuánto mide la altura?", r"A rectangle has a 50 cm perimeter and a 15 cm base. How tall is it?"),
       P(r"Les dues bases fan \(2\cdot15=30\) cm. La resta del perímetre són les dues altures:", r"Las dos bases miden \(2\cdot15=30\) cm. El resto del perímetro son las dos alturas:", r"The two bases make \(2\cdot15=30\) cm. The rest of the perimeter is the two heights:"),
       D(r"50-30=20\qquad h=20:2=\boxed{10\ \text{cm}}"))],
 [prob(L(r"Volem tancar un hort rectangular de 25 m × 18 m amb tela metàl·lica, deixant una porta de 3 m. Si la tela costa 4,50 € el metre, quant pagarem?", r"Queremos cercar un huerto rectangular de 25 m × 18 m con tela metálica, dejando una puerta de 3 m. Si la tela cuesta 4,50 € el metro, ¿cuánto pagaremos?", r"We want to fence a 25 m × 18 m rectangular vegetable garden with wire mesh, leaving a 3 m gate. If the mesh costs €4.50 per metre, how much will we pay?"),
       D(r"P=2\cdot25+2\cdot18=86\ \text{m}\qquad 86-3=83\ \text{m}\ \text{%s}" % Lt('de tela', 'de tela', 'of mesh')),
       D(r"83\cdot4{,}50=\boxed{373{,}50\ \text{€}}")),
  prob(L(r"Un triangle isòsceles té 34 cm de perímetre i la base desigual fa 10 cm. Quant fan els altres dos costats?", r"Un triángulo isósceles tiene 34 cm de perímetro y la base desigual mide 10 cm. ¿Cuánto miden los otros dos lados?", r"An isosceles triangle has a 34 cm perimeter and its unequal base is 10 cm. How long are the other two sides?"),
       D(r"34-10=24\qquad 24:2=\boxed{12\ \text{cm}\ \text{%s}}" % Lt('cadascun', 'cada uno', 'each')))])
ck(6 + 8 + 11, 25); ck(2 * 12 + 2 * R(75, 10), 39); ck(6 * R(42, 10), 25.2); ck(R(425, 10) / 5, 8.5); ck((50 - 30) / 2, 10); ck(2 * 25 + 2 * 18, 86); ck(83 * R(45, 10), 373.5); ck((34 - 10) / 2, 12)
s2 += practice([
  ('★', L(r"a) Perímetre d'un quadrat de 7,5 cm de costat. b) Perímetre d'un octàgon regular de 6 cm de costat.", r"a) Perímetro de un cuadrado de 7,5 cm de lado. b) Perímetro de un octógono regular de 6 cm de lado.", r"a) Perimeter of a square with 7.5 cm sides. b) Perimeter of a regular octagon with 6 cm sides.")),
  ('★★', L(r"c) Perímetre, en cm, d'un rectangle de 1,5 m × 80 cm. d) Un decàgon regular té 65 cm de perímetre. Quant fa el costat?", r"c) Perímetro, en cm, de un rectángulo de 1,5 m × 80 cm. d) Un decágono regular tiene 65 cm de perímetro. ¿Cuánto mide el lado?", r"c) Perimeter, in cm, of a 1.5 m × 80 cm rectangle. d) A regular decagon has a 65 cm perimeter. How long is its side?")),
  ('★★★', L(r"e) La base d'un rectangle fa el doble que l'altura i el perímetre fa 48 cm. Quant fan la base i l'altura?", r"e) La base de un rectángulo mide el doble que la altura y el perímetro mide 48 cm. ¿Cuánto miden la base y la altura?", r"e) A rectangle's base is twice its height and its perimeter is 48 cm. How long are the base and the height?"))],
  P(r"a) 30 cm. b) 48 cm. c) \(2\cdot150+2\cdot80=460\) cm. d) 6,5 cm. e) El perímetre són 6 altures: \(h=48:6=8\) cm i \(b=16\) cm.",
    r"a) 30 cm. b) 48 cm. c) \(2\cdot150+2\cdot80=460\) cm. d) 6,5 cm. e) El perímetro son 6 alturas: \(h=48:6=8\) cm y \(b=16\) cm.",
    r"a) 30 cm. b) 48 cm. c) \(2\cdot150+2\cdot80=460\) cm. d) 6.5 cm. e) The perimeter is 6 heights: \(h=48\div6=8\) cm and \(b=16\) cm."))
ck(4 * R(75, 10), 30); ck(8 * 6, 48); ck(2 * 150 + 2 * 80, 460); ck(R(65, 10), 6.5); ck(2 * 16 + 2 * 8, 48)

# =====================================================================
# 8.3 Àrea del quadrat i del rectangle
# =====================================================================
s3 = box('prop', L('Àrea del rectangle i del quadrat', 'Área del rectángulo y del cuadrado', 'Area of a rectangle and of a square'),
  P(r"Un rectangle de 5 cm de base i 3 cm d'altura es pot omplir amb <strong>3 files de 5 quadrets</strong> d'1 cm²: en total, \(5\cdot3=15\ \text{cm}^2\). En general, l'àrea és la <strong>base per l'altura</strong>:",
    r"Un rectángulo de 5 cm de base y 3 cm de altura se puede llenar con <strong>3 filas de 5 cuadraditos</strong> de 1 cm²: en total, \(5\cdot3=15\ \text{cm}^2\). En general, el área es la <strong>base por la altura</strong>:",
    r"A rectangle with a 5 cm base and a 3 cm height can be filled with <strong>3 rows of 5 squares</strong> of 1 cm²: \(5\cdot3=15\ \text{cm}^2\) in total. In general, the area is <strong>base times height</strong>:")
  + figs(G([('poly', [(0, 0), (5, 0), (5, 3), (0, 3)], 'gf')] + grid(0, 0, 5, 3) + [T_((2.5, 0), 'b = 5 cm', dy=16), T_((5, 1.5), 'h = 3 cm', dx=8, a='start')], W=230, pad=34,
           cap=L(r'Rectangle: \(A=b\cdot h=5\cdot3=15\ \text{cm}^2\)', r'Rectángulo: \(A=b\cdot h=5\cdot3=15\ \text{cm}^2\)', r'Rectangle: \(A=b\cdot h=5\cdot3=15\ \text{cm}^2\)')),
         G([('poly', [(0, 0), (4, 0), (4, 4), (0, 4)], 'gf')] + grid(0, 0, 4, 4) + [T_((2, 0), 'l = 4 cm', dy=16)], W=150, pad=26,
           cap=L(r'Quadrat: \(A=l\cdot l=l^2=16\ \text{cm}^2\)', r'Cuadrado: \(A=l\cdot l=l^2=16\ \text{cm}^2\)', r'Square: \(A=l\cdot l=l^2=16\ \text{cm}^2\)')))
  + D(r"A_{\text{%s}}=b\cdot h\qquad\qquad A_{\text{%s}}=l^2" % (Lt('rectangle', 'rectángulo', 'rectangle'), Lt('quadrat', 'cuadrado', 'square')))
  + ul(L(r"La fórmula també val amb <strong>decimals</strong>: un rectangle de 4,5 m × 3 m té \(A=4{,}5\cdot3=13{,}5\ \text{m}^2\).", r"La fórmula también vale con <strong>decimales</strong>: un rectángulo de 4,5 m × 3 m tiene \(A=4{,}5\cdot3=13{,}5\ \text{m}^2\).", r"The formula also works with <strong>decimals</strong>: a 4.5 m × 3 m rectangle has \(A=4.5\cdot3=13.5\ \text{m}^2\)."),
       L(r"Si coneixem l'àrea i la base, l'altura és \(h=A:b\). Si un quadrat té 49 cm², el costat és el nombre que elevat al quadrat dona 49: \(l=\sqrt{49}=7\ \text{cm}\).", r"Si conocemos el área y la base, la altura es \(h=A:b\). Si un cuadrado tiene 49 cm², el lado es el número que elevado al cuadrado da 49: \(l=\sqrt{49}=7\ \text{cm}\).", r"If we know the area and the base, the height is \(h=A\div b\). If a square has an area of 49 cm², its side is the number whose square is 49: \(l=\sqrt{49}=7\ \text{cm}\)."))
  + note(r"Les dues mesures han d'estar en la <strong>mateixa unitat</strong>, i el resultat ix en la unitat <strong>al quadrat</strong>: cm·cm = cm².",
         r"Las dos medidas deben estar en la <strong>misma unidad</strong>, y el resultado sale en la unidad <strong>al cuadrado</strong>: cm·cm = cm².",
         r"Both lengths must be in the <strong>same unit</strong>, and the answer comes out in that unit <strong>squared</strong>: cm·cm = cm².", '⚠️')
  + widget('w-rect', '▦', L('Rectangles en la quadrícula', 'Rectángulos en la cuadrícula', 'Rectangles on the grid'),
           ['<div class="wrow">' + rng('b', 1, 12, 1, 6, 'b') + rng('h', 1, 9, 1, 4, 'h') + '</div>'], out='<div class="gout"></div>')
  + drill('rect', 'Entrena: àrea del rectangle i del quadrat', 'Entrena: área del rectángulo y del cuadrado', 'Train: area of rectangles and squares'))
ck(R(45, 10) * 3, 13.5)
s3 += levels(
 [prob(L(r"Calcula l'àrea i el perímetre d'un rectangle de 8 cm × 5 cm.", r"Calcula el área y el perímetro de un rectángulo de 8 cm × 5 cm.", r"Find the area and the perimeter of an 8 cm × 5 cm rectangle."),
       D(r"A=8\cdot5=\boxed{40\ \text{cm}^2}\qquad P=2\cdot8+2\cdot5=\boxed{26\ \text{cm}}")),
  prob(L(r"Calcula l'àrea i el perímetre d'un quadrat de 9 m de costat.", r"Calcula el área y el perímetro de un cuadrado de 9 m de lado.", r"Find the area and the perimeter of a square with 9 m sides."),
       D(r"A=9^2=\boxed{81\ \text{m}^2}\qquad P=4\cdot9=\boxed{36\ \text{m}}"))],
 [prob(L(r"Un rectangle té 96 cm² d'àrea i 12 cm de base. Quant fa l'altura? I el perímetre?", r"Un rectángulo tiene 96 cm² de área y 12 cm de base. ¿Cuánto mide la altura? ¿Y el perímetro?", r"A rectangle has an area of 96 cm² and a 12 cm base. How tall is it? What's its perimeter?"),
       D(r"h=A:b=96:12=\boxed{8\ \text{cm}}\qquad P=2\cdot12+2\cdot8=\boxed{40\ \text{cm}}")),
  prob(L(r"Un quadrat té 36 m de perímetre. Calcula'n l'àrea.", r"Un cuadrado tiene 36 m de perímetro. Calcula su área.", r"A square has a 36 m perimeter. Find its area."),
       D(r"l=36:4=9\ \text{m}\qquad A=9^2=\boxed{81\ \text{m}^2}"))],
 [prob(L(r"Volem pintar una paret de 4,5 m × 2,8 m que té una porta de 0,9 m × 2 m. Quants m² cal pintar?", r"Queremos pintar una pared de 4,5 m × 2,8 m que tiene una puerta de 0,9 m × 2 m. ¿Cuántos m² hay que pintar?", r"We want to paint a 4.5 m × 2.8 m wall with a 0.9 m × 2 m door in it. How many m² do we need to paint?"),
       D(r"A_{\text{%s}}=4{,}5\cdot2{,}8=12{,}6\ \text{m}^2\qquad A_{\text{%s}}=0{,}9\cdot2=1{,}8\ \text{m}^2" % (Lt('paret', 'pared', 'wall'), Lt('porta', 'puerta', 'door'))),
       D(r"12{,}6-1{,}8=\boxed{10{,}8\ \text{m}^2}")),
  prob(L(r"El terra d'una habitació fa 6 m × 4 m. Quantes rajoles quadrades de 40 cm de costat calen per a cobrir-lo?", r"El suelo de una habitación mide 6 m × 4 m. ¿Cuántas baldosas cuadradas de 40 cm de lado hacen falta para cubrirlo?", r"A room's floor is 6 m × 4 m. How many square tiles with 40 cm sides are needed to cover it?"),
       P(r"Treballem en cm. Caben \(600:40=15\) rajoles al llarg i \(400:40=10\) a l'ample:", r"Trabajamos en cm. Caben \(600:40=15\) baldosas a lo largo y \(400:40=10\) a lo ancho:", r"Work in cm. \(600\div40=15\) tiles fit along the length and \(400\div40=10\) along the width:"),
       D(r"15\cdot10=\boxed{150\ \text{%s}}\qquad\left(\text{%s: }\ \frac{600\cdot400}{40\cdot40}=\frac{240\,000}{1600}=150\right)" % (Lt('rajoles', 'baldosas', 'tiles'), Lt('o bé', 'o bien', 'or'))))])
ck(8 * 5, 40); ck(2 * 8 + 2 * 5, 26); ck(81, 9 ** 2); ck(96 / 12, 8); ck(2 * 12 + 2 * 8, 40); ck(R(45, 10) * R(28, 10), 12.6); ck(R(9, 10) * 2, 1.8); ck(R(126, 10) - R(18, 10), 10.8)
ck((600 // 40) * (400 // 40), 150); ck(240000 / 1600, 150)
s3 += practice([
  ('★', L(r"a) Àrea d'un rectangle de 12 cm × 7 cm. b) Àrea d'un quadrat de 6,5 cm de costat.", r"a) Área de un rectángulo de 12 cm × 7 cm. b) Área de un cuadrado de 6,5 cm de lado.", r"a) Area of a 12 cm × 7 cm rectangle. b) Area of a square with 6.5 cm sides.")),
  ('★★', L(r"c) Un rectangle de 54 cm² fa 6 cm d'altura. Quant fan la base i el perímetre? d) Un quadrat té 64 cm² d'àrea. Quant fan el costat i el perímetre?", r"c) Un rectángulo de 54 cm² mide 6 cm de altura. ¿Cuánto miden la base y el perímetro? d) Un cuadrado tiene 64 cm² de área. ¿Cuánto miden el lado y el perímetro?", r"c) A 54 cm² rectangle is 6 cm tall. How long are its base and its perimeter? d) A square has an area of 64 cm². How long are its side and its perimeter?")),
  ('★★★', L(r"e) Un camp de futbol fa 105 m × 68 m. Quina és la seua àrea en m² i en hectàrees?", r"e) Un campo de fútbol mide 105 m × 68 m. ¿Cuál es su área en m² y en hectáreas?", r"e) A football pitch is 105 m × 68 m. What is its area in m² and in hectares?"))],
  P(r"a) 84 cm². b) 42,25 cm². c) \(b=9\) cm, \(P=30\) cm. d) \(l=8\) cm, \(P=32\) cm. e) 7140 m² = 0,714 ha.",
    r"a) 84 cm². b) 42,25 cm². c) \(b=9\) cm, \(P=30\) cm. d) \(l=8\) cm, \(P=32\) cm. e) 7140 m² = 0,714 ha.",
    r"a) 84 cm². b) 42.25 cm². c) \(b=9\) cm, \(P=30\) cm. d) \(l=8\) cm, \(P=32\) cm. e) 7140 m² = 0.714 ha."))
ck(12 * 7, 84); ck(R(65, 10) ** 2, 42.25); ck(54 / 6, 9); ck(2 * 9 + 2 * 6, 30); ck(8 ** 2, 64); ck(105 * 68, 7140); ck(R(7140, 10000), 0.714)
