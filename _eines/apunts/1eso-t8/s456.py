# Apartats 8.4-8.6 dels apunts de la Unitat 8 de 1r ESO: àrea del romboide i del triangle, del rombe i del trapezi,
# i dels polígons regulars i qualssevol.
from comu import *

def T_(P, t, **o): return ('txt', P, t, o)

# =====================================================================
# 8.4 Àrea del romboide i del triangle
# =====================================================================
RB = [(0, 0), (5, 0), (6.6, 2.6), (1.6, 2.6)]
F_CUT1 = [('poly', RB, 'gf'), ('poly', [(0, 0), (1.6, 0), (1.6, 2.6)], 'tr'), ('seg', (1.6, 0), (1.6, 2.6), 'd'), ('ra', (1.6, 0), (3, 0), (1.6, 2.6)),
          T_((2.5, 0), 'b', dy=16), T_((1.6, 1.3), 'h', dx=8, a='start')]
F_CUT2 = [('poly', [(1.6, 0), (6.6, 0), (6.6, 2.6), (1.6, 2.6)], 'gf'), ('poly', [(5, 0), (6.6, 0), (6.6, 2.6)], 'tr'), ('seg', (5, 0), (6.6, 2.6), 'd'),
          T_((4.1, 0), 'b', dy=16), T_((6.6, 1.3), 'h', dx=8, a='start')]
F_HALF = [('poly', [(0, 0), (5, 0), (1.6, 2.6)], 'tr'), ('poly', [(5, 0), (6.6, 2.6), (1.6, 2.6)], 'tl'), ('seg', (1.6, 0), (1.6, 2.6), 'd'), ('ra', (1.6, 0), (3, 0), (1.6, 2.6)),
          T_((2.5, 0), 'b', dy=16), T_((1.6, 1.3), 'h', dx=-7, a='end')]
def tri_h(C, cap):
    A, B = (0, 0), (4, 0)
    it = [('poly', [A, B, C], 'gf'), ('seg', (C[0], 0), C, 'd'), T_((2, 0), 'b', dy=16), T_((C[0], C[1] / 2), 'h', dx=7, a='start')]
    if C[0] > 4: it += [('seg', B, (C[0], 0), 'd')]
    it.append(('ra', (C[0], 0), (C[0] - 1 if C[0] > 0 else 1, 0), C))
    return G(it, W=150 if C[0] <= 4 else 190, cap=cap)
s4 = box('prop', L('Àrea del romboide', 'Área del romboide', 'Area of a parallelogram'),
  P(r"Si retallem el triangle d'un costat del romboide i l'enganxem a l'altre costat, obtenim un <strong>rectangle</strong> amb la mateixa base i la mateixa altura. Per tant:",
    r"Si recortamos el triángulo de un lado del romboide y lo pegamos en el otro lado, obtenemos un <strong>rectángulo</strong> con la misma base y la misma altura. Por tanto:",
    r"If we cut the triangle off one side of the parallelogram and stick it on the other side, we get a <strong>rectangle</strong> with the same base and the same height. So:")
  + figs(G(F_CUT1, W=210, cap=L('Retallem el triangle…', 'Recortamos el triángulo…', 'Cut off the triangle…')), G(F_CUT2, W=170, cap=L('…i el posem a l\'altre costat', '…y lo ponemos en el otro lado', '…and move it to the other side')))
  + D(r"A_{\text{romboide}}=b\cdot h")
  + note(r"L'<strong>altura</strong> és la distància entre les dues bases, mesurada <strong>perpendicularment</strong>. No és el costat inclinat!",
         r"La <strong>altura</strong> es la distancia entre las dos bases, medida <strong>perpendicularmente</strong>. ¡No es el lado inclinado!",
         r"The <strong>height</strong> is the distance between the two bases, measured <strong>at right angles</strong>. It isn't the slanted side!", '⚠️'))
s4 += box('prop', L('Àrea del triangle', 'Área del triángulo', 'Area of a triangle'),
  P(r"Una diagonal dividix el romboide en <strong>dos triangles iguals</strong>. Cada triangle és la meitat d'un romboide de la mateixa base i altura:",
    r"Una diagonal divide el romboide en <strong>dos triángulos iguales</strong>. Cada triángulo es la mitad de un romboide de la misma base y altura:",
    r"A diagonal splits the parallelogram into <strong>two equal triangles</strong>. Each triangle is half a parallelogram with the same base and height:")
  + figs(G(F_HALF, W=220))
  + D(r"A_{\text{%s}}=\frac{b\cdot h}{2}" % Lt('triangle', 'triángulo', 'triangle'))
  + P(r"L'altura és el segment perpendicular que va des del vèrtex oposat fins a la base (o fins a la prolongació de la base):",
      r"La altura es el segmento perpendicular que va desde el vértice opuesto hasta la base (o hasta la prolongación de la base):",
      r"The height is the perpendicular segment from the opposite vertex to the base (or to the base extended):")
  + figs(tri_h((1.4, 2.8), L('Acutangle: dins', 'Acutángulo: dentro', 'Acute: inside')), tri_h((0, 2.8), L('Rectangle: és un catet', 'Rectángulo: es un cateto', 'Right: it\'s a leg')), tri_h((5.6, 2.4), L('Obtusangle: fora', 'Obtusángulo: fuera', 'Obtuse: outside')), three=True)
  + note(r"En un <strong>triangle rectangle</strong>, els dos catets són base i altura: \(A=\dfrac{\text{%s}\cdot\text{%s}}{2}\)." % (Lt('catet', 'cateto', 'leg'), Lt('catet', 'cateto', 'leg')),
         r"En un <strong>triángulo rectángulo</strong>, los dos catetos son base y altura: \(A=\dfrac{\text{%s}\cdot\text{%s}}{2}\)." % (Lt('catet', 'cateto', 'leg'), Lt('catet', 'cateto', 'leg')),
         r"In a <strong>right triangle</strong>, the two legs are the base and the height: \(A=\dfrac{\text{%s}\cdot\text{%s}}{2}\)." % (Lt('catet', 'cateto', 'leg'), Lt('catet', 'cateto', 'leg')), '📐')
  + widget('w-shear', '◢', L('Mou el vèrtex: l\'àrea no canvia', 'Mueve el vértice: el área no cambia', 'Move the vertex: the area stays the same'),
           [seg([('ro', 'Romboide'), ('tr', L('Triangle', 'Triángulo', 'Triangle'))]),
            '<div class="wrow">' + rng('b', 2, 10, 1, 6, 'b') + rng('h', 1, 8, 1, 4, 'h') + rng('e', -3, 8, 0.5, 2, 'x') + '</div>'],
           out='<div class="gout"></div>')
  + drill('tri', "Entrena: àrea del romboide i del triangle", "Entrena: área del romboide y del triángulo", "Train: area of parallelograms and triangles"))
