# Fitxa de repàs per a l'examen de la unitat 3 (Proporcionalitat i percentatges) de 3r ESO, amb solucions pas a pas.
# Genera t3-fitxa-repas(.tex|-es.tex) i t3-fitxa-repas-solucions(.tex|-es.tex) a partir de la capçalera de les fitxes
# de repàs de la unitat 2 (../3eso-t2). No inclou interés compost, mescles ni moviments (decisió del professor).
# Cada resultat es comprova amb ck() abans d'escriure res.
#   python3 genera-repas.py && for f in t3-fitxa-repas t3-fitxa-repas-es t3-fitxa-repas-solucions t3-fitxa-repas-solucions-es; do pdflatex $f.tex; pdflatex $f.tex; done
import os, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
T2 = os.path.join(HERE, "..", "3eso-t2")


def ck(a, b, tol=1e-9):
    assert abs(float(a) - float(b)) < tol, (a, b)


# ======================================================================
# comprovacions numèriques de tots els resultats
# ======================================================================
# 1 percentatges, fraccions i decimals
ck(F(45, 100), F(9, 20)); ck(F(3, 8), 0.375); ck(F(6, 100), F(3, 50)); ck(F(120, 100), F(6, 5))
ordre = sorted([("8/25", 8 / 25), ("33%", 0.33), ("0,3p", 1 / 3), ("0,335", 0.335)], key=lambda t: t[1])
assert [o[0] for o in ordre] == ["8/25", "33%", "0,3p", "0,335"]
# 2 càlcul de percentatges
ck(260 * 0.35, 91); ck(1250 * 0.04, 50); ck(48 * 1.25, 60); ck(3000 * 0.005, 15)
ck(32 * 0.25, 8); ck((32 - 8) * 0.75, 18)
# 3 tant per cent i total
ck(18 / 120, 0.15); ck(63 / 84, 0.75); ck(84 / 0.35, 240); ck(208 / 640, 0.325); ck(54 / 0.18, 300)
# 4 augments i disminucions
ck(250 * 1.12, 280); ck(1800 * 0.65, 1170); ck(414 / 360, 1.15); ck(84 * 1.21, 101.64); ck(1250 / 1600, 0.78125)
# 5 quantitat inicial
ck(87.5 / 0.7, 125); ck(72.6 / 1.21, 60); ck(1620 / 1.08, 1500); ck(100 / 1.25, 80); ck(1.25 * 80, 100)
# 6 variacions encadenades
ck(1.2 * 0.9, 1.08); ck(300 * 0.75 * 0.9, 202.5); ck(1 - 0.75 * 0.9, 0.325); ck(1 / 1.25, 0.8); ck(1.05 * 1.05 * 0.9, 0.99225)
# 7 problemes de percentatges
ck((3 * 15 + 40) * 0.8 * 1.21, 82.28); ck(150000 * 1.06 * 0.94, 149460); ck(1.06 * 0.94, 0.9964)
# 8 repartiment directe
ck(120 / (6 + 9 + 15), 4); ck(4000 * 9, 36000); ck(6000 * 5, 30000); ck(2200 / 66000 * 36000, 1200); ck(2200 / 66000 * 30000, 1000)
# 9 repartiment invers (2,3,4 -> 6,4,3 ; 20,30,60 -> 3,2,1)
ck(1300 / 13, 100); ck(2700 / 6, 450)
ck(F(1300) / (F(1, 2) + F(1, 3) + F(1, 4)) / 2, 600); ck(F(2700) / (F(1, 20) + F(1, 30) + F(1, 60)) / 20, 1350)
# 10 proporcionalitat simple
ck(7.2 * 250 / 100, 18); ck(9 * 20 / 12, 15); ck(40 * 12 / 48, 10)
# 11 proporcionalitat composta
ck(6000 * 6 / 4 * 8 / 5, 14400); ck(15 * 8 / 10 * 6 / 8, 9); ck(10 * 15 / 12 * 8 / 10 * 900 / 600, 15)


# ======================================================================
# contingut: cada text és (valencià, castellà)
# ======================================================================
EX = []   # (títol, enunciat, cos de l'enunciat, títol curt solució, recorda, solució)


def ex(**k): EX.append(k)


TAULA_EX = (r"""\smallskip
{\renewcommand{\arraystretch}{1.8}\centering
\begin{tabular}{|C{0.6cm}|C{3.6cm}|C{3.6cm}|C{3.6cm}|}
\hline
\rowcolor{soft} & \textbf{%s} & \textbf{%s} & \textbf{Decimal} \\ \hline
a) & $45\,\%%$ & & \\ \hline
b) & & $\dfrac38$ & \\ \hline
c) & & & $0,06$ \\ \hline
d) & $120\,\%%$ & & \\ \hline
\end{tabular}\par}
""")
TAULA_SOL = (r"""\smallskip
{\renewcommand{\arraystretch}{2.8}\centering
\begin{tabular}{|C{0.6cm}|C{3.6cm}|C{3.6cm}|C{3.6cm}|}
\hline
\rowcolor{soft} & \textbf{%s} & \textbf{%s} & \textbf{Decimal} \\ \hline
a) & $45\,\%%$ & $\dfrac{45}{100}=\dfrac{9}{20}$ & $0,45$ \\ \hline
b) & $37,5\,\%%$ & $\dfrac38$ & $3:8=0,375$ \\ \hline
c) & $6\,\%%$ & $\dfrac{6}{100}=\dfrac{3}{50}$ & $0,06$ \\ \hline
d) & $120\,\%%$ & $\dfrac{120}{100}=\dfrac65$ & $1,2$ \\ \hline
\end{tabular}\par}
""")

