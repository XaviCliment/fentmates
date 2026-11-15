# Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex (2n ESO, Unitat 9: Cossos geomètrics. Àrees i volums)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 8 seccions segueixen els apartats dels apunts (9.1-9.8). Cada resultat numèric es comprova amb
# ck(valor exacte, valor escrit, decimals de l'arrodoniment).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Els cossos es dibuixen amb ../../apunts/2eso-t9/solids.py i fig11.py (la mateixa perspectiva que als apunts); el dibuix
# en TikZ (tz) és el de la fitxa de 3r ESO (../3eso-t11/genera.py).
# Ús: python3 genera.py && pdflatex t9-fitxa-exercicis.tex (dues vegades) && pdflatex t9-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '2eso-t9'))
from solids import polyhedron, cuboid, PH
from fig11 import f_cuboid, f_pyramid, f_cylinder, f_cone
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

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
def side(t, f, w='0.3'):
    """enunciat a l'esquerra (a continuació del número) i figura a la dreta"""
    return (r'\begin{minipage}[t]{%.2f\linewidth}%s\end{minipage}\hfill\begin{minipage}[t]{%s\linewidth}\vspace{0pt}\centering %s\end{minipage}\par'
            % (0.86 - float(w), t, w, f))
CM = lambda n: n + ' cm'

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Poliedres. Fórmula d'Euler. Poliedres regulars
# =====================================================================
TAU = [(T("prisma pentagonal", "prisma pentagonal"), 7, 10, 15), (T("piràmide hexagonal", "pirámide hexagonal"), 7, 7, 12), (T("prisma triangular", "prisma triangular"), 5, 6, 9),
       (T("piràmide quadrangular", "pirámide cuadrangular"), 5, 5, 8), (T("ortoedre", "ortoedro"), 6, 8, 12)]
for _, C, V, A in TAU: assert euler(C, V, A)
assert euler(6, 8, 12) and euler(8, 12, 18) and euler(7, 7, 12) and euler(8, 12, 18) and euler(9, 9, 16) and euler(8, 12, 18) and not euler(6, 7, 12)
HEAD1 = T(r"Poliedre & Cares & Vèrtexs & Arestes", r"Poliedro & Caras & Vértices & Aristas")
REG = [(T("tetraedre", "tetraedro"), True, ''), (T("prisma triangular", "prisma triangular"), False, T("cares de dos tipus", "caras de dos tipos")),
       (T("cub", "cubo"), True, ''), (T("piràmide quadrangular", "pirámide cuadrangular"), False, T("cares de dos tipus", "caras de dos tipos")),
       (T("dodecaedre", "dodecaedro"), True, ''), (T("ortoedre", "ortoedro"), False, T("rectangles diferents", "rectángulos distintos"))]
PLT = [(T("Tetraedre", "Tetraedro"), 4, T("triangles", "triángulos"), 3), (T("Cub", "Cubo"), 6, T("quadrats", "cuadrados"), 3), (T("Octaedre", "Octaedro"), 8, T("triangles", "triángulos"), 4),
       (T("Dodecaedre", "Dodecaedro"), 12, T("pentàgons", "pentágonos"), 3), (T("Icosaedre", "Icosaedro"), 20, T("triangles", "triángulos"), 5)]
S_.append((T("Poliedres. Fórmula d'Euler. Poliedres regulars", "Poliedros. Fórmula de Euler. Poliedros regulares"), [
 (1, T(r"Copia i completa la taula. Comprova en cada cas la fórmula d'Euler.", r"Copia y completa la tabla. Comprueba en cada caso la fórmula de Euler.")
     + r"\par\smallskip\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|l|C{1.6cm}|C{1.6cm}|C{1.6cm}|}\hline " + HEAD1 + r" \\\hline "
     + r" \\\hline ".join(n + r" & & & " for n, *_ in TAU) + r" \\\hline\end{tabular}\end{center}"
     + recorda(T(r"En un poliedre convex, \textbf{cares} + \textbf{vèrtexs} = \textbf{arestes} + 2: \ $C+V=A+2$ (fórmula d'Euler). Un prisma de base de $n$ costats té $n+2$ cares, $2n$ vèrtexs i $3n$ arestes; una piràmide, $n+1$ cares, $n+1$ vèrtexs i $2n$ arestes.",
                 r"En un poliedro convexo, \textbf{caras} + \textbf{vértices} = \textbf{aristas} + 2: \ $C+V=A+2$ (fórmula de Euler). Un prisma de base de $n$ lados tiene $n+2$ caras, $2n$ vértices y $3n$ aristas; una pirámide, $n+1$ caras, $n+1$ vértices y $2n$ aristas.")),
     r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{|l|C{1.6cm}|C{1.6cm}|C{1.6cm}|l|}\hline " + T("Poliedre", "Poliedro") + r" & $C$ & $V$ & $A$ & $C+V=A+2$ \\\hline "
     + r" \\\hline ".join(r"%s & %d & %d & %d & $%d=%d$" % (n, C, V, A, C + V, A + 2) for n, C, V, A in TAU) + r" \\\hline\end{tabular}\end{center}"),
 (1, T(r"Fes servir la fórmula d'Euler per a calcular el que falta en cada poliedre convex:", r"Usa la fórmula de Euler para calcular lo que falta en cada poliedro convexo:")
     + tasks(3, [r"$C=6$, \ $V=8$, \ $A=\ ?$", r"$V=12$, \ $A=18$, \ $C=\ ?$", r"$C=7$, \ $A=12$, \ $V=\ ?$"]),
     tasks(3, [r"$6+8=A+2\Rightarrow\res{A=12}$", r"$C+12=20\Rightarrow\res{C=8}$", r"$7+V=14\Rightarrow\res{V=7}$"])),
 (1, T(r"Quins d'aquests poliedres són regulars? Justifica-ho.", r"¿Cuáles de estos poliedros son regulares? Justifícalo.") + tasks(3, [n for n, *_ in REG]),
     tasks(3, [(r"\rest{%s}" % T("sí", "sí")) if ok else T("no", "no") + " (%s)" % why for _, ok, why in REG])
     + T(r"Un poliedre regular té totes les cares polígons regulars iguals i el mateix nombre de cares a cada vèrtex.", r"Un poliedro regular tiene todas las caras polígonos regulares iguales y el mismo número de caras en cada vértice.")),
 (2, T(r"Escriu, per a cadascun dels cinc poliedres regulars, quantes cares té, quina forma tenen i quantes cares es troben a cada vèrtex.", r"Escribe, para cada uno de los cinco poliedros regulares, cuántas caras tiene, qué forma tienen y cuántas caras se encuentran en cada vértice."),
     r"\begin{center}\renewcommand{\arraystretch}{1.2}\begin{tabular}{|l|c|c|c|}\hline & " + T("Cares", "Caras") + " & " + T("Forma", "Forma") + " & " + T("Cares per vèrtex", "Caras por vértice") + r" \\\hline "
     + r" \\\hline ".join(r"%s & %d & %s & %d" % p for p in PLT) + r" \\\hline\end{tabular}\end{center}"),
 (2, T(r"Un prisma té 18 arestes. Quin polígon té per base? Quantes cares i quants vèrtexs té?", r"Un prisma tiene 18 aristas. ¿Qué polígono tiene por base? ¿Cuántas caras y cuántos vértices tiene?"),
     r"$3n=18\Rightarrow n=6$: " + T("base", "base") + r" \rest{" + T("hexagonal", "hexagonal") + r"}; \ $\res{C=8}$, \ $\res{V=12}$ \ ($8+12=18+2$)."),
 (2, T(r"Una piràmide té 9 cares. Quin polígon té per base? Quants vèrtexs i arestes té?", r"Una pirámide tiene 9 caras. ¿Qué polígono tiene por base? ¿Cuántos vértices y aristas tiene?"),
     r"$n+1=9\Rightarrow n=8$: " + T("base", "base") + r" \rest{" + T("octogonal", "octogonal") + r"}; \ $\res{V=9}$, \ $\res{A=16}$ \ ($9+9=16+2$)."),
 (3, T(r"Pot existir un poliedre convex amb: \ a) 8 cares, 12 vèrtexs i 18 arestes? \ b) 6 cares, 7 vèrtexs i 12 arestes?", r"¿Puede existir un poliedro convexo con: \ a) 8 caras, 12 vértices y 18 aristas? \ b) 6 caras, 7 vértices y 12 aristas?"),
     T(r"a) $8+12=20=18+2$: \rest{sí} (per exemple, un prisma hexagonal). \ b) $6+7=13\neq14$: \rest{no}.", r"a) $8+12=20=18+2$: \rest{sí} (por ejemplo, un prisma hexagonal). \ b) $6+7=13\neq14$: \rest{no}.")),
 (3, T(r"Explica per què no hi pot haver cap poliedre regular amb cares hexagonals.", r"Explica por qué no puede haber ningún poliedro regular con caras hexagonales."),
     T(r"Cada angle d'un hexàgon regular fa $120^\circ$. En un vèrtex s'hi han d'ajuntar com a mínim 3 cares, i $3\cdot120^\circ=360^\circ$: les cares quedarien \rest{planes} i no tancarien cap cos.",
       r"Cada ángulo de un hexágono regular mide $120^\circ$. En un vértice deben juntarse como mínimo 3 caras, y $3\cdot120^\circ=360^\circ$: las caras quedarían \rest{planas} y no cerrarían ningún cuerpo.")),
]))

