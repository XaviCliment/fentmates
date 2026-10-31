# 12.5 Experiments irregulars. Llei dels grans nombres · 12.6 Experiments compostos
from comu import *

# =====================================================================
# 12.5 Experiments irregulars. Llei dels grans nombres
# =====================================================================
XN = [10, 50, 100, 200, 500, 1000]; XF = [7, 32, 61, 126, 309, 621]
XH = [Fr(f, n) for f, n in zip(XF, XN)]
XHt = ['0,7', '0,64', '0,61', '0,63', '0,618', '0,621']
for h, t in zip(XH, XHt): ck(h, t)
s5 = box('def', L('Experiments irregulars', 'Experimentos irregulares', 'Irregular experiments'),
  P(r"Un experiment aleatori és <strong>irregular</strong> quan els seus resultats <strong>no</strong> són equiprobables. Per exemple, llançar una xinxeta (pot caure amb la punta cap amunt o de costat), un tap de suro o un dau trucat, o que una jugadora de bàsquet encerte un tir lliure.",
    r"Un experimento aleatorio es <strong>irregular</strong> cuando sus resultados <strong>no</strong> son equiprobables. Por ejemplo, lanzar una chincheta (puede caer con la punta hacia arriba o de lado), un tapón de corcho o un dado trucado, o que una jugadora de baloncesto acierte un tiro libre.",
    r"A random experiment is <strong>irregular</strong> when its outcomes are <strong>not</strong> equally likely. For example, tossing a drawing pin (it can land point up or on its side), a cork or a loaded die, or a basketball player scoring a free throw.")
  + P(r"En aquests experiments <strong>no</strong> podem aplicar la llei de Laplace. L'única manera de conéixer la probabilitat és <strong>experimentar</strong>: repetir l'experiment moltes vegades i mirar la freqüència relativa.",
      r"En estos experimentos <strong>no</strong> podemos aplicar la ley de Laplace. La única manera de conocer la probabilidad es <strong>experimentar</strong>: repetir el experimento muchas veces y mirar la frecuencia relativa.",
      r"In these experiments we <strong>can't</strong> use Laplace's rule. The only way to find the probability is to <strong>experiment</strong>: repeat it many times and look at the relative frequency."))

