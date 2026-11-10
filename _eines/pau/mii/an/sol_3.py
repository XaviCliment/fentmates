# Solucions dels exercicis PAU d'anàlisi de 2n Batx MII (recull de l'IES Vermellar), números 91-128.
from mlib import *  # noqa: F401,F403

S = {}

# 91
f91 = a * x**3 + b * x**2 + c * x * cos(pi * x)
ok(f91.subs(x, 1), a + b - c); ok(diff(f91, x).subs(x, 1), 3 * a + 2 * b - c); ok(I(x * cos(pi * x), 0, 1), -2 / pi**2)
S[91] = SOL([st('a)', r'$f(1)=a+b+c\cos\pi=a+b-c=22$.'),
             st('b)', r"$f^{\prime}(x)=3ax^2+2bx+c\cos(\pi x)-c\pi x\sin(\pi x)$. Tangent horitzontal en $x=1$: $f^{\prime}(1)=3a+2b-c=0$."),
             st('c) Per parts.', r'$u=x$, $dv=\cos(\pi x)dx$, $v=\frac{\sin(\pi x)}{\pi}$: $$\int_0^1x\cos(\pi x)dx=\left[\frac{x\sin(\pi x)}{\pi}\right]_0^1-\int_0^1\frac{\sin(\pi x)}{\pi}dx=0+\left[\frac{\cos(\pi x)}{\pi^2}\right]_0^1=\frac{-1-1}{\pi^2}=-\frac{2}{\pi^2}$$')],
            r'a) $a+b-c=22$; b) $3a+2b-c=0$; c) $-\frac{2}{\pi^2}$.')

# 92
A92 = (x + 4) * (600 / x + 6)
ok(pos(diff(A92, x)), [20]); ok(A92.subs(x, 20), 864)
S[92] = SOL([st('a)', r'$R$ fa $x\times\frac{600}{x}$; la cartolina, $(x+4)\times\left(\frac{600}{x}+6\right)$: $$A(x)=(x+4)\left(\frac{600}{x}+6\right)=624+6x+\frac{2400}{x},\quad x>0$$'),
             st('b)', r"$A^{\prime}(x)=6-\dfrac{2400}{x^2}=0\iff x=20$ cm; $A^{\prime\prime}>0$: mínim."),
             st('c)', r'Cartolina de $24\times36$ cm (864 cm²), amb $R$ de $20\times30$ cm.')],
            r'a) $A(x)=624+6x+\frac{2400}{x}$; b) $x=20$ cm; c) $24$ cm $\times$ $36$ cm.')

# 93
f93 = x * exp(-x**2)
ok(sp.factor(diff(f93, x)), -(2 * x**2 - 1) * exp(-x**2)); pri(f93, -exp(-x**2) / 2); pri(x * exp(-x), -(x + 1) * exp(-x))
ok(solve(sp.Eq(f93.subs(x, 0), f93.subs(x, 1) + a), a), [-exp(-1)])
S[93] = SOL([st('a) Asímptotes.', r'Domini $\mathbb R$ (no hi ha verticals). $\displaystyle\lim_{x\to\pm\infty}\frac{x}{e^{x^2}}=0$: asímptota horitzontal $y=0$.'),
             st('Monotonia.', r"$f^{\prime}(x)=(1-2x^2)e^{-x^2}=0\iff x=\pm\frac{\sqrt2}{2}$." + taula_m([(r'(-\infty,-\frac{\sqrt2}{2})', '-'), (r'(-\frac{\sqrt2}{2},\frac{\sqrt2}{2})', '+'), (r'(\frac{\sqrt2}{2},+\infty)', '-')]) +
                r'Mínim $\left(-\frac{\sqrt2}{2},-\frac{1}{\sqrt{2e}}\right)$ i màxim $\left(\frac{\sqrt2}{2},\frac{1}{\sqrt{2e}}\right)$, amb $\frac{1}{\sqrt{2e}}\approx0{,}43$.'),
             st('b)', r'És senar (simètrica respecte a l’origen) i passa per $(0,0)$.' + gr([f93], xr=(-3.5, 3.5), yr=(-0.6, 0.6), pts=[(0, 0), (math.sqrt(0.5), 1 / math.sqrt(2 * math.e)), (-math.sqrt(0.5), -1 / math.sqrt(2 * math.e))])),
             st('c)', r'$g$ és contínua i derivable en $\mathbb R$; Rolle exigeix $g(0)=g(1)$: $0=e^{-1}+a\iff a=-\frac1e$.'),
             st('d)', r'$\int xe^{-x^2}dx=-\frac12\int-2xe^{-x^2}dx=-\frac12e^{-x^2}+C$. Per parts ($u=x$, $dv=e^{-x}dx$): $\int xe^{-x}dx=-xe^{-x}+\int e^{-x}dx=-(x+1)e^{-x}+C$.')],
            r'a) $y=0$; decreix en $(-\infty,-\frac{\sqrt2}{2})\cup(\frac{\sqrt2}{2},+\infty)$, creix en $(-\frac{\sqrt2}{2},\frac{\sqrt2}{2})$; c) $a=-\frac1e$; d) $-\frac12e^{-x^2}+C$ i $-(x+1)e^{-x}+C$.')

# 94
f94 = sqrt((30 * t)**2 + (250 - 40 * t)**2)
ok(sp.expand(f94**2), 2500 * t**2 - 20000 * t + 62500); ok(f94.subs(t, 4), 150); ok(f94.subs(t, R(25, 4)), R(375, 2))
S[94] = SOL([st('a)', r'Al cap de $t$ hores: $A=(0,30t)$ i $B=(250-40t,0)$. $$f(t)=\sqrt{(30t)^2+(250-40t)^2}=\sqrt{2500t^2-20000t+62500}=50\sqrt{t^2-8t+25}$$'),
             st('b)', r"$A$ arriba a $\left(0,\frac{375}{2}\right)$ en $\frac{187{,}5}{30}=6{,}25$ h i $B$ a l’origen en $\frac{250}{40}=6{,}25$ h: $T=6{,}25$ h. $f^{\prime}(t)=\dfrac{50(t-4)}{\sqrt{t^2-8t+25}}$: decreix en $[0,4)$ i creix en $(4;\,6{,}25]$."),
             st('c)', r'Mínim en $t=4$ h: $f(4)=50\cdot3=150$ km. Extrems: $f(0)=250$ km, $f(6{,}25)=187{,}5$ km. Màxim en $t=0$: 250 km.')],
            r'b) $T=6{,}25$ h; decreix en $[0,4)$ i creix en $(4;6{,}25]$; c) mínim 150 km ($t=4$ h) i màxim 250 km ($t=0$).')

