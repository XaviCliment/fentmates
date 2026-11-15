# Apartats 4.1-4.5 dels apunts de la Unitat 4 de 2n ESO: equacions de primer grau i problemes.
# Fet a partir de ../3eso-t5/build.py (5.1-5.3 i 5.7), amb el nivell de 2n. Les solucions es comproven amb sympy (ce).
from comu import *

# =====================================================================
# 4.1 Equacions: elements i solucions
# =====================================================================
s1 = box('def', L('Igualtats algebraiques: identitats i equacions', 'Igualdades algebraicas: identidades y ecuaciones', 'Algebraic equalities: identities and equations'),
  P(r"Una <strong>igualtat algebraica</strong> està formada per dues expressions algebraiques unides pel signe \(=\). N'hi ha de dos tipus:",
    r"Una <strong>igualdad algebraica</strong> está formada por dos expresiones algebraicas unidas por el signo \(=\). Las hay de dos tipos:",
    r"An <strong>algebraic equality</strong> is made of two algebraic expressions joined by an \(=\) sign. There are two kinds:")
  + ul(L(r"Una <strong>identitat</strong> és una igualtat que es compleix per a <strong>qualsevol valor</strong> de les lletres. Per exemple, \(x+x=2x\) o \(2(x+3)=2x+6\).",
         r"Una <strong>identidad</strong> es una igualdad que se cumple para <strong>cualquier valor</strong> de las letras. Por ejemplo, \(x+x=2x\) o \(2(x+3)=2x+6\).",
         r"An <strong>identity</strong> is an equality that holds for <strong>every value</strong> of the letters. For example, \(x+x=2x\) or \(2(x+3)=2x+6\)."),
       L(r"Una <strong>equació</strong> és una igualtat que només es compleix per a <strong>alguns valors</strong> (o per a cap). Per exemple, \(2x+3=11\) només és certa si \(x=4\).",
         r"Una <strong>ecuación</strong> es una igualdad que solo se cumple para <strong>algunos valores</strong> (o para ninguno). Por ejemplo, \(2x+3=11\) solo es cierta si \(x=4\).",
         r"An <strong>equation</strong> is an equality that only holds for <strong>some values</strong> (or none). For example, \(2x+3=11\) is only true when \(x=4\)."))
  + note(r"Per a saber si una igualtat és una identitat, operem i simplifiquem cada membre: si queden <strong>exactament iguals</strong>, és una identitat. Les identitats notables de la unitat anterior en són exemples.",
         r"Para saber si una igualdad es una identidad, operamos y simplificamos cada miembro: si quedan <strong>exactamente iguales</strong>, es una identidad. Las identidades notables de la unidad anterior son ejemplos.",
         r"To tell whether an equality is an identity, work out and simplify each side: if they end up <strong>exactly the same</strong>, it's an identity. The special products from the last unit are examples."))
s1 += box('def', L("Elements d'una equació", 'Elementos de una ecuación', 'Parts of an equation'),
  D(r"\underbrace{3x^2-5}_{\text{%s}}=\underbrace{2x+3}_{\text{%s}}" % (Lt('1r membre', '1.er miembro', 'left side'), Lt('2n membre', '2.º miembro', 'right side')))
  + ul(L(r"Els <strong>membres</strong> són les expressions que hi ha a cada costat del signe igual: el <strong>primer membre</strong> (a l'esquerra) i el <strong>segon membre</strong> (a la dreta).", r"Los <strong>miembros</strong> son las expresiones que hay a cada lado del signo igual: el <strong>primer miembro</strong> (a la izquierda) y el <strong>segundo miembro</strong> (a la derecha).", r"The <strong>sides</strong> are the expressions on each side of the equals sign: the <strong>left-hand side</strong> and the <strong>right-hand side</strong>."),
       L(r"Els <strong>termes</strong> són cadascun dels sumands: \(3x^2,\ -5,\ 2x,\ 3\). Els que no tenen lletra són <strong>termes independents</strong>.", r"Los <strong>términos</strong> son cada uno de los sumandos: \(3x^2,\ -5,\ 2x,\ 3\). Los que no tienen letra son <strong>términos independientes</strong>.", r"The <strong>terms</strong> are the parts being added: \(3x^2,\ -5,\ 2x,\ 3\). Those with no letter are <strong>constant terms</strong>."),
       L(r"La <strong>incògnita</strong> és la lletra el valor de la qual volem trobar (ací, \(x\)).", r"La <strong>incógnita</strong> es la letra cuyo valor queremos hallar (aquí, \(x\)).", r"The <strong>unknown</strong> is the letter whose value we want to find (here, \(x\))."),
       L(r"El <strong>grau</strong> és el major exponent de la incògnita <strong>un cop reduïda</strong> l'equació. Aquesta és de <strong>segon grau</strong>; \(2x+3=11\) és de <strong>primer grau</strong>.", r"El <strong>grado</strong> es el mayor exponente de la incógnita <strong>una vez reducida</strong> la ecuación. Esta es de <strong>segundo grado</strong>; \(2x+3=11\) es de <strong>primer grado</strong>.", r"The <strong>degree</strong> is the highest power of the unknown <strong>once the equation is simplified</strong>. This one is <strong>quadratic</strong> (degree 2); \(2x+3=11\) is <strong>linear</strong> (degree 1)."),
       L(r"Una <strong>solució</strong> és un valor de la incògnita que fa certa la igualtat. <strong>Resoldre</strong> una equació és trobar <em>totes</em> les seues solucions.", r"Una <strong>solución</strong> es un valor de la incógnita que hace cierta la igualdad. <strong>Resolver</strong> una ecuación es hallar <em>todas</em> sus soluciones.", r"A <strong>solution</strong> is a value of the unknown that makes the equality true. <strong>Solving</strong> an equation means finding <em>all</em> its solutions."))
  + note(r"Compte amb el grau: \(x(x+2)=x^2+5\) sembla de grau 2, però en operar queda \(x^2+2x=x^2+5\Rightarrow 2x=5\): és de <strong>primer grau</strong>.",
         r"Cuidado con el grado: \(x(x+2)=x^2+5\) parece de grado 2, pero al operar queda \(x^2+2x=x^2+5\Rightarrow 2x=5\): es de <strong>primer grado</strong>.",
         r"Careful with the degree: \(x(x+2)=x^2+5\) looks like degree 2, but working it out gives \(x^2+2x=x^2+5\Rightarrow 2x=5\): it's <strong>first degree</strong>.", '⚠'))
s1 += box('prop', L('Com comprovem si un nombre és solució?', '¿Cómo comprobamos si un número es solución?', 'How do we check whether a number is a solution?'),
  P(r"<strong>Substituïm</strong> la incògnita pel nombre en <strong>cada membre</strong> per separat i calculem. Si els dos resultats coincideixen, és solució.",
    r"<strong>Sustituimos</strong> la incógnita por el número en <strong>cada miembro</strong> por separado y calculamos. Si los dos resultados coinciden, es solución.",
    r"<strong>Substitute</strong> the number for the unknown in <strong>each side</strong> separately and work them out. If both results match, it's a solution.")
  + D(r"4x-1=2x+5:\qquad x=3\ \to\ 4\cdot3-1=11,\quad 2\cdot3+5=11\ \checkmark\qquad x=2\ \to\ 4\cdot2-1=7,\quad 2\cdot2+5=9\ \times")
  + P(r"Per tant, \(x=3\) és solució i \(x=2\) no ho és. Les equacions de segon grau poden tindre <strong>dues</strong> solucions: \(x^2+1=3x-1\) es compleix per a \(x=1\) i per a \(x=2\) (comprova-ho!).",
      r"Por tanto, \(x=3\) es solución y \(x=2\) no lo es. Las ecuaciones de segundo grado pueden tener <strong>dos</strong> soluciones: \(x^2+1=3x-1\) se cumple para \(x=1\) y para \(x=2\) (¡compruébalo!).",
      r"So \(x=3\) is a solution and \(x=2\) isn't. Quadratic equations can have <strong>two</strong> solutions: \(x^2+1=3x-1\) holds for \(x=1\) and for \(x=2\) (check it!).")
  + widget('w-check', '🔍', L('És solució?', '¿Es solución?', 'Is it a solution?'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), '4x-1=2x+5') + tin('x', 'x =', '3', 's') + '</div>', HELP,
            quick([('4x-1=2x+5|3', '4x−1 = 2x+5, x = 3'), ('4x-1=2x+5|2', '4x−1 = 2x+5, x = 2'), ('2(x+3)=2x+6|5', '2(x+3) = 2x+6'), ('x/2+x/3=5|6', 'x/2 + x/3 = 5, x = 6'), ('x^2+1=3x-1|2', 'x²+1 = 3x−1, x = 2'), ('x^2-2x=3|-1', 'x²−2x = 3, x = −1')])]))
