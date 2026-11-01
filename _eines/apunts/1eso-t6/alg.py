# Apartats 6.1-6.4 (llenguatge algebraic, valor numèric, monomis i operacions) dels apunts de la Unitat 6 de 1r ESO.
from comu import *

def rows3(items):
    """files de taula trilingües: (va, es, en, tex)"""
    return [[L(va, es, en), r'\(' + t + r'\)'] for va, es, en, t in items]

# ============================================================ 6.1
TRAD = [
  ("Un nombre", "Un número", "A number", "x"),
  ("El doble d'un nombre", "El doble de un número", "Twice a number", "2x"),
  ("El triple d'un nombre", "El triple de un número", "Three times a number", "3x"),
  ("La meitat d'un nombre", "La mitad de un número", "Half a number", r"\frac{x}{2}"),
  ("La tercera part d'un nombre", "La tercera parte de un número", "A third of a number", r"\frac{x}{3}"),
  ("Un nombre més 5", "Un número más 5", "A number plus 5", "x+5"),
  ("Un nombre menys 4", "Un número menos 4", "A number minus 4", "x-4"),
  ("El quadrat d'un nombre", "El cuadrado de un número", "The square of a number", "x^2"),
  ("El següent d'un nombre (el consecutiu)", "El siguiente de un número (el consecutivo)", "The next number (the consecutive one)", "x+1"),
  ("L'anterior d'un nombre", "El anterior de un número", "The number before", "x-1"),
  ("Un nombre parell", "Un número par", "An even number", "2x"),
  ("Un nombre senar", "Un número impar", "An odd number", "2x+1"),
  ("El 10 % d'un nombre", "El 10 % de un número", "10% of a number", r"0\dc1x"),
  ("L'edat d'una persona d'ací a 5 anys", "La edad de una persona dentro de 5 años", "A person's age in 5 years' time", "x+5"),
  ("L'edat d'una persona fa 3 anys", "La edad de una persona hace 3 años", "A person's age 3 years ago", "x-3"),
]
s1 = box('def', L('Per a què servixen les lletres?', '¿Para qué sirven las letras?', 'What are letters for?'),
  P(r"El <strong>llenguatge algebraic</strong> utilitza <strong>nombres i lletres</strong> units pels signes de les operacions. Les lletres representen nombres que no coneixem o que poden prendre qualsevol valor. Servix per a:",
    r"El <strong>lenguaje algebraico</strong> utiliza <strong>números y letras</strong> unidos por los signos de las operaciones. Las letras representan números que no conocemos o que pueden tomar cualquier valor. Sirve para:",
    r"<strong>Algebraic language</strong> uses <strong>numbers and letters</strong> joined by operation signs. The letters stand for numbers we don't know or that can take any value. It's used to:")
  + ul(L(r"<strong>Expressar propietats generals.</strong> La propietat commutativa de la suma, \(a+b=b+a\), es compleix per a qualssevol nombres \(a\) i \(b\).",
         r"<strong>Expresar propiedades generales.</strong> La propiedad conmutativa de la suma, \(a+b=b+a\), se cumple para cualesquiera números \(a\) y \(b\).",
         r"<strong>Express general properties.</strong> The commutative property of addition, \(a+b=b+a\), holds for any numbers \(a\) and \(b\)."),
       L(r"<strong>Escriure fórmules.</strong> L'àrea d'un rectangle és \(A=b\cdot h\) i el perímetre d'un quadrat, \(P=4\cdot l\).",
         r"<strong>Escribir fórmulas.</strong> El área de un rectángulo es \(A=b\cdot h\) y el perímetro de un cuadrado, \(P=4\cdot l\).",
         r"<strong>Write formulas.</strong> The area of a rectangle is \(A=b\cdot h\) and the perimeter of a square is \(P=4\cdot l\)."),
       L(r"<strong>Traduir enunciats</strong> i resoldre problemes: «el doble d'un nombre més 3» s'escriu \(2x+3\).",
         r"<strong>Traducir enunciados</strong> y resolver problemas: «el doble de un número más 3» se escribe \(2x+3\).",
         r"<strong>Translate statements</strong> and solve problems: “twice a number plus 3” is written \(2x+3\)."))
  + note(r"En àlgebra <strong>no escrivim el punt de multiplicar</strong> entre un nombre i una lletra o entre dues lletres: \(3\cdot x\) s'escriu \(3x\) i \(a\cdot b\) s'escriu \(ab\). El nombre va sempre davant (\(x\cdot5=5x\)) i \(1x\) s'escriu simplement \(x\).",
         r"En álgebra <strong>no escribimos el punto de multiplicar</strong> entre un número y una letra o entre dos letras: \(3\cdot x\) se escribe \(3x\) y \(a\cdot b\) se escribe \(ab\). El número va siempre delante (\(x\cdot5=5x\)) y \(1x\) se escribe simplemente \(x\).",
         r"In algebra we <strong>leave out the multiplication dot</strong> between a number and a letter or between two letters: \(3\cdot x\) is written \(3x\) and \(a\cdot b\) is written \(ab\). The number always goes first (\(x\cdot5=5x\)) and \(1x\) is just \(x\)."))
s1 += box('ex', L('Del llenguatge habitual al llenguatge algebraic', 'Del lenguaje habitual al lenguaje algebraico', 'From everyday language to algebra'),
  table([L('Enunciat', 'Enunciado', 'Statement'), L('Expressió algebraica', 'Expresión algebraica', 'Algebraic expression')], rows3(TRAD), 'data trad')
  + note(r"<strong>L'ordre de les paraules importa!</strong> «El doble d'un nombre més 3» és \(2x+3\) (primer multipliquem), però «el doble de la suma d'un nombre i 3» és \(2(x+3)\): primer sumem i després multipliquem. Per això fem servir el parèntesi.",
         r"<strong>¡El orden de las palabras importa!</strong> «El doble de un número más 3» es \(2x+3\) (primero multiplicamos), pero «el doble de la suma de un número y 3» es \(2(x+3)\): primero sumamos y después multiplicamos. Por eso usamos el paréntesis.",
         r"<strong>Word order matters!</strong> “Twice a number plus 3” is \(2x+3\) (multiply first), but “twice the sum of a number and 3” is \(2(x+3)\): add first, then multiply. That's why we use brackets.", '⚠️')
  + drill('trad', 'Entrena: tradueix al llenguatge algebraic (fes servir la lletra x)', 'Entrena: traduce al lenguaje algebraico (usa la letra x)', 'Train: translate into algebra (use the letter x)', HELP_E))
s1 += box('prop', L('Generalitzar: la fórmula d\'una sèrie', 'Generalizar: la fórmula de una serie', 'Generalising: the formula of a pattern'),
  P(r"Amb escuradents fem una fila de quadrats. Per a 1 quadrat en necessitem 4; per a 2, 7; per a 3, 10… Cada quadrat nou n'afegix <strong>3</strong>: el primer quadrat en té un de més (el costat de l'esquerra) i després hi ha 3 per cada quadrat. Per a \(n\) quadrats:",
    r"Con palillos hacemos una fila de cuadrados. Para 1 cuadrado necesitamos 4; para 2, 7; para 3, 10… Cada cuadrado nuevo añade <strong>3</strong>: el primer cuadrado tiene uno de más (el lado de la izquierda) y después hay 3 por cada cuadrado. Para \(n\) cuadrados:",
    r"We use matchsticks to make a row of squares. 1 square needs 4; 2 squares, 7; 3 squares, 10… Each new square adds <strong>3</strong>: there's one extra stick (the left side) and then 3 for each square. For \(n\) squares:")
  + D(r"\text{%s}=3n+1\qquad n=10\ \Rightarrow\ 3\cdot10+1=31" % Lt('escuradents', 'palillos', 'matchsticks'))
  + P(r"La lletra \(n\) representa <em>qualsevol</em> nombre de quadrats: la fórmula funciona per a tots.", r"La letra \(n\) representa <em>cualquier</em> número de cuadrados: la fórmula funciona para todos.", r"The letter \(n\) stands for <em>any</em> number of squares: the formula works for all of them.")
  + widget('w-pat', '🧩', L('Sèries amb escuradents', 'Series con palillos', 'Matchstick patterns'),
           ['<div class="wrow">' + seg([('q', L('Quadrats', 'Cuadrados', 'Squares')), ('t', L('Triangles', 'Triángulos', 'Triangles')), ('h', L('Hexàgons', 'Hexágonos', 'Hexagons'))], 'q')
            + '<label>n = <input type="range" min="1" max="8" step="1" value="3" data-k="n"> <strong class="rv">3</strong></label></div>'],
           out='<div class="fvis pat"></div><div class="hsteps"></div>'))
