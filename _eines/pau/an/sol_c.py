# Solucions dels exercicis PAU d'anàlisi (Comunitat Valenciana), números 81-118 del dossier.
import math
from anlib import *
from sol_a import opt, gq
S = {}
LAB5 = {'dom': 'a)', 'asi': 'b)', 'mon': 'c)', 'ext': 'd)', 'gra': 'e)'}
LAB4 = {'dom': 'a)', 'asi': 'b)', 'mon': 'c)', 'ext': 'c)', 'gra': 'd)'}

# 81
B81 = P(F('-0.01'), 1, -9); t81, x81, y81 = opt(B81, 'x', 'B', 'màxim'); ck(x81, 50); ck(y81, 16)
e81, _ = eq2(F('-0.01'), 1, -9)
S[81] = SOL([st('a)', r'$B(x)=I(x)-C(x)=4x-9-0{,}01x^2-3x=-0{,}01x^2+x-9$.'),
             st('b)', t81 + r' El preu ha de ser de 50 € i el benefici màxim és de 16 000 €.'),
             st('c)', r'Talls: $B(0)=-9$ → $(0,-9)$; ' + e81 + r' → $(10,0)$ i $(90,0)$. Creix en $(0,50)$ i decreix en $(50,+\infty)$.'),
             gq(B81, 0, 100, pts=[(0, -9), (10, 0), (50, 16), (90, 0)], xr=(-5, 105)),
             st('d)', r'$B(x)<0$ fora de les arrels: si $0\le x<10$ o si $x>90$ euros.')],
            r'a) $B(x)=-0{,}01x^2+x-9$; b) 50 €, 16 000 €; d) pèrdues si el preu és menor de 10 € o major de 90 €.')

# 82
f82 = P(F(-1, 800), 0, F(3, 2), 30, v='t'); ck(f82(20), 50); ck(f82(40), 10)
S[82] = SOL([st('a)', r"$f'(t)=\dfrac32-\dfrac{3t^2}{800}=0\iff t^2=400\iff t=20$ ($t\ge0$). $f''(t)=-\dfrac{6t}{800}<0$: màxim. $f(20)=30+30-10=50$ tones."),
             st('b)', r'$f(40)=30+60-\dfrac{64000}{800}=90-80=10$ tones: just el mínim exigit, per tant (amb les justes) és rendible.'),
             st('c)', r"Per a $t>20$, $f'(t)<0$: l’extracció decreix. Aleshores, si $t>40$, $f(t)<f(40)=10$: a partir dels 40 anys l’explotació ja no és rendible mai més."),
             gq(f82, 0, 50, v='t', pts=[(20, 50), (40, 10)], yl='f')],
            r'a) A l’any 20, 50 tones; b) $f(40)=10$: sí (just el mínim); c) sí, tot el període $t>40$.')

# 83
s83, r83 = estudi(R(P(1, 0, 0), P(-1, 2)), lab=LAB5, xr=(-8, 12), yr=(-20, 14))
S[83] = SOL(s83, resum(r83))

# 84
f84 = P(1, -8, 15, 0, v='t'); t1, t2 = (8 - math.sqrt(19)) / 3, (8 + math.sqrt(19)) / 3
S[84] = SOL([st('a)', r'$f(t)=t(t^2-8t+15)=t(t-3)(t-5)$. En $[0,6]$: $f>0$ en $(0,3)\cup(5,6]$ (beneficis) i $f<0$ en $(3,5)$ (pèrdues).'),
             st('Derivada:', r"$f'(t)=3t^2-16t+15=0\iff t=\dfrac{8\pm\sqrt{19}}{3}$, és a dir, $t_1\approx%s$ i $t_2\approx%s$. $f'>0$ en $[0,t_1)$, $f'<0$ en $(t_1,t_2)$ i $f'>0$ en $(t_2,6]$." % (ap(t1), ap(t2))),
             st('b)', r'Màxim relatiu en $t_1$: $f(t_1)\approx%s$. Però a l’extrem de l’interval $f(6)=216-288+90=18$, que és més gran: el màxim benefici de tot el període és en $t=6$, amb 18 desenes de milers d’euros (180 000 €). (Si es pregunta pel màxim relatiu: $t\approx1{,}21$ anys, uns 82 100 €.)' % ap(f84(t1))),
             st('c)', r'Mínim en $t_2\approx%s$ anys: $f(t_2)\approx%s$, és a dir, una pèrdua d’uns %s €.' % (ap(t2), ap(f84(t2)), '40\\,600')),
             st('d)', r"No: per a $t>t_2$ la derivada és positiva i, com que $f(5)=0$, per a $t>5$ la funció és sempre positiva i creixent. L’empresa ja no tornarà a tenir pèrdues."),
             gq(f84, 0, 7, v='t', pts=[(t1, f84(t1)), (t2, f84(t2)), (3, 0), (5, 0), (6, 18)], xr=(-0.3, 7))],
            r'a) Beneficis en $(0,3)\cup(5,6]$, pèrdues en $(3,5)$; b) màxim en $t=6$: 180 000 € (màxim relatiu en $t\approx1{,}21$); c) $t\approx4{,}12$: pèrdua de $\approx40\,600$ €; d) no.')
