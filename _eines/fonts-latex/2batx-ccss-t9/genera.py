# Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 9: Probabilitat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Els exercicis marcats amb \pau{...} són de la PAU d'altres comunitats (recopilació «Estadística y probabilidad en pruebas
# de acceso a la universidad de todas las comunidades de España» de www.ebaumatematicas.com, curs 2026/27), traduïts al
# valencià; si un apartat necessitava contingut posterior, l'exercici va a la secció corresponent o se n'ha llevat l'apartat.
# Totes les probabilitats de les solucions es calculen ací amb fraccions exactes (o per recompte de l'espai mostral) i
# CHK (al final) les compara amb les solucions oficials. Les solucions inclouen arbres, taules de contingència i diagrames
# de Venn dibuixats amb TikZ.
# Ús: python3 genera.py && pdflatex t9-fitxa-exercicis.tex (dues vegades) && pdflatex t9-fitxa-solucions.tex (dues vegades)
import os, re
from fractions import Fraction as F
from itertools import product, permutations
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

# ---------- nombres ----------
def p10(d):
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    return d == 1
def dec(x, k=4):
    s = ('%.*f' % (k, float(x))).rstrip('0').rstrip('.')
    return s.replace('.', '{,}')
def N(x):
    """valor exacte: decimal si és exacte, fracció i aproximació si no"""
    x = F(x)
    if p10(x.denominator) and x.denominator <= 10**6: return dec(x, 6)
    return r'\frac{%d}{%d}\approx %s' % (x.numerator, x.denominator, dec(x))
def Q(x):
    """només la fracció (o el decimal exacte)"""
    x = F(x)
    if p10(x.denominator) and x.denominator <= 10**6: return dec(x, 6)
    return r'\frac{%d}{%d}' % (x.numerator, x.denominator)
def pc(x): return dec(F(x) * 100, 2) + r'\,\%'
def B(x): return r'\res{' + N(x) + '}'

# ---------- figures ----------
def venn(v1, v2, v3, v0, la='A', lb='B'):
    """diagrama de Venn amb la probabilitat de cada regió: només A, A∩B, només B, cap"""
    return (r'\begin{tikzpicture}[scale=.62,baseline=(current bounding box.center)]'
            r'\draw[muted,rounded corners=3pt] (-2.9,-1.75) rectangle (2.9,1.75);'
            r'\fill[accent!12] (-0.65,0) circle (1.35); \fill[teal!14] (0.65,0) circle (1.35);'
            r'\draw[navy,thick] (-0.65,0) circle (1.35); \draw[navy,thick] (0.65,0) circle (1.35);'
            r'\node[font=\small\bfseries] at (-1.75,1.25) {$%s$}; \node[font=\small\bfseries] at (1.75,1.25) {$%s$};'
            r'\node[font=\scriptsize] at (-1.25,0) {$%s$}; \node[font=\scriptsize] at (0,0) {$%s$}; \node[font=\scriptsize] at (1.25,0) {$%s$};'
            r'\node[font=\scriptsize] at (2.25,-1.45) {$%s$};\end{tikzpicture}') % (la, lb, Q(v1), Q(v2), Q(v3), Q(v0))
def taula(rl, cl, M, fmt=Q):
    """taula de contingència: rl, cl etiquetes (sense el total); M matriu de valors amb els totals"""
    cols = 'l|' + 'c' * len(cl) + '|c'
    o = [r'{\small\renewcommand{\arraystretch}{1.25}\begin{tabular}{%s}' % cols, ' & ' + ' & '.join('$%s$' % c for c in cl) + r' & \textbf{Total}\\\hline']
    for i, r in enumerate(rl + [r'\textbf{Total}']):
        if i == len(rl): o.append(r'\hline')
        o.append(('$%s$' % r if i < len(rl) else r) + ' & ' + ' & '.join('$%s$' % fmt(v) for v in M[i]) + r'\\')
    o.append(r'\end{tabular}}')
    return '\n'.join(o)
def ct(a, b, ab, la='A', lb='B', fmt=Q, tot=1):
    """taula 2×2 a partir de P(A), P(B) i P(A∩B)"""
    a, b, ab = F(a), F(b), F(ab)
    M = [[ab, a - ab, a], [b - ab, tot - a - b + ab, tot - a], [b, tot - b, tot]]
    assert all(v >= 0 for r in M for v in r)
    return taula([la, r'\overline{%s}' % la], [lb, r'\overline{%s}' % lb], M, fmt)
def arbre(br, l=(2.4, 2.6), s=(2.6, 1.3), root=''):
    """arbre de probabilitats: br = [(etiqueta, prob, fills)], fills = [(etiqueta, prob, text de la fulla)]"""
    def p(x): return r'\scriptsize$%s$' % (Q(x) if not isinstance(x, str) else x)
    o = [r"\begin{tikzpicture}[grow'=right,sloped,level 1/.style={level distance=%gcm,sibling distance=%gcm},"
         r'level 2/.style={level distance=%gcm,sibling distance=%gcm},every node/.style={font=\small},'
         r'edge from parent/.style={draw=muted,thick},baseline=(current bounding box.center)]' % (l[0], s[0], l[1], s[1]),
         r'\node[circle,fill=navy,inner sep=1.6pt,label=left:{\scriptsize %s}] {}' % root]
    def pos(j, n): return 'above' if 2 * j + 1 <= n else 'below'
    for i, (lab, pr, kids) in enumerate(br):
        o.append(r'  child {node {$%s$}' % lab)
        for j, (kl, kp, leaf) in enumerate(kids):
            o.append(r'    child {node[anchor=west] {$%s$%s} edge from parent node[%s] {%s}}' % (kl, (r'\ \ {\color{teal}\scriptsize$%s$}' % leaf) if leaf else '', pos(j, len(kids)), p(kp)))
        o.append(r'    edge from parent node[%s] {%s}}' % (pos(i, len(br)), p(pr)))
    o.append(';\\end{tikzpicture}')
    return '\n'.join(o)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'

CHK = []  # (calculat, oficial o esperat): es comprova al final
def ck(x, y, tol=None):
    CHK.append((x, y, tol)); return x

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Espai mostral i operacions
E = set(range(1, 7)); A1, B1, C1 = {1, 2, 3}, {2, 4, 6}, {5, 6}
def st(s): return r'\{' + ',\\,'.join(str(x) for x in sorted(s)) + r'\}' if s else r'\varnothing'
ck(A1 | B1, {1, 2, 3, 4, 6}); ck(E - (A1 | C1), {4}); ck((E - A1) & (E - B1), {5})
E8 = set(range(1, 9)); A2, B2 = {1, 2, 3, 4}, {2, 4, 6, 8}
ck(E8 - (A2 | B2), (E8 - A2) & (E8 - B2)); ck(E8 - (A2 & B2), (E8 - A2) | (E8 - B2))
S.append(("Espai mostral i operacions amb successos", [
 (1, r"Escriu l'espai mostral dels experiments següents i digues quants elements té:" + tasks(1, [
      r"Llançar una moneda i un dau.", r"Anotar, per ordre de naixement, si cadascun dels tres fills d'una família és xic ($X$) o xica ($Y$).",
      r"Traure, una darrere l'altra i sense reemplaçament, dues boles d'una urna que en té una de roja ($R$), una de blava ($B$) i una de verda ($V$).",
      r"Llançar un dau fins que isca un 6 i anotar el nombre de tirades que han calgut."]),
     tasks(1, [r"$E=\{C1,C2,\dots,C6,\ {+}1,{+}2,\dots,{+}6\}$: \rest{12 elements}.", r"$E=\{XXX,XXY,XYX,XYY,YXX,YXY,YYX,YYY\}$: \rest{8 elements}.",
               r"$E=\{RB,RV,BR,BV,VR,VB\}$: \rest{6 elements} (l'ordre importa i no es pot repetir el color).",
               r"$E=\{1,2,3,4,\dots\}$: és un espai mostral \rest{infinit} (numerable)."])),
 (1, r"Llancem un dau i considerem els successos $A=$«eixir un nombre menor que 4», $B=$«eixir parell» i $C=$«eixir 5 o 6». Calcula:" + tasks(4, [
      r"$A\cup B$", r"$A\cap B$", r"$\co A$", r"$\co B$", r"$A-B$", r"$B\cap C$", r"$\co A\cap\co B$", r"$\overline{A\cup C}$"])
     + r"Quins parells d'aquests successos són incompatibles?",
     r"$A=\{1,2,3\}$, $B=\{2,4,6\}$, $C=\{5,6\}$." + tasks(4, [r"$%s$" % st(A1 | B1), r"$%s$" % st(A1 & B1), r"$%s$" % st(E - A1), r"$%s$" % st(E - B1),
      r"$%s$" % st(A1 - B1), r"$%s$" % st(B1 & C1), r"$%s$" % st((E - A1) & (E - B1)), r"$%s$" % st(E - (A1 | C1))])
     + r"Només \rest{$A$ i $C$} són incompatibles: $A\cap C=\varnothing$. ($A\cap B=\{2\}$ i $B\cap C=\{6\}$ no són buits.)"),
 (1, r"Siguen $M=$«un alumne aprova Matemàtiques» i $N=$«aprova Anglés». Expressa amb operacions entre $M$ i $N$ els successos següents:" + tasks(2, [
      r"Aprova les dues.", r"No n'aprova cap.", r"Aprova només Matemàtiques.", r"Aprova com a molt una.", r"Aprova almenys una.", r"Aprova exactament una.", r"Suspén alguna de les dues."])
     + recorda(r"«almenys un» és la unió; «tots dos», la intersecció; «cap» és $\co M\cap\co N=\overline{M\cup N}$ (De Morgan)."),
     tasks(2, [r"$\res{M\cap N}$", r"$\res{\co M\cap\co N=\overline{M\cup N}}$", r"$\res{M\cap\co N=M-N}$", r"$\res{\overline{M\cap N}=\co M\cup\co N}$", r"$\res{M\cup N}$",
               r"$\res{(M\cap\co N)\cup(\co M\cap N)}$", r"$\res{\co M\cup\co N}$ (el mateix que «com a molt una»)."])),
 (1, r"En l'espai mostral $E=\{1,2,3,4,5,6,7,8\}$ considerem $A=\{1,2,3,4\}$ i $B=\{2,4,6,8\}$. Comprova les dues lleis de De Morgan.",
     r"$\overline{A\cup B}=\overline{%s}=%s$ i $\co A\cap\co B=%s\cap%s=%s$: \rest{coincideixen}." % (st(A2 | B2), st(E8 - (A2 | B2)), st(E8 - A2), st(E8 - B2), st((E8 - A2) & (E8 - B2)))
     + r"\par $\overline{A\cap B}=\overline{%s}=%s$ i $\co A\cup\co B=%s$: \rest{coincideixen}." % (st(A2 & B2), st(E8 - (A2 & B2)), st((E8 - A2) | (E8 - B2)))),
 (2, r"Siguen $A$, $B$ i $C$ tres successos d'un mateix experiment. Expressa amb operacions:" + tasks(2, [
      r"Ocorre només $A$.", r"Ocorre almenys un dels tres.", r"No n'ocorre cap.", r"N'ocorre exactament un.", r"Ocorren tots tres.", r"N'ocorren almenys dos."]),
     tasks(1, [r"$\res{A\cap\co B\cap\co C}$", r"$\res{A\cup B\cup C}$", r"$\res{\co A\cap\co B\cap\co C=\overline{A\cup B\cup C}}$",
               r"$\res{(A\cap\co B\cap\co C)\cup(\co A\cap B\cap\co C)\cup(\co A\cap\co B\cap C)}$", r"$\res{A\cap B\cap C}$", r"$\res{(A\cap B)\cup(A\cap C)\cup(B\cap C)}$"])),
]))

