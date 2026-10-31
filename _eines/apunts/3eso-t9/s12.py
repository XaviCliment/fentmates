# 9.1 Teorema de Pitàgores · 9.2 Classificació de triangles pels costats
from comu import *

# =====================================================================
# 9.1 El teorema de Pitàgores
# =====================================================================
s1 = box('def', L('El teorema de Pitàgores', 'El teorema de Pitágoras', "Pythagoras' theorem"),
  P(r"En un <strong>triangle rectangle</strong> (té un angle de 90°), els dos costats que formen l'angle recte s'anomenen <strong>catets</strong> (\(a\) i \(b\)) i el costat oposat a l'angle recte és la <strong>hipotenusa</strong> (\(c\)), que és sempre el costat més llarg.",
    r"En un <strong>triángulo rectángulo</strong> (tiene un ángulo de 90°), los dos lados que forman el ángulo recto se llaman <strong>catetos</strong> (\(a\) y \(b\)) y el lado opuesto al ángulo recto es la <strong>hipotenusa</strong> (\(c\)), que es siempre el lado más largo.",
    r"In a <strong>right triangle</strong> (it has a 90° angle), the two sides that form the right angle are the <strong>legs</strong> (\(a\) and \(b\)) and the side opposite the right angle is the <strong>hypotenuse</strong> (\(c\)), which is always the longest side.")
  + P(r"<strong>Teorema de Pitàgores:</strong> en tot triangle rectangle, el quadrat de la hipotenusa és igual a la suma dels quadrats dels catets:",
      r"<strong>Teorema de Pitágoras:</strong> en todo triángulo rectángulo, el cuadrado de la hipotenusa es igual a la suma de los cuadrados de los catetos:",
      r"<strong>Pythagoras' theorem:</strong> in every right triangle, the square of the hypotenuse equals the sum of the squares of the legs:")
  + D(r"c^2=a^2+b^2")
  + P(r"Té una lectura geomètrica: l'<strong>àrea</strong> del quadrat construït sobre la hipotenusa és igual a la suma de les àrees dels quadrats construïts sobre els catets.",
      r"Tiene una lectura geométrica: el <strong>área</strong> del cuadrado construido sobre la hipotenusa es igual a la suma de las áreas de los cuadrados construidos sobre los catetos.",
      r"It has a geometric meaning: the <strong>area</strong> of the square drawn on the hypotenuse equals the sum of the areas of the squares drawn on the legs.")
  + figs(G(tri_sq(3, 4, grid=True), W=250, cap=r'\(3^2+4^2=5^2\): \(9+16=25\)'))
  + widget('w-pit', '📐', L('Els quadrats sobre els costats', 'Los cuadrados sobre los lados', 'Squares on the sides'),
           ['<div class="wrow">' + rng('a', 1, 8, 0.5, 3, 'a') + rng('b', 1, 8, 0.5, 4, 'b') + '</div>',
            quick([('3|4', '3, 4, 5'), ('6|8', '6, 8, 10'), ('5|5', '5, 5'), ('1|7', '1, 7'), ('2|3', '2, 3')])]))
s1 += box('prop', L('Per què és cert? Una demostració visual', '¿Por qué es cierto? Una demostración visual', 'Why is it true? A visual proof'),
  P(r"Dibuixem un quadrat de costat \(a+b\) i hi col·loquem quatre còpies del triangle rectangle de dues maneres diferents. En la primera, la part que queda lliure és un quadrat de costat \(c\) (àrea \(c^2\)). En la segona, queden lliures dos quadrats, de costats \(a\) i \(b\) (àrees \(a^2\) i \(b^2\)).",
    r"Dibujamos un cuadrado de lado \(a+b\) y colocamos dentro cuatro copias del triángulo rectángulo de dos maneras distintas. En la primera, la parte que queda libre es un cuadrado de lado \(c\) (área \(c^2\)). En la segunda, quedan libres dos cuadrados, de lados \(a\) y \(b\) (áreas \(a^2\) y \(b^2\)).",
    r"Draw a square of side \(a+b\) and place four copies of the right triangle inside it in two different ways. In the first, the free part is a square of side \(c\) (area \(c^2\)). In the second, two squares are left free, with sides \(a\) and \(b\) (areas \(a^2\) and \(b^2\)).")
  + P(r"El quadrat gran és el mateix i els quatre triangles també: per tant, les zones lliures tenen la mateixa àrea, \(c^2=a^2+b^2\).",
      r"El cuadrado grande es el mismo y los cuatro triángulos también: por tanto, las zonas libres tienen la misma área, \(c^2=a^2+b^2\).",
      r"The big square is the same and so are the four triangles, so the free regions have the same area: \(c^2=a^2+b^2\).")
  + widget('w-proof', '🧩', L('Recol·loca els quatre triangles', 'Recoloca los cuatro triángulos', 'Rearrange the four triangles'),
           [seg([('0', L('Disposició 1: queda c²', 'Disposición 1: queda c²', 'Layout 1: c² is left')), ('1', L('Disposició 2: queden a² i b²', 'Disposición 2: quedan a² y b²', 'Layout 2: a² and b² are left'))]),
            '<div class="wrow">' + rng('a', 1, 6, 0.5, 2, 'a') + rng('b', 1, 6, 0.5, 4, 'b') + '</div>']))
