# Apartats 9.4-9.7 dels apunts de la Unitat 9 de 1r ESO: interpretació de gràfics, funció de proporcionalitat directa
# y = mx, funció lineal y = mx + n i problemes amb funcions lineals. Totes les rectes es comproven amb lin() i ck().
from comu import *

def mono(P):
    """trams d'una línia poligonal acolorits segons creix, decreix o és constant"""
    return [([P[i], P[i + 1]], 'up' if P[i + 1][1] > P[i][1] else 'down' if P[i + 1][1] < P[i][1] else 'flat') for i in range(len(P) - 1)]
def at(P, x):
    """valor d'una línia poligonal en x"""
    for (a, ya), (b, yb) in zip(P, P[1:]):
        if a <= x <= b: return fr(ya) + (fr(yb) - fr(ya)) * (fr(x) - fr(a)) / (fr(b) - fr(a))
    raise ValueError(x)

# =====================================================================
# 9.4 Interpretació de gràfics
# =====================================================================
EXC = [(0, 0), (2, 8), (3, 8), (4, 12), (6, 0)]
ck(at(EXC, 1), 4); ck(at(EXC, 5), 6); ck(at(EXC, 2.5), 8)
XL_T, YL_D = Ls('temps (h)', 'tiempo (h)', 'time (h)'), Ls('distància (km)', 'distancia (km)', 'distance (km)')
F_EXC = pla((0, 7, 0, 13.6), curves=[(EXC, 'c0')], pts=[(x, y, None, 'p0') for x, y in EXC], proj=[(1, 4)], W=300, H=230, ys=2, xl=XL_T, yl=YL_D)
F_EXCm = pla((0, 7, 0, 13.6), curves=mono(EXC), pts=[(4, 12, L('màxim', 'máximo', 'maximum').replace('span', 'tspan'), 'mx')], W=300, H=230, ys=2, xl=XL_T, yl=YL_D)

s4 = box('def', L('Llegir un gràfic', 'Leer una gráfica', 'Reading a graph'),
  P(r"Un gràfic conta una història. La Júlia fa una excursió en bicicleta; el gràfic dona la <strong>distància</strong> a què està de casa en cada <strong>moment</strong>:",
    r"Una gráfica cuenta una historia. Júlia hace una excursión en bicicleta; la gráfica da la <strong>distancia</strong> a la que está de casa en cada <strong>momento</strong>:",
    r"A graph tells a story. Júlia goes on a bike ride; the graph gives her <strong>distance</strong> from home at each <strong>moment</strong>:")
  + '<div class="gout">' + F_EXC + '<div class="gcol">'
  + P(r"<strong>De la \(x\) a la \(y\)</strong>: a quina distància estava a la 1 h? Busquem 1 en l'eix horitzontal, pugem fins al gràfic i anem a l'eix vertical: <strong>4 km</strong>.",
      r"<strong>De la \(x\) a la \(y\)</strong>: ¿a qué distancia estaba a la 1 h? Buscamos 1 en el eje horizontal, subimos hasta la gráfica y vamos al eje vertical: <strong>4 km</strong>.",
      r"<strong>From \(x\) to \(y\)</strong>: how far away was she after 1 h? Find 1 on the horizontal axis, go up to the graph and across to the vertical axis: <strong>4 km</strong>.")
  + P(r"<strong>De la \(y\) a la \(x\)</strong>: quan estava a 8 km? Busquem 8 en l'eix vertical i mirem on el talla el gràfic: <strong>des de les 2 h fins a les 3 h</strong>, i una altra vegada a les <strong>4 h 40 min</strong>, quan tornava.",
      r"<strong>De la \(y\) a la \(x\)</strong>: ¿cuándo estaba a 8 km? Buscamos 8 en el eje vertical y miramos dónde lo corta la gráfica: <strong>desde las 2 h hasta las 3 h</strong>, y otra vez a las <strong>4 h 40 min</strong>, cuando volvía.",
      r"<strong>From \(y\) to \(x\)</strong>: when was she 8 km away? Find 8 on the vertical axis and see where the graph meets it: <strong>from 2 h to 3 h</strong>, and again at <strong>4 h 40 min</strong>, on her way back.")
  + '</div></div>')
ck(at(EXC, Fr(14, 3)), 8)

s4 += box('prop', L('Creixent, decreixent i constant. Màxims i mínims', 'Creciente, decreciente y constante. Máximos y mínimos', 'Increasing, decreasing and constant. Maxima and minima'),
  P(r"Llegim el gràfic <strong>d'esquerra a dreta</strong>, com un text:", r"Leemos la gráfica <strong>de izquierda a derecha</strong>, como un texto:", r"Read the graph <strong>from left to right</strong>, like a text:")
  + ul(L(r"És <strong>creixent</strong> on puja: quan augmenta la \(x\), augmenta la \(y\).", r"Es <strong>creciente</strong> donde sube: cuando aumenta la \(x\), aumenta la \(y\).", r"It is <strong>increasing</strong> where it goes up: as \(x\) increases, \(y\) increases."),
       L(r"És <strong>decreixent</strong> on baixa: quan augmenta la \(x\), disminueix la \(y\).", r"Es <strong>decreciente</strong> donde baja: cuando aumenta la \(x\), disminuye la \(y\).", r"It is <strong>decreasing</strong> where it goes down: as \(x\) increases, \(y\) decreases."),
       L(r"És <strong>constant</strong> on és horitzontal: la \(y\) no canvia.", r"Es <strong>constante</strong> donde es horizontal: la \(y\) no cambia.", r"It is <strong>constant</strong> where it's flat: \(y\) doesn't change."),
       L(r"El <strong>màxim</strong> és el punt més alt i el <strong>mínim</strong>, el més baix.", r"El <strong>máximo</strong> es el punto más alto y el <strong>mínimo</strong>, el más bajo.", r"The <strong>maximum</strong> is the highest point and the <strong>minimum</strong> the lowest."))
  + '<div class="gout">' + F_EXCm + '<div class="gcol">'
  + P(r"<span class='key ku'></span>Creix de 0 a 2 h i de 3 a 4 h.", r"<span class='key ku'></span>Crece de 0 a 2 h y de 3 a 4 h.", r"<span class='key ku'></span>Increasing from 0 to 2 h and from 3 to 4 h.")
  + P(r"<span class='key kf'></span>És constant de 2 a 3 h.", r"<span class='key kf'></span>Es constante de 2 a 3 h.", r"<span class='key kf'></span>Constant from 2 to 3 h.")
  + P(r"<span class='key kw'></span>Decreix de 4 a 6 h.", r"<span class='key kw'></span>Decrece de 4 a 6 h.", r"<span class='key kw'></span>Decreasing from 4 to 6 h.")
  + P(r"Màxim: \((4,\ 12)\): a les 4 h està a 12 km, el més lluny. Mínim: 0 km, a l'eixida i a l'arribada.", r"Máximo: \((4,\ 12)\): a las 4 h está a 12 km, lo más lejos. Mínimo: 0 km, a la salida y a la llegada.", r"Maximum: \((4,\ 12)\): after 4 h she is 12 km away, the furthest. Minimum: 0 km, at the start and at the end.")
  + '</div></div>')

s4 += box('prop', L('Gràfics de distància i temps', 'Gráficas de distancia y tiempo', 'Distance–time graphs'),
  tbl([L('El gràfic…', 'La gráfica…', 'The graph…'), L('vol dir que…', 'quiere decir que…', 'means that…')],
      [[L('puja', 'sube', 'goes up'), L("s'allunya del punt de partida", 'se aleja del punto de partida', 'it moves away from the start')],
       [L('és horitzontal', 'es horizontal', 'is flat'), L('està parat', 'está parado', 'it has stopped')],
       [L('baixa', 'baja', 'goes down'), L('torna cap al punt de partida', 'vuelve hacia el punto de partida', 'it is coming back')],
       [L('és més inclinat', 'está más inclinada', 'is steeper'), L('va més de pressa', 'va más deprisa', 'it is going faster')]])
  + P(r"Júlia va més de pressa a la tornada: baixa 12 km en 2 h (6 km cada hora), mentre que a l'anada pujava 4 km cada hora.",
      r"Júlia va más deprisa a la vuelta: baja 12 km en 2 h (6 km cada hora), mientras que a la ida subía 4 km cada hora.",
      r"Júlia is faster on the way back: she drops 12 km in 2 h (6 km an hour), while on the way out she climbed 4 km an hour.")
  + widget('w-story', '🎬', L('Un gràfic, una història', 'Una gráfica, una historia', 'One graph, one story'),
           [seg([('exc', L('Excursió', 'Excursión', 'Bike ride')), ('bany', L('Banyera', 'Bañera', 'Bath')), ('tmp', L('Temperatura', 'Temperatura', 'Temperature')), ('glo', L('Globus', 'Globo', 'Balloon'))]),
            '<div class="wrow">' + rng('t', 0, 6, 0.1, 1, 't') + '</div>'],
           out='<div class="gout"></div>')
  + drill('readg', 'Entrena: llig el gràfic', 'Entrena: lee la gráfica', 'Train: read the graph')
  + drill('match', 'Entrena: quin gràfic conta la història?', 'Entrena: ¿qué gráfica cuenta la historia?', 'Train: which graph tells the story?', 'opts'))
ck(Fr(12, 2), 6)

