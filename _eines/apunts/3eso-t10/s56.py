# 10.5 Figures semblants. Raó de semblança · 10.6 Criteris de semblança de triangles
from comu import *
from fig10 import *

# =====================================================================
# 10.5 Figures semblants. Raó de semblança
# =====================================================================
FL = [(0, 0), (4, 0), (4, 1), (1.5, 1), (1.5, 3), (0, 3)]
s5 = box('def', L('Figures semblants', 'Figuras semejantes', 'Similar figures'),
  P(r"Dues figures són <strong>semblants</strong> si tenen la mateixa forma, encara que la grandària siga diferent: una és una ampliació o una reducció de l'altra. En dos polígons semblants:",
    r"Dos figuras son <strong>semejantes</strong> si tienen la misma forma, aunque el tamaño sea distinto: una es una ampliación o una reducción de la otra. En dos polígonos semejantes:",
    r"Two figures are <strong>similar</strong> if they have the same shape, even if their size is different: one is an enlargement or a reduction of the other. In two similar polygons:")
  + ul(L(r"els angles corresponents són <strong>iguals</strong>;", r"los ángulos correspondientes son <strong>iguales</strong>;", r"corresponding angles are <strong>equal</strong>;"),
       L(r"els costats corresponents (o <strong>homòlegs</strong>) són <strong>proporcionals</strong>.", r"los lados correspondientes (u <strong>homólogos</strong>) son <strong>proporcionales</strong>.", r"corresponding sides are <strong>proportional</strong>."))
  + P(r"La raó constant entre els costats homòlegs és la <strong>raó de semblança</strong>, \(k\):",
      r"La razón constante entre los lados homólogos es la <strong>razón de semejanza</strong>, \(k\):",
      r"The constant ratio between corresponding sides is the <strong>scale factor</strong>, \(k\):")
  + D(r"k=\frac{a'}{a}=\frac{b'}{b}=\frac{c'}{c}=\dots")
  + figs(G(simpair(FL, 1.5, ['4', '1', '2,5', '2', '1,5', '3'], ['6', '1,5', '3,75', '3', '2,25', '4,5']), W=320, pad=24, cap=r"\(k=\frac{6}{4}=1{,}5\)"))
  + tbl([L('Raó', 'Razón', 'Factor'), L('Què és la figura nova', 'Qué es la figura nueva', 'What the new figure is')],
        [[r'\(k>1\)', L('una <strong>ampliació</strong>', 'una <strong>ampliación</strong>', 'an <strong>enlargement</strong>')],
         [r'\(k=1\)', L('una figura <strong>igual</strong>', 'una figura <strong>igual</strong>', 'a <strong>congruent</strong> figure')],
         [r'\(0<k<1\)', L('una <strong>reducció</strong>', 'una <strong>reducción</strong>', 'a <strong>reduction</strong>')]], 'narrow')
  + note(r"No n'hi ha prou amb una de les dues condicions. Un quadrat i un rectangle tenen els angles iguals però no són semblants; un quadrat i un rombe tenen els costats proporcionals però no són semblants.",
         r"No basta con una de las dos condiciones. Un cuadrado y un rectángulo tienen los ángulos iguales pero no son semejantes; un cuadrado y un rombo tienen los lados proporcionales pero no son semejantes.",
         r"One of the two conditions is not enough. A square and a rectangle have equal angles but aren't similar; a square and a rhombus have proportional sides but aren't similar.", '⚠️'))
