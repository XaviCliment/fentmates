# Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (1r ESO, Unitat 2: Divisibilitat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'

def recorda(t): return '\\recorda{%s}' % t

S = []  # [(títol, [(estrelles, enunciat, solució)])]
Y, N = r'\checkmark', r'$\times$'

# =====================================================================
S.append(("La relació de divisibilitat", [
 (1, r"Fes la divisió i digues si el primer nombre és múltiple del segon:" + tasks(4, [r"$84$ i $7$", r"$95$ i $8$", r"$132$ i $12$", r"$200$ i $15$"])
     + recorda(r"$a$ és \textbf{múltiple} de $b$ (i $b$ és \textbf{divisor} de $a$) quan la divisió $a:b$ és \textbf{exacta}: residu 0."),
     tasks(2, [r"$84=7\cdot12$: \res{\text{sí}}", r"$95=8\cdot11+7$: \res{\text{no}}", r"$132=12\cdot11$: \res{\text{sí}}", r"$200=15\cdot13+5$: \res{\text{no}}"])),
 (1, r"Completa amb la paraula \emph{múltiple} o \emph{divisor}:" + tasks(2, [r"$35$ és \rule{2cm}{0.4pt} de $7$.", r"$9$ és \rule{2cm}{0.4pt} de $63$.", r"$100$ és \rule{2cm}{0.4pt} de $25$.", r"$13$ és \rule{2cm}{0.4pt} de $52$."]),
     tasks(4, [r"múltiple", r"divisor", r"múltiple", r"divisor"])),
 (1, r"A partir de la igualtat $8\cdot9=72$, escriu quatre frases amb les paraules \emph{múltiple} i \emph{divisor}.",
     r"$72$ és múltiple de $8$; \ $72$ és múltiple de $9$; \ $8$ és divisor de $72$; \ $9$ és divisor de $72$."),
 (2, r"Vertader o fals? Justifica-ho:" + tasks(2, [r"$48$ és divisible per $6$.", r"$7$ és divisor de $77$.", r"$120$ és múltiple de $9$.", r"$0$ és múltiple de $15$.", r"$1$ és múltiple de $3$."]),
     tasks(1, [r"\res{\text{V}}: $48=6\cdot8$.", r"\res{\text{V}}: $77=7\cdot11$.", r"\res{\text{F}}: $120=9\cdot13+3$.", r"\res{\text{V}}: $0=15\cdot0$.", r"\res{\text{F}}: $1:3$ no és exacta (és $3$ el que és múltiple d'$1$)."])),
 (2, r"Quin és el nombre més xicotet que cal sumar a $100$ perquè el resultat siga múltiple de $9$? I el més xicotet que cal restar-li?",
     r"$100=9\cdot11+1$. \ Sumar: $\res{8}$ ($108=9\cdot12$). \ Restar: $\res{1}$ ($99=9\cdot11$)."),
 (3, r"En una divisió exacta, el divisor és $13$ i el quocient, $17$. Quin és el dividend? Amb el mateix divisor i quocient, quin és el dividend més gran que pot tindre una divisió \emph{no} exacta?",
     r"Exacta: $13\cdot17=\res{221}$. \ El residu com a molt és $12$: $221+12=\res{233}$."),
 (3, r"Troba tots els nombres de dues xifres que són múltiples de $7$ i acaben en $4$.",
     r"Dels múltiples de 7 de dues xifres ($14, 21, \ldots, 98$), acaben en 4: $\res{14}$ i $\res{84}$."),
]))