BANY = [(0, 0), (8, 32), (9, 40), (24, 40), (25, 32), (33, 0)]
ck(at(BANY, 4), 16)
XL_M, YL_CM = Ls('temps (min)', 'tiempo (min)', 'time (min)'), Ls('altura (cm)', 'altura (cm)', 'height (cm)')
F_BANY = pla((0, 35, 0, 46), curves=[(BANY, 'c0')], pts=[(x, y, None, 'p0') for x, y in BANY], W=300, H=220, xs=4, gx=2, ys=8, gy=4, xl=XL_M, yl=YL_CM)
GA = [(0, 0), (2, 120), (3, 120), (5, 240)]; GB = [(0, 0), (2, 120), (3, 0), (5, 120)]; GC = [(0, 0), (1, 120), (3, 120), (5, 0)]
def mini(P, cap): return fig(pla((0, 5.5, 0, 270), curves=[(P, 'c0')], W=160, H=110, xs=1, ys=60, gy=60, xl='t', yl='d'), cap)
CIC_A = [(0, 0), (4, 60)]; CIC_P = [(1, 0), (4, 60)]
ck(15 * 4, 60); ck(20 * (4 - 1), 60)
F_CIC = pla((0, 4.6, 0, 66), curves=[(CIC_A, 'c0'), (CIC_P, 'c1')], pts=[(4, 60, None, 'cut')], W=280, H=220, ys=10, gy=10, xl=XL_T, yl=YL_D)
LAIA = [(0, 0), (30, 2), (90, 2), (110, 0)]
F_LAIA = pla((0, 120, 0, 2.6), curves=[(LAIA, 'c0')], W=300, H=160, xs=10, gx=10, ys=0.5, gy=0.5, xl=XL_M, yl=YL_D)
s4 += levels(
 [prob(L(r"Mira el gràfic de l'excursió de Júlia. a) A quina distància de casa estava a les 5 h? b) Quant de temps va estar parada? c) Quina distància va recórrer en total?",
         r"Mira la gráfica de la excursión de Júlia. a) ¿A qué distancia de casa estaba a las 5 h? b) ¿Cuánto tiempo estuvo parada? c) ¿Qué distancia recorrió en total?",
         r"Look at the graph of Júlia's ride. a) How far from home was she after 5 h? b) How long did she stop for? c) How far did she ride altogether?"),
       P(r"a) Busquem \(t=5\): el gràfic està a l'altura \(\boxed{6\ \text{km}}\).", r"a) Buscamos \(t=5\): la gráfica está a la altura \(\boxed{6\ \text{km}}\).", r"a) Find \(t=5\): the graph is at height \(\boxed{6\ \text{km}}\)."),
       P(r"b) El tros horitzontal va de 2 h a 3 h: \(\boxed{1\ \text{hora}}\).", r"b) El trozo horizontal va de 2 h a 3 h: \(\boxed{1\ \text{hora}}\).", r"b) The flat part goes from 2 h to 3 h: \(\boxed{1\ \text{hour}}\)."),
       P(r"c) Va arribar fins a 12 km i va tornar: \(12+12=\boxed{24\ \text{km}}\).", r"c) Llegó hasta 12 km y volvió: \(12+12=\boxed{24\ \text{km}}\).", r"c) She got as far as 12 km and came back: \(12+12=\boxed{24\ \text{km}}\).")),
  prob(L(r"Mira el gràfic de la temperatura d'un dia de l'apartat 9.3. On és creixent? On és decreixent?", r"Mira la gráfica de la temperatura de un día del apartado 9.3. ¿Dónde es creciente? ¿Dónde es decreciente?", r"Look at the graph of the day's temperature in section 9.3. Where is it increasing? Where is it decreasing?"),
       P(r"D'esquerra a dreta: baixa de 0 a 4 h, puja de 4 a 16 h i torna a baixar de 16 a 24 h.", r"De izquierda a derecha: baja de 0 a 4 h, sube de 4 a 16 h y vuelve a bajar de 16 a 24 h.", r"From left to right: it goes down from 0 to 4 h, up from 4 to 16 h and down again from 16 to 24 h."),
       P(r"<strong>Creixent</strong>: de 4 h a 16 h. <strong>Decreixent</strong>: de 0 h a 4 h i de 16 h a 24 h.", r"<strong>Creciente</strong>: de 4 h a 16 h. <strong>Decreciente</strong>: de 0 h a 4 h y de 16 h a 24 h.", r"<strong>Increasing</strong>: from 4 h to 16 h. <strong>Decreasing</strong>: from 0 h to 4 h and from 16 h to 24 h."))],
 [prob(L(r"El gràfic mostra l'altura de l'aigua d'una banyera. Explica què passa en cada tram.", r"La gráfica muestra la altura del agua de una bañera. Explica qué pasa en cada tramo.", r"The graph shows the height of the water in a bath. Explain what happens in each part.") + figs(fig(F_BANY)),
       ul(L(r"De 0 a 8 min: s'<strong>ompli</strong> la banyera (puja 4 cm cada minut) fins a 32 cm.", r"De 0 a 8 min: se <strong>llena</strong> la bañera (sube 4 cm cada minuto) hasta 32 cm.", r"0 to 8 min: the bath <strong>fills</strong> (rising 4 cm a minute) up to 32 cm."),
          L(r"De 8 a 9 min: l'aigua puja de colp 8 cm: algú s'hi <strong>fica</strong> dins.", r"De 8 a 9 min: el agua sube de golpe 8 cm: alguien se <strong>mete</strong> dentro.", r"8 to 9 min: the water suddenly rises 8 cm: someone <strong>gets in</strong>."),
          L(r"De 9 a 24 min: l'altura és <strong>constant</strong> (40 cm): s'està banyant.", r"De 9 a 24 min: la altura es <strong>constante</strong> (40 cm): se está bañando.", r"9 to 24 min: the height is <strong>constant</strong> (40 cm): they're having a bath."),
          L(r"De 24 a 25 min: baixa 8 cm: <strong>ix</strong> de la banyera.", r"De 24 a 25 min: baja 8 cm: <strong>sale</strong> de la bañera.", r"24 to 25 min: it drops 8 cm: they <strong>get out</strong>."),
          L(r"De 25 a 33 min: es <strong>buida</strong> la banyera.", r"De 25 a 33 min: se <strong>vacía</strong> la bañera.", r"25 to 33 min: the bath <strong>empties</strong>."))),
  prob(L(r"Un cotxe ix de casa, va a velocitat constant durant 2 hores, para una hora en un restaurant i continua el viatge a la mateixa velocitat. Quin gràfic (temps, distància) conta aquesta història?",
         r"Un coche sale de casa, va a velocidad constante durante 2 horas, para una hora en un restaurante y continúa el viaje a la misma velocidad. ¿Qué gráfica (tiempo, distancia) cuenta esta historia?",
         r"A car leaves home, drives at a steady speed for 2 hours, stops for an hour at a restaurant and carries on at the same speed. Which (time, distance) graph tells this story?")
       + '<div class="figs three">' + mini(GA, 'A') + mini(GB, 'B') + mini(GC, 'C') + '</div>',
       P(r"La parada és un tros <strong>horitzontal</strong> i, com que continua el viatge, després la distància ha de seguir <strong>pujant</strong>. En B el cotxe torna a casa (baixa) i en C torna al final.",
         r"La parada es un trozo <strong>horizontal</strong> y, como continúa el viaje, después la distancia tiene que seguir <strong>subiendo</strong>. En B el coche vuelve a casa (baja) y en C vuelve al final.",
         r"The stop is a <strong>flat</strong> part and, since the car carries on, afterwards the distance must keep <strong>going up</strong>. In B the car goes back home (down) and in C it comes back at the end."),
       P(r"És el gràfic \(\boxed{\text{A}}\).", r"Es la gráfica \(\boxed{\text{A}}\).", r"It's graph \(\boxed{\text{A}}\)."))],
 [prob(L(r"L'Anna i el Pau fan la mateixa ruta en bici. Qui ix abans? Qui va més de pressa? On i quan es troben?", r"Anna y Pau hacen la misma ruta en bici. ¿Quién sale antes? ¿Quién va más deprisa? ¿Dónde y cuándo se encuentran?", r"Anna and Pau ride the same route. Who sets off first? Who is faster? Where and when do they meet?")
       + figs(fig(F_CIC, '<span class="key k0"></span>Anna &nbsp; <span class="key k1"></span>Pau')),
       P(r"L'Anna ix a les 0 h i el Pau, 1 hora després.", r"Anna sale a las 0 h y Pau, 1 hora después.", r"Anna sets off at 0 h and Pau 1 hour later."),
       P(r"L'Anna fa 60 km en 4 h: 15 km cada hora. El Pau fa 60 km en 3 h: 20 km cada hora. La línia del Pau és <strong>més inclinada</strong>: va més de pressa.",
         r"Anna hace 60 km en 4 h: 15 km cada hora. Pau hace 60 km en 3 h: 20 km cada hora. La línea de Pau está <strong>más inclinada</strong>: va más deprisa.",
         r"Anna covers 60 km in 4 h: 15 km an hour. Pau covers 60 km in 3 h: 20 km an hour. Pau's line is <strong>steeper</strong>: he's faster."),
       P(r"Les línies es tallen en \((4,\ 60)\): el Pau atrapa l'Anna a les \(\boxed{4\ \text{h}}\), a \(\boxed{60\ \text{km}}\) de l'eixida.", r"Las líneas se cortan en \((4,\ 60)\): Pau alcanza a Anna a las \(\boxed{4\ \text{h}}\), a \(\boxed{60\ \text{km}}\) de la salida.", r"The lines cross at \((4,\ 60)\): Pau catches Anna after \(\boxed{4\ \text{h}}\), \(\boxed{60\ \text{km}}\) from the start.")),
  prob(L(r"La Laia ix de casa, camina 2 km en 30 minuts fins a la biblioteca, hi està una hora i torna a casa en 20 minuts. Dibuixa el gràfic (temps en minuts, distància a casa en km).",
         r"Laia sale de casa, camina 2 km en 30 minutos hasta la biblioteca, está allí una hora y vuelve a casa en 20 minutos. Dibuja la gráfica (tiempo en minutos, distancia a casa en km).",
         r"Laia leaves home, walks 2 km in 30 minutes to the library, stays there an hour and walks home in 20 minutes. Draw the graph (time in minutes, distance from home in km)."),
       P(r"Els punts on canvia la història són \((0,\ 0)\), \((30,\ 2)\), \((90,\ 2)\) (30 min + 60 min) i \((110,\ 0)\) (90 + 20 min). Els unim:", r"Los puntos donde cambia la historia son \((0,\ 0)\), \((30,\ 2)\), \((90,\ 2)\) (30 min + 60 min) y \((110,\ 0)\) (90 + 20 min). Los unimos:", r"The points where the story changes are \((0,\ 0)\), \((30,\ 2)\), \((90,\ 2)\) (30 min + 60 min) and \((110,\ 0)\) (90 + 20 min). Join them:"),
       figs(fig(F_LAIA)), P(r"El tram de tornada és més inclinat que el d'anada: torna més de pressa.", r"El tramo de vuelta está más inclinado que el de ida: vuelve más deprisa.", r"The way back is steeper than the way there: she walks home faster."))])
