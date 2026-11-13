# Genera t1-fitxa-exercicis.tex i t1-fitxa-solucions.tex (4t ESO Matemàtiques B, Unitat 1: Nombres reals)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Les solucions de fraccions i intervals es calculen ací (aritmètica exacta) i les de radicals i logaritmes
# es comproven amb eq() (sympy, numèricament). Les solucions d'intervals porten la recta dibuixada amb TikZ.
# Ús: python3 genera.py && pdflatex t1-fitxa-exercicis.tex (dues vegades) && pdflatex t1-fitxa-solucions.tex (dues vegades)
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

S = []

# =====================================================================
# 1. Classificació dels nombres
g = [per('0', '', '7'), per('2', '', '45'), per('1', '3', '6'), per('0', '12', '5'), per('3', '', '9')]
ck(g, [F(7, 9), F(27, 11), F(41, 30), F(113, 900), F(4)])
S.append(("Classificació dels nombres", [
 (1, r"Indica el menor conjunt numèric ($\mathbb N$, $\mathbb Z$, $\mathbb Q$ o $\mathbb I$) al qual pertany cada nombre:"
     + tasks(5, [r"$\sqrt{36}$", r"$-7$", r"$\frac35$", r"$\sqrt7$", r"$0,25$", r"$-\sqrt9$", r"$2,\widehat3$", r"$\pi$", r"$\frac{12}{4}$", r"$-\frac{18}{6}$"]),
     tasks(5, [R(r"6\in\mathbb N"), R(r"\mathbb Z"), R(r"\mathbb Q"), R(r"\mathbb I"), R(r"\mathbb Q"), R(r"-3\in\mathbb Z"), R(r"\mathbb Q"), R(r"\mathbb I"), R(r"3\in\mathbb N"), R(r"-3\in\mathbb Z")])),
 (1, r"Indica si els nombres següents són racionals o irracionals. Justifica-ho:"
     + tasks(3, [r"$1,212121\ldots$", r"$1,2122122212222\ldots$", r"$\sqrt{\frac{16}{9}}$", r"$\sqrt{20}$", r"$\frac{\pi}{4}$", r"$\sqrt{0,25}$"]),
     tasks(2, [R(r"\mathbb Q") + r": és periòdic pur ($1,\widehat{21}$).", R(r"\mathbb I") + r": infinites xifres sense període.", R(r"\mathbb Q") + r": és $\frac43$.",
               R(r"\mathbb I") + r": 20 no és un quadrat perfecte.", R(r"\mathbb I") + r": $\pi$ és irracional.", R(r"\mathbb Q") + r": és $0,5=\frac12$."])),
 (2, r"Troba la fracció generatriu i simplifica-la:" + tasks(5, [r"$0,\widehat7$", r"$2,\widehat{45}$", r"$1,3\widehat6$", r"$0,12\widehat5$", r"$3,\widehat9$"])
     + recorda(r"Al numerador, el nombre sense coma menys la part no periòdica; al denominador, tants 9 com xifres té el període i tants 0 com xifres té l'anteperíode."),
     tasks(5, [R(tn(x)) for x in g]) + r"Fixa't: $3,\widehat9=4$."),
 (2, r"Raona si les afirmacions següents són verdaderes o falses:" + tasks(1, [r"Tot nombre enter és racional.", r"Tot nombre decimal es pot escriure com una fracció.",
      r"L'arrel quadrada d'un nombre natural sempre és irracional.", r"La suma d'un racional i un irracional és irracional.", r"$\sqrt{-16}$ és un nombre enter."]),
     tasks(1, [r"\rest{Verdadera}: tot enter $n$ és $\frac n1$.", r"\rest{Falsa}: només els exactes i els periòdics; $\pi=3,1415\ldots$ no.",
               r"\rest{Falsa}: $\sqrt{49}=7$ és natural. Només és irracional si el nombre no és un quadrat perfecte.",
               r"\rest{Verdadera}: per exemple, $1+\sqrt2$ té infinites xifres no periòdiques.", r"\rest{Falsa}: no és un nombre real (cap nombre al quadrat dona $-16$)."])),
]))

