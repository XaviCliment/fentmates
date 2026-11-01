# Apartats 5.1-5.5 (nombres decimals) dels apunts de la Unitat 5 de 1r ESO.
from comu import *

def gseg(g, pairs, on):
    return f'<div class="seg" role="group" data-g="{g}">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'

PV = [('C', 'centenes', 'centenas', 'hundreds'), ('D', 'desenes', 'decenas', 'tens'), ('U', 'unitats', 'unidades', 'units'),
      ('d', 'dècimes', 'décimas', 'tenths'), ('c', 'centèsimes', 'centésimas', 'hundredths'), ('m', 'mil·lèsimes', 'milésimas', 'thousandths')]

# ============================================================ 5.1
s1 = box('def', L('Què és un nombre decimal?', '¿Qué es un número decimal?', 'What is a decimal number?'),
  P(r"Els <strong>nombres decimals</strong> ens permeten expressar quantitats que no són senceres: un preu de \(2\dc35\) €, una altura de \(1\dc68\) m, una temperatura de \(36\dc6\) °C… Tenen dues parts separades per una <strong>coma</strong>:",
    r"Los <strong>números decimales</strong> nos permiten expresar cantidades que no son enteras: un precio de \(2\dc35\) €, una altura de \(1\dc68\) m, una temperatura de \(36\dc6\) °C… Tienen dos partes separadas por una <strong>coma</strong>:",
    r"<strong>Decimal numbers</strong> let us write amounts that aren't whole: a price of \(2\dc35\) €, a height of \(1\dc68\) m, a temperature of \(36\dc6\) °C… They have two parts separated by a <strong>decimal comma</strong> (in English-speaking countries, a point: 2.35):")
  + r'<div class="decparts"><span class="dp-i">245</span><span class="dp-c">,</span><span class="dp-f">378</span></div>'
  + ul(L("A l'esquerra de la coma hi ha la <strong>part entera</strong> (245).", "A la izquierda de la coma está la <strong>parte entera</strong> (245).", "To the left of the comma is the <strong>whole-number part</strong> (245)."),
       L("A la dreta de la coma hi ha la <strong>part decimal</strong> (378): és un tros d'unitat, menys que 1.", "A la derecha de la coma está la <strong>parte decimal</strong> (378): es un trozo de unidad, menos que 1.", "To the right is the <strong>decimal part</strong> (378): a piece of a unit, less than 1.")))
s1 += box('prop', L('Les unitats decimals', 'Las unidades decimales', 'Decimal units'),
  P(r"Si dividim la unitat en 10 parts iguals, cada part és una <strong>dècima</strong>; si la dividim en 100, una <strong>centèsima</strong>; i si la dividim en 1000, una <strong>mil·lèsima</strong>:",
    r"Si dividimos la unidad en 10 partes iguales, cada parte es una <strong>décima</strong>; si la dividimos en 100, una <strong>centésima</strong>; y si la dividimos en 1000, una <strong>milésima</strong>:",
    r"If we split one unit into 10 equal parts, each part is a <strong>tenth</strong>; into 100, a <strong>hundredth</strong>; and into 1000, a <strong>thousandth</strong>:")
  + r'\[1\ \tri{dècima}{décima}{tenth}=0\dc1=\frac{1}{10}\qquad 1\ \tri{centèsima}{centésima}{hundredth}=0\dc01=\frac{1}{100}\qquad 1\ \tri{mil·lèsima}{milésima}{thousandth}=0\dc001=\frac{1}{1000}\]'
  + r'\[1\ \tri{unitat}{unidad}{unit}=10\ \tri{dècimes}{décimas}{tenths}=100\ \tri{centèsimes}{centésimas}{hundredths}=1000\ \tri{mil·lèsimes}{milésimas}{thousandths}\]'
  + figs((svg_tenths(3), r'\(0\dc3\) = 3 ' + L('dècimes', 'décimas', 'tenths')), (svg_hund(27), r'\(0\dc27\) = 27 ' + L('centèsimes', 'centésimas', 'hundredths')), (svg_hund(100), r'\(1=100\) ' + L('centèsimes', 'centésimas', 'hundredths')))
  + note(r"Fixa't que \(0\dc27\) són 2 columnes (2 dècimes) i 7 quadradets (7 centèsimes): \(0\dc27=0\dc2+0\dc07\).",
         r"Fíjate en que \(0\dc27\) son 2 columnas (2 décimas) y 7 cuadraditos (7 centésimas): \(0\dc27=0\dc2+0\dc07\).",
         r"Notice that \(0\dc27\) is 2 columns (2 tenths) and 7 small squares (7 hundredths): \(0\dc27=0\dc2+0\dc07\)."))
s1 += sub('Valor de posició, lectura i descomposició', 'Valor de posición, lectura y descomposición', 'Place value, reading and expanded form')
s1 += box('def', L('Cada xifra val segons el lloc que ocupa', 'Cada cifra vale según el lugar que ocupa', 'Each digit is worth what its place says'),
  table([L(a, a, a) + '<br><small>' + L(va, es, en) + '</small>' for a, va, es, en in PV], [['2', '4', '5', '3', '7', '8']], 'data pv')
  + P(r"<strong>Lectura.</strong> Llegim la part entera, la paraula <em>unitats</em> i després la part decimal amb el nom de l'<strong>última</strong> xifra: \(245\dc378\) es llig «245 unitats i 378 mil·lèsimes». També és correcte dir «245 coma 378».",
      r"<strong>Lectura.</strong> Leemos la parte entera, la palabra <em>unidades</em> y después la parte decimal con el nombre de la <strong>última</strong> cifra: \(245\dc378\) se lee «245 unidades y 378 milésimas». También es correcto decir «245 coma 378».",
      r"<strong>Reading.</strong> Read the whole part, the word <em>units</em>, and then the decimal part with the name of the <strong>last</strong> digit's place: \(245\dc378\) is “245 units and 378 thousandths”. You can also say “245 point 378”.")
  + P(r"<strong>Descomposició.</strong> Sumem el valor de cada xifra:", r"<strong>Descomposición.</strong> Sumamos el valor de cada cifra:", r"<strong>Expanded form.</strong> Add up the value of each digit:")
  + r'\[245\dc378=200+40+5+0\dc3+0\dc07+0\dc008\]'
  + note(r"Afegir zeros a la <strong>dreta</strong> de la part decimal no canvia el nombre: \(2\dc5=2\dc50=2\dc500\) (5 dècimes = 50 centèsimes). En canvi, \(2\dc05\neq2\dc5\).",
         r"Añadir ceros a la <strong>derecha</strong> de la parte decimal no cambia el número: \(2\dc5=2\dc50=2\dc500\) (5 décimas = 50 centésimas). En cambio, \(2\dc05\neq2\dc5\).",
         r"Adding zeros on the <strong>right</strong> of the decimal part doesn't change the number: \(2\dc5=2\dc50=2\dc500\) (5 tenths = 50 hundredths). But \(2\dc05\neq2\dc5\)."))
s1 += widget('w-place', '🔢', L('Taula de valor posicional', 'Tabla de valor posicional', 'Place-value table'),
  f'  <div class="wrow">{nin("x", "Nombre decimal", "Número decimal", "Decimal number", "245,378", "m")}</div>\n'
  + '  ' + quick([('245,378', '245,378'), ('3,05', '3,05'), ('0,7', '0,7'), ('12,006', '12,006'), ('0,035', '0,035'), ('1,5', '1,5'), ('1,50', '1,50')]) + '\n')
s1 += level(1, 1,
  prob(L(r"Escriu com es llegeixen: a) \(7\dc25\) &nbsp; b) \(0\dc408\) &nbsp; c) \(12\dc06\)", r"Escribe cómo se leen: a) \(7\dc25\) &nbsp; b) \(0\dc408\) &nbsp; c) \(12\dc06\)", r"Write how to read them: a) \(7\dc25\) &nbsp; b) \(0\dc408\) &nbsp; c) \(12\dc06\)"),
       P(r"Mirem el lloc de l'última xifra: en a) i c) són centèsimes; en b), mil·lèsimes.", r"Miramos el lugar de la última cifra: en a) y c) son centésimas; en b), milésimas.", r"Look at the place of the last digit: in a) and c) it's hundredths; in b), thousandths."),
       ul(L("a) 7 unitats i 25 centèsimes.", "a) 7 unidades y 25 centésimas.", "a) 7 units and 25 hundredths."),
          L("b) 408 mil·lèsimes (no hi ha part entera).", "b) 408 milésimas (no hay parte entera).", "b) 408 thousandths (there's no whole part)."),
          L("c) 12 unitats i 6 centèsimes. Compte: el 0 ens diu que no hi ha dècimes.", "c) 12 unidades y 6 centésimas. Cuidado: el 0 nos dice que no hay décimas.", "c) 12 units and 6 hundredths. Careful: the 0 tells us there are no tenths."))))
