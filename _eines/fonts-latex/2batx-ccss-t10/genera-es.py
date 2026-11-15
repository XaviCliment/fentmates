# Versió en castellà de genera.py. Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 10: Distribució binomial i normal)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Els exercicis marcats amb \pau{...} són de la PAU d'altres comunitats (recopilació «Estadística y probabilidad en pruebas
# de acceso a la universidad de todas las comunidades de España» de www.ebaumatematicas.com, curs 2026/27), traduïts al
# valencià; se n'han llevat els apartats d'inferència (mitjanes mostrals, intervals de confiança), que no són del temari.
# Les probabilitats de la normal es calculen com a la PAU valenciana: z arredonit a dues decimals i valor de la taula
# N(0,1) amb quatre decimals (Phi); en els problemes inversos es pren el valor de la taula més pròxim (zinv). Les de la
# binomial, amb la fórmula (o amb la taula de la PAU, que dona els mateixos valors arredonits). CHK compara cada resultat
# amb la solució oficial (amb tolerància quan l'oficial no arredoneix z) o amb el valor esperat.
# Ús: python3 genera.py && pdflatex t10-fitxa-exercicis.tex (dues vegades) && pdflatex t10-fitxa-solucions.tex (dues vegades)
import os, re, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def dec(x, k=4):
    s = ('%.*f' % (k, float(x))).rstrip('0').rstrip('.')
    return s.replace('.', '{,}').replace('-', '-')
def d4(x): return ('%.4f' % float(x)).replace('.', '{,}')
def B(x, k=4): return r'\res{%s}' % d4(x) if k == 4 else r'\res{%s}' % dec(x, k)

# ---------- binomial i normal com a la PAU ----------
def pmf(n, p, k): return math.comb(n, k) * p ** k * (1 - p) ** (n - k)
def r2(z): return math.floor(abs(z) * 100 + 0.5 + 1e-9) / 100 * (1 if z >= 0 else -1)
def Phi(z):
    z = r2(z)
    if z < 0: return round(1 - Phi(-z), 4)
    if z >= 4: return 1.0
    return round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)
TAB = [(r / 10 + c / 100, Phi(r / 10 + c / 100)) for r in range(40) for c in range(10)]
def zinv(p):
    """z amb P(Z <= z) = p, prenent el valor de la taula més pròxim (mitjana si n'hi ha dos d'igual de pròxims)"""
    neg = p < 0.5; pp = 1 - p if neg else p
    d = min(abs(v - pp) for _, v in TAB); zs = [z for z, v in TAB if abs(abs(v - pp) - d) < 1e-12]
    z = sum(zs) / len(zs)
    return -z if neg else z
def zs(x, m, s): return r2((x - m) / s)
def fz(z): return dec(z, 2)

# ---------- figures: campana de Gauss amb l'àrea ombrejada ----------
def gauss(shade, ticks=(), w=4.2):
    """shade: llista d'intervals en unitats de z (None = infinit); ticks: [(z, etiqueta)]"""
    sx = w / 7.0
    o = [r'\begin{tikzpicture}[x=%.3fcm,y=1.6cm,baseline=(current bounding box.center)]' % sx]
    for a, b in shade:
        a = -3.5 if a is None else max(a, -3.5); b = 3.5 if b is None else min(b, 3.5)
        o.append(r'\fill[accent!35] (%.3f,0) -- plot[domain=%.3f:%.3f,samples=60,smooth] (\x,{exp(-\x*\x/2)}) -- (%.3f,0) -- cycle;' % (a, a, b, b))
    o.append(r'\draw[muted,-latex] (-3.6,0)--(3.7,0);')
    o.append(r'\draw[teal,thick] plot[domain=-3.5:3.5,samples=90,smooth] (\x,{exp(-\x*\x/2)});')
    for z, l in ticks:
        o.append(r'\draw[muted] (%.3f,0.05)--(%.3f,-0.05) node[below,font=\scriptsize,text=navy]{$%s$};' % (z, z, l))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'

CHK = []
def ck(x, y, tol=1e-9):
    assert abs(float(x) - float(y)) <= tol, (x, y); CHK.append(1); return x

S = []

# =====================================================================
# 1. Variables aleatòries discretes
k1 = F(2, 10); P1 = [F(1, 10), k1, F(3, 10), 2 * k1]; mu1 = sum(i * p for i, p in enumerate(P1)); v1 = sum(i * i * p for i, p in enumerate(P1)) - mu1 ** 2
ck(sum(P1), 1); ck(mu1, 2); ck(v1, 1)
S.append(("Variables aleatorias discretas", [
 (1, r"Di si las variables siguientes son discretas o continuas:" + tasks(2, [r"El número de hermanos de un alumno.", r"El tiempo que tarda un autobús en llegar.", r"El peso de un bebé.", r"El número de clientes que entran en una tienda en una hora.", r"La nota de un examen con decimales.", r"El número de caras en 10 lanzamientos."]),
     tasks(2, [r"\rest{Discreta}", r"\rest{Continua}", r"\rest{Continua}", r"\rest{Discreta}", r"\rest{Continua} (es una medida que puede tomar cualquier valor)", r"\rest{Discreta}"])),
 (2, r"Una variable aleatoria $X$ toma los valores 0, 1, 2 y 3 con probabilidades $0{,}1$, $k$, $0{,}3$ y $2k$, respectivamente." + tasks(1, [r"Calcula $k$.", r"Calcula la media y la desviación típica de $X$.", r"Calcula $P(X\geq2)$."])
     + recorda(r"$\sum p_i=1$; \ $\mu=\sum x_ip_i$; \ $\sigma^2=\sum x_i^2p_i-\mu^2$."),
     tasks(1, [r"$0{,}1+k+0{,}3+2k=1\Rightarrow3k=0{,}6\Rightarrow\res{k=0{,}2}$", r"$\mu=0+0{,}2+0{,}6+1{,}2=\res{2}$; \ $\sigma^2=0{,}2+1{,}2+3{,}6-2^2=1\Rightarrow\res{\sigma=1}$",
               r"$P(X\geq2)=0{,}3+0{,}4=\res{0{,}7}$"])),
 (2, r"En un juego se lanzan dos dados: si sale un doble, ganas 5 euros; si no, pierdes 1 euro. Sea $X$ la ganancia. Calcula la ganancia media y la desviación típica. ¿Es un juego justo?",
     r"$P(X=5)=\frac6{36}=\frac16$, $P(X=-1)=\frac56$. $\mu=5\cdot\frac16-1\cdot\frac56=\res{0}$: \rest{es un juego justo}. $\sigma^2=25\cdot\frac16+1\cdot\frac56-0=5\Rightarrow\res{\sigma=\sqrt5\approx2{,}24}$ euros."),
]))
ck(5 * F(1, 6) - F(5, 6), 0); ck(25 * F(1, 6) + F(5, 6), 5)

