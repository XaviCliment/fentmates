# Apartats 1.1-1.4 (nombres naturals i enters) dels apunts de la Unitat 1 de 4t ESO A.
# Part de la teoria ve de ../2eso-t1/build.py (apartats 1.1, 1.7-1.10), simplificada; els problemes són nous.
# Les asserts comproven els resultats escrits a mà.
from eines4a import *

def chk(e, v): assert ev(e) == v, (e, ev(e), v)

# ============================================================ 1.1 Els nombres naturals
s1 = box('def', L('Què són els nombres naturals?', '¿Qué son los números naturales?', 'What are natural numbers?'),
  P(r"Els <strong>nombres naturals</strong> són els que fem servir per a <strong>comptar</strong> (5 caixes, 120 alumnes) i per a <strong>ordenar</strong> (el 3r classificat). El conjunt dels naturals es representa amb la lletra \(\mathbb{N}\):",
    r"Los <strong>números naturales</strong> son los que usamos para <strong>contar</strong> (5 cajas, 120 alumnos) y para <strong>ordenar</strong> (el 3.er clasificado). El conjunto de los naturales se representa con la letra \(\mathbb{N}\):",
    r"<strong>Natural numbers</strong> are the numbers we use to <strong>count</strong> (5 boxes, 120 students) and to <strong>put things in order</strong> (3rd place). The set of natural numbers is written \(\mathbb{N}\):")
  + r'\[\mathbb{N}=\{0,\ 1,\ 2,\ 3,\ 4,\ 5,\ \ldots\}\]'
  + ul(L(r"Comencen en el \(0\) i no s'acaben mai: després de cada natural \(n\) sempre hi ha el <strong>següent</strong>, \(n+1\).",
         r"Empiezan en el \(0\) y no se acaban nunca: después de cada natural \(n\) siempre está el <strong>siguiente</strong>, \(n+1\).",
         r"They start at \(0\) and never end: every natural number \(n\) is followed by the <strong>next</strong> one, \(n+1\)."),
       L(r"Es representen en una semirecta, ordenats de menor a major i separats sempre per la mateixa distància.",
         r"Se representan en una semirrecta, ordenados de menor a mayor y separados siempre por la misma distancia.",
         r"They are shown on a half-line, in increasing order and always the same distance apart."))
  + nline(0, 10, pts=range(0, 11)))
s1 += box('prop', L('Operacions amb nombres naturals', 'Operaciones con números naturales', 'Operations with natural numbers'),
  P(r"Si <strong>sumem</strong> o <strong>multipliquem</strong> dos naturals, el resultat sempre és un natural. En canvi, la resta i la divisió no sempre es poden fer dins de \(\mathbb{N}\):",
    r"Si <strong>sumamos</strong> o <strong>multiplicamos</strong> dos naturales, el resultado siempre es un natural. En cambio, la resta y la división no siempre se pueden hacer dentro de \(\mathbb{N}\):",
    r"If we <strong>add</strong> or <strong>multiply</strong> two natural numbers, the result is always natural. Subtraction and division, however, can't always be done inside \(\mathbb{N}\):")
  + table([L('Operació', 'Operación', 'Operation'), L('Exemple', 'Ejemplo', 'Example'), L('Sempre dona un natural?', '¿Siempre da un natural?', 'Always natural?')],
          [[L('Suma', 'Suma', 'Addition'), r'\(7+5=12\)', '✅'],
           [L('Multiplicació', 'Multiplicación', 'Multiplication'), r'\(7\cdot5=35\)', '✅'],
           [L('Resta', 'Resta', 'Subtraction'), r'\(7-5=2\quad\) ' + L('però', 'pero', 'but') + r' \(\quad5-7=\ ?\)', '❌ ' + L('(ho resoldrem amb els enters)', '(lo resolveremos con los enteros)', '(integers will solve it)')],
           [L('Divisió', 'División', 'Division'), r'\(35:5=7\quad\) ' + L('però', 'pero', 'but') + r' \(\quad 7:5=\ ?\)', '❌ ' + L('(només si és exacta)', '(solo si es exacta)', '(only if exact)')]])
  + P(r"La multiplicació és <strong>distributiva</strong> respecte de la suma i la resta: \(a\cdot(b\pm c)=a\cdot b\pm a\cdot c\). Ens ajuda a calcular de cap i a <strong>traure factor comú</strong>:",
      r"La multiplicación es <strong>distributiva</strong> respecto de la suma y la resta: \(a\cdot(b\pm c)=a\cdot b\pm a\cdot c\). Nos ayuda a calcular de cabeza y a <strong>sacar factor común</strong>:",
      r"Multiplication is <strong>distributive</strong> over addition and subtraction: \(a\cdot(b\pm c)=a\cdot b\pm a\cdot c\). It helps with mental maths and with <strong>taking out a common factor</strong>:")
  + r'\[7\cdot99=7\cdot(100-1)=700-7=693\qquad 12\cdot15+12\cdot5=12\cdot(15+5)=12\cdot20=240\]')
assert 7 * 99 == 693 and 12 * 15 + 12 * 5 == 240
s1 += box('def', L('La divisió entera', 'La división entera', 'Division with remainder'),
  P(r"Quan una divisió no és exacta obtenim un <strong>quocient</strong> \(q\) i un <strong>residu</strong> \(r\), que sempre és menor que el divisor. Es compleix la <strong>prova de la divisió</strong>:",
    r"Cuando una división no es exacta obtenemos un <strong>cociente</strong> \(q\) y un <strong>resto</strong> \(r\), que siempre es menor que el divisor. Se cumple la <strong>prueba de la división</strong>:",
    r"When a division isn't exact we get a <strong>quotient</strong> \(q\) and a <strong>remainder</strong> \(r\), which is always smaller than the divisor. The <strong>division check</strong> holds:")
  + r'\[\underbrace{D}_{\tri{dividend}{dividendo}{dividend}}=\underbrace{d}_{\tri{divisor}{divisor}{divisor}}\cdot\underbrace{q}_{\tri{quocient}{cociente}{quotient}}+\underbrace{r}_{\tri{residu}{resto}{remainder}}\qquad 247=12\cdot20+7\]')
