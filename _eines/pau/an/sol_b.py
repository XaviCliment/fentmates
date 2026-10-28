# Solucions dels exercicis PAU d'anàlisi (Comunitat Valenciana), números 41-80 del dossier.
from anlib import *
from sol_a import opt, gq
S = {}
LAB5 = {'dom': 'a)', 'asi': 'b)', 'mon': 'c)', 'ext': 'd)', 'gra': 'e)'}

# gràfica de l'enunciat de l'exercici 62 (redibuixada a partir del dossier)
FIG62 = plot([(lambda x: 1 / (-2 - x), [-3.7, -2.001]), (lambda x: 1 / (x * (x + 2)), [-1.999, -0.001]),
              (lambda x: 1.5 * (x - 1) ** 2 / (x * (2 - x)), [0.001, 1.999]), (lambda x: 1 / (x - 2), [2.001, 3.7])],
             xr=(-3.7, 3.7), yr=(-2.6, 2.6), pts=[(-1, -1), (1, 0)])

# 41
y41 = R(P(5, 20, -25), P(1, 0, 7)); ck(y41(F(7)), F(45, 7))
S[41] = SOL([st('a)', r'$y<0\iff 5x^2+20x-25<0\iff x^2+4x-5<0\iff(x+5)(x-1)<0$. Com que $x\ge0$, hi ha pèrdues si $0\le x<1$: a partir del primer any ($x=1$) deixa de tenir pèrdues.'),
             st('b)', r"$$y'=\frac{(10x+20)(x^2+7)-(5x^2+20x-25)\,2x}{(x^2+7)^2}=\frac{-20x^2+120x+140}{(x^2+7)^2}=\frac{-20(x-7)(x+1)}{(x^2+7)^2}$$"
                     r"Per a $x\ge0$: $y'>0$ si $0\le x<7$ i $y'<0$ si $x>7$. Màxim en $x=7$: $y(7)=\dfrac{245+140-25}{56}=\dfrac{45}{7}\approx6{,}43$ milions d’euros."),
             st('c)', r'Comença amb pèrdues ($y(0)=-\frac{25}{7}\approx-3{,}57$), el resultat millora fins al màxim del 7è any i després disminueix acostant-se a $\displaystyle\lim_{x\to+\infty}y=\frac51=5$ milions d’euros.'),
             plot([(lambda x: y41(x), [0, 40])], xr=(-1, 40), yr=(-4.5, 7.5), ha=[5], pts=[(7, 45 / 7), (1, 0)])],
            r'a) A partir del 1r any; b) al 7è any, $\frac{45}{7}\approx6{,}43$ milions; c) a llarg termini, 5 milions d’euros.')

# 42
s42, r42 = estudi(R(P(1, 0, 0, 0), P(-1, 0, 1)), lab=LAB5, xr=(-5, 5), yr=(-8, 8))
S[42] = SOL(s42, resum(r42))

# 43
s43, r43 = estudi(R(P(1, 0, -6, 0)), lab=LAB5)
S[43] = SOL(s43, resum(r43))

# 44
c44a, _ = cont(-1, P(-1, 0), P(1, -1)); c44b, _ = cont(4, P(1, -1), P(1, -2, -6))
b44a, v44a = barrow(P(1, -1), 1, 4); b44b, v44b = barrow(P(1, -2, -6), 4, 5); a44 = ck(v44a + v44b, F(59, 6))
S[44] = SOL([st('a)', r'Els trossos són polinomis, continus en els seus intervals. Punts d’unió:'),
             r'<strong>En $x=-1$:</strong> ' + c44a, r'<strong>En $x=4$:</strong> ' + c44b,
             st('b)', r'En $[1,4)$, $f(x)=x-1\ge0$; en $[4,5]$, $x^2-2x-6$ només s’anul·la en $x=1\pm\sqrt7$ (fora de l’interval) i $f(4)=2>0$. $$A=' + b44a + '$$$$+' + b44b + r'$$ $A=\frac92+\frac{16}{3}=\frac{59}{6}\approx9{,}83$ u².'),
             plot([(lambda x: -x, [-2, -1]), (lambda x: x - 1, [-1, 3.9999]), (lambda x: x * x - 2 * x - 6, [4, 6])], xr=(-2.5, 6.5), yr=(-3, 12),
                  shade=[(lambda x: x - 1, None, 1, 4), (lambda x: x * x - 2 * x - 6, None, 4, 5)], pts=[(-1, 1, 'o'), (-1, -2), (4, 3, 'o'), (4, 2)])],
            r'a) Discontínua en $x=-1$ i en $x=4$ (salts); b) $A=\frac{59}{6}$ u²')

# 45
s45, r45 = estudi(R(P(1, 0), P(1, 0, 1)), lab=LAB5)
S[45] = SOL(s45, resum(r45))

