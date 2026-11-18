# 11.4 Càlcul de probabilitats: experiments regulars, llei de Laplace i recompte amb taules de doble entrada
# Fet a partir de l'apartat 11.4 de 2n ESO (../2eso-t11/s4.py), amb la taula dels dos daus de l'apartat 11.5 de 2n.
from comu import *

s4 = box('def', L('Experiments regulars i irregulars', 'Experimentos regulares e irregulares', 'Regular and irregular experiments'),
  P(r"Un experiment aleatori és <strong>regular</strong> quan tots els resultats elementals tenen la mateixa probabilitat (són <strong>equiprobables</strong>). Per exemple: llançar una moneda o un dau no trucats, girar una ruleta amb sectors iguals, traure a l'atzar una carta d'una baralla o una bola d'una bossa (si totes les boles són iguals al tacte).",
    r"Un experimento aleatorio es <strong>regular</strong> cuando todos los resultados elementales tienen la misma probabilidad (son <strong>equiprobables</strong>). Por ejemplo: lanzar una moneda o un dado no trucados, girar una ruleta con sectores iguales, sacar al azar una carta de una baraja o una bola de una bolsa (si todas las bolas son iguales al tacto).",
    r"A random experiment is <strong>regular</strong> when all the elementary outcomes have the same probability (they are <strong>equally likely</strong>). For example: tossing a fair coin or rolling a fair die, spinning a wheel with equal sectors, drawing a card from a pack at random or a ball from a bag (if all the balls feel the same).")
  + P(r"Si l'espai mostral té \(n\) resultats equiprobables, cadascun té probabilitat \(\frac1n\): en un dau, \(P(1)=P(2)=\dots=P(6)=\frac16\); en una moneda, \(P(C)=P(X)=\frac12\).",
      r"Si el espacio muestral tiene \(n\) resultados equiprobables, cada uno tiene probabilidad \(\frac1n\): en un dado, \(P(1)=P(2)=\dots=P(6)=\frac16\); en una moneda, \(P(C)=P(X)=\frac12\).",
      r"If the sample space has \(n\) equally likely outcomes, each has probability \(\frac1n\): on a die, \(P(1)=P(2)=\dots=P(6)=\frac16\); on a coin, \(P(C)=P(X)=\frac12\).")
  + P(r"Si els resultats <strong>no</strong> són equiprobables, l'experiment és <strong>irregular</strong>: una xinxeta, un tap de suro, un dau trucat, una ruleta amb sectors de mides diferents… La seua probabilitat només la podem estimar experimentant (apartat 11.3).",
      r"Si los resultados <strong>no</strong> son equiprobables, el experimento es <strong>irregular</strong>: una chincheta, un tapón de corcho, un dado trucado, una ruleta con sectores de tamaños distintos… Su probabilidad solo la podemos estimar experimentando (apartado 11.3).",
      r"If the outcomes are <strong>not</strong> equally likely, the experiment is <strong>irregular</strong>: a drawing pin, a cork, a loaded die, a wheel with sectors of different sizes… We can only estimate its probability by experimenting (section 11.3)."))

