# Apartats 9.1-9.3 dels apunts de la Unitat 9 de 4t ESO Matemàtiques A (Estadística): població, mostra i variables,
# taules de freqüències amb dades aïllades i taules amb dades agrupades en intervals. Fet a partir de ../1eso-t10/s123.py:
# 9.1 és el 10.1 de 1r amb el mostreig; 9.2 ajunta el 10.2 i la primera part del 10.3; 9.3 és la segona part del 10.3 amb la
# construcció dels intervals.
from comu import *

# =====================================================================
# 9.1 Població, mostra i variables estadístiques
# =====================================================================
QUAL, DISC, CONT = (L('Qualitativa', 'Cualitativa', 'Qualitative'), L('Quantitativa discreta', 'Cuantitativa discreta', 'Discrete quantitative'),
                    L('Quantitativa contínua', 'Cuantitativa continua', 'Continuous quantitative'))
s1 = box('def', L('Què és l’estadística?', '¿Qué es la estadística?', 'What is statistics?'),
  P(r"L'<strong>estadística</strong> és la part de les matemàtiques que <strong>arreplega</strong>, <strong>ordena</strong>, <strong>representa</strong> i <strong>interpreta</strong> dades per a traure'n conclusions. Abans de començar un estudi estadístic cal tindre clars aquests conceptes:",
    r"La <strong>estadística</strong> es la parte de las matemáticas que <strong>recoge</strong>, <strong>ordena</strong>, <strong>representa</strong> e <strong>interpreta</strong> datos para sacar conclusiones. Antes de empezar un estudio estadístico hay que tener claros estos conceptos:",
    r"<strong>Statistics</strong> is the part of mathematics that <strong>collects</strong>, <strong>organises</strong>, <strong>displays</strong> and <strong>interprets</strong> data to draw conclusions. Before starting a statistical study we need these ideas:")
  + ul(L(r"<strong>Població</strong>: el conjunt de <strong>tots</strong> els elements que volem estudiar.", r"<strong>Población</strong>: el conjunto de <strong>todos</strong> los elementos que queremos estudiar.", r"<strong>Population</strong>: the set of <strong>all</strong> the things we want to study."),
       L(r"<strong>Individu</strong>: cadascun dels elements de la població (una persona, un animal, un objecte…).", r"<strong>Individuo</strong>: cada uno de los elementos de la población (una persona, un animal, un objeto…).", r"<strong>Individual</strong>: each member of the population (a person, an animal, an object…)."),
       L(r"<strong>Mostra</strong>: una <strong>part</strong> de la població que triem per a fer l'estudi quan no podem preguntar a tothom. El nombre d'individus de la mostra és la seua <strong>grandària</strong>.",
         r"<strong>Muestra</strong>: una <strong>parte</strong> de la población que elegimos para hacer el estudio cuando no podemos preguntar a todos. El número de individuos de la muestra es su <strong>tamaño</strong>.",
         r"<strong>Sample</strong>: a <strong>part</strong> of the population that we choose for the study when we can't ask everybody. The number of individuals in the sample is its <strong>size</strong>."))
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"Volem saber quantes hores dormen els 600 alumnes d'un institut. Preguntem a 60 alumnes triats a l'atzar de tots els cursos.",
          r"Queremos saber cuántas horas duermen los 600 alumnos de un instituto. Preguntamos a 60 alumnos elegidos al azar de todos los cursos.",
          r"We want to know how many hours the 600 students of a school sleep. We ask 60 students chosen at random from every year group.")
        + ul(L(r"Població: els 600 alumnes de l'institut. &nbsp; Individu: cada alumne.", r"Población: los 600 alumnos del instituto. &nbsp; Individuo: cada alumno.", r"Population: the 600 students of the school. &nbsp; Individual: each student."),
             L(r"Mostra: els 60 alumnes enquestats (grandària 60).", r"Muestra: los 60 alumnos encuestados (tamaño 60).", r"Sample: the 60 students surveyed (size 60).")))
  + note(r"Una mostra ha de ser <strong>representativa</strong>: s'ha d'assemblar a la població. Si només preguntem als alumnes de 2n de Batxillerat la víspera d'un examen, les conclusions no valdran per a tot l'institut.",
         r"Una muestra tiene que ser <strong>representativa</strong>: tiene que parecerse a la población. Si solo preguntamos a los alumnos de 2º de Bachillerato la víspera de un examen, las conclusiones no valdrán para todo el instituto.",
         r"A sample must be <strong>representative</strong>: it must look like the population. If we only ask final-year students the night before an exam, the conclusions won't hold for the whole school.", '⚠️'))

s1 += box('prop', L('Variables estadístiques', 'Variables estadísticas', 'Statistical variables'),
  P(r"La <strong>variable estadística</strong> és la característica que estudiem en cada individu (el color preferit, el nombre de germans, l'alçada…). Pot ser de tres tipus:",
    r"La <strong>variable estadística</strong> es la característica que estudiamos en cada individuo (el color preferido, el número de hermanos, la altura…). Puede ser de tres tipos:",
    r"The <strong>statistical variable</strong> is the feature we study in each individual (favourite colour, number of siblings, height…). There are three types:")
  + ul(L(r"<strong>Qualitativa</strong>: els seus valors <strong>no són nombres</strong>, sinó qualitats. Exemples: color preferit, esport, tipus de mascota, mes de naixement.",
         r"<strong>Cualitativa</strong>: sus valores <strong>no son números</strong>, sino cualidades. Ejemplos: color preferido, deporte, tipo de mascota, mes de nacimiento.",
         r"<strong>Qualitative</strong>: its values <strong>are not numbers</strong> but qualities. Examples: favourite colour, sport, type of pet, month of birth."),
       L(r"<strong>Quantitativa discreta</strong>: els valors són nombres que s'obtenen <strong>comptant</strong>; només pot prendre valors aïllats (0, 1, 2…). Exemples: nombre de germans, gols en un partit, llibres llegits.",
         r"<strong>Cuantitativa discreta</strong>: los valores son números que se obtienen <strong>contando</strong>; solo puede tomar valores aislados (0, 1, 2…). Ejemplos: número de hermanos, goles en un partido, libros leídos.",
         r"<strong>Discrete quantitative</strong>: the values are numbers we get by <strong>counting</strong>; it only takes separate values (0, 1, 2…). Examples: number of siblings, goals in a match, books read."),
       L(r"<strong>Quantitativa contínua</strong>: els valors són nombres que s'obtenen <strong>mesurant</strong>; entre dos valors sempre n'hi pot haver un altre. Exemples: alçada, pes, temps, temperatura.",
         r"<strong>Cuantitativa continua</strong>: los valores son números que se obtienen <strong>midiendo</strong>; entre dos valores siempre puede haber otro. Ejemplos: altura, peso, tiempo, temperatura.",
         r"<strong>Continuous quantitative</strong>: the values are numbers we get by <strong>measuring</strong>; between two values there can always be another. Examples: height, weight, time, temperature."))
  + tbl([L('Variable', 'Variable', 'Variable'), L('Valors possibles', 'Valores posibles', 'Possible values'), L('Tipus', 'Tipo', 'Type')],
        [[L('Esport preferit', 'Deporte preferido', 'Favourite sport'), L('futbol, bàsquet, natació…', 'fútbol, baloncesto, natación…', 'football, basketball, swimming…'), QUAL],
         [L('Nombre de germans', 'Número de hermanos', 'Number of siblings'), '0, 1, 2, 3…', DISC],
         [L('Alçada (cm)', 'Altura (cm)', 'Height (cm)'), L('152; 152,5; 152,37…', '152; 152,5; 152,37…', '152; 152.5; 152.37…'), CONT]])
  + note(r"Truc: pregunta't <strong>«es compta o es mesura?»</strong>. Si es compta, és discreta; si es mesura (amb regle, rellotge, balança, termòmetre…), és contínua.",
         r"Truco: pregúntate <strong>«¿se cuenta o se mide?»</strong>. Si se cuenta, es discreta; si se mide (con regla, reloj, báscula, termómetro…), es continua.",
         r"Tip: ask yourself <strong>“is it counted or measured?”</strong>. If it's counted, it's discrete; if it's measured (with a ruler, clock, scales, thermometer…), it's continuous.")
  + drill('tipus', 'Entrena: de quin tipus és la variable?', 'Entrena: ¿de qué tipo es la variable?', 'Train: what type of variable is it?', 'opts')
  + drill('pobmos', 'Entrena: població o mostra?', 'Entrena: ¿población o muestra?', 'Train: population or sample?', 'opts'))

