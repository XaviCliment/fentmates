# Genera t1-fitxa-exercicis.tex i t1-fitxa-solucions.tex (1r ESO, Unitat 1: Nombres naturals)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'

RECORDA = []  # (secció, text) quadres de recordatori, només a la fitxa d'exercicis
def recorda(t): return '\\recorda{%s}' % t

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
S.append(("Els nombres naturals", [
 (1, r"Escriu amb xifres:" + tasks(2, [r"Vint-i-tres mil quatre-cents set.", r"Cent cinc mil seixanta.", r"Dos milions tres-cents mil.", r"Set milions cinquanta mil nou."]),
     tasks(4, [r"$23\,407$", r"$105\,060$", r"$2\,300\,000$", r"$7\,050\,009$"])),
 (1, r"Escriu amb lletres:" + tasks(4, [r"$4090$", r"$15\,600$", r"$308\,012$", r"$2\,040\,500$"]),
     tasks(2, [r"Quatre mil noranta.", r"Quinze mil sis-cents.", r"Tres-cents huit mil dotze.", r"Dos milions quaranta mil cinc-cents."])),
 (1, r"Quin valor té la xifra 7 en cadascun d'aquests nombres?" + tasks(6, [r"$4718$", r"$73\,052$", r"$1207$", r"$7\,300\,000$", r"$25\,070$", r"$870\,412$"]),
     tasks(6, [r"$700$", r"$70\,000$", r"$7$", r"$7\,000\,000$", r"$70$", r"$70\,000$"])),
 (2, r"Ordena de menor a major: \[45\,099\qquad 45\,909\qquad 4599\qquad 45\,990\qquad 49\,059\]",
     r"$4599<45\,099<45\,909<45\,990<49\,059$ \ (el de quatre xifres és el més xicotet; la resta es comparen xifra a xifra d'esquerra a dreta)."),
 (2, r"Escriu el nombre anterior i el següent de:" + tasks(4, [r"$1000$", r"$39\,999$", r"$100\,000$", r"$2\,009\,999$"]),
     tasks(2, [r"$999$ \ i \ $1001$", r"$39\,998$ \ i \ $40\,000$", r"$99\,999$ \ i \ $100\,001$", r"$2\,009\,998$ \ i \ $2\,010\,000$"])),
 (2, r"Respon:" + tasks(1, [r"Quantes desenes té en total el nombre $3450$?", r"Quantes centenes té en total el nombre $72\,000$?", r"Quantes unitats de miler té un milió?"]),
     tasks(3, [r"$\res{345}$ desenes", r"$\res{720}$ centenes", r"$\res{1000}$ milers"])),
 (3, r"Amb les xifres 4, 0, 9, 2 i 6, sense repetir-ne cap, escriu:" + tasks(1, [r"El nombre de cinc xifres més gran possible.", r"El nombre de cinc xifres més xicotet possible (recorda que no pot començar per 0).", r"El nombre de cinc xifres més gran que siga senar."]),
     tasks(1, [r"$\res{96\,420}$ (xifres de major a menor).", r"$\res{20\,469}$ (comencem per la xifra més xicoteta que no és 0).", r"Ha d'acabar en 9, l'única xifra senar: $\res{64\,209}$."])),
 (3, r"Quants nombres de tres xifres comencen per 5? I quants nombres de quatre xifres hi ha en total?",
     r"Del $500$ al $599$: $\res{100}$ nombres. \ Del $1000$ al $9999$: $9999-999=\res{9000}$ nombres."),
]))

