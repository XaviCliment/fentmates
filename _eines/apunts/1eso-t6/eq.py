# Apartats 6.5-6.9 (equacions de primer grau i problemes) dels apunts de la Unitat 6 de 1r ESO.
from comu import *

def solver(wid, val, pairs):
    return widget(wid, '🧮', L('Resol l\'equació pas a pas', 'Resuelve la ecuación paso a paso', 'Solve the equation step by step'),
                  ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), val) + '</div>', HELP_Q, quick(pairs)])
def chain(*rows):
    """passos d'una resolució en una sola fórmula alineada"""
    return D(r'\begin{aligned}' + r'\\'.join(rows) + r'\end{aligned}')

# ============================================================ 6.5
s5 = box('def', L('Identitats i equacions', 'Identidades y ecuaciones', 'Identities and equations'),
  P(r"Una <strong>igualtat algebraica</strong> està formada per dues expressions algebraiques unides pel signe \(=\). N'hi ha de dos tipus:",
    r"Una <strong>igualdad algebraica</strong> está formada por dos expresiones algebraicas unidas por el signo \(=\). Las hay de dos tipos:",
    r"An <strong>algebraic equality</strong> is made of two algebraic expressions joined by an \(=\) sign. There are two kinds:")
  + ul(L(r"Una <strong>identitat</strong> és certa per a <strong>qualsevol valor</strong> de les lletres: \(2(x+3)=2x+6\) o \(a+b=b+a\).", r"Una <strong>identidad</strong> es cierta para <strong>cualquier valor</strong> de las letras: \(2(x+3)=2x+6\) o \(a+b=b+a\).", r"An <strong>identity</strong> is true for <strong>every value</strong> of the letters: \(2(x+3)=2x+6\) or \(a+b=b+a\)."),
       L(r"Una <strong>equació</strong> només és certa per a <strong>alguns valors</strong> de les lletres: \(x+3=7\) només és certa si \(x=4\).", r"Una <strong>ecuación</strong> solo es cierta para <strong>algunos valores</strong> de las letras: \(x+3=7\) solo es cierta si \(x=4\).", r"An <strong>equation</strong> is only true for <strong>some values</strong> of the letters: \(x+3=7\) is only true when \(x=4\).")))
s5 += box('def', L("Elements d'una equació", 'Elementos de una ecuación', 'Parts of an equation'),
  D(r"\underbrace{2x+3}_{\text{%s}}=\underbrace{x+8}_{\text{%s}}" % (Lt('1r membre', '1.er miembro', 'left side'), Lt('2n membre', '2.º miembro', 'right side')))
  + ul(L(r"Els <strong>membres</strong> són les expressions que hi ha a cada costat del signe \(=\).", r"Los <strong>miembros</strong> son las expresiones que hay a cada lado del signo \(=\).", r"The <strong>sides</strong> are the expressions on each side of the \(=\) sign."),
       L(r"Els <strong>termes</strong> són cadascun dels sumands: \(2x\), \(3\), \(x\) i \(8\).", r"Los <strong>términos</strong> son cada uno de los sumandos: \(2x\), \(3\), \(x\) y \(8\).", r"The <strong>terms</strong> are the parts being added: \(2x\), \(3\), \(x\) and \(8\)."),
       L(r"La <strong>incògnita</strong> és la lletra el valor de la qual volem trobar (ací, \(x\)).", r"La <strong>incógnita</strong> es la letra cuyo valor queremos hallar (aquí, \(x\)).", r"The <strong>unknown</strong> is the letter whose value we want to find (here, \(x\))."),
       L(r"El <strong>grau</strong> és el major exponent de la incògnita. En aquesta unitat treballem equacions de <strong>primer grau</strong>: la \(x\) no està elevada a cap exponent.", r"El <strong>grado</strong> es el mayor exponente de la incógnita. En esta unidad trabajamos ecuaciones de <strong>primer grado</strong>: la \(x\) no está elevada a ningún exponente.", r"The <strong>degree</strong> is the highest power of the unknown. In this unit we work with <strong>first-degree</strong> (linear) equations: \(x\) isn't raised to any power."),
       L(r"La <strong>solució</strong> és el valor de la incògnita que fa certa la igualtat. <strong>Resoldre</strong> una equació és trobar-ne la solució.", r"La <strong>solución</strong> es el valor de la incógnita que hace cierta la igualdad. <strong>Resolver</strong> una ecuación es hallar su solución.", r"The <strong>solution</strong> is the value of the unknown that makes the equality true. <strong>Solving</strong> an equation means finding its solution.")))
s5 += box('prop', L('Com comprovem si un nombre és solució?', '¿Cómo comprobamos si un número es solución?', 'How do we check whether a number is a solution?'),
  P(r"<strong>Substituïm</strong> la incògnita pel nombre en <strong>cada membre</strong> per separat i calculem. Si els dos membres donen el mateix resultat, és solució.",
    r"<strong>Sustituimos</strong> la incógnita por el número en <strong>cada miembro</strong> por separado y calculamos. Si los dos miembros dan el mismo resultado, es solución.",
    r"<strong>Substitute</strong> the number for the unknown in <strong>each side</strong> separately and work them out. If both sides give the same result, it's a solution.")
  + D(r"2x+3=x+8:\qquad x=5\ \to\ 2\cdot5+3=13,\quad 5+8=13\ \checkmark\qquad x=4\ \to\ 2\cdot4+3=11,\quad 4+8=12\ \times")
  + P(r"Per tant, \(x=5\) és la solució i \(x=4\) no ho és. Podem imaginar l'equació com una <strong>balança en equilibri</strong>: els dos plats pesen el mateix només quan \(x\) val 5.",
      r"Por tanto, \(x=5\) es la solución y \(x=4\) no lo es. Podemos imaginar la ecuación como una <strong>balanza en equilibrio</strong>: los dos platos pesan lo mismo solo cuando \(x\) vale 5.",
      r"So \(x=5\) is the solution and \(x=4\) isn't. We can picture the equation as a <strong>balanced scale</strong>: both pans weigh the same only when \(x\) is 5.")
  + widget('w-check', '🔍', L('És solució?', '¿Es solución?', 'Is it a solution?'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), '2x+3=x+8') + tin('x', 'x =', '5', 's') + '</div>', HELP_Q,
            quick([('2x+3=x+8|5', '2x+3 = x+8, x = 5'), ('2x+3=x+8|4', '2x+3 = x+8, x = 4'), ('3(x-1)=2x|3', '3(x−1) = 2x, x = 3'), ('10-x=2x+1|3', '10−x = 2x+1, x = 3'), ('x/2+1=x-3|8', 'x/2+1 = x−3, x = 8'), ('2(x+3)=2x+6|7', '2(x+3) = 2x+6')])])
  + drill('sol', 'Entrena: és solució? (respon sí o no)', 'Entrena: ¿es solución? (responde sí o no)', 'Train: is it a solution? (answer yes or no)'))
