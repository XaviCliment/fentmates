# Solucions dels exercicis PAU de probabilitat (Comunitat Valenciana) números 2-52 del dossier.
# Cada solució es calcula amb fraccions exactes; ck() la compara amb el valor calculat a mà.
from comu import *
S = {}
o = r'\overline'

# 2
p = [F('0.6'), F('0.4')]; ap = [F('0.8'), F('0.1')]
pS = p[0] * (1 - ap[0]) + p[1] * (1 - ap[1]); ck(pS, F('0.48')); r = ck(p[0] * (1 - ap[0]) / pS, F(1, 4))
S[2] = SOL([st('Successos.', r'$B=$ «estudia bastant», $P(B)=0{,}6$; $\overline{B}=$ «estudia molt poc», $P(\overline B)=0{,}4$; $A=$ «aprova». Dades: $P(A|B)=0{,}8$, $P(A|\overline B)=0{,}1$.'),
            bayes([('B', p[0], 1 - ap[0]), ('B̄', p[1], 1 - ap[1])], 'Ā', 'A'),
            st('Probabilitat total de suspendre:', r'$$P(\overline A)=P(B)P(\overline A|B)+P(\overline B)P(\overline A|\overline B)=0{,}6\cdot0{,}2+0{,}4\cdot0{,}9=0{,}12+0{,}36=0{,}48$$'),
            st('Teorema de Bayes:', L(r'$$P(B|\overline A)=\frac{P(B)P(\overline A|B)}{P(\overline A)}=\frac{0{,}12}{0{,}48}=@r$$', r=N(r)))],
           L('$P(B|\\overline A)=@r$', r=N(r)))
# 3
pa, pb = F(2, 3), F(1, 3); pL = ck(pa * F('0.1') + pb * F('0.3'), F(1, 6)); r = ck(pb * F('0.3') / pL, F(3, 5))
S[3] = SOL([st('Successos.', r'$A$ i $B$: viure a cada ciutat; $L=$ «llig literatura». Com que $A$ té el doble d’habitants que $B$: $P(A)=\frac23$, $P(B)=\frac13$; $P(L|A)=0{,}1$, $P(L|B)=0{,}3$.'),
            bayes([('A', pa, F('0.1')), ('B', pb, F('0.3'))], 'L', 'L̄'),
            st('a) Probabilitat total:', L(r'$$P(L)=\tfrac23\cdot0{,}1+\tfrac13\cdot0{,}3=\tfrac1{15}+\tfrac1{10}=@r$$', r=N(pL))),
            st('b) Bayes:', L(r'$$P(B|L)=\frac{\frac13\cdot0{,}3}{\frac16}=\frac{1/10}{1/6}=@r$$', r=N(r)))],
           L('a) $P(L)=@a$; b) $P(B|L)=@b$', a=N(pL), b=N(r)))
# 4
a = ck(1 - F(30, 40) * F(29, 39) * F(28, 38), F(1 - F(30 * 29 * 28, 40 * 39 * 38))); b = ck(1 - F(3, 4) ** 3, F(37, 64))
S[4] = SOL([st('Idea.', '«Almenys una d’ors» és el contrari de «cap d’ors». Hi ha 10 ors i 30 cartes que no ho són.'),
            st('a) Sense reemplaçament:', L(r'$$P(\text{cap or})=\frac{30}{40}\cdot\frac{29}{39}\cdot\frac{28}{38}=@c\ \Rightarrow\ P(\text{almenys un or})=1-@c=@a$$', c=N(1 - a), a=N(a))),
            st('b) Amb reemplaçament:', L(r'les extraccions són independents: $$P(\text{almenys un or})=1-\left(\frac{30}{40}\right)^3=1-\frac{27}{64}=@b$$', b=N(b)))],
           L('a) $@a$; b) $@b$', a=N(a), b=N(b)))
# 5
from itertools import permutations
P3 = list(permutations(range(3))); r = ck(F(sum(1 for q in P3 if sum(q[i] == i for i in range(3)) == 1), 6), F(1, 2))
S[5] = SOL([st('Espai mostral.', 'Les cartes 1, 2, 3 es poden col·locar en els sobres 1, 2, 3 de $3!=6$ maneres equiprobables: 123, 132, 213, 231, 312, 321.'),
            st('Casos favorables', '(només una carta al seu sobre): 132 (només la 1), 321 (només la 2) i 213 (només la 3): 3 casos.'),
            st('Regla de Laplace:', r'$$P=\frac36=\frac12$$')], r'$P=\frac12=0{,}5$')
# 8
pA, pB = F(3, 4), F(1, 4); pAl = ck(pA * F('0.1') + pB * F('0.3'), F('0.15')); r = ck(pA * F('0.1') / pAl, F(1, 2))
S[8] = SOL([st('Successos.', r'$A$, $B$: ciutat; $Al=$ «al·lèrgic». $A$ té el triple d’habitants: $P(A)=\frac34$, $P(B)=\frac14$; $P(Al|A)=0{,}1$, $P(Al|B)=0{,}3$.'),
            bayes([('A', pA, F('0.1')), ('B', pB, F('0.3'))], 'Al', 'Āl'),
            st('Probabilitat total:', r'$$P(Al)=\tfrac34\cdot0{,}1+\tfrac14\cdot0{,}3=0{,}075+0{,}075=0{,}15$$'),
            st('Bayes:', r'$$P(A|Al)=\frac{0{,}075}{0{,}15}=0{,}5$$')], r'$P(Al)=0{,}15$; $P(A|Al)=0{,}5$')
