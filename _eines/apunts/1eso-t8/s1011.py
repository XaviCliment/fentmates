# Apartats 8.10-8.11 dels apunts de la Unitat 8 de 1r ESO: el teorema de Pitàgores (primera vegada que es veu) i
# les seues aplicacions per a calcular mesures desconegudes en àrees i perímetres. Les arrels no exactes
# s'arrodoneixen a les centèsimes; π ≈ 3,14 (PI3).
from comu import *

def T_(P, t, **o): return ('txt', P, t, o)
p = PI3
def hyp(a, b): return S(sp.nsimplify(a) ** 2 + sp.nsimplify(b) ** 2)
def leg(c, b): return S(sp.nsimplify(c) ** 2 - sp.nsimplify(b) ** 2)
def tri_sq(a, b, grid=False):
    """triangle rectangle de catets a (horitzontal) i b (vertical) amb els quadrats dels tres costats; amb grid,
    cada quadrat queda quadriculat en quadrets d'una unitat (també el de la hipotenusa, si c és enter)"""
    C0, A, B = (0, 0), (a, 0), (0, b)
    A2, B2 = (a + b, a), (b, a + b)
    it = [('poly', [(0, 0), (a, 0), (a, -a), (0, -a)], 'q0'), ('poly', [(0, 0), (0, b), (-b, b), (-b, 0)], 'q1'), ('poly', [A, B, B2, A2], 'q2')]
    if grid:
        for i in range(1, a): it += [('seg', (i, 0), (i, -a), 'gl'), ('seg', (0, -i), (a, -i), 'gl')]
        for i in range(1, b): it += [('seg', (0, i), (-b, i), 'gl'), ('seg', (-i, 0), (-i, b), 'gl')]
        c = math.hypot(a, b)
        if abs(c - round(c)) < 1e-9:
            c = round(c)
            for k in range(1, c):
                f = k / c
                it += [('seg', mid(A, B, f), mid(A2, B2, f), 'gl'), ('seg', mid(A, A2, f), mid(B, B2, f), 'gl')]
    it += [('poly', [C0, A, B], 'tr'), ('ra', C0, A, B),
           T_((a / 2, -a / 2), f'{a * a}', cls='big'), T_((-b / 2, b / 2), f'{b * b}', cls='big'), T_(((a + b) / 2, (a + b) / 2), f'{a * a + b * b}', cls='big'),
           T_((a / 2, 0), 'a', dy=-6), T_((0, b / 2), 'b', dx=8, a='start'), T_(off(A, B, 0.16 * min(a, b)), 'c', cls='hy')]
    return it
def rtri(a, b, la='a', lb='b', lc='c', hot=None):
    """triangle rectangle amb noms o mesures als costats; hot = costat que busquem"""
    return [('poly', [(0, 0), (a, 0), (0, b)], 'tr'), ('ra', (0, 0), (a, 0), (0, b)),
            T_((a / 2, 0), la, dy=16, cls='hot' if hot == 'a' else ''), T_((0, b / 2), lb, dx=-8, a='end', cls='hot' if hot == 'b' else ''),
            T_(off((a, 0), (0, b), -0.07 * (a + b)), lc, a='start', cls='hot' if hot == 'c' else 'hy')]

# =====================================================================
# 8.10 El teorema de Pitàgores
# =====================================================================
s10 = box('def', L('El triangle rectangle: catets i hipotenusa', 'El triángulo rectángulo: catetos e hipotenusa', 'The right triangle: legs and hypotenuse'),
  P(r"Un <strong>triangle rectangle</strong> té un angle recte (de \(90^\circ\)). Els seus costats tenen nom propi:",
    r"Un <strong>triángulo rectángulo</strong> tiene un ángulo recto (de \(90^\circ\)). Sus lados tienen nombre propio:",
    r"A <strong>right triangle</strong> has a right angle (\(90^\circ\)). Its sides have their own names:")
  + ul(L(r"Els <strong>catets</strong> (\(a\) i \(b\)) són els dos costats que formen l'angle recte.", r"Los <strong>catetos</strong> (\(a\) y \(b\)) son los dos lados que forman el ángulo recto.", r"The <strong>legs</strong> (\(a\) and \(b\)) are the two sides that form the right angle."),
       L(r"La <strong>hipotenusa</strong> (\(c\)) és el costat oposat a l'angle recte. És sempre el <strong>costat més llarg</strong>.", r"La <strong>hipotenusa</strong> (\(c\)) es el lado opuesto al ángulo recto. Es siempre el <strong>lado más largo</strong>.", r"The <strong>hypotenuse</strong> (\(c\)) is the side opposite the right angle. It's always the <strong>longest side</strong>."))
  + figs(G(rtri(4, 3, Ls('catet a', 'cateto a', 'leg a'), Ls('catet b', 'cateto b', 'leg b'), Ls('hipotenusa c', 'hipotenusa c', 'hypotenuse c')), W=260, pad=70))
  + note(r"Per a trobar la hipotenusa, busca l'angle recte (el quadradet): la hipotenusa és el costat que <strong>no toca</strong> l'angle recte.",
         r"Para encontrar la hipotenusa, busca el ángulo recto (el cuadradito): la hipotenusa es el lado que <strong>no toca</strong> el ángulo recto.",
         r"To find the hypotenuse, look for the right angle (the little square): the hypotenuse is the side that <strong>doesn't touch</strong> the right angle.", '🔎'))
s10 += box('prop', L('El teorema de Pitàgores', 'El teorema de Pitágoras', "Pythagoras' theorem"),
  P(r"En tot triangle rectangle, el <strong>quadrat de la hipotenusa</strong> és igual a la <strong>suma dels quadrats dels catets</strong>:",
    r"En todo triángulo rectángulo, el <strong>cuadrado de la hipotenusa</strong> es igual a la <strong>suma de los cuadrados de los catetos</strong>:",
    r"In every right triangle, the <strong>square of the hypotenuse</strong> equals the <strong>sum of the squares of the legs</strong>:")
  + D(r"\boxed{\ c^2=a^2+b^2\ }")
  + P(r"Té un significat amb <strong>àrees</strong>: si dibuixem un quadrat sobre cada costat, el quadrat de la hipotenusa té tanta àrea com els dos quadrats dels catets junts. Compta els quadrets: \(9+16=25\).",
      r"Tiene un significado con <strong>áreas</strong>: si dibujamos un cuadrado sobre cada lado, el cuadrado de la hipotenusa tiene tanta área como los dos cuadrados de los catetos juntos. Cuenta los cuadraditos: \(9+16=25\).",
      r"It has a meaning in terms of <strong>area</strong>: if we draw a square on each side, the square on the hypotenuse has as much area as the two squares on the legs together. Count the little squares: \(9+16=25\).")
  + figs(G(tri_sq(3, 4, grid=True), W=250, cap=r'\(3^2+4^2=5^2\qquad 9+16=25\)'))
  + note(r"El teorema <strong>només</strong> és vàlid per als triangles rectangles. Porta el nom de Pitàgores, un matemàtic grec del segle VI aC, però babilonis, egipcis, indis i xinesos ja el feien servir molt abans.",
         r"El teorema <strong>solo</strong> es válido para los triángulos rectángulos. Lleva el nombre de Pitágoras, un matemático griego del siglo VI a. C., pero babilonios, egipcios, indios y chinos ya lo usaban mucho antes.",
         r"The theorem <strong>only</strong> works for right triangles. It's named after Pythagoras, a Greek mathematician of the 6th century BC, but the Babylonians, Egyptians, Indians and Chinese were using it long before.", '📜')
  + widget('w-pit', '📐', L('Els quadrats sobre els costats', 'Los cuadrados sobre los lados', 'Squares on the sides'),
           ['<div class="wrow">' + rng('a', 1, 8, 1, 3, 'a') + rng('b', 1, 8, 1, 4, 'b') + '</div>',
            quick([('3|4', '3, 4'), ('6|8', '6, 8'), ('5|5', '5, 5'), ('1|7', '1, 7'), ('2|3', '2, 3')])]))
