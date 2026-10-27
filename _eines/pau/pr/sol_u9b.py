# Solucions dels exercicis PAU de probabilitat (Comunitat Valenciana) números 53-104 del dossier.
from comu import *
S = {}

# 53
a = ck(F(25, 45) * F(24, 44), F(10, 33)); b = ck(F(25 * 24 + 12 * 11 + 8 * 7, 45 * 44), F(197, 495)); c = ck(F(37, 45) * F(36, 44), F(37, 55))
S[53] = SOL([st('Dades.', 'Hi ha 45 caramels: 25 de taronja, 12 de llima i 8 de café. S’extrauen dos a l’atzar (sense reemplaçament).'),
             st('a)', L(r'$\frac{25}{45}\cdot\frac{24}{44}=@a$', a=N(a))), st('b)', L(r'$\frac{25\cdot24+12\cdot11+8\cdot7}{45\cdot44}=\frac{788}{1980}=@b$', b=N(b))),
             st('c)', L(r'Hi ha 37 que no són de café: $\frac{37}{45}\cdot\frac{36}{44}=@c$', c=N(c)))], L(r'a) $@a$; b) $@b$; c) $@c$', a=N(a), b=N(b), c=N(c)))
# 54
i = ck(F('0.4') * F('0.2'), F('0.08'))
S[54] = SOL([st('Intersecció:', r'$P(A\cap B)=P(B)P(A|B)=0{,}4\cdot0{,}2=0{,}08$'),
             st('a)', r'$\overline A\cup B$ és el contrari de $A\cap\overline B$: $P=1-(0{,}3-0{,}08)=0{,}78$'), st('b)', r'$P(B|A)=\dfrac{0{,}08}{0{,}3}=\dfrac4{15}\approx0{,}2667$'),
             st('c)', r'$P(A\cup B)=0{,}3+0{,}4-0{,}08=0{,}62\Rightarrow P(\overline A\cap\overline B)=0{,}38$'), st('d)', r'$P(A|B)=0{,}2\neq P(A)=0{,}3$: <strong>no</strong> són independents.'),
             ct(F('0.3'), F('0.4'), i)], r'a) $0{,}78$; b) $\frac4{15}$; c) $0{,}38$; d) No')
# 55
pr = [F('0.45'), F('0.3'), F('0.25')]; cc = [F('0.03'), F('0.05'), F('0.01')]; pC = ck(sum(x * y for x, y in zip(pr, cc)), F('0.031')); a = ck(F('0.0025') / pC, F(5, 62))
S[55] = SOL([bayes([('X', pr[0], cc[0]), ('Y', pr[1], cc[1]), ('Z', pr[2], cc[2])], 'C', 'C̄'),
             st('Probabilitat total de cancel·lar:', r'$P(C)=0{,}0135+0{,}015+0{,}0025=0{,}031$'),
             st('a)', L(r'$P(Z|C)=\dfrac{0{,}0025}{0{,}031}=@a$', a=N(a))), st('b)', r'$P(\overline C)=0{,}969$'), st('c)', r'$P(X\cap C)=0{,}45\cdot0{,}03=0{,}0135$'),
             st('d)', r'$P(\overline Y\cap C)=P(X\cap C)+P(Z\cap C)=0{,}0135+0{,}0025=0{,}016$')], L(r'a) $@a$; b) $0{,}969$; c) $0{,}0135$; d) $0{,}016$', a=N(a)))
# 56
i = ck(F('0.5') + F('0.4') - F('0.7'), F('0.2'))
S[56] = SOL([st('Intersecció:', r'$P(A\cap B)=0{,}5+0{,}4-0{,}7=0{,}2$'), st('a)', r'$1-0{,}7=0{,}3$'), st('b)', r'$0{,}5-0{,}2=0{,}3$'), st('c)', r'$P(A|B)=\dfrac{0{,}2}{0{,}4}=0{,}5$'),
             st('d)', r'$P(A)P(B)=0{,}2=P(A\cap B)$: <strong>sí</strong> que són independents.'), ct(F('0.5'), F('0.4'), i)], r'a) $0{,}3$; b) $0{,}3$; c) $0{,}5$; d) Sí')
# 57
pr = [F(1, 8), F(3, 8), F(1, 2)]; dd = [F('0.02'), F('0.015'), F('0.005')]; pD = ck(sum(x * y for x, y in zip(pr, dd)), F('0.010625'))
b = ck(pr[0] * dd[0] / pD, F(4, 17)); c = (pr[0] * (1 - dd[0]) + pr[1] * (1 - dd[1])) / (1 - pD); ck(c, F('0.491875') / F('0.989375'))
S[57] = SOL([st('Successos.', r'De les 8000 peces diàries: $P(M_1)=\frac{1000}{8000}=\frac18$, $P(M_2)=\frac38$, $P(M_3)=\frac12$ (la moderna). $D$: $0{,}02$, $0{,}015$, $0{,}005$.'),
             bayes([('M₁', pr[0], dd[0]), ('M₂', pr[1], dd[1]), ('M₃', pr[2], dd[2])], 'D', 'D̄'),
             st('a)', r'$P(D)=\tfrac18\cdot0{,}02+\tfrac38\cdot0{,}015+\tfrac12\cdot0{,}005=0{,}010625$'), st('b)', L(r'$P(M_1|D)=\dfrac{0{,}0025}{0{,}010625}=@b$', b=N(b))),
             st('c)', L(r'$P(\overline{M_3}|\overline D)=\dfrac{\frac18\cdot0{,}98+\frac38\cdot0{,}985}{1-0{,}010625}=\dfrac{0{,}491875}{0{,}989375}=@c$', c=N(c)))],
            L(r'a) $0{,}010625$; b) $@b$; c) $@c$', b=N(b), c=N(c)))
# 58
S[58] = SOL([st('a)', r'$P(I\cup E)=0{,}3+0{,}2-0{,}1=0{,}4$'), st('b)', r'$P(I|E)=\dfrac{0{,}1}{0{,}2}=0{,}5$'), st('c)', r'$P(I\cup E)-P(I\cap E)=0{,}4-0{,}1=0{,}3$'),
             ct(F('0.3'), F('0.2'), F('0.1'), 'I', 'E')], r'a) $0{,}4$; b) $0{,}5$; c) $0{,}3$')
# 59
S[59] = SOL([st('Taula.', taula(['H', 'D'], [r'\text{Grip}', r'\text{No grip}'], [[23, 157, 180], [25, 195, 220], [48, 352, 400]], str)),
             st('a)', r'$\frac{352}{400}=0{,}88$'), st('b)', r'$\frac{195}{400}=0{,}4875$'), st('c)', r'$P(H|\overline G)=\frac{157}{352}\approx0{,}446$'), st('d)', r'$P(\overline G|D)=\frac{195}{220}=\frac{39}{44}\approx0{,}8864$')],
            r'a) $0{,}88$; b) $0{,}4875$; c) $\frac{157}{352}$; d) $\frac{39}{44}$')