ex(t=("Percentatges, fraccions i decimals", "Porcentajes, fracciones y decimales"),
   e=("Completa la taula (cada fila és el mateix nombre escrit de tres maneres; la fracció, irreductible) i, després, ordena de menor a major els nombres de l'apartat e).",
      "Completa la tabla (cada fila es el mismo número escrito de tres formas; la fracción, irreducible) y, después, ordena de menor a mayor los números del apartado e)."),
   cos=(TAULA_EX % ("Percentatge", "Fracció") + r"""
\smallskip
{\color{navy}\bfseries e)}\ \ $\dfrac{8}{25}\qquad 33\,\%\qquad 0,\overline{3}\qquad 0,335$
""", TAULA_EX % ("Porcentaje", "Fracción") + r"""
\smallskip
{\color{navy}\bfseries e)}\ \ $\dfrac{8}{25}\qquad 33\,\%\qquad 0,\overline{3}\qquad 0,335$
"""),
   ts=("Completa la taula i ordena.", "Completa la tabla y ordena."),
   rec=(r"$p\,\%=\dfrac{p}{100}$. \textbf{\% $\to$ decimal:} dividim entre 100 ($35\,\%=0,35$). \textbf{Decimal $\to$ \%:} multipliquem per 100. \textbf{\% $\to$ fracció:} escrivim $\frac{p}{100}$ i simplifiquem. \textbf{Fracció $\to$ decimal:} dividim el numerador entre el denominador. Per a \textbf{ordenar}, ho passem tot a la mateixa forma (per exemple, a percentatge).",
        r"$p\,\%=\dfrac{p}{100}$. \textbf{\% $\to$ decimal:} dividimos entre 100 ($35\,\%=0,35$). \textbf{Decimal $\to$ \%:} multiplicamos por 100. \textbf{\% $\to$ fracción:} escribimos $\frac{p}{100}$ y simplificamos. \textbf{Fracción $\to$ decimal:} dividimos el numerador entre el denominador. Para \textbf{ordenar}, lo pasamos todo a la misma forma (por ejemplo, a porcentaje)."),
   sol=(TAULA_SOL % ("Percentatge", "Fracció") + r"""
\smallskip
\pas{a) Simplifiquem $\frac{45}{100}$ dividint entre 5. \ b) $3:8=0,375$ i, multiplicant per 100, $37,5\,\%$. \ c) $0,06\cdot100=6\,\%$; $\frac{6}{100}$ es simplifica entre 2. \ d) Més del 100\,\%: el decimal és més gran que 1.}

\ap{e} \pas{Ho passem tot a percentatge: $\frac{8}{25}=\frac{32}{100}=32\,\%$; \ $0,\overline{3}=33,33\ldots\,\%$; \ $0,335=33,5\,\%$.}
\[32\,\%<33\,\%<33,\overline{3}\,\%<33,5\,\%\quad\Longrightarrow\quad\res{\frac{8}{25}<33\,\%<0,\overline{3}<0,335}\]
""", TAULA_SOL % ("Porcentaje", "Fracción") + r"""
\smallskip
\pas{a) Simplificamos $\frac{45}{100}$ dividiendo entre 5. \ b) $3:8=0,375$ y, multiplicando por 100, $37,5\,\%$. \ c) $0,06\cdot100=6\,\%$; $\frac{6}{100}$ se simplifica entre 2. \ d) Más del 100\,\%: el decimal es mayor que 1.}

\ap{e} \pas{Lo pasamos todo a porcentaje: $\frac{8}{25}=\frac{32}{100}=32\,\%$; \ $0,\overline{3}=33,33\ldots\,\%$; \ $0,335=33,5\,\%$.}
\[32\,\%<33\,\%<33,\overline{3}\,\%<33,5\,\%\quad\Longrightarrow\quad\res{\frac{8}{25}<33\,\%<0,\overline{3}<0,335}\]
"""))

ex(t=("Càlcul de percentatges", "Cálculo de porcentajes"),
   e=("Calcula:", "Calcula:"),
   cos=(r"""\begin{tasks}(4)
  \task El $35\,\%$ de $260$
  \task El $4\,\%$ de $1\,250$
  \task El $125\,\%$ de $48$
  \task El $0,5\,\%$ de $3\,000$
\end{tasks}
{\color{navy}\bfseries e)}\ \ En una classe de $32$ alumnes, el $25\,\%$ fa classes de dibuix i, dels que no en fan, el $75\,\%$ fa música. Quants alumnes fan música?
""", r"""\begin{tasks}(4)
  \task El $35\,\%$ de $260$
  \task El $4\,\%$ de $1\,250$
  \task El $125\,\%$ de $48$
  \task El $0,5\,\%$ de $3\,000$
\end{tasks}
{\color{navy}\bfseries e)}\ \ En una clase de $32$ alumnos, el $25\,\%$ va a clases de dibujo y, de los que no van, el $75\,\%$ hace música. ¿Cuántos alumnos hacen música?
"""),
   ts=("Calcula.", "Calcula."),
   rec=(r"El $p\,\%$ de $C$ és $C\cdot\dfrac{p}{100}$: multipliquem per l'expressió decimal del percentatge ($35\,\%\to0,35$; \ $4\,\%\to0,04$; \ $0,5\,\%\to0,005$). Quan un percentatge és «\emph{del que queda}», primer calculem el que queda i després hi apliquem el percentatge.",
        r"El $p\,\%$ de $C$ es $C\cdot\dfrac{p}{100}$: multiplicamos por la expresión decimal del porcentaje ($35\,\%\to0,35$; \ $4\,\%\to0,04$; \ $0,5\,\%\to0,005$). Cuando un porcentaje es «\emph{de lo que queda}», primero calculamos lo que queda y después le aplicamos el porcentaje."),
   sol=(r"""\begin{tasks}(2)
  \task $260\cdot0,35=\res{91}$
  \task $1\,250\cdot0,04=\res{50}$
  \task $48\cdot1,25=\res{60}$ \ \pas{(més del total)}
  \task $3\,000\cdot0,005=\res{15}$
\end{tasks}
\ap{e} \pas{Fan dibuix: $32\cdot0,25=8$ alumnes. No en fan: $32-8=24$. El $75\,\%$ \emph{d'aquests 24} fa música:}
\[24\cdot0,75=\res{18\ \text{alumnes}}\]
""", r"""\begin{tasks}(2)
  \task $260\cdot0,35=\res{91}$
  \task $1\,250\cdot0,04=\res{50}$
  \task $48\cdot1,25=\res{60}$ \ \pas{(más del total)}
  \task $3\,000\cdot0,005=\res{15}$
\end{tasks}
\ap{e} \pas{Van a dibujo: $32\cdot0,25=8$ alumnos. No van: $32-8=24$. El $75\,\%$ \emph{de esos 24} hace música:}
\[24\cdot0,75=\res{18\ \text{alumnos}}\]
"""))

