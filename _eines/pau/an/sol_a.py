# Solucions dels exercicis PAU d'anàlisi (Comunitat Valenciana), números 1-40 del dossier.
# Els resultats es calculen amb fraccions exactes; ck() els compara amb el valor calculat a mà.
from anlib import *
S = {}


def opt(p, v='x', name='f', want=None):
    """extrem d'un polinomi de grau 2 (o d'una funció amb un sol punt crític racional): derivada, punt crític i
    criteri de la segona derivada. Torna (text, x*, f(x*))"""
    d = p.d(); rs = [r.ex for r in roots(d)]
    assert len(rs) == 1 and rs[0] is not None, rs
    x0 = rs[0]; d2 = d.d()(x0)
    kind = 'màxim' if d2 < 0 else 'mínim'
    if want: assert kind == want
    t = (r"$%s'(%s)=%s=0\iff %s=%s$. Com que $%s''(%s)=%s%s0$, és un <strong>%s</strong>: $%s(%s)=%s$."
         % (name, v, d.tex(v), v, nm(x0), name, nm(x0) if d.d().deg > 0 else v, nm(d2), '<' if d2 < 0 else '>', kind, name, nm(x0), nm(p(x0))))
    return t, x0, p(x0)


def gq(p, a, b, pts=(), v='x', yl='y', **k):
    """gràfica d'un polinomi en [a,b]"""
    return plot([(lambda x: p(float(x)), [float(a), float(b)])], xr=k.pop('xr', None), pts=pts, xl=v, yl=yl, **k)


# 1
f = P(1, -100, 0)
S[1] = SOL([st('Monotonia.', r"$f'(x)=2x-100=0\iff x=50$. Com que $x\ge0$ (és una inversió): si $0<x<50$, $f'(x)<0$ i $f$ decreix; si $x>50$, $f'(x)>0$ i $f$ creix."),
            st('Rendibilitat negativa.', r'$f(x)=x^2-100x=x(x-100)<0\iff 0<x<100$.'),
            gq(f, 0, 110, pts=[(50, -2500), (100, 0), (0, 0)])],
           r'A més inversió correspon més rendibilitat per a $x>50$ milions. La rendibilitat és negativa si $0<x<100$ milions.')
ck(f(50), -2500)

# 2
S[2] = SOL([st('Variables.', r'Siguen $x$ i $y$ les dimensions (en m). L’àrea és $xy=100\Rightarrow y=\dfrac{100}{x}$.'),
            st('Funció a minimitzar:', r'el perímetre $P(x)=2x+2y=2x+\dfrac{200}{x}$, amb $x>0$.'),
            st('Derivada:', r"$P'(x)=2-\dfrac{200}{x^2}=0\iff x^2=100\iff x=10$ (la solució negativa no té sentit)."),
            st('Comprovació:', r"$P''(x)=\dfrac{400}{x^3}$, $P''(10)=0{,}4>0$: és un mínim. Aleshores $y=\dfrac{100}{10}=10$.")],
           r'L’escenari ha de ser un quadrat de $10\ \text{m}\times10\ \text{m}$ (perímetre mínim de 40 m).')

# 3
S[3] = SOL([st('Criteri.', r"Una funció és creixent on $f'>0$ i decreixent on $f'<0$."),
            st('a)', r"$f'(x)=2x$: és negativa en $[-2,0)$ i positiva en $(0,2]$. Per tant $f$ decreix en $[-2,0)$ i creix en $(0,2]$ (mínim en $x=0$)."),
            st('b)', r"$g'(x)=3x^2\ge0$ i només s’anul·la en $x=0$, on no canvia de signe: $g$ és creixent en tot l’interval $[-2,2]$.")],
           r'a) $f$ decreix en $[-2,0)$ i creix en $(0,2]$; b) $g$ creix en tot $[-2,2]$.')

# 4
S[4] = SOL([st('Dades.', r"Si $I(t)$ és la inflació, $I'(t)=t-2$ per a $0\le t\le5$."),
            st('Signe de la derivada:', r"$I'(t)<0$ si $0\le t<2$ (la inflació baixa) i $I'(t)>0$ si $2<t\le5$ (puja)." + taula_m([('[0,\\,2)', '-'), ('(2,\\,5]', '+')], "I'(t)", 'I(t)'))],
           r'La inflació arriba al mínim en $t=2$.')

