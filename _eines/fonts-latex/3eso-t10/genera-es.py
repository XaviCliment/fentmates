# Versió en castellà de genera.py. Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (3r ESO, Unitat 10: Proporcionalitat. Teorema de Tales)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Cada resultat numèric es comprova amb ck(valor exacte, valor escrit, decimals de l'arrodoniment).
# Les figures es dibuixen amb la geometria de ../../apunts/3eso-t10/fig10.py (la mateixa que als apunts).
import os, re, sys, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'apunts', '3eso-t10'))
from fig10 import tales, tpos, shadow

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
      'ray': 'dashed,draw=muted', 'axis': 'muted', 'wall': 'line width=2pt,draw=muted', 'ang': 'draw=navy', '': 'thick'}
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

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Raons i proporcions entre segments
# =====================================================================
ck(R(12, 8), 1.5); ck(R(5, 20), 0.25); ck(R(60, 45), 1.33, 2); ck(R(20, 25), 0.8)
for a, b, c, d in [(3, 5, 12, 20), (8, 28, 2, 7), (10, 4, 15, 6), (2.5, 4, 5, 8), (6, 9, 10, 15), (3, 12, 0.75, 3)]: assert prop(a, b, c, d)
assert prop(2, 3, 4, 6) and not prop(3, 5, 6, 9) and prop(1.5, 2, 4.5, 6) and not prop(4, 7, 8, 15)
ck(R(6 * 10, 4), 15); ck(R(3) * 7 / R(25, 10), 8.4); ck(R(12 * 5, 3), 20); ck(R(56, 7) * 3, 24); ck(R(56, 7) * 4, 32)
ck(S(4 * 25), 10); ck(S(2 * 8), 4); ck(S(18), 4.24, 2)
S_.append(("Razones y proporciones entre segmentos", [
 (1, r"Calcula la razón entre los segmentos (si no es exacta, redondea a las centésimas):" + tasks(4, [r"12 cm y 8 cm", r"5 cm y 20 cm", r"0,6 m y 45 cm", r"2 dm y 25 cm"])
     + recorda(r"La \textbf{razón} de dos segmentos es el cociente de sus longitudes, medidas con la \textbf{misma unidad}. Cuatro segmentos son \textbf{proporcionales} si $\frac ab=\frac cd$, es decir, si $a\cdot d=b\cdot c$ (producto de los extremos = producto de los medios)."),
     tasks(4, [r"$\frac{12}{8}=\res{1{,}5}$", r"$\frac{5}{20}=\res{0{,}25}$", r"$\frac{60}{45}\approx\res{1{,}33}$", r"$\frac{20}{25}=\res{0{,}8}$"])),
 (1, r"Calcula $x$ en cada proporción:" + tasks(3, [r"$\dfrac35=\dfrac{x}{20}$", r"$\dfrac8x=\dfrac27$", r"$\dfrac x4=\dfrac{15}{6}$", r"$\dfrac{2{,}5}{x}=\dfrac58$", r"$\dfrac69=\dfrac{10}{x}$", r"$\dfrac{x}{12}=\dfrac{0{,}75}{3}$"]),
     tasks(3, [r"$5x=60\Rightarrow\res{x=12}$", r"$2x=56\Rightarrow\res{x=28}$", r"$6x=60\Rightarrow\res{x=10}$", r"$5x=20\Rightarrow\res{x=4}$", r"$6x=90\Rightarrow\res{x=15}$", r"$3x=9\Rightarrow\res{x=3}$"])),
 (1, r"¿Son proporcionales, en este orden, los siguientes segmentos?" + tasks(2, [r"2, 3, 4 y 6 cm", r"3, 5, 6 y 9 cm", r"1,5, 2, 4,5 y 6 cm", r"4, 7, 8 y 15 cm"]),
     tasks(2, [r"$2\cdot6=3\cdot4=12$: \rest{sí}", r"$3\cdot9=27\neq5\cdot6=30$: \rest{no}", r"$1{,}5\cdot6=2\cdot4{,}5=9$: \rest{sí}", r"$4\cdot15=60\neq7\cdot8=56$: \rest{no}"])),
 (2, r"Calcula el cuarto proporcional de los segmentos: \ a) 4, 6 y 10 cm; \ b) 2,5, 3 y 7 cm.",
     r"a) $\frac46=\frac{10}{x}\Rightarrow x=\frac{6\cdot10}{4}=\res{15\text{ cm}}$. \quad b) $\frac{2{,}5}{3}=\frac{7}{x}\Rightarrow x=\frac{3\cdot7}{2{,}5}=\res{8{,}4\text{ cm}}$."),
 (2, r"Dos segmentos están en razón $\frac35$. Si el pequeño mide 12 cm, ¿cuánto mide el grande?",
     r"$\frac35=\frac{12}{x}\Rightarrow3x=60\Rightarrow\res{x=20\text{ cm}}$."),
 (2, r"Dos segmentos suman 56 cm y están en razón $\frac34$. ¿Cuánto mide cada uno?",
     r"Son $3u$ y $4u$: $7u=56\Rightarrow u=8$. Segmentos de $\res{24\text{ cm}}$ y $\res{32\text{ cm}}$."),
 (3, r"La \textbf{media proporcional} de $a$ y $b$ es el segmento $x$ tal que $\frac ax=\frac xb$. Calcula la media proporcional de: \ a) 4 y 25; \ b) 2 y 8; \ c) 3 y 6 (redondea a las centésimas).",
     r"$x^2=a\cdot b$: \ a) $x^2=100\Rightarrow\res{x=10}$; \ b) $x^2=16\Rightarrow\res{x=4}$; \ c) $x^2=18\Rightarrow x=\sqrt{18}\approx\res{4{,}24}$."),
]))

