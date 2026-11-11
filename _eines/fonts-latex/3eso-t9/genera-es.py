# Versió en castellà de genera.py. Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex (3r ESO, Unitat 9: Perímetres i àrees. Teorema de Pitàgores)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Cada resultat numèric es comprova amb ck(valor exacte, valor escrit, decimals de l'arrodoniment).
import os, re, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- comprovacions ----------
pi, S, R = sp.pi, sp.sqrt, sp.Rational
def Q(v): return sp.nsimplify(v, rational=True) if isinstance(v, float) else sp.nsimplify(v)
def ck(v, w, d=None):
    """v: valor exacte; w: el que escrivim (nombre o text amb coma); d: decimals de l'arrodoniment (None = exacte)"""
    w = float(w.replace(',', '.')) if isinstance(w, str) else w
    if d is None: assert sp.simplify(Q(v) - Q(w)) == 0, (v, w)
    else: assert abs(float(v) - float(w)) <= 0.5 * 10 ** -d + 1e-9, (v, float(v), w, d)
def hyp(a, b): return S(Q(a) ** 2 + Q(b) ** 2)
def leg(c, b): return S(Q(c) ** 2 - Q(b) ** 2)
def kind(a, b, c):
    a, b, c = sorted([Q(a), Q(b), Q(c)])
    return 'rect' if c * c == a * a + b * b else 'acut' if c * c < a * a + b * b else 'obt'

# ---------- figures (TikZ) ----------
ST = {'gf': 'fill=teal!12,draw=teal,thick', 'tr': 'fill=accent!22,draw=accent,thick', 'sh': 'fill=navy!18,draw=navy,thick',
      'hole': 'fill=white,draw=white', 'gc': 'draw=teal,thick', 'd': 'dashed,muted', '': 'thick', 'lawn': 'fill=teal!25,draw=teal,thick'}
def P_(p): return '(%.3f,%.3f)' % (float(p[0]), float(p[1]))
def tz(items, s=0.5):
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center),line join=round]' % (s, s)]
    for it in items:
        k = it[0]
        if k == 'poly': o.append(r'\draw[%s] %s -- cycle;' % (ST[it[2]], ' -- '.join(P_(p) for p in it[1])))
        elif k == 'seg': o.append(r'\draw[%s] %s -- %s;' % (ST[it[3] if len(it) > 3 else ''], P_(it[1]), P_(it[2])))
        elif k == 'ra':
            V, A, B = it[1], it[2], it[3]; q = 0.22 / s
            def u(Pp):
                dx, dy = Pp[0] - V[0], Pp[1] - V[1]; n = math.hypot(dx, dy); return dx / n * q, dy / n * q
            ua, ub = u(A), u(B)
            o.append(r'\draw[thin] %s -- %s -- %s;' % (P_((V[0] + ua[0], V[1] + ua[1])), P_((V[0] + ua[0] + ub[0], V[1] + ua[1] + ub[1])), P_((V[0] + ub[0], V[1] + ub[1]))))
        elif k == 'lab': o.append(r'\node[font=\small,%s] at %s {%s};' % (it[3] if len(it) > 3 else 'inner sep=1pt', P_(it[1]), it[2]))
        elif k == 'circ': o.append(r'\draw[%s] %s circle[radius=%s];' % (ST[it[3]], P_(it[1]), it[2]))
        elif k == 'sect':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]; A0 = (C[0] + r * math.cos(math.radians(a0)), C[1] + r * math.sin(math.radians(a0)))
            o.append(r'\draw[%s] %s -- %s arc[start angle=%s,end angle=%s,radius=%s] -- cycle;' % (ST[it[5]], P_(C), P_(A0), a0, a1, r))
        elif k == 'arc':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]; A0 = (C[0] + r * math.cos(math.radians(a0)), C[1] + r * math.sin(math.radians(a0)))
            o.append(r'\draw[%s] %s arc[start angle=%s,end angle=%s,radius=%s];' % (ST[it[5] if len(it) > 5 else ''], P_(A0), a0, a1, r))
        elif k == 'leaf':
            a = it[1]; o.append(r'\draw[%s] (%s,0) arc[start angle=0,end angle=90,radius=%s] arc[start angle=180,end angle=270,radius=%s] -- cycle;' % (ST[it[2]], a, a, a))
        elif k == 'dot': o.append(r'\fill %s circle (1.4pt);' % P_(it[1]))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def rtri(a, b, la, lb, lc, s=0.15):
    """triangle rectangle de catets a (horitzontal) i b (vertical)"""
    return tz([('poly', [(0, 0), (a, 0), (0, b)], 'tr'), ('ra', (0, 0), (1, 0), (0, 1)), ('lab', (a / 2, 0), la, 'below'), ('lab', (0, b / 2), lb, 'left'), ('lab', (a / 2, b / 2), lc, 'above right')], s)

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. El teorema de Pitàgores
# =====================================================================
for a, b, w, d in [(6, 8, 10, None), (5, 12, 13, None), (9, 40, 41, None), (3, 7, 7.62, 2), (1.5, 2, 2.5, None), (10, 10, 14.14, 2)]: ck(hyp(a, b), w, d)
for c, b, w, d in [(25, 7, 24, None), (17, 8, 15, None), (10, 8, 6, None), (12, 5, 10.91, 2), (6.5, 2.5, 6, None), (9, 4, 8.06, 2)]: ck(leg(c, b), w, d)
ck(hyp(12, 16), 20); ck(leg(13, 5), 12); ck(leg(17, 15), 8)
ck(leg(6.5, 2.5), 6); ck(leg(50, 30), 40); ck(hyp(9, 12), 15); ck(hyp(6, 0.8), 6.05, 2)
x = sp.Symbol('x'); assert sp.solve(x ** 2 + (x + 2) ** 2 - 100, x) == [-8, 6]; assert sp.solve(x ** 2 + 9 - (9 - x) ** 2, x) == [4]
S_.append(("El teorema de Pitágoras", [
 (1, r"Calcula la hipotenusa de un triángulo rectángulo cuyos catetos miden (si no es exacta, redondea a las centésimas):" + tasks(3, [r"6 cm y 8 cm", r"5 cm y 12 cm", r"9 m y 40 m", r"3 cm y 7 cm", r"1,5 m y 2 m", r"10 cm y 10 cm"])
     + recorda(r"En un triángulo rectángulo, $c^2=a^2+b^2$, donde $c$ es la \textbf{hipotenusa} (el lado opuesto al ángulo recto, el más largo) y $a$, $b$ son los \textbf{catetos}. Para la hipotenusa sumamos: $c=\sqrt{a^2+b^2}$; para un cateto restamos: $a=\sqrt{c^2-b^2}$."),
     tasks(3, [r"$\sqrt{100}=\res{10\text{ cm}}$", r"$\sqrt{169}=\res{13\text{ cm}}$", r"$\sqrt{1681}=\res{41\text{ m}}$", r"$\sqrt{58}\approx\res{7{,}62\text{ cm}}$", r"$\sqrt{6{,}25}=\res{2{,}5\text{ m}}$", r"$\sqrt{200}\approx\res{14{,}14\text{ cm}}$"])),
 (1, r"Calcula el cateto que falta en cada triángulo rectángulo ($c$ es la hipotenusa):" + tasks(3, [r"$c=25$, $b=7$", r"$c=17$, $a=8$", r"$c=10$, $b=8$", r"$c=12$, $b=5$", r"$c=6{,}5$, $a=2{,}5$", r"$c=9$, $a=4$"]),
     tasks(3, [r"$\sqrt{576}=\res{24}$", r"$\sqrt{225}=\res{15}$", r"$\sqrt{36}=\res{6}$", r"$\sqrt{119}\approx\res{10{,}91}$", r"$\sqrt{36}=\res{6}$", r"$\sqrt{65}\approx\res{8{,}06}$"])),
 (1, r"Calcula la longitud $x$ en cada triángulo rectángulo (medidas en cm):\par\smallskip\begin{center}"
     + rtri(12, 16, '12', '16', '$x$') + r'\qquad ' + rtri(12, 5, '$x$', '5', '13') + r'\qquad ' + rtri(15, 8, '15', '$x$', '17') + r'\end{center}',
     r"a) $x=\sqrt{144+256}=\res{20}$ \qquad b) $x=\sqrt{169-25}=\res{12}$ \qquad c) $x=\sqrt{289-225}=\res{8}$"),
 (2, r"Una escalera de 6,5 m está apoyada en una pared. El pie de la escalera está a 2,5 m de la pared. ¿A qué altura de la pared llega?",
     r"La escalera es la hipotenusa: $h=\sqrt{6{,}5^2-2{,}5^2}=\sqrt{42{,}25-6{,}25}=\sqrt{36}=\res{6\text{ m}}$."),
 (2, r"Volamos una cometa con un hilo de 50 m tenso. Si estamos a 30 m (en horizontal) del punto del suelo que hay justo debajo de la cometa, ¿a qué altura vuela? (No tengas en cuenta la altura de la mano.)",
     r"$h=\sqrt{50^2-30^2}=\sqrt{1600}=\res{40\text{ m}}$."),
 (2, r"Un barco sale del puerto y navega 9 km hacia el norte y, después, 12 km hacia el este. ¿A qué distancia en línea recta se encuentra del puerto?",
     r"Los dos tramos son perpendiculares: $d=\sqrt{9^2+12^2}=\sqrt{225}=\res{15\text{ km}}$."),
 (2, r"Una rampa salva un desnivel de 0,8 m y ocupa 6 m en horizontal. ¿Cuánto mide la rampa?",
     r"$\sqrt{6^2+0{,}8^2}=\sqrt{36{,}64}\approx\res{6{,}05\text{ m}}$."),
 (3, r"En un triángulo rectángulo, un cateto mide 2 cm más que el otro y la hipotenusa mide 10 cm. ¿Cuánto miden los catetos?",
     r"$x^2+(x+2)^2=100\Rightarrow 2x^2+4x-96=0\Rightarrow x^2+2x-48=0\Rightarrow x=\frac{-2\pm14}{2}$: $x=6$ ($x=-8$ no tiene sentido). Catetos: $\res{6\text{ cm y }8\text{ cm}}$."),
 (3, r"Un poste vertical de 9 m se rompe por el viento y la punta toca el suelo a 3 m de la base (la parte de abajo sigue recta). ¿A qué altura se ha roto?",
     r"Si se rompe a altura $x$, el trozo caído mide $9-x$ y es la hipotenusa: $x^2+3^2=(9-x)^2\Rightarrow x^2+9=81-18x+x^2\Rightarrow18x=72\Rightarrow\res{x=4\text{ m}}$."),
]))

