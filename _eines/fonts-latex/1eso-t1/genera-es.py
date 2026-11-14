# Versió en castellà de genera.py. Genera t1-fitxa-exercicis-es.tex i t1-fitxa-solucions-es.tex (1r ESO, Unitat 1: Nombres naturals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'

RECORDA = []  # (secció, text) quadres de recordatori, només a la fitxa d'exercicis
def recorda(t): return '\\recorda{%s}' % t

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Los números naturales", [
 (1, r"Escribe con cifras:" + tasks(2, [r"Veintitrés mil cuatrocientos siete.", r"Ciento cinco mil sesenta.", r"Dos millones trescientos mil.", r"Siete millones cincuenta mil nueve."]),
     tasks(4, [r"$23\,407$", r"$105\,060$", r"$2\,300\,000$", r"$7\,050\,009$"])),
 (1, r"Escribe con letras:" + tasks(4, [r"$4090$", r"$15\,600$", r"$308\,012$", r"$2\,040\,500$"]),
     tasks(2, [r"Cuatro mil noventa.", r"Quince mil seiscientos.", r"Trescientos ocho mil doce.", r"Dos millones cuarenta mil quinientos."])),
 (1, r"¿Qué valor tiene la cifra 7 en cada uno de estos números?" + tasks(6, [r"$4718$", r"$73\,052$", r"$1207$", r"$7\,300\,000$", r"$25\,070$", r"$870\,412$"]),
     tasks(6, [r"$700$", r"$70\,000$", r"$7$", r"$7\,000\,000$", r"$70$", r"$70\,000$"])),
 (2, r"Ordena de menor a mayor: \[45\,099\qquad 45\,909\qquad 4599\qquad 45\,990\qquad 49\,059\]",
     r"$4599<45\,099<45\,909<45\,990<49\,059$ \ (el de cuatro cifras es el más pequeño; los demás se comparan cifra a cifra de izquierda a derecha)."),
 (2, r"Escribe el número anterior y el siguiente de:" + tasks(4, [r"$1000$", r"$39\,999$", r"$100\,000$", r"$2\,009\,999$"]),
     tasks(2, [r"$999$ \ y \ $1001$", r"$39\,998$ \ y \ $40\,000$", r"$99\,999$ \ y \ $100\,001$", r"$2\,009\,998$ \ y \ $2\,010\,000$"])),
 (2, r"Responde:" + tasks(1, [r"¿Cuántas decenas tiene en total el número $3450$?", r"¿Cuántas centenas tiene en total el número $72\,000$?", r"¿Cuántas unidades de millar tiene un millón?"]),
     tasks(3, [r"$\res{345}$ decenas", r"$\res{720}$ centenas", r"$\res{1000}$ millares"])),
 (3, r"Con las cifras 4, 0, 9, 2 y 6, sin repetir ninguna, escribe:" + tasks(1, [r"El número de cinco cifras más grande posible.", r"El número de cinco cifras más pequeño posible (recuerda que no puede empezar por 0).", r"El número de cinco cifras más grande que sea impar."]),
     tasks(1, [r"$\res{96\,420}$ (cifras de mayor a menor).", r"$\res{20\,469}$ (empezamos por la cifra más pequeña que no es 0).", r"Tiene que acabar en 9, la única cifra impar: $\res{64\,209}$."])),
 (3, r"¿Cuántos números de tres cifras empiezan por 5? ¿Y cuántos números de cuatro cifras hay en total?",
     r"Del $500$ al $599$: $\res{100}$ números. \ Del $1000$ al $9999$: $9999-999=\res{9000}$ números."),
]))

