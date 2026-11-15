# Apartats 2.1-2.4 (nombres decimals) dels apunts de la Unitat 2 de 2n ESO.
# Les asserts ck() comproven els resultats escrits a mà.
from comu import *

# ============================================================ 2.1
s1 = box('def', L('Què és un nombre decimal?', '¿Qué es un número decimal?', 'What is a decimal number?'),
  P(r"Els <strong>nombres decimals</strong> expressen quantitats que no són senceres: \(2\dc35\) €, \(1\dc68\) m, \(36\dc6\) °C… Tenen una <strong>part entera</strong> i una <strong>part decimal</strong>, separades per la <strong>coma</strong>. Cada xifra de la part decimal val deu vegades menys que la de la seua esquerra:",
    r"Los <strong>números decimales</strong> expresan cantidades que no son enteras: \(2\dc35\) €, \(1\dc68\) m, \(36\dc6\) °C… Tienen una <strong>parte entera</strong> y una <strong>parte decimal</strong>, separadas por la <strong>coma</strong>. Cada cifra de la parte decimal vale diez veces menos que la de su izquierda:",
    r"<strong>Decimal numbers</strong> express amounts that aren't whole: \(2\dc35\) €, \(1\dc68\) m, \(36\dc6\) °C… They have a <strong>whole-number part</strong> and a <strong>decimal part</strong>, separated by the <strong>decimal comma</strong> (a point in English-speaking countries). Each decimal digit is worth ten times less than the one on its left:")
  + r'<div class="decparts"><span class="dp-i">245</span><span class="dp-c">,</span><span class="dp-f">378</span></div>'
  + table(['C', 'D', 'U', ',', 'd', 'c', 'm'],
          [['<span class="pi">2</span>', '<span class="pi">4</span>', '<span class="pi">5</span>', '<span class="pc">,</span>', '<span class="pf">3</span>', '<span class="pf">7</span>', '<span class="pf">8</span>'],
           ['200', '40', '5', '', r'\(0\dc3\)', r'\(0\dc07\)', r'\(0\dc008\)']], 'data pv')
  + P(r"<strong>d</strong> = " + L("dècimes", "décimas", "tenths") + r" \(\left(\frac{1}{10}=0\dc1\right)\), &nbsp; <strong>c</strong> = " + L("centèsimes", "centésimas", "hundredths") + r" \(\left(\frac{1}{100}=0\dc01\right)\), &nbsp; <strong>m</strong> = " + L("mil·lèsimes", "milésimas", "thousandths") + r" \(\left(\frac{1}{1000}=0\dc001\right)\).",
      r"<strong>d</strong> = " + L("dècimes", "décimas", "tenths") + r" \(\left(\frac{1}{10}=0\dc1\right)\), &nbsp; <strong>c</strong> = " + L("centèsimes", "centésimas", "hundredths") + r" \(\left(\frac{1}{100}=0\dc01\right)\), &nbsp; <strong>m</strong> = " + L("mil·lèsimes", "milésimas", "thousandths") + r" \(\left(\frac{1}{1000}=0\dc001\right)\).",
      r"<strong>t</strong>enths \(\left(\frac{1}{10}=0\dc1\right)\), &nbsp; <strong>h</strong>undredths \(\left(\frac{1}{100}=0\dc01\right)\), &nbsp; <strong>th</strong>ousandths \(\left(\frac{1}{1000}=0\dc001\right)\).")
  + P(r"Es llegeix: <em>245 unitats i 378 mil·lèsimes</em> (diem el nom de l'<strong>última</strong> xifra). Els zeros a la dreta de l'última xifra decimal no canvien el valor: \(3\dc5=3\dc50=3\dc500\).",
      r"Se lee: <em>245 unidades y 378 milésimas</em> (decimos el nombre de la <strong>última</strong> cifra). Los ceros a la derecha de la última cifra decimal no cambian el valor: \(3\dc5=3\dc50=3\dc500\).",
      r"We read it as <em>245 units and 378 thousandths</em> (we name the <strong>last</strong> digit). Zeros to the right of the last decimal digit don't change the value: \(3\dc5=3\dc50=3\dc500\)."))
s1 += box('prop', L('Comparar, truncar i arrodonir', 'Comparar, truncar y redondear', 'Comparing, truncating and rounding'),
  ul(L(r"Per a <strong>comparar</strong> dos decimals mirem primer la part entera; si és igual, comparem xifra a xifra (dècimes, centèsimes…). Ajuda igualar els decimals amb zeros: \(\ 3\dc5\ \text{?}\ 3\dc48\ \to\ 3\dc50>3\dc48\).",
         r"Para <strong>comparar</strong> dos decimales miramos primero la parte entera; si es igual, comparamos cifra a cifra (décimas, centésimas…). Ayuda igualar los decimales con ceros: \(\ 3\dc5\ \text{?}\ 3\dc48\ \to\ 3\dc50>3\dc48\).",
         r"To <strong>compare</strong> two decimals, look at the whole-number part first; if it's the same, compare digit by digit (tenths, hundredths…). Padding with zeros helps: \(\ 3\dc5\ \text{?}\ 3\dc48\ \to\ 3\dc50>3\dc48\)."),
     L(r"<strong>Truncar</strong> és tallar: eliminem les xifres a partir d'una posició. \(\ 7\dc2961\to7\dc29\) (a les centèsimes).",
       r"<strong>Truncar</strong> es cortar: eliminamos las cifras a partir de una posición. \(\ 7\dc2961\to7\dc29\) (a las centésimas).",
       r"<strong>Truncating</strong> means cutting: drop every digit after a position. \(\ 7\dc2961\to7\dc29\) (to hundredths)."),
     L(r"<strong>Arrodonir</strong>: mirem la primera xifra que eliminem. Si és 0, 1, 2, 3 o 4, l'última xifra es queda igual; si és 5, 6, 7, 8 o 9, li sumem 1. \(\ 7\dc2961\approx7\dc30\) (a les centèsimes).",
       r"<strong>Redondear</strong>: miramos la primera cifra que eliminamos. Si es 0, 1, 2, 3 o 4, la última cifra se queda igual; si es 5, 6, 7, 8 o 9, le sumamos 1. \(\ 7\dc2961\approx7\dc30\) (a las centésimas).",
       r"<strong>Rounding</strong>: look at the first digit you drop. If it's 0, 1, 2, 3 or 4, the last digit stays; if it's 5, 6, 7, 8 or 9, add 1 to it. \(\ 7\dc2961\approx7\dc30\) (to hundredths).")))