ck(f84(t2), -4.06, 0.01); ck(f84(t1), 8.21, 0.01)

# 85
s85, r85 = estudi(R(P(1, -2, -3), P(1, 1, -2)), lab=LAB5, xr=(-7, 6), yr=(-8, 8))
S[85] = SOL(s85, resum(r85))

# 86
b86, v86 = barrow(P(1, -3, 3), -2, 1); ck(v86, F(33, 2))
S[86] = SOL([st('a)', r'Cada tros és continu ($x^2+1\ne0$). En $x=1$: $\displaystyle\lim_{x\to1^-}(x^2-3x+3)=1=f(1)$ i $\displaystyle\lim_{x\to1^+}\frac{ax^2}{x^2+1}=\frac a2$. Contínua si $\frac a2=1\iff a=2$.'),
             st('b)', r"Si $x<1$: $f'(x)=2x-3<0$. Si $x>1$: $$f'(x)=\frac{4x(x^2+1)-2x^2\cdot2x}{(x^2+1)^2}=\frac{4x}{(x^2+1)^2}>0$$ Decreix en $(-\infty,1)$ i creix en $(1,+\infty)$ (mínim absolut en $(1,1)$)."),
             st('c)', r'No té asímptotes verticals (és contínua en $\mathbb R$). $\displaystyle\lim_{x\to+\infty}\frac{2x^2}{x^2+1}=2$: asímptota horitzontal $y=2$ cap a $+\infty$; cap a $-\infty$, $\displaystyle\lim_{x\to-\infty}(x^2-3x+3)=+\infty$, no n’hi ha.'),
             st('d)', r'En $[-2,1]$, $f(x)=x^2-3x+3$: $$' + b86 + '$$'),
             plot([(lambda x: x * x - 3 * x + 3, [-3, 1]), (lambda x: 2 * x * x / (x * x + 1), [1, 10])], xr=(-3, 10), yr=(-0.5, 8), ha=[2], pts=[(1, 1)])],
            r'a) $a=2$; b) decreix en $(-\infty,1)$, creix en $(1,+\infty)$; c) AH $y=2$ (cap a $+\infty$), sense AV; d) $\frac{33}{2}$.')

# 87
s87, r87 = estudi(R(P(2, -3, 5), P(1, 0, -1)), lab=LAB5, xr=(-6, 6), yr=(-12, 14))
S[87] = SOL(s87, resum(r87))

# 88
B88 = P(-1, 16, -55); t88, x88, y88 = opt(B88, 'x', 'B', 'màxim'); ck(B88(6), 5); ck(x88, 8); ck(y88, 9)
S[88] = SOL([st('a)', r'$B(6)=-36+96-55=5$ €.'),
             st('b)', r'$B(x)>0\iff x^2-16x+55<0\iff(x-5)(x-11)<0\iff 5<x<11$ €.'),
             st('c)', t88),
             st('d)', r"$B'(x)=-2x+16$: creix si $x<8$ i decreix si $x>8$."),
             gq(B88, 3, 13, pts=[(5, 0), (8, 9), (11, 0), (6, 5)], xr=(2, 14))],
            r'a) 5 €; b) entre 5 i 11 €; c) a 8 €, benefici de 9 €; d) creix fins a 8 € i després decreix.')

# 89
s89, r89 = estudi(R(P(1, 0, 0), P(1, -1)), lab=LAB5, xr=(-6, 8), yr=(-14, 14))
S[89] = SOL(s89, resum(r89))

# 90
f90 = P(-1, 350, -15000); t90, x90, y90 = opt(f90, 'x', 'f', 'màxim'); ck(x90, 175); ck(y90, 15625)
e90, _ = eq2(-1, 350, -15000)
S[90] = SOL([st('a) i b)', t90),
             st('c)', e90 + r'. El benefici és positiu entre les dues arrels: a partir de 51 bicicletes llogades (més de 50).'),
             st('d)', r'Sí: si es lloguen més de 300 bicicletes (fins a 350), $f(x)<0$ i torna a haver pèrdues.'),
             gq(f90, 0, 350, pts=[(50, 0), (175, 15625), (300, 0)], xr=(-10, 360))],
            r'a) 175 bicicletes; b) 15 625 €; c) més de 50 bicicletes; d) sí, amb més de 300.')

# 91
s91, r91 = estudi(R(P(-1, 0, 1), P(1, 0, -4)), lab=LAB5, xr=(-6, 6), yr=(-5, 4))
S[91] = SOL(s91, resum(r91))

