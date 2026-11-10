# Solucions dels exercicis PAU d'anàlisi de 2n Batx MII (recull de l'IES Vermellar), números 46-90.
from mlib import *  # noqa: F401,F403

S = {}
al = sp.symbols('alpha', positive=True)

# 46
ok(I(x**2 + al, 0, sqrt(6)), sqrt(6) * (2 + al)); ok(solve(sp.Eq(sqrt(6) * (2 + al), sqrt(6) * (6 + al) / 2), al), [2])
S[46] = SOL([st('a)', r'$g(x)=x^2+\alpha>0$, així que $$A=\int_0^{\sqrt6}(x^2+\alpha)\,dx=\left[\frac{x^3}{3}+\alpha x\right]_0^{\sqrt6}=\frac{6\sqrt6}{3}+\alpha\sqrt6=\sqrt6\,(2+\alpha)\ \text{u}^2$$'),
             st('b)', r'La corba passa per $(0,\alpha)$ i $(\sqrt6,6+\alpha)$, dos vèrtexs del rectangle, que té àrea $\sqrt6\,(6+\alpha)$. La regió de davall de la corba és la de l’apartat a): $$\sqrt6\,(2+\alpha)=\frac{\sqrt6\,(6+\alpha)}{2}\iff4+2\alpha=6+\alpha\iff\alpha=2$$'),
             gr([x**2 + 2], xr=(-0.5, 3), yr=(-0.5, 9), shade=[(x**2 + 2, None, 0, math.sqrt(6))], pts=[(0, 2), (math.sqrt(6), 8)])],
            r'a) $A=\sqrt6\,(2+\alpha)$ u²; b) $\alpha=2$.')

# 47
S[47] = SOL([st('a)', r'Es mou cap amunt sobre $x=1$ a 2 m/s: $M(t)=(1,\,2t)$.'),
             st('b)', r'$m(t)=\dfrac{2t-0}{1-0}=2t$.'),
             st('c)', r"$m^{\prime}(t)=2$: el pendent creix a un ritme constant de 2 unitats per segon.")],
            r"a) $M(t)=(1,2t)$; b) $m(t)=2t$; c) $m^{\prime}(t)=2$.")

# 48
A48 = x * sqrt(50 - x**2 / 4)
ok(pos(diff(A48, x)), [10]); ok(A48.subs(x, 10), 50)
S[48] = SOL([st('a)', r'Per simetria, la base del rectangle (de longitud $x$) està centrada en el diàmetre i els vèrtexs superiors són $\left(\pm\frac x2,h\right)$ sobre $X^2+Y^2=50$: $h=\sqrt{50-\frac{x^2}{4}}$. $$A(x)=x\sqrt{50-\frac{x^2}{4}},\quad0<x<2\sqrt{50}$$'),
             st('b)', r"Maximitzem $A^2=50x^2-\frac{x^4}{4}$: $(A^2)^{\prime}=100x-x^3=0\iff x=10$ (positiu); hi passa de positiva a negativa: màxim. Altura $h=\sqrt{25}=5$ m i àrea $50$ m².")],
            r'a) $A(x)=x\sqrt{50-\frac{x^2}{4}}$; b) $x=10$ m (rectangle de $10\times5$ m, 50 m²).')

# 49
ok(I(1 / (9 - x**2), -2, 2), ln(5) / 3)
S[49] = SOL([st('a)', r"$f(x)=\dfrac{1}{9-x^2}$, domini $\mathbb R\setminus\{-3,3\}$. $f^{\prime}(x)=\dfrac{2x}{(9-x^2)^2}$, amb el signe de $x$: decreix en $(-\infty,-3)$ i $(-3,0)$; creix en $(0,3)$ i $(3,+\infty)$ (mínim relatiu en $(0,\frac19)$)."),
             st('b)', r'$1=A(3+x)+B(3-x)$: $x=3\Rightarrow A=\frac16$; $x=-3\Rightarrow B=\frac16$.'),
             st('c)', r'En $[-2,2]$, $f>0$: $$A=\frac16\int_{-2}^{2}\left(\frac{1}{3-x}+\frac{1}{3+x}\right)dx=\frac16\Big[\ln(3+x)-\ln(3-x)\Big]_{-2}^{2}=\frac16(\ln5+\ln5)=\frac{\ln5}{3}$$'),
             gr([1 / (9 - x**2)], xr=(-4.5, 4.5), yr=(-0.6, 0.8), va=(-3, 3), shade=[(1 / (9 - x**2), None, -2, 2)])],
            r'a) Decreix en $(-\infty,-3)\cup(-3,0)$ i creix en $(0,3)\cup(3,+\infty)$; b) $A=B=\frac16$; c) $\frac{\ln5}{3}\approx0{,}54$ u².')

# 50
ok(I(exp(x) - exp(-x), -a, a), 0)
S[50] = SOL([st('a)', r'$f(-x)=e^{-x}-e^{x}=-f(x)$, per tant $f(x)+f(-x)=0$ (la funció és senar).'),
             st('b)', r'$$\int_{-a}^{a}(e^x-e^{-x})\,dx=\Big[e^x+e^{-x}\Big]_{-a}^{a}=(e^a+e^{-a})-(e^{-a}+e^{a})=0$$ (és el resultat esperat per a una funció senar en un interval simètric).'),
             st('c)', r"$f^{\prime}(x)=e^x+e^{-x}$, $f^{\prime\prime}(x)=e^x-e^{-x}=0\iff e^{2x}=1\iff x=0$. $f^{\prime\prime}<0$ si $x<0$ i $f^{\prime\prime}>0$ si $x>0$: canvia la curvatura. Punt d’inflexió $(0,0)$.")],
            r'a) $0$; b) $0$; c) $(0,0)$.')

# 51
C51 = 700 * x**2 + 89600 / x
ok(sp.simplify((225 + 300) * R(4, 3) * x**2 + 256 * (2 * x + 2 * R(4, 3) * x) * 75 / x**2 - C51), 0)
ok([s_ for s_ in solve(diff(C51, x), x) if s_.is_real], [4]); ok(C51.subs(x, 4), 33600)
S[51] = SOL([st('Dimensions.', r'Base $x\times\frac43x$ i altura $h$: $\frac43x^2h=100\Rightarrow h=\dfrac{75}{x^2}$.'),
             st('Cost.', r'Sòl i sostre: $(225+300)\cdot\frac43x^2=700x^2$. Parets: $256\cdot2\left(x+\frac43x\right)h=256\cdot\frac{14x}{3}\cdot\frac{75}{x^2}=\dfrac{89600}{x}$. $$C(x)=700x^2+\frac{89600}{x},\quad x>0$$'),
             st('a)', r"$C^{\prime}(x)=1400x-\dfrac{89600}{x^2}=0\iff x^3=64\iff x=4$ m; $C^{\prime\prime}(x)=1400+\dfrac{179200}{x^3}>0$: mínim."),
             st('b)', r'$C(4)=11200+22400=33600$ €.')],
            r'a) $x=4$ m (base de $4\times\frac{16}{3}$ m i altura $\frac{75}{16}$ m); b) 33600 €.')

# 52
B52 = (120 - x) * (50 + R(5, 3) * x)
ok(solve(diff(B52, x), x), [45]); ok(B52.subs(x, 45), 9375)
S[52] = SOL([st('Variables.', r'Preu de venda inicial: $300\cdot1{,}4=420$ €. Si rebaixa $x$ euros, ven $50+\frac{5x}{3}$ unitats i guanya $420-x-300=120-x$ per unitat.'),
             st('Benefici.', r'$B(x)=(120-x)\left(50+\frac{5x}{3}\right)$, $0\le x\le120$.'),
             st('Màxim.', r"$B^{\prime}(x)=-\left(50+\frac{5x}{3}\right)+\frac53(120-x)=150-\frac{10x}{3}=0\iff x=45$; $B^{\prime\prime}=-\frac{10}{3}<0$: màxim. Preu $420-45=375$ €, unitats $50+75=125$, benefici $75\cdot125=9375$ €.")],
            r'Ha de demanar 125 unitats i vendre-les a 375 € cadascuna (benefici de 9375 €).')

