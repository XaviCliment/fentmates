# Versió en castellà de genera.py. Genera t2-fitxa-exercicis-es.tex i t2-fitxa-solucions-es.tex (1r ESO, Unitat 2: Divisibilitat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'

def recorda(t): return '\\recorda{%s}' % t

S = []  # [(títol, [(estrelles, enunciat, solució)])]
Y, N = r'\checkmark', r'$\times$'

# =====================================================================
S.append(("La relación de divisibilidad", [
 (1, r"Haz la división y di si el primer número es múltiplo del segundo:" + tasks(4, [r"$84$ y $7$", r"$95$ y $8$", r"$132$ y $12$", r"$200$ y $15$"])
     + recorda(r"$a$ es \textbf{múltiplo} de $b$ (y $b$ es \textbf{divisor} de $a$) cuando la división $a:b$ es \textbf{exacta}: resto 0."),
     tasks(2, [r"$84=7\cdot12$: \res{\text{sí}}", r"$95=8\cdot11+7$: \res{\text{no}}", r"$132=12\cdot11$: \res{\text{sí}}", r"$200=15\cdot13+5$: \res{\text{no}}"])),
 (1, r"Completa con la palabra \emph{múltiplo} o \emph{divisor}:" + tasks(2, [r"$35$ es \rule{2cm}{0.4pt} de $7$.", r"$9$ es \rule{2cm}{0.4pt} de $63$.", r"$100$ es \rule{2cm}{0.4pt} de $25$.", r"$13$ es \rule{2cm}{0.4pt} de $52$."]),
     tasks(4, [r"múltiplo", r"divisor", r"múltiplo", r"divisor"])),
 (1, r"A partir de la igualdad $8\cdot9=72$, escribe cuatro frases con las palabras \emph{múltiplo} y \emph{divisor}.",
     r"$72$ es múltiplo de $8$; \ $72$ es múltiplo de $9$; \ $8$ es divisor de $72$; \ $9$ es divisor de $72$."),
 (2, r"¿Verdadero o falso? Justifícalo:" + tasks(2, [r"$48$ es divisible por $6$.", r"$7$ es divisor de $77$.", r"$120$ es múltiplo de $9$.", r"$0$ es múltiplo de $15$.", r"$1$ es múltiplo de $3$."]),
     tasks(1, [r"\res{\text{V}}: $48=6\cdot8$.", r"\res{\text{V}}: $77=7\cdot11$.", r"\res{\text{F}}: $120=9\cdot13+3$.", r"\res{\text{V}}: $0=15\cdot0$.", r"\res{\text{F}}: $1:3$ no es exacta (es $3$ el que es múltiplo de $1$)."])),
 (2, r"¿Cuál es el número más pequeño que hay que sumar a $100$ para que el resultado sea múltiplo de $9$? ¿Y el más pequeño que hay que restarle?",
     r"$100=9\cdot11+1$. \ Sumar: $\res{8}$ ($108=9\cdot12$). \ Restar: $\res{1}$ ($99=9\cdot11$)."),
 (3, r"En una división exacta, el divisor es $13$ y el cociente, $17$. ¿Cuál es el dividendo? Con el mismo divisor y cociente, ¿cuál es el dividendo más grande que puede tener una división \emph{no} exacta?",
     r"Exacta: $13\cdot17=\res{221}$. \ El resto como mucho es $12$: $221+12=\res{233}$."),
 (3, r"Halla todos los números de dos cifras que son múltiplos de $7$ y acaban en $4$.",
     r"De los múltiplos de 7 de dos cifras ($14, 21, \ldots, 98$), acaban en 4: $\res{14}$ y $\res{84}$."),
]))