s4 += box('prop', L('Llei de Laplace', 'Ley de Laplace', "Laplace's rule"),
  P(r"En un experiment regular, la probabilitat d'un esdeveniment \(A\) és el quocient entre el nombre de resultats favorables a \(A\) i el nombre de resultats possibles:",
    r"En un experimento regular, la probabilidad de un suceso \(A\) es el cociente entre el número de resultados favorables a \(A\) y el número de resultados posibles:",
    r"In a regular experiment, the probability of an event \(A\) is the number of outcomes favourable to \(A\) divided by the number of possible outcomes:")
  + D(r"P(A)=\frac{%s}{%s}" % (Lt('nombre de casos favorables', 'número de casos favorables', 'number of favourable outcomes'), Lt('nombre de casos possibles', 'número de casos posibles', 'number of possible outcomes')))
  + ul(L(r"Dau: \(P(\text{parell})=\frac36=\frac12\); \(P(\text{múltiple de 3})=\frac26=\frac13\).", r"Dado: \(P(\text{par})=\frac36=\frac12\); \(P(\text{múltiplo de 3})=\frac26=\frac13\).", r"Die: \(P(\text{even})=\frac36=\frac12\); \(P(\text{multiple of 3})=\frac26=\frac13\)."),
       L(r"Bossa amb 5 boles roges, 3 blaves i 2 verdes: \(P(R)=\frac5{10}=\frac12\); \(P(\text{no verda})=\frac8{10}=\frac45\).", r"Bolsa con 5 bolas rojas, 3 azules y 2 verdes: \(P(R)=\frac5{10}=\frac12\); \(P(\text{no verde})=\frac8{10}=\frac45\).", r"Bag with 5 red, 3 blue and 2 green balls: \(P(R)=\frac5{10}=\frac12\); \(P(\text{not green})=\frac8{10}=\frac45\)."),
       L(r"Baralla espanyola (40 cartes: oros, copes, espases i bastos, amb l'1 al 7, la sota, el cavall i el rei de cada pal): \(P(\text{oros})=\frac{10}{40}=\frac14\); \(P(\text{as})=\frac4{40}=\frac1{10}\); \(P(\text{figura})=\frac{12}{40}=\frac3{10}\).", r"Baraja española (40 cartas: oros, copas, espadas y bastos, con el 1 al 7, la sota, el caballo y el rey de cada palo): \(P(\text{oros})=\frac{10}{40}=\frac14\); \(P(\text{as})=\frac4{40}=\frac1{10}\); \(P(\text{figura})=\frac{12}{40}=\frac3{10}\).", r"Spanish pack (40 cards: coins, cups, swords and clubs, with 1 to 7, the jack, the knight and the king of each suit): \(P(\text{coins})=\frac{10}{40}=\frac14\); \(P(\text{ace})=\frac4{40}=\frac1{10}\); \(P(\text{face card})=\frac{12}{40}=\frac3{10}\)."))
  + figs(bag('RRRRRBBBVV', cap=L('5 roges, 3 blaves i 2 verdes', '5 rojas, 3 azules y 2 verdes', '5 red, 3 blue and 2 green')))
  + note(r"Simplifica sempre la fracció. Si cal, escriu-la també com a decimal o percentatge: \(\frac{3}{10}=0{,}3=30\,\%\).",
         r"Simplifica siempre la fracción. Si hace falta, escríbela también como decimal o porcentaje: \(\frac{3}{10}=0{,}3=30\,\%\).",
         r"Always simplify the fraction. If needed, also write it as a decimal or a percentage: \(\frac{3}{10}=0.3=30\,\%\).")
  + note(r"La llei de Laplace <strong>només</strong> val si els resultats són equiprobables. Compte: «aprovar o suspendre» té dos resultats, però això no vol dir que cada un tinga probabilitat \(\frac12\)!",
         r"La ley de Laplace <strong>solo</strong> vale si los resultados son equiprobables. Cuidado: «aprobar o suspender» tiene dos resultados, ¡pero eso no quiere decir que cada uno tenga probabilidad \(\frac12\)!",
         r"Laplace's rule <strong>only</strong> works if the outcomes are equally likely. Careful: “pass or fail” has two outcomes, but that doesn't mean each has probability \(\frac12\)!", '⚠️')
  + widget('w-bag', '👜', L('Una bossa de boles', 'Una bolsa de bolas', 'A bag of balls'),
           ['<div class="wrow">' + rng('r', 0, 10, 1, 5, 'R') + rng('b', 0, 10, 1, 3, 'B') + rng('v', 0, 10, 1, 2, 'V') + rng('g', 0, 10, 1, 0, 'G') + '</div>',
            '<div class="wrow"><div class="seg sg-e" role="group"></div></div>',
            '<div class="wrow"><button class="btn" type="button" data-a="draw">🖐 ' + L('Trau-ne una', 'Saca una', 'Draw one') + '</button><span class="drawn"></span></div>'])
  + drill('lap', 'Entrena: llei de Laplace', 'Entrena: ley de Laplace', 'Train: Laplace\'s rule'))
ck(Fr(3, 6), Fr(1, 2)); ck(Fr(2, 6), Fr(1, 3)); ck(Fr(5, 10), Fr(1, 2)); ck(Fr(8, 10), Fr(4, 5)); ck(Fr(10, 40), Fr(1, 4)); ck(Fr(4, 40), Fr(1, 10)); ck(Fr(12, 40), Fr(3, 10))

