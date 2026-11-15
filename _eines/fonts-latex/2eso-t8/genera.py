# Genera t8-fitxa-exercicis.tex i t8-fitxa-solucions.tex (2n ESO, Unitat 8: Semblança. Teorema de Tales)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 5 seccions segueixen els apartats dels apunts (8.1-8.5).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Cada resultat numèric es comprova amb ck(valor exacte, valor escrit, decimals de l'arrodoniment).
# Les figures es dibuixen amb la geometria de ../../apunts/2eso-t8/fig8.py (la mateixa que als apunts) i el traductor a
# TikZ tz() de ../3eso-t10/genera.py.
# Ús: python3 genera.py && pdflatex t8-fitxa-exercicis.tex (dues vegades) && pdflatex t8-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '2eso-t8'))
from fig8 import tales, tpos, shadow
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- comprovacions ----------
S, R = sp.sqrt, sp.Rational
def Q(v): return sp.nsimplify(v, rational=True) if isinstance(v, float) else sp.nsimplify(v)
def ck(v, w, d=None):
    """v: valor exacte; w: el que escrivim (nombre o text amb coma); d: decimals de l'arrodoniment (None = exacte)"""
    w = float(w.replace(',', '.')) if isinstance(w, str) else w
    if d is None: assert sp.simplify(Q(v) - Q(w)) == 0, (v, w)
    else: assert abs(float(v) - float(w)) <= 0.5 * 10 ** -d + 1e-9, (v, float(v), w, d)
def prop(a, b, c, d):
    """a/b = c/d (amb valors exactes)"""
    return Q(a) * Q(d) == Q(b) * Q(c)
def sim(s1, s2):
    a, b = sorted(map(Q, s1)), sorted(map(Q, s2))
    r = [y / x for x, y in zip(a, b)]
    return r[0] if r[0] == r[1] == r[2] else None
x = sp.Symbol('x')

# ---------- figures (TikZ) ----------
ST = {'gf': 'fill=teal!12,draw=teal,thick', 'tr': 'fill=accent!22,draw=accent,thick', 'water': 'fill=teal!14,draw=none',
      'par': 'draw=navy,thick', 'tv': 'thick', 'hl': 'draw=accent,line width=1.6pt', 'hl2': 'draw=teal,line width=1.6pt',
      'ray': 'dashed,draw=muted', 'axis': 'muted', 'wall': 'line width=2pt,draw=muted', 'ang': 'draw=navy', 'gl': 'draw=muted,thin', '': 'thick'}
def P_(p): return '(%.3f,%.3f)' % (float(p[0]), float(p[1]))
def labtex(t):
    t = t.replace('′', "'")
    if re.fullmatch(r"[A-Za-z]'*", t): return '$%s$' % t
    m = re.fullmatch(r"([\d,]+)( ?m| ?cm)?", t)
    if m: return '$%s$%s' % (m.group(1).replace(',', '{,}'), ('\\,' + m.group(2).strip()) if m.group(2) else '')
    return t
def tz(items, s=0.5):
    """dibuixa en TikZ una llista d'elements en el format de G() dels apunts (poly, seg, ra, dot, txt, arc)"""
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
        elif k == 'dot': o.append(r'\fill %s circle (%spt);' % (P_(it[1]), 1.1 if len(it) > 2 and it[2] == 'sm' else 1.5))
        elif k == 'arc':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]; A0 = (C[0] + r * math.cos(math.radians(a0)), C[1] + r * math.sin(math.radians(a0)))
            o.append(r'\draw[%s] %s arc[start angle=%s,end angle=%s,radius=%s];' % (ST.get(it[5] if len(it) > 5 else '', 'thick'), P_(A0), a0, a1, r))
        elif k == 'txt':
            op = it[3] if len(it) > 3 else {}
            if not it[2] or op.get('cls') in ('tv', 'par'): continue
            dx, dy, a = op.get('dx', 0), op.get('dy', 4), op.get('a', 'middle')
            anc = []
            if dy >= 12: anc.append('below')
            elif dy <= -4: anc.append('above')
            if a == 'end' or dx < -3: anc.append('left')
            elif a == 'start' or dx > 3: anc.append('right')
            st = ('font=\\small,inner sep=2pt' + (',' + ' '.join(anc) if anc else '') + (',text=accent' if op.get('cls') == 'hot' else ''))
            o.append(r'\node[%s] at %s {%s};' % (st, P_(it[1]), labtex(it[2])))
        elif k == 'lab': o.append(r'\node[font=\small,%s] at %s {%s};' % (it[3] if len(it) > 3 else 'inner sep=1pt', P_(it[1]), it[2]))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def fig(*f): return r'\par\smallskip\begin{center}' + r'\qquad '.join(f) + r'\end{center}'

SI, NO = T('sí', 'sí'), T('no', 'no')
I_ = T('i', 'y')
S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Figures semblants
# =====================================================================
ck(R(10, 4), 2.5); ck(R(15, 6), 2.5); ck(R(15, 10) / 3, 0.5); ck(R(2, 4), 0.5); ck(R(25, 10) / 5, 0.5)
ck(5 * 3, 15); ck(7 * 3, 21); ck(9 * 3, 27); ck(5 * R(2, 5), 2); ck(7 * R(2, 5), 2.8); ck(9 * R(2, 5), 3.6)
ck(R(4, 6), R(2, 3)); ck(9 * R(2, 3), 6)
ck(R(6, 4), 1.5); ck(1 * R(3, 2), 1.5); ck(2 * R(3, 2), 3)
assert sim([4, 10, 4], [6, 15, 6]) == R(3, 2) and R(10, 5) != R(18, 8)
ck(24 * R(5, 2), 60); ck(32 * R(5, 2) ** 2, 200)
ck(6 * R(1, 3), 2); ck(36, 6 ** 2); ck(2 ** 2, 4); ck(R(36, 4), 9)
ck(R(72, 24), 3); assert [6 * 3, 8 * 3, 10 * 3] == [18, 24, 30]
ck(S(9), 3); ck(S(81), 9); ck(R(9, 3), 3)
ck(10 * 15, 150); ck(R(600, 150), 4); ck(S(4), 2); assert (20, 30) == (10 * 2, 15 * 2) and 20 * 30 == 600
ck(S(3 ** 2 + 4 ** 2), 5); ck(R(15, 5), 3); ck(R(9 * 12, 2), 54); ck(R(3 * 4, 2), 6); ck(R(54, 6), 9)
FL = [(0, 0), (4, 0), (4, 1), (1.5, 1), (1.5, 3), (0, 3)]
def Lfig(k, x0, labs, cls):
    """forma de L (FL) ampliada amb raó k i desplaçada x0, amb les etiquetes dels costats: (inferior, dreta, graó, interior, superior, esquerra)"""
    P = [(x0 + px * k, py * k) for px, py in FL]
    pos = [((x0 + 2 * k, 0), {'dy': 15}), ((x0 + 4 * k, 0.5 * k), {'dx': 6, 'a': 'start'}), ((x0 + 2.75 * k, k), {'dy': -6}),
           ((x0 + 1.5 * k, 2 * k), {'dx': 6, 'a': 'start'}), ((x0 + 0.75 * k, 3 * k), {'dy': -6}), ((x0, 1.5 * k), {'dx': -6, 'a': 'end'})]
    return [('poly', P, cls)] + [('txt', p, t, o) for (p, o), t in zip(pos, labs) if t]
