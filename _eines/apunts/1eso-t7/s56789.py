# Apartats 7.5-7.9 dels apunts de la Unitat 7 de 1r ESO: relacions entre angles, polígons, triangles,
# quadrilàters i angles dels polígons (polígons regulars).
from comu import *

def lab(P, t, dx=0, dy=-12, cls=''): return ('txt', P, t, {'dx': dx, 'dy': dy, 'cls': cls})
def angle_at(V, A, B):
    """angle (graus) en el vèrtex V del triangle o polígon"""
    a1 = math.atan2(A[1] - V[1], A[0] - V[0]); a2 = math.atan2(B[1] - V[1], B[0] - V[0])
    d = abs(math.degrees(a1 - a2)) % 360
    return min(d, 360 - d)
def dirn(V, P): return math.degrees(math.atan2(P[1] - V[1], P[0] - V[0]))
def amark(V, A, B, R=0.45, cls='af'):
    """arc ple de l'angle convex AVB"""
    a0, a1 = dirn(V, A), dirn(V, B)
    if (a1 - a0) % 360 > 180: a0, a1 = a1, a0
    if a1 < a0: a1 += 360
    return ('sect', V, R, a0, a1, cls)

# =====================================================================
# 7.5 Relacions entre angles
# =====================================================================
def pairfig(a, tot, c1='af', c2='af2', la='α', lb='β'):
    it = [('sect', (0, 0), 0.55, 0, a, c1), ('sect', (0, 0), 0.75, a, tot, c2), ('ln', (0, 0), (1.9, 0), '', 'e'), ('ln', (0, 0), pol((0, 0), 1.9, a), '', 'e'), ('ln', (0, 0), pol((0, 0), 1.9, tot), '', 'e'), ('dot', (0, 0)),
          ('txt', pol((0, 0), 0.95, a / 2), la, {'cls': 'hot'}), ('txt', pol((0, 0), 1.12, (a + tot) / 2), lb, {'cls': 'hot'})]
    if tot == 90: it.append(('ra', (0, 0), (1, 0), (0, 1)))
    return it
s5 = box('def', L('Angles complementaris i suplementaris', 'Ángulos complementarios y suplementarios', 'Complementary and supplementary angles'),
  ul(L(r"Dos angles són <strong>complementaris</strong> si sumen \(90^\circ\) (un angle recte). El complementari de \(\alpha\) és \(90^\circ-\alpha\).",
       r"Dos ángulos son <strong>complementarios</strong> si suman \(90^\circ\) (un ángulo recto). El complementario de \(\alpha\) es \(90^\circ-\alpha\).",
       r"Two angles are <strong>complementary</strong> if they add up to \(90^\circ\) (a right angle). The complement of \(\alpha\) is \(90^\circ-\alpha\)."),
     L(r"Dos angles són <strong>suplementaris</strong> si sumen \(180^\circ\) (un angle pla). El suplementari de \(\alpha\) és \(180^\circ-\alpha\).",
       r"Dos ángulos son <strong>suplementarios</strong> si suman \(180^\circ\) (un ángulo llano). El suplementario de \(\alpha\) es \(180^\circ-\alpha\).",
       r"Two angles are <strong>supplementary</strong> if they add up to \(180^\circ\) (a straight angle). The supplement of \(\alpha\) is \(180^\circ-\alpha\)."))
  + figs(G(pairfig(35, 90), W=180, pad=16, cap=r'\(35^\circ+55^\circ=90^\circ\)'), G(pairfig(50, 180), W=230, pad=16, cap=r'\(50^\circ+130^\circ=180^\circ\)'))
  + D(r"\text{%s }35^\circ:\ 90^\circ-35^\circ=55^\circ\qquad \text{%s }50^\circ:\ 180^\circ-50^\circ=130^\circ" % (Lt('Complementari de', 'Complementario de', 'Complement of'), Lt('Suplementari de', 'Suplementario de', 'Supplement of')))
  + note(r"Només els angles aguts tenen complementari, i només els angles més menuts que \(180^\circ\) tenen suplementari.",
         r"Solo los ángulos agudos tienen complementario, y solo los ángulos menores que \(180^\circ\) tienen suplementario.",
         r"Only acute angles have a complement, and only angles less than \(180^\circ\) have a supplement.")
  + widget('w-comp', '🧩', L('Complementari i suplementari', 'Complementario y suplementario', 'Complement and supplement'),
           ['<div class="wrow">' + rng('a', 1, 179, 1, 35, 'α') + '</div>', seg([('c', L('Complementari', 'Complementario', 'Complement')), ('s', L('Suplementari', 'Suplementario', 'Supplement'))])])
  + drill('cs', 'Entrena: complementaris i suplementaris', 'Entrena: complementarios y suplementarios', 'Train: complements and supplements', mode='sx'))
F_CONS = G([('sect', (0, 0), 0.6, 0, 40, 'af'), ('sect', (0, 0), 0.8, 40, 95, 'af2'), ('ln', (0, 0), (1.9, 0), '', 'e'), ('ln', (0, 0), pol((0, 0), 1.9, 40), 'hl', 'e'), ('ln', (0, 0), pol((0, 0), 1.9, 95), '', 'e'), ('dot', (0, 0))], W=160, pad=14,
           cap=L('Consecutius', 'Consecutivos', 'Adjacent (sharing a side)'))
F_ADJ = G([('sect', (0, 0), 0.6, 0, 65, 'af'), ('sect', (0, 0), 0.8, 65, 180, 'af2'), ('ln', (0, 0), (1.9, 0), '', 'e'), ('ln', (0, 0), (-1.9, 0), '', 'e'), ('ln', (0, 0), pol((0, 0), 1.9, 65), 'hl', 'e'), ('dot', (0, 0))], W=200, pad=14,
          cap=L('Adjacents (sumen 180°)', 'Adyacentes (suman 180°)', 'Linear pair (add to 180°)'))
F_OPV = G([('sect', (0, 0), 0.6, 30, 110, 'af'), ('sect', (0, 0), 0.6, 210, 290, 'af'), ('sect', (0, 0), 0.45, 110, 210, 'af2'), ('sect', (0, 0), 0.45, 290, 390, 'af2'),
           ('ln', pol((0, 0), 1.8, 210), pol((0, 0), 1.8, 30), '', 'b'), ('ln', pol((0, 0), 1.8, 290), pol((0, 0), 1.8, 110), '', 'b'), ('dot', (0, 0)),
           ('txt', pol((0, 0), 0.85, 70), 'α', {'cls': 'hot'}), ('txt', pol((0, 0), 0.85, 250), 'α', {'cls': 'hot'}), ('txt', pol((0, 0), 0.7, 160), 'β', {'cls': 'hot'}), ('txt', pol((0, 0), 0.7, 340), 'β', {'cls': 'hot'})], W=190, pad=14,
          cap=L('Oposats pel vèrtex: iguals', 'Opuestos por el vértice: iguales', 'Vertically opposite: equal'))
s5 += box('def', L('Angles consecutius, adjacents i oposats pel vèrtex', 'Ángulos consecutivos, adyacentes y opuestos por el vértice', 'Adjacent, linear-pair and vertically opposite angles'),
  ul(L(r"<strong>Consecutius:</strong> tenen el vèrtex i un costat en comú.", r"<strong>Consecutivos:</strong> tienen el vértice y un lado en común.", r"<strong>Adjacent:</strong> they share the vertex and one side."),
     L(r"<strong>Adjacents:</strong> són consecutius i els costats no comuns formen una recta. Per tant, sumen \(180^\circ\): són suplementaris.", r"<strong>Adyacentes:</strong> son consecutivos y los lados no comunes forman una recta. Por tanto, suman \(180^\circ\): son suplementarios.", r"<strong>Linear pair:</strong> adjacent angles whose other sides form a straight line. So they add up to \(180^\circ\): they're supplementary."),
     L(r"<strong>Oposats pel vèrtex:</strong> quan dues rectes es tallen, els angles que queden un davant de l'altre. Són <strong>iguals</strong>.", r"<strong>Opuestos por el vértice:</strong> cuando dos rectas se cortan, los ángulos que quedan uno enfrente del otro. Son <strong>iguales</strong>.", r"<strong>Vertically opposite:</strong> when two lines cross, the angles facing each other. They are <strong>equal</strong>."))
  + figs(F_CONS, F_ADJ, F_OPV, three=True)
  + P(r"Per què són iguals els oposats pel vèrtex? En la figura, \(\alpha+\beta=180^\circ\) (adjacents) i també l'altre \(\alpha\) més \(\beta\) fan \(180^\circ\). Per tant, els dos angles \(\alpha\) són iguals.",
      r"¿Por qué son iguales los opuestos por el vértice? En la figura, \(\alpha+\beta=180^\circ\) (adyacentes) y también el otro \(\alpha\) más \(\beta\) suman \(180^\circ\). Por tanto, los dos ángulos \(\alpha\) son iguales.",
      r"Why are vertically opposite angles equal? In the figure, \(\alpha+\beta=180^\circ\) (linear pair) and the other \(\alpha\) plus \(\beta\) also make \(180^\circ\). So the two \(\alpha\) angles are equal."))
# dues paral·leles tallades per una secant
def parfig(a, hl=None, labs=True, nums=False):
    """paral·leles y=0 i y=1.6, secant que forma l'angle a amb elles"""
    h = 1.6; X1 = h / math.tan(math.radians(a)); P1, P2 = (0, 0), (X1, h)
    it = [('ln', (-2.0, 0), (2.0 + X1, 0), '', 'b'), ('ln', (-2.0, h), (2.0 + X1, h), '', 'b'), ('ln', pol(P1, 1.25, 180 + a), pol(P2, 1.25, a), '', 'b')]
    for P, off_ in ((P1, 0), (P2, 4)):
        for k, (a0, a1) in enumerate([(0, a), (a, 180), (180, 180 + a), (180 + a, 360)]):
            n = off_ + k + 1; cls = 'af' if k % 2 == 0 else 'af2'
            if hl and n not in hl: cls = 'af0'
            it.append(('sect', P, 0.42 if k % 2 == 0 else 0.32, a0, a1, cls))
            if nums: it.append(('txt', pol(P, 0.68, (a0 + a1) / 2), str(n), {'cls': 'hot' if not hl or n in hl else ''}))
    it += [('dot', P1), ('dot', P2)]
    if labs: it += [lab((-1.9, h), 'r', 0, -8), lab((-1.9, 0), 's', 0, -8)]
    return it