S.append(("Aproximació: truncament i arrodoniment", [
 (1, r"Trunca els nombres següents a les desenes i a les centenes:" + tasks(3, [r"$1257$", r"$32\,041$", r"$57\,623$", r"$12\,354$", r"$3462$", r"$23\,465\,244$"]),
     tasks(3, [r"$1250$ \ i \ $1200$", r"$32\,040$ \ i \ $32\,000$", r"$57\,620$ \ i \ $57\,600$", r"$12\,350$ \ i \ $12\,300$", r"$3460$ \ i \ $3400$", r"$23\,465\,240$ \ i \ $23\,465\,200$"])),
 (1, r"Arrodoneix els nombres de l'exercici anterior a les desenes i a les centenes. En quins casos l'arrodoniment i el truncament no coincideixen? Quin dels dos s'acosta més al nombre de partida?",
     tasks(3, [r"$1260$ \ i \ $1300$", r"$32\,040$ \ i \ $32\,000$", r"$57\,620$ \ i \ $57\,600$", r"$12\,350$ \ i \ $12\,400$", r"$3460$ \ i \ $3500$", r"$23\,465\,240$ \ i \ $23\,465\,200$"])
     + r"\par No coincideixen en a) (desenes i centenes), d) (centenes) i e) (centenes). L'\textbf{arrodoniment} sempre dona el nombre més pròxim."),
 (2, r"Completa la taula aproximant a les unitats de miler:\par\smallskip{\renewcommand{\arraystretch}{1.6}\centering\begin{tabular}{|C{3.6cm}|C{3.6cm}|C{3.6cm}|}\hline\rowcolor{soft}\textbf{Nombre} & \textbf{Truncament} & \textbf{Arrodoniment}\\\hline $45\,678$ & & \\\hline $129\,350$ & & \\\hline $9499$ & & \\\hline $70\,501$ & & \\\hline $999\,600$ & & \\\hline\end{tabular}\par}",
     r"\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{3.6cm}|C{3.6cm}|C{3.6cm}|}\hline\rowcolor{soft}\textbf{Nombre} & \textbf{Truncament} & \textbf{Arrodoniment}\\\hline $45\,678$ & $45\,000$ & $46\,000$\\\hline $129\,350$ & $129\,000$ & $129\,000$\\\hline $9499$ & $9000$ & $9000$\\\hline $70\,501$ & $70\,000$ & $71\,000$\\\hline $999\,600$ & $999\,000$ & $1\,000\,000$\\\hline\end{tabular}\par}"),
 (2, r"Arrodoneix (compte amb els nous!):" + tasks(2, [r"$3995$ a les desenes.", r"$59\,960$ a les centenes.", r"$199\,500$ a les unitats de miler.", r"$2\,970\,000$ a les centenes de miler."]),
     tasks(4, [r"$4000$", r"$60\,000$", r"$200\,000$", r"$3\,000\,000$"])),
 (2, r"Una televisió costa $1349$ €. Arrodoneix el preu a les desenes i a les centenes i calcula l'error que es comet en cada cas.",
     r"Desenes: $\res{1350\text{ €}}$, error $1350-1349=1$ €. \ Centenes: $\res{1300\text{ €}}$, error $1349-1300=49$ €."),
 (3, r"En arrodonir un nombre a les centenes s'ha obtingut $8300$. Quin és el nombre més xicotet que podia ser? I el més gran?",
     r"Del $\res{8250}$ (puja) fins al $\res{8349}$ (es queda igual)."),
 (3, r"A un partit van $48\,652$ espectadors. Un diari titula «Quasi $49\,000$ espectadors» i un altre, «Més de $48\,000$ espectadors». Quin diari ha arrodonit i quin ha truncat? Quin s'equivoca menys?",
     r"El primer ha \textbf{arrodonit} (error $348$) i el segon ha \textbf{truncat} (error $652$). S'equivoca menys el primer."),
]))

