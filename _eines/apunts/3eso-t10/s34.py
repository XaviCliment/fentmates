# 10.3 Dividir un segment en parts iguals o proporcionals · 10.4 Triangles en posició de Tales
from comu import *
from fig10 import *

# =====================================================================
# 10.3 Dividir un segment en parts iguals o proporcionals
# =====================================================================
s3 = box('prop', L('Dividir un segment en parts iguals', 'Dividir un segmento en partes iguales', 'Dividing a segment into equal parts'),
  P(r"Amb el teorema de Tales podem dividir un segment \(AB\) en \(n\) parts iguals <strong>sense mesurar-lo</strong>, només amb regle i compàs (o escaire i cartabó):",
    r"Con el teorema de Tales podemos dividir un segmento \(AB\) en \(n\) partes iguales <strong>sin medirlo</strong>, solo con regla y compás (o escuadra y cartabón):",
    r"Thales' theorem lets us divide a segment \(AB\) into \(n\) equal parts <strong>without measuring it</strong>, using only a ruler and compasses (or set squares):")
  + ol(L(r"Des de l'extrem \(A\) traça una semirecta auxiliar, amb qualsevol inclinació.", r"Desde el extremo \(A\) traza una semirrecta auxiliar, con cualquier inclinación.", r"From the end point \(A\), draw an auxiliary ray at any angle."),
       L(r"Amb el compàs, marca-hi \(n\) segments iguals, un rere l'altre, començant en \(A\).", r"Con el compás, marca en ella \(n\) segmentos iguales, uno tras otro, empezando en \(A\).", r"With the compasses, mark \(n\) equal segments on it, one after another, starting at \(A\)."),
       L(r"Uneix l'última marca amb l'extrem \(B\).", r"Une la última marca con el extremo \(B\).", r"Join the last mark to the end point \(B\)."),
       L(r"Traça per les altres marques rectes <strong>paral·leles</strong> a aquesta. Tallen \(AB\) en \(n\) parts iguals.", r"Traza por las otras marcas rectas <strong>paralelas</strong> a esta. Cortan \(AB\) en \(n\) partes iguales.", r"Through the other marks draw lines <strong>parallel</strong> to it. They cut \(AB\) into \(n\) equal parts."))
  + P(r"Les paral·leles tallen la semirecta en segments iguals; pel teorema de Tales, també tallen \(AB\) en segments iguals.",
      r"Las paralelas cortan la semirrecta en segmentos iguales; por el teorema de Tales, también cortan \(AB\) en segmentos iguales.",
      r"The parallels cut the ray into equal segments, so by Thales' theorem they also cut \(AB\) into equal segments.")
  + widget('w-div', '✂️', L('Divideix un segment', 'Divide un segmento', 'Divide a segment'),
           [seg([('eq', L('Parts iguals', 'Partes iguales', 'Equal parts')), ('pr', L('Parts proporcionals', 'Partes proporcionales', 'Proportional parts'))]),
            '<div class="wrow">' + tin('L', L('Longitud de AB =', 'Longitud de AB =', 'Length of AB ='), '12') + tin('n', L('Nombre de parts =', 'Número de partes =', 'Number of parts ='), '5', 'eqonly') + tin('k', L('Proporcionals a', 'Proporcionales a', 'Proportional to'), '2, 3, 4', 'm pronly') + '</div>',
            '<div class="wrow">' + '<button class="btn" type="button" data-a="step">' + L('Pas següent de la construcció', 'Paso siguiente de la construcción', 'Next construction step') + '</button></div>'],
           out='<div class="gout"></div><div class="hsteps"></div>'))