ce('2x+3=x+8', 5); cv('2x+3', {'x': 4}, 11); cv('x+8', {'x': 4}, 12); ce('3(x-1)=2x', 3); ce('10-x=2x+1', 3); ce('x/2+1=x-3', 8); chk('2(x+3)', '2x+6')
s5 += levels([
  prob(L(r"En l'equació \(4x-1=2x+7\), indica: els membres, els termes, la incògnita i el grau.", r"En la ecuación \(4x-1=2x+7\), indica: los miembros, los términos, la incógnita y el grado.", r"In the equation \(4x-1=2x+7\), give: the sides, the terms, the unknown and the degree."),
       P(r"1r membre: \(\boxed{4x-1}\); 2n membre: \(\boxed{2x+7}\). Termes: \(\boxed{4x,\ -1,\ 2x,\ 7}\). Incògnita: \(\boxed{x}\). Grau: \(\boxed{1}\).", r"1.er miembro: \(\boxed{4x-1}\); 2.º miembro: \(\boxed{2x+7}\). Términos: \(\boxed{4x,\ -1,\ 2x,\ 7}\). Incógnita: \(\boxed{x}\). Grado: \(\boxed{1}\).", r"Left side: \(\boxed{4x-1}\); right side: \(\boxed{2x+7}\). Terms: \(\boxed{4x,\ -1,\ 2x,\ 7}\). Unknown: \(\boxed{x}\). Degree: \(\boxed{1}\).")),
  prob(L(r"Troba mentalment la solució: a) \(x+5=12\) &nbsp; b) \(3x=15\) &nbsp; c) \(\frac{x}{4}=2\) &nbsp; d) \(10-x=6\)", r"Halla mentalmente la solución: a) \(x+5=12\) &nbsp; b) \(3x=15\) &nbsp; c) \(\frac{x}{4}=2\) &nbsp; d) \(10-x=6\)", r"Find the solution in your head: a) \(x+5=12\) &nbsp; b) \(3x=15\) &nbsp; c) \(\frac{x}{4}=2\) &nbsp; d) \(10-x=6\)"),
       P(r"Pensem quin nombre fa certa cada igualtat:", r"Pensamos qué número hace cierta cada igualdad:", r"Think which number makes each equality true:"),
       D(r"\text{a) }x=\boxed{7}\ (7+5=12)\qquad \text{b) }x=\boxed{5}\ (3\cdot5=15)\qquad \text{c) }x=\boxed{8}\ (8:4=2)\qquad \text{d) }x=\boxed{4}\ (10-4=6)"))],
  [prob(L(r"Quin d'aquests valors és la solució de \(3x-2=x+6\)? \(\ x=2,\ x=3,\ x=4\)", r"¿Cuál de estos valores es la solución de \(3x-2=x+6\)? \(\ x=2,\ x=3,\ x=4\)", r"Which of these values solves \(3x-2=x+6\)? \(\ x=2,\ x=3,\ x=4\)"),
        D(r"x=2:\ 3\cdot2-2=4,\ \ 2+6=8\ \times\qquad x=3:\ 3\cdot3-2=7,\ \ 3+6=9\ \times"),
        D(r"x=4:\ 3\cdot4-2=10,\ \ 4+6=10\ \checkmark\qquad\Rightarrow\ \boxed{x=4}"))],
  [prob(L(r"Digues si és una identitat o una equació. Si és una equació, comprova si \(x=2\) n'és la solució. a) \(3(x+1)=3x+3\) &nbsp; b) \(x^2+x=6\) &nbsp; c) \(5-2x=x-1\)", r"Di si es una identidad o una ecuación. Si es una ecuación, comprueba si \(x=2\) es su solución. a) \(3(x+1)=3x+3\) &nbsp; b) \(x^2+x=6\) &nbsp; c) \(5-2x=x-1\)", r"Say whether it is an identity or an equation. If it's an equation, check whether \(x=2\) is a solution. a) \(3(x+1)=3x+3\) &nbsp; b) \(x^2+x=6\) &nbsp; c) \(5-2x=x-1\)"),
        P(r"a) En traure el parèntesi, \(3x+3=3x+3\): els dos membres són iguals, és una \(\boxed{\text{identitat}}\).", r"a) Al quitar el paréntesis, \(3x+3=3x+3\): los dos miembros son iguales, es una \(\boxed{\text{identidad}}\).", r"a) Removing the brackets, \(3x+3=3x+3\): both sides are the same, it's an \(\boxed{\text{identity}}\)."),
        P(r"b) Equació (de segon grau). \(2^2+2=6\ \checkmark\): \(x=2\) <strong>és</strong> solució. (També ho és \(x=-3\): comprova-ho!)", r"b) Ecuación (de segundo grado). \(2^2+2=6\ \checkmark\): \(x=2\) <strong>es</strong> solución. (También lo es \(x=-3\): ¡compruébalo!)", r"b) Equation (second degree). \(2^2+2=6\ \checkmark\): \(x=2\) <strong>is</strong> a solution. (So is \(x=-3\): check it!)"),
        P(r"c) Equació. \(5-2\cdot2=1\) i \(2-1=1\ \checkmark\): \(x=2\) <strong>és</strong> la solució.", r"c) Ecuación. \(5-2\cdot2=1\) y \(2-1=1\ \checkmark\): \(x=2\) <strong>es</strong> la solución.", r"c) Equation. \(5-2\cdot2=1\) and \(2-1=1\ \checkmark\): \(x=2\) <strong>is</strong> the solution."))])
for e, s in [('x+5=12', 7), ('3x=15', 5), ('x/4=2', 8), ('10-x=6', 4), ('3x-2=x+6', 4), ('5-2x=x-1', 2)]: ce(e, s)
chk('3(x+1)', '3x+3'); cv('x^2+x', {'x': 2}, 6); cv('x^2+x', {'x': -3}, 6)
s5 += practice([
  ('★', L(r"a) Escriu els membres i els termes de \(7-x=3x+1\). b) Comprova si \(x=3\) és solució de \(2x+4=10\).", r"a) Escribe los miembros y los términos de \(7-x=3x+1\). b) Comprueba si \(x=3\) es solución de \(2x+4=10\).", r"a) Write the sides and terms of \(7-x=3x+1\). b) Check whether \(x=3\) is a solution of \(2x+4=10\).")),
  ('★★', L(r"c) Comprova si \(x=-1\) és solució de \(5x+2=x-2\). d) Troba mentalment la solució de \(2x+1=9\).", r"c) Comprueba si \(x=-1\) es solución de \(5x+2=x-2\). d) Halla mentalmente la solución de \(2x+1=9\).", r"c) Check whether \(x=-1\) solves \(5x+2=x-2\). d) Find the solution of \(2x+1=9\) in your head.")),
  ('★★★', L(r"e) Escriu una equació que tinga per solució \(x=6\) i una identitat amb la lletra \(a\).", r"e) Escribe una ecuación que tenga por solución \(x=6\) y una identidad con la letra \(a\).", r"e) Write an equation whose solution is \(x=6\) and an identity with the letter \(a\)."))],
  P(r"a) Membres \(7-x\) i \(3x+1\); termes \(7,\ -x,\ 3x,\ 1\). &nbsp; b) \(2\cdot3+4=10\ \checkmark\): sí. &nbsp; c) \(5\cdot(-1)+2=-3\) i \(-1-2=-3\ \checkmark\): sí. &nbsp; d) \(x=4\). &nbsp; e) Per exemple, \(x+4=10\) i \(2a+a=3a\).", r"a) Miembros \(7-x\) y \(3x+1\); términos \(7,\ -x,\ 3x,\ 1\). &nbsp; b) \(2\cdot3+4=10\ \checkmark\): sí. &nbsp; c) \(5\cdot(-1)+2=-3\) y \(-1-2=-3\ \checkmark\): sí. &nbsp; d) \(x=4\). &nbsp; e) Por ejemplo, \(x+4=10\) y \(2a+a=3a\).", r"a) Sides \(7-x\) and \(3x+1\); terms \(7,\ -x,\ 3x,\ 1\). &nbsp; b) \(2\cdot3+4=10\ \checkmark\): yes. &nbsp; c) \(5\cdot(-1)+2=-3\) and \(-1-2=-3\ \checkmark\): yes. &nbsp; d) \(x=4\). &nbsp; e) For example, \(x+4=10\) and \(2a+a=3a\)."))
for e, s in [('2x+4=10', 3), ('5x+2=x-2', -1), ('2x+1=9', 4), ('x+4=10', 6)]: ce(e, s)

# ============================================================ 6.6
s6 = box('def', L('Equacions equivalents', 'Ecuaciones equivalentes', 'Equivalent equations'),
  P(r"Dues equacions són <strong>equivalents</strong> si tenen la mateixa solució. Per exemple, \(2x+3=11\), \(2x=8\) i \(x=4\) són equivalents. Per a resoldre una equació la transformem en altres d'equivalents cada vegada més senzilles, fins arribar a \(x=\text{nombre}\). Ho fem amb dues regles, com si fóra una balança:",
    r"Dos ecuaciones son <strong>equivalentes</strong> si tienen la misma solución. Por ejemplo, \(2x+3=11\), \(2x=8\) y \(x=4\) son equivalentes. Para resolver una ecuación la transformamos en otras equivalentes cada vez más sencillas, hasta llegar a \(x=\text{número}\). Lo hacemos con dos reglas, como si fuera una balanza:",
    r"Two equations are <strong>equivalent</strong> if they have the same solution. For example, \(2x+3=11\), \(2x=8\) and \(x=4\) are equivalent. To solve an equation we turn it into simpler and simpler equivalent ones until we reach \(x=\text{number}\). We use two rules, as if it were a balance:")
  + ul(L(r"<strong>Regla de la suma:</strong> si sumem o restem el <strong>mateix nombre</strong> (o la mateixa expressió) als dos membres, obtenim una equació equivalent.", r"<strong>Regla de la suma:</strong> si sumamos o restamos el <strong>mismo número</strong> (o la misma expresión) a los dos miembros, obtenemos una ecuación equivalente.", r"<strong>Addition rule:</strong> adding or subtracting the <strong>same number</strong> (or expression) on both sides gives an equivalent equation."),
       L(r"<strong>Regla del producte:</strong> si multipliquem o dividim els dos membres pel <strong>mateix nombre</strong> (diferent de 0), obtenim una equació equivalent.", r"<strong>Regla del producto:</strong> si multiplicamos o dividimos los dos miembros por el <strong>mismo número</strong> (distinto de 0), obtenemos una ecuación equivalente.", r"<strong>Multiplication rule:</strong> multiplying or dividing both sides by the <strong>same number</strong> (not 0) gives an equivalent equation."))
  + chain(r"2x+3&=11", r"2x+3\,\color{#e8603a}{-3}&=11\,\color{#e8603a}{-3}", r"2x&=8", r"\frac{2x}{\color{#e8603a}{2}}&=\frac{8}{\color{#e8603a}{2}}", r"x&=\boxed{4}")
  + widget('w-bal', '⚖️', L("La balança de l'equació", 'La balanza de la ecuación', 'The equation balance'),
           [quick([('3|2|1|8', '3x + 2 = x + 8'), ('2|5|0|11', '2x + 5 = 11'), ('4|1|2|7', '4x + 1 = 2x + 7'), ('1|9|3|1', 'x + 9 = 3x + 1'), ('5|0|2|9', '5x = 2x + 9')]),
            '<div class="wrow bal-ops"><button class="btn" type="button" data-op="u">' + L('− 1 a cada plat', '− 1 en cada plato', '− 1 from each pan') + '</button><button class="btn" type="button" data-op="x">' + L('− x a cada plat', '− x en cada plato', '− x from each pan') + '</button><button class="btn primary" type="button" data-op="d">÷ <span class="bal-k">n</span></button><button class="btn" type="button" data-op="r">↺ ' + L('Torna a començar', 'Volver a empezar', 'Start again') + '</button><button class="btn" type="button" data-op="n">↻ ' + L('Una altra', 'Otra', 'Another') + '</button></div>'],
           out='<div class="fvis bal"></div><div class="hsteps"></div>'))
