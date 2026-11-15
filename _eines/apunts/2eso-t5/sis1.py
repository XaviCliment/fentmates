# Apartats 5.1-5.3 dels apunts de la Unitat 5 de 2n ESO (Sistemes d'equacions): equacions amb dues incògnites,
# què és i què representa un sistema i mètode de substitució. Les solucions es comproven amb sympy (cs, ok, nok, same).
from comu import *

# =====================================================================
# 5.1 Equacions de primer grau amb dues incògnites
# =====================================================================
s1 = box('def', L('Una equació amb dues incògnites', 'Una ecuación con dos incógnitas', 'An equation with two unknowns'),
  P(r"Fins ara hem resolt equacions amb <strong>una</strong> incògnita, com \(2x+1=7\). Però hi ha situacions amb <strong>dues</strong> quantitats desconegudes. Per exemple: <em>«L'Anna i en Pau tenen 7 cromos entre els dos»</em>. Si \(x\) són els cromos de l'Anna i \(y\) els d'en Pau:",
    r"Hasta ahora hemos resuelto ecuaciones con <strong>una</strong> incógnita, como \(2x+1=7\). Pero hay situaciones con <strong>dos</strong> cantidades desconocidas. Por ejemplo: <em>«Ana y Pau tienen 7 cromos entre los dos»</em>. Si \(x\) son los cromos de Ana e \(y\) los de Pau:",
    r"So far we have solved equations with <strong>one</strong> unknown, like \(2x+1=7\). But some situations have <strong>two</strong> unknown quantities. For example: <em>“Anna and Pau have 7 stickers between them”</em>. If \(x\) is Anna's stickers and \(y\) is Pau's:")
  + D(r"x+y=7")
  + P(r"Una <strong>equació de primer grau</strong> (o lineal) <strong>amb dues incògnites</strong> és una equació que, un cop reduïda, es pot escriure així:",
      r"Una <strong>ecuación de primer grado</strong> (o lineal) <strong>con dos incógnitas</strong> es una ecuación que, una vez reducida, se puede escribir así:",
      r"A <strong>first-degree</strong> (linear) <strong>equation in two unknowns</strong> is one that, once simplified, can be written as:")
  + D(r"ax+by=c")
  + ul(L(r"\(x\) i \(y\) són les <strong>incògnites</strong>;", r"\(x\) e \(y\) son las <strong>incógnitas</strong>;", r"\(x\) and \(y\) are the <strong>unknowns</strong>;"),
       L(r"\(a\) i \(b\) són els <strong>coeficients</strong> (els nombres que multipliquen les incògnites);", r"\(a\) y \(b\) son los <strong>coeficientes</strong> (los números que multiplican a las incógnitas);", r"\(a\) and \(b\) are the <strong>coefficients</strong> (the numbers multiplying the unknowns);"),
       L(r"\(c\) és el <strong>terme independent</strong>.", r"\(c\) es el <strong>término independiente</strong>.", r"\(c\) is the <strong>constant term</strong>."))
  + P(r"Per exemple, \(2x+y=7\), \(x-3y=0\) o \(y=2x+1\) són equacions de primer grau amb dues incògnites. En canvi, \(x^2+y=5\) i \(xy=6\) <em>no</em> ho són: tenen termes de grau 2.",
      r"Por ejemplo, \(2x+y=7\), \(x-3y=0\) o \(y=2x+1\) son ecuaciones de primer grado con dos incógnitas. En cambio, \(x^2+y=5\) y \(xy=6\) <em>no</em> lo son: tienen términos de grado 2.",
      r"For example, \(2x+y=7\), \(x-3y=0\) and \(y=2x+1\) are first-degree equations in two unknowns. On the other hand, \(x^2+y=5\) and \(xy=6\) are <em>not</em>: they have terms of degree 2."))
s1 += box('def', L('Les solucions són parells de nombres', 'Las soluciones son pares de números', 'Solutions are pairs of numbers'),
  P(r"Una <strong>solució</strong> d'una equació amb dues incògnites és un <strong>parell de valors</strong> \((x,\,y)\) que fa certa la igualtat. Per a comprovar si un parell és solució, el substituïm i calculem:",
    r"Una <strong>solución</strong> de una ecuación con dos incógnitas es un <strong>par de valores</strong> \((x,\,y)\) que hace cierta la igualdad. Para comprobar si un par es solución, lo sustituimos y calculamos:",
    r"A <strong>solution</strong> of an equation in two unknowns is a <strong>pair of values</strong> \((x,\,y)\) that makes the equality true. To check whether a pair is a solution, substitute it and work it out:")
  + D(r"2x+y=7:\qquad (1,\,5)\to 2\cdot1+5=7\ \checkmark\qquad (3,\,1)\to 2\cdot3+1=7\ \checkmark\qquad (2,\,2)\to 2\cdot2+2=6\neq7\ \times")
  + note(r"L'ordre importa: en el parell \((1,\,5)\) el primer nombre és la \(x\) i el segon, la \(y\). El parell \((5,\,1)\) és un altre parell diferent: \(2\cdot5+1=11\neq7\), i no és solució.",
         r"El orden importa: en el par \((1,\,5)\) el primer número es la \(x\) y el segundo, la \(y\). El par \((5,\,1)\) es otro par distinto: \(2\cdot5+1=11\neq7\), y no es solución.",
         r"Order matters: in the pair \((1,\,5)\) the first number is \(x\) and the second is \(y\). The pair \((5,\,1)\) is a different one: \(2\cdot5+1=11\neq7\), so it isn't a solution.", '⚠'))
