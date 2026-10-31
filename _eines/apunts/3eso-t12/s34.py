# 12.3 Probabilitat d'un esdeveniment. Propietats · 12.4 Experiments regulars. Llei de Laplace
from comu import *

# =====================================================================
# 12.3 Probabilitat d'un esdeveniment
# =====================================================================
FD = [8, 11, 9, 12, 10, 10]; N_ = sum(FD)
assert N_ == 60
HD = [Fr(f, N_) for f in FD]
assert sum(HD) == 1
s3 = box('def', L('Freqüència absoluta i freqüència relativa', 'Frecuencia absoluta y frecuencia relativa', 'Absolute and relative frequency'),
  P(r"Si repetim un experiment aleatori \(n\) vegades i un esdeveniment \(A\) ocorre \(f\) vegades, \(f\) és la <strong>freqüència absoluta</strong> d'\(A\) i",
    r"Si repetimos un experimento aleatorio \(n\) veces y un suceso \(A\) ocurre \(f\) veces, \(f\) es la <strong>frecuencia absoluta</strong> de \(A\) y",
    r"If we repeat a random experiment \(n\) times and an event \(A\) happens \(f\) times, \(f\) is the <strong>absolute frequency</strong> of \(A\) and")
  + D(r"h(A)=\frac{f}{n}=\frac{%s}{%s}" % (Lt('vegades que ocorre A', 'veces que ocurre A', 'times A happens'), Lt('vegades que repetim', 'veces que repetimos', 'number of trials')))
  + P(r"és la seua <strong>freqüència relativa</strong>. És un nombre entre 0 i 1, i les freqüències relatives de tots els resultats sumen 1. Per exemple, hem llançat un dau 60 vegades:",
      r"es su <strong>frecuencia relativa</strong>. Es un número entre 0 y 1, y las frecuencias relativas de todos los resultados suman 1. Por ejemplo, hemos lanzado un dado 60 veces:",
      r"is its <strong>relative frequency</strong>. It's a number between 0 and 1, and the relative frequencies of all outcomes add up to 1. For example, we've rolled a die 60 times:")
  + tbl([L('Resultat', 'Resultado', 'Outcome')] + [str(i) for i in range(1, 7)] + ['Total'],
        [[L(r'Freq. absoluta \(f\)', r'Frec. absoluta \(f\)', r'Abs. frequency \(f\)')] + [str(f) for f in FD] + ['60'],
         [L(r'Freq. relativa \(h\)', r'Frec. relativa \(h\)', r'Rel. frequency \(h\)')] + [r'\(\frac{%d}{60}\)' % f for f in FD] + ['1'],
         [L('En decimal', 'En decimal', 'As a decimal')] + [r'\(%s\)' % dc(h) for h in HD] + ['1']], cls='narrow')
  + P(r"La freqüència relativa de «traure parell» és \(\frac{11+12+10}{60}=\frac{33}{60}=0{,}55\).",
      r"La frecuencia relativa de «sacar par» es \(\frac{11+12+10}{60}=\frac{33}{60}=0{,}55\).",
      r"The relative frequency of “even” is \(\frac{11+12+10}{60}=\frac{33}{60}=0.55\)."))
ck(Fr(11 + 12 + 10, 60), '0,55'); ck(HD[0], '0,13', 2); ck(HD[1], '0,18', 2); ck(HD[2], '0,15', 2); ck(HD[3], '0,20', 2); ck(HD[4], '0,17', 2)

SCALE = ('<div class="pscale"><div class="bar"></div><div class="ticks">'
         + ''.join(f'<span style="left:{p}%"><b>{v}</b>{t}</span>' for p, v, t in [
             (0, '0', L('impossible', 'imposible', 'impossible')), (25, '0,25', L('poc probable', 'poco probable', 'unlikely')),
             (50, '0,5', L('tan probable com no', 'tan probable como no', 'even chance')), (75, '0,75', L('molt probable', 'muy probable', 'likely')), (100, '1', L('segur', 'seguro', 'certain'))])
         + '</div></div>')
