# Apartats 3.1-3.3 dels apunts de la Unitat 3 de 2n ESO: l'àlgebra, monomis i operacions amb monomis.
# Els resultats escrits a mà es comproven amb chk() (sympy).
from comu import *

# =====================================================================
# 3.1 L'àlgebra: el llenguatge algebraic
# =====================================================================
TR1 = [("El doble d'un nombre", "El doble de un número", "Twice a number", "2x"),
       ("El triple d'un nombre", "El triple de un número", "Three times a number", "3x"),
       ("La meitat d'un nombre", "La mitad de un número", "Half a number", r"\frac{x}{2}"),
       ("El quadrat d'un nombre", "El cuadrado de un número", "The square of a number", "x^2"),
       ("El cub d'un nombre", "El cubo de un número", "The cube of a number", "x^3"),
       ("El següent d'un nombre", "El siguiente de un número", "The next number", "x+1"),
       ("L'anterior d'un nombre", "El anterior de un número", "The previous number", "x-1"),
       ("Un nombre parell", "Un número par", "An even number", "2x"),
       ("Un nombre senar", "Un número impar", "An odd number", "2x+1"),
       ("L'oposat d'un nombre", "El opuesto de un número", "The opposite of a number", "-x"),
       ("El 10 % d'un nombre", "El 10 % de un número", "10 % of a number", r"0\dc1x"),
       ("La suma de dos nombres", "La suma de dos números", "The sum of two numbers", "x+y"),
       ("El producte de dos nombres", "El producto de dos números", "The product of two numbers", "xy")]
s1 = box('def', L("Què és l'àlgebra?", '¿Qué es el álgebra?', 'What is algebra?'),
  P(r"L'<strong>àlgebra</strong> és la part de les matemàtiques que treballa amb <strong>lletres</strong> a més de nombres. Una lletra (\(x,\ y,\ a,\ b\ldots\)) representa un nombre que <strong>no coneixem</strong> o que <strong>pot prendre qualsevol valor</strong>. Les lletres s'anomenen <strong>variables</strong>.",
    r"El <strong>álgebra</strong> es la parte de las matemáticas que trabaja con <strong>letras</strong> además de números. Una letra (\(x,\ y,\ a,\ b\ldots\)) representa un número que <strong>no conocemos</strong> o que <strong>puede tomar cualquier valor</strong>. Las letras se llaman <strong>variables</strong>.",
    r"<strong>Algebra</strong> is the part of mathematics that works with <strong>letters</strong> as well as numbers. A letter (\(x,\ y,\ a,\ b\ldots\)) stands for a number we <strong>don't know</strong> or that <strong>can take any value</strong>. The letters are called <strong>variables</strong>.")
  + P("Amb l'àlgebra podem:", "Con el álgebra podemos:", "With algebra we can:")
  + ul(L(r"<strong>Generalitzar</strong> propietats: \(a\cdot b=b\cdot a\) és vàlid per a <em>tots</em> els nombres alhora.", r"<strong>Generalizar</strong> propiedades: \(a\cdot b=b\cdot a\) es válido para <em>todos</em> los números a la vez.", r"<strong>Generalise</strong> properties: \(a\cdot b=b\cdot a\) is true for <em>all</em> numbers at once."),
       L(r"<strong>Escriure fórmules</strong>: l'àrea d'un rectangle és \(A=b\cdot h\) i el perímetre d'un quadrat, \(P=4\ell\).", r"<strong>Escribir fórmulas</strong>: el área de un rectángulo es \(A=b\cdot h\) y el perímetro de un cuadrado, \(P=4\ell\).", r"<strong>Write formulas</strong>: the area of a rectangle is \(A=b\cdot h\) and the perimeter of a square is \(P=4\ell\)."),
       L(r"<strong>Descriure seqüències</strong>: els nombres parells són \(2,4,6,8\ldots\), és a dir, \(2n\).", r"<strong>Describir secuencias</strong>: los números pares son \(2,4,6,8\ldots\), es decir, \(2n\).", r"<strong>Describe sequences</strong>: the even numbers are \(2,4,6,8\ldots\), that is, \(2n\)."),
       L(r"<strong>Plantejar i resoldre equacions</strong> per a trobar nombres desconeguts (ho veurem a la unitat següent).", r"<strong>Plantear y resolver ecuaciones</strong> para encontrar números desconocidos (lo veremos en la unidad siguiente).", r"<strong>Set up and solve equations</strong> to find unknown numbers (next unit)."))
  + P(r"Una <strong>expressió algebraica</strong> és una combinació de nombres i lletres units per operacions: \(\ 3x-5,\quad 2a+b^2,\quad \frac{x+1}{2}\).",
      r"Una <strong>expresión algebraica</strong> es una combinación de números y letras unidos por operaciones: \(\ 3x-5,\quad 2a+b^2,\quad \frac{x+1}{2}\).",
      r"An <strong>algebraic expression</strong> combines numbers and letters with operations: \(\ 3x-5,\quad 2a+b^2,\quad \frac{x+1}{2}\)."))
s1 += box('prop', L('Del llenguatge habitual al llenguatge algebraic', 'Del lenguaje habitual al lenguaje algebraico', 'From words to algebra'),
  '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>' + L('Enunciat', 'Enunciado', 'In words') + '</th><th>' + L('Expressió', 'Expresión', 'Expression') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td class="l">{L(va, es, en)}</td><td>\\({e}\\)</td></tr>' for va, es, en, e in TR1) + '</tbody></table></div>'
  + note(r"Convenis: el signe de multiplicar entre un nombre i una lletra (o entre lletres) no s'escriu: \(3\cdot x=3x\), \(a\cdot b=ab\). I el 1 tampoc: \(1x=x\). El nombre sempre s'escriu davant: \(x\cdot 5=5x\).",
         r"Convenios: el signo de multiplicar entre un número y una letra (o entre letras) no se escribe: \(3\cdot x=3x\), \(a\cdot b=ab\). Y el 1 tampoco: \(1x=x\). El número siempre se escribe delante: \(x\cdot 5=5x\).",
         r"Conventions: we don't write the multiplication sign between a number and a letter (or between letters): \(3\cdot x=3x\), \(a\cdot b=ab\). Nor the 1: \(1x=x\). The number always goes first: \(x\cdot 5=5x\).")
  + note(r"Compte amb l'ordre de les paraules: «el doble d'un nombre més 3» és \(2x+3\), però «el doble de la suma d'un nombre i 3» és \(2(x+3)\). I «el quadrat de la suma» \((x+y)^2\) no és «la suma dels quadrats» \(x^2+y^2\).",
         r"Cuidado con el orden de las palabras: «el doble de un número más 3» es \(2x+3\), pero «el doble de la suma de un número y 3» es \(2(x+3)\). Y «el cuadrado de la suma» \((x+y)^2\) no es «la suma de los cuadrados» \(x^2+y^2\).",
         r"Watch the word order: “twice a number plus 3” is \(2x+3\), but “twice the sum of a number and 3” is \(2(x+3)\). And “the square of the sum” \((x+y)^2\) is not “the sum of the squares” \(x^2+y^2\).", '⚠'))
