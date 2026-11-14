# Versió en castellà de genera.py. Genera t1-fitxa-exercicis-es.tex i t1-fitxa-solucions-es.tex (4t ESO Matemàtiques B, Unitat 1: Nombres reals)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Els exercicis 1-17 són els de la fitxa del departament («Fitxa 1 (1a Av.): Nombres reals»), amb la mateixa numeració.
# Les seccions 8-10 són d'ampliació, enfocades al Batxillerat: hi ha els exercicis de racionalització i sumes de radicals
# del departament (els mateixos de la fitxa de 1r Batx MI) i exercicis nous de més nivell.
# Les solucions de fraccions i intervals es calculen ací (aritmètica exacta) i les de radicals, potències i logaritmes
# es comproven amb eq() (sympy, numèricament). Les solucions d'intervals porten la recta dibuixada amb TikZ.
# Ús: python3 genera-es.py && pdflatex t1-fitxa-exercicis-es.tex (dues vegades) && pdflatex t1-fitxa-solucions-es.tex (dues vegades)
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

S = []
def chk(pairs, **kw):
    for a, b in pairs: eq(a, b, **kw)

# =====================================================================
# 1. Classificació dels nombres (exercici 1 del departament)
ck(per('7', '', '9'), F(8))
S.append(("Clasificación de los números", [
 (1, r"Clasifica los números siguientes en el menor conjunto numérico al que pertenecen:" + tasks(4, [r"$-\frac{15}{2}$", r"$7,\widehat9$", r"$\sqrt{-4}$", r"$\pi+4$", r"$\sqrt[3]{-8}$", r"$\frac{16}{4}$", r"$3,1122333\ldots$"]),
     tasks(2, [R(r"\mathbb Q"), r"$7,\widehat9=\frac{79-7}{9}=8$: " + R(r"\mathbb N"), r"No es un número real.", R(r"\mathbb I") + r" (infinitas cifras sin período)", r"$-2$: " + R(r"\mathbb Z"), r"$4$: " + R(r"\mathbb N"),
               R(r"\mathbb I") + r" (las cifras no se repiten en bloques)"])),
]))

# =====================================================================
# 2. Intervals (exercicis 2 i 3 del departament)
A, B, Cc, D = P('(-inf,2]'), P('[1,5]'), P('(2,4]'), P('(-7,inf)')
r3 = [cup(A, B), cup(B, Cc), cup(A, D), cup(cup(A, B), Cc), cap(A, B), cap(B, D), cap(A, Cc), cap(cap(A, B), Cc)]
ck(r3, [P('(-inf,5]'), P('[1,5]'), P('(-inf,inf)'), P('(-inf,5]'), P('[1,2]'), P('[1,5]'), [], []])
S.append(("Intervalos y semirrectas", [
 (1, r"Representa estos intervalos en la recta real y exprésalos como inecuaciones:" + tasks(4, [r"$A=(-\infty, 2]$", r"$B=[1, 5]$", r"$C=(2, 4]$", r"$D=(-7, +\infty)$"]),
     tasks(2, [r"$x\le2$ " + recta(A), r"$1\le x\le5$ " + recta(B), r"$2<x\le4$ " + recta(Cc), r"$x>-7$ " + recta(D)])),
 (2, r"Calcula las uniones e intersecciones siguientes, donde $A$, $B$, $C$ y $D$ son los intervalos del ejercicio anterior:" + tasks(4, [r"$A\cup B$", r"$B\cup C$", r"$A\cup D$", r"$A\cup B\cup C$", r"$A\cap B$", r"$B\cap D$", r"$A\cap C$", r"$A\cap B\cap C$"])
     + recorda(r"La unión son los números que están en alguno de los intervalos; la intersección, los que están en todos a la vez."),
     tasks(2, [RI(x, -8, 6) if x else R(r"\varnothing") + r" (el 2 es de $A$ pero no de $C$)" for x in r3[:7]] + [R(r"\varnothing")])),
]))

# =====================================================================
# 3. Valor absolut (exercici 4 del departament)
S.append(("Valor absoluto", [
 (2, r"Averigua para qué valores de $x$ se cumplen las desigualdades siguientes. Expresa la solución gráficamente y con intervalos:" + tasks(4, [r"$|x|<5$", r"$|x|\ge4$", r"$|x+2|\le9$", r"$|x+1|\ge6$"])
     + recorda(r"Si $r>0$: \ $|A|<r\iff -r<A<r$ \quad y \quad $|A|>r\iff A<-r$ o $A>r$."),
     tasks(2, [RI('(-5,5)'), RI('(-inf,-4]U[4,inf)'), r"$-9\le x+2\le9$: " + RI('[-11,7]'), r"$x+1\le-6$ o $x+1\ge6$: " + RI('(-inf,-7]U[5,inf)')])),
]))

# =====================================================================
# 4. Potències (exercicis 5 i 6 del departament)
p5 = [F(-2) ** 5, -F(2) ** 5, F(53) ** 0, F(-1) ** 35, F(-3) ** 2, F(1, 2) ** -3, F(3, 2) ** 2, F(-1, 2) ** 4, F(2, 3) ** -2, F(1, 5) ** -1]
ck(p5, [-32, -32, 1, -1, 9, 8, F(9, 4), F(1, 16), F(9, 4), 5])
p6 = [((F(-1, 3) ** 3) * F(3, 2) ** -2) ** 2, (F(-2) ** 5 * (F(2) ** 3) ** 4) / (-F(2) ** 4 * F(-2) ** -6),
      F(2) ** 4 * F(3) ** -2 * F(5) ** -1 / (F(2) ** -3 * F(3) ** 2 * F(5) ** -2), F(3) ** -4 * 16 * F(9) ** -1 / (F(8) ** 2 * F(3) ** -5 * F(2) ** -3)]