# 60, 62 (mateixes dades)
a, b, i = F(2, 3), F(3, 4), F(5, 8); u = ck(a + b - i, F(19, 24))
for n in (60, 62):
    S[n] = SOL([st('Dades.', r'$P(A)=\frac23$, $P(B)=\frac34$' + (r', $P(A\cap B)=\frac58$.' if n == 60 else r' i $P(A\cup B)=\frac{19}{24}\Rightarrow P(A\cap B)=\frac23+\frac34-\frac{19}{24}=\frac{15}{24}=\frac58$.')),
                st('a)', r'$P(A\cup B)=\frac{19}{24}\approx0{,}7917$' if n == 60 else r'$P(A\cap B)=\frac58=0{,}625$'),
                st('b)', r'De Morgan: $P(\overline A\cap\overline B)=1-\frac{19}{24}=\frac5{24}\approx0{,}2083$'),
                st('c)', r'$P(A|B)=\dfrac{5/8}{3/4}=\dfrac56\approx0{,}8333$'),
                st('d)', r'$P(A)P(B)=\frac23\cdot\frac34=\frac12\neq\frac58$: <strong>no</strong> són independents.')],
               (r'a) $\frac{19}{24}$' if n == 60 else r'a) $\frac58$') + r'; b) $\frac5{24}$; c) $\frac56$; d) No')
ck((1 - u), F(5, 24)); ck(i / b, F(5, 6))
# 61
S[61] = SOL([st('Successos.', r'$L=$ «ha llegit un llibre» ($0{,}25$), $V=$ «ha vist una pel·lícula» ($0{,}65$), $P(L\cap V)=0{,}1$.'),
             st('a)', r'$P(V\cap\overline L)=0{,}65-0{,}1=0{,}55$'), st('b)', r'$1-P(L\cup V)=1-(0{,}25+0{,}65-0{,}1)=0{,}2$'), st('c)', r'$P(V|L)=\dfrac{0{,}1}{0{,}25}=0{,}4$'),
             ct(F('0.25'), F('0.65'), F('0.1'), 'L', 'V')], r'a) $0{,}55$; b) $0{,}2$; c) $0{,}4$')
# 63
pN = ck(F('0.2') / F('0.75'), F(4, 15)); i = ck(pN / 4, F(1, 15))
S[63] = SOL([st('Successos.', r'$E=$ «activitat esportiva», $N=$ «activitat no esportiva». $P(\overline E\cap\overline N)=0{,}25$, $P(E)=0{,}55$, $P(E|N)=\frac14$.'),
             st('Plantejament.', r'$P(E\cup N)=0{,}75=P(E)+P(N)-P(E\cap N)=0{,}55+P(N)-\tfrac14P(N)\Rightarrow0{,}75\,P(N)=0{,}2\Rightarrow P(N)=\frac4{15}$.'),
             st('a)', r'$P(E\cap N)=\frac14\cdot\frac4{15}=\frac1{15}\approx0{,}0667$'), st('b)', r'$P(E)=0{,}55$ (és una dada).'),
             st('c)', r'$P(E|N)=0{,}25\neq P(E)=0{,}55$: <strong>no</strong> són independents.')], r'a) $\frac1{15}$; b) $0{,}55$; c) No')
# 64
pR = ck(F(1, 4) * F(1, 3) + F(3, 4) * F('0.05'), F(29, 240)); b = ck(F(1, 12) / pR, F(20, 29)); c = ck(1 - F(3, 4) * F('0.05'), F('0.9625'))
S[64] = SOL([bayes([('E', F(1, 4), F(1, 3)), ('N', F(3, 4), F('0.05'))], 'R', 'R̄'),
             st('a)', L(r'$P(R)=\tfrac14\cdot\tfrac13+\tfrac34\cdot0{,}05=\tfrac1{12}+0{,}0375=@a$', a=N(pR))), st('b)', L(r'$P(E|R)=\dfrac{1/12}{29/240}=@b$', b=N(b))),
             st('c)', r'«Arriba a hora o ve de l’estranger» és el contrari de «arriba amb retard i ve del país»: $1-0{,}75\cdot0{,}05=0{,}9625$')],
            L(r'a) $@a$; b) $@b$; c) $0{,}9625$', a=N(pR), b=N(b)))
# 65
pE = ck(F('0.4') * F('0.35') + F('0.4') * F('0.55') + F('0.2') * F('0.4'), F('0.44')); c = ck(F('0.2') * F('0.6') / (1 - pE), F(3, 14))
S[65] = SOL([st('a)', r'$P(A)=P(B)$ i $P(A)+P(B)=1-0{,}2\Rightarrow P(A)=0{,}4$.'),
             bayes([('A', F('0.4'), F('0.35')), ('B', F('0.4'), F('0.55')), ('C', F('0.2'), F('0.4'))], 'E', 'Ē'),
             st('b)', r'$P(E)=0{,}14+0{,}22+0{,}08=0{,}44$'), st('c)', r'$P(C|\overline E)=\dfrac{0{,}2\cdot0{,}6}{0{,}56}=\dfrac3{14}\approx0{,}2143$')], r'a) $0{,}4$; b) $0{,}44$; c) $\frac3{14}$')
# 66
pp = dict(a=F(1, 12), b=F(1, 12), c=F(1, 12), d=F(1, 12), e=F(1, 2), f=F(1, 6)); A, B = set('acd'), set('cef'); E = set('abcdef')
def P(s): return sum((pp[x] for x in s), F(0))
ck(P(E), 1); ck(P(A | B), F(11, 12)); ck(P((E - A) | B), F(5, 6)); ck(P(A & B), F(1, 12)); ck(P(A & B) / P(B), F(1, 9))
S[66] = SOL([st('Successos.', r'$A=\{a,c,d\}$, $B=\{c,e,f\}$, $\overline A=\{b,e,f\}$. Sumem les probabilitats dels resultats elementals.'),
             st('a)', r'$A\cup B=\{a,c,d,e,f\}$: $P=1-P(b)=\frac{11}{12}$'), st('b)', r'$\overline A\cup B=\{b,c,e,f\}$: $P=\frac1{12}+\frac1{12}+\frac12+\frac16=\frac56$'),
             st('c)', r'$A\cap B=\{c\}$: $P=\frac1{12}$'), st('d)', r'$P(B)=\frac1{12}+\frac12+\frac16=\frac34$; $\ P(A|B)=\dfrac{1/12}{3/4}=\dfrac19$')],
            r'a) $\frac{11}{12}$; b) $\frac56$; c) $\frac1{12}$; d) $\frac19$')
# 67
pr = [F('0.55'), F('0.25'), F('0.2')]; dd = [F('0.2'), F('0.03'), F('0.01')]; pD = ck(sum(x * y for x, y in zip(pr, dd)), F('0.1195'))
a = ck(F('0.11') / pD, F(220, 239)); c = ck(F('0.25') + pD - F('0.0075'), F('0.362'))
S[67] = SOL([bayes([('Ll', pr[0], dd[0]), ('Se', pr[1], dd[1]), ('Pr', pr[2], dd[2])], 'D', 'D̄'),
             st('Probabilitat total:', r'$P(D)=0{,}11+0{,}0075+0{,}002=0{,}1195$'), st('a)', L(r'$P(Ll|D)=\dfrac{0{,}11}{0{,}1195}=@a$', a=N(a))),
             st('b)', r'$P(Pr\cap\overline D)=0{,}2\cdot0{,}99=0{,}198$'), st('c)', r'$P(Se\cup D)=0{,}25+0{,}1195-0{,}0075=0{,}362$')],
            L(r'a) $@a$; b) $0{,}198$; c) $0{,}362$', a=N(a)))