s4 += levels(
 [prob(L(r"Calcula l'àrea d'un romboide de 9 cm de base i 5 cm d'altura.", r"Calcula el área de un romboide de 9 cm de base y 5 cm de altura.", r"Find the area of a parallelogram with a 9 cm base and a 5 cm height."),
       D(r"A=b\cdot h=9\cdot5=\boxed{45\ \text{cm}^2}")),
  prob(L(r"Calcula l'àrea d'un triangle de 10 cm de base i 7 cm d'altura.", r"Calcula el área de un triángulo de 10 cm de base y 7 cm de altura.", r"Find the area of a triangle with a 10 cm base and a 7 cm height."),
       D(r"A=\frac{b\cdot h}{2}=\frac{10\cdot7}{2}=\frac{70}{2}=\boxed{35\ \text{cm}^2}"))],
 [prob(L(r"Els catets d'un triangle rectangle fan 6 cm i 8 cm, i la hipotenusa, 10 cm. Calcula'n l'àrea i el perímetre.", r"Los catetos de un triángulo rectángulo miden 6 cm y 8 cm, y la hipotenusa, 10 cm. Calcula su área y su perímetro.", r"The legs of a right triangle are 6 cm and 8 cm, and the hypotenuse is 10 cm. Find its area and its perimeter."),
       figs(G([('poly', [(0, 0), (8, 0), (0, 6)], 'gf'), ('ra', (0, 0), (1, 0), (0, 1)), T_((4, 0), '8', dy=16), T_((0, 3), '6', dx=-8, a='end'), T_(off((8, 0), (0, 6), -0.7), '10', a='start')], W=160)),
       P(r"Els catets són perpendiculars: un fa de base i l'altre d'altura. La hipotenusa només compta per al perímetre.", r"Los catetos son perpendiculares: uno hace de base y el otro de altura. La hipotenusa solo cuenta para el perímetro.", r"The legs are perpendicular: one is the base and the other the height. The hypotenuse only counts for the perimeter."),
       D(r"A=\frac{8\cdot6}{2}=\boxed{24\ \text{cm}^2}\qquad P=6+8+10=\boxed{24\ \text{cm}}")),
  prob(L(r"Un triangle té 30 cm² d'àrea i 12 cm de base. Quant fa l'altura?", r"Un triángulo tiene 30 cm² de área y 12 cm de base. ¿Cuánto mide la altura?", r"A triangle has an area of 30 cm² and a 12 cm base. How tall is it?"),
       P(r"Si \(\dfrac{b\cdot h}{2}=30\), aleshores \(b\cdot h=60\):", r"Si \(\dfrac{b\cdot h}{2}=30\), entonces \(b\cdot h=60\):", r"If \(\dfrac{b\cdot h}{2}=30\), then \(b\cdot h=60\):"),
       D(r"12\cdot h=60\ \Rightarrow\ h=60:12=\boxed{5\ \text{cm}}"))],
 [prob(L(r"Un triangle té 15 cm de base i 8 cm d'altura. Quina altura ha de tindre un altre triangle de 10 cm de base perquè tinga la mateixa àrea?", r"Un triángulo tiene 15 cm de base y 8 cm de altura. ¿Qué altura debe tener otro triángulo de 10 cm de base para que tenga la misma área?", r"A triangle has a 15 cm base and an 8 cm height. How tall must another triangle with a 10 cm base be to have the same area?"),
       D(r"A=\frac{15\cdot8}{2}=60\ \text{cm}^2\qquad \frac{10\cdot h}{2}=60\ \Rightarrow\ 10\cdot h=120\ \Rightarrow\ h=\boxed{12\ \text{cm}}")),
  prob(L(r"En el triangle de la figura (mesures en cm), calcula l'àrea de dues maneres: prenent com a base el costat de 10 cm i prenent com a base el de 8 cm.", r"En el triángulo de la figura (medidas en cm), calcula el área de dos maneras: tomando como base el lado de 10 cm y tomando como base el de 8 cm.", r"In the triangle in the figure (lengths in cm), work out the area in two ways: using the 10 cm side as the base and using the 8 cm side as the base.")
       + figs(G([('poly', [(0, 0), (10, 0), (6.4, 4.8)], 'gf'), ('seg', (6.4, 0), (6.4, 4.8), 'd'), ('ra', (6.4, 0), (10, 0), (6.4, 4.8)), ('ra', (6.4, 4.8), (0, 0), (10, 0)),
                 T_((5, 0), '10', dy=16), T_((6.4, 2.2), '4,8', dx=-7, a='end'), T_(off((6.4, 4.8), (0, 0), -0.6), '8', a='end'), T_(off((10, 0), (6.4, 4.8), -0.6), '6', a='start')], W=220)),
       P(r"Amb base 10, l'altura fa 4,8 cm. Els costats de 8 i 6 cm són perpendiculars (el triangle és rectangle): amb base 8, l'altura és el costat de 6 cm.", r"Con base 10, la altura mide 4,8 cm. Los lados de 8 y 6 cm son perpendiculares (el triángulo es rectángulo): con base 8, la altura es el lado de 6 cm.", r"With base 10 the height is 4.8 cm. The 8 cm and 6 cm sides are perpendicular (it's a right triangle): with base 8 the height is the 6 cm side."),
       D(r"A=\frac{10\cdot4{,}8}{2}=24\qquad A=\frac{8\cdot6}{2}=24\qquad\Rightarrow\ \boxed{24\ \text{cm}^2}"),
       P(r"Totes les parelles base–altura donen la mateixa àrea.", r"Todas las parejas base–altura dan la misma área.", r"Every base–height pair gives the same area."))])