s5 += box('prop', L('Llei dels grans nombres', 'Ley de los grandes números', 'Law of large numbers'),
  P(r"Quan repetim un experiment aleatori moltes vegades, la freqüència relativa d'un esdeveniment \(A\) <strong>s'estabilitza</strong> al voltant d'un valor fix. Aquest valor és la probabilitat de l'esdeveniment:",
    r"Cuando repetimos un experimento aleatorio muchas veces, la frecuencia relativa de un suceso \(A\) <strong>se estabiliza</strong> alrededor de un valor fijo. Ese valor es la probabilidad del suceso:",
    r"When we repeat a random experiment many times, the relative frequency of an event \(A\) <strong>settles down</strong> around a fixed value. That value is the probability of the event:")
  + D(r"P(A)\approx h(A)\quad %s" % Lt('si el nombre de repeticions és gran', 'si el número de repeticiones es grande', 'if the number of trials is large'))
  + P(r"Hem llançat una xinxeta i hem anotat quantes vegades ha caigut amb la punta cap amunt:", r"Hemos lanzado una chincheta y hemos anotado cuántas veces ha caído con la punta hacia arriba:", r"We tossed a drawing pin and recorded how many times it landed point up:")
  + tbl([L(r'Llançaments \(n\)', r'Lanzamientos \(n\)', r'Tosses \(n\)')] + [str(n) for n in XN],
        [[L(r'Punta amunt \(f\)', r'Punta arriba \(f\)', r'Point up \(f\)')] + [str(f) for f in XF],
         [L(r'Freq. relativa \(h\)', r'Frec. relativa \(h\)', r'Rel. frequency \(h\)')] + [r'\(%s\)' % t.replace(',', '{,}') for t in XHt]], cls='narrow')
  + P(r"Al principi la freqüència relativa canvia molt, però a mesura que fem més llançaments s'acosta a 0,62. Diem que \(P(\text{%s})\approx0{,}62\) i, per tant, \(P(\text{%s})\approx1-0{,}62=0{,}38\)." % (Lt('punta amunt', 'punta arriba', 'point up'), Lt('de costat', 'de lado', 'on its side')),
      r"Al principio la frecuencia relativa cambia mucho, pero a medida que hacemos más lanzamientos se acerca a 0,62. Decimos que \(P(\text{%s})\approx0{,}62\) y, por tanto, \(P(\text{%s})\approx1-0{,}62=0{,}38\)." % (Lt('punta amunt', 'punta arriba', 'point up'), Lt('de costat', 'de lado', 'on its side')),
      r"At first the relative frequency changes a lot, but as we toss more it gets closer to 0.62. We say \(P(\text{%s})\approx0.62\) and so \(P(\text{%s})\approx1-0.62=0.38\)." % (Lt('punta amunt', 'punta arriba', 'point up'), Lt('de costat', 'de lado', 'on its side')))
  + note(r"La llei també val per als experiments regulars: el naturalista Buffon va llançar una moneda 4040 vegades i va obtindre 2048 cares (\(h\approx0{,}507\)), i l'estadístic Karl Pearson, 24 000 vegades amb 12 012 cares (\(h=0{,}5005\)). Totes dues s'acosten a \(\frac12\).",
         r"La ley también vale para los experimentos regulares: el naturalista Buffon lanzó una moneda 4040 veces y obtuvo 2048 caras (\(h\approx0{,}507\)), y el estadístico Karl Pearson, 24 000 veces con 12 012 caras (\(h=0{,}5005\)). Las dos se acercan a \(\frac12\).",
         r"The law also holds for regular experiments: the naturalist Buffon tossed a coin 4040 times and got 2048 heads (\(h\approx0.507\)), and the statistician Karl Pearson tossed one 24,000 times and got 12,012 heads (\(h=0.5005\)). Both are close to \(\frac12\).", '📜')
  + widget('w-lgn', '📈', L('Repeteix l\'experiment moltes vegades', 'Repite el experimento muchas veces', 'Repeat the experiment many times'),
           ['<div class="wrow"><div class="seg sg-x" role="group"></div></div>',
            '<div class="wrow"><button class="btn primary" type="button" data-n="1">+1</button><button class="btn primary" type="button" data-n="10">+10</button><button class="btn primary" type="button" data-n="100">+100</button><button class="btn primary" type="button" data-n="1000">+1000</button><button class="btn" type="button" data-a="clr">↺ ' + L('Torna a començar', 'Volver a empezar', 'Start again') + '</button></div>'],
           out='<div class="gout"></div>'))
ck(Fr(2048, 4040), '0,507', 3); ck(Fr(12012, 24000), '0,5005')

s5 += box('prop', L('Fer previsions amb la probabilitat', 'Hacer previsiones con la probabilidad', 'Making predictions with probability'),
  P(r"La llei dels grans nombres també funciona a l'inrevés: si coneixem (o hem estimat) \(P(A)\) i repetim l'experiment \(n\) vegades, esperem que \(A\) ocórrega <strong>aproximadament</strong> \(n\cdot P(A)\) vegades.",
    r"La ley de los grandes números también funciona al revés: si conocemos (o hemos estimado) \(P(A)\) y repetimos el experimento \(n\) veces, esperamos que \(A\) ocurra <strong>aproximadamente</strong> \(n\cdot P(A)\) veces.",
    r"The law of large numbers also works the other way round: if we know (or have estimated) \(P(A)\) and repeat the experiment \(n\) times, we expect \(A\) to happen <strong>about</strong> \(n\cdot P(A)\) times.")
  + ul(L(r"Si llancem un dau 600 vegades, esperem uns \(600\cdot\frac16=100\) sisos (no exactament 100!).", r"Si lanzamos un dado 600 veces, esperamos unos \(600\cdot\frac16=100\) seises (¡no exactamente 100!).", r"If we roll a die 600 times, we expect about \(600\cdot\frac16=100\) sixes (not exactly 100!)."),
       L(r"Si llancem la xinxeta 300 vegades, esperem que caiga amb la punta cap amunt unes \(300\cdot0{,}62=186\) vegades.", r"Si lanzamos la chincheta 300 veces, esperamos que caiga con la punta hacia arriba unas \(300\cdot0{,}62=186\) veces.", r"If we toss the drawing pin 300 times, we expect it to land point up about \(300\cdot0.62=186\) times."))
  + note(r"L'atzar no té memòria. Si una moneda ha eixit creu cinc vegades seguides, la probabilitat que la següent siga cara continua sent \(\frac12\). La llei dels grans nombres parla de moltíssimes repeticions, no de «compensar» les últimes.",
         r"El azar no tiene memoria. Si una moneda ha salido cruz cinco veces seguidas, la probabilidad de que la siguiente sea cara sigue siendo \(\frac12\). La ley de los grandes números habla de muchísimas repeticiones, no de «compensar» las últimas.",
         r"Chance has no memory. If a coin has landed tails five times in a row, the probability that the next toss is heads is still \(\frac12\). The law of large numbers is about a huge number of trials, not about “making up” for the last few.", '🧠')
  + drill('freq', 'Entrena: freqüències i previsions', 'Entrena: frecuencias y previsiones', 'Train: frequencies and predictions'))
