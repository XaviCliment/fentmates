# Apartats 10.6-10.7 dels apunts de la Unitat 10 de 2n ESO (Funcions): funcions lineals y = mx + n i funcions constants y = k.
# Cada resultat es comprova amb ck() i lin() (fraccions exactes).
from comu import *

def slope(A, B): return (fr(B[1]) - fr(A[1])) / (fr(B[0]) - fr(A[0]))

# =====================================================================
# 10.6 Funcions lineals: y = mx + n
# =====================================================================
f6 = lin(2, 3)
X6 = [-2, -1, 0, 1, 2]
Y6 = [ck(f6(k), v) for k, v in zip(X6, [-1, 1, 3, 5, 7])]
F_LIN = pla((-4, 4, -3, 9), fns=[(2, 3, 'c0'), (2, 0, 'c2 dsh')], pts=[(a, b, None, 'p0') for a, b in zip(X6, Y6) if a] + [(0, 3, None, 'p1')],
            curves=[([(0, 3), (1, 3), (1, 5)], 'c1 stp')], labs=[(2.9, 8.4, 'y = 2x + 3', 'l0'), (3.2, 4.6, 'y = 2x', 'l2')], W=230, H=330)
F_PAR = pla((-4, 4, -5, 5), fns=[(Fr(1, 2), 2, 'c0'), (Fr(1, 2), 0, 'c1'), (Fr(1, 2), -3, 'c2')], pts=[(0, 2, None, 'p0'), (0, 0, None, 'p1'), (0, -3, None, 'p2')],
            labs=[(-2.6, 2.0, 'n = 2', 'l0'), (-2.6, -0.4, 'n = 0', 'l1'), (-2.6, -3.2, 'n = −3', 'l2')], W=220)
F_RD = pla((-3, 5, -4, 4), fns=[(Fr(-3, 2), 2, 'c0')], curves=[([(0, 2), (2, 2), (2, -1)], 'c1 stp')], pts=[(0, 2, None, 'p1'), (2, -1, None, 'p0')], W=200, H=200)
ck(slope((0, 2), (2, -1)), Fr(-3, 2))

s6 = box('def', L('Funció lineal', 'Función lineal', 'Linear function'),
  P(r"Una <strong>funció lineal</strong> té una equació de la forma", r"Una <strong>función lineal</strong> tiene una ecuación de la forma", r"A <strong>linear function</strong> has an equation of the form")
  + D(r"y=m\,x+n")
  + ul(L(r"\(m\) és el <strong>pendent</strong>: el que augmenta \(y\) quan \(x\) augmenta 1 (apartat 10.5).", r"\(m\) es la <strong>pendiente</strong>: lo que aumenta \(y\) cuando \(x\) aumenta 1 (apartado 10.5).", r"\(m\) is the <strong>slope</strong>: how much \(y\) goes up when \(x\) goes up by 1 (section 10.5)."),
       L(r"\(n\) és l'<strong>ordenada en l'origen</strong>: el valor de \(y\) per a \(x=0\). La recta talla l'eix \(Y\) en el punt \((0,\ n)\).", r"\(n\) es la <strong>ordenada en el origen</strong>: el valor de \(y\) para \(x=0\). La recta corta el eje \(Y\) en el punto \((0,\ n)\).", r"\(n\) is the <strong>y-intercept</strong>: the value of \(y\) when \(x=0\). The line crosses the \(y\)-axis at the point \((0,\ n)\)."),
       L(r"El seu gràfic és una <strong>recta</strong> paral·lela a \(y=mx\), desplaçada \(n\) unitats cap amunt (o cap avall si \(n<0\)).", r"Su gráfica es una <strong>recta</strong> paralela a \(y=mx\), desplazada \(n\) unidades hacia arriba (o hacia abajo si \(n<0\)).", r"Its graph is a <strong>straight line</strong> parallel to \(y=mx\), shifted \(n\) units up (or down if \(n<0\))."))
  + '<div class="gout"><div class="gcol">' + P(r"Exemple: \(y=2x+3\) (\(m=2\), \(n=3\)).", r"Ejemplo: \(y=2x+3\) (\(m=2\), \(n=3\)).", r"Example: \(y=2x+3\) (\(m=2\), \(n=3\)).") + tv(X6, Y6)
  + P(r"Cada valor de \(y\) és el de \(y=2x\) més 3: la recta puja 3 unitats.", r"Cada valor de \(y\) es el de \(y=2x\) más 3: la recta sube 3 unidades.", r"Each \(y\) value is that of \(y=2x\) plus 3: the line moves up 3 units.") + '</div>' + F_LIN + '</div>'
  + note(r"La funció de proporcionalitat \(y=mx\) és una funció lineal amb \(n=0\): per això passa per l'origen.",
         r"La función de proporcionalidad \(y=mx\) es una función lineal con \(n=0\): por eso pasa por el origen.",
         r"The direct proportion function \(y=mx\) is a linear function with \(n=0\): that's why it goes through the origin."))

