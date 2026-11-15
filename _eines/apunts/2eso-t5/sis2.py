# Apartats 5.4-5.7 dels apunts de la Unitat 5 de 2n ESO (Sistemes d'equacions): igualació, reducció (i quin mètode triem),
# mètode gràfic (i quantes solucions pot tindre un sistema) i problemes. Les solucions es comproven amb sympy (cs, ok, same).
from comu import *

# =====================================================================
# 5.4 Mètode d'igualació
# =====================================================================
s4 = box('prop', L("Mètode d'igualació", 'Método de igualación', 'Equalisation method'),
  ol(L(r"<strong>Aïllem la mateixa incògnita</strong> en les dues equacions.", r"<strong>Despejamos la misma incógnita</strong> en las dos ecuaciones.", r"<strong>Isolate the same unknown</strong> in both equations."),
     L(r"<strong>Igualem</strong> les dues expressions: si les dues són iguals a la mateixa incògnita, són iguals entre si.", r"<strong>Igualamos</strong> las dos expresiones: si las dos son iguales a la misma incógnita, son iguales entre sí.", r"<strong>Set</strong> the two expressions <strong>equal</strong>: both equal the same unknown, so they equal each other."),
     L(r"<strong>Resolem</strong> l'equació que en resulta, amb una sola incògnita.", r"<strong>Resolvemos</strong> la ecuación resultante, con una sola incógnita.", r"<strong>Solve</strong> the resulting equation in one unknown."),
     L(r"<strong>Substituïm</strong> el valor en qualsevol de les dues expressions aïllades.", r"<strong>Sustituimos</strong> el valor en cualquiera de las dos expresiones despejadas.", r"<strong>Substitute</strong> the value into either isolated expression."),
     L(r"<strong>Comprovem</strong> la solució.", r"<strong>Comprobamos</strong> la solución.", r"<strong>Check</strong> the solution."))
  + D(SY('x+y=5', 'x-2y=-1') + r"\qquad\Rightarrow\qquad " + SY('x=5-y', 'x=-1+2y'))
  + D(R([r"5-y=-1+2y", r"-y-2y=-1-5", r"-3y=-6", r"y=2"]) + r"\qquad x=5-2=3")
  + P(r"Comprovació: \(3+2=5\) ✓ i \(3-4=-1\) ✓. Solució: \(x=3,\ y=2\).", r"Comprobación: \(3+2=5\) ✓ y \(3-4=-1\) ✓. Solución: \(x=3,\ y=2\).", r"Check: \(3+2=5\) ✓ and \(3-4=-1\) ✓. Solution: \(x=3,\ y=2\).")
  + note(r"La igualació és molt còmoda quan la mateixa incògnita ja està aïllada en les dues equacions, com en \(y=2x-1,\ y=x+3\): només cal igualar.", r"La igualación es muy cómoda cuando la misma incógnita ya está despejada en las dos ecuaciones, como en \(y=2x-1,\ y=x+3\): solo hay que igualar.", r"Equalisation is very handy when the same unknown is already isolated in both equations, as in \(y=2x-1,\ y=x+3\): just set them equal."))
cs('x+y=5', 'x-2y=-1', (3, 2))
s4 += box('prop', L('I si en aïllar apareix un denominador?', '¿Y si al despejar aparece un denominador?', 'What if isolating gives a fraction?'),
  P(r"Si la incògnita té un coeficient diferent de 1, en aïllar-la apareix una fracció. Després d'igualar, la traiem com en les equacions amb denominadors de la unitat 4: multipliquem els dos membres pel denominador.",
    r"Si la incógnita tiene un coeficiente distinto de 1, al despejarla aparece una fracción. Después de igualar, la quitamos como en las ecuaciones con denominadores de la unidad 4: multiplicamos los dos miembros por el denominador.",
    r"If the unknown has a coefficient other than 1, isolating it gives a fraction. After setting the expressions equal, clear it as with the equations with fractions in unit 4: multiply both sides by the denominator.")
  + D(SY('2x-y=3', '3x+2y=8') + r"\qquad\Rightarrow\qquad " + SY('y=2x-3', r'y=\frac{8-3x}{2}'))
  + D(R([r"2x-3=\frac{8-3x}{2}", r"2(2x-3)=8-3x", r"4x-6=8-3x", r"7x=14", r"x=2"]) + r"\qquad y=2\cdot2-3=1"))
cs('2x-y=3', '3x+2y=8', (2, 1)); same('2(2x-3)=8-3x', '7x=14')
s4 += solver('w-igu', 'igu', L('Igualació pas a pas', 'Igualación paso a paso', 'Equalisation step by step'), 'x+y=5', 'x-2y=-1',
             [('x+y=5', 'x-2y=-1'), ('y=2x-1', 'y=x+3'), ('x=2y+1', 'x=7-y'), ('y=3x', 'x+y=8'), ('2x-y=3', '3x+2y=8'), ('x+3y=7', 'x-y=-1')])
s4 += drill('igu', "Entrena: mètode d'igualació", 'Entrena: método de igualación', 'Train: equalisation method')
s4 += levels(
 [prob(L(r"Resol \(" + SY('y=2x-1', 'y=x+3') + r"\).", r"Resuelve \(" + SY('y=2x-1', 'y=x+3') + r"\).", r"Solve \(" + SY('y=2x-1', 'y=x+3') + r"\)."),
       P(r"La \(y\) ja està aïllada en les dues: igualem.", r"La \(y\) ya está despejada en las dos: igualamos.", r"\(y\) is already isolated in both: set them equal."),
       D(R([r"2x-1=x+3", r"2x-x=3+1", r"x=4"]) + r"\qquad y=4+3=7\qquad " + BX(4, 7)))],
 [prob(L(r"Resol \(" + SY('x+3y=7', 'x-y=-1') + r"\).", r"Resuelve \(" + SY('x+3y=7', 'x-y=-1') + r"\).", r"Solve \(" + SY('x+3y=7', 'x-y=-1') + r"\)."),
       P(r"Aïllem la \(x\) de les dues equacions:", r"Despejamos la \(x\) de las dos ecuaciones:", r"Isolate \(x\) in both equations:"),
       D(r"x=7-3y,\qquad x=-1+y"),
       D(R([r"7-3y=-1+y", r"-4y=-8", r"y=2"]) + r"\qquad x=-1+2=1\qquad " + BX(1, 2))),
  prob(L(r"Resol \(" + SY('2x+y=1', '3x+y=3') + r"\).", r"Resuelve \(" + SY('2x+y=1', '3x+y=3') + r"\).", r"Solve \(" + SY('2x+y=1', '3x+y=3') + r"\)."),
       D(r"y=1-2x,\qquad y=3-3x"),
       D(R([r"1-2x=3-3x", r"-2x+3x=3-1", r"x=2"]) + r"\qquad y=1-2\cdot2=-3\qquad " + BX(2, -3)))],
 [prob(L(r"Resol \(" + SY('3x-2y=4', 'x+4y=6') + r"\).", r"Resuelve \(" + SY('3x-2y=4', 'x+4y=6') + r"\).", r"Solve \(" + SY('3x-2y=4', 'x+4y=6') + r"\)."),
       P(r"Aïllem la \(x\) de les dues. En la primera apareix un denominador:", r"Despejamos la \(x\) de las dos. En la primera aparece un denominador:", r"Isolate \(x\) in both. A fraction appears in the first:"),
       D(r"x=\frac{4+2y}{3},\qquad x=6-4y\qquad\Rightarrow\qquad \frac{4+2y}{3}=6-4y"),
       D(R([r"4+2y=3(6-4y)", r"4+2y=18-12y", r"14y=14", r"y=1"]) + r"\qquad x=6-4=2\qquad " + BX(2, 1)))])
