# Apartats 8.7-8.9 dels apunts de la Unitat 8 de 1r ESO: la circumferència i la seua longitud, l'àrea del cercle
# i de les figures circulars, i les figures compostes. Tots els càlculs amb π ≈ 3,14 (PI3).
from comu import *

def T_(P, t, **o): return ('txt', P, t, o)
p = PI3

# =====================================================================
# 8.7 La circumferència i la seua longitud
# =====================================================================
F_ELEM = [('circ', (0, 0), 3, 'gc'), ('arc', (0, 0), 3, 20, 75, 'hl'), ('seg', (0, 0), pol((0, 0), 3, 140), 'ch'), ('seg', pol((0, 0), 3, 200), pol((0, 0), 3, 20), ''),
          ('seg', pol((0, 0), 3, 250), pol((0, 0), 3, 320), 'd'), ('dot', (0, 0)),
          T_((0, 0), 'O', dx=8, dy=12), T_(mid((0, 0), pol((0, 0), 3, 140)), L('radi', 'radio', 'radius'), dx=-6, dy=-6, a='end', cls='c1'),
          T_(mid(pol((0, 0), 3, 200), pol((0, 0), 3, 20)), L('diàmetre', 'diámetro', 'diameter'), dx=10, dy=16),
          T_(pol((0, 0), 3.4, 48), L('arc', 'arco', 'arc'), a='start', cls='hot'), T_(mid(pol((0, 0), 3, 250), pol((0, 0), 3, 320)), L('corda', 'cuerda', 'chord'), dy=-8)]
s7 = box('def', L('Circumferència i cercle', 'Circunferencia y círculo', 'Circle and disc'),
  ul(L(r"La <strong>circumferència</strong> és la línia corba tancada formada pels punts que estan a la mateixa distància d'un punt interior, el <strong>centre</strong> \(O\). És una <strong>línia</strong>: té longitud.",
       r"La <strong>circunferencia</strong> es la línea curva cerrada formada por los puntos que están a la misma distancia de un punto interior, el <strong>centro</strong> \(O\). Es una <strong>línea</strong>: tiene longitud.",
       r"A <strong>circle</strong> is the closed curved line made of all the points at the same distance from an inside point, the <strong>centre</strong> \(O\). It's a <strong>line</strong>: it has a length."),
     L(r"El <strong>cercle</strong> és la superfície que queda dins de la circumferència. És una <strong>superfície</strong>: té àrea.",
       r"El <strong>círculo</strong> es la superficie que queda dentro de la circunferencia. Es una <strong>superficie</strong>: tiene área.",
       r"The <strong>disc</strong> is the surface inside the circle. It's a <strong>surface</strong>: it has an area."))
  + figs(G(F_ELEM, W=220, pad=40))
  + ul(L(r"<strong>Radi</strong> \(r\): segment que unix el centre amb un punt de la circumferència.", r"<strong>Radio</strong> \(r\): segmento que une el centro con un punto de la circunferencia.", r"<strong>Radius</strong> \(r\): segment from the centre to a point on the circle."),
       L(r"<strong>Corda</strong>: segment que unix dos punts de la circumferència. La corda que passa pel centre és el <strong>diàmetre</strong> \(d\), i fa el doble que el radi: \(d=2r\).", r"<strong>Cuerda</strong>: segmento que une dos puntos de la circunferencia. La cuerda que pasa por el centro es el <strong>diámetro</strong> \(d\), y mide el doble que el radio: \(d=2r\).", r"<strong>Chord</strong>: segment joining two points on the circle. The chord through the centre is the <strong>diameter</strong> \(d\), twice the radius: \(d=2r\)."),
       L(r"<strong>Arc</strong>: tros de circumferència entre dos punts. El diàmetre dividix la circumferència en dues <strong>semicircumferències</strong>.", r"<strong>Arco</strong>: trozo de circunferencia entre dos puntos. El diámetro divide la circunferencia en dos <strong>semicircunferencias</strong>.", r"<strong>Arc</strong>: part of the circle between two points. A diameter splits the circle into two <strong>semicircles</strong>.")))
