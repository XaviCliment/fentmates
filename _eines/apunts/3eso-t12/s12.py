# 12.1 Experiments aleatoris. Espai mostral i esdeveniments · 12.2 Operacions amb esdeveniments
from comu import *

D6 = list(range(1, 7))

TREE3 = ptree([(a, '', [(b, '', [(c, '', [], a + b + c) for c in 'CX']) for b in 'CX']) for a in 'CX'], W=320, rowh=26, leaf=True)

# =====================================================================
# 12.1 Experiments aleatoris. Espai mostral i esdeveniments
# =====================================================================
s1 = box('def', L('Experiments deterministes i aleatoris', 'Experimentos deterministas y aleatorios', 'Deterministic and random experiments'),
  P(r"Un <strong>experiment determinista</strong> és aquell del qual podem predir el resultat abans de fer-lo: si deixem caure una pedra, cau; si escalfem aigua a 100 °C al nivell de la mar, bull.",
    r"Un <strong>experimento determinista</strong> es aquel cuyo resultado podemos predecir antes de realizarlo: si dejamos caer una piedra, cae; si calentamos agua a 100 °C al nivel del mar, hierve.",
    r"A <strong>deterministic experiment</strong> is one whose result we can predict before doing it: if we drop a stone, it falls; if we heat water to 100 °C at sea level, it boils.")
  + P(r"Un <strong>experiment aleatori</strong> és aquell del qual <strong>no</strong> podem predir el resultat, encara que el repetim moltes vegades en les mateixes condicions: llançar una moneda o un dau, traure una carta d'una baralla, traure una bola d'una bossa sense mirar…",
      r"Un <strong>experimento aleatorio</strong> es aquel cuyo resultado <strong>no</strong> podemos predecir, aunque lo repitamos muchas veces en las mismas condiciones: lanzar una moneda o un dado, sacar una carta de una baraja, sacar una bola de una bolsa sin mirar…",
      r"A <strong>random experiment</strong> is one whose result we <strong>can't</strong> predict, even if we repeat it many times under the same conditions: tossing a coin or rolling a die, drawing a card from a pack, taking a ball out of a bag without looking…")
  + note(r"La paraula <em>aleatori</em> ve del llatí <em>alea</em>, «dau». La <strong>probabilitat</strong> és la part de les matemàtiques que estudia els experiments aleatoris.",
         r"La palabra <em>aleatorio</em> viene del latín <em>alea</em>, «dado». La <strong>probabilidad</strong> es la parte de las matemáticas que estudia los experimentos aleatorios.",
         r"The Spanish and Catalan word <em>aleatorio / aleatori</em> (random) comes from the Latin <em>alea</em>, “die”. <strong>Probability</strong> is the part of mathematics that studies random experiments.", '🎲'))

s1 += box('def', L('Espai mostral', 'Espacio muestral', 'Sample space'),
  P(r"Cada resultat possible d'un experiment aleatori és un <strong>resultat elemental</strong>. El conjunt de tots els resultats possibles és l'<strong>espai mostral</strong>, i l'escrivim \(E\):",
    r"Cada resultado posible de un experimento aleatorio es un <strong>resultado elemental</strong>. El conjunto de todos los resultados posibles es el <strong>espacio muestral</strong>, y lo escribimos \(E\):",
    r"Each possible result of a random experiment is an <strong>elementary outcome</strong>. The set of all possible outcomes is the <strong>sample space</strong>, written \(E\):")
  + ul(L(r"Llançar una moneda: \(E=\{C,\,X\}\) (cara i creu).", r"Lanzar una moneda: \(E=\{C,\,X\}\) (cara y cruz).", r"Tossing a coin: \(E=\{C,\,X\}\) (heads C and tails X)."),
       L(r"Llançar un dau: \(E=\{1,\,2,\,3,\,4,\,5,\,6\}\).", r"Lanzar un dado: \(E=\{1,\,2,\,3,\,4,\,5,\,6\}\).", r"Rolling a die: \(E=\{1,\,2,\,3,\,4,\,5,\,6\}\)."),
       L(r"Traure una bola d'una bossa amb boles roges, blaves i verdes: \(E=\{R,\,B,\,V\}\).", r"Sacar una bola de una bolsa con bolas rojas, azules y verdes: \(E=\{R,\,A,\,V\}\).", r"Taking a ball from a bag with red, blue and green balls: \(E=\{R,\,B,\,G\}\)."),
       L(r"Llançar dues monedes: \(E=\{CC,\,CX,\,XC,\,XX\}\). Atenció: \(CX\) (cara en la primera i creu en la segona) i \(XC\) són resultats diferents.", r"Lanzar dos monedas: \(E=\{CC,\,CX,\,XC,\,XX\}\). Atención: \(CX\) (cara en la primera y cruz en la segunda) y \(XC\) son resultados distintos.", r"Tossing two coins: \(E=\{CC,\,CX,\,XC,\,XX\}\). Careful: \(CX\) (heads on the first, tails on the second) and \(XC\) are different outcomes."))
  + widget('w-esp', '🧪', L("Fes l'experiment", 'Haz el experimento', 'Do the experiment'),
           ['<div class="wrow"><div class="seg sg-x" role="group"></div></div>',
            '<div class="wrow"><button class="btn primary" type="button" data-a="go">🎲 ' + L("Fes l'experiment", 'Haz el experimento', 'Do the experiment') + '</button><button class="btn" type="button" data-a="clr">↺ ' + L('Esborra', 'Borrar', 'Clear') + '</button></div>'],
           out='<div class="esp-out"></div>'))