ok('2x+y=7', 1, 5); ok('2x+y=7', 3, 1); nok('2x+y=7', 2, 2); nok('2x+y=7', 5, 1)
s1 += box('prop', L('Infinites solucions: la taula de valors', 'Infinitas soluciones: la tabla de valores', 'Infinitely many solutions: the table of values'),
  P(r"Tornem als cromos: \(x+y=7\). L'Anna en pot tindre 0 i en Pau 7; o 1 i 6; o 2 i 5… Si deixem que \(x\) i \(y\) siguen qualsevol nombre (també negatius o decimals), hi ha <strong>infinites solucions</strong>: per a cada valor que donem a la \(x\), podem calcular el de la \(y\).",
    r"Volvamos a los cromos: \(x+y=7\). Ana puede tener 0 y Pau 7; o 1 y 6; o 2 y 5… Si dejamos que \(x\) e \(y\) sean cualquier número (también negativos o decimales), hay <strong>infinitas soluciones</strong>: para cada valor que demos a la \(x\), podemos calcular el de la \(y\).",
    r"Back to the stickers: \(x+y=7\). Anna could have 0 and Pau 7; or 1 and 6; or 2 and 5… If \(x\) and \(y\) can be any number (negative or decimal too), there are <strong>infinitely many solutions</strong>: for every value we give \(x\), we can work out \(y\).")
  + P(r"El més còmode és <strong>aïllar la \(y\)</strong> i fer una <strong>taula de valors</strong>:", r"Lo más cómodo es <strong>despejar la \(y\)</strong> y hacer una <strong>tabla de valores</strong>:", r"The easiest way is to <strong>isolate \(y\)</strong> and make a <strong>table of values</strong>:")
  + D(r"2x+y=7\ \Rightarrow\ y=7-2x")
  + tvc('2x+y=7', [-1, 0, 1, 2, 3, 4])
  + P(r"Cada columna de la taula és una solució: \((-1,\,9),\ (0,\,7),\ (1,\,5),\ (2,\,3)\ldots\)", r"Cada columna de la tabla es una solución: \((-1,\,9),\ (0,\,7),\ (1,\,5),\ (2,\,3)\ldots\)", r"Each column of the table is a solution: \((-1,\,9),\ (0,\,7),\ (1,\,5),\ (2,\,3)\ldots\)")
  + drill('val', 'Entrena: troba la y', 'Entrena: halla la y', 'Train: find y', opts=True))
s1 += box('prop', L('La gràfica és una recta', 'La gráfica es una recta', 'The graph is a straight line'),
  P(r"Si dibuixem les solucions com a punts \((x,\,y)\) en uns eixos de coordenades, queden <strong>alineades</strong>: la gràfica d'una equació de primer grau amb dues incògnites és una <strong>recta</strong>. Cada punt de la recta és una solució, i cada solució és un punt de la recta.",
    r"Si dibujamos las soluciones como puntos \((x,\,y)\) en unos ejes de coordenadas, quedan <strong>alineadas</strong>: la gráfica de una ecuación de primer grado con dos incógnitas es una <strong>recta</strong>. Cada punto de la recta es una solución, y cada solución es un punto de la recta.",
    r"If we plot the solutions as points \((x,\,y)\) on a pair of axes, they <strong>line up</strong>: the graph of a first-degree equation in two unknowns is a <strong>straight line</strong>. Every point on the line is a solution, and every solution is a point on the line.")
  + figs(svg_graph([(2, 1, 7)], [(v, 7 - 2 * v, 'pt p0', None) for v in [-1, 0, 1, 2, 3, 4]], R=10, cap=r'\(2x+y=7\)'))
  + note(r"Per a dibuixar una recta n'hi ha prou amb <strong>dos punts</strong> (un tercer serveix per a comprovar que no t'has equivocat). Tria valors de \(x\) que donen valors de \(y\) enters: és més fàcil situar els punts.",
         r"Para dibujar una recta basta con <strong>dos puntos</strong> (un tercero sirve para comprobar que no te has equivocado). Elige valores de \(x\) que den valores de \(y\) enteros: es más fácil situar los puntos.",
         r"Two points are <strong>enough</strong> to draw a line (a third one checks you haven't made a mistake). Choose values of \(x\) that give whole-number \(y\): the points are easier to plot.")
  + widget('w-line', '📈', L('Taula de valors i recta', 'Tabla de valores y recta', 'Table of values and line'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), '2x+y=7') + '</div>', HELP,
            quick([('x+y=7', 'x+y = 7'), ('2x+y=7', '2x+y = 7'), ('x-y=2', 'x−y = 2'), ('y=2x-3', 'y = 2x−3'), ('x+2y=4', 'x+2y = 4'), ('3x-y=0', '3x−y = 0')])],
           out='<div class="gout"></div>'))