ce('4x-1=2x+5', [3]); ce('x^2+1=3x-1', [1, 2]); ce('2x+3=11', [4]); ce('2(x+3)=2x+6', 'totes'); ce('x(x+2)=x^2+5', ['5/2'])
s1 += levels(
 [prob(L(r"Indica quines igualtats són identitats i quines són equacions: a) \(3(x-2)=3x-6\); b) \(3x-2=7\); c) \(5x-x=4x\); d) \(x^2=9\).",
         r"Indica qué igualdades son identidades y cuáles son ecuaciones: a) \(3(x-2)=3x-6\); b) \(3x-2=7\); c) \(5x-x=4x\); d) \(x^2=9\).",
         r"Say which equalities are identities and which are equations: a) \(3(x-2)=3x-6\); b) \(3x-2=7\); c) \(5x-x=4x\); d) \(x^2=9\)."),
       P(r"a) En operar, el primer membre és \(3x-6\), igual que el segon: <strong>identitat</strong>. c) \(5x-x\) sempre és \(4x\): <strong>identitat</strong>.",
         r"a) Al operar, el primer miembro es \(3x-6\), igual que el segundo: <strong>identidad</strong>. c) \(5x-x\) siempre es \(4x\): <strong>identidad</strong>.",
         r"a) Working it out, the left side is \(3x-6\), the same as the right: <strong>identity</strong>. c) \(5x-x\) is always \(4x\): <strong>identity</strong>."),
       P(r"b) Només es compleix per a \(x=3\): <strong>equació</strong>. d) Només per a \(x=3\) i \(x=-3\): <strong>equació</strong>.",
         r"b) Solo se cumple para \(x=3\): <strong>ecuación</strong>. d) Solo para \(x=3\) y \(x=-3\): <strong>ecuación</strong>.",
         r"b) Only true for \(x=3\): <strong>equation</strong>. d) Only for \(x=3\) and \(x=-3\): <strong>equation</strong>.")),
  prob(L(r"Comprova si \(x=-1\) i \(x=2\) són solucions de \(x^2-2x=3\).", r"Comprueba si \(x=-1\) y \(x=2\) son soluciones de \(x^2-2x=3\).", r"Check whether \(x=-1\) and \(x=2\) are solutions of \(x^2-2x=3\)."),
       D(r"x=-1:\quad (-1)^2-2\cdot(-1)=1+2=3\ \checkmark\qquad\Rightarrow\ \boxed{\text{%s}}" % Lt('sí és solució', 'sí es solución', 'it is a solution')),
       D(r"x=2:\quad 2^2-2\cdot2=0\neq3\qquad\Rightarrow\ \boxed{\text{%s}}" % Lt('no és solució', 'no es solución', "it isn't a solution")))],
 [prob(L(r"En l'equació \(5x^2-3x+1=2x-7\), indica els membres, els termes, la incògnita i el grau.", r"En la ecuación \(5x^2-3x+1=2x-7\), indica los miembros, los términos, la incógnita y el grado.", r"In the equation \(5x^2-3x+1=2x-7\), give the sides, the terms, the unknown and the degree."),
       P(r"1r membre: \(5x^2-3x+1\); 2n membre: \(2x-7\). Termes: \(5x^2,\ -3x,\ 1,\ 2x,\ -7\). Incògnita: \(x\). Grau: <strong>2</strong>.", r"1.er miembro: \(5x^2-3x+1\); 2.º miembro: \(2x-7\). Términos: \(5x^2,\ -3x,\ 1,\ 2x,\ -7\). Incógnita: \(x\). Grado: <strong>2</strong>.", r"Left side: \(5x^2-3x+1\); right side: \(2x-7\). Terms: \(5x^2,\ -3x,\ 1,\ 2x,\ -7\). Unknown: \(x\). Degree: <strong>2</strong>.")),
  prob(L(r"Quin grau té l'equació \(x(x-3)=x^2+6\)?", r"¿Qué grado tiene la ecuación \(x(x-3)=x^2+6\)?", r"What degree is the equation \(x(x-3)=x^2+6\)?"),
       D(r"x^2-3x=x^2+6\ \Rightarrow\ -3x=6"),
       P(r"Els termes \(x^2\) es cancel·len: és de <strong>primer grau</strong> (i la solució és \(x=-2\)).", r"Los términos \(x^2\) se cancelan: es de <strong>primer grado</strong> (y la solución es \(x=-2\)).", r"The \(x^2\) terms cancel: it's <strong>first degree</strong> (and the solution is \(x=-2\))."))],
 [prob(L(r"Troba el valor de \(k\) perquè \(x=2\) siga solució de l'equació \(kx+4=3x+k\).", r"Halla el valor de \(k\) para que \(x=2\) sea solución de la ecuación \(kx+4=3x+k\).", r"Find \(k\) so that \(x=2\) is a solution of \(kx+4=3x+k\)."),
       P(r"Si \(x=2\) és solució, en substituir s'ha de complir la igualtat:", r"Si \(x=2\) es solución, al sustituir se tiene que cumplir la igualdad:", r"If \(x=2\) is a solution, substituting must make the equality true:"),
       D(r"2k+4=3\cdot2+k\ \Rightarrow\ 2k+4=6+k\ \Rightarrow\ \boxed{k=2}"),
       P(r"Comprovació: \(2\cdot2+4=8\) i \(3\cdot2+2=8\) ✓", r"Comprobación: \(2\cdot2+4=8\) y \(3\cdot2+2=8\) ✓", r"Check: \(2\cdot2+4=8\) and \(3\cdot2+2=8\) ✓"))])
ce('x^2=9', [3, -3]); ce('3x-2=7', [3]); chk('5x-x', '4x'); ce('x^2-2x=3', [-1, 3]); ce('5x^2-3x+1=2x-7', []); ce('x(x-3)=x^2+6', [-2]); ce('2x+4=3x+2', [2])
s1 += practice([
  ('★', L(r"Identitat o equació? a) \(4(x+1)=4x+4\); b) \(4x+1=4x\); c) \(x+x+x=3x\); d) \(x+5=12\).", r"¿Identidad o ecuación? a) \(4(x+1)=4x+4\); b) \(4x+1=4x\); c) \(x+x+x=3x\); d) \(x+5=12\).", r"Identity or equation? a) \(4(x+1)=4x+4\); b) \(4x+1=4x\); c) \(x+x+x=3x\); d) \(x+5=12\).")),
  ('★★', L(r"e) Comprova quins dels nombres \(-3,\ 0,\ 1,\ 3\) són solució de \(x^2-9=0\). f) Quin grau té \((x+1)^2=x^2+7\)?", r"e) Comprueba cuáles de los números \(-3,\ 0,\ 1,\ 3\) son solución de \(x^2-9=0\). f) ¿Qué grado tiene \((x+1)^2=x^2+7\)?", r"e) Check which of the numbers \(-3,\ 0,\ 1,\ 3\) are solutions of \(x^2-9=0\). f) What degree is \((x+1)^2=x^2+7\)?")),
  ('★★★', L(r"g) Troba \(m\) perquè \(x=-1\) siga solució de \(3x+m=2m-5\).", r"g) Halla \(m\) para que \(x=-1\) sea solución de \(3x+m=2m-5\).", r"g) Find \(m\) so that \(x=-1\) is a solution of \(3x+m=2m-5\)."))],
  P(r"a) identitat; b) equació sense solució (\(1\neq0\)); c) identitat; d) equació (\(x=7\)).", r"a) identidad; b) ecuación sin solución (\(1\neq0\)); c) identidad; d) ecuación (\(x=7\)).", r"a) identity; b) equation with no solution (\(1\neq0\)); c) identity; d) equation (\(x=7\)).")
  + P(r"e) \(-3\) i \(3\) ho són; \(0\) i \(1\) no. f) \(x^2+2x+1=x^2+7\Rightarrow 2x=6\): grau 1 (\(x=3\)).", r"e) \(-3\) y \(3\) lo son; \(0\) y \(1\) no. f) \(x^2+2x+1=x^2+7\Rightarrow 2x=6\): grado 1 (\(x=3\)).", r"e) \(-3\) and \(3\) are; \(0\) and \(1\) aren't. f) \(x^2+2x+1=x^2+7\Rightarrow 2x=6\): degree 1 (\(x=3\)).")
  + D(r"\text{g)}\ 3\cdot(-1)+m=2m-5\ \Rightarrow\ -3+m=2m-5\ \Rightarrow\ m=2"))
ce('4(x+1)=4x+4', 'totes'); ce('4x+1=4x', []); ce('x+x+x=3x', 'totes'); ce('x+5=12', [7]); ce('x^2-9=0', [-3, 3]); ce('(x+1)^2=x^2+7', [3])
assert sp.solve(sp.Eq(-3 + sp.Symbol('m'), 2 * sp.Symbol('m') - 5)) == [2]

