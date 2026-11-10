# Solucions de la pàgina PAU de probabilitat de 2n Batx MII (unitat 10): els 13 exercicis del dossier de l'IES Vermellar
# «Exercicis d'estadística i probabilitat de la selectivitat» (pp. 61-64), en el mateix ordre (S[1] ... S[13]).
# Probabilitats amb fraccions exactes o amb la binomial (fórmula); ck() les comprova.
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pr'))
from comu import *  # noqa: F401,F403
import comu
import sympy as sp
S = {}
def pmf(n, p, k): p = F(p); return math.comb(n, k) * p ** k * (1 - p) ** (n - k)
def cdf(n, p, a, b): return sum(pmf(n, p, k) for k in range(a, b + 1))
def d4(x): return ('%.4f' % float(x)).replace('.', '{,}')
def bin_(n, p, k): return r'\binom{%d}{%d}\,%s^{%d}\,%s^{%d}' % (n, k, dec(F(p)), k, dec(1 - F(p)), n - k)

# 1
x, y = sp.symbols('x y')
a0, a1, a2 = (1 - x) * (1 - y), x * (1 - y) + (1 - x) * y, x * y
X, Y = 1 - (1 - x) ** 2, 1 - (1 - y) ** 2
b0, b2 = (1 - x) ** 2 * (1 - y) ** 2, X * Y
b1 = sp.expand(1 - b0 - b2)
assert sp.simplify(a0 + a1 + a2 - 1) == 0 and sp.simplify(b1 - (X * (1 - Y) + (1 - X) * Y)) == 0
assert sp.simplify(X - (2 * x - x ** 2)) == 0; comu.CHK.append(1)
S[1] = SOL([st('a) Les dues monedes són independents:', r'$$P(\text{cap cara})=(1-x)(1-y)$$ $$P(\text{una cara})=x(1-y)+(1-x)\,y$$ $$P(\text{dues cares})=xy$$ (les tres sumen 1).'),
            st('b) Probabilitat final de cara de cada moneda.', r'La moneda M1 acaba en cara si ix cara la primera vegada o si ix creu i, en tornar-la a llançar, ix cara: $$P(C_1)=x+(1-x)\,x=2x-x^2=1-(1-x)^2$$ i, igualment, $P(C_2)=1-(1-y)^2$. Les monedes continuen sent independents.'),
            st('Resultat final:', r'$$P(\text{cap cara})=(1-x)^2(1-y)^2$$ $$P(\text{dues cares})=\big(1-(1-x)^2\big)\big(1-(1-y)^2\big)$$ $$P(\text{una cara})=\big(1-(1-x)^2\big)(1-y)^2+(1-x)^2\big(1-(1-y)^2\big)$$')],
           r'a) $(1-x)(1-y)$, $\ x(1-y)+(1-x)y$, $\ xy$; b) $(1-x)^2(1-y)^2$, $\ (2x-x^2)(1-y)^2+(1-x)^2(2y-y^2)$, $\ (2x-x^2)(2y-y^2)$')

# 2
pr = [F(95, 161), F(50, 161), F(16, 161)]; cd = [F('0.05'), F('0.04'), F('0.0625')]
R = ck(sum(p * c for p, c in zip(pr, cd)), F(31, 644)); ue = ck(pr[1] * cd[1] / R, F(8, 31))
S[2] = SOL([bayes([('N', pr[0], cd[0]), ('UE', pr[1], cd[1]), ('F', pr[2], cd[2])], 'R', 'R̄'),
            st('a) Probabilitat total:', r'$$P(R)=\tfrac{95}{161}\cdot0{,}05+\tfrac{50}{161}\cdot0{,}04+\tfrac{16}{161}\cdot0{,}0625=\tfrac{4{,}75+2+1}{161}=\tfrac{7{,}75}{161}=\tfrac{31}{644}\approx0{,}0481$$ (de mitjana, uns 7,75 vols retardats cada cap de setmana).'),
            st('b) Bayes:', r'$$P(UE\,|\,R)=\dfrac{2/161}{7{,}75/161}=\dfrac{2}{7{,}75}=\dfrac{8}{31}\approx0{,}2581$$')],
           r'a) $\frac{31}{644}\approx0{,}0481$; b) $\frac{8}{31}\approx0{,}2581$')

