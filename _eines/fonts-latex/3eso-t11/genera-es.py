# Versió en castellà de genera.py. Genera t11-fitxa-exercicis.tex i t11-fitxa-solucions.tex (3r ESO, Unitat 11: Cossos geomètrics)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Cada resultat numèric es comprova amb ck(valor exacte, valor escrit, decimals de l'arrodoniment).
# Els cossos es dibuixen amb ../../apunts/3eso-t11/solids.py i fig11.py (la mateixa perspectiva que als apunts).
import os, re, sys, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '3eso-t11'))
from solids import cylinder, cone, sphere, capsule, polyhedron, frustum, shift, PH
from fig11 import f_cuboid, f_pyramid, f_cylinder, f_cone, f_sphere

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- comprovacions ----------
pi, S, R = sp.pi, sp.sqrt, sp.Rational
def Q(v): return sp.nsimplify(v, rational=True) if isinstance(v, float) else sp.nsimplify(v)
def ck(v, w, d=None):
    """v: valor exacte; w: el que escrivim (nombre o text amb coma); d: decimals de l'arrodoniment (None = exacte)"""
    w = float(w.replace(',', '.').replace(' ', '')) if isinstance(w, str) else w
    if d is None: assert sp.simplify(Q(v) - Q(w)) == 0, (v, w)
    else: assert abs(float(v) - float(w)) <= 0.5 * 10 ** -d + 1e-9, (v, float(v), w, d)
def euler(C, V, A): return C + V == A + 2
x = sp.Symbol('x')

# ---------- figures (TikZ) ----------
ST = {'fr': 'fill=teal!14,draw=none', 'nf': 'fill=teal!14,draw=black', 'top': 'fill=teal!26,draw=black,thick', 'bs': 'fill=accent!18,draw=black',
      'ed': 'thick', 'hid': 'dashed,draw=muted', 'ax': 'dashed,draw=accent,thick', 'ax2': 'draw=navy,thick', '': 'thick'}
def P_(p): return '(%.3f,%.3f)' % (float(p[0]), float(p[1]))
def labtex(t):
    t = re.sub(r'(\w)<tspan[^>]*>(\w+)</tspan>', r'$\1_{\2}$', t)
    if re.fullmatch(r"[A-Za-z]", t): return '$%s$' % t
    m = re.fullmatch(r"([\d,]+)( ?m| ?cm)?", t)
    if m: return '$%s$%s' % (m.group(1).replace(',', '{,}'), ('\\,' + m.group(2).strip()) if m.group(2) else '')
    return t
def tz(items, s=0.5):
    """dibuixa en TikZ una llista d'elements en el format de G() dels apunts"""
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center),line join=round]' % (s, s)]
    for it in items:
        k = it[0]
        if k == 'poly': o.append(r'\path[%s] %s -- cycle;' % (ST[it[2]], ' -- '.join(P_(p) for p in it[1])) if ST[it[2]].endswith('none') else r'\draw[%s] %s -- cycle;' % (ST[it[2]], ' -- '.join(P_(p) for p in it[1])))
        elif k == 'pl': o.append(r'\draw[%s] %s;' % (ST[it[2]], ' -- '.join(P_(p) for p in it[1])))
        elif k == 'seg': o.append(r'\draw[%s] %s -- %s;' % (ST[it[3] if len(it) > 3 else ''], P_(it[1]), P_(it[2])))
        elif k == 'circ': o.append(r'\draw[%s] %s circle[radius=%s];' % (ST[it[3]].replace('draw=none', 'draw=black,thick'), P_(it[1]), it[2]))
        elif k == 'sect':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]; A0 = (C[0] + r * math.cos(math.radians(a0)), C[1] + r * math.sin(math.radians(a0)))
            o.append(r'\draw[%s] %s -- %s arc[start angle=%s,end angle=%s,radius=%s] -- cycle;' % (ST[it[5]], P_(C), P_(A0), a0, a1, r))
        elif k == 'dot': o.append(r'\fill %s circle (1.3pt);' % P_(it[1]))
        elif k == 'txt':
            op = it[3] if len(it) > 3 else {}
            if not it[2]: continue
            dx, dy, a = op.get('dx', 0), op.get('dy', 4), op.get('a', 'middle')
            anc = []
            if dy >= 12: anc.append('below')
            elif dy <= -4: anc.append('above')
            if a == 'end' or dx < -3: anc.append('left')
            elif a == 'start' or dx > 3: anc.append('right')
            col = {'ax': ',text=accent', 'ax2': ',text=navy', 'hot': ',text=accent'}.get(op.get('cls', ''), '')
            o.append(r'\node[font=\small,inner sep=2pt%s%s] at %s {%s};' % ((',' + ' '.join(anc)) if anc else '', col, P_(it[1]), labtex(it[2])))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def fig(*f): return r'\par\smallskip\begin{center}' + r'\qquad '.join(f) + r'\end{center}'
def side(t, f, w='0.3'):
    """enunciat a l'esquerra (a continuació del número) i figura a la dreta"""
    return (r'\begin{minipage}[t]{%.2f\linewidth}%s\end{minipage}\hfill\begin{minipage}[t]{%s\linewidth}\vspace{0pt}\centering %s\end{minipage}\par'
            % (0.86 - float(w), t, w, f))