# =====================================================================
# 2. Prismes: elements i àrea
# =====================================================================
ck(6 * 25, 150); ck(2 * (28 + 21 + 12), 122); ck(S(36 + 4 + 9), 7); ck(16 * 10, 160); ck(160 + 32, 192)
ck(S(25 + 144), 13); ck(30 * 10, 300); ck(300 + 60, 360)
ck(S(48), 6.93, 2); ck(48 * 5, 240); ck(24 * S(48), 166.28, 2); ck(240 + 48 * S(48), 572.55, 2)
ck(600 + 900 + 600, 2100); ck(S(108), 10.39, 2); ck(2 * R(75, 10) * R(25, 10), R(375, 10)); ck(R(375, 10) - R(16, 10) - R(12, 10), R(347, 10)); ck(R(347, 10) * 4, R(1388, 10))
ORT = tz(f_cuboid(7, 4, 3, la=CM('7'), lb=CM('4'), lc=CM('3'))[0], 0.42)
S_.append((T("Prismes: elements i àrea", "Prismas: elementos y área"), [
 (1, side(T(r"Calcula l'àrea total:", r"Calcula el área total:") + tasks(1, [T(r"d'un cub de 5 cm d'aresta;", r"de un cubo de 5 cm de arista;"), T(r"de l'ortoedre de la figura.", r"del ortoedro de la figura.")]), ORT, '0.36')
     + recorda(T(r"Àrea d'un prisma recte: $A_L=P_{\text{base}}\cdot h$, \ $A_T=A_L+2\,A_{\text{base}}$. Ortoedre d'arestes $a,\,b,\,c$: $A_T=2(ab+ac+bc)$ i la diagonal és $D=\sqrt{a^2+b^2+c^2}$.",
                 r"Área de un prisma recto: $A_L=P_{\text{base}}\cdot h$, \ $A_T=A_L+2\,A_{\text{base}}$. Ortoedro de aristas $a,\,b,\,c$: $A_T=2(ab+ac+bc)$ y la diagonal es $D=\sqrt{a^2+b^2+c^2}$.")),
     tasks(2, [r"$6\cdot5^2=\res{150\text{ cm}^2}$", r"$2(7\cdot4+7\cdot3+4\cdot3)=2\cdot61=\res{122\text{ cm}^2}$"])),
 (1, T(r"Calcula la diagonal d'un ortoedre de 6 cm × 2 cm × 3 cm.", r"Calcula la diagonal de un ortoedro de 6 cm × 2 cm × 3 cm."),
     r"$D=\sqrt{36+4+9}=\sqrt{49}=\res{7\text{ cm}}$."),
 (1, T(r"Un prisma quadrangular regular té 4 cm d'aresta de la base i 10 cm d'altura. Calcula'n l'àrea lateral i l'àrea total.", r"Un prisma cuadrangular regular tiene 4 cm de arista de la base y 10 cm de altura. Calcula su área lateral y su área total."),
     r"$A_L=16\cdot10=\res{160\text{ cm}^2}$; \ $A_T=160+2\cdot16=\res{192\text{ cm}^2}$."),
 (2, T(r"La base d'un prisma recte és un triangle rectangle de catets 5 cm i 12 cm, i l'altura del prisma és de 10 cm. Calcula'n l'àrea total.", r"La base de un prisma recto es un triángulo rectángulo de catetos 5 cm y 12 cm, y la altura del prisma es de 10 cm. Calcula su área total."),
     T(r"Hipotenusa: $\sqrt{25+144}=13$. \ $A_L=(5+12+13)\cdot10=300$; \ $A_{\text{base}}=\frac{5\cdot12}{2}=30$. \ $A_T=300+60=\res{360\text{ cm}^2}$.",
       r"Hipotenusa: $\sqrt{25+144}=13$. \ $A_L=(5+12+13)\cdot10=300$; \ $A_{\text{base}}=\frac{5\cdot12}{2}=30$. \ $A_T=300+60=\res{360\text{ cm}^2}$.")),
 (2, T(r"Calcula l'àrea total d'un prisma hexagonal regular de 8 cm d'aresta de la base i 5 cm d'altura.", r"Calcula el área total de un prisma hexagonal regular de 8 cm de arista de la base y 5 cm de altura."),
     r"$A_L=48\cdot5=240$; \ $a_b=\sqrt{64-16}=\sqrt{48}\approx6{,}93$; \ $A_{\text{base}}=\frac{48\cdot\sqrt{48}}{2}\approx166{,}28$. \ $A_T\approx240+332{,}55=\res{572{,}55\text{ cm}^2}$."),
 (2, T(r"Volem fer una caixa sense tapa de 30 cm × 20 cm de base i 15 cm d'altura. Quant cartó necessitem?", r"Queremos hacer una caja sin tapa de 30 cm × 20 cm de base y 15 cm de altura. ¿Cuánto cartón necesitamos?"),
     T(r"Base $30\cdot20=600$; \ cares laterals $2\cdot30\cdot15+2\cdot20\cdot15=1500$. \ Total: $\res{2100\text{ cm}^2}$ (només hi ha una base).", r"Base $30\cdot20=600$; \ caras laterales $2\cdot30\cdot15+2\cdot20\cdot15=1500$. \ Total: $\res{2100\text{ cm}^2}$ (solo hay una base).")),
 (3, T(r"Un cub té una àrea total de 216 cm². Quant mesura l'aresta? I la diagonal?", r"Un cubo tiene un área total de 216 cm². ¿Cuánto mide la arista? ¿Y la diagonal?"),
     r"$6l^2=216\Rightarrow l^2=36\Rightarrow\res{l=6\text{ cm}}$; \ $D=\sqrt{36+36+36}=\sqrt{108}\approx\res{10{,}39\text{ cm}}$."),
 (3, T(r"Volem pintar les quatre parets d'una habitació de 4 m × 3,5 m i 2,5 m d'altura. La porta fa 0,8 m × 2 m i la finestra 1,2 m × 1 m. Si pintar costa 4 € el metre quadrat, quant ens costarà?",
       r"Queremos pintar las cuatro paredes de una habitación de 4 m × 3,5 m y 2,5 m de altura. La puerta mide 0,8 m × 2 m y la ventana 1,2 m × 1 m. Si pintar cuesta 4 € el metro cuadrado, ¿cuánto nos costará?"),
     T(r"Parets: $2(4+3{,}5)\cdot2{,}5=37{,}5$ m²; \ llevem la porta i la finestra: $37{,}5-1{,}6-1{,}2=34{,}7$ m². \ Cost: $34{,}7\cdot4=\res{138{,}80\text{ €}}$.",
       r"Paredes: $2(4+3{,}5)\cdot2{,}5=37{,}5$ m²; \ quitamos la puerta y la ventana: $37{,}5-1{,}6-1{,}2=34{,}7$ m². \ Coste: $34{,}7\cdot4=\res{138{,}80\text{ €}}$.")),
]))

