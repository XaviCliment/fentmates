# Apartats 4.6-4.9 dels apunts de la Unitat 4 de 2n ESO: equacions de segon grau, discriminant i problemes.
# Fet a partir de ../3eso-t5/build.py (5.4, 5.5 i 5.7), amb el nivell de 2n. Les solucions es comproven amb sympy (ce).
from comu import *

# =====================================================================
# 4.6 Equacions de segon grau incompletes
# =====================================================================
s6 = box('def', L('Equació de segon grau', 'Ecuación de segundo grado', 'Quadratic equations'),
  P(r"Una <strong>equació de segon grau</strong> amb una incògnita és la que, un cop reduïda, té la <strong>forma general</strong>:", r"Una <strong>ecuación de segundo grado</strong> con una incógnita es la que, una vez reducida, tiene la <strong>forma general</strong>:", r"A <strong>second-degree (quadratic) equation</strong> in one unknown is one that, once simplified, has the <strong>general form</strong>:")
  + D(r"ax^2+bx+c=0\qquad(a\neq0)")
  + P(r"\(a\) és el coeficient de \(x^2\), \(b\) el de \(x\) i \(c\) el terme independent. Pot tindre <strong>dues solucions, una o cap</strong>.", r"\(a\) es el coeficiente de \(x^2\), \(b\) el de \(x\) y \(c\) el término independiente. Puede tener <strong>dos soluciones, una o ninguna</strong>.", r"\(a\) is the coefficient of \(x^2\), \(b\) the coefficient of \(x\) and \(c\) the constant term. It can have <strong>two solutions, one or none</strong>.")
  + ul(L(r"És <strong>completa</strong> si \(b\neq0\) i \(c\neq0\): \(\ 2x^2-7x+3=0\).", r"Es <strong>completa</strong> si \(b\neq0\) y \(c\neq0\): \(\ 2x^2-7x+3=0\).", r"It's <strong>complete</strong> if \(b\neq0\) and \(c\neq0\): \(\ 2x^2-7x+3=0\)."),
       L(r"És <strong>incompleta</strong> si \(b=0\) o \(c=0\): \(\ x^2-9=0\ \ (b=0),\quad 3x^2+5x=0\ \ (c=0)\).", r"Es <strong>incompleta</strong> si \(b=0\) o \(c=0\): \(\ x^2-9=0\ \ (b=0),\quad 3x^2+5x=0\ \ (c=0)\).", r"It's <strong>incomplete</strong> if \(b=0\) or \(c=0\): \(\ x^2-9=0\ \ (b=0),\quad 3x^2+5x=0\ \ (c=0)\)."))
  + note(r"Abans d'identificar \(a,\ b,\ c\), l'equació ha d'estar en forma general: tot en el primer membre, ordenat, i 0 en el segon. En \(5x-x^2=2\) passem el 2: \(-x^2+5x-2=0\), i \(a=-1,\ b=5,\ c=-2\).",
         r"Antes de identificar \(a,\ b,\ c\), la ecuación tiene que estar en forma general: todo en el primer miembro, ordenado, y 0 en el segundo. En \(5x-x^2=2\) pasamos el 2: \(-x^2+5x-2=0\), y \(a=-1,\ b=5,\ c=-2\).",
         r"Before reading off \(a,\ b,\ c\), the equation must be in general form: everything on the left, in order, and 0 on the right. In \(5x-x^2=2\) move the 2: \(-x^2+5x-2=0\), so \(a=-1,\ b=5,\ c=-2\)."))
s6 += box('prop', L('Incompletes sense terme en x: ax² + c = 0', 'Incompletas sin término en x: ax² + c = 0', 'No x term: ax² + c = 0'),
  P(r"Aïllem \(x^2\) i fem l'<strong>arrel quadrada</strong>, sense oblidar les <strong>dues</strong> arrels, la positiva i la negativa:", r"Despejamos \(x^2\) y hacemos la <strong>raíz cuadrada</strong>, sin olvidar las <strong>dos</strong> raíces, la positiva y la negativa:", r"Isolate \(x^2\) and take the <strong>square root</strong>, remembering <strong>both</strong> roots, positive and negative:")
  + D(r"2x^2-18=0\ \Rightarrow\ 2x^2=18\ \Rightarrow\ x^2=\frac{18}{2}=9\ \Rightarrow\ x=\pm\sqrt9=\pm3")
  + P(r"És a dir, \(x=3\) i \(x=-3\): totes dues compleixen l'equació, perquè \(3^2=(-3)^2=9\).", r"Es decir, \(x=3\) y \(x=-3\): las dos cumplen la ecuación, porque \(3^2=(-3)^2=9\).", r"That is, \(x=3\) and \(x=-3\): both satisfy the equation, because \(3^2=(-3)^2=9\).")
  + note(r"Si en aïllar queda \(x^2\) igual a un nombre <strong>negatiu</strong>, l'equació <strong>no té solució</strong>, perquè cap nombre al quadrat és negatiu: \(x^2+4=0\Rightarrow x^2=-4\), sense solució.", r"Si al despejar queda \(x^2\) igual a un número <strong>negativo</strong>, la ecuación <strong>no tiene solución</strong>, porque ningún número al cuadrado es negativo: \(x^2+4=0\Rightarrow x^2=-4\), sin solución.", r"If isolating gives \(x^2\) equal to a <strong>negative</strong> number, the equation has <strong>no solution</strong>, because no square is negative: \(x^2+4=0\Rightarrow x^2=-4\), no solution.", '⚠')
  + P(r"Si el nombre no és un quadrat perfecte, deixem la solució amb l'arrel: \(x^2=7\Rightarrow x=\pm\sqrt7\approx\pm2\dc65\).", r"Si el número no es un cuadrado perfecto, dejamos la solución con la raíz: \(x^2=7\Rightarrow x=\pm\sqrt7\approx\pm2\dc65\).", r"If the number isn't a perfect square, leave the answer with the root: \(x^2=7\Rightarrow x=\pm\sqrt7\approx\pm2\dc65\)."))
s6 += box('prop', L('Incompletes sense terme independent: ax² + bx = 0', 'Incompletas sin término independiente: ax² + bx = 0', 'No constant term: ax² + bx = 0'),
  P(r"Traiem <strong>factor comú</strong> \(x\) i fem servir que, si un producte val zero, algun dels factors ha de valdre zero:", r"Sacamos <strong>factor común</strong> \(x\) y usamos que, si un producto vale cero, alguno de los factores tiene que valer cero:", r"Take out the <strong>common factor</strong> \(x\) and use the fact that if a product is zero, one of the factors must be zero:")
  + D(r"ax^2+bx=0\ \Rightarrow\ x\,(ax+b)=0\ \Rightarrow\ \begin{cases}x=0\\ ax+b=0\ \Rightarrow\ x=-\dfrac{b}{a}\end{cases}")
  + D(r"3x^2-12x=0\ \Rightarrow\ 3x\,(x-4)=0\ \Rightarrow\ x=0,\quad x=4")
  + note(r"<strong>No dividisques</strong> els dos membres entre \(x\): perdries la solució \(x=0\). Aquestes equacions <strong>sempre</strong> tenen la solució \(x=0\).",
         r"<strong>No dividas</strong> los dos miembros entre \(x\): perderías la solución \(x=0\). Estas ecuaciones <strong>siempre</strong> tienen la solución \(x=0\).",
         r"<strong>Don't divide</strong> both sides by \(x\): you'd lose the solution \(x=0\). These equations <strong>always</strong> have the solution \(x=0\).", '⚠')
  + P(r"Si \(b=c=0\), l'equació és \(ax^2=0\) i l'única solució és \(x=0\).", r"Si \(b=c=0\), la ecuación es \(ax^2=0\) y la única solución es \(x=0\).", r"If \(b=c=0\), the equation is \(ax^2=0\) and the only solution is \(x=0\).")
  + drill('inc', 'Entrena: equacions incompletes', 'Entrena: ecuaciones incompletas', 'Train: incomplete quadratics', SETHINT))