# =====================================================================
# 2. Laplace
D2 = list(product(range(1, 7), repeat=2))
def pd(f): return F(sum(1 for a, b in D2 if f(a, b)), 36)
L1 = [pd(lambda a, b: a + b == 9), pd(lambda a, b: a + b <= 4), pd(lambda a, b: a * b == 12), pd(lambda a, b: a % 2 == 0 and b % 2 == 0), pd(lambda a, b: abs(a - b) >= 3)]
ck(L1, [F(1, 9), F(1, 6), F(1, 9), F(1, 4), F(1, 3)])
M3 = list(product('C+', repeat=3))
pk = F(1, 10)  # dau carregat: 5p + 1/2 = 1
ck(5 * pk + F(1, 2), 1)
S.append(("Probabilitat. Regla de Laplace", [
 (1, r"Una urna conté 4 boles roges, 5 de blaves i 3 de verdes. Traiem una bola a l'atzar. Calcula la probabilitat que:" + tasks(4, [r"siga roja;", r"no siga verda;", r"siga roja o blava;", r"siga groga."]),
     tasks(4, [r"$\frac{4}{12}=" + B(F(4, 12)) + "$", r"$\frac{9}{12}=" + B(F(9, 12)) + "$", r"$\frac{9}{12}=" + B(F(9, 12)) + "$", r"$\res{0}$ (impossible)"])),
 (1, r"Traiem una carta d'una baralla espanyola de 40 cartes (quatre pals de deu cartes: de l'1 al 7, sota, cavall i rei). Calcula la probabilitat de traure:" + tasks(2, [
      r"un or;", r"una figura (sota, cavall o rei);", r"un or o una figura;", r"una carta que no siga ni or ni figura;", r"un as que no siga d'ors."]),
     tasks(2, [r"$\frac{10}{40}=" + B(F(1, 4)) + "$", r"$\frac{12}{40}=" + B(F(12, 40)) + "$", r"$\frac{10+12-3}{40}=" + B(F(19, 40)) + "$ (les 3 figures d'ors es compten dues vegades)",
               r"$1-\frac{19}{40}=" + B(F(21, 40)) + "$", r"$\res{\frac{3}{40}}$"])),
 (1, r"\pau{Castella i Lleó, EBAU ordinària 2020} Es llança una moneda tres vegades. Calcula la probabilitat d'obtindre almenys una creu.",
     r"Hi ha $2^3=8$ resultats equiprobables i només $CCC$ no té cap creu: $P=1-\frac18=" + B(ck(1 - F(sum(1 for m in M3 if '+' not in m), 8), F(7, 8))) + "$."),
 (1, r"\pau{Castella i Lleó, EBAU extraordinària 2024} Una botiga d'animals fa un sorteig amb paperetes de tres xifres. El número premiat s'obté traient a l'atzar cada xifra, per separat i amb reemplaçament, d'una bossa amb boles del 0 al 9. Calcula la probabilitat que el número premiat acabe en 55.",
     r"Hi ha 1000 números possibles (000 a 999) i acaben en 55 els 10 de la forma $x55$: $P=\frac{10}{1000}=" + B(ck(F(10, 1000), F(1, 100))) + "$."),
 (1, r"Llancem dos daus. Calcula la probabilitat que:" + tasks(2, [r"la suma siga 9;", r"la suma siga com a molt 4;", r"el producte siga 12;", r"els dos resultats siguen parells;", r"la diferència entre els dos resultats siga almenys 3."]),
     r"Hi ha $6\cdot6=36$ parelles equiprobables." + tasks(2, [r"(3,6), (4,5), (5,4), (6,3): $\frac{4}{36}=" + B(L1[0]) + "$", r"6 parelles: $\frac{6}{36}=" + B(L1[1]) + "$",
      r"(2,6), (3,4), (4,3), (6,2): $" + B(L1[2]) + "$", r"$3\cdot3=9$ parelles: $" + B(L1[3]) + "$", r"$6+4+2=12$ parelles: $" + B(L1[4]) + "$"])),
 (2, r"\pau{Illes Balears, PBAU juliol 2018} Un dau està carregat de manera que la probabilitat d'obtindre un 6 és $\frac12$ i les probabilitats d'obtindre cadascuna de les altres cares són iguals a $p$. Es llança aquest dau; calcula la probabilitat de cada un dels successos següents:" + tasks(2, [
      r"S'obté un dos.", r"No s'obté un tres.", r"S'obté un nombre parell.", r"S'obté un nombre senar."]),
     r"$5p+\frac12=1\Rightarrow p=\frac{1}{10}$." + tasks(2, [r"$" + B(ck(pk, F(1, 10))) + "$", r"$1-\frac1{10}=" + B(ck(1 - pk, F(9, 10))) + "$",
      r"$\frac1{10}+\frac1{10}+\frac12=" + B(ck(2 * pk + F(1, 2), F(7, 10))) + "$", r"$3\cdot\frac1{10}=" + B(ck(3 * pk, F(3, 10))) + "$"])),
 (2, r"\pau{Andalusia, PEvAU ordinària 2023} Tenim una moneda trucada en què la probabilitat d'obtindre cara és el doble que la d'obtindre creu." + tasks(1, [
      r"Calcula la probabilitat d'obtindre cara en llançar la moneda.", r"Calcula la probabilitat d'obtindre una cara i una creu, sense importar l'ordre, en llançar dues vegades la moneda.",
      r"Calcula la probabilitat d'obtindre almenys una cara en llançar dues vegades la moneda."]),
     r"$P(C)=2P({+})$ i $P(C)+P({+})=1$." + tasks(1, [r"$3P({+})=1\Rightarrow P(C)=" + B(ck(F(2, 3), F(2, 3))) + "$",
      r"$P(C{+})+P({+}C)=2\cdot\frac23\cdot\frac13=" + B(ck(2 * F(2, 3) * F(1, 3), F(4, 9))) + "$ (els resultats ja no són equiprobables: multipliquem)",
      r"$1-P({+}{+})=1-\frac19=" + B(ck(1 - F(1, 9), F(8, 9))) + "$"])),
 (1, r"Triem a l'atzar un nombre de l'1 al 100. Calcula la probabilitat que siga múltiple de 3 o de 5.",
     r"Hi ha 33 múltiples de 3, 20 de 5 i 6 de 15 (comptats dues vegades): $P=\frac{33+20-6}{100}=" + B(ck(F(sum(1 for k in range(1, 101) if k % 3 == 0 or k % 5 == 0), 100), F(47, 100))) + "$."),
 (1, r"Llancem tres monedes. Calcula la probabilitat d'obtindre exactament dues cares i la d'obtindre més cares que creus.",
     r"De les 8 ternes, tenen dues cares $CC{+}$, $C{+}C$ i ${+}CC$: $" + B(ck(F(sum(1 for m in M3 if m.count('C') == 2), 8), F(3, 8))) + "$. Més cares que creus (2 o 3 cares): $\\frac{3+1}{8}=" + B(ck(F(sum(1 for m in M3 if m.count('C') >= 2), 8), F(1, 2))) + "$."),
 (2, r"Raona si les afirmacions següents són vertaderes o falses:" + tasks(1, [r"Si llancem dos daus i sumem, la probabilitat de cada suma és $\frac1{11}$, perquè hi ha 11 sumes possibles.",
      r"Si una moneda equilibrada ha eixit cara cinc vegades seguides, és més probable que la sisena vegada isca creu.", r"Pot ser que $P(A)=1{,}2$ si $A$ és un succés molt probable."]),
     tasks(1, [r"\rest{Falsa}: les sumes no són equiprobables (el 7 té 6 parelles i el 2 només una). Hem d'aplicar Laplace a les 36 parelles.",
               r"\rest{Falsa}: els llançaments són independents; la probabilitat continua sent $\frac12$.", r"\rest{Falsa}: tota probabilitat està entre 0 i 1."])),
]))