s1 += level(2, 2,
  prob(L("Escriu amb xifres: a) tres unitats i quaranta-cinc mil·lèsimes &nbsp; b) dotze centèsimes &nbsp; c) vint unitats i nou dècimes", "Escribe con cifras: a) tres unidades y cuarenta y cinco milésimas &nbsp; b) doce centésimas &nbsp; c) veinte unidades y nueve décimas", "Write in figures: a) three units and forty-five thousandths &nbsp; b) twelve hundredths &nbsp; c) twenty units and nine tenths"),
       P(r"Les mil·lèsimes ocupen 3 llocs després de la coma; les centèsimes, 2; les dècimes, 1. Omplim amb zeros els llocs buits:", r"Las milésimas ocupan 3 lugares después de la coma; las centésimas, 2; las décimas, 1. Rellenamos con ceros los huecos:", r"Thousandths take 3 places after the comma; hundredths, 2; tenths, 1. Fill the gaps with zeros:"),
       r'\[\text{a) }\boxed{3\dc045}\qquad\text{b) }\boxed{0\dc12}\qquad\text{c) }\boxed{20\dc9}\]'))
s1 += level(3, 3,
  prob(L(r"Descompon \(30\dc705\) i indica quant valen el 7 i el 5.", r"Descompón \(30\dc705\) e indica cuánto valen el 7 y el 5.", r"Write \(30\dc705\) in expanded form and say what the 7 and the 5 are worth."),
       r'\[30\dc705=30+0\dc7+0\dc005\]',
       P(r"El 7 és a les dècimes: val \(0\dc7\). El 5 és a les mil·lèsimes: val \(0\dc005\). Els zeros indiquen que no hi ha unitats ni centèsimes.", r"El 7 está en las décimas: vale \(0\dc7\). El 5 está en las milésimas: vale \(0\dc005\). Los ceros indican que no hay unidades ni centésimas.", r"The 7 is in the tenths: it's worth \(0\dc7\). The 5 is in the thousandths: it's worth \(0\dc005\). The zeros mean there are no units and no hundredths.")))
s1 += practice([
  ('★', L(r"a) Com es llig \(4\dc07\)? b) Quantes centèsimes hi ha en una unitat? I en una dècima?", r"a) ¿Cómo se lee \(4\dc07\)? b) ¿Cuántas centésimas hay en una unidad? ¿Y en una décima?", r"a) How do you read \(4\dc07\)? b) How many hundredths are there in one unit? And in one tenth?")),
  ('★★', L(r"c) Escriu amb xifres: sis unitats i tres mil·lèsimes. d) Quin valor té el 8 en \(0\dc183\)?", r"c) Escribe con cifras: seis unidades y tres milésimas. d) ¿Qué valor tiene el 8 en \(0\dc183\)?", r"c) Write in figures: six units and three thousandths. d) What is the 8 worth in \(0\dc183\)?")),
  ('★★★', L(r"e) Escriu el nombre format per 5 desenes, 2 dècimes i 9 mil·lèsimes. f) Són iguals \(3\dc4\), \(3\dc40\) i \(3\dc04\)?", r"e) Escribe el número formado por 5 decenas, 2 décimas y 9 milésimas. f) ¿Son iguales \(3\dc4\), \(3\dc40\) y \(3\dc04\)?", r"e) Write the number made of 5 tens, 2 tenths and 9 thousandths. f) Are \(3\dc4\), \(3\dc40\) and \(3\dc04\) equal?"))],
  P(r"a) 4 unitats i 7 centèsimes. &nbsp; b) 100 centèsimes; 10 centèsimes.", r"a) 4 unidades y 7 centésimas. &nbsp; b) 100 centésimas; 10 centésimas.", r"a) 4 units and 7 hundredths. &nbsp; b) 100 hundredths; 10 hundredths.")
  + P(r"c) \(6\dc003\). &nbsp; d) 8 centèsimes \(=0\dc08\).", r"c) \(6\dc003\). &nbsp; d) 8 centésimas \(=0\dc08\).", r"c) \(6\dc003\). &nbsp; d) 8 hundredths \(=0\dc08\).")
  + P(r"e) \(50\dc209\). &nbsp; f) \(3\dc4=3\dc40\), però \(3\dc04\) és diferent (4 centèsimes, no 4 dècimes).", r"e) \(50\dc209\). &nbsp; f) \(3\dc4=3\dc40\), pero \(3\dc04\) es distinto (4 centésimas, no 4 décimas).", r"e) \(50\dc209\). &nbsp; f) \(3\dc4=3\dc40\), but \(3\dc04\) is different (4 hundredths, not 4 tenths)."))

# ============================================================ 5.2
s2 = box('prop', L('Com comparem dos decimals', 'Cómo comparamos dos decimales', 'How to compare two decimals'),
  ol(L("Comparem la <strong>part entera</strong>: és més gran el que la té més gran. &nbsp; \\(12\\dc3>9\\dc87\\)", "Comparamos la <strong>parte entera</strong>: es mayor el que la tiene mayor. &nbsp; \\(12\\dc3>9\\dc87\\)", "Compare the <strong>whole parts</strong>: the bigger one wins. &nbsp; \\(12\\dc3>9\\dc87\\)"),
     L("Si són iguals, comparem les <strong>dècimes</strong>; si també són iguals, les <strong>centèsimes</strong>, i així successivament.", "Si son iguales, comparamos las <strong>décimas</strong>; si también son iguales, las <strong>centésimas</strong>, y así sucesivamente.", "If they're equal, compare the <strong>tenths</strong>; if those are equal too, the <strong>hundredths</strong>, and so on."))
  + P(r"Un truc: <strong>igualem el nombre de decimals</strong> afegint zeros i comparem com si fossen naturals:", r"Un truco: <strong>igualamos el número de decimales</strong> añadiendo ceros y comparamos como si fueran naturales:", r"A trick: <strong>give both the same number of decimals</strong> by adding zeros, then compare as whole numbers:")
  + r'\[3\dc5\ \text{?}\ 3\dc48\quad\longrightarrow\quad 3\dc50>3\dc48\]'
  + note(r"Error típic: pensar que \(3\dc48>3\dc5\) perquè 48 és més gran que 5. Però \(3\dc5\) té 5 <strong>dècimes</strong> i \(3\dc48\) només en té 4.",
         r"Error típico: pensar que \(3\dc48>3\dc5\) porque 48 es mayor que 5. Pero \(3\dc5\) tiene 5 <strong>décimas</strong> y \(3\dc48\) solo tiene 4.",
         r"Typical mistake: thinking \(3\dc48>3\dc5\) because 48 is bigger than 5. But \(3\dc5\) has 5 <strong>tenths</strong> and \(3\dc48\) only 4.", '⚠️'))
s2 += box('def', L('Representar decimals en la recta', 'Representar decimales en la recta', 'Decimals on the number line'),
  P(r"Per a situar \(2\dc74\): està entre 2 i 3, així que dividim aquest tros en 10 parts (dècimes) i ens quedem entre \(2\dc7\) i \(2\dc8\). Després dividim aquest tros en 10 parts més (centèsimes) i comptem 4:",
    r"Para situar \(2\dc74\): está entre 2 y 3, así que dividimos ese trozo en 10 partes (décimas) y nos quedamos entre \(2\dc7\) y \(2\dc8\). Después dividimos ese trozo en 10 partes más (centésimas) y contamos 4:",
    r"To place \(2\dc74\): it lies between 2 and 3, so split that piece into 10 parts (tenths) and we're between \(2\dc7\) and \(2\dc8\). Then split that piece into 10 more parts (hundredths) and count 4:")
  + figs((svg_nl(2, 3, 10, [(2.74, '2,74')], 1), L('Entre 2 i 3, de dècima en dècima', 'Entre 2 y 3, de décima en décima', 'From 2 to 3, in tenths')),
         (svg_nl(2.7, 2.8, 10, [(2.74, '2,74')], 2), L('Zoom: entre 2,7 i 2,8, de centèsima en centèsima', 'Zoom: entre 2,7 y 2,8, de centésima en centésima', 'Zoom: from 2.7 to 2.8, in hundredths')))
  + note(r"Entre dos decimals sempre hi ha infinits decimals més: entre \(1\dc4\) i \(1\dc5\) hi ha \(1\dc41\), \(1\dc45\), \(1\dc499\)…",
         r"Entre dos decimales siempre hay infinitos decimales más: entre \(1\dc4\) y \(1\dc5\) están \(1\dc41\), \(1\dc45\), \(1\dc499\)…",
         r"Between two decimals there are always infinitely many more: between \(1\dc4\) and \(1\dc5\) we have \(1\dc41\), \(1\dc45\), \(1\dc499\)…")
  + widget('w-zoom', '🔍', L('Lupa de la recta numèrica', 'Lupa de la recta numérica', 'Number-line magnifier'),
    f'  <div class="wrow">{nin("x", "Nombre", "Número", "Number", "2,74", "m")}</div>\n'
    + '  ' + quick([('2,74', '2,74'), ('0,35', '0,35'), ('5,608', '5,608'), ('1,09', '1,09'), ('7,5', '7,5'), ('0,006', '0,006')]) + '\n'))