s1 += levels(
 [prob(L(r"Quins d'aquests parells són solució de \(3x-y=5\)? \((2,\,1)\), \((0,\,-5)\), \((1,\,1)\), \((3,\,4)\).", r"¿Cuáles de estos pares son solución de \(3x-y=5\)? \((2,\,1)\), \((0,\,-5)\), \((1,\,1)\), \((3,\,4)\).", r"Which of these pairs are solutions of \(3x-y=5\)? \((2,\,1)\), \((0,\,-5)\), \((1,\,1)\), \((3,\,4)\)."),
       D(r"(2,1):\ 6-1=5\ \checkmark\qquad (0,-5):\ 0-(-5)=5\ \checkmark\qquad (1,1):\ 3-1=2\neq5\ \times\qquad (3,4):\ 9-4=5\ \checkmark"),
       P(r"Són solució \((2,\,1)\), \((0,\,-5)\) i \((3,\,4)\).", r"Son solución \((2,\,1)\), \((0,\,-5)\) y \((3,\,4)\).", r"\((2,\,1)\), \((0,\,-5)\) and \((3,\,4)\) are solutions.")),
  prob(L(r"Escriu tres solucions de \(x+2y=8\).", r"Escribe tres soluciones de \(x+2y=8\).", r"Write three solutions of \(x+2y=8\)."),
       P(r"Ací és més fàcil aïllar la \(x\): \(x=8-2y\). Donem valors a la \(y\):", r"Aquí es más fácil despejar la \(x\): \(x=8-2y\). Damos valores a la \(y\):", r"Here it's easier to isolate \(x\): \(x=8-2y\). Give values to \(y\):"),
       D(r"y=0\to x=8;\qquad y=1\to x=6;\qquad y=3\to x=2"),
       P(r"Per exemple, \((8,\,0)\), \((6,\,1)\) i \((2,\,3)\). N'hi ha moltes més!", r"Por ejemplo, \((8,\,0)\), \((6,\,1)\) y \((2,\,3)\). ¡Hay muchas más!", r"For example, \((8,\,0)\), \((6,\,1)\) and \((2,\,3)\). There are many more!"))],
 [prob(L(r"Fes una taula de valors i representa la recta \(y=2x-3\).", r"Haz una tabla de valores y representa la recta \(y=2x-3\).", r"Make a table of values and draw the line \(y=2x-3\)."),
       P(r"La \(y\) ja està aïllada. Donem valors a la \(x\):", r"La \(y\) ya está despejada. Damos valores a la \(x\):", r"\(y\) is already isolated. Give values to \(x\):")
       + tvc('y=2x-3', [-1, 0, 1, 2, 3]),
       figs(svg_graph([(-2, 1, -3)], [(v, 2 * v - 3, 'pt p0', None) for v in [-1, 0, 1, 2, 3]], R=6))),
  prob(L(r"Troba \(k\) perquè el parell \((2,\,-1)\) siga solució de \(kx+3y=5\).", r"Halla \(k\) para que el par \((2,\,-1)\) sea solución de \(kx+3y=5\).", r"Find \(k\) so that \((2,\,-1)\) is a solution of \(kx+3y=5\)."),
       P(r"Substituïm \(x=2\) i \(y=-1\) i resolem l'equació que queda, amb la incògnita \(k\):", r"Sustituimos \(x=2\) e \(y=-1\) y resolvemos la ecuación que queda, con la incógnita \(k\):", r"Substitute \(x=2\) and \(y=-1\) and solve the resulting equation for \(k\):"),
       D(r"k\cdot2+3\cdot(-1)=5\ \Rightarrow\ 2k-3=5\ \Rightarrow\ 2k=8\ \Rightarrow\ \boxed{k=4}"))],
 [prob(L(r"Troba la solució de \(x+y=10\) en què la \(x\) és el quàdruple de la \(y\).", r"Halla la solución de \(x+y=10\) en la que la \(x\) es el cuádruple de la \(y\).", r"Find the solution of \(x+y=10\) where \(x\) is four times \(y\)."),
       P(r"Si \(x=4y\), substituïm en l'equació:", r"Si \(x=4y\), sustituimos en la ecuación:", r"If \(x=4y\), substitute into the equation:"),
       D(r"4y+y=10\ \Rightarrow\ 5y=10\ \Rightarrow\ y=2,\quad x=4\cdot2=8"),
       P(r"La solució és \((8,\,2)\): \(8+2=10\) ✓. Fixa't que hem fet servir <em>dues</em> condicions alhora: això és un <strong>sistema d'equacions</strong>, que estudiem en el pròxim apartat!", r"La solución es \((8,\,2)\): \(8+2=10\) ✓. Fíjate en que hemos usado <em>dos</em> condiciones a la vez: esto es un <strong>sistema de ecuaciones</strong>, ¡que estudiamos en el próximo apartado!", r"The solution is \((8,\,2)\): \(8+2=10\) ✓. Notice we used <em>two</em> conditions at once: that's a <strong>system of equations</strong>, which we study in the next section!"))])