ck(9 * 5, 45); ck(R(10 * 7, 2), 35); ck(R(8 * 6, 2), 24); ck(6 + 8 + 10, 24); ck(R(60, 12), 5); ck(R(15 * 8, 2), 60); ck(R(120, 10), 12); ck(10 * R(48, 10) / 2, 24); ck(R(8 * 6, 2), 24)
# la figura: triangle (0,0),(10,0),(6,4;4,8) té costats 10, 8 i 6, i la perpendicular des de (10,0) al costat de 8 fa 6
assert abs(math.hypot(6.4, 4.8) - 8) < 1e-9 and abs(math.hypot(10 - 6.4, 4.8) - 6) < 1e-9
s4 += practice([
  ('★', L(r"a) Àrea d'un romboide de 14 cm de base i 6 cm d'altura. b) Àrea d'un triangle de 9 cm de base i 4 cm d'altura.", r"a) Área de un romboide de 14 cm de base y 6 cm de altura. b) Área de un triángulo de 9 cm de base y 4 cm de altura.", r"a) Area of a parallelogram with a 14 cm base and a 6 cm height. b) Area of a triangle with a 9 cm base and a 4 cm height.")),
  ('★★', L(r"c) Àrea d'un triangle rectangle de catets 7,5 cm i 4 cm. d) Un romboide té 72 m² d'àrea i 9 m de base. Quant fa l'altura?", r"c) Área de un triángulo rectángulo de catetos 7,5 cm y 4 cm. d) Un romboide tiene 72 m² de área y 9 m de base. ¿Cuánto mide la altura?", r"c) Area of a right triangle with legs of 7.5 cm and 4 cm. d) A parallelogram has an area of 72 m² and a 9 m base. How tall is it?")),
  ('★★★', L(r"e) Un triangle té 24 cm² d'àrea i 6 cm d'altura. Quant fa la base?", r"e) Un triángulo tiene 24 cm² de área y 6 cm de altura. ¿Cuánto mide la base?", r"e) A triangle has an area of 24 cm² and a 6 cm height. How long is its base?"))],
  P(r"a) 84 cm². b) 18 cm². c) 15 cm². d) \(72:9=8\) m. e) \(b\cdot6=48\Rightarrow b=8\) cm.",
    r"a) 84 cm². b) 18 cm². c) 15 cm². d) \(72:9=8\) m. e) \(b\cdot6=48\Rightarrow b=8\) cm.",
    r"a) 84 cm². b) 18 cm². c) 15 cm². d) \(72\div9=8\) m. e) \(b\cdot6=48\Rightarrow b=8\) cm."))
ck(14 * 6, 84); ck(R(9 * 4, 2), 18); ck(R(75, 10) * 4 / 2, 15); ck(R(72, 9), 8); ck(R(48, 6), 8)

# =====================================================================
# 8.5 Àrea del rombe i del trapezi
# =====================================================================
x, y = 2.6, 1.7
F_RB = [('poly', [(-x, -y), (x, -y), (x, y), (-x, y)], 'frame'), ('poly', [(-x, 0), (0, -y), (-x, -y)], 'tl'), ('poly', [(x, 0), (0, -y), (x, -y)], 'tl'), ('poly', [(x, 0), (0, y), (x, y)], 'tl'), ('poly', [(-x, 0), (0, y), (-x, y)], 'tl'),
        ('poly', [(-x, 0), (0, y), (x, 0), (0, -y)], 'gf'), ('seg', (-x, 0), (x, 0), 'd'), ('seg', (0, -y), (0, y), 'd'), T_((-x / 2, 0), 'D', dy=-6), T_((0, -y / 2), 'd', dx=6, a='start')]
