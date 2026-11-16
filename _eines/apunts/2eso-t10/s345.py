# Apartats 10.3-10.5 dels apunts de la Unitat 10 de 2n ESO (Funcions): funcions donades per la seua equació, funció de
# proporcionalitat y = mx i pendent d'una recta. Cada resultat es comprova amb ck() i lin() (fraccions exactes).
from comu import *

def samp(f, a, b, n=60):
    """punts d'una corba y = f(x) per a dibuixar-la com a línia poligonal"""
    return [(a + (b - a) * k / n, float(f(fr(a) + (fr(b) - fr(a)) * k / n))) for k in range(n + 1)]
def slope(A, B): return (fr(B[1]) - fr(A[1])) / (fr(B[0]) - fr(A[0]))

# =====================================================================
# 10.3 Funcions donades per la seua equació
# =====================================================================
f1 = lin(2, -1)
X1 = [-2, -1, 0, 1, 2, 3]
Y1 = [ck(f1(k), v) for k, v in zip(X1, [-5, -3, -1, 1, 3, 5])]
F_E1 = pla((-3, 4, -6, 6), fns=[(2, -1, 'c0')], pts=[(a, b, None, 'p0') for a, b in zip(X1, Y1)], W=210, H=300)
q = lambda x: fr(x) ** 2 - 1
XQ = [-3, -2, -1, 0, 1, 2, 3]
YQ = [ck(q(k), v) for k, v in zip(XQ, [8, 3, 0, -1, 0, 3, 8])]
F_Q = pla((-3.6, 3.6, -2, 9), curves=[(samp(q, -3.1, 3.1), 'c0')], pts=[(a, b, None, 'p0') for a, b in zip(XQ, YQ)], W=220, H=300)

s3 = box('def', L("L'equació d'una funció", 'La ecuación de una función', 'The equation of a function'),
  P(r"Moltes funcions es donen amb una <strong>equació</strong> (o fórmula) que diu què hem de fer amb la \(x\) per a obtindre la \(y\). Per exemple, \(y=2x-1\) vol dir: «multiplica la \(x\) per 2 i resta-li 1».",
    r"Muchas funciones se dan con una <strong>ecuación</strong> (o fórmula) que dice qué tenemos que hacer con la \(x\) para obtener la \(y\). Por ejemplo, \(y=2x-1\) quiere decir: «multiplica la \(x\) por 2 y réstale 1».",
    r"Many functions are given by an <strong>equation</strong> (or formula) that says what to do with \(x\) to get \(y\). For example, \(y=2x-1\) means: “multiply \(x\) by 2 and subtract 1”.")
  + P(r"Per a calcular el valor de \(y\) que correspon a un valor de \(x\), <strong>substituïm</strong> la \(x\) pel seu valor (si és negatiu, entre parèntesis) i fem les operacions:",
      r"Para calcular el valor de \(y\) que corresponde a un valor de \(x\), <strong>sustituimos</strong> la \(x\) por su valor (si es negativo, entre paréntesis) y hacemos las operaciones:",
      r"To find the value of \(y\) that goes with a value of \(x\), <strong>substitute</strong> \(x\) by its value (in brackets if it's negative) and do the operations:")
  + D(r"x=3:\ y=2\cdot3-1=5\qquad x=-2:\ y=2\cdot(-2)-1=-5")
  + note(r"De vegades s'escriu \(f(x)=2x-1\) en lloc de \(y=2x-1\). Aleshores \(f(3)=5\) vol dir que per a \(x=3\) la funció val 5: el punt \((3,\ 5)\) és del gràfic.",
         r"A veces se escribe \(f(x)=2x-1\) en lugar de \(y=2x-1\). Entonces \(f(3)=5\) quiere decir que para \(x=3\) la función vale 5: el punto \((3,\ 5)\) es de la gráfica.",
         r"Sometimes we write \(f(x)=2x-1\) instead of \(y=2x-1\). Then \(f(3)=5\) means that when \(x=3\) the function is 5: the point \((3,\ 5)\) is on the graph."))
ck(f1(3), 5); ck(f1(-2), -5)

s3 += box('prop', L("De l'equació al gràfic", 'De la ecuación a la gráfica', 'From the equation to the graph'),
  ol(L(r"Triem uns quants valors de \(x\) (negatius, el 0 i positius) i fem una <strong>taula de valors</strong>.", r"Elegimos unos cuantos valores de \(x\) (negativos, el 0 y positivos) y hacemos una <strong>tabla de valores</strong>.", r"Pick a few values of \(x\) (negative ones, 0 and positive ones) and make a <strong>table of values</strong>."),
     L(r"Dibuixem els <strong>punts</strong> en uns eixos.", r"Dibujamos los <strong>puntos</strong> en unos ejes.", r"Plot the <strong>points</strong> on a pair of axes."),
     L(r"Els <strong>unim</strong>: amb una recta si estan alineats o amb una línia corba suau si no ho estan.", r"Los <strong>unimos</strong>: con una recta si están alineados o con una línea curva suave si no lo están.", r"<strong>Join</strong> them: with a straight line if they line up, or with a smooth curve if they don't."))
  + '<div class="gout"><div class="gcol">' + P(r"\(y=2x-1\):", r"\(y=2x-1\):", r"\(y=2x-1\):") + tv(X1, Y1) + P(r"Els punts estan alineats: el gràfic és una <strong>recta</strong>.", r"Los puntos están alineados: la gráfica es una <strong>recta</strong>.", r"The points line up: the graph is a <strong>straight line</strong>.") + '</div>' + F_E1 + '</div>'
  + '<div class="gout"><div class="gcol">' + P(r"\(y=x^2-1\):", r"\(y=x^2-1\):", r"\(y=x^2-1\):") + tv(XQ, YQ) + P(r"Compte amb els negatius: \((-3)^2-1=9-1=8\). Els punts no estan alineats: el gràfic és una <strong>corba</strong> (una paràbola).",
      r"Cuidado con los negativos: \((-3)^2-1=9-1=8\). Los puntos no están alineados: la gráfica es una <strong>curva</strong> (una parábola).",
      r"Careful with negatives: \((-3)^2-1=9-1=8\). The points don't line up: the graph is a <strong>curve</strong> (a parabola).") + '</div>' + F_Q + '</div>'
  + widget('w-plot', '🧮', L("Escriu l'equació i mira el gràfic", 'Escribe la ecuación y mira la gráfica', 'Type the equation and see the graph'),
           ['<div class="wrow"><label>y = <input class="tin w" type="text" data-k="f" value="2x-1" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="f"></label></div>',
            '<div class="wrow">' + tin('a', L('x des de', 'x desde', 'x from'), '-3') + tin('b', L('fins a', 'hasta', 'to'), '3') + '</div>',
            quick([('2x-1|-3|3', 'y = 2x − 1'), ('x^2-1|-3|3', 'y = x² − 1'), ('-x+4|-2|6', 'y = −x + 4'), ('12/x|1|12', 'y = 12/x'), ('3|-3|3', 'y = 3')])],
           out='<div class="gout"></div>')
  + drill('img', 'Entrena: calcula la y', 'Entrena: calcula la y', 'Train: work out y'))