ce('2x^2-18=0', [3, -3]); ce('x^2+4=0', []); ce('x^2=7', ['sqrt(7)', '-sqrt(7)']); ce('3x^2-12x=0', [0, 4]); ce('5x-x^2=2', ['(5+sqrt(17))/2', '(5-sqrt(17))/2'])
s6 += levels(
 [prob(L(r"Resol: a) \(5x^2-45=0\); b) \(x^2+7x=0\); c) \(x^2+16=0\).", r"Resuelve: a) \(5x^2-45=0\); b) \(x^2+7x=0\); c) \(x^2+16=0\).", r"Solve: a) \(5x^2-45=0\); b) \(x^2+7x=0\); c) \(x^2+16=0\)."),
       D(r"\text{a)}\ x^2=\frac{45}{5}=9\ \Rightarrow\ \boxed{x=\pm3}"),
       D(r"\text{b)}\ x(x+7)=0\ \Rightarrow\ \boxed{x=0},\quad x+7=0\Rightarrow\boxed{x=-7}"),
       D(r"\text{c)}\ x^2=-16\ \Rightarrow\ \boxed{\text{%s}}" % Lt('cap solució', 'ninguna solución', 'no solution')))],
 [prob(L(r"Resol \((x+2)^2=4x+29\).", r"Resuelve \((x+2)^2=4x+29\).", r"Solve \((x+2)^2=4x+29\)."),
       P(r"Primer desenvolupem la identitat notable i la reduïm a la forma general:", r"Primero desarrollamos la identidad notable y la reducimos a la forma general:", r"First expand the special product and put it in general form:"),
       D(r"x^2+4x+4=4x+29\ \Rightarrow\ x^2-25=0\ \Rightarrow\ x^2=25\ \Rightarrow\ \boxed{x=\pm5}")),
  prob(L(r"Resol \(x(2x-5)=3x\).", r"Resuelve \(x(2x-5)=3x\).", r"Solve \(x(2x-5)=3x\)."),
       D(r"2x^2-5x=3x\ \Rightarrow\ 2x^2-8x=0\ \Rightarrow\ 2x(x-4)=0\ \Rightarrow\ \boxed{x=0},\ \boxed{x=4}"))],
 [prob(L(r"Resol \(9x^2-4=0\).", r"Resuelve \(9x^2-4=0\).", r"Solve \(9x^2-4=0\)."),
       D(r"x^2=\frac{4}{9}\ \Rightarrow\ x=\pm\sqrt{\frac49}=\boxed{\pm\frac23}")),
  prob(L(r"Resol \(\dfrac{x^2}{3}-\dfrac{x}{2}=\dfrac{x^2+x}{6}\).", r"Resuelve \(\dfrac{x^2}{3}-\dfrac{x}{2}=\dfrac{x^2+x}{6}\).", r"Solve \(\dfrac{x^2}{3}-\dfrac{x}{2}=\dfrac{x^2+x}{6}\)."),
       D(r"\text{m.c.m.}=6:\quad 2x^2-3x=x^2+x\ \Rightarrow\ x^2-4x=0"),
       D(r"x(x-4)=0\ \Rightarrow\ \boxed{x=0},\ \boxed{x=4}"))])
ce('5x^2-45=0', [3, -3]); ce('x^2+7x=0', [0, -7]); ce('x^2+16=0', []); ce('(x+2)^2=4x+29', [5, -5]); ce('x(2x-5)=3x', [0, 4]); ce('9x^2-4=0', ['2/3', '-2/3']); ce('x^2/3-x/2=(x^2+x)/6', [0, 4])
s6 += practice([
  ('★', L(r"Resol: a) \(x^2-49=0\); b) \(4x^2-20x=0\); c) \(3x^2=48\); d) \(x^2+x=0\).", r"Resuelve: a) \(x^2-49=0\); b) \(4x^2-20x=0\); c) \(3x^2=48\); d) \(x^2+x=0\).", r"Solve: a) \(x^2-49=0\); b) \(4x^2-20x=0\); c) \(3x^2=48\); d) \(x^2+x=0\).")),
  ('★★', L(r"e) \(2x^2+50=0\); f) \((x-3)(x+3)=7\); g) \(5x^2=3x\).", r"e) \(2x^2+50=0\); f) \((x-3)(x+3)=7\); g) \(5x^2=3x\).", r"e) \(2x^2+50=0\); f) \((x-3)(x+3)=7\); g) \(5x^2=3x\).")),
  ('★★★', L(r"h) \((2x-1)^2=1-6x\); i) \(\dfrac{x^2-1}{3}-\dfrac{x^2+1}{4}=1\).", r"h) \((2x-1)^2=1-6x\); i) \(\dfrac{x^2-1}{3}-\dfrac{x^2+1}{4}=1\).", r"h) \((2x-1)^2=1-6x\); i) \(\dfrac{x^2-1}{3}-\dfrac{x^2+1}{4}=1\)."))],
  D(r"\text{a)}\ x=\pm7\qquad \text{b)}\ 4x(x-5)=0\Rightarrow x=0,\ x=5\qquad \text{c)}\ x^2=16\Rightarrow x=\pm4\qquad \text{d)}\ x(x+1)=0\Rightarrow x=0,\ x=-1")
  + D(r"\text{e)}\ x^2=-25:\ \text{%s}\qquad \text{f)}\ x^2-9=7\Rightarrow x^2=16\Rightarrow x=\pm4\qquad \text{g)}\ x(5x-3)=0\Rightarrow x=0,\ x=\frac35" % Lt('cap solució', 'ninguna solución', 'no solution'))
  + D(r"\text{h)}\ 4x^2-4x+1=1-6x\Rightarrow 4x^2+2x=0\Rightarrow 2x(2x+1)=0\Rightarrow x=0,\ x=-\frac12")
  + D(r"\text{i)}\ 4(x^2-1)-3(x^2+1)=12\Rightarrow x^2=19\Rightarrow x=\pm\sqrt{19}"))
ce('x^2-49=0', [7, -7]); ce('4x^2-20x=0', [0, 5]); ce('3x^2=48', [4, -4]); ce('x^2+x=0', [0, -1]); ce('2x^2+50=0', []); ce('(x-3)(x+3)=7', [4, -4]); ce('5x^2=3x', [0, '3/5'])
ce('(2x-1)^2=1-6x', [0, '-1/2']); ce('(x^2-1)/3-(x^2+1)/4=1', ['sqrt(19)', '-sqrt(19)'])