# =====================================================================
# 2. Classificació de triangles pels costats
# =====================================================================
for t, k in [((5, 12, 13), 'rect'), ((6, 7, 8), 'acut'), ((4, 6, 9), 'obt'), ((10, 24, 26), 'rect'), ((7, 8, 12), 'obt'), ((9, 10, 11), 'acut'), ((4, 4, 7), 'obt'), ((1.5, 2, 2.5), 'rect')]: assert kind(*t) == k, t
for t, ok in [((12, 16, 20), True), ((9, 12, 16), False), ((15, 36, 39), True), ((11, 60, 61), True), ((8, 9, 12), False)]: assert (t[0] ** 2 + t[1] ** 2 == t[2] ** 2) == ok
ck(hyp(90, 120), 150); assert 152 ** 2 > 150 ** 2; ck(hyp(9, 12), 15); ck(leg(12, 9), 7.94, 2)
assert [x_ for x_ in range(9, 14) if x_ * x_ < 100] == [9] and [x_ for x_ in range(9, 14) if x_ * x_ > 100] == [11, 12, 13]
S_.append(("Clasificación de triángulos por los lados", [
 (1, r"Clasifica según los ángulos (acutángulo, rectángulo u obtusángulo) los triángulos de lados:" + tasks(3, [r"5, 12 y 13", r"6, 7 y 8", r"4, 6 y 9", r"10, 24 y 26", r"7, 8 y 12", r"9, 10 y 11"])
     + recorda(r"Si $c$ es el lado más largo: $c^2<a^2+b^2$ \ $\Rightarrow$ acutángulo; \ $c^2=a^2+b^2$ \ $\Rightarrow$ rectángulo; \ $c^2>a^2+b^2$ \ $\Rightarrow$ obtusángulo."),
     tasks(3, [r"$169=169$: \rest{rectángulo}", r"$64<85$: \rest{acutángulo}", r"$81>52$: \rest{obtusángulo}", r"$676=676$: \rest{rectángulo}", r"$144>113$: \rest{obtusángulo}", r"$121<181$: \rest{acutángulo}"])),
 (1, r"¿Cuáles de estas ternas son pitagóricas?" + tasks(5, [r"12, 16, 20", r"9, 12, 16", r"15, 36, 39", r"11, 60, 61", r"8, 9, 12"]),
     tasks(5, [r"\rest{sí}", r"no", r"\rest{sí}", r"\rest{sí}", r"no"]) + r"($144+256=400$; $81+144=225\neq256$; $225+1296=1521$; $121+3600=3721$; $64+81=145\neq144$.)"),
 (2, r"¿Pueden ser los lados de un triángulo? Si es así, clasifícalo." + tasks(3, [r"3, 5 y 9", r"4, 4 y 7", r"5, 7 y 12"]),
     tasks(3, [r"\rest{no}: $9>3+5$", r"\rest{sí}, obtusángulo ($49>32$)", r"\rest{no}: $12=5+7$"])),
 (2, r"Un triángulo tiene los lados de 1,5 m, 2 m y 2,5 m. ¿Es rectángulo? Si lo es, calcula su área tomando los catetos como base y altura.",
     r"$2{,}25+4=6{,}25=2{,}5^2$: \rest{sí}, es rectángulo. \ $A=\frac{1{,}5\cdot2}{2}=\res{1{,}5\text{ m}^2}$."),
 (2, r"Un carpintero quiere comprobar si una estantería de 90 cm × 120 cm tiene los ángulos rectos. ¿Cuánto tiene que medir la diagonal? Si la mide y le da 152 cm, ¿cómo es el ángulo?",
     r"$\sqrt{90^2+120^2}=\res{150\text{ cm}}$. Con 152 cm: $152^2>150^2$, el ángulo opuesto a la diagonal es \rest{obtuso} (más de 90°)."),
 (3, r"¿Cuánto tiene que medir $x$ para que el triángulo de lados 9, 12 y $x$ sea rectángulo? Hay dos posibilidades.",
     r"Si $x$ es la hipotenusa: $x=\sqrt{81+144}=\res{15}$. \ Si la hipotenusa es 12: $x=\sqrt{144-81}=\sqrt{63}\approx\res{7{,}94}$."),
 (3, r"El triángulo tiene lados 6, 8 y $x$, con $x$ un número entero mayor que 8. ¿Para qué valores de $x$ es acutángulo? ¿Y rectángulo? ¿Y obtusángulo?",
     r"Comparamos $x^2$ con $36+64=100$, y además tiene que ser $x<6+8=14$. \ Acutángulo: $\res{x=9}$; \ rectángulo: $\res{x=10}$; \ obtusángulo: $\res{x=11,\,12,\,13}$."),
]))

