# 11.3 Probabilitat d'un esdeveniment (freqüències, llei dels grans nombres i propietats, amb el contrari i la unió)
# Fet a partir de l'apartat 11.3 de 2n ESO (../2eso-t11/s3.py) i de les propietats de 3r ESO (../3eso-t12/s34.py).
from comu import *

FD = [8, 11, 9, 12, 10, 10]; N_ = sum(FD)
assert N_ == 60
HD = [Fr(f, N_) for f in FD]
assert sum(HD) == 1
s3 = box('def', L('Freqüència absoluta i freqüència relativa', 'Frecuencia absoluta y frecuencia relativa', 'Absolute and relative frequency'),
  P(r"Si repetim un experiment aleatori \(n\) vegades i un esdeveniment \(A\) ocorre \(f\) vegades, \(f\) és la <strong>freqüència absoluta</strong> d'\(A\) i",
    r"Si repetimos un experimento aleatorio \(n\) veces y un suceso \(A\) ocurre \(f\) veces, \(f\) es la <strong>frecuencia absoluta</strong> de \(A\) y",
    r"If we repeat a random experiment \(n\) times and an event \(A\) happens \(f\) times, \(f\) is the <strong>absolute frequency</strong> of \(A\) and")
  + D(r"h(A)=\frac{f}{n}=\frac{%s}{%s}" % (Lt('vegades que ocorre A', 'veces que ocurre A', 'times A happens'), Lt('vegades que repetim', 'veces que repetimos', 'number of trials')))
  + P(r"és la seua <strong>freqüència relativa</strong>. És un nombre entre 0 i 1 (es pot escriure com a fracció, decimal o percentatge), i les freqüències relatives de tots els resultats sumen 1. Per exemple, hem llançat un dau 60 vegades:",
      r"es su <strong>frecuencia relativa</strong>. Es un número entre 0 y 1 (se puede escribir como fracción, decimal o porcentaje), y las frecuencias relativas de todos los resultados suman 1. Por ejemplo, hemos lanzado un dado 60 veces:",
      r"is its <strong>relative frequency</strong>. It's a number between 0 and 1 (it can be written as a fraction, a decimal or a percentage), and the relative frequencies of all outcomes add up to 1. For example, we've rolled a die 60 times:")
  + tbl([L('Resultat', 'Resultado', 'Outcome')] + [str(i) for i in range(1, 7)] + ['Total'],
        [[L(r'Freq. absoluta \(f\)', r'Frec. absoluta \(f\)', r'Abs. frequency \(f\)')] + [str(f) for f in FD] + ['60'],
         [L(r'Freq. relativa \(h\)', r'Frec. relativa \(h\)', r'Rel. frequency \(h\)')] + [r'\(\frac{%d}{60}\)' % f for f in FD] + ['1'],
         [L('En decimal', 'En decimal', 'As a decimal')] + [r'\(%s\)' % dc(h) for h in HD] + ['1']], cls='narrow')
  + P(r"La freqüència relativa de «traure parell» és \(\frac{11+12+10}{60}=\frac{33}{60}=0{,}55\), és a dir, el 55 % de les vegades.",
      r"La frecuencia relativa de «sacar par» es \(\frac{11+12+10}{60}=\frac{33}{60}=0{,}55\), es decir, el 55 % de las veces.",
      r"The relative frequency of “even” is \(\frac{11+12+10}{60}=\frac{33}{60}=0.55\), that is, 55 % of the time."))
ck(Fr(11 + 12 + 10, 60), '0,55'); ck(HD[0], '0,13', 2); ck(HD[1], '0,18', 2); ck(HD[2], '0,15', 2); ck(HD[3], '0,20', 2); ck(HD[4], '0,17', 2)