ck(600 * Fr(1, 6), 100); ck(300 * Fr(62, 100), 186)

TD = [98, 102, 95, 104, 99, 502]
assert sum(TD) == 1000 and Fr(102 + 104 + 502, 1000) == Fr(708, 1000)
s5 += levels(
 [prob(L(r"Amb les dades de la xinxeta de la taula anterior, estima la probabilitat que caiga de costat. Quantes vegades esperes que caiga de costat si la llances 500 vegades?",
         r"Con los datos de la chincheta de la tabla anterior, estima la probabilidad de que caiga de lado. ¿Cuántas veces esperas que caiga de lado si la lanzas 500 veces?",
         r"Using the drawing-pin data in the table above, estimate the probability that it lands on its side. How many times do you expect it to land on its side if you toss it 500 times?"),
       P(r"Fem servir la freqüència relativa amb més llançaments, 0,621 ≈ 0,62:", r"Usamos la frecuencia relativa con más lanzamientos, 0,621 ≈ 0,62:", r"Use the relative frequency from the most tosses, 0.621 ≈ 0.62:"),
       D(r"P(\text{%s})\approx1-0{,}62=\boxed{0{,}38}\qquad 500\cdot0{,}38=\boxed{190\ \text{%s}}" % (Lt('de costat', 'de lado', 'on its side'), Lt('vegades', 'veces', 'times'))))],
 [prob(L(r"Una jugadora de bàsquet ha encertat 168 dels 240 tirs lliures que ha llançat aquesta temporada. Estima la probabilitat que encerte un tir lliure. Quants n'esperes que encerte en els 50 pròxims?",
         r"Una jugadora de baloncesto ha acertado 168 de los 240 tiros libres que ha lanzado esta temporada. Estima la probabilidad de que acierte un tiro libre. ¿Cuántos esperas que acierte en los 50 próximos?",
         r"A basketball player has scored 168 of the 240 free throws she's taken this season. Estimate the probability that she scores a free throw. How many do you expect her to score in the next 50?"),
       D(r"P(\text{%s})\approx\frac{168}{240}=\boxed{0{,}7}\qquad 50\cdot0{,}7=\boxed{35}" % Lt('encert', 'acierto', 'score'))),
  prob(L(r"En una bossa hi ha 20 boles, roges i blaves, però no sabem quantes de cada color. Traiem una bola, n'anotem el color i la tornem a la bossa. Ho repetim 500 vegades i ix roja 198 vegades. Quantes boles roges deu haver-hi?",
         r"En una bolsa hay 20 bolas, rojas y azules, pero no sabemos cuántas de cada color. Sacamos una bola, anotamos su color y la devolvemos a la bolsa. Lo repetimos 500 veces y sale roja 198 veces. ¿Cuántas bolas rojas debe de haber?",
         r"A bag holds 20 balls, red and blue, but we don't know how many of each. We draw a ball, note its colour and put it back. We do this 500 times and get red 198 times. How many red balls are there likely to be?"),
       D(r"P(R)\approx h(R)=\frac{198}{500}=0{,}396"),
       P(r"Si hi ha \(x\) boles roges, per Laplace \(P(R)=\frac{x}{20}\):", r"Si hay \(x\) bolas rojas, por Laplace \(P(R)=\frac{x}{20}\):", r"If there are \(x\) red balls, by Laplace \(P(R)=\frac{x}{20}\):"),
       D(r"\frac{x}{20}\approx0{,}396\ \Rightarrow\ x\approx20\cdot0{,}396=7{,}92\ \Rightarrow\ \boxed{%s}" % Lt('unes 8 roges i 12 blaves', 'unas 8 rojas y 12 azules', 'about 8 red and 12 blue')))],
 [prob(L(r"Sospitem que un dau està trucat. El llancem 1000 vegades i obtenim: 1 → 98, 2 → 102, 3 → 95, 4 → 104, 5 → 99 i 6 → 502. Estima \(P(6)\) i \(P(\text{parell})\). Està trucat?",
         r"Sospechamos que un dado está trucado. Lo lanzamos 1000 veces y obtenemos: 1 → 98, 2 → 102, 3 → 95, 4 → 104, 5 → 99 y 6 → 502. Estima \(P(6)\) y \(P(\text{par})\). ¿Está trucado?",
         r"We suspect a die is loaded. We roll it 1000 times and get: 1 → 98, 2 → 102, 3 → 95, 4 → 104, 5 → 99 and 6 → 502. Estimate \(P(6)\) and \(P(\text{even})\). Is it loaded?"),
       D(r"P(6)\approx\frac{502}{1000}\approx\boxed{0{,}5}\qquad P(\text{%s})\approx\frac{102+104+502}{1000}=\boxed{0{,}708}" % Lt('parell', 'par', 'even')),
       P(r"En un dau correcte esperaríem uns \(1000\cdot\frac16\approx167\) sisos. Amb 1000 llançaments, 502 sisos és massa lluny: el dau <strong>està trucat</strong> (el 6 ix la meitat de les vegades). Els altres resultats tenen, cadascun, \(P\approx0{,}1\).",
         r"En un dado correcto esperaríamos unos \(1000\cdot\frac16\approx167\) seises. Con 1000 lanzamientos, 502 seises está demasiado lejos: el dado <strong>está trucado</strong> (el 6 sale la mitad de las veces). Los otros resultados tienen, cada uno, \(P\approx0{,}1\).",
         r"With a fair die we'd expect about \(1000\cdot\frac16\approx167\) sixes. With 1000 rolls, 502 sixes is far too many: the die <strong>is loaded</strong> (6 comes up half the time). The other outcomes each have \(P\approx0.1\)."))])