s5 += box('prop', L('Dues paral·leles tallades per una secant', 'Dos paralelas cortadas por una secante', 'Two parallel lines cut by a transversal'),
  P(r"Si una recta talla dues rectes <strong>paral·leles</strong>, es formen 8 angles. Però només hi ha <strong>dues mesures</strong> diferents: els angles aguts són tots iguals i els obtusos també, i un agut i un obtús sempre sumen \(180^\circ\).",
    r"Si una recta corta dos rectas <strong>paralelas</strong>, se forman 8 ángulos. Pero solo hay <strong>dos medidas</strong> diferentes: los ángulos agudos son todos iguales y los obtusos también, y un agudo y un obtuso siempre suman \(180^\circ\).",
    r"If a line cuts two <strong>parallel</strong> lines, 8 angles are formed. But there are only <strong>two sizes</strong>: all the acute angles are equal, all the obtuse ones are equal, and an acute plus an obtuse always make \(180^\circ\).")
  + figs(G(parfig(55, nums=True), W=300, pad=14, cap=L('Els angles del mateix color són iguals', 'Los ángulos del mismo color son iguales', 'Angles of the same colour are equal')))
  + ul(L(r"<strong>Corresponents</strong> (en la mateixa posició en cada cruïlla): 1 i 5, 2 i 6, 3 i 7, 4 i 8. Són iguals.", r"<strong>Correspondientes</strong> (en la misma posición en cada cruce): 1 y 5, 2 y 6, 3 y 7, 4 y 8. Son iguales.", r"<strong>Corresponding</strong> (same position at each crossing): 1 and 5, 2 and 6, 3 and 7, 4 and 8. They're equal."),
       L(r"<strong>Alterns interns</strong> (entre les paral·leles, a costats diferents de la secant): 1 i 7, 2 i 8. Són iguals.", r"<strong>Alternos internos</strong> (entre las paralelas, a lados distintos de la secante): 1 y 7, 2 y 8. Son iguales.", r"<strong>Alternate interior</strong> (between the parallels, on opposite sides of the transversal): 1 and 7, 2 and 8. They're equal."),
       L(r"<strong>Alterns externs</strong> (fora de les paral·leles, a costats diferents de la secant): 3 i 5, 4 i 6. Són iguals.", r"<strong>Alternos externos</strong> (fuera de las paralelas, a lados distintos de la secante): 3 y 5, 4 y 6. Son iguales.", r"<strong>Alternate exterior</strong> (outside the parallels, on opposite sides of the transversal): 3 and 5, 4 and 6. They're equal."))
  + widget('w-par', '🛤️', L('Gira la secant', 'Gira la secante', 'Turn the transversal'),
           ['<div class="wrow">' + rng('a', 20, 160, 1, 55, 'α') + '</div>',
            seg([('t', L('Tots', 'Todos', 'All')), ('c', L('Corresponents', 'Correspondientes', 'Corresponding')), ('i', L('Alterns interns', 'Alternos internos', 'Alt. interior')), ('e', L('Alterns externs', 'Alternos externos', 'Alt. exterior')), ('o', L('Oposats pel vèrtex', 'Opuestos por el vértice', 'Vert. opposite'))])])
  + drill('par', 'Entrena: angles entre paral·leles', 'Entrena: ángulos entre paralelas', 'Train: angles between parallels', mode='int'))
assert 90 - 35 == 55 and 180 - 50 == 130
s5 += levels(
 [prob(L(r"Calcula el complementari i el suplementari de: a) \(28^\circ\); b) \(64^\circ\,15'\).", r"Calcula el complementario y el suplementario de: a) \(28^\circ\); b) \(64^\circ\,15'\).", r"Find the complement and the supplement of: a) \(28^\circ\); b) \(64^\circ\,15'\)."),
       D(r"\text{a) }90^\circ-28^\circ=\boxed{62^\circ}\qquad180^\circ-28^\circ=\boxed{152^\circ}"),
       P(r"b) Escrivim \(90^\circ=89^\circ\,60'\) i \(180^\circ=179^\circ\,60'\):", r"b) Escribimos \(90^\circ=89^\circ\,60'\) y \(180^\circ=179^\circ\,60'\):", r"b) Write \(90^\circ=89^\circ\,60'\) and \(180^\circ=179^\circ\,60'\):"),
       D(r"89^\circ\,60'-64^\circ\,15'=\boxed{25^\circ\,45'}\qquad179^\circ\,60'-64^\circ\,15'=\boxed{115^\circ\,45'}"))],
 [prob(L(r"Dos angles adjacents són tals que un és el triple de l'altre. Quant mesuren?", r"Dos ángulos adyacentes son tales que uno es el triple del otro. ¿Cuánto miden?", r"Two angles form a linear pair and one is three times the other. How big are they?"),
       P(r"Els angles adjacents sumen \(180^\circ\). Si el menut és \(x\), el gran és \(3x\):", r"Los ángulos adyacentes suman \(180^\circ\). Si el pequeño es \(x\), el grande es \(3x\):", r"Linear-pair angles add up to \(180^\circ\). If the small one is \(x\), the big one is \(3x\):"),
       D(r"x+3x=180\ \Rightarrow\ 4x=180\ \Rightarrow\ x=45"),
       P(r"Els angles mesuren <strong>\(45^\circ\) i \(135^\circ\)</strong>. Comprovació: \(45+135=180\ \checkmark\)", r"Los ángulos miden <strong>\(45^\circ\) y \(135^\circ\)</strong>. Comprobación: \(45+135=180\ \checkmark\)", r"The angles are <strong>\(45^\circ\) and \(135^\circ\)</strong>. Check: \(45+135=180\ \checkmark\)"))],
 [prob(L(r"Les rectes \(r\) i \(s\) són paral·leles i l'angle 1 fa \(65^\circ\). Calcula els altres set angles i explica per què.", r"Las rectas \(r\) y \(s\) son paralelas y el ángulo 1 mide \(65^\circ\). Calcula los otros siete ángulos y explica por qué.", r"Lines \(r\) and \(s\) are parallel and angle 1 is \(65^\circ\). Find the other seven angles and explain why.")
       + figs(G(parfig(65, nums=True), W=280, pad=14)),
       P(r"L'angle 3 és oposat pel vèrtex a l'1: \(\hat3=65^\circ\). Els angles 2 i 4 són adjacents a l'1: \(\hat2=\hat4=180^\circ-65^\circ=115^\circ\).",
         r"El ángulo 3 es opuesto por el vértice al 1: \(\hat3=65^\circ\). Los ángulos 2 y 4 son adyacentes al 1: \(\hat2=\hat4=180^\circ-65^\circ=115^\circ\).",
         r"Angle 3 is vertically opposite angle 1: \(\hat3=65^\circ\). Angles 2 and 4 form linear pairs with 1: \(\hat2=\hat4=180^\circ-65^\circ=115^\circ\)."),
       P(r"Els angles de l'altra cruïlla són corresponents a aquests: \(\hat5=\hat7=\boxed{65^\circ}\) i \(\hat6=\hat8=\boxed{115^\circ}\).",
         r"Los ángulos del otro cruce son correspondientes a estos: \(\hat5=\hat7=\boxed{65^\circ}\) y \(\hat6=\hat8=\boxed{115^\circ}\).",
         r"The angles at the other crossing correspond to these: \(\hat5=\hat7=\boxed{65^\circ}\) and \(\hat6=\hat8=\boxed{115^\circ}\)."))])
s5 += practice([
  ('★☆☆', L(r"Calcula el complementari de \(47^\circ\) i el suplementari de \(118^\circ\).", r"Calcula el complementario de \(47^\circ\) y el suplementario de \(118^\circ\).", r"Find the complement of \(47^\circ\) and the supplement of \(118^\circ\).")),
  ('★★☆', L(r"Dues rectes es tallen i un dels angles fa \(72^\circ\). Quant mesuren els altres tres?", r"Dos rectas se cortan y uno de los ángulos mide \(72^\circ\). ¿Cuánto miden los otros tres?", r"Two lines cross and one of the angles is \(72^\circ\). How big are the other three?")),
  ('★★★', L(r"Un angle mesura \(20^\circ\) més que el seu complementari. Quant mesura?", r"Un ángulo mide \(20^\circ\) más que su complementario. ¿Cuánto mide?", r"An angle is \(20^\circ\) bigger than its complement. How big is it?"))],
  ol(r"\(43^\circ\); \(62^\circ\)", r"\(72^\circ\), \(108^\circ\) " + L('i', 'y', 'and') + r" \(108^\circ\)", r"\(x+(x-20)=90\Rightarrow x=55^\circ\) (" + L('el complementari fa', 'el complementario mide', 'its complement is') + r" \(35^\circ\))"))
assert 90 - 47 == 43 and 180 - 118 == 62 and 180 - 72 == 108 and 55 + 35 == 90 and 55 - 35 == 20

# =====================================================================
# 7.6 Polígons: elements i classificació
# =====================================================================
PENT = [(0, 0), (3, -0.2), (3.8, 1.8), (1.8, 3.0), (-0.4, 1.9)]
def pnames(V, names, k=0.32):
    cx = sum(p[0] for p in V) / len(V); cy = sum(p[1] for p in V) / len(V)
    out = []
    for P, n in zip(V, names):
        dx, dy = P[0] - cx, P[1] - cy; d = math.hypot(dx, dy)
        out.append(('txt', (P[0] + dx / d * k, P[1] + dy / d * k), n, {}))
    return out
F_ELEM = G([('poly', PENT, 'gf'), ('seg', PENT[0], PENT[2], 'd'), ('seg', PENT[0], PENT[3], 'd'), amark(PENT[2], PENT[1], PENT[3], 0.5)] + [('dot', P) for P in PENT] + pnames(PENT, 'ABCDE')
           + [lab((1.5, -0.1), Ls('costat', 'lado', 'side'), 0, 16), lab((1.6, 0.9), Ls('diagonal', 'diagonal', 'diagonal'), 0, 4, 'hot'), lab((3.3, 1.75), Ls('angle', 'ángulo', 'angle'), -26, 4)], W=260, pad=26,
           cap=L('Elements d\'un polígon', 'Elementos de un polígono', 'Parts of a polygon'))