ex(t=("Tant per cent que representa un nombre", "Tanto por ciento que representa un número"),
   e=("Resol:", "Resuelve:"),
   cos=(r"""\begin{tasks}(1)
  \task Quin percentatge representa $18$ respecte de $120$?
  \task Quin percentatge representa $63$ respecte de $84$?
  \task El $35\,\%$ d'un nombre és $84$. Quin és el nombre?
  \task En un institut de $640$ alumnes, $208$ hi venen amb autobús. Quin percentatge representen?
\end{tasks}
{\color{navy}\bfseries e)}\ \ Hem pagat $54$~€ de senyal per a reservar un viatge, que és el $18\,\%$ del preu total. Quant costa el viatge?
""", r"""\begin{tasks}(1)
  \task ¿Qué porcentaje representa $18$ respecto de $120$?
  \task ¿Qué porcentaje representa $63$ respecto de $84$?
  \task El $35\,\%$ de un número es $84$. ¿Cuál es el número?
  \task En un instituto de $640$ alumnos, $208$ vienen en autobús. ¿Qué porcentaje representan?
\end{tasks}
{\color{navy}\bfseries e)}\ \ Hemos pagado $54$~€ de señal para reservar un viaje, que es el $18\,\%$ del precio total. ¿Cuánto cuesta el viaje?
"""),
   ts=("Resol.", "Resuelve."),
   rec=(r"\textbf{Percentatge:} $p=\dfrac{\text{part}}{\text{total}}\cdot100$ (el total és la quantitat de referència, la que fa de $100\,\%$). \textbf{Total:} si coneixem la part i el percentatge, $\text{total}=\text{part}:\dfrac{p}{100}$.",
        r"\textbf{Porcentaje:} $p=\dfrac{\text{parte}}{\text{total}}\cdot100$ (el total es la cantidad de referencia, la que hace de $100\,\%$). \textbf{Total:} si conocemos la parte y el porcentaje, $\text{total}=\text{parte}:\dfrac{p}{100}$."),
   sol=(r"""\ap{a} \[\frac{18}{120}=0,15\ \longrightarrow\ 0,15\cdot100=\res{15\,\%}\]
\ap{b} \[\frac{63}{84}=0,75\ \longrightarrow\ \res{75\,\%}\]
\ap{c} \pas{Coneixem la part (84) i el percentatge (35\,\%); busquem el total.}
\[84:0,35=\res{240}\qquad(\text{comprovació: }240\cdot0,35=84)\]
\ap{d} \pas{El total són els 640 alumnes.}
\[\frac{208}{640}=0,325\ \longrightarrow\ \res{32,5\,\%}\]
\ap{e} \pas{Els 54 € són la part; el preu del viatge és el total.}
\[54:0,18=\res{300\text{ €}}\]
""", r"""\ap{a} \[\frac{18}{120}=0,15\ \longrightarrow\ 0,15\cdot100=\res{15\,\%}\]
\ap{b} \[\frac{63}{84}=0,75\ \longrightarrow\ \res{75\,\%}\]
\ap{c} \pas{Conocemos la parte (84) y el porcentaje (35\,\%); buscamos el total.}
\[84:0,35=\res{240}\qquad(\text{comprobación: }240\cdot0,35=84)\]
\ap{d} \pas{El total son los 640 alumnos.}
\[\frac{208}{640}=0,325\ \longrightarrow\ \res{32,5\,\%}\]
\ap{e} \pas{Los 54 € son la parte; el precio del viaje es el total.}
\[54:0,18=\res{300\text{ €}}\]
"""))

ex(t=("Augments i disminucions percentuals", "Aumentos y disminuciones porcentuales"),
   e=("Resol utilitzant l'índex de variació:", "Resuelve utilizando el índice de variación:"),
   cos=(r"""\begin{tasks}(1)
  \task Augmenta $250$ un $12\,\%$.
  \task Disminueix $1\,800$ un $35\,\%$.
  \task Una camisa de $84$~€ sense IVA. Quant costa amb el $21\,\%$ d'IVA?
  \task Un preu passa de $360$~€ a $414$~€. Quin percentatge ha pujat?
  \task Un cotxe de segona mà valia $1\,600$~€ i ara val $1\,250$~€. Quin percentatge ha baixat?
\end{tasks}
""", r"""\begin{tasks}(1)
  \task Aumenta $250$ un $12\,\%$.
  \task Disminuye $1\,800$ un $35\,\%$.
  \task Una camisa de $84$~€ sin IVA. ¿Cuánto cuesta con el $21\,\%$ de IVA?
  \task Un precio pasa de $360$~€ a $414$~€. ¿Qué porcentaje ha subido?
  \task Un coche de segunda mano valía $1\,600$~€ y ahora vale $1\,250$~€. ¿Qué porcentaje ha bajado?
\end{tasks}
"""),
   ts=("Augments i disminucions.", "Aumentos y disminuciones."),
   rec=(r"$C_f=C_i\cdot I_V$, amb $I_V=1+\dfrac{p}{100}$ si augmenta i $I_V=1-\dfrac{p}{100}$ si disminueix. Si coneixem les dues quantitats, $I_V=\dfrac{C_f}{C_i}$: si $I_V>1$ ha augmentat (per exemple, $1,15\to+15\,\%$) i si $I_V<1$ ha disminuït ($0,92\to-8\,\%$).",
        r"$C_f=C_i\cdot I_V$, con $I_V=1+\dfrac{p}{100}$ si aumenta e $I_V=1-\dfrac{p}{100}$ si disminuye. Si conocemos las dos cantidades, $I_V=\dfrac{C_f}{C_i}$: si $I_V>1$ ha aumentado (por ejemplo, $1,15\to+15\,\%$) y si $I_V<1$ ha disminuido ($0,92\to-8\,\%$)."),
   sol=(r"""\ap{a} \[I_V=1+0,12=1,12\qquad 250\cdot1,12=\res{280}\]
\ap{b} \[I_V=1-0,35=0,65\qquad 1\,800\cdot0,65=\res{1\,170}\]
\ap{c} \[84\cdot1,21=\res{101,64\text{ €}}\]
\ap{d} \[I_V=\frac{414}{360}=1,15\ \longrightarrow\ \text{ha pujat un }\res{15\,\%}\]
\ap{e} \pas{L'índex és menor que 1: $1-0,78125=0,21875$.}
\[I_V=\frac{1\,250}{1\,600}=0,78125\ \longrightarrow\ \text{ha baixat un }\res{21,875\,\%}\approx21,9\,\%\]
""", r"""\ap{a} \[I_V=1+0,12=1,12\qquad 250\cdot1,12=\res{280}\]
\ap{b} \[I_V=1-0,35=0,65\qquad 1\,800\cdot0,65=\res{1\,170}\]
\ap{c} \[84\cdot1,21=\res{101,64\text{ €}}\]
\ap{d} \[I_V=\frac{414}{360}=1,15\ \longrightarrow\ \text{ha subido un }\res{15\,\%}\]
\ap{e} \pas{El índice es menor que 1: $1-0,78125=0,21875$.}
\[I_V=\frac{1\,250}{1\,600}=0,78125\ \longrightarrow\ \text{ha bajado un }\res{21,875\,\%}\approx21,9\,\%\]
"""))