s10 += box('prop', L('Per què és cert? Una demostració amb peces', '¿Por qué es cierto? Una demostración con piezas', 'Why is it true? A proof with pieces'),
  P(r"Agafem un quadrat de costat \(a+b\) i hi posem dins quatre còpies del triangle rectangle de dues maneres. En la primera, el tros que queda lliure és un quadrat de costat \(c\): té àrea \(c^2\). En la segona, queden lliures dos quadrats, de costats \(a\) i \(b\): tenen àrea \(a^2+b^2\).",
    r"Tomamos un cuadrado de lado \(a+b\) y colocamos dentro cuatro copias del triángulo rectángulo de dos maneras. En la primera, el trozo que queda libre es un cuadrado de lado \(c\): tiene área \(c^2\). En la segunda, quedan libres dos cuadrados, de lados \(a\) y \(b\): tienen área \(a^2+b^2\).",
    r"Take a square of side \(a+b\) and place four copies of the right triangle inside it in two ways. In the first, the free part is a square of side \(c\): its area is \(c^2\). In the second, two squares are left free, with sides \(a\) and \(b\): their area is \(a^2+b^2\).")
  + P(r"El quadrat gran és el mateix i els quatre triangles també. Per tant, el que queda lliure té la mateixa àrea: \(c^2=a^2+b^2\).",
      r"El cuadrado grande es el mismo y los cuatro triángulos también. Por tanto, lo que queda libre tiene la misma área: \(c^2=a^2+b^2\).",
      r"The big square is the same and so are the four triangles. So whatever is left free has the same area: \(c^2=a^2+b^2\).")
  + widget('w-proof', '🧩', L('Recol·loca els quatre triangles', 'Recoloca los cuatro triángulos', 'Rearrange the four triangles'),
           [seg([('0', L('Manera 1: queda c²', 'Manera 1: queda c²', 'Layout 1: c² is left')), ('1', L('Manera 2: queden a² i b²', 'Manera 2: quedan a² y b²', 'Layout 2: a² and b² are left'))]),
            '<div class="wrow">' + rng('a', 1, 6, 0.5, 2, 'a') + rng('b', 1, 6, 0.5, 4, 'b') + '</div>']))