S.append(("Aproximación: truncamiento y redondeo", [
 (1, r"Trunca los números siguientes a las decenas y a las centenas:" + tasks(3, [r"$1257$", r"$32\,041$", r"$57\,623$", r"$12\,354$", r"$3462$", r"$23\,465\,244$"]),
     tasks(3, [r"$1250$ \ y \ $1200$", r"$32\,040$ \ y \ $32\,000$", r"$57\,620$ \ y \ $57\,600$", r"$12\,350$ \ y \ $12\,300$", r"$3460$ \ y \ $3400$", r"$23\,465\,240$ \ y \ $23\,465\,200$"])),
 (1, r"Redondea los números del ejercicio anterior a las decenas y a las centenas. ¿En qué casos no coinciden el redondeo y el truncamiento? ¿Cuál de los dos se acerca más al número de partida?",
     tasks(3, [r"$1260$ \ y \ $1300$", r"$32\,040$ \ y \ $32\,000$", r"$57\,620$ \ y \ $57\,600$", r"$12\,350$ \ y \ $12\,400$", r"$3460$ \ y \ $3500$", r"$23\,465\,240$ \ y \ $23\,465\,200$"])
     + r"\par No coinciden en a) (decenas y centenas), d) (centenas) y e) (centenas). El \textbf{redondeo} siempre da el número más próximo."),
 (2, r"Completa la tabla aproximando a las unidades de millar:\par\smallskip{\renewcommand{\arraystretch}{1.6}\centering\begin{tabular}{|C{3.6cm}|C{3.6cm}|C{3.6cm}|}\hline\rowcolor{soft}\textbf{Número} & \textbf{Truncamiento} & \textbf{Redondeo}\\\hline $45\,678$ & & \\\hline $129\,350$ & & \\\hline $9499$ & & \\\hline $70\,501$ & & \\\hline $999\,600$ & & \\\hline\end{tabular}\par}",
     r"\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{3.6cm}|C{3.6cm}|C{3.6cm}|}\hline\rowcolor{soft}\textbf{Número} & \textbf{Truncamiento} & \textbf{Redondeo}\\\hline $45\,678$ & $45\,000$ & $46\,000$\\\hline $129\,350$ & $129\,000$ & $129\,000$\\\hline $9499$ & $9000$ & $9000$\\\hline $70\,501$ & $70\,000$ & $71\,000$\\\hline $999\,600$ & $999\,000$ & $1\,000\,000$\\\hline\end{tabular}\par}"),
 (2, r"Redondea (¡cuidado con los nueves!):" + tasks(2, [r"$3995$ a las decenas.", r"$59\,960$ a las centenas.", r"$199\,500$ a las unidades de millar.", r"$2\,970\,000$ a las centenas de millar."]),
     tasks(4, [r"$4000$", r"$60\,000$", r"$200\,000$", r"$3\,000\,000$"])),
 (2, r"Un televisor cuesta $1349$ €. Redondea el precio a las decenas y a las centenas y calcula el error que se comete en cada caso.",
     r"Decenas: $\res{1350\text{ €}}$, error $1350-1349=1$ €. \ Centenas: $\res{1300\text{ €}}$, error $1349-1300=49$ €."),
 (3, r"Al redondear un número a las centenas se ha obtenido $8300$. ¿Cuál es el número más pequeño que podía ser? ¿Y el más grande?",
     r"Del $\res{8250}$ (sube) hasta el $\res{8349}$ (se queda igual)."),
 (3, r"A un partido van $48\,652$ espectadores. Un periódico titula «Casi $49\,000$ espectadores» y otro, «Más de $48\,000$ espectadores». ¿Qué periódico ha redondeado y cuál ha truncado? ¿Cuál se equivoca menos?",
     r"El primero ha \textbf{redondeado} (error $348$) y el segundo ha \textbf{truncado} (error $652$). Se equivoca menos el primero."),
]))