# =====================================================================
# 4.2 Equacions de primer grau
# =====================================================================
s2 = box('prop', L('Equacions equivalents: les regles de la transposició', 'Ecuaciones equivalentes: las reglas de la transposición', 'Equivalent equations: the rules for moving terms'),
  P(r"Dues equacions són <strong>equivalents</strong> si tenen les mateixes solucions. Per a resoldre una equació la transformem en altres d'equivalents cada vegada més senzilles, fins que la incògnita queda aïllada. Una equació és com una <strong>balança en equilibri</strong>: si fem el mateix als dos platets, continua equilibrada.",
    r"Dos ecuaciones son <strong>equivalentes</strong> si tienen las mismas soluciones. Para resolver una ecuación la transformamos en otras equivalentes cada vez más sencillas, hasta que la incógnita queda aislada. Una ecuación es como una <strong>balanza en equilibrio</strong>: si hacemos lo mismo en los dos platillos, sigue equilibrada.",
    r"Two equations are <strong>equivalent</strong> if they have the same solutions. To solve an equation we turn it into simpler and simpler equivalent ones until the unknown is on its own. An equation is like a <strong>balanced scale</strong>: do the same thing to both pans and it stays balanced.")
  + ul(L(r"<strong>Regla de la suma</strong>: si sumem o restem el mateix nombre als dos membres, obtenim una equació equivalent. En la pràctica: <em>el que està sumant en un membre passa a l'altre restant, i viceversa</em>.",
         r"<strong>Regla de la suma</strong>: si sumamos o restamos el mismo número a los dos miembros, obtenemos una ecuación equivalente. En la práctica: <em>lo que está sumando en un miembro pasa al otro restando, y viceversa</em>.",
         r"<strong>Addition rule</strong>: adding or subtracting the same number on both sides gives an equivalent equation. In practice: <em>a term that is added on one side moves to the other side subtracted, and vice versa</em>."),
       L(r"<strong>Regla del producte</strong>: si multipliquem o dividim els dos membres pel mateix nombre (diferent de 0), obtenim una equació equivalent. En la pràctica: <em>el que està multiplicant tot un membre passa a l'altre dividint, i viceversa</em>.",
         r"<strong>Regla del producto</strong>: si multiplicamos o dividimos los dos miembros por el mismo número (distinto de 0), obtenemos una ecuación equivalente. En la práctica: <em>lo que está multiplicando a todo un miembro pasa al otro dividiendo, y viceversa</em>.",
         r"<strong>Multiplication rule</strong>: multiplying or dividing both sides by the same (non-zero) number gives an equivalent equation. In practice: <em>a number multiplying a whole side moves to the other side dividing, and vice versa</em>."))
  + D(r"3x+5=17\ \xrightarrow{-5}\ 3x=17-5=12\ \xrightarrow{:3}\ x=\frac{12}{3}=4")
  + note(r"Quan un nombre canvia de membre, el que canvia és l'<strong>operació</strong> (suma ↔ resta, producte ↔ divisió), no el signe del nombre: en \(-2x=8\), el \(-2\) passa dividint amb el seu signe: \(x=\frac{8}{-2}=-4\).",
         r"Cuando un número cambia de miembro, lo que cambia es la <strong>operación</strong> (suma ↔ resta, producto ↔ división), no el signo del número: en \(-2x=8\), el \(-2\) pasa dividiendo con su signo: \(x=\frac{8}{-2}=-4\).",
         r"When a number moves to the other side, what changes is the <strong>operation</strong> (add ↔ subtract, multiply ↔ divide), not the sign of the number: in \(-2x=8\), the \(-2\) moves across dividing, sign included: \(x=\frac{8}{-2}=-4\).", '⚠'))
ce('3x+5=17', [4]); ce('-2x=8', [-4])
s2 += box('def', L('Equació de primer grau i passos per a resoldre-la', 'Ecuación de primer grado y pasos para resolverla', 'Linear equations and how to solve them'),
  P(r"Una <strong>equació de primer grau</strong> amb una incògnita és la que, un cop reduïda, es pot escriure així:", r"Una <strong>ecuación de primer grado</strong> con una incógnita es la que, una vez reducida, se puede escribir así:", r"A <strong>first-degree equation</strong> in one unknown is one that, once simplified, can be written as:")
  + D(r"ax=b\quad(a\neq0)\qquad\Longrightarrow\qquad x=\frac{b}{a}")
  + P(r"Té <strong>una única solució</strong>. Quan no hi ha parèntesis ni denominadors, seguim aquests passos:", r"Tiene <strong>una única solución</strong>. Cuando no hay paréntesis ni denominadores, seguimos estos pasos:", r"It has <strong>exactly one solution</strong>. When there are no brackets or fractions, follow these steps:")
  + ol(L(r"<strong>Transposem</strong>: passem els termes amb \(x\) a un membre (normalment, el primer) i els nombres a l'altre.", r"<strong>Transponemos</strong>: pasamos los términos con \(x\) a un miembro (normalmente, el primero) y los números al otro.", r"<strong>Rearrange</strong>: move the \(x\) terms to one side (usually the left) and the numbers to the other."),
       L(r"<strong>Reduïm</strong> (sumem els termes semblants) fins a tindre \(ax=b\).", r"<strong>Reducimos</strong> (sumamos los términos semejantes) hasta tener \(ax=b\).", r"<strong>Simplify</strong> (collect like terms) until you have \(ax=b\)."),
       L(r"<strong>Aïllem</strong> la \(x\): \(x=\frac{b}{a}\), i simplifiquem la fracció si es pot.", r"<strong>Despejamos</strong> la \(x\): \(x=\frac{b}{a}\), y simplificamos la fracción si se puede.", r"<strong>Isolate</strong> \(x\): \(x=\frac{b}{a}\), and simplify the fraction if possible."),
       L(r"<strong>Comprovem</strong> la solució substituint-la en l'equació inicial.", r"<strong>Comprobamos</strong> la solución sustituyéndola en la ecuación inicial.", r"<strong>Check</strong> the solution by substituting it into the original equation."))
  + D(r"5x-3=2x+9\ \Rightarrow\ 5x-2x=9+3\ \Rightarrow\ 3x=12\ \Rightarrow\ x=\frac{12}{3}=4")
  + P(r"Comprovació: \(5\cdot4-3=17\) i \(2\cdot4+9=17\) ✓", r"Comprobación: \(5\cdot4-3=17\) y \(2\cdot4+9=17\) ✓", r"Check: \(5\cdot4-3=17\) and \(2\cdot4+9=17\) ✓")
  + note(r"La solució no ha de ser entera: en \(6x+1=2x+7\) queda \(4x=6\), i \(x=\frac{6}{4}=\frac{3}{2}\). Simplifica sempre la fracció.",
         r"La solución no tiene por qué ser entera: en \(6x+1=2x+7\) queda \(4x=6\), y \(x=\frac{6}{4}=\frac{3}{2}\). Simplifica siempre la fracción.",
         r"The solution needn't be a whole number: \(6x+1=2x+7\) gives \(4x=6\), so \(x=\frac{6}{4}=\frac{3}{2}\). Always simplify the fraction.")
  + widget('w-lin', '🧮', L('Resolució pas a pas', 'Resolución paso a paso', 'Step-by-step solver'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), '5x-3=2x+9') + '</div>', HELP,
            quick([('5x-3=2x+9', '5x−3 = 2x+9'), ('6x+1=2x+7', '6x+1 = 2x+7'), ('4-3x=x+12', '4−3x = x+12'), ('3(x-2)-2(x+1)=4-x', '3(x−2)−2(x+1) = 4−x'), ('(x+1)/2-(x-2)/3=2', '(x+1)/2 − (x−2)/3 = 2'), ('2(x+1)=2x+5', '2(x+1) = 2x+5')])])
  + drill('lin1', 'Entrena: equacions de primer grau', 'Entrena: ecuaciones de primer grado', 'Train: linear equations'))