chk('3*10+1', 31)
s1 += levels([
  prob(L(r"Expressa en llenguatge algebraic: a) el triple d'un nombre menys 7; b) la meitat d'un nombre més 1; c) un nombre més el seu doble; d) el quadrat d'un nombre menys 2.",
         r"Expresa en lenguaje algebraico: a) el triple de un número menos 7; b) la mitad de un número más 1; c) un número más su doble; d) el cuadrado de un número menos 2.",
         r"Write in algebra: a) three times a number minus 7; b) half a number plus 1; c) a number plus twice the number; d) the square of a number minus 2."),
       P(r"Anomenem \(x\) el nombre:", r"Llamamos \(x\) al número:", r"Call the number \(x\):"),
       D(r"\text{a) }\boxed{3x-7}\qquad \text{b) }\boxed{\frac{x}{2}+1}\qquad \text{c) }\boxed{x+2x}\qquad \text{d) }\boxed{x^2-2}"),
       note(r"En l'apartat 6.4 veurem que \(x+2x\) es pot escriure més curt: \(3x\).", r"En el apartado 6.4 veremos que \(x+2x\) se puede escribir más corto: \(3x\).", r"In section 6.4 we'll see that \(x+2x\) can be written more briefly: \(3x\)."))],
  [prob(L(r"La Marta té \(x\) anys. Expressa: a) l'edat del seu germà, que té 4 anys menys; b) l'edat de sa mare, que en té el triple; c) l'edat de la Marta d'ací a 10 anys; d) la suma de les edats de la Marta i el seu germà.",
          r"Marta tiene \(x\) años. Expresa: a) la edad de su hermano, que tiene 4 años menos; b) la edad de su madre, que tiene el triple; c) la edad de Marta dentro de 10 años; d) la suma de las edades de Marta y su hermano.",
          r"Marta is \(x\) years old. Write: a) the age of her brother, who is 4 years younger; b) the age of her mother, who is three times as old; c) Marta's age in 10 years' time; d) the sum of Marta's and her brother's ages."),
        D(r"\text{a) }\boxed{x-4}\qquad \text{b) }\boxed{3x}\qquad \text{c) }\boxed{x+10}\qquad \text{d) }\boxed{x+(x-4)}")),
   prob(L(r"Escriu una expressió per al perímetre i una altra per a l'àrea d'un rectangle de base \(x\) cm i altura 3 cm.",
          r"Escribe una expresión para el perímetro y otra para el área de un rectángulo de base \(x\) cm y altura 3 cm.",
          r"Write an expression for the perimeter and another for the area of a rectangle with base \(x\) cm and height 3 cm."),
        P(r"El perímetre és la suma dels quatre costats i l'àrea, base per altura:", r"El perímetro es la suma de los cuatro lados y el área, base por altura:", r"The perimeter is the sum of the four sides and the area is base times height:"),
        D(r"P=\boxed{x+3+x+3}\ \text{cm}\qquad A=x\cdot3=\boxed{3x}\ \text{cm}^2"))],
  [prob(L(r"Amb escuradents fem una fila de triangles: 1 triangle necessita 3 escuradents; 2 triangles, 5; 3 triangles, 7. Quants en calen per a \(n\) triangles? I per a 20 triangles?",
          r"Con palillos hacemos una fila de triángulos: 1 triángulo necesita 3 palillos; 2 triángulos, 5; 3 triángulos, 7. ¿Cuántos hacen falta para \(n\) triángulos? ¿Y para 20 triángulos?",
          r"We make a row of triangles with matchsticks: 1 triangle needs 3; 2 triangles, 5; 3 triangles, 7. How many are needed for \(n\) triangles? And for 20 triangles?"),
        P(r"Cada triangle nou afegix 2 escuradents; el primer en té un més:", r"Cada triángulo nuevo añade 2 palillos; el primero tiene uno más:", r"Each new triangle adds 2 matchsticks; the first one has one extra:"),
        D(r"3=2\cdot1+1,\quad 5=2\cdot2+1,\quad 7=2\cdot3+1\ \Rightarrow\ \boxed{2n+1}"),
        D(r"n=20:\ 2\cdot20+1=\boxed{41}\ \text{%s}" % Lt('escuradents', 'palillos', 'matchsticks'))),
   prob(L(r"Si \(x\) és el menor de tres nombres consecutius, expressa els altres dos i la seua suma. Fes el mateix amb tres nombres parells consecutius.",
          r"Si \(x\) es el menor de tres números consecutivos, expresa los otros dos y su suma. Haz lo mismo con tres números pares consecutivos.",
          r"If \(x\) is the smallest of three consecutive numbers, write the other two and their sum. Do the same with three consecutive even numbers."),
        D(r"x,\ x+1,\ x+2\qquad \text{%s: }\boxed{x+(x+1)+(x+2)}" % Lt('suma', 'suma', 'sum')),
        P(r"Els parells van de 2 en 2: si el menor és \(2x\), els següents són \(2x+2\) i \(2x+4\).", r"Los pares van de 2 en 2: si el menor es \(2x\), los siguientes son \(2x+2\) y \(2x+4\).", r"Even numbers go up in 2s: if the smallest is \(2x\), the next ones are \(2x+2\) and \(2x+4\).")
        + D(r"\boxed{2x+(2x+2)+(2x+4)}"))])
chk('2*20+1', 41)
s1 += practice([
  ('★', L(r"Tradueix: a) el quàdruple d'un nombre; b) un nombre menys 9; c) la cinquena part d'un nombre.", r"Traduce: a) el cuádruple de un número; b) un número menos 9; c) la quinta parte de un número.", r"Translate: a) four times a number; b) a number minus 9; c) a fifth of a number.")),
  ('★★', L(r"d) La suma de la meitat d'un nombre i 6. e) El triple de la diferència entre un nombre i 2. f) L'edat d'en Pau fa 7 anys, si ara en té \(x\).", r"d) La suma de la mitad de un número y 6. e) El triple de la diferencia entre un número y 2. f) La edad de Pau hace 7 años, si ahora tiene \(x\).", r"d) The sum of half a number and 6. e) Three times the difference between a number and 2. f) Pau's age 7 years ago, if he is \(x\) now.")),
  ('★★★', L(r"g) Amb escuradents fem una fila d'hexàgons: 1 hexàgon en necessita 6; 2 hexàgons, 11; 3 hexàgons, 16. Quina és la fórmula per a \(n\) hexàgons? Quants n'hi calen per a 10?", r"g) Con palillos hacemos una fila de hexágonos: 1 hexágono necesita 6; 2 hexágonos, 11; 3 hexágonos, 16. ¿Cuál es la fórmula para \(n\) hexágonos? ¿Cuántos hacen falta para 10?", r"g) We make a row of hexagons with matchsticks: 1 hexagon needs 6; 2 hexagons, 11; 3 hexagons, 16. What is the formula for \(n\) hexagons? How many are needed for 10?"))],
  P(r"a) \(4x\) &nbsp; b) \(x-9\) &nbsp; c) \(\frac{x}{5}\) &nbsp; d) \(\frac{x}{2}+6\) &nbsp; e) \(3(x-2)\) &nbsp; f) \(x-7\)", r"a) \(4x\) &nbsp; b) \(x-9\) &nbsp; c) \(\frac{x}{5}\) &nbsp; d) \(\frac{x}{2}+6\) &nbsp; e) \(3(x-2)\) &nbsp; f) \(x-7\)", r"a) \(4x\) &nbsp; b) \(x-9\) &nbsp; c) \(\frac{x}{5}\) &nbsp; d) \(\frac{x}{2}+6\) &nbsp; e) \(3(x-2)\) &nbsp; f) \(x-7\)")
  + P(r"g) Cada hexàgon nou n'afegix 5: \(5n+1\). Per a 10: \(5\cdot10+1=51\) escuradents.", r"g) Cada hexágono nuevo añade 5: \(5n+1\). Para 10: \(5\cdot10+1=51\) palillos.", r"g) Each new hexagon adds 5: \(5n+1\). For 10: \(5\cdot10+1=51\) matchsticks."))