HC = math.cos(math.radians(PH))

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Poliedres. Fórmula d'Euler. Poliedres regulars
# =====================================================================
TAU = [("prisma triangular", 5, 6, 9), ("pirámide pentagonal", 6, 6, 10), ("prisma hexagonal", 8, 12, 18), ("pirámide octogonal", 9, 9, 16), ("cubo", 6, 8, 12)]
for _, C, V, A in TAU: assert euler(C, V, A)
assert 18 == 8 + 12 - 2 and 7 == 15 + 2 - 10 and 20 == 30 + 2 - 12
assert euler(10, 16, 24) and euler(11, 11, 20) and euler(7, 7, 12) and not euler(5, 6, 10) and euler(8, 6, 12) and euler(10, 7, 15)
S_.append(("Poliedros. Fórmula de Euler. Poliedros regulares", [
 (1, r"Copia y completa la tabla. Comprueba en cada caso la fórmula de Euler.\par\smallskip\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|l|C{1.6cm}|C{1.6cm}|C{1.6cm}|}\hline Poliedro & Caras & Vértices & Aristas \\\hline "
     + r" \\\hline ".join(n + r" & & & " for n, *_ in TAU) + r" \\\hline\end{tabular}\end{center}"
     + recorda(r"En un poliedro convexo, \textbf{caras} + \textbf{vértices} = \textbf{aristas} + 2: \ $C+V=A+2$ (fórmula de Euler). Un prisma de base de $n$ lados tiene $n+2$ caras, $2n$ vértices y $3n$ aristas; una pirámide, $n+1$ caras, $n+1$ vértices y $2n$ aristas."),
     r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|l|C{1.6cm}|C{1.6cm}|C{1.6cm}|l|}\hline Poliedro & $C$ & $V$ & $A$ & $C+V=A+2$ \\\hline "
     + r" \\\hline ".join(r"%s & %d & %d & %d & $%d=%d$" % (n, C, V, A, C + V, A + 2) for n, C, V, A in TAU) + r" \\\hline\end{tabular}\end{center}"),
 (1, r"Usa la fórmula de Euler para calcular lo que falta en cada poliedro convexo:" + tasks(3, [r"$C=8$, \ $V=12$, \ $A=\ ?$", r"$V=10$, \ $A=15$, \ $C=\ ?$", r"$C=12$, \ $A=30$, \ $V=\ ?$"]),
     tasks(3, [r"$8+12=A+2\Rightarrow\res{A=18}$", r"$C+10=17\Rightarrow\res{C=7}$", r"$12+V=32\Rightarrow\res{V=20}$"])),
 (1, r"¿Cuáles de estos poliedros son regulares? Justifícalo." + tasks(3, [r"tetraedro", r"ortoedro", r"octaedro", r"pirámide cuadrangular regular", r"icosaedro", r"cubo"]),
     tasks(3, [r"\rest{sí}", r"no (rectángulos diferentes)", r"\rest{sí}", r"no (caras de dos tipos)", r"\rest{sí}", r"\rest{sí}"]) + r"Un poliedro regular tiene todas las caras polígonos regulares iguales y el mismo número de caras en cada vértice."),
 (2, r"Un prisma tiene 24 aristas. ¿Qué polígono tiene por base? ¿Cuántas caras y cuántos vértices tiene?",
     r"$3n=24\Rightarrow n=8$: base \rest{octogonal}; \ $\res{C=10}$, \ $\res{V=16}$ \ ($10+16=24+2$)."),
 (2, r"Una pirámide tiene 11 vértices. ¿Qué polígono tiene por base? ¿Cuántas caras y aristas tiene?",
     r"$n+1=11\Rightarrow n=10$: base \rest{decagonal}; \ $\res{C=11}$, \ $\res{A=20}$ \ ($11+11=20+2$)."),
 (2, r"¿Puede existir un poliedro convexo con: \ a) 7 caras, 7 vértices y 12 aristas? \ b) 5 caras, 6 vértices y 10 aristas?",
     r"a) $7+7=14=12+2$: \rest{sí} (por ejemplo, una pirámide hexagonal). \ b) $5+6=11\neq12$: \rest{no}."),
 (3, r"Si juntamos dos pirámides cuadrangulares iguales por la base obtenemos una \emph{bipirámide}. ¿Cuántas caras, vértices y aristas tiene? ¿Y si las pirámides son pentagonales?",
     r"Cuadrangulares: $\res{C=8,\ V=6,\ A=12}$ (es un octaedro si las caras son equiláteras). \ Pentagonales: $\res{C=10,\ V=7,\ A=15}$. \ En los dos casos $C+V=A+2$."),
 (3, r"Explica por qué no puede haber ningún poliedro regular con caras hexagonales.",
     r"Cada ángulo de un hexágono regular mide $120^\circ$. En un vértice se tienen que juntar como mínimo 3 caras, y $3\cdot120^\circ=360^\circ$: las caras quedarían \rest{planas} y no cerrarían ningún cuerpo."),
]))