# 46
B46 = P(F('-0.1'), 60, -2500); t46, x46, y46 = opt(B46, 'x', 'B', 'màxim'); ck(x46, 300); ck(y46, 6500)
S[46] = SOL([st('a)', r'$I(x)=80x$.'),
             st('b)', r'$B(x)=I(x)-C(x)=80x-0{,}1x^2-20x-2500=-0{,}1x^2+60x-2500$.'),
             st('c)', t46)],
            r'a) $I(x)=80x$; b) $B(x)=-0{,}1x^2+60x-2500$; c) 300 caixes, amb un benefici de 6500 €.')

# 47
s47, r47 = estudi(R(P(1, 0, 1), P(1, 0, -9)), lab=LAB5, yr=(-6, 7))
S[47] = SOL(s47, resum(r47))

# 48
p1, p2, p3 = P(F('-0.1'), 5, v='t'), P(F('0.05'), F('4.25'), v='t'), P(F('0.1'), -2, F('14.75'), v='t')
c48a, _ = cont(5, p1, p2, v='t'); c48b, _ = cont(10, p2, p3, v='t'); ck(p3(13), F('5.65'))
S[48] = SOL([st('a)', r'Els tres trossos són polinomis. Punts d’unió:'), r'<strong>En $t=5$:</strong> ' + c48a, r'<strong>En $t=10$:</strong> ' + c48b + ' La funció és contínua en $[0,13]$.',
             st('Monotonia.', r"$f'(t)=-0{,}1<0$ en $(0,5)$; $f'(t)=0{,}05>0$ en $(5,10)$; $f'(t)=0{,}2(t-10)>0$ en $(10,13)$. Decreix fins a $t=5$ i després creix." + taula_m([('[0,5)', '-'), ('(5,10)', '+'), ('(10,13]', '+')], "f'(t)", 'f(t)')),
             st('b) i c)', r'Candidats: $f(0)=5$, $f(5)=4{,}5$ (mínim) i $f(13)=4{,}75+0{,}1\cdot9=5{,}65$.'),
             plot([(lambda t: 5 - 0.1 * t, [0, 5]), (lambda t: 4.5 + 0.05 * (t - 5), [5, 10]), (lambda t: 4.75 + 0.1 * (t - 10) ** 2, [10, 13])], xr=(-0.5, 13.5), yr=(4, 6), pts=[(5, 4.5), (13, 5.65), (0, 5)], xl='t')],
            r'a) Contínua en $[0,13]$; b) màxima en $t=13$: 5,65 milions; c) mínima en $t=5$: 4,5 milions.')

# 49
I49 = P(-1000, 2000, 0, v='p'); t49, x49, y49 = opt(I49, 'p', 'I', 'màxim'); ck(x49, 1); ck(y49, 1000)
S[49] = SOL([st('a)', r'$I(p)=p\cdot n(p)=p(2000-1000p)=2000p-1000p^2$, amb $0\le p\le2$ (perquè $n(p)\ge0$).'),
             st('b)', t49)],
            r'a) $I(p)=2000p-1000p^2$; b) a 1 € el pastís, amb uns ingressos de 1000 € setmanals.')

# 50
c50a, _ = cont(2, R(P(2), P(1, 0)), P(1), fc='l'); c50b, _ = cont(3, P(1), P(-1, 6, -8), fc='l'); c50c, _ = cont(4, P(-1, 6, -8), P(0), fc='l')
b50a, v50a = barrow(P(1), 2, 3); b50b, v50b = barrow(P(-1, 6, -8), 3, 4); a50 = ck(v50a + v50b, F(5, 3))
S[50] = SOL([st('a)', r'Cada tros és continu en el seu interval ($\frac2x$ només falla en $x=0$, fora de $[1,2]$). Punts d’unió:'),
             r'<strong>En $x=2$:</strong> ' + c50a, r'<strong>En $x=3$:</strong> ' + c50b, r'<strong>En $x=4$:</strong> ' + c50c + ' Per tant $f$ és contínua en tot $[1,5]$.',
             st('b)', r'En $[3,4]$, $-x^2+6x-8=-(x-2)(x-4)\ge0$. $$A=' + b50a + '$$$$+' + b50b + r'$$ $A=1+\frac23=\frac53\approx1{,}67$ u².'),
             plot([(lambda x: 2 / x, [1, 2]), (lambda x: 1, [2, 3]), (lambda x: -x * x + 6 * x - 8, [3, 4]), (lambda x: 0, [4, 5])], xr=(0, 5.5), yr=(-0.5, 2.5),
                  shade=[(lambda x: 1, None, 2, 3), (lambda x: -x * x + 6 * x - 8, None, 3, 4)])],
            r'a) Contínua en tot $[1,5]$; b) $A=\frac53$ u²')

# 51
s51, r51 = estudi(R(P(1, 0, 0, 0), P(1, 0, -1)), lab={'asi': 'a)', 'mon': 'b)', 'ext': 'c)'}, graf=False)
S[51] = SOL(s51, resum(r51))