ce('2x+3=11', 4); ce('3x+2=x+8', 3); ce('2x+5=11', 3); ce('4x+1=2x+7', 3); ce('x+9=3x+1', 4); ce('5x=2x+9', 3)
s6 += box('prop', L('Transposició de termes', 'Transposición de términos', 'Moving terms across'),
  P(r"Aplicar les regles anteriors equival a <strong>passar</strong> un terme a l'altre membre canviant-li l'operació:", r"Aplicar las reglas anteriores equivale a <strong>pasar</strong> un término al otro miembro cambiándole la operación:", r"Using the rules above is the same as <strong>moving</strong> a term to the other side with the opposite operation:")
  + table([L('Si en un membre…', 'Si en un miembro…', 'If on one side it…'), L('…passa a l\'altre', '…pasa al otro', '…moves across'), L('Exemple', 'Ejemplo', 'Example')],
          [[L('està sumant', 'está sumando', 'is added'), L('restant', 'restando', 'subtracted'), r'\(x+7=12\ \Rightarrow\ x=12-7=\boxed{5}\)'],
           [L('està restant', 'está restando', 'is subtracted'), L('sumant', 'sumando', 'added'), r'\(x-4=-9\ \Rightarrow\ x=-9+4=\boxed{-5}\)'],
           [L('està multiplicant', 'está multiplicando', 'is multiplying'), L('dividint', 'dividiendo', 'dividing'), r'\(3x=21\ \Rightarrow\ x=\frac{21}{3}=\boxed{7}\)'],
           [L('està dividint', 'está dividiendo', 'is dividing'), L('multiplicant', 'multiplicando', 'multiplying'), r'\(\frac{x}{4}=3\ \Rightarrow\ x=3\cdot4=\boxed{12}\)']], 'data ptab')
  + note(r"El nombre que multiplica la \(x\) passa dividint <strong>amb el seu signe</strong>: \(-2x=10\Rightarrow x=\frac{10}{-2}=-5\). I \(-x=6\) vol dir \(-1\cdot x=6\), així que \(x=-6\).",
         r"El número que multiplica a la \(x\) pasa dividiendo <strong>con su signo</strong>: \(-2x=10\Rightarrow x=\frac{10}{-2}=-5\). Y \(-x=6\) quiere decir \(-1\cdot x=6\), así que \(x=-6\).",
         r"The number multiplying \(x\) moves across dividing <strong>with its sign</strong>: \(-2x=10\Rightarrow x=\frac{10}{-2}=-5\). And \(-x=6\) means \(-1\cdot x=6\), so \(x=-6\).", '⚠️'))
for e, s in [('x+7=12', 5), ('x-4=-9', -5), ('3x=21', 7), ('x/4=3', 12), ('-2x=10', -5), ('-x=6', -6)]: ce(e, s)
s6 += box('prop', L('Mètode general', 'Método general', 'General method'),
  ol(L(r"<strong>Transposem:</strong> els termes amb \(x\) a un membre (normalment, el primer) i els nombres a l'altre.", r"<strong>Transponemos:</strong> los términos con \(x\) a un miembro (normalmente, el primero) y los números al otro.", r"<strong>Rearrange:</strong> the \(x\) terms on one side (usually the left) and the numbers on the other."),
     L(r"<strong>Reduïm</strong> cada membre.", r"<strong>Reducimos</strong> cada miembro.", r"<strong>Simplify</strong> each side."),
     L(r"<strong>Aïllem</strong> la \(x\): el nombre que la multiplica passa dividint.", r"<strong>Despejamos</strong> la \(x\): el número que la multiplica pasa dividiendo.", r"<strong>Isolate</strong> \(x\): the number multiplying it moves across dividing."),
     L(r"<strong>Comprovem</strong> la solució en l'equació inicial.", r"<strong>Comprobamos</strong> la solución en la ecuación inicial.", r"<strong>Check</strong> the solution in the original equation."))
  + chain(r"5x-3&=2x+9", r"5x-2x&=9+3", r"3x&=12", r"x&=\frac{12}{3}=\boxed{4}")
  + P(r"Comprovació: \(5\cdot4-3=17\) i \(2\cdot4+9=17\ \checkmark\)", r"Comprobación: \(5\cdot4-3=17\) y \(2\cdot4+9=17\ \checkmark\)", r"Check: \(5\cdot4-3=17\) and \(2\cdot4+9=17\ \checkmark\)")
  + note(r"La solució no sempre és un nombre enter: \(4x=6\Rightarrow x=\frac{6}{4}=\frac{3}{2}\) (la deixem com a fracció irreductible). I hi ha equacions sense solució, com \(x+1=x+2\), que en reduir queda \(0x=1\): cap nombre multiplicat per 0 dona 1.",
         r"La solución no siempre es un número entero: \(4x=6\Rightarrow x=\frac{6}{4}=\frac{3}{2}\) (la dejamos como fracción irreducible). Y hay ecuaciones sin solución, como \(x+1=x+2\), que al reducir queda \(0x=1\): ningún número multiplicado por 0 da 1.",
         r"The solution isn't always a whole number: \(4x=6\Rightarrow x=\frac{6}{4}=\frac{3}{2}\) (leave it as a fraction in simplest form). And some equations have no solution, like \(x+1=x+2\), which simplifies to \(0x=1\): no number times 0 gives 1.")
  + solver('w-solve1', '5x-3=2x+9', [('5x-3=2x+9', '5x − 3 = 2x + 9'), ('x+7=12', 'x + 7 = 12'), ('-2x=10', '−2x = 10'), ('x/4=3', 'x/4 = 3'), ('7-2x=x+1', '7 − 2x = x + 1'), ('4x=6', '4x = 6'), ('x+1=x+2', 'x + 1 = x + 2')])
  + drill('eq1', 'Entrena: resol l\'equació', 'Entrena: resuelve la ecuación', 'Train: solve the equation'))