S.append(("Operaciones con números naturales", [
 (1, r"Calcula:" + tasks(2, [r"$3458+976+12\,045$", r"$20\,000-7386$", r"$507\cdot36$", r"$2300\cdot400$"]),
     tasks(4, [r"$16\,479$", r"$12\,614$", r"$18\,252$", r"$920\,000$"])),
 (1, r"Haz estas divisiones y compruébalas con la prueba $D=d\cdot q+r$:" + tasks(4, [r"$8745:15$", r"$9236:24$", r"$52\,000:125$", r"$7000:63$"]),
     tasks(2, [r"$q=583,\ r=0$ \ (exacta)", r"$q=384,\ r=20$: \ $24\cdot384+20=9236$", r"$q=416,\ r=0$ \ (exacta)", r"$q=111,\ r=7$: \ $63\cdot111+7=7000$"])),
 (2, r"Completa la tabla de divisiones:\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{2.6cm}|C{2.6cm}|C{2.6cm}|C{2.6cm}|}\hline\rowcolor{soft}\textbf{Dividendo} & \textbf{Divisor} & \textbf{Cociente} & \textbf{Resto}\\\hline & $12$ & $35$ & $7$\\\hline $500$ & & $41$ & $8$\\\hline $1000$ & $27$ & & \\\hline & $25$ & $18$ & $24$\\\hline\end{tabular}\par}",
     r"\par\smallskip{\renewcommand{\arraystretch}{1.4}\centering\begin{tabular}{|C{2.6cm}|C{2.6cm}|C{2.6cm}|C{2.6cm}|}\hline\rowcolor{soft}\textbf{Dividendo} & \textbf{Divisor} & \textbf{Cociente} & \textbf{Resto}\\\hline $427$ & $12$ & $35$ & $7$\\\hline $500$ & $12$ & $41$ & $8$\\\hline $1000$ & $27$ & $37$ & $1$\\\hline $474$ & $25$ & $18$ & $24$\\\hline\end{tabular}\par}"
     r"\smallskip Para el divisor: $(500-8):41=492:41=12$."),
 (2, r"Calcula mentalmente aplicando las propiedades de las operaciones:" + tasks(3, [r"$25\cdot17\cdot4$", r"$38+57+62+43$", r"$13\cdot99$", r"$8\cdot125$", r"$36\cdot7+36\cdot3$", r"$45\cdot102$"]),
     tasks(3, [r"$(25\cdot4)\cdot17=\res{1700}$", r"$100+100=\res{200}$", r"$13\cdot100-13=\res{1287}$", r"$\res{1000}$", r"$36\cdot(7+3)=\res{360}$", r"$45\cdot100+45\cdot2=\res{4590}$"])),
 (1, r"Calcula, respetando la jerarquía de las operaciones:" + tasks(2, [r"$40:8+15-4\cdot3$", r"$4\cdot7-18:3-2\cdot5$", r"$36:(5+4)+7$", r"$9\cdot3-4\cdot(11-6)$", r"$30-4\cdot(3+2)+5$", r"$(16+8):3-2\cdot4$", r"$3\cdot(5+4)-2\cdot(7-3)$", r"$50-6\cdot(12-3\cdot2)$"])
     + recorda(r"Orden de las operaciones: \textbf{1)} paréntesis y corchetes (de dentro hacia fuera); \textbf{2)} potencias y raíces; \textbf{3)} multiplicaciones y divisiones, de izquierda a derecha; \textbf{4)} sumas y restas, de izquierda a derecha."),
     tasks(4, [r"$5+15-12=\res{8}$", r"$28-6-10=\res{12}$", r"$4+7=\res{11}$", r"$27-20=\res{7}$", r"$30-20+5=\res{15}$", r"$8-8=\res{0}$", r"$27-8=\res{19}$", r"$50-36=\res{14}$"])),
 (2, r"Calcula:" + tasks(1, [r"$4\cdot6+3\cdot(8-5)-(12-7)\cdot3$", r"$9\cdot5-3\cdot(4+6)-48:8\cdot2$", r"$2\cdot(6+3\cdot4-8)+5\cdot4:2-(3+6)\cdot2$", r"$5\cdot[2+3\cdot(4+1)-7]+42:6$", r"$[(9+6):5+2\cdot4]\cdot2-96:12$", r"$25-4\cdot(9-2\cdot3)-[(2+3)\cdot4-6\cdot3]$"]),
     tasks(1, [r"$24+9-15=\res{18}$", r"$45-30-6\cdot2=45-30-12=\res{3}$", r"$2\cdot10+10-18=\res{12}$", r"$5\cdot[2+15-7]+7=5\cdot10+7=\res{57}$", r"$[3+8]\cdot2-8=22-8=\res{14}$", r"$25-12-[20-18]=13-2=\res{11}$"])),
 (3, r"Calcula:" + tasks(1, [r"$[50-(4+2)\cdot7]\cdot3-2\cdot[(9-5)\cdot3-4]$", r"$100-3\cdot[20-2\cdot(15-4\cdot3)]:7$"]),
     tasks(1, [r"$[50-42]\cdot3-2\cdot[12-4]=24-16=\res{8}$", r"$100-3\cdot[20-2\cdot3]:7=100-3\cdot14:7=100-42:7=100-6=\res{94}$"])),
 (3, r"Pon paréntesis donde haga falta para que cada igualdad sea cierta:" + tasks(3, [r"$6+4\cdot5-3=47$", r"$6+4\cdot5-3=14$", r"$6+4\cdot5-3=20$"]),
     tasks(3, [r"$(6+4)\cdot5-3=47$", r"$6+4\cdot(5-3)=14$", r"$(6+4)\cdot(5-3)=20$"])),
]))