ex(t=("Càlcul de la quantitat inicial", "Cálculo de la cantidad inicial"),
   e=("Calcula la quantitat inicial:", "Calcula la cantidad inicial:"),
   cos=(r"""\begin{tasks}(1)
  \task Amb un descompte del $30\,\%$ hem pagat $87,50$~€ per unes sabatilles. Quin era el preu sense descompte?
  \task Un llibre costa $72,60$~€ amb el $21\,\%$ d'IVA inclòs. Quin és el preu sense IVA?
  \task Després d'una pujada del $8\,\%$, un sou és de $1\,620$~€. Quin era el sou abans?
  \task Vertader o fals? «Si després d'augmentar un $25\,\%$ una quantitat val $100$, abans valia $75$.» Justifica-ho.
\end{tasks}
""", r"""\begin{tasks}(1)
  \task Con un descuento del $30\,\%$ hemos pagado $87,50$~€ por unas zapatillas. ¿Cuál era el precio sin descuento?
  \task Un libro cuesta $72,60$~€ con el $21\,\%$ de IVA incluido. ¿Cuál es el precio sin IVA?
  \task Después de una subida del $8\,\%$, un sueldo es de $1\,620$~€. ¿Cuál era el sueldo antes?
  \task ¿Verdadero o falso? «Si después de aumentar un $25\,\%$ una cantidad vale $100$, antes valía $75$.» Justifícalo.
\end{tasks}
"""),
   ts=("Quantitat inicial.", "Cantidad inicial."),
   rec=(r"Desfem la variació \textbf{dividint} entre l'índex de variació: $C_i=\dfrac{C_f}{I_V}$. \textbf{Error típic:} aplicar el percentatge a la quantitat final; el percentatge sempre es calcula sobre la quantitat \emph{inicial}.",
        r"Deshacemos la variación \textbf{dividiendo} entre el índice de variación: $C_i=\dfrac{C_f}{I_V}$. \textbf{Error típico:} aplicar el porcentaje a la cantidad final; el porcentaje siempre se calcula sobre la cantidad \emph{inicial}."),
   sol=(r"""\ap{a} \pas{Un descompte del 30\,\% vol dir que paguem el 70\,\%: $I_V=0,7$.}
\[C_i=\frac{87,50}{0,7}=\res{125\text{ €}}\]
\ap{b} \[C_i=\frac{72,60}{1,21}=\res{60\text{ €}}\]
\ap{c} \[C_i=\frac{1\,620}{1,08}=\res{1\,500\text{ €}}\]
\ap{d} \pas{Dividim entre l'índex de variació $1,25$:}
\[C_i=\frac{100}{1,25}=80\ne75\ \Longrightarrow\ \res{\text{Fals}}\]
\pas{El 75 s'obté si (malament) restem el $25\,\%$ de 100. Comprovació: $80\cdot1,25=100$.}
""", r"""\ap{a} \pas{Un descuento del 30\,\% significa que pagamos el 70\,\%: $I_V=0,7$.}
\[C_i=\frac{87,50}{0,7}=\res{125\text{ €}}\]
\ap{b} \[C_i=\frac{72,60}{1,21}=\res{60\text{ €}}\]
\ap{c} \[C_i=\frac{1\,620}{1,08}=\res{1\,500\text{ €}}\]
\ap{d} \pas{Dividimos entre el índice de variación $1,25$:}
\[C_i=\frac{100}{1,25}=80\ne75\ \Longrightarrow\ \res{\text{Falso}}\]
\pas{El 75 se obtiene si (mal) restamos el $25\,\%$ de 100. Comprobación: $80\cdot1,25=100$.}
"""))