# =====================================================================
# 2. Prismes: elements i àrea
# =====================================================================
ck(6 * 16, 96); ck(2 * (24 + 18 + 12), 108); ck(S(144 + 16 + 9), 13); ck(20 * 12, 240); ck(240 + 50, 290)
ck(12 * 10, 120); ck(2 * S(12), 6.93, 2); ck(120 + 4 * S(12), 133.86, 2)
ck(36 * 8, 288); ck(S(27), 5.20, 2); ck(18 * S(27), 93.53, 2); ck(288 + 36 * S(27), 475.06, 2)
ck(1200 + 1600 + 1200, 4000); ck(S(R(48, 3)), 4); ck(S(36 + 64), 10); ck(24 * 15, 360); ck(360 + 48, 408)
ORT = tz(f_cuboid(6, 3, 4, la='6 cm', lb='3 cm', lc='4 cm')[0], 0.45)
S_.append(("Prismas: elementos y área", [
 (1, side(r"Calcula el área total:" + tasks(1, [r"de un cubo de 4 cm de arista;", r"del ortoedro de la figura."]), ORT, '0.34')
     + recorda(r"Área de un prisma recto: $A_L=P_{\text{base}}\cdot h$, \ $A_T=A_L+2\,A_{\text{base}}$. Ortoedro de aristas $a,\,b,\,c$: $A_T=2(ab+ac+bc)$ y la diagonal es $D=\sqrt{a^2+b^2+c^2}$."),
     tasks(2, [r"$6\cdot4^2=\res{96\text{ cm}^2}$", r"$2(6\cdot3+6\cdot4+3\cdot4)=2\cdot54=\res{108\text{ cm}^2}$"])),
 (1, r"Calcula la diagonal de un ortoedro de 12 cm × 4 cm × 3 cm.",
     r"$D=\sqrt{144+16+9}=\sqrt{169}=\res{13\text{ cm}}$."),
 (1, r"Un prisma cuadrangular regular tiene 5 cm de arista de la base y 12 cm de altura. Calcula su área lateral y su área total.",
     r"$A_L=20\cdot12=\res{240\text{ cm}^2}$; \ $A_T=240+2\cdot25=\res{290\text{ cm}^2}$."),
 (2, r"Calcula el área total de un prisma triangular regular de 4 cm de arista de la base y 10 cm de altura.",
     r"$A_L=12\cdot10=120$; altura de la base $\sqrt{16-4}=\sqrt{12}\approx3{,}46$; $A_{\text{base}}=\frac{4\cdot\sqrt{12}}{2}\approx6{,}93$. \ $A_T\approx120+2\cdot6{,}93=\res{133{,}86\text{ cm}^2}$."),
 (2, r"Calcula el área total de un prisma hexagonal regular de 6 cm de arista de la base y 8 cm de altura.",
     r"$A_L=36\cdot8=288$; \ $a_b=\sqrt{36-9}=\sqrt{27}\approx5{,}20$; \ $A_{\text{base}}=\frac{36\cdot\sqrt{27}}{2}\approx93{,}53$. \ $A_T\approx288+187{,}06=\res{475{,}06\text{ cm}^2}$."),
 (2, r"Queremos hacer una caja sin tapa de 40 cm × 30 cm de base y 20 cm de altura. ¿Cuánto cartón necesitamos?",
     r"Base $40\cdot30=1200$; \ caras $2\cdot40\cdot20+2\cdot30\cdot20=2800$. \ Total: $\res{4000\text{ cm}^2}$."),
 (3, r"La diagonal de un cubo mide $\sqrt{48}$ cm. ¿Cuánto mide la arista? Calcula su área total.",
     r"$D^2=3l^2\Rightarrow3l^2=48\Rightarrow\res{l=4\text{ cm}}$; \ $A_T=6\cdot16=\res{96\text{ cm}^2}$."),
 (3, r"La base de un prisma recto es un triángulo rectángulo de catetos 6 cm y 8 cm, y la altura del prisma es 15 cm. Calcula su área total.",
     r"Hipotenusa: $\sqrt{36+64}=10$. \ $A_L=(6+8+10)\cdot15=360$; \ $A_{\text{base}}=\frac{6\cdot8}{2}=24$. \ $A_T=360+48=\res{408\text{ cm}^2}$."),
]))