OBJ = [(L('Moneda d\'1 €', 'Moneda de 1 €', '€1 coin'), 2.3, 7.2), (L('Got', 'Vaso', 'Glass'), 7, 22), (L('Plat', 'Plato', 'Plate'), 24, 75.4), (L('Roda de bici', 'Rueda de bici', 'Bike wheel'), 66, 207.3)]
s7 += box('prop', L('Longitud de la circumferència. El nombre π', 'Longitud de la circunferencia. El número π', 'Circumference. The number π'),
  P(r"Si mesurem amb una cinta la longitud \(L\) de diverses circumferències i la dividim pel seu diàmetre, sempre ix <strong>una mica més de 3</strong>:",
    r"Si medimos con una cinta la longitud \(L\) de varias circunferencias y la dividimos por su diámetro, siempre sale <strong>un poco más de 3</strong>:",
    r"If we measure the length \(L\) of several circles with a tape and divide it by the diameter, we always get <strong>a little more than 3</strong>:")
  + tbl([L('Objecte', 'Objeto', 'Object'), L('Diàmetre (cm)', 'Diámetro (cm)', 'Diameter (cm)'), L('Longitud (cm)', 'Longitud (cm)', 'Length (cm)'), r'\(L:d\)'],
        [[o, nf(d), nf(l), nf(l / d)] for o, d, l in OBJ], 'c')
  + P(r"Aquest quocient és sempre el mateix: és el nombre <strong>pi</strong>, \(\pi=3{,}14159\ldots\), que té infinites xifres decimals. Normalment fem servir \(\pi\approx3{,}14\). Per tant, la circumferència fa \(\pi\) vegades el diàmetre:",
      r"Este cociente es siempre el mismo: es el número <strong>pi</strong>, \(\pi=3{,}14159\ldots\), que tiene infinitas cifras decimales. Normalmente usamos \(\pi\approx3{,}14\). Por tanto, la circunferencia mide \(\pi\) veces el diámetro:",
      r"This quotient is always the same: it's the number <strong>pi</strong>, \(\pi=3.14159\ldots\), which has infinitely many decimal places. We usually use \(\pi\approx3.14\). So the circle is \(\pi\) times as long as its diameter:")
  + D(r"L=\pi\cdot d=2\cdot\pi\cdot r")
  + P(r"Una circumferència de 5 cm de radi fa \(L=2\cdot3{,}14\cdot5=31{,}4\ \text{cm}\).", r"Una circunferencia de 5 cm de radio mide \(L=2\cdot3{,}14\cdot5=31{,}4\ \text{cm}\).", r"A circle with a 5 cm radius is \(L=2\cdot3.14\cdot5=31.4\ \text{cm}\) long.")
  + widget('w-pi', '🛞', L('Fes rodar la roda', 'Haz rodar la rueda', 'Roll the wheel'),
           ['<div class="wrow">' + rng('d', 1, 10, 0.5, 4, 'd') + rng('t', 0, 1, 0.01, 0, 'volta') + '</div>'], out='<div class="gout"></div>')
  + note(r"Amb la calculadora pots fer servir la tecla \(\pi\): el resultat canvia molt poc. En aquesta unitat fem els càlculs amb \(\pi\approx3{,}14\).",
         r"Con la calculadora puedes usar la tecla \(\pi\): el resultado cambia muy poco. En esta unidad hacemos los cálculos con \(\pi\approx3{,}14\).",
         r"On a calculator you can use the \(\pi\) key: the answer changes very little. In this unit we work with \(\pi\approx3.14\).", '🧮'))
for o, d, l in OBJ: assert 3.1 < l / d < 3.16, (d, l)
ck(2 * p * 5, 31.4)
s7 += box('prop', L("Longitud d'un arc", 'Longitud de un arco', 'Length of an arc'),
  P(r"Una circumferència completa són \(360^\circ\). Un arc de \(n^\circ\) és la fracció \(\dfrac{n}{360}\) de la circumferència:",
    r"Una circunferencia completa son \(360^\circ\). Un arco de \(n^\circ\) es la fracción \(\dfrac{n}{360}\) de la circunferencia:",
    r"A whole circle is \(360^\circ\). An arc of \(n^\circ\) is the fraction \(\dfrac{n}{360}\) of the circle:")
  + D(r"L_{\text{arc}}=\frac{2\cdot\pi\cdot r\cdot n}{360}")
  + P(r"Per exemple, la semicircumferència és la meitat (\(180^\circ\)) i el quart de circumferència, la quarta part (\(90^\circ\)). Un arc de \(90^\circ\) en una circumferència de 10 cm de radi fa \(\dfrac{2\cdot3{,}14\cdot10\cdot90}{360}=\dfrac{62{,}8}{4}=15{,}7\ \text{cm}\).",
      r"Por ejemplo, la semicircunferencia es la mitad (\(180^\circ\)) y el cuarto de circunferencia, la cuarta parte (\(90^\circ\)). Un arco de \(90^\circ\) en una circunferencia de 10 cm de radio mide \(\dfrac{2\cdot3{,}14\cdot10\cdot90}{360}=\dfrac{62{,}8}{4}=15{,}7\ \text{cm}\).",
      r"For example, a semicircle is half the circle (\(180^\circ\)) and a quarter circle is a quarter (\(90^\circ\)). A \(90^\circ\) arc of a circle with a 10 cm radius is \(\dfrac{2\cdot3.14\cdot10\cdot90}{360}=\dfrac{62.8}{4}=15.7\ \text{cm}\) long.")
  + widget('w-circ', '◔', L('Circumferència i arcs', 'Circunferencia y arcos', 'Circles and arcs'),
           ['<div class="wrow">' + rng('r', 1, 12, 0.5, 5, 'r') + rng('n', 10, 360, 5, 90, 'n') + '</div>'], out='<div class="gout"></div>')
  + drill('circ', 'Entrena: longitud de la circumferència', 'Entrena: longitud de la circunferencia', 'Train: circumference'))
