# 11.5 Experiències compostes. Probabilitat (experiències independents, regla del producte i el contrari)
# Fet a partir de l'apartat 11.5 de 2n ESO (../2eso-t11/s5.py) i de la regla del producte de 3r ESO (../3eso-t12/s56.py).
from comu import *

TMD = ptree([(c, '1/2', [(str(d), '1/6', [], c + str(d) + ': 1/12') for d in range(1, 7)]) for c in 'CX'], W=260, rowh=19)
TC2 = ptree([('C', '1/2', [('C', '1/2', [], 'CC: 1/2 · 1/2 = 1/4'), ('X', '1/2', [], 'CX: 1/4')]), ('X', '1/2', [('C', '1/2', [], 'XC: 1/4'), ('X', '1/2', [], 'XX: 1/4')])], W=330)
TIND = ptree([('A', '0,3', [('B', '0,6', [], 'A∩B: 0,18'), ('B̄', '0,4', [], '0,12')]), ('Ā', '0,7', [('B', '0,6', [], '0,42'), ('B̄', '0,4', [], 'Ā∩B̄: 0,28')])], W=380)
s5 = box('def', L("Experiències compostes", "Experiencias compuestas", 'Compound experiments'),
  P(r"Una experiència és <strong>composta</strong> quan està formada per diverses experiències simples, fetes alhora o una darrere l'altra: llançar dues monedes, una moneda i un dau, dos daus, traure dues boles d'una bossa, contestar a l'atzar diverses preguntes d'un test…",
    r"Una experiencia es <strong>compuesta</strong> cuando está formada por varias experiencias simples, realizadas a la vez o una detrás de otra: lanzar dos monedas, una moneda y un dado, dos dados, sacar dos bolas de una bolsa, contestar al azar varias preguntas de un test…",
    r"An experiment is <strong>compound</strong> when it's made up of several simple experiments, done at the same time or one after another: tossing two coins, a coin and a die, two dice, drawing two balls from a bag, answering several test questions at random…")
  + P(r"Per a calcular-ne probabilitats fem un <strong>diagrama d'arbre</strong> i escrivim en cada branca la probabilitat d'aquell resultat. En llançar una moneda i un dau:",
      r"Para calcular sus probabilidades hacemos un <strong>diagrama de árbol</strong> y escribimos en cada rama la probabilidad de ese resultado. Al lanzar una moneda y un dado:",
      r"To work out probabilities we draw a <strong>tree diagram</strong> and write the probability of each result on its branch. Tossing a coin and rolling a die:")
  + figs(TMD)
  + ol(L(r"La probabilitat d'un camí és el <strong>producte</strong> de les probabilitats de les seues branques: \(P(C6)=\frac12\cdot\frac16=\frac1{12}\).", r"La probabilidad de un camino es el <strong>producto</strong> de las probabilidades de sus ramas: \(P(C6)=\frac12\cdot\frac16=\frac1{12}\).", r"The probability of a path is the <strong>product</strong> of the probabilities on its branches: \(P(C6)=\frac12\cdot\frac16=\frac1{12}\)."),
       L(r"Si un esdeveniment està format per diversos camins, en <strong>sumem</strong> les probabilitats: \(P(\text{%s})=\frac1{12}+\frac1{12}+\frac1{12}=\frac14\)." % Lt('creu i parell', 'cruz y par', 'tails and even'), r"Si un suceso está formado por varios caminos, <strong>sumamos</strong> sus probabilidades: \(P(\text{%s})=\frac1{12}+\frac1{12}+\frac1{12}=\frac14\)." % Lt('creu i parell', 'cruz y par', 'tails and even'), r"If an event is made up of several paths, <strong>add</strong> their probabilities: \(P(\text{%s})=\frac1{12}+\frac1{12}+\frac1{12}=\frac14\)." % Lt('creu i parell', 'cruz y par', 'tails and even')),
       L(r"Les probabilitats de les branques que ixen d'un mateix punt sumen 1, i les de tots els camins, també.", r"Las probabilidades de las ramas que salen de un mismo punto suman 1, y las de todos los caminos, también.", r"The probabilities of the branches leaving the same point add up to 1, and so do those of all the paths.")))