XN = [10, 50, 100, 200, 500, 1000]; XF = [7, 32, 61, 126, 309, 621]
XH = [Fr(f, n) for f, n in zip(XF, XN)]
XHt = ['0,7', '0,64', '0,61', '0,63', '0,618', '0,621']
for h, t in zip(XH, XHt): ck(h, t)
s3 += box('prop', L('La llei dels grans nombres', 'La ley de los grandes números', 'The law of large numbers'),
  P(r"Quan repetim un experiment aleatori moltes vegades, la freqüència relativa d'un esdeveniment \(A\) <strong>s'estabilitza</strong> al voltant d'un valor fix. Aquest valor és la <strong>probabilitat</strong> de l'esdeveniment, \(P(A)\):",
    r"Cuando repetimos un experimento aleatorio muchas veces, la frecuencia relativa de un suceso \(A\) <strong>se estabiliza</strong> alrededor de un valor fijo. Ese valor es la <strong>probabilidad</strong> del suceso, \(P(A)\):",
    r"When we repeat a random experiment many times, the relative frequency of an event \(A\) <strong>settles down</strong> around a fixed value. That value is the <strong>probability</strong> of the event, \(P(A)\):")
  + D(r"P(A)\approx h(A)\quad %s" % Lt('si el nombre de repeticions és gran', 'si el número de repeticiones es grande', 'if the number of trials is large'))
  + P(r"Hem llançat una xinxeta i hem anotat quantes vegades ha caigut amb la punta cap amunt:", r"Hemos lanzado una chincheta y hemos anotado cuántas veces ha caído con la punta hacia arriba:", r"We tossed a drawing pin and recorded how many times it landed point up:")
  + tbl([L(r'Llançaments \(n\)', r'Lanzamientos \(n\)', r'Tosses \(n\)')] + [str(n) for n in XN],
        [[L(r'Punta amunt \(f\)', r'Punta arriba \(f\)', r'Point up \(f\)')] + [str(f) for f in XF],
         [L(r'Freq. relativa \(h\)', r'Frec. relativa \(h\)', r'Rel. frequency \(h\)')] + [r'\(%s\)' % t.replace(',', '{,}') for t in XHt]], cls='narrow')
  + P(r"Al principi la freqüència relativa canvia molt, però a mesura que fem més llançaments s'acosta a 0,62. Diem que \(P(\text{%s})\approx0{,}62\)." % Lt('punta amunt', 'punta arriba', 'point up'),
      r"Al principio la frecuencia relativa cambia mucho, pero a medida que hacemos más lanzamientos se acerca a 0,62. Decimos que \(P(\text{%s})\approx0{,}62\)." % Lt('punta amunt', 'punta arriba', 'point up'),
      r"At first the relative frequency changes a lot, but as we toss more it gets closer to 0.62. We say \(P(\text{%s})\approx0.62\)." % Lt('punta amunt', 'punta arriba', 'point up'))
  + note(r"El naturalista Buffon va llançar una moneda 4040 vegades i va obtindre 2048 cares (\(h\approx0{,}507\)), i l'estadístic Karl Pearson, 24 000 vegades amb 12 012 cares (\(h=0{,}5005\)). Totes dues freqüències s'acosten a \(\frac12\).",
         r"El naturalista Buffon lanzó una moneda 4040 veces y obtuvo 2048 caras (\(h\approx0{,}507\)), y el estadístico Karl Pearson, 24 000 veces con 12 012 caras (\(h=0{,}5005\)). Las dos frecuencias se acercan a \(\frac12\).",
         r"The naturalist Buffon tossed a coin 4040 times and got 2048 heads (\(h\approx0.507\)), and the statistician Karl Pearson tossed one 24,000 times and got 12,012 heads (\(h=0.5005\)). Both frequencies are close to \(\frac12\).", '📜')
  + widget('w-lgn', '📈', L('Repeteix l\'experiment moltes vegades', 'Repite el experimento muchas veces', 'Repeat the experiment many times'),
           ['<div class="wrow"><div class="seg sg-x" role="group"></div></div>',
            '<div class="wrow"><button class="btn primary" type="button" data-n="1">+1</button><button class="btn primary" type="button" data-n="10">+10</button><button class="btn primary" type="button" data-n="100">+100</button><button class="btn primary" type="button" data-n="1000">+1000</button><button class="btn" type="button" data-a="clr">↺ ' + L('Torna a començar', 'Volver a empezar', 'Start again') + '</button></div>'],
           out='<div class="gout"></div>')
  + P(r"Si coneixem (o hem estimat) \(P(A)\) i repetim l'experiment \(n\) vegades, esperem que \(A\) ocórrega <strong>aproximadament</strong> \(n\cdot P(A)\) vegades: si llancem la xinxeta 300 vegades, esperem que caiga amb la punta cap amunt unes \(300\cdot0{,}62=186\) vegades (no exactament 186!).",
      r"Si conocemos (o hemos estimado) \(P(A)\) y repetimos el experimento \(n\) veces, esperamos que \(A\) ocurra <strong>aproximadamente</strong> \(n\cdot P(A)\) veces: si lanzamos la chincheta 300 veces, esperamos que caiga con la punta hacia arriba unas \(300\cdot0{,}62=186\) veces (¡no exactamente 186!).",
      r"If we know (or have estimated) \(P(A)\) and repeat the experiment \(n\) times, we expect \(A\) to happen <strong>about</strong> \(n\cdot P(A)\) times: if we toss the drawing pin 300 times, we expect it to land point up about \(300\cdot0.62=186\) times (not exactly 186!).")
  + note(r"L'atzar no té memòria. Si una moneda ha eixit creu cinc vegades seguides, la probabilitat que la següent siga cara continua sent \(\frac12\). La llei dels grans nombres parla de moltíssimes repeticions, no de «compensar» les últimes.",
         r"El azar no tiene memoria. Si una moneda ha salido cruz cinco veces seguidas, la probabilidad de que la siguiente sea cara sigue siendo \(\frac12\). La ley de los grandes números habla de muchísimas repeticiones, no de «compensar» las últimas.",
         r"Chance has no memory. If a coin has landed tails five times in a row, the probability that the next toss is heads is still \(\frac12\). The law of large numbers is about a huge number of trials, not about “making up” for the last few.", '🧠')
  + drill('freq', 'Entrena: freqüències i previsions', 'Entrena: frecuencias y previsiones', 'Train: frequencies and predictions'))