s3 += box('prop', L('Dividir un segment en parts proporcionals', 'Dividir un segmento en partes proporcionales', 'Dividing a segment into proportional parts'),
  P(r"Per a dividir \(AB\) en parts proporcionals a uns nombres (per exemple, 2, 3 i 4), sobre la semirecta auxiliar marquem \(2+3+4=9\) segments iguals i tracem les paral·leles només per les marques 2 i \(2+3=5\).",
    r"Para dividir \(AB\) en partes proporcionales a unos números (por ejemplo, 2, 3 y 4), sobre la semirrecta auxiliar marcamos \(2+3+4=9\) segmentos iguales y trazamos las paralelas solo por las marcas 2 y \(2+3=5\).",
    r"To divide \(AB\) into parts proportional to some numbers (for example 2, 3 and 4), mark \(2+3+4=9\) equal segments on the auxiliary ray and draw the parallels only through marks 2 and \(2+3=5\).")
  + figs(G(divseg(18, [2, 3, 4]), W=300, pad=26, cap=L('18 cm en parts proporcionals a 2, 3 i 4', '18 cm en partes proporcionales a 2, 3 y 4', '18 cm in parts proportional to 2, 3 and 4')))
  + P(r"També ho podem <strong>calcular</strong>: és un repartiment proporcional. Dividim la longitud entre la suma dels nombres i multipliquem per cada nombre:",
      r"También lo podemos <strong>calcular</strong>: es un reparto proporcional. Dividimos la longitud entre la suma de los números y multiplicamos por cada número:",
      r"We can also <strong>calculate</strong> it: it's a proportional distribution. Divide the length by the sum of the numbers and multiply by each number:")
  + D(r"\frac{18}{2+3+4}=\frac{18}{9}=2\qquad 2\cdot2=4\ \text{cm},\quad 3\cdot2=6\ \text{cm},\quad 4\cdot2=8\ \text{cm}")
  + drill('div', 'Entrena: divideix en parts proporcionals', 'Entrena: divide en partes proporcionales', 'Train: divide into proportional parts'))
assert 18 * 2 // 9 == 4 and 18 * 3 // 9 == 6 and 18 * 4 // 9 == 8
s3 += levels(
 [prob(L(r"Un segment de 15 cm es divideix en 6 parts iguals. Quant fa cada part? Explica com ho faries amb regle i compàs.", r"Un segmento de 15 cm se divide en 6 partes iguales. ¿Cuánto mide cada parte? Explica cómo lo harías con regla y compás.", r"A 15 cm segment is divided into 6 equal parts. How long is each part? Explain how you would do it with a ruler and compasses."),
       D(r"\frac{15}{6}=\boxed{2{,}5\ \text{cm}}"),
       P(r"Semirecta auxiliar des d'\(A\), 6 marques iguals amb el compàs, unim la sisena amb \(B\) i tracem paral·leles per les altres cinc.", r"Semirrecta auxiliar desde \(A\), 6 marcas iguales con el compás, unimos la sexta con \(B\) y trazamos paralelas por las otras cinco.", r"Auxiliary ray from \(A\), 6 equal marks with the compasses, join the sixth to \(B\) and draw parallels through the other five."))],
 [prob(L(r"Divideix un segment de 20 cm en tres parts proporcionals a 1, 3 i 4.", r"Divide un segmento de 20 cm en tres partes proporcionales a 1, 3 y 4.", r"Divide a 20 cm segment into three parts proportional to 1, 3 and 4."),
       D(r"\frac{20}{1+3+4}=\frac{20}{8}=2{,}5"),
       D(r"1\cdot2{,}5=\boxed{2{,}5\ \text{cm}}\qquad3\cdot2{,}5=\boxed{7{,}5\ \text{cm}}\qquad4\cdot2{,}5=\boxed{10\ \text{cm}}"),
       P(r"Amb la construcció: 8 marques iguals; paral·leles per les marques 1 i 4.", r"Con la construcción: 8 marcas iguales; paralelas por las marcas 1 y 4.", r"With the construction: 8 equal marks; parallels through marks 1 and 4."))],
 [prob(L(r"Un punt \(P\) divideix un segment \(AB\) de 28 cm de manera que \(\frac{\overline{AP}}{\overline{PB}}=\frac34\). Quant mesuren \(\overline{AP}\) i \(\overline{PB}\)?", r"Un punto \(P\) divide un segmento \(AB\) de 28 cm de manera que \(\frac{\overline{AP}}{\overline{PB}}=\frac34\). ¿Cuánto miden \(\overline{AP}\) y \(\overline{PB}\)?", r"A point \(P\) divides a 28 cm segment \(AB\) so that \(\frac{\overline{AP}}{\overline{PB}}=\frac34\). How long are \(\overline{AP}\) and \(\overline{PB}\)?"),
       P(r"Vol dir que \(AB\) es divideix en parts proporcionals a 3 i 4:", r"Quiere decir que \(AB\) se divide en partes proporcionales a 3 y 4:", r"It means \(AB\) is divided into parts proportional to 3 and 4:"),
       D(r"\frac{28}{3+4}=4\ \Rightarrow\ \overline{AP}=3\cdot4=\boxed{12\ \text{cm}},\quad\overline{PB}=4\cdot4=\boxed{16\ \text{cm}}"),
       P(r"Comprovació: \(\frac{12}{16}=\frac34\ \checkmark\)", r"Comprobación: \(\frac{12}{16}=\frac34\ \checkmark\)", r"Check: \(\frac{12}{16}=\frac34\ \checkmark\)"))])
