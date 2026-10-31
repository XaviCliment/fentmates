# 11.1 Poliedres. Fórmula d'Euler · 11.2 Prismes: elements i àrea
from comu import *
from fig11 import *

def solid(it, W=200, cap=None, maxh=200, pad=18): return G(it, W=W, cap=cap, maxh=maxh, pad=pad)

# =====================================================================
# 11.1 Poliedres. Fórmula d'Euler. Poliedres regulars
# =====================================================================
PR, PP = polyhedron(prism(5, 2, 3))
PR += [('txt', PP[7], Ls('vèrtex', 'vértice', 'vertex'), {'dx': 8, 'dy': -4, 'a': 'start', 'cls': 'hot'}), ('dot', PP[7], 'pa'),
       ('txt', ((PP[0][0] + PP[1][0]) / 2, (PP[0][1] + PP[1][1]) / 2), Ls('aresta', 'arista', 'edge'), {'dy': 16, 'cls': 'hot'}),
       ('txt', ((PP[0][0] + PP[1][0] + PP[5][0] + PP[6][0]) / 4, (PP[0][1] + PP[1][1] + PP[5][1] + PP[6][1]) / 4), Ls('cara', 'cara', 'face'), {'cls': 'hot'})]
s1 = box('def', L('Poliedres i els seus elements', 'Poliedros y sus elementos', 'Polyhedra and their parts'),
  P(r"Un <strong>poliedre</strong> és un cos geomètric limitat per polígons. Els seus elements són:",
    r"Un <strong>poliedro</strong> es un cuerpo geométrico limitado por polígonos. Sus elementos son:",
    r"A <strong>polyhedron</strong> is a solid bounded by polygons. Its parts are:")
  + ul(L(r"<strong>Cares</strong>: els polígons que el limiten.", r"<strong>Caras</strong>: los polígonos que lo limitan.", r"<strong>Faces</strong>: the polygons that bound it."),
       L(r"<strong>Arestes</strong>: els costats de les cares (cada aresta és comuna a dues cares).", r"<strong>Aristas</strong>: los lados de las caras (cada arista es común a dos caras).", r"<strong>Edges</strong>: the sides of the faces (each edge is shared by two faces)."),
       L(r"<strong>Vèrtexs</strong>: els punts on es troben tres o més arestes.", r"<strong>Vértices</strong>: los puntos donde se encuentran tres o más aristas.", r"<strong>Vertices</strong>: the points where three or more edges meet."),
       L(r"<strong>Angles díedres</strong>: els que formen dues cares que tenen una aresta comuna.", r"<strong>Ángulos diedros</strong>: los que forman dos caras que tienen una arista común.", r"<strong>Dihedral angles</strong>: the angles between two faces that share an edge."))
  + figs(solid(PR, W=220))
  + P(r"Un poliedre és <strong>convex</strong> si qualsevol segment que uneix dos punts seus queda dins del poliedre (totes les cares es poden recolzar sobre una taula); si no, és <strong>còncau</strong>.",
      r"Un poliedro es <strong>convexo</strong> si cualquier segmento que une dos puntos suyos queda dentro del poliedro (todas las caras se pueden apoyar sobre una mesa); si no, es <strong>cóncavo</strong>.",
      r"A polyhedron is <strong>convex</strong> if any segment joining two of its points stays inside it (it can rest on a table on any face); otherwise it is <strong>concave</strong>."))
