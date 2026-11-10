# Solucions dels exercicis PAU d'anàlisi de 2n Batx MII (recull de l'IES Vermellar), números 1-45.
# Cada resultat es comprova amb sympy (ok, okn, der, pri).
from mlib import *  # noqa: F401,F403

S = {}

# 1
ok(I(x + 1, 0, sqrt(10) - 1), R(9, 2)); ok(I(x + 1, 0, 2), 4)
S[1] = SOL([st('a)', r'Una primitiva de $x+1$ és $\dfrac{(x+1)^2}{2}$: $$\int_0^{a-1}(x+1)\,dx=\left[\frac{(x+1)^2}{2}\right]_0^{a-1}=\frac{a^2}{2}-\frac12=\frac92\iff a^2=10\iff a=\pm\sqrt{10}$$ El valor positiu és $a=\sqrt{10}$.'),
            st('b)', r'En $[0,2]$ la recta $y=x+1$ és positiva (talla l’eix en $x=-1$), així que l’àrea és directament la integral: $$A=\int_0^2(x+1)\,dx=\left[\frac{x^2}{2}+x\right]_0^2=2+2=4\ \text{u}^2$$'),
            gr([x + 1], xr=(-1.5, 3), yr=(-1, 4), shade=[(x + 1, None, 0, 2)])],
           r'a) $a=\sqrt{10}$; b) $A=\displaystyle\int_0^2(x+1)\,dx=4$ u².')

# 2
f2, g2 = asin(x / sqrt(1 + x**2)), acos(1 / sqrt(1 + x**2))
okn(diff(f2, x).subs(x, R(3, 2)), 1 / (1 + R(9, 4))); okn(diff(g2, x).subs(x, R(3, 2)), 1 / (1 + R(9, 4)))
ok(f2.subs(x, 0), 0); ok(g2.subs(x, 0), 0)
S[2] = SOL([st('Derivada de $f$.', r'Siga $u=\dfrac{x}{\sqrt{1+x^2}}$. $$u^{\prime}=\frac{\sqrt{1+x^2}-x\cdot\frac{x}{\sqrt{1+x^2}}}{1+x^2}=\frac{1}{(1+x^2)\sqrt{1+x^2}},\qquad \sqrt{1-u^2}=\sqrt{\frac{1}{1+x^2}}=\frac{1}{\sqrt{1+x^2}}$$ $$f^{\prime}(x)=\frac{u^{\prime}}{\sqrt{1-u^2}}=\frac{1}{1+x^2}$$'),
            st('Derivada de $g$.', r'Siga $v=(1+x^2)^{-1/2}$: $v^{\prime}=-\dfrac{x}{(1+x^2)\sqrt{1+x^2}}$ i, com que $x\ge0$, $\sqrt{1-v^2}=\sqrt{\dfrac{x^2}{1+x^2}}=\dfrac{x}{\sqrt{1+x^2}}$. $$g^{\prime}(x)=\frac{-v^{\prime}}{\sqrt{1-v^2}}=\frac{x}{(1+x^2)\sqrt{1+x^2}}\cdot\frac{\sqrt{1+x^2}}{x}=\frac{1}{1+x^2}\quad(x>0)$$'),
            st('Comparació.', r'$f^{\prime}(x)=g^{\prime}(x)$ per a tot $x>0$, per tant $(f-g)^{\prime}=0$ i $f-g$ és constant en $[0,+\infty)$ (totes dues són contínues en 0). Aquesta constant és $f(0)-g(0)=\arcsin 0-\arccos 1=0-0=0$.')],
           r'$f^{\prime}(x)=g^{\prime}(x)=\dfrac{1}{1+x^2}$; la diferència $f(x)-g(x)$ és constant i val 0: $f(x)=g(x)$ per a $x\ge0$ (de fet, totes dues són $\arctan x$).')

# 3
f3 = x**3 + 6 * x**2 - 6
ok(diff(f3, x).subs(x, -4), 0); ok(diff(f3, x).subs(x, 0), 0); ok(f3.subs(x, 1), 1)
S[3] = SOL([st('Condicions.', r"$f'(x)=3x^2+2ax+b$. Els extrems relatius anul·len la derivada: $$f'(0)=b=0,\qquad f'(-4)=48-8a+b=0\Rightarrow a=6$$ I $f(1)=1+a+b+c=1\Rightarrow 7+c=1\Rightarrow c=-6$."),
            st('Comprovació.', r"$f''(x)=6x+12$: $f''(-4)=-12<0$ (màxim) i $f''(0)=12>0$ (mínim).")],
           r'$a=6$, $b=0$, $c=-6$: $f(x)=x^3+6x^2-6$.')

# 4
ok(I(2 / (1 + x**2) - x**2, -1, 1), pi - R(2, 3))
S[4] = SOL([st('Punts de tall.', r'$x^2=\dfrac{2}{1+x^2}\iff x^4+x^2-2=0\iff (x^2+2)(x^2-1)=0\iff x=\pm1$.'),
            st('Posició.', r'En $x=0$: $\dfrac{2}{1+0}=2>0$, així que en $(-1,1)$ la corba $y=\dfrac{2}{1+x^2}$ està per damunt de la paràbola.'),
            st('Àrea.', r'$$A=\int_{-1}^{1}\left(\frac{2}{1+x^2}-x^2\right)dx=\left[2\arctan x-\frac{x^3}{3}\right]_{-1}^{1}=\left(\frac{\pi}{2}-\frac13\right)-\left(-\frac{\pi}{2}+\frac13\right)=\pi-\frac23$$'),
            gr([x**2, 2 / (1 + x**2)], xr=(-2.5, 2.5), yr=(-0.5, 3), shade=[(2 / (1 + x**2), x**2, -1, 1)], pts=[(-1, 1), (1, 1)])],
           r'$A=\pi-\dfrac23\approx %s$ u².' % dd(pi - R(2, 3)))

# 5
ok(2 * I(sin(x) - 2 * x / pi, 0, pi / 2), 2 - pi / 2)
pri(2 / pi * x * sin(x), 2 / pi * (sin(x) - x * cos(x)))
S[5] = SOL([st('Talls.', r'$\sin x=\frac{2}{\pi}x$ en $x=0$ i $x=\pm\frac{\pi}{2}$ ($\sin\frac{\pi}{2}=1=\frac{2}{\pi}\cdot\frac{\pi}{2}$). En $(0,\frac{\pi}{2})$ el sinus està per damunt de la recta (per exemple, en $\frac{\pi}{6}$: $\frac12>\frac13$), i en $(-\frac{\pi}{2},0)$ per davall (les dues funcions són senars).'),
            gr([sin(x), 2 * x / pi], xr=(-1.9, 1.9), yr=(-1.4, 1.4), shade=[(sin(x), 2 * x / pi, -math.pi / 2, math.pi / 2)], pts=[(-math.pi / 2, -1), (0, 0), (math.pi / 2, 1)]),
            st('a) Àrea.', r'Per simetria, $$A=2\int_0^{\pi/2}\left(\sin x-\frac{2}{\pi}x\right)dx=2\left[-\cos x-\frac{x^2}{\pi}\right]_0^{\pi/2}=2\left[\left(0-\frac{\pi}{4}\right)-(-1)\right]=2-\frac{\pi}{2}$$'),
            st('b) Per parts.', r'$u=x$, $dv=\sin x\,dx$ $\Rightarrow$ $du=dx$, $v=-\cos x$: $$\int\frac{2}{\pi}x\sin x\,dx=\frac{2}{\pi}\left(-x\cos x+\int\cos x\,dx\right)=\frac{2}{\pi}\left(\sin x-x\cos x\right)+C$$')],
           r'a) $A=2-\dfrac{\pi}{2}\approx %s$ u²; b) $\dfrac{2}{\pi}(\sin x-x\cos x)+C$.' % dd(2 - pi / 2))