# 53
q53 = (2 * x**2 + 12 * x - 6) / ((x - 2) * (x**2 + 9)); H53 = 2 * ln(x - 2) + 4 * atan(x / 3) - 2 * pi / 3
ok(sp.apart(q53, x), 2 / (x - 2) + 12 / (x**2 + 9)); pri(q53, H53, at=(R(5, 2), R(7, 2))); ok(H53.subs(x, 3), pi / 3)
S[53] = SOL([st('a)', r'El denominador només s’anul·la en $x=2$ i el numerador hi val $26\neq0$: asímptota vertical $x=2$. Grau del numerador (2) menor que el del denominador (3): asímptota horitzontal $y=0$.'),
             st('b) Fraccions simples.', r'$\dfrac{2x^2+12x-6}{(x-2)(x^2+9)}=\dfrac{A}{x-2}+\dfrac{Bx+C}{x^2+9}$. $x=2$: $26=13A\Rightarrow A=2$. Aleshores $2x^2+12x-6-2(x^2+9)=12x-24=(Bx+C)(x-2)\Rightarrow B=0,\ C=12$.'),
             st('Integral.', r'$$H(x)=\int\left(\frac{2}{x-2}+\frac{12}{x^2+9}\right)dx=2\ln|x-2|+4\arctan\frac x3+C$$ ($\int\frac{12}{9+x^2}dx=\frac{12}{9}\int\frac{dx}{1+(x/3)^2}=4\arctan\frac x3$). $H(3)=0+4\cdot\frac{\pi}{4}+C=\frac{\pi}{3}\Rightarrow C=-\frac{2\pi}{3}$.')],
            r'a) $x=2$ i $y=0$; b) $H(x)=2\ln|x-2|+4\arctan\dfrac x3-\dfrac{2\pi}{3}$.')

# 54
f54 = 8 / (1 + x**2)
ok(diff(f54, x, 2), 16 * (3 * x**2 - 1) / (1 + x**2)**3); ok(diff(f54, x).subs(x, -1 / sqrt(3)), 3 * sqrt(3))
S[54] = SOL([st('a)', r"$$f^{\prime}(x)=\frac{-16x}{(1+x^2)^2},\qquad f^{\prime\prime}(x)=\frac{-16(1+x^2)^2+16x\cdot2(1+x^2)\cdot2x}{(1+x^2)^4}=\frac{16(3x^2-1)}{(1+x^2)^3}$$"),
             st('b)', r"$f^{\prime\prime}(x)=0\iff x=\pm\frac{\sqrt3}{3}$, i hi canvia de signe. $f\left(\pm\frac{\sqrt3}{3}\right)=\frac{8}{4/3}=6$: punts d’inflexió $\left(\pm\frac{\sqrt3}{3},6\right)$."),
             st('c)', r"El pendent és $m(x)=f^{\prime}(x)$; els seus extrems són on $m^{\prime}=f^{\prime\prime}=0$. $f^{\prime\prime}>0$ si $x<-\frac{\sqrt3}{3}$ i $<0$ entre $\pm\frac{\sqrt3}{3}$: el pendent és màxim en $x=-\frac{\sqrt3}{3}$: $m=\dfrac{16\cdot\frac{\sqrt3}{3}}{16/9}=3\sqrt3$. Com que $f^{\prime}\to0$ en $\pm\infty$, és el màxim absolut.")],
            r'b) $\left(\pm\frac{\sqrt3}{3},6\right)$; c) $3\sqrt3\approx5{,}20$.')

# 55
D55 = (150 - 40 * t)**2 + (30 * t)**2
ok(solve(diff(D55, t), t), [R(12, 5)]); ok(sqrt(D55.subs(t, R(12, 5))), 90)
S[55] = SOL([st('Posicions.', r'Prenem B en l’origen a les 7 h, amb l’eix X cap a l’est. Al cap de $t$ hores: $A=(150-40t,\,0)$ i $B=(0,\,30t)$.'),
             st('Distància.', r"$d(t)^2=(150-40t)^2+900t^2=2500t^2-12000t+22500$. $(d^2)^{\prime}=5000t-12000=0\iff t=2{,}4$ h, i és un mínim (paràbola oberta cap amunt). $d(2{,}4)=\sqrt{14400-28800+22500}=\sqrt{8100}=90$ km.")],
            r'Estaran a distància mínima (90 km) al cap de 2,4 h = 2 h 24 min, és a dir, a les 9:24.')

# 56
S[56] = SOL([st('Relació.', r'$d=\sqrt{b^2+h^2}$, amb $b$ i $h$ funcions del temps i $b^{\prime}=h^{\prime}=0{,}2$ mm/min $=0{,}02$ cm/min.'),
             st('Derivada.', r"$$d^{\prime}=\frac{b\,b^{\prime}+h\,h^{\prime}}{\sqrt{b^2+h^2}}=\frac{8\cdot0{,}02+6\cdot0{,}02}{10}=0{,}028\ \text{cm/min}$$")],
            r'La diagonal creix a 0,028 cm/min = 0,28 mm/min.')

# 57
f57 = 20000 / x + 3 * pi * x / 2
x57 = 200 / sqrt(3 * pi)
ok(diff(f57, x).subs(x, x57), 0)
S[57] = SOL([st('a)', r'Si els costats verticals fan $y$: $xy+\pi\frac{x^2}{4}=10000\Rightarrow y=\dfrac{10000}{x}-\dfrac{\pi x}{4}$. El perímetre són dues semicircumferències ($\pi x$) i els dos costats verticals: $$P(x)=2y+\pi x=\frac{20000}{x}+\frac{\pi x}{2}$$'),
             st('b)', r'$f(x)=1\cdot2y+2\cdot\pi x=\dfrac{20000}{x}+\dfrac{3\pi x}{2}$, amb $0<x<\dfrac{200}{\sqrt\pi}$ (perquè $y>0$).'),
             st('c)', r"$f^{\prime}(x)=-\dfrac{20000}{x^2}+\dfrac{3\pi}{2}=0\iff x^2=\dfrac{40000}{3\pi}\iff x=\dfrac{200}{\sqrt{3\pi}}\approx%s$ m; $f^{\prime\prime}>0$: mínim. (Aleshores $y\approx%s$ m.)" % (dd(x57), dd(10000 / x57 - pi * x57 / 4)))],
            r'a) $P(x)=\frac{20000}{x}+\frac{\pi x}{2}$; b) $f(x)=\frac{20000}{x}+\frac{3\pi x}{2}$; c) $x=\frac{200}{\sqrt{3\pi}}\approx%s$ m.' % dd(x57))