s1 += widget('w-round', '✂️', L('Truncar i arrodonir', 'Truncar y redondear', 'Truncate and round'),
    f'  <div class="wrow">{nin("x", "Nombre", "Número", "Number", "7,2961", "m")}{gseg("k", [("0", L("Unitats", "Unidades", "Units")), ("1", L("Dècimes", "Décimas", "Tenths")), ("2", L("Centèsimes", "Centésimas", "Hundredths")), ("3", L("Mil·lèsimes", "Milésimas", "Thousandths"))], "2")}</div>\n'
    + '  ' + quick([('7,2961', '7,2961'), ('15,8962', '15,8962'), ('2,996', '2,996'), ('0,4449', '0,4449'), ('3,14159', '3,14159'), ('129,5', '129,5')]) + '\n')
s1 += drill('cmpd', 'Entrena: compara decimals', 'Entrena: compara decimales', 'Train: compare decimals')
s1 += drill('round', 'Entrena: arrodoneix', 'Entrena: redondea', 'Train: rounding')
s1 += level(1, 1,
  prob(L(r"Ordena de menor a major: \(\ 2\dc5;\ 2\dc05;\ 2\dc55;\ 2\dc505;\ 2\dc15\)", r"Ordena de menor a mayor: \(\ 2\dc5;\ 2\dc05;\ 2\dc55;\ 2\dc505;\ 2\dc15\)", r"Order from smallest to largest: \(\ 2\dc5;\ 2\dc05;\ 2\dc55;\ 2\dc505;\ 2\dc15\)"),
       P(r"Tots tenen la mateixa part entera. Els escrivim amb tres decimals i comparem:", r"Todos tienen la misma parte entera. Los escribimos con tres decimales y comparamos:", r"They all have the same whole-number part. Write them with three decimals and compare:")
       + r'\[2\dc050<2\dc150<2\dc500<2\dc505<2\dc550\]',
       r'\[\boxed{2\dc05<2\dc15<2\dc5<2\dc505<2\dc55}\]'))
assert sorted(['2.5', '2.05', '2.55', '2.505', '2.15'], key=Dm) == ['2.05', '2.15', '2.5', '2.505', '2.55']
s1 += level(2, 2,
  prob(L(r"Arrodoneix \(15\dc8962\) a les unitats, a les dècimes, a les centèsimes i a les mil·lèsimes.", r"Redondea \(15\dc8962\) a las unidades, a las décimas, a las centésimas y a las milésimas.", r"Round \(15\dc8962\) to the units, tenths, hundredths and thousandths."),
       r'\[\boxed{16}\qquad\boxed{15\dc9}\qquad\boxed{15\dc90}\qquad\boxed{15\dc896}\]',
       P(r"Fixa't en les centèsimes: \(15\dc89|62\): el 6 fa pujar el 9, que passa a 10 i se'n porta una: \(15\dc90\).", r"Fíjate en las centésimas: \(15\dc89|62\): el 6 hace subir el 9, que pasa a 10 y se lleva una: \(15\dc90\).", r"Look at the hundredths: \(15\dc89|62\): the 6 pushes the 9 up to 10, carrying one: \(15\dc90\).")))
for k, v in [(0, '16'), (1, '15.9'), (2, '15.90'), (3, '15.896')]: ck(Dm('15.8962').quantize(Dm(1).scaleb(-k), 'ROUND_HALF_UP'), v)
s1 += level(3, 3,
  prob(L(r"Escriu tres nombres compresos entre \(4\dc7\) i \(4\dc71\). Quants n'hi ha?", r"Escribe tres números comprendidos entre \(4\dc7\) y \(4\dc71\). ¿Cuántos hay?", r"Write three numbers between \(4\dc7\) and \(4\dc71\). How many are there?"),
       P(r"Afegim zeros: \(4\dc700\) i \(4\dc710\). Entre ells hi ha, per exemple, \(4\dc701\), \(4\dc705\) i \(4\dc7099\).", r"Añadimos ceros: \(4\dc700\) y \(4\dc710\). Entre ellos hay, por ejemplo, \(4\dc701\), \(4\dc705\) y \(4\dc7099\).", r"Pad with zeros: \(4\dc700\) and \(4\dc710\). Between them are, for example, \(4\dc701\), \(4\dc705\) and \(4\dc7099\)."),
       P(r"Sempre podem afegir més xifres decimals: entre dos decimals diferents hi ha <strong>infinits</strong> nombres decimals.", r"Siempre podemos añadir más cifras decimales: entre dos decimales distintos hay <strong>infinitos</strong> números decimales.", r"We can always add more decimal digits: between two different decimals there are <strong>infinitely many</strong> decimals.")))
s1 += practice([
  ('★', L(r"a) Com es llegeix \(0\dc408\)? &nbsp; b) Escriu amb xifres «dotze unitats i sis centèsimes».", r"a) ¿Cómo se lee \(0\dc408\)? &nbsp; b) Escribe con cifras «doce unidades y seis centésimas».", r"a) How do you read \(0\dc408\)? &nbsp; b) Write in figures “twelve units and six hundredths”.")),
  ('★★', L(r"c) Trunca i arrodoneix \(0\dc7049\) a les centèsimes. &nbsp; d) Ordena: \(0\dc09;\ 0\dc1;\ 0\dc099;\ 0\dc101\).", r"c) Trunca y redondea \(0\dc7049\) a las centésimas. &nbsp; d) Ordena: \(0\dc09;\ 0\dc1;\ 0\dc099;\ 0\dc101\).", r"c) Truncate and round \(0\dc7049\) to hundredths. &nbsp; d) Order: \(0\dc09;\ 0\dc1;\ 0\dc099;\ 0\dc101\).")),
  ('★★★', L(r"e) Quin és el nombre més xicotet amb dues xifres decimals que, arrodonit a les unitats, dona 8?", r"e) ¿Cuál es el número más pequeño con dos cifras decimales que, redondeado a las unidades, da 8?", r"e) What is the smallest number with two decimal places that rounds to 8?"))],
  P(r"a) 408 mil·lèsimes. &nbsp; b) \(12\dc06\). &nbsp; c) \(0\dc70\) i \(0\dc70\). &nbsp; d) \(0\dc09<0\dc099<0\dc1<0\dc101\). &nbsp; e) \(7\dc50\).",
    r"a) 408 milésimas. &nbsp; b) \(12\dc06\). &nbsp; c) \(0\dc70\) y \(0\dc70\). &nbsp; d) \(0\dc09<0\dc099<0\dc1<0\dc101\). &nbsp; e) \(7\dc50\).",
    r"a) 408 thousandths. &nbsp; b) \(12\dc06\). &nbsp; c) \(0\dc70\) and \(0\dc70\). &nbsp; d) \(0\dc09<0\dc099<0\dc1<0\dc101\). &nbsp; e) \(7\dc50\)."))