# 5
v5 = P(1, -6, 10, v='t'); t5, x5, y5 = opt(v5, 't', 'v', 'mínim'); ck(x5, 3); ck(y5, 1)
S[5] = SOL([st('Mínim del preu:', t5),
            st('Extrems de l’interval:', r'$v(0)=10$ i $v(12)=82$, majors que $v(3)=1$, per tant és el mínim absolut del primer any.'),
            gq(v5, 0, 12, pts=[(3, 1)], v='t', yl='v')],
           r'Convé comprar les accions al tercer mes ($t=3$), quan valen $v(3)=1$.')

# 6
S[6] = SOL([st('Costat superior.', r'Passa per $(3,3)$ i $(15,15)$: la recta és $y=x$.'),
            st('Àrea.', r'El trapezi és el recinte limitat per la recta $y=x$, l’eix $OX$ i les rectes $x=3$ i $x=15$. Com que $y=x\ge0$ en $[3,15]$: $$A=\int_3^{15}x\,dx$$'),
            st('Significat.', r'La integral definida d’una funció positiva és l’àrea compresa entre la seua gràfica i l’eix $OX$ entre els límits d’integració. (Si es calcula: $\left[\frac{x^2}{2}\right]_3^{15}=\frac{225-9}{2}=108$ u², que coincideix amb l’àrea del trapezi $\frac{(15+3)\cdot12}{2}=108$.)'),
            plot([(lambda x: x, [3, 15])], xr=(-1, 17), yr=(-2, 17), shade=[(lambda x: x, None, 3, 15)], pts=[(3, 3), (15, 15), (3, 0), (15, 0)])],
           r'$A=\displaystyle\int_3^{15}x\,dx\ (=108\ \text{u}^2)$')
ck(P(1, 0).prim()(15) - P(1, 0).prim()(3), 108)

# 7
S[7] = SOL([st('Derivada:', r"$f(x)=\dfrac{2}{x-3}\Rightarrow f'(x)=\dfrac{-2}{(x-3)^2}$."),
            st('En $x=4$:', r"$f'(4)=\dfrac{-2}{1}=-2$. És el pendent de la recta tangent a la gràfica en el punt $(4,\,2)$ i la taxa de variació instantània: en aquest punt la funció decreix 2 unitats per cada unitat que augmenta $x$."),
            st('En $x=5$:', r"la taxa de variació instantània és $f'(5)=\dfrac{-2}{4}=-\dfrac12$.")],
           r"$f'(4)=-2$; $TVI(5)=f'(5)=-\frac12$")

# 8
f8 = P(-1, 1, 0, v='t'); t8, x8, y8 = opt(f8, 't', 'f', 'màxim'); ck(x8, F(1, 2)); ck(y8, F(1, 4))
S[8] = SOL([st('a)', r'$f(t)=t-t^2=t(1-t)=0\iff t=0$ o $t=1$: el rendiment és nul al principi i al final de l’examen.'),
            st('b)', t8),
            st('c)', r"$f'(t)=1-2t>0$ si $0\le t<\frac12$ i $f'(t)<0$ si $\frac12<t\le1$." + taula_m([('[0,\\,\\frac12)', '+'), ('(\\frac12,\\,1]', '-')], "f'(t)", 'f(t)')),
            gq(f8, 0, 1, pts=[(0.5, 0.25)], v='t', yl='f', xr=(-0.1, 1.1))],
           r'a) $t=0$ i $t=1$ h; b) màxim en $t=\frac12$ h, amb $f=\frac14$; c) creix en $[0,\frac12)$ i decreix en $(\frac12,1]$.')

# 9
f9 = P(F('-0.00055'), F('0.165'), 0); t9, x9, y9 = opt(f9, 'x', 'f', 'màxim'); ck(x9, 150); ck(y9, F('12.375')); ck(f9(200), 11)
S[9] = SOL([st('Funció:', r'$f(x)=-0{,}00055x(x-300)=-0{,}00055x^2+0{,}165x$, per a $0\le x\le200$.'),
            st('a)', t9),
            st('b)', r"$f'(x)>0$ si $0\le x<150$ (la velocitat augmenta) i $f'(x)<0$ si $150<x\le200$ (disminueix)."),
            st('c)', r'$f(200)=-0{,}00055\cdot200\cdot(-100)=11$ m/s.')],
           r'a) als 150 m, amb $12{,}375$ m/s; b) augmenta entre 0 i 150 m i disminueix entre 150 i 200 m; c) arriba a la meta a 11 m/s.')