s6 = box('def', L('Què és un polígon?', '¿Qué es un polígono?', 'What is a polygon?'),
  P(r"Una <strong>línia poligonal</strong> està formada per segments units un darrere de l'altre. Si és <strong>tancada</strong> (l'últim segment acaba on comença el primer), la regió del pla que limita s'anomena <strong>polígon</strong>.",
    r"Una <strong>línea poligonal</strong> está formada por segmentos unidos uno detrás de otro. Si es <strong>cerrada</strong> (el último segmento acaba donde empieza el primero), la región del plano que limita se llama <strong>polígono</strong>.",
    r"A <strong>polygonal line</strong> is made of segments joined end to end. If it is <strong>closed</strong> (the last segment ends where the first one starts), the region of the plane it encloses is called a <strong>polygon</strong>.")
  + P(r"<strong>Elements d'un polígon:</strong>", r"<strong>Elementos de un polígono:</strong>", r"<strong>Parts of a polygon:</strong>")
  + ul(L(r"<strong>Costats:</strong> els segments que el limiten.", r"<strong>Lados:</strong> los segmentos que lo limitan.", r"<strong>Sides:</strong> the segments that bound it."),
       L(r"<strong>Vèrtexs:</strong> els punts on s'unixen dos costats. Un polígon té tants vèrtexs com costats.", r"<strong>Vértices:</strong> los puntos donde se unen dos lados. Un polígono tiene tantos vértices como lados.", r"<strong>Vertices:</strong> the points where two sides meet. A polygon has as many vertices as sides."),
       L(r"<strong>Angles interiors:</strong> els que formen dos costats consecutius, per dins del polígon.", r"<strong>Ángulos interiores:</strong> los que forman dos lados consecutivos, por dentro del polígono.", r"<strong>Interior angles:</strong> those formed by two consecutive sides, inside the polygon."),
       L(r"<strong>Diagonals:</strong> els segments que unixen dos vèrtexs <strong>no consecutius</strong>.", r"<strong>Diagonales:</strong> los segmentos que unen dos vértices <strong>no consecutivos</strong>.", r"<strong>Diagonals:</strong> segments joining two <strong>non-adjacent</strong> vertices."))
  + figs(F_ELEM))
NAMES = [(3, 'triangle', 'triángulo', 'triangle'), (4, 'quadrilàter', 'cuadrilátero', 'quadrilateral'), (5, 'pentàgon', 'pentágono', 'pentagon'), (6, 'hexàgon', 'hexágono', 'hexagon'),
         (7, 'heptàgon', 'heptágono', 'heptagon'), (8, 'octàgon', 'octógono', 'octagon'), (9, 'enneàgon', 'eneágono', 'nonagon'), (10, 'decàgon', 'decágono', 'decagon'),
         (11, 'endecàgon', 'endecágono', 'hendecagon'), (12, 'dodecàgon', 'dodecágono', 'dodecagon')]
CONC = [(0, 0), (3, 0), (3, 2.4), (1.5, 1.0), (0, 2.4)]
IRR = [(0, 0), (2.6, 0.3), (3.2, 2.0), (1.0, 2.8), (-0.4, 1.4)]
s6 += box('def', L('Classificació dels polígons', 'Clasificación de los polígonos', 'Types of polygons'),
  P(r"<strong>Pel nombre de costats:</strong>", r"<strong>Por el número de lados:</strong>", r"<strong>By the number of sides:</strong>")
  + tbl([L('Costats', 'Lados', 'Sides'), L('Nom', 'Nombre', 'Name'), L('Costats', 'Lados', 'Sides'), L('Nom', 'Nombre', 'Name')],
        [[str(NAMES[i][0]), L(*NAMES[i][1:]), str(NAMES[i + 5][0]), L(*NAMES[i + 5][1:])] for i in range(5)])
  + P(r"A partir de 13 costats se solen anomenar pel nombre: polígon de 15 costats, de 20 costats…", r"A partir de 13 lados se suelen nombrar por el número: polígono de 15 lados, de 20 lados…", r"From 13 sides on we usually just say the number: 15-sided polygon, 20-sided polygon…")
  + P(r"<strong>Per la forma:</strong>", r"<strong>Por la forma:</strong>", r"<strong>By shape:</strong>")
  + ul(L(r"<strong>Convex:</strong> tots els angles interiors fan menys de \(180^\circ\). Cap diagonal ix fora del polígon.", r"<strong>Convexo:</strong> todos los ángulos interiores miden menos de \(180^\circ\). Ninguna diagonal sale fuera del polígono.", r"<strong>Convex:</strong> all interior angles are less than \(180^\circ\). No diagonal goes outside the polygon."),
       L(r"<strong>Còncau:</strong> té algun angle interior de més de \(180^\circ\) i alguna diagonal queda fora.", r"<strong>Cóncavo:</strong> tiene algún ángulo interior de más de \(180^\circ\) y alguna diagonal queda fuera.", r"<strong>Concave:</strong> it has an interior angle of more than \(180^\circ\) and some diagonal lies outside."),
       L(r"<strong>Regular:</strong> té tots els costats iguals i tots els angles iguals. Si no, és <strong>irregular</strong>.", r"<strong>Regular:</strong> tiene todos los lados iguales y todos los ángulos iguales. Si no, es <strong>irregular</strong>.", r"<strong>Regular:</strong> all sides equal and all angles equal. Otherwise it is <strong>irregular</strong>."))
  + figs(G([('poly', IRR, 'gf')], W=150, pad=10, cap=L('Convex irregular', 'Convexo irregular', 'Convex, irregular')),
         G([('poly', CONC, 'gf'), ('seg', CONC[2], CONC[4], 'd'), ('sect', CONC[3], 0.35, dirn(CONC[3], CONC[4]), dirn(CONC[3], CONC[2]) + 360, 'af')], W=150, pad=10, cap=L('Còncau (la diagonal ix fora)', 'Cóncavo (la diagonal sale fuera)', 'Concave (a diagonal is outside)')),
         G([('poly', reg(6), 'gf')] + [('tick', a, b, 1) for a, b in zip(reg(6), reg(6)[1:] + reg(6)[:1])], W=150, pad=10, cap=L('Regular', 'Regular', 'Regular')), three=True))
s6 += box('prop', L('Nombre de diagonals', 'Número de diagonales', 'Number of diagonals'),
  P(r"Des de cada vèrtex d'un polígon de \(n\) costats ixen \(n-3\) diagonals (no se'n pot traçar cap al mateix vèrtex ni als dos vèrtexs del costat). Com que cada diagonal té dos extrems, la comptaríem dues vegades:",
    r"Desde cada vértice de un polígono de \(n\) lados salen \(n-3\) diagonales (no se puede trazar ninguna al mismo vértice ni a los dos vértices de al lado). Como cada diagonal tiene dos extremos, la contaríamos dos veces:",
    r"From each vertex of an \(n\)-sided polygon \(n-3\) diagonals leave (none to itself or to its two neighbours). Since each diagonal has two ends, we'd count it twice:")
  + D(r"\text{%s}=\frac{n\cdot(n-3)}{2}\qquad\text{%s: }\frac{6\cdot3}{2}=9" % (Lt('Nombre de diagonals', 'Número de diagonales', 'Number of diagonals'), Lt('Hexàgon', 'Hexágono', 'Hexagon')))
  + figs(G([('poly', reg(6), 'gf')] + [('seg', reg(6)[i], reg(6)[j], 'd' if i else 'hl') for i in range(6) for j in range(i + 2, 6) if not (i == 0 and j == 5)] + [('dot', P) for P in reg(6)], W=200, pad=12,
           cap=L("Hexàgon: 3 diagonals per vèrtex, 9 en total", "Hexágono: 3 diagonales por vértice, 9 en total", "Hexagon: 3 diagonals per vertex, 9 in all")))
  + widget('w-diag', '🕸️', L('Polígons i diagonals', 'Polígonos y diagonales', 'Polygons and diagonals'),
           ['<div class="wrow">' + rng('n', 3, 12, 1, 6, 'n') + '</div>', seg([('u', L("Diagonals d'un vèrtex", 'Diagonales de un vértice', 'Diagonals from one vertex')), ('t', L('Totes les diagonals', 'Todas las diagonales', 'All diagonals'))])])
  + drill('pname', 'Entrena: nom i diagonals dels polígons', 'Entrena: nombre y diagonales de los polígonos', 'Train: polygon names and diagonals', mode='opts'))
assert 6 * 3 // 2 == 9
s6 += levels(
 [prob(L(r"Quants costats, vèrtexs i diagonals té un octàgon?", r"¿Cuántos lados, vértices y diagonales tiene un octógono?", r"How many sides, vertices and diagonals does an octagon have?"),
       P(r"Té 8 costats i 8 vèrtexs. De cada vèrtex ixen \(8-3=5\) diagonals:", r"Tiene 8 lados y 8 vértices. De cada vértice salen \(8-3=5\) diagonales:", r"It has 8 sides and 8 vertices. From each vertex \(8-3=5\) diagonals leave:"),
       D(r"\frac{8\cdot5}{2}=\boxed{20\ \text{%s}}" % Lt('diagonals', 'diagonales', 'diagonals')))],
 [prob(L(r"Un rectangle té tots els angles iguals. És un polígon regular? I un rombe, que té tots els costats iguals?", r"Un rectángulo tiene todos los ángulos iguales. ¿Es un polígono regular? ¿Y un rombo, que tiene todos los lados iguales?", r"A rectangle has all its angles equal. Is it a regular polygon? And a rhombus, which has all its sides equal?"),
       P(r"<strong>No</strong> en cap dels dos casos. Un polígon regular ha de complir les <strong>dues</strong> condicions alhora: costats iguals i angles iguals. El rectangle té els costats desiguals i el rombe, els angles desiguals. L'únic quadrilàter regular és el <strong>quadrat</strong>.",
         r"<strong>No</strong> en ninguno de los dos casos. Un polígono regular debe cumplir las <strong>dos</strong> condiciones a la vez: lados iguales y ángulos iguales. El rectángulo tiene los lados desiguales y el rombo, los ángulos desiguales. El único cuadrilátero regular es el <strong>cuadrado</strong>.",
         r"<strong>No</strong> in both cases. A regular polygon must meet <strong>both</strong> conditions at once: equal sides and equal angles. The rectangle's sides aren't all equal and the rhombus's angles aren't. The only regular quadrilateral is the <strong>square</strong>."))],
 [prob(L(r"Quin polígon té 35 diagonals?", r"¿Qué polígono tiene 35 diagonales?", r"Which polygon has 35 diagonals?"),
       P(r"Necessitem \(\dfrac{n\cdot(n-3)}{2}=35\), és a dir, \(n\cdot(n-3)=70\). Provem: \(8\cdot5=40\), \(9\cdot6=54\), \(10\cdot7=70\ \checkmark\)",
         r"Necesitamos \(\dfrac{n\cdot(n-3)}{2}=35\), es decir, \(n\cdot(n-3)=70\). Probamos: \(8\cdot5=40\), \(9\cdot6=54\), \(10\cdot7=70\ \checkmark\)",
         r"We need \(\dfrac{n\cdot(n-3)}{2}=35\), i.e. \(n\cdot(n-3)=70\). Try: \(8\cdot5=40\), \(9\cdot6=54\), \(10\cdot7=70\ \checkmark\)"),
       P(r"És un <strong>decàgon</strong> (10 costats).", r"Es un <strong>decágono</strong> (10 lados).", r"It's a <strong>decagon</strong> (10 sides)."))])