# =====================================================================
# 2. Distribució binomial
d5 = [pmf(5, 1 / 6, 2), 1 - (5 / 6) ** 5]
ar = pmf(4, 0.48, 2); ck(ar, 0.3738, 5e-5)
ro = 1 - 0.38 ** 3; ck(ro, 0.9451, 5e-5)
an = [0.65 + 0.55 - 0.35, 0.2 / 0.35, pmf(11, 0.55, 8), 11 * 0.55]; ck(an[0], 0.85); ck(an[1], 4 / 7); ck(an[2], 0.1259, 5e-5)
pv = [0.5 ** 3, 0.6 ** 2]; ck(pv[0], 0.125); ck(pv[1], 0.36)
cy = [pmf(10, 0.1, 2), pmf(10, 0.1, 0) + pmf(10, 0.1, 1)]; ck(cy[0], 0.1937, 5e-5); ck(cy[1], 0.7361, 5e-5)
pg = 560 / 3280; cg = 1 - pmf(10, pg, 0) - pmf(10, pg, 1); ck(cg, 0.53, 5e-3)
S.append(("La distribución binomial", [
 (1, r"Di si las variables siguientes siguen una distribución binomial y, si es así, indica sus parámetros:" + tasks(1, [
      r"Número de seises en 12 lanzamientos de un dado.", r"Número de bolas rojas al sacar 3 bolas, sin reemplazamiento, de una urna con 4 rojas y 6 blancas.",
      r"Número de piezas defectuosas en una muestra de 50, si el 2\,\% de la producción es defectuosa.", r"Número de lanzamientos de una moneda hasta que sale la primera cara."])
     + recorda(r"una binomial $B(n,p)$ cuenta los éxitos en $n$ pruebas independientes con la misma probabilidad de éxito $p$."),
     tasks(1, [r"\rest{Sí}: $B\left(12,\frac16\right)$.", r"\rest{No}: sin reemplazamiento, la probabilidad de roja cambia en cada extracción.", r"\rest{Sí}: $B(50;\ 0{,}02)$ (la producción es muy grande: las pruebas son prácticamente independientes).",
               r"\rest{No}: el número de pruebas no está fijado."])),
 (1, r"Se lanza un dado 5 veces. Calcula la probabilidad de obtener exactamente dos cincos y la de obtener al menos un cinco.",
     r"$X\sim B\left(5,\frac16\right)$: \ $P(X=2)=\binom52\left(\frac16\right)^2\left(\frac56\right)^3=" + B(d5[0]) + r"$; \ $P(X\geq1)=1-\left(\frac56\right)^5=" + B(d5[1]) + "$."),
 (1, r"\pau{Aragón, EvAU extraordinaria 2024} En una ciudad, según los datos del INE, el 52\,\% de los habitantes son mujeres y el 48\,\% hombres. Se eligen cuatro personas de esta ciudad con reemplazamiento. Sea $X$ la variable que cuenta el número de hombres seleccionados. ¿Qué distribución tiene la variable $X$? Calcula $P(X=2)$.",
     r"$\res{X\sim B(4;\ 0{,}48)}$: 4 pruebas independientes con la misma probabilidad de hombre. \ $P(X=2)=\binom42\,0{,}48^2\,0{,}52^2=6\cdot0{,}2304\cdot0{,}2704=" + B(ar) + "$."),
 (1, r"\pau{Aragón, EvAU ordinaria 2024} Una vez hecha la votación, el candidato Rupérez ha ganado con el 62\,\% de los votos. Si elegimos 3 votantes con reemplazamiento, calcula la probabilidad de que al menos uno de ellos haya votado a Rupérez.",
     r"$X\sim B(3;\ 0{,}62)$: \ $P(X\geq1)=1-P(X=0)=1-0{,}38^3=" + B(ro) + "$."),
 (2, r"\pau{Andalucía, PAU extraordinaria 2026 (adaptado)} Sean $A$ y $B$ dos sucesos de un mismo experimento aleatorio con $P(A)=0{,}65$, $P(B)=0{,}55$ y $P(A\cap B)=0{,}35$." + tasks(1, [
      r"Calcula la probabilidad de que ocurra al menos uno y la probabilidad de que ocurra $B$, sabiendo que no ha ocurrido $A$.", r"El experimento se realiza 11 veces. Calcula la probabilidad de que el suceso $B$ ocurra exactamente 8 veces y el número esperado de veces que ocurre $B$."]),
     tasks(1, [r"$P(A\cup B)=0{,}65+0{,}55-0{,}35=" + B(an[0], 2) + r"$; \ $P(B|\overline A)=\frac{0{,}55-0{,}35}{0{,}35}=\frac47\approx" + B(an[1]) + "$",
               r"$X\sim B(11;\ 0{,}55)$: \ $P(X=8)=\binom{11}{8}0{,}55^8\,0{,}45^3=" + B(an[2]) + r"$; \ $\mu=11\cdot0{,}55=6{,}05$: se espera que ocurra unas \rest{6 veces}."])),
 (1, r"\pau{País Vasco, EAU extraordinaria 2023} Un jugador $A$ hace lanzamientos con una moneda equilibrada y otro jugador $B$, con una moneda trucada en la que la probabilidad de cara es $0{,}4$. Sean $X$ el número de caras de $A$ e $Y$ el número de cruces de $B$." + tasks(1, [
      r"Calcula la probabilidad de que el jugador $A$ obtenga 3 caras en 3 lanzamientos.", r"Calcula la probabilidad de que el jugador $B$ obtenga 2 cruces en 2 lanzamientos."]),
     tasks(1, [r"$X\sim B(3;\ 0{,}5)$: \ $P(X=3)=0{,}5^3=" + B(pv[0], 3) + "$", r"$Y\sim B(2;\ 0{,}6)$ (cruz: $1-0{,}4$): \ $P(Y=2)=0{,}6^2=" + B(pv[1], 2) + "$"])),
 (2, r"\pau{Castilla y León, PAU ordinaria 2026} El 90\,\% de los jóvenes de entre 25 y 34 años compra por Internet. Una tienda hace una encuesta a 10 clientes jóvenes." + tasks(1, [
      r"Calcula la probabilidad de que exactamente 2 de los 10 clientes no hagan compras en línea.", r"Calcula la probabilidad de que menos de 2 clientes no hagan compras en línea."]),
     r"$X=$ «número de clientes que no compran en línea» $\sim B(10;\ 0{,}1)$ (no está en la tabla de la PAU: $n=10$)." + tasks(1, [r"$P(X=2)=\binom{10}{2}0{,}1^2\,0{,}9^8=" + B(cy[0]) + "$",
      r"$P(X<2)=P(X=0)+P(X=1)=0{,}9^{10}+10\cdot0{,}1\cdot0{,}9^9=" + B(cy[1]) + "$"])),
 (2, r"\pau{Canarias, EBAU ordinaria 2022} Una compañía de seguros tiene asegurados 2500 coches, 560 autobuses y 220 motos. Para una inspección se eligen al azar las pólizas de 10 de los vehículos asegurados. ¿Cuál es la probabilidad de que entre los vehículos elegidos haya al menos dos autobuses?",
     r"Hay $3280$ vehículos y $p=\frac{560}{3280}\approx0{,}1707$. Como hay muchos vehículos, $X\sim B(10;\ 0{,}1707)$ aproximadamente: $P(X\geq2)=1-P(X=0)-P(X=1)=1-0{,}8293^{10}-10\cdot0{,}1707\cdot0{,}8293^9\approx" + B(cg) + "$."),
 (2, r"¿Cuántas veces, como mínimo, hay que lanzar una moneda para que la probabilidad de obtener al menos una cara sea mayor que $0{,}99$?",
     r"$P(\text{al menos una cara})=1-0{,}5^n>0{,}99\iff0{,}5^n<0{,}01\iff2^n>100$. Como $2^6=64$ y $2^7=128$: \ $\res{n=7}$ lanzamientos."),
]))
ck(2 ** 7 > 100 and 2 ** 6 < 100, 1)