# 92
f92 = P(-15, 1500, 36600); t92, x92, y92 = opt(f92, 'x', 'f', 'màxim'); ck(x92, 50); ck(y92, 74100); ck(f92(110), 20100)
S[92] = SOL([st('a)', r'$f(0)=36\,600$ milers de m³.'),
             st('b)', t92 + r' Al cap de 50 anys (inici de 2030), amb 74 100 milers de m³.'),
             st('c)', r'Deixa de ser rendible quan el benefici per m³ s’anul·la: $3-\dfrac{3x^2}{12100}=0\iff x^2=12100\iff x=110$ anys. Aleshores $f(110)=36600+165000-181500=20\,100$ milers de m³.')],
            r'a) 36 600 milers de m³; b) 50 anys, 74 100 milers de m³; c) 110 anys, 20 100 milers de m³.')

# 93
s93, r93 = estudi(R(P(1, 0, -36), P(1, -2, -8)), lab=LAB5, xr=(-10, 12), yr=(-10, 12))
S[93] = SOL(s93, resum(r93))

# 94
B94 = P(-2, 340, -672); t94, x94, y94 = opt(B94, 'x', 'B', 'màxim'); ck(x94, 85); ck(y94, 13778); ck(B94(100), 13328)
e94, _ = eq2(-2, 340, -672)
S[94] = SOL([st('Benefici:', r'$B(x)=I(x)-G(x)=4x^2+800x-6x^2-460x-672=-2x^2+340x-672$.'),
             st('a)', r'$B(x)\ge0$: ' + e94 + r'. El benefici és no negatiu entre 2 i 168: cal fabricar com a mínim 2 unitats.'),
             st('b)', t94 + r' Cal fabricar 85 unitats i el benefici és de 13 778 €.'),
             st('c)', r"Per a $x\ge100$, $B'(x)=-4x+340<0$: el benefici decreix. El màxim amb la normativa és en $x=100$: $B(100)=-20000+34000-672=13\,328$ €."),
             gq(B94, 0, 170, pts=[(2, 0), (85, 13778), (100, 13328), (168, 0)], xr=(-5, 175))],
            r'a) 2 unitats; b) 85 unitats, 13 778 €; c) 13 328 € (fabricant 100 unitats).')

# 95
s95, r95 = estudi(R(P(1, 1, -2), P(1, 2, 1)), lab=LAB5, dt='(x+1)^2', xr=(-8, 6), yr=(-8, 3))
S[95] = SOL(s95, resum(r95))

# 96
B96 = P(F(-1, 100), 40, 50000); t96, x96, y96 = opt(B96, 'x', 'B', 'màxim'); ck(x96, 2000); ck(y96, 90000)
S[96] = SOL([st('Funció:', r'$B(x)=50000+40x-\dfrac{x^2}{100}$, $x\ge0$.'),
             st('a)', t96),
             st('b)', r"$B'(x)=40-\dfrac{x}{50}$: positiva si $0\le x<2000$ (els beneficis creixen) i negativa si $x>2000$ (decreixen)."),
             st('c)', r'$B(x)<B(0)=50000\iff 40x-\dfrac{x^2}{100}<0\iff x(4000-x)<0\iff x>4000$. Sí: invertint més de 4000 € el benefici és menor que sense publicitat.'),
             gq(B96, 0, 5000, pts=[(2000, 90000), (4000, 50000), (0, 50000)], xr=(-100, 5100), yr=(0, 100000))],
            r'a) 2000 €, benefici màxim de 90 000 €; b) creixen en $[0,2000)$ i decreixen a partir de 2000 €; c) sí, a partir de 4000 €.')

# 97
s97, r97 = estudi(R(P(3, -4, -4), P(1, -1, -1)), lab=LAB5, xr=(-5, 6), yr=(-10, 14))
S[97] = SOL(s97, resum(r97))

# 98
f98 = P(F(-1, 10), F(6, 10), F(15, 10), 80); ck(f98(1), 82); ck(f98(2), F('84.6')); ck(f98(5), 90); ck(f98(12), F('11.6'))
S[98] = SOL([st('a)', r'$f(1)=\dfrac{800+15+6-1}{10}=82$ i $f(2)=\dfrac{800+30+24-8}{10}=84{,}6$. No: al cap d’un mes el rendiment és menor.'),
             st('b)', r"$f'(x)=\dfrac{15+12x-3x^2}{10}=0\iff x^2-4x-5=0\iff x=5$ ($x=-1$ no val). $f'>0$ si $x<5$ i $f'<0$ si $x>5$: màxim. $f(5)=\dfrac{800+75+150-125}{10}=90\,\%$."),
             st('c)', r'Com que creix fins a $x=5$ i després decreix, el mínim en $[0,12]$ és en un extrem: $f(0)=80$ i $f(12)=\dfrac{800+180+864-1728}{10}=11{,}6$. El rendiment mínim és 11,6 % > 10 %: no.'),
             gq(f98, 0, 12, pts=[(5, 90), (12, 11.6), (0, 80)], xr=(-0.5, 12.5))],
            r'a) No ($82<84{,}6$); b) als 5 mesos, 90 %; c) no, el mínim és 11,6 %.')