# 52
f52a, f52b = P(-1, -2, 3), P(1, -1)
c52, _ = cont(1, f52a, f52b); rows52 = [(0, f52a(0)), (1, f52b(1)), (3, f52b(3))]; e52, _, _ = extrems_abs(rows52)
b52a, v52a = barrow(f52a, 0, 1); b52b, v52b = barrow(f52b, 1, 3); a52 = ck(v52a + v52b, F(11, 3))
S[52] = SOL([st('a)', r'Els dos trossos són polinomis. En $x=1$: ' + c52 + r' Per tant $f$ és contínua en $[0,3]$.'),
             st('b)', r"En $(0,1)$, $f'(x)=-2x-2<0$ (decreix); en $(1,3)$, $f'(x)=1>0$ (creix). Candidats:" + taula_vals(rows52) + e52),
             st('c)', r'$f\ge0$ en $[0,3]$ ($-x^2-2x+3=-(x+3)(x-1)\ge0$ en $[0,1]$). $$A=' + b52a + '$$$$+' + b52b + r'$$ $A=\frac53+2=\frac{11}{3}$ u².'),
             plot([(lambda x: -x * x - 2 * x + 3, [0, 1]), (lambda x: x - 1, [1, 3])], xr=(-0.5, 3.5), yr=(-0.5, 3.5),
                  shade=[(lambda x: -x * x - 2 * x + 3, None, 0, 1), (lambda x: x - 1, None, 1, 3)], pts=[(0, 3), (1, 0), (3, 2)])],
            r'a) Contínua; b) màxim absolut 3 en $x=0$, mínim absolut 0 en $x=1$; c) $A=\frac{11}{3}$ u².')

# 53
s53, r53 = estudi(R(P(3, 2), P(1, 0, -1)), lab=LAB5, yr=(-8, 8))
S[53] = SOL(s53, resum(r53))

# 54
f54 = P(F(-1, 5000), F(120, 5000), 40); ck(f54(60), F('40.72')); ck(f54(300), F('29.2')); ck(f54(1), F('40.0238'))
S[54] = SOL([st('Interval:', r'$x\in[1,300]$ (es muny des de l’endemà del part).'),
             st('a)', r"$f'(x)=\dfrac{120-2x}{5000}=0\iff x=60$; $f'>0$ abans i $f'<0$ després: màxim. $f(60)=\dfrac{7200-3600}{5000}+40=40{,}72$ litres."),
             st('b)', r'El mínim absolut ha d’estar en un extrem de l’interval: $f(1)=40{,}0238$ i $f(300)=\dfrac{36000-90000}{5000}+40=29{,}2$.'),
             gq(f54, 1, 300, xr=(-10, 310), yr=(25, 42), pts=[(60, 40.72), (300, 29.2)])],
            r'a) El dia 60, amb 40,72 litres; b) el dia 300, amb 29,2 litres.')

# 55
S[55] = SOL([st('Observació.', r'Com que $f(\frac32)=\frac{13}{2}>3$ és un mínim i a la dreta la funció creix sempre, l’asímptota $y=3$ només pot ser-ho cap a $-\infty$: $\displaystyle\lim_{x\to-\infty}f(x)=3$ i $\displaystyle\lim_{x\to+\infty}f(x)=+\infty$.'),
             st('Branca esquerra.', r'Decreix des de $3$ (a $-\infty$), passa per $(0,0)$ i baixa a $-\infty$ en $x\to1^-$.'),
             st('Branca dreta.', r'Ve de $+\infty$ en $x\to1^+$, decreix fins al mínim $(\frac32,\frac{13}{2})$ i després creix sense límit.'),
             plot([(lambda x: 3 * x / (x - 1), [-8, 0.999]), (lambda x: 1 / (x - 1) + 4 * x - 1.5, [1.001, 4])], xr=(-8, 4), yr=(-6, 14), va=[1], ha=[3], pts=[(0, 0), (1.5, 6.5)])],
            r'Gràfica: asímptota vertical $x=1$, horitzontal $y=3$ (cap a $-\infty$), tall en $(0,0)$ i mínim $(\frac32,\frac{13}{2})$.')

# 56
I56 = P(-250, 2000, 86250); t56, x56, y56 = opt(I56, 'x', 'I', 'màxim'); ck(x56, 4); ck(y56, 90250)
S[56] = SOL([st('a)', r'$15\cdot5750=86\,250$ € mensuals.'),
             st('b)', r'Amb $x$ comercials més: $(15+x)$ comercials que ingressen $5750-250x$ cadascun. $$I(x)=(15+x)(5750-250x)=-250x^2+2000x+86250$$'),
             st('c) i d)', t56 + r' Total: $15+4=19$ comercials, cadascun amb $5750-1000=4750$ €.')],
            r'a) 86 250 €; b) $I(x)=-250x^2+2000x+86250$; c) 19 comercials; d) 90 250 €.')

