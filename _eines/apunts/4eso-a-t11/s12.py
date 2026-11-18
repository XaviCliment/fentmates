# 11.1 Experiments · 11.2 Esdeveniments
# Fet a partir dels apartats 11.1-11.2 de 2n ESO (../2eso-t11/s12.py) i de l'apartat 12.2 de 3r ESO (../3eso-t12/s12.py):
# operacions amb esdeveniments (unió, intersecció, contrari) i esdeveniments incompatibles.
from comu import *

D6 = list(range(1, 7))

TREE3 = ptree([(a, '', [(b, '', [(c, '', [], a + b + c) for c in 'CX']) for b in 'CX']) for a in 'CX'], W=320, rowh=26, leaf=True)
TMD0 = ptree([(c, '', [(str(d), '', [], c + str(d)) for d in range(1, 7)]) for c in 'CX'], W=230, rowh=19)

# =====================================================================
# 11.1 Experiments
# =====================================================================
s1 = box('def', L('Experiments deterministes i aleatoris', 'Experimentos deterministas y aleatorios', 'Deterministic and random experiments'),
  P(r"Un <strong>experiment</strong> és qualsevol acció que fem per a observar-ne el resultat. N'hi ha de dos tipus:",
    r"Un <strong>experimento</strong> es cualquier acción que realizamos para observar su resultado. Los hay de dos tipos:",
    r"An <strong>experiment</strong> is any action we carry out in order to observe its result. There are two kinds:")
  + ul(L(r"Un experiment és <strong>determinista</strong> quan podem saber el resultat abans de fer-lo: si el repetim en les mateixes condicions, el resultat és sempre el mateix. Si deixem caure una pedra, cau; si escalfem aigua a 100 °C al nivell de la mar, bull; si paguem 3 kg de pomes a 2 €/kg, paguem 6 €.",
         r"Un experimento es <strong>determinista</strong> cuando podemos saber el resultado antes de realizarlo: si lo repetimos en las mismas condiciones, el resultado es siempre el mismo. Si dejamos caer una piedra, cae; si calentamos agua a 100 °C al nivel del mar, hierve; si pagamos 3 kg de manzanas a 2 €/kg, pagamos 6 €.",
         r"An experiment is <strong>deterministic</strong> when we can know the result before doing it: if we repeat it under the same conditions, the result is always the same. If we drop a stone, it falls; if we heat water to 100 °C at sea level, it boils; if we buy 3 kg of apples at €2/kg, we pay €6."),
       L(r"Un experiment és <strong>aleatori</strong> quan <strong>no</strong> podem predir el resultat, encara que el repetim moltes vegades en les mateixes condicions: llançar una moneda o un dau, traure una carta d'una baralla, traure una bola d'una bossa sense mirar, el número guanyador d'un sorteig…",
         r"Un experimento es <strong>aleatorio</strong> cuando <strong>no</strong> podemos predecir el resultado, aunque lo repitamos muchas veces en las mismas condiciones: lanzar una moneda o un dado, sacar una carta de una baraja, sacar una bola de una bolsa sin mirar, el número ganador de un sorteo…",
         r"An experiment is <strong>random</strong> when we <strong>can't</strong> predict the result, even if we repeat it many times under the same conditions: tossing a coin or rolling a die, drawing a card from a pack, taking a ball out of a bag without looking, the winning number in a draw…"))
  + P(r"En un experiment aleatori sí que sabem quins resultats <em>poden</em> eixir (en un dau, de l'1 al 6), però no sabem quin eixirà. Diem que el resultat depén de l'<strong>atzar</strong>.",
      r"En un experimento aleatorio sí sabemos qué resultados <em>pueden</em> salir (en un dado, del 1 al 6), pero no sabemos cuál saldrá. Decimos que el resultado depende del <strong>azar</strong>.",
      r"In a random experiment we do know which results <em>can</em> come up (on a die, 1 to 6), but we don't know which one will. We say the result depends on <strong>chance</strong>.")
  + note(r"La paraula <em>aleatori</em> ve del llatí <em>alea</em>, «dau». La <strong>probabilitat</strong> és la part de les matemàtiques que estudia els experiments aleatoris: no ens diu què eixirà, però sí com d'esperable és cada resultat.",
         r"La palabra <em>aleatorio</em> viene del latín <em>alea</em>, «dado». La <strong>probabilidad</strong> es la parte de las matemáticas que estudia los experimentos aleatorios: no nos dice qué saldrá, pero sí lo esperable que es cada resultado.",
         r"The Spanish and Catalan word <em>aleatorio / aleatori</em> (random) comes from the Latin <em>alea</em>, “die”. <strong>Probability</strong> is the part of mathematics that studies random experiments: it doesn't tell us what will happen, but it does tell us how likely each result is.", '🎲'))