for k, v in [(1, 6), (2, 11), (3, 16), (10, 51)]: cv('5n+1', {'n': k}, v)
for k, v in [(1, 3), (2, 5), (3, 7)]: cv('2n+1', {'n': k}, v)

# ============================================================ 6.2
s2 = box('def', L('Expressions algebraiques', 'Expresiones algebraicas', 'Algebraic expressions'),
  P(r"Una <strong>expressió algebraica</strong> és una combinació de nombres i lletres units pels signes de les operacions. Per exemple:",
    r"Una <strong>expresión algebraica</strong> es una combinación de números y letras unidos por los signos de las operaciones. Por ejemplo:",
    r"An <strong>algebraic expression</strong> is a combination of numbers and letters joined by operation signs. For example:")
  + D(r"2x+3\qquad ab\qquad x^2-5x+6\qquad \frac{x+1}{2}\qquad 3(a-b)")
  + P(r"Cada sumand d'una expressió és un <strong>terme</strong>: \(x^2-5x+6\) té tres termes, \(x^2\), \(-5x\) i \(6\). Les lletres s'anomenen <strong>variables</strong>.",
      r"Cada sumando de una expresión es un <strong>término</strong>: \(x^2-5x+6\) tiene tres términos, \(x^2\), \(-5x\) y \(6\). Las letras se llaman <strong>variables</strong>.",
      r"Each part being added is a <strong>term</strong>: \(x^2-5x+6\) has three terms, \(x^2\), \(-5x\) and \(6\). The letters are called <strong>variables</strong>."))
s2 += box('def', L('Valor numèric', 'Valor numérico', 'Evaluating an expression'),
  P(r"El <strong>valor numèric</strong> d'una expressió algebraica és el nombre que obtenim quan <strong>substituïm</strong> les lletres per nombres i fem les operacions, respectant la jerarquia: parèntesis, potències, multiplicacions i divisions i, per últim, sumes i restes.",
    r"El <strong>valor numérico</strong> de una expresión algebraica es el número que obtenemos cuando <strong>sustituimos</strong> las letras por números y hacemos las operaciones, respetando la jerarquía: paréntesis, potencias, multiplicaciones y divisiones y, por último, sumas y restas.",
    r"The <strong>value</strong> of an algebraic expression is the number we get when we <strong>substitute</strong> numbers for the letters and work it out, following the order of operations: brackets, powers, multiplication and division and, finally, addition and subtraction.")
  + D(r"3x-5\ \text{%s}\ x=4:\quad 3\cdot4-5=12-5=\boxed{7}" % Lt('per a', 'para', 'for'))
  + D(r"x^2+2x\ \text{%s}\ x=-3:\quad (-3)^2+2\cdot(-3)=9-6=\boxed{3}" % Lt('per a', 'para', 'for'))
  + D(r"2a-b\ \text{%s}\ a=5,\ b=-2:\quad 2\cdot5-(-2)=10+2=\boxed{12}" % Lt('per a', 'para', 'for'))
  + note(r"Quan substituïm per un nombre <strong>negatiu</strong>, el posem sempre <strong>entre parèntesis</strong>: \((-3)^2=9\), però \(-3^2=-9\). I recorda que entre el nombre i la lletra hi ha una multiplicació: si \(x=4\), \(3x=3\cdot4\), no 34!",
         r"Cuando sustituimos por un número <strong>negativo</strong>, lo ponemos siempre <strong>entre paréntesis</strong>: \((-3)^2=9\), pero \(-3^2=-9\). Y recuerda que entre el número y la letra hay una multiplicación: si \(x=4\), \(3x=3\cdot4\), ¡no 34!",
         r"When we substitute a <strong>negative</strong> number, we always put it <strong>in brackets</strong>: \((-3)^2=9\), but \(-3^2=-9\). And remember there's a multiplication between the number and the letter: if \(x=4\), \(3x=3\cdot4\), not 34!", '⚠️')
  + widget('w-val', '🔢', L('Calcula el valor numèric', 'Calcula el valor numérico', 'Evaluate an expression'),
           ['<div class="wrow">' + tin('e', L('Expressió', 'Expresión', 'Expression'), 'x^2+2x') + tin('v', L('Valors', 'Valores', 'Values'), 'x=-3') + '</div>',
            hint_s("Escriu els valors així: x=-3. Si hi ha dues lletres, separa'ls amb punt i coma: a=5; b=-2.", "Escribe los valores así: x=-3. Si hay dos letras, sepáralos con punto y coma: a=5; b=-2.", "Type the values like this: x=-3. With two letters, separate them with a semicolon: a=5; b=-2."),
            quick([('3x-5|x=4', '3x − 5, x = 4'), ('x^2+2x|x=-3', 'x² + 2x, x = −3'), ('2a-b|a=5; b=-2', '2a − b'), ('(x+1)/2|x=7', '(x+1)/2'), ('3+1.2k|k=10', '3 + 1,2k'), ('b*h/2|b=8; h=5', 'b·h/2')])],
           out='<div class="hsteps"></div><div class="vtab"></div>')
  + drill('val', 'Entrena: calcula el valor numèric', 'Entrena: calcula el valor numérico', 'Train: evaluate the expression'))
