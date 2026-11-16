# Genera t2-fitxa-exercicis.tex i t2-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 2: Nombres reals)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució), en valencià i castellà amb T(va, es).
# Les eines (intervals exactes amb fraccions, recta real en TikZ, ck/eq per a comprovar) són a ../comu/eso4b.py,
# com a les fitxes de 4t ESO B; build(..., curs='4eso-a') posa la capçalera de Matemàtiques A.
# Les solucions de fraccions i intervals es calculen ací (aritmètica exacta) i les de radicals es comproven amb eq() (sympy).
# Ús: python3 genera.py (valencià) i python3 genera-es.py (castellà); després pdflatex dues vegades cada .tex.
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

LANG = 'es' if (len(sys.argv) > 1 and sys.argv[1] == 'es') else 'va'
def T(va, es): return es if LANG == 'es' else va

S = []
def chk(pairs, **kw):
    for a, b in pairs: eq(a, b, **kw)
NR = T(r"No és un nombre real.", r"No es un número real.")

# =====================================================================
# 1. Classificació dels nombres reals
chk([('18/3', 6), ('-sqrt(25)', -5), ('real_root(-27,3)', -3), ('sqrt(Rational(4,9))', 'Rational(2,3)'), ('sqrt(12)/sqrt(3)', 2)])
ck(per('0', '', '7'), F(7, 9)); ck(per('2', '', '03'), F(201, 99))
v5 = {'s10': math.sqrt(10), 'f': 19 / 6, 'pi': math.pi, 'p': float(per('3', '', '1')), 'd': 3.14}
ck(sorted(v5, key=v5.get), ['p', 'd', 'pi', 's10', 'f'])
TAULA = [r"-3", r"\dfrac52", r"\sqrt7", r"0", r"-1,\widehat6", r"\sqrt{16}", r"\dfrac{\pi}{3}"]
PERT = ["ZQR", "QR", "IR", "NZQR", "QR", "NZQR", "IR"]   # conjunts als quals pertany cada nombre
def taula(sol):
    o = [r"\begin{center}\renewcommand{\arraystretch}{1.6}\begin{tabular}{|C{1.6cm}|C{1.1cm}|C{1.1cm}|C{1.1cm}|C{1.1cm}|C{1.1cm}|}\hline",
         r"\rowcolor{soft} & $\mathbb N$ & $\mathbb Z$ & $\mathbb Q$ & $\mathbb I$ & $\mathbb R$\\\hline"]
    for x, p in zip(TAULA, PERT):
        o.append('$' + x + '$ & ' + ' & '.join((r'\textcolor{accent}{\checkmark}' if c in p else '') if sol else '' for c in 'NZQIR') + r'\\\hline')
    return '\n'.join(o + [r"\end{tabular}\end{center}"])
S.append((T("Classificació dels nombres reals", "Clasificación de los números reales"), [
 (1, T(r"Indica el menor conjunt numèric ($\mathbb N$, $\mathbb Z$, $\mathbb Q$ o $\mathbb I$) al qual pertany cada nombre:", r"Indica el menor conjunto numérico ($\mathbb N$, $\mathbb Z$, $\mathbb Q$ o $\mathbb I$) al que pertenece cada número:")
     + tasks(4, [r"$\dfrac{18}{3}$", r"$-\sqrt{25}$", r"$0,\widehat7$", r"$\sqrt{20}$", r"$-\dfrac74$", r"$\sqrt[3]{-27}$", r"$\pi-1$", r"$\sqrt{-9}$", r"$2,\widehat{03}$", r"$\sqrt{\dfrac49}$", r"$1,0100100010\ldots$", r"$\dfrac{\sqrt{12}}{\sqrt3}$"])
     + recorda(T(r"Primer fes les operacions que es puguen fer: $\frac{18}{3}=6$, $\sqrt[3]{-27}=-3$\ldots{} Un decimal exacte o periòdic és racional; un decimal infinit no periòdic és irracional.",
                 r"Primero haz las operaciones que se puedan hacer: $\frac{18}{3}=6$, $\sqrt[3]{-27}=-3$\ldots{} Un decimal exacto o periódico es racional; un decimal infinito no periódico es irracional.")),
     tasks(3, [r"$6\in" + Rm(r"\mathbb N") + "$", r"$-5\in" + Rm(r"\mathbb Z") + "$", r"$\frac79\in" + Rm(r"\mathbb Q") + "$", R(r"\mathbb I"), R(r"\mathbb Q"), r"$-3\in" + Rm(r"\mathbb Z") + "$",
               R(r"\mathbb I"), NR, r"$\frac{201}{99}\in" + Rm(r"\mathbb Q") + "$", r"$\frac23\in" + Rm(r"\mathbb Q") + "$", R(r"\mathbb I") + T(" (no periòdic)", " (no periódico)"), r"$\sqrt4=2\in" + Rm(r"\mathbb N") + "$"])),
 (1, T(r"Copia la taula i marca els conjunts als quals pertany cada nombre:", r"Copia la tabla y marca los conjuntos a los que pertenece cada número:") + taula(False),
     taula(True) + T(r"Fixa't que $\sqrt{16}=4$ i que tots els nombres són reals.", r"Fíjate en que $\sqrt{16}=4$ y en que todos los números son reales.")),
 (1, T(r"Digues si són vertaderes o falses les afirmacions següents. Si són falses, posa'n un contraexemple:", r"Di si son verdaderas o falsas las afirmaciones siguientes. Si son falsas, pon un contraejemplo:")
     + tasks(1, [T("Tot nombre natural és enter.", "Todo número natural es entero."), T("Tot nombre enter és natural.", "Todo número entero es natural."),
                 T("Tot decimal periòdic és racional.", "Todo decimal periódico es racional."), T(r"$\sqrt2=1,414213562$, perquè és el que diu la calculadora.", r"$\sqrt2=1,414213562$, porque es lo que dice la calculadora."),
                 T("Hi ha nombres racionals que també són irracionals.", "Hay números racionales que también son irracionales."), T("La suma de dos irracionals sempre és irracional.", "La suma de dos irracionales siempre es irracional.")]),
     tasks(1, [R(r"\text{V}"), R(r"\text{F}") + r": $-2\in\mathbb Z$, $-2\notin\mathbb N$", R(r"\text{V}") + T(": té fracció generatriu", ": tiene fracción generatriz"),
               R(r"\text{F}") + T(r": és una aproximació; $\sqrt2$ té infinites xifres no periòdiques", r": es una aproximación; $\sqrt2$ tiene infinitas cifras no periódicas"),
               R(r"\text{F}") + T(r": un nombre és racional o irracional, mai les dues coses", r": un número es racional o irracional, nunca las dos cosas"), R(r"\text{F}") + r": $\sqrt2+\left(-\sqrt2\right)=0$"])),
 (2, T("Escriu:", "Escribe:") + tasks(2, [T("un nombre enter que no siga natural;", "un número entero que no sea natural;"), T("un nombre racional que no siga enter;", "un número racional que no sea entero;"),
                                          T("tres nombres irracionals;", "tres números irracionales;"), T("un racional i un irracional compresos entre 3 i 4.", "un racional y un irracional comprendidos entre 3 y 4.")]),
     T("Per exemple:", "Por ejemplo:") + tasks(2, [R("-5"), R(r"\frac34"), R(r"\sqrt3,\ \pi,\ 1+\sqrt5"), R(r"3,5") + T(" i ", " y ") + R(r"\sqrt{10}") + r"\ ($9<10<16$)"])),
 (2, T(r"Ordena de menor a major i indica quins són racionals i quins irracionals (pots fer servir la calculadora): \ $\sqrt{10}$, \ $\frac{19}{6}$, \ $\pi$, \ $3,\widehat1$, \ $3,14$.",
       r"Ordena de menor a mayor e indica cuáles son racionales y cuáles irracionales (puedes usar la calculadora): \ $\sqrt{10}$, \ $\frac{19}{6}$, \ $\pi$, \ $3,\widehat1$, \ $3,14$."),
     r"$\sqrt{10}\approx3,1623$; \ $\frac{19}{6}=3,1\widehat6$; \ $\pi\approx3,1416$: \ " + R(r"3,\widehat1<3,14<\pi<\sqrt{10}<\frac{19}{6}") + r"\\[2pt]"
     + T(r"Racionals: $\frac{19}{6}$, $3,\widehat1$ i $3,14$. Irracionals: $\sqrt{10}$ i $\pi$.", r"Racionales: $\frac{19}{6}$, $3,\widehat1$ y $3,14$. Irracionales: $\sqrt{10}$ y $\pi$.")),
]))