# =====================================================================
# 3. Piràmides: elements i àrea
# =====================================================================
ck(S(36 + 64), 10); ck(64 * 10 / 2 + 256, 576); ck(36 * 10 / 2, 180); ck(24 * 12 / 2, 144); ck(S(169 - 25), 12); ck(40 * 13 / 2 + 100, 360)
ck(S(16 + 9), 5); ck(S(25 + 9), 5.83, 2); ck(24 * 5 / 2, 60); ck(60 + 36, 96); ck(S(12), 3.46, 2); ck(8 * S(12), 27.71, 2)
ck(S(R(225, 100) + 1), 1.80, 2); ck(4 * S(R(325, 100)), 7.21, 2); ck(S(48), 6.93, 2); ck(12 * S(48), 83.14, 2); ck(12 * S(12), 41.57, 2); ck(12 * S(48) + 12 * S(12), 124.71, 2)
PYF = tz(f_pyramid(4, 3.6, 3.2, labs=(CM('16'), CM('6'), '', ''))[0], 0.6)
S_.append((T("Piràmides: elements i àrea", "Pirámides: elementos y área"), [
 (1, side(T(r"La piràmide quadrangular regular de la figura té 16 cm d'aresta de la base i 6 cm d'altura. Calcula'n l'apotema i l'àrea total.", r"La pirámide cuadrangular regular de la figura tiene 16 cm de arista de la base y 6 cm de altura. Calcula su apotema y su área total."), PYF, '0.32')
     + recorda(T(r"En una piràmide regular, l'altura $h$, l'apotema de la base $a_b$ i l'apotema de la piràmide $a_p$ formen un triangle rectangle: $a_p^2=h^2+a_b^2$. \ $A_L=\frac{P_{\text{base}}\cdot a_p}{2}$, \ $A_T=A_L+A_{\text{base}}$.",
                 r"En una pirámide regular, la altura $h$, la apotema de la base $a_b$ y la apotema de la pirámide $a_p$ forman un triángulo rectángulo: $a_p^2=h^2+a_b^2$. \ $A_L=\frac{P_{\text{base}}\cdot a_p}{2}$, \ $A_T=A_L+A_{\text{base}}$.")),
     r"$a_b=8$; \ $a_p=\sqrt{36+64}=\res{10\text{ cm}}$. \ $A_T=\frac{64\cdot10}{2}+16^2=320+256=\res{576\text{ cm}^2}$."),
 (1, T(r"Una piràmide hexagonal regular té 6 cm d'aresta de la base i 10 cm d'apotema. Calcula'n l'àrea lateral.", r"Una pirámide hexagonal regular tiene 6 cm de arista de la base y 10 cm de apotema. Calcula su área lateral."),
     r"$A_L=\frac{36\cdot10}{2}=\res{180\text{ cm}^2}$."),
 (1, T(r"Una piràmide triangular regular té 8 cm d'aresta de la base i 12 cm d'apotema. Calcula'n l'àrea lateral.", r"Una pirámide triangular regular tiene 8 cm de arista de la base y 12 cm de apotema. Calcula su área lateral."),
     r"$A_L=\frac{24\cdot12}{2}=\res{144\text{ cm}^2}$."),
 (2, T(r"Una piràmide quadrangular regular té 10 cm d'aresta de la base i 13 cm d'apotema. Calcula'n l'altura i l'àrea total.", r"Una pirámide cuadrangular regular tiene 10 cm de arista de la base y 13 cm de apotema. Calcula su altura y su área total."),
     r"$a_b=5$; \ $h=\sqrt{13^2-5^2}=\sqrt{144}=\res{12\text{ cm}}$. \ $A_T=\frac{40\cdot13}{2}+100=\res{360\text{ cm}^2}$."),
 (2, T(r"Una piràmide quadrangular regular té 6 cm d'aresta de la base i 4 cm d'altura. Calcula l'apotema, l'aresta lateral i l'àrea total.", r"Una pirámide cuadrangular regular tiene 6 cm de arista de la base y 4 cm de altura. Calcula la apotema, la arista lateral y el área total."),
     T(r"$a_p=\sqrt{16+9}=\res{5\text{ cm}}$. \ L'aresta lateral és la hipotenusa de l'apotema i mig costat: $\sqrt{25+9}=\sqrt{34}\approx\res{5{,}83\text{ cm}}$. \ $A_T=\frac{24\cdot5}{2}+36=\res{96\text{ cm}^2}$.",
       r"$a_p=\sqrt{16+9}=\res{5\text{ cm}}$. \ La arista lateral es la hipotenusa de la apotema y medio lado: $\sqrt{25+9}=\sqrt{34}\approx\res{5{,}83\text{ cm}}$. \ $A_T=\frac{24\cdot5}{2}+36=\res{96\text{ cm}^2}$.")),
 (2, T(r"Calcula l'àrea total d'un tetraedre regular de 4 cm d'aresta.", r"Calcula el área total de un tetraedro regular de 4 cm de arista."),
     T(r"Són 4 triangles equilàters. Altura de cada un: $\sqrt{16-4}=\sqrt{12}\approx3{,}46$. \ $A=4\cdot\frac{4\cdot\sqrt{12}}{2}=8\sqrt{12}\approx\res{27{,}71\text{ cm}^2}$.",
       r"Son 4 triángulos equiláteros. Altura de cada uno: $\sqrt{16-4}=\sqrt{12}\approx3{,}46$. \ $A=4\cdot\frac{4\cdot\sqrt{12}}{2}=8\sqrt{12}\approx\res{27{,}71\text{ cm}^2}$.")),
 (3, T(r"Una tenda de campanya té forma de piràmide quadrangular regular de 2 m de costat de la base i 1,5 m d'altura. Quanta lona cal per a fer-la, si no té terra?", r"Una tienda de campaña tiene forma de pirámide cuadrangular regular de 2 m de lado de la base y 1,5 m de altura. ¿Cuánta lona hace falta para hacerla, si no tiene suelo?"),
     T(r"$a_b=1$; \ $a_p=\sqrt{1{,}5^2+1^2}=\sqrt{3{,}25}\approx1{,}80$ m. \ Només l'àrea lateral: $A_L=\frac{8\cdot\sqrt{3{,}25}}{2}\approx\res{7{,}21\text{ m}^2}$.",
       r"$a_b=1$; \ $a_p=\sqrt{1{,}5^2+1^2}=\sqrt{3{,}25}\approx1{,}80$ m. \ Solo el área lateral: $A_L=\frac{8\cdot\sqrt{3{,}25}}{2}\approx\res{7{,}21\text{ m}^2}$.")),
 (3, T(r"Calcula l'àrea total d'una piràmide hexagonal regular de 4 cm d'aresta de la base i 6 cm d'altura.", r"Calcula el área total de una pirámide hexagonal regular de 4 cm de arista de la base y 6 cm de altura."),
     r"$a_b=\sqrt{16-4}=\sqrt{12}\approx3{,}46$; \ $a_p=\sqrt{36+12}=\sqrt{48}\approx6{,}93$. \ $A_L=\frac{24\cdot\sqrt{48}}{2}\approx83{,}14$; \ $A_{\text{base}}=\frac{24\cdot\sqrt{12}}{2}\approx41{,}57$. \ $A_T\approx\res{124{,}71\text{ cm}^2}$."),
]))