S.append(("Múltiplos de un número", [
 (1, r"Escribe los diez primeros múltiplos (sin el 0) de:" + tasks(3, [r"$7$", r"$11$", r"$15$"]),
     tasks(1, [r"$7,\ 14,\ 21,\ 28,\ 35,\ 42,\ 49,\ 56,\ 63,\ 70$", r"$11,\ 22,\ 33,\ 44,\ 55,\ 66,\ 77,\ 88,\ 99,\ 110$", r"$15,\ 30,\ 45,\ 60,\ 75,\ 90,\ 105,\ 120,\ 135,\ 150$"])),
 (1, r"¿Cuáles de estos números son múltiplos de $6$? \[18\qquad 26\qquad 36\qquad 45\qquad 54\qquad 60\qquad 75\qquad 96\]",
     r"$\res{18,\ 36,\ 54,\ 60,\ 96}$ \ (los demás no dan división exacta entre 6)."),
 (2, r"Escribe los múltiplos de $13$ comprendidos entre $100$ y $170$.",
     r"$100=13\cdot7+9$: el primero es $13\cdot8=104$. \ $\res{104,\ 117,\ 130,\ 143,\ 156,\ 169}$."),
 (2, r"¿Cuántos múltiplos de $9$ hay entre $1$ y $200$? ¿Y entre $100$ y $200$?",
     r"$200:9\to q=22$: \ hay $\res{22}$. \ Hasta $99$ hay $11$, así que entre 100 y 200: $22-11=\res{11}$ (del $108$ al $198$)."),
 (2, r"Escribe los múltiplos comunes de $6$ y de $9$ menores que $100$ (sin el 0). ¿Cuál es el más pequeño?",
     r"$\res{18,\ 36,\ 54,\ 72,\ 90}$. El más pequeño es $18$ (su m.c.m.)."),
 (3, r"¿Cuál es el múltiplo de $17$ más próximo a $300$?",
     r"$300=17\cdot17+11$: los múltiplos más próximos son $289$ (a 11) y $306$ (a 6). \ El más próximo es $\res{306}$."),
 (3, r"Escribe el múltiplo de $12$ más grande que tenga tres cifras y el más pequeño que tenga cuatro.",
     r"$999=12\cdot83+3$: \ $12\cdot83=\res{996}$ \ y \ $12\cdot84=\res{1008}$."),
]))

S.append(("Divisores de un número", [
 (1, r"Calcula todos los divisores de:" + tasks(4, [r"$15$", r"$21$", r"$28$", r"$32$"])
     + recorda(r"Dividimos entre $1, 2, 3\ldots$ Cada división exacta da dos divisores (el divisor y el cociente). Paramos cuando el cociente es menor o igual que el divisor."),
     tasks(2, [r"$\{1,\ 3,\ 5,\ 15\}$", r"$\{1,\ 3,\ 7,\ 21\}$", r"$\{1,\ 2,\ 4,\ 7,\ 14,\ 28\}$", r"$\{1,\ 2,\ 4,\ 8,\ 16,\ 32\}$"])),
 (1, r"¿Cuáles de estos números son divisores de $60$? \[4\qquad 7\qquad 9\qquad 12\qquad 15\qquad 25\qquad 30\]",
     r"$\res{4,\ 12,\ 15,\ 30}$ \ ($60=4\cdot15=12\cdot5=15\cdot4=30\cdot2$)."),
 (2, r"Calcula todos los divisores de:" + tasks(4, [r"$48$", r"$72$", r"$90$", r"$100$"]),
     tasks(1, [r"$\{1,2,3,4,6,8,12,16,24,48\}$", r"$\{1,2,3,4,6,8,9,12,18,24,36,72\}$", r"$\{1,2,3,5,6,9,10,15,18,30,45,90\}$", r"$\{1,2,4,5,10,20,25,50,100\}$"])),
 (2, r"Escribe los divisores comunes de $24$ y de $36$. ¿Cuál es el más grande?",
     r"$\res{1,\ 2,\ 3,\ 4,\ 6,\ 12}$. El más grande es $12$ (su m.c.d.)."),
 (2, r"Pablo tiene 36 cromos y los quiere colocar formando filas, todas con el mismo número de cromos. ¿De cuántas maneras lo puede hacer?",
     r"Tantas como divisores tiene 36: $1\times36,\ 2\times18,\ 3\times12,\ 4\times9,\ 6\times6,\ 9\times4,\ 12\times3,\ 18\times2,\ 36\times1$: \ $\res{9\text{ maneras}}$."),
 (3, r"¿Cuál es el número menor que $50$ que tiene más divisores?",
     r"El $\res{48}$, con 10 divisores: $1, 2, 3, 4, 6, 8, 12, 16, 24, 48$."),
 (3, r"Halla un número que tenga exactamente $4$ divisores y otro que tenga exactamente $5$.",
     r"Por ejemplo, $\res{6}$: $\{1,2,3,6\}$ \ y \ $\res{16}$: $\{1,2,4,8,16\}$."),
]))