ck(R(15, 6), 2.5); ck(R(20, 8), 2.5); ck(R(28, 7) * 3, 12); ck(R(12, 16), R(3, 4))
s3 += practice([
  ('★', L(r"a) Divideix un segment de 14 cm en 4 parts iguals. Quant fa cada part?", r"a) Divide un segmento de 14 cm en 4 partes iguales. ¿Cuánto mide cada parte?", r"a) Divide a 14 cm segment into 4 equal parts. How long is each part?")),
  ('★★', L(r"b) Divideix un segment de 24 cm en parts proporcionals a 1, 2 i 3. c) I un de 10 cm en parts proporcionals a 2 i 3?", r"b) Divide un segmento de 24 cm en partes proporcionales a 1, 2 y 3. c) ¿Y uno de 10 cm en partes proporcionales a 2 y 3?", r"b) Divide a 24 cm segment into parts proportional to 1, 2 and 3. c) And a 10 cm one into parts proportional to 2 and 3?")),
  ('★★★', L(r"d) Un punt divideix un segment en dues parts proporcionals a 2 i 5, i la part més llarga fa 4,5 cm més que la curta. Quant mesura el segment?", r"d) Un punto divide un segmento en dos partes proporcionales a 2 y 5, y la parte más larga mide 4,5 cm más que la corta. ¿Cuánto mide el segmento?", r"d) A point divides a segment into two parts proportional to 2 and 5, and the longer part is 4.5 cm longer than the shorter one. How long is the segment?"))],
  P(r"a) \(14:4=3{,}5\) cm. b) \(24:6=4\): 4, 8 i 12 cm. c) \(10:5=2\): 4 i 6 cm. d) Les parts són \(2u\) i \(5u\); \(5u-2u=4{,}5\Rightarrow u=1{,}5\); segment \(7u=10{,}5\) cm.",
    r"a) \(14:4=3{,}5\) cm. b) \(24:6=4\): 4, 8 y 12 cm. c) \(10:5=2\): 4 y 6 cm. d) Las partes son \(2u\) y \(5u\); \(5u-2u=4{,}5\Rightarrow u=1{,}5\); segmento \(7u=10{,}5\) cm.",
    r"a) \(14:4=3.5\) cm. b) \(24:6=4\): 4, 8 and 12 cm. c) \(10:5=2\): 4 and 6 cm. d) The parts are \(2u\) and \(5u\); \(5u-2u=4.5\Rightarrow u=1.5\); segment \(7u=10.5\) cm."))
ck(R(14, 4), 3.5); ck(R(45, 10) / 3 * 7, 10.5)