# =====================================================================
# 3. Piràmides i troncs de piràmide
# =====================================================================
ck(S(144 + 25), 13); ck(40 * 13 / 2 + 100, 360); ck(24 * 9 / 2, 108); ck(S(25 - 9), 4); ck(24 * 5 / 2 + 36, 96)
ck(S(52), 7.21, 2); ck(S(68), 8.25, 2); ck(16 * S(52), 115.38, 2); ck(16 * S(52) + 64, 179.38, 2)
ck(4 * 6 * S(27) / 2, 62.35, 2); ck(S(16 + 9), 5); ck((48 + 24) * 5 / 2, 180); ck(180 + 144 + 36, 360)
apk = S(146 ** 2 + 115 ** 2); ck(apk, 185.85, 2); ck(920 * apk / 2, 85492, 0)
PYF = tz(f_pyramid(4, 3, 3.6, labs=('10 cm', '12 cm', '', ''))[0], 0.5)
S_.append(("Pirámides y troncos de pirámide", [
 (1, side(r"La pirámide cuadrangular regular de la figura tiene 10 cm de arista de la base y 12 cm de altura. Calcula su apotema y su área total.", PYF, '0.3')
     + recorda(r"En una pirámide regular, la altura $h$, la apotema de la base $a_b$ y la apotema de la pirámide $a_p$ forman un triángulo rectángulo: $a_p^2=h^2+a_b^2$. \ $A_L=\frac{P_{\text{base}}\cdot a_p}{2}$, \ $A_T=A_L+A_{\text{base}}$."),
     r"$a_b=5$; \ $a_p=\sqrt{144+25}=\res{13\text{ cm}}$. \ $A_T=\frac{40\cdot13}{2}+100=\res{360\text{ cm}^2}$."),
 (1, r"Una pirámide hexagonal regular tiene 4 cm de arista de la base y 9 cm de apotema. Calcula su área lateral.",
     r"$A_L=\frac{24\cdot9}{2}=\res{108\text{ cm}^2}$."),
 (2, r"Una pirámide cuadrangular regular tiene 6 cm de arista de la base y 5 cm de apotema. ¿Qué altura tiene? Calcula su área total.",
     r"$h=\sqrt{5^2-3^2}=\res{4\text{ cm}}$; \ $A_T=\frac{24\cdot5}{2}+36=\res{96\text{ cm}^2}$."),
 (2, r"Una pirámide cuadrangular regular tiene 8 cm de arista de la base y 6 cm de altura. Calcula la apotema, la arista lateral y el área total.",
     r"$a_p=\sqrt{36+16}=\sqrt{52}\approx\res{7{,}21\text{ cm}}$; \ arista: $\sqrt{a_p^2+4^2}=\sqrt{68}\approx\res{8{,}25\text{ cm}}$; \ $A_T=\frac{32\cdot\sqrt{52}}{2}+64\approx\res{179{,}38\text{ cm}^2}$."),
 (2, r"Calcula el área total de un tetraedro regular de 6 cm de arista.",
     r"Cada cara es un triángulo equilátero de altura $\sqrt{36-9}=\sqrt{27}\approx5{,}20$: \ $A=4\cdot\frac{6\cdot\sqrt{27}}{2}\approx\res{62{,}35\text{ cm}^2}$."),
 (3, r"Un tronco de pirámide cuadrangular regular tiene las aristas de las bases de 12 cm y 6 cm y una altura de 4 cm. Calcula la apotema del tronco y el área total.",
     r"$a_p=\sqrt{4^2+3^2}=\res{5\text{ cm}}$ \ (catetos: la altura y $\frac{12-6}{2}=3$). \ $A_T=\frac{(48+24)\cdot5}{2}+144+36=\res{360\text{ cm}^2}$."),
 (3, r"La gran pirámide de Keops (Guiza) tiene una base cuadrada de 230 m de lado y mide 146 m de altura. Calcula la apotema y el área de las cuatro caras laterales.",
     r"$a_p=\sqrt{146^2+115^2}=\sqrt{34\,541}\approx\res{185{,}85\text{ m}}$; \ $A_L=\frac{920\cdot185{,}85}{2}\approx\res{85\,492\text{ m}^2}$."),
]))

# =====================================================================
# 4. Cilindre i con
# =====================================================================
ck(60 * pi, 188.50, 2); ck(78 * pi, 245.04, 2); ck(S(25 + 144), 13); ck(65 * pi, 204.20, 2); ck(90 * pi, 282.74, 2)
ck(S(100 - 36), 8); ck(96 * pi, 301.59, 2); ck(96 * pi + 32 * pi, 128 * pi); ck(128 * pi, 402.12, 2)
ck(S(81 + 144), 15); ck(135 * pi, 424.12, 2); ck(R(120, 20), 6); ck(192 * pi, 603.19, 2); ck(360 * R(4, 12), 120)
ck(48 * pi, 150.80, 2); ck(48 * pi * R(1, 4), 37.70, 2)
CYF = tz(f_cylinder(1.5, 3.2, lr='3 cm', lh='10 cm')[0], 0.5)
CNF = tz(f_cone(1.6, 3.4, lr='5 cm', lh='12 cm', lg='g')[0], 0.5)
S_.append(("Cilindro y cono", [
 (1, side(r"Calcula el área lateral y el área total del cilindro de la figura.", CYF, '0.25')
     + recorda(r"Cilindro: $A_L=2\pi rh$, \ $A_T=2\pi rh+2\pi r^2$. \ Cono: $g^2=h^2+r^2$, \ $A_L=\pi rg$, \ $A_T=\pi rg+\pi r^2$. Usa la tecla $\pi$ y redondea a las centésimas."),
     r"$A_L=2\pi\cdot3\cdot10=60\pi\approx\res{188{,}50\text{ cm}^2}$; \ $A_T=60\pi+18\pi=78\pi\approx\res{245{,}04\text{ cm}^2}$."),
 (1, side(r"Calcula la generatriz, el área lateral y el área total del cono de la figura.", CNF, '0.25'),
     r"$g=\sqrt{144+25}=\res{13\text{ cm}}$; \ $A_L=\pi\cdot5\cdot13=65\pi\approx\res{204{,}20\text{ cm}^2}$; \ $A_T=65\pi+25\pi=90\pi\approx\res{282{,}74\text{ cm}^2}$."),
 (1, r"Un cono tiene 6 cm de radio y 10 cm de generatriz. ¿Qué altura tiene? Calcula su área total.",
     r"$h=\sqrt{100-36}=\res{8\text{ cm}}$; \ $A_T=60\pi+36\pi=96\pi\approx\res{301{,}59\text{ cm}^2}$."),
 (2, r"Una lata de refresco tiene 8 cm de diámetro y 12 cm de altura. ¿Cuánta chapa hace falta para fabricarla?",
     r"$r=4$: \ $A_T=2\pi\cdot4\cdot12+2\pi\cdot16=96\pi+32\pi=128\pi\approx\res{402{,}12\text{ cm}^2}$."),
 (2, r"Queremos hacer un gorro de payaso en forma de cono de 9 cm de radio y 12 cm de altura. ¿Cuánto papel necesitamos?",
     r"$g=\sqrt{81+144}=15$; \ solo la superficie lateral: $A_L=\pi\cdot9\cdot15=135\pi\approx\res{424{,}12\text{ cm}^2}$."),
 (2, r"Un cilindro tiene un área lateral de $120\pi$ cm² y 10 cm de altura. ¿Qué radio tiene? Calcula su área total.",
     r"$2\pi r\cdot10=120\pi\Rightarrow\res{r=6\text{ cm}}$; \ $A_T=120\pi+72\pi=192\pi\approx\res{603{,}19\text{ cm}^2}$."),
 (3, r"Un cono tiene 4 cm de radio y 12 cm de generatriz. ¿Qué ángulo tiene el sector circular de su desarrollo?",
     r"El arco del sector mide $2\pi\cdot4=8\pi$ y la circunferencia entera de radio 12 mediría $24\pi$: es $\frac{8\pi}{24\pi}=\frac13$ del círculo. \ Ángulo: $\frac{360^\circ}{3}=\res{120^\circ}$."),
 (3, r"Hay que pintar la superficie lateral de 12 columnas cilíndricas de 0,4 m de radio y 5 m de altura. Si un litro de pintura cubre 4 m², ¿cuántos litros hacen falta?",
     r"$A=12\cdot2\pi\cdot0{,}4\cdot5=48\pi\approx150{,}80\text{ m}^2$; \ $\frac{150{,}80}{4}\approx\res{37{,}70\text{ L}}$."),
]))