s6 += box('prop', L('Com es dibuixa i com es troba l\'equació', 'Cómo se dibuja y cómo se halla la ecuación', 'How to draw it and how to find its equation'),
  P(r"<strong>Dibuixar</strong> \(y=mx+n\): n'hi ha prou amb <strong>dos punts</strong>. Un de fàcil és \((0,\ n)\); des d'ell, avancem 1 cap a la dreta i pugem \(m\) (o baixem si \(m<0\)). O bé fem una taula amb dos o tres valors de \(x\).",
    r"<strong>Dibujar</strong> \(y=mx+n\): basta con <strong>dos puntos</strong>. Uno fácil es \((0,\ n)\); desde él, avanzamos 1 hacia la derecha y subimos \(m\) (o bajamos si \(m<0\)). O bien hacemos una tabla con dos o tres valores de \(x\).",
    r"<strong>Drawing</strong> \(y=mx+n\): <strong>two points</strong> are enough. An easy one is \((0,\ n)\); from there, move 1 to the right and go up \(m\) (or down if \(m<0\)). Or make a table with two or three values of \(x\).")
  + P(r"<strong>Rectes paral·leles</strong>: les rectes amb el <strong>mateix pendent</strong> són paral·leles; només canvia on tallen l'eix \(Y\).", r"<strong>Rectas paralelas</strong>: las rectas con la <strong>misma pendiente</strong> son paralelas; solo cambia dónde cortan el eje \(Y\).", r"<strong>Parallel lines</strong>: lines with the <strong>same slope</strong> are parallel; only where they cross the \(y\)-axis changes.")
  + figs(fig(F_PAR, L('\\(y=\\frac12x+n\\): rectes paral·leles', '\\(y=\\frac12x+n\\): rectas paralelas', '\\(y=\\frac12x+n\\): parallel lines')))
  + P(r"<strong>Trobar l'equació</strong> d'una recta:", r"<strong>Hallar la ecuación</strong> de una recta:", r"<strong>Finding the equation</strong> of a line:")
  + ul(L(r"<strong>Amb el gràfic</strong>: \(n\) és on talla l'eix \(Y\) i \(m\) es llig amb un triangle (quant puja o baixa per cada unitat que avança).", r"<strong>Con la gráfica</strong>: \(n\) es donde corta el eje \(Y\) y \(m\) se lee con un triángulo (cuánto sube o baja por cada unidad que avanza).", r"<strong>From the graph</strong>: \(n\) is where it crosses the \(y\)-axis and \(m\) is read with a triangle (how much it goes up or down for each unit across)."),
       L(r"<strong>Amb el pendent i un punt</strong> \((a,\ b)\): substituïm en \(b=m\cdot a+n\) i aïllem \(n\).", r"<strong>Con la pendiente y un punto</strong> \((a,\ b)\): sustituimos en \(b=m\cdot a+n\) y despejamos \(n\).", r"<strong>From the slope and a point</strong> \((a,\ b)\): substitute into \(b=m\cdot a+n\) and solve for \(n\)."),
       L(r"<strong>Amb dos punts</strong>: primer calculem \(m=\frac{y_2-y_1}{x_2-x_1}\) i després \(n\) amb un dels punts.", r"<strong>Con dos puntos</strong>: primero calculamos \(m=\frac{y_2-y_1}{x_2-x_1}\) y después \(n\) con uno de los puntos.", r"<strong>From two points</strong>: first work out \(m=\frac{y_2-y_1}{x_2-x_1}\) and then \(n\) using one of the points."))
  + '<div class="gout">' + F_RD + '<div class="gcol">'
  + P(r"Talla l'eix \(Y\) en \((0,\ 2)\): \(n=2\). Des d'allí, avança 2 i baixa 3: \(m=-\frac32\).", r"Corta el eje \(Y\) en \((0,\ 2)\): \(n=2\). Desde allí, avanza 2 y baja 3: \(m=-\frac32\).", r"It crosses the \(y\)-axis at \((0,\ 2)\): \(n=2\). From there, it goes 2 across and 3 down: \(m=-\frac32\).")
  + D(r"y=-\tfrac32x+2") + '</div></div>'
  + widget('w-mn', '📉', L('Explora y = m·x + n', 'Explora y = m·x + n', 'Explore y = m·x + n'),
           ['<div class="wrow">' + rng('m', -3, 3, 0.5, 1, 'm') + '</div>', '<div class="wrow">' + rng('n', -5, 5, 1, 2, 'n') + '</div>'], out='<div class="gout"></div>')
  + drill('img1', 'Entrena: calcula la y', 'Entrena: calcula la y', 'Train: work out y')
  + drill('eq', 'Entrena: quina és l\'equació?', 'Entrena: ¿cuál es la ecuación?', 'Train: which is the equation?', 'opts')
  + drill('eqpm', 'Entrena: troba la n', 'Entrena: halla la n', 'Train: find n'))