# 95
h95 = (x**3 + x**2 + 5 * x - 3) / (x**2 + 2 * x + 5)
ok(sp.apart(h95, x), x - 1 + (2 * x + 2) / (x**2 + 2 * x + 5)); ok(I(h95, 1, 5), 8 + ln(5)); ok(limit(h95, x, 0), R(-3, 5))
S[95] = SOL([st('a)', r'$x^2+2x+5=0$ no té solucions reals ($\Delta=-16$): domini $\mathbb R$. $\displaystyle\lim_{x\to+\infty}h(x)=+\infty$ (grau 3 sobre grau 2) i $\displaystyle\lim_{x\to0}h(x)=h(0)=-\frac35$.'),
             st('b)', r'Dividint: $h(x)=x-1+\dfrac{2x+2}{x^2+2x+5}$. L’últim terme tendeix a 0: asímptota obliqua $y=x-1$ (no n’hi ha d’altres).'),
             st('c)', r'Com que $(x^2+2x+5)^{\prime}=2x+2$: $$\int h(x)\,dx=\frac{x^2}{2}-x+\ln(x^2+2x+5)+C$$ En $[1,5]$ el numerador $x^3+x^2+5x-3$ és creixent i $h(1)=\frac12>0$: $h>0$. $$A=\left[\frac{x^2}{2}-x+\ln(x^2+2x+5)\right]_1^5=\left(\frac{15}{2}+\ln40\right)-\left(-\frac12+\ln8\right)=8+\ln5$$')],
            r'a) $\mathbb R$; $+\infty$ i $-\frac35$; b) $y=x-1$; c) $\frac{x^2}{2}-x+\ln(x^2+2x+5)+C$ i $A=8+\ln5\approx9{,}61$ u².')

# 96
ok(I(2 + x - x**2, 0, 2) * 2, R(20, 3))
S[96] = SOL([st('a)', r'$d(x)=\sqrt{x^2+(4-x^2-2)^2}=\sqrt{x^4-3x^2+4}$, $-2\le x\le2$.'),
             st('b) i c)', r"Amb $D=d^2$: $D^{\prime}(x)=4x^3-6x=2x(2x^2-3)=0\iff x=0,\ \pm\sqrt{\tfrac32}$. $D(0)=4$, $D\left(\pm\sqrt{\tfrac32}\right)=\frac74$, $D(\pm2)=8$. Màxim absolut en $(\pm2,0)$, $d=2\sqrt2$; mínim absolut en $\left(\pm\frac{\sqrt6}{2},\frac52\right)$, $d=\frac{\sqrt7}{2}$."),
             st('d)', r'$(4-x^2)-(2-|x|)=2+|x|-x^2=(2-|x|)(1+|x|)\ge0$ en $[-2,2]$, i el recinte és simètric: $$A=2\int_0^2(2+x-x^2)\,dx=2\left[2x+\frac{x^2}{2}-\frac{x^3}{3}\right]_0^2=2\cdot\frac{10}{3}=\frac{20}{3}$$'),
             gr([(4 - x**2, [-2, 2]), (2 - Abs(x), [-2, 2])], xr=(-2.6, 2.6), yr=(-0.4, 4.4), shade=[(4 - x**2, 2 - Abs(x), -2, 2)], pts=[(0, 2)])],
            r'b) $(2,0)$ i $(-2,0)$; c) $\left(\pm\frac{\sqrt6}{2},\frac52\right)$; d) $\frac{20}{3}$ u².')

# 97
f97 = (x**2 + 1) / (x**2 * (x - 1)); F97 = -ln(x) + 1 / x + 2 * ln(x - 1) + ln(2) - R(1, 2)
ok(sp.apart(f97, x), -1 / x - 1 / x**2 + 2 / (x - 1)); pri(f97, F97, at=(R(5, 2), R(7, 2))); ok(F97.subs(x, 2), 0); ok(I(f97, 2, 4), 2 * ln(3) - ln(2) - R(1, 4))
S[97] = SOL([st('a)', r'Domini $\mathbb R\setminus\{0,1\}$. $\displaystyle\lim_{x\to0}f=\frac{1}{0^+\cdot(-1)}=-\infty$ i $\displaystyle\lim_{x\to1^\pm}f=\pm\infty$: asímptotes verticals $x=0$ i $x=1$. Grau 2 sobre grau 3: horitzontal $y=0$.'),
             st('b) Fraccions simples.', r'$\dfrac{x^2+1}{x^2(x-1)}=\dfrac Ax+\dfrac{B}{x^2}+\dfrac{C}{x-1}$: $x=1\Rightarrow C=2$; $x=0\Rightarrow B=-1$; coeficient de $x^2$: $A+C=1\Rightarrow A=-1$. $$\int f(x)\,dx=-\ln|x|+\frac1x+2\ln|x-1|+C$$ Passa per $(2,0)$: $-\ln2+\frac12+C=0\Rightarrow C=\ln2-\frac12$.'),
             st('c)', r'En $[2,4]$, $f>0$: $$A=\left[-\ln x+\frac1x+2\ln(x-1)\right]_2^4=\left(-\ln4+\frac14+2\ln3\right)-\left(-\ln2+\frac12\right)=2\ln3-\ln2-\frac14$$')],
            r'a) $x=0$, $x=1$, $y=0$; b) $-\ln|x|+\frac1x+2\ln|x-1|+\ln2-\frac12$; c) $\ln\frac92-\frac14\approx%s$ u².' % dd(2 * ln(3) - ln(2) - R(1, 4)))

# 98
A98 = x / 4 * sqrt(400 - x**2)
ok(pos(diff(A98, x)), [10 * sqrt(2)]); ok(A98.subs(x, 10 * sqrt(2)), 50)
S[98] = SOL([st('a)', r'L’altura sobre el costat $x$ és $\sqrt{100-\frac{x^2}{4}}$: $A(x)=\frac x2\sqrt{100-\frac{x^2}{4}}=\frac x4\sqrt{400-x^2}$.'),
             st('b)', r"$A^{\prime}(x)=\frac14\left(\sqrt{400-x^2}-\frac{x^2}{\sqrt{400-x^2}}\right)=\frac{400-2x^2}{4\sqrt{400-x^2}}$: creix en $[0,10\sqrt2)$ i decreix en $(10\sqrt2,20]$."),
             st('c)', r'Màxim en $x=10\sqrt2\approx14{,}14$ cm (triangle rectangle isòsceles): $A=\frac{10\sqrt2}{4}\sqrt{200}=50$ cm².')],
            r'b) Creix en $[0,10\sqrt2)$, decreix en $(10\sqrt2,20]$; c) $x=10\sqrt2$ cm i $A=50$ cm².')