ck(R(6, 4), 1.5); ck(R(25, 10) * R(3, 2), 3.75); ck(R(15, 10) * R(3, 2), 2.25)
s5 += box('prop', L('Perímetres i àrees de figures semblants', 'Perímetros y áreas de figuras semejantes', 'Perimeters and areas of similar figures'),
  P(r"Si la raó de semblança és \(k\):", r"Si la razón de semejanza es \(k\):", r"If the scale factor is \(k\):")
  + ul(L(r"la raó dels <strong>perímetres</strong> (i de qualsevol longitud: altures, diagonals…) també és \(k\);", r"la razón de los <strong>perímetros</strong> (y de cualquier longitud: alturas, diagonales…) también es \(k\);", r"the ratio of the <strong>perimeters</strong> (and of any length: heights, diagonals…) is also \(k\);"),
       L(r"la raó de les <strong>àrees</strong> és \(k^2\).", r"la razón de las <strong>áreas</strong> es \(k^2\).", r"the ratio of the <strong>areas</strong> is \(k^2\)."))
  + D(r"\frac{P'}{P}=k\qquad\qquad\frac{A'}{A}=k^2")
  + P(r"Per què \(k^2\)? Si un rectangle de \(b\times h\) s'amplia amb raó \(k\), el nou fa \(kb\times kh\) i la seua àrea és \(kb\cdot kh=k^2\cdot bh\). Si dupliquem els costats (\(k=2\)), l'àrea es multiplica per 4.",
      r"¿Por qué \(k^2\)? Si un rectángulo de \(b\times h\) se amplía con razón \(k\), el nuevo mide \(kb\times kh\) y su área es \(kb\cdot kh=k^2\cdot bh\). Si duplicamos los lados (\(k=2\)), el área se multiplica por 4.",
      r"Why \(k^2\)? If a \(b\times h\) rectangle is enlarged by a factor \(k\), the new one is \(kb\times kh\) and its area is \(kb\cdot kh=k^2\cdot bh\). Doubling the sides (\(k=2\)) multiplies the area by 4.")
  + widget('w-sem', '🔍', L('Amplia o redueix una figura', 'Amplía o reduce una figura', 'Enlarge or reduce a shape'),
           [seg([('L', L('Forma de L', 'Forma de L', 'L shape')), ('T', L('Triangle', 'Triángulo', 'Triangle')), ('R', L('Rectangle', 'Rectángulo', 'Rectangle'))]),
            '<div class="wrow">' + rng('k', 0.25, 3, 0.25, 2, 'k') + '</div>'])
  + drill('sem', 'Entrena: figures semblants', 'Entrena: figuras semejantes', 'Train: similar figures'))
s5 += levels(
 [prob(L(r"Un rectangle de 4 cm × 6 cm és semblant a un altre que té el costat menut de 10 cm. Calcula la raó de semblança i el costat gran del segon rectangle.", r"Un rectángulo de 4 cm × 6 cm es semejante a otro que tiene el lado pequeño de 10 cm. Calcula la razón de semejanza y el lado grande del segundo rectángulo.", r"A 4 cm × 6 cm rectangle is similar to another whose short side is 10 cm. Find the scale factor and the long side of the second rectangle."),
       D(r"k=\frac{10}{4}=\boxed{2{,}5}\qquad 6\cdot2{,}5=\boxed{15\ \text{cm}}"))],
 [prob(L(r"Són semblants un rectangle de 3 cm × 5 cm i un altre de 6 cm × 9 cm?", r"¿Son semejantes un rectángulo de 3 cm × 5 cm y otro de 6 cm × 9 cm?", r"Are a 3 cm × 5 cm rectangle and a 6 cm × 9 cm one similar?"),
       P(r"Els angles són tots rectes. Comparem els costats homòlegs (el menut amb el menut i el gran amb el gran):", r"Los ángulos son todos rectos. Comparamos los lados homólogos (el pequeño con el pequeño y el grande con el grande):", r"All the angles are right angles. Compare corresponding sides (short with short and long with long):"),
       D(r"\frac63=2\qquad\frac95=1{,}8\qquad 2\neq1{,}8\ \Rightarrow\ \boxed{\text{%s}}" % Lt('no són semblants', 'no son semejantes', 'not similar'))),
  prob(L(r"Un triangle té 12 cm² d'àrea i 15 cm de perímetre. Calcula el perímetre i l'àrea d'un triangle semblant amb raó \(k=3\).", r"Un triángulo tiene 12 cm² de área y 15 cm de perímetro. Calcula el perímetro y el área de un triángulo semejante con razón \(k=3\).", r"A triangle has an area of 12 cm² and a perimeter of 15 cm. Find the perimeter and area of a similar triangle with \(k=3\)."),
       D(r"P'=15\cdot3=\boxed{45\ \text{cm}}\qquad A'=12\cdot3^2=12\cdot9=\boxed{108\ \text{cm}^2}"))],
 [prob(L(r"Volem ampliar una foto de 10 cm × 15 cm de manera que l'àrea siga 4 vegades més gran. Quines dimensions tindrà la foto ampliada? I si volem que l'àrea siga el doble?", r"Queremos ampliar una foto de 10 cm × 15 cm de modo que el área sea 4 veces mayor. ¿Qué dimensiones tendrá la foto ampliada? ¿Y si queremos que el área sea el doble?", r"We want to enlarge a 10 cm × 15 cm photo so that its area is 4 times bigger. What will its dimensions be? And if we want double the area?"),
       D(r"k^2=4\ \Rightarrow\ k=2:\quad\boxed{20\ \text{cm}\times30\ \text{cm}}"),
       D(r"k^2=2\ \Rightarrow\ k=\sqrt2\approx1{,}414:\quad10\sqrt2\approx\boxed{14{,}14\ \text{cm}}\times15\sqrt2\approx\boxed{21{,}21\ \text{cm}}"),
       P(r"Compte: per a doblar l'àrea no s'han de doblar els costats (això la multiplicaria per 4).", r"Cuidado: para doblar el área no hay que doblar los lados (eso la multiplicaría por 4).", r"Careful: to double the area you mustn't double the sides (that would multiply it by 4)."))])
