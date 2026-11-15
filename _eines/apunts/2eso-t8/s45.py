# 8.4 Aplicació a la semblança de triangles · 8.5 Problemes amb semblança de triangles
# Apunts de la Unitat 8 de 2n ESO (Semblança. Teorema de Tales). Cada resultat es comprova amb ck().
from comu import *
from fig8 import *

# =====================================================================
# 8.4 Aplicació a la semblança de triangles
# =====================================================================
s4 = box('def', L('Triangles en posició de Tales', 'Triángulos en posición de Tales', 'Triangles in Thales position'),
  P(r"Si en un triangle \(ABC\) tracem un segment \(B'C'\) <strong>paral·lel</strong> al costat \(BC\), obtenim un triangle menut \(AB'C'\) dins del gran. Diem que els triangles \(AB'C'\) i \(ABC\) estan en <strong>posició de Tales</strong>:",
    r"Si en un triángulo \(ABC\) trazamos un segmento \(B'C'\) <strong>paralelo</strong> al lado \(BC\), obtenemos un triángulo pequeño \(AB'C'\) dentro del grande. Decimos que los triángulos \(AB'C'\) y \(ABC\) están en <strong>posición de Tales</strong>:",
    r"If we draw a segment \(B'C'\) <strong>parallel</strong> to side \(BC\) of a triangle \(ABC\), we get a small triangle \(AB'C'\) inside the big one. We say triangles \(AB'C'\) and \(ABC\) are in <strong>Thales position</strong>:")
  + figs(G(tpos(6, 6.6, 50, 0.5), W=230, pad=24))
  + ul(L(r"tenen l'angle \(\hat A\) <strong>comú</strong>;", r"tienen el ángulo \(\hat A\) <strong>común</strong>;", r"they <strong>share</strong> angle \(\hat A\);"),
       L(r"els angles de la base són iguals, perquè \(B'C'\parallel BC\);", r"los ángulos de la base son iguales, porque \(B'C'\parallel BC\);", r"their base angles are equal, because \(B'C'\parallel BC\);"),
       L(r"pel teorema de Tales, els costats són proporcionals.", r"por el teorema de Tales, los lados son proporcionales.", r"by Thales' theorem, their sides are proportional."))
  + P(r"Per tant, <strong>dos triangles en posició de Tales són semblants</strong>, i la raó de semblança és la mateixa per als tres costats:",
      r"Por tanto, <strong>dos triángulos en posición de Tales son semejantes</strong>, y la razón de semejanza es la misma para los tres lados:",
      r"So <strong>two triangles in Thales position are similar</strong>, and the scale factor is the same for all three sides:")
  + D(r"\frac{\overline{AB'}}{\overline{AB}}=\frac{\overline{AC'}}{\overline{AC}}=\frac{\overline{B'C'}}{\overline{BC}}")
  + note(r"L'error més freqüent: posar \(\overline{B'B}\) en lloc de \(\overline{AB}\). Si et donen els trossos \(\overline{AB'}\) i \(\overline{B'B}\), suma'ls per a tindre el costat sencer: \(\overline{AB}=\overline{AB'}+\overline{B'B}\).",
         r"El error más frecuente: poner \(\overline{B'B}\) en lugar de \(\overline{AB}\). Si te dan los trozos \(\overline{AB'}\) y \(\overline{B'B}\), súmalos para tener el lado entero: \(\overline{AB}=\overline{AB'}+\overline{B'B}\).",
         r"The most common mistake: using \(\overline{B'B}\) instead of \(\overline{AB}\). If you're given the pieces \(\overline{AB'}\) and \(\overline{B'B}\), add them to get the whole side: \(\overline{AB}=\overline{AB'}+\overline{B'B}\).", '⚠️')
  + widget('w-tpos', '🔺', L('Desplaça el costat paral·lel', 'Desplaza el lado paralelo', 'Slide the parallel side'),
           ['<div class="wrow">' + rng('t', 0.1, 0.95, 0.05, 0.5, 't') + '</div>',
            '<div class="wrow">' + tin('AB', 'AB =', '8') + tin('AC', 'AC =', '10') + tin('BC', 'BC =', '9') + '</div>'])
  + drill('tpos', 'Entrena: triangles en posició de Tales', 'Entrena: triángulos en posición de Tales', 'Train: triangles in Thales position'))
s4 += box('prop', L('Com es calcula', 'Cómo se calcula', 'How to calculate'),
  P(r"En el triangle de la figura, \(B'C'\parallel BC\), \(\overline{AB'}=3\), \(\overline{B'B}=6\) i \(\overline{BC}=12\). Calculem \(\overline{B'C'}\):",
    r"En el triángulo de la figura, \(B'C'\parallel BC\), \(\overline{AB'}=3\), \(\overline{B'B}=6\) y \(\overline{BC}=12\). Calculamos \(\overline{B'C'}\):",
    r"In the triangle in the figure, \(B'C'\parallel BC\), \(\overline{AB'}=3\), \(\overline{B'B}=6\) and \(\overline{BC}=12\). Let's find \(\overline{B'C'}\):")
  + figs(G(tpos(6, 6.6, 50, 1 / 3, labs={'AB1': '3', 'B1B': '6', 'BC': '12', 'B1C1': 'x'}, hot='B1C1'), W=230, pad=26))
  + D(r"\overline{AB}=3+6=9\qquad\frac{3}{9}=\frac{x}{12}\ \Rightarrow\ 9x=36\ \Rightarrow\ x=4"))