s2 += box('prop', L('Aproximar: truncar i arrodonir', 'Aproximar: truncar y redondear', 'Approximating: truncating and rounding'),
  P(r"Moltes vegades no necessitem tots els decimals (per exemple, en euros només hi ha cèntims, és a dir, centèsimes). Per a <strong>aproximar</strong> a un ordre (unitats, dècimes, centèsimes…):",
    r"Muchas veces no necesitamos todos los decimales (por ejemplo, en euros solo hay céntimos, es decir, centésimas). Para <strong>aproximar</strong> a un orden (unidades, décimas, centésimas…):",
    r"We often don't need every decimal (in euros, for example, there are only cents, that is, hundredths). To <strong>approximate</strong> to a place (units, tenths, hundredths…):")
  + ul(L("<strong>Truncar</strong>: tallem i eliminem les xifres que hi ha a la dreta d'aquest ordre.", "<strong>Truncar</strong>: cortamos y eliminamos las cifras que hay a la derecha de ese orden.", "<strong>Truncate</strong>: cut off every digit to the right of that place."),
       L("<strong>Arrodonir</strong>: mirem la primera xifra que eliminem. Si és <strong>0, 1, 2, 3 o 4</strong>, deixem igual l'última xifra; si és <strong>5, 6, 7, 8 o 9</strong>, li sumem 1.", "<strong>Redondear</strong>: miramos la primera cifra que eliminamos. Si es <strong>0, 1, 2, 3 o 4</strong>, dejamos igual la última cifra; si es <strong>5, 6, 7, 8 o 9</strong>, le sumamos 1.", "<strong>Round</strong>: look at the first digit you remove. If it's <strong>0, 1, 2, 3 or 4</strong>, leave the last digit as it is; if it's <strong>5, 6, 7, 8 or 9</strong>, add 1 to it."))
  + table([L('Aproximem 3,4682 a…', 'Aproximamos 3,4682 a…', 'Approximating 3.4682 to…'), L('Truncament', 'Truncamiento', 'Truncation'), L('Arrodoniment', 'Redondeo', 'Rounding')],
          [[L('unitats', 'unidades', 'units'), r'\(3\)', r'\(3\)'], [L('dècimes', 'décimas', 'tenths'), r'\(3\dc4\)', r'\(3\dc5\)'], [L('centèsimes', 'centésimas', 'hundredths'), r'\(3\dc46\)', r'\(3\dc47\)'], [L('mil·lèsimes', 'milésimas', 'thousandths'), r'\(3\dc468\)', r'\(3\dc468\)']])
  + note(r"L'arrodoniment s'acosta més al nombre real. Per això els preus i les mesures s'arrodoneixen.", r"El redondeo se acerca más al número real. Por eso los precios y las medidas se redondean.", r"Rounding stays closer to the real number. That's why prices and measurements are rounded.")
  + widget('w-round', '✂️', L('Truncar i arrodonir', 'Truncar y redondear', 'Truncate and round'),
    f'  <div class="wrow">{nin("x", "Nombre", "Número", "Number", "3,4682", "m")}{gseg("k", [("0", L("Unitats", "Unidades", "Units")), ("1", L("Dècimes", "Décimas", "Tenths")), ("2", L("Centèsimes", "Centésimas", "Hundredths")), ("3", L("Mil·lèsimes", "Milésimas", "Thousandths"))], "2")}</div>\n'
    + '  ' + quick([('3,4682', '3,4682'), ('15,8962', '15,8962'), ('2,996', '2,996'), ('0,4449', '0,4449'), ('7,05', '7,05'), ('129,5', '129,5')]) + '\n')
  + drill('cmp', 'Entrena: compara decimals', 'Entrena: compara decimales', 'Train: compare decimals')
  + drill('round', 'Entrena: arrodoneix', 'Entrena: redondea', 'Train: rounding'))
ck(round(Dm('3.4682'), 2), '3.47'); ck(round(Dm('3.4682'), 1), '3.5')
s2 += level(1, 1,
  prob(L(r"Escriu &lt; o &gt;: a) \(4\dc7\ \square\ 4\dc68\) &nbsp; b) \(0\dc09\ \square\ 0\dc1\) &nbsp; c) \(5\dc307\ \square\ 5\dc37\)", r"Escribe &lt; o &gt;: a) \(4\dc7\ \square\ 4\dc68\) &nbsp; b) \(0\dc09\ \square\ 0\dc1\) &nbsp; c) \(5\dc307\ \square\ 5\dc37\)", r"Write &lt; or &gt;: a) \(4\dc7\ \square\ 4\dc68\) &nbsp; b) \(0\dc09\ \square\ 0\dc1\) &nbsp; c) \(5\dc307\ \square\ 5\dc37\)"),
       P(r"Igualem el nombre de decimals:", r"Igualamos el número de decimales:", r"Give them the same number of decimals:"),
       r'\[\text{a) }4\dc70>4\dc68\qquad\text{b) }0\dc09<0\dc10\qquad\text{c) }5\dc307<5\dc370\]'),
  prob(L(r"Ordena de menor a major: \(\ 2\dc5;\ 2\dc05;\ 2\dc55;\ 2\dc505;\ 2\dc0\)", r"Ordena de menor a mayor: \(\ 2\dc5;\ 2\dc05;\ 2\dc55;\ 2\dc505;\ 2\dc0\)", r"Order from smallest to largest: \(\ 2\dc5;\ 2\dc05;\ 2\dc55;\ 2\dc505;\ 2\dc0\)"),
       P(r"Tots amb tres decimals: \(2\dc500;\ 2\dc050;\ 2\dc550;\ 2\dc505;\ 2\dc000\). Ara comparem com a naturals:", r"Todos con tres decimales: \(2\dc500;\ 2\dc050;\ 2\dc550;\ 2\dc505;\ 2\dc000\). Ahora comparamos como naturales:", r"All with three decimals: \(2\dc500;\ 2\dc050;\ 2\dc550;\ 2\dc505;\ 2\dc000\). Now compare like whole numbers:"),
       r'\[2\dc0<2\dc05<2\dc5<2\dc505<2\dc55\]'))
s2 += level(2, 3,
  prob(L(r"Escriu tres nombres decimals compresos entre \(0\dc3\) i \(0\dc4\).", r"Escribe tres números decimales comprendidos entre \(0\dc3\) y \(0\dc4\).", r"Write three decimals between \(0\dc3\) and \(0\dc4\)."),
       P(r"Escrivim \(0\dc3=0\dc30\) i \(0\dc4=0\dc40\): entre 30 i 40 centèsimes hi ha, per exemple, \(0\dc31\), \(0\dc35\) i \(0\dc39\). (I moltes més: \(0\dc305\), \(0\dc3999\)…)", r"Escribimos \(0\dc3=0\dc30\) y \(0\dc4=0\dc40\): entre 30 y 40 centésimas están, por ejemplo, \(0\dc31\), \(0\dc35\) y \(0\dc39\). (Y muchas más: \(0\dc305\), \(0\dc3999\)…)", r"Write \(0\dc3=0\dc30\) and \(0\dc4=0\dc40\): between 30 and 40 hundredths are, for example, \(0\dc31\), \(0\dc35\) and \(0\dc39\). (And many more: \(0\dc305\), \(0\dc3999\)…)")))
s2 += level(3, 4,
  prob(L(r"Arrodoneix \(2\dc996\) a les centèsimes i \(15\dc8962\) a les unitats, a les dècimes i a les centèsimes.", r"Redondea \(2\dc996\) a las centésimas y \(15\dc8962\) a las unidades, a las décimas y a las centésimas.", r"Round \(2\dc996\) to hundredths, and \(15\dc8962\) to units, tenths and hundredths."),
       P(r"En \(2\dc996\) la xifra que eliminem és un 6: sumem 1 a les centèsimes. Però \(99+1=100\): «ens n'emportem una» fins a les unitats:", r"En \(2\dc996\) la cifra que eliminamos es un 6: sumamos 1 a las centésimas. Pero \(99+1=100\): «nos llevamos una» hasta las unidades:", r"In \(2\dc996\) the digit we remove is 6: add 1 to the hundredths. But \(99+1=100\): we “carry” all the way to the units:")
       + r'\[2\dc996\approx\boxed{3\dc00}\]' + P(r"Escrivim \(3\dc00\) i no \(3\) per a indicar que hem arrodonit a centèsimes.", r"Escribimos \(3\dc00\) y no \(3\) para indicar que hemos redondeado a centésimas.", r"We write \(3\dc00\), not \(3\), to show we've rounded to hundredths."),
       r'\[15\dc8962\approx\boxed{16}\ (\tri{unitats}{unidades}{units})\qquad 15\dc8962\approx\boxed{15\dc9}\ (\tri{dècimes}{décimas}{tenths})\qquad 15\dc8962\approx\boxed{15\dc90}\ (\tri{centèsimes}{centésimas}{hundredths})\]'))
