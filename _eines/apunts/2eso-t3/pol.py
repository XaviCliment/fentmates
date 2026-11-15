# Apartats 3.4-3.8 dels apunts de la Unitat 3 de 2n ESO: polinomis, suma i resta, producte, identitats notables i factor comú.
# Els resultats escrits a mà es comproven amb chk() (sympy).
from comu import *

# =====================================================================
# 3.4 Polinomis: parts
# =====================================================================
s4 = box('def', L('Què és un polinomi?', '¿Qué es un polinomio?', 'What is a polynomial?'),
  P(r"Un <strong>polinomi</strong> és una <strong>suma de monomis</strong> no semblants. Cada monomi és un <strong>terme</strong> del polinomi. Si té dos termes és un <strong>binomi</strong> i si en té tres, un <strong>trinomi</strong>. Els polinomis s'anomenen amb una lletra majúscula i la variable entre parèntesis: \(P(x)\), \(Q(x)\)…",
    r"Un <strong>polinomio</strong> es una <strong>suma de monomios</strong> no semejantes. Cada monomio es un <strong>término</strong> del polinomio. Si tiene dos términos es un <strong>binomio</strong> y si tiene tres, un <strong>trinomio</strong>. Los polinomios se nombran con una letra mayúscula y la variable entre paréntesis: \(P(x)\), \(Q(x)\)…",
    r"A <strong>polynomial</strong> is a <strong>sum of unlike monomials</strong>. Each monomial is a <strong>term</strong> of the polynomial. With two terms it's a <strong>binomial</strong> and with three, a <strong>trinomial</strong>. Polynomials are named with a capital letter and the variable in brackets: \(P(x)\), \(Q(x)\)…")
  + D(r"P(x)=\underbrace{4x^3}_{\tri{grau 3}{grado 3}{degree 3}}\ \underbrace{-\,2x^2}_{\tri{grau 2}{grado 2}{degree 2}}\ \underbrace{+\,x}_{\tri{grau 1}{grado 1}{degree 1}}\ \underbrace{-\,7}_{\tri{terme indep.}{término indep.}{constant}}")
  + P("Les seues parts són:", "Sus partes son:", "Its parts are:")
  + ul(L(r"El <strong>grau</strong> del polinomi: el grau més alt dels seus termes. \(P(x)\) és de grau 3.", r"El <strong>grado</strong> del polinomio: el grado más alto de sus términos. \(P(x)\) es de grado 3.", r"The <strong>degree</strong> of the polynomial: the highest degree of its terms. \(P(x)\) has degree 3."),
       L(r"Els <strong>coeficients</strong>: els nombres de cada terme, amb el seu signe: \(4,\ -2,\ 1,\ -7\).", r"Los <strong>coeficientes</strong>: los números de cada término, con su signo: \(4,\ -2,\ 1,\ -7\).", r"The <strong>coefficients</strong>: the numbers of each term, with their signs: \(4,\ -2,\ 1,\ -7\)."),
       L(r"El <strong>coeficient principal</strong>: el del terme de grau més alt (\(4\)).", r"El <strong>coeficiente principal</strong>: el del término de mayor grado (\(4\)).", r"The <strong>leading coefficient</strong>: that of the highest-degree term (\(4\))."),
       L(r"El <strong>terme independent</strong>: el que no té lletra (\(-7\)). Si no n'hi ha, és 0.", r"El <strong>término independiente</strong>: el que no tiene letra (\(-7\)). Si no hay, es 0.", r"The <strong>constant term</strong>: the one with no letter (\(-7\)). If there isn't one, it's 0.")))
s4 += box('def', L('Polinomi reduït, ordenat i complet', 'Polinomio reducido, ordenado y completo', 'Simplified, ordered and complete polynomials'),
  ul(L(r"<strong>Reduït</strong>: no té termes semblants. Abans de dir-ne el grau, cal <strong>reduir-lo</strong>: \(3x^2+x-x^2+5=2x^2+x+5\).", r"<strong>Reducido</strong>: no tiene términos semejantes. Antes de decir su grado, hay que <strong>reducirlo</strong>: \(3x^2+x-x^2+5=2x^2+x+5\).", r"<strong>Simplified</strong>: it has no like terms. Before giving its degree, <strong>simplify</strong> it: \(3x^2+x-x^2+5=2x^2+x+5\)."),
     L(r"<strong>Ordenat</strong>: els termes estan escrits de grau més alt a més baix. \(5-x^3+2x\) ordenat és \(-x^3+2x+5\).", r"<strong>Ordenado</strong>: los términos están escritos de mayor a menor grado. \(5-x^3+2x\) ordenado es \(-x^3+2x+5\).", r"<strong>Ordered</strong>: terms written from highest to lowest degree. \(5-x^3+2x\) in order is \(-x^3+2x+5\)."),
     L(r"<strong>Complet</strong>: té termes de tots els graus, des del més alt fins al terme independent. \(-x^3+2x+5\) no és complet (falta \(x^2\)); si cal, l'escrivim \(-x^3+0x^2+2x+5\).", r"<strong>Completo</strong>: tiene términos de todos los grados, desde el más alto hasta el término independiente. \(-x^3+2x+5\) no es completo (falta \(x^2\)); si hace falta, lo escribimos \(-x^3+0x^2+2x+5\).", r"<strong>Complete</strong>: it has terms of every degree, from the highest down to the constant. \(-x^3+2x+5\) isn't complete (no \(x^2\)); if needed we write \(-x^3+0x^2+2x+5\).")))
s4 += box('def', L("Valor numèric d'un polinomi", 'Valor numérico de un polinomio', 'Value of a polynomial'),
  P(r"El valor numèric de \(P(x)\) per a \(x=a\) s'escriu \(P(a)\): substituïm la \(x\) per \(a\) i operem.",
    r"El valor numérico de \(P(x)\) para \(x=a\) se escribe \(P(a)\): sustituimos la \(x\) por \(a\) y operamos.",
    r"The value of \(P(x)\) at \(x=a\) is written \(P(a)\): replace \(x\) with \(a\) and work it out.")
  + D(r"P(x)=4x^3-2x^2+x-7:\qquad P(2)=4\cdot8-2\cdot4+2-7=19\qquad P(0)=-7")
  + note(r"\(P(0)\) sempre és el terme independent: tots els termes amb \(x\) valen 0.", r"\(P(0)\) siempre es el término independiente: todos los términos con \(x\) valen 0.", r"\(P(0)\) is always the constant term: every term with \(x\) is 0.")
  + widget('w-poly', '🔬', L("Analitzador de polinomis", 'Analizador de polinomios', 'Polynomial analyser'),
           ['<div class="wrow">' + tin('p', 'P(x) =', '4x^3-2x^2+x-7') + tin('a', L('Valor de x', 'Valor de x', 'Value of x'), '2', 's') + '</div>', HELP,
            quick([('4x^3-2x^2+x-7|2', '4x³−2x²+x−7'), ('5-x^3+2x|-1', '5−x³+2x'), ('3x^2+x-x^2+5|3', '3x²+x−x²+5'), ('x^4-3x^2+1|-2', 'x⁴−3x²+1'), ('2x-x^2|1/2', '2x−x²')])], out='<div class="cards"></div><div class="hsteps"></div>'))