# =====================================================================
# 3. Amb la taula
b5 = [pmf(5, .25, 2), pmf(5, .25, 0) + pmf(5, .25, 1), pmf(5, .25, 4) + pmf(5, .25, 5), 1 - pmf(5, .25, 0)]
b9 = [sum(pmf(9, 1 / 3, k) for k in range(3)), 1 - sum(pmf(9, 1 / 3, k) for k in range(3))]
b7 = [pmf(7, .2, 1), pmf(7, .2, 0) + pmf(7, .2, 1), 1 - pmf(7, .2, 0) - pmf(7, .2, 1)]
b8 = [pmf(8, .1, 0), pmf(8, .1, 0) + pmf(8, .1, 1), pmf(8, .1, 1)]
b6 = sum(pmf(6, .25, k) for k in range(3, 7))
b12 = pmf(12, .2, 3)
def r4(x): return round(x, 4)
S.append(("La distribución binomial con la tabla de la PAU", [
 (1, r"Sea $X\sim B(5;\ 0{,}25)$. Calcula con la tabla de la PAU:" + tasks(4, [r"$P(X=2)$", r"$P(X\leq1)$", r"$P(X\geq4)$", r"$P(X>0)$"])
     + recorda(r"la tabla da $P(X=x)$ para $n\leq9$. Para las acumuladas, suma casillas de la misma columna o haz el contrario."),
     r"Bloque $n=5$, columna $p=0{,}25$:" + tasks(2, [r"$" + B(r4(b5[0])) + "$", r"$0{,}2373+0{,}3955=" + B(r4(pmf(5, .25, 0)) + r4(pmf(5, .25, 1))) + "$", r"$0{,}0146+0{,}0010=" + B(r4(pmf(5, .25, 4)) + r4(pmf(5, .25, 5))) + "$", r"$1-0{,}2373=" + B(1 - r4(pmf(5, .25, 0))) + "$"])),
 (1, r"Sea $X\sim B\left(9,\frac13\right)$. Calcula con la tabla $P(X\leq2)$ y $P(X\geq3)$.",
     r"Bloque $n=9$, columna $p=1/3$: \ $P(X\leq2)=0{,}0260+0{,}1171+0{,}2341=" + B(r4(pmf(9, 1/3, 0)) + r4(pmf(9, 1/3, 1)) + r4(pmf(9, 1/3, 2))) + r"$; \ $P(X\geq3)=1-0{,}3772=" + B(1 - (r4(pmf(9, 1/3, 0)) + r4(pmf(9, 1/3, 1)) + r4(pmf(9, 1/3, 2)))) + "$."),
 (2, r"El 80\,\% de los clientes de una tienda está satisfecho con la atención recibida. Se eligen 7 clientes al azar. Calcula, con la tabla de la PAU, la probabilidad de que:" + tasks(1, [r"estén satisfechos exactamente 6;", r"estén satisfechos al menos 6;", r"estén satisfechos como mucho 5."]),
     r"$X\sim B(7;\ 0{,}8)$ no está en la tabla ($p>0{,}5$). Contamos los no satisfechos: $Y=7-X\sim B(7;\ 0{,}2)$." + tasks(1, [r"$P(X=6)=P(Y=1)=" + B(r4(b7[0])) + "$", r"$P(X\geq6)=P(Y\leq1)=0{,}2097+0{,}3670=" + B(r4(pmf(7, .2, 0)) + r4(pmf(7, .2, 1))) + "$",
      r"$P(X\leq5)=1-P(X\geq6)=" + B(1 - r4(pmf(7, .2, 0)) - r4(pmf(7, .2, 1))) + "$"])),
 (2, r"Germina el 90\,\% de las semillas de una marca. Se plantan 8 semillas. Calcula, con la tabla, la probabilidad de que germinen todas, de que germinen al menos 7 y de que germinen exactamente 7.",
     r"$Y=$ «semillas que no germinan» $\sim B(8;\ 0{,}1)$: \ $P(\text{todas})=P(Y=0)=" + B(r4(b8[0])) + r"$; \ $P(X\geq7)=P(Y\leq1)=0{,}4305+0{,}3826=" + B(r4(pmf(8, .1, 0)) + r4(pmf(8, .1, 1))) + r"$; \ $P(X=7)=P(Y=1)=" + B(r4(b8[2])) + "$."),
 (2, r"Un test tiene 6 preguntas con 4 opciones cada una, de las que solo una es correcta. Se aprueba acertando al menos 3. Un alumno contesta todas las preguntas al azar. ¿Cuál es la probabilidad de que apruebe?",
     r"$X\sim B(6;\ 0{,}25)$; bloque $n=6$, columna $0{,}25$: \ $P(X\geq3)=0{,}1318+0{,}0330+0{,}0044+0{,}0002=" + B(sum(r4(pmf(6, .25, k)) for k in range(3, 7))) + "$."),
 (2, r"Sea $X\sim B(12;\ 0{,}2)$. ¿Se puede calcular $P(X=3)$ con la tabla de la PAU? Calcúlala.",
     r"\rest{No}: la tabla solo llega hasta $n=9$. Con la fórmula: $P(X=3)=\binom{12}{3}0{,}2^3\,0{,}8^9=220\cdot0{,}008\cdot0{,}1342=" + B(b12) + "$."),
]))
ck(r4(pmf(5, .25, 0)), .2373); ck(r4(pmf(9, 1/3, 1)), .1171); ck(r4(pmf(7, .2, 1)), .3670); ck(r4(pmf(8, .1, 1)), .3826); ck(r4(pmf(6, .25, 3)), .1318)

# =====================================================================
# 4. Normal típica
z4 = [Phi(1.53), 1 - Phi(2.05), Phi(-0.82), 1 - Phi(-1.2), Phi(1.5) - Phi(0.75), Phi(1) - Phi(-2), 2 * Phi(2.58) - 1]
S.append(("La normal tipificada $N(0,1)$ y su tabla", [
 (1, r"Si $Z\sim N(0,1)$, calcula con la tabla de la PAU:" + tasks(4, [r"$P(Z\leq1{,}53)$", r"$P(Z>2{,}05)$", r"$P(Z<-0{,}82)$", r"$P(Z\geq-1{,}2)$", r"$P(0{,}75\leq Z\leq1{,}5)$", r"$P(-2< Z<1)$", r"$P(|Z|\leq2{,}58)$"])
     + recorda(r"la tabla da $P(Z\leq z)$ para $z\geq0$. \ $P(Z\geq z)=1-P(Z\leq z)$, \ $P(Z\leq-z)=1-P(Z\leq z)$."),
     tasks(2, [r"$" + B(z4[0]) + "$", r"$1-0{,}9798=" + B(z4[1]) + "$", r"$1-0{,}7939=" + B(z4[2]) + "$", r"$P(Z\leq1{,}2)=" + B(z4[3]) + "$", r"$0{,}9332-0{,}7734=" + B(z4[4]) + "$",
               r"$0{,}8413-(1-0{,}9772)=" + B(z4[5]) + "$", r"$2\cdot0{,}9951-1=" + B(z4[6]) + "$"])),
 (2, r"Si $Z\sim N(0,1)$, halla el valor de $k$ en cada caso:" + tasks(2, [r"$P(Z\leq k)=0{,}8907$", r"$P(Z\geq k)=0{,}0505$", r"$P(Z\leq k)=0{,}25$", r"$P(-k\leq Z\leq k)=0{,}9$"])
     + recorda(r"busca la probabilidad \emph{dentro} de la tabla; si es menor que 0,5, $k$ es negativo."),
     tasks(1, [r"El valor está en la tabla: $\res{k=1{,}23}$", r"$P(Z\leq k)=0{,}9495\Rightarrow\res{k=1{,}64}$", r"$P(Z\leq-k)=0{,}75$: más próximo $0{,}7486\to0{,}67$, así que $\res{k\approx-0{,}67}$",
               r"$2P(Z\leq k)-1=0{,}9\Rightarrow P(Z\leq k)=0{,}95$: entre $1{,}64$ y $1{,}65$, $\res{k\approx1{,}645}$"])),
]))
ck(z4[0], .937); ck(z4[1], .0202); ck(z4[2], .2061); ck(z4[3], .8849); ck(z4[4], .1598); ck(z4[5], .8185); ck(z4[6], .9902)
ck(zinv(.8907), 1.23); ck(zinv(.9495), 1.64); ck(zinv(.25), -.67); ck(zinv(.95), 1.645)