assert 8 * 5 // 2 == 20 and 10 * 7 == 70
s6 += practice([
  ('★☆☆', L(r"Com s'anomena el polígon de 7 costats? I el de 12?", r"¿Cómo se llama el polígono de 7 lados? ¿Y el de 12?", r"What's the name of the 7-sided polygon? And the 12-sided one?")),
  ('★★☆', L(r"Quantes diagonals té un pentàgon? I un dodecàgon?", r"¿Cuántas diagonales tiene un pentágono? ¿Y un dodecágono?", r"How many diagonals does a pentagon have? And a dodecagon?")),
  ('★★☆', L(r"Pot un triangle tindre diagonals? Per què?", r"¿Puede un triángulo tener diagonales? ¿Por qué?", r"Can a triangle have diagonals? Why?"))],
  ol(L('Heptàgon; dodecàgon', 'Heptágono; dodecágono', 'Heptagon; dodecagon'), r"\(\frac{5\cdot2}{2}=5\); \(\frac{12\cdot9}{2}=54\)",
     L(r"No: cada vèrtex és consecutiu als altres dos (\(\frac{3\cdot0}{2}=0\)).", r"No: cada vértice es consecutivo a los otros dos (\(\frac{3\cdot0}{2}=0\)).", r"No: every vertex is next to the other two (\(\frac{3\cdot0}{2}=0\)).")))
assert 12 * 9 // 2 == 54

# =====================================================================
# 7.7 Triangles
# =====================================================================
def tri(V, cls='gf', ticks=(), ra=None, names=None, marks=()):
    it = [('poly', V, cls)]
    for i, n in ticks: it.append(('tick', V[i], V[(i + 1) % 3], n))
    for i in marks: it.append(amark(V[i], V[i - 1], V[(i + 1) % 3], 0.38))
    if ra is not None: it.append(('ra', V[ra], V[ra - 1], V[(ra + 1) % 3]))
    if names: it += pnames(V, names)
    return it
EQ = reg(3, 1.6); ISO = [(0, 0), (2.4, 0), (1.2, 2.6)]; ESC = [(0, 0), (3.2, 0), (2.2, 1.9)]
ACU = [(0, 0), (3, 0), (1.9, 2.2)]; REC = [(0, 0), (3, 0), (0, 2.2)]; OBT = [(0, 0), (3.4, 0), (-0.9, 1.6)]
s7 = box('def', L('Classificació dels triangles', 'Clasificación de los triángulos', 'Types of triangles'),
  P(r"Un <strong>triangle</strong> és un polígon de tres costats. Els vèrtexs s'anomenen amb majúscules (\(A\), \(B\), \(C\)) i el costat oposat a cada vèrtex, amb la minúscula corresponent (\(a\), \(b\), \(c\)).",
    r"Un <strong>triángulo</strong> es un polígono de tres lados. Los vértices se nombran con mayúsculas (\(A\), \(B\), \(C\)) y el lado opuesto a cada vértice, con la minúscula correspondiente (\(a\), \(b\), \(c\)).",
    r"A <strong>triangle</strong> is a three-sided polygon. Its vertices are named with capitals (\(A\), \(B\), \(C\)) and the side opposite each vertex with the matching small letter (\(a\), \(b\), \(c\)).")
  + P(r"<strong>Segons els costats:</strong>", r"<strong>Según sus lados:</strong>", r"<strong>By their sides:</strong>")
  + figs(G(tri(EQ, ticks=[(0, 1), (1, 1), (2, 1)]), W=140, pad=10, cap=L('<strong>Equilàter</strong>: 3 costats iguals', '<strong>Equilátero</strong>: 3 lados iguales', '<strong>Equilateral</strong>: 3 equal sides')),
         G(tri(ISO, ticks=[(1, 1), (2, 1)]), W=120, pad=10, cap=L('<strong>Isòsceles</strong>: 2 costats iguals', '<strong>Isósceles</strong>: 2 lados iguales', '<strong>Isosceles</strong>: 2 equal sides')),
         G(tri(ESC), W=160, pad=10, cap=L('<strong>Escalé</strong>: cap costat igual', '<strong>Escaleno</strong>: ningún lado igual', '<strong>Scalene</strong>: no equal sides')), three=True)
  + P(r"<strong>Segons els angles:</strong>", r"<strong>Según sus ángulos:</strong>", r"<strong>By their angles:</strong>")
  + figs(G(tri(ACU, marks=(0, 1, 2)), W=150, pad=10, cap=L('<strong>Acutangle</strong>: 3 angles aguts', '<strong>Acutángulo</strong>: 3 ángulos agudos', '<strong>Acute</strong>: 3 acute angles')),
         G(tri(REC, ra=0), W=150, pad=10, cap=L('<strong>Rectangle</strong>: 1 angle recte', '<strong>Rectángulo</strong>: 1 ángulo recto', '<strong>Right</strong>: 1 right angle')),
         G(tri(OBT, marks=(0,)), W=170, pad=10, cap=L('<strong>Obtusangle</strong>: 1 angle obtús', '<strong>Obtusángulo</strong>: 1 ángulo obtuso', '<strong>Obtuse</strong>: 1 obtuse angle')), three=True)
  + P(r"En un triangle rectangle, els dos costats que formen l'angle recte s'anomenen <strong>catets</strong> i el costat oposat a l'angle recte, <strong>hipotenusa</strong>. En un triangle isòsceles, el costat desigual és la <strong>base</strong>, i els dos angles de la base són iguals.",
      r"En un triángulo rectángulo, los dos lados que forman el ángulo recto se llaman <strong>catetos</strong> y el lado opuesto al ángulo recto, <strong>hipotenusa</strong>. En un triángulo isósceles, el lado desigual es la <strong>base</strong>, y los dos ángulos de la base son iguales.",
      r"In a right triangle, the two sides forming the right angle are the <strong>legs</strong> and the side opposite the right angle is the <strong>hypotenuse</strong>. In an isosceles triangle, the odd side is the <strong>base</strong>, and the two base angles are equal."))
assert angle_at(OBT[0], OBT[1], OBT[2]) > 90 and all(angle_at(ACU[i], ACU[i - 1], ACU[(i + 1) % 3]) < 90 for i in range(3))
TS = [(0, 0), (4, 0), (1.4, 2.4)]
F_SUM = G([('ln', (-1.2, 2.4), (3.8, 2.4), 'd', 'b'), ('poly', TS, 'gf'), amark(TS[0], TS[1], TS[2], 0.5, 'af'), amark(TS[1], TS[2], TS[0], 0.5, 'af2'), amark(TS[2], TS[0], TS[1], 0.42, 'af3'),
           ('sect', TS[2], 0.5, dirn(TS[2], TS[1]), 0, 'af2'), ('sect', TS[2], 0.5, 180, dirn(TS[2], TS[0]) + 360, 'af'),
           lab(pol(TS[0], 0.8, 30), 'A', 0, 4, 'hot'), lab(pol(TS[1], 0.8, 165), 'B', 0, 4, 'hot'), lab(pol(TS[2], 0.68, -81), 'C', 0, 4, 'hot'), lab(pol(TS[2], 0.8, 210), 'A', 0, 4, 'hot'), lab(pol(TS[2], 0.8, -21), 'B', 0, 4, 'hot')], W=280, pad=16,
          cap=L(r'\(\hat A+\hat B+\hat C\) formen un angle pla', r'\(\hat A+\hat B+\hat C\) forman un ángulo llano', r'\(\hat A+\hat B+\hat C\) make a straight angle'))
s7 += box('prop', L("Els angles d'un triangle sumen 180°", 'Los ángulos de un triángulo suman 180°', "A triangle's angles add up to 180°"),
  D(r"\hat A+\hat B+\hat C=180^\circ")
  + P(r"<strong>Per què?</strong> Tracem per \(C\) la paral·lela al costat \(AB\). Els angles marcats al costat de \(C\) són <strong>alterns interns</strong> amb \(\hat A\) i \(\hat B\) (apartat 7.5), per tant són iguals. Junt amb \(\hat C\) formen un angle pla: \(180^\circ\).",
      r"<strong>¿Por qué?</strong> Trazamos por \(C\) la paralela al lado \(AB\). Los ángulos marcados junto a \(C\) son <strong>alternos internos</strong> con \(\hat A\) y \(\hat B\) (apartado 7.5), por tanto son iguales. Junto con \(\hat C\) forman un ángulo llano: \(180^\circ\).",
      r"<strong>Why?</strong> Draw the parallel to side \(AB\) through \(C\). The angles marked next to \(C\) are <strong>alternate interior</strong> angles with \(\hat A\) and \(\hat B\) (section 7.5), so they're equal. Together with \(\hat C\) they form a straight angle: \(180^\circ\).")
  + figs(F_SUM)
  + ul(L(r"Un triangle només pot tindre <strong>un</strong> angle recte o <strong>un</strong> angle obtús (dos ja sumarien \(180^\circ\) o més).", r"Un triángulo solo puede tener <strong>un</strong> ángulo recto o <strong>un</strong> ángulo obtuso (dos ya sumarían \(180^\circ\) o más).", r"A triangle can have only <strong>one</strong> right angle or <strong>one</strong> obtuse angle (two would already make \(180^\circ\) or more)."),
       L(r"En un triangle rectangle, els dos angles aguts són complementaris: sumen \(90^\circ\).", r"En un triángulo rectángulo, los dos ángulos agudos son complementarios: suman \(90^\circ\).", r"In a right triangle the two acute angles are complementary: they add up to \(90^\circ\)."),
       L(r"Cada angle d'un triangle equilàter fa \(180^\circ:3=60^\circ\).", r"Cada ángulo de un triángulo equilátero mide \(180^\circ:3=60^\circ\).", r"Each angle of an equilateral triangle is \(180^\circ:3=60^\circ\)."))
  + widget('w-tsum', '🔺', L('El tercer angle', 'El tercer ángulo', 'The third angle'),
           ['<div class="wrow">' + rng('a', 5, 170, 1, 50, 'A') + rng('b', 5, 170, 1, 60, 'B') + '</div>'])
  + drill('tang', 'Entrena: calcula l\'angle que falta', 'Entrena: calcula el ángulo que falta', 'Train: find the missing angle', mode='int'))