TB, Tb, Th, Tx = 6, 3, 2.4, 1
TR = [(0, 0), (TB, 0), (Tx + Tb, Th), (Tx, Th)]
TR2 = [(TB, 0), (TB + Tb, 0), (Tx + Tb + TB, Th), (Tx + Tb, Th)]   # el mateix trapezi girat mitja volta
F_TP = [('poly', TR, 'gf'), ('seg', (Tx, 0), (Tx, Th), 'd'), ('ra', (Tx, 0), (2, 0), (Tx, 1)), T_((TB / 2, 0), 'B', dy=16), T_((Tx + Tb / 2, Th), 'b', dy=-7), T_((Tx, Th / 2), 'h', dx=6, a='start')]
F_TP2 = [('poly', TR, 'gf'), ('poly', TR2, 'tl'), T_((TB / 2, 0), 'B', dy=16), T_((TB + Tb / 2, 0), 'b', dy=16), T_((Tx + Tb / 2, Th), 'b', dy=-7), T_((Tx + Tb + TB / 2, Th), 'B', dy=-7)]
s5 = box('prop', L('Àrea del rombe', 'Área del rombo', 'Area of a rhombus'),
  P(r"El rombe cap dins d'un rectangle que té per costats les dues diagonals, \(D\) (la major) i \(d\) (la menor). Els quatre triangles de fora són iguals als quatre de dins: el rombe ocupa <strong>la meitat</strong> del rectangle.",
    r"El rombo cabe dentro de un rectángulo que tiene por lados las dos diagonales, \(D\) (la mayor) y \(d\) (la menor). Los cuatro triángulos de fuera son iguales a los cuatro de dentro: el rombo ocupa <strong>la mitad</strong> del rectángulo.",
    r"A rhombus fits inside a rectangle whose sides are its two diagonals, \(D\) (the long one) and \(d\) (the short one). The four triangles outside match the four inside: the rhombus covers <strong>half</strong> the rectangle.")
  + figs(G(F_RB, W=210))
  + D(r"A_{\text{%s}}=\frac{D\cdot d}{2}" % Lt('rombe', 'rombo', 'rhombus'))
  + note(r"Com que el rombe també és un romboide, si en coneixem la base (el costat) i l'altura, també podem fer \(A=b\cdot h\).",
         r"Como el rombo también es un romboide, si conocemos su base (el lado) y su altura, también podemos hacer \(A=b\cdot h\).",
         r"Since a rhombus is also a parallelogram, if we know its base (the side) and its height we can also use \(A=b\cdot h\)."))
s5 += box('prop', L('Àrea del trapezi', 'Área del trapecio', 'Area of a trapezium'),
  P(r"Si ajuntem dos trapezis iguals, un d'ells girat mitja volta, formen un <strong>romboide</strong> de base \(B+b\) i la mateixa altura \(h\). El trapezi és la meitat d'aquest romboide:",
    r"Si juntamos dos trapecios iguales, uno de ellos girado media vuelta, forman un <strong>romboide</strong> de base \(B+b\) y la misma altura \(h\). El trapecio es la mitad de ese romboide:",
    r"Two equal trapeziums, one turned half a turn, fit together into a <strong>parallelogram</strong> with base \(B+b\) and the same height \(h\). The trapezium is half that parallelogram:")
  + figs(G(F_TP, W=190, cap=L('Trapezi', 'Trapecio', 'Trapezium')), G(F_TP2, W=260, cap=L(r'Dos trapezis: romboide de base \(B+b\)', r'Dos trapecios: romboide de base \(B+b\)', r'Two trapeziums: a parallelogram with base \(B+b\)')))
  + D(r"A_{\text{%s}}=\frac{(B+b)\cdot h}{2}" % Lt('trapezi', 'trapecio', 'trapezium'))
  + P(r"Per exemple, si \(B=10\), \(b=6\) i \(h=4\) cm: \(A=\dfrac{(10+6)\cdot4}{2}=\dfrac{64}{2}=32\ \text{cm}^2\). Recorda que primer se sumen les bases (el parèntesi).",
      r"Por ejemplo, si \(B=10\), \(b=6\) y \(h=4\) cm: \(A=\dfrac{(10+6)\cdot4}{2}=\dfrac{64}{2}=32\ \text{cm}^2\). Recuerda que primero se suman las bases (el paréntesis).",
      r"For example, if \(B=10\), \(b=6\) and \(h=4\) cm: \(A=\dfrac{(10+6)\cdot4}{2}=\dfrac{64}{2}=32\ \text{cm}^2\). Remember to add the bases first (the bracket).")
  + widget('w-area', '⏢', L('Rombes i trapezis', 'Rombos y trapecios', 'Rhombuses and trapeziums'),
           [seg([('rb', L('Rombe', 'Rombo', 'Rhombus')), ('tp', L('Trapezi', 'Trapecio', 'Trapezium'))]),
            seg([('f', L('Figura', 'Figura', 'Shape')), ('c', L('Per què? Mostra la construcció', '¿Por qué? Muestra la construcción', 'Why? Show the construction'))]),
            '<div class="wrow">' + rng('p', 1, 14, 1, 10) + rng('q', 1, 12, 1, 6) + rng('r', 1, 10, 1, 4) + '</div>'],
           out='<div class="gout"></div>')
  + drill('rbtp', 'Entrena: àrea del rombe i del trapezi', 'Entrena: área del rombo y del trapecio', 'Train: area of rhombuses and trapeziums'))