assert sorted(['0.09', '0.1', '0.099', '0.101'], key=Dm) == ['0.09', '0.099', '0.1', '0.101']
ck(Dm('7.50').quantize(Dm(1), 'ROUND_HALF_UP'), '8'); ck(Dm('7.49').quantize(Dm(1), 'ROUND_HALF_UP'), '7')

# ============================================================ 2.2
s2 = box('def', L('Tipus de nombres decimals', 'Tipos de números decimales', 'Kinds of decimal numbers'),
  P(r"Segons com és la part decimal, hi ha quatre tipus de nombres decimals:", r"Según cómo es la parte decimal, hay cuatro tipos de números decimales:", r"Depending on the decimal part, there are four kinds of decimal numbers:")
  + table([L('Tipus', 'Tipo', 'Kind'), L('Com és la part decimal', 'Cómo es la parte decimal', 'What the decimal part is like'), L('Exemples', 'Ejemplos', 'Examples')],
          [[L('<strong>Exacte</strong>', '<strong>Exacto</strong>', '<strong>Terminating</strong>'), L("Té un nombre <strong>finit</strong> de xifres.", "Tiene un número <strong>finito</strong> de cifras.", "It has <strong>finitely many</strong> digits."), r'\(0\dc75\qquad 12\dc3\qquad 4\dc125\)'],
           [L('<strong>Periòdic pur</strong>', '<strong>Periódico puro</strong>', '<strong>Purely recurring</strong>'), L("Té infinites xifres i un grup (el <strong>període</strong>) es repeteix <strong>just després de la coma</strong>.", "Tiene infinitas cifras y un grupo (el <strong>periodo</strong>) se repite <strong>justo después de la coma</strong>.", "Infinitely many digits; a block (the <strong>period</strong>) repeats <strong>straight after the comma</strong>."), r'\(0\dc333\ldots=0\dc\overline{3}\qquad 2\dc\overline{45}\)'],
           [L('<strong>Periòdic mixt</strong>', '<strong>Periódico mixto</strong>', '<strong>Mixed recurring</strong>'), L("Té infinites xifres; abans del període hi ha xifres que no es repeteixen (l'<strong>anteperíode</strong>).", "Tiene infinitas cifras; antes del periodo hay cifras que no se repiten (el <strong>anteperiodo</strong>).", "Infinitely many digits; some non-repeating digits come before the period."), r'\(0\dc8333\ldots=0\dc8\overline{3}\qquad 1\dc2\overline{36}\)'],
           [L('<strong>No exacte i no periòdic</strong>', '<strong>No exacto y no periódico</strong>', '<strong>Non-terminating, non-recurring</strong>'), L("Té infinites xifres que <strong>no</strong> es repeteixen mai.", "Tiene infinitas cifras que <strong>no</strong> se repiten nunca.", "Infinitely many digits that <strong>never</strong> repeat."), r'\(\pi=3\dc14159\ldots\qquad 0\dc101001000\ldots\)']])
  + P(r"El període s'indica amb una ratlla (o un arc) damunt de les xifres que es repeteixen: \(\ 5\dc272727\ldots=5\dc\overline{27}\), \(\ 3\dc04111\ldots=3\dc04\overline{1}\).",
      r"El periodo se indica con una raya (o un arco) encima de las cifras que se repiten: \(\ 5\dc272727\ldots=5\dc\overline{27}\), \(\ 3\dc04111\ldots=3\dc04\overline{1}\).",
      r"The period is shown with a bar (or an arc) over the repeating digits: \(\ 5\dc272727\ldots=5\dc\overline{27}\), \(\ 3\dc04111\ldots=3\dc04\overline{1}\)."))
s2 += box('prop', L('Les parts d’un decimal periòdic', 'Las partes de un decimal periódico', 'The parts of a recurring decimal'),
  '<div class="gdig big"><span class="ge">3</span><span class="gc">,</span><span class="ga">04</span><span class="gp">1</span><span class="gp2">11…</span></div>'
  + '<div class="glab">' + L('<span class="ge">part entera: 3</span> · <span class="ga">anteperíode: 04</span> · <span class="gp">període: 1</span>', '<span class="ge">parte entera: 3</span> · <span class="ga">anteperiodo: 04</span> · <span class="gp">periodo: 1</span>', '<span class="ge">whole part: 3</span> · <span class="ga">non-repeating part: 04</span> · <span class="gp">period: 1</span>') + '</div>'
  + note(r"Els decimals exactes i els periòdics (purs i mixtos) es poden escriure sempre com a <strong>fracció</strong> (ho veurem a l'apartat 2.6). Els no exactes i no periòdics, com \(\pi\) o \(\sqrt{2}=1\dc41421\ldots\), <strong>no</strong>: s'anomenen <strong>irracionals</strong>.",
         r"Los decimales exactos y los periódicos (puros y mixtos) se pueden escribir siempre como <strong>fracción</strong> (lo veremos en el apartado 2.6). Los no exactos y no periódicos, como \(\pi\) o \(\sqrt{2}=1\dc41421\ldots\), <strong>no</strong>: se llaman <strong>irracionales</strong>.",
         r"Terminating and recurring decimals can always be written as a <strong>fraction</strong> (see section 2.6). Non-terminating, non-recurring ones, like \(\pi\) or \(\sqrt{2}=1\dc41421\ldots\), <strong>can't</strong>: they are called <strong>irrational</strong>."))