s7 += box('prop', L('Desigualtat triangular', 'Desigualdad triangular', 'Triangle inequality'),
  P(r"No amb tres segments qualssevol es pot construir un triangle. Cada costat ha de ser <strong>més menut que la suma dels altres dos</strong>. N'hi ha prou de comprovar-ho amb el costat més llarg:",
    r"No con tres segmentos cualesquiera se puede construir un triángulo. Cada lado debe ser <strong>menor que la suma de los otros dos</strong>. Basta con comprobarlo con el lado más largo:",
    r"You can't build a triangle from just any three segments. Each side must be <strong>less than the sum of the other two</strong>. It's enough to check the longest side:")
  + D(r"3,\,4,\,6:\ 6<3+4=7\ \checkmark\ \text{%s}\qquad 2,\,3,\,7:\ 7>2+3=5\ \text{✗}\ \text{%s}" % (Lt('sí', 'sí', 'yes'), Lt('no', 'no', 'no')))
  + figs(G([('seg', (0, 0), (7, 0), 'hl'), ('seg', (0, 0), (2, 0.6)), ('seg', (7, 0), (4, 1.2)), ('dot', (0, 0)), ('dot', (7, 0)), lab((3.5, 0), '7', 0, 16), lab((1, 0.3), '2', 0, -8), lab((5.5, 0.6), '3', 0, -8)], W=260, pad=16,
           cap=L('Amb 2 i 3 no arribem a tancar el triangle de base 7', 'Con 2 y 3 no llegamos a cerrar el triángulo de base 7', 'With 2 and 3 we can\'t close a triangle on a base of 7')))
  + widget('w-tri', '📐', L('Construïx un triangle a partir dels costats', 'Construye un triángulo a partir de los lados', 'Build a triangle from its sides'),
           ['<div class="wrow">' + tin('a', 'a =', '5') + tin('b', 'b =', '6') + tin('c', 'c =', '7') + '</div>',
            quick([('5|5|5', '5, 5, 5'), ('5|5|8', '5, 5, 8'), ('3|4|5', '3, 4, 5'), ('4|5|8', '4, 5, 8'), ('2|3|7', '2, 3, 7'), ('3|4|7', '3, 4, 7')])], out='<div class="gout"></div>')
  + drill('tcls', 'Entrena: classifica el triangle', 'Entrena: clasifica el triángulo', 'Train: classify the triangle', mode='opts'))
# rectes i punts notables d'un triangle (A, B, C fixos)
TA, TB, TC = (0.0, 0.0), (5.0, 0.0), (1.6, 3.2)
def circumcentre(A, B, C):
    d = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))
    ux = ((A[0] ** 2 + A[1] ** 2) * (B[1] - C[1]) + (B[0] ** 2 + B[1] ** 2) * (C[1] - A[1]) + (C[0] ** 2 + C[1] ** 2) * (A[1] - B[1])) / d
    uy = ((A[0] ** 2 + A[1] ** 2) * (C[0] - B[0]) + (B[0] ** 2 + B[1] ** 2) * (A[0] - C[0]) + (C[0] ** 2 + C[1] ** 2) * (B[0] - A[0])) / d
    return (ux, uy)
O_ = circumcentre(TA, TB, TC)
for Q_ in (TA, TB, TC): assert abs(math.dist(O_, Q_) - math.dist(O_, TA)) < 1e-9
NOT = [(L('Mediatrius', 'Mediatrices', 'Perpendicular bisectors'), L('Circumcentre', 'Circuncentro', 'Circumcentre'),
        L("És el centre de la circumferència que passa pels tres vèrtexs (circumscrita): equidista dels vèrtexs.", "Es el centro de la circunferencia que pasa por los tres vértices (circunscrita): equidista de los vértices.", "It is the centre of the circle through the three vertices (circumcircle): it's equidistant from the vertices.")),
       (L('Bisectrius', 'Bisectrices', 'Angle bisectors'), L('Incentre', 'Incentro', 'Incentre'),
        L("És el centre de la circumferència tangent als tres costats (inscrita): equidista dels costats.", "Es el centro de la circunferencia tangente a los tres lados (inscrita): equidista de los lados.", "It is the centre of the circle touching the three sides (incircle): it's equidistant from the sides.")),
       (L('Altures', 'Alturas', 'Altitudes'), L('Ortocentre', 'Ortocentro', 'Orthocentre'),
        L("L'altura és el segment perpendicular que va d'un vèrtex al costat oposat (o a la seua prolongació).", "La altura es el segmento perpendicular que va de un vértice al lado opuesto (o a su prolongación).", "An altitude is the perpendicular segment from a vertex to the opposite side (or its extension).")),
       (L('Mitjanes', 'Medianas', 'Medians'), L('Baricentre', 'Baricentro', 'Centroid'),
        L("La mitjana unix un vèrtex amb el punt mitjà del costat oposat. El baricentre és el centre de gravetat: el triangle s'hi aguanta en equilibri.", "La mediana une un vértice con el punto medio del lado opuesto. El baricentro es el centro de gravedad: el triángulo se sostiene en equilibrio sobre él.", "A median joins a vertex to the midpoint of the opposite side. The centroid is the centre of gravity: the triangle balances on it."))]
s7 += box('def', L("Rectes i punts notables d'un triangle", 'Rectas y puntos notables de un triángulo', 'Special lines and points of a triangle'),
  P(r"En tot triangle hi ha quatre tipus de rectes notables (tres de cada tipus, una per vèrtex o per costat). Les tres rectes de cada tipus es tallen <strong>en un mateix punt</strong>:",
    r"En todo triángulo hay cuatro tipos de rectas notables (tres de cada tipo, una por vértice o por lado). Las tres rectas de cada tipo se cortan <strong>en un mismo punto</strong>:",
    r"Every triangle has four kinds of special lines (three of each kind, one per vertex or side). The three lines of each kind meet <strong>at a single point</strong>:")
  + tbl([L('Rectes', 'Rectas', 'Lines'), L('Punt de tall', 'Punto de corte', 'Meeting point'), L('Què té d\'especial?', '¿Qué tiene de especial?', "What's special?")], [[f'<strong>{a}</strong>', b, c] for a, b, c in NOT])
  + widget('w-notable', '✨', L('Rectes i punts notables', 'Rectas y puntos notables', 'Special lines and points'),
           [seg([('m', L('Mediatrius', 'Mediatrices', 'Bisectors of sides')), ('b', L('Bisectrius', 'Bisectrices', 'Angle bisectors')), ('h', L('Altures', 'Alturas', 'Altitudes')), ('g', L('Mitjanes', 'Medianas', 'Medians'))]),
            '<div class="wrow">' + rng('cx', -1, 6, 0.1, 1.6, 'C') + '</div>',
            '<p class="hint-s">' + L("Mou el vèrtex C i observa on queda el punt de tall en un triangle acutangle, rectangle o obtusangle.", "Mueve el vértice C y observa dónde queda el punto de corte en un triángulo acutángulo, rectángulo u obtusángulo.", "Move vertex C and watch where the meeting point ends up in an acute, right or obtuse triangle.") + '</p>'])
  + note(r"En un triangle rectangle, l'ortocentre és el vèrtex de l'angle recte i el circumcentre és el punt mitjà de la hipotenusa. En un triangle obtusangle, l'ortocentre i el circumcentre queden fora del triangle.",
         r"En un triángulo rectángulo, el ortocentro es el vértice del ángulo recto y el circuncentro es el punto medio de la hipotenusa. En un triángulo obtusángulo, el ortocentro y el circuncentro quedan fuera del triángulo.",
         r"In a right triangle, the orthocentre is the right-angle vertex and the circumcentre is the midpoint of the hypotenuse. In an obtuse triangle, the orthocentre and circumcentre lie outside the triangle."))
s7 += levels(
 [prob(L(r"Dos angles d'un triangle fan \(48^\circ\) i \(75^\circ\). Quant fa el tercer? Classifica el triangle segons els angles.", r"Dos ángulos de un triángulo miden \(48^\circ\) y \(75^\circ\). ¿Cuánto mide el tercero? Clasifica el triángulo según sus ángulos.", r"Two angles of a triangle are \(48^\circ\) and \(75^\circ\). What's the third? Classify the triangle by its angles."),
       D(r"180^\circ-(48^\circ+75^\circ)=180^\circ-123^\circ=\boxed{57^\circ}"),
       P(r"Els tres angles són aguts: és <strong>acutangle</strong>.", r"Los tres ángulos son agudos: es <strong>acutángulo</strong>.", r"All three angles are acute: it's an <strong>acute</strong> triangle.")),
  prob(L(r"Es pot construir un triangle amb segments de 4 cm, 5 cm i 10 cm? I amb 6 cm, 6 cm i 11 cm?", r"¿Se puede construir un triángulo con segmentos de 4 cm, 5 cm y 10 cm? ¿Y con 6 cm, 6 cm y 11 cm?", r"Can a triangle be built from segments of 4 cm, 5 cm and 10 cm? And 6 cm, 6 cm and 11 cm?"),
       D(r"10>4+5=9\ \Rightarrow\ \text{%s}\qquad 11<6+6=12\ \Rightarrow\ \text{%s}" % (Lt('no', 'no', 'no'), Lt('sí (isòsceles)', 'sí (isósceles)', 'yes (isosceles)'))))],
 [prob(L(r"En un triangle isòsceles, l'angle desigual fa \(40^\circ\). Quant fan els altres dos?", r"En un triángulo isósceles, el ángulo desigual mide \(40^\circ\). ¿Cuánto miden los otros dos?", r"In an isosceles triangle the odd angle is \(40^\circ\). What are the other two?"),
       P(r"Els dos angles de la base són iguals i es reparteixen el que falta fins a \(180^\circ\):", r"Los dos ángulos de la base son iguales y se reparten lo que falta hasta \(180^\circ\):", r"The two base angles are equal and share what's left up to \(180^\circ\):"),
       D(r"(180^\circ-40^\circ):2=140^\circ:2=\boxed{70^\circ}\ \text{%s}" % Lt('cadascun', 'cada uno', 'each'))),
  prob(L(r"Un angle agut d'un triangle rectangle fa \(32^\circ\,20'\). Quant fa l'altre?", r"Un ángulo agudo de un triángulo rectángulo mide \(32^\circ\,20'\). ¿Cuánto mide el otro?", r"One acute angle of a right triangle is \(32^\circ\,20'\). What's the other?"),
       D(r"90^\circ-32^\circ\,20'=89^\circ\,60'-32^\circ\,20'=\boxed{57^\circ\,40'}"))],
 [prob(L(r"Els angles d'un triangle mesuren \(x\), \(2x\) i \(3x\). Quant mesura cada angle? Com és el triangle?", r"Los ángulos de un triángulo miden \(x\), \(2x\) y \(3x\). ¿Cuánto mide cada ángulo? ¿Cómo es el triángulo?", r"A triangle's angles are \(x\), \(2x\) and \(3x\). How big is each one? What kind of triangle is it?"),
       D(r"x+2x+3x=180\ \Rightarrow\ 6x=180\ \Rightarrow\ x=30"),
       P(r"Els angles fan \(30^\circ\), \(60^\circ\) i \(90^\circ\): és un triangle <strong>rectangle</strong> (i escalé, perquè té els tres angles diferents).",
         r"Los ángulos miden \(30^\circ\), \(60^\circ\) y \(90^\circ\): es un triángulo <strong>rectángulo</strong> (y escaleno, porque tiene los tres ángulos distintos).",
         r"The angles are \(30^\circ\), \(60^\circ\) and \(90^\circ\): it's a <strong>right</strong> triangle (and scalene, since its three angles are all different)."))])