s3 += box('def', L("Probabilitat d'un esdeveniment", 'Probabilidad de un suceso', 'Probability of an event'),
  P(r"La <strong>probabilitat</strong> d'un esdeveniment \(A\), \(P(A)\), és un nombre entre 0 i 1 que mesura com d'esperable és que ocórrega: com més a prop d'1, més fàcil és que ocórrega. Es pot escriure com a fracció, com a decimal o com a percentatge: \(P(A)=\frac14=0{,}25=25\,\%\).",
    r"La <strong>probabilidad</strong> de un suceso \(A\), \(P(A)\), es un número entre 0 y 1 que mide lo esperable que es que ocurra: cuanto más cerca de 1, más fácil es que ocurra. Se puede escribir como fracción, como decimal o como porcentaje: \(P(A)=\frac14=0{,}25=25\,\%\).",
    r"The <strong>probability</strong> of an event \(A\), \(P(A)\), is a number between 0 and 1 that measures how likely \(A\) is to happen: the closer to 1, the more likely. It can be written as a fraction, a decimal or a percentage: \(P(A)=\frac14=0.25=25\,\%\).")
  + SCALE
  + P(r"Com la calculem? Si el experiment és <strong>regular</strong> (tots els resultats tenen la mateixa possibilitat), amb la llei de Laplace (apartat 12.4). Si no, l'estimem amb la freqüència relativa d'un nombre gran de repeticions (apartat 12.5).",
      r"¿Cómo la calculamos? Si el experimento es <strong>regular</strong> (todos los resultados tienen la misma posibilidad), con la ley de Laplace (apartado 12.4). Si no, la estimamos con la frecuencia relativa de un número grande de repeticiones (apartado 12.5).",
      r"How do we work it out? If the experiment is <strong>regular</strong> (all outcomes are equally likely), with Laplace's rule (section 12.4). If not, we estimate it with the relative frequency over a large number of trials (section 12.5)."))

s3 += box('prop', L('Propietats de la probabilitat', 'Propiedades de la probabilidad', 'Properties of probability'),
  ol(L(r"Per a qualsevol esdeveniment, \(0\le P(A)\le1\).", r"Para cualquier suceso, \(0\le P(A)\le1\).", r"For any event, \(0\le P(A)\le1\)."),
     L(r"\(P(E)=1\) (esdeveniment segur) i \(P(\varnothing)=0\) (esdeveniment impossible).", r"\(P(E)=1\) (suceso seguro) y \(P(\varnothing)=0\) (suceso imposible).", r"\(P(E)=1\) (certain event) and \(P(\varnothing)=0\) (impossible event)."),
     L(r"Les probabilitats de tots els resultats elementals sumen 1.", r"Las probabilidades de todos los resultados elementales suman 1.", r"The probabilities of all the elementary outcomes add up to 1."),
     L(r"<strong>Esdeveniment contrari:</strong> \(P(\overline{A})=1-P(A)\).", r"<strong>Suceso contrario:</strong> \(P(\overline{A})=1-P(A)\).", r"<strong>Complementary event:</strong> \(P(\overline{A})=1-P(A)\)."),
     L(r"Si \(A\) i \(B\) són <strong>incompatibles</strong>: \(P(A\cup B)=P(A)+P(B)\).", r"Si \(A\) y \(B\) son <strong>incompatibles</strong>: \(P(A\cup B)=P(A)+P(B)\).", r"If \(A\) and \(B\) are <strong>mutually exclusive</strong>: \(P(A\cup B)=P(A)+P(B)\)."),
     L(r"En general (compatibles o no): \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\). Restem la intersecció perquè l'hem sumada dues vegades.", r"En general (compatibles o no): \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\). Restamos la intersección porque la hemos sumado dos veces.", r"In general (exclusive or not): \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\). We subtract the intersection because it has been added twice."))
  + note(r"La propietat del contrari és molt útil: de vegades és més fàcil calcular la probabilitat que <strong>no</strong> ocórrega una cosa i restar-la d'1.",
         r"La propiedad del contrario es muy útil: a veces es más fácil calcular la probabilidad de que algo <strong>no</strong> ocurra y restarla de 1.",
         r"The complement rule is very handy: sometimes it's easier to work out the probability that something does <strong>not</strong> happen and subtract it from 1.")
  + widget('w-prop', '⚖️', L('Probabilitats de dos esdeveniments', 'Probabilidades de dos sucesos', 'Probabilities of two events'),
           ['<div class="wrow">' + rng('a', 0, 1, 0.05, 0.5, 'P(A)') + rng('b', 0, 1, 0.05, 0.4, 'P(B)') + rng('c', 0, 1, 0.05, 0.2, 'P(A∩B)') + '</div>',
            quick([('0.5|0.4|0.2', 'P(A)=0,5 · P(B)=0,4 · P(A∩B)=0,2'), ('0.3|0.45|0', L('incompatibles', 'incompatibles', 'mutually exclusive')), ('0.6|0.3|0.3', 'B ⊂ A'), ('0.7|0.6|0.1', L('impossible?', '¿imposible?', 'impossible?'))])])
  + drill('prop', 'Entrena: propietats de la probabilitat', 'Entrena: propiedades de la probabilidad', 'Train: properties of probability'))