ce('5x-3=2x+9', 4); ce('4x=6', sp.Rational(3, 2)); ce('7-2x=x+1', 2)
s6 += levels([
  prob(L(r"Resol: a) \(x-8=3\) &nbsp; b) \(x+6=2\) &nbsp; c) \(5x=-35\) &nbsp; d) \(\frac{x}{3}=-2\)", r"Resuelve: a) \(x-8=3\) &nbsp; b) \(x+6=2\) &nbsp; c) \(5x=-35\) &nbsp; d) \(\frac{x}{3}=-2\)", r"Solve: a) \(x-8=3\) &nbsp; b) \(x+6=2\) &nbsp; c) \(5x=-35\) &nbsp; d) \(\frac{x}{3}=-2\)"),
       D(r"\text{a) }x=3+8=\boxed{11}\qquad \text{b) }x=2-6=\boxed{-4}\qquad \text{c) }x=\frac{-35}{5}=\boxed{-7}\qquad \text{d) }x=-2\cdot3=\boxed{-6}"))],
  [prob(L(r"Resol: \(2x+5=17\)", r"Resuelve: \(2x+5=17\)", r"Solve: \(2x+5=17\)"),
        chain(r"2x+5&=17", r"2x&=17-5", r"2x&=12", r"x&=\frac{12}{2}=\boxed{6}"),
        P(r"Comprovació: \(2\cdot6+5=17\ \checkmark\)", r"Comprobación: \(2\cdot6+5=17\ \checkmark\)", r"Check: \(2\cdot6+5=17\ \checkmark\)")),
   prob(L(r"Resol: \(8x-3=5x+12\)", r"Resuelve: \(8x-3=5x+12\)", r"Solve: \(8x-3=5x+12\)"),
        chain(r"8x-5x&=12+3", r"3x&=15", r"x&=\frac{15}{3}=\boxed{5}"),
        P(r"Comprovació: \(8\cdot5-3=37\) i \(5\cdot5+12=37\ \checkmark\)", r"Comprobación: \(8\cdot5-3=37\) y \(5\cdot5+12=37\ \checkmark\)", r"Check: \(8\cdot5-3=37\) and \(5\cdot5+12=37\ \checkmark\)"))],
  [prob(L(r"Resol: \(4-3x+2x=10+x\)", r"Resuelve: \(4-3x+2x=10+x\)", r"Solve: \(4-3x+2x=10+x\)"),
        P(r"Passem les \(x\) al primer membre i els nombres al segon:", r"Pasamos las \(x\) al primer miembro y los números al segundo:", r"Move the \(x\) terms to the left and the numbers to the right:"),
        chain(r"-3x+2x-x&=10-4", r"-2x&=6", r"x&=\frac{6}{-2}=\boxed{-3}"),
        P(r"Comprovació: \(4+9-6=7\) i \(10-3=7\ \checkmark\)", r"Comprobación: \(4+9-6=7\) y \(10-3=7\ \checkmark\)", r"Check: \(4+9-6=7\) and \(10-3=7\ \checkmark\)")),
   prob(L(r"Resol: \(6x+1=2x+3\)", r"Resuelve: \(6x+1=2x+3\)", r"Solve: \(6x+1=2x+3\)"),
        chain(r"6x-2x&=3-1", r"4x&=2", r"x&=\frac{2}{4}=\boxed{\frac{1}{2}}"),
        P(r"Comprovació: \(6\cdot\frac{1}{2}+1=4\) i \(2\cdot\frac{1}{2}+3=4\ \checkmark\)", r"Comprobación: \(6\cdot\frac{1}{2}+1=4\) y \(2\cdot\frac{1}{2}+3=4\ \checkmark\)", r"Check: \(6\cdot\frac{1}{2}+1=4\) and \(2\cdot\frac{1}{2}+3=4\ \checkmark\)"))])
for e, s in [('x-8=3', 11), ('x+6=2', -4), ('5x=-35', -7), ('x/3=-2', -6), ('2x+5=17', 6), ('8x-3=5x+12', 5), ('4-3x+2x=10+x', -3), ('6x+1=2x+3', sp.Rational(1, 2))]: ce(e, s)
s6 += practice([
  ('★', L(r"a) \(x+9=4\) &nbsp; b) \(7x=56\) &nbsp; c) \(\frac{x}{5}=6\)", r"a) \(x+9=4\) &nbsp; b) \(7x=56\) &nbsp; c) \(\frac{x}{5}=6\)", r"a) \(x+9=4\) &nbsp; b) \(7x=56\) &nbsp; c) \(\frac{x}{5}=6\)")),
  ('★★', L(r"d) \(3x-4=11\) &nbsp; e) \(9x+2=4x+22\) &nbsp; f) \(10-x=3x-6\)", r"d) \(3x-4=11\) &nbsp; e) \(9x+2=4x+22\) &nbsp; f) \(10-x=3x-6\)", r"d) \(3x-4=11\) &nbsp; e) \(9x+2=4x+22\) &nbsp; f) \(10-x=3x-6\)")),
  ('★★★', L(r"g) \(2x+7-5x=x-9\) &nbsp; h) \(5x-2=3x+1\)", r"g) \(2x+7-5x=x-9\) &nbsp; h) \(5x-2=3x+1\)", r"g) \(2x+7-5x=x-9\) &nbsp; h) \(5x-2=3x+1\)"))],
  P(r"a) \(x=-5\) &nbsp; b) \(x=8\) &nbsp; c) \(x=30\) &nbsp; d) \(3x=15,\ x=5\) &nbsp; e) \(5x=20,\ x=4\) &nbsp; f) \(-4x=-16,\ x=4\) &nbsp; g) \(-4x=-16,\ x=4\) &nbsp; h) \(2x=3,\ x=\frac{3}{2}\)", r"a) \(x=-5\) &nbsp; b) \(x=8\) &nbsp; c) \(x=30\) &nbsp; d) \(3x=15,\ x=5\) &nbsp; e) \(5x=20,\ x=4\) &nbsp; f) \(-4x=-16,\ x=4\) &nbsp; g) \(-4x=-16,\ x=4\) &nbsp; h) \(2x=3,\ x=\frac{3}{2}\)", r"a) \(x=-5\) &nbsp; b) \(x=8\) &nbsp; c) \(x=30\) &nbsp; d) \(3x=15,\ x=5\) &nbsp; e) \(5x=20,\ x=4\) &nbsp; f) \(-4x=-16,\ x=4\) &nbsp; g) \(-4x=-16,\ x=4\) &nbsp; h) \(2x=3,\ x=\frac{3}{2}\)"))
for e, s in [('x+9=4', -5), ('7x=56', 8), ('x/5=6', 30), ('3x-4=11', 5), ('9x+2=4x+22', 4), ('10-x=3x-6', 4), ('2x+7-5x=x-9', 4), ('5x-2=3x+1', sp.Rational(3, 2))]: ce(e, s)

# ============================================================ 6.7
s7 = box('prop', L('Equacions amb parèntesis', 'Ecuaciones con paréntesis', 'Equations with brackets'),
  P(r"Si l'equació té parèntesis, el primer pas és <strong>traure'ls</strong> amb la propietat distributiva (apartat 6.4). Després seguim el mètode general:",
    r"Si la ecuación tiene paréntesis, el primer paso es <strong>quitarlos</strong> con la propiedad distributiva (apartado 6.4). Después seguimos el método general:",
    r"If the equation has brackets, the first step is to <strong>remove them</strong> using the distributive property (section 6.4). Then follow the general method:")
  + ol(L("Traiem parèntesis.", "Quitamos paréntesis.", "Remove the brackets."), L("Transposem els termes.", "Transponemos los términos.", "Move the terms across."), L("Reduïm.", "Reducimos.", "Simplify."), L("Aïllem la \\(x\\).", "Despejamos la \\(x\\).", "Isolate \\(x\\)."), L("Comprovem.", "Comprobamos.", "Check."))
  + chain(r"3(x-2)&=x+4", r"3x-6&=x+4", r"3x-x&=4+6", r"2x&=10", r"x&=\frac{10}{2}=\boxed{5}")
  + P(r"Comprovació: \(3\cdot(5-2)=9\) i \(5+4=9\ \checkmark\)", r"Comprobación: \(3\cdot(5-2)=9\) y \(5+4=9\ \checkmark\)", r"Check: \(3\cdot(5-2)=9\) and \(5+4=9\ \checkmark\)")
  + note(r"Compte amb el <strong>signe menys</strong> davant d'un parèntesi: canvia el signe de tots els termes de dins. \(10-(x+3)=10-x-3\), i \(-2(x-4)=-2x+8\).",
         r"Cuidado con el <strong>signo menos</strong> delante de un paréntesis: cambia el signo de todos los términos de dentro. \(10-(x+3)=10-x-3\), y \(-2(x-4)=-2x+8\).",
         r"Watch out for a <strong>minus sign</strong> in front of brackets: it changes the sign of every term inside. \(10-(x+3)=10-x-3\), and \(-2(x-4)=-2x+8\).", '⚠️')
  + P(r"Un exemple amb dos parèntesis i un signe menys:", r"Un ejemplo con dos paréntesis y un signo menos:", r"An example with two sets of brackets and a minus sign:")
  + chain(r"4(x+1)-2(x-3)&=3x+5", r"4x+4-2x+6&=3x+5", r"4x-2x-3x&=5-4-6", r"-x&=-5", r"x&=\boxed{5}")
  + P(r"En l'últim pas, \(-x=-5\): multipliquem els dos membres per \(-1\) (canviem el signe als dos). Comprovació: \(4\cdot6-2\cdot2=20\) i \(3\cdot5+5=20\ \checkmark\)", r"En el último paso, \(-x=-5\): multiplicamos los dos miembros por \(-1\) (cambiamos el signo a los dos). Comprobación: \(4\cdot6-2\cdot2=20\) y \(3\cdot5+5=20\ \checkmark\)", r"In the last step, \(-x=-5\): multiply both sides by \(-1\) (change both signs). Check: \(4\cdot6-2\cdot2=20\) and \(3\cdot5+5=20\ \checkmark\)")
  + solver('w-solve2', '4(x+1)-2(x-3)=3x+5', [('3(x-2)=x+4', '3(x−2) = x+4'), ('4(x+1)-2(x-3)=3x+5', '4(x+1) − 2(x−3) = 3x+5'), ('10-(x+3)=2x+1', '10 − (x+3) = 2x+1'), ('5(2x-1)=3(x+4)', '5(2x−1) = 3(x+4)'), ('2(x+3)=2x+6', '2(x+3) = 2x+6')])
  + drill('eq2', 'Entrena: equacions amb parèntesis', 'Entrena: ecuaciones con paréntesis', 'Train: equations with brackets'))