S.append(("Problemas con números naturales", [
 (1, r"En un colegio se han comprado 36 balones por $612$ €. ¿Cuánto ha costado cada balón?",
     r"$612:36=\res{17\text{ €}}$ cada balón."),
 (1, r"Un pastelero hace cada día 13 docenas de pasteles de crema. ¿Cuántos habrá hecho en el mes de enero si ha tenido 6 días de fiesta?",
     r"Trabaja $31-6=25$ días y hace $13\cdot12=156$ pasteles al día: \ $156\cdot25=\res{3900\text{ pasteles}}$."),
 (1, r"Para repoblar un río se vierten 45 cajas con 758 alevines cada una. De cada caja mueren 27. ¿Cuántos alevines sobreviven?",
     r"De cada caja sobreviven $758-27=731$: \ $731\cdot45=\res{32\,895\text{ alevines}}$."),
 (2, r"Un agricultor tiene dos campos. En el primero recoge 34 cajas de manzanas y en el segundo, 12. Todas las cajas pesan 15 kg. ¿Cuánto cobrará si le pagan las manzanas a 2 € el kilo?",
     r"$(34+12)\cdot15=46\cdot15=690$ kg; \ $690\cdot2=\res{1380\text{ €}}$."),
 (2, r"En una obra trabajan 43 obreros, 7 horas cada día. La obra dura 147 días y cada obrero cobra 15 € por hora. ¿Cuánto han cobrado entre todos?",
     r"$43\cdot7\cdot147\cdot15=301\cdot147\cdot15=44\,247\cdot15=\res{663\,705\text{ €}}$."),
 (2, r"Los cuatro grupos de 1\textsuperscript{o} de ESO (de 28, 27, 29 y 26 alumnos) van de excursión con 8 profesores. Los autobuses tienen 55 plazas. ¿Cuántos autobuses hacen falta? Si cada autobús cuesta $330$ € y el precio lo pagan solo los alumnos a partes iguales, ¿cuánto paga cada alumno?",
     r"Alumnos: $28+27+29+26=110$; personas: $118$. \ $118:55\to q=2,\ r=8$: hacen falta \res{3\text{ autobuses}}.\\ $3\cdot330=990$ €; \ $990:110=\res{9\text{ €}}$ por alumno."),
 (2, r"Un camión transporta $23\,400$ botellas. En un accidente se rompe la tercera parte. ¿Cuántas cajas de 12 botellas hacen falta para guardar las que no se han roto?",
     r"Rotas: $23\,400:3=7800$. \ Enteras: $23\,400-7800=15\,600$. \ $15\,600:12=\res{1300\text{ cajas}}$."),
 (2, r"Un barco ha cobrado $9100$ € por $1300$ kg de merluza. ¿Cuánto cobrará otro barco por $1750$ kg de merluza de la misma calidad?",
     r"Precio de un kilo: $9100:1300=7$ €. \ $1750\cdot7=\res{12\,250\text{ €}}$."),
 (3, r"En una papelería hay la oferta «Paga 4 y llévate 5». He vuelto a casa con 20 rotuladores y he pagado $64$ €. ¿Cuánto cuesta cada rotulador?",
     r"De cada 5 pago 4: de los 20 he pagado $20:5\cdot4=16$. \ $64:16=\res{4\text{ €}}$ cada rotulador."),
 (3, r"Un cine tiene 24 filas de 18 asientos. En una sesión se han vendido 350 entradas a 7 €. ¿Cuántos asientos han quedado vacíos? ¿Cuánto se ha recaudado? ¿Cuánto dinero más se habría recaudado si se hubieran vendido todas las entradas?",
     r"Asientos: $24\cdot18=432$; vacíos: $432-350=\res{82}$. \ Recaudado: $350\cdot7=\res{2450\text{ €}}$.\\ Lleno: $432\cdot7=3024$ €; \ $3024-2450=\res{574\text{ €}}$ más."),
 (3, r"Una familia compra un sofá de $1380$ €. Paga $300$ € en el momento de la compra y el resto en cuotas mensuales de $90$ €. ¿Cuántas cuotas tendrá que pagar?",
     r"Faltan $1380-300=1080$ €. \ $1080:90=\res{12\text{ cuotas}}$ (un año)."),
]))

S.append(("Potencias", [
 (1, r"Escribe cada potencia como un producto y calcula su valor:" + tasks(5, [r"$3^{2}$", r"$5^{3}$", r"$7^{1}$", r"$2^{5}$", r"$9^{2}$", r"$6^{3}$", r"$0^{5}$", r"$1^{7}$", r"$4^{4}$", r"$11^{2}$"])
     + recorda(r"$a^{n}=\underbrace{a\cdot a\cdots a}_{n\text{ veces}}$ \qquad $a^{1}=a$ \qquad $1^{n}=1$ \qquad $0^{n}=0$. \quad ¡Cuidado: $2^{3}=2\cdot2\cdot2=8$, no $2\cdot3$!"),
     tasks(2, [r"$3\cdot3=9$", r"$5\cdot5\cdot5=125$", r"$7$", r"$2\cdot2\cdot2\cdot2\cdot2=32$", r"$9\cdot9=81$", r"$6\cdot6\cdot6=216$", r"$0\cdot0\cdot0\cdot0\cdot0=0$", r"$1\cdot1\cdot1\cdot1\cdot1\cdot1\cdot1=1$", r"$4\cdot4\cdot4\cdot4=256$", r"$11\cdot11=121$"])),
 (1, r"Escribe en forma de potencia y explica cómo se lee:" + tasks(4, [r"$7\cdot7\cdot7\cdot7$", r"$12\cdot12$", r"$2\cdot2\cdot2\cdot2\cdot2\cdot2$", r"$8\cdot8\cdot8$"]),
     tasks(2, [r"$7^{4}$: siete elevado a cuatro", r"$12^{2}$: doce al cuadrado", r"$2^{6}$: dos elevado a seis", r"$8^{3}$: ocho al cubo"])),
 (2, r"Escribe estos números en forma de potencia (de todas las maneras que sepas):" + tasks(6, [r"$49$", r"$125$", r"$32$", r"$1000$", r"$81$", r"$64$"]),
     tasks(3, [r"$7^{2}$", r"$5^{3}$", r"$2^{5}$", r"$10^{3}$", r"$9^{2}=3^{4}$", r"$8^{2}=4^{3}=2^{6}$"])),
 (2, r"Escribe el signo $<$, $>$ o $=$:" + tasks(4, [r"$2^{5}\ \square\ 5^{2}$", r"$3^{4}\ \square\ 4^{3}$", r"$2^{4}\ \square\ 4^{2}$", r"$10^{2}\ \square\ 2^{10}$"]),
     tasks(4, [r"$32>25$", r"$81>64$", r"$16=16$", r"$100<1024$"])),
 (2, r"Completa la tabla:\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|}\hline\rowcolor{soft}$n$ & $4$ & $7$ & $11$ & $13$ & $20$\\\hline $n^{2}$ & & & & & \\\hline $n^{3}$ & & & & & \\\hline\end{tabular}\par}",
     r"\par\smallskip{\renewcommand{\arraystretch}{1.4}\centering\begin{tabular}{|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|}\hline\rowcolor{soft}$n$ & $4$ & $7$ & $11$ & $13$ & $20$\\\hline $n^{2}$ & $16$ & $49$ & $121$ & $169$ & $400$\\\hline $n^{3}$ & $64$ & $343$ & $1331$ & $2197$ & $8000$\\\hline\end{tabular}\par}"),
 (3, r"En una sala de un museo hay 3 paredes con 3 cuadros en cada una; en cada cuadro aparecen 3 personas y cada persona lleva 3 flores. ¿Cuántas flores hay en total? ¿Y si Pedro tiene 6 bolsillos con 6 llaveros en cada uno y 6 llaves en cada llavero, cuántas llaves tiene? Expresa los resultados como potencias y calcúlalas.",
     r"Flores: $3\cdot3\cdot3\cdot3=3^{4}=\res{81}$. \ Llaves: $6\cdot6\cdot6=6^{3}=\res{216}$."),
 (3, r"Una bacteria se divide en dos cada hora. Si empezamos con una bacteria, ¿cuántas habrá al cabo de 1 hora? ¿Y de 2 horas? Expresa como potencia cuántas habrá al cabo de 10 horas y calcúlalo.",
     r"1 hora: $2$; \ 2 horas: $2^{2}=4$; \ 10 horas: $2^{10}=\res{1024\text{ bacterias}}$."),
]))