cs('y=2x-1', 'y=x+3', (4, 7)); cs('x+3y=7', 'x-y=-1', (1, 2)); cs('2x+y=1', '3x+y=3', (2, -3)); cs('3x-2y=4', 'x+4y=6', (2, 1)); same('4+2y=3(6-4y)', '14y=14')
s4 += practice([
  ('★', L(r"a) \(" + SY('y=3x', 'y=x+4') + r"\) b) \(" + SY('x=2y+1', 'x=7-y') + r"\)", r"a) \(" + SY('y=3x', 'y=x+4') + r"\) b) \(" + SY('x=2y+1', 'x=7-y') + r"\)", r"a) \(" + SY('y=3x', 'y=x+4') + r"\) b) \(" + SY('x=2y+1', 'x=7-y') + r"\)")),
  ('★★', L(r"c) \(" + SY('x+y=6', 'x-y=2') + r"\) d) \(" + SY('2x+y=8', 'x+y=5') + r"\)", r"c) \(" + SY('x+y=6', 'x-y=2') + r"\) d) \(" + SY('2x+y=8', 'x+y=5') + r"\)", r"c) \(" + SY('x+y=6', 'x-y=2') + r"\) d) \(" + SY('2x+y=8', 'x+y=5') + r"\)")),
  ('★★★', L(r"e) \(" + SY('2x+3y=8', 'x-y=-1') + r"\)", r"e) \(" + SY('2x+3y=8', 'x-y=-1') + r"\)", r"e) \(" + SY('2x+3y=8', 'x-y=-1') + r"\)"))],
  D(r"\text{a)}\ 3x=x+4\Rightarrow x=2,\ y=6\qquad \text{b)}\ 2y+1=7-y\Rightarrow y=2,\ x=5")
  + D(r"\text{c)}\ 6-y=2+y\Rightarrow y=2,\ x=4\qquad \text{d)}\ 8-2x=5-x\Rightarrow x=3,\ y=2")
  + D(r"\text{e)}\ \frac{8-3y}{2}=y-1\Rightarrow 8-3y=2y-2\Rightarrow 5y=10\Rightarrow y=2,\ x=1"))
cs('y=3x', 'y=x+4', (2, 6)); cs('x=2y+1', 'x=7-y', (5, 2)); cs('x+y=6', 'x-y=2', (4, 2)); cs('2x+y=8', 'x+y=5', (3, 2)); cs('2x+3y=8', 'x-y=-1', (1, 2)); same('8-3y=2(y-1)', '-5y=-10')

# =====================================================================
# 5.5 Mètode de reducció
# =====================================================================
s5 = box('prop', L('Mètode de reducció', 'Método de reducción', 'Elimination method'),
  ol(L(r"<strong>Multipliquem</strong> una equació (o les dues) per nombres adequats perquè els coeficients d'una incògnita queden <strong>oposats</strong> (com \(6x\) i \(-6x\)).", r"<strong>Multiplicamos</strong> una ecuación (o las dos) por números adecuados para que los coeficientes de una incógnita queden <strong>opuestos</strong> (como \(6x\) y \(-6x\)).", r"<strong>Multiply</strong> one equation (or both) by suitable numbers so the coefficients of one unknown become <strong>opposites</strong> (like \(6x\) and \(-6x\))."),
     L(r"<strong>Sumem</strong> les dues equacions membre a membre: aquesta incògnita desapareix.", r"<strong>Sumamos</strong> las dos ecuaciones miembro a miembro: esa incógnita desaparece.", r"<strong>Add</strong> the two equations side by side: that unknown disappears."),
     L(r"<strong>Resolem</strong> l'equació que queda.", r"<strong>Resolvemos</strong> la ecuación que queda.", r"<strong>Solve</strong> the equation that's left."),
     L(r"<strong>Substituïm</strong> el valor en una de les equacions inicials per a trobar l'altra incògnita, i <strong>comprovem</strong>.", r"<strong>Sustituimos</strong> el valor en una de las ecuaciones iniciales para hallar la otra incógnita, y <strong>comprobamos</strong>.", r"<strong>Substitute</strong> the value into one of the original equations to find the other unknown, and <strong>check</strong>."))
  + P(r"Si els coeficients d'una incògnita ja són oposats, sumem directament:", r"Si los coeficientes de una incógnita ya son opuestos, sumamos directamente:", r"If the coefficients of one unknown are already opposite, just add:")
  + D(r"\begin{array}{rrcr}3x&+2y&=&8\\5x&-2y&=&8\\\hline 8x&&=&16\end{array}\qquad\Rightarrow\qquad x=2,\qquad 3\cdot2+2y=8\ \Rightarrow\ 2y=2\ \Rightarrow\ y=1")
  + P(r"Si no, multipliquem. En \(x+2y=4,\ 3x-y=5\), si multipliquem la segona per \(2\) els coeficients de la \(y\) queden \(2y\) i \(-2y\):", r"Si no, multiplicamos. En \(x+2y=4,\ 3x-y=5\), si multiplicamos la segunda por \(2\) los coeficientes de la \(y\) quedan \(2y\) y \(-2y\):", r"Otherwise, multiply. In \(x+2y=4,\ 3x-y=5\), multiplying the second by \(2\) makes the \(y\) coefficients \(2y\) and \(-2y\):")
  + D(r"\begin{array}{lrrcr}&x&+2y&=&4\\\scriptstyle(\cdot2)&6x&-2y&=&10\\\hline &7x&&=&14\end{array}\qquad\Rightarrow\qquad x=2,\qquad 2+2y=4\ \Rightarrow\ y=1")
  + P(r"De vegades cal multiplicar les dues. Per a eliminar la \(x\) en \(2x+3y=12,\ 3x-4y=1\): el m.c.m. de 2 i 3 és 6, i multipliquem la primera per \(3\) i la segona per \(-2\).", r"A veces hay que multiplicar las dos. Para eliminar la \(x\) en \(2x+3y=12,\ 3x-4y=1\): el m.c.m. de 2 y 3 es 6, y multiplicamos la primera por \(3\) y la segunda por \(-2\).", r"Sometimes you multiply both. To eliminate \(x\) in \(2x+3y=12,\ 3x-4y=1\): the LCM of 2 and 3 is 6, so multiply the first by \(3\) and the second by \(-2\).")
  + D(r"\begin{array}{lrrcr}\scriptstyle(\cdot3)&6x&+9y&=&36\\\scriptstyle(\cdot(-2))&-6x&+8y&=&-2\\\hline &&17y&=&34\end{array}\qquad\Rightarrow\qquad y=2,\qquad 2x+3\cdot2=12\ \Rightarrow\ x=3")
  + note(r"Quan multipliquem una equació per un nombre, el multipliquem per <strong>tots</strong> els termes, també pel del segon membre. Compte amb els signes en multiplicar per un nombre negatiu.",
         r"Cuando multiplicamos una ecuación por un número, lo multiplicamos por <strong>todos</strong> los términos, también por el del segundo miembro. Cuidado con los signos al multiplicar por un número negativo.",
         r"When you multiply an equation by a number, multiply <strong>every</strong> term, including the one on the right. Watch the signs when multiplying by a negative number.", '⚠'))