s3 += box('prop', L('Un punt és del gràfic?', '¿Un punto es de la gráfica?', 'Is a point on the graph?'),
  P(r"Un punt \((a,\ b)\) és del gràfic si, en substituir \(x=a\) en l'equació, obtenim \(y=b\). Per exemple, amb \(y=2x-1\):",
    r"Un punto \((a,\ b)\) es de la gráfica si, al sustituir \(x=a\) en la ecuación, obtenemos \(y=b\). Por ejemplo, con \(y=2x-1\):",
    r"A point \((a,\ b)\) is on the graph if substituting \(x=a\) in the equation gives \(y=b\). For example, with \(y=2x-1\):")
  + ul(L(r"\((4,\ 7)\): \(2\cdot4-1=7\) ✓ <strong>sí</strong> que és del gràfic.", r"\((4,\ 7)\): \(2\cdot4-1=7\) ✓ <strong>sí</strong> es de la gráfica.", r"\((4,\ 7)\): \(2\cdot4-1=7\) ✓ it <strong>is</strong> on the graph."),
       L(r"\((5,\ 8)\): \(2\cdot5-1=9\neq8\) ✗ <strong>no</strong> és del gràfic.", r"\((5,\ 8)\): \(2\cdot5-1=9\neq8\) ✗ <strong>no</strong> es de la gráfica.", r"\((5,\ 8)\): \(2\cdot5-1=9\neq8\) ✗ it is <strong>not</strong> on the graph."))
  + P(r"<strong>Si ens donen la \(y\)</strong> i volem la \(x\), resolem una equació (unitat 4). Per a quin valor de \(x\) és \(y=11\)?",
      r"<strong>Si nos dan la \(y\)</strong> y queremos la \(x\), resolvemos una ecuación (unidad 4). ¿Para qué valor de \(x\) es \(y=11\)?",
      r"<strong>If we're given \(y\)</strong> and want \(x\), we solve an equation (unit 4). For which value of \(x\) is \(y=11\)?")
  + D(r"2x-1=11\ \Rightarrow\ 2x=12\ \Rightarrow\ x=6")
  + drill('belongs', 'Entrena: el punt és del gràfic?', 'Entrena: ¿el punto es de la gráfica?', 'Train: is the point on the graph?', 'opts')
  + drill('pre', 'Entrena: troba la x', 'Entrena: halla la x', 'Train: find x'))
ck(f1(4), 7); assert f1(5) == 9; ck(Fr(12, 2), 6)