ok('3x-y=5', 2, 1); ok('3x-y=5', 0, -5); nok('3x-y=5', 1, 1); ok('3x-y=5', 3, 4); ok('x+2y=8', 8, 0); ok('x+2y=8', 6, 1); ok('x+2y=8', 2, 3)
ok('4x+3y=5', 2, -1); cs('x+y=10', 'x=4y', (8, 2))
s1 += practice([
  ('★', L(r"a) És \((-1,\,4)\) solució de \(5x+2y=3\)? b) I \((1,\,2)\)?", r"a) ¿Es \((-1,\,4)\) solución de \(5x+2y=3\)? b) ¿Y \((1,\,2)\)?", r"a) Is \((-1,\,4)\) a solution of \(5x+2y=3\)? b) What about \((1,\,2)\)?")),
  ('★★', L(r"c) Fes una taula de valors de \(x-y=2\) i representa-la. d) Troba \(m\) perquè \((3,\,{m})\) siga solució de \(2x-5y=1\).", r"c) Haz una tabla de valores de \(x-y=2\) y represéntala. d) Halla \(m\) para que \((3,\,{m})\) sea solución de \(2x-5y=1\).", r"c) Make a table of values for \(x-y=2\) and draw it. d) Find \(m\) so that \((3,\,{m})\) is a solution of \(2x-5y=1\).")),
  ('★★★', L(r"e) Escriu totes les solucions de \(x+y=4\) en què \(x\) i \(y\) són nombres naturals (incloent-hi el 0).", r"e) Escribe todas las soluciones de \(x+y=4\) en las que \(x\) e \(y\) son números naturales (incluido el 0).", r"e) Write all the solutions of \(x+y=4\) where \(x\) and \(y\) are natural numbers (including 0)."))],
  D(r"\text{a)}\ 5\cdot(-1)+2\cdot4=3\ \checkmark\ \text{%s}\qquad \text{b)}\ 5+4=9\neq3\ \text{%s}" % (Lt('sí', 'sí', 'yes'), Lt('no', 'no', 'no')))
  + P(r"c) \(y=x-2\):", r"c) \(y=x-2\):", r"c) \(y=x-2\):") + tvc('x-y=2', [0, 1, 2, 3, 4])
  + D(r"\text{d)}\ 6-5m=1\Rightarrow -5m=-5\Rightarrow m=1\qquad \text{e)}\ (0,4),\ (1,3),\ (2,2),\ (3,1),\ (4,0)"))
ok('5x+2y=3', -1, 4); nok('5x+2y=3', 1, 2); ok('2x-5y=1', 3, 1)
for i in range(5): ok('x+y=4', i, 4 - i)

# =====================================================================
# 5.2 Sistemes de dues equacions amb dues incògnites
# =====================================================================
s2 = box('def', L("Què és un sistema d'equacions?", '¿Qué es un sistema de ecuaciones?', 'What is a system of equations?'),
  P(r"Tornem als cromos de l'Anna i en Pau. Ara sabem dues coses: <em>«entre els dos en tenen 7»</em> i <em>«l'Anna en té 1 més que en Pau»</em>. Cada frase és una equació:",
    r"Volvamos a los cromos de Ana y Pau. Ahora sabemos dos cosas: <em>«entre los dos tienen 7»</em> y <em>«Ana tiene 1 más que Pau»</em>. Cada frase es una ecuación:",
    r"Back to Anna's and Pau's stickers. Now we know two things: <em>“together they have 7”</em> and <em>“Anna has 1 more than Pau”</em>. Each sentence is an equation:")
  + D(SY(r"x+y=7", r"x-y=1"))
  + P(r"Un <strong>sistema de dues equacions amb dues incògnites</strong> és un conjunt de dues equacions de les quals busquem les <strong>solucions comunes</strong>. S'escriu amb una clau. La forma general és:",
      r"Un <strong>sistema de dos ecuaciones con dos incógnitas</strong> es un conjunto de dos ecuaciones de las que buscamos las <strong>soluciones comunes</strong>. Se escribe con una llave. La forma general es:",
      r"A <strong>system of two equations in two unknowns</strong> is a set of two equations whose <strong>common solutions</strong> we look for. It is written with a brace. The general form is:")
  + D(SY(r"ax+by=c", r"a'x+b'y=c'"))
  + P(r"La <strong>solució del sistema</strong> és el parell \((x,\,y)\) que compleix <strong>les dues equacions alhora</strong>. <strong>Resoldre</strong> un sistema és trobar-ne la solució.",
      r"La <strong>solución del sistema</strong> es el par \((x,\,y)\) que cumple <strong>las dos ecuaciones a la vez</strong>. <strong>Resolver</strong> un sistema es hallar su solución.",
      r"The <strong>solution of the system</strong> is the pair \((x,\,y)\) that satisfies <strong>both equations at once</strong>. <strong>Solving</strong> a system means finding its solution."))
cs('x+y=7', 'x-y=1', (4, 3))
s2 += box('prop', L('Buscant la solució comuna amb taules', 'Buscando la solución común con tablas', 'Finding the common solution with tables'),
  P(r"Fem una taula de valors de cada equació i busquem el parell que apareix en les dues:", r"Hacemos una tabla de valores de cada ecuación y buscamos el par que aparece en las dos:", r"Make a table of values for each equation and look for the pair that appears in both:")
  + '<div class="tv2">' + tvc('x+y=7', [1, 2, 3, 4, 5], 't0') + tvc('x-y=1', [1, 2, 3, 4, 5], 't1') + '</div>'
  + P(r"El parell \((4,\,3)\) és en les dues taules: \(4+3=7\) ✓ i \(4-3=1\) ✓. L'Anna té <strong>4 cromos</strong> i en Pau, <strong>3</strong>. En canvi, \((5,\,2)\) només compleix la primera: \(5-2=3\neq1\).",
      r"El par \((4,\,3)\) está en las dos tablas: \(4+3=7\) ✓ y \(4-3=1\) ✓. Ana tiene <strong>4 cromos</strong> y Pau, <strong>3</strong>. En cambio, \((5,\,2)\) solo cumple la primera: \(5-2=3\neq1\).",
      r"The pair \((4,\,3)\) is in both tables: \(4+3=7\) ✓ and \(4-3=1\) ✓. Anna has <strong>4 stickers</strong> and Pau <strong>3</strong>. On the other hand, \((5,\,2)\) only satisfies the first: \(5-2=3\neq1\).")
  + note(r"Buscar en taules funciona quan la solució està formada per nombres petits i enters, però no sempre és així. Per això aprendrem <strong>mètodes</strong> que funcionen sempre.",
         r"Buscar en tablas funciona cuando la solución está formada por números pequeños y enteros, pero no siempre es así. Por eso aprenderemos <strong>métodos</strong> que funcionan siempre.",
         r"Searching tables works when the solution is made of small whole numbers, but that isn't always the case. That's why we'll learn <strong>methods</strong> that always work."))