# 10
f10 = P(F('2.1'), F('0.8'), -1, v='t'); a10 = ck((f10(9) - f10(0)) / 9, F('19.7')); b10 = ck((f10(9) - f10(7)) / 2, F('34.4'))
S[10] = SOL([st('Valors:', r'$f(0)=-1$, $f(7)=%s$, $f(9)=%s$.' % (nm(f10(7)), nm(f10(9)))),
             st('a)', r'$$TVM[0,9]=\frac{f(9)-f(0)}{9-0}=\frac{%s-(-1)}{9}=%s$$ milers d’euros per any.' % (nm(f10(9)), nm(a10))),
             st('b)', r'$$TVM[7,9]=\frac{f(9)-f(7)}{9-7}=\frac{%s-%s}{2}=%s$$ milers d’euros per any.' % (nm(f10(9)), nm(f10(7)), nm(b10))),
             st('c)', r'El benefici creix en tot el període, i en els dos últims anys ho fa molt més de pressa (34,4 milers d’euros per any) que de mitjana (19,7).')],
            r'a) $19{,}7$ milers d’€/any; b) $34{,}4$ milers d’€/any; c) el creixement del benefici s’accelera.')

# 11
T11 = P(F(-18, 5000), 60, v='h'); ck(T11(15000), 6)
S[11] = SOL([st('a)', r'És lineal: $T(h)=60+mh$. El pendent és $m=\dfrac{-18}{5000}=-0{,}0036$ °F/m. Per tant $T(h)=60-0{,}0036h$, $0\le h\le20000$.'),
             st('b)', r'$T(15000)=60-0{,}0036\cdot15000=60-54=6$ °F.'),
             st('c)', r'$60-0{,}0036h=0\iff h=\dfrac{60}{0{,}0036}=\dfrac{50000}{3}\approx16666{,}67$ m.')],
            r'a) $T=60-0{,}0036h$; b) 6 °F; c) $h\approx16667$ m.')

# 12
f12 = P(2, -12, 23); t12, x12, y12 = opt(f12, 'x', 'f', 'mínim'); ck(x12, 3); ck(f12(2), 7); ck(f12(5), 13)
S[12] = SOL([st('Interval:', r'$x\in[2,5]$ (milers de revolucions per minut).'),
             st('Punt crític:', t12),
             st('Extrems absoluts:', 'comparem amb els extrems de l’interval:' + taula_vals([(2, f12(2)), (3, f12(3)), (5, f12(5))])),
             gq(f12, 2, 5, pts=[(2, 7), (3, 5), (5, 13)], xr=(0, 6))],
            r'a) Consum mínim amb 3000 rpm; b) consum màxim amb 5000 rpm; c) 5 litres/hora i 13 litres/hora, respectivament.')

# 13
B13 = P(-1, 60, -500); t13, x13, y13 = opt(B13, 'x', 'B', 'màxim'); ck(x13, 30); ck(y13, 400)
S[13] = SOL([st('Benefici total:', r'(unitats venudes)·(benefici per unitat): $B(x)=(50-x)(x-10)=-x^2+60x-500$, $0\le x\le50$.'),
             st('Màxim:', t13),
             st('Unitats:', r'$y=50-30=20$ unitats.')],
            r'Preu de 30 €, se’n venen 20 unitats i el benefici és de 400 €.')

# 14
S14 = P(3, -360, 16200); t14, x14, y14 = opt(S14, 'x', 'S', 'mínim'); ck(x14, 60); ck(y14, 5400)
S[14] = SOL([st('Variables.', r'Sumands $x$ i $90-x$. Volem minimitzar $S(x)=x^2+2(90-x)^2=3x^2-360x+16200$.'),
             st('Mínim:', t14),
             st('Sumands:', r'$x=60$ i $90-60=30$.')],
            r'$90=60+30$ (el valor mínim de la suma és $60^2+2\cdot30^2=5400$).')

# 15
S[15] = SOL([st('Cost mitjà:', r'$$C_m(x)=\frac{C(x)}{x}=\frac{x}{2}+5+\frac{800}{x},\quad x>0$$'),
             st('Derivada:', r"$C_m'(x)=\dfrac12-\dfrac{800}{x^2}=0\iff x^2=1600\iff x=40$."),
             st('Comprovació:', r"$C_m''(x)=\dfrac{1600}{x^3}$, $C_m''(40)>0$: mínim."),
             st('Valor:', r'$C_m(40)=20+5+20=45$ €/litre.')],
            r'El cost mitjà és mínim produint 40 litres, i val 45 € per litre.')
ck(F(40, 2) + 5 + F(800, 40), 45)