S.append(("Múltiples d'un nombre", [
 (1, r"Escriu els deu primers múltiples (sense el 0) de:" + tasks(3, [r"$7$", r"$11$", r"$15$"]),
     tasks(1, [r"$7,\ 14,\ 21,\ 28,\ 35,\ 42,\ 49,\ 56,\ 63,\ 70$", r"$11,\ 22,\ 33,\ 44,\ 55,\ 66,\ 77,\ 88,\ 99,\ 110$", r"$15,\ 30,\ 45,\ 60,\ 75,\ 90,\ 105,\ 120,\ 135,\ 150$"])),
 (1, r"Quins d'aquests nombres són múltiples de $6$? \[18\qquad 26\qquad 36\qquad 45\qquad 54\qquad 60\qquad 75\qquad 96\]",
     r"$\res{18,\ 36,\ 54,\ 60,\ 96}$ \ (la resta no donen divisió exacta entre 6)."),
 (2, r"Escriu els múltiples de $13$ compresos entre $100$ i $170$.",
     r"$100=13\cdot7+9$: el primer és $13\cdot8=104$. \ $\res{104,\ 117,\ 130,\ 143,\ 156,\ 169}$."),
 (2, r"Quants múltiples de $9$ hi ha entre $1$ i $200$? I entre $100$ i $200$?",
     r"$200:9\to q=22$: \ n'hi ha $\res{22}$. \ Fins a $99$ n'hi ha $11$, així que entre 100 i 200: $22-11=\res{11}$ (del $108$ al $198$)."),
 (2, r"Escriu els múltiples comuns de $6$ i de $9$ menors que $100$ (sense el 0). Quin és el més xicotet?",
     r"$\res{18,\ 36,\ 54,\ 72,\ 90}$. El més xicotet és $18$ (el seu mcm)."),
 (3, r"Quin és el múltiple de $17$ més pròxim a $300$?",
     r"$300=17\cdot17+11$: els múltiples més pròxims són $289$ (a 11) i $306$ (a 6). \ El més pròxim és $\res{306}$."),
 (3, r"Escriu el múltiple de $12$ més gran que tinga tres xifres i el més xicotet que en tinga quatre.",
     r"$999=12\cdot83+3$: \ $12\cdot83=\res{996}$ \ i \ $12\cdot84=\res{1008}$."),
]))

S.append(("Divisors d'un nombre", [
 (1, r"Calcula tots els divisors de:" + tasks(4, [r"$15$", r"$21$", r"$28$", r"$32$"])
     + recorda(r"Dividim entre $1, 2, 3\ldots$ Cada divisió exacta dona dos divisors (el divisor i el quocient). Parem quan el quocient és menor o igual que el divisor."),
     tasks(2, [r"$\{1,\ 3,\ 5,\ 15\}$", r"$\{1,\ 3,\ 7,\ 21\}$", r"$\{1,\ 2,\ 4,\ 7,\ 14,\ 28\}$", r"$\{1,\ 2,\ 4,\ 8,\ 16,\ 32\}$"])),
 (1, r"Quins d'aquests nombres són divisors de $60$? \[4\qquad 7\qquad 9\qquad 12\qquad 15\qquad 25\qquad 30\]",
     r"$\res{4,\ 12,\ 15,\ 30}$ \ ($60=4\cdot15=12\cdot5=15\cdot4=30\cdot2$)."),
 (2, r"Calcula tots els divisors de:" + tasks(4, [r"$48$", r"$72$", r"$90$", r"$100$"]),
     tasks(1, [r"$\{1,2,3,4,6,8,12,16,24,48\}$", r"$\{1,2,3,4,6,8,9,12,18,24,36,72\}$", r"$\{1,2,3,5,6,9,10,15,18,30,45,90\}$", r"$\{1,2,4,5,10,20,25,50,100\}$"])),
 (2, r"Escriu els divisors comuns de $24$ i de $36$. Quin és el més gran?",
     r"$\res{1,\ 2,\ 3,\ 4,\ 6,\ 12}$. El més gran és $12$ (el seu MCD)."),
 (2, r"En Pau té 36 cromos i els vol col·locar formant files, totes amb el mateix nombre de cromos. De quantes maneres ho pot fer?",
     r"Tantes com divisors té 36: $1\times36,\ 2\times18,\ 3\times12,\ 4\times9,\ 6\times6,\ 9\times4,\ 12\times3,\ 18\times2,\ 36\times1$: \ $\res{9\text{ maneres}}$."),
 (3, r"Quin és el nombre menor que $50$ que té més divisors?",
     r"El $\res{48}$, amb 10 divisors: $1, 2, 3, 4, 6, 8, 12, 16, 24, 48$."),
 (3, r"Troba un nombre que tinga exactament $4$ divisors i un altre que en tinga exactament $5$.",
     r"Per exemple, $\res{6}$: $\{1,2,3,6\}$ \ i \ $\res{16}$: $\{1,2,4,8,16\}$."),
]))

