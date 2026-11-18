# Apartat 10.3 dels apunts de la Unitat 10 de 4t ESO Matemàtiques A (Estadística bidimensional): correlació (sentit, força,
# relació lineal o no lineal, correlació i causalitat), a partir de la forma del núvol de punts.
from comu import *
from s12 import HX, HY

# núvols de mostra amb r exacte (nuvolR) i dos de no lineals
FIG_R = [(0.95, 3), (0.6, 5), (0.0, 9), (-0.6, 21), (-0.95, 4)]
CL = {r: nuvolR(30, r, s) for r, s in FIG_R}
for r, s in FIG_R:
    p = CL[r]; ckr(bi([a for a, b in p], [b for a, b in p])['r'], r)
    assert all(0 <= a <= 10 and 0 <= b <= 10 for a, b in p)
PAR = nuvolR(24, 0.6, 4, f=lambda x: 9 - 0.35 * (x - 5) ** 2)
FUN = [(x, 1 + 0.8 * x) for x in (1, 2, 3, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5)]
NAMES = [(0.95, L('Positiva i forta', 'Positiva y fuerte', 'Strong positive')), (0.6, L('Positiva i feble', 'Positiva y débil', 'Weak positive')),
         (0.0, L('Nul·la (no hi ha relació)', 'Nula (no hay relación)', 'None (no relationship)')), (-0.6, L('Negativa i feble', 'Negativa y débil', 'Weak negative')),
         (-0.95, L('Negativa i forta', 'Negativa y fuerte', 'Strong negative'))]
FIGS6 = ('<div class="figs f3">' + ''.join(fig(nv0(CL[r]), t) for r, t in NAMES)
         + fig(nv0(FUN), L('Funcional (tots en una recta)', 'Funcional (todos en una recta)', 'Functional (all on a line)')) + '</div>')

s3 = box('def', L('Correlació', 'Correlación', 'Correlation'),
  P(r"La <strong>correlació</strong> és la relació (o dependència) <strong>estadística</strong> que hi ha entre dues variables. La forma del núvol de punts ens diu com és:",
    r"La <strong>correlación</strong> es la relación (o dependencia) <strong>estadística</strong> que hay entre dos variables. La forma de la nube de puntos nos dice cómo es:",
    r"<strong>Correlation</strong> is the <strong>statistical</strong> relationship (or dependence) between two variables. The shape of the scatter plot tells us what it is like:")
  + ul(L(r"<strong>Sentit</strong>. La correlació és <strong>positiva</strong> (o directa) si, quan \(X\) creix, \(Y\) també tendeix a créixer: el núvol «puja». És <strong>negativa</strong> (o inversa) si, quan \(X\) creix, \(Y\) tendeix a decréixer: el núvol «baixa». És <strong>nul·la</strong> si el núvol no puja ni baixa.",
         r"<strong>Sentido</strong>. La correlación es <strong>positiva</strong> (o directa) si, cuando \(X\) crece, \(Y\) también tiende a crecer: la nube «sube». Es <strong>negativa</strong> (o inversa) si, cuando \(X\) crece, \(Y\) tiende a decrecer: la nube «baja». Es <strong>nula</strong> si la nube no sube ni baja.",
         r"<strong>Direction</strong>. The correlation is <strong>positive</strong> (or direct) if, as \(X\) increases, \(Y\) tends to increase too: the cloud “goes up”. It's <strong>negative</strong> (or inverse) if, as \(X\) increases, \(Y\) tends to decrease: the cloud “goes down”. It's <strong>zero</strong> if the cloud goes neither up nor down."),
       L(r"<strong>Força</strong>. La correlació és <strong>forta</strong> si els punts estan molt a prop d'una recta, i <strong>feble</strong> si estan molt escampats, encara que s'hi veja una tendència. Si tots els punts estan exactament en una recta, la relació és <strong>funcional</strong>.",
         r"<strong>Fuerza</strong>. La correlación es <strong>fuerte</strong> si los puntos están muy cerca de una recta, y <strong>débil</strong> si están muy dispersos, aunque se vea una tendencia. Si todos los puntos están exactamente en una recta, la relación es <strong>funcional</strong>.",
         r"<strong>Strength</strong>. The correlation is <strong>strong</strong> if the points are very close to a straight line and <strong>weak</strong> if they're widely scattered, even though a trend can be seen. If every point lies exactly on a line, the relationship is <strong>functional</strong>."))
  + FIGS6
  + box('ex', L('Exemples', 'Ejemplos', 'Examples'),
        tbl([L('Variables', 'Variables', 'Variables'), L('Correlació', 'Correlación', 'Correlation')],
            [[L("Hores d'estudi i nota (apartat 10.2)", 'Horas de estudio y nota (apartado 10.2)', 'Study hours and mark (section 10.2)'), L('positiva i forta', 'positiva y fuerte', 'strong positive')],
             [L('Temperatura i gelats venuts', 'Temperatura y helados vendidos', 'Temperature and ice creams sold'), L('positiva i forta', 'positiva y fuerte', 'strong positive')],
             [L("Quilòmetres d'un cotxe de segona mà i preu", 'Kilómetros de un coche de segunda mano y precio', 'Mileage of a second-hand car and its price'), L('negativa i forta', 'negativa y fuerte', 'strong negative')],
             [L('Hores davant de pantalles i hores de son', 'Horas delante de pantallas y horas de sueño', 'Screen time and hours of sleep'), L('negativa i feble', 'negativa y débil', 'weak negative')],
             [L('Alçada i nota de matemàtiques', 'Altura y nota de matemáticas', 'Height and maths mark'), L('nul·la', 'nula', 'zero')]])))