ck(R((10 + 6) * 4, 2), 32)
s5 += levels(
 [prob(L(r"Calcula l'àrea d'un rombe de diagonals 12 cm i 8 cm.", r"Calcula el área de un rombo de diagonales 12 cm y 8 cm.", r"Find the area of a rhombus with diagonals of 12 cm and 8 cm."),
       D(r"A=\frac{D\cdot d}{2}=\frac{12\cdot8}{2}=\frac{96}{2}=\boxed{48\ \text{cm}^2}")),
  prob(L(r"Calcula l'àrea d'un trapezi de bases 9 m i 5 m i 4 m d'altura.", r"Calcula el área de un trapecio de bases 9 m y 5 m y 4 m de altura.", r"Find the area of a trapezium with bases of 9 m and 5 m and a 4 m height."),
       D(r"A=\frac{(9+5)\cdot4}{2}=\frac{14\cdot4}{2}=\boxed{28\ \text{m}^2}"))],
 [prob(L(r"Un rombe té 36 cm² d'àrea i la diagonal menor fa 6 cm. Quant fa la diagonal major?", r"Un rombo tiene 36 cm² de área y la diagonal menor mide 6 cm. ¿Cuánto mide la diagonal mayor?", r"A rhombus has an area of 36 cm² and its short diagonal is 6 cm. How long is the long diagonal?"),
       D(r"\frac{D\cdot6}{2}=36\ \Rightarrow\ D\cdot6=72\ \Rightarrow\ D=\boxed{12\ \text{cm}}")),
  prob(L(r"Un trapezi rectangle té les bases de 14 cm i 8 cm, l'altura de 8 cm i el costat oblic de 10 cm. Calcula'n l'àrea i el perímetre.", r"Un trapecio rectángulo tiene las bases de 14 cm y 8 cm, la altura de 8 cm y el lado oblicuo de 10 cm. Calcula su área y su perímetro.", r"A right trapezium has bases of 14 cm and 8 cm, a height of 8 cm and a slanted side of 10 cm. Find its area and its perimeter."),
       figs(G([('poly', [(0, 0), (14, 0), (8, 8), (0, 8)], 'gf'), ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (0, 8), (0, 0), (1, 8)), T_((7, 0), '14', dy=16), T_((4, 8), '8', dy=-7), T_((0, 4), '8', dx=-8, a='end'), T_(off((14, 0), (8, 8), -0.9), '10', a='start')], W=190)),
       P(r"En el trapezi rectangle, el costat perpendicular a les bases és l'altura:", r"En el trapecio rectángulo, el lado perpendicular a las bases es la altura:", r"In a right trapezium, the side perpendicular to the bases is the height:"),
       D(r"A=\frac{(14+8)\cdot8}{2}=\boxed{88\ \text{cm}^2}\qquad P=14+8+8+10=\boxed{40\ \text{cm}}"))],
 [prob(L(r"Un estel té forma de rombe, amb diagonals de 80 cm i 50 cm. Quants cm² de paper calen per a fer-lo? I per a fer-ne 15?", r"Una cometa tiene forma de rombo, con diagonales de 80 cm y 50 cm. ¿Cuántos cm² de papel hacen falta para hacerla? ¿Y para hacer 15?", r"A kite is shaped like a rhombus, with diagonals of 80 cm and 50 cm. How many cm² of paper are needed to make it? And to make 15?"),
       D(r"A=\frac{80\cdot50}{2}=\boxed{2000\ \text{cm}^2}\qquad 15\cdot2000=30\,000\ \text{cm}^2=\boxed{3\ \text{m}^2}")),
  prob(L(r"Un terreny té forma de trapezi, amb bases de 120 m i 80 m i una amplària (altura) de 50 m. Quantes hectàrees fa? Quant val si el m² es paga a 30 €?", r"Un terreno tiene forma de trapecio, con bases de 120 m y 80 m y una anchura (altura) de 50 m. ¿Cuántas hectáreas mide? ¿Cuánto vale si el m² se paga a 30 €?", r"A plot of land is a trapezium with bases of 120 m and 80 m and a width (height) of 50 m. How many hectares is it? What is it worth at €30 per m²?"),
       D(r"A=\frac{(120+80)\cdot50}{2}=\frac{200\cdot50}{2}=5000\ \text{m}^2=\boxed{0{,}5\ \text{ha}}"),
       D(r"5000\cdot30=\boxed{150\,000\ \text{€}}"))])
ck(R(12 * 8, 2), 48); ck(R((9 + 5) * 4, 2), 28); ck(R(72, 6), 12); ck(R((14 + 8) * 8, 2), 88); ck(14 + 8 + 8 + 10, 40); assert math.hypot(6, 8) == 10
ck(R(80 * 50, 2), 2000); ck(15 * 2000, 30000); ck(R(30000, 10000), 3); ck(R((120 + 80) * 50, 2), 5000); ck(R(5000, 10000), 0.5); ck(5000 * 30, 150000)
s5 += practice([
  ('★', L(r"a) Àrea d'un rombe de diagonals 10 cm i 7 cm. b) Àrea d'un trapezi de bases 9 cm i 5 cm i altura 4 cm.", r"a) Área de un rombo de diagonales 10 cm y 7 cm. b) Área de un trapecio de bases 9 cm y 5 cm y altura 4 cm.", r"a) Area of a rhombus with diagonals of 10 cm and 7 cm. b) Area of a trapezium with bases of 9 cm and 5 cm and a 4 cm height.")),
  ('★★', L(r"c) Perímetre d'un rombe de 6,5 cm de costat. d) Un trapezi de 60 cm² té les bases de 12 cm i 8 cm. Quant fa l'altura?", r"c) Perímetro de un rombo de 6,5 cm de lado. d) Un trapecio de 60 cm² tiene las bases de 12 cm y 8 cm. ¿Cuánto mide la altura?", r"c) Perimeter of a rhombus with 6.5 cm sides. d) A 60 cm² trapezium has bases of 12 cm and 8 cm. How tall is it?")),
  ('★★★', L(r"e) Un rombe té 40 cm² d'àrea i una diagonal de 10 cm. Quant fa l'altra?", r"e) Un rombo tiene 40 cm² de área y una diagonal de 10 cm. ¿Cuánto mide la otra?", r"e) A rhombus has an area of 40 cm² and a 10 cm diagonal. How long is the other one?"))],
  P(r"a) 35 cm². b) 28 cm². c) 26 cm. d) \(\tfrac{20\cdot h}{2}=60\Rightarrow h=6\) cm. e) \(10\cdot d=80\Rightarrow d=8\) cm.",
    r"a) 35 cm². b) 28 cm². c) 26 cm. d) \(\tfrac{20\cdot h}{2}=60\Rightarrow h=6\) cm. e) \(10\cdot d=80\Rightarrow d=8\) cm.",
    r"a) 35 cm². b) 28 cm². c) 26 cm. d) \(\tfrac{20\cdot h}{2}=60\Rightarrow h=6\) cm. e) \(10\cdot d=80\Rightarrow d=8\) cm."))
