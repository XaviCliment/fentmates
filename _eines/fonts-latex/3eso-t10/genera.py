# Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (3r ESO, Unitat 10: Proporcionalitat. Teorema de Tales)
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
S_.append(("Raons i proporcions entre segments", [
 (1, r"Calcula la raó entre els segments (si no és exacta, arrodoneix a les centèsimes):" + tasks(4, [r"12 cm i 8 cm", r"5 cm i 20 cm", r"0,6 m i 45 cm", r"2 dm i 25 cm"])
     + recorda(r"La \textbf{raó} de dos segments és el quocient de les seues longituds, mesurades amb la \textbf{mateixa unitat}. Quatre segments són \textbf{proporcionals} si $\frac ab=\frac cd$, és a dir, si $a\cdot d=b\cdot c$ (producte dels extrems = producte dels mitjans)."),
     tasks(4, [r"$\frac{12}{8}=\res{1{,}5}$", r"$\frac{5}{20}=\res{0{,}25}$", r"$\frac{60}{45}\approx\res{1{,}33}$", r"$\frac{20}{25}=\res{0{,}8}$"])),
 (1, r"Calcula $x$ en cada proporció:" + tasks(3, [r"$\dfrac35=\dfrac{x}{20}$", r"$\dfrac8x=\dfrac27$", r"$\dfrac x4=\dfrac{15}{6}$", r"$\dfrac{2{,}5}{x}=\dfrac58$", r"$\dfrac69=\dfrac{10}{x}$", r"$\dfrac{x}{12}=\dfrac{0{,}75}{3}$"]),
     tasks(3, [r"$5x=60\Rightarrow\res{x=12}$", r"$2x=56\Rightarrow\res{x=28}$", r"$6x=60\Rightarrow\res{x=10}$", r"$5x=20\Rightarrow\res{x=4}$", r"$6x=90\Rightarrow\res{x=15}$", r"$3x=9\Rightarrow\res{x=3}$"])),
 (1, r"Són proporcionals, en aquest ordre, els segments següents?" + tasks(2, [r"2, 3, 4 i 6 cm", r"3, 5, 6 i 9 cm", r"1,5, 2, 4,5 i 6 cm", r"4, 7, 8 i 15 cm"]),
     tasks(2, [r"$2\cdot6=3\cdot4=12$: \rest{sí}", r"$3\cdot9=27\neq5\cdot6=30$: \rest{no}", r"$1{,}5\cdot6=2\cdot4{,}5=9$: \rest{sí}", r"$4\cdot15=60\neq7\cdot8=56$: \rest{no}"])),
 (2, r"Calcula el quart proporcional dels segments: \ a) 4, 6 i 10 cm; \ b) 2,5, 3 i 7 cm.",
     r"a) $\frac46=\frac{10}{x}\Rightarrow x=\frac{6\cdot10}{4}=\res{15\text{ cm}}$. \quad b) $\frac{2{,}5}{3}=\frac{7}{x}\Rightarrow x=\frac{3\cdot7}{2{,}5}=\res{8{,}4\text{ cm}}$."),
 (2, r"Dos segments estan en raó $\frac35$. Si el menut fa 12 cm, quant fa el gran?",
     r"$\frac35=\frac{12}{x}\Rightarrow3x=60\Rightarrow\res{x=20\text{ cm}}$."),
 (2, r"Dos segments sumen 56 cm i estan en raó $\frac34$. Quant fa cadascun?",
     r"Són $3u$ i $4u$: $7u=56\Rightarrow u=8$. Segments de $\res{24\text{ cm}}$ i $\res{32\text{ cm}}$."),
 (3, r"El \textbf{mitjà proporcional} de $a$ i $b$ és el segment $x$ tal que $\frac ax=\frac xb$. Calcula el mitjà proporcional de: \ a) 4 i 25; \ b) 2 i 8; \ c) 3 i 6 (arrodoneix a les centèsimes).",
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
 (1, r"Les rectes \textcolor{navy}{blau fosc} són paral·leles. Calcula $x$." + fig(tz(tales(2, 3, ar=55, as_=82, p=3.6, labs={'AB': '4', 'BC': '6', 'A1B1': '6', 'B1C1': 'x'}, hot='B1C1'), 0.55))
     + recorda(r"\textbf{Teorema de Tales:} si unes rectes paral·leles tallen dues secants, els segments que determinen sobre una són proporcionals als de l'altra: $\frac{\overline{AB}}{\overline{BC}}=\frac{\overline{A'B'}}{\overline{B'C'}}$, o bé $\frac{\overline{AB}}{\overline{A'B'}}=\frac{\overline{BC}}{\overline{B'C'}}=\frac{\overline{AC}}{\overline{A'C'}}$."),
     r"$\frac46=\frac6x\Rightarrow4x=36\Rightarrow\res{x=9}$."),
 (1, r"Les rectes $r$, $s$ i $t$ són paral·leles i tallen les secants en $A,\,B,\,C$ i $A',\,B',\,C'$. Calcula el segment que falta:"
     + tasks(1, [r"$\overline{AB}=3$, $\overline{BC}=5$, $\overline{A'B'}=4{,}8$. Calcula $\overline{B'C'}$.", r"$\overline{AB}=6$, $\overline{A'B'}=4$, $\overline{B'C'}=5$. Calcula $\overline{BC}$.", r"$\overline{AB}=4$, $\overline{AC}=10$, $\overline{A'C'}=15$. Calcula $\overline{A'B'}$."]),
     tasks(1, [r"$\frac35=\frac{4{,}8}{x}\Rightarrow\res{\overline{B'C'}=8}$", r"$\frac64=\frac{x}{5}\Rightarrow\res{\overline{BC}=7{,}5}$", r"$\frac{4}{10}=\frac{x}{15}\Rightarrow\res{\overline{A'B'}=6}$"])),
 (2, r"Les rectes \textcolor{navy}{blau fosc} són paral·leles. Calcula $x$." + fig(tz(tales(1.6, 3.2, ar=55, as_=82, p=3.6, labs={'AB': 'x', 'BC': '6', 'A1B1': '4', 'B1C1': '8'}, hot='AB'), 0.55)),
     r"$\frac x6=\frac48\Rightarrow8x=24\Rightarrow\res{x=3}$."),
 (2, r"Les rectes que tallen dues secants hi determinen aquests segments. Són paral·leles?" + tasks(3, [r"2 i 3; \ 4 i 6", r"3 i 4; \ 4 i 5", r"1,5 i 2,5; \ 2,4 i 4"]),
     tasks(3, [r"$\frac23=\frac46$: \rest{sí}", r"$\frac34=0{,}75\neq\frac45=0{,}8$: \rest{no}", r"$\frac{1{,}5}{2{,}5}=0{,}6=\frac{2{,}4}{4}$: \rest{sí}"]) + r"(Recíproc del teorema de Tales.)"),
 (2, r"Tres parcel·les estan entre dos carrers i les seues partions són paral·leles. Al carrer de la Mar fan 15 m, 20 m i 25 m de façana. Al carrer Ample, les tres juntes fan 72 m. Quant fa la façana de cada parcel·la al carrer Ample?",
     r"$k=\frac{72}{15+20+25}=\frac{72}{60}=1{,}2$: \ $15\cdot1{,}2=\res{18\text{ m}}$, \ $20\cdot1{,}2=\res{24\text{ m}}$, \ $25\cdot1{,}2=\res{30\text{ m}}$."),
 (3, r"Unes rectes paral·leles determinen $\overline{AB}=x$ i $\overline{BC}=x+4$ sobre una secant, i $\overline{A'B'}=3$ i $\overline{B'C'}=5$ sobre l'altra. Calcula $x$.",
     r"$\frac{x}{x+4}=\frac35\Rightarrow5x=3x+12\Rightarrow\res{x=6}$ \ (i $\overline{BC}=10$)."),
 (3, r"Unes rectes paral·leles determinen sobre una secant $\overline{AB}=5$ cm i $\overline{BC}=8$ cm. Sobre una altra secant, $\overline{A'C'}=19{,}5$ cm. Calcula $\overline{A'B'}$ i $\overline{B'C'}$.",
     r"$\frac{\overline{A'B'}}{5}=\frac{\overline{A'C'}}{13}=\frac{19{,}5}{13}=1{,}5$: \ $\res{\overline{A'B'}=7{,}5\text{ cm}}$, \ $\res{\overline{B'C'}=12\text{ cm}}$."),
]))

# =====================================================================
# 3. Dividir un segment en parts iguals o proporcionals
# =====================================================================
ck(R(12, 5), 2.4); assert [30 * k // 5 for k in (2, 3)] == [12, 18] and [24 * k // 6 for k in (1, 2, 3)] == [4, 8, 12] and [45 * k // 9 for k in (2, 3, 4)] == [10, 15, 20]
assert [10 * k // 5 for k in (2, 3)] == [4, 6]; assert [35 * k // 7 for k in (2, 5)] == [10, 25]
ck(R(36, 10) / 8, 0.45); ck(R(36, 10) / 8 * 2, 0.9); ck(R(36, 10) / 8 * 5, 2.25)
assert 12 / 4 == 3 and 3 * 3 == 9 and 7 * 3 == 21
S_.append(("Dividir un segment en parts iguals o proporcionals", [
 (1, r"Dibuixa un segment de 12 cm i divideix-lo en 5 parts iguals amb regle i compàs. Quant fa cada part?"
     + recorda(r"Des d'un extrem, traça una semirecta auxiliar i marca-hi amb el compàs tants segments iguals com parts vulgues. Uneix l'última marca amb l'altre extrem i traça paral·leles per les altres marques. Per a parts proporcionals a $2,\,3,\,4$, marca $2+3+4=9$ segments i traça les paral·leles per les marques 2 i 5."),
     r"Semirecta des d'$A$, 5 marques iguals, unim la cinquena amb $B$ i tracem paral·leles per les altres quatre. Cada part: $\frac{12}{5}=\res{2{,}4\text{ cm}}$."),
 (1, r"Calcula les parts en què queda dividit:" + tasks(1, [r"un segment de 30 cm, en parts proporcionals a 2 i 3", r"un segment de 24 cm, en parts proporcionals a 1, 2 i 3", r"un segment de 45 cm, en parts proporcionals a 2, 3 i 4"]),
     tasks(1, [r"$\frac{30}{5}=6$: \ $\res{12\text{ cm i }18\text{ cm}}$", r"$\frac{24}{6}=4$: \ $\res{4,\ 8\text{ i }12\text{ cm}}$", r"$\frac{45}{9}=5$: \ $\res{10,\ 15\text{ i }20\text{ cm}}$"])),
 (2, r"Dibuixa un segment de 10 cm i divideix-lo, amb regle i compàs, en dues parts proporcionals a 2 i 3. Explica els passos i comprova el resultat calculant.",
     r"Semirecta auxiliar, 5 marques iguals, unim la cinquena amb $B$ i tracem la paral·lela per la marca 2. Parts: $\frac{10}{5}=2$, \ $\res{4\text{ cm i }6\text{ cm}}$."),
 (2, r"Un punt $P$ divideix un segment $AB$ de 35 cm de manera que $\frac{\overline{AP}}{\overline{PB}}=\frac25$. Quant fan $\overline{AP}$ i $\overline{PB}$?",
     r"Parts proporcionals a 2 i 5: $\frac{35}{7}=5$; \ $\res{\overline{AP}=10\text{ cm}}$, \ $\res{\overline{PB}=25\text{ cm}}$."),
 (2, r"Tallem una corda de 3,6 m en tres trossos proporcionals a 1, 2 i 5. Quant fa cada tros?",
     r"$\frac{3{,}6}{8}=0{,}45$: \ $\res{0{,}45\text{ m}}$, \ $\res{0{,}9\text{ m}}$ i $\res{2{,}25\text{ m}}$."),
 (3, r"Un punt $P$ divideix un segment $AB$ en dues parts que estan en raó $\frac37$, i la part llarga fa 12 cm més que la curta. Quant fan les dues parts i el segment sencer?",
     r"Parts $3u$ i $7u$: $7u-3u=12\Rightarrow u=3$. \ $\res{9\text{ cm}}$ i $\res{21\text{ cm}}$; \ $\overline{AB}=\res{30\text{ cm}}$."),
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
S_.append(("Triangles en posició de Tales", [
 (1, r"En la figura, $B'C'\parallel BC$. Calcula $x$." + fig(FIG41)
     + recorda(r"Si $B'C'\parallel BC$, els triangles $AB'C'$ i $ABC$ estan en \textbf{posició de Tales}: $\frac{\overline{AB'}}{\overline{AB}}=\frac{\overline{AC'}}{\overline{AC}}=\frac{\overline{B'C'}}{\overline{BC}}$. Per al costat paral·lel, compara sempre \textbf{costats sencers} des del vèrtex $A$."),
     r"$\overline{AB}=4+6=10$; \ $\frac{4}{10}=\frac{x}{15}\Rightarrow\res{x=6}$."),
 (1, r"En un triangle $ABC$, $B'$ és un punt de $AB$ i $C'$ un punt de $AC$, amb $B'C'\parallel BC$. Calcula:" + tasks(1, [r"$\overline{B'C'}$, si $\overline{AB'}=3$, $\overline{B'B}=6$ i $\overline{BC}=12$.", r"$\overline{BC}$, si $\overline{AB'}=5$, $\overline{AB}=8$ i $\overline{B'C'}=7{,}5$.", r"$\overline{BC}$, si $\overline{AC'}=4$, $\overline{C'C}=2$ i $\overline{B'C'}=6$."]),
     tasks(1, [r"$\frac39=\frac x{12}\Rightarrow\res{\overline{B'C'}=4}$", r"$\frac58=\frac{7{,}5}{x}\Rightarrow\res{\overline{BC}=12}$", r"$\frac46=\frac6x\Rightarrow\res{\overline{BC}=9}$"])),
 (2, r"En la figura, $B'C'\parallel BC$. Calcula $x$ i $y$." + fig(FIG43),
     r"$\overline{AB}=10$: \ $\frac{6}{10}=\frac{7{,}2}{x}\Rightarrow\res{x=12}$. \ Tales: $\frac64=\frac9y\Rightarrow\res{y=6}$."),
 (2, r"Un triangle té 18 cm de base i 12 cm d'altura. Tracem una paral·lela a la base a 4 cm del vèrtex oposat. Quant mesura el segment de la paral·lela que queda dins del triangle?",
     r"El triangle menut i el gran estan en posició de Tales i les altures també són proporcionals: $\frac{4}{12}=\frac{x}{18}\Rightarrow\res{x=6\text{ cm}}$."),
 (2, r"En la figura, $AB\parallel DE$. Calcula $x=\overline{DE}$ i $y=\overline{CD}$." + fig(BOW),
     r"Els triangles $ABC$ i $DEC$ tenen l'angle en $C$ igual (oposats pel vèrtex) i $AB\parallel DE$: \ $\frac{\overline{CE}}{\overline{CA}}=\frac96=1{,}5$. \ $x=8\cdot1{,}5=\res{12}$, \ $y=5\cdot1{,}5=\res{7{,}5}$."),
 (3, r"Per a mesurar l'amplària d'un riu, l'Àlex clava una estaca $B$ a la vora, davant d'un arbre $A$ de l'altra riba. Camina 15 m perpendicularment a $AB$ fins a $C$, en clava una altra, continua 5 m fins a $D$ i gira 90° allunyant-se del riu fins que veu $C$ i $A$ alineats, en el punt $E$, que està a 4 m de $D$. Quina amplària té el riu?",
     r"Els triangles $ABC$ i $EDC$ són semblants (angle en $C$ oposat pel vèrtex i angles rectes en $B$ i $D$): \ $\frac{\overline{AB}}{4}=\frac{15}{5}\Rightarrow\res{\overline{AB}=12\text{ m}}$."),
 (3, r"En un triangle $ABC$, $B'C'\parallel BC$, $\overline{B'B}=6$, $\overline{B'C'}=4$ i $\overline{BC}=10$. Calcula $x=\overline{AB'}$.",
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
S_.append(("Figures semblants. Raó de semblança", [
 (1, r"Són semblants aquestes parelles de rectangles? Si ho són, calcula la raó de semblança." + tasks(2, [r"$4\times6$ \ i \ $6\times9$", r"$2\times5$ \ i \ $4\times8$", r"$3\times4$ \ i \ $6\times8$", r"un quadrat de 3 cm i un de 7 cm"])
     + recorda(r"Dues figures són \textbf{semblants} si tenen els angles iguals i els costats homòlegs proporcionals. La \textbf{raó de semblança} és $k=\frac{a'}{a}$. Els perímetres estan en raó $k$ i les àrees en raó $k^2$."),
     tasks(2, [r"$\frac64=\frac96=1{,}5$: \rest{sí}, $k=1{,}5$", r"$\frac42=2\neq\frac85$: \rest{no}", r"$\frac63=\frac84=2$: \rest{sí}, $k=2$", r"\rest{sí} (tots els quadrats ho són), $k=\frac73$"])),
 (1, r"Un triangle té costats de 4, 6 i 7 cm. Calcula els costats d'un triangle semblant amb raó: \ a) $k=2{,}5$; \ b) $k=0{,}4$.",
     r"a) $\res{10,\ 15\text{ i }17{,}5\text{ cm}}$. \quad b) $\res{1{,}6,\ 2{,}4\text{ i }2{,}8\text{ cm}}$."),
 (2, r"Una foto de 9 cm × 13 cm s'amplia fins que el costat menut fa 27 cm. Quant fa el costat gran? Quantes vegades més gran és l'àrea?",
     r"$k=\frac{27}{9}=3$; \ costat gran $13\cdot3=\res{39\text{ cm}}$; \ l'àrea es multiplica per $k^2=\res{9}$."),
 (2, r"Dos pentàgons són semblants amb raó $k=1{,}5$. El menut té 20 cm de perímetre i 27,5 cm² d'àrea. Calcula el perímetre i l'àrea del gran.",
     r"$P'=20\cdot1{,}5=\res{30\text{ cm}}$; \ $A'=27{,}5\cdot1{,}5^2=27{,}5\cdot2{,}25\approx\res{61{,}88\text{ cm}^2}$."),
 (2, r"Dues figures semblants tenen àrees de 18 cm² i 72 cm². Quina és la raó de semblança? Si el perímetre de la menuda és 16 cm, quin és el de la gran?",
     r"$k^2=\frac{72}{18}=4\Rightarrow\res{k=2}$; \ $P'=16\cdot2=\res{32\text{ cm}}$."),
 (3, r"Tenim un rectangle de 8 cm × 12 cm i en volem dibuixar un de semblant amb una àrea de 600 cm². Quines dimensions ha de tenir?",
     r"$A=96$; \ $k^2=\frac{600}{96}=6{,}25\Rightarrow k=2{,}5$. \ Dimensions: $\res{20\text{ cm}\times30\text{ cm}}$."),
 (3, r"Un triangle rectangle té catets de 3 cm i 4 cm. Un triangle semblant té 54 cm² d'àrea. Quant fan els seus costats?",
     r"Àrea del menut: $\frac{3\cdot4}{2}=6$; \ $k^2=\frac{54}{6}=9\Rightarrow k=3$. Hipotenusa del menut: 5. \ Costats: $\res{9,\ 12\text{ i }15\text{ cm}}$."),
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
S_.append(("Criteris de semblança de triangles", [
 (1, r"Són semblants els triangles que tenen aquests costats? Si ho són, dona la raó de semblança." + tasks(2, [r"2, 3, 4 \ i \ 6, 9, 12", r"3, 4, 6 \ i \ 6, 8, 10", r"5, 5, 8 \ i \ 7,5, 7,5, 12", r"4, 6, 9 \ i \ 6, 9, 12"])
     + recorda(r"Dos triangles són semblants si tenen: \textbf{1r)} dos angles iguals; \ o \textbf{2n)} els tres costats proporcionals; \ o \textbf{3r)} dos costats proporcionals i l'angle comprés igual. Per a comparar costats, ordena'ls de menor a major."),
     tasks(2, [r"\rest{sí}, $k=3$", r"\rest{no}: $\frac63=\frac84=2\neq\frac{10}{6}$", r"\rest{sí}, $k=1{,}5$", r"\rest{no}: $\frac64=\frac96=1{,}5\neq\frac{12}{9}$"])),
 (1, r"Són semblants aquests triangles? Justifica-ho." + tasks(1, [r"Un té angles de 35° i 75°, i l'altre, de 75° i 70°.", r"Un té angles de 50° i 60°, i l'altre, de 60° i 80°.", r"Dos triangles rectangles, l'un amb un angle de 30° i l'altre amb un angle de 60°."]),
     tasks(1, [r"El primer té 35°, 75°, 70°: \rest{sí} (criteri 1r).", r"El primer té 50°, 60°, 70° i el segon 60°, 80°, 40°: \rest{no}.", r"Tots dos tenen 90°, 30° i 60°: \rest{sí}."])),
 (2, r"Els triangles $ABC$ i $A'B'C'$ tenen $\hat A=\hat A'=50^\circ$, $\overline{AB}=4$, $\overline{AC}=6$, $\overline{A'B'}=6$ i $\overline{A'C'}=9$. Són semblants? Si $\overline{BC}=5$, quant fa $\overline{B'C'}$?",
     r"$\frac64=\frac96=1{,}5$ i l'angle comprés és igual: \rest{sí} (criteri 3r), $k=1{,}5$. \ $\overline{B'C'}=5\cdot1{,}5=\res{7{,}5}$."),
 (2, r"Un triangle té costats de 6, 8 i 10 cm. El costat menut d'un triangle semblant fa 9 cm. Calcula els altres dos costats i la raó entre les àrees.",
     r"$k=\frac96=1{,}5$: \ costats $\res{12\text{ cm i }15\text{ cm}}$; \ raó de les àrees $k^2=\res{2{,}25}$."),
 (2, r"Són semblants dos triangles isòsceles que tenen l'angle desigual de 40°? I dos triangles isòsceles qualssevol?",
     r"Els angles iguals fan $\frac{180-40}{2}=70^\circ$: tots dos tenen 40°, 70°, 70°, i són \rest{semblants}. Dos isòsceles qualssevol, \rest{no} necessàriament."),
 (2, r"Els catets d'un triangle rectangle fan 6 cm i 8 cm. Calcula la hipotenusa i, fent servir triangles semblants, l'altura sobre la hipotenusa.",
     r"$a=\sqrt{36+64}=10$. L'altura divideix el triangle en dos triangles semblants al gran: $\frac h8=\frac6{10}\Rightarrow\res{h=4{,}8\text{ cm}}$."),
 (3, r"Els catets d'un triangle rectangle $ABC$ (angle recte en $A$) fan $\overline{AB}=9$ cm i $\overline{AC}=12$ cm. L'altura $AH$ divideix la hipotenusa en dos segments. Calcula $\overline{BC}$, $\overline{BH}$, $\overline{HC}$ i $\overline{AH}$.",
     r"$\overline{BC}=\sqrt{81+144}=15$. Els triangles $HBA$ i $ABC$ són semblants (rectangles amb l'angle $\hat B$ comú): $\frac{\overline{BH}}{9}=\frac{9}{15}\Rightarrow\res{\overline{BH}=5{,}4}$; \ $\res{\overline{HC}=9{,}6}$; \ $\frac{\overline{AH}}{12}=\frac{9}{15}\Rightarrow\res{\overline{AH}=7{,}2}$ cm."),
 (3, r"En un trapezi $ABCD$ les bases fan $\overline{AB}=12$ cm i $\overline{CD}=8$ cm, i les diagonals es tallen en $O$. Si $\overline{AO}=9$ cm, quant fa $\overline{OC}$?",
     r"Els triangles $OAB$ i $OCD$ són semblants (angles en $O$ oposats pel vèrtex i $AB\parallel CD$): $\frac{\overline{OC}}{9}=\frac{8}{12}\Rightarrow\res{\overline{OC}=6\text{ cm}}$."),
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
S_.append(("Aplicacions: altures i distàncies", [
 (1, r"Un pal d'1 m fa una ombra d'1,25 m. Al mateix moment, un arbre fa una ombra de 10 m. Quina altura té l'arbre?" + fig(SHD)
     + recorda(r"Busca dos \textbf{triangles semblants} (rajos de sol paral·lels, un mirall, una visual que passa per dos punts…) i escriu la proporció entre costats homòlegs: $\frac{\text{altura}}{\text{ombra}}=\frac{\text{altura}'}{\text{ombra}'}$."),
     r"$\frac{H}{10}=\frac{1}{1{,}25}\Rightarrow\res{H=8\text{ m}}$."),
 (1, r"Un edifici de 24 m fa una ombra de 18 m. Quina ombra fa, al mateix moment, una persona d'1,6 m?",
     r"$\frac{s}{1{,}6}=\frac{18}{24}\Rightarrow\res{s=1{,}2\text{ m}}$."),
 (2, r"La Marta té els ulls a 1,5 m de terra. Posa un mirall $M$ a terra a 2 m d'ella i veu reflectida la punta d'una torre que està a 18 m del mirall. Quina altura té la torre?" + fig(MIRT),
     r"Els dos triangles són semblants: $\frac{H}{18}=\frac{1{,}5}{2}\Rightarrow\res{H=13{,}5\text{ m}}$."),
 (2, r"Tales va mesurar la gran piràmide amb les ombres. Si en un moment un bastó de 2 m fa una ombra de 2 m i l'ombra de la piràmide, comptada des del centre de la base, fa 146 m, quina altura té la piràmide?",
     r"$\frac{H}{146}=\frac22=1\Rightarrow\res{H=146\text{ m}}$ (en aquell moment, l'altura i l'ombra són iguals)."),
 (2, r"Una estaca d'1,5 m està clavada a 2 m d'un punt $P$ de terra. Des de $P$, la punta de l'estaca i la punta d'una torre que està a 30 m de $P$ queden alineades. Quina altura té la torre?",
     r"Triangles en posició de Tales: $\frac{H}{30}=\frac{1{,}5}{2}\Rightarrow\res{H=22{,}5\text{ m}}$."),
 (3, r"Una persona d'1,6 m està a 3 m d'un fanal de 5 m d'altura. Quant fa la seua ombra?" + fig(LAMP),
     r"$\frac{1{,}6}{s}=\frac{5}{s+3}\Rightarrow1{,}6s+4{,}8=5s\Rightarrow s=\frac{4{,}8}{3{,}4}\approx\res{1{,}41\text{ m}}$."),
 (3, r"Per a mesurar l'amplària $\overline{AB}$ d'un riu, des de $B$ (davant d'un arbre $A$ de l'altra riba) caminem 20 m perpendicularment a $AB$ fins a $C$ i 8 m més fins a $D$. Des de $D$ ens allunyem del riu, perpendicularment, fins al punt $E$ des d'on veiem $C$ i $A$ alineats. Si $\overline{DE}=6$ m, quina amplària té el riu?",
     r"Els triangles $ABC$ i $EDC$ són semblants (angles rectes en $B$ i $D$ i angles en $C$ oposats pel vèrtex): $\frac{\overline{AB}}{6}=\frac{20}{8}\Rightarrow\res{\overline{AB}=15\text{ m}}$."),
 (3, r"Una persona amb els ulls a 1,5 m de terra està a 3 m d'una tàpia de 3 m. Veu la part de dalt de la tàpia alineada amb la part de dalt d'un edifici que està 7 m darrere de la tàpia. Quina altura té l'edifici?" + fig(SIGHT),
     r"Traçant l'horitzontal dels ulls queden dos triangles en posició de Tales: $\frac{H-1{,}5}{10}=\frac{3-1{,}5}{3}=0{,}5\Rightarrow H-1{,}5=5\Rightarrow\res{H=6{,}5\text{ m}}$."),
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
S_.append(("Escales. Àrees i volums de figures semblants", [
 (1, r"Calcula la distància real:" + tasks(3, [r"8 cm en un plànol 1:50", r"6 cm en un mapa 1:25\,000", r"3,5 cm en un mapa 1:200\,000"])
     + recorda(r"Escala $1:n$: 1 cm del plànol són $n$ cm reals. \ Real $=$ plànol $\times\,n$; \ plànol $=$ real $:\,n$. Si la raó de semblança és $k$, les àrees es multipliquen per $k^2$ i els volums per $k^3$."),
     tasks(3, [r"$400\text{ cm}=\res{4\text{ m}}$", r"$150\,000\text{ cm}=\res{1{,}5\text{ km}}$", r"$700\,000\text{ cm}=\res{7\text{ km}}$"])),
 (1, r"Quina longitud tindrà en el plànol? \ a) Una paret de 12 m, en un plànol 1:100. \ b) Una carretera de 45 km, en un mapa 1:1\,500\,000.",
     r"a) $1200:100=\res{12\text{ cm}}$. \quad b) $4\,500\,000:1\,500\,000=\res{3\text{ cm}}$."),
 (2, r"Calcula l'escala: \ a) 5 cm del mapa representen 2 km; \ b) 3 cm del plànol representen 150 m.",
     r"a) $2\text{ km}=200\,000$ cm; \ $\frac{5}{200\,000}=\frac{1}{40\,000}$: \ $\res{1:40\,000}$. \quad b) $\frac{3}{15\,000}$: \ $\res{1:5000}$."),
 (2, r"En el plànol d'un pis a escala 1:200, el menjador fa 3 cm × 2,5 cm. Calcula'n les dimensions reals i la superfície.",
     r"$3\cdot200=600$ cm $=6$ m; \ $2{,}5\cdot200=500$ cm $=5$ m. \ $\res{6\text{ m}\times5\text{ m}}$, \ $A=\res{30\text{ m}^2}$."),
 (2, r"L'escala gràfica d'un mapa indica que 2 cm són 500 m. Quina és l'escala numèrica? Quina distància real hi ha entre dos punts que estan a 7 cm en el mapa?",
     r"$500\text{ m}=50\,000$ cm; \ $\frac{2}{50\,000}=\frac{1}{25\,000}$: \ $\res{1:25\,000}$. \ $7\cdot25\,000=175\,000$ cm $=\res{1{,}75\text{ km}}$."),
 (2, r"Una maqueta d'un cotxe està feta a escala 1:18. Si el cotxe real fa 4,5 m, quant fa la maqueta? El parabrisa de la maqueta té 40 cm². Quina superfície té el real?",
     r"$450:18=\res{25\text{ cm}}$. \ $A=40\cdot18^2=40\cdot324=12\,960\text{ cm}^2\approx\res{1{,}30\text{ m}^2}$."),
 (3, r"Dues botelles semblants fan 15 cm i 30 cm d'altura. La menuda té una capacitat de 0,25 L i una etiqueta de 60 cm². Quina capacitat té la gran? I quina superfície té la seua etiqueta?",
     r"$k=2$: \ capacitat $0{,}25\cdot2^3=\res{2\text{ L}}$; \ etiqueta $60\cdot2^2=\res{240\text{ cm}^2}$."),
 (3, r"En un mapa a escala 1:50\,000, un bosc ocupa 6 cm². Quina superfície real té, en km² i en hectàrees?",
     r"1 cm del mapa són $50\,000$ cm $=0{,}5$ km; \ 1 cm² són $0{,}5\cdot0{,}5=0{,}25$ km². \ $6\cdot0{,}25=\res{1{,}5\text{ km}^2}=\res{150\text{ ha}}$."),
]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n'
KW = "pdfkeywords={raó, proporció, segments proporcionals, teorema de Tales, posició de Tales, semblança, raó de semblança, criteris de semblança, escala}"
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
TITOL = 'Proporcionalitat. Teorema de Tales'
NU = 10

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
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs una calculadora de proporcions i eines per a practicar el teorema de Tales, la semblança i les escales. Els resultats aproximats estan arrodonits a les centèsimes."
             if sol_ else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos i fes un dibuix de cada situació. Escriu la proporció abans de calcular i, si un resultat no és exacte, arrodoneix-lo a les centèsimes.") + r'''
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