ck(Fr(2048, 4040), '0,507', 3); ck(Fr(12012, 24000), '0,5005'); ck(300 * Fr(62, 100), 186)

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
  + P(r"Com la calculem? Hi ha dues maneres:",
      r"¿Cómo la calculamos? Hay dos maneras:",
      r"How do we find it? There are two ways:")
  + ul(L(r"<strong>Experimentant</strong>: repetim l'experiment moltes vegades i prenem la freqüència relativa (llei dels grans nombres). És l'única manera quan els resultats no són igual de probables: una xinxeta, un tap de suro, un dau trucat, un tir a cistella…",
         r"<strong>Experimentando</strong>: repetimos el experimento muchas veces y tomamos la frecuencia relativa (ley de los grandes números). Es la única manera cuando los resultados no son igual de probables: una chincheta, un tapón de corcho, un dado trucado, un tiro a canasta…",
         r"<strong>By experimenting</strong>: we repeat the experiment many times and take the relative frequency (law of large numbers). It's the only way when the outcomes aren't equally likely: a drawing pin, a cork, a loaded die, a basketball shot…"),
       L(r"<strong>Comptant</strong>: si tots els resultats tenen la mateixa possibilitat (una moneda, un dau, una bossa de boles…), podem calcular-la sense fer l'experiment, amb la <strong>llei de Laplace</strong> (apartat 11.4).",
         r"<strong>Contando</strong>: si todos los resultados tienen la misma posibilidad (una moneda, un dado, una bolsa de bolas…), podemos calcularla sin hacer el experimento, con la <strong>ley de Laplace</strong> (apartado 11.4).",
         r"<strong>By counting</strong>: if all the outcomes are equally likely (a coin, a die, a bag of balls…), we can work it out without doing the experiment, using <strong>Laplace's rule</strong> (section 11.4).")))