s1 += box('def', L("Valor numèric d'una expressió algebraica", 'Valor numérico de una expresión algebraica', 'Evaluating an expression'),
  P(r"El <strong>valor numèric</strong> d'una expressió algebraica és el nombre que obtenim quan <strong>substituïm</strong> les lletres per nombres i fem les operacions, respectant la <strong>jerarquia</strong>: parèntesis, potències, multiplicacions i divisions, i sumes i restes.",
    r"El <strong>valor numérico</strong> de una expresión algebraica es el número que obtenemos cuando <strong>sustituimos</strong> las letras por números y hacemos las operaciones, respetando la <strong>jerarquía</strong>: paréntesis, potencias, multiplicaciones y divisiones, y sumas y restas.",
    r"The <strong>value</strong> of an algebraic expression is the number we get when we <strong>substitute</strong> numbers for the letters and work it out in the right <strong>order of operations</strong>: brackets, powers, multiplication and division, then addition and subtraction.")
  + D(r"2x^2-3x+1\quad\tri{per a}{para}{for}\ x=-2:\quad 2\cdot(-2)^2-3\cdot(-2)+1=2\cdot4+6+1=15")
  + note(r"Quan substituïm un nombre negatiu, l'escrivim <strong>entre parèntesis</strong>: \((-2)^2=4\), en canvi \(-2^2=-4\).",
         r"Cuando sustituimos un número negativo, lo escribimos <strong>entre paréntesis</strong>: \((-2)^2=4\), en cambio \(-2^2=-4\).",
         r"When you substitute a negative number, write it <strong>in brackets</strong>: \((-2)^2=4\), whereas \(-2^2=-4\).", '⚠')
  + widget('w-val', '🔢', L('Calculadora de valor numèric', 'Calculadora de valor numérico', 'Expression evaluator'),
           ['<div class="wrow">' + tin('p', L('Expressió', 'Expresión', 'Expression'), '2x^2-3x+1') + tin('x', 'x =', '-2', 's') + tin('y', 'y =', '1', 's') + '</div>', HELP,
            quick([('2x^2-3x+1|-2|0', '2x²−3x+1'), ('5x-x^2|3|0', '5x−x²'), ('3x+2y|4|-5', '3x+2y'), ('x^2y-xy^2|2|-1', 'x²y−xy²'), ('(x+1)/2|7|0', '(x+1)/2'), ('-x^3+1|-2|0', '−x³+1')])])
  + drill('lang', 'Entrena: del text a l\'expressió', 'Entrena: del texto a la expresión', 'Train: from words to algebra')
  + drill('val', 'Entrena: valor numèric', 'Entrena: valor numérico', 'Train: evaluating'))
chk('2*(-2)**2-3*(-2)+1', 15)
s1 += levels(
 [prob(L(r"Escriu en llenguatge algebraic: a) el triple d'un nombre menys 4; b) la meitat d'un nombre més 6; c) el quadrat d'un nombre més el seu doble.",
         r"Escribe en lenguaje algebraico: a) el triple de un número menos 4; b) la mitad de un número más 6; c) el cuadrado de un número más su doble.",
         r"Write in algebra: a) three times a number minus 4; b) half a number plus 6; c) the square of a number plus twice the number."),
       D(r"\text{a)}\ \boxed{3x-4}\qquad \text{b)}\ \boxed{\frac{x}{2}+6}\qquad \text{c)}\ \boxed{x^2+2x}")),
  prob(L(r"Calcula el valor numèric de \(5x-x^2\) per a \(x=3\) i per a \(x=-1\).", r"Calcula el valor numérico de \(5x-x^2\) para \(x=3\) y para \(x=-1\).", r"Evaluate \(5x-x^2\) for \(x=3\) and for \(x=-1\)."),
       D(r"x=3:\quad 5\cdot3-3^2=15-9=\boxed{6}"),
       D(r"x=-1:\quad 5\cdot(-1)-(-1)^2=-5-1=\boxed{-6}"),
       P(r"Fixa't que \(-(-1)^2=-1\): primer fem la potència, \((-1)^2=1\), i després el signe menys.", r"Fíjate en que \(-(-1)^2=-1\): primero hacemos la potencia, \((-1)^2=1\), y después el signo menos.", r"Note that \(-(-1)^2=-1\): first the power, \((-1)^2=1\), then the minus sign."))],
 [prob(L(r"L'Àlex té \(x\) euros. La seua germana en té el doble i el seu cosí, 5 € menys que l'Àlex. Escriu quants diners té cada un i quants en tenen entre tots tres.",
         r"Álex tiene \(x\) euros. Su hermana tiene el doble y su primo, 5 € menos que Álex. Escribe cuánto dinero tiene cada uno y cuánto tienen entre los tres.",
         r"Alex has \(x\) euros. His sister has twice as much and his cousin has €5 less than Alex. Write how much each one has and how much they have altogether."),
       D(r"\text{Àlex: }x\qquad \text{germana: }2x\qquad \text{cosí: }x-5"),
       D(r"x+2x+(x-5)=\boxed{4x-5}"),
       P(r"Per exemple, si l'Àlex té 12 €, entre tots tres tenen \(4\cdot12-5=43\) €.", r"Por ejemplo, si Álex tiene 12 €, entre los tres tienen \(4\cdot12-5=43\) €.", r"For example, if Alex has €12, together they have \(4\cdot12-5=43\) €.")),
  prob(L(r"Una botiga de bicicletes lloga cada bici per 4 € més 2,50 € per hora. Escriu l'expressió del preu de llogar una bici \(h\) hores i calcula quant costen 3 hores.",
         r"Una tienda de bicicletas alquila cada bici por 4 € más 2,50 € por hora. Escribe la expresión del precio de alquilar una bici \(h\) horas y calcula cuánto cuestan 3 horas.",
         r"A bike shop rents bikes for €4 plus €2.50 per hour. Write an expression for the price of renting a bike for \(h\) hours and find the cost of 3 hours."),
       D(r"\text{Preu}=2\dc5h+4"), D(r"h=3:\quad 2\dc5\cdot3+4=7\dc5+4=\boxed{11\dc50\ \text{€}}"))],
 [prob(L(r"Observa la seqüència de figures fetes amb escuradents: 4, 7, 10, 13… escuradents (cada quadrat nou en necessita 3 més). Escriu quants escuradents té la figura \(n\) i calcula'n els de la figura 50.",
         r"Observa la secuencia de figuras hechas con palillos: 4, 7, 10, 13… palillos (cada cuadrado nuevo necesita 3 más). Escribe cuántos palillos tiene la figura \(n\) y calcula los de la figura 50.",
         r"Look at the sequence of shapes made with matchsticks: 4, 7, 10, 13… matchsticks (each new square needs 3 more). Write how many matchsticks shape \(n\) has and work out shape 50."),
       P(r"El primer quadrat té 4 escuradents i cada figura en suma 3: la figura \(n\) en té \(4+3(n-1)\).", r"El primer cuadrado tiene 4 palillos y cada figura suma 3: la figura \(n\) tiene \(4+3(n-1)\).", r"The first square has 4 matchsticks and each shape adds 3: shape \(n\) has \(4+3(n-1)\)."),
       D(r"4+3(n-1)=4+3n-3=\boxed{3n+1}\qquad n=50:\ 3\cdot50+1=\boxed{151}"),
       P(r"Comprovació: per a \(n=1,2,3,4\) dona \(4,7,10,13\) ✓", r"Comprobación: para \(n=1,2,3,4\) da \(4,7,10,13\) ✓", r"Check: for \(n=1,2,3,4\) it gives \(4,7,10,13\) ✓"))])