S.append(("Operacions amb nombres naturals", [
 (1, r"Calcula:" + tasks(2, [r"$3458+976+12\,045$", r"$20\,000-7386$", r"$507\cdot36$", r"$2300\cdot400$"]),
     tasks(4, [r"$16\,479$", r"$12\,614$", r"$18\,252$", r"$920\,000$"])),
 (1, r"Fes aquestes divisions i comprova-les amb la prova $D=d\cdot q+r$:" + tasks(4, [r"$8745:15$", r"$9236:24$", r"$52\,000:125$", r"$7000:63$"]),
     tasks(2, [r"$q=583,\ r=0$ \ (exacta)", r"$q=384,\ r=20$: \ $24\cdot384+20=9236$", r"$q=416,\ r=0$ \ (exacta)", r"$q=111,\ r=7$: \ $63\cdot111+7=7000$"])),
 (2, r"Completa la taula de divisions:\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{2.6cm}|C{2.6cm}|C{2.6cm}|C{2.6cm}|}\hline\rowcolor{soft}\textbf{Dividend} & \textbf{Divisor} & \textbf{Quocient} & \textbf{Residu}\\\hline & $12$ & $35$ & $7$\\\hline $500$ & & $41$ & $8$\\\hline $1000$ & $27$ & & \\\hline & $25$ & $18$ & $24$\\\hline\end{tabular}\par}",
     r"\par\smallskip{\renewcommand{\arraystretch}{1.4}\centering\begin{tabular}{|C{2.6cm}|C{2.6cm}|C{2.6cm}|C{2.6cm}|}\hline\rowcolor{soft}\textbf{Dividend} & \textbf{Divisor} & \textbf{Quocient} & \textbf{Residu}\\\hline $427$ & $12$ & $35$ & $7$\\\hline $500$ & $12$ & $41$ & $8$\\\hline $1000$ & $27$ & $37$ & $1$\\\hline $474$ & $25$ & $18$ & $24$\\\hline\end{tabular}\par}"
     r"\smallskip Per al divisor: $(500-8):41=492:41=12$."),
 (2, r"Calcula de cap aplicant les propietats de les operacions:" + tasks(3, [r"$25\cdot17\cdot4$", r"$38+57+62+43$", r"$13\cdot99$", r"$8\cdot125$", r"$36\cdot7+36\cdot3$", r"$45\cdot102$"]),
     tasks(3, [r"$(25\cdot4)\cdot17=\res{1700}$", r"$100+100=\res{200}$", r"$13\cdot100-13=\res{1287}$", r"$\res{1000}$", r"$36\cdot(7+3)=\res{360}$", r"$45\cdot100+45\cdot2=\res{4590}$"])),
 (1, r"Calcula, respectant la jerarquia de les operacions:" + tasks(2, [r"$40:8+15-4\cdot3$", r"$4\cdot7-18:3-2\cdot5$", r"$36:(5+4)+7$", r"$9\cdot3-4\cdot(11-6)$", r"$30-4\cdot(3+2)+5$", r"$(16+8):3-2\cdot4$", r"$3\cdot(5+4)-2\cdot(7-3)$", r"$50-6\cdot(12-3\cdot2)$"])
     + recorda(r"Ordre de les operacions: \textbf{1)} parèntesis i claudàtors (de dins cap a fora); \textbf{2)} potències i arrels; \textbf{3)} multiplicacions i divisions, d'esquerra a dreta; \textbf{4)} sumes i restes, d'esquerra a dreta."),
     tasks(4, [r"$5+15-12=\res{8}$", r"$28-6-10=\res{12}$", r"$4+7=\res{11}$", r"$27-20=\res{7}$", r"$30-20+5=\res{15}$", r"$8-8=\res{0}$", r"$27-8=\res{19}$", r"$50-36=\res{14}$"])),
 (2, r"Calcula:" + tasks(1, [r"$4\cdot6+3\cdot(8-5)-(12-7)\cdot3$", r"$9\cdot5-3\cdot(4+6)-48:8\cdot2$", r"$2\cdot(6+3\cdot4-8)+5\cdot4:2-(3+6)\cdot2$", r"$5\cdot[2+3\cdot(4+1)-7]+42:6$", r"$[(9+6):5+2\cdot4]\cdot2-96:12$", r"$25-4\cdot(9-2\cdot3)-[(2+3)\cdot4-6\cdot3]$"]),
     tasks(1, [r"$24+9-15=\res{18}$", r"$45-30-6\cdot2=45-30-12=\res{3}$", r"$2\cdot10+10-18=\res{12}$", r"$5\cdot[2+15-7]+7=5\cdot10+7=\res{57}$", r"$[3+8]\cdot2-8=22-8=\res{14}$", r"$25-12-[20-18]=13-2=\res{11}$"])),
 (3, r"Calcula:" + tasks(1, [r"$[50-(4+2)\cdot7]\cdot3-2\cdot[(9-5)\cdot3-4]$", r"$100-3\cdot[20-2\cdot(15-4\cdot3)]:7$"]),
     tasks(1, [r"$[50-42]\cdot3-2\cdot[12-4]=24-16=\res{8}$", r"$100-3\cdot[20-2\cdot3]:7=100-3\cdot14:7=100-42:7=100-6=\res{94}$"])),
 (3, r"Posa parèntesis on calga perquè cada igualtat siga certa:" + tasks(3, [r"$6+4\cdot5-3=47$", r"$6+4\cdot5-3=14$", r"$6+4\cdot5-3=20$"]),
     tasks(3, [r"$(6+4)\cdot5-3=47$", r"$6+4\cdot(5-3)=14$", r"$(6+4)\cdot(5-3)=20$"])),
]))