ex(t=("Variacions percentuals encadenades", "Variaciones porcentuales encadenadas"),
   e=("Resol:", "Resuelve:"),
   cos=(r"""\begin{tasks}(1)
  \task Un preu puja un $20\,\%$ i després baixa un $10\,\%$. Quina és la variació percentual total?
  \task Un abric de $300$~€ es rebaixa un $25\,\%$ i a la caixa ens fan un $10\,\%$ de descompte addicional. Quant paguem? Quin descompte total ens han fet?
  \task Un preu puja un $25\,\%$. Quin percentatge ha de baixar per a tornar a ser el preu inicial?
  \task Un producte puja un $5\,\%$, després un altre $5\,\%$ i finalment baixa un $10\,\%$. Ha pujat o ha baixat respecte del preu inicial? Quin percentatge?
\end{tasks}
""", r"""\begin{tasks}(1)
  \task Un precio sube un $20\,\%$ y después baja un $10\,\%$. ¿Cuál es la variación porcentual total?
  \task Un abrigo de $300$~€ se rebaja un $25\,\%$ y en la caja nos hacen un $10\,\%$ de descuento adicional. ¿Cuánto pagamos? ¿Qué descuento total nos han hecho?
  \task Un precio sube un $25\,\%$. ¿Qué porcentaje tiene que bajar para volver a ser el precio inicial?
  \task Un producto sube un $5\,\%$, después otro $5\,\%$ y finalmente baja un $10\,\%$. ¿Ha subido o ha bajado respecto del precio inicial? ¿Qué porcentaje?
\end{tasks}
"""),
   ts=("Variacions encadenades.", "Variaciones encadenadas."),
   rec=(r"Cada variació s'aplica sobre el resultat de l'anterior, per això l'índex de variació total és el \textbf{producte} dels índexs: $I_{V\,\text{total}}=I_{V_1}\cdot I_{V_2}\cdots$ \ Els percentatges encadenats \textbf{no se sumen}.",
        r"Cada variación se aplica sobre el resultado de la anterior, por eso el índice de variación total es el \textbf{producto} de los índices: $I_{V\,\text{total}}=I_{V_1}\cdot I_{V_2}\cdots$ \ Los porcentajes encadenados \textbf{no se suman}."),
   sol=(r"""\ap{a} \[I_V=1,2\cdot0,9=1,08\ \longrightarrow\ \res{+8\,\%}\quad\text{(no un }10\,\%\text{)}\]
\ap{b} \[I_V=0,75\cdot0,9=0,675\qquad 300\cdot0,675=\res{202,50\text{ €}}\]
\pas{Descompte total: $1-0,675=0,325$, és a dir, un $\res{32,5\,\%}$ (no un 35\,\%).}
\ap{c} \pas{Busquem l'índex que compensa $1,25$: el producte ha de ser 1.}
\[I_V=\frac{1}{1,25}=0,8\ \longrightarrow\ \text{ha de baixar un }\res{20\,\%}\]
\ap{d} \[I_V=1,05\cdot1,05\cdot0,9=0,99225<1\]
\pas{Ha \textbf{baixat}: $1-0,99225=0,00775$, és a dir, un $\res{0,775\,\%}$ (encara que $5+5-10=0$).}
""", r"""\ap{a} \[I_V=1,2\cdot0,9=1,08\ \longrightarrow\ \res{+8\,\%}\quad\text{(no un }10\,\%\text{)}\]
\ap{b} \[I_V=0,75\cdot0,9=0,675\qquad 300\cdot0,675=\res{202,50\text{ €}}\]
\pas{Descuento total: $1-0,675=0,325$, es decir, un $\res{32,5\,\%}$ (no un 35\,\%).}
\ap{c} \pas{Buscamos el índice que compensa $1,25$: el producto tiene que ser 1.}
\[I_V=\frac{1}{1,25}=0,8\ \longrightarrow\ \text{tiene que bajar un }\res{20\,\%}\]
\ap{d} \[I_V=1,05\cdot1,05\cdot0,9=0,99225<1\]
\pas{Ha \textbf{bajado}: $1-0,99225=0,00775$, es decir, un $\res{0,775\,\%}$ (aunque $5+5-10=0$).}
"""))

ex(t=("Problemes de percentatges", "Problemas de porcentajes"),
   e=("Resol aquests problemes, que combinen diversos tipus de càlcul:", "Resuelve estos problemas, que combinan varios tipos de cálculo:"),
   cos=(r"""\begin{tasks}(1)
  \task Comprem $3$ samarretes de $15$~€ i uns pantalons de $40$~€ (preus sense IVA). La botiga ens fa un $20\,\%$ de descompte i després s'hi aplica el $21\,\%$ d'IVA. Quant paguem?
  \task Un pis valia $150\,000$~€. Un any puja un $6\,\%$ i l'any següent baixa un $6\,\%$. Quant val ara? Ha guanyat o ha perdut valor respecte del preu inicial? Quin percentatge?
\end{tasks}
""", r"""\begin{tasks}(1)
  \task Compramos $3$ camisetas de $15$~€ y unos pantalones de $40$~€ (precios sin IVA). La tienda nos hace un $20\,\%$ de descuento y después se aplica el $21\,\%$ de IVA. ¿Cuánto pagamos?
  \task Un piso valía $150\,000$~€. Un año sube un $6\,\%$ y al año siguiente baja un $6\,\%$. ¿Cuánto vale ahora? ¿Ha ganado o ha perdido valor respecto del precio inicial? ¿Qué porcentaje?
\end{tasks}
"""),
   ts=("Problemes de percentatges.", "Problemas de porcentajes."),
   rec=(r"Llig bé l'ordre de les operacions: primer calculem la quantitat sobre la qual s'apliquen els percentatges i després multipliquem pels índexs de variació, un darrere de l'altre.",
        r"Lee bien el orden de las operaciones: primero calculamos la cantidad sobre la que se aplican los porcentajes y después multiplicamos por los índices de variación, uno detrás de otro."),
   sol=(r"""\ap{a} \pas{Preu sense IVA ni descompte: $3\cdot15+40=85$~€. Apliquem el descompte ($I_V=0,8$) i l'IVA ($I_V=1,21$):}
\[85\cdot0,8\cdot1,21=68\cdot1,21=\res{82,28\text{ €}}\]
\ap{b} \[150\,000\cdot1,06\cdot0,94=150\,000\cdot0,9964=\res{149\,460\text{ €}}\]
\pas{Ha \textbf{perdut} $150\,000-149\,460=540$~€, és a dir, $1-0,9964=0,0036\to\res{0,36\,\%}$.}
""", r"""\ap{a} \pas{Precio sin IVA ni descuento: $3\cdot15+40=85$~€. Aplicamos el descuento ($I_V=0,8$) y el IVA ($I_V=1,21$):}
\[85\cdot0,8\cdot1,21=68\cdot1,21=\res{82,28\text{ €}}\]
\ap{b} \[150\,000\cdot1,06\cdot0,94=150\,000\cdot0,9964=\res{149\,460\text{ €}}\]
\pas{Ha \textbf{perdido} $150\,000-149\,460=540$~€, es decir, $1-0,9964=0,0036\to\res{0,36\,\%}$.}
"""))

