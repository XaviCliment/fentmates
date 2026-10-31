# 12.7 Extraccions amb i sense reemplaçament. Problemes
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

assert pp(3, 2, True, lambda s: s == 'RR') == Fr(9, 25) and pp(3, 2, False, lambda s: s == 'RR') == Fr(3, 10)
s7 = box('def', L('Extraccions amb reemplaçament i sense reemplaçament', 'Extracciones con reemplazamiento y sin reemplazamiento', 'Drawing with and without replacement'),
  P(r"Traiem dues boles, una darrere l'altra, d'una bossa amb 3 boles roges i 2 de blaves. Hi ha dues maneres de fer-ho:",
    r"Sacamos dos bolas, una detrás de otra, de una bolsa con 3 bolas rojas y 2 azules. Hay dos maneras de hacerlo:",
    r"We draw two balls, one after the other, from a bag with 3 red balls and 2 blue ones. There are two ways to do it:")
  + ul(L(r"<strong>Amb reemplaçament:</strong> tornem la primera bola a la bossa abans de traure la segona. La bossa és igual les dues vegades: les extraccions són <strong>independents</strong>.", r"<strong>Con reemplazamiento:</strong> devolvemos la primera bola a la bolsa antes de sacar la segunda. La bolsa es igual las dos veces: las extracciones son <strong>independientes</strong>.", r"<strong>With replacement:</strong> we put the first ball back before drawing the second. The bag is the same both times: the draws are <strong>independent</strong>."),
       L(r"<strong>Sense reemplaçament:</strong> no la tornem. En la segona extracció hi ha una bola menys i les probabilitats <strong>depenen</strong> del que ha eixit en la primera: les extraccions són <strong>dependents</strong>.", r"<strong>Sin reemplazamiento:</strong> no la devolvemos. En la segunda extracción hay una bola menos y las probabilidades <strong>dependen</strong> de lo que ha salido en la primera: las extracciones son <strong>dependientes</strong>.", r"<strong>Without replacement:</strong> we don't put it back. For the second draw there's one ball fewer and the probabilities <strong>depend</strong> on what came out first: the draws are <strong>dependent</strong>."))
  + figs(bag('RRRBB', cap=L('3 roges i 2 blaves', '3 rojas y 2 azules', '3 red and 2 blue')))
  + figs(btree(3, 2, True, W=330, cap=L('Amb reemplaçament', 'Con reemplazamiento', 'With replacement')), btree(3, 2, False, W=330, cap=L('Sense reemplaçament', 'Sin reemplazamiento', 'Without replacement')))
  + P(r"En tots dos casos multipliquem al llarg de cada camí:",
      r"En los dos casos multiplicamos a lo largo de cada camino:",
      r"In both cases we multiply along each path:")
  + D(r"%s\ P(RR)=\frac35\cdot\frac35=\frac9{25}\qquad\quad %s\ P(RR)=\frac35\cdot\frac24=\frac6{20}=\frac3{10}" % (Lt('Amb:', 'Con:', 'With:'), Lt('Sense:', 'Sin:', 'Without:')))
  + note(r"Sense reemplaçament, en la segona branca pensa: «quantes boles d'aquest color queden?» i «quantes boles queden en total?». Si la primera ha sigut roja, queden 2 roges de 4 boles.",
         r"Sin reemplazamiento, en la segunda rama piensa: «¿cuántas bolas de este color quedan?» y «¿cuántas bolas quedan en total?». Si la primera ha sido roja, quedan 2 rojas de 4 bolas.",
         r"Without replacement, on the second branch ask yourself: “how many balls of this colour are left?” and “how many balls are left altogether?”. If the first was red, 2 red are left out of 4 balls.")
  + widget('w-tree', '🌳', L("Diagrama d'arbre de dues extraccions", 'Diagrama de árbol de dos extracciones', 'Tree diagram for two draws'),
           ['<div class="wrow">' + rng('r', 1, 8, 1, 3, 'R') + rng('b', 1, 8, 1, 2, 'B') + '</div>',
            '<div class="wrow"><div class="seg sg-m" role="group"></div></div>',
            '<div class="wrow"><div class="seg sg-e" role="group"></div></div>'])
  + drill('tree', 'Entrena: dues extraccions', 'Entrena: dos extracciones', 'Train: two draws'))