S.append(("Problemes amb nombres naturals", [
 (1, r"En un col·legi s'han comprat 36 balons per $612$ €. Quant ha costat cada baló?",
     r"$612:36=\res{17\text{ €}}$ cada baló."),
 (1, r"Un pastisser fa cada dia 13 dotzenes de pastissos de crema. Quants n'haurà fet en el mes de gener si ha tingut 6 dies de festa?",
     r"Treballa $31-6=25$ dies i fa $13\cdot12=156$ pastissos al dia: \ $156\cdot25=\res{3900\text{ pastissos}}$."),
 (1, r"Per a repoblar un riu s'hi aboquen 45 caixes amb 758 alevins cadascuna. De cada caixa se'n moren 27. Quants alevins sobreviuen?",
     r"De cada caixa en sobreviuen $758-27=731$: \ $731\cdot45=\res{32\,895\text{ alevins}}$."),
 (2, r"Un agricultor té dos camps. En el primer replega 34 caixes de pomes i en el segon, 12. Totes les caixes pesen 15 kg. Quant cobrarà si li paguen les pomes a 2 € el quilo?",
     r"$(34+12)\cdot15=46\cdot15=690$ kg; \ $690\cdot2=\res{1380\text{ €}}$."),
 (2, r"En una obra treballen 43 obrers, 7 hores cada dia. L'obra dura 147 dies i cada obrer cobra 15 € per hora. Quant han cobrat entre tots?",
     r"$43\cdot7\cdot147\cdot15=301\cdot147\cdot15=44\,247\cdot15=\res{663\,705\text{ €}}$."),
 (2, r"Els quatre grups de 1r d'ESO (de 28, 27, 29 i 26 alumnes) van d'excursió amb 8 professors. Els autobusos tenen 55 places. Quants autobusos calen? Si cada autobús costa $330$ € i el preu el paguen només els alumnes a parts iguals, quant paga cada alumne?",
     r"Alumnes: $28+27+29+26=110$; persones: $118$. \ $118:55\to q=2,\ r=8$: calen \res{3\text{ autobusos}}.\\ $3\cdot330=990$ €; \ $990:110=\res{9\text{ €}}$ per alumne."),
 (2, r"Un camió transporta $23\,400$ botelles. En un accident se'n trenca la tercera part. Quantes caixes de 12 botelles calen per a guardar les que no s'han trencat?",
     r"Trencades: $23\,400:3=7800$. \ Senceres: $23\,400-7800=15\,600$. \ $15\,600:12=\res{1300\text{ caixes}}$."),
 (2, r"Un vaixell ha cobrat $9100$ € per $1300$ kg de lluç. Quant cobrarà un altre vaixell per $1750$ kg de lluç de la mateixa qualitat?",
     r"Preu d'un quilo: $9100:1300=7$ €. \ $1750\cdot7=\res{12\,250\text{ €}}$."),
 (3, r"En una papereria hi ha l'oferta «Paga'n 4 i emporta-te'n 5». He tornat a casa amb 20 retoladors i he pagat $64$ €. Quant costa cada retolador?",
     r"De cada 5 en pague 4: dels 20 n'he pagat $20:5\cdot4=16$. \ $64:16=\res{4\text{ €}}$ cada retolador."),
 (3, r"Un cinema té 24 files de 18 seients. En una sessió s'han venut 350 entrades a 7 €. Quants seients han quedat buits? Quant s'ha recaptat? Quants diners més s'haurien recaptat si s'hagueren venut totes les entrades?",
     r"Seients: $24\cdot18=432$; buits: $432-350=\res{82}$. \ Recaptat: $350\cdot7=\res{2450\text{ €}}$.\\ Ple: $432\cdot7=3024$ €; \ $3024-2450=\res{574\text{ €}}$ més."),
 (3, r"Una família compra un sofà de $1380$ €. Paga $300$ € en el moment de la compra i la resta en quotes mensuals de $90$ €. Quantes quotes haurà de pagar?",
     r"Falten $1380-300=1080$ €. \ $1080:90=\res{12\text{ quotes}}$ (un any)."),
]))

S.append(("Potències", [
 (1, r"Escriu cada potència com un producte i calcula'n el valor:" + tasks(5, [r"$3^{2}$", r"$5^{3}$", r"$7^{1}$", r"$2^{5}$", r"$9^{2}$", r"$6^{3}$", r"$0^{5}$", r"$1^{7}$", r"$4^{4}$", r"$11^{2}$"])
     + recorda(r"$a^{n}=\underbrace{a\cdot a\cdots a}_{n\text{ vegades}}$ \qquad $a^{1}=a$ \qquad $1^{n}=1$ \qquad $0^{n}=0$. \quad Compte: $2^{3}=2\cdot2\cdot2=8$, no $2\cdot3$!"),
     tasks(2, [r"$3\cdot3=9$", r"$5\cdot5\cdot5=125$", r"$7$", r"$2\cdot2\cdot2\cdot2\cdot2=32$", r"$9\cdot9=81$", r"$6\cdot6\cdot6=216$", r"$0\cdot0\cdot0\cdot0\cdot0=0$", r"$1\cdot1\cdot1\cdot1\cdot1\cdot1\cdot1=1$", r"$4\cdot4\cdot4\cdot4=256$", r"$11\cdot11=121$"])),
 (1, r"Escriu en forma de potència i explica com es llig:" + tasks(4, [r"$7\cdot7\cdot7\cdot7$", r"$12\cdot12$", r"$2\cdot2\cdot2\cdot2\cdot2\cdot2$", r"$8\cdot8\cdot8$"]),
     tasks(2, [r"$7^{4}$: set elevat a quatre", r"$12^{2}$: dotze al quadrat", r"$2^{6}$: dos elevat a sis", r"$8^{3}$: huit al cub"])),
 (2, r"Escriu aquests nombres en forma de potència (de totes les maneres que sàpies):" + tasks(6, [r"$49$", r"$125$", r"$32$", r"$1000$", r"$81$", r"$64$"]),
     tasks(3, [r"$7^{2}$", r"$5^{3}$", r"$2^{5}$", r"$10^{3}$", r"$9^{2}=3^{4}$", r"$8^{2}=4^{3}=2^{6}$"])),
 (2, r"Escriu el signe $<$, $>$ o $=$:" + tasks(4, [r"$2^{5}\ \square\ 5^{2}$", r"$3^{4}\ \square\ 4^{3}$", r"$2^{4}\ \square\ 4^{2}$", r"$10^{2}\ \square\ 2^{10}$"]),
     tasks(4, [r"$32>25$", r"$81>64$", r"$16=16$", r"$100<1024$"])),
 (2, r"Completa la taula:\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|}\hline\rowcolor{soft}$n$ & $4$ & $7$ & $11$ & $13$ & $20$\\\hline $n^{2}$ & & & & & \\\hline $n^{3}$ & & & & & \\\hline\end{tabular}\par}",
     r"\par\smallskip{\renewcommand{\arraystretch}{1.4}\centering\begin{tabular}{|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|C{1.6cm}|}\hline\rowcolor{soft}$n$ & $4$ & $7$ & $11$ & $13$ & $20$\\\hline $n^{2}$ & $16$ & $49$ & $121$ & $169$ & $400$\\\hline $n^{3}$ & $64$ & $343$ & $1331$ & $2197$ & $8000$\\\hline\end{tabular}\par}"),
 (3, r"En una sala d'un museu hi ha 3 parets amb 3 quadres en cadascuna; en cada quadre apareixen 3 persones i cada persona porta 3 flors. Quantes flors hi ha en total? I si Pere té 6 butxaques amb 6 clauers en cadascuna i 6 claus en cada clauer, quantes claus té? Expressa els resultats com a potències i calcula-les.",
     r"Flors: $3\cdot3\cdot3\cdot3=3^{4}=\res{81}$. \ Claus: $6\cdot6\cdot6=6^{3}=\res{216}$."),
 (3, r"Un bacteri es divideix en dos cada hora. Si comencem amb un bacteri, quants n'hi haurà al cap d'1 hora? I de 2 hores? Expressa com a potència quants n'hi haurà al cap de 10 hores i calcula-ho.",
     r"1 hora: $2$; \ 2 hores: $2^{2}=4$; \ 10 hores: $2^{10}=\res{1024\text{ bacteris}}$."),
]))