# 58
ok(solve(sp.Eq(4 + a**2 + 2 * a * 2, 1), a), [-3, -1])
S[58] = SOL([st('a)', r'Paràbola oberta cap avall amb vèrtex $(0,4)$ que talla l’eix OX en $x=\pm2$.'),
             st('b)', r"La recta $x+y=0$ té pendent $-1$; la perpendicular té pendent $1$: $f^{\prime}(x)=-2x=1\iff x=-\frac12$, $P=\left(-\frac12,\frac{15}{4}\right)$."),
             st('c) Tangent en $x=a$.', r'$y=4-a^2-2a(x-a)=4+a^2-2ax$. Passa per $(-2,1)$: $1=4+a^2+4a\iff a^2+4a+3=0\iff a=-1,\ a=-3$.'),
             st('Rectes.', r'$a=-1$: punt $(-1,3)$, $y=2x+5$. $\ a=-3$: punt $(-3,-5)$, $y=6x+13$. (Amb el punt $(2,-1)$ del recull s’obtindria $a^2-4a+5=0$, sense solucions reals: és un punt interior de la paràbola.)'),
             gr([4 - x**2, 2 * x + 5, 6 * x + 13], xr=(-4.5, 3), yr=(-7, 6), pts=[(-2, 1), (-1, 3), (-3, -5), (-0.5, 3.75)])],
            r'b) $P\left(-\frac12,\frac{15}{4}\right)$; c) $y=2x+5$ (tangent en $(-1,3)$) i $y=6x+13$ (tangent en $(-3,-5)$).')

# 59
ok(I(x**3 - 2 * x**2 + x, 0, 1), R(1, 12))
S[59] = SOL([st('a)', r'$x^3=2x^2-x\iff x(x^2-2x+1)=x(x-1)^2=0\iff x=0,\ x=1$: $A(0,0)$ i $B(1,1)$.'),
             st('b)', r'$f(x)-g(x)=x(x-1)^2\ge0$ si $x\ge0$, perquè és producte de dos factors no negatius.'),
             st('c)', r'$$A=\int_0^1(x^3-2x^2+x)\,dx=\left[\frac{x^4}{4}-\frac{2x^3}{3}+\frac{x^2}{2}\right]_0^1=\frac14-\frac23+\frac12=\frac{1}{12}$$'),
             gr([x**3, 2 * x**2 - x], xr=(-0.5, 1.6), yr=(-0.4, 2), shade=[(x**3, 2 * x**2 - x, 0, 1)], pts=[(0, 0), (1, 1)])],
            r'a) $A(0,0)$, $B(1,1)$; c) $\frac{1}{12}$ u².')

# 60
A60 = (x + 5) * sqrt(25 - x**2)
ok([s_ for s_ in solve(diff(A60, x), x) if s_ != -5], [R(5, 2)]); ok(A60.subs(x, R(5, 2)), 75 * sqrt(3) / 4)
S[60] = SOL([st('a)', r'$y=\sqrt{25-x^2}$. La base $BC$ fa $2y$ i l’altura des d’$A$ és $x+5$: $$S(x)=\frac12\cdot2\sqrt{25-x^2}\,(x+5)=(x+5)\sqrt{25-x^2},\quad-5\le x\le5$$'),
             st('b)', r"$$S^{\prime}(x)=\sqrt{25-x^2}-\frac{x(x+5)}{\sqrt{25-x^2}}=\frac{25-5x-2x^2}{\sqrt{25-x^2}}=0\iff2x^2+5x-25=0\iff x=\frac52\ (\text{o }x=-5)$$ $S^{\prime}>0$ abans i $<0$ després: màxim. $y=\sqrt{25-\frac{25}{4}}=\frac{5\sqrt3}{2}$."),
             st('c)', r'$S\left(\frac52\right)=\frac{15}{2}\cdot\frac{5\sqrt3}{2}=\frac{75\sqrt3}{4}$ (el triangle és equilàter).')],
            r'b) $B\left(\frac52,\frac{5\sqrt3}{2}\right)$, $C\left(\frac52,-\frac{5\sqrt3}{2}\right)$; c) $\frac{75\sqrt3}{4}\approx32{,}48$ u².')

# 61
f61 = x / (x**2 - 3 * x + 2)
ok(sp.factor(diff(f61, x)), -(x**2 - 2) / ((x - 1)**2 * (x - 2)**2)); pri(f61, -ln(x - 1) + 2 * ln(x - 2), at=(R(5, 2), R(7, 2)))
ok(f61.subs(x, -sqrt(2)), 2 * sqrt(2) - 3); ok(f61.subs(x, sqrt(2)), -2 * sqrt(2) - 3)
S[61] = SOL([st('a)', r'$x^2-3x+2=(x-1)(x-2)$: domini $\mathbb R\setminus\{1,2\}$. El numerador no s’anul·la en 1 ni en 2: asímptotes verticals $x=1$ i $x=2$. Grau del numerador menor: asímptota horitzontal $y=0$.'),
             st('b)', r"$$f^{\prime}(x)=\frac{(x^2-3x+2)-x(2x-3)}{(x^2-3x+2)^2}=\frac{2-x^2}{(x-1)^2(x-2)^2}=0\iff x=\pm\sqrt2$$" +
                taula_m([(r'(-\infty,-\sqrt2)', '-'), (r'(-\sqrt2,1)', '+'), (r'(1,\sqrt2)', '+'), (r'(\sqrt2,2)', '-'), (r'(2,+\infty)', '-')]) +
                r'Mínim relatiu en $x=-\sqrt2$ ($f=2\sqrt2-3\approx-0{,}17$) i màxim relatiu en $x=\sqrt2$ ($f=-2\sqrt2-3\approx-5{,}83$).'),
             st('c)', r'$\dfrac{x}{(x-1)(x-2)}=\dfrac{A}{x-1}+\dfrac{B}{x-2}$: $x=1\Rightarrow A=-1$; $x=2\Rightarrow B=2$. $$\int f(x)\,dx=-\ln|x-1|+2\ln|x-2|+C$$'),
             gr([f61], xr=(-5, 5), yr=(-9, 6), va=(1, 2), ha=(0,), pts=[(-math.sqrt(2), 2 * math.sqrt(2) - 3), (math.sqrt(2), -2 * math.sqrt(2) - 3)])],
            r'a) $\mathbb R\setminus\{1,2\}$; $x=1$, $x=2$, $y=0$. b) Decreix en $(-\infty,-\sqrt2)\cup(\sqrt2,2)\cup(2,+\infty)$ i creix en $(-\sqrt2,1)\cup(1,\sqrt2)$. c) $-\ln|x-1|+2\ln|x-2|+C$.')

# 62
S62 = 2 * x * (20 - 2 * x**2)
ok(solve(diff(S62, x), x), [-sqrt(R(10, 3)), sqrt(R(10, 3))]); ok(S62.subs(x, sqrt(R(10, 3))), 80 * sqrt(30) / 9)
S[62] = SOL([st('a)', r'$A(x,4-x^2)$, $B(-x,4-x^2)$, $C(x,x^2-16)$, $D(-x,x^2-16)$, amb $0<x\le2$. Base $2x$, altura $(4-x^2)-(x^2-16)=20-2x^2$: $$S(x)=2x(20-2x^2)=40x-4x^3$$'),
             st('b)', r"$S^{\prime}(x)=40-12x^2=0\iff x=\sqrt{\frac{10}{3}}=\frac{\sqrt{30}}{3}\approx1{,}83\in(0,2]$; $S^{\prime\prime}=-24x<0$: màxim."),
             st('c)', r'$S=2x\left(20-\frac{20}{3}\right)=\frac{80}{3}\cdot\frac{\sqrt{30}}{3}=\frac{80\sqrt{30}}{9}\approx48{,}69$ u².')],
            r'a) $S(x)=40x-4x^3$; b) $x=\frac{\sqrt{30}}{3}$; c) $\frac{80\sqrt{30}}{9}\approx48{,}69$ u².')