cv('3x-5', {'x': 4}, 7); cv('x^2+2x', {'x': -3}, 3); cv('2a-b', {'a': 5, 'b': -2}, 12)
s2 += levels([
  prob(L(r"Calcula el valor numèric de \(5x-2\) per a \(x=3\), \(x=0\) i \(x=-1\).", r"Calcula el valor numérico de \(5x-2\) para \(x=3\), \(x=0\) y \(x=-1\).", r"Evaluate \(5x-2\) for \(x=3\), \(x=0\) and \(x=-1\)."),
       D(r"x=3:\ 5\cdot3-2=\boxed{13}\qquad x=0:\ 5\cdot0-2=\boxed{-2}\qquad x=-1:\ 5\cdot(-1)-2=\boxed{-7}"))],
  [prob(L(r"Calcula el valor numèric de \(x^2-3x+1\) per a \(x=2\) i per a \(x=-2\).", r"Calcula el valor numérico de \(x^2-3x+1\) para \(x=2\) y para \(x=-2\).", r"Evaluate \(x^2-3x+1\) for \(x=2\) and for \(x=-2\)."),
        D(r"x=2:\ 2^2-3\cdot2+1=4-6+1=\boxed{-1}"),
        D(r"x=-2:\ (-2)^2-3\cdot(-2)+1=4+6+1=\boxed{11}")),
   prob(L(r"Un taxi cobra 3 € per pujar-hi i \(1\dc20\) € per quilòmetre. Escriu l'expressió del preu d'un viatge de \(k\) km i calcula quant costa un viatge de 5 km i un altre de 12 km.",
          r"Un taxi cobra 3 € por subir y \(1\dc20\) € por kilómetro. Escribe la expresión del precio de un viaje de \(k\) km y calcula cuánto cuesta un viaje de 5 km y otro de 12 km.",
          r"A taxi charges 3 € to get in and \(1\dc20\) € per kilometre. Write the expression for the price of a \(k\) km trip and work out the cost of a 5 km trip and a 12 km trip."),
        D(r"P=3+1\dc2k"),
        D(r"k=5:\ 3+1\dc2\cdot5=3+6=\boxed{9\ €}\qquad k=12:\ 3+1\dc2\cdot12=3+14\dc4=\boxed{17\dc40\ €}"))],
  [prob(L(r"Observa la taula. Quina expressió dona \(y\) a partir de \(x\)? Quant val \(y\) per a \(x=10\)?", r"Observa la tabla. ¿Qué expresión da \(y\) a partir de \(x\)? ¿Cuánto vale \(y\) para \(x=10\)?", r"Look at the table. Which expression gives \(y\) from \(x\)? What is \(y\) when \(x=10\)?")
        + table(['\\(x\\)', '1', '2', '3', '4'], [['\\(y\\)', '7', '10', '13', '16']], 'data ptab'),
        P(r"Cada vegada que \(x\) augmenta 1, \(y\) augmenta 3: l'expressió comença per \(3x\). Per a \(x=1\), \(3\cdot1=3\) i en volem 7: hem de sumar 4.", r"Cada vez que \(x\) aumenta 1, \(y\) aumenta 3: la expresión empieza por \(3x\). Para \(x=1\), \(3\cdot1=3\) y queremos 7: hay que sumar 4.", r"Each time \(x\) goes up by 1, \(y\) goes up by 3: the expression starts with \(3x\). For \(x=1\), \(3\cdot1=3\) but we want 7: we must add 4."),
        D(r"y=\boxed{3x+4}\qquad \text{%s: } 3\cdot4+4=16\ \checkmark\qquad x=10:\ 3\cdot10+4=\boxed{34}" % Lt('comprovem', 'comprobamos', 'check')))])
cv('5x-2', {'x': 3}, 13); cv('5x-2', {'x': 0}, -2); cv('5x-2', {'x': -1}, -7)
cv('x^2-3x+1', {'x': 2}, -1); cv('x^2-3x+1', {'x': -2}, 11)
cv('3+6/5*k', {'k': 5}, 9); cv('3+6/5*k', {'k': 12}, sp.Rational(87, 5))
for k, v in [(1, 7), (2, 10), (3, 13), (4, 16), (10, 34)]: cv('3x+4', {'x': k}, v)
s2 += practice([
  ('★', L(r"Calcula el valor numèric: a) \(4x+1\) per a \(x=-2\); b) \(10-3a\) per a \(a=4\).", r"Calcula el valor numérico: a) \(4x+1\) para \(x=-2\); b) \(10-3a\) para \(a=4\).", r"Evaluate: a) \(4x+1\) for \(x=-2\); b) \(10-3a\) for \(a=4\).")),
  ('★★', L(r"c) \(x^2-x\) per a \(x=-3\). d) \(2a+3b\) per a \(a=-1\), \(b=4\). e) \(\frac{x+5}{3}\) per a \(x=7\).", r"c) \(x^2-x\) para \(x=-3\). d) \(2a+3b\) para \(a=-1\), \(b=4\). e) \(\frac{x+5}{3}\) para \(x=7\).", r"c) \(x^2-x\) for \(x=-3\). d) \(2a+3b\) for \(a=-1\), \(b=4\). e) \(\frac{x+5}{3}\) for \(x=7\).")),
  ('★★★', L(r"f) El perímetre d'un rectangle és \(P=2b+2h\). Calcula'l si \(b=7\dc5\) cm i \(h=4\) cm. g) Busca un valor de \(x\) que faça que \(2x+1\) i \(x+5\) tinguen el mateix valor numèric.", r"f) El perímetro de un rectángulo es \(P=2b+2h\). Calcúlalo si \(b=7\dc5\) cm y \(h=4\) cm. g) Busca un valor de \(x\) que haga que \(2x+1\) y \(x+5\) tengan el mismo valor numérico.", r"f) The perimeter of a rectangle is \(P=2b+2h\). Work it out if \(b=7\dc5\) cm and \(h=4\) cm. g) Find a value of \(x\) that makes \(2x+1\) and \(x+5\) have the same value."))],
  P(r"a) \(4\cdot(-2)+1=-7\) &nbsp; b) \(10-3\cdot4=-2\) &nbsp; c) \((-3)^2-(-3)=9+3=12\) &nbsp; d) \(2\cdot(-1)+3\cdot4=10\) &nbsp; e) \(\frac{7+5}{3}=4\)", r"a) \(4\cdot(-2)+1=-7\) &nbsp; b) \(10-3\cdot4=-2\) &nbsp; c) \((-3)^2-(-3)=9+3=12\) &nbsp; d) \(2\cdot(-1)+3\cdot4=10\) &nbsp; e) \(\frac{7+5}{3}=4\)", r"a) \(4\cdot(-2)+1=-7\) &nbsp; b) \(10-3\cdot4=-2\) &nbsp; c) \((-3)^2-(-3)=9+3=12\) &nbsp; d) \(2\cdot(-1)+3\cdot4=10\) &nbsp; e) \(\frac{7+5}{3}=4\)")
  + P(r"f) \(2\cdot7\dc5+2\cdot4=15+8=23\) cm. &nbsp; g) Provant: per a \(x=4\), \(2\cdot4+1=9\) i \(4+5=9\). (En l'apartat 6.6 aprendrem a trobar-lo sense provar.)", r"f) \(2\cdot7\dc5+2\cdot4=15+8=23\) cm. &nbsp; g) Probando: para \(x=4\), \(2\cdot4+1=9\) y \(4+5=9\). (En el apartado 6.6 aprenderemos a encontrarlo sin probar.)", r"f) \(2\cdot7\dc5+2\cdot4=15+8=23\) cm. &nbsp; g) By trial: for \(x=4\), \(2\cdot4+1=9\) and \(4+5=9\). (In section 6.6 we'll learn to find it without guessing.)"))
cv('4x+1', {'x': -2}, -7); cv('10-3a', {'a': 4}, -2); cv('x^2-x', {'x': -3}, 12); cv('2a+3b', {'a': -1, 'b': 4}, 10); cv('(x+5)/3', {'x': 7}, 4)
cv('2b+2h', {'b': sp.Rational(15, 2), 'h': 4}, 23); ce('2x+1=x+5', 4)