PT = [Fr(1, 10), Fr(2, 10), Fr(1, 10), Fr(2, 10), Fr(1, 10)]; P6 = 1 - sum(PT)
assert P6 == Fr(3, 10) and PT[1] + PT[3] + P6 == Fr(7, 10)
pa, pb, pab = Fr(1, 2), Fr(2, 5), Fr(1, 5)
assert pa + pb - pab == Fr(7, 10) and 1 - (pa + pb - pab) == Fr(3, 10)
pf, pbq, pfb = Fr(30, 100), Fr(20, 100), Fr(8, 100)
assert pf + pbq - pfb == Fr(42, 100) and 1 - Fr(42, 100) == Fr(58, 100) and pf - pfb == Fr(22, 100)
pu, pa3, pb3 = Fr(8, 10), Fr(5, 10), Fr(45, 100)
assert pa3 + pb3 - pu == Fr(15, 100) and pa3 - Fr(15, 100) == Fr(35, 100)
s3 += levels(
 [prob(L(r"La probabilitat que demà ploga és 0,35. Quina és la probabilitat que no ploga?", r"La probabilidad de que mañana llueva es 0,35. ¿Cuál es la probabilidad de que no llueva?", r"The probability that it will rain tomorrow is 0.35. What is the probability that it won't?"),
       D(r"P(\overline{A})=1-P(A)=1-0{,}35=\boxed{0{,}65}")),
  prob(L(r"Un dau està trucat. Les probabilitats dels resultats de l'1 al 5 són 0,1, 0,2, 0,1, 0,2 i 0,1. Calcula la probabilitat de traure un 6 i la de traure parell.",
         r"Un dado está trucado. Las probabilidades de los resultados del 1 al 5 son 0,1, 0,2, 0,1, 0,2 y 0,1. Calcula la probabilidad de sacar un 6 y la de sacar par.",
         r"A die is loaded. The probabilities of the outcomes 1 to 5 are 0.1, 0.2, 0.1, 0.2 and 0.1. Find the probability of rolling a 6 and of rolling an even number."),
       P(r"Les sis probabilitats han de sumar 1:", r"Las seis probabilidades deben sumar 1:", r"The six probabilities must add up to 1:"),
       D(r"P(6)=1-(0{,}1+0{,}2+0{,}1+0{,}2+0{,}1)=1-0{,}7=\boxed{0{,}3}"),
       D(r"P(\text{%s})=P(2)+P(4)+P(6)=0{,}2+0{,}2+0{,}3=\boxed{0{,}7}" % Lt('parell', 'par', 'even')))],
 [prob(L(r"Siguen \(A\) i \(B\) dos esdeveniments amb \(P(A)=0{,}5\), \(P(B)=0{,}4\) i \(P(A\cap B)=0{,}2\). Calcula \(P(A\cup B)\) i la probabilitat que no ocórrega cap dels dos.",
         r"Sean \(A\) y \(B\) dos sucesos con \(P(A)=0{,}5\), \(P(B)=0{,}4\) y \(P(A\cap B)=0{,}2\). Calcula \(P(A\cup B)\) y la probabilidad de que no ocurra ninguno de los dos.",
         r"Let \(A\) and \(B\) be two events with \(P(A)=0.5\), \(P(B)=0.4\) and \(P(A\cap B)=0.2\). Find \(P(A\cup B)\) and the probability that neither happens."),
       D(r"P(A\cup B)=0{,}5+0{,}4-0{,}2=\boxed{0{,}7}"),
       P(r"«No ocorre cap dels dos» és el contrari d'«ocorre algun dels dos» (\(A\cup B\)):", r"«No ocurre ninguno de los dos» es el contrario de «ocurre alguno de los dos» (\(A\cup B\)):", r"“Neither happens” is the complement of “at least one happens” (\(A\cup B\)):"),
       D(r"P(\overline{A\cup B})=1-0{,}7=\boxed{0{,}3}")),
  prob(L(r"En un institut, el 30 % de l'alumnat juga a futbol, el 20 % a bàsquet i el 8 % a tots dos esports. Triem un alumne a l'atzar. Quina és la probabilitat que jugue a algun d'aquests esports? I que no en jugue a cap?",
         r"En un instituto, el 30 % del alumnado juega a fútbol, el 20 % a baloncesto y el 8 % a los dos deportes. Elegimos un alumno al azar. ¿Cuál es la probabilidad de que juegue a alguno de estos deportes? ¿Y de que no juegue a ninguno?",
         r"In a school, 30 % of the students play football, 20 % play basketball and 8 % play both. We pick a student at random. What is the probability that they play at least one of these sports? And neither?"),
       D(r"P(F\cup B)=0{,}30+0{,}20-0{,}08=\boxed{0{,}42}\qquad P(\overline{F\cup B})=1-0{,}42=\boxed{0{,}58}"),
       note(r"Si sumàrem directament 30 % + 20 %, l'alumnat que juga als dos esports (8 %) estaria comptat dues vegades.", r"Si sumáramos directamente 30 % + 20 %, el alumnado que juega a los dos deportes (8 %) estaría contado dos veces.", r"If we just added 30 % + 20 %, the students who play both sports (8 %) would be counted twice.", '⚠️'))],
 [prob(L(r"Sabem que \(P(A)=0{,}5\), \(P(B)=0{,}45\) i \(P(A\cup B)=0{,}8\). Calcula \(P(A\cap B)\). Són incompatibles? Quina és la probabilitat que ocórrega \(A\) però no \(B\)?",
         r"Sabemos que \(P(A)=0{,}5\), \(P(B)=0{,}45\) y \(P(A\cup B)=0{,}8\). Calcula \(P(A\cap B)\). ¿Son incompatibles? ¿Cuál es la probabilidad de que ocurra \(A\) pero no \(B\)?",
         r"We know that \(P(A)=0.5\), \(P(B)=0.45\) and \(P(A\cup B)=0.8\). Find \(P(A\cap B)\). Are they mutually exclusive? What is the probability that \(A\) happens but \(B\) doesn't?"),
       P(r"Aïllem la intersecció de la fórmula de la unió:", r"Despejamos la intersección de la fórmula de la unión:", r"Solve the union formula for the intersection:"),
       D(r"0{,}8=0{,}5+0{,}45-P(A\cap B)\ \Rightarrow\ P(A\cap B)=0{,}95-0{,}8=\boxed{0{,}15}"),
       P(r"Com que \(P(A\cap B)\neq0\), <strong>no</strong> són incompatibles. «\(A\) però no \(B\)» és la part d'\(A\) que no és en \(B\):", r"Como \(P(A\cap B)\neq0\), <strong>no</strong> son incompatibles. «\(A\) pero no \(B\)» es la parte de \(A\) que no está en \(B\):", r"Since \(P(A\cap B)\neq0\), they are <strong>not</strong> mutually exclusive. “\(A\) but not \(B\)” is the part of \(A\) outside \(B\):"),
       D(r"P(A\cap\overline{B})=P(A)-P(A\cap B)=0{,}5-0{,}15=\boxed{0{,}35}"))])