# mostreig (nou a 4t)
CUR = [('1r', 150), ('2n', 120), ('3r', 130), ('4t', 100)]
NCUR = sum(n for _, n in CUR); assert NCUR == 500
EST = [Fr(50 * n, NCUR) for _, n in CUR]; assert EST == [15, 12, 13, 10] and sum(EST) == 50
s1 += box('prop', L('Com es tria una mostra?', '¿Cómo se elige una muestra?', 'How do we choose a sample?'),
  P(r"Triar els individus de la mostra s'anomena <strong>mostreig</strong>. Perquè la mostra siga representativa, els individus s'han de triar <strong>a l'atzar</strong>. Hi ha diverses maneres de fer-ho:",
    r"Elegir los individuos de la muestra se llama <strong>muestreo</strong>. Para que la muestra sea representativa, los individuos se tienen que elegir <strong>al azar</strong>. Hay varias maneras de hacerlo:",
    r"Choosing the individuals of the sample is called <strong>sampling</strong>. For the sample to be representative, the individuals must be chosen <strong>at random</strong>. There are several ways to do it:")
  + ul(L(r"<strong>Aleatori simple</strong>: tots els individus tenen la mateixa probabilitat d'eixir, com en un sorteig (per exemple, traient números de la llista de l'alumnat).",
         r"<strong>Aleatorio simple</strong>: todos los individuos tienen la misma probabilidad de salir, como en un sorteo (por ejemplo, sacando números de la lista del alumnado).",
         r"<strong>Simple random</strong>: every individual has the same chance of being picked, like in a draw (for example, drawing numbers from the class list)."),
       L(r"<strong>Sistemàtic</strong>: triem a l'atzar el primer i després, un de cada \(k\) (per exemple, un de cada 10 alumnes de la llista).",
         r"<strong>Sistemático</strong>: elegimos al azar el primero y después, uno de cada \(k\) (por ejemplo, uno de cada 10 alumnos de la lista).",
         r"<strong>Systematic</strong>: pick the first one at random and then one in every \(k\) (for example, one in every 10 students on the list)."),
       L(r"<strong>Estratificat</strong>: dividim la població en grups (estrats: cursos, edats…) i triem de cada grup un nombre d'individus <strong>proporcional</strong> a la seua grandària.",
         r"<strong>Estratificado</strong>: dividimos la población en grupos (estratos: cursos, edades…) y elegimos de cada grupo un número de individuos <strong>proporcional</strong> a su tamaño.",
         r"<strong>Stratified</strong>: split the population into groups (strata: year groups, ages…) and pick from each group a number of individuals <strong>proportional</strong> to its size."))
  + box('ex', L('Exemple: mostreig estratificat', 'Ejemplo: muestreo estratificado', 'Example: stratified sampling'),
        P(r"Un institut d'ESO té 500 alumnes: 150 de 1r, 120 de 2n, 130 de 3r i 100 de 4t. Volem una mostra de 50 alumnes en què cada curs tinga el pes que li toca. Com que \(\frac{50}{500}=\frac1{10}\), agafem la desena part de cada curs:",
          r"Un instituto de ESO tiene 500 alumnos: 150 de 1º, 120 de 2º, 130 de 3º y 100 de 4º. Queremos una muestra de 50 alumnos en la que cada curso tenga el peso que le corresponde. Como \(\frac{50}{500}=\frac1{10}\), cogemos la décima parte de cada curso:",
          r"A secondary school has 500 students: 150 in Year 7, 120 in Year 8, 130 in Year 9 and 100 in Year 10. We want a sample of 50 students in which each year group has its fair weight. Since \(\frac{50}{500}=\frac1{10}\), we take a tenth of each year group:")
        + D(r"\tri{1r}{1º}{Y7}:\ \tfrac{150}{10}=15\qquad \tri{2n}{2º}{Y8}:\ \tfrac{120}{10}=12\qquad \tri{3r}{3º}{Y9}:\ \tfrac{130}{10}=13\qquad \tri{4t}{4º}{Y10}:\ \tfrac{100}{10}=10")
        + P(r"En total, \(15+12+13+10=50\) alumnes. Dins de cada curs, els triem a l'atzar.", r"En total, \(15+12+13+10=50\) alumnos. Dentro de cada curso, los elegimos al azar.", r"In total, \(15+12+13+10=50\) students. Within each year group, we choose them at random.")))

s1 += levels(
 [prob(L(r"Per a conéixer l'opinió dels 1&nbsp;200 veïns d'un poble sobre un nou parc, l'ajuntament pregunta a 150 veïns. Indica la població, la mostra, un individu i la variable estudiada.",
         r"Para conocer la opinión de los 1&nbsp;200 vecinos de un pueblo sobre un nuevo parque, el ayuntamiento pregunta a 150 vecinos. Indica la población, la muestra, un individuo y la variable estudiada.",
         r"To find out what the 1,200 residents of a village think about a new park, the council asks 150 residents. State the population, the sample, an individual and the variable studied."),
       ul(L(r"Població: els <strong>1&nbsp;200 veïns</strong> del poble.", r"Población: los <strong>1&nbsp;200 vecinos</strong> del pueblo.", r"Population: the <strong>1,200 residents</strong> of the village."),
          L(r"Mostra: els <strong>150 veïns</strong> preguntats (grandària 150).", r"Muestra: los <strong>150 vecinos</strong> preguntados (tamaño 150).", r"Sample: the <strong>150 residents</strong> asked (size 150)."),
          L(r"Individu: <strong>cada veí</strong>. &nbsp; Variable: l'<strong>opinió sobre el parc</strong> (qualitativa).", r"Individuo: <strong>cada vecino</strong>. &nbsp; Variable: la <strong>opinión sobre el parque</strong> (cualitativa).", r"Individual: <strong>each resident</strong>. &nbsp; Variable: <strong>their opinion of the park</strong> (qualitative)."))),
  prob(L(r"Classifica aquestes variables: a) nombre de mascotes; b) temps que tardes a arribar a l'institut; c) color dels ulls; d) nombre de missatges enviats en un dia; e) pes d'una motxilla; f) gènere musical preferit.",
         r"Clasifica estas variables: a) número de mascotas; b) tiempo que tardas en llegar al instituto; c) color de los ojos; d) número de mensajes enviados en un día; e) peso de una mochila; f) género musical preferido.",
         r"Classify these variables: a) number of pets; b) time it takes you to get to school; c) eye colour; d) number of messages sent in a day; e) weight of a school bag; f) favourite type of music."),
       P(r"Pensem si el valor és un nombre i, si ho és, si es compta o es mesura:", r"Pensamos si el valor es un número y, si lo es, si se cuenta o se mide:", r"Think whether the value is a number and, if so, whether it is counted or measured:"),
       ul(L(r"a) es compta → <strong>discreta</strong>; &nbsp; b) es mesura amb el rellotge → <strong>contínua</strong>; &nbsp; c) no és un nombre → <strong>qualitativa</strong>.",
            r"a) se cuenta → <strong>discreta</strong>; &nbsp; b) se mide con el reloj → <strong>continua</strong>; &nbsp; c) no es un número → <strong>cualitativa</strong>.",
            r"a) counted → <strong>discrete</strong>; &nbsp; b) measured with a clock → <strong>continuous</strong>; &nbsp; c) not a number → <strong>qualitative</strong>."),
          L(r"d) es compta → <strong>discreta</strong>; &nbsp; e) es mesura amb una balança → <strong>contínua</strong>; &nbsp; f) <strong>qualitativa</strong>.",
            r"d) se cuenta → <strong>discreta</strong>; &nbsp; e) se mide con una báscula → <strong>continua</strong>; &nbsp; f) <strong>cualitativa</strong>.",
            r"d) counted → <strong>discrete</strong>; &nbsp; e) measured with scales → <strong>continuous</strong>; &nbsp; f) <strong>qualitative</strong>.")))],
 [prob(L(r"Una fàbrica fa 10&nbsp;000 bombetes al dia i vol saber quantes hores duren. Per què no pot estudiar tota la població? Què ha de fer?",
         r"Una fábrica hace 10&nbsp;000 bombillas al día y quiere saber cuántas horas duran. ¿Por qué no puede estudiar toda la población? ¿Qué tiene que hacer?",
         r"A factory makes 10,000 light bulbs a day and wants to know how many hours they last. Why can't it study the whole population? What should it do?"),
       P(r"Per a saber quant dura una bombeta cal tindre-la encesa fins que es fon: si les provara totes, <strong>no en quedaria cap per a vendre</strong>. A més, seria molt car i lent.",
         r"Para saber cuánto dura una bombilla hay que tenerla encendida hasta que se funde: si las probara todas, <strong>no quedaría ninguna para vender</strong>. Además, sería muy caro y lento.",
         r"To know how long a bulb lasts you must leave it on until it burns out: if it tested them all, <strong>none would be left to sell</strong>. It would also be very expensive and slow."),
       P(r"Ha de triar una <strong>mostra</strong> a l'atzar (per exemple, 50 bombetes de diferents hores i màquines) i estudiar-ne la durada, que és una variable <strong>quantitativa contínua</strong>.",
         r"Tiene que elegir una <strong>muestra</strong> al azar (por ejemplo, 50 bombillas de diferentes horas y máquinas) y estudiar su duración, que es una variable <strong>cuantitativa continua</strong>.",
         r"It should pick a random <strong>sample</strong> (for example, 50 bulbs from different times and machines) and study how long they last, a <strong>continuous quantitative</strong> variable.")),
  prob(L(r"Per a saber quin és l'esport preferit dels joves d'una ciutat, Marc pregunta a 40 persones que ixen d'un partit de bàsquet. És una bona mostra?",
         r"Para saber cuál es el deporte preferido de los jóvenes de una ciudad, Marc pregunta a 40 personas que salen de un partido de baloncesto. ¿Es una buena muestra?",
         r"To find out the favourite sport of a city's young people, Marc asks 40 people coming out of a basketball game. Is it a good sample?"),
       P(r"<strong>No</strong>: la mostra <strong>no és representativa</strong>. Els qui van a un partit de bàsquet segurament prefereixen el bàsquet, i el resultat eixirà inflat. Caldria preguntar a joves triats a l'atzar en llocs diferents.",
         r"<strong>No</strong>: la muestra <strong>no es representativa</strong>. Quienes van a un partido de baloncesto seguramente prefieren el baloncesto, y el resultado saldrá inflado. Habría que preguntar a jóvenes elegidos al azar en lugares diferentes.",
         r"<strong>No</strong>: the sample <strong>is not representative</strong>. People at a basketball game probably prefer basketball, so the result will be inflated. We should ask young people chosen at random in different places."))],
 [prob(L(r"Una empresa té 600 treballadors: 360 a la fàbrica, 180 a les oficines i 60 en la botiga. Vol fer una enquesta a 40 treballadors amb un mostreig estratificat. Quants n'ha de triar de cada lloc?",
         r"Una empresa tiene 600 trabajadores: 360 en la fábrica, 180 en las oficinas y 60 en la tienda. Quiere hacer una encuesta a 40 trabajadores con un muestreo estratificado. ¿Cuántos tiene que elegir de cada lugar?",
         r"A company has 600 workers: 360 in the factory, 180 in the offices and 60 in the shop. It wants to survey 40 workers using stratified sampling. How many should it choose from each place?"),
       P(r"Cada lloc ha d'aportar a la mostra la mateixa proporció que té en l'empresa. La fracció de la població que entra en la mostra és \(\frac{40}{600}=\frac{1}{15}\):",
         r"Cada lugar tiene que aportar a la muestra la misma proporción que tiene en la empresa. La fracción de la población que entra en la muestra es \(\frac{40}{600}=\frac{1}{15}\):",
         r"Each place must contribute to the sample the same proportion it has in the company. The fraction of the population that goes into the sample is \(\frac{40}{600}=\frac{1}{15}\):"),
       D(r"\tri{fàbrica}{fábrica}{factory}:\ \tfrac{360}{15}=\boxed{24}\qquad \tri{oficines}{oficinas}{offices}:\ \tfrac{180}{15}=\boxed{12}\qquad \tri{botiga}{tienda}{shop}:\ \tfrac{60}{15}=\boxed{4}"),
       P(r"Comprovem: \(24+12+4=40\).", r"Comprobamos: \(24+12+4=40\).", r"Check: \(24+12+4=40\).")),
  prob(L(r"Vols fer un estudi sobre l'alumnat de la teua classe. Proposa una variable de cada tipus i escriu tres valors possibles de cadascuna.",
         r"Quieres hacer un estudio sobre el alumnado de tu clase. Propón una variable de cada tipo y escribe tres valores posibles de cada una.",
         r"You want to do a study about the students in your class. Suggest one variable of each type and write three possible values for each."),
       P(r"Hi ha moltes respostes vàlides. Per exemple:", r"Hay muchas respuestas válidas. Por ejemplo:", r"There are many valid answers. For example:"),
       ul(L(r"Qualitativa: <em>assignatura preferida</em> → Matemàtiques, Música, Educació Física.", r"Cualitativa: <em>asignatura preferida</em> → Matemáticas, Música, Educación Física.", r"Qualitative: <em>favourite subject</em> → Maths, Music, PE."),
          L(r"Discreta: <em>nombre de cosins</em> → 0, 4, 7.", r"Discreta: <em>número de primos</em> → 0, 4, 7.", r"Discrete: <em>number of cousins</em> → 0, 4, 7."),
          L(r"Contínua: <em>temps de son d'ahir (h)</em> → 7,5; 8; 9,25.", r"Continua: <em>tiempo de sueño de ayer (h)</em> → 7,5; 8; 9,25.", r"Continuous: <em>hours slept last night</em> → 7.5; 8; 9.25.")))])