ck(2 * p * 10 * 90 / 360, 15.7); ck(2 * p * 10, 62.8)
s7 += levels(
 [prob(L(r"Calcula la longitud d'una circumferència de 5 cm de radi i la d'una altra de 12 cm de diàmetre.", r"Calcula la longitud de una circunferencia de 5 cm de radio y la de otra de 12 cm de diámetro.", r"Find the length of a circle with a 5 cm radius and of another with a 12 cm diameter."),
       D(r"L=2\cdot3{,}14\cdot5=\boxed{31{,}4\ \text{cm}}\qquad L=3{,}14\cdot12=\boxed{37{,}68\ \text{cm}}"))],
 [prob(L(r"La roda d'una bicicleta fa 60 cm de diàmetre. Quants metres avança la bici quan la roda fa una volta? I quan en fa 1000?", r"La rueda de una bicicleta mide 60 cm de diámetro. ¿Cuántos metros avanza la bici cuando la rueda da una vuelta? ¿Y cuando da 1000?", r"A bike wheel is 60 cm across. How many metres does the bike move when the wheel turns once? And when it turns 1000 times?"),
       P(r"En cada volta, la bici avança tant com fa la circumferència de la roda:", r"En cada vuelta, la bici avanza tanto como mide la circunferencia de la rueda:", r"Each turn, the bike moves as far as the length of the wheel's circle:"),
       D(r"L=3{,}14\cdot60=188{,}4\ \text{cm}=\boxed{1{,}884\ \text{m}}\qquad 1000\cdot1{,}884=\boxed{1884\ \text{m}}")),
  prob(L(r"Calcula la longitud d'un arc de \(60^\circ\) en una circumferència de 6 cm de radi.", r"Calcula la longitud de un arco de \(60^\circ\) en una circunferencia de 6 cm de radio.", r"Find the length of a \(60^\circ\) arc of a circle with a 6 cm radius."),
       D(r"L_{\text{arc}}=\frac{2\cdot3{,}14\cdot6\cdot60}{360}=\frac{2260{,}8}{360}=\boxed{6{,}28\ \text{cm}}"))],
 [prob(L(r"Una circumferència fa 94,2 cm de longitud. Quant fan el diàmetre i el radi?", r"Una circunferencia mide 94,2 cm de longitud. ¿Cuánto miden el diámetro y el radio?", r"A circle is 94.2 cm long. How long are its diameter and its radius?"),
       P(r"Fem el camí al revés: si \(L=\pi\cdot d\), aleshores \(d=L:\pi\).", r"Hacemos el camino al revés: si \(L=\pi\cdot d\), entonces \(d=L:\pi\).", r"Work backwards: if \(L=\pi\cdot d\), then \(d=L\div\pi\)."),
       D(r"d=94{,}2:3{,}14=\boxed{30\ \text{cm}}\qquad r=30:2=\boxed{15\ \text{cm}}")),
  prob(L(r"Calcula el perímetre d'un semicercle de 4 cm de radi (la figura tancada pel diàmetre i la semicircumferència).", r"Calcula el perímetro de un semicírculo de 4 cm de radio (la figura cerrada por el diámetro y la semicircunferencia).", r"Find the perimeter of a semicircle with a 4 cm radius (the shape bounded by the diameter and the half circle)."),
       figs(G([('sect', (0, 0), 4, 0, 180, 'gf'), ('seg', (-4, 0), (4, 0), 'hl'), ('arc', (0, 0), 4, 0, 180, 'hl'), ('dot', (0, 0)), T_((2, 0), '4', dy=15)], W=160)),
       D(r"\frac{2\cdot3{,}14\cdot4}{2}+8=12{,}56+8=\boxed{20{,}56\ \text{cm}}"),
       P(r"No et deixes el diàmetre: també forma part del contorn.", r"No te dejes el diámetro: también forma parte del contorno.", r"Don't forget the diameter: it's part of the boundary too."))])
ck(2 * p * 5, 31.4); ck(p * 12, 37.68); ck(p * 60, 188.4); ck(1000 * R(1884, 1000), 1884); ck(2 * p * 6 * 60, 2260.8); ck(2 * p * 6 * 60 / 360, 6.28); ck(R(942, 10) / p, 30); ck(p * 4 + 8, 20.56)
s7 += practice([
  ('★', L(r"a) Longitud d'una circumferència de 3 cm de radi. b) Longitud d'una circumferència de 25 cm de diàmetre.", r"a) Longitud de una circunferencia de 3 cm de radio. b) Longitud de una circunferencia de 25 cm de diámetro.", r"a) Length of a circle with a 3 cm radius. b) Length of a circle with a 25 cm diameter.")),
  ('★★', L(r"c) Una circumferència fa 62,8 cm. Quant fa el radi? d) Longitud d'un arc de \(45^\circ\) en una circumferència de 8 cm de radi.", r"c) Una circunferencia mide 62,8 cm. ¿Cuánto mide el radio? d) Longitud de un arco de \(45^\circ\) en una circunferencia de 8 cm de radio.", r"c) A circle is 62.8 cm long. How long is its radius? d) Length of a \(45^\circ\) arc of a circle with an 8 cm radius.")),
  ('★★★', L(r"e) El radi de la Terra fa uns 6370 km. Quina distància recorreria algú que fera la volta a la Terra per l'equador?", r"e) El radio de la Tierra mide unos 6370 km. ¿Qué distancia recorrería alguien que diera la vuelta a la Tierra por el ecuador?", r"e) The Earth's radius is about 6370 km. How far would someone travel going round the Earth along the equator?"))],
  P(r"a) 18,84 cm. b) 78,5 cm. c) \(d=62{,}8:3{,}14=20\), \(r=10\) cm. d) \(\tfrac{50{,}24}{8}=6{,}28\) cm. e) \(2\cdot3{,}14\cdot6370=40\,003{,}6\) km (uns 40 000 km).",
    r"a) 18,84 cm. b) 78,5 cm. c) \(d=62{,}8:3{,}14=20\), \(r=10\) cm. d) \(\tfrac{50{,}24}{8}=6{,}28\) cm. e) \(2\cdot3{,}14\cdot6370=40\,003{,}6\) km (unos 40 000 km).",
    r"a) 18.84 cm. b) 78.5 cm. c) \(d=62.8\div3.14=20\), \(r=10\) cm. d) \(\tfrac{50.24}{8}=6.28\) cm. e) \(2\cdot3.14\cdot6370=40\,003.6\) km (about 40 000 km)."))
ck(2 * p * 3, 18.84); ck(p * 25, 78.5); ck(R(628, 10) / p, 20); ck(2 * p * 8, 50.24); ck(2 * p * 8 * 45 / 360, 6.28); ck(2 * p * 6370, 40003.6)