# 9
pM = ck(F(1, 3) * 1 + F(1, 3) * F(1, 2) * 2, F(2, 3)); r = ck(F(1, 6) / (1 - pM), F(1, 2))
S[9] = SOL([st('Successos.', r'$A$, $B$, $C$: emissora sintonitzada, $P(A)=P(B)=P(C)=\frac13$; $M=$ «sentim música»: $P(M|A)=1$, $P(M|B)=P(M|C)=\frac12$.'),
            bayes([('A', F(1, 3), F(1)), ('B', F(1, 3), F(1, 2)), ('C', F(1, 3), F(1, 2))], 'M', 'M̄'),
            st('a) Probabilitat total:', r'$$P(M)=\tfrac13\cdot1+\tfrac13\cdot\tfrac12+\tfrac13\cdot\tfrac12=\tfrac23$$'),
            st('b) Bayes:', r'$$P(B|\overline M)=\frac{\frac13\cdot\frac12}{1-\frac23}=\frac{1/6}{1/3}=\frac12$$')], r'a) $\frac23$; b) $\frac12$')
# 11
pL = ck(F('0.6') * F('0.3') + F('0.4') * F('0.5'), F('0.38')); r = ck(F('0.6') * F('0.7') / (1 - pL), F(21, 31))
S[11] = SOL([st('Successos.', r'$D=$ «xica» ($0{,}6$), $H=$ «xic» ($0{,}4$), $L=$ «llig COMIC»: $P(L|D)=0{,}3$, $P(L|H)=0{,}5$.'),
             bayes([('D', F('0.6'), F('0.3')), ('H', F('0.4'), F('0.5'))], 'L', 'L̄'),
             st('a)', r'$$P(L)=0{,}6\cdot0{,}3+0{,}4\cdot0{,}5=0{,}18+0{,}2=0{,}38$$'),
             st('b) Bayes:', L(r'$$P(D|\overline L)=\frac{0{,}6\cdot0{,}7}{1-0{,}38}=\frac{0{,}42}{0{,}62}=@r$$', r=N(r)))], L(r'a) $0{,}38$; b) $@r$', r=N(r)))
# 12
a = ck(F(10, 18) * F(3, 17) * F(5, 16), F(25, 816)); b = ck(6 * a, F(75, 408))
S[12] = SOL([st('Dades.', 'Hi ha 18 caramels: 10 de taronja (T), 5 de llima (L) i 3 de maduixa (M). S’extrauen sense reemplaçament.'),
             st('a) Regla del producte:', L(r'$$P(T_1\cap M_2\cap L_3)=\frac{10}{18}\cdot\frac{3}{17}\cdot\frac{5}{16}=\frac{150}{4896}=@a$$', a=N(a))),
             st('b)', L(r'Els tres sabors poden eixir en $3!=6$ ordres diferents i tots tenen la mateixa probabilitat (canvia l’ordre dels factors del numerador): $$P=6\cdot\frac{150}{4896}=@b$$', b=N(b)))],
            L('a) $@a$; b) $@b$', a=N(a), b=N(b)))
# 13
pN = ck(F(3, 4) * F('0.5') + F(1, 4) * F('0.7'), F(11, 20)); r = ck(F(3, 8) / pN, F(15, 22))
S[13] = SOL([st('Successos.', r'$B_1$, $B_2$: biblioteca. $P(B_1)=3P(B_2)$ i $P(B_1)+P(B_2)=1$, per tant $P(B_1)=\frac34$, $P(B_2)=\frac14$. $N=$ «novel·la»: $P(N|B_1)=0{,}5$, $P(N|B_2)=0{,}7$.'),
             bayes([('B₁', F(3, 4), F('0.5')), ('B₂', F(1, 4), F('0.7'))], 'N', 'N̄'),
             st('a)', r'$$P(N)=\tfrac34\cdot0{,}5+\tfrac14\cdot0{,}7=0{,}375+0{,}175=0{,}55$$'),
             st('b) Bayes:', L(r'$$P(B_1|N)=\frac{0{,}375}{0{,}55}=@r$$', r=N(r)))], L(r'a) $0{,}55$; b) $@r$', r=N(r)))
# 14
pP = ck(F('0.75') * F('0.6') + F('0.25') * F('0.9'), F('0.675')); r = ck(F('0.225') / pP, F(1, 3))
S[14] = SOL([st('Successos.', r'$T=$ «transport» ($0{,}75$), $C=$ «caminant» ($0{,}25$), $P=$ «puntual»: $P(P|T)=0{,}6$, $P(P|C)=0{,}9$.'),
             bayes([('T', F('0.75'), F('0.6')), ('C', F('0.25'), F('0.9'))], 'P', 'P̄'),
             st('Probabilitat total:', r'$P(P)=0{,}45+0{,}225=0{,}675$.'),
             st('a) Bayes:', L(r'$$P(C|P)=\frac{0{,}225}{0{,}675}=@r$$', r=N(r))), st('b)', r'$P(\overline P)=1-0{,}675=0{,}325$.')],
            L(r'a) $@r$; b) $0{,}325$', r=N(r)))
# 15
a = ck(1 - F('0.1') * F('0.2'), F('0.98')); b = ck(F('0.9') * F('0.2'), F('0.18'))
S[15] = SOL([st('Successos.', r'$A_1$, $A_2$: el programa detecta el virus. Són independents: $P(A_1)=0{,}9$, $P(A_2)=0{,}8$.'),
             st('a)', r'Es detecta si almenys un el detecta; el contrari és que cap no el detecte: $$P(A_1\cup A_2)=1-P(\overline{A_1})P(\overline{A_2})=1-0{,}1\cdot0{,}2=0{,}98$$'),
             st('b)', r'$$P(A_1\cap\overline{A_2})=0{,}9\cdot0{,}2=0{,}18$$')], r'a) $0{,}98$; b) $0{,}18$')
# 16
a = ck(F('0.75') * F('0.3') + F('0.25') * F('0.05'), F('0.2375')); b = ck(F('0.75') * F('0.7'), F('0.525'))
S[16] = SOL([st('Successos.', r'$R=$ «ha rebut propaganda» ($0{,}75$), $U=$ «ha utilitzat el videojoc»: $P(U|R)=0{,}3$, $P(U|\overline R)=0{,}05$.'),
             bayes([('R', F('0.75'), F('0.3')), ('R̄', F('0.25'), F('0.05'))], 'U', 'Ū'),
             st('a)', r'$$P(U)=0{,}75\cdot0{,}3+0{,}25\cdot0{,}05=0{,}225+0{,}0125=0{,}2375$$'), st('b)', r'$$P(R\cap\overline U)=0{,}75\cdot0{,}7=0{,}525$$')],
            r'a) $0{,}2375$; b) $0{,}525$')