# 57
B57 = R(P(36, 0), P(1, 0, 324)); ck(B57(F(18)) + 1, 2)
S[57] = SOL([st('Derivada:', r"$$B'(t)=\frac{36(t^2+324)-36t\cdot2t}{(t^2+324)^2}=\frac{36(324-t^2)}{(t^2+324)^2}=0\iff t=18$$"),
             st('a)', r"Per a $0\le t<18$, $B'>0$: el benefici creix des de $B(0)=1\,\%$; per a $18<t\le30$, $B'<0$: decreix fins a $B(30)=\frac{1080}{1224}+1\approx1{,}88\,\%$."),
             st('b)', r'Màxim en $t=18$ mesos: $B(18)=\dfrac{648}{648}+1=2\,\%$.'),
             st('c)', r'$\displaystyle\lim_{t\to+\infty}\left(\frac{36t}{t^2+324}+1\right)=0+1=1\,\%$.'),
             plot([(lambda t: 36 * t / (t * t + 324) + 1, [0, 60])], xr=(-2, 60), yr=(0, 2.4), ha=[1], pts=[(18, 2)], xl='t', yl='B')],
            r'a) Creix els 18 primers mesos i després decreix; b) 18 mesos, benefici del 2 %; c) 1 %.')

# 58
s58, r58 = estudi(R(P(1, 2, 1, 0, 0)), lab=LAB5, xr=(-2.2, 1.2), yr=(-0.1, 1.2))
S[58] = SOL(s58, resum(r58))

# 59
s59, r59 = estudi(R(P(-1, 4, -4), P(1, -4, 3)), lab=LAB5, xr=(-3, 7), yr=(-6, 6))
S[59] = SOL(s59, resum(r59))

# 60
c60a, _ = cont(0, P(1, 2), P(1, -2, 2)); c60b, _ = cont(3, P(1, -2, 2), P(3, -1))
f60 = P(1, -2, 2); rows60 = [(-2, F(0)), (0, F(2)), (1, f60(1)), (r'\frac52', f60(F(5, 2)))]; e60, _, _ = extrems_abs(rows60)
b60, v60 = barrow(f60, 1, 2); ck(v60, F(4, 3))
S[60] = SOL([st('a)', r'Els trossos són polinomis. Punts d’unió:'), r'<strong>En $x=0$:</strong> ' + c60a, r'<strong>En $x=3$:</strong> ' + c60b,
             st('b)', r"En $[-2,0)$, $f(x)=x+2$ creix. En $[0,\frac52]$, $f'(x)=2x-2=0\iff x=1$. Candidats:" + taula_vals(rows60) + e60),
             st('c)', r'En $[1,2]$, $f(x)=x^2-2x+2$: $$' + b60 + '$$'),
             plot([(lambda x: x + 2, [-2, 0]), (lambda x: x * x - 2 * x + 2, [0, 2.9999]), (lambda x: 3 * x - 1, [3, 5])], xr=(-2.5, 5.5), yr=(-1, 15), pts=[(3, 5, 'o'), (3, 8), (1, 1)])],
            r'a) Contínua excepte en $x=3$ (salt); b) màxim absolut $\frac{13}{4}$ en $x=\frac52$, mínim absolut 0 en $x=-2$; c) $\frac43$.')

# 61
B61 = P(-10, 6000, -250000); t61, x61, y61 = opt(B61, 'x', 'B', 'màxim'); ck(x61, 300); ck(y61, 650000)
S[61] = SOL([st('a)', r'$I(x)=8000x$.'),
             st('b)', r'$B(x)=I(x)-C(x)=8000x-10x^2-2000x-250000=-10x^2+6000x-250000$.'),
             st('c)', t61)],
            r'a) $I(x)=8000x$; b) $B(x)=-10x^2+6000x-250000$; c) 300 motocicletes, 650 000 €.')

# 62
b62, v62 = barrow(P(1, 2, -3, -4, 4), 0, 1); ck(v62, F(17, 10))
S[62] = SOL([st('a)', r'La funció no està definida en $x=-2$, $x=0$ ni $x=2$: $\mathrm{Dom}\,f=\mathbb R-\{-2,0,2\}$. Només talla els eixos en $(1,0)$ (no talla l’eix $OY$ perquè $0\notin\mathrm{Dom}\,f$).'),
             st('b)', r'Asímptotes verticals $x=-2$, $x=0$ i $x=2$; asímptota horitzontal $y=0$ (la gràfica s’hi acosta per tots dos costats).'),
             st('c)', r"$f'>0$ on la funció creix: $(-2,-1)\cup(1,2)$; $f'<0$ on decreix: $(-\infty,-2)\cup(-1,0)\cup(0,1)\cup(2,+\infty)$; $f'=0$ en els extrems relatius $x=-1$ (màxim) i $x=1$ (mínim)."),
             st('d)', r'$\displaystyle\lim_{x\to+\infty}f(x)=0$ i $\displaystyle\lim_{x\to0^+}f(x)=+\infty$.'),
             st('e)', '$$' + b62 + '$$')],
            r"a) $\mathbb R-\{-2,0,2\}$, tall $(1,0)$; b) AV $x=-2,0,2$, AH $y=0$; c) $f'>0$ en $(-2,-1)\cup(1,2)$, $f'=0$ en $x=\pm1$; d) $0$ i $+\infty$; e) $\frac{17}{10}$.")