assert 180 - 48 - 75 == 57 and (180 - 40) // 2 == 70 and dms(sx(90) - sx(32, 20)) == (57, 40, 0)
s7 += practice([
  ('★☆☆', L(r"Pot un triangle tindre dos angles obtusos? I ser rectangle i equilàter alhora?", r"¿Puede un triángulo tener dos ángulos obtusos? ¿Y ser rectángulo y equilátero a la vez?", r"Can a triangle have two obtuse angles? Can it be right and equilateral at once?")),
  ('★★☆', L(r"En un triangle isòsceles, cada angle de la base fa \(52^\circ\). Quant fa l'angle desigual?", r"En un triángulo isósceles, cada ángulo de la base mide \(52^\circ\). ¿Cuánto mide el ángulo desigual?", r"In an isosceles triangle each base angle is \(52^\circ\). What is the odd angle?")),
  ('★★★', L(r"Dos costats d'un triangle fan 4 cm i 9 cm. Entre quins valors pot estar el tercer costat?", r"Dos lados de un triángulo miden 4 cm y 9 cm. ¿Entre qué valores puede estar el tercer lado?", r"Two sides of a triangle are 4 cm and 9 cm. Between which values can the third side be?"))],
  ol(L(r"No: sumarien més de \(180^\circ\). No: els angles d'un equilàter fan \(60^\circ\).", r"No: sumarían más de \(180^\circ\). No: los ángulos de un equilátero miden \(60^\circ\).", r"No: they'd add up to more than \(180^\circ\). No: an equilateral triangle's angles are \(60^\circ\)."),
     r"\(180^\circ-2\cdot52^\circ=76^\circ\)", L(r"Ha de ser més gran que \(9-4=5\) i més menut que \(9+4=13\): entre 5 cm i 13 cm.", r"Debe ser mayor que \(9-4=5\) y menor que \(9+4=13\): entre 5 cm y 13 cm.", r"It must be more than \(9-4=5\) and less than \(9+4=13\): between 5 cm and 13 cm.")))
assert 180 - 2 * 52 == 76

# =====================================================================
# 7.8 Quadrilàters
# =====================================================================
QD = {
 'q': ([(0, 0), (2, 0), (2, 2), (0, 2)], 'quadrat', 'cuadrado', 'square'),
 'r': ([(0, 0), (3, 0), (3, 1.8), (0, 1.8)], 'rectangle', 'rectángulo', 'rectangle'),
 'b': ([(0, 0), (1.6, -1.1), (3.2, 0), (1.6, 1.1)], 'rombe', 'rombo', 'rhombus'),
 'o': ([(0, 0), (2.6, 0), (3.5, 1.6), (0.9, 1.6)], 'romboide', 'romboide', 'parallelogram'),
 'tr': ([(0, 0), (3.2, 0), (2.0, 1.8), (0, 1.8)], 'trapezi rectangle', 'trapecio rectángulo', 'right trapezium'),
 'ti': ([(0, 0), (3.4, 0), (2.5, 1.7), (0.9, 1.7)], 'trapezi isòsceles', 'trapecio isósceles', 'isosceles trapezium'),
 'te': ([(0, 0), (3.4, 0), (2.8, 1.7), (0.4, 1.7)], 'trapezi escalé', 'trapecio escaleno', 'scalene trapezium'),
 'tz': ([(0, 0), (2.8, 0.3), (3.4, 2.0), (0.6, 1.4)], 'trapezoide', 'trapezoide', 'irregular quadrilateral (trapezoid)')}
def qfig(k, W=130, cap=True):
    V, va, es, en = QD[k]
    it = [('poly', V, 'gf')]
    n = len(V)
    sides = [math.dist(V[i], V[(i + 1) % n]) for i in range(n)]
    grp = {}
    for i, s_ in enumerate(sides): grp.setdefault(round(s_, 6), []).append(i)
    t = 1
    for s_, ids in grp.items():
        if len(ids) > 1:
            for i in ids: it.append(('tick', V[i], V[(i + 1) % n], t))
            t += 1
    for i in range(n):
        if abs(angle_at(V[i], V[i - 1], V[(i + 1) % n]) - 90) < 1e-6: it.append(('ra', V[i], V[i - 1], V[(i + 1) % n]))
    return G(it, W=W, pad=10, cap=('<strong>' + L(va, es, en) + '</strong>') if cap else None)
s8 = box('def', L('Classificació dels quadrilàters', 'Clasificación de los cuadriláteros', 'Types of quadrilaterals'),
  P(r"Un <strong>quadrilàter</strong> és un polígon de quatre costats. Té dues diagonals. Els classifiquem segons quants parells de costats <strong>paral·lels</strong> tenen:",
    r"Un <strong>cuadrilátero</strong> es un polígono de cuatro lados. Tiene dos diagonales. Los clasificamos según cuántos pares de lados <strong>paralelos</strong> tienen:",
    r"A <strong>quadrilateral</strong> is a four-sided polygon. It has two diagonals. We classify them by how many pairs of <strong>parallel</strong> sides they have:")
  + ul(L(r"<strong>Paral·lelograms:</strong> els costats oposats són paral·lels dos a dos.", r"<strong>Paralelogramos:</strong> los lados opuestos son paralelos dos a dos.", r"<strong>Parallelograms:</strong> both pairs of opposite sides are parallel."))
  + figs(*[qfig(k) for k in 'qrbo'])
  + ul(L(r"<strong>Trapezis:</strong> només tenen dos costats paral·lels, que s'anomenen <strong>bases</strong>.", r"<strong>Trapecios:</strong> solo tienen dos lados paralelos, que se llaman <strong>bases</strong>.", r"<strong>Trapeziums:</strong> only two sides are parallel; they're called the <strong>bases</strong>."))
  + figs(*[qfig(k) for k in ('tr', 'ti', 'te')], three=True)
  + ul(L(r"<strong>Trapezoides:</strong> no tenen cap parell de costats paral·lels.", r"<strong>Trapezoides:</strong> no tienen ningún par de lados paralelos.", r"<strong>Trapezoids</strong> (irregular quadrilaterals): no parallel sides at all."))
  + figs(qfig('tz')))
YES, NO = '✔', '—'
s8 += box('prop', L('Propietats dels paral·lelograms', 'Propiedades de los paralelogramos', 'Properties of parallelograms'),
  tbl(['', L('Quadrat', 'Cuadrado', 'Square'), L('Rectangle', 'Rectángulo', 'Rectangle'), L('Rombe', 'Rombo', 'Rhombus'), L('Romboide', 'Romboide', 'Parallelogram')],
      [[L('Costats oposats iguals', 'Lados opuestos iguales', 'Opposite sides equal'), YES, YES, YES, YES],
       [L('Els 4 costats iguals', 'Los 4 lados iguales', 'All 4 sides equal'), YES, NO, YES, NO],
       [L('Angles oposats iguals', 'Ángulos opuestos iguales', 'Opposite angles equal'), YES, YES, YES, YES],
       [L('Els 4 angles rectes', 'Los 4 ángulos rectos', 'All 4 angles right'), YES, YES, NO, NO],
       [L('Les diagonals es tallen pel punt mitjà', 'Las diagonales se cortan por el punto medio', 'Diagonals bisect each other'), YES, YES, YES, YES],
       [L('Diagonals iguals', 'Diagonales iguales', 'Equal diagonals'), YES, YES, NO, NO],
       [L('Diagonals perpendiculars', 'Diagonales perpendiculares', 'Perpendicular diagonals'), YES, NO, YES, NO]], cls='c')
  + note(r"El quadrat és alhora un rectangle (té els 4 angles rectes) i un rombe (té els 4 costats iguals): compleix totes les propietats.",
         r"El cuadrado es a la vez un rectángulo (tiene los 4 ángulos rectos) y un rombo (tiene los 4 lados iguales): cumple todas las propiedades.",
         r"A square is both a rectangle (4 right angles) and a rhombus (4 equal sides): it has every property.")
  + widget('w-quad', '🔷', L('Explora els quadrilàters', 'Explora los cuadriláteros', 'Explore quadrilaterals'),
           [seg([(k, L(*QD[k][1:])) for k in ('q', 'r', 'b', 'o', 'tr', 'ti', 'te', 'tz')]), seg([('n', L('Sense diagonals', 'Sin diagonales', 'No diagonals')), ('d', L('Amb diagonals', 'Con diagonales', 'With diagonals'))])])
  + drill('quad', 'Entrena: quin quadrilàter és?', 'Entrena: ¿qué cuadrilátero es?', 'Train: which quadrilateral is it?', mode='opts'))