# =====================================================================
# 4.7 Equacions de segon grau completes
# =====================================================================
s7 = box('def', L('La fórmula de les equacions de segon grau', 'La fórmula de las ecuaciones de segundo grado', 'The quadratic formula'),
  P(r"Les solucions de \(ax^2+bx+c=0\) s'obtenen amb la fórmula:", r"Las soluciones de \(ax^2+bx+c=0\) se obtienen con la fórmula:", r"The solutions of \(ax^2+bx+c=0\) are given by the formula:")
  + D(r"\boxed{x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}}")
  + P(r"El signe \(\pm\) ens dona les dues solucions: una amb \(+\) i l'altra amb \(-\). Exemple: \(x^2-5x+6=0\), amb \(a=1,\ b=-5,\ c=6\):", r"El signo \(\pm\) nos da las dos soluciones: una con \(+\) y la otra con \(-\). Ejemplo: \(x^2-5x+6=0\), con \(a=1,\ b=-5,\ c=6\):", r"The \(\pm\) sign gives both solutions: one with \(+\) and the other with \(-\). Example: \(x^2-5x+6=0\), with \(a=1,\ b=-5,\ c=6\):")
  + D(r"x=\frac{-(-5)\pm\sqrt{(-5)^2-4\cdot1\cdot6}}{2\cdot1}=\frac{5\pm\sqrt{25-24}}{2}=\frac{5\pm1}{2}\ \Rightarrow\ x_1=\frac{6}{2}=3,\quad x_2=\frac{4}{2}=2")
  + P(r"Comprovació: \(3^2-5\cdot3+6=0\) ✓ i \(2^2-5\cdot2+6=0\) ✓", r"Comprobación: \(3^2-5\cdot3+6=0\) ✓ y \(2^2-5\cdot2+6=0\) ✓", r"Check: \(3^2-5\cdot3+6=0\) ✓ and \(2^2-5\cdot2+6=0\) ✓")
  + note(r"Errors típics: \(-b\) és l'<strong>oposat</strong> de \(b\) (si \(b=-5\), \(-b=5\)); \(b^2\) sempre és positiu, \((-5)^2=25\); si \(a\) o \(c\) són negatius, \(-4ac\) pot ser positiu; i la ratlla de fracció va davall de <strong>tot</strong> el numerador.",
         r"Errores típicos: \(-b\) es el <strong>opuesto</strong> de \(b\) (si \(b=-5\), \(-b=5\)); \(b^2\) siempre es positivo, \((-5)^2=25\); si \(a\) o \(c\) son negativos, \(-4ac\) puede ser positivo; y la raya de fracción va debajo de <strong>todo</strong> el numerador.",
         r"Common mistakes: \(-b\) is the <strong>opposite</strong> of \(b\) (if \(b=-5\), \(-b=5\)); \(b^2\) is always positive, \((-5)^2=25\); if \(a\) or \(c\) is negative, \(-4ac\) can be positive; and the fraction bar goes under the <strong>whole</strong> numerator.", '⚠')
  + note(r"La fórmula també serveix per a les incompletes, però per a aquestes els mètodes de l'apartat anterior són més ràpids.", r"La fórmula también sirve para las incompletas, pero para estas los métodos del apartado anterior son más rápidos.", r"The formula also works for incomplete equations, but the methods in the previous section are quicker."))
ce('x^2-5x+6=0', [2, 3])
s7 += box('prop', L('Equacions de segon grau que cal reduir abans', 'Ecuaciones de segundo grado que hay que reducir antes', 'Quadratics that need simplifying first'),
  P(r"Si hi ha parèntesis o denominadors, primer els eliminem (com a les de primer grau) i passem tots els termes al primer membre. Dos consells per a treballar amb nombres més còmodes:",
    r"Si hay paréntesis o denominadores, primero los eliminamos (como en las de primer grado) y pasamos todos los términos al primer miembro. Dos consejos para trabajar con números más cómodos:",
    r"If there are brackets or denominators, clear them first (as with linear equations) and move all the terms to the left. Two tips for working with friendlier numbers:")
  + ul(L(r"Si el coeficient \(a\) és negatiu, multipliquem tota l'equació per \(-1\): \(-x^2+2x+8=0\Rightarrow x^2-2x-8=0\).", r"Si el coeficiente \(a\) es negativo, multiplicamos toda la ecuación por \(-1\): \(-x^2+2x+8=0\Rightarrow x^2-2x-8=0\).", r"If \(a\) is negative, multiply the whole equation by \(-1\): \(-x^2+2x+8=0\Rightarrow x^2-2x-8=0\)."),
       L(r"Si tots els coeficients tenen un divisor comú, dividim: \(2x^2-2x-12=0\Rightarrow x^2-x-6=0\).", r"Si todos los coeficientes tienen un divisor común, dividimos: \(2x^2-2x-12=0\Rightarrow x^2-x-6=0\).", r"If all the coefficients share a factor, divide: \(2x^2-2x-12=0\Rightarrow x^2-x-6=0\)."))
  + D(r"(x+1)(x-2)=2x+2\ \Rightarrow\ x^2-2x+x-2=2x+2\ \Rightarrow\ x^2-3x-4=0")
  + D(r"x=\frac{3\pm\sqrt{9+16}}{2}=\frac{3\pm5}{2}\ \Rightarrow\ x_1=4,\quad x_2=-1")
  + widget('w-q2', '🧮', L('Resolució pas a pas de qualsevol equació de 2n grau', 'Resolución paso a paso de cualquier ecuación de 2.º grado', 'Step-by-step solver for any quadratic'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), 'x^2-5x+6=0') + '</div>', HELP,
            quick([('x^2-5x+6=0', 'x²−5x+6 = 0'), ('2x^2-7x+3=0', '2x²−7x+3 = 0'), ('-x^2+2x+8=0', '−x²+2x+8 = 0'), ('(x+1)(x-2)=2x+2', '(x+1)(x−2) = 2x+2'), ('x^2-6x+9=0', 'x²−6x+9 = 0'), ('x^2+x+1=0', 'x²+x+1 = 0'), ('x(x-1)/2-(x+1)/3=1', 'x(x−1)/2 − (x+1)/3 = 1'), ('3x^2-12x=0', '3x²−12x = 0')])])
  + drill('q2', 'Entrena: equacions completes', 'Entrena: ecuaciones completas', 'Train: complete quadratics', SETHINT))