chk('4*8-2*4+2-7', 19)
s4 += levels(
 [prob(L(r"Del polinomi \(Q(x)=3x-x^4+6+2x^2\), digues: a) el grau; b) el coeficient principal; c) el terme independent; d) si és complet. Escriu-lo ordenat.", r"Del polinomio \(Q(x)=3x-x^4+6+2x^2\), di: a) el grado; b) el coeficiente principal; c) el término independiente; d) si es completo. Escríbelo ordenado.", r"For \(Q(x)=3x-x^4+6+2x^2\), give: a) its degree; b) its leading coefficient; c) its constant term; d) whether it's complete. Write it in order."),
       D(r"Q(x)=-x^4+2x^2+3x+6"),
       P(r"a) Grau \(\boxed{4}\). b) Coeficient principal \(\boxed{-1}\). c) Terme independent \(\boxed{6}\). d) <strong>No</strong> és complet: falta el terme de grau 3.", r"a) Grado \(\boxed{4}\). b) Coeficiente principal \(\boxed{-1}\). c) Término independiente \(\boxed{6}\). d) <strong>No</strong> es completo: falta el término de grado 3.", r"a) Degree \(\boxed{4}\). b) Leading coefficient \(\boxed{-1}\). c) Constant term \(\boxed{6}\). d) It's <strong>not</strong> complete: there's no degree-3 term.")),
  prob(L(r"Si \(P(x)=x^2-5x+6\), calcula \(P(0)\), \(P(1)\), \(P(-1)\) i \(P(3)\).", r"Si \(P(x)=x^2-5x+6\), calcula \(P(0)\), \(P(1)\), \(P(-1)\) y \(P(3)\).", r"If \(P(x)=x^2-5x+6\), find \(P(0)\), \(P(1)\), \(P(-1)\) and \(P(3)\)."),
       D(r"P(0)=\boxed{6}\qquad P(1)=1-5+6=\boxed{2}"),
       D(r"P(-1)=(-1)^2-5\cdot(-1)+6=1+5+6=\boxed{12}\qquad P(3)=9-15+6=\boxed{0}"))],
 [prob(L(r"Redueix i ordena \(R(x)=2x^3-x+4x^2-5x^3+3x-1+x^2\). Quin grau té?", r"Reduce y ordena \(R(x)=2x^3-x+4x^2-5x^3+3x-1+x^2\). ¿Qué grado tiene?", r"Simplify and order \(R(x)=2x^3-x+4x^2-5x^3+3x-1+x^2\). What is its degree?"),
       D(r"R(x)=(2-5)x^3+(4+1)x^2+(-1+3)x-1=\boxed{-3x^3+5x^2+2x-1}"),
       P(r"És de grau \(\boxed{3}\) i, ara sí, complet.", r"Es de grado \(\boxed{3}\) y, ahora sí, completo.", r"It has degree \(\boxed{3}\) and, now, it's complete."))],
 [prob(L(r"Troba \(k\) perquè el polinomi \(P(x)=x^3+kx^2-4\) valga 0 per a \(x=2\).", r"Halla \(k\) para que el polinomio \(P(x)=x^3+kx^2-4\) valga 0 para \(x=2\).", r"Find \(k\) so that \(P(x)=x^3+kx^2-4\) is 0 when \(x=2\)."),
       D(r"P(2)=8+4k-4=4k+4"),
       P(r"Volem que \(4k+4=0\): quin nombre multiplicat per 4 i sumant-hi 4 dona 0? \(\ 4k=-4\), per tant \(\boxed{k=-1}\).", r"Queremos que \(4k+4=0\): ¿qué número multiplicado por 4 y sumándole 4 da 0? \(\ 4k=-4\), por tanto \(\boxed{k=-1}\).", r"We want \(4k+4=0\): which number times 4, plus 4, gives 0? \(\ 4k=-4\), so \(\boxed{k=-1}\)."),
       P(r"Comprovació: \(P(2)=8-4-4=0\) ✓", r"Comprobación: \(P(2)=8-4-4=0\) ✓", r"Check: \(P(2)=8-4-4=0\) ✓"))])
chk('1-5+6', 2); chk('1+5+6', 12); chk('9-15+6', 0)
chk('2x^3-x+4x^2-5x^3+3x-1+x^2', '-3x^3+5x^2+2x-1'); chk('8+4*(-1)-4', 0)
s4 += practice([
  ('★', L(r"a) Indica el grau, el coeficient principal i el terme independent de \(P(x)=7-3x^2+x^5\) i escriu-lo ordenat. És complet?", r"a) Indica el grado, el coeficiente principal y el término independiente de \(P(x)=7-3x^2+x^5\) y escríbelo ordenado. ¿Es completo?", r"a) Give the degree, leading coefficient and constant term of \(P(x)=7-3x^2+x^5\) and write it in order. Is it complete?")),
  ('★★', L(r"b) Redueix \(Q(x)=x^2-4x+3x^2+x-2\) i calcula \(Q(-2)\) i \(Q\!\left(\frac{1}{2}\right)\).", r"b) Reduce \(Q(x)=x^2-4x+3x^2+x-2\) y calcula \(Q(-2)\) y \(Q\!\left(\frac{1}{2}\right)\).", r"b) Simplify \(Q(x)=x^2-4x+3x^2+x-2\) and find \(Q(-2)\) and \(Q\!\left(\frac{1}{2}\right)\).")),
  ('★★★', L(r"c) Escriu un polinomi de grau 3, complet, amb coeficient principal \(-2\) i terme independent \(5\), tal que \(P(1)=0\).", r"c) Escribe un polinomio de grado 3, completo, con coeficiente principal \(-2\) y término independiente \(5\), tal que \(P(1)=0\).", r"c) Write a complete degree-3 polynomial with leading coefficient \(-2\) and constant term \(5\) such that \(P(1)=0\)."))],
  P(r"a) \(P(x)=x^5-3x^2+7\): grau 5, coeficient principal 1, terme independent 7; no és complet (falten \(x^4\), \(x^3\) i \(x\)).", r"a) \(P(x)=x^5-3x^2+7\): grado 5, coeficiente principal 1, término independiente 7; no es completo (faltan \(x^4\), \(x^3\) y \(x\)).", r"a) \(P(x)=x^5-3x^2+7\): degree 5, leading coefficient 1, constant term 7; not complete (no \(x^4\), \(x^3\) or \(x\)).")
  + D(r"\text{b)}\ Q(x)=4x^2-3x-2;\quad Q(-2)=16+6-2=20;\quad Q\!\left(\tfrac{1}{2}\right)=1-\tfrac{3}{2}-2=-\tfrac{5}{2}")
  + P(r"c) Per exemple \(P(x)=-2x^3+x^2-4x+5\): \(P(1)=-2+1-4+5=0\). (N'hi ha molts: cal que els coeficients del mig sumen \(-3\).)", r"c) Por ejemplo \(P(x)=-2x^3+x^2-4x+5\): \(P(1)=-2+1-4+5=0\). (Hay muchos: hace falta que los coeficientes del medio sumen \(-3\).)", r"c) For example \(P(x)=-2x^3+x^2-4x+5\): \(P(1)=-2+1-4+5=0\). (There are many: the middle coefficients must add up to \(-3\).)"))
chk('x^2-4x+3x^2+x-2', '4x^2-3x-2'); chk('4*4+6-2', 20); chk('4*(1/4)-3/2-2', '-5/2'); chk('-2+1-4+5', 0)