s1 += practice([('★☆☆', L(r"Classifica: a) talla de samarreta (S, M, L…); b) nombre de pisos d'un edifici; c) longitud d'un riu; d) marca del mòbil.",
                          r"Clasifica: a) talla de camiseta (S, M, L…); b) número de pisos de un edificio; c) longitud de un río; d) marca del móvil.",
                          r"Classify: a) T-shirt size (S, M, L…); b) number of floors in a building; c) length of a river; d) phone brand.")),
                ('★★☆', L(r"Per a saber quants llibres llegeixen a l'any els 300 alumnes de 4t d'ESO d'una ciutat, se'n pregunta a 45. Quina és la població? I la mostra? De quin tipus és la variable?",
                          r"Para saber cuántos libros leen al año los 300 alumnos de 4º de ESO de una ciudad, se pregunta a 45. ¿Cuál es la población? ¿Y la muestra? ¿De qué tipo es la variable?",
                          r"To find out how many books the 300 Year 10 students of a town read a year, 45 of them are asked. What is the population? And the sample? What type of variable is it?"))],
               L(r"1) a) qualitativa (no és un nombre); b) discreta; c) contínua; d) qualitativa. &nbsp; 2) Població: els 300 alumnes; mostra: els 45 preguntats; variable quantitativa discreta.",
                 r"1) a) cualitativa (no es un número); b) discreta; c) continua; d) cualitativa. &nbsp; 2) Población: los 300 alumnos; muestra: los 45 preguntados; variable cuantitativa discreta.",
                 r"1) a) qualitative (not a number); b) discrete; c) continuous; d) qualitative. &nbsp; 2) Population: the 300 students; sample: the 45 asked; discrete quantitative variable."))

ck(Fr(360, 15), 24); ck(Fr(180, 15), 12); ck(Fr(60, 15), 4)

# =====================================================================
# 9.2 Taules de freqüències amb dades aïllades
# =====================================================================
GERM = [1, 2, 0, 1, 1, 3, 2, 1, 0, 2, 1, 1, 4, 0, 2, 1, 3, 1, 2, 1]
TG = freqs(GERM); NG = len(GERM)
assert TG == [(0, 3), (1, 9), (2, 5), (3, 2), (4, 1)] and NG == 20
def row_rel(x, f, N, xl=None):
    h = Fr(f, N)
    return [xl if xl is not None else M(str(x)), tally(f), M(str(f)), M(r'\frac{%d}{%d}=%s' % (f, N, tn(h))), M(tn(100 * h) + r'\ \%')]
HREL = [L('Valor', 'Valor', 'Value') + ' ' + M('x_i'), L('Recompte', 'Recuento', 'Tally'), M('f_i'), M('h_i'), '%']
TOT = lambda N: ['<strong>' + L('Total', 'Total', 'Total') + '</strong>', '', M(r'N=%d' % N), M('1'), M(r'100\ \%')]
ck(sum(f for _, f in TG), 20); ck(sum(Fr(f, NG) for _, f in TG), 1)

s2 = box('def', L('Freqüència absoluta i freqüència relativa', 'Frecuencia absoluta y frecuencia relativa', 'Absolute and relative frequency'),
  P(r"Quan tenim les dades, el primer és <strong>comptar</strong> quantes vegades apareix cada valor. Per a no equivocar-nos fem un <strong>recompte</strong> amb palets: una ratlla per dada, i la cinquena travessa les quatre anteriors.",
    r"Cuando tenemos los datos, lo primero es <strong>contar</strong> cuántas veces aparece cada valor. Para no equivocarnos hacemos un <strong>recuento</strong> con palotes: una raya por dato, y la quinta tacha las cuatro anteriores.",
    r"Once we have the data, the first step is to <strong>count</strong> how many times each value appears. To avoid mistakes we keep a <strong>tally</strong>: one stroke per data value, and every fifth stroke crosses the previous four.")
  + ul(L(r"La <strong>freqüència absoluta</strong> \(f_i\) d'un valor és el <strong>nombre de vegades</strong> que apareix. La suma de totes és el nombre total de dades, \(N\).",
         r"La <strong>frecuencia absoluta</strong> \(f_i\) de un valor es el <strong>número de veces</strong> que aparece. La suma de todas es el número total de datos, \(N\).",
         r"The <strong>absolute frequency</strong> \(f_i\) of a value is the <strong>number of times</strong> it appears. They all add up to the total number of data, \(N\)."),
       L(r"La <strong>freqüència relativa</strong> \(h_i\) és la part del total que representa: \(h_i=\dfrac{f_i}{N}\). Es pot escriure com a fracció, com a decimal o com a <strong>percentatge</strong> (\(h_i\cdot 100\)). La suma de totes és 1 (el 100&nbsp;%).",
         r"La <strong>frecuencia relativa</strong> \(h_i\) es la parte del total que representa: \(h_i=\dfrac{f_i}{N}\). Se puede escribir como fracción, como decimal o como <strong>porcentaje</strong> (\(h_i\cdot 100\)). La suma de todas es 1 (el 100&nbsp;%).",
         r"The <strong>relative frequency</strong> \(h_i\) is the fraction of the total it represents: \(h_i=\dfrac{f_i}{N}\). It can be written as a fraction, a decimal or a <strong>percentage</strong> (\(h_i\cdot 100\)). They all add up to 1 (100&nbsp;%)."))
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"Hem preguntat a 20 alumnes quants germans tenen:", r"Hemos preguntado a 20 alumnos cuántos hermanos tienen:", r"We asked 20 students how many siblings they have:")
        + '<p class="dlist">' + ' &nbsp; '.join(str(x) for x in GERM) + '</p>'
        + tbl(HREL, [row_rel(x, f, NG) for x, f in TG] + [TOT(NG)], 'c freq')
        + P(r"Per exemple, 9 dels 20 alumnes tenen un germà: \(h=\frac{9}{20}=0\dc 45\), és a dir, el \(45\ \%\).",
            r"Por ejemplo, 9 de los 20 alumnos tienen un hermano: \(h=\frac{9}{20}=0\dc 45\), es decir, el \(45\ \%\).",
            r"For example, 9 of the 20 students have one sibling: \(h=\frac{9}{20}=0\dc 45\), that is, \(45\ \%\)."))
  + note(r"Comprova sempre que la suma de les \(f_i\) és \(N\) i la dels percentatges, \(100\ \%\): així saps que no t'has deixat cap dada.",
         r"Comprueba siempre que la suma de las \(f_i\) es \(N\) y la de los porcentajes, \(100\ \%\): así sabes que no te has dejado ningún dato.",
         r"Always check that the \(f_i\) add up to \(N\) and the percentages to \(100\ \%\): that way you know you haven't missed any data.", '✅')
  + widget('w-dice', '🎲', L('Llança un dau', 'Lanza un dado', 'Roll a die'),
           ['<p class="hint-s">' + L("Llança el dau moltes vegades: cada cara té la mateixa probabilitat. Què passa amb les freqüències relatives quan fas molts llançaments?",
                                     "Lanza el dado muchas veces: cada cara tiene la misma probabilidad. ¿Qué pasa con las frecuencias relativas cuando haces muchos lanzamientos?",
                                     "Roll the die many times: every face is equally likely. What happens to the relative frequencies when you roll a lot?") + '</p>',
            '<div class="wrow"><button class="btn primary" type="button" data-a="1">+1</button><button class="btn" type="button" data-a="10">+10</button><button class="btn" type="button" data-a="100">+100</button><button class="btn" type="button" data-a="1000">+1000</button><button class="btn" type="button" data-a="0">↺</button></div>'])
  + drill('freq', 'Entrena: compta la freqüència absoluta', 'Entrena: cuenta la frecuencia absoluta', 'Train: count the absolute frequency')
  + drill('rel', 'Entrena: freqüència relativa i percentatge', 'Entrena: frecuencia relativa y porcentaje', 'Train: relative frequency and percentage'))