# =====================================================================
# 5. Tipificació: problemes directes
def N2(x): return r'\res{%s}' % d4(x)
q = {}
q['b25'] = [Phi(zs(25, 15, 10)), Phi(zs(25, 15, 10)) - Phi(zs(5, 15, 10))]; ck(q['b25'][0], .8413); ck(q['b25'][1], .6826)
q['b21'] = [1 - Phi(zs(80, 70, 15)), Phi(zs(50, 70, 15)), Phi(zs(120, 70, 15)) - Phi(zs(60, 70, 15))]; ck(q['b21'][0], .2514); ck(q['b21'][1], .0918); ck(q['b21'][2], .7482)
q['b23'] = [0.5, 1 - Phi(zs(1.76, 1.62, .11))]; ck(q['b23'][1], .102, 1e-4)
q['c17'] = [1 - Phi(zs(36, 32, 10)), Phi(zs(35, 32, 10)) - Phi(zs(28, 32, 10))]; ck(q['c17'][0], .3446); ck(q['c17'][1], .2733)
q['cl21'] = 1 - Phi(zs(9, 6.8, 1.1)); ck(q['cl21'], .0228)
q['cl20'] = Phi(zs(4, 32, 12.5)); ck(q['cl20'], .0125)
q['cl19'] = [1 - Phi(zs(90, 74, 8)), 1 - Phi(zs(4, 5, 2))]; ck(q['cl19'][0], .0228); ck(q['cl19'][1], .6915)
q['pv20'] = [1 - Phi(zs(7, 6.2, 2)), Phi(zs(8, 6.2, 2)) - Phi(zs(5, 6.2, 2))]; ck(q['pv20'][0], .3446); ck(q['pv20'][1], .5416)
q['pv20b'] = [Phi(zs(75, 60, 10)), 1 - Phi(zs(80, 60, 10))]; ck(q['pv20b'][0], .9332); ck(q['pv20b'][1], .0228)
q['pv20c'] = [1 - Phi(zs(171, 163, 7)), Phi(zs(171, 163, 7)) - Phi(zs(155, 163, 7))]; ck(q['pv20c'][0], .1271); ck(q['pv20c'][1], .7458)
q['cl18'] = 1 - Phi(zs(1740, 1200, 400)); ck(q['cl18'], .0885)
q['c19'] = [1 - Phi(zs(62, 44, 18)), Phi(zs(40, 44, 18)), Phi(zs(30, 44, 18)) - Phi(zs(18, 44, 18))]; ck(250 * q['c19'][0], 40, 0.5); ck(250 * q['c19'][1], 103, 0.5); ck(250 * q['c19'][2], 37, 1.5)
q['c19j'] = Phi(zs(100, 89, 20)) - Phi(zs(86, 89, 20)); ck(q['c19j'], .2684)
q['c24'] = [Phi(zs(700, 725, 50)), Phi(zs(710, 725, 50))]; ck(q['c24'][0], .3085); ck(25 * q['c24'][1], 9.55, 0.01)
q['b24'] = [1 - Phi(zs(60, 79.6, 10)), Phi(zs(70, 79.6, 10)) - Phi(zs(60, 79.6, 10))]; ck(q['b24'][0], .975); ck(q['b24'][1], .1435)
def tip(x, m, s): return r'\frac{%s-%s}{%s}' % (dec(x, 3), dec(m, 3), dec(s, 3))
S.append(("Tipificación: problemas con la normal", [
 (1, r"\pau{Islas Baleares, PBAU extraordinaria 2025} Cuando un cliente entra en una tienda de electrodomésticos, el tiempo (en minutos) que pasa en ella sigue una distribución $N(15,10)$." + tasks(1, [
      r"¿Cuál es la probabilidad de que un cliente esté dentro de la tienda 25 minutos o menos?", r"¿Cuál es la probabilidad de que un cliente esté dentro de la tienda entre 5 y 25 minutos?"])
     + recorda(r"si $X\sim N(\mu,\sigma)$, entonces $Z=\dfrac{X-\mu}{\sigma}\sim N(0,1)$. Redondea $z$ a dos decimales y usa la tabla."),
     tasks(1, [r"$P(X\leq25)=P\left(Z\leq\frac{25-15}{10}\right)=P(Z\leq1)=" + N2(q['b25'][0]) + "$", r"$P(-1\leq Z\leq1)=2\cdot0{,}8413-1=" + N2(q['b25'][1]) + "$"])
     + cen(gauss([(-1, 1)], [(-1, '-1'), (0, '0'), (1, '1')]))),
 (1, r"\pau{Islas Baleares, PBAU ordinaria 2021} El peso de las personas de un colegio mayor sigue una ley normal de media 70 kg y desviación típica 15 kg. Elegimos una persona al azar; calcula la probabilidad de que:" + tasks(3, [r"pese más de 80 kg;", r"pese menos de 50 kg;", r"pese entre 60 y 120 kg."]),
     tasks(1, [r"$P(Z>0{,}67)=1-0{,}7486=" + N2(q['b21'][0]) + "$", r"$P(Z<-1{,}33)=1-0{,}9082=" + N2(q['b21'][1]) + "$", r"$P(-0{,}67< Z<3{,}33)=0{,}9996-0{,}2514=" + N2(q['b21'][2]) + "$"])),
 (2, r"\pau{Islas Baleares, PBAU extraordinaria 2023} En una población, la altura de los hombres sigue una normal de media 1,76 m y desviación típica 0,12 m, y la de las mujeres, una normal de media 1,62 m y desviación típica 0,11 m." + tasks(1, [
      r"Elegimos un hombre al azar. ¿Cuál es la probabilidad de que su altura sea mayor o igual que 1,76 m?", r"Elegimos una mujer al azar. ¿Cuál es la probabilidad de que su altura sea mayor o igual que 1,76 m?", r"¿Qué es más probable, que un hombre mida menos de 1,76 m o que lo haga una mujer?"]),
     tasks(1, [r"1,76 es la media de los hombres: $\res{0{,}5}$", r"$P\left(Z\geq\frac{1{,}76-1{,}62}{0{,}11}\right)=P(Z\geq1{,}27)=1-0{,}8980=" + N2(q['b23'][1]) + "$",
               r"Hombre: $0{,}5$; mujer: $1-0{,}102=0{,}898$. \rest{Es más probable que una mujer mida menos de 1,76 m.}"])),
 (1, r"\pau{Canarias, EBAU junio 2017} El gasto mensual en agua de las familias de cuatro miembros sigue una normal de media 32 euros y desviación típica 10 euros. Calcula la probabilidad de que el gasto mensual de una de estas familias:" + tasks(1, [r"sea mayor que 36 euros;", r"esté entre 28 y 35 euros."]),
     tasks(1, [r"$P(Z>0{,}4)=1-0{,}6554=" + N2(q['c17'][0]) + "$", r"$P(-0{,}4< Z<0{,}3)=0{,}6179-(1-0{,}6554)=" + N2(q['c17'][1]) + "$"])),
 (1, r"\pau{Castilla y León, EBAU extraordinaria 2021} La nota media de los alumnos de segundo de Bachillerato de un instituto sigue una normal de media 6,8 y desviación típica 1,1. Calcula la probabilidad de que un alumno haya obtenido más de un 9.",
     r"$P(X>9)=P\left(Z>\frac{9-6{,}8}{1{,}1}\right)=P(Z>2)=1-0{,}9772=" + N2(q['cl21']) + "$."),
 (1, r"\pau{Castilla y León, EBAU ordinaria 2020} La vida útil sin averías de un nuevo modelo de móvil (en meses) sigue una normal de media 32 y desviación típica 12,5. La campaña de lanzamiento ofrece cambiar gratuitamente el móvil si se avería en los primeros 4 meses. Calcula la probabilidad de que haya que sustituir un móvil.",
     r"$P(X<4)=P\left(Z<\frac{4-32}{12{,}5}\right)=P(Z<-2{,}24)=1-0{,}9875=" + N2(q['cl20']) + "$."),
 (1, r"\pau{Castilla y León, EBAU julio 2019 y junio 2019}" + tasks(1, [r"El tiempo de resolución de un examen sigue una normal de media 74 minutos y desviación típica 8 minutos. ¿Cuál es la probabilidad de necesitar más de los 90 minutos disponibles?",
      r"El tiempo que tarda un fumador en dejar de fumar sigue una normal de media 5 meses y desviación típica 2 meses. ¿Cuál es la probabilidad de que un fumador tarde más de 4 meses?"]),
     tasks(1, [r"$P(Z>2)=" + N2(q['cl19'][0]) + "$", r"$P(Z>-0{,}5)=P(Z<0{,}5)=" + N2(q['cl19'][1]) + "$"])),
 (1, r"\pau{País Vasco, EAU extraordinaria 2020} Las notas de un grupo en una asignatura siguen una normal de media 6,2 puntos y desviación típica 2 puntos. Se elige un estudiante al azar. Calcula la probabilidad de que su nota sea superior a 7 y la probabilidad de que esté entre 5 y 8 puntos.",
     r"$P(Z>0{,}4)=1-0{,}6554=" + N2(q['pv20'][0]) + r"$; \ $P(-0{,}6< Z<0{,}9)=0{,}8159-0{,}2743=" + N2(q['pv20'][1]) + "$." + cen(gauss([(-0.6, 0.9)], [(-0.6, '-0{,}6'), (0.9, '0{,}9')]))),
 (1, r"\pau{País Vasco, EAU extraordinaria 2020} El tiempo que necesitan los alumnos para terminar un examen sigue una normal de media 60 minutos y desviación típica 10 minutos. Si se dan 75 minutos, ¿qué proporción de alumnos lo terminará? ¿Y si se dan 80, qué proporción no lo terminará?",
     r"$P(X\leq75)=P(Z\leq1{,}5)=" + N2(q['pv20b'][0]) + r"$ \ (el $93{,}32\,\%$); \ $P(X>80)=P(Z>2)=" + N2(q['pv20b'][1]) + r"$ \ (el $2{,}28\,\%$)."),
 (1, r"\pau{País Vasco, EAU ordinaria 2020} La altura de las mujeres de un país sigue una normal de media 163 cm y desviación típica 7 cm. ¿Cuál es la probabilidad de que una mujer elegida al azar mida más de 171 cm? ¿Y de que mida entre 155 y 171 cm?",
     r"$z=\frac{171-163}{7}\approx1{,}14$: \ $P(Z>1{,}14)=1-0{,}8729=" + N2(q['pv20c'][0]) + r"$; \ $P(-1{,}14< Z<1{,}14)=2\cdot0{,}8729-1=" + N2(q['pv20c'][1]) + "$."),
 (1, r"\pau{Castilla y León, EBAU julio 2018} El salario mensual de los trabajadores de una empresa sigue una normal de media 1200 euros y desviación típica 400 euros. ¿Cuál es la probabilidad de que un trabajador cobre más de 1740 euros al mes?",
     r"$P\left(Z>\frac{540}{400}\right)=P(Z>1{,}35)=1-0{,}9115=" + N2(q['cl18']) + "$."),
 (2, r"\pau{Canarias, EBAU julio 2019} En una empresa hay 250 empleados. Su edad sigue una normal de media 44 años y desviación típica 18 años." + tasks(1, [
      r"¿Cuántos empleados se espera que tengan más de 62 años?", r"¿Cuántos empleados se espera que tengan menos de 40 años?", r"¿Cuántos empleados podrían conseguir el carné joven de transporte si el requisito es ser mayor de edad y no haber cumplido los 30 años?"]),
     r"Multiplicamos cada probabilidad por el total de empleados:" + tasks(1, [r"$P(Z>1)=0{,}1587$; \ $250\cdot0{,}1587\approx\res{40}$ empleados.", r"$P(Z<-0{,}22)=1-0{,}5871=0{,}4129$; \ $250\cdot0{,}4129\approx\res{103}$ empleados.",
      r"$P(18\leq X<30)=P(-1{,}44\leq Z<-0{,}78)=(1-0{,}7823)-(1-0{,}9251)=0{,}1428$; \ $250\cdot0{,}1428\approx\res{36}$ empleados."])),
 (1, r"\pau{Canarias, EBAU junio 2019} El peso de los jóvenes de una región que padecen diabetes de tipo 2 sigue una normal de media 89 kg y desviación típica 20 kg. ¿Qué porcentaje de estos jóvenes pesa entre 86 y 100 kg?",
     r"$P(-0{,}15< Z<0{,}55)=0{,}7088-(1-0{,}5596)=" + N2(q['c19j']) + r"$: \ el $\res{26{,}84\,\%}$."),
 (2, r"\pau{Canarias, EBAU extraordinaria 2024} En una ciudad, el alquiler mensual de los pisos de dos habitaciones sigue una normal de media 725 euros y desviación típica 50 euros." + tasks(1, [
      r"¿Cuál es la probabilidad de que alquilar uno de estos pisos cueste, como mucho, 700 euros al mes?", r"Una agencia inmobiliaria alquila 25 de estos pisos. ¿Cuántos se espera que cuesten menos de 710 euros al mes?"]),
     tasks(1, [r"$P(Z\leq-0{,}5)=1-0{,}6915=" + N2(q['c24'][0]) + "$", r"$P(Z<-0{,}3)=1-0{,}6179=0{,}3821$; \ $25\cdot0{,}3821\approx9{,}55$: se espera que sean \rest{entre 9 y 10}."])),
 (2, r"\pau{Islas Baleares, PBAU ordinaria 2024} Según el INE, la esperanza de vida de una persona nacida en 2020 es de 79,6 años para los hombres y de 83,6 años para las mujeres. Supongamos que el número de años que vivirá una persona nacida en 2020 sigue una normal de desviación típica 10 años, tanto para los hombres como para las mujeres." + tasks(1, [
      r"¿Cuál es la probabilidad de que un hombre nacido en 2020 viva más de 60 años? ¿Y de que viva entre 60 y 70 años?", r"¿Qué es más probable: que un hombre nacido en 2020 viva más de 89,6 años, o que una mujer nacida en 2020 viva más de 93,6 años?"]),
     tasks(1, [r"$P(Z>-1{,}96)=" + N2(q['b24'][0]) + r"$; \ $P(-1{,}96< Z<-0{,}96)=(1-0{,}8315)-(1-0{,}9750)=" + N2(q['b24'][1]) + "$",
               r"Hombre: $P\left(Z>\frac{10}{10}\right)=P(Z>1)$; mujer: $P\left(Z>\frac{10}{10}\right)=P(Z>1)$. \rest{Son igual de probables} ($0{,}1587$)."])),
]))