# 63
f63 = x**2 * exp(-x)
ok(sp.factor(diff(f63, x)), -x * (x - 2) * exp(-x)); ok(sp.factor(diff(f63, x, 2)), (x**2 - 4 * x + 2) * exp(-x)); ok(limit(f63, x, oo), 0)
S[63] = SOL([st('a)', r'Domini $\mathbb R$. $f(x)\ge0$ i $f(0)=0$; $\displaystyle\lim_{x\to-\infty}x^2e^{-x}=+\infty$ i $f$ és contínua, així que pren tots els valors no negatius: recorregut $[0,+\infty)$.'),
             st('b) i c)', r"$f^{\prime}(x)=(2x-x^2)e^{-x}=x(2-x)e^{-x}=0\iff x=0,\ x=2$." + taula_m([(r'(-\infty,0)', '-'), (r'(0,2)', '+'), (r'(2,+\infty)', '-')]) +
                r'Mínim relatiu en $x=0$ ($f=0$) i màxim relatiu en $x=2$ ($f=\frac{4}{e^2}\approx0{,}54$).'),
             st('d)', r"$f^{\prime\prime}(x)=(x^2-4x+2)e^{-x}=0\iff x=2\pm\sqrt2$, i hi canvia de signe: punts d’inflexió en $x=2-\sqrt2\approx0{,}59$ i $x=2+\sqrt2\approx3{,}41$."),
             st('e) Asímptota horitzontal.', r'$\displaystyle\lim_{x\to+\infty}\frac{x^2}{e^x}=0$, perquè l’exponencial és un infinit d’ordre superior a qualsevol potència: $y=0$ és asímptota horitzontal per la dreta. Per l’esquerra $f\to+\infty$ (i $\frac{f(x)}{x}\to-\infty$: branca parabòlica, sense asímptota).'),
             gr([f63], xr=(-1.6, 8), yr=(-0.3, 1.6), pts=[(0, 0), (2, 4 / math.e**2), (2 - math.sqrt(2), float(f63.subs(x, 2 - sqrt(2)))), (2 + math.sqrt(2), float(f63.subs(x, 2 + sqrt(2))))])],
            r'a) $\mathbb R$ i $[0,+\infty)$; b) mínim en $x=0$, màxim en $x=2$; c) decreix en $(-\infty,0)\cup(2,+\infty)$ i creix en $(0,2)$; d) $x=2\pm\sqrt2$; e) asímptota $y=0$ quan $x\to+\infty$.')

# 64
D64 = x**4 / 4 - 8 * x**2 + 81
ok(sp.expand(x**2 + (18 - x**2 / 2 - 9)**2), D64); ok(I(18 - x**2 / 2, -6, 6), 144)
S[64] = SOL([st('a)', r'$\Gamma$: $y=18-\frac{x^2}{2}$. $$f(x)=\sqrt{x^2+\left(9-\frac{x^2}{2}\right)^2}=\sqrt{\frac{x^4}{4}-8x^2+81},\quad-6\le x\le6$$'),
             st('b)', r"Estudiem $D=f^2$: $D^{\prime}(x)=x^3-16x=x(x-4)(x+4)=0\iff x=0,\pm4$. $D^{\prime}<0$ en $(-6,-4)$ i $(0,4)$, $>0$ en $(-4,0)$ i $(4,6)$: mínims relatius en $x=\pm4$, punts $(\pm4,10)$; màxim relatiu en $x=0$."),
             st('c)', r'$f(\pm4)=\sqrt{17}$, $f(0)=9$, $f(\pm6)=\sqrt{117}=3\sqrt{13}$. Mínim: $\sqrt{17}\approx4{,}12$ (en $(\pm4,10)$); màxim: $3\sqrt{13}\approx10{,}82$ (en $(\pm6,0)$).'),
             st('d)', r'$$A=\int_{-6}^{6}\left(18-\frac{x^2}{2}\right)dx=2\left[18x-\frac{x^3}{6}\right]_0^6=2(108-36)=144\ \text{u}^2$$')],
            r'a) $f(x)=\sqrt{\frac{x^4}{4}-8x^2+81}$; b) $(\pm4,10)$; c) mínim $\sqrt{17}$, màxim $3\sqrt{13}$; d) 144 u².')

# 65
ok(I(4 * x * ln(x), E, E**2), 3 * E**4 - E**2); pri(4 * x * ln(x), 2 * x**2 * ln(x) - x**2)
S[65] = SOL([st('a)', r"$f^{\prime}(x)=4\ln x+4=0\iff\ln x=-1\iff x=\frac1e$; $f^{\prime\prime}(x)=\frac4x>0$: mínim relatiu en $x=\frac1e$."),
             st('b)', r"$f^{\prime}(1)=4$: $y=4(x-1)=4x-4$."),
             st('c)', r'En $[e,e^2]$, $f>0$. Per parts ($u=\ln x$, $dv=4x\,dx$, $v=2x^2$): $\int4x\ln x\,dx=2x^2\ln x-\int2x\,dx=2x^2\ln x-x^2$. $$A=\Big[2x^2\ln x-x^2\Big]_e^{e^2}=(4e^4-e^4)-(2e^2-e^2)=3e^4-e^2$$')],
            r'a) $x=\frac1e$; b) $y=4x-4$; c) $3e^4-e^2\approx%s$ u².' % dd(3 * E**4 - E**2))

# 66
A66 = 12 * x - x**3
ok(solve(diff(A66, x), x), [-2, 2]); ok(A66.subs(x, 2), 16); ok(I(4 - x**2, -2, 2), R(32, 3))
S[66] = SOL([st('a)', r'Base $BC=2x$ (sobre $y=x^2$) i altura $12-x^2$: $T(x)=\frac12\cdot2x(12-x^2)=12x-x^3$, $0<x<\sqrt{12}$.'),
             st('b)', r"$T^{\prime}(x)=12-3x^2=0\iff x=2$; $T^{\prime\prime}(2)=-12<0$: màxim. $B(-2,4)$, $C(2,4)$, àrea 16."),
             st('c)', r'$$S=\int_{-2}^{2}(4-x^2)\,dx=\left[4x-\frac{x^3}{3}\right]_{-2}^{2}=\frac{32}{3}$$'),
             st('d)', r'El triangle queda per damunt de $y=4$ i $S$ per davall: no se superposen. Àrea total $16+\frac{32}{3}=\frac{80}{3}$.'),
             gr([(x**2, [-2, 2]), (12 - 4 * Abs(x), [-2, 2]), (sp.Integer(4), [-2, 2])], xr=(-3.5, 3.5), yr=(-0.5, 13), shade=[(12 - 4 * Abs(x), x**2, -2, 2)], pts=[(0, 12), (-2, 4), (2, 4)])],
            r'a) $12x-x^3$; b) $B(-2,4)$, $C(2,4)$; c) $\frac{32}{3}$; d) $\frac{80}{3}\approx26{,}67$ u².')

# 67
ok(I(-2 * x**2 + 2 * x, 0, 1), R(1, 3))
S[67] = SOL([st('a)', r"$f^{\prime}(x)=-2x+2$: $f$ creix en $(-\infty,1)$ i decreix en $(1,+\infty)$. $g^{\prime}(x)=2x$: $g$ decreix en $(-\infty,0)$ i creix en $(0,+\infty)$."),
             st('b)', r'Màxim relatiu de $f$: $(1,1)$. Mínim relatiu de $g$: $(0,0)$.'),
             st('c)', r'$-x^2+2x=x^2\iff2x(x-1)=0$: punts $(0,0)$ i $(1,1)$.'),
             st('d)', r'$$A=\int_0^1\big(-x^2+2x-x^2\big)dx=\left[-\frac{2x^3}{3}+x^2\right]_0^1=\frac13$$'),
             gr([-x**2 + 2 * x, x**2], xr=(-1, 2.5), yr=(-1, 2), shade=[(-x**2 + 2 * x, x**2, 0, 1)], pts=[(0, 0), (1, 1)])],
            r'b) Màxim de $f$ en $(1,1)$, mínim de $g$ en $(0,0)$; c) $(0,0)$ i $(1,1)$; d) $\frac13$ u².')