# 99
s99, r99 = estudi(R(P(1, 2, -15), P(2, -3, -2)), lab=LAB5, xr=(-8, 8), yr=(-8, 10))
S[99] = SOL(s99, resum(r99))

# 100
S[100] = SOL([st('a)', r'$1200+250\cdot5+150\cdot3=1200+1250+450=2900$ €.'),
              st('b)', r'Fins a 250 kWh es paga a 5 €; entre 250 i 900, 3 € per cada kWh que passa de 250 (amb $1200+1250=2450$ € ja acumulats); a partir de 900, 2 € per cada kWh que passa de 900 (amb $2450+650\cdot3=4400$ €): $$R(x)=\begin{cases}1200+5x & \text{si } 0\le x\le250\\ 1700+3x & \text{si } 250<x\le900\\ 2600+2x & \text{si } x>900\end{cases}$$ És contínua: $R(250)=2450$ i $R(900)=4400$ des dels dos costats.'),
              plot([(lambda x: 1200 + 5 * x, [0, 250]), (lambda x: 1700 + 3 * x, [250, 900]), (lambda x: 2600 + 2 * x, [900, 1600]), (lambda x: 1200 + 3 * x, [0, 1600])],
                   xr=(-30, 1650), yr=(0, 6500), pts=[(250, 2450), (900, 4400), (1400, 5400)], labels=[(1450, 6000, 'R₂ = 1200 + 3x')]),
              st('c)', r'L’altra empresa paga $R_2(x)=1200+3x$. Igualem tram a tram: si $0<x\le250$, $1200+5x=1200+3x$ només per a $x=0$; si $250<x\le900$, $1700+3x=1200+3x$ no té solució; si $x>900$, $2600+2x=1200+3x\iff x=1400$. Sí: amb 1400 kWh tots dos rebuts valen $1200+3\cdot1400=5400$ €.')],
             r'a) 2900 €; c) sí: 1400 kWh, amb un rebut de 5400 €.')

# 101
s101, r101 = estudi(R(P(1, -3, 0), P(1, -2, 1)), lab=LAB5, dt='x^2-2x+1=(x-1)^2', xr=(-6, 8), yr=(-10, 4))
S[101] = SOL([st('Simplificació:', r'$x(x-3)+(x+1)=x^2-2x+1=(x-1)^2$, per tant $f(x)=\dfrac{x^2-3x}{(x-1)^2}$.')] + s101, resum(r101))

# 102
S[102] = SOL([st('a)', r'Els dos trossos són polinomis. En $x=-1$: $\displaystyle\lim_{x\to-1^-}(x^3+ax^2+24x)=-1+a-24=a-25=f(-1)$ i $\displaystyle\lim_{x\to-1^+}\left[(x-1)^2+3\right]=7$. Contínua si $a-25=7\iff a=32$.'),
              st('b)', r"Amb $a=9$, en $]-\frac92,-\frac32[$ (on $x\le-1$): $f(x)=x^3+9x^2+24x$, $f'(x)=3x^2+18x+24=3(x+2)(x+4)=0\iff x=-4,\ x=-2$. $f''(x)=6x+18$: $f''(-4)=-6<0$ → màxim local $(-4,\,-16)$; $f''(-2)=6>0$ → mínim local $(-2,\,-20)$."),
              st('c)', r'Amb $a=0$, en $[2,3]$, $f(x)=(x-1)^2+3=x^2-2x+4>0$: $$' + barrow(P(1, -2, 4), 2, 3)[0] + r'$$ $A=\frac{16}{3}$ u².'),
              plot([lambda x: x * x - 2 * x + 4], xr=(-0.5, 4), yr=(-0.5, 9), shade=[(lambda x: x * x - 2 * x + 4, None, 2, 3)])],
             r'a) $a=32$; b) màxim local $(-4,-16)$ i mínim local $(-2,-20)$; c) $\frac{16}{3}$ u².')
ck(P(1, 9, 24, 0)(-4), -16); ck(P(1, 9, 24, 0)(-2), -20); ck(barrow(P(1, -2, 4), 2, 3)[1], F(16, 3))

# 103
dl103 = r"$$f'(x)=\frac{-2\cdot(3x^2-1)\cdot6x}{(3x^2-1)^4}=\frac{-12x}{(3x^2-1)^3}$$"
s103, r103 = estudi(R(P(1), P(9, 0, -6, 0, 1)), lab=LAB5, dt='(3x^2-1)^2', dline=dl103, xr=(-2, 2), yr=(-0.5, 6))
S[103] = SOL(s103, resum(r103))