FIG15 = tz(Lfig(1, 0, ['4', '1', '2,5', '2', '1,5', '3'], 'gf') + Lfig(1.5, 6, ['6', 'x', '', 'y', '', '4,5'], 'tr'), 0.42)
S_.append((T("Figures semblants", "Figuras semejantes"), [
 (1, T(r"Digues si són sempre semblants (\textit{sí} o \textit{no}) i explica per què:", r"Di si son siempre semejantes (\textit{sí} o \textit{no}) y explica por qué:")
     + tasks(2, [T(r"Dos quadrats qualssevol.", r"Dos cuadrados cualesquiera."), T(r"Dos rectangles qualssevol.", r"Dos rectángulos cualesquiera."),
                 T(r"Dos triangles equilàters.", r"Dos triángulos equiláteros."), T(r"Un quadrat i un rombe de 4 cm de costat.", r"Un cuadrado y un rombo de 4 cm de lado.")])
     + recorda(T(r"Dues figures són \textbf{semblants} si tenen els angles iguals i els costats homòlegs proporcionals. La \textbf{raó de semblança} és $k=\frac{\text{costat nou}}{\text{costat original}}$: si $k>1$ és una ampliació i si $k<1$, una reducció.",
                 r"Dos figuras son \textbf{semejantes} si tienen los ángulos iguales y los lados homólogos proporcionales. La \textbf{razón de semejanza} es $k=\frac{\text{lado nuevo}}{\text{lado original}}$: si $k>1$ es una ampliación y si $k<1$, una reducción.")),
     tasks(2, [T(r"\rest{Sí}: angles rectes i costats proporcionals.", r"\rest{Sí}: ángulos rectos y lados proporcionales."), T(r"\rest{No}: poden ser més o menys allargats.", r"\rest{No}: pueden ser más o menos alargados."),
               T(r"\rest{Sí}: tots els angles fan 60°.", r"\rest{Sí}: todos los ángulos miden 60°."), T(r"\rest{No}: els angles són diferents.", r"\rest{No}: los ángulos son distintos.")])),
 (1, T(r"Calcula la raó de semblança i digues si és una ampliació o una reducció:", r"Calcula la razón de semejanza y di si es una ampliación o una reducción:")
     + tasks(1, [T(r"D'un rectangle de 4 cm × 6 cm a un altre de 10 cm × 15 cm.", r"De un rectángulo de 4 cm × 6 cm a otro de 10 cm × 15 cm."),
                 T(r"D'un triangle de costats 3, 4 i 5 cm a un altre de costats 1,5, 2 i 2,5 cm.", r"De un triángulo de lados 3, 4 y 5 cm a otro de lados 1,5, 2 y 2,5 cm.")]),
     tasks(1, [T(r"$k=\frac{10}{4}=\frac{15}{6}=\res{2{,}5}$: \rest{ampliació}", r"$k=\frac{10}{4}=\frac{15}{6}=\res{2{,}5}$: \rest{ampliación}"),
               T(r"$k=\frac{1{,}5}{3}=\frac24=\frac{2{,}5}{5}=\res{0{,}5}$: \rest{reducció}", r"$k=\frac{1{,}5}{3}=\frac24=\frac{2{,}5}{5}=\res{0{,}5}$: \rest{reducción}")])),
 (1, T(r"Un triangle té costats de 5, 7 i 9 cm. Calcula els costats d'un triangle semblant: \ a) amb raó $k=3$; \ b) amb raó $k=0{,}4$.", r"Un triángulo tiene lados de 5, 7 y 9 cm. Calcula los lados de un triángulo semejante: \ a) con razón $k=3$; \ b) con razón $k=0{,}4$."),
     T(r"a) $\res{15,\ 21\text{ i }27\text{ cm}}$. \quad b) $5\cdot0{,}4=2$, \ $7\cdot0{,}4=2{,}8$, \ $9\cdot0{,}4=3{,}6$: \ $\res{2,\ 2{,}8\text{ i }3{,}6\text{ cm}}$.", r"a) $\res{15,\ 21\text{ y }27\text{ cm}}$. \quad b) $5\cdot0{,}4=2$, \ $7\cdot0{,}4=2{,}8$, \ $9\cdot0{,}4=3{,}6$: \ $\res{2,\ 2{,}8\text{ y }3{,}6\text{ cm}}$.")),
 (1, T(r"Un rectangle de 6 cm × 9 cm és semblant a un altre que té el costat menut de 4 cm. Calcula la raó de semblança i el costat gran del segon rectangle.", r"Un rectángulo de 6 cm × 9 cm es semejante a otro que tiene el lado pequeño de 4 cm. Calcula la razón de semejanza y el lado grande del segundo rectángulo."),
     r"$k=\frac46=\res{\frac23}$; \quad $9\cdot\frac23=\res{6\text{ cm}}$."),
 (2, T(r"Les dues figures són semblants. Calcula la raó de semblança i els costats $x$ i $y$.", r"Las dos figuras son semejantes. Calcula la razón de semejanza y los lados $x$ e $y$.") + fig(FIG15),
     T(r"$k=\frac64=\frac{4{,}5}{3}=\res{1{,}5}$; \quad $x=1\cdot1{,}5=\res{1{,}5}$; \quad $y=2\cdot1{,}5=\res{3}$.", r"$k=\frac64=\frac{4{,}5}{3}=\res{1{,}5}$; \quad $x=1\cdot1{,}5=\res{1{,}5}$; \quad $y=2\cdot1{,}5=\res{3}$.")),
 (2, T(r"Són semblants aquests rectangles? Si ho són, calcula la raó de semblança.", r"¿Son semejantes estos rectángulos? Si lo son, calcula la razón de semejanza.") + tasks(2, [r"4 cm × 10 cm \ " + I_ + r" \ 6 cm × 15 cm", r"5 cm × 8 cm \ " + I_ + r" \ 10 cm × 18 cm"]),
     tasks(2, [T(r"$\frac64=\frac{15}{10}=1{,}5$: \rest{sí}, $k=1{,}5$", r"$\frac64=\frac{15}{10}=1{,}5$: \rest{sí}, $k=1{,}5$"), T(r"$\frac{10}{5}=2\neq\frac{18}{8}=2{,}25$: \rest{no}", r"$\frac{10}{5}=2\neq\frac{18}{8}=2{,}25$: \rest{no}")])),
 (2, T(r"Un polígon té 24 cm de perímetre i 32 cm² d'àrea. Calcula el perímetre i l'àrea d'un polígon semblant amb raó $k=2{,}5$.", r"Un polígono tiene 24 cm de perímetro y 32 cm² de área. Calcula el perímetro y el área de un polígono semejante con razón $k=2{,}5$.")
     + recorda(T(r"Si la raó de semblança és $k$, els perímetres es multipliquen per $k$ i les àrees, per $k^2$.", r"Si la razón de semejanza es $k$, los perímetros se multiplican por $k$ y las áreas, por $k^2$.")),
     r"$P'=24\cdot2{,}5=\res{60\text{ cm}}$; \quad $A'=32\cdot2{,}5^2=32\cdot6{,}25=\res{200\text{ cm}^2}$."),
 (2, T(r"Un quadrat de 6 cm de costat es redueix amb raó $k=\frac13$. Calcula el costat i l'àrea del quadrat nou. Quantes vegades és més menuda l'àrea?", r"Un cuadrado de 6 cm de lado se reduce con razón $k=\frac13$. Calcula el lado y el área del cuadrado nuevo. ¿Cuántas veces es más pequeña el área?"),
     T(r"Costat $6\cdot\frac13=\res{2\text{ cm}}$; \ àrea $2^2=\res{4\text{ cm}^2}$ (abans, 36 cm²). L'àrea és $\res{9}$ vegades més menuda ($3^2=9$).", r"Lado $6\cdot\frac13=\res{2\text{ cm}}$; \ área $2^2=\res{4\text{ cm}^2}$ (antes, 36 cm²). El área es $\res{9}$ veces más pequeña ($3^2=9$).")),
 (2, T(r"Un triangle té costats de 6, 8 i 10 cm. Un triangle semblant té 72 cm de perímetre. Quant fan els seus costats?", r"Un triángulo tiene lados de 6, 8 y 10 cm. Un triángulo semejante tiene 72 cm de perímetro. ¿Cuánto miden sus lados?"),
     T(r"$P=6+8+10=24$; \ $k=\frac{72}{24}=3$: \ $\res{18,\ 24\text{ i }30\text{ cm}}$.", r"$P=6+8+10=24$; \ $k=\frac{72}{24}=3$: \ $\res{18,\ 24\text{ y }30\text{ cm}}$.")),
 (3, T(r"Dos quadrats tenen àrees de 9 cm² i 81 cm². Quant fa el costat de cadascun? Quina és la raó de semblança?", r"Dos cuadrados tienen áreas de 9 cm² y 81 cm². ¿Cuánto mide el lado de cada uno? ¿Cuál es la razón de semejanza?"),
     T(r"Costats $\sqrt9=\res{3\text{ cm}}$ i $\sqrt{81}=\res{9\text{ cm}}$; \ $k=\frac93=\res{3}$ (l'àrea es multiplica per $3^2=9$).", r"Lados $\sqrt9=\res{3\text{ cm}}$ y $\sqrt{81}=\res{9\text{ cm}}$; \ $k=\frac93=\res{3}$ (el área se multiplica por $3^2=9$).")),
 (3, T(r"Ampliem una foto de 10 cm × 15 cm i la foto ampliada té 600 cm² d'àrea. Quina és la raó de semblança? Quines dimensions té la foto ampliada?", r"Ampliamos una foto de 10 cm × 15 cm y la foto ampliada tiene 600 cm² de área. ¿Cuál es la razón de semejanza? ¿Qué dimensiones tiene la foto ampliada?"),
     T(r"$A=150$ cm²; \ $k^2=\frac{600}{150}=4\Rightarrow k=\res{2}$. \ Foto de $\res{20\text{ cm}\times30\text{ cm}}$.", r"$A=150$ cm²; \ $k^2=\frac{600}{150}=4\Rightarrow k=\res{2}$. \ Foto de $\res{20\text{ cm}\times30\text{ cm}}$.")),
 (3, T(r"Un triangle rectangle té catets de 3 cm i 4 cm, i la hipotenusa fa 5 cm. Un triangle semblant té una hipotenusa de 15 cm. Calcula els seus catets i compara les àrees dels dos triangles.", r"Un triángulo rectángulo tiene catetos de 3 cm y 4 cm, y la hipotenusa mide 5 cm. Un triángulo semejante tiene una hipotenusa de 15 cm. Calcula sus catetos y compara las áreas de los dos triángulos."),
     T(r"$k=\frac{15}{5}=3$: catets $\res{9\text{ cm}}$ i $\res{12\text{ cm}}$. \ Àrees: $\frac{3\cdot4}{2}=6$ cm² i $\frac{9\cdot12}{2}=54$ cm²: l'àrea és $\res{9}$ vegades més gran ($3^2$).", r"$k=\frac{15}{5}=3$: catetos $\res{9\text{ cm}}$ y $\res{12\text{ cm}}$. \ Áreas: $\frac{3\cdot4}{2}=6$ cm² y $\frac{9\cdot12}{2}=54$ cm²: el área es $\res{9}$ veces mayor ($3^2$).")),
]))