s3 += box('prop', L('Propietats de la probabilitat', 'Propiedades de la probabilidad', 'Properties of probability'),
  ol(L(r"Per a qualsevol esdeveniment, \(0\le P(A)\le1\).", r"Para cualquier suceso, \(0\le P(A)\le1\).", r"For any event, \(0\le P(A)\le1\)."),
     L(r"\(P(E)=1\) (esdeveniment segur) i \(P(\varnothing)=0\) (esdeveniment impossible).", r"\(P(E)=1\) (suceso seguro) y \(P(\varnothing)=0\) (suceso imposible).", r"\(P(E)=1\) (certain event) and \(P(\varnothing)=0\) (impossible event)."),
     L(r"Les probabilitats de tots els resultats elementals sumen 1, i la probabilitat d'un esdeveniment és la suma de les dels seus resultats: \(P(\text{parell})=P(2)+P(4)+P(6)\).", r"Las probabilidades de todos los resultados elementales suman 1, y la probabilidad de un suceso es la suma de las de sus resultados: \(P(\text{par})=P(2)+P(4)+P(6)\).", r"The probabilities of all the elementary outcomes add up to 1, and the probability of an event is the sum of those of its outcomes: \(P(\text{even})=P(2)+P(4)+P(6)\)."),
     L(r"<strong>Esdeveniment contrari:</strong> \(P(\overline{A})=1-P(A)\).", r"<strong>Suceso contrario:</strong> \(P(\overline{A})=1-P(A)\).", r"<strong>Complementary event:</strong> \(P(\overline{A})=1-P(A)\)."),
     L(r"Si \(A\) i \(B\) són <strong>incompatibles</strong>: \(P(A\cup B)=P(A)+P(B)\).", r"Si \(A\) y \(B\) son <strong>incompatibles</strong>: \(P(A\cup B)=P(A)+P(B)\).", r"If \(A\) and \(B\) are <strong>mutually exclusive</strong>: \(P(A\cup B)=P(A)+P(B)\)."),
     L(r"En general (compatibles o no): \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\). Restem la intersecció perquè l'hem sumada dues vegades.", r"En general (compatibles o no): \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\). Restamos la intersección porque la hemos sumado dos veces.", r"In general (exclusive or not): \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\). We subtract the intersection because it has been added twice."))
  + note(r"La propietat del contrari és molt útil: de vegades és més fàcil calcular la probabilitat que una cosa <strong>no</strong> ocórrega i restar-la d'1. Ho farem servir moltes vegades en els apartats 11.5 i 11.6 (per exemple, per a «almenys un»).",
         r"La propiedad del contrario es muy útil: a veces es más fácil calcular la probabilidad de que algo <strong>no</strong> ocurra y restarla de 1. Lo usaremos muchas veces en los apartados 11.5 y 11.6 (por ejemplo, para «al menos uno»).",
         r"The complement rule is very handy: sometimes it's easier to work out the probability that something does <strong>not</strong> happen and subtract it from 1. We'll use it a lot in sections 11.5 and 11.6 (for example, for “at least one”).")
  + widget('w-prop', '⚖️', L('Probabilitats de dos esdeveniments', 'Probabilidades de dos sucesos', 'Probabilities of two events'),
           ['<div class="wrow">' + rng('a', 0, 1, 0.05, 0.5, 'P(A)') + rng('b', 0, 1, 0.05, 0.4, 'P(B)') + rng('c', 0, 1, 0.05, 0.2, 'P(A∩B)') + '</div>',
            quick([('0.5|0.4|0.2', 'P(A)=0,5 · P(B)=0,4 · P(A∩B)=0,2'), ('0.3|0.45|0', L('incompatibles', 'incompatibles', 'mutually exclusive')), ('0.6|0.3|0.3', 'B ⊂ A'), ('0.7|0.6|0.1', L('impossible?', '¿imposible?', 'impossible?'))])])
  + drill('falta', 'Entrena: les probabilitats sumen 1', 'Entrena: las probabilidades suman 1', 'Train: probabilities add up to 1')
  + drill('prop', 'Entrena: propietats de la probabilitat', 'Entrena: propiedades de la probabilidad', 'Train: properties of probability'))