# =====================================================================
# 5. L'esfera. La Terra
# =====================================================================
ck(64 * pi, 201.06, 2); ck(100 * pi, 314.16, 2); ck(pi, 3.14, 2); ck(S(R(144, 4)), 6); ck(50 * pi, 157.08, 2)
ck(R(40000 * 50, 360), 5555.56, 2); ck(R(6371, 1737) ** 2, 13.45, 2)
SPF = tz(f_sphere(1.6, lr='r')[0], 0.5)
S_.append(("La esfera. La Tierra", [
 (1, side(r"Calcula el área de:" + tasks(1, [r"una esfera de 4 cm de radio;", r"una pelota de 10 cm de diámetro;", r"una bola de 0,5 m de radio."]), SPF, '0.22')
     + recorda(r"Área de la esfera: $A=4\pi r^2$ (cuatro círculos máximos). \ La \textbf{latitud} va de $0^\circ$ a $90^\circ$ N o S (desde el ecuador) y la \textbf{longitud}, de $0^\circ$ a $180^\circ$ E u O (desde el meridiano de Greenwich)."),
     tasks(3, [r"$64\pi\approx\res{201{,}06\text{ cm}^2}$", r"$100\pi\approx\res{314{,}16\text{ cm}^2}$", r"$\pi\approx\res{3{,}14\text{ m}^2}$"])),
 (2, r"Una esfera tiene un área de $144\pi$ cm². ¿Qué radio tiene?",
     r"$4\pi r^2=144\pi\Rightarrow r^2=36\Rightarrow\res{r=6\text{ cm}}$."),
 (2, r"Una cúpula tiene forma de semiesfera de 5 m de radio. ¿Qué superficie hay que impermeabilizar por fuera?",
     r"Media esfera: $\frac{4\pi\cdot25}{2}=50\pi\approx\res{157{,}08\text{ m}^2}$."),
 (2, r"Dos ciudades están sobre el mismo meridiano, una a $40^\circ$ N y la otra a $10^\circ$ S. ¿Cuántos grados de latitud las separan? Si un meridiano entero (la vuelta a la Tierra) mide 40\,000 km, ¿qué distancia hay entre ellas sobre el meridiano?",
     r"$40^\circ+10^\circ=\res{50^\circ}$; \ $\frac{40\,000\cdot50}{360}\approx\res{5555{,}56\text{ km}}$."),
 (2, r"Cuando en Greenwich son las 12 horas solares, ¿qué hora solar es en un lugar de longitud $45^\circ$ E? ¿Y en uno de longitud $30^\circ$ O?",
     r"Cada $15^\circ$ es una hora: \ $45^\circ$ E $\to$ 3 horas más: \res{15 h}; \ $30^\circ$ O $\to$ 2 horas menos: \res{10 h}."),
 (3, r"El radio de la Tierra es 6371 km y el de la Luna, 1737 km. ¿Cuántas veces mayor es la superficie de la Tierra que la de la Luna?",
     r"$\frac{4\pi\cdot6371^2}{4\pi\cdot1737^2}=\left(\frac{6371}{1737}\right)^2\approx\res{13{,}45}$ veces."),
]))