ce('3(x-2)=x+4', 5); ce('4(x+1)-2(x-3)=3x+5', 5); ce('10-(x+3)=2x+1', 2); ce('5(2x-1)=3(x+4)', sp.Rational(17, 7))
s7 += levels([
  prob(L(r"Resol: \(2(x+3)=14\)", r"Resuelve: \(2(x+3)=14\)", r"Solve: \(2(x+3)=14\)"),
       chain(r"2x+6&=14", r"2x&=14-6=8", r"x&=\frac{8}{2}=\boxed{4}"),
       note(r"També es podria dividir primer entre 2: \(x+3=7\Rightarrow x=4\).", r"También se podría dividir primero entre 2: \(x+3=7\Rightarrow x=4\).", r"You could also divide by 2 first: \(x+3=7\Rightarrow x=4\)."))],
  [prob(L(r"Resol: \(5(x-1)=3(x+1)\)", r"Resuelve: \(5(x-1)=3(x+1)\)", r"Solve: \(5(x-1)=3(x+1)\)"),
        chain(r"5x-5&=3x+3", r"5x-3x&=3+5", r"2x&=8", r"x&=\boxed{4}"),
        P(r"Comprovació: \(5\cdot3=15\) i \(3\cdot5=15\ \checkmark\)", r"Comprobación: \(5\cdot3=15\) y \(3\cdot5=15\ \checkmark\)", r"Check: \(5\cdot3=15\) and \(3\cdot5=15\ \checkmark\)")),
   prob(L(r"Resol: \(10-(x+3)=2x+1\)", r"Resuelve: \(10-(x+3)=2x+1\)", r"Solve: \(10-(x+3)=2x+1\)"),
        chain(r"10-x-3&=2x+1", r"-x-2x&=1-10+3", r"-3x&=-6", r"x&=\frac{-6}{-3}=\boxed{2}"),
        P(r"Comprovació: \(10-5=5\) i \(2\cdot2+1=5\ \checkmark\)", r"Comprobación: \(10-5=5\) y \(2\cdot2+1=5\ \checkmark\)", r"Check: \(10-5=5\) and \(2\cdot2+1=5\ \checkmark\)"))],
  [prob(L(r"Resol: \(3(2x-1)-4(x-2)=x+9\)", r"Resuelve: \(3(2x-1)-4(x-2)=x+9\)", r"Solve: \(3(2x-1)-4(x-2)=x+9\)"),
        chain(r"6x-3-4x+8&=x+9", r"6x-4x-x&=9+3-8", r"x&=\boxed{4}"),
        P(r"Comprovació: \(3\cdot7-4\cdot2=13\) i \(4+9=13\ \checkmark\)", r"Comprobación: \(3\cdot7-4\cdot2=13\) y \(4+9=13\ \checkmark\)", r"Check: \(3\cdot7-4\cdot2=13\) and \(4+9=13\ \checkmark\)")),
   prob(L(r"Resol: \(2(x+4)-x=x+8\). Què passa?", r"Resuelve: \(2(x+4)-x=x+8\). ¿Qué pasa?", r"Solve: \(2(x+4)-x=x+8\). What happens?"),
        chain(r"2x+8-x&=x+8", r"2x-x-x&=8-8", r"0x&=0"),
        P(r"Qualsevol nombre multiplicat per 0 dona 0: <strong>tots els nombres són solució</strong>. No és una equació, és una <strong>identitat</strong> (els dos membres són iguals, \(x+8\)).", r"Cualquier número multiplicado por 0 da 0: <strong>todos los números son solución</strong>. No es una ecuación, es una <strong>identidad</strong> (los dos miembros son iguales, \(x+8\)).", r"Any number times 0 gives 0: <strong>every number is a solution</strong>. It isn't an equation, it's an <strong>identity</strong> (both sides are the same, \(x+8\))."))])
for e, s in [('2(x+3)=14', 4), ('5(x-1)=3(x+1)', 4), ('3(2x-1)-4(x-2)=x+9', 4)]: ce(e, s)
chk('2(x+4)-x', 'x+8')
s7 += practice([
  ('★', L(r"a) \(4(x-2)=12\) &nbsp; b) \(3(x+5)=x+19\)", r"a) \(4(x-2)=12\) &nbsp; b) \(3(x+5)=x+19\)", r"a) \(4(x-2)=12\) &nbsp; b) \(3(x+5)=x+19\)")),
  ('★★', L(r"c) \(7x-(2x+6)=9\) &nbsp; d) \(2(3x-1)=4(x+2)\)", r"c) \(7x-(2x+6)=9\) &nbsp; d) \(2(3x-1)=4(x+2)\)", r"c) \(7x-(2x+6)=9\) &nbsp; d) \(2(3x-1)=4(x+2)\)")),
  ('★★★', L(r"e) \(5-2(x+1)=3(x-4)\) &nbsp; f) \(6(x-1)-2(2x+1)=3-x\)", r"e) \(5-2(x+1)=3(x-4)\) &nbsp; f) \(6(x-1)-2(2x+1)=3-x\)", r"e) \(5-2(x+1)=3(x-4)\) &nbsp; f) \(6(x-1)-2(2x+1)=3-x\)"))],
  P(r"a) \(4x-8=12,\ x=5\) &nbsp; b) \(3x+15=x+19,\ x=2\) &nbsp; c) \(5x-6=9,\ x=3\) &nbsp; d) \(6x-2=4x+8,\ x=5\)", r"a) \(4x-8=12,\ x=5\) &nbsp; b) \(3x+15=x+19,\ x=2\) &nbsp; c) \(5x-6=9,\ x=3\) &nbsp; d) \(6x-2=4x+8,\ x=5\)", r"a) \(4x-8=12,\ x=5\) &nbsp; b) \(3x+15=x+19,\ x=2\) &nbsp; c) \(5x-6=9,\ x=3\) &nbsp; d) \(6x-2=4x+8,\ x=5\)")
  + P(r"e) \(3-2x=3x-12,\ -5x=-15,\ x=3\) &nbsp; f) \(2x-8=3-x,\ 3x=11,\ x=\frac{11}{3}\)", r"e) \(3-2x=3x-12,\ -5x=-15,\ x=3\) &nbsp; f) \(2x-8=3-x,\ 3x=11,\ x=\frac{11}{3}\)", r"e) \(3-2x=3x-12,\ -5x=-15,\ x=3\) &nbsp; f) \(2x-8=3-x,\ 3x=11,\ x=\frac{11}{3}\)"))
for e, s in [('4(x-2)=12', 5), ('3(x+5)=x+19', 2), ('7x-(2x+6)=9', 3), ('2(3x-1)=4(x+2)', 5), ('5-2(x+1)=3(x-4)', 3), ('6(x-1)-2(2x+1)=3-x', sp.Rational(11, 3))]: ce(e, s)
chk('6(x-1)-2(2x+1)', '2x-8')