# =====================================================================
# 3. Aplicacions del teorema de Pitàgores
# =====================================================================
ck(hyp(20, 15), 25); ck(hyp(7, 7), 9.90, 2); ck(hyp(2.4, 1), 2.6); ck(leg(17, 8), 15); ck(leg(12, 6), 10.39, 2); ck(hyp(9, 12), 15)
ck(S(72), 8.49, 2); ck(4 * S(72), 33.94, 2); ck(hyp(6, 8), 10); ck(leg(13, 5), 12)
ck(hyp(3, 4), 5); ck(hyp(6, 8), 10); ck(hyp(4, 5), 6.40, 2); ck(leg(10, 6), 8)
dk = R(8128, 100) / S(337); ck(R(8128, 100), 81.28); ck(16 * dk, 70.8, 1); ck(9 * dk, 39.8, 1)
S_.append(("Aplicaciones del teorema de Pitágoras", [
 (1, r"Calcula la diagonal de:" + tasks(3, [r"un rectángulo de 20 × 15 cm", r"un cuadrado de 7 cm de lado", r"una puerta de 2,4 × 1 m"])
     + recorda(r"Busca el triángulo rectángulo escondido: la diagonal de un rectángulo, la altura de un triángulo isósceles o equilátero, la mitad de las diagonales de un rombo o la altura de un trapecio forman uno. Decide qué lado es la hipotenusa y aplica Pitágoras."),
     tasks(3, [r"$\sqrt{625}=\res{25\text{ cm}}$", r"$\sqrt{98}\approx\res{9{,}90\text{ cm}}$", r"$\sqrt{6{,}76}=\res{2{,}6\text{ m}}$"])),
 (1, r"Calcula la altura de un triángulo isósceles de lados iguales de 17 cm y base de 16 cm, y la de un triángulo equilátero de 12 cm de lado.",
     r"Isósceles: $h=\sqrt{17^2-8^2}=\sqrt{225}=\res{15\text{ cm}}$. \ Equilátero: $h=\sqrt{12^2-6^2}=\sqrt{108}\approx\res{10{,}39\text{ cm}}$."),
 (1, r"Las diagonales de un rombo miden 18 cm y 24 cm. Calcula su lado y su perímetro.",
     r"$l=\sqrt{9^2+12^2}=\sqrt{225}=\res{15\text{ cm}}$; \ $P=4\cdot15=\res{60\text{ cm}}$."),
 (2, r"La diagonal de un cuadrado mide 12 cm. Calcula su lado y su perímetro.",
     r"$l^2+l^2=144\Rightarrow l=\sqrt{72}\approx\res{8{,}49\text{ cm}}$; \ $P=4\sqrt{72}\approx\res{33{,}94\text{ cm}}$."),
 (2, r"Un trapecio rectángulo tiene las bases de 15 cm y 9 cm y la altura de 8 cm. Calcula el lado oblicuo y el perímetro.",
     r"$c=\sqrt{(15-9)^2+8^2}=\sqrt{100}=\res{10\text{ cm}}$; \ $P=15+9+8+10=\res{42\text{ cm}}$."),
 (2, r"Un trapecio isósceles tiene las bases de 22 cm y 12 cm y los lados no paralelos de 13 cm. Calcula su altura.",
     r"$\frac{22-12}{2}=5$; \ $h=\sqrt{13^2-5^2}=\sqrt{144}=\res{12\text{ cm}}$."),
 (2, r"Calcula la distancia entre los puntos:" + tasks(3, [r"$A(2,\,1)$ y $B(5,\,5)$", r"$C(-3,\,4)$ y $D(3,\,-4)$", r"$E(0,\,-2)$ y $F(4,\,3)$"])
     + recorda(r"$d(A,\,B)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$: es la hipotenusa de un triángulo rectángulo cuyos catetos son la diferencia de las $x$ y la de las $y$."),
     tasks(3, [r"$\sqrt{9+16}=\res{5}$", r"$\sqrt{36+64}=\res{10}$", r"$\sqrt{16+25}=\sqrt{41}\approx\res{6{,}40}$"])),
 (3, r"Sea el triángulo de vértices $A(1,\,1)$, $B(7,\,1)$ y $C(4,\,5)$. Calcula sus lados y su perímetro, y di cómo es según los lados y según los ángulos.",
     r"$AB=6$, \ $AC=\sqrt{9+16}=5$, \ $BC=\sqrt{9+16}=5$: \rest{isósceles}, $P=\res{16}$. \ $36<25+25$: \rest{acutángulo}."),
 (3, r"Un rombo tiene 10 cm de lado y una diagonal de 12 cm. ¿Cuánto mide la otra diagonal?",
     r"Mitad de la otra diagonal: $\sqrt{10^2-6^2}=8$; \ diagonal: $\res{16\text{ cm}}$."),
 (3, r"Un televisor de 32 pulgadas tiene la pantalla de proporción 16:9 (la anchura y la altura son $16k$ y $9k$). Las pulgadas miden la diagonal y 1 pulgada son 2,54 cm. Calcula la anchura y la altura de la pantalla.",
     r"$d=32\cdot2{,}54=81{,}28$ cm. \ $(16k)^2+(9k)^2=81{,}28^2\Rightarrow337k^2=6606{,}44\Rightarrow k\approx4{,}43$. \ Anchura $\approx\res{70{,}8\text{ cm}}$, altura $\approx\res{39{,}8\text{ cm}}$."),
]))
ck(R(8128, 100) ** 2, 6606.4384, 4); ck(dk, 4.43, 2); assert kind(6, 5, 5) == 'acut'