ck(Fr(168, 240), '0,7'); ck(50 * Fr(7, 10), 35); ck(Fr(198, 500), '0,396'); ck(20 * Fr(396, 1000), '7,92'); ck(Fr(1000, 6), 167, 0)
s5 += practice([
  ('★', L(r"a) Llancem un tap de suro 200 vegades i cau dret 46 vegades. Estima la probabilitat que caiga dret i la que no caiga dret.", r"a) Lanzamos un tapón de corcho 200 veces y cae de pie 46 veces. Estima la probabilidad de que caiga de pie y la de que no caiga de pie.", r"a) We toss a cork 200 times and it lands upright 46 times. Estimate the probability that it lands upright and that it doesn't.")),
  ('★★', L(r"b) Quants cincs esperes obtindre si llances un dau 900 vegades? c) Joan diu: «He llançat una moneda 10 vegades i han eixit 7 cares; per tant, \(P(\text{cara})=0{,}7\)». Té raó?", r"b) ¿Cuántos cincos esperas obtener si lanzas un dado 900 veces? c) Juan dice: «He lanzado una moneda 10 veces y han salido 7 caras; por tanto, \(P(\text{cara})=0{,}7\)». ¿Tiene razón?", r"b) How many fives do you expect if you roll a die 900 times? c) Joan says: “I tossed a coin 10 times and got 7 heads, so \(P(\text{heads})=0.7\).” Is he right?")),
  ('★★★', L(r"d) En una bossa hi ha boles blanques i 6 de negres. Traiem una bola i la tornem; després de 400 extraccions, n'han eixit 160 de negres. Quantes boles blanques deu haver-hi?", r"d) En una bolsa hay bolas blancas y 6 negras. Sacamos una bola y la devolvemos; después de 400 extracciones, han salido 160 negras. ¿Cuántas bolas blancas debe de haber?", r"d) A bag has some white balls and 6 black ones. We draw a ball and put it back; after 400 draws, 160 have been black. How many white balls are there likely to be?"))],
  P(r"a) \(\frac{46}{200}=0{,}23\) i \(0{,}77\). b) \(900\cdot\frac16=150\). c) No: 10 llançaments són massa pocs. La moneda és regular i \(P(\text{cara})=0{,}5\); la freqüència relativa s'hi acosta quan fem molts llançaments. d) \(h(N)=\frac{160}{400}=0{,}4\); si hi ha \(n\) boles, \(\frac6n\approx0{,}4\Rightarrow n\approx15\): unes 9 blanques.",
    r"a) \(\frac{46}{200}=0{,}23\) y \(0{,}77\). b) \(900\cdot\frac16=150\). c) No: 10 lanzamientos son demasiado pocos. La moneda es regular y \(P(\text{cara})=0{,}5\); la frecuencia relativa se acerca a ese valor cuando hacemos muchos lanzamientos. d) \(h(N)=\frac{160}{400}=0{,}4\); si hay \(n\) bolas, \(\frac6n\approx0{,}4\Rightarrow n\approx15\): unas 9 blancas.",
    r"a) \(\frac{46}{200}=0.23\) and \(0.77\). b) \(900\cdot\frac16=150\). c) No: 10 tosses are far too few. The coin is regular and \(P(\text{heads})=0.5\); the relative frequency gets close to it with many tosses. d) \(h(B)=\frac{160}{400}=0.4\); if there are \(n\) balls, \(\frac6n\approx0.4\Rightarrow n\approx15\): about 9 white."))