g6 = lin(2, -3)
XG = [-1, 0, 1, 2, 3]
YG = [ck(g6(k), v) for k, v in zip(XG, [-5, -3, -1, 1, 3])]
F_G6 = pla((-2, 4, -6, 4), fns=[(2, -3, 'c0')], pts=[(a, b, None, 'p0') for a, b in zip(XG, YG)], W=200, H=330)
F_EQ = pla((-4, 4, -4, 5), fns=[(-1, 3, 'c0'), (Fr(1, 3), -2, 'c1')], pts=[(0, 3, None, 'p0'), (3, 0, None, 'p0'), (0, -2, None, 'p1'), (3, -1, None, 'p1')], labs=[(-3.2, 4.2, 'r', 'l0'), (-3.2, -3.4, 's', 'l1')], W=220)
ck(slope((0, 3), (3, 0)), -1); ck(slope((0, -2), (3, -1)), Fr(1, 3))
P1, P2 = (1, 5), (3, 9)
m12 = ck(slope(P1, P2), 2); n12 = ck(fr(5) - 2 * 1, 3)
assert lin(2, 3)(-2) == -1
s6 += levels(
 [prob(L(r"Fes una taula de valors de \(y=2x-3\), representa-la i digues quin és el pendent i on talla l'eix \(Y\).", r"Haz una tabla de valores de \(y=2x-3\), represéntala y di cuál es la pendiente y dónde corta el eje \(Y\).", r"Make a table of values of \(y=2x-3\), plot it and say what the slope is and where it crosses the \(y\)-axis."),
       tv(XG, YG) + figs(fig(F_G6)),
       P(r"\(m=2\): creixent; cada pas a la dreta puja 2. \(n=-3\): talla l'eix \(Y\) en \((0,\ -3)\).", r"\(m=2\): creciente; cada paso a la derecha sube 2. \(n=-3\): corta el eje \(Y\) en \((0,\ -3)\).", r"\(m=2\): increasing; each step to the right goes up 2. \(n=-3\): it crosses the \(y\)-axis at \((0,\ -3)\).")),
  prob(L(r"Digues el pendent i l'ordenada en l'origen de cada recta i quines són paral·leles: \(y=3x-1\), \(y=-x+4\), \(y=3x+2\), \(y=5-x\), \(y=x\).", r"Di la pendiente y la ordenada en el origen de cada recta y cuáles son paralelas: \(y=3x-1\), \(y=-x+4\), \(y=3x+2\), \(y=5-x\), \(y=x\).", r"Give the slope and the y-intercept of each line and say which are parallel: \(y=3x-1\), \(y=-x+4\), \(y=3x+2\), \(y=5-x\), \(y=x\)."),
       tbl([L('Recta', 'Recta', 'Line'), 'm', 'n'], [[r'\(y=3x-1\)', '3', r'\(-1\)'], [r'\(y=-x+4\)', r'\(-1\)', '4'], [r'\(y=3x+2\)', '3', '2'], [r'\(y=5-x\)', r'\(-1\)', '5'], [r'\(y=x\)', '1', '0']]),
       P(r"Compte: \(y=5-x\) és el mateix que \(y=-x+5\). Són paral·leles les que tenen el mateix pendent: \(y=3x-1\) i \(y=3x+2\); \(y=-x+4\) i \(y=5-x\).", r"Cuidado: \(y=5-x\) es lo mismo que \(y=-x+5\). Son paralelas las que tienen la misma pendiente: \(y=3x-1\) e \(y=3x+2\); \(y=-x+4\) e \(y=5-x\).", r"Careful: \(y=5-x\) is the same as \(y=-x+5\). Lines with the same slope are parallel: \(y=3x-1\) and \(y=3x+2\); \(y=-x+4\) and \(y=5-x\)."))],
 [prob(L(r"Escriu l'equació de les rectes \(r\) i \(s\) del gràfic.", r"Escribe la ecuación de las rectas \(r\) y \(s\) de la gráfica.", r"Write the equation of lines \(r\) and \(s\) in the graph.") + figs(fig(F_EQ)),
       P(r"\(r\): talla l'eix \(Y\) en \((0,\ 3)\), \(n=3\). Passa per \((3,\ 0)\): avança 3 i baixa 3, \(m=-1\). \(\boxed{y=-x+3}\)", r"\(r\): corta el eje \(Y\) en \((0,\ 3)\), \(n=3\). Pasa por \((3,\ 0)\): avanza 3 y baja 3, \(m=-1\). \(\boxed{y=-x+3}\)", r"\(r\): crosses the \(y\)-axis at \((0,\ 3)\), \(n=3\). It goes through \((3,\ 0)\): 3 across and 3 down, \(m=-1\). \(\boxed{y=-x+3}\)"),
       P(r"\(s\): talla l'eix \(Y\) en \((0,\ -2)\), \(n=-2\). Passa per \((3,\ -1)\): avança 3 i puja 1, \(m=\frac13\). \(\boxed{y=\frac13x-2}\)", r"\(s\): corta el eje \(Y\) en \((0,\ -2)\), \(n=-2\). Pasa por \((3,\ -1)\): avanza 3 y sube 1, \(m=\frac13\). \(\boxed{y=\frac13x-2}\)", r"\(s\): crosses the \(y\)-axis at \((0,\ -2)\), \(n=-2\). It goes through \((3,\ -1)\): 3 across and 1 up, \(m=\frac13\). \(\boxed{y=\frac13x-2}\)")),
  prob(L(r"Una recta té pendent \(-3\) i passa pel punt \((2,\ 1)\). Escriu-ne l'equació.", r"Una recta tiene pendiente \(-3\) y pasa por el punto \((2,\ 1)\). Escribe su ecuación.", r"A line has slope \(-3\) and goes through the point \((2,\ 1)\). Write its equation."),
       P(r"És de la forma \(y=-3x+n\). Com que passa per \((2,\ 1)\), quan \(x=2\) ha de donar \(y=1\):", r"Es de la forma \(y=-3x+n\). Como pasa por \((2,\ 1)\), cuando \(x=2\) tiene que dar \(y=1\):", r"It has the form \(y=-3x+n\). Since it goes through \((2,\ 1)\), \(x=2\) must give \(y=1\):"),
       D(r"1=-3\cdot2+n\ \Rightarrow\ 1=-6+n\ \Rightarrow\ n=7\qquad \boxed{y=-3x+7}"))],
 [prob(L(r"Troba l'equació de la recta que passa per \(A(1,\ 5)\) i \(B(3,\ 9)\) i comprova si el punt \(C(-2,\ -1)\) hi és.", r"Halla la ecuación de la recta que pasa por \(A(1,\ 5)\) y \(B(3,\ 9)\) y comprueba si el punto \(C(-2,\ -1)\) está en ella.", r"Find the equation of the line through \(A(1,\ 5)\) and \(B(3,\ 9)\) and check whether the point \(C(-2,\ -1)\) is on it."),
       D(r"m=\frac{9-5}{3-1}=\frac42=2"),
       D(r"5=2\cdot1+n\ \Rightarrow\ n=3\qquad \boxed{y=2x+3}"),
       D(r"x=-2:\ y=2\cdot(-2)+3=-1\ \checkmark") + P(r"El punt \(C\) <strong>sí</strong> que és de la recta.", r"El punto \(C\) <strong>sí</strong> es de la recta.", r"Point \(C\) <strong>is</strong> on the line."))])