s1 += box('def', L('Esdeveniments', 'Sucesos', 'Events'),
  P(r"Un <strong>esdeveniment</strong> és qualsevol subconjunt de l'espai mostral. Diem que un esdeveniment <strong>ocorre</strong> (o es verifica) quan el resultat de l'experiment és un dels seus elements. En llançar un dau, per exemple:",
    r"Un <strong>suceso</strong> es cualquier subconjunto del espacio muestral. Decimos que un suceso <strong>ocurre</strong> (o se verifica) cuando el resultado del experimento es uno de sus elementos. Al lanzar un dado, por ejemplo:",
    r"An <strong>event</strong> is any subset of the sample space. We say an event <strong>happens</strong> when the result of the experiment is one of its elements. When rolling a die, for example:")
  + tbl([L('Tipus', 'Tipo', 'Type'), L('Què és', 'Qué es', 'What it is'), L('Exemple (dau)', 'Ejemplo (dado)', 'Example (die)')],
        [[L('<strong>Elemental</strong>', '<strong>Elemental</strong>', '<strong>Elementary</strong>'), L('té un sol resultat', 'tiene un solo resultado', 'it has a single outcome'), L(r'«traure un 5» \(=\{5\}\)', r'«sacar un 5» \(=\{5\}\)', r'“roll a 5” \(=\{5\}\)')],
         [L('<strong>Compost</strong>', '<strong>Compuesto</strong>', '<strong>Compound</strong>'), L('té dos o més resultats', 'tiene dos o más resultados', 'it has two or more outcomes'), L(r'«traure parell» \(=\{2,\,4,\,6\}\)', r'«sacar par» \(=\{2,\,4,\,6\}\)', r'“roll an even number” \(=\{2,\,4,\,6\}\)')],
         [L('<strong>Segur</strong>', '<strong>Seguro</strong>', '<strong>Certain</strong>'), L(r"ocorre sempre: és tot l'espai mostral \(E\)", r"ocurre siempre: es todo el espacio muestral \(E\)", r"it always happens: it's the whole sample space \(E\)"), L(r'«traure menys de 7» \(=E\)', r'«sacar menos de 7» \(=E\)', r'“roll less than 7” \(=E\)')],
         [L('<strong>Impossible</strong>', '<strong>Imposible</strong>', '<strong>Impossible</strong>'), L(r"no ocorre mai: no té cap element, \(\varnothing\)", r"no ocurre nunca: no tiene ningún elemento, \(\varnothing\)", r"it never happens: it has no elements, \(\varnothing\)"), L(r'«traure un 8» \(=\varnothing\)', r'«sacar un 8» \(=\varnothing\)', r'“roll an 8” \(=\varnothing\)')]])
  + note(r"Escriu sempre els esdeveniments entre claus i amb tots els seus elements: és la millor manera de no equivocar-se després en comptar.",
         r"Escribe siempre los sucesos entre llaves y con todos sus elementos: es la mejor manera de no equivocarse después al contar.",
         r"Always write events in braces listing all their elements: it's the best way to avoid counting mistakes later.")
  + drill('tipus', 'Entrena: quin tipus d\'esdeveniment és?', 'Entrena: ¿qué tipo de suceso es?', 'Train: what kind of event is it?', mode='opts'))