ck(R(10, 4), 2.5); ck(6 * R(5, 2), 15); ck(15 * 3, 45); ck(12 * 9, 108); ck(10 * S(2), 14.14, 2); ck(15 * S(2), 21.21, 2)
s5 += practice([
  ('★', L(r"a) Un triangle té costats de 3, 4 i 6 cm. Calcula els costats d'un triangle semblant amb raó \(k=1{,}5\). b) I amb raó \(k=0{,}5\)?", r"a) Un triángulo tiene lados de 3, 4 y 6 cm. Calcula los lados de un triángulo semejante con razón \(k=1{,}5\). b) ¿Y con razón \(k=0{,}5\)?", r"a) A triangle has sides 3, 4 and 6 cm. Find the sides of a similar triangle with \(k=1.5\). b) And with \(k=0.5\)?")),
  ('★★', L(r"c) Dos pentàgons regulars tenen costats de 4 cm i 6 cm. Quina és la raó de les seues àrees? d) Si el perímetre d'un polígon es triplica, què passa amb l'àrea?", r"c) Dos pentágonos regulares tienen lados de 4 cm y 6 cm. ¿Cuál es la razón de sus áreas? d) Si el perímetro de un polígono se triplica, ¿qué pasa con el área?", r"c) Two regular pentagons have 4 cm and 6 cm sides. What is the ratio of their areas? d) If a polygon's perimeter is tripled, what happens to its area?")),
  ('★★★', L(r"e) Dos quadrats semblants tenen àrees de 25 cm² i 64 cm². Quina és la raó de semblança? Quant fa el costat de cadascun?", r"e) Dos cuadrados semejantes tienen áreas de 25 cm² y 64 cm². ¿Cuál es la razón de semejanza? ¿Cuánto mide el lado de cada uno?", r"e) Two squares have areas 25 cm² and 64 cm². What is the scale factor? How long is each side?"))],
  P(r"a) 4,5, 6 i 9 cm. b) 1,5, 2 i 3 cm. c) \(k=1{,}5\), \(k^2=2{,}25\). d) \(k=3\): l'àrea es multiplica per 9. e) \(k^2=\frac{64}{25}\Rightarrow k=\frac85=1{,}6\); costats 5 cm i 8 cm.",
    r"a) 4,5, 6 y 9 cm. b) 1,5, 2 y 3 cm. c) \(k=1{,}5\), \(k^2=2{,}25\). d) \(k=3\): el área se multiplica por 9. e) \(k^2=\frac{64}{25}\Rightarrow k=\frac85=1{,}6\); lados 5 cm y 8 cm.",
    r"a) 4.5, 6 and 9 cm. b) 1.5, 2 and 3 cm. c) \(k=1.5\), \(k^2=2.25\). d) \(k=3\): the area is multiplied by 9. e) \(k^2=\frac{64}{25}\Rightarrow k=\frac85=1.6\); sides 5 cm and 8 cm."))