# =====================================================================
# 2. Plànols, mapes i maquetes
# =====================================================================
ck(7 * 50000, 350000); ck(R(350000, 100000), 3.5); ck(4 * 100, 400); ck(R(25, 10) * 200000 / 100000, 5); ck(12 * 250 / 100, 30)
ck(R(800, 200), 4); ck(R(1500000, 500000), 3); ck(R(12000, 2000), 6)
ck(R(150000, 3), 50000); ck(R(1000, 5), 200); ck(R(4000000, 2), 2000000)
ck(R(50000, 1), 50000); ck(R(65, 10) * R(1, 2), 3.25)
ck(8 * 50, 400); ck(R(64, 10) * 50, 320); ck(4 * R(32, 10), 12.8)
ck(18 * 25000, 450000); ck(R(450000, 100000), 4.5); ck(R(45, 10) / 5 * 60, 54)
ck(R(3600, 72), 50); ck(R(2880, 72), 40)
ck(9 * 500, 4500); ck(R(4500, 100), 45)
ck(R(18000000, 6), 3000000); ck(R(25, 10) * 3000000 / 100000, 75)
ck(25 * 16, 400); ck(400 * 150, 60000)
ck(R(8, 20), 0.4)
GRAF = tz([('poly', [(0, 0), (4, 0), (4, 0.3), (0, 0.3)], 'gf'), ('poly', [(0, 0), (1, 0), (1, 0.3), (0, 0.3)], 'tr'), ('poly', [(2, 0), (3, 0), (3, 0.3), (2, 0.3)], 'tr'),
           ('lab', (0, -0.35), '0'), ('lab', (1, -0.35), '0,5'), ('lab', (2, -0.35), '1'), ('lab', (3, -0.35), '1,5'), ('lab', (4.25, -0.35), '2 km')], 1)