# =====================================================================
# 3.5 Suma i resta de polinomis
# =====================================================================
s5 = box('def', L('Suma i resta de polinomis', 'Suma y resta de polinomios', 'Adding and subtracting polynomials'),
  P(r"Per a <strong>sumar</strong> dos polinomis, sumem els <strong>termes semblants</strong> (els del mateix grau). Ho podem fer en línia o en columna, posant els termes semblants un davall de l'altre:",
    r"Para <strong>sumar</strong> dos polinomios, sumamos los <strong>términos semejantes</strong> (los del mismo grado). Lo podemos hacer en línea o en columna, poniendo los términos semejantes uno debajo del otro:",
    r"To <strong>add</strong> two polynomials, add the <strong>like terms</strong> (those of the same degree). We can do it in a line or in columns, writing like terms one under the other:")
  + D(r"P(x)=3x^3-2x^2+5,\quad Q(x)=x^3+4x^2-3x-1")
  + D(r"P(x)+Q(x)=(3+1)x^3+(-2+4)x^2-3x+(5-1)=4x^3+2x^2-3x+4")
  + P(r"Per a <strong>restar</strong>, sumem el primer amb l'<strong>oposat</strong> del segon: canviem el signe de <strong>tots</strong> els termes del polinomi que restem.",
      r"Para <strong>restar</strong>, sumamos el primero con el <strong>opuesto</strong> del segundo: cambiamos el signo de <strong>todos</strong> los términos del polinomio que restamos.",
      r"To <strong>subtract</strong>, add the first to the <strong>opposite</strong> of the second: change the sign of <strong>every</strong> term of the polynomial being subtracted.")
  + D(r"P(x)-Q(x)=3x^3-2x^2+5\ \underbrace{-x^3-4x^2+3x+1}_{-Q(x)}=2x^3-6x^2+3x+6")
  + note(r"L'error més habitual en restar és canviar el signe només del primer terme. El signe menys davant del parèntesi afecta <strong>tots</strong> els termes: \(-(x^3+4x^2-3x-1)=-x^3-4x^2+3x+1\).",
         r"El error más habitual al restar es cambiar el signo solo del primer término. El signo menos delante del paréntesis afecta a <strong>todos</strong> los términos: \(-(x^3+4x^2-3x-1)=-x^3-4x^2+3x+1\).",
         r"The most common mistake when subtracting is changing the sign of the first term only. The minus sign before the bracket affects <strong>every</strong> term: \(-(x^3+4x^2-3x-1)=-x^3-4x^2+3x+1\).", '⚠')
  + widget('w-addsub', '➕', L('Suma i resta en columna', 'Suma y resta en columna', 'Adding and subtracting in columns'),
           ['<div class="wrow">' + tin('p', 'P =', '3x^3-2x^2+5') + seg([('+', 'P + Q'), ('-', 'P − Q')], '+') + tin('q', 'Q =', 'x^3+4x^2-3x-1') + '</div>', HELP,
            quick([('3x^3-2x^2+5|x^3+4x^2-3x-1', 'P, Q'), ('x^2-3x+2|-x^2+5x-7', 'x²−3x+2, −x²+5x−7'), ('4x^3-x|2x^2+x-3', '4x³−x, 2x²+x−3'), ('2x^2y-xy+3|x^2y+4xy', '2x²y−xy+3, x²y+4xy')])])
  + drill('addsub', 'Entrena: suma i resta de polinomis', 'Entrena: suma y resta de polinomios', 'Train: adding and subtracting'))
chk('(3x^3-2x^2+5)+(x^3+4x^2-3x-1)', '4x^3+2x^2-3x+4'); chk('(3x^3-2x^2+5)-(x^3+4x^2-3x-1)', '2x^3-6x^2+3x+6')
s5 += levels(
 [prob(L(r"Donats \(A(x)=2x^2-5x+3\) i \(B(x)=-x^2+2x-7\), calcula \(A(x)+B(x)\) i \(A(x)-B(x)\).", r"Dados \(A(x)=2x^2-5x+3\) y \(B(x)=-x^2+2x-7\), calcula \(A(x)+B(x)\) y \(A(x)-B(x)\).", r"Given \(A(x)=2x^2-5x+3\) and \(B(x)=-x^2+2x-7\), find \(A(x)+B(x)\) and \(A(x)-B(x)\)."),
       D(r"A+B=(2-1)x^2+(-5+2)x+(3-7)=\boxed{x^2-3x-4}"),
       D(r"A-B=2x^2-5x+3+x^2-2x+7=\boxed{3x^2-7x+10}"))],
 [prob(L(r"Amb \(P(x)=x^3-2x+1\), \(Q(x)=3x^2+x\) i \(R(x)=x^3-x^2+4\), calcula \(P(x)+Q(x)-R(x)\).", r"Con \(P(x)=x^3-2x+1\), \(Q(x)=3x^2+x\) y \(R(x)=x^3-x^2+4\), calcula \(P(x)+Q(x)-R(x)\).", r"With \(P(x)=x^3-2x+1\), \(Q(x)=3x^2+x\) and \(R(x)=x^3-x^2+4\), find \(P(x)+Q(x)-R(x)\)."),
       P(r"Posem en columna (cada grau en la seua columna, i el signe de \(R\) canviat):", r"Ponemos en columna (cada grado en su columna, y el signo de \(R\) cambiado):", r"Write in columns (each degree in its own column, with the signs of \(R\) changed):"),
       table(['', r'\(x^3\)', r'\(x^2\)', r'\(x\)', r'\(1\)'],
             [[r'\(P\)', r'\(1\)', r'\(0\)', r'\(-2\)', r'\(1\)'], [r'\(Q\)', r'\(0\)', r'\(3\)', r'\(1\)', r'\(0\)'], [r'\(-R\)', r'\(-1\)', r'\(1\)', r'\(0\)', r'\(-4\)'], [r'<b>' + L('Total', 'Total', 'Total') + '</b>', r'\(0\)', r'\(4\)', r'\(-1\)', r'\(-3\)']], 'data narrow coltab'),
       D(r"P+Q-R=\boxed{4x^2-x-3}"),
       P(r"Els termes de grau 3 s'han anul·lat: el resultat és de grau 2, encara que els polinomis eren de grau 3.", r"Los términos de grado 3 se han anulado: el resultado es de grado 2, aunque los polinomios eran de grado 3.", r"The degree-3 terms cancelled: the result has degree 2, even though the polynomials had degree 3."))],
 [prob(L(r"Quin polinomi hem de sumar a \(P(x)=2x^3-x^2+5x-3\) per a obtindre \(S(x)=x^3+4x-1\)?", r"¿Qué polinomio tenemos que sumar a \(P(x)=2x^3-x^2+5x-3\) para obtener \(S(x)=x^3+4x-1\)?", r"Which polynomial must be added to \(P(x)=2x^3-x^2+5x-3\) to get \(S(x)=x^3+4x-1\)?"),
       P(r"Si \(P+X=S\), aleshores \(X=S-P\):", r"Si \(P+X=S\), entonces \(X=S-P\):", r"If \(P+X=S\), then \(X=S-P\):"),
       D(r"X=x^3+4x-1-2x^3+x^2-5x+3=\boxed{-x^3+x^2-x+2}"),
       P(r"Comprovació: \(P+X=(2-1)x^3+(-1+1)x^2+(5-1)x+(-3+2)=x^3+4x-1\) ✓", r"Comprobación: \(P+X=(2-1)x^3+(-1+1)x^2+(5-1)x+(-3+2)=x^3+4x-1\) ✓", r"Check: \(P+X=(2-1)x^3+(-1+1)x^2+(5-1)x+(-3+2)=x^3+4x-1\) ✓"))])
chk('(2x^2-5x+3)+(-x^2+2x-7)', 'x^2-3x-4'); chk('(2x^2-5x+3)-(-x^2+2x-7)', '3x^2-7x+10'); chk('(x^3-2x+1)+(3x^2+x)-(x^3-x^2+4)', '4x^2-x-3')
chk('(x^3+4x-1)-(2x^3-x^2+5x-3)', '-x^3+x^2-x+2')
s5 += practice([
  ('★', L(r"Amb \(P(x)=5x^2-x+2\) i \(Q(x)=-3x^2+4x-6\), calcula a) \(P+Q\); b) \(P-Q\); c) \(Q-P\).", r"Con \(P(x)=5x^2-x+2\) y \(Q(x)=-3x^2+4x-6\), calcula a) \(P+Q\); b) \(P-Q\); c) \(Q-P\).", r"With \(P(x)=5x^2-x+2\) and \(Q(x)=-3x^2+4x-6\), find a) \(P+Q\); b) \(P-Q\); c) \(Q-P\).")),
  ('★★', L(r"d) \((x^3-4x^2+2)-(2x^3+x-5)+(x^2-3x)\).", r"d) \((x^3-4x^2+2)-(2x^3+x-5)+(x^2-3x)\).", r"d) \((x^3-4x^2+2)-(2x^3+x-5)+(x^2-3x)\).")),
  ('★★★', L(r"e) Un triangle té els costats \(x^2+1\), \(2x^2-x\) i \(3x+4\). Escriu-ne el perímetre i calcula'l per a \(x=3\).", r"e) Un triángulo tiene los lados \(x^2+1\), \(2x^2-x\) y \(3x+4\). Escribe su perímetro y calcúlalo para \(x=3\).", r"e) A triangle has sides \(x^2+1\), \(2x^2-x\) and \(3x+4\). Write its perimeter and work it out for \(x=3\)."))],
  D(r"\text{a)}\ 2x^2+3x-4\qquad \text{b)}\ 8x^2-5x+8\qquad \text{c)}\ -8x^2+5x-8")
  + D(r"\text{d)}\ -x^3-3x^2-4x+7\qquad \text{e)}\ 3x^2+2x+5;\ \ x=3:\ 27+6+5=38"))