# 17
a = ck(F('0.6') * F('0.4') + F('0.4') * F('0.3'), F('0.36')); b = ck(F('0.4') * F('0.7'), F('0.28'))
S[17] = SOL([st('Successos.', r'$E=$ «espanyol» ($0{,}6$), $M=$ «menor de 20 anys»: $P(M|E)=0{,}4$, $P(M|\overline E)=0{,}3$.'),
             bayes([('E', F('0.6'), F('0.4')), ('Ē', F('0.4'), F('0.3'))], 'M', 'M̄'),
             st('a)', r'$$P(M)=0{,}24+0{,}12=0{,}36$$'), st('b)', r'$$P(\overline E\cap\overline M)=0{,}4\cdot0{,}7=0{,}28$$')], r'a) $0{,}36$; b) $0{,}28$')
# 18
pa, pb = F(50, 300), F(250, 300); a = ck(pb * F('0.9'), F('0.75')); pD = pa * F('0.01') + pb * F('0.1'); b = ck(pa * F('0.01') / pD, F(1, 51))
S[18] = SOL([st('Successos.', r'En una hora es fan 300 peces: $P(A)=\frac{50}{300}=\frac16$, $P(B)=\frac{250}{300}=\frac56$. $D=$ «defectuosa»: $P(D|A)=0{,}01$, $P(D|B)=0{,}1$.'),
             bayes([('A', pa, F('0.01')), ('B', pb, F('0.1'))], 'D', 'D̄'),
             st('a)', r'$$P(B\cap\overline D)=\tfrac56\cdot0{,}9=0{,}75$$'),
             st('b) Bayes:', L(r'$$P(D)=\tfrac16\cdot0{,}01+\tfrac56\cdot0{,}1=@pd,\qquad P(A|D)=\frac{\frac16\cdot0{,}01}{@pd}=@b$$', pd=N(pD), b=N(b)))],
            L(r'a) $0{,}75$; b) $@b$', b=N(b)))
# 19
pOL = ck(F('0.4') * F('0.2'), F('0.08')); pO = ck(pOL + F('0.1'), F('0.18')); c = ck(pOL / pO, F(4, 9))
S[19] = SOL([st('Successos.', r'$L=$ «ha rebut un curs de LINUX», $O=$ «té ordinador a casa». $P(L)=0{,}4$, $P(O|L)=0{,}2$, $P(O\cap\overline L)=0{,}1$.'),
             st('a)', r'$$P(O\cap L)=P(L)P(O|L)=0{,}4\cdot0{,}2=0{,}08$$'), st('b)', r'$$P(O)=P(O\cap L)+P(O\cap\overline L)=0{,}08+0{,}1=0{,}18$$'),
             st('c)', L(r'$$P(L|O)=\frac{0{,}08}{0{,}18}=@c$$', c=N(c)))], L(r'a) $0{,}08$; b) $0{,}18$; c) $@c$', c=N(c)))
# 20
pR = ck(F(2, 3) * F('0.25') + F(1, 3) * F('0.1'), F(1, 5)); a = ck(F(1, 6) / pR, F(5, 6)); b = ck(F(1, 3) * F('0.9'), F('0.3'))
S[20] = SOL([st('Successos.', r'Hi ha el doble de dones que d’homes: $P(D)=\frac23$, $P(H)=\frac13$. $R=$ «ros»: $P(R|D)=0{,}25$, $P(R|H)=0{,}1$.'),
             bayes([('D', F(2, 3), F('0.25')), ('H', F(1, 3), F('0.1'))], 'R', 'R̄'),
             st('a)', r'$$P(R)=\tfrac23\cdot0{,}25+\tfrac13\cdot0{,}1=\tfrac16+\tfrac1{30}=\tfrac15,\qquad P(D|R)=\frac{1/6}{1/5}=\frac56$$'),
             st('b)', r'$$P(H\cap\overline R)=\tfrac13\cdot0{,}9=0{,}3$$')], r'a) $\frac56\approx0{,}8333$; b) $0{,}3$')
# 21
u = ck(F('0.5') + F('0.3') - F('0.1'), F('0.7'))
S[21] = SOL([st('Unió:', r'$P(A\cup B)=0{,}5+0{,}3-0{,}1=0{,}7$'), st('Condicionada:', r'$P(A|B)=\dfrac{P(A\cap B)}{P(B)}=\dfrac{0{,}1}{0{,}3}=\dfrac13\approx0{,}3333$'),
             st('$P(A|A\\cap B)$:', r'com que $A\cap B\subset A$, $A\cap(A\cap B)=A\cap B$ i $P(A|A\cap B)=\dfrac{P(A\cap B)}{P(A\cap B)}=1$.'),
             st('$P(A|A\\cup B)$:', r'com que $A\subset A\cup B$, $A\cap(A\cup B)=A$: $P(A|A\cup B)=\dfrac{0{,}5}{0{,}7}=\dfrac57\approx0{,}7143$.')],
            r'$0{,}7$; $\frac13$; $1$; $\frac57$')