ck(p6, [F(2 ** 4, 3 ** 10), F(2) ** 19, F(2 ** 7 * 5, 3 ** 4), F(2, 3)])
S.append(("Potencias", [
 (1, r"Calcula las potencias siguientes:" + tasks(5, [r"$(-2)^5$", r"$-2^5$", r"$53^0$", r"$(-1)^{35}$", r"$(-3)^2$", r"$\left(\frac12\right)^{-3}$", r"$\left(\frac32\right)^2$", r"$\left(\frac{-1}{2}\right)^4$", r"$\left(\frac23\right)^{-2}$", r"$\left(\frac15\right)^{-1}$"]),
     tasks(5, [R(tn(v)) for v in p5])),
 (2, r"Simplifica las expresiones siguientes con potencias:" + tasks(2, [r"$\left[\left(\dfrac{-1}{3}\right)^3\cdot\left(\dfrac32\right)^{-2}\right]^2$", r"$\dfrac{(-2)^5\cdot(2^3)^4}{-2^4\cdot(-2)^{-6}}$",
      r"$\dfrac{2^4\cdot3^{-2}\cdot5^{-1}}{2^{-3}\cdot3^2\cdot5^{-2}}$", r"$\dfrac{3^{-4}\cdot16\cdot9^{-1}}{8^2\cdot3^{-5}\cdot2^{-3}}$"])
     + recorda(r"Descompón las bases en factores primos y aplica $a^m\cdot a^n=a^{m+n}$, $a^m:a^n=a^{m-n}$, $(a^m)^n=a^{m\cdot n}$ y $a^{-n}=\frac1{a^n}$."),
     tasks(2, [r"$\left[-\frac{2^2}{3^5}\right]^2=" + Rm(r"\frac{2^4}{3^{10}}") + "$", r"$\dfrac{-2^{17}}{-2^{-2}}=" + Rm("2^{19}") + "$",
               r"$2^7\cdot3^{-4}\cdot5=" + Rm(r"\frac{640}{81}") + "$", r"$\dfrac{2^4\cdot3^{-6}}{2^3\cdot3^{-5}}=" + Rm(r"\frac23") + "$"])),
]))

# =====================================================================
# 5. Radicals (exercicis 7-13 del departament)
chk([('root(64,3)', 4), ('real_root(-8,3)', -2), ('root(100000,5)', 10), ('real_root(-32,5)', -2), ('sqrt(Rational(36,100))', 'Rational(6,10)'), ('real_root(-1,3)', -1)])
chk([('sqrt(1280)', '16*sqrt(5)'), ('root(1080,3)', '6*root(5,3)'), ('root(5184,3)', '12*root(3,3)'), ('root(1024,3)', '8*root(2,3)'),
     ('root(2**9*3**15*5**27,4)', '2**2*3**3*5**6*root(2*3**3*5**3,4)'), ('sqrt(3**8*5**11*7**5)', '3**4*5**5*7**2*sqrt(35)'),
     ('sqrt(a**7*b**7*c**9)', 'a**3*b**3*c**4*sqrt(a*b*c)'), ('root(x**27*y**30*z**48,5)', 'x**5*y**6*z**9*root(x**2*z**3,5)')])
chk([('Rational(3,5)*sqrt(2)', 'sqrt(Rational(18,25))'), ('2*root(5,3)', 'root(40,3)'), ('2*root(7,3)', 'root(56,3)'), ('4*root(20,4)', 'root(5120,4)'), ('root(6,4)/2', 'root(Rational(3,8),4)'),
     ('5*root(Rational(1,5),3)', 'root(25,3)'), ('3*root(15,5)', 'root(3645,5)'), ('root(Rational(1,2),4)/2', 'root(Rational(1,32),4)')])
chk([('2**Rational(3,4)*2**Rational(5,6)', '2**Rational(19,12)'), ('2**Rational(7,3)*2**Rational(-5,2)', '2**Rational(-1,6)'), ('3**Rational(1,2)/3**Rational(-3,4)', '3**Rational(5,4)'), ('(5**-2)**Rational(-3,4)', '5**Rational(3,2)')])
chk([('sqrt(5)*root(5,3)', 'root(5**5,6)'), ('root(2,3)*root(7,4)', 'root(5488,12)'), ('root(9,3)*sqrt(3)', '3*root(3,6)'), ('root(a,4)*root(a**3,3)*root(a**5,6)', 'a**2*root(a,12)'),
     ('sqrt(3)/root(3**4,5)', '1/root(27,10)'), ('sqrt(root(5,3))', 'root(5,6)'), ('root(sqrt(8),4)', 'root(8,8)'), ('root(2*sqrt(2**3),3)', 'root(32,6)')])
chk([('sqrt(45)-sqrt(125)-sqrt(20)', '-4*sqrt(5)'), ('sqrt(75)-sqrt(147)+sqrt(675)-sqrt(12)', '11*sqrt(3)'), ('sqrt(175)+sqrt(63)-2*sqrt(28)', '4*sqrt(7)'),
     ('sqrt(20)+sqrt(45)/3+2*sqrt(125)', '13*sqrt(5)'), ('sqrt(32)-sqrt(8)+3*sqrt(72)-2*sqrt(200)', 0), ('7*root(3,3)-root(24,3)+3*root(81,3)-4*root(375,3)', '-6*root(3,3)')])