chk('(5x^2-x+2)+(-3x^2+4x-6)', '2x^2+3x-4'); chk('(5x^2-x+2)-(-3x^2+4x-6)', '8x^2-5x+8'); chk('(x^3-4x^2+2)-(2x^3+x-5)+(x^2-3x)', '-x^3-3x^2-4x+7')
chk('(x^2+1)+(2x^2-x)+(3x+4)', '3x^2+2x+5'); chk('27+6+5', 38)

# =====================================================================
# 3.6 Producte de polinomis
# =====================================================================
s6 = box('def', L('Producte per un nombre i per un monomi', 'Producto por un número y por un monomio', 'Multiplying by a number or a monomial'),
  P(r"Per a multiplicar un polinomi per un nombre o per un monomi, apliquem la <strong>propietat distributiva</strong>: multipliquem <strong>cada terme</strong> del polinomi.",
    r"Para multiplicar un polinomio por un número o por un monomio, aplicamos la <strong>propiedad distributiva</strong>: multiplicamos <strong>cada término</strong> del polinomio.",
    r"To multiply a polynomial by a number or a monomial, use the <strong>distributive property</strong>: multiply <strong>each term</strong> of the polynomial.")
  + D(r"3\cdot(2x^2-x+4)=6x^2-3x+12\qquad -2x\cdot(3x^2-x+4)=-6x^3+2x^2-8x")
  + note(r"Compte amb els signes: \(-2x\cdot(-x)=+2x^2\). I no t'oblides de cap terme, ni tan sols del terme independent.", r"Cuidado con los signos: \(-2x\cdot(-x)=+2x^2\). Y no te olvides de ningún término, ni siquiera del término independiente.", r"Watch the signs: \(-2x\cdot(-x)=+2x^2\). And don't forget any term, not even the constant.", '⚠'))
s6 += box('def', L('Producte de dos polinomis', 'Producto de dos polinomios', 'Multiplying two polynomials'),
  P(r"Multipliquem <strong>cada terme del primer</strong> per <strong>cada terme del segon</strong> i, al final, <strong>reduïm</strong> els termes semblants. Una taula ajuda a no deixar-se'n cap:",
    r"Multiplicamos <strong>cada término del primero</strong> por <strong>cada término del segundo</strong> y, al final, <strong>reducimos</strong> los términos semejantes. Una tabla ayuda a no dejarse ninguno:",
    r"Multiply <strong>each term of the first</strong> by <strong>each term of the second</strong> and finally <strong>collect</strong> like terms. A grid helps you not to miss any:")
  + D(r"(x+3)(2x-5)=2x^2-5x+6x-15=2x^2+x-15")
  + table([r'\(\cdot\)', r'\(2x\)', r'\(-5\)'], [[r'\(x\)', r'\(2x^2\)', r'\(-5x\)'], [r'\(3\)', r'\(6x\)', r'\(-15\)']], 'data narrow multab')
  + P(r"El grau del producte és la <strong>suma dels graus</strong>: si multipliquem un polinomi de grau 1 per un de grau 2, el resultat és de grau 3.",
      r"El grado del producto es la <strong>suma de los grados</strong>: si multiplicamos un polinomio de grado 1 por uno de grado 2, el resultado es de grado 3.",
      r"The degree of the product is the <strong>sum of the degrees</strong>: a degree-1 polynomial times a degree-2 polynomial gives degree 3.")
  + widget('w-mul', '✖', L('Producte amb taula', 'Producto con tabla', 'Multiplying with a grid'),
           ['<div class="wrow">' + tin('p', 'P =', 'x+3') + tin('q', 'Q =', '2x-5') + '</div>', HELP,
            quick([('x+3|2x-5', '(x+3)(2x−5)'), ('-2x|3x^2-x+4', '−2x·(3x²−x+4)'), ('x-4|x+4', '(x−4)(x+4)'), ('2x-1|x^2+3x-2', '(2x−1)(x²+3x−2)'), ('x^2-x+1|x+1', '(x²−x+1)(x+1)')])])
  + drill('mul', 'Entrena: producte de polinomis', 'Entrena: producto de polinomios', 'Train: multiplying polynomials'))
chk('3(2x^2-x+4)', '6x^2-3x+12'); chk('-2x(3x^2-x+4)', '-6x^3+2x^2-8x'); chk('(x+3)(2x-5)', '2x^2+x-15')
s6 += levels(
 [prob(L(r"Calcula: a) \(-4(x^2-3x+2)\); b) \(5x^2\cdot(2x^3-x+3)\); c) \(-x\cdot(x^2-6x-1)\).", r"Calcula: a) \(-4(x^2-3x+2)\); b) \(5x^2\cdot(2x^3-x+3)\); c) \(-x\cdot(x^2-6x-1)\).", r"Work out: a) \(-4(x^2-3x+2)\); b) \(5x^2\cdot(2x^3-x+3)\); c) \(-x\cdot(x^2-6x-1)\)."),
       D(r"\text{a)}\ \boxed{-4x^2+12x-8}\qquad \text{b)}\ \boxed{10x^5-5x^3+15x^2}\qquad \text{c)}\ \boxed{-x^3+6x^2+x}")),
  prob(L(r"Calcula \((x-2)(x+7)\).", r"Calcula \((x-2)(x+7)\).", r"Work out \((x-2)(x+7)\)."),
       D(r"x^2+7x-2x-14=\boxed{x^2+5x-14}"))],
 [prob(L(r"Calcula \((2x-3)(x^2+4x-1)\).", r"Calcula \((2x-3)(x^2+4x-1)\).", r"Work out \((2x-3)(x^2+4x-1)\)."),
       table([r'\(\cdot\)', r'\(x^2\)', r'\(4x\)', r'\(-1\)'], [[r'\(2x\)', r'\(2x^3\)', r'\(8x^2\)', r'\(-2x\)'], [r'\(-3\)', r'\(-3x^2\)', r'\(-12x\)', r'\(3\)']], 'data narrow multab'),
       D(r"2x^3+(8-3)x^2+(-2-12)x+3=\boxed{2x^3+5x^2-14x+3}"),
       P(r"Comprovació ràpida amb \(x=1\): \((2-3)(1+4-1)=-4\) i \(2+5-14+3=-4\) ✓", r"Comprobación rápida con \(x=1\): \((2-3)(1+4-1)=-4\) y \(2+5-14+3=-4\) ✓", r"Quick check with \(x=1\): \((2-3)(1+4-1)=-4\) and \(2+5-14+3=-4\) ✓"))],
 [prob(L(r"Simplifica \(\ (x+2)(x-3)-x(x-4)+2(x-1)\).", r"Simplifica \(\ (x+2)(x-3)-x(x-4)+2(x-1)\).", r"Simplify \(\ (x+2)(x-3)-x(x-4)+2(x-1)\)."),
       D(r"(x+2)(x-3)=x^2-x-6\qquad -x(x-4)=-x^2+4x\qquad 2(x-1)=2x-2"),
       D(r"x^2-x-6-x^2+4x+2x-2=\boxed{5x-8}"),
       P(r"Els termes en \(x^2\) s'anul·len: el resultat és de grau 1.", r"Los términos en \(x^2\) se anulan: el resultado es de grado 1.", r"The \(x^2\) terms cancel: the result has degree 1.")),
  prob(L(r"Un jardí rectangular fa \(x+5\) m de llarg i \(x+2\) m d'ample. Al mig hi ha una bassa quadrada de \(x\) m de costat. Escriu l'àrea de la part amb gespa.", r"Un jardín rectangular mide \(x+5\) m de largo y \(x+2\) m de ancho. En medio hay un estanque cuadrado de \(x\) m de lado. Escribe el área de la parte con césped.", r"A rectangular garden is \(x+5\) m long and \(x+2\) m wide. In the middle there's a square pond with side \(x\) m. Write the area of the lawn."),
       D(r"(x+5)(x+2)-x^2=x^2+7x+10-x^2=\boxed{7x+10\ \text{m}^2}"))])
