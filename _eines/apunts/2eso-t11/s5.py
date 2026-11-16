# 11.5 Estratègies per al càlcul de probabilitats: diagrama d'arbre i taula de contingència
from comu import *

def btree(r, b, rep, W=360, cap=None):
    """arbre de dues extraccions d'una bossa amb r roges i b blaves"""
    n = r + b
    kids = []
    for c1, k1 in (('R', r), ('B', b)):
        ch = []
        for c2, k2 in (('R', r), ('B', b)):
            if rep: num, den = k2, n
            else: num, den = k2 - (c1 == c2), n - 1
            f = Fr(k1, n) * Fr(num, den)
            ch.append((c2 + '|' + BALLC[c2], f'{num}/{den}', [], f'{c1}{c2}: {k1}/{n} · {num}/{den} = {f.numerator}/{f.denominator}' if f.denominator > 1 else f'{c1}{c2}: {f}'))
        kids.append((c1 + '|' + BALLC[c1], f'{k1}/{n}', ch))
    return ptree(kids, W=W, rowh=36, cap=cap)
def pp(r, b, rep, ev):
    n = r + b; t = Fr(0)
    for c1, k1 in (('R', r), ('B', b)):
        for c2, k2 in (('R', r), ('B', b)):
            num, den = (k2, n) if rep else (k2 - (c1 == c2), n - 1)
            if ev(c1 + c2): t += Fr(k1, n) * Fr(num, den)
    return t

# ---------- arbres ----------
TMD = ptree([(c, '', [(str(d), '', [], c + str(d)) for d in range(1, 7)]) for c in 'CX'], W=230, rowh=19)
TC2 = ptree([('C', '1/2', [('C', '1/2', [], 'CC: 1/2 · 1/2 = 1/4'), ('X', '1/2', [], 'CX: 1/4')]), ('X', '1/2', [('C', '1/2', [], 'XC: 1/4'), ('X', '1/2', [], 'XX: 1/4')])], W=330)
s5 = box('def', L("Experiments compostos. El diagrama d'arbre", "Experimentos compuestos. El diagrama de árbol", 'Compound experiments. The tree diagram'),
  P(r"Un experiment és <strong>compost</strong> quan està format per diversos experiments simples, fets alhora o un darrere l'altre: llançar dues monedes, una moneda i un dau, dos daus, traure dues boles d'una bossa…",
    r"Un experimento es <strong>compuesto</strong> cuando está formado por varios experimentos simples, realizados a la vez o uno detrás de otro: lanzar dos monedas, una moneda y un dado, dos dados, sacar dos bolas de una bolsa…",
    r"An experiment is <strong>compound</strong> when it's made up of several simple experiments, done at the same time or one after another: tossing two coins, a coin and a die, two dice, drawing two balls from a bag…")
  + P(r"Per a no deixar-nos cap resultat, fem un <strong>diagrama d'arbre</strong>: dibuixem una branca per a cada resultat del primer experiment i, des de cada una, una branca per a cada resultat del segon. <strong>Cada camí</strong> de l'arrel a una fulla és un resultat de l'espai mostral. Per exemple, en llançar una moneda i un dau:",
      r"Para no dejarnos ningún resultado, hacemos un <strong>diagrama de árbol</strong>: dibujamos una rama para cada resultado del primer experimento y, desde cada una, una rama para cada resultado del segundo. <strong>Cada camino</strong> de la raíz a una hoja es un resultado del espacio muestral. Por ejemplo, al lanzar una moneda y un dado:",
      r"So as not to miss any outcome, we draw a <strong>tree diagram</strong>: one branch for each result of the first experiment and, from each of these, one branch for each result of the second. <strong>Each path</strong> from the root to a leaf is an outcome in the sample space. For example, tossing a coin and rolling a die:")
  + figs(TMD)
  + P(r"El nombre de resultats és el <strong>producte</strong> dels resultats de cada experiment: moneda i dau, \(2\cdot6=12\); tres monedes, \(2\cdot2\cdot2=8\); dos daus, \(6\cdot6=36\). Si l'experiment és regular, podem aplicar la llei de Laplace: \(P(C6)=\frac1{12}\), \(P(\text{%s})=\frac{6}{12}=\frac12\)." % Lt('creu i qualsevol nombre', 'cruz y cualquier número', 'tails and any number'),
      r"El número de resultados es el <strong>producto</strong> de los resultados de cada experimento: moneda y dado, \(2\cdot6=12\); tres monedas, \(2\cdot2\cdot2=8\); dos dados, \(6\cdot6=36\). Si el experimento es regular, podemos aplicar la ley de Laplace: \(P(C6)=\frac1{12}\), \(P(\text{%s})=\frac{6}{12}=\frac12\)." % Lt('creu i qualsevol nombre', 'cruz y cualquier número', 'tails and any number'),
      r"The number of outcomes is the <strong>product</strong> of the outcomes of each experiment: coin and die, \(2\cdot6=12\); three coins, \(2\cdot2\cdot2=8\); two dice, \(6\cdot6=36\). If the experiment is regular, we can use Laplace's rule: \(P(C6)=\frac1{12}\), \(P(\text{%s})=\frac{6}{12}=\frac12\)." % Lt('creu i qualsevol nombre', 'cruz y cualquier número', 'tails and any number')))