# =====================================================================
# 6. Problemes inversos
def inv_up(m, s, p): z = zinv(1 - p); return z, m + z * s   # valor superat pel p de la població
iq = {}
z, k = inv_up(116, 42, 0.10); iq['ba26'] = (Phi(zs(200, 116, 42)) - Phi(zs(100, 116, 42)), z, k); ck(iq['ba26'][0], .6252); ck(k, 169.76, 1e-6)
z, k = inv_up(6.2, 2, .25); iq['pv20'] = (z, k); ck(z, .67); ck(k, 7.55, .02)
zq = zinv(.75); iq['pv20q'] = (163 - zq * 7, 163 + zq * 7); ck(iq['pv20q'][0], 158.275, .05)
z, k = inv_up(250, 50, .4); iq['tr'] = (z, k, 6000 * (1 - Phi(zs(280, 250, 50)))); ck(k, 262.5); ck(iq['tr'][2], 1646, 1)
z1 = zinv(.2); z2 = zinv(.85); iq['pv19'] = (z1, 68 + z1 * 18, z2, 68 + z2 * 18); ck(iq['pv19'][1], 52.79, .1); ck(iq['pv19'][3], 86.63, .1)
za = zinv(.75); iq['car'] = (za, 6.8 + za * .6, 7 + za * .5); ck(iq['car'][1], 7.205, .01); ck(iq['car'][2], 7.3375, .01)
z, k = inv_up(5.8, 2.6, .2); iq['pv24'] = (z, k, Phi(-zs(5, 5.8, 2.6))); ck(k, 7.997, .02); ck(iq['pv24'][2], .6217)
zp = zinv(.7); sp = .8 / zp; z, k = inv_up(6.8, 1.5, .2); iq['pv22'] = (zp, sp, k, 1 - Phi(zs(5, 6.8, 1.5))); ck(sp, 1.5238, .02); ck(k, 8.0675, .01); ck(iq['pv22'][3], .8849)
zr = zinv(.84134); iq['lr24'] = (zr, 1 / zr, 6 + zinv(.975) * 1); ck(1 / zr, 1); ck(iq['lr24'][2], 7.96)
zr = zinv(.88493); iq['lr23'] = (zr, 183 - zr * 6.5, 183 - 2 * zr * 6.5); ck(iq['lr23'][1], 175.2); ck(iq['lr23'][2], 167.4)
iq['lr21'] = (1 - Phi(zs(190, 174, 8)), 190 - zinv(1 - .15866) * 8); ck(iq['lr21'][0], .0228); ck(iq['lr21'][1], 182)
zc = zinv(.8023); iq['cl18'] = (zc, 170 / zc); ck(iq['cl18'][1], 200)
zc = zinv(.6915); iq['cl26'] = (zc, 25 / zc, 1 - Phi(zs(400, 275, 25 / zc))); ck(iq['cl26'][1], 50); ck(iq['cl26'][2], .0062)
S.append(("Problemas inversos", [
 (2, r"\pau{Islas Baleares, PAU extraordinaria 2026} El tiempo que cada joven de una población dedica cada día a las redes sociales sigue una normal de media 116 minutos y desviación típica 42 minutos." + tasks(1, [
      r"¿Qué proporción de jóvenes dedica entre 100 y 200 minutos a las redes sociales?", r"Juan está en el 10\,\% de jóvenes que más tiempo les dedica. ¿Cuántos minutos les dedica, como mínimo?"])
     + recorda(r"en un problema inverso buscamos la probabilidad dentro de la tabla, leemos $z$ y deshacemos la tipificación: $x=\mu+z\,\sigma$."),
     tasks(1, [r"$P(-0{,}38< Z<2)=0{,}9772-(1-0{,}6480)=" + N2(iq['ba26'][0]) + r"$: el $62{,}52\,\%$.",
               r"$P(X\geq k)=0{,}1\Rightarrow P(Z\leq z)=0{,}9$: más próximo $0{,}8997\to z=1{,}28$; \ $k=116+1{,}28\cdot42=\res{169{,}76}$ minutos."]) + cen(gauss([(1.28, None)], [(0, '0'), (1.28, '1{,}28')]))),
 (2, r"\pau{País Vasco, EAU extraordinaria 2020} Las notas de un grupo siguen una normal de media 6,2 y desviación típica 2. Si el 25\,\% del alumnado con mejor nota obtuvo la calificación de sobresaliente, ¿cuál es la nota mínima para obtenerla?",
     r"$P(Z\leq z)=0{,}75$: más próximo $0{,}7486\to z=0{,}67$; \ $6{,}2+0{,}67\cdot2=\res{7{,}54}$."),
 (2, r"\pau{País Vasco, EAU ordinaria 2020} La altura de las mujeres de un país sigue una normal de media 163 cm y desviación típica 7 cm. Una empresa de disfraces quiere hacer cuatro tallas, cada una adecuada para el 25\,\% de las mujeres. ¿Qué alturas marcan el paso de una talla a otra?",
     r"Son los cuartiles: $z=\pm0{,}67$ (para $0{,}75$) y $z=0$. \ $163-0{,}67\cdot7=\res{158{,}31}$, \ $\res{163}$ \ y \ $163+0{,}67\cdot7=\res{167{,}69}$ cm."),
 (2, r"\pau{País Vasco, EAU ordinaria 2020} El peso de las truchas de una piscifactoría sigue una normal de media 250 g y desviación típica 50 g. Solo son aptas para la venta las que superan un peso determinado." + tasks(1, [
      r"¿Cuál debe ser ese peso si se quiere que el 40\,\% de las truchas sean aptas para la venta?", r"Si ese peso se establece en 280 g y en la piscifactoría hay 6000 truchas, ¿cuántas se podrán vender?"]),
     tasks(1, [r"$P(Z\leq z)=0{,}6$: más próximo $0{,}5987\to z=0{,}25$; \ $250+0{,}25\cdot50=\res{262{,}5}$ g", r"$P(Z>0{,}6)=1-0{,}7257=0{,}2743$; \ $6000\cdot0{,}2743\approx\res{1646}$ truchas"])),
 (2, r"\pau{País Vasco, EAU julio 2019} Las puntuaciones de una prueba de cultura general siguen una normal de media 68 y desviación típica 18. Se quiere clasificar a los habitantes en tres grupos (cultura baja, aceptable y excelente) de manera que el primer grupo tenga el 20\,\% de la población, el segundo el 65\,\% y el tercero el 15\,\% restante. ¿Qué puntuaciones marcan el paso de un grupo a otro?",
     r"Primer corte: $P(Z\leq z_1)=0{,}2\Rightarrow z_1\approx-0{,}84$ (buscamos $0{,}8$: $0{,}7995$); \ $68-0{,}84\cdot18=\res{52{,}88}$. \ Segundo corte: $P(Z\leq z_2)=0{,}85$: más próximo $0{,}8508\to z_2=1{,}04$; \ $68+1{,}04\cdot18=\res{86{,}72}$."),
 (2, r"\pau{País Vasco, EAU julio 2019 y PAU ordinaria 2025} La nota de acceso del alumnado preinscrito en el grado A sigue una normal $N(6{,}8;\ 0{,}6)$, y la del grado B, una $N(7;\ 0{,}5)$. En ambos casos solo se admite al 25\,\% del alumnado con mejores notas." + tasks(1, [
      r"¿Qué grado requerirá una nota mínima más baja?", r"Yolanda ha sacado un 7,25 y Teresa un 7,45. ¿A qué grados tendrán opción de acceso?"]),
     r"$P(Z\leq z)=0{,}75\Rightarrow z\approx0{,}67$." + tasks(1, [r"A: $6{,}8+0{,}67\cdot0{,}6=7{,}202$; \ B: $7+0{,}67\cdot0{,}5=7{,}335$. \rest{El grado A pide una nota mínima más baja.}",
      r"Yolanda ($7{,}25$) \rest{solo puede entrar en A}; Teresa ($7{,}45$) \rest{puede entrar en los dos}."])),
 (2, r"\pau{País Vasco, EAU ordinaria 2024} La puntuación de un examen de Matemáticas Aplicadas a las Ciencias Sociales sigue una normal de media 5,8 puntos y desviación típica 2,6 puntos." + tasks(1, [
      r"¿Qué puntuación es superada únicamente por el 20\,\% del alumnado?", r"Si el apto se obtiene con una puntuación igual o superior a 5, ¿qué porcentaje del alumnado ha sido apto?"]),
     tasks(1, [r"$P(Z\leq z)=0{,}8$: más próximo $0{,}7995\to z=0{,}84$; \ $5{,}8+0{,}84\cdot2{,}6=\res{7{,}984}$", r"$P(Z\geq-0{,}31)=P(Z\leq0{,}31)=" + N2(iq['pv24'][2]) + r"$: el $62{,}17\,\%$"])),
 (2, r"\pau{País Vasco, EAU ordinaria 2022} En el examen de Inglés, el 30\,\% del alumnado obtuvo una puntuación superior a 7,6 puntos. La puntuación sigue una normal de media 6,8 puntos." + tasks(1, [
      r"Calcula la desviación típica de la puntuación.", r"Si la desviación típica es de 1,5 puntos, ¿qué puntuación es superada únicamente por el 20\,\% del alumnado?", r"Si la desviación típica es de 1,5 puntos y se aprueba con un 5 o más, ¿qué porcentaje ha aprobado?"]),
     tasks(1, [r"$P\left(Z\leq\frac{0{,}8}{\sigma}\right)=0{,}7$: más próximo $0{,}6985\to0{,}52$; \ $\sigma=\frac{0{,}8}{0{,}52}\approx\res{1{,}54}$", r"$6{,}8+0{,}84\cdot1{,}5=\res{8{,}06}$",
               r"$P(Z\geq-1{,}2)=P(Z\leq1{,}2)=" + N2(iq['pv22'][3]) + r"$: el $88{,}49\,\%$"])),
 (2, r"\pau{La Rioja, EBAU ordinaria 2024} Las valoraciones de un producto siguen una normal de media $\mu$ y desviación típica $\sigma$. El porcentaje de valoraciones superiores a 7 coincide con el de valoraciones inferiores a 5." + tasks(1, [
      r"¿Por qué podemos deducir que $\mu=6$?", r"Si este porcentaje es del 15,866\,\%, ¿cuál es el valor de $\sigma$?", r"¿Qué valor es superado solo por el 2,5\,\% de las valoraciones?"]),
     tasks(1, [r"Por la simetría de la normal respecto de $\mu$, 5 y 7 están a la misma distancia de la media: $\mu=\frac{5+7}{2}=\res{6}$.",
               r"$P\left(Z\leq\frac1\sigma\right)=0{,}84134\approx0{,}8413\Rightarrow\frac1\sigma=1\Rightarrow\res{\sigma=1}$", r"$P(Z\leq z)=0{,}975\Rightarrow z=1{,}96$; \ $6+1{,}96=\res{7{,}96}$"])),
 (2, r"\pau{La Rioja, EBAU ordinaria 2023} La estatura de los policías de Francia sigue una normal de desviación típica 6,5 cm, de manera que el 11,507\,\% mide más de 183 cm." + tasks(1, [
      r"Calcula la media de la estatura.", r"Halla la estatura que es superada por el 88,493\,\% de los policías."]),
     tasks(1, [r"$P\left(Z\leq\frac{183-\mu}{6{,}5}\right)=0{,}88493\approx0{,}8849\Rightarrow\frac{183-\mu}{6{,}5}=1{,}2\Rightarrow\res{\mu=175{,}2}$ cm",
               r"Por simetría, $z=-1{,}2$: \ $175{,}2-1{,}2\cdot6{,}5=\res{167{,}4}$ cm"])),
 (2, r"\pau{La Rioja, EBAU extraordinaria 2021} La estatura de los hombres adultos españoles sigue una normal de media 174 cm y desviación típica 8 cm." + tasks(1, [
      r"¿Cuál es la probabilidad de que un hombre adulto español mida más de 190 cm?", r"Entre los hombres holandeses, la probabilidad de medir más de 190 cm (con la misma desviación típica) es 0,15866. ¿Cuál es su estatura media?"]),
     tasks(1, [r"$P(Z>2)=" + N2(iq['lr21'][0]) + "$", r"$P\left(Z\leq\frac{190-\mu}{8}\right)=0{,}84134\Rightarrow\frac{190-\mu}8=1\Rightarrow\res{\mu=182}$ cm"])),
 (2, r"\pau{Castilla y León, EBAU julio 2018} En una empresa, el salario medio mensual es de 1400 euros y el 80,23\,\% de los trabajadores cobra menos de 1570 euros. Calcula la desviación típica del salario, suponiendo que sigue una distribución normal.",
     r"$P\left(Z<\frac{170}{\sigma}\right)=0{,}8023\Rightarrow\frac{170}{\sigma}=0{,}85\Rightarrow\res{\sigma=200}$ euros."),
 (2, r"\pau{Castilla y León, PAU ordinaria 2026} El gasto mensual de los compradores en línea sigue una normal de media 275 euros." + tasks(1, [
      r"Si el 69,15\,\% de los compradores gasta menos de 300 euros al mes, determina la desviación típica del gasto.", r"Calcula la probabilidad de que un comprador gaste más de 400 euros al mes."]),
     tasks(1, [r"$P\left(Z<\frac{25}{\sigma}\right)=0{,}6915\Rightarrow\frac{25}\sigma=0{,}5\Rightarrow\res{\sigma=50}$ euros", r"$P(Z>2{,}5)=1-0{,}9938=" + N2(iq['cl26'][2]) + "$"])),
]))