# =====================================================================
# 2. Decimals i fracció generatriu
g7 = [per('0', '75', ''), per('1', '', '4'), per('2', '', '18'), per('0', '1', '6'), per('3', '2', '5'), per('0', '0', '3')]
ck(g7, [F(3, 4), F(13, 9), F(24, 11), F(1, 6), F(293, 90), F(1, 30)])
g8 = [per('0', '', '3') + per('0', '', '6'), per('2', '', '5') - per('1', '', '2'), per('1', '', '2') * per('0', '', '6'), per('0', '1', '6') * F(12, 10)]
ck(g8, [1, F(4, 3), F(22, 27), F(1, 5)])
ck([per('0', '', '9'), per('2', '4', '9')], [1, F(5, 2)])
S.append((T("Decimals i fracció generatriu", "Decimales y fracción generatriz"), [
 (1, T(r"Indica si cada decimal és exacte, periòdic pur, periòdic mixt o no periòdic, i si és racional o irracional:", r"Indica si cada decimal es exacto, periódico puro, periódico mixto o no periódico, y si es racional o irracional:")
     + tasks(3, [r"$3,25$", r"$1,\widehat{36}$", r"$0,8\widehat3$", r"$2,7182818\ldots$ (" + T("el nombre", "el número") + r" $e$)", r"$5,\widehat2$", r"$0,12\widehat{45}$"]),
     tasks(3, [R(T(r"\text{exacte}", r"\text{exacto}")) + r", $\mathbb Q$", R(T(r"\text{periòdic pur}", r"\text{periódico puro}")) + r", $\mathbb Q$", R(T(r"\text{periòdic mixt}", r"\text{periódico mixto}")) + r", $\mathbb Q$",
               R(T(r"\text{no periòdic}", r"\text{no periódico}")) + r", $\mathbb I$", R(T(r"\text{periòdic pur}", r"\text{periódico puro}")) + r", $\mathbb Q$", R(T(r"\text{periòdic mixt}", r"\text{periódico mixto}")) + r", $\mathbb Q$"])),
 (1, T("Calcula la fracció generatriu i simplifica-la:", "Calcula la fracción generatriz y simplifícala:") + tasks(3, [r"$0,75$", r"$1,\widehat4$", r"$2,\widehat{18}$", r"$0,1\widehat6$", r"$3,2\widehat5$", r"$0,0\widehat3$"])
     + recorda(T(r"Periòdic pur: $2,\widehat7=\frac{27-2}{9}$. \ Periòdic mixt: $1,2\widehat3=\frac{123-12}{90}$ (un 9 per cada xifra del període i un 0 per cada xifra de l'anteperíode).",
                 r"Periódico puro: $2,\widehat7=\frac{27-2}{9}$. \ Periódico mixto: $1,2\widehat3=\frac{123-12}{90}$ (un 9 por cada cifra del periodo y un 0 por cada cifra del anteperiodo).")),
     tasks(3, [r"$\frac{75}{100}=" + Rm(r"\frac34") + "$", r"$\frac{14-1}{9}=" + Rm(r"\frac{13}{9}") + "$", r"$\frac{218-2}{99}=\frac{216}{99}=" + Rm(r"\frac{24}{11}") + "$",
               r"$\frac{16-1}{90}=\frac{15}{90}=" + Rm(r"\frac16") + "$", r"$\frac{325-32}{90}=" + Rm(r"\frac{293}{90}") + "$", r"$\frac{3}{90}=" + Rm(r"\frac1{30}") + "$"])),
 (2, T("Escriu els decimals en forma de fracció i opera:", "Escribe los decimales en forma de fracción y opera:") + tasks(2, [r"$0,\widehat3+0,\widehat6$", r"$2,\widehat5-1,\widehat2$", r"$1,\widehat2\cdot0,\widehat6$", r"$0,1\widehat6\cdot1,2$"]),
     tasks(2, [r"$\frac39+\frac69=" + Rm("1") + "$", r"$\frac{23}{9}-\frac{11}{9}=\frac{12}{9}=" + Rm(r"\frac43") + "$", r"$\frac{11}{9}\cdot\frac69=" + Rm(r"\frac{22}{27}") + "$", r"$\frac16\cdot\frac65=" + Rm(r"\frac15") + "$"])),
 (3, T(r"Calcula la fracció generatriu de $0,\widehat9$ i de $2,4\widehat9$. Què hi observes?", r"Calcula la fracción generatriz de $0,\widehat9$ y de $2,4\widehat9$. ¿Qué observas?"),
     r"$0,\widehat9=\frac99=" + Rm("1") + r"$; \ $2,4\widehat9=\frac{249-24}{90}=\frac{225}{90}=" + Rm(r"\frac52=2,5") + r"$. "
     + T(r"Un decimal amb període 9 és igual a un decimal exacte: no hi ha cap nombre entre $0,\widehat9$ i $1$.", r"Un decimal con periodo 9 es igual a un decimal exacto: no hay ningún número entre $0,\widehat9$ y $1$.")),
]))

# =====================================================================
# 3. Intervals i semirectes
I10 = ['[-2,3]', '(1,5)', '[-1,inf)', '(-inf,4)', '(-3,0]', '(-inf,5/2]']
I12 = ['[-3,1)', '(-inf,2]', '(-1,4]', '(0,inf)']
S.append((T("Intervals i semirectes", "Intervalos y semirrectas"), [
 (1, T("Escriu com a interval o semirecta i representa'l en la recta real:", "Escribe como intervalo o semirrecta y represéntalo en la recta real:")
     + tasks(3, [r"$-2\le x\le3$", r"$1<x<5$", r"$x\ge-1$", r"$x<4$", r"$-3<x\le0$", r"$x\le\frac52$"])
     + recorda(T(r"Si l'extrem hi pertany ($\le$, $\ge$), claudàtor $[\ ]$ i punt ple; si no ($<$, $>$), parèntesi $(\ )$ i punt buit. A l'infinit, sempre parèntesi.",
                 r"Si el extremo pertenece ($\le$, $\ge$), corchete $[\ ]$ y punto lleno; si no ($<$, $>$), paréntesis $(\ )$ y punto vacío. En el infinito, siempre paréntesis.")),
     tasks(2, [RI(x, -4, 6) for x in I10])),
 (1, T("Escriu la desigualtat que correspon a cada interval o semirecta i representa'l:", "Escribe la desigualdad que corresponde a cada intervalo o semirrecta y represéntalo:")
     + tasks(4, [r"$[-4, 1)$", r"$(0, 6]$", r"$(-\infty, -2]$", r"$(3, +\infty)$"]),
     tasks(2, [R(r"-4\le x<1") + r"\\[2pt]" + recta(P('[-4,1)'), -5, 7), R(r"0<x\le6") + r"\\[2pt]" + recta(P('(0,6]'), -5, 7),
               R(r"x\le-2") + r"\\[2pt]" + recta(P('(-inf,-2]'), -5, 7), R(r"x>3") + r"\\[2pt]" + recta(P('(3,inf)'), -5, 7)])),
 (1, T("Escriu l'interval o la semirecta que hi ha representat en cada cas, i també la desigualtat:", "Escribe el intervalo o la semirrecta que hay representado en cada caso, y también la desigualdad:")
     + tasks(2, [recta(P(x), -5, 6) for x in I12]),
     tasks(2, [R(r"[-3, 1)") + r"\ \ $-3\le x<1$", R(r"(-\infty, 2]") + r"\ \ $x\le2$", R(r"(-1, 4]") + r"\ \ $-1<x\le4$", R(r"(0, +\infty)") + r"\ \ $x>0$"])),
 (2, T("Expressa amb un interval o una semirecta:", "Expresa con un intervalo o una semirrecta:")
     + tasks(1, [T(r"els nombres majors que $-3$ i menors o iguals que 2;", r"los números mayores que $-3$ y menores o iguales que 2;"), T("els nombres reals no negatius;", "los números reales no negativos;"),
                 T("els nombres menors que 5;", "los números menores que 5;"), T("els nombres positius menors que 1;", "los números positivos menores que 1;"),
                 T("els nombres que estan a una distància del 0 menor que 3.", "los números que están a una distancia del 0 menor que 3.")]),
     tasks(3, [R(r"(-3, 2]"), R(r"[0, +\infty)"), R(r"(-\infty, 5)"), R(r"(0, 1)"), R(r"(-3, 3)")])),
 (2, T("Quins nombres enters pertanyen a cada interval?", "¿Qué números enteros pertenecen a cada intervalo?") + tasks(4, [r"$(-3, 2]$", r"$[0, 4)$", r"$(-1, 1)$", r"$\left(-\frac52, \frac72\right)$"]),
     tasks(2, [R(r"-2,\,-1,\,0,\,1,\,2"), R(r"0,\,1,\,2,\,3"), R(r"0"), R(r"-2,\,-1,\,0,\,1,\,2,\,3")])),
 (2, T("Expressa cada situació amb un interval o una semirecta:", "Expresa cada situación con un intervalo o una semirrecta:")
     + tasks(1, [T(r"Un ascensor admet una càrrega $P$ de com a màxim 450 kg.", r"Un ascensor admite una carga $P$ de como máximo 450 kg."),
                 T(r"Per a traure el carnet de conduir cal tindre una edat $e$ d'almenys 18 anys.", r"Para sacarse el carné de conducir hay que tener una edad $e$ de al menos 18 años."),
                 T(r"Un termòstat manté la temperatura $t$ per damunt de 19\,$^\circ$C però per davall de 23\,$^\circ$C.", r"Un termostato mantiene la temperatura $t$ por encima de 19\,$^\circ$C pero por debajo de 23\,$^\circ$C."),
                 T(r"En una prova, aproven les notes $n$ iguals o superiors a 5 (la nota màxima és 10).", r"En una prueba, aprueban las notas $n$ iguales o superiores a 5 (la nota máxima es 10).")]),
     tasks(2, [R(r"P\in[0, 450]"), R(r"e\in[18, +\infty)"), R(r"t\in(19, 23)"), R(r"n\in[5, 10]")])),
]))