S.append(("Potencias de base 10", [
 (1, r"Escribe como número las potencias y como potencia los números:" + tasks(3, [r"$10^{3}$", r"$10^{6}$", r"$10^{8}$", r"$10\,000$", r"$100\,000$", r"$10$"]),
     tasks(3, [r"$1000$", r"$1\,000\,000$", r"$100\,000\,000$", r"$10^{4}$", r"$10^{5}$", r"$10^{1}$"])),
 (1, r"Escribe de forma abreviada con una potencia de 10:" + tasks(4, [r"$6\,000\,000$", r"$47\,000$", r"$350\,000\,000$", r"$2\,080\,000$"])
     + recorda(r"$10^{n}$ es un 1 seguido de $n$ ceros. Para abreviar, contamos los ceros \textbf{del final}: $\ 52\,000=52\cdot10^{3}$."),
     tasks(4, [r"$6\cdot10^{6}$", r"$47\cdot10^{3}$", r"$35\cdot10^{7}$", r"$208\cdot10^{4}$"])),
 (1, r"Escribe el número:" + tasks(4, [r"$9\cdot10^{5}$", r"$13\cdot10^{4}$", r"$207\cdot10^{3}$", r"$5\cdot10^{8}$"]),
     tasks(4, [r"$900\,000$", r"$130\,000$", r"$207\,000$", r"$500\,000\,000$"])),
 (2, r"Haz la descomposición polinómica de:" + tasks(4, [r"$6352$", r"$40\,718$", r"$805\,060$", r"$3\,000\,402$"]),
     tasks(2, [r"$6\cdot10^{3}+3\cdot10^{2}+5\cdot10+2$", r"$4\cdot10^{4}+7\cdot10^{2}+1\cdot10+8$", r"$8\cdot10^{5}+5\cdot10^{3}+6\cdot10$", r"$3\cdot10^{6}+4\cdot10^{2}+2$"])),
 (2, r"¿Qué número es?" + tasks(2, [r"$7\cdot10^{4}+2\cdot10^{3}+5\cdot10+9$", r"$3\cdot10^{5}+6\cdot10^{2}+1$", r"$4\cdot10^{6}+8\cdot10^{4}+3\cdot10^{3}$", r"$9\cdot10^{3}+9$"]),
     tasks(4, [r"$72\,059$", r"$300\,601$", r"$4\,083\,000$", r"$9009$"])),
 (3, r"Un número tiene 5 unidades de millón, 3 decenas de millar y 7 unidades. Escríbelo en forma polinómica y con cifras.",
     r"$5\cdot10^{6}+3\cdot10^{4}+7=\res{5\,030\,007}$."),
 (3, r"Un ordenador hace $1\,000\,000\,000$ operaciones por segundo. ¿Cuántas hace en $1000$ segundos? Escríbelo con potencias de 10.",
     r"$10^{9}\cdot10^{3}=10^{12}$: \ un 1 seguido de 12 ceros, $\res{1\,000\,000\,000\,000}$ operaciones."),
]))