# 3
pc_ = ck(F(1, 2) * F('0.6') + F(1, 2), F('0.8')); t3 = ck(pc_ ** 3, F('0.512')); u1 = ck(3 * (1 - pc_) * pc_ ** 2, F('0.384'))
m1 = ck(F(1, 2) * F('0.36') / (F(1, 2) * F('0.36') + F(1, 2)), F(9, 34))
S[3] = SOL([st('a) Una tirada:', r'en cada repetició es tria una moneda a l’atzar; per la probabilitat total, $$P(C)=\tfrac12\cdot0{,}6+\tfrac12\cdot1=0{,}8$$ Com que la moneda es torna a la bossa, les tres tirades són independents i el nombre de cares és $X\sim B(3;\ 0{,}8)$.'),
            st('1)', r'$P(X=3)=0{,}8^3=0{,}512$'),
            st('2)', r'Exactament una creu és $X=2$: $\ \binom32\,0{,}8^2\cdot0{,}2=3\cdot0{,}64\cdot0{,}2=0{,}384$'),
            st('b) Ara es llança dues vegades la mateixa moneda.', r'$P(CC\,|\,M_1)=0{,}6^2=0{,}36$ i $P(CC\,|\,M_2)=1$. $$P(CC)=\tfrac12\cdot0{,}36+\tfrac12\cdot1=0{,}68$$'),
            st('Bayes:', r'$$P(M_1\,|\,CC)=\dfrac{0{,}18}{0{,}68}=\dfrac{9}{34}\approx0{,}2647\qquad P(M_2\,|\,CC)=\dfrac{0{,}5}{0{,}68}=\dfrac{25}{34}\approx0{,}7353$$')],
           r'a) 1) $0{,}512$; 2) $0{,}384$; b) $P(M_1|CC)=\frac{9}{34}\approx0{,}2647$, $P(M_2|CC)=\frac{25}{34}\approx0{,}7353$')

# 4
v = [cdf(10, F('0.7'), 8, 10), cdf(10, F('0.7'), 5, 10), cdf(10, F('0.7'), 3, 8)]
for t_, r_ in zip(v, [0.3828, 0.9527, 0.8491]): ck(float(t_), r_, 1e-4)
S[4] = SOL([st('Variable.', r'Si el 30 % no aconsegueix venda, el 70 % sí: $X=$ «nombre de vendes en les 10 telefonades» $\sim B(10;\ 0{,}7)$.'),
            st('a)', L(r'Més de 7 és $X\ge8$: $$P(X\ge8)=@a+@b+@c\approx@r$$', a=bin_(10, '0.7', 8), b=bin_(10, '0.7', 9), c='0{,}7^{10}', r=d4(v[0])) + L(r'$\ (=@x+@y+@z)$', x=d4(pmf(10, F('0.7'), 8)), y=d4(pmf(10, F('0.7'), 9)), z=d4(pmf(10, F('0.7'), 10)))),
            st('b)', L(r'$$P(X\ge5)=1-P(X\le4)=1-\big(P(0)+P(1)+P(2)+P(3)+P(4)\big)\approx1-@q=@r$$', q=d4(1 - v[1]), r=d4(v[1]))),
            st('c)', L(r'$$P(3\le X\le8)=1-P(X\le2)-P(X=9)-P(X=10)\approx1-@a-@b-@c=@r$$', a=d4(cdf(10, F('0.7'), 0, 2)), b=d4(pmf(10, F('0.7'), 9)), c=d4(pmf(10, F('0.7'), 10)), r=d4(v[2])))],
           L(r'a) $@a$; b) $@b$; c) $@c$', a=d4(v[0]), b=d4(v[1]), c=d4(v[2])))

# 5
p3 = ck((F('0.1025') - F('0.3') * F('0.1') - F('0.25') * F('0.05')) / F('0.45'), F(2, 15))
nb = ck(F('0.3') * F('0.9') / (1 - F('0.1025')), F(108, 359)); nm2 = ck(1 - F('0.25') * F('0.05') / F('0.1025'), F(36, 41))
S[5] = SOL([st('Dades:', r'$P(M_1)=0{,}3$, $P(M_2)=0{,}25$, $P(M_3)=0{,}45$; $P(D|M_1)=0{,}1$, $P(D|M_2)=0{,}05$, $P(D|M_3)=p$ i $P(D)=0{,}1025$.'),
            st('a) Probabilitat total amb una incògnita:', r'$$0{,}1025=0{,}3\cdot0{,}1+0{,}25\cdot0{,}05+0{,}45\,p=0{,}0425+0{,}45\,p\ \Rightarrow\ p=\dfrac{0{,}06}{0{,}45}=\dfrac{2}{15}\approx0{,}1333$$'),
            st('b) Bayes:', r'$$P(M_1|\overline{D})=\dfrac{0{,}3\cdot0{,}9}{1-0{,}1025}=\dfrac{0{,}27}{0{,}8975}=\dfrac{108}{359}\approx0{,}3008$$'),
            st('c) Contrari:', r'$$P(\overline{M_2}|D)=1-P(M_2|D)=1-\dfrac{0{,}25\cdot0{,}05}{0{,}1025}=1-\dfrac{5}{41}=\dfrac{36}{41}\approx0{,}8780$$')],
           r'a) $\frac{2}{15}\approx0{,}1333$; b) $\frac{108}{359}\approx0{,}3008$; c) $\frac{36}{41}\approx0{,}8780$')