# 68
f68 = 4 * pi * x**2 + 400 / x; x68 = (50 / pi)**R(1, 3)
ok(diff(f68, x).subs(x, x68), 0); ok(f68.subs(x, x68), 600 / x68)
S[68] = SOL([st('a)', r'$A_b=\pi x^2$.'),
             st('b)', r'Altura: $\pi x^2h=100\Rightarrow h=\dfrac{100}{\pi x^2}$. $A_l=2\pi xh=\dfrac{200}{x}$.'),
             st('c)', r'$f(x)=4\pi x^2+2\cdot\dfrac{200}{x}=4\pi x^2+\dfrac{400}{x}$, $x>0$.'),
             st('d)', r"$f^{\prime}(x)=8\pi x-\dfrac{400}{x^2}=0\iff x^3=\dfrac{50}{\pi}\iff x=\sqrt[3]{\dfrac{50}{\pi}}\approx%s$ m; $f^{\prime\prime}>0$: mínim. $f\approx%s$ €." % (dd(x68, 3), dd(f68.subs(x, x68))))],
            r'd) $x=\sqrt[3]{50/\pi}\approx%s$ m, amb un cost mínim de $\approx%s$ €.' % (dd(x68), dd(f68.subs(x, x68))))

# 69
S[69] = SOL([st('a)', r'$P\big(x,\sqrt{2x+9}\big)$: $d(x)=\sqrt{x^2+2x+9}$, $-4{,}5\le x\le8$.'),
             st('b)', r"$(d^2)^{\prime}=2x+2=0\iff x=-1$ (mínim, paràbola cap amunt); en els extrems $d(-4{,}5)=4{,}5$ i $d(8)=\sqrt{89}$. $P=(-1,\sqrt7)$."),
             st('c)', r'$d(-1)=\sqrt8=2\sqrt2\approx2{,}83$.')],
            r'b) $P(-1,\sqrt7)$; c) $2\sqrt2\approx2{,}83$.')

# 70
th70 = sp.atan(abs((sqrt(3) / 2 + 2) / (1 - sqrt(3))))
okn(th70 * 180 / pi, 75.67166, 1e-5)
S[70] = SOL([st('a)', r"$f(\frac{\pi}{6})=\frac12$, $f^{\prime}(\frac{\pi}{6})=\cos\frac{\pi}{6}=\frac{\sqrt3}{2}$: $\ y=\frac12+\frac{\sqrt3}{2}\left(x-\frac{\pi}{6}\right)$."),
             st('b)', r"$f(\frac{\pi}{3})=\frac{\sqrt3}{2}$, $f^{\prime}(\frac{\pi}{3})=\frac12$; pendent de la normal $-2$: $\ y=\frac{\sqrt3}{2}-2\left(x-\frac{\pi}{3}\right)$."),
             st('c)', r'Amb $m_1=\frac{\sqrt3}{2}$ i $m_2=-2$: $$\tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|=\frac{\frac{\sqrt3}{2}+2}{\sqrt3-1}=\frac{7+5\sqrt3}{4}\approx3{,}915\Rightarrow\theta\approx75{,}67°$$')],
            r'a) $y=\frac12+\frac{\sqrt3}{2}(x-\frac{\pi}{6})$; b) $y=\frac{\sqrt3}{2}-2(x-\frac{\pi}{3})$; c) $\theta\approx75{,}67°$ (75° 40′).')

# 71
f71 = ln((1 + x) / (1 - x)) / 2; g71 = ln(sqrt((1 - x) / (1 + x)))
der(f71, 1 / (1 - x**2)); der(g71, -1 / (1 - x**2)); okn((f71 + g71).subs(x, R(3, 10)), 0)
S[71] = SOL([st('a)', r"$f(x)=\frac12\big(\ln(1+x)-\ln(1-x)\big)\Rightarrow f^{\prime}(x)=\frac12\left(\frac{1}{1+x}+\frac{1}{1-x}\right)=\frac{1}{1-x^2}$. $\ g(x)=\frac12\big(\ln(1-x)-\ln(1+x)\big)\Rightarrow g^{\prime}(x)=-\frac{1}{1-x^2}$."),
             st('b)', r'Cal $\frac{1+x}{1-x}>0$ (i, per a $g$, $\frac{1-x}{1+x}>0$): totes dues condicions equivalen a $-1<x<1$. Domini $(-1,1)$ per a les dues.'),
             st('c)', r'$g(x)=\frac12\ln\frac{1-x}{1+x}=-\frac12\ln\frac{1+x}{1-x}=-f(x)$, per tant $f(x)+g(x)=0$ per a tot $x\in(-1,1)$. Recorregut: $\{0\}$.')],
            r"a) $f^{\prime}=\frac{1}{1-x^2}$, $g^{\prime}=-\frac{1}{1-x^2}$; b) $(-1,1)$; c) $f+g=0$, recorregut $\{0\}$.")

# 72
f72 = 30 * sqrt(2 * x + 1); R72 = (40 - x) * f72
ok(I(f72, 0, 40), 7280); ok(solve(diff(R72, x), x), [13]); ok(R72.subs(x, 13), 2430 * sqrt(3))
S[72] = SOL([st('a)', r'$$A=\int_0^{40}30\sqrt{2x+1}\,dx=30\left[\frac{(2x+1)^{3/2}}{3}\right]_0^{40}=10\,(81^{3/2}-1)=10(729-1)=7280\ \text{u}^2$$'),
             st('b)', r"$R(x)=(40-x)\cdot30\sqrt{2x+1}$, $0\le x\le40$. $$R^{\prime}(x)=-30\sqrt{2x+1}+\frac{30(40-x)}{\sqrt{2x+1}}=\frac{30(39-3x)}{\sqrt{2x+1}}=0\iff x=13$$ (positiva abans, negativa després: màxim). $f(13)=30\sqrt{27}=90\sqrt3$. Vèrtexs: $(13,0)$, $(13,90\sqrt3)$, $(40,90\sqrt3)$, $(40,0)$."),
             st('c)', r'$R(13)=27\cdot90\sqrt3=2430\sqrt3\approx4208{,}88$ u².')],
            r'a) 7280 u²; b) $(13,0)$, $(13,90\sqrt3)$, $(40,90\sqrt3)$, $(40,0)$; c) $2430\sqrt3\approx4208{,}88$ u².')

# 73
ok(limit((x + 1) * sin(x) / x, x, 0), 1); pri((x + 1) * exp(2 * x), (2 * x + 1) * exp(2 * x) / 4); ok(I((x + 1) * exp(2 * x), 0, 1), (3 * E**2 - 1) / 4)
S[73] = SOL([st('a)', r'$f(0)=m$; $\displaystyle\lim_{x\to0^-}f=m$; $\displaystyle\lim_{x\to0^+}\frac{(x+1)\sin x}{x}=1\cdot1=1$ ($\frac{\sin x}{x}\to1$). Contínua $\iff m=1$.'),
             st('b)', r"$h(x)=(x+1)e^{2x}$, $h^{\prime}(x)=e^{2x}+2(x+1)e^{2x}=(2x+3)e^{2x}$: decreix en $(-\infty,-\frac32)$ i creix en $(-\frac32,+\infty)$ (mínim en $x=-\frac32$)."),
             st('c) Per parts.', r'$u=x+1$, $dv=e^{2x}dx$, $v=\frac12e^{2x}$: $$\int(x+1)e^{2x}dx=\frac{(x+1)e^{2x}}{2}-\int\frac{e^{2x}}{2}dx=\frac{(2x+1)e^{2x}}{4}+C$$ En $[0,1]$ la funció és positiva: $A=\left[\frac{(2x+1)e^{2x}}{4}\right]_0^1=\frac{3e^2-1}{4}$.')],
            r'a) $m=1$; b) decreix en $(-\infty,-\frac32)$, creix en $(-\frac32,+\infty)$; c) $\frac{(2x+1)e^{2x}}{4}+C$ i $A=\frac{3e^2-1}{4}\approx%s$ u².' % dd((3 * E**2 - 1) / 4))