ce('-x^2+2x+8=0', [4, -2]); ce('2x^2-2x-12=0', [3, -2]); ce('(x+1)(x-2)=2x+2', [4, -1]); ce('x(x-1)/2-(x+1)/3=1', ['8/3', -1])
s7 += levels(
 [prob(L(r"Resol \(x^2+2x-15=0\).", r"Resuelve \(x^2+2x-15=0\).", r"Solve \(x^2+2x-15=0\)."),
       P(r"\(a=1,\ b=2,\ c=-15\):", r"\(a=1,\ b=2,\ c=-15\):", r"\(a=1,\ b=2,\ c=-15\):"),
       D(r"x=\frac{-2\pm\sqrt{2^2-4\cdot1\cdot(-15)}}{2}=\frac{-2\pm\sqrt{64}}{2}=\frac{-2\pm8}{2}\ \Rightarrow\ \boxed{x_1=3},\quad \boxed{x_2=-5}")),
  prob(L(r"Resol \(2x^2-7x+3=0\).", r"Resuelve \(2x^2-7x+3=0\).", r"Solve \(2x^2-7x+3=0\)."),
       D(r"x=\frac{7\pm\sqrt{49-24}}{4}=\frac{7\pm5}{4}\ \Rightarrow\ \boxed{x_1=3},\quad \boxed{x_2=\frac{2}{4}=\frac12}"))],
 [prob(L(r"Resol \(-x^2+2x+8=0\).", r"Resuelve \(-x^2+2x+8=0\).", r"Solve \(-x^2+2x+8=0\)."),
       P(r"Multipliquem per \(-1\) per a tindre \(a\) positiu:", r"Multiplicamos por \(-1\) para tener \(a\) positivo:", r"Multiply by \(-1\) to make \(a\) positive:"),
       D(r"x^2-2x-8=0\ \Rightarrow\ x=\frac{2\pm\sqrt{4+32}}{2}=\frac{2\pm6}{2}\ \Rightarrow\ \boxed{x_1=4},\quad \boxed{x_2=-2}")),
  prob(L(r"Resol \(x(x+3)=2(x+3)\).", r"Resuelve \(x(x+3)=2(x+3)\).", r"Solve \(x(x+3)=2(x+3)\)."),
       D(r"x^2+3x=2x+6\ \Rightarrow\ x^2+x-6=0"),
       D(r"x=\frac{-1\pm\sqrt{1+24}}{2}=\frac{-1\pm5}{2}\ \Rightarrow\ \boxed{x_1=2},\quad \boxed{x_2=-3}"))],
 [prob(L(r"Resol \((x-2)^2+(x+1)^2=17\).", r"Resuelve \((x-2)^2+(x+1)^2=17\).", r"Solve \((x-2)^2+(x+1)^2=17\)."),
       D(r"x^2-4x+4+x^2+2x+1=17\ \Rightarrow\ 2x^2-2x-12=0\ \Rightarrow\ x^2-x-6=0"),
       D(r"x=\frac{1\pm\sqrt{1+24}}{2}=\frac{1\pm5}{2}\ \Rightarrow\ \boxed{x_1=3},\quad \boxed{x_2=-2}")),
  prob(L(r"Resol \(\dfrac{x(x-1)}{2}-\dfrac{x+1}{3}=1\).", r"Resuelve \(\dfrac{x(x-1)}{2}-\dfrac{x+1}{3}=1\).", r"Solve \(\dfrac{x(x-1)}{2}-\dfrac{x+1}{3}=1\)."),
       D(r"\xrightarrow{\cdot6}\ 3x(x-1)-2(x+1)=6\ \Rightarrow\ 3x^2-3x-2x-2=6\ \Rightarrow\ 3x^2-5x-8=0"),
       D(r"x=\frac{5\pm\sqrt{25+96}}{6}=\frac{5\pm11}{6}\ \Rightarrow\ \boxed{x_1=\frac{16}{6}=\frac83},\quad \boxed{x_2=-1}"))])
ce('x^2+2x-15=0', [3, -5]); ce('2x^2-7x+3=0', [3, '1/2']); ce('x(x+3)=2(x+3)', [2, -3]); ce('(x-2)^2+(x+1)^2=17', [3, -2])
s7 += practice([
  ('★', L(r"Resol: a) \(x^2-7x+10=0\); b) \(x^2+4x-21=0\); c) \(x^2+6x+8=0\); d) \(3x^2+5x-2=0\).", r"Resuelve: a) \(x^2-7x+10=0\); b) \(x^2+4x-21=0\); c) \(x^2+6x+8=0\); d) \(3x^2+5x-2=0\).", r"Solve: a) \(x^2-7x+10=0\); b) \(x^2+4x-21=0\); c) \(x^2+6x+8=0\); d) \(3x^2+5x-2=0\).")),
  ('★★', L(r"e) \(-x^2+x+12=0\); f) \(2x^2+4x-30=0\); g) \((x+3)(x-1)=5\).", r"e) \(-x^2+x+12=0\); f) \(2x^2+4x-30=0\); g) \((x+3)(x-1)=5\).", r"e) \(-x^2+x+12=0\); f) \(2x^2+4x-30=0\); g) \((x+3)(x-1)=5\).")),
  ('★★★', L(r"h) \((x+2)^2-3(x+4)=x\); i) \(\dfrac{x^2}{2}-\dfrac{x}{3}=\dfrac{4}{3}\).", r"h) \((x+2)^2-3(x+4)=x\); i) \(\dfrac{x^2}{2}-\dfrac{x}{3}=\dfrac{4}{3}\).", r"h) \((x+2)^2-3(x+4)=x\); i) \(\dfrac{x^2}{2}-\dfrac{x}{3}=\dfrac{4}{3}\)."))],
  D(r"\text{a)}\ x=\frac{7\pm3}{2}:\ 5,\ 2\qquad \text{b)}\ x=\frac{-4\pm10}{2}:\ 3,\ -7\qquad \text{c)}\ x=\frac{-6\pm2}{2}:\ -2,\ -4\qquad \text{d)}\ x=\frac{-5\pm7}{6}:\ \frac13,\ -2")
  + D(r"\text{e)}\ x^2-x-12=0:\ 4,\ -3\qquad \text{f)}\ x^2+2x-15=0:\ 3,\ -5\qquad \text{g)}\ x^2+2x-8=0:\ 2,\ -4")
  + D(r"\text{h)}\ x^2+4x+4-3x-12=x\Rightarrow x^2-8=0\Rightarrow x=\pm\sqrt8=\pm2\sqrt2\qquad \text{i)}\ 3x^2-2x-8=0:\ x=\frac{2\pm10}{6}:\ 2,\ -\frac43"))
ce('x^2-7x+10=0', [5, 2]); ce('x^2+4x-21=0', [3, -7]); ce('x^2+6x+8=0', [-2, -4]); ce('3x^2+5x-2=0', ['1/3', -2]); ce('-x^2+x+12=0', [4, -3]); ce('2x^2+4x-30=0', [3, -5])
ce('(x+3)(x-1)=5', [2, -4]); ce('(x+2)^2-3(x+4)=x', ['2*sqrt(2)', '-2*sqrt(2)']); ce('x^2/2-x/3=4/3', [2, '-4/3'])