# 22
pT = ck(F(1, 2) * F(15, 25) + F(1, 2) * F(20, 45), F(47, 90)); b = ck(F(1, 2) * F(25, 45) / (1 - pT), F(25, 43))
S[22] = SOL([st('Successos.', r'$B_1$, $B_2$: bossa triada ($\frac12$ cada una); $T=$ «taronja»: $P(T|B_1)=\frac{15}{25}$, $P(T|B_2)=\frac{20}{45}$.'),
             bayes([('B₁', F(1, 2), F(15, 25)), ('B₂', F(1, 2), F(20, 45))], 'T', 'L'),
             st('a)', L(r'$$P(T)=\tfrac12\cdot\tfrac{15}{25}+\tfrac12\cdot\tfrac{20}{45}=@a$$', a=N(pT))),
             st('b) Bayes:', L(r'$$P(B_2|L)=\frac{\frac12\cdot\frac{25}{45}}{1-\frac{47}{90}}=\frac{25/90}{43/90}=@b$$', b=N(b)))], L(r'a) $@a$; b) $@b$', a=N(pT), b=N(b)))
# 23
S[23] = SOL([st('a)', r'$P(M)P(E)=0{,}15\cdot0{,}3=0{,}045\neq0{,}1=P(M\cap E)$: <strong>no</strong> són independents.'),
             st('b) De Morgan:', r'$P(M\cup E)=0{,}15+0{,}3-0{,}1=0{,}35\ \Rightarrow\ P(\overline M\cap\overline E)=1-0{,}35=0{,}65$')], r'a) No; b) $0{,}65$')
# 24
pU = ck(F(3, 4) * F('0.22') + F(1, 4) * F('0.5'), F('0.29')); c = ck(F('0.165') / pU, F(33, 58))
S[24] = SOL([st('Successos.', r'Hi ha tres vegades més xiques que xics: $P(D)=\frac34$, $P(H)=\frac14$. $U=$ «porta ulleres»: $P(U|D)=0{,}22$, $P(U|H)=0{,}5$.'),
             bayes([('D', F(3, 4), F('0.22')), ('H', F(1, 4), F('0.5'))], 'U', 'Ū'),
             st('a)', r'$P(U)=0{,}165+0{,}125=0{,}29\Rightarrow P(\overline U)=0{,}71$'), st('b)', r'$P(D\cap U)=0{,}75\cdot0{,}22=0{,}165$'),
             st('c)', L(r'$P(D|U)=\dfrac{0{,}165}{0{,}29}=@c$', c=N(c)))], L(r'a) $0{,}71$; b) $0{,}165$; c) $@c$', c=N(c)))
# 25
pA = F('0.6'); pB = ck(F('0.9') - pA + F('0.2'), F('0.5'))
S[25] = SOL([st('Dades.', r'$P(A)=1-P(\overline A)=0{,}6$.'), st('$P(B)$:', r'$0{,}9=0{,}6+P(B)-0{,}2\Rightarrow P(B)=0{,}5$'),
             st('$P(A|B)$:', r'$\dfrac{0{,}2}{0{,}5}=0{,}4$'), st('$P(A\\cap\\overline B)$:', r'$P(A)-P(A\cap B)=0{,}6-0{,}2=0{,}4$'),
             st('$P(\\overline A\\cup\\overline B)$:', r'De Morgan: $1-P(A\cap B)=0{,}8$'), ct(pA, pB, F('0.2'))], r'$0{,}5$; $0{,}4$; $0{,}4$; $0{,}8$')
# 26
pr = [F(1000, 5000), F(1500, 5000), F(2500, 5000)]; dd = [F('0.011'), F('0.011'), F('0.03')]; pD = ck(sum(a * b for a, b in zip(pr, dd)), F('0.0205')); b = ck(pr[2] * dd[2] / pD, F(30, 41))
S[26] = SOL([st('Successos.', r'De les 5000 unitats diàries: $P(F_1)=0{,}2$, $P(F_2)=0{,}3$, $P(F_3)=0{,}5$. $D=$ «defectuosa»: $0{,}011$, $0{,}011$, $0{,}03$.'),
             bayes([('F₁', pr[0], dd[0]), ('F₂', pr[1], dd[1]), ('F₃', pr[2], dd[2])], 'D', 'D̄'),
             st('a)', r'$P(D)=0{,}2\cdot0{,}011+0{,}3\cdot0{,}011+0{,}5\cdot0{,}03=0{,}0205\Rightarrow P(\overline D)=0{,}9795$ (un $97{,}95\,\%$).'),
             st('b) Bayes:', L(r'$P(F_3|D)=\dfrac{0{,}015}{0{,}0205}=@b$', b=N(b)))], L(r'a) $0{,}9795$; b) $@b$', b=N(b)))
# 27
pU = 1 - F('0.55'); pR = ck(pU - F('0.35') + F('0.1'), F('0.2'))
S[27] = SOL([st('Successos.', r'$M=$ «escolta Music», $R=$ «escolta Rhythm». $P(M\cap R)=0{,}1$, $P(M)=0{,}35$, $P(\overline M\cap\overline R)=0{,}55$, és a dir $P(M\cup R)=0{,}45$.'),
             st('a)', r'$0{,}45=0{,}35+P(R)-0{,}1\Rightarrow P(R)=0{,}2$'), st('b)', r'$P(R\cap\overline M)=0{,}2-0{,}1=0{,}1$'), st('c)', r'$P(M|R)=\dfrac{0{,}1}{0{,}2}=0{,}5$'),
             ct(F('0.35'), pR, F('0.1'), 'M', 'R')], r'a) $0{,}2$; b) $0{,}1$; c) $0{,}5$')
# 28
S[28] = SOL([st('Plantejament.', r'Siguen $p=P(A)$ i $q=P(B)$. Com que són independents, $pq=\frac{3}{25}$; i $P(A\cup B)=p+q-pq=\frac{17}{25}\Rightarrow p+q=\frac{20}{25}=\frac45$.'),
             st('Equació de segon grau:', r'$p$ i $q$ són les solucions de $t^2-\frac45t+\frac3{25}=0\iff25t^2-20t+3=0$: $$t=\frac{20\pm\sqrt{400-300}}{50}=\frac{20\pm10}{50}\Rightarrow t=\frac35,\ t=\frac15$$')],
            r'Les probabilitats són $\frac35$ i $\frac15$.')