# 6
f6 = R(1, 4) * x**2 * (900 - 30 * x)
ok(solve(diff(f6, x), x), [0, 20]); ok(sqrt(f6.subs(x, 20)), 100 * sqrt(3))
S[6] = SOL([st('a) Costats i altura.', r'Si els costats iguals fan $y$: $x+2y=60\Rightarrow y=30-\frac{x}{2}$. L’altura sobre el costat $x$ divideix el triangle en dos triangles rectangles: $$h=\sqrt{y^2-\frac{x^2}{4}}=\sqrt{\left(30-\frac x2\right)^2-\frac{x^2}{4}}=\sqrt{900-30x}$$ $$A(x)=\frac{x}{2}\sqrt{900-30x},\qquad f(x)=A(x)^2=\frac{x^2}{4}(900-30x)=225x^2-\frac{15}{2}x^3$$ Per la desigualtat triangular, $x<2y=60-x$, és a dir, $0<x<30$.'),
            st('b) Màxim.', r"$f'(x)=450x-\frac{45}{2}x^2=\frac{45}{2}x(20-x)=0\Rightarrow x=20$ (en $(0,30)$). $f'>0$ en $(0,20)$ i $f'<0$ en $(20,30)$: màxim. Aleshores $y=20$: el triangle és equilàter, amb $A=10\sqrt{300}=100\sqrt3$ cm².")],
           r'$A(x)=\frac{x}{2}\sqrt{900-30x}$, $f(x)=225x^2-\frac{15}{2}x^3$, $0<x<30$; el màxim és en $x=20$ cm (triangle equilàter).')

# 7
f7 = 200 * x + 80000 / x
ok(solve(diff(f7, x), x), [-20, 20]); ok(f7.subs(x, 20), 8000)
S[7] = SOL([st('a) Funció.', r'Si un costat fa $x$, l’altre fa $\dfrac{400}{x}$. El perímetre és $2x+\dfrac{800}{x}$ i el cost: $$f(x)=100\left(2x+\frac{800}{x}\right)=200x+\frac{80000}{x},\qquad x>0$$'),
            st('b) Mínim.', r"$f'(x)=200-\dfrac{80000}{x^2}=0\iff x^2=400\iff x=20$. $f''(x)=\dfrac{160000}{x^3}>0$: mínim. El rectangle és un quadrat de 20 m de costat i la tanca costa $f(20)=4000+4000=8000$ €.")],
           r'$f(x)=200x+\dfrac{80000}{x}$, $x>0$; el mínim és en $x=20$ m (quadrat de 20 m), amb un cost de 8000 €.')

# 8
ok(I(4 - x**2, -2, 2), R(32, 3)); ok(pi * I((x**2 - 4)**2, -2, 2), R(512, 15) * pi)
S[8] = SOL([st('a) Superfície.', r'$y=x^2-4$ és una paràbola amb vèrtex $(0,-4)$ que talla l’eix en $x=\pm2$; en $[-2,2]$ és negativa, així que $$A=\int_{-2}^{2}\big(0-(x^2-4)\big)dx=\left[4x-\frac{x^3}{3}\right]_{-2}^{2}=\frac{16}{3}+\frac{16}{3}=\frac{32}{3}\ \text{u}^2$$'),
            gr([x**2 - 4], xr=(-3, 3), yr=(-5, 2), shade=[(x**2 - 4, None, -2, 2)], pts=[(-2, 0), (2, 0), (0, -4)]),
            st('b) Volum de revolució.', r'En girar al voltant de l’eix OX, cada secció perpendicular és un cercle de radi $|f(x)|$; sumant aquests discos: $$V=\pi\int_{-2}^{2}(x^2-4)^2\,dx=\pi\int_{-2}^{2}(x^4-8x^2+16)\,dx=\pi\left[\frac{x^5}{5}-\frac{8x^3}{3}+16x\right]_{-2}^{2}=\frac{512\pi}{15}\ \text{u}^3$$')],
           r'a) $A=\displaystyle\int_{-2}^{2}(4-x^2)\,dx=\frac{32}{3}$ u²; b) $V=\dfrac{512\pi}{15}\approx %s$ u³.' % dd(512 * pi / 15))

# 9
y9 = 1 / (1 + x**2); m9 = diff(y9, x)
ok(simplify(diff(m9, x) - (6 * x**2 - 2) / (1 + x**2)**3), 0); ok(m9.subs(x, -1 / sqrt(3)), 3 * sqrt(3) / 8)
S[9] = SOL([st('Funció pendent.', r"El pendent de la tangent en $x$ és $m(x)=y'=-\dfrac{2x}{(1+x^2)^2}$. Volem el màxim d’aquesta funció."),
            st('Derivada.', r"$$m'(x)=\frac{-2(1+x^2)^2+2x\cdot2(1+x^2)\cdot2x}{(1+x^2)^4}=\frac{6x^2-2}{(1+x^2)^3}=0\iff x=\pm\frac{1}{\sqrt3}$$" +
               taula_m([(r'(-\infty,-\frac{\sqrt3}{3})', '+'), (r'(-\frac{\sqrt3}{3},\frac{\sqrt3}{3})', '-'), (r'(\frac{\sqrt3}{3},+\infty)', '+')], "m'(x)", 'm(x)')),
            st('Màxim absolut.', r"En $x=-\frac{\sqrt3}{3}$ hi ha un màxim relatiu: $m\left(-\frac{\sqrt3}{3}\right)=\dfrac{2/\sqrt3}{(4/3)^2}=\dfrac{3\sqrt3}{8}$. Com que $m(x)\to0$ quan $x\to\pm\infty$ i el pendent és positiu només per a $x<0$, és el màxim absolut. El punt és $\left(-\frac{\sqrt3}{3},\,\frac34\right)$.")],
           r'El pendent màxim s’obté en el punt $\left(-\frac{\sqrt3}{3},\frac34\right)$ i val $\dfrac{3\sqrt3}{8}\approx %s$.' % dd(3 * sqrt(3) / 8))

# 10
ok(I(x - x**2 / 4, 0, 4), R(8, 3))
S[10] = SOL([st('Talls amb el riu.', r'$\dfrac{x^2}{4}-x=0\iff x(x-4)=0\iff x=0,\ x=4$. Entre 0 i 4 la paràbola està per davall de l’eix.'),
             st('Àrea de la pineda.', r'$$A=\int_0^4\left(x-\frac{x^2}{4}\right)dx=\left[\frac{x^2}{2}-\frac{x^3}{12}\right]_0^4=8-\frac{16}{3}=\frac83\ \text{km}^2$$'),
             gr([x**2 / 4 - x], xr=(-1, 5), yr=(-1.6, 1.2), shade=[(x**2 / 4 - x, None, 0, 4)], pts=[(0, 0), (4, 0)]),
             st('Preu.', r'$1\ \text{km}^2=100$ ha, per tant $\frac83$ km² $=\frac{800}{3}$ ha, i el preu és $\frac{800}{3}\cdot60=16000$ €.')],
            r'La pineda fa $\frac83$ km² $=\frac{800}{3}\approx266{,}67$ ha i val 16000 €.')