ce('5x-3=2x+9', [4]); ce('6x+1=2x+7', ['3/2']); ce('4-3x=x+12', [-2])
s2 += levels(
 [prob(L(r"Resol: a) \(x+9=4\); b) \(-5x=35\); c) \(\dfrac{x}{3}=-2\).", r"Resuelve: a) \(x+9=4\); b) \(-5x=35\); c) \(\dfrac{x}{3}=-2\).", r"Solve: a) \(x+9=4\); b) \(-5x=35\); c) \(\dfrac{x}{3}=-2\)."),
       D(r"\text{a)}\ x=4-9=\boxed{-5}\qquad\text{b)}\ x=\frac{35}{-5}=\boxed{-7}\qquad\text{c)}\ x=-2\cdot3=\boxed{-6}"),
       P(r"En c), el 3 divideix: passa a l'altre membre <strong>multiplicant</strong>.", r"En c), el 3 divide: pasa al otro miembro <strong>multiplicando</strong>.", r"In c), the 3 divides, so it moves across <strong>multiplying</strong>.")),
  prob(L(r"Resol \(7x-4=3x+8\).", r"Resuelve \(7x-4=3x+8\).", r"Solve \(7x-4=3x+8\)."),
       D(r"7x-3x=8+4\ \Rightarrow\ 4x=12\ \Rightarrow\ x=\frac{12}{4}=\boxed{3}"),
       P(r"Comprovació: \(7\cdot3-4=17\) i \(3\cdot3+8=17\) ✓", r"Comprobación: \(7\cdot3-4=17\) y \(3\cdot3+8=17\) ✓", r"Check: \(7\cdot3-4=17\) and \(3\cdot3+8=17\) ✓"))],
 [prob(L(r"Resol \(4-3x=x+12\).", r"Resuelve \(4-3x=x+12\).", r"Solve \(4-3x=x+12\)."),
       D(r"-3x-x=12-4\ \Rightarrow\ -4x=8\ \Rightarrow\ x=\frac{8}{-4}=\boxed{-2}"),
       P(r"També podríem passar les \(x\) al segon membre: \(4-12=x+3x\Rightarrow -8=4x\Rightarrow x=-2\). Ix el mateix.", r"También podríamos pasar las \(x\) al segundo miembro: \(4-12=x+3x\Rightarrow -8=4x\Rightarrow x=-2\). Sale lo mismo.", r"We could also move the \(x\) terms to the right: \(4-12=x+3x\Rightarrow -8=4x\Rightarrow x=-2\). Same answer."))],
 [prob(L(r"Resol \(5x-8+2x-3=4x+1-x+2\).", r"Resuelve \(5x-8+2x-3=4x+1-x+2\).", r"Solve \(5x-8+2x-3=4x+1-x+2\)."),
       P(r"Primer reduïm cada membre:", r"Primero reducimos cada miembro:", r"First simplify each side:"),
       D(r"7x-11=3x+3\ \Rightarrow\ 7x-3x=3+11\ \Rightarrow\ 4x=14\ \Rightarrow\ x=\frac{14}{4}=\boxed{\frac{7}{2}}"))])
ce('x+9=4', [-5]); ce('-5x=35', [-7]); ce('x/3=-2', [-6]); ce('7x-4=3x+8', [3]); ce('5x-8+2x-3=4x+1-x+2', ['7/2'])
s2 += practice([
  ('★', L(r"Resol: a) \(x-6=-2\); b) \(4x=-28\); c) \(3x+7=22\); d) \(9-2x=1\).", r"Resuelve: a) \(x-6=-2\); b) \(4x=-28\); c) \(3x+7=22\); d) \(9-2x=1\).", r"Solve: a) \(x-6=-2\); b) \(4x=-28\); c) \(3x+7=22\); d) \(9-2x=1\).")),
  ('★★', L(r"e) \(4x+7=x-5\); f) \(6-2x=3x-9\); g) \(8x-3=2x+1\).", r"e) \(4x+7=x-5\); f) \(6-2x=3x-9\); g) \(8x-3=2x+1\).", r"e) \(4x+7=x-5\); f) \(6-2x=3x-9\); g) \(8x-3=2x+1\).")),
  ('★★★', L(r"h) \(3x-5+x=10-2x+3\); i) \(2-x+4x=7x-6+x\).", r"h) \(3x-5+x=10-2x+3\); i) \(2-x+4x=7x-6+x\).", r"h) \(3x-5+x=10-2x+3\); i) \(2-x+4x=7x-6+x\)."))],
  D(r"\text{a)}\ x=4\qquad \text{b)}\ x=-7\qquad \text{c)}\ 3x=15\Rightarrow x=5\qquad \text{d)}\ -2x=-8\Rightarrow x=4")
  + D(r"\text{e)}\ 3x=-12\Rightarrow x=-4\qquad \text{f)}\ -5x=-15\Rightarrow x=3\qquad \text{g)}\ 6x=4\Rightarrow x=\frac23")
  + D(r"\text{h)}\ 4x-5=13-2x\Rightarrow 6x=18\Rightarrow x=3\qquad \text{i)}\ 3x+2=8x-6\Rightarrow -5x=-8\Rightarrow x=\frac85"))
ce('x-6=-2', [4]); ce('4x=-28', [-7]); ce('3x+7=22', [5]); ce('9-2x=1', [4]); ce('4x+7=x-5', [-4]); ce('6-2x=3x-9', [3]); ce('8x-3=2x+1', ['2/3'])
ce('3x-5+x=10-2x+3', [3]); ce('2-x+4x=7x-6+x', ['8/5'])

# =====================================================================
# 4.3 Equacions amb parèntesis
# =====================================================================
s3 = box('prop', L('Primer de tot, traiem els parèntesis', 'Primero de todo, quitamos los paréntesis', 'First of all, remove the brackets'),
  P(r"Si l'equació té parèntesis, el primer pas és eliminar-los amb la <strong>propietat distributiva</strong>: el nombre de fora multiplica <strong>cada</strong> terme de dins. Després continuem com a l'apartat anterior: transposem, reduïm i aïllem.",
    r"Si la ecuación tiene paréntesis, el primer paso es eliminarlos con la <strong>propiedad distributiva</strong>: el número de fuera multiplica <strong>cada</strong> término de dentro. Después seguimos como en el apartado anterior: transponemos, reducimos y despejamos.",
    r"If the equation has brackets, the first step is to remove them with the <strong>distributive property</strong>: the number outside multiplies <strong>every</strong> term inside. Then carry on as in the last section: rearrange, simplify and isolate.")
  + D(r"3(x-2)-2(x+1)=4-x")
  + D(r"3x-6-2x-2=4-x\ \Rightarrow\ 3x-2x+x=4+6+2\ \Rightarrow\ 2x=12\ \Rightarrow\ x=6")
  + P(r"Comprovació: \(3\cdot4-2\cdot7=12-14=-2\) i \(4-6=-2\) ✓", r"Comprobación: \(3\cdot4-2\cdot7=12-14=-2\) y \(4-6=-2\) ✓", r"Check: \(3\cdot4-2\cdot7=12-14=-2\) and \(4-6=-2\) ✓")
  + note(r"Un signe \(-\) davant d'un parèntesi <strong>canvia el signe de tots</strong> els termes de dins: \(-2(x+1)=-2x-2\) i \(-(3-x)=-3+x\).",
         r"Un signo \(-\) delante de un paréntesis <strong>cambia el signo de todos</strong> los términos de dentro: \(-2(x+1)=-2x-2\) y \(-(3-x)=-3+x\).",
         r"A \(-\) sign in front of a bracket <strong>changes the sign of every</strong> term inside: \(-2(x+1)=-2x-2\) and \(-(3-x)=-3+x\).", '⚠')
  + note(r"Si hi ha parèntesis dins de claudàtors, \([\ \ ]\), traiem primer els de dins: \(x-[2x-(3-x)]=x-[2x-3+x]=x-[3x-3]=-2x+3\).",
         r"Si hay paréntesis dentro de corchetes, \([\ \ ]\), quitamos primero los de dentro: \(x-[2x-(3-x)]=x-[2x-3+x]=x-[3x-3]=-2x+3\).",
         r"If there are brackets inside square brackets, \([\ \ ]\), remove the inner ones first: \(x-[2x-(3-x)]=x-[2x-3+x]=x-[3x-3]=-2x+3\)."))