ck(F(3, 5) * F(1, 5), F(3, 25)); ck(F(3, 5) + F(1, 5) - F(3, 25), F(17, 25))
# 29
v = F(1, 145); pP = ck(v * F('0.96') + (1 - v) * F('0.06'), F(48, 725)); b = ck(v * F('0.96') / pP, F('0.1')); c = ck((1 - v) * F('0.94'), F(3384, 3625))
S[29] = SOL([st('Successos.', r'$V=$ «és portador»: $P(V)=\frac1{145}$. $+=$ «test positiu»: $P(+|V)=0{,}96$, $P(-|\overline V)=0{,}94\Rightarrow P(+|\overline V)=0{,}06$.'),
             bayes([('V', v, F('0.96')), ('V̄', 1 - v, F('0.06'))], '+', '−'),
             st('a)', L(r'$$P(+)=\tfrac1{145}\cdot0{,}96+\tfrac{144}{145}\cdot0{,}06=\frac{9{,}6}{145}=@a$$', a=N(pP))),
             st('b) Bayes:', r'$$P(V|+)=\frac{0{,}96/145}{9{,}6/145}=0{,}1$$'), st('c)', L(r'$$P(-\cap\overline V)=\tfrac{144}{145}\cdot0{,}94=@c$$', c=N(c)))],
            L(r'a) $@a$; b) $0{,}1$; c) $@c$', a=N(pP), c=N(c)))
# 30
pA = ck(F('0.1') * F('0.97') + F('0.9') * F('0.02'), F('0.115')); b = ck(F('0.018') / pA, F(18, 115))
S[30] = SOL([st('Successos.', r'$I=$ «incident» ($0{,}1$), $S=$ «sona l’alarma»: $P(S|I)=0{,}97$, $P(S|\overline I)=0{,}02$.'),
             bayes([('I', F('0.1'), F('0.97')), ('Ī', F('0.9'), F('0.02'))], 'S', 'S̄'),
             st('a)', r'$P(S)=0{,}097+0{,}018=0{,}115\Rightarrow P(\overline S)=0{,}885$'), st('b) Bayes:', L(r'$P(\overline I|S)=\dfrac{0{,}018}{0{,}115}=@b$', b=N(b)))],
            L(r'a) $0{,}885$; b) $@b$', b=N(b)))
# 31
i = ck(F('0.4') + F('0.6') - F('0.7'), F('0.3'))
S[31] = SOL([st('Intersecció:', r'$P(A\cap B)=0{,}4+0{,}6-0{,}7=0{,}3$'), st('a)', r'$P(A)P(B)=0{,}24\neq0{,}3$: <strong>no</strong> són independents.'),
             st('b)', r'$P(A\cap\overline B)=0{,}4-0{,}3=0{,}1$'), st('c)', r'De Morgan: $P(\overline A\cap\overline B)=1-P(A\cup B)=0{,}3$'), ct(F('0.4'), F('0.6'), i)],
            r'a) No; b) $0{,}1$; c) $0{,}3$')
# 32
p, q = F(2, 3), F(3, 4)
S[32] = SOL([st('Successos.', r'$A$, $B$: encerta cada tirador. Són independents: $P(A)=\frac23$, $P(B)=\frac34$.'),
             st('a)', r'$P(A\cap B)=\frac23\cdot\frac34=\frac12$'), st('b)', r'$P(A\cap\overline B)+P(\overline A\cap B)=\frac23\cdot\frac14+\frac13\cdot\frac34=\frac{2+3}{12}=\frac5{12}$'),
             st('c)', r'$P(\overline A\cap\overline B)=\frac13\cdot\frac14=\frac1{12}$'), st('d)', r'$1-\frac1{12}=\frac{11}{12}$'),
             st('e)', r'$\frac12+\frac5{12}+\frac1{12}=1$: «encerten els dos», «n’encerta exactament un» i «no n’encerta cap» són incompatibles i un d’ells ha de passar sempre (formen un sistema complet).')],
            r'a) $\frac12$; b) $\frac5{12}$; c) $\frac1{12}$; d) $\frac{11}{12}$; e) $1$')
ck(p * q + p * (1 - q) + (1 - p) * q + (1 - p) * (1 - q), 1); ck(p * (1 - q) + (1 - p) * q, F(5, 12))
# 33
pB = ck(F('0.1') / F('0.2'), F('0.5')); pA = ck(F('0.7') - pB + F('0.1'), F('0.3'))
S[33] = SOL([st('a)', r'$P(B)=\dfrac{P(A\cap B)}{P(A|B)}=\dfrac{0{,}1}{0{,}2}=0{,}5$; $\ 0{,}7=P(A)+0{,}5-0{,}1\Rightarrow P(A)=0{,}3$.'),
             st('b)', r'$P(A)P(B)=0{,}15\neq0{,}1$: <strong>no</strong> són independents.'),
             st('c)', r'$\overline A\cup B$ és el contrari de $A\cap\overline B$: $P(\overline A\cup B)=1-(0{,}3-0{,}1)=0{,}8$.'), ct(pA, pB, F('0.1'))],
            r'a) $P(A)=0{,}3$, $P(B)=0{,}5$; b) No; c) $0{,}8$')
# 34
a = ck(F('0.6') + F('0.4') * F('0.8'), F('0.92')); b = ck(F('0.6') / a, F(15, 23))
S[34] = SOL([st('Successos.', r'$J=$ «aprova al juny» ($0{,}6$); els que suspenen ($0{,}4$) es presenten al setembre i hi aprova el $80\,\%$.'),
             st('a)', r'$P(\text{aprova})=0{,}6+0{,}4\cdot0{,}8=0{,}92$'), st('b)', L(r'$P(J|\text{aprova})=\dfrac{0{,}6}{0{,}92}=@b$', b=N(b)))], L(r'a) $0{,}92$; b) $@b$', b=N(b)))