chk('x+2x+(x-5)', '4x-5'); chk('2.5*3+4', 11.5); chk('4+3*(x-1)', '3x+1'); chk('3*50+1', 151)
s1 += practice([
  ('★', L(r"Escriu en llenguatge algebraic: a) el doble d'un nombre més 7; b) la tercera part d'un nombre; c) la suma de dos nombres consecutius.", r"Escribe en lenguaje algebraico: a) el doble de un número más 7; b) la tercera parte de un número; c) la suma de dos números consecutivos.", r"Write in algebra: a) twice a number plus 7; b) a third of a number; c) the sum of two consecutive numbers.")),
  ('★★', L(r"Calcula el valor numèric de d) \(x^2-4x+3\) per a \(x=-1\); e) \(2a-3b\) per a \(a=4,\ b=-2\).", r"Calcula el valor numérico de d) \(x^2-4x+3\) para \(x=-1\); e) \(2a-3b\) para \(a=4,\ b=-2\).", r"Evaluate d) \(x^2-4x+3\) for \(x=-1\); e) \(2a-3b\) for \(a=4,\ b=-2\).")),
  ('★★★', L(r"f) Un rectangle té una base 3 cm més llarga que l'altura \(x\). Escriu el perímetre i l'àrea, i calcula'ls per a \(x=5\) cm.", r"f) Un rectángulo tiene una base 3 cm más larga que la altura \(x\). Escribe el perímetro y el área, y calcúlalos para \(x=5\) cm.", r"f) A rectangle's base is 3 cm longer than its height \(x\). Write its perimeter and area and work them out for \(x=5\) cm."))],
  D(r"\text{a)}\ 2x+7\qquad \text{b)}\ \frac{x}{3}\qquad \text{c)}\ x+(x+1)=2x+1")
  + D(r"\text{d)}\ (-1)^2-4\cdot(-1)+3=1+4+3=8\qquad \text{e)}\ 2\cdot4-3\cdot(-2)=8+6=14")
  + D(r"\text{f)}\ P=2x+2(x+3)=4x+6\to 26\text{ cm};\qquad A=x(x+3)\to 5\cdot8=40\text{ cm}^2"))
chk('(-1)**2-4*(-1)+3', 8); chk('2*4-3*(-2)', 14); chk('2x+2(x+3)', '4x+6'); chk('4*5+6', 26); chk('5*8', 40)

# =====================================================================
# 3.2 Monomis: parts i valor numèric
# =====================================================================
s2 = box('def', L('Monomi: coeficient, part literal i grau', 'Monomio: coeficiente, parte literal y grado', 'Monomials: coefficient, variable part and degree'),
  P(r"Un <strong>monomi</strong> és l'expressió algebraica més senzilla: un <strong>nombre multiplicat per lletres</strong> elevades a exponents naturals (\(1,2,3\ldots\)). Per exemple: \(\ 5x^2,\quad -3ab,\quad \frac{2}{3}x^3y,\quad x,\quad -7\). Té aquestes parts:",
    r"Un <strong>monomio</strong> es la expresión algebraica más sencilla: un <strong>número multiplicado por letras</strong> elevadas a exponentes naturales (\(1,2,3\ldots\)). Por ejemplo: \(\ 5x^2,\quad -3ab,\quad \frac{2}{3}x^3y,\quad x,\quad -7\). Tiene estas partes:",
    r"A <strong>monomial</strong> is the simplest algebraic expression: a <strong>number multiplied by letters</strong> raised to whole-number powers (\(1,2,3\ldots\)). For example: \(\ 5x^2,\quad -3ab,\quad \frac{2}{3}x^3y,\quad x,\quad -7\). Its parts are:")
  + ul(L(r"El <strong>coeficient</strong>: el nombre, <strong>amb el seu signe</strong>.", r"El <strong>coeficiente</strong>: el número, <strong>con su signo</strong>.", r"The <strong>coefficient</strong>: the number, <strong>with its sign</strong>."),
       L(r"La <strong>part literal</strong>: les lletres amb els seus exponents.", r"La <strong>parte literal</strong>: las letras con sus exponentes.", r"The <strong>variable part</strong>: the letters with their exponents."),
       L(r"El <strong>grau</strong>: la <strong>suma dels exponents</strong> de totes les lletres.", r"El <strong>grado</strong>: la <strong>suma de los exponentes</strong> de todas las letras.", r"The <strong>degree</strong>: the <strong>sum of the exponents</strong> of all the letters."))
  + D(r"\underbrace{-4}_{\tri{coeficient}{coeficiente}{coefficient}}\ \underbrace{x^{3}y^{2}}_{\tri{part literal}{parte literal}{variable part}}\qquad \tri{grau}{grado}{degree}=3+2=5")
  + table([L('Monomi', 'Monomio', 'Monomial'), L('Coeficient', 'Coeficiente', 'Coefficient'), L('Part literal', 'Parte literal', 'Variable part'), L('Grau', 'Grado', 'Degree')],
          [[r'\(7x^2\)', r'\(7\)', r'\(x^2\)', r'\(2\)'], [r'\(-ab\)', r'\(-1\)', r'\(ab\)', r'\(1+1=2\)'], [r'\(\frac{3}{4}x^3y\)', r'\(\frac{3}{4}\)', r'\(x^3y\)', r'\(3+1=4\)'],
           [r'\(x\)', r'\(1\)', r'\(x\)', r'\(1\)'], [r'\(-9\)', r'\(-9\)', L('no en té', 'no tiene', 'none'), r'\(0\)']])
  + note(r"Si no veus el coeficient, és 1: \(x^2=1x^2\) i \(-ab=-1ab\). Si una lletra no té exponent, l'exponent és 1: \(x=x^1\). Un nombre sol, com \(-9\), és un monomi de <strong>grau 0</strong>.",
         r"Si no ves el coeficiente, es 1: \(x^2=1x^2\) y \(-ab=-1ab\). Si una letra no tiene exponente, el exponente es 1: \(x=x^1\). Un número solo, como \(-9\), es un monomio de <strong>grado 0</strong>.",
         r"If you can't see a coefficient, it's 1: \(x^2=1x^2\) and \(-ab=-1ab\). A letter with no exponent has exponent 1: \(x=x^1\). A number on its own, like \(-9\), is a monomial of <strong>degree 0</strong>."))
