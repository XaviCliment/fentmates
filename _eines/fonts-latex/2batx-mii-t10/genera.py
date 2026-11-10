# Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 10: Probabilitat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat les estrelles no es mostren.
# Les seccions segueixen els apunts interactius (materials/2batx-mii/t10-probabilitat.html), que són els de la unitat 9 de
# CCSS amb recompte, tres successos, «almenys un» en n proves, variables aleatòries i distribució binomial. La fitxa és un
# poc més difícil que la de CCSS (_eines/fonts-latex/2batx-ccss-t9) i acaba amb problemes de síntesi (Bayes + binomial).
# Els exercicis marcats amb \pau{...} són de la PAU de Matemàtiques II d'altres comunitats (la valenciana té la seua pàgina),
# traduïts al valencià i presos del recull «Estadística y probabilidad en pruebas de acceso a la universidad de todas las
# comunidades autónomas de España» (Matemàtiques II, curs 2026/27) de Juan Antonio Martínez García (www.ebaumatematicas.com).
# No s'hi han inclòs els exercicis de la distribució normal ni els d'aproximació de la binomial per la normal.
# Totes les probabilitats es calculen ací (fraccions exactes, recompte o binomial) i CHK, al final, les compara amb les
# solucions oficials. Errades del llibre corregides: Aragó ord. 2025 (4.2 b: P(A)=20/33 i P(B)=15/22, el llibre repeteix
# els valors de l'apartat a); Aragó ord. 2024 (51,85 % i no 51,89 %).
# Ús: python3 genera.py && pdflatex t10-fitxa-exercicis.tex (dues vegades) && pdflatex t10-fitxa-solucions.tex (dues vegades)
import os, re
from math import comb, perm, log, ceil, sqrt
from fractions import Fraction as F
from itertools import product, permutations
HERE = os.path.dirname(os.path.abspath(__file__))

def tasks(n, items):
    if any(len(re.sub(r'\\[a-z]+|[{}$]', '', i)) > 70 for i in items): n = 1
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
def d4(x): return ('%.4f' % float(x)).replace('.', '{,}')
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
def B(x): return r'\res{' + N(x) + '}'
def B4(x): return r'\res{' + (dec(x, 6) if isinstance(x, F) and p10(x.denominator) and x.denominator <= 10**4 else r'\approx' + d4(x)) + '}'
def pc(x, k=2): return dec(F(x) * 100, k) + r'\,\%'

# ---------- binomial ----------
def pmf(n, p, k): p = F(p); return comb(n, k) * p**k * (1 - p)**(n - k)
def cdf(n, p, a, b): return sum(pmf(n, p, k) for k in range(a, b + 1))
def bt(n, p, k):
    """terme de la binomial en TeX"""
    return r'\binom{%d}{%d}%s^{%d}\,%s^{%d}' % (n, k, Q(p), k, Q(1 - F(p)), n - k)

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
            o.append(r'    child {node[anchor=west] {$%s$%s} edge from parent node[%s] {%s}}' % (kl, (r'\ \ {\color{teal}\scriptsize$%s$}' % (Q(leaf) if not isinstance(leaf, str) else leaf)) if leaf != '' else '', pos(j, len(kids)), p(kp)))
        o.append(r'    edge from parent node[%s] {%s}}' % (pos(i, len(br)), p(pr)))
    o.append(';\\end{tikzpicture}')
    return '\n'.join(o)
def arb2(names, pri, cond, la='D', s=(2.4, 1.3)):
    """arbre de dos nivells per a probabilitat total: names[i], pri[i] = P(A_i), cond[i] = P(D|A_i)"""
    return arbre([(n, F(p), [(la, F(c), F(p) * F(c)), (r'\overline{%s}' % la, 1 - F(c), F(p) * (1 - F(c)))]) for n, p, c in zip(names, pri, cond)], s=s)
def cen(*gs): return '\n\n\\begin{center}' + '\\qquad'.join(gs) + '\\end{center}\n'

CHK = []  # (calculat, oficial o esperat, tolerància): es comprova al final
def ck(x, y, tol=None):
    CHK.append((x, y, tol)); return x
def tot(pr, cd): return sum(F(p) * F(c) for p, c in zip(pr, cd))

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
# 1. Experiments, Laplace i recompte
D2 = list(product(range(1, 7), repeat=2))
def pd(f): return F(sum(1 for a, b in D2 if f(a, b)), 36)
l1 = [pd(lambda a, b: max(a, b) == 4), pd(lambda a, b: abs(a - b) <= 1), pd(lambda a, b: a > b), pd(lambda a, b: (a * b) % 3 == 0)]
ck(l1, [F(7, 36), F(4, 9), F(5, 12), F(5, 9)])
cm = [F(comb(6, 2) * comb(5, 2), comb(11, 4)), 1 - F(comb(5, 4), comb(11, 4))]
ck(cm, [F(5, 11), F(65, 66)])
lb = F(perm(3, 3) * perm(3, 3), perm(5, 5)); ck(lb, F(3, 10))
pr6, pr5 = F(1, comb(49, 6)), F(comb(6, 5) * comb(43, 1), comb(49, 6)); ck([comb(49, 6), comb(6, 5) * 43], [13983816, 258])
an5, an23 = 1 - F(perm(365, 5), 365**5), 1 - F(perm(365, 23), 365**23); ck([float(an5), float(an23)], [0.0271, 0.5073], 1e-4)
dt = [F(k, 21) for k in range(1, 7)]; ck([sum(dt), dt[1] + dt[3] + dt[5], 1 - dt[0] - dt[1]], [1, F(4, 7), F(6, 7)])
mon = [1 - F(comb(5, 3), comb(10, 3)), F(2, 10)]; ck(mon, [F(11, 12), F('0.2')])
eu = [F(comb(7, 2), comb(12, 2)), F(comb(5, 2) + 5 * 2, comb(12, 2)), 1 - F(2 * comb(5, 3), comb(10, 3))]
ck([float(v) for v in eu], [0.3182, 0.303, 0.8333], 1e-4)
S.append(("Experiments aleatoris, regla de Laplace i recompte", [
 (1, r"Siguen $A$, $B$ i $C$ tres successos d'un mateix experiment. Expressa amb operacions:" + tasks(2, [
      r"Ocorre només $B$.", r"N'ocorre almenys un.", r"No n'ocorre cap.", r"N'ocorre exactament un.", r"N'ocorren almenys dos.", r"N'ocorren com a molt dos."])
     + recorda(r"De Morgan: $\overline{A\cup B}=\co A\cap\co B$ i $\overline{A\cap B}=\co A\cup\co B$; també valen per a tres successos."),
     tasks(1, [r"$\res{\co A\cap B\cap\co C}$", r"$\res{A\cup B\cup C}$", r"$\res{\co A\cap\co B\cap\co C=\overline{A\cup B\cup C}}$",
               r"$\res{(A\cap\co B\cap\co C)\cup(\co A\cap B\cap\co C)\cup(\co A\cap\co B\cap C)}$", r"$\res{(A\cap B)\cup(A\cap C)\cup(B\cap C)}$",
               r"$\res{\overline{A\cap B\cap C}=\co A\cup\co B\cup\co C}$"])),
 (1, r"Llancem dos daus. Calcula la probabilitat que:" + tasks(2, [r"el resultat més alt siga un 4;", r"els dos resultats es diferencien com a molt en 1;", r"el primer siga més gran que el segon;", r"el producte siga múltiple de 3."]),
     r"Hi ha $36$ parelles equiprobables." + tasks(2, [r"$(1,4),\dots,(4,4)$ i $(4,1),(4,2),(4,3)$: $\frac{7}{36}=" + B(l1[0]) + "$", r"$6+5+5=16$ parelles: $" + B(l1[1]) + "$",
      r"per simetria, $\frac{36-6}{2}=15$ parelles: $" + B(l1[2]) + "$", r"$1-\frac{4\cdot4}{36}=\frac{20}{36}=" + B(l1[3]) + "$ (cap dels dos és 3 o 6)"])),
 (1, r"En un grup hi ha 6 xiques i 5 xics. Es trien a l'atzar 4 persones per a fer un treball. Calcula la probabilitat que hi haja dues xiques i dos xics, i la que hi haja almenys una xica."
     + recorda(r"si triem un grup (no importa l'ordre), comptem amb combinacions: $\binom nk=\frac{n!}{k!\,(n-k)!}$."),
     r"Casos possibles: $\binom{11}{4}=330$." + tasks(1, [r"$\dfrac{\binom62\binom52}{\binom{11}4}=\dfrac{15\cdot10}{330}=" + B(cm[0]) + "$",
      r"$1-\dfrac{\binom54}{\binom{11}{4}}=1-\dfrac{5}{330}=" + B(cm[1]) + "$"])),
 (1, r"Col·loquem a l'atzar en una prestatgeria 5 llibres diferents, 3 dels quals són de matemàtiques. Quina és la probabilitat que els tres de matemàtiques queden junts?",
     r"Casos possibles: $5!=120$. Favorables: el bloc de matemàtiques i els altres dos llibres es poden ordenar de $3!$ maneres, i dins del bloc, de $3!$ maneres: $36$. $\ P=\frac{36}{120}=" + B(lb) + "$."),
 (2, r"En la Loteria Primitiva s'extrauen 6 números de l'1 al 49. Una persona fa una aposta de 6 números. Calcula la probabilitat que encerte els 6 números i la que n'encerte exactament 5.",
     r"Casos possibles: $\binom{49}{6}=13\,983\,816$." + tasks(1, [r"$P(6)=\dfrac{1}{13\,983\,816}\approx" + r"\res{7{,}15\cdot10^{-8}}$",
      r"$P(5)=\dfrac{\binom65\binom{43}1}{\binom{49}6}=\dfrac{258}{13\,983\,816}\approx\res{1{,}85\cdot10^{-5}}$ (5 dels 6 premiats i 1 dels 43 restants)"])
     + ('' if ck([float(pr6), float(pr5)], [7.15e-8, 1.845e-5], 1e-7) else '')),
 (2, r"\emph{Problema dels aniversaris.} Suposem que tots els dies de l'any (365) són igual de probables per a nàixer. Calcula la probabilitat que, en un grup de 5 persones, almenys dues facen anys el mateix dia. Repeteix el càlcul per a un grup de 23 persones (amb la calculadora).",
     r"El contrari és que tots facen anys en dies diferents: $P=1-\dfrac{V_{365,5}}{365^5}=1-\dfrac{365\cdot364\cdot363\cdot362\cdot361}{365^5}\approx" + r"\res{" + d4(an5) + "}$."
     + r" Per a 23 persones: $1-\dfrac{V_{365,23}}{365^{23}}\approx\res{" + d4(an23) + r"}$: ja és més probable que sí que no!"),
 (1, r"Un dau està trucat de manera que la probabilitat de cada cara és proporcional al número que hi apareix. Calcula la probabilitat de cada cara, la d'obtindre un nombre parell i la d'obtindre més de 2.",
     r"$P(k)=c\,k$ i $c(1+2+\dots+6)=21c=1\Rightarrow\res{P(k)=\frac{k}{21}}$. \ $P(\text{parell})=\frac{2+4+6}{21}=" + B(F(12, 21)) + r"$; \ $P(X>2)=1-\frac{1+2}{21}=" + B(F(18, 21)) + "$."),
 (1, r"\pau{Astúries, extraordinària 2025} En un moneder hi ha 5 monedes d'1 euro, 3 de 2 euros i 2 de 10 cèntims." + tasks(1, [
      r"Si traiem 3 monedes a l'atzar, quina és la probabilitat que almenys una siga d'1 euro?", r"Traiem dues monedes, una darrere l'altra (sense reemplaçament). Quina és la probabilitat que la segona siga de 10 cèntims?"]),
     tasks(1, [r"$1-P(\text{cap d'1 euro})=1-\dfrac{\binom53}{\binom{10}3}=1-\dfrac{10}{120}=" + B(mon[0]) + "$",
               r"$\frac{2}{10}\cdot\frac19+\frac{8}{10}\cdot\frac29=\frac{18}{90}=" + B(mon[1]) + "$ (com la primera: l'ordre no afavoreix cap posició)"])),
 (2, r"\pau{Navarra, ordinària 2026} Sobre la Pedra de Sant Martí es troben 5 bearnesos, 5 roncalesos i 2 suletins. Els bearnesos parlen entre ells en bearnés; els roncalesos, en basc; els suletins parlen entre ells en basc, però també es poden comunicar en bearnés amb els bearnesos." + tasks(1, [
      r"Agafant dues persones a l'atzar, quina és la probabilitat que es comuniquen en basc?", r"Agafant dues persones a l'atzar, quina és la probabilitat que es comuniquen en bearnés?",
      r"Els 5 roncalesos i els 5 bearnesos se'n van a celebrar la pau. Si se n'asseuen tres a l'atzar en una taula, quina és la probabilitat que no parlen tots el mateix idioma?"]),
     r"Parelles possibles: $\binom{12}{2}=66$." + tasks(1, [r"Parlen basc entre ells els $5+2=7$ roncalesos i suletins: $\frac{\binom72}{66}=\frac{21}{66}=" + B(eu[0]) + "$",
      r"Dos bearnesos o un bearnés i un suletí: $\frac{\binom52+5\cdot2}{66}=\frac{20}{66}=" + B(eu[1]) + "$",
      r"$1-P(\text{tots tres del mateix poble})=1-\dfrac{2\binom53}{\binom{10}3}=1-\dfrac{20}{120}=" + B(eu[2]) + "$"])),
]))