# 99
f99 = x / sqrt(x**2 - 1)
der(f99, -1 / (x**2 - 1)**R(3, 2), x); ok(I(f99, 2, 3), 2 * sqrt(2) - sqrt(3))
S[99] = SOL([st('a)', r'Cal $x^2-1>0$: domini $(-\infty,-1)\cup(1,+\infty)$. $\displaystyle\lim_{x\to1^+}f=+\infty$, $\displaystyle\lim_{x\to-1^-}f=-\infty$: verticals $x=\pm1$. $\displaystyle\lim_{x\to+\infty}\frac{x}{\sqrt{x^2-1}}=1$ i $\displaystyle\lim_{x\to-\infty}=-1$: horitzontals $y=1$ (per la dreta) i $y=-1$ (per l’esquerra).'),
             st('b)', r"$$f^{\prime}(x)=\frac{\sqrt{x^2-1}-\frac{x^2}{\sqrt{x^2-1}}}{x^2-1}=\frac{-1}{(x^2-1)^{3/2}}<0$$ Decreix en $(-\infty,-1)$ i en $(1,+\infty)$; no té extrems. És senar." + gr([f99], xr=(-5, 5), yr=(-5, 5), va=(-1, 1), ha=(-1, 1))),
             st('c)', r'$\displaystyle\int_2^3\frac{x}{\sqrt{x^2-1}}dx=\Big[\sqrt{x^2-1}\Big]_2^3=\sqrt8-\sqrt3=2\sqrt2-\sqrt3$.')],
            r'a) $(-\infty,-1)\cup(1,+\infty)$; $x=\pm1$, $y=1$ i $y=-1$; b) decreix en tot el domini; c) $2\sqrt2-\sqrt3\approx%s$.' % dd(2 * sqrt(2) - sqrt(3), 3))

# 100
f100 = 2 * x * (12 - R(12, 5) * x)
ok(solve(diff(f100, x), x), [R(5, 2)]); ok(f100.subs(x, R(5, 2)), 30)
S[100] = SOL([st('a)', r'La recta $AC$ és $y=12-\frac{12}{5}x$. El rectangle té base $2x$ i altura $12-\frac{12x}{5}$: $$f(x)=2x\left(12-\frac{12x}{5}\right)=24x-\frac{24x^2}{5},\quad0\le x\le5$$'),
             st('b)', r"$f^{\prime}(x)=24-\frac{48x}{5}=0\iff x=\frac52$; $f^{\prime\prime}<0$: màxim. Rectangle de base 5 i altura 6 (àrea 30)."),
             st('c)', r'Àrea del triangle: $\frac{10\cdot12}{2}=60$. Proporció $\frac{30}{60}=\frac12$.')],
            r'a) $f(x)=24x-\frac{24}{5}x^2$; b) $x=\frac52$: $5\times6$; c) la meitat de l’àrea del triangle.')

# 101
f101 = (x - 1) / (x * (x + 2))
ok(sp.factor(diff(f101, x)), -(x**2 - 2 * x - 2) / (x**2 * (x + 2)**2)); pri(f101, -ln(x) / 2 + R(3, 2) * ln(x + 2))
S[101] = SOL([st('a)', r'Domini $\mathbb R\setminus\{-2,0\}$; el numerador no s’anul·la en $-2$ ni en $0$: asímptotes verticals $x=-2$ i $x=0$. Horitzontal $y=0$.'),
             st('b)', r"$$f^{\prime}(x)=\frac{x(x+2)-(x-1)(2x+2)}{x^2(x+2)^2}=\frac{-x^2+2x+2}{x^2(x+2)^2}=0\iff x=1\pm\sqrt3$$" +
                taula_m([(r'(-\infty,-2)', '-'), (r'(-2,1-\sqrt3)', '-'), (r'(1-\sqrt3,0)', '+'), (r'(0,1+\sqrt3)', '+'), (r'(1+\sqrt3,+\infty)', '-')])),
             st('c)', r'$\dfrac{x-1}{x(x+2)}=\dfrac Ax+\dfrac{B}{x+2}$: $x=0\Rightarrow A=-\frac12$; $x=-2\Rightarrow B=\frac32$. $$\int f(x)\,dx=-\frac12\ln|x|+\frac32\ln|x+2|+C$$')],
            r'b) Decreix en $(-\infty,-2)\cup(-2,1-\sqrt3)\cup(1+\sqrt3,+\infty)$ i creix en $(1-\sqrt3,0)\cup(0,1+\sqrt3)$; c) $-\frac12\ln|x|+\frac32\ln|x+2|+C$.')

# 102
A102 = (80 - x) * (40 + R(5, 4) * x)
ok(solve(diff(A102, x), x), [24]); ok(A102.subs(x, 24), 3920)
S[102] = SOL([st('a)', r'Amb l’origen en el cantó trencat, la vora del trencament va de $(0,40)$ a $(32,0)$: $y=40-\frac54x$. $R$ va de $(x,y)$ fins al cantó oposat $(80,80)$: $$A(x)=(80-x)(80-y)=(80-x)\left(40+\frac54x\right),\quad0\le x\le32$$'),
             st('b)', r"$A^{\prime}(x)=-\left(40+\frac54x\right)+\frac54(80-x)=60-\frac52x=0\iff x=24$; $A^{\prime\prime}<0$. Aleshores $y=10$ i $R$ fa $56\times70$ cm. (Extrems: $A(0)=3200$, $A(32)=3840$.)"),
             st('c)', r'$A(24)=56\cdot70=3920$ cm².')],
            r'b) $56$ cm $\times$ $70$ cm (vèrtex en $(24,10)$); c) 3920 cm².')

# 103
f103 = x * exp(1 - x**2)
ok(sp.factor(diff(f103, x)), -(2 * x**2 - 1) * exp(1 - x**2)); pri(f103, -exp(1 - x**2) / 2); ok(f103.subs(x, sqrt(2) / 2), sqrt(E / 2))
S[103] = SOL([st('a)', r"Domini $\mathbb R$. $f^{\prime}(x)=(1-2x^2)e^{1-x^2}=0\iff x=\pm\frac{\sqrt2}{2}$: decreix en $\left(-\infty,-\frac{\sqrt2}{2}\right)\cup\left(\frac{\sqrt2}{2},+\infty\right)$ i creix en $\left(-\frac{\sqrt2}{2},\frac{\sqrt2}{2}\right)$. Mínim $\left(-\frac{\sqrt2}{2},-\sqrt{\frac e2}\right)$ i màxim $\left(\frac{\sqrt2}{2},\sqrt{\frac e2}\right)$ ($\sqrt{e/2}\approx1{,}17$)."),
             st('b)', r'No té verticals; $\displaystyle\lim_{x\to\pm\infty}\frac{ex}{e^{x^2}}=0$: asímptota horitzontal $y=0$. És senar.' + gr([f103], xr=(-3.5, 3.5), yr=(-1.5, 1.5), pts=[(0, 0), (math.sqrt(0.5), math.sqrt(math.e / 2)), (-math.sqrt(0.5), -math.sqrt(math.e / 2))])),
             st('c)', r'$\displaystyle\int xe^{1-x^2}dx=-\frac12\int(-2x)e^{1-x^2}dx=-\frac12e^{1-x^2}+C$.')],
            r'a) Mínim $\left(-\frac{\sqrt2}{2},-\sqrt{e/2}\right)$, màxim $\left(\frac{\sqrt2}{2},\sqrt{e/2}\right)$; b) $y=0$; c) $-\frac12e^{1-x^2}+C$.')