ck(fr(1) + 6, 7); assert lin(-3, 7)(2) == 1
s6 += practice([('★☆☆', L(r"Quin és el pendent i l'ordenada en l'origen de \(y=-4x+1\)? Talla l'eix \(Y\) per dalt o per baix de l'origen?", r"¿Cuál es la pendiente y la ordenada en el origen de \(y=-4x+1\)? ¿Corta el eje \(Y\) por encima o por debajo del origen?", r"What are the slope and the y-intercept of \(y=-4x+1\)? Does it cross the \(y\)-axis above or below the origin?")),
                ('★★☆', L(r"Escriu l'equació de la recta paral·lela a \(y=2x\) que passa per \((3,\ 4)\).", r"Escribe la ecuación de la recta paralela a \(y=2x\) que pasa por \((3,\ 4)\).", r"Write the equation of the line parallel to \(y=2x\) through \((3,\ 4)\)."))],
               L(r"1) \(m=-4\), \(n=1\): per dalt, en \((0,\ 1)\). &nbsp; 2) \(m=2\): \(4=6+n\Rightarrow n=-2\); \(y=2x-2\).", r"1) \(m=-4\), \(n=1\): por encima, en \((0,\ 1)\). &nbsp; 2) \(m=2\): \(4=6+n\Rightarrow n=-2\); \(y=2x-2\).", r"1) \(m=-4\), \(n=1\): above, at \((0,\ 1)\). &nbsp; 2) \(m=2\): \(4=6+n\Rightarrow n=-2\); \(y=2x-2\)."))