PR10 = [x for x in range(1, 11) if x in (2, 3, 5, 7)]
assert PR10 == [2, 3, 5, 7]
PAIRS = ['Anna–Biel', 'Anna–Carla', 'Anna–Dani', 'Biel–Carla', 'Biel–Dani', 'Carla–Dani']
assert len(PAIRS) == math.comb(4, 2) and sum('Anna' in p for p in PAIRS) == 3
s1 += levels(
 [prob(L(r"Indica quins experiments són aleatoris i quins deterministes: a) llançar un dau de parxís; b) mesurar quant tarda a caure una pedra des de 5 m; c) traure una carta d'una baralla; d) calcular l'àrea d'un quadrat de 3 cm de costat.",
         r"Indica qué experimentos son aleatorios y cuáles deterministas: a) lanzar un dado de parchís; b) medir cuánto tarda en caer una piedra desde 5 m; c) sacar una carta de una baraja; d) calcular el área de un cuadrado de 3 cm de lado.",
         r"Say which experiments are random and which are deterministic: a) rolling a ludo die; b) timing how long a stone takes to fall from 5 m; c) drawing a card from a pack; d) working out the area of a square with 3 cm sides."),
       P(r"a) i c) són <strong>aleatoris</strong>: no sabem quin resultat eixirà. b) i d) són <strong>deterministes</strong>: en les mateixes condicions, el resultat és sempre el mateix.",
         r"a) y c) son <strong>aleatorios</strong>: no sabemos qué resultado saldrá. b) y d) son <strong>deterministas</strong>: en las mismas condiciones, el resultado es siempre el mismo.",
         r"a) and c) are <strong>random</strong>: we don't know which result will come up. b) and d) are <strong>deterministic</strong>: under the same conditions the result is always the same.")),
  prob(L(r"Traiem una bola d'una urna amb deu boles numerades de l'1 al 10. Escriu l'espai mostral i els esdeveniments \(A=\) «nombre primer», \(B=\) «major que 7», \(C=\) «múltiple d'11» i \(D=\) «menor que 11». De quin tipus és cadascun?",
         r"Sacamos una bola de una urna con diez bolas numeradas del 1 al 10. Escribe el espacio muestral y los sucesos \(A=\) «número primo», \(B=\) «mayor que 7», \(C=\) «múltiplo de 11» y \(D=\) «menor que 11». ¿De qué tipo es cada uno?",
         r"We take a ball from an urn with ten balls numbered 1 to 10. Write the sample space and the events \(A=\) “prime number”, \(B=\) “greater than 7”, \(C=\) “multiple of 11” and \(D=\) “less than 11”. What kind of event is each one?"),
       D(r"E=\{1,\,2,\,3,\,4,\,5,\,6,\,7,\,8,\,9,\,10\}"),
       D(r"A=\{2,\,3,\,5,\,7\}\qquad B=\{8,\,9,\,10\}\qquad C=\varnothing\qquad D=E"),
       P(r"\(A\) i \(B\) són <strong>compostos</strong>, \(C\) és <strong>impossible</strong> i \(D\) és <strong>segur</strong>.", r"\(A\) y \(B\) son <strong>compuestos</strong>, \(C\) es <strong>imposible</strong> y \(D\) es <strong>seguro</strong>.", r"\(A\) and \(B\) are <strong>compound</strong>, \(C\) is <strong>impossible</strong> and \(D\) is <strong>certain</strong>."))],
 [prob(L(r"Llancem tres monedes. Fes un diagrama d'arbre, escriu l'espai mostral i l'esdeveniment \(A=\) «traure almenys dues cares».",
         r"Lanzamos tres monedas. Haz un diagrama de árbol, escribe el espacio muestral y el suceso \(A=\) «sacar al menos dos caras».",
         r"We toss three coins. Draw a tree diagram, write the sample space and the event \(A=\) “get at least two heads”."),
       P(r"Cada moneda pot eixir \(C\) o \(X\). En l'arbre, cada camí de l'esquerra a la dreta és un resultat:", r"Cada moneda puede salir \(C\) o \(X\). En el árbol, cada camino de izquierda a derecha es un resultado:", r"Each coin can land \(C\) or \(X\). In the tree, each path from left to right is an outcome:") + figs(TREE3),
       D(r"E=\{CCC,\,CCX,\,CXC,\,CXX,\,XCC,\,XCX,\,XXC,\,XXX\}"),
       P(r"«Almenys dues cares» vol dir <em>dues o tres</em> cares: \(A=\{CCC,\,CCX,\,CXC,\,XCC\}\).", r"«Al menos dos caras» quiere decir <em>dos o tres</em> caras: \(A=\{CCC,\,CCX,\,CXC,\,XCC\}\).", r"“At least two heads” means <em>two or three</em> heads: \(A=\{CCC,\,CCX,\,CXC,\,XCC\}\)."))],
 [prob(L(r"De quatre alumnes (Anna, Biel, Carla i Dani) en triem dos a l'atzar per a representar el grup. Escriu l'espai mostral. Quants resultats té l'esdeveniment «Anna és triada»?",
         r"De cuatro alumnos (Anna, Biel, Carla y Dani) elegimos dos al azar para representar al grupo. Escribe el espacio muestral. ¿Cuántos resultados tiene el suceso «Anna es elegida»?",
         r"From four students (Anna, Biel, Carla and Dani) we choose two at random to represent the class. Write the sample space. How many outcomes does the event “Anna is chosen” have?"),
       P(r"Ara l'ordre no importa (Anna–Biel és la mateixa parella que Biel–Anna). Fem les parelles de manera ordenada:", r"Ahora el orden no importa (Anna–Biel es la misma pareja que Biel–Anna). Formamos las parejas de manera ordenada:", r"Here order doesn't matter (Anna–Biel is the same pair as Biel–Anna). List the pairs systematically:"),
       chips(PAIRS, A=[p for p in PAIRS if 'Anna' in p]),
       P(r"L'espai mostral té <strong>6</strong> resultats i «Anna és triada» en té <strong>3</strong> (els marcats).", r"El espacio muestral tiene <strong>6</strong> resultados y «Anna es elegida» tiene <strong>3</strong> (los marcados).", r"The sample space has <strong>6</strong> outcomes and “Anna is chosen” has <strong>3</strong> (the highlighted ones)."))])