chk('-4(x^2-3x+2)', '-4x^2+12x-8'); chk('5x^2(2x^3-x+3)', '10x^5-5x^3+15x^2'); chk('-x(x^2-6x-1)', '-x^3+6x^2+x'); chk('(x-2)(x+7)', 'x^2+5x-14')
chk('(2x-3)(x^2+4x-1)', '2x^3+5x^2-14x+3'); chk('(x+2)(x-3)-x(x-4)+2(x-1)', '5x-8'); chk('(x+5)(x+2)-x^2', '7x+10')
s6 += practice([
  ('★', L(r"Calcula: a) \(6(x^2-2x+5)\); b) \(-3x(2x^2+x-4)\); c) \((x+4)(x-1)\).", r"Calcula: a) \(6(x^2-2x+5)\); b) \(-3x(2x^2+x-4)\); c) \((x+4)(x-1)\).", r"Work out: a) \(6(x^2-2x+5)\); b) \(-3x(2x^2+x-4)\); c) \((x+4)(x-1)\).")),
  ('★★', L(r"d) \((3x-2)(2x+5)\); e) \((x^2-3)(x^2+x-2)\).", r"d) \((3x-2)(2x+5)\); e) \((x^2-3)(x^2+x-2)\).", r"d) \((3x-2)(2x+5)\); e) \((x^2-3)(x^2+x-2)\).")),
  ('★★★', L(r"f) \((x-1)(x+1)(x+2)\); g) \(2x(x-3)-(x+1)(x-5)\).", r"f) \((x-1)(x+1)(x+2)\); g) \(2x(x-3)-(x+1)(x-5)\).", r"f) \((x-1)(x+1)(x+2)\); g) \(2x(x-3)-(x+1)(x-5)\)."))],
  D(r"\text{a)}\ 6x^2-12x+30\qquad \text{b)}\ -6x^3-3x^2+12x\qquad \text{c)}\ x^2+3x-4")
  + D(r"\text{d)}\ 6x^2+11x-10\qquad \text{e)}\ x^4+x^3-5x^2-3x+6")
  + D(r"\text{f)}\ (x^2-1)(x+2)=x^3+2x^2-x-2\qquad \text{g)}\ 2x^2-6x-(x^2-4x-5)=x^2-2x+5"))
chk('6(x^2-2x+5)', '6x^2-12x+30'); chk('-3x(2x^2+x-4)', '-6x^3-3x^2+12x'); chk('(x+4)(x-1)', 'x^2+3x-4')
chk('(3x-2)(2x+5)', '6x^2+11x-10'); chk('(x^2-3)(x^2+x-2)', 'x^4+x^3-5x^2-3x+6'); chk('(x-1)(x+1)(x+2)', 'x^3+2x^2-x-2'); chk('2x(x-3)-(x+1)(x-5)', 'x^2-2x+5')

# =====================================================================
# 3.7 Identitats notables
# =====================================================================
s7 = box('def', L('Les tres identitats notables', 'Las tres identidades notables', 'The three special products'),
  P(r"Hi ha tres productes que apareixen tan sovint que convé saber-los de memòria. Són les <strong>identitats notables</strong>:",
    r"Hay tres productos que aparecen tan a menudo que conviene saberlos de memoria. Son las <strong>identidades notables</strong>:",
    r"Three products come up so often that it's worth learning them by heart. They are the <strong>special products</strong>:")
  + D(r"\begin{aligned}(a+b)^2&=a^2+2ab+b^2&&\tri{quadrat d'una suma}{cuadrado de una suma}{square of a sum}\\(a-b)^2&=a^2-2ab+b^2&&\tri{quadrat d'una diferència}{cuadrado de una diferencia}{square of a difference}\\(a+b)(a-b)&=a^2-b^2&&\tri{suma per diferència}{suma por diferencia}{sum times difference}\end{aligned}")
  + P(r"En paraules: «el quadrat d'una suma és el quadrat del primer, <strong>més el doble del primer pel segon</strong>, més el quadrat del segon». I «suma per diferència és igual a <strong>diferència de quadrats</strong>».",
      r"En palabras: «el cuadrado de una suma es el cuadrado del primero, <strong>más el doble del primero por el segundo</strong>, más el cuadrado del segundo». Y «suma por diferencia es igual a <strong>diferencia de cuadrados</strong>».",
      r"In words: “the square of a sum is the first squared, <strong>plus twice the first times the second</strong>, plus the second squared”. And “sum times difference equals the <strong>difference of two squares</strong>”.")
  + P(r"Les podem comprovar multiplicant: \((a+b)^2=(a+b)(a+b)=a^2+ab+ab+b^2=a^2+2ab+b^2\). I també es veuen amb àrees:",
      r"Las podemos comprobar multiplicando: \((a+b)^2=(a+b)(a+b)=a^2+ab+ab+b^2=a^2+2ab+b^2\). Y también se ven con áreas:",
      r"We can check them by multiplying: \((a+b)^2=(a+b)(a+b)=a^2+ab+ab+b^2=a^2+2ab+b^2\). They can also be seen with areas:")
  + '<div class="figs"><figure>' + svg_sq() + '<figcaption>' + L("(a + b)² = a² + 2ab + b²", "(a + b)² = a² + 2ab + b²", "(a + b)² = a² + 2ab + b²") + '</figcaption></figure>' + svg_dif() + '</div>')