ck(round(Dm('15.8962'), 0), '16'); ck(round(Dm('15.8962'), 2), '15.90'); ck(round(Dm('2.996'), 2), '3.00')
s2 += practice([
  ('★', L(r"a) Compara: \(0\dc8\ \square\ 0\dc799\). b) Ordena de major a menor: \(1\dc2;\ 1\dc02;\ 1\dc22;\ 1\dc202\).", r"a) Compara: \(0\dc8\ \square\ 0\dc799\). b) Ordena de mayor a menor: \(1\dc2;\ 1\dc02;\ 1\dc22;\ 1\dc202\).", r"a) Compare: \(0\dc8\ \square\ 0\dc799\). b) Order from largest to smallest: \(1\dc2;\ 1\dc02;\ 1\dc22;\ 1\dc202\).")),
  ('★★', L(r"c) Escriu un decimal entre \(5\dc61\) i \(5\dc62\). d) Trunca i arrodoneix \(8\dc4537\) a les centèsimes.", r"c) Escribe un decimal entre \(5\dc61\) y \(5\dc62\). d) Trunca y redondea \(8\dc4537\) a las centésimas.", r"c) Write a decimal between \(5\dc61\) and \(5\dc62\). d) Truncate and round \(8\dc4537\) to hundredths.")),
  ('★★★', L(r"e) Una calculadora diu que un article costa \(4\dc9861\) €. Quant pagarem? f) Escriu un nombre que, arrodonit a les dècimes, done \(2\dc5\), i que siga menor que \(2\dc5\).", r"e) Una calculadora dice que un artículo cuesta \(4\dc9861\) €. ¿Cuánto pagaremos? f) Escribe un número que, redondeado a las décimas, dé \(2\dc5\), y que sea menor que \(2\dc5\).", r"e) A calculator says an item costs \(4\dc9861\) €. How much will we pay? f) Write a number that rounds to \(2\dc5\) (to tenths) and is less than \(2\dc5\)."))],
  P(r"a) \(0\dc800>0\dc799\). &nbsp; b) \(1\dc22>1\dc202>1\dc2>1\dc02\).", r"a) \(0\dc800>0\dc799\). &nbsp; b) \(1\dc22>1\dc202>1\dc2>1\dc02\).", r"a) \(0\dc800>0\dc799\). &nbsp; b) \(1\dc22>1\dc202>1\dc2>1\dc02\).")
  + P(r"c) Per exemple \(5\dc615\). &nbsp; d) Truncat: \(8\dc45\); arrodonit: \(8\dc45\) (la xifra eliminada és un 3).", r"c) Por ejemplo \(5\dc615\). &nbsp; d) Truncado: \(8\dc45\); redondeado: \(8\dc45\) (la cifra eliminada es un 3).", r"c) For example \(5\dc615\). &nbsp; d) Truncated: \(8\dc45\); rounded: \(8\dc45\) (the removed digit is 3).")
  + P(r"e) Arrodonim a cèntims: \(4\dc99\) €. &nbsp; f) Qualsevol entre \(2\dc45\) i \(2\dc5\), per exemple \(2\dc47\).", r"e) Redondeamos a céntimos: \(4\dc99\) €. &nbsp; f) Cualquiera entre \(2\dc45\) y \(2\dc5\), por ejemplo \(2\dc47\).", r"e) Round to cents: \(4\dc99\) €. &nbsp; f) Anything from \(2\dc45\) up to (not including) \(2\dc5\), e.g. \(2\dc47\)."))

# ============================================================ 5.3
s3 = box('prop', L('Sumar i restar decimals', 'Sumar y restar decimales', 'Adding and subtracting decimals'),
  ol(L("Col·loquem els nombres un davall de l'altre amb les <strong>comes alineades</strong> (unitats davall d'unitats, dècimes davall de dècimes…).", "Colocamos los números uno debajo del otro con las <strong>comas alineadas</strong> (unidades debajo de unidades, décimas debajo de décimas…).", "Write the numbers one under the other with the <strong>commas lined up</strong> (units under units, tenths under tenths…)."),
     L("Si cal, completem amb <strong>zeros</strong> perquè tinguen els mateixos decimals.", "Si hace falta, completamos con <strong>ceros</strong> para que tengan los mismos decimales.", "If needed, fill in with <strong>zeros</strong> so they have the same number of decimals."),
     L("Operem com amb nombres naturals i posem la coma al resultat, en la mateixa columna.", "Operamos como con números naturales y ponemos la coma en el resultado, en la misma columna.", "Work as with whole numbers and put the comma in the answer, in the same column."))
  + '<div class="figs"><figure>' + '<div class="colop"><table><tr><td></td><td>1</td><td>2</td><td class="cm">,</td><td>5</td><td class="z">0</td></tr><tr><td>+</td><td></td><td>3</td><td class="cm">,</td><td>7</td><td>8</td></tr><tr class="res"><td></td><td>1</td><td>6</td><td class="cm">,</td><td>2</td><td>8</td></tr></table></div>' + r'<figcaption>\(12\dc5+3\dc78\)</figcaption></figure>'
  + '<figure><div class="colop"><table><tr><td></td><td>1</td><td>5</td><td class="cm z">,</td><td class="z">0</td><td class="z">0</td></tr><tr><td>−</td><td></td><td>6</td><td class="cm">,</td><td>4</td><td>7</td></tr><tr class="res"><td></td><td></td><td>8</td><td class="cm">,</td><td>5</td><td>3</td></tr></table></div>' + r'<figcaption>\(15-6\dc47\)</figcaption></figure></div>'
  + note(r"Un nombre natural té la coma «amagada» al final: \(15=15\dc00\).", r"Un número natural tiene la coma «escondida» al final: \(15=15\dc00\).", r"A whole number has a “hidden” comma at the end: \(15=15\dc00\)."))
ck(Dm('12.5') + Dm('3.78'), '16.28'); ck(15 - Dm('6.47'), '8.53')
s3 += box('prop', L('Multiplicar decimals', 'Multiplicar decimales', 'Multiplying decimals'),
  P(r"Multipliquem com si no hi haguera comes i, al resultat, separem tantes xifres decimals com <strong>sumen</strong> els decimals dels dos factors:",
    r"Multiplicamos como si no hubiera comas y, en el resultado, separamos tantas cifras decimales como <strong>sumen</strong> los decimales de los dos factores:",
    r"Multiply as if there were no commas and, in the answer, mark off as many decimal places as the two factors have <strong>in total</strong>:")
  + r'\[3\dc25\cdot1\dc4\ :\quad 325\cdot14=4550\quad\longrightarrow\quad \underbrace{2}_{3\dc25}+\underbrace{1}_{1\dc4}=3\ \tri{decimals}{decimales}{decimals}\quad\longrightarrow\quad \boxed{4\dc550=4\dc55}\]'
  + note(r"Abans de multiplicar, <strong>estima</strong>: \(3\dc25\cdot1\dc4\) és una mica més que \(3\cdot1=3\) i menys que \(4\cdot2=8\). Si et dona 45,5 o 0,455, segur que hi ha un error en la coma.", r"Antes de multiplicar, <strong>estima</strong>: \(3\dc25\cdot1\dc4\) es algo más que \(3\cdot1=3\) y menos que \(4\cdot2=8\). Si te da 45,5 o 0,455, seguro que hay un error en la coma.", r"Before multiplying, <strong>estimate</strong>: \(3\dc25\cdot1\dc4\) is a bit more than \(3\cdot1=3\) and less than \(4\cdot2=8\). If you get 45.5 or 0.455, the comma is in the wrong place."))
ck(Dm('3.25') * Dm('1.4'), '4.55')
s3 += widget('w-col', '🧾', L('Operacions en columna', 'Operaciones en columna', 'Column arithmetic'),
  f'  <div class="wrow">{nin("a", "", "", "", "12,5", "m")}{gseg("op", [("+", "+"), ("-", "−"), ("*", "×")], "+")}{nin("b", "", "", "", "3,78", "m")}</div>\n'
  + '  ' + quick([('12,5;3,78;+', '12,5 + 3,78'), ('15;6,47;-', '15 − 6,47'), ('0,9;0,35;+', '0,9 + 0,35'), ('3,25;1,4;*', '3,25 × 1,4'), ('0,4;0,02;*', '0,4 × 0,02'), ('7,2;5;*', '7,2 × 5')]) + '\n')