# =====================================================================
# 4.8 El discriminant
# =====================================================================
s8 = box('def', L('El discriminant: quantes solucions hi ha?', 'El discriminante: ¿cuántas soluciones hay?', 'The discriminant: how many solutions?'),
  P(r"El nombre de dins de l'arrel de la fórmula, \(\Delta=b^2-4ac\), s'anomena <strong>discriminant</strong> (\(\Delta\) és la lletra grega <em>delta</em>). Ens diu quantes solucions té l'equació <strong>sense haver-la de resoldre</strong>:",
    r"El número de dentro de la raíz de la fórmula, \(\Delta=b^2-4ac\), se llama <strong>discriminante</strong> (\(\Delta\) es la letra griega <em>delta</em>). Nos dice cuántas soluciones tiene la ecuación <strong>sin tener que resolverla</strong>:",
    r"The number under the square root in the formula, \(\Delta=b^2-4ac\), is called the <strong>discriminant</strong> (\(\Delta\) is the Greek letter <em>delta</em>). It tells us how many solutions there are <strong>without solving</strong>:")
  + '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>\\(\\Delta=b^2-4ac\\)</th><th>' + L('Solucions', 'Soluciones', 'Solutions') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + '<tr><td>\\(\\Delta>0\\)</td><td class="l">' + L('Dues solucions diferents', 'Dos soluciones distintas', 'Two different solutions') + '</td><td>\\(x^2-5x+6=0:\\ \\Delta=25-24=1\\)</td></tr>'
  + '<tr><td>\\(\\Delta=0\\)</td><td class="l">' + L('Una solució (doble)', 'Una solución (doble)', 'One (repeated) solution') + '</td><td>\\(x^2-6x+9=0:\\ \\Delta=36-36=0\\)</td></tr>'
  + '<tr><td>\\(\\Delta<0\\)</td><td class="l">' + L('Cap solució', 'Ninguna solución', 'No solution') + '</td><td>\\(x^2+x+1=0:\\ \\Delta=1-4=-3\\)</td></tr></tbody></table></div>'
  + ul(L(r"Si \(\Delta>0\), la fórmula dona dos valors diferents, un amb \(+\sqrt\Delta\) i l'altre amb \(-\sqrt\Delta\).", r"Si \(\Delta>0\), la fórmula da dos valores distintos, uno con \(+\sqrt\Delta\) y el otro con \(-\sqrt\Delta\).", r"If \(\Delta>0\), the formula gives two different values, one with \(+\sqrt\Delta\) and one with \(-\sqrt\Delta\)."),
       L(r"Si \(\Delta=0\), sumar o restar 0 dona el mateix: una sola solució, \(x=\frac{-b}{2a}\). En l'exemple, \(x=\frac{6}{2}=3\), perquè \(x^2-6x+9=(x-3)^2\).", r"Si \(\Delta=0\), sumar o restar 0 da lo mismo: una sola solución, \(x=\frac{-b}{2a}\). En el ejemplo, \(x=\frac{6}{2}=3\), porque \(x^2-6x+9=(x-3)^2\).", r"If \(\Delta=0\), adding or subtracting 0 gives the same thing: one solution, \(x=\frac{-b}{2a}\). In the example, \(x=\frac{6}{2}=3\), since \(x^2-6x+9=(x-3)^2\)."),
       L(r"Si \(\Delta<0\), l'arrel quadrada d'un nombre negatiu no existeix: no hi ha solució.", r"Si \(\Delta<0\), la raíz cuadrada de un número negativo no existe: no hay solución.", r"If \(\Delta<0\), a negative number has no square root: there's no solution."))
  + note(r"Quan \(\Delta\) és positiu però no és un quadrat perfecte, les solucions no són exactes: les deixem amb l'arrel. \(x^2-3x-1=0\): \(\Delta=9+4=13\), \(x=\frac{3\pm\sqrt{13}}{2}\), és a dir, \(x_1\approx3\dc30\) i \(x_2\approx-0\dc30\).",
         r"Cuando \(\Delta\) es positivo pero no es un cuadrado perfecto, las soluciones no son exactas: las dejamos con la raíz. \(x^2-3x-1=0\): \(\Delta=9+4=13\), \(x=\frac{3\pm\sqrt{13}}{2}\), es decir, \(x_1\approx3\dc30\) y \(x_2\approx-0\dc30\).",
         r"When \(\Delta\) is positive but not a perfect square, the solutions aren't exact: leave them with the root. \(x^2-3x-1=0\): \(\Delta=9+4=13\), \(x=\frac{3\pm\sqrt{13}}{2}\), i.e. \(x_1\approx3\dc30\) and \(x_2\approx-0\dc30\)."))
ce('x^2-6x+9=0', [3]); ce('x^2+x+1=0', []); ce('x^2-3x-1=0', ['(3+sqrt(13))/2', '(3-sqrt(13))/2'])
s8 += box('prop', L('El discriminant i la gràfica', 'El discriminante y la gráfica', 'The discriminant and the graph'),
  P(r"Si dibuixem la paràbola \(y=ax^2+bx+c\), les solucions de \(ax^2+bx+c=0\) són els punts on <strong>talla l'eix \(X\)</strong> (on \(y=0\)). Mou els coeficients i observa com canvia el discriminant:",
    r"Si dibujamos la parábola \(y=ax^2+bx+c\), las soluciones de \(ax^2+bx+c=0\) son los puntos donde <strong>corta al eje \(X\)</strong> (donde \(y=0\)). Mueve los coeficientes y observa cómo cambia el discriminante:",
    r"If we draw the parabola \(y=ax^2+bx+c\), the solutions of \(ax^2+bx+c=0\) are the points where it <strong>crosses the \(x\)-axis</strong> (where \(y=0\)). Move the coefficients and watch the discriminant change:")
  + widget('w-disc', '📈', L('El discriminant i la paràbola', 'El discriminante y la parábola', 'The discriminant and the parabola'),
           ['<div class="wrow">' + rng('a', 'a', -3, 3, 1) + rng('b', 'b', -8, 8, -2) + rng('c', 'c', -9, 9, -3) + '</div>'],
           out='<div class="disc-out"><div class="disc-eq"></div><svg class="parab" viewBox="0 0 340 260" role="img" aria-label="paràbola"></svg></div>')
  + P(r"Prova, per exemple, \(b=-2\) i ves pujant \(c\): per a \(c<1\) hi ha dues solucions, per a \(c=1\) la paràbola només toca l'eix (\(\Delta=0\)) i per a \(c>1\) ja no el talla.",
      r"Prueba, por ejemplo, \(b=-2\) y ve subiendo \(c\): para \(c<1\) hay dos soluciones, para \(c=1\) la parábola solo toca el eje (\(\Delta=0\)) y para \(c>1\) ya no lo corta.",
      r"Try, for example, \(b=-2\) and slowly raise \(c\): for \(c<1\) there are two solutions, at \(c=1\) the parabola just touches the axis (\(\Delta=0\)) and for \(c>1\) it no longer crosses it.")
  + drill('disc', 'Entrena: quantes solucions té?', 'Entrena: ¿cuántas soluciones tiene?', 'Train: how many solutions?'))