# =====================================================================
# 6. Volum. Prismes i cilindres
# =====================================================================
for v, w in [(R(32, 10) * 1000, 3200), (R(450, 1000), 0.45), (R(25, 10) * 1000, 2500), (R(75, 100) * 1000, 750), (R(12000, 1000), 12), (R(5, 10), 0.5)]: ck(v, w)
ck(216, 216); ck(8 * 5 * 3, 120); ck(160 * pi, 502.65, 2); ck(R(5 * 12, 2) * 20, 600)
ck(6 * S(3), 10.39, 2); ck(30 * S(3), 51.96, 2); ck(R(60 * 30 * 40, 1000), 72); ck(72 * R(3, 4), 54)
ck(9 * pi, 28.27, 2); ck(9000 * pi, 28274, 0); ck(R(1 + 3, 2) * 25 * 10, 500); ck(500 / (16 * pi), 9.95, 2)
ck(24 * R(115, 10) * 5, 1380); ck(1380 - R(3375, 100) * pi, 1273.97, 2)
S_.append(("Volumen. Prismas y cilindros", [
 (1, r"Expresa en la unidad indicada:" + tasks(3, [r"3,2 m³ en L", r"450 cm³ en L", r"2,5 L en cm³", r"0,75 dm³ en mL", r"12\,000 L en m³", r"5 hL en m³"])
     + recorda(r"Cada unidad de volumen es 1000 veces la siguiente: $1\text{ m}^3=1000\text{ dm}^3$, \ $1\text{ dm}^3=1000\text{ cm}^3$. \ $1\text{ dm}^3=1\text{ L}$, \ $1\text{ cm}^3=1\text{ mL}$. \ Prisma y cilindro: $V=A_{\text{base}}\cdot h$; \ $V_{\text{cilindro}}=\pi r^2h$."),
     tasks(3, [r"$\res{3200\text{ L}}$", r"$\res{0{,}45\text{ L}}$", r"$\res{2500\text{ cm}^3}$", r"$\res{750\text{ mL}}$", r"$\res{12\text{ m}^3}$", r"$\res{0{,}5\text{ m}^3}$"])),
 (1, r"Calcula el volumen de:" + tasks(1, [r"un cubo de 6 cm de arista;", r"un ortoedro de 8 cm × 5 cm × 3 cm;", r"un cilindro de 4 cm de radio y 10 cm de altura."]),
     tasks(3, [r"$6^3=\res{216\text{ cm}^3}$", r"$\res{120\text{ cm}^3}$", r"$160\pi\approx\res{502{,}65\text{ cm}^3}$"])),
 (1, r"La base de un prisma es un triángulo rectángulo de catetos 5 cm y 12 cm. Si el prisma mide 20 cm de altura, ¿qué volumen tiene?",
     r"$V=\frac{5\cdot12}{2}\cdot20=\res{600\text{ cm}^3}$."),
 (2, r"Calcula el volumen de un prisma hexagonal regular de 2 cm de arista de la base y 5 cm de altura.",
     r"$a_b=\sqrt{4-1}=\sqrt3$; \ $A_{\text{base}}=\frac{12\cdot\sqrt3}{2}=6\sqrt3\approx10{,}39$; \ $V\approx\res{51{,}96\text{ cm}^3}$."),
 (2, r"Un acuario mide 60 cm × 30 cm de base y 40 cm de altura. ¿Cuántos litros caben? ¿Cuántos litros hay si el agua llega a $\frac34$ de la altura?",
     r"$V=72\,000\text{ cm}^3=\res{72\text{ L}}$; \ $\frac34\cdot72=\res{54\text{ L}}$."),
 (2, r"Un depósito cilíndrico tiene 1,5 m de radio y 4 m de altura. ¿Cuántos litros de agua caben?",
     r"$V=\pi\cdot1{,}5^2\cdot4=9\pi\approx28{,}27\text{ m}^3\approx\res{28\,274\text{ L}}$."),
 (2, r"Una piscina mide 25 m de largo y 10 m de ancho. El fondo es inclinado: la profundidad va de 1 m a 3 m. ¿Qué volumen de agua cabe? (Es un prisma con una base en forma de trapecio.)",
     r"Base (el lateral de la piscina): $\frac{(1+3)\cdot25}{2}=50\text{ m}^2$; \ $V=50\cdot10=\res{500\text{ m}^3}$."),
 (3, r"Un vaso cilíndrico mide 4 cm de radio. Si echamos medio litro de agua, ¿hasta qué altura llega?",
     r"$\pi\cdot16\cdot h=500\Rightarrow h=\frac{500}{16\pi}\approx\res{9{,}95\text{ cm}}$."),
 (3, r"Un ladrillo mide 24 cm × 11,5 cm × 5 cm y tiene tres agujeros cilíndricos de 1,5 cm de radio que lo atraviesan (en la dirección de los 5 cm). ¿Qué volumen de arcilla tiene?",
     r"$V=24\cdot11{,}5\cdot5-3\cdot\pi\cdot1{,}5^2\cdot5=1380-33{,}75\pi\approx\res{1273{,}97\text{ cm}^3}$."),
]))