# =====================================================================
# 2. Fórmules
f1 = dict(a=F('0.5'), b=F('0.4'), i=1 - F('0.8')); f1['u'] = f1['a'] + f1['b'] - f1['i']
ck([f1['i'], f1['u'], f1['u'] - f1['i'], f1['b'] - f1['i'], 1 - f1['u']], [F('0.2'), F('0.7'), F('0.5'), F('0.2'), F('0.3')])
t3 = [F('0.5'), F('0.4'), F('0.3'), F('0.2'), F('0.15'), F('0.1'), F('0.05')]
u3 = t3[0] + t3[1] + t3[2] - t3[3] - t3[4] - t3[5] + t3[6]; nA3 = t3[0] - t3[3] - t3[4] + t3[6]
ex1 = (t3[0] - t3[3] - t3[4] + t3[6]) + (t3[1] - t3[3] - t3[5] + t3[6]) + (t3[2] - t3[4] - t3[5] + t3[6])
ck([u3, 1 - u3, nA3, ex1], [F('0.8'), F('0.2'), F('0.2'), F('0.45')])
bl = dict(a=F('0.75'), b=1 - F('0.45'), amb=F('0.3')); bl['i'] = bl['a'] - bl['amb']
ck([bl['i'], bl['b'] - bl['i'], 1 - (bl['a'] + bl['b'] - bl['i'])], [F('0.45'), F('0.1'), F('0.15')])
rj = dict(a=F('0.27'), b=1 - F('0.82'), u=F('0.4')); rj['i'] = rj['a'] + rj['b'] - rj['u']
ck([rj['i'], 1 - rj['u'], 1 - rj['i']], [F('0.05'), F('0.6'), F('0.95')])
S.append(("Fórmules de la probabilitat", [
 (1, r"De dos successos se sap que $P(A)=0{,}5$, $P(B)=0{,}4$ i $P(\co A\cup\co B)=0{,}8$. Calcula:" + tasks(3, [r"$P(A\cap B)$", r"$P(A\cup B)$", r"$P(\text{només un})$", r"$P(\co A\cap B)$", r"$P(\co A\cap\co B)$"])
     + recorda(r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$; \ $P(\co A)=1-P(A)$; \ $P(A\cap\co B)=P(A)-P(A\cap B)$."),
     r"De Morgan: $P(A\cap B)=1-P(\co A\cup\co B)$." + tasks(3, [r"$1-0{,}8=" + B(f1['i']) + "$", r"$0{,}5+0{,}4-0{,}2=" + B(f1['u']) + "$", r"$0{,}7-0{,}2=" + B(f1['u'] - f1['i']) + "$",
      r"$0{,}4-0{,}2=" + B(f1['b'] - f1['i']) + "$", r"$1-0{,}7=" + B(1 - f1['u']) + "$"]) + cen(venn(f1['a'] - f1['i'], f1['i'], f1['b'] - f1['i'], 1 - f1['u']))),
 (2, r"Siguen $A$ i $B$ dos successos amb $P(A)=0{,}7$ i $P(B)=0{,}6$." + tasks(1, [r"Poden ser incompatibles?", r"Entre quins valors pot estar $P(A\cap B)$? I $P(A\cup B)$?", r"Demostra que, en general, $P(A\cap B)\geq P(A)+P(B)-1$ per a dos successos qualssevol."]),
     tasks(1, [r"\rest{No}: si ho foren, $P(A\cup B)=1{,}3>1$.", r"$P(A\cap B)=1{,}3-P(A\cup B)\geq0{,}3$ i $A\cap B\subset B\Rightarrow P(A\cap B)\leq0{,}6$: \ $\res{0{,}3\leq P(A\cap B)\leq0{,}6}$ \ i \ $\res{0{,}7\leq P(A\cup B)\leq1}$.",
               r"Com que $P(A\cup B)\leq1$: $P(A\cap B)=P(A)+P(B)-P(A\cup B)\geq P(A)+P(B)-1$. \rest{(Desigualtat de Bonferroni.)}"])),
 (2, r"Tres successos compleixen $P(A)=0{,}5$, $P(B)=0{,}4$, $P(C)=0{,}3$, $P(A\cap B)=0{,}2$, $P(A\cap C)=0{,}15$, $P(B\cap C)=0{,}1$ i $P(A\cap B\cap C)=0{,}05$. Calcula la probabilitat que:" + tasks(2, [
      r"n'ocórrega almenys un;", r"no n'ocórrega cap;", r"ocórrega només $A$;", r"n'ocórrega exactament un."]),
     tasks(2, [r"$0{,}5+0{,}4+0{,}3-0{,}2-0{,}15-0{,}1+0{,}05=" + B(u3) + "$", r"$1-0{,}8=" + B(1 - u3) + "$", r"$0{,}5-0{,}2-0{,}15+0{,}05=" + B(nA3) + "$",
               r"$0{,}2+0{,}15+0{,}05=" + B(ex1) + "$ (només $A$, només $B$ i només $C$)"])),
 (1, r"En una enquesta a 200 persones, 120 s'informen per les xarxes socials, 90 per la televisió i 40 per tots dos mitjans. Construeix la taula de contingència i calcula la probabilitat que una persona triada a l'atzar s'informe per algun dels dos mitjans, per cap i només per un.",
     cen(taula(['X', r'\overline{X}'], ['T', r'\overline{T}'], [[40, 80, 120], [50, 30, 80], [90, 110, 200]], str)) +
     tasks(3, [r"$\frac{170}{200}=" + B(F(170, 200)) + "$", r"$\frac{30}{200}=" + B(F(30, 200)) + "$", r"$\frac{80+50}{200}=" + B(F(130, 200)) + "$"])),
 (1, r"\pau{Illes Balears, extraordinària 2025} Siguen $A$ i $B$ dos successos d'un experiment aleatori i $A'$, $B'$ els seus contraris. Sabent que $P(A)=0{,}75$, $P(B')=0{,}45$ i $P(A-B)=0{,}3$, calcula:" + tasks(3, [r"$P(A\cap B)$", r"$P(B-A)$", r"$P(A'\cap B')$"]),
     r"$P(B)=0{,}55$." + tasks(3, [r"$P(A)-P(A-B)=" + B(bl['i']) + "$", r"$0{,}55-0{,}45=" + B(bl['b'] - bl['i']) + "$", r"$1-(0{,}75+0{,}55-0{,}45)=" + B(1 - bl['a'] - bl['b'] + bl['i']) + "$"])),
 (1, r"\pau{La Rioja, ordinària 2024} De dos successos $A$ i $B$ se sap que $P(A)=0{,}27$, $P(B')=0{,}82$ i $P(A\cup B)=0{,}4$. Determina si són compatibles o incompatibles i calcula $P\big((A\cup B)'\big)$ i $P(A'\cup B')$.",
     r"$P(A\cap B)=0{,}27+0{,}18-0{,}4=0{,}05\neq0$: \rest{són compatibles}. \ $P\big((A\cup B)'\big)=1-0{,}4=" + B(1 - rj['u']) + r"$; \ $P(A'\cup B')=1-P(A\cap B)=" + B(1 - rj['i']) + "$."),
]))

# =====================================================================
# 3. Condicionada i independència
c1 = dict(a=F('0.6')); c1['ab'] = c1['a'] * F('0.5'); c1['b'] = c1['ab'] + (1 - c1['a']) * F('0.25')
ck([c1['ab'], c1['b'], c1['ab'] / c1['b'], c1['a'] + c1['b'] - c1['ab']], [F('0.3'), F('0.4'), F('0.75'), F('0.7')])
sh = [1 - F('0.4') * F('0.5') * F('0.6'), F('0.6') * F('0.5') * F('0.6') + F('0.6') * F('0.5') * F('0.4') + F('0.4') * F('0.5') * F('0.4')]
ck(sh, [F('0.88'), F('0.38')])
xs = F(1, 2); ck(2 * xs - xs * xs, F(3, 4))
ast = [F('0.1') + F('0.05') - F('0.008'), F('0.008') / F('0.1')]; ck(ast, [F('0.142'), F('0.08')])
bal = [F('0.35') - F('0.25'), F('0.25') / F('0.6')]; ck([bal[0] * 60, bal[1]], [6, F(5, 12)])
cn = dict(a=F('0.4'), b=F('0.65'), u=1 - F('0.1')); cn['i'] = cn['a'] + cn['b'] - cn['u']
ck([cn['i'], cn['i'] / cn['b'], cn['i'] / cn['a'], (cn['a'] - cn['i']) / (1 - cn['b'])], [F('0.15'), F(3, 13), F('0.375'), F(5, 7)])
ex = dict(c=F('0.8'), x=F('0.6'), u=1 - F('0.1')); ex['i'] = ex['c'] + ex['x'] - ex['u']
ck([ex['i'], ex['u'] - ex['i'], (ex['c'] - ex['i']) / (1 - ex['x'])], [F('0.5'), F('0.4'), F('0.75')])
ga, gb = F(1, 3), F(1, 2)
ck([ga + gb - ga * gb, (1 - ga) / (1 - ga * gb), ga + gb, (1 - ga) / 1], [F(2, 3), F(4, 5), F(5, 6), F(2, 3)])
cl = dict(a=F('0.2'), i=F('0.1'), u=F('0.3')); cl['b'] = cl['u'] - cl['a'] + cl['i']
ck([cl['b'], cl['a'] - cl['i'], cl['i'] / cl['b'], cl['i'] / cl['a']], [F('0.2'), F('0.1'), F('0.5'), F('0.5')])
md = dict(b=F('0.4'), u=1 - F('0.4')); md['a'] = (md['u'] - md['b']) / (1 - F('0.2')); md['i'] = F('0.2') * md['a']
ck([1 - md['a'], md['i'], md['i'] / md['u']], [F('0.75'), F('0.05'), F(1, 12)])
mc = dict(a=F('0.7'), b=1 - F('0.2'), nn=F('0.1')); mc['u'] = 1 - mc['nn']; mc['i'] = mc['a'] + mc['b'] - mc['u']
ck([(1 - mc['a']) * (1 - mc['b']) == mc['nn'], mc['i'], (mc['b'] - mc['i']) / mc['b']], [False, F('0.6'), F('0.25')])
pv = dict(a=F('0.7'), b=F('0.1'))
pvr = [pv['a'] + pv['b'] - pv['a'] * pv['b'], 1 - pv['a'] * pv['b'], (1 - pv['a']) * (1 - pv['b']), pv['a'] * (1 - pv['b']), 1 - pv['a']]
ck(pvr, [F('0.73'), F('0.93'), F('0.27'), F('0.63'), F('0.3')])
bo = dict(u=F('0.7'), i=F('0.1'), anb=F('0.35')); bo['a'] = bo['i'] + bo['anb']; bo['b'] = bo['u'] - bo['anb']
ck([bo['a'], bo['b'], 1 - bo['i'], bo['a'] * bo['b'] == bo['i']], [F('0.45'), F('0.35'), F('0.9'), False])
mu = dict(i=F('0.6'), b=F('0.4'), ib=F('0.2'))
ck([mu['i'] * mu['b'] == mu['ib'], mu['ib'] / mu['i'], 1 - (mu['i'] + mu['b'] - mu['ib']), (mu['b'] - mu['ib']) / (1 - mu['i'])], [False, F(1, 3), F('0.2'), F('0.5')])
# Aragó ord. 2025: P(A|B)=2/3, P(B|A)=3/4; b) P(A∪B)=5/6
ar_x = F(5, 6) / (F(4, 3) + F(3, 2) - 1); ar_a, ar_b = F(4, 3) * ar_x, F(3, 2) * ar_x
ck([F(2, 3) + F(3, 4) - F(2, 3) * F(3, 4), ar_x, ar_a, ar_b, 1 - (ar_b - ar_x), ar_x / ar_b, ar_x / ar_a], [F(11, 12), F(5, 11), F(20, 33), F(15, 22), F(17, 22), F(2, 3), F(3, 4)])
cy = dict(d=F('0.55'), v=F('0.15')); cy['dv'] = cy['d'] * F(1, 5); cy['hv'] = cy['v'] - cy['dv']
ck([cy['hv'] / (1 - cy['d']), cy['dv'] / cy['v'], cy['hv']], [F(4, 45), F(11, 15), F('0.04')]); ck(float(cy['hv'] / (1 - cy['d'])), 0.0889, 1e-4)
cb = dict(c=F('0.6'), bl=F('0.08')); cb['ml'] = 1 - cb['c'] - cb['bl']
ck([cb['ml'] / (1 - cb['c']), cb['ml'] / (1 - F('0.2')), (F('0.8') - cb['ml']) / cb['c']], [F('0.8'), F('0.4'), F('0.8')])
gz = [F('0.8') + F('0.2') * F('0.75'), F('0.2') * F('0.75')]; ck(gz, [F('0.95'), F('0.15')])
gx = F(12 * 8, 60 - 12); ck([gx, F(gx, 60) == F(8 + gx, 60) * F(12, 60)], [2, True])
lr = [F('0.6'), F('0.75'), F('0.8')]
lr3 = lr[0] * lr[1] * lr[2]; lr1 = sum((1 - lr[j]) * lr[(j + 1) % 3] * lr[(j + 2) % 3] for j in range(3)); lrm = (1 - lr[0]) * lr[1] * lr[2]
ck([lr3, lr1, lrm / lr1], [F('0.36'), F('0.45'), F(8, 15)])
az = [F(28, 54), F(21, 45), F(28, 49)]; ck([float(az[0]), float(az[1]), az[2]], [0.5185, 0.4667, F(4, 7)], 1e-4)
S.append(("Probabilitat condicionada i independència", [
 (1, r"De dos successos se sap que $P(A)=0{,}6$, $P(B\cond A)=0{,}5$ i $P(B\cond\co A)=0{,}25$. Calcula $P(A\cap B)$, $P(B)$, $P(A\cond B)$ i $P(A\cup B)$. Són independents?"
     + recorda(r"$P(A\cond B)=\dfrac{P(A\cap B)}{P(B)}$. $A$ i $B$ són independents si $P(A\cap B)=P(A)P(B)$, és a dir, si $P(A\cond B)=P(A)$."),
     r"$P(A\cap B)=0{,}6\cdot0{,}5=" + B(c1['ab']) + r"$; \ $P(B)=0{,}3+0{,}4\cdot0{,}25=" + B(c1['b']) + r"$; \ $P(A\cond B)=\frac{0{,}3}{0{,}4}=" + B(c1['ab'] / c1['b'])
     + r"$; \ $P(A\cup B)=0{,}6+0{,}4-0{,}3=" + B(c1['a'] + c1['b'] - c1['ab']) + r"$. Com que $P(B\cond A)=0{,}5\neq P(B)=0{,}4$, \rest{no són independents}."),
 (2, r"Demostra que si $A$ i $B$ són independents, també ho són $A$ i $\co B$. Dedueix que també ho són $\co A$ i $\co B$.",
     r"$P(A\cap\co B)=P(A)-P(A\cap B)=P(A)-P(A)P(B)=P(A)\big(1-P(B)\big)=P(A)\,P(\co B)$. \ Aplicant el mateix resultat a la parella $\co B$, $A$ (que són independents), també són independents $\co B$ i $\co A$."),
 (1, r"Dos successos independents tenen la mateixa probabilitat i $P(A\cup B)=0{,}75$. Calcula $P(A)$ i la probabilitat que n'ocórrega exactament un.",
     r"$2x-x^2=0{,}75\Rightarrow x^2-2x+0{,}75=0\Rightarrow x=0{,}5$ (l'altra solució, $1{,}5$, no és una probabilitat): $\res{P(A)=0{,}5}$. \ $P(\text{exactament un})=2\cdot0{,}5\cdot0{,}5=" + B(F(1, 2)) + "$."),
 (1, r"Tres tiradors disparen una vegada cadascun a un blanc, de manera independent. Les probabilitats que encerten són $0{,}6$, $0{,}5$ i $0{,}4$. Calcula la probabilitat que el blanc reba algun impacte i la que en reba exactament dos.",
     r"$P(\text{almenys un})=1-0{,}4\cdot0{,}5\cdot0{,}6=" + B(sh[0]) + r"$. \ Exactament dos: $0{,}6\cdot0{,}5\cdot0{,}6+0{,}6\cdot0{,}5\cdot0{,}4+0{,}4\cdot0{,}5\cdot0{,}4=" + B(sh[1]) + "$."),
 (1, r"\pau{Astúries, ordinària 2026} En una fàbrica de pantalons texans, el 10\,\% de les peces no passa el test de longitud, el 5\,\% no passa el de les costures i el 0,8\,\% no passa cap dels dos." + tasks(1, [
      r"Calcula la probabilitat que una peça triada a l'atzar no passe almenys un dels tests.", r"Si una peça no ha passat el test de longitud, quina probabilitat hi ha que tampoc passe el de les costures?"]),
     tasks(1, [r"$0{,}1+0{,}05-0{,}008=" + B(ast[0]) + "$", r"$\frac{0{,}008}{0{,}1}=" + B(ast[1]) + "$"])),
 (1, r"\pau{Illes Balears, extraordinària 2026} En un institut de 60 alumnes, el 60\,\% juga a bàsquet, el 35\,\% forma part d'un equip federat i el 25\,\% juga a bàsquet i està federat." + tasks(1, [
      r"Hi ha algun alumne federat que no jugue a bàsquet? Si n'hi ha, quants?", r"Quina és la probabilitat que un alumne siga d'un equip federat sabent que juga a bàsquet?"]),
     tasks(1, [r"$0{,}35-0{,}25=0{,}1$ i $0{,}1\cdot60=\res{6\text{ alumnes}}$.", r"$P(F\cond B)=\frac{0{,}25}{0{,}6}=" + B(bal[1]) + "$"])),
 (1, r"\pau{Cantàbria, ordinària 2025} En un col·legi s'ofereixen atletisme ($A$) i bàsquet ($B$) com a activitats extraescolars, amb $P(A)=0{,}4$ i $P(B)=0{,}65$. Només un 10\,\% de l'alumnat no es matricula en cap esport." + tasks(1, [
      r"Calcula la probabilitat que un alumne es matricule en els dos esports.", r"Calcula $P(A\cond B)$, $P(B\cond A)$ i $P(A\cond B^c)$."]),
     tasks(1, [r"$P(A\cap B)=0{,}4+0{,}65-0{,}9=" + B(cn['i']) + "$", r"$\frac{0{,}15}{0{,}65}=" + B(cn['i'] / cn['b']) + r"$; \ $\frac{0{,}15}{0{,}4}=" + B(cn['i'] / cn['a']) + r"$; \ $\frac{0{,}25}{0{,}35}=" + B((cn['a'] - cn['i']) / (1 - cn['b'])) + "$"])),
 (1, r"\pau{Extremadura, ordinària 2024} En una residència, el 80\,\% dels residents té correu electrònic, el 60\,\% té xarxes socials i el 10\,\% no té ni l'un ni les altres. Calcula la probabilitat que un resident:" + tasks(1, [
      r"use correu electrònic i xarxes socials;", r"use només una de les dues coses;", r"use correu electrònic sabent que no usa xarxes socials."]),
     cen(ct(ex['c'], ex['x'], ex['i'], 'C', 'X')) + tasks(3, [r"$0{,}8+0{,}6-0{,}9=" + B(ex['i']) + "$", r"$0{,}9-0{,}5=" + B(ex['u'] - ex['i']) + "$", r"$\frac{0{,}3}{0{,}4}=" + B((ex['c'] - ex['i']) / (1 - ex['x'])) + "$"])),
 (2, r"\pau{Galícia, ordinària 2024} Se sap que $P(A)=\frac13$ i $P(B)=\frac12$." + tasks(1, [
      r"Suposant que $A$ i $B$ són independents, calcula $P(A\cup B)$ i $P\big(\co A\,/\,(\co A\cup\co B)\big)$.", r"Suposant que $A$ i $B$ són incompatibles, calcula $P(A\cup B)$ i $P\big(\co A\,/\,(\co A\cup\co B)\big)$."]),
     tasks(1, [r"$P(A\cup B)=\frac13+\frac12-\frac16=" + B(F(2, 3)) + r"$. Com que $\co A\subset\co A\cup\co B$: $\dfrac{P(\co A)}{1-P(A\cap B)}=\dfrac{2/3}{5/6}=" + B(F(4, 5)) + "$",
               r"$P(A\cup B)=\frac13+\frac12=" + B(F(5, 6)) + r"$. Ara $\co A\cup\co B=\overline{A\cap B}=E$: $P(\co A)=" + B(F(2, 3)) + "$"])),
 (1, r"\pau{Castella-la Manxa, ordinària 2024} Siguen $A$ i $B$ dos successos tals que $P(A)=0{,}2$, $P(A\cap B)=0{,}1$ i $P(A\cup B)=0{,}3$. Calcula $P(B)$, $P(A\cap\co B)$, $P(A\cond B)$ i $P(B\cond A)$.",
     r"$P(B)=0{,}3-0{,}2+0{,}1=" + B(cl['b']) + r"$; \ $P(A\cap\co B)=0{,}2-0{,}1=" + B(cl['a'] - cl['i']) + r"$; \ $P(A\cond B)=\frac{0{,}1}{0{,}2}=" + B(cl['i'] / cl['b']) + r"$; \ $P(B\cond A)=" + B(cl['i'] / cl['a']) + "$."),
 (2, r"\pau{Madrid, ordinària 2026} Sabent que $P(B)=0{,}4$, $P\big(\overline{A\cup B}\big)=0{,}4$ i $P(B\cond A)=0{,}2$, calcula:" + tasks(1, [r"$P(\co A)$ i $P(A\cap B)$.", r"$P\big((A\cap B)\cond(A\cup B)\big)$."]),
     tasks(1, [r"Si $P(A)=x$: $P(A\cap B)=0{,}2x$ i $P(A\cup B)=x+0{,}4-0{,}2x=0{,}6\Rightarrow x=0{,}25$. \ $P(\co A)=" + B(1 - md['a']) + r"$, \ $P(A\cap B)=" + B(md['i']) + "$",
               r"$A\cap B\subset A\cup B$: \ $\frac{0{,}05}{0{,}6}=" + B(md['i'] / md['u']) + "$"])),
 (1, r"\pau{Madrid, ordinària 2025 (coincidències)} Se sap que $P(A)=0{,}7$, $P(\co B)=0{,}2$ i $P(\co A\cap\co B)=0{,}1$." + tasks(1, [
      r"Raona si $\co A$ i $\co B$ són independents.", r"Calcula $P(A\cap B)$.", r"Calcula $P(\co A\cond B)$."]),
     tasks(1, [r"$P(\co A)P(\co B)=0{,}3\cdot0{,}2=0{,}06\neq0{,}1$: \rest{no són independents}.", r"$P(A\cup B)=0{,}9\Rightarrow P(A\cap B)=0{,}7+0{,}8-0{,}9=" + B(mc['i']) + "$",
               r"$\frac{P(B)-P(A\cap B)}{P(B)}=\frac{0{,}2}{0{,}8}=" + B((mc['b'] - mc['i']) / mc['b']) + "$"])),
 (1, r"\pau{País Basc, extraordinària 2024} Siguen $A$ i $B$ successos independents amb $P(A)=0{,}7$ i $P(B)=0{,}1$. Calcula raonadament:" + tasks(3, [r"$P(A\cup B)$", r"$P(\co A\cup\co B)$", r"$P(\co A\cap\co B)$", r"$P(A\cap\co B)$", r"$P(\co A\cond B)$"]),
     tasks(2, [r"$0{,}7+0{,}1-0{,}07=" + B(pvr[0]) + "$", r"$1-P(A\cap B)=" + B(pvr[1]) + "$", r"$0{,}3\cdot0{,}9=" + B(pvr[2]) + "$ (independents)", r"$0{,}7\cdot0{,}9=" + B(pvr[3]) + "$",
               r"$P(\co A)=" + B(pvr[4]) + "$ (independents)"])),
 (1, r"\pau{Illes Balears, ordinària 2024} Siguen $A$ i $B$ dos successos amb $P(A\cup B)=0{,}7$, $P(A\cap B)=0{,}1$ i $P(A\cap B^c)=0{,}35$. Calcula:" + tasks(4, [r"$P(A)$", r"$P(B)$", r"$P(A^c\cup B^c)$", r"Són independents?"]),
     tasks(2, [r"$0{,}1+0{,}35=" + B(bo['a']) + "$", r"$0{,}7-0{,}35=" + B(bo['b']) + "$", r"$1-0{,}1=" + B(1 - bo['i']) + "$", r"$0{,}45\cdot0{,}35=0{,}1575\neq0{,}1$: \rest{no}"])),
 (1, r"\pau{Múrcia, extraordinària 2024} El 60\,\% dels habitants d'una població consumeix pa integral, el 40\,\% pa blanc i el 20\,\% tots dos." + tasks(1, [
      r"Són independents els successos «consumir pa integral» i «consumir pa blanc»?", r"Sabent que un habitant consumeix pa integral, quina és la probabilitat que consumisca pa blanc?",
      r"Quin percentatge de la població no consumeix cap dels dos tipus de pa?", r"Sabent que un habitant no consumeix pa integral, quina és la probabilitat que consumisca pa blanc?"]),
     tasks(2, [r"$0{,}6\cdot0{,}4=0{,}24\neq0{,}2$: \rest{no}", r"$\frac{0{,}2}{0{,}6}=" + B(mu['ib'] / mu['i']) + "$", r"$1-0{,}8=0{,}2$: \ $\res{20\,\%}$", r"$\frac{0{,}4-0{,}2}{0{,}4}=" + B((mu['b'] - mu['ib']) / (1 - mu['i'])) + "$"])),
 (2, r"\pau{Aragó, ordinària 2025} De dos successos se sap que $P(A\cond B)=\frac23$ i $P(B\cond A)=\frac34$." + tasks(1, [
      r"Si $A$ i $B$ fóren independents, quant valdria $P(A\cup B)$?", r"Si $P(A\cup B)=\frac56$, quines són les probabilitats $P(A)$, $P(B)$ i $P(A\cup\co B)$?"]),
     tasks(1, [r"Independents: $P(A)=\frac23$ i $P(B)=\frac34$; \ $P(A\cup B)=\frac23+\frac34-\frac12=" + B(F(11, 12)) + "$",
               r"Si $x=P(A\cap B)$: $P(B)=\frac{3x}{2}$, $P(A)=\frac{4x}{3}$ i $\frac{4x}{3}+\frac{3x}{2}-x=\frac{11x}{6}=\frac56\Rightarrow x=\frac{5}{11}$. \ $P(A)=" + B(ar_a) + r"$, \ $P(B)=" + B(ar_b)
               + r"$, \ $P(A\cup\co B)=1-P(\co A\cap B)=1-\left(\frac{15}{22}-\frac{5}{11}\right)=" + B(1 - ar_b + ar_x) + "$"])),
 (1, r"\pau{Castella i Lleó, extraordinària 2025} En un grup de WhatsApp d'un gimnàs de judo, el 55\,\% són dones i la resta homes. El 15\,\% del grup és cinturó verd, i una cinquena part de les dones és cinturó verd." + tasks(1, [
      r"Quin percentatge dels homes és cinturó verd?", r"Si el grup rep un missatge d'un cinturó verd, quina és la probabilitat que l'haja enviat una dona?", r"Si no sabem res del remitent, quina és la probabilitat que siga home i cinturó verd?"]),
     r"$P(D\cap V)=0{,}55\cdot0{,}2=0{,}11$ i $P(H\cap V)=0{,}15-0{,}11=0{,}04$." + tasks(1, [r"$P(V\cond H)=\frac{0{,}04}{0{,}45}=" + B(cy['hv'] / F('0.45')) + r"$: \ $\res{8{,}89\,\%}$", r"$\frac{0{,}11}{0{,}15}=" + B(cy['dv'] / cy['v']) + "$", r"$" + B(cy['hv']) + "$"])),
 (1, r"\pau{Cantàbria, ordinària 2026} En un criador de cobais n'hi ha de pèl curt i de pèl llarg, blancs o marrons. El 60\,\% dels cobais és de pèl curt i només el 8\,\% són blancs de pèl llarg." + tasks(1, [
      r"Calcula la probabilitat que un cobai de pèl llarg triat a l'atzar siga marró.", r"Si la probabilitat que un cobai siga blanc és 0,2, calcula la probabilitat que un cobai marró siga de pèl llarg.", r"Amb la mateixa dada, calcula la probabilitat que un cobai de pèl curt siga marró."]),
     cen(taula(['C', 'L'], ['Bl', 'M'], [[F('0.12'), F('0.48'), F('0.6')], [F('0.08'), F('0.32'), F('0.4')], [F('0.2'), F('0.8'), 1]])) +
     tasks(3, [r"$\frac{0{,}32}{0{,}4}=" + B(cb['ml'] / F('0.4')) + "$", r"$\frac{0{,}32}{0{,}8}=" + B(cb['ml'] / F('0.8')) + "$", r"$\frac{0{,}48}{0{,}6}=" + B(F('0.48') / F('0.6')) + "$"])),
 (2, r"\pau{Galícia, extraordinària 2025} L'Antón té 60 parells de sabatilles, cadascun en la seua caixa: el 80\,\% són tradicionals i el 20\,\% de disseny. Entre les de disseny, el 75\,\% estan en bon estat, però només el 50\,\% de les tradicionals ho estan. Un dia agafa una caixa a l'atzar." + tasks(1, [
      r"Quina és la probabilitat que porte sabatilles tradicionals o en bon estat?", r"L'Antón no vol portar sabatilles que no estiguen en bon estat ni sabatilles tradicionals. Quina és la probabilitat que no haja de canviar-se?",
      r"L'Antón té 8 parells de sabatilles tradicionals blanques. Sabent que, en triar una caixa a l'atzar, els successos «ser blanques» i «ser de disseny» són independents, quants parells de sabatilles blanques de disseny té?"]),
     tasks(1, [r"$P(T\cup Bo)=P(T)+P(D\cap Bo)=0{,}8+0{,}2\cdot0{,}75=" + B(gz[0]) + "$", r"$P(D\cap Bo)=" + B(gz[1]) + "$",
               r"Si en té $x$: $\frac{x}{60}=\frac{8+x}{60}\cdot\frac{12}{60}\Rightarrow60x=96+12x\Rightarrow\res{x=2}$ parells."])),
 (1, r"\pau{La Rioja, ordinària 2026} Les probabilitats d'aprovar tres assignatures d'un grau són 60\,\%, 75\,\% i 80\,\% (Mètodes Algorítmics, Estadística i Bases de Dades), de manera independent." + tasks(1, [
      r"Calcula la probabilitat que un estudiant aprove les tres.", r"Calcula la probabilitat que en suspenga només una.", r"Si un estudiant n'ha suspés només una, quina és la probabilitat que siga Mètodes Algorítmics?"]),
     tasks(1, [r"$0{,}6\cdot0{,}75\cdot0{,}8=" + B(lr3) + "$", r"$0{,}4\cdot0{,}75\cdot0{,}8+0{,}6\cdot0{,}25\cdot0{,}8+0{,}6\cdot0{,}75\cdot0{,}2=0{,}24+0{,}12+0{,}09=" + B(lr1) + "$",
               r"$\frac{0{,}24}{0{,}45}=" + B(lrm / lr1) + "$"])),
 (1, r"\pau{Aragó, ordinària 2024} En una assignatura hi ha 99 persones matriculades (54 dones i 45 homes). En primera convocatòria aproven 49 persones (28 dones i 21 homes)." + tasks(1, [
      r"Quin percentatge de les dones aprova en primera convocatòria? I dels homes?", r"Si triem a l'atzar una persona que ha aprovat, quina és la probabilitat que siga una dona?"]),
     tasks(1, [r"Dones: $\frac{28}{54}\approx\res{51{,}85\,\%}$; \ homes: $\frac{21}{45}\approx\res{46{,}67\,\%}$", r"$\frac{28}{49}=" + B(az[2]) + "$"])),
]))

# =====================================================================
# 4. Experiments compostos i extraccions
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
def alt(b, n, turn=0):
    """probabilitat que guanye el jugador que comença (traure la primera blanca, sense reemplaçament)"""
    if b == 0: return F(0)
    t = b + n
    return (F(b, t) if turn == 0 else 0) + (F(n, t) * alt(b, n - 1, 1 - turn) if n else 0)
ja = [alt(2, 3), F(2, 5) / (1 - F(9, 25))]; ck(ja, [F(3, 5), F(5, 8)])
U = {'R': 5, 'V': 3}; s2r = pu(U, 2, False, lambda s: s[1] == 'R'); ck([s2r, pu(U, 2, False, lambda s: s == ('R', 'R')) / s2r], [F(5, 8), F(4, 7)])
d6 = [F(5, 6)**2 * F(1, 6), F(5, 6)**3]; ck(d6, [F(25, 216), F(125, 216)])
FT = list(permutations(range(1, 21), 2)); pf = lambda f: F(sum(1 for a, b in FT if f(a, b)), len(FT))
cyf = [pf(lambda a, b: a % 3 == 0 and b % 3 == 0), pf(lambda a, b: a % 6 == 0 and b % 3 == 0), pf(lambda a, b: a % 2 and b % 2), pf(lambda a, b: a % 2 and b % 2) / F(10, 20)]
ck(cyf, [F(3, 38), F(3, 76), F(9, 38), F(9, 19)])
ases = [F(4, 40), F(36, 40) * F(4, 39), F(36, 40) * F(35, 39) * F(4, 38)]; ck([ases[2], 1 - ases[0] - ases[1]], [F(21, 247), F(21, 26)])
cv = [F(11, 40) * F(10, 39), F(7, 11)]; ck([float(cv[0]), cv[1]], [0.0705, F(7, 11)], 1e-4)
asw = F(0)
for xa, pa in (('R', F(2, 5)), ('Az', F(3, 5))):
    for xb, pb in (('R', F(3, 5)), ('Az', F(2, 5))):
        Bc = {'R': 3, 'Az': 2}; Bc[xb] -= 1; Bc[xa] += 1; asw += pa * pb * F(Bc['Az'], 5)
asame = F(2, 5) * F(3, 5) + F(3, 5) * F(2, 5); ck([asame, asw], [F(12, 25), F('0.44')])
TT = {1: {1: F(1, 2), 2: F(1, 2)}, 2: {1: F(1, 2), 3: F(1, 2)}, 3: {2: F(1, 2), 3: F(1, 2)}}
def step(d):
    o = {1: F(0), 2: F(0), 3: F(0)}
    for i, p in d.items():
        for j, q in TT[i].items(): o[j] += p * q
    return o
tb = {1: F(1), 2: F(0), 3: F(0)}
for _ in range(3): tb = step(tb)
tc = {1: F(1, 2), 2: F(1, 4), 3: F(1, 4)}
for _ in range(2): tc = step(tc)
ck([tb[1], tc[1], tc[2], tc[3]], [F(3, 8), F(3, 8), F(5, 16), F(5, 16)])
pq = [F('0.04') * F('0.98'), 1 - F('0.04') * F('0.02') * F('0.01')]; ck(pq, [F('0.0392'), F('0.999992')])
S.append(("Experiments compostos. Extraccions amb i sense reemplaçament", [
 (2, r"Una urna conté 2 boles blanques i 3 de negres. L'Anna i en Pau trauen boles alternadament, començant per l'Anna; guanya qui trau la primera bola blanca. Calcula la probabilitat que guanye l'Anna:" + tasks(1, [r"si les boles no es tornen a l'urna;", r"si cada bola es torna a l'urna abans de la tirada següent."])
     + recorda(r"en un diagrama d'arbre multipliquem al llarg de cada camí i sumem els camins que formen el succés."),
     tasks(1, [r"L'Anna guanya en la 1a o en la 3a extracció (en la 5a ja no pot ser, perquè només hi ha 3 negres): $\frac25+\frac35\cdot\frac24\cdot\frac23=\frac25+\frac15=" + B(ja[0]) + "$",
               r"Guanya en la tirada 1, 3, 5\dots: $\frac25\left(1+\frac{9}{25}+\left(\frac{9}{25}\right)^2+\cdots\right)=\dfrac{2/5}{1-9/25}=" + B(ja[1]) + r"$ (sèrie geomètrica de raó $\frac{9}{25}$)"])),
 (1, r"D'una urna amb 5 boles roges i 3 de verdes se'n trauen dues sense reemplaçament. Calcula la probabilitat que la segona siga roja i, sabent que la segona ha sigut roja, la probabilitat que la primera també ho haja sigut.",
     r"$P(R_2)=\frac58\cdot\frac47+\frac38\cdot\frac57=\frac{35}{56}=" + B(s2r) + r"$; \ $P(R_1\cond R_2)=\dfrac{20/56}{35/56}=" + B(F(4, 7)) + "$."),
 (1, r"Llancem un dau fins que isca un 6. Calcula la probabilitat que el primer 6 isca en la tercera tirada i la que calguen més de tres tirades.",
     r"$P(\text{1r 6 en la 3a})=\left(\frac56\right)^2\frac16=" + B(d6[0]) + r"$; \ $P(\text{més de 3})=P(\text{cap 6 en les 3 primeres})=\left(\frac56\right)^3=" + B(d6[1]) + "$."),
 (1, r"\pau{Castella i Lleó, ordinària 2026} D'una bossa amb 20 fitxes numerades de l'1 al 20 se n'extrauen successivament 2 sense reemplaçament. Calcula la probabilitat que:" + tasks(1, [
      r"els dos números siguen múltiples de 3;", r"el primer siga múltiple de 6 i el segon múltiple de 3;", r"cap dels dos siga múltiple de 2;", r"la segona fitxa siga senar, sabent que la primera també ho ha sigut."]),
     tasks(2, [r"$\frac{6}{20}\cdot\frac{5}{19}=" + B(cyf[0]) + "$", r"$\frac{3}{20}\cdot\frac{5}{19}=" + B(cyf[1]) + "$", r"$\frac{10}{20}\cdot\frac{9}{19}=" + B(cyf[2]) + "$", r"$\frac{9}{19}\approx" + dec(cyf[3]) + r"$ \ ($\res{\frac{9}{19}}$)"])),
 (2, r"\pau{Castella-la Manxa, ordinària 2025} D'una baralla espanyola de 40 cartes (amb 4 asos), un jugador va traient cartes una a una fins que troba un as. Després, l'altre jugador ajunta totes les cartes, les barreja i fa el mateix. Guanya qui haja tret més cartes (comptant l'as); si en trauen les mateixes, empaten." + tasks(1, [
      r"Calcula les probabilitats que l'as isca en traure 1, 2 i 3 cartes, respectivament.", r"Si el primer jugador ha tret dues cartes (comptant l'as), quina és la probabilitat que el segon jugador guanye?"]),
     tasks(1, [r"$P(1)=\frac{4}{40}=" + B(ases[0]) + r"$; \ $P(2)=\frac{36}{40}\cdot\frac{4}{39}=" + B(ases[1]) + r"$; \ $P(3)=\frac{36}{40}\cdot\frac{35}{39}\cdot\frac{4}{38}=" + B(ases[2]) + "$",
               r"Ha de traure'n més de 2: $1-\frac1{10}-\frac{6}{65}=" + B(1 - ases[0] - ases[1]) + "$"])),
 (1, r"\pau{Castella-la Manxa, extraordinària 2024} En un mall de 40 cartes, 4 estan marcades només amb un punt verd, 5 només amb un punt roig i 7 amb els dos punts. (Una carta «té punt verd» si en té només un de verd o si en té un de verd i un de roig.)" + tasks(1, [
      r"Quina és la probabilitat de traure dues cartes sense reemplaçament i que totes dues tinguen punt verd?", r"Si traiem una carta i té punt verd, quina és la probabilitat que també tinga punt roig?"]),
     r"Tenen punt verd $4+7=11$ cartes." + tasks(1, [r"$\frac{11}{40}\cdot\frac{10}{39}=\frac{11}{156}\approx\res{" + d4(cv[0]) + "}$", r"$\frac{7}{11}=" + B(cv[1]) + "$"])),
 (2, r"\pau{Aragó, extraordinària 2026} L'urna A té dues boles roges i tres de blaves, i l'urna B, dues de blaves i tres de roges." + tasks(1, [
      r"Si traiem a l'atzar una bola de cada urna, què és més probable, que isquen del mateix color o de color diferent?", r"Les boles extretes en l'apartat anterior es posen en l'urna contrària (la de A en la B i al revés). Si ara traiem una bola de l'urna B, quina és la probabilitat que siga blava?"]),
     tasks(1, [r"$P(\text{mateix color})=\frac25\cdot\frac35+\frac35\cdot\frac25=" + B(asame) + r"<\frac12$: \rest{és més probable que siguen de color diferent} ($0{,}52$).",
               r"Si de A ix blava i de B roja, B queda amb 3 blaves; si ixen del mateix color, B no canvia (2 blaves); si de A ix roja i de B blava, B queda amb 1 blava: $\frac35\cdot\frac35\cdot\frac35+\frac{12}{25}\cdot\frac25+\frac25\cdot\frac25\cdot\frac15=" + B(asw) + "$"])),
 (2, r"\pau{Aragó, ordinària 2025} Una fitxa es mou en un tauler de tres caselles en fila (1, 2, 3). En cada torn es llança una moneda equilibrada: si ix cara s'intenta moure la fitxa a l'esquerra i si ix creu, a la dreta; si no es pot fer el moviment, la fitxa es queda on és." + tasks(1, [
      r"Construeix una taula amb les probabilitats de passar d'una casella a una altra en un torn.", r"Si la fitxa és en la casella 1, quina és la probabilitat que, després de tres torns, torne a estar en la casella 1?",
      r"La fitxa comença en la casella 1 amb probabilitat $\frac12$ i en la 2 i en la 3 amb probabilitat $\frac14$ cadascuna. Quina és la probabilitat que estiga en cada casella després de dos torns?"]),
     tasks(1, [r"Des de l'1: a l'1 o al 2 amb $\frac12$; des del 2: a l'1 o al 3 amb $\frac12$; des del 3: al 2 o al 3 amb $\frac12$.",
               r"Camins 1-1-1-1, 1-1-2-1 i 1-2-1-1, cadascun amb probabilitat $\frac18$: $" + B(tb[1]) + "$",
               r"$P(1)=" + B(tc[1]) + r"$, \ $P(2)=" + B(tc[2]) + r"$, \ $P(3)=" + B(tc[3]) + "$"])),
 (1, r"\pau{Canàries, ordinària 2024} En un avió s'han instal·lat tres paracaigudes $A$, $B$ i $C$: si falla $A$ s'activa $B$, i si també falla $B$ s'activa $C$. Les probabilitats que funcionen correctament són $0{,}96$, $0{,}98$ i $0{,}99$." + tasks(1, [
      r"Dibuixa un diagrama d'arbre amb tots els casos possibles.", r"Calcula la probabilitat que s'active el paracaigudes $B$ i funcione correctament.", r"Calcula la probabilitat que funcione algun paracaigudes."]),
     cen(arbre([('A', F('0.96'), []), (r'\overline{A}', F('0.04'), [('B', F('0.98'), F('0.04') * F('0.98')), (r'\overline{B}\to C', F('0.02'), '')])], s=(2.2, 1.3))) +
     tasks(1, [r"Si falla $B$, s'activa $C$ ($0{,}99$ funciona, $0{,}01$ falla).", r"$0{,}04\cdot0{,}98=" + B(pq[0]) + "$", r"$1-0{,}04\cdot0{,}02\cdot0{,}01=" + B(pq[1]) + "$"])),
]))

# =====================================================================
# 5. Probabilitat total i Bayes
tw = [F('0.02') * F('0.9') / (F('0.02') * F('0.9') + F('0.98') * F('0.05')), F('0.02') * F('0.81') / (F('0.02') * F('0.81') + F('0.98') * F('0.0025'))]
ck([float(v) for v in tw], [0.2687, 0.8686], 1e-4)
an = [F('0.45'), F('0.3'), F('0.25')], [F('0.03'), F('0.04'), F('0.05')]; anT = tot(*an)
anB = [p * c / anT for p, c in zip(*an)]; ck([anT, max(range(3), key=lambda i: anB[i])], [F('0.038'), 0])
asT = tot([F('0.75'), F('0.25')], [F('0.8'), F('0.65')]); ck([asT, F('0.6') / asT], [F('0.7625'), F(48, 61)])
bsT = tot([F('0.4'), F('0.6')], [F('0.3'), F('0.2')]); ck([F('0.8'), F('0.12') / bsT], [F('0.8'), F('0.5')])
tbT = tot([F('0.0005'), F('0.9995')], [F('0.01'), F('0.99')]); tbB = F('0.0005') * F('0.01') / tbT; ck(tbB, F(1, 197902))
cxT = tot([F('0.01'), F('0.99')], [F('0.95'), F('0.02')]); ck([F('0.0095') / cxT, 35000 * F('0.01') * F('0.05')], [F(95, 293), F(35, 2)])
cvT = tot([F(3, 10), F(2, 10), F(5, 10)], [F(1, 3), F(2, 3), F(1, 7)]); ck([cvT, F(5, 10) * F(6, 7) / (1 - cvT)], [F(32, 105), F(45, 73)])
csT = tot([F(50, 120), F(50, 120), F(20, 120)], [F('0.016'), F('0.016'), F('0.009')]); csr = (F(50, 120) * F('0.984')) / (F(20, 120) * F('0.991'))
ck([float(csT), csr > 2], [0.0148, True], 1e-4)
vr = [F('0.48'), F('0.28'), F('0.24')], [F(3, 4), F(1, 2), F(1, 3)]; vrT = tot(*vr)
ck([F('0.24') * F(1, 3), vrT, F('0.48') * F(3, 4) / vrT, F('0.48') * F(3, 4) == F('0.48') * vrT], [F('0.08'), F('0.58'), F(18, 29), False])
rjT = tot([F('0.02'), F('0.98')], [F('0.98'), F('0.04')]); ck([F('0.98') * F('0.04') / rjT, F('0.02') * F('0.02') / (1 - rjT)], [F(2, 3), F(1, 2353)])
mdT = F('0.032') + (1 - F('0.032') / F('0.08')) * F('0.004'); ck([1 - mdT, (mdT - F('0.032')) / mdT], [F('0.9656'), F(3, 43)])
mx = F('0.3') / 6; mF = F('0.1') + F('0.2') + mx
ck([mx, F('0.3') / F('0.8'), mF, F('0.1') / (1 - mF)], [F('0.05'), F('0.375'), F('0.35'), F(2, 13)])
mbB = F('0.4') * F('0.25') * 2 + F('0.2') * F('0.5'); mc_ = F('0.24') / F('0.6'); ck([mbB, mc_, mc_ == F('0.3')], [F('0.3'), F('0.4'), False])
mr = [F(7, 10), F(3, 10), F(2, 5) * F(3, 10) + F(3, 5) * F(4, 10)]; ck([mr[2], F(2, 5) * F(7, 10) / (1 - mr[2])], [F('0.36'), F(7, 16)])
pbN = 1148650; pbA = F('0.1') + F('0.52') * F('0.94') + F('0.38') * F('0.53'); ck([round(float(pbA * pbN)), F('0.52') * F('0.94') / pbA], [907663, F(2444, 3951)])
pa_ = tot([F(3, 12), F(5, 12), F(4, 12)], [F(3, 8), F(2, 8), F(2, 8)]); ck([pa_, F(2, 8), F(5, 12) * F(2, 8) / pa_], [F(9, 32), F('0.25'), F(10, 27)])
sim = {'T1': ((44, 30), (136, 120)), 'T2': ((140, 102), (40, 36))}
ef = {k: v[0][1] + v[1][1] for k, v in sim.items()}; nt = {k: v[0][0] + v[1][0] for k, v in sim.items()}
ck([F(ef['T1'], 288), F(30, 44) < F(102, 140), F(120, 136) < F(36, 40), F(ef['T1'], nt['T1']) > F(ef['T2'], nt['T2'])], [F(25, 48), True, True, True])
tz = [1550, 250, 150]; tw_ = [F('0.74'), F('0.18'), F('0.76')]; tzD = sum(n * w for n, w in zip(tz, tw_))
ck([float(tzD / 1950), F(45, tzD), F(250 - 45, 1950 - tzD)], [0.6697, F(45, 1306), F(205, 644)], 1e-4)
cbT = F(1, 3) * (F(4, 10) + F(1, 6) + F(3, 8)); ck([cbT, F(1, 3) * F(1, 6) / cbT, F(1, 2) * F(4, 10) * F(3, 9)], [F(113, 360), F(20, 113), F(1, 15)])
cpT = F(1, 3) + F(2, 3) * F(2, 5) * F(1, 2); ck([cpT, F(2, 3) * F(2, 5) * F(1, 2) / cpT], [F(7, 15), F(2, 7)])
U2 = {'R': 4, 'A': 2}; cy2 = [pu(U2, 2, False, lambda s: s[0] != s[1]), pu(U2, 2, False, lambda s: s[1] == 'A')]
ck([cy2[0], cy2[1], pu(U2, 2, False, lambda s: s == ('R', 'A')) / cy2[1]], [F(8, 15), F(1, 3), F('0.8')])
S.append(("Probabilitat total i teorema de Bayes", [
 (2, r"Una malaltia afecta el 2\,\% d'una població. Un test dona positiu en el 90\,\% dels malalts i en el 5\,\% dels sans." + tasks(1, [
      r"Si el test d'una persona dona positiu, quina és la probabilitat que estiga malalta?", r"Per a confirmar-ho, es repeteix el test (de manera independent). Si dona positiu les dues vegades, quina és ara la probabilitat que estiga malalta?"])
     + recorda(r"probabilitat total: $P(D)=\sum P(A_i)\,P(D\cond A_i)$. Bayes: $P(A_i\cond D)=\dfrac{P(A_i)\,P(D\cond A_i)}{P(D)}$."),
     tasks(1, [r"$\dfrac{0{,}02\cdot0{,}9}{0{,}02\cdot0{,}9+0{,}98\cdot0{,}05}=\dfrac{0{,}018}{0{,}067}\approx\res{" + d4(tw[0]) + "}$",
               r"$\dfrac{0{,}02\cdot0{,}9^2}{0{,}02\cdot0{,}9^2+0{,}98\cdot0{,}05^2}=\dfrac{0{,}0162}{0{,}01865}\approx\res{" + d4(tw[1]) + "}$: el segon positiu fa molt més fiable el diagnòstic."])),
 (1, r"\pau{Andalusia, extraordinària 2026} Tres màquines, $A$, $B$ i $C$, produeixen el 45\,\%, el 30\,\% i el 25\,\% dels cotxes d'una fàbrica, amb un 3\,\%, un 4\,\% i un 5\,\% de cotxes defectuosos, respectivament." + tasks(1, [
      r"Triem un cotxe a l'atzar. Calcula la probabilitat que siga defectuós.", r"Un cotxe triat a l'atzar resulta defectuós. Quina màquina té la probabilitat més gran d'haver-lo produït?"]),
     tasks(1, [r"$0{,}45\cdot0{,}03+0{,}3\cdot0{,}04+0{,}25\cdot0{,}05=0{,}0135+0{,}012+0{,}0125=" + B(anT) + "$",
               r"$P(A\cond D)=\frac{0{,}0135}{0{,}038}\approx" + dec(anB[0]) + r"$, \ $P(B\cond D)\approx" + dec(anB[1]) + r"$, \ $P(C\cond D)\approx" + dec(anB[2]) + r"$: \rest{la màquina $A$}."])),
 (1, r"\pau{Astúries, extraordinària 2026} Una jugadora de tennis de taula comença els partits restant en el 75\,\% de les ocasions. Quan comença restant guanya el 80\,\% dels partits, i quan comença traent, el 65\,\%." + tasks(1, [
      r"Calcula la probabilitat que guanye un partit.", r"Calcula la probabilitat que haja començat restant en un partit, sabent que l'ha guanyat."]),
     tasks(1, [r"$0{,}75\cdot0{,}8+0{,}25\cdot0{,}65=" + B(asT) + "$", r"$\frac{0{,}6}{0{,}7625}=" + B(F('0.6') / asT) + "$"])),
 (1, r"\pau{Illes Balears, ordinària 2026} En una plataforma de \emph{streaming} de videojocs, el 40\,\% dels usuaris juga principalment a jocs competitius en línia; d'aquests, el 30\,\% participa en tornejos oficials. Entre els que no juguen principalment a jocs competitius, el 20\,\% també participa en tornejos." + tasks(1, [
      r"Si triem un usuari que no juga principalment a jocs competitius, quina és la probabilitat que no participe en tornejos?", r"Si un usuari participa en tornejos, què és més probable, que jugue principalment a jocs competitius o que no?"]),
     tasks(1, [r"$1-0{,}2=" + B(F('0.8')) + "$", r"$P(T)=0{,}12+0{,}12=0{,}24$; $P(C\cond T)=\frac{0{,}12}{0{,}24}=0{,}5=P(\co C\cond T)$: \rest{són igual de probables}."])),
 (2, r"\pau{Illes Balears, ordinària 2025} La probabilitat de tindre tuberculosi és 0,0005. La probabilitat que una prova done positiu si la malaltia és present és del 99\,\%, i la que done negatiu si no és present també és del 99\,\%." + tasks(1, [
      r"Quina és la probabilitat que la prova done positiu si la persona no té la malaltia?", r"Quina és la probabilitat de tindre tuberculosi si el resultat de la prova és negatiu?"]),
     tasks(1, [r"$1-0{,}99=" + B(F('0.01')) + "$", r"$\dfrac{0{,}0005\cdot0{,}01}{0{,}0005\cdot0{,}01+0{,}9995\cdot0{,}99}=\dfrac{1}{197\,902}\approx\res{5{,}05\cdot10^{-6}}$"])),
 (2, r"\pau{Canàries, extraordinària 2025} Una prova detecta una malaltia rara que afecta l'1\,\% de la població adulta. La sensibilitat de la prova (donar positiu si la persona està malalta) és del 95\,\% i l'especificitat (donar negatiu si està sana), del 98\,\%." + tasks(1, [
      r"Calcula la probabilitat que una persona estiga malalta si la prova dona positiu.", r"Si 35\,000 persones es fan la prova, podem afirmar que s'espera que hi haja més de 50 persones malaltes amb resultat negatiu?"]),
     tasks(1, [r"$\dfrac{0{,}01\cdot0{,}95}{0{,}01\cdot0{,}95+0{,}99\cdot0{,}02}=\dfrac{0{,}0095}{0{,}0293}=" + B(F('0.0095') / cxT) + "$",
               r"$P(M\cap\text{neg})=0{,}01\cdot0{,}05=0{,}0005$ i $35\,000\cdot0{,}0005=17{,}5$: \rest{no}, se n'esperen unes 17 o 18."])),
 (1, r"\pau{Canàries, extraordinària 2024} Una malaltia la poden produir tres virus, $A$, $B$ i $C$. En un laboratori hi ha tres tubs amb el virus $A$, dos amb el $B$ i cinc amb el $C$. La probabilitat que el virus $A$ produïsca la malaltia és $\frac13$; la del $B$, $\frac23$, i la del $C$, $\frac17$." + tasks(1, [
      r"Es tria un tub a l'atzar i s'inocula el virus a un animal. Quina és la probabilitat que li produïsca la malaltia?", r"Si no li la produeix, quina és la probabilitat que s'haja injectat el virus $C$?"]),
     tasks(1, [r"$\frac{3}{10}\cdot\frac13+\frac{2}{10}\cdot\frac23+\frac{5}{10}\cdot\frac17=" + B(cvT) + "$", r"$\dfrac{\frac12\cdot\frac67}{1-\frac{32}{105}}=\dfrac{3/7}{73/105}=" + B(F(5, 10) * F(6, 7) / (1 - cvT)) + "$"])),
 (2, r"\pau{Canàries, extraordinària 2026} Un observatori rep 120 sensors: 20 són per al telescopi LST-1 i la resta es reparteixen per igual entre els telescopis MAGIC-I i MAGIC-II. Després del transport, un sensor dels MAGIC s'ha de recalibrar amb probabilitat 0,016 i un del LST-1, amb probabilitat 0,009. Es tria un sensor a l'atzar." + tasks(1, [
      r"Calcula la probabilitat que s'haja de recalibrar.", r"Si el sensor triat no s'ha de recalibrar, és la probabilitat que siga del MAGIC-II més gran que el doble de la probabilitat que siga del LST-1?"]),
     tasks(1, [r"$\frac{100}{120}\cdot0{,}016+\frac{20}{120}\cdot0{,}009=\frac{1{,}78}{120}\approx\res{" + d4(csT) + "}$",
               r"Les dues probabilitats tenen el mateix denominador $P(\co R)$; comparem els numeradors: $\frac{50}{120}\cdot0{,}984=0{,}41$ i $\frac{20}{120}\cdot0{,}991\approx0{,}165$. Com que $0{,}41>2\cdot0{,}165$, \rest{sí}."])),
 (1, r"\pau{Castella i Lleó, ordinària 2024} D'entre els vehicles que revisa un taller, el 48\,\% són cotxes (tres quartes parts requereixen reparació), el 28\,\% motocicletes (la meitat en requereix) i el 24\,\% furgonetes (un terç en requereix). Siguen $C$, $M$, $F$ i $R$ els successos «cotxe», «motocicleta», «furgoneta» i «requereix reparació»." + tasks(1, [
      r"Indica quines probabilitats dona l'enunciat.", r"Calcula $P(R\cap F)$, $P(R)$ i $P(C\cond R)$.", r"Són independents $C$ i $R$?"]),
     tasks(1, [r"$P(C)=0{,}48$, $P(M)=0{,}28$, $P(F)=0{,}24$; $P(R\cond C)=\frac34$, $P(R\cond M)=\frac12$, $P(R\cond F)=\frac13$.",
               r"$P(R\cap F)=0{,}24\cdot\frac13=" + B(F('0.08')) + r"$; \ $P(R)=0{,}36+0{,}14+0{,}08=" + B(vrT) + r"$; \ $P(C\cond R)=\frac{0{,}36}{0{,}58}=" + B(F('0.36') / vrT) + "$",
               r"$P(R\cond C)=0{,}75\neq P(R)=0{,}58$: \rest{no}."])),
 (1, r"\pau{La Rioja, extraordinària 2024} El 2\,\% de la població mundial pateix una malaltia. Una prova per a detectar-la dona positiu en el 98\,\% dels malalts i en el 4\,\% de les persones sanes. Calcula:" + tasks(1, [
      r"la probabilitat que una persona estiga sana, si la prova ha donat positiu;", r"la probabilitat que una persona estiga malalta, si la prova ha donat negatiu."]),
     tasks(1, [r"$\dfrac{0{,}98\cdot0{,}04}{0{,}02\cdot0{,}98+0{,}98\cdot0{,}04}=\dfrac{0{,}0392}{0{,}0588}=" + B(F(2, 3)) + "$", r"$\dfrac{0{,}02\cdot0{,}02}{1-0{,}0588}=\dfrac{0{,}0004}{0{,}9412}=" + B(F(1, 2353)) + "$"])),
 (2, r"\pau{Madrid, extraordinària 2025} La probabilitat que un corredor patisca una caiguda un dia de pluja és 0,08, i un dia sec, 0,004. La probabilitat de ploure i caure és 0,032. Avui un corredor ha eixit a córrer." + tasks(1, [
      r"Calcula la probabilitat que torne a casa sense haver caigut.", r"Calcula la probabilitat que no estiga plovent, sabent que ha caigut."]),
     r"$P(Ll)\cdot0{,}08=0{,}032\Rightarrow P(Ll)=0{,}4$; \ $P(C)=0{,}032+0{,}6\cdot0{,}004=0{,}0344$." + tasks(1, [r"$1-0{,}0344=" + B(1 - mdT) + "$", r"$\frac{0{,}0024}{0{,}0344}=" + B((mdT - F('0.032')) / mdT) + "$"])),
 (3, r"\pau{Madrid, ordinària 2024} En la secció d'idiomes d'una biblioteca hi ha llibres en francés o en anglés de tres categories: el 50\,\% són contes infantils, el 30\,\% novel·les històriques i la resta, manuals tècnics. Un de cada cinc contes està en francés i una de cada tres novel·les, en anglés. A més, un de cada set llibres en francés és un manual tècnic. Es tria un llibre a l'atzar." + tasks(1, [
      r"Calcula la probabilitat que estiga en francés si no és un manual tècnic.", r"Calcula la probabilitat que estiga en francés, i la probabilitat que siga una novel·la històrica si està en anglés."]),
     r"$P(Fr\cap C)=0{,}5\cdot\frac15=0{,}1$, \ $P(Fr\cap N)=0{,}3\cdot\frac23=0{,}2$. Si $x=P(Fr\cap M)$: $x=\frac17(0{,}3+x)\Rightarrow x=0{,}05$." +
     tasks(1, [r"$P(Fr\cond\co M)=\frac{0{,}1+0{,}2}{0{,}8}=" + B(F('0.375')) + "$", r"$P(Fr)=0{,}35$; \ $P(N\cond An)=\frac{0{,}3\cdot\frac13}{0{,}65}=\frac{0{,}1}{0{,}65}=" + B(F(2, 13)) + "$"])),
 (3, r"\pau{Madrid, extraordinària 2024} En un espai mostral hi ha dos successos incompatibles $A_1$ i $A_2$, de probabilitat 0,4 cadascun, i $A_3=\overline{A_1\cup A_2}$ (de probabilitat 0,2). D'un succés $B$ se sap que $P(B\cond A_1)=P(B\cond A_2)$ i $P(B\cond A_3)=2P(B\cond A_1)$; i d'un succés $C$ independent d'$A_1$, que $P(C\cond A_2)=0{,}3$ i $P(C\cond A_3)=0{,}6$." + tasks(1, [
      r"Calcula $P(B)$ si $P(B\cond A_1)=0{,}25$.", r"Calcula $P(C)$ i determina si $C$ és independent d'$A_2$."]),
     tasks(1, [r"$P(B)=0{,}4\cdot0{,}25+0{,}4\cdot0{,}25+0{,}2\cdot0{,}5=" + B(mbB) + "$",
               r"Com que $C$ i $A_1$ són independents, $P(C\cond A_1)=P(C)=c$: \ $c=0{,}4c+0{,}4\cdot0{,}3+0{,}2\cdot0{,}6\Rightarrow0{,}6c=0{,}24\Rightarrow" + B(mc_) + r"$. Com que $P(C\cond A_2)=0{,}3\neq0{,}4$, \rest{no és independent d'$A_2$}."])),
 (1, r"\pau{Múrcia, ordinària 2025} L'urna $U_1$ té 2 boles roges i 3 de verdes, i l'urna $U_2$, 6 de roges i 3 de verdes. Es trau una bola de $U_1$, es posa en $U_2$ i, a continuació, es trau una bola de $U_2$. Calcula la probabilitat que:" + tasks(1, [
      r"isca roja en $U_2$ sabent que ha eixit roja en $U_1$;", r"isca verda en $U_2$ sabent que ha eixit roja en $U_1$;", r"isca verda en $U_2$;", r"haja eixit roja en $U_1$ sabent que ha eixit roja en $U_2$."]),
     cen(arbre([('R_1', F(2, 5), [('R_2', F(7, 10), F(2, 5) * F(7, 10)), ('V_2', F(3, 10), F(2, 5) * F(3, 10))]), ('V_1', F(3, 5), [('R_2', F(6, 10), F(3, 5) * F(6, 10)), ('V_2', F(4, 10), F(3, 5) * F(4, 10))])], s=(2.4, 1.3))) +
     tasks(2, [r"$\frac{7}{10}=" + B(mr[0]) + "$", r"$\frac{3}{10}=" + B(mr[1]) + "$", r"$0{,}12+0{,}24=" + B(mr[2]) + "$", r"$\frac{0{,}28}{0{,}64}=" + B(F(7, 16)) + "$"])),
 (1, r"\pau{País Basc, ordinària 2026} El 2025 es van vendre a Espanya 1\,148\,650 cotxes: el 10\,\% totalment elèctrics (tots de canvi automàtic), el 52\,\% híbrids (el 6\,\% d'ells de canvi manual) i, de la resta, el 53\,\% de canvi automàtic." + tasks(1, [
      r"Calcula la quantitat de cotxes de canvi automàtic venuts el 2025.", r"Triem a l'atzar un cotxe venut el 2025 que té canvi automàtic. Calcula la probabilitat que siga híbrid."]),
     r"$P(Au)=0{,}1+0{,}52\cdot0{,}94+0{,}38\cdot0{,}53=0{,}7902$." + tasks(1, [r"$0{,}7902\cdot1\,148\,650\approx\res{907\,663\text{ cotxes}}$", r"$\frac{0{,}4888}{0{,}7902}=" + B(F('0.52') * F('0.94') / pbA) + "$"])),
 (1, r"\pau{País Basc, ordinària 2024} L'urna A té 3 boles verdes, 5 de roges i 4 de blaves, i l'urna B, 2 de verdes, 2 de roges i 3 de blaves. Es trau a l'atzar una bola d'A, es posa en B i, després, es trau una bola de B." + tasks(1, [
      r"Fes el diagrama d'arbre.", r"Calcula la probabilitat que la bola extreta de B siga verda.", r"Calcula la probabilitat que la bola de B siga verda sabent que la d'A ha sigut roja.", r"Sabent que la bola de B és verda, calcula la probabilitat que la d'A haja sigut roja."]),
     cen(arbre([('V_A', F(3, 12), [('V_B', F(3, 8), '')]), ('R_A', F(5, 12), [('V_B', F(2, 8), '')]), ('B_A', F(4, 12), [('V_B', F(2, 8), '')])], s=(1.7, 1.3))) +
     tasks(2, [r"(Només hi dibuixem les branques de $V_B$.)", r"$\frac{3}{12}\cdot\frac38+\frac{5}{12}\cdot\frac28+\frac{4}{12}\cdot\frac28=" + B(pa_) + "$", r"$\frac28=" + B(F(1, 4)) + "$", r"$\dfrac{\frac{5}{12}\cdot\frac28}{9/32}=" + B(F(10, 27)) + "$"])),
 (2, r"\pau{Aragó, ordinària 2026} En un hospital es fan dues tècniques per a operar una mateixa lesió. Aquestes són les intervencions dels últims anys i, entre parèntesis, les que van ser efectives:" + cen(taula(['\\text{Greus}', '\\text{Lleus}'], ['\\text{Tècnica 1}', '\\text{Tècnica 2}'], [['44\\ (30)', '140\\ (102)', '184'], ['136\\ (120)', '40\\ (36)', '176'], ['180\\ (150)', '180\\ (138)', '360']], str)) + tasks(1, [
      r"Es tria a l'atzar l'expedient d'una intervenció efectiva. Quina de les dues tècniques és més probable que s'haja usat?", r"Un cirurgià vol triar la tècnica amb més probabilitat d'èxit. Quina triarà per a una lesió lleu? I per a una greu?",
      r"Quan no se sap la gravetat de la lesió, el protocol de l'hospital és aplicar la tècnica 1. Justifica per què no és el més adequat."]),
     tasks(1, [r"Hi ha $150+138=288$ intervencions efectives: $P(T_1\cond E)=\frac{150}{288}\approx0{,}52>P(T_2\cond E)=\frac{138}{288}$: \rest{la tècnica 1}.",
               r"Lleu: $\frac{120}{136}\approx0{,}88<\frac{36}{40}=0{,}9$; greu: $\frac{30}{44}\approx0{,}68<\frac{102}{140}\approx0{,}73$: \rest{la tècnica 2 en tots dos casos}.",
               r"En total, $P(E\cond T_1)=\frac{150}{180}\approx0{,}83>P(E\cond T_2)=\frac{138}{180}\approx0{,}77$ només perquè la tècnica 1 s'ha aplicat sobretot a lesions lleus. Però la tècnica 2 és millor tant en les lleus com en les greus: \rest{s'hauria d'aplicar la 2} (paradoxa de Simpson)."])),
 (1, r"\pau{Aragó, extraordinària 2025} La Universitat de Saragossa té tres centres a Terol, amb 1550, 250 i 150 estudiants (Ciències Socials, Politècnica i Infermeria). El 74\,\% dels estudiants de Ciències Socials són dones, el 18\,\% dels de la Politècnica i el 76\,\% dels d'Infermeria." + tasks(1, [
      r"Si es tria un estudiant a l'atzar, quina és la probabilitat que siga dona?", r"Si és dona, quina és la probabilitat que estudie a la Politècnica?", r"Si és home, quina és la probabilitat que estudie a la Politècnica?"]),
     r"Dones: $1147+45+114=1306$ de 1950." + tasks(3, [r"$\frac{1306}{1950}\approx\res{" + d4(F(1306, 1950)) + "}$", r"$\frac{45}{1306}\approx\res{" + d4(F(45, 1306)) + "}$", r"$\frac{205}{644}\approx\res{" + d4(F(205, 644)) + "}$"])),
 (1, r"\pau{Cantàbria, extraordinària 2026} La caixa A té 10 boles, 4 de les quals són blanques; la B en té 6, una de blanca, i la C té 3 blanques de 8. La resta són roges." + tasks(1, [
      r"Calcula la probabilitat que, en traure una bola d'una caixa triada a l'atzar, siga blanca.", r"Si la bola triada és blanca, quina és la probabilitat que siga de la caixa B?", r"Calcula la probabilitat d'obtindre dues boles blanques si es trauen dues boles d'una caixa triada a l'atzar entre la A i la B."]),
     tasks(1, [r"$\frac13\left(\frac4{10}+\frac16+\frac38\right)=" + B(cbT) + "$", r"$\dfrac{\frac13\cdot\frac16}{113/360}=" + B(F(20, 113)) + "$", r"$\frac12\cdot\frac{4}{10}\cdot\frac39+\frac12\cdot0=" + B(F(1, 15)) + "$ (a la B només hi ha una blanca)"])),
 (2, r"\pau{Canàries, ordinària 2025} En una fira, un participant tria una de tres caixes sorpresa: una té premi i les altres dues estan buides. Si tria una caixa buida, trau una bola d'una urna amb 2 boles verdes i 3 de negres: si és negra, acaba sense premi; si és verda, pot triar una nova caixa entre les dues que no havia triat, i acaba." + tasks(1, [
      r"Dibuixa un diagrama d'arbre del joc.", r"Calcula la probabilitat d'obtindre premi.", r"Si el participant ha obtingut premi, quina és la probabilitat que haja tret bola verda?"]),
     cen(arbre([('P', F(1, 3), []), (r'\overline{P}', F(2, 3), [('V\\to P', F(2, 5) * F(1, 2), F(2, 3) * F(1, 5)), ('\\text{no}', 1 - F(2, 5) * F(1, 2), '')])], s=(2.2, 1.3))) +
     tasks(1, [r"Després de la verda, encerta la caixa amb probabilitat $\frac12$: la branca $V\to P$ té $\frac25\cdot\frac12=\frac15$.", r"$\frac13+\frac23\cdot\frac15=" + B(cpT) + "$", r"$\dfrac{2/15}{7/15}=" + B(F(2, 7)) + "$"])),
 (1, r"\pau{Castella i Lleó, ordinària 2025} D'una urna amb quatre boles roges i dues de blaves se'n trau una i, sense tornar-la, se'n trau una altra." + tasks(1, [
      r"Calcula la probabilitat que siguen de color diferent.", r"Calcula la probabilitat que la segona bola siga blava.", r"Si la segona bola és blava, calcula la probabilitat que la primera siga roja."]),
     tasks(3, [r"$2\cdot\frac46\cdot\frac25=" + B(cy2[0]) + "$", r"$\frac46\cdot\frac25+\frac26\cdot\frac15=" + B(cy2[1]) + "$", r"$\dfrac{8/30}{1/3}=" + B(F('0.8')) + "$"])),
]))

# =====================================================================
# 6. Variables aleatòries i binomial
va = [F('0.1'), F('0.2'), F('0.4'), F('0.3')]; vm = sum(k * p for k, p in enumerate(va)); vv = sum(k * k * p for k, p in enumerate(va)) - vm**2
ck([vm, vv], [F('1.9'), F('0.89')])
gw = F(3, 5) * F(2, 4); ck([gw, 2 * gw - (1 - gw), 1 / gw], [F(3, 10), F(-1, 10), F(10, 3)])
b6 = [pmf(6, F(1, 3), 2), cdf(6, F(1, 3), 0, 1), cdf(6, F(1, 3), 2, 6)]; ck([b6[0], b6[1], b6[1] + b6[2]], [F(80, 243), F(256, 729), 1])
ck(5 * F(1, 3) * F(2, 3)**4, 10 * F(1, 3)**2 * F(2, 3)**3)
nm = ceil(log(0.5) / log(0.98)); ck([nm, 1 - 0.98**(nm - 1) < 0.5 < 1 - 0.98**nm], [35, True])
ar15 = [pmf(15, F('0.16'), 2), cdf(15, F('0.16'), 0, 1), cdf(15, F('0.16'), 3, 15)]; ck([float(ar15[0]), ar15[2] > ar15[1]], [0.27865, True], 1e-5)
cr = [pmf(8, F('0.05'), 3), pmf(8, F('0.05'), 0), 1 - cdf(8, F('0.95'), 0, 1)]; ck([float(cr[0]), float(cr[1]), float(cr[2])], [0.0054, 0.6634, 1], 1e-4)
gf = [pmf(5, F('0.4'), 0), cdf(5, F('0.4'), 0, 2), 5 * F('0.4')]; ck(gf, [F('0.07776'), F('0.68256'), 2])
lu = [10 * F(1, 2), sqrt(10 * 0.25), cdf(10, F(1, 2), 0, 3)]; ck([lu[0], lu[1], float(lu[2])], [5, 1.58, 0.17], 5e-3)
gi = 1 - cdf(7, F('0.13'), 0, 1); ck(float(gi), 0.2281, 1e-4)
mb = pmf(9, F('0.05'), 3); ck(float(mb), 0.0077, 1e-4)
mp = [10 * F('0.98'), sqrt(10 * 0.98 * 0.02), pmf(10, F('0.02'), 1)]; ck([float(mp[2])], [0.16667], 1e-4)
nv = [pmf(10, F(1, 4), 0), pmf(10, F(1, 4), 7), cdf(10, F(1, 4), 7, 10)]; ck([float(v) for v in nv], [0.0563, 0.0031, 0.0035], 1e-4)
sf = [1 - F('0.3')**5, cdf(15, F('0.9'), 14, 15)]; ck([float(v) for v in sf], [0.99757, 0.549], 1e-3)
ae = [F('0.9')**10, 1 - F('0.1')**10 - 10 * F('0.9') * F('0.1')**9]; ck([float(v) for v in ae], [0.3487, 0.9999999909], 1e-4)
tq = [F(1, 5)**4, cdf(4, F(1, 5), 0, 2)]; ck(tq, [F(1, 625), F(608, 625)])
exr = [cdf(10, F('0.3'), 9, 10), 1 - F('0.7')**10, F('0.3') + F('0.35') - (1 - F('0.4'))]; ck([float(exr[0]), float(exr[1]), exr[2]], [0.00014, 0.9718, F('0.05')], 1e-4)
S.append(("Variables aleatòries discretes i distribució binomial", [
 (1, r"Una variable aleatòria $X$ pren els valors 0, 1, 2 i 3 amb probabilitats $0{,}1$, $a$, $2a$ i $0{,}3$. Calcula $a$, la mitjana i la desviació típica de $X$, i $P(X\geq2)$."
     + recorda(r"$\sum p_i=1$; \ $\mu=\sum x_ip_i$; \ $\sigma^2=\sum x_i^2p_i-\mu^2$."),
     r"$0{,}1+3a+0{,}3=1\Rightarrow\res{a=0{,}2}$. \ $\mu=0{,}2+0{,}8+0{,}9=" + B(vm) + r"$; \ $\sigma^2=0{,}2+1{,}6+2{,}7-1{,}9^2=0{,}89\Rightarrow\sigma\approx\res{" + d4(sqrt(float(vv))) + r"}$; \ $P(X\geq2)=" + B(F('0.7')) + "$."),
 (2, r"Un joc consisteix a pagar 1 € i traure dues boles, sense reemplaçament, d'una urna amb 3 boles blanques i 2 de negres. Si les dues són blanques es cobren 3 €. Calcula el guany esperat del jugador. Quant hauria de pagar-se per dues blanques perquè el joc fóra equitatiu?",
     r"$P(BB)=\frac35\cdot\frac24=\frac{3}{10}$. El guany net és $2$ € (prob. $0{,}3$) o $-1$ € (prob. $0{,}7$): $E=0{,}6-0{,}7=\res{-0{,}10\text{ €}}$ (perd 10 cèntims per partida). Equitatiu si $0{,}3\,x=1$: $\res{x=\frac{10}{3}\approx3{,}33\text{ €}}$."),
 (1, r"Raona si les variables següents són binomials i, si ho són, indica'n els paràmetres:" + tasks(1, [r"nombre de cinquets en 12 llançaments d'un dau;", r"nombre de boles roges en traure 3 boles sense reemplaçament d'una urna amb 4 roges i 6 blanques;",
      r"nombre de llançaments d'una moneda fins que ix la primera cara;", r"nombre de peces defectuoses en una mostra de 50 d'una producció enorme amb un 2\,\% de defectuoses."]),
     tasks(1, [r"\rest{Sí}: $B\left(12,\frac16\right)$.", r"\rest{No}: la probabilitat canvia d'una extracció a una altra (no són independents).", r"\rest{No}: el nombre de proves no està fixat.", r"\rest{Sí} (població molt gran): $B(50;\ 0{,}02)$."])),
 (1, r"Si $X\sim B\left(6,\frac13\right)$, calcula $P(X=2)$, $P(X\leq1)$, $P(X\geq2)$, la mitjana i la desviació típica."
     + recorda(r"$P(X=k)=\binom nk p^k q^{n-k}$, \ $\mu=np$, \ $\sigma=\sqrt{npq}$. Per a «almenys», sovint és més curt el contrari."),
     r"$P(X=2)=" + bt(6, F(1, 3), 2) + "=" + B(b6[0]) + r"$; \ $P(X\leq1)=\left(\frac23\right)^6+6\cdot\frac13\left(\frac23\right)^5=" + B(b6[1]) + r"$; \ $P(X\geq2)=1-P(X\leq1)=" + B(b6[2]) + r"$; \ $\mu=" + B(2) + r"$, \ $\sigma=\sqrt{6\cdot\frac13\cdot\frac23}=" + r"\res{\frac{2}{\sqrt3}\approx1{,}1547}$."),
 (2, r"Una variable $X\sim B(5,p)$ compleix $P(X=1)=P(X=2)$. Calcula $p$ i $P(X\geq1)$.",
     r"$5pq^4=10p^2q^3\Rightarrow q=2p\Rightarrow1-p=2p\Rightarrow\res{p=\frac13}$ ($p=0$ no té sentit). \ $P(X\geq1)=1-\left(\frac23\right)^5=" + B(1 - F(2, 3)**5) + "$."),
 (2, r"Una màquina fa un 2\,\% de peces defectuoses. Quantes peces cal revisar, com a mínim, perquè la probabilitat de trobar-ne almenys una de defectuosa supere 0,5?",
     r"$1-0{,}98^n>0{,}5\iff0{,}98^n<0{,}5\iff n>\dfrac{\ln0{,}5}{\ln0{,}98}\approx" + dec(log(0.5) / log(0.98), 2) + r"$ (en dividir per $\ln0{,}98<0$ la desigualtat gira): \ $\res{n=35}$ peces."),
 (1, r"\pau{Aragó, extraordinària 2024} El 84\,\% dels exàmens de Matemàtiques II de la convocatòria ordinària de 2022 a Aragó van traure una nota igual o superior a 5." + tasks(1, [
      r"Si se seleccionen 15 d'aquests exàmens a l'atzar, quina és la probabilitat que exactament 2 tinguen una nota inferior a 5?", r"Amb els 15 exàmens, és més probable que menys de 2 tinguen nota inferior a 5 o que més de 2 la tinguen?"]),
     r"$X=$ «nombre d'exàmens amb nota inferior a 5» $\sim B(15;\ 0{,}16)$." + tasks(1, [r"$\binom{15}{2}0{,}16^2\,0{,}84^{13}\approx" + r"\res{" + dec(ar15[0], 5) + "}$",
      r"$P(X<2)=0{,}84^{15}+15\cdot0{,}16\cdot0{,}84^{14}\approx" + d4(ar15[1]) + r"$ i $P(X>2)=1-P(X\leq2)\approx" + d4(ar15[2]) + r"$: \rest{és més probable que més de 2}."])),
 (1, r"\pau{Castella-la Manxa, extraordinària 2025} Una inspectora de sanitat sap que el 5\,\% dels restaurants no passarà una inspecció. Si en tria 8 a l'atzar, calcula la probabilitat que:" + tasks(1, [
      r"tres restaurants no passen la inspecció;", r"tots els restaurants passen la inspecció;", r"almenys dos restaurants passen la inspecció."]),
     r"$X=$ «nombre que no la passen» $\sim B(8;\ 0{,}05)$." + tasks(1, [r"$\binom83\,0{,}05^3\,0{,}95^5\approx\res{" + d4(cr[0]) + "}$", r"$0{,}95^8\approx\res{" + d4(cr[1]) + "}$",
      r"Ho passen almenys 2 si $X\leq6$: $1-P(X=7)-P(X=8)=1-8\cdot0{,}05^7\cdot0{,}95-0{,}05^8\approx\res{1}$ ($0{,}99999999$)"])),
 (1, r"\pau{Extremadura, extraordinària 2024} La probabilitat que un jugador de golf faça forat des de certa distància és 0,4. Si fa 5 llançaments, calcula:" + tasks(1, [r"la probabilitat que no faça cap forat;", r"la probabilitat de fer com a molt 2 forats;", r"el nombre mitjà de forats."]),
     r"$X\sim B(5;\ 0{,}4)$." + tasks(3, [r"$0{,}6^5=" + B(gf[0]) + "$", r"$0{,}07776+0{,}2592+0{,}3456=" + B(gf[1]) + "$", r"$\mu=5\cdot0{,}4=\res{2}$"])),
 (1, r"\pau{Extremadura, ordinària 2024} La tutora d'en Lluís li proposa un tracte: si en els pròxims 10 dies arriba tard com a molt 3 dies, li pujarà 1 punt la nota. La probabilitat que arribe tard cada dia és 0,5." + tasks(1, [
      r"Quina distribució segueix el nombre de dies que arriba tard? Quins en són els paràmetres?", r"Quina és la mitjana i la desviació típica?", r"Quina és la probabilitat que en Lluís aconseguisca el punt?"]),
     tasks(1, [r"$\res{X\sim B(10;\ 0{,}5)}$", r"$\mu=" + B(5) + r"$ dies; \ $\sigma=\sqrt{2{,}5}\approx\res{1{,}58}$ dies", r"$P(X\leq3)=\frac{1+10+45+120}{1024}=\frac{176}{1024}\approx\res{" + d4(lu[2]) + "}$"])),
 (1, r"\pau{Galícia, extraordinària 2024} En una colònia de corbs marins, cada ou té un 13\,\% de probabilitat de ser infèrtil. Si s'observa una posta de 7 ous, calcula la probabilitat que n'hi haja almenys 2 d'infèrtils.",
     r"$X\sim B(7;\ 0{,}13)$: \ $P(X\geq2)=1-0{,}87^7-7\cdot0{,}13\cdot0{,}87^6\approx\res{" + d4(gi) + "}$."),
 (1, r"\pau{Múrcia, ordinària 2026} Una fàbrica de bombetes sap que el 5\,\% són defectuoses. Calcula la probabilitat que en 9 bombetes triades a l'atzar n'hi haja exactament 3 de defectuoses.",
     r"$X\sim B(9;\ 0{,}05)$: \ $\binom93\,0{,}05^3\,0{,}95^6\approx\res{" + d4(mb) + "}$."),
 (1, r"\pau{Múrcia, ordinària 2025} El 2\,\% de les peces que fa una màquina són defectuoses. Considera el nombre de peces en bon estat d'un lot de 10 peces. Quina distribució segueix? Indica'n la mitjana i la desviació típica i calcula la probabilitat que hi haja exactament una peça defectuosa.",
     r"$\res{Y\sim B(10;\ 0{,}98)}$, \ $\mu=" + B(F('9.8')) + r"$, \ $\sigma=\sqrt{10\cdot0{,}98\cdot0{,}02}\approx\res{" + d4(mp[1]) + r"}$. \ Una defectuosa és $Y=9$: $\binom{10}{9}0{,}98^9\,0{,}02\approx\res{" + d4(mp[2]) + "}$."),
 (1, r"\pau{Navarra, ordinària 2026} En un examen tipus test de 10 preguntes, cada pregunta té 4 respostes de les quals només una és correcta. Si es respon a l'atzar:" + tasks(1, [
      r"Quina és la probabilitat de fallar-les totes?", r"Quina és la probabilitat d'encertar-ne exactament 7?", r"Per a aprovar cal respondre bé almenys 7 preguntes. Quina és la probabilitat d'aprovar?"]),
     r"$X\sim B(10;\ 0{,}25)$." + tasks(3, [r"$0{,}75^{10}\approx\res{" + d4(nv[0]) + "}$", r"$\binom{10}{7}0{,}25^7\,0{,}75^3\approx\res{" + d4(nv[1]) + "}$", r"$P(X\geq7)\approx\res{" + d4(nv[2]) + "}$"])),
 (1, r"\pau{Canàries, extraordinària 2026} Una acadèmia de surf garanteix que, després del curs, un surfista principiant agafa una ona amb una probabilitat del 70\,\%." + tasks(1, [
      r"Si un alumne intenta agafar 5 ones, quina és la probabilitat que n'agafe alguna?", r"Per a contractar un monitor s'avalua un surfista experimentat que agafa una ona amb una probabilitat del 90\,\%. El contracten si n'agafa almenys 14 de 15. Quina és la probabilitat que el contracten?"]),
     tasks(1, [r"$1-0{,}3^5=" + B(sf[0]) + "$", r"$X\sim B(15;\ 0{,}9)$: \ $0{,}9^{15}+15\cdot0{,}9^{14}\cdot0{,}1\approx\res{" + d4(sf[1]) + "}$"])),
 (1, r"\pau{Catalunya, setembre 2026} Un parc eòlic té 10 aerogeneradors de 100 MW cadascun. Cada aerogenerador té una probabilitat del 10\,\% d'estar parat, independentment dels altres." + tasks(1, [
      r"Quina és la probabilitat d'arribar als 1000 MW de potència total?", r"Quina és la probabilitat que la potència total supere els 150 MW?"]),
     r"$X=$ «aerogeneradors en marxa» $\sim B(10;\ 0{,}9)$." + tasks(1, [r"Tots en marxa: $0{,}9^{10}\approx\res{" + d4(ae[0]) + "}$",
      r"Almenys 2 en marxa: $1-0{,}1^{10}-10\cdot0{,}9\cdot0{,}1^{9}=\res{0{,}9999999909}$"])),
 (2, r"\pau{Aragó, ordinària 2026} Un test té 4 preguntes amb 5 respostes possibles cadascuna. Cada resposta correcta suma 2,5 punts i cada resposta incorrecta en resta 0,625. Es contesten les quatre preguntes a l'atzar." + tasks(1, [
      r"Quina és la probabilitat de traure un excel·lent (nota igual o superior a 9)?", r"Quina és la probabilitat de suspendre (nota inferior a 5)?"]),
     r"Amb $k$ encerts, la nota és $2{,}5k-0{,}625(4-k)$: val $10$, $6{,}875$, $3{,}75$\dots\ per a $k=4,3,2\dots$ i $X\sim B\left(4;\ \frac15\right)$." + tasks(1, [
      r"Cal encertar-les totes: $\left(\frac15\right)^4=" + B(tq[0]) + "$", r"Cal $X\leq2$: $1-P(X=3)-P(X=4)=1-\frac{16}{625}-\frac{1}{625}=" + B(tq[1]) + "$"])),
 (1, r"\pau{Extremadura, extraordinària 2025} El 30\,\% de la població d'una comarca veu el programa de televisió «La Revuelta». La productora telefona a l'atzar a 10 persones de la comarca." + tasks(1, [
      r"Calcula la probabilitat que més de 8 persones estigueren veient el programa.", r"Calcula la probabilitat que alguna de les 10 persones estiguera veient el programa.",
      r"Se sap que el 35\,\% de la població veu «El Hormiguero» i que el 40\,\% no veu cap dels dos programes. Quina és la probabilitat que una persona veja els dos programes?"]),
     tasks(1, [r"$X\sim B(10;\ 0{,}3)$: \ $P(X=9)+P(X=10)=10\cdot0{,}3^9\cdot0{,}7+0{,}3^{10}\approx\res{0{,}00014}$", r"$1-0{,}7^{10}\approx\res{" + d4(exr[1]) + "}$", r"$0{,}3+0{,}35-0{,}6=" + B(exr[2]) + "$"])),
]))

# =====================================================================
# 7. Problemes de síntesi
mon5 = [pmf(5, F(1, 2), 4), pmf(5, F('0.8'), 4)]; mT = mon5[1] / (mon5[0] + mon5[1]); ck(float(mT), 0.7239, 1e-4)
cm8 = [tot([F(1, 2), F(1, 3), F(1, 6)], [F(3, 5), F(2, 5), F(1, 5)]), pmf(5, F('0.25'), 2), 1 - F('0.75')**5]
ck([cm8[0], F(1, 3) * F(2, 5) / cm8[0]], [F(7, 15), F(2, 7)]); ck([float(cm8[1]), float(cm8[2])], [0.2637, 0.7627], 1e-4)
md4 = [F('0.7') * F(4, 7), F('0.7') * F(3, 7) + F('0.3') * F(1, 3)]; md4b = cdf(10, md4[1], 0, 2)
ck([md4[0], md4[1]], [F('0.4'), F('0.4')]); ck(float(md4b), 0.1673, 1e-4)
asr = [1 - F('0.94')**10, F('0.06') * F('0.05') + F('0.94') * F('0.96')]; ck([float(asr[0]), asr[1]], [0.4614, F('0.9054')], 1e-4)
ctS = [1 - F('0.8')**4, F('0.2') * F('0.95') + F('0.8') * F('0.005')]; ctS.append(F('0.2') * F('0.05') / (1 - ctS[1])); ck([float(ctS[0]), ctS[1], float(ctS[2])], [0.5904, F('0.194'), 0.0124], 1e-4)
cj = F('0.6') * F('0.05') + F('0.4') * F('0.03'); ck(cj, F('0.042'))
EA, EB, EC, ED = [0, 0, 4, 4, 4, 4], [3] * 6, [2, 2, 2, 2, 6, 6], [1, 1, 1, 5, 5, 5]
ef_a = F(sum(1 for a, b in product(EA, EB) if a > b), 36); ef_b = cdf(8, 1 - ef_a, 3, 8); ef_c = F(sum(1 for a, c in product(EA, EC) if c > a), 36)
ef_d = F(sum(1 for v in product(EA, EB, EC, ED) if min(v) < v[0] < max(v)), 6**4)
ck([ef_a, ef_c, ef_d], [F(2, 3), F(5, 9), F(4, 9)]); ck(float(ef_b), 0.5318, 1e-4)
S.append(("Problemes de síntesi", [
 (2, r"Una bossa conté dues monedes: una d'equilibrada i una de trucada, amb probabilitat de cara 0,8. Se'n tria una a l'atzar i es llança 5 vegades. Si han eixit exactament 4 cares, quina és la probabilitat que siga la moneda trucada?",
     r"Per a cada moneda, el nombre de cares és binomial: $P(4\cond E)=\binom54\left(\frac12\right)^5=\frac{5}{32}$ i $P(4\cond T)=\binom54\,0{,}8^4\cdot0{,}2=0{,}4096$. \ Bayes: $P(T\cond4)=\dfrac{\frac12\cdot0{,}4096}{\frac12\cdot\frac{5}{32}+\frac12\cdot0{,}4096}\approx\res{" + d4(mT) + "}$."),
 (1, r"\pau{Castella-la Manxa, extraordinària 2024} Tenim tres caixes: la A té dues cartes d'espases i tres de copes; la B, tres d'espases i dues de copes; i la C, quatre d'espases i una de copes. Es llança un dau: si ix senar es trau una carta de la caixa A; si ix 4 o 6, de la B; i si ix 2, de la C." + tasks(1, [
      r"Calcula la probabilitat d'obtindre una carta de copes.", r"Sabent que la carta és de copes, quina és la probabilitat que siga de la caixa B?",
      r"La probabilitat que un paracaigudista novell caiga en el punt correcte és 0,25. Si es llança 5 vegades, quina és la probabilitat que caiga en el punt correcte exactament dues vegades? I almenys una vegada?"]),
     tasks(1, [r"$\frac12\cdot\frac35+\frac13\cdot\frac25+\frac16\cdot\frac15=" + B(cm8[0]) + "$", r"$\dfrac{2/15}{7/15}=" + B(F(2, 7)) + "$",
               r"$X\sim B(5;\ 0{,}25)$: \ $\binom52\,0{,}25^2\,0{,}75^3\approx\res{" + d4(cm8[1]) + r"}$; \ $1-0{,}75^5\approx\res{" + d4(cm8[2]) + "}$"])),
 (2, r"\pau{Madrid, ordinària 2025 (coincidències)} En una empresa tecnològica, el 70\,\% dels empleats són europeus. Una tercera part dels no europeus es dedica a desenvolupar programari, i també tres de cada set dels europeus." + tasks(1, [
      r"En un sorteig entre els empleats, calcula la probabilitat que el premiat siga europeu i no desenvolupe programari.", r"En un segon sorteig es trien a l'atzar 10 empleats, que rebran un premi si com a molt 2 d'ells desenvolupen programari. Calcula la probabilitat que l'empresa haja de donar aquest segon premi."]),
     tasks(1, [r"$0{,}7\cdot\frac47=" + B(md4[0]) + "$", r"$P(\text{desenvolupa})=0{,}7\cdot\frac37+0{,}3\cdot\frac13=0{,}4$ i $X\sim B(10;\ 0{,}4)$: \ $P(X\leq2)=0{,}6^{10}+10\cdot0{,}4\cdot0{,}6^9+45\cdot0{,}4^2\cdot0{,}6^8\approx\res{" + d4(md4b) + "}$"])),
 (1, r"\pau{Astúries, ordinària 2025} El 6\,\% de les peces que fabrica una empresa són defectuoses. En el control de qualitat, un sistema de prova dona error amb probabilitat 0,95 si la peça és defectuosa i 0,04 si no ho és." + tasks(1, [
      r"Si es trien 10 peces a l'atzar, quina és la probabilitat que almenys una siga defectuosa?", r"Calcula la probabilitat que, en provar una peça triada a l'atzar, el sistema no done error."]),
     tasks(1, [r"$X\sim B(10;\ 0{,}06)$: \ $1-0{,}94^{10}\approx\res{" + d4(asr[0]) + "}$", r"$0{,}06\cdot0{,}05+0{,}94\cdot0{,}96=" + B(asr[1]) + "$"])),
 (2, r"\pau{Catalunya, setembre 2024} S'estima que el 20\,\% dels habitants d'una regió pateix arrítmia. Un monitor Holter la detecta en el 95\,\% dels casos de persones que la pateixen, però també dona falsos positius en el 0,5\,\% de les persones que no en pateixen." + tasks(1, [
      r"Si es trien 4 persones a l'atzar, quina és la probabilitat que almenys una patisca arrítmia?", r"Quina és la probabilitat que una persona triada a l'atzar obtinga un diagnòstic positiu?", r"Si una persona obté un diagnòstic negatiu, quina és la probabilitat que realment patisca arrítmia?"]),
     tasks(1, [r"$1-0{,}8^4=" + B(ctS[0]) + "$", r"$0{,}2\cdot0{,}95+0{,}8\cdot0{,}005=" + B(ctS[1]) + "$", r"$\frac{0{,}2\cdot0{,}05}{1-0{,}194}=\frac{0{,}01}{0{,}806}\approx\res{" + d4(ctS[2]) + "}$"])),
 (2, r"\pau{Catalunya, juny 2025} Una empresa produeix peces de ferro (el 60\,\%) i d'acer (la resta). El 95\,\% de les de ferro no té cap defecte, mentre que el 3\,\% de les d'acer és defectuosa." + tasks(1, [
      r"Si prenem una peça a l'atzar, quina és la probabilitat que siga defectuosa?", r"L'empresa produirà també peces de titani, que es vendran en paquets de 5. Cada peça de titani és defectuosa amb una probabilitat $p$, independentment de les altres. Comprova que la probabilitat que en un paquet hi haja exactament 4 peces defectuoses és $f(p)=5p^4-5p^5$."]),
     tasks(1, [r"$0{,}6\cdot0{,}05+0{,}4\cdot0{,}03=" + B(cj) + "$", r"$X\sim B(5,p)$: $P(X=4)=\binom54p^4(1-p)=5p^4-5p^5$. \rest{\checkmark}"])),
 (2, r"\pau{Múrcia, ordinària 2024} El joc dels daus d'Efron té 4 daus equilibrats de 6 cares, numerats així: dau A: 0, 0, 4, 4, 4, 4; dau B: 3, 3, 3, 3, 3, 3; dau C: 2, 2, 2, 2, 6, 6; dau D: 1, 1, 1, 5, 5, 5. L'Anna tria el dau A, la Bea el B, la Ceci el C i la Dèlia el D. Cada jugadora llança el seu dau: guanya qui trau la puntuació més alta i perd qui trau la més baixa." + tasks(1, [
      r"Si l'Anna juga contra la Bea, quina és la probabilitat que guanye l'Anna?", r"Si l'Anna juga 8 vegades contra la Bea, quina és la probabilitat que la Bea guanye almenys 3 vegades?",
      r"Si l'Anna juga contra la Ceci, quina és la probabilitat que guanye la Ceci?", r"Si juguen totes contra totes, quina és la probabilitat que l'Anna ni guanye ni perda?"]),
     tasks(1, [r"L'Anna guanya si trau 4: $" + B(ef_a) + "$", r"$X\sim B\left(8,\frac13\right)$: \ $P(X\geq3)=1-P(X\leq2)\approx\res{" + d4(ef_b) + "}$",
               r"La Ceci guanya si trau 6, o si trau 2 i l'Anna 0: $\frac13+\frac23\cdot\frac13=" + B(ef_c) + "$",
               r"Si l'Anna trau 0 perd segur; si trau 4, ha de no ser la més alta (C o D superen el 4: $1-\frac23\cdot\frac12=\frac23$): $\frac23\cdot\frac23=" + B(ef_d) + "$"])),
]))

# ---------- comprovacions ----------
for l, r, tol in CHK:
    if tol is None: assert l == r, (l, r)
    else:
        for x, y in (zip(l, r) if isinstance(l, list) else [(l, r)]): assert abs(x - y) < tol, (x, y)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={probabilitat, successos, regla de Laplace, combinatòria, probabilitat condicionada, independència, probabilitat total, teorema de Bayes, variable aleatòria, distribució binomial, PAU}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques II}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += '\n\\setlength{\\emergencystretch}{3em}\n'
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
% successos contraris i probabilitat condicionada
\newcommand{\co}[1]{\overline{#1}}
\newcommand{\cond}{\,|\,}
'''

TIT = "Probabilitat"
def build(sol):
    tt = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 10: %s. 2n de Batxillerat MII}" % (tt, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 10: %s · 2n Batxillerat MII" % (tt, TIT))
    assert 'MII}' in p and '2n Batxillerat MII' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques II}{2n Batx}{''' + ('Solucions de la fitxa · Unitat 10' if sol else "Fitxa d'exercicis · Unitat 10") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Les probabilitats s'han calculat de manera exacta; quan el resultat no és un decimal exacte, es dona la fracció i el valor aproximat amb quatre decimals. Pots comprovar els exercicis de dos successos amb la calculadora dels apunts interactius, i els de la binomial amb el giny de la distribució binomial."
             if sol else r"Resol els exercicis al quadern justificant cada pas. Defineix sempre els successos amb lletres i escriu les dades amb la notació de probabilitats ($P(A)$, $P(A\cap B)$, $P(A\,|\,B)$\dots); fes un diagrama de Venn, una taula de contingència o un diagrama d'arbre quan t'ajude. Els " + str(NPAU) + r" exercicis marcats amb {\color{teal}\bfseries\faUniversity\ PAU} són de les proves d'accés a la universitat (Matemàtiques II) de " + str(len(REGS)) + r" comunitats autònomes, traduïts al valencià; els de la PAU valenciana els tens a la pàgina d'exercicis tipus PAU de la unitat.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, qq, s in exs:
            n += 1
            if sol:
                head = re.sub(r'(\\pau\{[^}]*\}).*', r'\1', qq, flags=re.S) if qq.startswith('\\pau{') else ''
                out.append('\\ex{%d} %s%s\n\n' % (st, head, s))
            else:
                out.append('\\ex{%d} %s\n\n' % (st, qq))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't10-fitxa-solucions.tex' if sol else 't10-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

NPAU = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
REGS = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
n = build(False); build(True)
print(n, 'exercicis,', NPAU, 'de la PAU de', len(REGS), 'comunitats:', ', '.join(REGS), '·', len(CHK), 'comprovacions')