# 6
w = [pmf(10, F('0.6'), 0), pmf(10, F('0.6'), 4), cdf(10, F('0.6'), 8, 10)]
for t_, r_ in zip(w, [0.0001, 0.1115, 0.1673]): ck(float(t_), r_, 1e-4)
S[6] = SOL([st('Variable.', r'$X=$ «nombre de missatges amb emoticona» $\sim B(10;\ 0{,}6)$.'),
            st('a)', L(r'$P(X=0)=0{,}4^{10}\approx@a$ (exactament $0{,}0001048576$).', a=d4(w[0]))),
            st('b)', L(r'Dues cinquenes parts de 10 són 4 missatges: $$P(X=4)=@t=210\cdot0{,}0256\cdot0{,}046656\approx@a$$', t=bin_(10, '0.6', 4), a=d4(w[1]))),
            st('c)', L(r'$$P(X\ge8)=@x+@y+@z\approx@a$$', x=d4(pmf(10, F('0.6'), 8)), y=d4(pmf(10, F('0.6'), 9)), z=d4(pmf(10, F('0.6'), 10)), a=d4(w[2])))],
           L(r'a) $@a$; b) $@b$; c) $@c$', a=d4(w[0]), b=d4(w[1]), c=d4(w[2])))

# 7
dif = ck(1 - (F('0.4') ** 2 + F('0.25') ** 2 + F('0.35') ** 2), F('0.655')); m4 = pmf(10, F('0.4'), 4); m1_ = 1 - F('0.6') ** 10
ck(float(m4), 0.2508, 1e-4); ck(float(m1_), 0.9940, 1e-4)
S[7] = SOL([st('a)', r'$P(P)=1-0{,}4-0{,}25=0{,}35$'),
            st('b) Contrari:', r'que demanen el mateix tipus. Els dos clients són independents: $$P(\text{distints})=1-(0{,}4^2+0{,}25^2+0{,}35^2)=1-0{,}345=0{,}655$$'),
            st('c)', L(r'$X=$ «clients del grup que demanen margarida» $\sim B(10;\ 0{,}4)$: $$P(X=4)=@t\approx@a$$', t=bin_(10, '0.4', 4), a=d4(m4))),
            st('d)', L(r'$P(X\ge1)=1-P(X=0)=1-0{,}6^{10}\approx@a$', a=d4(m1_)))],
           L(r'a) $0{,}35$; b) $0{,}655$; c) $@a$; d) $@b$', a=d4(m4), b=d4(m1_)))

# 8
dT = ck(F('0.35') * F('0.03') + F('0.45') * F('0.04') + F('0.2') * F('0.01'), F('0.0305'))
eu = ck(F('0.35') * F('0.97') / (1 - dT), F(679, 1939)); g3 = cdf(9, F('0.4'), 3, 9); ck(float(g3), 0.7682, 1e-4)
S[8] = SOL([bayes([('EUA', F('0.35'), F('0.03')), ('Xina', F('0.45'), F('0.04')), ('Alem.', F('0.2'), F('0.01'))], 'D', 'D̄'),
            st('a) Probabilitat total:', r'$$P(D)=0{,}35\cdot0{,}03+0{,}45\cdot0{,}04+0{,}2\cdot0{,}01=0{,}0105+0{,}018+0{,}002=0{,}0305$$ (els percentatges de models no fan falta).'),
            st('b) Bayes:', r'$$P(EUA\,|\,\overline{D})=\dfrac{0{,}35\cdot0{,}97}{1-0{,}0305}=\dfrac{0{,}3395}{0{,}9695}\approx0{,}3502$$'),
            st('c)', L(r'A Alemanya el 40 % són del model M2: $X\sim B(9;\ 0{,}4)$. $$P(X\ge3)=1-P(0)-P(1)-P(2)=1-0{,}6^9-9\cdot0{,}4\cdot0{,}6^8-36\cdot0{,}4^2\cdot0{,}6^7\approx@a$$', a=d4(g3)))],
           L(r'a) $0{,}0305$; b) $\approx0{,}3502$; c) $@a$', a=d4(g3)))