TH = r"\textbf{Número} & $\boldsymbol{\div2}$ & $\boldsymbol{\div3}$ & $\boldsymbol{\div5}$ & $\boldsymbol{\div9}$ & $\boldsymbol{\div11}$\\\hline "
def ctab(rows):
    return (r"\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{2.4cm}|C{1.5cm}|C{1.5cm}|C{1.5cm}|C{1.5cm}|C{1.5cm}|}\hline\rowcolor{soft}" + TH
            + ''.join(' & '.join(r) + r'\\\hline ' for r in rows) + r"\end{tabular}\par}")
CN = ['3080', '7425', '1188', '2543', '6735']
CS = {'3080': '2 5 11', '7425': '3 5 9 11', '1188': '2 3 9 11', '2543': '', '6735': '3 5'}
S.append(("Criterios de divisibilidad", [
 (1, r"Completa la tabla: marca con una cruz los números por los que es divisible cada número." + ctab([['$%s$' % n] + [''] * 5 for n in CN])
     + recorda(r"Por \textbf{2}: acaba en cifra par. \ Por \textbf{3}: la suma de las cifras es múltiplo de 3. \ Por \textbf{5}: acaba en 0 o 5. \ Por \textbf{9}: la suma de las cifras es múltiplo de 9. \ Por \textbf{11}: la diferencia entre la suma de las cifras de lugar impar y la de lugar par es 0 o múltiplo de 11."),
     ctab([['$%s$' % n] + [Y if k in CS[n].split() else N for k in ['2', '3', '5', '9', '11']] for n in CN])
     + r"\par El $2543$ no es divisible por ninguno: es impar, las cifras suman 14 y la diferencia para el 11 es $8-6=2$."),
 (1, r"Escribe tres números de tres cifras que sean divisibles por $3$ pero no por $9$.",
     r"Por ejemplo, $\res{102,\ 111,\ 123}$: las cifras suman 3, 3 y 6 (múltiplos de 3, pero no de 9)."),
 (2, r"¿Qué cifras puedes poner en lugar de $\square$ para que $5\square4$ sea divisible por $3$? ¿Y por $9$?",
     r"$5+4=9$. \ Por 3: $\square=0,3,6,9$ \ ($\res{504,\ 534,\ 564,\ 594}$). \ Por 9: $\square=0$ o $9$ \ ($\res{504,\ 594}$)."),
 (2, r"¿Qué cifra hay que poner en lugar de $\square$ para que $38\square$ sea divisible por $2$ y por $3$ a la vez?",
     r"Por 3: $11+\square$ múltiplo de 3, \ $\square=1, 4, 7$. Por 2 tiene que ser par: $\square=4$, \ $\res{384}$."),
 (2, r"Comprueba, con el criterio, si estos números son divisibles por $11$:" + tasks(4, [r"$2849$", r"$9375$", r"$50\,182$", r"$13\,575$"]),
     tasks(2, [r"$(9+8)-(4+2)=11$: \res{\text{sí}}", r"$(7+9)-(5+3)=8$: \res{\text{no}}", r"$(2+1+5)-(8+0)=0$: \res{\text{sí}}", r"$(5+5+1)-(7+3)=1$: \res{\text{no}}"])),
 (3, r"Halla el número más grande de tres cifras que sea divisible por $2$, por $3$ y por $5$ a la vez.",
     r"Tiene que acabar en 0 (por 2 y por 5) y las cifras tienen que sumar un múltiplo de 3: $\res{990}$ ($9+9+0=18$)."),
 (3, r"Halla todas las cifras $a$ y $b$ para que el número $7a2b$ sea divisible por $5$ y por $9$ a la vez.",
     r"Por 5: $b=0$ o $5$. \ Si $b=0$: $9+a$ múltiplo de 9, $a=0$ o $9$. \ Si $b=5$: $14+a$, $a=4$. \ \ $\res{7020,\ 7920,\ 7425}$."),
]))