# =====================================================================
# 4. Cossos de revolució: cilindre i con
# =====================================================================
ck(48 * pi, 150.80, 2); ck(66 * pi, 207.35, 2); ck(60 * pi, 188.50, 2); ck(96 * pi, 301.59, 2); ck(S(64 + 225), 17); ck(200 * pi, 628.32, 2)
ck(88 * pi, 276.46, 2); ck(S(625 - 49), 24); ck(R(31416, 100) / (20 * pi), 5, 2); ck(150 * pi, 471.24, 2); ck(63 * pi, 197.92, 2); ck(10000 / (63 * pi), 50.5, 1)
CYL = tz(f_cylinder(1.5, 4, lr=CM('3'), lh=CM('8'))[0], 0.45)
S_.append((T("Cossos de revolució: cilindre i con", "Cuerpos de revolución: cilindro y cono"), [
 (1, T(r"Quin cos de revolució s'obté en fer girar:", r"¿Qué cuerpo de revolución se obtiene al hacer girar:")
     + tasks(1, [T(r"un rectangle al voltant d'un costat?", r"un rectángulo alrededor de un lado?"), T(r"un triangle rectangle al voltant d'un catet?", r"un triángulo rectángulo alrededor de un cateto?"),
                 T(r"un semicercle al voltant del diàmetre?", r"un semicírculo alrededor del diámetro?"), T(r"un triangle rectangle al voltant de la hipotenusa?", r"un triángulo rectángulo alrededor de la hipotenusa?")]),
     tasks(2, [r"\rest{%s}" % T("cilindre", "cilindro"), r"\rest{%s}" % T("con", "cono"), r"\rest{%s}" % T("esfera", "esfera"), T(r"\rest{dos cons} units per la base", r"\rest{dos conos} unidos por la base")])),
 (1, side(T(r"Calcula l'àrea lateral i l'àrea total del cilindre de la figura, de 3 cm de radi i 8 cm d'altura.", r"Calcula el área lateral y el área total del cilindro de la figura, de 3 cm de radio y 8 cm de altura."), CYL, '0.26')
     + recorda(T(r"Cilindre: $A_L=2\pi r h$, \ $A_T=2\pi r h+2\pi r^2$. \ Con: $A_L=\pi r g$, \ $A_T=\pi r g+\pi r^2$, on la generatriu compleix $g^2=h^2+r^2$.",
                 r"Cilindro: $A_L=2\pi r h$, \ $A_T=2\pi r h+2\pi r^2$. \ Cono: $A_L=\pi r g$, \ $A_T=\pi r g+\pi r^2$, donde la generatriz cumple $g^2=h^2+r^2$.")),
     r"$A_L=2\pi\cdot3\cdot8=48\pi\approx\res{150{,}80\text{ cm}^2}$; \ $A_T=48\pi+18\pi=66\pi\approx\res{207{,}35\text{ cm}^2}$."),
 (1, T(r"Un con té 6 cm de radi i 10 cm de generatriu. Calcula'n l'àrea lateral i l'àrea total.", r"Un cono tiene 6 cm de radio y 10 cm de generatriz. Calcula su área lateral y su área total."),
     r"$A_L=\pi\cdot6\cdot10=60\pi\approx\res{188{,}50\text{ cm}^2}$; \ $A_T=60\pi+36\pi=96\pi\approx\res{301{,}59\text{ cm}^2}$."),
 (2, T(r"Un con té 16 cm de diàmetre i 15 cm d'altura. Calcula la generatriu i l'àrea total.", r"Un cono tiene 16 cm de diámetro y 15 cm de altura. Calcula la generatriz y el área total."),
     r"$r=8$; \ $g=\sqrt{225+64}=\sqrt{289}=\res{17\text{ cm}}$. \ $A_T=136\pi+64\pi=200\pi\approx\res{628{,}32\text{ cm}^2}$."),
 (2, T(r"L'etiqueta d'una llanda cilíndrica de 8 cm de diàmetre i 11 cm d'altura cobreix tota la superfície lateral. Quina àrea té?", r"La etiqueta de una lata cilíndrica de 8 cm de diámetro y 11 cm de altura cubre toda la superficie lateral. ¿Qué área tiene?"),
     r"$A_L=2\pi\cdot4\cdot11=88\pi\approx\res{276{,}46\text{ cm}^2}$."),
 (2, T(r"Un con té 25 cm de generatriu i 7 cm de radi. Quina altura té?", r"Un cono tiene 25 cm de generatriz y 7 cm de radio. ¿Qué altura tiene?"),
     r"$h=\sqrt{25^2-7^2}=\sqrt{576}=\res{24\text{ cm}}$."),
 (3, T(r"Un cilindre de 10 cm d'altura té una àrea lateral de 314,16 cm². Quin radi té? Calcula'n l'àrea total.", r"Un cilindro de 10 cm de altura tiene un área lateral de 314,16 cm². ¿Qué radio tiene? Calcula su área total."),
     r"$2\pi r\cdot10=314{,}16\Rightarrow r=\frac{314{,}16}{20\pi}\approx\res{5\text{ cm}}$. \ $A_T=100\pi+50\pi=150\pi\approx\res{471{,}24\text{ cm}^2}$."),
 (3, T(r"Volem fer gots cilíndrics de cartolina, sense tapa, de 3 cm de radi i 9 cm d'altura. Quanta cartolina cal per a cada got? Quants gots, com a màxim, podríem fer amb 1 m² de cartolina (sense comptar el que es perd en retallar)?",
       r"Queremos hacer vasos cilíndricos de cartulina, sin tapa, de 3 cm de radio y 9 cm de altura. ¿Cuánta cartulina hace falta para cada vaso? ¿Cuántos vasos, como máximo, podríamos hacer con 1 m² de cartulina (sin contar lo que se pierde al recortar)?"),
     T(r"Un got té la superfície lateral i un sol cercle: $54\pi+9\pi=63\pi\approx\res{197{,}92\text{ cm}^2}$. \ 1 m² = 10\,000 cm²: $\frac{10\,000}{197{,}92}\approx50{,}5\Rightarrow\res{50\text{ gots}}$.",
       r"Un vaso tiene la superficie lateral y un solo círculo: $54\pi+9\pi=63\pi\approx\res{197{,}92\text{ cm}^2}$. \ 1 m² = 10\,000 cm²: $\frac{10\,000}{197{,}92}\approx50{,}5\Rightarrow\res{50\text{ vasos}}$.")),
]))