ck(Fr(1, 12), Fr(1, 12)); ck(Fr(6, 12), Fr(1, 2))

s5 += box('prop', L("Probabilitats en el diagrama d'arbre", 'Probabilidades en el diagrama de árbol', 'Probabilities on a tree diagram'),
  P(r"També podem escriure en cada branca la probabilitat d'aquell resultat. Llavors:",
    r"También podemos escribir en cada rama la probabilidad de ese resultado. Entonces:",
    r"We can also write the probability of each result on its branch. Then:")
  + ol(L(r"La probabilitat d'un camí és el <strong>producte</strong> de les probabilitats de les seues branques.", r"La probabilidad de un camino es el <strong>producto</strong> de las probabilidades de sus ramas.", r"The probability of a path is the <strong>product</strong> of the probabilities on its branches."),
       L(r"Si un esdeveniment està format per diversos camins, en <strong>sumem</strong> les probabilitats.", r"Si un suceso está formado por varios caminos, <strong>sumamos</strong> sus probabilidades.", r"If an event is made up of several paths, <strong>add</strong> their probabilities."),
       L(r"Les probabilitats de les branques que ixen d'un mateix punt sumen 1, i les de tots els camins, també.", r"Las probabilidades de las ramas que salen de un mismo punto suman 1, y las de todos los caminos, también.", r"The probabilities of the branches leaving the same point add up to 1, and so do those of all the paths."))
  + figs(TC2)
  + D(r"P(CC)=\frac12\cdot\frac12=\frac14\qquad P(\text{%s})=P(CX)+P(XC)=\frac14+\frac14=\frac12" % Lt('una cara i una creu', 'una cara y una cruz', 'one heads, one tails'))
  + P(r"Això és especialment útil quan els resultats <strong>no</strong> són equiprobables. Per exemple, si traiem dues boles d'una bossa amb 3 roges i 2 blaves, podem tornar la primera a la bossa (<strong>amb reemplaçament</strong>: la bossa és igual les dues vegades) o no tornar-la (<strong>sense reemplaçament</strong>: en la segona extracció hi ha una bola menys):",
      r"Esto es especialmente útil cuando los resultados <strong>no</strong> son equiprobables. Por ejemplo, si sacamos dos bolas de una bolsa con 3 rojas y 2 azules, podemos devolver la primera a la bolsa (<strong>con reemplazamiento</strong>: la bolsa es igual las dos veces) o no devolverla (<strong>sin reemplazamiento</strong>: en la segunda extracción hay una bola menos):",
      r"This is especially useful when the outcomes are <strong>not</strong> equally likely. For example, if we draw two balls from a bag with 3 red and 2 blue, we can put the first one back (<strong>with replacement</strong>: the bag is the same both times) or not (<strong>without replacement</strong>: there's one ball fewer for the second draw):")
  + figs(bag('RRRBB', cap=L('3 roges i 2 blaves', '3 rojas y 2 azules', '3 red and 2 blue')))
  + figs(btree(3, 2, True, W=330, cap=L('Amb reemplaçament', 'Con reemplazamiento', 'With replacement')), btree(3, 2, False, W=330, cap=L('Sense reemplaçament', 'Sin reemplazamiento', 'Without replacement')))
  + D(r"%s\ P(RR)=\frac35\cdot\frac35=\frac9{25}\qquad\quad %s\ P(RR)=\frac35\cdot\frac24=\frac6{20}=\frac3{10}" % (Lt('Amb:', 'Con:', 'With:'), Lt('Sense:', 'Sin:', 'Without:')))
  + note(r"Sense reemplaçament, en la segona branca pensa: «quantes boles d'aquest color queden?» i «quantes boles queden en total?». Si la primera ha sigut roja, queden 2 roges de 4 boles.",
         r"Sin reemplazamiento, en la segunda rama piensa: «¿cuántas bolas de este color quedan?» y «¿cuántas bolas quedan en total?». Si la primera ha sido roja, quedan 2 rojas de 4 bolas.",
         r"Without replacement, on the second branch ask yourself: “how many balls of this colour are left?” and “how many balls are left altogether?”. If the first was red, 2 red are left out of 4 balls.")
  + widget('w-tree', '🌳', L("Diagrama d'arbre de dues extraccions", 'Diagrama de árbol de dos extracciones', 'Tree diagram for two draws'),
           ['<div class="wrow">' + rng('r', 1, 8, 1, 3, 'R') + rng('b', 1, 8, 1, 2, 'B') + '</div>',
            '<div class="wrow"><div class="seg sg-m" role="group"></div></div>',
            '<div class="wrow"><div class="seg sg-e" role="group"></div></div>'])
  + drill('tree', 'Entrena: dues extraccions', 'Entrena: dos extracciones', 'Train: two draws'))