# 35
pr = [F('0.4'), F('0.3'), F('0.2'), F('0.1')]; dd = [F('0.05'), F('0.04'), F('0.03'), F('0.02')]
pD = ck(sum(a * b for a, b in zip(pr, dd)), F('0.04')); b = ck(pr[2] * (1 - dd[2]) / (1 - pD), F(97, 480))
S[35] = SOL([bayes([('A', pr[0], dd[0]), ('B', pr[1], dd[1]), ('C', pr[2], dd[2]), ('D', pr[3], dd[3])], 'Def', 'D̄ef'),
             st('a) Probabilitat total:', r'$P(Def)=0{,}4\cdot0{,}05+0{,}3\cdot0{,}04+0{,}2\cdot0{,}03+0{,}1\cdot0{,}02=0{,}04$'),
             st('b) Bayes:', L(r'$P(C|\overline{Def})=\dfrac{0{,}2\cdot0{,}97}{0{,}96}=@b$', b=N(b)))], L(r'a) $0{,}04$; b) $@b$', b=N(b)))
# 36
S[36] = SOL([st('a)', r'$P(A\cap B)=P(B)P(A|B)=0{,}2\cdot1=0{,}2$; $\ P(A\cup B)=0{,}7+0{,}2-0{,}2=0{,}7$; $\ P(B|A)=\dfrac{0{,}2}{0{,}7}=\dfrac27\approx0{,}2857$.'),
             st('b)', r'$P(A|B)=1\neq P(A)=0{,}7$: <strong>no</strong> són independents (de fet $B\subset A$).')], r'a) $0{,}2$; $0{,}7$; $\frac27$; b) No')
# 37
u = 1 - F('0.3'); i = ck(F('0.2') + F('0.5') - u, 0)
S[37] = SOL([st('Successos.', r'$A$, $B$: li agrada cada grup. $P(A)=0{,}2$, $P(B)=0{,}5$, $P(\overline A\cap\overline B)=0{,}3$.'),
             st('a)', r'$P(A\cup B)=1-0{,}3=0{,}7\Rightarrow P(A\cap B)=0{,}2+0{,}5-0{,}7=0$'), st('b)', r'$P(A\cup B)=0{,}7$'), st('c)', r'$P(B\cap\overline A)=0{,}5-0=0{,}5$')],
            r'a) $0$ (són incompatibles); b) $0{,}7$; c) $0{,}5$')
# 38
pB = ck(F('0.48') * F('0.3') + F('0.52') * F('0.35'), F('0.326')); a = ck(F('0.144') / pB, F(72, 163)); b = ck(F('0.48') + F('0.52') * F('0.65'), F('0.818'))
S[38] = SOL([st('Successos.', r'$H=$ «home» ($0{,}52$), $D=$ «dona» ($0{,}48$). Cadascú creu que guanya $A$ o $B$: $P(A|D)=0{,}7$, $P(B|H)=0{,}35$.'),
             arbre([('D', F('0.48'), [('A', F('0.7'), False), ('B', F('0.3'), True)]), ('H', F('0.52'), [('A', F('0.65'), False), ('B', F('0.35'), True)])]),
             st('a)', L(r'$P(B)=0{,}48\cdot0{,}3+0{,}52\cdot0{,}35=0{,}326$; $\ P(D|B)=\dfrac{0{,}144}{0{,}326}=@a$', a=N(a))),
             st('b)', r'$P(D\cup A)=P(D)+P(H\cap A)=0{,}48+0{,}52\cdot0{,}65=0{,}818$')], L(r'a) $@a$; b) $0{,}818$', a=N(a)))
# 39
i = ck(F('0.5') + F('0.4') - F('0.75'), F('0.15'))
S[39] = SOL([st('Dades.', r'$P(A)=0{,}5$, $P(B)=0{,}4$, $P(\overline A\cap\overline B)=0{,}25\Rightarrow P(A\cup B)=0{,}75$.'),
             st('a)', r'$A\cap B$: $\ P(A\cap B)=0{,}5+0{,}4-0{,}75=0{,}15$'), st('b)', r'$(A\cap\overline B)\cup(\overline A\cap B)$: $\ P=0{,}75-0{,}15=0{,}6$'),
             st('c)', r'$P(B|A)=\dfrac{0{,}15}{0{,}5}=0{,}3$'), ct(F('0.5'), F('0.4'), i)], r'a) $0{,}15$; b) $0{,}6$; c) $0{,}3$')
# 40
S[40] = SOL([st('Successos.', r'$T=$ «turisme» ($0{,}75$), $TT=$ «tot terreny» ($0{,}25$), $P=$ «és el primer cotxe»: $P(P|TT)=0{,}2$, $P(P|T)=0{,}4$.'),
             bayes([('T', F('0.75'), F('0.4')), ('TT', F('0.25'), F('0.2'))], 'P', 'P̄'),
             st('a)', r'$P(P)=0{,}3+0{,}05=0{,}35\Rightarrow P(\overline P)=0{,}65$'), st('b)', r'$P(T|P)=\dfrac{0{,}3}{0{,}35}=\dfrac67\approx0{,}8571$'),
             st('c)', r'$P(\overline P\cap TT)=0{,}25\cdot0{,}8=0{,}2$')], r'a) $0{,}65$; b) $\frac67$; c) $0{,}2$')
ck(F('0.3') / F('0.35'), F(6, 7))
# 41
i = ck(F('0.1') * F('0.9'), F('0.09')); pB = ck(i / F('0.2'), F('0.45'))
S[41] = SOL([st('a)', r'$p(A\cap B)=p(A)p(B|A)=0{,}1\cdot0{,}9=0{,}09$; $\ p(B)=\dfrac{0{,}09}{0{,}2}=0{,}45$'),
             st('b)', r'$p(A)p(B)=0{,}045\neq0{,}09$: <strong>no</strong> són independents.'),
             st('c)', r'$A\cup\overline B$ és el contrari de $\overline A\cap B$: $1-(0{,}45-0{,}09)=0{,}64$'), ct(F('0.1'), pB, i)], r'a) $0{,}09$; $0{,}45$; b) No; c) $0{,}64$')
