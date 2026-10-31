# 9.5 Polígons regulars · 9.6 La circumferència: longitud i arcs
from comu import *

def T_(P, t, **o): return ('txt', P, t, o)
def regpts(n, r, rot=None):
    rot = -90 - 180 / n if rot is None else rot   # un costat horitzontal a baix
    return [(r * math.cos(math.radians(rot + 360 * k / n)), r * math.sin(math.radians(rot + 360 * k / n))) for k in range(n)]
def reg_fig(n, tris=False):
    V = regpts(n, 3); M = mid(V[0], V[1])
    it = [('poly', V, 'gf')]
    if tris:
        for k in range(n): it.append(('poly', [(0, 0), V[k], V[(k + 1) % n]], 'tr' if k == 0 else 'tl'))
    else:
        it += [('poly', [(0, 0), M, V[1]], 'tr'), ('seg', (0, 0), V[1], ''), ('seg', (0, 0), M, 'd'), ('ra', M, V[1], (0, 0)),
               T_(off((0, 0), V[1], -0.3), 'r', a='start'), T_(mid((0, 0), M), 'a', dx=-8, a='end'), T_(mid(M, V[1]), 'l/2', dy=15)]
    it += [('dot', (0, 0)), T_((0, 0), 'O', dy=-7, dx=-6)]
    if tris: it.append(T_(mid((0, 0), M), 'a', dx=-7, a='end')); it.append(('seg', (0, 0), M, 'd'))
    return it

# =====================================================================
# 9.5 Polígons regulars
# =====================================================================
s5 = box('def', L('Polígons regulars i els seus elements', 'Polígonos regulares y sus elementos', 'Regular polygons and their parts'),
  P(r"Un polígon és <strong>regular</strong> si té tots els costats i tots els angles iguals. A més dels costats (\(l\)) i els vèrtexs, té:",
    r"Un polígono es <strong>regular</strong> si tiene todos los lados y todos los ángulos iguales. Además de los lados (\(l\)) y los vértices, tiene:",
    r"A polygon is <strong>regular</strong> if all its sides and all its angles are equal. Besides its sides (\(l\)) and vertices, it has:")
  + ul(L(r"<strong>Centre</strong> \(O\): el punt que està a la mateixa distància de tots els vèrtexs.", r"<strong>Centro</strong> \(O\): el punto que está a la misma distancia de todos los vértices.", r"<strong>Centre</strong> \(O\): the point at the same distance from every vertex."),
       L(r"<strong>Radi</strong> \(r\): el segment que uneix el centre amb un vèrtex.", r"<strong>Radio</strong> \(r\): el segmento que une el centro con un vértice.", r"<strong>Radius</strong> \(r\): the segment joining the centre to a vertex."),
       L(r"<strong>Apotema</strong> \(a\): el segment que uneix el centre amb el punt mitjà d'un costat. És <strong>perpendicular</strong> al costat.", r"<strong>Apotema</strong> \(a\): el segmento que une el centro con el punto medio de un lado. Es <strong>perpendicular</strong> al lado.", r"<strong>Apothem</strong> \(a\): the segment joining the centre to the midpoint of a side. It is <strong>perpendicular</strong> to the side."))
  + P(r"El radi, l'apotema i mig costat formen un <strong>triangle rectangle</strong>, amb el radi com a hipotenusa:", r"El radio, la apotema y medio lado forman un <strong>triángulo rectángulo</strong>, con el radio como hipotenusa:", r"The radius, the apothem and half a side form a <strong>right triangle</strong>, with the radius as hypotenuse:")
  + D(r"r^2=a^2+\left(\frac l2\right)^2\qquad\Rightarrow\qquad a=\sqrt{r^2-\left(\frac l2\right)^2}")
  + figs(G(reg_fig(6), W=210, cap=L('Hexàgon regular', 'Hexágono regular', 'Regular hexagon')), G(reg_fig(5), W=200, cap=L('Pentàgon regular', 'Pentágono regular', 'Regular pentagon'))))