# 11
pri(-16 / (x**2 - 2 * x - 15), 2 * ln(x + 3) - 2 * ln(5 - x)); ok(I(-16 / (x**2 - 2 * x - 15), 0, 3), ln(25))
S[11] = SOL([st('Fraccions simples.', r'$x^2-2x-15=(x-5)(x+3)$. $$\frac{-16}{(x-5)(x+3)}=\frac{A}{x-5}+\frac{B}{x+3}\Rightarrow -16=A(x+3)+B(x-5)$$ $x=5$: $A=-2$; $x=-3$: $B=2$. Per tant $$\int\frac{-16}{x^2-2x-15}\,dx=-2\ln|x-5|+2\ln|x+3|+C=2\ln\left|\frac{x+3}{x-5}\right|+C$$'),
             st('Interval.', r'L’integrand té asímptotes en $x=-3$ i $x=5$; perquè la integral entre 0 i $z$ tinga sentit, $z\in(-3,5)$. En aquest interval l’integrand és positiu, de manera que cal $z>0$.'),
             st('Equació.', r'$$\int_0^z=2\ln\frac{z+3}{5-z}-2\ln\frac35=2\ln\frac{5(z+3)}{3(5-z)}=\ln25\iff\frac{5(z+3)}{3(5-z)}=5\iff z+3=15-3z\iff z=3$$')],
            r'$z=3$.')

# 12
T12 = x / 5 + sqrt((6 - x)**2 + 9) / 3
ok(solve(diff(T12, x), x), [R(15, 4)]); ok(T12.subs(x, R(15, 4)), 2)
S[12] = SOL([st('Geometria.', r'Siga $H$ el punt de la costa més pròxim a la boia $B$ ($BH=3$). Aleshores $NH=\sqrt{(3\sqrt5)^2-3^2}=\sqrt{36}=6$ km. Si el nadador camina $x$ km cap a $H$ ($0\le x\le6$) i després neda en línia recta fins a la boia, neda $\sqrt{(6-x)^2+9}$ km.'),
             st('Temps.', r'$$T(x)=\frac{x}{5}+\frac{\sqrt{(6-x)^2+9}}{3}$$'),
             st('Derivada.', r"$$T'(x)=\frac15-\frac{6-x}{3\sqrt{(6-x)^2+9}}=0\iff 3\sqrt{(6-x)^2+9}=5(6-x)\iff 16(6-x)^2=81\iff 6-x=\frac94\iff x=\frac{15}{4}$$"),
             st('Comparació.', r'$T(0)=\sqrt5\approx2{,}24$ h, $T\!\left(\frac{15}{4}\right)=\frac34+\frac{15/4}{3}=2$ h, $T(6)=\frac65+1=2{,}2$ h. El mínim és en $x=3{,}75$ km, que es recorren caminant en $\frac{3{,}75}{5}=0{,}75$ h.')],
            r'Ha de caminar 3,75 km, és a dir, durant 0,75 h = 45 minuts (el temps total és de 2 h).')

# 13
m13 = R(3, 2); f13 = x**2 + m13 * x
ok(diff(f13, x).subs(x, R(-3, 4)), 0); ok(I(diff(f13, x) - f13, -1, R(3, 2)), R(125, 48))
S[13] = SOL([st('a)', r"$f'(x)=2x+m=0$ en $x=-\frac34$ $\Rightarrow m=\frac32$. Com que $f''(x)=2>0$, és un mínim."),
             st('b) Talls.', r"$f(x)=x^2+\frac32x$, $f'(x)=2x+\frac32$. $$x^2+\frac32x=2x+\frac32\iff 2x^2-x-3=0\iff x=-1,\ x=\frac32$$ Entre aquests valors la recta està per damunt (en $x=0$: $\frac32>0$)."),
             st('Àrea.', r'$$A=\int_{-1}^{3/2}\left(-x^2+\frac{x}{2}+\frac32\right)dx=\left[-\frac{x^3}{3}+\frac{x^2}{4}+\frac{3x}{2}\right]_{-1}^{3/2}=\frac{27}{16}-\left(-\frac{11}{12}\right)=\frac{125}{48}$$'),
             gr([f13, diff(f13, x)], xr=(-2.5, 2.5), yr=(-1.5, 5), shade=[(diff(f13, x), f13, -1, 1.5)], pts=[(-1, -0.5), (1.5, 4.5)])],
            r'a) $m=\frac32$; b) $A=\dfrac{125}{48}\approx %s$ u².' % dd(R(125, 48)))

# 14
ok(10 * 2**10, 10240)
S[14] = SOL([st('a)', r'Cada dia el nombre es multiplica per 2: $N(t)=10\cdot2^t$. Al cap de 10 dies, $N(10)=10\cdot2^{10}=10240$ bacteris.'),
             st('b)', r"Si $P'(t)=k$ és constant, $P(t)=kt+P(0)$ és lineal. $P(3)=3k+500=1100\Rightarrow k=200$ bacteris/dia. Aleshores $P(t)=500+200t$ i $P(10)=2500$: l’augment és $P(10)-P(0)=200\cdot10=2000$ bacteris.")],
            r'a) 10240 bacteris; b) un augment de 2000 bacteris.')

# 15
F15 = 2 * ln((x + 1)**2 + 1) + 7 * atan(x + 1)
pri((4 * x + 11) / ((x + 1)**2 + 1), F15); ok(I((4 * x + 11) / ((x + 1)**2 + 1), 0, sqrt(3) - 1), 2 * ln(2) + 7 * pi / 12)
S[15] = SOL([st('a) Descomposició.', r'Escrivim el numerador en funció de $x+1$: $4x+11=4(x+1)+7$. $$\int\frac{4x+11}{(x+1)^2+1}dx=2\int\frac{2(x+1)}{(x+1)^2+1}dx+7\int\frac{dx}{(x+1)^2+1}=2\ln\big((x+1)^2+1\big)+7\arctan(x+1)+C$$ (la primera és del tipus $\int\frac{u^{\prime}}{u}$ i la segona del tipus $\int\frac{u^{\prime}}{1+u^2}$).'),
             st('b) Barrow.', r'$$\Big[2\ln\big((x+1)^2+1\big)+7\arctan(x+1)\Big]_0^{\sqrt3-1}=\left(2\ln4+7\cdot\frac{\pi}{3}\right)-\left(2\ln2+7\cdot\frac{\pi}{4}\right)=2\ln2+\frac{7\pi}{12}$$')],
            r'a) $2\ln\big((x+1)^2+1\big)+7\arctan(x+1)+C$; b) $2\ln2+\dfrac{7\pi}{12}\approx %s$.' % dd(2 * ln(2) + 7 * pi / 12))

# 16
A16 = x**2 + (16 - x)**2
ok(solve(diff(A16, x), x), [8]); ok(sqrt(A16.subs(x, 8)), 8 * sqrt(2))
S[16] = SOL([st('Plantejament.', r'Cada vèrtex del quadrat interior divideix un costat del gran en dos trossos $x$ i $16-x$ ($0\le x\le16$). El costat interior és la hipotenusa d’un triangle rectangle amb aquests catets, i l’àrea és $$A(x)=x^2+(16-x)^2$$'),
             st('Mínim.', r"$A'(x)=2x-2(16-x)=4x-32=0\iff x=8$; $A''=4>0$: mínim. $A(8)=128$ cm² (als extrems, $A(0)=A(16)=256$).")],
            r'El quadrat d’àrea mínima té els vèrtexs en els punts mitjans dels costats: costat $8\sqrt2\approx11{,}31$ cm (àrea 128 cm²).')