# =====================================================================
# 5. L'esfera i la seua àrea
# =====================================================================
ck(196 * pi, 615.75, 2); ck(100 * pi, 314.16, 2); ck(R(4225, 100) * pi, 132.73, 2); ck(72 * pi, 226.19, 2); ck(50 / (2 * pi), 7.96, 2); ck(2500 / pi, 795.77, 2)
ck(100 * pi / 600 * 100, 52.36, 2); ck(2 * pi * 4 * 8, 64 * pi); ck(R(64, 96), R(2, 3))
S_.append((T("L'esfera i la seua àrea", "La esfera y su área"), [
 (1, T(r"Calcula l'àrea de:", r"Calcula el área de:") + tasks(2, [T(r"una esfera de 7 cm de radi;", r"una esfera de 7 cm de radio;"), T(r"una esfera de 10 cm de diàmetre.", r"una esfera de 10 cm de diámetro.")])
     + recorda(T(r"L'àrea de l'esfera és la de quatre cercles màxims: $A=4\pi r^2$. Compte: si et donen el diàmetre, el radi n'és la meitat.", r"El área de la esfera es la de cuatro círculos máximos: $A=4\pi r^2$. Cuidado: si te dan el diámetro, el radio es la mitad.")),
     tasks(2, [r"$4\pi\cdot49=196\pi\approx\res{615{,}75\text{ cm}^2}$", r"$r=5$: \ $4\pi\cdot25=100\pi\approx\res{314{,}16\text{ cm}^2}$"])),
 (1, T(r"Una esfera té una àrea de $36\pi$ cm². Quin radi té?", r"Una esfera tiene un área de $36\pi$ cm². ¿Qué radio tiene?"),
     r"$4\pi r^2=36\pi\Rightarrow r^2=9\Rightarrow\res{r=3\text{ cm}}$."),
 (2, T(r"Una pilota de tennis fa 6,5 cm de diàmetre. Quanta superfície té?", r"Una pelota de tenis mide 6,5 cm de diámetro. ¿Cuánta superficie tiene?"),
     r"$r=3{,}25$: \ $A=4\pi\cdot3{,}25^2=42{,}25\pi\approx\res{132{,}73\text{ cm}^2}$."),
 (2, T(r"Volem pintar per fora una cúpula semiesfèrica de 6 m de radi. Quina superfície hem de pintar?", r"Queremos pintar por fuera una cúpula semiesférica de 6 m de radio. ¿Qué superficie tenemos que pintar?"),
     T(r"La meitat de l'esfera: $\frac{4\pi\cdot36}{2}=72\pi\approx\res{226{,}19\text{ m}^2}$.", r"La mitad de la esfera: $\frac{4\pi\cdot36}{2}=72\pi\approx\res{226{,}19\text{ m}^2}$.")),
 (2, T(r"La circumferència màxima d'una pilota fa 50 cm. Calcula'n el radi i l'àrea.", r"La circunferencia máxima de un balón mide 50 cm. Calcula su radio y su área."),
     r"$2\pi r=50\Rightarrow r=\frac{50}{2\pi}\approx\res{7{,}96\text{ cm}}$; \ $A=4\pi r^2=\frac{2500}{\pi}\approx\res{795{,}77\text{ cm}^2}$."),
 (3, T(r"Una esfera està ficada dins d'un cub de 10 cm d'aresta i toca totes les cares. Quina és l'àrea de l'esfera? Quin percentatge representa de l'àrea del cub?", r"Una esfera está metida dentro de un cubo de 10 cm de arista y toca todas las caras. ¿Cuál es el área de la esfera? ¿Qué porcentaje representa del área del cubo?"),
     r"$r=5$: \ $A=100\pi\approx\res{314{,}16\text{ cm}^2}$. \ $A_{\text{" + T("cub", "cubo") + r"}}=600$: \ $\frac{314{,}16}{600}\cdot100\approx\res{52{,}36\,\%}$."),
 (3, T(r"Una esfera de 4 cm de radi està ficada en un cilindre que l'envolta exactament (radi 4 cm i altura 8 cm). Comprova que l'àrea de l'esfera és igual a l'àrea lateral del cilindre. Quina fracció de l'àrea total del cilindre representa?",
       r"Una esfera de 4 cm de radio está metida en un cilindro que la envuelve exactamente (radio 4 cm y altura 8 cm). Comprueba que el área de la esfera es igual al área lateral del cilindro. ¿Qué fracción del área total del cilindro representa?"),
     r"$A_{\text{" + T("esfera", "esfera") + r"}}=4\pi\cdot16=64\pi$; \ $A_L=2\pi\cdot4\cdot8=64\pi$ \ \checkmark. \ $A_T=64\pi+32\pi=96\pi$: \ $\frac{64\pi}{96\pi}=\res{\tfrac23}$ " + T("(descobriment d'Arquimedes).", "(descubrimiento de Arquímedes).")),
]))

