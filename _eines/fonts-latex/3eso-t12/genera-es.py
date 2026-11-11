# Versió en castellà de genera.py. Genera t12-fitxa-exercicis.tex i t12-fitxa-solucions.tex (3r ESO, Unitat 12: Probabilitat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Cada probabilitat es calcula amb fraccions exactes (Fraction) i es comprova amb ck() abans d'escriure-la.
import os, re
from fractions import Fraction as Fr
from itertools import product, permutations
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- comprovacions ----------
def ck(v, w):
    """v: valor calculat; w: el que escrivim (Fraction, enter o text decimal amb coma)"""
    if isinstance(w, str): w = Fr(w.replace(',', '.'))
    assert Fr(v) == Fr(w), (v, w)
def lap(E, f):
    """probabilitat per Laplace d'un espai mostral (llista) i una condició"""
    return Fr(sum(1 for e in E if f(e)), len(E))
def fr(f):
    f = Fr(f)
    return str(f.numerator) if f.denominator == 1 else r'\frac{%d}{%d}' % (f.numerator, f.denominator)
def fs(n, d):
    """n/d i, si es pot, simplificada"""
    f = Fr(n, d); s = r'\frac{%d}{%d}' % (n, d)
    return s if (f.numerator, f.denominator) == (n, d) else s + '=' + fr(f)
def st(xs): return r'\{' + ',\\,'.join(str(x) for x in xs) + r'\}' if xs else r'\varnothing'
D6 = range(1, 7)
DD = list(product(D6, D6))
def isprime(n): return n > 1 and all(n % k for k in range(2, int(n ** .5) + 1))

# ---------- figures (TikZ) ----------
BC = {'R': 'red!75!black', 'B': 'blue!70!black', 'A': 'blue!70!black', 'V': 'teal', 'G': 'yellow!80!orange', 'N': 'black!80', 'W': 'white'}
def tree(kids, ld=17, sd=(16, 8, 4.5), font=r'\small'):
    """diagrama d'arbre cap a la dreta. kids = [(etiqueta, prob, fills, text final)]; etiqueta 'R*' = boleta de color"""
    def node(lab, end):
        sty = ''
        if lab.endswith('*'):
            lab = lab[:-1]; c = BC[lab[0]]
            sty = 'circle,fill=%s,text=%s,inner sep=1.2pt,minimum size=4.2mm,font=\\scriptsize\\bfseries' % (c, 'black' if lab[0] in 'GW' else 'white')
        if end: sty += (',' if sty else '') + 'label={[font=\\scriptsize,xshift=1mm]right:%s}' % end
        return 'node[%s] {%s}' % (sty, lab)
    def ch(ks, d):
        o = ''
        for i, k in enumerate(ks):
            pos = 'above' if i < len(ks) / 2 else 'below'
            if len(ks) % 2 == 1 and i == len(ks) // 2: pos = 'above'
            o += ' child {%s%s edge from parent node[%s,pos=.55,font=\\scriptsize,text=teal!70!black,inner sep=1.5pt] {%s}}' % (
                node(k[0], k[3] if len(k) > 3 else ''), ch(k[2], d + 1), pos, '$%s$' % k[1] if k[1] else '')
        return o
    lv = ','.join('level %d/.style={sibling distance=%smm}' % (i + 1, s) for i, s in enumerate(sd))
    return (r"\begin{tikzpicture}[grow'=right,level distance=%smm," r'%s,every node/.style={font=%s\bfseries},edge from parent/.style={draw=muted,thick}]' % (ld, lv, font)
            + '\n\\node[circle,fill=navy,inner sep=1.2pt] {}' + ch(kids, 1) + ';\n\\end{tikzpicture}')
def dtab(op, hit, sym='+'):
    """taula de doble entrada de dos daus amb les caselles favorables acolorides"""
    o = [r'{\small\renewcommand{\arraystretch}{1.15}\setlength{\tabcolsep}{4pt}\begin{tabular}{c|cccccc}', r'\rowcolor{soft} $%s$ & 1 & 2 & 3 & 4 & 5 & 6\\\hline' % sym]
    for a in D6:
        o.append(r'\cellcolor{soft}%d & ' % a + ' & '.join((r'\cellcolor{accent!30}\textbf{%d}' if hit(a, b) else '%d') % op(a, b) for b in D6) + r'\\')
    o.append(r'\end{tabular}}')
    return '\n'.join(o)
def bag(spec, per=6, s=0.42):
    """bossa amb boles: spec = 'RRRBB'"""
    n = len(spec); cols = min(per, n); rows = (n + cols - 1) // cols
    o = [r'\begin{tikzpicture}[x=%scm,y=%scm,baseline=(current bounding box.center)]' % (s, s)]
    o.append(r'\draw[muted,thick,fill=soft] (-0.2,0.1) -- (-0.2,%.2f) to[out=-90,in=180] (%.2f,%.2f) to[out=0,in=-90] (%.2f,%.2f) -- (%.2f,0.1);' % (-rows + 0.3, cols / 2, -rows - 0.3, cols + 0.2, -rows + 0.3, cols + 0.2))
    o.append(r'\draw[muted,line width=1.6pt,line cap=round] (-0.4,0.1) -- (%.2f,0.1);' % (cols + 0.4))
    for i, c in enumerate(spec):
        r, k = divmod(i, cols)
        o.append(r'\filldraw[draw=black!50,fill=%s] (%.2f,%.2f) circle (0.38);' % (BC[c], k + 0.5, -r - 0.45))
    o.append(r'\end{tikzpicture}')
    return '\n'.join(o)
def ctab(head, rows):
    return (r'{\small\renewcommand{\arraystretch}{1.2}\begin{tabular}{l|' + 'c' * (len(head) - 1) + r'}' + '\n\\rowcolor{soft} ' + ' & '.join(head) + r'\\\hline' + '\n'
            + '\n'.join(' & '.join(str(c) for c in r) + r'\\' for r in rows) + '\n\\end{tabular}}')
def cen(*xs, sep=r'\qquad '): return r'\par\smallskip\begin{center}' + sep.join(xs) + r'\end{center}'