# =====================================================================
# 4. Perímetres i àrees de triangles i quadrilàters
# =====================================================================
ck(hyp(8, 6), 10); ck(leg(13, 5), 12); ck(16 * S(3), 27.71, 2); ck(leg(8, 4), 6.93, 2)
ck(R(117, 10) - R(12, 10), 10.5); assert math.ceil(10.5 / 4) == 3
ck(leg(10, 8), 6); ck(hyp(20, 15), 25); ck(R(2 * 150, 25), 12)
b_ = sp.Symbol('b'); assert sorted(sp.solve(b_ ** 2 + (17 - b_) ** 2 - 169, b_)) == [5, 12]
S_.append(("Perímetros y áreas de triángulos y cuadriláteros", [
 (1, r"Calcula el área y el perímetro de:" + tasks(2, [r"un cuadrado de 9 cm de lado", r"un rectángulo de 12 cm × 5 cm", r"un romboide de base 10 cm, altura 6 cm y lado oblicuo 7 cm", r"un rombo de diagonales 16 cm y 12 cm"])
     + recorda(r"Cuadrado $A=l^2$; \ rectángulo y romboide $A=b\cdot h$; \ rombo $A=\frac{D\cdot d}{2}$; \ trapecio $A=\frac{(B+b)\cdot h}{2}$; \ triángulo $A=\frac{b\cdot h}{2}$. El perímetro es la suma de los lados."),
     tasks(2, [r"$A=\res{81\text{ cm}^2}$, $P=\res{36\text{ cm}}$", r"$A=\res{60\text{ cm}^2}$, $P=\res{34\text{ cm}}$", r"$A=\res{60\text{ cm}^2}$, $P=\res{34\text{ cm}}$", r"$A=\res{96\text{ cm}^2}$; $l=\sqrt{64+36}=10$, $P=\res{40\text{ cm}}$"])),
 (1, r"Calcula el área de:" + tasks(2, [r"un trapecio de bases 11 m y 7 m y altura 5 m", r"un triángulo de 14 cm de base y 9 cm de altura"]),
     tasks(2, [r"$\frac{(11+7)\cdot5}{2}=\res{45\text{ m}^2}$", r"$\frac{14\cdot9}{2}=\res{63\text{ cm}^2}$"])),
 (1, r"Expresa en la unidad que se indica:" + tasks(4, [r"$3{,}5\text{ m}^2$ en cm²", r"$45\,000\text{ cm}^2$ en m²", r"$2{,}3\text{ ha}$ en m²", r"$750\text{ dm}^2$ en m²"]),
     tasks(4, [r"$\res{35\,000\text{ cm}^2}$", r"$\res{4{,}5\text{ m}^2}$", r"$\res{23\,000\text{ m}^2}$", r"$\res{7{,}5\text{ m}^2}$"])),
 (1, r"Un rectángulo tiene 72 cm² de área y 9 cm de base. Calcula su altura y su perímetro.",
     r"$h=\frac{72}{9}=\res{8\text{ cm}}$; \ $P=2\cdot9+2\cdot8=\res{34\text{ cm}}$."),
 (2, r"Calcula el área de un triángulo equilátero de 8 cm de lado.",
     r"$h=\sqrt{64-16}=\sqrt{48}\approx6{,}93$ cm; \ $A=\frac{8\cdot\sqrt{48}}{2}\approx\res{27{,}71\text{ cm}^2}$."),
 (2, r"Calcula el área y el perímetro de un triángulo isósceles de lados iguales de 10 cm y base de 12 cm.",
     r"$h=\sqrt{100-36}=8$; \ $A=\frac{12\cdot8}{2}=\res{48\text{ cm}^2}$; \ $P=\res{32\text{ cm}}$."),
 (2, r"Calcula el área y el perímetro de un trapecio isósceles de bases 20 cm y 10 cm y lados no paralelos de 13 cm.",
     r"$h=\sqrt{13^2-5^2}=12$; \ $A=\frac{(20+10)\cdot12}{2}=\res{180\text{ cm}^2}$; \ $P=20+10+2\cdot13=\res{56\text{ cm}}$."),
 (2, r"Un rombo tiene 40 cm de perímetro y una diagonal de 16 cm. Calcula su área.",
     r"$l=10$; mitad de la otra diagonal $\sqrt{100-64}=6$, \ $d=12$; \ $A=\frac{16\cdot12}{2}=\res{96\text{ cm}^2}$."),
 (2, r"Un campo rectangular mide 120 m × 85 m. Expresa su superficie en m² y en hectáreas. ¿Cuánto costará sembrar césped a 3 € el m²?",
     r"$A=\res{10\,200\text{ m}^2}=\res{1{,}02\text{ ha}}$; \ coste: $\res{30\,600\text{ €}}$."),
 (3, r"Queremos pintar una pared de 4,5 m × 2,6 m que tiene una ventana de 1,2 m × 1 m. Si un bote de pintura cubre 4 m², ¿cuántos botes tenemos que comprar?",
     r"$A=4{,}5\cdot2{,}6-1{,}2\cdot1=11{,}7-1{,}2=10{,}5\text{ m}^2$; \ $\frac{10{,}5}{4}=2{,}625$: \ $\res{3\text{ botes}}$."),
 (3, r"Los catetos de un triángulo rectángulo miden 20 cm y 15 cm. Calcula su área, la hipotenusa y la altura sobre la hipotenusa.",
     r"$A=\frac{20\cdot15}{2}=\res{150\text{ cm}^2}$; \ $c=\sqrt{625}=\res{25\text{ cm}}$. Tomando la hipotenusa como base: $\frac{25\cdot h}{2}=150\Rightarrow\res{h=12\text{ cm}}$."),
 (3, r"Un rectángulo tiene 34 cm de perímetro y 13 cm de diagonal. ¿Cuánto miden los lados? ¿Cuál es el área?",
     r"$b+h=17$ y $b^2+h^2=169$: \ $b^2+(17-b)^2=169\Rightarrow b^2-17b+60=0\Rightarrow b=12$ o $b=5$. Lados $\res{12\text{ cm y }5\text{ cm}}$; \ $A=\res{60\text{ cm}^2}$."),
]))