s1 += box('prop', L("Com sabem si un experiment és aleatori?", '¿Cómo sabemos si un experimento es aleatorio?', 'How do we know whether an experiment is random?'),
  P(r"Pregunta't: <strong>si el repetisc en les mateixes condicions, puc saber segur què passarà?</strong>",
    r"Pregúntate: <strong>si lo repito en las mismas condiciones, ¿puedo saber seguro qué pasará?</strong>",
    r"Ask yourself: <strong>if I repeat it under the same conditions, can I be sure what will happen?</strong>")
  + tbl([L('Experiment', 'Experimento', 'Experiment'), L('Sabem el resultat?', '¿Sabemos el resultado?', 'Do we know the result?'), L('Tipus', 'Tipo', 'Type')],
        [[L("Calcular l'àrea d'un quadrat de 3 cm de costat", 'Calcular el área de un cuadrado de 3 cm de lado', 'Working out the area of a square with 3 cm sides'), L('Sí: 9 cm²', 'Sí: 9 cm²', 'Yes: 9 cm²'), L('<strong>determinista</strong>', '<strong>determinista</strong>', '<strong>deterministic</strong>')],
         [L('Girar una ruleta i mirar el color', 'Girar una ruleta y mirar el color', 'Spinning a wheel and looking at the colour'), L('No', 'No', 'No'), L('<strong>aleatori</strong>', '<strong>aleatorio</strong>', '<strong>random</strong>')],
         [L("Mesurar quant tarda a caure una pedra des de 5 m", 'Medir cuánto tarda en caer una piedra desde 5 m', 'Timing how long a stone takes to fall from 5 m'), L('Sí: sempre el mateix temps (1 s, aprox.)', 'Sí: siempre el mismo tiempo (1 s, aprox.)', 'Yes: always the same time (about 1 s)'), L('<strong>determinista</strong>', '<strong>determinista</strong>', '<strong>deterministic</strong>')],
         [L('Triar a l\'atzar un alumne de la classe', 'Elegir al azar un alumno de la clase', 'Picking a student from the class at random'), L('No', 'No', 'No'), L('<strong>aleatori</strong>', '<strong>aleatorio</strong>', '<strong>random</strong>')],
         [L("Mirar de quin color es posa el paper de tornassol en vinagre", 'Mirar de qué color se pone el papel de tornasol en vinagre', 'Seeing what colour litmus paper turns in vinegar'), L('Sí: sempre roig', 'Sí: siempre rojo', 'Yes: always red'), L('<strong>determinista</strong>', '<strong>determinista</strong>', '<strong>deterministic</strong>')]])
  + note(r"Compte amb les situacions en què el resultat <em>no el sabem</em> però no és per l'atzar: el resultat d'una operació que encara no hem fet és determinista (només cal calcular-lo).",
         r"Cuidado con las situaciones en las que el resultado <em>no lo sabemos</em> pero no es por el azar: el resultado de una operación que aún no hemos hecho es determinista (solo hay que calcularlo).",
         r"Be careful with situations where we <em>don't know</em> the result but not because of chance: the result of a calculation we haven't done yet is deterministic (we just have to work it out).", '⚠️')
  + drill('det', 'Entrena: aleatori o determinista?', 'Entrena: ¿aleatorio o determinista?', 'Train: random or deterministic?', mode='opts'))

s1 += box('def', L("El llenguatge de l'atzar", 'El lenguaje del azar', 'The language of chance'),
  P(r"Abans de mesurar la probabilitat amb nombres, la descrivim amb paraules. En llançar un dau:",
    r"Antes de medir la probabilidad con números, la describimos con palabras. Al lanzar un dado:",
    r"Before measuring probability with numbers, we describe it in words. When rolling a die:")
  + tbl([L('Paraula', 'Palabra', 'Word'), L('Vol dir…', 'Quiere decir…', 'It means…'), L('Exemple (dau)', 'Ejemplo (dado)', 'Example (die)')],
        [[L('<strong>segur</strong>', '<strong>seguro</strong>', '<strong>certain</strong>'), L('passarà sempre', 'pasará siempre', 'it will always happen'), L('traure un nombre de l\'1 al 6', 'sacar un número del 1 al 6', 'rolling a number from 1 to 6')],
         [L('<strong>molt probable</strong>', '<strong>muy probable</strong>', '<strong>very likely</strong>'), L('passarà quasi sempre', 'pasará casi siempre', 'it will almost always happen'), L('traure més d\'1', 'sacar más de 1', 'rolling more than 1')],
         [L('<strong>tan probable com no</strong>', '<strong>tan probable como no</strong>', '<strong>even chance</strong>'), L('la meitat de les vegades', 'la mitad de las veces', 'half of the time'), L('traure parell', 'sacar par', 'rolling an even number')],
         [L('<strong>poc probable</strong>', '<strong>poco probable</strong>', '<strong>unlikely</strong>'), L('passarà poques vegades', 'pasará pocas veces', 'it will rarely happen'), L('traure un 6', 'sacar un 6', 'rolling a 6')],
         [L('<strong>impossible</strong>', '<strong>imposible</strong>', '<strong>impossible</strong>'), L('no passarà mai', 'no pasará nunca', 'it will never happen'), L('traure un 7', 'sacar un 7', 'rolling a 7')]]))