assert 12 * 20 + 7 == 247
s1 += level(1, 1,
  prob(L(r"Un magatzem té 230 ous i els envasa en oueres de 12. Quantes oueres s'omplin? Quants ous sobren?", r"Un almacén tiene 230 huevos y los envasa en hueveras de 12. ¿Cuántas hueveras se llenan? ¿Cuántos huevos sobran?", r"A warehouse has 230 eggs and packs them in boxes of 12. How many boxes are filled? How many eggs are left over?"),
       r'\[230=12\cdot19+2\]',
       P(r"S'omplin \(\boxed{19}\) oueres i sobren \(\boxed{2}\) ous.", r"Se llenan \(\boxed{19}\) hueveras y sobran \(\boxed{2}\) huevos.", r"\(\boxed{19}\) boxes are filled and \(\boxed{2}\) eggs are left over.")))
assert 12 * 19 + 2 == 230
s1 += level(2, 2,
  prob(L(r"Un taller compra 15 rodes a 48 € i 15 cambres a 12 €. Calcula el total de dues maneres diferents.", r"Un taller compra 15 ruedas a 48 € y 15 cámaras a 12 €. Calcula el total de dos maneras distintas.", r"A garage buys 15 tyres at €48 and 15 inner tubes at €12. Work out the total in two different ways."),
       r'\[15\cdot48+15\cdot12=720+180=\boxed{900\text{ €}}\]',
       P(r"Amb la propietat distributiva (factor comú 15) és més ràpid:", r"Con la propiedad distributiva (factor común 15) es más rápido:", r"With the distributive property (common factor 15) it's quicker:"),
       r'\[15\cdot(48+12)=15\cdot60=\boxed{900\text{ €}}\]'))
assert 15 * 48 + 15 * 12 == 900 == 15 * 60
s1 += practice([
  ('★', L(r"a) Calcula el quocient i el residu de \(500:23\) i fes la prova. b) Indica si el resultat és natural: \(9-14\), \(\ 6\cdot8\), \(\ 25:4\).", r"a) Calcula el cociente y el resto de \(500:23\) y haz la prueba. b) Indica si el resultado es natural: \(9-14\), \(\ 6\cdot8\), \(\ 25:4\).", r"a) Find the quotient and remainder of \(500:23\) and check. b) Is the result natural? \(9-14\), \(\ 6\cdot8\), \(\ 25:4\).")),
  ('★★', L(r"c) Calcula de cap: \(25\cdot101\) i \(\ 8\cdot37+8\cdot63\).", r"c) Calcula de cabeza: \(25\cdot101\) y \(\ 8\cdot37+8\cdot63\).", r"c) Work out mentally: \(25\cdot101\) and \(\ 8\cdot37+8\cdot63\)."))],
  P(r"a) \(500=23\cdot21+17\). &nbsp; b) No (\(-5\)); sí (48); no (no és exacta). &nbsp; c) \(2500+25=2525\); \(\ 8\cdot100=800\).", r"a) \(500=23\cdot21+17\). &nbsp; b) No (\(-5\)); sí (48); no (no es exacta). &nbsp; c) \(2500+25=2525\); \(\ 8\cdot100=800\).", r"a) \(500=23\cdot21+17\). &nbsp; b) No (\(-5\)); yes (48); no (not exact). &nbsp; c) \(2500+25=2525\); \(\ 8\cdot100=800\)."))
assert 23 * 21 + 17 == 500 and 25 * 101 == 2525 and 8 * 37 + 8 * 63 == 800

# ============================================================ 1.2 Operacions combinades amb naturals
s2 = box('def', L('Potències de nombres naturals', 'Potencias de números naturales', 'Powers of natural numbers'),
  P(r"Una <strong>potència</strong> és una multiplicació de factors iguals. El factor que es repeteix és la <strong>base</strong> i el nombre de vegades, l'<strong>exponent</strong>:",
    r"Una <strong>potencia</strong> es una multiplicación de factores iguales. El factor que se repite es la <strong>base</strong> y el número de veces, el <strong>exponente</strong>:",
    r"A <strong>power</strong> is a product of equal factors. The repeated factor is the <strong>base</strong> and the number of times is the <strong>exponent</strong>:")
  + r'\[a^n=\underbrace{a\cdot a\cdots a}_{n\ \tri{vegades}{veces}{times}}\qquad 2^5=2\cdot2\cdot2\cdot2\cdot2=32\qquad 10^3=1000\]'
  + ul(L(r"\(a^2\) es llig «\(a\) al <strong>quadrat</strong>» i \(a^3\), «\(a\) al <strong>cub</strong>». A més, \(a^1=a\) i \(a^0=1\).", r"\(a^2\) se lee «\(a\) al <strong>cuadrado</strong>» y \(a^3\), «\(a\) al <strong>cubo</strong>». Además, \(a^1=a\) y \(a^0=1\).", r"\(a^2\) is read “\(a\) <strong>squared</strong>” and \(a^3\), “\(a\) <strong>cubed</strong>”. Also, \(a^1=a\) and \(a^0=1\)."),
       L(r"Compte: \(2^5\neq2\cdot5\). L'exponent no multiplica la base, indica quantes vegades es repeteix.", r"Cuidado: \(2^5\neq2\cdot5\). El exponente no multiplica la base, indica cuántas veces se repite.", r"Careful: \(2^5\neq2\cdot5\). The exponent doesn't multiply the base; it says how many times it repeats.")))