ck(R(6, 4) ** 2, 2.25); ck(S(R(64, 25)), 1.6)

# =====================================================================
# 10.6 Criteris de semblança de triangles
# =====================================================================
T1, _ = tri_sides(4, 3, 3.6, 0, 'gf', ['a', 'b', 'c'], ['α', 'β', 'γ'])
T2, _ = tri_sides(6, 4.5, 5.4, 5.6, 'tr', ['a′', 'b′', 'c′'], ['α', 'β', 'γ'])
s6 = box('def', L('Triangles semblants', 'Triángulos semejantes', 'Similar triangles'),
  P(r"Dos triangles són semblants si tenen els tres angles iguals i els tres costats proporcionals. Però no cal comprovar-ho tot: n'hi ha prou amb qualsevol d'aquests <strong>criteris</strong>:",
    r"Dos triángulos son semejantes si tienen los tres ángulos iguales y los tres lados proporcionales. Pero no hace falta comprobarlo todo: basta con cualquiera de estos <strong>criterios</strong>:",
    r"Two triangles are similar if all three angles are equal and all three sides are proportional. But you don't need to check everything: any one of these <strong>criteria</strong> is enough:")
  + figs(G(T1 + T2, W=330, pad=24))
  + tbl([L('Criteri', 'Criterio', 'Criterion'), L('Condició', 'Condición', 'Condition')],
        [[L('<strong>1r · Angles</strong>', '<strong>1.º · Ángulos</strong>', '<strong>1st · Angles (AA)</strong>'), L(r"Tenen <strong>dos angles</strong> iguals (el tercer també ho és, perquè sumen 180°).", r"Tienen <strong>dos ángulos</strong> iguales (el tercero también lo es, porque suman 180°).", r"They have <strong>two equal angles</strong> (so the third is equal too, as they add up to 180°).")],
         [L('<strong>2n · Costats</strong>', '<strong>2.º · Lados</strong>', '<strong>2nd · Sides (SSS)</strong>'), L(r"Tenen els <strong>tres costats proporcionals</strong>: \(\frac{a'}{a}=\frac{b'}{b}=\frac{c'}{c}\).", r"Tienen los <strong>tres lados proporcionales</strong>: \(\frac{a'}{a}=\frac{b'}{b}=\frac{c'}{c}\).", r"All <strong>three sides are proportional</strong>: \(\frac{a'}{a}=\frac{b'}{b}=\frac{c'}{c}\).")],
         [L('<strong>3r · Costats i angle</strong>', '<strong>3.º · Lados y ángulo</strong>', '<strong>3rd · SAS</strong>'), L(r"Tenen <strong>dos costats proporcionals</strong> i l'<strong>angle comprés</strong> entre ells igual.", r"Tienen <strong>dos lados proporcionales</strong> y el <strong>ángulo comprendido</strong> entre ellos igual.", r"<strong>Two sides are proportional</strong> and the <strong>angle between them</strong> is equal.")]])
  + P(r"En particular, dos triangles en posició de Tales sempre són semblants (tenen l'angle \(\hat A\) comú i els angles de la base iguals, perquè \(B'C'\parallel BC\)). Dos triangles <strong>rectangles</strong> són semblants si tenen un angle agut igual.",
      r"En particular, dos triángulos en posición de Tales siempre son semejantes (tienen el ángulo \(\hat A\) común y los ángulos de la base iguales, porque \(B'C'\parallel BC\)). Dos triángulos <strong>rectángulos</strong> son semejantes si tienen un ángulo agudo igual.",
      r"In particular, two triangles in Thales position are always similar (they share angle \(\hat A\) and their base angles are equal because \(B'C'\parallel BC\)). Two <strong>right</strong> triangles are similar if they have one equal acute angle."))