S.append(("Potències de base 10", [
 (1, r"Escriu com a nombre les potències i com a potència els nombres:" + tasks(3, [r"$10^{3}$", r"$10^{6}$", r"$10^{8}$", r"$10\,000$", r"$100\,000$", r"$10$"]),
     tasks(3, [r"$1000$", r"$1\,000\,000$", r"$100\,000\,000$", r"$10^{4}$", r"$10^{5}$", r"$10^{1}$"])),
 (1, r"Escriu de forma abreujada amb una potència de 10:" + tasks(4, [r"$6\,000\,000$", r"$47\,000$", r"$350\,000\,000$", r"$2\,080\,000$"])
     + recorda(r"$10^{n}$ és un 1 seguit de $n$ zeros. Per a abreujar, comptem els zeros \textbf{del final}: $\ 52\,000=52\cdot10^{3}$."),
     tasks(4, [r"$6\cdot10^{6}$", r"$47\cdot10^{3}$", r"$35\cdot10^{7}$", r"$208\cdot10^{4}$"])),
 (1, r"Escriu el nombre:" + tasks(4, [r"$9\cdot10^{5}$", r"$13\cdot10^{4}$", r"$207\cdot10^{3}$", r"$5\cdot10^{8}$"]),
     tasks(4, [r"$900\,000$", r"$130\,000$", r"$207\,000$", r"$500\,000\,000$"])),
 (2, r"Fes la descomposició polinòmica de:" + tasks(4, [r"$6352$", r"$40\,718$", r"$805\,060$", r"$3\,000\,402$"]),
     tasks(2, [r"$6\cdot10^{3}+3\cdot10^{2}+5\cdot10+2$", r"$4\cdot10^{4}+7\cdot10^{2}+1\cdot10+8$", r"$8\cdot10^{5}+5\cdot10^{3}+6\cdot10$", r"$3\cdot10^{6}+4\cdot10^{2}+2$"])),
 (2, r"Quin nombre és?" + tasks(2, [r"$7\cdot10^{4}+2\cdot10^{3}+5\cdot10+9$", r"$3\cdot10^{5}+6\cdot10^{2}+1$", r"$4\cdot10^{6}+8\cdot10^{4}+3\cdot10^{3}$", r"$9\cdot10^{3}+9$"]),
     tasks(4, [r"$72\,059$", r"$300\,601$", r"$4\,083\,000$", r"$9009$"])),
 (3, r"Un nombre té 5 unitats de milió, 3 desenes de miler i 7 unitats. Escriu-lo en forma polinòmica i amb xifres.",
     r"$5\cdot10^{6}+3\cdot10^{4}+7=\res{5\,030\,007}$."),
 (3, r"Un ordinador fa $1\,000\,000\,000$ operacions per segon. Quantes en fa en $1000$ segons? Escriu-ho amb potències de 10.",
     r"$10^{9}\cdot10^{3}=10^{12}$: \ un 1 seguit de 12 zeros, $\res{1\,000\,000\,000\,000}$ operacions."),
]))