S.append(("Números primos y compuestos", [
 (1, r"Escribe los divisores de cada número y di si es primo o compuesto:" + tasks(3, [r"$11$", r"$15$", r"$19$", r"$27$", r"$31$", r"$49$"])
     + recorda(r"Un número es \textbf{primo} si solo tiene dos divisores: el 1 y él mismo. Si tiene más, es \textbf{compuesto}. El 1 no es ni primo ni compuesto."),
     tasks(3, [r"$\{1,11\}$: primo", r"$\{1,3,5,15\}$: compuesto", r"$\{1,19\}$: primo", r"$\{1,3,9,27\}$: compuesto", r"$\{1,31\}$: primo", r"$\{1,7,49\}$: compuesto"])),
 (1, r"Escribe todos los números primos comprendidos entre $60$ y $100$.",
     r"$\res{61,\ 67,\ 71,\ 73,\ 79,\ 83,\ 89,\ 97}$."),
 (2, r"Averigua si son primos dividiéndolos entre $2, 3, 5, 7, 11\ldots$ hasta que el cociente sea menor que el divisor:" + tasks(4, [r"$87$", r"$107$", r"$133$", r"$149$"]),
     tasks(2, [r"$87=3\cdot29$: \res{\text{compuesto}}", r"$107:11\to q=9<11$: \res{\text{primo}}", r"$133=7\cdot19$: \res{\text{compuesto}}", r"$149:13\to q=11<13$: \res{\text{primo}}"])),
 (2, r"Escribe cada número como suma de dos números primos:" + tasks(4, [r"$16$", r"$24$", r"$36$", r"$50$"]),
     tasks(2, [r"$3+13=5+11$", r"$5+19=7+17=11+13$", r"$5+31=7+29=13+23=17+19$", r"$3+47=7+43=13+37=19+31$"]) + r"\par (Basta con una manera.)"),
 (2, r"Explica por qué ningún número acabado en $5$, mayor que $5$, puede ser primo. ¿Y por qué ningún número par mayor que $2$ puede ser primo?",
     r"Si acaba en 5, es divisible por 5: tiene al menos los divisores 1, 5 y él mismo. Si es par, es divisible por 2: tiene al menos los divisores 1, 2 y él mismo."),
 (3, r"¿El año $2027$ es un número primo? ¿Y el $2028$?",
     r"$2027$ no es divisible por ningún primo hasta el $43$, y $47\cdot47=2209>2027$: es \res{\text{primo}}. \ $2028$ es par: \res{\text{compuesto}} ($2028=2^{2}\cdot3\cdot13^{2}$)."),
 (3, r"Halla tres números primos consecutivos cuya suma sea también un número primo.",
     r"Por ejemplo, $5+7+11=\res{23}$ \ o \ $7+11+13=\res{31}$."),
]))