s5 += box('prop', L("Àrea d'un polígon regular", 'Área de un polígono regular', 'Area of a regular polygon'),
  P(r"Si unim el centre amb els vèrtexs, un polígon regular de \(n\) costats queda dividit en \(n\) triangles iguals, de base \(l\) i altura \(a\). Per tant:",
    r"Si unimos el centro con los vértices, un polígono regular de \(n\) lados queda dividido en \(n\) triángulos iguales, de base \(l\) y altura \(a\). Por tanto:",
    r"Joining the centre to the vertices splits a regular polygon with \(n\) sides into \(n\) equal triangles with base \(l\) and height \(a\). So:")
  + D(r"A=n\cdot\frac{l\cdot a}{2}=\frac{P\cdot a}{2}\qquad(P=n\cdot l\ \text{%s})" % Lt('és el perímetre', 'es el perímetro', 'is the perimeter'))
  + figs(G(reg_fig(5, True), W=200, cap=r'\(A=5\cdot\dfrac{l\cdot a}{2}\)'))
  + P(r"<strong>L'hexàgon regular</strong> és especial: els sis triangles són <strong>equilàters</strong>, de manera que el radi és igual al costat, \(r=l\). Si el costat és 10 cm:",
      r"<strong>El hexágono regular</strong> es especial: los seis triángulos son <strong>equiláteros</strong>, de modo que el radio es igual al lado, \(r=l\). Si el lado es 10 cm:",
      r"<strong>The regular hexagon</strong> is special: its six triangles are <strong>equilateral</strong>, so the radius equals the side, \(r=l\). If the side is 10 cm:")
  + D(r"a=\sqrt{10^2-5^2}=\sqrt{75}\approx8{,}66\ \text{cm}\qquad A=\frac{60\cdot8{,}66}{2}\approx259{,}8\ \text{cm}^2")
  + widget('w-reg', '⬡', L('Explora els polígons regulars', 'Explora los polígonos regulares', 'Explore regular polygons'),
           ['<div class="wrow">' + rng('n', 3, 10, 1, 6, 'n') + rng('l', 1, 12, 0.5, 4, 'l') + '</div>'], out='<div class="gout"></div>')
  + drill('reg', 'Entrena: polígons regulars', 'Entrena: polígonos regulares', 'Train: regular polygons'))
ck(leg(10, 5), 8.66, 2); ck(60 * R(866, 100) / 2, 259.8, 1); ck(60 * leg(10, 5) / 2, 259.8, 1)
s5 += levels(
 [prob(L(r"Un pentàgon regular té 8 cm de costat i 5,5 cm d'apotema. Calcula'n el perímetre i l'àrea.", r"Un pentágono regular tiene 8 cm de lado y 5,5 cm de apotema. Calcula su perímetro y su área.", r"A regular pentagon has 8 cm sides and a 5.5 cm apothem. Find its perimeter and its area."),
       D(r"P=5\cdot8=\boxed{40\ \text{cm}}\qquad A=\frac{40\cdot5{,}5}{2}=\boxed{110\ \text{cm}^2}"))],
 [prob(L(r"Calcula l'àrea d'un hexàgon regular de 10 cm de costat.", r"Calcula el área de un hexágono regular de 10 cm de lado.", r"Find the area of a regular hexagon with 10 cm sides."),
       P(r"En l'hexàgon, \(r=l=10\). L'apotema és un catet del triangle de hipotenusa 10 i l'altre catet 5:", r"En el hexágono, \(r=l=10\). La apotema es un cateto del triángulo de hipotenusa 10 y el otro cateto 5:", r"In a hexagon \(r=l=10\). The apothem is a leg of the triangle with hypotenuse 10 and other leg 5:"),
       D(r"a=\sqrt{10^2-5^2}=\sqrt{75}\approx8{,}66\qquad A=\frac{60\cdot\sqrt{75}}{2}\approx\boxed{259{,}81\ \text{cm}^2}")),
  prob(L(r"Un octàgon regular té 6 cm de costat i 7,84 cm de radi. Calcula'n l'apotema i l'àrea.", r"Un octógono regular tiene 6 cm de lado y 7,84 cm de radio. Calcula su apotema y su área.", r"A regular octagon has 6 cm sides and a 7.84 cm radius. Find its apothem and its area."),
       D(r"a=\sqrt{7{,}84^2-3^2}=\sqrt{52{,}4656}\approx\boxed{7{,}24\ \text{cm}}\qquad A=\frac{48\cdot7{,}24}{2}\approx\boxed{173{,}8\ \text{cm}^2}"))],
 [prob(L(r"Un quadrat està inscrit en una circumferència de 5 cm de radi (els vèrtexs estan sobre la circumferència). Calcula'n el costat, l'apotema i l'àrea.", r"Un cuadrado está inscrito en una circunferencia de 5 cm de radio (los vértices están sobre la circunferencia). Calcula su lado, su apotema y su área.", r"A square is inscribed in a circle with a 5 cm radius (its vertices lie on the circle). Find its side, apothem and area."),
       figs(G([('circ', (0, 0), 5, 'gc'), ('poly', [(5, 0), (0, 5), (-5, 0), (0, -5)], 'gf'), ('poly', [(-5, 0), (0, -5), (0, 5)], 'tr'), ('seg', (-5, 0), (5, 0), 'd'), ('ra', (0, -5), (-5, 0), (5, 0)),
                ('dot', (0, 0)), T_((2.5, 0), 'r = 5', dy=-6), T_(off((-5, 0), (0, -5), -0.9), 'l'), T_(off((0, -5), (5, 0), -0.9), 'l')], W=190)),
       P(r"La diagonal del quadrat és un diàmetre, \(d=10\). Amb Pitàgores, \(l^2+l^2=10^2\):", r"La diagonal del cuadrado es un diámetro, \(d=10\). Con Pitágoras, \(l^2+l^2=10^2\):", r"The square's diagonal is a diameter, \(d=10\). By Pythagoras, \(l^2+l^2=10^2\):"),
       D(r"2l^2=100\Rightarrow l=\sqrt{50}\approx\boxed{7{,}07\ \text{cm}}\qquad a=\frac l2\approx\boxed{3{,}54\ \text{cm}}\qquad A=l^2=\boxed{50\ \text{cm}^2}"))])