S.append(("Propietats de les potències", [
 (1, r"Expressa com una única potència:" + tasks(3, [r"$5^{4}\cdot5^{2}$", r"$7^{3}\cdot7^{2}$", r"$3^{7}\cdot3$", r"$2^{10}\cdot2^{13}$", r"$2^{3}\cdot2^{5}\cdot2^{2}$", r"$3^{2}\cdot3\cdot3^{4}$"])
     + recorda(r"$a^{m}\cdot a^{n}=a^{m+n}$ \qquad $a^{m}:a^{n}=a^{m-n}$ \qquad $(a^{m})^{n}=a^{m\cdot n}$ \qquad $a^{n}\cdot b^{n}=(a\cdot b)^{n}$ \qquad $a^{n}:b^{n}=(a:b)^{n}$ \qquad $a^{0}=1$. \ Si no hi ha exponent, és un 1."),
     tasks(6, [r"$5^{6}$", r"$7^{5}$", r"$3^{8}$", r"$2^{23}$", r"$2^{10}$", r"$3^{7}$"])),
 (1, r"Expressa com una única potència:" + tasks(3, [r"$5^{8}:5^{2}$", r"$3^{6}:3$", r"$8^{5}:8^{2}$", r"$\dfrac{2^{9}}{2^{7}}$", r"$7^{10}:7^{4}:7^{3}$", r"$4^{7}:4^{7}$"]),
     tasks(6, [r"$5^{6}$", r"$3^{5}$", r"$8^{3}$", r"$2^{2}$", r"$7^{3}$", r"$4^{0}=1$"])),
 (1, r"Expressa com una única potència:" + tasks(3, [r"$(7^{2})^{3}$", r"$(5^{4})^{3}$", r"$(2^{5})^{2}$", r"$(9^{3})^{0}$", r"$\left[(4^{2})^{3}\right]^{2}$", r"$(6^{1})^{5}$"]),
     tasks(6, [r"$7^{6}$", r"$5^{12}$", r"$2^{10}$", r"$9^{0}=1$", r"$4^{12}$", r"$6^{5}$"])),
 (1, r"Expressa com una única potència (mateix exponent):" + tasks(3, [r"$5^{4}\cdot3^{4}$", r"$2^{3}\cdot7^{3}$", r"$8^{5}:2^{5}$", r"$21^{2}:7^{2}$", r"$2^{3}\cdot5^{3}\cdot7^{3}$", r"$36^{5}:2^{5}:3^{5}$"]),
     tasks(6, [r"$15^{4}$", r"$14^{3}$", r"$4^{5}$", r"$3^{2}$", r"$70^{3}$", r"$6^{5}$"])),
 (2, r"Expressa com una única potència:" + tasks(3, [r"$(2^{5}\cdot2^{3}):2^{4}$", r"$(5^{2})^{3}\cdot5^{3}$", r"$6^{3}\cdot6^{8}:6^{6}$", r"$(3^{9})^{2}:(3^{2})^{5}$", r"$3^{5}\cdot(3^{10}:3^{8})$", r"$\dfrac{7^{10}\cdot7^{4}}{7^{6}}$", r"$9^{4}\cdot9^{3}\cdot(9^{2})^{7}$", r"$\dfrac{4^{20}:4^{14}}{4^{3}\cdot4^{2}}$", r"$(3^{8}\cdot3^{2})^{5}$"]),
     tasks(3, [r"$2^{8}:2^{4}=2^{4}$", r"$5^{6}\cdot5^{3}=5^{9}$", r"$6^{11}:6^{6}=6^{5}$", r"$3^{18}:3^{10}=3^{8}$", r"$3^{5}\cdot3^{2}=3^{7}$", r"$7^{14}:7^{6}=7^{8}$", r"$9^{4+3+14}=9^{21}$", r"$4^{6}:4^{5}=4$", r"$(3^{10})^{5}=3^{50}$"])),
 (2, r"Calcula de la manera més ràpida:" + tasks(3, [r"$2^{5}\cdot5^{5}$", r"$25^{3}\cdot4^{3}$", r"$15^{4}:5^{4}$", r"$10^{7}:10^{4}$", r"$7^{9}:7^{7}$", r"$123^{0}$"]),
     tasks(3, [r"$10^{5}=100\,000$", r"$100^{3}=1\,000\,000$", r"$3^{4}=81$", r"$10^{3}=1000$", r"$7^{2}=49$", r"$1$"])),
 (3, r"Troba el valor de $x$ perquè es complisquen les igualtats:" + tasks(5, [r"$3^{8}:3^{2}=3^{x}$", r"$x^{4}\cdot5^{4}=10^{4}$", r"$5^{x}\cdot5^{3}=5^{7}$", r"$(4^{x})^{3}=4^{6}$", r"$6^{2}\cdot7^{2}=x^{2}$", r"$2^{7}\cdot2=2^{x}$", r"$4^{4}\cdot x^{4}=8^{4}$", r"$(6^{3})^{x}=1$", r"$3^{9}:3^{x}=3^{4}$", r"$4^{0}=x$"]),
     tasks(5, [r"$x=6$", r"$x=2$", r"$x=4$", r"$x=2$", r"$x=42$", r"$x=8$", r"$x=2$", r"$x=0$", r"$x=5$", r"$x=1$"])),
 (3, r"Resol:" + tasks(1, [r"Expressa com una única potència: $\left[(2^{3})^{4}\cdot2^{5}\right]:(2^{4})^{4}$", r"Expressa com una única potència: $(12^{5}:4^{5})\cdot3^{2}$", r"La Laia diu que $2^{3}+2^{3}=2^{6}$. Té raó? Explica-ho calculant els dos costats."]),
     tasks(1, [r"$\left[2^{12}\cdot2^{5}\right]:2^{16}=2^{17}:2^{16}=\res{2}$", r"$3^{5}\cdot3^{2}=\res{3^{7}}$", r"No: $2^{3}+2^{3}=8+8=16=2^{4}$, però $2^{6}=64$. Amb les sumes no hi ha cap propietat."])),
]))