# =====================================================================
# 5. Polígons regulars
# =====================================================================
ck(30 * R(413, 100) / 2, 61.95); ck(30 * R(433, 100) / 2, 64.95); ck(32 * R(483, 100) / 2, 77.28)
ck(leg(8, 4), 6.93, 2); ck(48 * leg(8, 4) / 2, 166.28, 2)
ck(leg(R(102, 10), 6), 8.25, 2); ck(60 * leg(R(102, 10), 6) / 2, 247.5, 1); ck(60 * R(825, 100) / 2, 247.5, 1)
ck(S(72), 8.49, 2); ck(S(72) / 2, 4.24, 2)
Ah = 6 * 10 * leg(10, 5) / 2; ck(Ah, 259.81, 2); ck(30000 / Ah, 115.5, 1); assert math.ceil(float(30000 / Ah)) == 116
ck(leg(4, 2), 3.46, 2); ck(2 * leg(4, 2), 6.93, 2); ck(3 * 2 * leg(4, 2) * 2 / 2, 20.78, 2)
S_.append(("Polígonos regulares", [
 (1, r"Calcula el perímetro y el área de los polígonos regulares:" + tasks(1, [r"pentágono de 6 cm de lado y 4,13 cm de apotema", r"hexágono de 5 cm de lado y 4,33 cm de apotema", r"octógono de 4 cm de lado y 4,83 cm de apotema"])
     + recorda(r"En un polígono regular, $A=\frac{P\cdot a}{2}$, donde $P$ es el perímetro y $a$ la apotema. El radio, la apotema y medio lado forman un triángulo rectángulo: $r^2=a^2+\left(\frac l2\right)^2$. En el hexágono regular, $r=l$."),
     tasks(1, [r"$P=\res{30\text{ cm}}$, \ $A=\frac{30\cdot4{,}13}{2}=\res{61{,}95\text{ cm}^2}$", r"$P=\res{30\text{ cm}}$, \ $A=\frac{30\cdot4{,}33}{2}=\res{64{,}95\text{ cm}^2}$", r"$P=\res{32\text{ cm}}$, \ $A=\frac{32\cdot4{,}83}{2}=\res{77{,}28\text{ cm}^2}$"])),
 (1, r"Un hexágono regular tiene 8 cm de lado. ¿Cuánto mide el radio? Calcula su apotema y su área.",
     r"$r=l=\res{8\text{ cm}}$; \ $a=\sqrt{64-16}=\sqrt{48}\approx\res{6{,}93\text{ cm}}$; \ $A=\frac{48\cdot\sqrt{48}}{2}\approx\res{166{,}28\text{ cm}^2}$."),
 (2, r"Un pentágono regular tiene 12 cm de lado y 10,2 cm de radio. Calcula su apotema y su área.",
     r"$a=\sqrt{10{,}2^2-6^2}=\sqrt{68{,}04}\approx\res{8{,}25\text{ cm}}$; \ $A\approx\frac{60\cdot8{,}25}{2}\approx\res{247{,}5\text{ cm}^2}$."),
 (2, r"Un cuadrado está inscrito en una circunferencia de 6 cm de radio. Calcula su lado, su apotema y su área.",
     r"La diagonal es un diámetro: $l^2+l^2=12^2\Rightarrow l=\sqrt{72}\approx\res{8{,}49\text{ cm}}$; \ $a=\frac l2\approx\res{4{,}24\text{ cm}}$; \ $A=l^2=\res{72\text{ cm}^2}$."),
 (2, r"Queremos cubrir 3 m² de pared con baldosas en forma de hexágono regular de 10 cm de lado. ¿Cuántas baldosas hacen falta, como mínimo?",
     r"$a=\sqrt{100-25}=\sqrt{75}$; \ $A=\frac{60\cdot\sqrt{75}}{2}\approx259{,}81\text{ cm}^2$. \ $\frac{30\,000}{259{,}81}\approx115{,}5$: \ $\res{116\text{ baldosas}}$."),
 (3, r"Un triángulo equilátero está inscrito en una circunferencia de 4 cm de radio. Sabiendo que su apotema es la mitad del radio, calcula su lado y su área.",
     r"$a=2$; \ $\frac l2=\sqrt{4^2-2^2}=\sqrt{12}\approx3{,}46\Rightarrow l\approx\res{6{,}93\text{ cm}}$; \ $A=\frac{3\cdot2\sqrt{12}\cdot2}{2}\approx\res{20{,}78\text{ cm}^2}$."),
]))

