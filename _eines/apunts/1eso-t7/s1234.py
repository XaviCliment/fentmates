# Apartats 7.1-7.4 dels apunts de la Unitat 7 de 1r ESO: punts i rectes, posicions relatives i mediatriu,
# angles i bisectriu, sistema sexagesimal.
from comu import *

def lab(P, t, dx=0, dy=-12, cls=''): return ('txt', P, t, {'dx': dx, 'dy': dy, 'cls': cls})

# =====================================================================
# 7.1 Punts, rectes, semirectes i segments
# =====================================================================
A0, B0 = (0.6, 0.5), (3.0, 1.3)
F_PUNT = G([('dot', (1, 1)), lab((1, 1), 'A', 0, -10), ('dot', (2.4, 0.6)), lab((2.4, 0.6), 'B', 0, -10), ('dot', (1.8, 1.7)), lab((1.8, 1.7), 'C', 0, -10)], W=200, pad=26,
           cap=L('Punts: A, B, C', 'Puntos: A, B, C', 'Points: A, B, C'))
F_RECTA = G([('ln', (-0.4, 0.17), (4.0, 1.63), '', 'b'), ('dot', A0), lab(A0, 'A'), ('dot', B0), lab(B0, 'B'), lab((3.7, 1.53), 'r', 0, 16)], W=200, pad=20,
            cap=L('Recta r (o recta AB)', 'Recta r (o recta AB)', 'Line r (or line AB)'))
F_SEMI = G([('ln', (0.6, 0.5), (4.0, 1.63), '', 'e'), ('dot', A0), lab(A0, 'O'), ('dot', B0), lab(B0, 'A')], W=200, pad=20,
           cap=L("Semirecta d'origen O", 'Semirrecta de origen O', 'Ray starting at O'))
F_SEG = G([('seg', A0, B0, 'hl'), ('dot', A0), lab(A0, 'A'), ('dot', B0), lab(B0, 'B')], W=200, pad=26,
          cap=L(r'Segment \(\overline{AB}\)', r'Segmento \(\overline{AB}\)', r'Segment \(\overline{AB}\)'))
s1 = box('def', L('Els elements bàsics: punt, recta i pla', 'Los elementos básicos: punto, recta y plano', 'The basic elements: point, line and plane'),
  ul(L(r"Un <strong>punt</strong> indica una posició. No té grandària: el dibuixem amb un puntet i l'anomenem amb una lletra <strong>majúscula</strong>: \(A\), \(B\), \(P\)…",
       r"Un <strong>punto</strong> indica una posición. No tiene tamaño: lo dibujamos con un puntito y lo nombramos con una letra <strong>mayúscula</strong>: \(A\), \(B\), \(P\)…",
       r"A <strong>point</strong> marks a position. It has no size: we draw it as a small dot and name it with a <strong>capital</strong> letter: \(A\), \(B\), \(P\)…"),
     L(r"Una <strong>recta</strong> és una línia que no es corba i que no té ni principi ni final (per això la dibuixem amb fletxes). L'anomenem amb una lletra <strong>minúscula</strong> (\(r\), \(s\), \(t\)) o amb dos dels seus punts: recta \(AB\).",
       r"Una <strong>recta</strong> es una línea que no se curva y que no tiene ni principio ni final (por eso la dibujamos con flechas). La nombramos con una letra <strong>minúscula</strong> (\(r\), \(s\), \(t\)) o con dos de sus puntos: recta \(AB\).",
       r"A <strong>line</strong> doesn't bend and has no beginning and no end (that's why we draw it with arrows). We name it with a <strong>lower-case</strong> letter (\(r\), \(s\), \(t\)) or with two of its points: line \(AB\)."),
     L(r"Un <strong>pla</strong> és una superfície plana que s'estén indefinidament en totes direccions, com un full de paper que no s'acabara mai. Totes les figures d'aquesta unitat estan dins d'un pla.",
       r"Un <strong>plano</strong> es una superficie plana que se extiende indefinidamente en todas las direcciones, como una hoja de papel que no se acabara nunca. Todas las figuras de esta unidad están dentro de un plano.",
       r"A <strong>plane</strong> is a flat surface that goes on forever in every direction, like a sheet of paper that never ends. All the shapes in this unit lie in a plane."))
  + figs(F_PUNT, F_RECTA))
s1 += box('prop', L('Punts i rectes', 'Puntos y rectas', 'Points and lines'),
  ul(L(r"Per un punt passen <strong>infinites</strong> rectes.", r"Por un punto pasan <strong>infinitas</strong> rectas.", r"<strong>Infinitely many</strong> lines pass through a point."),
     L(r"Per dos punts passa <strong>una única recta</strong>. Per això, per a dibuixar una recta, n'hi ha prou de marcar dos punts i unir-los amb el regle.",
       r"Por dos puntos pasa <strong>una única recta</strong>. Por eso, para dibujar una recta, basta con marcar dos puntos y unirlos con la regla.",
       r"Through two points there is <strong>exactly one line</strong>. That's why two points and a ruler are enough to draw a line."),
     L(r"Tres o més punts són <strong>alineats</strong> si estan sobre la mateixa recta.", r"Tres o más puntos están <strong>alineados</strong> si están sobre la misma recta.", r"Three or more points are <strong>collinear</strong> if they lie on the same line."))
  + figs(G([('ln', (-0.5, -0.25), (4.5, 2.25), '', 'b'), ('dot', (0.5, 0.25)), lab((0.5, 0.25), 'A'), ('dot', (2, 1)), lab((2, 1), 'B'), ('dot', (3.5, 1.75)), lab((3.5, 1.75), 'C')], W=220, pad=20,
           cap=L('A, B i C estan alineats', 'A, B y C están alineados', 'A, B and C are collinear')),
         G([('ln', (2, 1) , pol((2, 1), 1.6, a), '', 'b') for a in (0, 35, 70, 110, 145)] + [('ln', pol((2, 1), 1.6, 180), pol((2, 1), 1.6, 0), '', ''), ('dot', (2, 1)), lab((2, 1), 'P', 10, 16)], W=220, pad=20,
           cap=L('Infinites rectes passen per P', 'Infinitas rectas pasan por P', 'Infinitely many lines pass through P'))))
s1 += box('def', L('Semirecta i segment', 'Semirrecta y segmento', 'Ray and segment'),
  P(r"Un punt \(O\) d'una recta la dividix en dues parts. Cadascuna és una <strong>semirecta</strong>: té <strong>origen</strong> (el punt \(O\)) però no té final.",
    r"Un punto \(O\) de una recta la divide en dos partes. Cada una es una <strong>semirrecta</strong>: tiene <strong>origen</strong> (el punto \(O\)) pero no tiene final.",
    r"A point \(O\) on a line splits it into two parts. Each part is a <strong>ray</strong>: it has a <strong>starting point</strong> (the point \(O\)) but no end.")
  + P(r"Un <strong>segment</strong> és la part de recta compresa entre dos punts, que en són els <strong>extrems</strong>. Té principi i final, i per tant té una <strong>longitud</strong> que podem mesurar amb el regle. L'escrivim \(\overline{AB}\).",
      r"Un <strong>segmento</strong> es la parte de recta comprendida entre dos puntos, que son sus <strong>extremos</strong>. Tiene principio y final, y por tanto tiene una <strong>longitud</strong> que podemos medir con la regla. Lo escribimos \(\overline{AB}\).",
      r"A <strong>segment</strong> is the part of a line between two points, called its <strong>endpoints</strong>. It has a beginning and an end, so it has a <strong>length</strong> we can measure with a ruler. We write it \(\overline{AB}\).")
  + figs(F_SEMI, F_SEG)
  + P(r"Dos segments són <strong>iguals</strong> si tenen la mateixa longitud. El <strong>punt mitjà</strong> d'un segment és el punt que el dividix en dues parts iguals.",
      r"Dos segmentos son <strong>iguales</strong> si tienen la misma longitud. El <strong>punto medio</strong> de un segmento es el punto que lo divide en dos partes iguales.",
      r"Two segments are <strong>equal</strong> if they have the same length. The <strong>midpoint</strong> of a segment is the point that splits it into two equal parts.")
  + figs(G([('seg', (0, 0), (4, 0)), ('tick', (0, 0), (2, 0), 1), ('tick', (2, 0), (4, 0), 1), ('dot', (0, 0)), lab((0, 0), 'A'), ('dot', (4, 0)), lab((4, 0), 'B'), ('dot', (2, 0), 'pa'), lab((2, 0), 'M', 0, -12, 'hot'),
            lab((1, 0), '3 cm', 0, 18), lab((3, 0), '3 cm', 0, 18)], W=240, pad=24, cap=L(r'M és el punt mitjà de \(\overline{AB}\)', r'M es el punto medio de \(\overline{AB}\)', r'M is the midpoint of \(\overline{AB}\)')))
  + widget('w-elem', '✏️', L('Recta, semirecta o segment?', '¿Recta, semirrecta o segmento?', 'Line, ray or segment?'),
           [seg([('r', L('Recta', 'Recta', 'Line')), ('s', L('Semirecta', 'Semirrecta', 'Ray')), ('g', L('Segment', 'Segmento', 'Segment')), ('a', L('Punts alineats', 'Puntos alineados', 'Collinear points'))])])
  + widget('w-npts', '🔗', L('Quantes rectes passen per n punts?', '¿Cuántas rectas pasan por n puntos?', 'How many lines through n points?'),
           ['<div class="wrow">' + rng('n', 2, 9, 1, 4, 'n') + '</div>', '<p class="hint-s">' + L("Els punts estan col·locats de manera que no n'hi ha tres d'alineats.", "Los puntos están colocados de manera que no hay tres alineados.", "The points are placed so that no three are collinear.") + '</p>'])
  + drill('elem', 'Entrena: reconeix els elements', 'Entrena: reconoce los elementos', 'Train: recognise the elements', mode='opts'))