s4 += practice([('★☆☆', L(r"En el gràfic de la banyera, quina altura tenia l'aigua als 4 minuts? Quant de temps es va estar banyant?", r"En la gráfica de la bañera, ¿qué altura tenía el agua a los 4 minutos? ¿Cuánto tiempo estuvo bañándose?", r"In the bath graph, how high was the water after 4 minutes? How long was the bath?")),
                ('★★☆', L(r"En el gràfic de la Laia, on és creixent, on és constant i on és decreixent?", r"En la gráfica de Laia, ¿dónde es creciente, dónde es constante y dónde es decreciente?", r"In Laia's graph, where is it increasing, constant and decreasing?"))],
               L(r"1) 16 cm; de 9 a 24 min: 15 minuts. &nbsp; 2) Creix de 0 a 30 min, és constant de 30 a 90 min i decreix de 90 a 110 min.",
                 r"1) 16 cm; de 9 a 24 min: 15 minutos. &nbsp; 2) Crece de 0 a 30 min, es constante de 30 a 90 min y decrece de 90 a 110 min.",
                 r"1) 16 cm; from 9 to 24 min: 15 minutes. &nbsp; 2) Increasing from 0 to 30 min, constant from 30 to 90 min and decreasing from 90 to 110 min."))

# =====================================================================
# 9.5 Funció de proporcionalitat directa: y = m·x
# =====================================================================
W6 = (-5, 5, -6, 6)
F_PROP = pla(W6, fns=[(2, 0, 'c0'), (Fr(1, 2), 0, 'c1'), (-1, 0, 'c2')], labs=[(2.6, 5.6, 'y = 2x', 'l0'), (4.2, 2.8, 'y = x/2', 'l1'), (-4.2, 5.0, 'y = −x', 'l2')], W=260)
f3 = lin(3)
TV3 = [ck(f3(k), v) for k, v in zip([-2, -1, 0, 1, 2], [-6, -3, 0, 3, 6])]
F_Y3 = pla((-3, 3, -7, 7), fns=[(3, 0, 'c0')], pts=[(k, 3 * k, None, 'p0') for k in (-2, -1, 0, 1, 2)], W=200, ys=2)
F_PEND = pla((-1, 5, -1, 9), fns=[(2, 0, 'c0')], curves=[([(1, 2), (2, 2), (2, 4)], 'c1 stp'), ([(3, 6), (4, 6), (4, 8)], 'c1 stp')],
             labs=[(1.5, 1.4, '+1', 'l1'), (2.45, 3.1, '+2', 'l1'), (3.5, 5.4, '+1', 'l1'), (4.45, 7.1, '+2', 'l1')], W=200)

s5 = box('def', L('Funció de proporcionalitat directa', 'Función de proporcionalidad directa', 'Direct proportion function'),
  P(r"Si dues magnituds són <strong>directament proporcionals</strong> (unitat 5), el quocient \(\frac{y}{x}\) és sempre el mateix nombre \(m\), la <strong>constant de proporcionalitat</strong>. Aleshores \(y=m\cdot x\):",
    r"Si dos magnitudes son <strong>directamente proporcionales</strong> (unidad 5), el cociente \(\frac{y}{x}\) es siempre el mismo número \(m\), la <strong>constante de proporcionalidad</strong>. Entonces \(y=m\cdot x\):",
    r"If two quantities are <strong>directly proportional</strong> (unit 5), the quotient \(\frac{y}{x}\) is always the same number \(m\), the <strong>constant of proportionality</strong>. Then \(y=m\cdot x\):")
  + D(r"y=m\cdot x")
  + ul(L(r"El seu gràfic és sempre una <strong>recta que passa per l'origen</strong> \((0,\ 0)\).", r"Su gráfica es siempre una <strong>recta que pasa por el origen</strong> \((0,\ 0)\).", r"Its graph is always a <strong>straight line through the origin</strong> \((0,\ 0)\)."),
       L(r"Per a dibuixar-la n'hi ha prou amb <strong>dos punts</strong>: l'origen i un altre. És millor calcular-ne un tercer per a comprovar que estan alineats.",
         r"Para dibujarla basta con <strong>dos puntos</strong>: el origen y otro. Es mejor calcular un tercero para comprobar que están alineados.",
         r"To draw it, <strong>two points</strong> are enough: the origin and one more. It's best to work out a third one to check they line up."))
  + P(r"Exemple: \(y=3x\).", r"Ejemplo: \(y=3x\).", r"Example: \(y=3x\).")
  + '<div class="gout"><div class="gcol">' + tv([-2, -1, 0, 1, 2], TV3) + P(r"Cada vegada que \(x\) augmenta 1, \(y\) augmenta 3.", r"Cada vez que \(x\) aumenta 1, \(y\) aumenta 3.", r"Each time \(x\) goes up by 1, \(y\) goes up by 3.") + '</div>' + F_Y3 + '</div>'
  + P(r"Les pomes de l'apartat 9.3 (\(y=1{,}5x\)) i el perímetre del quadrat (\(P=4l\)) són funcions de proporcionalitat directa.",
      r"Las manzanas del apartado 9.3 (\(y=1{,}5x\)) y el perímetro del cuadrado (\(P=4l\)) son funciones de proporcionalidad directa.",
      r"The apples in section 9.3 (\(y=1.5x\)) and the perimeter of a square (\(P=4l\)) are direct proportion functions."))

s5 += box('prop', L('El pendent', 'La pendiente', 'The slope'),
  P(r"El nombre \(m\) s'anomena <strong>pendent</strong> de la recta: és el que augmenta \(y\) quan \(x\) augmenta 1. Ens diu com d'inclinada està:",
    r"El número \(m\) se llama <strong>pendiente</strong> de la recta: es lo que aumenta \(y\) cuando \(x\) aumenta 1. Nos dice lo inclinada que está:",
    r"The number \(m\) is called the <strong>slope</strong> of the line: it's how much \(y\) goes up when \(x\) goes up by 1. It tells us how steep the line is:")
  + '<div class="gout">' + F_PEND + '<div class="gcol">'
  + ul(L(r"Si \(m>0\), la recta és <strong>creixent</strong> (puja).", r"Si \(m>0\), la recta es <strong>creciente</strong> (sube).", r"If \(m>0\), the line is <strong>increasing</strong> (goes up)."),
       L(r"Si \(m<0\), la recta és <strong>decreixent</strong> (baixa).", r"Si \(m<0\), la recta es <strong>decreciente</strong> (baja).", r"If \(m<0\), the line is <strong>decreasing</strong> (goes down)."),
       L(r"Com més gran és \(m\) (sense mirar el signe), <strong>més inclinada</strong> és la recta.", r"Cuanto más grande es \(m\) (sin mirar el signo), <strong>más inclinada</strong> es la recta.", r"The bigger \(m\) is (ignoring the sign), the <strong>steeper</strong> the line."))
  + '</div></div>'
  + figs(fig(F_PROP, L('Tres rectes que passen per l\'origen', 'Tres rectas que pasan por el origen', 'Three lines through the origin')))
  + P(r"<strong>Trobar la fórmula</strong>: si la recta passa per l'origen i pel punt \((4,\ 10)\), aleshores \(m=\frac{y}{x}=\frac{10}{4}=2{,}5\) i la fórmula és \(y=2{,}5x\).",
      r"<strong>Hallar la fórmula</strong>: si la recta pasa por el origen y por el punto \((4,\ 10)\), entonces \(m=\frac{y}{x}=\frac{10}{4}=2{,}5\) y la fórmula es \(y=2{,}5x\).",
      r"<strong>Finding the formula</strong>: if the line goes through the origin and the point \((4,\ 10)\), then \(m=\frac{y}{x}=\frac{10}{4}=2.5\) and the formula is \(y=2.5x\).")
  + widget('w-m', '📈', L('Explora y = m·x', 'Explora y = m·x', 'Explore y = m·x'),
           ['<div class="wrow">' + rng('m', -3, 3, 0.5, 2, 'm') + '</div>'], out='<div class="gout"></div>')
  + drill('img0', 'Entrena: calcula la y', 'Entrena: calcula la y', 'Train: work out y')
  + drill('m0', 'Entrena: troba el pendent', 'Entrena: halla la pendiente', 'Train: find the slope'))
