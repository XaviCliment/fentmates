# 11.6 Experiències dependents. Probabilitat condicionada (extraccions sense reemplaçament, P(B/A), regla del producte
# P(A∩B) = P(A)·P(B/A) i probabilitat total sumant camins: dues urnes)
# Fet a partir de l'apartat 12.7 de 3r ESO (../3eso-t12/s7.py) i de l'apartat 11.5 de 2n ESO (../2eso-t11/s5.py).
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
s6 = box('def', L('Experiències dependents: extraccions sense reemplaçament', 'Experiencias dependientes: extracciones sin reemplazamiento', 'Dependent experiments: drawing without replacement'),
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
assert pp(3, 2, True, lambda s: s == 'RR') == Fr(9, 25) and pp(3, 2, False, lambda s: s == 'RR') == Fr(3, 10)

s6 += box('def', L('Probabilitat condicionada', 'Probabilidad condicionada', 'Conditional probability'),
  P(r"En les experiències dependents, la probabilitat de la segona etapa depén del que ha passat en la primera. La probabilitat que ocórrega \(B\) <strong>sabent que</strong> ja ha ocorregut \(A\) s'anomena <strong>probabilitat de \(B\) condicionada a \(A\)</strong> i s'escriu \(P(B/A)\). En la bossa amb 3 boles roges i 2 de blaves, sense reemplaçament:",
    r"En las experiencias dependientes, la probabilidad de la segunda etapa depende de lo que ha pasado en la primera. La probabilidad de que ocurra \(B\) <strong>sabiendo que</strong> ya ha ocurrido \(A\) se llama <strong>probabilidad de \(B\) condicionada a \(A\)</strong> y se escribe \(P(B/A)\). En la bolsa con 3 bolas rojas y 2 azules, sin reemplazamiento:",
    r"In dependent experiments, the probability in the second stage depends on what happened in the first. The probability that \(B\) happens <strong>given that</strong> \(A\) has already happened is called the <strong>conditional probability of \(B\) given \(A\)</strong> and is written \(P(B/A)\) (also \(P(B\mid A)\)). In the bag with 3 red and 2 blue balls, without replacement:")
  + D(r"P(R_2/R_1)=\frac24=\frac12\qquad P(R_2/B_1)=\frac34")
  + P(r"(\(R_1\) = «la primera és roja», \(R_2\) = «la segona és roja»). Són les probabilitats que escrivim en les branques de la segona etapa de l'arbre. Per això, la probabilitat d'un camí és:",
      r"(\(R_1\) = «la primera es roja», \(R_2\) = «la segunda es roja»). Son las probabilidades que escribimos en las ramas de la segunda etapa del árbol. Por eso, la probabilidad de un camino es:",
      r"(\(R_1\) = “the first is red”, \(R_2\) = “the second is red”). These are the probabilities we write on the second-stage branches of the tree. That's why the probability of a path is:")
  + D(r"P(A\cap B)=P(A)\cdot P(B/A)\qquad\quad P(R_1\cap R_2)=\frac35\cdot\frac24=\frac3{10}")
  + ul(L(r"Si \(A\) i \(B\) són <strong>independents</strong>, saber que ha passat \(A\) no canvia res: \(P(B/A)=P(B)\), i la fórmula queda \(P(A\cap B)=P(A)\cdot P(B)\) (apartat 11.5).", r"Si \(A\) y \(B\) son <strong>independientes</strong>, saber que ha pasado \(A\) no cambia nada: \(P(B/A)=P(B)\), y la fórmula queda \(P(A\cap B)=P(A)\cdot P(B)\) (apartado 11.5).", r"If \(A\) and \(B\) are <strong>independent</strong>, knowing that \(A\) happened changes nothing: \(P(B/A)=P(B)\), and the formula becomes \(P(A\cap B)=P(A)\cdot P(B)\) (section 11.5)."),
       L(r"Si són <strong>dependents</strong>, \(P(B/A)\neq P(B)\): amb reemplaçament, \(P(R_2/R_1)=\frac35\); sense reemplaçament, \(\frac24\).", r"Si son <strong>dependientes</strong>, \(P(B/A)\neq P(B)\): con reemplazamiento, \(P(R_2/R_1)=\frac35\); sin reemplazamiento, \(\frac24\).", r"If they are <strong>dependent</strong>, \(P(B/A)\neq P(B)\): with replacement, \(P(R_2/R_1)=\frac35\); without replacement, \(\frac24\)."))
  + note(r"Per a calcular \(P(B/A)\) amb la llei de Laplace, imagina la situació <strong>després</strong> d'haver passat \(A\): quins casos queden possibles i quins són favorables a \(B\)? Si traiem dues cartes d'una baralla espanyola sense reemplaçament i la primera és un as, queden 3 asos entre 39 cartes: \(P(\text{%s})=\frac3{39}=\frac1{13}\)." % Lt('as / as', 'as / as', 'ace / ace'),
         r"Para calcular \(P(B/A)\) con la ley de Laplace, imagina la situación <strong>después</strong> de haber pasado \(A\): ¿qué casos quedan posibles y cuáles son favorables a \(B\)? Si sacamos dos cartas de una baraja española sin reemplazamiento y la primera es un as, quedan 3 ases entre 39 cartas: \(P(\text{%s})=\frac3{39}=\frac1{13}\)." % Lt('as / as', 'as / as', 'ace / ace'),
         r"To find \(P(B/A)\) with Laplace's rule, picture the situation <strong>after</strong> \(A\) has happened: which outcomes are still possible and which are favourable to \(B\)? If we draw two cards from a Spanish pack without replacement and the first is an ace, 3 aces are left among 39 cards: \(P(\text{%s})=\frac3{39}=\frac1{13}\)." % Lt('as / as', 'as / as', 'ace / ace'))
  + drill('dep', 'Entrena: experiències dependents', 'Entrena: experiencias dependientes', 'Train: dependent experiments'))
ck(Fr(2, 4), Fr(1, 2)); ck(Fr(3, 5) * Fr(2, 4), Fr(3, 10)); ck(Fr(3, 39), Fr(1, 13))

UT = ptree([('C', '1/2', [('R|ball-r', '2/5', [], 'C, R: 1/2 · 2/5 = 1/5'), ('B|ball-b', '3/5', [], 'C, B: 3/10')]), ('X', '1/2', [('R|ball-r', '4/5', [], 'X, R: 1/2 · 4/5 = 2/5'), ('B|ball-b', '1/5', [], 'X, B: 1/10')])], W=330, rowh=36)
URN = Fr(1, 2) * Fr(2, 5) + Fr(1, 2) * Fr(4, 5)
assert URN == Fr(3, 5)
s6 += box('prop', L('Sumar camins: la probabilitat total', 'Sumar caminos: la probabilidad total', 'Adding paths: total probability'),
  P(r"De vegades la primera etapa decideix <strong>com</strong> es fa la segona. Tenim dues urnes: la urna I té 2 boles roges i 3 de blaves, i la urna II, 4 de roges i 1 de blava. Llancem una moneda: si ix cara traiem una bola de la urna I, i si ix creu, de la urna II. Les branques de la segona etapa són probabilitats condicionades (per exemple, \(P(R/\text{I})=\frac25\)):",
    r"A veces la primera etapa decide <strong>cómo</strong> se hace la segunda. Tenemos dos urnas: la urna I tiene 2 bolas rojas y 3 azules, y la urna II, 4 rojas y 1 azul. Lanzamos una moneda: si sale cara sacamos una bola de la urna I, y si sale cruz, de la urna II. Las ramas de la segunda etapa son probabilidades condicionadas (por ejemplo, \(P(R/\text{I})=\frac25\)):",
    r"Sometimes the first stage decides <strong>how</strong> the second is carried out. We have two urns: urn I has 2 red and 3 blue balls, and urn II, 4 red and 1 blue. We toss a coin: heads, we draw from urn I; tails, from urn II. The second-stage branches are conditional probabilities (for example, \(P(R/\text{I})=\frac25\)):")
  + figs(UT)
  + P(r"Hi ha dos camins que acaben en roja: n'hi ha prou de sumar-los.", r"Hay dos caminos que acaban en roja: basta con sumarlos.", r"Two paths end in red: just add them.")
  + D(r"P(R)=P(\text{I})\cdot P(R/\text{I})+P(\text{II})\cdot P(R/\text{II})=\frac12\cdot\frac25+\frac12\cdot\frac45=\frac15+\frac25=\frac35")
  + widget('w-urn', '🏺', L('Dues urnes', 'Dos urnas', 'Two urns'),
           ['<div class="wrow">' + rng('r1', 0, 8, 1, 2, 'R I') + rng('b1', 0, 8, 1, 3, 'B I') + '</div>',
            '<div class="wrow">' + rng('r2', 0, 8, 1, 4, 'R II') + rng('b2', 0, 8, 1, 1, 'B II') + '</div>',
            '<div class="wrow"><div class="seg sg-s" role="group"></div></div>',
            '<div class="wrow"><div class="seg sg-e" role="group"></div></div>'])
  + drill('urn', 'Entrena: dues urnes', 'Entrena: dos urnas', 'Train: two urns'))

# problema de l'examen: 60 % aproven mates; dels que aproven mates, el 75 % aproven física; dels que no, el 25 %
pm, pfm, pfn = Fr(6, 10), Fr(75, 100), Fr(25, 100)
assert pm * pfm == Fr(45, 100) and pm * pfm + (1 - pm) * pfn == Fr(55, 100) and (1 - pm) * (1 - pfn) == Fr(30, 100)
TMF = ptree([('M', '0,6', [('F', '0,75', [], 'M∩F: 0,45'), ('F̄', '0,25', [], '0,15')]), ('M̄', '0,4', [('F', '0,25', [], 'M̄∩F: 0,1'), ('F̄', '0,75', [], '0,3')])], W=380)
assert Fr(4, 6) * Fr(3, 5) * Fr(2, 4) == Fr(1, 5) and Fr(3, 5) * Fr(2, 4) + Fr(2, 5) * Fr(3, 4) == Fr(3, 5)
s6 += levels(
 [prob(L(r"En una bossa hi ha 4 boles roges i 6 de blaves. En traiem dues <strong>amb reemplaçament</strong>. Calcula la probabilitat que les dues siguen roges i que n'isca una de cada color.",
         r"En una bolsa hay 4 bolas rojas y 6 azules. Sacamos dos <strong>con reemplazamiento</strong>. Calcula la probabilidad de que las dos sean rojas y de que salga una de cada color.",
         r"A bag has 4 red balls and 6 blue ones. We draw two <strong>with replacement</strong>. Find the probability that both are red and that we get one of each colour."),
       figs(btree(4, 6, True)),
       D(r"P(RR)=\frac4{10}\cdot\frac4{10}=\frac{16}{100}=\boxed{\frac4{25}}"),
       D(r"P(\text{%s})=P(RB)+P(BR)=\frac{24}{100}+\frac{24}{100}=\frac{48}{100}=\boxed{\frac{12}{25}}" % Lt('una de cada', 'una de cada', 'one of each'))),
  prob(L(r"Fes el mateix problema <strong>sense reemplaçament</strong> i calcula també la probabilitat que les dues siguen blaves. Comprova que les tres probabilitats sumen 1.",
         r"Haz el mismo problema <strong>sin reemplazamiento</strong> y calcula también la probabilidad de que las dos sean azules. Comprueba que las tres probabilidades suman 1.",
         r"Do the same problem <strong>without replacement</strong> and also find the probability that both are blue. Check that the three probabilities add up to 1."),
       figs(btree(4, 6, False)),
       D(r"P(RR)=\frac4{10}\cdot\frac39=\frac{12}{90}=\boxed{\frac2{15}}\qquad P(BB)=\frac6{10}\cdot\frac59=\frac{30}{90}=\boxed{\frac13}"),
       D(r"P(\text{%s})=\frac4{10}\cdot\frac69+\frac6{10}\cdot\frac49=\frac{48}{90}=\boxed{\frac8{15}}" % Lt('una de cada', 'una de cada', 'one of each')),
       P(r"Comprovació: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)", r"Comprobación: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)", r"Check: \(\frac{12}{90}+\frac{48}{90}+\frac{30}{90}=\frac{90}{90}=1\ \checkmark\)"))],
 [prob(L(r"Traiem dues cartes d'una baralla espanyola sense tornar la primera. Quina és la probabilitat que totes dues siguen d'oros?", r"Sacamos dos cartas de una baraja española sin devolver la primera. ¿Cuál es la probabilidad de que las dos sean de oros?", r"We draw two cards from a Spanish pack without putting the first back. What is the probability that both are coins?"),
       P(r"Després de traure un oro, queden 9 oros entre 39 cartes:", r"Después de sacar un oro, quedan 9 oros entre 39 cartas:", r"After drawing a coins card, 9 coins are left among 39 cards:"),
       D(r"P(OO)=\frac{10}{40}\cdot\frac9{39}=\frac{90}{1560}=\boxed{\frac3{52}}\approx0{,}06")),
  prob(L(r"En un grup, el 60 % de l'alumnat aprova Matemàtiques. Dels que aproven Matemàtiques, el 75 % aprova Física, i dels que no aproven Matemàtiques, només el 25 %. Fes el diagrama d'arbre i calcula la probabilitat que un alumne triat a l'atzar aprove les dues assignatures i la probabilitat que aprove Física.",
         r"En un grupo, el 60 % del alumnado aprueba Matemáticas. De los que aprueban Matemáticas, el 75 % aprueba Física, y de los que no aprueban Matemáticas, solo el 25 %. Haz el diagrama de árbol y calcula la probabilidad de que un alumno elegido al azar apruebe las dos asignaturas y la probabilidad de que apruebe Física.",
         r"In a class, 60 % of the students pass Maths. Of those who pass Maths, 75 % pass Physics, and of those who don't pass Maths, only 25 %. Draw the tree diagram and find the probability that a student picked at random passes both subjects and the probability that they pass Physics."),
       P(r"\(M\) = «aprova Matemàtiques», \(F\) = «aprova Física». Les dades del 75 % i el 25 % són probabilitats condicionades: \(P(F/M)=0{,}75\) i \(P(F/\overline{M})=0{,}25\).",
         r"\(M\) = «aprueba Matemáticas», \(F\) = «aprueba Física». Los datos del 75 % y el 25 % son probabilidades condicionadas: \(P(F/M)=0{,}75\) y \(P(F/\overline{M})=0{,}25\).",
         r"\(M\) = “passes Maths”, \(F\) = “passes Physics”. The 75 % and 25 % figures are conditional probabilities: \(P(F/M)=0.75\) and \(P(F/\overline{M})=0.25\).") + figs(TMF),
       D(r"P(M\cap F)=P(M)\cdot P(F/M)=0{,}6\cdot0{,}75=\boxed{0{,}45}"),
       D(r"P(F)=0{,}6\cdot0{,}75+0{,}4\cdot0{,}25=0{,}45+0{,}1=\boxed{0{,}55}"))],
 [prob(L(r"La urna I té 3 boles roges i 1 de blava; la urna II té 1 bola roja i 3 de blaves. Llancem un dau: si ix 1 o 2 traiem una bola de la urna I, i si no, de la urna II. Calcula la probabilitat que la bola siga roja i la probabilitat que siga de la urna I i roja.",
         r"La urna I tiene 3 bolas rojas y 1 azul; la urna II tiene 1 bola roja y 3 azules. Lanzamos un dado: si sale 1 o 2 sacamos una bola de la urna I, y si no, de la urna II. Calcula la probabilidad de que la bola sea roja y la probabilidad de que sea de la urna I y roja.",
         r"Urn I has 3 red balls and 1 blue; urn II has 1 red ball and 3 blue. We roll a die: 1 or 2, we draw from urn I; otherwise, from urn II. Find the probability that the ball is red and the probability that it's from urn I and red."),
       P(r"\(P(\text{I})=\frac26=\frac13\) i \(P(\text{II})=\frac23\). Fem l'arbre:", r"\(P(\text{I})=\frac26=\frac13\) y \(P(\text{II})=\frac23\). Hacemos el árbol:", r"\(P(\text{I})=\frac26=\frac13\) and \(P(\text{II})=\frac23\). Draw the tree:")
       + figs(ptree([('I', '1/3', [('R|ball-r', '3/4', [], 'I, R: 1/3 · 3/4 = 1/4'), ('B|ball-b', '1/4', [], 'I, B: 1/12')]), ('II', '2/3', [('R|ball-r', '1/4', [], 'II, R: 2/3 · 1/4 = 1/6'), ('B|ball-b', '3/4', [], 'II, B: 1/2')])], W=340, rowh=36)),
       D(r"P(\text{I}\cap R)=\frac13\cdot\frac34=\boxed{\frac14}\qquad P(R)=\frac14+\frac23\cdot\frac14=\frac14+\frac16=\boxed{\frac5{12}}")),
  prob(L(r"En una bossa hi ha 4 boles roges i 2 de blaves. a) En traiem tres sense reemplaçament: quina és la probabilitat que les tres siguen roges? b) Si en traiem dues sense reemplaçament, quina és la probabilitat que la <strong>segona</strong> siga roja?",
         r"En una bolsa hay 4 bolas rojas y 2 azules. a) Sacamos tres sin reemplazamiento: ¿cuál es la probabilidad de que las tres sean rojas? b) Si sacamos dos sin reemplazamiento, ¿cuál es la probabilidad de que la <strong>segunda</strong> sea roja?",
         r"A bag has 4 red balls and 2 blue ones. a) We draw three without replacement: what is the probability that all three are red? b) If we draw two without replacement, what is the probability that the <strong>second</strong> one is red?"),
       P(r"a) Després de cada roja queda una roja menys i una bola menys:", r"a) Después de cada roja queda una roja menos y una bola menos:", r"a) After each red there's one red fewer and one ball fewer:"),
       D(r"P(R_1\cap R_2\cap R_3)=\frac46\cdot\frac35\cdot\frac24=\frac{24}{120}=\boxed{\frac15}"),
       P(r"b) La segona pot ser roja per dos camins: \(RR\) i \(BR\). En sumem les probabilitats:", r"b) La segunda puede ser roja por dos caminos: \(RR\) y \(AR\). Sumamos sus probabilidades:", r"b) The second can be red along two paths: \(RR\) and \(BR\). Add their probabilities:"),
       D(r"P(R_2)=\frac46\cdot\frac35+\frac26\cdot\frac45=\frac{12}{30}+\frac{8}{30}=\frac{20}{30}=\boxed{\frac23}"),
       note(r"És la mateixa probabilitat que la de la primera bola, \(\frac46=\frac23\). Si no sabem què ha eixit abans, totes les extraccions tenen la mateixa probabilitat de ser roges.",
            r"Es la misma probabilidad que la de la primera bola, \(\frac46=\frac23\). Si no sabemos qué ha salido antes, todas las extracciones tienen la misma probabilidad de ser rojas.",
            r"It's the same as the probability for the first ball, \(\frac46=\frac23\). If we don't know what came out before, every draw has the same probability of being red."))])
assert Fr(1, 3) * Fr(3, 4) == Fr(1, 4) and Fr(1, 4) + Fr(2, 3) * Fr(1, 4) == Fr(5, 12)
assert Fr(4, 6) * Fr(3, 5) + Fr(2, 6) * Fr(4, 5) == Fr(2, 3) and Fr(10, 40) * Fr(9, 39) == Fr(3, 52)
assert pp(4, 6, True, lambda s: s == 'RR') == Fr(4, 25) and pp(4, 6, True, lambda s: s in ('RB', 'BR')) == Fr(12, 25)
assert pp(4, 6, False, lambda s: s == 'RR') == Fr(2, 15) and pp(4, 6, False, lambda s: s in ('RB', 'BR')) == Fr(8, 15) and pp(4, 6, False, lambda s: s == 'BB') == Fr(1, 3)
s6 += practice([
  ('★', L(r"a) En una bossa hi ha 2 boles blanques i 3 de negres. En traiem dues amb reemplaçament. Quina és la probabilitat que les dues siguen negres?", r"a) En una bolsa hay 2 bolas blancas y 3 negras. Sacamos dos con reemplazamiento. ¿Cuál es la probabilidad de que las dos sean negras?", r"a) A bag has 2 white balls and 3 black ones. We draw two with replacement. What is the probability that both are black?")),
  ('★★', L(r"b) Repeteix-ho sense reemplaçament. c) Traiem dues cartes d'una baralla espanyola sense reemplaçament. Quina és la probabilitat que cap no siga un as?", r"b) Repítelo sin reemplazamiento. c) Sacamos dos cartas de una baraja española sin reemplazamiento. ¿Cuál es la probabilidad de que ninguna sea un as?", r"b) Do it again without replacement. c) We draw two cards from a Spanish pack without replacement. What is the probability that neither is an ace?")),
  ('★★★', L(r"d) En una caixa hi ha 5 bombetes i 2 són defectuoses. En provem dues a l'atzar (sense reemplaçament). Quina és la probabilitat que almenys una siga defectuosa?", r"d) En una caja hay 5 bombillas y 2 son defectuosas. Probamos dos al azar (sin reemplazamiento). ¿Cuál es la probabilidad de que al menos una sea defectuosa?", r"d) A box has 5 light bulbs and 2 are faulty. We test two at random (without replacement). What is the probability that at least one is faulty?"))],
  P(r"a) \(\frac35\cdot\frac35=\frac9{25}\). b) \(\frac35\cdot\frac24=\frac3{10}\). c) \(\frac{36}{40}\cdot\frac{35}{39}=\frac{21}{26}\approx0{,}81\). d) Contrari: cap defectuosa, \(\frac35\cdot\frac24=\frac3{10}\); \(P=1-\frac3{10}=\frac7{10}\).",
    r"a) \(\frac35\cdot\frac35=\frac9{25}\). b) \(\frac35\cdot\frac24=\frac3{10}\). c) \(\frac{36}{40}\cdot\frac{35}{39}=\frac{21}{26}\approx0{,}81\). d) Contrario: ninguna defectuosa, \(\frac35\cdot\frac24=\frac3{10}\); \(P=1-\frac3{10}=\frac7{10}\).",
    r"a) \(\frac35\cdot\frac35=\frac9{25}\). b) \(\frac35\cdot\frac24=\frac3{10}\). c) \(\frac{36}{40}\cdot\frac{35}{39}=\frac{21}{26}\approx0.81\). d) Complement: none faulty, \(\frac35\cdot\frac24=\frac3{10}\); \(P=1-\frac3{10}=\frac7{10}\)."))
assert Fr(36, 40) * Fr(35, 39) == Fr(21, 26) and 1 - Fr(3, 5) * Fr(2, 4) == Fr(7, 10); ck(Fr(21, 26), '0,81', 2)