# =====================================================================
# 4. Operacions amb intervals
A, B = P('[-2,3]'), P('(1,5)')
r16 = [cup(A, B), cap(A, B)]
ck(r16, [P('[-2,5)'), P('(1,3]')])
A, B, C = P('(-inf,1]'), P('[-3,4)'), P('(2,inf)')
r17 = [cup(A, B), cap(A, B), cap(B, C), cap(A, C), cup(B, C), cup(A, C)]
ck(r17, [P('(-inf,4)'), P('[-3,1]'), P('(2,4)'), [], P('[-3,inf)'), P('(-inf,1]U(2,inf)')])
r18 = [cup(P('[0,4)'), P('[4,7]')), cap(P('[0,4)'), P('[4,7]')), cap(P('(-5,-1]'), P('[-1,2)')), cap(P('(-inf,3)'), P('(-inf,0]')), cap(P('(-2,6)'), P('[1,3]'))]
ck(r18, [P('[0,7]'), [], P('[-1,-1]'), P('(-inf,0]'), P('[1,3]')])
r19 = [cap(P('(-2,inf)'), P('(-inf,5]')), cap(P('[1,inf)'), P('(-inf,1)')), cap(P('(-inf,4]'), P('(-inf,-1]')), cap(P('(0,inf)'), P('[3,inf)'))]
ck(r19, [P('(-2,5]'), [], P('(-inf,-1]'), P('[3,inf)')])
ck([cap(P('[2,8]'), P('[5,12]')), cup(P('[0,12)'), P('(65,inf)'))], [P('[5,8]'), P('[0,12)U(65,inf)')])
A21, B21 = P('(-1,3]'), P('[2,6)')
ck([cap(A21, B21), cup(A21, B21)], [P('[2,3]'), P('(-1,6)')])
def RS(S, lo=None, hi=None): return (R(st(S)) + r'\\[2pt]' + recta(S, lo, hi)) if S else R(r'\varnothing')
S.append((T("Operacions amb intervals", "Operaciones con intervalos"), [
 (1, T(r"Donats $A=[-2, 3]$ i $B=(1, 5)$, representa'ls en la mateixa recta i calcula $A\cup B$ i $A\cap B$.", r"Dados $A=[-2, 3]$ y $B=(1, 5)$, represéntalos en la misma recta y calcula $A\cup B$ y $A\cap B$.")
     + recorda(T(r"La unió $A\cup B$ són els nombres que estan en $A$ \textbf{o} en $B$; la intersecció $A\cap B$, els que estan en $A$ \textbf{i} en $B$ alhora.",
                 r"La unión $A\cup B$ son los números que están en $A$ \textbf{o} en $B$; la intersección $A\cap B$, los que están en $A$ \textbf{y} en $B$ a la vez.")),
     tasks(2, [r"$A\cup B=" + Rm(st(r16[0])) + r"$\\[2pt]" + recta(r16[0], -3, 6), r"$A\cap B=" + Rm(st(r16[1])) + r"$\\[2pt]" + recta(r16[1], -3, 6)])),
 (2, T(r"Siguen $A=(-\infty, 1]$, $B=[-3, 4)$ i $C=(2, +\infty)$. Calcula:", r"Sean $A=(-\infty, 1]$, $B=[-3, 4)$ y $C=(2, +\infty)$. Calcula:")
     + tasks(3, [r"$A\cup B$", r"$A\cap B$", r"$B\cap C$", r"$A\cap C$", r"$B\cup C$", r"$A\cup C$"]),
     tasks(2, [RS(x, -5, 6) for x in r17[:3]] + [R(r"\varnothing") + T(" (no tenen cap nombre en comú)", " (no tienen ningún número en común)")] + [RS(x, -5, 6) for x in r17[4:]])),
 (2, T("Calcula i representa:", "Calcula y representa:") + tasks(3, [r"$[0, 4)\cup[4, 7]$", r"$[0, 4)\cap[4, 7]$", r"$(-5, -1]\cap[-1, 2)$", r"$(-\infty, 3)\cap(-\infty, 0]$", r"$(-2, 6)\cap[1, 3]$"]),
     tasks(2, [RS(r18[0], -1, 8), R(r"\varnothing") + T(" (el 4 no és del primer)", " (el 4 no es del primero)"), R(r"\{-1\}") + T(" (només un nombre)", " (solo un número)"), RS(r18[3], -4, 4), RS(r18[4], -3, 7)])),
 (2, T("Escriu amb un interval o una semirecta els nombres que compleixen alhora les dues condicions:", "Escribe con un intervalo o una semirrecta los números que cumplen a la vez las dos condiciones:")
     + tasks(2, [r"$x>-2$ \ " + T("i", "y") + r" \ $x\le5$", r"$x\ge1$ \ " + T("i", "y") + r" \ $x<1$", r"$x\le4$ \ " + T("i", "y") + r" \ $x\le-1$", r"$x>0$ \ " + T("i", "y") + r" \ $x\ge3$"]),
     tasks(4, [R(st(r19[0])), R(r"\varnothing"), R(st(r19[2])), R(st(r19[3]))])),
 (2, tasks(1, [T(r"Un medicament s'ha de conservar entre 2\,$^\circ$C i 8\,$^\circ$C (tots dos inclosos). La càmera d'un camió manté la temperatura entre 5\,$^\circ$C i 12\,$^\circ$C. Expressa-ho amb intervals. Entre quines temperatures pot estar el medicament dins del camió?",
                 r"Un medicamento se tiene que conservar entre 2\,$^\circ$C y 8\,$^\circ$C (ambos incluidos). La cámara de un camión mantiene la temperatura entre 5\,$^\circ$C y 12\,$^\circ$C. Exprésalo con intervalos. ¿Entre qué temperaturas puede estar el medicamento dentro del camión?"),
                T(r"Un museu fa entrada reduïda als menors de 12 anys i als majors de 65. Expressa amb intervals les edats que tenen entrada reduïda.", r"Un museo hace entrada reducida a los menores de 12 años y a los mayores de 65. Expresa con intervalos las edades que tienen entrada reducida.")]),
     tasks(1, [r"$M=[2, 8]$, \ $C=[5, 12]$, \ $M\cap C=" + Rm(r"[5, 8]") + r"$: " + T(r"entre 5\,$^\circ$C i 8\,$^\circ$C.", r"entre 5\,$^\circ$C y 8\,$^\circ$C."),
               R(r"[0, 12)\cup(65, +\infty)") + T(r" \ (una unió de dos intervals que no es toquen)", r" \ (una unión de dos intervalos que no se tocan)")])),
 (3, T(r"Troba dos intervals $A$ i $B$ tals que $A\cap B=[2, 3]$ i $A\cup B=(-1, 6)$.", r"Halla dos intervalos $A$ y $B$ tales que $A\cap B=[2, 3]$ y $A\cup B=(-1, 6)$."),
     T("Per exemple, ", "Por ejemplo, ") + R(r"A=(-1, 3]") + T(" i ", " y ") + R(r"B=[2, 6)") + r"\\[2pt]" + recta(A21 + [], -2, 7) + r"\quad" + recta(B21, -2, 7)),
]))

# =====================================================================
# 5. Arrels i radicals
chk([('sqrt(81)', 9), ('root(64,3)', 4), ('root(16,4)', 2), ('real_root(-1,5)', -1), ('real_root(-1000,3)', -10), ('sqrt(Rational(49,100))', 'Rational(7,10)'), ('root(Rational(27,8),3)', 'Rational(3,2)')])
for v, a, b in [(30, 5, 6), (50 ** (1 / 3), 3, 4), (math.sqrt(90), 9, 10), (100 ** 0.25, 3, 4), (-(20 ** (1 / 3)), -3, -2)]:
    if v == 30: v = math.sqrt(30)
    assert a < v < b, (v, a, b)
ap = [math.sqrt(7), 20 ** (1 / 3), 50 ** 0.25, -(100 ** 0.2)]
ck([round(x, 2) for x in ap], [2.65, 2.71, 2.66, -2.51])
S.append((T("Arrels i radicals", "Raíces y radicales"), [
 (1, T("Calcula les arrels següents, si existeixen:", "Calcula las raíces siguientes, si existen:")
     + tasks(4, [r"$\sqrt{81}$", r"$\sqrt[3]{64}$", r"$\sqrt[4]{16}$", r"$\sqrt[5]{-1}$", r"$\sqrt[3]{-1000}$", r"$\sqrt{0,49}$", r"$\sqrt[3]{\frac{27}{8}}$", r"$\sqrt[4]{-81}$"])
     + recorda(T(r"$\sqrt[n]{a}=x\iff x^n=a$. Si l'índex és parell i el radicand negatiu, l'arrel no és un nombre real.", r"$\sqrt[n]{a}=x\iff x^n=a$. Si el índice es par y el radicando negativo, la raíz no es un número real.")),
     tasks(4, [R("9"), R("4"), R("2"), R("-1"), R("-10"), R("0,7"), R(r"\frac32"), T("No és real.", "No es real.")])),
 (1, T("Quantes arrels reals té cada radical? Calcula-les:", "¿Cuántas raíces reales tiene cada radical? Calcúlalas:") + tasks(5, [r"$\sqrt{36}$", r"$\sqrt[3]{-125}$", r"$\sqrt[4]{-1}$", r"$\sqrt[6]{64}$", r"$\sqrt[5]{32}$"]),
     tasks(3, [T("Dues: ", "Dos: ") + R(r"\pm6"), T("Una: ", "Una: ") + R("-5"), T("Cap ", "Ninguna ") + r"\ ($\notin\mathbb R$)", T("Dues: ", "Dos: ") + R(r"\pm2"), T("Una: ", "Una: ") + R("2")])),
 (2, T("Sense calculadora, digues entre quins dos nombres enters consecutius està cada arrel:", "Sin calculadora, di entre qué dos números enteros consecutivos está cada raíz:")
     + tasks(5, [r"$\sqrt{30}$", r"$\sqrt[3]{50}$", r"$\sqrt{90}$", r"$\sqrt[4]{100}$", r"$\sqrt[3]{-20}$"]),
     tasks(2, [r"$25<30<36$: \ " + R(r"5<\sqrt{30}<6"), r"$27<50<64$: \ " + R(r"3<\sqrt[3]{50}<4"), r"$81<90<100$: \ " + R(r"9<\sqrt{90}<10"),
               r"$81<100<256$: \ " + R(r"3<\sqrt[4]{100}<4"), r"$-27<-20<-8$: \ " + R(r"-3<\sqrt[3]{-20}<-2")])),
 (1, T("Amb la calculadora, aproxima a les centèsimes:", "Con la calculadora, aproxima a las centésimas:") + tasks(4, [r"$\sqrt7$", r"$\sqrt[3]{20}$", r"$\sqrt[4]{50}$", r"$\sqrt[5]{-100}$"]),
     tasks(4, [R(r"2,65"), R(r"2,71"), R(r"2,66"), R(r"-2,51")])),
]))