s3 += practice([
  ('★', L(r"a) Si \(P(A)=\frac38\), quant val \(P(\overline{A})\)? b) Pot ser que \(P(A)=1{,}2\)? I que \(P(A)=-0{,}3\)?", r"a) Si \(P(A)=\frac38\), ¿cuánto vale \(P(\overline{A})\)? b) ¿Puede ser que \(P(A)=1{,}2\)? ¿Y que \(P(A)=-0{,}3\)?", r"a) If \(P(A)=\frac38\), what is \(P(\overline{A})\)? b) Can \(P(A)=1.2\)? What about \(P(A)=-0.3\)?")),
  ('★★', L(r"c) \(A\) i \(B\) són incompatibles, amb \(P(A)=0{,}25\) i \(P(B)=0{,}6\). Calcula \(P(A\cup B)\) i \(P(\overline{A\cup B})\). d) En una ruleta, \(P(\text{roig})=0{,}45\), \(P(\text{negre})=0{,}45\) i la resta és verd. Quant val \(P(\text{verd})\)?", r"c) \(A\) y \(B\) son incompatibles, con \(P(A)=0{,}25\) y \(P(B)=0{,}6\). Calcula \(P(A\cup B)\) y \(P(\overline{A\cup B})\). d) En una ruleta, \(P(\text{rojo})=0{,}45\), \(P(\text{negro})=0{,}45\) y el resto es verde. ¿Cuánto vale \(P(\text{verde})\)?", r"c) \(A\) and \(B\) are mutually exclusive, with \(P(A)=0.25\) and \(P(B)=0.6\). Find \(P(A\cup B)\) and \(P(\overline{A\cup B})\). d) On a roulette wheel, \(P(\text{red})=0.45\), \(P(\text{black})=0.45\) and the rest is green. What is \(P(\text{green})\)?")),
  ('★★★', L(r"e) El 60 % de les famílies d'un poble té gos, el 35 % té gat i el 25 % no té cap dels dos. Quin percentatge té gos i gat?", r"e) El 60 % de las familias de un pueblo tiene perro, el 35 % tiene gato y el 25 % no tiene ninguno de los dos. ¿Qué porcentaje tiene perro y gato?", r"e) 60 % of the families in a village have a dog, 35 % have a cat and 25 % have neither. What percentage have both a dog and a cat?"))],
  P(r"a) \(\frac58\). b) No: una probabilitat sempre està entre 0 i 1. c) \(0{,}85\) i \(0{,}15\). d) \(1-0{,}9=0{,}1\). e) \(P(G\cup T)=1-0{,}25=0{,}75\); \(P(G\cap T)=0{,}60+0{,}35-0{,}75=0{,}20\): el <strong>20 %</strong>.",
    r"a) \(\frac58\). b) No: una probabilidad siempre está entre 0 y 1. c) \(0{,}85\) y \(0{,}15\). d) \(1-0{,}9=0{,}1\). e) \(P(G\cup T)=1-0{,}25=0{,}75\); \(P(G\cap T)=0{,}60+0{,}35-0{,}75=0{,}20\): el <strong>20 %</strong>.",
    r"a) \(\frac58\). b) No: a probability is always between 0 and 1. c) \(0.85\) and \(0.15\). d) \(1-0.9=0.1\). e) \(P(D\cup C)=1-0.25=0.75\); \(P(D\cap C)=0.60+0.35-0.75=0.20\): <strong>20 %</strong>."))