nok('x-y=1', 5, 2)
s2 += box('prop', L('Què representa un sistema? Dues rectes', '¿Qué representa un sistema? Dos rectas', 'What does a system represent? Two lines'),
  P(r"Cada equació és una recta. La solució del sistema és un punt que està en <strong>les dues rectes</strong> alhora: el <strong>punt de tall</strong>.",
    r"Cada ecuación es una recta. La solución del sistema es un punto que está en <strong>las dos rectas</strong> a la vez: el <strong>punto de corte</strong>.",
    r"Each equation is a line. The solution of the system is a point lying on <strong>both lines</strong>: the <strong>crossing point</strong>.")
  + figs(svg_graph([(1, 1, 7), (1, -1, 1)], [(4, 3, 'cut', '(4, 3)')], R=8, cap=r'\(x+y=7\ \) i \(\ x-y=1\)'))
  + note(r"Abans de resoldre un sistema, convé escriure cada equació en la <strong>forma reduïda</strong> \(ax+by=c\): les incògnites al primer membre, ordenades (primer la \(x\) i després la \(y\)), i el nombre al segon membre.",
         r"Antes de resolver un sistema, conviene escribir cada ecuación en la <strong>forma reducida</strong> \(ax+by=c\): las incógnitas en el primer miembro, ordenadas (primero la \(x\) y después la \(y\)), y el número en el segundo miembro.",
         r"Before solving a system, write each equation in <strong>standard form</strong> \(ax+by=c\): the unknowns on the left, in order (first \(x\), then \(y\)), and the number on the right."))
s2 += box('prop', L('Com resoldrem els sistemes?', '¿Cómo resolveremos los sistemas?', 'How will we solve systems?'),
  P(r"La idea dels mètodes algebraics és sempre la mateixa: <strong>eliminar una incògnita</strong> per a obtindre una equació de primer grau amb una sola incògnita, que ja sabem resoldre (unitat 4). Veurem tres mètodes algebraics, <strong>substitució</strong>, <strong>igualació</strong> i <strong>reducció</strong>, i el <strong>mètode gràfic</strong>. Tots donen la mateixa solució.",
    r"La idea de los métodos algebraicos es siempre la misma: <strong>eliminar una incógnita</strong> para obtener una ecuación de primer grado con una sola incógnita, que ya sabemos resolver (unidad 4). Veremos tres métodos algebraicos, <strong>sustitución</strong>, <strong>igualación</strong> y <strong>reducción</strong>, y el <strong>método gráfico</strong>. Todos dan la misma solución.",
    r"The algebraic methods always share one idea: <strong>eliminate one unknown</strong> to get a first-degree equation in a single unknown, which we already know how to solve (unit 4). We'll see three algebraic methods, <strong>substitution</strong>, <strong>equalisation</strong> and <strong>elimination</strong>, plus the <strong>graphical method</strong>. They all give the same solution.")
  + widget('w-pair', '🔍', L('És solució del sistema?', '¿Es solución del sistema?', 'Is it a solution of the system?'),
           [two('x+y=7', 'x-y=1'), '<div class="wrow">' + tin('x', 'x =', '4', 's') + tin('y', 'y =', '3', 's') + '</div>', HELP,
            quick([('x+y=7|x-y=1|4|3', '(4, 3)'), ('x+y=7|x-y=1|5|2', '(5, 2)'), ('2x+3y=4|x-y=7|5|-2', '2x+3y=4, x−y=7: (5, −2)'), ('3x-2y=1|x+y=2|1|1', '3x−2y=1, x+y=2: (1, 1)'), ('x+2y=5|2x-y=5|1|2', 'x+2y=5, 2x−y=5: (1, 2)')])])
  + drill('pair', 'Entrena: és solució?', 'Entrena: ¿es solución?', 'Train: is it a solution?', opts=True))