# =====================================================================
# 2. Intervals i semirectes
S.append(("Intervals i semirectes", [
 (1, r"Completa la taula:" + '\n\n\\begin{center}\\renewcommand{\\arraystretch}{1.5}\\begin{tabular}{|C{4.6cm}|C{3.2cm}|C{6cm}|}\\hline\\rowcolor{soft}\\textbf{Desigualtat} & \\textbf{Interval} & \\textbf{Representació}\\\\\\hline'
     r'$-1\le x<4$ & & \\\hline & $(-\infty, 2]$ & \\\hline $x>-3$ & & \\\hline & $(0, 5)$ & \\\hline $x<1$ & & \\\hline\end{tabular}\end{center}',
     tasks(2, [r"$-1\le x<4$: " + RI('[-1,4)'), r"$x\le2$: " + RI('(-inf,2]'), r"$x>-3$: " + RI('(-3,inf)'), r"$0<x<5$: " + RI('(0,5)'), r"$x<1$: " + RI('(-inf,1)')])),
 (1, r"Escriu com a interval o semirecta i representa:" + tasks(3, [r"$x>2$", r"$-1\le x\le4$", r"$x\le-3$", r"$0<x<5$", r"$-2\le x<3$", r"$x\ge\frac12$"]),
     tasks(2, [RI('(2,inf)'), RI('[-1,4]'), RI('(-inf,-3]'), RI('(0,5)'), RI('[-2,3)'), RI('[1/2,inf)')])),
 (1, r"Escriu la desigualtat que compleixen els nombres de cada interval i representa'l:" + tasks(4, [r"$[-3, 1)$", r"$(-\infty, 2]$", r"$(4, +\infty)$", r"$(-5, 0)$"]),
     tasks(2, [r"$-3\le x<1$ " + recta(P('[-3,1)')), r"$x\le2$ " + recta(P('(-inf,2]')), r"$x>4$ " + recta(P('(4,inf)')), r"$-5<x<0$ " + recta(P('(-5,0)'))])),
 (2, r"Escriu com a interval o semirecta:" + tasks(1, [r"Els nombres més grans que $-2$ i, com a màxim, iguals a 6.", r"Els nombres reals positius.", r"Els nombres reals no negatius.",
      r"Els nombres que estan entre 1 i 5, amb el 5 inclòs.", r"Els nombres la distància dels quals al 0 és menor que 3."]),
     tasks(1, [R(r"(-2, 6]"), R(r"(0, +\infty)"), R(r"[0, +\infty)") + r" (el 0 no és negatiu)", R(r"(1, 5]"), R(r"(-3, 3)")])),
]))

# =====================================================================
# 3. Unió i intersecció d'intervals
A, B, C, D = P('[-3,2]'), P('(0,5]'), P('[4,inf)'), P('(-inf,1)')
r9 = [cup(A, B), cap(A, B), cap(B, C), cap(A, C), cup(A, D), cap(B, D), cup(C, D), cap(A, D)]
ck(r9, [P('[-3,5]'), P('(0,2]'), P('[4,5]'), [], P('(-inf,2]'), P('(0,1)'), P('(-inf,1)U[4,inf)'), P('[-3,1)')])
E, G = P('(-inf,3]'), P('(-1,6)')
H, K = P('[2,inf)'), P('(-inf,2)')
r10 = [cup(E, G), cap(E, G), cup(H, K), cap(H, K)]
ck(r10, [P('(-inf,6)'), P('(-1,3]'), P('(-inf,inf)'), []])
S.append(("Unió i intersecció d'intervals", [
 (2, r"Donats els intervals $A=[-3, 2]$, $B=(0, 5]$, $C=[4, +\infty)$ i $D=(-\infty, 1)$, calcula i representa:"
     + tasks(4, [r"$A\cup B$", r"$A\cap B$", r"$B\cap C$", r"$A\cap C$", r"$A\cup D$", r"$B\cap D$", r"$C\cup D$", r"$A\cap D$"])
     + recorda(r"La unió $\cup$ són els nombres que estan en algun dels dos; la intersecció $\cap$, els que estan en tots dos alhora."),
     tasks(2, [RI(x, -4, 6) if x else R(r"\varnothing") for x in r9])),
 (2, r"Calcula $E\cup G$ i $E\cap G$, amb $E=(-\infty, 3]$ i $G=(-1, 6)$. Després fes el mateix amb $H=[2, +\infty)$ i $K=(-\infty, 2)$. Què observes?",
     tasks(2, [r"$E\cup G=$ " + RI(r10[0]), r"$E\cap G=$ " + RI(r10[1]), r"$H\cup K=" + Rm(r"\mathbb R") + "$", r"$H\cap K=" + Rm(r"\varnothing") + "$"])
     + r"$H$ i $K$ es toquen en el 2 sense solapar-se: entre les dues cobreixen tota la recta, però no tenen cap nombre en comú."),
 (1, r"Escriu en forma d'interval els nombres que compleixen alhora les dues desigualtats:" + tasks(4, [r"$x<3$ i $x\ge5$", r"$x>0$ i $x<4$", r"$x\le-1$ i $x>-6$", r"$x<3$ i $x\ge-2$"]),
     tasks(4, [R(r"\varnothing"), R(st(P('(0,4)'))), R(st(P('(-6,-1]'))), R(st(P('[-2,3)')))])),
]))