s3 += box('prop', L('Multiplicar i dividir per 10, 100, 1000…', 'Multiplicar y dividir por 10, 100, 1000…', 'Multiplying and dividing by 10, 100, 1000…'),
  ul(L("Per a <strong>multiplicar</strong> per 10, 100, 1000…, movem la coma cap a la <strong>dreta</strong> tants llocs com zeros hi ha. Si falten xifres, afegim zeros.", "Para <strong>multiplicar</strong> por 10, 100, 1000…, movemos la coma hacia la <strong>derecha</strong> tantos lugares como ceros hay. Si faltan cifras, añadimos ceros.", "To <strong>multiply</strong> by 10, 100, 1000…, move the comma to the <strong>right</strong> as many places as there are zeros. If you run out of digits, add zeros."),
     L("Per a <strong>dividir</strong> entre 10, 100, 1000…, movem la coma cap a l'<strong>esquerra</strong>. Si falten xifres, afegim zeros davant.", "Para <strong>dividir</strong> entre 10, 100, 1000…, movemos la coma hacia la <strong>izquierda</strong>. Si faltan cifras, añadimos ceros delante.", "To <strong>divide</strong> by 10, 100, 1000…, move the comma to the <strong>left</strong>. If you run out of digits, add zeros in front."))
  + r'\[3\dc7\cdot100=370\qquad 0\dc052\cdot1000=52\qquad 45\dc2:1000=0\dc0452\qquad 8:100=0\dc08\]'
  + note(r"Multiplicar per \(0\dc1\) és el mateix que dividir entre 10, i multiplicar per \(0\dc01\), dividir entre 100: \(\ 250\cdot0\dc1=25\).", r"Multiplicar por \(0\dc1\) es lo mismo que dividir entre 10, y multiplicar por \(0\dc01\), dividir entre 100: \(\ 250\cdot0\dc1=25\).", r"Multiplying by \(0\dc1\) is the same as dividing by 10, and multiplying by \(0\dc01\), dividing by 100: \(\ 250\cdot0\dc1=25\).")
  + widget('w-p10', '↔️', L('Movem la coma', 'Movemos la coma', 'Moving the comma'),
    f'  <div class="wrow">{nin("x", "Nombre", "Número", "Number", "3,7", "m")}{gseg("op", [("*", "×"), (":", ":")], "*")}{gseg("p", [("1", "10"), ("2", "100"), ("3", "1000")], "2")}</div>\n'
    + '  ' + quick([('3,7;*;2', '3,7 × 100'), ('0,052;*;3', '0,052 × 1000'), ('45,2;:;3', '45,2 : 1000'), ('8;:;2', '8 : 100'), ('6,15;*;1', '6,15 × 10'), ('0,3;:;1', '0,3 : 10')]) + '\n')
  + drill('p10', 'Entrena: per 10, 100 i 1000', 'Entrena: por 10, 100 y 1000', 'Train: by 10, 100 and 1000')
  + drill('ops', 'Entrena: suma, resta i multiplica', 'Entrena: suma, resta y multiplica', 'Train: add, subtract, multiply'))
ck(Dm('3.7') * 100, '370'); ck(Dm('0.052') * 1000, '52'); ck(Dm('45.2') / 1000, '0.0452'); ck(Dm(8) / 100, '0.08')
s3 += level(1, 1,
  prob(L(r"Calcula: a) \(23\dc45+7\dc8\) &nbsp; b) \(40-12\dc35\) &nbsp; c) \(4\dc6\cdot3\)", r"Calcula: a) \(23\dc45+7\dc8\) &nbsp; b) \(40-12\dc35\) &nbsp; c) \(4\dc6\cdot3\)", r"Work out: a) \(23\dc45+7\dc8\) &nbsp; b) \(40-12\dc35\) &nbsp; c) \(4\dc6\cdot3\)"),
       r'\[\text{a) }23\dc45+7\dc80=\boxed{31\dc25}\qquad\text{b) }40\dc00-12\dc35=\boxed{27\dc65}\]',
       r'\[\text{c) }46\cdot3=138\ \longrightarrow\ 1\ \tri{decimal}{decimal}{decimal}:\ \boxed{13\dc8}\]'))
ck(Dm('23.45') + Dm('7.8'), '31.25'); ck(40 - Dm('12.35'), '27.65'); ck(Dm('4.6') * 3, '13.8')
s3 += level(2, 2,
  prob(L(r"Calcula: a) \(2\dc35\cdot0\dc4\) &nbsp; b) \(0\dc07\cdot100\) &nbsp; c) \(0\dc6\cdot0\dc05\)", r"Calcula: a) \(2\dc35\cdot0\dc4\) &nbsp; b) \(0\dc07\cdot100\) &nbsp; c) \(0\dc6\cdot0\dc05\)", r"Work out: a) \(2\dc35\cdot0\dc4\) &nbsp; b) \(0\dc07\cdot100\) &nbsp; c) \(0\dc6\cdot0\dc05\)"),
       r'\[\text{a) }235\cdot4=940,\ 2+1=3\ \tri{decimals}{decimales}{decimals}:\ 0\dc940=\boxed{0\dc94}\]',
       r'\[\text{b) }0\dc07\cdot100=\boxed{7}\qquad\text{c) }6\cdot5=30,\ 1+2=3\ \tri{decimals}{decimales}{decimals}:\ \boxed{0\dc03}\]',
       P(r"Fixa't que en a) i c) el resultat és <strong>menor</strong> que el primer factor: multiplicar per un nombre menor que 1 fa el resultat més xicotet.", r"Fíjate en que en a) y c) el resultado es <strong>menor</strong> que el primer factor: multiplicar por un número menor que 1 hace el resultado más pequeño.", r"Notice that in a) and c) the answer is <strong>smaller</strong> than the first factor: multiplying by a number less than 1 makes it smaller.")))
ck(Dm('2.35') * Dm('0.4'), '0.94'); ck(Dm('0.07') * 100, '7'); ck(Dm('0.6') * Dm('0.05'), '0.03')
s3 += level(3, 3,
  prob(L(r"Comprem \(2\dc5\) kg de pomes a \(1\dc80\) €/kg i \(1\dc5\) kg de cireres a \(6\dc40\) €/kg. Paguem amb un bitllet de 20 €. Quant ens tornen?", r"Compramos \(2\dc5\) kg de manzanas a \(1\dc80\) €/kg y \(1\dc5\) kg de cerezas a \(6\dc40\) €/kg. Pagamos con un billete de 20 €. ¿Cuánto nos devuelven?", r"We buy \(2\dc5\) kg of apples at \(1\dc80\) €/kg and \(1\dc5\) kg of cherries at \(6\dc40\) €/kg. We pay with a 20 € note. How much change do we get?"),
       r'\[\tri{Pomes}{Manzanas}{Apples}:\ 2\dc5\cdot1\dc80=4\dc50\ €\qquad \tri{Cireres}{Cerezas}{Cherries}:\ 1\dc5\cdot6\dc40=9\dc60\ €\]',
       r'\[\tri{Total}{Total}{Total}:\ 4\dc50+9\dc60=14\dc10\ €\qquad \tri{Canvi}{Cambio}{Change}:\ 20-14\dc10=\boxed{5\dc90\ €}\]'))
ck(Dm('2.5') * Dm('1.80') + Dm('1.5') * Dm('6.40'), '14.10'); ck(20 - Dm('14.10'), '5.90')
s3 += practice([
  ('★', L(r"a) \(7\dc06+12\dc9\) &nbsp; b) \(9\dc2-4\dc75\) &nbsp; c) \(0\dc3\cdot1000\)", r"a) \(7\dc06+12\dc9\) &nbsp; b) \(9\dc2-4\dc75\) &nbsp; c) \(0\dc3\cdot1000\)", r"a) \(7\dc06+12\dc9\) &nbsp; b) \(9\dc2-4\dc75\) &nbsp; c) \(0\dc3\cdot1000\)")),
  ('★★', L(r"d) \(1\dc25\cdot0\dc8\) &nbsp; e) \(56\dc3:100\) &nbsp; f) \(0\dc12\cdot0\dc3\)", r"d) \(1\dc25\cdot0\dc8\) &nbsp; e) \(56\dc3:100\) &nbsp; f) \(0\dc12\cdot0\dc3\)", r"d) \(1\dc25\cdot0\dc8\) &nbsp; e) \(56\dc3:100\) &nbsp; f) \(0\dc12\cdot0\dc3\)")),
  ('★★★', L(r"g) Un quadern costa \(1\dc35\) € i un bolígraf \(0\dc85\) €. Quant costen 4 quaderns i 6 bolígrafs? h) Quin nombre hem de sumar a \(3\dc78\) per a obtenir 10?", r"g) Un cuaderno cuesta \(1\dc35\) € y un bolígrafo \(0\dc85\) €. ¿Cuánto cuestan 4 cuadernos y 6 bolígrafos? h) ¿Qué número hay que sumar a \(3\dc78\) para obtener 10?", r"g) A notebook costs \(1\dc35\) € and a pen \(0\dc85\) €. How much do 4 notebooks and 6 pens cost? h) What must we add to \(3\dc78\) to get 10?"))],
  P(r"a) \(19\dc96\) &nbsp; b) \(4\dc45\) &nbsp; c) \(300\)", r"a) \(19\dc96\) &nbsp; b) \(4\dc45\) &nbsp; c) \(300\)", r"a) \(19\dc96\) &nbsp; b) \(4\dc45\) &nbsp; c) \(300\)")
  + P(r"d) \(1\) &nbsp; e) \(0\dc563\) &nbsp; f) \(0\dc036\)", r"d) \(1\) &nbsp; e) \(0\dc563\) &nbsp; f) \(0\dc036\)", r"d) \(1\) &nbsp; e) \(0\dc563\) &nbsp; f) \(0\dc036\)")
  + P(r"g) \(5\dc40+5\dc10=10\dc50\) €. &nbsp; h) \(10-3\dc78=6\dc22\).", r"g) \(5\dc40+5\dc10=10\dc50\) €. &nbsp; h) \(10-3\dc78=6\dc22\).", r"g) \(5\dc40+5\dc10=10\dc50\) €. &nbsp; h) \(10-3\dc78=6\dc22\)."))