ck(3 + 6, 9); ck(R(36, 9), 4)
T1, _ = tri_sides(4, 3, 3.6, 0, 'gf', ['a', 'b', 'c'], ['α', 'β', 'γ'])
T2, _ = tri_sides(6, 4.5, 5.4, 5.6, 'tr', ['a′', 'b′', 'c′'], ['α', 'β', 'γ'])
s4 += box('def', L('Quan són semblants dos triangles?', '¿Cuándo son semejantes dos triángulos?', 'When are two triangles similar?'),
  P(r"Dos triangles són semblants si tenen els tres angles iguals i els tres costats proporcionals. Però en els triangles no cal comprovar-ho tot: n'hi ha prou que es complisca <strong>un</strong> d'aquests <strong>criteris</strong>:",
    r"Dos triángulos son semejantes si tienen los tres ángulos iguales y los tres lados proporcionales. Pero en los triángulos no hace falta comprobarlo todo: basta con que se cumpla <strong>uno</strong> de estos <strong>criterios</strong>:",
    r"Two triangles are similar if all three angles are equal and all three sides are proportional. But with triangles you don't need to check everything: <strong>one</strong> of these <strong>criteria</strong> is enough:")
  + figs(G(T1 + T2, W=330, pad=24))
  + tbl([L('Criteri', 'Criterio', 'Criterion'), L('Condició', 'Condición', 'Condition')],
        [[L('<strong>1r · Dos angles</strong>', '<strong>1.º · Dos ángulos</strong>', '<strong>1st · Two angles</strong>'), L(r"Tenen <strong>dos angles</strong> iguals (aleshores el tercer també és igual, perquè els tres sumen 180°).", r"Tienen <strong>dos ángulos</strong> iguales (entonces el tercero también es igual, porque los tres suman 180°).", r"They have <strong>two equal angles</strong> (then the third is equal too, since all three add up to 180°).")],
         [L('<strong>2n · Tres costats</strong>', '<strong>2.º · Tres lados</strong>', '<strong>2nd · Three sides</strong>'), L(r"Tenen els <strong>tres costats proporcionals</strong>: \(\frac{a'}{a}=\frac{b'}{b}=\frac{c'}{c}\).", r"Tienen los <strong>tres lados proporcionales</strong>: \(\frac{a'}{a}=\frac{b'}{b}=\frac{c'}{c}\).", r"All <strong>three sides are proportional</strong>: \(\frac{a'}{a}=\frac{b'}{b}=\frac{c'}{c}\).")],
         [L('<strong>3r · Dos costats i l\'angle</strong>', '<strong>3.º · Dos lados y el ángulo</strong>', '<strong>3rd · Two sides and the angle</strong>'), L(r"Tenen <strong>dos costats proporcionals</strong> i l'<strong>angle que formen</strong> és igual.", r"Tienen <strong>dos lados proporcionales</strong> y el <strong>ángulo que forman</strong> es igual.", r"<strong>Two sides are proportional</strong> and the <strong>angle between them</strong> is equal.")]])
  + P(r"En particular, dos <strong>triangles rectangles</strong> són semblants si tenen un angle agut igual (ja tenen igual l'angle recte), i <strong>tots els triangles equilàters</strong> són semblants (tenen tots els angles de 60°).",
      r"En particular, dos <strong>triángulos rectángulos</strong> son semejantes si tienen un ángulo agudo igual (ya tienen igual el ángulo recto), y <strong>todos los triángulos equiláteros</strong> son semejantes (tienen todos los ángulos de 60°).",
      r"In particular, two <strong>right triangles</strong> are similar if they have one equal acute angle (the right angles already match), and <strong>all equilateral triangles</strong> are similar (all their angles are 60°)."))