s1 += box('prop', L("La fórmula d'Euler", 'La fórmula de Euler', "Euler's formula"),
  P(r"En tot poliedre convex, el nombre de cares \(C\), de vèrtexs \(V\) i d'arestes \(A\) compleix la <strong>fórmula d'Euler</strong>:",
    r"En todo poliedro convexo, el número de caras \(C\), de vértices \(V\) y de aristas \(A\) cumple la <strong>fórmula de Euler</strong>:",
    r"In every convex polyhedron, the number of faces \(C\), vertices \(V\) and edges \(A\) satisfies <strong>Euler's formula</strong>:")
  + D(r"C+V=A+2")
  + P(r"Per exemple, el prisma pentagonal de la figura té \(C=7\), \(V=10\) i \(A=15\): \(7+10=15+2\ \checkmark\). Si en coneixem dos, la fórmula ens dona el tercer.",
      r"Por ejemplo, el prisma pentagonal de la figura tiene \(C=7\), \(V=10\) y \(A=15\): \(7+10=15+2\ \checkmark\). Si conocemos dos, la fórmula nos da el tercero.",
      r"For example, the pentagonal prism in the figure has \(C=7\), \(V=10\) and \(A=15\): \(7+10=15+2\ \checkmark\). If we know two of them, the formula gives the third.")
  + widget('w-poly', '🧊', L('Gira el poliedre i compta', 'Gira el poliedro y cuenta', 'Rotate the polyhedron and count'),
           [seg([('tetra', L('Tetraedre', 'Tetraedro', 'Tetrahedron')), ('cub', L('Cub', 'Cubo', 'Cube')), ('octa', L('Octaedre', 'Octaedro', 'Octahedron')), ('dodeca', L('Dodecaedre', 'Dodecaedro', 'Dodecahedron')), ('ico', L('Icosaedre', 'Icosaedro', 'Icosahedron')),
                 ('p5', L('Prisma pentagonal', 'Prisma pentagonal', 'Pentagonal prism')), ('y6', L('Piràmide hexagonal', 'Pirámide hexagonal', 'Hexagonal pyramid'))], 1),
            '<p class="hint-s">' + L("Arrossega el dibuix per a girar el cos. Les arestes ocultes es veuen discontínues.", "Arrastra el dibujo para girar el cuerpo. Las aristas ocultas se ven discontinuas.", "Drag the picture to rotate the solid. Hidden edges are dashed.") + '</p>'])
  + drill('euler', "Entrena: fórmula d'Euler", 'Entrena: fórmula de Euler', "Train: Euler's formula", 'int'))
assert 7 + 10 == 15 + 2
PLAT = [('tetra', 'Tetraedre', 'Tetraedro', 'Tetrahedron'), ('cub', 'Cub', 'Cubo', 'Cube'), ('octa', 'Octaedre', 'Octaedro', 'Octahedron'), ('dodeca', 'Dodecaedre', 'Dodecaedro', 'Dodecahedron'), ('ico', 'Icosaedre', 'Icosaedro', 'Icosahedron')]
s1 += box('def', L('Els poliedres regulars', 'Los poliedros regulares', 'The regular polyhedra'),
  P(r"Un poliedre convex és <strong>regular</strong> si totes les cares són polígons regulars iguals i a cada vèrtex concorre el mateix nombre de cares. Només n'hi ha <strong>cinc</strong> (els <em>sòlids platònics</em>):",
    r"Un poliedro convexo es <strong>regular</strong> si todas sus caras son polígonos regulares iguales y en cada vértice concurre el mismo número de caras. Solo hay <strong>cinco</strong> (los <em>sólidos platónicos</em>):",
    r"A convex polyhedron is <strong>regular</strong> if all its faces are equal regular polygons and the same number of faces meet at each vertex. There are only <strong>five</strong> (the <em>Platonic solids</em>):")
  + '<div class="figs plat">' + ''.join(G(polyhedron(platonic(k, 1))[0], W=110, maxh=110, pad=8, cap=L(va, es, en)) for k, va, es, en in PLAT) + '</div>'
  + tbl(['', 'C', 'V', 'A', L('Cares', 'Caras', 'Faces'), L('Cares per vèrtex', 'Caras por vértice', 'Faces per vertex')],
        [[L('Tetraedre', 'Tetraedro', 'Tetrahedron'), '4', '4', '6', L('triangles', 'triángulos', 'triangles'), '3'],
         [L('Cub (hexaedre)', 'Cubo (hexaedro)', 'Cube (hexahedron)'), '6', '8', '12', L('quadrats', 'cuadrados', 'squares'), '3'],
         [L('Octaedre', 'Octaedro', 'Octahedron'), '8', '6', '12', L('triangles', 'triángulos', 'triangles'), '4'],
         [L('Dodecaedre', 'Dodecaedro', 'Dodecahedron'), '12', '20', '30', L('pentàgons', 'pentágonos', 'pentagons'), '3'],
         [L('Icosaedre', 'Icosaedro', 'Icosahedron'), '20', '12', '30', L('triangles', 'triángulos', 'triangles'), '5']])
  + note(r"Per què només cinc? A cada vèrtex, els angles de les cares han de sumar <strong>menys de 360°</strong> (si no, quedarien planes). Amb triangles (60°) podem ajuntar-ne 3, 4 o 5; amb quadrats (90°), 3; amb pentàgons (108°), 3. Amb hexàgons (120°), tres ja sumen 360°.",
         r"¿Por qué solo cinco? En cada vértice, los ángulos de las caras deben sumar <strong>menos de 360°</strong> (si no, quedarían planas). Con triángulos (60°) podemos juntar 3, 4 o 5; con cuadrados (90°), 3; con pentágonos (108°), 3. Con hexágonos (120°), tres ya suman 360°.",
         r"Why only five? At each vertex the face angles must add up to <strong>less than 360°</strong> (otherwise they'd lie flat). With triangles (60°) we can join 3, 4 or 5; with squares (90°), 3; with pentagons (108°), 3. With hexagons (120°), three already make 360°.", '🤔'))