# =====================================================================
# 6. Volum. Prismes i cilindres
# =====================================================================
ck(6 ** 3, 216); ck(10 * 4 * 5, 200); ck(40 * pi, 125.66, 2); ck(6 * 20, 120); ck(60 * 30 * 40, 72000); ck(60 * 30 * 35, 63000)
ck(3 * pi, 9.42, 2); ck(3000 * pi, 9425, 0); ck(S(3), 1.73, 2); ck(6 * S(3), 10.39, 2); ck(60 * S(3), 103.92, 2); ck(R(1000, 57), 17.54, 2)
S_.append((T("Volum. Prismes i cilindres", "Volumen. Prismas y cilindros"), [
 (1, T(r"Expressa en la unitat que s'indica:", r"Expresa en la unidad que se indica:")
     + tasks(3, [r"5 m³ \ " + T("en", "en") + r" dm³", r"2,5 dm³ \ " + T("en", "en") + r" cm³", r"7500 cm³ \ " + T("en", "en") + r" dm³", r"0,35 m³ \ " + T("en litres", "en litros"), r"3 L \ " + T("en", "en") + r" cm³", r"250 mL \ " + T("en", "en") + r" dm³"])
     + recorda(T(r"Cada unitat de volum és 1000 vegades la següent: 1 m³ = 1000 dm³, 1 dm³ = 1000 cm³. \ I la clau de la capacitat: 1 dm³ = 1 L, \ 1 cm³ = 1 mL, \ 1 m³ = 1000 L.",
                 r"Cada unidad de volumen es 1000 veces la siguiente: 1 m³ = 1000 dm³, 1 dm³ = 1000 cm³. \ Y la clave de la capacidad: 1 dm³ = 1 L, \ 1 cm³ = 1 mL, \ 1 m³ = 1000 L.")),
     tasks(3, [r"\rest{5000 dm³}", r"\rest{2500 cm³}", r"\rest{7,5 dm³}", r"\rest{350 L}", r"\rest{3000 cm³}", r"\rest{0,25 dm³}"])),
 (1, T(r"Calcula el volum d'un cub de 6 cm d'aresta i el d'un ortoedre de 10 cm × 4 cm × 5 cm.", r"Calcula el volumen de un cubo de 6 cm de arista y el de un ortoedro de 10 cm × 4 cm × 5 cm."),
     r"$6^3=\res{216\text{ cm}^3}$; \ $10\cdot4\cdot5=\res{200\text{ cm}^3}$."),
 (1, T(r"Calcula el volum d'un cilindre de 2 cm de radi i 10 cm d'altura.", r"Calcula el volumen de un cilindro de 2 cm de radio y 10 cm de altura."),
     r"$V=\pi\cdot2^2\cdot10=40\pi\approx\res{125{,}66\text{ cm}^3}$."),
 (2, T(r"Un prisma té de base un triangle rectangle de catets 3 cm i 4 cm, i 20 cm d'altura. Quin volum té?", r"Un prisma tiene de base un triángulo rectángulo de catetos 3 cm y 4 cm, y 20 cm de altura. ¿Qué volumen tiene?"),
     r"$A_{\text{base}}=\frac{3\cdot4}{2}=6$; \ $V=6\cdot20=\res{120\text{ cm}^3}$."),
 (2, T(r"Un aquari fa 60 cm de llarg, 30 cm d'ample i 40 cm d'alt. Quants litres hi caben? Quants n'hi posem si l'omplim fins a 35 cm d'altura?", r"Un acuario mide 60 cm de largo, 30 cm de ancho y 40 cm de alto. ¿Cuántos litros caben? ¿Cuántos ponemos si lo llenamos hasta 35 cm de altura?"),
     r"$60\cdot30\cdot40=72\,000\text{ cm}^3=\res{72\text{ L}}$; \ $60\cdot30\cdot35=63\,000\text{ cm}^3=\res{63\text{ L}}$."),
 (2, T(r"Un dipòsit cilíndric té 1 m de radi i 3 m d'altura. Quants litres d'aigua hi caben?", r"Un depósito cilíndrico tiene 1 m de radio y 3 m de altura. ¿Cuántos litros de agua caben?"),
     r"$V=\pi\cdot1^2\cdot3=3\pi\approx9{,}42\text{ m}^3\approx\res{9425\text{ L}}$."),
 (3, T(r"Calcula el volum d'un prisma hexagonal regular de 2 cm d'aresta de la base i 10 cm d'altura.", r"Calcula el volumen de un prisma hexagonal regular de 2 cm de arista de la base y 10 cm de altura."),
     r"$a_b=\sqrt{4-1}=\sqrt3\approx1{,}73$; \ $A_{\text{base}}=\frac{12\cdot\sqrt3}{2}=6\sqrt3\approx10{,}39$. \ $V=60\sqrt3\approx\res{103{,}92\text{ cm}^3}$."),
 (3, T(r"Un tetrabric d'1 L de llet té una base rectangular de 6 cm × 9,5 cm. Quina altura ha de tenir com a mínim?", r"Un tetrabrik de 1 L de leche tiene una base rectangular de 6 cm × 9,5 cm. ¿Qué altura debe tener como mínimo?"),
     r"1 L = 1000 cm³: \ $6\cdot9{,}5\cdot h=1000\Rightarrow h=\frac{1000}{57}\approx\res{17{,}54\text{ cm}}$."),
]))