cs('3x+2y=8', '5x-2y=8', (2, 1)); cs('x+2y=4', '3x-y=5', (2, 1)); same('(x+2y)+2(3x-y)=4+10', '7x=14'); cs('2x+3y=12', '3x-4y=1', (3, 2)); same('3(2x+3y)-2(3x-4y)=36-2', '17y=34')
s5 += solver('w-red', 'red', L('Reducció pas a pas', 'Reducción paso a paso', 'Elimination step by step'), 'x+2y=4', '3x-y=5',
             [('x+y=10', 'x-y=4'), ('3x+2y=8', '5x-2y=8'), ('x+2y=4', '3x-y=5'), ('2x+5y=1', '4x+3y=-5'), ('2x+3y=12', '3x-4y=1'), ('3x+4y=2', '2x-3y=7')])
s5 += drill('red', 'Entrena: mètode de reducció', 'Entrena: método de reducción', 'Train: elimination method')
s5 += levels(
 [prob(L(r"Resol \(" + SY('x+y=10', 'x-y=4') + r"\).", r"Resuelve \(" + SY('x+y=10', 'x-y=4') + r"\).", r"Solve \(" + SY('x+y=10', 'x-y=4') + r"\)."),
       P(r"Els coeficients de la \(y\) ja són oposats. Sumem:", r"Los coeficientes de la \(y\) ya son opuestos. Sumamos:", r"The \(y\) coefficients are already opposite. Add:"),
       D(r"2x=14\ \Rightarrow\ x=7\qquad 7+y=10\ \Rightarrow\ y=3\qquad " + BX(7, 3)))],
 [prob(L(r"Resol \(" + SY('2x+5y=1', '4x+3y=-5') + r"\).", r"Resuelve \(" + SY('2x+5y=1', '4x+3y=-5') + r"\).", r"Solve \(" + SY('2x+5y=1', '4x+3y=-5') + r"\)."),
       P(r"Multipliquem la primera per \(-2\) per a eliminar la \(x\):", r"Multiplicamos la primera por \(-2\) para eliminar la \(x\):", r"Multiply the first by \(-2\) to eliminate \(x\):"),
       D(r"\begin{array}{rrcr}-4x&-10y&=&-2\\4x&+3y&=&-5\\\hline &-7y&=&-7\end{array}\qquad\Rightarrow\qquad y=1"),
       D(r"2x+5\cdot1=1\ \Rightarrow\ 2x=-4\ \Rightarrow\ x=-2\qquad " + BX(-2, 1)))],
 [prob(L(r"Resol \(" + SY('3x+4y=2', '2x-3y=7') + r"\).", r"Resuelve \(" + SY('3x+4y=2', '2x-3y=7') + r"\).", r"Solve \(" + SY('3x+4y=2', '2x-3y=7') + r"\)."),
       P(r"Eliminem la \(x\): m.c.m.(3, 2) = 6. Multipliquem la primera per \(2\) i la segona per \(-3\):", r"Eliminamos la \(x\): m.c.m.(3, 2) = 6. Multiplicamos la primera por \(2\) y la segunda por \(-3\):", r"Eliminate \(x\): LCM(3, 2) = 6. Multiply the first by \(2\) and the second by \(-3\):"),
       D(r"\begin{array}{rrcr}6x&+8y&=&4\\-6x&+9y&=&-21\\\hline &17y&=&-17\end{array}\qquad\Rightarrow\qquad y=-1"),
       D(r"3x+4\cdot(-1)=2\ \Rightarrow\ 3x=6\ \Rightarrow\ x=2\qquad " + BX(2, -1)))])
cs('x+y=10', 'x-y=4', (7, 3)); cs('2x+5y=1', '4x+3y=-5', (-2, 1)); same('-2*(2x+5y)+(4x+3y)=-2-5', '-7y=-7'); cs('3x+4y=2', '2x-3y=7', (2, -1)); same('2(3x+4y)-3(2x-3y)=4-21', '17y=-17')
s5 += box('prop', L('Quin mètode triem?', '¿Qué método elegimos?', 'Which method should we choose?'),
  P(r"Els tres mètodes donen sempre la mateixa solució: tria el que et faça treballar menys.", r"Los tres métodos dan siempre la misma solución: elige el que te haga trabajar menos.", r"All three methods always give the same solution: pick the one that means less work.")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Si el sistema…', 'Si el sistema…', 'If the system…') + '</th><th>' + L('Mètode', 'Método', 'Method') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + '<tr><td>' + L(r"té una incògnita aïllada o amb coeficient \(1\) o \(-1\)", r"tiene una incógnita despejada o con coeficiente \(1\) o \(-1\)", r"has an isolated unknown or one with coefficient \(1\) or \(-1\)") + '</td><td>' + L('Substitució', 'Sustitución', 'Substitution') + r'</td><td>\(' + SY('y=3x-2', '2x+y=8') + r'\)</td></tr>'
  + '<tr><td>' + L(r"té la mateixa incògnita aïllada en les dues equacions", r"tiene la misma incógnita despejada en las dos ecuaciones", r"has the same unknown isolated in both equations") + '</td><td>' + L('Igualació', 'Igualación', 'Equalisation') + r'</td><td>\(' + SY('y=2x+1', 'y=x+4') + r'\)</td></tr>'
  + '<tr><td>' + L(r"té coeficients iguals, oposats o múltiples, o cap coeficient 1", r"tiene coeficientes iguales, opuestos o múltiplos, o ningún coeficiente 1", r"has equal, opposite or multiple coefficients, or no coefficient 1") + '</td><td>' + L('Reducció', 'Reducción', 'Elimination') + r'</td><td>\(' + SY('3x+2y=7', '5x-2y=1') + r'\)</td></tr>'
  + '</tbody></table></div>'
  + solver('w-all', None, L('Resol qualsevol sistema', 'Resuelve cualquier sistema', 'Solve any system'), '3x+2y=7', '5x-2y=1',
           [('y=3x-2', '2x+y=8'), ('y=2x+1', 'y=x+4'), ('3x+2y=7', '5x-2y=1'), ('2x+3y=12', '3x-4y=1'), ('x+y=1', '2x-y=8'), ('2x-y=3', 'x+3y=5')]))