TH = r"\textbf{Nombre} & $\boldsymbol{\div2}$ & $\boldsymbol{\div3}$ & $\boldsymbol{\div5}$ & $\boldsymbol{\div9}$ & $\boldsymbol{\div11}$\\\hline "
def ctab(rows):
    return (r"\par\smallskip{\renewcommand{\arraystretch}{1.5}\centering\begin{tabular}{|C{2.4cm}|C{1.5cm}|C{1.5cm}|C{1.5cm}|C{1.5cm}|C{1.5cm}|}\hline\rowcolor{soft}" + TH
            + ''.join(' & '.join(r) + r'\\\hline ' for r in rows) + r"\end{tabular}\par}")
CN = ['3080', '7425', '1188', '2543', '6735']
CS = {'3080': '2 5 11', '7425': '3 5 9 11', '1188': '2 3 9 11', '2543': '', '6735': '3 5'}
S.append(("Criteris de divisibilitat", [
 (1, r"Completa la taula: marca amb una creu els nombres pels quals és divisible cada nombre." + ctab([['$%s$' % n] + [''] * 5 for n in CN])
     + recorda(r"Per \textbf{2}: acaba en xifra parella. \ Per \textbf{3}: la suma de les xifres és múltiple de 3. \ Per \textbf{5}: acaba en 0 o 5. \ Per \textbf{9}: la suma de les xifres és múltiple de 9. \ Per \textbf{11}: la diferència entre la suma de les xifres de lloc senar i la de lloc parell és 0 o múltiple d'11."),
     ctab([['$%s$' % n] + [Y if k in CS[n].split() else N for k in ['2', '3', '5', '9', '11']] for n in CN])
     + r"\par El $2543$ no és divisible per cap: és senar, les xifres sumen 14 i la diferència per a l'11 és $8-6=2$."),
 (1, r"Escriu tres nombres de tres xifres que siguen divisibles per $3$ però no per $9$.",
     r"Per exemple, $\res{102,\ 111,\ 123}$: les xifres sumen 3, 3 i 6 (múltiples de 3, però no de 9)."),
 (2, r"Quines xifres pots posar en lloc de $\square$ perquè $5\square4$ siga divisible per $3$? I per $9$?",
     r"$5+4=9$. \ Per 3: $\square=0,3,6,9$ \ ($\res{504,\ 534,\ 564,\ 594}$). \ Per 9: $\square=0$ o $9$ \ ($\res{504,\ 594}$)."),
 (2, r"Quina xifra cal posar en lloc de $\square$ perquè $38\square$ siga divisible per $2$ i per $3$ alhora?",
     r"Per 3: $11+\square$ múltiple de 3, \ $\square=1, 4, 7$. Per 2 ha de ser parella: $\square=4$, \ $\res{384}$."),
 (2, r"Comprova, amb el criteri, si aquests nombres són divisibles per $11$:" + tasks(4, [r"$2849$", r"$9375$", r"$50\,182$", r"$13\,575$"]),
     tasks(2, [r"$(9+8)-(4+2)=11$: \res{\text{sí}}", r"$(7+9)-(5+3)=8$: \res{\text{no}}", r"$(2+1+5)-(8+0)=0$: \res{\text{sí}}", r"$(5+5+1)-(7+3)=1$: \res{\text{no}}"])),
 (3, r"Troba el nombre més gran de tres xifres que siga divisible per $2$, per $3$ i per $5$ alhora.",
     r"Ha d'acabar en 0 (per 2 i per 5) i les xifres han de sumar un múltiple de 3: $\res{990}$ ($9+9+0=18$)."),
 (3, r"Troba totes les xifres $a$ i $b$ perquè el nombre $7a2b$ siga divisible per $5$ i per $9$ alhora.",
     r"Per 5: $b=0$ o $5$. \ Si $b=0$: $9+a$ múltiple de 9, $a=0$ o $9$. \ Si $b=5$: $14+a$, $a=4$. \ \ $\res{7020,\ 7920,\ 7425}$."),
]))