# 74
A74 = (80 - x) * (60 + x)
ok(solve(diff(A74, x), x), [10]); ok(A74.subs(x, 10), 4900)
S[74] = SOL([st('a)', r'El segment $AB$ és $x+y=20$, així que $P(x,20-x)$. $R$ té costats $80-x$ i $80-y=60+x$: $$S(x)=(80-x)(60+x)=4800+20x-x^2,\quad0\le x\le20$$'),
             st('b)', r"$S^{\prime}(x)=20-2x=0\iff x=10$; $S^{\prime\prime}=-2<0$. Als extrems $S(0)=S(20)=4800$."),
             st('c)', r'$S(10)=70\cdot70=4900$ cm².')],
            r'a) $S(x)=4800+20x-x^2$; b) $x=10$; c) 4900 cm² (un quadrat de 70 cm).')

# 75
f75 = x * exp(x) - 3 * x
ok(I(f75, 0, ln(3)), 3 * ln(3) - 2 - R(3, 2) * ln(3)**2)
S[75] = SOL([st('a)', r'$f(x)=x(e^x-3)=0\iff x=0$ o $x=\ln3$. Punts $(0,0)$ i $(\ln3,0)$.'),
             st('b)', r"$f^{\prime}(x)=(x+1)e^x-3$, $f^{\prime\prime}(x)=(x+2)e^x=0\iff x=-2$, on canvia de signe: punt d’inflexió $\left(-2,\,6-\frac{2}{e^2}\right)$. Per a $x>-2$, $f^{\prime\prime}>0$ i $f^{\prime}$ creix; per tant, si $x>2$: $f^{\prime}(x)>f^{\prime}(2)=3e^2-3>0$ i $f$ és creixent."),
             st('c)', r'En $[0,\ln3]$, $e^x\le3$ i $f\le0$. Per parts, $\int xe^x\,dx=(x-1)e^x$: $$\int_0^{\ln3}(xe^x-3x)dx=\left[(x-1)e^x-\frac{3x^2}{2}\right]_0^{\ln3}=3\ln3-2-\frac32(\ln3)^2\approx-0{,}515$$ L’àrea és el valor absolut.'),
             gr([f75], xr=(-3.5, 2), yr=(-1.2, 7), shade=[(f75, None, 0, math.log(3))], pts=[(0, 0), (math.log(3), 0), (-2, 6 - 2 / math.e**2)])],
            r'a) $(0,0)$ i $(\ln3,0)$; b) inflexió en $\left(-2,6-\frac2{e^2}\right)$; c) $A=2+\frac32(\ln3)^2-3\ln3\approx%s$ u².' % dd(2 + R(3, 2) * ln(3)**2 - 3 * ln(3), 3))

# 76
T76 = (60 + x) * (800 - 10 * x)
ok(T76.subs(x, 1), 48190); ok(T76.subs(x, 10), 49000); ok(T76.subs(x, 20), 48000); ok(solve(diff(T76, x), x), [10])
S[76] = SOL([st('a)', r'61 passatgers: $61\cdot790=48190$ €; 70: $70\cdot700=49000$ €; 80: $80\cdot600=48000$ €.'),
             st('b)', r'$T(x)=(60+x)(800-10x)=48000+200x-10x^2$, $0\le x\le20$.'),
             st('c)', r"$T^{\prime}(x)=200-20x=0\iff x=10$; $T^{\prime\prime}=-20<0$: màxim, $T(10)=49000$ €.")],
            r'a) 48190, 49000 i 48000 €; b) $T(x)=(60+x)(800-10x)$; c) 70 passatgers (49000 €).')

# 77
ok(I(-2 * (x - 1) * (x - 3), 1, 3), R(8, 3)); ok(I((x - 1) * (x - 3), 0, 1), R(4, 3))
S[77] = SOL([st('a)', r"$f(x)=x^2-4x+3$, $f^{\prime}(x)=2x-4$: decreix en $(-\infty,2)$ i creix en $(2,+\infty)$."),
             st('b)', r'Les dues corbes es tallen en $x=1$ i $x=3$; entre elles $f<0$ i $-f>0$: $$A=\int_1^3\big(-f-f\big)dx=-2\int_1^3(x^2-4x+3)\,dx=-2\left[\frac{x^3}{3}-2x^2+3x\right]_1^3=-2\left(0-\frac43\right)=\frac83$$'),
             st('c)', r'En $[0,1]$, $(x-1)(x-3)\ge0$, i amb $a>0$: $$\int_0^1a(x^2-4x+3)\,dx=a\left(\frac13-2+3\right)=\frac{4a}{3}=\frac43\iff a=1$$'),
             gr([(x - 1) * (x - 3), -(x - 1) * (x - 3)], xr=(-0.5, 4.5), yr=(-3.5, 3.5), shade=[(-(x - 1) * (x - 3), (x - 1) * (x - 3), 1, 3)])],
            r'a) Decreix en $(-\infty,2)$ i creix en $(2,+\infty)$; b) $\frac83$ u²; c) $a=1$.')

# 78
D78 = x**2 + (x**2 / 4 - 4)**2
ok(sp.expand(D78), x**4 / 16 - x**2 + 16); ok(D78.subs(x, 2 * sqrt(2)), 12); ok(D78.subs(x, 6), 61)
S[78] = SOL([st('a)', r'$P\left(x,\frac{x^2}{4}\right)$: $d(x)=\sqrt{x^2+\left(\frac{x^2}{4}-4\right)^2}=\sqrt{\frac{x^4}{16}-x^2+16}$, $-6\le x\le6$.'),
             st('b)', r"$D=d^2$: $D^{\prime}(x)=\frac{x^3}{4}-2x=\frac x4(x^2-8)=0\iff x=0,\ \pm2\sqrt2$. $D(0)=16$, $D(\pm2\sqrt2)=12$, $D(\pm6)=61$. Mínim en $(\pm2\sqrt2,\,2)$, a distància $2\sqrt3\approx3{,}46$."),
             st('c)', r'El màxim és en els extrems del tram: $(\pm6,\,9)$, a distància $\sqrt{61}\approx7{,}81$.')],
            r'b) $(2\sqrt2,2)$ i $(-2\sqrt2,2)$; c) $(6,9)$ i $(-6,9)$.')