s3 += box('prop', L('Relació lineal i no lineal', 'Relación lineal y no lineal', 'Linear and non-linear relationships'),
  P(r"Si els punts s'agrupen al voltant d'una <strong>recta</strong>, la relació és <strong>lineal</strong>. Però de vegades els punts segueixen una <strong>corba</strong>: per exemple, el rendiment d'un esportista augmenta amb les hores d'entrenament… fins que es cansa i comença a baixar. En aquest curs només estudiem les relacions lineals.",
    r"Si los puntos se agrupan alrededor de una <strong>recta</strong>, la relación es <strong>lineal</strong>. Pero a veces los puntos siguen una <strong>curva</strong>: por ejemplo, el rendimiento de un deportista aumenta con las horas de entrenamiento… hasta que se cansa y empieza a bajar. En este curso solo estudiamos las relaciones lineales.",
    r"If the points cluster around a <strong>straight line</strong>, the relationship is <strong>linear</strong>. But sometimes the points follow a <strong>curve</strong>: for instance, an athlete's performance improves with hours of training… until they get tired and it starts to drop. In this course we only study linear relationships.")
  + figs(fig(nv0(PAR), L('Relació forta, però no lineal', 'Relación fuerte, pero no lineal', 'Strong but non-linear relationship'))))

s3 += box('def', L('Correlació no vol dir causa', 'Correlación no quiere decir causa', "Correlation doesn't mean causation"),
  P(r"Que dues variables tinguen una correlació forta <strong>no vol dir</strong> que una siga la <strong>causa</strong> de l'altra. A l'estiu es venen més gelats i també hi ha més persones que s'ofeguen a la platja: la correlació és positiva, però els gelats no fan que la gent s'ofegue. Totes dues coses depenen d'una <strong>tercera variable</strong>: la calor (hi ha més gent a la platja).",
    r"Que dos variables tengan una correlación fuerte <strong>no quiere decir</strong> que una sea la <strong>causa</strong> de la otra. En verano se venden más helados y también hay más personas que se ahogan en la playa: la correlación es positiva, pero los helados no hacen que la gente se ahogue. Las dos cosas dependen de una <strong>tercera variable</strong>: el calor (hay más gente en la playa).",
    r"Two variables having a strong correlation <strong>doesn't mean</strong> that one <strong>causes</strong> the other. In summer more ice creams are sold and more people drown at the beach: the correlation is positive, but ice creams don't make people drown. Both depend on a <strong>third variable</strong>: the heat (there are more people at the beach).")
  + note(r"Abans de dir que una cosa provoca una altra, pregunta't si hi ha alguna altra variable que les faça variar totes dues.",
         r"Antes de decir que una cosa provoca otra, pregúntate si hay alguna otra variable que las haga variar a las dos.",
         r"Before saying that one thing causes another, ask yourself whether some other variable makes both of them change.", '⚠️'))

s3 += (widget('w-slide', '🎚️', L('Com canvia el núvol segons la correlació', 'Cómo cambia la nube según la correlación', 'How the cloud changes with the correlation'),
              ['<p class="hint-s">' + L("Mou el control: a la dreta, correlació positiva; a l'esquerra, negativa; al centre, nul·la. Com més als extrems, més forta.",
                                        "Mueve el control: a la derecha, correlación positiva; a la izquierda, negativa; en el centro, nula. Cuanto más en los extremos, más fuerte.",
                                        "Move the slider: to the right, positive correlation; to the left, negative; in the middle, zero. The closer to the ends, the stronger.") + '</p>',
               '<div class="wrow">' + rng('r', -1, 1, 0.05, 0.7, 'correlació') + '</div>'],
              out='<div class="gout cl-wrap"><svg class="sgraf nv" viewBox="0 0 340 250" role="img" aria-label="núvol"></svg></div>')
       + drill('tipus', 'Entrena: quin tipus de correlació té el núvol?', 'Entrena: ¿qué tipo de correlación tiene la nube?', 'Train: what kind of correlation does the cloud show?', 'opts')
       + drill('sentit', 'Entrena: correlació positiva, negativa o nul·la?', 'Entrena: ¿correlación positiva, negativa o nula?', 'Train: positive, negative or zero correlation?', 'opts'))