ex(t=("Repartiments directament proporcionals", "Repartos directamente proporcionales"),
   e=("Resol:", "Resuelve:"),
   cos=(r"""\begin{tasks}(1)
  \task Tres amics van comprar una papereta de rifa: un hi va posar $6$~€, un altre $9$~€ i el tercer $15$~€. Si guanyen $120$~€, quant li correspon a cadascun?
  \task Dues sòcies obrin una botiga: Anna hi posa $4\,000$~€ durant $9$ mesos i Berta $6\,000$~€ durant $5$ mesos. Com s'han de repartir un benefici de $2\,200$~€?
\end{tasks}
""", r"""\begin{tasks}(1)
  \task Tres amigos compraron una papeleta de rifa: uno puso $6$~€, otro $9$~€ y el tercero $15$~€. Si ganan $120$~€, ¿cuánto le corresponde a cada uno?
  \task Dos socias abren una tienda: Ana pone $4\,000$~€ durante $9$ meses y Berta $6\,000$~€ durante $5$ meses. ¿Cómo deben repartirse un beneficio de $2\,200$~€?
\end{tasks}
"""),
   ts=("Repartiments directes.", "Repartos directos."),
   rec=(r"Repartir $N$ directament a $a,\ b,\ c$: calculem el valor d'una part, $k=\dfrac{N}{a+b+c}$, i cadascú rep $k\cdot a$, $k\cdot b$, $k\cdot c$. Si el repartiment depén de dues magnituds (diners i temps), repartim directament al \textbf{producte}. Comprova sempre que la suma de les parts és $N$.",
        r"Repartir $N$ directamente a $a,\ b,\ c$: calculamos el valor de una parte, $k=\dfrac{N}{a+b+c}$, y cada uno recibe $k\cdot a$, $k\cdot b$, $k\cdot c$. Si el reparto depende de dos magnitudes (dinero y tiempo), repartimos directamente al \textbf{producto}. Comprueba siempre que la suma de las partes es $N$."),
   sol=(r"""\ap{a} \[k=\frac{120}{6+9+15}=\frac{120}{30}=4\qquad 6\cdot4=\res{24\text{ €}}\quad 9\cdot4=\res{36\text{ €}}\quad 15\cdot4=\res{60\text{ €}}\]
\pas{Comprovació: $24+36+60=120$.}
\ap{b} \pas{Repartim directament a capital $\times$ temps: Anna $4\,000\cdot9=36\,000$; Berta $6\,000\cdot5=30\,000$.}
\[k=\frac{2\,200}{36\,000+30\,000}=\frac{2\,200}{66\,000}=\frac{1}{30}\qquad\text{Anna: }\frac{36\,000}{30}=\res{1\,200\text{ €}}\quad\text{Berta: }\frac{30\,000}{30}=\res{1\,000\text{ €}}\]
""", r"""\ap{a} \[k=\frac{120}{6+9+15}=\frac{120}{30}=4\qquad 6\cdot4=\res{24\text{ €}}\quad 9\cdot4=\res{36\text{ €}}\quad 15\cdot4=\res{60\text{ €}}\]
\pas{Comprobación: $24+36+60=120$.}
\ap{b} \pas{Repartimos directamente a capital $\times$ tiempo: Ana $4\,000\cdot9=36\,000$; Berta $6\,000\cdot5=30\,000$.}
\[k=\frac{2\,200}{36\,000+30\,000}=\frac{2\,200}{66\,000}=\frac{1}{30}\qquad\text{Ana: }\frac{36\,000}{30}=\res{1\,200\text{ €}}\quad\text{Berta: }\frac{30\,000}{30}=\res{1\,000\text{ €}}\]
"""))

ex(t=("Repartiments inversament proporcionals", "Repartos inversamente proporcionales"),
   e=("Resol:", "Resuelve:"),
   cos=(r"""\begin{tasks}(1)
  \task Reparteix $1\,300$ de manera inversament proporcional a $2$, $3$ i $4$.
  \task Un premi de $2\,700$~€ es reparteix entre tres corredors de manera inversament proporcional al temps que han tardat a fer una cursa: $20$, $30$ i $60$ minuts. Quant rep cadascun?
\end{tasks}
""", r"""\begin{tasks}(1)
  \task Reparte $1\,300$ de forma inversamente proporcional a $2$, $3$ y $4$.
  \task Un premio de $2\,700$~€ se reparte entre tres corredores de forma inversamente proporcional al tiempo que han tardado en hacer una carrera: $20$, $30$ y $60$ minutos. ¿Cuánto recibe cada uno?
\end{tasks}
"""),
   ts=("Repartiments inversos.", "Repartos inversos."),
   rec=(r"Qui té el nombre més gran rep \textbf{menys}. Repartir inversament a $a,\ b,\ c$ és repartir directament a $\frac1a,\ \frac1b,\ \frac1c$. \textbf{Truc:} reduïm els inversos a comú denominador (el m.c.m.) i repartim directament als numeradors.",
        r"Quien tiene el número mayor recibe \textbf{menos}. Repartir inversamente a $a,\ b,\ c$ es repartir directamente a $\frac1a,\ \frac1b,\ \frac1c$. \textbf{Truco:} reducimos los inversos a común denominador (el m.c.m.) y repartimos directamente a los numeradores."),
   sol=(r"""\ap{a} \pas{m.c.m.$(2,3,4)=12$:}
\[\frac12,\ \frac13,\ \frac14=\frac{6}{12},\ \frac{4}{12},\ \frac{3}{12}\ \longrightarrow\ \text{directament a }6,\ 4,\ 3\]
\[k=\frac{1\,300}{6+4+3}=100\qquad\res{600},\quad\res{400},\quad\res{300}\]
\ap{b} \pas{Menys temps $\to$ més premi. m.c.m.$(20,30,60)=60$:}
\[\frac{1}{20},\ \frac{1}{30},\ \frac{1}{60}=\frac{3}{60},\ \frac{2}{60},\ \frac{1}{60}\ \longrightarrow\ \text{directament a }3,\ 2,\ 1\]
\[k=\frac{2\,700}{3+2+1}=450\qquad\res{1\,350\text{ €}},\quad\res{900\text{ €}},\quad\res{450\text{ €}}\]
""", r"""\ap{a} \pas{m.c.m.$(2,3,4)=12$:}
\[\frac12,\ \frac13,\ \frac14=\frac{6}{12},\ \frac{4}{12},\ \frac{3}{12}\ \longrightarrow\ \text{directamente a }6,\ 4,\ 3\]
\[k=\frac{1\,300}{6+4+3}=100\qquad\res{600},\quad\res{400},\quad\res{300}\]
\ap{b} \pas{Menos tiempo $\to$ más premio. m.c.m.$(20,30,60)=60$:}
\[\frac{1}{20},\ \frac{1}{30},\ \frac{1}{60}=\frac{3}{60},\ \frac{2}{60},\ \frac{1}{60}\ \longrightarrow\ \text{directamente a }3,\ 2,\ 1\]
\[k=\frac{2\,700}{3+2+1}=450\qquad\res{1\,350\text{ €}},\quad\res{900\text{ €}},\quad\res{450\text{ €}}\]
"""))