cs('y=3x-2', '2x+y=8', (2, 4)); cs('y=2x+1', 'y=x+4', (3, 7)); cs('3x+2y=7', '5x-2y=1', (1, 2)); cs('x+y=1', '2x-y=8', (3, -2)); cs('2x-y=3', 'x+3y=5', (2, 1))
s5 += practice([
  ('★', L(r"a) \(" + SY('2x+y=9', '3x-y=11') + r"\) b) \(" + SY('x+3y=5', '2x+y=5') + r"\)", r"a) \(" + SY('2x+y=9', '3x-y=11') + r"\) b) \(" + SY('x+3y=5', '2x+y=5') + r"\)", r"a) \(" + SY('2x+y=9', '3x-y=11') + r"\) b) \(" + SY('x+3y=5', '2x+y=5') + r"\)")),
  ('★★', L(r"c) \(" + SY('2x+3y=7', 'x-2y=0') + r"\)", r"c) \(" + SY('2x+3y=7', 'x-2y=0') + r"\)", r"c) \(" + SY('2x+3y=7', 'x-2y=0') + r"\)")),
  ('★★★', L(r"d) \(" + SY('5x+2y=1', '3x+5y=-7') + r"\)", r"d) \(" + SY('5x+2y=1', '3x+5y=-7') + r"\)", r"d) \(" + SY('5x+2y=1', '3x+5y=-7') + r"\)"))],
  D(r"\text{a)}\ 5x=20\Rightarrow x=4,\ y=1\qquad \text{b)}\ (\cdot(-2))\ -5y=-5\Rightarrow y=1,\ x=2")
  + D(r"\text{c)}\ (\cdot(-2))\ \text{%s}:\ 7y=7\Rightarrow y=1,\ x=2" % Lt('a la 2a', 'a la 2.ª', 'the 2nd'))
  + D(r"\text{d)}\ (\cdot5),\ (\cdot(-2)):\ 19x=19\Rightarrow x=1,\ y=-2"))
cs('2x+y=9', '3x-y=11', (4, 1)); cs('x+3y=5', '2x+y=5', (2, 1)); cs('2x+3y=7', 'x-2y=0', (2, 1)); same('(2x+3y)-2(x-2y)=7', '7y=7'); cs('5x+2y=1', '3x+5y=-7', (1, -2)); same('5(5x+2y)-2(3x+5y)=5+14', '19x=19')

# =====================================================================
# 5.6 Mètode gràfic
# =====================================================================
s6 = box('prop', L('Mètode gràfic', 'Método gráfico', 'Graphical method'),
  ol(L(r"Fem una <strong>taula de valors</strong> per a cada equació (dos o tres punts).", r"Hacemos una <strong>tabla de valores</strong> para cada ecuación (dos o tres puntos).", r"Make a <strong>table of values</strong> for each equation (two or three points)."),
     L(r"Representem les <strong>dues rectes</strong> en els mateixos eixos.", r"Representamos las <strong>dos rectas</strong> en los mismos ejes.", r"Draw the <strong>two lines</strong> on the same axes."),
     L(r"El <strong>punt de tall</strong> de les rectes és la solució del sistema. La comprovem en les dues equacions.", r"El <strong>punto de corte</strong> de las rectas es la solución del sistema. La comprobamos en las dos ecuaciones.", r"The <strong>crossing point</strong> of the lines is the solution. Check it in both equations."))
  + D(SY('x+y=5', '2x-y=1') + r"\qquad\Rightarrow\qquad " + SY('y=5-x', 'y=2x-1'))
  + '<div class="tv2">' + tvc('x+y=5', [0, 1, 5], 't0') + tvc('2x-y=1', [0, 1, 2], 't1') + '</div>'
  + figs(svg_graph([(1, 1, 5), (2, -1, 1)], [(0, 5, 'pt p0', None), (1, 4, 'pt p0', None), (5, 0, 'pt p0', None), (0, -1, 'pt p1', None), (1, 1, 'pt p1', None), (2, 3, 'cut', '(2, 3)')], R=6))
  + P(r"Les rectes es tallen en \((2,\,3)\). Comprovació: \(2+3=5\) ✓ i \(4-3=1\) ✓. Solució: \(x=2,\ y=3\).", r"Las rectas se cortan en \((2,\,3)\). Comprobación: \(2+3=5\) ✓ y \(4-3=1\) ✓. Solución: \(x=2,\ y=3\).", r"The lines cross at \((2,\,3)\). Check: \(2+3=5\) ✓ and \(4-3=1\) ✓. Solution: \(x=2,\ y=3\).")
  + note(r"El mètode gràfic ajuda a <strong>entendre</strong> què és la solució, però només és exacte si el punt de tall té coordenades fàcils de llegir. Si la solució és, per exemple, \(x=\frac{7}{3}\), el dibuix només en dona una aproximació: aleshores cal un mètode algebraic.",
         r"El método gráfico ayuda a <strong>entender</strong> qué es la solución, pero solo es exacto si el punto de corte tiene coordenadas fáciles de leer. Si la solución es, por ejemplo, \(x=\frac{7}{3}\), el dibujo solo da una aproximación: entonces hace falta un método algebraico.",
         r"The graphical method helps you <strong>understand</strong> what the solution is, but it's only exact when the crossing point is easy to read. If the solution is, say, \(x=\frac{7}{3}\), the drawing only gives an approximation: then you need an algebraic method.", '⚠'))