# =====================================================================
# 6. Radicals i potències d'exponent fraccionari
chk([('sqrt(8)', '2**Rational(3,2)'), ('root(9,3)', '3**Rational(2,3)'), ('1/sqrt(5)', '5**Rational(-1,2)'), ('1/root(4,3)', '2**Rational(-2,3)'), ('root(27,4)', '3**Rational(3,4)'), ('sqrt(Rational(1,2))', '2**Rational(-1,2)')])
p29 = ['9**Rational(1,2)', '8**Rational(1,3)', '16**Rational(3,4)', '27**Rational(2,3)', '32**Rational(2,5)', '4**Rational(-1,2)', '125**Rational(-2,3)', '100**Rational(3,2)']
chk(zip(p29, [3, 2, 8, 9, 4, 'Rational(1,2)', 'Rational(1,25)', 1000]))
chk([('2**Rational(1,2)*2**Rational(1,3)', 'root(32,6)'), ('3**Rational(3,4)/3**Rational(1,2)', 'root(3,4)'), ('(5**Rational(2,3))**Rational(3,4)', 'sqrt(5)'), ('sqrt(3)*root(3,3)', 'root(243,6)'),
     ('root(a**2,3)*sqrt(a)', 'a*root(a,6)'), ('sqrt(x)/root(x,4)', 'root(x,4)')])
S.append((T("Radicals i potències d'exponent fraccionari", "Radicales y potencias de exponente fraccionario"), [
 (1, T("Escriu en forma de potència:", "Escribe en forma de potencia:") + tasks(6, [r"$\sqrt3$", r"$\sqrt[3]{5^2}$", r"$\sqrt[4]{x^3}$", r"$\sqrt[5]2$", r"$\sqrt{a^5}$", r"$\sqrt[3]7$"])
     + recorda(r"$\sqrt[n]{a^m}=a^{\frac mn}$: " + T("l'exponent del radicand va al numerador i l'índex, al denominador.", "el exponente del radicando va al numerador y el índice, al denominador.")),
     tasks(6, [R(r"3^{\frac12}"), R(r"5^{\frac23}"), R(r"x^{\frac34}"), R(r"2^{\frac15}"), R(r"a^{\frac52}"), R(r"7^{\frac13}")])),
 (1, T("Escriu en forma de radical:", "Escribe en forma de radical:") + tasks(6, [r"$5^{\frac12}$", r"$2^{\frac34}$", r"$3^{\frac25}$", r"$a^{\frac53}$", r"$10^{\frac13}$", r"$x^{\frac72}$"]),
     tasks(6, [R(r"\sqrt5"), R(r"\sqrt[4]{2^3}"), R(r"\sqrt[5]{3^2}"), R(r"\sqrt[3]{a^5}"), R(r"\sqrt[3]{10}"), R(r"\sqrt{x^7}")])),
 (2, T("Escriu com una potència d'un nombre primer:", "Escribe como una potencia de un número primo:") + tasks(6, [r"$\sqrt8$", r"$\sqrt[3]9$", r"$\dfrac{1}{\sqrt5}$", r"$\dfrac{1}{\sqrt[3]4}$", r"$\sqrt[4]{27}$", r"$\sqrt{\dfrac12}$"]),
     tasks(3, [r"$\sqrt{2^3}=" + Rm(r"2^{\frac32}") + "$", r"$\sqrt[3]{3^2}=" + Rm(r"3^{\frac23}") + "$", R(r"5^{-\frac12}"), r"$\dfrac{1}{2^{\frac23}}=" + Rm(r"2^{-\frac23}") + "$", r"$\sqrt[4]{3^3}=" + Rm(r"3^{\frac34}") + "$", R(r"2^{-\frac12}")])),
 (2, T("Calcula sense calculadora:", "Calcula sin calculadora:") + tasks(4, [r"$9^{\frac12}$", r"$8^{\frac13}$", r"$16^{\frac34}$", r"$27^{\frac23}$", r"$32^{\frac25}$", r"$4^{-\frac12}$", r"$125^{-\frac23}$", r"$100^{\frac32}$"])
     + recorda(T(r"Escriu la base com a potència: $16^{\frac34}=\left(2^4\right)^{\frac34}=2^3$.", r"Escribe la base como potencia: $16^{\frac34}=\left(2^4\right)^{\frac34}=2^3$.")),
     tasks(4, [R("3"), R("2"), r"$2^3=" + Rm("8") + "$", r"$3^2=" + Rm("9") + "$", r"$2^2=" + Rm("4") + "$", R(r"\frac12"), r"$5^{-2}=" + Rm(r"\frac1{25}") + "$", r"$10^3=" + Rm("1000") + "$"])),
 (3, T("Expressa com una sola potència i després com un radical:", "Expresa como una sola potencia y después como un radical:")
     + tasks(3, [r"$2^{\frac12}\cdot2^{\frac13}$", r"$3^{\frac34}:3^{\frac12}$", r"$\left(5^{\frac23}\right)^{\frac34}$", r"$\sqrt3\cdot\sqrt[3]3$", r"$\sqrt[3]{a^2}\cdot\sqrt a$", r"$\dfrac{\sqrt x}{\sqrt[4]x}$"])
     + recorda(r"$a^p\cdot a^q=a^{p+q}$, \ $a^p:a^q=a^{p-q}$, \ $\left(a^p\right)^q=a^{p\cdot q}$."),
     tasks(2, [r"$2^{\frac56}=" + Rm(r"\sqrt[6]{32}") + "$", r"$3^{\frac14}=" + Rm(r"\sqrt[4]3") + "$", r"$5^{\frac12}=" + Rm(r"\sqrt5") + "$", r"$3^{\frac12+\frac13}=3^{\frac56}=" + Rm(r"\sqrt[6]{243}") + "$",
               r"$a^{\frac23+\frac12}=a^{\frac76}=" + Rm(r"a\sqrt[6]a") + "$", r"$x^{\frac12-\frac14}=x^{\frac14}=" + Rm(r"\sqrt[4]x") + "$"])),
]))