assert 2 ** 19 == 524288 and 5488 == 2 ** 4 * 7 ** 3
S.append(("Radicales", [
 (1, r"Calcula las raíces siguientes siempre que se pueda:" + tasks(3, [r"$\sqrt[3]{64}$", r"$\sqrt[3]{-8}$", r"$\sqrt[5]{100\,000}$", r"$\sqrt[5]{-32}$", r"$\sqrt{0,36}$", r"$\sqrt{-1}$", r"$\sqrt[3]1$", r"$\sqrt[3]{-1}$", r"$\sqrt1$"]),
     tasks(3, [R("4"), R("-2"), R("10"), R("-2"), R("0,6"), r"No es real.", R("1"), R("-1"), R("1") + r" \ (y $-1$, porque $(-1)^2=1$)"])),
 (2, r"Extrae todos los factores que se pueda de las raíces siguientes:" + tasks(4, [r"$\sqrt{1280}$", r"$\sqrt[3]{1080}$", r"$\sqrt[3]{5184}$", r"$\sqrt[3]{1024}$", r"$\sqrt[4]{2^9\cdot3^{15}\cdot5^{27}}$", r"$\sqrt{3^8\cdot5^{11}\cdot7^5}$", r"$\sqrt{a^7\cdot b^7\cdot c^9}$", r"$\sqrt[5]{x^{27}\cdot y^{30}\cdot z^{48}}$"]),
     tasks(2, [r"$\sqrt{2^8\cdot5}=" + Rm(r"16\sqrt5") + "$", r"$\sqrt[3]{2^3\cdot3^3\cdot5}=" + Rm(r"6\sqrt[3]5") + "$", r"$\sqrt[3]{2^6\cdot3^4}=" + Rm(r"12\sqrt[3]3") + "$", r"$\sqrt[3]{2^{10}}=" + Rm(r"8\sqrt[3]2") + "$",
               R(r"2^2\cdot3^3\cdot5^6\sqrt[4]{2\cdot3^3\cdot5^3}"), R(r"3^4\cdot5^5\cdot7^2\sqrt{5\cdot7}"), R(r"a^3b^3c^4\sqrt{abc}"), R(r"x^5y^6z^9\sqrt[5]{x^2z^3}")])),
 (2, r"Introduce los factores en las raíces y simplifica:" + tasks(4, [r"$\frac35\sqrt2$", r"$2\sqrt[3]5$", r"$2\sqrt[3]7$", r"$4\sqrt[4]{20}$", r"$\frac12\sqrt[4]6$", r"$5\sqrt[3]{\frac15}$", r"$3\sqrt[5]{15}$", r"$\frac12\sqrt[4]{\frac12}$"])
     + recorda(r"El factor entra en la raíz elevado al índice: $a\sqrt[n]{b}=\sqrt[n]{a^n\cdot b}$."),
     tasks(4, [R(r"\sqrt{\frac{18}{25}}"), R(r"\sqrt[3]{40}"), R(r"\sqrt[3]{56}"), R(r"\sqrt[4]{5120}"), R(r"\sqrt[4]{\frac38}"), R(r"\sqrt[3]{25}"), R(r"\sqrt[5]{3645}"), R(r"\sqrt[4]{\frac1{32}}")])),
 (1, r"¿Cuántas raíces reales hay en cada caso?" + tasks(2, [r"$\sqrt[\text{par}]{\text{positivo}}$", r"$\sqrt[\text{par}]{\text{negativo}}$", r"$\sqrt[\text{impar}]{\text{positivo}}$", r"$\sqrt[\text{impar}]{\text{negativo}}$"]),
     tasks(2, [R("2") + r" (opuestas: $\pm\sqrt{16}=\pm4$)", R("0") + r" ($\sqrt{-16}\notin\mathbb R$)", R("1") + r", positiva", R("1") + r", negativa ($\sqrt[3]{-8}=-2$)"])),
 (1, r"Expresa en forma de una sola potencia:" + tasks(4, [r"$2^{\frac34}\cdot2^{\frac56}$", r"$2^{\frac73}\cdot2^{-\frac52}$", r"$\dfrac{3^{\frac12}}{3^{-\frac34}}$", r"$\left(5^{-2}\right)^{-\frac34}$"]),
     tasks(4, [R(r"2^{\frac{19}{12}}"), R(r"2^{-\frac16}"), R(r"3^{\frac54}"), R(r"5^{\frac32}")])),
 (2, r"Expresa con un solo radical y simplifica si es posible:" + tasks(4, [r"$\sqrt5\cdot\sqrt[3]5$", r"$\sqrt[3]2\cdot\sqrt[4]7$", r"$\sqrt[3]9\cdot\sqrt3$", r"$\sqrt[4]a\cdot\sqrt[3]{a^3}\cdot\sqrt[6]{a^5}$", r"$\dfrac{\sqrt3}{\sqrt[5]{3^4}}$", r"$\sqrt{\sqrt[3]5}$", r"$\sqrt[4]{\sqrt8}$", r"$\sqrt[3]{2\sqrt{2^3}}$"])
     + recorda(r"Pasa a forma de potencia ($\sqrt[n]{a^m}=a^{\frac mn}$) o reduce a índice común."),
     tasks(4, [R(r"\sqrt[6]{5^5}"), R(r"\sqrt[12]{2^4\cdot7^3}"), R(r"\sqrt[6]{3^7}=3\sqrt[6]3"), R(r"a^{\frac{25}{12}}=a^2\sqrt[12]a"), R(r"3^{-\frac3{10}}=\frac{1}{\sqrt[10]{27}}"), R(r"\sqrt[6]5"), R(r"\sqrt[8]8"), R(r"2^{\frac56}=\sqrt[6]{32}")])),
 (2, r"Calcula:" + tasks(2, [r"$\sqrt{45}-\sqrt{125}-\sqrt{20}$", r"$\sqrt{75}-\sqrt{147}+\sqrt{675}-\sqrt{12}$", r"$\sqrt{175}+\sqrt{63}-2\sqrt{28}$", r"$\sqrt{20}+\frac13\sqrt{45}+2\sqrt{125}$", r"$\sqrt{32}-\sqrt8+3\sqrt{72}-2\sqrt{200}$", r"$7\sqrt[3]3-\sqrt[3]{24}+3\sqrt[3]{81}-4\sqrt[3]{375}$"])
     + recorda(r"Extrae factores y suma solo los radicales semejantes (mismo índice y mismo radicando)."),
     tasks(2, [r"$3\sqrt5-5\sqrt5-2\sqrt5=" + Rm(r"-4\sqrt5") + "$", r"$5\sqrt3-7\sqrt3+15\sqrt3-2\sqrt3=" + Rm(r"11\sqrt3") + "$", r"$5\sqrt7+3\sqrt7-4\sqrt7=" + Rm(r"4\sqrt7") + "$",
               r"$2\sqrt5+\sqrt5+10\sqrt5=" + Rm(r"13\sqrt5") + "$", r"$4\sqrt2-2\sqrt2+18\sqrt2-20\sqrt2=" + Rm("0") + "$", r"$7\sqrt[3]3-2\sqrt[3]3+9\sqrt[3]3-20\sqrt[3]3=" + Rm(r"-6\sqrt[3]3") + "$"])),
]))