ex(t=("Proporcionalitat simple directa i inversa", "Proporcionalidad simple directa e inversa"),
   e=("Resol:", "Resuelve:"),
   cos=(r"""\begin{tasks}(1)
  \task Indica si són directament proporcionals, inversament proporcionals o no proporcionals: (1) el nombre de pintors i el temps que tarden a pintar una casa; (2) els litres de gasolina i el preu que paguem; (3) el pes i l'edat d'un bebé.
  \task Un cotxe gasta $7,2$ L de gasolina cada $100$ km. Quants litres gastarà en $250$ km?
  \task $9$ obrers fan una obra en $20$ dies. Quants dies tardarien $12$ obrers?
  \task Un campament de $40$ persones té menjar per a $15$ dies. Al cap de $3$ dies hi arriben $8$ persones més. Per a quants dies arribarà el menjar que queda?
\end{tasks}
""", r"""\begin{tasks}(1)
  \task Indica si son directamente proporcionales, inversamente proporcionales o no proporcionales: (1) el número de pintores y el tiempo que tardan en pintar una casa; (2) los litros de gasolina y el precio que pagamos; (3) el peso y la edad de un bebé.
  \task Un coche gasta $7,2$ L de gasolina cada $100$ km. ¿Cuántos litros gastará en $250$ km?
  \task $9$ obreros hacen una obra en $20$ días. ¿Cuántos días tardarían $12$ obreros?
  \task Un campamento de $40$ personas tiene comida para $15$ días. Al cabo de $3$ días llegan $8$ personas más. ¿Para cuántos días llegará la comida que queda?
\end{tasks}
"""),
   ts=("Proporcionalitat simple.", "Proporcionalidad simple."),
   rec=(r"\textbf{Directa:} el doble $\to$ el doble; es conserva el quocient: $x=\dfrac{b\cdot c}{a}$. \textbf{Inversa:} el doble $\to$ la meitat; es conserva el producte: $x=\dfrac{a\cdot b}{c}$. Per a decidir-ho, pregunta't: \emph{si una augmenta, l'altra augmenta o disminueix?}",
        r"\textbf{Directa:} el doble $\to$ el doble; se conserva el cociente: $x=\dfrac{b\cdot c}{a}$. \textbf{Inversa:} el doble $\to$ la mitad; se conserva el producto: $x=\dfrac{a\cdot b}{c}$. Para decidirlo, pregúntate: \emph{si una aumenta, ¿la otra aumenta o disminuye?}"),
   sol=(r"""\ap{a} \pas{(1) Més pintors $\to$ menys temps: $\res{\text{inversa}}$. \ (2) El doble de litres costa el doble: $\res{\text{directa}}$. \ (3) Creixen tots dos, però un bebé del doble d'edat no pesa el doble: $\res{\text{no proporcionals}}$.}
\ap{b} \pas{Més quilòmetres $\to$ més gasolina (directa).}
\[x=\frac{7,2\cdot250}{100}=\res{18\ \text{L}}\]
\ap{c} \pas{Més obrers $\to$ menys dies (inversa). Un obrer sol tardaria $9\cdot20=180$ dies.}
\[x=\frac{9\cdot20}{12}=\frac{180}{12}=\res{15\ \text{dies}}\]
\ap{d} \pas{Després de 3 dies, a 40 persones els queda menjar per a $15-3=12$ dies. Ara són 48 (inversa):}
\[x=\frac{40\cdot12}{48}=\res{10\ \text{dies}}\]
""", r"""\ap{a} \pas{(1) Más pintores $\to$ menos tiempo: $\res{\text{inversa}}$. \ (2) El doble de litros cuesta el doble: $\res{\text{directa}}$. \ (3) Crecen los dos, pero un bebé del doble de edad no pesa el doble: $\res{\text{no proporcionales}}$.}
\ap{b} \pas{Más kilómetros $\to$ más gasolina (directa).}
\[x=\frac{7,2\cdot250}{100}=\res{18\ \text{L}}\]
\ap{c} \pas{Más obreros $\to$ menos días (inversa). Un obrero solo tardaría $9\cdot20=180$ días.}
\[x=\frac{9\cdot20}{12}=\frac{180}{12}=\res{15\ \text{días}}\]
\ap{d} \pas{Después de 3 días, a 40 personas les queda comida para $15-3=12$ días. Ahora son 48 (inversa):}
\[x=\frac{40\cdot12}{48}=\res{10\ \text{días}}\]
"""))

ex(t=("Proporcionalitat composta", "Proporcionalidad compuesta"),
   e=("Resol:", "Resuelve:"),
   cos=(r"""\begin{tasks}(1)
  \task $4$ impressores, funcionant $5$ hores, imprimeixen $6\,000$ fulls. Quants fulls imprimiran $6$ impressores en $8$ hores?
  \task $8$ obrers, treballant $6$ hores diàries, fan una obra en $15$ dies. Quants dies tardarien $10$ obrers treballant $8$ hores diàries?
  \task $15$ operaris, treballant $8$ hores diàries, fabriquen $600$ peces en $10$ dies. Quants dies necessitaran $12$ operaris, treballant $10$ hores diàries, per a fabricar $900$ peces?
\end{tasks}
""", r"""\begin{tasks}(1)
  \task $4$ impresoras, funcionando $5$ horas, imprimen $6\,000$ hojas. ¿Cuántas hojas imprimirán $6$ impresoras en $8$ horas?
  \task $8$ obreros, trabajando $6$ horas diarias, hacen una obra en $15$ días. ¿Cuántos días tardarían $10$ obreros trabajando $8$ horas diarias?
  \task $15$ operarios, trabajando $8$ horas diarias, fabrican $600$ piezas en $10$ días. ¿Cuántos días necesitarán $12$ operarios, trabajando $10$ horas diarias, para fabricar $900$ piezas?
\end{tasks}
"""),
   ts=("Proporcionalitat composta.", "Proporcionalidad compuesta."),
   rec=(r"Fem una taula amb les magnituds (la incògnita al final). Comparem \textbf{cada magnitud amb la de la incògnita per separat} i decidim si és directa (D) o inversa (I). Multipliquem el valor conegut per cada raó: si és D, per $\frac{\text{nou}}{\text{antic}}$; si és I, per $\frac{\text{antic}}{\text{nou}}$.",
        r"Hacemos una tabla con las magnitudes (la incógnita al final). Comparamos \textbf{cada magnitud con la de la incógnita por separado} y decidimos si es directa (D) o inversa (I). Multiplicamos el valor conocido por cada razón: si es D, por $\frac{\text{nuevo}}{\text{antiguo}}$; si es I, por $\frac{\text{antiguo}}{\text{nuevo}}$."),
   sol=(r"""\ap{a} \pas{Més impressores $\to$ més fulls (D). Més hores $\to$ més fulls (D).}
\[x=6\,000\cdot\frac64\cdot\frac85=6\,000\cdot1,5\cdot1,6=\res{14\,400\ \text{fulls}}\]
\ap{b} \pas{Més obrers $\to$ menys dies (I). Més hores al dia $\to$ menys dies (I). Girem les dues raons.}
\[x=15\cdot\frac{8}{10}\cdot\frac{6}{8}=15\cdot0,8\cdot0,75=\res{9\ \text{dies}}\]
\ap{c} \pas{Menys operaris $\to$ més dies (I). Més hores al dia $\to$ menys dies (I). Més peces $\to$ més dies (D).}
\[x=10\cdot\frac{15}{12}\cdot\frac{8}{10}\cdot\frac{900}{600}=10\cdot1,25\cdot0,8\cdot1,5=\res{15\ \text{dies}}\]
""", r"""\ap{a} \pas{Más impresoras $\to$ más hojas (D). Más horas $\to$ más hojas (D).}
\[x=6\,000\cdot\frac64\cdot\frac85=6\,000\cdot1,5\cdot1,6=\res{14\,400\ \text{hojas}}\]
\ap{b} \pas{Más obreros $\to$ menos días (I). Más horas al día $\to$ menos días (I). Invertimos las dos razones.}
\[x=15\cdot\frac{8}{10}\cdot\frac{6}{8}=15\cdot0,8\cdot0,75=\res{9\ \text{días}}\]
\ap{c} \pas{Menos operarios $\to$ más días (I). Más horas al día $\to$ menos días (I). Más piezas $\to$ más días (D).}
\[x=10\cdot\frac{15}{12}\cdot\frac{8}{10}\cdot\frac{900}{600}=10\cdot1,25\cdot0,8\cdot1,5=\res{15\ \text{días}}\]
"""))