g3 = lin(3, -2)
X3 = [-1, 0, 1, 2]
Y3 = [ck(g3(k), v) for k, v in zip(X3, [-5, -2, 1, 4])]
c3 = lambda x: 4 - fr(x) ** 2
XC = [-2, -1, 0, 1, 2]
YC = [ck(c3(k), v) for k, v in zip(XC, [0, 3, 4, 3, 0])]
F_C3 = pla((-3, 3, -1.5, 5), curves=[(samp(c3, -2.3, 2.3), 'c0')], pts=[(a, b, None, 'p0') for a, b in zip(XC, YC)], W=220, H=240)
h3 = lin(-2, 5)
RA = lambda x: fr(x) * (10 - fr(x))
XR = list(range(1, 10))
YR = [ck(RA(k), v) for k, v in zip(XR, [9, 16, 21, 24, 25, 24, 21, 16, 9])]
F_RA = pla((0, 10.5, 0, 29), curves=[(samp(RA, 0, 10), 'c0')], pts=[(a, b, None, 'p0') for a, b in zip(XR, YR)] + [(5, 25, None, 'p1')], W=260, H=220, ys=5, gy=5, xl='x (m)', yl='A (m²)')
s3 += levels(
 [prob(L(r"Fes una taula de valors de \(y=3x-2\) per a \(x=-1,\ 0,\ 1,\ 2\) i calcula també el valor de \(y\) per a \(x=\frac12\).", r"Haz una tabla de valores de \(y=3x-2\) para \(x=-1,\ 0,\ 1,\ 2\) y calcula también el valor de \(y\) para \(x=\frac12\).", r"Make a table of values of \(y=3x-2\) for \(x=-1,\ 0,\ 1,\ 2\) and also work out \(y\) for \(x=\frac12\)."),
       D(r"x=-1:\ y=3\cdot(-1)-2=-5\qquad x=0:\ y=-2\qquad x=1:\ y=1\qquad x=2:\ y=4"),
       tv(X3, Y3) + D(r"x=\tfrac12:\ y=3\cdot\tfrac12-2=\tfrac32-2=\boxed{-\tfrac12}")),
  prob(L(r"Fes la taula de valors de \(y=4-x^2\) per a \(x=-2,\ -1,\ 0,\ 1,\ 2\) i dibuixa el gràfic.", r"Haz la tabla de valores de \(y=4-x^2\) para \(x=-2,\ -1,\ 0,\ 1,\ 2\) y dibuja la gráfica.", r"Make the table of values of \(y=4-x^2\) for \(x=-2,\ -1,\ 0,\ 1,\ 2\) and draw the graph."),
       D(r"x=-2:\ y=4-(-2)^2=4-4=0\qquad x=-1:\ y=4-1=3\qquad x=0:\ y=4"),
       tv(XC, YC) + figs(fig(F_C3)) + P(r"No estan alineats: els unim amb una corba suau. El punt més alt és \((0,\ 4)\).", r"No están alineados: los unimos con una curva suave. El punto más alto es \((0,\ 4)\).", r"They don't line up: join them with a smooth curve. The highest point is \((0,\ 4)\)."))],
 [prob(L(r"Quins d'aquests punts són del gràfic de \(y=-2x+5\)? \(A(1,\ 3)\), \(B(-2,\ 9)\), \(C(3,\ -2)\), \(D(0,\ 5)\).", r"¿Cuáles de estos puntos son de la gráfica de \(y=-2x+5\)? \(A(1,\ 3)\), \(B(-2,\ 9)\), \(C(3,\ -2)\), \(D(0,\ 5)\).", r"Which of these points are on the graph of \(y=-2x+5\)? \(A(1,\ 3)\), \(B(-2,\ 9)\), \(C(3,\ -2)\), \(D(0,\ 5)\)."),
       D(r"A:\ -2\cdot1+5=3\ \checkmark\qquad B:\ -2\cdot(-2)+5=9\ \checkmark\qquad C:\ -2\cdot3+5=-1\neq-2\ \times\qquad D:\ 0+5=5\ \checkmark"),
       P(r"Són del gràfic \(A\), \(B\) i \(D\); \(C\) <strong>no</strong>.", r"Son de la gráfica \(A\), \(B\) y \(D\); \(C\) <strong>no</strong>.", r"\(A\), \(B\) and \(D\) are on the graph; \(C\) is <strong>not</strong>.")),
  prob(L(r"a) Per a quin valor de \(x\) la funció \(y=-2x+5\) val \(-7\)? b) Per a quins valors de \(x\) la funció \(y=x^2\) val 9?", r"a) ¿Para qué valor de \(x\) la función \(y=-2x+5\) vale \(-7\)? b) ¿Para qué valores de \(x\) la función \(y=x^2\) vale 9?", r"a) For which value of \(x\) is \(y=-2x+5\) equal to \(-7\)? b) For which values of \(x\) is \(y=x^2\) equal to 9?"),
       D(r"\text{a) } -2x+5=-7\ \Rightarrow\ -2x=-12\ \Rightarrow\ \boxed{x=6}"),
       D(r"\text{b) } x^2=9\ \Rightarrow\ \boxed{x=3}\ \text{" + Lt('o', 'o', 'or') + r"}\ \boxed{x=-3}"),
       P(r"Que dos valors de \(x\) donen la mateixa \(y\) no impedeix que siga una funció: el que no pot passar és que una \(x\) tinga dues \(y\).", r"Que dos valores de \(x\) den la misma \(y\) no impide que sea una función: lo que no puede pasar es que una \(x\) tenga dos \(y\).", r"Two values of \(x\) giving the same \(y\) doesn't stop it being a function: what can't happen is one \(x\) having two values of \(y\)."))],
 [prob(L(r"Un rectangle té 20 m de perímetre. Si la base fa \(x\) metres, l'altura fa \(10-x\). a) Escriu l'equació de l'àrea \(A\). b) Fes la taula per a \(x=1,\ 2,\ \ldots,\ 9\) i el gràfic. c) Quina base dona l'àrea més gran?",
         r"Un rectángulo tiene 20 m de perímetro. Si la base mide \(x\) metros, la altura mide \(10-x\). a) Escribe la ecuación del área \(A\). b) Haz la tabla para \(x=1,\ 2,\ \ldots,\ 9\) y la gráfica. c) ¿Qué base da el área más grande?",
         r"A rectangle has a perimeter of 20 m. If the base is \(x\) metres, the height is \(10-x\). a) Write the equation for the area \(A\). b) Make the table for \(x=1,\ 2,\ \ldots,\ 9\) and the graph. c) Which base gives the biggest area?"),
       D(r"\text{a) } A=x\,(10-x)"),
       tv(XR, YR, 'x', 'A') + figs(fig(F_RA)),
       P(r"c) L'àrea és màxima per a \(x=\boxed{5\ \text{m}}\): és un quadrat de 5 m de costat i \(A=25\ \text{m}^2\).", r"c) El área es máxima para \(x=\boxed{5\ \text{m}}\): es un cuadrado de 5 m de lado y \(A=25\ \text{m}^2\).", r"c) The area is biggest for \(x=\boxed{5\ \text{m}}\): a square with 5 m sides and \(A=25\ \text{m}^2\)."))])
ck(g3(Fr(1, 2)), Fr(-1, 2)); [ck(h3(a), b) for a, b in [(1, 3), (-2, 9), (0, 5)]]; assert h3(3) == -1
ck((fr(-7) - 5) / -2, 6); assert 3 ** 2 == (-3) ** 2 == 9 and max(YR) == RA(5) == 25
s3 += practice([('★☆☆', L(r"Calcula el valor de \(y=5-3x\) per a \(x=2\) i per a \(x=-1\).", r"Calcula el valor de \(y=5-3x\) para \(x=2\) y para \(x=-1\).", r"Work out \(y=5-3x\) for \(x=2\) and for \(x=-1\).")),
                ('★★☆', L(r"És el punt \((-2,\ 5)\) del gràfic de \(y=x^2+1\)? Per a quin valor de \(x\) val 9 la funció \(y=4x-3\)?", r"¿Es el punto \((-2,\ 5)\) de la gráfica de \(y=x^2+1\)? ¿Para qué valor de \(x\) vale 9 la función \(y=4x-3\)?", r"Is the point \((-2,\ 5)\) on the graph of \(y=x^2+1\)? For which value of \(x\) is \(y=4x-3\) equal to 9?"))],
               L(r"1) \(y=-1\) i \(y=8\). &nbsp; 2) Sí: \((-2)^2+1=5\). \(4x-3=9\Rightarrow x=3\).", r"1) \(y=-1\) e \(y=8\). &nbsp; 2) Sí: \((-2)^2+1=5\). \(4x-3=9\Rightarrow x=3\).", r"1) \(y=-1\) and \(y=8\). &nbsp; 2) Yes: \((-2)^2+1=5\). \(4x-3=9\Rightarrow x=3\)."))
ck(lin(-3, 5)(2), -1); ck(lin(-3, 5)(-1), 8); ck((-2) ** 2 + 1, 5); ck(Fr(12, 4), 3)

# =====================================================================
# 10.4 Funció de proporcionalitat: y = mx
# =====================================================================
W6 = (-5, 5, -6, 6)
F_PROP = pla(W6, fns=[(2, 0, 'c0'), (Fr(1, 2), 0, 'c1'), (-1, 0, 'c2')], labs=[(2.6, 5.6, 'y = 2x', 'l0'), (4.2, 2.8, 'y = x/2', 'l1'), (-4.2, 5.0, 'y = −x', 'l2')], W=260)
f3 = lin(3)
TV3 = [ck(f3(k), v) for k, v in zip([-2, -1, 0, 1, 2], [-6, -3, 0, 3, 6])]
F_Y3 = pla((-3, 3, -7, 7), fns=[(3, 0, 'c0')], pts=[(k, 3 * k, None, 'p0') for k in (-2, -1, 0, 1, 2)], W=200, ys=2)
KGP = [1, 2, 3, 4]
F_POMES = pla((0, 4.6, 0, 7.4), fns=[('1.5', 0, 'c0', 0, 4.4)], pts=[(k, fr('1.5') * k, None, 'p0') for k in [0] + KGP], W=220, H=220, xl='kg', yl='€', ys=1.5, gy=1.5)