NOT = [(4, 2), (5, 5), (6, 6), (7, 5), (8, 4), (9, 2), (10, 1)]
NN = sum(f for _, f in NOT); assert NN == 25
def acc(tab):
    s, out = 0, []
    for _, f in tab: s += f; out.append(s)
    return out
FN = acc(NOT); assert FN == [2, 7, 13, 18, 22, 24, 25]
HF = [M('x_i'), M('f_i'), M('F_i'), M('h_i'), M('H_i'), M(r'\%'), M(r'\%_A')]
def cel(v, d):
    """valor exacte si té com a molt d decimals; si no, arrodonit amb ≈"""
    v = Fr(v); t = ('%.*f' % (d, float(v))).rstrip('0').rstrip('.')
    return tn(v) if fr(t) == v else r'\approx ' + tr(v, d)
def frow(x, f, F, N, xc=None):
    return [xc or M(str(x)), M(str(f)), M(str(F)), M(cel(Fr(f, N), 3)), M(cel(Fr(F, N), 3)), M(cel(Fr(100 * f, N), 1)), M(cel(Fr(100 * F, N), 1))]
def ftot(N, pre=1): return ['<strong>Total</strong>'] + [''] * (pre - 1) + [M(str(N)), '', M('1'), '', M('100'), '']
TNOT = tbl(HF, [frow(x, f, F, NN) for (x, f), F in zip(NOT, FN)] + [ftot(25)], 'c freq')
ALT = [152, 147, 158, 150, 143, 161, 155, 149, 151, 146, 157, 153, 163, 150, 148, 154, 159, 141, 152, 156, 145, 151, 160, 149, 153, 144, 158, 147, 162, 150]
EDG = [140, 145, 150, 155, 160, 165]
FA = [sum(1 for a in ALT if EDG[i] <= a < EDG[i + 1]) for i in range(5)]
assert len(ALT) == 30 and FA == [3, 7, 10, 6, 4], FA
def ivl(a, b): return M(r'[%s,\ %s)' % (a, b))
TALT = tbl([L('Alçada (cm)', 'Altura (cm)', 'Height (cm)'), L('Marca de classe', 'Marca de clase', 'Class mark')] + HF[1:],
           [[ivl(EDG[i], EDG[i + 1])] + frow(None, f, F, 30, M(tn(Fr(EDG[i] + EDG[i + 1], 2))))
            for i, (f, F) in enumerate(zip(FA, acc([(0, f) for f in FA])))] + [ftot(30, 2)], 'c freq')

s2 += box('def', L('La taula de freqüències', 'La tabla de frecuencias', 'The frequency table'),
  P(r"Una <strong>taula de freqüències</strong> organitza les dades: en la primera columna posem els valors \(x_i\) <strong>ordenats</strong> i, al costat, les seues freqüències. Quan la variable és quantitativa també hi afegim la <strong>freqüència absoluta acumulada</strong> \(F_i\):",
    r"Una <strong>tabla de frecuencias</strong> organiza los datos: en la primera columna ponemos los valores \(x_i\) <strong>ordenados</strong> y, al lado, sus frecuencias. Cuando la variable es cuantitativa también añadimos la <strong>frecuencia absoluta acumulada</strong> \(F_i\):",
    r"A <strong>frequency table</strong> organises the data: the first column has the values \(x_i\) <strong>in order</strong> and next to them their frequencies. When the variable is quantitative we also add the <strong>cumulative frequency</strong> \(F_i\):")
  + ul(L(r"\(F_i\) és el nombre de dades <strong>menors o iguals</strong> que \(x_i\). S'obté sumant les \(f_i\) des de dalt fins a la fila de \(x_i\).",
         r"\(F_i\) es el número de datos <strong>menores o iguales</strong> que \(x_i\). Se obtiene sumando las \(f_i\) desde arriba hasta la fila de \(x_i\).",
         r"\(F_i\) is the number of data values <strong>less than or equal to</strong> \(x_i\). Add up the \(f_i\) from the top down to the row of \(x_i\)."),
       L(r"L'última \(F_i\) sempre és \(N\), el nombre total de dades.", r"La última \(F_i\) siempre es \(N\), el número total de datos.", r"The last \(F_i\) is always \(N\), the total number of data."),
       L(r"La <strong>freqüència relativa acumulada</strong> és \(H_i=\dfrac{F_i}{N}\) (o la suma de les \(h_i\) fins a eixa fila), i el <strong>percentatge acumulat</strong> és \(\%_A=H_i\cdot100\). L'última \(H_i\) és 1 i l'últim \(\%_A\), el 100&nbsp;%.",
         r"La <strong>frecuencia relativa acumulada</strong> es \(H_i=\dfrac{F_i}{N}\) (o la suma de las \(h_i\) hasta esa fila), y el <strong>porcentaje acumulado</strong> es \(\%_A=H_i\cdot100\). La última \(H_i\) es 1 y el último \(\%_A\), el 100&nbsp;%.",
         r"The <strong>cumulative relative frequency</strong> is \(H_i=\dfrac{F_i}{N}\) (or the sum of the \(h_i\) down to that row), and the <strong>cumulative percentage</strong> is \(\%_A=H_i\cdot100\). The last \(H_i\) is 1 and the last \(\%_A\) is 100&nbsp;%."))
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"Notes d'un examen de 25 alumnes:", r"Notas de un examen de 25 alumnos:", r"Marks in a test for 25 students:") + TNOT
        + ul(L(r"Han tret un 6 o menys \(F=13\) alumnes, el \(\%_A=52\ \%\). Han aprovat (5 o més) \(25-2=23\) alumnes.", r"Han sacado un 6 o menos \(F=13\) alumnos, el \(\%_A=52\ \%\). Han aprobado (5 o más) \(25-2=23\) alumnos.", r"\(F=13\) students got 6 or less, \(\%_A=52\ \%\). \(25-2=23\) students passed (5 or more)."),
             L(r"Han tret més d'un 7: \(25-18=7\) alumnes, el \(16+8+4=28\ \%\).", r"Han sacado más de un 7: \(25-18=7\) alumnos, el \(16+8+4=28\ \%\).", r"Got more than 7: \(25-18=7\) students, \(16+8+4=28\ \%\)."))))
ck(NN - FN[3], 7); ck(Fr(100 * FN[2], NN), 52); ck(Fr(100 * 4, 25) + Fr(100 * 2, 25) + Fr(100, 25), 28)

s2 += (widget('w-tally', '🧮', L('Laboratori de dades: de la llista a la taula', 'Laboratorio de datos: de la lista a la tabla', 'Data lab: from list to table'),
              ['<p class="hint-s">' + L("Escriu les dades separades per espais (nombres o paraules) o tria un exemple. L'eina fa el recompte i la taula de freqüències.",
                                        "Escribe los datos separados por espacios (números o palabras) o elige un ejemplo. La herramienta hace el recuento y la tabla de frecuencias.",
                                        "Type the data separated by spaces (numbers or words) or choose an example. The tool tallies them and makes the frequency table.") + '</p>',
               seg([('germ', L('Germans', 'Hermanos', 'Siblings')), ('fru', L('Fruita', 'Fruta', 'Fruit')), ('not', L('Notes', 'Notas', 'Marks')), ('own', L('Les meues', 'Las mías', 'My own'))]),
               '<div class="wrow"><label style="flex:1">' + L('Dades', 'Datos', 'Data') + ' <textarea class="tin w dta" data-k="d" rows="2" spellcheck="false" autocapitalize="off" aria-label="dades"></textarea></label></div>'],
              out='<div class="tout"></div>')
       + drill('acum', 'Entrena: llig la taula de freqüències', 'Entrena: lee la tabla de frecuencias', 'Train: read the frequency table'))