for C, V, A in [(4, 4, 6), (6, 8, 12), (8, 6, 12), (12, 20, 30), (20, 12, 30)]: assert C + V == A + 2
s1 += levels(
 [prob(L(r"Compta les cares, els vèrtexs i les arestes d'una piràmide hexagonal i comprova la fórmula d'Euler.", r"Cuenta las caras, los vértices y las aristas de una pirámide hexagonal y comprueba la fórmula de Euler.", r"Count the faces, vertices and edges of a hexagonal pyramid and check Euler's formula."),
       P(r"Base hexagonal + 6 triangles: \(C=7\). Vèrtexs: 6 de la base + el vèrtex de dalt: \(V=7\). Arestes: 6 de la base + 6 laterals: \(A=12\).", r"Base hexagonal + 6 triángulos: \(C=7\). Vértices: 6 de la base + el de arriba: \(V=7\). Aristas: 6 de la base + 6 laterales: \(A=12\).", r"Hexagonal base + 6 triangles: \(C=7\). Vertices: 6 on the base + the apex: \(V=7\). Edges: 6 on the base + 6 lateral: \(A=12\)."),
       D(r"C+V=7+7=14=12+2\ \checkmark"))],
 [prob(L(r"Un poliedre convex té 9 cares i 16 arestes. Quants vèrtexs té?", r"Un poliedro convexo tiene 9 caras y 16 aristas. ¿Cuántos vértices tiene?", r"A convex polyhedron has 9 faces and 16 edges. How many vertices does it have?"),
       D(r"9+V=16+2\ \Rightarrow\ V=\boxed{9}"),
       P(r"(Per exemple, una piràmide octogonal: base + 8 triangles, 8 + 1 vèrtexs, 16 arestes.)", r"(Por ejemplo, una pirámide octogonal: base + 8 triángulos, 8 + 1 vértices, 16 aristas.)", r"(For example, an octagonal pyramid: base + 8 triangles, 8 + 1 vertices, 16 edges.)"))],
 [prob(L(r"Un prisma té 30 arestes. Quantes cares i quants vèrtexs té? Quin polígon és la base?", r"Un prisma tiene 30 aristas. ¿Cuántas caras y cuántos vértices tiene? ¿Qué polígono es la base?", r"A prism has 30 edges. How many faces and vertices does it have? What polygon is its base?"),
       P(r"Si la base té \(n\) costats, el prisma té \(n+n+n=3n\) arestes (dues bases i les laterals), \(n+2\) cares i \(2n\) vèrtexs:", r"Si la base tiene \(n\) lados, el prisma tiene \(n+n+n=3n\) aristas (dos bases y las laterales), \(n+2\) caras y \(2n\) vértices:", r"If the base has \(n\) sides, the prism has \(n+n+n=3n\) edges (two bases and the lateral ones), \(n+2\) faces and \(2n\) vertices:"),
       D(r"3n=30\ \Rightarrow\ n=10:\quad C=\boxed{12},\quad V=\boxed{20},\quad\text{%s}" % Lt('base decagonal', 'base decagonal', 'decagonal base')),
       P(r"Comprovació: \(12+20=30+2\ \checkmark\)", r"Comprobación: \(12+20=30+2\ \checkmark\)", r"Check: \(12+20=30+2\ \checkmark\)"))])