s2 += level(1, 1,
  prob(L(r"Classifica i, si són periòdics, indica'n el període i l'anteperíode: a) \(4\dc252525\ldots\) &nbsp; b) \(0\dc125\) &nbsp; c) \(7\dc31666\ldots\) &nbsp; d) \(1\dc010010001\ldots\)",
         r"Clasifica y, si son periódicos, indica su periodo y su anteperiodo: a) \(4\dc252525\ldots\) &nbsp; b) \(0\dc125\) &nbsp; c) \(7\dc31666\ldots\) &nbsp; d) \(1\dc010010001\ldots\)",
         r"Classify them and, if they recur, give the period and the non-repeating part: a) \(4\dc252525\ldots\) &nbsp; b) \(0\dc125\) &nbsp; c) \(7\dc31666\ldots\) &nbsp; d) \(1\dc010010001\ldots\)"),
       P(r"a) \(4\dc\overline{25}\): periòdic pur, període 25. &nbsp; b) Exacte.", r"a) \(4\dc\overline{25}\): periódico puro, periodo 25. &nbsp; b) Exacto.", r"a) \(4\dc\overline{25}\): purely recurring, period 25. &nbsp; b) Terminating."),
       P(r"c) \(7\dc31\overline{6}\): periòdic mixt, anteperíode 31 i període 6. &nbsp; d) No exacte i no periòdic: el nombre de zeros va creixent i cap grup es repeteix sempre igual.", r"c) \(7\dc31\overline{6}\): periódico mixto, anteperiodo 31 y periodo 6. &nbsp; d) No exacto y no periódico: el número de ceros va creciendo y ningún grupo se repite siempre igual.", r"c) \(7\dc31\overline{6}\): mixed recurring, non-repeating part 31 and period 6. &nbsp; d) Neither: the number of zeros keeps growing, so no block repeats.")))
s2 += level(2, 2,
  prob(L(r"Ordena de menor a major: \(\ 0\dc\overline{3};\ 0\dc3;\ 0\dc3\overline{4};\ 0\dc\overline{34};\ 0\dc33\)", r"Ordena de menor a mayor: \(\ 0\dc\overline{3};\ 0\dc3;\ 0\dc3\overline{4};\ 0\dc\overline{34};\ 0\dc33\)", r"Order from smallest to largest: \(\ 0\dc\overline{3};\ 0\dc3;\ 0\dc3\overline{4};\ 0\dc\overline{34};\ 0\dc33\)"),
       P(r"Escrivim unes quantes xifres de cada un i comparem xifra a xifra:", r"Escribimos unas cuantas cifras de cada uno y comparamos cifra a cifra:", r"Write a few digits of each and compare digit by digit:")
       + r'\[0\dc3000\ldots\quad 0\dc3300\ldots\quad 0\dc3333\ldots\quad 0\dc3434\ldots\quad 0\dc3444\ldots\]',
       r'\[\boxed{0\dc3<0\dc33<0\dc\overline{3}<0\dc\overline{34}<0\dc3\overline{4}}\]'))
assert Fr(3, 10) < Fr(33, 100) < Fr(1, 3) < Fr(34, 99) < gen(0, '3', '4')
s2 += level(3, 3,
  prob(L(r"Escriu un nombre periòdic pur, un de periòdic mixt i un d'exacte que estiguen tots tres entre \(2\dc1\) i \(2\dc2\).", r"Escribe un número periódico puro, uno periódico mixto y uno exacto que estén los tres entre \(2\dc1\) y \(2\dc2\).", r"Write a purely recurring, a mixed recurring and a terminating number, all between \(2\dc1\) and \(2\dc2\)."),
       P(r"Per exemple: periòdic pur \(2\dc\overline{15}=2\dc1515\ldots\); periòdic mixt \(2\dc1\overline{7}=2\dc1777\ldots\); exacte \(2\dc125\). (Hi ha infinites respostes.)", r"Por ejemplo: periódico puro \(2\dc\overline{15}=2\dc1515\ldots\); periódico mixto \(2\dc1\overline{7}=2\dc1777\ldots\); exacto \(2\dc125\). (Hay infinitas respuestas.)", r"For example: purely recurring \(2\dc\overline{15}=2\dc1515\ldots\); mixed recurring \(2\dc1\overline{7}=2\dc1777\ldots\); terminating \(2\dc125\). (There are infinitely many answers.)")))
assert Fr(21, 10) < 2 + Fr(15, 99) < Fr(22, 10) and Fr(21, 10) < gen(2, '1', '7') < Fr(22, 10)
s2 += practice([
  ('★', L(r"a) Escriu amb la ratlla del període: \(0\dc777\ldots\), \(\ 3\dc1252525\ldots\), \(\ 12\dc408408\ldots\)", r"a) Escribe con la raya del periodo: \(0\dc777\ldots\), \(\ 3\dc1252525\ldots\), \(\ 12\dc408408\ldots\)", r"a) Write with the period bar: \(0\dc777\ldots\), \(\ 3\dc1252525\ldots\), \(\ 12\dc408408\ldots\)")),
  ('★★', L(r"b) Classifica: \(5\dc\overline{6}\), \(\ 0\dc0\overline{9}\), \(\ 8\dc25\), \(\ 2\dc1234567891011\ldots\) (les xifres són els naturals seguits).", r"b) Clasifica: \(5\dc\overline{6}\), \(\ 0\dc0\overline{9}\), \(\ 8\dc25\), \(\ 2\dc1234567891011\ldots\) (las cifras son los naturales seguidos).", r"b) Classify: \(5\dc\overline{6}\), \(\ 0\dc0\overline{9}\), \(\ 8\dc25\), \(\ 2\dc1234567891011\ldots\) (the digits are the natural numbers in a row).")),
  ('★★★', L(r"c) És més gran \(1\dc\overline{9}\) o \(1\dc99\)? Pensa quant valdria la diferència.", r"c) ¿Es mayor \(1\dc\overline{9}\) o \(1\dc99\)? Piensa cuánto valdría la diferencia.", r"c) Which is bigger, \(1\dc\overline{9}\) or \(1\dc99\)? Think about the difference."))],
  P(r"a) \(0\dc\overline{7}\); \(\ 3\dc1\overline{25}\); \(\ 12\dc\overline{408}\). &nbsp; b) pur; mixt; exacte; no exacte i no periòdic. &nbsp; c) \(1\dc\overline{9}>1\dc99\), i de fet \(1\dc\overline{9}=2\) (ho comprovaràs amb la fracció generatriu a l'apartat 2.6).",
    r"a) \(0\dc\overline{7}\); \(\ 3\dc1\overline{25}\); \(\ 12\dc\overline{408}\). &nbsp; b) puro; mixto; exacto; no exacto y no periódico. &nbsp; c) \(1\dc\overline{9}>1\dc99\), y de hecho \(1\dc\overline{9}=2\) (lo comprobarás con la fracción generatriz en el apartado 2.6).",
    r"a) \(0\dc\overline{7}\); \(\ 3\dc1\overline{25}\); \(\ 12\dc\overline{408}\). &nbsp; b) pure; mixed; terminating; neither. &nbsp; c) \(1\dc\overline{9}>1\dc99\); in fact \(1\dc\overline{9}=2\) (you'll check it with the generating fraction in section 2.6)."))