# =====================================================================
# 6. Racionalització (exercici 14 del departament)
chk([('2/sqrt(7)', '2*sqrt(7)/7'), ('1/sqrt(3)', 'sqrt(3)/3'), ('3*sqrt(2)/sqrt(3)', 'sqrt(6)'), ('6/root(4,3)', '3*root(2,3)'), ('5/(2*root(10,3))', 'root(100,3)/4'),
     ('5/(2-sqrt(3))', '10+5*sqrt(3)'), ('2*sqrt(3)/(sqrt(5)-sqrt(3))', 'sqrt(15)+3'), ('sqrt(2)/(sqrt(2)+4)', '(2*sqrt(2)-1)/7')])
S.append(("Racionalización", [
 (2, r"Racionaliza:" + tasks(4, [r"$\dfrac{2}{\sqrt7}$", r"$\dfrac{1}{\sqrt3}$", r"$\dfrac{3\sqrt2}{\sqrt3}$", r"$\dfrac{6}{\sqrt[3]4}$", r"$\dfrac{5}{2\sqrt[3]{10}}$", r"$\dfrac{5}{2-\sqrt3}$", r"$\dfrac{2\sqrt3}{\sqrt5-\sqrt3}$", r"$\dfrac{\sqrt2}{\sqrt2+4}$"])
     + recorda(r"Con una suma o una resta en el denominador, multiplica por el conjugado: $(a+b)(a-b)=a^2-b^2$."),
     tasks(4, [R(r"\dfrac{2\sqrt7}{7}"), R(r"\dfrac{\sqrt3}{3}"), R(r"\sqrt6"), R(r"3\sqrt[3]2"), R(r"\dfrac{\sqrt[3]{100}}{4}"), R(r"10+5\sqrt3"), R(r"\sqrt{15}+3"), R(r"\dfrac{2\sqrt2-1}{7}")])),
]))

# =====================================================================
# 7. Logaritmes (exercicis 15-17 del departament)
chk([('log(8,2)', 3), ('log(81,3)', 4), ('log(1000,10)', 3), ('log(exp(-4))', -4), ('log(Rational(1,10000),10)', -4), ('log(Rational(1,4),4)', -1), ('log(root(4,6),2)', 'Rational(1,3)'), ('log(exp(3))', 3)])
chk([('log(27,3)', 3), ('log(256,2)', 8), ('5**3', 125), ('log(exp(5))', 5), ('log(10000,10)', 4)])
ck([round(0.31 + 1.4, 2), round(3 * 0.31 + 1.4, 2)], [1.71, 2.33])
S.append(("Logaritmos", [
 (1, r"Calcula, utilizando la definición, los logaritmos siguientes:" + tasks(4, [r"$\log_2 8$", r"$\log_3 81$", r"$\log 1000$", r"$\ln e^{-4}$", r"$\log 0,0001$", r"$\log_4 0,25$", r"$\log_2\sqrt[6]4$", r"$\ln e^3$"])
     + recorda(r"$\log_a b=c\iff a^c=b$. Además, $\log_a a=1$ y $\log_a 1=0$."),
     tasks(4, [R("3"), R("4"), R("3"), R("-4"), R("-4"), R("-1"), R(r"\frac13"), R("3")])),
 (1, r"Halla cuánto vale $x$ en cada caso:" + tasks(4, [r"$\log_3 27=x$", r"$\log_2 x=8$", r"$\log_x 125=3$", r"$\ln e^5=x$", r"$\log 0,0001=x$", r"$\log 10\,000=x$", r"$\log_a a=x$", r"$\log_a 1=x$"]),
     tasks(4, [R("x=3"), R("x=256"), R("x=5"), R("x=5"), R("x=-4"), R("x=4"), R("x=1"), R("x=0")])),
 (2, r"Sabiendo que $\log_5 a=0,31$ y que $\log_5 b=1,4$, calcula:" + tasks(2, [r"$\log_5(a\cdot b)$", r"$\log_5(a^3\cdot b)$"]),
     tasks(2, [r"$0,31+1,4=" + Rm("1,71") + "$", r"$3\cdot0,31+1,4=" + Rm("2,33") + "$"])),
]))