# ============================================================ 6.8
s8 = box('prop', L('Equacions amb denominadors', 'Ecuaciones con denominadores', 'Equations with fractions'),
  P(r"Si hi ha fraccions, primer les <strong>eliminem</strong>: multipliquem <strong>tots</strong> els termes dels dos membres pel <strong>m.c.m. dels denominadors</strong> (unitats 2 i 4). Així obtenim una equació equivalent sense denominadors.",
    r"Si hay fracciones, primero las <strong>eliminamos</strong>: multiplicamos <strong>todos</strong> los términos de los dos miembros por el <strong>m.c.m. de los denominadores</strong> (unidades 2 y 4). Así obtenemos una ecuación equivalente sin denominadores.",
    r"If there are fractions, we <strong>clear</strong> them first: multiply <strong>every</strong> term on both sides by the <strong>LCM of the denominators</strong> (units 2 and 4). This gives an equivalent equation with no denominators.")
  + D(r"\frac{x}{2}+\frac{x}{3}=5\qquad \text{m.c.m.}(2,3)=6")
  + chain(r"6\cdot\frac{x}{2}+6\cdot\frac{x}{3}&=6\cdot5", r"3x+2x&=30", r"5x&=30", r"x&=\frac{30}{5}=\boxed{6}")
  + P(r"Truc: dividim el m.c.m. entre cada denominador i el resultat multiplica el numerador (\(6:2=3\), \(6:3=2\)). Comprovació: \(\frac{6}{2}+\frac{6}{3}=3+2=5\ \checkmark\)", r"Truco: dividimos el m.c.m. entre cada denominador y el resultado multiplica al numerador (\(6:2=3\), \(6:3=2\)). Comprobación: \(\frac{6}{2}+\frac{6}{3}=3+2=5\ \checkmark\)", r"Tip: divide the LCM by each denominator and multiply the numerator by the result (\(6:2=3\), \(6:3=2\)). Check: \(\frac{6}{2}+\frac{6}{3}=3+2=5\ \checkmark\)")
  + note(r"Els termes <strong>sense denominador</strong> també es multipliquen pel m.c.m.: en \(\frac{x}{4}+1=3\) queda \(x+4=12\), no \(x+1=12\).",
         r"Los términos <strong>sin denominador</strong> también se multiplican por el m.c.m.: en \(\frac{x}{4}+1=3\) queda \(x+4=12\), no \(x+1=12\).",
         r"Terms <strong>without a denominator</strong> are multiplied by the LCM too: \(\frac{x}{4}+1=3\) becomes \(x+4=12\), not \(x+1=12\).", '⚠️')
  + P(r"Si un numerador té <strong>més d'un terme</strong>, en multiplicar el posem entre parèntesis. Sobretot si davant de la fracció hi ha un signe menys!", r"Si un numerador tiene <strong>más de un término</strong>, al multiplicar lo ponemos entre paréntesis. ¡Sobre todo si delante de la fracción hay un signo menos!", r"If a numerator has <strong>more than one term</strong>, put it in brackets when multiplying. Especially if there's a minus sign in front of the fraction!")
  + D(r"\frac{x+1}{2}-\frac{x-2}{3}=2\qquad \text{m.c.m.}(2,3)=6")
  + chain(r"3(x+1)-2(x-2)&=12", r"3x+3-2x+4&=12", r"3x-2x&=12-3-4", r"x&=\boxed{5}")
  + P(r"Comprovació: \(\frac{6}{2}-\frac{3}{3}=3-1=2\ \checkmark\)", r"Comprobación: \(\frac{6}{2}-\frac{3}{3}=3-1=2\ \checkmark\)", r"Check: \(\frac{6}{2}-\frac{3}{3}=3-1=2\ \checkmark\)")
  + solver('w-solve3', '(x+1)/2-(x-2)/3=2', [('x/2+x/3=5', 'x/2 + x/3 = 5'), ('x/4+1=3', 'x/4 + 1 = 3'), ('(x+1)/2-(x-2)/3=2', '(x+1)/2 − (x−2)/3 = 2'), ('x-(x-1)/4=7', 'x − (x−1)/4 = 7'), ('(2x-1)/3=x/2', '(2x−1)/3 = x/2')])
  + drill('eq3', 'Entrena: equacions amb denominadors', 'Entrena: ecuaciones con denominadores', 'Train: equations with fractions'))
for e, s in [('x/2+x/3=5', 6), ('x/4+1=3', 8), ('(x+1)/2-(x-2)/3=2', 5), ('x-(x-1)/4=7', 9), ('(2x-1)/3=x/2', 2)]: ce(e, s)
s8 += levels([
  prob(L(r"Resol: \(\frac{x}{3}+2=6\)", r"Resuelve: \(\frac{x}{3}+2=6\)", r"Solve: \(\frac{x}{3}+2=6\)"),
       P(r"Multipliquem tots els termes per 3:", r"Multiplicamos todos los términos por 3:", r"Multiply every term by 3:"),
       chain(r"x+6&=18", r"x&=18-6=\boxed{12}"),
       note(r"També es pot fer transposant: \(\frac{x}{3}=6-2=4\Rightarrow x=4\cdot3=12\).", r"También se puede hacer transponiendo: \(\frac{x}{3}=6-2=4\Rightarrow x=4\cdot3=12\).", r"You can also move terms across: \(\frac{x}{3}=6-2=4\Rightarrow x=4\cdot3=12\)."))],
  [prob(L(r"Resol: \(\frac{x}{2}-\frac{x}{5}=3\)", r"Resuelve: \(\frac{x}{2}-\frac{x}{5}=3\)", r"Solve: \(\frac{x}{2}-\frac{x}{5}=3\)"),
        P(r"\(\text{m.c.m.}(2,5)=10\):", r"\(\text{m.c.m.}(2,5)=10\):", r"\(\text{LCM}(2,5)=10\):"),
        chain(r"5x-2x&=30", r"3x&=30", r"x&=\boxed{10}"),
        P(r"Comprovació: \(5-2=3\ \checkmark\)", r"Comprobación: \(5-2=3\ \checkmark\)", r"Check: \(5-2=3\ \checkmark\)")),
   prob(L(r"Resol: \(\frac{x+3}{4}=\frac{x}{2}\)", r"Resuelve: \(\frac{x+3}{4}=\frac{x}{2}\)", r"Solve: \(\frac{x+3}{4}=\frac{x}{2}\)"),
        P(r"\(\text{m.c.m.}(4,2)=4\):", r"\(\text{m.c.m.}(4,2)=4\):", r"\(\text{LCM}(4,2)=4\):"),
        chain(r"x+3&=2x", r"x-2x&=-3", r"-x&=-3", r"x&=\boxed{3}"),
        P(r"Comprovació: \(\frac{6}{4}=\frac{3}{2}\ \checkmark\)", r"Comprobación: \(\frac{6}{4}=\frac{3}{2}\ \checkmark\)", r"Check: \(\frac{6}{4}=\frac{3}{2}\ \checkmark\)"))],
  [prob(L(r"Resol: \(x-\frac{x-1}{4}=7\)", r"Resuelve: \(x-\frac{x-1}{4}=7\)", r"Solve: \(x-\frac{x-1}{4}=7\)"),
        P(r"Multipliquem per 4 i posem el numerador \(x-1\) entre parèntesis, perquè el signe menys afecta tots dos termes:", r"Multiplicamos por 4 y ponemos el numerador \(x-1\) entre paréntesis, porque el signo menos afecta a los dos términos:", r"Multiply by 4 and put the numerator \(x-1\) in brackets, because the minus sign affects both terms:"),
        chain(r"4x-(x-1)&=28", r"4x-x+1&=28", r"3x&=27", r"x&=\boxed{9}"),
        P(r"Comprovació: \(9-\frac{8}{4}=9-2=7\ \checkmark\)", r"Comprobación: \(9-\frac{8}{4}=9-2=7\ \checkmark\)", r"Check: \(9-\frac{8}{4}=9-2=7\ \checkmark\)")),
   prob(L(r"Resol: \(\frac{x}{2}+\frac{x}{3}+\frac{x}{6}=x-1\). Què passa?", r"Resuelve: \(\frac{x}{2}+\frac{x}{3}+\frac{x}{6}=x-1\). ¿Qué pasa?", r"Solve: \(\frac{x}{2}+\frac{x}{3}+\frac{x}{6}=x-1\). What happens?"),
        chain(r"3x+2x+x&=6x-6", r"6x-6x&=-6", r"0x&=-6"),
        P(r"Cap nombre multiplicat per 0 dona \(-6\): l'equació <strong>no té solució</strong>. (La meitat més la tercera part més la sisena part d'un nombre sempre és el nombre sencer, i mai pot ser el nombre menys 1.)", r"Ningún número multiplicado por 0 da \(-6\): la ecuación <strong>no tiene solución</strong>. (La mitad más un tercio más un sexto de un número siempre es el número entero, y nunca puede ser el número menos 1.)", r"No number times 0 gives \(-6\): the equation has <strong>no solution</strong>. (Half plus a third plus a sixth of a number is always the whole number, so it can never equal the number minus 1.)"))])
for e, s in [('x/3+2=6', 12), ('x/2-x/5=3', 10), ('(x+3)/4=x/2', 3)]: ce(e, s)
chk('x/2+x/3+x/6', 'x')
s8 += practice([
  ('★', L(r"a) \(\frac{x}{5}=4\) &nbsp; b) \(\frac{x}{2}+3=7\)", r"a) \(\frac{x}{5}=4\) &nbsp; b) \(\frac{x}{2}+3=7\)", r"a) \(\frac{x}{5}=4\) &nbsp; b) \(\frac{x}{2}+3=7\)")),
  ('★★', L(r"c) \(\frac{x}{3}+\frac{x}{6}=3\) &nbsp; d) \(\frac{x-2}{3}=\frac{x}{4}\)", r"c) \(\frac{x}{3}+\frac{x}{6}=3\) &nbsp; d) \(\frac{x-2}{3}=\frac{x}{4}\)", r"c) \(\frac{x}{3}+\frac{x}{6}=3\) &nbsp; d) \(\frac{x-2}{3}=\frac{x}{4}\)")),
  ('★★★', L(r"e) \(\frac{x+4}{2}-\frac{x-1}{3}=4\) &nbsp; f) \(\frac{2x}{5}-1=\frac{x}{2}-2\)", r"e) \(\frac{x+4}{2}-\frac{x-1}{3}=4\) &nbsp; f) \(\frac{2x}{5}-1=\frac{x}{2}-2\)", r"e) \(\frac{x+4}{2}-\frac{x-1}{3}=4\) &nbsp; f) \(\frac{2x}{5}-1=\frac{x}{2}-2\)"))],
  P(r"a) \(x=20\) &nbsp; b) \(x+6=14,\ x=8\) &nbsp; c) \(2x+x=18,\ x=6\) &nbsp; d) \(4(x-2)=3x,\ x=8\)", r"a) \(x=20\) &nbsp; b) \(x+6=14,\ x=8\) &nbsp; c) \(2x+x=18,\ x=6\) &nbsp; d) \(4(x-2)=3x,\ x=8\)", r"a) \(x=20\) &nbsp; b) \(x+6=14,\ x=8\) &nbsp; c) \(2x+x=18,\ x=6\) &nbsp; d) \(4(x-2)=3x,\ x=8\)")
  + P(r"e) \(3(x+4)-2(x-1)=24,\ x+14=24,\ x=10\) &nbsp; f) \(4x-10=5x-20,\ -x=-10,\ x=10\)", r"e) \(3(x+4)-2(x-1)=24,\ x+14=24,\ x=10\) &nbsp; f) \(4x-10=5x-20,\ -x=-10,\ x=10\)", r"e) \(3(x+4)-2(x-1)=24,\ x+14=24,\ x=10\) &nbsp; f) \(4x-10=5x-20,\ -x=-10,\ x=10\)"))