# ============================================================ 6.3
MONOS = [('7x', '7', 'x', '1'), ('-3a^2b', '-3', 'a^2b', '3'), ('x^3', '1', 'x^3', '3'), ('-y', '-1', 'y', '1'), (r'\frac{2}{3}xy', r'\frac{2}{3}', 'xy', '2'), ('8', '8', '—', '0')]
s3 = box('def', L('Monomis', 'Monomios', 'Monomials'),
  P(r"Un <strong>monomi</strong> és una expressió algebraica formada pel <strong>producte</strong> d'un nombre i una o més lletres, que poden estar elevades a exponents naturals. En un monomi distingim:",
    r"Un <strong>monomio</strong> es una expresión algebraica formada por el <strong>producto</strong> de un número y una o más letras, que pueden estar elevadas a exponentes naturales. En un monomio distinguimos:",
    r"A <strong>monomial</strong> is an algebraic expression made of the <strong>product</strong> of a number and one or more letters, which may be raised to whole-number powers. In a monomial we identify:")
  + D(r"\underbrace{-5}_{\text{%s}}\ \underbrace{x^2y}_{\text{%s}}\qquad \text{%s}=2+1=3" % (Lt('coeficient', 'coeficiente', 'coefficient'), Lt('part literal', 'parte literal', 'literal part'), Lt('grau', 'grado', 'degree')))
  + ul(L(r"El <strong>coeficient</strong>: el nombre que multiplica (amb el seu signe).", r"El <strong>coeficiente</strong>: el número que multiplica (con su signo).", r"The <strong>coefficient</strong>: the number multiplying (with its sign)."),
       L(r"La <strong>part literal</strong>: les lletres amb els seus exponents.", r"La <strong>parte literal</strong>: las letras con sus exponentes.", r"The <strong>literal part</strong>: the letters with their exponents."),
       L(r"El <strong>grau</strong>: la suma dels exponents de totes les lletres.", r"El <strong>grado</strong>: la suma de los exponentes de todas las letras.", r"The <strong>degree</strong>: the sum of the exponents of all the letters."))
  + table([L('Monomi', 'Monomio', 'Monomial'), L('Coeficient', 'Coeficiente', 'Coefficient'), L('Part literal', 'Parte literal', 'Literal part'), L('Grau', 'Grado', 'Degree')],
          [[r'\(%s\)' % m, r'\(%s\)' % c, r'\(%s\)' % p if p != '—' else p, g] for m, c, p, g in MONOS], 'data ptab')
  + note(r"Quan el coeficient és 1 no s'escriu (\(x^3\)) i quan és \(-1\) només posem el signe (\(-y\)). Una lletra sense exponent té exponent 1 (\(x=x^1\)). Un nombre sol, com \(8\), és un monomi de <strong>grau 0</strong>.",
         r"Cuando el coeficiente es 1 no se escribe (\(x^3\)) y cuando es \(-1\) solo ponemos el signo (\(-y\)). Una letra sin exponente tiene exponente 1 (\(x=x^1\)). Un número solo, como \(8\), es un monomio de <strong>grado 0</strong>.",
         r"When the coefficient is 1 we don't write it (\(x^3\)) and when it's \(-1\) we only write the sign (\(-y\)). A letter with no exponent has exponent 1 (\(x=x^1\)). A number on its own, like \(8\), is a monomial of <strong>degree 0</strong>.")
  + note(r"<strong>No són monomis</strong>: \(x+3\) (és una suma), \(\frac{5}{x}\) (la lletra està dividint) ni \(2^x\) (la lletra és a l'exponent).",
         r"<strong>No son monomios</strong>: \(x+3\) (es una suma), \(\frac{5}{x}\) (la letra está dividiendo) ni \(2^x\) (la letra está en el exponente).",
         r"<strong>These are not monomials</strong>: \(x+3\) (it's a sum), \(\frac{5}{x}\) (the letter is dividing) or \(2^x\) (the letter is in the exponent).", '⚠️'))
s3 += box('def', L('Monomis semblants', 'Monomios semejantes', 'Like terms'),
  P(r"Dos monomis són <strong>semblants</strong> si tenen la <strong>mateixa part literal</strong> (les mateixes lletres amb els mateixos exponents). Només poden canviar els coeficients.",
    r"Dos monomios son <strong>semejantes</strong> si tienen la <strong>misma parte literal</strong> (las mismas letras con los mismos exponentes). Solo pueden cambiar los coeficientes.",
    r"Two monomials are <strong>like terms</strong> if they have the <strong>same literal part</strong> (the same letters with the same exponents). Only the coefficients can differ.")
  + D(r"3x^2\ \text{%s}\ -5x^2\ \checkmark\qquad 4ab\ \text{%s}\ ab\ \checkmark\qquad 3x^2\ \text{%s}\ 3x\ \times\qquad 2xy^2\ \text{%s}\ 2x^2y\ \times" % ((Lt('i', 'y', 'and'),) * 4)))
s3 += box('def', L('Polinomis', 'Polinomios', 'Polynomials'),
  P(r"Un <strong>polinomi</strong> és una suma de monomis no semblants. Cada monomi és un <strong>terme</strong> del polinomi; el que no té lletra és el <strong>terme independent</strong>. Si té dos termes és un <strong>binomi</strong> i, si en té tres, un <strong>trinomi</strong>. El <strong>grau</strong> d'un polinomi és el grau del seu terme de grau més alt.",
    r"Un <strong>polinomio</strong> es una suma de monomios no semejantes. Cada monomio es un <strong>término</strong> del polinomio; el que no tiene letra es el <strong>término independiente</strong>. Si tiene dos términos es un <strong>binomio</strong> y, si tiene tres, un <strong>trinomio</strong>. El <strong>grado</strong> de un polinomio es el grado de su término de mayor grado.",
    r"A <strong>polynomial</strong> is a sum of unlike monomials. Each monomial is a <strong>term</strong>; the one without a letter is the <strong>constant term</strong>. With two terms it's a <strong>binomial</strong> and with three, a <strong>trinomial</strong>. The <strong>degree</strong> of a polynomial is the degree of its highest-degree term.")
  + D(r"x^2-5x+6:\ \text{%s}" % Lt('trinomi de grau 2, terme independent 6', 'trinomio de grado 2, término independiente 6', 'trinomial of degree 2, constant term 6'))
  + widget('w-mono', '🔎', L('Analitza un monomi o un polinomi', 'Analiza un monomio o un polinomio', 'Analyse a monomial or polynomial'),
           ['<div class="wrow">' + tin('e', L('Expressió', 'Expresión', 'Expression'), '-5x^2y') + '</div>',
            quick([('-5x^2y', '−5x²y'), ('7x', '7x'), ('-y', '−y'), ('2/3xy', '⅔xy'), ('8', '8'), ('x^2-5x+6', 'x² − 5x + 6'), ('3x+2x', '3x + 2x'), ('5/x', '5/x')])])
  + drill('mono', 'Entrena: coeficient i grau', 'Entrena: coeficiente y grado', 'Train: coefficient and degree'))