assert gen(1, '', '9') == 2

# ============================================================ 2.3
s3 = box('def', L('Sumar, restar i multiplicar decimals', 'Sumar, restar y multiplicar decimales', 'Adding, subtracting and multiplying decimals'),
  ul(L(r"<strong>Suma i resta</strong>: col·loquem els nombres amb les <strong>comes alineades</strong> (unitats davall d'unitats, dècimes davall de dècimes…), completem amb zeros i operem com amb naturals. La coma del resultat va al mateix lloc. \(\ 23\dc45+7\dc8=31\dc25\)",
         r"<strong>Suma y resta</strong>: colocamos los números con las <strong>comas alineadas</strong> (unidades debajo de unidades, décimas debajo de décimas…), completamos con ceros y operamos como con naturales. La coma del resultado va en el mismo lugar. \(\ 23\dc45+7\dc8=31\dc25\)",
         r"<strong>Adding and subtracting</strong>: write the numbers with the <strong>commas lined up</strong> (units under units, tenths under tenths…), fill in zeros and work as with whole numbers. The comma goes in the same place in the answer. \(\ 23\dc45+7\dc8=31\dc25\)"),
     L(r"<strong>Multiplicació</strong>: multipliquem com si no hi haguera comes i, al resultat, separem tantes xifres decimals com <strong>sumen</strong> els dos factors. \(\ 3\dc25\cdot1\dc4\to325\cdot14=4550\to4\dc550=4\dc55\) (2 + 1 = 3 decimals).",
       r"<strong>Multiplicación</strong>: multiplicamos como si no hubiera comas y, en el resultado, separamos tantas cifras decimales como <strong>suman</strong> los dos factores. \(\ 3\dc25\cdot1\dc4\to325\cdot14=4550\to4\dc550=4\dc55\) (2 + 1 = 3 decimales).",
       r"<strong>Multiplying</strong>: multiply as if there were no commas and, in the answer, mark off as many decimal places as the two factors have <strong>together</strong>. \(\ 3\dc25\cdot1\dc4\to325\cdot14=4550\to4\dc550=4\dc55\) (2 + 1 = 3 decimals).")))
ck(Dm('23.45') + Dm('7.8'), '31.25'); ck(Dm('3.25') * Dm('1.4'), '4.55')
s3 += widget('w-col', '🧾', L('Operacions en columna', 'Operaciones en columna', 'Column arithmetic'),
  f'  <div class="wrow">{nin("a", "", "", "", "23,45", "m")}{gseg("op", [("+", "+"), ("-", "−"), ("*", "×")], "+")}{nin("b", "", "", "", "7,8", "m")}</div>\n'
  + '  ' + quick([('23,45;7,8;+', '23,45 + 7,8'), ('15;6,47;-', '15 − 6,47'), ('100;0,01;-', '100 − 0,01'), ('3,25;1,4;*', '3,25 × 1,4'), ('0,4;0,02;*', '0,4 × 0,02'), ('12,5;0,8;*', '12,5 × 0,8')]) + '\n')
s3 += box('prop', L('Multiplicar i dividir per la unitat seguida de zeros', 'Multiplicar y dividir por la unidad seguida de ceros', 'Multiplying and dividing by 10, 100, 1000…'),
  ul(L(r"Per a <strong>multiplicar</strong> per 10, 100, 1000…, movem la coma a la <strong>dreta</strong> tants llocs com zeros hi ha (si falten xifres, afegim zeros): \(\ 0\dc052\cdot1000=52\).", r"Para <strong>multiplicar</strong> por 10, 100, 1000…, movemos la coma a la <strong>derecha</strong> tantos lugares como ceros hay (si faltan cifras, añadimos ceros): \(\ 0\dc052\cdot1000=52\).", r"To <strong>multiply</strong> by 10, 100, 1000…, move the comma <strong>right</strong> one place per zero (add zeros if you run out of digits): \(\ 0\dc052\cdot1000=52\)."),
     L(r"Per a <strong>dividir</strong> entre 10, 100, 1000…, movem la coma a l'<strong>esquerra</strong>: \(\ 45\dc2:1000=0\dc0452\).", r"Para <strong>dividir</strong> entre 10, 100, 1000…, movemos la coma a la <strong>izquierda</strong>: \(\ 45\dc2:1000=0\dc0452\).", r"To <strong>divide</strong> by 10, 100, 1000…, move the comma <strong>left</strong>: \(\ 45\dc2:1000=0\dc0452\)."),
     L(r"Multiplicar per \(0\dc1\), \(0\dc01\)… és com dividir entre 10, 100…: \(\ 250\cdot0\dc1=25\).", r"Multiplicar por \(0\dc1\), \(0\dc01\)… es como dividir entre 10, 100…: \(\ 250\cdot0\dc1=25\).", r"Multiplying by \(0\dc1\), \(0\dc01\)… is like dividing by 10, 100…: \(\ 250\cdot0\dc1=25\).")))