# 104
L104 = 2 * (4 + pi) / y + (2 + pi / 2) * y
ok(pos(diff(L104, y), y), [2]); ok(L104.subs(y, 2), 8 + 2 * pi)
S[104] = SOL([st('a)', r'Els semicercles tenen diàmetre $y$. Superfície: $xy+\pi\frac{y^2}{4}=4+\pi\Rightarrow x=\dfrac{4+\pi}{y}-\dfrac{\pi y}{4}$. Les ratlles són els dos costats horitzontals, els dos verticals i les dues semicircumferències: $$L(y)=2x+2y+\pi y=\frac{2(4+\pi)}{y}+\left(2+\frac{\pi}{2}\right)y$$'),
             st('b)', r"$L^{\prime}(y)=-\dfrac{2(4+\pi)}{y^2}+\dfrac{4+\pi}{2}=0\iff y^2=4\iff y=2$; $L^{\prime\prime}>0$: mínim. $x=\frac{4+\pi}{2}-\frac{\pi}{2}=2$.")],
            r'a) $L(y)=\frac{2(4+\pi)}{y}+\left(2+\frac{\pi}{2}\right)y$; b) rectangle de $2\times2$ m amb semicercles de diàmetre 2 m (longitud $8+2\pi$ m).')

# 105
f105 = (x**2 + 3) / (x**2 - 4)
ok(sp.factor(diff(f105, x)), -14 * x / ((x - 2)**2 * (x + 2)**2)); pri(f105, x + R(7, 4) * ln((x - 2) / (x + 2)), at=(R(5, 2), R(7, 2)))
S[105] = SOL([st('a)', r'Domini $\mathbb R\setminus\{-2,2\}$. Talla OY en $\left(0,-\frac34\right)$; $x^2+3\neq0$: no talla OX.'),
             st('b)', r'Verticals $x=\pm2$ (numerador no nul); $\displaystyle\lim_{x\to\pm\infty}f=1$: horitzontal $y=1$.'),
             st('c)', r"$f^{\prime}(x)=\dfrac{2x(x^2-4)-2x(x^2+3)}{(x^2-4)^2}=\dfrac{-14x}{(x^2-4)^2}$: creix en $(-\infty,-2)\cup(-2,0)$ i decreix en $(0,2)\cup(2,+\infty)$. Màxim relatiu $\left(0,-\frac34\right)$."),
             st('d)', r'$f(x)=1+\dfrac{7}{x^2-4}=1+\dfrac74\left(\dfrac{1}{x-2}-\dfrac{1}{x+2}\right)$: $$\int f(x)\,dx=x+\frac74\ln\left|\frac{x-2}{x+2}\right|+C$$'),
             gr([f105], xr=(-6, 6), yr=(-5, 6), va=(-2, 2), ha=(1,), pts=[(0, -0.75)])],
            r'b) $x=\pm2$, $y=1$; c) màxim en $\left(0,-\frac34\right)$; d) $x+\frac74\ln\left|\frac{x-2}{x+2}\right|+C$.')

# 106
S106 = sqrt(3) / 4 * x**2 + ((240 - 3 * x) / 4)**2; x106 = 720 / (9 + 4 * sqrt(3))
ok(diff(S106, x).subs(x, x106), 0)
S[106] = SOL([st('a)', r'Triangle de costat $x$ (gasta $3x$ m) i quadrat de costat $\frac{240-3x}{4}$: $$S(x)=\frac{\sqrt3}{4}x^2+\left(\frac{240-3x}{4}\right)^2,\quad0\le x\le80$$'),
             st('b)', r"$S^{\prime}(x)=\frac{\sqrt3}{2}x-\frac38(240-3x)=0\iff x\,\frac{4\sqrt3+9}{8}=90\iff x=\frac{720}{9+4\sqrt3}\approx%s$ m; $S^{\prime\prime}>0$: mínim. Cable per al triangle: $3x\approx%s$ m. Àrea mínima $\approx%s$ m²." % (dd(x106), dd(3 * x106), dd(S106.subs(x, x106))))],
            r'b) Cal $3x=\frac{2160}{9+4\sqrt3}\approx%s$ m de cable per al triangle; l’àrea mínima és $\approx%s$ m².' % (dd(3 * x106), dd(S106.subs(x, x106))))

# 107
pri(18 / (x**2 - 5 * x - 14), 2 * ln(x - 7) - 2 * ln(x + 2), at=(R(15, 2), 9)); ok(I(18 / (x**2 - 5 * x - 14), 8, 10), ln(R(25, 4)))
S[107] = SOL([st('a)', r'$x^2-5x-14=(x-7)(x+2)$; $\dfrac{18}{(x-7)(x+2)}=\dfrac{A}{x-7}+\dfrac{B}{x+2}$: $x=7\Rightarrow A=2$; $x=-2\Rightarrow B=-2$. $$\int\frac{18}{x^2-5x-14}dx=2\ln|x-7|-2\ln|x+2|+C=2\ln\left|\frac{x-7}{x+2}\right|+C$$'),
             st('b)', r'Per a $t>7$: $\displaystyle\int_8^t=2\ln\frac{t-7}{t+2}-2\ln\frac{1}{10}=2\ln\frac{10(t-7)}{t+2}$.'),
             st('c)', r'$2\ln\frac{10(t-7)}{t+2}=\ln\frac{25}{4}\iff\frac{10(t-7)}{t+2}=\frac52\iff20t-140=5t+10\iff t=10$.')],
            r'a) $2\ln\left|\frac{x-7}{x+2}\right|+C$; b) $2\ln\frac{10(t-7)}{t+2}$; c) $t=10$.')

# 108
ok(pos(diff(x * exp(-x**2), x)), [sqrt(2) / 2])
S[108] = SOL([st('a)', r'El rectangle té vèrtexs $(0,0)$, $(x,0)$, $M$ i $(0,f(x))$: $A(x)=xe^{-x^2}$, $x>0$.'),
             st('b)', r"$A^{\prime}(x)=(1-2x^2)e^{-x^2}=0\iff x=\frac{\sqrt2}{2}$; positiva abans i negativa després: màxim. $M=\left(\frac{\sqrt2}{2},e^{-1/2}\right)$ i $A=\frac{\sqrt2}{2}e^{-1/2}=\frac{1}{\sqrt{2e}}\approx0{,}43$ u².")],
            r'a) $A(x)=xe^{-x^2}$; b) $M\left(\frac{\sqrt2}{2},\frac{1}{\sqrt e}\right)$, àrea $\frac{1}{\sqrt{2e}}\approx0{,}43$ u².')