COL = [3, 2, 1, 3, 4, 2, 3, 1, 3, 2, 3, 5, 1, 3, 2, 3]  # 1 blau, 2 roig, 3 negre, 4 blanc, 5 verd
CN = {1: L('blau', 'azul', 'blue'), 2: L('roig', 'rojo', 'red'), 3: L('negre', 'negro', 'black'), 4: L('blanc', 'blanco', 'white'), 5: L('verd', 'verde', 'green')}
TC = freqs(COL); NC = len(COL)
assert TC == [(1, 3), (2, 4), (3, 7), (4, 1), (5, 1)] and NC == 16
CNs = {1: ('B', 'A', 'Bl'), 2: ('R', 'R', 'R'), 3: ('N', 'N', 'K'), 4: ('Bc', 'Bc', 'W'), 5: ('V', 'V', 'G')}
DAU = {1: 7, 2: 9, 3: 8, 4: 10, 5: 6, 6: 10}
assert sum(DAU.values()) == 50
EX3 = [(Fr(1, 4), 25), (Fr(3, 5), 60), (Fr(7, 20), 35), (Fr(2, 25), 8)]
for h, p in EX3: ck(100 * h, p)
S2L = (
 [prob(L(r"Aquests són els colors dels cotxes que han passat per davant de l'institut: " + ', '.join({1: 'blau', 2: 'roig', 3: 'negre', 4: 'blanc', 5: 'verd'}[c] for c in COL) + ". Fes la taula de freqüències absolutes i relatives.",
         r"Estos son los colores de los coches que han pasado por delante del instituto: " + ', '.join({1: 'azul', 2: 'rojo', 3: 'negro', 4: 'blanco', 5: 'verde'}[c] for c in COL) + ". Haz la tabla de frecuencias absolutas y relativas.",
         r"These are the colours of the cars that drove past the school: " + ', '.join({1: 'blue', 2: 'red', 3: 'black', 4: 'white', 5: 'green'}[c] for c in COL) + ". Make the table of absolute and relative frequencies."),
       P(r"Fem el recompte de cada color i dividim entre el total, \(N=16\):", r"Hacemos el recuento de cada color y dividimos entre el total, \(N=16\):", r"We tally each colour and divide by the total, \(N=16\):")
       + tbl(HREL, [row_rel(c, f, NC, CN[c]) for c, f in TC] + [TOT(NC)], 'c freq'),
       P(r"El color més repetit és el negre: \(7\) de cada \(16\) cotxes, el \(43\dc 75\ \%\).", r"El color más repetido es el negro: \(7\) de cada \(16\) coches, el \(43\dc 75\ \%\).", r"The most common colour is black: \(7\) out of every \(16\) cars, \(43\dc 75\ \%\).")),
  prob(L(r"Escriu com a percentatge aquestes freqüències relatives: \(\frac14\), \(\frac35\), \(0\dc 35\), \(\frac{2}{25}\).",
         r"Escribe como porcentaje estas frecuencias relativas: \(\frac14\), \(\frac35\), \(0\dc 35\), \(\frac{2}{25}\).",
         r"Write these relative frequencies as percentages: \(\frac14\), \(\frac35\), \(0\dc 35\), \(\frac{2}{25}\)."),
       D(r"\tfrac14=0\dc 25\to\boxed{25\ \%}\qquad \tfrac35=0\dc 6\to\boxed{60\ \%}\qquad 0\dc 35\to\boxed{35\ \%}\qquad \tfrac{2}{25}=0\dc 08\to\boxed{8\ \%}"))],
 [prob(L(r"Hem llançat un dau 50 vegades. Ha eixit l'1 set vegades, el 2 nou, el 3 huit, el 4 deu, el 5 sis i el 6 la resta. Quantes vegades ha eixit el 6? Quin percentatge de llançaments ha eixit un nombre parell?",
         r"Hemos lanzado un dado 50 veces. Ha salido el 1 siete veces, el 2 nueve, el 3 ocho, el 4 diez, el 5 seis y el 6 el resto. ¿Cuántas veces ha salido el 6? ¿Qué porcentaje de lanzamientos ha salido un número par?",
         r"We rolled a die 50 times. We got 1 seven times, 2 nine times, 3 eight times, 4 ten times, 5 six times and 6 the rest. How many times did we get a 6? What percentage of the rolls were even?"),
       D(r"f_6=50-(7+9+8+10+6)=50-40=\boxed{10}"),
       P(r"Parells: \(f_2+f_4+f_6=9+10+10=29\) llançaments de 50:", r"Pares: \(f_2+f_4+f_6=9+10+10=29\) lanzamientos de 50:", r"Even: \(f_2+f_4+f_6=9+10+10=29\) rolls out of 50:")
       + D(r"\frac{29}{50}=0\dc 58\ \to\ \boxed{58\ \%}")),
  prob(L(r"En una enquesta, el \(30\ \%\) dels 240 alumnes d'un institut diu que va a peu. Quina és la freqüència absoluta d'aquest valor?",
         r"En una encuesta, el \(30\ \%\) de los 240 alumnos de un instituto dice que va a pie. ¿Cuál es la frecuencia absoluta de este valor?",
         r"In a survey, \(30\ \%\) of a school's 240 students say they walk to school. What is the absolute frequency of this value?"),
       P(r"Ara fem el camí al revés: \(f_i=h_i\cdot N\).", r"Ahora hacemos el camino al revés: \(f_i=h_i\cdot N\).", r"Now we go the other way: \(f_i=h_i\cdot N\).")
       + D(r"f=0\dc 30\cdot 240=\boxed{72}\ \tri{alumnes}{alumnos}{students}"))],
 [prob(L(r"En una classe, la freqüència relativa de l'alumnat que fa esport fora de l'institut és \(0\dc 6\). Si 18 alumnes fan esport, quants alumnes hi ha a la classe? Quants no en fan?",
         r"En una clase, la frecuencia relativa del alumnado que hace deporte fuera del instituto es \(0\dc 6\). Si 18 alumnos hacen deporte, ¿cuántos alumnos hay en la clase? ¿Cuántos no hacen?",
         r"In a class, the relative frequency of students who do sport outside school is \(0\dc 6\). If 18 students do sport, how many students are there in the class? How many don't?"),
       P(r"Com que \(h=\dfrac{f}{N}\), tenim \(0\dc 6=\dfrac{18}{N}\). Busquem el nombre que multiplicat per \(0\dc 6\) dona 18:", r"Como \(h=\dfrac{f}{N}\), tenemos \(0\dc 6=\dfrac{18}{N}\). Buscamos el número que multiplicado por \(0\dc 6\) da 18:", r"Since \(h=\dfrac{f}{N}\), we have \(0\dc 6=\dfrac{18}{N}\). We look for the number that multiplied by \(0\dc 6\) gives 18:")
       + D(r"N=18:0\dc 6=\boxed{30}\ \tri{alumnes}{alumnos}{students}\qquad 30-18=\boxed{12}\ \tri{no en fan}{no hacen}{don't}"))])