# 68
i = ck(F('0.35') + F('0.5') - F('0.7'), F('0.15'))
S[68] = SOL([st('a)', r'$P(V\cup C)=1-0{,}3=0{,}7$'), st('b)', r'$P(V\cap C)=0{,}35+0{,}5-0{,}7=0{,}15$'), st('c)', r'$P(V\cap\overline C)=0{,}35-0{,}15=0{,}2$'),
             st('d)', r'$P(\overline V|\overline C)=\dfrac{0{,}3}{0{,}5}=0{,}6$'), ct(F('0.35'), F('0.5'), i, 'V', 'C')], r'a) $0{,}7$; b) $0{,}15$; c) $0{,}2$; d) $0{,}6$')
# 69
def walk(n):
    d = {3: F(1)}
    for _ in range(n):
        e = {}
        for k, p in d.items():
            if k in (1, 5): e[k] = e.get(k, 0) + p
            else:
                e[k - 1] = e.get(k - 1, 0) + p / 2; e[k + 1] = e.get(k + 1, 0) + p / 2
        d = e
    return d
w3, w4 = walk(3), walk(4); ck(w3.get(3, 0), 0); ck(w3[1] + w3[5], F(1, 2)); ck(w4[1] + w4[5], F(3, 4))
S[69] = SOL([st('a) Arbre.', 'Des de la cadira 3: després del 1r llançament, 2 o 4 ($\\frac12$ cada una). Després del 2n: cadira 1 ($\\frac14$), 3 ($\\frac12$) o 5 ($\\frac14$); les cadires 1 i 5 ja no canvien. Després del 3r: des de 3 es passa a 2 o 4. Després del 4t: des de 2 es passa a 1 o 3, i des de 4 a 3 o 5.'
                   + arbre([('2', F(1, 2), [('1', F(1, 2), True), ('3', F(1, 2), False)]), ('4', F(1, 2), [('3', F(1, 2), False), ('5', F(1, 2), True)])])),
             st('b)', r'Després de dos llançaments no està a 2 ni a 4, i després de tres llançaments només pot estar a 1, 2, 4 o 5: $P(\text{cadira }3)=0$.'),
             st('c)', r'Ja estava en un extrem després del 2n llançament amb probabilitat $\frac14+\frac14=\frac12$ i el 3r no el pot portar a cap extrem nou (des de 3 va a 2 o 4): $P=\frac12$.'),
             st('d)', r'Després del 3r: extrems $\frac12$, cadira 2 $\frac14$ i cadira 4 $\frac14$. Del 2 i del 4 passa a un extrem amb probabilitat $\frac12$: $P=\frac12+\frac14\cdot\frac12+\frac14\cdot\frac12=\frac34$.')],
            r'b) $0$; c) $\frac12$; d) $\frac34$')
# 70
pr = [F('0.35'), F('0.2'), F('0.45')]; dd = [F('0.02'), F('0.05'), F('0.03')]; pR = ck(sum(x * y for x, y in zip(pr, dd)), F('0.0305'))
post = [x * y / pR for x, y in zip(pr, dd)]; ck(max(range(3), key=lambda k: post[k]), 2)
S[70] = SOL([bayes([('D₁', pr[0], dd[0]), ('D₂', pr[1], dd[1]), ('D₃', pr[2], dd[2])], 'R', 'R̄'),
             st('a)', r'$P(R)=0{,}007+0{,}01+0{,}0135=0{,}0305\Rightarrow P(\overline R)=0{,}9695$: el $96{,}95\,\%$.'), st('b)', r'$P(D_2\cap R)=0{,}2\cdot0{,}05=0{,}01$'),
             st('c) Bayes:', L(r'$P(D_1|R)=@a$, $P(D_2|R)=@b$, $P(D_3|R)=@c$. La destinació més probable és la <strong>3</strong>.', a=N(post[0]), b=N(post[1]), c=N(post[2])))],
            r'a) $96{,}95\,\%$; b) $0{,}01$; c) destinació 3')
# 71
pF = ck(F('0.7') / F('0.875'), F('0.8')); pE = F('0.9')
S[71] = SOL([st('Dades.', r'$E=$ «experiència», $F=$ «formació adequada». $P(E\cap F)=0{,}7$, $P(E\cap\overline F)=0{,}2$, $P(E|F)=0{,}875$.'),
             st('a)', r'$P(E)=0{,}7+0{,}2=0{,}9\Rightarrow P(\overline E)=0{,}1$'), st('b)', r'$P(F|E)=\dfrac{0{,}7}{0{,}9}=\dfrac79\approx0{,}7778$'),
             st('c)', r'$P(F)=\dfrac{0{,}7}{0{,}875}=0{,}8$; $\ P(E\cup F)=0{,}9+0{,}8-0{,}7=1\Rightarrow P(\overline F\cap\overline E)=0$'), ct(pE, pF, F('0.7'), 'E', 'F')],
            r'a) $0{,}1$; b) $\frac79$; c) $0$')
# 72
pD = ck(F('0.06') + F('0.02'), F('0.08')); b = ck(F('0.54') / F('0.92'), F(27, 46))
S[72] = SOL([bayes([('A', F('0.6'), F('0.1')), ('B', F('0.4'), F('0.05'))], 'D', 'D̄'),
             st('a)', r'$P(D)=0{,}06+0{,}02=0{,}08$'), st('b)', L(r'$P(A|\overline D)=\dfrac{0{,}54}{0{,}92}=@b$', b=N(b))), st('c)', r'$P(B\cap D)=0{,}02$')],
            L(r'a) $0{,}08$; b) $@b$; c) $0{,}02$', b=N(b)))
# 73
S[73] = SOL([st('Successos.', r'$T=$ «paga amb targeta» ($0{,}68$), $S=$ «supera 500 €» ($0{,}15$), $P(T\cap S)=0{,}05$.'), ct(F('0.68'), F('0.15'), F('0.05'), 'T', 'S'),
             st('a)', r'$P(\overline S\cap\overline T)=1-(0{,}68+0{,}15-0{,}05)=0{,}22$'), st('b)', r'$P(\overline S|\overline T)=\dfrac{0{,}22}{0{,}32}=\dfrac{11}{16}=0{,}6875$'),
             st('c)', r'$P(T|\overline S)=\dfrac{0{,}63}{0{,}85}=\dfrac{63}{85}\approx0{,}7412$')], r'a) $0{,}22$; b) $0{,}6875$; c) $\frac{63}{85}$')