# 17
ok(sp.factor((x - 1)**3 - 5 + x**2), (x - 2) * (x**2 + 3)); ok(I(5 - x**2 - (x - 1)**3, 0, 2), R(22, 3))
S[17] = SOL([st('a) Tall.', r'$(x-1)^3=5-x^2\iff x^3-2x^2+3x-6=0\iff (x-2)(x^2+3)=0\iff x=2$. El punt de tall és $(2,1)$.'),
             st('b) Recinte.', r'Està limitat per l’eix OY ($x=0$) i el punt de tall ($x=2$); en $x=0$, $5>-1$, així que la paràbola està per damunt: $$A=\int_0^2\big(5-x^2-(x-1)^3\big)dx=\left[5x-\frac{x^3}{3}-\frac{(x-1)^4}{4}\right]_0^2=\left(10-\frac83-\frac14\right)-\left(-\frac14\right)=\frac{22}{3}$$'),
             gr([(x - 1)**3, 5 - x**2], xr=(-1, 3), yr=(-2, 6), shade=[(5 - x**2, (x - 1)**3, 0, 2)], pts=[(2, 1)])],
            r'a) $(2,1)$; b) $A=\dfrac{22}{3}\approx7{,}33$ u².')

# 18
V18 = pi / 3 * (2 * r * h**2 - h**3)
ok(solve(diff(V18, h), h), [0, R(4, 3) * r]); ok(V18.subs(h, R(4, 3) * r) / (R(4, 3) * pi * r**3), R(8, 27))
S[18] = SOL([st('Plantejament.', r'Siga $R$ el radi de l’esfera, $h$ l’altura del con ($0<h<2R$) i $\rho$ el radi de la base. Tallant per un pla que conté l’eix, el centre de l’esfera dista $|h-R|$ de la base: $\rho^2+(h-R)^2=R^2\Rightarrow\rho^2=2Rh-h^2$. $$V(h)=\frac13\pi\rho^2h=\frac{\pi}{3}(2Rh^2-h^3)$$'),
             st('Màxim.', r"$V'(h)=\frac{\pi}{3}(4Rh-3h^2)=0\Rightarrow h=\frac{4R}{3}$. $V'>0$ abans i $V'<0$ després: màxim. $$V_{\max}=\frac{\pi}{3}\left(2R\cdot\frac{16R^2}{9}-\frac{64R^3}{27}\right)=\frac{32\pi R^3}{81}$$"),
             st('Comparació.', r'$\dfrac{V_{\max}}{V_{esfera}}=\dfrac{32\pi R^3/81}{4\pi R^3/3}=\dfrac{8}{27}\approx0{,}2963<0{,}30$.')],
            r'El con inscrit més gran té $V=\frac{32\pi R^3}{81}$, que és el $29{,}63\,\%$ del volum de l’esfera: qualsevol con inscrit ocupa menys del 30 %.')

# 19
ok(limit(sin(pi * x) / x, x, 0, '-'), pi); ok(limit(x * ln(x), x, 0, '+'), 0)
S[19] = SOL([st('Fora de 0.', r'Per a $x>0$, $x\ln x+a$ és contínua; per a $x<0$, $\frac{\sin\pi x}{x}$ és quocient de contínues amb denominador no nul. Només cal estudiar $x=0$.'),
             st('Límit per l’esquerra.', r'Amb l’infinitèsim equivalent $\sin\pi x\sim\pi x$: $\displaystyle\lim_{x\to0^-}\frac{\sin\pi x}{x}=\lim_{x\to0^-}\frac{\pi x}{x}=\pi$.'),
             st('Límit per la dreta.', r'$\displaystyle\lim_{x\to0^+}x\ln x$ és del tipus $0\cdot(-\infty)$. Amb $x=\frac1t$ ($t\to+\infty$): $x\ln x=-\dfrac{\ln t}{t}\to0$, perquè el logaritme és un infinit d’ordre inferior a $t$. Per tant $\displaystyle\lim_{x\to0^+}(x\ln x+a)=a$.'),
             st('Continuïtat.', r'Cal $\displaystyle\lim_{x\to0^-}f=\lim_{x\to0^+}f=f(0)$: $\pi=a=b$.')],
            r'$a=b=\pi$.')

# 20
C20 = R(29483, 100000) * t + R(4253, 100000) * t**2 - R(35, 100000) * t**3
z20 = max(float(v) for v in sp.Poly(C20 / t, t).nroots()); m20 = max(float(v) for v in sp.Poly(diff(C20, t), t).nroots())
okn(z20, 128.0866, 1e-4); okn(m20, 84.3438, 1e-4)
S[20] = SOL([st('a) Zeros.', r'$C(t)=t\,(0{,}29483+0{,}04253t-0{,}00035t^2)=0$. A banda de $t=0$: $$0{,}00035t^2-0{,}04253t-0{,}29483=0\Rightarrow t=\frac{0{,}04253\pm\sqrt{0{,}04253^2+4\cdot0{,}00035\cdot0{,}29483}}{0{,}0007}\Rightarrow t\approx%s,\ t\approx%s$$ La concentració és positiva entre $t=0$ i $t\approx%s$ min.' % (ap(z20), ap(min(float(v) for v in sp.Poly(C20 / t, t).nroots())), ap(z20))),
             st('b) Màxim.', r"$C'(t)=0{,}29483+0{,}08506t-0{,}00105t^2=0\Rightarrow t=\dfrac{0{,}08506+\sqrt{0{,}08506^2+4\cdot0{,}00105\cdot0{,}29483}}{0{,}0021}\approx%s$ min (l’altra arrel és negativa). Com que $C''(t)=0{,}08506-0{,}0021t<0$ en aquest punt, és un màxim: $C(%s)\approx%s$ mg/ml." % (ap(m20), ap(m20), ap(C20.subs(t, m20)))),
             gr([(C20, [0, z20])], xr=(-8, 140), pts=[(m20, float(C20.subs(t, m20))), (z20, 0)], xl='t', yl='C')],
            r'a) El fàrmac actua durant uns $%s$ minuts (unes 2 h 8 min); b) la concentració és màxima als $%s$ minuts.' % (ap(z20, 1), ap(m20, 1)))

# 21
ok(solve(diff(2 * r - r**2, r), r), [1]); ok(solve(diff(2 * r + 2 / r, r), r), [-1, 1])
S[21] = SOL([st('a)', r"$2R+R\alpha=4\Rightarrow\alpha=\dfrac{4-2R}{R}$ ($0<R<2$). $A(R)=\frac12\alpha R^2=\frac12R(4-2R)=2R-R^2$. $A'(R)=2-2R=0\iff R=1$, $A''=-2<0$: màxim. Aleshores $\alpha=2$ rad (àrea 1 m²)."),
             st('b)', r"$\frac12\alpha R^2=1\Rightarrow\alpha=\dfrac{2}{R^2}$. $P(R)=2R+R\alpha=2R+\dfrac2R$, $R>0$. $P'(R)=2-\dfrac{2}{R^2}=0\iff R=1$; $P''(R)=\dfrac{4}{R^3}>0$: mínim, $P(1)=4$ m.")],
            r'a) $\alpha=2$ rad (amb $R=1$ m); b) $R=1$ m (perímetre mínim de 4 m).')