ck(fr(10) / 4, '2.5')

T_A = ([1, 2, 3], [4, 8, 12]); T_B = ([1, 2, 3], [3, 5, 7]); T_C = ([2, 4, 6], [1, 2, 3])
def prop(T): return len({fr(y) / x for x, y in zip(*T)}) == 1
assert prop(T_A) and not prop(T_B) and prop(T_C)
F_P2 = pla(W6, fns=[(-2, 0, 'c0'), (Fr(1, 2), 0, 'c1')], pts=[(-2, 4, None, 'p0'), (2, -4, None, 'p0'), (-4, -2, None, 'p1'), (4, 2, None, 'p1')], labs=[(-3.6, 5.4, 'y = −2x', 'l0'), (3.9, 3.0, 'y = x/2', 'l1')], W=240)
F_EUR = pla((0, 55, 0, 66), fns=[('1.1', 0, 'c0', 0, 55)], pts=[(30, 33, None, 'p0'), (50, 55, None, 'p1')], proj=[(30, 33), (50, 55)], W=280, H=240, xs=10, gx=5, ys=10, gy=5, xl='€', yl='$')
ck(fr('1.1') * 30, 33); ck(fr(55) / fr('1.1'), 50)
s5 += levels(
 [prob(L(r"Fes una taula de valors de \(y=3x\) per a \(x=-2,\ -1,\ 0,\ 1,\ 2\) i representa-la.", r"Haz una tabla de valores de \(y=3x\) para \(x=-2,\ -1,\ 0,\ 1,\ 2\) y represéntala.", r"Make a table of values of \(y=3x\) for \(x=-2,\ -1,\ 0,\ 1,\ 2\) and plot it."),
       D(r"x=-2:\ y=3\cdot(-2)=-6\qquad x=-1:\ y=-3\qquad x=0:\ y=0\qquad x=1:\ y=3\qquad x=2:\ y=6"),
       tv([-2, -1, 0, 1, 2], TV3) + P(r"És la recta dibuixada al principi de l'apartat: passa per l'origen i és creixent.", r"Es la recta dibujada al principio del apartado: pasa por el origen y es creciente.", r"It's the line drawn at the start of the section: it goes through the origin and is increasing.")),
  prob(L(r"Quines d'aquestes taules corresponen a una funció de proporcionalitat directa? Escriu-ne la fórmula.", r"¿Cuáles de estas tablas corresponden a una función de proporcionalidad directa? Escribe su fórmula.", r"Which of these tables come from a direct proportion function? Write its formula.")
       + '<div class="tv2">' + tv(*T_A, 'x', 'y') + tv(*T_B, 'x', 'y') + tv(*T_C, 'x', 'y') + '</div>',
       P(r"Calculem \(\frac{y}{x}\) en cada columna: si sempre dona el mateix, és de proporcionalitat directa.", r"Calculamos \(\frac{y}{x}\) en cada columna: si siempre da lo mismo, es de proporcionalidad directa.", r"Work out \(\frac{y}{x}\) in each column: if it's always the same, it's direct proportion."),
       ul(L(r"Primera: \(\frac41=\frac82=\frac{12}{3}=4\). <strong>Sí</strong>: \(y=4x\).", r"Primera: \(\frac41=\frac82=\frac{12}{3}=4\). <strong>Sí</strong>: \(y=4x\).", r"First: \(\frac41=\frac82=\frac{12}{3}=4\). <strong>Yes</strong>: \(y=4x\)."),
          L(r"Segona: \(\frac31=3\) però \(\frac52=2{,}5\). <strong>No</strong>.", r"Segunda: \(\frac31=3\) pero \(\frac52=2{,}5\). <strong>No</strong>.", r"Second: \(\frac31=3\) but \(\frac52=2.5\). <strong>No</strong>."),
          L(r"Tercera: \(\frac12=\frac24=\frac36=0{,}5\). <strong>Sí</strong>: \(y=0{,}5x\).", r"Tercera: \(\frac12=\frac24=\frac36=0{,}5\). <strong>Sí</strong>: \(y=0{,}5x\).", r"Third: \(\frac12=\frac24=\frac36=0.5\). <strong>Yes</strong>: \(y=0.5x\).")))],
 [prob(L(r"Representa en els mateixos eixos \(y=-2x\) i \(y=\frac{x}{2}\). Quina és creixent? Quina és més inclinada?", r"Representa en los mismos ejes \(y=-2x\) e \(y=\frac{x}{2}\). ¿Cuál es creciente? ¿Cuál está más inclinada?", r"Plot \(y=-2x\) and \(y=\frac{x}{2}\) on the same axes. Which one is increasing? Which is steeper?"),
       P(r"Punts de \(y=-2x\): \((-2,\ 4)\), \((0,\ 0)\), \((2,\ -4)\). Punts de \(y=\frac x2\): \((-4,\ -2)\), \((0,\ 0)\), \((4,\ 2)\) (triem \(x\) parells perquè ixquen enters).",
         r"Puntos de \(y=-2x\): \((-2,\ 4)\), \((0,\ 0)\), \((2,\ -4)\). Puntos de \(y=\frac x2\): \((-4,\ -2)\), \((0,\ 0)\), \((4,\ 2)\) (elegimos \(x\) pares para que salgan enteros).",
         r"Points of \(y=-2x\): \((-2,\ 4)\), \((0,\ 0)\), \((2,\ -4)\). Points of \(y=\frac x2\): \((-4,\ -2)\), \((0,\ 0)\), \((4,\ 2)\) (we pick even \(x\) so the results are whole numbers).") + figs(fig(F_P2)),
       P(r"\(y=\frac x2\) és <strong>creixent</strong> (\(m=0{,}5>0\)); \(y=-2x\) és decreixent i <strong>més inclinada</strong> (2 és més gran que 0,5).", r"\(y=\frac x2\) es <strong>creciente</strong> (\(m=0{,}5>0\)); \(y=-2x\) es decreciente y <strong>más inclinada</strong> (2 es mayor que 0,5).", r"\(y=\frac x2\) is <strong>increasing</strong> (\(m=0.5>0\)); \(y=-2x\) is decreasing and <strong>steeper</strong> (2 is bigger than 0.5).")),
  prob(L(r"Una recta passa per l'origen i pel punt \((4,\ 10)\). Escriu-ne la fórmula i comprova si els punts \((-2,\ -5)\) i \((6,\ 14)\) hi són.", r"Una recta pasa por el origen y por el punto \((4,\ 10)\). Escribe su fórmula y comprueba si los puntos \((-2,\ -5)\) y \((6,\ 14)\) están en ella.", r"A line goes through the origin and the point \((4,\ 10)\). Write its formula and check whether \((-2,\ -5)\) and \((6,\ 14)\) are on it."),
       D(r"m=\frac{10}{4}=2{,}5\ \Rightarrow\ \boxed{y=2{,}5x}"),
       P(r"Substituïm la \(x\) de cada punt i mirem si dona la seua \(y\):", r"Sustituimos la \(x\) de cada punto y miramos si da su \(y\):", r"Substitute each point's \(x\) and see whether we get its \(y\):"),
       D(r"x=-2:\ 2{,}5\cdot(-2)=-5\ \checkmark\qquad x=6:\ 2{,}5\cdot6=15\neq14\ \times"),
       P(r"\((-2,\ -5)\) <strong>sí</strong> que és de la recta; \((6,\ 14)\) <strong>no</strong>.", r"\((-2,\ -5)\) <strong>sí</strong> es de la recta; \((6,\ 14)\) <strong>no</strong>.", r"\((-2,\ -5)\) <strong>is</strong> on the line; \((6,\ 14)\) <strong>isn't</strong>."))],
 [prob(L(r"Un dia, 1 euro val 1,10 dòlars. Escriu la fórmula que passa d'euros (\(x\)) a dòlars (\(y\)), dibuixa'n el gràfic i calcula: a) quants dòlars són 30 €; b) quants euros són 55 $.",
         r"Un día, 1 euro vale 1,10 dólares. Escribe la fórmula que pasa de euros (\(x\)) a dólares (\(y\)), dibuja su gráfica y calcula: a) cuántos dólares son 30 €; b) cuántos euros son 55 $.",
         r"One day, 1 euro is worth 1.10 dollars. Write the formula that converts euros (\(x\)) into dollars (\(y\)), draw its graph and work out: a) how many dollars €30 is; b) how many euros $55 is."),
       D(r"y=1{,}1\cdot x") + figs(fig(F_EUR)),
       D(r"\text{a) } y=1{,}1\cdot30=\boxed{33\ \$}\qquad \text{b) } 1{,}1\cdot x=55\ \Rightarrow\ x=\frac{55}{1{,}1}=\boxed{50\ \text{€}}"),
       P(r"En el gràfic: des de 30 en l'eix horitzontal pugem fins a la recta i llegim 33; des de 55 en l'eix vertical anem fins a la recta i baixem a 50.", r"En la gráfica: desde 30 en el eje horizontal subimos hasta la recta y leemos 33; desde 55 en el eje vertical vamos hasta la recta y bajamos a 50.", r"On the graph: from 30 on the horizontal axis go up to the line and read 33; from 55 on the vertical axis go across to the line and down to 50."))])