s8 += box('prop', L("Els angles d'un quadrilàter sumen 360°", 'Los ángulos de un cuadrilátero suman 360°', "A quadrilateral's angles add up to 360°"),
  P(r"Una diagonal dividix qualsevol quadrilàter en <strong>dos triangles</strong>. Els angles dels dos triangles formen exactament els angles del quadrilàter, per tant:",
    r"Una diagonal divide cualquier cuadrilátero en <strong>dos triángulos</strong>. Los ángulos de los dos triángulos forman exactamente los ángulos del cuadrilátero, por tanto:",
    r"A diagonal splits any quadrilateral into <strong>two triangles</strong>. The angles of the two triangles make up exactly the angles of the quadrilateral, so:")
  + D(r"\hat A+\hat B+\hat C+\hat D=2\cdot180^\circ=360^\circ")
  + figs(G([('poly', QD['tz'][0], 'gf'), ('poly', QD['tz'][0][:3], 'tl'), ('seg', QD['tz'][0][0], QD['tz'][0][2], 'hl')] + pnames(QD['tz'][0], 'ABCD'), W=200, pad=16,
           cap=L('Dos triangles: 180° + 180°', 'Dos triángulos: 180° + 180°', 'Two triangles: 180° + 180°')))
  + drill('qang', 'Entrena: angles dels quadrilàters', 'Entrena: ángulos de los cuadriláteros', 'Train: angles in quadrilaterals', mode='int'))
s8 += levels(
 [prob(L(r"Tres angles d'un quadrilàter fan \(85^\circ\), \(110^\circ\) i \(72^\circ\). Quant fa el quart?", r"Tres ángulos de un cuadrilátero miden \(85^\circ\), \(110^\circ\) y \(72^\circ\). ¿Cuánto mide el cuarto?", r"Three angles of a quadrilateral are \(85^\circ\), \(110^\circ\) and \(72^\circ\). What's the fourth?"),
       D(r"360^\circ-(85^\circ+110^\circ+72^\circ)=360^\circ-267^\circ=\boxed{93^\circ}"))],
 [prob(L(r"Un angle d'un rombe fa \(70^\circ\). Quant fan els altres tres?", r"Un ángulo de un rombo mide \(70^\circ\). ¿Cuánto miden los otros tres?", r"One angle of a rhombus is \(70^\circ\). What are the other three?"),
       P(r"En un paral·lelogram els angles oposats són iguals, així que n'hi ha dos de \(70^\circ\). Els altres dos són iguals entre si i completen els \(360^\circ\):",
         r"En un paralelogramo los ángulos opuestos son iguales, así que hay dos de \(70^\circ\). Los otros dos son iguales entre sí y completan los \(360^\circ\):",
         r"In a parallelogram opposite angles are equal, so there are two of \(70^\circ\). The other two are equal and complete the \(360^\circ\):"),
       D(r"(360^\circ-2\cdot70^\circ):2=220^\circ:2=110^\circ\ \Rightarrow\ \boxed{70^\circ,\ 110^\circ,\ 70^\circ,\ 110^\circ}"),
       note(r"Fixa't que dos angles consecutius d'un paral·lelogram sempre són suplementaris: \(70^\circ+110^\circ=180^\circ\).", r"Fíjate en que dos ángulos consecutivos de un paralelogramo siempre son suplementarios: \(70^\circ+110^\circ=180^\circ\).", r"Notice that two consecutive angles of a parallelogram are always supplementary: \(70^\circ+110^\circ=180^\circ\)."))],
 [prob(L(r"Digues si és cert o fals i explica per què: a) tot quadrat és un rombe; b) tot rectangle és un quadrat; c) un trapezi pot tindre dos angles rectes.", r"Di si es verdadero o falso y explica por qué: a) todo cuadrado es un rombo; b) todo rectángulo es un cuadrado; c) un trapecio puede tener dos ángulos rectos.", r"True or false? Explain: a) every square is a rhombus; b) every rectangle is a square; c) a trapezium can have two right angles."),
       P(r"a) <strong>Cert</strong>: el quadrat té els 4 costats iguals. b) <strong>Fals</strong>: un rectangle pot tindre costats desiguals (3 cm × 5 cm). c) <strong>Cert</strong>: el trapezi rectangle té dos angles rectes.",
         r"a) <strong>Verdadero</strong>: el cuadrado tiene los 4 lados iguales. b) <strong>Falso</strong>: un rectángulo puede tener lados desiguales (3 cm × 5 cm). c) <strong>Verdadero</strong>: el trapecio rectángulo tiene dos ángulos rectos.",
         r"a) <strong>True</strong>: a square has 4 equal sides. b) <strong>False</strong>: a rectangle can have unequal sides (3 cm × 5 cm). c) <strong>True</strong>: a right trapezium has two right angles."))])
assert 360 - (85 + 110 + 72) == 93 and (360 - 140) // 2 == 110
s8 += practice([
  ('★☆☆', L(r"Quin paral·lelogram té les diagonals iguals però no perpendiculars?", r"¿Qué paralelogramo tiene las diagonales iguales pero no perpendiculares?", r"Which parallelogram has equal but not perpendicular diagonals?")),
  ('★★☆', L(r"En un trapezi isòsceles, un dels angles fa \(65^\circ\). Quant fan els altres?", r"En un trapecio isósceles, uno de los ángulos mide \(65^\circ\). ¿Cuánto miden los otros?", r"In an isosceles trapezium one angle is \(65^\circ\). What are the others?")),
  ('★★★', L(r"Els angles d'un quadrilàter mesuren \(x\), \(x+10^\circ\), \(x+20^\circ\) i \(x+30^\circ\). Quant fa cadascun?", r"Los ángulos de un cuadrilátero miden \(x\), \(x+10^\circ\), \(x+20^\circ\) y \(x+30^\circ\). ¿Cuánto mide cada uno?", r"A quadrilateral's angles are \(x\), \(x+10^\circ\), \(x+20^\circ\) and \(x+30^\circ\). How big is each?"))],
  ol(L('El rectangle', 'El rectángulo', 'The rectangle'), r"\(65^\circ\), \(115^\circ\), \(115^\circ\)", r"\(4x+60=360\Rightarrow x=75\): \(75^\circ\), \(85^\circ\), \(95^\circ\), \(105^\circ\)"))
assert 4 * 75 + 60 == 360

# =====================================================================
# 7.9 Angles dels polígons. Polígons regulars
# =====================================================================
H6 = reg(6, 1.6)
F_TRI = G([('poly', H6, 'gf')] + [('seg', H6[0], H6[j], 'hl') for j in (2, 3, 4)] + [('txt', ((H6[0][0] + H6[j][0] + H6[j + 1][0]) / 3, (H6[0][1] + H6[j][1] + H6[j + 1][1]) / 3), '180°', {'cls': 'hot'}) for j in (1, 2, 3, 4)], W=200, pad=12,
          cap=L('Hexàgon: 4 triangles → 4 · 180° = 720°', 'Hexágono: 4 triángulos → 4 · 180° = 720°', 'Hexagon: 4 triangles → 4 · 180° = 720°'))
s9 = box('prop', L("Suma dels angles d'un polígon", 'Suma de los ángulos de un polígono', 'Sum of the angles of a polygon'),
  P(r"Si tracem totes les diagonals que ixen d'un vèrtex, un polígon convex de \(n\) costats queda dividit en \(n-2\) triangles. Els angles d'aquests triangles formen els angles del polígon:",
    r"Si trazamos todas las diagonales que salen de un vértice, un polígono convexo de \(n\) lados queda dividido en \(n-2\) triángulos. Los ángulos de estos triángulos forman los ángulos del polígono:",
    r"Drawing all the diagonals from one vertex splits a convex \(n\)-sided polygon into \(n-2\) triangles. The angles of those triangles make up the polygon's angles:")
  + D(r"S=(n-2)\cdot180^\circ")
  + figs(F_TRI)
  + tbl([L('Polígon', 'Polígono', 'Polygon'), 'n', L('Triangles', 'Triángulos', 'Triangles'), L('Suma dels angles', 'Suma de los ángulos', 'Angle sum')],
        [[L(*NAMES[i][1:]), str(NAMES[i][0]), str(NAMES[i][0] - 2), r'\(%d^\circ\)' % ((NAMES[i][0] - 2) * 180)] for i in range(6)], cls='c'))
s9 += box('def', L('Polígons regulars', 'Polígonos regulares', 'Regular polygons'),
  P(r"Recorda que un polígon <strong>regular</strong> té tots els costats i tots els angles iguals. Els seus elements propis són:",
    r"Recuerda que un polígono <strong>regular</strong> tiene todos los lados y todos los ángulos iguales. Sus elementos propios son:",
    r"Remember that a <strong>regular</strong> polygon has all sides and all angles equal. Its special parts are:")
  + ul(L(r"<strong>Centre</strong> \(O\): el punt que està a la mateixa distància de tots els vèrtexs.", r"<strong>Centro</strong> \(O\): el punto que está a la misma distancia de todos los vértices.", r"<strong>Centre</strong> \(O\): the point the same distance from every vertex."),
       L(r"<strong>Radi</strong> \(r\): el segment que unix el centre amb un vèrtex.", r"<strong>Radio</strong> \(r\): el segmento que une el centro con un vértice.", r"<strong>Radius</strong> \(r\): the segment from the centre to a vertex."),
       L(r"<strong>Apotema</strong> \(a\): el segment que unix el centre amb el punt mitjà d'un costat. És perpendicular al costat.", r"<strong>Apotema</strong> \(a\): el segmento que une el centro con el punto medio de un lado. Es perpendicular al lado.", r"<strong>Apothem</strong> \(a\): the segment from the centre to the midpoint of a side. It's perpendicular to the side."),
       L(r"<strong>Angle central</strong>: el que formen dos radis consecutius. Fa \(360^\circ:n\).", r"<strong>Ángulo central</strong>: el que forman dos radios consecutivos. Mide \(360^\circ:n\).", r"<strong>Central angle</strong>: the angle between two consecutive radii. It's \(360^\circ:n\)."))
  + figs(G([('circ', (0, 0), 1.6, 'gc'), ('poly', reg(5, 1.6), 'gf'), ('sect', (0, 0), 0.45, -90 - 36, -90 + 36, 'af'), ('seg', (0, 0), reg(5, 1.6)[0], 'hl'), ('seg', (0, 0), reg(5, 1.6)[1], ''),
            ('seg', (0, 0), (0, -1.6 * math.cos(math.radians(36))), 'ch'), ('ra', (0, -1.6 * math.cos(math.radians(36))), reg(5, 1.6)[1], (0, 0)), ('dot', (0, 0)), lab((0, 0), 'O', 0, -10),
            lab(mid((0, 0), reg(5, 1.6)[0]), 'r', -10, 0, 'hot'), lab((0, -0.95), 'a', 9, 4, 'hot')], W=210, pad=14,
           cap=L('Pentàgon regular: centre, radi, apotema i angle central', 'Pentágono regular: centro, radio, apotema y ángulo central', 'Regular pentagon: centre, radius, apothem and central angle')))
  + P(r"Com que tots els angles són iguals, cadascun val la suma entre \(n\):", r"Como todos los ángulos son iguales, cada uno vale la suma entre \(n\):", r"Since all angles are equal, each one is the sum divided by \(n\):")
  + D(r"\text{%s}=\frac{(n-2)\cdot180^\circ}{n}\qquad\text{%s}=\frac{360^\circ}{n}" % (Lt('Angle interior', 'Ángulo interior', 'Interior angle'), Lt('Angle central', 'Ángulo central', 'Central angle')))
  + D(r"\text{%s: }\frac{4\cdot180^\circ}{6}=\frac{720^\circ}{6}=120^\circ\qquad\frac{360^\circ}{6}=60^\circ" % Lt('Hexàgon regular', 'Hexágono regular', 'Regular hexagon'))
  + note(r"L'angle interior i l'angle central d'un polígon regular sempre són suplementaris: \(120^\circ+60^\circ=180^\circ\).", r"El ángulo interior y el ángulo central de un polígono regular siempre son suplementarios: \(120^\circ+60^\circ=180^\circ\).", r"The interior angle and the central angle of a regular polygon are always supplementary: \(120^\circ+60^\circ=180^\circ\).")
  + widget('w-poly', '⬡', L('Angles dels polígons regulars', 'Ángulos de los polígonos regulares', 'Angles of regular polygons'),
           ['<div class="wrow">' + rng('n', 3, 12, 1, 6, 'n') + '</div>', seg([('t', L('Triangles', 'Triángulos', 'Triangles')), ('c', L('Angle central', 'Ángulo central', 'Central angle')), ('e', L('Elements', 'Elementos', 'Parts'))])])
  + drill('poly', 'Entrena: angles dels polígons', 'Entrena: ángulos de los polígonos', 'Train: polygon angles', mode='dec'))