assert 1 - Fr(3, 8) == Fr(5, 8) and Fr(25, 100) + Fr(6, 10) == Fr(85, 100) and Fr(60, 100) + Fr(35, 100) - Fr(75, 100) == Fr(20, 100)

# =====================================================================
# 12.4 Experiments regulars. Llei de Laplace
# =====================================================================
s4 = box('def', L('Experiments regulars', 'Experimentos regulares', 'Regular experiments'),
  P(r"Un experiment aleatori és <strong>regular</strong> quan tots els resultats elementals tenen la mateixa probabilitat (són <strong>equiprobables</strong>). Per exemple: llançar una moneda o un dau no trucats, girar una ruleta amb sectors iguals, traure a l'atzar una carta d'una baralla o una bola d'una bossa (si totes les boles són iguals al tacte).",
    r"Un experimento aleatorio es <strong>regular</strong> cuando todos los resultados elementales tienen la misma probabilidad (son <strong>equiprobables</strong>). Por ejemplo: lanzar una moneda o un dado no trucados, girar una ruleta con sectores iguales, sacar al azar una carta de una baraja o una bola de una bolsa (si todas las bolas son iguales al tacto).",
    r"A random experiment is <strong>regular</strong> when all the elementary outcomes have the same probability (they are <strong>equally likely</strong>). For example: tossing a fair coin or rolling a fair die, spinning a wheel with equal sectors, drawing a card from a pack at random or a ball from a bag (if all the balls feel the same).")
  + P(r"Si l'espai mostral té \(n\) resultats equiprobables, cadascun té probabilitat \(\frac1n\): en un dau, \(P(1)=P(2)=\dots=P(6)=\frac16\).",
      r"Si el espacio muestral tiene \(n\) resultados equiprobables, cada uno tiene probabilidad \(\frac1n\): en un dado, \(P(1)=P(2)=\dots=P(6)=\frac16\).",
      r"If the sample space has \(n\) equally likely outcomes, each has probability \(\frac1n\): on a die, \(P(1)=P(2)=\dots=P(6)=\frac16\)."))