# 79
f79 = x / (x + 1)**2
ok(sp.factor(diff(f79, x)), -(x - 1) / (x + 1)**3); pri(f79, ln(x + 1) + 1 / (x + 1))
S[79] = SOL([st('a)', r'Domini $\mathbb R\setminus\{-1\}$. $\displaystyle\lim_{x\to-1}\frac{x}{(x+1)^2}=\frac{-1}{0^+}=-\infty$: asímptota vertical $x=-1$. Grau del numerador menor: asímptota horitzontal $y=0$.'),
             st('b)', r"$$f^{\prime}(x)=\frac{(x+1)^2-2x(x+1)}{(x+1)^4}=\frac{1-x}{(x+1)^3}$$" + taula_m([(r'(-\infty,-1)', '-'), (r'(-1,1)', '+'), (r'(1,+\infty)', '-')]) + r'Màxim relatiu en $\left(1,\frac14\right)$.'),
             st('c)', r'$\dfrac{x}{(x+1)^2}=\dfrac{(x+1)-1}{(x+1)^2}=\dfrac{1}{x+1}-\dfrac{1}{(x+1)^2}$: $$\int f(x)\,dx=\ln|x+1|+\frac{1}{x+1}+C$$')],
            r'a) $x=-1$ i $y=0$; b) decreix en $(-\infty,-1)\cup(1,+\infty)$ i creix en $(-1,1)$; c) $\ln|x+1|+\frac{1}{x+1}+C$.')

# 80
C80 = 15 * x**2 + 30000 / x
ok([s_ for s_ in solve(diff(C80, x), x) if s_.is_real], [10]); ok(C80.subs(x, 10), 4500)
S[80] = SOL([st('a)', r'Altura $h=\dfrac{1500}{x^2}$. $C(x)=15x^2+5\cdot4xh=15x^2+\dfrac{30000}{x}$, $x>0$.'),
             st('b)', r"$C^{\prime}(x)=30x-\dfrac{30000}{x^2}=0\iff x^3=1000\iff x=10$ m; $C^{\prime\prime}>0$: mínim. $h=15$ m."),
             st('c)', r'$C(10)=1500+3000=4500$ €.')],
            r'a) $C(x)=15x^2+\frac{30000}{x}$; b) costat 10 m i altura 15 m; c) 4500 €.')

# 81
f81 = 1 / (x**2 - 5 * x + 6)
pri(f81, ln(x - 3) - ln(x - 2), at=(R(7, 2), R(9, 2))); ok(I(f81, 4, 6), ln(R(3, 2)))
S[81] = SOL([st('a)', r'$x^2-5x+6=(x-2)(x-3)$: domini $\mathbb R\setminus\{2,3\}$; asímptotes verticals $x=2$ i $x=3$ i horitzontal $y=0$.'),
             st('b)', r"$f^{\prime}(x)=-\dfrac{2x-5}{(x^2-5x+6)^2}$: creix en $(-\infty,2)\cup\left(2,\frac52\right)$ i decreix en $\left(\frac52,3\right)\cup(3,+\infty)$. Màxim relatiu en $\left(\frac52,-4\right)$."),
             st('c)', r'$\dfrac{1}{(x-2)(x-3)}=\dfrac{-1}{x-2}+\dfrac{1}{x-3}$: $\displaystyle\int f(x)\,dx=\ln\left|\frac{x-3}{x-2}\right|+C$.'),
             st('d)', r'Per a $x>3$, $f>0$: $$\left[\ln\frac{x-3}{x-2}\right]_4^a=\ln\frac{a-3}{a-2}-\ln\frac12=\ln\frac{2(a-3)}{a-2}=\ln\frac32\iff4(a-3)=3(a-2)\iff a=6$$')],
            r'a) $x=2$, $x=3$, $y=0$; b) creix en $(-\infty,2)\cup(2,\frac52)$, decreix en $(\frac52,3)\cup(3,+\infty)$; c) $\ln\left|\frac{x-3}{x-2}\right|+C$; d) $a=6$.')

# 82
I82 = 300 * x + 900 * (23 - 5 * x) / (10 - x)
ok(solve(diff(I82, x), x), [1, 19]); ok(I82.subs(x, 1), 2100)
S[82] = SOL([st('a)', r'$I(x)=300x+900\cdot\dfrac{23-5x}{10-x}$, $0<x<\frac{23}{5}$.'),
             st('b)', r"$$I^{\prime}(x)=300+900\cdot\frac{-5(10-x)+(23-5x)}{(10-x)^2}=300-\frac{24300}{(10-x)^2}=0\iff(10-x)^2=81\iff x=1$$ ($x=19$ queda fora). $I^{\prime}>0$ si $x<1$ i $<0$ si $x>1$: màxim. $y=\frac{18}{9}=2$."),
             st('c)', r'$I(1)=300+1800=2100$ €.')],
            r'b) 1 tona de qualitat baixa i 2 d’alta; c) 2100 €.')

# 83
ok(I(x**2 - x, -1, 0), R(5, 6)); ok(I(x**2 + x, 0, 2), R(14, 3))
S[83] = SOL([st('a)', r'$x^2+|x|=0\iff x=0$ (suma de dos termes no negatius). Només talla els eixos en $(0,0)$.'),
             st('b)', r'$f(-x)=(-x)^2+|-x|=x^2+|x|=f(x)$: és parella, simètrica respecte a l’eix OY.'),
             st('c)', r"$f(x)=x^2-x$ si $x<0$ i $x^2+x$ si $x\ge0$. Per a $x<0$: $f^{\prime}=2x-1<0$ (decreix); per a $x>0$: $f^{\prime}=2x+1>0$ (creix). En $x=0$ hi ha un mínim relatiu (i absolut), $f(0)=0$, en què la funció no és derivable (derivades laterals $-1$ i $1$)."),
             st('d)', gr([x**2 + Abs(x)], xr=(-2.5, 2.5), yr=(-0.5, 6), pts=[(0, 0)])),
             st('e)', r'$$\int_{-1}^0(x^2-x)\,dx=\left[\frac{x^3}{3}-\frac{x^2}{2}\right]_{-1}^0=\frac13+\frac12=\frac56,\qquad\int_0^2(x^2+x)\,dx=\frac83+2=\frac{14}{3}$$')],
            r'a) $(0,0)$; c) decreix en $(-\infty,0)$, creix en $(0,+\infty)$, mínim en $(0,0)$; e) $\frac56$ i $\frac{14}{3}$.')

# 84
P84 = x * (-x**2 - x + 6)
x84 = (sqrt(19) - 1) / 3
ok(diff(P84, x).subs(x, x84), 0); ok(I(-x**2 - x + 6, 0, 2), R(22, 3))
S[84] = SOL([st('a)', r'$f(x)=-x^2-x+6=-(x+3)(x-2)$: paràbola cap avall, vèrtex $\left(-\frac12,\frac{25}{4}\right)$. Per a $x=0$, $y=6$; $y=0$ per a $x=2$ (l’altre zero, $-3$, és fora de $[0,2]$).'),
             gr([(-x**2 - x + 6, [0, 2])], xr=(-0.5, 2.5), yr=(-0.5, 7), shade=[(-x**2 - x + 6, None, 0, 2)], pts=[(0, 6), (2, 0)]),
             st('b)', r"$P(x)=xy=-x^3-x^2+6x$; $P^{\prime}(x)=-3x^2-2x+6=0\iff x=\dfrac{-1+\sqrt{19}}{3}\approx1{,}12$ (l’altra és negativa); $P^{\prime\prime}=-6x-2<0$: màxim."),
             st('c)', r'$$A=\int_0^2(-x^2-x+6)\,dx=\left[-\frac{x^3}{3}-\frac{x^2}{2}+6x\right]_0^2=-\frac83-2+12=\frac{22}{3}$$')],
            r'a) $y=6$ i $x=2$; b) $x=\frac{\sqrt{19}-1}{3}\approx1{,}12$; c) $\frac{22}{3}$ u².')