# =====================================================================
# 8. Ampliació: nombres, intervals, valor absolut i potències
g8 = [per('2', '', '7') + per('3', '', '4') - per('1', '', '1'), per('1', '', '8') + per('0', '', '1'), per('0', '1', '6') * per('1', '', '5'), per('1', '2', '3') - per('0', '', '45')]
ck(g8, [F(46, 9), F(2), F(7, 27), F(257, 330)])
A8, B8, C8 = P('(-3,5/2]'), P('[1/2,4)'), P('(-inf,1]')
r8 = [cap(A8, B8), cup(A8, C8), cap(B8, C8), cap(cap(A8, B8), C8), cup(B8, C8)]
ck(r8, [P('[1/2,5/2]'), P('(-inf,5/2]'), P('[1/2,1]'), P('[1/2,1]'), P('(-inf,4)')])
pw = [F(6) ** -2 * F(9) ** 3 * F(2) ** 5 / (F(4) ** 2 * 27 * F(3) ** -1)]
ck(pw, [F(9, 2)])
chk([('8**Rational(2,3)*27**Rational(-1,3)/16**Rational(3,4)', 'Rational(1,6)'), ('Rational(1,32)**Rational(-2,5)', 4), ('81**Rational(3,4)', 27)])
S.append(("Ampliación: números, intervalos, valor absoluto y potencias", [
 (2, r"Escribe los números en forma de fracción y opera:" + tasks(2, [r"$2,\widehat7+3,\widehat4-1,\widehat1$", r"$1,\widehat8+0,\widehat1$", r"$0,1\widehat6\cdot1,\widehat5$", r"$1,2\widehat3-0,\widehat{45}$"]),
     tasks(2, [r"$\frac{25}9+\frac{31}9-\frac{10}9=" + Rm(tn(g8[0])) + "$", r"$\frac{17}9+\frac19=" + Rm("2") + "$", r"$\frac16\cdot\frac{14}9=" + Rm(tn(g8[2])) + "$", r"$\frac{37}{30}-\frac5{11}=" + Rm(tn(g8[3])) + "$"])),
 (2, r"Dados $A=\left(-3, \frac52\right]$, $B=\left[\frac12, 4\right)$ y $C=(-\infty, 1]$, calcula:" + tasks(3, [r"$A\cap B$", r"$A\cup C$", r"$B\cap C$", r"$A\cap B\cap C$", r"$B\cup C$"]),
     tasks(2, [RI(x, -4, 5) for x in r8])),
 (2, r"Resuelve y representa:" + tasks(4, [r"$|2x-1|>3$", r"$|3x+6|\le9$", r"$|5-x|\ge2$", r"$|x-3|<-1$"]),
     tasks(2, [RI('(-inf,-1)U(2,inf)'), RI('[-5,1]'), RI('(-inf,3]U[7,inf)'), R(r"\varnothing") + r" (un valor absoluto no puede ser negativo)"])),
 (3, r"Escribe cada intervalo con una desigualdad con valor absoluto (busca su centro y su radio): \ $(1, 7)$, \ $[-5, 1]$, \ $(-\infty, -1)\cup(5, +\infty)$.",
     tasks(3, [R(r"|x-4|<3"), R(r"|x+2|\le3"), R(r"|x-2|>3")])),
 (2, r"La temperatura $T$ de una nevera debe ser de $4\,^\circ$C con un error máximo de $1,5\,^\circ$C. Escríbelo con un valor absoluto y como intervalo. ¿Es aceptable una lectura de $5,7\,^\circ$C?",
     R(r"|T-4|\le1,5") + r", es decir, $T\in[2,5;\ 5,5]$. Una lectura de $5,7\,^\circ$C \rest{no es aceptable}: $|5,7-4|=1,7>1,5$."),
 (3, r"Simplifica, descomponiendo las bases en factores primos: \ $\dfrac{6^{-2}\cdot9^3\cdot2^5}{4^2\cdot27\cdot3^{-1}}$. \ Calcula también, sin calculadora: \ $\dfrac{8^{2/3}\cdot27^{-1/3}}{16^{3/4}}$, \ $\left(\dfrac1{32}\right)^{-2/5}$, \ $81^{0,75}$.",
     r"$\dfrac{2^{-2}3^{-2}\cdot3^6\cdot2^5}{2^4\cdot3^3\cdot3^{-1}}=2^{-1}\cdot3^2=" + Rm(r"\frac92") + r"$; \ $\dfrac{4\cdot\frac13}{8}=" + Rm(r"\frac16") + r"$; \ $2^2=" + Rm("4") + r"$; \ $3^3=" + Rm("27") + "$."),
]))

# =====================================================================
# 9. Ampliació: radicals i racionalització (exercicis de racionalització i sumes del departament i nous)
chk([('5/sqrt(5)', 'sqrt(5)'), ('2*sqrt(6)/sqrt(2)', '2*sqrt(3)'), ('sqrt(Rational(5,2))', 'sqrt(10)/2'), ('3/sqrt(5)', '3*sqrt(5)/5'), ('root(Rational(3,2),3)', 'root(12,3)/2'), ('3/(2*root(4,3))', '3*root(2,3)/4'),
     ('3*y/(x*sqrt(y))', '3*sqrt(y)/x'), ('x*sqrt(y)/(y*sqrt(x))', 'sqrt(x*y)/y'), ('2*sqrt(12)/(5*sqrt(3))', 'Rational(4,5)'), ('3*sqrt(2)/sqrt(6)', 'sqrt(3)'),
     ('3*x*y**2/root(x**2*y,3)', '3*y*root(x*y**2,3)'), ('6*(3-y)/root((3-y)**2,3)', '6*root(3-y,3)'), ('-4/(root(3,4)*root(2,3))', '-Rational(2,3)*root(27,4)*root(4,3)')], subs={})