s2 += box('prop', L('Què <u>no</u> és un monomi', 'Qué <u>no</u> es un monomio', 'What is <u>not</u> a monomial'),
  ul(L(r"\(2x+3\): té dues parts que se sumen (és un <em>binomi</em>, un polinomi).", r"\(2x+3\): tiene dos partes que se suman (es un <em>binomio</em>, un polinomio).", r"\(2x+3\): it has two parts added together (a <em>binomial</em>, a polynomial)."),
     L(r"\(\frac{5}{x}\): la lletra està al denominador.", r"\(\frac{5}{x}\): la letra está en el denominador.", r"\(\frac{5}{x}\): the letter is in the denominator."),
     L(r"\(x^{-2}\) o \(\sqrt{x}\): l'exponent no és un nombre natural.", r"\(x^{-2}\) o \(\sqrt{x}\): el exponente no es un número natural.", r"\(x^{-2}\) or \(\sqrt{x}\): the exponent isn't a whole number."))
  + note(r"En canvi, \(\frac{x}{5}\) <strong>sí</strong> que és un monomi: és \(\frac{1}{5}x\), de coeficient \(\frac{1}{5}\).", r"En cambio, \(\frac{x}{5}\) <strong>sí</strong> es un monomio: es \(\frac{1}{5}x\), de coeficiente \(\frac{1}{5}\).", r"But \(\frac{x}{5}\) <strong>is</strong> a monomial: it's \(\frac{1}{5}x\), with coefficient \(\frac{1}{5}\)."))
s2 += box('def', L('Monomis semblants', 'Monomios semejantes', 'Like terms'),
  P(r"Dos monomis són <strong>semblants</strong> si tenen <strong>la mateixa part literal</strong> (les mateixes lletres amb els mateixos exponents). Els coeficients poden ser diferents.",
    r"Dos monomios son <strong>semejantes</strong> si tienen <strong>la misma parte literal</strong> (las mismas letras con los mismos exponentes). Los coeficientes pueden ser distintos.",
    r"Two monomials are <strong>like terms</strong> if they have <strong>the same variable part</strong> (the same letters with the same exponents). The coefficients can differ.")
  + D(r"5x^2y\ \text{ i }\ -\tfrac{1}{2}x^2y\ \tri{són semblants}{son semejantes}{are like terms};\qquad 5x^2y\ \text{ i }\ 5xy^2\ \tri{no ho són}{no lo son}{are not}")
  + P(r"Dos monomis semblants que només es diferencien en el signe del coeficient, com \(3ab\) i \(-3ab\), són <strong>oposats</strong>: sumen 0.",
      r"Dos monomios semejantes que solo se diferencian en el signo del coeficiente, como \(3ab\) y \(-3ab\), son <strong>opuestos</strong>: suman 0.",
      r"Two like terms that differ only in the sign of the coefficient, like \(3ab\) and \(-3ab\), are <strong>opposites</strong>: they add up to 0."))
s2 += box('def', L("Valor numèric d'un monomi", 'Valor numérico de un monomio', 'Value of a monomial'),
  P(r"Com en qualsevol expressió, substituïm cada lletra pel seu valor i operem. Primer les <strong>potències</strong> i després la <strong>multiplicació</strong>:",
    r"Como en cualquier expresión, sustituimos cada letra por su valor y operamos. Primero las <strong>potencias</strong> y después la <strong>multiplicación</strong>:",
    r"As with any expression, replace each letter with its value and work it out. <strong>Powers</strong> first, then <strong>multiplication</strong>:")
  + D(r"-4x^3y^2\quad\tri{per a}{para}{for}\ x=-1,\ y=3:\quad -4\cdot(-1)^3\cdot3^2=-4\cdot(-1)\cdot9=36")
  + widget('w-mono', '🔎', L('Analitzador de monomis', 'Analizador de monomios', 'Monomial analyser'),
           ['<div class="wrow">' + tin('m', L('Monomi', 'Monomio', 'Monomial'), '-4x^3y^2') + '</div>', HELP,
            quick([('-4x^3y^2', '−4x³y²'), ('7x^2', '7x²'), ('-ab', '−ab'), ('3/4x^3y', '¾x³y'), ('x', 'x'), ('-9', '−9'), ('2x*5x^2', '2x·5x²'), ('5/x', '5/x'), ('2x+3', '2x+3')])], out='<div class="cards"></div>'))