# 109
f109 = 1 / x + ln(x + 1)
ok(sp.factor(sp.together(diff(f109, x))), (x**2 - x - 1) / (x**2 * (x + 1))); ok(I(f109, 1, 2), 3 * ln(3) - ln(2) - 1)
x1, x2 = (1 - sqrt(5)) / 2, (1 + sqrt(5)) / 2
S[109] = SOL([st('a)', r'Cal $x\neq0$ i $x+1>0$: domini $(-1,0)\cup(0,+\infty)$. $\displaystyle\lim_{x\to0^\pm}f=\pm\infty$: asímptota $x=0$. $\displaystyle\lim_{x\to-1^+}f=-1+(-\infty)=-\infty$: asímptota $x=-1$. Quan $x\to+\infty$, $f\to+\infty$ i $\frac{f(x)}{x}\to0$: no hi ha horitzontal ni obliqua.'),
             st('b)', r"$$f^{\prime}(x)=-\frac{1}{x^2}+\frac{1}{x+1}=\frac{x^2-x-1}{x^2(x+1)}=0\iff x=\frac{1\pm\sqrt5}{2}$$ (totes dues en el domini). El denominador és positiu en el domini." +
                taula_m([(r'(-1,\frac{1-\sqrt5}{2})', '+'), (r'(\frac{1-\sqrt5}{2},0)', '-'), (r'(0,\frac{1+\sqrt5}{2})', '-'), (r'(\frac{1+\sqrt5}{2},+\infty)', '+')]) +
                r'Màxim relatiu en $x=\frac{1-\sqrt5}{2}\approx-0{,}62$ ($f\approx%s$) i mínim relatiu en $x=\frac{1+\sqrt5}{2}\approx1{,}62$ ($f\approx%s$).' % (dd(f109.subs(x, x1)), dd(f109.subs(x, x2)))),
             st('c)', r'En $[1,2]$, $f>0$. Per parts, $\int\ln(x+1)dx=(x+1)\ln(x+1)-x$: $$A=\Big[\ln x+(x+1)\ln(x+1)-x\Big]_1^2=(\ln2+3\ln3-2)-(2\ln2-1)=3\ln3-\ln2-1$$')],
            r'a) $(-1,0)\cup(0,+\infty)$, asímptotes $x=-1$ i $x=0$; b) creix en $(-1,\frac{1-\sqrt5}{2})\cup(\frac{1+\sqrt5}{2},+\infty)$, decreix en $(\frac{1-\sqrt5}{2},0)\cup(0,\frac{1+\sqrt5}{2})$; c) $3\ln3-\ln2-1\approx%s$ u².' % dd(3 * ln(3) - ln(2) - 1))

# 110
ok(I(12 - x**2, -sqrt(12), sqrt(12)), 32 * sqrt(3))
S[110] = SOL([st('a)', r"Porta amb cantonades $(\pm x,0)$ i $(\pm x,12-x^2)$: $A(x)=2x(12-x^2)$, $A^{\prime}(x)=24-6x^2=0\iff x=2$ (màxim, $A^{\prime\prime}<0$). Amplada 4 m i altura 8 m."),
             st('b)', r'Porta: $32$ m². Entrada: $$\int_{-\sqrt{12}}^{\sqrt{12}}(12-x^2)\,dx=2\left[12x-\frac{x^3}{3}\right]_0^{2\sqrt3}=2\cdot16\sqrt3=32\sqrt3\approx55{,}43\ \text{m}^2$$ Pedra: $32\sqrt3-32\approx23{,}43$ m².')],
            r'a) 4 m d’ample per 8 m d’alt; b) porta 32 m², pedra $32\sqrt3-32\approx23{,}43$ m².')

# 111
f111 = k * x * exp(-2 * x)
ok(sp.factor(diff(f111, x)), -k * (2 * x - 1) * exp(-2 * x)); ok(f111.subs(x, R(1, 2)), k / (2 * E))
S[111] = SOL([st('a)', r'Domini $\mathbb R$, sense asímptotes verticals. Si $k\neq0$: $\displaystyle\lim_{x\to+\infty}\frac{kx}{e^{2x}}=0$ (l’exponencial domina): $y=0$ per la dreta; quan $x\to-\infty$, $kxe^{-2x}\to\mp\infty$ i $\frac{f(x)}{x}=ke^{-2x}\to\pm\infty$: no hi ha asímptota per l’esquerra. (Si $k=0$, $f=0$.)'),
             st('b)', r"$f^{\prime}(x)=k(1-2x)e^{-2x}$. Si $k>0$: creix en $(-\infty,\frac12)$, decreix en $(\frac12,+\infty)$ i té un màxim en $\left(\frac12,\frac{k}{2e}\right)$. Si $k<0$: al revés, mínim en $\left(\frac12,\frac{k}{2e}\right)$. Si $k=0$ és constant."),
             st('c)', r'Per a qualsevol $k$, $f(0)=k\cdot0\cdot e^0=0$, i $0\in[-1,1]$.')],
            r'a) $y=0$ (quan $x\to+\infty$, si $k\neq0$); b) extrem en $x=\frac12$ (màxim si $k>0$, mínim si $k<0$); c) $f(0)=0$.')

# 112
aa = sp.symbols('aa', positive=True)
Ar = 2 * (I(aa - x**2, 0, sqrt(aa)) + I(x**2 - aa, sqrt(aa), 1))
ok(Ar.subs(aa, R(9, 16)), R(2, 3))
S[112] = SOL([st('Plantejament.', r'Les gràfiques es tallen en $x=\pm\sqrt a$. L’àrea compresa entre elles en $[-1,1]$ (simètrica) és $$A=2\left[\int_0^{\sqrt a}(a-x^2)dx+\int_{\sqrt a}^1(x^2-a)dx\right]=2\left[\frac23a\sqrt a+\left(\frac13-a+\frac23a\sqrt a\right)\right]=2\left(\frac43a\sqrt a-a+\frac13\right)$$'),
             st('Condició.', r'$A=\frac13\cdot2=\frac23$: $\frac43a\sqrt a-a+\frac13=\frac13\iff a\left(\frac43\sqrt a-1\right)=0\iff\sqrt a=\frac34\iff a=\frac{9}{16}$.'),
             gr([(x**2, [-1, 1]), (sp.Rational(9, 16), [-1, 1])], xr=(-1.3, 1.3), yr=(-0.1, 1.15), shade=[(x**2, sp.Rational(9, 16), -1, 1)])],
            r'$a=\frac{9}{16}$.')

# 113
h113 = x**2 + R(3, 2) * x
ok(diff(h113, x).subs(x, R(-3, 4)), 0); ok(I(diff(h113, x) - h113, -1, R(3, 2)), R(125, 48))
S[113] = SOL([st('a)', r"$h^{\prime}(x)=a+2x=0$ en $x=-\frac34\Rightarrow a=\frac32$ ($h^{\prime\prime}=2>0$: mínim)."),
             st('b)', r"$h(x)=x^2+\frac32x$: paràbola amb vèrtex $\left(-\frac34,-\frac{9}{16}\right)$ i zeros $0$, $-\frac32$. $h^{\prime}(x)=2x+\frac32$: recta."),
             gr([h113, diff(h113, x)], xr=(-2.5, 2.5), yr=(-1.5, 5), shade=[(diff(h113, x), h113, -1, 1.5)], pts=[(-1, -0.5), (1.5, 4.5), (-0.75, -0.5625)]),
             st('c)', r'$x^2+\frac32x=2x+\frac32\iff2x^2-x-3=0\iff x=-1,\ \frac32$. $$A=\int_{-1}^{3/2}\left(-x^2+\frac x2+\frac32\right)dx=\left[-\frac{x^3}{3}+\frac{x^2}{4}+\frac{3x}{2}\right]_{-1}^{3/2}=\frac{125}{48}$$')],
            r'a) $a=\frac32$; c) $\frac{125}{48}\approx2{,}60$ u².')