# 9
l1 = pmf(4, F(3, 5), 1); l2 = cdf(4, F(3, 5), 0, 2); al = 1 - F(2, 5) ** 4
nmin = math.ceil(math.log(0.001) / math.log(0.4)); ck(nmin, 8); ck(F(2, 5) ** 8 < F(1, 1000) < F(2, 5) ** 7, True)
ck(l1, F(96, 625)); ck(l2, F(328, 625))
S[9] = SOL([st('Variable.', r'$X=$ «nombre de publicacions amb «M’agrada»» $\sim B\left(4,\frac35\right)$.'),
            st('a)', L(r'Exactament un «M’agrada»: $$P(X=1)=\binom41\cdot\tfrac35\cdot\left(\tfrac25\right)^3=\tfrac{96}{625}=0{,}1536$$ (Si s’entén «almenys un»: $1-\left(\frac25\right)^4=\frac{609}{625}=0{,}9744$.)')),
            st('b)', r'$$P(X\le2)=1-P(X=3)-P(X=4)=1-\tfrac{216}{625}-\tfrac{81}{625}=\tfrac{328}{625}=0{,}5248$$'),
            st('c)', r'Amb $n$ publicacions: $1-0{,}4^n>0{,}999\iff0{,}4^n<0{,}001\iff n\ln0{,}4<\ln0{,}001\iff n>\dfrac{\ln0{,}001}{\ln0{,}4}\approx7{,}54$ (en dividir per $\ln0{,}4<0$ la desigualtat gira). Comprovació: $0{,}4^7\approx0{,}0016$ i $0{,}4^8\approx0{,}00066$.')],
           r'a) $0{,}1536$; b) $0{,}5248$; c) <strong>8 publicacions</strong>')
ck(al, F(609, 625))

# 10
M = [[17, 6, 7, 1], [22, 17, 10, 3], [8, 12, 11, 6]]
ck(sum(map(sum, M)), 120); na = ck(1 - F(sum(r[3] for r in M), 120), F(11, 12))
noP = 120 - sum(r[1] for r in M); ge25 = sum(r[0] + r[2] + r[3] for r in M[1:]); ck(noP, 85); ck(ge25, 60)
pTA = ck(F(M[1][2] + M[1][3], sum(M[1])), F(1, 4)); c3 = cdf(10, pTA, 0, 3); ck(float(c3), 0.7759, 1e-4)
S[10] = SOL([taula(['<25', '25-60', '>60'], [r'\text{Nov.}', r'\text{Poe.}', r'\text{Tea.}', r'\text{Ass.}'], [r + [sum(r)] for r in M] + [[sum(c) for c in zip(*M)] + [120]], str),
             st('a)', r'Hi ha $1+3+6=10$ persones que prefereixen l’assaig: $\ P(\overline{\text{Ass.}})=1-\frac{10}{120}=\frac{11}{12}\approx0{,}9167$'),
             st('b) Condicionada (ens restringim als que no prefereixen la poesia):', r'n’hi ha $120-35=85$, i d’aquests en tenen 25 o més $(22+10+3)+(8+11+6)=60$: $$P(\geq25\ \text{anys}\,|\,\overline{\text{Poe.}})=\dfrac{60}{85}=\dfrac{12}{17}\approx0{,}7059$$'),
             st('c)', L(r'Entre els 52 membres de 25 a 60 anys, prefereixen teatre o assaig $10+3=13$: $p=\frac{13}{52}=\frac14$. Amb $X\sim B\left(10,\frac14\right)$: $$P(X\le3)=0{,}75^{10}+10\cdot0{,}25\cdot0{,}75^9+45\cdot0{,}25^2\cdot0{,}75^8+120\cdot0{,}25^3\cdot0{,}75^7\approx@a$$', a=d4(c3)))],
            L(r'a) $\frac{11}{12}\approx0{,}9167$; b) $\frac{12}{17}\approx0{,}7059$; c) $@a$', a=d4(c3)))