chk([('1/(sqrt(2)+sqrt(3))', 'sqrt(3)-sqrt(2)'), ('2/(sqrt(2)-1)', '2*sqrt(2)+2'), ('sqrt(2)/(3-sqrt(2))', '(3*sqrt(2)+2)/7'), ('(1-sqrt(2))/(1+sqrt(2))', '2*sqrt(2)-3'), ('(sqrt(5)-2)/(3-2*sqrt(5))', '(sqrt(5)-4)/11'),
     ('1/(sqrt(x)-sqrt(y))', '(sqrt(x)+sqrt(y))/(x-y)'), ('sqrt(2*y)/(sqrt(2)-sqrt(y))', '(2*sqrt(y)+y*sqrt(2))/(2-y)'), ('sqrt(x*y)/(2*sqrt(x)-3*sqrt(y))', '(2*x*sqrt(y)+3*y*sqrt(x))/(4*x-9*y)'),
     ('5/(2*(sqrt(3)-sqrt(2)))', '5*(sqrt(3)+sqrt(2))/2'), ('sqrt(2)/(2*sqrt(2)+1)', '(4-sqrt(2))/7'), ('(2+sqrt(2))/(2-sqrt(2))', '3+2*sqrt(2)')], subs={})
chk([('sqrt(8)+sqrt(18)+sqrt(32)+sqrt(50)', '14*sqrt(2)'), ('sqrt(28)+sqrt(63)-sqrt(175)', 0), ('6*sqrt(3)-4*sqrt(3)+5*sqrt(3)', '7*sqrt(3)'), ('3*sqrt(2)+5*sqrt(2)-8*sqrt(2)', 0),
     ('3*sqrt(2)-3*sqrt(8)+3*sqrt(18)', '6*sqrt(2)'), ('2*a*sqrt(3)-sqrt(27*a**2)+a*sqrt(12)', 'a*sqrt(3)'), ('(3+a)*sqrt(5)-sqrt(125)+sqrt(5*a**2)', '(2*a-2)*sqrt(5)'),
     ('7*sqrt(54)-3*sqrt(18)+sqrt(24)-Rational(3,5)*sqrt(50)-sqrt(6)', '22*sqrt(6)-12*sqrt(2)'), ('sqrt(Rational(1,3))+sqrt(27)', '10*sqrt(3)/3'), ('sqrt(Rational(1,2))+sqrt(2)+root(4,4)+root(8,6)+root(64,4)', '11*sqrt(2)/2'),
     ('2*sqrt(Rational(3,4))-sqrt(27)+sqrt(12)/4-3*sqrt(Rational(75,9))', '-13*sqrt(3)/2'), ('sqrt(18)+5*sqrt(12)-2*sqrt(2)-sqrt(243)', 'sqrt(2)+sqrt(3)'), ('2*sqrt(3)+5*root(27,6)-3*sqrt(12)', 'sqrt(3)'), ('5*sqrt(20)-2*sqrt(45)+sqrt(5)', '5*sqrt(5)')])
chk([('(sqrt(3)+sqrt(2))**2', '5+2*sqrt(6)'), ('(2*sqrt(5)-1)*(2*sqrt(5)+1)', 19), ('sqrt(2)*(sqrt(8)-sqrt(18))', -2), ('(sqrt(5)+1)**2-2*sqrt(5)', 6),
     ('(sqrt(3)+1)/(sqrt(3)-1)-(sqrt(3)-1)/(sqrt(3)+1)', '2*sqrt(3)'), ('1/sqrt(2)+1/(sqrt(2)+1)', '3*sqrt(2)/2-1'), ('sqrt(50)', '5*sqrt(2)')])