s5 += practice([('★☆☆', L(r"Fes la taula de \(y=-x\) per a \(x=-2,\ 0,\ 2\). És creixent o decreixent?", r"Haz la tabla de \(y=-x\) para \(x=-2,\ 0,\ 2\). ¿Es creciente o decreciente?", r"Make the table of \(y=-x\) for \(x=-2,\ 0,\ 2\). Is it increasing or decreasing?")),
                ('★★☆', L(r"Una recta passa per l'origen i per \((-3,\ 6)\). Quina és la seua fórmula?", r"Una recta pasa por el origen y por \((-3,\ 6)\). ¿Cuál es su fórmula?", r"A line goes through the origin and \((-3,\ 6)\). What is its formula?"))],
               L(r"1) \(y=2,\ 0,\ -2\): decreixent (\(m=-1\)). &nbsp; 2) \(m=\frac{6}{-3}=-2\): \(y=-2x\).", r"1) \(y=2,\ 0,\ -2\): decreciente (\(m=-1\)). &nbsp; 2) \(m=\frac{6}{-3}=-2\): \(y=-2x\).", r"1) \(y=2,\ 0,\ -2\): decreasing (\(m=-1\)). &nbsp; 2) \(m=\frac{6}{-3}=-2\): \(y=-2x\)."))
ck(fr(6) / -3, -2)

# =====================================================================
# 9.6 Funció lineal: y = m·x + n
# =====================================================================
f21 = lin(2, 1)
TV21 = [ck(f21(k), v) for k, v in zip([-2, -1, 0, 1, 2], [-3, -1, 1, 3, 5])]
F_PAR = pla(W6, fns=[(2, 0, 'c2'), (2, 1, 'c0'), (2, -3, 'c1')], pts=[(0, 1, None, 'p0'), (0, -3, None, 'p1')],
            labs=[(-1.2, 1.4, 'y = 2x + 1', 'l0'), (3.6, 1.2, 'y = 2x − 3', 'l1'), (1.6, 5.6, 'y = 2x', 'l2')], W=260)
F_LEC = pla(W6, fns=[(-1, 3, 'c0'), (2, -1, 'c1')], pts=[(0, 3, None, 'p0'), (0, -1, None, 'p1')],
            curves=[([(0, 3), (1, 3), (1, 2)], 'c0 stp'), ([(0, -1), (1, -1), (1, 1)], 'c1 stp')], W=240)
F_CTE = pla((-5, 5, -2, 5), fns=[(0, 3, 'c0')], labs=[(3.4, 3.6, 'y = 3', 'l0')], W=200)

s6 = box('def', L('Funció lineal', 'Función lineal', 'Linear function'),
  P(r"Una <strong>funció lineal</strong> té una fórmula de la forma", r"Una <strong>función lineal</strong> tiene una fórmula de la forma", r"A <strong>linear function</strong> has a formula of the form")
  + D(r"y=m\cdot x+n")
  + ul(L(r"\(m\) és el <strong>pendent</strong>: el que augmenta (o disminueix, si és negatiu) la \(y\) quan la \(x\) augmenta 1.", r"\(m\) es la <strong>pendiente</strong>: lo que aumenta (o disminuye, si es negativa) la \(y\) cuando la \(x\) aumenta 1.", r"\(m\) is the <strong>slope</strong>: how much \(y\) goes up (or down, if negative) when \(x\) goes up by 1."),
       L(r"\(n\) és l'<strong>ordenada en l'origen</strong>: la recta talla l'eix \(Y\) en el punt \((0,\ n)\), perquè si \(x=0\) aleshores \(y=n\).", r"\(n\) es la <strong>ordenada en el origen</strong>: la recta corta el eje \(Y\) en el punto \((0,\ n)\), porque si \(x=0\) entonces \(y=n\).", r"\(n\) is the <strong>y-intercept</strong>: the line crosses the y-axis at \((0,\ n)\), because when \(x=0\), \(y=n\)."),
       L(r"El seu gràfic és una <strong>recta</strong>. Si \(n=0\), és una funció de proporcionalitat directa (passa per l'origen).", r"Su gráfica es una <strong>recta</strong>. Si \(n=0\), es una función de proporcionalidad directa (pasa por el origen).", r"Its graph is a <strong>straight line</strong>. If \(n=0\), it's a direct proportion function (it goes through the origin)."))
  + P(r"Exemple: \(y=2x+1\). Cada valor de \(y\) és el de \(y=2x\) <strong>més 1</strong>:", r"Ejemplo: \(y=2x+1\). Cada valor de \(y\) es el de \(y=2x\) <strong>más 1</strong>:", r"Example: \(y=2x+1\). Each value of \(y\) is the one for \(y=2x\) <strong>plus 1</strong>:")
  + tv([-2, -1, 0, 1, 2], TV21)
  + P(r"Les rectes amb el <strong>mateix pendent</strong> són <strong>paral·leles</strong>: \(y=2x+1\) és la recta \(y=2x\) pujada 1 unitat, i \(y=2x-3\), baixada 3 unitats.",
      r"Las rectas con la <strong>misma pendiente</strong> son <strong>paralelas</strong>: \(y=2x+1\) es la recta \(y=2x\) subida 1 unidad, e \(y=2x-3\), bajada 3 unidades.",
      r"Lines with the <strong>same slope</strong> are <strong>parallel</strong>: \(y=2x+1\) is the line \(y=2x\) moved up 1 unit, and \(y=2x-3\) moved down 3 units.")
  + figs(fig(F_PAR, L('Rectes paral·leles de pendent 2', 'Rectas paralelas de pendiente 2', 'Parallel lines with slope 2')))
  + note(r"Si \(m=0\), la fórmula és \(y=n\): la \(y\) sempre val el mateix. És una <strong>funció constant</strong> i el seu gràfic és una recta <strong>horitzontal</strong>.",
         r"Si \(m=0\), la fórmula es \(y=n\): la \(y\) siempre vale lo mismo. Es una <strong>función constante</strong> y su gráfica es una recta <strong>horizontal</strong>.",
         r"If \(m=0\), the formula is \(y=n\): \(y\) always has the same value. It's a <strong>constant function</strong> and its graph is a <strong>horizontal</strong> line.")
  + figs(fig(F_CTE, L('Funció constant', 'Función constante', 'Constant function'))))

s6 += box('prop', L('Com es representa i com es llig la fórmula', 'Cómo se representa y cómo se lee la fórmula', 'Plotting it and reading its formula'),
  P(r"<strong>Per a representar</strong> \(y=mx+n\): fem una taula amb dos o tres valors de \(x\) (el 0 és el més fàcil: dona \((0,\ n)\)), dibuixem els punts i els unim amb una recta.",
    r"<strong>Para representar</strong> \(y=mx+n\): hacemos una tabla con dos o tres valores de \(x\) (el 0 es el más fácil: da \((0,\ n)\)), dibujamos los puntos y los unimos con una recta.",
    r"<strong>To plot</strong> \(y=mx+n\): make a table with two or three values of \(x\) (0 is the easiest: it gives \((0,\ n)\)), plot the points and join them with a straight line.")
  + P(r"<strong>Per a trobar la fórmula</strong> d'una recta dibuixada:", r"<strong>Para hallar la fórmula</strong> de una recta dibujada:", r"<strong>To find the formula</strong> of a line on a graph:")
  + '<div class="gout">' + F_LEC + '<div class="gcol">'
  + ol(L(r"Mirem on talla l'eix \(Y\): és \(n\).", r"Miramos dónde corta el eje \(Y\): es \(n\).", r"See where it crosses the y-axis: that's \(n\)."),
       L(r"Des d'aquest punt, avancem 1 a la dreta i comptem quant puja (o baixa) fins a tornar a la recta: és \(m\).", r"Desde ese punto, avanzamos 1 a la derecha y contamos cuánto sube (o baja) hasta volver a la recta: es \(m\).", r"From that point, move 1 to the right and count how far up (or down) you go to get back to the line: that's \(m\)."))
  + P(r"<span class='key k0'></span>Talla en 3 i baixa 1: \(y=-x+3\).", r"<span class='key k0'></span>Corta en 3 y baja 1: \(y=-x+3\).", r"<span class='key k0'></span>Crosses at 3 and goes down 1: \(y=-x+3\).")
  + P(r"<span class='key k1'></span>Talla en \(-1\) i puja 2: \(y=2x-1\).", r"<span class='key k1'></span>Corta en \(-1\) y sube 2: \(y=2x-1\).", r"<span class='key k1'></span>Crosses at \(-1\) and goes up 2: \(y=2x-1\).")
  + '</div></div>'
  + P(r"<strong>Per a saber si un punt és de la recta</strong>, substituïm la seua \(x\) en la fórmula: si dona la seua \(y\), hi és. \((2,\ 3)\) és de \(y=2x-1\) perquè \(2\cdot2-1=3\).",
      r"<strong>Para saber si un punto es de la recta</strong>, sustituimos su \(x\) en la fórmula: si da su \(y\), está. \((2,\ 3)\) es de \(y=2x-1\) porque \(2\cdot2-1=3\).",
      r"<strong>To check whether a point is on the line</strong>, substitute its \(x\) into the formula: if you get its \(y\), it's on it. \((2,\ 3)\) is on \(y=2x-1\) because \(2\cdot2-1=3\).")
  + widget('w-mn', '📐', L('Explora y = m·x + n', 'Explora y = m·x + n', 'Explore y = m·x + n'),
           ['<div class="wrow">' + rng('m', -3, 3, 0.5, 2, 'm') + rng('n', -5, 5, 1, 1, 'n') + '</div>'], out='<div class="gout"></div>')
  + drill('img', 'Entrena: calcula la y', 'Entrena: calcula la y', 'Train: work out y')
  + drill('eq', 'Entrena: quina és la fórmula de la recta?', 'Entrena: ¿cuál es la fórmula de la recta?', 'Train: what is the formula of the line?', 'opts'))
ck(lin(2, -1)(2), 3); ck(lin(-1, 3)(1), 2); ck(lin(2, -1)(1), 1)