ck(Fr(1, 2) * Fr(1, 6), Fr(1, 12)); ck(3 * Fr(1, 12), Fr(1, 4))

s5 += box('prop', L('Experiències independents. Regla del producte', 'Experiencias independientes. Regla del producto', 'Independent experiments. Product rule'),
  P(r"Dues experiències són <strong>independents</strong> quan el resultat de la primera no influeix en el de la segona: dues monedes, dos daus, una moneda i un dau, traure dues boles <strong>amb reemplaçament</strong>, el temps que fa a dues ciutats llunyanes… Llavors les probabilitats de la segona etapa de l'arbre són les mateixes, haja eixit el que haja eixit en la primera, i",
    r"Dos experiencias son <strong>independientes</strong> cuando el resultado de la primera no influye en el de la segunda: dos monedas, dos dados, una moneda y un dado, sacar dos bolas <strong>con reemplazamiento</strong>, el tiempo que hace en dos ciudades lejanas… Entonces las probabilidades de la segunda etapa del árbol son las mismas, haya salido lo que haya salido en la primera, y",
    r"Two experiments are <strong>independent</strong> when the result of the first doesn't affect the second: two coins, two dice, a coin and a die, drawing two balls <strong>with replacement</strong>, the weather in two distant cities… Then the probabilities in the second stage of the tree are the same whatever happened in the first, and")
  + D(r"P(A\cap B)=P(A)\cdot P(B)")
  + figs(TC2)
  + D(r"P(CC)=\frac12\cdot\frac12=\frac14\qquad P(\text{%s})=P(CX)+P(XC)=\frac14+\frac14=\frac12" % Lt('una cara i una creu', 'una cara y una cruz', 'one heads, one tails'))
  + P(r"També funciona amb decimals. Si la probabilitat que ploga dissabte és 0,3 i la que ploga diumenge és 0,6 (independents), la probabilitat que ploga els dos dies és \(0{,}3\cdot0{,}6=0{,}18\):",
      r"También funciona con decimales. Si la probabilidad de que llueva el sábado es 0,3 y la de que llueva el domingo es 0,6 (independientes), la probabilidad de que llueva los dos días es \(0{,}3\cdot0{,}6=0{,}18\):",
      r"It also works with decimals. If the probability of rain on Saturday is 0.3 and on Sunday 0.6 (independent), the probability of rain on both days is \(0.3\cdot0.6=0.18\):")
  + figs(TIND))
assert Fr(3, 10) * Fr(6, 10) == Fr(18, 100) and Fr(3, 10) * Fr(4, 10) == Fr(12, 100) and Fr(7, 10) * Fr(6, 10) == Fr(42, 100) and Fr(7, 10) * Fr(4, 10) == Fr(28, 100)