chk('-4*(-1)**3*3**2', 36)
s2 += levels(
 [prob(L(r"Indica el coeficient, la part literal i el grau de: a) \(-8x^4\); b) \(xy^3\); c) \(\frac{2}{5}a^2b^2c\).", r"Indica el coeficiente, la parte literal y el grado de: a) \(-8x^4\); b) \(xy^3\); c) \(\frac{2}{5}a^2b^2c\).", r"Give the coefficient, variable part and degree of: a) \(-8x^4\); b) \(xy^3\); c) \(\frac{2}{5}a^2b^2c\)."),
       P(r"a) Coeficient \(-8\), part literal \(x^4\), grau \(\boxed{4}\).", r"a) Coeficiente \(-8\), parte literal \(x^4\), grado \(\boxed{4}\).", r"a) Coefficient \(-8\), variable part \(x^4\), degree \(\boxed{4}\)."),
       P(r"b) Coeficient \(1\) (no s'escriu), part literal \(xy^3\), grau \(1+3=\boxed{4}\).", r"b) Coeficiente \(1\) (no se escribe), parte literal \(xy^3\), grado \(1+3=\boxed{4}\).", r"b) Coefficient \(1\) (not written), variable part \(xy^3\), degree \(1+3=\boxed{4}\)."),
       P(r"c) Coeficient \(\frac{2}{5}\), part literal \(a^2b^2c\), grau \(2+2+1=\boxed{5}\).", r"c) Coeficiente \(\frac{2}{5}\), parte literal \(a^2b^2c\), grado \(2+2+1=\boxed{5}\).", r"c) Coefficient \(\frac{2}{5}\), variable part \(a^2b^2c\), degree \(2+2+1=\boxed{5}\).")),
  prob(L(r"Agrupa els monomis semblants: \(\ 3x^2,\ -5x,\ \frac{1}{2}x^2,\ 7xy,\ x,\ -x^2,\ -2xy\).", r"Agrupa los monomios semejantes: \(\ 3x^2,\ -5x,\ \frac{1}{2}x^2,\ 7xy,\ x,\ -x^2,\ -2xy\).", r"Group the like terms: \(\ 3x^2,\ -5x,\ \frac{1}{2}x^2,\ 7xy,\ x,\ -x^2,\ -2xy\)."),
       D(r"\{3x^2,\ \tfrac{1}{2}x^2,\ -x^2\}\qquad \{-5x,\ x\}\qquad \{7xy,\ -2xy\}"))],
 [prob(L(r"Calcula el valor numèric de \(-2a^2b\) per a \(a=3,\ b=-1\) i per a \(a=-\frac{1}{2},\ b=4\).", r"Calcula el valor numérico de \(-2a^2b\) para \(a=3,\ b=-1\) y para \(a=-\frac{1}{2},\ b=4\).", r"Evaluate \(-2a^2b\) for \(a=3,\ b=-1\) and for \(a=-\frac{1}{2},\ b=4\)."),
       D(r"-2\cdot3^2\cdot(-1)=-2\cdot9\cdot(-1)=\boxed{18}"),
       D(r"-2\cdot\left(-\tfrac{1}{2}\right)^2\cdot4=-2\cdot\tfrac{1}{4}\cdot4=\boxed{-2}"))],
 [prob(L(r"Escriu un monomi de grau 5, amb les lletres \(x\) i \(y\) i coeficient \(-3\), que valga \(-24\) per a \(x=2,\ y=1\). N'hi ha més d'un?", r"Escribe un monomio de grado 5, con las letras \(x\) e \(y\) y coeficiente \(-3\), que valga \(-24\) para \(x=2,\ y=1\). ¿Hay más de uno?", r"Write a degree-5 monomial in \(x\) and \(y\) with coefficient \(-3\) whose value is \(-24\) when \(x=2,\ y=1\). Is there more than one?"),
       P(r"Ha de ser \(-3x^my^n\) amb \(m+n=5\). Com que \(y=1\), el valor és \(-3\cdot2^m=-24\), és a dir, \(2^m=8\) i \(m=3\). Aleshores \(n=2\):", r"Debe ser \(-3x^my^n\) con \(m+n=5\). Como \(y=1\), el valor es \(-3\cdot2^m=-24\), es decir, \(2^m=8\) y \(m=3\). Entonces \(n=2\):", r"It must be \(-3x^my^n\) with \(m+n=5\). Since \(y=1\), its value is \(-3\cdot2^m=-24\), so \(2^m=8\) and \(m=3\). Then \(n=2\):"),
       D(r"\boxed{-3x^3y^2}"),
       P(r"Només n'hi ha un: l'exponent de la \(x\) queda obligat pel valor i el de la \(y\), pel grau.", r"Solo hay uno: el exponente de la \(x\) queda obligado por el valor y el de la \(y\), por el grado.", r"There's only one: the exponent of \(x\) is forced by the value and the exponent of \(y\) by the degree."))])
chk('-2*9*(-1)', 18); chk('-2*(1/4)*4', -2); chk('-3*2**3*1', -24)
s2 += practice([
  ('★', L(r"a) Indica el coeficient, la part literal i el grau de \(6x^2y^3\), \(-z\) i \(\frac{x^4}{3}\). b) Quins d'aquests són monomis? \(\ 4x^3,\ \ \frac{2}{x},\ \ x^2-1,\ \ -\frac{y}{2},\ \ 8\).", r"a) Indica el coeficiente, la parte literal y el grado de \(6x^2y^3\), \(-z\) y \(\frac{x^4}{3}\). b) ¿Cuáles de estos son monomios? \(\ 4x^3,\ \ \frac{2}{x},\ \ x^2-1,\ \ -\frac{y}{2},\ \ 8\).", r"a) Give the coefficient, variable part and degree of \(6x^2y^3\), \(-z\) and \(\frac{x^4}{3}\). b) Which of these are monomials? \(\ 4x^3,\ \ \frac{2}{x},\ \ x^2-1,\ \ -\frac{y}{2},\ \ 8\).")),
  ('★★', L(r"c) Escriu dos monomis semblants a \(-2ab^3\) i un d'oposat. d) Calcula el valor numèric de \(5x^2y\) per a \(x=-2,\ y=3\).", r"c) Escribe dos monomios semejantes a \(-2ab^3\) y uno opuesto. d) Calcula el valor numérico de \(5x^2y\) para \(x=-2,\ y=3\).", r"c) Write two like terms of \(-2ab^3\) and its opposite. d) Evaluate \(5x^2y\) for \(x=-2,\ y=3\).")),
  ('★★★', L(r"e) Troba \(m\) perquè els monomis \(4x^{m+1}y\) i \(-x^5y\) siguen semblants. Quin és el grau de tots dos?", r"e) Halla \(m\) para que los monomios \(4x^{m+1}y\) y \(-x^5y\) sean semejantes. ¿Cuál es el grado de ambos?", r"e) Find \(m\) so that \(4x^{m+1}y\) and \(-x^5y\) are like terms. What is their degree?"))],
  P(r"a) \(6x^2y^3\): coef. \(6\), part literal \(x^2y^3\), grau 5. \(-z\): coef. \(-1\), part literal \(z\), grau 1. \(\frac{x^4}{3}\): coef. \(\frac{1}{3}\), part literal \(x^4\), grau 4. b) Són monomis \(4x^3\), \(-\frac{y}{2}\) i \(8\).",
    r"a) \(6x^2y^3\): coef. \(6\), parte literal \(x^2y^3\), grado 5. \(-z\): coef. \(-1\), parte literal \(z\), grado 1. \(\frac{x^4}{3}\): coef. \(\frac{1}{3}\), parte literal \(x^4\), grado 4. b) Son monomios \(4x^3\), \(-\frac{y}{2}\) y \(8\).",
    r"a) \(6x^2y^3\): coef. \(6\), variable part \(x^2y^3\), degree 5. \(-z\): coef. \(-1\), variable part \(z\), degree 1. \(\frac{x^4}{3}\): coef. \(\frac{1}{3}\), variable part \(x^4\), degree 4. b) The monomials are \(4x^3\), \(-\frac{y}{2}\) and \(8\).")
  + P(r"c) Per exemple \(7ab^3\) i \(\frac{1}{2}ab^3\); l'oposat és \(2ab^3\). d) \(5\cdot(-2)^2\cdot3=5\cdot4\cdot3=60\). e) Cal \(m+1=5\), és a dir, \(m=4\); tots dos són de grau \(5+1=6\).",
      r"c) Por ejemplo \(7ab^3\) y \(\frac{1}{2}ab^3\); el opuesto es \(2ab^3\). d) \(5\cdot(-2)^2\cdot3=5\cdot4\cdot3=60\). e) Hace falta \(m+1=5\), es decir, \(m=4\); los dos son de grado \(5+1=6\).",
      r"c) For example \(7ab^3\) and \(\frac{1}{2}ab^3\); the opposite is \(2ab^3\). d) \(5\cdot(-2)^2\cdot3=5\cdot4\cdot3=60\). e) We need \(m+1=5\), so \(m=4\); both have degree \(5+1=6\)."))