# 63
c63a, _ = cont(3, P(-1, 15), P(1, -8, 26), fc='l'); c63b, _ = cont(6, P(1, -8, 26), P(2, 2), fc='l')
S[63] = SOL([st('a)', 'Els trossos són polinomis. Punts d’unió:'), r'<strong>En $x=3$:</strong> ' + c63a, r'<strong>En $x=6$:</strong> ' + c63b,
             st('b)', r"En $[0,3]$, $f$ decreix de $15$ a $12$. En $(3,6]$, $f'(x)=2x-8=0\iff x=4$, $f(4)=10$ (mínim relatiu), i $f(6)=14$ (prop de $x=3$ els valors s’acosten a 11). En $(6,8]$, $f$ creix fins a $f(8)=18$." +
                taula_vals([(0, 15), (3, 12), (4, 10), (6, 14), (8, 18)]) + r'Valor màxim: 18 € ($x=8$); valor mínim: 10 € ($x=4$).'),
             st('c)', r'Convé comprar quan l’acció val menys, a les 4 hores (10 €), i vendre al final, a les 8 hores (18 €): el benefici és de $18-10=8$ € per acció.'),
             plot([(lambda x: -x + 15, [0, 3]), (lambda x: x * x - 8 * x + 26, [3.0001, 6]), (lambda x: 2 * x + 2, [6, 8])], xr=(-0.5, 8.5), yr=(0, 20), pts=[(3, 12), (3, 11, 'o'), (4, 10), (8, 18)])],
            r'a) Discontínua en $x=3$ (salt); b) màxim 18 €, mínim 10 €; c) comprar a les 4 h i vendre a les 8 h: 8 € per acció.')

# 64
s64, r64 = estudi(R(P(1, 2, -3, -4, 4)), lab={'dom': 'a)', 'mon': 'b)', 'ext': 'c)'}, only=True, graf=False)
b64, v64 = barrow(P(1, 2, -3, -4, 4), -1, 1); ck(v64, F(32, 5))
S[64] = SOL([st('Expressió:', r'$f(x)=\left[(x-1)(x+2)\right]^2=(x^2+x-2)^2=x^4+2x^3-3x^2-4x+4$.')] + s64 +
            [st('d)', '$$' + b64 + '$$'), plot([lambda x: (x - 1) ** 2 * (x + 2) ** 2], xr=(-3.2, 2.2), yr=(-0.5, 8), pts=[(-2, 0), (-0.5, 81 / 16), (1, 0)])],
            r'a) $\mathbb R$; talls $(0,4)$, $(-2,0)$, $(1,0)$; b) creix en $(-2,-\frac12)\cup(1,+\infty)$; c) mínims $(-2,0)$, $(1,0)$, màxim $(-\frac12,\frac{81}{16})$; d) $\frac{32}{5}$.')

# 65
s65, r65 = estudi(R(P(1, -8, 16), P(1, -8, 15)), lab=LAB5, xr=(-1, 9), yr=(-4, 6))
S[65] = SOL(s65, resum(r65))

# 66
b66, v66 = barrow(P(1, -3, -8), 5, 6); ck(v66, F(35, 6))
S[66] = SOL([st('a)', r'$\frac ax$ és contínua en $[2,5)$ i el polinomi en $[5,7]$. En $x=5$: $\displaystyle\lim_{x\to5^-}\frac ax=\frac a5$ i $\displaystyle\lim_{x\to5^+}(x^2-3x-8)=2=f(5)$. Contínua si $\frac a5=2\iff a=10$.'),
             st('b)', r"Amb $a=15$: en $(2,5)$, $f'(x)=-\dfrac{15}{x^2}<0$ (decreix); en $(5,7)$, $f'(x)=2x-3>0$ (creix)." + taula_m([('[2,5)', '-'), ('(5,7]', '+')]) +
                r'Decreix en $[2,5)$ i creix en $(5,7]$ (en $x=5$ hi ha un salt: $f(5^-)=3$, $f(5)=2$).'),
             st('c)', r'En $[5,6]$, $f(x)=x^2-3x-8$: $$' + b66 + '$$')],
            r'a) $a=10$; b) decreix en $[2,5)$, creix en $(5,7]$; c) $\frac{35}{6}$.')

# 67
s67, r67 = estudi(R(P(2, 0, 2, -1), P(1, 0, -9, 0)), lab={'asi': 'a)'}, only=True, graf=False)
s67b, _ = estudi(R(P(1, 4, 4, 0, -8)), lab={'mon': 'b)', 'ext': 'c)'}, only=True, graf=False, name='g')
S[67] = SOL(s67 + s67b + [plot([lambda x: x ** 4 + 4 * x ** 3 + 4 * x ** 2 - 8], xr=(-3, 1), yr=(-9, -4), pts=[(-2, -8), (-1, -7), (0, -8)], yl='g')],
            r'a) AV $x=-3$, $x=0$, $x=3$; AH $y=2$; b) $g$ decreix en $(-\infty,-2)\cup(-1,0)$ i creix en $(-2,-1)\cup(0,+\infty)$; c) mínims $(-2,-8)$ i $(0,-8)$, màxim $(-1,-7)$.')