# 16
C16 = P(F('-0.6'), 15, 90); t16, x16, y16 = opt(C16, 'x', 'C', 'màxim'); ck(x16, F('12.5')); ck(y16, F('183.75'))
S[16] = SOL([st('a)', r"$C'(x)=15-1{,}2x=0\iff x=12{,}5$. Si $0\le x<12{,}5$, $C'>0$: la concentració creix; si $12{,}5<x\le20$, $C'<0$: decreix." + taula_m([('[0,\\,12{,}5)', '+'), ('(12{,}5,\\,20]', '-')], "C'(x)", 'C(x)')),
             st('b)', t16 + r' A més, $C(0)=90$ i $C(20)=150$ són menors, per tant és el màxim absolut.'),
             gq(C16, 0, 20, pts=[(12.5, 183.75)], yl='C')],
            r'a) Creix els primers 12,5 dies i després decreix; b) concentració màxima de $183{,}75\ \mu\text{g/m}^3$ (en $x=12{,}5$ dies).')
ck(C16(20), 150)

# 17
B17 = P(-16, 24000, -700000); t17, x17, y17 = opt(B17, 'x', 'B', 'màxim'); ck(x17, 750); ck(y17, 8300000)
S[17] = SOL([st('a)', r'$B(x)=I(x)-G(x)=28x^2+36000x-44x^2-12000x-700000=-16x^2+24000x-700000$.'),
             st('b) i c)', t17)],
            r'a) $B(x)=-16x^2+24000x-700000$; b) 750 unitats; c) 8 300 000 €.')

# 18
p18 = P(F(-1, 2), 1, 1); b18, v18 = barrow(p18, 0, 2); ck(v18, F(8, 3))
S[18] = SOL([st('Plantejament.', r'La paret està limitada per la paràbola $y=-0{,}5x^2+x+1$, l’eix $OX$ i les rectes $x=0$ i $x=2$. La paràbola és positiva en $[0,2]$ ($y(0)=y(2)=1$, màxim $y(1)=1{,}5$).'),
             st('Superfície:', '$$' + b18 + '$$'),
             gq(p18, 0, 2, xr=(-0.5, 2.5), yr=(-0.3, 1.8), shade=[(lambda x: p18(float(x)), None, 0, 2)])],
            r'$S=\frac83\approx2{,}67$ m²')

# 19
C19 = P(-10, 60, 0, v='t'); t19, x19, y19 = opt(C19, 't', 'C', 'màxim'); ck(x19, 3); ck(y19, 90)
S[19] = SOL([st('a)', t19 + ' És a les 23 h.'),
             st('b)', r'$C(t)=50\iff t^2-6t+5=0\iff t=1,\ t=5$; $C(t)=80\iff t^2-6t+8=0\iff t=2,\ t=4$. La paràbola puja fins a $t=3$ i després baixa, per tant $50\le C(t)\le80$ si $t\in[1,2]\cup[4,5]$.'),
             gq(C19, 0, 6, v='t', yl='C', pts=[(1, 50), (2, 80), (4, 80), (5, 50), (3, 90)])],
            r'a) 90 clients (a les 23 h, $t=3$); b) entre les 21 h i les 22 h, o entre les 0 h i la 1 h.')

# 20
S[20] = SOL([st('Variables.', r'Siguen $x$ i $y$ l’amplària i l’altura del text: $xy=18\Rightarrow y=\dfrac{18}{x}$. El cartell mesura $(x+2)\times(y+4)$.'),
             st('Funció a minimitzar:', r'$$A(x)=(x+2)\left(\frac{18}{x}+4\right)=4x+\frac{36}{x}+26,\quad x>0$$'),
             st('Derivada:', r"$A'(x)=4-\dfrac{36}{x^2}=0\iff x^2=9\iff x=3$; $A''(x)=\dfrac{72}{x^3}>0$: mínim."),
             st('Dimensions:', r'text de $3\times6$ cm; cartell de $(3+2)\times(6+4)=5\times10$ cm, amb àrea $50$ cm².')],
            r'El cartell ha de fer 5 cm d’ample i 10 cm d’alt.')
ck(4 * 3 + F(36, 3) + 26, 50)