s7 += box('prop', L('Com resoldre un problema de probabilitat', 'Cómo resolver un problema de probabilidad', 'How to solve a probability problem'),
  ol(L(r"Llig bé l'enunciat: quin és l'experiment? És simple o compost? Els resultats són equiprobables?", r"Lee bien el enunciado: ¿cuál es el experimento? ¿Es simple o compuesto? ¿Los resultados son equiprobables?", r"Read the problem carefully: what's the experiment? Is it simple or compound? Are the outcomes equally likely?"),
     L(r"Si és simple i regular, compta casos i aplica <strong>Laplace</strong>. Si les dades són una <strong>taula</strong>, compta a la taula.", r"Si es simple y regular, cuenta casos y aplica <strong>Laplace</strong>. Si los datos son una <strong>tabla</strong>, cuenta en la tabla.", r"If it's simple and regular, count cases and use <strong>Laplace</strong>. If the data are in a <strong>table</strong>, count in the table."),
     L(r"Si és compost, fes un <strong>diagrama d'arbre</strong> (o una taula de doble entrada), multiplica al llarg dels camins i suma els camins favorables.", r"Si es compuesto, haz un <strong>diagrama de árbol</strong> (o una tabla de doble entrada), multiplica a lo largo de los caminos y suma los caminos favorables.", r"If it's compound, draw a <strong>tree diagram</strong> (or a two-way table), multiply along the paths and add the favourable paths."),
     L(r"Si demanen «almenys un» o «algun», pensa en el <strong>contrari</strong>.", r"Si piden «al menos uno» o «alguno», piensa en el <strong>contrario</strong>.", r"If they ask for “at least one” or “any”, think of the <strong>complement</strong>."),
     L(r"Comprova que el resultat està entre 0 i 1 i que té sentit.", r"Comprueba que el resultado está entre 0 y 1 y que tiene sentido.", r"Check that the result is between 0 and 1 and that it makes sense.")))

assert pp(4, 6, True, lambda s: s == 'RR') == Fr(4, 25) and pp(4, 6, True, lambda s: s in ('RB', 'BR')) == Fr(12, 25)
assert pp(4, 6, False, lambda s: s == 'RR') == Fr(2, 15) and pp(4, 6, False, lambda s: s in ('RB', 'BR')) == Fr(8, 15) and pp(4, 6, False, lambda s: s == 'BB') == Fr(1, 3)
assert Fr(2, 15) + Fr(8, 15) + Fr(1, 3) == 1
assert Fr(10, 40) * Fr(9, 39) == Fr(3, 52)
URN = Fr(1, 2) * Fr(2, 5) + Fr(1, 2) * Fr(4, 5)
assert URN == Fr(3, 5)
UT = ptree([('C', '1/2', [('R|ball-r', '2/5', [], 'C, R: 1/2 · 2/5 = 1/5'), ('B|ball-b', '3/5', [], 'C, B: 3/10')]), ('X', '1/2', [('R|ball-r', '4/5', [], 'X, R: 1/2 · 4/5 = 2/5'), ('B|ball-b', '1/5', [], 'X, B: 1/10')])], W=330, rowh=36)
CT = tbl(['', L('Ulleres', 'Gafas', 'Glasses'), L('Sense ulleres', 'Sin gafas', 'No glasses'), 'Total'],
         [[L('<strong>Xiques</strong>', '<strong>Chicas</strong>', '<strong>Girls</strong>'), '6', '10', '16'],
          [L('<strong>Xics</strong>', '<strong>Chicos</strong>', '<strong>Boys</strong>'), '4', '10', '14'],
          ['<strong>Total</strong>', '10', '20', '30']], cls='narrow')