# 68
R68 = R(P(700, 0), P(4, 0, 9)); ck(R68(F(3)), F(140, 3)); ck(R68(F(3, 2)), F(175, 3))
e68, _ = eq2(4, -20, 9, 't')
S[68] = SOL([st('a)', r'$R(3)=\dfrac{2100}{45}=\dfrac{140}{3}\approx46{,}67$.'),
             st('b)', r"$$R'(t)=\frac{700(4t^2+9)-700t\cdot8t}{(4t^2+9)^2}=\frac{700(9-4t^2)}{(4t^2+9)^2}=0\iff t=\frac32$$ $R'>0$ en $[0,\frac32)$ (augmenta) i $R'<0$ en $(\frac32,6]$ (disminueix). Rendiment màxim: $R(\frac32)=\dfrac{1050}{18}=\dfrac{175}{3}\approx58{,}33$."),
             st('c)', r'$\dfrac{700t}{4t^2+9}=35\iff 20t=4t^2+9\iff$ ' + e68 + r'. Després del màxim ($t>\frac32$): $t=4{,}5$ h.'),
             plot([(lambda t: 700 * t / (4 * t * t + 9), [0, 6])], xr=(-0.3, 6.3), pts=[(1.5, 175 / 3), (4.5, 35)], xl='t', yl='R')],
            r'a) $\approx46{,}67$; b) augmenta fins a $t=1{,}5$ h i després disminueix; màxim $\frac{175}{3}\approx58{,}33$; c) a les 4,5 hores.')

# 69
c69, _ = cont(1, P(1, 0, 2), R(P(6), P(1, 0, 1)), fc='l')
b69, v69 = barrow(P(1, 0, 2), -1, 1); ck(v69, F(14, 3))
S[69] = SOL([st('a)', r'$x^2+2$ és contínua i $\dfrac{6}{x^2+1}$ també (el denominador no s’anul·la). En $x=1$: ' + c69 + r' Contínua en $\mathbb R$.'),
             st('b)', r"Si $x<1$: $f'(x)=2x$, negativa en $(-\infty,0)$ i positiva en $(0,1)$. Si $x>1$: $f'(x)=\dfrac{-12x}{(x^2+1)^2}<0$." +
                taula_m([('(-\\infty,0)', '-'), ('(0,1)', '+'), ('(1,+\\infty)', '-')]) + r'Mínim local en $(0,2)$ i màxim local en $(1,3)$ (la funció és contínua i passa de créixer a decréixer).'),
             st('c)', r'En $[-1,1]$, $f(x)=x^2+2>0$: $$A=' + b69 + r'$$'),
             plot([(lambda x: x * x + 2, [-3, 1]), (lambda x: 6 / (x * x + 1), [1, 6])], xr=(-3, 6), yr=(-0.5, 7), shade=[(lambda x: x * x + 2, None, -1, 1)], pts=[(0, 2), (1, 3)])],
            r'a) Contínua en $\mathbb R$; b) mínim $(0,2)$, màxim $(1,3)$; c) $A=\frac{14}{3}$ u².')

# 70
c70, _ = cont(5, P(F('-1.1'), F('15.5')), R(P(5, 45), P(1, 2)), fc='l')
S[70] = SOL([st('a)', r'El primer tros és un polinomi i el segon és continu per a $x>5$ (només falla en $x=-2$). En $x=5$: ' + c70 + r' Contínua en $[0,+\infty)$.'),
             st('b)', r"En $(0,5)$: $f'(x)=-1{,}1<0$. Per a $x>5$: $$f'(x)=\frac{5(x+2)-(5x+45)}{(x+2)^2}=\frac{-35}{(x+2)^2}<0$$ La funció és contínua i decreixent en tot el domini; per tant, si $x>5$, $f(x)<f(5)=10$ fotografies per minut."),
             st('c)', r'$\displaystyle\lim_{x\to+\infty}\frac{5x+45}{x+2}=5$ i $f(x)-5=\dfrac{35}{x+2}>0$: la funció s’acosta a 5 però sempre és major. Sí, és cert: mai revelarà menys de 5 fotografies per minut.'),
             plot([(lambda x: 15.5 - 1.1 * x, [0, 5]), (lambda x: (5 * x + 45) / (x + 2), [5, 40])], xr=(-1, 40), yr=(0, 17), ha=[5], pts=[(5, 10)])],
            r'a) Contínua; b) decreixent; per a $x>5$, $f(x)<10$; c) sí: $y=5$ és una asímptota horitzontal i $f(x)>5$.')