s9 += box('prop', L('Mosaics amb polígons regulars', 'Mosaicos con polígonos regulares', 'Tiling with regular polygons'),
  P(r"Per a cobrir el terra amb rajoles iguals d'un sol polígon regular, sense deixar buits ni muntar-les, els angles que es troben en cada vèrtex han de sumar \(360^\circ\). Això només passa amb tres polígons:",
    r"Para cubrir el suelo con baldosas iguales de un solo polígono regular, sin dejar huecos ni montarlas, los ángulos que se juntan en cada vértice deben sumar \(360^\circ\). Esto solo pasa con tres polígonos:",
    r"To cover a floor with identical tiles of one regular polygon, with no gaps or overlaps, the angles meeting at each vertex must add up to \(360^\circ\). That only happens with three polygons:")
  + D(r"6\cdot60^\circ=360^\circ\qquad4\cdot90^\circ=360^\circ\qquad3\cdot120^\circ=360^\circ")
  + figs(G([('poly', [(i + 0.5 * (j % 2), j * 0.866), (i + 1 + 0.5 * (j % 2), j * 0.866), (i + 0.5 + 0.5 * (j % 2), (j + 1) * 0.866)], 'gf') for i in range(3) for j in range(2)]
           + [('poly', [(i + 0.5 + 0.5 * (j % 2), (j + 1) * 0.866), (i + 1 + 0.5 * (j % 2), j * 0.866), (i + 1.5 + 0.5 * (j % 2), (j + 1) * 0.866)], 'tl') for i in range(3) for j in range(2) if i + 1.5 + 0.5 * (j % 2) <= 3.6], W=150, pad=8,
           cap=L('Triangles', 'Triángulos', 'Triangles')),
         G([('poly', [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)], 'gf' if (i + j) % 2 else 'tl') for i in range(3) for j in range(2)], W=150, pad=8, cap=L('Quadrats', 'Cuadrados', 'Squares')),
         G([('poly', [(cx + 0.6 * math.cos(math.radians(60 * k)), cy + 0.6 * math.sin(math.radians(60 * k))) for k in range(6)], 'gf' if (i + j) % 2 else 'tl')
            for i in range(3) for j in range(2) for cx, cy in [(i * 0.9, j * 1.039 + (0.52 if i % 2 else 0))]], W=150, pad=8, cap=L('Hexàgons', 'Hexágonos', 'Hexagons')), three=True)
  + P(r"Amb pentàgons regulars no es pot: cada angle fa \(108^\circ\) i \(360\) no és múltiple de \(108\) (3 angles fan \(324^\circ\) i 4 en fan \(432^\circ\)).",
      r"Con pentágonos regulares no se puede: cada ángulo mide \(108^\circ\) y \(360\) no es múltiplo de \(108\) (3 ángulos suman \(324^\circ\) y 4 suman \(432^\circ\)).",
      r"Regular pentagons won't work: each angle is \(108^\circ\) and \(360\) isn't a multiple of \(108\) (3 angles make \(324^\circ\), 4 make \(432^\circ\))."), )
assert 3 * 180 // 5 == 108 and 3 * 108 == 324 and 4 * 108 == 432
s9 += levels(
 [prob(L(r"Quant sumen els angles interiors d'un octàgon? Quant fa cada angle d'un octàgon regular? I l'angle central?", r"¿Cuánto suman los ángulos interiores de un octógono? ¿Cuánto mide cada ángulo de un octógono regular? ¿Y el ángulo central?", r"What do the interior angles of an octagon add up to? How big is each angle of a regular octagon? And the central angle?"),
       D(r"S=(8-2)\cdot180^\circ=6\cdot180^\circ=\boxed{1080^\circ}\qquad1080^\circ:8=\boxed{135^\circ}\qquad360^\circ:8=\boxed{45^\circ}"))],
 [prob(L(r"Cada angle interior d'un polígon regular fa \(140^\circ\). Quants costats té?", r"Cada ángulo interior de un polígono regular mide \(140^\circ\). ¿Cuántos lados tiene?", r"Each interior angle of a regular polygon is \(140^\circ\). How many sides does it have?"),
       P(r"L'angle central és el suplementari de l'interior: \(180^\circ-140^\circ=40^\circ\). Com que l'angle central fa \(360^\circ:n\):",
         r"El ángulo central es el suplementario del interior: \(180^\circ-140^\circ=40^\circ\). Como el ángulo central mide \(360^\circ:n\):",
         r"The central angle is the supplement of the interior angle: \(180^\circ-140^\circ=40^\circ\). Since the central angle is \(360^\circ:n\):"),
       D(r"n=360^\circ:40^\circ=9\ \Rightarrow\ \text{%s}" % Lt('és un enneàgon', 'es un eneágono', "it's a nonagon")),
       P(r"Comprovació: \((9-2)\cdot180^\circ=1260^\circ\) i \(1260^\circ:9=140^\circ\ \checkmark\)", r"Comprobación: \((9-2)\cdot180^\circ=1260^\circ\) y \(1260^\circ:9=140^\circ\ \checkmark\)", r"Check: \((9-2)\cdot180^\circ=1260^\circ\) and \(1260^\circ:9=140^\circ\ \checkmark\)"))],
 [prob(L(r"Els angles interiors d'un polígon sumen \(1800^\circ\). Quants costats té? Quantes diagonals?", r"Los ángulos interiores de un polígono suman \(1800^\circ\). ¿Cuántos lados tiene? ¿Cuántas diagonales?", r"A polygon's interior angles add up to \(1800^\circ\). How many sides does it have? How many diagonals?"),
       D(r"(n-2)\cdot180=1800\ \Rightarrow\ n-2=1800:180=10\ \Rightarrow\ n=12"),
       P(r"És un <strong>dodecàgon</strong>, i té \(\dfrac{12\cdot9}{2}=\boxed{54}\) diagonals.", r"Es un <strong>dodecágono</strong>, y tiene \(\dfrac{12\cdot9}{2}=\boxed{54}\) diagonales.", r"It's a <strong>dodecagon</strong>, with \(\dfrac{12\cdot9}{2}=\boxed{54}\) diagonals."))])
assert 6 * 180 == 1080 and 1080 // 8 == 135 and 360 // 8 == 45 and 360 // 40 == 9 and 7 * 180 == 1260 and 1260 // 9 == 140 and 1800 // 180 + 2 == 12
s9 += practice([
  ('★☆☆', L(r"Quant fa cada angle d'un pentàgon regular? I l'angle central?", r"¿Cuánto mide cada ángulo de un pentágono regular? ¿Y el ángulo central?", r"How big is each angle of a regular pentagon? And the central angle?")),
  ('★★☆', L(r"L'angle central d'un polígon regular fa \(30^\circ\). Quin polígon és? Quant fa cada angle interior?", r"El ángulo central de un polígono regular mide \(30^\circ\). ¿Qué polígono es? ¿Cuánto mide cada ángulo interior?", r"The central angle of a regular polygon is \(30^\circ\). Which polygon is it? How big is each interior angle?")),
  ('★★★', L(r"Es pot fer un mosaic només amb octàgons regulars? Per què?", r"¿Se puede hacer un mosaico solo con octógonos regulares? ¿Por qué?", r"Can you tile a floor with regular octagons only? Why?"))],
  ol(r"\(540^\circ:5=108^\circ\); \(72^\circ\)", L(r"\(360:30=12\): dodecàgon; \(180^\circ-30^\circ=150^\circ\)", r"\(360:30=12\): dodecágono; \(180^\circ-30^\circ=150^\circ\)", r"\(360:30=12\): dodecagon; \(180^\circ-30^\circ=150^\circ\)"),
     L(r"No: cada angle fa \(135^\circ\) i \(360\) no és múltiple de \(135\) (2 angles fan \(270^\circ\) i 3 en fan \(405^\circ\)).", r"No: cada ángulo mide \(135^\circ\) y \(360\) no es múltiplo de \(135\) (2 ángulos suman \(270^\circ\) y 3 suman \(405^\circ\)).", r"No: each angle is \(135^\circ\) and \(360\) isn't a multiple of \(135\) (2 angles make \(270^\circ\), 3 make \(405^\circ\)).")))
assert 540 // 5 == 108 and 360 // 5 == 72 and 360 // 30 == 12 and 2 * 135 == 270 and 3 * 135 == 405