ck(Fr(18) / fr('0.6'), 30); ck(fr('0.30') * 240, 72); ck(Fr(29, 50) * 100, 58); ck(Fr(7, 16) * 100, '43.75')
S3A = [(0, 4), (1, 6), (2, 7), (3, 2), (4, 1)]
S3B = [12, 25, 8, 31, 17, 22, 5, 28, 14, 19, 33, 9, 21, 26, 16, 11, 24, 18, 30, 7]
EDB = [0, 10, 20, 30, 40]; FB = [sum(1 for a in S3B if EDB[i] <= a < EDB[i + 1]) for i in range(4)]
assert len(S3B) == 20 and FB == [4, 7, 6, 3], FB
S3L = (
 [prob(L(r"Completa la taula de freqüències del nombre de llibres llegits l'estiu passat per 20 alumnes: " + ', '.join(f'{x} llibres → {f} alumnes' for x, f in S3A) + ".",
         r"Completa la tabla de frecuencias del número de libros leídos el verano pasado por 20 alumnos: " + ', '.join(f'{x} libros → {f} alumnos' for x, f in S3A) + ".",
         r"Complete the frequency table for the number of books read last summer by 20 students: " + ', '.join(f'{x} books → {f} students' for x, f in S3A) + "."),
       P(r"Acumulem les \(f_i\) i dividim entre \(N=20\):", r"Acumulamos las \(f_i\) y dividimos entre \(N=20\):", r"Accumulate the \(f_i\) and divide by \(N=20\):")
       + tbl(HF, [frow(x, f, F, 20) for (x, f), F in zip(S3A, acc(S3A))] + [ftot(20)], 'c freq'))],
 [prob(L(r"Amb la taula de l'exercici 3 (llibres llegits), respon: a) quants alumnes han llegit com a molt 2 llibres? b) quants n'han llegit més de 2? c) quin percentatge n'ha llegit almenys 1?",
         r"Con la tabla del ejercicio 3 (libros leídos), responde: a) ¿cuántos alumnos han leído como mucho 2 libros? b) ¿cuántos han leído más de 2? c) ¿qué porcentaje ha leído al menos 1?",
         r"Using the table in exercise 3 (books read), answer: a) how many students read at most 2 books? b) how many read more than 2? c) what percentage read at least 1?"),
       P(r"a) «Com a molt 2» vol dir 0, 1 o 2: és la freqüència acumulada \(F=17\) alumnes.", r"a) «Como mucho 2» quiere decir 0, 1 o 2: es la frecuencia acumulada \(F=17\) alumnos.", r"a) “At most 2” means 0, 1 or 2: it's the cumulative frequency \(F=17\) students."),
       P(r"b) Més de 2 són la resta: \(20-17=3\) alumnes.", r"b) Más de 2 son el resto: \(20-17=3\) alumnos.", r"b) More than 2 is the rest: \(20-17=3\) students."),
       P(r"c) «Almenys 1» són tots menys els que n'han llegit 0: \(20-4=16\), i \(\frac{16}{20}=0\dc 8\to\boxed{80\ \%}\).", r"c) «Al menos 1» son todos menos los que han leído 0: \(20-4=16\), y \(\frac{16}{20}=0\dc 8\to\boxed{80\ \%}\).", r"c) “At least 1” is everybody except those who read 0: \(20-4=16\), and \(\frac{16}{20}=0\dc 8\to\boxed{80\ \%}\)."))],
 [prob(L(r"Aquests són els minuts que 20 alumnes tarden a arribar a l'institut: " + ', '.join(str(a) for a in S3B) + ". Agrupa les dades en intervals d'amplitud 10 començant en 0 i fes la taula amb les marques de classe. Quants tarden menys de 20 minuts?",
         r"Estos son los minutos que 20 alumnos tardan en llegar al instituto: " + ', '.join(str(a) for a in S3B) + ". Agrupa los datos en intervalos de amplitud 10 empezando en 0 y haz la tabla con las marcas de clase. ¿Cuántos tardan menos de 20 minutos?",
         r"These are the minutes 20 students take to get to school: " + ', '.join(str(a) for a in S3B) + ". Group the data into intervals of width 10 starting at 0 and make the table with the class marks. How many take less than 20 minutes?"),
       tbl([L('Temps (min)', 'Tiempo (min)', 'Time (min)'), L('Marca', 'Marca', 'Mark')] + HF[1:],
           [[ivl(EDB[i], EDB[i + 1])] + frow(None, f, F, 20, M(str(EDB[i] + 5))) for i, (f, F) in enumerate(zip(FB, acc([(0, f) for f in FB])))]
           + [ftot(20, 2)], 'c freq'),
       P(r"Menys de 20 minuts són els dos primers intervals: \(F=4+7=\boxed{11}\) alumnes.", r"Menos de 20 minutos son los dos primeros intervalos: \(F=4+7=\boxed{11}\) alumnos.", r"Less than 20 minutes is the first two intervals: \(F=4+7=\boxed{11}\) students."))])
ck(acc(S3A)[2], 17); ck(Fr(16, 20) * 100, 80); ck(FB[0] + FB[1], 11)
s2 += levels(S2L[0] + S3L[0], S2L[1] + S3L[1], S2L[2])
MUS = [6, 7, 5, 6, 8, 6, 9, 7, 6, 5, 8, 7]
GOL = [2, 1, 0, 3, 1, 2, 2, 4, 1, 0, 2, 1, 3, 2, 1]
assert freqs(MUS) == [(5, 2), (6, 4), (7, 3), (8, 2), (9, 1)] and freqs(GOL) == [(0, 2), (1, 5), (2, 5), (3, 2), (4, 1)] and acc(freqs(GOL)) == [2, 7, 12, 14, 15]
ck(fr('0.15') * 80, 12); ck(Fr(3, 15) * 100, 20)
s2 += practice([('★☆☆', L(r"Aquestes són les notes de música de 12 alumnes: 6, 7, 5, 6, 8, 6, 9, 7, 6, 5, 8, 7. Fes la taula amb \(f_i\), \(F_i\), \(h_i\) i percentatges.",
                          r"Estas son las notas de música de 12 alumnos: 6, 7, 5, 6, 8, 6, 9, 7, 6, 5, 8, 7. Haz la tabla con \(f_i\), \(F_i\), \(h_i\) y porcentajes.",
                          r"These are the music marks of 12 students: 6, 7, 5, 6, 8, 6, 9, 7, 6, 5, 8, 7. Make the table with \(f_i\), \(F_i\), \(h_i\) and percentages.")),
                ('★★☆', L(r"Un equip ha marcat aquests gols en 15 partits: 2, 1, 0, 3, 1, 2, 2, 4, 1, 0, 2, 1, 3, 2, 1. En quants partits ha marcat menys de 3 gols? En quin percentatge n'ha marcat 3 o més?",
                          r"Un equipo ha marcado estos goles en 15 partidos: 2, 1, 0, 3, 1, 2, 2, 4, 1, 0, 2, 1, 3, 2, 1. ¿En cuántos partidos ha marcado menos de 3 goles? ¿En qué porcentaje ha marcado 3 o más?",
                          r"A team scored these goals in 15 matches: 2, 1, 0, 3, 1, 2, 2, 4, 1, 0, 2, 1, 3, 2, 1. In how many matches did it score fewer than 3 goals? In what percentage did it score 3 or more?")),
                ('★★☆', L(r"En una mostra de 80 persones, el \(15\ \%\) té els ulls blaus. Quantes persones són?", r"En una muestra de 80 personas, el \(15\ \%\) tiene los ojos azules. ¿Cuántas personas son?", r"In a sample of 80 people, \(15\ \%\) have blue eyes. How many people is that?"))],
               L(r"1) 5: \(f=2\), \(F=2\), \(h\approx0\dc 17\) (\(16\dc 7\ \%\)); 6: 4, 6, \(\approx0\dc 33\) (\(33\dc 3\ \%\)); 7: 3, 9, \(0\dc 25\) (\(25\ \%\)); 8: 2, 11, \(\approx0\dc 17\); 9: 1, 12, \(\approx0\dc 08\) (\(8\dc 3\ \%\)). &nbsp; 2) Gols 0, 1, 2, 3, 4 amb \(f_i\) 2, 5, 5, 2, 1 i \(F_i\) 2, 7, 12, 14, 15: menys de 3 en \(F=12\) partits; 3 o més en 3 de 15, el \(20\ \%\). &nbsp; 3) \(0\dc 15\cdot80=12\) persones.",
                 r"1) 5: \(f=2\), \(F=2\), \(h\approx0\dc 17\) (\(16\dc 7\ \%\)); 6: 4, 6, \(\approx0\dc 33\) (\(33\dc 3\ \%\)); 7: 3, 9, \(0\dc 25\) (\(25\ \%\)); 8: 2, 11, \(\approx0\dc 17\); 9: 1, 12, \(\approx0\dc 08\) (\(8\dc 3\ \%\)). &nbsp; 2) Goles 0, 1, 2, 3, 4 con \(f_i\) 2, 5, 5, 2, 1 y \(F_i\) 2, 7, 12, 14, 15: menos de 3 en \(F=12\) partidos; 3 o más en 3 de 15, el \(20\ \%\). &nbsp; 3) \(0\dc 15\cdot80=12\) personas.",
                 r"1) 5: \(f=2\), \(F=2\), \(h\approx0\dc 17\) (\(16\dc 7\ \%\)); 6: 4, 6, \(\approx0\dc 33\) (\(33\dc 3\ \%\)); 7: 3, 9, \(0\dc 25\) (\(25\ \%\)); 8: 2, 11, \(\approx0\dc 17\); 9: 1, 12, \(\approx0\dc 08\) (\(8\dc 3\ \%\)). &nbsp; 2) Goals 0, 1, 2, 3, 4 with \(f_i\) 2, 5, 5, 2, 1 and \(F_i\) 2, 7, 12, 14, 15: fewer than 3 in \(F=12\) matches; 3 or more in 3 out of 15, \(20\ \%\). &nbsp; 3) \(0\dc 15\cdot80=12\) people."))
assert acc(freqs(MUS)) == [2, 6, 9, 11, 12]