# =====================================================================
# 10.4 Triangles en posició de Tales
# =====================================================================
s4 = box('def', L('Triangles en posició de Tales', 'Triángulos en posición de Tales', 'Triangles in Thales position'),
  P(r"Dos triangles \(ABC\) i \(AB'C'\) estan en <strong>posició de Tales</strong> si tenen un angle comú, \(\hat A\), i els costats oposats a aquest angle, \(BC\) i \(B'C'\), són <strong>paral·lels</strong>.",
    r"Dos triángulos \(ABC\) y \(AB'C'\) están en <strong>posición de Tales</strong> si tienen un ángulo común, \(\hat A\), y los lados opuestos a ese ángulo, \(BC\) y \(B'C'\), son <strong>paralelos</strong>.",
    r"Two triangles \(ABC\) and \(AB'C'\) are in <strong>Thales position</strong> if they share an angle, \(\hat A\), and the sides opposite that angle, \(BC\) and \(B'C'\), are <strong>parallel</strong>.")
  + figs(G(tpos(6, 6.5, 52, 0.55), W=240, cap=r"\(B'C'\parallel BC\)"))
  + P(r"Aleshores els tres costats del triangle menut són proporcionals als tres costats del gran:",
      r"Entonces los tres lados del triángulo pequeño son proporcionales a los tres lados del grande:",
      r"Then the three sides of the small triangle are proportional to the three sides of the big one:")
  + D(r"\frac{\overline{AB'}}{\overline{AB}}=\frac{\overline{AC'}}{\overline{AC}}=\frac{\overline{B'C'}}{\overline{BC}}")
  + P(r"Les dues primeres raons venen directament del teorema de Tales. Per a la tercera, que inclou els costats paral·lels, cal comparar <strong>costats sencers</strong> (des del vèrtex \(A\)), no els trossos \(\overline{B'B}\) o \(\overline{C'C}\).",
      r"Las dos primeras razones vienen directamente del teorema de Tales. Para la tercera, que incluye los lados paralelos, hay que comparar <strong>lados enteros</strong> (desde el vértice \(A\)), no los trozos \(\overline{B'B}\) o \(\overline{C'C}\).",
      r"The first two ratios come straight from Thales' theorem. For the third one, which includes the parallel sides, you must compare <strong>whole sides</strong> (from vertex \(A\)), not the pieces \(\overline{B'B}\) or \(\overline{C'C}\).")
  + note(r"Error típic: escriure \(\frac{\overline{AB'}}{\overline{B'B}}=\frac{\overline{B'C'}}{\overline{BC}}\). Aquesta proporció és <strong>falsa</strong>; la bona és \(\frac{\overline{AB'}}{\overline{AB}}=\frac{\overline{B'C'}}{\overline{BC}}\).",
         r"Error típico: escribir \(\frac{\overline{AB'}}{\overline{B'B}}=\frac{\overline{B'C'}}{\overline{BC}}\). Esta proporción es <strong>falsa</strong>; la buena es \(\frac{\overline{AB'}}{\overline{AB}}=\frac{\overline{B'C'}}{\overline{BC}}\).",
         r"Typical mistake: writing \(\frac{\overline{AB'}}{\overline{B'B}}=\frac{\overline{B'C'}}{\overline{BC}}\). That proportion is <strong>false</strong>; the right one is \(\frac{\overline{AB'}}{\overline{AB}}=\frac{\overline{B'C'}}{\overline{BC}}\).", '⚠️')
  + widget('w-tpos', '🔺', L('Desplaça el costat paral·lel', 'Desplaza el lado paralelo', 'Slide the parallel side'),
           ['<div class="wrow">' + rng('t', 0.1, 0.95, 0.05, 0.5, 't') + '</div>',
            '<div class="wrow">' + tin('AB', 'AB =', '8') + tin('AC', 'AC =', '10') + tin('BC', 'BC =', '9') + '</div>']))
s4 += box('prop', L('Com es calcula', 'Cómo se calcula', 'How to calculate'),
  P(r"En el triangle de la figura, \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{B'B}=6\) i \(\overline{BC}=12{,}5\). Calculem \(\overline{B'C'}\):",
    r"En el triángulo de la figura, \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{B'B}=6\) y \(\overline{BC}=12{,}5\). Calculamos \(\overline{B'C'}\):",
    r"In the triangle in the figure, \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{B'B}=6\) and \(\overline{BC}=12.5\). Let's find \(\overline{B'C'}\):")
  + figs(G(tpos(6, 6.5, 52, 0.4, labs={'AB1': '4', 'B1B': '6', 'BC': '12,5', 'B1C1': 'x'}, hot='B1C1'), W=240))
  + D(r"\overline{AB}=4+6=10\qquad\frac{4}{10}=\frac{x}{12{,}5}\ \Rightarrow\ x=\frac{4\cdot12{,}5}{10}=5")
  + drill('tpos', 'Entrena: triangles en posició de Tales', 'Entrena: triángulos en posición de Tales', 'Train: triangles in Thales position'))