for e, s in [('x/5=4', 20), ('x/2+3=7', 8), ('x/3+x/6=3', 6), ('(x-2)/3=x/4', 8), ('(x+4)/2-(x-1)/3=4', 10), ('2x/5-1=x/2-2', 10)]: ce(e, s)
chk('3(x+4)-2(x-1)', 'x+14')

# ============================================================ 6.9
s9 = box('prop', L('Com resoldre un problema amb una equació', 'Cómo resolver un problema con una ecuación', 'How to solve a problem with an equation'),
  ol(L(r"<strong>Llegim</strong> bé l'enunciat i pensem què ens pregunten.", r"<strong>Leemos</strong> bien el enunciado y pensamos qué nos preguntan.", r"<strong>Read</strong> the problem carefully and work out what is being asked."),
     L(r"<strong>Triem la incògnita:</strong> diem què és \(x\) i expressem les altres quantitats amb \(x\).", r"<strong>Elegimos la incógnita:</strong> decimos qué es \(x\) y expresamos las demás cantidades con \(x\).", r"<strong>Choose the unknown:</strong> say what \(x\) is and write the other amounts using \(x\)."),
     L(r"<strong>Plantegem</strong> l'equació: traduïm l'enunciat al llenguatge algebraic.", r"<strong>Planteamos</strong> la ecuación: traducimos el enunciado al lenguaje algebraico.", r"<strong>Set up</strong> the equation: translate the statement into algebra."),
     L(r"<strong>Resolem</strong> l'equació.", r"<strong>Resolvemos</strong> la ecuación.", r"<strong>Solve</strong> the equation."),
     L(r"<strong>Comprovem</strong> que la solució té sentit i compleix l'enunciat, i <strong>responem</strong> la pregunta amb una frase.", r"<strong>Comprobamos</strong> que la solución tiene sentido y cumple el enunciado, y <strong>respondemos</strong> la pregunta con una frase.", r"<strong>Check</strong> that the solution makes sense and fits the problem, and <strong>answer</strong> the question in a sentence."))
  + P(r"<strong>Exemple.</strong> Si al triple d'un nombre li restem 7, obtenim 20. Quin és el nombre?", r"<strong>Ejemplo.</strong> Si al triple de un número le restamos 7, obtenemos 20. ¿Cuál es el número?", r"<strong>Example.</strong> If we subtract 7 from three times a number, we get 20. What is the number?")
  + P(r"Incògnita: \(x=\) el nombre. Equació i resolució:", r"Incógnita: \(x=\) el número. Ecuación y resolución:", r"Unknown: \(x=\) the number. Equation and solution:")
  + chain(r"3x-7&=20", r"3x&=27", r"x&=\boxed{9}")
  + P(r"Comprovació: \(3\cdot9-7=27-7=20\ \checkmark\). El nombre és el 9.", r"Comprobación: \(3\cdot9-7=27-7=20\ \checkmark\). El número es el 9.", r"Check: \(3\cdot9-7=27-7=20\ \checkmark\). The number is 9.")
  + note(r"Comprovem sempre si la solució <strong>té sentit</strong>: si busquem un nombre de persones i ens ix \(x=7\dc5\) o \(x=-3\), alguna cosa està malament (o el problema no té solució).",
         r"Comprobamos siempre si la solución <strong>tiene sentido</strong>: si buscamos un número de personas y nos sale \(x=7\dc5\) o \(x=-3\), algo está mal (o el problema no tiene solución).",
         r"Always check that the solution <strong>makes sense</strong>: if we're looking for a number of people and get \(x=7\dc5\) or \(x=-3\), something is wrong (or the problem has no solution).")
  + widget('w-plan', '📝', L('Planteja i resol', 'Plantea y resuelve', 'Set up and solve'),
           ['<div class="wrow">' + seg([('c', L('Consecutius', 'Consecutivos', 'Consecutive')), ('e', L('Edats', 'Edades', 'Ages')), ('r', L('Rectangle', 'Rectángulo', 'Rectangle')), ('d', L('Repartiment', 'Reparto', 'Sharing'))], 'c') + '</div>',
            '<p class="pq"></p>',
            '<div class="wrow">' + '<label><span class="pl" data-p="p"></span> <input class="tin s" type="text" inputmode="numeric" data-k="p" value="84" autocomplete="off" aria-label="p"></label>'
            + '<label><span class="pl" data-p="q"></span> <input class="tin s" type="text" inputmode="numeric" data-k="q" value="" autocomplete="off" aria-label="q"></label></div>'])
  + drill('prob', 'Entrena: problemes', 'Entrena: problemas', 'Train: word problems'))