# 11
pT = ck(F('0.2') * F('0.9') + F('0.8') * F('0.05'), F('0.22')); sP = ck(F('0.04') / pT, F(2, 11)); m2 = cdf(8, F('0.2'), 0, 2); ck(float(m2), 0.7969, 1e-4)
S[11] = SOL([bayes([('M', F('0.2'), F('0.9')), ('S', F('0.8'), F('0.05'))], '+', '−'),
             st('a) Probabilitat total:', r'$P(+)=0{,}2\cdot0{,}9+0{,}8\cdot0{,}05=0{,}18+0{,}04=0{,}22$'),
             st('b) Bayes:', r'$P(S\,|\,+)=\dfrac{0{,}04}{0{,}22}=\dfrac{2}{11}\approx0{,}1818$'),
             st('c)', L(r'$X=$ «malalts entre les 8 persones» $\sim B(8;\ 0{,}2)$: $$P(X\le2)=0{,}8^8+8\cdot0{,}2\cdot0{,}8^7+28\cdot0{,}2^2\cdot0{,}8^6\approx@a$$', a=d4(m2)))],
            L(r'a) $0{,}22$; b) $\frac{2}{11}\approx0{,}1818$; c) $@a$', a=d4(m2)))

# 12
G = ck(F(1, 2) * F(1, 3) + F(1, 2) * F(1, 2), F(5, 12)); cG = ck(F(1, 6) / G, F(2, 5)); g5 = ck(pmf(7, F(1, 3), 5), F(28, 729))
S[12] = SOL([bayes([('Cara', F(1, 2), F(1, 3)), ('Creu', F(1, 2), F(1, 2))], 'G', 'Ḡ'),
             st('a)', r'Amb cara cal un 5 o un 6 ($\frac26=\frac13$); amb creu, un parell ($\frac12$): $$P(G)=\tfrac12\cdot\tfrac13+\tfrac12\cdot\tfrac12=\tfrac16+\tfrac14=\tfrac{5}{12}\approx0{,}4167$$'),
             st('b) Bayes:', r'$P(\text{Cara}\,|\,G)=\dfrac{1/6}{5/12}=\dfrac25=0{,}4$'),
             st('c)', r'Si sempre ix cara, cada ronda es guanya amb probabilitat $\frac13$ i $X\sim B\left(7,\frac13\right)$: $$P(X=5)=\binom75\left(\tfrac13\right)^5\left(\tfrac23\right)^2=21\cdot\tfrac{4}{2187}=\tfrac{28}{729}\approx0{,}0384$$')],
            r'a) $\frac{5}{12}\approx0{,}4167$; b) $\frac25$; c) $\frac{28}{729}\approx0{,}0384$')

# 13
Ro = ck(F('0.1') * F('0.75') + F('0.4') * F('0.125') + F('0.5') * F('0.55'), F('0.4'))
rd = ck(F('0.5') * F('0.45') / (1 - Ro), F('0.375')); r56 = cdf(10, F('0.55'), 5, 6); ck(float(r56), 0.4724, 1e-4)
S[13] = SOL([bayes([('H', F('0.1'), F('0.75')), ('T', F('0.4'), F('0.125')), ('D', F('0.5'), F('0.55'))], 'Ro', 'Ra'),
             st('Dades:', r'herba ($H$) 10 %, terra batuda ($T$) 40 %, pista dura ($D$) 50 %. Com que en cada partit guanya un dels dos, en herba Roger en guanya el 75 %.'),
             st('a) Probabilitat total:', r'$P(Ro)=0{,}1\cdot0{,}75+0{,}4\cdot0{,}125+0{,}5\cdot0{,}55=0{,}075+0{,}05+0{,}275=0{,}4$: <strong>el 40 %</strong>.'),
             st('b) Bayes:', r'$P(Ra)=0{,}6$ i $\ P(D\,|\,Ra)=\dfrac{0{,}5\cdot0{,}45}{0{,}6}=\dfrac{0{,}225}{0{,}6}=0{,}375$'),
             st('c)', L(r'$X=$ «partits guanyats per Roger» $\sim B(10;\ 0{,}55)$: $$P(X=5)+P(X=6)=@a+@b\approx@c$$', a=d4(pmf(10, F('0.55'), 5)), b=d4(pmf(10, F('0.55'), 6)), c=d4(r56)))],
            L(r'a) 40 %; b) $0{,}375$; c) $@a$', a=d4(r56)))