# =====================================================================
# 2. El teorema de Tales
# =====================================================================
assert prop(4, 6, 6, 9); assert prop(3, 5, R(48, 10), 8); assert prop(6, R(75, 10), 4, 5); assert prop(4, 10, 6, 15)
assert sp.solve(8 * x - 4 * 6, x) == [3]
assert prop(2, 3, 4, 6) and not prop(3, 4, 4, 5) and prop(1.5, 2.5, 2.4, 4)
ck(R(72, 60), 1.2); assert [15 * R(6, 5), 20 * R(6, 5), 25 * R(6, 5)] == [18, 24, 30]
assert sp.solve(5 * x - 3 * (x + 4), x) == [6]
ck(R(5, 13) * R(195, 10), 7.5); ck(R(8, 13) * R(195, 10), 12)
S_.append(("El teorema de Tales", [
 (1, r"Las rectas \textcolor{navy}{azul oscuro} son paralelas. Calcula $x$." + fig(tz(tales(2, 3, ar=55, as_=82, p=3.6, labs={'AB': '4', 'BC': '6', 'A1B1': '6', 'B1C1': 'x'}, hot='B1C1'), 0.55))
     + recorda(r"\textbf{Teorema de Tales:} si unas rectas paralelas cortan dos secantes, los segmentos que determinan sobre una son proporcionales a los de la otra: $\frac{\overline{AB}}{\overline{BC}}=\frac{\overline{A'B'}}{\overline{B'C'}}$, o bien $\frac{\overline{AB}}{\overline{A'B'}}=\frac{\overline{BC}}{\overline{B'C'}}=\frac{\overline{AC}}{\overline{A'C'}}$."),
     r"$\frac46=\frac6x\Rightarrow4x=36\Rightarrow\res{x=9}$."),
 (1, r"Las rectas $r$, $s$ y $t$ son paralelas y cortan las secantes en $A,\,B,\,C$ y $A',\,B',\,C'$. Calcula el segmento que falta:"
     + tasks(1, [r"$\overline{AB}=3$, $\overline{BC}=5$, $\overline{A'B'}=4{,}8$. Calcula $\overline{B'C'}$.", r"$\overline{AB}=6$, $\overline{A'B'}=4$, $\overline{B'C'}=5$. Calcula $\overline{BC}$.", r"$\overline{AB}=4$, $\overline{AC}=10$, $\overline{A'C'}=15$. Calcula $\overline{A'B'}$."]),
     tasks(1, [r"$\frac35=\frac{4{,}8}{x}\Rightarrow\res{\overline{B'C'}=8}$", r"$\frac64=\frac{x}{5}\Rightarrow\res{\overline{BC}=7{,}5}$", r"$\frac{4}{10}=\frac{x}{15}\Rightarrow\res{\overline{A'B'}=6}$"])),
 (2, r"Las rectas \textcolor{navy}{azul oscuro} son paralelas. Calcula $x$." + fig(tz(tales(1.6, 3.2, ar=55, as_=82, p=3.6, labs={'AB': 'x', 'BC': '6', 'A1B1': '4', 'B1C1': '8'}, hot='AB'), 0.55)),
     r"$\frac x6=\frac48\Rightarrow8x=24\Rightarrow\res{x=3}$."),
 (2, r"Las rectas que cortan dos secantes determinan en ellas estos segmentos. ¿Son paralelas?" + tasks(3, [r"2 y 3; \ 4 y 6", r"3 y 4; \ 4 y 5", r"1,5 y 2,5; \ 2,4 y 4"]),
     tasks(3, [r"$\frac23=\frac46$: \rest{sí}", r"$\frac34=0{,}75\neq\frac45=0{,}8$: \rest{no}", r"$\frac{1{,}5}{2{,}5}=0{,}6=\frac{2{,}4}{4}$: \rest{sí}"]) + r"(Recíproco del teorema de Tales.)"),
 (2, r"Tres parcelas están entre dos calles y sus lindes son paralelas. En la calle del Mar miden 15 m, 20 m y 25 m de fachada. En la calle Ancha, las tres juntas miden 72 m. ¿Cuánto mide la fachada de cada parcela en la calle Ancha?",
     r"$k=\frac{72}{15+20+25}=\frac{72}{60}=1{,}2$: \ $15\cdot1{,}2=\res{18\text{ m}}$, \ $20\cdot1{,}2=\res{24\text{ m}}$, \ $25\cdot1{,}2=\res{30\text{ m}}$."),
 (3, r"Unas rectas paralelas determinan $\overline{AB}=x$ y $\overline{BC}=x+4$ sobre una secante, y $\overline{A'B'}=3$ y $\overline{B'C'}=5$ sobre la otra. Calcula $x$.",
     r"$\frac{x}{x+4}=\frac35\Rightarrow5x=3x+12\Rightarrow\res{x=6}$ \ (y $\overline{BC}=10$)."),
 (3, r"Unas rectas paralelas determinan sobre una secante $\overline{AB}=5$ cm y $\overline{BC}=8$ cm. Sobre otra secante, $\overline{A'C'}=19{,}5$ cm. Calcula $\overline{A'B'}$ y $\overline{B'C'}$.",
     r"$\frac{\overline{A'B'}}{5}=\frac{\overline{A'C'}}{13}=\frac{19{,}5}{13}=1{,}5$: \ $\res{\overline{A'B'}=7{,}5\text{ cm}}$, \ $\res{\overline{B'C'}=12\text{ cm}}$."),
]))