s1 += practice([
  ('★', L(r"a) Escriu l'espai mostral de l'experiment «girar una ruleta dividida en 8 sectors iguals numerats de l'1 al 8». b) Escriu-hi els esdeveniments «traure un múltiple de 3» i «traure un nombre més gran que 8».", r"a) Escribe el espacio muestral del experimento «girar una ruleta dividida en 8 sectores iguales numerados del 1 al 8». b) Escribe en él los sucesos «sacar un múltiplo de 3» y «sacar un número mayor que 8».", r"a) Write the sample space of “spinning a wheel divided into 8 equal sectors numbered 1 to 8”. b) Write the events “get a multiple of 3” and “get a number greater than 8”.")),
  ('★★', L(r"c) Llancem una moneda i un dau. Quants resultats té l'espai mostral? Escriu l'esdeveniment «cara i nombre parell».", r"c) Lanzamos una moneda y un dado. ¿Cuántos resultados tiene el espacio muestral? Escribe el suceso «cara y número par».", r"c) We toss a coin and roll a die. How many outcomes does the sample space have? Write the event “heads and an even number”.")),
  ('★★★', L(r"d) Formem nombres de dues xifres diferents amb les xifres 1, 2 i 3. Escriu l'espai mostral i l'esdeveniment «el nombre és més gran que 20».", r"d) Formamos números de dos cifras distintas con las cifras 1, 2 y 3. Escribe el espacio muestral y el suceso «el número es mayor que 20».", r"d) We make two-digit numbers with different digits using 1, 2 and 3. Write the sample space and the event “the number is greater than 20”."))],
  P(r"a) \(E=\{1,\,2,\,3,\,4,\,5,\,6,\,7,\,8\}\). b) \(\{3,\,6\}\) i \(\varnothing\) (impossible). c) \(2\cdot6=12\) resultats; \(\{C2,\,C4,\,C6\}\). d) \(E=\{12,\,13,\,21,\,23,\,31,\,32\}\); \(\{21,\,23,\,31,\,32\}\).",
    r"a) \(E=\{1,\,2,\,3,\,4,\,5,\,6,\,7,\,8\}\). b) \(\{3,\,6\}\) y \(\varnothing\) (imposible). c) \(2\cdot6=12\) resultados; \(\{C2,\,C4,\,C6\}\). d) \(E=\{12,\,13,\,21,\,23,\,31,\,32\}\); \(\{21,\,23,\,31,\,32\}\).",
    r"a) \(E=\{1,\,2,\,3,\,4,\,5,\,6,\,7,\,8\}\). b) \(\{3,\,6\}\) and \(\varnothing\) (impossible). c) \(2\cdot6=12\) outcomes; \(\{C2,\,C4,\,C6\}\). d) \(E=\{12,\,13,\,21,\,23,\,31,\,32\}\); \(\{21,\,23,\,31,\,32\}\)."))
NUMS = [10 * a + b for a in (1, 2, 3) for b in (1, 2, 3) if a != b]
assert NUMS == [12, 13, 21, 23, 31, 32] and [n for n in NUMS if n > 20] == [21, 23, 31, 32]