# 22
ok(1 - R(995, 1000)**4, R(19850499375, 10**12))
S[22] = SOL([st('Model.', r'$Q=k\,r^4$. Amb el radi real $r^{\prime}=0{,}995\,r$, el cabal és $Q^{\prime}=k(0{,}995r)^4=0{,}995^4\,Q\approx0{,}98015\,Q$.'),
             st('Estimació amb la derivada.', r"$\dfrac{dQ}{dr}=4kr^3\Rightarrow \Delta Q\approx4kr^3\,\Delta r\Rightarrow\dfrac{\Delta Q}{Q}\approx4\,\dfrac{\Delta r}{r}=4\cdot(-0{,}5\,\%)=-2\,\%$.")],
            r'El cabal es reduirà aproximadament un 2 % (exactament un $1{,}985\,\%$).')

# 23
S[23] = SOL([st('Tangent genèrica.', r"$(2,3)$ no és de la corba ($f(2)=7$). La tangent en el punt d’abscissa $a$ és $y=f(a)+f'(a)(x-a)$, amb $f(a)=a^2+2a-1$ i $f'(a)=2a+2$."),
             st('Passa per $(2,3)$.', r'$3=a^2+2a-1+(2a+2)(2-a)=-a^2+4a+3\iff a^2-4a=0\iff a=0$ o $a=4$.'),
             st('Rectes.', r"$a=0$: $f(0)=-1$, $f'(0)=2$: $y=2x-1$. $\quad a=4$: $f(4)=23$, $f'(4)=10$: $y=23+10(x-4)=10x-17$."),
             gr([x**2 + 2 * x - 1, 2 * x - 1, 10 * x - 17], xr=(-3, 5.5), yr=(-4, 26), pts=[(2, 3), (0, -1), (4, 23)])],
            r'$y=2x-1$ (tangent en $(0,-1)$) i $y=10x-17$ (tangent en $(4,23)$).')
ok(((x**2 + 2 * x - 1) - (2 * x - 1)).subs(x, 0), 0); ok(((x**2 + 2 * x - 1) - (10 * x - 17)).subs(x, 4), 0)

# 24
D24 = (20 - 30 * t)**2 + (15 - 60 * t)**2
ok(solve(diff(D24, t), t), [R(1, 3)]); ok(sqrt(D24.subs(t, R(1, 3))), 5 * sqrt(5))
S[24] = SOL([st('a) Distància.', r'Els canals $y=x$ i $y=-x$ són perpendiculars i es tallen en $P=(0,0)$. Al cap de $t$ hores, A és a $20-30t$ km de $P$ i B a $15-60t$ km (amb signe: si és negatiu, la llanxa ja ha passat per $P$ i continua pel mateix canal). Pel teorema de Pitàgores, $$d(t)=\sqrt{(20-30t)^2+(15-60t)^2}=\sqrt{4500t^2-3000t+625}$$'),
             st('b) Mínim.', r"Minimitzem $D(t)=d(t)^2$: $D'(t)=9000t-3000=0\iff t=\frac13$ h, i $D''=9000>0$. $$d\left(\tfrac13\right)=\sqrt{10^2+(-5)^2}=\sqrt{125}=5\sqrt5\ \text{km}$$ (B ja ha passat per $P$, en $t=\frac14$ h, i es troba a 5 km a l’altre costat.)")],
            r'a) $d(t)=\sqrt{4500t^2-3000t+625}$ km; b) la distància mínima és $5\sqrt5\approx11{,}18$ km, als 20 minuts.')

# 25
ok(I(4 - x**2, -1, 2) + I(x**2 - 4, 2, 4), R(59, 3))
S[25] = SOL([st('a)', r'$g(x)=x^2-4$ és una paràbola amb vèrtex $(0,-4)$ que talla l’eix OX en $x=2$ (dins de l’interval). Valors: $g(-1)=-3$, $g(0)=-4$, $g(2)=0$, $g(4)=12$.'),
             gr([(x**2 - 4, [-1, 4]), (Abs(x**2 - 4), [-1, 4])], xr=(-2, 5), yr=(-5, 13), pts=[(-1, -3), (0, -4), (2, 0), (4, 12), (0, 4)]),
             st('b)', r'$f=|g|$ reflecteix la part negativa: candidats als extrems són els extrems de l’interval, el vèrtex i el zero: $f(-1)=3$, $f(0)=4$, $f(2)=0$, $f(4)=12$. Màxim absolut: 12 en $x=4$. Mínim absolut: 0 en $x=2$.'),
             st('c) Àrea.', r'$$A=\int_{-1}^{2}(4-x^2)\,dx+\int_2^4(x^2-4)\,dx=\left[4x-\frac{x^3}{3}\right]_{-1}^{2}+\left[\frac{x^3}{3}-4x\right]_2^4=9+\frac{32}{3}=\frac{59}{3}$$')],
            r'b) Màxim absolut 12 (en $x=4$) i mínim absolut 0 (en $x=2$); c) $A=\dfrac{59}{3}\approx19{,}67$ u².')

# 26
ok(R(17, 83) * 5, R(85, 83))
S[26] = SOL([st('Semblança.', r'Si la persona és a $x$ m del fanal i l’ombra fa $s$ m, els triangles formats pel focus i pel cap de la persona són semblants: $$\frac{10}{x+s}=\frac{1{,}7}{s}\Rightarrow 10s=1{,}7x+1{,}7s\Rightarrow s=\frac{1{,}7}{8{,}3}x=\frac{17}{83}x$$'),
             st('a)', r'$x=5$: $s=\dfrac{85}{83}\approx1{,}02$ m.'),
             st('b)', r"Com que $x=3t$: $s(t)=\dfrac{51}{83}t$ i $s'(t)=\dfrac{51}{83}\approx0{,}61$ m/s, constant.")],
            r'a) $s=\frac{85}{83}\approx1{,}02$ m; b) l’ombra creix a $\frac{51}{83}\approx0{,}61$ m/s en qualsevol instant.')

# 27
S[27] = SOL([st('a)', r'$f(x)=\ln x$ és contínua en $[1,e]$ i derivable en $(1,e)$. Pel teorema del valor mitjà (Lagrange), existeix $c\in(1,e)$ amb $$f^{\prime}(c)=\frac{f(e)-f(1)}{e-1}=\frac{1}{e-1},$$ que és el pendent de la recta $AB$. En $P=(c,\ln c)$ la tangent és paral·lela a $AB$.'),
             st('b)', r"$f'(x)=\dfrac1x$: $\dfrac1c=\dfrac{1}{e-1}\iff c=e-1\approx1{,}718\in(1,e)$. $P=\big(e-1,\ \ln(e-1)\big)\approx(1{,}718;\ 0{,}541)$."),
             st('c)', r'El pendent és $\dfrac{1}{e-1}\approx0{,}582$.')],
            r'b) $P=(e-1,\ln(e-1))$; c) pendent $\frac{1}{e-1}\approx0{,}58$.')

# 28
C28 = 16 * x + 25 / x
ok(solve(diff(C28, x), x), [R(-5, 4), R(5, 4)]); ok(C28.subs(x, R(5, 4)), 40)
S[28] = SOL([st('Cost.', r'Si la base fa $x$ m i l’altura $y$ m, $xy=1$. $$C=2\cdot8x+2\cdot12{,}5y=16x+25y=16x+\frac{25}{x},\quad x>0$$'),
             st('a) Mínim.', r"$C'(x)=16-\dfrac{25}{x^2}=0\iff x=\dfrac54$; $C''(x)=\dfrac{50}{x^3}>0$: mínim. $y=\dfrac45$."),
             st('b)', r'$C\left(\frac54\right)=20+20=40$ €.')],
            r'a) Base 1,25 m i altura 0,8 m; b) 40 €.')