# =====================================================================
# 7. Aproximació de la binomial per la normal
def aprox(n, p, lo, hi):
    m = n * p; s = math.sqrt(n * p * (1 - p))
    if lo is None: return Phi(zs(hi, m, s))
    if hi is None: return 1 - Phi(zs(lo, m, s))
    return Phi(zs(hi, m, s)) - Phi(zs(lo, m, s))
ap = [aprox(100, .2, None, 15.5), aprox(100, .2, 19.5, 20.5), aprox(100, .2, 24.5, None)]
ex = [sum(pmf(100, .2, k) for k in range(16)), pmf(100, .2, 20), sum(pmf(100, .2, k) for k in range(25, 101))]
ck(ap[0], 1 - Phi(1.13)); ck(abs(ap[0] - ex[0]) < 0.02, 1)
cn = [2500 * .1 + 560 * .08 + 220 * .16, aprox(2500, .1, 269.5, None)]; ck(cn[0], 330); ck(cn[1], .0968)
pa = [aprox(400, .5, None, 189.5), aprox(200, .6, None, 109.5)]; ck(pa[0], .1469); ck(pa[1], 1 - Phi(1.52)); ck(pa[0] > pa[1], 1)
a26 = aprox(1350, .4, 499.5, 580.5); ck(a26, .9756)
v105 = aprox(100, .5, 39.5, None); ck(v105, .9821)
ex3 = [sum(pmf(50, .3, k) for k in range(10, 21)), aprox(50, .3, 9.5, 20.5)]
S.append(("Aproximación de la binomial por la normal", [
 (1, r"Sea $X\sim B(100;\ 0{,}2)$." + tasks(1, [r"Comprueba que se puede aproximar por una normal e indica cuál.", r"Calcula aproximadamente $P(X\leq15)$, $P(X=20)$ y $P(X\geq25)$."])
     + recorda(r"si $np\geq5$ y $nq\geq5$, $B(n,p)\approx N\left(np,\sqrt{npq}\right)$. No olvides la corrección de continuidad ($\pm0{,}5$)."),
     tasks(1, [r"$np=20\geq5$, $nq=80\geq5$: \ $\res{X'\sim N(20,\,4)}$ ($\sigma=\sqrt{100\cdot0{,}2\cdot0{,}8}=4$)",
               r"$P(X\leq15)\approx P(X'\leq15{,}5)=P(Z\leq-1{,}13)=1-0{,}8708=" + N2(ap[0]) + r"$; \ $P(X=20)\approx P(19{,}5\leq X'\leq20{,}5)=P(-0{,}13\leq Z\leq0{,}13)=" + N2(ap[1]) + r"$; \ $P(X\geq25)\approx P(X'\geq24{,}5)=P(Z\geq1{,}13)=" + N2(ap[2]) + "$"])),
 (2, r"\pau{Canarias, EBAU ordinaria 2022} Una compañía de seguros tiene asegurados 2500 coches, 560 autobuses y 220 motos. Las probabilidades de tener un accidente a lo largo de un año son 0,1 para los coches, 0,08 para los autobuses y 0,16 para las motos." + tasks(1, [
      r"¿Cuántos vehículos en total se puede esperar que tengan un accidente a lo largo del próximo año?", r"¿Cuál es la probabilidad de que el año que viene tengan un accidente al menos 270 de los coches asegurados?"]),
     tasks(1, [r"Sumamos las medias $np$: $2500\cdot0{,}1+560\cdot0{,}08+220\cdot0{,}16=250+44{,}8+35{,}2=\res{330}$ vehículos",
               r"$X\sim B(2500;\ 0{,}1)\approx N(250,\,15)$: \ $P(X\geq270)\approx P(X'\geq269{,}5)=P(Z\geq1{,}3)=1-0{,}9032=" + N2(cn[1]) + "$"])),
 (2, r"\pau{País Vasco, EAU extraordinaria 2023} El jugador $A$ lanza una moneda equilibrada y el jugador $B$, una moneda trucada en la que la probabilidad de cara es $0{,}4$. ¿Qué es más probable, que el jugador $A$ obtenga menos de 190 caras en 400 lanzamientos, o que el jugador $B$ obtenga menos de 110 cruces en 200 lanzamientos? Justifica la respuesta.",
     r"$A$: $X\sim B(400;\ 0{,}5)\approx N(200,\,10)$: \ $P(X\leq189)\approx P(Z\leq\frac{189{,}5-200}{10})=P(Z\leq-1{,}05)=" + N2(pa[0]) + r"$. \ $B$: cruces $Y\sim B(200;\ 0{,}6)\approx N(120;\ \sqrt{48}\approx6{,}93)$: \ $P(Y\leq109)\approx P(Z\leq-1{,}52)=" + N2(pa[1]) + r"$. \ \rest{Es más probable el suceso del jugador $A$.}"),
 (2, r"\pau{Andalucía, PAU ordinaria 2026 (adaptado)} Un suceso tiene probabilidad $0{,}4$ y el experimento se repite 1350 veces de manera independiente. Sea $X$ el número de veces que ocurre." + tasks(1, [r"¿Qué distribución sigue $X$?", r"Calcula la probabilidad de que el suceso ocurra como mucho 580 veces, pero más de 499 veces."]),
     tasks(1, [r"$\res{X\sim B(1350;\ 0{,}4)}$", r"$\mu=540$, $\sigma=\sqrt{324}=18$: \ $P(500\leq X\leq580)\approx P(499{,}5\leq X'\leq580{,}5)=P(-2{,}25\leq Z\leq2{,}25)=2\cdot0{,}9878-1=" + N2(a26) + "$"])),
 (2, r"Sea $X\sim B(50;\ 0{,}3)$. Calcula $P(10\leq X\leq20)$ con la aproximación normal y compárala con el valor exacto, $" + d4(ex3[0]) + "$.",
     r"$N(15;\ \sqrt{10{,}5}\approx3{,}24)$: \ $P(9{,}5\leq X'\leq20{,}5)=P(-1{,}70\leq Z\leq1{,}70)=2\cdot0{,}9554-1=" + N2(ex3[1]) + r"$. La diferencia es de solo $" + d4(abs(ex3[1] - ex3[0])) + "$."),
]))
ck(ex3[1], 2 * Phi(1.7) - 1)