s4 += box('prop', L('Llei de Laplace', 'Ley de Laplace', "Laplace's rule"),
  P(r"En un experiment regular, la probabilitat d'un esdeveniment \(A\) és el quocient entre el nombre de resultats favorables a \(A\) i el nombre de resultats possibles:",
    r"En un experimento regular, la probabilidad de un suceso \(A\) es el cociente entre el número de resultados favorables a \(A\) y el número de resultados posibles:",
    r"In a regular experiment, the probability of an event \(A\) is the number of outcomes favourable to \(A\) divided by the number of possible outcomes:")
  + D(r"P(A)=\frac{%s}{%s}" % (Lt('nombre de casos favorables', 'número de casos favorables', 'number of favourable outcomes'), Lt('nombre de casos possibles', 'número de casos posibles', 'number of possible outcomes')))
  + ul(L(r"Dau: \(P(\text{parell})=\frac36=\frac12\); \(P(\text{múltiple de 3})=\frac26=\frac13\).", r"Dado: \(P(\text{par})=\frac36=\frac12\); \(P(\text{múltiplo de 3})=\frac26=\frac13\).", r"Die: \(P(\text{even})=\frac36=\frac12\); \(P(\text{multiple of 3})=\frac26=\frac13\)."),
       L(r"Bossa amb 5 boles roges, 3 blaves i 2 verdes: \(P(R)=\frac5{10}=\frac12\); \(P(\text{no verda})=\frac8{10}=\frac45\).", r"Bolsa con 5 bolas rojas, 3 azules y 2 verdes: \(P(R)=\frac5{10}=\frac12\); \(P(\text{no verde})=\frac8{10}=\frac45\).", r"Bag with 5 red, 3 blue and 2 green balls: \(P(R)=\frac5{10}=\frac12\); \(P(\text{not green})=\frac8{10}=\frac45\)."),
       L(r"Baralla espanyola (40 cartes): \(P(\text{oros})=\frac{10}{40}=\frac14\); \(P(\text{as})=\frac4{40}=\frac1{10}\); \(P(\text{figura})=\frac{12}{40}=\frac3{10}\).", r"Baraja española (40 cartas): \(P(\text{oros})=\frac{10}{40}=\frac14\); \(P(\text{as})=\frac4{40}=\frac1{10}\); \(P(\text{figura})=\frac{12}{40}=\frac3{10}\).", r"Spanish pack (40 cards): \(P(\text{coins})=\frac{10}{40}=\frac14\); \(P(\text{ace})=\frac4{40}=\frac1{10}\); \(P(\text{face card})=\frac{12}{40}=\frac3{10}\)."))
  + figs(bag('RRRRRBBBVV', cap=L('5 roges, 3 blaves i 2 verdes', '5 rojas, 3 azules y 2 verdes', '5 red, 3 blue and 2 green')))
  + note(r"La llei de Laplace <strong>només</strong> val si els resultats són equiprobables. Una ruleta amb sectors de mides diferents, un dau trucat o una xinxeta no són regulars. I compte: «aprovar o suspendre» té dos resultats, però això no vol dir que cada un tinga probabilitat \(\frac12\)!",
         r"La ley de Laplace <strong>solo</strong> vale si los resultados son equiprobables. Una ruleta con sectores de tamaños distintos, un dado trucado o una chincheta no son regulares. Y cuidado: «aprobar o suspender» tiene dos resultados, ¡pero eso no quiere decir que cada uno tenga probabilidad \(\frac12\)!",
         r"Laplace's rule <strong>only</strong> works if the outcomes are equally likely. A wheel with sectors of different sizes, a loaded die or a drawing pin aren't regular. And careful: “pass or fail” has two outcomes, but that doesn't mean each has probability \(\frac12\)!", '⚠️')
  + widget('w-bag', '👜', L('Una bossa de boles', 'Una bolsa de bolas', 'A bag of balls'),
           ['<div class="wrow">' + rng('r', 0, 10, 1, 5, 'R') + rng('b', 0, 10, 1, 3, 'B') + rng('v', 0, 10, 1, 2, 'V') + rng('g', 0, 10, 1, 0, 'G') + '</div>',
            '<div class="wrow"><div class="seg sg-e" role="group"></div></div>',
            '<div class="wrow"><button class="btn" type="button" data-a="draw">🖐 ' + L('Trau-ne una', 'Saca una', 'Draw one') + '</button><span class="drawn"></span></div>'])
  + drill('lap', 'Entrena: llei de Laplace', 'Entrena: ley de Laplace', 'Train: Laplace\'s rule'))
ck(Fr(3, 6), Fr(1, 2)); ck(Fr(5, 10), Fr(1, 2)); ck(Fr(8, 10), Fr(4, 5)); ck(Fr(10, 40), Fr(1, 4)); ck(Fr(4, 40), Fr(1, 10)); ck(Fr(12, 40), Fr(3, 10))