S.append(("Ampliación: radicales y racionalización", [
 (2, r"Racionaliza el denominador de las expresiones siguientes:" + tasks(4, [r"$\dfrac{5}{\sqrt5}$", r"$\dfrac{2\sqrt6}{\sqrt2}$", r"$\sqrt{\dfrac52}$", r"$\dfrac{3}{\sqrt5}$", r"$\sqrt[3]{\dfrac32}$", r"$\dfrac{3}{2\sqrt[3]4}$", r"$\dfrac{3y}{x\sqrt y}$",
      r"$\dfrac{x\sqrt y}{y\sqrt x}$", r"$\dfrac{2\sqrt{12}}{5\sqrt3}$", r"$\dfrac{3\sqrt2}{\sqrt6}$", r"$\dfrac{3xy^2}{\sqrt[3]{x^2y}}$", r"$\dfrac{6(3-y)}{\sqrt[3]{(3-y)^2}}$", r"$\dfrac{-4}{\sqrt[4]3\cdot\sqrt[3]2}$"]),
     tasks(4, [R(r"\sqrt5"), R(r"2\sqrt3"), R(r"\frac{\sqrt{10}}{2}"), R(r"\frac{3\sqrt5}{5}"), R(r"\frac{\sqrt[3]{12}}{2}"), R(r"\frac{3\sqrt[3]2}{4}"), R(r"\frac{3\sqrt y}{x}"), R(r"\frac{\sqrt{xy}}{y}"),
               R(r"\frac45"), R(r"\sqrt3"), R(r"3y\sqrt[3]{xy^2}"), R(r"6\sqrt[3]{3-y}"), R(r"-\frac23\sqrt[4]{27}\,\sqrt[3]4")])),
 (3, r"Racionaliza el denominador de las expresiones siguientes:" + tasks(4, [r"$\dfrac{1}{\sqrt2+\sqrt3}$", r"$\dfrac{2}{\sqrt2-1}$", r"$\dfrac{\sqrt2}{3-\sqrt2}$", r"$\dfrac{1-\sqrt2}{1+\sqrt2}$", r"$\dfrac{\sqrt5-2}{3-2\sqrt5}$", r"$\dfrac{1}{\sqrt x-\sqrt y}$",
      r"$\dfrac{\sqrt{2y}}{\sqrt2-\sqrt y}$", r"$\dfrac{\sqrt{xy}}{2\sqrt x-3\sqrt y}$", r"$\dfrac{5}{2(\sqrt3-\sqrt2)}$", r"$\dfrac{\sqrt2}{2\sqrt2+1}$", r"$\dfrac{2+\sqrt2}{2-\sqrt2}$"]),
     tasks(3, [R(r"\sqrt3-\sqrt2"), R(r"2\sqrt2+2"), R(r"\frac{3\sqrt2+2}{7}"), R(r"2\sqrt2-3"), R(r"\frac{\sqrt5-4}{11}"), R(r"\frac{\sqrt x+\sqrt y}{x-y}"), R(r"\frac{2\sqrt y+y\sqrt2}{2-y}"),
               R(r"\frac{2x\sqrt y+3y\sqrt x}{4x-9y}"), R(r"\frac{5(\sqrt3+\sqrt2)}{2}"), R(r"\frac{4-\sqrt2}{7}"), R(r"3+2\sqrt2")])),
 (2, r"Realiza las sumas y restas siguientes:" + tasks(2, [r"$\sqrt8+\sqrt{18}+\sqrt{32}+\sqrt{50}$", r"$\sqrt{28}+\sqrt{63}-\sqrt{175}$", r"$6\sqrt3-4\sqrt3+5\sqrt3$", r"$3\sqrt2+5\sqrt2-8\sqrt2$", r"$3\sqrt2-3\sqrt8+3\sqrt{18}$",
      r"$2a\sqrt3-\sqrt{27a^2}+a\sqrt{12}$", r"$(3+a)\sqrt5-\sqrt{125}+\sqrt{5a^2}$", r"$7\sqrt{54}-3\sqrt{18}+\sqrt{24}-\frac35\sqrt{50}-\sqrt6$", r"$\sqrt{\frac13}+\sqrt{27}$", r"$\sqrt{\frac12}+\sqrt2+\sqrt[4]4+\sqrt[6]8+\sqrt[4]{64}$",
      r"$2\sqrt{\frac34}-\sqrt{27}+\frac14\sqrt{12}-3\sqrt{\frac{75}{9}}$", r"$\sqrt{18}+5\sqrt{12}-2\sqrt2-\sqrt{243}$", r"$2\sqrt3+5\sqrt[6]{27}-3\sqrt{12}$", r"$5\sqrt{20}-2\sqrt{45}+\sqrt5$"]),
     tasks(4, [R(r"14\sqrt2"), R("0"), R(r"7\sqrt3"), R("0"), R(r"6\sqrt2"), R(r"a\sqrt3"), R(r"(2a-2)\sqrt5"), R(r"22\sqrt6-12\sqrt2"), R(r"\frac{10\sqrt3}{3}"), R(r"\frac{11\sqrt2}{2}"), R(r"-\frac{13\sqrt3}{2}"), R(r"\sqrt2+\sqrt3"), R(r"\sqrt3"), R(r"5\sqrt5")])
     + r"(En los apartados f) y g) suponemos $a\ge0$.)"),
 (3, r"Opera y simplifica:" + tasks(2, [r"$(\sqrt3+\sqrt2)^2$", r"$(2\sqrt5-1)(2\sqrt5+1)$", r"$\sqrt2\left(\sqrt8-\sqrt{18}\right)$", r"$(\sqrt5+1)^2-2\sqrt5$",
      r"$\dfrac{\sqrt3+1}{\sqrt3-1}-\dfrac{\sqrt3-1}{\sqrt3+1}$", r"$\dfrac{1}{\sqrt2}+\dfrac{1}{\sqrt2+1}$"]),
     tasks(2, [R(r"5+2\sqrt6"), R("19"), R("-2"), R("6"), r"$\dfrac{(\sqrt3+1)^2-(\sqrt3-1)^2}{2}=" + Rm(r"2\sqrt3") + "$", r"$\dfrac{\sqrt2}{2}+\sqrt2-1=" + Rm(r"\frac{3\sqrt2}{2}-1") + "$"])),
 (2, r"Un cuadrado tiene un área de $50\ \text{cm}^2$. Calcula su lado y su diagonal en forma de radical simplificado.",
     r"Lado: $\sqrt{50}=" + Rm(r"5\sqrt2\ \text{cm}") + r"$. Diagonal: $\sqrt2\cdot5\sqrt2=" + Rm(r"10\ \text{cm}") + r"$."),
]))