ck(5 * 8, 40); ck(40 * R(55, 10) / 2, 110); ck(60 * S(75) / 2, 259.81, 2); ck(leg(R(784, 100), 3), 7.24, 2); ck(48 * R(724, 100) / 2, 173.8, 1); ck(48 * leg(R(784, 100), 3) / 2, 173.8, 1)
ck(S(50), 7.07, 2); ck(S(50) / 2, 3.54, 2)
s5 += practice([
  ('★', L(r"a) Àrea d'un hexàgon regular de 36 cm de perímetre i 5,2 cm d'apotema. b) Perímetre d'un decàgon regular de 4,5 cm de costat.", r"a) Área de un hexágono regular de 36 cm de perímetro y 5,2 cm de apotema. b) Perímetro de un decágono regular de 4,5 cm de lado.", r"a) Area of a regular hexagon with a 36 cm perimeter and a 5.2 cm apothem. b) Perimeter of a regular decagon with 4.5 cm sides.")),
  ('★★', L(r"c) Un pentàgon regular té 10 cm de costat i 8,5 cm de radi. Calcula'n l'apotema i l'àrea.", r"c) Un pentágono regular tiene 10 cm de lado y 8,5 cm de radio. Calcula su apotema y su área.", r"c) A regular pentagon has 10 cm sides and an 8.5 cm radius. Find its apothem and its area.")),
  ('★★★', L(r"d) Un hexàgon regular té 6 cm d'apotema. Quant mesura el costat? I l'àrea?", r"d) Un hexágono regular tiene 6 cm de apotema. ¿Cuánto mide el lado? ¿Y el área?", r"d) A regular hexagon has a 6 cm apothem. How long is its side? What is its area?"))],
  P(r"a) \(\tfrac{36\cdot5{,}2}{2}=93{,}6\) cm². b) \(45\) cm. c) \(a=\sqrt{8{,}5^2-5^2}=\sqrt{47{,}25}\approx6{,}87\) cm; \(A\approx\tfrac{50\cdot6{,}87}{2}\approx171{,}8\) cm². d) \(l^2=6^2+\left(\tfrac l2\right)^2\Rightarrow\tfrac34l^2=36\Rightarrow l=\sqrt{48}\approx6{,}93\) cm; \(A\approx\tfrac{6\cdot6{,}93\cdot6}{2}\approx124{,}7\) cm².",
    r"a) \(\tfrac{36\cdot5{,}2}{2}=93{,}6\) cm². b) \(45\) cm. c) \(a=\sqrt{8{,}5^2-5^2}=\sqrt{47{,}25}\approx6{,}87\) cm; \(A\approx\tfrac{50\cdot6{,}87}{2}\approx171{,}8\) cm². d) \(l^2=6^2+\left(\tfrac l2\right)^2\Rightarrow\tfrac34l^2=36\Rightarrow l=\sqrt{48}\approx6{,}93\) cm; \(A\approx\tfrac{6\cdot6{,}93\cdot6}{2}\approx124{,}7\) cm².",
    r"a) \(\tfrac{36\cdot5.2}{2}=93.6\) cm². b) \(45\) cm. c) \(a=\sqrt{8.5^2-5^2}=\sqrt{47.25}\approx6.87\) cm; \(A\approx\tfrac{50\cdot6.87}{2}\approx171.8\) cm². d) \(l^2=6^2+\left(\tfrac l2\right)^2\Rightarrow\tfrac34l^2=36\Rightarrow l=\sqrt{48}\approx6.93\) cm; \(A\approx\tfrac{6\cdot6.93\cdot6}{2}\approx124.7\) cm²."))