S.append(("Descomposición en factores primos", [
 (1, r"Descompón en factores primos:" + tasks(4, [r"$36$", r"$50$", r"$72$", r"$81$"])
     + recorda(r"Dividimos entre el primo más pequeño posible (2, 3, 5, 7\ldots) hasta llegar a 1, y escribimos los factores repetidos como potencia: $\ 360=2^{3}\cdot3^{2}\cdot5$."),
     tasks(4, [r"$2^{2}\cdot3^{2}$", r"$2\cdot5^{2}$", r"$2^{3}\cdot3^{2}$", r"$3^{4}$"])),
 (1, r"Descompón en factores primos:" + tasks(4, [r"$120$", r"$126$", r"$196$", r"$225$"]),
     tasks(4, [r"$2^{3}\cdot3\cdot5$", r"$2\cdot3^{2}\cdot7$", r"$2^{2}\cdot7^{2}$", r"$3^{2}\cdot5^{2}$"])),
 (2, r"Descompón en factores primos:" + tasks(4, [r"$540$", r"$784$", r"$1260$", r"$2310$"]),
     tasks(4, [r"$2^{2}\cdot3^{3}\cdot5$", r"$2^{4}\cdot7^{2}$", r"$2^{2}\cdot3^{2}\cdot5\cdot7$", r"$2\cdot3\cdot5\cdot7\cdot11$"])),
 (2, r"¿Qué número tiene cada descomposición?" + tasks(4, [r"$2^{4}\cdot3$", r"$2\cdot3^{2}\cdot7$", r"$2^{2}\cdot5^{3}$", r"$3\cdot5\cdot11$"]),
     tasks(4, [r"$48$", r"$126$", r"$500$", r"$165$"])),
 (2, r"Completa las descomposiciones:" + tasks(3, [r"$2^{\square}\cdot3\cdot5^{\square}=600$", r"$2^{2}\cdot3^{\square}\cdot7=252$", r"$2\cdot\square^{2}\cdot5=90$"]),
     tasks(3, [r"$2^{3}\cdot3\cdot5^{2}$", r"$2^{2}\cdot3^{2}\cdot7$", r"$2\cdot3^{2}\cdot5$"])),
 (3, r"¿Por qué número, el más pequeño posible, hay que multiplicar $90$ para que el resultado sea un cuadrado perfecto?",
     r"$90=2\cdot3^{2}\cdot5$: falta un 2 y un 5 para que todos los exponentes sean pares. Por $\res{10}$: $900=2^{2}\cdot3^{2}\cdot5^{2}=30^{2}$."),
 (3, r"Un número tiene la descomposición $2^{2}\cdot3\cdot5$. ¿Qué número es? Escribe todos sus divisores.",
     r"Es el $60$. \ Divisores: $\res{1,\ 2,\ 3,\ 4,\ 5,\ 6,\ 10,\ 12,\ 15,\ 20,\ 30,\ 60}$."),
]))

S.append(("Mínimo común múltiplo", [
 (1, r"Calcula el m.c.m. escribiendo la lista de múltiplos:" + tasks(4, [r"$\text{m.c.m.}(3,4)$", r"$\text{m.c.m.}(6,9)$", r"$\text{m.c.m.}(8,10)$", r"$\text{m.c.m.}(5,15)$"]),
     tasks(4, [r"$12$", r"$18$", r"$40$", r"$15$"])),
 (1, r"Calcula el m.c.m. a partir de la descomposición en factores primos:" + tasks(4, [r"$\text{m.c.m.}(12,20)$", r"$\text{m.c.m.}(18,30)$", r"$\text{m.c.m.}(24,36)$", r"$\text{m.c.m.}(14,21)$"])
     + recorda(r"\textbf{m.c.m.}: factores \textbf{comunes y no comunes}, cada uno con el \textbf{mayor} exponente."),
     tasks(2, [r"$2^{2}\cdot3\cdot5=\res{60}$", r"$2\cdot3^{2}\cdot5=\res{90}$", r"$2^{3}\cdot3^{2}=\res{72}$", r"$2\cdot3\cdot7=\res{42}$"])),
 (2, r"Calcula:" + tasks(4, [r"$\text{m.c.m.}(40,60)$", r"$\text{m.c.m.}(36,54)$", r"$\text{m.c.m.}(45,75)$", r"$\text{m.c.m.}(28,42)$"]),
     tasks(2, [r"$2^{3}\cdot3\cdot5=\res{120}$", r"$2^{2}\cdot3^{3}=\res{108}$", r"$3^{2}\cdot5^{2}=\res{225}$", r"$2^{2}\cdot3\cdot7=\res{84}$"])),
 (2, r"Calcula:" + tasks(3, [r"$\text{m.c.m.}(6,8,12)$", r"$\text{m.c.m.}(10,12,15)$", r"$\text{m.c.m.}(8,18,27)$"]),
     tasks(3, [r"$2^{3}\cdot3=\res{24}$", r"$2^{2}\cdot3\cdot5=\res{60}$", r"$2^{3}\cdot3^{3}=\res{216}$"])),
 (2, r"Calcula sin descomponer y explica cómo lo has hecho:" + tasks(4, [r"$\text{m.c.m.}(9,10)$", r"$\text{m.c.m.}(7,35)$", r"$\text{m.c.m.}(11,13)$", r"$\text{m.c.m.}(16,48)$"]),
     tasks(2, [r"$\res{90}$: no tienen factores comunes", r"$\res{35}$: 35 es múltiplo de 7", r"$\res{143}$: los dos son primos", r"$\res{48}$: 48 es múltiplo de 16"])),
 (3, r"Calcula el m.c.m. de $\ a=2^{3}\cdot3^{2}\cdot7\ $ y $\ b=2^{2}\cdot3^{3}\cdot5$.",
     r"$2^{3}\cdot3^{3}\cdot5\cdot7=8\cdot27\cdot35=\res{7560}$."),
 (3, r"El m.c.m. de dos números es $60$ y uno de ellos es $12$. ¿Qué valores puede tener el otro?",
     r"$60=2^{2}\cdot3\cdot5$ y $12=2^{2}\cdot3$: el otro tiene que dividir a 60 y tener el factor 5. \ $\res{5,\ 10,\ 15,\ 20,\ 30,\ 60}$."),
]))