S.append(("Nombres primers i compostos", [
 (1, r"Escriu els divisors de cada nombre i digues si és primer o compost:" + tasks(3, [r"$11$", r"$15$", r"$19$", r"$27$", r"$31$", r"$49$"])
     + recorda(r"Un nombre és \textbf{primer} si només té dos divisors: l'1 i ell mateix. Si en té més, és \textbf{compost}. L'1 no és ni primer ni compost."),
     tasks(3, [r"$\{1,11\}$: primer", r"$\{1,3,5,15\}$: compost", r"$\{1,19\}$: primer", r"$\{1,3,9,27\}$: compost", r"$\{1,31\}$: primer", r"$\{1,7,49\}$: compost"])),
 (1, r"Escriu tots els nombres primers compresos entre $60$ i $100$.",
     r"$\res{61,\ 67,\ 71,\ 73,\ 79,\ 83,\ 89,\ 97}$."),
 (2, r"Esbrina si són primers dividint-los entre $2, 3, 5, 7, 11\ldots$ fins que el quocient siga menor que el divisor:" + tasks(4, [r"$87$", r"$107$", r"$133$", r"$149$"]),
     tasks(2, [r"$87=3\cdot29$: \res{\text{compost}}", r"$107:11\to q=9<11$: \res{\text{primer}}", r"$133=7\cdot19$: \res{\text{compost}}", r"$149:13\to q=11<13$: \res{\text{primer}}"])),
 (2, r"Escriu cada nombre com a suma de dos nombres primers:" + tasks(4, [r"$16$", r"$24$", r"$36$", r"$50$"]),
     tasks(2, [r"$3+13=5+11$", r"$5+19=7+17=11+13$", r"$5+31=7+29=13+23=17+19$", r"$3+47=7+43=13+37=19+31$"]) + r"\par (N'hi ha prou amb una manera.)"),
 (2, r"Explica per què cap nombre acabat en $5$, més gran que $5$, pot ser primer. I per què cap nombre parell més gran que $2$ pot ser primer?",
     r"Si acaba en 5, és divisible per 5: té almenys els divisors 1, 5 i ell mateix. Si és parell, és divisible per 2: té almenys els divisors 1, 2 i ell mateix."),
 (3, r"L'any $2027$ és un nombre primer? I el $2028$?",
     r"$2027$ no és divisible per cap primer fins al $43$, i $47\cdot47=2209>2027$: és \res{\text{primer}}. \ $2028$ és parell: \res{\text{compost}} ($2028=2^{2}\cdot3\cdot13^{2}$)."),
 (3, r"Troba tres nombres primers consecutius la suma dels quals siga també un nombre primer.",
     r"Per exemple, $5+7+11=\res{23}$ \ o \ $7+11+13=\res{31}$."),
]))