# 42
vf = F('0.8') * F('0.75'); pf = ck(F('0.96') - F('0.8') + vf, F('0.76'))
S[42] = SOL([st('Successos.', r'$V=$ «li agrada el vi» ($0{,}8$), $C=$ «li agrada el formatge»: $P(C|V)=0{,}75$; $P(\overline V\cap\overline C)=0{,}04$.'),
             st('a)', r'$P(V\cap C)=0{,}8\cdot0{,}75=0{,}6$: el $60\,\%$.'),
             st('b)', r'$P(V\cup C)=0{,}96\Rightarrow P(C)=0{,}96-0{,}8+0{,}6=0{,}76\Rightarrow P(\overline C)=0{,}24$: el $24\,\%$.'),
             st('c)', r'$P(V|C)=\dfrac{0{,}6}{0{,}76}=\dfrac{15}{19}\approx0{,}7895$'), st('d)', r'$P(V|\overline C)=\dfrac{0{,}2}{0{,}24}=\dfrac56\approx0{,}8333$: un $83{,}33\,\%$.'),
             ct(F('0.8'), pf, vf, 'V', 'C')], r'a) $60\,\%$; b) $24\,\%$; c) $\frac{15}{19}$; d) $83{,}33\,\%$')
ck(F('0.6') / F('0.76'), F(15, 19)); ck(F('0.2') / F('0.24'), F(5, 6))
# 43
pr = [F(1, 4), F(1, 3), F(5, 12)]; sk = [F('0.8'), F('0.6'), F('0.4')]; pE = ck(sum(a * b for a, b in zip(pr, sk)), F(17, 30))
b = ck(pr[1] * F('0.4') / (1 - pE), F(4, 13)); c = ck((pr[0] * sk[0] + pr[2] * sk[2]) / pE, F(11, 17))
S[43] = SOL([st('Successos.', r'$P$ (petit) $=\frac14$, $M$ (mitjà) $=\frac13$, $G$ (gran) $=1-\frac14-\frac13=\frac5{12}$; $E=$ «sap esquiar»: $0{,}8$, $0{,}6$, $0{,}4$.'),
             bayes([('P', pr[0], sk[0]), ('M', pr[1], sk[1]), ('G', pr[2], sk[2])], 'E', 'Ē'),
             st('a)', L(r'$P(E)=\tfrac14\cdot0{,}8+\tfrac13\cdot0{,}6+\tfrac5{12}\cdot0{,}4=0{,}2+0{,}2+\tfrac16=@a$', a=N(pE))),
             st('b)', L(r'$P(M|\overline E)=\dfrac{\frac13\cdot0{,}4}{1-\frac{17}{30}}=@b$', b=N(b))), st('c)', L(r'$P(G\cup P|E)=\dfrac{\frac16+0{,}2}{\frac{17}{30}}=@c$', c=N(c)))],
            L(r'a) $@a$; b) $@b$; c) $@c$', a=N(pE), b=N(b), c=N(c)))
# 44
a = ck(F('0.6') * F(1, 2) + F('0.4'), F('0.7')); b = ck(F('0.3') / a, F(3, 7)); c = ck(2 * F(6, 10) * F(4, 9), F(8, 15))
S[44] = SOL([st('Successos.', r'$L=$ «moneda legal» ($\frac{6}{10}$), $D=$ «dues cares» ($\frac4{10}$), $C=$ «ix cara»: $P(C|L)=\frac12$, $P(C|D)=1$.'),
             bayes([('L', F(6, 10), F(1, 2)), ('D', F(4, 10), F(1))], 'C', '+'),
             st('a)', r'$P(C)=0{,}6\cdot0{,}5+0{,}4\cdot1=0{,}7$'), st('b)', r'$P(L|C)=\dfrac{0{,}3}{0{,}7}=\dfrac37\approx0{,}4286$'),
             st('c)', r'Sense reemplaçament, la legal pot eixir la primera o la segona: $$P=\frac{6}{10}\cdot\frac49+\frac4{10}\cdot\frac69=\frac{48}{90}=\frac8{15}$$')],
            r'a) $0{,}7$; b) $\frac37$; c) $\frac8{15}\approx0{,}5333$')
# 45
pA = ck(F('0.25') * F('0.7') + F('0.6') * F('0.8') + F('0.15') * F('0.9'), F('0.79')); b = ck(F('0.48') / pA, F(48, 79))
S[45] = SOL([bayes([('T', F('0.25'), F('0.7')), ('H', F('0.6'), F('0.8')), ('A', F('0.15'), F('0.9'))], 'Ap', 'Āp'),
             st('a)', r'$P(Ap)=0{,}175+0{,}48+0{,}135=0{,}79\Rightarrow P(\overline{Ap})=0{,}21$'), st('b)', L(r'$P(H|Ap)=\dfrac{0{,}48}{0{,}79}=@b$', b=N(b)))],
            L(r'a) $0{,}21$; b) $@b$', b=N(b)))
# 46
i = ck(F('0.75') - F('0.3'), F('0.45')); pB = ck(i + (F('0.25') - F('0.15')), F('0.55'))
S[46] = SOL([st('Dades.', r'$P(A)=0{,}75$, $P(A\cap\overline B)=0{,}3$, $P(\overline A\cap\overline B)=0{,}15$.'),
             st('a)', r'$P(A\cap B)=0{,}75-0{,}3=0{,}45$'), st('b)', r'$P(\overline A\cap B)=0{,}25-0{,}15=0{,}1\Rightarrow P(B)=0{,}45+0{,}1=0{,}55$'),
             st('c)', r'$P(\overline B|A)=\dfrac{0{,}3}{0{,}75}=0{,}4$'), ct(F('0.75'), pB, i)], r'a) $0{,}45$; b) $0{,}55$; c) $0{,}4$')