S.append(("Problemas de m.c.m.", [
 (1, r"Un faro se enciende cada $9$ segundos y otro, cada $12$. Si ahora se han encendido los dos a la vez, ¿dentro de cuánto tiempo volverán a coincidir?"
     + recorda(r"Si hay cosas que se \textbf{repiten} y queremos saber cuándo volverán a \textbf{coincidir}, o buscamos el número \textbf{más pequeño} que es múltiplo de varios, usamos el \textbf{m.c.m.}"),
     r"$\text{m.c.m.}(9,12)=2^{2}\cdot3^{2}=\res{36\text{ s}}$."),
 (1, r"Lucía entrena a fútbol cada $3$ días y va a natación cada $4$. Hoy ha hecho las dos cosas. ¿Dentro de cuántos días las volverá a hacer el mismo día?",
     r"$\text{m.c.m.}(3,4)=\res{12\text{ días}}$."),
 (2, r"Tres amigos van al cine: uno cada $6$ días, otro cada $8$ y el otro cada $10$. Si hoy han coincidido, ¿dentro de cuántos días volverán a coincidir?",
     r"$\text{m.c.m.}(6,8,10)=2^{3}\cdot3\cdot5=\res{120\text{ días}}$."),
 (2, r"¿Cuál es el número más pequeño de lápices que se puede empaquetar en cajas de $12$, de $15$ o de $18$ sin que sobre ninguno?",
     r"$\text{m.c.m.}(12,15,18)=2^{2}\cdot3^{2}\cdot5=\res{180\text{ lápices}}$."),
 (2, r"Dos autobuses salen juntos de la parada a las 7:30. Uno vuelve cada $20$ minutos y el otro, cada $25$. ¿A qué hora volverán a coincidir?",
     r"$\text{m.c.m.}(20,25)=2^{2}\cdot5^{2}=100$ min $=1$ h $40$ min: \ a las $\res{9{:}10}$."),
 (3, r"Si agrupamos las galletas de una caja de $6$ en $6$, de $8$ en $8$ o de $10$ en $10$, siempre sobran $3$. ¿Cuántas galletas hay como mínimo? ¿Y si sabemos que hay entre $200$ y $300$?",
     r"$\text{m.c.m.}(6,8,10)=120$: como mínimo $120+3=\res{123}$. \ Entre 200 y 300: $240+3=\res{243}$."),
 (3, r"Una rueda dentada de $15$ dientes engrana con otra de $24$ dientes. ¿Cuántas vueltas tiene que dar cada una para que vuelvan a estar en la posición inicial?",
     r"$\text{m.c.m.}(15,24)=2^{3}\cdot3\cdot5=120$ dientes: \ la primera da $120:15=\res{8\text{ vueltas}}$ y la segunda, $120:24=\res{5\text{ vueltas}}$."),
]))