# 21
f21 = P(F('-0.1'), F('2.5'), -10); t21, x21, y21 = opt(f21, 'x', 'f', 'màxim'); ck(x21, F('12.5')); ck(y21, F('5.625'))
S[21] = SOL([st('a)', t21 + ' (milers d’euros).'),
             st('b)', r'$f(x)=0\iff x^2-25x+100=0\iff x=5,\ x=20$. Entre 5 i 20 tones el benefici és positiu: cal vendre almenys 5 tones.'),
             st('c)', r"Benefici per tona: $g(x)=\dfrac{f(x)}{x}=-0{,}1x+2{,}5-\dfrac{10}{x}$. $g'(x)=-0{,}1+\dfrac{10}{x^2}=0\iff x^2=100\iff x=10$; $g''(x)=-\dfrac{20}{x^3}<0$: màxim. $g(10)=-1+2{,}5-1=0{,}5$ milers d’euros per tona.")],
            r'a) 12,5 t, benefici de 5625 €; b) 5 t; c) 10 t, amb 500 € per tona.')
ck(F('-0.1') * 10 + F('2.5') - 1, F('0.5'))

# 22
I22 = P(-150, 600, 172800); t22, x22, y22 = opt(I22, 'x', 'I', 'màxim'); ck(x22, 2); ck(y22, 173400)
S[22] = SOL([st('a)', r'Siga $x$ el nombre d’euros que es rebaixa la tarifa. La tarifa és $36-x$ i els contractes $4800+150x$: $$I(x)=(36-x)(4800+150x)=-150x^2+600x+172800$$'),
             st('b)', t22),
             st('Resultat:', r'tarifa de $36-2=34$ € i $4800+150\cdot2=5100$ abonats.')],
            r'Tarifa de 34 €, amb 5100 abonats i un ingrés màxim de 173 400 €.')

# 23
I23 = P(-5, 50, 6000); t23, x23, y23 = opt(I23, 'x', 'I', 'màxim'); ck(x23, 5); ck(y23, 6125)
S[23] = SOL([st('Funció.', r'Si es venen al cap de $x$ dies: queden $2000-50x$ kg a $3+0{,}1x$ €/kg. $$I(x)=(2000-50x)(3+0{,}1x)=-5x^2+50x+6000$$'),
             st('Màxim:', t23),
             st('Quilos i preu:', r'$2000-250=1750$ kg a $3{,}5$ €/kg.')],
            r'Al cap de 5 dies: es venen 1750 kg a 3,50 €/kg i s’ingressen 6125 €.')

# 24
p24 = P(1, 2, 1); s24, a24 = area_steps(p24, -2, 5); ck(a24, F(217, 3))
S[24] = SOL([st('Signe.', r'$y=x^2+2x+1=(x+1)^2\ge0$: la paràbola no talla l’eix (només el toca en $x=-1$), per tant l’àrea és la integral entre $-2$ i $5$.')] + s24[1:] +
            [gq(p24, -2, 5, xr=(-3, 6), shade=[(lambda x: p24(float(x)), None, -2, 5)])],
            r'$A=\frac{217}{3}\approx72{,}33$ u²')

# 25
G25 = P(-50, 1000, 40000); t25, x25, y25 = opt(G25, 'x', 'G', 'màxim'); ck(x25, 10); ck(y25, 45000)
S[25] = SOL([st('Funció.', r'Siga $x$ el nombre d’augments de 50 €: el preu és $1000+50x$ i es lloguen $40-x$ vaixells. $$G(x)=(1000+50x)(40-x)=-50x^2+1000x+40000$$'),
             st('Màxim:', t25)],
            r'Preu de $1000+500=1500$ €: es lloguen 30 vaixells i s’ingressen 45 000 €.')

# 26
B26 = P(-1, 300, -20000); t26, x26, y26 = opt(B26, 'x', 'B', 'màxim'); ck(x26, 150); ck(y26, 2500)
S[26] = SOL([st('a)', r'$B(x)=I(x)-C(x)=400x+2x^2-20000-100x-3x^2=-x^2+300x-20000$.'),
             st('b)', t26)],
            r'a) $B(x)=-x^2+300x-20000$; b) 150 ciclomotors, amb un benefici de 2500 €.')

# 27
f27 = P(-1, 32, 144); t27, x27, y27 = opt(f27, 'x', 'f', 'màxim'); ck(f27(3), 231); ck(y27, 400)
e27, _ = eq2(-1, 32, 144)
S[27] = SOL([st('a)', r'$f(3)=-9+96+144=231$ persones.'),
             st('b)', t27),
             st('c) i d)', r'La malaltia comença i acaba quan no hi ha malalts: ' + e27 + r'. Va començar 4 dies abans de descobrir-se ($x=-4$) i acaba el dia 36.'),
             gq(f27, -4, 36, pts=[(-4, 0), (16, 400), (36, 0), (3, 231)], xr=(-8, 40))],
            r'a) 231; b) el dia 16 (400 malalts); c) 4 dies abans del descobriment; d) el dia 36.')