ck(F('0.63') / F('0.85'), F(63, 85))
# 74
a = ck(F(1, 3) * (F(1, 5) + F(1, 4) + F(1, 3)), F(47, 180)); b = ck(F(1, 9) / a, F(20, 47))
S[74] = SOL([bayes([('Blau', F(1, 3), F(1, 5)), ('Roig', F(1, 3), F(1, 4)), ('Verd', F(1, 3), F(1, 3))], 'O', 'Ō'),
             st('a)', L(r'$P(O)=\tfrac13\left(\tfrac15+\tfrac14+\tfrac13\right)=@a$', a=N(a))), st('b)', L(r'$P(V|O)=\dfrac{1/9}{47/180}=@b$', b=N(b))),
             st('c)', r'Amb un clauer de $n$ claus: $P(\text{falla la 1a i obri la 2a})=\frac{n-1}{n}\cdot\frac1{n-1}=\frac1n$. Per tant, el resultat és el mateix que en a): $\frac{47}{180}$.')],
            L(r'a) $@a$; b) $@b$; c) $@a$', a=N(a), b=N(b)))
# 75
a = ck(F(1, 2) * F(1, 36) + F(1, 2) * F(2, 6) * F(4, 6), F(1, 8)); b = ck(F(1, 2) * F(2, 36) + F(1, 2) * 2 * F(4, 6) * F(2, 6), F(1, 4)); c = ck(F(1, 2) * F(8, 36) / a, F(8, 9))
S[75] = SOL([st('Successos.', r'$N=$ «dau normal», $T=$ «dau trucat» ($\frac12$ cada un). Amb el trucat: $P(5)=\frac46$, $P(6)=\frac26$.'),
             st('a)', r'$P(6,5)=\tfrac12\cdot\tfrac16\cdot\tfrac16+\tfrac12\cdot\tfrac26\cdot\tfrac46=\tfrac1{72}+\tfrac8{72}=\tfrac18$'),
             st('b)', r'Suma 11: $(5,6)$ o $(6,5)$. $P=\tfrac12\cdot\tfrac2{36}+\tfrac12\cdot2\cdot\tfrac46\cdot\tfrac26=\tfrac1{36}+\tfrac8{36}=\tfrac14$'),
             st('c) Bayes:', r'$P(T|6,5)=\dfrac{8/72}{1/8}=\dfrac89$')], r'a) $\frac18$; b) $\frac14$; c) $\frac89$')
# 76
pp = dict(a=F(1, 8), c=F(1, 8), d=F(1, 4), e=F(1, 3)); pp['b'] = 1 - sum(pp.values()); ck(pp['b'], F(1, 6))
A, B, E = set('abc'), set('bde'), set('abcde')
def P(s): return sum((pp[x] for x in s), F(0))
ck(P(A & B), F(1, 6)); ck(P(A | (E - B)), F(5, 12)); ck(P((E - A) & (E - B)), 0); ck(P(A - B) / P(E - B), 1); ck(P(A & B) / P(A), F(2, 5))
S[76] = SOL([st('Dades.', r'$P(b)=1-\frac18-\frac18-\frac14-\frac13=\frac16$. $\ \overline A=\{d,e\}$, $\overline B=\{a,c\}$.'),
             st('a)', r'$A\cap B=\{b\}$: $\frac16$'), st('b)', r'$A\cup\overline B=\{a,b,c\}=A$: $\frac18+\frac16+\frac18=\frac5{12}$'),
             st('c)', r'$\overline A\cap\overline B=\varnothing$: $0$'), st('d)', r'$P(A|\overline B)=\dfrac{P(\{a,c\})}{P(\{a,c\})}=1$'), st('e)', r'$P(B|A)=\dfrac{1/6}{5/12}=\dfrac25$')],
            r'a) $\frac16$; b) $\frac5{12}$; c) $0$; d) $1$; e) $\frac25$')
# 77
sp = F(2, 3) * F(3, 8); ck(sp, F(1, 4)); c = ck((F(1, 3) - F('0.05')) / F('0.7'), F(17, 42))
S[77] = SOL([st('Successos.', r'$S=$ «té Smart TV» ($\frac23$), $T=$ «televisió de pagament». $P(T|S)=\frac38$, $P(T)=0{,}3$.'),
             st('Intersecció:', r'$P(S\cap T)=\frac23\cdot\frac38=\frac14=0{,}25$'), ct(F(2, 3), F('0.3'), sp, 'S', 'T'),
             st('a)', r'$P(\overline S\cap T)=0{,}3-0{,}25=0{,}05$'), st('b)', r'$P(S|T)=\dfrac{0{,}25}{0{,}3}=\dfrac56\approx0{,}8333$'),
             st('c)', r'$P(\overline S|\overline T)=\dfrac{\frac13-0{,}05}{0{,}7}=\dfrac{17}{42}\approx0{,}4048$')], r'a) $0{,}05$; b) $\frac56$; c) $\frac{17}{42}$')
# 78
pS = ck(F('0.7') * F('0.05') + F('0.3') * F('0.02'), F('0.041')); b = ck(F('0.006') / pS, F(6, 41))
S[78] = SOL([bayes([('H', F('0.7'), F('0.05')), ('D', F('0.3'), F('0.02'))], 'S', 'S̄'),
             st('a)', r'$P(S)=0{,}035+0{,}006=0{,}041$'), st('b)', L(r'$P(D|S)=\dfrac{0{,}006}{0{,}041}=@b$', b=N(b))), st('c)', r'$P(H\cap S)=0{,}035$: el $3{,}5\,\%$.')],
            L(r'a) $0{,}041$; b) $@b$; c) $3{,}5\,\%$', b=N(b)))
# 79
x = ck((F('0.25') - F('0.2') * F('0.15') - F('0.4') * F('0.4')) / F('0.4'), F('0.15'))
b = ck(F('0.2') * F('0.85') / F('0.75'), F(17, 75))
S[79] = SOL([st('Successos.', r'$V$ ($0{,}2$), $U$ ($0{,}4$), $S$ ($0{,}4$); $H=$ «híbrid» ($0{,}25$): $P(H|V)=0{,}15$, $P(H|U)=0{,}4$, $P(H|S)=x$.'),
             st('Càlcul de $x$:', r'$0{,}25=0{,}2\cdot0{,}15+0{,}4\cdot0{,}4+0{,}4x=0{,}19+0{,}4x\Rightarrow x=0{,}15$.'),
             bayes([('V', F('0.2'), F('0.15')), ('U', F('0.4'), F('0.4')), ('S', F('0.4'), x)], 'H', 'H̄'),
             st('a)', r'$P(U|H)=\dfrac{0{,}16}{0{,}25}=0{,}64$'), st('b)', L(r'$P(V|\overline H)=\dfrac{0{,}2\cdot0{,}85}{0{,}75}=@b$', b=N(b))),
             st('c)', r'$P(H|S)=x=0{,}15$'), st('d)', r'$P(\overline V\cap\overline H)=P(\overline H)-P(V\cap\overline H)=0{,}75-0{,}17=0{,}58$')],
            L(r'a) $0{,}64$; b) $@b$; c) $0{,}15$; d) $0{,}58$', b=N(b)))