S.append(("Descomposició en factors primers", [
 (1, r"Descompon en factors primers:" + tasks(4, [r"$36$", r"$50$", r"$72$", r"$81$"])
     + recorda(r"Dividim entre el primer més xicotet possible (2, 3, 5, 7\ldots) fins a arribar a 1, i escrivim els factors repetits com a potència: $\ 360=2^{3}\cdot3^{2}\cdot5$."),
     tasks(4, [r"$2^{2}\cdot3^{2}$", r"$2\cdot5^{2}$", r"$2^{3}\cdot3^{2}$", r"$3^{4}$"])),
 (1, r"Descompon en factors primers:" + tasks(4, [r"$120$", r"$126$", r"$196$", r"$225$"]),
     tasks(4, [r"$2^{3}\cdot3\cdot5$", r"$2\cdot3^{2}\cdot7$", r"$2^{2}\cdot7^{2}$", r"$3^{2}\cdot5^{2}$"])),
 (2, r"Descompon en factors primers:" + tasks(4, [r"$540$", r"$784$", r"$1260$", r"$2310$"]),
     tasks(4, [r"$2^{2}\cdot3^{3}\cdot5$", r"$2^{4}\cdot7^{2}$", r"$2^{2}\cdot3^{2}\cdot5\cdot7$", r"$2\cdot3\cdot5\cdot7\cdot11$"])),
 (2, r"Quin nombre té cada descomposició?" + tasks(4, [r"$2^{4}\cdot3$", r"$2\cdot3^{2}\cdot7$", r"$2^{2}\cdot5^{3}$", r"$3\cdot5\cdot11$"]),
     tasks(4, [r"$48$", r"$126$", r"$500$", r"$165$"])),
 (2, r"Completa les descomposicions:" + tasks(3, [r"$2^{\square}\cdot3\cdot5^{\square}=600$", r"$2^{2}\cdot3^{\square}\cdot7=252$", r"$2\cdot\square^{2}\cdot5=90$"]),
     tasks(3, [r"$2^{3}\cdot3\cdot5^{2}$", r"$2^{2}\cdot3^{2}\cdot7$", r"$2\cdot3^{2}\cdot5$"])),
 (3, r"Per quin nombre, el més xicotet possible, cal multiplicar $90$ perquè el resultat siga un quadrat perfecte?",
     r"$90=2\cdot3^{2}\cdot5$: falta un 2 i un 5 perquè tots els exponents siguen parells. Per $\res{10}$: $900=2^{2}\cdot3^{2}\cdot5^{2}=30^{2}$."),
 (3, r"Un nombre té la descomposició $2^{2}\cdot3\cdot5$. Quin nombre és? Escriu tots els seus divisors.",
     r"És el $60$. \ Divisors: $\res{1,\ 2,\ 3,\ 4,\ 5,\ 6,\ 10,\ 12,\ 15,\ 20,\ 30,\ 60}$."),
]))