s3 += levels([
  prob(L(r"Indica el coeficient, la part literal i el grau de: a) \(9x^2\) &nbsp; b) \(-ab\) &nbsp; c) \(4xy^3\) &nbsp; d) \(-\frac{x}{2}\)", r"Indica el coeficiente, la parte literal y el grado de: a) \(9x^2\) &nbsp; b) \(-ab\) &nbsp; c) \(4xy^3\) &nbsp; d) \(-\frac{x}{2}\)", r"Give the coefficient, literal part and degree of: a) \(9x^2\) &nbsp; b) \(-ab\) &nbsp; c) \(4xy^3\) &nbsp; d) \(-\frac{x}{2}\)"),
       table([L('Monomi', 'Monomio', 'Monomial'), L('Coeficient', 'Coeficiente', 'Coefficient'), L('Part literal', 'Parte literal', 'Literal part'), L('Grau', 'Grado', 'Degree')],
             [[r'\(9x^2\)', r'\(\boxed{9}\)', r'\(\boxed{x^2}\)', r'\(\boxed{2}\)'], [r'\(-ab\)', r'\(\boxed{-1}\)', r'\(\boxed{ab}\)', r'\(\boxed{2}\)'], [r'\(4xy^3\)', r'\(\boxed{4}\)', r'\(\boxed{xy^3}\)', r'\(\boxed{4}\)'], [r'\(-\frac{x}{2}\)', r'\(\boxed{-\frac{1}{2}}\)', r'\(\boxed{x}\)', r'\(\boxed{1}\)']], 'data ptab'),
       note(r"\(-\frac{x}{2}\) és un monomi: és el mateix que \(-\frac{1}{2}x\). La lletra està multiplicada per \(-\frac{1}{2}\), no dividint.", r"\(-\frac{x}{2}\) es un monomio: es lo mismo que \(-\frac{1}{2}x\). La letra está multiplicada por \(-\frac{1}{2}\), no dividiendo.", r"\(-\frac{x}{2}\) is a monomial: it's the same as \(-\frac{1}{2}x\). The letter is multiplied by \(-\frac{1}{2}\), not dividing."))],
  [prob(L(r"Agrupa els monomis semblants: \(\ 3x,\ -2x^2,\ 5,\ x,\ 7x^2,\ -4,\ \frac{1}{2}x\)", r"Agrupa los monomios semejantes: \(\ 3x,\ -2x^2,\ 5,\ x,\ 7x^2,\ -4,\ \frac{1}{2}x\)", r"Group the like terms: \(\ 3x,\ -2x^2,\ 5,\ x,\ 7x^2,\ -4,\ \frac{1}{2}x\)"),
        D(r"\text{%s } x:\ \boxed{3x,\ x,\ \tfrac{1}{2}x}\qquad \text{%s } x^2:\ \boxed{-2x^2,\ 7x^2}\qquad \text{%s}:\ \boxed{5,\ -4}" % (Lt('amb', 'con', 'with'), Lt('amb', 'con', 'with'), Lt('sense lletra', 'sin letra', 'no letter')))),
   prob(L(r"Digues el nombre de termes, el grau i el terme independent de: a) \(4x^3-x+2\) &nbsp; b) \(6-x^2\) &nbsp; c) \(2x+5x^2-3x^4\)", r"Di el número de términos, el grado y el término independiente de: a) \(4x^3-x+2\) &nbsp; b) \(6-x^2\) &nbsp; c) \(2x+5x^2-3x^4\)", r"Give the number of terms, the degree and the constant term of: a) \(4x^3-x+2\) &nbsp; b) \(6-x^2\) &nbsp; c) \(2x+5x^2-3x^4\)"),
        P(r"a) Trinomi de grau \(\boxed{3}\), terme independent \(\boxed{2}\). &nbsp; b) Binomi de grau \(\boxed{2}\), terme independent \(\boxed{6}\). &nbsp; c) Trinomi de grau \(\boxed{4}\) (el terme de grau més alt és \(-3x^4\), encara que no estiga el primer); no té terme independent (és 0).",
          r"a) Trinomio de grado \(\boxed{3}\), término independiente \(\boxed{2}\). &nbsp; b) Binomio de grado \(\boxed{2}\), término independiente \(\boxed{6}\). &nbsp; c) Trinomio de grado \(\boxed{4}\) (el término de mayor grado es \(-3x^4\), aunque no esté el primero); no tiene término independiente (es 0).",
          r"a) Trinomial of degree \(\boxed{3}\), constant term \(\boxed{2}\). &nbsp; b) Binomial of degree \(\boxed{2}\), constant term \(\boxed{6}\). &nbsp; c) Trinomial of degree \(\boxed{4}\) (the highest-degree term is \(-3x^4\), even though it isn't first); no constant term (it's 0)."))],
  [prob(L(r"Escriu: a) un monomi de grau 4, amb coeficient \(-3\) i dues lletres; b) un monomi semblant a \(-6a^2b\) amb coeficient 2; c) un trinomi de grau 3 amb terme independent 5.", r"Escribe: a) un monomio de grado 4, con coeficiente \(-3\) y dos letras; b) un monomio semejante a \(-6a^2b\) con coeficiente 2; c) un trinomio de grado 3 con término independiente 5.", r"Write: a) a monomial of degree 4 with coefficient \(-3\) and two letters; b) a like term of \(-6a^2b\) with coefficient 2; c) a trinomial of degree 3 with constant term 5."),
        P(r"Hi ha moltes respostes possibles. Per exemple:", r"Hay muchas respuestas posibles. Por ejemplo:", r"There are many possible answers. For example:"),
        D(r"\text{a) }\boxed{-3x^3y}\ \ (3+1=4)\qquad \text{b) }\boxed{2a^2b}\qquad \text{c) }\boxed{x^3-2x+5}"))])
s3 += practice([
  ('★', L(r"a) Quin és el coeficient i el grau de \(-8x^5\)? b) I de \(xy\)?", r"a) ¿Cuál es el coeficiente y el grado de \(-8x^5\)? b) ¿Y de \(xy\)?", r"a) What are the coefficient and degree of \(-8x^5\)? b) And of \(xy\)?")),
  ('★★', L(r"c) Són semblants \(5ab^2\) i \(-ab^2\)? I \(3x^2y\) i \(3xy^2\)? d) Quin grau té el polinomi \(7-2x+x^3\)?", r"c) ¿Son semejantes \(5ab^2\) y \(-ab^2\)? ¿Y \(3x^2y\) y \(3xy^2\)? d) ¿Qué grado tiene el polinomio \(7-2x+x^3\)?", r"c) Are \(5ab^2\) and \(-ab^2\) like terms? What about \(3x^2y\) and \(3xy^2\)? d) What is the degree of \(7-2x+x^3\)?")),
  ('★★★', L(r"e) Escriu tres monomis semblants entre ells, de grau 3, la suma dels coeficients dels quals siga 0.", r"e) Escribe tres monomios semejantes entre ellos, de grado 3, cuyos coeficientes sumen 0.", r"e) Write three like monomials of degree 3 whose coefficients add up to 0."))],
  P(r"a) Coeficient \(-8\), grau 5. &nbsp; b) Coeficient 1, grau 2. &nbsp; c) Sí (part literal \(ab^2\)); no (\(x^2y\neq xy^2\)). &nbsp; d) Grau 3. &nbsp; e) Per exemple, \(2x^3,\ 3x^3,\ -5x^3\).", r"a) Coeficiente \(-8\), grado 5. &nbsp; b) Coeficiente 1, grado 2. &nbsp; c) Sí (parte literal \(ab^2\)); no (\(x^2y\neq xy^2\)). &nbsp; d) Grado 3. &nbsp; e) Por ejemplo, \(2x^3,\ 3x^3,\ -5x^3\).", r"a) Coefficient \(-8\), degree 5. &nbsp; b) Coefficient 1, degree 2. &nbsp; c) Yes (literal part \(ab^2\)); no (\(x^2y\neq xy^2\)). &nbsp; d) Degree 3. &nbsp; e) For example, \(2x^3,\ 3x^3,\ -5x^3\)."))
chk('2x^3+3x^3-5x^3', 0)