# =====================================================================
# 12.2 Operacions amb esdeveniments
# =====================================================================
A_ = [2, 4, 6]; B_ = [3, 6]
U_ = sorted(set(A_) | set(B_)); I_ = sorted(set(A_) & set(B_)); NA = [x for x in D6 if x not in A_]
assert U_ == [2, 3, 4, 6] and I_ == [6] and NA == [1, 3, 5]
s2 = box('def', L('Unió, intersecció i esdeveniment contrari', 'Unión, intersección y suceso contrario', 'Union, intersection and complementary event'),
  P(r"Amb els esdeveniments podem operar com amb els conjunts. En llançar un dau, prenem \(A=\) «parell» \(=\{2,\,4,\,6\}\) i \(B=\) «múltiple de 3» \(=\{3,\,6\}\):",
    r"Con los sucesos podemos operar como con los conjuntos. Al lanzar un dado, tomamos \(A=\) «par» \(=\{2,\,4,\,6\}\) y \(B=\) «múltiplo de 3» \(=\{3,\,6\}\):",
    r"We can operate with events just like with sets. When rolling a die, take \(A=\) “even” \(=\{2,\,4,\,6\}\) and \(B=\) “multiple of 3” \(=\{3,\,6\}\):")
  + tbl([L('Operació', 'Operación', 'Operation'), L('Ocorre quan…', 'Ocurre cuando…', 'Happens when…'), L('Exemple', 'Ejemplo', 'Example')],
        [[L(r'<strong>Unió</strong> \(A\cup B\)', r'<strong>Unión</strong> \(A\cup B\)', r'<strong>Union</strong> \(A\cup B\)'), L(r'ocorre \(A\) <strong>o</strong> \(B\) (o tots dos)', r'ocurre \(A\) <strong>o</strong> \(B\) (o ambos)', r'\(A\) <strong>or</strong> \(B\) happens (or both)'), r'\(A\cup B=\{2,\,3,\,4,\,6\}\)'],
         [L(r'<strong>Intersecció</strong> \(A\cap B\)', r'<strong>Intersección</strong> \(A\cap B\)', r'<strong>Intersection</strong> \(A\cap B\)'), L(r'ocorren \(A\) <strong>i</strong> \(B\) alhora', r'ocurren \(A\) <strong>y</strong> \(B\) a la vez', r'\(A\) <strong>and</strong> \(B\) both happen'), r'\(A\cap B=\{6\}\)'],
         [L(r'<strong>Contrari</strong> \(\overline{A}\)', r'<strong>Contrario</strong> \(\overline{A}\)', r'<strong>Complement</strong> \(\overline{A}\)'), L(r'<strong>no</strong> ocorre \(A\)', r'<strong>no</strong> ocurre \(A\)', r'\(A\) does <strong>not</strong> happen'), r'\(\overline{A}=\{1,\,3,\,5\}\)']])
  + chips(D6, A=A_, B=B_, cls='legend')
  + note(r"La unió és la paraula <strong>«o»</strong> (ajunta els elements de tots dos, sense repetir-los) i la intersecció és la paraula <strong>«i»</strong> (només els elements comuns). El contrari d'\(A\) són els elements de \(E\) que <strong>no</strong> són en \(A\).",
         r"La unión es la palabra <strong>«o»</strong> (junta los elementos de ambos, sin repetirlos) y la intersección es la palabra <strong>«y»</strong> (solo los elementos comunes). El contrario de \(A\) son los elementos de \(E\) que <strong>no</strong> están en \(A\).",
         r"Union is the word <strong>“or”</strong> (put the elements of both together, without repeating them) and intersection is the word <strong>“and”</strong> (only the common elements). The complement of \(A\) is the elements of \(E\) that are <strong>not</strong> in \(A\)."))

