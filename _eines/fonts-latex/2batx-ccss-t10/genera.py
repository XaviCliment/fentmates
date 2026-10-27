# Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 10: Distribució binomial i normal)
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
S.append(("Variables aleatòries discretes", [
 (1, r"Digues si les variables següents són discretes o contínues:" + tasks(2, [r"El nombre de germans d'un alumne.", r"El temps que tarda un autobús a arribar.", r"El pes d'un nadó.", r"El nombre de clients que entren en una botiga en una hora.", r"La nota d'un examen amb decimals.", r"El nombre de cares en 10 llançaments."]),
     tasks(2, [r"\rest{Discreta}", r"\rest{Contínua}", r"\rest{Contínua}", r"\rest{Discreta}", r"\rest{Contínua} (és una mesura que pot prendre qualsevol valor)", r"\rest{Discreta}"])),
 (2, r"Una variable aleatòria $X$ pren els valors 0, 1, 2 i 3 amb probabilitats $0{,}1$, $k$, $0{,}3$ i $2k$, respectivament." + tasks(1, [r"Calcula $k$.", r"Calcula la mitjana i la desviació típica de $X$.", r"Calcula $P(X\geq2)$."])
     + recorda(r"$\sum p_i=1$; \ $\mu=\sum x_ip_i$; \ $\sigma^2=\sum x_i^2p_i-\mu^2$."),
     tasks(1, [r"$0{,}1+k+0{,}3+2k=1\Rightarrow3k=0{,}6\Rightarrow\res{k=0{,}2}$", r"$\mu=0+0{,}2+0{,}6+1{,}2=\res{2}$; \ $\sigma^2=0{,}2+1{,}2+3{,}6-2^2=1\Rightarrow\res{\sigma=1}$",
               r"$P(X\geq2)=0{,}3+0{,}4=\res{0{,}7}$"])),
 (2, r"En un joc es llancen dos daus: si ix un doble, guanyes 5 euros; si no, perds 1 euro. Siga $X$ el guany. Calcula el guany mitjà i la desviació típica. És un joc just?",
     r"$P(X=5)=\frac6{36}=\frac16$, $P(X=-1)=\frac56$. $\mu=5\cdot\frac16-1\cdot\frac56=\res{0}$: \rest{és un joc just}. $\sigma^2=25\cdot\frac16+1\cdot\frac56-0=5\Rightarrow\res{\sigma=\sqrt5\approx2{,}24}$ euros."),
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
S.append(("La distribució binomial", [
 (1, r"Digues si les variables següents segueixen una distribució binomial i, si és així, indica'n els paràmetres:" + tasks(1, [
      r"Nombre de sisos en 12 llançaments d'un dau.", r"Nombre de boles roges en traure 3 boles, sense reemplaçament, d'una urna amb 4 roges i 6 blanques.",
      r"Nombre de peces defectuoses en una mostra de 50, si el 2\,\% de la producció és defectuosa.", r"Nombre de llançaments d'una moneda fins que ix la primera cara."])
     + recorda(r"una binomial $B(n,p)$ compta els èxits en $n$ proves independents amb la mateixa probabilitat d'èxit $p$."),
     tasks(1, [r"\rest{Sí}: $B\left(12,\frac16\right)$.", r"\rest{No}: sense reemplaçament, la probabilitat de roja canvia en cada extracció.", r"\rest{Sí}: $B(50;\ 0{,}02)$ (la producció és molt gran: les proves són pràcticament independents).",
               r"\rest{No}: el nombre de proves no està fixat."])),
 (1, r"Es llança un dau 5 vegades. Calcula la probabilitat d'obtindre exactament dos cincs i la d'obtindre almenys un cinc.",
     r"$X\sim B\left(5,\frac16\right)$: \ $P(X=2)=\binom52\left(\frac16\right)^2\left(\frac56\right)^3=" + B(d5[0]) + r"$; \ $P(X\geq1)=1-\left(\frac56\right)^5=" + B(d5[1]) + "$."),
 (1, r"\pau{Aragó, EvAU extraordinària 2024} En una ciutat, segons les dades de l'INE, el 52\,\% dels habitants són dones i el 48\,\% homes. Es trien quatre persones d'aquesta ciutat amb reemplaçament. Siga $X$ la variable que compta el nombre d'homes seleccionats. Quina distribució té la variable $X$? Calcula $P(X=2)$.",
     r"$\res{X\sim B(4;\ 0{,}48)}$: 4 proves independents amb la mateixa probabilitat d'home. \ $P(X=2)=\binom42\,0{,}48^2\,0{,}52^2=6\cdot0{,}2304\cdot0{,}2704=" + B(ar) + "$."),
 (1, r"\pau{Aragó, EvAU ordinària 2024} Una vegada feta la votació, el candidat Rupérez ha guanyat amb el 62\,\% dels vots. Si triem 3 votants amb reemplaçament, calcula la probabilitat que almenys un d'ells haja votat Rupérez.",
     r"$X\sim B(3;\ 0{,}62)$: \ $P(X\geq1)=1-P(X=0)=1-0{,}38^3=" + B(ro) + "$."),
 (2, r"\pau{Andalusia, PAU extraordinària 2026 (adaptat)} Siguen $A$ i $B$ dos successos d'un mateix experiment aleatori amb $P(A)=0{,}65$, $P(B)=0{,}55$ i $P(A\cap B)=0{,}35$." + tasks(1, [
      r"Calcula la probabilitat que n'ocórrega almenys un i la probabilitat que ocórrega $B$, sabent que no ha ocorregut $A$.", r"L'experiment es fa 11 vegades. Calcula la probabilitat que el succés $B$ ocórrega exactament 8 vegades i el nombre esperat de vegades que ocorre $B$."]),
     tasks(1, [r"$P(A\cup B)=0{,}65+0{,}55-0{,}35=" + B(an[0], 2) + r"$; \ $P(B|\overline A)=\frac{0{,}55-0{,}35}{0{,}35}=\frac47\approx" + B(an[1]) + "$",
               r"$X\sim B(11;\ 0{,}55)$: \ $P(X=8)=\binom{11}{8}0{,}55^8\,0{,}45^3=" + B(an[2]) + r"$; \ $\mu=11\cdot0{,}55=6{,}05$: s'espera que ocórrega unes \rest{6 vegades}."])),
 (1, r"\pau{País Basc, EAU extraordinària 2023} Un jugador $A$ fa llançaments amb una moneda equilibrada i un altre jugador $B$, amb una moneda trucada en què la probabilitat de cara és $0{,}4$. Siguen $X$ el nombre de cares de $A$ i $Y$ el nombre de creus de $B$." + tasks(1, [
      r"Calcula la probabilitat que el jugador $A$ obtinga 3 cares en 3 llançaments.", r"Calcula la probabilitat que el jugador $B$ obtinga 2 creus en 2 llançaments."]),
     tasks(1, [r"$X\sim B(3;\ 0{,}5)$: \ $P(X=3)=0{,}5^3=" + B(pv[0], 3) + "$", r"$Y\sim B(2;\ 0{,}6)$ (creu: $1-0{,}4$): \ $P(Y=2)=0{,}6^2=" + B(pv[1], 2) + "$"])),
 (2, r"\pau{Castella i Lleó, PAU ordinària 2026} El 90\,\% dels joves d'entre 25 i 34 anys compra per Internet. Una botiga fa una enquesta a 10 clients joves." + tasks(1, [
      r"Calcula la probabilitat que exactament 2 dels 10 clients no facen compres en línia.", r"Calcula la probabilitat que menys de 2 clients no facen compres en línia."]),
     r"$X=$ «nombre de clients que no compren en línia» $\sim B(10;\ 0{,}1)$ (no és a la taula de la PAU: $n=10$)." + tasks(1, [r"$P(X=2)=\binom{10}{2}0{,}1^2\,0{,}9^8=" + B(cy[0]) + "$",
      r"$P(X<2)=P(X=0)+P(X=1)=0{,}9^{10}+10\cdot0{,}1\cdot0{,}9^9=" + B(cy[1]) + "$"])),
 (2, r"\pau{Canàries, EBAU ordinària 2022} Una companyia d'assegurances té assegurats 2500 cotxes, 560 autobusos i 220 motos. Per a una inspecció es trien a l'atzar les pòlisses de 10 dels vehicles assegurats. Quina és la probabilitat que entre els vehicles triats hi haja almenys dos autobusos?",
     r"Hi ha $3280$ vehicles i $p=\frac{560}{3280}\approx0{,}1707$. Com que hi ha molts vehicles, $X\sim B(10;\ 0{,}1707)$ aproximadament: $P(X\geq2)=1-P(X=0)-P(X=1)=1-0{,}8293^{10}-10\cdot0{,}1707\cdot0{,}8293^9\approx" + B(cg) + "$."),
 (2, r"Quantes vegades, com a mínim, cal llançar una moneda perquè la probabilitat d'obtindre almenys una cara siga més gran que $0{,}99$?",
     r"$P(\text{almenys una cara})=1-0{,}5^n>0{,}99\iff0{,}5^n<0{,}01\iff2^n>100$. Com que $2^6=64$ i $2^7=128$: \ $\res{n=7}$ llançaments."),
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
S.append(("La distribució binomial amb la taula de la PAU", [
 (1, r"Siga $X\sim B(5;\ 0{,}25)$. Calcula amb la taula de la PAU:" + tasks(4, [r"$P(X=2)$", r"$P(X\leq1)$", r"$P(X\geq4)$", r"$P(X>0)$"])
     + recorda(r"la taula dona $P(X=x)$ per a $n\leq9$. Per a les acumulades, suma caselles de la mateixa columna o fes el contrari."),
     r"Bloc $n=5$, columna $p=0{,}25$:" + tasks(2, [r"$" + B(r4(b5[0])) + "$", r"$0{,}2373+0{,}3955=" + B(r4(pmf(5, .25, 0)) + r4(pmf(5, .25, 1))) + "$", r"$0{,}0146+0{,}0010=" + B(r4(pmf(5, .25, 4)) + r4(pmf(5, .25, 5))) + "$", r"$1-0{,}2373=" + B(1 - r4(pmf(5, .25, 0))) + "$"])),
 (1, r"Siga $X\sim B\left(9,\frac13\right)$. Calcula amb la taula $P(X\leq2)$ i $P(X\geq3)$.",
     r"Bloc $n=9$, columna $p=1/3$: \ $P(X\leq2)=0{,}0260+0{,}1171+0{,}2341=" + B(r4(pmf(9, 1/3, 0)) + r4(pmf(9, 1/3, 1)) + r4(pmf(9, 1/3, 2))) + r"$; \ $P(X\geq3)=1-0{,}3772=" + B(1 - (r4(pmf(9, 1/3, 0)) + r4(pmf(9, 1/3, 1)) + r4(pmf(9, 1/3, 2)))) + "$."),
 (2, r"El 80\,\% dels clients d'una botiga està satisfet amb l'atenció rebuda. Es trien 7 clients a l'atzar. Calcula, amb la taula de la PAU, la probabilitat que:" + tasks(3, [r"n'estiguen satisfets exactament 6;", r"n'estiguen satisfets almenys 6;", r"n'estiguen satisfets com a molt 5."]),
     r"$X\sim B(7;\ 0{,}8)$ no és a la taula ($p>0{,}5$). Comptem els no satisfets: $Y=7-X\sim B(7;\ 0{,}2)$." + tasks(1, [r"$P(X=6)=P(Y=1)=" + B(r4(b7[0])) + "$", r"$P(X\geq6)=P(Y\leq1)=0{,}2097+0{,}3670=" + B(r4(pmf(7, .2, 0)) + r4(pmf(7, .2, 1))) + "$",
      r"$P(X\leq5)=1-P(X\geq6)=" + B(1 - r4(pmf(7, .2, 0)) - r4(pmf(7, .2, 1))) + "$"])),
 (2, r"Germina el 90\,\% de les llavors d'una marca. Es planten 8 llavors. Calcula, amb la taula, la probabilitat que germinen totes, que germinen almenys 7 i que en germinen exactament 7.",
     r"$Y=$ «llavors que no germinen» $\sim B(8;\ 0{,}1)$: \ $P(\text{totes})=P(Y=0)=" + B(r4(b8[0])) + r"$; \ $P(X\geq7)=P(Y\leq1)=0{,}4305+0{,}3826=" + B(r4(pmf(8, .1, 0)) + r4(pmf(8, .1, 1))) + r"$; \ $P(X=7)=P(Y=1)=" + B(r4(b8[2])) + "$."),
 (2, r"Un test té 6 preguntes amb 4 opcions cadascuna, de les quals només una és correcta. S'aprova encertant-ne almenys 3. Un alumne contesta totes les preguntes a l'atzar. Quina és la probabilitat que aprove?",
     r"$X\sim B(6;\ 0{,}25)$; bloc $n=6$, columna $0{,}25$: \ $P(X\geq3)=0{,}1318+0{,}0330+0{,}0044+0{,}0002=" + B(sum(r4(pmf(6, .25, k)) for k in range(3, 7))) + "$."),
 (2, r"Siga $X\sim B(12;\ 0{,}2)$. Es pot calcular $P(X=3)$ amb la taula de la PAU? Calcula-la.",
     r"\rest{No}: la taula només arriba fins a $n=9$. Amb la fórmula: $P(X=3)=\binom{12}{3}0{,}2^3\,0{,}8^9=220\cdot0{,}008\cdot0{,}1342=" + B(b12) + "$."),
]))
ck(r4(pmf(5, .25, 0)), .2373); ck(r4(pmf(9, 1/3, 1)), .1171); ck(r4(pmf(7, .2, 1)), .3670); ck(r4(pmf(8, .1, 1)), .3826); ck(r4(pmf(6, .25, 3)), .1318)

# =====================================================================
# 4. Normal típica
z4 = [Phi(1.53), 1 - Phi(2.05), Phi(-0.82), 1 - Phi(-1.2), Phi(1.5) - Phi(0.75), Phi(1) - Phi(-2), 2 * Phi(2.58) - 1]
S.append(("La normal típica $N(0,1)$ i la seua taula", [
 (1, r"Si $Z\sim N(0,1)$, calcula amb la taula de la PAU:" + tasks(4, [r"$P(Z\leq1{,}53)$", r"$P(Z>2{,}05)$", r"$P(Z<-0{,}82)$", r"$P(Z\geq-1{,}2)$", r"$P(0{,}75\leq Z\leq1{,}5)$", r"$P(-2< Z<1)$", r"$P(|Z|\leq2{,}58)$"])
     + recorda(r"la taula dona $P(Z\leq z)$ per a $z\geq0$. \ $P(Z\geq z)=1-P(Z\leq z)$, \ $P(Z\leq-z)=1-P(Z\leq z)$."),
     tasks(2, [r"$" + B(z4[0]) + "$", r"$1-0{,}9798=" + B(z4[1]) + "$", r"$1-0{,}7939=" + B(z4[2]) + "$", r"$P(Z\leq1{,}2)=" + B(z4[3]) + "$", r"$0{,}9332-0{,}7734=" + B(z4[4]) + "$",
               r"$0{,}8413-(1-0{,}9772)=" + B(z4[5]) + "$", r"$2\cdot0{,}9951-1=" + B(z4[6]) + "$"])),
 (2, r"Si $Z\sim N(0,1)$, troba el valor de $k$ en cada cas:" + tasks(2, [r"$P(Z\leq k)=0{,}8907$", r"$P(Z\geq k)=0{,}0505$", r"$P(Z\leq k)=0{,}25$", r"$P(-k\leq Z\leq k)=0{,}9$"])
     + recorda(r"busca la probabilitat \emph{dins} de la taula; si és menor que 0,5, $k$ és negatiu."),
     tasks(1, [r"El valor és a la taula: $\res{k=1{,}23}$", r"$P(Z\leq k)=0{,}9495\Rightarrow\res{k=1{,}64}$", r"$P(Z\leq-k)=0{,}75$: més pròxim $0{,}7486\to0{,}67$, així que $\res{k\approx-0{,}67}$",
               r"$2P(Z\leq k)-1=0{,}9\Rightarrow P(Z\leq k)=0{,}95$: entre $1{,}64$ i $1{,}65$, $\res{k\approx1{,}645}$"])),
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
S.append(("Tipificació: problemes amb la normal", [
 (1, r"\pau{Illes Balears, PBAU extraordinària 2025} Quan un client entra en una botiga d'electrodomèstics, el temps (en minuts) que hi passa segueix una distribució $N(15,10)$." + tasks(1, [
      r"Quina és la probabilitat que un client estiga dins de la botiga 25 minuts o menys?", r"Quina és la probabilitat que un client estiga dins de la botiga entre 5 i 25 minuts?"])
     + recorda(r"si $X\sim N(\mu,\sigma)$, aleshores $Z=\dfrac{X-\mu}{\sigma}\sim N(0,1)$. Arredoneix $z$ a dues decimals i fes servir la taula."),
     tasks(1, [r"$P(X\leq25)=P\left(Z\leq\frac{25-15}{10}\right)=P(Z\leq1)=" + N2(q['b25'][0]) + "$", r"$P(-1\leq Z\leq1)=2\cdot0{,}8413-1=" + N2(q['b25'][1]) + "$"])
     + cen(gauss([(-1, 1)], [(-1, '-1'), (0, '0'), (1, '1')]))),
 (1, r"\pau{Illes Balears, PBAU ordinària 2021} El pes de les persones d'un col·legi major segueix una llei normal de mitjana 70 kg i desviació típica 15 kg. Triem una persona a l'atzar; calcula la probabilitat que:" + tasks(3, [r"pese més de 80 kg;", r"pese menys de 50 kg;", r"pese entre 60 i 120 kg."]),
     tasks(1, [r"$P(Z>0{,}67)=1-0{,}7486=" + N2(q['b21'][0]) + "$", r"$P(Z<-1{,}33)=1-0{,}9082=" + N2(q['b21'][1]) + "$", r"$P(-0{,}67< Z<3{,}33)=0{,}9996-0{,}2514=" + N2(q['b21'][2]) + "$"])),
 (2, r"\pau{Illes Balears, PBAU extraordinària 2023} En una població, l'altura dels homes segueix una normal de mitjana 1,76 m i desviació típica 0,12 m, i la de les dones, una normal de mitjana 1,62 m i desviació típica 0,11 m." + tasks(1, [
      r"Triem un home a l'atzar. Quina és la probabilitat que la seua altura siga major o igual que 1,76 m?", r"Triem una dona a l'atzar. Quina és la probabilitat que la seua altura siga major o igual que 1,76 m?", r"Què és més probable, que un home mesure menys d'1,76 m o que ho faça una dona?"]),
     tasks(1, [r"1,76 és la mitjana dels homes: $\res{0{,}5}$", r"$P\left(Z\geq\frac{1{,}76-1{,}62}{0{,}11}\right)=P(Z\geq1{,}27)=1-0{,}8980=" + N2(q['b23'][1]) + "$",
               r"Home: $0{,}5$; dona: $1-0{,}102=0{,}898$. \rest{És més probable que una dona mesure menys d'1,76 m.}"])),
 (1, r"\pau{Canàries, EBAU juny 2017} La despesa mensual en aigua de les famílies de quatre membres segueix una normal de mitjana 32 euros i desviació típica 10 euros. Calcula la probabilitat que la despesa mensual d'una d'aquestes famílies:" + tasks(1, [r"siga més gran que 36 euros;", r"estiga entre 28 i 35 euros."]),
     tasks(1, [r"$P(Z>0{,}4)=1-0{,}6554=" + N2(q['c17'][0]) + "$", r"$P(-0{,}4< Z<0{,}3)=0{,}6179-(1-0{,}6554)=" + N2(q['c17'][1]) + "$"])),
 (1, r"\pau{Castella i Lleó, EBAU extraordinària 2021} La nota mitjana dels alumnes de segon de Batxillerat d'un institut segueix una normal de mitjana 6,8 i desviació típica 1,1. Calcula la probabilitat que un alumne haja obtingut més d'un 9.",
     r"$P(X>9)=P\left(Z>\frac{9-6{,}8}{1{,}1}\right)=P(Z>2)=1-0{,}9772=" + N2(q['cl21']) + "$."),
 (1, r"\pau{Castella i Lleó, EBAU ordinària 2020} La vida útil sense avaries d'un nou model de mòbil (en mesos) segueix una normal de mitjana 32 i desviació típica 12,5. La campanya de llançament ofereix canviar gratuïtament el mòbil si s'avaria en els primers 4 mesos. Calcula la probabilitat que calga substituir un mòbil.",
     r"$P(X<4)=P\left(Z<\frac{4-32}{12{,}5}\right)=P(Z<-2{,}24)=1-0{,}9875=" + N2(q['cl20']) + "$."),
 (1, r"\pau{Castella i Lleó, EBAU juliol 2019 i juny 2019}" + tasks(1, [r"El temps de resolució d'un examen segueix una normal de mitjana 74 minuts i desviació típica 8 minuts. Quina és la probabilitat de necessitar més dels 90 minuts disponibles?",
      r"El temps que tarda un fumador a deixar de fumar segueix una normal de mitjana 5 mesos i desviació típica 2 mesos. Quina és la probabilitat que un fumador tarde més de 4 mesos?"]),
     tasks(1, [r"$P(Z>2)=" + N2(q['cl19'][0]) + "$", r"$P(Z>-0{,}5)=P(Z<0{,}5)=" + N2(q['cl19'][1]) + "$"])),
 (1, r"\pau{País Basc, EAU extraordinària 2020} Les notes d'un grup en una assignatura segueixen una normal de mitjana 6,2 punts i desviació típica 2 punts. Es tria un estudiant a l'atzar. Calcula la probabilitat que la seua nota siga superior a 7 i la probabilitat que estiga entre 5 i 8 punts.",
     r"$P(Z>0{,}4)=1-0{,}6554=" + N2(q['pv20'][0]) + r"$; \ $P(-0{,}6< Z<0{,}9)=0{,}8159-0{,}2743=" + N2(q['pv20'][1]) + "$." + cen(gauss([(-0.6, 0.9)], [(-0.6, '-0{,}6'), (0.9, '0{,}9')]))),
 (1, r"\pau{País Basc, EAU extraordinària 2020} El temps que necessiten els alumnes per a acabar un examen segueix una normal de mitjana 60 minuts i desviació típica 10 minuts. Si es donen 75 minuts, quina proporció d'alumnes l'acabarà? I si se'n donen 80, quina proporció no l'acabarà?",
     r"$P(X\leq75)=P(Z\leq1{,}5)=" + N2(q['pv20b'][0]) + r"$ \ (el $93{,}32\,\%$); \ $P(X>80)=P(Z>2)=" + N2(q['pv20b'][1]) + r"$ \ (el $2{,}28\,\%$)."),
 (1, r"\pau{País Basc, EAU ordinària 2020} L'altura de les dones d'un país segueix una normal de mitjana 163 cm i desviació típica 7 cm. Quina és la probabilitat que una dona triada a l'atzar mesure més de 171 cm? I que mesure entre 155 i 171 cm?",
     r"$z=\frac{171-163}{7}\approx1{,}14$: \ $P(Z>1{,}14)=1-0{,}8729=" + N2(q['pv20c'][0]) + r"$; \ $P(-1{,}14< Z<1{,}14)=2\cdot0{,}8729-1=" + N2(q['pv20c'][1]) + "$."),
 (1, r"\pau{Castella i Lleó, EBAU juliol 2018} El salari mensual dels treballadors d'una empresa segueix una normal de mitjana 1200 euros i desviació típica 400 euros. Quina és la probabilitat que un treballador cobre més de 1740 euros al mes?",
     r"$P\left(Z>\frac{540}{400}\right)=P(Z>1{,}35)=1-0{,}9115=" + N2(q['cl18']) + "$."),
 (2, r"\pau{Canàries, EBAU juliol 2019} En una empresa hi ha 250 empleats. La seua edat segueix una normal de mitjana 44 anys i desviació típica 18 anys." + tasks(1, [
      r"Quants empleats s'espera que tinguen més de 62 anys?", r"Quants empleats s'espera que tinguen menys de 40 anys?", r"Quants empleats podrien aconseguir el carnet jove de transport si el requisit és ser major d'edat i no haver complit els 30 anys?"]),
     r"Multipliquem cada probabilitat pel total d'empleats:" + tasks(1, [r"$P(Z>1)=0{,}1587$; \ $250\cdot0{,}1587\approx\res{40}$ empleats.", r"$P(Z<-0{,}22)=1-0{,}5871=0{,}4129$; \ $250\cdot0{,}4129\approx\res{103}$ empleats.",
      r"$P(18\leq X<30)=P(-1{,}44\leq Z<-0{,}78)=(1-0{,}7823)-(1-0{,}9251)=0{,}1428$; \ $250\cdot0{,}1428\approx\res{36}$ empleats."])),
 (1, r"\pau{Canàries, EBAU juny 2019} El pes dels joves d'una regió que pateixen diabetis de tipus 2 segueix una normal de mitjana 89 kg i desviació típica 20 kg. Quin percentatge d'aquests joves pesa entre 86 i 100 kg?",
     r"$P(-0{,}15< Z<0{,}55)=0{,}7088-(1-0{,}5596)=" + N2(q['c19j']) + r"$: \ el $\res{26{,}84\,\%}$."),
 (2, r"\pau{Canàries, EBAU extraordinària 2024} En una ciutat, el lloguer mensual dels pisos de dues habitacions segueix una normal de mitjana 725 euros i desviació típica 50 euros." + tasks(1, [
      r"Quina és la probabilitat que llogar un d'aquests pisos coste, com a molt, 700 euros al mes?", r"Una agència immobiliària lloga 25 d'aquests pisos. Quants s'espera que costen menys de 710 euros al mes?"]),
     tasks(1, [r"$P(Z\leq-0{,}5)=1-0{,}6915=" + N2(q['c24'][0]) + "$", r"$P(Z<-0{,}3)=1-0{,}6179=0{,}3821$; \ $25\cdot0{,}3821\approx9{,}55$: s'espera que en siguen \rest{entre 9 i 10}."])),
 (2, r"\pau{Illes Balears, PBAU ordinària 2024} Segons l'INE, l'esperança de vida d'una persona nascuda el 2020 és de 79,6 anys per als homes i de 83,6 anys per a les dones. Suposem que el nombre d'anys que viurà una persona nascuda el 2020 segueix una normal de desviació típica 10 anys, tant per als homes com per a les dones." + tasks(1, [
      r"Quina és la probabilitat que un home nascut el 2020 visca més de 60 anys? I que visca entre 60 i 70 anys?", r"Què és més probable: que un home nascut el 2020 visca més de 89,6 anys, o que una dona nascuda el 2020 visca més de 93,6 anys?"]),
     tasks(1, [r"$P(Z>-1{,}96)=" + N2(q['b24'][0]) + r"$; \ $P(-1{,}96< Z<-0{,}96)=(1-0{,}8315)-(1-0{,}9750)=" + N2(q['b24'][1]) + "$",
               r"Home: $P\left(Z>\frac{10}{10}\right)=P(Z>1)$; dona: $P\left(Z>\frac{10}{10}\right)=P(Z>1)$. \rest{Són igual de probables} ($0{,}1587$)."])),
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
S.append(("Problemes inversos", [
 (2, r"\pau{Illes Balears, PAU extraordinària 2026} El temps que cada jove d'una població dedica cada dia a les xarxes socials segueix una normal de mitjana 116 minuts i desviació típica 42 minuts." + tasks(1, [
      r"Quina proporció de joves dedica entre 100 i 200 minuts a les xarxes socials?", r"En Joan és del 10\,\% de joves que més temps hi dedica. Quants minuts hi dedica, com a mínim?"])
     + recorda(r"en un problema invers busquem la probabilitat dins de la taula, llegim $z$ i desfem la tipificació: $x=\mu+z\,\sigma$."),
     tasks(1, [r"$P(-0{,}38< Z<2)=0{,}9772-(1-0{,}6480)=" + N2(iq['ba26'][0]) + r"$: el $62{,}52\,\%$.",
               r"$P(X\geq k)=0{,}1\Rightarrow P(Z\leq z)=0{,}9$: més pròxim $0{,}8997\to z=1{,}28$; \ $k=116+1{,}28\cdot42=\res{169{,}76}$ minuts."]) + cen(gauss([(1.28, None)], [(0, '0'), (1.28, '1{,}28')]))),
 (2, r"\pau{País Basc, EAU extraordinària 2020} Les notes d'un grup segueixen una normal de mitjana 6,2 i desviació típica 2. Si el 25\,\% de l'alumnat amb millor nota va obtindre la qualificació d'excel·lent, quina és la nota mínima per a obtindre-la?",
     r"$P(Z\leq z)=0{,}75$: més pròxim $0{,}7486\to z=0{,}67$; \ $6{,}2+0{,}67\cdot2=\res{7{,}54}$."),
 (2, r"\pau{País Basc, EAU ordinària 2020} L'altura de les dones d'un país segueix una normal de mitjana 163 cm i desviació típica 7 cm. Una empresa de disfresses vol fer quatre talles, cadascuna adequada per al 25\,\% de les dones. Quines altures marquen el pas d'una talla a una altra?",
     r"Són els quartils: $z=\pm0{,}67$ (per a $0{,}75$) i $z=0$. \ $163-0{,}67\cdot7=\res{158{,}31}$, \ $\res{163}$ \ i \ $163+0{,}67\cdot7=\res{167{,}69}$ cm."),
 (2, r"\pau{País Basc, EAU ordinària 2020} El pes de les truites d'una piscifactoria segueix una normal de mitjana 250 g i desviació típica 50 g. Només són aptes per a la venda les que superen un pes determinat." + tasks(1, [
      r"Quin ha de ser aquest pes si es vol que el 40\,\% de les truites siguen aptes per a la venda?", r"Si aquest pes s'estableix en 280 g i a la piscifactoria hi ha 6000 truites, quantes se'n podran vendre?"]),
     tasks(1, [r"$P(Z\leq z)=0{,}6$: més pròxim $0{,}5987\to z=0{,}25$; \ $250+0{,}25\cdot50=\res{262{,}5}$ g", r"$P(Z>0{,}6)=1-0{,}7257=0{,}2743$; \ $6000\cdot0{,}2743\approx\res{1646}$ truites"])),
 (2, r"\pau{País Basc, EAU juliol 2019} Les puntuacions d'una prova de cultura general segueixen una normal de mitjana 68 i desviació típica 18. Es vol classificar els habitants en tres grups (cultura baixa, acceptable i excel·lent) de manera que el primer grup tinga el 20\,\% de la població, el segon el 65\,\% i el tercer el 15\,\% restant. Quines puntuacions marquen el pas d'un grup a un altre?",
     r"Primer tall: $P(Z\leq z_1)=0{,}2\Rightarrow z_1\approx-0{,}84$ (busquem $0{,}8$: $0{,}7995$); \ $68-0{,}84\cdot18=\res{52{,}88}$. \ Segon tall: $P(Z\leq z_2)=0{,}85$: més pròxim $0{,}8508\to z_2=1{,}04$; \ $68+1{,}04\cdot18=\res{86{,}72}$."),
 (2, r"\pau{País Basc, EAU juliol 2019 i PAU ordinària 2025} La nota d'accés de l'alumnat preinscrit en el grau A segueix una normal $N(6{,}8;\ 0{,}6)$, i la del grau B, una $N(7;\ 0{,}5)$. En tots dos casos només s'admet el 25\,\% de l'alumnat amb millors notes." + tasks(1, [
      r"Quin grau requerirà una nota mínima més baixa?", r"La Iolanda ha tret un 7,25 i la Teresa un 7,45. A quins graus tindran opció d'accés?"]),
     r"$P(Z\leq z)=0{,}75\Rightarrow z\approx0{,}67$." + tasks(1, [r"A: $6{,}8+0{,}67\cdot0{,}6=7{,}202$; \ B: $7+0{,}67\cdot0{,}5=7{,}335$. \rest{El grau A demana una nota mínima més baixa.}",
      r"La Iolanda ($7{,}25$) \rest{només pot entrar en A}; la Teresa ($7{,}45$) \rest{pot entrar en tots dos}."])),
 (2, r"\pau{País Basc, EAU ordinària 2024} La puntuació d'un examen de Matemàtiques Aplicades a les Ciències Socials segueix una normal de mitjana 5,8 punts i desviació típica 2,6 punts." + tasks(1, [
      r"Quina puntuació és superada únicament pel 20\,\% de l'alumnat?", r"Si l'apte s'obté amb una puntuació igual o superior a 5, quin percentatge de l'alumnat ha sigut apte?"]),
     tasks(1, [r"$P(Z\leq z)=0{,}8$: més pròxim $0{,}7995\to z=0{,}84$; \ $5{,}8+0{,}84\cdot2{,}6=\res{7{,}984}$", r"$P(Z\geq-0{,}31)=P(Z\leq0{,}31)=" + N2(iq['pv24'][2]) + r"$: el $62{,}17\,\%$"])),
 (2, r"\pau{País Basc, EAU ordinària 2022} En l'examen d'Anglés, el 30\,\% de l'alumnat va obtindre una puntuació superior a 7,6 punts. La puntuació segueix una normal de mitjana 6,8 punts." + tasks(1, [
      r"Calcula la desviació típica de la puntuació.", r"Si la desviació típica és de 1,5 punts, quina puntuació és superada únicament pel 20\,\% de l'alumnat?", r"Si la desviació típica és de 1,5 punts i s'aprova amb un 5 o més, quin percentatge ha aprovat?"]),
     tasks(1, [r"$P\left(Z\leq\frac{0{,}8}{\sigma}\right)=0{,}7$: més pròxim $0{,}6985\to0{,}52$; \ $\sigma=\frac{0{,}8}{0{,}52}\approx\res{1{,}54}$", r"$6{,}8+0{,}84\cdot1{,}5=\res{8{,}06}$",
               r"$P(Z\geq-1{,}2)=P(Z\leq1{,}2)=" + N2(iq['pv22'][3]) + r"$: el $88{,}49\,\%$"])),
 (2, r"\pau{La Rioja, EBAU ordinària 2024} Les valoracions d'un producte segueixen una normal de mitjana $\mu$ i desviació típica $\sigma$. El percentatge de valoracions superiors a 7 coincideix amb el de valoracions inferiors a 5." + tasks(1, [
      r"Per què podem deduir que $\mu=6$?", r"Si aquest percentatge és del 15,866\,\%, quin és el valor de $\sigma$?", r"Quin valor és superat només pel 2,5\,\% de les valoracions?"]),
     tasks(1, [r"Per la simetria de la normal respecte de $\mu$, 5 i 7 estan a la mateixa distància de la mitjana: $\mu=\frac{5+7}{2}=\res{6}$.",
               r"$P\left(Z\leq\frac1\sigma\right)=0{,}84134\approx0{,}8413\Rightarrow\frac1\sigma=1\Rightarrow\res{\sigma=1}$", r"$P(Z\leq z)=0{,}975\Rightarrow z=1{,}96$; \ $6+1{,}96=\res{7{,}96}$"])),
 (2, r"\pau{La Rioja, EBAU ordinària 2023} L'estatura dels policies de França segueix una normal de desviació típica 6,5 cm, de manera que l'11,507\,\% mesura més de 183 cm." + tasks(1, [
      r"Calcula la mitjana de l'estatura.", r"Troba l'estatura que és superada pel 88,493\,\% dels policies."]),
     tasks(1, [r"$P\left(Z\leq\frac{183-\mu}{6{,}5}\right)=0{,}88493\approx0{,}8849\Rightarrow\frac{183-\mu}{6{,}5}=1{,}2\Rightarrow\res{\mu=175{,}2}$ cm",
               r"Per simetria, $z=-1{,}2$: \ $175{,}2-1{,}2\cdot6{,}5=\res{167{,}4}$ cm"])),
 (2, r"\pau{La Rioja, EBAU extraordinària 2021} L'estatura dels homes adults espanyols segueix una normal de mitjana 174 cm i desviació típica 8 cm." + tasks(1, [
      r"Quina és la probabilitat que un home adult espanyol mesure més de 190 cm?", r"Entre els homes holandesos, la probabilitat de mesurar més de 190 cm (amb la mateixa desviació típica) és 0,15866. Quina és la seua estatura mitjana?"]),
     tasks(1, [r"$P(Z>2)=" + N2(iq['lr21'][0]) + "$", r"$P\left(Z\leq\frac{190-\mu}{8}\right)=0{,}84134\Rightarrow\frac{190-\mu}8=1\Rightarrow\res{\mu=182}$ cm"])),
 (2, r"\pau{Castella i Lleó, EBAU juliol 2018} En una empresa, el salari mitjà mensual és de 1400 euros i el 80,23\,\% dels treballadors cobra menys de 1570 euros. Calcula la desviació típica del salari, suposant que segueix una distribució normal.",
     r"$P\left(Z<\frac{170}{\sigma}\right)=0{,}8023\Rightarrow\frac{170}{\sigma}=0{,}85\Rightarrow\res{\sigma=200}$ euros."),
 (2, r"\pau{Castella i Lleó, PAU ordinària 2026} La despesa mensual dels compradors en línia segueix una normal de mitjana 275 euros." + tasks(1, [
      r"Si el 69,15\,\% dels compradors gasta menys de 300 euros al mes, determina la desviació típica de la despesa.", r"Calcula la probabilitat que un comprador gaste més de 400 euros al mes."]),
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
S.append(("Aproximació de la binomial per la normal", [
 (1, r"Siga $X\sim B(100;\ 0{,}2)$." + tasks(1, [r"Comprova que es pot aproximar per una normal i indica quina.", r"Calcula aproximadament $P(X\leq15)$, $P(X=20)$ i $P(X\geq25)$."])
     + recorda(r"si $np\geq5$ i $nq\geq5$, $B(n,p)\approx N\left(np,\sqrt{npq}\right)$. No oblides la correcció de continuïtat ($\pm0{,}5$)."),
     tasks(1, [r"$np=20\geq5$, $nq=80\geq5$: \ $\res{X'\sim N(20,\,4)}$ ($\sigma=\sqrt{100\cdot0{,}2\cdot0{,}8}=4$)",
               r"$P(X\leq15)\approx P(X'\leq15{,}5)=P(Z\leq-1{,}13)=1-0{,}8708=" + N2(ap[0]) + r"$; \ $P(X=20)\approx P(19{,}5\leq X'\leq20{,}5)=P(-0{,}13\leq Z\leq0{,}13)=" + N2(ap[1]) + r"$; \ $P(X\geq25)\approx P(X'\geq24{,}5)=P(Z\geq1{,}13)=" + N2(ap[2]) + "$"])),
 (2, r"\pau{Canàries, EBAU ordinària 2022} Una companyia d'assegurances té assegurats 2500 cotxes, 560 autobusos i 220 motos. Les probabilitats de tindre un accident al llarg d'un any són 0,1 per als cotxes, 0,08 per als autobusos i 0,16 per a les motos." + tasks(1, [
      r"Quants vehicles en total es pot esperar que tinguen un accident al llarg del pròxim any?", r"Quina és la probabilitat que l'any que ve tinguen un accident almenys 270 dels cotxes assegurats?"]),
     tasks(1, [r"Sumem les mitjanes $np$: $2500\cdot0{,}1+560\cdot0{,}08+220\cdot0{,}16=250+44{,}8+35{,}2=\res{330}$ vehicles",
               r"$X\sim B(2500;\ 0{,}1)\approx N(250,\,15)$: \ $P(X\geq270)\approx P(X'\geq269{,}5)=P(Z\geq1{,}3)=1-0{,}9032=" + N2(cn[1]) + "$"])),
 (2, r"\pau{País Basc, EAU extraordinària 2023} El jugador $A$ llança una moneda equilibrada i el jugador $B$, una moneda trucada en què la probabilitat de cara és $0{,}4$. Què és més probable, que el jugador $A$ obtinga menys de 190 cares en 400 llançaments, o que el jugador $B$ obtinga menys de 110 creus en 200 llançaments? Justifica la resposta.",
     r"$A$: $X\sim B(400;\ 0{,}5)\approx N(200,\,10)$: \ $P(X\leq189)\approx P(Z\leq\frac{189{,}5-200}{10})=P(Z\leq-1{,}05)=" + N2(pa[0]) + r"$. \ $B$: creus $Y\sim B(200;\ 0{,}6)\approx N(120;\ \sqrt{48}\approx6{,}93)$: \ $P(Y\leq109)\approx P(Z\leq-1{,}52)=" + N2(pa[1]) + r"$. \ \rest{És més probable el succés del jugador $A$.}"),
 (2, r"\pau{Andalusia, PAU ordinària 2026 (adaptat)} Un succés té probabilitat $0{,}4$ i l'experiment es repeteix 1350 vegades de manera independent. Siga $X$ el nombre de vegades que ocorre." + tasks(1, [r"Quina distribució segueix $X$?", r"Calcula la probabilitat que el succés ocórrega com a molt 580 vegades, però més de 499 vegades."]),
     tasks(1, [r"$\res{X\sim B(1350;\ 0{,}4)}$", r"$\mu=540$, $\sigma=\sqrt{324}=18$: \ $P(500\leq X\leq580)\approx P(499{,}5\leq X'\leq580{,}5)=P(-2{,}25\leq Z\leq2{,}25)=2\cdot0{,}9878-1=" + N2(a26) + "$"])),
 (2, r"Siga $X\sim B(50;\ 0{,}3)$. Calcula $P(10\leq X\leq20)$ amb l'aproximació normal i compara-la amb el valor exacte, $" + d4(ex3[0]) + "$.",
     r"$N(15;\ \sqrt{10{,}5}\approx3{,}24)$: \ $P(9{,}5\leq X'\leq20{,}5)=P(-1{,}70\leq Z\leq1{,}70)=2\cdot0{,}9554-1=" + N2(ex3[1]) + r"$. La diferència és de només $" + d4(abs(ex3[1] - ex3[0])) + "$."),
]))
ck(ex3[1], 2 * Phi(1.7) - 1)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={variable aleatòria, distribució binomial, distribució normal, normal típica, tipificació, aproximació de la binomial per la normal, taules, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'''
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
'''

TIT = "Distribució binomial i normal"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 10: %s. 2n de Batxillerat CCSS}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 10: %s · 2n Batxillerat CCSS" % (t, TIT))
    assert 'Unitat 10' in p and 'unitat 10' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{16}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 10' if sol else "Fitxa d'exercicis · Unitat 10") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    npau = sum(1 for _, exs in S for _, q_, _ in exs if '\\pau{' in q_)
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Les probabilitats de la normal s'han calculat com a la PAU: arredonint $z$ a dues decimals i llegint la taula $N(0,1)$. En els problemes inversos s'ha pres el valor de la taula més pròxim; per això alguns resultats poden diferir lleugerament dels que s'obtenen amb una calculadora."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos. Fes servir les taules de la binomial i de la normal $N(0,1)$ de la PAU valenciana, que tens als apunts interactius de la unitat: arredoneix $z$ a dues decimals. Els " + str(npau) + r" exercicis marcats amb \textcolor{teal}{\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st_, q_, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st_, s if sol else q_))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb la calculadora de probabilitats dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't10-fitxa-solucions.tex' if sol else 't10-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n, npau

n = build(False); build(True)
print(n[0], 'exercicis,', n[1], 'de la PAU;', len(CHK), 'comprovacions')