assert 2 ** 5 == 32
s2 += box('def', L('Arrel quadrada', 'Raíz cuadrada', 'Square root'),
  P(r"L'<strong>arrel quadrada</strong> d'un nombre és el nombre que, elevat al quadrat, dona el primer: \(\ \sqrt{a}=b\iff b^2=a\). Per exemple, \(\sqrt{49}=7\) perquè \(7^2=49\).",
    r"La <strong>raíz cuadrada</strong> de un número es el número que, elevado al cuadrado, da el primero: \(\ \sqrt{a}=b\iff b^2=a\). Por ejemplo, \(\sqrt{49}=7\) porque \(7^2=49\).",
    r"The <strong>square root</strong> of a number is the number whose square is the first one: \(\ \sqrt{a}=b\iff b^2=a\). For example, \(\sqrt{49}=7\) because \(7^2=49\).")
  + table([L('Nombre', 'Número', 'Number')] + [str(n) for n in range(1, 13)],
          [[L('Quadrat', 'Cuadrado', 'Square')] + [str(n * n) for n in range(1, 13)]], 'data')
  + ul(L(r"Els nombres de la fila de baix són <strong>quadrats perfectes</strong>: la seua arrel és exacta.", r"Los números de la fila de abajo son <strong>cuadrados perfectos</strong>: su raíz es exacta.", r"The numbers in the bottom row are <strong>perfect squares</strong>: their root is exact."),
       L(r"Si no és un quadrat perfecte, calculem l'<strong>arrel entera</strong>: el nombre més gran el quadrat del qual no supera el radicand. \(\sqrt{50}\approx7\) amb residu \(1\), perquè \(50=7^2+1\).", r"Si no es un cuadrado perfecto, calculamos la <strong>raíz entera</strong>: el mayor número cuyo cuadrado no supera el radicando. \(\sqrt{50}\approx7\) con resto \(1\), porque \(50=7^2+1\).", r"If it isn't a perfect square, we find the <strong>integer root</strong>: the largest number whose square doesn't exceed the radicand. \(\sqrt{50}\approx7\) with remainder \(1\), because \(50=7^2+1\).")))
s2 += W_rootz
s2 += box('prop', L('Jerarquia de les operacions', 'Jerarquía de las operaciones', 'Order of operations'),
  P(r"Quan en una expressió hi ha diverses operacions, les fem sempre en aquest ordre:", r"Cuando en una expresión hay varias operaciones, las hacemos siempre en este orden:", r"When an expression has several operations, always do them in this order:")
  + ol(L("<strong>Parèntesis i claudàtors</strong>, començant pels de dins.", "<strong>Paréntesis y corchetes</strong>, empezando por los de dentro.", "<strong>Brackets</strong>, starting with the innermost."),
       L("<strong>Potències i arrels</strong>.", "<strong>Potencias y raíces</strong>.", "<strong>Powers and roots</strong>."),
       L("<strong>Multiplicacions i divisions</strong>, d'esquerra a dreta.", "<strong>Multiplicaciones y divisiones</strong>, de izquierda a derecha.", "<strong>Multiplication and division</strong>, from left to right."),
       L("<strong>Sumes i restes</strong>, d'esquerra a dreta.", "<strong>Sumas y restas</strong>, de izquierda a derecha.", "<strong>Addition and subtraction</strong>, from left to right."))
  + r'\[20-\underbrace{3^2}_{9}\cdot2+\underbrace{\sqrt{16}}_{4}=20-\underbrace{9\cdot2}_{18}+4=\boxed{6}\]'
  + box('warn', L('Errors freqüents', 'Errores frecuentes', 'Common mistakes'),
        ul(L(r"\(8+2\cdot5=8+10=18\), i no \(10\cdot5=50\): primer la multiplicació.", r"\(8+2\cdot5=8+10=18\), y no \(10\cdot5=50\): primero la multiplicación.", r"\(8+2\cdot5=8+10=18\), not \(10\cdot5=50\): multiplication first."),
           L(r"\(12:2\cdot3=6\cdot3=18\), i no \(12:6=2\): d'esquerra a dreta.", r"\(12:2\cdot3=6\cdot3=18\), y no \(12:6=2\): de izquierda a derecha.", r"\(12:2\cdot3=6\cdot3=18\), not \(12:6=2\): left to right."),
           L(r"\(\sqrt{9+16}=\sqrt{25}=5\), i no \(\sqrt{9}+\sqrt{16}=7\): l'arrel no es reparteix en la suma.", r"\(\sqrt{9+16}=\sqrt{25}=5\), y no \(\sqrt{9}+\sqrt{16}=7\): la raíz no se reparte en la suma.", r"\(\sqrt{9+16}=\sqrt{25}=5\), not \(\sqrt{9}+\sqrt{16}=7\): a root doesn't split over a sum."))))
chk('20-3^2·2+√16', 6); chk('8+2·5', 18); chk('12:2·3', 18); chk('√(9+16)', 5)
s2 += hierz(["20-3^2·2+√16", "(3+4)·5-2^3", "2^3+3^2·2", "√49+2·(8-3)^2", "50-[18:(3^2-6)]·4", "5·√36-2^4:8"])
s2 += drillz('natc', 'Entrena: operacions combinades amb naturals', 'Entrena: operaciones combinadas con naturales', 'Train: mixed operations with natural numbers')
s2 += level(1, 1,
  prob(L(r"Calcula: \(\ 4\cdot(9-5)+2^3\).", r"Calcula: \(\ 4\cdot(9-5)+2^3\).", r"Work out: \(\ 4\cdot(9-5)+2^3\)."),
       r'\[4\cdot4+8=16+8=\boxed{24}\]'))