s4 += box('prop', L('Laplace i les propietats: el contrari i la unió', 'Laplace y las propiedades: el contrario y la unión', "Laplace and the properties: complement and union"),
  P(r"Amb la llei de Laplace també podem fer servir les propietats de l'apartat 11.3. En una bossa amb 5 boles roges, 3 de blaves i 2 de verdes:",
    r"Con la ley de Laplace también podemos usar las propiedades del apartado 11.3. En una bolsa con 5 bolas rojas, 3 azules y 2 verdes:",
    r"With Laplace's rule we can also use the properties from section 11.3. In a bag with 5 red, 3 blue and 2 green balls:")
  + D(r"P(\text{%s})=1-P(V)=1-\frac2{10}=\frac8{10}=\frac45" % Lt('no verda', 'no verde', 'not green'))
  + P(r"I en una baralla espanyola, per a \(A=\) «oros» i \(B=\) «figura» (compatibles: hi ha 3 figures d'oros):",
      r"Y en una baraja española, para \(A=\) «oros» y \(B=\) «figura» (compatibles: hay 3 figuras de oros):",
      r"And in a Spanish pack, for \(A=\) “coins” and \(B=\) “face card” (compatible: there are 3 face cards of coins):")
  + D(r"P(A\cup B)=P(A)+P(B)-P(A\cap B)=\frac{10}{40}+\frac{12}{40}-\frac3{40}=\frac{19}{40}")
  + P(r"Comprova-ho comptant: 10 oros més les 9 figures que no són d'oros fan 19 cartes.",
      r"Compruébalo contando: 10 oros más las 9 figuras que no son de oros hacen 19 cartas.",
      r"Check by counting: 10 coins cards plus the 9 face cards that aren't coins make 19 cards."))
ck(1 - Fr(2, 10), Fr(4, 5)); ck(Fr(10, 40) + Fr(12, 40) - Fr(3, 40), Fr(19, 40)); assert 10 + 12 - 3 == 19

s4 += box('prop', L('Taula de doble entrada: dos daus', 'Tabla de doble entrada: dos dados', 'Two-way table: two dice'),
  P(r"Quan l'experiment compost té només dues parts, també podem escriure tots els resultats en una <strong>taula de doble entrada</strong>: una part a les files i l'altra a les columnes. En llançar dos daus hi ha \(6\cdot6=36\) resultats equiprobables (\((2,5)\) i \((5,2)\) són resultats diferents). Si sumem els punts, la taula mostra les 36 sumes; les caselles marcades són les de suma 7:",
    r"Cuando el experimento compuesto tiene solo dos partes, también podemos escribir todos los resultados en una <strong>tabla de doble entrada</strong>: una parte en las filas y la otra en las columnas. Al lanzar dos dados hay \(6\cdot6=36\) resultados equiprobables (\((2,5)\) y \((5,2)\) son resultados distintos). Si sumamos los puntos, la tabla muestra las 36 sumas; las casillas marcadas son las de suma 7:",
    r"When the compound experiment has only two parts, we can also write all the outcomes in a <strong>two-way table</strong>: one part in the rows and the other in the columns. Rolling two dice gives \(6\cdot6=36\) equally likely outcomes (\((2,5)\) and \((5,2)\) are different outcomes). If we add the scores, the table shows the 36 sums; the highlighted cells are those with sum 7:")
  + dgrid(lambda a, b: a + b, lambda a, b: a + b == 7)
  + D(r"P(\text{%s}=7)=\frac6{36}=\frac16\qquad P(\text{%s}=2)=\frac1{36}\qquad P(\text{%s}=12)=\frac1{36}" % (Lt('suma', 'suma', 'sum'), Lt('suma', 'suma', 'sum'), Lt('suma', 'suma', 'sum')))
  + note(r"Les sumes del 2 al 12 <strong>no</strong> són equiprobables: el 7 és la més probable. Si haguérem pres \(E=\{2,\,3,\,\dots,\,12\}\) i aplicat Laplace, ens hauria eixit \(\frac1{11}\), que és <strong>incorrecte</strong>.",
         r"Las sumas del 2 al 12 <strong>no</strong> son equiprobables: el 7 es la más probable. Si hubiéramos tomado \(E=\{2,\,3,\,\dots,\,12\}\) y aplicado Laplace, nos habría salido \(\frac1{11}\), que es <strong>incorrecto</strong>.",
         r"The sums 2 to 12 are <strong>not</strong> equally likely: 7 is the most likely. If we had taken \(E=\{2,\,3,\,\dots,\,12\}\) and used Laplace, we'd have got \(\frac1{11}\), which is <strong>wrong</strong>.", '⚠️')
  + widget('w-dice2', '🎲', L('Dos daus', 'Dos dados', 'Two dice'),
           ['<div class="wrow"><div class="seg sg-o" role="group"></div></div>',
            '<div class="wrow"><div class="seg sg-r" role="group"></div>' + rng('k', 2, 12, 1, 7, 'k') + '</div>',
            '<div class="wrow"><button class="btn" type="button" data-a="roll">🎲 ' + L('Llança els daus', 'Lanza los dados', 'Roll the dice') + '</button><span class="drawn"></span></div>'])
  + drill('dice', 'Entrena: dos daus', 'Entrena: dos dados', 'Train: two dice'))