S_.append((T("Plànols, mapes i maquetes", "Planos, mapas y maquetas"), [
 (1, T(r"Calcula la distància real i expressa-la en m o en km:", r"Calcula la distancia real y exprésala en m o en km:")
     + tasks(2, [T(r"7 cm en un mapa $1:50\,000$", r"7 cm en un mapa $1:50\,000$"), T(r"4 cm en un plànol $1:100$", r"4 cm en un plano $1:100$"),
                 T(r"2,5 cm en un mapa $1:200\,000$", r"2,5 cm en un mapa $1:200\,000$"), T(r"12 cm en un plànol $1:250$", r"12 cm en un plano $1:250$")])
     + recorda(T(r"Escala $1:n$: 1 cm del plànol són $n$ cm reals. \ Real $=$ plànol $\times\,n$; \ plànol $=$ real $:\,n$. \ 1 m $=100$ cm; \ 1 km $=100\,000$ cm.",
                 r"Escala $1:n$: 1 cm del plano son $n$ cm reales. \ Real $=$ plano $\times\,n$; \ plano $=$ real $:\,n$. \ 1 m $=100$ cm; \ 1 km $=100\,000$ cm.")),
     tasks(2, [r"$350\,000\text{ cm}=\res{3{,}5\text{ km}}$", r"$400\text{ cm}=\res{4\text{ m}}$", r"$500\,000\text{ cm}=\res{5\text{ km}}$", r"$3000\text{ cm}=\res{30\text{ m}}$"])),
 (1, T(r"Quina longitud tindrà en el plànol o en el mapa?", r"¿Qué longitud tendrá en el plano o en el mapa?")
     + tasks(1, [T(r"Una paret de 8 m, en un plànol $1:200$.", r"Una pared de 8 m, en un plano $1:200$."), T(r"Una carretera de 15 km, en un mapa $1:500\,000$.", r"Una carretera de 15 km, en un mapa $1:500\,000$."),
                 T(r"Un carrer de 120 m, en un plànol $1:2000$.", r"Una calle de 120 m, en un plano $1:2000$.")]),
     tasks(1, [r"$800:200=\res{4\text{ cm}}$", r"$1\,500\,000:500\,000=\res{3\text{ cm}}$", r"$12\,000:2000=\res{6\text{ cm}}$"])),
 (1, T(r"Calcula l'escala:", r"Calcula la escala:")
     + tasks(1, [T(r"3 cm del mapa representen 1,5 km.", r"3 cm del mapa representan 1,5 km."), T(r"5 cm del plànol representen 10 m.", r"5 cm del plano representan 10 m."), T(r"2 cm del mapa representen 40 km.", r"2 cm del mapa representan 40 km.")]),
     tasks(1, [r"$150\,000:3=50\,000$: \ $\res{1:50\,000}$", r"$1000:5=200$: \ $\res{1:200}$", r"$4\,000\,000:2=2\,000\,000$: \ $\res{1:2\,000\,000}$"])),
 (2, T(r"Aquesta és l'escala gràfica d'un mapa (cada tram fa 1 cm). Quina és l'escala numèrica? Quina distància real hi ha entre dos punts que estan a 6,5 cm en el mapa?", r"Esta es la escala gráfica de un mapa (cada tramo mide 1 cm). ¿Cuál es la escala numérica? ¿Qué distancia real hay entre dos puntos que están a 6,5 cm en el mapa?") + fig(GRAF),
     T(r"1 cm són 500 m $=50\,000$ cm: \ $\res{1:50\,000}$. \ $6{,}5\cdot500=3250$ m $=\res{3{,}25\text{ km}}$.", r"1 cm son 500 m $=50\,000$ cm: \ $\res{1:50\,000}$. \ $6{,}5\cdot500=3250$ m $=\res{3{,}25\text{ km}}$.")),
 (2, T(r"En el plànol d'una casa a escala $1:50$, un dormitori fa 8 cm × 6,4 cm. Quines dimensions reals té? Quina superfície?", r"En el plano de una casa a escala $1:50$, un dormitorio mide 8 cm × 6,4 cm. ¿Qué dimensiones reales tiene? ¿Qué superficie?"),
     r"$8\cdot50=400$ cm $=4$ m; \ $6{,}4\cdot50=320$ cm $=3{,}2$ m. \ " + T(r"$\res{4\text{ m}\times3{,}2\text{ m}}$, \ superfície $\res{12{,}8\text{ m}^2}$.", r"$\res{4\text{ m}\times3{,}2\text{ m}}$, \ superficie $\res{12{,}8\text{ m}^2}$.")),
 (2, T(r"En un mapa a escala $1:25\,000$, el camí d'una excursió fa 18 cm. Quants km té l'excursió? Quant de temps tardarem si caminem a 5 km/h?", r"En un mapa a escala $1:25\,000$, el camino de una excursión mide 18 cm. ¿Cuántos km tiene la excursión? ¿Cuánto tiempo tardaremos si caminamos a 5 km/h?"),
     T(r"$18\cdot25\,000=450\,000$ cm $=\res{4{,}5\text{ km}}$. \ $4{,}5:5=0{,}9$ h $=\res{54\text{ minuts}}$.", r"$18\cdot25\,000=450\,000$ cm $=\res{4{,}5\text{ km}}$. \ $4{,}5:5=0{,}9$ h $=\res{54\text{ minutos}}$.")),
 (2, T(r"Una maqueta d'un avió està feta a escala $1:72$. L'avió real fa 36 m de llarg i 28,8 m d'ala a ala. Quines mesures té la maqueta?", r"Una maqueta de un avión está hecha a escala $1:72$. El avión real mide 36 m de largo y 28,8 m de ala a ala. ¿Qué medidas tiene la maqueta?"),
     T(r"$3600:72=\res{50\text{ cm}}$ de llarg; \ $2880:72=\res{40\text{ cm}}$ d'ala a ala.", r"$3600:72=\res{50\text{ cm}}$ de largo; \ $2880:72=\res{40\text{ cm}}$ de ala a ala.")),
 (2, T(r"En una maqueta a escala $1:500$, un edifici fa 9 cm d'altura. Quina altura té l'edifici real?", r"En una maqueta a escala $1:500$, un edificio mide 9 cm de altura. ¿Qué altura tiene el edificio real?"),
     r"$9\cdot500=4500$ cm $=\res{45\text{ m}}$."),
 (3, T(r"Dues ciutats que estan a 180 km es troben a 6 cm en un mapa. Quina és l'escala del mapa? A quina distància real està una altra ciutat que en el mapa és a 2,5 cm?", r"Dos ciudades que están a 180 km se encuentran a 6 cm en un mapa. ¿Cuál es la escala del mapa? ¿A qué distancia real está otra ciudad que en el mapa está a 2,5 cm?"),
     r"$180\text{ km}=18\,000\,000$ cm; \ $18\,000\,000:6=3\,000\,000$: \ $\res{1:3\,000\,000}$. \ $2{,}5\cdot30=\res{75\text{ km}}$ " + T("(1 cm són 30 km).", "(1 cm son 30 km).")),
 (3, T(r"En un plànol a escala $1:100$, una parcel·la rectangular fa 25 cm × 16 cm. Quina superfície real té? Si el metre quadrat costa 150~€, quant costa la parcel·la?", r"En un plano a escala $1:100$, una parcela rectangular mide 25 cm × 16 cm. ¿Qué superficie real tiene? Si el metro cuadrado cuesta 150~€, ¿cuánto cuesta la parcela?"),
     T(r"1 cm del plànol és 1 m real: $25\text{ m}\times16\text{ m}=\res{400\text{ m}^2}$. \ $400\cdot150=\res{60\,000\text{ €}}$.", r"1 cm del plano es 1 m real: $25\text{ m}\times16\text{ m}=\res{400\text{ m}^2}$. \ $400\cdot150=\res{60\,000\text{ €}}$.")),
 (3, T(r"En un llibre de ciències hi ha el dibuix d'una formiga a escala $20:1$ (és a dir, ampliat 20 vegades). Si en el dibuix la formiga fa 8 cm, quant fa la formiga de veritat?", r"En un libro de ciencias está el dibujo de una hormiga a escala $20:1$ (es decir, ampliado 20 veces). Si en el dibujo la hormiga mide 8 cm, ¿cuánto mide la hormiga de verdad?"),
     r"$8:20=0{,}4$ cm $=\res{4\text{ mm}}$."),
]))