s7 += box('prop', L('Com aplicar-les', 'Cómo aplicarlas', 'How to use them'),
  P(r"Identifica qui fa de \(a\) i qui fa de \(b\) i substitueix, <strong>amb parèntesis</strong>:", r"Identifica quién hace de \(a\) y quién de \(b\) y sustituye, <strong>con paréntesis</strong>:", r"Work out what plays the role of \(a\) and of \(b\) and substitute, <strong>using brackets</strong>:")
  + D(r"(3x+2)^2=(3x)^2+2\cdot3x\cdot2+2^2=9x^2+12x+4")
  + D(r"(x-5)^2=x^2-2\cdot x\cdot5+5^2=x^2-10x+25\qquad (2x+3)(2x-3)=(2x)^2-3^2=4x^2-9")
  + note(r"Error típic: \((x+3)^2\neq x^2+9\). No t'oblides del <strong>doble producte</strong>! Fes la prova amb \(x=1\): \((1+3)^2=16\), però \(1+9=10\).",
         r"Error típico: \((x+3)^2\neq x^2+9\). ¡No te olvides del <strong>doble producto</strong>! Haz la prueba con \(x=1\): \((1+3)^2=16\), pero \(1+9=10\).",
         r"Common mistake: \((x+3)^2\neq x^2+9\). Don't forget the <strong>middle term</strong>! Try \(x=1\): \((1+3)^2=16\), but \(1+9=10\).", '⚠')
  + P(r"També les podem fer servir <strong>al revés</strong>, per a escriure un polinomi com a producte: \(x^2-49=(x+7)(x-7)\) i \(x^2+6x+9=(x+3)^2\).",
      r"También las podemos usar <strong>al revés</strong>, para escribir un polinomio como producto: \(x^2-49=(x+7)(x-7)\) y \(x^2+6x+9=(x+3)^2\).",
      r"We can also use them <strong>backwards</strong>, to write a polynomial as a product: \(x^2-49=(x+7)(x-7)\) and \(x^2+6x+9=(x+3)^2\).")
  + widget('w-id', '🟧', L('Desenvolupa una identitat notable', 'Desarrolla una identidad notable', 'Expand a special product'),
           ['<div class="wrow">' + seg([('sq+', '(a + b)²'), ('sq-', '(a − b)²'), ('dif', '(a + b)(a − b)')], 'sq+') + '</div>',
            '<div class="wrow">' + tin('a', 'a =', '3x', 's') + tin('b', 'b =', '2', 's') + '</div>',
            quick([('3x|2|sq+', '(3x+2)²'), ('x|5|sq-', '(x−5)²'), ('2x|3|dif', '(2x+3)(2x−3)'), ('x^2|1|sq+', '(x²+1)²'), ('4|x|sq-', '(4−x)²'), ('x|1/2|dif', '(x+½)(x−½)')])])
  + drill('id', 'Entrena: identitats notables', 'Entrena: identidades notables', 'Train: special products'))
chk('(3x+2)^2', '9x^2+12x+4'); chk('(x-5)^2', 'x^2-10x+25'); chk('(2x+3)(2x-3)', '4x^2-9'); chk('(x+7)(x-7)', 'x^2-49'); chk('(x+3)^2', 'x^2+6x+9')
s7 += levels(
 [prob(L(r"Desenvolupa: a) \((x+4)^2\); b) \((x-6)^2\); c) \((x+1)(x-1)\).", r"Desarrolla: a) \((x+4)^2\); b) \((x-6)^2\); c) \((x+1)(x-1)\).", r"Expand: a) \((x+4)^2\); b) \((x-6)^2\); c) \((x+1)(x-1)\)."),
       D(r"\text{a)}\ x^2+2\cdot x\cdot4+16=\boxed{x^2+8x+16}\qquad \text{b)}\ x^2-2\cdot x\cdot6+36=\boxed{x^2-12x+36}"),
       D(r"\text{c)}\ \boxed{x^2-1}"))],
 [prob(L(r"Desenvolupa: a) \((2x-5)^2\); b) \((3x+y)^2\); c) \((x^2+4)(x^2-4)\).", r"Desarrolla: a) \((2x-5)^2\); b) \((3x+y)^2\); c) \((x^2+4)(x^2-4)\).", r"Expand: a) \((2x-5)^2\); b) \((3x+y)^2\); c) \((x^2+4)(x^2-4)\)."),
       D(r"\text{a)}\ (2x)^2-2\cdot2x\cdot5+5^2=\boxed{4x^2-20x+25}"),
       D(r"\text{b)}\ (3x)^2+2\cdot3x\cdot y+y^2=\boxed{9x^2+6xy+y^2}\qquad \text{c)}\ (x^2)^2-4^2=\boxed{x^4-16}")),
  prob(L(r"Escriu com a quadrat d'un binomi o com a suma per diferència: a) \(x^2-14x+49\); b) \(x^2-25\); c) \(4x^2+4x+1\).", r"Escribe como cuadrado de un binomio o como suma por diferencia: a) \(x^2-14x+49\); b) \(x^2-25\); c) \(4x^2+4x+1\).", r"Write as a perfect square or as sum times difference: a) \(x^2-14x+49\); b) \(x^2-25\); c) \(4x^2+4x+1\)."),
       P(r"a) \(x^2\) i \(49=7^2\) són quadrats i \(14x=2\cdot x\cdot7\), amb signe menys: \(\boxed{(x-7)^2}\).", r"a) \(x^2\) y \(49=7^2\) son cuadrados y \(14x=2\cdot x\cdot7\), con signo menos: \(\boxed{(x-7)^2}\).", r"a) \(x^2\) and \(49=7^2\) are squares and \(14x=2\cdot x\cdot7\), with a minus sign: \(\boxed{(x-7)^2}\)."),
       P(r"b) Diferència de quadrats: \(x^2-5^2=\boxed{(x+5)(x-5)}\).", r"b) Diferencia de cuadrados: \(x^2-5^2=\boxed{(x+5)(x-5)}\).", r"b) Difference of two squares: \(x^2-5^2=\boxed{(x+5)(x-5)}\)."),
       P(r"c) \(4x^2=(2x)^2\), \(1=1^2\) i \(4x=2\cdot2x\cdot1\): \(\boxed{(2x+1)^2}\).", r"c) \(4x^2=(2x)^2\), \(1=1^2\) y \(4x=2\cdot2x\cdot1\): \(\boxed{(2x+1)^2}\).", r"c) \(4x^2=(2x)^2\), \(1=1^2\) and \(4x=2\cdot2x\cdot1\): \(\boxed{(2x+1)^2}\)."))],
 [prob(L(r"Simplifica \(\ (x+3)^2-(x-3)^2-(2x+1)(2x-1)\).", r"Simplifica \(\ (x+3)^2-(x-3)^2-(2x+1)(2x-1)\).", r"Simplify \(\ (x+3)^2-(x-3)^2-(2x+1)(2x-1)\)."),
       D(r"(x^2+6x+9)-(x^2-6x+9)-(4x^2-1)"),
       P(r"Compte: cada resta canvia el signe de <strong>tots</strong> els termes del parèntesi:", r"Ojo: cada resta cambia el signo de <strong>todos</strong> los términos del paréntesis:", r"Careful: each subtraction changes the sign of <strong>every</strong> term in the bracket:"),
       D(r"x^2+6x+9-x^2+6x-9-4x^2+1=\boxed{-4x^2+12x+1}")),
  prob(L(r"Calcula de memòria fent servir les identitats notables: a) \(101^2\); b) \(49^2\); c) \(52\cdot48\).", r"Calcula de memoria usando las identidades notables: a) \(101^2\); b) \(49^2\); c) \(52\cdot48\).", r"Work out mentally with the special products: a) \(101^2\); b) \(49^2\); c) \(52\cdot48\)."),
       D(r"\text{a)}\ (100+1)^2=10\,000+200+1=\boxed{10\,201}"),
       D(r"\text{b)}\ (50-1)^2=2500-100+1=\boxed{2401}\qquad \text{c)}\ (50+2)(50-2)=2500-4=\boxed{2496}"))])