chk('5*(-2)**2*3', 60)

# =====================================================================
# 3.3 Operacions amb monomis
# =====================================================================
s3 = box('def', L('Suma i resta de monomis', 'Suma y resta de monomios', 'Adding and subtracting monomials'),
  P(r"Només podem sumar o restar <strong>monomis semblants</strong>. Sumem o restem els <strong>coeficients</strong> i deixem <strong>la mateixa part literal</strong>:",
    r"Solo podemos sumar o restar <strong>monomios semejantes</strong>. Sumamos o restamos los <strong>coeficientes</strong> y dejamos <strong>la misma parte literal</strong>:",
    r"We can only add or subtract <strong>like terms</strong>. Add or subtract the <strong>coefficients</strong> and keep <strong>the same variable part</strong>:")
  + D(r"5x^2+3x^2=(5+3)x^2=8x^2\qquad 4ab-7ab=(4-7)ab=-3ab")
  + P(r"Si no són semblants, la suma es deixa indicada: \(5x^2+3x\) no es pot simplificar (és un polinomi). Quan en una expressió hi ha molts termes, <strong>reduir</strong> vol dir agrupar els semblants:",
      r"Si no son semejantes, la suma se deja indicada: \(5x^2+3x\) no se puede simplificar (es un polinomio). Cuando en una expresión hay muchos términos, <strong>reducir</strong> significa agrupar los semejantes:",
      r"If they aren't like terms, the sum is left as it is: \(5x^2+3x\) can't be simplified (it's a polynomial). When an expression has many terms, <strong>simplifying</strong> means collecting like terms:")
  + D(r"\underline{3x^2}\ \underline{\underline{-5x}}+4\ \underline{-x^2}\ \underline{\underline{+2x}}-1=2x^2-3x+3")
  + note(r"Error molt freqüent: \(5x^2+3x^2\neq 8x^4\). En sumar, els <strong>exponents no canvien</strong>: sumem «quantes \(x^2\)» tenim, com 5 pomes + 3 pomes = 8 pomes.",
         r"Error muy frecuente: \(5x^2+3x^2\neq 8x^4\). Al sumar, los <strong>exponentes no cambian</strong>: sumamos «cuántas \(x^2\)» tenemos, como 5 manzanas + 3 manzanas = 8 manzanas.",
         r"Very common mistake: \(5x^2+3x^2\neq 8x^4\). When adding, the <strong>exponents don't change</strong>: we're counting “how many \(x^2\)” we have, like 5 apples + 3 apples = 8 apples.", '⚠')
  + drill('red', 'Entrena: reduir termes semblants', 'Entrena: reducir términos semejantes', 'Train: collecting like terms'))
chk('3x^2-5x+4-x^2+2x-1', '2x^2-3x+3')
s3 += box('def', L('Producte i quocient de monomis', 'Producto y cociente de monomios', 'Multiplying and dividing monomials'),
  P(r"Per a <strong>multiplicar</strong>, multipliquem els coeficients i, per a cada lletra, <strong>sumem els exponents</strong> (\(x^m\cdot x^n=x^{m+n}\)). Els monomis <strong>no</strong> han de ser semblants:",
    r"Para <strong>multiplicar</strong>, multiplicamos los coeficientes y, para cada letra, <strong>sumamos los exponentes</strong> (\(x^m\cdot x^n=x^{m+n}\)). Los monomios <strong>no</strong> tienen que ser semejantes:",
    r"To <strong>multiply</strong>, multiply the coefficients and, for each letter, <strong>add the exponents</strong> (\(x^m\cdot x^n=x^{m+n}\)). The monomials do <strong>not</strong> have to be like terms:")
  + D(r"(-3x^2y)\cdot(4xy^3)=(-3\cdot4)\,x^{2+1}y^{1+3}=-12x^3y^4")
  + P(r"Per a <strong>dividir</strong>, dividim els coeficients i, per a cada lletra, <strong>restem els exponents</strong> (\(x^m:x^n=x^{m-n}\)):",
      r"Para <strong>dividir</strong>, dividimos los coeficientes y, para cada letra, <strong>restamos los exponentes</strong> (\(x^m:x^n=x^{m-n}\)):",
      r"To <strong>divide</strong>, divide the coefficients and, for each letter, <strong>subtract the exponents</strong> (\(x^m:x^n=x^{m-n}\)):")
  + D(r"15x^5y^2:(3x^2y)=(15:3)\,x^{5-2}y^{2-1}=5x^3y\qquad 6x^2y:(2x^2)=3x^0y=3y")
  + note(r"El quocient de dos monomis només és un monomi si cada lletra del divisor està en el dividend amb un exponent igual o més gran. Per exemple, \(4x^2:(8x^3)=\frac{1}{2x}\) <strong>no</strong> és un monomi.",
         r"El cociente de dos monomios solo es un monomio si cada letra del divisor está en el dividendo con un exponente igual o mayor. Por ejemplo, \(4x^2:(8x^3)=\frac{1}{2x}\) <strong>no</strong> es un monomio.",
         r"The quotient of two monomials is a monomial only if every letter of the divisor appears in the dividend with an equal or higher exponent. For example, \(4x^2:(8x^3)=\frac{1}{2x}\) is <strong>not</strong> a monomial."))