# 80
pr = [F('0.1'), F('0.2'), F('0.7')]; dd = [F('0.01'), F('0.03'), F('0.06')]; pT = ck(sum(x * y for x, y in zip(pr, dd)), F('0.049'))
b = ck(F('0.006') / pT, F(6, 49)); c = ck((pr[1] * F('0.97') + pr[2] * F('0.94')) / (1 - pT), F(284, 317))
S[80] = SOL([st('Successos.', r'$V$ (vehicle) $=0{,}7$; transport públic $=2\cdot$ caminant i entre els dos sumen $0{,}3$: $P(C)=0{,}1$, $P(Tp)=0{,}2$.'),
             bayes([('C', pr[0], dd[0]), ('Tp', pr[1], dd[1]), ('V', pr[2], dd[2])], 'R', 'R̄'),
             st('a)', r'$P(R)=0{,}001+0{,}006+0{,}042=0{,}049\Rightarrow P(\overline R)=0{,}951$'), st('b)', L(r'$P(Tp|R)=\dfrac{0{,}006}{0{,}049}=@b$', b=N(b))),
             st('c)', L(r'$P(\overline C|\overline R)=\dfrac{0{,}2\cdot0{,}97+0{,}7\cdot0{,}94}{0{,}951}=\dfrac{0{,}852}{0{,}951}=@c$', c=N(c)))],
            L(r'a) $0{,}951$; b) $@b$; c) $@c$', b=N(b), c=N(c)))
# 81
pB = ck(F(1, 2) * F(2, 5) + F(1, 2) * F(1, 5), F('0.3'))
S[81] = SOL([st('Dades.', r'$P(A)=0{,}5$, $P(B|A)=\frac25$, $P(\overline B|\overline A)=\frac45\Rightarrow P(B|\overline A)=\frac15$.'),
             bayes([('A', F(1, 2), F(2, 5)), ('Ā', F(1, 2), F(1, 5))], 'B', 'B̄'),
             st('a)', r'$P(B)=0{,}2+0{,}1=0{,}3$'), st('b)', r'$P(A|B)=\dfrac{0{,}2}{0{,}3}=\dfrac23$'), st('c)', r'$P(\overline A|\overline B)=\dfrac{0{,}4}{0{,}7}=\dfrac47\approx0{,}5714$'),
             st('d)', r'$P(A\cap\overline B)=0{,}5\cdot0{,}6=0{,}3$')], r'a) $0{,}3$; b) $\frac23$; c) $\frac47$; d) $0{,}3$')
# 82
pC = ck(F('0.05') * F('0.96') + F('0.95') * F('0.02'), F('0.067')); b = ck(F('0.05') * F('0.04') / (1 - pC), F(2, 933))
S[82] = SOL([st('Successos.', r'$P=$ «plagi» ($0{,}05$), $C=$ «classificat com a plagi»: $P(\overline C|P)=0{,}04\Rightarrow P(C|P)=0{,}96$; $P(C|\overline P)=0{,}02$.'),
             bayes([('P', F('0.05'), F('0.96')), ('P̄', F('0.95'), F('0.02'))], 'C', 'C̄'),
             st('a)', r'$P(C)=0{,}048+0{,}019=0{,}067$'), st('b)', L(r'$P(P|\overline C)=\dfrac{0{,}05\cdot0{,}04}{0{,}933}=@b$', b=N(b, 5))), st('c)', r'$P(P\cap C)=0{,}048$: el $4{,}8\,\%$.')],
            L(r'a) $0{,}067$; b) $@b$; c) $4{,}8\,\%$', b=N(b, 5)))
# 83
i = ck(1 - F('0.7'), F('0.3')); pB = ck(F('0.8') - F('0.4') + i, F('0.7'))
S[83] = SOL([st('Dades.', r'De Morgan: $P(A\cap B)=1-P(\overline A\cup\overline B)=0{,}3$; $\ P(B)=0{,}8-0{,}4+0{,}3=0{,}7$.'), ct(F('0.4'), pB, i),
             st('a)', r'$P(A)P(B)=0{,}28\neq0{,}3$: <strong>no</strong> són independents.'), st('b)', r'$0{,}8-0{,}3=0{,}5$'), st('c)', r'$P(\overline B)=0{,}3$'),
             st('d)', r'$P(\overline A|B)=\dfrac{0{,}4}{0{,}7}=\dfrac47\approx0{,}5714$')], r'a) No; b) $0{,}5$; c) $0{,}3$; d) $\frac47$')
# 84
S[84] = SOL([st('Successos.', r'$M=$ «més d’una persona» ($0{,}8$), $P=$ «subscrita a Panoramix» ($0{,}3$), $P(M\cap P)=0{,}2$.'), ct(F('0.8'), F('0.3'), F('0.2'), 'M', 'P'),
             st('a)', r'$P(\overline P)=0{,}7$'), st('b)', r'$P(\overline M\cap P)=0{,}3-0{,}2=0{,}1$'), st('c)', r'$P(P|\overline M)=\dfrac{0{,}1}{0{,}2}=0{,}5$'),
             st('d)', r'$P(M|P)=\dfrac{0{,}2}{0{,}3}=\dfrac23\approx0{,}6667$')], r'a) $0{,}7$; b) $0{,}1$; c) $0{,}5$; d) $\frac23$')
# 85
S[85] = SOL([st('Dades.', r'$P(B)=1-0{,}75=0{,}25$; $\ P(A\cap B)=0{,}4\cdot0{,}25=0{,}1$.'), ct(F('0.4'), F('0.25'), F('0.1')),
             st('a)', r'$P(B|A)=0{,}25=P(B)$: <strong>sí</strong> que són independents.'), st('b)', r'$P(A\cup B)=0{,}4+0{,}25-0{,}1=0{,}55$'),
             st('c)', r'$P(A|B^c)=\dfrac{0{,}3}{0{,}75}=0{,}4$ (igual que $P(A)$, per la independència)'), st('d)', r'$P(A^c\cup B^c)=1-0{,}1=0{,}9$; $\ P(A^c\cap B^c)=1-0{,}55=0{,}45$')],
            r'a) Sí; b) $0{,}55$; c) $0{,}4$; d) $0{,}9$ i $0{,}45$')
# 86
x = ck((F('0.34') - F('0.09') - F('0.4') * F('0.7')) / (F('0.25') - F('0.4')), F('0.2')); y = F('0.7') - x
b = ck(y * F('0.4') / F('0.34'), F(10, 17)); c = ck(y * F('0.4') / (F('0.09') + y * F('0.4')), F(20, 29))
S[86] = SOL([st('a)', r'Siguen $x=P(4{,}7^{\prime\prime})$ i $y=P(5^{\prime\prime})$, amb $x+y=0{,}7$. Probabilitat total de dur protector: $0{,}3\cdot0{,}3+0{,}25x+0{,}4y=0{,}34$. Substituint $y=0{,}7-x$: $0{,}09+0{,}25x+0{,}28-0{,}4x=0{,}34\Rightarrow x=0{,}2$, $y=0{,}5$: el $20\,\%$ i el $50\,\%$.'),
             bayes([('4"', F('0.3'), F('0.3')), ('4,7"', x, F('0.25')), ('5"', y, F('0.4'))], 'Pr', 'P̄r'),
             st('b)', r'$P(5^{\prime\prime}|Pr)=\dfrac{0{,}5\cdot0{,}4}{0{,}34}=\dfrac{10}{17}\approx0{,}5882$'),
             st('c)', r'Ens restringim als que tenen protector i pantalla de 4 o 5 polzades: $\dfrac{0{,}2}{0{,}09+0{,}2}=\dfrac{20}{29}\approx0{,}6897$')],
            r'a) $20\,\%$ i $50\,\%$; b) $\frac{10}{17}$; c) $\frac{20}{29}$')