# =====================================================================
# 7. Volum de piràmides, cons i esferes
# =====================================================================
ck(R(36 * 10, 3), 120); ck(21 * pi, 65.97, 2); ck(288 * pi, 904.78, 2); ck(R(4000, 3) * pi, 4188.79, 2)
ck(S(169 - 25), 12); ck(R(100 * 12, 3), 400); ck(S(100 - 36), 8); ck(96 * pi, 301.59, 2); ck(R(4, 3) * pi * 1331, 5575.28, 2)
ck(36 * S(12), 124.71, 2); ck(1152 * pi, 3619.11, 2); assert sp.solve(R(1, 3) * 36 * x - R(4, 3) * 216, x) == [24]
S_.append(("Volumen de pirámides, conos y esferas", [
 (1, r"Calcula el volumen de:" + tasks(1, [r"una pirámide cuadrangular de 6 cm de arista de la base y 10 cm de altura;", r"un cono de 3 cm de radio y 7 cm de altura;", r"una esfera de 6 cm de radio."])
     + recorda(r"$V_{\text{pirámide}}=\frac{A_{\text{base}}\cdot h}{3}$; \ $V_{\text{cono}}=\frac{\pi r^2h}{3}$; \ $V_{\text{esfera}}=\frac43\pi r^3$."),
     tasks(3, [r"$\frac{36\cdot10}{3}=\res{120\text{ cm}^3}$", r"$21\pi\approx\res{65{,}97\text{ cm}^3}$", r"$288\pi\approx\res{904{,}78\text{ cm}^3}$"])),
 (1, r"¿Qué volumen tiene una bola de 20 cm de diámetro? Exprésalo en cm³ y en litros.",
     r"$r=10$: \ $V=\frac43\pi\cdot1000\approx\res{4188{,}79\text{ cm}^3}\approx\res{4{,}19\text{ L}}$."),
 (2, r"Una pirámide cuadrangular regular tiene 10 cm de arista de la base y 13 cm de apotema. Calcula su altura y su volumen.",
     r"$h=\sqrt{13^2-5^2}=\res{12\text{ cm}}$; \ $V=\frac{100\cdot12}{3}=\res{400\text{ cm}^3}$."),
 (2, r"Un cono tiene 6 cm de radio y 10 cm de generatriz. Calcula su volumen.",
     r"$h=\sqrt{100-36}=8$; \ $V=\frac{\pi\cdot36\cdot8}{3}=96\pi\approx\res{301{,}59\text{ cm}^3}$."),
 (2, r"¿Cuántos litros de aire hay dentro de una pelota de baloncesto de 11 cm de radio?",
     r"$V=\frac43\pi\cdot11^3\approx5575{,}28\text{ cm}^3\approx\res{5{,}58\text{ L}}$."),
 (2, r"Calcula el volumen de una pirámide hexagonal regular de 4 cm de arista de la base y 9 cm de altura.",
     r"$a_b=\sqrt{12}$; \ $A_{\text{base}}=\frac{24\cdot\sqrt{12}}{2}\approx41{,}57$; \ $V=\frac{A_{\text{base}}\cdot9}{3}\approx\res{124{,}71\text{ cm}^3}$."),
 (3, r"Un bol tiene forma de semiesfera de 12 cm de radio interior. ¿Cuántos litros caben?",
     r"$V=\frac12\cdot\frac43\pi\cdot12^3=1152\pi\approx3619{,}11\text{ cm}^3\approx\res{3{,}62\text{ L}}$."),
 (3, r"Una esfera y un cono tienen el mismo radio, 6 cm, y el mismo volumen. ¿Qué altura tiene el cono?",
     r"$\frac13\pi\cdot36\cdot h=\frac43\pi\cdot216\Rightarrow12h=288\Rightarrow\res{h=24\text{ cm}}$ \ (cuatro veces el radio)."),
]))

# =====================================================================
# 8. Cossos compostos i problemes
# =====================================================================
ck(216 + 48, 264); ck(90 * pi + 12 * pi, 102 * pi); ck(102 * pi, 320.44, 2)
ck(24 * pi + R(32, 3) * pi, R(104, 3) * pi); ck(R(104, 3) * pi, 108.91, 2); ck(40 * pi, 125.66, 2)
ck(R(625, 100) * 12 / 3 + R(2, 3) * R(15625, 1000), R(425, 12)); ck(R(425, 12) * pi, 111.26, 2)
ck(550 * pi, 1727.88, 2); ck(1000 - 90 * pi, 717.26, 2)
assert sp.solve(18 * x - 12 * (x + 24), x) == [48]; ck(R(324 * 72, 3) - R(144 * 48, 3), 5472); ck(5472 * pi, 17190.80, 2); ck(5472 * pi / 1000, 17.19, 2)
ck(R(4, 3) * 27 / 36, 1)
Vt = 20 * pi + R(16, 3) * pi; ck(Vt, R(76, 3) * pi); ck(Vt, 79.59, 2); ck(Vt * 1000 / 50, 1591.7, 1); ck(Vt * 1000 / 50 / 60, 26.5, 1)
SIT = cylinder(1.5, 3.4, top=False)[0] + shift(cone(1.5, 1.4)[0], 0, 3.4 * HC)
SIT += [('seg', (0, 0), (1.5, 0), 'ax'), ('txt', (0.75, 0), '3 m', {'dy': 22, 'cls': 'ax'}), ('txt', (1.5, 1.7 * HC), '10 m', {'dx': 8, 'a': 'start'}),
        ('seg', (0, 3.4 * HC), (0, 4.8 * HC), 'ax'), ('txt', (-0.8, 4.1 * HC), '4 m', {'dx': -6, 'a': 'end', 'cls': 'ax'})]