s4 = box('def', L('Funció de proporcionalitat directa', 'Función de proporcionalidad directa', 'Direct proportion function'),
  P(r"Si dues magnituds són <strong>directament proporcionals</strong> (unitat 6), el quocient \(\frac{y}{x}\) és sempre el mateix nombre \(m\), la <strong>constant de proporcionalitat</strong>. Aleshores \(y=m\cdot x\). Per exemple, si les pomes valen 1,50 € el kg:",
    r"Si dos magnitudes son <strong>directamente proporcionales</strong> (unidad 6), el cociente \(\frac{y}{x}\) es siempre el mismo número \(m\), la <strong>constante de proporcionalidad</strong>. Entonces \(y=m\cdot x\). Por ejemplo, si las manzanas valen 1,50 € el kg:",
    r"If two quantities are <strong>directly proportional</strong> (unit 6), the quotient \(\frac{y}{x}\) is always the same number \(m\), the <strong>constant of proportionality</strong>. Then \(y=m\cdot x\). For example, if apples cost €1.50 per kg:")
  + '<div class="gout"><div class="gcol">' + tv(KGP, ['1{,}5', '3', '4{,}5', '6'], 'kg', '€')
  + D(r"\frac{1{,}5}{1}=\frac{3}{2}=\frac{4{,}5}{3}=\frac{6}{4}=1{,}5\ \Rightarrow\ y=1{,}5x") + '</div>' + F_POMES + '</div>'
  + D(r"y=m\cdot x")
  + ul(L(r"Es diu <strong>funció de proporcionalitat</strong> (directa). El nombre \(m\) és el <strong>pendent</strong> de la recta (apartat 10.5).", r"Se llama <strong>función de proporcionalidad</strong> (directa). El número \(m\) es la <strong>pendiente</strong> de la recta (apartado 10.5).", r"It's called a <strong>direct proportion function</strong>. The number \(m\) is the <strong>slope</strong> of the line (section 10.5)."),
       L(r"El seu gràfic és sempre una <strong>recta que passa per l'origen</strong> \((0,\ 0)\): si \(x=0\), \(y=m\cdot0=0\).", r"Su gráfica es siempre una <strong>recta que pasa por el origen</strong> \((0,\ 0)\): si \(x=0\), \(y=m\cdot0=0\).", r"Its graph is always a <strong>straight line through the origin</strong> \((0,\ 0)\): if \(x=0\), \(y=m\cdot0=0\)."),
       L(r"Per a dibuixar-la n'hi ha prou amb <strong>dos punts</strong>: l'origen i un altre. És millor calcular-ne un tercer per a comprovar que estan alineats.",
         r"Para dibujarla basta con <strong>dos puntos</strong>: el origen y otro. Es mejor calcular un tercero para comprobar que están alineados.",
         r"To draw it, <strong>two points</strong> are enough: the origin and one more. It's best to work out a third one to check they line up."))
  + P(r"Exemple: \(y=3x\).", r"Ejemplo: \(y=3x\).", r"Example: \(y=3x\).")
  + '<div class="gout"><div class="gcol">' + tv([-2, -1, 0, 1, 2], TV3) + P(r"Cada vegada que \(x\) augmenta 1, \(y\) augmenta 3. Si \(x\) es duplica, \(y\) també es duplica.", r"Cada vez que \(x\) aumenta 1, \(y\) aumenta 3. Si \(x\) se duplica, \(y\) también se duplica.", r"Each time \(x\) goes up by 1, \(y\) goes up by 3. If \(x\) doubles, \(y\) doubles too.") + '</div>' + F_Y3 + '</div>')
[ck(fr('1.5') * k, v) for k, v in zip(KGP, ['1.5', '3', '4.5', '6'])]

s4 += box('prop', L('Com és la recta segons m', 'Cómo es la recta según m', 'What the line looks like depending on m'),
  ul(L(r"Si \(m>0\), la recta és <strong>creixent</strong> (puja d'esquerra a dreta) i passa pels quadrants I i III.", r"Si \(m>0\), la recta es <strong>creciente</strong> (sube de izquierda a derecha) y pasa por los cuadrantes I y III.", r"If \(m>0\), the line is <strong>increasing</strong> (goes up from left to right) and passes through quadrants I and III."),
     L(r"Si \(m<0\), la recta és <strong>decreixent</strong> (baixa) i passa pels quadrants II i IV.", r"Si \(m<0\), la recta es <strong>decreciente</strong> (baja) y pasa por los cuadrantes II y IV.", r"If \(m<0\), the line is <strong>decreasing</strong> (goes down) and passes through quadrants II and IV."),
     L(r"Com més gran és \(m\) (sense mirar el signe), <strong>més inclinada</strong> és la recta.", r"Cuanto más grande es \(m\) (sin mirar el signo), <strong>más inclinada</strong> está la recta.", r"The bigger \(m\) is (ignoring the sign), the <strong>steeper</strong> the line."))
  + figs(fig(F_PROP, L('Tres rectes que passen per l\'origen', 'Tres rectas que pasan por el origen', 'Three lines through the origin')))
  + P(r"<strong>Trobar l'equació</strong>: si la recta passa per l'origen i pel punt \((4,\ 10)\), aleshores \(m=\frac{y}{x}=\frac{10}{4}=2{,}5\) i l'equació és \(y=2{,}5x\).",
      r"<strong>Hallar la ecuación</strong>: si la recta pasa por el origen y por el punto \((4,\ 10)\), entonces \(m=\frac{y}{x}=\frac{10}{4}=2{,}5\) y la ecuación es \(y=2{,}5x\).",
      r"<strong>Finding the equation</strong>: if the line goes through the origin and the point \((4,\ 10)\), then \(m=\frac{y}{x}=\frac{10}{4}=2.5\) and the equation is \(y=2.5x\).")
  + widget('w-m', '📈', L('Explora y = m·x', 'Explora y = m·x', 'Explore y = m·x'),
           ['<div class="wrow">' + rng('m', -3, 3, 0.5, 2, 'm') + '</div>'], out='<div class="gout"></div>')
  + drill('img0', 'Entrena: calcula la y', 'Entrena: calcula la y', 'Train: work out y')
  + drill('m0', 'Entrena: troba la constant m', 'Entrena: halla la constante m', 'Train: find the constant m'))
ck(fr(10) / 4, '2.5')