# 87
a = ck(F(2 * 1 + 3 * 2, 90), F(4, 45)); b = ck(2 * F(2, 10) * F(8, 9), F(16, 45)); c = ck(b / (a + b), F(4, 5))
S[87] = SOL([st('Dades.', 'Urna: 2 blanques, 3 grogues, 5 negres (10 boles), dues extraccions sense reemplaçament.'),
             st('a)', r'$P(BB)+P(GG)=\frac2{10}\cdot\frac19+\frac3{10}\cdot\frac29=\frac{2+6}{90}=\frac4{45}$'),
             st('b)', r'Una blanca i l’altra no (en qualsevol ordre): $2\cdot\frac2{10}\cdot\frac89=\frac{32}{90}=\frac{16}{45}$'),
             st('c)', r'$P(3r\,|\,\text{premi})=\dfrac{16/45}{4/45+16/45}=\dfrac45$')], r'a) $\frac4{45}$; b) $\frac{16}{45}$; c) $\frac45$')
# 88
pP = ck(F('0.05') * F('0.99') + F('0.95') * F('0.05'), F('0.097')); a = ck(F('0.0495') / pP, F(99, 194)); b = ck(F('0.9025') / (1 - pP), F(1805, 1806))
c = ck(F('0.0495') + F('0.9025'), F('0.952')); d = ck(F('0.0099') / (F('0.0099') + F('0.0495')), F(1, 6))
S[88] = SOL([bayes([('M', F('0.05'), F('0.99')), ('S', F('0.95'), F('0.05'))], '+', '−'),
             st('a)', L(r'$P(+)=0{,}0495+0{,}0475=0{,}097$; $\ P(M|+)=\dfrac{0{,}0495}{0{,}097}=@a$', a=N(a))),
             st('b)', L(r'$P(S|-)=\dfrac{0{,}95\cdot0{,}95}{1-0{,}097}=\dfrac{0{,}9025}{0{,}903}=@b$', b=N(b))),
             st('c)', r'Resultat correcte: $P(M\cap+)+P(S\cap-)=0{,}0495+0{,}9025=0{,}952$'),
             st('d)', r'Amb $P(M)=0{,}01$: $P(M|+)=\dfrac{0{,}01\cdot0{,}99}{0{,}01\cdot0{,}99+0{,}99\cdot0{,}05}=\dfrac{0{,}0099}{0{,}0594}=\dfrac16\approx0{,}1667$')],
            L(r'a) $@a$; b) $@b$; c) $0{,}952$; d) $\frac16$', a=N(a), b=N(b)))
# 89
pr = [F('0.3'), F('0.55'), F('0.15')]; nb = [F(3, 4), F(9, 10), F(2, 5)]; pB = ck(sum(x * y for x, y in zip(pr, nb)), F('0.78'))
a = ck(F('0.15') + pB - F('0.15') * F(2, 5), F('0.87')); b = ck(F('0.55') * F('0.1') + F('0.15') * F('0.6'), F('0.145')); c = ck((F('0.3') * F('0.25') + F('0.55') * F('0.1')) / (1 - pB), F(13, 22))
S[89] = SOL([bayes([('<30', pr[0], nb[0]), ('30-60', pr[1], nb[1]), ('>60', pr[2], nb[2])], 'B', 'D'),
             st('Probabilitat total:', r'$P(B)=0{,}3\cdot\frac34+0{,}55\cdot\frac9{10}+0{,}15\cdot\frac25=0{,}225+0{,}495+0{,}06=0{,}78$'),
             st('a)', r'$P(A\cup B)=0{,}15+0{,}78-0{,}06=0{,}87$'), st('b)', r'$P(C\cap D)=0{,}55\cdot0{,}1+0{,}15\cdot0{,}6=0{,}145$'),
             st('c)', L(r'$P(\le60|D)=\dfrac{0{,}3\cdot0{,}25+0{,}55\cdot0{,}1}{0{,}22}=\dfrac{0{,}13}{0{,}22}=@c$', c=N(c)))],
            L(r'a) $0{,}87$; b) $0{,}145$; c) $@c$', c=N(c)))
# 90
w2, w1 = F(1, 4) * F(1, 2), F(1, 2) * F(1, 3); pG = ck(w2 + w1, F(7, 24))
six_win = F(1, 4) * F(1, 6) + F(1, 2) * F(1, 6); pAB = F(1, 6) - six_win
ck(pAB, F(1, 24)); ck((1 - pG) * F(1, 6) == pAB, False)
S[90] = SOL([st('Probabilitats de les monedes.', r'$P(\text{dues cares})=\frac14$, $P(\text{una cara})=\frac12$. Dau: $P(\text{parell})=\frac12$, $P(\ge5)=\frac13$.'),
             st('a)', r'$P(G)=\frac14\cdot\frac12+\frac12\cdot\frac13=\frac18+\frac16=\frac7{24}$'), st('b)', r'$\dfrac{1/8}{7/24}=\dfrac37$'),
             st('c)', r'Amb un 5 només es guanya amb una cara: $P(5\cap G)=\frac12\cdot\frac16=\frac1{12}$; $\ \dfrac{1/12}{7/24}=\dfrac27$'),
             st('d)', r'$P(B)=\frac16$; amb un 6 es guanya amb dues cares o amb una: $P(G\cap B)=\frac14\cdot\frac16+\frac12\cdot\frac16=\frac18$, així que $P(A\cap B)=\frac16-\frac18=\frac1{24}$. Però $P(A)P(B)=\frac{17}{24}\cdot\frac16=\frac{17}{144}\neq\frac1{24}$: <strong>no</strong> són independents.')],
            r'a) $\frac7{24}$; b) $\frac37$; c) $\frac27$; d) No')
# 91
pA = ck(F('0.8') - F('0.4') + F('0.3'), F('0.7'))
S[91] = SOL([st('a)', r'$P(A\cup B)=1-P(A^C\cap B^C)=0{,}8$'), st('b)', r'$0{,}8-0{,}3=0{,}5$'),
             st('c)', r'$P(A)=0{,}8-0{,}4+0{,}3=0{,}7$; $\ P(B|A)=\dfrac{0{,}3}{0{,}7}=\dfrac37\approx0{,}4286$'), st('d)', r'$P(A)P(B)=0{,}28\neq0{,}3$: <strong>no</strong> són independents.'),
             ct(pA, F('0.4'), F('0.3'))], r'a) $0{,}8$; b) $0{,}5$; c) $\frac37$; d) No')