# =====================================================================
# 3. Fórmules
a, b, u = F('0.45'), F('0.3'), F('0.6'); i3 = a + b - u
ck([i3, 1 - u, a - i3, 1 - i3, u - i3], [F('0.15'), F('0.4'), F('0.3'), F('0.85'), F('0.45')])
ma, mb, mu = F('0.4'), F('0.6'), F('0.8'); mi = ma + mb - mu
nA, nB, nAuB = F('0.7'), F('0.4'), F('0.9'); a18, b18, i18 = 1 - nA, 1 - nB, 1 - nAuB
S.append(("Fórmules de la probabilitat", [
 (1, r"Siguen $A$ i $B$ dos successos amb $P(A)=0{,}45$, $P(B)=0{,}3$ i $P(A\cup B)=0{,}6$. Calcula:" + tasks(3, [r"$P(A\cap B)$", r"$P(\co A\cap\co B)$", r"$P(A\cap\co B)$", r"$P(\co A\cup\co B)$", r"$P(\text{només un dels dos})$"])
     + recorda(r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$; \ $P(\co A)=1-P(A)$; \ $P(A\cap\co B)=P(A)-P(A\cap B)$; \ De Morgan: $\co A\cap\co B=\overline{A\cup B}$ i $\co A\cup\co B=\overline{A\cap B}$."),
     tasks(2, [r"$0{,}45+0{,}3-0{,}6=" + B(i3) + "$", r"$1-0{,}6=" + B(1 - u) + "$", r"$0{,}45-0{,}15=" + B(a - i3) + "$", r"$1-0{,}15=" + B(1 - i3) + "$", r"$0{,}6-0{,}15=" + B(u - i3) + "$"])
     + cen(venn(a - i3, i3, b - i3, 1 - u))),
 (1, r"\pau{Madrid, EvAU juliol 2018} Siguen $A$ i $B$ dos successos d'un experiment aleatori tals que $P(A)=0{,}4$, $P(B)=0{,}6$ i $P(A\cup B)=0{,}8$. Calcula $P(\co A\cap B)$ i $P(\co A\cup\co B)$.",
     r"$P(A\cap B)=0{,}4+0{,}6-0{,}8=0{,}2$. \ $P(\co A\cap B)=P(B)-P(A\cap B)=" + B(ck(mb - mi, F('0.4'))) + r"$; \ $P(\co A\cup\co B)=1-P(A\cap B)=" + B(1 - mi) + "$."),
 (1, r"De dos successos se sap que $P(\co A)=0{,}7$, $P(\co B)=0{,}4$ i $P(\co A\cup\co B)=0{,}9$. Calcula $P(A)$, $P(B)$, $P(A\cap B)$, $P(A\cup B)$ i $P(\co A\cap\co B)$.",
     r"$P(A)=" + B(a18) + r"$, $P(B)=" + B(b18) + r"$. De Morgan: $P(A\cap B)=1-P(\co A\cup\co B)=" + B(i18) + r"$; \ $P(A\cup B)=0{,}3+0{,}6-0{,}1=" + B(a18 + b18 - i18) + r"$; \ $P(\co A\cap\co B)=1-0{,}8=" + B(ck(1 - (a18 + b18 - i18), F('0.2'))) + "$."),
 (1, r"Els successos $A$ i $B$ són incompatibles, amb $P(A)=0{,}35$ i $P(B)=0{,}4$. Calcula $P(A\cup B)$, $P(\co A\cap\co B)$, $P(A\cap\co B)$ i $P(\co A\cup\co B)$.",
     r"$P(A\cap B)=0$: $P(A\cup B)=" + B(F('0.75')) + r"$; \ $P(\co A\cap\co B)=" + B(F('0.25')) + r"$; \ $P(A\cap\co B)=P(A)=" + B(F('0.35')) + r"$; \ $P(\co A\cup\co B)=1-0=\res{1}$."),
 (2, r"Siguen $A$ i $B$ dos successos amb $P(A)=0{,}6$ i $P(B)=0{,}7$." + tasks(1, [r"Poden ser incompatibles?", r"Entre quins valors pot estar $P(A\cap B)$?", r"I $P(A\cup B)$?"]),
     tasks(1, [r"\rest{No}: si ho foren, $P(A\cup B)=0{,}6+0{,}7=1{,}3>1$.", r"Com que $P(A\cup B)\leq1$, $P(A\cap B)=1{,}3-P(A\cup B)\geq0{,}3$; i $A\cap B\subset A$, així que $P(A\cap B)\leq0{,}6$: \ $\res{0{,}3\leq P(A\cap B)\leq0{,}6}$.",
               r"$P(A\cup B)=1{,}3-P(A\cap B)$: \ $\res{0{,}7\leq P(A\cup B)\leq1}$."])),
 (2, r"Tres successos $A$, $B$ i $C$ tenen probabilitat $0{,}4$ cadascun; les interseccions de dos en dos tenen probabilitat $0{,}15$ i $P(A\cap B\cap C)=0{,}05$. Calcula la probabilitat que n'ocórrega almenys un i que no n'ocórrega cap.",
     r"$P(A\cup B\cup C)=3\cdot0{,}4-3\cdot0{,}15+0{,}05=" + B(ck(3 * F('0.4') - 3 * F('0.15') + F('0.05'), F('0.8'))) + r"$; \ $P(\text{cap})=1-0{,}8=" + B(F('0.2')) + "$."),
]))

# =====================================================================
# 4. Amb l'espai mostral i sense
pA = pd(lambda x, y: (x + y) % 2 == 0); pB = pd(lambda x, y: 6 in (x, y)); pAB = pd(lambda x, y: (x + y) % 2 == 0 and 6 in (x, y)); pU = pd(lambda x, y: (x + y) % 2 == 0 or 6 in (x, y))
ck([pA, pB, pAB, pU, pA + pB - pAB], [F(1, 2), F(11, 36), F(5, 36), F(2, 3), pU])
T30 = range(1, 31); q2 = F(sum(1 for k in T30 if k % 2 == 0 or k % 3 == 0), 30); q1 = F(sum(1 for k in T30 if (k % 2 == 0) != (k % 3 == 0)), 30)
ck([q2, q1, 1 - q2], [F(2, 3), F(1, 2), F(1, 3)])
# Galícia 2024: P(L ∪ M) = 0,8, P(L ∩ M) = 0,35, P(no L) = 0,6
gL, gU, gI = F('0.4'), F('0.8'), F('0.35'); gM = gU - gL + gI
# Andalusia 2022: P(V) = 0,65, P(L) = 0,45, cap = 0,15
vV, vL, vU = F('0.65'), F('0.45'), F('0.85'); vI = vV + vL - vU
pP, pT, pN = F('0.55'), F('0.4'), F('0.25'); pI = pP + pT - (1 - pN)
S.append(("Càlcul de probabilitats coneixent l'espai mostral i sense conéixer-lo", [
 (1, r"Llancem dos daus i considerem els successos $A=$«la suma és parella» i $B=$«almenys un dels daus és un 6». Calcula $P(A)$, $P(B)$ i $P(A\cap B)$ per recompte i, amb la fórmula, $P(A\cup B)$. Comprova el resultat comptant els casos de $A\cup B$.",
     r"$P(A)=\frac{18}{36}=" + B(pA) + r"$, \ $P(B)=" + B(pB) + r"$, \ $A\cap B=\{(2,6),(4,6),(6,6),(6,2),(6,4)\}$: $P(A\cap B)=" + B(pAB) + r"$." +
     r"\par $P(A\cup B)=\frac{18+11-5}{36}=\frac{24}{36}=" + B(pU) + r"$. Comptant: les 18 parelles de suma parella més les 6 amb un 6 i suma senar, $(1,6),(3,6),(5,6),(6,1),(6,3),(6,5)$: 24 casos. \rest{Coincideix.}"),
 (1, r"Traiem a l'atzar una targeta d'una caixa amb targetes numerades de l'1 al 30. Siguen $A=$«el nombre és parell» i $B=$«el nombre és múltiple de 3». Calcula, aplicant les fórmules, la probabilitat que siga parell o múltiple de 3, que complisca només una de les dues condicions i que no en complisca cap.",
     r"$P(A)=\frac{15}{30}$, $P(B)=\frac{10}{30}$, $P(A\cap B)=P(\text{múltiple de 6})=\frac{5}{30}$." + tasks(1, [r"$P(A\cup B)=\frac{15+10-5}{30}=" + B(q2) + "$",
      r"$P(A\cup B)-P(A\cap B)=\frac{20-5}{30}=" + B(q1) + "$", r"$1-P(A\cup B)=" + B(1 - q2) + "$"])),
 (1, r"\pau{Galícia, ABAU extraordinària 2024} En una enquesta, el 80\,\% dels entrevistats diu que llig o escolta música, el 35\,\% fa les dues coses i el 60\,\% no llig. Calcula les probabilitats que una persona triada a l'atzar:" + tasks(1, [
      r"escolte música i no llija;", r"llija i no escolte música;", r"faça només una de les dues coses."]),
     r"$P(L)=1-0{,}6=0{,}4$ i $P(M)=0{,}8-0{,}4+0{,}35=0{,}75$." + tasks(1, [r"$P(M\cap\co L)=P(M)-P(M\cap L)=" + B(ck(gM - gI, F('0.4'))) + "$", r"$P(L\cap\co M)=0{,}4-0{,}35=" + B(ck(gL - gI, F('0.05'))) + "$",
      r"$0{,}4+0{,}05=" + B(ck(gU - gI, F('0.45'))) + "$"]) + cen(ct(gL, gM, gI, 'L', 'M'))),
 (1, r"\pau{Andalusia, PEvAU ordinària 2022} En el seu temps lliure, el 65\,\% dels estudiants d'un centre juga a videojocs, el 45\,\% llig llibres i el 15\,\% no fa cap de les dues coses. Triem un estudiant a l'atzar. Calcula la probabilitat que:" + tasks(1, [
      r"jugue a videojocs o llija llibres;", r"jugue a videojocs i no llija llibres."]),
     tasks(1, [r"De Morgan: $P(V\cup L)=1-P(\co V\cap\co L)=1-0{,}15=" + B(ck(vU, F('0.85'))) + "$", r"$P(V\cap L)=0{,}65+0{,}45-0{,}85=0{,}25\Rightarrow P(V\cap\co L)=0{,}65-0{,}25=" + B(ck(vV - vI, F('0.4'))) + "$"])
     + cen(ct(vV, vL, vI, 'V', 'L'))),
 (1, r"En una ciutat, el 55\,\% dels habitants llig la premsa, el 40\,\% veu les notícies a la televisió i el 25\,\% no fa cap de les dues coses. Construeix la taula de contingència i calcula la probabilitat que un habitant triat a l'atzar:" + tasks(2, [
      r"faça les dues coses;", r"només llija la premsa;", r"faça només una de les dues;", r"llija la premsa o no veja la televisió."]),
     cen(ct(pP, pT, pI, 'P', 'T')) + tasks(2, [r"$" + B(ck(pI, F('0.2'))) + "$", r"$" + B(pP - pI) + "$", r"$0{,}35+0{,}2=" + B(pP - pI + pT - pI) + "$", r"$1-P(\co P\cap T)=1-0{,}2=" + B(1 - (pT - pI)) + "$"])),
 (1, r"En un grup de 30 persones, 18 parlen anglés, 12 francés i 6 no parlen cap dels dos idiomes. Triem una persona a l'atzar. Calcula la probabilitat que parle els dos idiomes, que en parle només un i que parle francés però no anglés.",
     r"Parlen algun idioma $30-6=24$; els dos: $18+12-24=6$." + tasks(3, [r"$\frac{6}{30}=" + B(F(6, 30)) + "$", r"$\frac{24-6}{30}=" + B(F(18, 30)) + "$", r"$\frac{12-6}{30}=" + B(F(6, 30)) + "$"])
     + cen(taula(['A', r'\overline{A}'], ['F', r'\overline{F}'], [[6, 12, 18], [6, 6, 12], [12, 18, 30]], str))),
]))

# =====================================================================
# 5. Condicionada
c_a, c_b, c_i = F('0.5'), F('0.4'), F('0.1'); c_u = c_a + c_b - c_i
m19 = F('0.3'); m19ab = m19 * F('0.4'); m19nab = (1 - m19) * F('0.6'); m19b = m19ab + m19nab
ck([m19ab / m19b, (1 - m19 - m19nab) / (1 - m19b)], [F(2, 9), F(14, 23)])
b17 = F('0.6') * F('0.3')
r17 = F('0.55'); r17u = F('0.9') + F('0.6') - r17
l20 = [F(46, 120), F(34, 120), F(16, 120)]; l20u = l20[0] + l20[1] - l20[2]
i21 = F('0.72') * F('0.64'); i21u = F('0.55') + F('0.72') - i21
mur = {'Veterinària': (30, 10), 'Economia': (25, 12), 'Química': (20, 13), 'Biologia': (15, 8), 'Matemàtiques': (10, 6)}
dones = sum(v[1] for v in mur.values()); homes = 100 - dones
ex39 = F('0.6') * F('0.5'); ex39b = ex39 + F('0.4') * F('0.25')
S.append(("Probabilitat condicionada", [
 (1, r"Siguen $A$ i $B$ dos successos amb $P(A)=0{,}5$, $P(B)=0{,}4$ i $P(A\cap B)=0{,}1$. Calcula:" + tasks(3, [r"$P(A\cond B)$", r"$P(B\cond A)$", r"$P(A\cond\co B)$", r"$P(\co A\cond\co B)$", r"$P(B\cond\co A)$", r"$P(\co B\cond A)$"])
     + recorda(r"$P(A\cond B)=\dfrac{P(A\cap B)}{P(B)}$. El succés que va darrere de la barra és la condició: va al denominador."),
     tasks(3, [r"$\frac{0{,}1}{0{,}4}=" + B(c_i / c_b) + "$", r"$\frac{0{,}1}{0{,}5}=" + B(c_i / c_a) + "$", r"$\frac{0{,}4}{0{,}6}=" + B((c_a - c_i) / (1 - c_b)) + "$",
               r"$\frac{0{,}2}{0{,}6}=" + B((1 - c_u) / (1 - c_b)) + "$", r"$\frac{0{,}3}{0{,}5}=" + B((c_b - c_i) / (1 - c_a)) + "$", r"$1-0{,}2=" + B(1 - c_i / c_a) + "$"])
     + cen(venn(c_a - c_i, c_i, c_b - c_i, 1 - c_u))),
 (2, r"\pau{Madrid, EvAU juliol 2019} Siguen $A$ i $B$ dos successos amb $P(A)=0{,}3$, $P(B\cond A)=0{,}4$ i $P(B\cond\co A)=0{,}6$. Calcula:" + tasks(2, [r"$P(A\cond B)$", r"$P(\co A\cond\co B)$"]),
     r"$P(A\cap B)=0{,}3\cdot0{,}4=0{,}12$; \ $P(\co A\cap B)=0{,}7\cdot0{,}6=0{,}42$; \ $P(B)=0{,}54$; \ $P(\co A\cap\co B)=0{,}7-0{,}42=0{,}28$." +
     tasks(2, [r"$\frac{0{,}12}{0{,}54}=" + B(m19ab / m19b) + "$", r"$\frac{0{,}28}{0{,}46}=" + B((1 - m19 - m19nab) / (1 - m19b)) + "$"])),
 (1, r"\pau{Illes Balears, PBAU setembre 2017} Siguen $A$ i $B$ dos successos amb probabilitats $0{,}4$ i $0{,}6$, respectivament. Se sap que, donat $B$, la probabilitat que ocórrega $A$ és $0{,}3$." + tasks(1, [
      r"Quina és la probabilitat que ocórreguen tots dos successos alhora?", r"Quina és la probabilitat que ocórrega algun dels dos?", r"Quina és la probabilitat que no n'ocórrega cap?"]),
     tasks(1, [r"$P(A\cap B)=P(B)\,P(A\cond B)=0{,}6\cdot0{,}3=" + B(ck(b17, F('0.18'))) + "$", r"$0{,}4+0{,}6-0{,}18=" + B(ck(F('0.4') + F('0.6') - b17, F('0.82'))) + "$", r"$1-0{,}82=" + B(ck(b17, F('0.18'))) + "$"])),
 (1, r"\pau{Andalusia, PEvAU juny 2017} El 90\,\% dels alumnes d'un centre està interessat per les xarxes socials, el 60\,\% per les seues notes i el 55\,\% per les dues coses. Es tria un alumne a l'atzar." + tasks(1, [
      r"Quina és la probabilitat que estiga interessat per alguna de les dues coses?", r"Calcula la probabilitat que estiga interessat per les notes, sabent que no està interessat per les xarxes socials.", r"Calcula la probabilitat que no estiga interessat per cap de les dues coses."]),
     cen(ct(F('0.9'), F('0.6'), r17, 'X', 'N')) + tasks(1, [r"$0{,}9+0{,}6-0{,}55=" + B(ck(r17u, F('0.95'))) + "$", r"$P(N\cond\co X)=\frac{P(N\cap\co X)}{P(\co X)}=\frac{0{,}05}{0{,}1}=" + B(ck(F('0.05') / F('0.1'), F('0.5'))) + "$",
      r"$1-0{,}95=" + B(ck(1 - r17u, F('0.05'))) + "$"])),
 (2, r"\pau{Andalusia, PEvAU ordinària 2020} A 120 estudiants se'ls ha recomanat la lectura de dos llibres: 46 han llegit el primer, 34 el segon i 16 tots dos. Es tria un estudiant a l'atzar. Calcula la probabilitat que:" + tasks(1, [
      r"haja llegit algun dels dos llibres;", r"no n'haja llegit cap;", r"només haja llegit el primer;", r"haja llegit el primer, si se sap que no ha llegit el segon."]),
     cen(taula(['L_1', r'\overline{L_1}'], ['L_2', r'\overline{L_2}'], [[16, 30, 46], [18, 56, 74], [34, 86, 120]], str)) +
     tasks(2, [r"$\frac{64}{120}=" + B(ck(l20u, F(8, 15))) + "$", r"$\frac{56}{120}=" + B(ck(1 - l20u, F(7, 15))) + "$", r"$\frac{30}{120}=" + B(ck(l20[0] - l20[2], F(1, 4))) + "$",
               r"$P(L_1\cond\co L_2)=\frac{30}{86}=" + B(ck((l20[0] - l20[2]) / (1 - l20[1]), F(15, 43))) + "$"])),
 (2, r"\pau{Andalusia, PEvAU ordinària 2021} De les compres fetes en les últimes rebaixes, el 55\,\% van ser de productes electrònics i el 72\,\% es van fer per Internet; de les compres fetes per Internet, el 64\,\% van ser de productes electrònics. Es tria una compra a l'atzar. Calcula la probabilitat que:" + tasks(1, [
      r"haja sigut de productes electrònics i feta per Internet;", r"s'haja fet per Internet o haja sigut de productes electrònics;", r"no s'haja fet per Internet, sabent que no va ser de productes electrònics."]),
     tasks(1, [r"$P(E\cap I)=P(I)\,P(E\cond I)=0{,}72\cdot0{,}64=" + B(ck(i21, F('0.4608'))) + "$", r"$0{,}55+0{,}72-0{,}4608=" + B(ck(i21u, F('0.8092'))) + "$",
               r"$P(\co I\cond\co E)=\frac{P(\co I\cap\co E)}{P(\co E)}=\frac{1-0{,}8092}{0{,}45}=" + B(ck((1 - i21u) / F('0.45'), F(53, 125))) + "$"])),
 (2, r"\pau{Múrcia, PAU extraordinària 2025} En una enquesta a 100 estudiants de segon de Batxillerat, 30 volen estudiar Veterinària, 25 Economia, 20 Química, 15 Biologia i 10 Matemàtiques. D'ells, 10, 12, 13, 8 i 6 són dones, respectivament. Ningú no es pot matricular en més d'un grau. Triem un estudiant a l'atzar. Calcula la probabilitat que:" + tasks(2, [
      r"siga dona;", r"siga home i vulga estudiar Veterinària;", r"vulga estudiar Química o Veterinària;", r"no vulga estudiar ni Biologia ni Matemàtiques;", r"vulga estudiar Química, sabent que és dona;", r"vulga estudiar Economia, sabent que és home."]),
     cen(taula(['D', 'H'], [r'\text{Vet.}', r'\text{Eco.}', r'\text{Quí.}', r'\text{Bio.}', r'\text{Mat.}'], [[v[1] for v in mur.values()] + [dones], [v[0] - v[1] for v in mur.values()] + [homes], [v[0] for v in mur.values()] + [100]], str)) +
     tasks(3, [r"$" + B(ck(F(dones, 100), F('0.49'))) + "$", r"$\frac{20}{100}=" + B(ck(F(30 - 10, 100), F('0.2'))) + "$", r"$\frac{50}{100}=" + B(ck(F(50, 100), F('0.5'))) + "$",
               r"$\frac{75}{100}=" + B(ck(F(100 - 25, 100), F('0.75'))) + "$", r"$\frac{13}{49}=" + B(ck(F(13, dones), F(13, 49))) + "$", r"$\frac{13}{51}=" + B(ck(F(25 - 12, homes), F(13, 51))) + "$"])),
 (2, r"De dos successos se sap que $P(A)=0{,}6$, $P(B\cond A)=0{,}5$ i $P(B\cond\co A)=0{,}25$. Calcula $P(A\cap B)$, $P(B)$, $P(A\cond B)$ i $P(A\cup B)$.",
     r"$P(A\cap B)=0{,}6\cdot0{,}5=" + B(ex39) + r"$; \ $P(\co A\cap B)=0{,}4\cdot0{,}25=0{,}1$, \ $P(B)=" + B(ex39b) + r"$; \ $P(A\cond B)=\frac{0{,}3}{0{,}4}=" + B(ex39 / ex39b) + r"$; \ $P(A\cup B)=0{,}6+0{,}4-0{,}3=" + B(F('0.6') + ex39b - ex39) + "$."),
]))

# =====================================================================
# 6. Independència
g20 = F('0.4') * F('0.75')
o24 = F('0.11') / F('0.275')
v17 = (F('0.2') - F('0.03')) / F('0.4')
s13 = {(x, y) for x, y in D2 if x + y == 3}; s13u = {(x, y) for x, y in D2 if 1 in (x, y)}
pC13, pAB13, pI13 = F(len(s13), 36), F(len(s13u), 36), F(len(s13 & s13u), 36)
S.append(("Independència de successos", [
 (1, r"Els successos $A$ i $B$ són independents, amb $P(A)=0{,}3$ i $P(B)=0{,}5$. Calcula $P(A\cap B)$, $P(A\cup B)$, $P(\co A\cap\co B)$, $P(A\cond B)$ i $P(A\cap\co B)$."
     + recorda(r"$A$ i $B$ són independents si $P(A\cap B)=P(A)\cdot P(B)$. Aleshores també ho són $A$ i $\co B$, $\co A$ i $B$, i $\co A$ i $\co B$."),
     r"$P(A\cap B)=0{,}3\cdot0{,}5=" + B(F('0.15')) + r"$; \ $P(A\cup B)=0{,}3+0{,}5-0{,}15=" + B(F('0.65')) + r"$; \ $P(\co A\cap\co B)=0{,}7\cdot0{,}5=" + B(F('0.35')) + r"$; \ $P(A\cond B)=P(A)=" + B(F('0.3')) + r"$; \ $P(A\cap\co B)=0{,}3\cdot0{,}5=" + B(F('0.15')) + "$."),
 (2, r"Se sap que $P(A)=0{,}4$ i $P(A\cup B)=0{,}7$. Calcula $P(B)$ si:" + tasks(2, [r"$A$ i $B$ són incompatibles;", r"$A$ i $B$ són independents."]),
     tasks(2, [r"$0{,}7=0{,}4+P(B)\Rightarrow P(B)=" + B(F('0.3')) + "$", r"$0{,}7=0{,}4+p-0{,}4p\Rightarrow0{,}6p=0{,}3\Rightarrow p=" + B(ck(F('0.3') / F('0.6'), F('0.5'))) + "$"])),
 (1, r"\pau{Madrid, EvAU extraordinària 2021} Siguen $A$ i $B$ dos successos amb $P(A)=0{,}5$, $P(B)=0{,}8$ i $P(A\cup B)=0{,}9$." + tasks(1, [r"Estudia si els successos $A$ i $B$ són independents.", r"Calcula $P(A\cond\co B)$."]),
     tasks(1, [r"$P(A\cap B)=0{,}5+0{,}8-0{,}9=0{,}4=0{,}5\cdot0{,}8$: \rest{són independents}.", r"$\frac{P(A\cap\co B)}{P(\co B)}=\frac{0{,}1}{0{,}2}=" + B(ck(F('0.1') / F('0.2'), F('0.5'))) + "$ ($=P(A)$, com havia de ser)."])),
 (1, r"\pau{Castella-la Manxa, EvAU setembre 2017} D'un estudi sobre accidents de trànsit es va deduir que el 29\,\% dels conductors superaven els límits d'alcohol en sang, el 14\,\% tenien presència de drogues en sang i el 37\,\% superaven els límits d'alcohol o tenien presència de drogues (o totes dues coses)." + tasks(1, [
      r"Calcula la probabilitat que, en un accident, el conductor supere els límits d'alcohol i tinga presència de drogues en sang.", r"Raona si són independents els successos «superar els límits d'alcohol» i «presència de drogues en sang»."]),
     tasks(1, [r"$0{,}29+0{,}14-0{,}37=" + B(ck(F('0.29') + F('0.14') - F('0.37'), F('0.06'))) + "$", r"$0{,}29\cdot0{,}14=0{,}0406\neq0{,}06$: \rest{no són independents}."])),
 (2, r"\pau{Galícia, ABAU ordinària 2020} Siguen $A$ i $B$ dos successos amb $P(A)=0{,}4$, $P(B)=0{,}7$ i $P(B\cond A)=0{,}75$. Calcula:" + tasks(4, [r"$P(A\cap B)$", r"$P(A\cup\co B)$", r"$P(A\cap\co B)$", r"Són independents?"]),
     tasks(1, [r"$0{,}4\cdot0{,}75=" + B(ck(g20, F('0.3'))) + "$", r"$1-P(\co A\cap B)=1-(0{,}7-0{,}3)=" + B(ck(1 - (F('0.7') - g20), F('0.6'))) + "$", r"$0{,}4-0{,}3=" + B(ck(F('0.4') - g20, F('0.1'))) + "$",
               r"$P(A)P(B)=0{,}28\neq0{,}3$ (o bé $P(B\cond A)=0{,}75\neq P(B)$): \rest{no són independents}."])),
 (1, r"\pau{Andalusia, PEvAU setembre 2018} En una localitat, el 25\,\% dels habitants va periòdicament al dentista, el 10\,\% es fa una analítica i el 8\,\% fa les dues coses." + tasks(1, [
      r"Raona si els successos «anar al dentista» i «fer-se una analítica» són independents.", r"Quin percentatge d'habitants ni es fa una analítica ni va al dentista?", r"Si triem a l'atzar un habitant d'entre els que van al dentista, quina és la probabilitat que es faça una analítica?"]),
     tasks(1, [r"$0{,}25\cdot0{,}1=0{,}025\neq0{,}08$: \rest{no són independents}.", r"$1-(0{,}25+0{,}1-0{,}08)=0{,}73$: \ $\res{73\,\%}$", r"$P(An\cond D)=\frac{0{,}08}{0{,}25}=" + B(ck(F('0.08') / F('0.25'), F('0.32'))) + "$"])),
 (1, r"\pau{La Rioja, EBAU ordinària 2020} En una classe hi ha 24 estudiants: 12 han aprovat anglés, 16 han aprovat matemàtiques i 4 han suspés les dues assignatures." + tasks(1, [
      r"Quina és la probabilitat que un alumne triat a l'atzar haja aprovat matemàtiques i suspés anglés?", r"Quina és la probabilitat que haja aprovat les dues assignatures?", r"Són independents els successos «aprovar matemàtiques» i «aprovar anglés»?"]),
     r"Aproven alguna $24-4=20$; les dues: $12+16-20=8$." + cen(taula(['M', r'\overline{M}'], ['A', r'\overline{A}'], [[8, 8, 16], [4, 4, 8], [12, 12, 24]], str)) +
     tasks(1, [r"$\frac{8}{24}=" + B(ck(F(16 - 8, 24), F(1, 3))) + "$", r"$\frac{8}{24}=" + B(F(8, 24)) + "$", r"$P(M)P(A)=\frac{16}{24}\cdot\frac{12}{24}=\frac13=P(M\cap A)$: \rest{sí que són independents}."])
     + ('' if ck(F(16, 24) * F(12, 24), F(8, 24)) else '')),
 (2, r"\pau{Galícia, ABAU ordinària 2024} S'estima que en una població el 20\,\% pateix obesitat i que l'11\,\% pateix obesitat i és hipertens. A més, el 27,5\,\% dels hipertensos pateix obesitat." + tasks(1, [
      r"Quin percentatge de la població pateix obesitat o és hipertens?", r"Són independents els successos «patir obesitat» i «ser hipertens»?", r"Calcula la probabilitat que un individu que no pateix obesitat siga hipertens."]),
     r"$P(O\cap H)=P(H)\,P(O\cond H)\Rightarrow P(H)=\frac{0{,}11}{0{,}275}=" + N(o24) + "$." +
     tasks(1, [r"$0{,}2+0{,}4-0{,}11=0{,}49$: \ $\res{49\,\%}$" + ('' if ck(F('0.2') + o24 - F('0.11'), F('0.49')) else ''), r"$0{,}2\cdot0{,}4=0{,}08\neq0{,}11$: \rest{no són independents}.",
               r"$P(H\cond\co O)=\frac{0{,}4-0{,}11}{0{,}8}=" + B(ck((o24 - F('0.11')) / F('0.8'), F('0.3625'))) + "$"])),
 (2, r"\pau{Galícia, ABAU setembre 2017} El 60\,\% dels individus d'una població estan vacunats contra una malaltia. Durant una epidèmia, el 20\,\% va contraure la malaltia i el 3\,\% està vacunat i la va contraure." + tasks(1, [
      r"Calcula el percentatge d'individus que han contret la malaltia entre els que no estan vacunats.", r"Calcula el percentatge de vacunats entre els que van contraure la malaltia. Justifica si els successos «estar vacunat» i «contraure la malaltia» són dependents o independents."]),
     tasks(1, [r"$P(M\cond\co V)=\frac{0{,}2-0{,}03}{0{,}4}=" + N(ck(v17, F('0.425'))) + r"$: \ $\res{42{,}5\,\%}$", r"$P(V\cond M)=\frac{0{,}03}{0{,}2}=0{,}15$: \ $\res{15\,\%}$. Com que $P(V\cond M)=0{,}15\neq P(V)=0{,}6$, \rest{són dependents}."])),
 (2, r"\pau{Madrid, PAU ordinària 2025} De tres successos $A$, $B$ i $C$ se sap que $A$ i $C$ són disjunts (incompatibles), $A$ i $B$ són independents, $P(A)=0{,}25$, $P(B)=0{,}2$ i $P(B\cap C)=0{,}05$." + tasks(1, [
      r"Calcula la probabilitat que ocórrega almenys un dels successos $A$ o $B$.", r"Calcula $P(\co B\cup\co C)$.", r"Poden ser independents els successos $A$ i $C$?"]),
     tasks(1, [r"$P(A\cup B)=0{,}25+0{,}2-0{,}25\cdot0{,}2=" + B(ck(F('0.25') + F('0.2') - F('0.05'), F('0.4'))) + "$", r"De Morgan: $1-P(B\cap C)=" + B(F('0.95')) + "$",
               r"Com que $P(B\cap C)>0$, $P(C)>0$; si foren independents, $P(A\cap C)=0{,}25\,P(C)>0$, però és 0 perquè són disjunts: \rest{no poden ser independents}."])),
 (1, r"\pau{País Basc, EAU extraordinària 2022} La Deiene i la Kattalin són jugadores de bàsquet. La Deiene encistella 2 de cada 5 tirs i la Kattalin 3 de cada 7. Si totes dues tiren a cistella una sola vegada, calcula la probabilitat que:" + tasks(2, [
      r"totes dues encistellen;", r"no n'encistelle cap;", r"només encistelle la Deiene;", r"n'encistelle almenys una."]),
     r"Els tirs són independents: multipliquem." + tasks(2, [r"$\frac25\cdot\frac37=" + B(ck(F(2, 5) * F(3, 7), F(6, 35))) + "$", r"$\frac35\cdot\frac47=" + B(ck(F(3, 5) * F(4, 7), F(12, 35))) + "$",
      r"$\frac25\cdot\frac47=" + B(ck(F(2, 5) * F(4, 7), F(8, 35))) + "$", r"$1-\frac{12}{35}=" + B(F(23, 35)) + "$"])),
 (2, r"\pau{Illes Balears, PBAU extraordinària 2023} Tirem dos daus no trucats i considerem els successos $A=$«en el primer dau ha eixit un 1», $B=$«en el segon dau ha eixit un 1» i $C=$«la suma dels dos daus és 3»." + tasks(1, [
      r"Calcula $P(A)$.", r"Calcula $P(A\cup B)$.", r"Són independents els successos $C$ i $A\cup B$?"]),
     tasks(1, [r"$\frac{6}{36}=" + B(F(1, 6)) + "$", r"$\frac{6+6-1}{36}=" + B(ck(pAB13, F(11, 36))) + "$",
               r"$C=\{(1,2),(2,1)\}\subset A\cup B$, així que $P(C\cap(A\cup B))=P(C)=\frac{2}{36}$, però $P(C)\,P(A\cup B)=\frac{2}{36}\cdot\frac{11}{36}\neq\frac{2}{36}$: \rest{no són independents}."])
     + ('' if ck(pI13, pC13) else '')),
 (2, r"Raona si les afirmacions següents són vertaderes o falses:" + tasks(1, [r"Dos successos incompatibles (amb probabilitats no nul·les) són independents.",
      r"Si $A$ i $B$ són independents, aleshores $\co A$ i $\co B$ també ho són.", r"Si $P(A\cond B)=P(A)$, aleshores $P(B\cond A)=P(B)$."]),
     tasks(1, [r"\rest{Falsa}: $P(A\cap B)=0$, però $P(A)P(B)>0$. Si passa un, segur que no passa l'altre: depenen l'un de l'altre.",
               r"\rest{Vertadera}: $P(\co A\cap\co B)=1-P(A\cup B)=1-P(A)-P(B)+P(A)P(B)=(1-P(A))(1-P(B))=P(\co A)P(\co B)$.",
               r"\rest{Vertadera}: $P(A\cond B)=P(A)\iff P(A\cap B)=P(A)P(B)\iff P(B\cond A)=P(B)$."])),
]))

# =====================================================================
# 7. Experiments compostos i extraccions
def urn(cnt, nd, rep):
    """totes les seqüències de colors amb la seua probabilitat"""
    out = {}
    def rec(c, seq, p):
        if len(seq) == nd: out[tuple(seq)] = out.get(tuple(seq), 0) + p; return
        t = sum(c.values())
        for k, v in c.items():
            if v:
                d = dict(c)
                if not rep: d[k] -= 1
                rec(d, seq + [k], p * F(v, t))
    rec(dict(cnt), [], F(1)); return out
def pu(cnt, nd, rep, f): return sum(p for s, p in urn(cnt, nd, rep).items() if f(s))
U53 = {'R': 4, 'B': 6}
w3 = [pu(U53, 3, True, lambda s: s.count('R') == 3), pu(U53, 3, True, lambda s: s.count('R') == 2), pu(U53, 3, False, lambda s: s.count('R') == 3), pu(U53, 3, False, lambda s: s.count('R') == 2)]
ck(w3, [F('0.064'), F('0.288'), F(1, 30), F(3, 10)])
U54 = {'B': 3, 'R': 1, 'N': 4}
a20 = [pu(U54, 2, False, lambda s: s == ('B', 'B')), pu(U54, 2, False, lambda s: 'B' in s), pu(U54, 2, False, lambda s: s[0] == s[1])]
ck([a20[0], a20[1], a20[2], a20[0] / a20[2]], [F(3, 28), F(9, 14), F(9, 28), F(1, 3)])
ck([float(a20[0]), float(a20[1]), float(a20[2])], [0.107, 0.643, 0.321], 1e-3)
U55 = {'B': 15, 'N': 5}
v18 = [F(15, 20), pu(U55, 2, False, lambda s: s == ('B', 'B')), F(4, 19), pu(U55, 2, False, lambda s: s[0] != s[1])]
ck(v18, [F(3, 4), F(21, 38), F(4, 19), F(15, 38)])
U56 = {'D': 4, 'O': 8}
n17 = [pu(U56, 3, False, lambda s: 'D' not in s), pu(U56, 3, False, lambda s: 'D' in s), pu(U56, 3, False, lambda s: s.count('D') == 1)]
ck(n17, [F(14, 55), F(41, 55), F(28, 55)])
U57 = {'B': 2, 'N': 4, 'R': 5}
r2a = pu(U57, 2, False, lambda s: s[0] == 'R'); r2b = pu(U57, 2, False, lambda s: s[0] == s[1]); r2ab = pu(U57, 2, False, lambda s: s == ('R', 'R'))
a17 = [r2ab, 1 - r2b, pu(U57, 2, False, lambda s: s[1] == 'R')]
ck(a17, [F(2, 11), F(38, 55), F(5, 11)]); ck(r2a * r2b != r2ab, True)
U58 = {'V': 3, 'A': 2, 'R': 4}
f1 = pu(U58, 2, False, lambda s: s == ('A', 'A')); f2 = pu(U58, 2, False, lambda s: s == ('V', 'V')); f3 = pu(U58, 2, False, lambda s: s.count('A') == 1)
ck([f1 + f2, f3, f3 / (f1 + f2 + f3)], [F(1, 9), F(7, 18), F(7, 9)])
LR = list(permutations(range(10), 2)); pc_ = F(sum(1 for x, y in LR if y > x), 90)
pac = F(sum(1 for x, y in LR if x == 0 and y > x), 90) / pc_; pbc = F(sum(1 for x, y in LR if x == 5 and y > x), 90) / pc_
ck([pc_, pac, pbc], [F(1, 2), F(1, 5), F(4, 45)])
K40 = {'K': 4, 'X': 36}
k22 = [F(4, 40), pu(K40, 2, False, lambda s: s[1] == 'K'), pu(K40, 2, False, lambda s: 'K' not in s)]
ck(k22, [F(1, 10), F(1, 10), F(21, 26)])
P3 = list(permutations([1, 2, 3])); m17a = F(sum(1 for p in P3 if p[1] % 2 and p[2] % 2), 6)
s1 = {p for p in P3 if p.index(2) < 2}; s2 = {p for p in P3 if p.index(2) in (0, 2)}
ck([m17a, F(len(s1 & s2), 6) == F(len(s1), 6) * F(len(s2), 6)], [F(1, 3), False])
dep = {'Ad': (12, 4), 'Pr': (30, 11), 'Ve': (6, 1)}
tot = sum(a + b for a, b in dep.values()); ang = sum(a for a, b in dep.values())
same3 = sum(F((a + b) * (a + b - 1) * (a + b - 2), tot * (tot - 1) * (tot - 2)) for a, b in dep.values())
ck([F(ang, tot), F(dep['Ve'][0], ang), F(12, tot) == F(16, tot) * F(ang, tot)], [F('0.75'), F('0.125'), True]); ck(float(same3), 0.27, 5e-3)
S.append(("Experiments compostos. Extraccions amb i sense reemplaçament", [
 (1, r"Una urna conté 4 boles roges i 6 de blaves. Traiem tres boles. Calcula la probabilitat que les tres siguen roges i la probabilitat que n'hi haja exactament dues de roges:" + tasks(2, [r"amb reemplaçament;", r"sense reemplaçament."])
     + recorda(r"en un diagrama d'arbre, multipliquem les probabilitats al llarg de cada camí i sumem els camins que formen el succés. Sense reemplaçament, la composició de l'urna canvia en cada extracció."),
     tasks(1, [r"$0{,}4^3=" + B(w3[0]) + r"$; \ dues roges: $RRB$, $RBR$, $BRR$: $3\cdot0{,}4^2\cdot0{,}6=" + B(w3[1]) + "$",
               r"$\frac4{10}\cdot\frac39\cdot\frac28=" + B(w3[2]) + r"$; \ dues roges: $3\cdot\frac{4\cdot3\cdot6}{10\cdot9\cdot8}=" + B(w3[3]) + "$"])),
 (1, r"\pau{Aragó, EvAU extraordinària 2020} En una bossa tenim 8 boles: 3 blanques, 1 roja i 4 negres. Traiem dues boles sense reemplaçament. Calcula:" + tasks(1, [
      r"La probabilitat que les dues siguen blanques.", r"La probabilitat que almenys una siga blanca.", r"La probabilitat que les dues siguen del mateix color.", r"La probabilitat que siguen blanques, si se sap que les dues són del mateix color."]),
     tasks(2, [r"$\frac38\cdot\frac27=" + B(a20[0]) + "$", r"$1-\frac58\cdot\frac47=" + B(a20[1]) + "$", r"$\frac38\cdot\frac27+\frac48\cdot\frac37=" + B(a20[2]) + "$ (dues roges és impossible)",
               r"$\frac{6/56}{18/56}=" + B(a20[0] / a20[2]) + "$"])),
 (1, r"\pau{País Basc, EAU juny 2018} En una urna hi ha 15 boles blanques i 5 de negres. Calcula:" + tasks(1, [
      r"Si traiem una bola a l'atzar, la probabilitat que siga blanca.", r"Si en traiem dues a l'atzar, la probabilitat que totes dues siguen blanques.", r"Si traiem una bola i després una altra, i la primera és negra, la probabilitat que la segona també siga negra.",
      r"Si traiem una bola i després una altra, la probabilitat que siguen de color diferent."]),
     tasks(2, [r"$\frac{15}{20}=" + B(v18[0]) + "$", r"$\frac{15}{20}\cdot\frac{14}{19}=" + B(v18[1]) + "$", r"$\frac{4}{19}\approx" + dec(v18[2]) + r"$ \ ($\res{" + Q(v18[2]) + "}$)",
               r"$\frac{15}{20}\cdot\frac{5}{19}+\frac{5}{20}\cdot\frac{15}{19}=" + B(v18[3]) + "$"])),
 (1, r"\pau{Navarra, EvAU setembre 2017} Una caixa conté dotze bolígrafs, quatre dels quals són defectuosos. Se'n trauen tres de manera successiva i sense tornar-los a la caixa." + tasks(1, [
      r"Calcula la probabilitat que cap dels tres bolígrafs tinga defectes.", r"Calcula la probabilitat que almenys un dels tres siga defectuós.", r"Calcula la probabilitat que només un siga defectuós."]),
     tasks(1, [r"$\frac{8}{12}\cdot\frac{7}{11}\cdot\frac{6}{10}=" + B(n17[0]) + "$", r"$1-\frac{14}{55}=" + B(n17[1]) + "$", r"$3\cdot\frac{4}{12}\cdot\frac{8}{11}\cdot\frac{7}{10}=" + B(n17[2]) + "$ (el defectuós pot eixir en 1r, 2n o 3r lloc)"])),
 (2, r"\pau{Aragó, EvAU juny 2017} En una urna hi ha 2 boles blanques, 4 de negres i 5 de roges. Se'n trauen dues, una darrere l'altra, sense reemplaçament. Calcula:" + tasks(1, [
      r"La probabilitat que les dues siguen roges.", r"La probabilitat que siguen de color diferent.", r"La probabilitat que la segona bola siga roja.",
      r"Si $A$ és el succés «la primera bola és roja» i $B$ el succés «les dues boles són del mateix color», són independents $A$ i $B$?"]),
     tasks(2, [r"$\frac5{11}\cdot\frac4{10}=" + B(a17[0]) + "$", r"$1-\frac{2\cdot1+4\cdot3+5\cdot4}{110}=" + B(a17[1]) + "$",
               r"$\frac{2}{11}\cdot\frac{5}{10}+\frac{4}{11}\cdot\frac{5}{10}+\frac{5}{11}\cdot\frac{4}{10}=" + B(a17[2]) + "$",
               r"$P(A\cap B)=\frac{2}{11}$ i $P(A)P(B)=\frac{5}{11}\cdot\frac{17}{55}=\frac{17}{121}\neq\frac{22}{121}$: \rest{no}"])),
 (2, r"\pau{Andalusia, PEvAU extraordinària 2023} Una caixa conté 3 fitxes verdes, 2 de blaves i 4 de roges. Un joc consisteix a fer dues extraccions sense reemplaçament: qui trau dues fitxes blaves guanya el primer premi; qui en trau dues de verdes, el segon premi; i qui trau una blava i una d'un altre color, el tercer premi." + tasks(1, [
      r"Calcula la probabilitat que un jugador aconseguisca el primer o el segon premi.", r"Calcula la probabilitat que un jugador guanye el tercer premi.", r"Sabent que un jugador ha obtingut premi, quina és la probabilitat que haja guanyat el tercer?"]),
     tasks(1, [r"$\frac29\cdot\frac18+\frac39\cdot\frac28=\frac{2+6}{72}=" + B(f1 + f2) + "$", r"$\frac29\cdot\frac78+\frac79\cdot\frac28=\frac{28}{72}=" + B(f3) + "$",
               r"$\frac{7/18}{1/9+7/18}=" + B(f3 / (f1 + f2 + f3)) + "$"])),
 (2, r"\pau{La Rioja, EBAU ordinària 2023} Un bombo de loteria té deu boles numerades del 0 al 9. Fem dues extraccions consecutives sense reemplaçar la primera bola. Considerem els successos $A=$«la primera bola és 0», $B=$«la primera bola és 5» i $C=$«la segona bola és més gran que la primera». Calcula $P(A)$, $P(B)$, $P(C)$, $P(A\cond C)$ i $P(B\cond C)$.",
     r"$P(A)=P(B)=" + B(F(1, 10)) + r"$. Hi ha $10\cdot9=90$ parelles i, per simetria, en la meitat la segona és més gran: $P(C)=\frac{45}{90}=" + B(pc_) + r"$." +
     r"\par $P(A\cond C)=\frac{P(A\cap C)}{P(C)}=\frac{9/90}{1/2}=" + B(pac) + r"$ \ (si la primera és 0, la segona sempre és més gran); \ $P(B\cond C)=\frac{4/90}{1/2}=" + B(pbc) + "$."),
 (2, r"\pau{País Basc, EAU extraordinària 2022} Es van a sortejar 4 viatges a Nova York entre 40 persones amb una baralla de 40 cartes: es reparteix una carta a cada persona i les que reben un rei guanyen un viatge." + tasks(1, [
      r"Calcula la probabilitat que guanye un viatge la primera persona que rep la carta.", r"Calcula la probabilitat que guanye un viatge la segona persona que rep la carta.", r"Calcula la probabilitat que cap de les dues primeres persones guanye un viatge."]),
     tasks(1, [r"$\frac{4}{40}=" + B(k22[0]) + "$", r"$\frac{4}{40}\cdot\frac{3}{39}+\frac{36}{40}\cdot\frac{4}{39}=" + B(k22[1]) + "$ (com la primera: l'ordre no afavoreix ningú)", r"$\frac{36}{40}\cdot\frac{35}{39}=" + B(k22[2]) + "$"])),
 (2, r"\pau{Múrcia, EBAU juny 2017} Una urna conté tres boles numerades de l'1 al 3. Se'n trauen successivament les tres boles." + tasks(1, [
      r"Calcula la probabilitat que les dues últimes boles extretes siguen senars.", r"Determina si són independents els successos $S_1=$«ix el nombre parell abans que algun dels senars» i $S_2=$«els dos nombres senars ixen consecutivament»."]),
     r"Hi ha $3!=6$ ordres equiprobables." + tasks(1, [r"Les dues últimes són senars si el 2 ix el primer: $\frac26=" + B(m17a) + "$",
      r"$S_1$: el 2 no és l'últim, $P(S_1)=\frac46$; $S_2$: el 2 és el primer o l'últim, $P(S_2)=\frac46$; $S_1\cap S_2$: el 2 és el primer, $\frac26$. Com que $\frac46\cdot\frac46=\frac49\neq\frac13$, \rest{són dependents}."])),
 (2, r"\pau{Aragó, EvAU setembre 2019} Una empresa té 64 treballadors repartits en tres departaments. S'ha estudiat si saben anglés o no:" + cen(taula([r'\text{Sap anglés}', r'\text{No en sap}'], [r'\text{Admin.}', r'\text{Producció}', r'\text{Vendes}'], [[12, 30, 6, 48], [4, 11, 1, 16], [16, 41, 7, 64]], str)) + tasks(1, [
      r"Triem a l'atzar un treballador. Quina és la probabilitat que sàpia anglés?", r"Triem a l'atzar un treballador d'entre els que saben anglés. Quina és la probabilitat que siga del departament de Vendes?",
      r"Siguen $A=$«el treballador és d'Administració» i $B=$«el treballador sap anglés». Són independents?", r"Triem a l'atzar tres treballadors (sense reemplaçament). Quina és la probabilitat que siguen del mateix departament?"]),
     tasks(1, [r"$\frac{48}{64}=" + B(F(48, 64)) + "$", r"$\frac{6}{48}=" + B(F(6, 48)) + "$", r"$P(A\cap B)=\frac{12}{64}=\frac{3}{16}$ i $P(A)P(B)=\frac{16}{64}\cdot\frac{48}{64}=\frac{3}{16}$: \rest{sí que són independents}.",
               r"$\frac{16\cdot15\cdot14+41\cdot40\cdot39+7\cdot6\cdot5}{64\cdot63\cdot62}=" + B(same3) + "$"])),
]))

# =====================================================================
# 8. Probabilitat total i Bayes
def tot(pr, cd): return sum(F(p) * F(c) for p, c in zip(pr, cd))
ag = [F('0.4'), F('0.35'), F('0.25')]; ap = [F('0.8'), F('0.6'), F('0.92')]
agT = tot(ag, ap); ck([ag[2] * ap[2], 1 - agT, agT, ag[1] * (1 - ap[1]) + ag[2] * (1 - ap[2]), ag[2] * ap[2] / agT], [F('0.23'), F('0.24'), F('0.76'), F('0.16'), F(23, 76)])
lv = [F('0.5'), F('0.3'), F('0.2')]; ld = [F('0.05'), F('0.15'), F('0.2')]; lvT = tot(lv, ld); ck([1 - lvT, lv[0] * ld[0] / lvT], [F('0.89'), F(5, 22)])
dn = tot([F('0.3'), F('0.7')], [F('0.8'), F('0.7')]); ck([dn, F('0.24') / dn], [F('0.73'), F(24, 73)])
bt = tot([F('0.3'), F('0.7')], [F('0.4'), F('0.25')]); ck([F('0.3') * F('0.4'), bt], [F('0.12'), F('0.295')])
bo = tot([F(40, 50), F(10, 50)], [F('0.05'), F('0.02')]); ck([1 - bo, F(40, 50) * F('0.05') / bo], [F('0.956'), F(10, 11)])
sp = tot([F('0.2'), F('0.8')], [F('0.4'), F('0.006')]); ck([F('0.08') / sp, F('0.8') * F('0.994') / (1 - sp), F('0.2') * F('0.6') + F('0.8') * F('0.006')], [F(50, 53), F(497, 572), F(78, 625)])
dp = tot([F('0.04'), F('0.96')], [F('0.92'), F('0.1')]); ck([dp, F('0.04') * F('0.08'), F('0.96') * F('0.9') / (1 - dp)], [F('0.1328'), F('0.0032'), F(270, 271)])
gu = tot([F(1, 3), F(2, 3)], [F(6, 14), F(5, 9)]); ck([gu, F(1, 3) * F(8, 14) / (1 - gu)], [F(97, 189), F(9, 23)])
cn = tot([F(1, 3)] * 3, [F(4, 10), F(2, 7), F(7, 11)]); ck([cn, F(1, 3) * F(6, 10) / (1 - cn)], [F(509, 1155), F(231, 646)])
mc = tot([F(1, 3)] * 3, [F(4, 10), F(1, 6), F(3, 8)]); ck([mc, F(1, 3) * F(6, 10) / (1 - mc)], [F(113, 360), F(72, 247)])
nv = tot([F(5, 6), F(1, 6)], [F(7, 10), F(2, 8)]); ck([nv, F(1, 6) * F(6, 8) / (1 - nv)], [F('0.625'), F(1, 3)])
mb = tot([F('0.3'), F('0.5'), F('0.2')], [F('0.7'), F('0.95'), F('0.5')]); ck([F('0.2') * F('0.5'), mb, F('0.1') / mb, F('0.7') * F('0.95') * F('0.5')], [F('0.1'), F('0.785'), F(20, 157), F('0.3325')])
iso = tot([F(60, 200), F(50, 200), F(90, 200)], [F('0.3'), F('0.2'), F('0.4')]); ck([iso, F(50, 200) * F('0.2') / iso, F(60, 200) * F('0.3') == F(60, 200) * iso], [F('0.32'), F(5, 32), False])
un_c = (F('0.395') - F('0.6') * F('0.4') - F('0.3') * F('0.5')) / F('0.1'); ck([1 - un_c, (F('0.6') * F('0.4') + F('0.3') * F('0.5')) / F('0.395')], [F('0.95'), F(78, 79)])
ck(float(F(78, 79)), 0.987, 1e-3)
rz = tot([F(6, 10), F(4, 10)], [F(5, 15), F(12, 15)]); ck([rz, F(4, 10) * F(3, 15) / (1 - rz)], [F('0.52'), F(1, 6)])
U79 = {'V': 4, 'R': 2}
as1 = F(1, 2) * pu(U79, 2, False, lambda s: s == ('R', 'R'))
as2 = F(1, 2) * F(4, 6) + F(1, 2) * pu(U79, 2, False, lambda s: 'R' not in s)
as3 = F(1, 2) * F(4, 6) + F(1, 2) * pu(U79, 2, False, lambda s: 'V' in s)
ck([as1, as2, as3, F(1, 2) * F(4, 6) / as3], [F(1, 30), F(8, 15), F('0.8'), F(5, 12)])
bx = [F(1, 4), F(1, 2) * F(1, 4) + F(1, 2) * F(3, 4)]; ck([bx[0], bx[1], F(1, 2) * F(1, 4) / bx[1]], [F(1, 4), F(1, 2), F(1, 4)])
pk2 = F(13, 52) * F(12, 51) + F(39, 52) * F(13, 51); pk3 = F(39, 52) * F(38, 51) / (1 - pk2); ck([pk2, pk3], [F(1, 4), F(38, 51)])
S.append(("Probabilitat total i teorema de Bayes", [
 (1, r"\pau{Aragó, EvAU ordinària 2023} En una facultat d'Economia s'ofereix una assignatura en tres grups, G1, G2 i G3, que representen el 40\,\%, el 35\,\% i el 25\,\% dels estudiants, respectivament. Supera l'assignatura el 80\,\% del grup G1, el 60\,\% del G2 i el 92\,\% del G3. Calcula la probabilitat que, en triar un estudiant a l'atzar:" + tasks(1, [
      r"haja superat l'assignatura i siga del grup G3;", r"no haja superat l'assignatura;", r"haja superat l'assignatura;", r"ni haja superat l'assignatura ni siga del grup G1;", r"siga del grup G3, si ha superat l'assignatura."])
     + recorda(r"probabilitat total: $P(S)=P(G_1)P(S\cond G_1)+P(G_2)P(S\cond G_2)+P(G_3)P(S\cond G_3)$. Bayes: $P(G_i\cond S)=\dfrac{P(G_i)P(S\cond G_i)}{P(S)}$."),
     cen(arbre([('G_1', ag[0], [('S', ap[0], Q(ag[0] * ap[0])), (r'\overline{S}', 1 - ap[0], Q(ag[0] * (1 - ap[0])))]), ('G_2', ag[1], [('S', ap[1], Q(ag[1] * ap[1])), (r'\overline{S}', 1 - ap[1], Q(ag[1] * (1 - ap[1])))]),
                ('G_3', ag[2], [('S', ap[2], Q(ag[2] * ap[2])), (r'\overline{S}', 1 - ap[2], Q(ag[2] * (1 - ap[2])))])])) +
     tasks(2, [r"$0{,}25\cdot0{,}92=" + B(ag[2] * ap[2]) + "$", r"$1-0{,}76=" + B(1 - agT) + "$", r"$0{,}32+0{,}21+0{,}23=" + B(agT) + "$", r"$0{,}35\cdot0{,}4+0{,}25\cdot0{,}08=" + B(ag[1] * (1 - ap[1]) + ag[2] * (1 - ap[2])) + "$",
               r"$P(G_3\cond S)=\frac{0{,}23}{0{,}76}=" + B(ag[2] * ap[2] / agT) + "$"])),
 (1, r"\pau{Andalusia, PEvAU setembre 2018} Un hotel té tres rentadores industrials, $L_1$, $L_2$ i $L_3$. $L_1$ fa el 50\,\% de les rentades, $L_2$ el 30\,\% i $L_3$ la resta. $L_1$ produeix un 5\,\% de rentades defectuoses, $L_2$ un 15\,\% i $L_3$ un 20\,\%. Es tria a l'atzar una rentada." + tasks(1, [
      r"Calcula la probabilitat que no siga defectuosa.", r"Calcula la probabilitat que l'haja feta $L_1$, sabent que ha sigut defectuosa."]),
     tasks(1, [r"$P(D)=0{,}5\cdot0{,}05+0{,}3\cdot0{,}15+0{,}2\cdot0{,}2=0{,}11\Rightarrow P(\co D)=" + B(1 - lvT) + "$", r"$P(L_1\cond D)=\frac{0{,}025}{0{,}11}=" + B(lv[0] * ld[0] / lvT) + "$"])),
 (1, r"\pau{Galícia, ABAU setembre 2018} En una empresa, el 30\,\% dels empleats són dones i el 70\,\% restant, homes. De les dones, el 80\,\% té contracte indefinit, mentre que dels homes només el 70\,\% en té." + tasks(1, [
      r"Calcula el percentatge de persones de l'empresa que tenen contracte indefinit.", r"Si un empleat té contracte indefinit, quina és la probabilitat que siga dona?", r"Són independents els successos «ser home» i «tenir contracte indefinit»?"]),
     cen(arbre([('D', F('0.3'), [('I', F('0.8'), '0{,}24'), (r'\overline{I}', F('0.2'), '0{,}06')]), ('H', F('0.7'), [('I', F('0.7'), '0{,}49'), (r'\overline{I}', F('0.3'), '0{,}21')])], s=(2.4, 1.3))) +
     tasks(1, [r"$0{,}24+0{,}49=0{,}73$: \ $\res{73\,\%}$", r"$P(D\cond I)=\frac{0{,}24}{0{,}73}=" + B(F('0.24') / dn) + "$", r"$P(I\cond H)=0{,}7\neq P(I)=0{,}73$: \rest{no són independents}."])),
 (1, r"\pau{Galícia, ABAU juny 2018} El 30\,\% dels estudiants de secundària d'un institut juga a bàsquet. Entre els que juguen a bàsquet, el 40\,\% juga també a tenis; entre els que no juguen a bàsquet, una quarta part juga a tenis. Triem un estudiant a l'atzar." + tasks(1, [
      r"Quina és la probabilitat que practique tots dos esports?", r"Quina és la probabilitat que jugue a tenis?", r"Són independents els successos «jugar a tenis» i «jugar a bàsquet»?"]),
     tasks(1, [r"$0{,}3\cdot0{,}4=" + B(F('0.12')) + "$", r"$0{,}12+0{,}7\cdot0{,}25=" + B(bt) + "$", r"$P(T\cond B)=0{,}4\neq P(T)=0{,}295$: \rest{no són independents}."])),
 (1, r"\pau{Andalusia, PEvAU extraordinària 2020} Una empresa fabrica bombetes LED i halògenes. El 5\,\% de les LED i el 2\,\% de les halògenes ixen defectuoses. Es tria a l'atzar una bombeta d'una caixa que conté 40 bombetes LED i 10 d'halògenes." + tasks(1, [
      r"Calcula la probabilitat que la bombeta triada no siga defectuosa.", r"Calcula la probabilitat que la bombeta siga LED, sabent que és defectuosa."]),
     tasks(1, [r"$P(D)=\frac{40}{50}\cdot0{,}05+\frac{10}{50}\cdot0{,}02=0{,}044\Rightarrow P(\co D)=" + B(1 - bo) + "$", r"$P(LED\cond D)=\frac{0{,}04}{0{,}044}=" + B(F(40, 50) * F('0.05') / bo) + "$"])),
 (2, r"\pau{Andalusia, PEvAU ordinària 2023} En una base de dades de correus electrònics s'ha observat que el 20\,\% dels correus rebuts són brossa (\emph{spam}). A més, la paraula «lottery» apareix en el 40\,\% dels correus brossa i en el 0,6\,\% dels que no ho són." + tasks(1, [
      r"Calcula la probabilitat que un correu triat a l'atzar en què apareix la paraula «lottery» siga brossa.", r"Calcula la probabilitat que un correu triat a l'atzar en què no apareix la paraula «lottery» no siga brossa.",
      r"Si un correu s'etiqueta com a brossa quan apareix la paraula «lottery» i com a no brossa quan no apareix, calcula la probabilitat que un correu s'etiquete incorrectament."]),
     cen(arbre([('S', F('0.2'), [('L', F('0.4'), '0{,}08'), (r'\overline{L}', F('0.6'), '0{,}12')]), (r'\overline{S}', F('0.8'), [('L', F('0.006'), '0{,}0048'), (r'\overline{L}', F('0.994'), '0{,}7952')])], s=(2.4, 1.3))) +
     r"$P(L)=0{,}08+0{,}0048=0{,}0848$." + tasks(1, [r"$P(S\cond L)=\frac{0{,}08}{0{,}0848}=" + B(F('0.08') / sp) + "$", r"$P(\co S\cond\co L)=\frac{0{,}7952}{0{,}9152}=" + B(F('0.8') * F('0.994') / (1 - sp)) + "$",
      r"$P(S\cap\co L)+P(\co S\cap L)=0{,}12+0{,}0048=" + B(F('0.1248')) + "$"])),
 (2, r"\pau{Navarra, EvAU extraordinària 2022} Es considera que el 4\,\% dels esportistes federats consumeix alguna substància no permesa. Una nova prova de detecció identifica correctament el consum en el 92\,\% dels casos, però si un esportista no en consumeix, la prova dona positiu en el 10\,\% dels casos. Es tria un esportista a l'atzar. Calcula (amb 4 decimals):" + tasks(1, [
      r"La probabilitat que obtinga un resultat positiu.", r"La probabilitat que siga consumidor i la prova done negatiu.", r"La probabilitat que no siga consumidor, sabent que la prova ha donat negatiu."]),
     tasks(1, [r"$0{,}04\cdot0{,}92+0{,}96\cdot0{,}1=" + B(dp) + "$", r"$0{,}04\cdot0{,}08=" + B(F('0.0032')) + "$", r"$\frac{0{,}96\cdot0{,}9}{1-0{,}1328}=\frac{0{,}864}{0{,}8672}=" + B(F('0.864') / (1 - dp)) + "$"])),
 (2, r"\pau{Galícia, ABAU extraordinària 2023} En una urna A hi ha 8 boles verdes i 6 de roges, i en una urna B, 4 de verdes i 5 de roges. Es llança un dau: si ix un nombre menor que 3 es trau una bola de l'urna A, i si no, de l'urna B." + tasks(1, [
      r"Calcula la probabilitat que la bola extreta siga roja.", r"Sabent que s'ha extret una bola verda, quina és la probabilitat que siga de l'urna A?", r"Són independents els successos «traure bola roja» i «la bola és de l'urna A»?"]),
     cen(arbre([('A', F(1, 3), [('V', F(8, 14), Q(F(1, 3) * F(8, 14))), ('R', F(6, 14), Q(F(1, 3) * F(6, 14)))]), ('B', F(2, 3), [('V', F(4, 9), Q(F(2, 3) * F(4, 9))), ('R', F(5, 9), Q(F(2, 3) * F(5, 9)))])], s=(2.4, 1.3))) +
     tasks(1, [r"$\frac13\cdot\frac{6}{14}+\frac23\cdot\frac59=\frac17+\frac{10}{27}=" + B(gu) + "$", r"$P(A\cond V)=\frac{4/21}{92/189}=" + B(F(1, 3) * F(8, 14) / (1 - gu)) + "$",
               r"$P(R\cond A)=\frac{6}{14}=\frac37\approx0{,}4286\neq P(R)\approx" + dec(gu) + r"$: \rest{no són independents}."])),
 (2, r"\pau{Canàries, EBAU extraordinària 2022} Tenim tres urnes iguals: la primera té 6 boles blanques i 4 de negres, la segona 5 de blanques i 2 de negres, i la tercera 4 de blanques i 7 de negres." + tasks(1, [
      r"Es trau una bola d'una urna triada a l'atzar. Fes un diagrama amb les probabilitats dels resultats possibles.", r"Calcula la probabilitat de traure una bola negra.", r"S'ha extret una bola i és blanca. Calcula la probabilitat que siga de la primera urna."]),
     cen(arbre([('U_1', F(1, 3), [('B', F(6, 10), ''), ('N', F(4, 10), '')]), ('U_2', F(1, 3), [('B', F(5, 7), ''), ('N', F(2, 7), '')]), ('U_3', F(1, 3), [('B', F(4, 11), ''), ('N', F(7, 11), '')])])) +
     tasks(1, [r"Vegeu l'arbre.", r"$\frac13\left(\frac4{10}+\frac27+\frac7{11}\right)=" + B(cn) + "$", r"$P(U_1\cond B)=\frac{\frac13\cdot\frac{6}{10}}{1-\frac{509}{1155}}=\frac{1/5}{646/1155}=" + B(F(1, 3) * F(6, 10) / (1 - cn)) + "$"])),
 (2, r"\pau{Múrcia, EBAU extraordinària 2021} Hi ha tres caixes: la primera conté 4 boles blaves i 6 de blanques; la segona, una bola blava i 5 de blanques; la tercera, 3 de blaves i 5 de blanques. Agafem una bola a l'atzar d'una de les caixes, també triada a l'atzar." + tasks(1, [
      r"Calcula la probabilitat que la bola siga blava.", r"Si la bola és blanca, calcula la probabilitat que siga de la primera caixa."]),
     tasks(1, [r"$\frac13\left(\frac4{10}+\frac16+\frac38\right)=" + B(mc) + "$", r"$\frac{\frac13\cdot\frac{6}{10}}{1-\frac{113}{360}}=\frac{72/360}{247/360}=" + B(F(1, 3) * F(6, 10) / (1 - mc)) + "$"])),
 (1, r"\pau{Navarra, EvAU setembre 2018} Dos estudiants construeixen un dau amb 5 cares roges i una de blava, posen 7 boles verdes i 3 de negres en una caixa A, i 6 de negres i 2 de verdes en una caixa B. Llancen el dau: si ix roig, traguen una bola de la caixa A, i si ix blau, de la B." + tasks(1, [
      r"Calcula la probabilitat que la bola siga verda.", r"Calcula la probabilitat que la cara del dau siga blava, sabent que la bola no és verda."]),
     tasks(1, [r"$\frac56\cdot\frac7{10}+\frac16\cdot\frac28=" + B(nv) + "$", r"$\frac{\frac16\cdot\frac68}{1-0{,}625}=\frac{0{,}125}{0{,}375}=" + B(F(1, 6) * F(6, 8) / (1 - nv)) + "$"])),
 (1, r"\pau{Aragó, EvAU extraordinària 2024} A Espanya, el 30\,\% de la població té menys de 30 anys, el 50\,\% entre 30 i 65 anys, i el 20\,\% més de 65. Un estudi afirma que té telèfon mòbil el 70\,\% dels menors de 30 anys, el 95\,\% dels que tenen entre 30 i 65, i el 50\,\% dels majors de 65." + tasks(1, [
      r"Es tria una persona a l'atzar. Calcula la probabilitat que tinga més de 65 anys i tinga mòbil.", r"Quina és la probabilitat que una persona triada a l'atzar tinga mòbil?", r"Triem una persona a l'atzar i té mòbil. Quina és la probabilitat que tinga més de 65 anys?",
      r"Triem una persona de cada grup d'edat. Quina és la probabilitat que totes tres tinguen mòbil? (Es pot suposar independència.)"]),
     tasks(2, [r"$0{,}2\cdot0{,}5=" + B(F('0.1')) + "$", r"$0{,}21+0{,}475+0{,}1=" + B(mb) + "$", r"$\frac{0{,}1}{0{,}785}=" + B(F('0.1') / mb) + "$", r"$0{,}7\cdot0{,}95\cdot0{,}5=" + B(F('0.3325')) + "$"])),
 (1, r"\pau{Galícia, ABAU setembre 2018} En una població, de cada 200 consumidors d'una beguda isotònica, 60 consumeixen la marca A, 50 la marca B i la resta, la C. A més, són joves el 30\,\% dels consumidors d'A, el 20\,\% dels de B i el 40\,\% dels de C." + tasks(1, [
      r"Si se selecciona a l'atzar un consumidor, quina és la probabilitat que siga jove?", r"Si s'ha seleccionat un jove, troba la probabilitat que consumisca la marca B.", r"Són independents els successos «ser jove» i «consumir la marca A»?"]),
     tasks(1, [r"$0{,}3\cdot0{,}3+0{,}25\cdot0{,}2+0{,}45\cdot0{,}4=" + B(iso) + "$", r"$\frac{0{,}05}{0{,}32}=" + B(F(50, 200) * F('0.2') / iso) + "$", r"$P(J\cond A)=0{,}3\neq P(J)=0{,}32$: \rest{no són independents}."])),
 (2, r"\pau{Andalusia, PEvAU extraordinària 2022} En una regió hi ha tres universitats, A, B i C. Dels estudiants que van acabar l'any passat, el 60\,\% procedien de la A, el 30\,\% de la B i la resta de la C. La probabilitat que un estudiant de la A no trobe treball a la regió és 0,4, i per a un de la B, 0,5." + tasks(1, [
      r"Si la probabilitat que un estudiant no trobe treball a la regió és 0,395, determina la probabilitat que un estudiant de la universitat C sí que en trobe.", r"Calcula la probabilitat que un estudiant que no ha trobat treball a la regió procedisca de la universitat A o de la B."]),
     tasks(1, [r"$0{,}395=0{,}6\cdot0{,}4+0{,}3\cdot0{,}5+0{,}1\cdot x\Rightarrow x=P(\co T\cond C)=0{,}05\Rightarrow P(T\cond C)=" + B(1 - un_c) + "$",
               r"$\frac{0{,}24+0{,}15}{0{,}395}=" + B(F('0.39') / F('0.395')) + r"$ (o bé $1-\frac{0{,}005}{0{,}395}$)"])),
 (2, r"\pau{Andalusia, PEvAU extraordinària 2020} Una urna conté 6 boles roges i 4 de blaves. Es trau una bola a l'atzar i es reemplaça per sis boles de l'altre color. A continuació, es trau una segona bola." + tasks(1, [
      r"Calcula la probabilitat que la segona bola siga roja.", r"Si sabem que la segona bola és blava, quina és la probabilitat que la primera també ho haja sigut?"]),
     r"Si la primera és roja, queden 5 roges i 10 blaves; si és blava, 12 roges i 3 blaves." + cen(arbre([('R_1', F(6, 10), [('R_2', F(5, 15), Q(F(6, 10) * F(5, 15))), ('B_2', F(10, 15), Q(F(6, 10) * F(10, 15)))]), ('B_1', F(4, 10), [('R_2', F(12, 15), Q(F(4, 10) * F(12, 15))), ('B_2', F(3, 15), Q(F(4, 10) * F(3, 15)))])], s=(2.4, 1.3))) +
     tasks(1, [r"$\frac{6}{10}\cdot\frac{5}{15}+\frac{4}{10}\cdot\frac{12}{15}=" + B(rz) + "$", r"$P(B_1\cond B_2)=\frac{\frac{4}{10}\cdot\frac{3}{15}}{1-0{,}52}=\frac{0{,}08}{0{,}48}=" + B(F(4, 10) * F(3, 15) / (1 - rz)) + "$"])),
 (2, r"\pau{País Basc, EAU ordinària 2024} L'Asier té una urna amb 4 boles verdes i 2 de roges. Llança una moneda: si ix cara, trau una bola de l'urna, i si ix creu, en trau dues sense reemplaçament." + tasks(1, [
      r"Quina és la probabilitat que l'Asier haja tret dues boles roges?", r"Calcula la probabilitat que no haja tret cap bola roja.", r"Calcula la probabilitat que haja tret almenys una bola verda.", r"Calcula la probabilitat que haja eixit cara, sabent que almenys una bola és verda."]),
     tasks(2, [r"$\frac12\cdot\frac26\cdot\frac15=" + B(as1) + "$", r"$\frac12\cdot\frac46+\frac12\cdot\frac46\cdot\frac35=" + B(as2) + "$", r"$\frac12\cdot\frac46+\frac12\left(1-\frac1{15}\right)=" + B(as3) + "$",
               r"$\frac{1/3}{4/5}=" + B(F(1, 3) / as3) + "$"])),
 (2, r"\pau{País Basc, EAU extraordinària 2024} En una caixa hi ha una bola roja i una de blava. Es trau una bola i, abans de traure'n una segona, es torna a la caixa la primera bola extreta i se n'afigen dues més del mateix color. A continuació es trau una segona bola." + tasks(1, [
      r"Calcula la probabilitat que la segona bola siga roja si la primera ha sigut blava.", r"Calcula la probabilitat que la segona bola siga blava.", r"Si la segona bola ha sigut blava, quina és la probabilitat que la primera haja sigut roja?"]),
     r"Després de la primera extracció hi ha 4 boles: 3 del color de la primera i 1 de l'altre." + tasks(1, [r"$" + B(bx[0]) + "$ (queden 1 roja i 3 blaves)", r"$\frac12\cdot\frac14+\frac12\cdot\frac34=" + B(bx[1]) + "$",
      r"$\frac{\frac12\cdot\frac14}{\frac12}=" + B(F(1, 2) * F(1, 4) / bx[1]) + "$"])),
 (2, r"\pau{Madrid, EvAU ordinària 2022} D'una baralla de pòquer de 52 cartes (13 de cada pal: diamants, cors, piques i trèvols) s'elimina una carta a l'atzar, sense mirar-la. Després es tria a l'atzar una carta de les que queden i s'observa." + tasks(1, [
      r"Calcula la probabilitat que la carta observada siga de diamants.", r"Si la carta observada no és de diamants, calcula la probabilitat que la carta eliminada tampoc no ho fóra."]),
     tasks(1, [r"$\frac{13}{52}\cdot\frac{12}{51}+\frac{39}{52}\cdot\frac{13}{51}=" + B(pk2) + "$", r"$\frac{\frac{39}{52}\cdot\frac{38}{51}}{3/4}=" + B(pk3) + "$"])),
]))

# ---------- comprovacions ----------
for l, r, tol in CHK:
    if tol is None: assert l == r, (l, r)
    else:
        for x, y in (zip(l, r) if isinstance(l, list) else [(l, r)]): assert abs(x - y) < tol, (x, y)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={probabilitat, espai mostral, successos, regla de Laplace, probabilitat condicionada, independència, taules de contingència, diagrames d'arbre, extraccions, probabilitat total, teorema de Bayes, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les Ciències Socials II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
# a Batxillerat no posem estrelles de dificultat
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
# el primer exercici de cada secció no fa salt de pàgina: així no queda separat del títol
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
assert 'refstepcounter{exer}' in pre
# que el títol d'una secció no quede sol al final del full
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
assert '16\\baselineskip' in pre
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
% successos contraris i probabilitat condicionada
\newcommand{\co}[1]{\overline{#1}}
\newcommand{\cond}{\,|\,}
'''

TIT = "Probabilitat"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 9: %s. 2n de Batxillerat CCSS}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 9: %s · 2n Batxillerat CCSS" % (t, TIT))
    assert 'Unitat 9' in p and 'unitat 9' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 9' if sol else "Fitxa d'exercicis · Unitat 9") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    npau = sum(1 for _, exs in S for _, q, _ in exs if '\\pau{' in q)
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Les probabilitats s'han calculat de manera exacta; quan el resultat no és un decimal exacte, es dona la fracció i el valor aproximat amb quatre decimals. Pots comprovar els exercicis de dos successos amb la calculadora dels apunts interactius de la unitat, i els d'arbres amb els ginys d'extraccions i de Bayes."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos. Defineix sempre els successos amb lletres i escriu les dades amb la notació de probabilitats ($P(A)$, $P(A\cap B)$, $P(A\,|\,B)$\dots). Fes un diagrama de Venn, una taula de contingència o un diagrama d'arbre quan t'ajude. Els " + str(npau) + r" exercicis marcats amb \textcolor{teal}{\faUniversity\ PAU} són de les proves d'accés a la universitat d'altres comunitats autònomes.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            n += 1
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't9-fitxa-solucions.tex' if sol else 't9-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n, npau

n = build(False); build(True)
print(n[0], 'exercicis,', n[1], 'de la PAU;', len(CHK), 'comprovacions')