S7 = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == 7]
assert len(S7) == 6; ck(Fr(6, 36), Fr(1, 6))

W_ = 'PROBABILITAT'
assert len(W_) == 12 and sum(c in 'AEIOU' for c in W_) == 5 and W_.count('A') == 2
x_ = [x for x in range(0, 100) if Fr(3 + x, 15 + x) == Fr(1, 2)]
assert x_ == [9]
assert len([x for x in range(1, 21) if x % 2 == 0 or x % 5 == 0]) == 12
assert len([1 for a in range(1, 7) for b in range(1, 7) if a + b == 10]) == 3 and len([1 for a in range(1, 7) for b in range(1, 7) if a + b >= 10]) == 6
s4 += levels(
 [prob(L(r"En una urna hi ha 4 boles roges, 6 de blaves i 5 de verdes. Traiem una bola a l'atzar. Calcula la probabilitat que siga roja, blava, verda i que no siga blava.",
         r"En una urna hay 4 bolas rojas, 6 azules y 5 verdes. Sacamos una bola al azar. Calcula la probabilidad de que sea roja, azul, verde y de que no sea azul.",
         r"An urn holds 4 red, 6 blue and 5 green balls. We draw one at random. Find the probability that it's red, blue, green, and that it isn't blue."),
       P(r"Hi ha \(4+6+5=15\) boles (casos possibles):", r"Hay \(4+6+5=15\) bolas (casos posibles):", r"There are \(4+6+5=15\) balls (possible outcomes):") + figs(bag('RRRRBBBBBBVVVVV')),
       D(r"P(R)=\frac4{15}\qquad P(B)=\frac6{15}=\frac25\qquad P(V)=\frac5{15}=\frac13"),
       P(r"«No blava» vol dir roja o verda: \(4+5=9\) casos favorables.", r"«No azul» quiere decir roja o verde: \(4+5=9\) casos favorables.", r"“Not blue” means red or green: \(4+5=9\) favourable outcomes."),
       D(r"P(\text{%s})=\frac{9}{15}=\boxed{\frac35}" % Lt('no blava', 'no azul', 'not blue')),
       P(r"Comprovació: \(\frac4{15}+\frac6{15}+\frac5{15}=1\ \checkmark\)", r"Comprobación: \(\frac4{15}+\frac6{15}+\frac5{15}=1\ \checkmark\)", r"Check: \(\frac4{15}+\frac6{15}+\frac5{15}=1\ \checkmark\)")),
  prob(L(r"Llancem un dau. Calcula la probabilitat de traure un nombre primer i la de traure més de 4.", r"Lanzamos un dado. Calcula la probabilidad de sacar un número primo y la de sacar más de 4.", r"We roll a die. Find the probability of rolling a prime number and of rolling more than 4."),
       D(r"P(\text{%s})=P(\{2,3,5\})=\frac36=\boxed{\frac12}\qquad P(\{5,6\})=\frac26=\boxed{\frac13}" % Lt('primer', 'primo', 'prime')))],
 [prob(L(r"Escrivim cada lletra de la paraula PROBABILITAT en una targeta i en traiem una a l'atzar. Quina és la probabilitat que siga una A? I una vocal? I una consonant?",
         r"Escribimos cada letra de la palabra valenciana PROBABILITAT en una tarjeta y sacamos una al azar. ¿Cuál es la probabilidad de que sea una A? ¿Y una vocal? ¿Y una consonante?",
         r"We write each letter of the Valencian word PROBABILITAT on a card and draw one at random. What is the probability that it's an A? A vowel? A consonant?"),
       P(r"Hi ha 12 targetes. Les vocals són O, A, I, I, A (5 targetes):", r"Hay 12 tarjetas. Las vocales son O, A, I, I, A (5 tarjetas):", r"There are 12 cards. The vowels are O, A, I, I, A (5 cards):"),
       D(r"P(A)=\frac2{12}=\boxed{\frac16}\qquad P(\text{%s})=\boxed{\frac5{12}}\qquad P(\text{%s})=\frac{12-5}{12}=\boxed{\frac7{12}}" % (Lt('vocal', 'vocal', 'vowel'), Lt('consonant', 'consonante', 'consonant')))),
  prob(L(r"En un bombo hi ha 20 boles numerades de l'1 al 20. Calcula la probabilitat de traure un múltiple de 5, un nombre de dues xifres i un nombre parell o múltiple de 5.",
         r"En un bombo hay 20 bolas numeradas del 1 al 20. Calcula la probabilidad de sacar un múltiplo de 5, un número de dos cifras y un número par o múltiplo de 5.",
         r"A drum holds 20 balls numbered 1 to 20. Find the probability of a multiple of 5, a two-digit number, and a number that is even or a multiple of 5."),
       D(r"P(\{5,\,10,\,15,\,20\})=\frac4{20}=\boxed{\frac15}\qquad P(\{10,\,11,\,\dots,\,20\})=\boxed{\frac{11}{20}}"),
       P(r"Parells: 2, 4, 6, …, 20 (10 boles). Afegim els múltiples de 5 que no són parells, 5 i 15 (el 10 i el 20 ja els hem comptat): \(10+2=12\) casos favorables.",
         r"Pares: 2, 4, 6, …, 20 (10 bolas). Añadimos los múltiplos de 5 que no son pares, 5 y 15 (el 10 y el 20 ya los hemos contado): \(10+2=12\) casos favorables.",
         r"Even: 2, 4, 6, …, 20 (10 balls). Add the multiples of 5 that aren't even, 5 and 15 (10 and 20 have already been counted): \(10+2=12\) favourable outcomes."),
       D(r"P(\text{%s})=\frac{12}{20}=\boxed{\frac35}" % Lt('parell o múltiple de 5', 'par o múltiplo de 5', 'even or multiple of 5'))),
  prob(L(r"Llancem dos daus i sumem els punts. Calcula la probabilitat que la suma siga 10, que siga 10 o més, i que els dos daus traguen el mateix nombre (doble).", r"Lanzamos dos dados y sumamos los puntos. Calcula la probabilidad de que la suma sea 10, de que sea 10 o más, y de que los dos dados saquen el mismo número (doble).", r"We roll two dice and add the scores. Find the probability that the sum is 10, that it's 10 or more, and that both dice show the same number (a double)."),
       P(r"Mirem la taula: suma 10 en \((4,6),\,(5,5),\,(6,4)\); suma 11 en dues caselles i suma 12 en una. Els dobles són la diagonal (6 caselles).", r"Miramos la tabla: suma 10 en \((4,6),\,(5,5),\,(6,4)\); suma 11 en dos casillas y suma 12 en una. Los dobles son la diagonal (6 casillas).", r"Look at the table: sum 10 at \((4,6),\,(5,5),\,(6,4)\); sum 11 in two cells and sum 12 in one. The doubles are the diagonal (6 cells)."),
       D(r"P(10)=\frac3{36}=\boxed{\frac1{12}}\qquad P(\ge10)=\frac{3+2+1}{36}=\boxed{\frac16}\qquad P(\text{%s})=\frac6{36}=\boxed{\frac16}" % Lt('doble', 'doble', 'double')))],
 [prob(L(r"En una bossa hi ha 3 boles roges i unes quantes de blaves. Si la probabilitat de traure una bola roja és \(\frac15\), quantes boles blaves hi ha? Quantes boles roges hauríem d'afegir perquè la probabilitat de roja fóra \(\frac12\)?",
         r"En una bolsa hay 3 bolas rojas y algunas azules. Si la probabilidad de sacar una bola roja es \(\frac15\), ¿cuántas bolas azules hay? ¿Cuántas bolas rojas tendríamos que añadir para que la probabilidad de roja fuera \(\frac12\)?",
         r"A bag has 3 red balls and some blue ones. If the probability of drawing a red ball is \(\frac15\), how many blue balls are there? How many red balls would we need to add to make the probability of red \(\frac12\)?"),
       P(r"\(P(R)=\frac15\) vol dir que 1 de cada 5 boles és roja. Com que hi ha 3 roges, hi ha \(3\cdot5=15\) boles en total i \(15-3=\) <strong>12 boles blaves</strong>.", r"\(P(R)=\frac15\) quiere decir que 1 de cada 5 bolas es roja. Como hay 3 rojas, hay \(3\cdot5=15\) bolas en total y \(15-3=\) <strong>12 bolas azules</strong>.", r"\(P(R)=\frac15\) means 1 in every 5 balls is red. Since there are 3 red, there are \(3\cdot5=15\) balls in total and \(15-3=\) <strong>12 blue balls</strong>."),
       P(r"Perquè \(P(R)=\frac12\) hi ha d'haver tantes roges com blaves: 12 roges. Cal afegir \(12-3=\) <strong>9 boles roges</strong>.", r"Para que \(P(R)=\frac12\) tiene que haber tantas rojas como azules: 12 rojas. Hay que añadir \(12-3=\) <strong>9 bolas rojas</strong>.", r"For \(P(R)=\frac12\) there must be as many red as blue: 12 red. We need to add \(12-3=\) <strong>9 red balls</strong>."),
       P(r"Comprovació: \(P(R)=\frac{12}{24}=\frac12\ \checkmark\)", r"Comprobación: \(P(R)=\frac{12}{24}=\frac12\ \checkmark\)", r"Check: \(P(R)=\frac{12}{24}=\frac12\ \checkmark\)"))])
