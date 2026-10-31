# Genera t12-fitxa-exercicis.tex i t12-fitxa-solucions.tex (3r ESO, Unitat 12: Probabilitat)
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
BC = {'R': 'red!75!black', 'B': 'blue!70!black', 'V': 'teal', 'G': 'yellow!80!orange', 'N': 'black!80', 'W': 'white'}
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
S_.append(("Experiments aleatoris. Espai mostral i esdeveniments", [
 (1, r"Indica si són experiments aleatoris o deterministes:" + tasks(2, [r"Llançar un dau i anotar el resultat.", r"Mesurar la temperatura a què bull l'aigua al nivell de la mar.", r"Traure una carta d'una baralla sense mirar.", r"Calcular quant pagarem per 3 kg de pomes a 2 €/kg.", r"Endevinar el número guanyador de la loteria.", r"Deixar caure una pilota i mirar si cau a terra."])
     + recorda(r"Un experiment és \textbf{aleatori} si no podem predir-ne el resultat, encara que el repetim en les mateixes condicions. L'\textbf{espai mostral} $E$ és el conjunt de tots els resultats possibles, i un \textbf{esdeveniment} és un subconjunt d'$E$."),
     tasks(2, [r"\rest{aleatori}", r"\rest{determinista}", r"\rest{aleatori}", r"\rest{determinista} (6 €)", r"\rest{aleatori}", r"\rest{determinista}"])),
 (1, r"Escriu l'espai mostral d'aquests experiments:" + tasks(2, [r"Llançar una moneda.", r"Llançar un dau de quatre cares (tetraedre) numerades de l'1 al 4.", r"Girar una ruleta amb 5 sectors iguals: roig, blau, verd, groc i negre.", r"Traure una bola d'una bossa amb boles roges i blaves.", r"Triar a l'atzar un dia de la setmana.", r"Preguntar a algú quantes germanes té (com a màxim, 3)."]),
     tasks(2, [r"$E=\{C,\,X\}$", r"$E=\{1,\,2,\,3,\,4\}$", r"$E=\{\text{roig},\,\text{blau},\,\text{verd},\,\text{groc},\,\text{negre}\}$", r"$E=\{R,\,B\}$", r"$E=\{\text{dl},\,\text{dt},\,\text{dc},\,\text{dj},\,\text{dv},\,\text{ds},\,\text{dg}\}$", r"$E=\{0,\,1,\,2,\,3\}$"])),
 (1, r"Traiem una bola d'una urna amb 12 boles numerades de l'1 al 12. Escriu aquests esdeveniments i digues de quin tipus és cadascun (elemental, compost, segur o impossible):" + tasks(3, [r"$A=$ «parell»", r"$B=$ «múltiple de 5»", r"$C=$ «més gran que 12»", r"$D=$ «divisor de 12»", r"$F=$ «menor que 13»", r"$G=$ «múltiple d'11»"]),
     tasks(3, [r"$\{2,4,6,8,10,12\}$: \rest{compost}", r"$\{5,\,10\}$: \rest{compost}", r"$\varnothing$: \rest{impossible}", r"$\{1,2,3,4,6,12\}$: \rest{compost}", r"$E$: \rest{segur}", r"$\{11\}$: \rest{elemental}"])),
 (2, r"Llancem dues monedes. Fes un diagrama d'arbre i escriu l'espai mostral i els esdeveniments $A=$ «almenys una cara», $B=$ «cap cara» i $C=$ «les dues iguals».",
     cen(T2) + r"$E=\{CC,\,CX,\,XC,\,XX\}$; \quad $A=\res{\{CC,\,CX,\,XC\}}$, \quad $B=\res{\{XX\}}$, \quad $C=\res{\{CC,\,XX\}}$."),
 (2, r"Llancem una moneda i un dau. Fes una taula de doble entrada amb tots els resultats. Quants n'hi ha? Escriu els esdeveniments «cara i nombre parell» i «creu i menor que 3».",
     cen(ctab(['', '1', '2', '3', '4', '5', '6'], [['$C$'] + ['$C%d$' % i for i in D6], ['$X$'] + ['$X%d$' % i for i in D6]]))
     + r"$2\cdot6=\res{12}$ resultats. \quad «Cara i parell» $=\res{\{C2,\,C4,\,C6\}}$; \quad «creu i menor que 3» $=\res{\{X1,\,X2\}}$."),
 (2, r"Una família té tres fills. Anotem si cadascun és xiqueta (A) o xiquet (O), per ordre de naixement. Fes un diagrama d'arbre, escriu l'espai mostral i l'esdeveniment «exactament dues xiquetes».",
     cen(T3) + r"$E=\{OOO,\,OOA,\,OAO,\,OAA,\,AOO,\,AOA,\,AAO,\,AAA\}$ (8 resultats). \quad «Dues xiquetes» $=\res{\{OAA,\,AOA,\,AAO\}}$."),
 (3, r"Formem nombres de tres xifres diferents amb les xifres 1, 2 i 3. Escriu l'espai mostral i els esdeveniments «el nombre és parell» i «el nombre és més gran que 200».",
     r"$E=\{123,\,132,\,213,\,231,\,312,\,321\}$. \quad «Parell» $=\res{\{132,\,312\}}$; \quad «més gran que 200» $=\res{\{213,\,231,\,312,\,321\}}$."),
 (3, r"Llancem dos daus (un de roig i un de blau). Quants resultats té l'espai mostral? Escriu els esdeveniments «la suma és 5» i «trauen el mateix nombre (doble)».",
     r"$6\cdot6=\res{36}$ resultats (parells ordenats). «Suma 5» $=\res{\{(1,4),\,(2,3),\,(3,2),\,(4,1)\}}$; «doble» $=\res{\{(1,1),\,(2,2),\,\dots,\,(6,6)\}}$ (6 resultats)."),
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
S_.append(("Operacions amb esdeveniments", [
 (1, r"Llancem un dau. Siguen $A=$ «múltiple de 3» i $B=$ «menor que 3». Calcula $A\cup B$, $A\cap B$, $\overline{A}$ i $\overline{B}$. Són incompatibles?"
     + recorda(r"$A\cup B$ («$A$ o $B$»): elements d'$A$ o de $B$. \ $A\cap B$ («$A$ i $B$»): elements comuns. \ $\overline{A}$ («no $A$»): elements d'$E$ que no són en $A$. Si $A\cap B=\varnothing$, $A$ i $B$ són \textbf{incompatibles}."),
     r"$A=\{3,\,6\}$, $B=\{1,\,2\}$: \ $A\cup B=\res{\{1,\,2,\,3,\,6\}}$, \ $A\cap B=\res{\varnothing}$, \ $\overline{A}=\res{\{1,\,2,\,4,\,5\}}$, \ $\overline{B}=\res{\{3,\,4,\,5,\,6\}}$. \ Són \rest{incompatibles}, perquè no tenen cap element comú."),
 (1, r"En una urna hi ha deu boles numerades de l'1 al 10. Siguen $A=$ «parell» i $B=$ «primer». Calcula $A\cup B$, $A\cap B$, $\overline{A}$ i $\overline{B}$.",
     r"$A=\{2,4,6,8,10\}$, $B=\{2,3,5,7\}$: \ $A\cup B=\res{\{2,3,4,5,6,7,8,10\}}$, \ $A\cap B=\res{\{2\}}$, \ $\overline{A}=\res{\{1,3,5,7,9\}}$, \ $\overline{B}=\res{\{1,4,6,8,9,10\}}$."),
 (1, r"Llancem un dau. Siguen $A=$ «parell» i $B=$ «major que 4». Explica amb paraules què volen dir $A\cup B$, $A\cap B$ i $\overline{A}$ i escriu-ne els elements.",
     r"$A\cup B$: «parell o major que 4» $=\res{\{2,4,5,6\}}$. \ $A\cap B$: «parell i major que 4» $=\res{\{6\}}$. \ $\overline{A}$: «no parell», és a dir, senar $=\res{\{1,3,5\}}$."),
 (2, r"Traiem una carta d'una baralla espanyola (40 cartes: oros, copes, espases i bastos; de cada pal, de l'1 al 7, sota, cavall i rei). Siguen $O=$ «oros» i $A=$ «as». Descriu $O\cap A$, $O\cup A$ i $\overline{O}$ i digues quantes cartes té cadascun.",
     r"$O\cap A$ = l'as d'oros: \res{1 carta}. \ $O\cup A$ = els 10 oros i els altres 3 asos: $10+4-1=\res{13\text{ cartes}}$. \ $\overline{O}$ = les que no són d'oros: \res{30 cartes}."),
 (2, r"Llancem un dau. Indica si aquests parells d'esdeveniments són compatibles, incompatibles o contraris:" + tasks(1, [r"«traure 1 o 2» i «traure 5 o 6»", r"«parell» i «senar»", r"«múltiple de 3» i «parell»", r"«menor que 4» i «major o igual que 4»"]),
     tasks(1, [r"$\{1,2\}\cap\{5,6\}=\varnothing$: \rest{incompatibles}, però no contraris (si ix un 3, no ocorre cap dels dos).", r"\rest{contraris} (i, per tant, incompatibles).", r"\rest{compatibles}: tots dos ocorren si ix un 6.", r"\rest{contraris}: $\{1,2,3\}$ i $\{4,5,6\}$."])),
 (2, r"Llancem tres monedes. Siguen $A=$ «almenys dues cares» i $B=$ «la primera és creu». Escriu $A$, $B$, $A\cap B$, $A\cup B$ i $\overline{A}$.",
     r"$A=\{CCC,\,CCX,\,CXC,\,XCC\}$, \ $B=\{XCC,\,XCX,\,XXC,\,XXX\}$. \ $A\cap B=\res{\{XCC\}}$; \ $A\cup B=\res{E-\{CXX\}}$ (7 resultats); \ $\overline{A}=\res{\{CXX,\,XCX,\,XXC,\,XXX\}}$."),
 (3, r"Traiem una bola d'una urna amb boles de l'1 al 12. Siguen $A=$ «múltiple de 2» i $B=$ «múltiple de 3». Escriu amb operacions i calcula: a) «és múltiple de 2 però no de 3»; b) «no és múltiple ni de 2 ni de 3». Comprova que b) és el contrari d'$A\cup B$.",
     r"$A=\{2,4,6,8,10,12\}$, $B=\{3,6,9,12\}$. \ a) $A\cap\overline{B}=\res{\{2,4,8,10\}}$. \ b) $\overline{A}\cap\overline{B}=\res{\{1,5,7,11\}}$. \ $A\cup B=\{2,3,4,6,8,9,10,12\}$ i el seu contrari és $\{1,5,7,11\}$ \checkmark"),
 (3, r"Llancem un dau i siga $A=\{1,\,2,\,3\}$. Quants esdeveniments $B$ de dos elements són incompatibles amb $A$? Escriu-los. N'hi ha algun que siga el contrari d'$A$?",
     r"$B$ ha d'estar dins de $\overline{A}=\{4,5,6\}$: \ $\{4,5\}$, $\{4,6\}$, $\{5,6\}$: \res{3 esdeveniments}. Cap és el contrari d'$A$, perquè el contrari és $\{4,5,6\}$, que té tres elements."),
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
S_.append(("Probabilitat d'un esdeveniment. Propietats", [
 (1, r"Hem llançat un dau 50 vegades i hem obtingut aquests resultats. Completa la taula amb les freqüències relatives (en decimal) i calcula la freqüència relativa de «traure parell».\par\smallskip\begin{center}"
     + ctab(['Resultat', '1', '2', '3', '4', '5', '6'], [['Freq. absoluta'] + [str(f) for f in FQ], ['Freq. relativa'] + ['' for f in FQ]]) + r'\end{center}'
     + recorda(r"Si un esdeveniment ocorre $f$ vegades en $n$ repeticions, la seua \textbf{freqüència relativa} és $h=\frac{f}{n}$."),
     r"$h$: \ $\res{0{,}14}$, \ $\res{0{,}18}$, \ $\res{0{,}16}$, \ $\res{0{,}2}$, \ $\res{0{,}12}$, \ $\res{0{,}2}$ \ (sumen 1). \quad $h(\text{parell})=\frac{9+10+10}{50}=\res{0{,}58}$."),
 (1, r"Calcula la probabilitat de l'esdeveniment contrari:" + tasks(3, [r"$P(A)=0{,}62$", r"$P(B)=\frac37$", r"$P(C)=15\,\%$"])
     + recorda(r"$P(\overline{A})=1-P(A)$."),
     tasks(3, [r"$P(\overline{A})=\res{0{,}38}$", r"$P(\overline{B})=\res{\frac47}$", r"$P(\overline{C})=\res{85\,\%}$"])),
 (1, r"Quins d'aquests nombres poden ser la probabilitat d'un esdeveniment?" + tasks(4, [r"$0{,}7$", r"$1{,}2$", r"$-0{,}1$", r"$\frac32$", r"$0$", r"$100\,\%$", r"$\frac54$", r"$\frac{99}{100}$"]),
     r"Una probabilitat sempre està entre 0 i 1. Poden ser-ho: \rest{$0{,}7$, \ $0$, \ $100\,\%$ i $\frac{99}{100}$}. No poden ser-ho: $1{,}2$, $-0{,}1$, $\frac32$ i $\frac54$."),
 (2, r"Una ruleta té sectors de quatre colors. Sabem que $P(\text{roig})=0{,}35$, $P(\text{blau})=0{,}25$ i $P(\text{verd})=0{,}1$. Calcula $P(\text{groc})$, $P(\text{no roig})$ i $P(\text{blau o groc})$.",
     r"$P(\text{groc})=1-(0{,}35+0{,}25+0{,}1)=\res{0{,}3}$. \ $P(\text{no roig})=1-0{,}35=\res{0{,}65}$. \ Són incompatibles: $P(\text{blau o groc})=0{,}25+0{,}3=\res{0{,}55}$."),
 (2, r"Siguen $A$ i $B$ dos esdeveniments amb $P(A)=0{,}4$, $P(B)=0{,}5$ i $P(A\cap B)=0{,}15$. Calcula $P(A\cup B)$, la probabilitat que no ocórrega cap dels dos i la probabilitat que ocórrega $A$ però no $B$."
     + recorda(r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$."),
     r"$P(A\cup B)=0{,}4+0{,}5-0{,}15=\res{0{,}75}$. \ $P(\overline{A\cup B})=1-0{,}75=\res{0{,}25}$. \ $P(A\cap\overline{B})=0{,}4-0{,}15=\res{0{,}25}$."),
 (2, r"a) $A$ i $B$ són incompatibles, amb $P(A)=0{,}3$ i $P(B)=0{,}45$. Calcula $P(A\cup B)$. \ b) Poden ser incompatibles dos esdeveniments amb $P(A)=0{,}6$ i $P(B)=0{,}5$? Per què?",
     r"a) $P(A\cup B)=0{,}3+0{,}45=\res{0{,}75}$. \ b) \rest{No}: si foren incompatibles, $P(A\cup B)=0{,}6+0{,}5=1{,}1>1$, i això és impossible."),
 (2, r"En una enquesta, el 45 % de l'alumnat diu que llig per plaer, el 60 % que fa esport i el 25 % que fa totes dues coses. Triem una persona a l'atzar. Calcula la probabilitat que: a) faça alguna de les dues coses; b) no en faça cap; c) només faça esport.",
     r"a) $0{,}45+0{,}60-0{,}25=\res{0{,}8}$. \ b) $1-0{,}8=\res{0{,}2}$. \ c) $0{,}60-0{,}25=\res{0{,}35}$."),
 (3, r"Sabem que $P(A\cup B)=0{,}9$, $P(\overline{A})=0{,}3$ i $P(\overline{B})=0{,}4$. Calcula $P(A)$, $P(B)$ i $P(A\cap B)$. Són incompatibles?",
     r"$P(A)=1-0{,}3=\res{0{,}7}$, \ $P(B)=1-0{,}4=\res{0{,}6}$. \ $0{,}9=0{,}7+0{,}6-P(A\cap B)\Rightarrow P(A\cap B)=\res{0{,}4}$. \ \rest{No} són incompatibles ($P(A\cap B)\neq0$)."),
 (3, r"Un dau està trucat de manera que la probabilitat de cada cara és proporcional al seu nombre: $P(k)=k\cdot p$. Calcula $p$, $P(6)$ i $P(\text{parell})$.",
     r"Les sis probabilitats sumen 1: $p+2p+\dots+6p=21p=1\Rightarrow p=\res{\frac1{21}}$. \ $P(6)=\frac6{21}=\res{\frac27}$. \ $P(\text{parell})=\frac{2+4+6}{21}=\frac{12}{21}=\res{\frac47}$."),
]))

# =====================================================================
# 4. Experiments regulars. Llei de Laplace
# =====================================================================
for f, w in [(lambda x: x == 5, Fr(1, 6)), (lambda x: x % 2 == 0, Fr(1, 2)), (lambda x: x > 2, Fr(2, 3)), (lambda x: x % 3 == 0, Fr(1, 3)), (lambda x: x == 7, 0), (lambda x: x < 7, 1)]: ck(lap(D6, f), w)
ck(Fr(6, 15), Fr(2, 5)); ck(Fr(4, 15), Fr(4, 15)); ck(Fr(5, 15), Fr(1, 3)); ck(Fr(10, 15), Fr(2, 3))
ck(lap(U12, lambda x: x % 4 == 0), Fr(1, 4)); ck(lap(U12, isprime), Fr(5, 12)); ck(lap(U12, lambda x: 12 % x == 0), Fr(1, 2))
ck(Fr(10, 40), Fr(1, 4)); ck(Fr(4, 40), Fr(1, 10)); ck(Fr(3, 40), Fr(3, 40)); ck(Fr(28, 40), Fr(7, 10)); ck(Fr(13, 40), Fr(13, 40))
WM = 'MATEMATIQUES'; assert len(WM) == 12 and sum(c in 'AEIOU' for c in WM) == 6 and WM.count('M') == 2 and WM.count('T') == 2
ck(lap(WM, lambda c: c in 'AEIOU'), Fr(1, 2)); ck(lap(WM, lambda c: c == 'M'), Fr(1, 6))
L100 = range(100); ck(lap(L100, lambda x: x % 10 == 7), Fr(1, 10)); ck(lap(L100, lambda x: x // 10 == x % 10), Fr(1, 10)); ck(lap(L100, lambda x: x > 89), Fr(1, 10))
ck(lap(range(1, 21), lambda x: x % 3 == 0 or x % 5 == 0), Fr(9, 20))
assert [x for x in range(0, 50) if Fr(x, 5 + x) == Fr(2, 3)] == [10]
pv = 1 - Fr(1, 4) - Fr(1, 3); ck(pv, Fr(5, 12)); assert 10 / pv == 24 and 24 * Fr(1, 4) == 6 and 24 * Fr(1, 3) == 8
ck(Fr(180, 360), Fr(1, 2)); ck(Fr(120, 360), Fr(1, 3)); ck(Fr(60, 360), Fr(1, 6))
ck(lap(D6, lambda x: x >= 5), Fr(1, 3))
RUL = (r'\begin{tikzpicture}[scale=0.75,baseline=(current bounding box.center)]\fill[red!60] (0,0) -- (0:1.3) arc[start angle=0,end angle=180,radius=1.3] -- cycle;'
       r'\fill[blue!55] (0,0) -- (180:1.3) arc[start angle=180,end angle=300,radius=1.3] -- cycle;\fill[teal!60] (0,0) -- (300:1.3) arc[start angle=300,end angle=360,radius=1.3] -- cycle;'
       r'\draw[thick] (0,0) circle (1.3);\draw (0,0)--(0:1.3) (0,0)--(180:1.3) (0,0)--(300:1.3);\node[font=\scriptsize\bfseries] at (90:0.7) {180°};\node[font=\scriptsize\bfseries,white] at (240:0.75) {120°};\node[font=\scriptsize\bfseries] at (330:0.8) {60°};\end{tikzpicture}')
S_.append(("Experiments regulars. Llei de Laplace", [
 (1, r"Llancem un dau. Calcula la probabilitat de:" + tasks(3, [r"traure un 5", r"traure parell", r"traure més de 2", r"traure un múltiple de 3", r"traure un 7", r"traure menys de 7"])
     + recorda(r"En un experiment \textbf{regular} (resultats equiprobables): \ $P(A)=\dfrac{\text{nombre de casos favorables}}{\text{nombre de casos possibles}}$."),
     tasks(3, [r"$\res{\frac16}$", r"$\frac36=\res{\frac12}$", r"$\frac46=\res{\frac23}$", r"$\frac26=\res{\frac13}$", r"$\res{0}$ (impossible)", r"$\res{1}$ (segur)"])),
 (1, r"En una bossa hi ha 6 boles roges, 4 de blaves i 5 de verdes. Traiem una bola a l'atzar. Calcula $P(R)$, $P(B)$, $P(V)$ i $P(\text{no verda})$." + cen(bag('RRRRRRBBBBVVVVV', per=8)),
     r"Hi ha 15 boles: \ $P(R)=\frac6{15}=\res{\frac25}$, \ $P(B)=\res{\frac4{15}}$, \ $P(V)=\frac5{15}=\res{\frac13}$, \ $P(\text{no verda})=1-\frac13=\res{\frac23}$."),
 (1, r"Girem una ruleta de 12 sectors iguals numerats de l'1 al 12. Calcula la probabilitat de traure: a) un múltiple de 4; b) un nombre primer; c) un divisor de 12.",
     r"a) $\{4,8,12\}$: $\frac3{12}=\res{\frac14}$. \ b) $\{2,3,5,7,11\}$: $\res{\frac5{12}}$. \ c) $\{1,2,3,4,6,12\}$: $\frac6{12}=\res{\frac12}$."),
 (2, r"Traiem una carta d'una baralla espanyola de 40 cartes. Calcula la probabilitat que siga:" + tasks(3, [r"de copes", r"un as", r"una figura d'espases", r"que no siga figura", r"un as o un oro", r"el cavall de bastos"]),
     tasks(3, [r"$\frac{10}{40}=\res{\frac14}$", r"$\frac4{40}=\res{\frac1{10}}$", r"$\res{\frac3{40}}$", r"$\frac{28}{40}=\res{\frac7{10}}$", r"$\frac{10+4-1}{40}=\res{\frac{13}{40}}$", r"$\res{\frac1{40}}$"])),
 (2, r"Escrivim cada lletra de la paraula MATEMATIQUES en una targeta i en traiem una a l'atzar. Quina és la probabilitat que siga una vocal? I una M? I una consonant?",
     r"12 lletres; vocals A, E, A, I, U, E: \ $P(\text{vocal})=\frac6{12}=\res{\frac12}$; \ $P(M)=\frac2{12}=\res{\frac16}$; \ $P(\text{consonant})=1-\frac12=\res{\frac12}$."),
 (2, r"En una rifa hi ha 100 paperetes numerades del 00 al 99. Calcula la probabilitat que la papereta premiada: a) acabe en 7; b) tinga les dues xifres iguals; c) siga més gran que 89.",
     r"a) $07,17,\dots,97$: $\frac{10}{100}=\res{\frac1{10}}$. \ b) $00,11,\dots,99$: $\res{\frac1{10}}$. \ c) $90,\dots,99$: $\res{\frac1{10}}$."),
 (2, r"Traiem una bola d'un bombo amb boles numerades de l'1 al 20. Quina és la probabilitat que siga múltiple de 3 o de 5?",
     r"$\{3,5,6,9,10,12,15,18,20\}$: 9 casos ($6+4-1$, perquè el 15 és múltiple dels dos): \ $P=\res{\frac9{20}}$."),
 (2, r"En Pau i la Maria juguen amb un dau: en Pau guanya si ix 5 o 6, i la Maria si ix 1, 2, 3 o 4. És just el joc? Com el canviaries perquè ho fóra?",
     r"$P(\text{Pau})=\frac26=\frac13$ i $P(\text{Maria})=\frac46=\frac23$: \rest{no és just}. Per exemple: en Pau guanya amb parell i la Maria amb senar ($\frac12$ cadascun)."),
 (3, r"En una bossa hi ha 5 boles roges i unes quantes de blaves. Si la probabilitat de traure una bola blava és $\frac23$, quantes boles blaves hi ha?",
     r"Si hi ha $x$ blaves: $\frac{x}{5+x}=\frac23\Rightarrow3x=10+2x\Rightarrow\res{x=10}$. \ (Comprovació: $\frac{10}{15}=\frac23$ \checkmark)"),
 (3, r"En una bossa hi ha boles roges, blaves i 10 de verdes. Si $P(R)=\frac14$ i $P(B)=\frac13$, quantes boles hi ha de cada color?",
     r"$P(V)=1-\frac14-\frac13=\frac5{12}$; si hi ha $n$ boles, $\frac{10}{n}=\frac5{12}\Rightarrow n=24$: \ \res{6 roges, 8 blaves i 10 verdes}."),
 (3, r"Aquesta ruleta té tres sectors de 180°, 120° i 60°. És un experiment regular? Calcula la probabilitat de cada color." + cen(RUL),
     r"\rest{No} és regular: els sectors no són iguals. La probabilitat és la fracció de cercle que ocupa cada sector: \ $P(\text{roig})=\frac{180}{360}=\res{\frac12}$, \ $P(\text{blau})=\frac{120}{360}=\res{\frac13}$, \ $P(\text{verd})=\frac{60}{360}=\res{\frac16}$."),
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
S_.append(("Experiments irregulars. Llei dels grans nombres", [
 (1, r"Classifica aquests experiments en regulars o irregulars:" + tasks(2, [r"Llançar una moneda d'1 €.", r"Llançar una xinxeta i mirar si cau amb la punta cap amunt.", r"Llançar un tap de suro i mirar si cau dret.", r"Traure una carta d'una baralla.", r"Girar la ruleta de l'exercici anterior.", r"Llançar un got de plàstic i mirar com cau."]),
     tasks(2, [r"\rest{regular}", r"\rest{irregular}", r"\rest{irregular}", r"\rest{regular}", r"\rest{irregular}", r"\rest{irregular}"])),
 (1, r"Hem llançat una xinxeta diverses vegades i hem anotat quantes ha caigut amb la punta cap amunt. Completa la taula i estima la probabilitat que caiga amb la punta cap amunt.\par\smallskip\begin{center}"
     + ctab(['Llançaments', '20', '100', '500', '1000'], [['Punta amunt'] + [str(f) for f in XF], ['Freq. relativa', '', '', '', '']]) + r'\end{center}'
     + recorda(r"\textbf{Llei dels grans nombres}: quan repetim un experiment moltes vegades, la freqüència relativa d'un esdeveniment s'estabilitza al voltant de la seua probabilitat."),
     r"$h$: \ $0{,}65$; \ $0{,}58$; \ $0{,}594$; \ $0{,}601$. \ Amb més llançaments s'estabilitza: $P(\text{punta amunt})\approx\res{0{,}6}$."),
 (2, r"Un jugador d'handbol ha marcat 45 dels 60 penals que ha llançat. Estima la probabilitat que marque un penal. Quants penals esperes que marque dels 20 pròxims?",
     r"$P\approx\frac{45}{60}=\res{0{,}75}$. \ $20\cdot0{,}75=\res{15\text{ penals}}$ (aproximadament)."),
 (2, r"Joan ha llançat una moneda 10 vegades i n'han eixit 7 cares. Diu que la moneda està trucada perquè la freqüència relativa de cara és 0,7. Té raó?",
     r"\rest{No} necessàriament: 10 llançaments són molt pocs i la freqüència relativa varia molt. Per a saber si està trucada caldria llançar-la moltes més vegades (centenars o milers) i veure si $h$ s'acosta a 0,5."),
 (2, r"Llancem un dau 600 vegades. Quantes vegades esperes que isca cada resultat? Si obtenim 1 → 95, 2 → 104, 3 → 98, 4 → 101, 5 → 106 i 6 → 96, creus que el dau està trucat?",
     r"$600\cdot\frac16=\res{100}$ vegades cadascun. Els resultats són tots prop de 100: \rest{no sembla trucat}."),
 (2, r"En una bossa hi ha 30 boles, roges i blanques. Traiem una bola, n'anotem el color i la tornem a la bossa. Després de 300 extraccions n'han eixit 120 de roges. Quantes boles roges deu haver-hi?",
     r"$P(R)\approx\frac{120}{300}=0{,}4$; \ si hi ha $x$ roges, $\frac{x}{30}\approx0{,}4\Rightarrow x\approx\res{12\text{ roges}}$ (i 18 blanques)."),
 (3, r"Hem llançat un dau 1200 vegades: 1 → 150, 2 → 150, 3 → 150, 4 → 150, 5 → 200 i 6 → 400. Estima $P(6)$ i $P(\text{parell})$. Quants sisos esperes en 300 llançaments més? Està trucat?",
     r"$P(6)\approx\frac{400}{1200}=\res{\frac13}$; \ $P(\text{parell})\approx\frac{150+150+400}{1200}=\frac{700}{1200}=\res{\frac7{12}}\approx0{,}58$. \ $300\cdot\frac13=\res{100\text{ sisos}}$. \ \rest{Sí}: en un dau correcte esperaríem uns 200 de cada resultat."),
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
S_.append(("Experiments compostos. Diagrames d'arbre", [
 (1, r"Llancem una moneda i un dau. Calcula la probabilitat de: a) cara i un 3; b) creu i un nombre parell; c) un nombre primer (amb cara o creu)."
     + recorda(r"En un \textbf{diagrama d'arbre}, la probabilitat d'un camí és el \textbf{producte} de les probabilitats de les seues branques; si un esdeveniment té diversos camins, les \textbf{sumem}."),
     r"a) $\frac12\cdot\frac16=\res{\frac1{12}}$. \ b) $\frac12\cdot\frac36=\res{\frac14}$. \ c) $\{2,3,5\}$: $\frac36=\res{\frac12}$."),
 (1, r"Llancem dues monedes. Fes el diagrama d'arbre amb les probabilitats i calcula $P(\text{dues cares})$ i $P(\text{almenys una creu})$.",
     cen(TC) + r"$P(CC)=\frac12\cdot\frac12=\res{\frac14}$. \ $P(\text{almenys una creu})=1-P(CC)=\res{\frac34}$."),
 (1, r"Llancem dos daus i sumem els punts. Completa la taula de doble entrada i calcula la probabilitat que la suma siga: a) 8; b) 2; c) 10 o més; d) senar.",
     cen(dtab(lambda a, b: a + b, lambda a, b: a + b == 8)) + r"a) $\res{\frac5{36}}$ (marcades). \ b) $\res{\frac1{36}}$. \ c) $\frac{3+2+1}{36}=\res{\frac16}$. \ d) $\frac{18}{36}=\res{\frac12}$."),
 (2, r"Llancem dos daus. Calcula la probabilitat que: a) traguen el mateix nombre; b) la diferència entre el major i el menor siga 2; c) el producte siga parell.",
     r"a) $\frac6{36}=\res{\frac16}$. \ b) $(1,3),(2,4),(3,5),(4,6)$ i al revés: $\frac8{36}=\res{\frac29}$. \ c) Contrari: tots dos senars, $\frac36\cdot\frac36=\frac14$; \ $P=1-\frac14=\res{\frac34}$."),
 (2, r"Llancem tres monedes. Calcula la probabilitat de: a) tres cares; b) exactament una cara; c) almenys una cara.",
     r"Cada camí de l'arbre té probabilitat $\frac12\cdot\frac12\cdot\frac12=\frac18$. \ a) $\res{\frac18}$. \ b) $CXX$, $XCX$, $XXC$: $\res{\frac38}$. \ c) $1-P(XXX)=1-\frac18=\res{\frac78}$."),
 (2, r"Una jugadora de futbol marca el 80 % dels penals. En llança dos. Fes el diagrama d'arbre i calcula la probabilitat que marque tots dos, que no en marque cap i que en marque exactament un.",
     cen(TG) + r"$P(GG)=\res{0{,}64}$; \ $P(FF)=\res{0{,}04}$; \ $P(\text{exactament un})=0{,}16+0{,}16=\res{0{,}32}$. \ (Sumen 1 \checkmark)"),
 (2, r"Llancem un dau dues vegades. Calcula la probabilitat de traure: a) dos sisos; b) cap sis; c) almenys un sis.",
     r"a) $\frac16\cdot\frac16=\res{\frac1{36}}$. \ b) $\frac56\cdot\frac56=\res{\frac{25}{36}}$. \ c) $1-\frac{25}{36}=\res{\frac{11}{36}}$."),
 (3, r"Un examen tipus test té 3 preguntes amb 4 opcions cadascuna (només una correcta). Si les contestes totes a l'atzar, quina és la probabilitat d'encertar-les totes? I de no encertar-ne cap? I d'encertar-ne almenys una?",
     r"$P(\text{totes})=\left(\frac14\right)^3=\res{\frac1{64}}$. \ $P(\text{cap})=\left(\frac34\right)^3=\res{\frac{27}{64}}$. \ $P(\text{almenys una})=1-\frac{27}{64}=\res{\frac{37}{64}}$."),
 (3, r"Llancem un dau tres vegades. Quina és la probabilitat que isca tres vegades el mateix nombre? I que isca almenys un sis?",
     r"El primer pot ser qualsevol; els altres dos han de coincidir: $1\cdot\frac16\cdot\frac16=\res{\frac1{36}}$. \ $P(\text{almenys un 6})=1-\left(\frac56\right)^3=1-\frac{125}{216}=\res{\frac{91}{216}}\approx0{,}42$."),
 (3, r"Llancem dos daus. Siguen $A=$ «la suma és 7» i $B=$ «algun dels daus és un 6». Calcula $P(A)$, $P(B)$, $P(A\cap B)$ i $P(A\cup B)$.",
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
UR = tree([('I', r'\frac13', [('R*', r'\frac34', [], r'$\frac13\cdot\frac34=\frac14$'), ('B*', r'\frac14', [], '')]), ('II', r'\frac23', [('R*', r'\frac14', [], r'$\frac23\cdot\frac14=\frac16$'), ('B*', r'\frac34', [], '')])], ld=18, sd=(16, 8))
CTt = ctab(['', 'Esport federat', 'No federat', 'Total'], [['Xics', '70', '', '180'], ['Xiques', '', '', ''], ['Total', '120', '', '400']])
CTs = ctab(['', 'Esport federat', 'No federat', 'Total'], [['Xics', '70', '110', '180'], ['Xiques', '50', '170', '220'], ['Total', '120', '280', '400']])
S_.append(("Extraccions amb i sense reemplaçament. Problemes", [
 (1, r"En una bossa hi ha 3 boles blanques (B) i 2 de negres (N). En traiem dues \textbf{amb reemplaçament}. Fes el diagrama d'arbre i calcula la probabilitat que: a) les dues siguen blanques; b) les dues siguen negres; c) n'isca una de cada color."
     + recorda(r"\textbf{Amb reemplaçament} tornem la bola a la bossa: la segona extracció té les mateixes probabilitats. \textbf{Sense reemplaçament} no la tornem: en la segona extracció hi ha una bola menys."),
     cen(btree(3, 2, True)) + r"a) $\frac35\cdot\frac35=\res{\frac9{25}}$. \ b) $\frac25\cdot\frac25=\res{\frac4{25}}$. \ c) $\frac6{25}+\frac6{25}=\res{\frac{12}{25}}$."),
 (1, r"Resol l'exercici anterior traient les dues boles \textbf{sense reemplaçament}.",
     cen(btree(3, 2, False)) + r"a) $\frac35\cdot\frac24=\res{\frac3{10}}$. \ b) $\frac25\cdot\frac14=\res{\frac1{10}}$. \ c) $\frac3{10}+\frac3{10}=\res{\frac35}$. \ (Sumen 1 \checkmark)"),
 (2, r"Traiem dues cartes d'una baralla espanyola de 40 cartes, sense reemplaçament. Calcula la probabilitat que: a) les dues siguen asos; b) cap no siga un as.",
     r"a) $\frac4{40}\cdot\frac3{39}=\frac{12}{1560}=\res{\frac1{130}}$. \ b) $\frac{36}{40}\cdot\frac{35}{39}=\frac{1260}{1560}=\res{\frac{21}{26}}\approx0{,}81$."),
 (2, r"En una bossa hi ha 5 boles roges, 3 de blaves i 2 de verdes. En traiem dues sense reemplaçament. Calcula la probabilitat que: a) les dues siguen roges; b) les dues siguen del mateix color." + cen(bag('RRRRRBBBVV', per=5)),
     r"a) $\frac5{10}\cdot\frac49=\frac{20}{90}=\res{\frac29}$. \ b) $\frac{20}{90}+\frac3{10}\cdot\frac29+\frac2{10}\cdot\frac19=\frac{20+6+2}{90}=\frac{28}{90}=\res{\frac{14}{45}}$."),
 (2, r"En un institut hi ha 400 alumnes, dels quals 180 són xics. Fan esport federat 120 alumnes, 70 dels quals són xics. Completa la taula i, si triem una persona a l'atzar, calcula: a) $P(\text{esport federat})$; b) $P(\text{xica i esport federat})$; c) $P(\text{xica o esport federat})$; d) si sabem que és una xica, la probabilitat que faça esport federat."
     + cen(CTt),
     cen(CTs) + r"a) $\frac{120}{400}=\res{\frac3{10}}$. \ b) $\frac{50}{400}=\res{\frac18}$. \ c) $\frac{220+120-50}{400}=\frac{290}{400}=\res{\frac{29}{40}}$. \ d) Només comptem les 220 xiques: $\frac{50}{220}=\res{\frac5{22}}$."),
 (2, r"La urna I té 3 boles roges i 1 de blava; la urna II té 1 bola roja i 3 de blaves. Llancem un dau: si ix 1 o 2, traiem una bola de la urna I, i si no, de la urna II. Quina és la probabilitat de traure una bola roja?",
     cen(UR) + r"$P(R)=\frac13\cdot\frac34+\frac23\cdot\frac14=\frac14+\frac16=\res{\frac5{12}}$."),
 (3, r"En una caixa hi ha 10 bombetes, 3 de les quals són defectuoses. En provem dues a l'atzar (sense reemplaçament). Quina és la probabilitat que almenys una siga defectuosa?",
     r"Contrari: cap defectuosa, $\frac7{10}\cdot\frac69=\frac{42}{90}=\frac7{15}$. \ $P=1-\frac7{15}=\res{\frac8{15}}$."),
 (3, r"En una bossa hi ha 4 boles roges i 2 de blaves. En traiem tres, una darrere l'altra, sense reemplaçament. Quina és la probabilitat que les tres siguen roges?",
     r"$\frac46\cdot\frac35\cdot\frac24=\frac{24}{120}=\res{\frac15}$."),
 (3, r"L'Anna i en Biel llancen una moneda per torns i guanya qui trau cara primer. Comença l'Anna. Calcula la probabilitat que: a) l'Anna guanye en la primera tirada; b) en Biel guanye en la seua primera tirada; c) algú guanye en les dues primeres tirades.",
     r"a) $\res{\frac12}$. \ b) L'Anna ha de traure creu i en Biel cara: $\frac12\cdot\frac12=\res{\frac14}$. \ c) $\frac12+\frac14=\res{\frac34}$ (o bé $1-P(XX)=1-\frac14$)."),
]))

# =====================================================================
pre_ = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre_ = pre_.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\usepackage{pifont}\n\\usetikzlibrary{trees}\n'
KW = "pdfkeywords={probabilitat, experiment aleatori, espai mostral, esdeveniments, llei de Laplace, llei dels grans nombres, freqüència relativa, diagrama d'arbre, reemplaçament}"
pre_ = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre_)
pre_ = pre_.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre_ += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
TITOL = 'Probabilitat'

def build(sol_):
    t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
    p = pre_.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                     "pdftitle={%s de la unitat 12: %s. 3r d'ESO}" % (t, TITOL))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 12: %s · 3r d'ESO" % (t, TITOL))
    assert 'Unitat 12' in p and 'unitat 12' in p
    out = [p]
    if sol_: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n\\newcommand{\\rest}[1]{\\fbox{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n\\newcommand{\\rest}[1]{#1}\n')
    out.append(r'''
\def\fmneed{14}
\input{../comu/fentmates.tex}
\fmcurs{3eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{3r ESO}{''' + ('Solucions de la fitxa · Unitat 12' if sol_ else "Fitxa d'exercicis · Unitat 12") + '}{' + TITOL + r'''}
''')
    if not sol_:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs simulacions, una bossa de boles, la taula dels dos daus i un diagrama d'arbre que calcula les probabilitats pas a pas. Les probabilitats es donen en fracció irreductible (o en decimal, si les dades ho són)."
             if sol_ else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos: escriu l'espai mostral, fes un diagrama d'arbre o una taula quan calga i dona les probabilitats en forma de fracció irreductible (o en decimal, si les dades ho són).") + r'''
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
    name = 't12-fitxa-solucions.tex' if sol_ else 't12-fitxa-exercicis.tex'
    with open(os.path.join(HERE, name), 'w', encoding='utf-8') as fh: fh.write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