T_A = ([1, 2, 3], [4, 8, 12]); T_B = ([1, 2, 3], [3, 5, 7]); T_C = ([2, 4, 6], [1, 2, 3])
def isprop(T): return len({fr(y) / x for x, y in zip(*T)}) == 1
assert isprop(T_A) and not isprop(T_B) and isprop(T_C)
F_P2 = pla(W6, fns=[(-2, 0, 'c0'), (Fr(1, 2), 0, 'c1')], pts=[(-2, 4, None, 'p0'), (2, -4, None, 'p0'), (-4, -2, None, 'p1'), (4, 2, None, 'p1')], labs=[(-3.6, 5.4, 'y = −2x', 'l0'), (3.9, 3.0, 'y = x/2', 'l1')], W=240)
F_EUR = pla((0, 55, 0, 66), fns=[('1.1', 0, 'c0', 0, 55)], pts=[(30, 33, None, 'p0'), (50, 55, None, 'p1')], proj=[(30, 33), (50, 55)], W=280, H=240, xs=10, gx=5, ys=10, gy=5, xl='€', yl='$')
ck(fr('1.1') * 30, 33); ck(fr(55) / fr('1.1'), 50)
s4 += levels(
 [prob(L(r"Quines d'aquestes taules corresponen a una funció de proporcionalitat? Escriu-ne l'equació.", r"¿Cuáles de estas tablas corresponden a una función de proporcionalidad? Escribe su ecuación.", r"Which of these tables come from a direct proportion function? Write its equation.")
       + '<div class="tv2">' + tv(*T_A, 'x', 'y') + tv(*T_B, 'x', 'y') + tv(*T_C, 'x', 'y') + '</div>',
       P(r"Calculem \(\frac{y}{x}\) en cada columna: si sempre dona el mateix, és de proporcionalitat.", r"Calculamos \(\frac{y}{x}\) en cada columna: si siempre da lo mismo, es de proporcionalidad.", r"Work out \(\frac{y}{x}\) in each column: if it's always the same, it's direct proportion."),
       ul(L(r"Primera: \(\frac41=\frac82=\frac{12}{3}=4\). <strong>Sí</strong>: \(y=4x\).", r"Primera: \(\frac41=\frac82=\frac{12}{3}=4\). <strong>Sí</strong>: \(y=4x\).", r"First: \(\frac41=\frac82=\frac{12}{3}=4\). <strong>Yes</strong>: \(y=4x\)."),
          L(r"Segona: \(\frac31=3\) però \(\frac52=2{,}5\). <strong>No</strong>.", r"Segunda: \(\frac31=3\) pero \(\frac52=2{,}5\). <strong>No</strong>.", r"Second: \(\frac31=3\) but \(\frac52=2.5\). <strong>No</strong>."),
          L(r"Tercera: \(\frac12=\frac24=\frac36=0{,}5\). <strong>Sí</strong>: \(y=0{,}5x\).", r"Tercera: \(\frac12=\frac24=\frac36=0{,}5\). <strong>Sí</strong>: \(y=0{,}5x\).", r"Third: \(\frac12=\frac24=\frac36=0.5\). <strong>Yes</strong>: \(y=0.5x\)."))),
  prob(L(r"El perímetre d'un hexàgon regular depén del costat. Escriu l'equació, digues si és de proporcionalitat i calcula el perímetre si el costat fa 3,5 cm.", r"El perímetro de un hexágono regular depende del lado. Escribe la ecuación, di si es de proporcionalidad y calcula el perímetro si el lado mide 3,5 cm.", r"The perimeter of a regular hexagon depends on its side. Write the equation, say whether it is direct proportion and work out the perimeter if the side is 3.5 cm."),
       P(r"Té 6 costats iguals: \(P=6l\). És de la forma \(y=mx\) amb \(m=6\): <strong>sí</strong> que és de proporcionalitat.", r"Tiene 6 lados iguales: \(P=6l\). Es de la forma \(y=mx\) con \(m=6\): <strong>sí</strong> es de proporcionalidad.", r"It has 6 equal sides: \(P=6l\). It has the form \(y=mx\) with \(m=6\): it <strong>is</strong> direct proportion."),
       D(r"P=6\cdot3{,}5=\boxed{21\ \text{cm}}"))],
 [prob(L(r"Representa en els mateixos eixos \(y=-2x\) i \(y=\frac{x}{2}\). Quina és creixent? Quina és més inclinada?", r"Representa en los mismos ejes \(y=-2x\) e \(y=\frac{x}{2}\). ¿Cuál es creciente? ¿Cuál está más inclinada?", r"Plot \(y=-2x\) and \(y=\frac{x}{2}\) on the same axes. Which one is increasing? Which is steeper?"),
       P(r"Punts de \(y=-2x\): \((-2,\ 4)\), \((0,\ 0)\), \((2,\ -4)\). Punts de \(y=\frac x2\): \((-4,\ -2)\), \((0,\ 0)\), \((4,\ 2)\) (triem \(x\) parells perquè ixquen enters).",
         r"Puntos de \(y=-2x\): \((-2,\ 4)\), \((0,\ 0)\), \((2,\ -4)\). Puntos de \(y=\frac x2\): \((-4,\ -2)\), \((0,\ 0)\), \((4,\ 2)\) (elegimos \(x\) pares para que salgan enteros).",
         r"Points of \(y=-2x\): \((-2,\ 4)\), \((0,\ 0)\), \((2,\ -4)\). Points of \(y=\frac x2\): \((-4,\ -2)\), \((0,\ 0)\), \((4,\ 2)\) (we pick even \(x\) so the results are whole numbers).") + figs(fig(F_P2)),
       P(r"\(y=\frac x2\) és <strong>creixent</strong> (\(m=0{,}5>0\)); \(y=-2x\) és decreixent i <strong>més inclinada</strong> (2 és més gran que 0,5).", r"\(y=\frac x2\) es <strong>creciente</strong> (\(m=0{,}5>0\)); \(y=-2x\) es decreciente y <strong>más inclinada</strong> (2 es mayor que 0,5).", r"\(y=\frac x2\) is <strong>increasing</strong> (\(m=0.5>0\)); \(y=-2x\) is decreasing and <strong>steeper</strong> (2 is bigger than 0.5).")),
  prob(L(r"Una recta passa per l'origen i pel punt \((4,\ 10)\). Escriu-ne l'equació i comprova si els punts \((-2,\ -5)\) i \((6,\ 14)\) hi són.", r"Una recta pasa por el origen y por el punto \((4,\ 10)\). Escribe su ecuación y comprueba si los puntos \((-2,\ -5)\) y \((6,\ 14)\) están en ella.", r"A line goes through the origin and the point \((4,\ 10)\). Write its equation and check whether \((-2,\ -5)\) and \((6,\ 14)\) are on it."),
       D(r"m=\frac{10}{4}=2{,}5\ \Rightarrow\ \boxed{y=2{,}5x}"),
       D(r"x=-2:\ 2{,}5\cdot(-2)=-5\ \checkmark\qquad x=6:\ 2{,}5\cdot6=15\neq14\ \times"),
       P(r"\((-2,\ -5)\) <strong>sí</strong> que és de la recta; \((6,\ 14)\) <strong>no</strong>.", r"\((-2,\ -5)\) <strong>sí</strong> es de la recta; \((6,\ 14)\) <strong>no</strong>.", r"\((-2,\ -5)\) <strong>is</strong> on the line; \((6,\ 14)\) <strong>isn't</strong>."))],
 [prob(L(r"Un dia, 1 euro val 1,10 dòlars. Escriu la funció que passa d'euros (\(x\)) a dòlars (\(y\)), dibuixa'n el gràfic i calcula: a) quants dòlars són 30 €; b) quants euros són 55 $.",
         r"Un día, 1 euro vale 1,10 dólares. Escribe la función que pasa de euros (\(x\)) a dólares (\(y\)), dibuja su gráfica y calcula: a) cuántos dólares son 30 €; b) cuántos euros son 55 $.",
         r"One day, 1 euro is worth 1.10 dollars. Write the function that converts euros (\(x\)) into dollars (\(y\)), draw its graph and work out: a) how many dollars €30 is; b) how many euros $55 is."),
       D(r"y=1{,}1\cdot x") + figs(fig(F_EUR)),
       D(r"\text{a) } y=1{,}1\cdot30=\boxed{33\ \$}\qquad \text{b) } 1{,}1\cdot x=55\ \Rightarrow\ x=\frac{55}{1{,}1}=\boxed{50\ \text{€}}"),
       P(r"En el gràfic: des de 30 en l'eix horitzontal pugem fins a la recta i llegim 33; des de 55 en l'eix vertical anem fins a la recta i baixem a 50.", r"En la gráfica: desde 30 en el eje horizontal subimos hasta la recta y leemos 33; desde 55 en el eje vertical vamos hasta la recta y bajamos a 50.", r"On the graph: from 30 on the horizontal axis go up to the line and read 33; from 55 on the vertical axis go across to the line and down to 50."))])