# 71
R71 = P(F('-0.01'), F('0.1'), 1); t71, x71, y71 = opt(R71, 'x', 'R', 'màxim'); ck(x71, 5); ck(y71, F('1.25'))
S[71] = SOL([st('a)', t71 + r' Cal invertir 5 milers d’euros (5000 €) i la rendibilitat màxima és de 1250 €.'),
             st('b)', r"$$R_m(x)=\frac{R(x)}{x}=-0{,}01x+0{,}1+\frac1x,\qquad R_m'(x)=-0{,}01-\frac1{x^2}<0$$ La rendibilitat mitjana és sempre decreixent: com més s’inverteix, menor és la rendibilitat per cada euro invertit."),
             plot([(lambda x: -0.01 * x + 0.1 + 1 / x, [0.15, 20])], xr=(-0.5, 20), yr=(-0.2, 2), xl='x', yl='R_m')],
            r'a) 5000 €, rendibilitat màxima de 1250 €; b) $R_m(x)=-0{,}01x+0{,}1+\frac1x$, sempre decreixent.')

# 72
s72, r72 = estudi(R(P(1, 0, 0), P(-1, 4)), lab=LAB5, xr=(-10, 16), yr=(-30, 20))
S[72] = SOL(s72, resum(r72))

# 73
f73 = P(F(-1, 2), 4, 1); rows73 = [(0, F(3)), (2, F(7)), (4, f73(4)), (8, f73(8))]; e73, _, _ = extrems_abs(rows73)
b73, v73 = barrow(f73, 5, 7); ck(v73, F(41, 3))
S[73] = SOL([st('a)', r"En $[0,2)$, $f(x)=2x+3$ creix. En $[2,8]$, $f'(x)=-x+4=0\iff x=4$, amb $f'>0$ abans i $f'<0$ després. Com que $f$ és contínua en $[0,8]$, els extrems absoluts estan entre aquests candidats:" + taula_vals(rows73) + e73),
             st('b)', '$$' + b73 + '$$'),
             plot([(lambda x: 2 * x + 3, [0, 2]), (lambda x: -x * x / 2 + 4 * x + 1, [2, 8])], xr=(-0.5, 8.5), yr=(-0.5, 10), pts=[(0, 3), (4, 9), (8, 1)])],
            r'a) Màxim absolut 9 en $x=4$; mínim absolut 1 en $x=8$; b) $\frac{41}{3}$.')

# 74
s74, r74 = estudi(R(P(1, 0, 0), P(1, 0, -1)), lab=LAB5, xr=(-4, 4), yr=(-5, 6))
S[74] = SOL(s74, resum(r74))

# 75
s75, r75 = estudi(R(P(1, -2, 1, 0)), lab={'dom': 'a)', 'mon': 'b)', 'ext': 'c)', 'gra': 'd)'}, asim=False, xr=(-0.8, 2.2), yr=(-0.6, 1.2))
S[75] = SOL(s75 + [st('e)', r'$g(x)=f(x-2)$: la gràfica de $g$ és la de $f$ desplaçada 2 unitats a la dreta. Per tant $g$ té un màxim local en $x=\frac13+2=\frac73$ (valor $\frac{4}{27}$) i un mínim local en $x=1+2=3$ (valor $0$).')],
            r'b) creix en $(-\infty,\frac13)\cup(1,+\infty)$; c) màxim $(\frac13,\frac4{27})$, mínim $(1,0)$; e) $g$: màxim en $x=\frac73$ i mínim en $x=3$.')

# 76
p76 = P(F('-0.01'), F('0.09'), F('0.1')); r76 = R(P(F('1.26'), F('0.02'), F('-0.02')), P(1, 0, -1))
c76, _ = cont(8, p76, r76, fc='l'); t76, x76, y76 = opt(p76, 'x', 'B', 'màxim'); ck(x76, F('4.5')); ck(y76, F('0.3025'))
S[76] = SOL([st('a)', r'El primer tros és un polinomi; el segon només falla en $x=\pm1$, fora de $x>8$. En $x=8$: ' + c76 + r' $B$ és contínua en $(0,+\infty)$.'),
             st('b)', r"En $(0,8)$: $B'(x)=-0{,}02x+0{,}09=0\iff x=4{,}5$. Per a $x>8$: $$B'(x)=1{,}26\,\frac{(x^2-1)-x\cdot2x}{(x^2-1)^2}=\frac{-1{,}26(x^2+1)}{(x^2-1)^2}<0$$" +
                taula_m([('(0,\\,4{,}5)', '+'), ('(4{,}5,\\,8)', '-'), ('(8,+\\infty)', '-')], "B'(x)", 'B(x)') + r'Creix en $(0;4{,}5)$ i decreix en $(4{,}5;+\infty)$.'),
             st('c)', t76 + r' Cal invertir 4500 € i el benefici màxim és de 302,50 €.'),
             st('d)', r'$\displaystyle\lim_{x\to+\infty}B(x)=0+0{,}02=0{,}02$ milers d’euros. Com que $B$ decreix i s’acosta a 0,02 sense arribar-hi, el benefici sempre serà major de 20 €.'),
             plot([(lambda x: -0.01 * x * x + 0.09 * x + 0.1, [0, 8]), (lambda x: 1.26 * x / (x * x - 1) + 0.02, [8, 40])], xr=(-1, 40), yr=(0, 0.35), ha=[0.02], pts=[(4.5, 0.3025), (8, 0.18)])],
            r'a) Contínua; b) creix en $(0;4{,}5)$, decreix en $(4{,}5;+\infty)$; c) 4500 €, amb 302,50 €; d) com a mínim, 20 €.')