S.append(("Arrels quadrades", [
 (1, r"Calcula les arrels exactes:" + tasks(4, [r"$\sqrt{81}$", r"$\sqrt{64}$", r"$\sqrt{9}$", r"$\sqrt{100}$", r"$\sqrt{900}$", r"$\sqrt{169}$", r"$\sqrt{2500}$", r"$\sqrt{121}$"])
     + recorda(r"$\sqrt{144}=12$ perquè $12^{2}=144$. \qquad Arrel entera: $\sqrt{27}$ té arrel entera 5 i residu 2, perquè $27=5^{2}+2$ ($5^{2}=25$, però $6^{2}=36$ ja es passa)."),
     tasks(4, [r"$9$", r"$8$", r"$3$", r"$10$", r"$30$", r"$13$", r"$50$", r"$11$"])),
 (1, r"Calcula l'arrel entera i el residu:" + tasks(4, [r"$\sqrt{18}$", r"$\sqrt{40}$", r"$\sqrt{117}$", r"$\sqrt{15}$", r"$\sqrt{75}$", r"$\sqrt{31}$", r"$\sqrt{200}$", r"$\sqrt{97}$"]),
     tasks(4, [r"$4$, residu $2$", r"$6$, residu $4$", r"$10$, residu $17$", r"$3$, residu $6$", r"$8$, residu $11$", r"$5$, residu $6$", r"$14$, residu $4$", r"$9$, residu $16$"])),
 (2, r"Entre quins dos nombres naturals consecutius està cada arrel?" + tasks(4, [r"$\sqrt{50}$", r"$\sqrt{130}$", r"$\sqrt{300}$", r"$\sqrt{999}$"]),
     tasks(4, [r"$7$ i $8$", r"$11$ i $12$", r"$17$ i $18$", r"$31$ i $32$"]) + r"\par Per exemple: $31^{2}=961<999<1024=32^{2}$."),
 (2, r"Completa la taula:\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{3.2cm}|C{3.2cm}|C{3.2cm}|}\hline\rowcolor{soft}\textbf{Radicand} & \textbf{Arrel entera} & \textbf{Residu}\\\hline & $8$ & $5$\\\hline & $12$ & $0$\\\hline & $15$ & $20$\\\hline $60$ & & \\\hline\end{tabular}\par}",
     r"\par\smallskip{\renewcommand{\arraystretch}{1.4}\centering\begin{tabular}{|C{3.2cm}|C{3.2cm}|C{3.2cm}|}\hline\rowcolor{soft}\textbf{Radicand} & \textbf{Arrel entera} & \textbf{Residu}\\\hline $69$ & $8$ & $5$\\\hline $144$ & $12$ & $0$\\\hline $245$ & $15$ & $20$\\\hline $60$ & $7$ & $11$\\\hline\end{tabular}\par}"),
 (3, r"Si l'arrel entera d'un nombre és 10, quin és el residu més gran que pot tindre? Quants nombres naturals tenen arrel entera 10?",
     r"Del $100$ al $120$ (el $121=11^{2}$ ja té arrel 11): residu màxim $120-100=\res{20}$ i hi ha $\res{21}$ nombres."),
 (3, r"Escriu tots els quadrats perfectes que hi ha entre $200$ i $399$.",
     r"$15^{2}=225$, \ $16^{2}=256$, \ $17^{2}=289$, \ $18^{2}=324$, \ $19^{2}=361$."),
]))