ce('x^2-2x+1=0', [1])
s8 += levels(
 [prob(L(r"Sense resoldre-les, digues quantes solucions té cada equació: a) \(x^2-4x+4=0\); b) \(3x^2+2x+1=0\); c) \(2x^2-x-3=0\).",
         r"Sin resolverlas, di cuántas soluciones tiene cada ecuación: a) \(x^2-4x+4=0\); b) \(3x^2+2x+1=0\); c) \(2x^2-x-3=0\).",
         r"Without solving, say how many solutions each equation has: a) \(x^2-4x+4=0\); b) \(3x^2+2x+1=0\); c) \(2x^2-x-3=0\)."),
       D(r"\text{a)}\ \Delta=(-4)^2-4\cdot1\cdot4=16-16=0\ \to\ \boxed{\text{%s}}" % Lt('una solució', 'una solución', 'one solution')),
       D(r"\text{b)}\ \Delta=2^2-4\cdot3\cdot1=4-12=-8<0\ \to\ \boxed{\text{%s}}" % Lt('cap solució', 'ninguna solución', 'no solution')),
       D(r"\text{c)}\ \Delta=(-1)^2-4\cdot2\cdot(-3)=1+24=25>0\ \to\ \boxed{\text{%s}}" % Lt('dues solucions', 'dos soluciones', 'two solutions')))],
 [prob(L(r"Resol \(4x^2-4x+1=0\). Què té de particular?", r"Resuelve \(4x^2-4x+1=0\). ¿Qué tiene de particular?", r"Solve \(4x^2-4x+1=0\). What's special about it?"),
       D(r"\Delta=16-16=0\ \Rightarrow\ x=\frac{4\pm0}{8}=\boxed{\frac12}"),
       P(r"Té una única solució (doble), perquè \(4x^2-4x+1=(2x-1)^2\): és una identitat notable.", r"Tiene una única solución (doble), porque \(4x^2-4x+1=(2x-1)^2\): es una identidad notable.", r"It has a single (double) solution, because \(4x^2-4x+1=(2x-1)^2\): it's a special product.")),
  prob(L(r"Resol \(x^2-2x-2=0\) i dona'n les solucions aproximades.", r"Resuelve \(x^2-2x-2=0\) y da sus soluciones aproximadas.", r"Solve \(x^2-2x-2=0\) and give approximate solutions."),
       D(r"\Delta=4+8=12\ \Rightarrow\ x=\frac{2\pm\sqrt{12}}{2}\ \Rightarrow\ \boxed{x_1\approx2\dc73},\quad \boxed{x_2\approx-0\dc73}"))],
 [prob(L(r"Troba el valor de \(k\) perquè l'equació \(x^2-6x+k=0\) tinga una única solució. Quina és?", r"Halla el valor de \(k\) para que la ecuación \(x^2-6x+k=0\) tenga una única solución. ¿Cuál es?", r"Find \(k\) so that \(x^2-6x+k=0\) has exactly one solution. What is it?"),
       P(r"Ha de ser \(\Delta=0\):", r"Tiene que ser \(\Delta=0\):", r"We need \(\Delta=0\):"),
       D(r"(-6)^2-4\cdot1\cdot k=0\ \Rightarrow\ 36-4k=0\ \Rightarrow\ \boxed{k=9}"),
       D(r"x^2-6x+9=0\ \Rightarrow\ x=\frac{6\pm0}{2}=\boxed{3}")),
  prob(L(r"Per a quins valors de \(c\) l'equació \(x^2+4x+c=0\) no té solució?", r"¿Para qué valores de \(c\) la ecuación \(x^2+4x+c=0\) no tiene solución?", r"For which values of \(c\) does \(x^2+4x+c=0\) have no solution?"),
       D(r"\Delta=16-4c<0\ \Rightarrow\ 16<4c\ \Rightarrow\ \boxed{c>4}"),
       P(r"Per exemple, \(x^2+4x+5=0\) té \(\Delta=-4\): cap solució. Amb \(c=4\) hi ha una solució i amb \(c<4\), dues.", r"Por ejemplo, \(x^2+4x+5=0\) tiene \(\Delta=-4\): ninguna solución. Con \(c=4\) hay una solución y con \(c<4\), dos.", r"For example, \(x^2+4x+5=0\) has \(\Delta=-4\): no solution. With \(c=4\) there's one solution and with \(c<4\), two."))])
ce('x^2-4x+4=0', [2]); ce('3x^2+2x+1=0', []); ce('2x^2-x-3=0', ['3/2', -1]); ce('4x^2-4x+1=0', ['1/2']); ce('x^2-2x-2=0', ['1+sqrt(3)', '1-sqrt(3)']); ce('x^2+4x+5=0', []); ce('x^2+4x+4=0', [-2])
s8 += practice([
  ('★', L(r"Calcula el discriminant i digues quantes solucions té: a) \(x^2+5x+6=0\); b) \(x^2-10x+25=0\); c) \(2x^2+3x+4=0\); d) \(-x^2+2x+3=0\).", r"Calcula el discriminante y di cuántas soluciones tiene: a) \(x^2+5x+6=0\); b) \(x^2-10x+25=0\); c) \(2x^2+3x+4=0\); d) \(-x^2+2x+3=0\).", r"Work out the discriminant and say how many solutions there are: a) \(x^2+5x+6=0\); b) \(x^2-10x+25=0\); c) \(2x^2+3x+4=0\); d) \(-x^2+2x+3=0\).")),
  ('★★', L(r"e) Resol les que tinguen solució de l'exercici anterior. f) Resol \(9x^2+6x+1=0\).", r"e) Resuelve las que tengan solución del ejercicio anterior. f) Resuelve \(9x^2+6x+1=0\).", r"e) Solve the ones from the previous exercise that have solutions. f) Solve \(9x^2+6x+1=0\).")),
  ('★★★', L(r"g) Troba \(m\) perquè \(x^2+mx+9=0\) tinga una solució doble. h) Troba \(k\) perquè \(x=2\) siga solució de \(x^2+kx-6=0\) i calcula l'altra solució.", r"g) Halla \(m\) para que \(x^2+mx+9=0\) tenga una solución doble. h) Halla \(k\) para que \(x=2\) sea solución de \(x^2+kx-6=0\) y calcula la otra solución.", r"g) Find \(m\) so that \(x^2+mx+9=0\) has a double solution. h) Find \(k\) so that \(x=2\) is a solution of \(x^2+kx-6=0\) and find the other solution."))],
  D(r"\text{a)}\ \Delta=1:\ 2\qquad \text{b)}\ \Delta=0:\ 1\qquad \text{c)}\ \Delta=-23:\ 0\qquad \text{d)}\ \Delta=16:\ 2")
  + D(r"\text{e)}\ \text{a)}\ x=-2,\ -3\quad \text{b)}\ x=5\quad \text{d)}\ x=3,\ -1\qquad \text{f)}\ \Delta=0:\ x=-\frac13")
  + D(r"\text{g)}\ m^2-36=0\Rightarrow m=\pm6\qquad \text{h)}\ 4+2k-6=0\Rightarrow k=1;\ \ x^2+x-6=0:\ x=2,\ x=-3"))
ce('x^2+5x+6=0', [-2, -3]); ce('x^2-10x+25=0', [5]); ce('2x^2+3x+4=0', []); ce('-x^2+2x+3=0', [3, -1]); ce('9x^2+6x+1=0', ['-1/3']); ce('x^2+6x+9=0', [-3]); ce('x^2+x-6=0', [2, -3])