s1 += box('def', L('Espai mostral', 'Espacio muestral', 'Sample space'),
  P(r"Cada resultat possible d'un experiment aleatori és un <strong>resultat elemental</strong> (o <strong>cas</strong>). El conjunt de tots els resultats possibles és l'<strong>espai mostral</strong>, i l'escrivim \(E\), entre claus:",
    r"Cada resultado posible de un experimento aleatorio es un <strong>resultado elemental</strong> (o <strong>caso</strong>). El conjunto de todos los resultados posibles es el <strong>espacio muestral</strong>, y lo escribimos \(E\), entre llaves:",
    r"Each possible result of a random experiment is an <strong>elementary outcome</strong>. The set of all possible outcomes is the <strong>sample space</strong>, written \(E\), in braces:")
  + ul(L(r"Llançar una moneda: \(E=\{C,\,X\}\) (cara i creu).", r"Lanzar una moneda: \(E=\{C,\,X\}\) (cara y cruz).", r"Tossing a coin: \(E=\{C,\,X\}\) (heads C and tails X)."),
       L(r"Llançar un dau: \(E=\{1,\,2,\,3,\,4,\,5,\,6\}\).", r"Lanzar un dado: \(E=\{1,\,2,\,3,\,4,\,5,\,6\}\).", r"Rolling a die: \(E=\{1,\,2,\,3,\,4,\,5,\,6\}\)."),
       L(r"Traure una bola d'una bossa amb boles roges, blaves i verdes: \(E=\{R,\,B,\,V\}\).", r"Sacar una bola de una bolsa con bolas rojas, azules y verdes: \(E=\{R,\,A,\,V\}\).", r"Taking a ball from a bag with red, blue and green balls: \(E=\{R,\,B,\,G\}\)."),
       L(r"Llançar dues monedes: \(E=\{CC,\,CX,\,XC,\,XX\}\). Atenció: \(CX\) (cara en la primera i creu en la segona) i \(XC\) són resultats diferents.", r"Lanzar dos monedas: \(E=\{CC,\,CX,\,XC,\,XX\}\). Atención: \(CX\) (cara en la primera y cruz en la segunda) y \(XC\) son resultados distintos.", r"Tossing two coins: \(E=\{CC,\,CX,\,XC,\,XX\}\). Careful: \(CX\) (heads on the first, tails on the second) and \(XC\) are different outcomes."))
  + note(r"Quan l'experiment té diverses parts (dues monedes, una moneda i un dau…), ordena els resultats amb un <strong>diagrama d'arbre</strong> o una taula perquè no se te n'oblide cap. Ho veiem tot seguit.",
         r"Cuando el experimento tiene varias partes (dos monedas, una moneda y un dado…), ordena los resultados con un <strong>diagrama de árbol</strong> o una tabla para que no se te olvide ninguno. Lo vemos a continuación.",
         r"When the experiment has several parts (two coins, a coin and a die…), organise the outcomes with a <strong>tree diagram</strong> or a table so you don't miss any. We'll see how right below.")
  + widget('w-esp', '🧪', L("Fes l'experiment", 'Haz el experimento', 'Do the experiment'),
           ['<div class="wrow"><div class="seg sg-x" role="group"></div></div>',
            '<div class="wrow"><button class="btn primary" type="button" data-a="go">🎲 ' + L("Fes l'experiment", 'Haz el experimento', 'Do the experiment') + '</button><button class="btn" type="button" data-a="clr">↺ ' + L('Esborra', 'Borrar', 'Clear') + '</button></div>'],
           out='<div class="esp-out"></div>'))