# 29
ok(I((x**3 - 3 * x + 8) - (-3 * x), -2, 0) - I((x**3 - 3 * x + 8) - (-3 * x), -3, -2), R(81, 4))
S[29] = SOL([st('a)', r"$f'(x)=3x^2-3=0\iff x=\pm1$; en $[-3,0]$ només $x=-1$. $f(-3)=-10$, $f(-1)=10$, $f(0)=8$. El màxim absolut és $f(-1)=10$."),
             st('b)', r'$x^3-3x+8=-3x\iff x^3=-8\iff x=-2$. El punt és $(-2,6)$.'),
             st('c)', r'$f(x)-g(x)=x^3+8$, negativa en $[-3,-2)$ i positiva en $(-2,0]$. $$A=\left|\int_{-3}^{-2}(x^3+8)dx\right|+\int_{-2}^{0}(x^3+8)dx=\left|\left[\frac{x^4}{4}+8x\right]_{-3}^{-2}\right|+\left[\frac{x^4}{4}+8x\right]_{-2}^{0}=\frac{33}{4}+12=\frac{81}{4}$$'),
             gr([x**3 - 3 * x + 8, -3 * x], xr=(-3.5, 1), yr=(-12, 13), shade=[(x**3 - 3 * x + 8, -3 * x, -3, 0)], pts=[(-2, 6), (-1, 10)])],
            r'a) Màxim absolut $f(-1)=10$; b) $(-2,6)$; c) $A=\dfrac{81}{4}=20{,}25$ u².')

# 30
ok(diff(pi * (R(9, 5) * t)**2, t).subs(t, 25), 162 * pi)
S[30] = SOL([st('a)', r'$r(t)=1{,}8t$ m, $t$ en minuts: $A(t)=\pi(1{,}8t)^2=3{,}24\pi t^2$ m².'),
             st('b)', r"$r=45\iff t=25$ min. $A'(t)=6{,}48\pi t$, $A'(25)=162\pi$ m²/min. (També: $A'=2\pi r\,r'=2\pi\cdot45\cdot1{,}8$.)")],
            r'a) $A(t)=3{,}24\pi t^2$ m²; b) $162\pi\approx%s$ m²/min.' % dd(162 * pi))

# 31
g31 = -2 * x / pi + sin(x)
ok(g31.subs(x, pi / 2), 0); okn(g31.subs(x, pi / 4), sqrt(2) / 2 - R(1, 2))
S[31] = SOL([st('a)', r"$f'(x)=a+\cos x$. $O\in$ corba: $f(0)=b=0$. Tangent horitzontal en $O$: $f'(0)=a+1=0\Rightarrow a=-1$."),
             st('b)', r'$g(0)=0$: ja tenim un zero. A més, $g$ és contínua, $g\left(\frac{\pi}{4}\right)=-\frac12+\frac{\sqrt2}{2}>0$ i $g(\pi)=-2<0$; pel teorema de Bolzano té un altre zero en $\left(\frac{\pi}{4},\pi\right)$. No en té més: si en tinguera tres, pel teorema de Rolle $g^{\prime}(x)=-\frac2\pi+\cos x$ s’anul·laria dues vegades en $[0,\pi]$, però és estrictament decreixent en aquest interval.'),
             st('c)', r'$g(0)=0$ i $g\left(\frac{\pi}{2}\right)=-\frac2\pi\cdot\frac\pi2+1=0$.'),
             gr([sin(x), 2 * x / pi], xr=(-0.3, 3.4), yr=(-0.3, 2.2), pts=[(0, 0), (math.pi / 2, 1)])],
            r'a) $a=-1$, $b=0$; c) els zeros són $x=0$ i $x=\frac{\pi}{2}$ (on la recta $y=\frac{2}{\pi}x$ talla $y=\sin x$).')

# 32
f32 = sqrt(x**2 + 9) + sqrt((5 - x)**2 + 16)
ok(solve(diff(f32, x), x), [R(15, 7)]); ok(f32.subs(x, R(15, 7)), sqrt(74))
S[32] = SOL([st('a)', r'Col·loquem el pal de 3 m en $x=0$ i el de 4 m en $x=5$. Els cables van de $(0,3)$ a $P(x,0)$ i de $P$ a $(5,4)$: $$f(x)=\sqrt{x^2+9}+\sqrt{(5-x)^2+16},\quad0\le x\le5$$'),
             st('b) Derivada.', r"$$f'(x)=\frac{x}{\sqrt{x^2+9}}-\frac{5-x}{\sqrt{(5-x)^2+16}}=0\iff x^2\big((5-x)^2+16\big)=(5-x)^2(x^2+9)\iff16x^2=9(5-x)^2$$ $\iff4x=3(5-x)\iff x=\frac{15}{7}$. Els pendents (en valor absolut) dels segments són $\frac3x$ i $\frac{4}{5-x}$, i són iguals $\iff 3(5-x)=4x\iff x=\frac{15}{7}$: és la mateixa condició."),
             st('Mínim.', r'$f(0)=3+\sqrt{41}\approx9{,}40$, $f(5)=\sqrt{34}+4\approx9{,}83$ i $$f\left(\tfrac{15}{7}\right)=\frac{\sqrt{666}}{7}+\frac{\sqrt{1184}}{7}=\frac{3\sqrt{74}+4\sqrt{74}}{7}=\sqrt{74}\approx8{,}60$$ és el mínim.')],
            r'a) $f(x)=\sqrt{x^2+9}+\sqrt{(5-x)^2+16}$; b) mínim en $x=\frac{15}{7}$ m, on els pendents són iguals en valor absolut; longitud mínima $\sqrt{74}\approx8{,}60$ m.')

# 33
q33 = (12 * x**3 - 8 * x**2 + 9 * x - 5) / (6 * x**2 - 7 * x + 2)
H33 = x**2 + x + ln(2 * x - 1) + ln(3 * x - 2) - 1
pri(q33, H33); ok(H33.subs(x, 1), 1); ok(sp.apart(q33, x), 2 * x + 1 + 2 / (2 * x - 1) + 3 / (3 * x - 2))
S[33] = SOL([st('a) Verticals.', r'$g(x)=6x^2-7x+2=(2x-1)(3x-2)$ s’anul·la en $x=\frac12$ i $x=\frac23$; $f\left(\frac12\right)=-1\neq0$ i $f\left(\frac23\right)=1\neq0$: asímptotes verticals $x=\frac12$ i $x=\frac23$.'),
             st('Obliqua.', r'Dividim: $12x^3-8x^2+9x-5=(6x^2-7x+2)(2x+1)+(12x-7)$, és a dir, $$\frac{f(x)}{g(x)}=2x+1+\frac{12x-7}{(2x-1)(3x-2)}$$ L’últim terme tendeix a 0 quan $x\to\pm\infty$: asímptota obliqua $y=2x+1$ (no n’hi ha d’horitzontal).'),
             st('b) Fraccions simples.', r'$\dfrac{12x-7}{(2x-1)(3x-2)}=\dfrac{A}{2x-1}+\dfrac{B}{3x-2}$: $x=\frac12\Rightarrow-1=-\frac A2\Rightarrow A=2$; $x=\frac23\Rightarrow1=\frac B3\Rightarrow B=3$. $$H(x)=x^2+x+\ln|2x-1|+\ln|3x-2|+C$$'),
             st('Condició.', r'$H(1)=2+\ln1+\ln1+C=1\Rightarrow C=-1$.')],
            r'a) $x=\frac12$, $x=\frac23$ i $y=2x+1$; b) $H(x)=x^2+x+\ln|2x-1|+\ln|3x-2|-1$.')