ck(Dm('0.052') * 1000, '52'); ck(Dm('45.2') / 1000, '0.0452'); ck(250 * Dm('0.1'), '25')
s3 += widget('w-p10', '↔️', L('Movem la coma', 'Movemos la coma', 'Moving the comma'),
    f'  <div class="wrow">{nin("x", "Nombre", "Número", "Number", "0,052", "m")}{gseg("op", [("*", "×"), (":", ":")], "*")}{gseg("p", [("1", "10"), ("2", "100"), ("3", "1000")], "3")}</div>\n'
    + '  ' + quick([('0,052;*;3', '0,052 × 1000'), ('3,7;*;2', '3,7 × 100'), ('45,2;:;3', '45,2 : 1000'), ('8;:;2', '8 : 100'), ('6,15;*;1', '6,15 × 10'), ('0,3;:;1', '0,3 : 10')]) + '\n')
s3 += drill('ops', 'Entrena: suma, resta i multiplica', 'Entrena: suma, resta y multiplica', 'Train: add, subtract, multiply')
s3 += drill('p10', 'Entrena: per 10, 100 i 1000', 'Entrena: por 10, 100 y 1000', 'Train: by 10, 100 and 1000')
s3 += level(1, 1,
  prob(L(r"Calcula: a) \(40-12\dc35\) &nbsp; b) \(3\dc06+12\dc9+0\dc4\) &nbsp; c) \(0\dc6\cdot0\dc05\)", r"Calcula: a) \(40-12\dc35\) &nbsp; b) \(3\dc06+12\dc9+0\dc4\) &nbsp; c) \(0\dc6\cdot0\dc05\)", r"Work out: a) \(40-12\dc35\) &nbsp; b) \(3\dc06+12\dc9+0\dc4\) &nbsp; c) \(0\dc6\cdot0\dc05\)"),
       r'\[\text{a) }40\dc00-12\dc35=\boxed{27\dc65}\qquad\text{b) }3\dc06+12\dc90+0\dc40=\boxed{16\dc36}\]',
       r'\[\text{c) }6\cdot5=30,\ 1+2=3\ \tri{decimals}{decimales}{decimals}:\ 0\dc030=\boxed{0\dc03}\]'))
ck(40 - Dm('12.35'), '27.65'); ck(Dm('3.06') + Dm('12.9') + Dm('0.4'), '16.36'); ck(Dm('0.6') * Dm('0.05'), '0.03')
s3 += level(2, 2,
  prob(L(r"Compre \(2\dc5\) kg de pomes a \(1\dc86\) €/kg i \(0\dc75\) kg de formatge a \(14\dc20\) €/kg. Pague amb un bitllet de 20 €. Quant em tornen?", r"Compro \(2\dc5\) kg de manzanas a \(1\dc86\) €/kg y \(0\dc75\) kg de queso a \(14\dc20\) €/kg. Pago con un billete de 20 €. ¿Cuánto me devuelven?", r"I buy \(2\dc5\) kg of apples at \(1\dc86\) €/kg and \(0\dc75\) kg of cheese at \(14\dc20\) €/kg. I pay with a 20 € note. How much change do I get?"),
       r'\[2\dc5\cdot1\dc86=4\dc65\ €\qquad 0\dc75\cdot14\dc20=10\dc65\ €\]',
       r'\[4\dc65+10\dc65=15\dc30\ €\qquad 20-15\dc30=\boxed{4\dc70\ €}\]'))
ck(Dm('2.5') * Dm('1.86'), '4.65'); ck(Dm('0.75') * Dm('14.20'), '10.65'); ck(20 - Dm('15.30'), '4.70')
s3 += level(3, 3,
  prob(L(r"Un full de paper fa \(0\dc012\) cm de gruix. Quant fa un paquet de 500 fulls? I una pila de 1000 paquets, en metres?", r"Una hoja de papel tiene \(0\dc012\) cm de grosor. ¿Cuánto mide un paquete de 500 hojas? ¿Y una pila de 1000 paquetes, en metros?", r"A sheet of paper is \(0\dc012\) cm thick. How thick is a pack of 500 sheets? And a stack of 1000 packs, in metres?"),
       r'\[0\dc012\cdot500=0\dc012\cdot5\cdot100=0\dc06\cdot100=\boxed{6\ \text{cm}}\]',
       r'\[6\cdot1000=6000\ \text{cm}=6000:100=\boxed{60\ \text{m}}\]'))
ck(Dm('0.012') * 500, '6')
s3 += practice([
  ('★', L(r"a) \(15-6\dc47\) &nbsp; b) \(4\dc6\cdot3\) &nbsp; c) \(2\dc35\cdot0\dc4\) &nbsp; d) \(3\dc7\cdot100\)", r"a) \(15-6\dc47\) &nbsp; b) \(4\dc6\cdot3\) &nbsp; c) \(2\dc35\cdot0\dc4\) &nbsp; d) \(3\dc7\cdot100\)", r"a) \(15-6\dc47\) &nbsp; b) \(4\dc6\cdot3\) &nbsp; c) \(2\dc35\cdot0\dc4\) &nbsp; d) \(3\dc7\cdot100\)")),
  ('★★', L(r"e) \(8:100\) &nbsp; f) \(0\dc07\cdot0\dc3\) &nbsp; g) \(12\dc5\cdot1\dc2-9\dc75\)", r"e) \(8:100\) &nbsp; f) \(0\dc07\cdot0\dc3\) &nbsp; g) \(12\dc5\cdot1\dc2-9\dc75\)", r"e) \(8:100\) &nbsp; f) \(0\dc07\cdot0\dc3\) &nbsp; g) \(12\dc5\cdot1\dc2-9\dc75\)")),
  ('★★★', L(r"h) Una ampolla de 1,5 L d'aigua costa 0,65 € i un paquet de 6 ampolles, 3,49 €. Quant estalviem per litre si comprem el paquet? (arrodoneix als cèntims)", r"h) Una botella de 1,5 L de agua cuesta 0,65 € y un paquete de 6 botellas, 3,49 €. ¿Cuánto ahorramos por litro si compramos el paquete? (redondea a los céntimos)", r"h) A 1.5 L bottle of water costs 0.65 € and a pack of 6 bottles costs 3.49 €. How much do we save per litre by buying the pack? (round to the cent)"))],
  P(r"a) \(8\dc53\) &nbsp; b) \(13\dc8\) &nbsp; c) \(0\dc94\) &nbsp; d) \(370\) &nbsp; e) \(0\dc08\) &nbsp; f) \(0\dc021\) &nbsp; g) \(15-9\dc75=5\dc25\) &nbsp; h) Ampolla: \(0\dc65:1\dc5\approx0\dc43\) €/L; paquet: \(3\dc49:9\approx0\dc39\) €/L. Estalviem uns \(0\dc04\) € per litre.",
    r"a) \(8\dc53\) &nbsp; b) \(13\dc8\) &nbsp; c) \(0\dc94\) &nbsp; d) \(370\) &nbsp; e) \(0\dc08\) &nbsp; f) \(0\dc021\) &nbsp; g) \(15-9\dc75=5\dc25\) &nbsp; h) Botella: \(0\dc65:1\dc5\approx0\dc43\) €/L; paquete: \(3\dc49:9\approx0\dc39\) €/L. Ahorramos unos \(0\dc04\) € por litro.",
    r"a) \(8\dc53\) &nbsp; b) \(13\dc8\) &nbsp; c) \(0\dc94\) &nbsp; d) \(370\) &nbsp; e) \(0\dc08\) &nbsp; f) \(0\dc021\) &nbsp; g) \(15-9\dc75=5\dc25\) &nbsp; h) Bottle: \(0\dc65:1\dc5\approx0\dc43\) €/L; pack: \(3\dc49:9\approx0\dc39\) €/L. We save about \(0\dc04\) € per litre."))