# 28
B28 = R(P(25, 0), P(1, 0, 16))
S[28] = SOL([st('Derivada:', r"$$B'(x)=\frac{25(x^2+16)-25x\cdot2x}{(x^2+16)^2}=\frac{25(16-x^2)}{(x^2+16)^2}$$"),
             st('a)', r"$B'(x)=0\iff x=4$ ($x\ge0$). $B'>0$ si $0\le x<4$ i $B'<0$ si $x>4$: màxim en $x=4$, $B(4)=\dfrac{100}{32}=3{,}125$ milers d’euros."),
             st('b)', r'Per a $x\ge0$, numerador i denominador són no negatius: $B(x)\ge0$. L’empresa no tindrà pèrdues (i $\lim_{x\to+\infty}B(x)=0$).'),
             plot([(lambda x: B28(x), [0, 30])], xr=(-1, 30), pts=[(4, 3.125)], yl='B')],
            r'a) Als 4 anys, benefici màxim de 3125 €; b) no, $B(x)\ge0$ per a tot $x\ge0$.')
ck(B28(F(4)), F(25, 8))

# 29
s29, r29 = estudi(R(P(1, 1, -5, 3)), lab={'dom': 'a)', 'tall': '', 'mon': 'b)', 'ext': 'c)', 'gra': 'd)'}, asim=False)
S[29] = SOL(s29, resum(r29))

# 30
c30a, _ = cont(-2, P(3, 10), P(1, 0, 0)); c30b, _ = cont(1, P(1, 0, 0), P(F(1, 2), F(3, 2)))
b30, v30 = barrow(P(2, 0, -3, 2), 2, 3); ck(v30, 27)
S[30] = SOL([st('a) Trossos.', r'Cada tros és un polinomi, continu en el seu interval. (Al dossier el tercer tros apareix com a «$-1\le x\le3$», que se solapa amb el segon; s’entén $1\le x\le3$.) Estudiem els punts d’unió:'),
             r'<strong>En $x=-2$:</strong> ' + c30a,
             r'<strong>En $x=1$:</strong> ' + c30b,
             plot([(lambda x: 3 * x + 10, [-3, -2]), (lambda x: x * x, [-2, 0.9999]), (lambda x: (x + 3) / 2, [1, 3])], xr=(-3.5, 3.5), pts=[(1, 1, 'o'), (1, 2)]),
             st('b)', '$$' + b30 + '$$')],
            r'a) Contínua en $[-3,3]$ excepte en $x=1$ (salt); b) $27$.')

# 31
c31a = r'$\displaystyle\lim_{x\to-1^-}(3x+a)=a-3$, $\displaystyle\lim_{x\to-1^+}(ax+2)=2-a=f(-1)$. Contínua si $a-3=2-a\iff a=\frac52$.'
c31b, _ = cont(-1, P(3, 0), P(2)); c31c, _ = cont(1, P(2), R(P(2, -11), P(1, -3)))
b31, v31 = barrow(P(1, 0, 0, -2), -2, 2); ck(v31, -8)
S[31] = SOL([st('a)', c31a),
             st('b)', r'Amb $a=0$: $f(x)=3x$ si $x<-1$; $f(x)=2$ si $-1\le x<1$; $f(x)=\dfrac{2x-11}{x-3}$ si $x\ge1$. Els dos primers trossos són polinomis; el tercer no està definit en $x=3$.'),
             r'<strong>En $x=-1$:</strong> ' + c31b, r'<strong>En $x=1$:</strong> ' + c31c,
             r'<strong>En $x=3$:</strong> $f(3)$ no existeix i $\displaystyle\lim_{x\to3^-}\frac{2x-11}{x-3}=+\infty$, $\displaystyle\lim_{x\to3^+}\frac{2x-11}{x-3}=-\infty$: discontinuïtat asimptòtica (inevitable, de salt infinit).',
             st('c)', '$$' + b31 + '$$')],
            r'a) $a=\frac52$; b) discontínua en $x=-1$ i $x=1$ (salt) i en $x=3$ (asímptota vertical); c) $-8$.')

# 32
s32, r32 = estudi(R(P(2, 0), P(1, 0, 1)), lab={'dom': 'a)', 'asi': 'b)', 'mon': 'c)', 'ext': 'd)', 'gra': 'e)'})
S[32] = SOL(s32, resum(r32))