s4 += practice([
  ('★', L(r"a) Girem una ruleta de 10 sectors iguals numerats de l'1 al 10. Calcula la probabilitat de traure un múltiple de 3 i la de traure un nombre parell.", r"a) Giramos una ruleta de 10 sectores iguales numerados del 1 al 10. Calcula la probabilidad de sacar un múltiplo de 3 y la de sacar un número par.", r"a) We spin a wheel with 10 equal sectors numbered 1 to 10. Find the probability of a multiple of 3 and of an even number.")),
  ('★★', L(r"b) En una classe hi ha 14 xiques i 11 xics. Triem una persona a l'atzar per a ser delegada. Quina és la probabilitat que siga un xic? c) Traiem una carta de la baralla espanyola: quina és la probabilitat que siga un as o un rei?", r"b) En una clase hay 14 chicas y 11 chicos. Elegimos una persona al azar para ser delegada. ¿Cuál es la probabilidad de que sea un chico? c) Sacamos una carta de la baraja española: ¿cuál es la probabilidad de que sea un as o un rey?", r"b) A class has 14 girls and 11 boys. We pick someone at random as class rep. What is the probability it's a boy? c) We draw a card from the Spanish pack: what is the probability that it's an ace or a king?")),
  ('★★★', L(r"d) En una bossa hi ha boles roges, blaves i verdes. \(P(R)=\frac13\), \(P(B)=\frac12\) i hi ha 4 boles verdes. Quantes boles hi ha de cada color?", r"d) En una bolsa hay bolas rojas, azules y verdes. \(P(R)=\frac13\), \(P(A)=\frac12\) y hay 4 bolas verdes. ¿Cuántas bolas hay de cada color?", r"d) A bag has red, blue and green balls. \(P(R)=\frac13\), \(P(B)=\frac12\) and there are 4 green balls. How many balls of each colour are there?"))],
  P(r"a) \(\frac3{10}\) i \(\frac5{10}=\frac12\). b) \(\frac{11}{25}=0{,}44\). c) \(\frac8{40}=\frac15\). d) \(P(V)=1-\frac13-\frac12=\frac16\): 1 de cada 6 boles és verda, així que hi ha \(4\cdot6=24\) boles: 8 roges, 12 blaves i 4 verdes.",
    r"a) \(\frac3{10}\) y \(\frac5{10}=\frac12\). b) \(\frac{11}{25}=0{,}44\). c) \(\frac8{40}=\frac15\). d) \(P(V)=1-\frac13-\frac12=\frac16\): 1 de cada 6 bolas es verde, así que hay \(4\cdot6=24\) bolas: 8 rojas, 12 azules y 4 verdes.",
    r"a) \(\frac3{10}\) and \(\frac5{10}=\frac12\). b) \(\frac{11}{25}=0.44\). c) \(\frac8{40}=\frac15\). d) \(P(G)=1-\frac13-\frac12=\frac16\): 1 in 6 balls is green, so there are \(4\cdot6=24\) balls: 8 red, 12 blue and 4 green."))
assert Fr(11, 25) == Fr(44, 100) and 1 - Fr(1, 3) - Fr(1, 2) == Fr(1, 6) and (24 // 3, 24 // 2, 4) == (8, 12, 4)