# =====================================================================
# 8.8 L'àrea del cercle i de les figures circulars
# =====================================================================
def pizza(n, r=1):
    th = 360 / n; hw = math.sin(math.radians(th / 2)); ch = math.cos(math.radians(th / 2))
    it1 = [('sect', (0, 0), r, 90 - th / 2 + k * th, 90 + th / 2 + k * th, 'q1' if k % 2 else 'q0') for k in range(n)]
    it2 = []
    for k in range(n // 2):
        it2.append(('sect', (2 * k * hw, 0), r, 90 - th / 2, 90 + th / 2, 'q0'))
        it2.append(('sect', (2 * k * hw + hw, ch), r, 270 - th / 2, 270 + th / 2, 'q1'))
    it2 += [T_(((n * hw) / 2 - hw / 2, 0), '≈ π · r', dy=15), T_((-hw, ch / 2), 'r', dx=-6, a='end')]
    return it1, it2
P1, P2 = pizza(16)
s8 = box('prop', L("Àrea del cercle", 'Área del círculo', 'Area of a disc'),
  P(r"Tallem el cercle en molts sectors iguals (com una pizza) i els col·loquem alternant-los cap amunt i cap avall. La figura s'assembla a un <strong>rectangle</strong> d'altura \(r\) i de base la meitat de la circumferència, \(\pi\cdot r\):",
    r"Cortamos el círculo en muchos sectores iguales (como una pizza) y los colocamos alternándolos hacia arriba y hacia abajo. La figura se parece a un <strong>rectángulo</strong> de altura \(r\) y de base la mitad de la circunferencia, \(\pi\cdot r\):",
    r"Cut the disc into lots of equal sectors (like a pizza) and lay them side by side, alternately pointing up and down. The shape looks like a <strong>rectangle</strong> of height \(r\) whose base is half the circle, \(\pi\cdot r\):")
  + figs(G(P1, W=140), G(P2, W=300))
  + D(r"A_{\text{%s}}=\pi\cdot r\cdot r=\pi\cdot r^2" % Lt('cercle', 'círculo', 'disc'))
  + P(r"Un cercle de 5 cm de radi té \(A=3{,}14\cdot5^2=3{,}14\cdot25=78{,}5\ \text{cm}^2\).", r"Un círculo de 5 cm de radio tiene \(A=3{,}14\cdot5^2=3{,}14\cdot25=78{,}5\ \text{cm}^2\).", r"A disc with a 5 cm radius has \(A=3.14\cdot5^2=3.14\cdot25=78.5\ \text{cm}^2\).")
  + note(r"Compte! Primer fem el quadrat del radi i després multipliquem per \(\pi\). I si et donen el <strong>diàmetre</strong>, abans has de calcular el radi: \(r=d:2\).",
         r"¡Cuidado! Primero hacemos el cuadrado del radio y después multiplicamos por \(\pi\). Y si te dan el <strong>diámetro</strong>, antes tienes que calcular el radio: \(r=d:2\).",
         r"Careful! Square the radius first and then multiply by \(\pi\). And if you're given the <strong>diameter</strong>, work out the radius first: \(r=d\div2\).", '⚠️')
  + widget('w-pizza', '🍕', L('Del cercle al rectangle', 'Del círculo al rectángulo', 'From disc to rectangle'),
           ['<div class="wrow">' + rng('n', 4, 40, 2, 8, 'n') + '</div>'], out='<div class="gout"></div>'))
ck(p * 25, 78.5)
s8 += box('prop', L('Figures circulars', 'Figuras circulares', 'Circular shapes'),
  figs(G([('circ', (0, 0), 2, 'gc'), ('sect', (0, 0), 2, 0, 180, 'sh'), ('seg', (-2, 0), (2, 0), ''), ('dot', (0, 0))], W=130, cap=L(r'Semicercle: \(A=\dfrac{\pi\cdot r^2}{2}\)', r'Semicírculo: \(A=\dfrac{\pi\cdot r^2}{2}\)', r'Semicircle: \(A=\dfrac{\pi\cdot r^2}{2}\)')),
       G([('circ', (0, 0), 2, 'gc'), ('sect', (0, 0), 2, 0, 90, 'sh'), ('dot', (0, 0))], W=130, cap=L(r'Quart de cercle: \(A=\dfrac{\pi\cdot r^2}{4}\)', r'Cuarto de círculo: \(A=\dfrac{\pi\cdot r^2}{4}\)', r'Quarter disc: \(A=\dfrac{\pi\cdot r^2}{4}\)')),
       G([('circ', (0, 0), 2, 'gc'), ('sect', (0, 0), 2, 20, 130, 'sh'), ('arc', (0, 0), 0.5, 20, 130, 'ang'), T_(pol((0, 0), 0.85, 75), 'n°'), ('dot', (0, 0))], W=130,
         cap=L(r'Sector circular: \(A=\dfrac{\pi\cdot r^2\cdot n}{360}\)', r'Sector circular: \(A=\dfrac{\pi\cdot r^2\cdot n}{360}\)', r'Sector: \(A=\dfrac{\pi\cdot r^2\cdot n}{360}\)')),
       G([('circ', (0, 0), 2, 'sh'), ('circ', (0, 0), 1.1, 'hole'), ('circ', (0, 0), 1.1, 'gc'), ('seg', (0, 0), pol((0, 0), 2, 35), ''), ('seg', (0, 0), pol((0, 0), 1.1, 160), 'd'), ('dot', (0, 0)),
          T_(pol((0, 0), 1.55, 45), 'R'), T_(pol((0, 0), 0.55, 175), 'r')], W=130,
         cap=L(r'Corona circular: \(A=\pi\cdot R^2-\pi\cdot r^2\)', r'Corona circular: \(A=\pi\cdot R^2-\pi\cdot r^2\)', r'Ring (annulus): \(A=\pi\cdot R^2-\pi\cdot r^2\)')), three=True)
  + ul(L(r"Un <strong>sector circular</strong> és el tros de cercle entre dos radis. Com passava amb els arcs, un sector de \(n^\circ\) és la fracció \(\dfrac{n}{360}\) del cercle.", r"Un <strong>sector circular</strong> es el trozo de círculo entre dos radios. Como pasaba con los arcos, un sector de \(n^\circ\) es la fracción \(\dfrac{n}{360}\) del círculo.", r"A <strong>sector</strong> is the slice of disc between two radii. As with arcs, a sector of \(n^\circ\) is the fraction \(\dfrac{n}{360}\) of the disc."),
       L(r"Una <strong>corona circular</strong> és la superfície entre dues circumferències concèntriques (amb el mateix centre): el cercle gran menys el menut.", r"Una <strong>corona circular</strong> es la superficie entre dos circunferencias concéntricas (con el mismo centro): el círculo grande menos el pequeño.", r"A <strong>ring</strong> (annulus) is the surface between two circles with the same centre: the big disc minus the small one."))
  + widget('w-circa', '⭕', L('Àrees de figures circulars', 'Áreas de figuras circulares', 'Areas of circular shapes'),
           [seg([('c', L('Cercle', 'Círculo', 'Disc')), ('s', L('Sector', 'Sector', 'Sector')), ('k', L('Corona', 'Corona', 'Ring'))]),
            '<div class="wrow">' + rng('R', 1, 12, 0.5, 6, 'R') + rng('r', 0.5, 11, 0.5, 3, 'r') + rng('n', 10, 350, 10, 90, 'n') + '</div>'],
           out='<div class="gout"></div>')
  + drill('circa', "Entrena: àrea del cercle i de les figures circulars", "Entrena: área del círculo y de las figuras circulares", "Train: areas of discs and circular shapes"))
s8 += levels(
 [prob(L(r"Calcula l'àrea d'un cercle de 10 cm de radi i la d'un altre de 8 cm de diàmetre.", r"Calcula el área de un círculo de 10 cm de radio y la de otro de 8 cm de diámetro.", r"Find the area of a disc with a 10 cm radius and of another with an 8 cm diameter."),
       D(r"A=3{,}14\cdot10^2=3{,}14\cdot100=\boxed{314\ \text{cm}^2}"),
       D(r"r=8:2=4\qquad A=3{,}14\cdot4^2=3{,}14\cdot16=\boxed{50{,}24\ \text{cm}^2}"))],
 [prob(L(r"Calcula l'àrea d'un sector circular de \(60^\circ\) i 6 cm de radi.", r"Calcula el área de un sector circular de \(60^\circ\) y 6 cm de radio.", r"Find the area of a \(60^\circ\) sector with a 6 cm radius."),
       D(r"A=\frac{3{,}14\cdot6^2\cdot60}{360}=\frac{3{,}14\cdot36}{6}=\boxed{18{,}84\ \text{cm}^2}")),
  prob(L(r"Calcula l'àrea d'una corona circular de radis 5 cm i 3 cm.", r"Calcula el área de una corona circular de radios 5 cm y 3 cm.", r"Find the area of a ring with radii of 5 cm and 3 cm."),
       D(r"A=3{,}14\cdot5^2-3{,}14\cdot3^2=78{,}5-28{,}26=\boxed{50{,}24\ \text{cm}^2}"))],
 [prob(L(r"Què és més pizza: una pizza de 30 cm de diàmetre o dues de 20 cm?", r"¿Qué es más pizza: una pizza de 30 cm de diámetro o dos de 20 cm?", r"Which is more pizza: one 30 cm pizza or two 20 cm pizzas?"),
       D(r"A_{30}=3{,}14\cdot15^2=706{,}5\ \text{cm}^2\qquad 2\cdot A_{20}=2\cdot3{,}14\cdot10^2=628\ \text{cm}^2"),
       P(r"La pizza gran té <strong>més</strong> superfície que les dues menudes juntes.", r"La pizza grande tiene <strong>más</strong> superficie que las dos pequeñas juntas.", r"The big pizza has <strong>more</strong> surface than the two small ones together.")),
  prob(L(r"Una pista circular té un radi de 12 m. Al voltant hi ha un camí d'1,5 m d'amplària. Calcula l'àrea del camí.", r"Una pista circular tiene un radio de 12 m. Alrededor hay un camino de 1,5 m de anchura. Calcula el área del camino.", r"A circular track has a 12 m radius. Around it there's a path 1.5 m wide. Find the area of the path."),
       P(r"El camí és una corona circular de radis \(R=12+1{,}5=13{,}5\) m i \(r=12\) m:", r"El camino es una corona circular de radios \(R=12+1{,}5=13{,}5\) m y \(r=12\) m:", r"The path is a ring with radii \(R=12+1.5=13.5\) m and \(r=12\) m:"),
       D(r"A=3{,}14\cdot13{,}5^2-3{,}14\cdot12^2=572{,}265-452{,}16=\boxed{120{,}105\ \text{m}^2}"))])
ck(p * 100, 314); ck(p * 16, 50.24); ck(p * 36 * 60 / 360, 18.84); ck(p * 25 - p * 9, 50.24); ck(p * 9, 28.26); ck(p * 225, 706.5); ck(2 * p * 100, 628)
ck(p * R(135, 10) ** 2, 572.265); ck(p * 144, 452.16); ck(p * R(135, 10) ** 2 - p * 144, 120.105)
s8 += practice([
  ('★', L(r"a) Àrea d'un cercle de 7 cm de radi. b) Àrea d'un cercle de 6 cm de diàmetre.", r"a) Área de un círculo de 7 cm de radio. b) Área de un círculo de 6 cm de diámetro.", r"a) Area of a disc with a 7 cm radius. b) Area of a disc with a 6 cm diameter.")),
  ('★★', L(r"c) Àrea d'un quart de cercle de 4 cm de radi. d) Àrea d'un sector de \(120^\circ\) i 3 cm de radi.", r"c) Área de un cuarto de círculo de 4 cm de radio. d) Área de un sector de \(120^\circ\) y 3 cm de radio.", r"c) Area of a quarter disc with a 4 cm radius. d) Area of a \(120^\circ\) sector with a 3 cm radius.")),
  ('★★★', L(r"e) Àrea d'una corona circular de radis 10 cm i 8 cm. f) Un cercle té 113,04 cm² d'àrea. Quant fa el radi?", r"e) Área de una corona circular de radios 10 cm y 8 cm. f) Un círculo tiene 113,04 cm² de área. ¿Cuánto mide el radio?", r"e) Area of a ring with radii of 10 cm and 8 cm. f) A disc has an area of 113.04 cm². How long is its radius?"))],
  P(r"a) 153,86 cm². b) \(r=3\): 28,26 cm². c) 12,56 cm². d) 9,42 cm². e) \(314-200{,}96=113{,}04\) cm². f) \(r^2=113{,}04:3{,}14=36\Rightarrow r=6\) cm.",
    r"a) 153,86 cm². b) \(r=3\): 28,26 cm². c) 12,56 cm². d) 9,42 cm². e) \(314-200{,}96=113{,}04\) cm². f) \(r^2=113{,}04:3{,}14=36\Rightarrow r=6\) cm.",
    r"a) 153.86 cm². b) \(r=3\): 28.26 cm². c) 12.56 cm². d) 9.42 cm². e) \(314-200.96=113.04\) cm². f) \(r^2=113.04\div3.14=36\Rightarrow r=6\) cm."))
ck(p * 49, 153.86); ck(p * 9, 28.26); ck(p * 16 / 4, 12.56); ck(p * 9 * 120 / 360, 9.42); ck(p * 64, 200.96); ck(p * 100 - p * 64, 113.04); ck(R(11304, 100) / p, 36)

# =====================================================================
# 8.9 Figures compostes
# =====================================================================
F_L = [('poly', [(0, 0), (8, 0), (8, 4), (5, 4), (5, 6), (0, 6)], 'gf'), T_((4, 0), '8', dy=16), T_((0, 3), '6', dx=-8, a='end'), T_((8, 2), '4', dx=8, a='start'), T_((6.5, 4), '3', dy=-7), T_((5, 5), '2', dx=8, a='start'), T_((2.5, 6), '5', dy=-7)]
F_L1 = [('poly', [(0, 0), (8, 0), (8, 4), (0, 4)], 'q0'), ('poly', [(0, 4), (5, 4), (5, 6), (0, 6)], 'q1'), T_((4, 2), '8 · 4 = 32', cls='big'), T_((2.5, 5), '5 · 2 = 10')]
F_L2 = [('poly', [(0, 0), (8, 0), (8, 6), (0, 6)], 'q0'), ('poly', [(5, 4), (8, 4), (8, 6), (5, 6)], 'hole'), ('poly', [(5, 4), (8, 4), (8, 6), (5, 6)], 'frame'), T_((3, 2.5), '8 · 6 = 48', cls='big'), T_((6.5, 5), '3 · 2 = 6')]
F_FIN = [('poly', [(0, 0), (4, 0), (4, 3), (0, 3)], 'sh'), ('sect', (2, 3), 2, 0, 180, 'sh'), ('seg', (0, 3), (4, 3), 'd'), T_((2, 0), '4 m', dy=16), T_((4, 1.5), '3 m', dx=8, a='start')]
F_CAMI = [('poly', [(-1, -1), (13, -1), (13, 9), (-1, 9)], 'sh'), ('poly', [(0, 0), (12, 0), (12, 8), (0, 8)], 'lawn'), T_((6, 4), '12 m × 8 m'), T_((12.5, 4), '1 m', dx=6, a='start')]
s9 = box('prop', L('Com calculem l\'àrea d\'una figura composta', 'Cómo calculamos el área de una figura compuesta', 'How to find the area of a compound shape'),
  P(r"Una figura <strong>composta</strong> està formada per figures conegudes. Hi ha dues estratègies:",
    r"Una figura <strong>compuesta</strong> está formada por figuras conocidas. Hay dos estrategias:",
    r"A <strong>compound</strong> shape is made of shapes we know. There are two strategies:")
  + ul(L(r"<strong>Descompondre i sumar</strong>: la tallem en trossos coneguts i sumem les àrees.", r"<strong>Descomponer y sumar</strong>: la cortamos en trozos conocidos y sumamos las áreas.", r"<strong>Split and add</strong>: cut it into known pieces and add their areas."),
       L(r"<strong>Completar i restar</strong>: la completem fins a una figura coneguda i restem el que hem afegit (o els forats).", r"<strong>Completar y restar</strong>: la completamos hasta una figura conocida y restamos lo que hemos añadido (o los agujeros).", r"<strong>Complete and subtract</strong>: complete it to a known shape and subtract what you added (or the holes)."))
  + figs(G(F_L, W=170, pad=22, cap=L('La figura (en cm)', 'La figura (en cm)', 'The shape (in cm)')),
         G(F_L1, W=170, pad=22, cap=L(r'Sumant: \(32+10=42\ \text{cm}^2\)', r'Sumando: \(32+10=42\ \text{cm}^2\)', r'Adding: \(32+10=42\ \text{cm}^2\)')),
         G(F_L2, W=170, pad=22, cap=L(r'Restant: \(48-6=42\ \text{cm}^2\)', r'Restando: \(48-6=42\ \text{cm}^2\)', r'Subtracting: \(48-6=42\ \text{cm}^2\)')), three=True)
  + note(r"El <strong>perímetre</strong> és només el <strong>contorn exterior</strong>: les línies que hem dibuixat per dividir la figura no compten. En la figura en forma de L: \(P=8+4+3+2+5+6=28\ \text{cm}\).",
         r"El <strong>perímetro</strong> es solo el <strong>contorno exterior</strong>: las líneas que hemos dibujado para dividir la figura no cuentan. En la figura en forma de L: \(P=8+4+3+2+5+6=28\ \text{cm}\).",
         r"The <strong>perimeter</strong> is just the <strong>outer boundary</strong>: the lines we drew to split the shape don't count. For the L-shape: \(P=8+4+3+2+5+6=28\ \text{cm}\).", '⚠️')
  + widget('w-comp', '🧩', L('Figures compostes', 'Figuras compuestas', 'Compound shapes'),
           [seg([('L', L('En L', 'En L', 'L-shape')), ('casa', L('Casa', 'Casa', 'House')), ('fin', L('Finestra', 'Ventana', 'Window')), ('pista', L('Pista', 'Pista', 'Track')), ('forat', L('Forat', 'Agujero', 'Hole')), ('cami', L('Camí', 'Camino', 'Path'))]),
            '<div class="wrow">' + rng('a', 2, 14, 1, 8, 'a') + rng('b', 2, 12, 1, 6, 'b') + rng('c', 1, 6, 1, 2, 'c') + '</div>'],
           out='<div class="gout"></div>')
  + drill('comp', 'Entrena: figures compostes', 'Entrena: figuras compuestas', 'Train: compound shapes'))
ck(8 * 4 + 5 * 2, 42); ck(8 * 6 - 3 * 2, 42); ck(8 + 4 + 3 + 2 + 5 + 6, 28)
s9 += levels(
 [prob(L(r"La façana d'una caseta és un rectangle de 6 m × 4 m amb una teulada en forma de triangle de 6 m de base i 3 m d'altura. Calcula'n l'àrea.", r"La fachada de una caseta es un rectángulo de 6 m × 4 m con un tejado en forma de triángulo de 6 m de base y 3 m de altura. Calcula su área.", r"The front of a hut is a 6 m × 4 m rectangle with a triangular roof with a 6 m base and a 3 m height. Find its area."),
       figs(G([('poly', [(0, 0), (6, 0), (6, 4), (0, 4)], 'q0'), ('poly', [(0, 4), (6, 4), (3, 7)], 'q1'), ('seg', (3, 4), (3, 7), 'd'), T_((3, 0), '6', dy=16), T_((6, 2), '4', dx=8, a='start'), T_((3, 5.5), '3', dx=6, a='start')], W=130)),
       D(r"A=6\cdot4+\frac{6\cdot3}{2}=24+9=\boxed{33\ \text{m}^2}"))],
 [prob(L(r"Una finestra té forma de rectangle de 4 m × 3 m acabat per dalt amb un semicercle. Calcula'n l'àrea i el perímetre.", r"Una ventana tiene forma de rectángulo de 4 m × 3 m acabado por arriba con un semicírculo. Calcula su área y su perímetro.", r"A window is a 4 m × 3 m rectangle topped with a semicircle. Find its area and its perimeter."),
       figs(G(F_FIN, W=130)),
       P(r"El semicercle té 2 m de radi (la meitat de 4):", r"El semicírculo tiene 2 m de radio (la mitad de 4):", r"The semicircle has a 2 m radius (half of 4):"),
       D(r"A=4\cdot3+\frac{3{,}14\cdot2^2}{2}=12+6{,}28=\boxed{18{,}28\ \text{m}^2}"),
       P(r"El contorn té la base, els dos costats i la semicircumferència (el diàmetre de dalt no compta):", r"El contorno tiene la base, los dos lados y la semicircunferencia (el diámetro de arriba no cuenta):", r"The boundary has the base, the two sides and the half circle (the top diameter doesn't count):"),
       D(r"P=4+3+3+\frac{2\cdot3{,}14\cdot2}{2}=10+6{,}28=\boxed{16{,}28\ \text{m}}")),
  prob(L(r"Al voltant d'un jardí rectangular de 12 m × 8 m es fa un camí d'1 m d'amplària. Calcula l'àrea del camí.", r"Alrededor de un jardín rectangular de 12 m × 8 m se hace un camino de 1 m de anchura. Calcula el área del camino.", r"A path 1 m wide is built around a 12 m × 8 m rectangular garden. Find the area of the path."),
       figs(G(F_CAMI, W=180)),
       P(r"El rectangle exterior fa \((12+2)\times(8+2)\). Li restem el jardí:", r"El rectángulo exterior mide \((12+2)\times(8+2)\). Le restamos el jardín:", r"The outer rectangle is \((12+2)\times(8+2)\). Subtract the garden:"),
       D(r"A=14\cdot10-12\cdot8=140-96=\boxed{44\ \text{m}^2}"))],
 [prob(L(r"Una pista d'atletisme està formada per un rectangle de 100 m × 60 m i dos semicercles als extrems. Calcula'n l'àrea i la longitud d'una volta.", r"Una pista de atletismo está formada por un rectángulo de 100 m × 60 m y dos semicírculos en los extremos. Calcula su área y la longitud de una vuelta.", r"An athletics track is made of a 100 m × 60 m rectangle with two semicircles at the ends. Find its area and the length of one lap."),
       figs(G([('poly', [(0, 0), (10, 0), (10, 6), (0, 6)], 'sh'), ('sect', (10, 3), 3, -90, 90, 'sh'), ('sect', (0, 3), 3, 90, 270, 'sh'), ('seg', (0, 0), (0, 6), 'd'), ('seg', (10, 0), (10, 6), 'd'), T_((5, 0), '100 m', dy=16), T_((10, 3), '60 m', dx=-6, a='end')], W=220)),
       P(r"Els dos semicercles fan un cercle sencer de radi 30 m:", r"Los dos semicírculos forman un círculo entero de radio 30 m:", r"The two semicircles make a whole disc with a 30 m radius:"),
       D(r"A=100\cdot60+3{,}14\cdot30^2=6000+2826=\boxed{8826\ \text{m}^2}"),
       D(r"P=2\cdot100+2\cdot3{,}14\cdot30=200+188{,}4=\boxed{388{,}4\ \text{m}}")),
  prob(L(r"Calcula l'àrea de la zona ombrejada: un quadrat de 10 cm de costat amb un forat circular de 10 cm de diàmetre.", r"Calcula el área de la zona sombreada: un cuadrado de 10 cm de lado con un agujero circular de 10 cm de diámetro.", r"Find the shaded area: a square with 10 cm sides with a circular hole 10 cm across."),
       figs(G([('poly', [(0, 0), (10, 0), (10, 10), (0, 10)], 'sh'), ('circ', (5, 5), 5, 'hole'), ('circ', (5, 5), 5, 'gc'), ('dot', (5, 5)), T_((5, 0), '10', dy=16)], W=130)),
       D(r"A=10^2-3{,}14\cdot5^2=100-78{,}5=\boxed{21{,}5\ \text{cm}^2}"))])
ck(6 * 4 + R(6 * 3, 2), 33); ck(4 * 3 + p * 4 / 2, 18.28); ck(4 + 3 + 3 + p * 2, 16.28); ck(14 * 10 - 12 * 8, 44); ck(100 * 60 + p * 900, 8826); ck(p * 900, 2826); ck(200 + 2 * p * 30, 388.4); ck(100 - p * 25, 21.5)
s9 += practice([
  ('★', L(r"a) Calcula l'àrea i el perímetre d'una figura en forma de L feta amb un rectangle de 10 cm × 6 cm al qual s'ha llevat un quadrat de 3 cm de costat en una cantonada.", r"a) Calcula el área y el perímetro de una figura en forma de L hecha con un rectángulo de 10 cm × 6 cm al que se le ha quitado un cuadrado de 3 cm de lado en una esquina.", r"a) Find the area and perimeter of an L-shape made from a 10 cm × 6 cm rectangle with a 3 cm square cut from one corner.")),
  ('★★', L(r"b) Àrea d'un quadrat de 8 cm de costat amb un semicercle de 8 cm de diàmetre enganxat a un costat. c) Àrea d'un cercle de 6 cm de radi amb un forat quadrat de 4 cm de costat.", r"b) Área de un cuadrado de 8 cm de lado con un semicírculo de 8 cm de diámetro pegado a un lado. c) Área de un círculo de 6 cm de radio con un agujero cuadrado de 4 cm de lado.", r"b) Area of a square with 8 cm sides with a semicircle 8 cm across attached to one side. c) Area of a disc with a 6 cm radius with a square hole with 4 cm sides.")),
  ('★★★', L(r"d) Dins d'un rectangle de 20 m × 10 m es dibuixa un semicercle que té el diàmetre sobre el costat llarg i toca el costat de dalt. Quina àrea del rectangle queda fora del semicercle?", r"d) Dentro de un rectángulo de 20 m × 10 m se dibuja un semicírculo que tiene el diámetro sobre el lado largo y toca el lado de arriba. ¿Qué área del rectángulo queda fuera del semicírculo?", r"d) Inside a 20 m × 10 m rectangle we draw a semicircle with its diameter on the long side, touching the top side. What area of the rectangle is left outside the semicircle?"))],
  P(r"a) \(A=60-9=51\) cm², \(P=2\cdot10+2\cdot6=32\) cm (el mateix que el rectangle!). b) \(64+\tfrac{3{,}14\cdot16}{2}=64+25{,}12=89{,}12\) cm². c) \(113{,}04-16=97{,}04\) cm². d) Semicercle de radi 10 m: \(200-157=43\) m².",
    r"a) \(A=60-9=51\) cm², \(P=2\cdot10+2\cdot6=32\) cm (¡lo mismo que el rectángulo!). b) \(64+\tfrac{3{,}14\cdot16}{2}=64+25{,}12=89{,}12\) cm². c) \(113{,}04-16=97{,}04\) cm². d) Semicírculo de radio 10 m: \(200-157=43\) m².",
    r"a) \(A=60-9=51\) cm², \(P=2\cdot10+2\cdot6=32\) cm (the same as the rectangle!). b) \(64+\tfrac{3.14\cdot16}{2}=64+25.12=89.12\) cm². c) \(113.04-16=97.04\) cm². d) Semicircle with a 10 m radius: \(200-157=43\) m²."))
ck(60 - 9, 51); ck(2 * 10 + 2 * 6, 32); ck(64 + p * 16 / 2, 89.12); ck(p * 36 - 16, 97.04); ck(200 - p * 100 / 2, 43)