assert 7 + 7 == 12 + 2 and 9 + 9 == 16 + 2 and 12 + 20 == 30 + 2
s1 += practice([
  ('★', L(r"a) Quantes cares, vèrtexs i arestes té un prisma triangular? b) I una piràmide quadrangular? Comprova la fórmula d'Euler.", r"a) ¿Cuántas caras, vértices y aristas tiene un prisma triangular? b) ¿Y una pirámide cuadrangular? Comprueba la fórmula de Euler.", r"a) How many faces, vertices and edges does a triangular prism have? b) And a square pyramid? Check Euler's formula.")),
  ('★★', L(r"c) Un poliedre convex té 8 vèrtexs i 12 arestes. Quantes cares té? d) Pot existir un poliedre convex amb 6 cares, 6 vèrtexs i 11 arestes?", r"c) Un poliedro convexo tiene 8 vértices y 12 aristas. ¿Cuántas caras tiene? d) ¿Puede existir un poliedro convexo con 6 caras, 6 vértices y 11 aristas?", r"c) A convex polyhedron has 8 vertices and 12 edges. How many faces does it have? d) Can a convex polyhedron have 6 faces, 6 vertices and 11 edges?")),
  ('★★★', L(r"e) Una piràmide té 24 arestes. Quin polígon té per base? Quantes cares i vèrtexs té?", r"e) Una pirámide tiene 24 aristas. ¿Qué polígono tiene por base? ¿Cuántas caras y vértices tiene?", r"e) A pyramid has 24 edges. What polygon is its base? How many faces and vertices does it have?"))],
  P(r"a) \(C=5,\ V=6,\ A=9\): \(5+6=9+2\). b) \(C=5,\ V=5,\ A=8\): \(5+5=8+2\). c) \(C=12+2-8=6\). d) No: \(6+6=12\neq13\). e) \(2n=24\Rightarrow n=12\): base dodecagonal, \(C=13\), \(V=13\).",
    r"a) \(C=5,\ V=6,\ A=9\): \(5+6=9+2\). b) \(C=5,\ V=5,\ A=8\): \(5+5=8+2\). c) \(C=12+2-8=6\). d) No: \(6+6=12\neq13\). e) \(2n=24\Rightarrow n=12\): base dodecagonal, \(C=13\), \(V=13\).",
    r"a) \(C=5,\ V=6,\ A=9\): \(5+6=9+2\). b) \(C=5,\ V=5,\ A=8\): \(5+5=8+2\). c) \(C=12+2-8=6\). d) No: \(6+6=12\neq13\). e) \(2n=24\Rightarrow n=12\): dodecagonal base, \(C=13\), \(V=13\)."))
assert 5 + 6 == 9 + 2 and 5 + 5 == 8 + 2 and 6 + 6 != 11 + 2 and 13 + 13 == 24 + 2