cs('x+y=5', '2x-y=1', (2, 3))
s6 += grafw('w-graf', 'x+y=5', '2x-y=1', [('x+y=5', '2x-y=1'), ('x-y=1', 'x+y=7'), ('2x+y=1', 'x-y=5'), ('y=x+2', 'y=-2x-4'), ('x+y=2', 'x+y=5'), ('x-y=1', '2x-2y=2')])
s6 += drill('gra', 'Entrena: llig la solució en la gràfica', 'Entrena: lee la solución en la gráfica', 'Train: read the solution from the graph')
s6 += box('def', L('Quantes solucions pot tindre un sistema?', '¿Cuántas soluciones puede tener un sistema?', 'How many solutions can a system have?'),
  P(r"Dues rectes només poden estar en tres posicions. Per això, un sistema de dues equacions de primer grau pot tindre <strong>una solució</strong>, <strong>cap</strong> o <strong>infinites</strong>:",
    r"Dos rectas solo pueden estar en tres posiciones. Por eso, un sistema de dos ecuaciones de primer grado puede tener <strong>una solución</strong>, <strong>ninguna</strong> o <strong>infinitas</strong>:",
    r"Two lines can only be in three positions. So a system of two first-degree equations can have <strong>one solution</strong>, <strong>none</strong> or <strong>infinitely many</strong>:")
  + figs(svg_graph([(1, 1, 3), (1, -1, -1)], [(1, 2, 'cut', None)], R=4, cap=L('Es tallen: una solució', 'Se cortan: una solución', 'They cross: one solution')),
         svg_graph([(1, 1, -1), (1, 1, 3)], [], R=4, cap=L('Paral·leles: cap solució', 'Paralelas: ninguna solución', 'Parallel: no solution')),
         svg_graph([(1, -2, -2, 0), (2, -4, -4, 1, True)], [], R=4, cap=L('La mateixa recta: infinites', 'La misma recta: infinitas', 'Same line: infinitely many')))
  + ul(L(r"\(" + SY('x+y=3', 'x-y=-1') + r"\): les rectes es tallen en \((1,\,2)\). Té <strong>una solució</strong>.", r"\(" + SY('x+y=3', 'x-y=-1') + r"\): las rectas se cortan en \((1,\,2)\). Tiene <strong>una solución</strong>.", r"\(" + SY('x+y=3', 'x-y=-1') + r"\): the lines cross at \((1,\,2)\). It has <strong>one solution</strong>."),
       L(r"\(" + SY('x+y=-1', 'x+y=3') + r"\): dos nombres no poden sumar \(-1\) i \(3\) alhora. Les rectes són paral·leles: <strong>no té solució</strong>.", r"\(" + SY('x+y=-1', 'x+y=3') + r"\): dos números no pueden sumar \(-1\) y \(3\) a la vez. Las rectas son paralelas: <strong>no tiene solución</strong>.", r"\(" + SY('x+y=-1', 'x+y=3') + r"\): two numbers can't add up to \(-1\) and \(3\) at once. The lines are parallel: <strong>no solution</strong>."),
       L(r"\(" + SY('x-2y=-2', '2x-4y=-4') + r"\): la segona equació és la primera multiplicada per 2. Són la mateixa recta: <strong>infinites solucions</strong>.", r"\(" + SY('x-2y=-2', '2x-4y=-4') + r"\): la segunda ecuación es la primera multiplicada por 2. Son la misma recta: <strong>infinitas soluciones</strong>.", r"\(" + SY('x-2y=-2', '2x-4y=-4') + r"\): the second equation is the first times 2. They are the same line: <strong>infinitely many solutions</strong>."))
  + note(r"Si resolem algebraicament un sistema sense solució, arribem a una igualtat impossible, com \(0x=4\). Si el sistema té infinites solucions, arribem a \(0x=0\), que es compleix sempre.",
         r"Si resolvemos algebraicamente un sistema sin solución, llegamos a una igualdad imposible, como \(0x=4\). Si el sistema tiene infinitas soluciones, llegamos a \(0x=0\), que se cumple siempre.",
         r"If you solve a system with no solution algebraically, you reach an impossible equality such as \(0x=4\). If it has infinitely many solutions, you reach \(0x=0\), which is always true."))
cs('x+y=3', 'x-y=-1', (1, 2)); cs('x+y=-1', 'x+y=3', 'SI'); cs('x-2y=-2', '2x-4y=-4', 'SCI'); cs('x+y=2', 'x+y=5', 'SI'); cs('x-y=1', '2x-2y=2', 'SCI')
s6 += levels(
 [prob(L(r"Resol gràficament \(" + SY('x-y=1', 'x+y=7') + r"\).", r"Resuelve gráficamente \(" + SY('x-y=1', 'x+y=7') + r"\).", r"Solve graphically \(" + SY('x-y=1', 'x+y=7') + r"\)."),
       '<div class="tv2">' + tvc('x-y=1', [0, 1, 4], 't0') + tvc('x+y=7', [0, 3, 7], 't1') + '</div>',
       figs(svg_graph([(1, -1, 1), (1, 1, 7)], [(4, 3, 'cut', '(4, 3)')], R=8)),
       P(r"Les rectes es tallen en \((4,\,3)\): \(x=4,\ y=3\). Comprovació: \(4-3=1\) ✓, \(4+3=7\) ✓.", r"Las rectas se cortan en \((4,\,3)\): \(x=4,\ y=3\). Comprobación: \(4-3=1\) ✓, \(4+3=7\) ✓.", r"The lines cross at \((4,\,3)\): \(x=4,\ y=3\). Check: \(4-3=1\) ✓, \(4+3=7\) ✓."))],
 [prob(L(r"Resol gràficament \(" + SY('2x+y=1', 'x-y=5') + r"\).", r"Resuelve gráficamente \(" + SY('2x+y=1', 'x-y=5') + r"\).", r"Solve graphically \(" + SY('2x+y=1', 'x-y=5') + r"\)."),
       '<div class="tv2">' + tvc('2x+y=1', [-1, 0, 2], 't0') + tvc('x-y=5', [0, 2, 5], 't1') + '</div>',
       figs(svg_graph([(2, 1, 1), (1, -1, 5)], [(2, -3, 'cut', '(2, −3)')], R=6)),
       P(r"Punt de tall: \((2,\,-3)\). Comprovació: \(4-3=1\) ✓, \(2+3=5\) ✓.", r"Punto de corte: \((2,\,-3)\). Comprobación: \(4-3=1\) ✓, \(2+3=5\) ✓.", r"Crossing point: \((2,\,-3)\). Check: \(4-3=1\) ✓, \(2+3=5\) ✓."))],
 [prob(L(r"Representa \(" + SY('x+2y=4', '2x+4y=2') + r"\). Quantes solucions té? Què passa si el resolem per reducció?", r"Representa \(" + SY('x+2y=4', '2x+4y=2') + r"\). ¿Cuántas soluciones tiene? ¿Qué pasa si lo resolvemos por reducción?", r"Draw \(" + SY('x+2y=4', '2x+4y=2') + r"\). How many solutions does it have? What happens if we solve it by elimination?"),
       '<div class="tv2">' + tvc('x+2y=4', [0, 2, 4], 't0') + tvc('2x+4y=2', [-1, 1, 3], 't1') + '</div>',
       figs(svg_graph([(1, 2, 4), (2, 4, 2)], [], R=5)),
       P(r"Les rectes són paral·leles: <strong>no té solució</strong>. Per reducció, multipliquem la primera per \(-2\) i sumem:", r"Las rectas son paralelas: <strong>no tiene solución</strong>. Por reducción, multiplicamos la primera por \(-2\) y sumamos:", r"The lines are parallel: <strong>no solution</strong>. By elimination, multiply the first by \(-2\) and add:"),
       D(r"\begin{array}{rrcr}-2x&-4y&=&-8\\2x&+4y&=&2\\\hline &0&=&-6\end{array}"),
       P(r"Hem arribat a una igualtat impossible, \(0=-6\): ho confirma.", r"Hemos llegado a una igualdad imposible, \(0=-6\): lo confirma.", r"We've reached an impossible equality, \(0=-6\): that confirms it."))])