chk('4·(9-5)+2^3', 24)
s2 += level(2, 2,
  prob(L(r"Calcula: \(\ 50-\left[18:\left(3^2-6\right)\right]\cdot4\).", r"Calcula: \(\ 50-\left[18:\left(3^2-6\right)\right]\cdot4\).", r"Work out: \(\ 50-\left[18:\left(3^2-6\right)\right]\cdot4\)."),
       P(r"Comencem pel parèntesi de dins: \(3^2-6=9-6=3\).", r"Empezamos por el paréntesis de dentro: \(3^2-6=9-6=3\).", r"Start with the innermost brackets: \(3^2-6=9-6=3\)."),
       r'\[50-[18:3]\cdot4=50-6\cdot4=50-24=\boxed{26}\]'),
  prob(L(r"En una botiga comprem 3 samarretes de 12 € i 2 pantalons de 25 €. Paguem amb un bitllet de 100 €. Escriu l'operació en una sola expressió i calcula el canvi.", r"En una tienda compramos 3 camisetas de 12 € y 2 pantalones de 25 €. Pagamos con un billete de 100 €. Escribe la operación en una sola expresión y calcula el cambio.", r"In a shop we buy 3 T-shirts at €12 and 2 pairs of trousers at €25. We pay with a €100 note. Write it as a single expression and work out the change."),
       r'\[100-(3\cdot12+2\cdot25)=100-(36+50)=100-86=\boxed{14\text{ €}}\]'))
chk('50-[18:(3^2-6)]·4', 26); chk('100-(3·12+2·25)', 14)
s2 += level(3, 4,
  prob(L(r"Un alumne ha fet \(\ 6+4\cdot3^2=10\cdot3^2=10\cdot9=90\). Troba l'error i fes-ho bé.", r"Un alumno ha hecho \(\ 6+4\cdot3^2=10\cdot3^2=10\cdot9=90\). Encuentra el error y hazlo bien.", r"A student wrote \(\ 6+4\cdot3^2=10\cdot3^2=10\cdot9=90\). Find the mistake and fix it."),
       P(r"Ha sumat abans de fer la potència i la multiplicació. Correcte:", r"Ha sumado antes de hacer la potencia y la multiplicación. Correcto:", r"They added before doing the power and the multiplication. Correct:"),
       r'\[6+4\cdot\underbrace{3^2}_{9}=6+\underbrace{4\cdot9}_{36}=\boxed{42}\]'),
  prob(L(r"Un terreny quadrat fa 625 m². Quant mesura el costat? Quants metres de tanca calen per a envoltar-lo, si deixem una porta de 3 m?", r"Un terreno cuadrado mide 625 m². ¿Cuánto mide el lado? ¿Cuántos metros de valla hacen falta para rodearlo, si dejamos una puerta de 3 m?", r"A square plot has an area of 625 m². How long is each side? How many metres of fencing are needed to go round it, leaving a 3 m gate?"),
       r'\[\tri{costat}{lado}{side}=\sqrt{625}=\boxed{25\text{ m}}\qquad 4\cdot25-3=100-3=\boxed{97\text{ m}}\]'))
chk('6+4·3^2', 42); chk('√625', 25); chk('4·√625-3', 97)
s2 += practice([
  ('★', L(r"a) Calcula: \(3^4\), \(\ 10^5\), \(\ \sqrt{81}\), \(\ \sqrt{144}\), \(\ 7^0\). b) Arrel entera i residu de 90.", r"a) Calcula: \(3^4\), \(\ 10^5\), \(\ \sqrt{81}\), \(\ \sqrt{144}\), \(\ 7^0\). b) Raíz entera y resto de 90.", r"a) Work out: \(3^4\), \(\ 10^5\), \(\ \sqrt{81}\), \(\ \sqrt{144}\), \(\ 7^0\). b) Integer root and remainder of 90.")),
  ('★★', L(r"c) \(\ 15-2\cdot3+4^2:8\) &nbsp; d) \(\ (15-2)\cdot3+\sqrt{100}\) &nbsp; e) \(\ 2\cdot\left[5^2-(4+3\cdot2)\right]\)", r"c) \(\ 15-2\cdot3+4^2:8\) &nbsp; d) \(\ (15-2)\cdot3+\sqrt{100}\) &nbsp; e) \(\ 2\cdot\left[5^2-(4+3\cdot2)\right]\)", r"c) \(\ 15-2\cdot3+4^2:8\) &nbsp; d) \(\ (15-2)\cdot3+\sqrt{100}\) &nbsp; e) \(\ 2\cdot\left[5^2-(4+3\cdot2)\right]\)"))],
  P(r"a) \(81\), \(100\,000\), \(9\), \(12\), \(1\). b) \(9\), residu \(9\) (\(90=9^2+9\)). &nbsp; c) \(15-6+2=11\) &nbsp; d) \(39+10=49\) &nbsp; e) \(2\cdot[25-10]=30\)", r"a) \(81\), \(100\,000\), \(9\), \(12\), \(1\). b) \(9\), resto \(9\) (\(90=9^2+9\)). &nbsp; c) \(15-6+2=11\) &nbsp; d) \(39+10=49\) &nbsp; e) \(2\cdot[25-10]=30\)", r"a) \(81\), \(100\,000\), \(9\), \(12\), \(1\). b) \(9\), remainder \(9\) (\(90=9^2+9\)). &nbsp; c) \(15-6+2=11\) &nbsp; d) \(39+10=49\) &nbsp; e) \(2\cdot[25-10]=30\)"))