s2 += box('prop', L('Esdeveniments incompatibles', 'Sucesos incompatibles', 'Mutually exclusive events'),
  P(r"Dos esdeveniments són <strong>incompatibles</strong> si no poden ocórrer alhora, és a dir, si \(A\cap B=\varnothing\). Si poden ocórrer alhora, són <strong>compatibles</strong>.",
    r"Dos sucesos son <strong>incompatibles</strong> si no pueden ocurrir a la vez, es decir, si \(A\cap B=\varnothing\). Si pueden ocurrir a la vez, son <strong>compatibles</strong>.",
    r"Two events are <strong>mutually exclusive</strong> (incompatible) if they can't happen at the same time, that is, if \(A\cap B=\varnothing\). If they can happen together, they are <strong>compatible</strong>.")
  + ul(L(r"«Traure parell» i «traure múltiple de 3» són <strong>compatibles</strong>: si ix un 6, ocorren tots dos.", r"«Sacar par» y «sacar múltiplo de 3» son <strong>compatibles</strong>: si sale un 6, ocurren los dos.", r"“Even” and “multiple of 3” are <strong>compatible</strong>: if a 6 comes up, both happen."),
       L(r"«Traure un 1» i «traure un 6» són <strong>incompatibles</strong>, però <strong>no</strong> són contraris: si ix un 3, no ocorre cap dels dos.", r"«Sacar un 1» y «sacar un 6» son <strong>incompatibles</strong>, pero <strong>no</strong> son contrarios: si sale un 3, no ocurre ninguno de los dos.", r"“Roll a 1” and “roll a 6” are <strong>mutually exclusive</strong>, but they are <strong>not</strong> complementary: if a 3 comes up, neither happens."))
  + P(r"Un esdeveniment i el seu contrari sempre són incompatibles i, a més, entre tots dos completen l'espai mostral:",
      r"Un suceso y su contrario siempre son incompatibles y, además, entre los dos completan el espacio muestral:",
      r"An event and its complement are always mutually exclusive and, together, they make up the whole sample space:")
  + D(r"A\cap\overline{A}=\varnothing\qquad\quad A\cup\overline{A}=E")
  + widget('w-ops', '🔀', L('Operacions amb esdeveniments', 'Operaciones con sucesos', 'Operations with events'),
           ['<div class="wrow"><div class="seg sg-u" role="group"></div></div>',
            '<div class="wrow"><span class="slab a">A</span><div class="seg sg-a" role="group"></div></div>',
            '<div class="wrow"><span class="slab b">B</span><div class="seg sg-b" role="group"></div></div>'],
           out='<div class="ops-out"></div>')
  + drill('ops', 'Entrena: opera amb esdeveniments', 'Entrena: opera con sucesos', 'Train: operate with events', mode='opts'))