ck(15 - Dm('6.47'), '8.53'); ck(Dm('4.6') * 3, '13.8'); ck(Dm('2.35') * Dm('0.4'), '0.94'); ck(Dm('0.07') * Dm('0.3'), '0.021'); ck(Dm('12.5') * Dm('1.2') - Dm('9.75'), '5.25')
assert round(0.65 / 1.5, 2) == 0.43 and round(3.49 / 9, 2) == 0.39

# ============================================================ 2.4
s4 = box('def', L('Dividir amb decimals', 'Dividir con decimales', 'Dividing with decimals'),
  ul(L(r"<strong>Dividend decimal i divisor natural</strong>: dividim com sempre i, quan baixem la primera xifra decimal, posem la coma al quocient. \(\ 9\dc75:3=3\dc25\)",
         r"<strong>Dividendo decimal y divisor natural</strong>: dividimos como siempre y, cuando bajamos la primera cifra decimal, ponemos la coma en el cociente. \(\ 9\dc75:3=3\dc25\)",
         r"<strong>Decimal dividend, whole divisor</strong>: divide as usual and, when you bring down the first decimal digit, put the comma in the quotient. \(\ 9\dc75:3=3\dc25\)"),
     L(r"<strong>Divisor decimal</strong>: multipliquem el dividend i el divisor per la unitat seguida de tants zeros com decimals té el divisor. El quocient no canvia: \(\ 12\dc6:0\dc35=1260:35=36\)",
       r"<strong>Divisor decimal</strong>: multiplicamos el dividendo y el divisor por la unidad seguida de tantos ceros como decimales tiene el divisor. El cociente no cambia: \(\ 12\dc6:0\dc35=1260:35=36\)",
       r"<strong>Decimal divisor</strong>: multiply dividend and divisor by 1 followed by as many zeros as the divisor has decimals. The quotient doesn't change: \(\ 12\dc6:0\dc35=1260:35=36\)"),
     L(r"Si la divisió no és exacta, podem continuar afegint zeros al dividend per a obtindre més decimals al quocient i, després, <strong>arrodonir</strong>: \(\ 10:3=3\dc333\ldots\approx3\dc33\).",
       r"Si la división no es exacta, podemos continuar añadiendo ceros al dividendo para obtener más decimales en el cociente y, después, <strong>redondear</strong>: \(\ 10:3=3\dc333\ldots\approx3\dc33\).",
       r"If the division isn't exact, keep adding zeros to the dividend to get more decimals in the quotient, then <strong>round</strong>: \(\ 10:3=3\dc333\ldots\approx3\dc33\).")))
ck(Dm('9.75') / 3, '3.25'); ck(Dm('12.6') / Dm('0.35'), '36')
s4 += widget('w-div', '➗', L('Divisió pas a pas', 'División paso a paso', 'Division step by step'),
  f'  <div class="wrow">{nin("a", "Dividend", "Dividendo", "Dividend", "12,6", "m")}{nin("b", "Divisor", "Divisor", "Divisor", "0,35", "m")}{gseg("k", [("0", L("0 decimals", "0 decimales", "0 decimals")), ("1", "1"), ("2", "2"), ("3", "3")], "2")}</div>\n'
  + '  ' + quick([('12,6;0,35', '12,6 : 0,35'), ('9,75;3', '9,75 : 3'), ('7;4', '7 : 4'), ('2,73;0,7', '2,73 : 0,7'), ('5;0,25', '5 : 0,25'), ('10;3', '10 : 3'), ('0,9;0,004', '0,9 : 0,004')]) + '\n')
s4 += drill('div', 'Entrena: divisions amb decimals', 'Entrena: divisiones con decimales', 'Train: dividing with decimals')
s4 += box('prop', L('Operacions combinades amb decimals', 'Operaciones combinadas con decimales', 'Mixed operations with decimals'),
  P(r"Seguim la mateixa <strong>jerarquia</strong> que amb els enters: primer els parèntesis, després les multiplicacions i divisions (d'esquerra a dreta) i, al final, les sumes i restes.", r"Seguimos la misma <strong>jerarquía</strong> que con los enteros: primero los paréntesis, después las multiplicaciones y divisiones (de izquierda a derecha) y, al final, las sumas y restas.", r"We follow the same <strong>order of operations</strong> as with integers: brackets first, then multiplication and division (left to right), and finally addition and subtraction.")
  + r'\[5\dc2-1\dc5\cdot2\dc4+0\dc6:0\dc2=5\dc2-3\dc6+3=\boxed{4\dc6}\]')