# =====================================================================
# 4.9 Problemes amb equacions de segon grau
# =====================================================================
TR9 = [("El quadrat d'un nombre", "El cuadrado de un número", "The square of a number", r"x^2"),
       ("El producte de dos nombres consecutius", "El producto de dos números consecutivos", "The product of two consecutive numbers", r"x(x+1)"),
       ("Àrea d'un quadrat de costat x", "Área de un cuadrado de lado x", "Area of a square of side x", r"x^2"),
       ("Àrea d'un rectangle d'altura x i base 3 m més llarga", "Área de un rectángulo de altura x y base 3 m más larga", "Area of a rectangle of height x and a base 3 m longer", r"x(x+3)"),
       ("Triangle rectangle de catets x, y i hipotenusa h", "Triángulo rectángulo de catetos x, y e hipotenusa h", "Right triangle with legs x, y and hypotenuse h", r"x^2+y^2=h^2")]
s9 = box('prop', L('Problemes que porten a una equació de segon grau', 'Problemas que llevan a una ecuación de segundo grado', 'Problems that lead to a quadratic'),
  P(r"Es resolen amb els mateixos passos que els de primer grau. La diferència és que l'equació sol tindre <strong>dues solucions</strong> i hem de <strong>comprovar quines tenen sentit</strong> en el problema: una longitud, una edat o un nombre de persones no poden ser negatius, i si ens demanen un nombre natural, no pot ser una fracció.",
    r"Se resuelven con los mismos pasos que los de primer grado. La diferencia es que la ecuación suele tener <strong>dos soluciones</strong> y tenemos que <strong>comprobar cuáles tienen sentido</strong> en el problema: una longitud, una edad o un número de personas no pueden ser negativos, y si nos piden un número natural, no puede ser una fracción.",
    r"They're solved with the same steps as linear ones. The difference is that the equation usually has <strong>two solutions</strong> and we must <strong>check which ones make sense</strong> in the problem: a length, an age or a number of people can't be negative, and if we're asked for a natural number it can't be a fraction.")
  + '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>' + L('Enunciat', 'Enunciado', 'In words') + '</th><th>' + L('Expressió', 'Expresión', 'Expression') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td class="l">{L(va, es, en)}</td><td>\\({e}\\)</td></tr>' for va, es, en, e in TR9) + '</tbody></table></div>'
  + note(r"De vegades les dues solucions són vàlides: si busquem «un nombre» (sense dir que siga positiu), \(x=7\) i \(x=-7\) poden ser totes dues respostes correctes.",
         r"A veces las dos soluciones son válidas: si buscamos «un número» (sin decir que sea positivo), \(x=7\) y \(x=-7\) pueden ser las dos respuestas correctas.",
         r"Sometimes both solutions are valid: if we're looking for “a number” (without saying it's positive), \(x=7\) and \(x=-7\) can both be correct answers.")
  + drill('prob2', 'Entrena: planteja i resol', 'Entrena: plantea y resuelve', 'Train: set up and solve'))
s9 += levels(
 [prob(L(r"Si al quadrat d'un nombre li restem 5, obtenim 44. Quin pot ser el nombre?", r"Si al cuadrado de un número le restamos 5, obtenemos 44. ¿Qué número puede ser?", r"The square of a number minus 5 is 44. What could the number be?"),
       D(r"x^2-5=44\ \Rightarrow\ x^2=49\ \Rightarrow\ x=\pm7"),
       P(r"Totes dues són vàlides: el nombre pot ser <strong>7 o −7</strong> (\((-7)^2-5=44\) ✓).", r"Las dos son válidas: el número puede ser <strong>7 o −7</strong> (\((-7)^2-5=44\) ✓).", r"Both are valid: the number can be <strong>7 or −7</strong> (\((-7)^2-5=44\) ✓).")),
  prob(L(r"Un rectangle fa 3 m més de llarg que d'ample i la seua àrea és 40 m². Quines dimensions té?", r"Un rectángulo mide 3 m más de largo que de ancho y su área es 40 m². ¿Qué dimensiones tiene?", r"A rectangle is 3 m longer than it is wide and its area is 40 m². What are its dimensions?"),
       P(r"\(x\) = amplària; la llargària és \(x+3\).", r"\(x\) = anchura; la longitud es \(x+3\).", r"\(x\) = width; the length is \(x+3\)."),
       D(r"x(x+3)=40\ \Rightarrow\ x^2+3x-40=0\ \Rightarrow\ x=\frac{-3\pm\sqrt{9+160}}{2}=\frac{-3\pm13}{2}=\begin{cases}5\\-8\end{cases}"),
       P(r"Una longitud no pot ser negativa: descartem \(-8\). El rectangle fa <strong>5 m × 8 m</strong> ✓", r"Una longitud no puede ser negativa: descartamos \(-8\). El rectángulo mide <strong>5 m × 8 m</strong> ✓", r"A length can't be negative: discard \(-8\). The rectangle is <strong>5 m × 8 m</strong> ✓"))],
 [prob(L(r"Troba dos nombres naturals consecutius el producte dels quals siga 156.", r"Halla dos números naturales consecutivos cuyo producto sea 156.", r"Find two consecutive natural numbers whose product is 156."),
       D(r"x(x+1)=156\ \Rightarrow\ x^2+x-156=0\ \Rightarrow\ x=\frac{-1\pm\sqrt{1+624}}{2}=\frac{-1\pm25}{2}=\begin{cases}12\\-13\end{cases}"),
       P(r"\(-13\) no és natural. Els nombres són <strong>12 i 13</strong> (\(12\cdot13=156\) ✓).", r"\(-13\) no es natural. Los números son <strong>12 y 13</strong> (\(12\cdot13=156\) ✓).", r"\(-13\) isn't natural. The numbers are <strong>12 and 13</strong> (\(12\cdot13=156\) ✓).")),
  prob(L(r"Els catets d'un triangle rectangle mesuren \(x\) i \(x+7\) cm, i la hipotenusa 13 cm. Quant mesuren els catets?", r"Los catetos de un triángulo rectángulo miden \(x\) y \(x+7\) cm, y la hipotenusa 13 cm. ¿Cuánto miden los catetos?", r"The legs of a right triangle are \(x\) and \(x+7\) cm long and the hypotenuse is 13 cm. How long are the legs?"),
       P(r"Pel teorema de Pitàgores:", r"Por el teorema de Pitágoras:", r"By Pythagoras' theorem:"),
       D(r"x^2+(x+7)^2=13^2\ \Rightarrow\ 2x^2+14x+49=169\ \Rightarrow\ 2x^2+14x-120=0\ \Rightarrow\ x^2+7x-60=0"),
       D(r"x=\frac{-7\pm\sqrt{49+240}}{2}=\frac{-7\pm17}{2}=\begin{cases}5\\-12\ (\text{%s})\end{cases}" % Lt('no val', 'no vale', 'not valid')),
       P(r"Els catets fan <strong>5 cm i 12 cm</strong>. Comprovació: \(25+144=169\) ✓", r"Los catetos miden <strong>5 cm y 12 cm</strong>. Comprobación: \(25+144=169\) ✓", r"The legs are <strong>5 cm and 12 cm</strong>. Check: \(25+144=169\) ✓"))],
 [prob(L(r"La suma dels quadrats de tres nombres consecutius és 110. Quins són?", r"La suma de los cuadrados de tres números consecutivos es 110. ¿Cuáles son?", r"The squares of three consecutive numbers add up to 110. What are the numbers?"),
       D(r"x^2+(x+1)^2+(x+2)^2=110\ \Rightarrow\ 3x^2+6x+5=110\ \Rightarrow\ 3x^2+6x-105=0\ \Rightarrow\ x^2+2x-35=0"),
       D(r"x=\frac{-2\pm\sqrt{4+140}}{2}=\frac{-2\pm12}{2}=\begin{cases}5\\-7\end{cases}"),
       P(r"Ací les dues solucions tenen sentit: els nombres poden ser <strong>5, 6 i 7</strong> o bé <strong>−7, −6 i −5</strong> (\(25+36+49=110\) ✓).", r"Aquí las dos soluciones tienen sentido: los números pueden ser <strong>5, 6 y 7</strong> o bien <strong>−7, −6 y −5</strong> (\(25+36+49=110\) ✓).", r"Here both solutions make sense: the numbers can be <strong>5, 6 and 7</strong> or <strong>−7, −6 and −5</strong> (\(25+36+49=110\) ✓).")),
  prob(L(r"Un jardí rectangular de 12 m × 8 m està envoltat per un camí d'amplària constant. Si l'àrea total (jardí i camí) és 192 m², quina amplària té el camí?", r"Un jardín rectangular de 12 m × 8 m está rodeado por un camino de anchura constante. Si el área total (jardín y camino) es 192 m², ¿qué anchura tiene el camino?", r"A 12 m × 8 m rectangular garden is surrounded by a path of constant width. If the total area (garden and path) is 192 m², how wide is the path?"),
       P(r"\(x\) = amplària del camí. El camí s'afig pels dos costats: les dimensions totals són \(12+2x\) i \(8+2x\).", r"\(x\) = anchura del camino. El camino se añade por los dos lados: las dimensiones totales son \(12+2x\) y \(8+2x\).", r"\(x\) = width of the path. It's added on both sides: the overall dimensions are \(12+2x\) and \(8+2x\)."),
       D(r"(12+2x)(8+2x)=192\ \Rightarrow\ 4x^2+40x+96=192\ \Rightarrow\ 4x^2+40x-96=0\ \Rightarrow\ x^2+10x-24=0"),
       D(r"x=\frac{-10\pm\sqrt{100+96}}{2}=\frac{-10\pm14}{2}=\begin{cases}2\\-12\ (\text{%s})\end{cases}" % Lt('no val', 'no vale', 'not valid')),
       P(r"El camí fa <strong>2 m</strong> d'ample: \(16\cdot12=192\) ✓", r"El camino mide <strong>2 m</strong> de ancho: \(16\cdot12=192\) ✓", r"The path is <strong>2 m</strong> wide: \(16\cdot12=192\) ✓"))])