S.append(("Operacions i problemes amb potències i arrels", [
 (1, r"Calcula:" + tasks(2, [r"$3^{2}+4\cdot2-2^{3}$", r"$\sqrt{25}+6\cdot(2^{2}-1)-4^{2}$", r"$6+2^{4}-3\cdot2^{2}$", r"$(2^{2}+1)\cdot3+\sqrt{64}:4$", r"$2^{3}+12:\sqrt{16}-(2+1)^{2}$", r"$3\cdot\sqrt{36}+4\cdot(3^{2}+5)$"]),
     tasks(2, [r"$9+8-8=\res{9}$", r"$5+18-16=\res{7}$", r"$6+16-12=\res{10}$", r"$15+2=\res{17}$", r"$8+3-9=\res{2}$", r"$18+56=\res{74}$"])),
 (2, r"Calcula:" + tasks(2, [r"$5\cdot(\sqrt{16}-2)^{2}+(2^{3}-5)^{2}$", r"$(\sqrt{64}-\sqrt{25})^{3}+2\cdot(4^{2}-13)-\sqrt{16}\cdot(6^{2}-30)$", r"$3^{3}-2^{2}+\sqrt{81}\cdot(\sqrt{49}-3)^{2}$", r"$(\sqrt{81}-\sqrt{25})^{2}+2^{3}-\sqrt{9+7}$", r"$\left[(2-1)^{5}+2\right]\cdot\left[(3^{2})^{2}-2^{2}\right]$", r"$10^{2}:5^{2}+4\cdot\sqrt{25}-2^{0}$"]),
     tasks(2, [r"$5\cdot4+9=\res{29}$", r"$27+6-24=\res{9}$", r"$27-4+9\cdot16=\res{167}$", r"$16+8-4=\res{20}$", r"$3\cdot77=\res{231}$", r"$4+20-1=\res{23}$"])),
 (3, r"Calcula:" + tasks(1, [r"$3^{2}\cdot(15-\sqrt{25})^{2}-2^{3}\cdot(15-5)^{2}$", r"$\sqrt{4}\cdot(3^{2}-3)^{2}+2^{2}\cdot(5^{2}-5)^{2}$", r"$\left(1+2\cdot\sqrt{49}-3^{2}-5\right)\cdot\left(1+3\cdot\sqrt{36}-17\right)$", r"$\sqrt{6^{2}+8^{2}}-\sqrt{13^{2}-12^{2}}$"]),
     tasks(1, [r"$9\cdot100-8\cdot100=\res{100}$", r"$2\cdot36+4\cdot400=72+1600=\res{1672}$", r"$(1+14-9-5)\cdot(1+18-17)=1\cdot2=\res{2}$", r"$\sqrt{100}-\sqrt{25}=10-5=\res{5}$"])),
 (1, r"Una finca quadrada fa 36 m de costat. Quants metres quadrats té? Si el metre quadrat es paga a 50 €, quant val la finca?",
     r"$36^{2}=\res{1296\text{ m}^{2}}$; \ $1296\cdot50=\res{64\,800\text{ €}}$."),
 (1, r"En Xavier té 81 segells i vol col·locar-los en una vitrina formant un quadrat. Quants segells ha de posar a cada costat?",
     r"$\sqrt{81}=\res{9\text{ segells}}$ per costat."),
 (2, r"Un jardí quadrat té $225$ m² d'àrea. Volem envoltar-lo amb una tanca que costa 6 € el metre. Quant costarà?",
     r"Costat: $\sqrt{225}=15$ m. \ Perímetre: $4\cdot15=60$ m. \ Cost: $60\cdot6=\res{360\text{ €}}$."),
 (2, r"Una sala té tantes files com seients té cada fila, i hi caben 324 persones. Quantes files té?",
     r"$\sqrt{324}=\res{18\text{ files}}$ (de 18 seients)."),
 (2, r"Tenim 150 rajoles quadrades i volem fer el quadrat més gran possible. Quantes rajoles posem a cada costat? Quantes en sobren? Quantes en faltarien per al quadrat següent?",
     r"$12^{2}=144\le150<169=13^{2}$: \ $\res{12}$ per costat, en sobren $\res{6}$ i en faltarien $169-150=\res{19}$."),
 (3, r"Un cub gran està format per cubets: n'hi ha 5 en cada aresta. Quants cubets té? Pintem de roig totes les cares exteriors del cub gran. Quants cubets no tindran cap cara pintada?",
     r"Total: $5^{3}=\res{125}$. \ Sense pintar queden els de dins, un cub de $3$ d'aresta: $3^{3}=\res{27}$."),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
pre = pre.replace('\\usepackage{icomma}\n', '\\usepackage{icomma}\n\\usepackage{cancel}\n')
KW = 'pdfkeywords={nombres naturals, aproximació, arrodoniment, truncament, operacions combinades, potències, potències de 10, arrels quadrades}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 1: Nombres naturals. 1r d'ESO}" % (t if sol else "Fitxa d'exercicis"))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 1: Nombres naturals · 1r d'ESO" % t)
    assert 'Unitat 1' in p and 'unitat 1' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\begin{document}
\thispagestyle{primera}

\begin{minipage}[c]{0.25\textwidth}\includegraphics[width=\linewidth]{logo-gva.png}\end{minipage}%
\begin{minipage}[c]{0.5\textwidth}\centering
  {\color{navy}\Large\bfseries ''' + ('Solucions de la fitxa de la unitat 1:' if sol else "Fitxa d'exercicis de la unitat 1:") + r'''\\[2pt] Nombres naturals}\\[5pt]
  {\color{accent}\large\bfseries 1r d'ESO}
\end{minipage}%
\begin{minipage}[c]{0.25\textwidth}\hfill\includegraphics[width=0.85\linewidth]{logo-vermellar.png}\end{minipage}

\vspace{6pt}
{\color{navy}\hrule height 1.2pt}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Les taules es poden completar directament en la fitxa. Fes els càlculs sense calculadora.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't1-fitxa-solucions.tex' if sol else 't1-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
