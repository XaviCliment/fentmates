# Genera t11-fitxa-exercicis.tex i t11-fitxa-solucions.tex (3r ESO, Unitat 11: Cossos geomètrics)
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
TAU = [("prisma triangular", 5, 6, 9), ("piràmide pentagonal", 6, 6, 10), ("prisma hexagonal", 8, 12, 18), ("piràmide octogonal", 9, 9, 16), ("cub", 6, 8, 12)]
for _, C, V, A in TAU: assert euler(C, V, A)
assert 18 == 8 + 12 - 2 and 7 == 15 + 2 - 10 and 20 == 30 + 2 - 12
assert euler(10, 16, 24) and euler(11, 11, 20) and euler(7, 7, 12) and not euler(5, 6, 10) and euler(8, 6, 12) and euler(10, 7, 15)
S_.append(("Poliedres. Fórmula d'Euler. Poliedres regulars", [
 (1, r"Copia i completa la taula. Comprova en cada cas la fórmula d'Euler.\par\smallskip\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|l|C{1.6cm}|C{1.6cm}|C{1.6cm}|}\hline Poliedre & Cares & Vèrtexs & Arestes \\\hline "
     + r" \\\hline ".join(n + r" & & & " for n, *_ in TAU) + r" \\\hline\end{tabular}\end{center}"
     + recorda(r"En un poliedre convex, \textbf{cares} + \textbf{vèrtexs} = \textbf{arestes} + 2: \ $C+V=A+2$ (fórmula d'Euler). Un prisma de base de $n$ costats té $n+2$ cares, $2n$ vèrtexs i $3n$ arestes; una piràmide, $n+1$ cares, $n+1$ vèrtexs i $2n$ arestes."),
     r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|l|C{1.6cm}|C{1.6cm}|C{1.6cm}|l|}\hline Poliedre & $C$ & $V$ & $A$ & $C+V=A+2$ \\\hline "
     + r" \\\hline ".join(r"%s & %d & %d & %d & $%d=%d$" % (n, C, V, A, C + V, A + 2) for n, C, V, A in TAU) + r" \\\hline\end{tabular}\end{center}"),
 (1, r"Fes servir la fórmula d'Euler per a calcular el que falta en cada poliedre convex:" + tasks(3, [r"$C=8$, \ $V=12$, \ $A=\ ?$", r"$V=10$, \ $A=15$, \ $C=\ ?$", r"$C=12$, \ $A=30$, \ $V=\ ?$"]),
     tasks(3, [r"$8+12=A+2\Rightarrow\res{A=18}$", r"$C+10=17\Rightarrow\res{C=7}$", r"$12+V=32\Rightarrow\res{V=20}$"])),
 (1, r"Quins d'aquests poliedres són regulars? Justifica-ho." + tasks(3, [r"tetraedre", r"ortoedre", r"octaedre", r"piràmide quadrangular regular", r"icosaedre", r"cub"]),
     tasks(3, [r"\rest{sí}", r"no (rectangles diferents)", r"\rest{sí}", r"no (cares de dos tipus)", r"\rest{sí}", r"\rest{sí}"]) + r"Un poliedre regular té totes les cares polígons regulars iguals i el mateix nombre de cares a cada vèrtex."),
 (2, r"Un prisma té 24 arestes. Quin polígon té per base? Quantes cares i quants vèrtexs té?",
     r"$3n=24\Rightarrow n=8$: base \rest{octogonal}; \ $\res{C=10}$, \ $\res{V=16}$ \ ($10+16=24+2$)."),
 (2, r"Una piràmide té 11 vèrtexs. Quin polígon té per base? Quantes cares i arestes té?",
     r"$n+1=11\Rightarrow n=10$: base \rest{decagonal}; \ $\res{C=11}$, \ $\res{A=20}$ \ ($11+11=20+2$)."),
 (2, r"Pot existir un poliedre convex amb: \ a) 7 cares, 7 vèrtexs i 12 arestes? \ b) 5 cares, 6 vèrtexs i 10 arestes?",
     r"a) $7+7=14=12+2$: \rest{sí} (per exemple, una piràmide hexagonal). \ b) $5+6=11\neq12$: \rest{no}."),
 (3, r"Si ajuntem dues piràmides quadrangulars iguals per la base obtenim una \emph{bipiràmide}. Quantes cares, vèrtexs i arestes té? I si les piràmides són pentagonals?",
     r"Quadrangulars: $\res{C=8,\ V=6,\ A=12}$ (és un octaedre si les cares són equilàters). \ Pentagonals: $\res{C=10,\ V=7,\ A=15}$. \ En tots dos casos $C+V=A+2$."),
 (3, r"Explica per què no hi pot haver cap poliedre regular amb cares hexagonals.",
     r"Cada angle d'un hexàgon regular fa $120^\circ$. En un vèrtex s'hi han d'ajuntar com a mínim 3 cares, i $3\cdot120^\circ=360^\circ$: les cares quedarien \rest{planes} i no tancarien cap cos."),
]))