# =====================================================================
# 9.3 Taules de freqüències amb dades agrupades
# =====================================================================
s3 = box('prop', L('Dades agrupades en intervals', 'Datos agrupados en intervalos', 'Data grouped into intervals'),
  P(r"Si la variable és <strong>contínua</strong> o té <strong>molts valors diferents</strong>, agrupem les dades en <strong>intervals</strong> (o classes) de la mateixa amplitud:",
    r"Si la variable es <strong>continua</strong> o tiene <strong>muchos valores diferentes</strong>, agrupamos los datos en <strong>intervalos</strong> (o clases) de la misma amplitud:",
    r"If the variable is <strong>continuous</strong> or has <strong>many different values</strong>, we group the data into <strong>intervals</strong> (or classes) of the same width:")
  + ul(L(r"L'interval \([150,\ 155)\) conté les dades que són <strong>majors o iguals que 150 i menors que 155</strong>: el 150 hi entra, però el 155 va a l'interval següent.",
         r"El intervalo \([150,\ 155)\) contiene los datos que son <strong>mayores o iguales que 150 y menores que 155</strong>: el 150 entra, pero el 155 va al intervalo siguiente.",
         r"The interval \([150,\ 155)\) contains the values that are <strong>greater than or equal to 150 and less than 155</strong>: 150 is in it, but 155 goes into the next interval."),
       L(r"La <strong>marca de classe</strong> és el punt mitjà de l'interval: \(\dfrac{150+155}{2}=152\dc 5\). Representa totes les dades de l'interval.",
         r"La <strong>marca de clase</strong> es el punto medio del intervalo: \(\dfrac{150+155}{2}=152\dc 5\). Representa todos los datos del intervalo.",
         r"The <strong>class mark</strong> is the midpoint of the interval: \(\dfrac{150+155}{2}=152\dc 5\). It stands for all the data in the interval."))
  + box('ex', L('Exemple', 'Ejemplo', 'Example'),
        P(r"Alçades (en cm) de 30 alumnes:", r"Alturas (en cm) de 30 alumnos:", r"Heights (in cm) of 30 students:")
        + '<p class="dlist">' + ' &nbsp; '.join(str(a) for a in ALT) + '</p>' + TALT
        + P(r"Fixa't que els alumnes que fan exactament 150&nbsp;cm (n'hi ha tres) es compten en l'interval \([150,\ 155)\).",
            r"Fíjate en que los alumnos que miden exactamente 150&nbsp;cm (hay tres) se cuentan en el intervalo \([150,\ 155)\).",
            r"Notice that the students who are exactly 150&nbsp;cm tall (there are three) are counted in the interval \([150,\ 155)\).")))
assert ALT.count(150) == 3
import math as _m
ck(max(ALT) - min(ALT), 22); assert 5 < _m.sqrt(30) < 6
s3 += box('def', L('Com es fan els intervals?', '¿Cómo se hacen los intervalos?', 'How do we make the intervals?'),
  P(r"Quan ens donen les dades soltes, hem de decidir nosaltres quants intervals fem i de quina amplitud. Una manera de fer-ho:",
    r"Cuando nos dan los datos sueltos, tenemos que decidir nosotros cuántos intervalos hacemos y de qué amplitud. Una manera de hacerlo:",
    r"When we're given the raw data, we have to decide how many intervals to make and how wide. One way to do it:")
  + ol(L(r"Calculem el <strong>rang</strong> o recorregut: \(x_{\max}-x_{\min}\).", r"Calculamos el <strong>rango</strong> o recorrido: \(x_{\max}-x_{\min}\).", r"Work out the <strong>range</strong>: \(x_{\max}-x_{\min}\)."),
       L(r"Triem el <strong>nombre d'intervals</strong>: entre 5 i 10 sol anar bé. Una regla pràctica és prendre un nombre pròxim a \(\sqrt N\).",
         r"Elegimos el <strong>número de intervalos</strong>: entre 5 y 10 suele ir bien. Una regla práctica es tomar un número próximo a \(\sqrt N\).",
         r"Choose the <strong>number of intervals</strong>: between 5 and 10 usually works. A rule of thumb is a number close to \(\sqrt N\)."),
       L(r"L'<strong>amplitud</strong> de cada interval és el rang dividit entre el nombre d'intervals, <strong>arrodonit cap amunt</strong> a un nombre còmode (2, 5, 10…).",
         r"La <strong>amplitud</strong> de cada intervalo es el rango dividido entre el número de intervalos, <strong>redondeado hacia arriba</strong> a un número cómodo (2, 5, 10…).",
         r"The <strong>width</strong> of each interval is the range divided by the number of intervals, <strong>rounded up</strong> to a convenient number (2, 5, 10…)."),
       L(r"Comencem el primer interval en un valor rodó igual o menor que \(x_{\min}\), i anem sumant l'amplitud fins a passar de \(x_{\max}\).",
         r"Empezamos el primer intervalo en un valor redondo igual o menor que \(x_{\min}\), y vamos sumando la amplitud hasta pasar de \(x_{\max}\).",
         r"Start the first interval at a round value less than or equal to \(x_{\min}\), and keep adding the width until you pass \(x_{\max}\)."))
  + box('ex', L('Exemple: les 30 alçades', 'Ejemplo: las 30 alturas', 'Example: the 30 heights'),
        ul(L(r"La més alta fa 163 cm i la més baixa, 141 cm: rang \(=163-141=22\) cm.", r"La más alta mide 163 cm y la más baja, 141 cm: rango \(=163-141=22\) cm.", r"The tallest is 163 cm and the shortest 141 cm: range \(=163-141=22\) cm."),
           L(r"\(\sqrt{30}\approx5\dc 5\): fem 5 intervals. &nbsp; \(22:5=4\dc 4\), i arrodonim cap amunt: amplitud 5 cm.", r"\(\sqrt{30}\approx5\dc 5\): hacemos 5 intervalos. &nbsp; \(22:5=4\dc 4\), y redondeamos hacia arriba: amplitud 5 cm.", r"\(\sqrt{30}\approx5\dc 5\): we make 5 intervals. &nbsp; \(22:5=4\dc 4\), rounded up: width 5 cm."),
           L(r"Comencem en 140: \([140,\ 145)\), \([145,\ 150)\), …, \([160,\ 165)\). És la taula de l'exemple de dalt.", r"Empezamos en 140: \([140,\ 145)\), \([145,\ 150)\), …, \([160,\ 165)\). Es la tabla del ejemplo de arriba.", r"We start at 140: \([140,\ 145)\), \([145,\ 150)\), …, \([160,\ 165)\). That's the table in the example above.")))
  + note(r"Quan agrupem perdem informació: dins d'un interval ja no sabem quines dades exactes hi havia. Per això els càlculs que farem amb les marques de classe seran <strong>aproximats</strong>.",
         r"Cuando agrupamos perdemos información: dentro de un intervalo ya no sabemos qué datos exactos había. Por eso los cálculos que haremos con las marcas de clase serán <strong>aproximados</strong>.",
         r"Grouping loses information: inside an interval we no longer know the exact values. That's why the calculations we do with class marks will be <strong>approximate</strong>.", '⚠️'))
s3 += (widget('w-grp', '🗂️', L('Agrupa les dades en intervals', 'Agrupa los datos en intervalos', 'Group the data into intervals'),
              ['<p class="hint-s">' + L("Escriu les dades (o tria un exemple), l'inici del primer interval i l'amplitud. L'eina et suggereix quants intervals fer i construeix la taula.",
                                        "Escribe los datos (o elige un ejemplo), el inicio del primer intervalo y la amplitud. La herramienta te sugiere cuántos intervalos hacer y construye la tabla.",
                                        "Type the data (or choose an example), where the first interval starts and the width. The tool suggests how many intervals to make and builds the table.") + '</p>',
               seg([('alt', L('Alçades', 'Alturas', 'Heights')), ('min', L('Minuts', 'Minutos', 'Minutes')), ('own', L('Les meues', 'Las mías', 'My own'))]),
               '<div class="wrow"><label style="flex:1">' + L('Dades', 'Datos', 'Data') + ' <textarea class="tin w dta" data-k="d" rows="2" spellcheck="false" autocapitalize="off" aria-label="dades"></textarea></label></div>',
               '<div class="wrow">' + tin('a', L('Inici', 'Inicio', 'Start'), '140') + tin('w', L('Amplitud', 'Amplitud', 'Width'), '5') + '</div>'],
              out='<div class="tout"></div>')
       + drill('interval', 'Entrena: en quin interval va la dada?', 'Entrena: ¿en qué intervalo va el dato?', 'Train: which interval does the value go in?', 'opts')
       + drill('marca', 'Entrena: calcula la marca de classe', 'Entrena: calcula la marca de clase', 'Train: find the class mark'))