ck(Fr(46, 200), '0,23'); ck(900 * Fr(1, 6), 150); ck(Fr(160, 400), '0,4'); assert Fr(6, 15) == Fr(4, 10)

# =====================================================================
# 12.6 Experiments compostos
# =====================================================================
S7 = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == 7]
assert len(S7) == 6
TC2 = ptree([('C', '1/2', [('C', '1/2', [], 'CC: 1/2 · 1/2 = 1/4'), ('X', '1/2', [], 'CX: 1/4')]), ('X', '1/2', [('C', '1/2', [], 'XC: 1/4'), ('X', '1/2', [], 'XX: 1/4')])], W=330)
s6 = box('def', L('Experiments compostos', 'Experimentos compuestos', 'Compound experiments'),
  P(r"Un experiment és <strong>compost</strong> quan està format per diversos experiments simples, fets alhora o un darrere l'altre: llançar dues monedes, una moneda i un dau, dos daus, traure dues boles d'una bossa…",
    r"Un experimento es <strong>compuesto</strong> cuando está formado por varios experimentos simples, realizados a la vez o uno detrás de otro: lanzar dos monedas, una moneda y un dado, dos dados, sacar dos bolas de una bolsa…",
    r"An experiment is <strong>compound</strong> when it's made up of several simple experiments, done at the same time or one after another: tossing two coins, a coin and a die, two dice, drawing two balls from a bag…")
  + P(r"Per a escriure'n l'espai mostral fem servir un <strong>diagrama d'arbre</strong> o, si són dos experiments, una <strong>taula de doble entrada</strong>. El nombre de resultats és el <strong>producte</strong> dels resultats de cada experiment: moneda i dau, \(2\cdot6=12\); tres monedes, \(2\cdot2\cdot2=8\); dos daus, \(6\cdot6=36\).",
      r"Para escribir su espacio muestral usamos un <strong>diagrama de árbol</strong> o, si son dos experimentos, una <strong>tabla de doble entrada</strong>. El número de resultados es el <strong>producto</strong> de los resultados de cada experimento: moneda y dado, \(2\cdot6=12\); tres monedas, \(2\cdot2\cdot2=8\); dos dados, \(6\cdot6=36\).",
      r"To write its sample space we use a <strong>tree diagram</strong> or, for two experiments, a <strong>two-way table</strong>. The number of outcomes is the <strong>product</strong> of the outcomes of each experiment: coin and die, \(2\cdot6=12\); three coins, \(2\cdot2\cdot2=8\); two dice, \(6\cdot6=36\)."))