s6 += box('prop', L('Com comprovar-ho amb els costats', 'Cómo comprobarlo con los lados', 'How to check it with the sides'),
  P(r"<strong>Ordena</strong> els costats de cada triangle de menor a major i divideix-los en aquest ordre. Si les tres raons coincideixen, són semblants:",
    r"<strong>Ordena</strong> los lados de cada triángulo de menor a mayor y divídelos en ese orden. Si las tres razones coinciden, son semejantes:",
    r"<strong>Sort</strong> the sides of each triangle from shortest to longest and divide them in that order. If the three ratios agree, the triangles are similar:")
  + D(r"(4,\ 6,\ 7)\ \text{%s}\ (6,\ 9,\ 10{,}5):\quad\frac64=1{,}5\quad\frac96=1{,}5\quad\frac{10{,}5}{7}=1{,}5\ \Rightarrow\ \text{%s},\ k=1{,}5" % (Lt('i', 'y', 'and'), Lt('semblants', 'semejantes', 'similar')))
  + widget('w-crit', '⚖️', L('Són semblants aquests triangles?', '¿Son semejantes estos triángulos?', 'Are these triangles similar?'),
           ['<div class="wrow"><b>1:</b> ' + tin('a', 'a =', '4') + tin('b', 'b =', '6') + tin('c', 'c =', '7') + '</div>',
            '<div class="wrow"><b>2:</b> ' + tin('d', "a′ =", '10,5') + tin('e', "b′ =", '6') + tin('f', "c′ =", '9') + '</div>',
            quick([('4|6|7|10,5|6|9', '4, 6, 7 · 10,5, 6, 9'), ('3|4|5|6|8|11', '3, 4, 5 · 6, 8, 11'), ('5|5|8|2|2|3,2', '5, 5, 8 · 2, 2, 3,2'), ('2|3|4|3|4|5', '2, 3, 4 · 3, 4, 5')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('crit', 'Entrena: són semblants?', 'Entrena: ¿son semejantes?', 'Train: are they similar?', 'opts'))
ck(R(105, 10) / 7, 1.5)
s6 += levels(
 [prob(L(r"Són semblants els triangles de costats 5, 7 i 8 cm i 15, 21 i 24 cm? Quina és la raó de semblança?", r"¿Son semejantes los triángulos de lados 5, 7 y 8 cm y 15, 21 y 24 cm? ¿Cuál es la razón de semejanza?", r"Are the triangles with sides 5, 7, 8 cm and 15, 21, 24 cm similar? What is the scale factor?"),
       D(r"\frac{15}{5}=\frac{21}{7}=\frac{24}{8}=3\ \Rightarrow\ \boxed{\text{%s},\ k=3}" % Lt('semblants', 'semejantes', 'similar'))),
  prob(L(r"Un triangle té dos angles de 50° i 65°. Un altre en té dos de 65° i 65°. Són semblants?", r"Un triángulo tiene dos ángulos de 50° y 65°. Otro tiene dos de 65° y 65°. ¿Son semejantes?", r"A triangle has two angles of 50° and 65°. Another has two angles of 65° and 65°. Are they similar?"),
       D(r"180^\circ-50^\circ-65^\circ=65^\circ\ \Rightarrow\ 50^\circ,\ 65^\circ,\ 65^\circ\qquad 180^\circ-65^\circ-65^\circ=50^\circ\ \Rightarrow\ 65^\circ,\ 65^\circ,\ 50^\circ"),
       P(r"Tenen els mateixos angles: <strong>són semblants</strong> (criteri 1r).", r"Tienen los mismos ángulos: <strong>son semejantes</strong> (criterio 1.º).", r"They have the same angles: <strong>they are similar</strong> (AA criterion)."))],
 [prob(L(r"Els triangles \(ABC\) i \(A'B'C'\) tenen \(\hat A=\hat A'=40^\circ\), \(\overline{AB}=6\), \(\overline{AC}=9\), \(\overline{A'B'}=8\) i \(\overline{A'C'}=12\). Són semblants? Si \(\overline{BC}=6{,}1\), quant mesura \(\overline{B'C'}\)?", r"Los triángulos \(ABC\) y \(A'B'C'\) tienen \(\hat A=\hat A'=40^\circ\), \(\overline{AB}=6\), \(\overline{AC}=9\), \(\overline{A'B'}=8\) y \(\overline{A'C'}=12\). ¿Son semejantes? Si \(\overline{BC}=6{,}1\), ¿cuánto mide \(\overline{B'C'}\)?", r"Triangles \(ABC\) and \(A'B'C'\) have \(\hat A=\hat A'=40^\circ\), \(\overline{AB}=6\), \(\overline{AC}=9\), \(\overline{A'B'}=8\) and \(\overline{A'C'}=12\). Are they similar? If \(\overline{BC}=6.1\), how long is \(\overline{B'C'}\)?"),
       D(r"\frac86=\frac{12}{9}=\frac43"),
       P(r"Dos costats proporcionals i l'angle comprés igual: <strong>són semblants</strong> (criteri 3r), amb \(k=\frac43\).", r"Dos lados proporcionales y el ángulo comprendido igual: <strong>son semejantes</strong> (criterio 3.º), con \(k=\frac43\).", r"Two proportional sides and an equal included angle: <strong>they are similar</strong> (SAS), with \(k=\frac43\)."),
       D(r"\overline{B'C'}=6{,}1\cdot\frac43\approx\boxed{8{,}13}"))],
 [prob(L(r"En un triangle rectangle \(ABC\), amb l'angle recte en \(A\), els catets mesuren 15 cm i 20 cm. Tracem l'altura \(AH\) sobre la hipotenusa. Calcula l'altura usant triangles semblants.", r"En un triángulo rectángulo \(ABC\), con el ángulo recto en \(A\), los catetos miden 15 cm y 20 cm. Trazamos la altura \(AH\) sobre la hipotenusa. Calcula la altura usando triángulos semejantes.", r"In a right triangle \(ABC\) with the right angle at \(A\), the legs are 15 cm and 20 cm. Draw the height \(AH\) onto the hypotenuse. Find the height using similar triangles."),
       D(r"\overline{BC}=\sqrt{15^2+20^2}=\sqrt{625}=25"),
       P(r"Els triangles \(ABC\) i \(HBA\) són rectangles i comparteixen l'angle \(\hat B\): són semblants (criteri 1r). Els costats homòlegs són: hipotenusa \(BC\) ↔ hipotenusa \(AB\), i catet \(AC\) ↔ catet \(HA\):", r"Los triángulos \(ABC\) y \(HBA\) son rectángulos y comparten el ángulo \(\hat B\): son semejantes (criterio 1.º). Los lados homólogos son: hipotenusa \(BC\) ↔ hipotenusa \(AB\), y cateto \(AC\) ↔ cateto \(HA\):", r"Triangles \(ABC\) and \(HBA\) are right triangles sharing angle \(\hat B\), so they're similar (AA). Corresponding sides: hypotenuse \(BC\) ↔ hypotenuse \(AB\), and leg \(AC\) ↔ leg \(HA\):")
       + figs(G([('poly', [(0, 0), (25, 0), (9, 12)], 'gf'), ('poly', [(0, 0), (9, 0), (9, 12)], 'tr'), ('seg', (9, 0), (9, 12), 'hl'), ('ra', (9, 12), (0, 0), (25, 0)), ('ra', (9, 0), (0, 0), (9, 12)),
                 ('txt', (0, 0), 'B', {'dx': -8, 'a': 'end'}), ('txt', (25, 0), 'C', {'dx': 8, 'a': 'start'}), ('txt', (9, 12), 'A', {'dy': -8}), ('txt', (9, 0), 'H', {'dy': 15}),
                 ('txt', (4.5, 6), '15', {'dx': -8, 'a': 'end'}), ('txt', (17, 6), '20', {'dx': 8, 'a': 'start'}), ('txt', (9, 6), 'h', {'dx': 7, 'a': 'start', 'cls': 'hot'})], W=260, pad=24)),
       D(r"\frac{h}{20}=\frac{15}{25}\ \Rightarrow\ h=\frac{15\cdot20}{25}=\boxed{12\ \text{cm}}"),
       P(r"Comprovació amb l'àrea: \(\frac{15\cdot20}{2}=150=\frac{25\cdot12}{2}\ \checkmark\)", r"Comprobación con el área: \(\frac{15\cdot20}{2}=150=\frac{25\cdot12}{2}\ \checkmark\)", r"Check with the area: \(\frac{15\cdot20}{2}=150=\frac{25\cdot12}{2}\ \checkmark\)"))])
assert R(15, 5) == R(21, 7) == R(24, 8) == 3; ck(R(8, 6), R(12, 9)); ck(R(61, 10) * R(4, 3), 8.13, 2); ck(hyp(15, 20), 25); ck(R(15 * 20, 25), 12)
s6 += practice([
  ('★', L(r"a) Són semblants els triangles de costats 2, 3, 4 i 6, 9, 12? b) I els de costats 4, 5, 6 i 8, 10, 11?", r"a) ¿Son semejantes los triángulos de lados 2, 3, 4 y 6, 9, 12? b) ¿Y los de lados 4, 5, 6 y 8, 10, 11?", r"a) Are the triangles with sides 2, 3, 4 and 6, 9, 12 similar? b) And 4, 5, 6 and 8, 10, 11?")),
  ('★★', L(r"c) Un triangle té angles de 30° i 70°, i un altre, de 70° i 80°. Són semblants? d) Són semblants tots els triangles equilàters? I tots els isòsceles?", r"c) Un triángulo tiene ángulos de 30° y 70°, y otro, de 70° y 80°. ¿Son semejantes? d) ¿Son semejantes todos los triángulos equiláteros? ¿Y todos los isósceles?", r"c) One triangle has angles of 30° and 70°, another of 70° and 80°. Are they similar? d) Are all equilateral triangles similar? What about all isosceles ones?")),
  ('★★★', L(r"e) Els costats d'un triangle mesuren 6, 8 i 9 cm. Un triangle semblant té 69 cm de perímetre. Quant mesuren els seus costats?", r"e) Los lados de un triángulo miden 6, 8 y 9 cm. Un triángulo semejante tiene 69 cm de perímetro. ¿Cuánto miden sus lados?", r"e) A triangle has sides 6, 8 and 9 cm. A similar triangle has a perimeter of 69 cm. How long are its sides?"))],
  P(r"a) Sí, \(k=3\). b) No: \(\frac84=\frac{10}5=2\), però \(\frac{11}{6}\neq2\). c) Sí: el primer té 30°, 70°, 80°. d) Els equilàters sí (tots tenen angles de 60°); els isòsceles no. e) \(P=23\), \(k=\frac{69}{23}=3\): 18, 24 i 27 cm.",
    r"a) Sí, \(k=3\). b) No: \(\frac84=\frac{10}5=2\), pero \(\frac{11}{6}\neq2\). c) Sí: el primero tiene 30°, 70°, 80°. d) Los equiláteros sí (todos tienen ángulos de 60°); los isósceles no. e) \(P=23\), \(k=\frac{69}{23}=3\): 18, 24 y 27 cm.",
    r"a) Yes, \(k=3\). b) No: \(\frac84=\frac{10}5=2\), but \(\frac{11}{6}\neq2\). c) Yes: the first has 30°, 70°, 80°. d) Equilateral ones yes (all angles are 60°); isosceles ones no. e) \(P=23\), \(k=\frac{69}{23}=3\): 18, 24 and 27 cm."))
assert 180 - 30 - 70 == 80 and R(69, 23) == 3