S.append(("Máximo común divisor", [
 (1, r"Calcula el m.c.d. escribiendo la lista de divisores:" + tasks(4, [r"$\text{m.c.d.}(8,12)$", r"$\text{m.c.d.}(15,20)$", r"$\text{m.c.d.}(18,27)$", r"$\text{m.c.d.}(14,25)$"]),
     tasks(4, [r"$4$", r"$5$", r"$9$", r"$1$"])),
 (1, r"Calcula el m.c.d. a partir de la descomposición en factores primos:" + tasks(4, [r"$\text{m.c.d.}(24,36)$", r"$\text{m.c.d.}(30,45)$", r"$\text{m.c.d.}(42,56)$", r"$\text{m.c.d.}(60,90)$"])
     + recorda(r"\textbf{m.c.d.}: \textbf{solo} los factores \textbf{comunes}, cada uno con el \textbf{menor} exponente. Si no hay ninguno común, el m.c.d. es 1 (\emph{primos entre sí})."),
     tasks(2, [r"$2^{2}\cdot3=\res{12}$", r"$3\cdot5=\res{15}$", r"$2\cdot7=\res{14}$", r"$2\cdot3\cdot5=\res{30}$"])),
 (2, r"Calcula:" + tasks(4, [r"$\text{m.c.d.}(84,126)$", r"$\text{m.c.d.}(120,180)$", r"$\text{m.c.d.}(96,144)$", r"$\text{m.c.d.}(105,165)$"]),
     tasks(2, [r"$2\cdot3\cdot7=\res{42}$", r"$2^{2}\cdot3\cdot5=\res{60}$", r"$2^{4}\cdot3=\res{48}$", r"$3\cdot5=\res{15}$"])),
 (2, r"Calcula:" + tasks(3, [r"$\text{m.c.d.}(12,18,30)$", r"$\text{m.c.d.}(24,40,56)$", r"$\text{m.c.d.}(45,75,105)$"]),
     tasks(3, [r"$2\cdot3=\res{6}$", r"$2^{3}=\res{8}$", r"$3\cdot5=\res{15}$"])),
 (2, r"¿Cuáles de estas parejas son primos entre sí?" + tasks(4, [r"$8$ y $21$", r"$15$ y $25$", r"$14$ y $27$", r"$22$ y $33$"]),
     tasks(2, [r"\res{\text{sí}} ($\text{m.c.d.}=1$)", r"no ($\text{m.c.d.}=5$)", r"\res{\text{sí}} ($\text{m.c.d.}=1$)", r"no ($\text{m.c.d.}=11$)"])),
 (3, r"Calcula el m.c.d. y el m.c.m. de $36$ y $60$, y comprueba que $\text{m.c.d.}\cdot\text{m.c.m.}=36\cdot60$.",
     r"$36=2^{2}\cdot3^{2}$, \ $60=2^{2}\cdot3\cdot5$: \ $\text{m.c.d.}=\res{12}$, \ $\text{m.c.m.}=\res{180}$. \ $12\cdot180=2160=36\cdot60$ \checkmark"),
 (3, r"El m.c.d. de dos números es $8$ y su m.c.m., $96$. Si uno de los números es $24$, ¿cuál es el otro?",
     r"$\text{m.c.d.}\cdot\text{m.c.m.}=a\cdot b$: \ $8\cdot96=768$; \ $768:24=\res{32}$."),
]))