s3 += box('def', L("Potència d'un monomi", 'Potencia de un monomio', 'Powers of a monomial'),
  P(r"Per a elevar un monomi a un exponent, elevem el <strong>coeficient</strong> a aquest exponent i <strong>multipliquem</strong> l'exponent de cada lletra per ell (\((x^m)^n=x^{m\cdot n}\)):",
    r"Para elevar un monomio a un exponente, elevamos el <strong>coeficiente</strong> a ese exponente y <strong>multiplicamos</strong> el exponente de cada letra por él (\((x^m)^n=x^{m\cdot n}\)):",
    r"To raise a monomial to a power, raise the <strong>coefficient</strong> to that power and <strong>multiply</strong> each letter's exponent by it (\((x^m)^n=x^{m\cdot n}\)):")
  + D(r"(-2x^3y)^4=(-2)^4\,x^{3\cdot4}y^{1\cdot4}=16x^{12}y^4\qquad (-2x^3y)^3=(-2)^3\,x^{9}y^{3}=-8x^9y^3")
  + note(r"Compte amb el signe: un coeficient negatiu elevat a un exponent <strong>parell</strong> dona positiu i a un exponent <strong>senar</strong> dona negatiu. I compte amb els parèntesis: \((3x)^2=9x^2\), però \(3x^2\) només eleva la \(x\).",
         r"Cuidado con el signo: un coeficiente negativo elevado a un exponente <strong>par</strong> da positivo y a un exponente <strong>impar</strong> da negativo. Y cuidado con los paréntesis: \((3x)^2=9x^2\), pero \(3x^2\) solo eleva la \(x\).",
         r"Watch the sign: a negative coefficient to an <strong>even</strong> power is positive and to an <strong>odd</strong> power is negative. And watch the brackets: \((3x)^2=9x^2\), but \(3x^2\) only squares the \(x\).", '⚠')
  + widget('w-monops', '🧮', L('Operacions amb monomis pas a pas', 'Operaciones con monomios paso a paso', 'Monomial operations step by step'),
           ['<div class="wrow">' + tin('a', 'A =', '-3x^2y', 's') + seg([('+', '+'), ('-', '−'), ('*', '·'), (':', ':'), ('^', 'Aⁿ')], '*') + tin('b', 'B =', '4xy^3', 's') + '</div>',
            '<p class="hint-s">' + L("Escriu les potències amb ^ (x^2). Per a la potència Aⁿ, escriu l'exponent n a la casella B.", "Escribe las potencias con ^ (x^2). Para la potencia Aⁿ, escribe el exponente n en la casilla B.", "Type powers with ^ (x^2). For the power Aⁿ, type the exponent n in box B.") + '</p>',
            quick([('5x^2|3x^2|+', '5x² + 3x²'), ('4ab|7ab|-', '4ab − 7ab'), ('5x^2|3x|+', '5x² + 3x'), ('-3x^2y|4xy^3|*', '(−3x²y)·(4xy³)'), ('15x^5y^2|3x^2y|:', '15x⁵y² : 3x²y'), ('4x^2|8x^3|:', '4x² : 8x³'), ('-2x^3y|4|^', '(−2x³y)⁴'), ('-2x^3y|3|^', '(−2x³y)³')])])
  + drill('mono', 'Entrena: suma, producte i quocient', 'Entrena: suma, producto y cociente', 'Train: sums, products and quotients')
  + drill('pow', "Entrena: potència d'un monomi", 'Entrena: potencia de un monomio', 'Train: powers of a monomial'))
chk('(-3x^2y)*(4xy^3)', '-12x^3y^4'); chk('15x^5y^2/(3x^2y)', '5x^3y'); chk('(-2x^3y)^4', '16x^12y^4'); chk('(-2x^3y)^3', '-8x^9y^3')
s3 += box('prop', L('Operacions combinades amb monomis', 'Operaciones combinadas con monomios', 'Mixed operations with monomials'),
  P(r"Seguim la mateixa <strong>jerarquia</strong> que amb els nombres: 1) parèntesis, 2) potències, 3) multiplicacions i divisions (d'esquerra a dreta), 4) sumes i restes. Al final, <strong>reduïm</strong> els termes semblants.",
    r"Seguimos la misma <strong>jerarquía</strong> que con los números: 1) paréntesis, 2) potencias, 3) multiplicaciones y divisiones (de izquierda a derecha), 4) sumas y restas. Al final, <strong>reducimos</strong> los términos semejantes.",
    r"We follow the same <strong>order of operations</strong> as with numbers: 1) brackets, 2) powers, 3) multiplication and division (left to right), 4) addition and subtraction. Finally, we <strong>collect</strong> like terms.")
  + D(r"(2x^2)^3:(4x^2)-3x\cdot x^3=8x^6:(4x^2)-3x^4=2x^4-3x^4=-x^4")
  + drill('comb', 'Entrena: operacions combinades', 'Entrena: operaciones combinadas', 'Train: mixed operations'))
chk('(2x^2)^3/(4x^2)-3x*x^3', '-x^4')
s3 += levels(
 [prob(L(r"Redueix: a) \(7x-2x+x\); b) \(4a^2-6a^2+a^2\); c) \(3x^2+5x-x^2-8x+2\).", r"Reduce: a) \(7x-2x+x\); b) \(4a^2-6a^2+a^2\); c) \(3x^2+5x-x^2-8x+2\).", r"Simplify: a) \(7x-2x+x\); b) \(4a^2-6a^2+a^2\); c) \(3x^2+5x-x^2-8x+2\)."),
       D(r"\text{a)}\ (7-2+1)x=\boxed{6x}\qquad \text{b)}\ (4-6+1)a^2=\boxed{-a^2}"),
       D(r"\text{c)}\ (3-1)x^2+(5-8)x+2=\boxed{2x^2-3x+2}")),
  prob(L(r"Calcula: a) \(5x^3\cdot(-2x^4)\); b) \(-6a^2b\cdot\frac{1}{3}ab^2\); c) \(20x^6:(5x^2)\); d) \((-9x^4y^3):(-3xy^3)\).", r"Calcula: a) \(5x^3\cdot(-2x^4)\); b) \(-6a^2b\cdot\frac{1}{3}ab^2\); c) \(20x^6:(5x^2)\); d) \((-9x^4y^3):(-3xy^3)\).", r"Work out: a) \(5x^3\cdot(-2x^4)\); b) \(-6a^2b\cdot\frac{1}{3}ab^2\); c) \(20x^6:(5x^2)\); d) \((-9x^4y^3):(-3xy^3)\)."),
       D(r"\text{a)}\ \boxed{-10x^7}\qquad \text{b)}\ -6\cdot\tfrac{1}{3}\,a^{3}b^{3}=\boxed{-2a^3b^3}"),
       D(r"\text{c)}\ \boxed{4x^4}\qquad \text{d)}\ 3x^{3}y^{0}=\boxed{3x^3}"),
       P(r"En d) la \(y\) desapareix perquè \(y^3:y^3=y^0=1\).", r"En d) la \(y\) desaparece porque \(y^3:y^3=y^0=1\).", r"In d) the \(y\) disappears because \(y^3:y^3=y^0=1\)."))],
 [prob(L(r"Calcula: a) \((3x^2)^3\); b) \((-x^3y^2)^4\); c) \(\left(-\frac{1}{2}ab^3\right)^3\).", r"Calcula: a) \((3x^2)^3\); b) \((-x^3y^2)^4\); c) \(\left(-\frac{1}{2}ab^3\right)^3\).", r"Work out: a) \((3x^2)^3\); b) \((-x^3y^2)^4\); c) \(\left(-\frac{1}{2}ab^3\right)^3\)."),
       D(r"\text{a)}\ 3^3x^{6}=\boxed{27x^6}\qquad \text{b)}\ (-1)^4x^{12}y^{8}=\boxed{x^{12}y^8}\qquad \text{c)}\ \left(-\tfrac{1}{2}\right)^3a^3b^9=\boxed{-\tfrac{1}{8}a^3b^9}")),
  prob(L(r"Opera i redueix: \(\ 2x\cdot5x^3-(3x^2)^2+12x^5:(4x)\).", r"Opera y reduce: \(\ 2x\cdot5x^3-(3x^2)^2+12x^5:(4x)\).", r"Work out and simplify: \(\ 2x\cdot5x^3-(3x^2)^2+12x^5:(4x)\)."),
       P(r"Primer la potència; després el producte i el quocient; al final sumem i restem:", r"Primero la potencia; después el producto y el cociente; al final sumamos y restamos:", r"First the power; then the product and the quotient; finally add and subtract:"),
       D(r"2x\cdot5x^3-9x^4+12x^5:(4x)=10x^4-9x^4+3x^4=\boxed{4x^4}"))],
 [prob(L(r"Opera i redueix: \(\ (-2x^2y)^3:(4x^3y^2)-3x^2\cdot(-xy)\cdot x\).", r"Opera y reduce: \(\ (-2x^2y)^3:(4x^3y^2)-3x^2\cdot(-xy)\cdot x\).", r"Work out and simplify: \(\ (-2x^2y)^3:(4x^3y^2)-3x^2\cdot(-xy)\cdot x\)."),
       D(r"(-2x^2y)^3=-8x^6y^3\qquad -8x^6y^3:(4x^3y^2)=-2x^3y"),
       D(r"-3x^2\cdot(-xy)\cdot x=+3x^4y\quad\tri{(menys per menys, més)}{(menos por menos, más)}{(minus times minus is plus)}"),
       D(r"-2x^3y+3x^4y=\boxed{3x^4y-2x^3y}"),
       P(r"Els dos termes finals <strong>no</strong> són semblants (\(x^4y\) i \(x^3y\)): ja no es pot reduir més.", r"Los dos términos finales <strong>no</strong> son semejantes (\(x^4y\) y \(x^3y\)): ya no se puede reducir más.", r"The two final terms are <strong>not</strong> like terms (\(x^4y\) and \(x^3y\)): nothing more can be done.")),
  prob(L(r"Un cub té l'aresta \(3x\) cm. Escriu-ne l'àrea total i el volum com a monomis. Què passa amb el volum si l'aresta es duplica?", r"Un cubo tiene la arista \(3x\) cm. Escribe su área total y su volumen como monomios. ¿Qué pasa con el volumen si la arista se duplica?", r"A cube has edge \(3x\) cm. Write its total surface area and volume as monomials. What happens to the volume if the edge doubles?"),
       D(r"A=6\cdot(3x)^2=6\cdot9x^2=\boxed{54x^2\ \text{cm}^2}\qquad V=(3x)^3=\boxed{27x^3\ \text{cm}^3}"),
       D(r"(2\cdot3x)^3=(6x)^3=216x^3=8\cdot27x^3"),
       P(r"El volum es fa <strong>8 vegades</strong> més gran (\(2^3=8\)).", r"El volumen se hace <strong>8 veces</strong> mayor (\(2^3=8\)).", r"The volume becomes <strong>8 times</strong> bigger (\(2^3=8\))."))])