# 33
C33 = P(27, -234, 2000, v='t'); t33, x33, y33 = opt(C33, 't', 'C', 'mínim'); ck(x33, F(13, 3)); ck(y33, 1493)
ck(C33(6), 1568); a33 = ck(C33(2) - C33(1), -153); b33 = ck(C33(6) - C33(5), 63)
S[33] = SOL([st('Punt crític:', t33 + r' $t=\frac{13}{3}$ h = 4 h 20 min, és a dir, a les 12.20 h.'),
             st('Extrems absoluts en $[0,6]$:', taula_vals([(0, C33(0)), (r'\frac{13}{3}', C33(x33)), (6, C33(6))], 'C', 't')),
             st('a)', r'El màxim és a l’obertura (8.00 h): 2000 €.'),
             st('b)', r'El mínim és a les 12.20 h: 1493 €.'),
             st('c)', r"$C'(t)<0$ en $[0,\frac{13}{3})$ i $C'(t)>0$ en $(\frac{13}{3},6]$; el mínim relatiu és absolut perquè la funció decreix abans i creix després, i el màxim absolut és el valor més gran de la taula."),
             st('d)', r'$TVM[1,2]=\dfrac{C(2)-C(1)}{1}=1640-1793=-153$ €/h; $TVM[5,6]=C(6)-C(5)=1568-1505=63$ €/h.'),
             st('e)', r'Entre les 9 i les 10 h l’efectiu disminueix (153 € per hora) i entre les 13 i les 14 h augmenta (63 € per hora).')],
            r'a) 8.00 h, 2000 €; b) 12.20 h, 1493 €; d) $-153$ €/h i $63$ €/h.')

# 34
c34a, _ = cont(-3, P(2), P(1, 0, 0), fc='l'); c34b, _ = cont(1, P(1, 0, 0), P(1))
b34a, v34a = barrow(P(1, 0, 0), -3, 1); b34b, v34b = barrow(P(1), 1, 2); a34 = ck(v34a + v34b, F(31, 3))
S[34] = SOL([st('a)', 'Els tres trossos són constants o polinomis, contínus en els seus intervals. Punts d’unió:'),
             r'<strong>En $x=-3$:</strong> ' + c34a, r'<strong>En $x=1$:</strong> ' + c34b,
             st('b)', r'$f(x)\ge0$ en $[-3,2]$:' + r'$$A=' + b34a + '$$$$+' + b34b + '$$' + r'$A=\frac{28}{3}+1=\frac{31}{3}\approx10{,}33$ u².'),
             plot([(lambda x: 2, [-4, -3]), (lambda x: x * x, [-2.9999, 0.9999]), (lambda x: 1, [1, 2])], xr=(-4.5, 2.5), yr=(-1, 10),
                  shade=[(lambda x: x * x, None, -3, 1), (lambda x: 1, None, 1, 2)], pts=[(-3, 2), (-3, 9, 'o')])],
            r'a) Contínua en $[-4,2]$ excepte en $x=-3$ (salt); b) $A=\frac{31}{3}$ u²')

# 35
import math as _m
S[35] = SOL([st('a) Esbós.', 'Situem les asímptotes, el tall $(2,0)$ i els mínims $(0,3)$ i $(4,-2)$, i unim respectant el signe i els límits:' +
                plot([(lambda x: 1.2 / (-1 - x), [-6, -1.001]), (lambda x: 3 + 1.5 * x * x / (1 - x * x), [-0.999, 0.999]),
                      (lambda x: 3 ** 1.5 * (2 - x) / (x - 1) ** 1.5, [1.001, 14])], xr=(-6, 12), yr=(-4, 9), va=[-1, 1], ha=[0], pts=[(0, 3), (4, -2), (2, 0)])),
             st('b)', r'A l’esquerra de $x=-1$ la funció puja de $0$ a $+\infty$; entre $-1$ i $1$ baixa des de $+\infty$ fins al mínim $(0,3)$ i torna a pujar; a la dreta de $x=1$ baixa des de $+\infty$ fins al mínim $(4,-2)$ i després puja cap a $0$.' +
                taula_m([('(-\\infty,-1)', '+'), ('(-1,0)', '-'), ('(0,1)', '+'), ('(1,4)', '-'), ('(4,+\\infty)', '+')]))],
            r'Creixent en $(-\infty,-1)\cup(0,1)\cup(4,+\infty)$; decreixent en $(-1,0)\cup(1,4)$.')