# =====================================================================
# 7. Radicals equivalents
chk([('sqrt(3)', 'root(9,4)'), ('root(25,6)', 'root(5,3)'), ('root(a**3,4)', 'root(a**6,8)')]); assert abs(2 ** (1 / 3) - 8 ** (1 / 6)) > 0.01
s33 = [('root(9,4)', 'sqrt(3)'), ('root(8,6)', 'sqrt(2)'), ('root(16,8)', 'sqrt(2)'), ('root(27,9)', 'root(3,3)'), ('root(32,10)', 'sqrt(2)'), ('root(a**4,6)', 'root(a**2,3)'), ('root(x**9,12)', 'root(x**3,4)'), ('root(a**2*b**4,6)', 'root(a*b**2,3)')]
chk(s33)
chk([('sqrt(2)', 'root(8,6)'), ('root(3,3)', 'root(9,6)'), ('sqrt(5)', 'root(25,4)'), ('root(2,3)', 'root(16,12)'), ('root(5,4)', 'root(125,12)'), ('root(3,6)', 'root(9,12)')])
o1 = {'a': math.sqrt(2), 'b': 3 ** (1 / 3), 'c': 6 ** (1 / 6)}; o2 = {'a': 4 ** (1 / 3), 'b': math.sqrt(3), 'c': 5 ** 0.25}
ck([sorted(o1, key=o1.get), sorted(o2, key=o2.get)], [['c', 'a', 'b'], ['c', 'a', 'b']])
S.append((T("Radicals equivalents", "Radicales equivalentes"), [
 (1, T("Escriu tres radicals equivalents a cadascun d'aquests:", "Escribe tres radicales equivalentes a cada uno de estos:") + tasks(3, [r"$\sqrt2$", r"$\sqrt[3]5$", r"$\sqrt[5]{a^2}$"])
     + recorda(r"$\sqrt[n]{a^m}=\sqrt[n\cdot p]{a^{m\cdot p}}$: " + T("multipliquem l'índex i l'exponent pel mateix nombre.", "multiplicamos el índice y el exponente por el mismo número.")),
     T("Per exemple:", "Por ejemplo:") + tasks(1, [R(r"\sqrt[4]{2^2}=\sqrt[6]{2^3}=\sqrt[8]{2^4}"), R(r"\sqrt[6]{5^2}=\sqrt[9]{5^3}=\sqrt[12]{5^4}"), R(r"\sqrt[10]{a^4}=\sqrt[15]{a^6}=\sqrt[20]{a^8}")])),
 (1, T("Digues si són equivalents els radicals de cada parella. Justifica-ho passant-los a potència:", "Di si son equivalentes los radicales de cada pareja. Justifícalo pasándolos a potencia:")
     + tasks(2, [r"$\sqrt3$ \ " + T("i", "y") + r" \ $\sqrt[4]9$", r"$\sqrt[3]2$ \ " + T("i", "y") + r" \ $\sqrt[6]8$", r"$\sqrt[6]{25}$ \ " + T("i", "y") + r" \ $\sqrt[3]5$", r"$\sqrt[4]{a^3}$ \ " + T("i", "y") + r" \ $\sqrt[8]{a^6}$"]),
     tasks(2, [r"$3^{\frac12}=3^{\frac24}$: " + R(T(r"\text{sí}", r"\text{sí}")), r"$2^{\frac13}\ne2^{\frac36}=2^{\frac12}$: " + R(r"\text{no}"), r"$5^{\frac26}=5^{\frac13}$: " + R(T(r"\text{sí}", r"\text{sí}")), r"$a^{\frac34}=a^{\frac68}$: " + R(T(r"\text{sí}", r"\text{sí}"))])),
 (2, T("Simplifica els radicals següents:", "Simplifica los radicales siguientes:") + tasks(4, [r"$\sqrt[4]9$", r"$\sqrt[6]8$", r"$\sqrt[8]{16}$", r"$\sqrt[9]{27}$", r"$\sqrt[10]{32}$", r"$\sqrt[6]{a^4}$", r"$\sqrt[12]{x^9}$", r"$\sqrt[6]{a^2b^4}$"])
     + recorda(T("Descompon el radicand i divideix l'índex i els exponents pel seu m.c.d.", "Descompón el radicando y divide el índice y los exponentes por su m.c.d.")),
     tasks(4, [r"$\sqrt[4]{3^2}=" + Rm(r"\sqrt3") + "$", r"$\sqrt[6]{2^3}=" + Rm(r"\sqrt2") + "$", r"$\sqrt[8]{2^4}=" + Rm(r"\sqrt2") + "$", r"$\sqrt[9]{3^3}=" + Rm(r"\sqrt[3]3") + "$",
               r"$\sqrt[10]{2^5}=" + Rm(r"\sqrt2") + "$", R(r"\sqrt[3]{a^2}"), R(r"\sqrt[4]{x^3}"), R(r"\sqrt[3]{ab^2}")])),
 (2, T("Redueix a índex comú:", "Reduce a índice común:") + tasks(3, [r"$\sqrt2$ \ " + T("i", "y") + r" \ $\sqrt[3]3$", r"$\sqrt5$ \ " + T("i", "y") + r" \ $\sqrt[4]3$", r"$\sqrt[3]2$, \ $\sqrt[4]5$ \ " + T("i", "y") + r" \ $\sqrt[6]3$"]),
     tasks(3, [R(r"\sqrt[6]8,\ \sqrt[6]9"), R(r"\sqrt[4]{25},\ \sqrt[4]3"), R(r"\sqrt[12]{16},\ \sqrt[12]{125},\ \sqrt[12]{9}")])),
 (3, T("Ordena de menor a major, reduint primer a índex comú:", "Ordena de menor a mayor, reduciendo primero a índice común:") + tasks(2, [r"$\sqrt2$, \ $\sqrt[3]3$, \ $\sqrt[6]6$", r"$\sqrt[3]4$, \ $\sqrt3$, \ $\sqrt[4]5$"]),
     tasks(1, [r"$\sqrt[6]8$, \ $\sqrt[6]9$, \ $\sqrt[6]6$: \ " + R(r"\sqrt[6]6<\sqrt2<\sqrt[3]3"), r"$\sqrt[12]{256}$, \ $\sqrt[12]{729}$, \ $\sqrt[12]{125}$: \ " + R(r"\sqrt[4]5<\sqrt[3]4<\sqrt3")])),
]))

# =====================================================================
# 8. Extracció i introducció de factors
e36 = [('sqrt(12)', '2*sqrt(3)'), ('sqrt(18)', '3*sqrt(2)'), ('sqrt(50)', '5*sqrt(2)'), ('sqrt(75)', '5*sqrt(3)'), ('sqrt(98)', '7*sqrt(2)'), ('sqrt(200)', '10*sqrt(2)'),
       ('root(16,3)', '2*root(2,3)'), ('root(54,3)', '3*root(2,3)'), ('root(81,3)', '3*root(3,3)'), ('root(250,3)', '5*root(2,3)')]
chk(e36)
chk([('sqrt(a**3)', 'a*sqrt(a)'), ('sqrt(8*x**5)', '2*x**2*sqrt(2*x)'), ('root(a**4*b**6,3)', 'a*b**2*root(a,3)'), ('sqrt(72*a**2*b**3)', '6*a*b*sqrt(2*b)'), ('root(24*x**7,3)', '2*x**2*root(3*x,3)'), ('root(32*a**9,4)', '2*a**2*root(2*a,4)')])
chk([('2*sqrt(3)', 'sqrt(12)'), ('3*sqrt(2)', 'sqrt(18)'), ('5*sqrt(5)', 'sqrt(125)'), ('2*root(5,3)', 'root(40,3)'), ('3*root(2,3)', 'root(54,3)'), ('a*sqrt(a)', 'sqrt(a**3)'), ('2*x*sqrt(x)', 'sqrt(4*x**3)')])
assert 5 * math.sqrt(3) > 3 * math.sqrt(5) and 3 * 2 ** (1 / 3) > 2 * 3 ** (1 / 3)
chk([('sqrt(Rational(18,25))', '3*sqrt(2)/5'), ('sqrt(Rational(12,49))', '2*sqrt(3)/7'), ('root(Rational(16,27),3)', '2*root(2,3)/3'), ('sqrt(Rational(75,4))', '5*sqrt(3)/2')])
S.append((T("Extracció i introducció de factors", "Extracción e introducción de factores"), [
 (1, T("Extrau tots els factors possibles:", "Extrae todos los factores posibles:") + tasks(5, [r"$\sqrt{12}$", r"$\sqrt{18}$", r"$\sqrt{50}$", r"$\sqrt{75}$", r"$\sqrt{98}$", r"$\sqrt{200}$", r"$\sqrt[3]{16}$", r"$\sqrt[3]{54}$", r"$\sqrt[3]{81}$", r"$\sqrt[3]{250}$"])
     + recorda(T(r"Descompon el radicand en factors primers. Ix fora cada factor que tinga exponent igual o més gran que l'índex: $\sqrt{72}=\sqrt{2^3\cdot3^2}=2\cdot3\sqrt2=6\sqrt2$.",
                 r"Descompón el radicando en factores primos. Sale fuera cada factor que tenga exponente igual o mayor que el índice: $\sqrt{72}=\sqrt{2^3\cdot3^2}=2\cdot3\sqrt2=6\sqrt2$.")),
     tasks(5, [R(r"2\sqrt3"), R(r"3\sqrt2"), R(r"5\sqrt2"), R(r"5\sqrt3"), R(r"7\sqrt2"), R(r"10\sqrt2"), R(r"2\sqrt[3]2"), R(r"3\sqrt[3]2"), R(r"3\sqrt[3]3"), R(r"5\sqrt[3]2")])),
 (2, T("Extrau tots els factors possibles (les lletres representen nombres positius):", "Extrae todos los factores posibles (las letras representan números positivos):")
     + tasks(3, [r"$\sqrt{a^3}$", r"$\sqrt{8x^5}$", r"$\sqrt[3]{a^4b^6}$", r"$\sqrt{72a^2b^3}$", r"$\sqrt[3]{24x^7}$", r"$\sqrt[4]{32a^9}$"]),
     tasks(3, [R(r"a\sqrt a"), R(r"2x^2\sqrt{2x}"), R(r"ab^2\sqrt[3]a"), R(r"6ab\sqrt{2b}"), R(r"2x^2\sqrt[3]{3x}"), R(r"2a^2\sqrt[4]{2a}")])),
 (1, T("Introdueix els factors dins del radical:", "Introduce los factores dentro del radical:") + tasks(4, [r"$2\sqrt3$", r"$3\sqrt2$", r"$5\sqrt5$", r"$2\sqrt[3]5$", r"$3\sqrt[3]2$", r"$a\sqrt a$", r"$2x\sqrt x$"])
     + recorda(T(r"El factor entra elevat a l'índex: $a\sqrt[n]{b}=\sqrt[n]{a^n\cdot b}$.", r"El factor entra elevado al índice: $a\sqrt[n]{b}=\sqrt[n]{a^n\cdot b}$.")),
     tasks(4, [R(r"\sqrt{12}"), R(r"\sqrt{18}"), R(r"\sqrt{125}"), R(r"\sqrt[3]{40}"), R(r"\sqrt[3]{54}"), R(r"\sqrt{a^3}"), R(r"\sqrt{4x^3}")])),
 (2, T("Introdueix els factors i digues quin nombre és més gran en cada parella:", "Introduce los factores y di qué número es mayor en cada pareja:")
     + tasks(2, [r"$3\sqrt5$ \ " + T("o", "o") + r" \ $5\sqrt3$", r"$2\sqrt[3]3$ \ " + T("o", "o") + r" \ $3\sqrt[3]2$"]),
     tasks(2, [r"$\sqrt{45}<\sqrt{75}$: \ " + R(r"5\sqrt3"), r"$\sqrt[3]{24}<\sqrt[3]{54}$: \ " + R(r"3\sqrt[3]2")])),
 (3, T("Extrau factors (fes l'arrel del numerador i la del denominador):", "Extrae factores (haz la raíz del numerador y la del denominador):") + tasks(4, [r"$\sqrt{\dfrac{18}{25}}$", r"$\sqrt{\dfrac{12}{49}}$", r"$\sqrt[3]{\dfrac{16}{27}}$", r"$\sqrt{\dfrac{75}{4}}$"]),
     tasks(4, [R(r"\dfrac{3\sqrt2}{5}"), R(r"\dfrac{2\sqrt3}{7}"), R(r"\dfrac{2\sqrt[3]2}{3}"), R(r"\dfrac{5\sqrt3}{2}")])),
]))