ck(6 * fr('3.5'), 21)
s4 += practice([('★☆☆', L(r"Fes la taula de \(y=-x\) per a \(x=-2,\ 0,\ 2\). És creixent o decreixent?", r"Haz la tabla de \(y=-x\) para \(x=-2,\ 0,\ 2\). ¿Es creciente o decreciente?", r"Make the table of \(y=-x\) for \(x=-2,\ 0,\ 2\). Is it increasing or decreasing?")),
                ('★★☆', L(r"Una recta passa per l'origen i per \((-3,\ 6)\). Quina és la seua equació?", r"Una recta pasa por el origen y por \((-3,\ 6)\). ¿Cuál es su ecuación?", r"A line goes through the origin and \((-3,\ 6)\). What is its equation?"))],
               L(r"1) \(y=2,\ 0,\ -2\): decreixent (\(m=-1\)). &nbsp; 2) \(m=\frac{6}{-3}=-2\): \(y=-2x\).", r"1) \(y=2,\ 0,\ -2\): decreciente (\(m=-1\)). &nbsp; 2) \(m=\frac{6}{-3}=-2\): \(y=-2x\).", r"1) \(y=2,\ 0,\ -2\): decreasing (\(m=-1\)). &nbsp; 2) \(m=\frac{6}{-3}=-2\): \(y=-2x\)."))
ck(fr(6) / -3, -2)

# =====================================================================
# 10.5 Pendent d'una recta
# =====================================================================
A5, B5 = (1, 1), (4, 7)
ck(slope(A5, B5), 2)
F_PEN = pla((-1, 6, -1, 9), fns=[(2, -1, 'c0')], curves=[([A5, (4, 1), B5], 'c1 stp')], pts=[(1, 1, 'A', 'p0', -14, -6), (4, 7, 'B', 'p0', 8, 4)],
            labs=[(2.5, 0.35, '+3', 'l1'), (4.55, 4.2, '+6', 'l1')], W=220, H=280)
F_SIG = pla((-4, 4, -4, 4), fns=[(Fr(3, 2), 0, 'c0'), (Fr(-1, 2), 1, 'c1'), (0, -2, 'c2')], labs=[(2.9, 3.7, 'm > 0', 'l0'), (-3.0, 3.1, 'm < 0', 'l1'), (2.8, -1.4, 'm = 0', 'l2')], W=220)
F_FR = pla((-1, 7, -1, 5), fns=[(Fr(2, 3), 0, 'c0')], curves=[([(0, 0), (3, 0), (3, 2)], 'c1 stp'), ([(3, 2), (6, 2), (6, 4)], 'c1 stp')], pts=[(0, 0, None, 'p0'), (3, 2, None, 'p0'), (6, 4, None, 'p0')],
           labs=[(1.6, 0.35, '+3', 'l1'), (3.5, 1.1, '+2', 'l1')], W=220, H=180)