# 36
c36a, _ = cont(2, P(1, 2), P(1, -6, 12)); ck(P(1, -6, 12)(4), 4)
f36 = P(1, -6, 12); rows36 = [(0, F(2)), (2, F(4)), (3, f36(3)), (4, f36(4))]; e36, M36, m36 = extrems_abs(rows36)
b36a, v36a = barrow(P(1, 2), 0, 2); b36b, v36b = barrow(f36, 2, 3); a36 = ck(v36a + v36b, F(28, 3))
S[36] = SOL([st('a)', r'En $x=2$: ' + c36a + r' En $x=4$: $\displaystyle\lim_{x\to4^-}(x^2-6x+12)=4=f(4)$ i $\displaystyle\lim_{x\to4^+}(-2x+a)=a-8$. Contínua si $a-8=4\iff a=12$.'),
             st('b)', r"En $[0,2)$, $f(x)=x+2$ és creixent. En $[2,4]$, $f'(x)=2x-6=0\iff x=3$. Candidats: extrems de l’interval, punt d’unió i punt crític:" + taula_vals(rows36) + e36),
             st('c)', r'$f>0$ en $[0,3]$. $$A=' + b36a + '$$$$+' + b36b + r'$$ $A=6+\frac{10}{3}=\frac{28}{3}\approx9{,}33$ u².'),
             plot([(lambda x: x + 2, [0, 2]), (lambda x: x * x - 6 * x + 12, [2, 4]), (lambda x: -2 * x + 12, [4, 8])], xr=(-0.5, 8.5), yr=(-1, 6),
                  shade=[(lambda x: x + 2, None, 0, 2), (lambda x: x * x - 6 * x + 12, None, 2, 3)], pts=[(0, 2), (2, 4), (3, 3), (4, 4)])],
            r'a) $a=12$; b) màxim absolut 4 (en $x=2$ i $x=4$), mínim absolut 2 (en $x=0$); c) $\frac{28}{3}$ u².')

# 37
s37, r37 = estudi(R(P(1, 0, 4), P(2, -3)), lab={'dom': 'a)', 'asi': 'b)', 'mon': 'c)', 'ext': 'd)', 'gra': 'e)'})
S[37] = SOL(s37, resum(r37))
ck(R(P(1, 0, 4), P(2, -3))(F(4)), 4)

# 38
f38 = P(1, -9, 24, 3); s38, a38 = area_steps(f38, 0, 5); ck(a38, F(385, 4)); ck(f38(2), 23); ck(f38(4), 19)
S[38] = SOL([st('a)', r"$y'=3x^2-18x+24=3(x-2)(x-4)=0\iff x=2,\ x=4$. $y''=6x-18$: $y''(2)=-6<0$ → màxim local $(2,\,23)$; $y''(4)=6>0$ → mínim local $(4,\,19)$."),
             st('b)', r'El mínim local val 19 i $f(0)=3$, $f(5)=23$: la funció és positiva en $[0,5]$.')] + s38[1:] +
            [gq(f38, 0, 5, xr=(-0.5, 5.5), pts=[(2, 23), (4, 19)], shade=[(lambda x: f38(float(x)), None, 0, 5)])],
            r'a) Màxim $(2,23)$, mínim $(4,19)$; b) $A=\frac{385}{4}=96{,}25$ u².')

# 39
f39 = P(1, -6, 9, 1); rows39 = [(1, f39(1)), (3, f39(3)), (4, f39(4))]; e39, _, _ = extrems_abs(rows39)
c39, _ = cont(1, P(2, 3), f39)
S[39] = SOL([st('a)', r"$f'(x)=3x^2-12x+9=3(x-1)(x-3)=0\iff x=1,\ x=3$. Avaluem en els punts crítics i en els extrems de $[1,4]$:" + taula_vals(rows39) + e39),
             st('b)', r'Els dos trossos són polinomis, continus en els seus intervals. En $x=1$: ' + c39 + ' Per tant $f$ és contínua en $[0,4]$.')],
            r'a) Màxim absolut 5 (en $x=1$ i $x=4$), mínim absolut 1 (en $x=3$); b) contínua en $[0,4]$.')

# 40
s40, r40 = estudi(R(P(1, 0, 0), P(-1, 0, 4)), lab={'dom': 'a)', 'asi': 'b)', 'mon': 'c)', 'ext': 'd)', 'gra': 'e)'})
S[40] = SOL(s40, resum(r40))