ce('3(x-2)-2(x+1)=4-x', [6]); chk('x-(2x-(3-x))', '-2x+3')
s3 += box('prop', L('Casos especials: cap solució o infinites solucions', 'Casos especiales: ninguna solución o infinitas soluciones', 'Special cases: no solution or infinitely many'),
  P(r"De vegades, en transposar i reduir, les \(x\) es cancel·len i arribem a \(0x=b\):", r"A veces, al transponer y reducir, las \(x\) se cancelan y llegamos a \(0x=b\):", r"Sometimes, when you rearrange and simplify, the \(x\) terms cancel and you get \(0x=b\):")
  + ul(L(r"Si \(b\neq0\), cap nombre multiplicat per 0 dona \(b\): l'equació <strong>no té solució</strong>. Exemple: \(2(x+1)=2x+5\Rightarrow 2x+2=2x+5\Rightarrow 0x=3\).",
         r"Si \(b\neq0\), ningún número multiplicado por 0 da \(b\): la ecuación <strong>no tiene solución</strong>. Ejemplo: \(2(x+1)=2x+5\Rightarrow 2x+2=2x+5\Rightarrow 0x=3\).",
         r"If \(b\neq0\), no number times 0 gives \(b\): the equation has <strong>no solution</strong>. Example: \(2(x+1)=2x+5\Rightarrow 2x+2=2x+5\Rightarrow 0x=3\)."),
       L(r"Si \(b=0\), tot nombre la compleix: <strong>infinites solucions</strong> (en realitat és una identitat). Exemple: \(3(x+2)-x=2x+6\Rightarrow 2x+6=2x+6\Rightarrow 0x=0\).",
         r"Si \(b=0\), todo número la cumple: <strong>infinitas soluciones</strong> (en realidad es una identidad). Ejemplo: \(3(x+2)-x=2x+6\Rightarrow 2x+6=2x+6\Rightarrow 0x=0\).",
         r"If \(b=0\), every number works: <strong>infinitely many solutions</strong> (it's really an identity). Example: \(3(x+2)-x=2x+6\Rightarrow 2x+6=2x+6\Rightarrow 0x=0\)."))
  + P(r"La calculadora pas a pas de l'apartat anterior també resol equacions amb parèntesis: prova-hi \(7-(2x-3)=4(1-x)+12\).", r"La calculadora paso a paso del apartado anterior también resuelve ecuaciones con paréntesis: prueba \(7-(2x-3)=4(1-x)+12\).", r"The step-by-step solver in the previous section handles brackets too: try \(7-(2x-3)=4(1-x)+12\).")
  + drill('par', 'Entrena: equacions amb parèntesis', 'Entrena: ecuaciones con paréntesis', 'Train: equations with brackets'))
ce('2(x+1)=2x+5', []); ce('3(x+2)-x=2x+6', 'totes'); ce('7-(2x-3)=4(1-x)+12', [3])
s3 += levels(
 [prob(L(r"Resol \(2(x+5)=3x-1\).", r"Resuelve \(2(x+5)=3x-1\).", r"Solve \(2(x+5)=3x-1\)."),
       D(r"2x+10=3x-1\ \Rightarrow\ 2x-3x=-1-10\ \Rightarrow\ -x=-11\ \Rightarrow\ \boxed{x=11}")),
  prob(L(r"Resol \(4-(x+3)=2x-5\).", r"Resuelve \(4-(x+3)=2x-5\).", r"Solve \(4-(x+3)=2x-5\)."),
       D(r"4-x-3=2x-5\ \Rightarrow\ -x-2x=-5-4+3\ \Rightarrow\ -3x=-6\ \Rightarrow\ \boxed{x=2}"))],
 [prob(L(r"Resol \(5-3(2x-1)=4(x+2)-10\).", r"Resuelve \(5-3(2x-1)=4(x+2)-10\).", r"Solve \(5-3(2x-1)=4(x+2)-10\)."),
       P(r"Traiem parèntesis (compte amb el \(-3\): canvia el signe dels dos termes):", r"Quitamos paréntesis (cuidado con el \(-3\): cambia el signo de los dos términos):", r"Remove brackets (careful with the \(-3\): it changes the sign of both terms):"),
       D(r"5-6x+3=4x+8-10\ \Rightarrow\ -6x-4x=8-10-5-3\ \Rightarrow\ -10x=-10\ \Rightarrow\ \boxed{x=1}")),
  prob(L(r"Resol \(2(3x-1)-(x+4)=5(x-1)+1\).", r"Resuelve \(2(3x-1)-(x+4)=5(x-1)+1\).", r"Solve \(2(3x-1)-(x+4)=5(x-1)+1\)."),
       D(r"6x-2-x-4=5x-5+1\ \Rightarrow\ 5x-6=5x-4\ \Rightarrow\ 5x-5x=-4+6\ \Rightarrow\ 0x=2"),
       P(r"Cap nombre multiplicat per 0 dona 2: l'equació <strong>no té solució</strong>.", r"Ningún número multiplicado por 0 da 2: la ecuación <strong>no tiene solución</strong>.", r"No number times 0 gives 2: the equation has <strong>no solution</strong>."))],
 [prob(L(r"Resol \(x-[2x-(3-x)]=7\).", r"Resuelve \(x-[2x-(3-x)]=7\).", r"Solve \(x-[2x-(3-x)]=7\)."),
       P(r"Traiem primer el parèntesi de dins i després el claudàtor:", r"Quitamos primero el paréntesis de dentro y después el corchete:", r"Remove the inner bracket first, then the square bracket:"),
       D(r"x-[2x-3+x]=7\ \Rightarrow\ x-[3x-3]=7\ \Rightarrow\ x-3x+3=7\ \Rightarrow\ -2x=4\ \Rightarrow\ \boxed{x=-2}")),
  prob(L(r"Resol \(3(x-1)-2(4-x)=5(x+1)-16\). Què hi passa?", r"Resuelve \(3(x-1)-2(4-x)=5(x+1)-16\). ¿Qué pasa?", r"Solve \(3(x-1)-2(4-x)=5(x+1)-16\). What happens?"),
       D(r"3x-3-8+2x=5x+5-16\ \Rightarrow\ 5x-11=5x-11\ \Rightarrow\ 0x=0"),
       P(r"Els dos membres són iguals: és una identitat, i <strong>qualsevol nombre</strong> és solució (infinites solucions).", r"Los dos miembros son iguales: es una identidad, y <strong>cualquier número</strong> es solución (infinitas soluciones).", r"Both sides are the same: it's an identity, and <strong>every number</strong> is a solution (infinitely many)."))])
ce('2(x+5)=3x-1', [11]); ce('4-(x+3)=2x-5', [2]); ce('5-3(2x-1)=4(x+2)-10', [1]); ce('2(3x-1)-(x+4)=5(x-1)+1', []); ce('x-(2x-(3-x))=7', [-2]); ce('3(x-1)-2(4-x)=5(x+1)-16', 'totes')
s3 += practice([
  ('★', L(r"Resol: a) \(3(x-2)=12\); b) \(5(x+1)=2x-7\); c) \(2(x-4)=x+1\).", r"Resuelve: a) \(3(x-2)=12\); b) \(5(x+1)=2x-7\); c) \(2(x-4)=x+1\).", r"Solve: a) \(3(x-2)=12\); b) \(5(x+1)=2x-7\); c) \(2(x-4)=x+1\).")),
  ('★★', L(r"d) \(3(x-4)=2(x+1)-5\); e) \(7-(2x-3)=4(1-x)+12\); f) \(5x-2(x-1)=3x+4\).", r"d) \(3(x-4)=2(x+1)-5\); e) \(7-(2x-3)=4(1-x)+12\); f) \(5x-2(x-1)=3x+4\).", r"d) \(3(x-4)=2(x+1)-5\); e) \(7-(2x-3)=4(1-x)+12\); f) \(5x-2(x-1)=3x+4\).")),
  ('★★★', L(r"g) \(4(x-3)-(x-5)=2(x+1)\); h) \(2[3-2(x+1)]=5-3(2x-1)-x\).", r"g) \(4(x-3)-(x-5)=2(x+1)\); h) \(2[3-2(x+1)]=5-3(2x-1)-x\).", r"g) \(4(x-3)-(x-5)=2(x+1)\); h) \(2[3-2(x+1)]=5-3(2x-1)-x\)."))],
  D(r"\text{a)}\ 3x-6=12\Rightarrow x=6\qquad \text{b)}\ 5x+5=2x-7\Rightarrow 3x=-12\Rightarrow x=-4\qquad \text{c)}\ 2x-8=x+1\Rightarrow x=9")
  + D(r"\text{d)}\ 3x-12=2x-3\Rightarrow x=9\qquad \text{e)}\ 10-2x=16-4x\Rightarrow 2x=6\Rightarrow x=3\qquad \text{f)}\ 3x+2=3x+4\Rightarrow 0x=2:\ \text{%s}" % Lt('cap solució', 'ninguna solución', 'no solution'))
  + D(r"\text{g)}\ 3x-7=2x+2\Rightarrow x=9\qquad \text{h)}\ 2[1-2x]=8-7x\Rightarrow 2-4x=8-7x\Rightarrow 3x=6\Rightarrow x=2"))
ce('3(x-2)=12', [6]); ce('5(x+1)=2x-7', [-4]); ce('2(x-4)=x+1', [9]); ce('3(x-4)=2(x+1)-5', [9]); ce('5x-2(x-1)=3x+4', []); ce('4(x-3)-(x-5)=2(x+1)', [9]); ce('2(3-2(x+1))=5-3(2x-1)-x', [2])