chk('(x+4)^2', 'x^2+8x+16'); chk('(x-6)^2', 'x^2-12x+36'); chk('(2x-5)^2', '4x^2-20x+25'); chk('(3x+y)^2', '9x^2+6xy+y^2'); chk('(x^2+4)(x^2-4)', 'x^4-16')
chk('(x-7)^2', 'x^2-14x+49'); chk('(x+5)(x-5)', 'x^2-25'); chk('(2x+1)^2', '4x^2+4x+1'); chk('(x+3)^2-(x-3)^2-(2x+1)(2x-1)', '-4x^2+12x+1')
chk('101**2', 10201); chk('49**2', 2401); chk('52*48', 2496)
s7 += practice([
  ('★', L(r"Desenvolupa: a) \((x+2)^2\); b) \((x-3)^2\); c) \((x+8)(x-8)\); d) \((a+b)^2\) per a \(a=5x,\ b=1\).", r"Desarrolla: a) \((x+2)^2\); b) \((x-3)^2\); c) \((x+8)(x-8)\); d) \((a+b)^2\) para \(a=5x,\ b=1\).", r"Expand: a) \((x+2)^2\); b) \((x-3)^2\); c) \((x+8)(x-8)\); d) \((a+b)^2\) with \(a=5x,\ b=1\).")),
  ('★★', L(r"e) \((3x-4)^2\); f) \((2x+5y)(2x-5y)\); g) \((x^2-2x)^2\). h) Escriu com a producte: \(x^2+10x+25\) i \(9x^2-1\).", r"e) \((3x-4)^2\); f) \((2x+5y)(2x-5y)\); g) \((x^2-2x)^2\). h) Escribe como producto: \(x^2+10x+25\) y \(9x^2-1\).", r"e) \((3x-4)^2\); f) \((2x+5y)(2x-5y)\); g) \((x^2-2x)^2\). h) Write as a product: \(x^2+10x+25\) and \(9x^2-1\).")),
  ('★★★', L(r"i) Simplifica \((2x-1)^2-(x+2)(x-2)+(x+1)^2\). j) Calcula \(99^2\) i \(61\cdot59\) sense calculadora.", r"i) Simplifica \((2x-1)^2-(x+2)(x-2)+(x+1)^2\). j) Calcula \(99^2\) y \(61\cdot59\) sin calculadora.", r"i) Simplify \((2x-1)^2-(x+2)(x-2)+(x+1)^2\). j) Work out \(99^2\) and \(61\cdot59\) without a calculator."))],
  D(r"\text{a)}\ x^2+4x+4\qquad \text{b)}\ x^2-6x+9\qquad \text{c)}\ x^2-64\qquad \text{d)}\ 25x^2+10x+1")
  + D(r"\text{e)}\ 9x^2-24x+16\qquad \text{f)}\ 4x^2-25y^2\qquad \text{g)}\ x^4-4x^3+4x^2\qquad \text{h)}\ (x+5)^2;\ \ (3x+1)(3x-1)")
  + D(r"\text{i)}\ 4x^2-4x+1-x^2+4+x^2+2x+1=4x^2-2x+6\qquad \text{j)}\ (100-1)^2=9801;\ \ (60+1)(60-1)=3599"))
chk('(x+2)^2', 'x^2+4x+4'); chk('(x-3)^2', 'x^2-6x+9'); chk('(x+8)(x-8)', 'x^2-64'); chk('(5x+1)^2', '25x^2+10x+1')
chk('(3x-4)^2', '9x^2-24x+16'); chk('(2x+5y)(2x-5y)', '4x^2-25y^2'); chk('(x^2-2x)^2', 'x^4-4x^3+4x^2'); chk('(x+5)^2', 'x^2+10x+25'); chk('(3x+1)(3x-1)', '9x^2-1')
chk('(2x-1)^2-(x+2)(x-2)+(x+1)^2', '4x^2-2x+6'); chk('99**2', 9801); chk('61*59', 3599)

# =====================================================================
# 3.8 Extracció de factor comú
# =====================================================================
s8 = box('def', L('Traure factor comú', 'Sacar factor común', 'Taking out a common factor'),
  P(r"<strong>Traure factor comú</strong> és aplicar la propietat distributiva <strong>al revés</strong>: si tots els termes d'un polinomi tenen un factor comú, l'escrivim fora d'un parèntesi.",
    r"<strong>Sacar factor común</strong> es aplicar la propiedad distributiva <strong>al revés</strong>: si todos los términos de un polinomio tienen un factor común, lo escribimos fuera de un paréntesis.",
    r"<strong>Taking out a common factor</strong> is using the distributive property <strong>backwards</strong>: if every term of a polynomial shares a factor, we write it outside a bracket.")
  + D(r"a\cdot b+a\cdot c=a\cdot(b+c)\qquad\qquad 12x^3-18x^2+6x=6x\,(2x^2-3x+1)")
  + P("Per a trobar el factor comú (el més gran possible):", "Para encontrar el factor común (el mayor posible):", "To find the (greatest) common factor:")
  + ol(L(r"<strong>Part numèrica</strong>: el MCD dels coeficients. \(\text{MCD}(12,18,6)=6\).", r"<strong>Parte numérica</strong>: el MCD de los coeficientes. \(\text{MCD}(12,18,6)=6\).", r"<strong>Number part</strong>: the gcd of the coefficients. \(\gcd(12,18,6)=6\)."),
       L(r"<strong>Part literal</strong>: les lletres que estan en <strong>tots</strong> els termes, amb el <strong>menor exponent</strong>. Ací, \(x\).", r"<strong>Parte literal</strong>: las letras que están en <strong>todos</strong> los términos, con el <strong>menor exponente</strong>. Aquí, \(x\).", r"<strong>Variable part</strong>: the letters in <strong>every</strong> term, with the <strong>lowest exponent</strong>. Here, \(x\)."),
       L(r"Dins del parèntesi escrivim el que queda en <strong>dividir cada terme</strong> entre el factor comú: \(12x^3:6x=2x^2\), \(\ -18x^2:6x=-3x\), \(\ 6x:6x=1\).", r"Dentro del paréntesis escribimos lo que queda al <strong>dividir cada término</strong> entre el factor común: \(12x^3:6x=2x^2\), \(\ -18x^2:6x=-3x\), \(\ 6x:6x=1\).", r"Inside the bracket write what's left after <strong>dividing each term</strong> by the common factor: \(12x^3:6x=2x^2\), \(\ -18x^2:6x=-3x\), \(\ 6x:6x=1\)."))
  + note(r"Quan un terme és igual al factor comú, dins del parèntesi queda un <strong>1</strong>, no un 0. Comprova sempre el resultat multiplicant: has de tornar a obtindre el polinomi inicial.",
         r"Cuando un término es igual al factor común, dentro del paréntesis queda un <strong>1</strong>, no un 0. Comprueba siempre el resultado multiplicando: tienes que volver a obtener el polinomio inicial.",
         r"When a term equals the common factor, a <strong>1</strong> is left in the bracket, not a 0. Always check by multiplying back: you must get the original polynomial.", '⚠'))
s8 += box('prop', L('Per a què serveix?', '¿Para qué sirve?', 'What is it for?'),
  ul(L(r"Per a <strong>calcular més ràpid</strong>: \(37\cdot15+37\cdot85=37\cdot(15+85)=37\cdot100=3700\).", r"Para <strong>calcular más rápido</strong>: \(37\cdot15+37\cdot85=37\cdot(15+85)=37\cdot100=3700\).", r"To <strong>calculate faster</strong>: \(37\cdot15+37\cdot85=37\cdot(15+85)=37\cdot100=3700\)."),
     L(r"Per a escriure un polinomi com a <strong>producte</strong> (<em>factoritzar-lo</em>), cosa molt útil per a simplificar fraccions i resoldre equacions en cursos següents.", r"Para escribir un polinomio como <strong>producto</strong> (<em>factorizarlo</em>), algo muy útil para simplificar fracciones y resolver ecuaciones en cursos siguientes.", r"To write a polynomial as a <strong>product</strong> (<em>factorise</em> it), very useful for simplifying fractions and solving equations in later years."),
     L(r"Combinat amb les identitats notables: \(2x^3-18x=2x(x^2-9)=2x(x+3)(x-3)\).", r"Combinado con las identidades notables: \(2x^3-18x=2x(x^2-9)=2x(x+3)(x-3)\).", r"Combined with the special products: \(2x^3-18x=2x(x^2-9)=2x(x+3)(x-3)\)."))
  + widget('w-fc', '🧲', L('Traure factor comú pas a pas', 'Sacar factor común paso a paso', 'Taking out a common factor step by step'),
           ['<div class="wrow">' + tin('p', 'P =', '12x^3-18x^2+6x') + '</div>', HELP,
            quick([('12x^3-18x^2+6x', '12x³−18x²+6x'), ('10x^2-15x', '10x²−15x'), ('4a^2b-6ab^2', '4a²b−6ab²'), ('x^4+x^3-x^2', 'x⁴+x³−x²'), ('2x^3-18x', '2x³−18x'), ('3x^2+12x+12', '3x²+12x+12'), ('3x^2+5y', '3x²+5y')])])
  + drill('fc', 'Entrena: el factor comú', 'Entrena: el factor común', 'Train: the common factor'))