# =====================================================================
# 4. Radicals
for a_, b_ in [('8**(Rational(2,3))', 4), ('16**(Rational(3,4))', 8), ('27**(Rational(-1,3))', 'Rational(1,3)'), ('25**(Rational(1,2))', 5), ('real_root(-27,3)', -3),
               ('root(16,4)', 2), ('root(32,5)', 2), ('root(Rational(8,27),3)', 'Rational(2,3)'), ('sqrt(Rational(9,100))', 'Rational(3,10)')]:
    eq(a_, b_)
rad16 = [('sqrt(12)', '2*sqrt(3)'), ('sqrt(50)', '5*sqrt(2)'), ('sqrt(98)', '7*sqrt(2)'), ('root(24,3)', '2*root(3,3)'), ('root(250,3)', '5*root(2,3)'),
         ('root(32,4)', '2*root(2,4)'), ('sqrt(18*a**3)', '3*a*sqrt(2*a)'), ('root(16*x**5*y**3,3)', '2*x*y*root(2*x**2,3)'), ('sqrt(Rational(75,4))', '5*sqrt(3)/2')]
for a_, b_ in rad16: eq(a_, b_)
for a_, b_ in [('2*sqrt(3)', 'sqrt(12)'), ('3*sqrt(2)', 'sqrt(18)'), ('2*root(5,3)', 'root(40,3)'), ('a*sqrt(a)', 'sqrt(a**3)'), ('2*x*root(x,3)', 'root(8*x**4,3)'), ('sqrt(8)/2', 'sqrt(2)')]: eq(a_, b_)
sums = [('sqrt(12)+sqrt(27)', '5*sqrt(3)'), ('sqrt(50)-sqrt(18)+sqrt(8)', '4*sqrt(2)'), ('2*sqrt(45)-3*sqrt(20)+sqrt(5)', 'sqrt(5)'), ('root(16,3)+root(54,3)-root(2,3)', '4*root(2,3)'),
        ('3*sqrt(8)-2*sqrt(32)+sqrt(72)', '4*sqrt(2)'), ('sqrt(75)-2*sqrt(12)-sqrt(27)', '-2*sqrt(3)'), ('5*sqrt(a)-sqrt(4*a)+sqrt(9*a)', '6*sqrt(a)'), ('root(81,3)-2*root(24,3)+root(375,3)', '4*root(3,3)')]
for a_, b_ in sums: eq(a_, b_)
prods = [('sqrt(2)*sqrt(8)', 4), ('sqrt(3)*sqrt(6)', '3*sqrt(2)'), ('root(4,3)*root(2,3)', 2), ('sqrt(10)/sqrt(2)', 'sqrt(5)'), ('root(54,3)/root(2,3)', 3),
         ('2*sqrt(3)*5*sqrt(6)', '30*sqrt(2)'), ('sqrt(2)*root(2,3)', 'root(32,6)'), ('sqrt(3)/root(3,4)', 'root(3,4)')]