S.append(("Mínim comú múltiple", [
 (1, r"Calcula el mcm escrivint la llista de múltiples:" + tasks(4, [r"$\text{mcm}(3,4)$", r"$\text{mcm}(6,9)$", r"$\text{mcm}(8,10)$", r"$\text{mcm}(5,15)$"]),
     tasks(4, [r"$12$", r"$18$", r"$40$", r"$15$"])),
 (1, r"Calcula el mcm a partir de la descomposició en factors primers:" + tasks(4, [r"$\text{mcm}(12,20)$", r"$\text{mcm}(18,30)$", r"$\text{mcm}(24,36)$", r"$\text{mcm}(14,21)$"])
     + recorda(r"\textbf{mcm}: factors \textbf{comuns i no comuns}, cadascun amb el \textbf{major} exponent."),
     tasks(2, [r"$2^{2}\cdot3\cdot5=\res{60}$", r"$2\cdot3^{2}\cdot5=\res{90}$", r"$2^{3}\cdot3^{2}=\res{72}$", r"$2\cdot3\cdot7=\res{42}$"])),
 (2, r"Calcula:" + tasks(4, [r"$\text{mcm}(40,60)$", r"$\text{mcm}(36,54)$", r"$\text{mcm}(45,75)$", r"$\text{mcm}(28,42)$"]),
     tasks(2, [r"$2^{3}\cdot3\cdot5=\res{120}$", r"$2^{2}\cdot3^{3}=\res{108}$", r"$3^{2}\cdot5^{2}=\res{225}$", r"$2^{2}\cdot3\cdot7=\res{84}$"])),
 (2, r"Calcula:" + tasks(3, [r"$\text{mcm}(6,8,12)$", r"$\text{mcm}(10,12,15)$", r"$\text{mcm}(8,18,27)$"]),
     tasks(3, [r"$2^{3}\cdot3=\res{24}$", r"$2^{2}\cdot3\cdot5=\res{60}$", r"$2^{3}\cdot3^{3}=\res{216}$"])),
 (2, r"Calcula sense descompondre i explica com ho has fet:" + tasks(4, [r"$\text{mcm}(9,10)$", r"$\text{mcm}(7,35)$", r"$\text{mcm}(11,13)$", r"$\text{mcm}(16,48)$"]),
     tasks(2, [r"$\res{90}$: no tenen factors comuns", r"$\res{35}$: 35 és múltiple de 7", r"$\res{143}$: tots dos són primers", r"$\res{48}$: 48 és múltiple de 16"])),
 (3, r"Calcula el mcm de $\ a=2^{3}\cdot3^{2}\cdot7\ $ i $\ b=2^{2}\cdot3^{3}\cdot5$.",
     r"$2^{3}\cdot3^{3}\cdot5\cdot7=8\cdot27\cdot35=\res{7560}$."),
 (3, r"El mcm de dos nombres és $60$ i un d'ells és $12$. Quins valors pot tindre l'altre?",
     r"$60=2^{2}\cdot3\cdot5$ i $12=2^{2}\cdot3$: l'altre ha de dividir 60 i tindre el factor 5. \ $\res{5,\ 10,\ 15,\ 20,\ 30,\ 60}$."),
]))

S.append(("Problemes de mcm", [
 (1, r"Un far s'encén cada $9$ segons i un altre, cada $12$. Si ara s'han encés tots dos alhora, d'ací a quant de temps tornaran a coincidir?"
     + recorda(r"Si hi ha coses que es \textbf{repeteixen} i volem saber quan tornaran a \textbf{coincidir}, o busquem el nombre \textbf{més xicotet} que és múltiple de diversos, fem servir el \textbf{mcm}."),
     r"$\text{mcm}(9,12)=2^{2}\cdot3^{2}=\res{36\text{ s}}$."),
 (1, r"La Laia entrena a futbol cada $3$ dies i va a natació cada $4$. Hui ha fet les dues coses. D'ací a quants dies les tornarà a fer el mateix dia?",
     r"$\text{mcm}(3,4)=\res{12\text{ dies}}$."),
 (2, r"Tres amics van al cinema: un cada $6$ dies, un altre cada $8$ i l'altre cada $10$. Si hui hi han coincidit, d'ací a quants dies tornaran a coincidir?",
     r"$\text{mcm}(6,8,10)=2^{3}\cdot3\cdot5=\res{120\text{ dies}}$."),
 (2, r"Quin és el nombre més xicotet de llapis que es pot empaquetar en capses de $12$, de $15$ o de $18$ sense que en sobre cap?",
     r"$\text{mcm}(12,15,18)=2^{2}\cdot3^{2}\cdot5=\res{180\text{ llapis}}$."),
 (2, r"Dos autobusos ixen junts de la parada a les 7:30. Un hi torna cada $20$ minuts i l'altre, cada $25$. A quina hora tornaran a coincidir?",
     r"$\text{mcm}(20,25)=2^{2}\cdot5^{2}=100$ min $=1$ h $40$ min: \ a les $\res{9{:}10}$."),
 (3, r"Si agrupem les galetes d'una caixa de $6$ en $6$, de $8$ en $8$ o de $10$ en $10$, sempre en sobren $3$. Quantes galetes hi ha com a mínim? I si sabem que n'hi ha entre $200$ i $300$?",
     r"$\text{mcm}(6,8,10)=120$: com a mínim $120+3=\res{123}$. \ Entre 200 i 300: $240+3=\res{243}$."),
 (3, r"Una roda dentada de $15$ dents engrana amb una altra de $24$ dents. Quantes voltes ha de fer cadascuna perquè tornen a estar en la posició inicial?",
     r"$\text{mcm}(15,24)=2^{3}\cdot3\cdot5=120$ dents: \ la primera fa $120:15=\res{8\text{ voltes}}$ i la segona, $120:24=\res{5\text{ voltes}}$."),
]))