ck(Dm('7.06') + Dm('12.9'), '19.96'); ck(Dm('9.2') - Dm('4.75'), '4.45'); ck(Dm('1.25') * Dm('0.8'), '1'); ck(Dm('56.3') / 100, '0.563'); ck(Dm('0.12') * Dm('0.3'), '0.036')
ck(4 * Dm('1.35') + 6 * Dm('0.85'), '10.50')

# ============================================================ 5.4
s4 = box('prop', L('Dividir un decimal entre un natural', 'Dividir un decimal entre un natural', 'Dividing a decimal by a whole number'),
  P(r"Dividim com sempre i, <strong>quan baixem la primera xifra decimal</strong>, posem la coma al quocient:", r"Dividimos como siempre y, <strong>cuando bajamos la primera cifra decimal</strong>, ponemos la coma en el cociente:", r"Divide as usual and, <strong>when you bring down the first decimal digit</strong>, put the comma in the quotient:")
  + r'\[9\dc75:3=3\dc25\qquad\left(\ 9:3=3\ \to\ \text{,}\ \to\ 7:3=2\ \tri{residu}{resto}{rem.}\ 1\ \to\ 15:3=5\ \right)\]')
s4 += box('prop', L('Traure decimals al quocient', 'Sacar decimales en el cociente', 'Getting decimals in the quotient'),
  P(r"Si una divisió no és exacta, podem continuar: posem una coma al quocient, afegim un 0 al residu i seguim dividint.", r"Si una división no es exacta, podemos continuar: ponemos una coma en el cociente, añadimos un 0 al resto y seguimos dividiendo.", r"If a division isn't exact, we can keep going: put a comma in the quotient, add a 0 to the remainder and keep dividing.")
  + r'\[7:4\ \to\ 1,\ \tri{residu}{resto}{rem.}\ 3\ \to\ 30:4=7,\ \tri{residu}{resto}{rem.}\ 2\ \to\ 20:4=5,\ \tri{residu}{resto}{rem.}\ 0\qquad 7:4=\boxed{1\dc75}\]')
s4 += box('prop', L('Dividir entre un decimal', 'Dividir entre un decimal', 'Dividing by a decimal'),
  P(r"Si el <strong>divisor</strong> té decimals, multipliquem dividend i divisor per 10, 100, 1000… fins que el divisor siga natural. El quocient no canvia:",
    r"Si el <strong>divisor</strong> tiene decimales, multiplicamos dividendo y divisor por 10, 100, 1000… hasta que el divisor sea natural. El cociente no cambia:",
    r"If the <strong>divisor</strong> has decimals, multiply both dividend and divisor by 10, 100, 1000… until the divisor is a whole number. The quotient doesn't change:")
  + r'\[12\dc6:0\dc35\ \xrightarrow{\ \cdot100\ }\ 1260:35=\boxed{36}\]'
  + note(r"Dividir entre un nombre <strong>menor que 1</strong> fa el resultat <strong>més gran</strong>: \(12\dc6:0\dc35=36\). Té sentit: en \(12\dc6\) hi caben moltes vegades \(0\dc35\).",
         r"Dividir entre un número <strong>menor que 1</strong> hace el resultado <strong>mayor</strong>: \(12\dc6:0\dc35=36\). Tiene sentido: en \(12\dc6\) cabe muchas veces \(0\dc35\).",
         r"Dividing by a number <strong>less than 1</strong> makes the answer <strong>bigger</strong>: \(12\dc6:0\dc35=36\). It makes sense: \(0\dc35\) fits into \(12\dc6\) many times."))
ck(Dm('9.75') / 3, '3.25'); ck(Dm(7) / 4, '1.75'); ck(Dm('12.6') / Dm('0.35'), '36')
s4 += widget('w-div', '➗', L('Divisió pas a pas', 'División paso a paso', 'Division step by step'),
  f'  <div class="wrow">{nin("a", "Dividend", "Dividendo", "Dividend", "12,6", "m")}{nin("b", "Divisor", "Divisor", "Divisor", "0,35", "m")}{gseg("k", [("0", L("0 decimals", "0 decimales", "0 decimals")), ("1", "1"), ("2", "2"), ("3", "3")], "2")}</div>\n'
  + '  ' + quick([('12,6;0,35', '12,6 : 0,35'), ('9,75;3', '9,75 : 3'), ('7;4', '7 : 4'), ('2,73;0,7', '2,73 : 0,7'), ('5;0,25', '5 : 0,25'), ('10;3', '10 : 3'), ('0,9;0,004', '0,9 : 0,004')]) + '\n')
s4 += drill('div', 'Entrena: divisions amb decimals', 'Entrena: divisiones con decimales', 'Train: dividing with decimals')
s4 += level(1, 1,
  prob(L(r"Calcula: a) \(8\dc4:4\) &nbsp; b) \(15:8\)", r"Calcula: a) \(8\dc4:4\) &nbsp; b) \(15:8\)", r"Work out: a) \(8\dc4:4\) &nbsp; b) \(15:8\)"),
       r'\[\text{a) }8\dc4:4=\boxed{2\dc1}\]',
       r'\[\text{b) }15:8=1,\ \tri{residu}{resto}{rem.}\ 7\ \to\ 70:8=8\ (6)\ \to\ 60:8=7\ (4)\ \to\ 40:8=5\ (0)\qquad 15:8=\boxed{1\dc875}\]'))
ck(Dm('8.4') / 4, '2.1'); ck(Dm(15) / 8, '1.875')
s4 += level(2, 2,
  prob(L(r"Calcula: a) \(4\dc5:0\dc9\) &nbsp; b) \(2\dc73:0\dc7\) &nbsp; c) \(6:0\dc12\)", r"Calcula: a) \(4\dc5:0\dc9\) &nbsp; b) \(2\dc73:0\dc7\) &nbsp; c) \(6:0\dc12\)", r"Work out: a) \(4\dc5:0\dc9\) &nbsp; b) \(2\dc73:0\dc7\) &nbsp; c) \(6:0\dc12\)"),
       r'\[\text{a) }45:9=\boxed{5}\qquad\text{b) }27\dc3:7=\boxed{3\dc9}\qquad\text{c) }600:12=\boxed{50}\]',
       P(r"En a) i b) multipliquem per 10 (el divisor té 1 decimal); en c), per 100.", r"En a) y b) multiplicamos por 10 (el divisor tiene 1 decimal); en c), por 100.", r"In a) and b) multiply by 10 (the divisor has 1 decimal); in c), by 100.")))
ck(Dm('4.5') / Dm('0.9'), '5'); ck(Dm('2.73') / Dm('0.7'), '3.9'); ck(Dm(6) / Dm('0.12'), '50')
s4 += level(3, 3,
  prob(L(r"Amb una botella de \(1\dc5\) L, quants gots de \(0\dc25\) L podem omplir? I si un tros de formatge de \(0\dc85\) kg costa \(11\dc39\) €, quin és el preu d'un quilo?", r"Con una botella de \(1\dc5\) L, ¿cuántos vasos de \(0\dc25\) L podemos llenar? Y si un trozo de queso de \(0\dc85\) kg cuesta \(11\dc39\) €, ¿cuál es el precio de un kilo?", r"How many \(0\dc25\) L glasses can we fill from a \(1\dc5\) L bottle? And if a \(0\dc85\) kg piece of cheese costs \(11\dc39\) €, what's the price per kilo?"),
       r'\[1\dc5:0\dc25=150:25=\boxed{6\ \tri{gots}{vasos}{glasses}}\]',
       r'\[11\dc39:0\dc85=1139:85=\boxed{13\dc40\ €/\text{kg}}\]',
       P(r"Comprovació: \(0\dc85\cdot13\dc40=11\dc39\). ✓", r"Comprobación: \(0\dc85\cdot13\dc40=11\dc39\). ✓", r"Check: \(0\dc85\cdot13\dc40=11\dc39\). ✓")))