s1 += box('prop', L("Com s'escriu l'espai mostral d'un experiment compost", 'Cómo se escribe el espacio muestral de un experimento compuesto', 'How to write the sample space of a compound experiment'),
  P(r"Si fem diversos experiments seguits (o alhora), cada resultat és una llista ordenada amb un resultat de cada experiment. Per a no deixar-nos-en cap, els escrivim amb un <strong>diagrama d'arbre</strong>: una branca per a cada resultat del primer experiment i, des de cada una, una branca per a cada resultat del segon. En llançar una moneda i un dau:",
    r"Si hacemos varios experimentos seguidos (o a la vez), cada resultado es una lista ordenada con un resultado de cada experimento. Para no dejarnos ninguno, los escribimos con un <strong>diagrama de árbol</strong>: una rama para cada resultado del primer experimento y, desde cada una, una rama para cada resultado del segundo. Al lanzar una moneda y un dado:",
    r"If we carry out several experiments in a row (or at once), each outcome is an ordered list with one result from each experiment. To make sure we don't miss any, we write them with a <strong>tree diagram</strong>: one branch for each result of the first experiment and, from each, one branch for each result of the second. Tossing a coin and rolling a die:")
  + figs(TMD0)
  + D(r"E=\{C1,\,C2,\,C3,\,C4,\,C5,\,C6,\,X1,\,X2,\,X3,\,X4,\,X5,\,X6\}")
  + P(r"El nombre de resultats és el <strong>producte</strong> dels resultats de cada experiment: moneda i dau, \(2\cdot6=12\); tres monedes, \(2\cdot2\cdot2=8\); dos daus, \(6\cdot6=36\).",
      r"El número de resultados es el <strong>producto</strong> de los resultados de cada experimento: moneda y dado, \(2\cdot6=12\); tres monedas, \(2\cdot2\cdot2=8\); dos dados, \(6\cdot6=36\).",
      r"The number of outcomes is the <strong>product</strong> of the outcomes of each experiment: coin and die, \(2\cdot6=12\); three coins, \(2\cdot2\cdot2=8\); two dice, \(6\cdot6=36\)."))
assert 2 * 6 == 12 and 2 ** 3 == 8 and 6 * 6 == 36