# =====================================================================
# 3. El teorema de Tales
# =====================================================================
assert prop(3, 4, 9, 12) and prop(5, 7, 10, 14) and prop(4, 6, 8, 12) and prop(2.5, 5, 3, 6)
assert prop(2, 5, 3, R(75, 10)); assert prop(6, 4, R(45, 10), 3); assert prop(4, 8, 3, 6)
assert prop(R(36, 10), R(48, 10), R(45, 10), 6); ck(R(45, 10) + 6, 10.5)
assert prop(3, R(45, 10), 4, 6) and not prop(2, 5, 3, 7)
ck(R(3, 2) * 3, 4.5); ck(R(3, 2) * 4, 6)
ck(R(21, 3), 7); ck(R(21, 7), 3); assert [3, 6, 12] == [1 * 3, 2 * 3, 4 * 3]
ck(R(84, 72), R(7, 6)); assert [18 * R(7, 6), 24 * R(7, 6), 30 * R(7, 6)] == [21, 28, 35] and 21 + 28 + 35 == 84
assert sp.solve(9 * x - 6 * (x + 2), x) == [4]; ck(R(10, 3), 3.33, 2)
TA3 = tz(tales(3, 2, ar=55, as_=82, p=3.6, labs={'AB': '6', 'BC': '4', 'A1B1': '4,5', 'B1C1': 'x'}, hot='B1C1'), 0.55)
TA4 = tz(tales(1.5, 3, ar=55, as_=82, p=3.6, labs={'AB': 'x', 'BC': '8', 'A1B1': '3', 'B1C1': '6'}, hot='AB'), 0.55)
PAR = T(r"Les rectes \textcolor{navy}{blau fosc} són paral·leles. Calcula $x$.", r"Las rectas \textcolor{navy}{azul oscuro} son paralelas. Calcula $x$.")
S_.append((T("El teorema de Tales", "El teorema de Tales"), [
 (1, T(r"Calcula $x$ en cada proporció:", r"Calcula $x$ en cada proporción:") + tasks(4, [r"$\dfrac34=\dfrac{x}{12}$", r"$\dfrac5x=\dfrac{10}{14}$", r"$\dfrac x6=\dfrac{8}{12}$", r"$\dfrac{2{,}5}{5}=\dfrac3x$"]),
     tasks(4, [r"$4x=36\Rightarrow\res{x=9}$", r"$10x=70\Rightarrow\res{x=7}$", r"$12x=48\Rightarrow\res{x=4}$", r"$2{,}5x=15\Rightarrow\res{x=6}$"])),
 (1, T(r"Tres rectes paral·leles tallen dues rectes $a$ i $b$. Sobre $a$ determinen $\overline{AB}=2$ cm i $\overline{BC}=5$ cm, i sobre $b$, $\overline{A'B'}=3$ cm. Calcula $\overline{B'C'}$.", r"Tres rectas paralelas cortan dos rectas $a$ y $b$. Sobre $a$ determinan $\overline{AB}=2$ cm y $\overline{BC}=5$ cm, y sobre $b$, $\overline{A'B'}=3$ cm. Calcula $\overline{B'C'}$.")
     + recorda(T(r"\textbf{Teorema de Tales:} si unes rectes paral·leles tallen dues rectes, els segments que determinen sobre l'una són proporcionals als de l'altra: $\frac{\overline{AB}}{\overline{BC}}=\frac{\overline{A'B'}}{\overline{B'C'}}$.",
                 r"\textbf{Teorema de Tales:} si unas rectas paralelas cortan dos rectas, los segmentos que determinan sobre una son proporcionales a los de la otra: $\frac{\overline{AB}}{\overline{BC}}=\frac{\overline{A'B'}}{\overline{B'C'}}$.")),
     r"$\frac25=\frac3x\Rightarrow2x=15\Rightarrow\res{x=7{,}5\text{ cm}}$."),
 (1, PAR + fig(TA3), r"$\frac64=\frac{4{,}5}{x}\Rightarrow6x=18\Rightarrow\res{x=3}$."),
 (2, PAR + fig(TA4), r"$\frac x8=\frac36\Rightarrow6x=24\Rightarrow\res{x=4}$."),
 (2, T(r"Amb rectes paral·leles, $\overline{AB}=3{,}6$, $\overline{BC}=4{,}8$ i $\overline{B'C'}=6$. Calcula $\overline{A'B'}$ i $\overline{A'C'}$.", r"Con rectas paralelas, $\overline{AB}=3{,}6$, $\overline{BC}=4{,}8$ y $\overline{B'C'}=6$. Calcula $\overline{A'B'}$ y $\overline{A'C'}$."),
     r"$\frac{3{,}6}{4{,}8}=\frac x6\Rightarrow4{,}8x=21{,}6\Rightarrow\res{\overline{A'B'}=4{,}5}$; \quad $\overline{A'C'}=4{,}5+6=\res{10{,}5}$."),
 (2, T(r"Unes rectes tallen dues secants i hi determinen aquests segments. Poden ser paral·leles les rectes?", r"Unas rectas cortan dos secantes y determinan en ellas estos segmentos. ¿Pueden ser paralelas las rectas?")
     + tasks(2, [T(r"3 i 4,5 en una; 4 i 6 en l'altra", r"3 y 4,5 en una; 4 y 6 en la otra"), T(r"2 i 5 en una; 3 i 7 en l'altra", r"2 y 5 en una; 3 y 7 en la otra")]),
     tasks(2, [r"$3\cdot6=4{,}5\cdot4=18$: \rest{" + SI + "}", r"$2\cdot7=14\neq5\cdot3=15$: \rest{" + NO + "}"])),
 (2, T(r"Quatre rectes paral·leles determinen sobre una recta $\overline{AB}=2$, $\overline{BC}=3$ i $\overline{CD}=4$, i sobre una altra, $\overline{A'B'}=3$. Calcula $\overline{B'C'}$ i $\overline{C'D'}$.", r"Cuatro rectas paralelas determinan sobre una recta $\overline{AB}=2$, $\overline{BC}=3$ y $\overline{CD}=4$, y sobre otra, $\overline{A'B'}=3$. Calcula $\overline{B'C'}$ y $\overline{C'D'}$."),
     T(r"Cada segment de la segona recta és $\frac32=1{,}5$ vegades el de la primera: \ $\overline{B'C'}=3\cdot1{,}5=\res{4{,}5}$, \ $\overline{C'D'}=4\cdot1{,}5=\res{6}$.", r"Cada segmento de la segunda recta es $\frac32=1{,}5$ veces el de la primera: \ $\overline{B'C'}=3\cdot1{,}5=\res{4{,}5}$, \ $\overline{C'D'}=4\cdot1{,}5=\res{6}$.")),
 (2, T(r"Dividim un segment de 21 cm: \ a) en 3 parts iguals; \ b) en parts proporcionals a 1, 2 i 4. Quant fa cada part?", r"Dividimos un segmento de 21 cm: \ a) en 3 partes iguales; \ b) en partes proporcionales a 1, 2 y 4. ¿Cuánto mide cada parte?"),
     T(r"a) $21:3=\res{7\text{ cm}}$ cada part. \quad b) $\frac{21}{1+2+4}=3$: \ $\res{3,\ 6\text{ i }12\text{ cm}}$.", r"a) $21:3=\res{7\text{ cm}}$ cada parte. \quad b) $\frac{21}{1+2+4}=3$: \ $\res{3,\ 6\text{ y }12\text{ cm}}$.")),
 (3, T(r"Tres solars tenen les partions paral·leles i donen a dos carrers. Al carrer Major, les façanes fan 18 m, 24 m i 30 m. Al carrer Nou, les tres façanes fan en total 84 m. Quant fa cada façana al carrer Nou?", r"Tres solares tienen las lindes paralelas y dan a dos calles. En la calle Mayor, las fachadas miden 18 m, 24 m y 30 m. En la calle Nueva, las tres fachadas miden en total 84 m. ¿Cuánto mide cada fachada en la calle Nueva?"),
     r"$\frac{84}{18+24+30}=\frac{84}{72}=\frac76$: \ $18\cdot\frac76=\res{21\text{ m}}$, \ $24\cdot\frac76=\res{28\text{ m}}$, \ $30\cdot\frac76=\res{35\text{ m}}$."),
 (3, T(r"Amb rectes paral·leles, $\overline{AB}=x$, $\overline{BC}=x+2$, $\overline{A'B'}=6$ i $\overline{B'C'}=9$. Calcula $x$.", r"Con rectas paralelas, $\overline{AB}=x$, $\overline{BC}=x+2$, $\overline{A'B'}=6$ y $\overline{B'C'}=9$. Calcula $x$."),
     r"$\frac{x}{x+2}=\frac69\Rightarrow9x=6x+12\Rightarrow3x=12\Rightarrow\res{x=4}$."),
 (3, T(r"Explica com dividiries un segment de 10 cm en 3 parts iguals amb regle i escaire, sense mesurar. Quant farà cada part?", r"Explica cómo dividirías un segmento de 10 cm en 3 partes iguales con regla y escuadra, sin medir. ¿Cuánto medirá cada parte?"),
     T(r"Des d'$A$ es traça una semirecta auxiliar i s'hi marquen 3 segments iguals. S'uneix l'última marca amb $B$ i, per les altres dues, es traça paral·leles a aquesta recta: tallen $AB$ en 3 parts iguals (teorema de Tales). Cada part fa $\frac{10}{3}\approx\res{3{,}33\text{ cm}}$.",
       r"Desde $A$ se traza una semirrecta auxiliar y se marcan en ella 3 segmentos iguales. Se une la última marca con $B$ y, por las otras dos, se trazan paralelas a esa recta: cortan $AB$ en 3 partes iguales (teorema de Tales). Cada parte mide $\frac{10}{3}\approx\res{3{,}33\text{ cm}}$.")),
]))