# =====================================================================
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
# el primer exercici de cada secció no fa salt de pàgina: així no queda separat del títol
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'''
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Distribución binomial y normal"
KW = "variable aleatoria, distribución binomial, distribución normal, normal tipificada, tipificación, aproximación de la binomial por la normal, tablas, PAU"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 10: %s' % (t, TIT), capcalera='%s · Unidad 10: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 10' if sol else 'Ficha de ejercicios · Unidad 10') + '}{\\raggedright ' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    npau = sum(1 for _, exs in S for _, q_, _ in exs if '\\pau{' in q_)
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Las probabilidades de la normal se han calculado como en la PAU: redondeando $z$ a dos decimales y leyendo la tabla $N(0,1)$. En los problemas inversos se ha tomado el valor de la tabla más próximo; por eso algunos resultados pueden diferir ligeramente de los que se obtienen con una calculadora."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Usa las tablas de la binomial y de la normal $N(0,1)$ de la PAU valenciana, que tienes en los apuntes interactivos de la unidad: redondea $z$ a dos decimales. Los " + str(npau) + r" ejercicios marcados con \textcolor{teal}{\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q_, s) in enumerate(exs):
            n += 1
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, s if sol else q_))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con la calculadora de probabilidades de los apuntes interactivos.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't10-fitxa-solucions-es.tex' if sol else 't10-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n, npau

n = build(False); build(True)
print(n[0], 'ejercicios,', n[1], 'de la PAU;', len(CHK), 'comprobaciones')