# =====================================================================
# 9. Operacions amb radicals
chk([('3*sqrt(2)+5*sqrt(2)-sqrt(2)', '7*sqrt(2)'), ('4*root(5,3)-7*root(5,3)', '-3*root(5,3)'), ('2*sqrt(3)+sqrt(3)-6*sqrt(3)', '-3*sqrt(3)'), ('sqrt(7)+3*sqrt(5)-4*sqrt(7)+sqrt(5)', '-3*sqrt(7)+4*sqrt(5)')])
s42 = [('sqrt(8)+sqrt(18)', '5*sqrt(2)'), ('sqrt(12)+sqrt(27)-sqrt(3)', '4*sqrt(3)'), ('sqrt(50)-sqrt(32)+sqrt(2)', '2*sqrt(2)'), ('2*sqrt(45)-sqrt(20)+sqrt(5)', '5*sqrt(5)'),
       ('3*sqrt(12)-2*sqrt(27)+sqrt(75)', '5*sqrt(3)'), ('root(16,3)+root(54,3)-root(2,3)', '4*root(2,3)'), ('sqrt(20)+sqrt(45)-sqrt(80)', 'sqrt(5)'), ('5*sqrt(8)-2*sqrt(18)+sqrt(72)', '10*sqrt(2)')]
chk(s42)
s43 = [('sqrt(2)*sqrt(8)', 4), ('sqrt(3)*sqrt(12)', 6), ('sqrt(5)*sqrt(10)', '5*sqrt(2)'), ('2*sqrt(3)*4*sqrt(6)', '24*sqrt(2)'), ('root(4,3)*root(2,3)', 2), ('root(9,3)*root(3,3)', 3),
       ('sqrt(50)/sqrt(2)', 5), ('sqrt(72)/sqrt(8)', 3), ('root(48,3)/root(6,3)', 2), ('6*sqrt(15)/(3*sqrt(5))', '2*sqrt(3)')]
chk(s43)
chk([('sqrt(3)**2', 3), ('sqrt(5)**4', 25), ('(2*sqrt(3))**2', 12), ('root(2,3)**6', 4), ('root(4,3)**2', '2*root(2,3)'), ('sqrt(sqrt(3))', 'root(3,4)'), ('root(sqrt(5),3)', 'root(5,6)'), ('sqrt(root(sqrt(2),3))', 'root(2,12)')])
chk([('sqrt(2)*root(2,3)', 'root(32,6)'), ('sqrt(3)*root(2,3)', 'root(108,6)'), ('root(5,3)*sqrt(5)', 'root(3125,6)'), ('sqrt(2)/root(2,3)', 'root(2,6)'), ('root(9,3)/sqrt(3)', 'root(3,6)')])
chk([('sqrt(2)*(sqrt(2)+sqrt(8))', 6), ('sqrt(3)*(2*sqrt(3)-sqrt(12))', 0), ('(sqrt(5)+1)*(sqrt(5)+2)', '7+3*sqrt(5)'), ('(2*sqrt(3)+1)*(sqrt(3)-2)', '4-3*sqrt(3)')])
chk([('(sqrt(3)+1)**2', '4+2*sqrt(3)'), ('(sqrt(5)-sqrt(2))**2', '7-2*sqrt(10)'), ('(sqrt(7)+2)*(sqrt(7)-2)', 3), ('(3*sqrt(2)-1)**2', '19-6*sqrt(2)'), ('(2*sqrt(5)+3)*(2*sqrt(5)-3)', 11), ('(1+sqrt(2))**2-(1-sqrt(2))**2', '4*sqrt(2)')])
S.append((T("Operacions amb radicals", "Operaciones con radicales"), [
 (1, T("Opera els radicals semblants:", "Opera los radicales semejantes:") + tasks(2, [r"$3\sqrt2+5\sqrt2-\sqrt2$", r"$4\sqrt[3]5-7\sqrt[3]5$", r"$2\sqrt3+\sqrt3-6\sqrt3$", r"$\sqrt7+3\sqrt5-4\sqrt7+\sqrt5$"])
     + recorda(T(r"Només es poden sumar o restar radicals semblants (mateix índex i mateix radicand): se sumen els coeficients. $\sqrt2+\sqrt3$ no es pot ajuntar.",
                 r"Solo se pueden sumar o restar radicales semejantes (mismo índice y mismo radicando): se suman los coeficientes. $\sqrt2+\sqrt3$ no se puede juntar.")),
     tasks(4, [R(r"7\sqrt2"), R(r"-3\sqrt[3]5"), R(r"-3\sqrt3"), R(r"-3\sqrt7+4\sqrt5")])),
 (2, T("Extrau factors i opera:", "Extrae factores y opera:") + tasks(2, [r"$\sqrt8+\sqrt{18}$", r"$\sqrt{12}+\sqrt{27}-\sqrt3$", r"$\sqrt{50}-\sqrt{32}+\sqrt2$", r"$2\sqrt{45}-\sqrt{20}+\sqrt5$",
                                                                       r"$3\sqrt{12}-2\sqrt{27}+\sqrt{75}$", r"$\sqrt[3]{16}+\sqrt[3]{54}-\sqrt[3]2$", r"$\sqrt{20}+\sqrt{45}-\sqrt{80}$", r"$5\sqrt8-2\sqrt{18}+\sqrt{72}$"]),
     tasks(2, [r"$2\sqrt2+3\sqrt2=" + Rm(r"5\sqrt2") + "$", r"$2\sqrt3+3\sqrt3-\sqrt3=" + Rm(r"4\sqrt3") + "$", r"$5\sqrt2-4\sqrt2+\sqrt2=" + Rm(r"2\sqrt2") + "$", r"$6\sqrt5-2\sqrt5+\sqrt5=" + Rm(r"5\sqrt5") + "$",
               r"$6\sqrt3-6\sqrt3+5\sqrt3=" + Rm(r"5\sqrt3") + "$", r"$2\sqrt[3]2+3\sqrt[3]2-\sqrt[3]2=" + Rm(r"4\sqrt[3]2") + "$", r"$2\sqrt5+3\sqrt5-4\sqrt5=" + Rm(r"\sqrt5") + "$", r"$10\sqrt2-6\sqrt2+6\sqrt2=" + Rm(r"10\sqrt2") + "$"])),
 (1, T("Multiplica o divideix i simplifica el resultat:", "Multiplica o divide y simplifica el resultado:") + tasks(5, [r"$\sqrt2\cdot\sqrt8$", r"$\sqrt3\cdot\sqrt{12}$", r"$\sqrt5\cdot\sqrt{10}$", r"$2\sqrt3\cdot4\sqrt6$", r"$\sqrt[3]4\cdot\sqrt[3]2$",
                                                                                                                    r"$\sqrt[3]9\cdot\sqrt[3]3$", r"$\dfrac{\sqrt{50}}{\sqrt2}$", r"$\dfrac{\sqrt{72}}{\sqrt8}$", r"$\dfrac{\sqrt[3]{48}}{\sqrt[3]6}$", r"$\dfrac{6\sqrt{15}}{3\sqrt5}$"])
     + recorda(r"$\sqrt[n]a\cdot\sqrt[n]b=\sqrt[n]{a\cdot b}$ \quad " + T("i", "y") + r" \quad $\sqrt[n]a:\sqrt[n]b=\sqrt[n]{a:b}$ \quad (" + T("mateix índex", "mismo índice") + ")."),
     tasks(5, [r"$\sqrt{16}=" + Rm("4") + "$", r"$\sqrt{36}=" + Rm("6") + "$", r"$\sqrt{50}=" + Rm(r"5\sqrt2") + "$", r"$8\sqrt{18}=" + Rm(r"24\sqrt2") + "$", r"$\sqrt[3]8=" + Rm("2") + "$",
               r"$\sqrt[3]{27}=" + Rm("3") + "$", r"$\sqrt{25}=" + Rm("5") + "$", r"$\sqrt9=" + Rm("3") + "$", r"$\sqrt[3]8=" + Rm("2") + "$", R(r"2\sqrt3")])),
 (2, T("Calcula les potències i escriu com un sol radical les arrels d'arrels:", "Calcula las potencias y escribe como un solo radical las raíces de raíces:")
     + tasks(4, [r"$\left(\sqrt3\right)^2$", r"$\left(\sqrt5\right)^4$", r"$\left(2\sqrt3\right)^2$", r"$\left(\sqrt[3]2\right)^6$", r"$\left(\sqrt[3]4\right)^2$", r"$\sqrt{\sqrt3}$", r"$\sqrt[3]{\sqrt5}$", r"$\sqrt{\sqrt[3]{\sqrt2}}$"])
     + recorda(r"$\left(\sqrt[n]a\right)^p=\sqrt[n]{a^p}$ \quad " + T("i", "y") + r" \quad $\sqrt[m]{\sqrt[n]a}=\sqrt[m\cdot n]a$."),
     tasks(4, [R("3"), R("25"), r"$4\cdot3=" + Rm("12") + "$", r"$2^2=" + Rm("4") + "$", r"$\sqrt[3]{16}=" + Rm(r"2\sqrt[3]2") + "$", R(r"\sqrt[4]3"), R(r"\sqrt[6]5"), R(r"\sqrt[12]2")])),
 (2, T("Escriu com un sol radical (redueix primer a índex comú o passa a potència):", "Escribe como un solo radical (reduce primero a índice común o pasa a potencia):")
     + tasks(5, [r"$\sqrt2\cdot\sqrt[3]2$", r"$\sqrt3\cdot\sqrt[3]2$", r"$\sqrt[3]5\cdot\sqrt5$", r"$\dfrac{\sqrt2}{\sqrt[3]2}$", r"$\dfrac{\sqrt[3]9}{\sqrt3}$"]),
     tasks(3, [r"$\sqrt[6]{2^3\cdot2^2}=" + Rm(r"\sqrt[6]{32}") + "$", r"$\sqrt[6]{3^3\cdot2^2}=" + Rm(r"\sqrt[6]{108}") + "$", r"$\sqrt[6]{5^2\cdot5^3}=" + Rm(r"\sqrt[6]{3125}") + "$",
               r"$2^{\frac12-\frac13}=" + Rm(r"\sqrt[6]2") + "$", r"$3^{\frac23-\frac12}=" + Rm(r"\sqrt[6]3") + "$"])),
 (2, T("Aplica la propietat distributiva i simplifica:", "Aplica la propiedad distributiva y simplifica:") + tasks(2, [r"$\sqrt2\left(\sqrt2+\sqrt8\right)$", r"$\sqrt3\left(2\sqrt3-\sqrt{12}\right)$", r"$\left(\sqrt5+1\right)\left(\sqrt5+2\right)$", r"$\left(2\sqrt3+1\right)\left(\sqrt3-2\right)$"]),
     tasks(2, [r"$2+4=" + Rm("6") + "$", r"$6-6=" + Rm("0") + "$", r"$5+2\sqrt5+\sqrt5+2=" + Rm(r"7+3\sqrt5") + "$", r"$6-4\sqrt3+\sqrt3-2=" + Rm(r"4-3\sqrt3") + "$"])),
 (3, T("Desenvolupa amb les identitats notables:", "Desarrolla con las identidades notables:") + tasks(2, [r"$\left(\sqrt3+1\right)^2$", r"$\left(\sqrt5-\sqrt2\right)^2$", r"$\left(\sqrt7+2\right)\left(\sqrt7-2\right)$", r"$\left(3\sqrt2-1\right)^2$",
                                                                                                         r"$\left(2\sqrt5+3\right)\left(2\sqrt5-3\right)$", r"$\left(1+\sqrt2\right)^2-\left(1-\sqrt2\right)^2$"])
     + recorda(r"$(a+b)^2=a^2+2ab+b^2$, \ $(a-b)^2=a^2-2ab+b^2$, \ $(a+b)(a-b)=a^2-b^2$."),
     tasks(2, [r"$3+2\sqrt3+1=" + Rm(r"4+2\sqrt3") + "$", r"$5-2\sqrt{10}+2=" + Rm(r"7-2\sqrt{10}") + "$", r"$7-4=" + Rm("3") + "$", r"$18-6\sqrt2+1=" + Rm(r"19-6\sqrt2") + "$",
               r"$20-9=" + Rm("11") + "$", r"$\left(3+2\sqrt2\right)-\left(3-2\sqrt2\right)=" + Rm(r"4\sqrt2") + "$"])),
]))