# ======================================================================
# capçaleres (preses de les fitxes de repàs de la unitat 2)
# ======================================================================
def head(src, sol, es):
    s = open(os.path.join(T2, src), encoding="utf-8").read()
    s = s[:s.index(r"\begin{document}")]
    if es:
        s = s.replace("unidad 2: Números reales", "unidad 3: Proporcionalidad y porcentajes")
        s = s.replace("Unidad 2 · Números reales", "Unidad 3 · Proporcionalidad y porcentajes").replace("Unidad 2}", "Unidad 3}")
        s = s.replace("pdfkeywords={números reales, potencias, radicales, notación científica, intervalos}",
                      "pdfkeywords={porcentajes, aumentos, disminuciones, repartos, proporcionalidad directa, inversa y compuesta}")
    else:
        s = s.replace("unitat 2: Nombres reals", "unitat 3: Proporcionalitat i percentatges")
        s = s.replace("Unitat 2 · Nombres reals", "Unitat 3 · Proporcionalitat i percentatges").replace("Unitat 2}", "Unitat 3}")
        s = s.replace("pdfkeywords={nombres reals, potències, radicals, notació científica, intervals}",
                      "pdfkeywords={percentatges, augments, disminucions, repartiments, proporcionalitat directa, inversa i composta}")
    assert "2:" not in s.split("pdftitle")[1][:120] and "Nombres reals" not in s and "Números reales" not in s, src
    return s


INTRO_EX = (r"Aquesta fitxa repassa els continguts de l'examen: hi ha un exercici de cada tipus. Pots fer servir la \textbf{calculadora}, però escriu tots els passos al quadern (l'exercici 1 el pots completar en aquest full). Després, corregeix-te amb les solucions pas a pas.",
            r"Esta ficha repasa los contenidos del examen: hay un ejercicio de cada tipo. Puedes usar la \textbf{calculadora}, pero escribe todos los pasos en el cuaderno (el ejercicio 1 lo puedes completar en esta hoja). Después, corrígete con las soluciones paso a paso.")
INTRO_SOL = (r"Abans de cada exercici tens un requadre \textbf{Recorda} amb la regla que cal aplicar. Compara els teus passos amb els d'ací, no només el resultat: el resultat final està dins d'un requadre. Si t'has equivocat, torna a fer l'apartat sense mirar la solució.",
             r"Antes de cada ejercicio tienes un recuadro \textbf{Recuerda} con la regla que hay que aplicar. Compara tus pasos con los de aquí, no solo el resultado: el resultado final está dentro de un recuadro. Si te has equivocado, vuelve a hacer el apartado sin mirar la solución.")
CAP = {(0, 0): r"\capcalera{Matemàtiques}{3r ESO}{Fitxa de repàs · Unitat 3}{Proporcionalitat i percentatges}",
       (0, 1): r"\capcalera{Matemáticas}{3\textsuperscript{o} ESO}{Ficha de repaso · Unidad 3}{Proporcionalidad y porcentajes}",
       (1, 0): r"\capcalera{Matemàtiques}{3r ESO}{Solucions de la fitxa de repàs · Unitat 3}{Proporcionalitat i percentatges}",
       (1, 1): r"\capcalera{Matemáticas}{3\textsuperscript{o} ESO}{Soluciones de la ficha de repaso · Unidad 3}{Proporcionalidad y porcentajes}"}


def build(sol, es):
    i = 1 if es else 0
    src = ("t2-fitxa-repas-solucions" if sol else "t2-fitxa-repas") + ("-es" if es else "") + ".tex"
    out = [head(src, sol, es), r"\begin{document}", r"\thispagestyle{primera}", "", CAP[(sol, i)], r"\vspace{8pt}", "",
           r"\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]",
           r"\small " + (INTRO_SOL if sol else INTRO_EX)[i], r"\end{tcolorbox}", ""]
    for k in EX:
        out.append("% " + "-" * 53)
        if sol:
            out.append(r"\ex{%s}{%s}" % (k["t"][i], k["ts"][i]))
            out.append(r"\recorda{%s}" % k["rec"][i])
            out.append("")
            out.append(k["sol"][i])
        else:
            out.append(r"\ex{%s}{%s}" % (k["t"][i], k["e"][i]))
            out.append(k["cos"][i])
    out.append(r"\end{document}")
    name = "t3-fitxa-repas" + ("-solucions" if sol else "") + ("-es" if es else "") + ".tex"
    open(os.path.join(HERE, name), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(name, len(EX), "exercicis")


for sol in (0, 1):
    for es in (False, True):
        build(sol, es)