W_ = 'PROBABILITAT'
assert len(W_) == 12 and sum(c in 'AEIOU' for c in W_) == 5 and W_.count('A') == 2 and W_.count('B') == 2 and W_.count('T') == 2
x_ = [x for x in range(0, 100) if Fr(3 + x, 15 + x) == Fr(1, 2)]
assert x_ == [9]
s4 += levels(
 [prob(L(r"En una urna hi ha 4 boles roges, 6 de blaves i 5 de verdes. Traiem una bola a l'atzar. Calcula la probabilitat que siga roja, blava, verda i que no siga blava.",
         r"En una urna hay 4 bolas rojas, 6 azules y 5 verdes. Sacamos una bola al azar. Calcula la probabilidad de que sea roja, azul, verde y de que no sea azul.",
         r"An urn holds 4 red, 6 blue and 5 green balls. We draw one at random. Find the probability that it's red, blue, green, and that it isn't blue."),
       P(r"Hi ha \(4+6+5=15\) boles (casos possibles):", r"Hay \(4+6+5=15\) bolas (casos posibles):", r"There are \(4+6+5=15\) balls (possible outcomes):") + figs(bag('RRRRBBBBBBVVVVV')),
       D(r"P(R)=\frac4{15}\qquad P(B)=\frac6{15}=\frac25\qquad P(V)=\frac5{15}=\frac13"),
       D(r"P(\overline{B})=1-\frac25=\boxed{\frac35}\qquad\left(%s\ \frac{4+5}{15}=\frac9{15}=\frac35\right)" % Lt('o bé', 'o bien', 'or')),
       P(r"Comprovació: \(\frac4{15}+\frac6{15}+\frac5{15}=1\ \checkmark\)", r"Comprobación: \(\frac4{15}+\frac6{15}+\frac5{15}=1\ \checkmark\)", r"Check: \(\frac4{15}+\frac6{15}+\frac5{15}=1\ \checkmark\)")),
  prob(L(r"Llancem un dau. Calcula la probabilitat de traure un nombre primer i la de traure més de 4.", r"Lanzamos un dado. Calcula la probabilidad de sacar un número primo y la de sacar más de 4.", r"We roll a die. Find the probability of rolling a prime number and of rolling more than 4."),
       D(r"P(\text{%s})=P(\{2,3,5\})=\frac36=\boxed{\frac12}\qquad P(\{5,6\})=\frac26=\boxed{\frac13}" % Lt('primer', 'primo', 'prime')))],
 [prob(L(r"Escrivim cada lletra de la paraula PROBABILITAT en una targeta i en traiem una a l'atzar. Quina és la probabilitat que siga una A? I una vocal? I una consonant?",
         r"Escribimos cada letra de la palabra valenciana PROBABILITAT en una tarjeta y sacamos una al azar. ¿Cuál es la probabilidad de que sea una A? ¿Y una vocal? ¿Y una consonante?",
         r"We write each letter of the Valencian word PROBABILITAT on a card and draw one at random. What is the probability that it's an A? A vowel? A consonant?"),
       P(r"Hi ha 12 targetes. Les vocals són O, A, I, I, A (5 targetes):", r"Hay 12 tarjetas. Las vocales son O, A, I, I, A (5 tarjetas):", r"There are 12 cards. The vowels are O, A, I, I, A (5 cards):"),
       D(r"P(A)=\frac2{12}=\boxed{\frac16}\qquad P(\text{%s})=\boxed{\frac5{12}}\qquad P(\text{%s})=1-\frac5{12}=\boxed{\frac7{12}}" % (Lt('vocal', 'vocal', 'vowel'), Lt('consonant', 'consonante', 'consonant')))),
  prob(L(r"Traiem una carta d'una baralla espanyola. Calcula la probabilitat que siga un rei, que siga de copes o figura, i que no siga ni de copes ni figura.",
         r"Sacamos una carta de una baraja española. Calcula la probabilidad de que sea un rey, de que sea de copas o figura, y de que no sea ni de copas ni figura.",
         r"We draw a card from a Spanish pack. Find the probability that it's a king, that it's cups or a face card, and that it's neither cups nor a face card."),
       D(r"P(\text{%s})=\frac4{40}=\boxed{\frac1{10}}" % Lt('rei', 'rey', 'king')),
       P(r"Copes o figura: 10 copes + 12 figures − 3 figures de copes (comptades dues vegades) = 19 cartes.", r"Copas o figura: 10 copas + 12 figuras − 3 figuras de copas (contadas dos veces) = 19 cartas.", r"Cups or face card: 10 cups + 12 face cards − 3 face cards of cups (counted twice) = 19 cards."),
       D(r"P(C\cup F)=\frac{10}{40}+\frac{12}{40}-\frac3{40}=\boxed{\frac{19}{40}}\qquad P(\overline{C\cup F})=1-\frac{19}{40}=\boxed{\frac{21}{40}}"))],
 [prob(L(r"En una bossa hi ha 3 boles roges i unes quantes de blaves. Si la probabilitat de traure una bola roja és \(\frac15\), quantes boles blaves hi ha? Quantes boles roges hauríem d'afegir perquè la probabilitat de roja fóra \(\frac12\)?",
         r"En una bolsa hay 3 bolas rojas y algunas azules. Si la probabilidad de sacar una bola roja es \(\frac15\), ¿cuántas bolas azules hay? ¿Cuántas bolas rojas tendríamos que añadir para que la probabilidad de roja fuera \(\frac12\)?",
         r"A bag has 3 red balls and some blue ones. If the probability of drawing a red ball is \(\frac15\), how many blue balls are there? How many red balls would we need to add to make the probability of red \(\frac12\)?"),
       P(r"Si hi ha \(n\) boles en total, \(\frac3n=\frac15\Rightarrow n=15\). Per tant hi ha \(15-3=\) <strong>12 boles blaves</strong>.", r"Si hay \(n\) bolas en total, \(\frac3n=\frac15\Rightarrow n=15\). Por tanto hay \(15-3=\) <strong>12 bolas azules</strong>.", r"If there are \(n\) balls in total, \(\frac3n=\frac15\Rightarrow n=15\). So there are \(15-3=\) <strong>12 blue balls</strong>."),
       P(r"Si afegim \(x\) boles roges:", r"Si añadimos \(x\) bolas rojas:", r"If we add \(x\) red balls:"),
       D(r"\frac{3+x}{15+x}=\frac12\ \Rightarrow\ 6+2x=15+x\ \Rightarrow\ \boxed{x=9}"),
       P(r"Comprovació: 12 roges i 12 blaves, \(P(R)=\frac{12}{24}=\frac12\ \checkmark\) (també ho podíem pensar així: cal que hi haja tantes roges com blaves).", r"Comprobación: 12 rojas y 12 azules, \(P(R)=\frac{12}{24}=\frac12\ \checkmark\) (también podíamos pensarlo así: hace falta que haya tantas rojas como azules).", r"Check: 12 red and 12 blue, \(P(R)=\frac{12}{24}=\frac12\ \checkmark\) (we could also see it this way: there must be as many red as blue)."))])