s5 += box('prop', L('«Almenys un»: fes servir el contrari', '«Al menos uno»: usa el contrario', '“At least one”: use the complement'),
  P(r"Quan demanen la probabilitat d'«almenys un» (o «algun»), sovint hi ha molts camins favorables. El contrari, «cap», és un sol camí:",
    r"Cuando piden la probabilidad de «al menos uno» (o «alguno»), a menudo hay muchos caminos favorables. El contrario, «ninguno», es un solo camino:",
    r"When asked for the probability of “at least one” (or “any”), there are often many favourable paths. The complement, “none”, is a single path:")
  + D(r"P(\text{%s})=1-P(\text{%s})" % (Lt('almenys un', 'al menos uno', 'at least one'), Lt('cap', 'ninguno', 'none')))
  + P(r"Plou almenys un dia del cap de setmana: \(1-0{,}7\cdot0{,}4=1-0{,}28=0{,}72\). Traiem almenys un 6 en llançar dos daus:",
      r"Llueve al menos un día del fin de semana: \(1-0{,}7\cdot0{,}4=1-0{,}28=0{,}72\). Sacamos al menos un 6 al lanzar dos dados:",
      r"It rains on at least one day of the weekend: \(1-0.7\cdot0.4=1-0.28=0.72\). Getting at least one 6 when rolling two dice:")
  + D(r"P(\text{%s})=1-P(\text{%s})=1-\frac56\cdot\frac56=1-\frac{25}{36}=\frac{11}{36}" % (Lt('almenys un 6', 'al menos un 6', 'at least one 6'), Lt('cap 6', 'ningún 6', 'no 6')))
  + note(r"Compte: la probabilitat d'almenys un 6 en dos daus <strong>no</strong> és \(\frac16+\frac16=\frac13\). Aquesta suma compta dues vegades el resultat (6, 6): els esdeveniments «6 en el primer» i «6 en el segon» no són incompatibles.",
         r"Cuidado: la probabilidad de al menos un 6 en dos dados <strong>no</strong> es \(\frac16+\frac16=\frac13\). Esa suma cuenta dos veces el resultado (6, 6): los sucesos «6 en el primero» y «6 en el segundo» no son incompatibles.",
         r"Careful: the probability of at least one 6 with two dice is <strong>not</strong> \(\frac16+\frac16=\frac13\). That sum counts the outcome (6, 6) twice: “6 on the first” and “6 on the second” aren't mutually exclusive.", '⚠️')
  + widget('w-ind', '🔗', L('Dues experiències independents', 'Dos experiencias independientes', 'Two independent experiments'),
           ['<div class="wrow">' + rng('a', 0, 1, 0.05, 0.3, 'P(A)') + rng('b', 0, 1, 0.05, 0.6, 'P(B)') + '</div>',
            quick([('0.3|0.6', L('pluja: 0,3 i 0,6', 'lluvia: 0,3 y 0,6', 'rain: 0.3 and 0.6')), ('0.5|0.5', L('dues monedes', 'dos monedas', 'two coins')), ('0.7|0.7', L('dos tirs del 70 %', 'dos tiros del 70 %', 'two 70 % shots')), ('0.95|0.9', L('dues peces fiables', 'dos piezas fiables', 'two reliable parts'))]),
            '<div class="wrow"><div class="seg sg-e" role="group"></div></div>'])
  + drill('ind', 'Entrena: experiències independents', 'Entrena: experiencias independientes', 'Train: independent experiments'))
assert 1 - Fr(7, 10) * Fr(4, 10) == Fr(72, 100) and 1 - Fr(5, 6) ** 2 == Fr(11, 36)