s1 += box('prop', L("Calcular un costat d'un triangle rectangle", 'Calcular un lado de un triángulo rectángulo', 'Finding a side of a right triangle'),
  P(r"Si coneixem dos costats, el teorema ens dona el tercer. Per a la <strong>hipotenusa</strong> sumem els quadrats; per a un <strong>catet</strong> restem: al quadrat de la hipotenusa li llevem el quadrat de l'altre catet.",
    r"Si conocemos dos lados, el teorema nos da el tercero. Para la <strong>hipotenusa</strong> sumamos los cuadrados; para un <strong>cateto</strong> restamos: al cuadrado de la hipotenusa le quitamos el cuadrado del otro cateto.",
    r"If we know two sides, the theorem gives the third. For the <strong>hypotenuse</strong> add the squares; for a <strong>leg</strong> subtract: take the square of the other leg away from the square of the hypotenuse.")
  + D(r"c=\sqrt{a^2+b^2}\qquad\quad a=\sqrt{c^2-b^2}\qquad\quad b=\sqrt{c^2-a^2}")
  + D(r"a=6,\ b=8:\quad c=\sqrt{36+64}=\sqrt{100}=10") + D(r"c=13,\ b=5:\quad a=\sqrt{169-25}=\sqrt{144}=12")
  + note(r"Si l'arrel no és exacta, deixa-la indicada (\(\sqrt{74}\)) o dona'n un valor aproximat amb la calculadora: \(\sqrt{74}\approx8{,}60\). Abans de restar, comprova que la hipotenusa és el costat més llarg!",
         r"Si la raíz no es exacta, déjala indicada (\(\sqrt{74}\)) o da un valor aproximado con la calculadora: \(\sqrt{74}\approx8{,}60\). Antes de restar, ¡comprueba que la hipotenusa es el lado más largo!",
         r"If the root isn't exact, leave it as \(\sqrt{74}\) or give an approximate value with a calculator: \(\sqrt{74}\approx8.60\). Before subtracting, check that the hypotenuse is the longest side!")
  + widget('w-pcalc', '🧮', L('Calculadora de Pitàgores', 'Calculadora de Pitágoras', 'Pythagoras calculator'),
           ['<div class="wrow">' + tin('a', L('catet a =', 'cateto a =', 'leg a ='), '6') + tin('b', L('catet b =', 'cateto b =', 'leg b ='), '8') + tin('c', L('hipotenusa c =', 'hipotenusa c =', 'hypotenuse c ='), '') + '</div>',
            '<p class="hint-s">' + L("Deixa en blanc el costat que vols calcular.", "Deja en blanco el lado que quieres calcular.", "Leave blank the side you want to find.") + '</p>',
            quick([('6|8|', 'a = 6, b = 8'), ('|5|13', 'b = 5, c = 13'), ('7||25', 'a = 7, c = 25'), ('5|7|', 'a = 5, b = 7'), ('|1,4|5', 'b = 1,4, c = 5')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('hip', 'Entrena: calcula la hipotenusa', 'Entrena: calcula la hipotenusa', 'Train: find the hypotenuse')
  + drill('cat', 'Entrena: calcula un catet', 'Entrena: calcula un cateto', 'Train: find a leg'))
ck(hyp(6, 8), 10); ck(leg(13, 5), 12); ck(hyp(5, 7), 8.60, 2)
s1 += box('prop', L('Ternes pitagòriques', 'Ternas pitagóricas', 'Pythagorean triples'),
  P(r"Tres nombres naturals que compleixen \(a^2+b^2=c^2\) formen una <strong>terna pitagòrica</strong>. Les més conegudes són",
    r"Tres números naturales que cumplen \(a^2+b^2=c^2\) forman una <strong>terna pitagórica</strong>. Las más conocidas son",
    r"Three whole numbers with \(a^2+b^2=c^2\) form a <strong>Pythagorean triple</strong>. The best known are")
  + D(r"(3,\,4,\,5)\quad(5,\,12,\,13)\quad(8,\,15,\,17)\quad(7,\,24,\,25)\quad(20,\,21,\,29)")
  + P(r"Si multipliquem una terna per un nombre, n'obtenim una altra: \((6,\,8,\,10)\), \((9,\,12,\,15)\), \((10,\,24,\,26)\)…",
      r"Si multiplicamos una terna por un número, obtenemos otra: \((6,\,8,\,10)\), \((9,\,12,\,15)\), \((10,\,24,\,26)\)…",
      r"Multiplying a triple by a number gives another one: \((6,\,8,\,10)\), \((9,\,12,\,15)\), \((10,\,24,\,26)\)…")
  + note(r"Els antics egipcis feien angles rectes amb una corda de 12 nucs igualment separats: si la tensaven formant un triangle de costats 3, 4 i 5, l'angle entre els costats 3 i 4 era recte.",
         r"Los antiguos egipcios trazaban ángulos rectos con una cuerda de 12 nudos igualmente separados: si la tensaban formando un triángulo de lados 3, 4 y 5, el ángulo entre los lados 3 y 4 era recto.",
         r"The ancient Egyptians made right angles with a rope with 12 equally spaced knots: stretched into a triangle with sides 3, 4 and 5, the angle between the sides 3 and 4 was a right angle.", '🏺'))
for t in [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (6, 8, 10), (9, 12, 15), (10, 24, 26)]: assert t[0] ** 2 + t[1] ** 2 == t[2] ** 2

LAD = G([('seg', (0, -0.05), (0, 5.4), 'wall'), ('seg', (-0.4, 0), (2.4, 0), 'wall'), ('poly', [(0, 0), (1.4, 0), (0, 4.8)], 'tr'), ('ra', (0, 0), (1, 0), (0, 1)),
         ('txt', (0.7, 0), '1,4 m', {'dy': 15}), ('txt', (0, 2.4), 'h', {'dx': -10, 'cls': 'hy'}), ('txt', off((1.4, 0), (0, 4.8), -0.4), '5 m')], W=150, maxh=230)
x_ = sp.Symbol('x')
assert sp.solve(x_ ** 2 + (x_ + 7) ** 2 - 169, x_) == [-12, 5]
s1 += levels(
 [prob(L(r"Calcula la hipotenusa d'un triangle rectangle els catets del qual mesuren 9 cm i 12 cm.", r"Calcula la hipotenusa de un triángulo rectángulo cuyos catetos miden 9 cm y 12 cm.", r"Find the hypotenuse of a right triangle whose legs are 9 cm and 12 cm."),
       D(r"c=\sqrt{9^2+12^2}=\sqrt{81+144}=\sqrt{225}=\boxed{15\ \text{cm}}")),
  prob(L(r"La hipotenusa d'un triangle rectangle mesura 10 m i un catet, 7 m. Calcula l'altre catet.", r"La hipotenusa de un triángulo rectángulo mide 10 m y un cateto, 7 m. Calcula el otro cateto.", r"The hypotenuse of a right triangle is 10 m and one leg is 7 m. Find the other leg."),
       D(r"b=\sqrt{10^2-7^2}=\sqrt{100-49}=\sqrt{51}\approx\boxed{7{,}14\ \text{m}}"))],
 [prob(L(r"Una escala de 5 m està recolzada en una paret i el peu de l'escala està a 1,4 m de la paret. A quina altura arriba l'escala?", r"Una escalera de 5 m está apoyada en una pared y el pie de la escalera está a 1,4 m de la pared. ¿A qué altura llega la escalera?", r"A 5 m ladder leans against a wall with its foot 1.4 m from the wall. How high up the wall does it reach?"),
       P(r"L'escala, la paret i el terra formen un triangle rectangle. L'escala és la <strong>hipotenusa</strong> i l'altura, un catet:", r"La escalera, la pared y el suelo forman un triángulo rectángulo. La escalera es la <strong>hipotenusa</strong> y la altura, un cateto:", r"The ladder, the wall and the ground form a right triangle. The ladder is the <strong>hypotenuse</strong> and the height is a leg:") + figs(LAD),
       D(r"h=\sqrt{5^2-1{,}4^2}=\sqrt{25-1{,}96}=\sqrt{23{,}04}=\boxed{4{,}8\ \text{m}}"))],
 [prob(L(r"En un triangle rectangle, un catet mesura 7 cm més que l'altre i la hipotenusa mesura 13 cm. Quant mesuren els catets?", r"En un triángulo rectángulo, un cateto mide 7 cm más que el otro y la hipotenusa mide 13 cm. ¿Cuánto miden los catetos?", r"In a right triangle one leg is 7 cm longer than the other and the hypotenuse is 13 cm. How long are the legs?"),
       P(r"Si un catet és \(x\), l'altre és \(x+7\). Apliquem Pitàgores i resolem l'equació de segon grau:", r"Si un cateto es \(x\), el otro es \(x+7\). Aplicamos Pitágoras y resolvemos la ecuación de segundo grado:", r"If one leg is \(x\), the other is \(x+7\). Apply Pythagoras and solve the quadratic equation:"),
       D(r"x^2+(x+7)^2=13^2\ \Rightarrow\ 2x^2+14x+49=169\ \Rightarrow\ x^2+7x-60=0"),
       D(r"x=\frac{-7\pm\sqrt{49+240}}{2}=\frac{-7\pm17}{2}\ \Rightarrow\ x=5\ \ (x=-12\ \text{%s})" % Lt('no té sentit', 'no tiene sentido', 'makes no sense')),
       P(r"Els catets mesuren <strong>5 cm</strong> i <strong>12 cm</strong>. Comprovació: \(25+144=169\ \checkmark\)", r"Los catetos miden <strong>5 cm</strong> y <strong>12 cm</strong>. Comprobación: \(25+144=169\ \checkmark\)", r"The legs are <strong>5 cm</strong> and <strong>12 cm</strong>. Check: \(25+144=169\ \checkmark\)"))])
ck(hyp(9, 12), 15); ck(leg(10, 7), 7.14, 2); ck(leg(5, R(14, 10)), R(48, 10))
s1 += practice([
  ('★', L(r"a) Calcula la hipotenusa si els catets mesuren 8 i 15. b) Calcula un catet si la hipotenusa mesura 26 i l'altre catet, 10.", r"a) Calcula la hipotenusa si los catetos miden 8 y 15. b) Calcula un cateto si la hipotenusa mide 26 y el otro cateto, 10.", r"a) Find the hypotenuse if the legs are 8 and 15. b) Find a leg if the hypotenuse is 26 and the other leg is 10.")),
  ('★★', L(r"c) Calcula la hipotenusa si els catets mesuren 4 i 5 (arrodoneix a les centèsimes). d) Una porta fa 2 m d'amplària i la seua diagonal mesura 2,5 m. Quina altura té?", r"c) Calcula la hipotenusa si los catetos miden 4 y 5 (redondea a las centésimas). d) Una puerta mide 2 m de ancho y su diagonal mide 2,5 m. ¿Qué altura tiene?", r"c) Find the hypotenuse if the legs are 4 and 5 (round to 2 decimal places). d) A gate is 2 m wide and its diagonal is 2.5 m. How tall is it?")),
  ('★★★', L(r"e) Un triangle rectangle isòsceles (els dos catets iguals) té una hipotenusa de 8 cm. Quant mesura cada catet?", r"e) Un triángulo rectángulo isósceles (los dos catetos iguales) tiene una hipotenusa de 8 cm. ¿Cuánto mide cada cateto?", r"e) An isosceles right triangle (both legs equal) has an 8 cm hypotenuse. How long is each leg?"))],
  P(r"a) \(\sqrt{64+225}=17\). b) \(\sqrt{676-100}=24\). c) \(\sqrt{41}\approx6{,}40\). d) \(\sqrt{6{,}25-4}=\sqrt{2{,}25}=1{,}5\) m. e) \(x^2+x^2=64\Rightarrow x=\sqrt{32}\approx5{,}66\) cm.",
    r"a) \(\sqrt{64+225}=17\). b) \(\sqrt{676-100}=24\). c) \(\sqrt{41}\approx6{,}40\). d) \(\sqrt{6{,}25-4}=\sqrt{2{,}25}=1{,}5\) m. e) \(x^2+x^2=64\Rightarrow x=\sqrt{32}\approx5{,}66\) cm.",
    r"a) \(\sqrt{64+225}=17\). b) \(\sqrt{676-100}=24\). c) \(\sqrt{41}\approx6.40\). d) \(\sqrt{6.25-4}=\sqrt{2.25}=1.5\) m. e) \(x^2+x^2=64\Rightarrow x=\sqrt{32}\approx5.66\) cm."))
ck(hyp(8, 15), 17); ck(leg(26, 10), 24); ck(hyp(4, 5), 6.40, 2); ck(leg(R(5, 2), 2), R(3, 2)); ck(S(32), 5.66, 2)

# =====================================================================
# 9.2 Classificació de triangles pels costats
# =====================================================================
def tri3(a, b, c, cls='tr', mark=''):
    """triangle de costats a, b, c amb c (el més llarg) a la base; marca l'angle oposat a c"""
    xA = (c * c + b * b - a * a) / (2 * c); yA = math.sqrt(b * b - xA * xA)
    T = (xA, yA); it = [('poly', [(0, 0), (c, 0), T], cls)]
    if mark == 'r': it.append(('ra', T, (0, 0), (c, 0)))
    elif mark:
        a0 = math.degrees(math.atan2(-yA, -xA)); a1 = math.degrees(math.atan2(-yA, c - xA))
        it.append(('arc', T, 0.18 * c, a0, a1, 'ang'))
    it += [('txt', (c / 2, 0), str(c).replace('.', ','), {'dy': 15}), ('txt', off((0, 0), T, 0.09 * c), str(b).replace('.', ','), {}), ('txt', off(T, (c, 0), 0.09 * c), str(a).replace('.', ','), {})]
    return it
s2 = box('def', L('El recíproc del teorema de Pitàgores', 'El recíproco del teorema de Pitágoras', 'The converse of Pythagoras'),
  P(r"El teorema també funciona al revés: si els costats \(a,\,b,\,c\) d'un triangle compleixen \(c^2=a^2+b^2\), el triangle és <strong>rectangle</strong>, i l'angle recte és el que està davant del costat \(c\).",
    r"El teorema también funciona al revés: si los lados \(a,\,b,\,c\) de un triángulo cumplen \(c^2=a^2+b^2\), el triángulo es <strong>rectángulo</strong>, y el ángulo recto es el que está frente al lado \(c\).",
    r"The theorem also works backwards: if the sides \(a,\,b,\,c\) of a triangle satisfy \(c^2=a^2+b^2\), the triangle is a <strong>right triangle</strong>, and the right angle is the one opposite side \(c\).")
  + P(r"Si no es compleix la igualtat, el triangle no és rectangle, però la comparació encara ens diu com és l'angle més gran.",
      r"Si no se cumple la igualdad, el triángulo no es rectángulo, pero la comparación aún nos dice cómo es el ángulo mayor.",
      r"If the equality fails, the triangle isn't a right triangle, but the comparison still tells us what the largest angle is like."))
s2 += box('prop', L('Classificar un triangle pels angles a partir dels costats', 'Clasificar un triángulo por sus ángulos a partir de los lados', 'Classifying a triangle by its angles from its sides'),
  P(r"Siga \(c\) el costat <strong>més llarg</strong>. Comparem \(c^2\) amb \(a^2+b^2\):", r"Sea \(c\) el lado <strong>más largo</strong>. Comparamos \(c^2\) con \(a^2+b^2\):", r"Let \(c\) be the <strong>longest</strong> side. Compare \(c^2\) with \(a^2+b^2\):")
  + tbl(['', L('Triangle', 'Triángulo', 'Triangle'), L("L'angle més gran", 'El ángulo mayor', 'The largest angle')],
        [[r'\(c^2<a^2+b^2\)', L('<strong>acutangle</strong>', '<strong>acutángulo</strong>', '<strong>acute</strong>'), L('és agut (menys de 90°)', 'es agudo (menos de 90°)', 'is acute (less than 90°)')],
         [r'\(c^2=a^2+b^2\)', L('<strong>rectangle</strong>', '<strong>rectángulo</strong>', '<strong>right</strong>'), L('és recte (90°)', 'es recto (90°)', 'is a right angle (90°)')],
         [r'\(c^2>a^2+b^2\)', L('<strong>obtusangle</strong>', '<strong>obtusángulo</strong>', '<strong>obtuse</strong>'), L('és obtús (més de 90°)', 'es obtuso (más de 90°)', 'is obtuse (more than 90°)')]], 'narrow')
  + figs(G(tri3(5, 6, 7, 'tr', 'a'), W=200, cap=r'\(49<25+36\)'), G(tri3(3, 4, 5, 'tr', 'r'), W=200, cap=r'\(25=9+16\)'), G(tri3(3, 5, 7, 'tr', 'o'), W=200, cap=r'\(49>9+25\)'), three=True)
  + note(r"Abans de res, comprova que els tres segments poden formar un triangle: el costat més llarg ha de ser <strong>menor que la suma</strong> dels altres dos (desigualtat triangular). Amb 2, 3 i 6 no hi ha triangle: \(6>2+3\).",
         r"Antes de nada, comprueba que los tres segmentos pueden formar un triángulo: el lado más largo debe ser <strong>menor que la suma</strong> de los otros dos (desigualdad triangular). Con 2, 3 y 6 no hay triángulo: \(6>2+3\).",
         r"First of all, check that the three lengths can make a triangle: the longest side must be <strong>less than the sum</strong> of the other two (triangle inequality). With 2, 3 and 6 there is no triangle: \(6>2+3\).", '⚠️')
  + widget('w-class', '🔺', L('Classifica un triangle', 'Clasifica un triángulo', 'Classify a triangle'),
           ['<div class="wrow">' + tin('a', 'a =', '4') + tin('b', 'b =', '5') + tin('c', 'c =', '6') + '</div>',
            quick([('6|8|10', '6, 8, 10'), ('4|5|6', '4, 5, 6'), ('3|5|7', '3, 5, 7'), ('20|21|29', '20, 21, 29'), ('2|3|6', '2, 3, 6')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('class', 'Entrena: acutangle, rectangle o obtusangle?', 'Entrena: ¿acutángulo, rectángulo u obtusángulo?', 'Train: acute, right or obtuse?', 'opts'))
s2 += levels(
 [prob(L(r"Classifica segons els angles els triangles de costats: a) 6, 8 i 10; b) 4, 5 i 6; c) 3, 5 i 7.", r"Clasifica según sus ángulos los triángulos de lados: a) 6, 8 y 10; b) 4, 5 y 6; c) 3, 5 y 7.", r"Classify by their angles the triangles with sides: a) 6, 8 and 10; b) 4, 5 and 6; c) 3, 5 and 7."),
       D(r"\text{a) }10^2=100,\quad 6^2+8^2=36+64=100\ \Rightarrow\ \boxed{\text{%s}}" % Lt('rectangle', 'rectángulo', 'right')),
       D(r"\text{b) }6^2=36,\quad 4^2+5^2=16+25=41\ \Rightarrow\ 36<41\ \Rightarrow\ \boxed{\text{%s}}" % Lt('acutangle', 'acutángulo', 'acute')),
       D(r"\text{c) }7^2=49,\quad 3^2+5^2=9+25=34\ \Rightarrow\ 49>34\ \Rightarrow\ \boxed{\text{%s}}" % Lt('obtusangle', 'obtusángulo', 'obtuse')))],
 [prob(L(r"Un fuster ha fet un marc de 60 cm × 80 cm i en mesura una diagonal: 1 m. Té els angles rectes? I si la diagonal haguera mesurat 98 cm?", r"Un carpintero ha hecho un marco de 60 cm × 80 cm y mide una diagonal: 1 m. ¿Tiene los ángulos rectos? ¿Y si la diagonal hubiera medido 98 cm?", r"A carpenter has made a 60 cm × 80 cm frame and measures a diagonal: 1 m. Are its corners right angles? What if the diagonal had been 98 cm?"),
       D(r"60^2+80^2=3600+6400=10\,000=100^2"),
       P(r"Es compleix el teorema: l'angle és <strong>recte</strong>. Amb 98 cm, \(98^2=9604<10\,000\): l'angle oposat a la diagonal seria <strong>agut</strong> i el marc no seria rectangular.", r"Se cumple el teorema: el ángulo es <strong>recto</strong>. Con 98 cm, \(98^2=9604<10\,000\): el ángulo opuesto a la diagonal sería <strong>agudo</strong> y el marco no sería rectangular.", r"The theorem holds: the angle is a <strong>right angle</strong>. With 98 cm, \(98^2=9604<10\,000\): the angle opposite the diagonal would be <strong>acute</strong> and the frame wouldn't be rectangular."))],
 [prob(L(r"Quant ha de mesurar \(x\) perquè el triangle de costats 8, 15 i \(x\) siga rectangle? Hi ha dues possibilitats.", r"¿Cuánto debe medir \(x\) para que el triángulo de lados 8, 15 y \(x\) sea rectángulo? Hay dos posibilidades.", r"How long must \(x\) be for the triangle with sides 8, 15 and \(x\) to be a right triangle? There are two possibilities."),
       P(r"Si \(x\) és la hipotenusa:", r"Si \(x\) es la hipotenusa:", r"If \(x\) is the hypotenuse:") + D(r"x=\sqrt{8^2+15^2}=\sqrt{289}=\boxed{17}"),
       P(r"Si la hipotenusa és 15, \(x\) és un catet:", r"Si la hipotenusa es 15, \(x\) es un cateto:", r"If the hypotenuse is 15, \(x\) is a leg:") + D(r"x=\sqrt{15^2-8^2}=\sqrt{161}\approx\boxed{12{,}69}"))])
ck(hyp(8, 15), 17); ck(leg(15, 8), 12.69, 2)
s2 += practice([
  ('★', L(r"Classifica els triangles de costats: a) 9, 12 i 15; b) 5, 6 i 8.", r"Clasifica los triángulos de lados: a) 9, 12 y 15; b) 5, 6 y 8.", r"Classify the triangles with sides: a) 9, 12 and 15; b) 5, 6 and 8.")),
  ('★★', L(r"c) És rectangle el triangle de costats 7, 24 i 25? d) Pot existir un triangle de costats 3, 4 i 8?", r"c) ¿Es rectángulo el triángulo de lados 7, 24 y 25? d) ¿Puede existir un triángulo de lados 3, 4 y 8?", r"c) Is the triangle with sides 7, 24 and 25 a right triangle? d) Can a triangle with sides 3, 4 and 8 exist?")),
  ('★★★', L(r"e) Troba els valors enters de \(x\) que fan obtusangle el triangle de costats 5, 12 i \(x\), si \(x\) és el costat més llarg.", r"e) Halla los valores enteros de \(x\) que hacen obtusángulo el triángulo de lados 5, 12 y \(x\), si \(x\) es el lado más largo.", r"e) Find the whole-number values of \(x\) that make the triangle with sides 5, 12 and \(x\) obtuse, if \(x\) is the longest side."))],
  P(r"a) \(225=81+144\): rectangle. b) \(64>25+36=61\): obtusangle. c) Sí: \(625=49+576\). d) No: \(8>3+4\). e) \(x^2>169\Rightarrow x>13\), i a més \(x<5+12=17\): \(x=14,\,15,\,16\).",
    r"a) \(225=81+144\): rectángulo. b) \(64>25+36=61\): obtusángulo. c) Sí: \(625=49+576\). d) No: \(8>3+4\). e) \(x^2>169\Rightarrow x>13\), y además \(x<5+12=17\): \(x=14,\,15,\,16\).",
    r"a) \(225=81+144\): right. b) \(64>25+36=61\): obtuse. c) Yes: \(625=49+576\). d) No: \(8>3+4\). e) \(x^2>169\Rightarrow x>13\), and also \(x<5+12=17\): \(x=14,\,15,\,16\)."))
assert 15 ** 2 == 9 ** 2 + 12 ** 2 and 8 ** 2 > 5 ** 2 + 6 ** 2 and 25 ** 2 == 7 ** 2 + 24 ** 2
assert [x for x in range(13, 30) if x * x > 169 and x < 17] == [14, 15, 16]