s6 += box('prop', L('Dos daus: la taula de doble entrada', 'Dos dados: la tabla de doble entrada', 'Two dice: the two-way table'),
  P(r"En llançar dos daus hi ha 36 resultats equiprobables (el primer dau i el segon es distingeixen: \((2,5)\) i \((5,2)\) són resultats diferents). Si sumem els punts, la taula mostra les 36 sumes. Les caselles marcades són les de suma 7:",
    r"Al lanzar dos dados hay 36 resultados equiprobables (el primer dado y el segundo se distinguen: \((2,5)\) y \((5,2)\) son resultados distintos). Si sumamos los puntos, la tabla muestra las 36 sumas. Las casillas marcadas son las de suma 7:",
    r"Rolling two dice gives 36 equally likely outcomes (the first and second die are different: \((2,5)\) and \((5,2)\) are different outcomes). If we add the scores, the table shows the 36 sums. The highlighted cells are those with sum 7:")
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
ck(Fr(6, 36), Fr(1, 6))

s6 += box('prop', L('Regla del producte (experiments independents)', 'Regla del producto (experimentos independientes)', 'Product rule (independent experiments)'),
  P(r"Dos experiments són <strong>independents</strong> si el resultat del primer no influeix en el del segon (dues monedes, dos daus, una moneda i un dau…). Llavors, en el diagrama d'arbre:",
    r"Dos experimentos son <strong>independientes</strong> si el resultado del primero no influye en el del segundo (dos monedas, dos dados, una moneda y un dado…). Entonces, en el diagrama de árbol:",
    r"Two experiments are <strong>independent</strong> if the result of the first doesn't affect the second (two coins, two dice, a coin and a die…). Then, in the tree diagram:")
  + ol(L(r"Escrivim en cada branca la probabilitat d'aquell resultat.", r"Escribimos en cada rama la probabilidad de ese resultado.", r"Write the probability of each result on its branch."),
       L(r"La probabilitat d'un camí és el <strong>producte</strong> de les probabilitats de les seues branques.", r"La probabilidad de un camino es el <strong>producto</strong> de las probabilidades de sus ramas.", r"The probability of a path is the <strong>product</strong> of the probabilities on its branches."),
       L(r"Si un esdeveniment està format per diversos camins, en <strong>sumem</strong> les probabilitats.", r"Si un suceso está formado por varios caminos, <strong>sumamos</strong> sus probabilidades.", r"If an event is made up of several paths, <strong>add</strong> their probabilities."))
  + figs(TC2)
  + D(r"P(CC)=\frac12\cdot\frac12=\frac14\qquad P(\text{%s})=P(CX)+P(XC)=\frac14+\frac14=\frac12" % Lt('una cara i una creu', 'una cara y una cruz', 'one heads, one tails'))
  + P(r"Les probabilitats de tots els camins sumen 1. I quan es pregunta «almenys un», sovint és més ràpid el contrari: en llançar dos daus,",
      r"Las probabilidades de todos los caminos suman 1. Y cuando se pregunta «al menos uno», a menudo es más rápido el contrario: al lanzar dos dados,",
      r"The probabilities of all the paths add up to 1. And for “at least one”, the complement is often quicker: rolling two dice,")
  + D(r"P(\text{%s})=1-P(\text{%s})=1-\frac56\cdot\frac56=1-\frac{25}{36}=\frac{11}{36}" % (Lt('almenys un 6', 'al menos un 6', 'at least one 6'), Lt('cap 6', 'ningún 6', 'no 6'))))
assert len([1 for a in range(1, 7) for b in range(1, 7) if a == 6 or b == 6]) == 11 and 1 - Fr(5, 6) ** 2 == Fr(11, 36)

TB = ptree([('E', '0,7', [('E', '0,7', [], 'EE: 0,49'), ('F', '0,3', [], 'EF: 0,21')]), ('F', '0,3', [('E', '0,7', [], 'FE: 0,21'), ('F', '0,3', [], 'FF: 0,09')])], W=300)
pe = Fr(7, 10)
assert pe * pe == Fr(49, 100) and 2 * pe * (1 - pe) == Fr(42, 100) and (1 - pe) ** 2 == Fr(9, 100) and Fr(49 + 42 + 9, 100) == 1
assert len([1 for a in range(1, 7) for b in range(1, 7) if a + b == 10]) == 3 and len([1 for a in range(1, 7) for b in range(1, 7) if a + b >= 10]) == 6
assert 1 - Fr(5, 6) ** 3 == Fr(91, 216); ck(Fr(91, 216), '0,42', 2)
s6 += levels(
 [prob(L(r"Llancem una moneda i un dau. Calcula la probabilitat de traure cara i un 6, i la de traure creu i un nombre parell.", r"Lanzamos una moneda y un dado. Calcula la probabilidad de sacar cara y un 6, y la de sacar cruz y un número par.", r"We toss a coin and roll a die. Find the probability of heads and a 6, and of tails and an even number."),
       D(r"P(C\ \text{%s}\ 6)=\frac12\cdot\frac16=\boxed{\frac1{12}}\qquad P(X\ \text{%s}\ \text{%s})=\frac12\cdot\frac36=\boxed{\frac14}" % (Lt('i', 'y', 'and'), Lt('i', 'y', 'and'), Lt('parell', 'par', 'even'))),
       P(r"També per Laplace: hi ha \(2\cdot6=12\) resultats i només un és \(C6\): \(\frac1{12}\ \checkmark\)", r"También por Laplace: hay \(2\cdot6=12\) resultados y solo uno es \(C6\): \(\frac1{12}\ \checkmark\)", r"Also by Laplace: there are \(2\cdot6=12\) outcomes and only one is \(C6\): \(\frac1{12}\ \checkmark\)")),
  prob(L(r"Llancem dos daus i sumem els punts. Calcula la probabilitat que la suma siga 10, que siga 10 o més, i que els dos daus traguen el mateix nombre (doble).", r"Lanzamos dos dados y sumamos los puntos. Calcula la probabilidad de que la suma sea 10, de que sea 10 o más, y de que los dos dados saquen el mismo número (doble).", r"We roll two dice and add the scores. Find the probability that the sum is 10, that it's 10 or more, and that both dice show the same number (a double)."),
       P(r"Mirem la taula: suma 10 en \((4,6),\,(5,5),\,(6,4)\); suma 11 en dues caselles i suma 12 en una. Els dobles són la diagonal (6 caselles).", r"Miramos la tabla: suma 10 en \((4,6),\,(5,5),\,(6,4)\); suma 11 en dos casillas y suma 12 en una. Los dobles son la diagonal (6 casillas).", r"Look at the table: sum 10 at \((4,6),\,(5,5),\,(6,4)\); sum 11 in two cells and sum 12 in one. The doubles are the diagonal (6 cells)."),
       D(r"P(10)=\frac3{36}=\boxed{\frac1{12}}\qquad P(\ge10)=\frac{3+2+1}{36}=\boxed{\frac16}\qquad P(\text{%s})=\frac6{36}=\boxed{\frac16}" % Lt('doble', 'doble', 'double')))],
 [prob(L(r"Una jugadora encerta el 70 % dels tirs lliures. En llança dos (l'un no influeix en l'altre). Calcula la probabilitat que n'encerte tots dos, que no n'encerte cap i que n'encerte exactament un.",
         r"Una jugadora acierta el 70 % de los tiros libres. Lanza dos (uno no influye en el otro). Calcula la probabilidad de que acierte los dos, de que no acierte ninguno y de que acierte exactamente uno.",
         r"A player scores 70 % of her free throws. She takes two (one doesn't affect the other). Find the probability that she scores both, neither, and exactly one."),
       P(r"\(E\) = encert, \(F\) = fallada. Fem l'arbre:", r"\(E\) = acierto, \(F\) = fallo. Hacemos el árbol:", r"\(E\) = score, \(F\) = miss. Draw the tree:") + figs(TB),
       D(r"P(EE)=0{,}7\cdot0{,}7=\boxed{0{,}49}\qquad P(FF)=0{,}3\cdot0{,}3=\boxed{0{,}09}"),
       D(r"P(\text{%s})=P(EF)+P(FE)=0{,}21+0{,}21=\boxed{0{,}42}" % Lt('exactament un', 'exactamente uno', 'exactly one')),
       P(r"Comprovació: \(0{,}49+0{,}42+0{,}09=1\ \checkmark\)", r"Comprobación: \(0{,}49+0{,}42+0{,}09=1\ \checkmark\)", r"Check: \(0.49+0.42+0.09=1\ \checkmark\)"))],
 [prob(L(r"Llancem un dau tres vegades. Quina és la probabilitat de traure almenys un 6?", r"Lanzamos un dado tres veces. ¿Cuál es la probabilidad de sacar al menos un 6?", r"We roll a die three times. What is the probability of getting at least one 6?"),
       P(r"«Almenys un 6» té molts casos (un, dos o tres sisos). El contrari és «cap 6», que és un sol camí de l'arbre:", r"«Al menos un 6» tiene muchos casos (uno, dos o tres seises). El contrario es «ningún 6», que es un solo camino del árbol:", r"“At least one 6” has many cases (one, two or three sixes). Its complement, “no 6”, is a single path in the tree:"),
       D(r"P(\text{%s})=\frac56\cdot\frac56\cdot\frac56=\frac{125}{216}" % Lt('cap 6', 'ningún 6', 'no 6')),
       D(r"P(\text{%s})=1-\frac{125}{216}=\boxed{\frac{91}{216}}\approx0{,}42" % Lt('almenys un 6', 'al menos un 6', 'at least one 6')),
       note(r"No és \(\frac16+\frac16+\frac16=\frac12\): aquesta suma compta més d'una vegada els casos amb dos o tres sisos.", r"No es \(\frac16+\frac16+\frac16=\frac12\): esa suma cuenta más de una vez los casos con dos o tres seises.", r"It isn't \(\frac16+\frac16+\frac16=\frac12\): that sum counts the cases with two or three sixes more than once.", '⚠️'))])
s6 += practice([
  ('★', L(r"a) Llancem dues monedes. Quina és la probabilitat de traure dues creus? b) Llancem dos daus: quina és la probabilitat que la suma siga 5?", r"a) Lanzamos dos monedas. ¿Cuál es la probabilidad de sacar dos cruces? b) Lanzamos dos dados: ¿cuál es la probabilidad de que la suma sea 5?", r"a) We toss two coins. What is the probability of two tails? b) We roll two dice: what is the probability that the sum is 5?")),
  ('★★', L(r"c) Llancem tres monedes. Calcula la probabilitat de traure exactament dues cares. d) Girem dues vegades una ruleta amb 4 sectors iguals (1, 2, 3 i 4). Quina és la probabilitat que el producte siga parell?", r"c) Lanzamos tres monedas. Calcula la probabilidad de sacar exactamente dos caras. d) Giramos dos veces una ruleta con 4 sectores iguales (1, 2, 3 y 4). ¿Cuál es la probabilidad de que el producto sea par?", r"c) We toss three coins. Find the probability of exactly two heads. d) We spin a wheel with 4 equal sectors (1, 2, 3 and 4) twice. What is the probability that the product is even?")),
  ('★★★', L(r"e) Un examen té 4 preguntes de vertader o fals. Si les contestes totes a l'atzar, quina és la probabilitat d'encertar-ne almenys una?", r"e) Un examen tiene 4 preguntas de verdadero o falso. Si las contestas todas al azar, ¿cuál es la probabilidad de acertar al menos una?", r"e) A test has 4 true-or-false questions. If you answer them all at random, what is the probability of getting at least one right?"))],
  P(r"a) \(\frac14\). b) \(\frac4{36}=\frac19\). c) \(CCX,\,CXC,\,XCC\): \(\frac38\). d) Contrari: els dos senars, \(\frac24\cdot\frac24=\frac14\); \(P=1-\frac14=\frac34\). e) \(1-\left(\frac12\right)^4=1-\frac1{16}=\frac{15}{16}\).",
    r"a) \(\frac14\). b) \(\frac4{36}=\frac19\). c) \(CCX,\,CXC,\,XCC\): \(\frac38\). d) Contrario: los dos impares, \(\frac24\cdot\frac24=\frac14\); \(P=1-\frac14=\frac34\). e) \(1-\left(\frac12\right)^4=1-\frac1{16}=\frac{15}{16}\).",
    r"a) \(\frac14\). b) \(\frac4{36}=\frac19\). c) \(CCX,\,CXC,\,XCC\): \(\frac38\). d) Complement: both odd, \(\frac24\cdot\frac24=\frac14\); \(P=1-\frac14=\frac34\). e) \(1-\left(\frac12\right)^4=1-\frac1{16}=\frac{15}{16}\)."))
assert len([1 for a in range(1, 7) for b in range(1, 7) if a + b == 5]) == 4
assert Fr(len([1 for a in range(1, 5) for b in range(1, 5) if a * b % 2 == 0]), 16) == Fr(3, 4) and 1 - Fr(1, 16) == Fr(15, 16)