LL = [a + b for a in 'SOL' for b in 'SOL' if a != b]
assert LL == ['SO', 'SL', 'OS', 'OL', 'LS', 'LO']
s1 += levels(
 [prob(L(r"Indica quins experiments són aleatoris i quins deterministes: a) llançar un dau de parxís; b) calcular el preu de 4 entrades a 7,50 € cadascuna; c) traure una carta d'una baralla; d) mirar a quina temperatura es fon el gel.",
         r"Indica qué experimentos son aleatorios y cuáles deterministas: a) lanzar un dado de parchís; b) calcular el precio de 4 entradas a 7,50 € cada una; c) sacar una carta de una baraja; d) mirar a qué temperatura se funde el hielo.",
         r"Say which experiments are random and which are deterministic: a) rolling a ludo die; b) working out the price of 4 tickets at €7.50 each; c) drawing a card from a pack; d) checking the temperature at which ice melts."),
       P(r"a) i c) són <strong>aleatoris</strong>: no sabem quin resultat eixirà. b) i d) són <strong>deterministes</strong>: el resultat és sempre el mateix (30 € i 0 °C).",
         r"a) y c) son <strong>aleatorios</strong>: no sabemos qué resultado saldrá. b) y d) son <strong>deterministas</strong>: el resultado es siempre el mismo (30 € y 0 °C).",
         r"a) and c) are <strong>random</strong>: we don't know which result will come up. b) and d) are <strong>deterministic</strong>: the result is always the same (€30 and 0 °C).")),
  prob(L(r"Escriu l'espai mostral d'aquests experiments: a) llançar dues monedes; b) triar a l'atzar un dia de la setmana; c) girar una ruleta de 5 sectors iguals de colors roig, blau, verd, groc i negre.",
         r"Escribe el espacio muestral de estos experimentos: a) lanzar dos monedas; b) elegir al azar un día de la semana; c) girar una ruleta de 5 sectores iguales de colores rojo, azul, verde, amarillo y negro.",
         r"Write the sample space of these experiments: a) tossing two coins; b) choosing a day of the week at random; c) spinning a wheel with 5 equal sectors coloured red, blue, green, yellow and black."),
       D(r"\text{a)}\ E=\{CC,\,CX,\,XC,\,XX\}"),
       P(r"b) \(E=\{\text{dl},\,\text{dt},\,\text{dc},\,\text{dj},\,\text{dv},\,\text{ds},\,\text{dg}\}\) (7 resultats). c) \(E=\{R,\,B,\,V,\,G,\,N\}\).",
         r"b) \(E=\{\text{L},\,\text{M},\,\text{X},\,\text{J},\,\text{V},\,\text{S},\,\text{D}\}\) (7 resultados). c) \(E=\{R,\,A,\,V,\,Am,\,N\}\).",
         r"b) \(E=\{\text{Mon},\,\text{Tue},\,\text{Wed},\,\text{Thu},\,\text{Fri},\,\text{Sat},\,\text{Sun}\}\) (7 outcomes). c) \(E=\{R,\,B,\,G,\,Y,\,K\}\)."))],
 [prob(L(r"En una bossa hi ha 5 boles roges i 1 de blava. Traiem una bola sense mirar. Descriu amb paraules (segur, probable, poc probable, impossible) els esdeveniments: a) traure una bola roja; b) traure una bola blava; c) traure una bola verda; d) traure una bola roja o blava.",
         r"En una bolsa hay 5 bolas rojas y 1 azul. Sacamos una bola sin mirar. Describe con palabras (seguro, probable, poco probable, imposible) los sucesos: a) sacar una bola roja; b) sacar una bola azul; c) sacar una bola verde; d) sacar una bola roja o azul.",
         r"A bag has 5 red balls and 1 blue one. We take a ball without looking. Describe in words (certain, likely, unlikely, impossible): a) getting a red ball; b) getting a blue ball; c) getting a green ball; d) getting a red or a blue ball."),
       figs(bag('RRRRRB')),
       P(r"a) <strong>Molt probable</strong>: hi ha moltes més roges. b) <strong>Poc probable</strong>: només n'hi ha una. c) <strong>Impossible</strong>: no hi ha cap bola verda. d) <strong>Segur</strong>: totes les boles són roges o blaves.",
         r"a) <strong>Muy probable</strong>: hay muchas más rojas. b) <strong>Poco probable</strong>: solo hay una. c) <strong>Imposible</strong>: no hay ninguna bola verde. d) <strong>Seguro</strong>: todas las bolas son rojas o azules.",
         r"a) <strong>Very likely</strong>: there are many more red ones. b) <strong>Unlikely</strong>: there's only one. c) <strong>Impossible</strong>: there are no green balls. d) <strong>Certain</strong>: all the balls are red or blue.")),
  prob(L(r"Escrivim les lletres S, O i L en tres targetes. En traiem dues, una darrere l'altra, i formem una «paraula» de dues lletres. Fes un diagrama d'arbre i escriu l'espai mostral. Quants resultats té? I si tornem la primera targeta abans de traure la segona?",
         r"Escribimos las letras S, O y L en tres tarjetas. Sacamos dos, una detrás de otra, y formamos una «palabra» de dos letras. Haz un diagrama de árbol y escribe el espacio muestral. ¿Cuántos resultados tiene? ¿Y si devolvemos la primera tarjeta antes de sacar la segunda?",
         r"We write the letters S, O and L on three cards. We draw two, one after the other, and make a two-letter “word”. Draw a tree diagram and write the sample space. How many outcomes are there? What if we put the first card back before drawing the second?"),
       P(r"Sense tornar la targeta, en la segona extracció només queden 2 lletres:", r"Sin devolver la tarjeta, en la segunda extracción solo quedan 2 letras:", r"Without putting the card back, only 2 letters are left for the second draw:")
       + figs(ptree([(a, '', [(b, '', [], a + b) for b in 'SOL' if b != a]) for a in 'SOL'], W=220, rowh=22)),
       D(r"E=\{SO,\,SL,\,OS,\,OL,\,LS,\,LO\}\quad(3\cdot2=6\ %s)" % Lt('resultats', 'resultados', 'outcomes')),
       P(r"Si tornem la targeta, la segona pot ser qualsevol de les 3 lletres: \(3\cdot3=9\) resultats (s'hi afigen \(SS\), \(OO\) i \(LL\)).",
         r"Si devolvemos la tarjeta, la segunda puede ser cualquiera de las 3 letras: \(3\cdot3=9\) resultados (se añaden \(SS\), \(OO\) y \(LL\)).",
         r"If we put the card back, the second can be any of the 3 letters: \(3\cdot3=9\) outcomes (adding \(SS\), \(OO\) and \(LL\))."))],
 [prob(L(r"L'Àlex diu: «Llançar una pilota a cistella és un experiment aleatori, però llançar-la des de dalt d'un edifici per a veure si cau és determinista». Té raó? I «mesurar l'altura d'un alumne triat a l'atzar»?",
         r"Álex dice: «Lanzar una pelota a canasta es un experimento aleatorio, pero lanzarla desde lo alto de un edificio para ver si cae es determinista». ¿Tiene razón? ¿Y «medir la altura de un alumno elegido al azar»?",
         r"Àlex says: “Shooting a ball at the basket is a random experiment, but dropping it from the top of a building to see whether it falls is deterministic.” Is he right? What about “measuring the height of a student picked at random”?"),
       P(r"Sí. Ningú no pot assegurar si una pilota entrarà a cistella (ni tan sols un bon jugador), però sí que podem assegurar que una pilota que deixem anar <strong>cau</strong>.",
         r"Sí. Nadie puede asegurar si una pelota entrará en la canasta (ni siquiera un buen jugador), pero sí podemos asegurar que una pelota que soltamos <strong>cae</strong>.",
         r"Yes. Nobody can be sure whether a ball will go in the basket (not even a good player), but we can be sure that a ball we let go of <strong>falls</strong>."),
       P(r"Mesurar l'altura d'un alumne <strong>triat a l'atzar</strong> és aleatori: no sabem quin alumne eixirà ni, per tant, quina altura mesurarem. (Si sempre mesuràrem el mateix alumne, seria determinista.)",
         r"Medir la altura de un alumno <strong>elegido al azar</strong> es aleatorio: no sabemos qué alumno saldrá ni, por tanto, qué altura mediremos. (Si siempre midiéramos al mismo alumno, sería determinista.)",
         r"Measuring the height of a student <strong>picked at random</strong> is random: we don't know which student will come up, so we don't know which height we'll measure. (If we always measured the same student, it would be deterministic.)")),
  prob(L(r"Llancem tres monedes. Fes un diagrama d'arbre, escriu l'espai mostral i l'esdeveniment \(A=\) «traure almenys dues cares».",
         r"Lanzamos tres monedas. Haz un diagrama de árbol, escribe el espacio muestral y el suceso \(A=\) «sacar al menos dos caras».",
         r"We toss three coins. Draw a tree diagram, write the sample space and the event \(A=\) “get at least two heads”."),
       P(r"Cada moneda pot eixir \(C\) o \(X\). En l'arbre, cada camí de l'esquerra a la dreta és un resultat:", r"Cada moneda puede salir \(C\) o \(X\). En el árbol, cada camino de izquierda a derecha es un resultado:", r"Each coin can land \(C\) or \(X\). In the tree, each path from left to right is an outcome:") + figs(TREE3),
       D(r"E=\{CCC,\,CCX,\,CXC,\,CXX,\,XCC,\,XCX,\,XXC,\,XXX\}"),
       P(r"«Almenys dues cares» vol dir <em>dues o tres</em> cares: \(A=\{CCC,\,CCX,\,CXC,\,XCC\}\).", r"«Al menos dos caras» quiere decir <em>dos o tres</em> caras: \(A=\{CCC,\,CCX,\,CXC,\,XCC\}\).", r"“At least two heads” means <em>two or three</em> heads: \(A=\{CCC,\,CCX,\,CXC,\,XCC\}\)."))])