ck(36 * R(52, 10) / 2, 93.6); ck(10 * R(45, 10), 45); ck(leg(R(85, 10), 5), 6.87, 2); ck(50 * leg(R(85, 10), 5) / 2, 171.8, 1); ck(S(48), 6.93, 2); ck(6 * S(48) * 6 / 2, 124.7, 1); ck(6 * R(693, 100) * 3, 124.7, 1)

# =====================================================================
# 9.6 La circumferència: longitud i arcs
# =====================================================================
CIRC = G([('circ', (0, 0), 3, 'gc'), ('arc', (0, 0), 3, 20, 75, 'hl'), ('seg', (0, 0), (3 * math.cos(math.radians(-35)), 3 * math.sin(math.radians(-35))), ''),
          ('seg', (-3, 0), (3, 0), 'd'), ('seg', (3 * math.cos(math.radians(20)), 3 * math.sin(math.radians(20))), (3 * math.cos(math.radians(75)), 3 * math.sin(math.radians(75))), 'ch'), ('dot', (0, 0)),
          T_((0, 0), 'O', dy=16), T_((1.3, -1.1), 'r', dx=6), T_((-1.5, 0), 'd', dy=-6), T_((3.2 * math.cos(math.radians(50)), 3.2 * math.sin(math.radians(50))), Ls('arc', 'arco', 'arc'), a='start', dx=4),
          T_((2.1, 1.75), Ls('corda', 'cuerda', 'chord'), dy=12, dx=-14)], W=200)
s6 = box('def', L('Circumferència i cercle', 'Circunferencia y círculo', 'Circle and disc'),
  ul(L(r"La <strong>circumferència</strong> és la línia formada per tots els punts que estan a la mateixa distància, el <strong>radi</strong> \(r\), d'un punt anomenat <strong>centre</strong>.", r"La <strong>circunferencia</strong> es la línea formada por todos los puntos que están a la misma distancia, el <strong>radio</strong> \(r\), de un punto llamado <strong>centro</strong>.", r"A <strong>circle</strong> (the curve) is the line made of all the points at the same distance, the <strong>radius</strong> \(r\), from a point called the <strong>centre</strong>."),
     L(r"El <strong>cercle</strong> és la superfície que tanca la circumferència.", r"El <strong>círculo</strong> es la superficie que encierra la circunferencia.", r"The <strong>disc</strong> is the surface the circle encloses."),
     L(r"Una <strong>corda</strong> uneix dos punts de la circumferència; la més llarga, que passa pel centre, és el <strong>diàmetre</strong>: \(d=2r\). Un <strong>arc</strong> és un tros de circumferència.", r"Una <strong>cuerda</strong> une dos puntos de la circunferencia; la más larga, que pasa por el centro, es el <strong>diámetro</strong>: \(d=2r\). Un <strong>arco</strong> es un trozo de circunferencia.", r"A <strong>chord</strong> joins two points on the circle; the longest, through the centre, is the <strong>diameter</strong>: \(d=2r\). An <strong>arc</strong> is a piece of the circle."))
  + figs(CIRC))