PT = [Fr(1, 10), Fr(2, 10), Fr(1, 10), Fr(2, 10), Fr(1, 10)]; P6 = 1 - sum(PT)
assert P6 == Fr(3, 10) and PT[1] + PT[3] + P6 == Fr(7, 10)
pa, pb, pab = Fr(1, 2), Fr(2, 5), Fr(1, 5)
assert pa + pb - pab == Fr(7, 10) and 1 - (pa + pb - pab) == Fr(3, 10)
pf, pbq, pfb = Fr(30, 100), Fr(20, 100), Fr(8, 100)
assert pf + pbq - pfb == Fr(42, 100) and 1 - Fr(42, 100) == Fr(58, 100) and pf - pfb == Fr(22, 100)
pu, pa3, pb3 = Fr(8, 10), Fr(5, 10), Fr(45, 100)
s3 += levels(
 [prob(L(r"La probabilitat que demà ploga és 0,35. Quina és la probabilitat que no ploga?", r"La probabilidad de que mañana llueva es 0,35. ¿Cuál es la probabilidad de que no llueva?", r"The probability that it will rain tomorrow is 0.35. What is the probability that it won't?"),
       D(r"P(\overline{A})=1-P(A)=1-0{,}35=\boxed{0{,}65}")),
  prob(L(r"Llancem un tap de suro 200 vegades i cau dret 46 vegades. Estima la probabilitat que caiga dret. Quantes vegades esperes que caiga dret si el llances 500 vegades?",
         r"Lanzamos un tapón de corcho 200 veces y cae de pie 46 veces. Estima la probabilidad de que caiga de pie. ¿Cuántas veces esperas que caiga de pie si lo lanzas 500 veces?",
         r"We toss a cork 200 times and it lands upright 46 times. Estimate the probability that it lands upright. How many times do you expect it to land upright if you toss it 500 times?"),
       D(r"P(\text{%s})\approx h=\frac{46}{200}=\boxed{0{,}23}\qquad 500\cdot0{,}23=\boxed{115\ \text{%s}}" % (Lt('dret', 'de pie', 'upright'), Lt('vegades', 'veces', 'times')))),
  prob(L(r"Un dau està trucat. Les probabilitats dels resultats de l'1 al 5 són 0,1, 0,2, 0,1, 0,2 i 0,1. Calcula la probabilitat de traure un 6 i la de traure parell.",
         r"Un dado está trucado. Las probabilidades de los resultados del 1 al 5 son 0,1, 0,2, 0,1, 0,2 y 0,1. Calcula la probabilidad de sacar un 6 y la de sacar par.",
         r"A die is loaded. The probabilities of the outcomes 1 to 5 are 0.1, 0.2, 0.1, 0.2 and 0.1. Find the probability of rolling a 6 and of rolling an even number."),
       P(r"Les sis probabilitats han de sumar 1:", r"Las seis probabilidades deben sumar 1:", r"The six probabilities must add up to 1:"),
       D(r"P(6)=1-(0{,}1+0{,}2+0{,}1+0{,}2+0{,}1)=1-0{,}7=\boxed{0{,}3}"),
       D(r"P(\text{%s})=P(2)+P(4)+P(6)=0{,}2+0{,}2+0{,}3=\boxed{0{,}7}" % Lt('parell', 'par', 'even')))],
 [prob(L(r"Una jugadora de bàsquet ha encertat 168 dels 240 tirs lliures que ha llançat aquesta temporada. Estima la probabilitat que encerte un tir lliure. Quants n'esperes que encerte en els 50 pròxims?",
         r"Una jugadora de baloncesto ha acertado 168 de los 240 tiros libres que ha lanzado esta temporada. Estima la probabilidad de que acierte un tiro libre. ¿Cuántos esperas que acierte en los 50 próximos?",
         r"A basketball player has scored 168 of the 240 free throws she's taken this season. Estimate the probability that she scores a free throw. How many do you expect her to score in the next 50?"),
       D(r"P(\text{%s})\approx\frac{168}{240}=\boxed{0{,}7}\qquad 50\cdot0{,}7=\boxed{35}" % Lt('encert', 'acierto', 'score'))),
  prob(L(r"Siguen \(A\) i \(B\) dos esdeveniments amb \(P(A)=0{,}5\), \(P(B)=0{,}4\) i \(P(A\cap B)=0{,}2\). Calcula \(P(A\cup B)\) i la probabilitat que no ocórrega cap dels dos.",
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
 [prob(L(r"En una bossa hi ha 20 boles, roges i blaves, però no sabem quantes de cada color. Traiem una bola, n'anotem el color i la tornem a la bossa. Ho repetim 500 vegades i ix roja 198 vegades. Quantes boles roges deu haver-hi?",
         r"En una bolsa hay 20 bolas, rojas y azules, pero no sabemos cuántas de cada color. Sacamos una bola, anotamos su color y la devolvemos a la bolsa. Lo repetimos 500 veces y sale roja 198 veces. ¿Cuántas bolas rojas debe de haber?",
         r"A bag holds 20 balls, red and blue, but we don't know how many of each. We draw a ball, note its colour and put it back. We do this 500 times and get red 198 times. How many red balls are there likely to be?"),
       D(r"P(R)\approx h(R)=\frac{198}{500}=0{,}396\approx0{,}4"),
       P(r"Si la probabilitat de roja és, més o menys, 0,4, aproximadament el 40 % de les boles són roges:", r"Si la probabilidad de roja es, más o menos, 0,4, aproximadamente el 40 % de las bolas son rojas:", r"If the probability of red is about 0.4, about 40 % of the balls are red:"),
       D(r"20\cdot0{,}396=7{,}92\ \Rightarrow\ \boxed{%s}" % Lt('unes 8 roges i 12 blaves', 'unas 8 rojas y 12 azules', 'about 8 red and 12 blue'))),
  prob(L(r"Sabem que \(P(A)=0{,}5\), \(P(B)=0{,}45\) i \(P(A\cup B)=0{,}8\). Calcula \(P(A\cap B)\). Són incompatibles? Quina és la probabilitat que ocórrega \(A\) però no \(B\)?",
         r"Sabemos que \(P(A)=0{,}5\), \(P(B)=0{,}45\) y \(P(A\cup B)=0{,}8\). Calcula \(P(A\cap B)\). ¿Son incompatibles? ¿Cuál es la probabilidad de que ocurra \(A\) pero no \(B\)?",
         r"We know that \(P(A)=0.5\), \(P(B)=0.45\) and \(P(A\cup B)=0.8\). Find \(P(A\cap B)\). Are they mutually exclusive? What is the probability that \(A\) happens but \(B\) doesn't?"),
       P(r"Aïllem la intersecció de la fórmula de la unió:", r"Despejamos la intersección de la fórmula de la unión:", r"Solve the union formula for the intersection:"),
       D(r"0{,}8=0{,}5+0{,}45-P(A\cap B)\ \Rightarrow\ P(A\cap B)=0{,}95-0{,}8=\boxed{0{,}15}"),
       P(r"Com que \(P(A\cap B)\neq0\), <strong>no</strong> són incompatibles. «\(A\) però no \(B\)» és la part d'\(A\) que no és en \(B\):", r"Como \(P(A\cap B)\neq0\), <strong>no</strong> son incompatibles. «\(A\) pero no \(B\)» es la parte de \(A\) que no está en \(B\):", r"Since \(P(A\cap B)\neq0\), they are <strong>not</strong> mutually exclusive. “\(A\) but not \(B\)” is the part of \(A\) outside \(B\):"),
       D(r"P(A\cap\overline{B})=P(A)-P(A\cap B)=0{,}5-0{,}15=\boxed{0{,}35}")),
  prob(L(r"Un dau està trucat de manera que cada cara té una probabilitat proporcional al seu nombre: \(P(1)=p\), \(P(2)=2p\), …, \(P(6)=6p\). Calcula \(p\), \(P(6)\) i la probabilitat de traure parell.",
         r"Un dado está trucado de manera que cada cara tiene una probabilidad proporcional a su número: \(P(1)=p\), \(P(2)=2p\), …, \(P(6)=6p\). Calcula \(p\), \(P(6)\) y la probabilidad de sacar par.",
         r"A die is loaded so that each face has a probability proportional to its number: \(P(1)=p\), \(P(2)=2p\), …, \(P(6)=6p\). Find \(p\), \(P(6)\) and the probability of rolling an even number."),
       P(r"Les sis probabilitats sumen 1:", r"Las seis probabilidades suman 1:", r"The six probabilities add up to 1:"),
       D(r"p+2p+3p+4p+5p+6p=21p=1\ \Rightarrow\ \boxed{p=\frac1{21}}\qquad P(6)=\frac6{21}=\boxed{\frac27}"),
       D(r"P(\text{%s})=P(2)+P(4)+P(6)=\frac{2+4+6}{21}=\frac{12}{21}=\boxed{\frac47}" % Lt('parell', 'par', 'even')))])
ck(Fr(46, 200), '0,23'); ck(500 * Fr(23, 100), 115); ck(Fr(168, 240), '0,7'); ck(50 * Fr(7, 10), 35); ck(Fr(198, 500), '0,396'); ck(20 * Fr(396, 1000), '7,92')
assert 1 - Fr(35, 100) == Fr(65, 100) and sum(range(1, 7)) == 21 and Fr(6, 21) == Fr(2, 7) and Fr(12, 21) == Fr(4, 7)
s3 += practice([
  ('★', L(r"a) Si \(P(A)=\frac38\), quant val \(P(\overline{A})\)? b) Pot ser que \(P(A)=1{,}2\)? I que \(P(A)=-0{,}3\)?", r"a) Si \(P(A)=\frac38\), ¿cuánto vale \(P(\overline{A})\)? b) ¿Puede ser que \(P(A)=1{,}2\)? ¿Y que \(P(A)=-0{,}3\)?", r"a) If \(P(A)=\frac38\), what is \(P(\overline{A})\)? b) Can \(P(A)=1.2\)? What about \(P(A)=-0.3\)?")),
  ('★★', L(r"c) \(A\) i \(B\) són incompatibles, amb \(P(A)=0{,}25\) i \(P(B)=0{,}6\). Calcula \(P(A\cup B)\) i \(P(\overline{A\cup B})\). d) En una ruleta, \(P(\text{roig})=0{,}45\), \(P(\text{negre})=0{,}45\) i la resta és verd. Quant val \(P(\text{verd})\)?", r"c) \(A\) y \(B\) son incompatibles, con \(P(A)=0{,}25\) y \(P(B)=0{,}6\). Calcula \(P(A\cup B)\) y \(P(\overline{A\cup B})\). d) En una ruleta, \(P(\text{rojo})=0{,}45\), \(P(\text{negro})=0{,}45\) y el resto es verde. ¿Cuánto vale \(P(\text{verde})\)?", r"c) \(A\) and \(B\) are mutually exclusive, with \(P(A)=0.25\) and \(P(B)=0.6\). Find \(P(A\cup B)\) and \(P(\overline{A\cup B})\). d) On a roulette wheel, \(P(\text{red})=0.45\), \(P(\text{black})=0.45\) and the rest is green. What is \(P(\text{green})\)?")),
  ('★★★', L(r"e) El 60 % de les famílies d'un poble té gos, el 35 % té gat i el 25 % no té cap dels dos. Quin percentatge té gos i gat?", r"e) El 60 % de las familias de un pueblo tiene perro, el 35 % tiene gato y el 25 % no tiene ninguno de los dos. ¿Qué porcentaje tiene perro y gato?", r"e) 60 % of the families in a village have a dog, 35 % have a cat and 25 % have neither. What percentage have both a dog and a cat?"))],
  P(r"a) \(\frac58\). b) No: una probabilitat sempre està entre 0 i 1. c) \(0{,}85\) i \(0{,}15\). d) \(1-0{,}9=0{,}1\). e) \(P(G\cup T)=1-0{,}25=0{,}75\); \(P(G\cap T)=0{,}60+0{,}35-0{,}75=0{,}20\): el <strong>20 %</strong>.",
    r"a) \(\frac58\). b) No: una probabilidad siempre está entre 0 y 1. c) \(0{,}85\) y \(0{,}15\). d) \(1-0{,}9=0{,}1\). e) \(P(G\cup T)=1-0{,}25=0{,}75\); \(P(G\cap T)=0{,}60+0{,}35-0{,}75=0{,}20\): el <strong>20 %</strong>.",
    r"a) \(\frac58\). b) No: a probability is always between 0 and 1. c) \(0.85\) and \(0.15\). d) \(1-0.9=0.1\). e) \(P(D\cup C)=1-0.25=0.75\); \(P(D\cap C)=0.60+0.35-0.75=0.20\): <strong>20 %</strong>."))
assert 1 - Fr(3, 8) == Fr(5, 8) and Fr(25, 100) + Fr(6, 10) == Fr(85, 100) and Fr(60, 100) + Fr(35, 100) - Fr(75, 100) == Fr(20, 100) and 1 - Fr(9, 10) == Fr(1, 10)