# ============================================================ 6.4
s4 = box('prop', L('Suma i resta de monomis', 'Suma y resta de monomios', 'Adding and subtracting monomials'),
  P(r"Només es poden sumar o restar monomis <strong>semblants</strong>: sumem (o restem) els <strong>coeficients</strong> i deixem la mateixa part literal.",
    r"Solo se pueden sumar o restar monomios <strong>semejantes</strong>: sumamos (o restamos) los <strong>coeficientes</strong> y dejamos la misma parte literal.",
    r"Only <strong>like terms</strong> can be added or subtracted: add (or subtract) the <strong>coefficients</strong> and keep the same literal part.")
  + D(r"3x+5x=8x\qquad 7a^2-2a^2=5a^2\qquad 4x-x=3x\qquad x-6x=-5x")
  + P(r"És com comptar objectes: 3 pomes més 5 pomes són 8 pomes. Però 3 pomes més 2 peres no són «5 pomeres»: si els monomis no són semblants, la suma es deixa indicada. Per exemple, \(4x+3\) no es pot escriure més curt.",
      r"Es como contar objetos: 3 manzanas más 5 manzanas son 8 manzanas. Pero 3 manzanas más 2 peras no son «5 manzaperas»: si los monomios no son semejantes, la suma se deja indicada. Por ejemplo, \(4x+3\) no se puede escribir más corto.",
      r"It's like counting objects: 3 apples plus 5 apples make 8 apples. But 3 apples plus 2 pears aren't “5 applepears”: if the terms aren't alike, the sum is left as it is. For example, \(4x+3\) can't be written any shorter.")
  + note(r"Error molt freqüent: \(3x+2=5x\) <strong>és fals</strong>! Prova-ho amb \(x=10\): \(3\cdot10+2=32\), però \(5\cdot10=50\).", r"Error muy frecuente: ¡\(3x+2=5x\) <strong>es falso</strong>! Pruébalo con \(x=10\): \(3\cdot10+2=32\), pero \(5\cdot10=50\).", r"A very common mistake: \(3x+2=5x\) <strong>is false</strong>! Try it with \(x=10\): \(3\cdot10+2=32\), but \(5\cdot10=50\).", '⚠️'))
s4 += box('prop', L('Reduir una expressió', 'Reducir una expresión', 'Simplifying an expression'),
  P(r"<strong>Reduir</strong> una expressió és agrupar els termes semblants fins que no en quede cap de repetit:", r"<strong>Reducir</strong> una expresión es agrupar los términos semejantes hasta que no quede ninguno repetido:", r"To <strong>simplify</strong> (collect like terms) means grouping like terms until none is repeated:")
  + D(r"5x+3-2x+4=(5x-2x)+(3+4)=\boxed{3x+7}")
  + D(r"2x^2+3x-x^2+5-7x=(2x^2-x^2)+(3x-7x)+5=\boxed{x^2-4x+5}")
  + P(r"Amb les <strong>fitxes algebraiques</strong> ho veiem molt bé: una barra és una \(x\), un quadradet és una unitat i les fitxes roges són negatives. Una fitxa positiva i una de negativa iguals s'anul·len (sumen 0).",
      r"Con las <strong>fichas algebraicas</strong> lo vemos muy bien: una barra es una \(x\), un cuadradito es una unidad y las fichas rojas son negativas. Una ficha positiva y una negativa iguales se anulan (suman 0).",
      r"<strong>Algebra tiles</strong> make it very clear: a bar is an \(x\), a small square is a unit and red tiles are negative. A positive and a negative tile of the same kind cancel out (they add up to 0).")
  + widget('w-tiles', '🧱', L('Fitxes algebraiques', 'Fichas algebraicas', 'Algebra tiles'),
           ['<div class="wrow">' + tin('e', L('Expressió', 'Expresión', 'Expression'), '5x+3-2x+4') + '</div>', HELP_E,
            quick([('5x+3-2x+4', '5x + 3 − 2x + 4'), ('x+6-3x-2', 'x + 6 − 3x − 2'), ('2x^2+3x-x^2-x+1', '2x² + 3x − x² − x + 1'), ('4-x+x-4', '4 − x + x − 4'), ('2(x+3)-x', '2(x+3) − x')])],
           out='<div class="fvis tiles"></div><div class="hsteps"></div>')
  + drill('red', 'Entrena: redueix l\'expressió', 'Entrena: reduce la expresión', 'Train: simplify the expression', HELP_E))
chk('5x+3-2x+4', '3x+7'); chk('2x^2+3x-x^2+5-7x', 'x^2-4x+5')
s4 += box('prop', L('Producte de monomis', 'Producto de monomios', 'Multiplying monomials'),
  P(r"Per a multiplicar monomis (encara que no siguen semblants), multipliquem els <strong>coeficients</strong> entre ells i les <strong>parts literals</strong> entre elles. Recorda que, en multiplicar potències de la mateixa base, se <strong>sumen els exponents</strong>: \(x\cdot x=x^2\), \(x^2\cdot x=x^3\).",
    r"Para multiplicar monomios (aunque no sean semejantes), multiplicamos los <strong>coeficientes</strong> entre sí y las <strong>partes literales</strong> entre sí. Recuerda que, al multiplicar potencias de la misma base, se <strong>suman los exponentes</strong>: \(x\cdot x=x^2\), \(x^2\cdot x=x^3\).",
    r"To multiply monomials (even unlike ones), multiply the <strong>coefficients</strong> together and the <strong>literal parts</strong> together. Remember that when multiplying powers with the same base we <strong>add the exponents</strong>: \(x\cdot x=x^2\), \(x^2\cdot x=x^3\).")
  + D(r"3x\cdot4x=12x^2\qquad (-2a)\cdot5b=-10ab\qquad 2x^2\cdot(-3x)=-6x^3\qquad 4\cdot(-5x)=-20x")
  + note(r"No confongues la suma amb el producte: \(x+x=2x\), però \(x\cdot x=x^2\).", r"No confundas la suma con el producto: \(x+x=2x\), pero \(x\cdot x=x^2\).", r"Don't mix up adding and multiplying: \(x+x=2x\), but \(x\cdot x=x^2\).", '⚠️'))
s4 += box('prop', L('Propietat distributiva: traure parèntesis', 'Propiedad distributiva: quitar paréntesis', 'The distributive property: removing brackets'),
  P(r"Per a multiplicar un nombre (o un monomi) per una suma, el multipliquem per <strong>cada terme</strong> del parèntesi:", r"Para multiplicar un número (o un monomio) por una suma, lo multiplicamos por <strong>cada término</strong> del paréntesis:", r"To multiply a number (or monomial) by a sum, multiply it by <strong>each term</strong> in the brackets:")
  + D(r"a(b+c)=ab+ac")
  + D(r"3(x+2)=3x+6\qquad -2(x-4)=-2x+8\qquad 5(2x-1)=10x-5\qquad x(x+3)=x^2+3x")
  + P(r"Un <strong>signe menys</strong> davant d'un parèntesi canvia el signe de <strong>tots</strong> els termes de dins: \(-(x-5)=-x+5\). Després de traure parèntesis, reduïm:",
      r"Un <strong>signo menos</strong> delante de un paréntesis cambia el signo de <strong>todos</strong> los términos de dentro: \(-(x-5)=-x+5\). Después de quitar paréntesis, reducimos:",
      r"A <strong>minus sign</strong> in front of brackets changes the sign of <strong>every</strong> term inside: \(-(x-5)=-x+5\). After removing brackets, simplify:")
  + D(r"3(x+2)-2(x-1)=3x+6-2x+2=\boxed{x+8}")
  + note(r"Compte amb els signes: \(-2(x-1)=-2x+2\), perquè \((-2)\cdot(-1)=+2\). I no oblides multiplicar el <strong>segon</strong> terme: \(3(x+2)\neq3x+2\).", r"Cuidado con los signos: \(-2(x-1)=-2x+2\), porque \((-2)\cdot(-1)=+2\). Y no olvides multiplicar el <strong>segundo</strong> término: \(3(x+2)\neq3x+2\).", r"Watch the signs: \(-2(x-1)=-2x+2\), because \((-2)\cdot(-1)=+2\). And don't forget to multiply the <strong>second</strong> term: \(3(x+2)\neq3x+2\).", '⚠️')
  + widget('w-red', '🧹', L('Redueix pas a pas', 'Reduce paso a paso', 'Simplify step by step'),
           ['<div class="wrow">' + tin('e', L('Expressió', 'Expresión', 'Expression'), '3(x+2)-2(x-1)') + '</div>', HELP_E,
            quick([('3(x+2)-2(x-1)', '3(x+2) − 2(x−1)'), ('5x-(2x-7)', '5x − (2x−7)'), ('4(2x-1)-3(x+2)+x', '4(2x−1) − 3(x+2) + x'), ('3x*4x-x^2', '3x·4x − x²'), ('x(x+3)-2x', 'x(x+3) − 2x'), ('2(a+b)-(a-b)', '2(a+b) − (a−b)')])])
  + drill('mul', 'Entrena: multiplica i redueix', 'Entrena: multiplica y reduce', 'Train: multiply and simplify', HELP_E))