ck(R(4) * R(125, 10) / 10, 5)
s4 += levels(
 [prob(L(r"En el triangle \(ABC\), \(B'C'\parallel BC\). Si \(\overline{AB'}=3\) cm, \(\overline{AB}=9\) cm i \(\overline{BC}=12\) cm, quant mesura \(\overline{B'C'}\)?", r"En el triángulo \(ABC\), \(B'C'\parallel BC\). Si \(\overline{AB'}=3\) cm, \(\overline{AB}=9\) cm y \(\overline{BC}=12\) cm, ¿cuánto mide \(\overline{B'C'}\)?", r"In triangle \(ABC\), \(B'C'\parallel BC\). If \(\overline{AB'}=3\) cm, \(\overline{AB}=9\) cm and \(\overline{BC}=12\) cm, how long is \(\overline{B'C'}\)?"),
       D(r"\frac{3}{9}=\frac{x}{12}\ \Rightarrow\ x=\frac{3\cdot12}{9}=\boxed{4\ \text{cm}}"))],
 [prob(L(r"En la figura, \(B'C'\parallel BC\). Calcula \(x=\overline{AC'}\) i \(y=\overline{BC}\).", r"En la figura, \(B'C'\parallel BC\). Calcula \(x=\overline{AC'}\) e \(y=\overline{BC}\).", r"In the figure \(B'C'\parallel BC\). Find \(x=\overline{AC'}\) and \(y=\overline{BC}\).")
       + figs(G(tpos(6, 6.5, 52, 0.4, labs={'AB1': '6', 'B1B': '9', 'AC1': 'x', 'C1C': '10,5', 'B1C1': '5', 'BC': 'y'}), W=250)),
       P(r"Amb el teorema de Tales sobre els costats \(AB\) i \(AC\):", r"Con el teorema de Tales sobre los lados \(AB\) y \(AC\):", r"With Thales' theorem on the sides \(AB\) and \(AC\):"),
       D(r"\frac{6}{9}=\frac{x}{10{,}5}\ \Rightarrow\ x=\frac{6\cdot10{,}5}{9}=\boxed{7}"),
       P(r"Per al costat paral·lel, costats sencers: \(\overline{AB}=6+9=15\).", r"Para el lado paralelo, lados enteros: \(\overline{AB}=6+9=15\).", r"For the parallel side, use whole sides: \(\overline{AB}=6+9=15\)."),
       D(r"\frac{6}{15}=\frac{5}{y}\ \Rightarrow\ y=\frac{15\cdot5}{6}=\boxed{12{,}5}"))],
 [prob(L(r"Per a mesurar l'amplària \(x\) d'un riu, clavem estaques com en la figura: \(\overline{AB}=x\) (amplària del riu), \(\overline{BC}=12\) m, \(\overline{CD}=8\) m i \(\overline{DE}=10\) m, amb \(AB\parallel DE\) i els punts \(A,\,C,\,E\) alineats, igual que \(B,\,C,\,D\). Quina amplària té el riu?", r"Para medir la anchura \(x\) de un río, clavamos estacas como en la figura: \(\overline{AB}=x\) (anchura del río), \(\overline{BC}=12\) m, \(\overline{CD}=8\) m y \(\overline{DE}=10\) m, con \(AB\parallel DE\) y los puntos \(A,\,C,\,E\) alineados, igual que \(B,\,C,\,D\). ¿Qué anchura tiene el río?", r"To measure the width \(x\) of a river we drive in stakes as in the figure: \(\overline{AB}=x\) (river width), \(\overline{BC}=12\) m, \(\overline{CD}=8\) m and \(\overline{DE}=10\) m, with \(AB\parallel DE\) and the points \(A,\,C,\,E\) in a line, as are \(B,\,C,\,D\). How wide is the river?")
       + figs(G([('poly', [(-3, 1.6), (22, 1.6), (22, 13.4), (-3, 13.4)], 'water'), ('poly', [(0, 0), (12, 0), (0, 15)], 'gf'), ('poly', [(12, 0), (20, 0), (20, -10)], 'tr'),
                 ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (20, 0), (19, 0), (20, -1)), ('dot', (0, 0)), ('dot', (0, 15)), ('dot', (12, 0)), ('dot', (20, 0)), ('dot', (20, -10)),
                 ('txt', (0, 15), 'A', {'dx': -8, 'a': 'end'}), ('txt', (0, 0), 'B', {'dx': -8, 'a': 'end', 'dy': 10}), ('txt', (12, 0), 'C', {'dy': -8}), ('txt', (20, 0), 'D', {'dx': 8, 'a': 'start'}), ('txt', (20, -10), 'E', {'dx': 8, 'a': 'start'}),
                 ('txt', (0, 7.5), 'x', {'dx': 10, 'a': 'start', 'cls': 'hot'}), ('txt', (6, 0), '12 m', {'dy': 15}), ('txt', (16, 0), '8 m', {'dy': -7}), ('txt', (20, -5), '10 m', {'dx': 8, 'a': 'start'})], W=250, pad=26)),
       P(r"Els triangles \(ABC\) i \(EDC\) tenen els angles en \(C\) iguals (oposats pel vèrtex) i els costats \(AB\) i \(DE\) paral·lels: estan en posició de Tales (girada). Per tant:", r"Los triángulos \(ABC\) y \(EDC\) tienen los ángulos en \(C\) iguales (opuestos por el vértice) y los lados \(AB\) y \(DE\) paralelos: están en posición de Tales (girada). Por tanto:", r"Triangles \(ABC\) and \(EDC\) have equal angles at \(C\) (vertically opposite) and parallel sides \(AB\) and \(DE\): they're in (rotated) Thales position. So:"),
       D(r"\frac{x}{10}=\frac{12}{8}\ \Rightarrow\ x=\frac{10\cdot12}{8}=\boxed{15\ \text{m}}"))])