S.append(("Propiedades de las potencias", [
 (1, r"Expresa como una única potencia:" + tasks(3, [r"$5^{4}\cdot5^{2}$", r"$7^{3}\cdot7^{2}$", r"$3^{7}\cdot3$", r"$2^{10}\cdot2^{13}$", r"$2^{3}\cdot2^{5}\cdot2^{2}$", r"$3^{2}\cdot3\cdot3^{4}$"])
     + recorda(r"$a^{m}\cdot a^{n}=a^{m+n}$ \qquad $a^{m}:a^{n}=a^{m-n}$ \qquad $(a^{m})^{n}=a^{m\cdot n}$ \qquad $a^{n}\cdot b^{n}=(a\cdot b)^{n}$ \qquad $a^{n}:b^{n}=(a:b)^{n}$ \qquad $a^{0}=1$. \ Si no hay exponente, es un 1."),
     tasks(6, [r"$5^{6}$", r"$7^{5}$", r"$3^{8}$", r"$2^{23}$", r"$2^{10}$", r"$3^{7}$"])),
 (1, r"Expresa como una única potencia:" + tasks(3, [r"$5^{8}:5^{2}$", r"$3^{6}:3$", r"$8^{5}:8^{2}$", r"$\dfrac{2^{9}}{2^{7}}$", r"$7^{10}:7^{4}:7^{3}$", r"$4^{7}:4^{7}$"]),
     tasks(6, [r"$5^{6}$", r"$3^{5}$", r"$8^{3}$", r"$2^{2}$", r"$7^{3}$", r"$4^{0}=1$"])),
 (1, r"Expresa como una única potencia:" + tasks(3, [r"$(7^{2})^{3}$", r"$(5^{4})^{3}$", r"$(2^{5})^{2}$", r"$(9^{3})^{0}$", r"$\left[(4^{2})^{3}\right]^{2}$", r"$(6^{1})^{5}$"]),
     tasks(6, [r"$7^{6}$", r"$5^{12}$", r"$2^{10}$", r"$9^{0}=1$", r"$4^{12}$", r"$6^{5}$"])),
 (1, r"Expresa como una única potencia (mismo exponente):" + tasks(3, [r"$5^{4}\cdot3^{4}$", r"$2^{3}\cdot7^{3}$", r"$8^{5}:2^{5}$", r"$21^{2}:7^{2}$", r"$2^{3}\cdot5^{3}\cdot7^{3}$", r"$36^{5}:2^{5}:3^{5}$"]),
     tasks(6, [r"$15^{4}$", r"$14^{3}$", r"$4^{5}$", r"$3^{2}$", r"$70^{3}$", r"$6^{5}$"])),
 (2, r"Expresa como una única potencia:" + tasks(3, [r"$(2^{5}\cdot2^{3}):2^{4}$", r"$(5^{2})^{3}\cdot5^{3}$", r"$6^{3}\cdot6^{8}:6^{6}$", r"$(3^{9})^{2}:(3^{2})^{5}$", r"$3^{5}\cdot(3^{10}:3^{8})$", r"$\dfrac{7^{10}\cdot7^{4}}{7^{6}}$", r"$9^{4}\cdot9^{3}\cdot(9^{2})^{7}$", r"$\dfrac{4^{20}:4^{14}}{4^{3}\cdot4^{2}}$", r"$(3^{8}\cdot3^{2})^{5}$"]),
     tasks(3, [r"$2^{8}:2^{4}=2^{4}$", r"$5^{6}\cdot5^{3}=5^{9}$", r"$6^{11}:6^{6}=6^{5}$", r"$3^{18}:3^{10}=3^{8}$", r"$3^{5}\cdot3^{2}=3^{7}$", r"$7^{14}:7^{6}=7^{8}$", r"$9^{4+3+14}=9^{21}$", r"$4^{6}:4^{5}=4$", r"$(3^{10})^{5}=3^{50}$"])),
 (2, r"Calcula de la manera más rápida:" + tasks(3, [r"$2^{5}\cdot5^{5}$", r"$25^{3}\cdot4^{3}$", r"$15^{4}:5^{4}$", r"$10^{7}:10^{4}$", r"$7^{9}:7^{7}$", r"$123^{0}$"]),
     tasks(3, [r"$10^{5}=100\,000$", r"$100^{3}=1\,000\,000$", r"$3^{4}=81$", r"$10^{3}=1000$", r"$7^{2}=49$", r"$1$"])),
 (3, r"Halla el valor de $x$ para que se cumplan las igualdades:" + tasks(5, [r"$3^{8}:3^{2}=3^{x}$", r"$x^{4}\cdot5^{4}=10^{4}$", r"$5^{x}\cdot5^{3}=5^{7}$", r"$(4^{x})^{3}=4^{6}$", r"$6^{2}\cdot7^{2}=x^{2}$", r"$2^{7}\cdot2=2^{x}$", r"$4^{4}\cdot x^{4}=8^{4}$", r"$(6^{3})^{x}=1$", r"$3^{9}:3^{x}=3^{4}$", r"$4^{0}=x$"]),
     tasks(5, [r"$x=6$", r"$x=2$", r"$x=4$", r"$x=2$", r"$x=42$", r"$x=8$", r"$x=2$", r"$x=0$", r"$x=5$", r"$x=1$"])),
 (3, r"Resuelve:" + tasks(1, [r"Expresa como una única potencia: $\left[(2^{3})^{4}\cdot2^{5}\right]:(2^{4})^{4}$", r"Expresa como una única potencia: $(12^{5}:4^{5})\cdot3^{2}$", r"Lucía dice que $2^{3}+2^{3}=2^{6}$. ¿Tiene razón? Explícalo calculando los dos lados."]),
     tasks(1, [r"$\left[2^{12}\cdot2^{5}\right]:2^{16}=2^{17}:2^{16}=\res{2}$", r"$3^{5}\cdot3^{2}=\res{3^{7}}$", r"No: $2^{3}+2^{3}=8+8=16=2^{4}$, pero $2^{6}=64$. Con las sumas no hay ninguna propiedad."])),
]))