ck(Dm('5.2') - Dm('1.5') * Dm('2.4') + Dm('0.6') / Dm('0.2'), '4.6')
s4 += level(1, 1,
  prob(L(r"Calcula: a) \(8\dc4:4\) &nbsp; b) \(15:8\) &nbsp; c) \(4\dc5:0\dc9\)", r"Calcula: a) \(8\dc4:4\) &nbsp; b) \(15:8\) &nbsp; c) \(4\dc5:0\dc9\)", r"Work out: a) \(8\dc4:4\) &nbsp; b) \(15:8\) &nbsp; c) \(4\dc5:0\dc9\)"),
       r'\[\text{a) }8\dc4:4=\boxed{2\dc1}\qquad\text{b) }15:8=\boxed{1\dc875}\qquad\text{c) }45:9=\boxed{5}\]'))
ck(Dm('8.4') / 4, '2.1'); ck(Dm(15) / 8, '1.875'); ck(Dm('4.5') / Dm('0.9'), '5')
s4 += level(2, 2,
  prob(L(r"Calcula: \(\ (3\dc5-1\dc25)\cdot0\dc4+2\dc7:0\dc09\)", r"Calcula: \(\ (3\dc5-1\dc25)\cdot0\dc4+2\dc7:0\dc09\)", r"Work out: \(\ (3\dc5-1\dc25)\cdot0\dc4+2\dc7:0\dc09\)"),
       r'\[(3\dc5-1\dc25)\cdot0\dc4+2\dc7:0\dc09=2\dc25\cdot0\dc4+270:9\]',
       r'\[=0\dc9+30=\boxed{30\dc9}\]'))
ck((Dm('3.5') - Dm('1.25')) * Dm('0.4') + Dm('2.7') / Dm('0.09'), '30.9')
s4 += level(3, 3,
  prob(L(r"Un tros de formatge de \(0\dc85\) kg costa \(11\dc39\) €. Quin és el preu del quilo? Quant costarà un altre tros de \(1\dc2\) kg del mateix formatge?", r"Un trozo de queso de \(0\dc85\) kg cuesta \(11\dc39\) €. ¿Cuál es el precio del kilo? ¿Cuánto costará otro trozo de \(1\dc2\) kg del mismo queso?", r"A \(0\dc85\) kg piece of cheese costs \(11\dc39\) €. What's the price per kilo? How much will a \(1\dc2\) kg piece of the same cheese cost?"),
       r'\[11\dc39:0\dc85=1139:85=\boxed{13\dc40\ €/\text{kg}}\]',
       r'\[13\dc40\cdot1\dc2=\boxed{16\dc08\ €}\]'))
ck(Dm('11.39') / Dm('0.85'), '13.4'); ck(Dm('13.40') * Dm('1.2'), '16.08')
s4 += practice([
  ('★', L(r"a) \(6\dc24:3\) &nbsp; b) \(9:4\) &nbsp; c) \(3\dc6:0\dc4\)", r"a) \(6\dc24:3\) &nbsp; b) \(9:4\) &nbsp; c) \(3\dc6:0\dc4\)", r"a) \(6\dc24:3\) &nbsp; b) \(9:4\) &nbsp; c) \(3\dc6:0\dc4\)")),
  ('★★', L(r"d) \(2:0\dc05\) &nbsp; e) \(7:6\) amb dues xifres decimals &nbsp; f) \(1\dc2\cdot(4-2\dc5)+0\dc8:4\)", r"d) \(2:0\dc05\) &nbsp; e) \(7:6\) con dos cifras decimales &nbsp; f) \(1\dc2\cdot(4-2\dc5)+0\dc8:4\)", r"d) \(2:0\dc05\) &nbsp; e) \(7:6\) to two decimal places &nbsp; f) \(1\dc2\cdot(4-2\dc5)+0\dc8:4\)")),
  ('★★★', L(r"g) Un cotxe gasta \(31\dc5\) L en 450 km. Quants litres gasta cada 100 km? Si el litre de gasolina costa \(1\dc58\) €, quant costa fer 100 km?", r"g) Un coche gasta \(31\dc5\) L en 450 km. ¿Cuántos litros gasta cada 100 km? Si el litro de gasolina cuesta \(1\dc58\) €, ¿cuánto cuesta hacer 100 km?", r"g) A car uses \(31\dc5\) L in 450 km. How many litres per 100 km? If petrol costs \(1\dc58\) € a litre, how much do 100 km cost?"))],
  P(r"a) \(2\dc08\) &nbsp; b) \(2\dc25\) &nbsp; c) \(9\) &nbsp; d) \(40\) &nbsp; e) \(1\dc16\), residu \(0\dc04\) (\(7:6=1\dc1\overline{6}\)) &nbsp; f) \(1\dc8+0\dc2=2\) &nbsp; g) \(31\dc5:4\dc5=7\) L; \(\ 7\cdot1\dc58=11\dc06\) €.",
    r"a) \(2\dc08\) &nbsp; b) \(2\dc25\) &nbsp; c) \(9\) &nbsp; d) \(40\) &nbsp; e) \(1\dc16\), resto \(0\dc04\) (\(7:6=1\dc1\overline{6}\)) &nbsp; f) \(1\dc8+0\dc2=2\) &nbsp; g) \(31\dc5:4\dc5=7\) L; \(\ 7\cdot1\dc58=11\dc06\) €.",
    r"a) \(2\dc08\) &nbsp; b) \(2\dc25\) &nbsp; c) \(9\) &nbsp; d) \(40\) &nbsp; e) \(1\dc16\), remainder \(0\dc04\) (\(7:6=1\dc1\overline{6}\)) &nbsp; f) \(1\dc8+0\dc2=2\) &nbsp; g) \(31\dc5:4\dc5=7\) L; \(\ 7\cdot1\dc58=11\dc06\) €."))
ck(Dm('6.24') / 3, '2.08'); ck(Dm(9) / 4, '2.25'); ck(Dm('3.6') / Dm('0.4'), '9'); ck(Dm(2) / Dm('0.05'), '40'); ck(7 - 6 * Dm('1.16'), '0.04')
ck(Dm('1.2') * (4 - Dm('2.5')) + Dm('0.8') / 4, '2'); ck(Dm('31.5') / Dm('4.5'), '7'); ck(7 * Dm('1.58'), '11.06')