# 104
I104 = P(-1, 60, 100); t104a, xa, ya = opt(I104, 'x', 'I', 'màxim'); ck(xa, 30); ck(ya, 1000)
B104 = P(-1, 48, 100); t104b, xb, yb = opt(B104, 'x', 'B', 'màxim'); ck(xb, 24); ck(yb, 676)
e104, _ = eq2(-1, 48, 100)
S[104] = SOL([st('a)', t104a),
              st('b)', r'$B(x)=I(x)-12x=-x^2+48x+100$. ' + t104b),
              st('c)', r'$B(x)>0$: ' + e104 + r'. Entre les arrels $B>0$; com que $x\ge0$: $0\le x<50$ kg.')],
             r'a) 30 kg, 1000 €; b) 24 kg, 676 €; c) menys de 50 kg.')

# 105
p1, p2, p3 = R(P(1, 0, 1), P(1, 1)), P(2, 4), P(-1, 3, 60)
c105a, _ = cont(4, p1, p2); c105b, _ = cont(8, p2, p3)
xm = math.sqrt(2) - 1
s105, a105 = area_steps(p3, 8, 9); ck(a105, F(79, 6))
S[105] = SOL([st('a)', r'El primer tros només falla en $x=-1$ (fora de $[0,4)$) i els altres són polinomis. Punts d’unió:'),
              r'<strong>En $x=4$:</strong> ' + c105a, r'<strong>En $x=8$:</strong> ' + c105b,
              st('b)', r"En $(0,4)$: $f'(x)=\dfrac{2x(1+x)-(1+x^2)}{(1+x)^2}=\dfrac{x^2+2x-1}{(1+x)^2}=0\iff x=-1+\sqrt2\approx0{,}41$. En $(4,8)$: $f'(x)=2>0$. En $(8,9)$: $f'(x)=3-2x<0$." +
                 taula_m([('(0,\\sqrt2-1)', '-'), ('(\\sqrt2-1,4)', '+'), ('(4,8)', '+'), ('(8,9)', '-')]) +
                 r'Decreix en $[0,\sqrt2-1)$ i en $(8,9]$; creix en $(\sqrt2-1,4)$ i en $(4,8)$.'),
              st('c)', r'Candidats: $f(0)=1$, $f(\sqrt2-1)=\dfrac{4-2\sqrt2}{\sqrt2}=2\sqrt2-2\approx0{,}83$, $f(4)=12$ (abans del salt els valors s’acosten a $\frac{17}{5}$), $f(8)=20$ i $f(9)=6$. Màxim absolut: $f(8)=20$; mínim absolut: $f(\sqrt2-1)=2\sqrt2-2\approx0{,}83$.'),
              st('d)', r'En $[8,9]$, $f(x)=-x^2+3x+60$ ($f(9)=6>0$).')] + s105[1:] +
             [plot([(lambda x: (1 + x * x) / (1 + x), [0, 3.9999]), (lambda x: 2 * x + 4, [4, 7.9999]), (lambda x: 3 * x + 60 - x * x, [8, 9])], xr=(-0.3, 9.5), yr=(-1, 22),
                   shade=[(lambda x: 3 * x + 60 - x * x, None, 8, 9)], pts=[(4, 3.4, 'o'), (4, 12), (8, 20), (xm, 2 * math.sqrt(2) - 2)])],
             r'a) Discontínua en $x=4$ (salt); b) decreix en $[0,\sqrt2-1)\cup(8,9]$, creix en $(\sqrt2-1,8)$; c) màxim 20 en $x=8$, mínim $2\sqrt2-2$ en $x=\sqrt2-1$; d) $\frac{79}{6}$ u².')

# 106
s106, r106 = estudi(R(P(4, 0, -36), P(1, -2, -8)), lab=LAB4, xr=(-10, 12), yr=(-12, 16))
S[106] = SOL(s106, resum(r106))

# 107
A107 = F(1, 800); B107 = F(50) - A107 * 10000; ck(B107, F('37.5'))
r107 = P(F('-0.15'), 5, 0, v='m'); t107, m107, rm = opt(r107, 'm', 'r', 'màxim'); ck(m107, F(50, 3)); ck(rm, F(125, 3))
S[107] = SOL([st('a)', r"Per a $r>100$, $T'(r)=2Ar$: $T'(1600)=3200A=4\iff A=\frac{1}{800}$. Continuïtat en $r=100$: $\frac{100}{4}+25=50=A\cdot100^2+B=12{,}5+B\iff B=37{,}5$."),
              st('b)', r"$T'(r)=\frac14>0$ si $0<r<100$ i $T'(r)=\frac{r}{400}>0$ si $r>100$: la temperatura sempre creix. No hi ha màxims ni mínims relatius; l’únic extrem és el mínim absolut a l’inici, $T(0)=25$, i no té màxim."),
              st('c)', t107 + r' Mínim en un extrem de $[0,30]$: $r(0)=0$ i $r(30)=150-135=15$, per tant el mínim és $r=0$ en $m=0$. Temperatures (tram $r\le100$): $T\left(\frac{125}{3}\right)=\frac{125}{12}+25=\frac{425}{12}\approx35{,}42$ i $T(0)=25$.')],
             r'a) $A=\frac1{800}$, $B=37{,}5$; b) no (sempre creix); c) màxim en $m=\frac{50}{3}\approx16{,}7$ min ($r\approx41{,}67$, $T\approx35{,}42$); mínim en $m=0$ ($r=0$, $T=25$).')