# =====================================================================
# 4.4 Equacions amb denominadors
# =====================================================================
s4 = box('prop', L('Com eliminem els denominadors', 'Cómo eliminamos los denominadores', 'How to clear the denominators'),
  P(r"Quan hi ha fraccions, primer les eliminem multiplicant <strong>tots els termes</strong> dels dos membres pel <strong>mínim comú múltiple</strong> (m.c.m.) dels denominadors. Així obtenim una equació equivalent sense denominadors.",
    r"Cuando hay fracciones, primero las eliminamos multiplicando <strong>todos los términos</strong> de los dos miembros por el <strong>mínimo común múltiplo</strong> (m.c.m.) de los denominadores. Así obtenemos una ecuación equivalente sin denominadores.",
    r"When there are fractions, first clear them by multiplying <strong>every term</strong> on both sides by the <strong>lowest common multiple</strong> (LCM) of the denominators. This gives an equivalent equation with no denominators.")
  + ol(L(r"Calculem el m.c.m. dels denominadors.", r"Calculamos el m.c.m. de los denominadores.", r"Find the LCM of the denominators."),
       L(r"Per a cada fracció, <strong>dividim el m.c.m. entre el denominador</strong> i multipliquem el resultat pel numerador, que posem <strong>entre parèntesis</strong>. Els termes sense denominador es multipliquen pel m.c.m.",
         r"Para cada fracción, <strong>dividimos el m.c.m. entre el denominador</strong> y multiplicamos el resultado por el numerador, que ponemos <strong>entre paréntesis</strong>. Los términos sin denominador se multiplican por el m.c.m.",
         r"For each fraction, <strong>divide the LCM by the denominator</strong> and multiply the result by the numerator, written <strong>in brackets</strong>. Terms with no denominator are multiplied by the LCM."),
       L(r"Continuem com abans: parèntesis, transposició, reducció i aïllament.", r"Continuamos como antes: paréntesis, transposición, reducción y despeje.", r"Carry on as before: brackets, rearranging, simplifying and isolating."))
  + D(r"\frac{x+1}{2}-\frac{x-2}{3}=2\qquad \text{m.c.m.}(2,3)=6")
  + D(r"3(x+1)-2(x-2)=12\ \Rightarrow\ 3x+3-2x+4=12\ \Rightarrow\ x=12-7=5")
  + note(r"El signe \(-\) davant d'una fracció afecta <strong>tot el numerador</strong>: \(-\frac{x-2}{3}\) es converteix en \(-2(x-2)=-2x+4\), no en \(-2x-4\). Per això el numerador va sempre entre parèntesis.",
         r"El signo \(-\) delante de una fracción afecta a <strong>todo el numerador</strong>: \(-\frac{x-2}{3}\) se convierte en \(-2(x-2)=-2x+4\), no en \(-2x-4\). Por eso el numerador va siempre entre paréntesis.",
         r"A \(-\) sign in front of a fraction affects <strong>the whole numerator</strong>: \(-\frac{x-2}{3}\) becomes \(-2(x-2)=-2x+4\), not \(-2x-4\). That's why the numerator always goes in brackets.", '⚠')
  + note(r"No oblides multiplicar també els termes <strong>sense denominador</strong> (com el 2 del segon membre, que es converteix en 12).",
         r"No olvides multiplicar también los términos <strong>sin denominador</strong> (como el 2 del segundo miembro, que se convierte en 12).",
         r"Don't forget to multiply the terms <strong>with no denominator</strong> too (like the 2 on the right, which becomes 12).", '⚠')
  + P(r"Si només hi ha una fracció a cada membre, podem <strong>multiplicar en creu</strong>: \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\Rightarrow 2(x+3)=4(x-1)\). La calculadora pas a pas de l'apartat 4.2 també elimina els denominadors.",
      r"Si solo hay una fracción en cada miembro, podemos <strong>multiplicar en cruz</strong>: \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\Rightarrow 2(x+3)=4(x-1)\). La calculadora paso a paso del apartado 4.2 también elimina los denominadores.",
      r"If there's just one fraction on each side, you can <strong>cross-multiply</strong>: \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\Rightarrow 2(x+3)=4(x-1)\). The step-by-step solver in section 4.2 also clears denominators.")
  + drill('den', 'Entrena: equacions amb denominadors', 'Entrena: ecuaciones con denominadores', 'Train: equations with fractions'))
ce('(x+1)/2-(x-2)/3=2', [5]); ce('(x+3)/4=(x-1)/2', [5])
s4 += levels(
 [prob(L(r"Resol \(\dfrac{x}{3}+\dfrac{x}{2}=10\).", r"Resuelve \(\dfrac{x}{3}+\dfrac{x}{2}=10\).", r"Solve \(\dfrac{x}{3}+\dfrac{x}{2}=10\)."),
       D(r"\text{m.c.m.}(3,2)=6:\quad 2x+3x=60\ \Rightarrow\ 5x=60\ \Rightarrow\ \boxed{x=12}")),
  prob(L(r"Resol \(\dfrac{x+2}{3}=4\).", r"Resuelve \(\dfrac{x+2}{3}=4\).", r"Solve \(\dfrac{x+2}{3}=4\)."),
       D(r"x+2=4\cdot3=12\ \Rightarrow\ \boxed{x=10}"))],
 [prob(L(r"Resol \(\dfrac{x-1}{4}-\dfrac{x-3}{6}=1\).", r"Resuelve \(\dfrac{x-1}{4}-\dfrac{x-3}{6}=1\).", r"Solve \(\dfrac{x-1}{4}-\dfrac{x-3}{6}=1\)."),
       D(r"\text{m.c.m.}(4,6)=12:\quad 3(x-1)-2(x-3)=12"),
       D(r"3x-3-2x+6=12\ \Rightarrow\ x+3=12\ \Rightarrow\ \boxed{x=9}")),
  prob(L(r"Resol \(x-\dfrac{x+1}{3}=\dfrac{x+4}{2}\).", r"Resuelve \(x-\dfrac{x+1}{3}=\dfrac{x+4}{2}\).", r"Solve \(x-\dfrac{x+1}{3}=\dfrac{x+4}{2}\)."),
       D(r"\text{m.c.m.}(3,2)=6:\quad 6x-2(x+1)=3(x+4)"),
       D(r"6x-2x-2=3x+12\ \Rightarrow\ 4x-3x=12+2\ \Rightarrow\ \boxed{x=14}"))],
 [prob(L(r"Resol \(\dfrac{x-3}{2}-\dfrac{2(x-1)}{3}=\dfrac{x}{6}-3\).", r"Resuelve \(\dfrac{x-3}{2}-\dfrac{2(x-1)}{3}=\dfrac{x}{6}-3\).", r"Solve \(\dfrac{x-3}{2}-\dfrac{2(x-1)}{3}=\dfrac{x}{6}-3\)."),
       D(r"\text{m.c.m.}(2,3,6)=6:\quad 3(x-3)-2\cdot2(x-1)=x-18"),
       D(r"3x-9-4x+4=x-18\ \Rightarrow\ -x-5=x-18\ \Rightarrow\ -2x=-13\ \Rightarrow\ \boxed{x=\frac{13}{2}}"),
       P(r"Quan el numerador ja té un parèntesi, com \(2(x-1)\), multipliquem primer pel nombre que ix del m.c.m. (ací, 2) i després traiem el parèntesi.", r"Cuando el numerador ya tiene un paréntesis, como \(2(x-1)\), multiplicamos primero por el número que sale del m.c.m. (aquí, 2) y después quitamos el paréntesis.", r"When the numerator already has a bracket, like \(2(x-1)\), first multiply by the number from the LCM (here, 2), then remove the bracket."))])
ce('x/3+x/2=10', [12]); ce('(x+2)/3=4', [10]); ce('(x-1)/4-(x-3)/6=1', [9]); ce('x-(x+1)/3=(x+4)/2', [14]); ce('(x-3)/2-2(x-1)/3=x/6-3', ['13/2'])
s4 += practice([
  ('★', L(r"Resol: a) \(\dfrac{x}{2}-\dfrac{x}{5}=3\); b) \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\); c) \(\dfrac{3x-1}{4}=2\).", r"Resuelve: a) \(\dfrac{x}{2}-\dfrac{x}{5}=3\); b) \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\); c) \(\dfrac{3x-1}{4}=2\).", r"Solve: a) \(\dfrac{x}{2}-\dfrac{x}{5}=3\); b) \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\); c) \(\dfrac{3x-1}{4}=2\).")),
  ('★★', L(r"d) \(\dfrac{x+2}{3}-\dfrac{x-1}{4}=2\); e) \(\dfrac{x-1}{3}+\dfrac{x+2}{6}=x-2\).", r"d) \(\dfrac{x+2}{3}-\dfrac{x-1}{4}=2\); e) \(\dfrac{x-1}{3}+\dfrac{x+2}{6}=x-2\).", r"d) \(\dfrac{x+2}{3}-\dfrac{x-1}{4}=2\); e) \(\dfrac{x-1}{3}+\dfrac{x+2}{6}=x-2\).")),
  ('★★★', L(r"f) \(\dfrac{2(x-1)}{3}-\dfrac{x+1}{4}=\dfrac{x}{2}-\dfrac{3}{4}\).", r"f) \(\dfrac{2(x-1)}{3}-\dfrac{x+1}{4}=\dfrac{x}{2}-\dfrac{3}{4}\).", r"f) \(\dfrac{2(x-1)}{3}-\dfrac{x+1}{4}=\dfrac{x}{2}-\dfrac{3}{4}\)."))],
  D(r"\text{a)}\ 5x-2x=30\Rightarrow x=10\qquad \text{b)}\ x+3=2(x-1)\Rightarrow x=5\qquad \text{c)}\ 3x-1=8\Rightarrow x=3")
  + D(r"\text{d)}\ 4(x+2)-3(x-1)=24\Rightarrow x+11=24\Rightarrow x=13\qquad \text{e)}\ 2(x-1)+(x+2)=6x-12\Rightarrow 3x=6x-12\Rightarrow x=4")
  + D(r"\text{f)}\ 8(x-1)-3(x+1)=6x-9\Rightarrow 5x-11=6x-9\Rightarrow x=-2"))