MN = [('3x - 4', 3, -4), ('-x + 5', -1, 5), (r'\frac{x}{2} + 1', Fr(1, 2), 1), ('6', 0, 6), ('-4x', -4, 0)]
F_DOS = pla(W6, fns=[(1, 2, 'c0'), (-1, 4, 'c1')], pts=[(1, 3, '(1, 3)', 'cut')], labs=[(-3.0, 0.2, 'y = x + 2', 'l0'), (-2.6, 5.6, 'y = −x + 4', 'l1')], W=260)
ck(lin(1, 2)(1), 3); ck(lin(-1, 4)(1), 3)
F_DUES = pla(W6, fns=[(-2, 3, 'c0'), (Fr(1, 2), -2, 'c1')], pts=[(0, 3, None, 'p0'), (0, -2, None, 'p1'), (1, 1, None, 'p0'), (2, -1, None, 'p1')], labs=[(-1.4, 5.6, 'a', 'l0'), (4.3, 0.8, 'b', 'l1')], W=240)
ck(lin(-2, 3)(1), 1); ck(lin(Fr(1, 2), -2)(2), -1)
s6 += levels(
 [prob(L(r"Fes una taula de valors de \(y=2x+1\) i representa-la.", r"Haz una tabla de valores de \(y=2x+1\) y represéntala.", r"Make a table of values of \(y=2x+1\) and plot it."),
       D(r"x=-2:\ y=2\cdot(-2)+1=-3\qquad x=0:\ y=2\cdot0+1=1\qquad x=2:\ y=2\cdot2+1=5"),
       tv([-2, -1, 0, 1, 2], TV21) + P(r"És la recta <span class='key k0'></span> del dibuix de més amunt: talla l'eix \(Y\) en \((0,\ 1)\) i puja 2 per cada 1 que avança.", r"Es la recta <span class='key k0'></span> del dibujo de más arriba: corta el eje \(Y\) en \((0,\ 1)\) y sube 2 por cada 1 que avanza.", r"It's the <span class='key k0'></span> line in the picture above: it crosses the y-axis at \((0,\ 1)\) and goes up 2 for every 1 across.")),
  prob(L(r"Escriu el pendent i l'ordenada en l'origen de: \(y=3x-4\), \(y=-x+5\), \(y=\frac x2+1\), \(y=6\), \(y=-4x\).", r"Escribe la pendiente y la ordenada en el origen de: \(y=3x-4\), \(y=-x+5\), \(y=\frac x2+1\), \(y=6\), \(y=-4x\).", r"Write the slope and the y-intercept of: \(y=3x-4\), \(y=-x+5\), \(y=\frac x2+1\), \(y=6\), \(y=-4x\)."),
       P(r"\(m\) és el nombre que multiplica la \(x\) i \(n\), el nombre solt (amb el seu signe):", r"\(m\) es el número que multiplica a la \(x\) y \(n\), el número suelto (con su signo):", r"\(m\) is the number multiplying \(x\) and \(n\) is the number on its own (with its sign):"),
       tbl(['', r'\(y=3x-4\)', r'\(y=-x+5\)', r'\(y=\frac x2+1\)', r'\(y=6\)', r'\(y=-4x\)'], [[r'\(m\)'] + [f'\\({tn(m)}\\)' for _, m, _ in MN], [r'\(n\)'] + [f'\\({tn(n)}\\)' for _, _, n in MN]], 'c'))],
 [prob(L(r"Representa en els mateixos eixos \(y=x+2\) i \(y=-x+4\). En quin punt es tallen?", r"Representa en los mismos ejes \(y=x+2\) e \(y=-x+4\). ¿En qué punto se cortan?", r"Plot \(y=x+2\) and \(y=-x+4\) on the same axes. Where do they cross?"),
       tv([-2, 0, 2], [0, 2, 4], 'x', r'\(x+2\)') + tv([-2, 0, 2], [6, 4, 2], 'x', r'\(-x+4\)') + figs(fig(F_DOS)),
       P(r"Es tallen en \(\boxed{(1,\ 3)}\). Ho comprovem: \(1+2=3\) i \(-1+4=3\).", r"Se cortan en \(\boxed{(1,\ 3)}\). Lo comprobamos: \(1+2=3\) y \(-1+4=3\).", r"They cross at \(\boxed{(1,\ 3)}\). Check: \(1+2=3\) and \(-1+4=3\).")),
  prob(L(r"Comprova si els punts \((2,\ 7)\) i \((-1,\ -3)\) són de la recta \(y=3x+1\).", r"Comprueba si los puntos \((2,\ 7)\) y \((-1,\ -3)\) son de la recta \(y=3x+1\).", r"Check whether the points \((2,\ 7)\) and \((-1,\ -3)\) are on the line \(y=3x+1\)."),
       D(r"x=2:\ 3\cdot2+1=7\ \checkmark\qquad x=-1:\ 3\cdot(-1)+1=-2\neq-3\ \times"),
       P(r"\((2,\ 7)\) <strong>sí</strong> que és de la recta; \((-1,\ -3)\) <strong>no</strong>.", r"\((2,\ 7)\) <strong>sí</strong> es de la recta; \((-1,\ -3)\) <strong>no</strong>.", r"\((2,\ 7)\) <strong>is</strong> on the line; \((-1,\ -3)\) <strong>isn't</strong>.")),
  prob(L(r"Escriu la fórmula de les rectes \(a\) i \(b\).", r"Escribe la fórmula de las rectas \(a\) y \(b\).", r"Write the formula of lines \(a\) and \(b\).") + figs(fig(F_DUES)),
       P(r"\(a\) talla l'eix \(Y\) en 3 i, per cada 1 que avança, baixa 2: \(\boxed{y=-2x+3}\).", r"\(a\) corta el eje \(Y\) en 3 y, por cada 1 que avanza, baja 2: \(\boxed{y=-2x+3}\).", r"\(a\) crosses the y-axis at 3 and, for every 1 across, goes down 2: \(\boxed{y=-2x+3}\)."),
       P(r"\(b\) talla en \(-2\) i, per cada 2 que avança, puja 1: puja \(\frac12\) per cada 1. \(\boxed{y=\frac x2-2}\).", r"\(b\) corta en \(-2\) y, por cada 2 que avanza, sube 1: sube \(\frac12\) por cada 1. \(\boxed{y=\frac x2-2}\).", r"\(b\) crosses at \(-2\) and, for every 2 across, goes up 1: up \(\frac12\) for each 1. \(\boxed{y=\frac x2-2}\)."))],
 [prob(L(r"Troba la fórmula de la recta que passa per \((0,\ -1)\) i \((2,\ 3)\), i la de la recta que passa per \((1,\ 1)\) i \((3,\ -3)\).", r"Halla la fórmula de la recta que pasa por \((0,\ -1)\) y \((2,\ 3)\), y la de la recta que pasa por \((1,\ 1)\) y \((3,\ -3)\).", r"Find the formula of the line through \((0,\ -1)\) and \((2,\ 3)\), and of the line through \((1,\ 1)\) and \((3,\ -3)\)."),
       P(r"Primera: talla l'eix \(Y\) en \((0,\ -1)\), així que \(n=-1\). De \(x=0\) a \(x=2\) la \(y\) passa de \(-1\) a 3: puja 4 en 2 passos, és a dir, 2 per pas. \(\boxed{y=2x-1}\).",
         r"Primera: corta el eje \(Y\) en \((0,\ -1)\), así que \(n=-1\). De \(x=0\) a \(x=2\) la \(y\) pasa de \(-1\) a 3: sube 4 en 2 pasos, es decir, 2 por paso. \(\boxed{y=2x-1}\).",
         r"First: it crosses the y-axis at \((0,\ -1)\), so \(n=-1\). From \(x=0\) to \(x=2\), \(y\) goes from \(-1\) to 3: up 4 in 2 steps, that's 2 per step. \(\boxed{y=2x-1}\)."),
       P(r"Segona: de \(x=1\) a \(x=3\) la \(y\) passa d'1 a \(-3\): baixa 4 en 2 passos, \(m=-2\). Per a trobar \(n\), tornem enrere un pas des de \((1,\ 1)\): \(x=0\), \(y=1+2=3\). \(\boxed{y=-2x+3}\).",
         r"Segunda: de \(x=1\) a \(x=3\) la \(y\) pasa de 1 a \(-3\): baja 4 en 2 pasos, \(m=-2\). Para hallar \(n\), retrocedemos un paso desde \((1,\ 1)\): \(x=0\), \(y=1+2=3\). \(\boxed{y=-2x+3}\).",
         r"Second: from \(x=1\) to \(x=3\), \(y\) goes from 1 to \(-3\): down 4 in 2 steps, \(m=-2\). To find \(n\), go back one step from \((1,\ 1)\): \(x=0\), \(y=1+2=3\). \(\boxed{y=-2x+3}\)."),
       D(r"\text{Comprovació: } 2\cdot2-1=3\quad -2\cdot1+3=1\quad -2\cdot3+3=-3\ \checkmark"))])
for (a, b), (m, n) in [(((0, -1), (2, 3)), (2, -1)), (((1, 1), (3, -3)), (-2, 3))]:
    ck(lin(m, n)(a[0]), a[1]); ck(lin(m, n)(b[0]), b[1])