# =====================================================================
# 10. Ampliació: logaritmes i problemes
l2, l3 = 0.301, 0.477
L10 = [2 * l2 + l3, 1 - l2, l3 - l2, (l2 + 2 * l3) / 2, l2 + l3 - 2]
ck([round(v, 4) for v in L10], [1.079, 0.699, 0.176, 0.6275, -1.222])
calc = [math.log(20, 3), math.log(60, 0.5), math.log(100, 2), math.log(7)]
ck([round(v, 3) for v in calc], [2.727, -5.907, 6.644, 1.946])
chk([('log(49,7)', 2), ('Rational(1,2)**-3', 8), ('2**-3', 'Rational(1,8)'), ('sqrt(2)**4', 4)])
t_bac = 4 / math.log10(2); t_cap = math.log10(4 / 3) / math.log10(1.04); ph = -math.log10(2.5e-5)
ck([round(t_bac, 2), round(t_cap, 2), math.ceil(t_cap), round(ph, 2)], [13.29, 7.33, 8, 4.6])
assert 2 ** 3 < 10 < 2 ** 4 and 3 ** 2 < 10 < 3 ** 3
S.append(("Ampliación: logaritmos y problemas", [
 (2, r"Halla $x$:" + tasks(4, [r"$\log_x 49=2$", r"$\log_{\frac12}x=-3$", r"$\log_x\frac18=-3$", r"$\log_{\sqrt2}x=4$"]),
     tasks(4, [R("x=7"), R("x=8"), R("x=2"), R("x=4")])),
 (2, r"Sabiendo que $\log2=0,301$ y $\log3=0,477$, calcula sin calculadora:" + tasks(5, [r"$\log12$", r"$\log5$", r"$\log1,5$", r"$\log\sqrt{18}$", r"$\log0,06$"]),
     tasks(2, [r"$2\log2+\log3=" + Rm(dec(L10[0])) + "$", r"$\log\frac{10}2=1-\log2=" + Rm(dec(L10[1])) + "$", r"$\log3-\log2=" + Rm(dec(L10[2])) + "$",
               r"$\frac12(\log2+2\log3)=" + Rm(dec(L10[3], 4)) + "$", r"$\log\frac{6}{100}=\log2+\log3-2=" + Rm(dec(L10[4])) + "$"])),
 (2, r"Desarrolla con las propiedades de los logaritmos y escribe $E$ sin logaritmos:" + tasks(2, [r"$\log\dfrac{100x^3}{y}$", r"$\log\sqrt{\dfrac{x}{y}}$", r"$\log E=\log3+2\log x-\log y$", r"$\log E=2-\log x$"]),
     tasks(2, [R(r"2+3\log x-\log y"), R(r"\tfrac12(\log x-\log y)"), R(r"E=\dfrac{3x^2}{y}"), R(r"E=\dfrac{100}{x}")])),
 (1, r"Con la calculadora (cambio de base), calcula con tres decimales:" + tasks(4, [r"$\log_3 20$", r"$\log_{0,5}60$", r"$\log_2 100$", r"$\ln7$"])
     + recorda(r"$\log_a x=\dfrac{\log x}{\log a}=\dfrac{\ln x}{\ln a}$."),
     tasks(4, [R(dec(v)) for v in calc])),
 (2, r"Una colonia de bacterias se duplica cada hora. ¿Cuántas horas tarda en pasar de 100 bacterias a un millón?",
     r"$100\cdot2^t=10^6\Rightarrow2^t=10^4\Rightarrow t=\log_2 10^4=\dfrac{4}{\log2}\approx" + Rm(dec(t_bac, 2) + r"\ \text{horas}") + "$."),
 (2, r"Ingresamos 1500 € en una cuenta al 4\,\% de interés compuesto anual. ¿Cuántos años deben pasar, como mínimo, para que haya 2000 €?",
     r"$1500\cdot1,04^t=2000\Rightarrow1,04^t=\frac43\Rightarrow t=\dfrac{\log\frac43}{\log1,04}\approx" + dec(t_cap, 2) + r"$. Hacen falta " + R(r"8\ \text{años}") + "."),
 (3, r"El pH de una disolución es $\text{pH}=-\log[\text{H}^+]$. Calcula el pH si $[\text{H}^+]=10^{-3}$ y si $[\text{H}^+]=2,5\cdot10^{-5}$. ¿Cuál es más ácida (pH menor)?",
     r"$\text{pH}=" + Rm("3") + r"$; \ $\text{pH}=-\log(2,5\cdot10^{-5})\approx" + Rm(dec(ph, 2)) + r"$. Es más ácida \rest{la primera}."),
 (3, r"Sin calculadora, ordena de menor a mayor $\log_2 10$, \ $3$ \ y \ $\log_3 10$. Justifícalo.",
     r"$2^3=8<10\Rightarrow\log_210>3$; \ $3^2=9<10<27=3^3\Rightarrow2<\log_310<3$. Por tanto, " + R(r"\log_310<3<\log_210") + "."),
]))

assert [len(x[1]) for x in S][:7] == [1, 2, 1, 2, 7, 1, 3]  # 17 exercicis del departament
build(HERE, 1, "Números reales", S,
      "números reales, intervalos, valor absoluto, potencias, radicales, racionalización, logaritmos",
      r"Resuélvelos en el cuaderno mostrando todos los pasos. Da los resultados de manera exacta (fracciones y radicales simplificados, sin raíces en el denominador). Usa la calculadora solo cuando el enunciado lo diga. Los ejercicios 1--17 son los de la ficha del departamento; las secciones 8, 9 y 10 son de ampliación, para preparar el Bachillerato.",
      r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar los de intervalos, valor absoluto, radicales, racionalización y logaritmos con las herramientas interactivas de los apuntes de la unidad.", lang='es')
