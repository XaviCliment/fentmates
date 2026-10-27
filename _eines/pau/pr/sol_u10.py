# Solucions dels exercicis PAU de distribució binomial i normal (Comunitat Valenciana): números 1, 6, 7, 10 i 105 del dossier.
# Com a la PAU: binomial amb la fórmula o amb la taula; normal amb z arredonit a dues decimals i la taula N(0,1).
import math
from comu import *
import comu
def ck(x, y, tol=1e-9): return comu.ck(x, y, tol)
S = {}
def pmf(n, p, k): return math.comb(n, k) * p ** k * (1 - p) ** (n - k)
def T(z): return Phi(round(z, 2)) if z >= 0 else round(1 - Phi(round(-z, 2)), 4)
def d4(x): return ('%.4f' % x).replace('.', '{,}')

# 1
p0 = ck(0.1 ** 4, 0.0001, 1e-12)
S[1] = SOL([st('Variable.', r'$X=$ «nombre d’excel·lents en els 4 exàmens» $\sim B(4;\ 0{,}9)$: 4 proves independents amb probabilitat d’èxit $0{,}9$.'),
            st('Fórmula:', r'$$P(X=0)=\binom40\,0{,}9^0\,0{,}1^4=0{,}0001$$'),
            st('Amb la taula:', r'$p=0{,}9$ no és a la taula; comptem els exàmens sense excel·lent, $Y=4-X\sim B(4;\ 0{,}1)$: $P(X=0)=P(Y=4)=0{,}0001$ (bloc $n=4$, columna $0{,}10$).')],
           r'$P(X=0)=0{,}0001$')
# 6
a = ck(T(1.14) - T(0.57), 0.1572); b = ck(1 - T(1.43), 0.0764); c = ck(T(-1.43), 0.0764)
S[6] = SOL([st('Tipificació.', r'$X\sim N(100,14)\Rightarrow Z=\dfrac{X-100}{14}\sim N(0,1)$. Arredonim $z$ a dues decimals i fem servir la taula.'),
            st('a)', r'$$P(108\le X\le116)=P\left(\tfrac{8}{14}\le Z\le\tfrac{16}{14}\right)=P(0{,}57\le Z\le1{,}14)=0{,}8729-0{,}7157=0{,}1572$$ $1200\cdot0{,}1572\approx188{,}6$: unes <strong>189 persones</strong>.'),
            st('b)', r'$$P(X\gt120)=P(Z\gt1{,}43)=1-0{,}9236=0{,}0764$$ $1200\cdot0{,}0764\approx91{,}7$: unes <strong>92 persones</strong>.'),
            st('c)', r'Per simetria, $P(X\lt80)=P(Z\lt-1{,}43)=1-0{,}9236=0{,}0764$: també unes <strong>92 persones</strong>.')],
           r'a) 189; b) 92; c) 92 persones (aproximadament)')
ck(round(1200 * a), 189); ck(round(1200 * b), 92)
# 7
q5 = 0.517 ** 5; r5 = 0.483 ** 5; a = ck(1 - q5, 0.9631, 1e-4); b = ck(1 - r5, 0.9737, 1e-4)
S[7] = SOL([st('Variable.', r'$X=$ «nombre de xics entre els 5 fills» $\sim B(5;\ 0{,}517)$ (els naixements són independents). $p=0{,}517$ no és a la taula: fem servir la fórmula i el contrari.'),
            st('a)', L(r'«Almenys una xica» és el contrari de «5 xics»: $$P=1-P(X=5)=1-0{,}517^5=1-@q=@a$$', q=d4(q5), a=d4(a))),
            st('b)', L(r'«Almenys un xic» és el contrari de «cap xic» (5 xiques): $$P=1-P(X=0)=1-0{,}483^5=1-@r=@b$$', r=d4(r5), b=d4(b)))],
           L(r'a) $@a$; b) $@b$', a=d4(a), b=d4(b)))
# 10
t0, t1 = 0.1975, 0.3951; ck(round(pmf(4, 1 / 3, 0), 4), t0); ck(round(pmf(4, 1 / 3, 1), 4), t1); r = ck(1 - t0 - t1, 0.4074, 1e-9); ck(1 - pmf(4, 1 / 3, 0) - pmf(4, 1 / 3, 1), 11 / 27)
S[10] = SOL([st('Variable.', r'$X=$ «nombre de respostes correctes» $\sim B\left(4,\frac13\right)$: 4 preguntes independents, cadascuna amb probabilitat $\frac13$ d’encertar a l’atzar.'),
             st('Amb la taula de la PAU', r'(bloc $n=4$, columna $p=1/3$): $P(X=0)=0{,}1975$, $P(X=1)=0{,}3951$.'),
             st('Contrari:', r'$$P(X\ge2)=1-P(X=0)-P(X=1)=1-0{,}1975-0{,}3951=0{,}4074$$'),
             st('Amb la fórmula', r's’obté el valor exacte: $1-\left(\frac23\right)^4-4\cdot\frac13\cdot\left(\frac23\right)^3=1-\frac{16}{81}-\frac{32}{81}=\frac{33}{81}=\frac{11}{27}\approx0{,}4074$.')],
            r'$P(X\ge2)=\frac{11}{27}\approx0{,}4074$')
# 105
pv = ck(0.3 * 0.5 + 0.7 * 0.05, 0.185); b = ck(0.15 / pv, 30 / 37)
c0, c1 = 0.8145, 0.1715; ck(round(pmf(4, .05, 0), 4), c0); ck(round(pmf(4, .05, 1), 4), c1); c = ck(1 - c0 - c1, 0.014, 1e-9)
d = ck(T(2.1), 0.9821)
S[105] = SOL([bayes([('T', F('0.3'), F('0.5')), ('T̄', F('0.7'), F('0.05'))], 'V', 'V̄'),
              st('a) Probabilitat total:', r'$P(V)=0{,}3\cdot0{,}5+0{,}7\cdot0{,}05=0{,}15+0{,}035=0{,}185$'),
              st('b) Bayes:', r'$P(T|V)=\dfrac{0{,}15}{0{,}185}=\dfrac{30}{37}\approx0{,}8108$'),
              st('c) Binomial amb la taula:', r'$X\sim B(4;\ 0{,}05)$ (bloc $n=4$, columna $0{,}05$): $$P(X\ge2)=1-P(X=0)-P(X=1)=1-0{,}8145-0{,}1715=0{,}0140$$'),
              st('d) Aproximació normal:', r'$X\sim B(100;\ 0{,}5)$, amb $np=nq=50\ge5$: $X\approx X^\prime\sim N\left(50,\sqrt{100\cdot0{,}5\cdot0{,}5}=5\right)$. Amb la correcció de continuïtat: $$P(X\ge40)\approx P(X^\prime\ge39{,}5)=P\left(Z\ge\tfrac{39{,}5-50}{5}\right)=P(Z\ge-2{,}1)=P(Z\le2{,}1)=0{,}9821$$')],
             r'a) $0{,}185$; b) $\frac{30}{37}\approx0{,}8108$; c) $0{,}0140$; d) $0{,}9821$')