assert lin(2, -2)(3) == 4

# =====================================================================
# 10.7 Funcions constants: y = k
# =====================================================================
F_K = pla((-4, 4, -4, 5), fns=[(0, 3, 'c0'), (0, -2, 'c1')], pts=[(a, 3, None, 'p0') for a in (-2, -1, 0, 1, 2)], labs=[(2.8, 3.5, 'y = 3', 'l0'), (2.8, -1.5, 'y = −2', 'l1')], W=230)
F_V = pla((-4, 4, -4, 4), curves=[([(2, -4), (2, 4)], 'c1')], pts=[(2, -2, None, 'bad'), (2, 1, None, 'bad'), (2, 3, None, 'bad')], labs=[(2.9, 3.4, 'x = 2', 'l1')], W=180)
PARK = [(0, 2), (1, 2)], [(1, 5), (3, 5)], [(3, 8), (6, 8)]
F_PARK = pla((0, 6.5, 0, 10), curves=[(s, 'c0') for s in PARK], pts=[(1, 2, None, 'p0'), (3, 5, None, 'p0')], W=260, H=200, ys=2, gy=1, xl='h', yl='€')
s7 = box('def', L('Funció constant', 'Función constante', 'Constant function'),
  P(r"Una <strong>funció constant</strong> pren <strong>sempre el mateix valor</strong>, siga quin siga el valor de \(x\). La seua equació és", r"Una <strong>función constante</strong> toma <strong>siempre el mismo valor</strong>, sea cual sea el valor de \(x\). Su ecuación es", r"A <strong>constant function</strong> <strong>always takes the same value</strong>, whatever the value of \(x\). Its equation is")
  + D(r"y=k\qquad(k\ \text{" + Lt('un nombre', 'un número', 'a number') + r"})")
  + '<div class="gout"><div class="gcol">'
  + ul(L(r"El seu gràfic és una <strong>recta horitzontal</strong> que talla l'eix \(Y\) en \((0,\ k)\).", r"Su gráfica es una <strong>recta horizontal</strong> que corta el eje \(Y\) en \((0,\ k)\).", r"Its graph is a <strong>horizontal line</strong> crossing the \(y\)-axis at \((0,\ k)\)."),
       L(r"És una funció lineal amb pendent \(m=0\): \(y=0\cdot x+k\). No creix ni decreix.", r"Es una función lineal con pendiente \(m=0\): \(y=0\cdot x+k\). No crece ni decrece.", r"It's a linear function with slope \(m=0\): \(y=0\cdot x+k\). It neither increases nor decreases."),
       L(r"En la taula, tots els valors de \(y\) són iguals:", r"En la tabla, todos los valores de \(y\) son iguales:", r"In its table, all the \(y\) values are the same:") + tv([-2, -1, 0, 1, 2], [3] * 5),
       L(r"La funció \(y=0\) és l'eix \(X\).", r"La función \(y=0\) es el eje \(X\).", r"The function \(y=0\) is the \(x\)-axis."))
  + '</div>' + F_K + '</div>'
  + P(r"Exemples: una tarifa plana de mòbil de 15 € al mes (paguem el mateix parlem el que parlem), la temperatura d'un frigorífic que està sempre a 4 °C, el preu d'un llibre segons el dia de la setmana…",
      r"Ejemplos: una tarifa plana de móvil de 15 € al mes (pagamos lo mismo hablemos lo que hablemos), la temperatura de un frigorífico que está siempre a 4 °C, el precio de un libro según el día de la semana…",
      r"Examples: a flat-rate phone plan of €15 a month (we pay the same however much we talk), the temperature of a fridge that's always at 4 °C, the price of a book depending on the day of the week…"))