# problemes 10.3
C3A = [(1, 9), (2, 8), (3, 8), (4, 6), (5, 5), (6, 5), (7, 3), (8, 2)]
C3B = [(1, 4), (2, 7), (3, 2), (4, 6), (5, 3), (6, 8), (7, 4), (8, 5)]
C3C = [(1, 2), (2, 4), (3, 3), (4, 6), (5, 5), (6, 8), (7, 6), (8, 9)]
rA = bi(*zip(*C3A))['r']; rB = bi(*zip(*C3B))['r']; rC = bi(*zip(*C3C))['r']
assert rA < -0.95 and abs(rB) < 0.25 and 0.85 < rC < 0.95, (rA, rB, rC)
def nvs(p): return nuvol(p, (0, 9, 1), (0, 10, 2), axes=None, W=220, H=180, rad=3.6)
s3 += levels(
 [prob(L(r"Descriu la correlació (sentit i força) de cadascun d'aquests núvols:", r"Describe la correlación (sentido y fuerza) de cada una de estas nubes:", r"Describe the correlation (direction and strength) of each of these scatter plots:")
       + '<div class="figs f3">' + fig(nvs(C3A), 'A') + fig(nvs(C3B), 'B') + fig(nvs(C3C), 'C') + '</div>',
       P(r"A: <strong>negativa i forta</strong> (baixa i els punts estan quasi en una recta). &nbsp; B: <strong>nul·la</strong> (no puja ni baixa). &nbsp; C: <strong>positiva i forta</strong> (puja; els punts estan bastant a prop d'una recta, però menys que en A).",
         r"A: <strong>negativa y fuerte</strong> (baja y los puntos están casi en una recta). &nbsp; B: <strong>nula</strong> (no sube ni baja). &nbsp; C: <strong>positiva y fuerte</strong> (sube; los puntos están bastante cerca de una recta, pero menos que en A).",
         r"A: <strong>strong negative</strong> (it goes down and the points are almost on a line). &nbsp; B: <strong>zero</strong> (it goes neither up nor down). &nbsp; C: <strong>strong positive</strong> (it goes up; the points are fairly close to a line, but less so than in A).")),
  prob(L(r"Quina correlació esperes entre aquestes variables? a) Pes d'una carta i preu del segell. b) Velocitat d'un cotxe i temps que tarda a fer 100 km. c) Edat d'un cotxe i el seu preu. d) Nombre de germans i nota de l'examen.",
         r"¿Qué correlación esperas entre estas variables? a) Peso de una carta y precio del sello. b) Velocidad de un coche y tiempo que tarda en hacer 100 km. c) Edad de un coche y su precio. d) Número de hermanos y nota del examen.",
         r"What correlation do you expect between these variables? a) Weight of a letter and the price of the stamp. b) Speed of a car and the time it takes to drive 100 km. c) Age of a car and its price. d) Number of siblings and test mark."),
       P(r"a) <strong>Positiva</strong> (com més pesa, més costa). &nbsp; b) <strong>Negativa</strong>: com més velocitat, menys temps (de fet és una relació funcional, \(t=\frac{100}{v}\), però no lineal). &nbsp; c) <strong>Negativa</strong>: els cotxes més vells valen menys. &nbsp; d) <strong>Nul·la</strong>.",
         r"a) <strong>Positiva</strong> (cuanto más pesa, más cuesta). &nbsp; b) <strong>Negativa</strong>: cuanta más velocidad, menos tiempo (de hecho es una relación funcional, \(t=\frac{100}{v}\), pero no lineal). &nbsp; c) <strong>Negativa</strong>: los coches más viejos valen menos. &nbsp; d) <strong>Nula</strong>.",
         r"a) <strong>Positive</strong> (the heavier it is, the more it costs). &nbsp; b) <strong>Negative</strong>: the faster, the less time (in fact it's a functional relationship, \(t=\frac{100}{v}\), but not a linear one). &nbsp; c) <strong>Negative</strong>: older cars are worth less. &nbsp; d) <strong>Zero</strong>."))],
 [prob(L(r"Dibuixa el núvol de punts de les hores d'estudi i les notes dels 10 alumnes de l'apartat 10.1 i descriu-ne la correlació. Si un alumne més estudia 6 hores i trau un 2, com canvia la correlació?",
         r"Dibuja la nube de puntos de las horas de estudio y las notas de los 10 alumnos del apartado 10.1 y describe su correlación. Si un alumno más estudia 6 horas y saca un 2, ¿cómo cambia la correlación?",
         r"Draw the scatter plot of the study hours and marks of the 10 students in section 10.1 and describe its correlation. If one more student studies 6 hours and gets a 2, how does the correlation change?"),
       fig(nuvol(list(zip(HX, HY)) + [(6, 2)], (0, 8, 1), (0, 10, 1), hl=10)),
       P(r"Sense el nou alumne, la correlació és <strong>positiva i forta</strong>. El punt \((6,\,2)\) queda molt lluny de la resta (és una dada <strong>atípica</strong>): la correlació continua sent positiva, però <strong>més feble</strong>. Un sol punt pot canviar molt la correlació.",
         r"Sin el nuevo alumno, la correlación es <strong>positiva y fuerte</strong>. El punto \((6,\,2)\) queda muy lejos del resto (es un dato <strong>atípico</strong>): la correlación sigue siendo positiva, pero <strong>más débil</strong>. Un solo punto puede cambiar mucho la correlación.",
         r"Without the new student, the correlation is <strong>strong positive</strong>. The point \((6,\,2)\) is far from the others (it's an <strong>outlier</strong>): the correlation is still positive but <strong>weaker</strong>. A single point can change the correlation a lot."))],
 [prob(L(r"En les ciutats amb més farmàcies hi ha més casos de grip. Vol dir això que les farmàcies contagien la grip? Explica-ho.",
         r"En las ciudades con más farmacias hay más casos de gripe. ¿Quiere decir esto que las farmacias contagian la gripe? Explícalo.",
         r"Cities with more chemists have more cases of flu. Does that mean chemists spread flu? Explain."),
       P(r"<strong>No</strong>. Hi ha correlació positiva, però no és una relació causa-efecte: totes dues variables depenen d'una tercera, el <strong>nombre d'habitants</strong>. Les ciutats més grans tenen més farmàcies i també més persones que agafen la grip.",
         r"<strong>No</strong>. Hay correlación positiva, pero no es una relación causa-efecto: las dos variables dependen de una tercera, el <strong>número de habitantes</strong>. Las ciudades más grandes tienen más farmacias y también más personas que cogen la gripe.",
         r"<strong>No</strong>. There's a positive correlation, but it isn't cause and effect: both variables depend on a third one, the <strong>number of inhabitants</strong>. Bigger cities have more chemists and also more people who catch flu."))])