cs('x-y=1', 'x+y=7', (4, 3)); cs('2x+y=1', 'x-y=5', (2, -3)); cs('x+2y=4', '2x+4y=2', 'SI'); same('-2*(x+2y)+(2x+4y)=-8+2', '0=-6')
s6 += practice([
  ('★', L(r"Resol gràficament: a) \(" + SY('x+y=4', 'x-y=2') + r"\) b) \(" + SY('y=2x', 'x+y=6') + r"\)", r"Resuelve gráficamente: a) \(" + SY('x+y=4', 'x-y=2') + r"\) b) \(" + SY('y=2x', 'x+y=6') + r"\)", r"Solve graphically: a) \(" + SY('x+y=4', 'x-y=2') + r"\) b) \(" + SY('y=2x', 'x+y=6') + r"\)")),
  ('★★', L(r"c) \(" + SY('2x-y=4', 'x+2y=-3') + r"\)", r"c) \(" + SY('2x-y=4', 'x+2y=-3') + r"\)", r"c) \(" + SY('2x-y=4', 'x+2y=-3') + r"\)")),
  ('★★★', L(r"d) Sense dibuixar-los, digues quantes solucions té cada sistema: \(" + SY('x-y=3', '2x-2y=6') + r"\) i \(" + SY('x+3y=1', 'x+3y=4') + r"\).", r"d) Sin dibujarlos, di cuántas soluciones tiene cada sistema: \(" + SY('x-y=3', '2x-2y=6') + r"\) y \(" + SY('x+3y=1', 'x+3y=4') + r"\).", r"d) Without drawing them, say how many solutions each system has: \(" + SY('x-y=3', '2x-2y=6') + r"\) and \(" + SY('x+3y=1', 'x+3y=4') + r"\)."))],
  P(r"a) \((3,\,1)\); b) \((2,\,4)\); c) \((1,\,-2)\). Pots comprovar-ho amb el giny d'aquest apartat. d) El primer té infinites solucions (la segona equació és la primera per 2); el segon, cap (\(x+3y\) no pot valdre 1 i 4 alhora).", r"a) \((3,\,1)\); b) \((2,\,4)\); c) \((1,\,-2)\). Puedes comprobarlo con la herramienta de este apartado. d) El primero tiene infinitas soluciones (la segunda ecuación es la primera por 2); el segundo, ninguna (\(x+3y\) no puede valer 1 y 4 a la vez).", r"a) \((3,\,1)\); b) \((2,\,4)\); c) \((1,\,-2)\). You can check them with this section's tool. d) The first has infinitely many solutions (the second equation is the first times 2); the second has none (\(x+3y\) can't be 1 and 4 at once)."))
cs('x+y=4', 'x-y=2', (3, 1)); cs('y=2x', 'x+y=6', (2, 4)); cs('2x-y=4', 'x+2y=-3', (1, -2)); cs('x-y=3', '2x-2y=6', 'SCI'); cs('x+3y=1', 'x+3y=4', 'SI')

# =====================================================================
# 5.7 Problemes amb sistemes d'equacions
# =====================================================================
s7 = box('prop', L('Com es resol un problema amb un sistema', 'Cómo se resuelve un problema con un sistema', 'How to solve a word problem with a system'),
  ol(L(r"<strong>Llegim</strong> l'enunciat amb calma i identifiquem les dues quantitats desconegudes.", r"<strong>Leemos</strong> el enunciado con calma e identificamos las dos cantidades desconocidas.", r"<strong>Read</strong> the problem carefully and identify the two unknown quantities."),
     L(r"<strong>Triem les incògnites</strong> i escrivim què representen: \(x=\ldots\), \(y=\ldots\)", r"<strong>Elegimos las incógnitas</strong> y escribimos qué representan: \(x=\ldots\), \(y=\ldots\)", r"<strong>Choose the unknowns</strong> and write what they stand for: \(x=\ldots\), \(y=\ldots\)"),
     L(r"<strong>Plantegem el sistema</strong>: busquem dues relacions entre les incògnites i escrivim una equació per a cadascuna.", r"<strong>Planteamos el sistema</strong>: buscamos dos relaciones entre las incógnitas y escribimos una ecuación para cada una.", r"<strong>Set up the system</strong>: find two relationships between the unknowns and write an equation for each."),
     L(r"<strong>Resolem</strong> el sistema pel mètode més còmode.", r"<strong>Resolvemos</strong> el sistema por el método más cómodo.", r"<strong>Solve</strong> the system by the easiest method."),
     L(r"<strong>Comprovem</strong> que la solució compleix l'enunciat i que té sentit (no hi pot haver \(-3\) persones ni \(2{,}5\) gallines!), i <strong>responem</strong> amb una frase.", r"<strong>Comprobamos</strong> que la solución cumple el enunciado y que tiene sentido (¡no puede haber \(-3\) personas ni \(2{,}5\) gallinas!), y <strong>respondemos</strong> con una frase.", r"<strong>Check</strong> that the solution fits the problem and makes sense (you can't have \(-3\) people or \(2.5\) hens!), and <strong>answer</strong> with a sentence."))
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Frase', 'Frase', 'Phrase') + '</th><th>' + L('Equació', 'Ecuación', 'Equation') + '</th></tr></thead><tbody>'
  + ''.join('<tr><td>' + a + r'</td><td>\(' + b + r'\)</td></tr>' for a, b in [
      (L('Dos nombres sumen 30', 'Dos números suman 30', 'Two numbers add up to 30'), 'x+y=30'),
      (L('La seua diferència és 4', 'Su diferencia es 4', 'Their difference is 4'), 'x-y=4'),
      (L('Un és el triple de l\'altre', 'Uno es el triple del otro', 'One is three times the other'), 'x=3y'),
      (L('Un en té 5 més que l\'altre', 'Uno tiene 5 más que el otro', 'One has 5 more than the other'), 'x=y+5'),
      (L('\(x\) objectes de 2 € i \(y\) de 3 € costen 19 €', '\(x\) objetos de 2 € e \(y\) de 3 € cuestan 19 €', '\(x\) items at €2 and \(y\) at €3 cost €19'), '2x+3y=19'),
      (L('D\'ací a 4 anys, l\'edat de la mare serà el doble de la del fill', 'Dentro de 4 años, la edad de la madre será el doble de la del hijo', 'In 4 years the mother will be twice as old as her son'), 'x+4=2(y+4)')])
  + '</tbody></table></div>'
  + drill('tra', "Entrena: quin és el sistema?", 'Entrena: ¿cuál es el sistema?', 'Train: which is the system?', opts=True))