chk('6x(2x^2-3x+1)', '12x^3-18x^2+6x'); chk('37*15+37*85', 3700); chk('2x(x+3)(x-3)', '2x^3-18x')
s8 += levels(
 [prob(L(r"Trau factor comú: a) \(5x+10\); b) \(x^2-7x\); c) \(9x^3+6x^2\).", r"Saca factor común: a) \(5x+10\); b) \(x^2-7x\); c) \(9x^3+6x^2\).", r"Take out the common factor: a) \(5x+10\); b) \(x^2-7x\); c) \(9x^3+6x^2\)."),
       D(r"\text{a)}\ \boxed{5(x+2)}\qquad \text{b)}\ \boxed{x(x-7)}\qquad \text{c)}\ \boxed{3x^2(3x+2)}"),
       P(r"En c): \(\text{MCD}(9,6)=3\) i la \(x\) amb l'exponent més xicotet, \(x^2\).", r"En c): \(\text{MCD}(9,6)=3\) y la \(x\) con el exponente más pequeño, \(x^2\).", r"In c): \(\gcd(9,6)=3\) and \(x\) with the lowest exponent, \(x^2\).")),
  prob(L(r"Calcula de la manera més ràpida: \(\ 23\cdot47+23\cdot53\).", r"Calcula de la manera más rápida: \(\ 23\cdot47+23\cdot53\).", r"Work out the quickest way: \(\ 23\cdot47+23\cdot53\)."),
       D(r"23\cdot(47+53)=23\cdot100=\boxed{2300}"))],
 [prob(L(r"Trau factor comú: a) \(8a^2b-12ab^2\); b) \(x^5-3x^4+x^2\); c) \(-6x^3-9x\).", r"Saca factor común: a) \(8a^2b-12ab^2\); b) \(x^5-3x^4+x^2\); c) \(-6x^3-9x\).", r"Take out the common factor: a) \(8a^2b-12ab^2\); b) \(x^5-3x^4+x^2\); c) \(-6x^3-9x\)."),
       D(r"\text{a)}\ \boxed{4ab(2a-3b)}\qquad \text{b)}\ \boxed{x^2(x^3-3x^2+1)}\qquad \text{c)}\ \boxed{-3x(2x^2+3)}"),
       P(r"En c) també és correcte \(3x(-2x^2-3)\), però quan el primer terme és negatiu sol traure's el signe menys fora.", r"En c) también es correcto \(3x(-2x^2-3)\), pero cuando el primer término es negativo se suele sacar el signo menos fuera.", r"In c) \(3x(-2x^2-3)\) is also correct, but when the first term is negative we usually take the minus sign out."))],
 [prob(L(r"Factoritza tant com pugues (factor comú i, després, identitats notables): a) \(3x^3-12x\); b) \(5x^3+10x^2+5x\).", r"Factoriza tanto como puedas (factor común y, después, identidades notables): a) \(3x^3-12x\); b) \(5x^3+10x^2+5x\).", r"Factorise as far as you can (common factor, then special products): a) \(3x^3-12x\); b) \(5x^3+10x^2+5x\)."),
       D(r"\text{a)}\ 3x(x^2-4)=\boxed{3x(x+2)(x-2)}"),
       D(r"\text{b)}\ 5x(x^2+2x+1)=\boxed{5x(x+1)^2}")),
  prob(L(r"Trau factor comú: \(\ 2x(x-3)+5(x-3)\).", r"Saca factor común: \(\ 2x(x-3)+5(x-3)\).", r"Take out the common factor: \(\ 2x(x-3)+5(x-3)\)."),
       P(r"El factor comú pot ser un <strong>binomi</strong> sencer: tots dos termes tenen \((x-3)\).", r"El factor común puede ser un <strong>binomio</strong> entero: los dos términos tienen \((x-3)\).", r"The common factor can be a whole <strong>binomial</strong>: both terms contain \((x-3)\)."),
       D(r"2x(x-3)+5(x-3)=\boxed{(x-3)(2x+5)}"))])
chk('5(x+2)', '5x+10'); chk('x(x-7)', 'x^2-7x'); chk('3x^2(3x+2)', '9x^3+6x^2'); chk('23*100', 2300); chk('23*47+23*53', 2300)
chk('4a*b*(2a-3b)', '8a^2b-12ab^2'); chk('x^2(x^3-3x^2+1)', 'x^5-3x^4+x^2'); chk('-3x(2x^2+3)', '-6x^3-9x')
chk('3x(x+2)(x-2)', '3x^3-12x'); chk('5x(x+1)^2', '5x^3+10x^2+5x'); chk('(x-3)(2x+5)', '2x(x-3)+5(x-3)')
s8 += practice([
  ('★', L(r"Trau factor comú: a) \(4x-12\); b) \(x^3+5x^2\); c) \(14x^2-21x\); d) \(6x^4-2x^3+8x^2\).", r"Saca factor común: a) \(4x-12\); b) \(x^3+5x^2\); c) \(14x^2-21x\); d) \(6x^4-2x^3+8x^2\).", r"Take out the common factor: a) \(4x-12\); b) \(x^3+5x^2\); c) \(14x^2-21x\); d) \(6x^4-2x^3+8x^2\).")),
  ('★★', L(r"e) \(15a^3b^2-10a^2b^3+5a^2b^2\); f) \(-x^3+x^2-x\). g) Calcula \(17\cdot64+17\cdot36\) de manera ràpida.", r"e) \(15a^3b^2-10a^2b^3+5a^2b^2\); f) \(-x^3+x^2-x\). g) Calcula \(17\cdot64+17\cdot36\) de manera rápida.", r"e) \(15a^3b^2-10a^2b^3+5a^2b^2\); f) \(-x^3+x^2-x\). g) Work out \(17\cdot64+17\cdot36\) quickly.")),
  ('★★★', L(r"Factoritza: h) \(2x^3-50x\); i) \(x^4-6x^3+9x^2\); j) \(x(x+4)-3(x+4)\).", r"Factoriza: h) \(2x^3-50x\); i) \(x^4-6x^3+9x^2\); j) \(x(x+4)-3(x+4)\).", r"Factorise: h) \(2x^3-50x\); i) \(x^4-6x^3+9x^2\); j) \(x(x+4)-3(x+4)\)."))],
  D(r"\text{a)}\ 4(x-3)\qquad \text{b)}\ x^2(x+5)\qquad \text{c)}\ 7x(2x-3)\qquad \text{d)}\ 2x^2(3x^2-x+4)")
  + D(r"\text{e)}\ 5a^2b^2(3a-2b+1)\qquad \text{f)}\ -x(x^2-x+1)\qquad \text{g)}\ 17\cdot100=1700")
  + D(r"\text{h)}\ 2x(x+5)(x-5)\qquad \text{i)}\ x^2(x-3)^2\qquad \text{j)}\ (x+4)(x-3)"))
chk('4(x-3)', '4x-12'); chk('x^2(x+5)', 'x^3+5x^2'); chk('7x(2x-3)', '14x^2-21x'); chk('2x^2(3x^2-x+4)', '6x^4-2x^3+8x^2')
chk('5a^2b^2(3a-2b+1)', '15a^3b^2-10a^2b^3+5a^2b^2'); chk('-x(x^2-x+1)', '-x^3+x^2-x'); chk('17*64+17*36', 1700)
chk('2x(x+5)(x-5)', '2x^3-50x'); chk('x^2(x-3)^2', 'x^4-6x^3+9x^2'); chk('(x+4)(x-3)', 'x(x+4)-3(x+4)')