s4 += practice([
  ('★', L(r"a) Girem una ruleta de 10 sectors iguals numerats de l'1 al 10. Calcula la probabilitat de traure un múltiple de 3 i la de traure un nombre parell.", r"a) Giramos una ruleta de 10 sectores iguales numerados del 1 al 10. Calcula la probabilidad de sacar un múltiplo de 3 y la de sacar un número par.", r"a) We spin a wheel with 10 equal sectors numbered 1 to 10. Find the probability of a multiple of 3 and of an even number.")),
  ('★★', L(r"b) En una classe hi ha 14 xiques i 11 xics. Triem una persona a l'atzar per a ser delegada. Quina és la probabilitat que siga un xic? c) Traiem una carta de la baralla espanyola: quina és la probabilitat que siga un as o un rei?", r"b) En una clase hay 14 chicas y 11 chicos. Elegimos una persona al azar para ser delegada. ¿Cuál es la probabilidad de que sea un chico? c) Sacamos una carta de la baraja española: ¿cuál es la probabilidad de que sea un as o un rey?", r"b) A class has 14 girls and 11 boys. We pick someone at random as class rep. What is the probability it's a boy? c) We draw a card from the Spanish pack: what is the probability that it's an ace or a king?")),
  ('★★★', L(r"d) En una bossa hi ha boles roges, blaves i verdes. \(P(R)=\frac13\), \(P(B)=\frac12\) i hi ha 4 boles verdes. Quantes boles hi ha de cada color?", r"d) En una bolsa hay bolas rojas, azules y verdes. \(P(R)=\frac13\), \(P(A)=\frac12\) y hay 4 bolas verdes. ¿Cuántas bolas hay de cada color?", r"d) A bag has red, blue and green balls. \(P(R)=\frac13\), \(P(B)=\frac12\) and there are 4 green balls. How many balls of each colour are there?"))],
  P(r"a) \(\frac3{10}\) i \(\frac5{10}=\frac12\). b) \(\frac{11}{25}=0{,}44\). c) \(\frac8{40}=\frac15\). d) \(P(V)=1-\frac13-\frac12=\frac16\), i \(\frac4n=\frac16\Rightarrow n=24\): 8 roges, 12 blaves i 4 verdes.",
    r"a) \(\frac3{10}\) y \(\frac5{10}=\frac12\). b) \(\frac{11}{25}=0{,}44\). c) \(\frac8{40}=\frac15\). d) \(P(V)=1-\frac13-\frac12=\frac16\), y \(\frac4n=\frac16\Rightarrow n=24\): 8 rojas, 12 azules y 4 verdes.",
    r"a) \(\frac3{10}\) and \(\frac5{10}=\frac12\). b) \(\frac{11}{25}=0.44\). c) \(\frac8{40}=\frac15\). d) \(P(G)=1-\frac13-\frac12=\frac16\), and \(\frac4n=\frac16\Rightarrow n=24\): 8 red, 12 blue and 4 green."))
assert Fr(11, 25) == Fr(44, 100) and 1 - Fr(1, 3) - Fr(1, 2) == Fr(1, 6) and (24 // 3, 24 // 2, 4) == (8, 12, 4)