# =====================================================================
# 3. Dividir un segment en parts iguals o proporcionals
# =====================================================================
ck(R(12, 5), 2.4); assert [30 * k // 5 for k in (2, 3)] == [12, 18] and [24 * k // 6 for k in (1, 2, 3)] == [4, 8, 12] and [45 * k // 9 for k in (2, 3, 4)] == [10, 15, 20]
assert [10 * k // 5 for k in (2, 3)] == [4, 6]; assert [35 * k // 7 for k in (2, 5)] == [10, 25]
ck(R(36, 10) / 8, 0.45); ck(R(36, 10) / 8 * 2, 0.9); ck(R(36, 10) / 8 * 5, 2.25)
assert 12 / 4 == 3 and 3 * 3 == 9 and 7 * 3 == 21
S_.append(("Dividir un segmento en partes iguales o proporcionales", [
 (1, r"Dibuja un segmento de 12 cm y divídelo en 5 partes iguales con regla y compás. ¿Cuánto mide cada parte?"
     + recorda(r"Desde un extremo, traza una semirrecta auxiliar y marca en ella con el compás tantos segmentos iguales como partes quieras. Une la última marca con el otro extremo y traza paralelas por las otras marcas. Para partes proporcionales a $2,\,3,\,4$, marca $2+3+4=9$ segmentos y traza las paralelas por las marcas 2 y 5."),
     r"Semirrecta desde $A$, 5 marcas iguales, unimos la quinta con $B$ y trazamos paralelas por las otras cuatro. Cada parte: $\frac{12}{5}=\res{2{,}4\text{ cm}}$."),
 (1, r"Calcula las partes en que queda dividido:" + tasks(1, [r"un segmento de 30 cm, en partes proporcionales a 2 y 3", r"un segmento de 24 cm, en partes proporcionales a 1, 2 y 3", r"un segmento de 45 cm, en partes proporcionales a 2, 3 y 4"]),
     tasks(1, [r"$\frac{30}{5}=6$: \ $\res{12\text{ cm y }18\text{ cm}}$", r"$\frac{24}{6}=4$: \ $\res{4,\ 8\text{ y }12\text{ cm}}$", r"$\frac{45}{9}=5$: \ $\res{10,\ 15\text{ y }20\text{ cm}}$"])),
 (2, r"Dibuja un segmento de 10 cm y divídelo, con regla y compás, en dos partes proporcionales a 2 y 3. Explica los pasos y comprueba el resultado calculando.",
     r"Semirrecta auxiliar, 5 marcas iguales, unimos la quinta con $B$ y trazamos la paralela por la marca 2. Partes: $\frac{10}{5}=2$, \ $\res{4\text{ cm y }6\text{ cm}}$."),
 (2, r"Un punto $P$ divide un segmento $AB$ de 35 cm de manera que $\frac{\overline{AP}}{\overline{PB}}=\frac25$. ¿Cuánto miden $\overline{AP}$ y $\overline{PB}$?",
     r"Partes proporcionales a 2 y 5: $\frac{35}{7}=5$; \ $\res{\overline{AP}=10\text{ cm}}$, \ $\res{\overline{PB}=25\text{ cm}}$."),
 (2, r"Cortamos una cuerda de 3,6 m en tres trozos proporcionales a 1, 2 y 5. ¿Cuánto mide cada trozo?",
     r"$\frac{3{,}6}{8}=0{,}45$: \ $\res{0{,}45\text{ m}}$, \ $\res{0{,}9\text{ m}}$ y $\res{2{,}25\text{ m}}$."),
 (3, r"Un punto $P$ divide un segmento $AB$ en dos partes que están en razón $\frac37$, y la parte larga mide 12 cm más que la corta. ¿Cuánto miden las dos partes y el segmento entero?",
     r"Partes $3u$ y $7u$: $7u-3u=12\Rightarrow u=3$. \ $\res{9\text{ cm}}$ y $\res{21\text{ cm}}$; \ $\overline{AB}=\res{30\text{ cm}}$."),
]))

# =====================================================================
# 4. Triangles en posició de Tales
# =====================================================================
ck(R(4 * 15, 10), 6); ck(R(3 * 12, 9), 4); ck(R(8) * R(75, 10) / 5, 12); ck(R(6 * 6, 4), 9)
ck(R(6 * 4, 9), R(24, 9)); ck(R(6) * R(72, 10) / 6 * 10 / 6, 12)  # AB'=6, AB=10, B'C'=7,2 → BC=12
assert prop(6, 4, 9, 6)
ck(R(18 * 4, 12), 6); ck(R(8 * 9, 6), 12); ck(R(5 * 9, 6), 7.5); ck(R(15 * 4, 5), 12)
assert sp.solve(10 * x - 4 * (x + 6), x) == [4]
FIG41 = tz(tpos(6, 6.5, 52, 0.4, labs={'AB1': '4', 'B1B': '6', 'BC': '15', 'B1C1': 'x'}, hot='B1C1'), 0.5)
FIG43 = tz(tpos(6, 6.5, 52, 0.6, labs={'AB1': '6', 'B1B': '4', 'AC1': '9', 'C1C': 'y', 'B1C1': '7,2', 'BC': 'x'}), 0.5)
BOW = tz([('poly', [(0, 0), (6, 0), (2.4, 3.2)], 'gf'), ('poly', [(2.4, 3.2), (6, 8), (-3, 8)], 'tr'),
          ('lab', (0, 0), '$A$', 'below left'), ('lab', (6, 0), '$B$', 'below right'), ('lab', (2.4, 3.2), '$C$', 'left=4pt'),
          ('lab', (-3, 8), '$D$', 'above left'), ('lab', (6, 8), '$E$', 'above right'),
          ('lab', (3, 0), '$8$', 'below'), ('lab', (1.2, 1.6), '$6$', 'left'), ('lab', (4.2, 1.6), '$5$', 'right'), ('lab', (1.5, 8), '$x$', 'above'), ('lab', (4.2, 5.6), '$9$', 'right'), ('lab', (-0.3, 5.6), '$y$', 'left')], 0.42)
S_.append(("Triángulos en posición de Tales", [
 (1, r"En la figura, $B'C'\parallel BC$. Calcula $x$." + fig(FIG41)
     + recorda(r"Si $B'C'\parallel BC$, los triángulos $AB'C'$ y $ABC$ están en \textbf{posición de Tales}: $\frac{\overline{AB'}}{\overline{AB}}=\frac{\overline{AC'}}{\overline{AC}}=\frac{\overline{B'C'}}{\overline{BC}}$. Para el lado paralelo, compara siempre \textbf{lados enteros} desde el vértice $A$."),
     r"$\overline{AB}=4+6=10$; \ $\frac{4}{10}=\frac{x}{15}\Rightarrow\res{x=6}$."),
 (1, r"En un triángulo $ABC$, $B'$ es un punto de $AB$ y $C'$ un punto de $AC$, con $B'C'\parallel BC$. Calcula:" + tasks(1, [r"$\overline{B'C'}$, si $\overline{AB'}=3$, $\overline{B'B}=6$ y $\overline{BC}=12$.", r"$\overline{BC}$, si $\overline{AB'}=5$, $\overline{AB}=8$ y $\overline{B'C'}=7{,}5$.", r"$\overline{BC}$, si $\overline{AC'}=4$, $\overline{C'C}=2$ y $\overline{B'C'}=6$."]),
     tasks(1, [r"$\frac39=\frac x{12}\Rightarrow\res{\overline{B'C'}=4}$", r"$\frac58=\frac{7{,}5}{x}\Rightarrow\res{\overline{BC}=12}$", r"$\frac46=\frac6x\Rightarrow\res{\overline{BC}=9}$"])),
 (2, r"En la figura, $B'C'\parallel BC$. Calcula $x$ y $y$." + fig(FIG43),
     r"$\overline{AB}=10$: \ $\frac{6}{10}=\frac{7{,}2}{x}\Rightarrow\res{x=12}$. \ Tales: $\frac64=\frac9y\Rightarrow\res{y=6}$."),
 (2, r"Un triángulo tiene 18 cm de base y 12 cm de altura. Trazamos una paralela a la base a 4 cm del vértice opuesto. ¿Cuánto mide el segmento de la paralela que queda dentro del triángulo?",
     r"El triángulo pequeño y el grande están en posición de Tales y las alturas también son proporcionales: $\frac{4}{12}=\frac{x}{18}\Rightarrow\res{x=6\text{ cm}}$."),
 (2, r"En la figura, $AB\parallel DE$. Calcula $x=\overline{DE}$ y $y=\overline{CD}$." + fig(BOW),
     r"Los triángulos $ABC$ y $DEC$ tienen el ángulo en $C$ igual (opuestos por el vértice) y $AB\parallel DE$: \ $\frac{\overline{CE}}{\overline{CA}}=\frac96=1{,}5$. \ $x=8\cdot1{,}5=\res{12}$, \ $y=5\cdot1{,}5=\res{7{,}5}$."),
 (3, r"Para medir la anchura de un río, Álex clava una estaca $B$ en la orilla, delante de un árbol $A$ de la otra orilla. Camina 15 m perpendicularmente a $AB$ hasta $C$, clava otra, continúa 5 m hasta $D$ y gira 90° alejándose del río hasta que ve $C$ y $A$ alineados, en el punto $E$, que está a 4 m de $D$. ¿Qué anchura tiene el río?",
     r"Los triángulos $ABC$ y $EDC$ son semejantes (ángulo en $C$ opuesto por el vértice y ángulos rectos en $B$ y $D$): \ $\frac{\overline{AB}}{4}=\frac{15}{5}\Rightarrow\res{\overline{AB}=12\text{ m}}$."),
 (3, r"En un triángulo $ABC$, $B'C'\parallel BC$, $\overline{B'B}=6$, $\overline{B'C'}=4$ y $\overline{BC}=10$. Calcula $x=\overline{AB'}$.",
     r"$\frac{x}{x+6}=\frac{4}{10}\Rightarrow10x=4x+24\Rightarrow\res{x=4}$."),
]))
# comprovacions de la figura papallona: C divideix AD i BE en raó 1,5
ck(R(9, 6), 1.5)

# =====================================================================
# 5. Figures semblants. Raó de semblança
# =====================================================================
assert R(6, 4) == R(9, 6) and R(4, 2) != R(8, 5) and R(6, 3) == R(8, 4)
assert [4 * R(5, 2), 6 * R(5, 2), 7 * R(5, 2)] == [10, 15, R(35, 2)] and [4 * R(2, 5), 6 * R(2, 5), 7 * R(2, 5)] == [R(8, 5), R(12, 5), R(14, 5)]
ck(R(27, 9), 3); ck(13 * 3, 39)
ck(20 * R(3, 2), 30); ck(R(275, 10) * R(9, 4), 61.875); ck(R(275, 10) * R(9, 4), 61.88, 2)
ck(S(R(72, 18)), 2); ck(R(600, 96), 6.25); ck(S(R(625, 100)), 2.5); ck(S(R(54, 6)), 3)
S_.append(("Figuras semejantes. Razón de semejanza", [
 (1, r"¿Son semejantes estas parejas de rectángulos? Si lo son, calcula la razón de semejanza." + tasks(2, [r"$4\times6$ \ y \ $6\times9$", r"$2\times5$ \ y \ $4\times8$", r"$3\times4$ \ y \ $6\times8$", r"un cuadrado de 3 cm y uno de 7 cm"])
     + recorda(r"Dos figuras son \textbf{semejantes} si tienen los ángulos iguales y los lados homólogos proporcionales. La \textbf{razón de semejanza} es $k=\frac{a'}{a}$. Los perímetros están en razón $k$ y las áreas en razón $k^2$."),
     tasks(2, [r"$\frac64=\frac96=1{,}5$: \rest{sí}, $k=1{,}5$", r"$\frac42=2\neq\frac85$: \rest{no}", r"$\frac63=\frac84=2$: \rest{sí}, $k=2$", r"\rest{sí} (todos los cuadrados lo son), $k=\frac73$"])),
 (1, r"Un triángulo tiene lados de 4, 6 y 7 cm. Calcula los lados de un triángulo semejante con razón: \ a) $k=2{,}5$; \ b) $k=0{,}4$.",
     r"a) $\res{10,\ 15\text{ y }17{,}5\text{ cm}}$. \quad b) $\res{1{,}6,\ 2{,}4\text{ y }2{,}8\text{ cm}}$."),
 (2, r"Una foto de 9 cm × 13 cm se amplía hasta que el lado pequeño mide 27 cm. ¿Cuánto mide el lado grande? ¿Cuántas veces mayor es el área?",
     r"$k=\frac{27}{9}=3$; \ lado grande $13\cdot3=\res{39\text{ cm}}$; \ el área se multiplica por $k^2=\res{9}$."),
 (2, r"Dos pentágonos son semejantes con razón $k=1{,}5$. El pequeño tiene 20 cm de perímetro y 27,5 cm² de área. Calcula el perímetro y el área del grande.",
     r"$P'=20\cdot1{,}5=\res{30\text{ cm}}$; \ $A'=27{,}5\cdot1{,}5^2=27{,}5\cdot2{,}25\approx\res{61{,}88\text{ cm}^2}$."),
 (2, r"Dos figuras semejantes tienen áreas de 18 cm² y 72 cm². ¿Cuál es la razón de semejanza? Si el perímetro de la pequeña es 16 cm, ¿cuál es el de la grande?",
     r"$k^2=\frac{72}{18}=4\Rightarrow\res{k=2}$; \ $P'=16\cdot2=\res{32\text{ cm}}$."),
 (3, r"Tenemos un rectángulo de 8 cm × 12 cm y queremos dibujar uno semejante con un área de 600 cm². ¿Qué dimensiones tiene que tener?",
     r"$A=96$; \ $k^2=\frac{600}{96}=6{,}25\Rightarrow k=2{,}5$. \ Dimensions: $\res{20\text{ cm}\times30\text{ cm}}$."),
 (3, r"Un triángulo rectángulo tiene catetos de 3 cm y 4 cm. Un triángulo semejante tiene 54 cm² de área. ¿Cuánto miden sus lados?",
     r"Área del pequeño: $\frac{3\cdot4}{2}=6$; \ $k^2=\frac{54}{6}=9\Rightarrow k=3$. Hipotenusa del pequeño: 5. \ Lados: $\res{9,\ 12\text{ y }15\text{ cm}}$."),
]))

# =====================================================================
# 6. Criteris de semblança de triangles
# =====================================================================
assert sim((2, 3, 4), (6, 9, 12)) == 3 and sim((3, 4, 6), (6, 8, 10)) is None and sim((5, 5, 8), (7.5, 7.5, 12)) == R(3, 2) and sim((4, 6, 9), (6, 9, 12)) is None
assert sorted([35, 75, 70]) == sorted([75, 70, 180 - 75 - 70]) and sorted([50, 60, 70]) != sorted([60, 80, 40])
assert R(6, 4) == R(9, 6); ck(5 * R(3, 2), 7.5); assert [6 * R(3, 2), 8 * R(3, 2), 10 * R(3, 2)] == [9, 12, 15]
assert (180 - 40) / 2 == 70
ck(R(6 * 8, 10), 4.8); ck(R(81, 15), 5.4); ck(15 - R(81, 15), 9.6); ck(R(9 * 12, 15), 7.2)
ck(R(9 * 8, 12), 6)
S_.append(("Criterios de semejanza de triángulos", [
 (1, r"¿Son semejantes los triángulos que tienen estos lados? Si lo son, da la razón de semejanza." + tasks(2, [r"2, 3, 4 \ y \ 6, 9, 12", r"3, 4, 6 \ y \ 6, 8, 10", r"5, 5, 8 \ y \ 7,5, 7,5, 12", r"4, 6, 9 \ y \ 6, 9, 12"])
     + recorda(r"Dos triángulos son semejantes si tienen: \textbf{1)} dos ángulos iguales; \ o \textbf{2)} los tres lados proporcionales; \ o \textbf{3)} dos lados proporcionales y el ángulo comprendido igual. Para comparar lados, ordénalos de menor a mayor."),
     tasks(2, [r"\rest{sí}, $k=3$", r"\rest{no}: $\frac63=\frac84=2\neq\frac{10}{6}$", r"\rest{sí}, $k=1{,}5$", r"\rest{no}: $\frac64=\frac96=1{,}5\neq\frac{12}{9}$"])),
 (1, r"¿Son semejantes estos triángulos? Justifícalo." + tasks(1, [r"Uno tiene ángulos de 35° y 75°, y el otro, de 75° y 70°.", r"Uno tiene ángulos de 50° y 60°, y el otro, de 60° y 80°.", r"Dos triángulos rectángulos, uno con un ángulo de 30° y el otro con un ángulo de 60°."]),
     tasks(1, [r"El primero tiene 35°, 75°, 70°: \rest{sí} (criterio 1).", r"El primero tiene 50°, 60°, 70° y el segundo 60°, 80°, 40°: \rest{no}.", r"Los dos tienen 90°, 30° y 60°: \rest{sí}."])),
 (2, r"Los triángulos $ABC$ y $A'B'C'$ tienen $\hat A=\hat A'=50^\circ$, $\overline{AB}=4$, $\overline{AC}=6$, $\overline{A'B'}=6$ y $\overline{A'C'}=9$. ¿Son semejantes? Si $\overline{BC}=5$, ¿cuánto mide $\overline{B'C'}$?",
     r"$\frac64=\frac96=1{,}5$ y el ángulo comprendido es igual: \rest{sí} (criterio 3), $k=1{,}5$. \ $\overline{B'C'}=5\cdot1{,}5=\res{7{,}5}$."),
 (2, r"Un triángulo tiene lados de 6, 8 y 10 cm. El lado pequeño de un triángulo semejante mide 9 cm. Calcula los otros dos lados y la razón entre las áreas.",
     r"$k=\frac96=1{,}5$: \ lados $\res{12\text{ cm y }15\text{ cm}}$; \ razón de las áreas $k^2=\res{2{,}25}$."),
 (2, r"¿Son semejantes dos triángulos isósceles que tienen el ángulo desigual de 40°? ¿Y dos triángulos isósceles cualesquiera?",
     r"Los ángulos iguales miden $\frac{180-40}{2}=70^\circ$: los dos tienen 40°, 70°, 70°, y son \rest{semejantes}. Dos isósceles cualesquiera, \rest{no} necesariamente."),
 (2, r"Los catetos de un triángulo rectángulo miden 6 cm y 8 cm. Calcula la hipotenusa y, usando triángulos semejantes, la altura sobre la hipotenusa.",
     r"$a=\sqrt{36+64}=10$. La altura divide el triángulo en dos triángulos semejantes al grande: $\frac h8=\frac6{10}\Rightarrow\res{h=4{,}8\text{ cm}}$."),
 (3, r"Los catetos de un triángulo rectángulo $ABC$ (ángulo recto en $A$) miden $\overline{AB}=9$ cm y $\overline{AC}=12$ cm. La altura $AH$ divide la hipotenusa en dos segmentos. Calcula $\overline{BC}$, $\overline{BH}$, $\overline{HC}$ y $\overline{AH}$.",
     r"$\overline{BC}=\sqrt{81+144}=15$. Los triángulos $HBA$ y $ABC$ son semejantes (rectángulos con el ángulo $\hat B$ común): $\frac{\overline{BH}}{9}=\frac{9}{15}\Rightarrow\res{\overline{BH}=5{,}4}$; \ $\res{\overline{HC}=9{,}6}$; \ $\frac{\overline{AH}}{12}=\frac{9}{15}\Rightarrow\res{\overline{AH}=7{,}2}$ cm."),
 (3, r"En un trapecio $ABCD$ las bases miden $\overline{AB}=12$ cm y $\overline{CD}=8$ cm, y las diagonales se cortan en $O$. Si $\overline{AO}=9$ cm, ¿cuánto mide $\overline{OC}$?",
     r"Los triángulos $OAB$ y $OCD$ son semejantes (ángulos en $O$ opuestos por el vértice y $AB\parallel CD$): $\frac{\overline{OC}}{9}=\frac{8}{12}\Rightarrow\res{\overline{OC}=6\text{ cm}}$."),
]))

# =====================================================================
# 7. Aplicacions: altures i distàncies
# =====================================================================
ck(R(10) / R(125, 100), 8); ck(R(16, 10) * 18 / 24, 1.2); ck(R(18) * R(15, 10) / 2, 13.5); ck(R(30) * R(15, 10) / 2, 22.5)
s_ = sp.solve(R(16, 10) * (x + 3) - 5 * x, x)[0]; ck(s_, 1.41, 2); ck(s_, R(48, 34))
ck(R(15 * 4, 5), 12); ck(R(20) * 6 / 8, 15); ck(R(15, 10) + R(15, 10) / 3 * 10, 6.5)
SHD = tz(shadow(2, 2.5, 8, 10, '1 m', '$H$', '1,25 m', '10 m', hot='h2'), 0.32)
MIRT = tz([('seg', (-0.5, 0), (21, 0), 'axis'), ('seg', (0, 0), (0, 1.5), 'wall'), ('seg', (20, 0), (20, 13.5), 'wall'),
           ('seg', (0, 1.5), (2, 0), 'ray'), ('seg', (2, 0), (20, 13.5), 'ray'), ('dot', (2, 0)),
           ('lab', (0, 0.75), '$1{,}5$\\,m', 'left'), ('lab', (1, -1.6), '$2$\\,m', 'below'), ('lab', (11, -1.6), '$18$\\,m', 'below'), ('lab', (20, 6.75), '$H$', 'right'), ('lab', (2, 0), '$M$', 'below')], 0.26)
LAMP = tz([('seg', (-0.5, 0), (5.2, 0), 'axis'), ('seg', (0, 0), (0, 5), 'wall'), ('seg', (3, 0), (3, 1.6), 'wall'), ('seg', (0, 5), (3 + 48 / 34, 0), 'ray'), ('dot', (0, 5)),
           ('lab', (0, 2.5), '$5$\\,m', 'left'), ('lab', (3, 0.8), '$1{,}6$\\,m', 'left'), ('lab', (1.5, 0), '$3$\\,m', 'below'), ('lab', (3 + 24 / 34, 0), '$s$', 'below')], 0.55)
SIGHT = tz([('seg', (-0.5, 0), (10.8, 0), 'axis'), ('seg', (0, 0), (0, 1.5), 'wall'), ('seg', (3, 0), (3, 3), 'wall'), ('seg', (10, 0), (10, 6.5), 'wall'),
            ('seg', (0, 1.5), (10, 6.5), 'ray'), ('seg', (0, 1.5), (10, 1.5), 'ray'),
            ('lab', (0, 0.75), '$1{,}5$', 'left'), ('lab', (3, 1.5), '$3$\\,m', 'right'), ('lab', (1.5, 0), '$3$\\,m', 'below'), ('lab', (6.5, 0), '$7$\\,m', 'below'), ('lab', (10, 4), '$H$', 'right')], 0.45)
S_.append(("Aplicaciones: alturas y distancias", [
 (1, r"Un palo de 1 m proyecta una sombra de 1,25 m. En el mismo momento, un árbol proyecta una sombra de 10 m. ¿Qué altura tiene el árbol?" + fig(SHD)
     + recorda(r"Busca dos \textbf{triángulos semejantes} (rayos de sol paralelos, un espejo, una visual que pasa por dos puntos…) y escribe la proporción entre lados homólogos: $\frac{\text{altura}}{\text{sombra}}=\frac{\text{altura}'}{\text{sombra}'}$."),
     r"$\frac{H}{10}=\frac{1}{1{,}25}\Rightarrow\res{H=8\text{ m}}$."),
 (1, r"Un edificio de 24 m proyecta una sombra de 18 m. ¿Qué sombra proyecta, en el mismo momento, una persona de 1,6 m?",
     r"$\frac{s}{1{,}6}=\frac{18}{24}\Rightarrow\res{s=1{,}2\text{ m}}$."),
 (2, r"Marta tiene los ojos a 1,5 m del suelo. Pone un espejo $M$ en el suelo a 2 m de ella y ve reflejada la punta de una torre que está a 18 m del espejo. ¿Qué altura tiene la torre?" + fig(MIRT),
     r"Los dos triángulos son semejantes: $\frac{H}{18}=\frac{1{,}5}{2}\Rightarrow\res{H=13{,}5\text{ m}}$."),
 (2, r"Tales midió la gran pirámide con las sombras. Si en un momento un bastón de 2 m proyecta una sombra de 2 m y la sombra de la pirámide, contada desde el centro de la base, mide 146 m, ¿qué altura tiene la pirámide?",
     r"$\frac{H}{146}=\frac22=1\Rightarrow\res{H=146\text{ m}}$ (en aquel momento, la altura y la sombra son iguales)."),
 (2, r"Una estaca de 1,5 m está clavada a 2 m de un punto $P$ del suelo. Desde $P$, la punta de la estaca y la punta de una torre que está a 30 m de $P$ quedan alineadas. ¿Qué altura tiene la torre?",
     r"Triángulos en posición de Tales: $\frac{H}{30}=\frac{1{,}5}{2}\Rightarrow\res{H=22{,}5\text{ m}}$."),
 (3, r"Una persona de 1,6 m está a 3 m de una farola de 5 m de altura. ¿Cuánto mide su sombra?" + fig(LAMP),
     r"$\frac{1{,}6}{s}=\frac{5}{s+3}\Rightarrow1{,}6s+4{,}8=5s\Rightarrow s=\frac{4{,}8}{3{,}4}\approx\res{1{,}41\text{ m}}$."),
 (3, r"Para medir la anchura $\overline{AB}$ de un río, desde $B$ (delante de un árbol $A$ de la otra orilla) caminamos 20 m perpendicularmente a $AB$ hasta $C$ y 8 m más hasta $D$. Desde $D$ nos alejamos del río, perpendicularmente, hasta el punto $E$ desde donde vemos $C$ y $A$ alineados. Si $\overline{DE}=6$ m, ¿qué anchura tiene el río?",
     r"Los triángulos $ABC$ y $EDC$ son semejantes (ángulos rectos en $B$ y $D$ y ángulos en $C$ opuestos por el vértice): $\frac{\overline{AB}}{6}=\frac{20}{8}\Rightarrow\res{\overline{AB}=15\text{ m}}$."),
 (3, r"Una persona con los ojos a 1,5 m del suelo está a 3 m de una tapia de 3 m. Ve la parte de arriba de la tapia alineada con la parte de arriba de un edificio que está 7 m detrás de la tapia. ¿Qué altura tiene el edificio?" + fig(SIGHT),
     r"Trazando la horizontal de los ojos quedan dos triángulos en posición de Tales: $\frac{H-1{,}5}{10}=\frac{3-1{,}5}{3}=0{,}5\Rightarrow H-1{,}5=5\Rightarrow\res{H=6{,}5\text{ m}}$."),
]))

# =====================================================================
# 8. Escales. Àrees i volums de figures semblants
# =====================================================================
ck(R(8 * 50, 100), 4); ck(R(6 * 25000, 100000), 1.5); ck(R(35, 10) * 200000 / 100000, 7)
ck(R(1200, 100), 12); ck(R(45 * 100000, 1500000), 3)
ck(R(200000, 5), 40000); ck(R(15000, 3), 5000)
ck(3 * 200 / R(100), 6); ck(R(25, 10) * 200 / 100, 5); ck(R(75, 10) * 200 ** 2 / 10 ** 4, 30)
ck(R(50000, 2), 25000); ck(R(7) * 25000 / 100000, 1.75)
ck(R(450, 18), 25); ck(40 * 18 ** 2, 12960); ck(R(12960, 10000), 1.30, 2)
ck(R(25, 100) * 8, 2); ck(60 * 4, 240)
ck(6 * R(1, 2) ** 2, 1.5)
S_.append(("Escalas. Áreas y volúmenes de figuras semejantes", [
 (1, r"Calcula la distancia real:" + tasks(3, [r"8 cm en un plano 1:50", r"6 cm en un mapa 1:25\,000", r"3,5 cm en un mapa 1:200\,000"])
     + recorda(r"Escala $1:n$: 1 cm del plano son $n$ cm reales. \ Real $=$ plano $\times\,n$; \ plano $=$ real $:\,n$. Si la razón de semejanza es $k$, las áreas se multiplican por $k^2$ y los volúmenes por $k^3$."),
     tasks(3, [r"$400\text{ cm}=\res{4\text{ m}}$", r"$150\,000\text{ cm}=\res{1{,}5\text{ km}}$", r"$700\,000\text{ cm}=\res{7\text{ km}}$"])),
 (1, r"¿Qué longitud tendrá en el plano? \ a) Una pared de 12 m, en un plano 1:100. \ b) Una carretera de 45 km, en un mapa 1:1\,500\,000.",
     r"a) $1200:100=\res{12\text{ cm}}$. \quad b) $4\,500\,000:1\,500\,000=\res{3\text{ cm}}$."),
 (2, r"Calcula la escala: \ a) 5 cm del mapa representan 2 km; \ b) 3 cm del plano representan 150 m.",
     r"a) $2\text{ km}=200\,000$ cm; \ $\frac{5}{200\,000}=\frac{1}{40\,000}$: \ $\res{1:40\,000}$. \quad b) $\frac{3}{15\,000}$: \ $\res{1:5000}$."),
 (2, r"En el plano de un piso a escala 1:200, el comedor mide 3 cm × 2,5 cm. Calcula sus dimensiones reales y su superficie.",
     r"$3\cdot200=600$ cm $=6$ m; \ $2{,}5\cdot200=500$ cm $=5$ m. \ $\res{6\text{ m}\times5\text{ m}}$, \ $A=\res{30\text{ m}^2}$."),
 (2, r"La escala gráfica de un mapa indica que 2 cm son 500 m. ¿Cuál es la escala numérica? ¿Qué distancia real hay entre dos puntos que están a 7 cm en el mapa?",
     r"$500\text{ m}=50\,000$ cm; \ $\frac{2}{50\,000}=\frac{1}{25\,000}$: \ $\res{1:25\,000}$. \ $7\cdot25\,000=175\,000$ cm $=\res{1{,}75\text{ km}}$."),
 (2, r"Una maqueta de un coche está hecha a escala 1:18. Si el coche real mide 4,5 m, ¿cuánto mide la maqueta? El parabrisas de la maqueta tiene 40 cm². ¿Qué superficie tiene el real?",
     r"$450:18=\res{25\text{ cm}}$. \ $A=40\cdot18^2=40\cdot324=12\,960\text{ cm}^2\approx\res{1{,}30\text{ m}^2}$."),
 (3, r"Dos botellas semejantes miden 15 cm y 30 cm de altura. La pequeña tiene una capacidad de 0,25 L y una etiqueta de 60 cm². ¿Qué capacidad tiene la grande? ¿Y qué superficie tiene su etiqueta?",
     r"$k=2$: \ capacitat $0{,}25\cdot2^3=\res{2\text{ L}}$; \ etiqueta $60\cdot2^2=\res{240\text{ cm}^2}$."),
 (3, r"En un mapa a escala 1:50\,000, un bosque ocupa 6 cm². ¿Qué superficie real tiene, en km² y en hectáreas?",
     r"1 cm del mapa son $50\,000$ cm $=0{,}5$ km; \ 1 cm² son $0{,}5\cdot0{,}5=0{,}25$ km². \ $6\cdot0{,}25=\res{1{,}5\text{ km}^2}=\res{150\text{ ha}}$."),
]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = "pdfkeywords={raó, proporció, segments proporcionals, teorema de Tales, posició de Tales, semblança, raó de semblança, criteris de semblança, escala}"
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TITOL = 'Proporcionalitat. Teorema de Tales'
NU = 10

pre = pre_

def build(sol_):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, ASSIGNATURA
    t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 10: Proporcionalidad. Teorema de Tales' % t, capcalera='%s · Unidad 10: Proporcionalidad. Teorema de Tales' % t,
                 pdfkeywords='razón, proporción, segmentos proporcionales, teorema de Tales, posición de Tales, semejanza, razón de semejanza, criterios de semejanza, escala')
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

''' + ASSIGNATURA + '{' + ('Soluciones de la ficha · Unidad 10' if sol_ else 'Ficha de ejercicios · Unidad 10') + '}{Proporcionalidad. Teorema de Tales}\n')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás una calculadora de proporciones y herramientas para practicar el teorema de Tales, la semejanza y las escalas. Los resultados aproximados están redondeados a las centésimas."
             if sol_ else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos y haz un dibujo de cada situación. Escribe la proporción antes de calcular y, si un resultado no es exacto, redondéalo a las centésimas.") + r'''
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
    name = 't10-fitxa-solucions-es.tex' if sol_ else 't10-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