s1 += practice([
  ('★', L(r"a) Escriu dos experiments aleatoris i dos de deterministes que no apareguen en aquests apunts.", r"a) Escribe dos experimentos aleatorios y dos deterministas que no aparezcan en estos apuntes.", r"a) Write two random and two deterministic experiments that don't appear in these notes.")),
  ('★★', L(r"b) Classifica: llançar una xinxeta; calcular el perímetre d'un hexàgon regular de 2 cm de costat; endevinar el temps que farà d'ací a un mes; traure una peça de dòmino d'una caixa sense mirar.", r"b) Clasifica: lanzar una chincheta; calcular el perímetro de un hexágono regular de 2 cm de lado; adivinar el tiempo que hará dentro de un mes; sacar una ficha de dominó de una caja sin mirar.", r"b) Classify: tossing a drawing pin; working out the perimeter of a regular hexagon with 2 cm sides; guessing the weather a month from now; taking a domino out of a box without looking.")),
  ('★★★', L(r"c) Amb un dau normal, escriu un esdeveniment segur, un de molt probable, un de poc probable i un d'impossible.", r"c) Con un dado normal, escribe un suceso seguro, uno muy probable, uno poco probable y uno imposible.", r"c) With an ordinary die, write a certain event, a very likely one, an unlikely one and an impossible one."))],
  P(r"a) Resposta oberta: per exemple, el número de la loteria o el color d'un caramel tret d'una bossa (aleatoris); el pes de 2 L d'aigua o el resultat de \(25\cdot4\) (deterministes). b) Aleatori; determinista (12 cm); aleatori; aleatori. c) Per exemple: «menys de 7» (segur), «més de 1» (molt probable), «un 1» (poc probable) i «un 0» (impossible).",
    r"a) Respuesta abierta: por ejemplo, el número de la lotería o el color de un caramelo sacado de una bolsa (aleatorios); el peso de 2 L de agua o el resultado de \(25\cdot4\) (deterministas). b) Aleatorio; determinista (12 cm); aleatorio; aleatorio. c) Por ejemplo: «menos de 7» (seguro), «más de 1» (muy probable), «un 1» (poco probable) y «un 0» (imposible).",
    r"a) Open answer: for example, the lottery number or the colour of a sweet taken from a bag (random); the weight of 2 L of water or the result of \(25\cdot4\) (deterministic). b) Random; deterministic (12 cm); random; random. c) For example: “less than 7” (certain), “more than 1” (very likely), “a 1” (unlikely) and “a 0” (impossible)."))
assert 6 * 2 == 12 and 4 * Fr(15, 2) == 30