# baralla espanyola: 40 cartes, 10 de cada pal; figures: sota, cavall, rei (12)
O_, F_ = 10, 12; OF = 3
assert O_ + F_ - OF == 19 and 40 - F_ == 28
B3 = [x for x in range(1, 21) if x % 3 == 0]; B5 = [x for x in range(1, 21) if x % 5 == 0]
assert B3 == [3, 6, 9, 12, 15, 18] and B5 == [5, 10, 15, 20] and sorted(set(B3) | set(B5)) == [3, 5, 6, 9, 10, 12, 15, 18, 20]
A2 = [2, 4, 6]; B2 = [4, 5, 6]
assert [x for x in A2 if x not in B2] == [2] and [x for x in D6 if x not in A2 and x not in B2] == [1, 3] == [x for x in D6 if x not in set(A2) | set(B2)]
s2 += levels(
 [prob(L(r"Llancem un dau. Siguen \(A=\) «menor que 4» i \(B=\) «parell». Calcula \(A\cup B\), \(A\cap B\), \(\overline{A}\) i \(\overline{B}\). Són incompatibles?",
         r"Lanzamos un dado. Sean \(A=\) «menor que 4» y \(B=\) «par». Calcula \(A\cup B\), \(A\cap B\), \(\overline{A}\) y \(\overline{B}\). ¿Son incompatibles?",
         r"We roll a die. Let \(A=\) “less than 4” and \(B=\) “even”. Find \(A\cup B\), \(A\cap B\), \(\overline{A}\) and \(\overline{B}\). Are they mutually exclusive?"),
       D(r"A=\{1,\,2,\,3\}\qquad B=\{2,\,4,\,6\}"),
       D(r"A\cup B=\{1,\,2,\,3,\,4,\,6\}\qquad A\cap B=\{2\}\qquad \overline{A}=\{4,\,5,\,6\}\qquad \overline{B}=\{1,\,3,\,5\}"),
       P(r"No són incompatibles, perquè \(A\cap B\neq\varnothing\): si ix un 2, ocorren tots dos.", r"No son incompatibles, porque \(A\cap B\neq\varnothing\): si sale un 2, ocurren los dos.", r"They aren't mutually exclusive, because \(A\cap B\neq\varnothing\): if a 2 comes up, both happen."))],
 [prob(L(r"Traiem una carta d'una baralla espanyola (40 cartes: oros, copes, espases i bastos, amb l'1 al 7, la sota, el cavall i el rei de cada pal). Siguen \(O=\) «oros» i \(F=\) «figura» (sota, cavall o rei). Quantes cartes té cada un d'aquests esdeveniments: \(O\cap F\), \(O\cup F\) i \(\overline{F}\)?",
         r"Sacamos una carta de una baraja española (40 cartas: oros, copas, espadas y bastos, con el 1 al 7, la sota, el caballo y el rey de cada palo). Sean \(O=\) «oros» y \(F=\) «figura» (sota, caballo o rey). ¿Cuántas cartas tiene cada uno de estos sucesos: \(O\cap F\), \(O\cup F\) y \(\overline{F}\)?",
         r"We draw a card from a Spanish pack (40 cards: coins, cups, swords and clubs, with 1 to 7, the jack, the knight and the king of each suit). Let \(O=\) “coins” and \(F=\) “face card” (jack, knight or king). How many cards does each of these events have: \(O\cap F\), \(O\cup F\) and \(\overline{F}\)?"),
       P(r"Hi ha 10 oros i \(3\cdot4=12\) figures.", r"Hay 10 oros y \(3\cdot4=12\) figuras.", r"There are 10 coins cards and \(3\cdot4=12\) face cards."),
       P(r"\(O\cap F\) = figures d'oros (sota, cavall i rei d'oros): <strong>3 cartes</strong>.", r"\(O\cap F\) = figuras de oros (sota, caballo y rey de oros): <strong>3 cartas</strong>.", r"\(O\cap F\) = face cards of coins (jack, knight and king of coins): <strong>3 cards</strong>."),
       P(r"\(O\cup F\): sumem oros i figures, però les 3 figures d'oros les hem comptat dues vegades: \(10+12-3=\) <strong>19 cartes</strong>.", r"\(O\cup F\): sumamos oros y figuras, pero las 3 figuras de oros las hemos contado dos veces: \(10+12-3=\) <strong>19 cartas</strong>.", r"\(O\cup F\): add coins and face cards, but the 3 face cards of coins have been counted twice: \(10+12-3=\) <strong>19 cards</strong>."),
       P(r"\(\overline{F}\) = les cartes que no són figura: \(40-12=\) <strong>28 cartes</strong>.", r"\(\overline{F}\) = las cartas que no son figura: \(40-12=\) <strong>28 cartas</strong>.", r"\(\overline{F}\) = the cards that aren't face cards: \(40-12=\) <strong>28 cards</strong>.")),
  prob(L(r"En un bombo hi ha 20 boles numerades de l'1 al 20. Siguen \(A=\) «múltiple de 3» i \(B=\) «múltiple de 5». Escriu \(A\cup B\) i \(A\cap B\).",
         r"En un bombo hay 20 bolas numeradas del 1 al 20. Sean \(A=\) «múltiplo de 3» y \(B=\) «múltiplo de 5». Escribe \(A\cup B\) y \(A\cap B\).",
         r"A drum holds 20 balls numbered 1 to 20. Let \(A=\) “multiple of 3” and \(B=\) “multiple of 5”. Write \(A\cup B\) and \(A\cap B\)."),
       D(r"A=\{3,\,6,\,9,\,12,\,15,\,18\}\qquad B=\{5,\,10,\,15,\,20\}"),
       D(r"A\cup B=\{3,\,5,\,6,\,9,\,10,\,12,\,15,\,18,\,20\}\qquad A\cap B=\{15\}"))],
 [prob(L(r"Llancem un dau. Siguen \(A=\) «parell» i \(B=\) «major que 3». Escriu amb operacions i calcula: a) «ocorre \(A\) però no \(B\)»; b) «no ocorre cap dels dos». Comprova que b) és el contrari d'\(A\cup B\).",
         r"Lanzamos un dado. Sean \(A=\) «par» y \(B=\) «mayor que 3». Escribe con operaciones y calcula: a) «ocurre \(A\) pero no \(B\)»; b) «no ocurre ninguno de los dos». Comprueba que b) es el contrario de \(A\cup B\).",
         r"We roll a die. Let \(A=\) “even” and \(B=\) “greater than 3”. Write using operations and work out: a) “\(A\) happens but \(B\) doesn't”; b) “neither happens”. Check that b) is the complement of \(A\cup B\)."),
       D(r"A=\{2,\,4,\,6\}\qquad B=\{4,\,5,\,6\}\qquad \overline{A}=\{1,\,3,\,5\}\qquad \overline{B}=\{1,\,2,\,3\}"),
       P(r"a) «\(A\) i no \(B\)» és \(A\cap\overline{B}=\{2\}\).", r"a) «\(A\) y no \(B\)» es \(A\cap\overline{B}=\{2\}\).", r"a) “\(A\) and not \(B\)” is \(A\cap\overline{B}=\{2\}\)."),
       P(r"b) «ni \(A\) ni \(B\)» és \(\overline{A}\cap\overline{B}=\{1,\,3\}\). I com que \(A\cup B=\{2,\,4,\,5,\,6\}\), el seu contrari també és \(\{1,\,3\}\ \checkmark\)", r"b) «ni \(A\) ni \(B\)» es \(\overline{A}\cap\overline{B}=\{1,\,3\}\). Y como \(A\cup B=\{2,\,4,\,5,\,6\}\), su contrario también es \(\{1,\,3\}\ \checkmark\)", r"b) “neither \(A\) nor \(B\)” is \(\overline{A}\cap\overline{B}=\{1,\,3\}\). And since \(A\cup B=\{2,\,4,\,5,\,6\}\), its complement is also \(\{1,\,3\}\ \checkmark\)"))])