# =====================================================================
# 4. Aplicació a la semblança de triangles
# =====================================================================
assert sim([4, 5, 6], [8, 10, 12]) == 2 and sim([3, 3, 4], [6, 6, 9]) is None and sim([5, 12, 13], [7.5, 18, 19.5]) == R(3, 2)
assert sorted([45, 60, 180 - 45 - 60]) == sorted([60, 75, 180 - 60 - 75]); assert sorted([50, 50, 80]) != sorted([50, 90, 40])
ck(4 + 2, 6); ck(R(4 * 9, 6), 6); ck(R(8 * 3, 6), 4); ck(R(5 * 8, 4), 10)
assert sorted([90, 40, 50]) == sorted([90, 50, 40])
ck(R(9, 6), 1.5); ck(8 * R(3, 2), 12); ck(9 * R(3, 2), 13.5)
ck(R(6, 4), R(9, 6)); ck(R(53, 10) * R(3, 2), 7.95)
ck(R(45, 18), 2.5); assert [4 * R(5, 2), 6 * R(5, 2), 8 * R(5, 2)] == [10, 15, 20]
ck(R(5 * 12, 15), 4); ck(R(6 * 15, 5), 18); ck(18 - 6, 12); ck(10 + 12 + 12 + 4, 38)
ck(8 * 9, 72); ck(R(4 * 3, 2), 6); ck(R(10, 4), 2.5); ck(3 * R(5, 2), 7.5); ck(R(10 * R(75, 10), 2), 37.5); ck(6 * R(25, 4), 37.5)
TP3 = tz(tpos(6, 6.5, 52, 2 / 3, labs={'AB1': '4', 'B1B': '2', 'BC': '9', 'B1C1': 'x'}, hot='B1C1'), 0.5)
TP4 = tz(tpos(6, 6.5, 52, 2 / 3, labs={'AB1': '6', 'B1B': '3', 'AC1': '8', 'C1C': 'x'}, hot='C1C'), 0.5)
TP5 = tz(tpos(6, 6.5, 52, 0.5, labs={'AB1': '4', 'B1B': '4', 'B1C1': '5', 'BC': 'x'}, hot='BC'), 0.5)
TPP = T(r"En la figura, $B'C'\parallel BC$. Calcula $x$.", r"En la figura, $B'C'\parallel BC$. Calcula $x$.")
S_.append((T("Aplicació a la semblança de triangles", "Aplicación a la semejanza de triángulos"), [
 (1, T(r"Són semblants els triangles que tenen aquests costats? Si ho són, calcula la raó de semblança.", r"¿Son semejantes los triángulos que tienen estos lados? Si lo son, calcula la razón de semejanza.")
     + tasks(1, [T(r"4, 5, 6 \ i \ 8, 10, 12", r"4, 5, 6 \ y \ 8, 10, 12"), T(r"3, 3, 4 \ i \ 6, 6, 9", r"3, 3, 4 \ y \ 6, 6, 9"), T(r"5, 12, 13 \ i \ 7,5, 18, 19,5", r"5, 12, 13 \ y \ 7,5, 18, 19,5")])
     + recorda(T(r"Dos triangles són semblants si tenen \textbf{dos angles iguals}, o els \textbf{tres costats proporcionals}, o \textbf{dos costats proporcionals i l'angle que formen igual}. Per a comparar costats, ordena'ls de menor a major.",
                 r"Dos triángulos son semejantes si tienen \textbf{dos ángulos iguales}, o los \textbf{tres lados proporcionales}, o \textbf{dos lados proporcionales y el ángulo que forman igual}. Para comparar lados, ordénalos de menor a mayor.")),
     tasks(1, [r"$\frac84=\frac{10}5=\frac{12}6=2$: \rest{" + SI + r"}, $k=2$", r"$\frac63=2$, \ $\frac94=2{,}25$: \rest{" + NO + "}", r"$\frac{7{,}5}{5}=\frac{18}{12}=\frac{19{,}5}{13}=1{,}5$: \rest{" + SI + r"}, $k=1{,}5$"])),
 (1, T(r"Són semblants aquests triangles?", r"¿Son semejantes estos triángulos?")
     + tasks(1, [T(r"Un té angles de 45° i 60°, i l'altre, de 60° i 75°.", r"Uno tiene ángulos de 45° y 60°, y el otro, de 60° y 75°."), T(r"Un té angles de 50° i 50°, i l'altre, de 50° i 90°.", r"Uno tiene ángulos de 50° y 50°, y el otro, de 50° y 90°.")]),
     tasks(1, [T(r"El tercer angle del primer fa 75° i el del segon, 45°: tenen els mateixos angles: \rest{sí}.", r"El tercer ángulo del primero mide 75° y el del segundo, 45°: tienen los mismos ángulos: \rest{sí}."),
               T(r"Angles 50°, 50°, 80° i 50°, 90°, 40°: \rest{no}.", r"Ángulos 50°, 50°, 80° y 50°, 90°, 40°: \rest{no}.")])),
 (1, TPP + fig(TP3), r"$\overline{AB}=4+2=6$; \quad $\frac46=\frac x9\Rightarrow6x=36\Rightarrow\res{x=6}$."),
 (2, TPP + fig(TP4), T(r"Pel teorema de Tales: $\frac63=\frac8x\Rightarrow6x=24\Rightarrow\res{x=4}$.", r"Por el teorema de Tales: $\frac63=\frac8x\Rightarrow6x=24\Rightarrow\res{x=4}$.")),
 (2, TPP + fig(TP5), r"$\overline{AB}=4+4=8$; \quad $\frac48=\frac5x\Rightarrow4x=40\Rightarrow\res{x=10}$."),
 (2, T(r"Un triangle rectangle té un angle de 40°. Un altre triangle rectangle té un angle de 50°. Són semblants? Per què?", r"Un triángulo rectángulo tiene un ángulo de 40°. Otro triángulo rectángulo tiene un ángulo de 50°. ¿Son semejantes? ¿Por qué?"),
     T(r"\rest{Sí}: els angles del primer són 90°, 40° i 50°, i els del segon, 90°, 50° i 40°. Tenen els tres angles iguals.", r"\rest{Sí}: los ángulos del primero son 90°, 40° y 50°, y los del segundo, 90°, 50° y 40°. Tienen los tres ángulos iguales.")),
 (2, T(r"Els costats d'un triangle fan 6, 8 i 9 cm. En un triangle semblant, el costat menut fa 9 cm. Quant fan els altres dos costats?", r"Los lados de un triángulo miden 6, 8 y 9 cm. En un triángulo semejante, el lado pequeño mide 9 cm. ¿Cuánto miden los otros dos lados?"),
     T(r"$k=\frac96=1{,}5$: \ $8\cdot1{,}5=\res{12\text{ cm}}$ i $9\cdot1{,}5=\res{13{,}5\text{ cm}}$.", r"$k=\frac96=1{,}5$: \ $8\cdot1{,}5=\res{12\text{ cm}}$ y $9\cdot1{,}5=\res{13{,}5\text{ cm}}$.")),
 (2, T(r"En els triangles $ABC$ i $A'B'C'$, $\hat A=\hat A'=60^\circ$, $\overline{AB}=4$, $\overline{AC}=6$, $\overline{A'B'}=6$ i $\overline{A'C'}=9$. Són semblants? Si $\overline{BC}=5{,}3$, quant fa $\overline{B'C'}$?", r"En los triángulos $ABC$ y $A'B'C'$, $\hat A=\hat A'=60^\circ$, $\overline{AB}=4$, $\overline{AC}=6$, $\overline{A'B'}=6$ y $\overline{A'C'}=9$. ¿Son semejantes? Si $\overline{BC}=5{,}3$, ¿cuánto mide $\overline{B'C'}$?"),
     T(r"$\frac64=\frac96=1{,}5$ i l'angle comprés és igual: \rest{sí} (criteri 3r), $k=1{,}5$. \ $\overline{B'C'}=5{,}3\cdot1{,}5=\res{7{,}95}$.", r"$\frac64=\frac96=1{,}5$ y el ángulo comprendido es igual: \rest{sí} (criterio 3.º), $k=1{,}5$. \ $\overline{B'C'}=5{,}3\cdot1{,}5=\res{7{,}95}$.")),
 (3, T(r"Els costats d'un triangle fan 4, 6 i 8 cm. Un triangle semblant té 45 cm de perímetre. Quant fan els seus costats?", r"Los lados de un triángulo miden 4, 6 y 8 cm. Un triángulo semejante tiene 45 cm de perímetro. ¿Cuánto miden sus lados?"),
     T(r"$P=18$, \ $k=\frac{45}{18}=2{,}5$: \ $\res{10,\ 15\text{ i }20\text{ cm}}$.", r"$P=18$, \ $k=\frac{45}{18}=2{,}5$: \ $\res{10,\ 15\text{ y }20\text{ cm}}$.")),
 (3, T(r"En un triangle $ABC$, tracem $B'C'\parallel BC$ amb $\overline{AB'}=5$, $\overline{B'B}=10$, $\overline{BC}=12$ i $\overline{AC'}=6$. Calcula $\overline{B'C'}$, $\overline{C'C}$ i el perímetre del trapezi $B'BCC'$.", r"En un triángulo $ABC$, trazamos $B'C'\parallel BC$ con $\overline{AB'}=5$, $\overline{B'B}=10$, $\overline{BC}=12$ y $\overline{AC'}=6$. Calcula $\overline{B'C'}$, $\overline{C'C}$ y el perímetro del trapecio $B'BCC'$."),
     r"$\overline{AB}=15$; \ $\frac5{15}=\frac{x}{12}\Rightarrow\res{\overline{B'C'}=4}$; \ $\frac5{15}=\frac6{\overline{AC}}\Rightarrow\overline{AC}=18$, \ $\res{\overline{C'C}=12}$. \ $P=10+12+12+4=\res{38}$."),
 (3, T(r"Un triangle té una base de 4 cm i una altura de 3 cm. En un triangle semblant, la base fa 10 cm. Calcula'n l'altura i l'àrea. Per quant s'ha multiplicat l'àrea?", r"Un triángulo tiene una base de 4 cm y una altura de 3 cm. En un triángulo semejante, la base mide 10 cm. Calcula su altura y su área. ¿Por cuánto se ha multiplicado el área?"),
     T(r"$k=\frac{10}4=2{,}5$; \ altura $3\cdot2{,}5=\res{7{,}5\text{ cm}}$; \ àrea $\frac{10\cdot7{,}5}{2}=\res{37{,}5\text{ cm}^2}$ (abans, 6 cm²): s'ha multiplicat per $2{,}5^2=\res{6{,}25}$.", r"$k=\frac{10}4=2{,}5$; \ altura $3\cdot2{,}5=\res{7{,}5\text{ cm}}$; \ área $\frac{10\cdot7{,}5}{2}=\res{37{,}5\text{ cm}^2}$ (antes, 6 cm²): se ha multiplicado por $2{,}5^2=\res{6{,}25}$.")),
]))