# =====================================================================
# 11.2 Esdeveniments
# =====================================================================
s2 = box('def', L('Esdeveniments', 'Sucesos', 'Events'),
  P(r"Un <strong>esdeveniment</strong> és qualsevol subconjunt de l'espai mostral: un grup de resultats que descrivim amb una frase. Diem que un esdeveniment <strong>ocorre</strong> quan el resultat de l'experiment és un dels seus elements. En llançar un dau, per exemple:",
    r"Un <strong>suceso</strong> es cualquier subconjunto del espacio muestral: un grupo de resultados que describimos con una frase. Decimos que un suceso <strong>ocurre</strong> cuando el resultado del experimento es uno de sus elementos. Al lanzar un dado, por ejemplo:",
    r"An <strong>event</strong> is any subset of the sample space: a group of outcomes that we describe with a sentence. We say an event <strong>happens</strong> when the result of the experiment is one of its elements. When rolling a die, for example:")
  + tbl([L('Tipus', 'Tipo', 'Type'), L('Què és', 'Qué es', 'What it is'), L('Exemple (dau)', 'Ejemplo (dado)', 'Example (die)')],
        [[L('<strong>Elemental</strong>', '<strong>Elemental</strong>', '<strong>Elementary</strong>'), L('té un sol resultat', 'tiene un solo resultado', 'it has a single outcome'), L(r'«traure un 5» \(=\{5\}\)', r'«sacar un 5» \(=\{5\}\)', r'“roll a 5” \(=\{5\}\)')],
         [L('<strong>Compost</strong>', '<strong>Compuesto</strong>', '<strong>Compound</strong>'), L('té dos o més resultats', 'tiene dos o más resultados', 'it has two or more outcomes'), L(r'«traure parell» \(=\{2,\,4,\,6\}\)', r'«sacar par» \(=\{2,\,4,\,6\}\)', r'“roll an even number” \(=\{2,\,4,\,6\}\)')],
         [L('<strong>Segur</strong>', '<strong>Seguro</strong>', '<strong>Certain</strong>'), L(r"ocorre sempre: és tot l'espai mostral \(E\)", r"ocurre siempre: es todo el espacio muestral \(E\)", r"it always happens: it's the whole sample space \(E\)"), L(r'«traure menys de 7» \(=E\)', r'«sacar menos de 7» \(=E\)', r'“roll less than 7” \(=E\)')],
         [L('<strong>Impossible</strong>', '<strong>Imposible</strong>', '<strong>Impossible</strong>'), L(r"no ocorre mai: no té cap element, \(\varnothing\)", r"no ocurre nunca: no tiene ningún elemento, \(\varnothing\)", r"it never happens: it has no elements, \(\varnothing\)"), L(r'«traure un 8» \(=\varnothing\)', r'«sacar un 8» \(=\varnothing\)', r'“roll an 8” \(=\varnothing\)')]])
  + P(r"Els esdeveniments s'anomenen amb lletres majúscules: \(A=\) «traure parell» \(=\{2,\,4,\,6\}\). Els resultats d'\(A\) són els <strong>casos favorables</strong> a \(A\).",
      r"Los sucesos se nombran con letras mayúsculas: \(A=\) «sacar par» \(=\{2,\,4,\,6\}\). Los resultados de \(A\) son los <strong>casos favorables</strong> a \(A\).",
      r"Events are named with capital letters: \(A=\) “roll an even number” \(=\{2,\,4,\,6\}\). The outcomes in \(A\) are the outcomes <strong>favourable</strong> to \(A\).")
  + chips(D6, A=[2, 4, 6])
  + note(r"Escriu sempre els esdeveniments entre claus i amb tots els seus elements: és la millor manera de no equivocar-se després en comptar.",
         r"Escribe siempre los sucesos entre llaves y con todos sus elementos: es la mejor manera de no equivocarse después al contar.",
         r"Always write events in braces listing all their elements: it's the best way to avoid counting mistakes later.")
  + drill('tipus', 'Entrena: quin tipus d\'esdeveniment és?', 'Entrena: ¿qué tipo de suceso es?', 'Train: what kind of event is it?', mode='opts'))