S.append(("Raíces cuadradas", [
 (1, r"Calcula las raíces exactas:" + tasks(4, [r"$\sqrt{81}$", r"$\sqrt{64}$", r"$\sqrt{9}$", r"$\sqrt{100}$", r"$\sqrt{900}$", r"$\sqrt{169}$", r"$\sqrt{2500}$", r"$\sqrt{121}$"])
     + recorda(r"$\sqrt{144}=12$ porque $12^{2}=144$. \qquad Raíz entera: $\sqrt{27}$ tiene raíz entera 5 y resto 2, porque $27=5^{2}+2$ ($5^{2}=25$, pero $6^{2}=36$ ya se pasa)."),
     tasks(4, [r"$9$", r"$8$", r"$3$", r"$10$", r"$30$", r"$13$", r"$50$", r"$11$"])),
 (1, r"Calcula la raíz entera y el resto:" + tasks(4, [r"$\sqrt{18}$", r"$\sqrt{40}$", r"$\sqrt{117}$", r"$\sqrt{15}$", r"$\sqrt{75}$", r"$\sqrt{31}$", r"$\sqrt{200}$", r"$\sqrt{97}$"]),
     tasks(4, [r"$4$, resto $2$", r"$6$, resto $4$", r"$10$, resto $17$", r"$3$, resto $6$", r"$8$, resto $11$", r"$5$, resto $6$", r"$14$, resto $4$", r"$9$, resto $16$"])),
 (2, r"¿Entre qué dos números naturales consecutivos está cada raíz?" + tasks(4, [r"$\sqrt{50}$", r"$\sqrt{130}$", r"$\sqrt{300}$", r"$\sqrt{999}$"]),
     tasks(4, [r"$7$ y $8$", r"$11$ y $12$", r"$17$ y $18$", r"$31$ y $32$"]) + r"\par Por ejemplo: $31^{2}=961<999<1024=32^{2}$."),
 (2, r"Completa la tabla:\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{3.2cm}|C{3.2cm}|C{3.2cm}|}\hline\rowcolor{soft}\textbf{Radicando} & \textbf{Raíz entera} & \textbf{Resto}\\\hline & $8$ & $5$\\\hline & $12$ & $0$\\\hline & $15$ & $20$\\\hline $60$ & & \\\hline\end{tabular}\par}",
     r"\par\smallskip{\renewcommand{\arraystretch}{1.4}\centering\begin{tabular}{|C{3.2cm}|C{3.2cm}|C{3.2cm}|}\hline\rowcolor{soft}\textbf{Radicando} & \textbf{Raíz entera} & \textbf{Resto}\\\hline $69$ & $8$ & $5$\\\hline $144$ & $12$ & $0$\\\hline $245$ & $15$ & $20$\\\hline $60$ & $7$ & $11$\\\hline\end{tabular}\par}"),
 (3, r"Si la raíz entera de un número es 10, ¿cuál es el resto más grande que puede tener? ¿Cuántos números naturales tienen raíz entera 10?",
     r"Del $100$ al $120$ (el $121=11^{2}$ ya tiene raíz 11): resto máximo $120-100=\res{20}$ y hay $\res{21}$ números."),
 (3, r"Escribe todos los cuadrados perfectos que hay entre $200$ y $399$.",
     r"$15^{2}=225$, \ $16^{2}=256$, \ $17^{2}=289$, \ $18^{2}=324$, \ $19^{2}=361$."),
]))