ce('3x-7=20', 9)
s9 += levels([
  prob(L(r"La suma d'un nombre i el seu doble és 45. Quin és el nombre?", r"La suma de un número y su doble es 45. ¿Cuál es el número?", r"A number plus twice the number makes 45. What is the number?"),
       P(r"\(x=\) el nombre; el seu doble, \(2x\).", r"\(x=\) el número; su doble, \(2x\).", r"\(x=\) the number; twice it, \(2x\)."),
       chain(r"x+2x&=45", r"3x&=45", r"x&=\boxed{15}"),
       P(r"Comprovació: \(15+30=45\ \checkmark\). El nombre és el 15.", r"Comprobación: \(15+30=45\ \checkmark\). El número es el 15.", r"Check: \(15+30=45\ \checkmark\). The number is 15.")),
  prob(L(r"Tres nombres consecutius sumen 84. Quins són?", r"Tres números consecutivos suman 84. ¿Cuáles son?", r"Three consecutive numbers add up to 84. What are they?"),
       P(r"\(x=\) el menor; els altres són \(x+1\) i \(x+2\).", r"\(x=\) el menor; los otros son \(x+1\) y \(x+2\).", r"\(x=\) the smallest; the others are \(x+1\) and \(x+2\)."),
       chain(r"x+(x+1)+(x+2)&=84", r"3x+3&=84", r"3x&=81", r"x&=27"),
       P(r"Els nombres són \(\boxed{27,\ 28\ \text{i}\ 29}\). Comprovació: \(27+28+29=84\ \checkmark\)", r"Los números son \(\boxed{27,\ 28\ \text{y}\ 29}\). Comprobación: \(27+28+29=84\ \checkmark\)", r"The numbers are \(\boxed{27,\ 28\ \text{and}\ 29}\). Check: \(27+28+29=84\ \checkmark\)"))],
  [prob(L(r"Una mare té 38 anys i la seua filla, 8. D'ací a quants anys l'edat de la mare serà el triple que la de la filla?", r"Una madre tiene 38 años y su hija, 8. ¿Dentro de cuántos años la edad de la madre será el triple que la de la hija?", r"A mother is 38 and her daughter is 8. In how many years will the mother be three times as old as her daughter?"),
        P(r"\(x=\) anys que han de passar. Aleshores la mare tindrà \(38+x\) anys i la filla, \(8+x\).", r"\(x=\) años que tienen que pasar. Entonces la madre tendrá \(38+x\) años y la hija, \(8+x\).", r"\(x=\) the number of years. By then the mother will be \(38+x\) and the daughter \(8+x\)."),
        chain(r"38+x&=3(8+x)", r"38+x&=24+3x", r"x-3x&=24-38", r"-2x&=-14", r"x&=\boxed{7}"),
        P(r"D'ací a 7 anys: la mare en tindrà 45 i la filla 15, i \(45=3\cdot15\ \checkmark\)", r"Dentro de 7 años: la madre tendrá 45 y la hija 15, y \(45=3\cdot15\ \checkmark\)", r"In 7 years: the mother will be 45 and the daughter 15, and \(45=3\cdot15\ \checkmark\)")),
   prob(L(r"Repartim 130 € entre tres germans. El segon rep el doble que el primer i el tercer, 10 € més que el primer. Quant rep cadascun?", r"Repartimos 130 € entre tres hermanos. El segundo recibe el doble que el primero y el tercero, 10 € más que el primero. ¿Cuánto recibe cada uno?", r"We share 130 € among three siblings. The second gets twice as much as the first, and the third gets 10 € more than the first. How much does each get?"),
        P(r"\(x=\) el que rep el primer; el segon, \(2x\); el tercer, \(x+10\).", r"\(x=\) lo que recibe el primero; el segundo, \(2x\); el tercero, \(x+10\).", r"\(x=\) what the first gets; the second, \(2x\); the third, \(x+10\)."),
        chain(r"x+2x+(x+10)&=130", r"4x+10&=130", r"4x&=120", r"x&=30"),
        P(r"El primer rep \(\boxed{30\ €}\), el segon \(\boxed{60\ €}\) i el tercer \(\boxed{40\ €}\). Comprovació: \(30+60+40=130\ \checkmark\)", r"El primero recibe \(\boxed{30\ €}\), el segundo \(\boxed{60\ €}\) y el tercero \(\boxed{40\ €}\). Comprobación: \(30+60+40=130\ \checkmark\)", r"The first gets \(\boxed{30\ €}\), the second \(\boxed{60\ €}\) and the third \(\boxed{40\ €}\). Check: \(30+60+40=130\ \checkmark\)"))],
  [prob(L(r"El perímetre d'un rectangle és 54 cm i la base fa el doble que l'altura. Quant mesuren la base i l'altura?", r"El perímetro de un rectángulo es 54 cm y la base mide el doble que la altura. ¿Cuánto miden la base y la altura?", r"A rectangle has a perimeter of 54 cm and its base is twice its height. How long are the base and the height?"),
        P(r"\(x=\) l'altura; la base és \(2x\). El perímetre és la suma dels quatre costats:", r"\(x=\) la altura; la base es \(2x\). El perímetro es la suma de los cuatro lados:", r"\(x=\) the height; the base is \(2x\). The perimeter is the sum of the four sides:"),
        chain(r"2x+x+2x+x&=54", r"6x&=54", r"x&=9"),
        P(r"Altura \(\boxed{9\ \text{cm}}\) i base \(\boxed{18\ \text{cm}}\). Comprovació: \(18+9+18+9=54\ \checkmark\)", r"Altura \(\boxed{9\ \text{cm}}\) y base \(\boxed{18\ \text{cm}}\). Comprobación: \(18+9+18+9=54\ \checkmark\)", r"Height \(\boxed{9\ \text{cm}}\) and base \(\boxed{18\ \text{cm}}\). Check: \(18+9+18+9=54\ \checkmark\)")),
   prob(L(r"En una granja hi ha gallines i conills. En total hi ha 40 caps i 100 potes. Quantes gallines i quants conills hi ha?", r"En una granja hay gallinas y conejos. En total hay 40 cabezas y 100 patas. ¿Cuántas gallinas y cuántos conejos hay?", r"A farm has hens and rabbits. Altogether there are 40 heads and 100 legs. How many hens and how many rabbits are there?"),
        P(r"\(x=\) nombre de gallines; com que hi ha 40 caps, els conills són \(40-x\). Les gallines tenen 2 potes i els conills, 4:", r"\(x=\) número de gallinas; como hay 40 cabezas, los conejos son \(40-x\). Las gallinas tienen 2 patas y los conejos, 4:", r"\(x=\) number of hens; since there are 40 heads, there are \(40-x\) rabbits. Hens have 2 legs and rabbits 4:"),
        chain(r"2x+4(40-x)&=100", r"2x+160-4x&=100", r"-2x&=-60", r"x&=30"),
        P(r"Hi ha \(\boxed{30\ \text{gallines}}\) i \(\boxed{10\ \text{conills}}\). Comprovació: \(30\cdot2+10\cdot4=60+40=100\ \checkmark\)", r"Hay \(\boxed{30\ \text{gallinas}}\) y \(\boxed{10\ \text{conejos}}\). Comprobación: \(30\cdot2+10\cdot4=60+40=100\ \checkmark\)", r"There are \(\boxed{30\ \text{hens}}\) and \(\boxed{10\ \text{rabbits}}\). Check: \(30\cdot2+10\cdot4=60+40=100\ \checkmark\)"))])
for e, s in [('x+2x=45', 15), ('x+(x+1)+(x+2)=84', 27), ('38+x=3(8+x)', 7), ('x+2x+(x+10)=130', 30), ('2x+x+2x+x=54', 9), ('2x+4(40-x)=100', 30)]: ce(e, s)
s9 += practice([
  ('★', L(r"a) Si a un nombre li sumem 15 obtenim el doble del nombre. Quin és? b) Dos nombres consecutius sumen 51. Quins són?", r"a) Si a un número le sumamos 15 obtenemos el doble del número. ¿Cuál es? b) Dos números consecutivos suman 51. ¿Cuáles son?", r"a) Adding 15 to a number gives twice the number. What is it? b) Two consecutive numbers add up to 51. What are they?")),
  ('★★', L(r"c) La Laia té 3 anys més que el seu germà i entre els dos en sumen 27. Quants anys té cadascun? d) Un bolígraf costa 2 € més que un llapis. Per 3 bolígrafs i 2 llapis paguem 16 €. Quant costa cada cosa?", r"c) Laia tiene 3 años más que su hermano y entre los dos suman 27. ¿Cuántos años tiene cada uno? d) Un bolígrafo cuesta 2 € más que un lápiz. Por 3 bolígrafos y 2 lápices pagamos 16 €. ¿Cuánto cuesta cada cosa?", r"c) Laia is 3 years older than her brother and together they are 27. How old is each? d) A pen costs 2 € more than a pencil. 3 pens and 2 pencils cost 16 €. How much does each cost?")),
  ('★★★', L(r"e) La meitat d'un nombre més la seua tercera part és 15. Quin és el nombre? f) Un pare té 40 anys i el seu fill, 12. Quants anys fa que l'edat del pare era el quíntuple que la del fill?", r"e) La mitad de un número más su tercera parte es 15. ¿Cuál es el número? f) Un padre tiene 40 años y su hijo, 12. ¿Cuántos años hace que la edad del padre era el quíntuple que la del hijo?", r"e) Half a number plus a third of it is 15. What is the number? f) A father is 40 and his son is 12. How many years ago was the father five times as old as his son?"))],
  P(r"a) \(x+15=2x\Rightarrow x=15\). &nbsp; b) \(x+(x+1)=51\Rightarrow x=25\): 25 i 26. &nbsp; c) \(x+(x+3)=27\Rightarrow x=12\): el germà 12 anys i la Laia 15. &nbsp; d) Llapis \(x\): \(3(x+2)+2x=16\Rightarrow 5x=10\Rightarrow x=2\): llapis 2 € i bolígraf 4 €.", r"a) \(x+15=2x\Rightarrow x=15\). &nbsp; b) \(x+(x+1)=51\Rightarrow x=25\): 25 y 26. &nbsp; c) \(x+(x+3)=27\Rightarrow x=12\): el hermano 12 años y Laia 15. &nbsp; d) Lápiz \(x\): \(3(x+2)+2x=16\Rightarrow 5x=10\Rightarrow x=2\): lápiz 2 € y bolígrafo 4 €.", r"a) \(x+15=2x\Rightarrow x=15\). &nbsp; b) \(x+(x+1)=51\Rightarrow x=25\): 25 and 26. &nbsp; c) \(x+(x+3)=27\Rightarrow x=12\): her brother is 12 and Laia 15. &nbsp; d) Pencil \(x\): \(3(x+2)+2x=16\Rightarrow 5x=10\Rightarrow x=2\): pencil 2 € and pen 4 €.")
  + P(r"e) \(\frac{x}{2}+\frac{x}{3}=15\Rightarrow 3x+2x=90\Rightarrow x=18\). &nbsp; f) Fa \(x\) anys: \(40-x=5(12-x)\Rightarrow 40-x=60-5x\Rightarrow 4x=20\Rightarrow x=5\). Fa 5 anys (35 i 7).", r"e) \(\frac{x}{2}+\frac{x}{3}=15\Rightarrow 3x+2x=90\Rightarrow x=18\). &nbsp; f) Hace \(x\) años: \(40-x=5(12-x)\Rightarrow 40-x=60-5x\Rightarrow 4x=20\Rightarrow x=5\). Hace 5 años (35 y 7).", r"e) \(\frac{x}{2}+\frac{x}{3}=15\Rightarrow 3x+2x=90\Rightarrow x=18\). &nbsp; f) \(x\) years ago: \(40-x=5(12-x)\Rightarrow 40-x=60-5x\Rightarrow 4x=20\Rightarrow x=5\). 5 years ago (35 and 7)."))
for e, s in [('x+15=2x', 15), ('x+(x+1)=51', 25), ('x+(x+3)=27', 12), ('3(x+2)+2x=16', 2), ('x/2+x/3=15', 18), ('40-x=5(12-x)', 5)]: ce(e, s)