for a_, b_ in prods: eq(a_, b_)
pots = [('sqrt(3)**4', 9), ('root(2,3)**6', 4), ('(2*sqrt(5))**2', 20), ('sqrt(2)**5', '4*sqrt(2)'), ('root(4,3)**2', '2*root(2,3)'), ('root(8,4)**2', '2*sqrt(2)')]
for a_, b_ in pots: eq(a_, b_)
for a_, b_ in [('sqrt(sqrt(5))', 'root(5,4)'), ('root(sqrt(2),3)', 'root(2,6)'), ('sqrt(2*sqrt(2))', 'root(8,4)'), ('sqrt(3*root(3,3))', 'root(9,3)')]: eq(a_, b_)
comb = [('(sqrt(3)+sqrt(2))**2', '5+2*sqrt(6)'), ('(sqrt(5)+1)*(sqrt(5)-1)', 4), ('(2*sqrt(3)-1)**2', '13-4*sqrt(3)'), ('sqrt(2)*(sqrt(8)-sqrt(18))', -2), ('(3+sqrt(2))*(1-sqrt(2))', '1-2*sqrt(2)')]
for a_, b_ in comb: eq(a_, b_)
eq('root(3,2)', 'root(27,6)'); eq('root(2,3)', 'root(4,6)'); eq('sqrt(2)', 'root(2**6,12)'); eq('root(5,4)', 'root(5**3,12)'); eq('root(3,3)', 'root(3**4,12)')
assert 3 ** 3 > 5 ** 2  # √3 > ∛5
S.append(("Radicals", [
 (1, r"Escriu en forma de potència:" + tasks(4, [r"$\sqrt5$", r"$\sqrt[3]{7^2}$", r"$\sqrt[5]{x^3}$", r"$\dfrac{1}{\sqrt3}$"]) + r"I en forma de radical:" + tasks(4, [r"$3^{\frac12}$", r"$5^{\frac23}$", r"$a^{\frac34}$", r"$2^{-\frac12}$"], start=5)
     + recorda(r"$\sqrt[n]{a^m}=a^{\frac mn}$: l'exponent va al numerador i l'índex al denominador."),
     tasks(4, [R(r"5^{\frac12}"), R(r"7^{\frac23}"), R(r"x^{\frac35}"), R(r"3^{-\frac12}"), R(r"\sqrt3"), R(r"\sqrt[3]{25}"), R(r"\sqrt[4]{a^3}"), R(r"\dfrac{1}{\sqrt2}")])),
 (1, r"Calcula sense calculadora:" + tasks(5, [r"$\sqrt[3]{-27}$", r"$\sqrt[4]{16}$", r"$\sqrt[5]{32}$", r"$\sqrt[3]{\frac{8}{27}}$", r"$\sqrt{0,09}$", r"$8^{\frac23}$", r"$16^{\frac34}$", r"$27^{-\frac13}$", r"$25^{\frac12}$", r"$\sqrt{-25}$"]),
     tasks(5, [R("-3"), R("2"), R("2"), R(r"\frac23"), R("0,3"), R("4"), R("8"), R(r"\frac13"), R("5"), r"No és real."])),
 (1, r"Simplifica els radicals següents:" + tasks(3, [r"$\sqrt[6]{8}$", r"$\sqrt[9]{27}$", r"$\sqrt[4]{25}$", r"$\sqrt[12]{a^8}$", r"$\sqrt[10]{x^4y^6}$", r"$\sqrt[8]{16}$"]),
     tasks(3, [R(r"\sqrt2"), R(r"\sqrt[3]3"), R(r"\sqrt5"), R(r"\sqrt[3]{a^2}"), R(r"\sqrt[5]{x^2y^3}"), R(r"\sqrt2")])),
 (2, r"Redueix a índex comú i ordena de menor a major:" + tasks(2, [r"$\sqrt3$ i $\sqrt[3]5$", r"$\sqrt2$, $\sqrt[4]5$ i $\sqrt[3]3$"]),
     tasks(1, [r"$\sqrt[6]{27}$ i $\sqrt[6]{25}$, per tant " + R(r"\sqrt[3]5<\sqrt3"), r"$\sqrt[12]{64}$, $\sqrt[12]{125}$ i $\sqrt[12]{81}$, per tant " + R(r"\sqrt2<\sqrt[3]3<\sqrt[4]5")])),
 (2, r"Extrau tots els factors possibles:" + tasks(3, [r"$\sqrt{12}$", r"$\sqrt{50}$", r"$\sqrt{98}$", r"$\sqrt[3]{24}$", r"$\sqrt[3]{250}$", r"$\sqrt[4]{32}$", r"$\sqrt{18a^3}$", r"$\sqrt[3]{16x^5y^3}$", r"$\sqrt{\frac{75}{4}}$"]),
     tasks(3, [R(r"2\sqrt3"), R(r"5\sqrt2"), R(r"7\sqrt2"), R(r"2\sqrt[3]3"), R(r"5\sqrt[3]2"), R(r"2\sqrt[4]2"), R(r"3a\sqrt{2a}"), R(r"2xy\sqrt[3]{2x^2}"), R(r"\frac{5\sqrt3}{2}")])),
 (1, r"Introdueix dins del radical el factor de fora:" + tasks(3, [r"$2\sqrt3$", r"$3\sqrt2$", r"$2\sqrt[3]5$", r"$a\sqrt a$", r"$2x\sqrt[3]x$", r"$\frac12\sqrt8$"]),
     tasks(3, [R(r"\sqrt{12}"), R(r"\sqrt{18}"), R(r"\sqrt[3]{40}"), R(r"\sqrt{a^3}"), R(r"\sqrt[3]{8x^4}"), R(r"\sqrt{\frac{8}{4}}=\sqrt2")])),
 (2, r"Fes les sumes i restes:" + tasks(2, [r"$\sqrt{12}+\sqrt{27}$", r"$\sqrt{50}-\sqrt{18}+\sqrt8$", r"$2\sqrt{45}-3\sqrt{20}+\sqrt5$", r"$\sqrt[3]{16}+\sqrt[3]{54}-\sqrt[3]2$",
      r"$3\sqrt8-2\sqrt{32}+\sqrt{72}$", r"$\sqrt{75}-2\sqrt{12}-\sqrt{27}$", r"$5\sqrt a-\sqrt{4a}+\sqrt{9a}$", r"$\sqrt[3]{81}-2\sqrt[3]{24}+\sqrt[3]{375}$"])
     + recorda(r"Només es poden sumar radicals semblants (mateix índex i mateix radicand). Extrau factors abans!"),
     tasks(4, [R(r"5\sqrt3"), R(r"4\sqrt2"), R(r"\sqrt5"), R(r"4\sqrt[3]2"), R(r"4\sqrt2"), R(r"-2\sqrt3"), R(r"6\sqrt a"), R(r"4\sqrt[3]3")])),
 (2, r"Calcula i simplifica:" + tasks(4, [r"$\sqrt2\cdot\sqrt8$", r"$\sqrt3\cdot\sqrt6$", r"$\sqrt[3]4\cdot\sqrt[3]2$", r"$\sqrt{10}:\sqrt2$", r"$\sqrt[3]{54}:\sqrt[3]2$", r"$2\sqrt3\cdot5\sqrt6$", r"$\sqrt2\cdot\sqrt[3]2$", r"$\sqrt3:\sqrt[4]3$"]),
     tasks(4, [R("4"), R(r"3\sqrt2"), R("2"), R(r"\sqrt5"), R("3"), R(r"30\sqrt2"), R(r"\sqrt[6]{32}"), R(r"\sqrt[4]3")])),
 (2, r"Calcula les potències i expressa com un sol radical:" + tasks(3, [r"$(\sqrt3)^4$", r"$(\sqrt[3]2)^6$", r"$(2\sqrt5)^2$", r"$(\sqrt2)^5$", r"$(\sqrt[3]4)^2$", r"$(\sqrt[4]8)^2$"])
     + tasks(4, [r"$\sqrt{\sqrt5}$", r"$\sqrt[3]{\sqrt2}$", r"$\sqrt{2\sqrt2}$", r"$\sqrt{3\sqrt[3]3}$"], start=7),
     tasks(3, [R("9"), R("4"), R("20"), R(r"4\sqrt2"), R(r"2\sqrt[3]2"), R(r"2\sqrt2")]) + tasks(4, [R(r"\sqrt[4]5"), R(r"\sqrt[6]2"), R(r"\sqrt[4]8"), R(r"\sqrt[3]9")], start=7)),
 (3, r"Opera i simplifica:" + tasks(2, [r"$(\sqrt3+\sqrt2)^2$", r"$(\sqrt5+1)(\sqrt5-1)$", r"$(2\sqrt3-1)^2$", r"$\sqrt2\left(\sqrt8-\sqrt{18}\right)$", r"$(3+\sqrt2)(1-\sqrt2)$"]),
     tasks(3, [R(r"5+2\sqrt6"), R("4"), R(r"13-4\sqrt3"), R("-2"), R(r"1-2\sqrt2")])),
]))