s10 += box('prop', L("Calcular un costat d'un triangle rectangle", 'Calcular un lado de un triángulo rectángulo', 'Finding a side of a right triangle'),
  P(r"Si coneixem dos costats d'un triangle rectangle, el teorema ens dona el tercer. Al final hem de fer una <strong>arrel quadrada</strong>, perquè l'arrel desfà el quadrat (ho vam veure a la Unitat 1).",
    r"Si conocemos dos lados de un triángulo rectángulo, el teorema nos da el tercero. Al final tenemos que hacer una <strong>raíz cuadrada</strong>, porque la raíz deshace el cuadrado (lo vimos en la Unidad 1).",
    r"If we know two sides of a right triangle, the theorem gives us the third. At the end we take a <strong>square root</strong>, because the root undoes the square (we saw this in Unit 1).")
  + ul(L(r"<strong>Hipotenusa</strong>: <strong>sumem</strong> els quadrats dels catets i fem l'arrel.", r"<strong>Hipotenusa</strong>: <strong>sumamos</strong> los cuadrados de los catetos y hacemos la raíz.", r"<strong>Hypotenuse</strong>: <strong>add</strong> the squares of the legs and take the root."),
       L(r"<strong>Catet</strong>: al quadrat de la hipotenusa li <strong>restem</strong> el quadrat de l'altre catet i fem l'arrel.", r"<strong>Cateto</strong>: al cuadrado de la hipotenusa le <strong>restamos</strong> el cuadrado del otro cateto y hacemos la raíz.", r"<strong>Leg</strong>: <strong>subtract</strong> the square of the other leg from the square of the hypotenuse and take the root."))
  + D(r"c=\sqrt{a^2+b^2}\qquad\qquad a=\sqrt{c^2-b^2}\qquad\qquad b=\sqrt{c^2-a^2}")
  + D(r"a=6,\ b=8:\quad c=\sqrt{6^2+8^2}=\sqrt{36+64}=\sqrt{100}=10")
  + D(r"c=13,\ b=5:\quad a=\sqrt{13^2-5^2}=\sqrt{169-25}=\sqrt{144}=12")
  + P(r"Va bé tindre a mà els quadrats dels primers nombres, per a reconéixer les arrels exactes:", r"Va bien tener a mano los cuadrados de los primeros números, para reconocer las raíces exactas:", r"It helps to know the first squares by heart, to spot exact roots:")
  + tbl([r'\(n\)'] + [str(k) for k in range(1, 16)], [[r'\(n^2\)'] + [str(k * k) for k in range(1, 16)]], 'sq')
  + note(r"Si l'arrel no és exacta, la calculem amb la tecla \(\sqrt{\ }\) de la calculadora i <strong>arrodonim a les centèsimes</strong>: \(\sqrt{74}=8{,}602\ldots\approx8{,}60\). I, abans de restar, comprova que la hipotenusa és el costat més llarg!",
         r"Si la raíz no es exacta, la calculamos con la tecla \(\sqrt{\ }\) de la calculadora y <strong>redondeamos a las centésimas</strong>: \(\sqrt{74}=8{,}602\ldots\approx8{,}60\). Y, antes de restar, ¡comprueba que la hipotenusa es el lado más largo!",
         r"If the root isn't exact, use the \(\sqrt{\ }\) key on your calculator and <strong>round to hundredths</strong>: \(\sqrt{74}=8.602\ldots\approx8.60\). And before subtracting, check that the hypotenuse is the longest side!", '🧮')
  + widget('w-pcalc', '🧮', L('Calculadora de Pitàgores', 'Calculadora de Pitágoras', 'Pythagoras calculator'),
           ['<div class="wrow">' + tin('a', L('catet a =', 'cateto a =', 'leg a ='), '6') + tin('b', L('catet b =', 'cateto b =', 'leg b ='), '8') + tin('c', L('hipotenusa c =', 'hipotenusa c =', 'hypotenuse c ='), '') + '</div>',
            '<p class="hint-s">' + L("Deixa en blanc el costat que vols calcular.", "Deja en blanco el lado que quieres calcular.", "Leave blank the side you want to find.") + '</p>',
            quick([('6|8|', 'a = 6, b = 8'), ('|5|13', 'b = 5, c = 13'), ('9|12|', 'a = 9, b = 12'), ('5|7|', 'a = 5, b = 7'), ('|2|6', 'b = 2, c = 6')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('hip', 'Entrena: calcula la hipotenusa', 'Entrena: calcula la hipotenusa', 'Train: find the hypotenuse')
  + drill('cat', 'Entrena: calcula un catet', 'Entrena: calcula un cateto', 'Train: find a leg'))
ck(hyp(6, 8), 10); ck(leg(13, 5), 12); ck(hyp(5, 7), 8.60, 2); ck(S(74), 8.602, 3)
s10 += box('prop', L('És rectangle aquest triangle?', '¿Es rectángulo este triángulo?', 'Is this a right triangle?'),
  P(r"El teorema també funciona al revés: si el quadrat del costat més llarg és igual a la suma dels quadrats dels altres dos, el triangle <strong>és rectangle</strong>. Si no hi són iguals, <strong>no ho és</strong>.",
    r"El teorema también funciona al revés: si el cuadrado del lado más largo es igual a la suma de los cuadrados de los otros dos, el triángulo <strong>es rectángulo</strong>. Si no son iguales, <strong>no lo es</strong>.",
    r"The theorem also works backwards: if the square of the longest side equals the sum of the squares of the other two, the triangle <strong>is a right triangle</strong>. If they're not equal, <strong>it isn't</strong>.")
  + D(r"5,\,12,\,13:\quad 13^2=169,\quad 5^2+12^2=25+144=169\ \ \Rightarrow\ \ " + Lt('rectangle', 'rectángulo', 'right') + r"")
  + D(r"4,\,5,\,7:\quad 7^2=49,\quad 4^2+5^2=16+25=41\ \ \Rightarrow\ \ " + Lt('no és rectangle', 'no es rectángulo', 'not right') + r"")
  + P(r"Tres nombres naturals que compleixen \(a^2+b^2=c^2\) formen una <strong>terna pitagòrica</strong>: \((3,\,4,\,5)\), \((5,\,12,\,13)\), \((8,\,15,\,17)\), \((7,\,24,\,25)\)… Si multipliquem una terna per un nombre, n'obtenim una altra: \((6,\,8,\,10)\), \((9,\,12,\,15)\)…",
      r"Tres números naturales que cumplen \(a^2+b^2=c^2\) forman una <strong>terna pitagórica</strong>: \((3,\,4,\,5)\), \((5,\,12,\,13)\), \((8,\,15,\,17)\), \((7,\,24,\,25)\)… Si multiplicamos una terna por un número, obtenemos otra: \((6,\,8,\,10)\), \((9,\,12,\,15)\)…",
      r"Three whole numbers with \(a^2+b^2=c^2\) form a <strong>Pythagorean triple</strong>: \((3,\,4,\,5)\), \((5,\,12,\,13)\), \((8,\,15,\,17)\), \((7,\,24,\,25)\)… Multiplying a triple by a number gives another one: \((6,\,8,\,10)\), \((9,\,12,\,15)\)…")
  + note(r"Els antics egipcis feien angles rectes amb una corda de 12 nucs igual de separats: si la tensaven formant un triangle de costats 3, 4 i 5, l'angle entre els costats 3 i 4 era recte.",
         r"Los antiguos egipcios trazaban ángulos rectos con una cuerda de 12 nudos igual de separados: si la tensaban formando un triángulo de lados 3, 4 y 5, el ángulo entre los lados 3 y 4 era recto.",
         r"The ancient Egyptians made right angles with a rope with 12 equally spaced knots: stretched into a triangle with sides 3, 4 and 5, the angle between the sides 3 and 4 was a right angle.", '🏺')
  + widget('w-esrect', '✅', L('És rectangle?', '¿Es rectángulo?', 'Is it a right triangle?'),
           ['<div class="wrow">' + tin('a', L('costat 1 =', 'lado 1 =', 'side 1 ='), '5') + tin('b', L('costat 2 =', 'lado 2 =', 'side 2 ='), '12') + tin('c', L('costat 3 =', 'lado 3 =', 'side 3 ='), '13') + '</div>',
            quick([('5|12|13', '5, 12, 13'), ('4|5|7', '4, 5, 7'), ('6|8|10', '6, 8, 10'), ('8|15|17', '8, 15, 17'), ('5|6|8', '5, 6, 8'), ('2|3|4', '2, 3, 4')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('esrect', 'Entrena: és rectangle o no?', 'Entrena: ¿es rectángulo o no?', 'Train: right triangle or not?', mode='opts'))
for t in [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15)]: assert t[0] ** 2 + t[1] ** 2 == t[2] ** 2
ck(4 ** 2 + 5 ** 2, 41); assert 41 != 49
s10 += levels(
 [prob(L(r"Els catets d'un triangle rectangle fan 9 cm i 12 cm. Quant fa la hipotenusa?", r"Los catetos de un triángulo rectángulo miden 9 cm y 12 cm. ¿Cuánto mide la hipotenusa?", r"The legs of a right triangle are 9 cm and 12 cm. How long is the hypotenuse?"),
       figs(G(rtri(4, 3, '12', '9', 'c = ?', 'c'), W=170, pad=40)),
       D(r"c^2=9^2+12^2=81+144=225"), D(r"c=\sqrt{225}=\boxed{15\ \text{cm}}")),
  prob(L(r"La hipotenusa d'un triangle rectangle fa 10 m i un catet fa 6 m. Quant fa l'altre catet?", r"La hipotenusa de un triángulo rectángulo mide 10 m y un cateto mide 6 m. ¿Cuánto mide el otro cateto?", r"The hypotenuse of a right triangle is 10 m and one leg is 6 m. How long is the other leg?"),
       P(r"Busquem un catet: restem.", r"Buscamos un cateto: restamos.", r"We want a leg: subtract."),
       D(r"b^2=10^2-6^2=100-36=64"), D(r"b=\sqrt{64}=\boxed{8\ \text{m}}"))],
 [prob(L(r"Una escala de 2,5 m està recolzada en una paret. El peu de l'escala està a 0,7 m de la paret. A quina altura arriba l'escala?", r"Una escalera de 2,5 m está apoyada en una pared. El pie de la escalera está a 0,7 m de la pared. ¿A qué altura llega la escalera?", r"A 2.5 m ladder leans against a wall. Its foot is 0.7 m from the wall. How high up the wall does it reach?"),
       figs(G([('seg', (0, 0), (0, 2.6), ''), ('seg', (-0.3, 0), (1.1, 0), ''), ('poly', [(0, 0), (0.7, 0), (0, 2.4)], 'tr'), ('ra', (0, 0), (0.7, 0), (0, 2.4)),
               T_((0.35, 0), '0,7', dy=16), T_((0, 1.2), 'h = ?', dx=-8, a='end', cls='hot'), T_(off((0.7, 0), (0, 2.4), -0.15), '2,5', a='start')], W=120, pad=30)),
       P(r"L'escala és la hipotenusa (està enfront de l'angle recte entre la paret i el terra):", r"La escalera es la hipotenusa (está enfrente del ángulo recto entre la pared y el suelo):", r"The ladder is the hypotenuse (it's opposite the right angle between the wall and the floor):"),
       D(r"h^2=2{,}5^2-0{,}7^2=6{,}25-0{,}49=5{,}76"), D(r"h=\sqrt{5{,}76}=\boxed{2{,}4\ \text{m}}")),
  prob(L(r"Els catets d'un triangle rectangle fan 5 cm i 7 cm. Calcula la hipotenusa.", r"Los catetos de un triángulo rectángulo miden 5 cm y 7 cm. Calcula la hipotenusa.", r"The legs of a right triangle are 5 cm and 7 cm. Find the hypotenuse."),
       D(r"c^2=5^2+7^2=25+49=74"),
       P(r"74 no és cap quadrat de la taula: l'arrel no és exacta. Amb la calculadora:", r"74 no es ningún cuadrado de la tabla: la raíz no es exacta. Con la calculadora:", r"74 isn't one of the squares in the table, so the root isn't exact. With a calculator:"),
       D(r"c=\sqrt{74}=8{,}602\ldots\approx\boxed{8{,}60\ \text{cm}}")),
  prob(L(r"Són rectangles els triangles de costats a) 7, 24 i 25 cm; b) 6, 7 i 9 cm?", r"¿Son rectángulos los triángulos de lados a) 7, 24 y 25 cm; b) 6, 7 y 9 cm?", r"Are these right triangles? a) sides 7, 24 and 25 cm; b) sides 6, 7 and 9 cm"),
       P(r"Comparem el quadrat del costat més llarg amb la suma dels quadrats dels altres dos:", r"Comparamos el cuadrado del lado más largo con la suma de los cuadrados de los otros dos:", r"Compare the square of the longest side with the sum of the squares of the other two:"),
       D(r"\text{a) }25^2=625,\quad 7^2+24^2=49+576=625\ \Rightarrow\ \boxed{" + Lt('sí que és rectangle', 'sí es rectángulo', "it's a right triangle") + r"}"),
       D(r"\text{b) }9^2=81,\quad 6^2+7^2=36+49=85\ \Rightarrow\ \boxed{" + Lt('no és rectangle', 'no es rectángulo', "it isn't a right triangle") + r"}"))],
 [prob(L(r"Un camp de futbol fa 100 m de llarg i 64 m d'ample. Quants metres t'estalvies si el travesses en diagonal en lloc d'anar per les bandes?", r"Un campo de fútbol mide 100 m de largo y 64 m de ancho. ¿Cuántos metros te ahorras si lo cruzas en diagonal en lugar de ir por las bandas?", r"A football pitch is 100 m long and 64 m wide. How many metres do you save by crossing it diagonally instead of walking along the edges?"),
       figs(G([('poly', [(0, 0), (10, 0), (10, 6.4), (0, 6.4)], 'lawn'), ('poly', [(0, 0), (10, 0), (10, 6.4)], 'tr'), ('ra', (10, 0), (0, 0), (10, 6.4)), T_((5, 0), '100 m', dy=16), T_((10, 3.2), '64 m', dx=8, a='start'), T_(off((0, 0), (10, 6.4), 0.7), 'd', cls='hot')], W=200, pad=36)),
       D(r"d=\sqrt{100^2+64^2}=\sqrt{10\,000+4096}=\sqrt{14\,096}\approx118{,}73\ \text{m}"),
       P(r"Per les bandes hi ha \(100+64=164\) m. T'estalvies", r"Por las bandas hay \(100+64=164\) m. Te ahorras", r"Along the edges it's \(100+64=164\) m. You save"),
       D(r"164-118{,}73=\boxed{45{,}27\ \text{m}}"))])
ck(hyp(9, 12), 15); ck(leg(10, 6), 8); ck(R(625, 100) - R(49, 100), 5.76); ck(leg(R(25, 10), R(7, 10)), 2.4)
ck(25 + 49, 74); ck(49 + 576, 625); ck(36 + 49, 85); ck(hyp(100, 64), 118.73, 2); ck(164 - 118.73, 45.27)
s10 += practice([
  ('★', L(r"a) Calcula la hipotenusa d'un triangle rectangle de catets 8 cm i 15 cm. b) La hipotenusa fa 26 cm i un catet 10 cm. Quant fa l'altre catet?", r"a) Calcula la hipotenusa de un triángulo rectángulo de catetos 8 cm y 15 cm. b) La hipotenusa mide 26 cm y un cateto 10 cm. ¿Cuánto mide el otro cateto?", r"a) Find the hypotenuse of a right triangle with legs of 8 cm and 15 cm. b) The hypotenuse is 26 cm and one leg is 10 cm. How long is the other leg?")),
  ('★★', L(r"c) Calcula la hipotenusa si els catets fan 3 cm i 5 cm (arrodoneix a les centèsimes). d) Són rectangles els triangles de costats 9, 40, 41 i 5, 6, 8?", r"c) Calcula la hipotenusa si los catetos miden 3 cm y 5 cm (redondea a las centésimas). d) ¿Son rectángulos los triángulos de lados 9, 40, 41 y 5, 6, 8?", r"c) Find the hypotenuse if the legs are 3 cm and 5 cm (round to hundredths). d) Are the triangles with sides 9, 40, 41 and 5, 6, 8 right triangles?")),
  ('★★★', L(r"e) Un estel està lligat a un fil de 25 m ben tibant. L'estel està just damunt d'un punt que queda a 15 m de la persona que l'agafa. A quina altura està l'estel (sense comptar l'altura de la mà)?", r"e) Una cometa está atada a un hilo de 25 m bien tenso. La cometa está justo encima de un punto que queda a 15 m de la persona que la sujeta. ¿A qué altura está la cometa (sin contar la altura de la mano)?", r"e) A kite is on a tight 25 m string. The kite is right above a point 15 m from the person holding it. How high is the kite (not counting the height of the hand)?"))],
  P(r"a) \(\sqrt{64+225}=\sqrt{289}=17\) cm. b) \(\sqrt{676-100}=\sqrt{576}=24\) cm. c) \(\sqrt{9+25}=\sqrt{34}\approx5{,}83\) cm. d) \(81+1600=1681=41^2\): sí; \(25+36=61\neq64\): no. e) \(\sqrt{625-225}=\sqrt{400}=20\) m.",
    r"a) \(\sqrt{64+225}=\sqrt{289}=17\) cm. b) \(\sqrt{676-100}=\sqrt{576}=24\) cm. c) \(\sqrt{9+25}=\sqrt{34}\approx5{,}83\) cm. d) \(81+1600=1681=41^2\): sí; \(25+36=61\neq64\): no. e) \(\sqrt{625-225}=\sqrt{400}=20\) m.",
    r"a) \(\sqrt{64+225}=\sqrt{289}=17\) cm. b) \(\sqrt{676-100}=\sqrt{576}=24\) cm. c) \(\sqrt{9+25}=\sqrt{34}\approx5.83\) cm. d) \(81+1600=1681=41^2\): yes; \(25+36=61\neq64\): no. e) \(\sqrt{625-225}=\sqrt{400}=20\) m."))
ck(hyp(8, 15), 17); ck(leg(26, 10), 24); ck(hyp(3, 5), 5.83, 2); ck(81 + 1600, 41 ** 2); ck(25 + 36, 61); ck(leg(25, 15), 20)

# =====================================================================
# 8.11 Pitàgores per a calcular àrees i perímetres
# =====================================================================
def capf(va, es, en): return L(va, es, en)
FA_RECT = [('poly', [(0, 0), (6, 0), (6, 4), (0, 4)], 'gf'), ('poly', [(0, 0), (6, 0), (6, 4)], 'tr'), ('ra', (6, 0), (0, 0), (6, 4)), T_((3, 0), 'b', dy=16), T_((6, 2), 'h', dx=8, a='start'), T_(off((0, 0), (6, 4), 0.5), 'd', cls='hot')]
FA_ISO = [('poly', [(-3, 0), (3, 0), (0, 5)], 'gf'), ('poly', [(0, 0), (3, 0), (0, 5)], 'tr'), ('seg', (0, 0), (0, 5), 'd'), ('ra', (0, 0), (3, 0), (0, 5)), T_((1.5, 0), r'b/2', dy=16), T_((0, 2.5), 'h', dx=-8, a='end', cls='hot'), T_(off((3, 0), (0, 5), -0.45), 'l', a='start')]
FA_ROM = [('poly', [(-4, 0), (0, 3), (4, 0), (0, -3)], 'gf'), ('seg', (-4, 0), (4, 0), 'd'), ('seg', (0, -3), (0, 3), 'd'), ('poly', [(0, 0), (4, 0), (0, 3)], 'tr'), ('ra', (0, 0), (4, 0), (0, 3)), T_((2, 0), 'D/2', dy=16), T_((0, 1.5), 'd/2', dx=-6, a='end'), T_(off((4, 0), (0, 3), -0.45), 'l', a='start', cls='hot')]
FA_TRAP = [('poly', [(0, 0), (7, 0), (4, 4), (0, 4)], 'gf'), ('poly', [(4, 0), (7, 0), (4, 4)], 'tr'), ('seg', (4, 0), (4, 4), 'd'), ('ra', (4, 0), (7, 0), (4, 4)), T_((3.5, 0), 'B', dy=16), T_((2, 4), 'b', dy=-7), T_((5.5, 0), 'B − b', dy=-6, cls='sm'), T_((4, 2), 'h', dx=-8, a='end'), T_(off((7, 0), (4, 4), -0.5), 'c', a='start', cls='hot')]
HX = reg(6, 3)
FA_HEX = [('poly', HX, 'gf'), ('poly', [(0, 0), mid(HX[0], HX[1]), HX[1]], 'tr'), ('seg', (0, 0), HX[0], 'd'), ('ra', mid(HX[0], HX[1]), (0, 0), HX[1]), ('dot', (0, 0)),
          T_(mid((0, 0), HX[1]), 'r = l', dx=-8, dy=-4, a='end'), T_(mid(mid(HX[0], HX[1]), HX[1]), 'l/2', dy=16), T_(mid((0, 0), mid(HX[0], HX[1])), 'a', dx=-8, a='end', cls='hot')]
s11 = box('prop', L('Busca el triangle rectangle amagat', 'Busca el triángulo rectángulo escondido', 'Look for the hidden right triangle'),
  P(r"Moltes vegades, per a calcular una àrea o un perímetre ens falta una mesura: una altura, un costat inclinat, una apotema… Si dins de la figura hi ha un <strong>triangle rectangle</strong> amb dos costats coneguts, el teorema de Pitàgores ens dona el tercer.",
    r"Muchas veces, para calcular un área o un perímetro nos falta una medida: una altura, un lado inclinado, una apotema… Si dentro de la figura hay un <strong>triángulo rectángulo</strong> con dos lados conocidos, el teorema de Pitágoras nos da el tercero.",
    r"Often, to find an area or a perimeter, we're missing a length: a height, a slanted side, an apothem… If there's a <strong>right triangle</strong> inside the shape with two known sides, Pythagoras' theorem gives us the third.")
  + ol(L(r"Dibuixa la figura i traça l'altura, la diagonal o l'apotema que necessites.", r"Dibuja la figura y traza la altura, la diagonal o la apotema que necesitas.", r"Draw the shape and add the height, diagonal or apothem you need."),
       L(r"Busca un triangle rectangle on la mesura que vols siga un costat i en conegues els altres dos.", r"Busca un triángulo rectángulo donde la medida que quieres sea un lado y conozcas los otros dos.", r"Find a right triangle where the length you want is a side and you know the other two."),
       L(r"Aplica Pitàgores (compte: quina és la hipotenusa?).", r"Aplica Pitágoras (cuidado: ¿cuál es la hipotenusa?).", r"Apply Pythagoras (careful: which side is the hypotenuse?)."),
       L(r"Ara ja pots calcular l'àrea o el perímetre.", r"Ahora ya puedes calcular el área o el perímetro.", r"Now you can find the area or the perimeter."))
  + figs(G(FA_RECT, W=170, pad=24, cap=capf(r'Rectangle: \(d^2=b^2+h^2\)', r'Rectángulo: \(d^2=b^2+h^2\)', r'Rectangle: \(d^2=b^2+h^2\)')),
         G(FA_ISO, W=140, pad=24, cap=capf(r'Triangle isòsceles: \(h^2=l^2-\left(\tfrac b2\right)^2\)', r'Triángulo isósceles: \(h^2=l^2-\left(\tfrac b2\right)^2\)', r'Isosceles triangle: \(h^2=l^2-\left(\tfrac b2\right)^2\)')),
         G(FA_ROM, W=180, pad=24, cap=capf(r'Rombe: \(l^2=\left(\tfrac D2\right)^2+\left(\tfrac d2\right)^2\)', r'Rombo: \(l^2=\left(\tfrac D2\right)^2+\left(\tfrac d2\right)^2\)', r'Rhombus: \(l^2=\left(\tfrac D2\right)^2+\left(\tfrac d2\right)^2\)')), three=True)
  + figs(G(FA_TRAP, W=200, pad=24, cap=capf(r'Trapezi rectangle: \(c^2=(B-b)^2+h^2\)', r'Trapecio rectángulo: \(c^2=(B-b)^2+h^2\)', r'Right trapezium: \(c^2=(B-b)^2+h^2\)')),
         G(FA_HEX, W=190, pad=24, cap=capf(r'Hexàgon regular: \(a^2=l^2-\left(\tfrac l2\right)^2\)', r'Hexágono regular: \(a^2=l^2-\left(\tfrac l2\right)^2\)', r'Regular hexagon: \(a^2=l^2-\left(\tfrac l2\right)^2\)')))
  + note(r"En el <strong>triangle isòsceles</strong> i en el <strong>trapezi isòsceles</strong>, l'altura parteix la figura en dues meitats iguals. En el <strong>rombe</strong>, les diagonals es tallen per la meitat formant angles rectes. En l'<strong>hexàgon regular</strong>, el radi és igual al costat.",
         r"En el <strong>triángulo isósceles</strong> y en el <strong>trapecio isósceles</strong>, la altura parte la figura en dos mitades iguales. En el <strong>rombo</strong>, las diagonales se cortan por la mitad formando ángulos rectos. En el <strong>hexágono regular</strong>, el radio es igual al lado.",
         r"In an <strong>isosceles triangle</strong> and an <strong>isosceles trapezium</strong>, the height splits the shape into two equal halves. In a <strong>rhombus</strong>, the diagonals cut each other in half at right angles. In a <strong>regular hexagon</strong>, the radius equals the side.", '💡')
  + widget('w-apl', '🔺', L('Pitàgores dins de les figures', 'Pitágoras dentro de las figuras', 'Pythagoras inside shapes'),
           [seg([('rect', L('Rectangle', 'Rectángulo', 'Rectangle')), ('iso', L('Triangle isòsceles', 'Triángulo isósceles', 'Isosceles triangle')), ('eq', L('Triangle equilàter', 'Triángulo equilátero', 'Equilateral triangle')),
                 ('rom', L('Rombe', 'Rombo', 'Rhombus')), ('trap', L('Trapezi isòsceles', 'Trapecio isósceles', 'Isosceles trapezium')), ('hex', L('Hexàgon', 'Hexágono', 'Hexagon'))]),
            '<div class="wrow">' + rng('p', 1, 16, 1, 8, 'p') + rng('q', 1, 16, 1, 6, 'q') + rng('r', 1, 12, 1, 5, 'r') + '</div>'])
  + drill('apl', 'Entrena: Pitàgores en figures', 'Entrena: Pitágoras en figuras', 'Train: Pythagoras in shapes'))
s11 += levels(
 [prob(L(r"Calcula la diagonal d'un rectangle de 12 cm × 5 cm.", r"Calcula la diagonal de un rectángulo de 12 cm × 5 cm.", r"Find the diagonal of a 12 cm × 5 cm rectangle."),
       figs(G([('poly', [(0, 0), (12, 0), (12, 5), (0, 5)], 'gf'), ('poly', [(0, 0), (12, 0), (12, 5)], 'tr'), ('ra', (12, 0), (0, 0), (12, 5)), T_((6, 0), '12', dy=16), T_((12, 2.5), '5', dx=8, a='start'), T_(off((0, 0), (12, 5), 0.8), 'd', cls='hot')], W=180, pad=24)),
       P(r"La diagonal és la hipotenusa d'un triangle rectangle que té de catets la base i l'altura:", r"La diagonal es la hipotenusa de un triángulo rectángulo que tiene de catetos la base y la altura:", r"The diagonal is the hypotenuse of a right triangle whose legs are the base and the height:"),
       D(r"d=\sqrt{12^2+5^2}=\sqrt{144+25}=\sqrt{169}=\boxed{13\ \text{cm}}")),
  prob(L(r"Un triangle isòsceles té els dos costats iguals de 10 cm i la base de 12 cm. Calcula'n l'altura i l'àrea.", r"Un triángulo isósceles tiene los dos lados iguales de 10 cm y la base de 12 cm. Calcula su altura y su área.", r"An isosceles triangle has two equal sides of 10 cm and a 12 cm base. Find its height and its area."),
       figs(G([('poly', [(-6, 0), (6, 0), (0, 8)], 'gf'), ('poly', [(0, 0), (6, 0), (0, 8)], 'tr'), ('seg', (0, 0), (0, 8), 'd'), ('ra', (0, 0), (6, 0), (0, 8)), T_((3, 0), '6', dy=16), T_((-3, 0), '6', dy=16), T_((0, 4), 'h', dx=-8, a='end', cls='hot'), T_(off((6, 0), (0, 8), -0.6), '10', a='start')], W=150, pad=24)),
       P(r"L'altura parteix la base en dues meitats de 6 cm. En el triangle rectangle, la hipotenusa és el costat de 10 cm:", r"La altura parte la base en dos mitades de 6 cm. En el triángulo rectángulo, la hipotenusa es el lado de 10 cm:", r"The height splits the base into two halves of 6 cm. In the right triangle, the hypotenuse is the 10 cm side:"),
       D(r"h=\sqrt{10^2-6^2}=\sqrt{100-36}=\sqrt{64}=8\ \text{cm}"), D(r"A=\frac{b\cdot h}{2}=\frac{12\cdot8}{2}=\boxed{48\ \text{cm}^2}"))],
 [prob(L(r"Les diagonals d'un rombe fan 16 cm i 12 cm. Calcula'n l'àrea i el perímetre.", r"Las diagonales de un rombo miden 16 cm y 12 cm. Calcula su área y su perímetro.", r"The diagonals of a rhombus are 16 cm and 12 cm. Find its area and its perimeter."),
       D(r"A=\frac{D\cdot d}{2}=\frac{16\cdot12}{2}=\boxed{96\ \text{cm}^2}"),
       P(r"Per al perímetre necessitem el costat. Les semidiagonals (8 i 6 cm) són els catets d'un triangle rectangle que té el costat com a hipotenusa:", r"Para el perímetro necesitamos el lado. Las semidiagonales (8 y 6 cm) son los catetos de un triángulo rectángulo que tiene el lado como hipotenusa:", r"For the perimeter we need the side. The half-diagonals (8 and 6 cm) are the legs of a right triangle whose hypotenuse is the side:"),
       D(r"l=\sqrt{8^2+6^2}=\sqrt{64+36}=\sqrt{100}=10\ \text{cm}\qquad P=4\cdot10=\boxed{40\ \text{cm}}")),
  prob(L(r"Un trapezi rectangle té les bases de 10 cm i 4 cm i l'altura de 8 cm. Calcula'n l'àrea i el perímetre.", r"Un trapecio rectángulo tiene las bases de 10 cm y 4 cm y la altura de 8 cm. Calcula su área y su perímetro.", r"A right trapezium has bases of 10 cm and 4 cm and a height of 8 cm. Find its area and its perimeter."),
       figs(G([('poly', [(0, 0), (10, 0), (4, 8), (0, 8)], 'gf'), ('poly', [(4, 0), (10, 0), (4, 8)], 'tr'), ('seg', (4, 0), (4, 8), 'd'), ('ra', (4, 0), (10, 0), (4, 8)), ('ra', (0, 0), (10, 0), (0, 8)),
               T_((5, 0), '10', dy=16), T_((2, 8), '4', dy=-7), T_((0, 4), '8', dx=-8, a='end'), T_((7, 0), '6', dy=-6), T_(off((10, 0), (4, 8), -0.7), 'c', a='start', cls='hot')], W=150, pad=24)),
       D(r"A=\frac{(B+b)\cdot h}{2}=\frac{(10+4)\cdot8}{2}=\boxed{56\ \text{cm}^2}"),
       P(r"Ens falta el costat inclinat \(c\). Si tracem l'altura des del final de la base menuda, queda un triangle rectangle de catets \(10-4=6\) cm i 8 cm:", r"Nos falta el lado inclinado \(c\). Si trazamos la altura desde el final de la base menor, queda un triángulo rectángulo de catetos \(10-4=6\) cm y 8 cm:", r"We're missing the slanted side \(c\). Drawing the height from the end of the short base leaves a right triangle with legs \(10-4=6\) cm and 8 cm:"),
       D(r"c=\sqrt{6^2+8^2}=\sqrt{100}=10\ \text{cm}\qquad P=10+4+8+10=\boxed{32\ \text{cm}}")),
  prob(L(r"Calcula l'àrea d'un hexàgon regular de 6 cm de costat.", r"Calcula el área de un hexágono regular de 6 cm de lado.", r"Find the area of a regular hexagon with 6 cm sides."),
       P(r"Necessitem l'apotema. En l'hexàgon regular el radi és igual al costat (6 cm). L'apotema, mig costat (3 cm) i el radi formen un triangle rectangle on el radi és la hipotenusa:", r"Necesitamos la apotema. En el hexágono regular el radio es igual al lado (6 cm). La apotema, medio lado (3 cm) y el radio forman un triángulo rectángulo donde el radio es la hipotenusa:", r"We need the apothem. In a regular hexagon the radius equals the side (6 cm). The apothem, half a side (3 cm) and the radius form a right triangle whose hypotenuse is the radius:"),
       D(r"a=\sqrt{6^2-3^2}=\sqrt{36-9}=\sqrt{27}\approx5{,}20\ \text{cm}"),
       D(r"P=6\cdot6=36\ \text{cm}\qquad A=\frac{P\cdot a}{2}=\frac{36\cdot5{,}2}{2}=\boxed{93{,}6\ \text{cm}^2}"))],
 [prob(L(r"Calcula l'àrea d'un triangle equilàter de 10 cm de costat.", r"Calcula el área de un triángulo equilátero de 10 cm de lado.", r"Find the area of an equilateral triangle with 10 cm sides."),
       P(r"L'altura parteix la base en dues meitats de 5 cm:", r"La altura parte la base en dos mitades de 5 cm:", r"The height splits the base into two halves of 5 cm:"),
       D(r"h=\sqrt{10^2-5^2}=\sqrt{75}\approx8{,}66\ \text{cm}\qquad A=\frac{10\cdot8{,}66}{2}=\boxed{43{,}3\ \text{cm}^2}")),
  prob(L(r"Dins d'un cercle de 5 cm de radi hi ha un quadrat amb els quatre vèrtexs sobre la circumferència. Calcula l'àrea de la part del cercle que queda fora del quadrat.", r"Dentro de un círculo de 5 cm de radio hay un cuadrado con los cuatro vértices sobre la circunferencia. Calcula el área de la parte del círculo que queda fuera del cuadrado.", r"Inside a disc with a 5 cm radius there's a square with its four corners on the circle. Find the area of the part of the disc outside the square."),
       figs(G([('circ', (0, 0), 5, 'sh'), ('poly', [(5, 0), (0, 5), (-5, 0), (0, -5)], 'hole'), ('poly', [(5, 0), (0, 5), (-5, 0), (0, -5)], 'frame'), ('poly', [(-5, 0), (0, -5), (5, 0)], 'tr'), ('ra', (0, -5), (-5, 0), (5, 0)), ('seg', (-5, 0), (5, 0), 'd'), ('dot', (0, 0)), T_((0, 0), '10', dy=-6), T_(mid((-5, 0), (0, -5)), 'l', dx=-8, dy=8, a='end', cls='hot'), T_(mid((0, -5), (5, 0)), 'l', dx=8, dy=8, a='start', cls='hot')], W=150, pad=20)),
       P(r"La diagonal del quadrat és un diàmetre: 10 cm. Dos costats del quadrat i la diagonal formen un triangle rectangle:", r"La diagonal del cuadrado es un diámetro: 10 cm. Dos lados del cuadrado y la diagonal forman un triángulo rectángulo:", r"The square's diagonal is a diameter: 10 cm. Two sides of the square and the diagonal form a right triangle:"),
       D(r"l^2+l^2=10^2\ \Rightarrow\ 2\cdot l^2=100\ \Rightarrow\ l^2=50"),
       P(r"I \(l^2\) és justament l'àrea del quadrat: 50 cm². No cal ni fer l'arrel!", r"Y \(l^2\) es justamente el área del cuadrado: 50 cm². ¡No hace falta ni hacer la raíz!", r"And \(l^2\) is exactly the area of the square: 50 cm². No need to take the root!"),
       D(r"A=3{,}14\cdot5^2-50=78{,}5-50=\boxed{28{,}5\ \text{cm}^2}")),
  prob(L(r"La façana d'una caseta és un rectangle de 6 m d'ample i 4 m d'alt amb una teulada en forma de triangle isòsceles de 4 m d'altura. Calcula'n l'àrea i el perímetre.", r"La fachada de una caseta es un rectángulo de 6 m de ancho y 4 m de alto con un tejado en forma de triángulo isósceles de 4 m de altura. Calcula su área y su perímetro.", r"The front of a hut is a rectangle 6 m wide and 4 m tall with a roof shaped like an isosceles triangle 4 m high. Find its area and its perimeter."),
       figs(G([('poly', [(0, 0), (6, 0), (6, 4), (0, 4)], 'gf'), ('poly', [(0, 4), (6, 4), (3, 8)], 'sh'), ('poly', [(3, 4), (6, 4), (3, 8)], 'tr'), ('seg', (3, 4), (3, 8), 'd'), ('ra', (3, 4), (6, 4), (3, 8)),
               T_((3, 0), '6', dy=16), T_((6, 2), '4', dx=8, a='start'), T_((3, 6), '4', dx=-8, a='end'), T_((4.5, 4), '3', dy=16), T_(off((6, 4), (3, 8), -0.5), 'x', a='start', cls='hot')], W=130, pad=24)),
       D(r"A=6\cdot4+\frac{6\cdot4}{2}=24+12=\boxed{36\ \text{m}^2}"),
       P(r"Cada costat de la teulada és la hipotenusa d'un triangle de catets 3 m (mitja base) i 4 m:", r"Cada lado del tejado es la hipotenusa de un triángulo de catetos 3 m (media base) y 4 m:", r"Each side of the roof is the hypotenuse of a triangle with legs of 3 m (half the base) and 4 m:"),
       D(r"x=\sqrt{3^2+4^2}=\sqrt{25}=5\ \text{m}\qquad P=6+4+4+5+5=\boxed{24\ \text{m}}"))])
ck(hyp(12, 5), 13); ck(leg(10, 6), 8); ck(R(12 * 8, 2), 48); ck(R(16 * 12, 2), 96); ck(hyp(8, 6), 10); ck(R(14 * 8, 2), 56); ck(10 + 4 + 8 + 10, 32)
ck(S(27), 5.20, 2); ck(36 * R(52, 10) / 2, 93.6); ck(S(75), 8.66, 2); ck(10 * R(866, 100) / 2, 43.3); ck(p * 25 - 50, 28.5); ck(24 + 12, 36); ck(hyp(3, 4), 5); ck(6 + 4 + 4 + 5 + 5, 24)
s11 += practice([
  ('★', L(r"a) Una pantalla fa 80 cm d'ample i 60 cm d'alt. Quant fa la diagonal? b) Calcula la diagonal d'un quadrat de 5 cm de costat.", r"a) Una pantalla mide 80 cm de ancho y 60 cm de alto. ¿Cuánto mide la diagonal? b) Calcula la diagonal de un cuadrado de 5 cm de lado.", r"a) A screen is 80 cm wide and 60 cm tall. How long is its diagonal? b) Find the diagonal of a square with 5 cm sides.")),
  ('★★', L(r"c) Les diagonals d'un rombe fan 24 cm i 10 cm. Calcula'n l'àrea i el perímetre. d) Un triangle isòsceles té 10 cm de base i els costats iguals de 13 cm. Calcula'n l'àrea i el perímetre.", r"c) Las diagonales de un rombo miden 24 cm y 10 cm. Calcula su área y su perímetro. d) Un triángulo isósceles tiene 10 cm de base y los lados iguales de 13 cm. Calcula su área y su perímetro.", r"c) A rhombus has diagonals of 24 cm and 10 cm. Find its area and its perimeter. d) An isosceles triangle has a 10 cm base and equal sides of 13 cm. Find its area and its perimeter.")),
  ('★★★', L(r"e) Un trapezi isòsceles té les bases de 20 cm i 8 cm i els costats iguals de 10 cm. Calcula'n l'àrea. f) Un rectangle de 8 cm × 6 cm té els quatre vèrtexs sobre una circumferència. Calcula la longitud de la circumferència.", r"e) Un trapecio isósceles tiene las bases de 20 cm y 8 cm y los lados iguales de 10 cm. Calcula su área. f) Un rectángulo de 8 cm × 6 cm tiene los cuatro vértices sobre una circunferencia. Calcula la longitud de la circunferencia.", r"e) An isosceles trapezium has bases of 20 cm and 8 cm and equal sides of 10 cm. Find its area. f) An 8 cm × 6 cm rectangle has its four corners on a circle. Find the length of the circle."))],
  P(r"a) \(\sqrt{6400+3600}=\sqrt{10\,000}=100\) cm. b) \(\sqrt{25+25}=\sqrt{50}\approx7{,}07\) cm. c) \(A=120\) cm²; \(l=\sqrt{12^2+5^2}=13\), \(P=52\) cm. d) \(h=\sqrt{169-25}=12\), \(A=60\) cm², \(P=36\) cm. e) Sobren \((20-8):2=6\) cm a cada costat: \(h=\sqrt{100-36}=8\), \(A=\tfrac{(20+8)\cdot8}{2}=112\) cm². f) La diagonal és un diàmetre: \(d=\sqrt{64+36}=10\), \(L=3{,}14\cdot10=31{,}4\) cm.",
    r"a) \(\sqrt{6400+3600}=\sqrt{10\,000}=100\) cm. b) \(\sqrt{25+25}=\sqrt{50}\approx7{,}07\) cm. c) \(A=120\) cm²; \(l=\sqrt{12^2+5^2}=13\), \(P=52\) cm. d) \(h=\sqrt{169-25}=12\), \(A=60\) cm², \(P=36\) cm. e) Sobran \((20-8):2=6\) cm a cada lado: \(h=\sqrt{100-36}=8\), \(A=\tfrac{(20+8)\cdot8}{2}=112\) cm². f) La diagonal es un diámetro: \(d=\sqrt{64+36}=10\), \(L=3{,}14\cdot10=31{,}4\) cm.",
    r"a) \(\sqrt{6400+3600}=\sqrt{10\,000}=100\) cm. b) \(\sqrt{25+25}=\sqrt{50}\approx7.07\) cm. c) \(A=120\) cm²; \(l=\sqrt{12^2+5^2}=13\), \(P=52\) cm. d) \(h=\sqrt{169-25}=12\), \(A=60\) cm², \(P=36\) cm. e) There's \((20-8)\div2=6\) cm left over on each side: \(h=\sqrt{100-36}=8\), \(A=\tfrac{(20+8)\cdot8}{2}=112\) cm². f) The diagonal is a diameter: \(d=\sqrt{64+36}=10\), \(L=3.14\cdot10=31.4\) cm."))
ck(hyp(80, 60), 100); ck(S(50), 7.07, 2); ck(R(24 * 10, 2), 120); ck(hyp(12, 5), 13); ck(4 * 13, 52); ck(leg(13, 5), 12); ck(R(10 * 12, 2), 60); ck(10 + 26, 36)
ck(R(20 - 8, 2), 6); ck(leg(10, 6), 8); ck(R(28 * 8, 2), 112); ck(hyp(8, 6), 10); ck(p * 10, 31.4)