s6 += practice([('★☆☆', L(r"Fes la taula de \(y=-x+2\) per a \(x=-1,\ 0,\ 1,\ 2\) i digues on talla l'eix \(Y\).", r"Haz la tabla de \(y=-x+2\) para \(x=-1,\ 0,\ 1,\ 2\) y di dónde corta el eje \(Y\).", r"Make the table of \(y=-x+2\) for \(x=-1,\ 0,\ 1,\ 2\) and say where it crosses the y-axis.")),
                ('★★☆', L(r"Escriu la fórmula d'una recta paral·lela a \(y=3x\) que talle l'eix \(Y\) en \((0,\ -2)\).", r"Escribe la fórmula de una recta paralela a \(y=3x\) que corte el eje \(Y\) en \((0,\ -2)\).", r"Write the formula of a line parallel to \(y=3x\) that crosses the y-axis at \((0,\ -2)\)."))],
               L(r"1) \(y=3,\ 2,\ 1,\ 0\); talla en \((0,\ 2)\). &nbsp; 2) Mateix pendent, \(n=-2\): \(y=3x-2\).", r"1) \(y=3,\ 2,\ 1,\ 0\); corta en \((0,\ 2)\). &nbsp; 2) Misma pendiente, \(n=-2\): \(y=3x-2\).", r"1) \(y=3,\ 2,\ 1,\ 0\); crosses at \((0,\ 2)\). &nbsp; 2) Same slope, \(n=-2\): \(y=3x-2\)."))
assert [lin(-1, 2)(k) for k in (-1, 0, 1, 2)] == [3, 2, 1, 0]

# =====================================================================
# 9.7 Problemes amb funcions lineals
# =====================================================================
TAXI = lin('1.2', 3)
ck(TAXI(10), 15); ck((fr(21) - 3) / fr('1.2'), 15)
F_TAXI = pla((0, 16.5, 0, 25), fns=[('1.2', 3, 'c0', 0, 16.5)], pts=[(0, 3, None, 'p0'), (10, 15, None, 'p0'), (15, 21, None, 'p1')], proj=[(10, 15), (15, 21)], W=300, H=240, xs=2, gx=1, ys=3, gy=3, xl='km', yl='€')
DIP = lin(-20, 500)
ck(DIP(10), 300); ck(fr(500) / 20, 25)
F_DIP = pla((0, 27, 0, 560), fns=[(-20, 500, 'c0', 0, 25)], pts=[(0, 500, None, 'p0'), (25, 0, None, 'p1')], W=280, H=220, xs=5, gx=5, ys=100, gy=50, xl='min', yl='L')
GA_, GB_ = lin(25, 20), lin(30)
ck(GA_(4), 120); ck(GB_(4), 120)
F_GYM = pla((0, 8.5, 0, 260), fns=[(25, 20, 'c0', 0, 8.5), (30, 0, 'c1', 0, 8.5)], pts=[(4, 120, None, 'cut')], proj=[(4, 120)], W=300, H=240, ys=40, gy=20, xl=Ls('mesos', 'meses', 'months'), yl='€')

s7 = box('prop', L('Com es resol un problema amb una funció lineal', 'Cómo se resuelve un problema con una función lineal', 'Solving a problem with a linear function'),
  P(r"Moltes situacions tenen una <strong>part fixa</strong> (el que es paga o el que hi ha al principi) i una <strong>part que augmenta (o disminueix) sempre igual</strong> per cada unitat. Són funcions lineals:",
    r"Muchas situaciones tienen una <strong>parte fija</strong> (lo que se paga o lo que hay al principio) y una <strong>parte que aumenta (o disminuye) siempre igual</strong> por cada unidad. Son funciones lineales:",
    r"Many situations have a <strong>fixed part</strong> (what you pay or what there is at the start) and a <strong>part that always goes up (or down) by the same amount</strong> per unit. They're linear functions:")
  + D(r"y=\underbrace{m}_{\text{" + Lt('per cada unitat', 'por cada unidad', 'per unit') + r"}}\cdot x+\underbrace{n}_{\text{" + Lt('part fixa', 'parte fija', 'fixed part') + r"}}")
  + ol(L(r"Identifiquem les dues variables (\(x\) i \(y\)) i les seues unitats.", r"Identificamos las dos variables (\(x\) e \(y\)) y sus unidades.", r"Identify the two variables (\(x\) and \(y\)) and their units."),
       L(r"Busquem la part fixa \(n\) i el que canvia per cada unitat, \(m\) (negatiu si disminueix).", r"Buscamos la parte fija \(n\) y lo que cambia por cada unidad, \(m\) (negativo si disminuye).", r"Find the fixed part \(n\) and the change per unit, \(m\) (negative if it goes down)."),
       L(r"Escrivim la fórmula \(y=mx+n\) i, si cal, fem la taula i el gràfic.", r"Escribimos la fórmula \(y=mx+n\) y, si hace falta, hacemos la tabla y la gráfica.", r"Write the formula \(y=mx+n\) and, if needed, make the table and the graph."),
       L(r"Responem: si ens donen la \(x\), la substituïm; si ens donen la \(y\), resolem l'equació (unitat 6) o ho llegim en el gràfic.", r"Respondemos: si nos dan la \(x\), la sustituimos; si nos dan la \(y\), resolvemos la ecuación (unidad 6) o lo leemos en la gráfica.", r"Answer: if you're given \(x\), substitute it; if you're given \(y\), solve the equation (unit 6) or read it off the graph.")))
s7 += box('ex', L('Exemple: el taxi', 'Ejemplo: el taxi', 'Example: the taxi'),
  P(r"Un taxi cobra 3 € per la baixada de bandera i 1,20 € per cada km. Quant costa un viatge de 10 km? Quants km podem fer amb 21 €?",
    r"Un taxi cobra 3 € por la bajada de bandera y 1,20 € por cada km. ¿Cuánto cuesta un viaje de 10 km? ¿Cuántos km podemos hacer con 21 €?",
    r"A taxi charges a €3 pick-up fee plus €1.20 per km. How much is a 10 km ride? How many km can we go with €21?")
  + '<div class="gout"><div class="gcol">'
  + P(r"\(x\) = km, \(y\) = preu (€). Part fixa: 3 €; per cada km: 1,20 €.", r"\(x\) = km, \(y\) = precio (€). Parte fija: 3 €; por cada km: 1,20 €.", r"\(x\) = km, \(y\) = price (€). Fixed part: €3; per km: €1.20.")
  + D(r"y=1{,}2x+3") + D(r"x=10:\ y=1{,}2\cdot10+3=15\ \text{€}") + D(r"1{,}2x+3=21\ \Rightarrow\ 1{,}2x=18") + D(r"x=\frac{18}{1{,}2}=15\ \text{km}")
  + '</div>' + F_TAXI + '</div>')
s7 += box('ex', L('Exemple: un dipòsit que es buida', 'Ejemplo: un depósito que se vacía', 'Example: a tank that empties'),
  P(r"Un dipòsit té 500 L d'aigua i se'n buiden 20 L cada minut. Escriu la fórmula. Quanta aigua queda als 10 minuts? Quan es buida?",
    r"Un depósito tiene 500 L de agua y se vacían 20 L cada minuto. Escribe la fórmula. ¿Cuánta agua queda a los 10 minutos? ¿Cuándo se vacía?",
    r"A tank holds 500 L of water and 20 L drain out every minute. Write the formula. How much water is left after 10 minutes? When is it empty?")
  + '<div class="gout"><div class="gcol">'
  + P(r"Part fixa: 500 L. Cada minut <strong>disminueix</strong> 20 L, així que el pendent és negatiu:", r"Parte fija: 500 L. Cada minuto <strong>disminuye</strong> 20 L, así que la pendiente es negativa:", r"Fixed part: 500 L. Every minute it <strong>drops</strong> 20 L, so the slope is negative:")
  + D(r"y=-20x+500") + D(r"x=10:\ y=-200+500=300\ \text{L}") + D(r"-20x+500=0\ \Rightarrow\ 20x=500") + D(r"x=\frac{500}{20}=25\ \text{min}")
  + '</div>' + F_DIP + '</div>')
s7 += box('ex', L('Exemple: quina oferta ix més a compte?', 'Ejemplo: ¿qué oferta sale más a cuenta?', 'Example: which deal is better?'),
  P(r"El gimnàs A cobra 20 € de matrícula i 25 € al mes; el gimnàs B no té matrícula i cobra 30 € al mes. Quin convé més?",
    r"El gimnasio A cobra 20 € de matrícula y 25 € al mes; el gimnasio B no tiene matrícula y cobra 30 € al mes. ¿Cuál conviene más?",
    r"Gym A charges a €20 joining fee and €25 a month; gym B has no joining fee and charges €30 a month. Which one is better?")
  + '<div class="gout"><div class="gcol">' + D(r"A:\ y=25x+20\qquad B:\ y=30x")
  + tv([1, 2, 3, 4, 5, 6], [GA_(k) for k in range(1, 7)], Ls('mesos', 'meses', 'months').replace('tspan', 'span'), 'A') + tv([1, 2, 3, 4, 5, 6], [GB_(k) for k in range(1, 7)], Ls('mesos', 'meses', 'months').replace('tspan', 'span'), 'B')
  + P(r"Als 4 mesos costen el mateix (120 €): les rectes es tallen en \((4,\ 120)\). Abans, B és més barat; després, A és més barat.",
      r"A los 4 meses cuestan lo mismo (120 €): las rectas se cortan en \((4,\ 120)\). Antes, B es más barato; después, A es más barato.",
      r"After 4 months they cost the same (€120): the lines cross at \((4,\ 120)\). Before that, B is cheaper; after that, A is cheaper.")
  + '</div>' + F_GYM + '</div>'
  + widget('w-two', '⚖️', L('Compara dues tarifes', 'Compara dos tarifas', 'Compare two price plans'),
           ['<div class="wrow"><span class="wl"><span class="key k0"></span>A</span>' + tin('na', L('Part fixa', 'Parte fija', 'Fixed part'), '20') + tin('ma', L('Per unitat', 'Por unidad', 'Per unit'), '25') + '</div>',
            '<div class="wrow"><span class="wl"><span class="key k1"></span>B</span>' + tin('nb', L('Part fixa', 'Parte fija', 'Fixed part'), '0') + tin('mb', L('Per unitat', 'Por unidad', 'Per unit'), '30') + '</div>'],
           out='<div class="gout"></div>')
  + drill('prob', 'Entrena: problemes', 'Entrena: problemas', 'Train: problems'))