# 114
V114 = x * (16 - 2 * x) * (10 - 2 * x)
ok(solve(diff(V114, x), x), [2, R(20, 3)]); ok(V114.subs(x, 2), 144)
S[114] = SOL([st('Volum.', r'La base fa $(16-2x)\times(10-2x)$ i l’altura $x$: $V(x)=x(16-2x)(10-2x)=4x^3-52x^2+160x$, $0<x<5$.'),
             st('a)', r"$V^{\prime}(x)=12x^2-104x+160=4(3x^2-26x+40)=0\iff x=2$ o $x=\frac{20}{3}$ (fora). $V^{\prime\prime}(2)=24\cdot2-104<0$: màxim. Caixa de $12\times6\times2$ cm."),
             st('b)', r'$V(2)=2\cdot12\cdot6=144$ cm³.')],
            r'a) $12$ cm $\times$ $6$ cm de base i 2 cm d’altura; b) 144 cm³.')

# 115
P115 = 2 * R(5, 4) * x**2 + 4 * x * 80 / x**2
ok([s_ for s_ in solve(diff(P115, x), x) if s_.is_real], [4]); ok(P115.subs(x, 4), 120)
S[115] = SOL([st('a)', r'Altura $h=\frac{80}{x^2}$. Laterals: $4xh=\frac{320}{x}$ cm² a 1 cèntim; base i tapa: $2x^2$ cm² a 1,25 cèntims: $$P(x)=2{,}5x^2+\frac{320}{x}\ \text{cèntims},\quad x>0$$'),
             st('b)', r"$P^{\prime}(x)=5x-\dfrac{320}{x^2}=0\iff x^3=64\iff x=4$ cm; $P^{\prime\prime}>0$: mínim. $h=5$ cm."),
             st('c)', r'$P(4)=40+80=120$ cèntims $=1{,}20$ €.')],
            r'a) $P(x)=2{,}5x^2+\frac{320}{x}$; b) base de 4 cm de costat i 5 cm d’altura; c) 1,20 €.')

# 116
f116 = x * Abs(x - 2)
ok(-I(-x**2 + 2 * x, -1, 0) + I(-x**2 + 2 * x, 0, 2) + I(x**2 - 2 * x, 2, 5), R(62, 3))
S[116] = SOL([st('a)', r'$f(x)=\begin{cases}-x^2+2x & x<2\\ x^2-2x & x\ge2\end{cases}$; s’anul·la en $x=0$ i $x=2$, és negativa en $[-1,0)$ i positiva en $(0,2)\cup(2,5]$.' + gr([(f116, [-1, 5])], xr=(-1.5, 5.5), yr=(-4, 16), shade=[(f116, None, -1, 5)], pts=[(0, 0), (2, 0), (1, 1)])),
             st('b)', r'$$A=\left|\int_{-1}^0(-x^2+2x)dx\right|+\int_0^2(-x^2+2x)dx+\int_2^5(x^2-2x)dx=\frac43+\frac43+18=\frac{62}{3}$$')],
            r'b) $\frac{62}{3}\approx20{,}67$ u².')

# 117
x117 = sqrt(20 * sqrt(3) / 9); V117 = sqrt(3) / 12 * (10 * x - sqrt(3) / 2 * x**3)
ok(diff(V117, x).subs(x, x117), 0)
S[117] = SOL([st('a)', r'$A=2\cdot\frac{\sqrt3}{4}x^2+3xh=\frac{\sqrt3}{2}x^2+3xh=10$.'),
             st('b)', r"$h=\dfrac{10-\frac{\sqrt3}{2}x^2}{3x}$ i $V=\frac{\sqrt3}{4}x^2h=\frac{\sqrt3}{12}\left(10x-\frac{\sqrt3}{2}x^3\right)$. $V^{\prime}=\frac{\sqrt3}{12}\left(10-\frac{3\sqrt3}{2}x^2\right)=0\iff x^2=\frac{20\sqrt3}{9}$, $x\approx%s$ cm (màxim, $V^{\prime\prime}<0$). Aleshores $\frac{\sqrt3}{2}x^2=\frac{10}{3}$ i $h=\frac{20}{9x}\approx%s$ cm." % (dd(x117, 3), dd(20 / (9 * x117), 3))),
             st('c)', r'$V=\frac{\sqrt3}{4}x^2\cdot\frac{20}{9x}=\frac{5\sqrt3}{9}x\approx%s$ cm³.' % dd(V117.subs(x, x117), 3))],
            r'b) $x=\sqrt{\frac{20\sqrt3}{9}}\approx%s$ cm, $h\approx%s$ cm; c) $V\approx%s$ cm³.' % (dd(x117, 3), dd(20 / (9 * x117), 3), dd(V117.subs(x, x117), 3)))
ok(V117.subs(x, x117), R(5, 9) * sqrt(3) * x117)

# 118
f118 = 4 / (x - 1)**2 + x
ok(sp.factor(f118.subs(x, -1)), 0); pri(f118, -4 / (x - 1) + x**2 / 2); ok(solve(diff(f118, x), x)[0] if len([s_ for s_ in solve(diff(f118, x), x) if s_.is_real]) == 1 else 0, 3)
S[118] = SOL([st('a)', r'Domini $\mathbb R\setminus\{1\}$. $\displaystyle\lim_{x\to1}f=+\infty$: vertical $x=1$. $f(x)-x=\frac{4}{(x-1)^2}\to0$: obliqua $y=x$.'),
             st('b)', r"$f^{\prime}(x)=1-\dfrac{8}{(x-1)^3}=0\iff(x-1)^3=8\iff x=3$." + taula_m([(r'(-\infty,1)', '+'), (r'(1,3)', '-'), (r'(3,+\infty)', '+')]) + r'Mínim relatiu $(3,4)$.'),
             st('c)', r'Talls: $(0,4)$ i, com que $x^3-2x^2+x+4=(x+1)(x^2-3x+4)$, $(-1,0)$.' + gr([f118], xr=(-4, 7), yr=(-4, 12), va=(1,), ob=(lambda v: v,), pts=[(3, 4), (-1, 0), (0, 4)])),
             st('d)', r'$\displaystyle\int\left(4(x-1)^{-2}+x\right)dx=-\frac{4}{x-1}+\frac{x^2}{2}+C$.')],
            r'a) $x=1$ i $y=x$; b) mínim $(3,4)$, creix en $(-\infty,1)\cup(3,+\infty)$ i decreix en $(1,3)$; d) $-\frac{4}{x-1}+\frac{x^2}{2}+C$.')

# 119
f119 = x / (x**2 + 1)
ok(sp.factor(diff(f119, x)), -(x - 1) * (x + 1) / (x**2 + 1)**2)
S[119] = SOL([st('a)', r"Domini $\mathbb R$ (sense verticals); horitzontal $y=0$. $f^{\prime}(x)=\dfrac{1-x^2}{(x^2+1)^2}$: decreix en $(-\infty,-1)\cup(1,+\infty)$ i creix en $(-1,1)$."),
             st('b)', r'Mínim relatiu $\left(-1,-\frac12\right)$ i màxim relatiu $\left(1,\frac12\right)$. Com que $f\to0$ en $\pm\infty$ i $|f(x)|\le\frac12$ ($x^2+1\ge2|x|$), també són absoluts.'),
             st('c)', r'És senar i passa per l’origen.' + gr([f119], xr=(-6, 6), yr=(-0.8, 0.8), pts=[(-1, -0.5), (1, 0.5), (0, 0)]))],
            r'a) $y=0$; decreix en $(-\infty,-1)\cup(1,+\infty)$, creix en $(-1,1)$; b) mínim absolut $-\frac12$ en $x=-1$ i màxim absolut $\frac12$ en $x=1$.')