ok('2x+3y=4', 5, -2); ok('x-y=7', 5, -2); cs('3x-2y=1', 'x+y=2', (1, 1)); ok('x+2y=5', 1, 2); nok('2x-y=5', 1, 2)
s2 += levels(
 [prob(L(r"Comprova si \((2,\,-1)\) és solució del sistema \(" + SY('3x+2y=4', 'x-y=3') + r"\).", r"Comprueba si \((2,\,-1)\) es solución del sistema \(" + SY('3x+2y=4', 'x-y=3') + r"\).", r"Check whether \((2,\,-1)\) is a solution of the system \(" + SY('3x+2y=4', 'x-y=3') + r"\)."),
       D(r"3\cdot2+2\cdot(-1)=6-2=4\ \checkmark\qquad 2-(-1)=2+1=3\ \checkmark"),
       P(r"Compleix les dues equacions: <strong>sí</strong> que és solució.", r"Cumple las dos ecuaciones: <strong>sí</strong> es solución.", r"It satisfies both equations: it <strong>is</strong> a solution.")),
  prob(L(r"Escriu el sistema: <em>«Dos nombres sumen 12 i el primer és el doble del segon»</em>. Comprova que \((8,\,4)\) és la solució.", r"Escribe el sistema: <em>«Dos números suman 12 y el primero es el doble del segundo»</em>. Comprueba que \((8,\,4)\) es la solución.", r"Write the system: <em>“Two numbers add up to 12 and the first is twice the second”</em>. Check that \((8,\,4)\) is the solution."),
       P(r"Si \(x\) és el primer nombre i \(y\) el segon:", r"Si \(x\) es el primer número e \(y\) el segundo:", r"If \(x\) is the first number and \(y\) the second:"),
       D(SY('x+y=12', 'x=2y') + r"\qquad 8+4=12\ \checkmark,\qquad 8=2\cdot4\ \checkmark"))],
 [prob(L(r"Quin d'aquests parells és la solució del sistema \(" + SY('x+2y=5', '2x-y=5') + r"\)? \((1,\,2)\), \((3,\,1)\), \((5,\,0)\).", r"¿Cuál de estos pares es la solución del sistema \(" + SY('x+2y=5', '2x-y=5') + r"\)? \((1,\,2)\), \((3,\,1)\), \((5,\,0)\).", r"Which of these pairs is the solution of the system \(" + SY('x+2y=5', '2x-y=5') + r"\)? \((1,\,2)\), \((3,\,1)\), \((5,\,0)\)."),
       D(r"(1,2):\ 1+4=5\ \checkmark,\ \ 2-2=0\ \times\qquad (3,1):\ 3+2=5\ \checkmark,\ \ 6-1=5\ \checkmark\qquad (5,0):\ 5\ \checkmark,\ \ 10\ \times"),
       P(r"Els tres compleixen la primera, però només \((3,\,1)\) compleix les dues: és la solució.", r"Los tres cumplen la primera, pero solo \((3,\,1)\) cumple las dos: es la solución.", r"All three satisfy the first, but only \((3,\,1)\) satisfies both: it's the solution."))],
 [prob(L(r"Troba \(a\) i \(b\) perquè \((2,\,-1)\) siga la solució de \(" + SY('ax+3y=5', '2x+by=7') + r"\).", r"Halla \(a\) y \(b\) para que \((2,\,-1)\) sea la solución de \(" + SY('ax+3y=5', '2x+by=7') + r"\).", r"Find \(a\) and \(b\) so that \((2,\,-1)\) is the solution of \(" + SY('ax+3y=5', '2x+by=7') + r"\)."),
       D(r"2a+3\cdot(-1)=5\ \Rightarrow\ 2a=8\ \Rightarrow\ \boxed{a=4}"),
       D(r"2\cdot2+b\cdot(-1)=7\ \Rightarrow\ 4-b=7\ \Rightarrow\ \boxed{b=-3}"))])
cs('3x+2y=4', 'x-y=3', (2, -1)); cs('x+y=12', 'x=2y', (8, 4)); cs('x+2y=5', '2x-y=5', (3, 1)); ok('x+2y=5', 1, 2); ok('x+2y=5', 5, 0); cs('4x+3y=5', '2x-3y=7', (2, -1))
s2 += practice([
  ('★', L(r"a) És \((1,\,4)\) solució de \(" + SY('2x+y=6', 'x-y=-3') + r"\)?", r"a) ¿Es \((1,\,4)\) solución de \(" + SY('2x+y=6', 'x-y=-3') + r"\)?", r"a) Is \((1,\,4)\) a solution of \(" + SY('2x+y=6', 'x-y=-3') + r"\)?")),
  ('★★', L(r"b) Comprova quin dels parells \((0,\,3)\), \((2,\,1)\) i \((-1,\,5)\) és la solució de \(" + SY('2x+y=3', 'x+y=4') + r"\).", r"b) Comprueba cuál de los pares \((0,\,3)\), \((2,\,1)\) y \((-1,\,5)\) es la solución de \(" + SY('2x+y=3', 'x+y=4') + r"\).", r"b) Check which of \((0,\,3)\), \((2,\,1)\) and \((-1,\,5)\) is the solution of \(" + SY('2x+y=3', 'x+y=4') + r"\).")),
  ('★★★', L(r"c) Escriu un sistema que tinga la solució \((3,\,-2)\).", r"c) Escribe un sistema que tenga la solución \((3,\,-2)\).", r"c) Write a system whose solution is \((3,\,-2)\)."))],
  D(r"\text{a)}\ 2+4=6\ \checkmark,\ \ 1-4=-3\ \checkmark:\ \text{%s}\qquad \text{b)}\ (-1,\,5):\ -2+5=3\ \checkmark,\ \ -1+5=4\ \checkmark" % Lt('sí', 'sí', 'yes'))
  + P(r"c) Per exemple, \(x+y=1\) i \(x-y=5\): \(3+(-2)=1\) i \(3-(-2)=5\) (hi ha infinites respostes possibles).", r"c) Por ejemplo, \(x+y=1\) y \(x-y=5\): \(3+(-2)=1\) y \(3-(-2)=5\) (hay infinitas respuestas posibles).", r"c) For example, \(x+y=1\) and \(x-y=5\): \(3+(-2)=1\) and \(3-(-2)=5\) (there are infinitely many possible answers)."))