ck(R(3 * 12, 9), 4); ck(R(6) * R(105, 10) / 9, 7); ck(R(15 * 5, 6), 12.5); ck(R(10 * 12, 8), 15)
s4 += practice([
  ('★', L(r"a) \(B'C'\parallel BC\), \(\overline{AB'}=5\), \(\overline{AB}=20\), \(\overline{BC}=16\). Calcula \(\overline{B'C'}\).", r"a) \(B'C'\parallel BC\), \(\overline{AB'}=5\), \(\overline{AB}=20\), \(\overline{BC}=16\). Calcula \(\overline{B'C'}\).", r"a) \(B'C'\parallel BC\), \(\overline{AB'}=5\), \(\overline{AB}=20\), \(\overline{BC}=16\). Find \(\overline{B'C'}\).")),
  ('★★', L(r"b) \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{B'B}=2\), \(\overline{B'C'}=6\). Calcula \(\overline{BC}\). c) Amb les mateixes dades i \(\overline{AC}=7{,}5\), calcula \(\overline{AC'}\).", r"b) \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{B'B}=2\), \(\overline{B'C'}=6\). Calcula \(\overline{BC}\). c) Con los mismos datos y \(\overline{AC}=7{,}5\), calcula \(\overline{AC'}\).", r"b) \(B'C'\parallel BC\), \(\overline{AB'}=4\), \(\overline{B'B}=2\), \(\overline{B'C'}=6\). Find \(\overline{BC}\). c) With the same data and \(\overline{AC}=7.5\), find \(\overline{AC'}\).")),
  ('★★★', L(r"d) En un triangle de 12 cm de base i 8 cm d'altura tracem una paral·lela a la base a 2 cm del vèrtex oposat. Quant mesura el segment de la paral·lela que queda dins del triangle?", r"d) En un triángulo de 12 cm de base y 8 cm de altura trazamos una paralela a la base a 2 cm del vértice opuesto. ¿Cuánto mide el segmento de la paralela que queda dentro del triángulo?", r"d) In a triangle with a 12 cm base and an 8 cm height we draw a line parallel to the base 2 cm from the opposite vertex. How long is the part of that line inside the triangle?"))],
  P(r"a) \(\frac5{20}=\frac x{16}\Rightarrow x=4\). b) \(\frac46=\frac6x\Rightarrow x=9\). c) \(\frac46=\frac{x}{7{,}5}\Rightarrow x=5\). d) Les altures també són proporcionals: \(\frac28=\frac{x}{12}\Rightarrow x=3\) cm.",
    r"a) \(\frac5{20}=\frac x{16}\Rightarrow x=4\). b) \(\frac46=\frac6x\Rightarrow x=9\). c) \(\frac46=\frac{x}{7{,}5}\Rightarrow x=5\). d) Las alturas también son proporcionales: \(\frac28=\frac{x}{12}\Rightarrow x=3\) cm.",
    r"a) \(\frac5{20}=\frac x{16}\Rightarrow x=4\). b) \(\frac46=\frac6x\Rightarrow x=9\). c) \(\frac46=\frac{x}{7.5}\Rightarrow x=5\). d) The heights are proportional too: \(\frac28=\frac{x}{12}\Rightarrow x=3\) cm."))
ck(R(5 * 16, 20), 4); ck(R(36, 4), 9); ck(R(4) * R(75, 10) / 6, 5); ck(R(2 * 12, 8), 3)