assert pp(3, 2, True, lambda s: s == 'RR') == Fr(9, 25) and pp(3, 2, False, lambda s: s == 'RR') == Fr(3, 10)

# ---------- taula de doble entrada ----------
s5 += box('prop', L('Taula de doble entrada: dos daus', 'Tabla de doble entrada: dos dados', 'Two-way table: two dice'),
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

# ---------- taula de contingència ----------
GL = [[6, 10], [4, 10]]   # files: xiques, xics · columnes: ulleres, sense ulleres
assert [sum(r) for r in GL] == [16, 14] and [GL[0][j] + GL[1][j] for j in (0, 1)] == [10, 20] and sum(map(sum, GL)) == 30
RH = [L('Xiques', 'Chicas', 'Girls'), L('Xics', 'Chicos', 'Boys')]
CH = [L('Ulleres', 'Gafas', 'Glasses'), L('Sense ulleres', 'Sin gafas', 'No glasses')]
s5 += box('def', L('La taula de contingència', 'La tabla de contingencia', 'The contingency table'),
  P(r"Quan triem a l'atzar una persona (o un objecte) d'un grup i ens fixem en <strong>dues característiques</strong> alhora, organitzem les dades en una <strong>taula de contingència</strong>: cada casella diu quants elements tenen alhora la característica de la fila i la de la columna, i a la vora hi ha els <strong>totals</strong>. En un grup de 30 alumnes de 2n d'ESO:",
    r"Cuando elegimos al azar una persona (o un objeto) de un grupo y nos fijamos en <strong>dos características</strong> a la vez, organizamos los datos en una <strong>tabla de contingencia</strong>: cada casilla dice cuántos elementos tienen a la vez la característica de la fila y la de la columna, y en el borde están los <strong>totales</strong>. En un grupo de 30 alumnos de 2º de ESO:",
    r"When we pick a person (or an object) at random from a group and look at <strong>two characteristics</strong> at once, we organise the data in a <strong>contingency table</strong>: each cell says how many elements have both the row characteristic and the column characteristic, and the <strong>totals</strong> are along the edge. In a Year 8 class of 30 students:")
  + ctab(RH, CH, GL)
  + P(r"Com que triem la persona a l'atzar, tots els alumnes tenen la mateixa probabilitat de ser triats i podem aplicar la llei de Laplace: els casos possibles són el <strong>total</strong> (30) i els favorables, els de la casella o la fila o columna que corresponga:",
      r"Como elegimos a la persona al azar, todos los alumnos tienen la misma probabilidad de ser elegidos y podemos aplicar la ley de Laplace: los casos posibles son el <strong>total</strong> (30) y los favorables, los de la casilla o la fila o columna que corresponda:",
      r"Since we pick the person at random, every student is equally likely to be chosen and we can use Laplace's rule: the possible outcomes are the <strong>total</strong> (30) and the favourable ones are those in the matching cell, row or column:")
  + ul(L(r"\(P(\text{xica})=\frac{16}{30}=\frac8{15}\) (total de la fila de les xiques).", r"\(P(\text{chica})=\frac{16}{30}=\frac8{15}\) (total de la fila de las chicas).", r"\(P(\text{girl})=\frac{16}{30}=\frac8{15}\) (total of the girls' row)."),
       L(r"\(P(\text{ulleres})=\frac{10}{30}=\frac13\) (total de la columna de les ulleres).", r"\(P(\text{gafas})=\frac{10}{30}=\frac13\) (total de la columna de las gafas).", r"\(P(\text{glasses})=\frac{10}{30}=\frac13\) (total of the glasses column)."),
       L(r"\(P(\text{xica i ulleres})=\frac6{30}=\frac15\) (una sola casella: les dues coses alhora).", r"\(P(\text{chica y gafas})=\frac6{30}=\frac15\) (una sola casilla: las dos cosas a la vez).", r"\(P(\text{girl and glasses})=\frac6{30}=\frac15\) (a single cell: both at once)."),
       L(r"\(P(\text{xica o ulleres})=\frac{6+10+4}{30}=\frac{20}{30}=\frac23\) (les caselles on hi ha alguna de les dues coses, sense comptar-ne cap dues vegades).", r"\(P(\text{chica o gafas})=\frac{6+10+4}{30}=\frac{20}{30}=\frac23\) (las casillas donde hay alguna de las dos cosas, sin contar ninguna dos veces).", r"\(P(\text{girl or glasses})=\frac{6+10+4}{30}=\frac{20}{30}=\frac23\) (the cells with at least one of the two, without counting any twice)."),
       L(r"Si ja sabem que és un xic, els casos possibles són només els 14 xics: \(P(\text{ulleres, si és xic})=\frac4{14}=\frac27\).", r"Si ya sabemos que es un chico, los casos posibles son solo los 14 chicos: \(P(\text{gafas, si es chico})=\frac4{14}=\frac27\).", r"If we already know it's a boy, the possible outcomes are only the 14 boys: \(P(\text{glasses, if boy})=\frac4{14}=\frac27\)."))
  + note(r"Abans de calcular, <strong>completa la taula</strong>: les caselles de cada fila sumen el total de la fila, les de cada columna sumen el total de la columna, i tots els totals sumen el total general. Moltes vegades l'enunciat només dona algunes dades i les altres s'han de trobar sumant o restant.",
         r"Antes de calcular, <strong>completa la tabla</strong>: las casillas de cada fila suman el total de la fila, las de cada columna suman el total de la columna, y todos los totales suman el total general. Muchas veces el enunciado solo da algunos datos y los otros hay que encontrarlos sumando o restando.",
         r"Before calculating, <strong>complete the table</strong>: the cells in each row add up to the row total, those in each column add up to the column total, and the totals add up to the grand total. Often the problem only gives some of the data and the rest must be found by adding or subtracting.")
  + widget('w-cont', '🧮', L('Taula de contingència', 'Tabla de contingencia', 'Contingency table'),
           ['<div class="wrow"><div class="seg sg-c" role="group"></div></div>',
            '<div class="ct-box"></div>',
            '<div class="wrow"><div class="seg sg-e" role="group"></div></div>'])
  + drill('cont', 'Entrena: taules de contingència', 'Entrena: tablas de contingencia', 'Train: contingency tables'))
ck(Fr(16, 30), Fr(8, 15)); ck(Fr(10, 30), Fr(1, 3)); ck(Fr(6, 30), Fr(1, 5)); ck(Fr(6 + 10 + 4, 30), Fr(2, 3)); ck(Fr(4, 14), Fr(2, 7))
assert 16 + 10 - 6 == 6 + 10 + 4

s5 += box('prop', L('Quina estratègia faig servir?', '¿Qué estrategia utilizo?', 'Which strategy should I use?'),
  ol(L(r"Llig bé l'enunciat: quin és l'experiment? És simple o compost? Els resultats són equiprobables?", r"Lee bien el enunciado: ¿cuál es el experimento? ¿Es simple o compuesto? ¿Los resultados son equiprobables?", r"Read the problem carefully: what's the experiment? Is it simple or compound? Are the outcomes equally likely?"),
     L(r"Si és simple i regular, compta casos i aplica <strong>Laplace</strong>.", r"Si es simple y regular, cuenta casos y aplica <strong>Laplace</strong>.", r"If it's simple and regular, count cases and use <strong>Laplace</strong>."),
     L(r"Si és compost (es fa en diverses etapes), fes un <strong>diagrama d'arbre</strong>: multiplica al llarg dels camins i suma els camins favorables. Si només té dues parts, també pots fer una <strong>taula de doble entrada</strong>.", r"Si es compuesto (se hace en varias etapas), haz un <strong>diagrama de árbol</strong>: multiplica a lo largo de los caminos y suma los caminos favorables. Si solo tiene dos partes, también puedes hacer una <strong>tabla de doble entrada</strong>.", r"If it's compound (done in several stages), draw a <strong>tree diagram</strong>: multiply along the paths and add the favourable paths. If it has only two parts, you can also make a <strong>two-way table</strong>."),
     L(r"Si les dades classifiquen un grup segons dues característiques, fes (o completa) una <strong>taula de contingència</strong> i compta-hi.", r"Si los datos clasifican un grupo según dos características, haz (o completa) una <strong>tabla de contingencia</strong> y cuenta en ella.", r"If the data classify a group by two characteristics, make (or complete) a <strong>contingency table</strong> and count in it."),
     L(r"Comprova que el resultat està entre 0 i 1 i que té sentit.", r"Comprueba que el resultado está entre 0 y 1 y que tiene sentido.", r"Check that the result is between 0 and 1 and that it makes sense.")))

# ---------- problemes ----------
TB = ptree([('E', '0,7', [('E', '0,7', [], 'EE: 0,49'), ('F', '0,3', [], 'EF: 0,21')]), ('F', '0,3', [('E', '0,7', [], 'FE: 0,21'), ('F', '0,3', [], 'FF: 0,09')])], W=300)
pe = Fr(7, 10)
assert pe * pe == Fr(49, 100) and 2 * pe * (1 - pe) == Fr(42, 100) and (1 - pe) ** 2 == Fr(9, 100) and Fr(49 + 42 + 9, 100) == 1
SP = [[18, 12], [9, 21]]  # files: 1r, 2n · columnes: esport, no
assert [sum(r) for r in SP] == [30, 30] and [SP[0][j] + SP[1][j] for j in (0, 1)] == [27, 33] and sum(map(sum, SP)) == 60
RS = [L('1r ESO', '1º ESO', 'Year 7'), L('2n ESO', '2º ESO', 'Year 8')]
CS = [L('Fa esport', 'Hace deporte', 'Does sport'), L('No en fa', 'No hace', "Doesn't")]
# exercici de completar: 200 persones, 120 dones; 90 persones van en bici, 50 de les quals són dones
BK = [[50, 70], [40, 40]]
assert sum(BK[0]) == 120 and BK[0][0] + BK[1][0] == 90 and sum(map(sum, BK)) == 200
RB = [L('Dones', 'Mujeres', 'Women'), L('Homes', 'Hombres', 'Men')]
CB = [L('Bici', 'Bici', 'Bike'), L('No bici', 'No bici', 'No bike')]
UT = ptree([('C', '1/2', [('R|ball-r', '2/5', [], 'C, R: 1/2 · 2/5 = 1/5'), ('B|ball-b', '3/5', [], 'C, B: 3/10')]), ('X', '1/2', [('R|ball-r', '4/5', [], 'X, R: 1/2 · 4/5 = 2/5'), ('B|ball-b', '1/5', [], 'X, B: 1/10')])], W=330, rowh=36)
URN = Fr(1, 2) * Fr(2, 5) + Fr(1, 2) * Fr(4, 5)
assert URN == Fr(3, 5)
s5 += levels(
 [prob(L(r"Llancem una moneda i un dau. Calcula la probabilitat de traure cara i un 6, i la de traure creu i un nombre parell.", r"Lanzamos una moneda y un dado. Calcula la probabilidad de sacar cara y un 6, y la de sacar cruz y un número par.", r"We toss a coin and roll a die. Find the probability of heads and a 6, and of tails and an even number."),
       P(r"Mirem l'arbre de la moneda i el dau: hi ha 12 camins equiprobables.", r"Miramos el árbol de la moneda y el dado: hay 12 caminos equiprobables.", r"Look at the coin-and-die tree: there are 12 equally likely paths."),
       D(r"P(C6)=\boxed{\frac1{12}}\qquad P(\{X2,\,X4,\,X6\})=\frac3{12}=\boxed{\frac14}"),
       P(r"També multiplicant: \(\frac12\cdot\frac16=\frac1{12}\) i \(\frac12\cdot\frac36=\frac14\ \checkmark\)", r"También multiplicando: \(\frac12\cdot\frac16=\frac1{12}\) y \(\frac12\cdot\frac36=\frac14\ \checkmark\)", r"Also by multiplying: \(\frac12\cdot\frac16=\frac1{12}\) and \(\frac12\cdot\frac36=\frac14\ \checkmark\)")),
  prob(L(r"En un institut hi ha 60 alumnes entre 1r i 2n d'ESO. La taula mostra quants fan esport fora de l'institut. Triem un alumne a l'atzar. Calcula: a) \(P(\text{fa esport})\); b) \(P(\text{és de 1r i fa esport})\); c) si sabem que és de 2n, quina és la probabilitat que faça esport?",
         r"En un instituto hay 60 alumnos entre 1º y 2º de ESO. La tabla muestra cuántos hacen deporte fuera del instituto. Elegimos un alumno al azar. Calcula: a) \(P(\text{hace deporte})\); b) \(P(\text{es de 1º y hace deporte})\); c) si sabemos que es de 2º, ¿cuál es la probabilidad de que haga deporte?",
         r"A school has 60 students in Years 7 and 8. The table shows how many do sport outside school. We pick a student at random. Find: a) \(P(\text{does sport})\); b) \(P(\text{Year 7 and does sport})\); c) if we know they're in Year 8, what is the probability that they do sport?") + ctab(RS, CS, SP),
       P(r"a) Total de la columna «fa esport»: \(\frac{27}{60}=\boxed{\frac9{20}}\). b) Una casella: \(\frac{18}{60}=\boxed{\frac3{10}}\).", r"a) Total de la columna «hace deporte»: \(\frac{27}{60}=\boxed{\frac9{20}}\). b) Una casilla: \(\frac{18}{60}=\boxed{\frac3{10}}\).", r"a) Total of the “does sport” column: \(\frac{27}{60}=\boxed{\frac9{20}}\). b) One cell: \(\frac{18}{60}=\boxed{\frac3{10}}\)."),
       P(r"c) Ara els casos possibles són els 30 alumnes de 2n, i 9 fan esport: \(\frac9{30}=\boxed{\frac3{10}}\).", r"c) Ahora los casos posibles son los 30 alumnos de 2º, y 9 hacen deporte: \(\frac9{30}=\boxed{\frac3{10}}\).", r"c) Now the possible outcomes are the 30 Year 8 students, and 9 do sport: \(\frac9{30}=\boxed{\frac3{10}}\)."))],
 [prob(L(r"Una jugadora encerta el 70 % dels tirs lliures. En llança dos (l'un no influeix en l'altre). Calcula la probabilitat que n'encerte tots dos, que no n'encerte cap i que n'encerte exactament un.",
         r"Una jugadora acierta el 70 % de los tiros libres. Lanza dos (uno no influye en el otro). Calcula la probabilidad de que acierte los dos, de que no acierte ninguno y de que acierte exactamente uno.",
         r"A player scores 70 % of her free throws. She takes two (one doesn't affect the other). Find the probability that she scores both, neither, and exactly one."),
       P(r"\(E\) = encert, \(F\) = fallada. Fem l'arbre:", r"\(E\) = acierto, \(F\) = fallo. Hacemos el árbol:", r"\(E\) = score, \(F\) = miss. Draw the tree:") + figs(TB),
       D(r"P(EE)=0{,}7\cdot0{,}7=\boxed{0{,}49}\qquad P(FF)=0{,}3\cdot0{,}3=\boxed{0{,}09}"),
       D(r"P(\text{%s})=P(EF)+P(FE)=0{,}21+0{,}21=\boxed{0{,}42}" % Lt('exactament un', 'exactamente uno', 'exactly one')),
       P(r"Comprovació: \(0{,}49+0{,}42+0{,}09=1\ \checkmark\)", r"Comprobación: \(0{,}49+0{,}42+0{,}09=1\ \checkmark\)", r"Check: \(0.49+0.42+0.09=1\ \checkmark\)")),
  prob(L(r"En una enquesta a 200 persones d'un poble, 120 són dones i 90 van a treballar amb bicicleta. De les dones, 50 van amb bicicleta. Completa la taula de contingència i calcula la probabilitat que una persona triada a l'atzar siga un home que va amb bicicleta, i la probabilitat que no vaja amb bicicleta.",
         r"En una encuesta a 200 personas de un pueblo, 120 son mujeres y 90 van a trabajar en bicicleta. De las mujeres, 50 van en bicicleta. Completa la tabla de contingencia y calcula la probabilidad de que una persona elegida al azar sea un hombre que va en bicicleta, y la probabilidad de que no vaya en bicicleta.",
         r"In a survey of 200 people in a village, 120 are women and 90 cycle to work. Of the women, 50 cycle. Complete the contingency table and find the probability that a person picked at random is a man who cycles, and the probability that they don't cycle."),
       P(r"Posem les dades i trobem la resta restant: homes \(200-120=80\); homes en bici \(90-50=40\); dones sense bici \(120-50=70\); homes sense bici \(80-40=40\).", r"Ponemos los datos y encontramos el resto restando: hombres \(200-120=80\); hombres en bici \(90-50=40\); mujeres sin bici \(120-50=70\); hombres sin bici \(80-40=40\).", r"Fill in the data and find the rest by subtracting: men \(200-120=80\); men by bike \(90-50=40\); women not by bike \(120-50=70\); men not by bike \(80-40=40\).")
       + ctab(RB, CB, BK, hit=lambda i, j: (i, j) == (1, 0)),
       D(r"P(\text{%s})=\frac{40}{200}=\boxed{\frac15}\qquad P(\text{%s})=\frac{70+40}{200}=\frac{110}{200}=\boxed{\frac{11}{20}}" % (Lt('home i bici', 'hombre y bici', 'man and bike'), Lt('no bici', 'no bici', 'no bike'))))],
 [prob(L(r"Tenim dues urnes: la urna I té 2 boles roges i 3 de blaves, i la urna II té 4 roges i 1 blava. Llancem una moneda: si ix cara traiem una bola de la urna I, i si ix creu, de la urna II. Quina és la probabilitat que la bola siga roja?",
         r"Tenemos dos urnas: la urna I tiene 2 bolas rojas y 3 azules, y la urna II tiene 4 rojas y 1 azul. Lanzamos una moneda: si sale cara sacamos una bola de la urna I, y si sale cruz, de la urna II. ¿Cuál es la probabilidad de que la bola sea roja?",
         r"We have two urns: urn I has 2 red balls and 3 blue ones, and urn II has 4 red and 1 blue. We toss a coin: heads, we draw a ball from urn I; tails, from urn II. What is the probability that the ball is red?"),
       figs(UT),
       P(r"Hi ha dos camins que acaben en roja. En sumem les probabilitats:", r"Hay dos caminos que acaban en roja. Sumamos sus probabilidades:", r"Two paths end in red. Add their probabilities:"),
       D(r"P(R)=\frac12\cdot\frac25+\frac12\cdot\frac45=\frac15+\frac25=\boxed{\frac35}")),
  prob(L(r"En una bossa hi ha 4 boles roges i 6 de blaves. En traiem dues <strong>sense reemplaçament</strong>. Calcula la probabilitat que les dues siguen roges, que les dues siguen blaves i que n'isca una de cada color. Comprova que les tres probabilitats sumen 1.",
         r"En una bolsa hay 4 bolas rojas y 6 azules. Sacamos dos <strong>sin reemplazamiento</strong>. Calcula la probabilidad de que las dos sean rojas, de que las dos sean azules y de que salga una de cada color. Comprueba que las tres probabilidades suman 1.",
         r"A bag has 4 red balls and 6 blue ones. We draw two <strong>without replacement</strong>. Find the probability that both are red, that both are blue and that we get one of each colour. Check that the three probabilities add up to 1."),
       figs(btree(4, 6, False)),
       D(r"P(RR)=\frac4{10}\cdot\frac39=\frac{12}{90}=\boxed{\frac2{15}}\qquad P(BB)=\frac6{10}\cdot\frac59=\frac{30}{90}=\boxed{\frac13}"),
       D(r"P(\text{%s})=\frac4{10}\cdot\frac69+\frac6{10}\cdot\frac49=\frac{48}{90}=\boxed{\frac8{15}}" % Lt('una de cada', 'una de cada', 'one of each')),
       P(r"Comprovació: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)", r"Comprobación: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)", r"Check: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)"))])
ck(Fr(27, 60), Fr(9, 20)); ck(Fr(18, 60), Fr(3, 10)); ck(Fr(9, 30), Fr(3, 10)); ck(Fr(40, 200), Fr(1, 5)); ck(Fr(110, 200), Fr(11, 20))
assert pp(4, 6, False, lambda s: s == 'RR') == Fr(2, 15) and pp(4, 6, False, lambda s: s in ('RB', 'BR')) == Fr(8, 15) and pp(4, 6, False, lambda s: s == 'BB') == Fr(1, 3)
s5 += practice([
  ('★', L(r"a) Llancem dues monedes. Quina és la probabilitat de traure dues creus? b) Llancem dos daus: quina és la probabilitat que la suma siga 5?", r"a) Lanzamos dos monedas. ¿Cuál es la probabilidad de sacar dos cruces? b) Lanzamos dos dados: ¿cuál es la probabilidad de que la suma sea 5?", r"a) We toss two coins. What is the probability of two tails? b) We roll two dice: what is the probability that the sum is 5?")),
  ('★★', L(r"c) Llancem tres monedes. Calcula la probabilitat de traure exactament dues cares. d) En una bossa hi ha 2 boles blanques i 3 de negres. En traiem dues amb reemplaçament. Quina és la probabilitat que les dues siguen negres? I sense reemplaçament?", r"c) Lanzamos tres monedas. Calcula la probabilidad de sacar exactamente dos caras. d) En una bolsa hay 2 bolas blancas y 3 negras. Sacamos dos con reemplazamiento. ¿Cuál es la probabilidad de que las dos sean negras? ¿Y sin reemplazamiento?", r"c) We toss three coins. Find the probability of exactly two heads. d) A bag has 2 white balls and 3 black ones. We draw two with replacement. What is the probability that both are black? And without replacement?")),
  ('★★★', L(r"e) En un institut hi ha 400 alumnes; 240 tenen mòbil propi, i dels 180 alumnes de primer cicle, 72 en tenen. Fes la taula de contingència i calcula la probabilitat que un alumne triat a l'atzar siga de primer cicle i no tinga mòbil. Si triem un alumne amb mòbil, quina és la probabilitat que siga de primer cicle?", r"e) En un instituto hay 400 alumnos; 240 tienen móvil propio, y de los 180 alumnos de primer ciclo, 72 lo tienen. Haz la tabla de contingencia y calcula la probabilidad de que un alumno elegido al azar sea de primer ciclo y no tenga móvil. Si elegimos un alumno con móvil, ¿cuál es la probabilidad de que sea de primer ciclo?", r"e) A school has 400 students; 240 have their own mobile phone, and of the 180 lower-school students, 72 have one. Make the contingency table and find the probability that a student picked at random is in the lower school and has no phone. If we pick a student with a phone, what is the probability that they're in the lower school?"))],
  P(r"a) \(\frac14\). b) \(\frac4{36}=\frac19\). c) \(CCX,\,CXC,\,XCC\): \(\frac38\). d) \(\frac35\cdot\frac35=\frac9{25}\); sense reemplaçament, \(\frac35\cdot\frac24=\frac3{10}\). e) Primer cicle sense mòbil: \(180-72=108\), \(P=\frac{108}{400}=\frac{27}{100}\). Entre els 240 amb mòbil, 72 són de primer cicle: \(\frac{72}{240}=\frac3{10}\).",
    r"a) \(\frac14\). b) \(\frac4{36}=\frac19\). c) \(CCX,\,CXC,\,XCC\): \(\frac38\). d) \(\frac35\cdot\frac35=\frac9{25}\); sin reemplazamiento, \(\frac35\cdot\frac24=\frac3{10}\). e) Primer ciclo sin móvil: \(180-72=108\), \(P=\frac{108}{400}=\frac{27}{100}\). Entre los 240 con móvil, 72 son de primer ciclo: \(\frac{72}{240}=\frac3{10}\).",
    r"a) \(\frac14\). b) \(\frac4{36}=\frac19\). c) \(CCX,\,CXC,\,XCC\): \(\frac38\). d) \(\frac35\cdot\frac35=\frac9{25}\); without replacement, \(\frac35\cdot\frac24=\frac3{10}\). e) Lower school without a phone: \(180-72=108\), \(P=\frac{108}{400}=\frac{27}{100}\). Among the 240 with a phone, 72 are in the lower school: \(\frac{72}{240}=\frac3{10}\)."))
assert len([1 for a in range(1, 7) for b in range(1, 7) if a + b == 5]) == 4 and Fr(108, 400) == Fr(27, 100) and Fr(72, 240) == Fr(3, 10)
assert pp(3, 2, True, lambda s: s == 'RR') == Fr(9, 25) and pp(3, 2, False, lambda s: s == 'RR') == Fr(3, 10)