s7 += levels(
 [prob(L(r"La suma de dos nombres és 45 i la seua diferència és 7. Quins són?", r"La suma de dos números es 45 y su diferencia es 7. ¿Cuáles son?", r"Two numbers add up to 45 and their difference is 7. What are they?"),
       P(r"\(x\) = el nombre major, \(y\) = el menor.", r"\(x\) = el número mayor, \(y\) = el menor.", r"\(x\) = the larger number, \(y\) = the smaller."),
       D(SY('x+y=45', 'x-y=7') + r"\ \xrightarrow{+}\ 2x=52\ \Rightarrow\ x=26,\ \ y=45-26=19"),
       P(r"Els nombres són <strong>26 i 19</strong>: \(26+19=45\) i \(26-19=7\) ✓", r"Los números son <strong>26 y 19</strong>: \(26+19=45\) y \(26-19=7\) ✓", r"The numbers are <strong>26 and 19</strong>: \(26+19=45\) and \(26-19=7\) ✓")),
  prob(L(r"En una granja hi ha gallines i conills. En total hi ha 35 caps i 94 potes. Quants animals hi ha de cada tipus?", r"En una granja hay gallinas y conejos. En total hay 35 cabezas y 94 patas. ¿Cuántos animales hay de cada tipo?", r"A farm has hens and rabbits: 35 heads and 94 legs in total. How many of each are there?"),
       P(r"\(x\) = gallines, \(y\) = conills. Cada animal té un cap; les gallines tenen 2 potes i els conills, 4.", r"\(x\) = gallinas, \(y\) = conejos. Cada animal tiene una cabeza; las gallinas tienen 2 patas y los conejos, 4.", r"\(x\) = hens, \(y\) = rabbits. Each animal has one head; hens have 2 legs and rabbits 4."),
       D(SY('x+y=35', '2x+4y=94') + r"\ \xrightarrow{(\cdot(-2))}\ \begin{array}{rrcr}-2x&-2y&=&-70\\2x&+4y&=&94\\\hline&2y&=&24\end{array}\ \Rightarrow\ y=12,\ \ x=23"),
       P(r"Hi ha <strong>23 gallines i 12 conills</strong>: \(46+48=94\) potes ✓", r"Hay <strong>23 gallinas y 12 conejos</strong>: \(46+48=94\) patas ✓", r"There are <strong>23 hens and 12 rabbits</strong>: \(46+48=94\) legs ✓"))],
 [prob(L(r"Les entrades d'un teatre costen 8 € per als adults i 5 € per als xiquets. Un dia hi van entrar 120 persones i es van recaptar 750 €. Quants adults i quants xiquets hi van anar?", r"Las entradas de un teatro cuestan 8 € para los adultos y 5 € para los niños. Un día entraron 120 personas y se recaudaron 750 €. ¿Cuántos adultos y cuántos niños fueron?", r"Theatre tickets cost €8 for adults and €5 for children. One day 120 people went in and €750 was taken. How many adults and how many children went?"),
       P(r"\(x\) = adults, \(y\) = xiquets. Per substitució:", r"\(x\) = adultos, \(y\) = niños. Por sustitución:", r"\(x\) = adults, \(y\) = children. By substitution:"),
       D(SY('x+y=120', '8x+5y=750') + r"\qquad y=120-x\ \Rightarrow\ 8x+5(120-x)=750\ \Rightarrow\ 3x=150\ \Rightarrow\ x=50,\ \ y=70"),
       P(r"Hi van anar <strong>50 adults i 70 xiquets</strong>: \(400+350=750\) € ✓", r"Fueron <strong>50 adultos y 70 niños</strong>: \(400+350=750\) € ✓", r"<strong>50 adults and 70 children</strong> went: \(400+350=750\) € ✓")),
  prob(L(r"La base d'un rectangle fa 4 cm més que l'altura i el perímetre és 36 cm. Quines dimensions té?", r"La base de un rectángulo mide 4 cm más que la altura y el perímetro es 36 cm. ¿Qué dimensiones tiene?", r"A rectangle's base is 4 cm longer than its height and its perimeter is 36 cm. What are its dimensions?"),
       P(r"\(x\) = base, \(y\) = altura. El perímetre és la suma dels quatre costats: \(2x+2y\).", r"\(x\) = base, \(y\) = altura. El perímetro es la suma de los cuatro lados: \(2x+2y\).", r"\(x\) = base, \(y\) = height. The perimeter is the sum of the four sides: \(2x+2y\)."),
       D(SY('x=y+4', '2x+2y=36') + r"\qquad 2(y+4)+2y=36\ \Rightarrow\ 4y=28\ \Rightarrow\ y=7,\ \ x=11"),
       P(r"La base fa <strong>11 cm</strong> i l'altura <strong>7 cm</strong>: \(22+14=36\) ✓", r"La base mide <strong>11 cm</strong> y la altura <strong>7 cm</strong>: \(22+14=36\) ✓", r"The base is <strong>11 cm</strong> and the height <strong>7 cm</strong>: \(22+14=36\) ✓"))],
 [prob(L(r"Un pare té el triple d'edat que el seu fill. D'ací a 10 anys només en tindrà el doble. Quants anys tenen ara?", r"Un padre tiene el triple de edad que su hijo. Dentro de 10 años solo tendrá el doble. ¿Cuántos años tienen ahora?", r"A father is three times as old as his son. In 10 years he'll only be twice as old. How old are they now?"),
       P(r"\(x\) = edat del pare, \(y\) = edat del fill (ara). D'ací a 10 anys tindran \(x+10\) i \(y+10\).", r"\(x\) = edad del padre, \(y\) = edad del hijo (ahora). Dentro de 10 años tendrán \(x+10\) e \(y+10\).", r"\(x\) = father's age, \(y\) = son's age (now). In 10 years they'll be \(x+10\) and \(y+10\)."),
       D(SY('x=3y', 'x+10=2(y+10)') + r"\qquad 3y+10=2y+20\ \Rightarrow\ y=10,\ \ x=30"),
       P(r"El pare té <strong>30 anys</strong> i el fill <strong>10</strong>. D'ací a 10 anys: 40 i 20, i 40 és el doble de 20 ✓", r"El padre tiene <strong>30 años</strong> y el hijo <strong>10</strong>. Dentro de 10 años: 40 y 20, y 40 es el doble de 20 ✓", r"The father is <strong>30</strong> and the son <strong>10</strong>. In 10 years: 40 and 20, and 40 is twice 20 ✓")),
  prob(L(r"Un test té 20 preguntes i l'Anna les ha contestades totes. Cada encert suma 3 punts i cada errada en resta 1. Si ha tret 40 punts, quantes n'ha encertat?", r"Un test tiene 20 preguntas y Ana las ha contestado todas. Cada acierto suma 3 puntos y cada fallo resta 1. Si ha sacado 40 puntos, ¿cuántas ha acertado?", r"A test has 20 questions and Anna answered them all. Each right answer scores 3 points and each wrong one loses 1. If she scored 40, how many did she get right?"),
       P(r"\(x\) = encerts, \(y\) = errades. Els coeficients de la \(y\) ja són oposats:", r"\(x\) = aciertos, \(y\) = fallos. Los coeficientes de la \(y\) ya son opuestos:", r"\(x\) = right, \(y\) = wrong. The \(y\) coefficients are already opposite:"),
       D(SY('x+y=20', '3x-y=40') + r"\ \xrightarrow{+}\ 4x=60\ \Rightarrow\ x=15,\ \ y=5"),
       P(r"N'ha encertat <strong>15</strong> (i n'ha fallat 5): \(45-5=40\) ✓", r"Ha acertado <strong>15</strong> (y ha fallado 5): \(45-5=40\) ✓", r"She got <strong>15</strong> right (and 5 wrong): \(45-5=40\) ✓"))])