# =====================================================================
# 6. La circumferència: longitud i arcs
# =====================================================================
ck(14 * pi, 43.98, 2); ck(15 * pi, 47.12, 2); ck(5 * pi, 15.71, 2); ck(R(6283, 100) / (2 * pi), 10, 2)
ck(2 * pi * 8 / 4, 12.57, 2); ck(2 * pi * 12 * 30 / 360, 6.28, 2); ck(2 * pi * 4 * 225 / 360, 15.71, 2)
ck(150000 / (60 * pi), 795.8, 1); ck(200 + 73 * pi, 429.34, 2); ck(2 * pi * 15 / 3, 31.42, 2)
ck(R(1885, 100) * 360 / (24 * pi), 90, 1); vT = 2 * pi * 150 * 10 ** 6 / (365 * 24); ck(vT, 107589, 0)
S_.append(("La circunferencia: longitud y arcos", [
 (1, r"Calcula la longitud de la circunferencia de:" + tasks(3, [r"7 cm de radio", r"15 cm de diámetro", r"2,5 m de radio"])
     + recorda(r"$L=2\pi r=\pi d$. \ Un arco de $n^\circ$ mide $L_{\text{arco}}=\frac{2\pi r\cdot n}{360}$. Usa la tecla $\pi$ de la calculadora y redondea solo al final."),
     tasks(3, [r"$14\pi\approx\res{43{,}98\text{ cm}}$", r"$15\pi\approx\res{47{,}12\text{ cm}}$", r"$5\pi\approx\res{15{,}71\text{ m}}$"])),
 (1, r"Una circunferencia mide 62,83 cm de longitud. ¿Cuánto miden el radio y el diámetro?",
     r"$r=\frac{62{,}83}{2\pi}\approx\res{10\text{ cm}}$; \ $d\approx\res{20\text{ cm}}$."),
 (1, r"Calcula la longitud de los arcos:" + tasks(3, [r"de 90° y 8 cm de radio", r"de 30° y 12 cm de radio", r"de 225° y 4 cm de radio"]),
     tasks(3, [r"$4\pi\approx\res{12{,}57\text{ cm}}$", r"$2\pi\approx\res{6{,}28\text{ cm}}$", r"$5\pi\approx\res{15{,}71\text{ cm}}$"])),
 (2, r"Las ruedas de una bicicleta miden 60 cm de diámetro. ¿Cuántas vueltas da cada rueda en un recorrido de 1,5 km?",
     r"Cada vuelta: $60\pi\approx188{,}50$ cm. \ $\frac{150\,000}{60\pi}\approx\res{795{,}8\text{ vueltas}}$ (unas 796)."),
 (2, r"La cuerda interior de una pista de atletismo está formada por dos rectas de 100 m y dos semicircunferencias de 36,5 m de radio. ¿Cuánto mide una vuelta?",
     r"Las dos semicircunferencias forman una circunferencia: $200+2\pi\cdot36{,}5=200+73\pi\approx\res{429{,}34\text{ m}}$."),
 (2, r"La aguja minutera de un reloj mide 15 cm. ¿Qué distancia recorre su punta en 20 minutos?",
     r"20 min son $\frac13$ de vuelta (120°): \ $\frac{2\pi\cdot15}{3}=10\pi\approx\res{31{,}42\text{ cm}}$."),
 (3, r"En una circunferencia de 12 cm de radio, un arco mide 18,85 cm. ¿Cuántos grados tiene?",
     r"$\frac{2\pi\cdot12\cdot n}{360}=18{,}85\Rightarrow n=\frac{18{,}85\cdot360}{24\pi}\approx\res{90^\circ}$."),
 (3, r"La Tierra da una vuelta al Sol cada año siguiendo una órbita casi circular de 150 millones de km de radio. ¿A qué velocidad media (en km/h) viaja la Tierra?",
     r"$L=2\pi\cdot150\,000\,000\approx942\,477\,796$ km; \ 1 año $=365\cdot24=8760$ h; \ $v=\frac{L}{8760}\approx\res{107\,589\text{ km/h}}$."),
]))
ck(2 * pi * 150 * 10 ** 6, 942477796, 0); ck(60 * pi, 188.50, 2)

# =====================================================================
# 7. Àrea del cercle i figures circulars
# =====================================================================
ck(25 * pi, 78.54, 2); ck(36 * pi, 113.10, 2); ck(R(64, 100) * pi, 2.01, 2)
ck(36 * pi * 60 / 360, 18.85, 2); ck(100 * pi * 150 / 360, 130.90, 2); ck(4 * pi * 270 / 360, 9.42, 2); ck(65 * pi, 204.20, 2)
ck(S(200 / pi), 7.98, 2); ck(2 * pi * S(200 / pi), 50.13, 2); ck(pi * 95 * 80 / 360, 66.32, 2)
ck(25 * pi, 78.54, 2); ck(R(75, 4) * pi, 58.90, 2); ck(leg(5, R(5, 2)) ** 2, R(75, 4))
ck(225 * pi / 8, 88.36, 2); ck(30 * pi / 8, 11.78, 2); ck(6 * pi - 9 * S(3), 3.26, 2); ck(6 * pi, 18.85, 2); ck(9 * S(3), 15.59, 2); ck(S(50), 7.07, 2)
SEG = tz([('sect', (0, 0), 3, 0, 60, 'sh'), ('poly', [(0, 0), (3, 0), (1.5, 1.5 * math.sqrt(3))], 'hole'), ('seg', (0, 0), (3, 0)), ('seg', (0, 0), (1.5, 1.5 * math.sqrt(3))), ('seg', (3, 0), (1.5, 1.5 * math.sqrt(3))),
          ('arc', (0, 0), 3, 0, 60), ('dot', (0, 0)), ('lab', (1.5, 0), '6 cm', 'below'), ('arc', (0, 0), 0.6, 0, 60), ('lab', (0.75, 0.35), r'\scriptsize 60°', 'right')], 0.55)
S_.append(("Área del círculo y figuras circulares", [
 (1, r"Calcula el área del círculo de:" + tasks(3, [r"5 cm de radio", r"12 cm de diámetro", r"0,8 m de radio"])
     + recorda(r"Círculo $A=\pi r^2$; \ sector de $n^\circ$: $A=\frac{\pi r^2\cdot n}{360}$; \ corona: $A=\pi\left(R^2-r^2\right)$; \ trapecio circular: $A=\frac{\pi\left(R^2-r^2\right)\cdot n}{360}$."),
     tasks(3, [r"$25\pi\approx\res{78{,}54\text{ cm}^2}$", r"$36\pi\approx\res{113{,}10\text{ cm}^2}$", r"$0{,}64\pi\approx\res{2{,}01\text{ m}^2}$"])),
 (1, r"Calcula el área de los sectores circulares:" + tasks(3, [r"de 60° y 6 cm de radio", r"de 150° y 10 cm de radio", r"de 270° y 2 cm de radio"]),
     tasks(3, [r"$6\pi\approx\res{18{,}85\text{ cm}^2}$", r"$\frac{125\pi}{3}\approx\res{130{,}90\text{ cm}^2}$", r"$3\pi\approx\res{9{,}42\text{ cm}^2}$"])),
 (1, r"Calcula el área de una corona circular de radios 9 cm y 4 cm.",
     r"$\pi(81-16)=65\pi\approx\res{204{,}20\text{ cm}^2}$."),
 (2, r"Un círculo tiene 200 cm² de área. Calcula su radio y la longitud de la circunferencia.",
     r"$r=\sqrt{\frac{200}{\pi}}\approx\res{7{,}98\text{ cm}}$; \ $L=2\pi r\approx\res{50{,}13\text{ cm}}$."),
 (2, r"Calcula el área de un trapecio circular de radios 12 cm y 7 cm y amplitud 80°.",
     r"$\frac{\pi(144-49)\cdot80}{360}=\frac{190\pi}{9}\approx\res{66{,}32\text{ cm}^2}$."),
 (2, r"Una pizza de 30 cm de diámetro se corta en 8 porciones iguales. Calcula la superficie de cada porción y la longitud de su borde (el arco).",
     r"$A=\frac{225\pi}{8}\approx\res{88{,}36\text{ cm}^2}$; \ arco: $\frac{30\pi}{8}\approx\res{11{,}78\text{ cm}}$."),
 (2, r"Un hexágono regular tiene 30 cm de perímetro. Calcula el área del círculo circunscrito (el que pasa por los vértices) y la del círculo inscrito (el radio es la apotema).",
     r"$l=r=5$: \ circunscrito $25\pi\approx\res{78{,}54\text{ cm}^2}$. \ $a^2=25-6{,}25=18{,}75$: \ inscrito $18{,}75\pi\approx\res{58{,}90\text{ cm}^2}$."),
 (3, r"Calcula el área del segmento circular sombreado, determinado por un ángulo de 60° en un círculo de 6 cm de radio. (El triángulo es equilátero.)\par\smallskip\begin{center}" + SEG + r'\end{center}',
     r"Sector: $\frac{36\pi\cdot60}{360}=6\pi$. \ Triángulo equilátero de lado 6: $h=\sqrt{27}$, $A=3\sqrt{27}\approx15{,}59$. \ Segmento: $6\pi-3\sqrt{27}\approx\res{3{,}26\text{ cm}^2}$."),
 (3, r"Una corona circular tiene un área de $50\pi$ cm² y el radio exterior mide 10 cm. ¿Cuánto mide el radio interior?",
     r"$\pi(100-r^2)=50\pi\Rightarrow r^2=50\Rightarrow r=\sqrt{50}\approx\res{7{,}07\text{ cm}}$."),
]))