chk('15-2·3+4^2:8', 11); chk('(15-2)·3+√100', 49); chk('2·[5^2-(4+3·2)]', 30); assert 9 ** 2 + 9 == 90

# ============================================================ 1.3 Els nombres enters
s3 = box('def', L('Què són els nombres enters?', '¿Qué son los números enteros?', 'What are integers?'),
  P(r"Amb els naturals no podem expressar una temperatura <strong>baix zero</strong>, un <strong>soterrani</strong>, un <strong>deute</strong> o una <strong>profunditat</strong>, ni fer restes com \(3-5\). Per a això fem servir els <strong>nombres enters</strong>: els naturals amb signe positiu, els seus oposats amb signe negatiu i el zero:",
    r"Con los naturales no podemos expresar una temperatura <strong>bajo cero</strong>, un <strong>sótano</strong>, una <strong>deuda</strong> o una <strong>profundidad</strong>, ni hacer restas como \(3-5\). Para ello usamos los <strong>números enteros</strong>: los naturales con signo positivo, sus opuestos con signo negativo y el cero:",
    r"Natural numbers can't express a temperature <strong>below zero</strong>, a <strong>basement</strong>, a <strong>debt</strong> or a <strong>depth</strong>, nor subtractions like \(3-5\). For this we use <strong>integers</strong>: the natural numbers with a positive sign, their opposites with a negative sign, and zero:")
  + r'\[\mathbb{Z}=\{\,\ldots,\ -3,\ -2,\ -1,\ 0,\ +1,\ +2,\ +3,\ \ldots\}\qquad \mathbb{N}\subset\mathbb{Z}\]'
  + P(r"El signe \(+\) dels positius es pot ometre (\(+7=7\)); el signe \(-\) dels negatius s'ha d'escriure sempre. El \(0\) no és ni positiu ni negatiu.", r"El signo \(+\) de los positivos se puede omitir (\(+7=7\)); el signo \(-\) de los negativos se tiene que escribir siempre. El \(0\) no es ni positivo ni negativo.", r"The \(+\) sign of positives can be left out (\(+7=7\)); the \(-\) sign of negatives must always be written. \(0\) is neither positive nor negative."))
s3 += W_ctx
s3 += box('def', L('Recta numèrica i ordre', 'Recta numérica y orden', 'Number line and order'),
  P(r"Els enters es representen en una recta: el \(0\) al centre, els positius a la dreta i els negatius a l'esquerra. <strong>Com més a la dreta, més gran</strong>: qualsevol positiu és major que qualsevol negatiu i, entre dos negatius, és més gran el que està més a prop del 0.",
    r"Los enteros se representan en una recta: el \(0\) en el centro, los positivos a la derecha y los negativos a la izquierda. <strong>Cuanto más a la derecha, mayor</strong>: cualquier positivo es mayor que cualquier negativo y, entre dos negativos, es mayor el que está más cerca del 0.",
    r"Integers are shown on a line: \(0\) in the middle, positives to the right and negatives to the left. <strong>The further right, the larger</strong>: every positive is larger than every negative and, of two negatives, the one closer to 0 is larger.")
  + nline(-6, 6, pts=(-5, -2, 3)) + r'\[-5<-2<0<3\]')
s3 += W_line + drillz('ord', 'Entrena: ordre', 'Entrena: orden', 'Train: order')
s3 += box('def', L('Valor absolut i oposat', 'Valor absoluto y opuesto', 'Absolute value and opposite'),
  ul(L(r"El <strong>valor absolut</strong> d'un enter, \(|a|\), és la seua <strong>distància al 0</strong>. És el nombre sense el signe i mai no és negatiu: \(\ |-7|=7\), \(\ |+4|=4\), \(\ |0|=0\).", r"El <strong>valor absoluto</strong> de un entero, \(|a|\), es su <strong>distancia al 0</strong>. Es el número sin el signo y nunca es negativo: \(\ |-7|=7\), \(\ |+4|=4\), \(\ |0|=0\).", r"The <strong>absolute value</strong> of an integer, \(|a|\), is its <strong>distance from 0</strong>. It's the number without its sign and is never negative: \(\ |-7|=7\), \(\ |+4|=4\), \(\ |0|=0\)."),
     L(r"L'<strong>oposat</strong> d'un enter té el mateix valor absolut i el signe contrari: \(\text{op}(-7)=7\), \(\ \text{op}(4)=-4\). L'oposat de \(a\) s'escriu \(-a\).", r"El <strong>opuesto</strong> de un entero tiene el mismo valor absoluto y el signo contrario: \(\text{op}(-7)=7\), \(\ \text{op}(4)=-4\). El opuesto de \(a\) se escribe \(-a\).", r"The <strong>opposite</strong> of an integer has the same absolute value and the other sign: \(\text{op}(-7)=7\), \(\ \text{op}(4)=-4\). The opposite of \(a\) is written \(-a\)."),
     L(r"Dos nombres oposats estan a la mateixa distància del 0, un a cada costat. Per exemple, \(-5\) i \(5\) són els dos enters amb \(|x|=5\).", r"Dos números opuestos están a la misma distancia del 0, uno a cada lado. Por ejemplo, \(-5\) y \(5\) son los dos enteros con \(|x|=5\).", r"Two opposite numbers are the same distance from 0, one on each side. For example, \(-5\) and \(5\) are the two integers with \(|x|=5\).")))