ce('x^2-5=44', [7, -7]); ce('x(x+3)=40', [5, -8]); ce('x(x+1)=156', [12, -13]); ce('x^2+(x+7)^2=169', [5, -12]); ce('x^2+(x+1)^2+(x+2)^2=110', [5, -7]); ce('(12+2x)(8+2x)=192', [2, -12])
s9 += practice([
  ('★', L(r"a) El quadrat d'un nombre positiu és 81. Quin és? b) L'àrea d'un quadrat és 144 cm². Quant fa el costat? c) El triple del quadrat d'un nombre és 75. Quin pot ser el nombre?",
          r"a) El cuadrado de un número positivo es 81. ¿Cuál es? b) El área de un cuadrado es 144 cm². ¿Cuánto mide el lado? c) El triple del cuadrado de un número es 75. ¿Qué número puede ser?",
          r"a) The square of a positive number is 81. What is it? b) A square has an area of 144 cm². How long is its side? c) Three times the square of a number is 75. What could the number be?")),
  ('★★', L(r"d) La suma d'un nombre i el seu quadrat és 56. Quin nombre pot ser? e) La base d'un rectangle fa 4 cm més que l'altura i l'àrea és 60 cm². Quines dimensions té? f) El producte de dos nombres parells consecutius és 168. Quins són?",
           r"d) La suma de un número y su cuadrado es 56. ¿Qué número puede ser? e) La base de un rectángulo mide 4 cm más que la altura y el área es 60 cm². ¿Qué dimensiones tiene? f) El producto de dos números pares consecutivos es 168. ¿Cuáles son?",
           r"d) A number plus its square is 56. What could the number be? e) A rectangle's base is 4 cm longer than its height and its area is 60 cm². What are its dimensions? f) Two consecutive even numbers multiply to 168. What are they?")),
  ('★★★', L(r"g) Un rectangle té 34 m de perímetre i 60 m² d'àrea. Quines dimensions té? h) La hipotenusa d'un triangle rectangle fa 10 cm i un catet fa 2 cm més que l'altre. Quant fan els catets?",
            r"g) Un rectángulo tiene 34 m de perímetro y 60 m² de área. ¿Qué dimensiones tiene? h) La hipotenusa de un triángulo rectángulo mide 10 cm y un cateto mide 2 cm más que el otro. ¿Cuánto miden los catetos?",
            r"g) A rectangle has a perimeter of 34 m and an area of 60 m². What are its dimensions? h) A right triangle has a 10 cm hypotenuse and one leg is 2 cm longer than the other. How long are the legs?"))],
  D(r"\text{a)}\ x^2=81\Rightarrow x=9\qquad \text{b)}\ x^2=144\Rightarrow x=12\ \text{cm}\qquad \text{c)}\ 3x^2=75\Rightarrow x^2=25\Rightarrow x=\pm5")
  + D(r"\text{d)}\ x^2+x-56=0\Rightarrow x=7\ \text{%s}\ x=-8\qquad \text{e)}\ x(x+4)=60\Rightarrow x^2+4x-60=0\Rightarrow x=6:\ 6\ \text{cm}\times10\ \text{cm}" % Lt('o', 'o', 'or'))
  + D(r"\text{f)}\ 2x(2x+2)=168\Rightarrow x^2+x-42=0\Rightarrow x=6:\ 12\ \text{%s}\ 14\ \ (\text{%s}\ -14\ \text{%s}\ -12)" % (Lt('i', 'y', 'and'), Lt('o bé', 'o bien', 'or'), Lt('i', 'y', 'and')))
  + D(r"\text{g)}\ x(17-x)=60\Rightarrow x^2-17x+60=0\Rightarrow x=12,\ 5:\ 12\ \text{m}\times5\ \text{m}\qquad \text{h)}\ x^2+(x+2)^2=100\Rightarrow x^2+2x-48=0\Rightarrow x=6:\ 6\ \text{cm}\ \text{%s}\ 8\ \text{cm}" % Lt('i', 'y', 'and')))
ce('x^2=81', [9, -9]); ce('x^2=144', [12, -12]); ce('3x^2=75', [5, -5]); ce('x^2+x=56', [7, -8]); ce('x(x+4)=60', [6, -10]); ce('2x(2x+2)=168', [6, -7]); ce('x(17-x)=60', [12, 5]); ce('x^2+(x+2)^2=100', [6, -8])