ce('x/2-x/5=3', [10]); ce('(x+3)/4=(x-1)/2', [5]); ce('(3x-1)/4=2', [3]); ce('(x+2)/3-(x-1)/4=2', [13]); ce('(x-1)/3+(x+2)/6=x-2', [4]); ce('2(x-1)/3-(x+1)/4=x/2-3/4', [-2])

# =====================================================================
# 4.5 Problemes amb equacions de primer grau
# =====================================================================
TR5 = [("Un nombre i el seu doble / triple", "Un número y su doble / triple", "A number and twice / three times it", r"x,\ 2x,\ 3x"),
       ("La meitat / la tercera part d'un nombre", "La mitad / la tercera parte de un número", "Half / a third of a number", r"\frac{x}{2},\ \frac{x}{3}"),
       ("Dos nombres consecutius", "Dos números consecutivos", "Two consecutive numbers", r"x,\ x+1"),
       ("Dos nombres parells consecutius", "Dos números pares consecutivos", "Two consecutive even numbers", r"2x,\ 2x+2"),
       ("Dos nombres que sumen 20", "Dos números que suman 20", "Two numbers adding up to 20", r"x,\ 20-x"),
       ("Edat ara / d'ací a 5 anys / fa 3 anys", "Edad ahora / dentro de 5 años / hace 3 años", "Age now / in 5 years / 3 years ago", r"x,\ x+5,\ x-3"),
       ("Una fracció (2/5) d'una quantitat", "Una fracción (2/5) de una cantidad", "A fraction (2/5) of an amount", r"\frac{2}{5}x"),
       ("Un preu amb un descompte del 20 %", "Un precio con un descuento del 20 %", "A price with a 20% discount", r"0\dc8\,x"),
       ("Rectangle d'altura x i base 3 m més llarga: perímetre", "Rectángulo de altura x y base 3 m más larga: perímetro", "Rectangle of height x and a base 3 m longer: perimeter", r"2x+2(x+3)")]
s5 = box('prop', L('Com resolem un problema amb equacions', 'Cómo resolvemos un problema con ecuaciones', 'How to solve a word problem with equations'),
  ol(L(r"<strong>Llegim i entenem</strong> l'enunciat: quines dades tenim i què ens pregunten.", r"<strong>Leemos y entendemos</strong> el enunciado: qué datos tenemos y qué nos preguntan.", r"<strong>Read and understand</strong> the problem: what data you have and what you're asked."),
     L(r"<strong>Triem la incògnita</strong>: escrivim clarament què és \(x\) (normalment, el que ens pregunten) i expressem les altres quantitats en funció de \(x\).", r"<strong>Elegimos la incógnita</strong>: escribimos claramente qué es \(x\) (normalmente, lo que nos preguntan) y expresamos las otras cantidades en función de \(x\).", r"<strong>Choose the unknown</strong>: write down clearly what \(x\) is (usually what you're asked for) and express the other quantities in terms of \(x\)."),
     L(r"<strong>Plantegem l'equació</strong>: traduïm al llenguatge algebraic la relació de l'enunciat.", r"<strong>Planteamos la ecuación</strong>: traducimos al lenguaje algebraico la relación del enunciado.", r"<strong>Set up the equation</strong>: translate the relationship in the problem into algebra."),
     L(r"<strong>Resolem</strong> l'equació.", r"<strong>Resolvemos</strong> la ecuación.", r"<strong>Solve</strong> the equation."),
     L(r"<strong>Comprovem i interpretem</strong> la solució: responem la pregunta amb una frase i mirem que tinga sentit (no hi pot haver persones decimals ni longituds negatives…).", r"<strong>Comprobamos e interpretamos</strong> la solución: respondemos la pregunta con una frase y miramos que tenga sentido (no puede haber personas decimales ni longitudes negativas…).", r"<strong>Check and interpret</strong> the solution: answer the question in a sentence and make sure it makes sense (no fractions of people, no negative lengths…).")))
s5 += box('prop', L('Traduccions útils', 'Traducciones útiles', 'Useful translations'),
  '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>' + L('Enunciat', 'Enunciado', 'In words') + '</th><th>' + L('Expressió', 'Expresión', 'Expression') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td class="l">{L(va, es, en)}</td><td>\\({e}\\)</td></tr>' for va, es, en, e in TR5) + '</tbody></table></div>'
  + note(r"En els problemes d'edats, el temps passa <strong>igual per a tothom</strong>: si d'ací a \(x\) anys la mare té \(38+x\), el fill en tindrà \(10+x\).",
         r"En los problemas de edades, el tiempo pasa <strong>igual para todos</strong>: si dentro de \(x\) años la madre tiene \(38+x\), el hijo tendrá \(10+x\).",
         r"In age problems, time passes <strong>equally for everyone</strong>: if in \(x\) years the mother is \(38+x\), the son will be \(10+x\).")
  + drill('prob', 'Entrena: planteja i resol', 'Entrena: plantea y resuelve', 'Train: set up and solve'))