S.append(("Màxim comú divisor", [
 (1, r"Calcula el MCD escrivint la llista de divisors:" + tasks(4, [r"$\text{MCD}(8,12)$", r"$\text{MCD}(15,20)$", r"$\text{MCD}(18,27)$", r"$\text{MCD}(14,25)$"]),
     tasks(4, [r"$4$", r"$5$", r"$9$", r"$1$"])),
 (1, r"Calcula el MCD a partir de la descomposició en factors primers:" + tasks(4, [r"$\text{MCD}(24,36)$", r"$\text{MCD}(30,45)$", r"$\text{MCD}(42,56)$", r"$\text{MCD}(60,90)$"])
     + recorda(r"\textbf{MCD}: \textbf{només} els factors \textbf{comuns}, cadascun amb el \textbf{menor} exponent. Si no n'hi ha cap de comú, el MCD és 1 (\emph{primers entre si})."),
     tasks(2, [r"$2^{2}\cdot3=\res{12}$", r"$3\cdot5=\res{15}$", r"$2\cdot7=\res{14}$", r"$2\cdot3\cdot5=\res{30}$"])),
 (2, r"Calcula:" + tasks(4, [r"$\text{MCD}(84,126)$", r"$\text{MCD}(120,180)$", r"$\text{MCD}(96,144)$", r"$\text{MCD}(105,165)$"]),
     tasks(2, [r"$2\cdot3\cdot7=\res{42}$", r"$2^{2}\cdot3\cdot5=\res{60}$", r"$2^{4}\cdot3=\res{48}$", r"$3\cdot5=\res{15}$"])),
 (2, r"Calcula:" + tasks(3, [r"$\text{MCD}(12,18,30)$", r"$\text{MCD}(24,40,56)$", r"$\text{MCD}(45,75,105)$"]),
     tasks(3, [r"$2\cdot3=\res{6}$", r"$2^{3}=\res{8}$", r"$3\cdot5=\res{15}$"])),
 (2, r"Quines d'aquestes parelles són primers entre si?" + tasks(4, [r"$8$ i $21$", r"$15$ i $25$", r"$14$ i $27$", r"$22$ i $33$"]),
     tasks(2, [r"\res{\text{sí}} ($\text{MCD}=1$)", r"no ($\text{MCD}=5$)", r"\res{\text{sí}} ($\text{MCD}=1$)", r"no ($\text{MCD}=11$)"])),
 (3, r"Calcula el MCD i el mcm de $36$ i $60$, i comprova que $\text{MCD}\cdot\text{mcm}=36\cdot60$.",
     r"$36=2^{2}\cdot3^{2}$, \ $60=2^{2}\cdot3\cdot5$: \ $\text{MCD}=\res{12}$, \ $\text{mcm}=\res{180}$. \ $12\cdot180=2160=36\cdot60$ \checkmark"),
 (3, r"El MCD de dos nombres és $8$ i el seu mcm, $96$. Si un dels nombres és $24$, quin és l'altre?",
     r"$\text{MCD}\cdot\text{mcm}=a\cdot b$: \ $8\cdot96=768$; \ $768:24=\res{32}$."),
]))