# =====================================================================
# 7. Volum de piràmides, cons i esferes
# =====================================================================
ck(R(81 * 10, 3), 270); ck(R(16 * 9, 3) * pi, 48 * pi); ck(48 * pi, 150.80, 2); ck(36 * pi, 113.10, 2); ck(R(4000, 3) * pi, 4188.79, 2)
ck(S(225 - 81), 12); ck(324 * pi, 1017.88, 2); ck(S(25 - 16), 3); ck(R(64 * 3, 3), 64); ck(2304 * pi, 7238.23, 2); ck(R(4, 3) * 216, 288); ck(144 * pi, 452.39, 2); ck(R(36, 54), R(2, 3))
S_.append((T("Volum de piràmides, cons i esferes", "Volumen de pirámides, conos y esferas"), [
 (1, T(r"Calcula el volum d'una piràmide quadrangular de 9 cm d'aresta de la base i 10 cm d'altura.", r"Calcula el volumen de una pirámide cuadrangular de 9 cm de arista de la base y 10 cm de altura.")
     + recorda(T(r"$V_{\text{piràmide}}=\frac{A_{\text{base}}\cdot h}{3}$, \ $V_{\text{con}}=\frac{\pi r^2h}{3}$ (un terç del prisma o del cilindre de la mateixa base i altura), \ $V_{\text{esfera}}=\frac43\pi r^3$.",
                 r"$V_{\text{pirámide}}=\frac{A_{\text{base}}\cdot h}{3}$, \ $V_{\text{cono}}=\frac{\pi r^2h}{3}$ (un tercio del prisma o del cilindro de la misma base y altura), \ $V_{\text{esfera}}=\frac43\pi r^3$.")),
     r"$V=\frac{81\cdot10}{3}=\res{270\text{ cm}^3}$."),
 (1, T(r"Calcula el volum d'un con de 4 cm de radi i 9 cm d'altura.", r"Calcula el volumen de un cono de 4 cm de radio y 9 cm de altura."),
     r"$V=\frac{\pi\cdot16\cdot9}{3}=48\pi\approx\res{150{,}80\text{ cm}^3}$."),
 (1, T(r"Calcula el volum d'una esfera de 3 cm de radi i el d'una de 10 cm de radi.", r"Calcula el volumen de una esfera de 3 cm de radio y el de una de 10 cm de radio."),
     r"$\frac43\pi\cdot27=36\pi\approx\res{113{,}10\text{ cm}^3}$; \ $\frac43\pi\cdot1000=\frac{4000\pi}{3}\approx\res{4188{,}79\text{ cm}^3}$."),
 (2, T(r"Un con té 15 cm de generatriu i 9 cm de radi. Calcula'n l'altura i el volum.", r"Un cono tiene 15 cm de generatriz y 9 cm de radio. Calcula su altura y su volumen."),
     r"$h=\sqrt{225-81}=\res{12\text{ cm}}$; \ $V=\frac{\pi\cdot81\cdot12}{3}=324\pi\approx\res{1017{,}88\text{ cm}^3}$."),
 (2, T(r"Una piràmide quadrangular regular té 8 cm d'aresta de la base i 5 cm d'apotema. Calcula'n l'altura i el volum.", r"Una pirámide cuadrangular regular tiene 8 cm de arista de la base y 5 cm de apotema. Calcula su altura y su volumen."),
     r"$a_b=4$; \ $h=\sqrt{25-16}=\res{3\text{ cm}}$; \ $V=\frac{64\cdot3}{3}=\res{64\text{ cm}^3}$."),
 (2, T(r"Una pilota de bàsquet fa 24 cm de diàmetre. Quants litres d'aire conté?", r"Un balón de baloncesto mide 24 cm de diámetro. ¿Cuántos litros de aire contiene?"),
     r"$r=12$: \ $V=\frac43\pi\cdot1728=2304\pi\approx7238{,}23\text{ cm}^3\approx\res{7{,}24\text{ L}}$."),
 (3, T(r"Una esfera té un volum de $288\pi$ cm³. Quin radi té? Calcula'n l'àrea.", r"Una esfera tiene un volumen de $288\pi$ cm³. ¿Qué radio tiene? Calcula su área."),
     r"$\frac43r^3=288\Rightarrow r^3=216\Rightarrow\res{r=6\text{ cm}}$; \ $A=4\pi\cdot36=144\pi\approx\res{452{,}39\text{ cm}^2}$."),
 (3, T(r"Un cilindre de 3 cm de radi i 6 cm d'altura està ple d'aigua. Hi fiquem una esfera de 3 cm de radi (que hi cap justa). Quina fracció de l'aigua vessa?", r"Un cilindro de 3 cm de radio y 6 cm de altura está lleno de agua. Metemos una esfera de 3 cm de radio (que cabe justa). ¿Qué fracción del agua se derrama?"),
     T(r"$V_{\text{cil}}=\pi\cdot9\cdot6=54\pi$; \ $V_{\text{esfera}}=\frac43\pi\cdot27=36\pi$. \ Vessa $\frac{36\pi}{54\pi}=\res{\tfrac23}$ de l'aigua.", r"$V_{\text{cil}}=\pi\cdot9\cdot6=54\pi$; \ $V_{\text{esfera}}=\frac43\pi\cdot27=36\pi$. \ Se derrama $\frac{36\pi}{54\pi}=\res{\tfrac23}$ del agua.")),
]))