# =====================================================================
# 5. Racionalització
rac1 = [('1/sqrt(2)', 'sqrt(2)/2'), ('6/sqrt(3)', '2*sqrt(3)'), ('5/(2*sqrt(5))', 'sqrt(5)/2'), ('sqrt(2)/sqrt(6)', 'sqrt(3)/3'), ('3/(4*sqrt(6))', 'sqrt(6)/8'), ('10/sqrt(50)', 'sqrt(2)')]
rac2 = [('2/root(2,3)', 'root(4,3)'), ('6/root(9,3)', '2*root(3,3)'), ('1/root(8,4)', 'root(2,4)/2'), ('10/root(4,5)', '5*root(8,5)')]
rac3 = [('1/(sqrt(3)-1)', '(sqrt(3)+1)/2'), ('4/(3+sqrt(5))', '3-sqrt(5)'), ('sqrt(2)/(sqrt(2)+1)', '2-sqrt(2)'), ('(1+sqrt(2))/(1-sqrt(2))', '-3-2*sqrt(2)'),
        ('6/(sqrt(5)-sqrt(2))', '2*(sqrt(5)+sqrt(2))'), ('(sqrt(3)+sqrt(2))/(sqrt(3)-sqrt(2))', '5+2*sqrt(6)')]
for a_, b_ in rac1 + rac2 + rac3: eq(a_, b_)
eq('1/(sqrt(2)-1)-1/(sqrt(2)+1)', 2); eq('2/sqrt(2)+3/(sqrt(2)+1)', '4*sqrt(2)-3')
S.append(("Racionalització", [
 (1, r"Racionalitza:" + tasks(3, [r"$\dfrac{1}{\sqrt2}$", r"$\dfrac{6}{\sqrt3}$", r"$\dfrac{5}{2\sqrt5}$", r"$\dfrac{\sqrt2}{\sqrt6}$", r"$\dfrac{3}{4\sqrt6}$", r"$\dfrac{10}{\sqrt{50}}$"]),
     tasks(3, [R(r"\dfrac{\sqrt2}{2}"), R(r"2\sqrt3"), R(r"\dfrac{\sqrt5}{2}"), R(r"\dfrac{\sqrt3}{3}"), R(r"\dfrac{\sqrt6}{8}"), R(r"\sqrt2")])),
 (2, r"Racionalitza:" + tasks(4, [r"$\dfrac{2}{\sqrt[3]2}$", r"$\dfrac{6}{\sqrt[3]9}$", r"$\dfrac{1}{\sqrt[4]8}$", r"$\dfrac{10}{\sqrt[5]4}$"])
     + recorda(r"Per a $\sqrt[n]{b^m}$, multipliquem dalt i baix per $\sqrt[n]{b^{\,n-m}}$, perquè l'exponent arribe a l'índex."),
     tasks(4, [R(r"\sqrt[3]4"), R(r"2\sqrt[3]3"), R(r"\dfrac{\sqrt[4]2}{2}"), R(r"5\sqrt[5]8")])),
 (2, r"Racionalitza multiplicant pel conjugat:" + tasks(3, [r"$\dfrac{1}{\sqrt3-1}$", r"$\dfrac{4}{3+\sqrt5}$", r"$\dfrac{\sqrt2}{\sqrt2+1}$", r"$\dfrac{1+\sqrt2}{1-\sqrt2}$", r"$\dfrac{6}{\sqrt5-\sqrt2}$", r"$\dfrac{\sqrt3+\sqrt2}{\sqrt3-\sqrt2}$"])
     + recorda(r"$(a+b)(a-b)=a^2-b^2$."),
     tasks(3, [R(r"\dfrac{\sqrt3+1}{2}"), R(r"3-\sqrt5"), R(r"2-\sqrt2"), R(r"-3-2\sqrt2"), R(r"2\left(\sqrt5+\sqrt2\right)"), R(r"5+2\sqrt6")])),
 (3, r"Racionalitza i opera:" + tasks(2, [r"$\dfrac{1}{\sqrt2-1}-\dfrac{1}{\sqrt2+1}$", r"$\dfrac{2}{\sqrt2}+\dfrac{3}{\sqrt2+1}$"]),
     tasks(2, [r"$(\sqrt2+1)-(\sqrt2-1)=" + Rm("2") + "$", r"$\sqrt2+3(\sqrt2-1)=" + Rm(r"4\sqrt2-3") + "$"])),
]))