cs('2x+y=6', 'x-y=-3', (1, 4)); cs('2x+y=3', 'x+y=4', (-1, 5)); nok('x+y=4', 0, 3); nok('2x+y=3', 2, 1); cs('x+y=1', 'x-y=5', (3, -2))

# =====================================================================
# 5.3 Mètode de substitució
# =====================================================================
s3 = box('prop', L('Mètode de substitució', 'Método de sustitución', 'Substitution method'),
  ol(L(r"<strong>Aïllem</strong> una incògnita en una de les equacions (la més fàcil: la que té coeficient \(1\) o \(-1\)).", r"<strong>Despejamos</strong> una incógnita en una de las ecuaciones (la más fácil: la que tiene coeficiente \(1\) o \(-1\)).", r"<strong>Isolate</strong> one unknown in one of the equations (the easiest: one with coefficient \(1\) or \(-1\))."),
     L(r"<strong>Substituïm</strong> l'expressió obtinguda en l'<strong>altra</strong> equació. Queda una equació amb una sola incògnita.", r"<strong>Sustituimos</strong> la expresión obtenida en la <strong>otra</strong> ecuación. Queda una ecuación con una sola incógnita.", r"<strong>Substitute</strong> that expression into the <strong>other</strong> equation. You get an equation in a single unknown."),
     L(r"<strong>Resolem</strong> aquesta equació.", r"<strong>Resolvemos</strong> esta ecuación.", r"<strong>Solve</strong> that equation."),
     L(r"<strong>Substituïm</strong> el valor trobat en l'expressió aïllada per a calcular l'altra incògnita.", r"<strong>Sustituimos</strong> el valor hallado en la expresión despejada para calcular la otra incógnita.", r"<strong>Substitute</strong> the value back into the isolated expression to find the other unknown."),
     L(r"<strong>Comprovem</strong> la solució en les dues equacions.", r"<strong>Comprobamos</strong> la solución en las dos ecuaciones.", r"<strong>Check</strong> the solution in both equations."))
  + D(SY('2x+y=7', '3x-2y=7'))
  + D(r"\text{1. }y=7-2x\qquad \text{2. }3x-2(7-2x)=7")
  + D(r"\text{3. }3x-14+4x=7\ \Rightarrow\ 7x=21\ \Rightarrow\ x=3\qquad \text{4. }y=7-2\cdot3=1")
  + P(r"5. Comprovació: \(2\cdot3+1=7\) ✓ i \(3\cdot3-2\cdot1=7\) ✓. La solució és \(x=3,\ y=1\).", r"5. Comprobación: \(2\cdot3+1=7\) ✓ y \(3\cdot3-2\cdot1=7\) ✓. La solución es \(x=3,\ y=1\).", r"5. Check: \(2\cdot3+1=7\) ✓ and \(3\cdot3-2\cdot1=7\) ✓. The solution is \(x=3,\ y=1\).")
  + note(r"Quan substituïm, l'expressió va sempre <strong>entre parèntesis</strong>: \(-2(7-2x)=-14+4x\). Si oblidem el parèntesi, el \(-2\) només multiplicaria el 7 i el resultat eixiria malament.",
         r"Cuando sustituimos, la expresión va siempre <strong>entre paréntesis</strong>: \(-2(7-2x)=-14+4x\). Si olvidamos el paréntesis, el \(-2\) solo multiplicaría al 7 y el resultado saldría mal.",
         r"When substituting, the expression always goes <strong>in brackets</strong>: \(-2(7-2x)=-14+4x\). Without the bracket, the \(-2\) would only multiply the 7 and the answer would come out wrong.", '⚠')
  + note(r"El mètode de substitució és el més còmode quan alguna incògnita té coeficient \(1\) o \(-1\), o quan ja està aïllada (per exemple, \(y=3x-2\)).",
         r"El método de sustitución es el más cómodo cuando alguna incógnita tiene coeficiente \(1\) o \(-1\), o cuando ya está despejada (por ejemplo, \(y=3x-2\)).",
         r"Substitution is easiest when one unknown has coefficient \(1\) or \(-1\), or is already isolated (e.g. \(y=3x-2\))."))
cs('2x+y=7', '3x-2y=7', (3, 1)); same('3x-2(7-2x)=7', '7x=21')
s3 += solver('w-sub', 'sub', L('Substitució pas a pas', 'Sustitución paso a paso', 'Substitution step by step'), '2x+y=7', '3x-2y=7',
             [('2x+y=7', '3x-2y=7'), ('x=2y', 'x+y=9'), ('x-2y=1', '3x+y=10'), ('y=3x-1', '2x+y=9'), ('x+y=8', 'x-y=2'), ('4x-y=5', '3x+2y=12')])