# 34
f34 = x**3 - 9 * x**2 + 24 * x - 18
ok(diff(f34, x).subs(x, 2), 0); ok(diff(f34, x).subs(x, 4), 0); ok(f34.subs(x, 3), 0)
S[34] = SOL([st('a)', r"$f'(x)=3x^2+2ax+b$. Tangents horitzontals: $f'(2)=12+4a+b=0$ i $f'(4)=48+8a+b=0$. Restant: $36+4a=0\Rightarrow a=-9$, i $b=24$."),
             st('b)', r"$f''(x)=6x-18=0\iff x=3$ (i $f'''=6\neq0$: és d’inflexió). Perquè estiga en l’eix OX: $f(3)=27-81+72+c=18+c=0\Rightarrow c=-18$.")],
            r'a) $a=-9$, $b=24$; b) $c=-18$.')

# 35
V35 = 100 * x + 250 * (40 - 5 * x) / (10 - x)
ok(solve(diff(V35, x), x), [5, 15]); ok(V35.subs(x, 5), 1250); ok(V35.subs(x, 0), 1000); ok(V35.subs(x, 8), 800)
S[35] = SOL([st('Funció.', r'Valor de venda diari: $$V(x)=100x+250\cdot\frac{40-5x}{10-x},\quad0\le x\le8$$'),
             st('Derivada.', r"$$V'(x)=100+250\cdot\frac{-5(10-x)+(40-5x)}{(10-x)^2}=100-\frac{2500}{(10-x)^2}=0\iff(10-x)^2=25\iff x=5$$ ($x=15$ queda fora). $V''(x)=-\dfrac{5000}{(10-x)^3}<0$: màxim."),
             st('Comprovació.', r'$V(0)=1000$, $V(5)=500+750=1250$, $V(8)=800$ €. El màxim absolut és en $x=5$.')],
            r'S’han de produir 5 tones d’acer de baixa qualitat (i 3 d’alta), amb un valor de venda màxim de 1250 €.')

# 36
A36 = 2 * x * (12 - x**2)
ok(solve(diff(A36, x), x), [-2, 2]); ok(A36.subs(x, 2), 32)
S[36] = SOL([st('Plantejament.', r'Per simetria, els vèrtexs són $(\pm x,0)$ i $(\pm x,12-x^2)$, amb $0<x<\sqrt{12}$: $$A(x)=2x(12-x^2)=24x-2x^3$$'),
             st('Màxim.', r"$A'(x)=24-6x^2=0\iff x=2$; $A''(2)=-24<0$: màxim. Base $2x=4$, altura $12-4=8$."),
             gr([12 - x**2], xr=(-4, 4), yr=(-1, 13), shade=[(sp.Integer(8), None, -2, 2)], pts=[(-2, 8), (2, 8)])],
            r'El cartell fa 4 de base per 8 d’altura (àrea màxima 32).')

# 37
q37 = (4 * x**2 + 2 * x + 10) / (x**3 + x**2 + 5 * x + 5)
H37 = 2 * ln(x + 1) + ln(x**2 + 5) - ln(5)
pri(q37, H37); ok(H37.subs(x, 0), 0)
S[37] = SOL([st('a)', r'$g(x)=x^2(x+1)+5(x+1)=(x+1)(x^2+5)$ només s’anul·la en $x=-1$, i $f(-1)=12\neq0$: asímptota vertical $x=-1$. El grau del numerador és menor que el del denominador: asímptota horitzontal $y=0$.'),
             st('b) Fraccions simples.', r'$$\frac{4x^2+2x+10}{(x+1)(x^2+5)}=\frac{A}{x+1}+\frac{Bx+C}{x^2+5}$$ $x=-1$: $12=6A\Rightarrow A=2$. Aleshores $4x^2+2x+10-2(x^2+5)=2x^2+2x=(Bx+C)(x+1)\Rightarrow B=2,\ C=0$.'),
             st('Integral.', r'$$H(x)=\int\left(\frac{2}{x+1}+\frac{2x}{x^2+5}\right)dx=2\ln|x+1|+\ln(x^2+5)+C$$ $H(0)=\ln5+C=0\Rightarrow C=-\ln5$.')],
            r'a) $x=-1$ i $y=0$; b) $H(x)=2\ln|x+1|+\ln(x^2+5)-\ln5$.')

# 38
ok(solve(sp.Eq(-8, 8 / a - 16 / a**2), a), [-2, 1])
S[38] = SOL([st('a)', r"$f'(x)=-\dfrac{4}{x^2}$; $f(2)=2$, $f'(2)=-1$. Tangent: $y-2=-(x-2)\iff y=-x+4$. Normal (pendent $1$): $y-2=x-2\iff y=x$."),
             st('b) Tangent en $x=a$.', r'$y=\dfrac4a-\dfrac{4}{a^2}(x-a)=\dfrac8a-\dfrac{4}{a^2}x$. Passa per $(4,-8)$: $$-8=\frac8a-\frac{16}{a^2}\iff 8a^2+8a-16=0\iff a^2+a-2=0\iff a=1,\ a=-2$$'),
             st('Punts.', r'$M=(1,4)$ (tangent $y=8-4x$) i $N=(-2,-2)$ (tangent $y=-x-4$). Totes dues passen per $(4,-8)$.')],
            r'a) Tangent $y=-x+4$, normal $y=x$; b) $M(1,4)$ i $N(-2,-2)$.')

# 39
ok(limit((12 + x**R(7, 4)) / (x**2 - 2 * x + 10), x, oo), 0)
S[39] = SOL([st('Ordre dels infinits.', r'$12+n\sqrt[4]{n^3}=12+n^{7/4}$ és un infinit d’ordre $\frac74$, i $n^2-2n+10$ d’ordre 2.'),
             st('Límit.', r'$$\lim_{n\to\infty}\frac{12+n^{7/4}}{n^2-2n+10}=\lim_{n\to\infty}\frac{\frac{12}{n^2}+\frac{1}{n^{1/4}}}{1-\frac2n+\frac{10}{n^2}}=\frac{0}{1}=0$$'),
             st('Conclusió.', r'Com que el quocient tendeix a 0, per a $n$ gran és menor que 1: el nombre d’operacions d’$A$ (que no supera $12+n^{7/4}$) és menor que el de $B$.')],
            r'$\displaystyle\lim_{n\to\infty}\frac{12+n\sqrt[4]{n^3}}{n^2-2n+10}=0$, i per tant per a $n$ gran $A$ fa menys operacions que $B$.')