# =====================================================================
# 8. Cossos compostos i problemes
# =====================================================================
ck(125 + R(25 * 6, 3), 175); ck(36 * pi + 18 * pi, 54 * pi); ck(54 * pi, 169.65, 2); ck(72 * pi + 12 * pi, 84 * pi); ck(84 * pi, 263.89, 2); ck(2200 * pi, 6911.50, 2)
ck(1728 - 48 * pi, 1577.20, 2); ck(250 + 2 * 35 * 2, 390); ck(25 * 10 * 2, 500); ck(R(500000, 400), 1250); ck(R(1250, 60), 20.83, 2)
ck(2 * pi * R(325, 100) ** 3, 215.69, 2); ck(R(20, 3) / 16, R(5, 12)); ck(10 + R(5, 12), 10.42, 2)
TORRE, _ = polyhedron(cuboid(5, 5, 5) + [(2.5, 2.5, 11)])
TORRE = tz(TORRE, 0.3)
S_.append((T("Cossos compostos i problemes", "Cuerpos compuestos y problemas"), [
 (1, side(T(r"La peça de la figura és un cub de 5 cm d'aresta amb una piràmide de 6 cm d'altura al damunt. Calcula'n el volum.", r"La pieza de la figura es un cubo de 5 cm de arista con una pirámide de 6 cm de altura encima. Calcula su volumen."), TORRE, '0.2')
     + recorda(T(r"Per a calcular el volum d'un cos compost, el descomponem en cossos simples i sumem els volums (o els restem, si hi ha forats). Per a l'àrea, només sumem les superfícies que queden per fora.",
                 r"Para calcular el volumen de un cuerpo compuesto, lo descomponemos en cuerpos simples y sumamos los volúmenes (o los restamos, si hay agujeros). Para el área, solo sumamos las superficies que quedan por fuera.")),
     r"$V=5^3+\frac{25\cdot6}{3}=125+50=\res{175\text{ cm}^3}$."),
 (2, T(r"Un gelat és un con de 3 cm de radi i 12 cm d'altura, ple de gelat, amb una semiesfera de gelat al damunt. Quant de gelat hi ha?", r"Un helado es un cono de 3 cm de radio y 12 cm de altura, lleno de helado, con una semiesfera de helado encima. ¿Cuánto helado hay?"),
     r"$V=\frac{\pi\cdot9\cdot12}{3}+\frac12\cdot\frac43\pi\cdot27=36\pi+18\pi=54\pi\approx\res{169{,}65\text{ cm}^3}$."),
 (2, T(r"Una sitja és un cilindre de 3 m de radi i 8 m d'altura amb una teulada cònica de 4 m d'altura. Quin volum té?", r"Un silo es un cilindro de 3 m de radio y 8 m de altura con un tejado cónico de 4 m de altura. ¿Qué volumen tiene?"),
     r"$V=\pi\cdot9\cdot8+\frac{\pi\cdot9\cdot4}{3}=72\pi+12\pi=84\pi\approx\res{263{,}89\text{ m}^3}$."),
 (2, T(r"Un tub de 2 m de llarg té 6 cm de radi exterior i 5 cm de radi interior. Quin volum de material té?", r"Un tubo de 2 m de largo tiene 6 cm de radio exterior y 5 cm de radio interior. ¿Qué volumen de material tiene?"),
     r"$V=\pi(6^2-5^2)\cdot200=2200\pi\approx\res{6911{,}50\text{ cm}^3}$."),
 (2, T(r"Un cub de 12 cm d'aresta té un forat cilíndric de 2 cm de radi que el travessa de banda a banda. Quin volum té?", r"Un cubo de 12 cm de arista tiene un agujero cilíndrico de 2 cm de radio que lo atraviesa de lado a lado. ¿Qué volumen tiene?"),
     r"$V=12^3-\pi\cdot4\cdot12=1728-48\pi\approx\res{1577{,}20\text{ cm}^3}$."),
 (3, T(r"Una piscina fa 25 m de llarg, 10 m d'ample i 2 m de fondària. a) Quants metres quadrats de rajoles calen per a cobrir el fons i les parets? b) Quants litres d'aigua hi caben? c) Quant de temps tardarà a omplir-se amb una bomba que aboca 400 L per minut?",
       r"Una piscina mide 25 m de largo, 10 m de ancho y 2 m de profundidad. a) ¿Cuántos metros cuadrados de baldosas hacen falta para cubrir el fondo y las paredes? b) ¿Cuántos litros de agua caben? c) ¿Cuánto tardará en llenarse con una bomba que echa 400 L por minuto?"),
     T(r"a) $25\cdot10+2(25+10)\cdot2=250+140=\res{390\text{ m}^2}$. \ b) $25\cdot10\cdot2=500\text{ m}^3=\res{500\,000\text{ L}}$. \ c) $\frac{500\,000}{400}=1250$ min $\approx\res{20{,}83\text{ hores}}$ (20 h 50 min).",
       r"a) $25\cdot10+2(25+10)\cdot2=250+140=\res{390\text{ m}^2}$. \ b) $25\cdot10\cdot2=500\text{ m}^3=\res{500\,000\text{ L}}$. \ c) $\frac{500\,000}{400}=1250$ min $\approx\res{20{,}83\text{ horas}}$ (20 h 50 min).")),
 (3, T(r"Tres pilotes de tennis de 3,25 cm de radi es venen en un tub cilíndric on caben justes (radi 3,25 cm i altura 19,5 cm). Quina fracció del tub ocupen les pilotes? Quin volum queda buit?",
       r"Tres pelotas de tenis de 3,25 cm de radio se venden en un tubo cilíndrico en el que caben justas (radio 3,25 cm y altura 19,5 cm). ¿Qué fracción del tubo ocupan las pelotas? ¿Qué volumen queda vacío?"),
     T(r"Amb $r=3{,}25$ i $h=6r$: \ $V_{\text{tub}}=\pi r^2\cdot6r=6\pi r^3$; \ $V_{\text{pilotes}}=3\cdot\frac43\pi r^3=4\pi r^3$. \ Ocupen $\res{\tfrac46=\tfrac23}$ del tub. \ Buit: $2\pi r^3=2\pi\cdot3{,}25^3\approx\res{215{,}69\text{ cm}^3}$.",
       r"Con $r=3{,}25$ y $h=6r$: \ $V_{\text{tubo}}=\pi r^2\cdot6r=6\pi r^3$; \ $V_{\text{pelotas}}=3\cdot\frac43\pi r^3=4\pi r^3$. \ Ocupan $\res{\tfrac46=\tfrac23}$ del tubo. \ Vacío: $2\pi r^3=2\pi\cdot3{,}25^3\approx\res{215{,}69\text{ cm}^3}$.")),
 (3, T(r"Un got cilíndric de 4 cm de radi té aigua fins a 10 cm d'altura. Hi tirem 5 boles d'1 cm de radi, que queden cobertes. Fins a quina altura arriba ara l'aigua?", r"Un vaso cilíndrico de 4 cm de radio tiene agua hasta 10 cm de altura. Echamos 5 bolas de 1 cm de radio, que quedan cubiertas. ¿Hasta qué altura llega ahora el agua?"),
     T(r"Volum de les boles: $5\cdot\frac43\pi=\frac{20\pi}{3}$. \ L'aigua puja $h$: \ $16\pi h=\frac{20\pi}{3}\Rightarrow h=\frac{5}{12}\approx0{,}42$ cm. \ Arriba a $\res{10{,}42\text{ cm}}$.",
       r"Volumen de las bolas: $5\cdot\frac43\pi=\frac{20\pi}{3}$. \ El agua sube $h$: \ $16\pi h=\frac{20\pi}{3}\Rightarrow h=\frac{5}{12}\approx0{,}42$ cm. \ Llega a $\res{10{,}42\text{ cm}}$.")),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("poliedres, fórmula d'Euler, poliedres regulars, prisma, piràmide, cilindre, con, esfera, àrea, volum, capacitat",
       'poliedros, fórmula de Euler, poliedros regulares, prisma, pirámide, cilindro, cono, esfera, área, volumen, capacidad')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\usepackage{pifont}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T('Cossos geomètrics. Àrees i volums', 'Cuerpos geométricos. Áreas y volúmenes')
TITC = TIT.replace('. ', '.\\\\ ')  # a la capçalera, en dues línies

def build(sol_):
    if ES:
        sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 9: %s' % (t, TIT), capcalera='%s · Unidad 9: %s' % (t, TIT), pdfkeywords=KW, curs='2eso')
        cap = assignatura('2eso') + '{' + ('Soluciones de la ficha · Unidad 9' if sol_ else 'Ficha de ejercicios · Unidad 9') + '}{' + TITC + '}'
    else:
        t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat 9: %s. 2n d'ESO}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 9: %s · 2n d'ESO" % (t, TIT))
        assert "2n d'ESO" in p and 'Unitat 9' in p and 'unitat 9' in p
        cap = r'\capcalera{Matemàtiques}{2n ESO}{' + ('Solucions de la fitxa · Unitat 9' if sol_ else "Fitxa d'exercicis · Unitat 9") + '}{' + TITC + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol_ else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{14}\n\\input{../comu/fentmates.tex}\n\\fmcurs{2eso}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol_:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs cossos que pots girar i eines que calculen àrees i volums pas a pas. Els resultats aproximats estan arrodonits a les centèsimes.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás cuerpos que puedes girar y herramientas que calculan áreas y volúmenes paso a paso. Los resultados aproximados están redondeados a las centésimas.")
             if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i fes un dibuix de cada cos. Si un resultat no és exacte, arrodoneix-lo a les centèsimes i fes servir la tecla $\pi$ de la calculadora.",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y haz un dibujo de cada cuerpo. Si un resultado no es exacto, redondéalo a las centésimas y usa la tecla $\pi$ de la calculadora."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            out.append('\\ex{%d} %s\n\n' % (st, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.", "¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't9-fitxa-%s%s.tex' % ('solucions' if sol_ else 'exercicis', '-es' if ES else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(x[1]) for x in S_), T('exercicis', 'ejercicios'))