s3 += W_abs + drillz('abs', 'Entrena: valor absolut i oposat', 'Entrena: valor absoluto y opuesto', 'Train: absolute value and opposite')
s3 += level(1, 1,
  prob(L(r"Expressa amb un enter: a) 8 graus baix zero; b) el 2n soterrani; c) un deute de 350 €; d) un pis 5a planta; e) una fossa a 1200 m de profunditat.", r"Expresa con un entero: a) 8 grados bajo cero; b) el 2.º sótano; c) una deuda de 350 €; d) un piso 5.ª planta; e) una fosa a 1200 m de profundidad.", r"Write as an integer: a) 8 degrees below zero; b) the 2nd basement; c) a €350 debt; d) a flat on the 5th floor; e) a trench 1200 m deep."),
       r'\[\text{a) }-8\qquad\text{b) }-2\qquad\text{c) }-350\qquad\text{d) }+5\qquad\text{e) }-1200\]'),
  prob(L(r"Ordena de menor a major: \(\ -3,\ 5,\ -8,\ 0,\ 2,\ -1,\ -12,\ 7\).", r"Ordena de menor a mayor: \(\ -3,\ 5,\ -8,\ 0,\ 2,\ -1,\ -12,\ 7\).", r"Put in increasing order: \(\ -3,\ 5,\ -8,\ 0,\ 2,\ -1,\ -12,\ 7\)."),
       r'\[-12<-8<-3<-1<0<2<5<7\]'))
assert sorted([-3, 5, -8, 0, 2, -1, -12, 7]) == [-12, -8, -3, -1, 0, 2, 5, 7]
s3 += level(2, 3,
  prob(L(r"Calcula: a) \(|-9|+|4|\); b) \(|-9+4|\); c) \(\text{op}(|-6|)\). Escriu tots els enters \(x\) que compleixen d) \(|x|=3\) i e) \(|x|<3\).", r"Calcula: a) \(|-9|+|4|\); b) \(|-9+4|\); c) \(\text{op}(|-6|)\). Escribe todos los enteros \(x\) que cumplen d) \(|x|=3\) y e) \(|x|<3\).", r"Work out: a) \(|-9|+|4|\); b) \(|-9+4|\); c) \(\text{op}(|-6|)\). Write all the integers \(x\) such that d) \(|x|=3\) and e) \(|x|<3\)."),
       r'\[\text{a) }9+4=\boxed{13}\qquad\text{b) }|-5|=\boxed{5}\qquad\text{c) }\text{op}(6)=\boxed{-6}\]',
       r'\[\text{d) }\boxed{-3\ \tri{i}{y}{and}\ 3}\qquad\text{e) }\boxed{-2,\,-1,\,0,\,1,\,2}\]'))

# ============================================================ 1.4 Operacions amb enters
s4 = box('def', L("Suma i resta d'enters", 'Suma y resta de enteros', 'Adding and subtracting integers'),
  ul(L(r"<strong>Mateix signe:</strong> sumem els valors absoluts i posem el signe comú: \(\ (-7)+(-5)=-12\), \(\ 4+9=13\).", r"<strong>Mismo signo:</strong> sumamos los valores absolutos y ponemos el signo común: \(\ (-7)+(-5)=-12\), \(\ 4+9=13\).", r"<strong>Same sign:</strong> add the absolute values and keep the common sign: \(\ (-7)+(-5)=-12\), \(\ 4+9=13\)."),
     L(r"<strong>Signe diferent:</strong> restem els valors absoluts (el major menys el menor) i posem el signe del que té <strong>major valor absolut</strong>: \(\ (-9)+4=-5\), \(\ 12+(-7)=5\).", r"<strong>Signo distinto:</strong> restamos los valores absolutos (el mayor menos el menor) y ponemos el signo del que tiene <strong>mayor valor absoluto</strong>: \(\ (-9)+4=-5\), \(\ 12+(-7)=5\).", r"<strong>Different signs:</strong> subtract the absolute values (larger minus smaller) and use the sign of the one with the <strong>larger absolute value</strong>: \(\ (-9)+4=-5\), \(\ 12+(-7)=5\)."))
  + box('prop', L("Restar és sumar l'oposat", 'Restar es sumar el opuesto', 'Subtracting is adding the opposite'),
        r'\[a-b=a+(-b)\qquad 8-13=8+(-13)=-5\qquad (-6)-(-10)=-6+10=4\]'))
s4 += W_add + drillz('add', 'Entrena: sumes i restes', 'Entrena: sumas y restas', 'Train: adding and subtracting')
s4 += box('def', L('Llevar parèntesis', 'Quitar paréntesis', 'Removing brackets'),
  ul(L(r"Un parèntesi precedit de \(+\) es lleva sense canviar res: \(\ +(-3)=-3\), \(\ +(5-2)=5-2\).", r"Un paréntesis precedido de \(+\) se quita sin cambiar nada: \(\ +(-3)=-3\), \(\ +(5-2)=5-2\).", r"Brackets preceded by \(+\) are removed without changing anything: \(\ +(-3)=-3\), \(\ +(5-2)=5-2\)."),
     L(r"Un parèntesi precedit de \(-\) es lleva <strong>canviant el signe</strong> de tots els termes de dins: \(\ -(-3)=+3\), \(\ -(5-2)=-5+2\).", r"Un paréntesis precedido de \(-\) se quita <strong>cambiando el signo</strong> de todos los términos de dentro: \(\ -(-3)=+3\), \(\ -(5-2)=-5+2\).", r"Brackets preceded by \(-\) are removed by <strong>changing the sign</strong> of every term inside: \(\ -(-3)=+3\), \(\ -(5-2)=-5+2\)."),
     L(r"Amb moltes sumes i restes és còmode <strong>agrupar</strong> positius i negatius: \(\ 5-8+3-7+2=(5+3+2)-(8+7)=10-15=-5\).", r"Con muchas sumas y restas es cómodo <strong>agrupar</strong> positivos y negativos: \(\ 5-8+3-7+2=(5+3+2)-(8+7)=10-15=-5\).", r"With many additions and subtractions it helps to <strong>group</strong> positives and negatives: \(\ 5-8+3-7+2=(5+3+2)-(8+7)=10-15=-5\).")))