# 108
s108, r108 = estudi(R(P(1, 0, 0, 0), P(-1, 0, 1)), lab=LAB4, xr=(-5, 5), yr=(-8, 8))
S[108] = SOL([st('Simplificació:', r'$f(x)=\dfrac{x}{1-x^2}-x=\dfrac{x-x(1-x^2)}{1-x^2}=\dfrac{x^3}{1-x^2}$.')] + s108, resum(r108))

# 109
h109 = P(F(-1, 3000), F(29, 3000), F(1, 100))
DA, DB = P(F(29, 3000), F(1, 100)), P(F(1, 3000), 0, 0)
sA, aA = area_steps(DB, 30, 50, q=DA, nf='D_B', ng='D_A'); sB, aB = area_steps(DA, 0, 30, q=DB, nf='D_A', ng='D_B'); ck(aB, F(33, 20)); ck(aA, F(133, 45))
S[109] = SOL([st('a)', r'$\dfrac{x^2}{3000}=\dfrac{1}{100}+\dfrac{29x}{3000}\iff x^2-29x-30=0\iff x=30$ (la solució $x=-1$ no té sentit).'),
              st('b)', r'$D_A-D_B=\dfrac{-x^2+29x+30}{3000}=\dfrac{-(x-30)(x+1)}{3000}$: és positiu si $0\le x<30$ i negatiu si $30<x\le50$. El desgast és menor per a B en $[0,30)$ i menor per a A en $(30,50]$.'),
              st('c) Interval on A desgasta menys, $[30,50]$:', r'$A_1=\displaystyle\int_{30}^{50}(D_B-D_A)\,dx$.')] + sA[1:] +
             [st('Interval on B desgasta menys, $[0,30]$:', r'$A_2=\displaystyle\int_{0}^{30}(D_A-D_B)\,dx$.')] + sB[1:] +
             [plot([lambda x: 0.01 + 29 * x / 3000, lambda x: x * x / 3000], xr=(-1, 52), yr=(-0.05, 0.9),
                   shade=[(lambda x: 0.01 + 29 * x / 3000, lambda x: x * x / 3000, 0, 30), (lambda x: x * x / 3000, lambda x: 0.01 + 29 * x / 3000, 30, 50)], pts=[(30, 0.3)])],
             r'a) 30 mesos; b) B desgasta menys en $[0,30)$ i A en $(30,50]$; c) $\frac{133}{45}\approx2{,}96$ i $\frac{33}{20}=1{,}65$.')

# 110
s110, r110 = estudi(R(P(1, 0), P(1, 2, 1)), lab=LAB4, dt='(x+1)^2', xr=(-6, 5), yr=(-6, 1))
S[110] = SOL([st('Simplificació:', r'$x(2x+4)+2=2(x+1)^2$ i $$f(x)=\frac12-\frac{1+x^2}{2(x+1)^2}=\frac{(x+1)^2-(1+x^2)}{2(x+1)^2}=\frac{2x}{2(x+1)^2}=\frac{x}{(x+1)^2}$$')] + s110, resum(r110))

# 111
B111 = P(-1, 12, -11, v='t'); t111, x111, y111 = opt(B111, 't', 'B', 'màxim'); ck(y111, 25)
b111, v111 = barrow(B111, 3, 8, v='t'); ck(v111, F(340, 3))
S[111] = SOL([st('a)', t111 + ' Als 6 anys, 25 milions d’euros.'),
              st('b)', r'El mínim en $[2,9]$ és en un extrem: $B(2)=9$ i $B(9)=16$. Mínim als 2 anys: 9 milions.'),
              st('c)', r'$-t^2+12t-11>24\iff t^2-12t+35<0\iff(t-5)(t-7)<0\iff 5<t<7$.'),
              st('d)', '$$' + b111 + '$$'),
              gq(B111, 2, 9, v='t', pts=[(6, 25), (2, 9), (9, 16), (5, 24), (7, 24)], xr=(0, 10), yl='B')],
             r'a) $t=6$, 25 M€; b) $t=2$, 9 M€; c) entre els 5 i els 7 anys; d) $\frac{340}{3}$.')

# 112
s112, r112 = estudi(R(P(3, 0, -27), P(1, 1, -2)), lab=LAB4, xr=(-8, 7), yr=(-15, 25))
S[112] = SOL(s112, resum(r112))