# 120
ok(I(8 * x, 0, R(1, 2)) + I(1 / x**2, R(1, 2), 1), 2)
S[120] = SOL([st('a)', r"Domini $\mathbb R\setminus\{0\}$; vertical $x=0$ i horitzontal $y=0$. $f^{\prime}(x)=-\frac{2}{x^3}$: creix en $(-\infty,0)$ i decreix en $(0,+\infty)$."),
             st('b) i tall.', r'$\frac{1}{x^2}=8x\iff x^3=\frac18\iff x=\frac12$: punt $\left(\frac12,4\right)$.' + gr([1 / x**2, 8 * x], xr=(-2, 2.5), yr=(-1, 8), va=(0,), shade=[(sp.Piecewise((8 * x, x < sp.Rational(1, 2)), (1 / x**2, True)), None, 0.001, 1)], pts=[(0.5, 4)])),
             st('c)', r'El recinte és sota la recta entre 0 i $\frac12$ i sota $f$ entre $\frac12$ i 1: $$A=\int_0^{1/2}8x\,dx+\int_{1/2}^1\frac{dx}{x^2}=\Big[4x^2\Big]_0^{1/2}+\left[-\frac1x\right]_{1/2}^1=1+1=2$$')],
            r'a) $x=0$, $y=0$; creix en $(-\infty,0)$, decreix en $(0,+\infty)$; c) 2 u².')

# 121
f121 = x / (9 - x**2)
ok(sp.factor(diff(f121, x)), (x**2 + 9) / ((x - 3)**2 * (x + 3)**2)); pri(f121, -ln(9 - x**2) / 2); ok(2 * I(f121, 0, 1), ln(R(9, 8)))
S[121] = SOL([st('a)', r"Domini $\mathbb R\setminus\{-3,3\}$; verticals $x=\pm3$, horitzontal $y=0$. $f^{\prime}(x)=\dfrac{9+x^2}{(9-x^2)^2}>0$: creix en $(-\infty,-3)$, $(-3,3)$ i $(3,+\infty)$."),
             st('b)', r'És senar.' + gr([f121], xr=(-7, 7), yr=(-3, 3), va=(-3, 3), shade=[(f121, None, -1, 1)], pts=[(0, 0)])),
             st('c)', r'$\displaystyle\int\frac{x}{9-x^2}dx=-\frac12\int\frac{-2x}{9-x^2}dx=-\frac12\ln|9-x^2|+C$.'),
             st('d)', r'$f\le0$ en $[-1,0]$ i $f\ge0$ en $[0,1]$; per simetria $$A=2\int_0^1\frac{x}{9-x^2}dx=-\Big[\ln(9-x^2)\Big]_0^1=\ln9-\ln8=\ln\frac98$$')],
            r'a) $x=\pm3$, $y=0$, creixent en tot el domini; c) $-\frac12\ln|9-x^2|+C$; d) $\ln\frac98\approx0{,}118$ u².')

# 122
r122 = (33 / (2 * pi))**R(1, 3); A122 = 2 * pi * r**2 + 66 / r
ok(diff(A122, r).subs(r, r122), 0)
S[122] = SOL([st('a)', r'$A=2\pi r^2+2\pi rh$, amb $\pi r^2h=33\Rightarrow h=\frac{33}{\pi r^2}$: $A(r)=2\pi r^2+\frac{66}{r}$.'),
             st('b)', r"$A^{\prime}(r)=4\pi r-\frac{66}{r^2}=0\iff r^3=\frac{33}{2\pi}\iff r=\sqrt[3]{\frac{33}{2\pi}}\approx%s$ cm; $A^{\prime\prime}>0$: mínim. $h=\frac{33}{\pi r^2}=2r\approx%s$ cm." % (dd(r122), dd(2 * r122))),
             st('c)', r'$A=2\pi r^2+4\pi r^2=6\pi r^2\approx%s$ cm².' % dd(6 * pi * r122**2))],
            r'b) $r=\sqrt[3]{\frac{33}{2\pi}}\approx%s$ cm i $h=2r\approx%s$ cm; c) $\approx%s$ cm².' % (dd(r122), dd(2 * r122), dd(6 * pi * r122**2)))
ok(A122.subs(r, r122), 6 * pi * r122**2)

# 123
f123 = (x + 1) / (x**2 + 1)
ok(sp.factor(diff(f123, x)), -(x**2 + 2 * x - 1) / (x**2 + 1)**2); ok(f123.subs(x, -1 + sqrt(2)), (1 + sqrt(2)) / 2); ok(f123.subs(x, -1 - sqrt(2)), (1 - sqrt(2)) / 2)
S[123] = SOL([st('a)', r'$x^2+1>0$: domini $\mathbb R$, i és contínua en tot $\mathbb R$ (quocient de polinomis amb denominador no nul).'),
             st('b)', r"No té verticals; horitzontal $y=0$. $f^{\prime}(x)=\dfrac{(x^2+1)-2x(x+1)}{(x^2+1)^2}=\dfrac{1-2x-x^2}{(x^2+1)^2}=0\iff x=-1\pm\sqrt2$." +
                taula_m([(r'(-\infty,-1-\sqrt2)', '-'), (r'(-1-\sqrt2,-1+\sqrt2)', '+'), (r'(-1+\sqrt2,+\infty)', '-')])),
             st('c)', r'Mínim en $x=-1-\sqrt2$: $f=\frac{1-\sqrt2}{2}\approx-0{,}21$; màxim en $x=-1+\sqrt2$: $f=\frac{1+\sqrt2}{2}\approx1{,}21$. Com que $f\to0$ en $\pm\infty$, també són el mínim i el màxim absoluts.'),
             st('d)', gr([f123], xr=(-7, 6), yr=(-0.5, 1.5), pts=[(-1 - math.sqrt(2), (1 - math.sqrt(2)) / 2), (-1 + math.sqrt(2), (1 + math.sqrt(2)) / 2), (-1, 0), (0, 1)]))],
            r'b) $y=0$; decreix en $(-\infty,-1-\sqrt2)\cup(-1+\sqrt2,+\infty)$, creix en $(-1-\sqrt2,-1+\sqrt2)$; c) mínim absolut $\frac{1-\sqrt2}{2}$ i màxim absolut $\frac{1+\sqrt2}{2}$.')