ck(R(10 * 7, 2), 35); ck(R((9 + 5) * 4, 2), 28); ck(4 * R(65, 10), 26); ck(R(120, 20), 6); ck(R(80, 10), 8)

# =====================================================================
# 8.6 Àrea dels polígons regulars i dels polígons qualssevol
# =====================================================================
def reg_fig(n, tris=False):
    V = reg(n, 3); M = mid(V[0], V[1])
    it = [('poly', V, 'gf')]
    if tris:
        for k in range(n): it.append(('poly', [(0, 0), V[k], V[(k + 1) % n]], 'tr' if k == 0 else 'tl'))
        it += [('seg', (0, 0), M, 'd'), ('ra', M, V[1], (0, 0)), T_(mid((0, 0), M), 'a', dx=-7, a='end'), T_(M, 'l', dy=15)]
    else:
        it += [('seg', (0, 0), V[1], 'ch'), ('seg', (0, 0), M, 'hl'), ('ra', M, V[1], (0, 0)),
               T_(off((0, 0), V[1], -0.3), 'r', a='start', cls='c1'), T_(mid((0, 0), M), 'a', dx=-8, a='end', cls='hot'), T_(M, 'l', dy=15)]
    it += [('dot', (0, 0)), T_((0, 0), 'O', dy=-7, dx=-8)]
    return it
s6 = box('def', L('Elements d\'un polígon regular', 'Elementos de un polígono regular', 'Parts of a regular polygon'),
  P(r"Un polígon és <strong>regular</strong> si té tots els costats i tots els angles iguals. A més dels costats (\(l\)) i els vèrtexs, té:",
    r"Un polígono es <strong>regular</strong> si tiene todos los lados y todos los ángulos iguales. Además de los lados (\(l\)) y los vértices, tiene:",
    r"A polygon is <strong>regular</strong> if all its sides and all its angles are equal. Besides its sides (\(l\)) and vertices, it has:")
  + ul(L(r"<strong>Centre</strong> \(O\): el punt que està a la mateixa distància de tots els vèrtexs.", r"<strong>Centro</strong> \(O\): el punto que está a la misma distancia de todos los vértices.", r"<strong>Centre</strong> \(O\): the point at the same distance from every vertex."),
       L(r"<strong>Radi</strong> \(r\): el segment que unix el centre amb un vèrtex.", r"<strong>Radio</strong> \(r\): el segmento que une el centro con un vértice.", r"<strong>Radius</strong> \(r\): the segment joining the centre to a vertex."),
       L(r"<strong>Apotema</strong> \(a\): el segment que unix el centre amb el punt mitjà d'un costat. És <strong>perpendicular</strong> al costat.", r"<strong>Apotema</strong> \(a\): el segmento que une el centro con el punto medio de un lado. Es <strong>perpendicular</strong> al lado.", r"<strong>Apothem</strong> \(a\): the segment joining the centre to the midpoint of a side. It is <strong>perpendicular</strong> to the side."))
  + figs(G(reg_fig(6), W=190, cap=L('Hexàgon regular', 'Hexágono regular', 'Regular hexagon')), G(reg_fig(5), W=180, cap=L('Pentàgon regular', 'Pentágono regular', 'Regular pentagon'))))
s6 += box('prop', L("Àrea d'un polígon regular", 'Área de un polígono regular', 'Area of a regular polygon'),
  P(r"Si unim el centre amb els vèrtexs, un polígon regular de \(n\) costats queda dividit en \(n\) <strong>triangles iguals</strong>, de base \(l\) i altura \(a\) (l'apotema). Sumem les àrees dels \(n\) triangles:",
    r"Si unimos el centro con los vértices, un polígono regular de \(n\) lados queda dividido en \(n\) <strong>triángulos iguales</strong>, de base \(l\) y altura \(a\) (la apotema). Sumamos las áreas de los \(n\) triángulos:",
    r"Joining the centre to the vertices splits a regular polygon with \(n\) sides into \(n\) <strong>equal triangles</strong> with base \(l\) and height \(a\) (the apothem). Add up the areas of the \(n\) triangles:")
  + figs(G(reg_fig(5, True), W=190, cap=r'\(A=5\cdot\dfrac{l\cdot a}{2}\)'))
  + D(r"A=n\cdot\frac{l\cdot a}{2}=\frac{P\cdot a}{2}\qquad(P=n\cdot l\ \text{%s})" % Lt('és el perímetre', 'es el perímetro', 'is the perimeter'))
  + P(r"Per exemple, un pentàgon regular de 8 cm de costat i 5,5 cm d'apotema té \(P=5\cdot8=40\) cm i \(A=\dfrac{40\cdot5{,}5}{2}=110\ \text{cm}^2\).",
      r"Por ejemplo, un pentágono regular de 8 cm de lado y 5,5 cm de apotema tiene \(P=5\cdot8=40\) cm y \(A=\dfrac{40\cdot5{,}5}{2}=110\ \text{cm}^2\).",
      r"For example, a regular pentagon with 8 cm sides and a 5.5 cm apothem has \(P=5\cdot8=40\) cm and \(A=\dfrac{40\cdot5.5}{2}=110\ \text{cm}^2\).")
  + note(r"L'apotema ens la donaran o la mesurarem amb el regle. En l'<strong>hexàgon regular</strong> els sis triangles són equilàters: el radi és igual al costat.",
         r"La apotema nos la darán o la mediremos con la regla. En el <strong>hexágono regular</strong> los seis triángulos son equiláteros: el radio es igual al lado.",
         r"The apothem will be given or we'll measure it with a ruler. In a <strong>regular hexagon</strong> the six triangles are equilateral: the radius equals the side.", '📏')
  + widget('w-reg', '⬡', L('Explora els polígons regulars', 'Explora los polígonos regulares', 'Explore regular polygons'),
           ['<div class="wrow">' + rng('n', 3, 10, 1, 6, 'n') + rng('l', 1, 12, 0.5, 4, 'l') + '</div>'], out='<div class="gout"></div>')
  + drill('reg', 'Entrena: polígons regulars', 'Entrena: polígonos regulares', 'Train: regular polygons'))