# =====================================================================
# 10. Racionalització
chk([('1/sqrt(2)', 'sqrt(2)/2'), ('3/sqrt(3)', 'sqrt(3)'), ('6/sqrt(2)', '3*sqrt(2)'), ('5/sqrt(10)', 'sqrt(10)/2'), ('2/(3*sqrt(5))', '2*sqrt(5)/15'), ('sqrt(2)/sqrt(6)', 'sqrt(3)/3')])
chk([('1/root(2,3)', 'root(4,3)/2'), ('6/root(3,3)', '2*root(9,3)'), ('4/root(4,3)', '2*root(2,3)'), ('10/root(25,3)', '2*root(5,3)'), ('1/root(2,4)', 'root(8,4)/2'), ('3/root(27,4)', 'root(3,4)')])
chk([('1/(sqrt(2)+1)', 'sqrt(2)-1'), ('2/(sqrt(3)-1)', 'sqrt(3)+1'), ('3/(2+sqrt(3))', '6-3*sqrt(3)'), ('4/(sqrt(5)+sqrt(3))', '2*sqrt(5)-2*sqrt(3)'), ('sqrt(2)/(sqrt(2)-1)', '2+sqrt(2)'), ('6/(3-sqrt(3))', '3+sqrt(3)'),
     ('(sqrt(3)+1)/(sqrt(3)-1)', '2+sqrt(3)'), ('1/(2*sqrt(2)-sqrt(3))', '(2*sqrt(2)+sqrt(3))/5')])
chk([('1/sqrt(2)+1/sqrt(8)', '3*sqrt(2)/4'), ('2/sqrt(3)-sqrt(3)', '-sqrt(3)/3'), ('1/(sqrt(2)-1)-1/(sqrt(2)+1)', 2), ('sqrt(12)/(sqrt(3)+1)', '3-sqrt(3)')])
S.append((T("Racionalització", "Racionalización"), [
 (1, T("Racionalitza i simplifica:", "Racionaliza y simplifica:") + tasks(6, [r"$\dfrac{1}{\sqrt2}$", r"$\dfrac{3}{\sqrt3}$", r"$\dfrac{6}{\sqrt2}$", r"$\dfrac{5}{\sqrt{10}}$", r"$\dfrac{2}{3\sqrt5}$", r"$\dfrac{\sqrt2}{\sqrt6}$"])
     + recorda(T(r"Si al denominador hi ha $\sqrt b$, multiplica el numerador i el denominador per $\sqrt b$: $\ \dfrac{6}{\sqrt3}=\dfrac{6\sqrt3}{3}=2\sqrt3$.", r"Si en el denominador hay $\sqrt b$, multiplica el numerador y el denominador por $\sqrt b$: $\ \dfrac{6}{\sqrt3}=\dfrac{6\sqrt3}{3}=2\sqrt3$.")),
     tasks(6, [R(r"\dfrac{\sqrt2}{2}"), R(r"\sqrt3"), R(r"3\sqrt2"), R(r"\dfrac{\sqrt{10}}{2}"), R(r"\dfrac{2\sqrt5}{15}"), R(r"\dfrac{\sqrt3}{3}")])),
 (2, T("Racionalitza i simplifica:", "Racionaliza y simplifica:") + tasks(6, [r"$\dfrac{1}{\sqrt[3]2}$", r"$\dfrac{6}{\sqrt[3]3}$", r"$\dfrac{4}{\sqrt[3]4}$", r"$\dfrac{10}{\sqrt[3]{25}}$", r"$\dfrac{1}{\sqrt[4]2}$", r"$\dfrac{3}{\sqrt[4]{27}}$"])
     + recorda(T(r"Amb $\sqrt[n]{b^m}$ al denominador, multiplica per $\sqrt[n]{b^{n-m}}$, perquè $\sqrt[n]{b^m}\cdot\sqrt[n]{b^{n-m}}=\sqrt[n]{b^n}=b$.", r"Con $\sqrt[n]{b^m}$ en el denominador, multiplica por $\sqrt[n]{b^{n-m}}$, porque $\sqrt[n]{b^m}\cdot\sqrt[n]{b^{n-m}}=\sqrt[n]{b^n}=b$.")),
     tasks(3, [R(r"\dfrac{\sqrt[3]4}{2}"), r"$\dfrac{6\sqrt[3]9}{3}=" + Rm(r"2\sqrt[3]9") + "$", r"$\dfrac{4\sqrt[3]2}{2}=" + Rm(r"2\sqrt[3]2") + "$", r"$\dfrac{10\sqrt[3]5}{5}=" + Rm(r"2\sqrt[3]5") + "$",
               R(r"\dfrac{\sqrt[4]8}{2}"), r"$\dfrac{3\sqrt[4]3}{3}=" + Rm(r"\sqrt[4]3") + "$"])),
 (2, T("Racionalitza multiplicant pel conjugat:", "Racionaliza multiplicando por el conjugado:") + tasks(4, [r"$\dfrac{1}{\sqrt2+1}$", r"$\dfrac{2}{\sqrt3-1}$", r"$\dfrac{3}{2+\sqrt3}$", r"$\dfrac{4}{\sqrt5+\sqrt3}$",
                                                                                                          r"$\dfrac{\sqrt2}{\sqrt2-1}$", r"$\dfrac{6}{3-\sqrt3}$", r"$\dfrac{\sqrt3+1}{\sqrt3-1}$", r"$\dfrac{1}{2\sqrt2-\sqrt3}$"])
     + recorda(T(r"El conjugat de $a+\sqrt b$ és $a-\sqrt b$, i $\left(a+\sqrt b\right)\left(a-\sqrt b\right)=a^2-b$.", r"El conjugado de $a+\sqrt b$ es $a-\sqrt b$, y $\left(a+\sqrt b\right)\left(a-\sqrt b\right)=a^2-b$.")),
     tasks(2, [r"$\dfrac{\sqrt2-1}{2-1}=" + Rm(r"\sqrt2-1") + "$", r"$\dfrac{2\left(\sqrt3+1\right)}{3-1}=" + Rm(r"\sqrt3+1") + "$", r"$\dfrac{3\left(2-\sqrt3\right)}{4-3}=" + Rm(r"6-3\sqrt3") + "$",
               r"$\dfrac{4\left(\sqrt5-\sqrt3\right)}{5-3}=" + Rm(r"2\sqrt5-2\sqrt3") + "$", r"$\dfrac{\sqrt2\left(\sqrt2+1\right)}{2-1}=" + Rm(r"2+\sqrt2") + "$", r"$\dfrac{6\left(3+\sqrt3\right)}{9-3}=" + Rm(r"3+\sqrt3") + "$",
               r"$\dfrac{\left(\sqrt3+1\right)^2}{3-1}=\dfrac{4+2\sqrt3}{2}=" + Rm(r"2+\sqrt3") + "$", r"$\dfrac{2\sqrt2+\sqrt3}{8-3}=" + Rm(r"\dfrac{2\sqrt2+\sqrt3}{5}") + "$"])),
 (3, T("Racionalitza i opera:", "Racionaliza y opera:") + tasks(2, [r"$\dfrac{1}{\sqrt2}+\dfrac{1}{\sqrt8}$", r"$\dfrac{2}{\sqrt3}-\sqrt3$", r"$\dfrac{1}{\sqrt2-1}-\dfrac{1}{\sqrt2+1}$", r"$\dfrac{\sqrt{12}}{\sqrt3+1}$"]),
     tasks(2, [r"$\dfrac{\sqrt2}{2}+\dfrac{\sqrt2}{4}=" + Rm(r"\dfrac{3\sqrt2}{4}") + "$", r"$\dfrac{2\sqrt3}{3}-\dfrac{3\sqrt3}{3}=" + Rm(r"-\dfrac{\sqrt3}{3}") + "$",
               r"$\left(\sqrt2+1\right)-\left(\sqrt2-1\right)=" + Rm("2") + "$", r"$\dfrac{2\sqrt3\left(\sqrt3-1\right)}{2}=" + Rm(r"3-\sqrt3") + "$"])),
]))