# 124
f124 = cos(pi * x / 9) + 2; G = I(f124, 0, 12)
ok(G, 24 - 9 * sqrt(3) / (2 * pi)); ok(sp.ceiling(G / 3), 8)
S[124] = SOL([st('a)', r"$1\le f(x)\le3$: no talla l’eix OX; talla OY en $(0,3)$. $f^{\prime}(x)=-\frac{\pi}{9}\sin\frac{\pi x}{9}=0$ en $x=0$ i $x=9$: decreix en $(0,9)$ i creix en $(9,12)$. Màxim absolut $f(0)=3$, mínim absolut $f(9)=1$; $f(12)=\cos\frac{4\pi}{3}+2=\frac32$." + gr([(f124, [0, 12])], xr=(-0.5, 12.5), yr=(-0.3, 3.4), shade=[(f124, None, 0, 12)], pts=[(0, 3), (9, 1), (12, 1.5)])),
             st('b)', r'$$A_{verd}=\int_0^{12}\left(\cos\frac{\pi x}{9}+2\right)dx=\left[\frac9\pi\sin\frac{\pi x}{9}+2x\right]_0^{12}=\frac9\pi\sin\frac{4\pi}{3}+24=24-\frac{9\sqrt3}{2\pi}\approx%s\ \text{m}^2$$ $A_{roig}=36-A_{verd}=12+\frac{9\sqrt3}{2\pi}\approx%s$ m².' % (dd(G), dd(36 - G))),
             st('c)', r'$\frac{%s}{3}\approx%s$: calen 8 pots.' % (dd(G), dd(G / 3)))],
            r'b) Verd $24-\frac{9\sqrt3}{2\pi}\approx%s$ m², roig $12+\frac{9\sqrt3}{2\pi}\approx%s$ m²; c) 8 pots.' % (dd(G), dd(36 - G)))

# 125
s125 = sqrt(6) / 2
ok(I(3 - 2 * x**2, -1, s125) + I(2 * x**2 - 3, s125, 5), R(212, 3) + 2 * sqrt(6))
S[125] = SOL([st('a)', r"$2x^2-3=0\iff x=\pm\frac{\sqrt6}{2}$; dins de $[-1,5]$ només $\frac{\sqrt6}{2}\approx1{,}22$. $f(x)=3-2x^2$ en $\left[-1,\frac{\sqrt6}{2}\right]$ ($f^{\prime}=-4x$) i $2x^2-3$ en $\left[\frac{\sqrt6}{2},5\right]$ ($f^{\prime}=4x>0$). Creix en $(-1,0)$ i $\left(\frac{\sqrt6}{2},5\right)$, decreix en $\left(0,\frac{\sqrt6}{2}\right)$."),
             st('b)', r'Candidats: $f(-1)=1$, $f(0)=3$, $f\left(\frac{\sqrt6}{2}\right)=0$, $f(5)=47$. Màxim absolut 47 en $x=5$; mínim absolut 0 en $x=\frac{\sqrt6}{2}$.'),
             st('c)', gr([(Abs(2 * x**2 - 3), [-1, 5])], xr=(-1.5, 5.5), yr=(-2, 50), shade=[(Abs(2 * x**2 - 3), None, -1, 5)], pts=[(-1, 1), (0, 3), (math.sqrt(1.5), 0), (5, 47)])),
             st('d)', r'Amb $s=\frac{\sqrt6}{2}$ ($s^2=\frac32$): $$A=\int_{-1}^{s}(3-2x^2)dx+\int_s^5(2x^2-3)dx=\left(\sqrt6+\frac73\right)+\left(\frac{205}{3}+\sqrt6\right)=\frac{212}{3}+2\sqrt6$$')],
            r'a) Creix en $(-1,0)\cup(\frac{\sqrt6}{2},5)$, decreix en $(0,\frac{\sqrt6}{2})$; b) màxim 47, mínim 0; d) $\frac{212}{3}+2\sqrt6\approx%s$ u².' % dd(R(212, 3) + 2 * sqrt(6)))

# 126
V126 = pi / 2 * (600 * r - r**3)
ok(pos(diff(V126, r), r), [10 * sqrt(2)]); ok(V126.subs(r, 10 * sqrt(2)), 2000 * sqrt(2) * pi)
S[126] = SOL([st('a)', r'Àrea: lateral corba $\pi rL$ (mig cilindre) i dos semicercles $\pi r^2$: $\pi rL+\pi r^2=600\pi\Rightarrow L=\frac{600-r^2}{r}$. $$V(r)=\frac{\pi r^2}{2}L=\frac{\pi}{2}(600r-r^3),\quad0<r<\sqrt{600}$$'),
             st('b)', r"$V^{\prime}(r)=\frac\pi2(600-3r^2)=0\iff r=\sqrt{200}=10\sqrt2$ cm; $V^{\prime\prime}<0$: màxim. $L=\frac{400}{10\sqrt2}=20\sqrt2$ cm i $V=\frac\pi2\cdot10\sqrt2\cdot400=2000\sqrt2\,\pi\approx%s$ cm³." % dd(2000 * sqrt(2) * pi))],
            r'a) $V(r)=\frac\pi2(600r-r^3)$; b) $r=10\sqrt2\approx14{,}14$ cm, $L=20\sqrt2\approx28{,}28$ cm, $V=2000\sqrt2\,\pi\approx%s$ cm³.' % dd(2000 * sqrt(2) * pi))

# 127
F127 = R(10, 3) * t**3 - t**4 / 4 + 6
pri(t**2 * (10 - t), F127, t); ok(F127.subs(t, 10), R(2518, 3))
S[127] = SOL([st('a)', r'$F(t)=\int(10t^2-t^3)dt=\frac{10t^3}{3}-\frac{t^4}{4}+C$; $F(0)=6\Rightarrow C=6$.'),
             st('b)', r"$F^{\prime}(t)=t^2(10-t)\ge0$ si $0\le t<10$ i $<0$ si $t>10$: màxim en $t=10$. $F(10)=\frac{10000}{3}-2500+6=\frac{2518}{3}\approx839{,}33$.")],
            r'a) $F(t)=\frac{10}{3}t^3-\frac{t^4}{4}+6$; b) als 10 dies, amb un coeficient de $\frac{2518}{3}\approx839{,}33$.')

# 128
f128 = x**2 / 4 * (900 - 30 * x)
ok(pos(diff(f128, x)), [20]); ok(sqrt(f128.subs(x, 20)), 100 * sqrt(3))
S[128] = SOL([st('a)', r'Costats iguals $\frac{60-x}{2}=30-\frac x2$; altura $\sqrt{\left(30-\frac x2\right)^2-\frac{x^2}{4}}=\sqrt{900-30x}$: $$A(x)=\frac x2\sqrt{900-30x},\quad0<x<30$$'),
             st('b)', r"$f(x)=A(x)^2=225x^2-\frac{15}{2}x^3$; $f^{\prime}(x)=450x-\frac{45}{2}x^2=0\iff x=20$; $f^{\prime}>0$ abans i $<0$ després: màxim. El triangle és equilàter i $A(20)=10\sqrt{300}=100\sqrt3\approx173{,}21$ m².")],
            r'a) $A(x)=\frac x2\sqrt{900-30x}$; b) $x=20$ m, amb $A=100\sqrt3\approx173{,}21$ m².')