# 40
D40 = x**2 + (2 - x**2)**2
ok(D40.subs(x, sqrt(R(3, 2))), R(7, 4))
S[40] = SOL([st('a)', r'Els punts del segment són $(x,0)$, $-2\le x\le2$; la seua distància al sortidor és $\sqrt{x^2+4}\ge2$, mínima en $(0,0)$ ($d=2$).'),
             st('b) Arc.', r"Un punt de l’arc és $(x,4-x^2)$: $d^2=x^2+(2-x^2)^2=x^4-3x^2+4=D(x)$. $D'(x)=4x^3-6x=2x(2x^2-3)=0\iff x=0,\ x=\pm\sqrt{\tfrac32}$. $D(0)=4$, $D\left(\pm\sqrt{\tfrac32}\right)=\frac94-\frac92+4=\frac74$, $D(\pm2)=8$. Els punts més pròxims són $\left(\pm\frac{\sqrt6}{2},\frac52\right)$, a distància $\frac{\sqrt7}{2}\approx1{,}32$."),
             st('c)', r'Com que $\frac{\sqrt7}{2}<2$, els punts de la vora més pròxims al sortidor són els de l’arc: $\left(\pm\frac{\sqrt6}{2},\frac52\right)$.'),
             gr([(4 - x**2, [-2, 2]), (sp.Integer(0), [-2, 2])], xr=(-3, 3), yr=(-0.8, 4.5), pts=[(0, 2), (math.sqrt(1.5), 2.5), (-math.sqrt(1.5), 2.5), (0, 0)])],
            r'a) $(0,0)$; b) i c) $\left(\frac{\sqrt6}{2},\frac52\right)$ i $\left(-\frac{\sqrt6}{2},\frac52\right)$, a distància $\frac{\sqrt7}{2}$.')

# 41
ok(I(1 / (4 + x**2), 0, 2), pi / 8); ok(I(1 / (4 + x**2), 0, 2 / sqrt(3)), pi / 12)
S[41] = SOL([st('a)', r'$$A=\int_0^2\frac{dx}{4+x^2}=\frac14\int_0^2\frac{dx}{1+(x/2)^2}=\left[\frac12\arctan\frac x2\right]_0^2=\frac12\cdot\frac{\pi}{4}=\frac{\pi}{8}\ \text{u}^2$$'),
             st('b)', r'L’àrea d’$A$ ha de ser $\frac23\cdot\frac{\pi}{8}=\frac{\pi}{12}$: $$\frac12\arctan\frac\alpha2=\frac{\pi}{12}\iff\arctan\frac\alpha2=\frac{\pi}{6}\iff\frac\alpha2=\frac{1}{\sqrt3}\iff\alpha=\frac{2\sqrt3}{3}$$'),
             gr([1 / (4 + x**2)], xr=(-0.5, 2.5), yr=(-0.03, 0.3), shade=[(1 / (4 + x**2), None, 0, 2)], pts=[(2 / math.sqrt(3), 0.1875)])],
            r'a) $\frac{\pi}{8}\approx0{,}39$ u²; b) $\alpha=\frac{2\sqrt3}{3}\approx1{,}15$.')

# 42
S[42] = SOL([st('a)', r'Paràbola amb vèrtex $(0,-4)$, oberta cap amunt, que talla l’eix OX en $x=\pm2$ i l’eix OY en $(0,-4)$.'),
             gr([x**2 - 4, (ln(x**2 - 4), [-4.5, -2.0001]), (ln(x**2 - 4), [2.0001, 4.5])], xr=(-4.5, 4.5), yr=(-5, 6), va=(-2, 2), pts=[(0, -4)]),
             st('b)', r'$\ln f(x)$ existeix si $x^2-4>0\iff x<-2$ o $x>2$: domini $(-\infty,-2)\cup(2,+\infty)$.'),
             st('c)', r"$g'(x)=\dfrac{2x}{x^2-4}$; el denominador és positiu en el domini, així que el signe és el de $x$: $g$ decreix en $(-\infty,-2)$ i creix en $(2,+\infty)$. No té màxim absolut: $\displaystyle\lim_{x\to\pm\infty}g(x)=+\infty$ (tampoc no té mínim, perquè $g\to-\infty$ quan $x\to\pm2$).")],
            r'b) $(-\infty,-2)\cup(2,+\infty)$; c) decreix en $(-\infty,-2)$, creix en $(2,+\infty)$ i no té màxim absolut.')

# 43
S43 = (x + 2) * (18 / x + 4)
ok(solve(diff(S43, x), x), [-3, 3]); ok(S43.subs(x, 3), 50)
S[43] = SOL([st('Plantejament.', r'Si el text fa $x$ cm d’ample i $\frac{18}{x}$ d’alt, el full fa $(x+2)\times\left(\frac{18}{x}+4\right)$: $$S(x)=(x+2)\left(\frac{18}{x}+4\right)=26+4x+\frac{36}{x},\quad x>0$$'),
             st('Mínim.', r"$S'(x)=4-\dfrac{36}{x^2}=0\iff x=3$; $S''(x)=\dfrac{72}{x^3}>0$: mínim. Text de $3\times6$ cm; full de $5\times10$ cm.")],
            r'El full ha de fer 5 cm d’ample i 10 cm d’alt (50 cm²).')

# 44
th = sp.symbols('theta', real=True)
A44 = 800 * sin(th) * (1 - cos(th))
ok(diff(A44, th).subs(th, 2 * pi / 3), 0); ok(A44.subs(th, 2 * pi / 3), 600 * sqrt(3))
S[44] = SOL([st('Plantejament.', r'Siga $\theta$ l’angle entre el costat oblic i la base menor ($\frac{\pi}{2}<\theta<\pi$). Baixant la perpendicular des de l’extrem de la base menor: altura $h=40\sin\theta$, i la base major és $20+40\cos(\pi-\theta)=20-40\cos\theta$. $$A(\theta)=\frac{20+(20-40\cos\theta)}{2}\cdot40\sin\theta=800\sin\theta\,(1-\cos\theta)$$'),
             st('Derivada.', r"$A'(\theta)=800\left(\cos\theta-\cos^2\theta+\sin^2\theta\right)=800(1+\cos\theta-2\cos^2\theta)=-800(2\cos\theta+1)(\cos\theta-1)$. En $(\frac\pi2,\pi)$ s’anul·la si $\cos\theta=-\frac12\iff\theta=\frac{2\pi}{3}=120°$; abans és positiva i després negativa: màxim."),
             st('Àrea màxima.', r'$A\left(\frac{2\pi}{3}\right)=800\cdot\frac{\sqrt3}{2}\cdot\frac32=600\sqrt3$ cm².')],
            r'L’angle ha de ser de $120°$ ($\frac{2\pi}{3}$ rad) i l’àrea màxima és $600\sqrt3\approx1039{,}23$ cm².')

# 45
F45 = x * (a / 2 * x**2 + (a + b) * x)
ok(I(a * t + b, 1, x + 1, t), a / 2 * x**2 + (a + b) * x); ok(diff(F45, x, 2).subs(x, 0), 2 * (a + b))
S[45] = SOL([st('a)', r'$$\int_1^{x+1}(at+b)\,dt=\left[\frac{a t^2}{2}+bt\right]_1^{x+1}=\frac a2\big((x+1)^2-1\big)+bx=\frac a2x^2+(a+b)x$$'),
             st('b)', r"$F(x)=\dfrac a2x^3+(a+b)x^2\Rightarrow F'(x)=\dfrac{3a}{2}x^2+2(a+b)x$."),
             st('c)', r"$F''(x)=3ax+2(a+b)$; $F''(0)=2(a+b)=0\iff b=-a$.")],
            r"a) $\frac a2x^2+(a+b)x$; b) $F'(x)=\frac{3a}{2}x^2+2(a+b)x$; c) $a+b=0$.")