# 47
pD = ck(F('0.625') * F('0.8') + F('0.375') * F(1, 3), F('0.625')); c = ck(F('0.625') * F('0.2') / (1 - pD), F(1, 3))
S[47] = SOL([st('Successos.', r'$A=$ «parla anglés» ($0{,}625$), $D=$ «parla alemany»: $P(D|A)=0{,}8$, $P(D|\overline A)=\frac13$.'),
             bayes([('A', F('0.625'), F('0.8')), ('Ā', F('0.375'), F(1, 3))], 'D', 'D̄'),
             st('a)', r'$P(A\cap D)=0{,}625\cdot0{,}8=0{,}5$: el $50\,\%$.'), st('b)', r'$P(D)=0{,}5+0{,}375\cdot\frac13=0{,}625$: el $62{,}5\,\%$.'),
             st('c)', r'$P(A|\overline D)=\dfrac{0{,}625\cdot0{,}2}{0{,}375}=\dfrac13$')], r'a) $50\,\%$; b) $62{,}5\,\%$; c) $\frac13$')
# 48
S[48] = SOL([st('Taula.', 'Hi ha 50 alumnes; cursen francés 4 del grup A i 5 del B.' + taula(['A', 'B'], [r'\text{Francés}', r'\text{No francés}'], [[4, 21, 25], [5, 20, 25], [9, 41, 50]], str)),
             st('a)', r'$P(\overline F)=\frac{41}{50}=0{,}82$'), st('b)', r'$P(B|F)=\frac59\approx0{,}5556$'), st('c)', r'Del grup A, els xics que no cursen francés són $15-2=13$: $P=\frac{13}{25}=0{,}52$.')],
            r'a) $0{,}82$; b) $\frac59$; c) $0{,}52$')
# 49
S[49] = SOL([st('Independència.', r'$S=$ «soci» ($0{,}15$), $R=$ «pèl-roig» ($0{,}03$), independents: $P(S\cap R)=0{,}15\cdot0{,}03=0{,}0045$.'),
             st('a)', r'$P(R\cap\overline S)=0{,}03\cdot0{,}85=0{,}0255$'), st('b)', r'$P(R\cup S)=0{,}03+0{,}15-0{,}0045=0{,}1755$'), st('c)', r'Per independència, $P(S|\overline R)=P(S)=0{,}15$.')],
            r'a) $0{,}0255$; b) $0{,}1755$; c) $0{,}15$')
ck(F('0.03') + F('0.15') - F('0.0045'), F('0.1755'))
# 50
pR = ck(F(1, 3) * (0 + F(1, 2) + F(3, 4)), F(5, 12)); b = ck(F(1, 6) / pR, F(2, 5))
S[50] = SOL([bayes([('U₁', F(1, 3), F(0)), ('U₂', F(1, 3), F(1, 2)), ('U₃', F(1, 3), F(3, 4))], 'R', 'Bl'),
             st('a)', r'$P(R)=\frac13\cdot0+\frac13\cdot\frac24+\frac13\cdot\frac34=\frac5{12}$'), st('b)', r'$P(U_2|R)=\dfrac{1/6}{5/12}=\dfrac25$')], r'a) $\frac5{12}\approx0{,}4167$; b) $\frac25$')
# 51
pN = ck(F(30, 120) * F('0.2') + F(90, 120) * F('0.1'), F('0.125')); b = ck(F(90, 120) * F('0.9') / (1 - pN), F(27, 35)); c = ck(F(30, 120) * F(29, 119), F(29, 476))
S[51] = SOL([st('Successos.', r'$M=$ «l’havia patida» ($\frac{30}{120}=0{,}25$), $R=$ «reacciona positivament»: $P(R|M)=0{,}8$, $P(R|\overline M)=0{,}9$.'),
             bayes([('M', F(1, 4), F('0.8')), ('M̄', F(3, 4), F('0.9'))], 'R', 'R̄'),
             st('a)', r'$P(\overline R)=0{,}25\cdot0{,}2+0{,}75\cdot0{,}1=0{,}125$'), st('b)', r'$P(\overline M|R)=\dfrac{0{,}675}{0{,}875}=\dfrac{27}{35}\approx0{,}7714$'),
             st('c)', r'Sense reemplaçament: $\frac{30}{120}\cdot\frac{29}{119}=\frac{29}{476}\approx0{,}0609$')], r'a) $0{,}125$; b) $\frac{27}{35}$; c) $\frac{29}{476}$')
# 52
a = ck(F(5, 7) * F(5, 6) ** 2 + F(2, 7) * F(4, 6) ** 2, F(157, 252)); b = ck(F(5, 7) * 2 * F(5, 6) * F(1, 6) + F(2, 7) * 2 * F(4, 6) * F(2, 6), F(41, 126))
pR1 = F(5, 7) * F(5, 6) + F(2, 7) * F(4, 6); c = ck(F(2, 7) * F(4, 6) / pR1, F(8, 33))
S[52] = SOL([st('Composició de B.', r'Si passem una roja ($\frac57$), B té 5 roges i 1 blava; si passem una blava ($\frac27$), B té 4 roges i 2 blaves. Després traiem dues boles <em>amb</em> reemplaçament.'),
             st('a)', L(r'$$P(RR)=\tfrac57\left(\tfrac56\right)^2+\tfrac27\left(\tfrac46\right)^2=\frac{125+32}{252}=@a$$', a=N(a))),
             st('b)', L(r'$$P(\text{distint color})=\tfrac57\cdot2\cdot\tfrac56\cdot\tfrac16+\tfrac27\cdot2\cdot\tfrac46\cdot\tfrac26=\frac{50+32}{252}=@b$$', b=N(b))),
             st('c) Bayes:', L(r'$P(R_1)=\tfrac57\cdot\tfrac56+\tfrac27\cdot\tfrac46=\tfrac{33}{42}$; $\ P(\text{blava passada}|R_1)=\dfrac{8/42}{33/42}=@c$', c=N(c)))],
            L(r'a) $@a$; b) $@b$; c) $@c$', a=N(a), b=N(b), c=N(c)))