# =====================================================================
# 8. Figures compostes i problemes
# =====================================================================
ck(36 + 12, 48); ck(hyp(3, 4), 5); ck(64 + 8 * pi, 89.13, 2); ck(24 + 4 * pi, 36.57, 2); ck(60 - 9 * pi, 31.73, 2); ck(20 + 6 * pi, 38.85, 2)
ck(144 - 36 * pi, 30.90, 2); ck(R(252, 100) + R(49, 100) * pi / 2, 3.29, 2); ck(5 + R(7, 10) * pi, 7.20, 2); ck(29 * 16 - 25 * 12, 164)
ck(50 * pi - 100, 57.08, 2); ck(300 - 75 * pi, 64.38, 2); ck(16 * pi - 24 * S(3), 8.70, 2); ck(R(77, 4) * pi, 60.48, 2)
CASA = tz([('poly', [(0, 0), (6, 0), (6, 6), (3, 10), (0, 6)], 'gf'), ('seg', (0, 6), (6, 6), 'd'), ('seg', (3, 6), (3, 10), 'd'), ('ra', (3, 6), (6, 6), (3, 10)),
           ('lab', (3, 0), '6 m', 'below'), ('lab', (6, 3), '6 m', 'right'), ('lab', (3, 8), '4 m', 'right')], 0.17)
SEMI = tz([('poly', [(0, 0), (8, 0), (8, 8), (0, 8)], 'sh'), ('sect', (4, 8), 4, 0, 180, 'sh'), ('seg', (0, 8), (8, 8), 'd'), ('lab', (4, 0), '8 cm', 'below')], 0.15)
RSC = tz([('poly', [(0, 0), (10, 0), (10, 6), (0, 6)], 'sh'), ('sect', (0, 3), 3, -90, 90, 'hole'), ('sect', (10, 3), 3, 90, 270, 'hole'), ('arc', (0, 3), 3, -90, 90), ('arc', (10, 3), 3, 90, 270),
          ('lab', (5, 0), '10 cm', 'below'), ('lab', (10, 3), '6 cm', 'right')], 0.2)
QC = tz([('poly', [(0, 0), (12, 0), (12, 12), (0, 12)], 'sh'), ('sect', (0, 0), 12, 0, 90, 'hole'), ('arc', (0, 0), 12, 0, 90), ('lab', (6, 0), '12 cm', 'below'), ('seg', (0, 0), (8.485, 8.485), 'd'), ('lab', (4.2, 4.2), '12', 'above left')], 0.13)
FIN = tz([('poly', [(0, 0), (1.4, 0), (1.4, 1.8), (0, 1.8)], 'gf'), ('sect', (0.7, 1.8), 0.7, 0, 180, 'gf'), ('seg', (0, 1.8), (1.4, 1.8), 'd'), ('lab', (0.7, 0), '1,4 m', 'below'), ('lab', (1.4, 0.9), '1,8 m', 'right')], 0.75)
LEAF = tz([('poly', [(0, 0), (10, 0), (10, 10), (0, 10)], 'gf'), ('leaf', 10, 'sh'), ('lab', (5, 0), '10 cm', 'below')], 0.15)
CIR3 = tz([('poly', [(0, 0), (30, 0), (30, 10), (0, 10)], 'sh'), ('circ', (5, 5), 5, 'hole'), ('circ', (15, 5), 5, 'hole'), ('circ', (25, 5), 5, 'hole'),
           ('circ', (5, 5), 5, 'gc'), ('circ', (15, 5), 5, 'gc'), ('circ', (25, 5), 5, 'gc'), ('poly', [(0, 0), (30, 0), (30, 10), (0, 10)], 'd'), ('lab', (15, 0), '30 cm', 'below'), ('lab', (30, 5), '10 cm', 'right')], 0.14)
CABRA = tz([('sect', (0, 0), 5, 90, 360, 'sh'), ('sect', (4, 0), 1, 0, 90, 'sh'), ('sect', (0, 4), 1, 0, 90, 'sh'), ('poly', [(0, 0), (4, 0), (4, 4), (0, 4)], 'gf'),
            ('dot', (0, 0)), ('seg', (0, 0), (-3.54, -3.54), 'd'), ('lab', (-1.8, -1.8), '5 m', 'above left'), ('lab', (2, 2), 'corral'), ('lab', (2, 4), '4 m', 'below')], 0.24)