# 92
a = ck(F('0.9') * F('0.2'), F('0.18')); b = ck(F('0.9') + F('0.1') * F('0.5'), F('0.95')); c = ck(F('0.9') * F('0.5') / (F('0.9') * F('0.5') + F('0.1')), F(9, 11))
S[92] = SOL([st('Successos.', r'Auditor correcte $C$ ($0{,}9$) o incorrecte $I$ ($0{,}1$, sempre posa «Acceptable»). Qualificació real: E $0{,}3$, A $0{,}5$, D $0{,}2$.'),
             st('a)', r'Només els correctes posen «Deficient», i ho fan quan ho mereix: $0{,}9\cdot0{,}2=0{,}18$'),
             st('b)', r'Rep la que mereix si l’auditor és correcte, o si és incorrecte però l’empresa mereix «Acceptable»: $0{,}9+0{,}1\cdot0{,}5=0{,}95$'),
             st('c) Bayes:', r'$P(\text{posa A})=0{,}9\cdot0{,}5+0{,}1\cdot1=0{,}55$; $\ P(C|\text{posa A})=\dfrac{0{,}45}{0{,}55}=\dfrac9{11}\approx0{,}8182$')],
            r'a) $0{,}18$; b) $0{,}95$; c) $\frac9{11}$')
# 93
a = ck(F('0.1') * F('0.05'), F('0.005')); pS = F('0.095') + F('0.27'); b = ck(F('0.27') / pS, F(54, 73)); c = ck(a / (1 - pS), F(1, 127))
S[93] = SOL([bayes([('At', F('0.1'), F('0.95')), ('Āt', F('0.9'), F('0.3'))], 'S', 'S̄'),
             st('a)', r'$P(At\cap\overline S)=0{,}1\cdot0{,}05=0{,}005$'), st('b)', L(r'$P(S)=0{,}095+0{,}27=0{,}365$; $\ P(\overline{At}|S)=\dfrac{0{,}27}{0{,}365}=@b$', b=N(b))),
             st('c)', L(r'$P(At|\overline S)=\dfrac{0{,}005}{0{,}635}=@c$', c=N(c, 5)))], L(r'a) $0{,}005$; b) $@b$; c) $@c$', b=N(b), c=N(c, 5)))
# 94
a = ck((F('0.3') - F('0.14') + F('0.1') - F('0.02')) / F('0.4'), F('0.6')); b = ck(1 - F('0.02'), F('0.98'))
pJ = F('0.54') + F('0.14') + F('0.02'); pK = 1 - F('0.3'); ck(pJ * pK == F('0.56'), False)
S[94] = SOL([st('Taula (casat / no casat):', taula([r'\text{Casat}', r'\text{No casat}'], [r'1', r'2', r'\ge3'], [[F('0.54'), F('0.14'), F('0.02'), F('0.7')], [F('0.06'), F('0.16'), F('0.08'), F('0.3')], [F('0.6'), F('0.3'), F('0.1'), 1]])),
             st('a)', r'$P(\overline{Cas}|\ge2)=\dfrac{0{,}16+0{,}08}{0{,}4}=0{,}6$'),
             st('b)', r'$G\cup H$ és el contrari de «casat i tres o més viatges»: $1-0{,}02=0{,}98$'),
             st('c)', r'$P(J)=0{,}7$, $P(K)=1-0{,}3=0{,}7$, $P(J\cap K)=0{,}54+0{,}02=0{,}56\neq0{,}7\cdot0{,}7=0{,}49$: <strong>no</strong> són independents.')],
            r'a) $0{,}6$; b) $0{,}98$; c) No')
# 95
pD = ck(F('0.3') / F('0.4'), F('0.75'))
S[95] = SOL([st('Dades.', r'$P(A\cap D)=0{,}3$, $P(A)=0{,}4$, $P(A|D)=0{,}4$.'), st('a)', r'$P(D)=\dfrac{0{,}3}{0{,}4}=0{,}75$'), st('b)', r'$P(D\cap\overline A)=0{,}75-0{,}3=0{,}45$'),
             st('c)', r'$P(A|\overline D)=\dfrac{0{,}4-0{,}3}{0{,}25}=0{,}4$'), ct(F('0.4'), pD, F('0.3'), 'A', 'D')], r'a) $0{,}75$; b) $0{,}45$; c) $0{,}4$')
# 96
cc = F(2, 3) * F(1, 4) + F(1, 3) * F(9, 16); ck(cc, F(17, 48)); a = ck(F(1, 6) / cc, F(8, 17)); b = ck(F(1, 3) + F(2, 3) * F(3, 4), F(5, 6))
pTT = F(2, 3) * F(1, 4) + F(1, 3) * F(1, 16); ck(pTT, F(3, 16)); ck(F(1, 6) * F(1, 4) == F(1, 6) * pTT, False)
S[96] = SOL([st('Dades.', r'$P(>2)=\frac23$ (moneda bona, $P(C)=\frac12$); $P(\le2)=\frac13$ (moneda defectuosa: $P(C)=3P({+})\Rightarrow P(C)=\frac34$).'),
             arbre([('>2', F(2, 3), [('CC', F(1, 4), True), ('altres', F(3, 4), False)]), ('≤2', F(1, 3), [('CC', F(9, 16), True), ('altres', F(7, 16), False)])]),
             st('a)', r'$P(CC)=\frac23\cdot\frac14+\frac13\cdot\frac9{16}=\frac16+\frac3{16}=\frac{17}{48}$; $\ P(>2|CC)=\dfrac{1/6}{17/48}=\dfrac8{17}$'),
             st('b)', r'$P(\le2\ \cup\ \text{almenys una cara})=P(\le2)+P(>2)\cdot P(\text{almenys una cara}|>2)=\frac13+\frac23\cdot\frac34=\frac56$'),
             st('c)', r'$P(6)=\frac16$; $\ P(++)=\frac23\cdot\frac14+\frac13\cdot\frac1{16}=\frac3{16}$; $\ P(6\cap++)=\frac16\cdot\frac14=\frac1{24}\neq\frac16\cdot\frac3{16}=\frac1{32}$: <strong>no</strong> són independents.')],
            r'a) $\frac8{17}$; b) $\frac56$; c) No')
# 97
ck(F(318, 400), F('0.795')); ck(F(290, 372), F(145, 186)); ck(F(78, 400) == F(90, 400) * F(328, 400), False)
S[97] = SOL([st('Taula.', taula([r'\text{ESO}', r'\text{Batx.}'], [r'\text{Futbol}', r'\text{Bàsquet}', r'\text{Música}'], [[230, 60, 20, 310], [70, 12, 8, 90], [300, 72, 28, 400]], str)),
             st('a)', r'$P(ESO\cup Mús)=\dfrac{310+8}{400}=0{,}795$'), st('b)', r'$P(ESO|Esp)=\dfrac{230+60}{300+72}=\dfrac{290}{372}=\dfrac{145}{186}\approx0{,}7796$'),
             st('c)', r'$P(Bat)=\frac{90}{400}$, $P(\overline{Bàs})=\frac{328}{400}$; $P(Bat\cap\overline{Bàs})=\frac{78}{400}=0{,}195\neq\frac{90}{400}\cdot\frac{328}{400}=0{,}1845$: <strong>no</strong> són independents.')],
            r'a) $0{,}795$; b) $\frac{145}{186}$; c) No')