s7 += box('prop', L('Rectes horitzontals i verticals', 'Rectas horizontales y verticales', 'Horizontal and vertical lines'),
  '<div class="gout">' + F_V + '<div class="gcol">'
  + P(r"Una recta <strong>vertical</strong>, com \(x=2\), <strong>no és una funció</strong>: al valor \(x=2\) li corresponen infinits valors de \(y\) (no supera la prova de la recta vertical).",
      r"Una recta <strong>vertical</strong>, como \(x=2\), <strong>no es una función</strong>: al valor \(x=2\) le corresponden infinitos valores de \(y\) (no supera la prueba de la recta vertical).",
      r"A <strong>vertical</strong> line, like \(x=2\), is <strong>not a function</strong>: the value \(x=2\) is paired with infinitely many values of \(y\) (it fails the vertical line test).")
  + tbl(['', L('Horitzontal', 'Horizontal', 'Horizontal'), L('Vertical', 'Vertical', 'Vertical')],
        [[L('Equació', 'Ecuación', 'Equation'), r'\(y=k\)', r'\(x=a\)'], [L('Pendent', 'Pendiente', 'Slope'), r'\(m=0\)', L('no en té', 'no tiene', 'none')], [L('És funció?', '¿Es función?', 'Function?'), L('<strong>sí</strong>', '<strong>sí</strong>', '<strong>yes</strong>'), L('<strong>no</strong>', '<strong>no</strong>', '<strong>no</strong>')]])
  + '</div></div>'
  + P(r"<strong>Funcions constants a trossos.</strong> Moltes tarifes són constants per trams. Un aparcament cobra 2 € la primera hora, 5 € fins a 3 hores i 8 € fins a 6 hores. El gràfic té tres trossos horitzontals:",
      r"<strong>Funciones constantes a trozos.</strong> Muchas tarifas son constantes por tramos. Un aparcamiento cobra 2 € la primera hora, 5 € hasta 3 horas y 8 € hasta 6 horas. La gráfica tiene tres trozos horizontales:",
      r"<strong>Piecewise constant functions.</strong> Many prices are constant in stages. A car park charges €2 for the first hour, €5 up to 3 hours and €8 up to 6 hours. The graph has three flat pieces:")
  + figs(fig(F_PARK, L('Aparcament: per 2 h 30 min paguem 5 €', 'Aparcamiento: por 2 h 30 min pagamos 5 €', 'Car park: 2 h 30 min costs €5')))
  + widget('w-const', '➖', L('Recta horitzontal o vertical?', '¿Recta horizontal o vertical?', 'Horizontal or vertical line?'),
           [seg([('h', 'y = k'), ('v', 'x = k')]), '<div class="wrow">' + rng('k', -4, 4, 0.5, 2, 'k') + '</div>'], out='<div class="gout"></div>')
  + drill('kind', 'Entrena: de quin tipus és la funció?', 'Entrena: ¿de qué tipo es la función?', 'Train: what type of function is it?', 'opts'))