ck(Dm('1.5') / Dm('0.25'), '6'); ck(Dm('11.39') / Dm('0.85'), '13.4')
s4 += practice([
  ('★', L(r"a) \(6\dc24:3\) &nbsp; b) \(9:4\) &nbsp; c) \(0\dc8:2\)", r"a) \(6\dc24:3\) &nbsp; b) \(9:4\) &nbsp; c) \(0\dc8:2\)", r"a) \(6\dc24:3\) &nbsp; b) \(9:4\) &nbsp; c) \(0\dc8:2\)")),
  ('★★', L(r"d) \(3\dc6:0\dc4\) &nbsp; e) \(1\dc44:1\dc2\) &nbsp; f) \(2:0\dc05\)", r"d) \(3\dc6:0\dc4\) &nbsp; e) \(1\dc44:1\dc2\) &nbsp; f) \(2:0\dc05\)", r"d) \(3\dc6:0\dc4\) &nbsp; e) \(1\dc44:1\dc2\) &nbsp; f) \(2:0\dc05\)")),
  ('★★★', L(r"g) Calcula \(10:3\) amb dues xifres decimals. Què observes si continues? h) Un cotxe gasta \(31\dc5\) L en 450 km. Quants litres gasta cada 100 km?", r"g) Calcula \(10:3\) con dos cifras decimales. ¿Qué observas si continúas? h) Un coche gasta \(31\dc5\) L en 450 km. ¿Cuántos litros gasta cada 100 km?", r"g) Work out \(10:3\) to two decimal places. What do you notice if you carry on? h) A car uses \(31\dc5\) L in 450 km. How many litres does it use per 100 km?"))],
  P(r"a) \(2\dc08\) &nbsp; b) \(2\dc25\) &nbsp; c) \(0\dc4\)", r"a) \(2\dc08\) &nbsp; b) \(2\dc25\) &nbsp; c) \(0\dc4\)", r"a) \(2\dc08\) &nbsp; b) \(2\dc25\) &nbsp; c) \(0\dc4\)")
  + P(r"d) \(9\) &nbsp; e) \(1\dc2\) &nbsp; f) \(40\)", r"d) \(9\) &nbsp; e) \(1\dc2\) &nbsp; f) \(40\)", r"d) \(9\) &nbsp; e) \(1\dc2\) &nbsp; f) \(40\)")
  + P(r"g) \(3\dc33\), residu 1. El residu sempre és 1 i el quocient és \(3\dc333\ldots\): no s'acaba mai (ho veurem a l'apartat 5.5). &nbsp; h) \(31\dc5:4\dc5=7\) L cada 100 km.", r"g) \(3\dc33\), resto 1. El resto siempre es 1 y el cociente es \(3\dc333\ldots\): no se acaba nunca (lo veremos en el apartado 5.5). &nbsp; h) \(31\dc5:4\dc5=7\) L cada 100 km.", r"g) \(3\dc33\), remainder 1. The remainder is always 1 and the quotient is \(3\dc333\ldots\): it never ends (see section 5.5). &nbsp; h) \(31\dc5:4\dc5=7\) L per 100 km."))
ck(Dm('6.24') / 3, '2.08'); ck(Dm(9) / 4, '2.25'); ck(Dm('3.6') / Dm('0.4'), '9'); ck(Dm('1.44') / Dm('1.2'), '1.2'); ck(Dm(2) / Dm('0.05'), '40'); ck(Dm('31.5') / Dm('4.5'), '7')

# ============================================================ 5.5
s5 = box('def', L('De decimal a fracció', 'De decimal a fracción', 'From decimal to fraction'),
  P(r"Un decimal que s'acaba (<strong>decimal exacte</strong>) es pot escriure com una <strong>fracció decimal</strong>, amb denominador 10, 100, 1000…: al numerador posem el nombre sense coma i al denominador, un 1 seguit de tants zeros com xifres decimals té. Després <strong>simplifiquem</strong>:",
    r"Un decimal que se acaba (<strong>decimal exacto</strong>) se puede escribir como una <strong>fracción decimal</strong>, con denominador 10, 100, 1000…: en el numerador ponemos el número sin coma y en el denominador, un 1 seguido de tantos ceros como cifras decimales tiene. Después <strong>simplificamos</strong>:",
    r"A decimal that ends (a <strong>terminating decimal</strong>) can be written as a <strong>decimal fraction</strong>, with denominator 10, 100, 1000…: the numerator is the number without its comma, and the denominator is a 1 followed by as many zeros as decimal places. Then <strong>simplify</strong>:")
  + r'\[0\dc35=\frac{35}{100}=\frac{7}{20}\qquad 2\dc4=\frac{24}{10}=\frac{12}{5}\qquad 0\dc125=\frac{125}{1000}=\frac{1}{8}\]')
ck(Fr(35, 100), Fr(7, 20)); ck(Fr(24, 10), Fr(12, 5)); ck(Fr(125, 1000), Fr(1, 8))
s5 += box('def', L('De fracció a decimal', 'De fracción a decimal', 'From fraction to decimal'),
  P(r"Una fracció és una divisió: dividim el numerador entre el denominador. Poden passar dues coses:", r"Una fracción es una división: dividimos el numerador entre el denominador. Pueden pasar dos cosas:", r"A fraction is a division: divide the numerator by the denominator. Two things can happen:")
  + ul(L(r"La divisió s'acaba (residu 0): és un <strong>decimal exacte</strong>. &nbsp; \(\frac{3}{8}=3:8=0\dc375\)", r"La división se acaba (resto 0): es un <strong>decimal exacto</strong>. &nbsp; \(\frac{3}{8}=3:8=0\dc375\)", r"The division ends (remainder 0): it's a <strong>terminating decimal</strong>. &nbsp; \(\frac{3}{8}=3:8=0\dc375\)"),
         L(r"La divisió no s'acaba mai i les xifres es <strong>repeteixen</strong>: és un <strong>decimal periòdic</strong>. El grup de xifres que es repeteix és el <strong>període</strong> i el marquem amb un arc o una ratlla: \(\frac{2}{3}=0\dc666\ldots=0\dc\overline{6}\)", r"La división no se acaba nunca y las cifras se <strong>repiten</strong>: es un <strong>decimal periódico</strong>. El grupo de cifras que se repite es el <strong>periodo</strong> y lo marcamos con un arco o una raya: \(\frac{2}{3}=0\dc666\ldots=0\dc\overline{6}\)", r"The division never ends and the digits <strong>repeat</strong>: it's a <strong>recurring decimal</strong>. The repeating block is the <strong>period</strong>, marked with a bar: \(\frac{2}{3}=0\dc666\ldots=0\dc\overline{6}\)"))
  + P(r"Per què es repeteixen? Perquè els residus només poden ser 0, 1, 2… fins al divisor menys 1. Quan un residu es repeteix, tot torna a començar.", r"¿Por qué se repiten? Porque los restos solo pueden ser 0, 1, 2… hasta el divisor menos 1. Cuando un resto se repite, todo vuelve a empezar.", r"Why do they repeat? Because the remainders can only be 0, 1, 2… up to the divisor minus 1. Once a remainder comes back, everything starts over.")
  + table([L('Tipus', 'Tipo', 'Type'), L('Exemple', 'Ejemplo', 'Example'), L('Com és', 'Cómo es', 'What it looks like')],
          [[L('Exacte', 'Exacto', 'Terminating'), r'\(\frac{7}{4}=1\dc75\)', L("Té un nombre finit de decimals.", "Tiene un número finito de decimales.", "Finitely many decimals.")],
           [L('Periòdic pur', 'Periódico puro', 'Purely recurring'), r'\(\frac{4}{11}=0\dc363636\ldots=0\dc\overline{36}\)', L("El període comença just després de la coma.", "El periodo empieza justo después de la coma.", "The period starts right after the comma.")],
           [L('Periòdic mixt', 'Periódico mixto', 'Mixed recurring'), r'\(\frac{5}{6}=0\dc8333\ldots=0\dc8\overline{3}\)', L("Hi ha xifres que no es repeteixen (l'<em>anteperíode</em>) abans del període.", "Hay cifras que no se repiten (el <em>anteperiodo</em>) antes del periodo.", "Some non-repeating digits come before the period.")]])
  + note(r"Hi ha decimals amb infinites xifres que <strong>no</strong> es repeteixen mai, com \(\pi=3\dc14159\ldots\) Aquests no venen de cap fracció; els estudiaràs en cursos posteriors.", r"Hay decimales con infinitas cifras que <strong>no</strong> se repiten nunca, como \(\pi=3\dc14159\ldots\) Estos no vienen de ninguna fracción; los estudiarás en cursos posteriores.", r"Some decimals have infinitely many digits that <strong>never</strong> repeat, like \(\pi=3\dc14159\ldots\) They don't come from any fraction; you'll study them in later years."))
ck(Fr(3, 8), Fr('0.375')); ck(Fr(7, 4), Fr('1.75'))
EQV = [('1/2', '0,5'), ('1/4', '0,25'), ('3/4', '0,75'), ('1/5', '0,2'), ('1/10', '0,1'), ('1/8', '0,125'), ('1/3', r'0\dc\overline{3}'), ('2/3', r'0\dc\overline{6}')]
s5 += box('prop', L('Equivalències que convé saber', 'Equivalencias que conviene saber', 'Equivalences worth knowing'),
  '<div class="eqv">' + ''.join(r'<span>\(\frac{%s}{%s}=%s\)</span>' % (a.split('/')[0], a.split('/')[1], b.replace(',', r'\dc')) for a, b in EQV) + '</div>'
  + P(r"Per a <strong>comparar</strong> fraccions i decimals, els passem tots a decimal: \(\ \frac{3}{5}=0\dc6\) i \(0\dc6<0\dc65\), així que \(\frac{3}{5}<0\dc65\).",
      r"Para <strong>comparar</strong> fracciones y decimales, los pasamos todos a decimal: \(\ \frac{3}{5}=0\dc6\) y \(0\dc6<0\dc65\), así que \(\frac{3}{5}<0\dc65\).",
      r"To <strong>compare</strong> fractions and decimals, turn them all into decimals: \(\ \frac{3}{5}=0\dc6\) and \(0\dc6<0\dc65\), so \(\frac{3}{5}<0\dc65\)."))