TB = ptree([('E', '0,7', [('E', '0,7', [], 'EE: 0,49'), ('F', '0,3', [], 'EF: 0,21')]), ('F', '0,3', [('E', '0,7', [], 'FE: 0,21'), ('F', '0,3', [], 'FF: 0,09')])], W=300)
pe = Fr(7, 10)
assert pe * pe == Fr(49, 100) and 2 * pe * (1 - pe) == Fr(42, 100) and (1 - pe) ** 2 == Fr(9, 100) and Fr(49 + 42 + 9, 100) == 1
assert 1 - Fr(5, 6) ** 3 == Fr(91, 216); ck(Fr(91, 216), '0,42', 2)
N4 = [n for n in range(1, 10) if 1 - Fr(5, 6) ** n > Fr(1, 2)][0]
assert N4 == 4 and 1 - Fr(5, 6) ** 4 == Fr(671, 1296); ck(Fr(671, 1296), '0,52', 2); ck(Fr(91, 216), '0,42', 2)
assert Fr(1, 4) ** 3 == Fr(1, 64) and Fr(3, 4) ** 3 == Fr(27, 64) and 1 - Fr(27, 64) == Fr(37, 64)
s5 += levels(
 [prob(L(r"Llancem una moneda i un dau. Calcula la probabilitat de traure cara i un 6, i la de traure creu i un nombre parell.", r"Lanzamos una moneda y un dado. Calcula la probabilidad de sacar cara y un 6, y la de sacar cruz y un número par.", r"We toss a coin and roll a die. Find the probability of heads and a 6, and of tails and an even number."),
       D(r"P(C\ \text{%s}\ 6)=\frac12\cdot\frac16=\boxed{\frac1{12}}\qquad P(X\ \text{%s}\ \text{%s})=\frac12\cdot\frac36=\boxed{\frac14}" % (Lt('i', 'y', 'and'), Lt('i', 'y', 'and'), Lt('parell', 'par', 'even'))),
       P(r"També per Laplace: hi ha \(2\cdot6=12\) resultats i només un és \(C6\): \(\frac1{12}\ \checkmark\)", r"También por Laplace: hay \(2\cdot6=12\) resultados y solo uno es \(C6\): \(\frac1{12}\ \checkmark\)", r"Also by Laplace: there are \(2\cdot6=12\) outcomes and only one is \(C6\): \(\frac1{12}\ \checkmark\)")),
  prob(L(r"Un test té 3 preguntes amb 4 opcions cadascuna (només una correcta). Si les contestem a l'atzar, quina és la probabilitat d'encertar-les totes? I de no encertar-ne cap?",
         r"Un test tiene 3 preguntas con 4 opciones cada una (solo una correcta). Si las contestamos al azar, ¿cuál es la probabilidad de acertarlas todas? ¿Y de no acertar ninguna?",
         r"A test has 3 questions with 4 options each (only one correct). If we answer at random, what is the probability of getting them all right? And none right?"),
       P(r"Cada pregunta és independent de les altres: encertem amb probabilitat \(\frac14\) i fallem amb \(\frac34\).", r"Cada pregunta es independiente de las otras: acertamos con probabilidad \(\frac14\) y fallamos con \(\frac34\).", r"Each question is independent of the others: we get it right with probability \(\frac14\) and wrong with \(\frac34\)."),
       D(r"P(EEE)=\frac14\cdot\frac14\cdot\frac14=\boxed{\frac1{64}}\qquad P(FFF)=\frac34\cdot\frac34\cdot\frac34=\boxed{\frac{27}{64}}"),
       P(r"I, amb el contrari, la probabilitat d'encertar-ne almenys una és \(1-\frac{27}{64}=\frac{37}{64}\).", r"Y, con el contrario, la probabilidad de acertar al menos una es \(1-\frac{27}{64}=\frac{37}{64}\).", r"And, using the complement, the probability of getting at least one right is \(1-\frac{27}{64}=\frac{37}{64}\)."))],
 [prob(L(r"Una jugadora encerta el 70 % dels tirs lliures. En llança dos (l'un no influeix en l'altre). Calcula la probabilitat que n'encerte tots dos, que no n'encerte cap i que n'encerte exactament un.",
         r"Una jugadora acierta el 70 % de los tiros libres. Lanza dos (uno no influye en el otro). Calcula la probabilidad de que acierte los dos, de que no acierte ninguno y de que acierte exactamente uno.",
         r"A player scores 70 % of her free throws. She takes two (one doesn't affect the other). Find the probability that she scores both, neither, and exactly one."),
       P(r"\(E\) = encert, \(F\) = fallada. Fem l'arbre:", r"\(E\) = acierto, \(F\) = fallo. Hacemos el árbol:", r"\(E\) = score, \(F\) = miss. Draw the tree:") + figs(TB),
       D(r"P(EE)=0{,}7\cdot0{,}7=\boxed{0{,}49}\qquad P(FF)=0{,}3\cdot0{,}3=\boxed{0{,}09}"),
       D(r"P(\text{%s})=P(EF)+P(FE)=0{,}21+0{,}21=\boxed{0{,}42}" % Lt('exactament un', 'exactamente uno', 'exactly one')),
       P(r"Comprovació: \(0{,}49+0{,}42+0{,}09=1\ \checkmark\)", r"Comprobación: \(0{,}49+0{,}42+0{,}09=1\ \checkmark\)", r"Check: \(0.49+0.42+0.09=1\ \checkmark\)")),
  prob(L(r"Llancem tres monedes. Calcula la probabilitat de traure exactament dues cares i la de traure almenys dues cares.", r"Lanzamos tres monedas. Calcula la probabilidad de sacar exactamente dos caras y la de sacar al menos dos caras.", r"We toss three coins. Find the probability of exactly two heads and of at least two heads."),
       P(r"Cada camí de l'arbre té probabilitat \(\frac12\cdot\frac12\cdot\frac12=\frac18\):", r"Cada camino del árbol tiene probabilidad \(\frac12\cdot\frac12\cdot\frac12=\frac18\):", r"Each path in the tree has probability \(\frac12\cdot\frac12\cdot\frac12=\frac18\):") + figs(ptree([(a, '1/2', [(b, '1/2', [(c, '1/2', [], a + b + c + ': 1/8') for c in 'CX']) for b in 'CX']) for a in 'CX'], W=330, rowh=26)),
       D(r"P(\text{%s})=P(CCX)+P(CXC)+P(XCC)=\frac38" % Lt('exactament dues cares', 'exactamente dos caras', 'exactly two heads')),
       P(r"«Almenys dues cares» vol dir dues o tres: afegim el camí \(CCC\).", r"«Al menos dos caras» quiere decir dos o tres: añadimos el camino \(CCC\).", r"“At least two heads” means two or three: add the path \(CCC\)."),
       D(r"P(\text{%s})=\frac38+\frac18=\frac48=\boxed{\frac12}" % Lt('almenys dues cares', 'al menos dos caras', 'at least two heads')))],
 [prob(L(r"Llancem un dau tres vegades. Quina és la probabilitat de traure almenys un 6?", r"Lanzamos un dado tres veces. ¿Cuál es la probabilidad de sacar al menos un 6?", r"We roll a die three times. What is the probability of getting at least one 6?"),
       P(r"«Almenys un 6» té molts casos (un, dos o tres sisos). El contrari és «cap 6», que és un sol camí de l'arbre:", r"«Al menos un 6» tiene muchos casos (uno, dos o tres seises). El contrario es «ningún 6», que es un solo camino del árbol:", r"“At least one 6” has many cases (one, two or three sixes). Its complement, “no 6”, is a single path in the tree:"),
       D(r"P(\text{%s})=\frac56\cdot\frac56\cdot\frac56=\frac{125}{216}" % Lt('cap 6', 'ningún 6', 'no 6')),
       D(r"P(\text{%s})=1-\frac{125}{216}=\boxed{\frac{91}{216}}\approx0{,}42" % Lt('almenys un 6', 'al menos un 6', 'at least one 6')),
       note(r"No és \(\frac16+\frac16+\frac16=\frac12\): aquesta suma compta més d'una vegada els casos amb dos o tres sisos.", r"No es \(\frac16+\frac16+\frac16=\frac12\): esa suma cuenta más de una vez los casos con dos o tres seises.", r"It isn't \(\frac16+\frac16+\frac16=\frac12\): that sum counts the cases with two or three sixes more than once.", '⚠️')),
  prob(L(r"Quantes vegades hem de llançar un dau, com a mínim, perquè la probabilitat de traure almenys un 6 siga més gran que \(\frac12\)?",
         r"¿Cuántas veces tenemos que lanzar un dado, como mínimo, para que la probabilidad de sacar al menos un 6 sea mayor que \(\frac12\)?",
         r"What is the smallest number of times we must roll a die for the probability of getting at least one 6 to be greater than \(\frac12\)?"),
       P(r"Si llancem el dau \(n\) vegades, \(P(\text{%s})=1-\left(\frac56\right)^n\). Provem valors de \(n\):" % Lt('almenys un 6', 'al menos un 6', 'at least one 6'),
         r"Si lanzamos el dado \(n\) veces, \(P(\text{%s})=1-\left(\frac56\right)^n\). Probamos valores de \(n\):" % Lt('almenys un 6', 'al menos un 6', 'at least one 6'),
         r"If we roll the die \(n\) times, \(P(\text{%s})=1-\left(\frac56\right)^n\). Try values of \(n\):" % Lt('almenys un 6', 'al menos un 6', 'at least one 6')),
       D(r"n=3:\ 1-\frac{125}{216}=\frac{91}{216}\approx0{,}42\qquad n=4:\ 1-\frac{625}{1296}=\frac{671}{1296}\approx0{,}52"),
       P(r"Cal llançar-lo <strong>4 vegades</strong>. (Amb tres, encara és menys probable traure algun 6 que no traure'n cap.)", r"Hay que lanzarlo <strong>4 veces</strong>. (Con tres, todavía es menos probable sacar algún 6 que no sacar ninguno.)", r"We need to roll it <strong>4 times</strong>. (With three, getting a 6 is still less likely than getting none.)"))])