ck(5 * 8, 40); ck(40 * R(55, 10) / 2, 110)
# polígon qualsevol en quadrícula
PV = [(0, 0), (6, 0), (6, 3), (3, 5), (0, 3)]
TV = [(0, 0), (6, 2), (2, 5)]
def shoelace(V): return abs(sum(V[i][0] * V[(i + 1) % len(V)][1] - V[(i + 1) % len(V)][0] * V[i][1] for i in range(len(V)))) / 2
assert shoelace(PV) == 24 and shoelace(TV) == 13
s6 += box('prop', L('Àrea d\'un polígon qualsevol', 'Área de un polígono cualquiera', 'Area of any polygon'),
  P(r"Si el polígon no és regular, el <strong>descomponem</strong> en figures que sabem calcular (triangles, rectangles, trapezis…) i <strong>sumem</strong> les àrees. Una altra estratègia és <strong>completar</strong>: el tanquem dins d'un rectangle i hi <strong>restem</strong> els trossos que sobren.",
    r"Si el polígono no es regular, lo <strong>descomponemos</strong> en figuras que sabemos calcular (triángulos, rectángulos, trapecios…) y <strong>sumamos</strong> las áreas. Otra estrategia es <strong>completar</strong>: lo encerramos dentro de un rectángulo y <strong>restamos</strong> los trozos que sobran.",
    r"If the polygon isn't regular, we <strong>split</strong> it into shapes we know how to work out (triangles, rectangles, trapeziums…) and <strong>add</strong> the areas. Another strategy is to <strong>complete</strong> it: put it inside a rectangle and <strong>subtract</strong> the leftover pieces.")
  + figs(G(grid(0, 0, 6, 5) + [('poly', [(0, 0), (6, 0), (6, 3), (0, 3)], 'q0'), ('poly', [(0, 3), (6, 3), (3, 5)], 'q1'), ('seg', (3, 3), (3, 5), 'd'), T_((3, 1.5), '6 · 3 = 18', cls='big'), T_((3, 3.6), '6·2 : 2 = 6')], W=200, pad=12,
           cap=L(r'Sumem: \(18+6=24\) u²', r'Sumamos: \(18+6=24\) u²', r'Add: \(18+6=24\) sq. units')),
         G(grid(0, 0, 6, 5) + [('poly', [(0, 0), (6, 0), (6, 2)], 'tl'), ('poly', [(6, 2), (6, 5), (2, 5)], 'tl'), ('poly', [(0, 0), (2, 5), (0, 5)], 'tl'), ('poly', TV, 'sh'),
                               T_((4.4, 0.6), 'A = 6', cls='sm'), T_((4.9, 4.1), 'A = 6', cls='sm'), T_((0.75, 3.8), 'A = 5', cls='sm')], W=200, pad=12,
           cap=L(r'Restem: \(30-6-6-5=13\) u²', r'Restamos: \(30-6-6-5=13\) u²', r'Subtract: \(30-6-6-5=13\) sq. units'))))