# =====================================================================
# 11.2 Prismes: elements i àrea
# =====================================================================
FP, _ = f_prism(6, 2, 3.4, ll='l', lh='h')
FO, _ = f_cuboid(4, 2.2, 3, la='a', lb='b', lc='c')
s2 = box('def', L('Prismes', 'Prismas', 'Prisms'),
  P(r"Un <strong>prisma</strong> és un poliedre que té dues cares iguals i paral·leles, les <strong>bases</strong>, i les altres cares (les <strong>cares laterals</strong>) són paral·lelograms. L'<strong>altura</strong> \(h\) és la distància entre les bases. El nom depén del polígon de la base: prisma triangular, quadrangular, pentagonal…",
    r"Un <strong>prisma</strong> es un poliedro que tiene dos caras iguales y paralelas, las <strong>bases</strong>, y las demás caras (las <strong>caras laterales</strong>) son paralelogramos. La <strong>altura</strong> \(h\) es la distancia entre las bases. El nombre depende del polígono de la base: prisma triangular, cuadrangular, pentagonal…",
    r"A <strong>prism</strong> is a polyhedron with two equal parallel faces, the <strong>bases</strong>, while the other faces (the <strong>lateral faces</strong>) are parallelograms. The <strong>height</strong> \(h\) is the distance between the bases. It's named after its base: triangular, square, pentagonal prism…")
  + ul(L(r"<strong>Recte</strong>: les cares laterals són rectangles (perpendiculars a les bases). Si no, és <strong>oblic</strong>.", r"<strong>Recto</strong>: las caras laterales son rectángulos (perpendiculares a las bases). Si no, es <strong>oblicuo</strong>.", r"<strong>Right</strong>: the lateral faces are rectangles (perpendicular to the bases). Otherwise it's <strong>oblique</strong>."),
       L(r"<strong>Regular</strong>: és recte i les bases són polígons regulars.", r"<strong>Regular</strong>: es recto y las bases son polígonos regulares.", r"<strong>Regular</strong>: it's right and its bases are regular polygons."),
       L(r"<strong>Paral·lelepípede</strong>: totes les cares són paral·lelograms. Si són rectangles, és un <strong>ortoedre</strong> (una caixa); si són quadrats, un <strong>cub</strong>.", r"<strong>Paralelepípedo</strong>: todas las caras son paralelogramos. Si son rectángulos, es un <strong>ortoedro</strong> (una caja); si son cuadrados, un <strong>cubo</strong>.", r"<strong>Parallelepiped</strong>: all faces are parallelograms. If they're rectangles it's a <strong>cuboid</strong> (a box); if they're squares, a <strong>cube</strong>."))
  + figs(solid(FP, cap=L('Prisma hexagonal regular', 'Prisma hexagonal regular', 'Regular hexagonal prism')), solid(FO, W=230, cap=L('Ortoedre', 'Ortoedro', 'Cuboid'))))
FD, _ = f_cuboid(4, 2.2, 3, la='a', lb='b', lc='c', diag=True)
s2 += box('prop', L("La diagonal d'un ortoedre", 'La diagonal de un ortoedro', 'The diagonal of a cuboid'),
  P(r"La diagonal \(D\) d'un ortoedre d'arestes \(a\), \(b\) i \(c\) es calcula aplicant Pitàgores dues vegades: primer la diagonal de la base, \(d^2=a^2+b^2\), i després \(D^2=d^2+c^2\):",
    r"La diagonal \(D\) de un ortoedro de aristas \(a\), \(b\) y \(c\) se calcula aplicando Pitágoras dos veces: primero la diagonal de la base, \(d^2=a^2+b^2\), y después \(D^2=d^2+c^2\):",
    r"The diagonal \(D\) of a cuboid with edges \(a\), \(b\) and \(c\) is found by applying Pythagoras twice: first the base diagonal, \(d^2=a^2+b^2\), then \(D^2=d^2+c^2\):")
  + figs(solid(FD, W=230))
  + D(r"D=\sqrt{a^2+b^2+c^2}\qquad\qquad a=3,\ b=4,\ c=12:\ \ D=\sqrt{9+16+144}=\sqrt{169}=13")
  + drill('diag', "Entrena: diagonal d'un ortoedre", 'Entrena: diagonal de un ortoedro', 'Train: diagonal of a cuboid'))