# =====================================================================
# 6. Logaritmes
L1 = [('log(32,2)', 5), ('log(81,3)', 4), ('log(10000,10)', 4), ('log(Rational(1,1000),10)', -3), ('log(Rational(1,25),5)', -2), ('log(Rational(1,8),2)', -3), ('log(exp(4))', 4), ('log(1/E)', -1), ('log(7,7)', 1), ('log(1,9)', 0)]
L2 = [('log(sqrt(2),2)', 'Rational(1,2)'), ('log(root(3,3),3)', 'Rational(1,3)'), ('log(8,4)', 'Rational(3,2)'), ('log(4,Rational(1,2))', -2), ('log(2,8)', 'Rational(1,3)'), ('log(sqrt(125),5)', 'Rational(3,2)'), ('log(Rational(1,10),10)', -1), ('log(9,sqrt(3))', 4)]
for a_, b_ in L1 + L2: eq(a_, b_)
L4 = [('log(2,6)+log(3,6)', 1), ('log(24,2)-log(3,2)', 3), ('log(25,10)+log(4,10)', 2), ('log(18,3)-log(2,3)', 2), ('log(16**3,2)', 12), ('log(125,5)+log(5,5)-log(25,5)', 2)]
for a_, b_ in L4: eq(a_, b_)
l2, l3 = 0.301, 0.477
L5 = [l2 + l3, 3 * l2, 1 - l2, l2 + 2 * l3, l3 - l2, (2 * l2 + l3) / 2, l2 - 1, 3 * l3]
ck([round(x, 4) for x in L5], [0.778, 0.903, 0.699, 1.255, 0.176, 0.5395, -0.699, 1.431])
calc = [math.log10(50), math.log(7), math.log10(0.35), math.log(0.5), math.log(15, 3), math.log(100, 2), math.log(2, 7), math.log(0.2, 5)]
ck([round(x, 3) for x in calc], [1.699, 1.946, -0.456, -0.693, 2.465, 6.644, 0.356, -1.0])
S.append(("Logaritmes", [
 (1, r"Aplicant la definició, calcula:" + tasks(5, [r"$\log_2 32$", r"$\log_3 81$", r"$\log 10\,000$", r"$\log 0,001$", r"$\log_5\frac{1}{25}$", r"$\log_2\frac18$", r"$\ln e^4$", r"$\ln\frac1e$", r"$\log_7 7$", r"$\log_9 1$"])
     + recorda(r"$\log_a b=c\iff a^c=b$. A més, $\log_a a=1$ i $\log_a 1=0$."),
     tasks(5, [R("5"), R("4"), R("4"), R("-3"), R("-2"), R("-3"), R("4"), R("-1"), R("1"), R("0")])),
 (2, r"Aplicant la definició, calcula:" + tasks(4, [r"$\log_2\sqrt2$", r"$\log_3\sqrt[3]3$", r"$\log_4 8$", r"$\log_{\frac12}4$", r"$\log_8 2$", r"$\log_5\sqrt{125}$", r"$\log 0,1$", r"$\log_{\sqrt3}9$"]),
     tasks(4, [R(r"\frac12"), R(r"\frac13"), R(r"\frac32"), R("-2"), R(r"\frac13"), R(r"\frac32"), R("-1"), R("4")])),
 (2, r"Troba el valor de $x$:" + tasks(3, [r"$\log_x 49=2$", r"$\log_2 x=5$", r"$\log_3 x=-2$", r"$\log_x\frac18=-3$", r"$\log_5 x=0$", r"$\log x=-2$"]),
     tasks(3, [R("x=7"), R("x=32"), R(r"x=\frac19"), R("x=2"), R("x=1"), R("x=0,01")])),
 (1, r"Calcula aplicant les propietats dels logaritmes:" + tasks(3, [r"$\log_6 2+\log_6 3$", r"$\log_2 24-\log_2 3$", r"$\log 25+\log 4$", r"$\log_3 18-\log_3 2$", r"$\log_2 16^3$", r"$\log_5 125+\log_5 5-\log_5 25$"]),
     tasks(3, [r"$\log_6 6=" + Rm("1") + "$", r"$\log_2 8=" + Rm("3") + "$", r"$\log100=" + Rm("2") + "$", r"$\log_3 9=" + Rm("2") + "$", r"$3\cdot4=" + Rm("12") + "$", r"$3+1-2=" + Rm("2") + "$"])),
 (2, r"Sabent que $\log2=0,301$ i $\log3=0,477$, calcula sense calculadora:" + tasks(4, [r"$\log6$", r"$\log8$", r"$\log5$", r"$\log18$", r"$\log1,5$", r"$\log\sqrt{12}$", r"$\log0,2$", r"$\log27$"]),
     tasks(2, [r"$\log2+\log3=" + Rm(dec(L5[0])) + "$", r"$3\log2=" + Rm(dec(L5[1])) + "$", r"$\log\frac{10}2=1-\log2=" + Rm(dec(L5[2])) + "$", r"$\log2+2\log3=" + Rm(dec(L5[3])) + "$",
               r"$\log\frac32=\log3-\log2=" + Rm(dec(L5[4])) + "$", r"$\frac12(2\log2+\log3)=" + Rm(dec(L5[5], 4)) + "$", r"$\log\frac2{10}=\log2-1=" + Rm(dec(L5[6])) + "$", r"$3\log3=" + Rm(dec(L5[7])) + "$"])),
 (2, r"Desenvolupa aplicant les propietats:" + tasks(2, [r"$\log(x^2y)$", r"$\log\dfrac{100x}{y^3}$", r"$\log\sqrt{\dfrac xy}$", r"$\ln(e^2x)$", r"$\log_2\dfrac{8a^3}{b}$"]),
     tasks(1, [R(r"2\log x+\log y"), R(r"2+\log x-3\log y"), R(r"\tfrac12\left(\log x-\log y\right)"), R(r"2+\ln x"), R(r"3+3\log_2a-\log_2b")])),
 (2, r"Escriu $E$ sense logaritmes:" + tasks(1, [r"$\log E=\log3+2\log x-\log y$", r"$\log E=2-\log x$", r"$\log E=\frac12\log a+3\log b$"]),
     tasks(3, [R(r"E=\dfrac{3x^2}{y}"), R(r"E=\dfrac{100}{x}"), R(r"E=b^3\sqrt a")])),
 (1, r"Amb la calculadora, calcula amb tres decimals:" + tasks(4, [r"$\log50$", r"$\ln7$", r"$\log0,35$", r"$\ln0,5$", r"$\log_3 15$", r"$\log_2 100$", r"$\log_7 2$", r"$\log_5 0,2$"])
     + recorda(r"Canvi de base: $\log_a x=\dfrac{\log x}{\log a}=\dfrac{\ln x}{\ln a}$."),
     tasks(4, [R(dec(x)) for x in calc[:7]] + [R("-1") + r" (exacte: $5^{-1}=0,2$)"])),
 (2, r"Calcula sense calculadora:" + tasks(2, [r"$\log1000+\ln e^3-\log_2 16$", r"$\ln1+\log0,01$", r"$\ln\sqrt e$", r"$\log\sqrt[3]{100}$"]),
     tasks(4, [R("2"), R("-2"), R(r"\frac12"), R(r"\frac23")])),
]))
eq('log(1000,10)+3-log(16,2)', 2); eq('log(Rational(1,100),10)', -2); eq('log(sqrt(E))', 'Rational(1,2)'); eq('log(100**Rational(1,3),10)', 'Rational(2,3)')