# =====================================================================
# 11. Problemes
ck([round(20 * math.sqrt(2), 2), round(math.sqrt(50) * math.sqrt(2), 6)], [28.28, 10.0])
chk([('2*(sqrt(12)+sqrt(27))', '10*sqrt(3)'), ('sqrt(12)*sqrt(27)', 18), ('sqrt(12+27)', 'sqrt(39)')])
chk([('sqrt(8+12)', '2*sqrt(5)'), ('sqrt(8)*sqrt(12)/2', '2*sqrt(6)')])
chk([('root(54,3)', '3*root(2,3)'), ('6*(3*root(2,3))**2', '54*root(4,3)')]); ck([round(54 ** (1 / 3), 2), round(54 * 4 ** (1 / 3), 1)], [3.78, 85.7])
chk([('sqrt((2*sqrt(3))**2-sqrt(3)**2)', 3), ('2*sqrt(3)*3/2', '3*sqrt(3)')])
chk([('21/(21*sqrt(2)/2)', 'sqrt(2)')]); ck(round(21 * math.sqrt(2), 2), 29.7)
S.append((T("Problemes", "Problemas"), [
 (2, T(r"Un quadrat té una àrea de $50\ \text{cm}^2$. Calcula'n el costat, el perímetre i la diagonal. Dona els resultats en forma de radical simplificat i, el perímetre, també aproximat a les centèsimes.",
       r"Un cuadrado tiene un área de $50\ \text{cm}^2$. Calcula su lado, su perímetro y su diagonal. Da los resultados en forma de radical simplificado y, el perímetro, también aproximado a las centésimas."),
     T("Costat: ", "Lado: ") + r"$\sqrt{50}=" + Rm(r"5\sqrt2\ \text{cm}") + r"$; \ " + T("perímetre: ", "perímetro: ") + r"$4\cdot5\sqrt2=" + Rm(r"20\sqrt2\approx28,28\ \text{cm}") + r"$; \ "
     + T("diagonal (Pitàgores): ", "diagonal (Pitágoras): ") + r"$\sqrt{50+50}=\sqrt{100}=" + Rm(r"10\ \text{cm}") + "$."),
 (2, T(r"Un rectangle fa $\sqrt{12}$ cm de base i $\sqrt{27}$ cm d'altura. Calcula'n el perímetre, l'àrea i la diagonal.", r"Un rectángulo mide $\sqrt{12}$ cm de base y $\sqrt{27}$ cm de altura. Calcula su perímetro, su área y su diagonal."),
     T("Perímetre: ", "Perímetro: ") + r"$2\left(2\sqrt3+3\sqrt3\right)=" + Rm(r"10\sqrt3\ \text{cm}") + r"$; \ " + T("àrea: ", "área: ") + r"$\sqrt{12\cdot27}=\sqrt{324}=" + Rm(r"18\ \text{cm}^2") + r"$; \ "
     + T("diagonal: ", "diagonal: ") + r"$\sqrt{12+27}=" + Rm(r"\sqrt{39}\ \text{cm}") + "$."),
 (2, T(r"Els catets d'un triangle rectangle fan $\sqrt8$ cm i $\sqrt{12}$ cm. Calcula'n la hipotenusa i l'àrea.", r"Los catetos de un triángulo rectángulo miden $\sqrt8$ cm y $\sqrt{12}$ cm. Calcula su hipotenusa y su área."),
     T("Hipotenusa: ", "Hipotenusa: ") + r"$\sqrt{8+12}=\sqrt{20}=" + Rm(r"2\sqrt5\ \text{cm}") + r"$; \ " + T("àrea: ", "área: ") + r"$\dfrac{\sqrt8\cdot\sqrt{12}}{2}=\dfrac{\sqrt{96}}{2}=\dfrac{4\sqrt6}{2}=" + Rm(r"2\sqrt6\ \text{cm}^2") + "$."),
 (2, T(r"Un cub té un volum de $54\ \text{cm}^3$. Calcula'n l'aresta i la superfície total en forma de radical, i aproxima-les a les centèsimes.", r"Un cubo tiene un volumen de $54\ \text{cm}^3$. Calcula su arista y su superficie total en forma de radical, y aproxímalas a las centésimas."),
     T("Aresta: ", "Arista: ") + r"$\sqrt[3]{54}=" + Rm(r"3\sqrt[3]2\approx3,78\ \text{cm}") + r"$; \ " + T("superfície: ", "superficie: ") + r"$6\left(3\sqrt[3]2\right)^2=6\cdot9\sqrt[3]4=" + Rm(r"54\sqrt[3]4\approx85,72\ \text{cm}^2") + "$."),
 (3, T(r"Un triangle equilàter fa $2\sqrt3$ cm de costat. Calcula'n l'altura i l'àrea.", r"Un triángulo equilátero mide $2\sqrt3$ cm de lado. Calcula su altura y su área."),
     T("Altura (Pitàgores amb la meitat del costat): ", "Altura (Pitágoras con la mitad del lado): ") + r"$h=\sqrt{\left(2\sqrt3\right)^2-\left(\sqrt3\right)^2}=\sqrt{12-3}=" + Rm(r"3\ \text{cm}") + r"$; \ "
     + T("àrea: ", "área: ") + r"$\dfrac{2\sqrt3\cdot3}{2}=" + Rm(r"3\sqrt3\ \text{cm}^2") + "$."),
 (3, T(r"En un full DIN A4, el costat llarg entre el costat curt és $\sqrt2$. Si el costat curt fa 21 cm, quant fa el llarg (exacte i aproximat)? Si pleguem el full per la meitat, el nou costat curt és la meitat del llarg: comprova, racionalitzant, que el nou full també compleix que llarg\,:\,curt $=\sqrt2$.",
       r"En un folio DIN A4, el lado largo entre el lado corto es $\sqrt2$. Si el lado corto mide 21 cm, ¿cuánto mide el largo (exacto y aproximado)? Si doblamos el folio por la mitad, el nuevo lado corto es la mitad del largo: comprueba, racionalizando, que el nuevo folio también cumple que largo\,:\,corto $=\sqrt2$."),
     T("Llarg: ", "Largo: ") + R(r"21\sqrt2\approx29,70\ \text{cm}") + r". \ " + T("Plegat: llarg 21 cm i curt ", "Doblado: largo 21 cm y corto ") + r"$\frac{21\sqrt2}{2}$ cm; \ $\dfrac{21}{\frac{21\sqrt2}{2}}=\dfrac{2}{\sqrt2}=\dfrac{2\sqrt2}{2}=" + Rm(r"\sqrt2") + "$."),
]))

# =====================================================================
TITOL = T("Nombres reals", "Números reales")
KW = T("nombres reals, nombres racionals, nombres irracionals, fracció generatriu, intervals, semirectes, unió, intersecció, arrels, radicals, potències d'exponent fraccionari, radicals equivalents, extracció de factors, operacions amb radicals, racionalització",
       "números reales, números racionales, números irracionales, fracción generatriz, intervalos, semirrectas, unión, intersección, raíces, radicales, potencias de exponente fraccionario, radicales equivalentes, extracción de factores, operaciones con radicales, racionalización")
INTRO_EX = T(r"Resol-los al quadern mostrant tots els passos. Fes servir la calculadora només quan l'enunciat ho diga.", r"Resuélvelos en el cuaderno mostrando todos los pasos. Usa la calculadora solo cuando el enunciado lo diga.")
INTRO_SOL = T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat.",
              r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad.")
build(HERE, 2, TITOL, S, KW, INTRO_EX, INTRO_SOL, lang=LANG, curs='4eso-a')