chk('5-8+3-7+2', -5)
s4 += W_par + drillz('par', 'Entrena: parèntesis', 'Entrena: paréntesis', 'Train: brackets')
s4 += box('def', L('Multiplicació i divisió: la regla dels signes', 'Multiplicación y división: la regla de los signos', 'Multiplication and division: the sign rule'),
  P(r"Multipliquem (o dividim) els valors absoluts i el signe del resultat el decidim així:", r"Multiplicamos (o dividimos) los valores absolutos y el signo del resultado lo decidimos así:", r"Multiply (or divide) the absolute values; the sign of the result is decided like this:")
  + SGT
  + r'\[(-6)\cdot(-4)=24\qquad 7\cdot(-8)=-56\qquad (-45):9=-5\qquad (-56):(-7)=8\]'
  + note(r"Amb diversos factors, el resultat és positiu si hi ha un nombre <strong>parell</strong> de factors negatius i negatiu si n'hi ha un nombre <strong>senar</strong>: \((-2)\cdot(-3)\cdot(-5)=-30\).", r"Con varios factores, el resultado es positivo si hay un número <strong>par</strong> de factores negativos y negativo si hay un número <strong>impar</strong>: \((-2)\cdot(-3)\cdot(-5)=-30\).", r"With several factors, the result is positive if there is an <strong>even</strong> number of negative factors and negative if there is an <strong>odd</strong> number: \((-2)\cdot(-3)\cdot(-5)=-30\)."))
s4 += W_sign + drillz('mul', 'Entrena: multiplicació i divisió', 'Entrena: multiplicación y división', 'Train: multiplying and dividing')
s4 += box('prop', L('Operacions combinades amb enters', 'Operaciones combinadas con enteros', 'Mixed operations with integers'),
  P(r"Seguim la mateixa <strong>jerarquia</strong> que amb els naturals (parèntesis → potències i arrels → \(\cdot\) i \(:\) → \(+\) i \(-\)) i apliquem en cada pas les regles dels signes:",
    r"Seguimos la misma <strong>jerarquía</strong> que con los naturales (paréntesis → potencias y raíces → \(\cdot\) y \(:\) → \(+\) y \(-\)) y aplicamos en cada paso las reglas de los signos:",
    r"Follow the same <strong>order of operations</strong> as with natural numbers (brackets → powers and roots → \(\cdot\) and \(:\) → \(+\) and \(-\)) and apply the sign rules at each step:")
  + r'\[18:(-3)+2\cdot(-5)=-6+(-10)=\boxed{-16}\]'
  + note(r"Escriu entre parèntesis els nombres negatius que van darrere d'un signe d'operació: \(5\cdot(-2)\), i no \(5\cdot-2\).", r"Escribe entre paréntesis los números negativos que van detrás de un signo de operación: \(5\cdot(-2)\), y no \(5\cdot-2\).", r"Put negative numbers in brackets when they follow an operation sign: \(5\cdot(-2)\), not \(5\cdot-2\).", '⚠️'))
chk('18:(-3)+2·(-5)', -16)
s4 += hierz(["18:(-3)+2·(-5)", "4-2·[3-(6-10)]", "-20:4·(-2)", "(-3)·(2-7)+15:(-5)", "-6-[4-3·(2-5)]", "25:(-5)-(-3)·(4-6):2"])
s4 += drillz('comb', 'Entrena: operacions combinades amb enters', 'Entrena: operaciones combinadas con enteros', 'Train: mixed operations with integers')
s4 += level(1, 1,
  prob(L(r"A les 7 del matí el termòmetre marcava \(-4\) °C i a migdia, \(9\) °C. Quants graus ha pujat la temperatura?", r"A las 7 de la mañana el termómetro marcaba \(-4\) °C y a mediodía, \(9\) °C. ¿Cuántos grados ha subido la temperatura?", r"At 7 a.m. the thermometer read \(-4\) °C and at midday \(9\) °C. How many degrees did the temperature rise?"),
       r'\[9-(-4)=9+4=\boxed{13\ °\text{C}}\]'),
  prob(L(r"Calcula: \(\ 7-(3-5+2)\ \) i \(\ (-2)\cdot(+5)\cdot(-3)\).", r"Calcula: \(\ 7-(3-5+2)\ \) y \(\ (-2)\cdot(+5)\cdot(-3)\).", r"Work out: \(\ 7-(3-5+2)\ \) and \(\ (-2)\cdot(+5)\cdot(-3)\)."),
       r'\[7-3+5-2=\boxed{7}\qquad (-10)\cdot(-3)=\boxed{30}\]'))