# =====================================================================
# 5. Problemes amb semblança de triangles
# =====================================================================
ck(R(9 * 2) / R(15, 10), 12); ck(R(15, 10) * 14 / 21, 1); ck(R(15) * R(12, 10) / R(9, 10), 20)
ck(R(15) * R(16, 10) / 2, 12); ck(R(4) * R(9, 10) / 6, 0.6)
assert sp.solve(R(15, 10) * (x + 2) - R(45, 10) * x, x) == [1]
ck(R(15, 10) - R(6, 10), 0.9); ck(4 * R(9, 10) / R(15, 10), 2.4)
ck(6 * R(5, 10) / R(1, 10), 30); ck(R(25, 10) * 9 / 3, 7.5); ck(R(219) * R(18, 10) / R(27, 10), 146); ck(R(12, 10) * 8 / R(16, 10), 6)
SHD = tz(shadow(1.2, 0.9, 6, 4.5, '1,2 m', '$H$', '0,9 m', '15 m', hot='h2'), 0.42)
MIRT = tz([('seg', (-0.5, 0), (17.5, 0), 'axis'), ('seg', (0, 0), (0, 1.6), 'wall'), ('seg', (17, 0), (17, 12), 'wall'),
           ('seg', (0, 1.6), (2, 0), 'ray'), ('seg', (2, 0), (17, 12), 'ray'), ('poly', [(0, 0), (0, 1.6), (2, 0)], 'tr'), ('poly', [(2, 0), (17, 0), (17, 12)], 'gf'),
           ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (17, 0), (16, 0), (17, 1)), ('dot', (2, 0)),
           ('txt', (0, 0.8), '1,6 m', {'dx': -8, 'a': 'end'}), ('txt', (1, 0), '2 m', {'dy': 15}), ('txt', (9.5, 0), '15 m', {'dy': 15}), ('txt', (17, 6), '$H$', {'dx': 8, 'a': 'start', 'cls': 'hot'})], 0.22)
LADDER = tz([('seg', (-0.4, 0), (1.9, 0), 'axis'), ('seg', (0, 0), (0, 4.4), 'wall'), ('poly', [(0, 0), (1.5, 0), (0, 4)], 'gf'), ('seg', (0.6, 0), (0.6, 2.4), 'ray'), ('dot', (0.6, 2.4)),
             ('ra', (0, 0), (1, 0), (0, 1)), ('txt', (0, 2), '4 m', {'dx': -8, 'a': 'end'}), ('txt', (0.6, 1.2), '$h$', {'dx': 6, 'a': 'start', 'cls': 'hot'}),
             ('seg', (0, -0.35), (0.6, -0.35), 'ray'), ('lab', (0.3, -0.6), '0,6 m'), ('seg', (0, -0.95), (1.5, -0.95), 'ray'), ('lab', (0.75, -1.2), '1,5 m')], 0.75)
RIU = tz([('poly', [(-1, 0.3), (12, 0.3), (12, 7.2), (-1, 7.2)], 'water'), ('poly', [(0, 0), (0, 7.5), (9, 0)], 'gf'), ('poly', [(9, 0), (12, 0), (12, -2.5)], 'tr'), ('seg', (-1, 0), (12.5, 0), 'axis'),
          ('ra', (0, 0), (1, 0), (0, 1)), ('ra', (12, 0), (11, 0), (12, -1)),
          ('txt', (0, 7.5), '$A$', {'dx': -8, 'a': 'end'}), ('txt', (0, 0), '$B$', {'dx': -8, 'a': 'end'}), ('txt', (9, 0), '$C$', {'dx': -6, 'dy': -8, 'a': 'end'}), ('txt', (12, 0), '$D$', {'dx': 8, 'a': 'start'}), ('txt', (12, -2.5), '$E$', {'dx': 8, 'a': 'start'}),
          ('txt', (4.5, 0), '9 m', {'dy': 15}), ('txt', (10.5, 0), '3 m', {'dy': -8}), ('txt', (12, -1.25), '2,5 m', {'dx': 8, 'a': 'start'}), ('txt', (0, 3.75), 'x', {'dx': -8, 'a': 'end', 'cls': 'hot'})], 0.3)