s5 = box('def', L('El pendent d\'una recta', 'La pendiente de una recta', 'The slope of a line'),
  P(r"El <strong>pendent</strong> \(m\) d'una recta mesura com d'inclinada està: és el que <strong>augmenta</strong> (o disminueix) la \(y\) quan la \(x\) <strong>augmenta 1</strong>. Si la recta passa per dos punts \(A(x_1,\ y_1)\) i \(B(x_2,\ y_2)\):",
    r"La <strong>pendiente</strong> \(m\) de una recta mide lo inclinada que está: es lo que <strong>aumenta</strong> (o disminuye) la \(y\) cuando la \(x\) <strong>aumenta 1</strong>. Si la recta pasa por dos puntos \(A(x_1,\ y_1)\) y \(B(x_2,\ y_2)\):",
    r"The <strong>slope</strong> \(m\) of a line measures how steep it is: it's how much \(y\) <strong>goes up</strong> (or down) when \(x\) <strong>goes up by 1</strong>. If the line goes through two points \(A(x_1,\ y_1)\) and \(B(x_2,\ y_2)\):")
  + D(r"m=\frac{\text{" + Lt('variació de la ', 'variación de la ', 'change in ') + r"}y}{\text{" + Lt('variació de la ', 'variación de la ', 'change in ') + r"}x}=\frac{y_2-y_1}{x_2-x_1}")
  + '<div class="gout">' + F_PEN + '<div class="gcol">'
  + P(r"Des d'\(A(1,\ 1)\) fins a \(B(4,\ 7)\) avancem 3 cap a la dreta i pugem 6:", r"Desde \(A(1,\ 1)\) hasta \(B(4,\ 7)\) avanzamos 3 hacia la derecha y subimos 6:", r"From \(A(1,\ 1)\) to \(B(4,\ 7)\) we move 3 to the right and go up 6:")
  + D(r"m=\frac{7-1}{4-1}=\frac{6}{3}=2")
  + P(r"Per cada unitat que avancem cap a la dreta, la recta puja 2.", r"Por cada unidad que avanzamos hacia la derecha, la recta sube 2.", r"For every unit we move to the right, the line goes up 2.")
  + '</div></div>'
  + note(r"Restem sempre en el mateix ordre a dalt i a baix (\(B\) menys \(A\) o \(A\) menys \(B\)): \(\frac{1-7}{1-4}=\frac{-6}{-3}=2\) també.",
         r"Restamos siempre en el mismo orden arriba y abajo (\(B\) menos \(A\) o \(A\) menos \(B\)): \(\frac{1-7}{1-4}=\frac{-6}{-3}=2\) también.",
         r"Always subtract in the same order on top and at the bottom (\(B\) minus \(A\) or \(A\) minus \(B\)): \(\frac{1-7}{1-4}=\frac{-6}{-3}=2\) as well."))
ck(Fr(1 - 7, 1 - 4), 2)

s5 += box('prop', L('Què ens diu el pendent', 'Qué nos dice la pendiente', 'What the slope tells us'),
  '<div class="gout">' + F_SIG + '<div class="gcol">'
  + ul(L(r"\(m>0\): la recta <strong>puja</strong> (funció creixent).", r"\(m>0\): la recta <strong>sube</strong> (función creciente).", r"\(m>0\): the line <strong>goes up</strong> (increasing function)."),
       L(r"\(m<0\): la recta <strong>baixa</strong> (funció decreixent).", r"\(m<0\): la recta <strong>baja</strong> (función decreciente).", r"\(m<0\): the line <strong>goes down</strong> (decreasing function)."),
       L(r"\(m=0\): la recta és <strong>horitzontal</strong> (funció constant).", r"\(m=0\): la recta es <strong>horizontal</strong> (función constante).", r"\(m=0\): the line is <strong>horizontal</strong> (constant function)."),
       L(r"Com més gran és \(m\) sense el signe, <strong>més inclinada</strong>: \(y=5x\) és més inclinada que \(y=2x\), i \(y=-3x\) més que \(y=-x\).", r"Cuanto más grande es \(m\) sin el signo, <strong>más inclinada</strong>: \(y=5x\) está más inclinada que \(y=2x\), e \(y=-3x\) más que \(y=-x\).", r"The bigger \(m\) is without its sign, the <strong>steeper</strong>: \(y=5x\) is steeper than \(y=2x\), and \(y=-3x\) steeper than \(y=-x\)."))
  + '</div></div>'
  + P(r"<strong>Pendent fraccionari.</strong> Si \(m=\frac23\), per cada 3 unitats que avancem cap a la dreta, la recta puja 2. Així es dibuixa fàcilment sense decimals:",
      r"<strong>Pendiente fraccionaria.</strong> Si \(m=\frac23\), por cada 3 unidades que avanzamos hacia la derecha, la recta sube 2. Así se dibuja fácilmente sin decimales:",
      r"<strong>Fractional slope.</strong> If \(m=\frac23\), for every 3 units to the right the line goes up 2. That way it's easy to draw without decimals:")
  + figs(fig(F_FR, L('\\(y=\\frac23x\\): 3 a la dreta, 2 amunt', '\\(y=\\frac23x\\): 3 a la derecha, 2 arriba', '\\(y=\\frac23x\\): 3 right, 2 up')))
  + widget('w-slope', '📐', L('El pendent entre dos punts', 'La pendiente entre dos puntos', 'The slope between two points'),
           ['<div class="wrow">' + tin('a', 'A', '(1, 1)', 'w') + tin('b', 'B', '(4, 7)', 'w') + '</div>',
            quick([('(1, 1)|(4, 7)', 'm = 2'), ('(-2, 4)|(2, -4)', 'm = −2'), ('(0, 1)|(3, 3)', 'm = 2/3'), ('(-3, 2)|(4, 2)', 'm = 0')])],
           out='<div class="gout"></div>')
  + drill('slope2', 'Entrena: pendent per dos punts', 'Entrena: pendiente por dos puntos', 'Train: slope through two points')
  + drill('slopeg', 'Entrena: llig el pendent en el gràfic', 'Entrena: lee la pendiente en la gráfica', 'Train: read the slope off the graph'))
ck(Fr(2, 3) * 3, 2)