# 77
f77 = R(P(F('35.7'), F('71.4')), P(1, 0, 21)); ck(f77(F(3)), F('5.95')); ck(f77(F(0)), F('3.4')); ck(f77(F(8)), F('4.2'))
S[77] = SOL([st('Derivada:', r"$$f'(x)=35{,}7\,\frac{(x^2+21)-(x+2)\,2x}{(x^2+21)^2}=35{,}7\,\frac{-x^2-4x+21}{(x^2+21)^2}=\frac{-35{,}7(x+7)(x-3)}{(x^2+21)^2}$$ En $[0,8]$: $f'>0$ si $x<3$ i $f'<0$ si $x>3$."),
             st('Candidats:', taula_vals([(0, F('3.4')), (3, F('5.95')), (8, F('4.2'))])),
             st('a)', r'Màxim de 5,95 € a les 3 hores.'),
             st('b)', r'Mínim de 3,40 € a l’obertura ($x=0$).'),
             st('c)', r'Compra: $20\cdot3{,}4=68$ €; venda: $20\cdot4{,}2=84$ €. Guanys de $84-68=16$ €.'),
             plot([(lambda x: f77(x), [0, 8])], xr=(-0.3, 8.3), yr=(0, 6.5), pts=[(0, 3.4), (3, 5.95), (8, 4.2)])],
            r'a) 5,95 € en $x=3$ h; b) 3,40 € en $x=0$; c) guanys de 16 €.')

# 78
S[78] = SOL([st('a)', r'$\displaystyle\lim_{x\to3^-}(x^3-3x-20)=27-9-20=-2=f(3)$ i $\displaystyle\lim_{x\to3^+}\frac{2}{a-x}=\frac{2}{a-3}$. Contínua si $\dfrac{2}{a-3}=-2\iff a-3=-1\iff a=2$.'),
             st('b)', r"Amb $a=0$, per a $x>3$ $f(x)=-\dfrac2x$. Si $x<3$: $f'(x)=3x^2-3=3(x+1)(x-1)$; si $x>3$: $f'(x)=\dfrac{2}{x^2}>0$." +
                taula_m([('(-\\infty,-1)', '+'), ('(-1,1)', '-'), ('(1,3)', '+'), ('(3,+\\infty)', '+')]) +
                r'Creix en $(-\infty,-1)\cup(1,3)\cup(3,+\infty)$ i decreix en $(-1,1)$. (En $x=3$ hi ha un salt: $f(3)=-2$ i $f(3^+)=-\frac23$.)'),
             st('c)', r'Màxim local en $(-1,\,-18)$ i mínim local en $(1,\,-22)$. En $x=3$ no hi ha extrem: a l’esquerra els valors són menors que $f(3)=-2$ i a la dreta, majors.'),
             plot([(lambda x: x ** 3 - 3 * x - 20, [-4, 3]), (lambda x: -2 / x, [3, 10])], xr=(-4, 10), yr=(-30, 3), pts=[(-1, -18), (1, -22), (3, -2), (3, -2 / 3, 'o')])],
            r'a) $a=2$; b) creix en $(-\infty,-1)\cup(1,3)\cup(3,+\infty)$, decreix en $(-1,1)$; c) màxim $(-1,-18)$, mínim $(1,-22)$.')
ck(P(1, 0, -3, -20)(-1), -18); ck(P(1, 0, -3, -20)(1), -22)

# 79
s79, r79 = estudi(R(P(1, -1), P(1, -4, 4)), lab={'dom': 'a)', 'asi': 'b)', 'ext': 'c)', 'gra': 'd)'}, dt='(x-2)^2', xr=(-4, 8), yr=(-2, 6))
S[79] = SOL(s79, resum(r79))

# 80
f80 = R(P(10, 21), P(1, 3)); ck(f80(F(6)), 9); ck(f80(F(87)), F('9.9'))
S[80] = SOL([st('a)', r'$f(6)=\dfrac{81}{9}=9$ km² i $f(87)=\dfrac{891}{90}=9{,}9$ km².'),
             st('b)', r"$f'(t)=\dfrac{10(t+3)-(10t+21)}{(t+3)^2}=\dfrac{9}{(t+3)^2}>0$: la superfície desglaçada creix sempre."),
             st('c)', r'$g(t)=10-\dfrac{9}{t+3}=\dfrac{10(t+3)-9}{t+3}=\dfrac{10t+21}{t+3}=f(t)$: són la mateixa funció.'),
             st('d)', r'$\displaystyle\lim_{t\to+\infty}\frac{10t+21}{t+3}=10$ i $f(t)<10$ sempre: el desglaç creix però mai arribarà als 10 km².'),
             plot([(lambda t: (10 * t + 21) / (t + 3), [0, 100])], xr=(-3, 100), yr=(0, 11), ha=[10], pts=[(6, 9), (87, 9.9)], xl='t')],
            r'a) 9 km² i 9,9 km²; b) creix; c) són iguals; d) sí, 10 km².')