s6 += box('prop', L('Longitud de la circumferència', 'Longitud de la circunferencia', 'Circumference'),
  P(r"En qualsevol circumferència, si dividim la longitud entre el diàmetre obtenim sempre el mateix nombre, \(\pi=3{,}14159\ldots\) (un nombre irracional: té infinites xifres decimals no periòdiques). Per tant:",
    r"En cualquier circunferencia, si dividimos la longitud entre el diámetro obtenemos siempre el mismo número, \(\pi=3{,}14159\ldots\) (un número irracional: tiene infinitas cifras decimales no periódicas). Por tanto:",
    r"In every circle, dividing the circumference by the diameter always gives the same number, \(\pi=3.14159\ldots\) (an irrational number: its decimals go on forever without repeating). So:")
  + D(r"L=2\pi r=\pi d")
  + P(r"Un <strong>arc</strong> de \(n^\circ\) és la fracció \(\frac{n}{360}\) de la circumferència sencera:", r"Un <strong>arco</strong> de \(n^\circ\) es la fracción \(\frac{n}{360}\) de la circunferencia entera:", r"An <strong>arc</strong> of \(n^\circ\) is the fraction \(\frac{n}{360}\) of the whole circle:")
  + D(r"L_{\text{arc}}=\frac{2\pi r\cdot n}{360}\qquad\quad r=9,\ n=120^\circ:\ \ L_{\text{arc}}=\frac{2\pi\cdot9\cdot120}{360}=6\pi\approx18{,}85")
  + note(r"Fes servir la tecla \(\pi\) de la calculadora i arrodoneix només el resultat final. Si uses \(\pi\approx3{,}14\), el resultat varia una mica.", r"Usa la tecla \(\pi\) de la calculadora y redondea solo el resultado final. Si usas \(\pi\approx3{,}14\), el resultado varía un poco.", r"Use the \(\pi\) key on your calculator and round only the final answer. With \(\pi\approx3.14\) the result changes slightly.", '🧮')
  + widget('w-circ', '⭕', L('Longitud de la circumferència i dels arcs', 'Longitud de la circunferencia y de los arcos', 'Circumference and arc length'),
           ['<div class="wrow">' + rng('r', 0.5, 10, 0.5, 3, 'r') + rng('n', 0, 360, 5, 120, 'n') + '</div>'], out='<div class="gout"></div>')
  + drill('circ', 'Entrena: longituds i arcs', 'Entrena: longitudes y arcos', 'Train: circumferences and arcs'))
ck(2 * pi * 9 * 120 / 360, 18.85, 2)
s6 += levels(
 [prob(L(r"Calcula la longitud d'una circumferència de 4,5 cm de radi.", r"Calcula la longitud de una circunferencia de 4,5 cm de radio.", r"Find the circumference of a circle with a 4.5 cm radius."),
       D(r"L=2\pi\cdot4{,}5=9\pi\approx\boxed{28{,}27\ \text{cm}}")),
  prob(L(r"La roda d'una bicicleta fa 70 cm de diàmetre. Quina distància recorre en cada volta? Quantes voltes completes fa en 1 km?", r"La rueda de una bicicleta mide 70 cm de diámetro. ¿Qué distancia recorre en cada vuelta? ¿Cuántas vueltas completas da en 1 km?", r"A bike wheel is 70 cm across. How far does it travel in one turn? How many full turns does it make in 1 km?"),
       D(r"L=\pi\cdot70\approx\boxed{219{,}91\ \text{cm}}"), D(r"1\ \text{km}=100\,000\ \text{cm}\qquad \frac{100\,000}{219{,}91}\approx454{,}7\ \Rightarrow\ \boxed{454\ \text{%s}}" % Lt('voltes completes', 'vueltas completas', 'full turns')))],
 [prob(L(r"Calcula la longitud d'un arc de 120° en una circumferència de 9 cm de radi.", r"Calcula la longitud de un arco de 120° en una circunferencia de 9 cm de radio.", r"Find the length of a 120° arc in a circle with a 9 cm radius."),
       D(r"L_{\text{arc}}=\frac{2\pi\cdot9\cdot120}{360}=6\pi\approx\boxed{18{,}85\ \text{cm}}"))],
 [prob(L(r"En una circumferència de 6 cm de radi, un arc mesura 15,71 cm. Quants graus té?", r"En una circunferencia de 6 cm de radio, un arco mide 15,71 cm. ¿Cuántos grados tiene?", r"In a circle with a 6 cm radius, an arc is 15.71 cm long. How many degrees does it measure?"),
       D(r"\frac{2\pi\cdot6\cdot n}{360}=15{,}71\ \Rightarrow\ n=\frac{15{,}71\cdot360}{12\pi}\approx\boxed{150^\circ}")),
  prob(L(r"Calcula el perímetre d'un semicercle de 5 cm de radi (l'arc més el diàmetre).", r"Calcula el perímetro de un semicírculo de 5 cm de radio (el arco más el diámetro).", r"Find the perimeter of a semicircle with a 5 cm radius (the arc plus the diameter)."),
       figs(G([('sect', (0, 0), 5, 0, 180, 'gf'), T_((0, 0), '10 cm', dy=15), ('dot', (0, 0))], W=180)),
       D(r"P=\frac{2\pi\cdot5}{2}+10=5\pi+10\approx\boxed{25{,}71\ \text{cm}}"))])