# 85
C85 = 10 * sqrt(x**2 + 36) + 5 * (18 - x)
ok(pos(diff(C85, x)), [2 * sqrt(3)]); ok(C85.subs(x, 2 * sqrt(3)), 90 + 30 * sqrt(3))
S[85] = SOL([st('a)', r'$MP=\sqrt{x^2+36}$ i $PN=18-x$: $C(x)=10\sqrt{x^2+36}+5(18-x)$, $0\le x\le18$.'),
             st('b)', r"$C^{\prime}(x)=\dfrac{10x}{\sqrt{x^2+36}}-5=0\iff2x=\sqrt{x^2+36}\iff3x^2=36\iff x=2\sqrt3\approx3{,}46$ m. Comparant: $C(0)=150$, $C(18)=10\sqrt{360}\approx189{,}74$."),
             st('c)', r'$C(2\sqrt3)=10\cdot4\sqrt3+90-10\sqrt3=90+30\sqrt3\approx141{,}96$ €.')],
            r'b) $x=2\sqrt3\approx3{,}46$ m; c) $90+30\sqrt3\approx141{,}96$ €.')

# 86
ok(I(x + 1 / x, 1, E), (E**2 + 1) / 2)
S[86] = SOL([st('a)', r"$f(x)=x+\frac1x$, $f^{\prime}(x)=1-\frac{1}{x^2}=\frac{x^2-1}{x^2}$: creix en $(-\infty,-1)\cup(1,+\infty)$ i decreix en $(-1,0)\cup(0,1)$. Màxim relatiu $(-1,-2)$ i mínim relatiu $(1,2)$."),
             st('b)', r'Vertical $x=0$ ($\lim_{x\to0^\pm}f=\pm\infty$). Obliqua: $f(x)-x=\frac1x\to0$: $y=x$.'),
             st('c)', r'En $[1,e]$, $f>0$: $A=\displaystyle\int_1^e\left(x+\frac1x\right)dx=\left[\frac{x^2}{2}+\ln x\right]_1^e=\frac{e^2}{2}+1-\frac12=\frac{e^2+1}{2}$.'),
             gr([x + 1 / x], xr=(-4, 4), yr=(-6, 6), va=(0,), ob=(lambda v: v,), shade=[(x + 1 / x, None, 1, math.e)], pts=[(-1, -2), (1, 2)])],
            r'a) Màxim $(-1,-2)$, mínim $(1,2)$; b) $x=0$ i $y=x$; c) $\frac{e^2+1}{2}\approx%s$ u².' % dd((E**2 + 1) / 2))

# 87
ok(I(a * x - x**3, 0, sqrt(a)), a**2 / 4)
S[87] = SOL([st('a)', r"$f(x)=x(x^2-a)$: talla els eixos en $(0,0)$ i $(\pm\sqrt a,0)$. $f^{\prime}(x)=3x^2-a=0\iff x=\pm\sqrt{a/3}$: creix en $(-\infty,-\sqrt{a/3})\cup(\sqrt{a/3},+\infty)$ i decreix en $(-\sqrt{a/3},\sqrt{a/3})$."),
             st('b)', r'$a=9$: zeros $0,\pm3$; màxim $(-\sqrt3,6\sqrt3)$, mínim $(\sqrt3,-6\sqrt3)$, inflexió $(0,0)$.' + gr([x**3 - 9 * x], xr=(-4, 4), yr=(-14, 14), pts=[(-3, 0), (0, 0), (3, 0), (-math.sqrt(3), 6 * math.sqrt(3)), (math.sqrt(3), -6 * math.sqrt(3))])),
             st('c)', r'En el primer quadrant es tallen en $x=0$ i $x=\sqrt a$, i $ax\ge x^3$ entre ells: $$A(a)=\int_0^{\sqrt a}(ax-x^3)\,dx=\left[\frac{ax^2}{2}-\frac{x^4}{4}\right]_0^{\sqrt a}=\frac{a^2}{2}-\frac{a^2}{4}=\frac{a^2}{4}$$'),
             st('d)', r'$\int_0^2x^3dx=4$: $\frac{a^2}{4}=4\iff a=4$.')],
            r'c) $\frac{a^2}{4}$; d) $a=4$.')

# 88
A88 = x / 2 * sqrt(900 - 60 * x)
ok(pos(diff(A88, x)), [10]); ok(A88.subs(x, 10), 50 * sqrt(3))
S[88] = SOL([st('a)', r'$OA=\sqrt{x^2+y^2}$ i $AB=x$: $\sqrt{x^2+y^2}=30-x\Rightarrow y^2=900-60x$, $0<x<15$. El triangle és rectangle en $B$: $$A(x)=\frac{x\,y}{2}=\frac x2\sqrt{900-60x}$$'),
             st('b)', r"Maximitzem $A^2=225x^2-15x^3$: $(A^2)^{\prime}=450x-45x^2=0\iff x=10$; positiva abans i negativa després: màxim."),
             st('c)', r'$y=\sqrt{300}=10\sqrt3$ i $A(10)=5\cdot10\sqrt3=50\sqrt3\approx86{,}6$ m².')],
            r'a) $A(x)=\frac x2\sqrt{900-60x}$; b) $x=10$ m; c) $50\sqrt3\approx86{,}60$ m².')

# 89
ok(I(1 / (x**2 - x), 2, 3), ln(R(4, 3)))
S[89] = SOL([st('a)', r'$x^2-x=x(x-1)$: domini $\mathbb R\setminus\{0,1\}$; asímptotes verticals $x=0$, $x=1$ i horitzontal $y=0$.'),
             st('b)', r"$f^{\prime}(x)=-\dfrac{2x-1}{(x^2-x)^2}$: creix en $(-\infty,0)\cup\left(0,\frac12\right)$ i decreix en $\left(\frac12,1\right)\cup(1,+\infty)$ (màxim relatiu $(\frac12,-4)$)."),
             st('c)', r'En $[2,3]$, $f>0$. $\frac{1}{x(x-1)}=\frac{1}{x-1}-\frac1x$: $$A=\Big[\ln(x-1)-\ln x\Big]_2^3=\ln\frac23-\ln\frac12=\ln\frac43$$')],
            r'a) $x=0$, $x=1$, $y=0$; b) creix en $(-\infty,0)\cup(0,\frac12)$, decreix en $(\frac12,1)\cup(1,+\infty)$; c) $\ln\frac43\approx0{,}29$ u².')

# 90
S90 = sqrt(3) * x**2 / 36 + (100 - x)**2 / 16; x90 = 900 / (9 + 4 * sqrt(3))
ok(diff(S90, x).subs(x, x90), 0); okn(S90.subs(x, x90), 271.85282, 1e-6)
S[90] = SOL([st('a)', r'Costat del triangle $\frac x3$ i del quadrat $\frac{100-x}{4}$: $$S(x)=\frac{\sqrt3}{4}\left(\frac x3\right)^2+\left(\frac{100-x}{4}\right)^2=\frac{\sqrt3\,x^2}{36}+\frac{(100-x)^2}{16}$$'),
             st('b)', r"$S^{\prime}(x)=\frac{\sqrt3\,x}{18}-\frac{100-x}{8}=0\iff x\left(\frac{\sqrt3}{18}+\frac18\right)=\frac{100}{8}\iff x=\frac{900}{9+4\sqrt3}\approx%s$ cm. $S^{\prime\prime}>0$: és el mínim, $S\approx%s$ cm²." % (dd(x90), dd(S90.subs(x, x90)))),
             st('c)', r'El màxim d’una funció contínua en $[0,100]$ amb només un mínim relatiu està en un extrem: $S(0)=625$, $S(100)=\frac{10000\sqrt3}{36}\approx481{,}13$. Màxim en $x=0$: tot el filferro s’usa per al quadrat (no es fa triangle).')],
            r'b) $x=\frac{900}{9+4\sqrt3}\approx%s$ cm; c) $x=0$ (només quadrat, 625 cm²).' % dd(x90))