A_ = [2, 4, 6]; B_ = [3, 6]
U_ = sorted(set(A_) | set(B_)); I_ = sorted(set(A_) & set(B_)); NA = [x for x in D6 if x not in A_]
assert U_ == [2, 3, 4, 6] and I_ == [6] and NA == [1, 3, 5]
s2 += box('def', L('Unió, intersecció i esdeveniment contrari', 'Unión, intersección y suceso contrario', 'Union, intersection and complementary event'),
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

PR10 = [x for x in range(1, 11) if x in (2, 3, 5, 7)]
assert PR10 == [2, 3, 5, 7]
PAIRS = ['Anna–Biel', 'Anna–Carla', 'Anna–Dani', 'Biel–Carla', 'Biel–Dani', 'Carla–Dani']
assert len(PAIRS) == math.comb(4, 2) and sum('Anna' in p for p in PAIRS) == 3
# baralla espanyola: 40 cartes, 10 de cada pal; figures: sota, cavall, rei (12)
O_, F_ = 10, 12; OF = 3
assert O_ + F_ - OF == 19 and 40 - F_ == 28
B3 = [x for x in range(1, 21) if x % 3 == 0]; B5 = [x for x in range(1, 21) if x % 5 == 0]
assert B3 == [3, 6, 9, 12, 15, 18] and B5 == [5, 10, 15, 20] and sorted(set(B3) | set(B5)) == [3, 5, 6, 9, 10, 12, 15, 18, 20]
A2 = [2, 4, 6]; B2 = [4, 5, 6]
assert [x for x in A2 if x not in B2] == [2] and [x for x in D6 if x not in A2 and x not in B2] == [1, 3] == [x for x in D6 if x not in set(A2) | set(B2)]
s2 += levels(
 [prob(L(r"Escriu l'espai mostral de l'experiment «girar una ruleta dividida en 8 sectors iguals numerats de l'1 al 8» i els esdeveniments \(A=\) «múltiple de 3» i \(B=\) «més gran que 5».",
         r"Escribe el espacio muestral del experimento «girar una ruleta dividida en 8 sectores iguales numerados del 1 al 8» y los sucesos \(A=\) «múltiplo de 3» y \(B=\) «mayor que 5».",
         r"Write the sample space of “spinning a wheel divided into 8 equal sectors numbered 1 to 8” and the events \(A=\) “multiple of 3” and \(B=\) “greater than 5”."),
       D(r"E=\{1,\,2,\,3,\,4,\,5,\,6,\,7,\,8\}\qquad A=\{3,\,6\}\qquad B=\{6,\,7,\,8\}")),
  prob(L(r"Traiem una bola d'una urna amb deu boles numerades de l'1 al 10. Escriu l'espai mostral i els esdeveniments \(A=\) «nombre primer», \(B=\) «major que 7», \(C=\) «múltiple d'11» i \(D=\) «menor que 11». De quin tipus és cadascun?",
         r"Sacamos una bola de una urna con diez bolas numeradas del 1 al 10. Escribe el espacio muestral y los sucesos \(A=\) «número primo», \(B=\) «mayor que 7», \(C=\) «múltiplo de 11» y \(D=\) «menor que 11». ¿De qué tipo es cada uno?",
         r"We take a ball from an urn with ten balls numbered 1 to 10. Write the sample space and the events \(A=\) “prime number”, \(B=\) “greater than 7”, \(C=\) “multiple of 11” and \(D=\) “less than 11”. What kind of event is each one?"),
       D(r"E=\{1,\,2,\,3,\,4,\,5,\,6,\,7,\,8,\,9,\,10\}"),
       D(r"A=\{2,\,3,\,5,\,7\}\qquad B=\{8,\,9,\,10\}\qquad C=\varnothing\qquad D=E"),
       P(r"\(A\) i \(B\) són <strong>compostos</strong>, \(C\) és <strong>impossible</strong> i \(D\) és <strong>segur</strong>.", r"\(A\) y \(B\) son <strong>compuestos</strong>, \(C\) es <strong>imposible</strong> y \(D\) es <strong>seguro</strong>.", r"\(A\) and \(B\) are <strong>compound</strong>, \(C\) is <strong>impossible</strong> and \(D\) is <strong>certain</strong>.")),
  prob(L(r"Llancem un dau. Siguen \(A=\) «menor que 4» i \(B=\) «parell». Calcula \(A\cup B\), \(A\cap B\), \(\overline{A}\) i \(\overline{B}\). Són incompatibles?",
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
 [prob(L(r"De quatre alumnes (Anna, Biel, Carla i Dani) en triem dos a l'atzar per a representar el grup. Escriu l'espai mostral. Quants resultats té l'esdeveniment «Anna és triada»?",
         r"De cuatro alumnos (Anna, Biel, Carla y Dani) elegimos dos al azar para representar al grupo. Escribe el espacio muestral. ¿Cuántos resultados tiene el suceso «Anna es elegida»?",
         r"From four students (Anna, Biel, Carla and Dani) we choose two at random to represent the class. Write the sample space. How many outcomes does the event “Anna is chosen” have?"),
       P(r"Ara l'ordre no importa (Anna–Biel és la mateixa parella que Biel–Anna). Fem les parelles de manera ordenada:", r"Ahora el orden no importa (Anna–Biel es la misma pareja que Biel–Anna). Formamos las parejas de manera ordenada:", r"Here order doesn't matter (Anna–Biel is the same pair as Biel–Anna). List the pairs systematically:"),
       chips(PAIRS, A=[p for p in PAIRS if 'Anna' in p]),
       P(r"L'espai mostral té <strong>6</strong> resultats i «Anna és triada» en té <strong>3</strong> (els marcats).", r"El espacio muestral tiene <strong>6</strong> resultados y «Anna es elegida» tiene <strong>3</strong> (los marcados).", r"The sample space has <strong>6</strong> outcomes and “Anna is chosen” has <strong>3</strong> (the highlighted ones).")),
  prob(L(r"Llancem un dau. Siguen \(A=\) «parell» i \(B=\) «major que 3». Escriu amb operacions i calcula: a) «ocorre \(A\) però no \(B\)»; b) «no ocorre cap dels dos». Comprova que b) és el contrari d'\(A\cup B\).",
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
assert [x for x in range(1, 9) if x % 3 == 0] == [3, 6] and [x for x in range(1, 9) if x > 5] == [6, 7, 8]