# problemes de 9.3
DIN = [(0, 5, 6), (5, 10, 10), (10, 15, 12), (15, 20, 8), (20, 25, 4)]
NDIN = sum(f for *_, f in DIN); assert NDIN == 40
FDIN = acc([(0, f) for *_, f in DIN]); assert FDIN == [6, 16, 28, 36, 40]
ck(Fr(100 * 4, 40), 10); ck(Fr(100 * (12 + 8), 40), 50)
DEU = [23, 45, 31, 12, 58, 37, 41, 29, 66, 35, 18, 47, 52, 33, 27, 39, 44, 61, 25, 36, 49, 30, 15, 42, 55, 38, 21, 34, 69, 46, 28, 40, 53, 32, 43, 26]
EDD = [10, 20, 30, 40, 50, 60, 70]; FDEU = [sum(1 for a in DEU if EDD[i] <= a < EDD[i + 1]) for i in range(6)]
assert len(DEU) == 36 and min(DEU) == 12 and max(DEU) == 69 and FDEU == [3, 7, 10, 9, 4, 3], FDEU
ck(max(DEU) - min(DEU), 57); ck(Fr(57, 6), '9.5'); ck(Fr(100 * (FDEU[4] + FDEU[5]), 36), Fr(175, 9))
s3 += levels(
 [prob(L(r"En quin dels intervals \([0,\ 10)\), \([10,\ 20)\), \([20,\ 30)\) van les dades \(10\), \(19\dc 9\), \(20\) i \(0\)? Quina és la marca de classe de cada interval?",
         r"¿En cuál de los intervalos \([0,\ 10)\), \([10,\ 20)\), \([20,\ 30)\) van los datos \(10\), \(19\dc 9\), \(20\) y \(0\)? ¿Cuál es la marca de clase de cada intervalo?",
         r"Which of the intervals \([0,\ 10)\), \([10,\ 20)\), \([20,\ 30)\) do the values \(10\), \(19\dc 9\), \(20\) and \(0\) go in? What is the class mark of each interval?"),
       P(r"L'extrem esquerre entra (claudàtor) i el dret no (parèntesi): \(10\to[10,\ 20)\); \(19\dc 9\to[10,\ 20)\); \(20\to[20,\ 30)\); \(0\to[0,\ 10)\).",
         r"El extremo izquierdo entra (corchete) y el derecho no (paréntesis): \(10\to[10,\ 20)\); \(19\dc 9\to[10,\ 20)\); \(20\to[20,\ 30)\); \(0\to[0,\ 10)\).",
         r"The left end is included (square bracket) and the right end isn't (round bracket): \(10\to[10,\ 20)\); \(19\dc 9\to[10,\ 20)\); \(20\to[20,\ 30)\); \(0\to[0,\ 10)\)."),
       D(r"\tfrac{0+10}{2}=\boxed{5}\qquad \tfrac{10+20}{2}=\boxed{15}\qquad \tfrac{20+30}{2}=\boxed{25}"))],
 S3L[2] + [prob(L(r"La taula recull els diners (en €) que 40 alumnes gasten a la setmana. Quants gasten menys de 15 €? Quin percentatge gasta 20 € o més? I entre 10 i 20 €?",
                  r"La tabla recoge el dinero (en €) que 40 alumnos gastan a la semana. ¿Cuántos gastan menos de 15 €? ¿Qué porcentaje gasta 20 € o más? ¿Y entre 10 y 20 €?",
                  r"The table shows the money (in €) that 40 students spend a week. How many spend less than 15 €? What percentage spends 20 € or more? And between 10 and 20 €?")
                + tbl([L('Diners (€)', 'Dinero (€)', 'Money (€)')] + [ivl(a, b) for a, b, _ in DIN], [[M('f_i')] + [M(str(f)) for *_, f in DIN]], 'c'),
       tbl([L('Diners (€)', 'Dinero (€)', 'Money (€)'), L('Marca', 'Marca', 'Mark'), M('f_i'), M('F_i'), M(r'\%')],
           [[ivl(a, b), M(tn(Fr(a + b, 2))), M(str(f)), M(str(F)), M(tn(Fr(100 * f, 40)))] for (a, b, f), F in zip(DIN, FDIN)]
           + [['<strong>Total</strong>', '', M('40'), '', M('100')]], 'c freq'),
       P(r"Menys de 15 €: els tres primers intervals, \(F=\boxed{28}\) alumnes. &nbsp; 20 € o més: l'últim interval, \(\frac{4}{40}\to\boxed{10\ \%}\). &nbsp; Entre 10 i 20 €: \([10,\ 15)\) i \([15,\ 20)\), \(12+8=20\) alumnes, el \(\boxed{50\ \%}\).",
         r"Menos de 15 €: los tres primeros intervalos, \(F=\boxed{28}\) alumnos. &nbsp; 20 € o más: el último intervalo, \(\frac{4}{40}\to\boxed{10\ \%}\). &nbsp; Entre 10 y 20 €: \([10,\ 15)\) y \([15,\ 20)\), \(12+8=20\) alumnos, el \(\boxed{50\ \%}\).",
         r"Less than 15 €: the first three intervals, \(F=\boxed{28}\) students. &nbsp; 20 € or more: the last interval, \(\frac{4}{40}\to\boxed{10\ \%}\). &nbsp; Between 10 and 20 €: \([10,\ 15)\) and \([15,\ 20)\), \(12+8=20\) students, \(\boxed{50\ \%}\)."))],
 [prob(L(r"Aquests són els minuts que 36 alumnes han dedicat als deures un dia: " + ', '.join(str(a) for a in DEU) + ". Decideix quants intervals fas i de quina amplitud, fes la taula de freqüències i digues quin percentatge ha dedicat 50 minuts o més.",
         r"Estos son los minutos que 36 alumnos han dedicado a los deberes un día: " + ', '.join(str(a) for a in DEU) + ". Decide cuántos intervalos haces y de qué amplitud, haz la tabla de frecuencias y di qué porcentaje ha dedicado 50 minutos o más.",
         r"These are the minutes 36 students spent on homework one day: " + ', '.join(str(a) for a in DEU) + ". Decide how many intervals to make and how wide, make the frequency table and say what percentage spent 50 minutes or more."),
       P(r"Rang: \(69-12=57\) minuts. Com que \(\sqrt{36}=6\), fem 6 intervals: \(57:6=9\dc 5\to\) amplitud <strong>10</strong>. Comencem en 10:",
         r"Rango: \(69-12=57\) minutos. Como \(\sqrt{36}=6\), hacemos 6 intervalos: \(57:6=9\dc 5\to\) amplitud <strong>10</strong>. Empezamos en 10:",
         r"Range: \(69-12=57\) minutes. Since \(\sqrt{36}=6\), we make 6 intervals: \(57:6=9\dc 5\to\) width <strong>10</strong>. We start at 10:")
       + tbl([L('Temps (min)', 'Tiempo (min)', 'Time (min)'), L('Marca', 'Marca', 'Mark')] + HF[1:],
             [[ivl(EDD[i], EDD[i + 1])] + frow(None, f, F, 36, M(str(EDD[i] + 5))) for i, (f, F) in enumerate(zip(FDEU, acc([(0, f) for f in FDEU])))] + [ftot(36, 2)], 'c freq'),
       P(r"50 minuts o més: \(4+3=7\) alumnes de 36, \(\frac{7}{36}\approx\boxed{19\dc 4\ \%}\).", r"50 minutos o más: \(4+3=7\) alumnos de 36, \(\frac{7}{36}\approx\boxed{19\dc 4\ \%}\).", r"50 minutes or more: \(4+3=7\) students out of 36, \(\frac{7}{36}\approx\boxed{19\dc 4\ \%}\)."))])
PES = [52, 61, 48, 57, 66, 55, 49, 63, 58, 54, 70, 51, 59, 62, 47, 56, 53, 65, 60, 57]
EDP = [45, 50, 55, 60, 65, 70, 75]; FPES = [sum(1 for a in PES if EDP[i] <= a < EDP[i + 1]) for i in range(6)]
assert len(PES) == 20 and FPES == [3, 4, 6, 4, 2, 1], FPES
ck(FPES[0] + FPES[1] + FPES[2], 13); ck(Fr(100 * 13, 20), 65)
s3 += practice([('★☆☆', L(r"Escriu tres dades que vagen en l'interval \([2\dc 5,\ 3)\) i calcula'n la marca de classe.", r"Escribe tres datos que vayan en el intervalo \([2\dc 5,\ 3)\) y calcula su marca de clase.", r"Write three values that go in the interval \([2\dc 5,\ 3)\) and find its class mark.")),
                ('★★☆', L(r"Pesos (kg) de 20 alumnes: " + ', '.join(str(a) for a in PES) + r". Agrupa'ls en intervals d'amplitud 5 començant en 45 i fes la taula amb \(f_i\) i \(F_i\). Quin percentatge pesa menys de 60 kg?",
                          r"Pesos (kg) de 20 alumnos: " + ', '.join(str(a) for a in PES) + r". Agrúpalos en intervalos de amplitud 5 empezando en 45 y haz la tabla con \(f_i\) y \(F_i\). ¿Qué porcentaje pesa menos de 60 kg?",
                          r"Weights (kg) of 20 students: " + ', '.join(str(a) for a in PES) + r". Group them into intervals of width 5 starting at 45 and make the table with \(f_i\) and \(F_i\). What percentage weighs less than 60 kg?"))],
               L(r"1) Per exemple 2,5; 2,7; 2,99 (el 3 no hi entra); marca \(\frac{2\dc 5+3}{2}=2\dc 75\). &nbsp; 2) \([45,50)\): 3, \(F=3\); \([50,55)\): 4, 7; \([55,60)\): 6, 13; \([60,65)\): 4, 17; \([65,70)\): 2, 19; \([70,75)\): 1, 20. Menys de 60 kg: \(\frac{13}{20}=65\ \%\).",
                 r"1) Por ejemplo 2,5; 2,7; 2,99 (el 3 no entra); marca \(\frac{2\dc 5+3}{2}=2\dc 75\). &nbsp; 2) \([45,50)\): 3, \(F=3\); \([50,55)\): 4, 7; \([55,60)\): 6, 13; \([60,65)\): 4, 17; \([65,70)\): 2, 19; \([70,75)\): 1, 20. Menos de 60 kg: \(\frac{13}{20}=65\ \%\).",
                 r"1) For example 2.5; 2.7; 2.99 (3 isn't included); mark \(\frac{2\dc 5+3}{2}=2\dc 75\). &nbsp; 2) \([45,50)\): 3, \(F=3\); \([50,55)\): 4, 7; \([55,60)\): 6, 13; \([60,65)\): 4, 17; \([65,70)\): 2, 19; \([70,75)\): 1, 20. Less than 60 kg: \(\frac{13}{20}=65\ \%\)."))
assert acc([(0, f) for f in FPES]) == [3, 7, 13, 17, 19, 20]