s2 += practice([
  ('★', L(r"a) Llancem un dau. Siguen \(A=\{1,\,2\}\) i \(B=\{2,\,3,\,5\}\). Calcula \(A\cup B\), \(A\cap B\) i \(\overline{B}\).", r"a) Lanzamos un dado. Sean \(A=\{1,\,2\}\) y \(B=\{2,\,3,\,5\}\). Calcula \(A\cup B\), \(A\cap B\) y \(\overline{B}\).", r"a) We roll a die. Let \(A=\{1,\,2\}\) and \(B=\{2,\,3,\,5\}\). Find \(A\cup B\), \(A\cap B\) and \(\overline{B}\).")),
  ('★★', L(r"b) Al dau, escriu un esdeveniment incompatible amb «parell» que no siga el seu contrari. c) Quin és el contrari de «traure almenys un 5»… en un sol llançament?", r"b) En el dado, escribe un suceso incompatible con «par» que no sea su contrario. c) ¿Cuál es el contrario de «sacar al menos un 5»… en un solo lanzamiento?", r"b) On the die, write an event that is mutually exclusive with “even” but isn't its complement. c) What is the complement of “roll at least a 5”… in a single roll?")),
  ('★★★', L(r"d) Llancem dues monedes. Siguen \(A=\) «la primera és cara» i \(B=\) «les dues són iguals». Calcula \(A\cap B\), \(A\cup B\) i \(\overline{A\cup B}\).", r"d) Lanzamos dos monedas. Sean \(A=\) «la primera es cara» y \(B=\) «las dos son iguales». Calcula \(A\cap B\), \(A\cup B\) y \(\overline{A\cup B}\).", r"d) We toss two coins. Let \(A=\) “the first is heads” and \(B=\) “both are the same”. Find \(A\cap B\), \(A\cup B\) and \(\overline{A\cup B}\)."))],
  P(r"a) \(\{1,\,2,\,3,\,5\}\), \(\{2\}\), \(\{1,\,4,\,6\}\). b) Per exemple \(\{1,\,3\}\) o \(\{5\}\). c) «Traure 1, 2, 3 o 4» \(=\{1,\,2,\,3,\,4\}\). d) \(A=\{CC,\,CX\}\), \(B=\{CC,\,XX\}\): \(A\cap B=\{CC\}\), \(A\cup B=\{CC,\,CX,\,XX\}\), \(\overline{A\cup B}=\{XC\}\).",
    r"a) \(\{1,\,2,\,3,\,5\}\), \(\{2\}\), \(\{1,\,4,\,6\}\). b) Por ejemplo \(\{1,\,3\}\) o \(\{5\}\). c) «Sacar 1, 2, 3 o 4» \(=\{1,\,2,\,3,\,4\}\). d) \(A=\{CC,\,CX\}\), \(B=\{CC,\,XX\}\): \(A\cap B=\{CC\}\), \(A\cup B=\{CC,\,CX,\,XX\}\), \(\overline{A\cup B}=\{XC\}\).",
    r"a) \(\{1,\,2,\,3,\,5\}\), \(\{2\}\), \(\{1,\,4,\,6\}\). b) For example \(\{1,\,3\}\) or \(\{5\}\). c) “Roll 1, 2, 3 or 4” \(=\{1,\,2,\,3,\,4\}\). d) \(A=\{CC,\,CX\}\), \(B=\{CC,\,XX\}\): \(A\cap B=\{CC\}\), \(A\cup B=\{CC,\,CX,\,XX\}\), \(\overline{A\cup B}=\{XC\}\)."))
assert sorted({1, 2} | {2, 3, 5}) == [1, 2, 3, 5] and [x for x in D6 if x not in (2, 3, 5)] == [1, 4, 6]