assert Fr(10, 30) == Fr(1, 3) and Fr(6, 30) == Fr(1, 5) and Fr(16 + 10 - 6, 30) == Fr(2, 3) and Fr(4, 14) == Fr(2, 7)
s7 += levels(
 [prob(L(r"En una bossa hi ha 4 boles roges i 6 de blaves. En traiem dues <strong>amb reemplaçament</strong>. Calcula la probabilitat que les dues siguen roges i que n'isca una de cada color.",
         r"En una bolsa hay 4 bolas rojas y 6 azules. Sacamos dos <strong>con reemplazamiento</strong>. Calcula la probabilidad de que las dos sean rojas y de que salga una de cada color.",
         r"A bag has 4 red balls and 6 blue ones. We draw two <strong>with replacement</strong>. Find the probability that both are red and that we get one of each colour."),
       figs(btree(4, 6, True)),
       D(r"P(RR)=\frac4{10}\cdot\frac4{10}=\frac{16}{100}=\boxed{\frac4{25}}"),
       D(r"P(\text{%s})=P(RB)+P(BR)=\frac{24}{100}+\frac{24}{100}=\frac{48}{100}=\boxed{\frac{12}{25}}" % Lt('una de cada', 'una de cada', 'one of each')))],
 [prob(L(r"Fes el mateix problema <strong>sense reemplaçament</strong> i calcula també la probabilitat que les dues siguen blaves. Comprova que les tres probabilitats sumen 1.",
         r"Haz el mismo problema <strong>sin reemplazamiento</strong> y calcula también la probabilidad de que las dos sean azules. Comprueba que las tres probabilidades suman 1.",
         r"Do the same problem <strong>without replacement</strong> and also find the probability that both are blue. Check that the three probabilities add up to 1."),
       figs(btree(4, 6, False)),
       D(r"P(RR)=\frac4{10}\cdot\frac39=\frac{12}{90}=\boxed{\frac2{15}}\qquad P(BB)=\frac6{10}\cdot\frac59=\frac{30}{90}=\boxed{\frac13}"),
       D(r"P(\text{%s})=\frac4{10}\cdot\frac69+\frac6{10}\cdot\frac49=\frac{48}{90}=\boxed{\frac8{15}}" % Lt('una de cada', 'una de cada', 'one of each')),
       P(r"Comprovació: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)", r"Comprobación: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)", r"Check: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)")),
  prob(L(r"Traiem dues cartes d'una baralla espanyola sense tornar la primera. Quina és la probabilitat que totes dues siguen d'oros?", r"Sacamos dos cartas de una baraja española sin devolver la primera. ¿Cuál es la probabilidad de que las dos sean de oros?", r"We draw two cards from a Spanish pack without putting the first back. What is the probability that both are coins?"),
       P(r"Després de traure un oro, queden 9 oros entre 39 cartes:", r"Después de sacar un oro, quedan 9 oros entre 39 cartas:", r"After drawing a coins card, 9 coins are left among 39 cards:"),
       D(r"P(OO)=\frac{10}{40}\cdot\frac9{39}=\frac{90}{1560}=\boxed{\frac3{52}}\approx0{,}06"))],
 [prob(L(r"Tenim dues urnes: la urna I té 2 boles roges i 3 de blaves, i la urna II té 4 roges i 1 blava. Llancem una moneda: si ix cara traiem una bola de la urna I, i si ix creu, de la urna II. Quina és la probabilitat que la bola siga roja?",
         r"Tenemos dos urnas: la urna I tiene 2 bolas rojas y 3 azules, y la urna II tiene 4 rojas y 1 azul. Lanzamos una moneda: si sale cara sacamos una bola de la urna I, y si sale cruz, de la urna II. ¿Cuál es la probabilidad de que la bola sea roja?",
         r"We have two urns: urn I has 2 red balls and 3 blue ones, and urn II has 4 red and 1 blue. We toss a coin: heads, we draw a ball from urn I; tails, from urn II. What is the probability that the ball is red?"),
       figs(UT),
       P(r"Hi ha dos camins que acaben en roja. En sumem les probabilitats:", r"Hay dos caminos que acaban en roja. Sumamos sus probabilidades:", r"Two paths end in red. Add their probabilities:"),
       D(r"P(R)=\frac12\cdot\frac25+\frac12\cdot\frac45=\frac15+\frac25=\boxed{\frac35}")),
  prob(L(r"En un grup de 3r d'ESO hi ha 30 alumnes. La taula mostra quants porten ulleres. Triem una persona a l'atzar. Calcula: a) \(P(\text{ulleres})\); b) \(P(\text{xica i ulleres})\); c) \(P(\text{xica o ulleres})\); d) si sabem que és un xic, quina és la probabilitat que porte ulleres?",
         r"En un grupo de 3º de ESO hay 30 alumnos. La tabla muestra cuántos llevan gafas. Elegimos una persona al azar. Calcula: a) \(P(\text{gafas})\); b) \(P(\text{chica y gafas})\); c) \(P(\text{chica o gafas})\); d) si sabemos que es un chico, ¿cuál es la probabilidad de que lleve gafas?",
         r"A Year 9 class has 30 students. The table shows how many wear glasses. We pick someone at random. Find: a) \(P(\text{glasses})\); b) \(P(\text{girl and glasses})\); c) \(P(\text{girl or glasses})\); d) if we know it's a boy, what is the probability that he wears glasses?") + CT,
       P(r"a) \(\frac{10}{30}=\frac13\). b) \(\frac6{30}=\frac15\).", r"a) \(\frac{10}{30}=\frac13\). b) \(\frac6{30}=\frac15\).", r"a) \(\frac{10}{30}=\frac13\). b) \(\frac6{30}=\frac15\)."),
       P(r"c) Xiques (16) més alumnes amb ulleres (10), sense comptar dues vegades les 6 xiques amb ulleres: \(\frac{16+10-6}{30}=\frac{20}{30}=\frac23\).", r"c) Chicas (16) más alumnos con gafas (10), sin contar dos veces las 6 chicas con gafas: \(\frac{16+10-6}{30}=\frac{20}{30}=\frac23\).", r"c) Girls (16) plus students with glasses (10), without counting the 6 girls with glasses twice: \(\frac{16+10-6}{30}=\frac{20}{30}=\frac23\)."),
       P(r"d) Ara només hi ha 14 casos possibles (els xics), i 4 porten ulleres: \(\frac4{14}=\frac27\).", r"d) Ahora solo hay 14 casos posibles (los chicos), y 4 llevan gafas: \(\frac4{14}=\frac27\).", r"d) Now there are only 14 possible cases (the boys), and 4 wear glasses: \(\frac4{14}=\frac27\)."))])