for l, r in [('3x*4x', '12x^2'), ('(-2a)*5b', '-10ab'), ('2x^2*(-3x)', '-6x^3'), ('4*(-5x)', '-20x'), ('3(x+2)', '3x+6'), ('-2(x-4)', '-2x+8'), ('5(2x-1)', '10x-5'), ('x(x+3)', 'x^2+3x'), ('-(x-5)', '-x+5'), ('3(x+2)-2(x-1)', 'x+8')]: chk(l, r)
s4 += levels([
  prob(L(r"Redueix: a) \(6x+2x\) &nbsp; b) \(9a-4a\) &nbsp; c) \(3x-7x\) &nbsp; d) \(5x+2-3x+1\)", r"Reduce: a) \(6x+2x\) &nbsp; b) \(9a-4a\) &nbsp; c) \(3x-7x\) &nbsp; d) \(5x+2-3x+1\)", r"Simplify: a) \(6x+2x\) &nbsp; b) \(9a-4a\) &nbsp; c) \(3x-7x\) &nbsp; d) \(5x+2-3x+1\)"),
       D(r"\text{a) }\boxed{8x}\qquad \text{b) }\boxed{5a}\qquad \text{c) }\boxed{-4x}\qquad \text{d) }(5x-3x)+(2+1)=\boxed{2x+3}"))],
  [prob(L(r"Calcula: a) \(4x\cdot3x\) &nbsp; b) \((-2a)\cdot5a\) &nbsp; c) \(3(x-5)\) &nbsp; d) \(-(2x+1)\)", r"Calcula: a) \(4x\cdot3x\) &nbsp; b) \((-2a)\cdot5a\) &nbsp; c) \(3(x-5)\) &nbsp; d) \(-(2x+1)\)", r"Work out: a) \(4x\cdot3x\) &nbsp; b) \((-2a)\cdot5a\) &nbsp; c) \(3(x-5)\) &nbsp; d) \(-(2x+1)\)"),
        D(r"\text{a) }\boxed{12x^2}\qquad \text{b) }\boxed{-10a^2}\qquad \text{c) }\boxed{3x-15}\qquad \text{d) }\boxed{-2x-1}")),
   prob(L(r"Traure parèntesis i redueix: \(2(x+4)+3(x-1)\)", r"Quita paréntesis y reduce: \(2(x+4)+3(x-1)\)", r"Remove the brackets and simplify: \(2(x+4)+3(x-1)\)"),
        D(r"2(x+4)+3(x-1)=2x+8+3x-3"),
        D(r"=(2x+3x)+(8-3)=\boxed{5x+5}"))],
  [prob(L(r"Redueix: \(4(2x-1)-3(x+2)+x\)", r"Reduce: \(4(2x-1)-3(x+2)+x\)", r"Simplify: \(4(2x-1)-3(x+2)+x\)"),
        P(r"Traiem parèntesis amb molta cura amb el signe menys:", r"Quitamos paréntesis con mucho cuidado con el signo menos:", r"Remove the brackets, being very careful with the minus sign:"),
        D(r"4(2x-1)-3(x+2)+x=8x-4-3x-6+x"),
        D(r"=(8x-3x+x)+(-4-6)=\boxed{6x-10}")),
   prob(L(r"Un rectangle té una base de \(x+3\) cm i una altura de \(x\) cm. Escriu el seu perímetre de manera reduïda i calcula'l per a \(x=5\).", r"Un rectángulo tiene una base de \(x+3\) cm y una altura de \(x\) cm. Escribe su perímetro de forma reducida y calcúlalo para \(x=5\).", r"A rectangle has base \(x+3\) cm and height \(x\) cm. Write its perimeter in simplified form and work it out for \(x=5\)."),
        D(r"P=2(x+3)+2x=2x+6+2x=\boxed{4x+6}\ \text{cm}"),
        D(r"x=5:\ 4\cdot5+6=\boxed{26\ \text{cm}}"))])
for l, r in [('6x+2x', '8x'), ('9a-4a', '5a'), ('3x-7x', '-4x'), ('5x+2-3x+1', '2x+3'), ('4x*3x', '12x^2'), ('(-2a)*5a', '-10a^2'), ('3(x-5)', '3x-15'), ('-(2x+1)', '-2x-1'),
             ('2(x+4)+3(x-1)', '5x+5'), ('4(2x-1)-3(x+2)+x', '6x-10'), ('2(x+3)+2x', '4x+6')]: chk(l, r)
cv('4x+6', {'x': 5}, 26)
s4 += practice([
  ('★', L(r"Redueix: a) \(7x-2x+x\) &nbsp; b) \(4a+5-a-8\)", r"Reduce: a) \(7x-2x+x\) &nbsp; b) \(4a+5-a-8\)", r"Simplify: a) \(7x-2x+x\) &nbsp; b) \(4a+5-a-8\)")),
  ('★★', L(r"Calcula i redueix: c) \(5x\cdot(-2x)\) &nbsp; d) \(6(x-2)+4\) &nbsp; e) \(10-(3x+4)\)", r"Calcula y reduce: c) \(5x\cdot(-2x)\) &nbsp; d) \(6(x-2)+4\) &nbsp; e) \(10-(3x+4)\)", r"Work out and simplify: c) \(5x\cdot(-2x)\) &nbsp; d) \(6(x-2)+4\) &nbsp; e) \(10-(3x+4)\)")),
  ('★★★', L(r"f) \(3(2x-5)-2(x-4)\) &nbsp; g) \(x(x-2)+2(x+1)\)", r"f) \(3(2x-5)-2(x-4)\) &nbsp; g) \(x(x-2)+2(x+1)\)", r"f) \(3(2x-5)-2(x-4)\) &nbsp; g) \(x(x-2)+2(x+1)\)"))],
  P(r"a) \(6x\) &nbsp; b) \(3a-3\) &nbsp; c) \(-10x^2\) &nbsp; d) \(6x-12+4=6x-8\) &nbsp; e) \(10-3x-4=6-3x\)", r"a) \(6x\) &nbsp; b) \(3a-3\) &nbsp; c) \(-10x^2\) &nbsp; d) \(6x-12+4=6x-8\) &nbsp; e) \(10-3x-4=6-3x\)", r"a) \(6x\) &nbsp; b) \(3a-3\) &nbsp; c) \(-10x^2\) &nbsp; d) \(6x-12+4=6x-8\) &nbsp; e) \(10-3x-4=6-3x\)")
  + P(r"f) \(6x-15-2x+8=4x-7\) &nbsp; g) \(x^2-2x+2x+2=x^2+2\)", r"f) \(6x-15-2x+8=4x-7\) &nbsp; g) \(x^2-2x+2x+2=x^2+2\)", r"f) \(6x-15-2x+8=4x-7\) &nbsp; g) \(x^2-2x+2x+2=x^2+2\)"))
for l, r in [('7x-2x+x', '6x'), ('4a+5-a-8', '3a-3'), ('5x*(-2x)', '-10x^2'), ('6(x-2)+4', '6x-8'), ('10-(3x+4)', '6-3x'), ('3(2x-5)-2(x-4)', '4x-7'), ('x(x-2)+2(x+1)', 'x^2+2')]: chk(l, r)