S_ = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Experiments aleatoris. Espai mostral i esdeveniments
# =====================================================================
U12 = range(1, 13)
assert [x for x in U12 if x % 2 == 0] == [2, 4, 6, 8, 10, 12] and [x for x in U12 if x % 5 == 0] == [5, 10] and [x for x in U12 if 12 % x == 0] == [1, 2, 3, 4, 6, 12]
C2 = [a + b for a in 'CX' for b in 'CX']
assert [e for e in C2 if 'C' in e] == ['CC', 'CX', 'XC'] and [e for e in C2 if e[0] == e[1]] == ['CC', 'XX']
F3 = [a + b + c for a in 'OA' for b in 'OA' for c in 'OA']
assert len(F3) == 8 and [e for e in F3 if e.count('A') == 2] == ['OAA', 'AOA', 'AAO']
N3 = sorted(int(''.join(p)) for p in permutations('123'))
assert N3 == [123, 132, 213, 231, 312, 321] and [n for n in N3 if n % 2 == 0] == [132, 312] and [n for n in N3 if n > 200] == [213, 231, 312, 321]
assert [(a, b) for a, b in DD if a + b == 5] == [(1, 4), (2, 3), (3, 2), (4, 1)]
T2 = tree([('C', '', [('C', '', [], '$CC$'), ('X', '', [], '$CX$')]), ('X', '', [('C', '', [], '$XC$'), ('X', '', [], '$XX$')])], ld=14, sd=(13, 6.5))
T3 = tree([(a, '', [(b, '', [(c, '', [], '$%s$' % (a + b + c)) for c in 'OA']) for b in 'OA']) for a in 'OA'], ld=13, sd=(20, 10, 5))
S_.append(("Experimentos aleatorios. Espacio muestral y sucesos", [
 (1, r"Indica si son experimentos aleatorios o deterministas:" + tasks(2, [r"Lanzar un dado y anotar el resultado.", r"Medir la temperatura a la que hierve el agua al nivel del mar.", r"Sacar una carta de una baraja sin mirar.", r"Calcular cuánto pagaremos por 3 kg de manzanas a 2 €/kg.", r"Adivinar el número ganador de la lotería.", r"Dejar caer una pelota y mirar si cae al suelo."])
     + recorda(r"Un experimento es \textbf{aleatorio} si no podemos predecir su resultado, aunque lo repitamos en las mismas condiciones. El \textbf{espacio muestral} $E$ es el conjunto de todos los resultados posibles, y un \textbf{suceso} es un subconjunto de $E$."),
     tasks(2, [r"\rest{aleatorio}", r"\rest{determinista}", r"\rest{aleatorio}", r"\rest{determinista} (6 €)", r"\rest{aleatorio}", r"\rest{determinista}"])),
 (1, r"Escribe el espacio muestral de estos experimentos:" + tasks(2, [r"Lanzar una moneda.", r"Lanzar un dado de cuatro caras (tetraedro) numeradas del 1 al 4.", r"Girar una ruleta con 5 sectores iguales: rojo, azul, verde, amarillo y negro.", r"Sacar una bola de una bolsa con bolas rojas (R) y azules (A).", r"Elegir al azar un día de la semana.", r"Preguntar a alguien cuántas hermanas tiene (como máximo, 3)."]),
     tasks(2, [r"$E=\{C,\,X\}$", r"$E=\{1,\,2,\,3,\,4\}$", r"$E=\{\text{rojo},\,\text{azul},\,\text{verde},\,\text{amarillo},\,\text{negro}\}$", r"$E=\{R,\,A\}$", r"$E=\{\text{lu},\,\text{ma},\,\text{mi},\,\text{ju},\,\text{vi},\,\text{sá},\,\text{do}\}$", r"$E=\{0,\,1,\,2,\,3\}$"])),
 (1, r"Sacamos una bola de una urna con 12 bolas numeradas del 1 al 12. Escribe estos sucesos y di de qué tipo es cada uno (elemental, compuesto, seguro o imposible):" + tasks(3, [r"$A=$ «par»", r"$B=$ «múltiplo de 5»", r"$C=$ «mayor que 12»", r"$D=$ «divisor de 12»", r"$F=$ «menor que 13»", r"$G=$ «múltiplo de 11»"]),
     tasks(3, [r"$\{2,4,6,8,10,12\}$: \rest{compuesto}", r"$\{5,\,10\}$: \rest{compuesto}", r"$\varnothing$: \rest{imposible}", r"$\{1,2,3,4,6,12\}$: \rest{compuesto}", r"$E$: \rest{seguro}", r"$\{11\}$: \rest{elemental}"])),
 (2, r"Lanzamos dos monedas. Haz un diagrama de árbol y escribe el espacio muestral y los sucesos $A=$ «al menos una cara», $B=$ «ninguna cara» y $C=$ «las dos iguales».",
     cen(T2) + r"$E=\{CC,\,CX,\,XC,\,XX\}$; \quad $A=\res{\{CC,\,CX,\,XC\}}$, \quad $B=\res{\{XX\}}$, \quad $C=\res{\{CC,\,XX\}}$."),
 (2, r"Lanzamos una moneda y un dado. Haz una tabla de doble entrada con todos los resultados. ¿Cuántos hay? Escribe los sucesos «cara y número par» y «cruz y menor que 3».",
     cen(ctab(['', '1', '2', '3', '4', '5', '6'], [['$C$'] + ['$C%d$' % i for i in D6], ['$X$'] + ['$X%d$' % i for i in D6]]))
     + r"$2\cdot6=\res{12}$ resultados. \quad «Cara y par» $=\res{\{C2,\,C4,\,C6\}}$; \quad «cruz y menor que 3» $=\res{\{X1,\,X2\}}$."),
 (2, r"Una familia tiene tres hijos. Anotamos si cada uno es chica (A) o chico (O), por orden de nacimiento. Haz un diagrama de árbol, escribe el espacio muestral y el suceso «exactamente dos chicas».",
     cen(T3) + r"$E=\{OOO,\,OOA,\,OAO,\,OAA,\,AOO,\,AOA,\,AAO,\,AAA\}$ (8 resultados). \quad «Dos chicas» $=\res{\{OAA,\,AOA,\,AAO\}}$."),
 (3, r"Formamos números de tres cifras distintas con las cifras 1, 2 y 3. Escribe el espacio muestral y los sucesos «el número es par» y «el número es mayor que 200».",
     r"$E=\{123,\,132,\,213,\,231,\,312,\,321\}$. \quad «Par» $=\res{\{132,\,312\}}$; \quad «mayor que 200» $=\res{\{213,\,231,\,312,\,321\}}$."),
 (3, r"Lanzamos dos dados (uno rojo y uno azul). ¿Cuántos resultados tiene el espacio muestral? Escribe los sucesos «la suma es 5» y «sale el mismo número (doble)».",
     r"$6\cdot6=\res{36}$ resultados (pares ordenados). «Suma 5» $=\res{\{(1,4),\,(2,3),\,(3,2),\,(4,1)\}}$; «doble» $=\res{\{(1,1),\,(2,2),\,\dots,\,(6,6)\}}$ (6 resultados)."),
]))

# =====================================================================
# 2. Operacions amb esdeveniments
# =====================================================================
def ops(E, A, B):
    A, B = set(A), set(B)
    return (sorted(A | B), sorted(A & B), sorted(set(E) - A), sorted(set(E) - B))
assert ops(D6, [3, 6], [1, 2]) == ([1, 2, 3, 6], [], [1, 2, 4, 5], [3, 4, 5, 6])
U10 = range(1, 11); P10 = [x for x in U10 if x % 2 == 0]; Q10 = [x for x in U10 if isprime(x)]
assert ops(U10, P10, Q10) == ([2, 3, 4, 5, 6, 7, 8, 10], [2], [1, 3, 5, 7, 9], [1, 4, 6, 8, 9, 10])
assert ops(D6, [2, 4, 6], [5, 6]) == ([2, 4, 5, 6], [6], [1, 3, 5], [1, 2, 3, 4])
assert 10 + 4 - 1 == 13 and 40 - 10 == 30
C3 = [a + b + c for a in 'CX' for b in 'CX' for c in 'CX']
A3 = [e for e in C3 if e.count('C') >= 2]; B3 = [e for e in C3 if e[0] == 'X']
assert A3 == ['CCC', 'CCX', 'CXC', 'XCC'] and B3 == ['XCC', 'XCX', 'XXC', 'XXX']
assert [e for e in A3 if e in B3] == ['XCC'] and len(set(A3) | set(B3)) == 7 and [e for e in C3 if e not in A3] == ['CXX', 'XCX', 'XXC', 'XXX']
A12 = [x for x in U12 if x % 2 == 0]; B12 = [x for x in U12 if x % 3 == 0]
assert [x for x in A12 if x not in B12] == [2, 4, 8, 10] and [x for x in U12 if x not in A12 and x not in B12] == [1, 5, 7, 11]
assert [x for x in U12 if x not in set(A12) | set(B12)] == [1, 5, 7, 11]
assert len([s for s in [(4, 5), (4, 6), (5, 6)]]) == 3
S_.append(("Operaciones con sucesos", [
 (1, r"Lanzamos un dado. Sean $A=$ «múltiplo de 3» y $B=$ «menor que 3». Calcula $A\cup B$, $A\cap B$, $\overline{A}$ y $\overline{B}$. ¿Son incompatibles?"
     + recorda(r"$A\cup B$ («$A$ o $B$»): elementos de $A$ o de $B$. \ $A\cap B$ («$A$ y $B$»): elementos comunes. \ $\overline{A}$ («no $A$»): elementos de $E$ que no están en $A$. Si $A\cap B=\varnothing$, $A$ y $B$ son \textbf{incompatibles}."),
     r"$A=\{3,\,6\}$, $B=\{1,\,2\}$: \ $A\cup B=\res{\{1,\,2,\,3,\,6\}}$, \ $A\cap B=\res{\varnothing}$, \ $\overline{A}=\res{\{1,\,2,\,4,\,5\}}$, \ $\overline{B}=\res{\{3,\,4,\,5,\,6\}}$. \ Son \rest{incompatibles}, porque no tienen ningún elemento común."),
 (1, r"En una urna hay diez bolas numeradas del 1 al 10. Sean $A=$ «par» y $B=$ «primo». Calcula $A\cup B$, $A\cap B$, $\overline{A}$ y $\overline{B}$.",
     r"$A=\{2,4,6,8,10\}$, $B=\{2,3,5,7\}$: \ $A\cup B=\res{\{2,3,4,5,6,7,8,10\}}$, \ $A\cap B=\res{\{2\}}$, \ $\overline{A}=\res{\{1,3,5,7,9\}}$, \ $\overline{B}=\res{\{1,4,6,8,9,10\}}$."),
 (1, r"Lanzamos un dado. Sean $A=$ «par» y $B=$ «mayor que 4». Explica con palabras qué significan $A\cup B$, $A\cap B$ y $\overline{A}$ y escribe sus elementos.",
     r"$A\cup B$: «par o mayor que 4» $=\res{\{2,4,5,6\}}$. \ $A\cap B$: «par y mayor que 4» $=\res{\{6\}}$. \ $\overline{A}$: «no par», es decir, impar $=\res{\{1,3,5\}}$."),
 (2, r"Sacamos una carta de una baraja española (40 cartas: oros, copas, espadas y bastos; de cada palo, del 1 al 7, sota, caballo y rey). Sean $O=$ «oros» y $A=$ «as». Describe $O\cap A$, $O\cup A$ y $\overline{O}$ y di cuántas cartas tiene cada uno.",
     r"$O\cap A$ = el as de oros: \res{1 carta}. \ $O\cup A$ = los 10 oros y los otros 3 ases: $10+4-1=\res{13\text{ cartas}}$. \ $\overline{O}$ = las que no son de oros: \res{30 cartas}."),
 (2, r"Lanzamos un dado. Indica si estos pares de sucesos son compatibles, incompatibles o contrarios:" + tasks(1, [r"«sacar 1 o 2» y «sacar 5 o 6»", r"«par» e «impar»", r"«múltiplo de 3» y «par»", r"«menor que 4» y «mayor o igual que 4»"]),
     tasks(1, [r"$\{1,2\}\cap\{5,6\}=\varnothing$: \rest{incompatibles}, pero no contrarios (si sale un 3, no ocurre ninguno de los dos).", r"\rest{contrarios} (y, por tanto, incompatibles).", r"\rest{compatibles}: los dos ocurren si sale un 6.", r"\rest{contrarios}: $\{1,2,3\}$ y $\{4,5,6\}$."])),
 (2, r"Lanzamos tres monedas. Sean $A=$ «al menos dos caras» y $B=$ «la primera es cruz». Escribe $A$, $B$, $A\cap B$, $A\cup B$ y $\overline{A}$.",
     r"$A=\{CCC,\,CCX,\,CXC,\,XCC\}$, \ $B=\{XCC,\,XCX,\,XXC,\,XXX\}$. \ $A\cap B=\res{\{XCC\}}$; \ $A\cup B=\res{E-\{CXX\}}$ (7 resultados); \ $\overline{A}=\res{\{CXX,\,XCX,\,XXC,\,XXX\}}$."),
 (3, r"Sacamos una bola de una urna con bolas del 1 al 12. Sean $A=$ «múltiplo de 2» y $B=$ «múltiplo de 3». Escribe con operaciones y calcula: a) «es múltiplo de 2 pero no de 3»; b) «no es múltiplo ni de 2 ni de 3». Comprueba que b) es el contrario de $A\cup B$.",
     r"$A=\{2,4,6,8,10,12\}$, $B=\{3,6,9,12\}$. \ a) $A\cap\overline{B}=\res{\{2,4,8,10\}}$. \ b) $\overline{A}\cap\overline{B}=\res{\{1,5,7,11\}}$. \ $A\cup B=\{2,3,4,6,8,9,10,12\}$ y su contrario es $\{1,5,7,11\}$ \checkmark"),
 (3, r"Lanzamos un dado y sea $A=\{1,\,2,\,3\}$. ¿Cuántos sucesos $B$ de dos elementos son incompatibles con $A$? Escríbelos. ¿Hay alguno que sea el contrario de $A$?",
     r"$B$ tiene que estar dentro de $\overline{A}=\{4,5,6\}$: \ $\{4,5\}$, $\{4,6\}$, $\{5,6\}$: \res{3 sucesos}. Ninguno es el contrario de $A$, porque el contrario es $\{4,5,6\}$, que tiene tres elementos."),
]))