s5 += levels(
 [prob(L(r"La suma de tres nombres consecutius és 84. Quins són?", r"La suma de tres números consecutivos es 84. ¿Cuáles son?", r"Three consecutive numbers add up to 84. What are they?"),
       P(r"Incògnita: \(x\) = el menor; els altres són \(x+1\) i \(x+2\).", r"Incógnita: \(x\) = el menor; los otros son \(x+1\) y \(x+2\).", r"Unknown: \(x\) = the smallest; the others are \(x+1\) and \(x+2\)."),
       D(r"x+(x+1)+(x+2)=84\ \Rightarrow\ 3x+3=84\ \Rightarrow\ 3x=81\ \Rightarrow\ x=27"),
       P(r"Els nombres són <strong>27, 28 i 29</strong>. Comprovació: \(27+28+29=84\) ✓", r"Los números son <strong>27, 28 y 29</strong>. Comprobación: \(27+28+29=84\) ✓", r"The numbers are <strong>27, 28 and 29</strong>. Check: \(27+28+29=84\) ✓")),
  prob(L(r"La Laura té el triple de cromos que el Pau i entre els dos en tenen 64. Quants en té cadascun?", r"Laura tiene el triple de cromos que Pau y entre los dos tienen 64. ¿Cuántos tiene cada uno?", r"Laura has three times as many stickers as Pau, and together they have 64. How many does each have?"),
       P(r"\(x\) = cromos del Pau; la Laura en té \(3x\).", r"\(x\) = cromos de Pau; Laura tiene \(3x\).", r"\(x\) = Pau's stickers; Laura has \(3x\)."),
       D(r"x+3x=64\ \Rightarrow\ 4x=64\ \Rightarrow\ x=16"),
       P(r"El Pau en té <strong>16</strong> i la Laura <strong>48</strong> (\(16+48=64\) ✓).", r"Pau tiene <strong>16</strong> y Laura <strong>48</strong> (\(16+48=64\) ✓).", r"Pau has <strong>16</strong> and Laura <strong>48</strong> (\(16+48=64\) ✓)."))],
 [prob(L(r"Una mare té 38 anys i el seu fill, 10. Quants anys han de passar perquè l'edat de la mare siga el doble que la del fill?", r"Una madre tiene 38 años y su hijo, 10. ¿Cuántos años tienen que pasar para que la edad de la madre sea el doble que la del hijo?", r"A mother is 38 and her son is 10. How many years until the mother is twice as old as her son?"),
       P(r"\(x\) = anys que han de passar. Aleshores la mare tindrà \(38+x\) i el fill \(10+x\).", r"\(x\) = años que tienen que pasar. Entonces la madre tendrá \(38+x\) y el hijo \(10+x\).", r"\(x\) = number of years. Then the mother will be \(38+x\) and the son \(10+x\)."),
       D(r"38+x=2(10+x)\ \Rightarrow\ 38+x=20+2x\ \Rightarrow\ 18=x"),
       P(r"D'ací a <strong>18 anys</strong>: la mare en tindrà 56 i el fill 28, que és la meitat ✓", r"Dentro de <strong>18 años</strong>: la madre tendrá 56 y el hijo 28, que es la mitad ✓", r"In <strong>18 years</strong>: the mother will be 56 and the son 28, which is half ✓")),
  prob(L(r"En una classe, \(\frac13\) de l'alumnat ve en autobús, \(\frac25\) a peu i els 8 restants en bicicleta. Quants alumnes hi ha?", r"En una clase, \(\frac13\) del alumnado viene en autobús, \(\frac25\) a pie y los 8 restantes en bicicleta. ¿Cuántos alumnos hay?", r"In a class, \(\frac13\) of the students come by bus, \(\frac25\) on foot and the other 8 by bike. How many students are there?"),
       P(r"\(x\) = nombre total d'alumnes. La suma de les tres parts és el total:", r"\(x\) = número total de alumnos. La suma de las tres partes es el total:", r"\(x\) = total number of students. The three parts add up to the total:"),
       D(r"\frac{x}{3}+\frac{2x}{5}+8=x\ \xrightarrow{\cdot15}\ 5x+6x+120=15x\ \Rightarrow\ 120=4x\ \Rightarrow\ x=30"),
       P(r"Hi ha <strong>30 alumnes</strong>: 10 en autobús, 12 a peu i 8 en bici ✓", r"Hay <strong>30 alumnos</strong>: 10 en autobús, 12 a pie y 8 en bici ✓", r"There are <strong>30 students</strong>: 10 by bus, 12 on foot and 8 by bike ✓"))],
 [prob(L(r"En un corral hi ha gallines i conills: en total, 40 caps i 110 potes. Quants animals hi ha de cada tipus?", r"En un corral hay gallinas y conejos: en total, 40 cabezas y 110 patas. ¿Cuántos animales hay de cada tipo?", r"A farmyard has hens and rabbits: 40 heads and 110 legs in all. How many of each are there?"),
       P(r"\(x\) = gallines (2 potes); conills: \(40-x\) (4 potes).", r"\(x\) = gallinas (2 patas); conejos: \(40-x\) (4 patas).", r"\(x\) = hens (2 legs); rabbits: \(40-x\) (4 legs)."),
       D(r"2x+4(40-x)=110\ \Rightarrow\ 2x+160-4x=110\ \Rightarrow\ -2x=-50\ \Rightarrow\ x=25"),
       P(r"Hi ha <strong>25 gallines i 15 conills</strong>: \(50+60=110\) potes ✓", r"Hay <strong>25 gallinas y 15 conejos</strong>: \(50+60=110\) patas ✓", r"There are <strong>25 hens and 15 rabbits</strong>: \(50+60=110\) legs ✓")),
  prob(L(r"Dos ciclistes ixen alhora de dues ciutats separades 90 km i van l'un cap a l'altre, a 20 km/h i a 25 km/h. Quant de temps tarden a trobar-se? A quina distància de la primera ciutat es troben?", r"Dos ciclistas salen a la vez de dos ciudades separadas 90 km y van el uno hacia el otro, a 20 km/h y a 25 km/h. ¿Cuánto tardan en encontrarse? ¿A qué distancia de la primera ciudad se encuentran?", r"Two cyclists set off at the same time from two towns 90 km apart and ride towards each other at 20 km/h and 25 km/h. How long until they meet? How far from the first town?"),
       P(r"\(t\) = hores fins que es troben. Distància = velocitat · temps, i entre els dos recorren els 90 km:", r"\(t\) = horas hasta que se encuentran. Distancia = velocidad · tiempo, y entre los dos recorren los 90 km:", r"\(t\) = hours until they meet. Distance = speed · time, and together they cover the 90 km:"),
       D(r"20t+25t=90\ \Rightarrow\ 45t=90\ \Rightarrow\ t=2"),
       P(r"Es troben al cap de <strong>2 hores</strong>, a \(20\cdot2=\) <strong>40 km</strong> de la primera ciutat (l'altre n'ha fet 50) ✓", r"Se encuentran al cabo de <strong>2 horas</strong>, a \(20\cdot2=\) <strong>40 km</strong> de la primera ciudad (el otro ha hecho 50) ✓", r"They meet after <strong>2 hours</strong>, \(20\cdot2=\) <strong>40 km</strong> from the first town (the other has ridden 50) ✓"))])
ce('x+(x+1)+(x+2)=84', [27]); ce('x+3x=64', [16]); ce('38+x=2(10+x)', [18]); ce('x/3+2x/5+8=x', [30]); ce('2x+4(40-x)=110', [25]); ce('20x+25x=90', [2])
s5 += practice([
  ('★', L(r"a) Si al triple d'un nombre li restem 7, obtenim el mateix que si al seu doble li sumem 5. Quin nombre és? b) La suma de dos nombres parells consecutius és 46. Quins són?",
          r"a) Si al triple de un número le restamos 7, obtenemos lo mismo que si a su doble le sumamos 5. ¿Qué número es? b) La suma de dos números pares consecutivos es 46. ¿Cuáles son?",
          r"a) Three times a number minus 7 is the same as twice the number plus 5. What is the number? b) Two consecutive even numbers add up to 46. What are they?")),
  ('★★', L(r"c) Un pare té 42 anys i el seu fill 12. Fa quants anys l'edat del pare era el quàdruple de la del fill? d) La base d'un rectangle fa 5 cm més que l'altura i el perímetre és 46 cm. Quines dimensions té? e) Un jersei rebaixat un 20 % costa 36 €. Quant costava abans?",
           r"c) Un padre tiene 42 años y su hijo 12. ¿Hace cuántos años la edad del padre era el cuádruple de la del hijo? d) La base de un rectángulo mide 5 cm más que la altura y el perímetro es 46 cm. ¿Qué dimensiones tiene? e) Un jersey rebajado un 20 % cuesta 36 €. ¿Cuánto costaba antes?",
           r"c) A father is 42 and his son is 12. How many years ago was the father four times as old as his son? d) A rectangle's base is 5 cm longer than its height and its perimeter is 46 cm. What are its dimensions? e) A jumper with 20% off costs €36. What was the original price?")),
  ('★★★', L(r"f) En una guardiola hi ha 30 monedes, unes d'1 € i altres de 2 €, que sumen 46 €. Quantes n'hi ha de cada tipus? g) Una persona gasta la tercera part dels seus diners en roba i la quarta part en llibres, i encara li queden 25 €. Quants diners tenia?",
            r"f) En una hucha hay 30 monedas, unas de 1 € y otras de 2 €, que suman 46 €. ¿Cuántas hay de cada tipo? g) Una persona gasta la tercera parte de su dinero en ropa y la cuarta parte en libros, y aún le quedan 25 €. ¿Cuánto dinero tenía?",
            r"f) A money box holds 30 coins, some €1 and some €2, worth €46 in all. How many of each are there? g) Someone spends a third of their money on clothes and a quarter on books, and still has €25 left. How much did they have?"))],
  D(r"\text{a)}\ 3x-7=2x+5\Rightarrow x=12\qquad \text{b)}\ 2x+(2x+2)=46\Rightarrow x=11:\ 22\ \text{%s}\ 24" % Lt('i', 'y', 'and'))
  + D(r"\text{c)}\ 42-x=4(12-x)\Rightarrow 3x=6\Rightarrow x=2\ \text{%s}\qquad \text{d)}\ 2x+2(x+5)=46\Rightarrow x=9:\ 9\ \text{cm}\times14\ \text{cm}" % Lt('anys', 'años', 'years'))
  + D(r"\text{e)}\ 0\dc8\,x=36\Rightarrow x=45\ \text{€}\qquad \text{f)}\ 2x+(30-x)=46\Rightarrow x=16:\ \text{%s}" % Lt("16 de 2 € i 14 d'1 €", '16 de 2 € y 14 de 1 €', '16 of €2 and 14 of €1'))
  + D(r"\text{g)}\ x-\frac{x}{3}-\frac{x}{4}=25\ \xrightarrow{\cdot12}\ 5x=300\Rightarrow x=60\ \text{€}"))
ce('3x-7=2x+5', [12]); ce('2x+(2x+2)=46', [11]); ce('42-x=4(12-x)', [2]); ce('2x+2(x+5)=46', [9]); ce('8x/10=36', [45]); ce('2x+(30-x)=46', [16]); ce('x-x/3-x/4=25', [60])