s4 += box('prop', L('Com comprovar-ho amb els costats', 'Cómo comprobarlo con los lados', 'How to check it with the sides'),
  P(r"<strong>Ordena</strong> els costats de cada triangle de menor a major i divideix-los en aquest ordre. Si les tres raons donen el mateix, són semblants:",
    r"<strong>Ordena</strong> los lados de cada triángulo de menor a mayor y divídelos en ese orden. Si las tres razones dan lo mismo, son semejantes:",
    r"<strong>Sort</strong> the sides of each triangle from shortest to longest and divide them in that order. If the three ratios are the same, the triangles are similar:")
  + D(r"(4,\ 6,\ 7)\ \text{%s}\ (6,\ 9,\ 10{,}5):\quad\frac64=1{,}5\quad\frac96=1{,}5\quad\frac{10{,}5}{7}=1{,}5\ \Rightarrow\ \text{%s},\ k=1{,}5" % (Lt('i', 'y', 'and'), Lt('semblants', 'semejantes', 'similar')))
  + widget('w-crit', '⚖️', L('Són semblants aquests triangles?', '¿Son semejantes estos triángulos?', 'Are these triangles similar?'),
           ['<div class="wrow"><b>1:</b> ' + tin('a', 'a =', '4') + tin('b', 'b =', '6') + tin('c', 'c =', '7') + '</div>',
            '<div class="wrow"><b>2:</b> ' + tin('d', "a′ =", '10,5') + tin('e', "b′ =", '6') + tin('f', "c′ =", '9') + '</div>',
            quick([('4|6|7|10,5|6|9', '4, 6, 7 · 10,5, 6, 9'), ('3|4|5|6|8|11', '3, 4, 5 · 6, 8, 11'), ('5|5|8|2|2|3,2', '5, 5, 8 · 2, 2, 3,2'), ('2|3|4|3|4|5', '2, 3, 4 · 3, 4, 5')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('crit', 'Entrena: són semblants?', 'Entrena: ¿son semejantes?', 'Train: are they similar?', 'opts'))
ck(R(105, 10) / 7, 1.5)
s4 += levels(
 [prob(L(r"Són semblants els triangles de costats 3, 5 i 6 cm i 9, 15 i 18 cm? Quina és la raó de semblança?", r"¿Son semejantes los triángulos de lados 3, 5 y 6 cm y 9, 15 y 18 cm? ¿Cuál es la razón de semejanza?", r"Are the triangles with sides 3, 5, 6 cm and 9, 15, 18 cm similar? What is the scale factor?"),
       D(r"\frac93=\frac{15}{5}=\frac{18}{6}=3\ \Rightarrow\ \boxed{\text{%s},\ k=3}" % Lt('semblants', 'semejantes', 'similar'))),
  prob(L(r"En un triangle \(ABC\), \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{AB}=10\) i \(\overline{BC}=15\). Calcula \(\overline{B'C'}\).", r"En un triángulo \(ABC\), \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{AB}=10\) y \(\overline{BC}=15\). Calcula \(\overline{B'C'}\).", r"In a triangle \(ABC\), \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{AB}=10\) and \(\overline{BC}=15\). Find \(\overline{B'C'}\)."),
       D(r"\frac{4}{10}=\frac{x}{15}\ \Rightarrow\ 10x=60\ \Rightarrow\ x=\boxed{6}"))],
 [prob(L(r"Un triangle té dos angles de 40° i 75°. Un altre en té dos de 65° i 75°. Són semblants?", r"Un triángulo tiene dos ángulos de 40° y 75°. Otro tiene dos de 65° y 75°. ¿Son semejantes?", r"A triangle has two angles of 40° and 75°. Another has two angles of 65° and 75°. Are they similar?"),
       D(r"180^\circ-40^\circ-75^\circ=65^\circ\ \Rightarrow\ 40^\circ,\ 65^\circ,\ 75^\circ\qquad 180^\circ-65^\circ-75^\circ=40^\circ\ \Rightarrow\ 40^\circ,\ 65^\circ,\ 75^\circ"),
       P(r"Tenen els mateixos angles: <strong>són semblants</strong> (criteri 1r).", r"Tienen los mismos ángulos: <strong>son semejantes</strong> (criterio 1.º).", r"They have the same angles: <strong>they are similar</strong> (1st criterion).")),
  prob(L(r"En la figura, \(B'C'\parallel BC\). Calcula \(x=\overline{C'C}\).", r"En la figura, \(B'C'\parallel BC\). Calcula \(x=\overline{C'C}\).", r"In the figure, \(B'C'\parallel BC\). Find \(x=\overline{C'C}\).")
       + figs(G(tpos(6, 6.6, 50, 0.4, labs={'AB1': '4', 'B1B': '6', 'AC1': '5', 'C1C': 'x'}, hot='C1C'), W=230, pad=26)),
       P(r"Pel teorema de Tales, els trossos dels dos costats són proporcionals:", r"Por el teorema de Tales, los trozos de los dos lados son proporcionales:", r"By Thales' theorem, the pieces of the two sides are proportional:"),
       D(r"\frac{4}{6}=\frac{5}{x}\ \Rightarrow\ 4x=30\ \Rightarrow\ x=\boxed{7{,}5}"))],
 [prob(L(r"Dos triangles rectangles tenen un angle agut de 35°. Els catets del primer fan 4 cm i 6 cm. En el segon, el catet homòleg del de 4 cm fa 10 cm. Quant fa l'altre catet? Quina és la raó entre les àrees?", r"Dos triángulos rectángulos tienen un ángulo agudo de 35°. Los catetos del primero miden 4 cm y 6 cm. En el segundo, el cateto homólogo del de 4 cm mide 10 cm. ¿Cuánto mide el otro cateto? ¿Cuál es la razón entre las áreas?", r"Two right triangles have a 35° acute angle. The legs of the first are 4 cm and 6 cm. In the second, the leg matching the 4 cm one is 10 cm. How long is the other leg? What is the ratio of the areas?"),
       P(r"Tenen l'angle recte i un angle de 35° iguals: són semblants (criteri 1r).", r"Tienen el ángulo recto y un ángulo de 35° iguales: son semejantes (criterio 1.º).", r"They share the right angle and a 35° angle: they're similar (1st criterion)."),
       D(r"k=\frac{10}{4}=2{,}5\qquad6\cdot2{,}5=\boxed{15\ \text{cm}}"),
       D(r"A=\frac{4\cdot6}{2}=12\ \text{cm}^2\qquad A'=\frac{10\cdot15}{2}=75\ \text{cm}^2\qquad\frac{75}{12}=\boxed{6{,}25}=2{,}5^2"))])
assert R(9, 3) == R(15, 5) == R(18, 6) == 3; ck(R(60, 10), 6); assert 180 - 40 - 75 == 65 and 180 - 65 - 75 == 40; ck(R(30, 4), 7.5)
ck(R(10, 4), 2.5); ck(6 * R(5, 2), 15); ck(R(4 * 6, 2), 12); ck(R(10 * 15, 2), 75); ck(R(75, 12), 6.25); ck(R(5, 2) ** 2, 6.25)
s4 += practice([
  ('★', L(r"a) Són semblants els triangles de costats 2, 4, 5 i 6, 12, 15? b) I els de costats 3, 4, 6 i 6, 8, 10?", r"a) ¿Son semejantes los triángulos de lados 2, 4, 5 y 6, 12, 15? b) ¿Y los de lados 3, 4, 6 y 6, 8, 10?", r"a) Are the triangles with sides 2, 4, 5 and 6, 12, 15 similar? b) And 3, 4, 6 and 6, 8, 10?")),
  ('★★', L(r"c) En un triangle \(ABC\), \(B'C'\parallel BC\), \(\overline{AB'}=5\), \(\overline{B'B}=3\) i \(\overline{B'C'}=7{,}5\). Calcula \(\overline{BC}\). d) Un triangle té angles de 50° i 60°, i un altre, de 60° i 70°. Són semblants?", r"c) En un triángulo \(ABC\), \(B'C'\parallel BC\), \(\overline{AB'}=5\), \(\overline{B'B}=3\) y \(\overline{B'C'}=7{,}5\). Calcula \(\overline{BC}\). d) Un triángulo tiene ángulos de 50° y 60°, y otro, de 60° y 70°. ¿Son semejantes?", r"c) In a triangle \(ABC\), \(B'C'\parallel BC\), \(\overline{AB'}=5\), \(\overline{B'B}=3\) and \(\overline{B'C'}=7.5\). Find \(\overline{BC}\). d) A triangle has angles of 50° and 60°, another of 60° and 70°. Are they similar?")),
  ('★★★', L(r"e) Els costats d'un triangle fan 5, 6 i 9 cm. Un triangle semblant té 60 cm de perímetre. Quant fan els seus costats?", r"e) Los lados de un triángulo miden 5, 6 y 9 cm. Un triángulo semejante tiene 60 cm de perímetro. ¿Cuánto miden sus lados?", r"e) A triangle has sides 5, 6 and 9 cm. A similar triangle has a perimeter of 60 cm. How long are its sides?"))],
  P(r"a) Sí, \(k=3\). b) No: \(\frac63=\frac84=2\), però \(\frac{10}{6}\approx1{,}67\). c) \(\overline{AB}=8\); \(\frac58=\frac{7{,}5}{x}\Rightarrow x=12\). d) Sí: el primer té 50°, 60° i 70°. e) \(P=20\), \(k=3\): 15, 18 i 27 cm.",
    r"a) Sí, \(k=3\). b) No: \(\frac63=\frac84=2\), pero \(\frac{10}{6}\approx1{,}67\). c) \(\overline{AB}=8\); \(\frac58=\frac{7{,}5}{x}\Rightarrow x=12\). d) Sí: el primero tiene 50°, 60° y 70°. e) \(P=20\), \(k=3\): 15, 18 y 27 cm.",
    r"a) Yes, \(k=3\). b) No: \(\frac63=\frac84=2\), but \(\frac{10}{6}\approx1.67\). c) \(\overline{AB}=8\); \(\frac58=\frac{7.5}{x}\Rightarrow x=12\). d) Yes: the first has 50°, 60° and 70°. e) \(P=20\), \(k=3\): 15, 18 and 27 cm."))
ck(R(10, 6), 1.67, 2); ck(R(8) * R(75, 10) / 5, 12); assert 180 - 50 - 60 == 70; ck(R(60, 20), 3)

# =====================================================================
# 8.5 Problemes amb semblança de triangles
# =====================================================================
s5 = box('prop', L('Com resoldre un problema de semblança', 'Cómo resolver un problema de semejanza', 'How to solve a similarity problem'),
  ol(L(r"Fes un <strong>dibuix</strong> de la situació i marca-hi les dades i la incògnita.", r"Haz un <strong>dibujo</strong> de la situación y marca en él los datos y la incógnita.", r"Make a <strong>drawing</strong> of the situation and mark the data and the unknown on it."),
     L(r"Busca <strong>dos triangles semblants</strong> (amb dos angles iguals, o en posició de Tales).", r"Busca <strong>dos triángulos semejantes</strong> (con dos ángulos iguales, o en posición de Tales).", r"Find <strong>two similar triangles</strong> (with two equal angles, or in Thales position)."),
     L(r"Escriu la <strong>proporció</strong> entre costats homòlegs i resol-la.", r"Escribe la <strong>proporción</strong> entre lados homólogos y resuélvela.", r"Write the <strong>proportion</strong> between corresponding sides and solve it."),
     L(r"Comprova que el resultat té sentit (un arbre no fa 300 m!).", r"Comprueba que el resultado tiene sentido (¡un árbol no mide 300 m!).", r"Check the result makes sense (a tree isn't 300 m tall!)."))
  )
s5 += box('prop', L('Altures amb ombres', 'Alturas con sombras', 'Heights from shadows'),
  P(r"Els rajos del Sol arriben pràcticament <strong>paral·lels</strong>. Al mateix moment, un pal vertical i un edifici formen amb les seues ombres dos triangles rectangles amb els mateixos angles: són <strong>semblants</strong>. Per tant, l'altura i l'ombra són proporcionals:",
    r"Los rayos del Sol llegan prácticamente <strong>paralelos</strong>. En el mismo momento, un palo vertical y un edificio forman con sus sombras dos triángulos rectángulos con los mismos ángulos: son <strong>semejantes</strong>. Por tanto, la altura y la sombra son proporcionales:",
    r"The Sun's rays arrive practically <strong>parallel</strong>. At the same moment, a vertical stick and a building form two right triangles with their shadows that have the same angles: they are <strong>similar</strong>. So height and shadow are proportional:")
  + figs(G(shadow(1.5, 2, 9, 12, '1,5 m', 'H', '2 m', '12 m', hot='h2'), W=320, pad=26))
  + D(r"\frac{H}{12}=\frac{1{,}5}{2}\ \Rightarrow\ H=\frac{12\cdot1{,}5}{2}=9\ \text{m}")
  + note(r"Diuen que Tales de Milet va calcular així l'altura de la gran piràmide d'Egipte: va esperar el moment en què la seua pròpia ombra feia el mateix que la seua altura. En aquell moment, l'ombra de la piràmide (comptada des del centre de la base) també mesurava el mateix que la piràmide.",
         r"Dicen que Tales de Mileto calculó así la altura de la gran pirámide de Egipto: esperó el momento en que su propia sombra medía lo mismo que su altura. En ese momento, la sombra de la pirámide (contada desde el centro de la base) también medía lo mismo que la pirámide.",
         r"Thales of Miletus is said to have found the height of the Great Pyramid this way: he waited for the moment when his own shadow was as long as he was tall. At that moment, the pyramid's shadow (measured from the centre of its base) was also as long as the pyramid was tall.", '🏛️')
  + widget('w-ombra', '☀️', L('Calcula una altura amb les ombres', 'Calcula una altura con las sombras', 'Find a height from shadows'),
           ['<div class="wrow">' + rng('h', 0.5, 3, 0.1, 1.5, 'h') + rng('s', 0.5, 5, 0.1, 2, 's') + '</div>',
            '<div class="wrow">' + rng('S', 2, 30, 0.5, 12, 'S') + '</div>'])
  + drill('ombra', 'Entrena: altures i ombres', 'Entrena: alturas y sombras', 'Train: heights and shadows'))
ck(R(12) * R(15, 10) / 2, 9)
MIR = G([('seg', (-0.5, 0), (12, 0), 'axis'), ('seg', (0, 0), (0, 1.6), 'wall'), ('seg', (11, 0), (11, 7.2), 'wall'),
         ('seg', (0, 1.6), (2, 0), 'ray'), ('seg', (2, 0), (11, 7.2), 'ray'), ('poly', [(0, 0), (0, 1.6), (2, 0)], 'tr'), ('poly', [(2, 0), (11, 0), (11, 7.2)], 'gf'),
         ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (11, 0), (10, 0), (11, 1)), ('dot', (2, 0), 'pa'),
         ('txt', (0, 0.8), '1,6 m', {'dx': -8, 'a': 'end'}), ('txt', (1, 0), '2 m', {'dy': 15}), ('txt', (6.5, 0), '9 m', {'dy': 15}), ('txt', (11, 3.6), 'H', {'dx': 8, 'a': 'start', 'cls': 'hot'}),
         ('txt', (2, 0), Ls('mirall', 'espejo', 'mirror'), {'dy': -10})], W=300, pad=26)
s5 += box('prop', L('Altures amb un mirall', 'Alturas con un espejo', 'Heights with a mirror'),
  P(r"Posem un mirall a terra i ens allunyem fins que hi veiem la punta de l'arbre. Com que la llum es reflecteix amb el mateix angle amb què arriba, els dos triangles rectangles tenen els angles iguals i són semblants:",
    r"Ponemos un espejo en el suelo y nos alejamos hasta que vemos en él la punta del árbol. Como la luz se refleja con el mismo ángulo con el que llega, los dos triángulos rectángulos tienen los ángulos iguales y son semejantes:",
    r"We put a mirror on the ground and step back until we see the top of the tree in it. Since light is reflected at the same angle at which it arrives, the two right triangles have equal angles and are similar:")
  + figs(MIR)
  + D(r"\frac{H}{9}=\frac{1{,}6}{2}\ \Rightarrow\ H=\frac{9\cdot1{,}6}{2}=7{,}2\ \text{m}"))
ck(R(9) * R(16, 10) / 2, 7.2)
FAN = G([('seg', (-0.5, 0), (6.6, 0), 'axis'), ('poly', [(0, 0), (0, 6), (40 / 7, 0)], 'gf'), ('poly', [(4, 0), (4, 1.8), (40 / 7, 0)], 'tr'), ('seg', (0, 0), (0, 6), 'wall'), ('seg', (4, 0), (4, 1.8), 'wall'),
         ('seg', (0, 6), (40 / 7, 0), 'ray'), ('dot', (0, 6), 'pa'), ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (4, 0), (5, 0), (4, 1)),
         ('txt', (0, 3), '6 m', {'dx': -8, 'a': 'end'}), ('txt', (4, 0.9), '1,8', {'dx': -6, 'a': 'end'}), ('txt', (2, 0), '4 m', {'dy': 15}), ('txt', (4 + 6 / 7, 0), 's', {'dy': 15, 'cls': 'hot'})], W=260, pad=26)
s5 += box('prop', L('Distàncies amb triangles en posició de Tales', 'Distancias con triángulos en posición de Tales', 'Distances with triangles in Thales position'),
  P(r"Si la llum ix d'un <strong>punt</strong> (un fanal, una bombeta), o si alineem la vista amb la punta d'un objecte proper i la d'un de llunyà, es formen dos triangles en <strong>posició de Tales</strong>: tenen un angle comú i els costats oposats són paral·lels.",
    r"Si la luz sale de un <strong>punto</strong> (una farola, una bombilla), o si alineamos la vista con la punta de un objeto cercano y la de uno lejano, se forman dos triángulos en <strong>posición de Tales</strong>: tienen un ángulo común y los lados opuestos son paralelos.",
    r"If light comes from a <strong>point</strong> (a street lamp, a bulb), or if we line up our eye with the top of a nearby object and that of a distant one, we get two triangles in <strong>Thales position</strong>: they share an angle and their opposite sides are parallel.")
  + figs(FAN)
  + P(r"Una persona d'1,8 m està a 4 m d'un fanal de 6 m. Els triangles tenen l'angle comú on acaba l'ombra. L'ombra de la persona fa \(s\) i la del fanal, \(s+4\):",
      r"Una persona de 1,8 m está a 4 m de una farola de 6 m. Los triángulos tienen el ángulo común donde acaba la sombra. La sombra de la persona mide \(s\) y la de la farola, \(s+4\):",
      r"A 1.8 m tall person stands 4 m from a 6 m street lamp. The triangles share the angle where the shadow ends. The person's shadow is \(s\) and the lamp's is \(s+4\):")
  + D(r"\frac{1{,}8}{s}=\frac{6}{s+4}\ \Rightarrow\ 1{,}8s+7{,}2=6s\ \Rightarrow\ 7{,}2=4{,}2s\ \Rightarrow\ s=\frac{7{,}2}{4{,}2}\approx1{,}71\ \text{m}"))
ck(R(72, 42), 1.71, 2); assert sp.solve(R(18, 10) * (x_ := sp.Symbol('s')) + R(72, 10) - 6 * x_, x_) == [R(72, 42)]
s5 += levels(
 [prob(L(r"Un arbre fa una ombra de 8 m. Al mateix moment, un bastó d'1 m fa una ombra de 0,8 m. Quina altura té l'arbre?", r"Un árbol da una sombra de 8 m. En el mismo momento, un bastón de 1 m da una sombra de 0,8 m. ¿Qué altura tiene el árbol?", r"A tree casts an 8 m shadow. At the same moment, a 1 m stick casts a 0.8 m shadow. How tall is the tree?"),
       D(r"\frac{H}{8}=\frac{1}{0{,}8}\ \Rightarrow\ H=\frac{8\cdot1}{0{,}8}=\boxed{10\ \text{m}}")),
  prob(L(r"Un edifici de 24 m fa una ombra de 18 m. Quina ombra fa, al mateix moment, una persona d'1,6 m?", r"Un edificio de 24 m da una sombra de 18 m. ¿Qué sombra da, en el mismo momento, una persona de 1,6 m?", r"A 24 m building casts an 18 m shadow. What shadow does a 1.6 m person cast at the same moment?"),
       D(r"\frac{1{,}6}{s}=\frac{24}{18}\ \Rightarrow\ 24s=28{,}8\ \Rightarrow\ s=\boxed{1{,}2\ \text{m}}"))],
 [prob(L(r"La Marta (els ulls a 1,5 m de terra) posa un mirall a terra a 2 m d'ella i a 12 m d'una torre. Quan mira el mirall hi veu just la punta de la torre. Quina altura té la torre?", r"Marta (los ojos a 1,5 m del suelo) pone un espejo en el suelo a 2 m de ella y a 12 m de una torre. Cuando mira el espejo ve justo la punta de la torre. ¿Qué altura tiene la torre?", r"Marta (eyes 1.5 m above the ground) puts a mirror on the ground 2 m from her and 12 m from a tower. Looking into it, she sees exactly the top of the tower. How tall is the tower?"),
       D(r"\frac{H}{12}=\frac{1{,}5}{2}\ \Rightarrow\ H=\frac{12\cdot1{,}5}{2}=\boxed{9\ \text{m}}")),
  prob(L(r"Una rampa puja 1,2 m d'altura en 8 m horitzontals. A quina altura està un punt de la rampa que és a 3 m (horitzontals) del començament?", r"Una rampa sube 1,2 m de altura en 8 m horizontales. ¿A qué altura está un punto de la rampa que está a 3 m (horizontales) del comienzo?", r"A ramp rises 1.2 m over 8 m horizontally. How high is a point on the ramp 3 m (horizontally) from the start?"),
       P(r"Els dos triangles (el de 3 m i el de 8 m) estan en posició de Tales: tenen l'angle del començament de la rampa comú.", r"Los dos triángulos (el de 3 m y el de 8 m) están en posición de Tales: tienen común el ángulo del comienzo de la rampa.", r"The two triangles (the 3 m one and the 8 m one) are in Thales position: they share the angle at the start of the ramp."),
       D(r"\frac{h}{3}=\frac{1{,}2}{8}\ \Rightarrow\ h=\frac{3\cdot1{,}2}{8}=\boxed{0{,}45\ \text{m}}"))],
 [prob(L(r"Per a saber l'amplària d'un riu, la Joana tria un arbre \(A\) de l'altra riba i fa aquestes mesures a la seua riba: \(\overline{BC}=6\) m, \(\overline{CD}=2\) m i \(\overline{DE}=3\) m, de manera que \(BA\) i \(DE\) són paral·leles i \(A\), \(C\) i \(E\) estan alineats. Quant fa d'ample el riu (\(\overline{AB}\))?", r"Para saber la anchura de un río, Juana elige un árbol \(A\) de la otra orilla y hace estas medidas en su orilla: \(\overline{BC}=6\) m, \(\overline{CD}=2\) m y \(\overline{DE}=3\) m, de modo que \(BA\) y \(DE\) son paralelas y \(A\), \(C\) y \(E\) están alineados. ¿Cuánto mide de ancho el río (\(\overline{AB}\))?", r"To find the width of a river, Joana picks a tree \(A\) on the far bank and measures on her side: \(\overline{BC}=6\) m, \(\overline{CD}=2\) m and \(\overline{DE}=3\) m, so that \(BA\) and \(DE\) are parallel and \(A\), \(C\) and \(E\) are in line. How wide is the river (\(\overline{AB}\))?")
       + figs(G([('poly', [(-1, 0.25), (9, 0.25), (9, 8.75), (-1, 8.75)], 'water'), ('poly', [(0, 0), (0, 9), (6, 0)], 'gf'), ('poly', [(6, 0), (8, 0), (8, -3)], 'tr'), ('seg', (0, 9), (8, -3), 'ray'), ('seg', (-1, 0), (9, 0), 'axis'),
                 ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (8, 0), (7, 0), (8, -1)),
                 ('dot', (0, 9)), ('dot', (0, 0)), ('dot', (6, 0)), ('dot', (8, 0)), ('dot', (8, -3)),
                 ('txt', (0, 9), 'A', {'dx': -8, 'a': 'end'}), ('txt', (0, 0), 'B', {'dx': -8, 'a': 'end'}), ('txt', (6, 0), 'C', {'dy': -8}), ('txt', (8, 0), 'D', {'dx': 8, 'a': 'start', 'dy': -6}), ('txt', (8, -3), 'E', {'dx': 8, 'a': 'start'}),
                 ('txt', (3, 0), '6 m', {'dy': 15}), ('txt', (7, 0), '2', {'dy': -8}), ('txt', (8, -1.5), '3 m', {'dx': 8, 'a': 'start'}), ('txt', (0, 4.5), 'x', {'dx': -8, 'a': 'end', 'cls': 'hot'})], W=230, pad=26)),
       P(r"Els triangles \(ABC\) i \(EDC\) tenen els angles en \(C\) iguals (oposats pel vèrtex) i un angle recte: són semblants.", r"Los triángulos \(ABC\) y \(EDC\) tienen los ángulos en \(C\) iguales (opuestos por el vértice) y un ángulo recto: son semejantes.", r"Triangles \(ABC\) and \(EDC\) have equal angles at \(C\) (vertically opposite) and a right angle: they are similar."),
       D(r"\frac{x}{3}=\frac{6}{2}\ \Rightarrow\ x=\frac{3\cdot6}{2}=\boxed{9\ \text{m}}")),
  prob(L(r"Un nen d'1,2 m està a 3 m d'un fanal de 4,8 m. Quant fa la seua ombra?", r"Un niño de 1,2 m está a 3 m de una farola de 4,8 m. ¿Cuánto mide su sombra?", r"A 1.2 m tall child stands 3 m from a 4.8 m street lamp. How long is their shadow?"),
       D(r"\frac{1{,}2}{s}=\frac{4{,}8}{s+3}\ \Rightarrow\ 1{,}2s+3{,}6=4{,}8s\ \Rightarrow\ 3{,}6=3{,}6s\ \Rightarrow\ s=\boxed{1\ \text{m}}"),
       P(r"Comprovació: \(\frac{1{,}2}{1}=1{,}2\) i \(\frac{4{,}8}{4}=1{,}2\) ✓", r"Comprobación: \(\frac{1{,}2}{1}=1{,}2\) y \(\frac{4{,}8}{4}=1{,}2\) ✓", r"Check: \(\frac{1.2}{1}=1.2\) and \(\frac{4.8}{4}=1.2\) ✓"))])
ck(R(8) / R(8, 10), 10); ck(R(16, 10) * 18, 28.8); ck(R(288, 240), 1.2); ck(R(12) * R(15, 10) / 2, 9); ck(R(3) * R(12, 10) / 8, 0.45); ck(R(3 * 6, 2), 9)
assert sp.solve(R(12, 10) * (s_ := sp.Symbol('s')) + R(36, 10) - R(48, 10) * s_, s_) == [1]
s5 += practice([
  ('★', L(r"a) Un pal d'1,5 m fa una ombra de 2,5 m. Quina altura té una antena que fa una ombra de 30 m? b) Una persona d'1,7 m fa una ombra de 2 m. Quina ombra fa un arbre de 5,1 m?", r"a) Un palo de 1,5 m da una sombra de 2,5 m. ¿Qué altura tiene una antena que da una sombra de 30 m? b) Una persona de 1,7 m da una sombra de 2 m. ¿Qué sombra da un árbol de 5,1 m?", r"a) A 1.5 m stick casts a 2.5 m shadow. How tall is an aerial that casts a 30 m shadow? b) A 1.7 m person casts a 2 m shadow. What shadow does a 5.1 m tree cast?")),
  ('★★', L(r"c) Amb els ulls a 1,6 m de terra i un mirall a 1,2 m de nosaltres, veiem la punta d'un pi que està a 6 m del mirall. Quina altura té el pi?", r"c) Con los ojos a 1,6 m del suelo y un espejo a 1,2 m de nosotros, vemos la punta de un pino que está a 6 m del espejo. ¿Qué altura tiene el pino?", r"c) With our eyes 1.6 m above the ground and a mirror 1.2 m from us, we see the top of a pine tree 6 m from the mirror. How tall is the pine?")),
  ('★★★', L(r"d) Mirem una torre llunyana i la tapem exactament amb un regle vertical de 20 cm que tenim a 60 cm dels ulls. Si la torre fa 30 m, a quina distància està de nosaltres?", r"d) Miramos una torre lejana y la tapamos exactamente con una regla vertical de 20 cm que tenemos a 60 cm de los ojos. Si la torre mide 30 m, ¿a qué distancia está de nosotros?", r"d) We look at a distant tower and exactly cover it with a 20 cm vertical ruler held 60 cm from our eyes. If the tower is 30 m tall, how far away is it?"))],
  P(r"a) \(\frac{H}{30}=\frac{1{,}5}{2{,}5}\Rightarrow H=18\) m. b) \(\frac{5{,}1}{s}=\frac{1{,}7}{2}\Rightarrow s=6\) m. c) \(H=\frac{6\cdot1{,}6}{1{,}2}=8\) m. d) \(\frac{d}{30}=\frac{0{,}6}{0{,}2}\Rightarrow d=90\) m.",
    r"a) \(\frac{H}{30}=\frac{1{,}5}{2{,}5}\Rightarrow H=18\) m. b) \(\frac{5{,}1}{s}=\frac{1{,}7}{2}\Rightarrow s=6\) m. c) \(H=\frac{6\cdot1{,}6}{1{,}2}=8\) m. d) \(\frac{d}{30}=\frac{0{,}6}{0{,}2}\Rightarrow d=90\) m.",
    r"a) \(\frac{H}{30}=\frac{1.5}{2.5}\Rightarrow H=18\) m. b) \(\frac{5.1}{s}=\frac{1.7}{2}\Rightarrow s=6\) m. c) \(H=\frac{6\cdot1.6}{1.2}=8\) m. d) \(\frac{d}{30}=\frac{0.6}{0.2}\Rightarrow d=90\) m."))
ck(R(30) * R(15, 10) / R(25, 10), 18); ck(R(51, 10) * 2 / R(17, 10), 6); ck(R(6) * R(16, 10) / R(12, 10), 8); ck(R(30) * R(6, 10) / R(2, 10), 90)