s7 += practice([
  ('★', L(r"a) En una bossa hi ha 2 boles blanques i 3 de negres. En traiem dues amb reemplaçament. Quina és la probabilitat que les dues siguen negres?", r"a) En una bolsa hay 2 bolas blancas y 3 negras. Sacamos dos con reemplazamiento. ¿Cuál es la probabilidad de que las dos sean negras?", r"a) A bag has 2 white balls and 3 black ones. We draw two with replacement. What is the probability that both are black?")),
  ('★★', L(r"b) Repeteix-ho sense reemplaçament. c) Traiem dues cartes d'una baralla espanyola sense reemplaçament. Quina és la probabilitat que cap no siga un as?", r"b) Repítelo sin reemplazamiento. c) Sacamos dos cartas de una baraja española sin reemplazamiento. ¿Cuál es la probabilidad de que ninguna sea un as?", r"b) Do it again without replacement. c) We draw two cards from a Spanish pack without replacement. What is the probability that neither is an ace?")),
  ('★★★', L(r"d) En una caixa hi ha 5 bombetes i 2 són defectuoses. En provem dues a l'atzar (sense reemplaçament). Quina és la probabilitat que almenys una siga defectuosa?", r"d) En una caja hay 5 bombillas y 2 son defectuosas. Probamos dos al azar (sin reemplazamiento). ¿Cuál es la probabilidad de que al menos una sea defectuosa?", r"d) A box has 5 light bulbs and 2 are faulty. We test two at random (without replacement). What is the probability that at least one is faulty?"))],
  P(r"a) \(\frac35\cdot\frac35=\frac9{25}\). b) \(\frac35\cdot\frac24=\frac3{10}\). c) \(\frac{36}{40}\cdot\frac{35}{39}=\frac{21}{26}\approx0{,}81\). d) Contrari: cap defectuosa, \(\frac35\cdot\frac24=\frac3{10}\); \(P=1-\frac3{10}=\frac7{10}\).",
    r"a) \(\frac35\cdot\frac35=\frac9{25}\). b) \(\frac35\cdot\frac24=\frac3{10}\). c) \(\frac{36}{40}\cdot\frac{35}{39}=\frac{21}{26}\approx0{,}81\). d) Contrario: ninguna defectuosa, \(\frac35\cdot\frac24=\frac3{10}\); \(P=1-\frac3{10}=\frac7{10}\).",
    r"a) \(\frac35\cdot\frac35=\frac9{25}\). b) \(\frac35\cdot\frac24=\frac3{10}\). c) \(\frac{36}{40}\cdot\frac{35}{39}=\frac{21}{26}\approx0.81\). d) Complement: none faulty, \(\frac35\cdot\frac24=\frac3{10}\); \(P=1-\frac3{10}=\frac7{10}\)."))
assert Fr(36, 40) * Fr(35, 39) == Fr(21, 26) and 1 - Fr(3, 5) * Fr(2, 4) == Fr(7, 10); ck(Fr(21, 26), '0,81', 2)