S_.append((T("Problemes amb semblança de triangles", "Problemas con semejanza de triángulos"), [
 (1, T(r"Un arbre fa una ombra de 9 m. Al mateix moment, un pal de 2 m fa una ombra d'1,5 m. Quina altura té l'arbre?", r"Un árbol da una sombra de 9 m. En el mismo momento, un palo de 2 m da una sombra de 1,5 m. ¿Qué altura tiene el árbol?")
     + recorda(T(r"Fes un dibuix, busca dos triangles semblants (amb els mateixos angles o en posició de Tales) i escriu la proporció entre costats homòlegs. Al mateix moment, els rajos del Sol són paral·lels: altura i ombra són proporcionals.",
                 r"Haz un dibujo, busca dos triángulos semejantes (con los mismos ángulos o en posición de Tales) y escribe la proporción entre lados homólogos. En el mismo momento, los rayos del Sol son paralelos: altura y sombra son proporcionales.")),
     r"$\frac{H}{9}=\frac{2}{1{,}5}\Rightarrow H=\frac{9\cdot2}{1{,}5}=\res{12\text{ m}}$."),
 (1, T(r"Un edifici de 21 m fa una ombra de 14 m. Quina ombra fa, al mateix moment, una persona d'1,5 m?", r"Un edificio de 21 m da una sombra de 14 m. ¿Qué sombra da, en el mismo momento, una persona de 1,5 m?"),
     r"$\frac{1{,}5}{s}=\frac{21}{14}\Rightarrow21s=21\Rightarrow\res{s=1\text{ m}}$."),
 (1, T(r"Calcula l'altura $H$ de la torre.", r"Calcula la altura $H$ de la torre.") + fig(SHD), r"$\frac{H}{15}=\frac{1{,}2}{0{,}9}\Rightarrow H=\frac{15\cdot1{,}2}{0{,}9}=\res{20\text{ m}}$."),
 (2, T(r"La Clara té els ulls a 1,6 m de terra. Posa un mirall a terra, a 2 m d'ella i a 15 m d'un edifici, i hi veu just el capdamunt de l'edifici. Quina altura té l'edifici?", r"Clara tiene los ojos a 1,6 m del suelo. Pone un espejo en el suelo, a 2 m de ella y a 15 m de un edificio, y ve en él justo lo alto del edificio. ¿Qué altura tiene el edificio?") + fig(MIRT),
     r"$\frac{H}{15}=\frac{1{,}6}{2}\Rightarrow H=\frac{15\cdot1{,}6}{2}=\res{12\text{ m}}$."),
 (2, T(r"Una rampa puja 0,9 m d'altura en 6 m horitzontals. A quina altura està un punt de la rampa que és a 4 m (horitzontals) del començament?", r"Una rampa sube 0,9 m de altura en 6 m horizontales. ¿A qué altura está un punto de la rampa que está a 4 m (horizontales) del comienzo?"),
     T(r"Triangles en posició de Tales: $\frac h4=\frac{0{,}9}{6}\Rightarrow h=\frac{4\cdot0{,}9}{6}=\res{0{,}6\text{ m}}$.", r"Triángulos en posición de Tales: $\frac h4=\frac{0{,}9}{6}\Rightarrow h=\frac{4\cdot0{,}9}{6}=\res{0{,}6\text{ m}}$.")),
 (2, T(r"Una persona d'1,5 m està a 2 m d'un fanal de 4,5 m d'altura. Quant fa la seua ombra?", r"Una persona de 1,5 m está a 2 m de una farola de 4,5 m de altura. ¿Cuánto mide su sombra?"),
     r"$\frac{1{,}5}{s}=\frac{4{,}5}{s+2}\Rightarrow1{,}5s+3=4{,}5s\Rightarrow3s=3\Rightarrow\res{s=1\text{ m}}$."),
 (2, T(r"Una escala recolzada en una paret arriba a 4 m d'altura, i el seu peu està a 1,5 m de la paret. A quina altura $h$ està el punt de l'escala que és a 0,6 m de la paret?", r"Una escalera apoyada en una pared llega a 4 m de altura, y su pie está a 1,5 m de la pared. ¿A qué altura $h$ está el punto de la escalera que está a 0,6 m de la pared?") + fig(LADDER),
     T(r"Des del peu de l'escala, el punt està a $1{,}5-0{,}6=0{,}9$ m. \ $\frac h{0{,}9}=\frac4{1{,}5}\Rightarrow h=\frac{0{,}9\cdot4}{1{,}5}=\res{2{,}4\text{ m}}$.", r"Desde el pie de la escalera, el punto está a $1{,}5-0{,}6=0{,}9$ m. \ $\frac h{0{,}9}=\frac4{1{,}5}\Rightarrow h=\frac{0{,}9\cdot4}{1{,}5}=\res{2{,}4\text{ m}}$.")),
 (2, T(r"Amb el braç estirat, tapem exactament un arbre de 6 m d'altura amb un regle vertical de 10 cm que està a 50 cm dels ulls. A quina distància està l'arbre?", r"Con el brazo estirado, tapamos exactamente un árbol de 6 m de altura con una regla vertical de 10 cm que está a 50 cm de los ojos. ¿A qué distancia está el árbol?"),
     r"$\frac d6=\frac{0{,}5}{0{,}1}\Rightarrow d=\frac{6\cdot0{,}5}{0{,}1}=\res{30\text{ m}}$."),
 (3, T(r"Per a mesurar l'amplària $x$ d'un riu s'han pres les mesures de la figura ($AB\parallel DE$ i $A$, $C$, $E$ alineats). Quant fa d'ample el riu?", r"Para medir la anchura $x$ de un río se han tomado las medidas de la figura ($AB\parallel DE$ y $A$, $C$, $E$ alineados). ¿Cuánto mide de ancho el río?") + fig(RIU),
     T(r"Els triangles $ABC$ i $EDC$ són semblants (angle recte i angles en $C$ oposats pel vèrtex): $\frac x{2{,}5}=\frac93\Rightarrow\res{x=7{,}5\text{ m}}$.", r"Los triángulos $ABC$ y $EDC$ son semejantes (ángulo recto y ángulos en $C$ opuestos por el vértice): $\frac x{2{,}5}=\frac93\Rightarrow\res{x=7{,}5\text{ m}}$.")),
 (3, T(r"Tales, que feia 1,8 m d'altura, va mesurar la seua ombra: 2,7 m. Al mateix moment, l'ombra de la piràmide, comptada des del centre de la base, feia 219 m. Quina altura tenia la piràmide?", r"Tales, que medía 1,8 m de altura, midió su sombra: 2,7 m. En el mismo momento, la sombra de la pirámide, contada desde el centro de la base, medía 219 m. ¿Qué altura tenía la pirámide?"),
     r"$\frac{H}{219}=\frac{1{,}8}{2{,}7}\Rightarrow H=\frac{219\cdot1{,}8}{2{,}7}=\res{146\text{ m}}$."),
 (3, T(r"Un nen d'1,2 m es col·loca de manera que la punta de la seua ombra coincideix amb la de l'ombra d'un arbre. L'ombra del nen fa 1,6 m i el nen està a 6,4 m de l'arbre. Quina altura té l'arbre?", r"Un niño de 1,2 m se coloca de modo que la punta de su sombra coincide con la de la sombra de un árbol. La sombra del niño mide 1,6 m y el niño está a 6,4 m del árbol. ¿Qué altura tiene el árbol?"),
     T(r"L'ombra de l'arbre fa $1{,}6+6{,}4=8$ m (triangles en posició de Tales): $\frac H8=\frac{1{,}2}{1{,}6}\Rightarrow H=\frac{8\cdot1{,}2}{1{,}6}=\res{6\text{ m}}$.", r"La sombra del árbol mide $1{,}6+6{,}4=8$ m (triángulos en posición de Tales): $\frac H8=\frac{1{,}2}{1{,}6}\Rightarrow H=\frac{8\cdot1{,}2}{1{,}6}=\res{6\text{ m}}$.")),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("semblança, figures semblants, raó de semblança, escala, plànols, mapes, maquetes, teorema de Tales, posició de Tales, criteris de semblança, ombres",
       'semejanza, figuras semejantes, razón de semejanza, escala, planos, mapas, maquetas, teorema de Tales, posición de Tales, criterios de semejanza, sombras')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\usepackage{pifont}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T("Semblança. Teorema de Tales", 'Semejanza. Teorema de Tales')
NU = 8

def build(sol_):
    if ES:
        sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad %d: %s' % (t, NU, TIT), capcalera='%s · Unidad %d: %s' % (t, NU, TIT), pdfkeywords=KW, curs='2eso')
        cap = assignatura('2eso') + '{' + ('Soluciones de la ficha · Unidad %d' % NU if sol_ else 'Ficha de ejercicios · Unidad %d' % NU) + '}{' + TIT + '}'
    else:
        t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat %d: %s. 2n d'ESO}" % (t, NU, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat %d: %s · 2n d'ESO" % (t, NU, TIT))
        assert "2n d'ESO" in p and 'Unitat %d' % NU in p and 'unitat %d' % NU in p
        cap = r'\capcalera{Matemàtiques}{2n ESO}{' + ('Solucions de la fitxa · Unitat %d' % NU if sol_ else "Fitxa d'exercicis · Unitat %d" % NU) + '}{' + TIT + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol_ else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{14}\n\\input{../comu/fentmates.tex}\n\\fmcurs{2eso}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol_:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs una calculadora de proporcions i d'escales i eines per a practicar la semblança i el teorema de Tales. Els resultats aproximats estan arrodonits a les centèsimes.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás una calculadora de proporciones y de escalas y herramientas para practicar la semejanza y el teorema de Tales. Los resultados aproximados están redondeados a las centésimas.") if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i fes un dibuix de cada situació. Escriu la proporció abans de calcular. Les seccions segueixen l'ordre dels apunts de la unitat (8.1--8.5).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y haz un dibujo de cada situación. Escribe la proporción antes de calcular. Las secciones siguen el orden de los apuntes de la unidad (8.1--8.5)."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            out.append('\\ex{%d} %s\n\n' % (st, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't%d-fitxa-%s%s.tex' % (NU, 'solucions' if sol_ else 'exercicis', '-es' if ES else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(x[1]) for x in S_), T('exercicis', 'ejercicios'))
