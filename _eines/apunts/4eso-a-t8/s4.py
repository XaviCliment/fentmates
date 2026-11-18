# 8.4 Semblança de triangles: triangles en posició de Tales i criteris de semblança
# Apunts de la Unitat 8 de 4t ESO A (Semblança. Aplicacions), fets a partir de l'apartat 8.4 de 2n ESO (../2eso-t8/s45.py).
# Cada resultat es comprova amb ck().
from comu import *
from fig8 import *

# =====================================================================
# 8.4 Semblança de triangles
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
  + P(r"En particular, <strong>tots els triangles equilàters</strong> són semblants (tenen tots els angles de 60°). Els <strong>triangles rectangles</strong> tenen uns criteris encara més senzills, que veurem a l'apartat 8.6.",
      r"En particular, <strong>todos los triángulos equiláteros</strong> son semejantes (tienen todos los ángulos de 60°). Los <strong>triángulos rectángulos</strong> tienen unos criterios todavía más sencillos, que veremos en el apartado 8.6.",
      r"In particular, <strong>all equilateral triangles</strong> are similar (all their angles are 60°). <strong>Right triangles</strong> have even simpler criteria, which we'll see in section 8.6."))
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