S.append(("Problemas de m.c.d.", [
 (1, r"Tenemos $30$ manzanas y $45$ naranjas y queremos hacer el máximo número de lotes iguales, sin que sobre ninguna fruta. ¿Cuántos lotes podemos hacer? ¿Qué llevará cada lote?"
     + recorda(r"Si queremos \textbf{repartir} o \textbf{cortar} en partes iguales, \textbf{sin que sobre nada}, y las partes tienen que ser \textbf{lo más grandes posible} (o el máximo número de grupos), usamos el \textbf{m.c.d.}"),
     r"$\text{m.c.d.}(30,45)=15$: \ $\res{15\text{ lotes}}$, cada uno con $2$ manzanas y $3$ naranjas."),
 (1, r"Queremos cortar dos cuerdas de $36$ m y $48$ m en trozos iguales, lo más largos posible. ¿Cuánto medirá cada trozo? ¿Cuántos trozos tendremos?",
     r"$\text{m.c.d.}(36,48)=\res{12\text{ m}}$; \ $3+4=\res{7\text{ trozos}}$."),
 (2, r"Queremos embaldosar un suelo de $360$ cm por $280$ cm con baldosas cuadradas, lo más grandes posible, sin cortar ninguna. ¿Cuánto medirá el lado de cada baldosa? ¿Cuántas baldosas hacen falta?",
     r"$\text{m.c.d.}(360,280)=2^{3}\cdot5=\res{40\text{ cm}}$; \ $9\cdot7=\res{63\text{ baldosas}}$."),
 (2, r"Una librería tiene $120$ libros de cuentos, $84$ de poesía y $60$ cómics. Quiere hacer paquetes con el mismo número de libros, todos de un solo tipo y lo más grandes posible. ¿Cuántos libros habrá en cada paquete? ¿Cuántos paquetes hará?",
     r"$\text{m.c.d.}(120,84,60)=\res{12\text{ libros}}$; \ $10+7+5=\res{22\text{ paquetes}}$."),
 (2, r"Di si hay que calcular el m.c.m. o el m.c.d. y resuelve:" + tasks(1, [r"Un reloj suena cada $15$ minutos y otro, cada $25$. Si ahora han sonado juntos, ¿cuándo volverán a coincidir?", r"Queremos repartir $48$ bolígrafos y $64$ lápices en el máximo número de estuches iguales, sin que sobre ninguno."]),
     tasks(1, [r"m.c.m.: $\text{m.c.m.}(15,25)=\res{75\text{ min}}$.", r"m.c.d.: $\text{m.c.d.}(48,64)=\res{16\text{ estuches}}$, con 3 bolígrafos y 4 lápices cada uno."])),
 (3, r"Una maestra reparte $75$ cromos y $105$ pegatinas entre el alumnado, de manera que todos reciben la misma cantidad de cada cosa. Le sobran $3$ cromos y $9$ pegatinas. ¿Cuántos alumnos puede haber, como máximo? ¿Cuántos cromos y pegatinas recibe cada uno?",
     r"Se han repartido $72$ cromos y $96$ pegatinas: \ $\text{m.c.d.}(72,96)=\res{24\text{ alumnos}}$ (más grande que 9). Cada uno recibe $\res{3}$ cromos y $\res{4}$ pegatinas."),
 (3, r"Queremos plantar árboles alrededor de un jardín rectangular de $72$ m por $48$ m, a la misma distancia entre ellos, la mayor posible y con un árbol en cada esquina. ¿A qué distancia los plantaremos? ¿Cuántos árboles hacen falta?",
     r"$\text{m.c.d.}(72,48)=\res{24\text{ m}}$. \ Perímetro: $2\cdot(72+48)=240$ m; \ $240:24=\res{10\text{ árboles}}$."),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 2: Divisibilidad' % t, capcalera='%s · Unidad 2: Divisibilidad' % t,
                 pdfkeywords='divisibilidad, múltiplos, divisores, criterios de divisibilidad, números primos, factores primos, m.c.m., m.c.d.',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 2' if sol else 'Ficha de ejercicios · Unidad 2') + '}{Divisibilidad}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. La tabla se puede completar directamente en la ficha. Haz los cálculos sin calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't2-fitxa-solucions-es.tex' if sol else 't2-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