R1, R2 = ((-1, 4), (2, -2)), ((0, -3), (4, 3))
ck(slope(*R1), -2); ck(slope(*R2), '1.5')
F_RL = pla((-1, 6, -1, 5), fns=[(Fr(3, 4), Fr(1, 4), 'c0')], curves=[([(1, 1), (5, 1), (5, 4)], 'c1 stp')], pts=[(1, 1, None, 'p0'), (5, 4, None, 'p0')], W=220, H=180)
ck(slope((1, 1), (5, 4)), Fr(3, 4))
PA, PB, PC = (0, 1), (2, 4), (6, 10)
ck(slope(PA, PB), Fr(3, 2)); ck(slope(PB, PC), Fr(3, 2))
s5 += levels(
 [prob(L(r"Calcula el pendent de la recta que passa per: a) \((-1,\ 4)\) i \((2,\ -2)\); b) \((0,\ -3)\) i \((4,\ 3)\). Digues si és creixent o decreixent.", r"Calcula la pendiente de la recta que pasa por: a) \((-1,\ 4)\) y \((2,\ -2)\); b) \((0,\ -3)\) y \((4,\ 3)\). Di si es creciente o decreciente.", r"Work out the slope of the line through: a) \((-1,\ 4)\) and \((2,\ -2)\); b) \((0,\ -3)\) and \((4,\ 3)\). Say whether it is increasing or decreasing."),
       D(r"\text{a) } m=\frac{-2-4}{2-(-1)}=\frac{-6}{3}=\boxed{-2}"),
       P(r"Negatiu: <strong>decreixent</strong>.", r"Negativa: <strong>decreciente</strong>.", r"Negative: <strong>decreasing</strong>."),
       D(r"\text{b) } m=\frac{3-(-3)}{4-0}=\frac{6}{4}=\boxed{1{,}5}") + P(r"Positiu: <strong>creixent</strong>.", r"Positiva: <strong>creciente</strong>.", r"Positive: <strong>increasing</strong>.")),
  prob(L(r"Llig el pendent d'aquesta recta en el gràfic.", r"Lee la pendiente de esta recta en la gráfica.", r"Read the slope of this line off the graph.") + figs(fig(F_RL)),
       P(r"Busquem dos punts de la recta que caiguen en la quadrícula: \((1,\ 1)\) i \((5,\ 4)\).", r"Buscamos dos puntos de la recta que caigan en la cuadrícula: \((1,\ 1)\) y \((5,\ 4)\).", r"Find two points on the line that sit on the grid: \((1,\ 1)\) and \((5,\ 4)\)."),
       P(r"Avancem 4 cap a la dreta i pugem 3: \(m=\boxed{\frac34}\).", r"Avanzamos 4 hacia la derecha y subimos 3: \(m=\boxed{\frac34}\).", r"Move 4 to the right and go up 3: \(m=\boxed{\frac34}\)."))],
 [prob(L(r"Ordena les rectes de menys a més inclinada i digues quines són creixents: \(y=-4x\), \(y=\frac12x\), \(y=3x\), \(y=-x\).", r"Ordena las rectas de menos a más inclinada y di cuáles son crecientes: \(y=-4x\), \(y=\frac12x\), \(y=3x\), \(y=-x\).", r"Put the lines in order from least to most steep and say which are increasing: \(y=-4x\), \(y=\frac12x\), \(y=3x\), \(y=-x\)."),
       P(r"Comparem els pendents sense el signe: \(\frac12<1<3<4\).", r"Comparamos las pendientes sin el signo: \(\frac12<1<3<4\).", r"Compare the slopes without their signs: \(\frac12<1<3<4\)."),
       P(r"Ordre: \(y=\frac12x\), \(y=-x\), \(y=3x\), \(y=-4x\). Són creixents les de pendent positiu: \(y=\frac12x\) i \(y=3x\).", r"Orden: \(y=\frac12x\), \(y=-x\), \(y=3x\), \(y=-4x\). Son crecientes las de pendiente positiva: \(y=\frac12x\) e \(y=3x\).", r"Order: \(y=\frac12x\), \(y=-x\), \(y=3x\), \(y=-4x\). The ones with positive slope are increasing: \(y=\frac12x\) and \(y=3x\).")),
  prob(L(r"Un senyal de trànsit avisa que una carretera té un pendent del 8 %: puja 8 m per cada 100 m que avancem en horitzontal. Quin és el pendent \(m\)? Quant pujarem en 2,5 km?",
         r"Una señal de tráfico avisa de que una carretera tiene una pendiente del 8 %: sube 8 m por cada 100 m que avanzamos en horizontal. ¿Cuál es la pendiente \(m\)? ¿Cuánto subiremos en 2,5 km?",
         r"A road sign warns that a road has an 8 % gradient: it rises 8 m for every 100 m travelled horizontally. What is the slope \(m\)? How much will we climb over 2.5 km?"),
       D(r"m=\frac{8}{100}=0{,}08"),
       P(r"2,5 km són 2.500 m en horitzontal:", r"2,5 km son 2.500 m en horizontal:", r"2.5 km is 2,500 m horizontally:") + D(r"0{,}08\cdot2500=\boxed{200\ \text{m}}"))],
 [prob(L(r"Estan alineats els punts \(A(0,\ 1)\), \(B(2,\ 4)\) i \(C(6,\ 10)\)? I \(A\), \(B\) i \(D(4,\ 8)\)?", r"¿Están alineados los puntos \(A(0,\ 1)\), \(B(2,\ 4)\) y \(C(6,\ 10)\)? ¿Y \(A\), \(B\) y \(D(4,\ 8)\)?", r"Do the points \(A(0,\ 1)\), \(B(2,\ 4)\) and \(C(6,\ 10)\) lie on a line? And \(A\), \(B\) and \(D(4,\ 8)\)?"),
       P(r"Tres punts estan alineats si el pendent de \(A\) a \(B\) és el mateix que el de \(B\) a l'altre punt.", r"Tres puntos están alineados si la pendiente de \(A\) a \(B\) es la misma que la de \(B\) al otro punto.", r"Three points lie on a line if the slope from \(A\) to \(B\) is the same as from \(B\) to the other point."),
       D(r"m_{AB}=\frac{4-1}{2-0}=\frac32\qquad m_{BC}=\frac{10-4}{6-2}=\frac64=\frac32\ \checkmark\qquad m_{BD}=\frac{8-4}{4-2}=2\neq\frac32\ \times"),
       P(r"\(A\), \(B\) i \(C\) <strong>sí</strong> que estan alineats; \(A\), \(B\) i \(D\) <strong>no</strong>.", r"\(A\), \(B\) y \(C\) <strong>sí</strong> están alineados; \(A\), \(B\) y \(D\) <strong>no</strong>.", r"\(A\), \(B\) and \(C\) <strong>do</strong> lie on a line; \(A\), \(B\) and \(D\) <strong>don't</strong>."))])
ck(fr('0.08') * 2500, 200); ck(slope(PB, (4, 8)), 2)
s5 += practice([('★☆☆', L(r"Calcula el pendent de la recta que passa per \((2,\ 3)\) i \((5,\ 9)\).", r"Calcula la pendiente de la recta que pasa por \((2,\ 3)\) y \((5,\ 9)\).", r"Work out the slope of the line through \((2,\ 3)\) and \((5,\ 9)\).")),
                ('★★☆', L(r"Una rampa puja 1,2 m en 10 m de recorregut horitzontal. Quin és el seu pendent? Expressa'l en tant per cent.", r"Una rampa sube 1,2 m en 10 m de recorrido horizontal. ¿Cuál es su pendiente? Exprésala en tanto por ciento.", r"A ramp rises 1.2 m over 10 m horizontally. What is its slope? Give it as a percentage."))],
               L(r"1) \(m=\frac{9-3}{5-2}=\frac63=2\). &nbsp; 2) \(m=\frac{1{,}2}{10}=0{,}12\): un 12 %.", r"1) \(m=\frac{9-3}{5-2}=\frac63=2\). &nbsp; 2) \(m=\frac{1{,}2}{10}=0{,}12\): un 12 %.", r"1) \(m=\frac{9-3}{5-2}=\frac63=2\). &nbsp; 2) \(m=\frac{1.2}{10}=0.12\): 12 %."))
ck(slope((2, 3), (5, 9)), 2); ck(fr('1.2') / 10, '0.12')