S.append(("Problemes de MCD", [
 (1, r"Tenim $30$ pomes i $45$ taronges i volem fer el màxim nombre de lots iguals, sense que sobre cap fruita. Quants lots podem fer? Què portarà cada lot?"
     + recorda(r"Si volem \textbf{repartir} o \textbf{tallar} en parts iguals, \textbf{sense que sobre res}, i les parts han de ser \textbf{el més grans possible} (o el màxim nombre de grups), fem servir el \textbf{MCD}."),
     r"$\text{MCD}(30,45)=15$: \ $\res{15\text{ lots}}$, cadascun amb $2$ pomes i $3$ taronges."),
 (1, r"Volem tallar dues cordes de $36$ m i $48$ m en trossos iguals, el més llargs possible. Quant farà cada tros? Quants trossos tindrem?",
     r"$\text{MCD}(36,48)=\res{12\text{ m}}$; \ $3+4=\res{7\text{ trossos}}$."),
 (2, r"Volem enrajolar un terra de $360$ cm per $280$ cm amb rajoles quadrades, el més grans possible, sense tallar-ne cap. Quant farà el costat de cada rajola? Quantes rajoles calen?",
     r"$\text{MCD}(360,280)=2^{3}\cdot5=\res{40\text{ cm}}$; \ $9\cdot7=\res{63\text{ rajoles}}$."),
 (2, r"Una llibreria té $120$ llibres de contes, $84$ de poesia i $60$ còmics. Vol fer paquets amb el mateix nombre de llibres, tots d'un sol tipus i el més grans possible. Quants llibres hi haurà en cada paquet? Quants paquets farà?",
     r"$\text{MCD}(120,84,60)=\res{12\text{ llibres}}$; \ $10+7+5=\res{22\text{ paquets}}$."),
 (2, r"Digues si cal calcular el mcm o el MCD i resol:" + tasks(1, [r"Un rellotge sona cada $15$ minuts i un altre, cada $25$. Si ara han sonat junts, quan tornaran a coincidir?", r"Volem repartir $48$ bolígrafs i $64$ llapis en el màxim nombre d'estoigs iguals, sense que en sobre cap."]),
     tasks(1, [r"mcm: $\text{mcm}(15,25)=\res{75\text{ min}}$.", r"MCD: $\text{MCD}(48,64)=\res{16\text{ estoigs}}$, amb 3 bolígrafs i 4 llapis cadascun."])),
 (3, r"Una mestra reparteix $75$ cromos i $105$ adhesius entre l'alumnat, de manera que tots reben la mateixa quantitat de cada cosa. Li sobren $3$ cromos i $9$ adhesius. Quants alumnes hi pot haver, com a màxim? Quants cromos i adhesius rep cadascú?",
     r"S'han repartit $72$ cromos i $96$ adhesius: \ $\text{MCD}(72,96)=\res{24\text{ alumnes}}$ (més gran que 9). Cadascú rep $\res{3}$ cromos i $\res{4}$ adhesius."),
 (3, r"Volem plantar arbres al voltant d'un jardí rectangular de $72$ m per $48$ m, a la mateixa distància entre ells, la més gran possible i amb un arbre a cada cantonada. A quina distància els plantarem? Quants arbres calen?",
     r"$\text{MCD}(72,48)=\res{24\text{ m}}$. \ Perímetre: $2\cdot(72+48)=240$ m; \ $240:24=\res{10\text{ arbres}}$."),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={divisibilitat, múltiples, divisors, criteris de divisibilitat, nombres primers, factors primers, mcm, MCD}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 2: Divisibilitat. 1r d'ESO}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 2: Divisibilitat · 1r d'ESO" % t)
    assert 'Unitat 2' in p and 'unitat 2' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\begin{document}
\thispagestyle{primera}

\begin{minipage}[c]{0.25\textwidth}\includegraphics[width=\linewidth]{logo-gva.png}\end{minipage}%
\begin{minipage}[c]{0.5\textwidth}\centering
  {\color{navy}\Large\bfseries ''' + ('Solucions de la fitxa de la unitat 2:' if sol else "Fitxa d'exercicis de la unitat 2:") + r'''\\[2pt] Divisibilitat}\\[5pt]
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
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. La taula es pot completar directament en la fitxa. Fes els càlculs sense calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't2-fitxa-solucions.tex' if sol else 't2-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