chk('7-(3-5+2)', 7); chk('(-2)·5·(-3)', 30)
s4 += level(2, 3,
  prob(L(r"Calcula: \(\ -6-\left[4-3\cdot(2-5)\right]\).", r"Calcula: \(\ -6-\left[4-3\cdot(2-5)\right]\).", r"Work out: \(\ -6-\left[4-3\cdot(2-5)\right]\)."),
       r'\[-6-[4-3\cdot(-3)]=-6-[4+9]=-6-13=\boxed{-19}\]'),
  prob(L(r"Un compte té un saldo de 230 €. Es paguen 3 rebuts de 85 € i després es cobra una nòmina de 120 €. Quin és el saldo final? Ha arribat a estar en negatiu?", r"Una cuenta tiene un saldo de 230 €. Se pagan 3 recibos de 85 € y después se cobra una nómina de 120 €. ¿Cuál es el saldo final? ¿Ha llegado a estar en negativo?", r"An account has a balance of €230. Three €85 bills are paid and then a €120 payslip comes in. What is the final balance? Did it go negative?"),
       r'\[230-3\cdot85+120=230-255+120=\boxed{95\text{ €}}\]',
       P(r"Sí: després de pagar els rebuts el saldo era \(230-255=-25\) €.", r"Sí: después de pagar los recibos el saldo era \(230-255=-25\) €.", r"Yes: after paying the bills the balance was \(230-255=-25\) €.")))
chk('-6-[4-3·(2-5)]', -19); chk('230-3·85+120', 95)
s4 += level(3, 5,
  prob(L(r"Un ascensor és a la planta 3. Baixa 5 plantes, puja 2, baixa 4 i, finalment, puja 7. A quina planta para? Quantes plantes ha recorregut en total?", r"Un ascensor está en la planta 3. Baja 5 plantas, sube 2, baja 4 y, finalmente, sube 7. ¿En qué planta para? ¿Cuántas plantas ha recorrido en total?", r"A lift is on floor 3. It goes down 5 floors, up 2, down 4 and finally up 7. Which floor does it stop at? How many floors has it travelled in total?"),
       r'\[3-5+2-4+7=(3+2+7)-(5+4)=12-9=\boxed{3}\]',
       P(r"Torna a la planta 3. Per a la distància sumem els valors absoluts dels moviments: \(5+2+4+7=\boxed{18}\) plantes.", r"Vuelve a la planta 3. Para la distancia sumamos los valores absolutos de los movimientos: \(5+2+4+7=\boxed{18}\) plantas.", r"It's back on floor 3. For the distance, add the absolute values of the moves: \(5+2+4+7=\boxed{18}\) floors.")))
chk('3-5+2-4+7', 3)
s4 += practice([
  ('★', L(r"a) \(\ -8+3\) &nbsp; b) \(\ -4-9\) &nbsp; c) \(\ 6-(-2)\) &nbsp; d) \(\ (-7)\cdot(-6)\) &nbsp; e) \(\ (-63):9\)", r"a) \(\ -8+3\) &nbsp; b) \(\ -4-9\) &nbsp; c) \(\ 6-(-2)\) &nbsp; d) \(\ (-7)\cdot(-6)\) &nbsp; e) \(\ (-63):9\)", r"a) \(\ -8+3\) &nbsp; b) \(\ -4-9\) &nbsp; c) \(\ 6-(-2)\) &nbsp; d) \(\ (-7)\cdot(-6)\) &nbsp; e) \(\ (-63):9\)")),
  ('★★', L(r"f) \(\ 12-25+3-8-(-6)\) &nbsp; g) \(\ (-3)\cdot(2-7)+15:(-5)\)", r"f) \(\ 12-25+3-8-(-6)\) &nbsp; g) \(\ (-3)\cdot(2-7)+15:(-5)\)", r"f) \(\ 12-25+3-8-(-6)\) &nbsp; g) \(\ (-3)\cdot(2-7)+15:(-5)\)")),
  ('★★★', L(r"h) \(\ 10-[3-(5-8)]\cdot(-2)\) &nbsp; i) Un submarí és a \(-120\) m, puja 45 m i després baixa el doble del que ha pujat. On és ara?", r"h) \(\ 10-[3-(5-8)]\cdot(-2)\) &nbsp; i) Un submarino está a \(-120\) m, sube 45 m y después baja el doble de lo que ha subido. ¿Dónde está ahora?", r"h) \(\ 10-[3-(5-8)]\cdot(-2)\) &nbsp; i) A submarine is at \(-120\) m, rises 45 m and then goes down twice as much as it rose. Where is it now?"))],
  P(r"a) \(-5\) &nbsp; b) \(-13\) &nbsp; c) \(8\) &nbsp; d) \(42\) &nbsp; e) \(-7\) &nbsp; f) \(-12\) &nbsp; g) \(15-3=12\) &nbsp; h) \(10-6\cdot(-2)=22\) &nbsp; i) \(-120+45-90=-165\) m", r"a) \(-5\) &nbsp; b) \(-13\) &nbsp; c) \(8\) &nbsp; d) \(42\) &nbsp; e) \(-7\) &nbsp; f) \(-12\) &nbsp; g) \(15-3=12\) &nbsp; h) \(10-6\cdot(-2)=22\) &nbsp; i) \(-120+45-90=-165\) m", r"a) \(-5\) &nbsp; b) \(-13\) &nbsp; c) \(8\) &nbsp; d) \(42\) &nbsp; e) \(-7\) &nbsp; f) \(-12\) &nbsp; g) \(15-3=12\) &nbsp; h) \(10-6\cdot(-2)=22\) &nbsp; i) \(-120+45-90=-165\) m"))
chk('-8+3', -5); chk('-4-9', -13); chk('6-(-2)', 8); chk('(-7)·(-6)', 42); chk('(-63):9', -7); chk('12-25+3-8-(-6)', -12)
chk('(-3)·(2-7)+15:(-5)', 12); chk('10-[3-(5-8)]·(-2)', 22); chk('-120+45-2·45', -165)