ck(9 * pi, 28.27, 2); ck(70 * pi, 219.91, 2); ck(100000 / (70 * pi), 454.7, 1); assert math.floor(100000 / (70 * math.pi)) == 454
ck(R(1571, 100) * 360 / (12 * pi), 150, 0); ck(5 * pi + 10, 25.71, 2)
s6 += practice([
  ('★', L(r"a) Longitud d'una circumferència de 12 cm de diàmetre. b) Radi d'una circumferència que fa 31,4 cm de longitud.", r"a) Longitud de una circunferencia de 12 cm de diámetro. b) Radio de una circunferencia que mide 31,4 cm de longitud.", r"a) Circumference of a circle 12 cm across. b) Radius of a circle whose circumference is 31.4 cm.")),
  ('★★', L(r"c) Longitud d'un arc de 45° en una circumferència de 8 cm de radi. d) El radi de la Terra és d'uns 6 371 km. Quant mesura l'equador?", r"c) Longitud de un arco de 45° en una circunferencia de 8 cm de radio. d) El radio de la Tierra es de unos 6 371 km. ¿Cuánto mide el ecuador?", r"c) Length of a 45° arc in a circle with an 8 cm radius. d) The Earth's radius is about 6,371 km. How long is the equator?")),
  ('★★★', L(r"e) Quants graus té un arc de 10 cm en una circumferència de 10 cm de radi?", r"e) ¿Cuántos grados tiene un arco de 10 cm en una circunferencia de 10 cm de radio?", r"e) How many degrees is a 10 cm arc in a circle with a 10 cm radius?"))],
  P(r"a) \(12\pi\approx37{,}70\) cm. b) \(r=\tfrac{31{,}4}{2\pi}\approx5\) cm. c) \(\tfrac{2\pi\cdot8\cdot45}{360}=2\pi\approx6{,}28\) cm. d) \(2\pi\cdot6371\approx40\,030\) km. e) \(n=\tfrac{10\cdot360}{20\pi}\approx57{,}30^\circ\).",
    r"a) \(12\pi\approx37{,}70\) cm. b) \(r=\tfrac{31{,}4}{2\pi}\approx5\) cm. c) \(\tfrac{2\pi\cdot8\cdot45}{360}=2\pi\approx6{,}28\) cm. d) \(2\pi\cdot6371\approx40\,030\) km. e) \(n=\tfrac{10\cdot360}{20\pi}\approx57{,}30^\circ\).",
    r"a) \(12\pi\approx37.70\) cm. b) \(r=\tfrac{31.4}{2\pi}\approx5\) cm. c) \(\tfrac{2\pi\cdot8\cdot45}{360}=2\pi\approx6.28\) cm. d) \(2\pi\cdot6371\approx40{,}030\) km. e) \(n=\tfrac{10\cdot360}{20\pi}\approx57.30^\circ\)."))
ck(12 * pi, 37.70, 2); ck(R(314, 10) / (2 * pi), 5, 0); ck(2 * pi * 8 * 45 / 360, 6.28, 2); ck(2 * pi * 6371, 40030, -1); ck(3600 / (20 * pi), 57.30, 2)