S.append(("Operaciones y problemas con potencias y raíces", [
 (1, r"Calcula:" + tasks(2, [r"$3^{2}+4\cdot2-2^{3}$", r"$\sqrt{25}+6\cdot(2^{2}-1)-4^{2}$", r"$6+2^{4}-3\cdot2^{2}$", r"$(2^{2}+1)\cdot3+\sqrt{64}:4$", r"$2^{3}+12:\sqrt{16}-(2+1)^{2}$", r"$3\cdot\sqrt{36}+4\cdot(3^{2}+5)$"]),
     tasks(2, [r"$9+8-8=\res{9}$", r"$5+18-16=\res{7}$", r"$6+16-12=\res{10}$", r"$15+2=\res{17}$", r"$8+3-9=\res{2}$", r"$18+56=\res{74}$"])),
 (2, r"Calcula:" + tasks(2, [r"$5\cdot(\sqrt{16}-2)^{2}+(2^{3}-5)^{2}$", r"$(\sqrt{64}-\sqrt{25})^{3}+2\cdot(4^{2}-13)-\sqrt{16}\cdot(6^{2}-30)$", r"$3^{3}-2^{2}+\sqrt{81}\cdot(\sqrt{49}-3)^{2}$", r"$(\sqrt{81}-\sqrt{25})^{2}+2^{3}-\sqrt{9+7}$", r"$\left[(2-1)^{5}+2\right]\cdot\left[(3^{2})^{2}-2^{2}\right]$", r"$10^{2}:5^{2}+4\cdot\sqrt{25}-2^{0}$"]),
     tasks(2, [r"$5\cdot4+9=\res{29}$", r"$27+6-24=\res{9}$", r"$27-4+9\cdot16=\res{167}$", r"$16+8-4=\res{20}$", r"$3\cdot77=\res{231}$", r"$4+20-1=\res{23}$"])),
 (3, r"Calcula:" + tasks(1, [r"$3^{2}\cdot(15-\sqrt{25})^{2}-2^{3}\cdot(15-5)^{2}$", r"$\sqrt{4}\cdot(3^{2}-3)^{2}+2^{2}\cdot(5^{2}-5)^{2}$", r"$\left(1+2\cdot\sqrt{49}-3^{2}-5\right)\cdot\left(1+3\cdot\sqrt{36}-17\right)$", r"$\sqrt{6^{2}+8^{2}}-\sqrt{13^{2}-12^{2}}$"]),
     tasks(1, [r"$9\cdot100-8\cdot100=\res{100}$", r"$2\cdot36+4\cdot400=72+1600=\res{1672}$", r"$(1+14-9-5)\cdot(1+18-17)=1\cdot2=\res{2}$", r"$\sqrt{100}-\sqrt{25}=10-5=\res{5}$"])),
 (1, r"Una finca cuadrada mide 36 m de lado. ¿Cuántos metros cuadrados tiene? Si el metro cuadrado se paga a 50 €, ¿cuánto vale la finca?",
     r"$36^{2}=\res{1296\text{ m}^{2}}$; \ $1296\cdot50=\res{64\,800\text{ €}}$."),
 (1, r"Javier tiene 81 sellos y quiere colocarlos en una vitrina formando un cuadrado. ¿Cuántos sellos tiene que poner en cada lado?",
     r"$\sqrt{81}=\res{9\text{ sellos}}$ por lado."),
 (2, r"Un jardín cuadrado tiene $225$ m² de área. Queremos rodearlo con una valla que cuesta 6 € el metro. ¿Cuánto costará?",
     r"Lado: $\sqrt{225}=15$ m. \ Perímetro: $4\cdot15=60$ m. \ Coste: $60\cdot6=\res{360\text{ €}}$."),
 (2, r"Una sala tiene tantas filas como asientos tiene cada fila, y caben 324 personas. ¿Cuántas filas tiene?",
     r"$\sqrt{324}=\res{18\text{ filas}}$ (de 18 asientos)."),
 (2, r"Tenemos 150 baldosas cuadradas y queremos hacer el cuadrado más grande posible. ¿Cuántas baldosas ponemos en cada lado? ¿Cuántas sobran? ¿Cuántas faltarían para el cuadrado siguiente?",
     r"$12^{2}=144\le150<169=13^{2}$: \ $\res{12}$ por lado, sobran $\res{6}$ y faltarían $169-150=\res{19}$."),
 (3, r"Un cubo grande está formado por cubitos: hay 5 en cada arista. ¿Cuántos cubitos tiene? Pintamos de rojo todas las caras exteriores del cubo grande. ¿Cuántos cubitos no tendrán ninguna cara pintada?",
     r"Total: $5^{3}=\res{125}$. \ Sin pintar quedan los de dentro, un cubo de $3$ de arista: $3^{3}=\res{27}$."),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
pre = pre.replace('\\usepackage{icomma}\n', '\\usepackage{icomma}\n\\usepackage{cancel}\n')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 1: Números naturales' % t, capcalera='%s · Unidad 1: Números naturales' % t,
                 pdfkeywords='números naturales, aproximación, redondeo, truncamiento, operaciones combinadas, potencias, potencias de 10, raíces cuadradas',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 1' if sol else 'Ficha de ejercicios · Unidad 1') + '}{Números naturales}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Las tablas se pueden completar directamente en la ficha. Haz los cálculos sin calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            if sol:
                out.append('\\ex{%d} %s\n\n' % (st, s))
            else:
                out.append('\\ex{%d} %s\n\n' % (st, q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't1-fitxa-solucions-es.tex' if sol else 't1-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