s5 += practice([
  ('★', L(r"a) Llancem dues monedes i un dau. Quina és la probabilitat de traure dues cares i un 5? b) Llancem dos daus: quina és la probabilitat que tots dos siguen parells?", r"a) Lanzamos dos monedas y un dado. ¿Cuál es la probabilidad de sacar dos caras y un 5? b) Lanzamos dos dados: ¿cuál es la probabilidad de que los dos sean pares?", r"a) We toss two coins and roll a die. What is the probability of two heads and a 5? b) We roll two dice: what is the probability that both are even?")),
  ('★★', L(r"c) Un semàfor està en verd el 40 % del temps i un altre, independent, el 70 %. Quina és la probabilitat de trobar-ne almenys un en verd? d) Girem dues vegades una ruleta amb 4 sectors iguals (1, 2, 3 i 4). Quina és la probabilitat que el producte siga parell?", r"c) Un semáforo está en verde el 40 % del tiempo y otro, independiente, el 70 %. ¿Cuál es la probabilidad de encontrar al menos uno en verde? d) Giramos dos veces una ruleta con 4 sectores iguales (1, 2, 3 y 4). ¿Cuál es la probabilidad de que el producto sea par?", r"c) One traffic light is green 40 % of the time and another, independent one, 70 %. What is the probability of finding at least one green? d) We spin a wheel with 4 equal sectors (1, 2, 3 and 4) twice. What is the probability that the product is even?")),
  ('★★★', L(r"e) Un examen té 4 preguntes de vertader o fals. Si les contestes totes a l'atzar, quina és la probabilitat d'encertar-ne almenys una? I d'encertar-ne exactament tres?", r"e) Un examen tiene 4 preguntas de verdadero o falso. Si las contestas todas al azar, ¿cuál es la probabilidad de acertar al menos una? ¿Y de acertar exactamente tres?", r"e) A test has 4 true-or-false questions. If you answer them all at random, what is the probability of getting at least one right? And exactly three?"))],
  P(r"a) \(\frac12\cdot\frac12\cdot\frac16=\frac1{24}\). b) \(\frac36\cdot\frac36=\frac14\). c) \(1-0{,}6\cdot0{,}3=1-0{,}18=0{,}82\). d) Contrari: els dos senars, \(\frac24\cdot\frac24=\frac14\); \(P=1-\frac14=\frac34\). e) \(1-\left(\frac12\right)^4=\frac{15}{16}\); exactament tres: 4 camins (la fallada pot ser qualsevol de les 4 preguntes) de \(\frac1{16}\), \(\frac4{16}=\frac14\).",
    r"a) \(\frac12\cdot\frac12\cdot\frac16=\frac1{24}\). b) \(\frac36\cdot\frac36=\frac14\). c) \(1-0{,}6\cdot0{,}3=1-0{,}18=0{,}82\). d) Contrario: los dos impares, \(\frac24\cdot\frac24=\frac14\); \(P=1-\frac14=\frac34\). e) \(1-\left(\frac12\right)^4=\frac{15}{16}\); exactamente tres: 4 caminos (el fallo puede ser cualquiera de las 4 preguntas) de \(\frac1{16}\), \(\frac4{16}=\frac14\).",
    r"a) \(\frac12\cdot\frac12\cdot\frac16=\frac1{24}\). b) \(\frac36\cdot\frac36=\frac14\). c) \(1-0.6\cdot0.3=1-0.18=0.82\). d) Complement: both odd, \(\frac24\cdot\frac24=\frac14\); \(P=1-\frac14=\frac34\). e) \(1-\left(\frac12\right)^4=\frac{15}{16}\); exactly three: 4 paths (the wrong one can be any of the 4 questions) of \(\frac1{16}\), \(\frac4{16}=\frac14\)."))
assert Fr(1, 2) * Fr(1, 2) * Fr(1, 6) == Fr(1, 24) and Fr(1, 2) * Fr(1, 2) == Fr(1, 4) and 1 - Fr(6, 10) * Fr(3, 10) == Fr(82, 100)
assert Fr(len([1 for a in range(1, 5) for b in range(1, 5) if a * b % 2 == 0]), 16) == Fr(3, 4) and 1 - Fr(1, 16) == Fr(15, 16) and 4 * Fr(1, 16) == Fr(1, 4)