# =====================================================================
# 7. Problemes
t_bac = 4 / math.log10(2); t_cap = math.log10(4 / 3) / math.log10(1.04); ph = -math.log10(2.5e-5)
ck([round(t_bac, 2), round(t_cap, 2), math.ceil(t_cap), round(ph, 2)], [13.29, 7.33, 8, 4.6])
eq('sqrt(12)*sqrt(27)', 18); eq('2*(sqrt(12)+sqrt(27))', '10*sqrt(3)'); eq('sqrt(12+27)', 'sqrt(39)')
S.append(("Problemes", [
 (2, r"Un quadrat té una àrea de $50\ \text{cm}^2$. Calcula'n el costat i la diagonal en forma de radical simplificat.",
     r"Costat: $\sqrt{50}=" + Rm(r"5\sqrt2\ \text{cm}") + r"$. Diagonal: $\sqrt2\cdot5\sqrt2=" + Rm(r"10\ \text{cm}") + r"$."),
 (2, r"Un rectangle fa $\sqrt{12}$ cm d'amplària i $\sqrt{27}$ cm de llargària. Calcula'n el perímetre, l'àrea i la diagonal de manera exacta.",
     r"Perímetre: $2(2\sqrt3+3\sqrt3)=" + Rm(r"10\sqrt3\ \text{cm}") + r"$. Àrea: $\sqrt{12\cdot27}=\sqrt{324}=" + Rm(r"18\ \text{cm}^2") + r"$. Diagonal: $\sqrt{12+27}=" + Rm(r"\sqrt{39}\ \text{cm}") + "$."),
 (2, r"Per a anar a una excursió cal tindre almenys 12 anys i menys de 17. Escriu l'interval d'edats. Si el preu reduït és per a menors de 14 anys, quines edats poden anar a l'excursió amb preu reduït?",
     r"Excursió: " + R(r"[12, 17)") + r". Preu reduït: $[0, 14)$. Les dues coses alhora: $[12, 17)\cap[0, 14)=" + Rm(st(cap(P('[12,17)'), P('[0,14)')))) + "$."),
 (2, r"Una colònia de bacteris es duplica cada hora. Quantes hores tarda a passar de 100 bacteris a un milió?",
     r"$100\cdot2^t=10^6\Rightarrow2^t=10^4\Rightarrow t=\dfrac{4}{\log2}\approx" + Rm(dec(t_bac, 2) + r"\ \text{hores}") + "$."),
 (2, r"Ingressem 1500 € en un compte al 4\,\% d'interés compost anual. Quants anys han de passar, com a mínim, perquè hi haja 2000 €?",
     r"$1500\cdot1,04^t=2000\Rightarrow1,04^t=\frac43\Rightarrow t=\dfrac{\log\frac43}{\log1,04}\approx" + dec(t_cap, 2) + r"$. Calen " + R(r"8\ \text{anys}") + "."),
 (3, r"El pH d'una dissolució és $\text{pH}=-\log[\text{H}^+]$. Calcula el pH si $[\text{H}^+]=10^{-3}$ i si $[\text{H}^+]=2,5\cdot10^{-5}$. Quina de les dues és més àcida (pH menor)?",
     r"$\text{pH}=-\log10^{-3}=" + Rm("3") + r"$; \ $\text{pH}=-\log(2,5\cdot10^{-5})\approx" + Rm(dec(ph, 2)) + r"$. És més àcida \rest{la primera}."),
]))

build(HERE, 1, "Nombres reals", S,
      "nombres reals, intervals, semirectes, unió, intersecció, radicals, racionalització, logaritmes",
      r"Resol-los al quadern mostrant tots els passos. Dona els resultats de manera exacta (fraccions i radicals simplificats, sense arrels al denominador). Fes servir la calculadora només quan l'enunciat ho diga.",
      r"Intenta resoldre cada exercici abans de mirar-ne la solució. Pots comprovar els d'intervals, radicals, racionalització i logaritmes amb les eines interactives dels apunts de la unitat.")