# 113
b113, v113 = barrow(P(1, 0, 2, v='t'), 0, 1, v='t'); ck(v113, F(7, 3))
S[113] = SOL([st('a)', r'Continuïtat en $t=1$: $g(1)=3$ i $\displaystyle\lim_{t\to1^+}\left(\frac at+2\right)=a+2\Rightarrow a=1$. En $t=2$: $g(2)=\frac12+2=\frac52$ i $\displaystyle\lim_{t\to2^+}\left(ct+\frac{b}{t^2}\right)=2c+\frac b4\Rightarrow 8c+b=10$. '
                     r"Derivada: si $2<t<4$, $g'(t)=c-\dfrac{2b}{t^3}$, i $g'(3)=c-\dfrac{2b}{27}=\dfrac{23}{27}\Rightarrow 27c-2b=23$. Resolent: $b=10-8c$, $27c-20+16c=23$, $c=1$, $b=2$."),
              st('b)', r"1r gerent: $g'(t)=2t\ge0$, creix. 2n gerent: $g(t)=\frac1t+2$, $g'(t)=-\frac{1}{t^2}<0$, decreix. 3r gerent: $g(t)=t+\frac{2}{t^2}$, $g'(t)=1-\frac{4}{t^3}>0$ si $t>\sqrt[3]{4}\approx1{,}59$, creix. No ha crescut amb tots: amb el segon va baixar."),
              st('c)', r'$g$ és contínua en $[0,4]$. Valors: $g(0)=2$, $g(1)=3$, $g(2)=\frac52$, $g(4)=4+\frac{2}{16}=\frac{33}{8}$. Màxim relatiu en $t=1$ ($g=3$) i mínim relatiu en $t=2$ ($g=\frac52$); màxim absolut $\frac{33}{8}=4{,}125$ en $t=4$ i mínim absolut 2 en $t=0$.'),
              st('d)', r'$100000\cdot$ $$' + b113 + r'$$ El salari del primer gerent és $100000\cdot\frac73\approx233\,333{,}33$ €.'),
              plot([(lambda t: t * t + 2, [0, 1]), (lambda t: 1 / t + 2, [1, 2]), (lambda t: t + 2 / t ** 2, [2, 4])], xr=(-0.2, 4.3), yr=(0, 4.6), pts=[(1, 3), (2, 2.5), (4, 4.125), (0, 2)], xl='t', yl='g')],
             r'a) $a=1$, $b=2$, $c=1$; b) no, amb el segon gerent decreix; c) màx. absolut $\frac{33}{8}$ ($t=4$), mín. absolut 2 ($t=0$), màx. relatiu en $t=1$, mín. relatiu en $t=2$; d) $\approx233\,333$ €.')

# 114
b114, v114 = barrow(P(16, 0, 800, 0, 10000), 0, 2); ck(v114, F(333536, 15))
S[114] = SOL([st('Avís.', r'Al dossier falta l’expressió dels ingressos $I(x)$, de manera que els apartats a) i b) no es poden resoldre amb les dades donades. El mètode seria: a) $B(x)=I(x)-G(x)$, resoldre $B\'(x)=0$ i comprovar que és un màxim; b) $E(x)=\dfrac{I(x)}{G(x)}$, resoldre $E\'(x)=0$ i comprovar que és un màxim.'),
              st('c)', r'$G(x)^2=(4x^2+100)^2=16x^4+800x^2+10000$: $$' + b114 + r'$$ $\approx22\,235{,}73$.')],
             r'c) $\frac{333536}{15}\approx22\,235{,}73$ (a) i b) necessiten $I(x)$, que no apareix a l’enunciat del dossier).')

# 115
b115, v115 = barrow(P(1, 2, 1), 2, 3); ck(v115, F(37, 3))
S[115] = SOL([st('a)', r'El primer tros, $\ln(x^2+a)$, està definit i és continu per a tot $x\le1$ si $x^2+a>0$, és a dir, si $a>0$. Els altres trossos són continus ($x+1\ne0$ per a $x>4$). '
                     r'En $x=1$: $\ln(1+a)=\displaystyle\lim_{x\to1^+}(x+1)^2=4\iff 1+a=e^4\iff a=e^4-1$. En $x=4$: $(4+1)^2=25=\displaystyle\lim_{x\to4^+}\left(5x+\frac{b}{x+1}\right)=20+\frac b5\iff b=25$.'),
              st('b)', r"Amb $a=54$, $b=25$. En $[-1,1]$: $f'(x)=\dfrac{2x}{x^2+54}$, mínim en $x=0$: $f(0)=\ln54\approx3{,}99$; $f(\pm1)=\ln55\approx4{,}01$. En $(1,4]$, $(x+1)^2$ creix de 4 (no assolit; en $x=1$ hi ha salt perquè $a\ne e^4-1$) a 25. En $(4,5]$: $f'(x)=5-\dfrac{25}{(x+1)^2}>0$, creix fins a $f(5)=25+\frac{25}{6}=\frac{175}{6}$ (contínua en $x=4$ perquè $b=25$). "
                     r'Màxim absolut $\frac{175}{6}\approx29{,}17$ en $x=5$; mínim absolut $\ln54\approx3{,}99$ en $x=0$.'),
              st('c)', r'En $[2,3]$, $f(x)=(x+1)^2>0$: $$' + b115 + '$$'),
              plot([(lambda x: math.log(x * x + 54), [-1, 1]), (lambda x: (x + 1) ** 2, [1.0001, 4]), (lambda x: 5 * x + 25 / (x + 1), [4, 5])], xr=(-1.3, 5.5), yr=(0, 31),
                   shade=[(lambda x: (x + 1) ** 2, None, 2, 3)], pts=[(0, math.log(54)), (5, 175 / 6), (1, 4, 'o')])],
             r'a) $a=e^4-1$, $b=25$; b) màxim absolut $\frac{175}{6}$ en $x=5$, mínim absolut $\ln54$ en $x=0$; c) $\frac{37}{3}$ u².')