CAP = capsule(1, 3)[0] + [('txt', (1, 1.5 * HC), '6 cm', {'dx': 8, 'a': 'start'}), ('seg', (0, 0), (1, 0), 'ax'), ('txt', (0.5, -1), '2 cm', {'dy': 15, 'cls': 'ax'})]
S_.append(("Cuerpos compuestos y problemas", [
 (1, r"Una pieza está formada por un cubo de 6 cm de arista y, encima, una pirámide de la misma base y 4 cm de altura. Calcula su volumen."
     + recorda(r"Descompón el cuerpo en cuerpos simples. El volumen es la suma (o la diferencia, si hay agujeros) de los volúmenes. Para el área, suma solo las superficies que quedan por fuera."),
     r"$V=6^3+\frac{36\cdot4}{3}=216+48=\res{264\text{ cm}^3}$."),
 (2, side(r"Un silo tiene la forma de la figura: un cilindro de 3 m de radio y 10 m de altura con un tejado cónico de 4 m de altura. ¿Qué volumen tiene?", tz(SIT, 0.42), '0.25'),
     r"$V=\pi\cdot9\cdot10+\frac{\pi\cdot9\cdot4}{3}=90\pi+12\pi=102\pi\approx\res{320{,}44\text{ m}^3}$."),
 (2, side(r"Una cápsula es un cilindro de 2 cm de radio y 6 cm de largo con una semiesfera en cada extremo. Calcula su volumen y su área.", tz(CAP, 0.5), '0.2'),
     r"$V=\pi\cdot4\cdot6+\frac43\pi\cdot8=24\pi+\frac{32\pi}{3}=\frac{104\pi}{3}\approx\res{108{,}91\text{ cm}^3}$; \ $A=2\pi\cdot2\cdot6+4\pi\cdot4=40\pi\approx\res{125{,}66\text{ cm}^2}$."),
 (2, r"Un helado es un cucurucho cónico de 2,5 cm de radio y 12 cm de altura, lleno, con una semiesfera de helado encima. ¿Qué volumen de helado hay?",
     r"$V=\frac{\pi\cdot2{,}5^2\cdot12}{3}+\frac12\cdot\frac43\pi\cdot2{,}5^3=25\pi+\frac{125\pi}{12}=\frac{425\pi}{12}\approx\res{111{,}26\text{ cm}^3}$."),
 (2, r"Un tubo de 50 cm de largo tiene 6 cm de radio exterior y 5 cm de radio interior. ¿Qué volumen de material tiene?",
     r"$V=\pi(6^2-5^2)\cdot50=550\pi\approx\res{1727{,}88\text{ cm}^3}$."),
 (2, r"Un cubo de 10 cm de arista tiene un agujero cilíndrico de 3 cm de radio que lo atraviesa de lado a lado. ¿Qué volumen tiene?",
     r"$V=1000-\pi\cdot9\cdot10=1000-90\pi\approx\res{717{,}26\text{ cm}^3}$."),
 (3, r"Un cubo tiene forma de tronco de cono: el fondo mide 12 cm de radio, la boca 18 cm y la altura es de 24 cm. ¿Cuántos litros caben? \emph{(Pista: es un cono grande al que le quitamos un cono pequeño; calcula la altura del pequeño con el teorema de Tales.)}",
     r"Si el cono pequeño mide $x$ de altura: $\frac{x}{12}=\frac{x+24}{18}\Rightarrow x=48$. \ $V=\frac{\pi\cdot18^2\cdot72}{3}-\frac{\pi\cdot12^2\cdot48}{3}=7776\pi-2304\pi=5472\pi\approx17\,190{,}80\text{ cm}^3\approx\res{17{,}19\text{ L}}$."),
 (3, r"Dejamos caer una bola de acero de 3 cm de radio dentro de un vaso cilíndrico de 6 cm de radio que contiene agua (y la bola queda cubierta). ¿Cuánto sube el nivel del agua?",
     r"El volumen de la bola es $\frac43\pi\cdot27=36\pi$. \ $\pi\cdot36\cdot h=36\pi\Rightarrow\res{h=1\text{ cm}}$."),
 (3, r"Un depósito de agua es un cilindro de 2 m de radio y 5 m de altura con el fondo en forma de semiesfera. ¿Cuántos m³ caben? ¿Cuánto tiempo tardará en llenarse con un grifo que vierte 50 L por minuto?",
     r"$V=\pi\cdot4\cdot5+\frac12\cdot\frac43\pi\cdot8=20\pi+\frac{16\pi}{3}=\frac{76\pi}{3}\approx\res{79{,}59\text{ m}^3}$. \ $\frac{79\,587}{50}\approx1591{,}7$ min $\approx\res{26{,}5\text{ horas}}$."),
]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = "pdfkeywords={poliedres, fórmula d'Euler, poliedres regulars, prisma, piràmide, cilindre, con, esfera, àrea, volum, capacitat}"
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TITOL = 'Cossos geomètrics'
NU = 11

pre = pre_

def build(sol_):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, ASSIGNATURA
    t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 11: Cuerpos geométricos' % t, capcalera='%s · Unidad 11: Cuerpos geométricos' % t,
                 pdfkeywords='poliedros, fórmula de Euler, poliedros regulares, prisma, pirámide, cilindro, cono, esfera, área, volumen, capacidad')
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

''' + ASSIGNATURA + '{' + ('Soluciones de la ficha · Unidad 11' if sol_ else 'Ficha de ejercicios · Unidad 11') + '}{Cuerpos geométricos}\n')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás cuerpos que puedes girar y herramientas que calculan áreas y volúmenes paso a paso. Los resultados aproximados están redondeados a las centésimas con la tecla $\pi$ de la calculadora."
             if sol_ else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y haz un dibujo de cada cuerpo. Si un resultado no es exacto, redondéalo a las centésimas; para $\pi$, usa la tecla de la calculadora.") + r'''
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
    name = 't11-fitxa-solucions-es.tex' if sol_ else 't11-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