ck(S(9 + 16 + 144), 13)
s2 += box('prop', L("Àrea d'un prisma", 'Área de un prisma', 'Surface area of a prism'),
  P(r"Si despleguem un prisma recte obtenim el seu <strong>desenvolupament</strong>: un rectangle format per les cares laterals (de base el perímetre de la base i d'altura \(h\)) i els dos polígons de les bases. Per tant:",
    r"Si desplegamos un prisma recto obtenemos su <strong>desarrollo</strong>: un rectángulo formado por las caras laterales (de base el perímetro de la base y de altura \(h\)) y los dos polígonos de las bases. Por tanto:",
    r"Unfolding a right prism gives its <strong>net</strong>: a rectangle made of the lateral faces (as wide as the base perimeter and \(h\) tall) and the two base polygons. So:")
  + figs(G(net_prism(6, 2, 3.4), W=300, pad=12, cap=L('Desenvolupament del prisma hexagonal', 'Desarrollo del prisma hexagonal', 'Net of the hexagonal prism')))
  + D(r"A_L=P_{\text{base}}\cdot h\qquad\qquad A_T=A_L+2\,A_{\text{base}}")
  + P(r"Exemple: prisma hexagonal regular de \(l=4\) cm i \(h=10\) cm. L'apotema de la base, amb Pitàgores, és \(a=\sqrt{4^2-2^2}=\sqrt{12}\approx3{,}46\) cm.",
      r"Ejemplo: prisma hexagonal regular de \(l=4\) cm y \(h=10\) cm. La apotema de la base, con Pitágoras, es \(a=\sqrt{4^2-2^2}=\sqrt{12}\approx3{,}46\) cm.",
      r"Example: a regular hexagonal prism with \(l=4\) cm and \(h=10\) cm. By Pythagoras the base apothem is \(a=\sqrt{4^2-2^2}=\sqrt{12}\approx3.46\) cm.")
  + D(r"A_L=24\cdot10=240\ \text{cm}^2\qquad A_{\text{base}}=\frac{P\cdot a}{2}=\frac{24\cdot\sqrt{12}}{2}\approx41{,}57\ \text{cm}^2")
  + D(r"A_T\approx240+2\cdot41{,}57=323{,}14\ \text{cm}^2")
  + widget('w-prism', '📦', L('Prismes regulars: dibuix, desenvolupament i àrea', 'Prismas regulares: dibujo, desarrollo y área', 'Regular prisms: picture, net and area'),
           ['<div class="wrow">' + rng('n', 3, 8, 1, 6, 'n') + rng('l', 1, 10, 0.5, 4, 'l') + rng('h', 1, 15, 0.5, 10, 'h') + '</div>'],
           out='<div class="gout"></div><div class="hsteps"></div>')
  + drill('prisma', "Entrena: àrea d'un prisma", 'Entrena: área de un prisma', 'Train: surface area of a prism'))
ab = S(12); ck(ab, 3.46, 2); ck(24 * ab / 2, 41.57, 2); ck(240 + 24 * ab, 323.14, 2)
s2 += levels(
 [prob(L(r"Calcula l'àrea total d'un ortoedre de 8 cm × 5 cm × 3 cm i la d'un cub de 6 cm d'aresta.", r"Calcula el área total de un ortoedro de 8 cm × 5 cm × 3 cm y la de un cubo de 6 cm de arista.", r"Find the total surface area of an 8 cm × 5 cm × 3 cm cuboid and of a cube with 6 cm edges."),
       P(r"L'ortoedre té tres parelles de cares iguals:", r"El ortoedro tiene tres pares de caras iguales:", r"The cuboid has three pairs of equal faces:"),
       D(r"A_T=2(8\cdot5+8\cdot3+5\cdot3)=2(40+24+15)=\boxed{158\ \text{cm}^2}\qquad A_{\text{%s}}=6\cdot6^2=\boxed{216\ \text{cm}^2}" % Lt('cub', 'cubo', 'cube')))],
 [prob(L(r"Un prisma triangular regular té 6 cm d'aresta de la base i 15 cm d'altura. Calcula'n l'àrea lateral i l'àrea total.", r"Un prisma triangular regular tiene 6 cm de arista de la base y 15 cm de altura. Calcula su área lateral y su área total.", r"A regular triangular prism has 6 cm base edges and is 15 cm tall. Find its lateral and total surface area."),
       D(r"A_L=(3\cdot6)\cdot15=\boxed{270\ \text{cm}^2}"),
       P(r"La base és un triangle equilàter; la seua altura és \(\sqrt{6^2-3^2}=\sqrt{27}\approx5{,}20\) cm:", r"La base es un triángulo equilátero; su altura es \(\sqrt{6^2-3^2}=\sqrt{27}\approx5{,}20\) cm:", r"The base is an equilateral triangle; its height is \(\sqrt{6^2-3^2}=\sqrt{27}\approx5.20\) cm:"),
       D(r"A_{\text{base}}=\frac{6\cdot\sqrt{27}}{2}\approx15{,}59\ \text{cm}^2\qquad A_T\approx270+2\cdot15{,}59=\boxed{301{,}18\ \text{cm}^2}"))],
 [prob(L(r"Volem pintar les parets i el sostre d'una habitació de 5 m × 4 m i 2,5 m d'altura. La porta fa 0,8 m × 2 m i la finestra, 1,5 m × 1,2 m. Si un pot de pintura cobreix 12 m², quants pots hem de comprar?", r"Queremos pintar las paredes y el techo de una habitación de 5 m × 4 m y 2,5 m de altura. La puerta mide 0,8 m × 2 m y la ventana, 1,5 m × 1,2 m. Si un bote de pintura cubre 12 m², ¿cuántos botes hay que comprar?", r"We want to paint the walls and ceiling of a 5 m × 4 m room, 2.5 m high. The door is 0.8 m × 2 m and the window 1.5 m × 1.2 m. If a tin of paint covers 12 m², how many tins do we need?"),
       D(r"\text{%s}:\ 2(5+4)\cdot2{,}5=45\ \text{m}^2\qquad\text{%s}:\ 5\cdot4=20\ \text{m}^2" % (Lt('Parets', 'Paredes', 'Walls'), Lt('sostre', 'techo', 'ceiling'))),
       D(r"45+20-0{,}8\cdot2-1{,}5\cdot1{,}2=65-1{,}6-1{,}8=61{,}6\ \text{m}^2"),
       D(r"\frac{61{,}6}{12}\approx5{,}13\ \Rightarrow\ \boxed{6\ \text{%s}}" % Lt('pots', 'botes', 'tins')))])