# 98
a = ck(F(75 + 50 + 60, 600), F(37, 120)); b = ck(F(200, 415), F(40, 83))
S[98] = SOL([st('Recompte.', 'Tenen problemes respiratoris $0{,}3\\cdot250=75$ (A), $0{,}2\\cdot250=50$ (B) i $0{,}6\\cdot100=60$ (no vacunats): 185 de 600.'),
             st('a)', r'$\frac{185}{600}=\frac{37}{120}\approx0{,}3083$'), st('b)', r'No tenen problemes $600-185=415$, i dels de B, $200$: $\frac{200}{415}=\frac{40}{83}\approx0{,}4819$'),
             st('c)', r'$\frac{60}{600}=0{,}1$')], r'a) $\frac{37}{120}$; b) $\frac{40}{83}$; c) $0{,}1$')
# 99
pG = ck(F('0.35') * F('0.2') + F('0.25') * F('0.3') + F('0.4') * F('0.6'), F('0.385')); b = ck(F('0.315') / pG, F(9, 11)); c = ck(F('0.07') + F('0.25'), F('0.32'))
S[99] = SOL([bayes([('X', F('0.35'), F('0.2')), ('M', F('0.25'), F('0.3')), ('G', F('0.4'), F('0.6'))], 'U', 'Ū'),
             st('a)', r'$P(U)=0{,}07+0{,}075+0{,}24=0{,}385$'), st('b)', r'$P(M\cup G|U)=\dfrac{0{,}075+0{,}24}{0{,}385}=\dfrac9{11}\approx0{,}8182$'),
             st('c)', r'El primer succés és $X\cup M$ i el segon $U\cup M\cup G$. La intersecció és $(X\cap U)\cup M$: $0{,}07+0{,}25=0{,}32$')],
            r'a) $0{,}385$; b) $\frac9{11}$; c) $0{,}32$')
# 100
v = F(1, 145); a = ck(v * F('0.04'), F(1, 3625)); pP = v * F('0.96') + (1 - v) * F('0.06'); b = ck(v * F('0.96') / pP, F('0.1')); c = ck(v * F('0.96') + (1 - v) * F('0.94'), F(3408, 3625))
S[100] = SOL([bayes([('M', v, F('0.96')), ('M̄', 1 - v, F('0.06'))], '+', '−'),
              st('a)', L(r'$P(M\cap-)=\frac1{145}\cdot0{,}04=@a$', a=N(a, 6))), st('b)', r'$P(+)=\frac{0{,}96+144\cdot0{,}06}{145}=\frac{9{,}6}{145}$; $\ P(M|+)=\dfrac{0{,}96}{9{,}6}=0{,}1$'),
              st('c)', L(r'$P(M\cap+)+P(\overline M\cap-)=\frac{0{,}96+144\cdot0{,}94}{145}=@c$', c=N(c)))],
             L(r'a) $@a$; b) $0{,}1$; c) $@c$', a=N(a, 6), c=N(c)))
# 101
ck(800 + 1400 - 300, 2000 - 100)
S[101] = SOL([st('Taula.', taula(['N', r'\overline N'], ['P', r'\overline P'], [[300, 500, 800], [1100, 100, 1200], [1400, 600, 2000]], str)),
              st('a)', r'$\frac{1900}{2000}=0{,}95$'), st('b)', r'$\frac{500}{2000}=0{,}25$'), st('c)', r'$\frac{500+1100}{2000}=0{,}8$'), st('d)', r'$P(\overline N|\overline P)=\frac{100}{600}=\frac16\approx0{,}1667$')],
             r'a) $0{,}95$; b) $0{,}25$; c) $0{,}8$; d) $\frac16$')
# 102
pp_, pn = F('0.8') * F('0.7'), F('0.2') * F('0.3'); mix = F('0.8') * F('0.3') + F('0.2') * F('0.7')
ad = ck(pp_ + mix * F('0.6'), F('0.788')); b = ck((pp_ + F('0.8') * F('0.3') * F('0.6')) / ad, F(176, 197)); c = ck(pp_ / (pp_ + pn), F(28, 31))
S[102] = SOL([st('Probabilitats.', 'Passa el 1r control amb $0{,}8$, el 2n amb $0{,}7$ i el 3r (si cal) amb $0{,}6$; els controls són independents.'),
              st('a)', r'Adequat: $PP$, o $PN$ i 3r positiu, o $NP$ i 3r positiu: $0{,}8\cdot0{,}7+(0{,}8\cdot0{,}3+0{,}2\cdot0{,}7)\cdot0{,}6=0{,}56+0{,}228=0{,}788$'),
              st('b)', r'$P(1r\cap Ad)=0{,}56+0{,}8\cdot0{,}3\cdot0{,}6=0{,}704$; $\ \dfrac{0{,}704}{0{,}788}=\dfrac{176}{197}\approx0{,}8934$'),
              st('c)', r'Només dos controls si els dos coincideixen: $PP$ ($0{,}56$) o $NN$ ($0{,}06$). $\ \dfrac{0{,}56}{0{,}62}=\dfrac{28}{31}\approx0{,}9032$')],
             r'a) $0{,}788$; b) $\frac{176}{197}$; c) $\frac{28}{31}$')
# 103
x = ck((F('0.79') - F('0.5') * F('0.8') - F('0.15') * F('0.85')) / F('0.35'), F('0.75')); b = ck(F('0.35') * F('0.25') / F('0.21'), F(5, 12)); c = ck(F('0.35') + F('0.5') * F('0.8'), F('0.75'))
S[103] = SOL([st('Dades.', r'Becaris $0{,}5$ (estudis superiors $0{,}8$), aprenents $0{,}35$ (proporció $x$), mestres $0{,}15$ (estudis superiors $0{,}85$). $P(S)=0{,}79$.'),
              st('Càlcul de $x$:', r'$0{,}79=0{,}4+0{,}35x+0{,}1275\Rightarrow x=0{,}75$'),
              bayes([('Bec', F('0.5'), F('0.8')), ('Apr', F('0.35'), x), ('Mes', F('0.15'), F('0.85'))], 'S', 'S̄'),
              st('a)', r'$P(S\cap Apr)=0{,}35\cdot0{,}75=0{,}2625$'), st('b)', r'$P(Apr|\overline S)=\dfrac{0{,}35\cdot0{,}25}{0{,}21}=\dfrac5{12}\approx0{,}4167$'),
              st('c)', r'$(Apr\cup Bec)\cap(S\cup Apr)=Apr\cup(Bec\cap S)$: $0{,}35+0{,}4=0{,}75$')],
             r'a) $0{,}2625$; b) $\frac5{12}$; c) $0{,}75$')
# 104
a = ck(F('0.3') * F('0.95'), F('0.285')); b = ck(F('0.63') / (F('0.63') + F('0.015')), F(42, 43)); c = ck(F('0.07') + F('0.015'), F('0.085'))
S[104] = SOL([bayes([('BG', F('0.7'), F('0.9')), ('MG', F('0.3'), F('0.05'))], 'diu BG', 'diu MG'),
              st('a)', r'$P(MG\cap\text{diu }MG)=0{,}3\cdot0{,}95=0{,}285$'), st('b)', r'$P(BG|\text{diu }BG)=\dfrac{0{,}63}{0{,}63+0{,}015}=\dfrac{42}{43}\approx0{,}9767$'),
              st('c)', r'Incorrecte: $0{,}7\cdot0{,}1+0{,}3\cdot0{,}05=0{,}085$')], r'a) $0{,}285$; b) $\frac{42}{43}$; c) $0{,}085$')