F_ABCD = G([('ln', (-0.6, 0), (6.6, 0), '', 'b')] + [x for i, t in enumerate('ABCD') for x in (('dot', (2 * i, 0)), lab((2 * i, 0), t))], W=260, pad=20)
s1 += levels(
 [prob(L(r"Observa la figura: els punts \(A\), \(B\) i \(C\) estan sobre la recta \(r\). Escriu tots els segments que tenen per extrems dos d'aquests punts.",
         r"Observa la figura: los puntos \(A\), \(B\) y \(C\) están sobre la recta \(r\). Escribe todos los segmentos que tienen por extremos dos de estos puntos.",
         r"Look at the figure: points \(A\), \(B\) and \(C\) lie on line \(r\). Write down all the segments whose endpoints are two of these points.")
       + figs(G([('ln', (-0.6, 0), (4.6, 0), '', 'b'), lab((4.4, 0), 'r', 0, 16)] + [x for i, t in enumerate('ABC') for x in (('dot', (2 * i, 0)), lab((2 * i, 0), t))], W=240, pad=20)),
       P(r"Agafem els punts de dos en dos: \(\overline{AB}\), \(\overline{AC}\) i \(\overline{BC}\). Hi ha <strong>3 segments</strong> (\(\overline{BA}\) és el mateix segment que \(\overline{AB}\)).",
         r"Tomamos los puntos de dos en dos: \(\overline{AB}\), \(\overline{AC}\) y \(\overline{BC}\). Hay <strong>3 segmentos</strong> (\(\overline{BA}\) es el mismo segmento que \(\overline{AB}\)).",
         r"Take the points two at a time: \(\overline{AB}\), \(\overline{AC}\) and \(\overline{BC}\). There are <strong>3 segments</strong> (\(\overline{BA}\) is the same segment as \(\overline{AB}\)).")),
  prob(L(r"En la mateixa figura, quantes semirectes tenen l'origen en algun dels punts \(A\), \(B\) o \(C\)?",
         r"En la misma figura, ¿cuántas semirrectas tienen el origen en alguno de los puntos \(A\), \(B\) o \(C\)?",
         r"In the same figure, how many rays start at one of the points \(A\), \(B\) or \(C\)?"),
       P(r"Cada punt dividix la recta en dues semirectes (una cap a l'esquerra i una cap a la dreta): \(3\cdot2=\) <strong>6 semirectes</strong>.",
         r"Cada punto divide la recta en dos semirrectas (una hacia la izquierda y una hacia la derecha): \(3\cdot2=\) <strong>6 semirrectas</strong>.",
         r"Each point splits the line into two rays (one to the left and one to the right): \(3\cdot2=\) <strong>6 rays</strong>."))],
 [prob(L(r"Sobre una recta marquem quatre punts \(A\), \(B\), \(C\) i \(D\), en aquest ordre. Quants segments determinen?",
         r"Sobre una recta marcamos cuatro puntos \(A\), \(B\), \(C\) y \(D\), en este orden. ¿Cuántos segmentos determinan?",
         r"On a line we mark four points \(A\), \(B\), \(C\) and \(D\), in that order. How many segments do they determine?") + figs(F_ABCD),
       P(r"Comptem de manera ordenada, sense repetir: començant per \(A\): \(\overline{AB}\), \(\overline{AC}\), \(\overline{AD}\); començant per \(B\): \(\overline{BC}\), \(\overline{BD}\); començant per \(C\): \(\overline{CD}\).",
         r"Contamos de manera ordenada, sin repetir: empezando por \(A\): \(\overline{AB}\), \(\overline{AC}\), \(\overline{AD}\); empezando por \(B\): \(\overline{BC}\), \(\overline{BD}\); empezando por \(C\): \(\overline{CD}\).",
         r"Count in order without repeating: starting at \(A\): \(\overline{AB}\), \(\overline{AC}\), \(\overline{AD}\); starting at \(B\): \(\overline{BC}\), \(\overline{BD}\); starting at \(C\): \(\overline{CD}\)."),
       D(r"3+2+1=6\ \text{%s}" % Lt('segments', 'segmentos', 'segments')))],
 [prob(L(r"Dibuixem cinc punts de manera que no n'hi ha tres d'alineats. Quantes rectes podem traçar que passen per dos d'aquests punts?",
         r"Dibujamos cinco puntos de manera que no hay tres alineados. ¿Cuántas rectas podemos trazar que pasen por dos de estos puntos?",
         r"We draw five points so that no three are collinear. How many lines can we draw through two of these points?"),
       P(r"De cada punt ixen 4 rectes (una cap a cadascun dels altres punts): \(5\cdot4=20\). Però així hem comptat cada recta <strong>dues vegades</strong> (la recta \(AB\) i la recta \(BA\) són la mateixa):",
         r"De cada punto salen 4 rectas (una hacia cada uno de los otros puntos): \(5\cdot4=20\). Pero así hemos contado cada recta <strong>dos veces</strong> (la recta \(AB\) y la recta \(BA\) son la misma):",
         r"From each point 4 lines leave (one to each of the other points): \(5\cdot4=20\). But that counts every line <strong>twice</strong> (line \(AB\) and line \(BA\) are the same):"),
       D(r"\frac{5\cdot4}{2}=10\ \text{%s}" % Lt('rectes', 'rectas', 'lines')),
       P(r"Pots comprovar-ho amb l'eina «Quantes rectes passen per n punts?». En general, amb \(n\) punts hi ha \(\dfrac{n\cdot(n-1)}{2}\) rectes.",
         r"Puedes comprobarlo con la herramienta «¿Cuántas rectas pasan por n puntos?». En general, con \(n\) puntos hay \(\dfrac{n\cdot(n-1)}{2}\) rectas.",
         r"You can check it with the tool “How many lines through n points?”. In general, \(n\) points give \(\dfrac{n\cdot(n-1)}{2}\) lines."))])