S_.append(("Figuras compuestas y problemas", [
 (1, r"Calcula el área y el perímetro de la fachada de la caseta.\par\smallskip\begin{center}" + CASA + r'\end{center}'
     + recorda(r"Para una figura compuesta, descomponla en figuras conocidas y suma las áreas, o mírala como una figura grande a la que le quitas trozos y resta. El perímetro es solo el contorno exterior."),
     r"$A=6\cdot6+\frac{6\cdot4}{2}=36+12=\res{48\text{ m}^2}$. \ Lados del tejado: $\sqrt{3^2+4^2}=5$; \ $P=6+6+6+5+5=\res{28\text{ m}}$."),
 (1, r"A un cuadrado de 8 cm de lado le añadimos un semicírculo sobre uno de los lados. Calcula el área y el perímetro de la figura.\par\smallskip\begin{center}" + SEMI + r'\end{center}',
     r"$A=64+\frac{\pi\cdot4^2}{2}=64+8\pi\approx\res{89{,}13\text{ cm}^2}$; \ $P=3\cdot8+\frac{2\pi\cdot4}{2}=24+4\pi\approx\res{36{,}57\text{ cm}}$."),
 (2, r"De un rectángulo de 10 cm × 6 cm recortamos dos semicírculos de 6 cm de diámetro en los lados cortos. Calcula el área y el perímetro de la figura que queda.\par\smallskip\begin{center}" + RSC + r'\end{center}',
     r"Los dos semicírculos forman un círculo de radio 3: \ $A=60-9\pi\approx\res{31{,}73\text{ cm}^2}$; \ $P=2\cdot10+2\pi\cdot3=20+6\pi\approx\res{38{,}85\text{ cm}}$."),
 (2, r"Calcula el área de la zona sombreada: un cuadrado de 12 cm de lado menos un cuarto de círculo de radio 12 cm.\par\smallskip\begin{center}" + QC + r'\end{center}',
     r"$A=144-\frac{\pi\cdot144}{4}=144-36\pi\approx\res{30{,}90\text{ cm}^2}$."),
 (2, r"Una ventana tiene forma de rectángulo de 1,4 m de anchura y 1,8 m de altura terminado en un semicírculo. Calcula la superficie de cristal y la longitud del marco exterior.\par\smallskip\begin{center}" + FIN + r'\end{center}',
     r"$A=1{,}4\cdot1{,}8+\frac{\pi\cdot0{,}7^2}{2}=2{,}52+0{,}245\pi\approx\res{3{,}29\text{ m}^2}$; \ $P=1{,}4+2\cdot1{,}8+0{,}7\pi\approx\res{7{,}20\text{ m}}$."),
 (2, r"Alrededor de una piscina de 25 m × 12 m se hace una acera de 2 m de anchura. Calcula la superficie de la acera.",
     r"Rectángulo exterior: $(25+4)\times(12+4)=29\cdot16=464$; \ $A=464-300=\res{164\text{ m}^2}$."),
 (3, r"Calcula el área de la «hoja» sombreada. Los arcos son cuartos de circunferencia con centro en dos vértices opuestos del cuadrado de 10 cm de lado.\par\smallskip\begin{center}" + LEAF + r'\end{center}',
     r"Media hoja = cuarto de círculo $-$ medio cuadrado $=25\pi-50$. \ $A=2(25\pi-50)=50\pi-100\approx\res{57{,}08\text{ cm}^2}$."),
 (3, r"Tres círculos iguales caben justo dentro de un rectángulo de 30 cm × 10 cm. Calcula el área de la zona sombreada.\par\smallskip\begin{center}" + CIR3 + r'\end{center}',
     r"Radio 5: \ $A=300-3\cdot25\pi=300-75\pi\approx\res{64{,}38\text{ cm}^2}$."),
 (3, r"Calcula el área comprendida entre un hexágono regular de 4 cm de lado y la circunferencia que pasa por sus vértices.",
     r"$r=4$, \ $a=\sqrt{16-4}=\sqrt{12}$; \ hexágono: $\frac{24\sqrt{12}}{2}=12\sqrt{12}\approx41{,}57$; \ $A=16\pi-12\sqrt{12}\approx50{,}27-41{,}57=\res{8{,}70\text{ cm}^2}$."),
 (3, r"Una cabra está atada con una cuerda de 5 m a una esquina exterior de un corral cuadrado de 4 m de lado, y no puede entrar en el corral. ¿Qué superficie puede pastar?\par\smallskip\begin{center}" + CABRA + r'\end{center}',
     r"Tres cuartos de círculo de radio 5 y, al doblar las esquinas, dos cuartos de círculo de radio $5-4=1$: \ $A=\frac34\cdot25\pi+2\cdot\frac{\pi}{4}=19{,}25\pi\approx\res{60{,}48\text{ m}^2}$."),
]))
ck(12 * S(12), 41.57, 2); ck(16 * pi, 50.27, 2)

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = "pdfkeywords={teorema de Pitàgores, hipotenusa, catets, perímetre, àrea, polígons regulars, apotema, circumferència, cercle, sector circular, corona circular}"
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TITOL = 'Perímetres i àrees. Teorema de Pitàgores'

pre = pre_

def build(sol_):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, ASSIGNATURA
    t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 9: Perímetros y áreas. Teorema de Pitágoras' % t, capcalera='%s · Unidad 9: Perímetros y áreas. Teorema de Pitágoras' % t,
                 pdfkeywords='teorema de Pitágoras, hipotenusa, catetos, perímetro, área, polígonos regulares, apotema, circunferencia, círculo, sector circular, corona circular')
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

''' + ASSIGNATURA + '{' + ('Soluciones de la ficha · Unidad 9' if sol_ else 'Ficha de ejercicios · Unidad 9') + '}{Perímetros y áreas. Teorema de Pitágoras}\n')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás una calculadora de Pitágoras y herramientas que calculan áreas y perímetros paso a paso. Los resultados aproximados están redondeados a las centésimas con la tecla $\pi$ de la calculadora."
             if sol_ else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y haz un dibujo de cada situación. Si un resultado no es exacto, redondéalo a las centésimas; para $\pi$, usa la tecla de la calculadora.") + r'''
\end{tcolorbox}
''')
    num, k = {}, 0
    for i, (_, exs) in enumerate(S_, 1):
        for j in range(1, len(exs) + 1):
            k += 1; num['@S%dE%d@' % (i, j)] = str(k)
    ref = lambda t: re.sub(r'@S\d+E\d+@', lambda m: num[m.group(0)], t)
    n = 0
    refs = globals().get('REFS', {})
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st, q, s) in enumerate(exs):
            n += 1
            lab = ''.join(r'\label{%s}' % kk for kk, (tt, jj) in refs.items() if tt == title and jj == j)
            out.append('\\ex{%d}%s %s\n\n' % (st, lab, ref(s if sol_ else q)))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't9-fitxa-solucions-es.tex' if sol_ else 't9-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