cs('x+y=45', 'x-y=7', (26, 19)); cs('x+y=35', '2x+4y=94', (23, 12)); cs('x+y=120', '8x+5y=750', (50, 70)); cs('x=y+4', '2x+2y=36', (11, 7))
cs('x=3y', 'x+10=2(y+10)', (30, 10)); cs('x+y=20', '3x-y=40', (15, 5)); same('8x+5(120-x)=750', '3x=150'); same('2(y+4)+2y=36', '4y=28')
s7 += drill('prob', 'Entrena: planteja i resol', 'Entrena: plantea y resuelve', 'Train: set up and solve')
s7 += practice([
  ('★', L(r"a) Dos nombres sumen 30 i un és el quàdruple de l'altre. Quins són? b) En una guardiola hi ha 25 monedes d'1 € i de 2 €, que sumen 38 €. Quantes n'hi ha de cada?", r"a) Dos números suman 30 y uno es el cuádruple del otro. ¿Cuáles son? b) En una hucha hay 25 monedas de 1 € y de 2 €, que suman 38 €. ¿Cuántas hay de cada?", r"a) Two numbers add up to 30 and one is four times the other. What are they? b) A money box holds 25 €1 and €2 coins worth €38. How many of each?")),
  ('★★', L(r"c) Tres quaderns i dos bolígrafs costen 11 €; dos quaderns i tres bolígrafs, 9 €. Quant costa cada cosa? d) En una classe hi ha 25 alumnes. Si vinguera una xica més, hi hauria tantes xiques com xics. Quants n'hi ha de cada?", r"c) Tres cuadernos y dos bolígrafos cuestan 11 €; dos cuadernos y tres bolígrafos, 9 €. ¿Cuánto cuesta cada cosa? d) En una clase hay 25 alumnos. Si viniera una chica más, habría tantas chicas como chicos. ¿Cuántos hay de cada?", r"c) Three notebooks and two pens cost €11; two notebooks and three pens, €9. How much is each? d) A class has 25 students. If one more girl came, there would be as many girls as boys. How many of each are there?")),
  ('★★★', L(r"e) Les xifres d'un nombre de dues xifres sumen 9. Si les intercanviem, el nombre augmenta en 27. Quin és el nombre?", r"e) Las cifras de un número de dos cifras suman 9. Si las intercambiamos, el número aumenta en 27. ¿Cuál es el número?", r"e) The digits of a two-digit number add up to 9. Swapping them increases the number by 27. What is the number?"))],
  D(r"\text{a)}\ \begin{cases}x+y=30\\x=4y\end{cases}\Rightarrow y=6,\ x=24\qquad \text{b)}\ \begin{cases}x+y=25\\x+2y=38\end{cases}\Rightarrow y=13,\ x=12")
  + D(r"\text{c)}\ \begin{cases}3q+2b=11\\2q+3b=9\end{cases}\Rightarrow q=3\text{ €},\ b=1\text{ €}\qquad \text{d)}\ \begin{cases}x+y=25\\y+1=x\end{cases}\Rightarrow 2y+1=25\Rightarrow y=12\ \text{%s},\ x=13\ \text{%s}" % (Lt('xiques', 'chicas', 'girls'), Lt('xics', 'chicos', 'boys')))
  + P(r"e) \(x\) = desenes, \(y\) = unitats. El nombre és \(10x+y\) i, intercanviat, \(10y+x\):", r"e) \(x\) = decenas, \(y\) = unidades. El número es \(10x+y\) y, intercambiado, \(10y+x\):", r"e) \(x\) = tens, \(y\) = units. The number is \(10x+y\) and, swapped, \(10y+x\):")
  + D(r"\begin{cases}x+y=9\\10y+x=10x+y+27\end{cases}\Rightarrow\begin{cases}x+y=9\\-x+y=3\end{cases}\Rightarrow 2y=12\Rightarrow y=6,\ x=3:\ \ 36"))
cs('x+y=30', 'x=4y', (24, 6)); cs('x+y=25', 'x+2y=38', (12, 13)); cs('3x+2y=11', '2x+3y=9', (3, 1)); cs('x+y=9', '10y+x=10x+y+27', (3, 6)); cs('x+y=25', 'y+1=x', (13, 12)); same('10y+x=10x+y+27', '-9x+9y=27')