rH = bi(HX, HY)['r']; rH2 = bi(HX + [6], HY + [2])['r']; assert 0.9 < rH and 0 < rH2 < rH - 0.2, (rH, rH2)
s3 += practice([('★☆☆', L(r"Posa un exemple de dues variables amb correlació positiva, un altre amb correlació negativa i un altre amb correlació nul·la.", r"Pon un ejemplo de dos variables con correlación positiva, otro con correlación negativa y otro con correlación nula.", r"Give an example of two variables with positive correlation, another with negative correlation and another with zero correlation.")),
                ('★★☆', L(r"Dibuixa el núvol de \((1,8),\ (2,7),\ (3,7),\ (4,5),\ (5,4),\ (6,2)\) i descriu-ne la correlació.", r"Dibuja la nube de \((1,8),\ (2,7),\ (3,7),\ (4,5),\ (5,4),\ (6,2)\) y describe su correlación.", r"Draw the scatter plot of \((1,8),\ (2,7),\ (3,7),\ (4,5),\ (5,4),\ (6,2)\) and describe its correlation."))],
               L(r"1) Per exemple: positiva, alçada i pes; negativa, preu d'un producte i unitats venudes; nul·la, número de calçat i nota. &nbsp; 2) Els punts baixen i estan molt a prop d'una recta: correlació <strong>negativa i forta</strong>.",
                 r"1) Por ejemplo: positiva, altura y peso; negativa, precio de un producto y unidades vendidas; nula, número de calzado y nota. &nbsp; 2) Los puntos bajan y están muy cerca de una recta: correlación <strong>negativa y fuerte</strong>.",
                 r"1) For example: positive, height and weight; negative, the price of a product and units sold; zero, shoe size and mark. &nbsp; 2) The points go down and are very close to a line: <strong>strong negative</strong> correlation.")
               + fig(nuvol([(1, 8), (2, 7), (3, 7), (4, 5), (5, 4), (6, 2)], (0, 7, 1), (0, 10, 2))))
assert bi([1, 2, 3, 4, 5, 6], [8, 7, 7, 5, 4, 2])['r'] < -0.95