TEL = lin(0, 25)
s7 += levels(
 [prob(L(r"Representa en els mateixos eixos les funcions \(y=3\), \(y=-1\) i \(y=0\).", r"Representa en los mismos ejes las funciones \(y=3\), \(y=-1\) e \(y=0\).", r"Plot the functions \(y=3\), \(y=-1\) and \(y=0\) on the same axes."),
       P(r"Són rectes horitzontals que tallen l'eix \(Y\) en 3, en \(-1\) i en 0 (aquesta última és l'eix \(X\)).", r"Son rectas horizontales que cortan el eje \(Y\) en 3, en \(-1\) y en 0 (esta última es el eje \(X\)).", r"They are horizontal lines crossing the \(y\)-axis at 3, at \(-1\) and at 0 (the last one is the \(x\)-axis).")
       + figs(fig(pla((-4, 4, -3, 4), fns=[(0, 3, 'c0'), (0, -1, 'c1'), (0, 0, 'c2')], labs=[(2.8, 3.4, 'y = 3', 'l0'), (2.8, -0.6, 'y = −1', 'l1'), (-2.8, 0.4, 'y = 0', 'l2')], W=220)))),
  prob(L(r"Escriu l'equació de la recta horitzontal i de la recta vertical que passen pel punt \((5,\ -4)\). Quina és una funció?", r"Escribe la ecuación de la recta horizontal y de la recta vertical que pasan por el punto \((5,\ -4)\). ¿Cuál es una función?", r"Write the equations of the horizontal and the vertical line through the point \((5,\ -4)\). Which one is a function?"),
       P(r"En la horitzontal, tots els punts tenen \(y=-4\): \(\boxed{y=-4}\). En la vertical, tots tenen \(x=5\): \(\boxed{x=5}\).", r"En la horizontal, todos los puntos tienen \(y=-4\): \(\boxed{y=-4}\). En la vertical, todos tienen \(x=5\): \(\boxed{x=5}\).", r"On the horizontal one, every point has \(y=-4\): \(\boxed{y=-4}\). On the vertical one, every point has \(x=5\): \(\boxed{x=5}\)."),
       P(r"Només \(y=-4\) és una funció (constant).", r"Solo \(y=-4\) es una función (constante).", r"Only \(y=-4\) is a function (a constant one)."))],
 [prob(L(r"Classifica aquestes funcions en <em>de proporcionalitat</em>, <em>lineals</em> (no de proporcionalitat), <em>constants</em> o <em>cap d'aquestes</em>: \(y=5x\), \(y=2x-7\), \(y=6\), \(y=x^2\), \(y=-\frac{x}{3}\), \(y=4-x\).",
         r"Clasifica estas funciones en <em>de proporcionalidad</em>, <em>lineales</em> (no de proporcionalidad), <em>constantes</em> o <em>ninguna de estas</em>: \(y=5x\), \(y=2x-7\), \(y=6\), \(y=x^2\), \(y=-\frac{x}{3}\), \(y=4-x\).",
         r"Classify these functions as <em>direct proportion</em>, <em>linear</em> (not direct proportion), <em>constant</em> or <em>none of these</em>: \(y=5x\), \(y=2x-7\), \(y=6\), \(y=x^2\), \(y=-\frac{x}{3}\), \(y=4-x\)."),
       ul(L(r"De proporcionalitat (\(y=mx\)): \(y=5x\) i \(y=-\frac{x}{3}\).", r"De proporcionalidad (\(y=mx\)): \(y=5x\) e \(y=-\frac{x}{3}\).", r"Direct proportion (\(y=mx\)): \(y=5x\) and \(y=-\frac{x}{3}\)."),
          L(r"Lineals (\(y=mx+n\), \(n\neq0\)): \(y=2x-7\) i \(y=4-x\).", r"Lineales (\(y=mx+n\), \(n\neq0\)): \(y=2x-7\) e \(y=4-x\).", r"Linear (\(y=mx+n\), \(n\neq0\)): \(y=2x-7\) and \(y=4-x\)."),
          L(r"Constant (\(y=k\)): \(y=6\).", r"Constante (\(y=k\)): \(y=6\).", r"Constant (\(y=k\)): \(y=6\)."),
          L(r"Cap d'aquestes: \(y=x^2\) (el seu gràfic no és una recta).", r"Ninguna de estas: \(y=x^2\) (su gráfica no es una recta).", r"None of these: \(y=x^2\) (its graph isn't a straight line)."))),
  prob(L(r"Mira el gràfic de l'aparcament. Quant paguem per 40 minuts? I per 2 hores? I per 4 h 15 min? Quant de temps podem estar-hi per 5 €?", r"Mira la gráfica del aparcamiento. ¿Cuánto pagamos por 40 minutos? ¿Y por 2 horas? ¿Y por 4 h 15 min? ¿Cuánto tiempo podemos estar por 5 €?", r"Look at the car park graph. How much do we pay for 40 minutes? And for 2 hours? And for 4 h 15 min? How long can we stay for €5?"),
       P(r"40 min és menys d'1 h: \(\boxed{2\ €}\). 2 h està en el segon tram: \(\boxed{5\ €}\). 4 h 15 min està en el tercer: \(\boxed{8\ €}\).", r"40 min es menos de 1 h: \(\boxed{2\ €}\). 2 h está en el segundo tramo: \(\boxed{5\ €}\). 4 h 15 min está en el tercero: \(\boxed{8\ €}\).", r"40 min is less than 1 h: \(\boxed{2\ €}\). 2 h is in the second stage: \(\boxed{5\ €}\). 4 h 15 min is in the third: \(\boxed{8\ €}\)."),
       P(r"Per 5 € podem estar-hi <strong>de més d'1 h fins a 3 h</strong>.", r"Por 5 € podemos estar <strong>de más de 1 h hasta 3 h</strong>.", r"For €5 we can stay <strong>from just over 1 h up to 3 h</strong>."))],
 [prob(L(r"Una companyia ofereix una tarifa plana de 25 € al mes i una altra cobra 0,05 € per minut. Escriu les dues funcions. A partir de quants minuts convé la tarifa plana?",
         r"Una compañía ofrece una tarifa plana de 25 € al mes y otra cobra 0,05 € por minuto. Escribe las dos funciones. ¿A partir de cuántos minutos conviene la tarifa plana?",
         r"One company offers a flat rate of €25 a month and another charges €0.05 a minute. Write both functions. From how many minutes is the flat rate better?"),
       D(r"\text{" + Lt('Plana', 'Plana', 'Flat') + r"}:\ y=25\qquad \text{" + Lt('Per minut', 'Por minuto', 'Per minute') + r"}:\ y=0{,}05x"),
       P(r"Costen el mateix quan \(0{,}05x=25\):", r"Cuestan lo mismo cuando \(0{,}05x=25\):", r"They cost the same when \(0.05x=25\):") + D(r"x=\frac{25}{0{,}05}=500\ \text{min}"),
       P(r"Si parlem <strong>més de 500 minuts</strong>, la tarifa per minut supera els 25 €: convé la tarifa plana.", r"Si hablamos <strong>más de 500 minutos</strong>, la tarifa por minuto supera los 25 €: conviene la tarifa plana.", r"If we talk for <strong>more than 500 minutes</strong>, the per-minute plan goes over €25: the flat rate is better.")
       + figs(fig(pla((0, 800, 0, 44), fns=[(0, 25, 'c0', 0, 800), ('0.05', 0, 'c1', 0, 800)], pts=[(500, 25, None, 'cut')], proj=[(500, 25)], W=280, H=200, xs=100, gx=50, ys=10, gy=5, xl='min', yl='€'),
                      '<span class="key k0"></span>' + L('plana', 'plana', 'flat') + ' &nbsp; <span class="key k1"></span>' + L('per minut', 'por minuto', 'per minute'))))])