# =====================================================================
# 2. Prismes: elements i àrea
# =====================================================================
ck(6 * 16, 96); ck(2 * (24 + 18 + 12), 108); ck(S(144 + 16 + 9), 13); ck(20 * 12, 240); ck(240 + 50, 290)
ck(12 * 10, 120); ck(2 * S(12), 6.93, 2); ck(120 + 4 * S(12), 133.86, 2)
ck(36 * 8, 288); ck(S(27), 5.20, 2); ck(18 * S(27), 93.53, 2); ck(288 + 36 * S(27), 475.06, 2)
ck(1200 + 1600 + 1200, 4000); ck(S(R(48, 3)), 4); ck(S(36 + 64), 10); ck(24 * 15, 360); ck(360 + 48, 408)
ORT = tz(f_cuboid(6, 3, 4, la='6 cm', lb='3 cm', lc='4 cm')[0], 0.45)
S_.append(("Prismes: elements i àrea", [
 (1, side(r"Calcula l'àrea total:" + tasks(1, [r"d'un cub de 4 cm d'aresta;", r"de l'ortoedre de la figura."]), ORT, '0.34')
     + recorda(r"Àrea d'un prisma recte: $A_L=P_{\text{base}}\cdot h$, \ $A_T=A_L+2\,A_{\text{base}}$. Ortoedre d'arestes $a,\,b,\,c$: $A_T=2(ab+ac+bc)$ i la diagonal és $D=\sqrt{a^2+b^2+c^2}$."),
     tasks(2, [r"$6\cdot4^2=\res{96\text{ cm}^2}$", r"$2(6\cdot3+6\cdot4+3\cdot4)=2\cdot54=\res{108\text{ cm}^2}$"])),
 (1, r"Calcula la diagonal d'un ortoedre de 12 cm × 4 cm × 3 cm.",
     r"$D=\sqrt{144+16+9}=\sqrt{169}=\res{13\text{ cm}}$."),
 (1, r"Un prisma quadrangular regular té 5 cm d'aresta de la base i 12 cm d'altura. Calcula'n l'àrea lateral i l'àrea total.",
     r"$A_L=20\cdot12=\res{240\text{ cm}^2}$; \ $A_T=240+2\cdot25=\res{290\text{ cm}^2}$."),
 (2, r"Calcula l'àrea total d'un prisma triangular regular de 4 cm d'aresta de la base i 10 cm d'altura.",
     r"$A_L=12\cdot10=120$; altura de la base $\sqrt{16-4}=\sqrt{12}\approx3{,}46$; $A_{\text{base}}=\frac{4\cdot\sqrt{12}}{2}\approx6{,}93$. \ $A_T\approx120+2\cdot6{,}93=\res{133{,}86\text{ cm}^2}$."),
 (2, r"Calcula l'àrea total d'un prisma hexagonal regular de 6 cm d'aresta de la base i 8 cm d'altura.",
     r"$A_L=36\cdot8=288$; \ $a_b=\sqrt{36-9}=\sqrt{27}\approx5{,}20$; \ $A_{\text{base}}=\frac{36\cdot\sqrt{27}}{2}\approx93{,}53$. \ $A_T\approx288+187{,}06=\res{475{,}06\text{ cm}^2}$."),
 (2, r"Volem fer una caixa sense tapa de 40 cm × 30 cm de base i 20 cm d'altura. Quant cartó necessitem?",
     r"Base $40\cdot30=1200$; \ cares $2\cdot40\cdot20+2\cdot30\cdot20=2800$. \ Total: $\res{4000\text{ cm}^2}$."),
 (3, r"La diagonal d'un cub mesura $\sqrt{48}$ cm. Quant mesura l'aresta? Calcula'n l'àrea total.",
     r"$D^2=3l^2\Rightarrow3l^2=48\Rightarrow\res{l=4\text{ cm}}$; \ $A_T=6\cdot16=\res{96\text{ cm}^2}$."),
 (3, r"La base d'un prisma recte és un triangle rectangle de catets 6 cm i 8 cm, i l'altura del prisma és 15 cm. Calcula'n l'àrea total.",
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
S_.append(("Piràmides i troncs de piràmide", [
 (1, side(r"La piràmide quadrangular regular de la figura té 10 cm d'aresta de la base i 12 cm d'altura. Calcula'n l'apotema i l'àrea total.", PYF, '0.3')
     + recorda(r"En una piràmide regular, l'altura $h$, l'apotema de la base $a_b$ i l'apotema de la piràmide $a_p$ formen un triangle rectangle: $a_p^2=h^2+a_b^2$. \ $A_L=\frac{P_{\text{base}}\cdot a_p}{2}$, \ $A_T=A_L+A_{\text{base}}$."),
     r"$a_b=5$; \ $a_p=\sqrt{144+25}=\res{13\text{ cm}}$. \ $A_T=\frac{40\cdot13}{2}+100=\res{360\text{ cm}^2}$."),
 (1, r"Una piràmide hexagonal regular té 4 cm d'aresta de la base i 9 cm d'apotema. Calcula'n l'àrea lateral.",
     r"$A_L=\frac{24\cdot9}{2}=\res{108\text{ cm}^2}$."),
 (2, r"Una piràmide quadrangular regular té 6 cm d'aresta de la base i 5 cm d'apotema. Quina altura té? Calcula'n l'àrea total.",
     r"$h=\sqrt{5^2-3^2}=\res{4\text{ cm}}$; \ $A_T=\frac{24\cdot5}{2}+36=\res{96\text{ cm}^2}$."),
 (2, r"Una piràmide quadrangular regular té 8 cm d'aresta de la base i 6 cm d'altura. Calcula l'apotema, l'aresta lateral i l'àrea total.",
     r"$a_p=\sqrt{36+16}=\sqrt{52}\approx\res{7{,}21\text{ cm}}$; \ aresta: $\sqrt{a_p^2+4^2}=\sqrt{68}\approx\res{8{,}25\text{ cm}}$; \ $A_T=\frac{32\cdot\sqrt{52}}{2}+64\approx\res{179{,}38\text{ cm}^2}$."),
 (2, r"Calcula l'àrea total d'un tetraedre regular de 6 cm d'aresta.",
     r"Cada cara és un triangle equilàter d'altura $\sqrt{36-9}=\sqrt{27}\approx5{,}20$: \ $A=4\cdot\frac{6\cdot\sqrt{27}}{2}\approx\res{62{,}35\text{ cm}^2}$."),
 (3, r"Un tronc de piràmide quadrangular regular té les arestes de les bases de 12 cm i 6 cm i una altura de 4 cm. Calcula l'apotema del tronc i l'àrea total.",
     r"$a_p=\sqrt{4^2+3^2}=\res{5\text{ cm}}$ \ (catets: l'altura i $\frac{12-6}{2}=3$). \ $A_T=\frac{(48+24)\cdot5}{2}+144+36=\res{360\text{ cm}^2}$."),
 (3, r"La gran piràmide de Khufu (Gizeh) té una base quadrada de 230 m de costat i fa 146 m d'altura. Calcula l'apotema i l'àrea de les quatre cares laterals.",
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
S_.append(("Cilindre i con", [
 (1, side(r"Calcula l'àrea lateral i l'àrea total del cilindre de la figura.", CYF, '0.25')
     + recorda(r"Cilindre: $A_L=2\pi rh$, \ $A_T=2\pi rh+2\pi r^2$. \ Con: $g^2=h^2+r^2$, \ $A_L=\pi rg$, \ $A_T=\pi rg+\pi r^2$. Fes servir la tecla $\pi$ i arrodoneix a les centèsimes."),
     r"$A_L=2\pi\cdot3\cdot10=60\pi\approx\res{188{,}50\text{ cm}^2}$; \ $A_T=60\pi+18\pi=78\pi\approx\res{245{,}04\text{ cm}^2}$."),
 (1, side(r"Calcula la generatriu, l'àrea lateral i l'àrea total del con de la figura.", CNF, '0.25'),
     r"$g=\sqrt{144+25}=\res{13\text{ cm}}$; \ $A_L=\pi\cdot5\cdot13=65\pi\approx\res{204{,}20\text{ cm}^2}$; \ $A_T=65\pi+25\pi=90\pi\approx\res{282{,}74\text{ cm}^2}$."),
 (1, r"Un con té 6 cm de radi i 10 cm de generatriu. Quina altura té? Calcula'n l'àrea total.",
     r"$h=\sqrt{100-36}=\res{8\text{ cm}}$; \ $A_T=60\pi+36\pi=96\pi\approx\res{301{,}59\text{ cm}^2}$."),
 (2, r"Una llanda de refresc té 8 cm de diàmetre i 12 cm d'altura. Quanta xapa cal per a fer-la?",
     r"$r=4$: \ $A_T=2\pi\cdot4\cdot12+2\pi\cdot16=96\pi+32\pi=128\pi\approx\res{402{,}12\text{ cm}^2}$."),
 (2, r"Volem fer un barret de pallasso en forma de con de 9 cm de radi i 12 cm d'altura. Quant paper necessitem?",
     r"$g=\sqrt{81+144}=15$; \ només la superfície lateral: $A_L=\pi\cdot9\cdot15=135\pi\approx\res{424{,}12\text{ cm}^2}$."),
 (2, r"Un cilindre té una àrea lateral de $120\pi$ cm² i 10 cm d'altura. Quin radi té? Calcula'n l'àrea total.",
     r"$2\pi r\cdot10=120\pi\Rightarrow\res{r=6\text{ cm}}$; \ $A_T=120\pi+72\pi=192\pi\approx\res{603{,}19\text{ cm}^2}$."),
 (3, r"Un con té 4 cm de radi i 12 cm de generatriu. Quin angle té el sector circular del seu desenvolupament?",
     r"L'arc del sector fa $2\pi\cdot4=8\pi$ i la circumferència sencera de radi 12 faria $24\pi$: és $\frac{8\pi}{24\pi}=\frac13$ del cercle. \ Angle: $\frac{360^\circ}{3}=\res{120^\circ}$."),
 (3, r"Cal pintar la superfície lateral de 12 columnes cilíndriques de 0,4 m de radi i 5 m d'altura. Si un litre de pintura cobreix 4 m², quants litres calen?",
     r"$A=12\cdot2\pi\cdot0{,}4\cdot5=48\pi\approx150{,}80\text{ m}^2$; \ $\frac{150{,}80}{4}\approx\res{37{,}70\text{ L}}$."),
]))

# =====================================================================
# 5. L'esfera. La Terra
# =====================================================================
ck(64 * pi, 201.06, 2); ck(100 * pi, 314.16, 2); ck(pi, 3.14, 2); ck(S(R(144, 4)), 6); ck(50 * pi, 157.08, 2)
ck(R(40000 * 50, 360), 5555.56, 2); ck(R(6371, 1737) ** 2, 13.45, 2)
SPF = tz(f_sphere(1.6, lr='r')[0], 0.5)
S_.append(("L'esfera. La Terra", [
 (1, side(r"Calcula l'àrea de:" + tasks(1, [r"una esfera de 4 cm de radi;", r"una pilota de 10 cm de diàmetre;", r"una bola de 0,5 m de radi."]), SPF, '0.22')
     + recorda(r"Àrea de l'esfera: $A=4\pi r^2$ (quatre cercles màxims). \ La \textbf{latitud} va de $0^\circ$ a $90^\circ$ N o S (des de l'equador) i la \textbf{longitud}, de $0^\circ$ a $180^\circ$ E o O (des del meridià de Greenwich)."),
     tasks(3, [r"$64\pi\approx\res{201{,}06\text{ cm}^2}$", r"$100\pi\approx\res{314{,}16\text{ cm}^2}$", r"$\pi\approx\res{3{,}14\text{ m}^2}$"])),
 (2, r"Una esfera té una àrea de $144\pi$ cm². Quin radi té?",
     r"$4\pi r^2=144\pi\Rightarrow r^2=36\Rightarrow\res{r=6\text{ cm}}$."),
 (2, r"Una cúpula té forma de semiesfera de 5 m de radi. Quina superfície cal impermeabilitzar per fora?",
     r"Mitja esfera: $\frac{4\pi\cdot25}{2}=50\pi\approx\res{157{,}08\text{ m}^2}$."),
 (2, r"Dues ciutats estan sobre el mateix meridià, l'una a $40^\circ$ N i l'altra a $10^\circ$ S. Quants graus de latitud les separen? Si un meridià sencer (la volta a la Terra) fa 40\,000 km, quina distància hi ha entre elles sobre el meridià?",
     r"$40^\circ+10^\circ=\res{50^\circ}$; \ $\frac{40\,000\cdot50}{360}\approx\res{5555{,}56\text{ km}}$."),
 (2, r"Quan a Greenwich són les 12 hores solars, quina hora solar és en un lloc de longitud $45^\circ$ E? I en un de longitud $30^\circ$ O?",
     r"Cada $15^\circ$ és una hora: \ $45^\circ$ E $\to$ 3 hores més: \res{15 h}; \ $30^\circ$ O $\to$ 2 hores menys: \res{10 h}."),
 (3, r"El radi de la Terra és 6371 km i el de la Lluna, 1737 km. Quantes vegades més gran és la superfície de la Terra que la de la Lluna?",
     r"$\frac{4\pi\cdot6371^2}{4\pi\cdot1737^2}=\left(\frac{6371}{1737}\right)^2\approx\res{13{,}45}$ vegades."),
]))

# =====================================================================
# 6. Volum. Prismes i cilindres
# =====================================================================
for v, w in [(R(32, 10) * 1000, 3200), (R(450, 1000), 0.45), (R(25, 10) * 1000, 2500), (R(75, 100) * 1000, 750), (R(12000, 1000), 12), (R(5, 10), 0.5)]: ck(v, w)
ck(216, 216); ck(8 * 5 * 3, 120); ck(160 * pi, 502.65, 2); ck(R(5 * 12, 2) * 20, 600)
ck(6 * S(3), 10.39, 2); ck(30 * S(3), 51.96, 2); ck(R(60 * 30 * 40, 1000), 72); ck(72 * R(3, 4), 54)
ck(9 * pi, 28.27, 2); ck(9000 * pi, 28274, 0); ck(R(1 + 3, 2) * 25 * 10, 500); ck(500 / (16 * pi), 9.95, 2)
ck(24 * R(115, 10) * 5, 1380); ck(1380 - R(3375, 100) * pi, 1273.97, 2)
S_.append(("Volum. Prismes i cilindres", [
 (1, r"Expressa en la unitat indicada:" + tasks(3, [r"3,2 m³ en L", r"450 cm³ en L", r"2,5 L en cm³", r"0,75 dm³ en mL", r"12\,000 L en m³", r"5 hL en m³"])
     + recorda(r"Cada unitat de volum és 1000 vegades la següent: $1\text{ m}^3=1000\text{ dm}^3$, \ $1\text{ dm}^3=1000\text{ cm}^3$. \ $1\text{ dm}^3=1\text{ L}$, \ $1\text{ cm}^3=1\text{ mL}$. \ Prisma i cilindre: $V=A_{\text{base}}\cdot h$; \ $V_{\text{cilindre}}=\pi r^2h$."),
     tasks(3, [r"$\res{3200\text{ L}}$", r"$\res{0{,}45\text{ L}}$", r"$\res{2500\text{ cm}^3}$", r"$\res{750\text{ mL}}$", r"$\res{12\text{ m}^3}$", r"$\res{0{,}5\text{ m}^3}$"])),
 (1, r"Calcula el volum de:" + tasks(1, [r"un cub de 6 cm d'aresta;", r"un ortoedre de 8 cm × 5 cm × 3 cm;", r"un cilindre de 4 cm de radi i 10 cm d'altura."]),
     tasks(3, [r"$6^3=\res{216\text{ cm}^3}$", r"$\res{120\text{ cm}^3}$", r"$160\pi\approx\res{502{,}65\text{ cm}^3}$"])),
 (1, r"La base d'un prisma és un triangle rectangle de catets 5 cm i 12 cm. Si el prisma fa 20 cm d'altura, quin volum té?",
     r"$V=\frac{5\cdot12}{2}\cdot20=\res{600\text{ cm}^3}$."),
 (2, r"Calcula el volum d'un prisma hexagonal regular de 2 cm d'aresta de la base i 5 cm d'altura.",
     r"$a_b=\sqrt{4-1}=\sqrt3$; \ $A_{\text{base}}=\frac{12\cdot\sqrt3}{2}=6\sqrt3\approx10{,}39$; \ $V\approx\res{51{,}96\text{ cm}^3}$."),
 (2, r"Un aquari fa 60 cm × 30 cm de base i 40 cm d'altura. Quants litres hi caben? Quants litres hi ha si l'aigua arriba a $\frac34$ de l'altura?",
     r"$V=72\,000\text{ cm}^3=\res{72\text{ L}}$; \ $\frac34\cdot72=\res{54\text{ L}}$."),
 (2, r"Un dipòsit cilíndric té 1,5 m de radi i 4 m d'altura. Quants litres d'aigua hi caben?",
     r"$V=\pi\cdot1{,}5^2\cdot4=9\pi\approx28{,}27\text{ m}^3\approx\res{28\,274\text{ L}}$."),
 (2, r"Una piscina fa 25 m de llarg i 10 m d'ample. El fons és inclinat: la fondària va d'1 m a 3 m. Quin volum d'aigua hi cap? (És un prisma amb una base en forma de trapezi.)",
     r"Base (el lateral de la piscina): $\frac{(1+3)\cdot25}{2}=50\text{ m}^2$; \ $V=50\cdot10=\res{500\text{ m}^3}$."),
 (3, r"Un got cilíndric fa 4 cm de radi. Si hi aboquem mig litre d'aigua, fins a quina altura arriba?",
     r"$\pi\cdot16\cdot h=500\Rightarrow h=\frac{500}{16\pi}\approx\res{9{,}95\text{ cm}}$."),
 (3, r"Una rajola fa 24 cm × 11,5 cm × 5 cm i té tres forats cilíndrics de 1,5 cm de radi que la travessen (en la direcció dels 5 cm). Quin volum de fang té?",
     r"$V=24\cdot11{,}5\cdot5-3\cdot\pi\cdot1{,}5^2\cdot5=1380-33{,}75\pi\approx\res{1273{,}97\text{ cm}^3}$."),
]))

# =====================================================================
# 7. Volum de piràmides, cons i esferes
# =====================================================================
ck(R(36 * 10, 3), 120); ck(21 * pi, 65.97, 2); ck(288 * pi, 904.78, 2); ck(R(4000, 3) * pi, 4188.79, 2)
ck(S(169 - 25), 12); ck(R(100 * 12, 3), 400); ck(S(100 - 36), 8); ck(96 * pi, 301.59, 2); ck(R(4, 3) * pi * 1331, 5575.28, 2)
ck(36 * S(12), 124.71, 2); ck(1152 * pi, 3619.11, 2); assert sp.solve(R(1, 3) * 36 * x - R(4, 3) * 216, x) == [24]
S_.append(("Volum de piràmides, cons i esferes", [
 (1, r"Calcula el volum de:" + tasks(1, [r"una piràmide quadrangular de 6 cm d'aresta de la base i 10 cm d'altura;", r"un con de 3 cm de radi i 7 cm d'altura;", r"una esfera de 6 cm de radi."])
     + recorda(r"$V_{\text{piràmide}}=\frac{A_{\text{base}}\cdot h}{3}$; \ $V_{\text{con}}=\frac{\pi r^2h}{3}$; \ $V_{\text{esfera}}=\frac43\pi r^3$."),
     tasks(3, [r"$\frac{36\cdot10}{3}=\res{120\text{ cm}^3}$", r"$21\pi\approx\res{65{,}97\text{ cm}^3}$", r"$288\pi\approx\res{904{,}78\text{ cm}^3}$"])),
 (1, r"Quin volum té una bola de 20 cm de diàmetre? Expressa'l en cm³ i en litres.",
     r"$r=10$: \ $V=\frac43\pi\cdot1000\approx\res{4188{,}79\text{ cm}^3}\approx\res{4{,}19\text{ L}}$."),
 (2, r"Una piràmide quadrangular regular té 10 cm d'aresta de la base i 13 cm d'apotema. Calcula'n l'altura i el volum.",
     r"$h=\sqrt{13^2-5^2}=\res{12\text{ cm}}$; \ $V=\frac{100\cdot12}{3}=\res{400\text{ cm}^3}$."),
 (2, r"Un con té 6 cm de radi i 10 cm de generatriu. Calcula'n el volum.",
     r"$h=\sqrt{100-36}=8$; \ $V=\frac{\pi\cdot36\cdot8}{3}=96\pi\approx\res{301{,}59\text{ cm}^3}$."),
 (2, r"Quants litres d'aire hi ha dins d'una pilota de bàsquet d'11 cm de radi?",
     r"$V=\frac43\pi\cdot11^3\approx5575{,}28\text{ cm}^3\approx\res{5{,}58\text{ L}}$."),
 (2, r"Calcula el volum d'una piràmide hexagonal regular de 4 cm d'aresta de la base i 9 cm d'altura.",
     r"$a_b=\sqrt{12}$; \ $A_{\text{base}}=\frac{24\cdot\sqrt{12}}{2}\approx41{,}57$; \ $V=\frac{A_{\text{base}}\cdot9}{3}\approx\res{124{,}71\text{ cm}^3}$."),
 (3, r"Un bol té forma de semiesfera de 12 cm de radi interior. Quants litres hi caben?",
     r"$V=\frac12\cdot\frac43\pi\cdot12^3=1152\pi\approx3619{,}11\text{ cm}^3\approx\res{3{,}62\text{ L}}$."),
 (3, r"Una esfera i un con tenen el mateix radi, 6 cm, i el mateix volum. Quina altura té el con?",
     r"$\frac13\pi\cdot36\cdot h=\frac43\pi\cdot216\Rightarrow12h=288\Rightarrow\res{h=24\text{ cm}}$ \ (quatre vegades el radi)."),
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
S_.append(("Cossos compostos i problemes", [
 (1, r"Una peça està formada per un cub de 6 cm d'aresta i, al damunt, una piràmide de la mateixa base i 4 cm d'altura. Calcula'n el volum."
     + recorda(r"Descompon el cos en cossos simples. El volum és la suma (o la diferència, si hi ha forats) dels volums. Per a l'àrea, suma només les superfícies que queden per fora."),
     r"$V=6^3+\frac{36\cdot4}{3}=216+48=\res{264\text{ cm}^3}$."),
 (2, side(r"Una sitja té la forma de la figura: un cilindre de 3 m de radi i 10 m d'altura amb una teulada cònica de 4 m d'altura. Quin volum té?", tz(SIT, 0.42), '0.25'),
     r"$V=\pi\cdot9\cdot10+\frac{\pi\cdot9\cdot4}{3}=90\pi+12\pi=102\pi\approx\res{320{,}44\text{ m}^3}$."),
 (2, side(r"Una càpsula és un cilindre de 2 cm de radi i 6 cm de llarg amb una semiesfera a cada extrem. Calcula'n el volum i l'àrea.", tz(CAP, 0.5), '0.2'),
     r"$V=\pi\cdot4\cdot6+\frac43\pi\cdot8=24\pi+\frac{32\pi}{3}=\frac{104\pi}{3}\approx\res{108{,}91\text{ cm}^3}$; \ $A=2\pi\cdot2\cdot6+4\pi\cdot4=40\pi\approx\res{125{,}66\text{ cm}^2}$."),
 (2, r"Un gelat és un cucurutxo cònic de 2,5 cm de radi i 12 cm d'altura, ple, amb una semiesfera de gelat al damunt. Quin volum de gelat hi ha?",
     r"$V=\frac{\pi\cdot2{,}5^2\cdot12}{3}+\frac12\cdot\frac43\pi\cdot2{,}5^3=25\pi+\frac{125\pi}{12}=\frac{425\pi}{12}\approx\res{111{,}26\text{ cm}^3}$."),
 (2, r"Un tub de 50 cm de llarg té 6 cm de radi exterior i 5 cm de radi interior. Quin volum de material té?",
     r"$V=\pi(6^2-5^2)\cdot50=550\pi\approx\res{1727{,}88\text{ cm}^3}$."),
 (2, r"Un cub de 10 cm d'aresta té un forat cilíndric de 3 cm de radi que el travessa de banda a banda. Quin volum té?",
     r"$V=1000-\pi\cdot9\cdot10=1000-90\pi\approx\res{717{,}26\text{ cm}^3}$."),
 (3, r"Un cubell té forma de tronc de con: el fons fa 12 cm de radi, la boca 18 cm i l'altura és de 24 cm. Quants litres hi caben? \emph{(Pista: és un con gran al qual llevem un con menut; calcula l'altura del menut amb el teorema de Tales.)}",
     r"Si el con menut fa $x$ d'altura: $\frac{x}{12}=\frac{x+24}{18}\Rightarrow x=48$. \ $V=\frac{\pi\cdot18^2\cdot72}{3}-\frac{\pi\cdot12^2\cdot48}{3}=7776\pi-2304\pi=5472\pi\approx17\,190{,}80\text{ cm}^3\approx\res{17{,}19\text{ L}}$."),
 (3, r"Deixem caure una bola d'acer de 3 cm de radi dins d'un got cilíndric de 6 cm de radi que conté aigua (i la bola queda coberta). Quant puja el nivell de l'aigua?",
     r"El volum de la bola és $\frac43\pi\cdot27=36\pi$. \ $\pi\cdot36\cdot h=36\pi\Rightarrow\res{h=1\text{ cm}}$."),
 (3, r"Un dipòsit d'aigua és un cilindre de 2 m de radi i 5 m d'altura amb el fons en forma de semiesfera. Quants m³ hi caben? Quant de temps tardarà a omplir-se amb una aixeta que aboca 50 L per minut?",
     r"$V=\pi\cdot4\cdot5+\frac12\cdot\frac43\pi\cdot8=20\pi+\frac{16\pi}{3}=\frac{76\pi}{3}\approx\res{79{,}59\text{ m}^3}$. \ $\frac{79\,587}{50}\approx1591{,}7$ min $\approx\res{26{,}5\text{ hores}}$."),
]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = "pdfkeywords={poliedres, fórmula d'Euler, poliedres regulars, prisma, piràmide, cilindre, con, esfera, àrea, volum, capacitat}"
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
TITOL = 'Cossos geomètrics'
NU = 11

def build(sol_):
    t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
    p = pre_.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                     "pdftitle={%s de la unitat %d: %s. 3r d'ESO}" % (t, NU, TITOL))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat %d: %s · 3r d'ESO" % (t, NU, TITOL))
    assert 'Unitat %d' % NU in p and 'unitat %d' % NU in p
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{3r ESO}{''' + ('Solucions de la fitxa · Unitat %d' % NU if sol_ else "Fitxa d'exercicis · Unitat %d" % NU) + '}{' + TITOL + r'''}
''')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs cossos que pots girar i eines que calculen àrees i volums pas a pas. Els resultats aproximats estan arrodonits a les centèsimes amb la tecla $\pi$ de la calculadora."
             if sol_ else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i fes un dibuix de cada cos. Si un resultat no és exacte, arrodoneix-lo a les centèsimes; per a $\pi$, fes servir la tecla de la calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st_, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st_, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't%d-fitxa-solucions.tex' % NU if sol_ else 't%d-fitxa-exercicis.tex' % NU
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