chk('7x-2x+x', '6x'); chk('4a^2-6a^2+a^2', '-a^2'); chk('3x^2+5x-x^2-8x+2', '2x^2-3x+2')
chk('5x^3*(-2x^4)', '-10x^7'); chk('-6a^2b*a*b^2/3', '-2a^3b^3'); chk('20x^6/(5x^2)', '4x^4'); chk('(-9x^4y^3)/(-3x*y^3)', '3x^3')
chk('(3x^2)^3', '27x^6'); chk('(-x^3y^2)^4', 'x^12y^8'); chk('(-ab^3/2)^3', '-a^3b^9/8')
chk('2x*5x^3-(3x^2)^2+12x^5/(4x)', '4x^4'); chk('(-2x^2y)^3/(4x^3y^2)-3x^2*(-x*y)*x', '3x^4y-2x^3y')
chk('6*(3x)^2', '54x^2'); chk('(6x)^3', '8*27x^3')
s3 += practice([
  ('★', L(r"Calcula: a) \(6x^2-9x^2+2x^2\); b) \(-4x^3\cdot3x\); c) \(14a^5b:(7a^2b)\); d) \((2x^4)^2\).", r"Calcula: a) \(6x^2-9x^2+2x^2\); b) \(-4x^3\cdot3x\); c) \(14a^5b:(7a^2b)\); d) \((2x^4)^2\).", r"Work out: a) \(6x^2-9x^2+2x^2\); b) \(-4x^3\cdot3x\); c) \(14a^5b:(7a^2b)\); d) \((2x^4)^2\).")),
  ('★★', L(r"e) \(x^2\cdot(-2x)^3\); f) \((-5x^2y)^2:(5xy^2)\); g) \(4x\cdot2x^2-x^2\cdot5x\).", r"e) \(x^2\cdot(-2x)^3\); f) \((-5x^2y)^2:(5xy^2)\); g) \(4x\cdot2x^2-x^2\cdot5x\).", r"e) \(x^2\cdot(-2x)^3\); f) \((-5x^2y)^2:(5xy^2)\); g) \(4x\cdot2x^2-x^2\cdot5x\).")),
  ('★★★', L(r"h) \((3a^2b)^2\cdot(-ab)^3:(9a^5b^4)\); i) \((-x^2)^3+2x^4\cdot(-x)^2-(2x^3)^2:4\).", r"h) \((3a^2b)^2\cdot(-ab)^3:(9a^5b^4)\); i) \((-x^2)^3+2x^4\cdot(-x)^2-(2x^3)^2:4\).", r"h) \((3a^2b)^2\cdot(-ab)^3:(9a^5b^4)\); i) \((-x^2)^3+2x^4\cdot(-x)^2-(2x^3)^2:4\)."))],
  D(r"\text{a)}\ -x^2\qquad \text{b)}\ -12x^4\qquad \text{c)}\ 2a^3\qquad \text{d)}\ 4x^8")
  + D(r"\text{e)}\ x^2\cdot(-8x^3)=-8x^5\qquad \text{f)}\ 25x^4y^2:(5xy^2)=5x^3\qquad \text{g)}\ 8x^3-5x^3=3x^3")
  + D(r"\text{h)}\ 9a^4b^2\cdot(-a^3b^3):(9a^5b^4)=-9a^7b^5:(9a^5b^4)=-a^2b\qquad \text{i)}\ -x^6+2x^6-x^6=0"))
chk('6x^2-9x^2+2x^2', '-x^2'); chk('-4x^3*3x', '-12x^4'); chk('14a^5b/(7a^2b)', '2a^3'); chk('(2x^4)^2', '4x^8')
chk('x^2*(-2x)^3', '-8x^5'); chk('(-5x^2y)^2/(5x*y^2)', '5x^3'); chk('4x*2x^2-x^2*5x', '3x^3')
chk('(3a^2b)^2*(-a*b)^3/(9a^5b^4)', '-a^2b'); chk('(-x^2)^3+2x^4*(-x)^2-(2x^3)^2/4', 0)