s5 += widget('w-fd', '🔁', L('Fraccions ⇄ decimals', 'Fracciones ⇄ decimales', 'Fractions ⇄ decimals'),
  f'  <div class="wrow">{gseg("m", [("f", L("Fracció → decimal", "Fracción → decimal", "Fraction → decimal")), ("d", L("Decimal → fracció", "Decimal → fracción", "Decimal → fraction"))], "f")}</div>\n'
  + f'  <div class="wrow" style="margin-top:8px"><span data-p="f">{nin("n", "Numerador", "Numerador", "Numerator", "5", "s", "numeric")}{nin("d", "Denominador", "Denominador", "Denominator", "6", "s", "numeric")}</span><span data-p="d">{nin("x", "Decimal exacte", "Decimal exacto", "Terminating decimal", "0,35", "m")}</span></div>\n'
  + '  ' + quick([('f;5;6', '5/6'), ('f;3;8', '3/8'), ('f;4;11', '4/11'), ('f;2;3', '2/3'), ('f;7;12', '7/12'), ('f;1;7', '1/7'), ('d;0,35', '0,35'), ('d;2,4', '2,4'), ('d;0,125', '0,125')]) + '\n')
s5 += drill('fd', 'Entrena: fraccions i decimals', 'Entrena: fracciones y decimales', 'Train: fractions and decimals')
s5 += level(1, 1,
  prob(L(r"Escriu com a fracció irreductible: a) \(0\dc6\) &nbsp; b) \(0\dc45\) &nbsp; c) \(1\dc2\) &nbsp; d) \(0\dc004\)", r"Escribe como fracción irreducible: a) \(0\dc6\) &nbsp; b) \(0\dc45\) &nbsp; c) \(1\dc2\) &nbsp; d) \(0\dc004\)", r"Write as a fraction in simplest form: a) \(0\dc6\) &nbsp; b) \(0\dc45\) &nbsp; c) \(1\dc2\) &nbsp; d) \(0\dc004\)"),
       r'\[\text{a) }\frac{6}{10}=\boxed{\frac{3}{5}}\qquad\text{b) }\frac{45}{100}=\boxed{\frac{9}{20}}\qquad\text{c) }\frac{12}{10}=\boxed{\frac{6}{5}}\qquad\text{d) }\frac{4}{1000}=\boxed{\frac{1}{250}}\]'))
for a, b in [('0.6', Fr(3, 5)), ('0.45', Fr(9, 20)), ('1.2', Fr(6, 5)), ('0.004', Fr(1, 250))]: ck(Fr(a), b)
s5 += level(2, 2,
  prob(L(r"Escriu en forma decimal i classifica: a) \(\frac{9}{20}\) &nbsp; b) \(\frac{5}{9}\) &nbsp; c) \(\frac{7}{12}\)", r"Escribe en forma decimal y clasifica: a) \(\frac{9}{20}\) &nbsp; b) \(\frac{5}{9}\) &nbsp; c) \(\frac{7}{12}\)", r"Write as decimals and classify: a) \(\frac{9}{20}\) &nbsp; b) \(\frac{5}{9}\) &nbsp; c) \(\frac{7}{12}\)"),
       r'\[\text{a) }9:20=\boxed{0\dc45}\ \ (\tri{exacte}{exacto}{terminating})\]',
       r'\[\text{b) }5:9=0\dc555\ldots=\boxed{0\dc\overline{5}}\ \ (\tri{periòdic pur}{periódico puro}{purely recurring})\]',
       r'\[\text{c) }7:12=0\dc58333\ldots=\boxed{0\dc58\overline{3}}\ \ (\tri{periòdic mixt}{periódico mixto}{mixed recurring})\]'))
ck(Fr(9, 20), Fr('0.45')); assert str(Dm(7) / 12).startswith('0.58333'); assert str(Dm(5) / 9).startswith('0.5555')
s5 += level(3, 3,
  prob(L(r"Ordena de menor a major: \(\ 0\dc7;\ \frac{2}{3};\ 0\dc67;\ \frac{3}{4};\ 0\dc\overline{6}\)", r"Ordena de menor a mayor: \(\ 0\dc7;\ \frac{2}{3};\ 0\dc67;\ \frac{3}{4};\ 0\dc\overline{6}\)", r"Order from smallest to largest: \(\ 0\dc7;\ \frac{2}{3};\ 0\dc67;\ \frac{3}{4};\ 0\dc\overline{6}\)"),
       P(r"Passem les fraccions a decimal: \(\frac{2}{3}=0\dc666\ldots\) (és el mateix nombre que \(0\dc\overline{6}\)) i \(\frac{3}{4}=0\dc75\). Comparem xifra a xifra:", r"Pasamos las fracciones a decimal: \(\frac{2}{3}=0\dc666\ldots\) (es el mismo número que \(0\dc\overline{6}\)) y \(\frac{3}{4}=0\dc75\). Comparamos cifra a cifra:", r"Turn the fractions into decimals: \(\frac{2}{3}=0\dc666\ldots\) (the same number as \(0\dc\overline{6}\)) and \(\frac{3}{4}=0\dc75\). Compare digit by digit:"),
       r'\[\frac{2}{3}=0\dc\overline{6}<0\dc67<0\dc7<\frac{3}{4}\]'))
s5 += practice([
  ('★', L(r"a) Escriu \(0\dc8\) i \(0\dc25\) com a fracció irreductible. b) Escriu \(\frac{3}{5}\) i \(\frac{7}{100}\) en forma decimal.", r"a) Escribe \(0\dc8\) y \(0\dc25\) como fracción irreducible. b) Escribe \(\frac{3}{5}\) y \(\frac{7}{100}\) en forma decimal.", r"a) Write \(0\dc8\) and \(0\dc25\) as fractions in simplest form. b) Write \(\frac{3}{5}\) and \(\frac{7}{100}\) as decimals.")),
  ('★★', L(r"c) Classifica: \(\frac{1}{6}\), \(\frac{3}{11}\), \(\frac{11}{8}\). d) Escriu \(2\dc75\) com a fracció irreductible.", r"c) Clasifica: \(\frac{1}{6}\), \(\frac{3}{11}\), \(\frac{11}{8}\). d) Escribe \(2\dc75\) como fracción irreducible.", r"c) Classify: \(\frac{1}{6}\), \(\frac{3}{11}\), \(\frac{11}{8}\). d) Write \(2\dc75\) as a fraction in simplest form.")),
  ('★★★', L(r"e) Quin és més gran, \(\frac{5}{8}\) o \(0\dc62\)? f) Troba una fracció de denominador 3 que estiga entre \(1\dc5\) i 2.", r"e) ¿Cuál es mayor, \(\frac{5}{8}\) o \(0\dc62\)? f) Encuentra una fracción de denominador 3 que esté entre \(1\dc5\) y 2.", r"e) Which is bigger, \(\frac{5}{8}\) or \(0\dc62\)? f) Find a fraction with denominator 3 between \(1\dc5\) and 2."))],
  P(r"a) \(\frac{4}{5}\), \(\frac{1}{4}\). &nbsp; b) \(0\dc6\), \(0\dc07\).", r"a) \(\frac{4}{5}\), \(\frac{1}{4}\). &nbsp; b) \(0\dc6\), \(0\dc07\).", r"a) \(\frac{4}{5}\), \(\frac{1}{4}\). &nbsp; b) \(0\dc6\), \(0\dc07\).")
  + P(r"c) \(0\dc1\overline{6}\) periòdic mixt; \(0\dc\overline{27}\) periòdic pur; \(1\dc375\) exacte. &nbsp; d) \(\frac{275}{100}=\frac{11}{4}\).", r"c) \(0\dc1\overline{6}\) periódico mixto; \(0\dc\overline{27}\) periódico puro; \(1\dc375\) exacto. &nbsp; d) \(\frac{275}{100}=\frac{11}{4}\).", r"c) \(0\dc1\overline{6}\) mixed recurring; \(0\dc\overline{27}\) purely recurring; \(1\dc375\) terminating. &nbsp; d) \(\frac{275}{100}=\frac{11}{4}\).")
  + P(r"e) \(\frac{5}{8}=0\dc625>0\dc62\). &nbsp; f) \(\frac{5}{3}=1\dc\overline{6}\).", r"e) \(\frac{5}{8}=0\dc625>0\dc62\). &nbsp; f) \(\frac{5}{3}=1\dc\overline{6}\).", r"e) \(\frac{5}{8}=0\dc625>0\dc62\). &nbsp; f) \(\frac{5}{3}=1\dc\overline{6}\)."))
ck(Fr(275, 100), Fr(11, 4)); ck(Fr(11, 8), Fr('1.375')); assert str(Dm(3) / 11).startswith('0.272727')