# 116
s116, r116 = estudi(R(P(1, -2, 4), P(1, 0, -4)), lab=LAB4, xr=(-8, 10), yr=(-8, 10))
S[116] = SOL(s116, resum(r116))

# 117
C1 = P(-1, 8, 11, v='t'); ck(C1(4), 27)
S[117] = SOL([st('a)', r'$\displaystyle\lim_{t\to6^-}(-t^2+8t+a)=12+a=C(6)$ i $\displaystyle\lim_{t\to6^+}\frac{12t+89}{t+1}=\frac{161}{7}=23$. Contínua si $12+a=23\iff a=11$.'),
              st('b)', r"En $[0,6]$: $C'(t)=-2t+8=0\iff t=4$, amb $C'>0$ abans i $C'<0$ després: màxim $C(4)=-16+32+11=27$ ppm. En $(6,15]$ la concentració decreix (apartat c) des de 23, per tant és menor que 27: és el màxim absolut de les 15 hores."),
              st('c)', r"En $]6,15]$: $$C'(t)=\frac{12(t+1)-(12t+89)}{(t+1)^2}=\frac{-77}{(t+1)^2}<0$$ Sí, la concentració es redueix en tot moment."),
              st('d)', r'En $[0,6]$: $-t^2+8t+11>20\iff t^2-8t+9<0\iff 4-\sqrt7<t<4+\sqrt7$; amb $t\le6$: $(4-\sqrt7,\,6]$. En $(6,15]$: $\dfrac{12t+89}{t+1}>20\iff12t+89>20t+20\iff t<8{,}625$. L’alerta ha d’estar activada en $(4-\sqrt7;\ 8{,}625)$, és a dir, aproximadament entre 1,35 h i 8,63 h.'),
              plot([(lambda t: -t * t + 8 * t + 11, [0, 6]), (lambda t: (12 * t + 89) / (t + 1), [6, 15])], xr=(-0.5, 15.5), yr=(0, 30), ha=[20], pts=[(4, 27), (6, 23), (4 - math.sqrt(7), 20), (8.625, 20)], xl='t', yl='C')],
             r'a) $a=11$; b) $t=4$ h, 27 ppm, és el màxim absolut; c) sí; d) entre $t=4-\sqrt7\approx1{,}35$ h i $t=8{,}625$ h.')

# 118
f118 = R(P(1, 1, 4), P(1, 1)); ck(f118(F(1)), 3); ck(f118(F(5)), F(17, 3))
b118, v118 = barrow(P(1, 1, 4), 2, 3); ck(v118, F(77, 6))
S[118] = SOL([st('a)', r'$f(0)=B=4$ i $f(1)=A+\frac{B}{2}=A+2=3\Rightarrow A=1$. Per tant $f(x)=x+\dfrac{4}{x+1}$.'),
              st('b)', r'$x+\dfrac4{x+1}>4\iff x(x+1)+4>4(x+1)\iff x^2-3x>0\iff x(x-3)>0$. En $[0,5]$: $x\in(3,5]$.'),
              st('c)', r"$f'(x)=1-\dfrac{4}{(x+1)^2}=0\iff(x+1)^2=4\iff x=1$. Decreix en $[0,1)$ i creix en $(1,5]$."),
              st('d)', r'Mínim en $x=1$: $f(1)=3$ milions. Màxim en un extrem: $f(0)=4$ i $f(5)=5+\frac46=\frac{17}{3}\approx5{,}67$ milions, en $x=5$.'),
              st('e)', r'$g(x)=(x+1)f(x)=x(x+1)+4=x^2+x+4>0$: $$' + b118 + r'$$ u².'),
              plot([(lambda x: x + 4 / (x + 1), [0, 5])], xr=(-0.3, 5.3), yr=(0, 6.5), ha=[4], pts=[(1, 3), (5, 17 / 3), (3, 4)])],
             r'a) $A=1$, $B=4$; b) $(3,5]$; c) decreix en $[0,1)$, creix en $(1,5]$; d) mínim 3 M€ ($x=1$), màxim $\frac{17}{3}$ M€ ($x=5$); e) $\frac{77}{6}$ u².')