ck(Fr(25) / fr('0.05'), 500); ck(TEL(123), 25)
s7 += practice([('★☆☆', L(r"Quin és el pendent de la recta \(y=-7\)? Per on talla l'eix \(Y\)?", r"¿Cuál es la pendiente de la recta \(y=-7\)? ¿Por dónde corta el eje \(Y\)?", r"What is the slope of the line \(y=-7\)? Where does it cross the \(y\)-axis?")),
                ('★★☆', L(r"Una recta passa per \((-3,\ 2)\) i \((4,\ 2)\). Quina és la seua equació?", r"Una recta pasa por \((-3,\ 2)\) y \((4,\ 2)\). ¿Cuál es su ecuación?", r"A line goes through \((-3,\ 2)\) and \((4,\ 2)\). What is its equation?"))],
               L(r"1) \(m=0\); en \((0,\ -7)\). &nbsp; 2) \(m=\frac{2-2}{4+3}=0\): és constant, \(y=2\).", r"1) \(m=0\); en \((0,\ -7)\). &nbsp; 2) \(m=\frac{2-2}{4+3}=0\): es constante, \(y=2\).", r"1) \(m=0\); at \((0,\ -7)\). &nbsp; 2) \(m=\frac{2-2}{4+3}=0\): it's constant, \(y=2\)."))
ck(slope((-3, 2), (4, 2)), 0)