# =====================================================================
# 3. Probabilitat d'un esdeveniment. Propietats
# =====================================================================
FQ = [7, 9, 8, 10, 6, 10]; assert sum(FQ) == 50
HQ = [Fr(f, 50) for f in FQ]
for h, w in zip(HQ, ['0,14', '0,18', '0,16', '0,2', '0,12', '0,2']): ck(h, w)
ck(Fr(9 + 10 + 10, 50), '0,58')
ck(1 - Fr(62, 100), '0,38'); ck(1 - Fr(3, 7), Fr(4, 7)); ck(1 - Fr(15, 100), Fr(85, 100))
ck(1 - Fr(35, 100) - Fr(25, 100) - Fr(1, 10), '0,3'); ck(1 - Fr(35, 100), '0,65'); ck(Fr(25, 100) + Fr(3, 10), '0,55')
ck(Fr(4, 10) + Fr(5, 10) - Fr(15, 100), '0,75'); ck(1 - Fr(75, 100), '0,25'); ck(Fr(4, 10) - Fr(15, 100), '0,25')
ck(Fr(3, 10) + Fr(45, 100), '0,75'); assert Fr(6, 10) + Fr(5, 10) > 1
ck(Fr(45, 100) + Fr(60, 100) - Fr(25, 100), '0,8'); ck(Fr(2, 10), '0,2'); ck(Fr(60, 100) - Fr(25, 100), '0,35')
pa, pb = 1 - Fr(3, 10), 1 - Fr(4, 10); ck(pa, '0,7'); ck(pb, '0,6'); ck(pa + pb - Fr(9, 10), '0,4')
PK = [Fr(k, 21) for k in D6]; assert sum(PK) == 1; ck(PK[5], Fr(2, 7)); ck(PK[1] + PK[3] + PK[5], Fr(4, 7)); ck(PK[0], Fr(1, 21))
S_.append(("Probabilidad de un suceso. Propiedades", [
 (1, r"Hemos lanzado un dado 50 veces y hemos obtenido estos resultados. Completa la tabla con las frecuencias relativas (en decimal) y calcula la frecuencia relativa de «sacar par».\par\smallskip\begin{center}"
     + ctab(['Resultado', '1', '2', '3', '4', '5', '6'], [['Frec. absoluta'] + [str(f) for f in FQ], ['Frec. relativa'] + ['' for f in FQ]]) + r'\end{center}'
     + recorda(r"Si un suceso ocurre $f$ veces en $n$ repeticiones, su \textbf{frecuencia relativa} es $h=\frac{f}{n}$."),
     r"$h$: \ $\res{0{,}14}$, \ $\res{0{,}18}$, \ $\res{0{,}16}$, \ $\res{0{,}2}$, \ $\res{0{,}12}$, \ $\res{0{,}2}$ \ (suman 1). \quad $h(\text{par})=\frac{9+10+10}{50}=\res{0{,}58}$."),
 (1, r"Calcula la probabilidad del suceso contrario:" + tasks(3, [r"$P(A)=0{,}62$", r"$P(B)=\frac37$", r"$P(C)=15\,\%$"])
     + recorda(r"$P(\overline{A})=1-P(A)$."),
     tasks(3, [r"$P(\overline{A})=\res{0{,}38}$", r"$P(\overline{B})=\res{\frac47}$", r"$P(\overline{C})=\res{85\,\%}$"])),
 (1, r"¿Cuáles de estos números pueden ser la probabilidad de un suceso?" + tasks(4, [r"$0{,}7$", r"$1{,}2$", r"$-0{,}1$", r"$\frac32$", r"$0$", r"$100\,\%$", r"$\frac54$", r"$\frac{99}{100}$"]),
     r"Una probabilidad siempre está entre 0 y 1. Pueden serlo: \rest{$0{,}7$, \ $0$, \ $100\,\%$ y $\frac{99}{100}$}. No pueden serlo: $1{,}2$, $-0{,}1$, $\frac32$ y $\frac54$."),
 (2, r"Una ruleta tiene sectores de cuatro colores. Sabemos que $P(\text{rojo})=0{,}35$, $P(\text{azul})=0{,}25$ y $P(\text{verde})=0{,}1$. Calcula $P(\text{amarillo})$, $P(\text{no rojo})$ y $P(\text{azul o amarillo})$.",
     r"$P(\text{amarillo})=1-(0{,}35+0{,}25+0{,}1)=\res{0{,}3}$. \ $P(\text{no rojo})=1-0{,}35=\res{0{,}65}$. \ Son incompatibles: $P(\text{azul o amarillo})=0{,}25+0{,}3=\res{0{,}55}$."),
 (2, r"Sean $A$ y $B$ dos sucesos con $P(A)=0{,}4$, $P(B)=0{,}5$ y $P(A\cap B)=0{,}15$. Calcula $P(A\cup B)$, la probabilidad de que no ocurra ninguno de los dos y la probabilidad de que ocurra $A$ pero no $B$."
     + recorda(r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$."),
     r"$P(A\cup B)=0{,}4+0{,}5-0{,}15=\res{0{,}75}$. \ $P(\overline{A\cup B})=1-0{,}75=\res{0{,}25}$. \ $P(A\cap\overline{B})=0{,}4-0{,}15=\res{0{,}25}$."),
 (2, r"a) $A$ y $B$ son incompatibles, con $P(A)=0{,}3$ y $P(B)=0{,}45$. Calcula $P(A\cup B)$. \ b) ¿Pueden ser incompatibles dos sucesos con $P(A)=0{,}6$ y $P(B)=0{,}5$? ¿Por qué?",
     r"a) $P(A\cup B)=0{,}3+0{,}45=\res{0{,}75}$. \ b) \rest{No}: si fueran incompatibles, $P(A\cup B)=0{,}6+0{,}5=1{,}1>1$, y eso es imposible."),
 (2, r"En una encuesta, el 45 % del alumnado dice que lee por placer, el 60 % que hace deporte y el 25 % que hace las dos cosas. Elegimos una persona al azar. Calcula la probabilidad de que: a) haga alguna de las dos cosas; b) no haga ninguna; c) solo haga deporte.",
     r"a) $0{,}45+0{,}60-0{,}25=\res{0{,}8}$. \ b) $1-0{,}8=\res{0{,}2}$. \ c) $0{,}60-0{,}25=\res{0{,}35}$."),
 (3, r"Sabemos que $P(A\cup B)=0{,}9$, $P(\overline{A})=0{,}3$ y $P(\overline{B})=0{,}4$. Calcula $P(A)$, $P(B)$ y $P(A\cap B)$. ¿Son incompatibles?",
     r"$P(A)=1-0{,}3=\res{0{,}7}$, \ $P(B)=1-0{,}4=\res{0{,}6}$. \ $0{,}9=0{,}7+0{,}6-P(A\cap B)\Rightarrow P(A\cap B)=\res{0{,}4}$. \ \rest{No} son incompatibles ($P(A\cap B)\neq0$)."),
 (3, r"Un dado está trucado de manera que la probabilidad de cada cara es proporcional a su número: $P(k)=k\cdot p$. Calcula $p$, $P(6)$ y $P(\text{par})$.",
     r"Las seis probabilidades suman 1: $p+2p+\dots+6p=21p=1\Rightarrow p=\res{\frac1{21}}$. \ $P(6)=\frac6{21}=\res{\frac27}$. \ $P(\text{par})=\frac{2+4+6}{21}=\frac{12}{21}=\res{\frac47}$."),
]))

# =====================================================================
# 4. Experiments regulars. Llei de Laplace
# =====================================================================
for f, w in [(lambda x: x == 5, Fr(1, 6)), (lambda x: x % 2 == 0, Fr(1, 2)), (lambda x: x > 2, Fr(2, 3)), (lambda x: x % 3 == 0, Fr(1, 3)), (lambda x: x == 7, 0), (lambda x: x < 7, 1)]: ck(lap(D6, f), w)
ck(Fr(6, 15), Fr(2, 5)); ck(Fr(4, 15), Fr(4, 15)); ck(Fr(5, 15), Fr(1, 3)); ck(Fr(10, 15), Fr(2, 3))
ck(lap(U12, lambda x: x % 4 == 0), Fr(1, 4)); ck(lap(U12, isprime), Fr(5, 12)); ck(lap(U12, lambda x: 12 % x == 0), Fr(1, 2))
ck(Fr(10, 40), Fr(1, 4)); ck(Fr(4, 40), Fr(1, 10)); ck(Fr(3, 40), Fr(3, 40)); ck(Fr(28, 40), Fr(7, 10)); ck(Fr(13, 40), Fr(13, 40))
WM = 'MATEMATICAS'; assert len(WM) == 11 and sum(c in 'AEIOU' for c in WM) == 5 and WM.count('M') == 2 and WM.count('T') == 2
ck(lap(WM, lambda c: c in 'AEIOU'), Fr(5, 11)); ck(lap(WM, lambda c: c == 'M'), Fr(2, 11)); ck(1 - lap(WM, lambda c: c in 'AEIOU'), Fr(6, 11))
L100 = range(100); ck(lap(L100, lambda x: x % 10 == 7), Fr(1, 10)); ck(lap(L100, lambda x: x // 10 == x % 10), Fr(1, 10)); ck(lap(L100, lambda x: x > 89), Fr(1, 10))
ck(lap(range(1, 21), lambda x: x % 3 == 0 or x % 5 == 0), Fr(9, 20))
assert [x for x in range(0, 50) if Fr(x, 5 + x) == Fr(2, 3)] == [10]
pv = 1 - Fr(1, 4) - Fr(1, 3); ck(pv, Fr(5, 12)); assert 10 / pv == 24 and 24 * Fr(1, 4) == 6 and 24 * Fr(1, 3) == 8
ck(Fr(180, 360), Fr(1, 2)); ck(Fr(120, 360), Fr(1, 3)); ck(Fr(60, 360), Fr(1, 6))
ck(lap(D6, lambda x: x >= 5), Fr(1, 3))
RUL = (r'\begin{tikzpicture}[scale=0.75,baseline=(current bounding box.center)]\fill[red!60] (0,0) -- (0:1.3) arc[start angle=0,end angle=180,radius=1.3] -- cycle;'
       r'\fill[blue!55] (0,0) -- (180:1.3) arc[start angle=180,end angle=300,radius=1.3] -- cycle;\fill[teal!60] (0,0) -- (300:1.3) arc[start angle=300,end angle=360,radius=1.3] -- cycle;'
       r'\draw[thick] (0,0) circle (1.3);\draw (0,0)--(0:1.3) (0,0)--(180:1.3) (0,0)--(300:1.3);\node[font=\scriptsize\bfseries] at (90:0.7) {180°};\node[font=\scriptsize\bfseries,white] at (240:0.75) {120°};\node[font=\scriptsize\bfseries] at (330:0.8) {60°};\end{tikzpicture}')
S_.append(("Experimentos regulares. Ley de Laplace", [
 (1, r"Lanzamos un dado. Calcula la probabilidad de:" + tasks(3, [r"sacar un 5", r"sacar par", r"sacar más de 2", r"sacar un múltiplo de 3", r"sacar un 7", r"sacar menos de 7"])
     + recorda(r"En un experimento \textbf{regular} (resultados equiprobables): \ $P(A)=\dfrac{\text{número de casos favorables}}{\text{número de casos posibles}}$."),
     tasks(3, [r"$\res{\frac16}$", r"$\frac36=\res{\frac12}$", r"$\frac46=\res{\frac23}$", r"$\frac26=\res{\frac13}$", r"$\res{0}$ (imposible)", r"$\res{1}$ (seguro)"])),
 (1, r"En una bolsa hay 6 bolas rojas (R), 4 azules (A) y 5 verdes (V). Sacamos una bola al azar. Calcula $P(R)$, $P(A)$, $P(V)$ y $P(\text{no verde})$." + cen(bag('RRRRRRBBBBVVVVV', per=8)),
     r"Hay 15 bolas: \ $P(R)=\frac6{15}=\res{\frac25}$, \ $P(A)=\res{\frac4{15}}$, \ $P(V)=\frac5{15}=\res{\frac13}$, \ $P(\text{no verde})=1-\frac13=\res{\frac23}$."),
 (1, r"Giramos una ruleta de 12 sectores iguales numerados del 1 al 12. Calcula la probabilidad de sacar: a) un múltiplo de 4; b) un número primo; c) un divisor de 12.",
     r"a) $\{4,8,12\}$: $\frac3{12}=\res{\frac14}$. \ b) $\{2,3,5,7,11\}$: $\res{\frac5{12}}$. \ c) $\{1,2,3,4,6,12\}$: $\frac6{12}=\res{\frac12}$."),
 (2, r"Sacamos una carta de una baraja española de 40 cartas. Calcula la probabilidad de que sea:" + tasks(3, [r"de copas", r"un as", r"una figura de espadas", r"que no sea figura", r"un as o un oro", r"el caballo de bastos"]),
     tasks(3, [r"$\frac{10}{40}=\res{\frac14}$", r"$\frac4{40}=\res{\frac1{10}}$", r"$\res{\frac3{40}}$", r"$\frac{28}{40}=\res{\frac7{10}}$", r"$\frac{10+4-1}{40}=\res{\frac{13}{40}}$", r"$\res{\frac1{40}}$"])),
 (2, r"Escribimos cada letra de la palabra MATEMÁTICAS en una tarjeta y sacamos una al azar. ¿Cuál es la probabilidad de que sea una vocal? ¿Y una M? ¿Y una consonante?",
     r"11 letras; vocales A, E, A, I, A: \ $P(\text{vocal})=\res{\frac5{11}}$; \ $P(M)=\res{\frac2{11}}$; \ $P(\text{consonante})=1-\frac5{11}=\res{\frac6{11}}$."),
 (2, r"En una rifa hay 100 papeletas numeradas del 00 al 99. Calcula la probabilidad de que la papeleta premiada: a) acabe en 7; b) tenga las dos cifras iguales; c) sea mayor que 89.",
     r"a) $07,17,\dots,97$: $\frac{10}{100}=\res{\frac1{10}}$. \ b) $00,11,\dots,99$: $\res{\frac1{10}}$. \ c) $90,\dots,99$: $\res{\frac1{10}}$."),
 (2, r"Sacamos una bola de un bombo con bolas numeradas del 1 al 20. ¿Cuál es la probabilidad de que sea múltiplo de 3 o de 5?",
     r"$\{3,5,6,9,10,12,15,18,20\}$: 9 casos ($6+4-1$, porque el 15 es múltiplo de los dos): \ $P=\res{\frac9{20}}$."),
 (2, r"Pablo y María juegan con un dado: Pablo gana si sale 5 o 6, y María si sale 1, 2, 3 o 4. ¿Es justo el juego? ¿Cómo lo cambiarías para que lo fuera?",
     r"$P(\text{Pablo})=\frac26=\frac13$ y $P(\text{María})=\frac46=\frac23$: \rest{no es justo}. Por ejemplo: Pablo gana con par y María con impar ($\frac12$ cada uno)."),
 (3, r"En una bolsa hay 5 bolas rojas y unas cuantas azules. Si la probabilidad de sacar una bola azul es $\frac23$, ¿cuántas bolas azules hay?",
     r"Si hay $x$ azules: $\frac{x}{5+x}=\frac23\Rightarrow3x=10+2x\Rightarrow\res{x=10}$. \ (Comprobación: $\frac{10}{15}=\frac23$ \checkmark)"),
 (3, r"En una bolsa hay bolas rojas, azules y 10 verdes. Si $P(R)=\frac14$ y $P(A)=\frac13$, ¿cuántas bolas hay de cada color?",
     r"$P(V)=1-\frac14-\frac13=\frac5{12}$; si hay $n$ bolas, $\frac{10}{n}=\frac5{12}\Rightarrow n=24$: \ \res{6 rojas, 8 azules y 10 verdes}."),
 (3, r"Esta ruleta tiene tres sectores de 180°, 120° y 60°. ¿Es un experimento regular? Calcula la probabilidad de cada color." + cen(RUL),
     r"\rest{No} es regular: los sectores no son iguales. La probabilidad es la fracción de círculo que ocupa cada sector: \ $P(\text{rojo})=\frac{180}{360}=\res{\frac12}$, \ $P(\text{azul})=\frac{120}{360}=\res{\frac13}$, \ $P(\text{verde})=\frac{60}{360}=\res{\frac16}$."),
]))

# =====================================================================
# 5. Experiments irregulars. Llei dels grans nombres
# =====================================================================
XN, XF = [20, 100, 500, 1000], [13, 58, 297, 601]
for f, n, w in zip(XF, XN, ['0,65', '0,58', '0,594', '0,601']): ck(Fr(f, n), w)
ck(Fr(45, 60), '0,75'); ck(20 * Fr(3, 4), 15)
ck(30 * Fr(120, 300), 12); ck(Fr(120, 300), '0,4')
TD = [150, 150, 150, 150, 200, 400]; assert sum(TD) == 1200
ck(Fr(400, 1200), Fr(1, 3)); ck(Fr(150 + 150 + 400, 1200), Fr(7, 12)); ck(300 * Fr(1, 3), 100)
ck(600 * Fr(1, 6), 100)
S_.append(("Experimentos irregulares. Ley de los grandes números", [
 (1, r"Clasifica estos experimentos en regulares o irregulares:" + tasks(2, [r"Lanzar una moneda de 1 €.", r"Lanzar una chincheta y mirar si cae con la punta hacia arriba.", r"Lanzar un tapón de corcho y mirar si cae de pie.", r"Sacar una carta de una baraja.", r"Girar la ruleta del ejercicio anterior.", r"Lanzar un vaso de plástico y mirar cómo cae."]),
     tasks(2, [r"\rest{regular}", r"\rest{irregular}", r"\rest{irregular}", r"\rest{regular}", r"\rest{irregular}", r"\rest{irregular}"])),
 (1, r"Hemos lanzado una chincheta varias veces y hemos anotado cuántas ha caído con la punta hacia arriba. Completa la tabla y estima la probabilidad de que caiga con la punta hacia arriba.\par\smallskip\begin{center}"
     + ctab(['Lanzamientos', '20', '100', '500', '1000'], [['Punta arriba'] + [str(f) for f in XF], ['Frec. relativa', '', '', '', '']]) + r'\end{center}'
     + recorda(r"\textbf{Ley de los grandes números}: cuando repetimos un experimento muchas veces, la frecuencia relativa de un suceso se estabiliza alrededor de su probabilidad."),
     r"$h$: \ $0{,}65$; \ $0{,}58$; \ $0{,}594$; \ $0{,}601$. \ Con más lanzamientos se estabiliza: $P(\text{punta arriba})\approx\res{0{,}6}$."),
 (2, r"Un jugador de balonmano ha marcado 45 de los 60 penaltis que ha lanzado. Estima la probabilidad de que marque un penalti. ¿Cuántos penaltis esperas que marque de los 20 próximos?",
     r"$P\approx\frac{45}{60}=\res{0{,}75}$. \ $20\cdot0{,}75=\res{15\text{ penaltis}}$ (aproximadamente)."),
 (2, r"Juan ha lanzado una moneda 10 veces y han salido 7 caras. Dice que la moneda está trucada porque la frecuencia relativa de cara es 0,7. ¿Tiene razón?",
     r"\rest{No} necesariamente: 10 lanzamientos son muy pocos y la frecuencia relativa varía mucho. Para saber si está trucada habría que lanzarla muchas más veces (cientos o miles) y ver si $h$ se acerca a 0,5."),
 (2, r"Lanzamos un dado 600 veces. ¿Cuántas veces esperas que salga cada resultado? Si obtenemos 1 → 95, 2 → 104, 3 → 98, 4 → 101, 5 → 106 y 6 → 96, ¿crees que el dado está trucado?",
     r"$600\cdot\frac16=\res{100}$ veces cada uno. Los resultados están todos cerca de 100: \rest{no parece trucado}."),
 (2, r"En una bolsa hay 30 bolas, rojas y blancas. Sacamos una bola, anotamos su color y la devolvemos a la bolsa. Después de 300 extracciones han salido 120 rojas. ¿Cuántas bolas rojas debe de haber?",
     r"$P(R)\approx\frac{120}{300}=0{,}4$; \ si hay $x$ rojas, $\frac{x}{30}\approx0{,}4\Rightarrow x\approx\res{12\text{ rojas}}$ (y 18 blancas)."),
 (3, r"Hemos lanzado un dado 1200 veces: 1 → 150, 2 → 150, 3 → 150, 4 → 150, 5 → 200 y 6 → 400. Estima $P(6)$ y $P(\text{par})$. ¿Cuántos seises esperas en 300 lanzamientos más? ¿Está trucado?",
     r"$P(6)\approx\frac{400}{1200}=\res{\frac13}$; \ $P(\text{par})\approx\frac{150+150+400}{1200}=\frac{700}{1200}=\res{\frac7{12}}\approx0{,}58$. \ $300\cdot\frac13=\res{100\text{ seises}}$. \ \rest{Sí}: en un dado correcto esperaríamos unos 200 de cada resultado."),
]))

# =====================================================================
# 6. Experiments compostos
# =====================================================================
MD = list(product('CX', D6))
ck(lap(MD, lambda e: e == ('C', 3)), Fr(1, 12)); ck(lap(MD, lambda e: e[0] == 'X' and e[1] % 2 == 0), Fr(1, 4)); ck(lap(MD, lambda e: isprime(e[1])), Fr(1, 2))
ck(lap(DD, lambda e: sum(e) == 8), Fr(5, 36)); ck(lap(DD, lambda e: sum(e) == 2), Fr(1, 36)); ck(lap(DD, lambda e: sum(e) >= 10), Fr(1, 6)); ck(lap(DD, lambda e: sum(e) % 2 == 1), Fr(1, 2))
ck(lap(DD, lambda e: e[0] == e[1]), Fr(1, 6)); ck(lap(DD, lambda e: abs(e[0] - e[1]) == 2), Fr(2, 9)); ck(lap(DD, lambda e: e[0] * e[1] % 2 == 0), Fr(3, 4))
CC2 = list(product('CX', repeat=2)); ck(lap(CC2, lambda e: e == ('C', 'C')), Fr(1, 4)); ck(lap(CC2, lambda e: 'X' in e), Fr(3, 4))
CC3 = list(product('CX', repeat=3)); ck(lap(CC3, lambda e: e.count('C') == 3), Fr(1, 8)); ck(lap(CC3, lambda e: e.count('C') == 1), Fr(3, 8)); ck(lap(CC3, lambda e: 'C' in e), Fr(7, 8))
g = Fr(8, 10); ck(g * g, '0,64'); ck((1 - g) ** 2, '0,04'); ck(2 * g * (1 - g), '0,32')
ck(Fr(1, 36), Fr(1, 36)); ck(Fr(5, 6) ** 2, Fr(25, 36)); ck(lap(DD, lambda e: 6 in e), Fr(11, 36))
ck(Fr(1, 4) ** 3, Fr(1, 64)); ck(Fr(3, 4) ** 3, Fr(27, 64)); ck(1 - Fr(27, 64), Fr(37, 64))
D3 = list(product(D6, repeat=3)); ck(lap(D3, lambda e: e[0] == e[1] == e[2]), Fr(1, 36)); ck(lap(D3, lambda e: 6 in e), Fr(91, 216))
ck(lap(DD, lambda e: sum(e) == 7 and 6 in e), Fr(1, 18)); ck(lap(DD, lambda e: sum(e) == 7 or 6 in e), Fr(5, 12))
TC = tree([('C', r'\frac12', [('C', r'\frac12', [], r'$CC$'), ('X', r'\frac12', [], r'$CX$')]), ('X', r'\frac12', [('C', r'\frac12', [], r'$XC$'), ('X', r'\frac12', [], r'$XX$')])], ld=16, sd=(14, 7))
TG = tree([('G', '0{,}8', [('G', '0{,}8', [], r'$GG$: $0{,}64$'), ('F', '0{,}2', [], r'$GF$: $0{,}16$')]), ('F', '0{,}2', [('G', '0{,}8', [], r'$FG$: $0{,}16$'), ('F', '0{,}2', [], r'$FF$: $0{,}04$')])], ld=17, sd=(15, 7.5))
S_.append(("Experimentos compuestos. Diagramas de árbol", [
 (1, r"Lanzamos una moneda y un dado. Calcula la probabilidad de: a) cara y un 3; b) cruz y un número par; c) un número primo (con cara o cruz)."
     + recorda(r"En un \textbf{diagrama de árbol}, la probabilidad de un camino es el \textbf{producto} de las probabilidades de sus ramas; si un suceso tiene varios caminos, las \textbf{sumamos}."),
     r"a) $\frac12\cdot\frac16=\res{\frac1{12}}$. \ b) $\frac12\cdot\frac36=\res{\frac14}$. \ c) $\{2,3,5\}$: $\frac36=\res{\frac12}$."),
 (1, r"Lanzamos dos monedas. Haz el diagrama de árbol con las probabilidades y calcula $P(\text{dos caras})$ y $P(\text{al menos una cruz})$.",
     cen(TC) + r"$P(CC)=\frac12\cdot\frac12=\res{\frac14}$. \ $P(\text{al menos una cruz})=1-P(CC)=\res{\frac34}$."),
 (1, r"Lanzamos dos dados y sumamos los puntos. Completa la tabla de doble entrada y calcula la probabilidad de que la suma sea: a) 8; b) 2; c) 10 o más; d) impar.",
     cen(dtab(lambda a, b: a + b, lambda a, b: a + b == 8)) + r"a) $\res{\frac5{36}}$ (marcadas). \ b) $\res{\frac1{36}}$. \ c) $\frac{3+2+1}{36}=\res{\frac16}$. \ d) $\frac{18}{36}=\res{\frac12}$."),
 (2, r"Lanzamos dos dados. Calcula la probabilidad de que: a) salga el mismo número; b) la diferencia entre el mayor y el menor sea 2; c) el producto sea par.",
     r"a) $\frac6{36}=\res{\frac16}$. \ b) $(1,3),(2,4),(3,5),(4,6)$ y al revés: $\frac8{36}=\res{\frac29}$. \ c) Contrario: los dos impares, $\frac36\cdot\frac36=\frac14$; \ $P=1-\frac14=\res{\frac34}$."),
 (2, r"Lanzamos tres monedas. Calcula la probabilidad de: a) tres caras; b) exactamente una cara; c) al menos una cara.",
     r"Cada camino del árbol tiene probabilidad $\frac12\cdot\frac12\cdot\frac12=\frac18$. \ a) $\res{\frac18}$. \ b) $CXX$, $XCX$, $XXC$: $\res{\frac38}$. \ c) $1-P(XXX)=1-\frac18=\res{\frac78}$."),
 (2, r"Una jugadora de fútbol marca el 80 % de los penaltis. Lanza dos. Haz el diagrama de árbol y calcula la probabilidad de que marque los dos, de que no marque ninguno y de que marque exactamente uno.",
     cen(TG) + r"$P(GG)=\res{0{,}64}$; \ $P(FF)=\res{0{,}04}$; \ $P(\text{exactamente uno})=0{,}16+0{,}16=\res{0{,}32}$. \ (Suman 1 \checkmark)"),
 (2, r"Lanzamos un dado dos veces. Calcula la probabilidad de sacar: a) dos seises; b) ningún seis; c) al menos un seis.",
     r"a) $\frac16\cdot\frac16=\res{\frac1{36}}$. \ b) $\frac56\cdot\frac56=\res{\frac{25}{36}}$. \ c) $1-\frac{25}{36}=\res{\frac{11}{36}}$."),
 (3, r"Un examen tipo test tiene 3 preguntas con 4 opciones cada una (solo una correcta). Si las contestas todas al azar, ¿cuál es la probabilidad de acertarlas todas? ¿Y de no acertar ninguna? ¿Y de acertar al menos una?",
     r"$P(\text{todas})=\left(\frac14\right)^3=\res{\frac1{64}}$. \ $P(\text{ninguna})=\left(\frac34\right)^3=\res{\frac{27}{64}}$. \ $P(\text{al menos una})=1-\frac{27}{64}=\res{\frac{37}{64}}$."),
 (3, r"Lanzamos un dado tres veces. ¿Cuál es la probabilidad de que salga tres veces el mismo número? ¿Y de que salga al menos un seis?",
     r"El primero puede ser cualquiera; los otros dos tienen que coincidir: $1\cdot\frac16\cdot\frac16=\res{\frac1{36}}$. \ $P(\text{al menos un 6})=1-\left(\frac56\right)^3=1-\frac{125}{216}=\res{\frac{91}{216}}\approx0{,}42$."),
 (3, r"Lanzamos dos dados. Sean $A=$ «la suma es 7» y $B=$ «alguno de los dados es un 6». Calcula $P(A)$, $P(B)$, $P(A\cap B)$ y $P(A\cup B)$.",
     r"$P(A)=\frac6{36}$, \ $P(B)=\frac{11}{36}$, \ $A\cap B=\{(1,6),(6,1)\}$: $P(A\cap B)=\frac2{36}=\res{\frac1{18}}$. \ $P(A\cup B)=\frac{6+11-2}{36}=\frac{15}{36}=\res{\frac5{12}}$."),
]))

# =====================================================================
# 7. Extraccions amb i sense reemplaçament. Problemes
# =====================================================================
def two(spec, rep):
    """probabilitats de cada parell de colors en dues extraccions d'una bossa"""
    n = len(spec); out = {}
    for i, j in product(range(n), repeat=2):
        if not rep and i == j: continue
        k = spec[i] + spec[j]; out[k] = out.get(k, 0) + 1
    tot = n * n if rep else n * (n - 1)
    return {k: Fr(v, tot) for k, v in out.items()}
def btree(r, b, rep, cr='B', cb='N'):
    n = r + b; kids = []
    for c1, k1 in ((cr, r), (cb, b)):
        ch = []
        for c2, k2 in ((cr, r), (cb, b)):
            num, den = (k2, n) if rep else (k2 - (c1 == c2), n - 1)
            ch.append((c2 + '*', r'\frac{%d}{%d}' % (num, den), [], r'$%s$: $%s$' % (c1 + c2, fr(Fr(k1, n) * Fr(num, den)))))
        kids.append((c1 + '*', r'\frac{%d}{%d}' % (k1, n), ch))
    return tree(kids, ld=17, sd=(16, 8))
P1 = two('BBBNN', True); ck(P1['BB'], Fr(9, 25)); ck(P1['NN'], Fr(4, 25)); ck(P1['BN'] + P1['NB'], Fr(12, 25))
P2 = two('BBBNN', False); ck(P2['BB'], Fr(3, 10)); ck(P2['NN'], Fr(1, 10)); ck(P2['BN'] + P2['NB'], Fr(3, 5))
ck(Fr(4, 40) * Fr(3, 39), Fr(1, 130)); ck(Fr(36, 40) * Fr(35, 39), Fr(21, 26))
P3 = two('RRRRRBBBVV', False); ck(P3['RR'], Fr(2, 9)); ck(P3['RR'] + P3['BB'] + P3['VV'], Fr(14, 45))
assert (70 + 50, 110 + 170, 400 - 180) == (120, 280, 220)
ck(Fr(120, 400), Fr(3, 10)); ck(Fr(50, 400), Fr(1, 8)); ck(Fr(220 + 120 - 50, 400), Fr(29, 40)); ck(Fr(50, 220), Fr(5, 22))
ck(Fr(1, 3) * Fr(3, 4) + Fr(2, 3) * Fr(1, 4), Fr(5, 12))
ck(1 - Fr(7, 10) * Fr(6, 9), Fr(8, 15))
ck(Fr(4, 6) * Fr(3, 5) * Fr(2, 4), Fr(1, 5))
ck(Fr(1, 2), Fr(1, 2)); ck(Fr(1, 2) * Fr(1, 2), Fr(1, 4)); ck(Fr(1, 2) + Fr(1, 4), Fr(3, 4))
UR = tree([('I', r'\frac13', [('R*', r'\frac34', [], r'$\frac13\cdot\frac34=\frac14$'), ('A*', r'\frac14', [], '')]), ('II', r'\frac23', [('R*', r'\frac14', [], r'$\frac23\cdot\frac14=\frac16$'), ('A*', r'\frac34', [], '')])], ld=18, sd=(16, 8))
CTt = ctab(['', 'Deporte federado', 'No federado', 'Total'], [['Chicos', '70', '', '180'], ['Chicas', '', '', ''], ['Total', '120', '', '400']])
CTs = ctab(['', 'Deporte federado', 'No federado', 'Total'], [['Chicos', '70', '110', '180'], ['Chicas', '50', '170', '220'], ['Total', '120', '280', '400']])
S_.append(("Extracciones con y sin reemplazamiento. Problemas", [
 (1, r"En una bolsa hay 3 bolas blancas (B) y 2 negras (N). Sacamos dos \textbf{con reemplazamiento}. Haz el diagrama de árbol y calcula la probabilidad de que: a) las dos sean blancas; b) las dos sean negras; c) salga una de cada color."
     + recorda(r"\textbf{Con reemplazamiento} devolvemos la bola a la bolsa: la segunda extracción tiene las mismas probabilidades. \textbf{Sin reemplazamiento} no la devolvemos: en la segunda extracción hay una bola menos."),
     cen(btree(3, 2, True)) + r"a) $\frac35\cdot\frac35=\res{\frac9{25}}$. \ b) $\frac25\cdot\frac25=\res{\frac4{25}}$. \ c) $\frac6{25}+\frac6{25}=\res{\frac{12}{25}}$."),
 (1, r"Resuelve el ejercicio anterior sacando las dos bolas \textbf{sin reemplazamiento}.",
     cen(btree(3, 2, False)) + r"a) $\frac35\cdot\frac24=\res{\frac3{10}}$. \ b) $\frac25\cdot\frac14=\res{\frac1{10}}$. \ c) $\frac3{10}+\frac3{10}=\res{\frac35}$. \ (Suman 1 \checkmark)"),
 (2, r"Sacamos dos cartas de una baraja española de 40 cartas, sin reemplazamiento. Calcula la probabilidad de que: a) las dos sean ases; b) ninguna sea un as.",
     r"a) $\frac4{40}\cdot\frac3{39}=\frac{12}{1560}=\res{\frac1{130}}$. \ b) $\frac{36}{40}\cdot\frac{35}{39}=\frac{1260}{1560}=\res{\frac{21}{26}}\approx0{,}81$."),
 (2, r"En una bolsa hay 5 bolas rojas, 3 azules y 2 verdes. Sacamos dos sin reemplazamiento. Calcula la probabilidad de que: a) las dos sean rojas; b) las dos sean del mismo color." + cen(bag('RRRRRBBBVV', per=5)),
     r"a) $\frac5{10}\cdot\frac49=\frac{20}{90}=\res{\frac29}$. \ b) $\frac{20}{90}+\frac3{10}\cdot\frac29+\frac2{10}\cdot\frac19=\frac{20+6+2}{90}=\frac{28}{90}=\res{\frac{14}{45}}$."),
 (2, r"En un instituto hay 400 alumnos, de los cuales 180 son chicos. Hacen deporte federado 120 alumnos, 70 de los cuales son chicos. Completa la tabla y, si elegimos una persona al azar, calcula: a) $P(\text{deporte federado})$; b) $P(\text{chica y deporte federado})$; c) $P(\text{chica o deporte federado})$; d) si sabemos que es una chica, la probabilidad de que haga deporte federado."
     + cen(CTt),
     cen(CTs) + r"a) $\frac{120}{400}=\res{\frac3{10}}$. \ b) $\frac{50}{400}=\res{\frac18}$. \ c) $\frac{220+120-50}{400}=\frac{290}{400}=\res{\frac{29}{40}}$. \ d) Solo contamos las 220 chicas: $\frac{50}{220}=\res{\frac5{22}}$."),
 (2, r"La urna I tiene 3 bolas rojas (R) y 1 azul (A); la urna II tiene 1 bola roja y 3 azules. Lanzamos un dado: si sale 1 o 2, sacamos una bola de la urna I, y si no, de la urna II. ¿Cuál es la probabilidad de sacar una bola roja?",
     cen(UR) + r"$P(R)=\frac13\cdot\frac34+\frac23\cdot\frac14=\frac14+\frac16=\res{\frac5{12}}$."),
 (3, r"En una caja hay 10 bombillas, 3 de las cuales son defectuosas. Probamos dos al azar (sin reemplazamiento). ¿Cuál es la probabilidad de que al menos una sea defectuosa?",
     r"Contrario: ninguna defectuosa, $\frac7{10}\cdot\frac69=\frac{42}{90}=\frac7{15}$. \ $P=1-\frac7{15}=\res{\frac8{15}}$."),
 (3, r"En una bolsa hay 4 bolas rojas y 2 azules. Sacamos tres, una detrás de otra, sin reemplazamiento. ¿Cuál es la probabilidad de que las tres sean rojas?",
     r"$\frac46\cdot\frac35\cdot\frac24=\frac{24}{120}=\res{\frac15}$."),
 (3, r"Ana y Biel lanzan una moneda por turnos y gana quien saca cara primero. Empieza Ana. Calcula la probabilidad de que: a) Ana gane en la primera tirada; b) Biel gane en su primera tirada; c) alguien gane en las dos primeras tiradas.",
     r"a) $\res{\frac12}$. \ b) Ana tiene que sacar cruz y Biel cara: $\frac12\cdot\frac12=\res{\frac14}$. \ c) $\frac12+\frac14=\res{\frac34}$ (o bien $1-P(XX)=1-\frac14$)."),
]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n\\usetikzlibrary{trees}\n'
KW = "pdfkeywords={probabilitat, experiment aleatori, espai mostral, esdeveniments, llei de Laplace, llei dels grans nombres, freqüència relativa, diagrama d'arbre, reemplaçament}"
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
'''
TITOL = 'Probabilitat'

# =====================================================================
# Contingut avançat ocult (2026-11-01): les operacions amb esdeveniments (unió, intersecció, contrari, incompatibles)
# i les fórmules P(Ā) = 1 − P(A) i P(A∪B) es donen en cursos posteriors. Els exercicis de dalt es conserven sense
# tocar; ací s'oculta o es reescriu el que en depén. Amb FM_AVANCAT=1 python3 genera.py ix la fitxa original.
# =====================================================================
AVANCAT = os.environ.get('FM_AVANCAT') == '1'
SEC_OCULTES = {"Operaciones con sucesos"}
# exercicis ocults: un tros únic del seu enunciat
EX_OCULTS = [r"Calcula la probabilidad del suceso contrario:",
             r"Sean $A$ y $B$ dos sucesos con $P(A)=0{,}4$",
             r"a) $A$ y $B$ son incompatibles, con $P(A)=0{,}3$",
             r"En una encuesta, el 45 % del alumnado",
             r"Sabemos que $P(A\cup B)=0{,}9$"]
# reescriptures (sense operacions ni fórmules del contrari): (text original, text nou), en enunciats i solucions
CANVIS = [
 (r"$P(\text{no rojo})=1-0{,}35=\res{0{,}65}$. \ Son incompatibles: $P(\text{azul o amarillo})=0{,}25+0{,}3=\res{0{,}55}$.",
  r"$P(\text{no rojo})=P(\text{azul})+P(\text{verde})+P(\text{amarillo})=0{,}25+0{,}1+0{,}3=\res{0{,}65}$. \ $P(\text{azul o amarillo})=0{,}25+0{,}3=\res{0{,}55}$."),
 (r"$P(\text{no verde})=1-\frac13=\res{\frac23}$.", r"$P(\text{no verde})=\frac{6+4}{15}=\frac{10}{15}=\res{\frac23}$."),
 (r"$P(\text{consonante})=1-\frac5{11}=\res{\frac6{11}}$.", r"$P(\text{consonante})=\frac{11-5}{11}=\res{\frac6{11}}$."),
 (r"$P(\text{al menos una cruz})=1-P(CC)=\res{\frac34}$.", r"$P(\text{al menos una cruz})=P(CX)+P(XC)+P(XX)=\frac14+\frac14+\frac14=\res{\frac34}$."),
 (r"c) Contrario: los dos impares, $\frac36\cdot\frac36=\frac14$; \ $P=1-\frac14=\res{\frac34}$.", r"c) En la tabla de 36 productos, 27 son pares (solo son impares los 9 de dos números impares): $\frac{27}{36}=\res{\frac34}$."),
 (r"c) $1-P(XXX)=1-\frac18=\res{\frac78}$.", r"c) Todos los caminos menos $XXX$: $\res{\frac78}$."),
 (r"c) $1-\frac{25}{36}=\res{\frac{11}{36}}$.", r"c) En la tabla, la fila y la columna del 6 tienen 11 casillas: $\res{\frac{11}{36}}$."),
 (r"¿Y de no acertar ninguna? ¿Y de acertar al menos una?", r"¿Y de no acertar ninguna? ¿Y de acertar exactamente una?"),
 (r"$P(\text{al menos una})=1-\frac{27}{64}=\res{\frac{37}{64}}$.", r"$P(\text{exactamente una})=3\cdot\frac14\cdot\frac34\cdot\frac34=\res{\frac{27}{64}}$ (tres caminos: el acierto puede estar en la primera, la segunda o la tercera pregunta)."),
 (r"¿Y de que salga al menos un seis?", r"¿Y de que no salga ningún seis?"),
 (r"$P(\text{al menos un 6})=1-\left(\frac56\right)^3=1-\frac{125}{216}=\res{\frac{91}{216}}\approx0{,}42$.", r"$P(\text{ningún 6})=\frac56\cdot\frac56\cdot\frac56=\res{\frac{125}{216}}\approx0{,}58$."),
 (r"Sean $A=$ «la suma es 7» y $B=$ «alguno de los dados es un 6». Calcula $P(A)$, $P(B)$, $P(A\cap B)$ y $P(A\cup B)$.",
  r"Calcula la probabilidad de que: a) la suma sea 7; b) alguno de los dados sea un 6; c) la suma sea 7 y algún dado sea un 6; d) la suma sea 7 o algún dado sea un 6."),
 (r"$P(A)=\frac6{36}$, \ $P(B)=\frac{11}{36}$, \ $A\cap B=\{(1,6),(6,1)\}$: $P(A\cap B)=\frac2{36}=\res{\frac1{18}}$. \ $P(A\cup B)=\frac{6+11-2}{36}=\frac{15}{36}=\res{\frac5{12}}$.",
  r"Contamos en la tabla: a) $\frac6{36}=\res{\frac16}$. \ b) $\res{\frac{11}{36}}$. \ c) $(1,6)$ y $(6,1)$: $\frac2{36}=\res{\frac1{18}}$. \ d) $6+11-2=15$ casillas (las 2 de c) no se cuentan dos veces): $\frac{15}{36}=\res{\frac5{12}}$."),
 (r"Contrario: ninguna defectuosa, $\frac7{10}\cdot\frac69=\frac{42}{90}=\frac7{15}$. \ $P=1-\frac7{15}=\res{\frac8{15}}$.",
  r"Sumamos los caminos con alguna defectuosa ($D$); $B$ es una bombilla buena: $DD$: $\frac3{10}\cdot\frac29=\frac6{90}$; \ $DB$: $\frac3{10}\cdot\frac79=\frac{21}{90}$; \ $BD$: $\frac7{10}\cdot\frac39=\frac{21}{90}$. \ $P=\frac{48}{90}=\res{\frac8{15}}$."),
 (r" (o bien $1-P(XX)=1-\frac14$)", r""),
]
ck(Fr(25, 100) + Fr(1, 10) + Fr(3, 10), '0,65'); ck(Fr(10, 15), Fr(2, 3)); ck(Fr(11 - 5, 11), Fr(6, 11)); ck(3 * Fr(1, 4), Fr(3, 4)); ck(lap(DD, lambda e: e[0] * e[1] % 2 == 0), Fr(27, 36))
ck(3 * Fr(1, 4) * Fr(3, 4) ** 2, Fr(27, 64)); ck(Fr(5, 6) ** 3, Fr(125, 216)); assert abs(float(Fr(125, 216)) - 0.58) < 0.005
ck(lap(DD, lambda e: sum(e) == 7), Fr(1, 6)); ck(Fr(6 + 21 + 21, 90), Fr(8, 15)); ck(Fr(3, 10) * Fr(2, 9), Fr(6, 90))
# exercicis nous per a la secció 3 (substitueixen els que s'oculten)
NOUS = {"Probabilidad de un suceso. Propiedades": [
 (1, r"Una ruleta tiene tres colores. Sabemos que $P(\text{rojo})=0{,}5$ y $P(\text{azul})=0{,}3$. Calcula $P(\text{verde})$ y la probabilidad de que salga rojo o verde."
     + recorda(r"Las probabilidades de todos los resultados elementales suman 1, y la probabilidad de un suceso es la suma de las probabilidades de sus resultados elementales."),
     r"$P(\text{verde})=1-(0{,}5+0{,}3)=\res{0{,}2}$. \ $P(\text{rojo o verde})=0{,}5+0{,}2=\res{0{,}7}$."),
 (2, r"Un dado está trucado: las caras del 1 al 5 tienen la misma probabilidad y $P(6)=0{,}5$. Calcula $P(1)$, la probabilidad de sacar par y la de sacar menos de 3.",
     r"Si $P(1)=\dots=P(5)=x$: \ $5x+0{,}5=1\Rightarrow x=\res{0{,}1}$. \ $P(\text{par})=0{,}1+0{,}1+0{,}5=\res{0{,}7}$. \ $P(\text{menos de 3})=0{,}1+0{,}1=\res{0{,}2}$."),
 (3, r"En una bolsa hay bolas rojas, azules y verdes. La probabilidad de sacar roja es el doble que la de sacar azul, y $P(\text{verde})=0{,}4$. Calcula $P(\text{roja})$ y $P(\text{azul})$. Si en la bolsa hay 20 bolas, ¿cuántas hay de cada color?",
     r"Si $P(\text{azul})=x$: \ $2x+x+0{,}4=1\Rightarrow x=0{,}2$. \ $P(\text{roja})=\res{0{,}4}$, \ $P(\text{azul})=\res{0{,}2}$. \ Con 20 bolas: \res{8 rojas, 4 azules y 8 verdes}."),
]}
ck(1 - Fr(5, 10) - Fr(3, 10), '0,2'); ck(Fr(5, 10) + Fr(2, 10), '0,7'); ck((1 - Fr(1, 2)) / 5, '0,1'); ck(Fr(1, 10) * 2 + Fr(1, 2), '0,7')
ck((1 - Fr(4, 10)) / 3, '0,2'); assert (20 * Fr(4, 10), 20 * Fr(2, 10), 20 * Fr(4, 10)) == (8, 4, 8)

def ajusta(S):
    """aplica les ocultacions i les reescriptures (res si AVANCAT)"""
    if AVANCAT: return S
    out, usats = [], set()
    for title, exs in S:
        if title in SEC_OCULTES: continue
        nous = []
        for ex in exs:
            if any(o in ex[1] for o in EX_OCULTS):
                usats.update(o for o in EX_OCULTS if o in ex[1]); continue
            q, s_ = ex[1], ex[2]
            for a, b in CANVIS:
                if a in q or a in s_: usats.add(a)
                q, s_ = q.replace(a, b), s_.replace(a, b)
            nous.append((ex[0], q, s_))
        nous = sorted(nous + NOUS.get(title, []), key=lambda e: e[0])
        out.append((title, nous))
    falten = [x for x in EX_OCULTS + [a for a, _ in CANVIS] if x not in usats]
    assert not falten, falten
    return out

pre = pre_
S_ = ajusta(S_)  # amaga o reescriu el contingut avançat (com fa genera.py)

def build(sol_):
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, ASSIGNATURA
    t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 12: Probabilidad' % t, capcalera='%s · Unidad 12: Probabilidad' % t,
                 pdfkeywords='probabilidad, experimento aleatorio, espacio muestral, sucesos, ley de Laplace, ley de los grandes números, frecuencia relativa, diagrama de árbol, reemplazamiento')
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

''' + ASSIGNATURA + '{' + ('Soluciones de la ficha · Unidad 12' if sol_ else 'Ficha de ejercicios · Unidad 12') + '}{Probabilidad}\n')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás simulaciones, una bolsa de bolas, la tabla de los dos dados y un diagrama de árbol que calcula las probabilidades paso a paso. Las probabilidades se dan en fracción irreducible (o en decimal, si los datos lo son)."
             if sol_ else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos: escribe el espacio muestral, haz un diagrama de árbol o una tabla cuando haga falta y da las probabilidades en forma de fracción irreducible (o en decimal, si los datos lo son).") + r'''
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
    name = 't12-fitxa-solucions-es.tex' if sol_ else 't12-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