ck(5 * 4 // 2, 10); ck(3 + 2 + 1, 6)
s1 += practice([
  ('★☆☆', L(r"Un segment \(\overline{AB}\) fa 9 cm. Quant mesura cadascuna de les parts en què el dividix el seu punt mitjà?", r"Un segmento \(\overline{AB}\) mide 9 cm. ¿Cuánto mide cada una de las partes en que lo divide su punto medio?", r"A segment \(\overline{AB}\) is 9 cm long. How long is each part its midpoint divides it into?")),
  ('★★☆', L(r"Sobre una recta hi ha cinc punts. Quants segments determinen?", r"Sobre una recta hay cinco puntos. ¿Cuántos segmentos determinan?", r"There are five points on a line. How many segments do they determine?")),
  ('★★★', L(r"Quantes rectes determinen sis punts si no n'hi ha tres d'alineats?", r"¿Cuántas rectas determinan seis puntos si no hay tres alineados?", r"How many lines do six points determine if no three are collinear?"))],
  ol(r"\(9:2=4{,}5\) cm", r"\(4+3+2+1=10\) " + L('segments', 'segmentos', 'segments'), r"\(\dfrac{6\cdot5}{2}=15\) " + L('rectes', 'rectas', 'lines')))
ck(4 + 3 + 2 + 1, 10); ck(6 * 5 // 2, 15)

# =====================================================================
# 7.2 Posicions relatives de dues rectes. Mediatriu
# =====================================================================
F_SEC = G([('ln', (0, 0), (4, 2), '', 'b'), ('ln', (0, 2.2), (4, 0.2), '', 'b'), ('dot', (2.2, 1.1), 'pa'), lab((2.2, 1.1), 'P', 0, -12), lab((3.9, 1.95), 'r', 0, 16), lab((3.9, 0.25), 's', 0, -10)], W=200, pad=18,
          cap=L('Secants: es tallen en un punt', 'Secantes: se cortan en un punto', 'Intersecting: they meet at a point'))
F_PAR = G([('ln', (0, 0.3), (4, 1.3), '', 'b'), ('ln', (0, 1.3), (4, 2.3), '', 'b'), lab((3.9, 1.27), 'r', 0, 16), lab((3.9, 2.27), 's', 0, 16)], W=200, pad=18,
          cap=L('Paral·leles: no es tallen mai', 'Paralelas: no se cortan nunca', 'Parallel: they never meet'))
F_PERP = G([('ln', (0, 1.2), (4, 1.2), '', 'b'), ('ln', (2, -0.4), (2, 2.6), '', 'b'), ('ra', (2, 1.2), (3, 1.2), (2, 2)), lab((3.9, 1.2), 'r', 0, 16), lab((2, 2.5), 's', 10, 4)], W=200, pad=18,
           cap=L('Perpendiculars: angles rectes', 'Perpendiculares: ángulos rectos', 'Perpendicular: right angles'))
s2 = box('def', L('Posicions relatives de dues rectes', 'Posiciones relativas de dos rectas', 'Relative positions of two lines'),
  P(r"Dues rectes d'un pla poden ser:", r"Dos rectas de un plano pueden ser:", r"Two lines in a plane can be:")
  + ul(L(r"<strong>Secants</strong>: es tallen en un únic punt.", r"<strong>Secantes</strong>: se cortan en un único punto.", r"<strong>Intersecting</strong>: they cross at exactly one point."),
       L(r"<strong>Paral·leles</strong>: no es tallen mai; sempre estan a la mateixa distància. S'escriu \(r\parallel s\).", r"<strong>Paralelas</strong>: no se cortan nunca; siempre están a la misma distancia. Se escribe \(r\parallel s\).", r"<strong>Parallel</strong>: they never meet; they are always the same distance apart. We write \(r\parallel s\)."),
       L(r"<strong>Coincidents</strong>: són la mateixa recta (tenen tots els punts en comú).", r"<strong>Coincidentes</strong>: son la misma recta (tienen todos los puntos en común).", r"<strong>Coincident</strong>: they are the same line (all their points are shared)."))
  + P(r"Quan dues rectes secants formen quatre angles iguals (quatre <strong>angles rectes</strong>), diem que són <strong>perpendiculars</strong>: \(r\perp s\). L'angle recte el marquem amb un quadradet.",
      r"Cuando dos rectas secantes forman cuatro ángulos iguales (cuatro <strong>ángulos rectos</strong>), decimos que son <strong>perpendiculares</strong>: \(r\perp s\). El ángulo recto lo marcamos con un cuadradito.",
      r"When two intersecting lines form four equal angles (four <strong>right angles</strong>), we say they are <strong>perpendicular</strong>: \(r\perp s\). A right angle is marked with a little square.")
  + figs(F_SEC, F_PAR, F_PERP, three=True)
  + note(r"Al teu voltant n'hi ha molts exemples: els rails del tren són paral·lels; les vores d'un full es tallen perpendicularment a les cantonades; els carrers d'una cruïlla són secants.",
         r"A tu alrededor hay muchos ejemplos: los raíles del tren son paralelos; los bordes de una hoja se cortan perpendicularmente en las esquinas; las calles de un cruce son secantes.",
         r"There are lots of examples around you: railway tracks are parallel; the edges of a sheet of paper meet at right angles at the corners; the streets at a crossroads intersect.", '🚆')
  + widget('w-pos', '📏', L('Gira i mou la recta s', 'Gira y mueve la recta s', 'Turn and move line s'),
           ['<div class="wrow">' + rng('a', 0, 180, 5, 30, L('angle', 'ángulo', 'angle')) + rng('d', -3, 3, 0.5, 1, L('desplaçament', 'desplazamiento', 'shift')) + '</div>',
            quick([('0|1', L('Paral·leles', 'Paralelas', 'Parallel')), ('90|0', L('Perpendiculars', 'Perpendiculares', 'Perpendicular')), ('0|0', L('Coincidents', 'Coincidentes', 'Coincident')), ('45|-1', L('Secants', 'Secantes', 'Intersecting'))])])
  + drill('pos', 'Entrena: posicions de dues rectes', 'Entrena: posiciones de dos rectas', 'Train: positions of two lines', mode='opts'))
s2 += box('prop', L("Distància d'un punt a una recta", 'Distancia de un punto a una recta', 'Distance from a point to a line'),
  P(r"La <strong>distància</strong> d'un punt \(P\) a una recta \(r\) és la longitud del segment <strong>perpendicular</strong> que va de \(P\) fins a la recta. És el camí més curt entre el punt i la recta.",
    r"La <strong>distancia</strong> de un punto \(P\) a una recta \(r\) es la longitud del segmento <strong>perpendicular</strong> que va de \(P\) hasta la recta. Es el camino más corto entre el punto y la recta.",
    r"The <strong>distance</strong> from a point \(P\) to a line \(r\) is the length of the <strong>perpendicular</strong> segment from \(P\) to the line. It's the shortest path between the point and the line.")
  + figs(G([('ln', (-0.4, 0), (4.4, 0), '', 'b'), lab((4.3, 0), 'r', 0, 16), ('seg', (1.6, 1.8), (0.2, 0), 'd'), ('seg', (1.6, 1.8), (3.6, 0), 'd'), ('seg', (1.6, 1.8), (1.6, 0), 'hl'), ('ra', (1.6, 0), (2.4, 0), (1.6, 1)),
            ('dot', (1.6, 1.8)), lab((1.6, 1.8), 'P', 0, -10), ('dot', (1.6, 0)), lab((1.6, 1.0), 'd', 10, 4, 'hot')], W=240, pad=20,
           cap=L('El segment perpendicular és el més curt', 'El segmento perpendicular es el más corto', 'The perpendicular segment is the shortest'))))
F_MED = G([('seg', (0, 0), (4, 0), ''), ('dot', (0, 0)), lab((0, 0), 'A', -8, 16), ('dot', (4, 0)), lab((4, 0), 'B', 8, 16), ('ln', (2, -1.4), (2, 2.6), 'hl', 'b'), ('ra', (2, 0), (3, 0), (2, 1)),
           ('tick', (0, 0), (2, 0), 1), ('tick', (2, 0), (4, 0), 1), ('dot', (2, 0)), lab((2, 0), 'M', 10, 16), ('seg', (0, 0), (2, 1.8), 'd'), ('seg', (4, 0), (2, 1.8), 'd'), ('tick', (0, 0), (2, 1.8), 2), ('tick', (4, 0), (2, 1.8), 2),
           ('dot', (2, 1.8), 'pa'), lab((2, 1.8), 'P', 12, 0), lab((2, 2.5), 'm', 12, 4, 'hot')], W=230, pad=20,
          cap=L('La mediatriu m del segment AB', 'La mediatriz m del segmento AB', 'The perpendicular bisector m of AB'))
s2 += box('def', L("Mediatriu d'un segment", 'Mediatriz de un segmento', 'Perpendicular bisector of a segment'),
  P(r"La <strong>mediatriu</strong> d'un segment \(\overline{AB}\) és la recta <strong>perpendicular</strong> al segment que passa pel seu <strong>punt mitjà</strong> \(M\).",
    r"La <strong>mediatriz</strong> de un segmento \(\overline{AB}\) es la recta <strong>perpendicular</strong> al segmento que pasa por su <strong>punto medio</strong> \(M\).",
    r"The <strong>perpendicular bisector</strong> of a segment \(\overline{AB}\) is the line <strong>perpendicular</strong> to the segment through its <strong>midpoint</strong> \(M\).")
  + P(r"<strong>Propietat:</strong> cada punt \(P\) de la mediatriu està a la <strong>mateixa distància</strong> (equidista) dels dos extrems: \(PA=PB\).",
      r"<strong>Propiedad:</strong> cada punto \(P\) de la mediatriz está a la <strong>misma distancia</strong> (equidista) de los dos extremos: \(PA=PB\).",
      r"<strong>Property:</strong> every point \(P\) on the perpendicular bisector is the <strong>same distance</strong> from both endpoints: \(PA=PB\).")
  + figs(F_MED)
  + P(r"<strong>Com es construïx amb regle i compàs:</strong>", r"<strong>Cómo se construye con regla y compás:</strong>", r"<strong>How to construct it with ruler and compass:</strong>")
  + ol(L(r"Obri el compàs una mica més de la meitat del segment.", r"Abre el compás algo más de la mitad del segmento.", r"Open the compass a little more than half the segment."),
       L(r"Punxa en \(A\) i traça un arc per damunt i per davall del segment.", r"Pincha en \(A\) y traza un arco por encima y por debajo del segmento.", r"Put the point on \(A\) and draw an arc above and below the segment."),
       L(r"Sense canviar l'obertura, punxa en \(B\) i traça un altre arc que talle els anteriors.", r"Sin cambiar la abertura, pincha en \(B\) y traza otro arco que corte los anteriores.", r"Without changing the opening, put the point on \(B\) and draw another arc crossing the first ones."),
       L(r"Unix amb el regle els dos punts de tall: aquesta recta és la mediatriu.", r"Une con la regla los dos puntos de corte: esa recta es la mediatriz.", r"Join the two crossing points with the ruler: that line is the perpendicular bisector."))
  + widget('w-medi', '🧭', L('Mou el punt P per la mediatriu', 'Mueve el punto P por la mediatriz', 'Move point P along the bisector'),
           ['<div class="wrow">' + rng('p', -3, 4, 0.25, 1.5, 'P') + '</div>', seg([('m', L('P sobre la mediatriu', 'P sobre la mediatriz', 'P on the bisector')), ('f', L('P fora de la mediatriu', 'P fuera de la mediatriz', 'P off the bisector'))])]))
s2 += levels(
 [prob(L(r"Digues si són secants, paral·leles o perpendiculars: a) les dues vores llargues d'una regla; b) la vora de la pissarra i la paret del costat; c) les dues agulles d'un rellotge a les 3 en punt; d) les agulles a la 1 en punt.",
         r"Di si son secantes, paralelas o perpendiculares: a) los dos bordes largos de una regla; b) el borde de la pizarra y la pared de al lado; c) las dos agujas de un reloj a las 3 en punto; d) las agujas a la 1 en punto.",
         r"Say whether they are intersecting, parallel or perpendicular: a) the two long edges of a ruler; b) the edge of the board and the side wall; c) the two hands of a clock at 3 o'clock; d) the hands at 1 o'clock."),
       P(r"a) <strong>Paral·leles</strong>. b) <strong>Perpendiculars</strong> (es tallen formant angles rectes). c) <strong>Perpendiculars</strong>: a les 3 en punt les agulles formen un angle recte. d) <strong>Secants</strong> (no perpendiculars).",
         r"a) <strong>Paralelas</strong>. b) <strong>Perpendiculares</strong> (se cortan formando ángulos rectos). c) <strong>Perpendiculares</strong>: a las 3 en punto las agujas forman un ángulo recto. d) <strong>Secantes</strong> (no perpendiculares).",
         r"a) <strong>Parallel</strong>. b) <strong>Perpendicular</strong> (they meet at right angles). c) <strong>Perpendicular</strong>: at 3 o'clock the hands form a right angle. d) <strong>Intersecting</strong> (not perpendicular)."))],
 [prob(L(r"Dues cases estan situades en els punts \(A\) i \(B\). L'ajuntament vol posar un fanal que estiga a la mateixa distància de les dues cases. On el pot posar?",
         r"Dos casas están situadas en los puntos \(A\) y \(B\). El ayuntamiento quiere poner una farola que esté a la misma distancia de las dos casas. ¿Dónde la puede poner?",
         r"Two houses stand at points \(A\) and \(B\). The council wants a lamppost the same distance from both houses. Where can it go?"),
       P(r"Els punts que equidisten de \(A\) i de \(B\) són els de la <strong>mediatriu</strong> del segment \(\overline{AB}\). El fanal es pot posar en <strong>qualsevol punt de la mediatriu</strong>: hi ha infinites possibilitats.",
         r"Los puntos que equidistan de \(A\) y de \(B\) son los de la <strong>mediatriz</strong> del segmento \(\overline{AB}\). La farola se puede poner en <strong>cualquier punto de la mediatriz</strong>: hay infinitas posibilidades.",
         r"The points equidistant from \(A\) and \(B\) are those on the <strong>perpendicular bisector</strong> of \(\overline{AB}\). The lamppost can go <strong>anywhere on the bisector</strong>: there are infinitely many options."))],
 [prob(L(r"Tres pobles \(A\), \(B\) i \(C\) no estan alineats. Volen construir un dipòsit d'aigua que estiga a la mateixa distància dels tres pobles. Com es troba el lloc?",
         r"Tres pueblos \(A\), \(B\) y \(C\) no están alineados. Quieren construir un depósito de agua que esté a la misma distancia de los tres pueblos. ¿Cómo se encuentra el lugar?",
         r"Three villages \(A\), \(B\) and \(C\) are not collinear. They want to build a water tank the same distance from all three. How do we find the spot?"),
       P(r"Els punts que equidisten de \(A\) i \(B\) estan en la mediatriu de \(\overline{AB}\); els que equidisten de \(B\) i \(C\), en la mediatriu de \(\overline{BC}\).",
         r"Los puntos que equidistan de \(A\) y \(B\) están en la mediatriz de \(\overline{AB}\); los que equidistan de \(B\) y \(C\), en la mediatriz de \(\overline{BC}\).",
         r"Points equidistant from \(A\) and \(B\) lie on the bisector of \(\overline{AB}\); those equidistant from \(B\) and \(C\), on the bisector of \(\overline{BC}\)."),
       P(r"El dipòsit s'ha de posar en el <strong>punt on es tallen les dues mediatrius</strong>: està a la mateixa distància de \(A\) i \(B\), i de \(B\) i \(C\), per tant dels tres pobles. (En l'apartat 7.7 veurem que aquest punt s'anomena <em>circumcentre</em>.)",
         r"El depósito se debe poner en el <strong>punto donde se cortan las dos mediatrices</strong>: está a la misma distancia de \(A\) y \(B\), y de \(B\) y \(C\), por tanto de los tres pueblos. (En el apartado 7.7 veremos que este punto se llama <em>circuncentro</em>.)",
         r"The tank must go at the <strong>point where the two bisectors cross</strong>: it is equidistant from \(A\) and \(B\), and from \(B\) and \(C\), so from all three villages. (In section 7.7 we'll see this point is called the <em>circumcentre</em>.)"))])
s2 += practice([
  ('★☆☆', L(r"Dibuixa una recta \(r\) i un punt \(P\) fora d'ella. Traça la recta paral·lela i la recta perpendicular a \(r\) que passen per \(P\).", r"Dibuja una recta \(r\) y un punto \(P\) fuera de ella. Traza la recta paralela y la recta perpendicular a \(r\) que pasan por \(P\).", r"Draw a line \(r\) and a point \(P\) not on it. Draw the parallel and the perpendicular to \(r\) through \(P\).")),
  ('★★☆', L(r"Si \(r\parallel s\) i \(s\parallel t\), com són \(r\) i \(t\)? I si \(r\perp s\) i \(s\perp t\)?", r"Si \(r\parallel s\) y \(s\parallel t\), ¿cómo son \(r\) y \(t\)? ¿Y si \(r\perp s\) y \(s\perp t\)?", r"If \(r\parallel s\) and \(s\parallel t\), how are \(r\) and \(t\) related? And if \(r\perp s\) and \(s\perp t\)?"))],
  ol(L(r"Amb l'escaire i el cartabó: la paral·lela es fa lliscant l'escaire sobre el cartabó; la perpendicular, recolzant un catet de l'escaire en \(r\).", r"Con la escuadra y el cartabón: la paralela se hace deslizando la escuadra sobre el cartabón; la perpendicular, apoyando un cateto de la escuadra en \(r\).", r"With set squares: slide one along the other for the parallel; rest one short side on \(r\) for the perpendicular."),
     L(r"En els dos casos, \(r\parallel t\) (dues rectes perpendiculars a una mateixa recta són paral·leles entre si).", r"En los dos casos, \(r\parallel t\) (dos rectas perpendiculares a una misma recta son paralelas entre sí).", r"In both cases \(r\parallel t\) (two lines perpendicular to the same line are parallel to each other).")))

# =====================================================================
# 7.3 Angles: elements, mesura i classificació. Bisectriu
# =====================================================================
ANG = [(0, 0.001, 'nul', 'nulo', 'zero', r'0^\circ'), (35, None, 'agut', 'agudo', 'acute', r'<90^\circ'), (90, None, 'recte', 'recto', 'right', r'90^\circ'), (130, None, 'obtús', 'obtuso', 'obtuse', r'90^\circ\text{–}180^\circ'),
       (180, None, 'pla', 'llano', 'straight', r'180^\circ'), (250, None, 'còncau', 'cóncavo', 'reflex', r'>180^\circ'), (360, None, 'complet', 'completo', 'full turn', r'360^\circ')]
def angf(a):
    if a == 0: it = [('ln', (0, 0), (1.6, 0), '', 'e'), ('ln', (0, 0.06), (1.6, 0.06), '', ''), ('dot', (0, 0))]
    elif a == 360: it = [('circ', (0, 0), 0.5, 'af'), ('ln', (0, 0), (1.6, 0), '', 'e'), ('dot', (0, 0))]
    else: it = angfig((0, 0), 0, a, R=0.5)
    if a == 90: it[0] = ('poly', [(0, 0), (0.4, 0), (0.4, 0.4), (0, 0.4)], 'af')
    return it + [('txt', (-1.6, -1.6), ' ', {}), ('txt', (1.6, 1.6), ' ', {})]
s3 = box('def', L('Què és un angle?', '¿Qué es un ángulo?', 'What is an angle?'),
  P(r"Un <strong>angle</strong> és la regió del pla limitada per dues <strong>semirectes</strong> que tenen el mateix origen. Les semirectes són els <strong>costats</strong> de l'angle i l'origen comú n'és el <strong>vèrtex</strong>.",
    r"Un <strong>ángulo</strong> es la región del plano limitada por dos <strong>semirrectas</strong> que tienen el mismo origen. Las semirrectas son los <strong>lados</strong> del ángulo y el origen común es su <strong>vértice</strong>.",
    r"An <strong>angle</strong> is the region of the plane bounded by two <strong>rays</strong> with the same starting point. The rays are the <strong>sides</strong> of the angle and the common starting point is its <strong>vertex</strong>.")
  + figs(G(angfig((0, 0), 10, 60, r=2.2, R=0.7, lab=r'α') + [('dot', pol((0, 0), 1.7, 10)), lab(pol((0, 0), 1.7, 10), 'A', 0, 16), ('dot', pol((0, 0), 1.7, 60)), lab(pol((0, 0), 1.7, 60), 'B', -10, 0),
            lab((0, 0), 'O', -10, 14), lab(pol((0, 0), 2.5, 22), Ls('costat', 'lado', 'side'), 0, 4), lab(pol((0, 0), 2.3, 70), Ls('costat', 'lado', 'side'), 0, 4), lab((0.15, -0.45), Ls('vèrtex', 'vértice', 'vertex'), 0, 4)], W=240, pad=26,
           cap=L(r'L\'angle \(\widehat{AOB}\) o \(\hat O\) o \(\alpha\)', r'El ángulo \(\widehat{AOB}\) o \(\hat O\) o \(\alpha\)', r'The angle \(\widehat{AOB}\) or \(\hat O\) or \(\alpha\)')))
  + P(r"Un angle es pot anomenar amb tres lletres, amb la del vèrtex al mig (\(\widehat{AOB}\)), només amb la lletra del vèrtex (\(\hat O\)) o amb una lletra grega (\(\alpha\) alfa, \(\beta\) beta, \(\gamma\) gamma…).",
      r"Un ángulo se puede nombrar con tres letras, con la del vértice en medio (\(\widehat{AOB}\)), solo con la letra del vértice (\(\hat O\)) o con una letra griega (\(\alpha\) alfa, \(\beta\) beta, \(\gamma\) gamma…).",
      r"An angle can be named with three letters, the vertex in the middle (\(\widehat{AOB}\)), with just the vertex letter (\(\hat O\)) or with a Greek letter (\(\alpha\) alpha, \(\beta\) beta, \(\gamma\) gamma…).")
  + P(r"Els angles es mesuren en <strong>graus</strong> (\(^\circ\)). Si dividim una volta completa en 360 parts iguals, cadascuna és un grau: una volta completa fa \(360^\circ\), mitja volta \(180^\circ\) i un quart de volta \(90^\circ\). La mesura d'un angle <strong>no depén</strong> de la llargària dels costats que dibuixem.",
      r"Los ángulos se miden en <strong>grados</strong> (\(^\circ\)). Si dividimos una vuelta completa en 360 partes iguales, cada una es un grado: una vuelta completa mide \(360^\circ\), media vuelta \(180^\circ\) y un cuarto de vuelta \(90^\circ\). La medida de un ángulo <strong>no depende</strong> de la longitud de los lados que dibujemos.",
      r"Angles are measured in <strong>degrees</strong> (\(^\circ\)). Split a full turn into 360 equal parts and each one is a degree: a full turn is \(360^\circ\), half a turn \(180^\circ\) and a quarter turn \(90^\circ\). The size of an angle <strong>doesn't depend</strong> on how long we draw its sides."))
s3 += box('prop', L('Mesurar amb el transportador', 'Medir con el transportador', 'Measuring with a protractor'),
  ol(L(r"Col·loca el <strong>centre</strong> del transportador damunt del <strong>vèrtex</strong> de l'angle.", r"Coloca el <strong>centro</strong> del transportador encima del <strong>vértice</strong> del ángulo.", r"Place the protractor's <strong>centre</strong> on the angle's <strong>vertex</strong>."),
     L(r"Fes coincidir la línia del \(0^\circ\) amb un dels costats.", r"Haz coincidir la línea del \(0^\circ\) con uno de los lados.", r"Line up the \(0^\circ\) line with one of the sides."),
     L(r"Llig el nombre per on passa l'altre costat, en l'escala que comença en 0 en el primer costat.", r"Lee el número por donde pasa el otro lado, en la escala que empieza en 0 en el primer lado.", r"Read the number where the other side crosses, on the scale that starts at 0 on the first side."))
  + note(r"El transportador té dues escales (una per dins i una per fora). Abans de llegir, pregunta't si l'angle és més gran o més menut que un angle recte: així no confondràs \(50^\circ\) amb \(130^\circ\).",
         r"El transportador tiene dos escalas (una por dentro y otra por fuera). Antes de leer, pregúntate si el ángulo es mayor o menor que un ángulo recto: así no confundirás \(50^\circ\) con \(130^\circ\).",
         r"A protractor has two scales (inner and outer). Before reading, ask yourself whether the angle is bigger or smaller than a right angle, so you won't mix up \(50^\circ\) and \(130^\circ\)."))
s3 += box('def', L('Classificació dels angles', 'Clasificación de los ángulos', 'Types of angles'),
  figs(*[G(angf(a), W=150, pad=10, cap='<strong>' + L(va, es, en) + r'</strong> \(' + m + r'\)') for a, _, va, es, en, m in ANG], three=True)
  + P(r"Els angles més menuts que un angle pla (\(\le180^\circ\)) s'anomenen <strong>convexos</strong>; els més grans que un angle pla, <strong>còncaus</strong>. Dues semirectes amb el mateix origen formen sempre dos angles: un de convex i un de còncau, que sumen \(360^\circ\).",
      r"Los ángulos menores que un ángulo llano (\(\le180^\circ\)) se llaman <strong>convexos</strong>; los mayores que un ángulo llano, <strong>cóncavos</strong>. Dos semirrectas con el mismo origen forman siempre dos ángulos: uno convexo y uno cóncavo, que suman \(360^\circ\).",
      r"Angles up to a straight angle (\(\le180^\circ\)) are called <strong>convex</strong>; bigger ones are <strong>reflex</strong> (concave). Two rays from the same point always form two angles, one convex and one reflex, adding up to \(360^\circ\).")
  + widget('w-ang', '📐', L('Obri l\'angle', 'Abre el ángulo', 'Open the angle'),
           ['<div class="wrow">' + rng('a', 0, 360, 1, 50, 'α') + '</div>', seg([('a', L('Angle', 'Ángulo', 'Angle')), ('b', L('Amb la bisectriu', 'Con la bisectriz', 'With the bisector'))]),
            quick([('0', '0°'), ('45', '45°'), ('90', '90°'), ('120', '120°'), ('180', '180°'), ('270', '270°'), ('360', '360°')])])
  + drill('cls', "Entrena: classifica l'angle", 'Entrena: clasifica el ángulo', 'Train: classify the angle', mode='opts'))
F_BIS = G(angfig((0, 0), 0, 80, r=2.3, R=0.6) + [('sect', (0, 0), 0.9, 0, 40, 'af2'), ('ln', (0, 0), pol((0, 0), 2.3, 40), 'hl', 'e'), ('dot', pol((0, 0), 1.6, 40), 'pa'), ('seg', pol((0, 0), 1.6, 40), (1.6 * math.cos(math.radians(40)), 0), 'd'),
           ('seg', pol((0, 0), 1.6, 40), pol((0, 0), 1.6 * math.cos(math.radians(40)), 80), 'd'), ('ra', (1.6 * math.cos(math.radians(40)), 0), (2, 0), pol((0, 0), 1.6, 40)),
           ('ra', pol((0, 0), 1.6 * math.cos(math.radians(40)), 80), (0, 0), pol((0, 0), 1.6, 40)), lab(pol((0, 0), 2.45, 40), 'b', 6, 0, 'hot')], W=220, pad=20,
          cap=L('La bisectriu b dividix l\'angle en dos angles iguals', 'La bisectriz b divide el ángulo en dos ángulos iguales', 'The bisector b splits the angle into two equal angles'))
s3 += box('def', L("Bisectriu d'un angle", 'Bisectriz de un ángulo', 'Angle bisector'),
  P(r"La <strong>bisectriu</strong> d'un angle és la semirecta que ix del vèrtex i el dividix en <strong>dos angles iguals</strong>. Si l'angle fa \(80^\circ\), cada meitat fa \(40^\circ\).",
    r"La <strong>bisectriz</strong> de un ángulo es la semirrecta que sale del vértice y lo divide en <strong>dos ángulos iguales</strong>. Si el ángulo mide \(80^\circ\), cada mitad mide \(40^\circ\).",
    r"The <strong>bisector</strong> of an angle is the ray from the vertex that splits it into <strong>two equal angles</strong>. If the angle is \(80^\circ\), each half is \(40^\circ\).")
  + P(r"<strong>Propietat:</strong> cada punt de la bisectriu està a la mateixa distància dels dos costats de l'angle.",
      r"<strong>Propiedad:</strong> cada punto de la bisectriz está a la misma distancia de los dos lados del ángulo.",
      r"<strong>Property:</strong> every point on the bisector is the same distance from both sides of the angle.")
  + figs(F_BIS)
  + P(r"<strong>Construcció amb compàs:</strong> punxa en el vèrtex i traça un arc que talle els dos costats; des de cada punt de tall traça un arc (amb la mateixa obertura) de manera que es tallen; unix el vèrtex amb aquest punt.",
      r"<strong>Construcción con compás:</strong> pincha en el vértice y traza un arco que corte los dos lados; desde cada punto de corte traza un arco (con la misma abertura) de manera que se corten; une el vértice con ese punto.",
      r"<strong>Construction with compasses:</strong> put the point on the vertex and draw an arc crossing both sides; from each crossing draw an arc (same opening) so that they meet; join the vertex to that point."))
s3 += levels(
 [prob(L(r"Classifica els angles: \(35^\circ\), \(90^\circ\), \(145^\circ\), \(180^\circ\), \(220^\circ\) i \(89^\circ\).", r"Clasifica los ángulos: \(35^\circ\), \(90^\circ\), \(145^\circ\), \(180^\circ\), \(220^\circ\) y \(89^\circ\).", r"Classify the angles: \(35^\circ\), \(90^\circ\), \(145^\circ\), \(180^\circ\), \(220^\circ\) and \(89^\circ\)."),
       P(r"\(35^\circ\): agut. \(90^\circ\): recte. \(145^\circ\): obtús. \(180^\circ\): pla. \(220^\circ\): còncau. \(89^\circ\): agut (per poc, però és més menut que \(90^\circ\)).",
         r"\(35^\circ\): agudo. \(90^\circ\): recto. \(145^\circ\): obtuso. \(180^\circ\): llano. \(220^\circ\): cóncavo. \(89^\circ\): agudo (por poco, pero es menor que \(90^\circ\)).",
         r"\(35^\circ\): acute. \(90^\circ\): right. \(145^\circ\): obtuse. \(180^\circ\): straight. \(220^\circ\): reflex. \(89^\circ\): acute (only just, but it's less than \(90^\circ\))."))],
 [prob(L(r"Quin angle formen les agulles d'un rellotge a les 3 en punt? I a les 6? I a les 2?", r"¿Qué ángulo forman las agujas de un reloj a las 3 en punto? ¿Y a las 6? ¿Y a las 2?", r"What angle do a clock's hands make at 3 o'clock? At 6? At 2?"),
       P(r"Les 12 hores omplin una volta completa: entre dos nombres consecutius de l'esfera hi ha \(360^\circ:12=30^\circ\).",
         r"Las 12 horas llenan una vuelta completa: entre dos números consecutivos de la esfera hay \(360^\circ:12=30^\circ\).",
         r"The 12 hours fill a full turn: between two consecutive numbers on the dial there are \(360^\circ:12=30^\circ\)."),
       D(r"3\text{ h}: 3\cdot30^\circ=\boxed{90^\circ}\qquad 6\text{ h}: 6\cdot30^\circ=\boxed{180^\circ}\qquad 2\text{ h}: 2\cdot30^\circ=\boxed{60^\circ}"))],
 [prob(L(r"La bisectriu d'un angle forma amb un dels costats un angle de \(37^\circ\). Quant mesura l'angle? Com és?", r"La bisectriz de un ángulo forma con uno de los lados un ángulo de \(37^\circ\). ¿Cuánto mide el ángulo? ¿Cómo es?", r"An angle's bisector makes a \(37^\circ\) angle with one of the sides. How big is the angle? What type is it?"),
       P(r"La bisectriu dividix l'angle en dues meitats iguals, així que l'angle sencer és el doble:", r"La bisectriz divide el ángulo en dos mitades iguales, así que el ángulo entero es el doble:", r"The bisector splits the angle into two equal halves, so the whole angle is double:"),
       D(r"2\cdot37^\circ=\boxed{74^\circ}\quad\text{%s}" % Lt('(agut)', '(agudo)', '(acute)')))])
ck(360 // 12, 30); ck(2 * 37, 74)
s3 += practice([
  ('★☆☆', L(r"Quin angle forma la recta perpendicular a una altra amb ella? I mitja volta?", r"¿Qué ángulo forma la recta perpendicular a otra con ella? ¿Y media vuelta?", r"What angle does a perpendicular make with its line? And half a turn?")),
  ('★★☆', L(r"Quants graus gira l'agulla dels minuts en 20 minuts? I en 45 minuts?", r"¿Cuántos grados gira la aguja de los minutos en 20 minutos? ¿Y en 45 minutos?", r"How many degrees does the minute hand turn in 20 minutes? In 45 minutes?")),
  ('★★☆', L(r"Dues semirectes amb el mateix origen formen un angle convex de \(110^\circ\). Quant mesura l'angle còncau que formen?", r"Dos semirrectas con el mismo origen forman un ángulo convexo de \(110^\circ\). ¿Cuánto mide el ángulo cóncavo que forman?", r"Two rays from the same point make a convex angle of \(110^\circ\). How big is the reflex angle they make?"))],
  ol(r"\(90^\circ\); \(180^\circ\)", L(r"Cada minut, \(360^\circ:60=6^\circ\): \(20\cdot6^\circ=120^\circ\) i \(45\cdot6^\circ=270^\circ\)", r"Cada minuto, \(360^\circ:60=6^\circ\): \(20\cdot6^\circ=120^\circ\) y \(45\cdot6^\circ=270^\circ\)", r"Each minute, \(360^\circ:60=6^\circ\): \(20\cdot6^\circ=120^\circ\) and \(45\cdot6^\circ=270^\circ\)"),
     r"\(360^\circ-110^\circ=250^\circ\)"))
ck(20 * 6, 120); ck(45 * 6, 270); ck(360 - 110, 250)

# =====================================================================
# 7.4 Mesura d'angles: el sistema sexagesimal
# =====================================================================
def vcol(rows, sep=None):
    """operació en columna amb graus, minuts i segons (cada fila: (signe, d, m, s) amb cadenes); sep: fila davall de la qual va la ratlla"""
    out = ''
    for i, r in enumerate(rows):
        out += '%s & %s & %s & %s' % r
        if i < len(rows) - 1: out += r'\\' + (r' \hline ' if sep == i else '')
    return r'\begin{array}{rrrr}' + out + r'\end{array}'
def deg(x): return r'%s^\circ' % x
s4 = box('def', L('Graus, minuts i segons', 'Grados, minutos y segundos', 'Degrees, minutes and seconds'),
  P(r"Per a mesurar angles amb més precisió dividim el grau en parts més menudes, de 60 en 60, com les hores del rellotge. Per això diem que és un <strong>sistema sexagesimal</strong>:",
    r"Para medir ángulos con más precisión dividimos el grado en partes más pequeñas, de 60 en 60, como las horas del reloj. Por eso decimos que es un <strong>sistema sexagesimal</strong>:",
    r"To measure angles more precisely we split the degree into smaller parts, in sixties, like the hours on a clock. That's why it's called a <strong>sexagesimal system</strong>:")
  + D(r"1^\circ=60'\ (\text{%s})\qquad 1'=60''\ (\text{%s})\qquad 1^\circ=3600''" % (Lt('minuts', 'minutos', 'minutes'), Lt('segons', 'segundos', 'seconds')))
  + P(r"Un angle està en <strong>forma complexa</strong> si s'expressa amb diverses unitats (\(25^\circ\,14'\,36''\)) i en <strong>forma incomplexa</strong> si s'expressa amb una sola unitat (\(90\,876''\)). En forma complexa, els minuts i els segons han de ser més menuts que 60.",
      r"Un ángulo está en <strong>forma compleja</strong> si se expresa con varias unidades (\(25^\circ\,14'\,36''\)) y en <strong>forma incompleja</strong> si se expresa con una sola unidad (\(90\,876''\)). En forma compleja, los minutos y los segundos deben ser menores que 60.",
      r"An angle is in <strong>compound form</strong> when it uses several units (\(25^\circ\,14'\,36''\)) and in <strong>simple form</strong> when it uses only one (\(90\,876''\)). In compound form, minutes and seconds must be less than 60.")
  + figs(G([('txt', (0, 1), '× 60', {'cls': 'hot'}), ('txt', (2, 1), '× 60', {'cls': 'hot'}), ('txt', (-1, 0), Ls('graus', 'grados', 'degrees'), {'cls': 'big'}), ('txt', (1, 0), Ls('minuts', 'minutos', 'minutes'), {'cls': 'big'}), ('txt', (3, 0), Ls('segons', 'segundos', 'seconds'), {'cls': 'big'}),
            ('ln', (-0.45, 0.55), (0.45, 0.55), 'hl', 'e'), ('ln', (1.55, 0.55), (2.45, 0.55), 'hl', 'e'), ('ln', (0.45, -0.55), (-0.45, -0.55), '', 'e'), ('ln', (2.45, -0.55), (1.55, -0.55), '', 'e'),
            ('txt', (0, -1), ': 60', {'cls': 'big'}), ('txt', (2, -1), ': 60', {'cls': 'big'})], W=300, pad=34, maxh=150)))
t1 = sx(25, 14, 36); assert t1 == 90876
s4 += box('prop', L('Pas de forma complexa a incomplexa', 'Paso de forma compleja a incompleja', 'Compound to simple form'),
  P(r"Per a passar a una unitat més menuda <strong>multipliquem</strong> per 60 (o per 3600 dels graus als segons) i després sumem:",
    r"Para pasar a una unidad más pequeña <strong>multiplicamos</strong> por 60 (o por 3600 de grados a segundos) y después sumamos:",
    r"To change to a smaller unit we <strong>multiply</strong> by 60 (or by 3600 from degrees to seconds) and then add:")
  + D(r"25^\circ\,14'\,36''=25\cdot3600''+14\cdot60''+36''=90\,000''+840''+36''=\boxed{90\,876''}")
  + D(r"12^\circ\,35'=12\cdot60'+35'=720'+35'=\boxed{755'}")
  + note(r"Els graus amb decimals també es poden passar a minuts: \(12{,}5^\circ=12^\circ+0{,}5\cdot60'=12^\circ\,30'\).",
         r"Los grados con decimales también se pueden pasar a minutos: \(12{,}5^\circ=12^\circ+0{,}5\cdot60'=12^\circ\,30'\).",
         r"Degrees with decimals can also be changed into minutes: \(12.5^\circ=12^\circ+0.5\cdot60'=12^\circ\,30'\)."))
ck(12 * 60 + 35, 755)
assert dms(7385) == (2, 3, 5) and 7385 // 60 == 123 and 7385 % 60 == 5 and 123 // 60 == 2 and 123 % 60 == 3
s4 += box('prop', L('Pas de forma incomplexa a complexa', 'Paso de forma incompleja a compleja', 'Simple to compound form'),
  P(r"Per a passar a una unitat més gran <strong>dividim</strong> entre 60. El residu són les unitats que queden i el quocient es torna a dividir:",
    r"Para pasar a una unidad mayor <strong>dividimos</strong> entre 60. El resto son las unidades que quedan y el cociente se vuelve a dividir:",
    r"To change to a bigger unit we <strong>divide</strong> by 60. The remainder is what's left in that unit and the quotient is divided again:")
  + D(r"7385'':60=123'\ \ \text{%s}\ 5''\qquad 123':60=2^\circ\ \ \text{%s}\ 3'" % (Lt('i sobren', 'y sobran', 'remainder'), Lt('i sobren', 'y sobran', 'remainder')))
  + D(r"7385''=\boxed{2^\circ\,3'\,5''}")
  + widget('w-sexa', '🔄', L('Convertidor sexagesimal', 'Conversor sexagesimal', 'Sexagesimal converter'),
           [seg([('c', L('Complexa → incomplexa', 'Compleja → incompleja', 'Compound → simple')), ('i', L('Incomplexa → complexa', 'Incompleja → compleja', 'Simple → compound'))]),
            '<div class="wrow sx-c">' + tin('d', '', '25', 's') + '° ' + tin('m', '', '14', 's') + "' " + tin('s', '', '36', 's') + "''</div>",
            '<div class="wrow sx-i">' + tin('n', '', '7385', 'm') + seg([('s', L('segons', 'segundos', 'seconds')), ('m', L('minuts', 'minutos', 'minutes'))]).replace('<div class="wrow">', '').replace('</div></div>', '</div>') + '</div>'],
           out='<div class="hsteps"></div>')
  + drill('sxs', 'Entrena: passa a segons', 'Entrena: pasa a segundos', 'Train: convert to seconds', mode='int')
  + drill('sxc', 'Entrena: passa a forma complexa', 'Entrena: pasa a forma compleja', 'Train: convert to compound form', mode='sx'))

# operacions
a_, b_ = sx(37, 48, 25), sx(25, 26, 50); r_ = a_ + b_; assert dms(r_) == (63, 15, 15)
c_, d_ = sx(50, 15, 10), sx(23, 40, 35); e_ = c_ - d_; assert dms(e_) == (26, 34, 35)
f_ = sx(15, 24, 37) * 3; assert dms(f_) == (46, 13, 51)
g_ = sx(125, 17); assert g_ % 4 == 0 and dms(g_ // 4) == (31, 19, 15)
s4 += box('prop', L('Operacions amb angles', 'Operaciones con ángulos', 'Operations with angles'),
  P(r"<strong>Suma.</strong> Col·loquem graus davall de graus, minuts davall de minuts i segons davall de segons, i sumem cada columna. Si els segons o els minuts arriben a 60 o més, els convertim en la unitat següent:",
    r"<strong>Suma.</strong> Colocamos grados debajo de grados, minutos debajo de minutos y segundos debajo de segundos, y sumamos cada columna. Si los segundos o los minutos llegan a 60 o más, los convertimos en la unidad siguiente:",
    r"<strong>Addition.</strong> Line up degrees under degrees, minutes under minutes and seconds under seconds, and add each column. If the seconds or minutes reach 60 or more, carry them into the next unit:")
  + D(vcol([('', deg(37), "48'", "25''"), ('+', deg(25), "26'", "50''"), ('', deg(62), "74'", "75''")], sep=1) + r"\ \Rightarrow\ 75''=1'\,15'',\ \ 75'=1^\circ\,15'\ \Rightarrow\ \boxed{63^\circ\,15'\,15''}")
  + P(r"<strong>Resta.</strong> Si en una columna no podem restar, convertim una unitat de la columna de l'esquerra en 60 de la columna de la dreta (com quan «en portem» en la resta normal):",
      r"<strong>Resta.</strong> Si en una columna no podemos restar, convertimos una unidad de la columna de la izquierda en 60 de la columna de la derecha (como cuando «nos llevamos» en la resta normal):",
      r"<strong>Subtraction.</strong> If a column can't be subtracted, change one unit from the column on its left into 60 of the column on the right (like borrowing in ordinary subtraction):")
  + D(vcol([('', deg(50), "15'", "10''"), ('-', deg(23), "40'", "35''")], sep=1) + r"\ \to\ " + vcol([('', deg(49), "74'", "70''"), ('-', deg(23), "40'", "35''"), ('', deg(26), "34'", "35''")], sep=1) + r"\ \Rightarrow\ \boxed{26^\circ\,34'\,35''}")
  + P(r"<strong>Multiplicació per un nombre natural.</strong> Multipliquem cada unitat pel nombre i després passem els segons i minuts que sobrepassen 60 a la unitat següent:",
      r"<strong>Multiplicación por un número natural.</strong> Multiplicamos cada unidad por el número y después pasamos los segundos y minutos que sobrepasan 60 a la unidad siguiente:",
      r"<strong>Multiplying by a whole number.</strong> Multiply each unit by the number, then carry seconds and minutes over 60 into the next unit:")
  + D(r"(15^\circ\,24'\,37'')\cdot3=45^\circ\,72'\,111''=45^\circ\,73'\,51''=\boxed{46^\circ\,13'\,51''}")
  + P(r"<strong>Divisió entre un nombre natural.</strong> Dividim els graus; el residu el passem a minuts (×60) i el sumem als minuts; dividim els minuts i fem el mateix amb els segons:",
      r"<strong>División entre un número natural.</strong> Dividimos los grados; el resto lo pasamos a minutos (×60) y lo sumamos a los minutos; dividimos los minutos y hacemos lo mismo con los segundos:",
      r"<strong>Dividing by a whole number.</strong> Divide the degrees; change the remainder into minutes (×60) and add them to the minutes; divide the minutes and do the same with the seconds:")
  + D(r"125^\circ:4=31^\circ\ \text{%s}\ 1^\circ=60'" % Lt('i sobra', 'y sobra', 'remainder'))
  + D(r"(60'+17'):4=77':4=19'\ \text{%s}\ 1'=60''" % Lt('i sobra', 'y sobra', 'remainder'))
  + D(r"60'':4=15''\qquad\Rightarrow\qquad(125^\circ\,17'):4=\boxed{31^\circ\,19'\,15''}")
  + widget('w-sexop', '🧮', L('Calculadora d\'angles', 'Calculadora de ángulos', 'Angle calculator'),
           [seg([('+', L('Suma', 'Suma', 'Add')), ('-', L('Resta', 'Resta', 'Subtract')), ('*', L('Multiplica', 'Multiplica', 'Multiply')), ('/', L('Dividix', 'Divide', 'Divide'))]),
            '<div class="wrow">' + tin('d1', '', '37', 's') + '° ' + tin('m1', '', '48', 's') + "' " + tin('s1', '', '25', 's') + "''</div>",
            '<div class="wrow op-b">' + tin('d2', '', '25', 's') + '° ' + tin('m2', '', '26', 's') + "' " + tin('s2', '', '50', 's') + "''</div>",
            '<div class="wrow op-n">' + tin('k', '× / :', '3', 's') + '</div>'],
           out='<div class="hsteps"></div>')
  + drill('sxop', 'Entrena: opera amb angles', 'Entrena: opera con ángulos', 'Train: angle arithmetic', mode='sx'))
h_ = sx(45, 38) + sx(72, 49); assert dms(h_) == (118, 27, 0)
k_ = sx(90) - sx(42, 17, 35); assert dms(k_) == (47, 42, 25)
m_ = sx(180); assert m_ % 7 != 0
s4 += levels(
 [prob(L(r"Expressa en segons: a) \(3^\circ\,20'\); b) \(1^\circ\,5'\,12''\).", r"Expresa en segundos: a) \(3^\circ\,20'\); b) \(1^\circ\,5'\,12''\).", r"Write in seconds: a) \(3^\circ\,20'\); b) \(1^\circ\,5'\,12''\)."),
       D(r"\text{a) }3\cdot3600+20\cdot60=10\,800+1200=\boxed{12\,000''}\qquad\text{b) }3600+5\cdot60+12=3600+300+12=\boxed{3912''}"))],
 [prob(L(r"Calcula: a) \(45^\circ\,38'+72^\circ\,49'\); b) \(90^\circ-42^\circ\,17'\,35''\).", r"Calcula: a) \(45^\circ\,38'+72^\circ\,49'\); b) \(90^\circ-42^\circ\,17'\,35''\).", r"Work out: a) \(45^\circ\,38'+72^\circ\,49'\); b) \(90^\circ-42^\circ\,17'\,35''\)."),
       D(r"\text{a) }117^\circ\,87'=117^\circ+1^\circ\,27'=\boxed{118^\circ\,27'}"),
       P(r"b) Escrivim \(90^\circ\) com \(89^\circ\,59'\,60''\) (un grau es convertix en \(60'\), i un d'aquests minuts en \(60''\)):",
         r"b) Escribimos \(90^\circ\) como \(89^\circ\,59'\,60''\) (un grado se convierte en \(60'\), y uno de esos minutos en \(60''\)):",
         r"b) Write \(90^\circ\) as \(89^\circ\,59'\,60''\) (one degree becomes \(60'\), and one of those minutes becomes \(60''\)):"),
       D(vcol([('', deg(89), "59'", "60''"), ('-', deg(42), "17'", "35''"), ('', deg(47), "42'", "25''")], sep=1) + r"\ \Rightarrow\ \boxed{47^\circ\,42'\,25''}"))],
 [prob(L(r"Dividim un angle pla en 7 angles iguals. Quant mesura cadascun? Comprova el resultat.", r"Dividimos un ángulo llano en 7 ángulos iguales. ¿Cuánto mide cada uno? Comprueba el resultado.", r"A straight angle is split into 7 equal angles. How big is each one? Check your answer."),
       D(r"180^\circ:7=25^\circ\ \text{%s}\ 5^\circ=300'\qquad300':7=42'\ \text{%s}\ 6'=360''\qquad360'':7=51''\ \text{%s}\ 3''" % (Lt('i sobren', 'y sobran', 'rem.'), Lt('i sobren', 'y sobran', 'rem.'), Lt('i sobren', 'y sobran', 'rem.'))),
       P(r"Cada angle fa aproximadament <strong>\(25^\circ\,42'\,51''\)</strong> (sobren \(3''\), que no es poden repartir en segons sencers). Comprovació: \(7\cdot(25^\circ\,42'\,51'')+3''=175^\circ\,294'\,360''=180^\circ\ \checkmark\)",
         r"Cada ángulo mide aproximadamente <strong>\(25^\circ\,42'\,51''\)</strong> (sobran \(3''\), que no se pueden repartir en segundos enteros). Comprobación: \(7\cdot(25^\circ\,42'\,51'')+3''=175^\circ\,294'\,360''=180^\circ\ \checkmark\)",
         r"Each angle is about <strong>\(25^\circ\,42'\,51''\)</strong> (\(3''\) are left over and can't be shared in whole seconds). Check: \(7\cdot(25^\circ\,42'\,51'')+3''=175^\circ\,294'\,360''=180^\circ\ \checkmark\)"))])
ck(sx(3, 20), 12000); ck(sx(1, 5, 12), 3912); assert sx(25, 42, 51) * 7 + 3 == sx(180) and 175 * 3600 + 294 * 60 + 360 == sx(180)
s4 += practice([
  ('★☆☆', L(r"Passa a forma complexa: a) \(200'\); b) \(5000''\).", r"Pasa a forma compleja: a) \(200'\); b) \(5000''\).", r"Write in compound form: a) \(200'\); b) \(5000''\).")),
  ('★★☆', L(r"Calcula \(18^\circ\,45'\,30''+26^\circ\,34'\,40''\) i \(60^\circ\,10'-35^\circ\,25'\).", r"Calcula \(18^\circ\,45'\,30''+26^\circ\,34'\,40''\) y \(60^\circ\,10'-35^\circ\,25'\).", r"Work out \(18^\circ\,45'\,30''+26^\circ\,34'\,40''\) and \(60^\circ\,10'-35^\circ\,25'\).")),
  ('★★★', L(r"Calcula \((12^\circ\,25'\,40'')\cdot5\) i \((100^\circ\,30'):6\).", r"Calcula \((12^\circ\,25'\,40'')\cdot5\) y \((100^\circ\,30'):6\).", r"Work out \((12^\circ\,25'\,40'')\cdot5\) and \((100^\circ\,30'):6\)."))],
  ol(r"a) \(3^\circ\,20'\); b) \(1^\circ\,23'\,20''\)", r"\(45^\circ\,20'\,10''\); \(24^\circ\,45'\)", r"\(62^\circ\,8'\,20''\); \(16^\circ\,45'\)"))
assert dms(200 * 60) == (3, 20, 0) and dms(5000) == (1, 23, 20)
assert dms(sx(18, 45, 30) + sx(26, 34, 40)) == (45, 20, 10) and dms(sx(60, 10) - sx(35, 25)) == (24, 45, 0)
assert dms(sx(12, 25, 40) * 5) == (62, 8, 20) and sx(100, 30) % 6 == 0 and dms(sx(100, 30) // 6) == (16, 45, 0)