ck(6 * 3 + R(6 * 2, 2), 24); ck(30 - R(6 * 2, 2) - R(4 * 3, 2) - R(2 * 5, 2), 13)
s6 += levels(
 [prob(L(r"Un hexàgon regular té 6 cm de costat i 5,2 cm d'apotema. Calcula'n el perímetre i l'àrea.", r"Un hexágono regular tiene 6 cm de lado y 5,2 cm de apotema. Calcula su perímetro y su área.", r"A regular hexagon has 6 cm sides and a 5.2 cm apothem. Find its perimeter and its area."),
       D(r"P=6\cdot6=\boxed{36\ \text{cm}}\qquad A=\frac{P\cdot a}{2}=\frac{36\cdot5{,}2}{2}=\boxed{93{,}6\ \text{cm}^2}"))],
 [prob(L(r"Un octàgon regular té 48 cm de perímetre i 7,24 cm d'apotema. Quant fa el costat? I l'àrea?", r"Un octógono regular tiene 48 cm de perímetro y 7,24 cm de apotema. ¿Cuánto mide el lado? ¿Y el área?", r"A regular octagon has a 48 cm perimeter and a 7.24 cm apothem. How long is its side? What's its area?"),
       D(r"l=48:8=\boxed{6\ \text{cm}}\qquad A=\frac{48\cdot7{,}24}{2}=\boxed{173{,}76\ \text{cm}^2}")),
  prob(L(r"Un pentàgon regular de 6 cm de costat té 61,95 cm² d'àrea. Quant fa l'apotema?", r"Un pentágono regular de 6 cm de lado tiene 61,95 cm² de área. ¿Cuánto mide la apotema?", r"A regular pentagon with 6 cm sides has an area of 61.95 cm². How long is its apothem?"),
       D(r"P=5\cdot6=30\qquad \frac{30\cdot a}{2}=61{,}95\ \Rightarrow\ 30\cdot a=123{,}9\ \Rightarrow\ a=\boxed{4{,}13\ \text{cm}}"))],
 [prob(L(r"Calcula l'àrea del polígon de la figura (cada quadret és 1 cm²) de dues maneres: descomponent-lo i completant-lo fins a un rectangle.", r"Calcula el área del polígono de la figura (cada cuadradito es 1 cm²) de dos maneras: descomponiéndolo y completándolo hasta un rectángulo.", r"Work out the area of the polygon in the figure (each square is 1 cm²) in two ways: by splitting it and by completing it to a rectangle.")
       + figs(G(grid(0, 0, 7, 4) + [('poly', [(0, 0), (7, 0), (7, 2), (4, 4), (0, 4)], 'gf')], W=200, pad=12)),
       P(r"<strong>Descomponent</strong>: un rectangle de \(4\times4\), un rectangle de \(3\times2\) i un triangle de catets 3 i 2.", r"<strong>Descomponiendo</strong>: un rectángulo de \(4\times4\), un rectángulo de \(3\times2\) y un triángulo de catetos 3 y 2.", r"<strong>Splitting</strong>: a \(4\times4\) rectangle, a \(3\times2\) rectangle and a triangle with legs 3 and 2."),
       D(r"16+6+\frac{3\cdot2}{2}=16+6+3=\boxed{25\ \text{cm}^2}"),
       P(r"<strong>Completant</strong>: el rectangle de \(7\times4\) menys el triangle de la cantonada.", r"<strong>Completando</strong>: el rectángulo de \(7\times4\) menos el triángulo de la esquina.", r"<strong>Completing</strong>: the \(7\times4\) rectangle minus the corner triangle."),
       D(r"28-\frac{3\cdot2}{2}=28-3=\boxed{25\ \text{cm}^2}"))])
ck(36 * R(52, 10) / 2, 93.6); ck(48 / 8, 6); ck(48 * R(724, 100) / 2, 173.76); ck(R(1239, 10) / 30, 4.13); ck(16 + 6 + 3, 25); ck(28 - 3, 25)
assert shoelace([(0, 0), (7, 0), (7, 2), (4, 4), (0, 4)]) == 25
assert abs(6 / (2 * math.tan(math.pi / 5)) - 4.13) < 0.01 and abs(6 / (2 * math.tan(math.pi / 6)) - 5.2) < 0.01 and abs(6 / (2 * math.tan(math.pi / 8)) - 7.24) < 0.01
s6 += practice([
  ('★', L(r"a) Àrea d'un hexàgon regular de 10 cm de costat i 8,66 cm d'apotema.", r"a) Área de un hexágono regular de 10 cm de lado y 8,66 cm de apotema.", r"a) Area of a regular hexagon with 10 cm sides and an 8.66 cm apothem.")),
  ('★★', L(r"b) Perímetre i àrea d'un decàgon regular de 5 cm de costat i 7,69 cm d'apotema. c) Comprova que la fórmula \(A=\tfrac{P\cdot a}{2}\) també funciona en un quadrat de 6 cm de costat (quant fa l'apotema?).", r"b) Perímetro y área de un decágono regular de 5 cm de lado y 7,69 cm de apotema. c) Comprueba que la fórmula \(A=\tfrac{P\cdot a}{2}\) también funciona en un cuadrado de 6 cm de lado (¿cuánto mide la apotema?).", r"b) Perimeter and area of a regular decagon with 5 cm sides and a 7.69 cm apothem. c) Check that the formula \(A=\tfrac{P\cdot a}{2}\) also works for a square with 6 cm sides (how long is the apothem?).")),
  ('★★★', L(r"d) Un pentàgon regular té 50 cm de perímetre i 172 cm² d'àrea. Quant fa l'apotema?", r"d) Un pentágono regular tiene 50 cm de perímetro y 172 cm² de área. ¿Cuánto mide la apotema?", r"d) A regular pentagon has a 50 cm perimeter and an area of 172 cm². How long is its apothem?"))],
  P(r"a) \(\tfrac{60\cdot8{,}66}{2}=259{,}8\) cm². b) \(P=50\) cm, \(A=192{,}25\) cm². c) \(a=3\) cm: \(\tfrac{24\cdot3}{2}=36=6^2\) cm². d) \(25\cdot a=172\Rightarrow a=6{,}88\) cm.",
    r"a) \(\tfrac{60\cdot8{,}66}{2}=259{,}8\) cm². b) \(P=50\) cm, \(A=192{,}25\) cm². c) \(a=3\) cm: \(\tfrac{24\cdot3}{2}=36=6^2\) cm². d) \(25\cdot a=172\Rightarrow a=6{,}88\) cm.",
    r"a) \(\tfrac{60\cdot8.66}{2}=259.8\) cm². b) \(P=50\) cm, \(A=192.25\) cm². c) \(a=3\) cm: \(\tfrac{24\cdot3}{2}=36=6^2\) cm². d) \(25\cdot a=172\Rightarrow a=6.88\) cm."))
ck(60 * R(866, 100) / 2, 259.8); ck(50 * R(769, 100) / 2, 192.25); ck(R(24 * 3, 2), 36); ck(R(172, 25), 6.88)