ESP = lin(-2, 20); ck(ESP(3), 14); ck(fr(20) / 2, 10)
MOB = lin('0.1', 5); ck(MOB(60), 11); ck((fr(8) - 5) / fr('0.1'), 30)
AIX = lin(15, 50); ck(AIX(10), 200); ck((fr(350) - 50) / 15, 20)
LAMP = [(1, 50), (2, 80), (3, 110)]; FON = lin(30, 20)
for h, p in LAMP: ck(FON(h), p)
ck(FON(5), 170)
LA, LB = lin('0.2', 40), lin('0.1', 60); ck(LA(200), 80); ck(LB(200), 80); ck(LA(100), 60); ck(LB(100), 70)
F_ESP = pla((0, 11, 0, 22), fns=[(-2, 20, 'c0', 0, 10)], pts=[(3, 14, None, 'p0'), (10, 0, None, 'p1')], proj=[(3, 14)], W=260, H=220, xs=1, ys=2, xl='h', yl='cm')
F_LLO = pla((0, 330, 0, 110), fns=[('0.2', 40, 'c0', 0, 330), ('0.1', 60, 'c1', 0, 330)], pts=[(200, 80, None, 'cut')], proj=[(200, 80)], W=300, H=220, xs=50, gx=25, ys=20, gy=10, xl='km', yl='€')
s7 += levels(
 [prob(L(r"Una espelma fa 20 cm i cada hora que està encesa es crema 2 cm. Escriu la fórmula de l'altura \(y\) en funció de les hores \(x\). Quant farà al cap de 3 h? Quan s'acabarà?",
         r"Una vela mide 20 cm y cada hora que está encendida se quema 2 cm. Escribe la fórmula de la altura \(y\) en función de las horas \(x\). ¿Cuánto medirá al cabo de 3 h? ¿Cuándo se acabará?",
         r"A candle is 20 cm tall and burns down 2 cm every hour it's lit. Write the formula for its height \(y\) in terms of the hours \(x\). How tall will it be after 3 h? When will it be used up?"),
       P(r"Part fixa: 20 cm; cada hora <strong>disminueix</strong> 2 cm.", r"Parte fija: 20 cm; cada hora <strong>disminuye</strong> 2 cm.", r"Fixed part: 20 cm; every hour it <strong>drops</strong> 2 cm.") + D(r"y=-2x+20"),
       D(r"x=3:\ y=-6+20=\boxed{14\ \text{cm}}\qquad -2x+20=0\ \Rightarrow\ x=\boxed{10\ \text{h}}") + figs(fig(F_ESP))),
  prob(L(r"Una tarifa de mòbil costa 5 € al mes més 0,10 € per minut. Quant paguem si parlem 60 minuts? I quants minuts hem parlat si paguem 8 €?", r"Una tarifa de móvil cuesta 5 € al mes más 0,10 € por minuto. ¿Cuánto pagamos si hablamos 60 minutos? ¿Y cuántos minutos hemos hablado si pagamos 8 €?", r"A mobile plan costs €5 a month plus €0.10 a minute. How much do we pay for 60 minutes? And how many minutes did we talk if we pay €8?"),
       D(r"y=0{,}1x+5"), D(r"x=60:\ y=6+5=\boxed{11\ \text{€}}\qquad 0{,}1x+5=8\ \Rightarrow\ 0{,}1x=3\ \Rightarrow\ x=\boxed{30\ \text{min}}"))],
 [prob(L(r"Un dipòsit té 50 L i una aixeta hi aboca 15 L cada minut. Escriu la fórmula. Quants litres hi haurà als 10 minuts? Si hi caben 350 L, quan s'omplirà?",
         r"Un depósito tiene 50 L y un grifo echa 15 L cada minuto. Escribe la fórmula. ¿Cuántos litros habrá a los 10 minutos? Si caben 350 L, ¿cuándo se llenará?",
         r"A tank has 50 L in it and a tap pours in 15 L a minute. Write the formula. How many litres will there be after 10 minutes? If it holds 350 L, when will it be full?"),
       D(r"y=15x+50"), D(r"x=10:\ y=150+50=\boxed{200\ \text{L}}\qquad 15x+50=350\ \Rightarrow\ 15x=300\ \Rightarrow\ x=\boxed{20\ \text{min}}")),
  prob(L(r"Un lampista cobra segons aquesta taula. Troba la fórmula i calcula quant cobrarà per 5 hores.", r"Un fontanero cobra según esta tabla. Halla la fórmula y calcula cuánto cobrará por 5 horas.", r"A plumber charges according to this table. Find the formula and work out the charge for 5 hours.")
       + tv([h for h, _ in LAMP], [p for _, p in LAMP], Ls('Hores', 'Horas', 'Hours').replace('tspan', 'span'), L('Preu (€)', 'Precio (€)', 'Price (€)')),
       P(r"Cada hora més, el preu puja \(80-50=30\) €: \(m=30\). Si de 1 h tornem a 0 h, restem 30: \(n=50-30=20\) € (el desplaçament).", r"Cada hora más, el precio sube \(80-50=30\) €: \(m=30\). Si de 1 h volvemos a 0 h, restamos 30: \(n=50-30=20\) € (el desplazamiento).", r"Each extra hour adds \(80-50=30\) €: \(m=30\). Going back from 1 h to 0 h, subtract 30: \(n=50-30=20\) € (the call-out fee)."),
       D(r"y=30x+20\qquad x=5:\ y=150+20=\boxed{170\ \text{€}}"))],
 [prob(L(r"Per a llogar una furgoneta, l'empresa A cobra 40 € més 0,20 € per km i l'empresa B, 60 € més 0,10 € per km. Quina convé si fem 100 km? Per a quants km costen el mateix?",
         r"Para alquilar una furgoneta, la empresa A cobra 40 € más 0,20 € por km y la empresa B, 60 € más 0,10 € por km. ¿Cuál conviene si hacemos 100 km? ¿Para cuántos km cuestan lo mismo?",
         r"To hire a van, company A charges €40 plus €0.20 per km and company B €60 plus €0.10 per km. Which is better for 100 km? For how many km do they cost the same?"),
       D(r"A:\ y=0{,}2x+40\qquad B:\ y=0{,}1x+60"),
       D(r"x=100:\quad A=20+40=60\ \text{€}\qquad B=10+60=70\ \text{€}") + P(r"Per a 100 km convé l'empresa <strong>A</strong>.", r"Para 100 km conviene la empresa <strong>A</strong>.", r"For 100 km company <strong>A</strong> is better."),
       P(r"Cada km, A cobra 0,10 € més que B, però comença 20 € per davall. La diferència desapareix quan \(0{,}10\cdot x=20\), és a dir, \(x=200\) km:", r"Cada km, A cobra 0,10 € más que B, pero empieza 20 € por debajo. La diferencia desaparece cuando \(0{,}10\cdot x=20\), es decir, \(x=200\) km:", r"Each km, A charges €0.10 more than B, but it starts €20 lower. The gap disappears when \(0.10\cdot x=20\), that is, \(x=200\) km:")
       + D(r"A=0{,}2\cdot200+40=80\ \text{€}\qquad B=0{,}1\cdot200+60=80\ \text{€}") + figs(fig(F_LLO)),
       P(r"Costen el mateix per a \(\boxed{200\ \text{km}}\). Per a menys km convé A; per a més, B.", r"Cuestan lo mismo para \(\boxed{200\ \text{km}}\). Para menos km conviene A; para más, B.", r"They cost the same for \(\boxed{200\ \text{km}}\). For fewer km A is better; for more, B."))])
s7 += practice([('★☆☆', L(r"Una entrada al zoo val 12 € per persona i l'aparcament, 5 €. Escriu la fórmula i calcula el preu per a 4 persones.", r"Una entrada al zoo vale 12 € por persona y el aparcamiento, 5 €. Escribe la fórmula y calcula el precio para 4 personas.", r"A zoo ticket is €12 per person and parking is €5. Write the formula and work out the price for 4 people.")),
                ('★★☆', L(r"Un cotxe té 45 L de gasolina i en gasta 6 L cada 100 km. Quanta gasolina li queda després de 300 km? (\(x\) = centenars de km)", r"Un coche tiene 45 L de gasolina y gasta 6 L cada 100 km. ¿Cuánta gasolina le queda después de 300 km? (\(x\) = centenares de km)", r"A car has 45 L of petrol and uses 6 L per 100 km. How much is left after 300 km? (\(x\) = hundreds of km)"))],
               L(r"1) \(y=12x+5\); \(12\cdot4+5=53\) €. &nbsp; 2) \(y=-6x+45\); \(x=3\): \(y=27\) L.", r"1) \(y=12x+5\); \(12\cdot4+5=53\) €. &nbsp; 2) \(y=-6x+45\); \(x=3\): \(y=27\) L.", r"1) \(y=12x+5\); \(12\cdot4+5=53\) €. &nbsp; 2) \(y=-6x+45\); \(x=3\): \(y=27\) L."))
ck(lin(12, 5)(4), 53); ck(lin(-6, 45)(3), 27)