s3 += drill('sub', 'Entrena: mètode de substitució', 'Entrena: método de sustitución', 'Train: substitution method')
s3 += levels(
 [prob(L(r"Resol \(" + SY('x=2y', 'x+y=9') + r"\).", r"Resuelve \(" + SY('x=2y', 'x+y=9') + r"\).", r"Solve \(" + SY('x=2y', 'x+y=9') + r"\)."),
       P(r"La \(x\) ja està aïllada: la substituïm en la segona equació.", r"La \(x\) ya está despejada: la sustituimos en la segunda ecuación.", r"\(x\) is already isolated: substitute it into the second equation."),
       D(R([r"2y+y=9", r"3y=9", r"y=3"]) + r"\qquad x=2\cdot3=6\qquad " + BX(6, 3))),
  prob(L(r"Resol \(" + SY('x+y=8', 'x-y=2') + r"\).", r"Resuelve \(" + SY('x+y=8', 'x-y=2') + r"\).", r"Solve \(" + SY('x+y=8', 'x-y=2') + r"\)."),
       P(r"Aïllem la \(x\) de la primera i la substituïm en la segona:", r"Despejamos la \(x\) de la primera y la sustituimos en la segunda:", r"Isolate \(x\) in the first and substitute into the second:"),
       D(r"x=8-y\ \Rightarrow\ (8-y)-y=2\ \Rightarrow\ -2y=-6\ \Rightarrow\ y=3"),
       D(r"x=8-3=5\qquad " + BX(5, 3)))],
 [prob(L(r"Resol \(" + SY('3x+y=11', '5x-2y=0') + r"\).", r"Resuelve \(" + SY('3x+y=11', '5x-2y=0') + r"\).", r"Solve \(" + SY('3x+y=11', '5x-2y=0') + r"\)."),
       D(r"y=11-3x\ \Rightarrow\ 5x-2(11-3x)=0"),
       D(R([r"5x-22+6x=0", r"11x=22", r"x=2"]) + r"\qquad y=11-3\cdot2=5"),
       P(r"Comprovació: \(6+5=11\) ✓; \(10-10=0\) ✓. Solució: \(x=2,\ y=5\).", r"Comprobación: \(6+5=11\) ✓; \(10-10=0\) ✓. Solución: \(x=2,\ y=5\).", r"Check: \(6+5=11\) ✓; \(10-10=0\) ✓. Solution: \(x=2,\ y=5\)."))],
 [prob(L(r"Resol \(" + SY('2x+3y=-1', 'x-2y=3') + r"\). Compte amb els signes!", r"Resuelve \(" + SY('2x+3y=-1', 'x-2y=3') + r"\). ¡Cuidado con los signos!", r"Solve \(" + SY('2x+3y=-1', 'x-2y=3') + r"\). Watch the signs!"),
       P(r"La \(x\) de la segona equació té coeficient 1: \(x=3+2y\).", r"La \(x\) de la segunda ecuación tiene coeficiente 1: \(x=3+2y\).", r"The \(x\) in the second equation has coefficient 1: \(x=3+2y\)."),
       D(R([r"2(3+2y)+3y=-1", r"6+4y+3y=-1", r"7y=-7", r"y=-1"])),
       D(r"x=3+2\cdot(-1)=3-2=1\qquad " + BX(1, -1)),
       P(r"Comprovació: \(2-3=-1\) ✓; \(1+2=3\) ✓.", r"Comprobación: \(2-3=-1\) ✓; \(1+2=3\) ✓.", r"Check: \(2-3=-1\) ✓; \(1+2=3\) ✓."))])
cs('x=2y', 'x+y=9', (6, 3)); cs('x+y=8', 'x-y=2', (5, 3)); cs('3x+y=11', '5x-2y=0', (2, 5)); same('5x-2(11-3x)=0', '11x=22'); cs('2x+3y=-1', 'x-2y=3', (1, -1)); same('2(3+2y)+3y=-1', '7y=-7')
s3 += practice([
  ('★', L(r"a) \(" + SY('y=x+3', '2x+y=9') + r"\) b) \(" + SY('x-2y=1', '3x+y=10') + r"\)", r"a) \(" + SY('y=x+3', '2x+y=9') + r"\) b) \(" + SY('x-2y=1', '3x+y=10') + r"\)", r"a) \(" + SY('y=x+3', '2x+y=9') + r"\) b) \(" + SY('x-2y=1', '3x+y=10') + r"\)")),
  ('★★', L(r"c) \(" + SY('4x-y=5', '3x+2y=12') + r"\)", r"c) \(" + SY('4x-y=5', '3x+2y=12') + r"\)", r"c) \(" + SY('4x-y=5', '3x+2y=12') + r"\)")),
  ('★★★', L(r"d) \(" + SY('3x-4y=10', 'x+y=1') + r"\)", r"d) \(" + SY('3x-4y=10', 'x+y=1') + r"\)", r"d) \(" + SY('3x-4y=10', 'x+y=1') + r"\)"))],
  D(r"\text{a)}\ 2x+x+3=9\Rightarrow x=2,\ y=5\qquad \text{b)}\ x=1+2y\Rightarrow 3+6y+y=10\Rightarrow y=1,\ x=3")
  + D(r"\text{c)}\ y=4x-5\Rightarrow 3x+8x-10=12\Rightarrow x=2,\ y=3")
  + D(r"\text{d)}\ y=1-x\Rightarrow 3x-4+4x=10\Rightarrow 7x=14\Rightarrow x=2,\ y=-1"))
cs('y=x+3', '2x+y=9', (2, 5)); cs('x-2y=1', '3x+y=10', (3, 1)); cs('4x-y=5', '3x+2y=12', (2, 3)); cs('3x-4y=10', 'x+y=1', (2, -1)); same('3x-4(1-x)=10', '7x=14')