ck(2 * (40 + 24 + 15), 158); ck(6 * 36, 216); ck(18 * 15, 270); ck(S(27), 5.20, 2); ck(6 * S(27) / 2, 15.59, 2); ck(270 + 6 * S(27), 301.18, 2); ck(R(616, 10) / 12, 5.13, 2)
s2 += practice([
  ('★', L(r"a) Calcula l'àrea total d'un cub de 5 cm d'aresta. b) I la d'un ortoedre de 10 × 4 × 6 cm.", r"a) Calcula el área total de un cubo de 5 cm de arista. b) Y la de un ortoedro de 10 × 4 × 6 cm.", r"a) Find the total area of a cube with 5 cm edges. b) And of a 10 × 4 × 6 cm cuboid.")),
  ('★★', L(r"c) Calcula la diagonal d'un ortoedre de 2 × 3 × 6 cm. d) Un prisma quadrangular regular té 3 cm d'aresta de la base i 8 cm d'altura. Calcula l'àrea total.", r"c) Calcula la diagonal de un ortoedro de 2 × 3 × 6 cm. d) Un prisma cuadrangular regular tiene 3 cm de arista de la base y 8 cm de altura. Calcula el área total.", r"c) Find the diagonal of a 2 × 3 × 6 cm cuboid. d) A regular square prism has 3 cm base edges and is 8 cm tall. Find its total area.")),
  ('★★★', L(r"e) Un cub té una diagonal de \(\sqrt{75}\) cm. Quant mesura l'aresta? Quina és l'àrea total?", r"e) Un cubo tiene una diagonal de \(\sqrt{75}\) cm. ¿Cuánto mide la arista? ¿Cuál es el área total?", r"e) A cube has a diagonal of \(\sqrt{75}\) cm. How long is its edge? What is its total area?"))],
  P(r"a) \(6\cdot25=150\) cm². b) \(2(40+60+24)=248\) cm². c) \(\sqrt{4+9+36}=7\) cm. d) \(12\cdot8+2\cdot9=114\) cm². e) \(3l^2=75\Rightarrow l=5\) cm; \(A=150\) cm².",
    r"a) \(6\cdot25=150\) cm². b) \(2(40+60+24)=248\) cm². c) \(\sqrt{4+9+36}=7\) cm. d) \(12\cdot8+2\cdot9=114\) cm². e) \(3l^2=75\Rightarrow l=5\) cm; \(A=150\) cm².",
    r"a) \(6\cdot25=150\) cm². b) \(2(40+60+24)=248\) cm². c) \(\sqrt{4+9+36}=7\) cm. d) \(12\cdot8+2\cdot9=114\) cm². e) \(3l^2=75\Rightarrow l=5\) cm; \(A=150\) cm²."))
assert 2 * (40 + 60 + 24) == 248 and 12 * 8 + 18 == 114; ck(S(49), 7)
