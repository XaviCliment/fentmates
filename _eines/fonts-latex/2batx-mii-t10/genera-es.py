# Versió en castellà de genera.py. Genera t10-fitxa-exercicis.tex i t10-fitxa-solucions.tex (2n Batxillerat Matemàtiques II, Unitat 10: Probabilitat)
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
    """valor exacto: decimal si es exacto, fracción y aproximación si no"""
    x = F(x)
    if p10(x.denominator) and x.denominator <= 10**6: return dec(x, 6)
    return r'\frac{%d}{%d}\approx %s' % (x.numerator, x.denominator, dec(x))
def Q(x):
    """solo la fracción (o el decimal exacto)"""
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
    """término de la binomial en TeX"""
    return r'\binom{%d}{%d}%s^{%d}\,%s^{%d}' % (n, k, Q(p), k, Q(1 - F(p)), n - k)

# ---------- figures ----------
def venn(v1, v2, v3, v0, la='A', lb='B'):
    """diagrama de Venn con la probabilidad de cada región: solo A, A∩B, solo B, ninguno"""
    return (r'\begin{tikzpicture}[scale=.62,baseline=(current bounding box.center)]'
            r'\draw[muted,rounded corners=3pt] (-2.9,-1.75) rectangle (2.9,1.75);'
            r'\fill[accent!12] (-0.65,0) circle (1.35); \fill[teal!14] (0.65,0) circle (1.35);'
            r'\draw[navy,thick] (-0.65,0) circle (1.35); \draw[navy,thick] (0.65,0) circle (1.35);'
            r'\node[font=\small\bfseries] at (-1.75,1.25) {$%s$}; \node[font=\small\bfseries] at (1.75,1.25) {$%s$};'
            r'\node[font=\scriptsize] at (-1.25,0) {$%s$}; \node[font=\scriptsize] at (0,0) {$%s$}; \node[font=\scriptsize] at (1.25,0) {$%s$};'
            r'\node[font=\scriptsize] at (2.25,-1.45) {$%s$};\end{tikzpicture}') % (la, lb, Q(v1), Q(v2), Q(v3), Q(v0))
def taula(rl, cl, M, fmt=Q):
    """tabla de contingencia: rl, cl etiquetas (sin el total); M matriz de valores con los totales"""
    cols = 'l|' + 'c' * len(cl) + '|c'
    o = [r'{\small\renewcommand{\arraystretch}{1.25}\begin{tabular}{%s}' % cols, ' & ' + ' & '.join('$%s$' % c for c in cl) + r' & \textbf{Total}\\\hline']
    for i, r in enumerate(rl + [r'\textbf{Total}']):
        if i == len(rl): o.append(r'\hline')
        o.append(('$%s$' % r if i < len(rl) else r) + ' & ' + ' & '.join('$%s$' % fmt(v) for v in M[i]) + r'\\')
    o.append(r'\end{tabular}}')
    return '\n'.join(o)
def ct(a, b, ab, la='A', lb='B', fmt=Q, tot=1):
    """tabla 2×2 a partir de P(A), P(B) y P(A∩B)"""
    a, b, ab = F(a), F(b), F(ab)
    M = [[ab, a - ab, a], [b - ab, tot - a - b + ab, tot - a], [b, tot - b, tot]]
    assert all(v >= 0 for r in M for v in r)
    return taula([la, r'\overline{%s}' % la], [lb, r'\overline{%s}' % lb], M, fmt)
def arbre(br, l=(2.4, 2.6), s=(2.6, 1.3), root=''):
    """árbol de probabilidades: br = [(etiqueta, prob, hijos)], hijos = [(etiqueta, prob, texto de la hoja)]"""
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
    """árbol de dos niveles para probabilidad total: names[i], pri[i] = P(A_i), cond[i] = P(D|A_i)"""
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
S.append(("Experimentos aleatorios, regla de Laplace y recuento", [
 (1, r"Sean $A$, $B$ y $C$ tres sucesos de un mismo experimento. Expresa con operaciones:" + tasks(2, [
      r"Ocurre solo $B$.", r"Ocurre al menos uno.", r"No ocurre ninguno.", r"Ocurre exactamente uno.", r"Ocurren al menos dos.", r"Ocurren como mucho dos."])
     + recorda(r"De Morgan: $\overline{A\cup B}=\co A\cap\co B$ y $\overline{A\cap B}=\co A\cup\co B$; también valen para tres sucesos."),
     tasks(1, [r"$\res{\co A\cap B\cap\co C}$", r"$\res{A\cup B\cup C}$", r"$\res{\co A\cap\co B\cap\co C=\overline{A\cup B\cup C}}$",
               r"$\res{(A\cap\co B\cap\co C)\cup(\co A\cap B\cap\co C)\cup(\co A\cap\co B\cap C)}$", r"$\res{(A\cap B)\cup(A\cap C)\cup(B\cap C)}$",
               r"$\res{\overline{A\cap B\cap C}=\co A\cup\co B\cup\co C}$"])),
 (1, r"Lanzamos dos dados. Calcula la probabilidad de que:" + tasks(2, [r"el resultado más alto sea un 4;", r"los dos resultados se diferencien como mucho en 1;", r"el primero sea mayor que el segundo;", r"el producto sea múltiplo de 3."]),
     r"Hay $36$ parejas equiprobables." + tasks(2, [r"$(1,4),\dots,(4,4)$ y $(4,1),(4,2),(4,3)$: $\frac{7}{36}=" + B(l1[0]) + "$", r"$6+5+5=16$ parejas: $" + B(l1[1]) + "$",
      r"por simetría, $\frac{36-6}{2}=15$ parejas: $" + B(l1[2]) + "$", r"$1-\frac{4\cdot4}{36}=\frac{20}{36}=" + B(l1[3]) + "$ (ninguno de los dos es 3 o 6)"])),
 (1, r"En un grupo hay 6 chicas y 5 chicos. Se eligen al azar 4 personas para hacer un trabajo. Calcula la probabilidad de que haya dos chicas y dos chicos, y la de que haya al menos una chica."
     + recorda(r"si elegimos un grupo (no importa el orden), contamos con combinaciones: $\binom nk=\frac{n!}{k!\,(n-k)!}$."),
     r"Casos posibles: $\binom{11}{4}=330$." + tasks(1, [r"$\dfrac{\binom62\binom52}{\binom{11}4}=\dfrac{15\cdot10}{330}=" + B(cm[0]) + "$",
      r"$1-\dfrac{\binom54}{\binom{11}{4}}=1-\dfrac{5}{330}=" + B(cm[1]) + "$"])),
 (1, r"Colocamos al azar en una estantería 5 libros diferentes, 3 de los cuales son de matemáticas. ¿Cuál es la probabilidad de que los tres de matemáticas queden juntos?",
     r"Casos posibles: $5!=120$. Favorables: el bloque de matemáticas y los otros dos libros se pueden ordenar de $3!$ maneras, y dentro del bloque, de $3!$ maneras: $36$. $\ P=\frac{36}{120}=" + B(lb) + "$."),
 (2, r"En la Lotería Primitiva se extraen 6 números del 1 al 49. Una persona hace una apuesta de 6 números. Calcula la probabilidad de que acierte los 6 números y la de que acierte exactamente 5.",
     r"Casos posibles: $\binom{49}{6}=13\,983\,816$." + tasks(1, [r"$P(6)=\dfrac{1}{13\,983\,816}\approx" + r"\res{7{,}15\cdot10^{-8}}$",
      r"$P(5)=\dfrac{\binom65\binom{43}1}{\binom{49}6}=\dfrac{258}{13\,983\,816}\approx\res{1{,}85\cdot10^{-5}}$ (5 de los 6 premiados y 1 de los 43 restantes)"])
     + ('' if ck([float(pr6), float(pr5)], [7.15e-8, 1.845e-5], 1e-7) else '')),
 (2, r"\emph{Problema de los cumpleaños.} Supongamos que todos los días del año (365) son igual de probables para nacer. Calcula la probabilidad de que, en un grupo de 5 personas, al menos dos cumplan años el mismo día. Repite el cálculo para un grupo de 23 personas (con la calculadora).",
     r"Lo contrario es que todos cumplan años en días diferentes: $P=1-\dfrac{V_{365,5}}{365^5}=1-\dfrac{365\cdot364\cdot363\cdot362\cdot361}{365^5}\approx" + r"\res{" + d4(an5) + "}$."
     + r" Para 23 personas: $1-\dfrac{V_{365,23}}{365^{23}}\approx\res{" + d4(an23) + r"}$: ¡ya es más probable que sí que no!"),
 (1, r"Un dado está trucado de manera que la probabilidad de cada cara es proporcional al número que aparece en ella. Calcula la probabilidad de cada cara, la de obtener un número par y la de obtener más de 2.",
     r"$P(k)=c\,k$ y $c(1+2+\dots+6)=21c=1\Rightarrow\res{P(k)=\frac{k}{21}}$. \ $P(\text{par})=\frac{2+4+6}{21}=" + B(F(12, 21)) + r"$; \ $P(X>2)=1-\frac{1+2}{21}=" + B(F(18, 21)) + "$."),
 (1, r"\pau{Asturias, extraordinaria 2025} En un monedero hay 5 monedas de 1 euro, 3 de 2 euros y 2 de 10 céntimos." + tasks(1, [
      r"Si sacamos 3 monedas al azar, ¿cuál es la probabilidad de que al menos una sea de 1 euro?", r"Sacamos dos monedas, una detrás de otra (sin reemplazamiento). ¿Cuál es la probabilidad de que la segunda sea de 10 céntimos?"]),
     tasks(1, [r"$1-P(\text{ninguna de 1 euro})=1-\dfrac{\binom53}{\binom{10}3}=1-\dfrac{10}{120}=" + B(mon[0]) + "$",
               r"$\frac{2}{10}\cdot\frac19+\frac{8}{10}\cdot\frac29=\frac{18}{90}=" + B(mon[1]) + "$ (como la primera: el orden no favorece ninguna posición)"])),
 (2, r"\pau{Navarra, ordinaria 2026} Sobre la Piedra de San Martín se encuentran 5 bearneses, 5 roncaleses y 2 suletinos. Los bearneses hablan entre ellos en bearnés; los roncaleses, en euskera; los suletinos hablan entre ellos en euskera, pero también se pueden comunicar en bearnés con los bearneses." + tasks(1, [
      r"Tomando dos personas al azar, ¿cuál es la probabilidad de que se comuniquen en euskera?", r"Tomando dos personas al azar, ¿cuál es la probabilidad de que se comuniquen en bearnés?",
      r"Los 5 roncaleses y los 5 bearneses se van a celebrar la paz. Si se sientan tres al azar en una mesa, ¿cuál es la probabilidad de que no hablen todos el mismo idioma?"]),
     r"Parejas posibles: $\binom{12}{2}=66$." + tasks(1, [r"Hablan euskera entre ellos los $5+2=7$ roncaleses y suletinos: $\frac{\binom72}{66}=\frac{21}{66}=" + B(eu[0]) + "$",
      r"Dos bearneses o un bearnés y un suletino: $\frac{\binom52+5\cdot2}{66}=\frac{20}{66}=" + B(eu[1]) + "$",
      r"$1-P(\text{los tres del mismo pueblo})=1-\dfrac{2\binom53}{\binom{10}3}=1-\dfrac{20}{120}=" + B(eu[2]) + "$"])),
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
S.append(("Fórmulas de la probabilidad", [
 (1, r"De dos sucesos se sabe que $P(A)=0{,}5$, $P(B)=0{,}4$ y $P(\co A\cup\co B)=0{,}8$. Calcula:" + tasks(3, [r"$P(A\cap B)$", r"$P(A\cup B)$", r"$P(\text{solo uno})$", r"$P(\co A\cap B)$", r"$P(\co A\cap\co B)$"])
     + recorda(r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$; \ $P(\co A)=1-P(A)$; \ $P(A\cap\co B)=P(A)-P(A\cap B)$."),
     r"De Morgan: $P(A\cap B)=1-P(\co A\cup\co B)$." + tasks(3, [r"$1-0{,}8=" + B(f1['i']) + "$", r"$0{,}5+0{,}4-0{,}2=" + B(f1['u']) + "$", r"$0{,}7-0{,}2=" + B(f1['u'] - f1['i']) + "$",
      r"$0{,}4-0{,}2=" + B(f1['b'] - f1['i']) + "$", r"$1-0{,}7=" + B(1 - f1['u']) + "$"]) + cen(venn(f1['a'] - f1['i'], f1['i'], f1['b'] - f1['i'], 1 - f1['u']))),
 (2, r"Sean $A$ y $B$ dos sucesos con $P(A)=0{,}7$ y $P(B)=0{,}6$." + tasks(1, [r"¿Pueden ser incompatibles?", r"¿Entre qué valores puede estar $P(A\cap B)$? I $P(A\cup B)$?", r"Demuestra que, en general, $P(A\cap B)\geq P(A)+P(B)-1$ para dos sucesos cualesquiera."]),
     tasks(1, [r"\rest{No}: si lo fueran, $P(A\cup B)=1{,}3>1$.", r"$P(A\cap B)=1{,}3-P(A\cup B)\geq0{,}3$ y $A\cap B\subset B\Rightarrow P(A\cap B)\leq0{,}6$: \ $\res{0{,}3\leq P(A\cap B)\leq0{,}6}$ \ y \ $\res{0{,}7\leq P(A\cup B)\leq1}$.",
               r"Como $P(A\cup B)\leq1$: $P(A\cap B)=P(A)+P(B)-P(A\cup B)\geq P(A)+P(B)-1$. \rest{(Desigualdad de Bonferroni.)}"])),
 (2, r"Tres sucesos cumplen $P(A)=0{,}5$, $P(B)=0{,}4$, $P(C)=0{,}3$, $P(A\cap B)=0{,}2$, $P(A\cap C)=0{,}15$, $P(B\cap C)=0{,}1$ y $P(A\cap B\cap C)=0{,}05$. Calcula la probabilidad de que:" + tasks(2, [
      r"ocurra al menos uno;", r"no ocurra ninguno;", r"ocurra solo $A$;", r"ocurra exactamente uno."]),
     tasks(2, [r"$0{,}5+0{,}4+0{,}3-0{,}2-0{,}15-0{,}1+0{,}05=" + B(u3) + "$", r"$1-0{,}8=" + B(1 - u3) + "$", r"$0{,}5-0{,}2-0{,}15+0{,}05=" + B(nA3) + "$",
               r"$0{,}2+0{,}15+0{,}05=" + B(ex1) + "$ (solo $A$, solo $B$ y solo $C$)"])),
 (1, r"En una encuesta a 200 personas, 120 se informan por las redes sociales, 90 por la televisión y 40 por ambos medios. Construye la tabla de contingencia y calcula la probabilidad de que una persona elegida al azar se informe por alguno de los dos medios, por ninguno y solo por uno.",
     cen(taula(['X', r'\overline{X}'], ['T', r'\overline{T}'], [[40, 80, 120], [50, 30, 80], [90, 110, 200]], str)) +
     tasks(3, [r"$\frac{170}{200}=" + B(F(170, 200)) + "$", r"$\frac{30}{200}=" + B(F(30, 200)) + "$", r"$\frac{80+50}{200}=" + B(F(130, 200)) + "$"])),
 (1, r"\pau{Islas Baleares, extraordinaria 2025} Sean $A$ y $B$ dos sucesos de un experimento aleatorio y $A'$, $B'$ sus contrarios. Sabiendo que $P(A)=0{,}75$, $P(B')=0{,}45$ y $P(A-B)=0{,}3$, calcula:" + tasks(3, [r"$P(A\cap B)$", r"$P(B-A)$", r"$P(A'\cap B')$"]),
     r"$P(B)=0{,}55$." + tasks(3, [r"$P(A)-P(A-B)=" + B(bl['i']) + "$", r"$0{,}55-0{,}45=" + B(bl['b'] - bl['i']) + "$", r"$1-(0{,}75+0{,}55-0{,}45)=" + B(1 - bl['a'] - bl['b'] + bl['i']) + "$"])),
 (1, r"\pau{La Rioja, ordinaria 2024} De dos sucesos $A$ y $B$ se sabe que $P(A)=0{,}27$, $P(B')=0{,}82$ y $P(A\cup B)=0{,}4$. Determina si son compatibles o incompatibles y calcula $P\big((A\cup B)'\big)$ y $P(A'\cup B')$.",
     r"$P(A\cap B)=0{,}27+0{,}18-0{,}4=0{,}05\neq0$: \rest{son compatibles}. \ $P\big((A\cup B)'\big)=1-0{,}4=" + B(1 - rj['u']) + r"$; \ $P(A'\cup B')=1-P(A\cap B)=" + B(1 - rj['i']) + "$."),
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
S.append(("Probabilidad condicionada e independencia", [
 (1, r"De dos sucesos se sabe que $P(A)=0{,}6$, $P(B\cond A)=0{,}5$ y $P(B\cond\co A)=0{,}25$. Calcula $P(A\cap B)$, $P(B)$, $P(A\cond B)$ y $P(A\cup B)$. ¿Son independientes?"
     + recorda(r"$P(A\cond B)=\dfrac{P(A\cap B)}{P(B)}$. $A$ y $B$ son independientes si $P(A\cap B)=P(A)P(B)$, es decir, si $P(A\cond B)=P(A)$."),
     r"$P(A\cap B)=0{,}6\cdot0{,}5=" + B(c1['ab']) + r"$; \ $P(B)=0{,}3+0{,}4\cdot0{,}25=" + B(c1['b']) + r"$; \ $P(A\cond B)=\frac{0{,}3}{0{,}4}=" + B(c1['ab'] / c1['b'])
     + r"$; \ $P(A\cup B)=0{,}6+0{,}4-0{,}3=" + B(c1['a'] + c1['b'] - c1['ab']) + r"$. Como $P(B\cond A)=0{,}5\neq P(B)=0{,}4$, \rest{no son independientes}."),
 (2, r"Demuestra que si $A$ y $B$ son independientes, también lo son $A$ y $\co B$. Deduce que también lo son $\co A$ y $\co B$.",
     r"$P(A\cap\co B)=P(A)-P(A\cap B)=P(A)-P(A)P(B)=P(A)\big(1-P(B)\big)=P(A)\,P(\co B)$. \ Aplicando el mismo resultado a la pareja $\co B$, $A$ (que son independientes), también son independientes $\co B$ y $\co A$."),
 (1, r"Dos sucesos independientes tienen la misma probabilidad y $P(A\cup B)=0{,}75$. Calcula $P(A)$ y la probabilidad de que ocurra exactamente uno.",
     r"$2x-x^2=0{,}75\Rightarrow x^2-2x+0{,}75=0\Rightarrow x=0{,}5$ (la otra solución, $1{,}5$, no es una probabilidad): $\res{P(A)=0{,}5}$. \ $P(\text{exactamente uno})=2\cdot0{,}5\cdot0{,}5=" + B(F(1, 2)) + "$."),
 (1, r"Tres tiradores disparan una vez cada uno a un blanco, de manera independiente. Las probabilidades de que acierten son $0{,}6$, $0{,}5$ y $0{,}4$. Calcula la probabilidad de que el blanco reciba algún impacto y la de que reciba exactamente dos.",
     r"$P(\text{al menos uno})=1-0{,}4\cdot0{,}5\cdot0{,}6=" + B(sh[0]) + r"$. \ Exactamente dos: $0{,}6\cdot0{,}5\cdot0{,}6+0{,}6\cdot0{,}5\cdot0{,}4+0{,}4\cdot0{,}5\cdot0{,}4=" + B(sh[1]) + "$."),
 (1, r"\pau{Asturias, ordinaria 2026} En una fábrica de pantalones vaqueros, el 10\,\% de las prendas no pasa el test de longitud, el 5\,\% no pasa el de las costuras y el 0,8\,\% no pasa ninguno de los dos." + tasks(1, [
      r"Calcula la probabilidad de que una prenda elegida al azar no pase al menos uno de los tests.", r"Si una prenda no ha pasado el test de longitud, ¿qué probabilidad hay de que tampoco pase el de las costuras?"]),
     tasks(1, [r"$0{,}1+0{,}05-0{,}008=" + B(ast[0]) + "$", r"$\frac{0{,}008}{0{,}1}=" + B(ast[1]) + "$"])),
 (1, r"\pau{Islas Baleares, extraordinaria 2026} En un instituto de 60 alumnos, el 60\,\% juega a baloncesto, el 35\,\% forma parte de un equipo federado y el 25\,\% juega a baloncesto y está federado." + tasks(1, [
      r"¿Hay algún alumno federado que no juegue a baloncesto? Si lo hay, ¿cuántos?", r"¿Cuál es la probabilidad de que un alumno sea de un equipo federado sabiendo que juega a baloncesto?"]),
     tasks(1, [r"$0{,}35-0{,}25=0{,}1$ y $0{,}1\cdot60=\res{6\text{ alumnos}}$.", r"$P(F\cond B)=\frac{0{,}25}{0{,}6}=" + B(bal[1]) + "$"])),
 (1, r"\pau{Cantabria, ordinaria 2025} En un colegio se ofrecen atletismo ($A$) y baloncesto ($B$) como actividades extraescolares, con $P(A)=0{,}4$ y $P(B)=0{,}65$. Solo un 10\,\% del alumnado no se matricula en ningún deporte." + tasks(1, [
      r"Calcula la probabilidad de que un alumno se matricule en los dos deportes.", r"Calcula $P(A\cond B)$, $P(B\cond A)$ y $P(A\cond B^c)$."]),
     tasks(1, [r"$P(A\cap B)=0{,}4+0{,}65-0{,}9=" + B(cn['i']) + "$", r"$\frac{0{,}15}{0{,}65}=" + B(cn['i'] / cn['b']) + r"$; \ $\frac{0{,}15}{0{,}4}=" + B(cn['i'] / cn['a']) + r"$; \ $\frac{0{,}25}{0{,}35}=" + B((cn['a'] - cn['i']) / (1 - cn['b'])) + "$"])),
 (1, r"\pau{Extremadura, ordinaria 2024} En una residencia, el 80\,\% de los residentes tiene correo electrónico, el 60\,\% tiene redes sociales y el 10\,\% no tiene ni lo uno ni lo otro. Calcula la probabilidad de que un residente:" + tasks(1, [
      r"use correo electrónico y redes sociales;", r"use solo una de las dos cosas;", r"use correo electrónico sabiendo que no usa redes sociales."]),
     cen(ct(ex['c'], ex['x'], ex['i'], 'C', 'X')) + tasks(3, [r"$0{,}8+0{,}6-0{,}9=" + B(ex['i']) + "$", r"$0{,}9-0{,}5=" + B(ex['u'] - ex['i']) + "$", r"$\frac{0{,}3}{0{,}4}=" + B((ex['c'] - ex['i']) / (1 - ex['x'])) + "$"])),
 (2, r"\pau{Galicia, ordinaria 2024} Se sabe que $P(A)=\frac13$ y $P(B)=\frac12$." + tasks(1, [
      r"Suponiendo que $A$ y $B$ son independientes, calcula $P(A\cup B)$ y $P\big(\co A\,/\,(\co A\cup\co B)\big)$.", r"Suponiendo que $A$ y $B$ son incompatibles, calcula $P(A\cup B)$ y $P\big(\co A\,/\,(\co A\cup\co B)\big)$."]),
     tasks(1, [r"$P(A\cup B)=\frac13+\frac12-\frac16=" + B(F(2, 3)) + r"$. Como $\co A\subset\co A\cup\co B$: $\dfrac{P(\co A)}{1-P(A\cap B)}=\dfrac{2/3}{5/6}=" + B(F(4, 5)) + "$",
               r"$P(A\cup B)=\frac13+\frac12=" + B(F(5, 6)) + r"$. Ahora $\co A\cup\co B=\overline{A\cap B}=E$: $P(\co A)=" + B(F(2, 3)) + "$"])),
 (1, r"\pau{Castilla-La Mancha, ordinaria 2024} Sean $A$ y $B$ dos sucesos tales que $P(A)=0{,}2$, $P(A\cap B)=0{,}1$ y $P(A\cup B)=0{,}3$. Calcula $P(B)$, $P(A\cap\co B)$, $P(A\cond B)$ y $P(B\cond A)$.",
     r"$P(B)=0{,}3-0{,}2+0{,}1=" + B(cl['b']) + r"$; \ $P(A\cap\co B)=0{,}2-0{,}1=" + B(cl['a'] - cl['i']) + r"$; \ $P(A\cond B)=\frac{0{,}1}{0{,}2}=" + B(cl['i'] / cl['b']) + r"$; \ $P(B\cond A)=" + B(cl['i'] / cl['a']) + "$."),
 (2, r"\pau{Madrid, ordinaria 2026} Sabiendo que $P(B)=0{,}4$, $P\big(\overline{A\cup B}\big)=0{,}4$ y $P(B\cond A)=0{,}2$, calcula:" + tasks(1, [r"$P(\co A)$ y $P(A\cap B)$.", r"$P\big((A\cap B)\cond(A\cup B)\big)$."]),
     tasks(1, [r"Si $P(A)=x$: $P(A\cap B)=0{,}2x$ y $P(A\cup B)=x+0{,}4-0{,}2x=0{,}6\Rightarrow x=0{,}25$. \ $P(\co A)=" + B(1 - md['a']) + r"$, \ $P(A\cap B)=" + B(md['i']) + "$",
               r"$A\cap B\subset A\cup B$: \ $\frac{0{,}05}{0{,}6}=" + B(md['i'] / md['u']) + "$"])),
 (1, r"\pau{Madrid, ordinaria 2025 (coincidencias)} Se sabe que $P(A)=0{,}7$, $P(\co B)=0{,}2$ y $P(\co A\cap\co B)=0{,}1$." + tasks(1, [
      r"Razona si $\co A$ y $\co B$ son independientes.", r"Calcula $P(A\cap B)$.", r"Calcula $P(\co A\cond B)$."]),
     tasks(1, [r"$P(\co A)P(\co B)=0{,}3\cdot0{,}2=0{,}06\neq0{,}1$: \rest{no son independientes}.", r"$P(A\cup B)=0{,}9\Rightarrow P(A\cap B)=0{,}7+0{,}8-0{,}9=" + B(mc['i']) + "$",
               r"$\frac{P(B)-P(A\cap B)}{P(B)}=\frac{0{,}2}{0{,}8}=" + B((mc['b'] - mc['i']) / mc['b']) + "$"])),
 (1, r"\pau{País Vasco, extraordinaria 2024} Sean $A$ y $B$ sucesos independientes con $P(A)=0{,}7$ y $P(B)=0{,}1$. Calcula razonadamente:" + tasks(3, [r"$P(A\cup B)$", r"$P(\co A\cup\co B)$", r"$P(\co A\cap\co B)$", r"$P(A\cap\co B)$", r"$P(\co A\cond B)$"]),
     tasks(2, [r"$0{,}7+0{,}1-0{,}07=" + B(pvr[0]) + "$", r"$1-P(A\cap B)=" + B(pvr[1]) + "$", r"$0{,}3\cdot0{,}9=" + B(pvr[2]) + "$ (independientes)", r"$0{,}7\cdot0{,}9=" + B(pvr[3]) + "$",
               r"$P(\co A)=" + B(pvr[4]) + "$ (independientes)"])),
 (1, r"\pau{Islas Baleares, ordinaria 2024} Sean $A$ y $B$ dos sucesos con $P(A\cup B)=0{,}7$, $P(A\cap B)=0{,}1$ y $P(A\cap B^c)=0{,}35$. Calcula:" + tasks(4, [r"$P(A)$", r"$P(B)$", r"$P(A^c\cup B^c)$", r"¿Independientes?"]),
     tasks(2, [r"$0{,}1+0{,}35=" + B(bo['a']) + "$", r"$0{,}7-0{,}35=" + B(bo['b']) + "$", r"$1-0{,}1=" + B(1 - bo['i']) + "$", r"$0{,}45\cdot0{,}35=0{,}1575\neq0{,}1$: \rest{no}"])),
 (1, r"\pau{Murcia, extraordinaria 2024} El 60\,\% de los habitantes de una población consume pan integral, el 40\,\% pan blanco y el 20\,\% ambos." + tasks(1, [
      r"¿Son independientes los sucesos «consumir pan integral» y «consumir pan blanco»?", r"Sabiendo que un habitante consume pan integral, ¿cuál es la probabilidad de que consuma pan blanco?",
      r"¿Qué porcentaje de la población no consume ninguno de los dos tipos de pan?", r"Sabiendo que un habitante no consume pan integral, ¿cuál es la probabilidad de que consuma pan blanco?"]),
     tasks(2, [r"$0{,}6\cdot0{,}4=0{,}24\neq0{,}2$: \rest{no}", r"$\frac{0{,}2}{0{,}6}=" + B(mu['ib'] / mu['i']) + "$", r"$1-0{,}8=0{,}2$: \ $\res{20\,\%}$", r"$\frac{0{,}4-0{,}2}{0{,}4}=" + B((mu['b'] - mu['ib']) / (1 - mu['i'])) + "$"])),
 (2, r"\pau{Aragón, ordinaria 2025} De dos sucesos se sabe que $P(A\cond B)=\frac23$ y $P(B\cond A)=\frac34$." + tasks(1, [
      r"Si $A$ y $B$ fueran independientes, ¿cuánto valdría $P(A\cup B)$?", r"Si $P(A\cup B)=\frac56$, ¿cuáles son las probabilidades $P(A)$, $P(B)$ y $P(A\cup\co B)$?"]),
     tasks(1, [r"Independientes: $P(A)=\frac23$ y $P(B)=\frac34$; \ $P(A\cup B)=\frac23+\frac34-\frac12=" + B(F(11, 12)) + "$",
               r"Si $x=P(A\cap B)$: $P(B)=\frac{3x}{2}$, $P(A)=\frac{4x}{3}$ y $\frac{4x}{3}+\frac{3x}{2}-x=\frac{11x}{6}=\frac56\Rightarrow x=\frac{5}{11}$. \ $P(A)=" + B(ar_a) + r"$, \ $P(B)=" + B(ar_b)
               + r"$, \ $P(A\cup\co B)=1-P(\co A\cap B)=1-\left(\frac{15}{22}-\frac{5}{11}\right)=" + B(1 - ar_b + ar_x) + "$"])),
 (1, r"\pau{Castilla y León, extraordinaria 2025} En un grupo de WhatsApp de un gimnasio de judo, el 55\,\% son mujeres y el resto hombres. El 15\,\% del grupo es cinturón verde, y una quinta parte de las mujeres es cinturón verde." + tasks(1, [
      r"¿Qué porcentaje de los hombres es cinturón verde?", r"Si el grupo recibe un mensaje de un cinturón verde, ¿cuál es la probabilidad de que lo haya enviado una mujer?", r"Si no sabemos nada del remitente, ¿cuál es la probabilidad de que sea hombre y cinturón verde?"]),
     r"$P(D\cap V)=0{,}55\cdot0{,}2=0{,}11$ y $P(H\cap V)=0{,}15-0{,}11=0{,}04$." + tasks(1, [r"$P(V\cond H)=\frac{0{,}04}{0{,}45}=" + B(cy['hv'] / F('0.45')) + r"$: \ $\res{8{,}89\,\%}$", r"$\frac{0{,}11}{0{,}15}=" + B(cy['dv'] / cy['v']) + "$", r"$" + B(cy['hv']) + "$"])),
 (1, r"\pau{Cantabria, ordinaria 2026} En un criadero de cobayas las hay de pelo corto y de pelo largo, blancas o marrones. El 60\,\% de las cobayas es de pelo corto y solo el 8\,\% son blancas de pelo largo." + tasks(1, [
      r"Calcula la probabilidad de que una cobaya de pelo largo elegida al azar sea marrón.", r"Si la probabilidad de que una cobaya sea blanca es 0,2, calcula la probabilidad de que una cobaya marrón sea de pelo largo.", r"Con el mismo dato, calcula la probabilidad de que una cobaya de pelo corto sea marrón."]),
     cen(taula(['C', 'L'], ['Bl', 'M'], [[F('0.12'), F('0.48'), F('0.6')], [F('0.08'), F('0.32'), F('0.4')], [F('0.2'), F('0.8'), 1]])) +
     tasks(3, [r"$\frac{0{,}32}{0{,}4}=" + B(cb['ml'] / F('0.4')) + "$", r"$\frac{0{,}32}{0{,}8}=" + B(cb['ml'] / F('0.8')) + "$", r"$\frac{0{,}48}{0{,}6}=" + B(F('0.48') / F('0.6')) + "$"])),
 (2, r"\pau{Galicia, extraordinaria 2025} Antón tiene 60 pares de zapatillas, cada uno en su caja: el 80\,\% son tradicionales y el 20\,\% de diseño. Entre las de diseño, el 75\,\% están en buen estado, pero solo el 50\,\% de las tradicionales lo están. Un día coge una caja al azar." + tasks(1, [
      r"¿Cuál es la probabilidad de que lleve zapatillas tradicionales o en buen estado?", r"Antón no quiere llevar zapatillas que no estén en buen estado ni zapatillas tradicionales. ¿Cuál es la probabilidad de que no tenga que cambiarse?",
      r"Antón tiene 8 pares de zapatillas tradicionales blancas. Sabiendo que, al elegir una caja al azar, los sucesos «ser blancas» y «ser de diseño» son independientes, ¿cuántos pares de zapatillas blancas de diseño tiene?"]),
     tasks(1, [r"$P(T\cup Bo)=P(T)+P(D\cap Bo)=0{,}8+0{,}2\cdot0{,}75=" + B(gz[0]) + "$", r"$P(D\cap Bo)=" + B(gz[1]) + "$",
               r"Si tiene $x$: $\frac{x}{60}=\frac{8+x}{60}\cdot\frac{12}{60}\Rightarrow60x=96+12x\Rightarrow\res{x=2}$ pares."])),
 (1, r"\pau{La Rioja, ordinaria 2026} Las probabilidades de aprobar tres asignaturas de un grado son 60\,\%, 75\,\% y 80\,\% (Métodos Algorítmicos, Estadística y Bases de Datos), de manera independiente." + tasks(1, [
      r"Calcula la probabilidad de que un estudiante apruebe las tres.", r"Calcula la probabilidad de que suspenda solo una.", r"Si un estudiante ha suspendido solo una, ¿cuál es la probabilidad de que sea Métodos Algorítmicos?"]),
     tasks(1, [r"$0{,}6\cdot0{,}75\cdot0{,}8=" + B(lr3) + "$", r"$0{,}4\cdot0{,}75\cdot0{,}8+0{,}6\cdot0{,}25\cdot0{,}8+0{,}6\cdot0{,}75\cdot0{,}2=0{,}24+0{,}12+0{,}09=" + B(lr1) + "$",
               r"$\frac{0{,}24}{0{,}45}=" + B(lrm / lr1) + "$"])),
 (1, r"\pau{Aragón, ordinaria 2024} En una asignatura hay 99 personas matriculadas (54 mujeres y 45 hombres). En primera convocatoria aprueban 49 personas (28 mujeres y 21 hombres)." + tasks(1, [
      r"¿Qué porcentaje de las mujeres aprueba en primera convocatoria? ¿Y de los hombres?", r"Si elegimos al azar una persona que ha aprobado, ¿cuál es la probabilidad de que sea una mujer?"]),
     tasks(1, [r"Mujeres: $\frac{28}{54}\approx\res{51{,}85\,\%}$; \ hombres: $\frac{21}{45}\approx\res{46{,}67\,\%}$", r"$\frac{28}{49}=" + B(az[2]) + "$"])),
]))

# =====================================================================
# 4. Experiments compostos i extraccions
def urn(cnt, nd, rep):
    """todas las secuencias de colores con su probabilidad"""
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
    """probabilidad de que gane el jugador que empieza (sacar la primera blanca, sin reemplazamiento)"""
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
S.append(("Experimentos compuestos. Extracciones con y sin reemplazamiento", [
 (2, r"Una urna contiene 2 bolas blancas y 3 negras. Ana y Pablo sacan bolas alternadamente, empezando por Ana; gana quien saca la primera bola blanca. Calcula la probabilidad de que gane Ana:" + tasks(1, [r"si las bolas no se devuelven a la urna;", r"si cada bola se devuelve a la urna antes de la tirada siguiente."])
     + recorda(r"en un diagrama de árbol multiplicamos a lo largo de cada camino y sumamos los caminos que forman el suceso."),
     tasks(1, [r"Ana gana en la 1.ª o en la 3.ª extracción (en la 5.ª ya no puede ser, porque solo hay 3 negras): $\frac25+\frac35\cdot\frac24\cdot\frac23=\frac25+\frac15=" + B(ja[0]) + "$",
               r"Gana en la tirada 1, 3, 5\dots: $\frac25\left(1+\frac{9}{25}+\left(\frac{9}{25}\right)^2+\cdots\right)=\dfrac{2/5}{1-9/25}=" + B(ja[1]) + r"$ (serie geométrica de razón $\frac{9}{25}$)"])),
 (1, r"De una urna con 5 bolas rojas y 3 verdes se sacan dos sin reemplazamiento. Calcula la probabilidad de que la segunda sea roja y, sabiendo que la segunda ha sido roja, la probabilidad de que la primera también lo haya sido.",
     r"$P(R_2)=\frac58\cdot\frac47+\frac38\cdot\frac57=\frac{35}{56}=" + B(s2r) + r"$; \ $P(R_1\cond R_2)=\dfrac{20/56}{35/56}=" + B(F(4, 7)) + "$."),
 (1, r"Lanzamos un dado hasta que sale un 6. Calcula la probabilidad de que el primer 6 salga en la tercera tirada y la de que hagan falta más de tres tiradas.",
     r"$P(\text{1.er 6 en la 3.ª})=\left(\frac56\right)^2\frac16=" + B(d6[0]) + r"$; \ $P(\text{más de 3})=P(\text{ningún 6 en las 3 primeras})=\left(\frac56\right)^3=" + B(d6[1]) + "$."),
 (1, r"\pau{Castilla y León, ordinaria 2026} De una bolsa con 20 fichas numeradas del 1 al 20 se extraen sucesivamente 2 sin reemplazamiento. Calcula la probabilidad de que:" + tasks(1, [
      r"los dos números sean múltiplos de 3;", r"el primero sea múltiplo de 6 y el segundo múltiplo de 3;", r"ninguno de los dos sea múltiplo de 2;", r"la segunda ficha sea impar, sabiendo que la primera también lo ha sido."]),
     tasks(2, [r"$\frac{6}{20}\cdot\frac{5}{19}=" + B(cyf[0]) + "$", r"$\frac{3}{20}\cdot\frac{5}{19}=" + B(cyf[1]) + "$", r"$\frac{10}{20}\cdot\frac{9}{19}=" + B(cyf[2]) + "$", r"$\frac{9}{19}\approx" + dec(cyf[3]) + r"$ \ ($\res{\frac{9}{19}}$)"])),
 (2, r"\pau{Castilla-La Mancha, ordinaria 2025} De una baraja española de 40 cartas (con 4 ases), un jugador va sacando cartas una a una hasta que encuentra un as. Después, el otro jugador junta todas las cartas, las baraja y hace lo mismo. Gana quien haya sacado más cartas (contando el as); si sacan las mismas, empatan." + tasks(1, [
      r"Calcula las probabilidades de que el as salga al sacar 1, 2 y 3 cartas, respectivamente.", r"Si el primer jugador ha sacado dos cartas (contando el as), ¿cuál es la probabilidad de que el segundo jugador gane?"]),
     tasks(1, [r"$P(1)=\frac{4}{40}=" + B(ases[0]) + r"$; \ $P(2)=\frac{36}{40}\cdot\frac{4}{39}=" + B(ases[1]) + r"$; \ $P(3)=\frac{36}{40}\cdot\frac{35}{39}\cdot\frac{4}{38}=" + B(ases[2]) + "$",
               r"Tiene que sacar más de 2: $1-\frac1{10}-\frac{6}{65}=" + B(1 - ases[0] - ases[1]) + "$"])),
 (1, r"\pau{Castilla-La Mancha, extraordinaria 2024} En un mazo de 40 cartas, 4 están marcadas solo con un punto verde, 5 solo con un punto rojo y 7 con los dos puntos. (Una carta «tiene punto verde» si tiene solo uno verde o si tiene uno verde y uno rojo.)" + tasks(1, [
      r"¿Cuál es la probabilidad de sacar dos cartas sin reemplazamiento y que ambas tengan punto verde?", r"Si sacamos una carta y tiene punto verde, ¿cuál es la probabilidad de que también tenga punto rojo?"]),
     r"Tienen punto verde $4+7=11$ cartas." + tasks(1, [r"$\frac{11}{40}\cdot\frac{10}{39}=\frac{11}{156}\approx\res{" + d4(cv[0]) + "}$", r"$\frac{7}{11}=" + B(cv[1]) + "$"])),
 (2, r"\pau{Aragón, extraordinaria 2026} La urna A tiene dos bolas rojas y tres azules, y la urna B, dos azules y tres rojas." + tasks(1, [
      r"Si sacamos al azar una bola de cada urna, ¿qué es más probable, que salgan del mismo color o de distinto color?", r"Las bolas extraídas en el apartado anterior se ponen en la urna contraria (la de A en la B y al revés). Si ahora sacamos una bola de la urna B, ¿cuál es la probabilidad de que sea azul?"]),
     tasks(1, [r"$P(\text{mismo color})=\frac25\cdot\frac35+\frac35\cdot\frac25=" + B(asame) + r"<\frac12$: \rest{es más probable que sean de distinto color} ($0{,}52$).",
               r"Si de A sale azul y de B roja, B queda con 3 azules; si salen del mismo color, B no cambia (2 azules); si de A sale roja y de B azul, B queda con 1 azul: $\frac35\cdot\frac35\cdot\frac35+\frac{12}{25}\cdot\frac25+\frac25\cdot\frac25\cdot\frac15=" + B(asw) + "$"])),
 (2, r"\pau{Aragón, ordinaria 2025} Una ficha se mueve en un tablero de tres casillas en fila (1, 2, 3). En cada turno se lanza una moneda equilibrada: si sale cara se intenta mover la ficha a la izquierda y si sale cruz, a la derecha; si no se puede hacer el movimiento, la ficha se queda donde está." + tasks(1, [
      r"Construye una tabla con las probabilidades de pasar de una casilla a otra en un turno.", r"Si la ficha está en la casilla 1, ¿cuál es la probabilidad de que, después de tres turnos, vuelva a estar en la casilla 1?",
      r"La ficha empieza en la casilla 1 con probabilidad $\frac12$ y en la 2 y en la 3 con probabilidad $\frac14$ cada una. ¿Cuál es la probabilidad de que esté en cada casilla después de dos turnos?"]),
     tasks(1, [r"Desde la 1: a la 1 o a la 2 con $\frac12$; desde la 2: a la 1 o a la 3 con $\frac12$; desde la 3: a la 2 o a la 3 con $\frac12$.",
               r"Caminos 1-1-1-1, 1-1-2-1 y 1-2-1-1, cada uno con probabilidad $\frac18$: $" + B(tb[1]) + "$",
               r"$P(1)=" + B(tc[1]) + r"$, \ $P(2)=" + B(tc[2]) + r"$, \ $P(3)=" + B(tc[3]) + "$"])),
 (1, r"\pau{Canarias, ordinaria 2024} En un avión se han instalado tres paracaídas $A$, $B$ y $C$: si falla $A$ se activa $B$, y si también falla $B$ se activa $C$. Las probabilidades de que funcionen correctamente son $0{,}96$, $0{,}98$ y $0{,}99$." + tasks(1, [
      r"Dibuja un diagrama de árbol con todos los casos posibles.", r"Calcula la probabilidad de que se active el paracaídas $B$ y funcione correctamente.", r"Calcula la probabilidad de que funcione algún paracaídas."]),
     cen(arbre([('A', F('0.96'), []), (r'\overline{A}', F('0.04'), [('B', F('0.98'), F('0.04') * F('0.98')), (r'\overline{B}\to C', F('0.02'), '')])], s=(2.2, 1.3))) +
     tasks(1, [r"Si falla $B$, se activa $C$ ($0{,}99$ funciona, $0{,}01$ falla).", r"$0{,}04\cdot0{,}98=" + B(pq[0]) + "$", r"$1-0{,}04\cdot0{,}02\cdot0{,}01=" + B(pq[1]) + "$"])),
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
S.append(("Probabilidad total y teorema de Bayes", [
 (2, r"Una enfermedad afecta al 2\,\% de una población. Un test da positivo en el 90\,\% de los enfermos y en el 5\,\% de los sanos." + tasks(1, [
      r"Si el test de una persona da positivo, ¿cuál es la probabilidad de que esté enferma?", r"Para confirmarlo, se repite el test (de manera independiente). Si da positivo las dos veces, ¿cuál es ahora la probabilidad de que esté enferma?"])
     + recorda(r"probabilidad total: $P(D)=\sum P(A_i)\,P(D\cond A_i)$. Bayes: $P(A_i\cond D)=\dfrac{P(A_i)\,P(D\cond A_i)}{P(D)}$."),
     tasks(1, [r"$\dfrac{0{,}02\cdot0{,}9}{0{,}02\cdot0{,}9+0{,}98\cdot0{,}05}=\dfrac{0{,}018}{0{,}067}\approx\res{" + d4(tw[0]) + "}$",
               r"$\dfrac{0{,}02\cdot0{,}9^2}{0{,}02\cdot0{,}9^2+0{,}98\cdot0{,}05^2}=\dfrac{0{,}0162}{0{,}01865}\approx\res{" + d4(tw[1]) + "}$: el segundo positivo hace mucho más fiable el diagnóstico."])),
 (1, r"\pau{Andalucía, extraordinaria 2026} Tres máquinas, $A$, $B$ y $C$, producen el 45\,\%, el 30\,\% y el 25\,\% de los coches de una fábrica, con un 3\,\%, un 4\,\% y un 5\,\% de coches defectuosos, respectivamente." + tasks(1, [
      r"Elegimos un coche al azar. Calcula la probabilidad de que sea defectuoso.", r"Un coche elegido al azar resulta defectuoso. ¿Qué máquina tiene la mayor probabilidad de haberlo producido?"]),
     tasks(1, [r"$0{,}45\cdot0{,}03+0{,}3\cdot0{,}04+0{,}25\cdot0{,}05=0{,}0135+0{,}012+0{,}0125=" + B(anT) + "$",
               r"$P(A\cond D)=\frac{0{,}0135}{0{,}038}\approx" + dec(anB[0]) + r"$, \ $P(B\cond D)\approx" + dec(anB[1]) + r"$, \ $P(C\cond D)\approx" + dec(anB[2]) + r"$: \rest{la máquina $A$}."])),
 (1, r"\pau{Asturias, extraordinaria 2026} Una jugadora de tenis de mesa empieza los partidos restando en el 75\,\% de las ocasiones. Cuando empieza restando gana el 80\,\% de los partidos, y cuando empieza sacando, el 65\,\%." + tasks(1, [
      r"Calcula la probabilidad de que gane un partido.", r"Calcula la probabilidad de que haya empezado restando en un partido, sabiendo que lo ha ganado."]),
     tasks(1, [r"$0{,}75\cdot0{,}8+0{,}25\cdot0{,}65=" + B(asT) + "$", r"$\frac{0{,}6}{0{,}7625}=" + B(F('0.6') / asT) + "$"])),
 (1, r"\pau{Islas Baleares, ordinaria 2026} En una plataforma de \emph{streaming} de videojuegos, el 40\,\% de los usuarios juega principalmente a juegos competitivos en línea; de estos, el 30\,\% participa en torneos oficiales. Entre los que no juegan principalmente a juegos competitivos, el 20\,\% también participa en torneos." + tasks(1, [
      r"Si elegimos un usuario que no juega principalmente a juegos competitivos, ¿cuál es la probabilidad de que no participe en torneos?", r"Si un usuario participa en torneos, ¿qué es más probable, que juegue principalmente a juegos competitivos o que no?"]),
     tasks(1, [r"$1-0{,}2=" + B(F('0.8')) + "$", r"$P(T)=0{,}12+0{,}12=0{,}24$; $P(C\cond T)=\frac{0{,}12}{0{,}24}=0{,}5=P(\co C\cond T)$: \rest{son igual de probables}."])),
 (2, r"\pau{Islas Baleares, ordinaria 2025} La probabilidad de tener tuberculosis es 0,0005. La probabilidad de que una prueba dé positivo si la enfermedad está presente es del 99\,\%, y la de que dé negativo si no está presente también es del 99\,\%." + tasks(1, [
      r"¿Cuál es la probabilidad de que la prueba dé positivo si la persona no tiene la enfermedad?", r"¿Cuál es la probabilidad de tener tuberculosis si el resultado de la prueba es negativo?"]),
     tasks(1, [r"$1-0{,}99=" + B(F('0.01')) + "$", r"$\dfrac{0{,}0005\cdot0{,}01}{0{,}0005\cdot0{,}01+0{,}9995\cdot0{,}99}=\dfrac{1}{197\,902}\approx\res{5{,}05\cdot10^{-6}}$"])),
 (2, r"\pau{Canarias, extraordinaria 2025} Una prueba detecta una enfermedad rara que afecta al 1\,\% de la población adulta. La sensibilidad de la prueba (dar positivo si la persona está enferma) es del 95\,\% y la especificidad (dar negativo si está sana), del 98\,\%." + tasks(1, [
      r"Calcula la probabilidad de que una persona esté enferma si la prueba da positivo.", r"Si 35\,000 personas se hacen la prueba, ¿podemos afirmar que se espera que haya más de 50 personas enfermas con resultado negativo?"]),
     tasks(1, [r"$\dfrac{0{,}01\cdot0{,}95}{0{,}01\cdot0{,}95+0{,}99\cdot0{,}02}=\dfrac{0{,}0095}{0{,}0293}=" + B(F('0.0095') / cxT) + "$",
               r"$P(M\cap\text{neg})=0{,}01\cdot0{,}05=0{,}0005$ y $35\,000\cdot0{,}0005=17{,}5$: \rest{no}, se esperan unas 17 o 18."])),
 (1, r"\pau{Canarias, extraordinaria 2024} Una enfermedad la pueden producir tres virus, $A$, $B$ y $C$. En un laboratorio hay tres tubos con el virus $A$, dos con el $B$ y cinco con el $C$. La probabilidad de que el virus $A$ produzca la enfermedad es $\frac13$; la del $B$, $\frac23$, y la del $C$, $\frac17$." + tasks(1, [
      r"Se elige un tubo al azar y se inocula el virus a un animal. ¿Cuál es la probabilidad de que le produzca la enfermedad?", r"Si no se la produce, ¿cuál es la probabilidad de que se le haya inyectado el virus $C$?"]),
     tasks(1, [r"$\frac{3}{10}\cdot\frac13+\frac{2}{10}\cdot\frac23+\frac{5}{10}\cdot\frac17=" + B(cvT) + "$", r"$\dfrac{\frac12\cdot\frac67}{1-\frac{32}{105}}=\dfrac{3/7}{73/105}=" + B(F(5, 10) * F(6, 7) / (1 - cvT)) + "$"])),
 (2, r"\pau{Canarias, extraordinaria 2026} Un observatorio recibe 120 sensores: 20 son para el telescopio LST-1 y el resto se reparten por igual entre los telescopios MAGIC-I y MAGIC-II. Después del transporte, un sensor de los MAGIC se tiene que recalibrar con probabilidad 0,016 y uno del LST-1, con probabilidad 0,009. Se elige un sensor al azar." + tasks(1, [
      r"Calcula la probabilidad de que se tenga que recalibrar.", r"Si el sensor elegido no se tiene que recalibrar, ¿es la probabilidad de que sea del MAGIC-II mayor que el doble de la probabilidad de que sea del LST-1?"]),
     tasks(1, [r"$\frac{100}{120}\cdot0{,}016+\frac{20}{120}\cdot0{,}009=\frac{1{,}78}{120}\approx\res{" + d4(csT) + "}$",
               r"Las dos probabilidades tienen el mismo denominador $P(\co R)$; comparamos los numeradores: $\frac{50}{120}\cdot0{,}984=0{,}41$ y $\frac{20}{120}\cdot0{,}991\approx0{,}165$. Como $0{,}41>2\cdot0{,}165$, \rest{sí}."])),
 (1, r"\pau{Castilla y León, ordinaria 2024} De entre los vehículos que revisa un taller, el 48\,\% son coches (tres cuartas partes requieren reparación), el 28\,\% motocicletas (la mitad la requiere) y el 24\,\% furgonetas (un tercio la requiere). Sean $C$, $M$, $F$ y $R$ los sucesos «coche», «motocicleta», «furgoneta» y «requiere reparación»." + tasks(1, [
      r"Indica qué probabilidades da el enunciado.", r"Calcula $P(R\cap F)$, $P(R)$ y $P(C\cond R)$.", r"¿Son independientes $C$ y $R$?"]),
     tasks(1, [r"$P(C)=0{,}48$, $P(M)=0{,}28$, $P(F)=0{,}24$; $P(R\cond C)=\frac34$, $P(R\cond M)=\frac12$, $P(R\cond F)=\frac13$.",
               r"$P(R\cap F)=0{,}24\cdot\frac13=" + B(F('0.08')) + r"$; \ $P(R)=0{,}36+0{,}14+0{,}08=" + B(vrT) + r"$; \ $P(C\cond R)=\frac{0{,}36}{0{,}58}=" + B(F('0.36') / vrT) + "$",
               r"$P(R\cond C)=0{,}75\neq P(R)=0{,}58$: \rest{no}."])),
 (1, r"\pau{La Rioja, extraordinaria 2024} El 2\,\% de la población mundial padece una enfermedad. Una prueba para detectarla da positivo en el 98\,\% de los enfermos y en el 4\,\% de las personas sanas. Calcula:" + tasks(1, [
      r"la probabilidad de que una persona esté sana, si la prueba ha dado positivo;", r"la probabilidad de que una persona esté enferma, si la prueba ha dado negativo."]),
     tasks(1, [r"$\dfrac{0{,}98\cdot0{,}04}{0{,}02\cdot0{,}98+0{,}98\cdot0{,}04}=\dfrac{0{,}0392}{0{,}0588}=" + B(F(2, 3)) + "$", r"$\dfrac{0{,}02\cdot0{,}02}{1-0{,}0588}=\dfrac{0{,}0004}{0{,}9412}=" + B(F(1, 2353)) + "$"])),
 (2, r"\pau{Madrid, extraordinaria 2025} La probabilidad de que un corredor sufra una caída un día de lluvia es 0,08, y un día seco, 0,004. La probabilidad de llover y caerse es 0,032. Hoy un corredor ha salido a correr." + tasks(1, [
      r"Calcula la probabilidad de que vuelva a casa sin haberse caído.", r"Calcula la probabilidad de que no esté lloviendo, sabiendo que se ha caído."]),
     r"$P(Ll)\cdot0{,}08=0{,}032\Rightarrow P(Ll)=0{,}4$; \ $P(C)=0{,}032+0{,}6\cdot0{,}004=0{,}0344$." + tasks(1, [r"$1-0{,}0344=" + B(1 - mdT) + "$", r"$\frac{0{,}0024}{0{,}0344}=" + B((mdT - F('0.032')) / mdT) + "$"])),
 (3, r"\pau{Madrid, ordinaria 2024} En la sección de idiomas de una biblioteca hay libros en francés o en inglés de tres categorías: el 50\,\% son cuentos infantiles, el 30\,\% novelas históricas y el resto, manuales técnicos. Uno de cada cinco cuentos está en francés y una de cada tres novelas, en inglés. Además, uno de cada siete libros en francés es un manual técnico. Se elige un libro al azar." + tasks(1, [
      r"Calcula la probabilidad de que esté en francés si no es un manual técnico.", r"Calcula la probabilidad de que esté en francés, y la probabilidad de que sea una novela histórica si está en inglés."]),
     r"$P(Fr\cap C)=0{,}5\cdot\frac15=0{,}1$, \ $P(Fr\cap N)=0{,}3\cdot\frac23=0{,}2$. Si $x=P(Fr\cap M)$: $x=\frac17(0{,}3+x)\Rightarrow x=0{,}05$." +
     tasks(1, [r"$P(Fr\cond\co M)=\frac{0{,}1+0{,}2}{0{,}8}=" + B(F('0.375')) + "$", r"$P(Fr)=0{,}35$; \ $P(N\cond An)=\frac{0{,}3\cdot\frac13}{0{,}65}=\frac{0{,}1}{0{,}65}=" + B(F(2, 13)) + "$"])),
 (3, r"\pau{Madrid, extraordinaria 2024} En un espacio muestral hay dos sucesos incompatibles $A_1$ y $A_2$, de probabilidad 0,4 cada uno, y $A_3=\overline{A_1\cup A_2}$ (de probabilidad 0,2). De un suceso $B$ se sabe que $P(B\cond A_1)=P(B\cond A_2)$ y $P(B\cond A_3)=2P(B\cond A_1)$; y de un suceso $C$ independiente de $A_1$, que $P(C\cond A_2)=0{,}3$ y $P(C\cond A_3)=0{,}6$." + tasks(1, [
      r"Calcula $P(B)$ si $P(B\cond A_1)=0{,}25$.", r"Calcula $P(C)$ y determina si $C$ es independiente de $A_2$."]),
     tasks(1, [r"$P(B)=0{,}4\cdot0{,}25+0{,}4\cdot0{,}25+0{,}2\cdot0{,}5=" + B(mbB) + "$",
               r"Como $C$ y $A_1$ son independientes, $P(C\cond A_1)=P(C)=c$: \ $c=0{,}4c+0{,}4\cdot0{,}3+0{,}2\cdot0{,}6\Rightarrow0{,}6c=0{,}24\Rightarrow" + B(mc_) + r"$. Como $P(C\cond A_2)=0{,}3\neq0{,}4$, \rest{no es independiente de $A_2$}."])),
 (1, r"\pau{Murcia, ordinaria 2025} La urna $U_1$ tiene 2 bolas rojas y 3 verdes, y la urna $U_2$, 6 rojas y 3 verdes. Se saca una bola de $U_1$, se pone en $U_2$ y, a continuación, se saca una bola de $U_2$. Calcula la probabilidad de que:" + tasks(1, [
      r"salga roja en $U_2$ sabiendo que ha salido roja en $U_1$;", r"salga verde en $U_2$ sabiendo que ha salido roja en $U_1$;", r"salga verde en $U_2$;", r"haya salido roja en $U_1$ sabiendo que ha salido roja en $U_2$."]),
     cen(arbre([('R_1', F(2, 5), [('R_2', F(7, 10), F(2, 5) * F(7, 10)), ('V_2', F(3, 10), F(2, 5) * F(3, 10))]), ('V_1', F(3, 5), [('R_2', F(6, 10), F(3, 5) * F(6, 10)), ('V_2', F(4, 10), F(3, 5) * F(4, 10))])], s=(2.4, 1.3))) +
     tasks(2, [r"$\frac{7}{10}=" + B(mr[0]) + "$", r"$\frac{3}{10}=" + B(mr[1]) + "$", r"$0{,}12+0{,}24=" + B(mr[2]) + "$", r"$\frac{0{,}28}{0{,}64}=" + B(F(7, 16)) + "$"])),
 (1, r"\pau{País Vasco, ordinaria 2026} En 2025 se vendieron en España 1\,148\,650 coches: el 10\,\% totalmente eléctricos (todos de cambio automático), el 52\,\% híbridos (el 6\,\% de ellos de cambio manual) y, del resto, el 53\,\% de cambio automático." + tasks(1, [
      r"Calcula la cantidad de coches de cambio automático vendidos en 2025.", r"Elegimos al azar un coche vendido en 2025 que tiene cambio automático. Calcula la probabilidad de que sea híbrido."]),
     r"$P(Au)=0{,}1+0{,}52\cdot0{,}94+0{,}38\cdot0{,}53=0{,}7902$." + tasks(1, [r"$0{,}7902\cdot1\,148\,650\approx\res{907\,663\text{ coches}}$", r"$\frac{0{,}4888}{0{,}7902}=" + B(F('0.52') * F('0.94') / pbA) + "$"])),
 (1, r"\pau{País Vasco, ordinaria 2024} La urna A tiene 3 bolas verdes, 5 rojas y 4 azules, y la urna B, 2 verdes, 2 rojas y 3 azules. Se saca al azar una bola de A, se pone en B y, después, se saca una bola de B." + tasks(1, [
      r"Haz el diagrama de árbol.", r"Calcula la probabilidad de que la bola extraída de B sea verde.", r"Calcula la probabilidad de que la bola de B sea verde sabiendo que la de A ha sido roja.", r"Sabiendo que la bola de B es verde, calcula la probabilidad de que la de A haya sido roja."]),
     cen(arbre([('V_A', F(3, 12), [('V_B', F(3, 8), '')]), ('R_A', F(5, 12), [('V_B', F(2, 8), '')]), ('B_A', F(4, 12), [('V_B', F(2, 8), '')])], s=(1.7, 1.3))) +
     tasks(2, [r"(Solo dibujamos las ramas de $V_B$.)", r"$\frac{3}{12}\cdot\frac38+\frac{5}{12}\cdot\frac28+\frac{4}{12}\cdot\frac28=" + B(pa_) + "$", r"$\frac28=" + B(F(1, 4)) + "$", r"$\dfrac{\frac{5}{12}\cdot\frac28}{9/32}=" + B(F(10, 27)) + "$"])),
 (2, r"\pau{Aragón, ordinaria 2026} En un hospital se usan dos técnicas para operar una misma lesión. Estas son las intervenciones de los últimos años y, entre paréntesis, las que fueron efectivas:" + cen(taula(['\\text{Graves}', '\\text{Leves}'], ['\\text{Técnica 1}', '\\text{Técnica 2}'], [['44\\ (30)', '140\\ (102)', '184'], ['136\\ (120)', '40\\ (36)', '176'], ['180\\ (150)', '180\\ (138)', '360']], str)) + tasks(1, [
      r"Se elige al azar el expediente de una intervención efectiva. ¿Cuál de las dos técnicas es más probable que se haya usado?", r"Un cirujano quiere elegir la técnica con más probabilidad de éxito. ¿Cuál elegirá para una lesión leve? ¿Y para una grave?",
      r"Cuando no se sabe la gravedad de la lesión, el protocolo del hospital es aplicar la técnica 1. Justifica por qué no es lo más adecuado."]),
     tasks(1, [r"Hay $150+138=288$ intervenciones efectivas: $P(T_1\cond E)=\frac{150}{288}\approx0{,}52>P(T_2\cond E)=\frac{138}{288}$: \rest{la técnica 1}.",
               r"Leve: $\frac{120}{136}\approx0{,}88<\frac{36}{40}=0{,}9$; grave: $\frac{30}{44}\approx0{,}68<\frac{102}{140}\approx0{,}73$: \rest{la técnica 2 en ambos casos}.",
               r"En total, $P(E\cond T_1)=\frac{150}{180}\approx0{,}83>P(E\cond T_2)=\frac{138}{180}\approx0{,}77$ solo porque la técnica 1 se ha aplicado sobre todo a lesiones leves. Pero la técnica 2 es mejor tanto en las leves como en las graves: \rest{se debería aplicar la 2} (paradoja de Simpson)."])),
 (1, r"\pau{Aragón, extraordinaria 2025} La Universidad de Zaragoza tiene tres centros en Teruel, con 1550, 250 y 150 estudiantes (Ciencias Sociales, Politécnica y Enfermería). El 74\,\% de los estudiantes de Ciencias Sociales son mujeres, el 18\,\% de los de la Politécnica y el 76\,\% de los de Enfermería." + tasks(1, [
      r"Si se elige un estudiante al azar, ¿cuál es la probabilidad de que sea mujer?", r"Si es mujer, ¿cuál es la probabilidad de que estudie en la Politécnica?", r"Si es hombre, ¿cuál es la probabilidad de que estudie en la Politécnica?"]),
     r"Mujeres: $1147+45+114=1306$ de 1950." + tasks(3, [r"$\frac{1306}{1950}\approx\res{" + d4(F(1306, 1950)) + "}$", r"$\frac{45}{1306}\approx\res{" + d4(F(45, 1306)) + "}$", r"$\frac{205}{644}\approx\res{" + d4(F(205, 644)) + "}$"])),
 (1, r"\pau{Cantabria, extraordinaria 2026} La caja A tiene 10 bolas, 4 de las cuales son blancas; la B tiene 6, una blanca, y la C tiene 3 blancas de 8. El resto son rojas." + tasks(1, [
      r"Calcula la probabilidad de que, al sacar una bola de una caja elegida al azar, sea blanca.", r"Si la bola elegida es blanca, ¿cuál es la probabilidad de que sea de la caja B?", r"Calcula la probabilidad de obtener dos bolas blancas si se sacan dos bolas de una caja elegida al azar entre la A y la B."]),
     tasks(1, [r"$\frac13\left(\frac4{10}+\frac16+\frac38\right)=" + B(cbT) + "$", r"$\dfrac{\frac13\cdot\frac16}{113/360}=" + B(F(20, 113)) + "$", r"$\frac12\cdot\frac{4}{10}\cdot\frac39+\frac12\cdot0=" + B(F(1, 15)) + "$ (en la B solo hay una blanca)"])),
 (2, r"\pau{Canarias, ordinaria 2025} En una feria, un participante elige una de tres cajas sorpresa: una tiene premio y las otras dos están vacías. Si elige una caja vacía, saca una bola de una urna con 2 bolas verdes y 3 negras: si es negra, termina sin premio; si es verde, puede elegir una nueva caja entre las dos que no había elegido, y termina." + tasks(1, [
      r"Dibuja un diagrama de árbol del juego.", r"Calcula la probabilidad de obtener premio.", r"Si el participante ha obtenido premio, ¿cuál es la probabilidad de que haya sacado bola verde?"]),
     cen(arbre([('P', F(1, 3), []), (r'\overline{P}', F(2, 3), [('V\\to P', F(2, 5) * F(1, 2), F(2, 3) * F(1, 5)), ('\\text{no}', 1 - F(2, 5) * F(1, 2), '')])], s=(2.2, 1.3))) +
     tasks(1, [r"Después de la verde, acierta la caja con probabilidad $\frac12$: la rama $V\to P$ tiene $\frac25\cdot\frac12=\frac15$.", r"$\frac13+\frac23\cdot\frac15=" + B(cpT) + "$", r"$\dfrac{2/15}{7/15}=" + B(F(2, 7)) + "$"])),
 (1, r"\pau{Castilla y León, ordinaria 2025} De una urna con cuatro bolas rojas y dos azules se saca una y, sin devolverla, se saca otra." + tasks(1, [
      r"Calcula la probabilidad de que sean de distinto color.", r"Calcula la probabilidad de que la segunda bola sea azul.", r"Si la segunda bola es azul, calcula la probabilidad de que la primera sea roja."]),
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
S.append(("Variables aleatorias discretas y distribución binomial", [
 (1, r"Una variable aleatoria $X$ toma los valores 0, 1, 2 y 3 con probabilidades $0{,}1$, $a$, $2a$ y $0{,}3$. Calcula $a$, la media y la desviación típica de $X$, y $P(X\geq2)$."
     + recorda(r"$\sum p_i=1$; \ $\mu=\sum x_ip_i$; \ $\sigma^2=\sum x_i^2p_i-\mu^2$."),
     r"$0{,}1+3a+0{,}3=1\Rightarrow\res{a=0{,}2}$. \ $\mu=0{,}2+0{,}8+0{,}9=" + B(vm) + r"$; \ $\sigma^2=0{,}2+1{,}6+2{,}7-1{,}9^2=0{,}89\Rightarrow\sigma\approx\res{" + d4(sqrt(float(vv))) + r"}$; \ $P(X\geq2)=" + B(F('0.7')) + "$."),
 (2, r"Un juego consiste en pagar 1 € y sacar dos bolas, sin reemplazamiento, de una urna con 3 bolas blancas y 2 negras. Si las dos son blancas se cobran 3 €. Calcula la ganancia esperada del jugador. ¿Cuánto debería pagarse por dos blancas para que el juego fuera equitativo?",
     r"$P(BB)=\frac35\cdot\frac24=\frac{3}{10}$. La ganancia neta es $2$ € (prob. $0{,}3$) o $-1$ € (prob. $0{,}7$): $E=0{,}6-0{,}7=\res{-0{,}10\text{ €}}$ (pierde 10 céntimos por partida). Equitativo si $0{,}3\,x=1$: $\res{x=\frac{10}{3}\approx3{,}33\text{ €}}$."),
 (1, r"Razona si las variables siguientes son binomiales y, si lo son, indica sus parámetros:" + tasks(1, [r"número de cincos en 12 lanzamientos de un dado;", r"número de bolas rojas al sacar 3 bolas sin reemplazamiento de una urna con 4 rojas y 6 blancas;",
      r"número de lanzamientos de una moneda hasta que sale la primera cara;", r"número de piezas defectuosas en una muestra de 50 de una producción enorme con un 2\,\% de defectuosas."]),
     tasks(1, [r"\rest{Sí}: $B\left(12,\frac16\right)$.", r"\rest{No}: la probabilidad cambia de una extracción a otra (no son independientes).", r"\rest{No}: el número de pruebas no está fijado.", r"\rest{Sí} (población muy grande): $B(50;\ 0{,}02)$."])),
 (1, r"Si $X\sim B\left(6,\frac13\right)$, calcula $P(X=2)$, $P(X\leq1)$, $P(X\geq2)$, la media y la desviación típica."
     + recorda(r"$P(X=k)=\binom nk p^k q^{n-k}$, \ $\mu=np$, \ $\sigma=\sqrt{npq}$. Para «al menos», a menudo es más corto el contrario."),
     r"$P(X=2)=" + bt(6, F(1, 3), 2) + "=" + B(b6[0]) + r"$; \ $P(X\leq1)=\left(\frac23\right)^6+6\cdot\frac13\left(\frac23\right)^5=" + B(b6[1]) + r"$; \ $P(X\geq2)=1-P(X\leq1)=" + B(b6[2]) + r"$; \ $\mu=" + B(2) + r"$, \ $\sigma=\sqrt{6\cdot\frac13\cdot\frac23}=" + r"\res{\frac{2}{\sqrt3}\approx1{,}1547}$."),
 (2, r"Una variable $X\sim B(5,p)$ cumple $P(X=1)=P(X=2)$. Calcula $p$ y $P(X\geq1)$.",
     r"$5pq^4=10p^2q^3\Rightarrow q=2p\Rightarrow1-p=2p\Rightarrow\res{p=\frac13}$ ($p=0$ no tiene sentido). \ $P(X\geq1)=1-\left(\frac23\right)^5=" + B(1 - F(2, 3)**5) + "$."),
 (2, r"Una máquina hace un 2\,\% de piezas defectuosas. ¿Cuántas piezas hay que revisar, como mínimo, para que la probabilidad de encontrar al menos una defectuosa supere 0,5?",
     r"$1-0{,}98^n>0{,}5\iff0{,}98^n<0{,}5\iff n>\dfrac{\ln0{,}5}{\ln0{,}98}\approx" + dec(log(0.5) / log(0.98), 2) + r"$ (al dividir por $\ln0{,}98<0$ la desigualdad cambia de sentido): \ $\res{n=35}$ piezas."),
 (1, r"\pau{Aragón, extraordinaria 2024} El 84\,\% de los exámenes de Matemáticas II de la convocatoria ordinaria de 2022 en Aragón sacaron una nota igual o superior a 5." + tasks(1, [
      r"Si se seleccionan 15 de estos exámenes al azar, ¿cuál es la probabilidad de que exactamente 2 tengan una nota inferior a 5?", r"Con los 15 exámenes, ¿es más probable que menos de 2 tengan nota inferior a 5 o que más de 2 la tengan?"]),
     r"$X=$ «número de exámenes con nota inferior a 5» $\sim B(15;\ 0{,}16)$." + tasks(1, [r"$\binom{15}{2}0{,}16^2\,0{,}84^{13}\approx" + r"\res{" + dec(ar15[0], 5) + "}$",
      r"$P(X<2)=0{,}84^{15}+15\cdot0{,}16\cdot0{,}84^{14}\approx" + d4(ar15[1]) + r"$ i $P(X>2)=1-P(X\leq2)\approx" + d4(ar15[2]) + r"$: \rest{es más probable que más de 2}."])),
 (1, r"\pau{Castilla-La Mancha, extraordinaria 2025} Una inspectora de sanidad sabe que el 5\,\% de los restaurantes no pasará una inspección. Si elige 8 al azar, calcula la probabilidad de que:" + tasks(1, [
      r"tres restaurantes no pasen la inspección;", r"todos los restaurantes pasen la inspección;", r"al menos dos restaurantes pasen la inspección."]),
     r"$X=$ «número que no la pasan» $\sim B(8;\ 0{,}05)$." + tasks(1, [r"$\binom83\,0{,}05^3\,0{,}95^5\approx\res{" + d4(cr[0]) + "}$", r"$0{,}95^8\approx\res{" + d4(cr[1]) + "}$",
      r"La pasan al menos 2 si $X\leq6$: $1-P(X=7)-P(X=8)=1-8\cdot0{,}05^7\cdot0{,}95-0{,}05^8\approx\res{1}$ ($0{,}99999999$)"])),
 (1, r"\pau{Extremadura, extraordinaria 2024} La probabilidad de que un jugador de golf haga hoyo desde cierta distancia es 0,4. Si hace 5 lanzamientos, calcula:" + tasks(1, [r"la probabilidad de que no haga ningún hoyo;", r"la probabilidad de hacer como mucho 2 hoyos;", r"el número medio de hoyos."]),
     r"$X\sim B(5;\ 0{,}4)$." + tasks(3, [r"$0{,}6^5=" + B(gf[0]) + "$", r"$0{,}07776+0{,}2592+0{,}3456=" + B(gf[1]) + "$", r"$\mu=5\cdot0{,}4=\res{2}$"])),
 (1, r"\pau{Extremadura, ordinaria 2024} La tutora de Luis le propone un trato: si en los próximos 10 días llega tarde como mucho 3 días, le subirá 1 punto la nota. La probabilidad de que llegue tarde cada día es 0,5." + tasks(1, [
      r"¿Qué distribución sigue el número de días que llega tarde? ¿Cuáles son sus parámetros?", r"¿Cuáles son la media y la desviación típica?", r"¿Cuál es la probabilidad de que Luis consiga el punto?"]),
     tasks(1, [r"$\res{X\sim B(10;\ 0{,}5)}$", r"$\mu=" + B(5) + r"$ días; \ $\sigma=\sqrt{2{,}5}\approx\res{1{,}58}$ días", r"$P(X\leq3)=\frac{1+10+45+120}{1024}=\frac{176}{1024}\approx\res{" + d4(lu[2]) + "}$"])),
 (1, r"\pau{Galicia, extraordinaria 2024} En una colonia de cormoranes, cada huevo tiene un 13\,\% de probabilidad de ser infértil. Si se observa una puesta de 7 huevos, calcula la probabilidad de que haya al menos 2 infértiles.",
     r"$X\sim B(7;\ 0{,}13)$: \ $P(X\geq2)=1-0{,}87^7-7\cdot0{,}13\cdot0{,}87^6\approx\res{" + d4(gi) + "}$."),
 (1, r"\pau{Murcia, ordinaria 2026} Una fábrica de bombillas sabe que el 5\,\% son defectuosas. Calcula la probabilidad de que en 9 bombillas elegidas al azar haya exactamente 3 defectuosas.",
     r"$X\sim B(9;\ 0{,}05)$: \ $\binom93\,0{,}05^3\,0{,}95^6\approx\res{" + d4(mb) + "}$."),
 (1, r"\pau{Murcia, ordinaria 2025} El 2\,\% de las piezas que hace una máquina son defectuosas. Considera el número de piezas en buen estado de un lote de 10 piezas. ¿Qué distribución sigue? Indica su media y su desviación típica y calcula la probabilidad de que haya exactamente una pieza defectuosa.",
     r"$\res{Y\sim B(10;\ 0{,}98)}$, \ $\mu=" + B(F('9.8')) + r"$, \ $\sigma=\sqrt{10\cdot0{,}98\cdot0{,}02}\approx\res{" + d4(mp[1]) + r"}$. \ Una defectuosa es $Y=9$: $\binom{10}{9}0{,}98^9\,0{,}02\approx\res{" + d4(mp[2]) + "}$."),
 (1, r"\pau{Navarra, ordinaria 2026} En un examen tipo test de 10 preguntas, cada pregunta tiene 4 respuestas de las que solo una es correcta. Si se responde al azar:" + tasks(1, [
      r"¿Cuál es la probabilidad de fallarlas todas?", r"¿Cuál es la probabilidad de acertar exactamente 7?", r"Para aprobar hay que responder bien al menos 7 preguntas. ¿Cuál es la probabilidad de aprobar?"]),
     r"$X\sim B(10;\ 0{,}25)$." + tasks(3, [r"$0{,}75^{10}\approx\res{" + d4(nv[0]) + "}$", r"$\binom{10}{7}0{,}25^7\,0{,}75^3\approx\res{" + d4(nv[1]) + "}$", r"$P(X\geq7)\approx\res{" + d4(nv[2]) + "}$"])),
 (1, r"\pau{Canarias, extraordinaria 2026} Una academia de surf garantiza que, después del curso, un surfista principiante coge una ola con una probabilidad del 70\,\%." + tasks(1, [
      r"Si un alumno intenta coger 5 olas, ¿cuál es la probabilidad de que coja alguna?", r"Para contratar a un monitor se evalúa a un surfista experimentado que coge una ola con una probabilidad del 90\,\%. Lo contratan si coge al menos 14 de 15. ¿Cuál es la probabilidad de que lo contraten?"]),
     tasks(1, [r"$1-0{,}3^5=" + B(sf[0]) + "$", r"$X\sim B(15;\ 0{,}9)$: \ $0{,}9^{15}+15\cdot0{,}9^{14}\cdot0{,}1\approx\res{" + d4(sf[1]) + "}$"])),
 (1, r"\pau{Cataluña, septiembre 2026} Un parque eólico tiene 10 aerogeneradores de 100 MW cada uno. Cada aerogenerador tiene una probabilidad del 10\,\% de estar parado, independientemente de los demás." + tasks(1, [
      r"¿Cuál es la probabilidad de llegar a los 1000 MW de potencia total?", r"¿Cuál es la probabilidad de que la potencia total supere los 150 MW?"]),
     r"$X=$ «aerogeneradores en marcha» $\sim B(10;\ 0{,}9)$." + tasks(1, [r"Todos en marcha: $0{,}9^{10}\approx\res{" + d4(ae[0]) + "}$",
      r"Al menos 2 en marcha: $1-0{,}1^{10}-10\cdot0{,}9\cdot0{,}1^{9}=\res{0{,}9999999909}$"])),
 (2, r"\pau{Aragón, ordinaria 2026} Un test tiene 4 preguntas con 5 respuestas posibles cada una. Cada respuesta correcta suma 2,5 puntos y cada respuesta incorrecta resta 0,625. Se contestan las cuatro preguntas al azar." + tasks(1, [
      r"¿Cuál es la probabilidad de sacar un sobresaliente (nota igual o superior a 9)?", r"¿Cuál es la probabilidad de suspender (nota inferior a 5)?"]),
     r"Con $k$ aciertos, la nota es $2{,}5k-0{,}625(4-k)$: vale $10$, $6{,}875$, $3{,}75$\dots\ para $k=4,3,2\dots$ y $X\sim B\left(4;\ \frac15\right)$." + tasks(1, [
      r"Hay que acertarlas todas: $\left(\frac15\right)^4=" + B(tq[0]) + "$", r"Hace falta $X\leq2$: $1-P(X=3)-P(X=4)=1-\frac{16}{625}-\frac{1}{625}=" + B(tq[1]) + "$"])),
 (1, r"\pau{Extremadura, extraordinaria 2025} El 30\,\% de la población de una comarca ve el programa de televisión «La Revuelta». La productora telefonea al azar a 10 personas de la comarca." + tasks(1, [
      r"Calcula la probabilidad de que más de 8 personas estuvieran viendo el programa.", r"Calcula la probabilidad de que alguna de las 10 personas estuviera viendo el programa.",
      r"Se sabe que el 35\,\% de la población ve «El Hormiguero» y que el 40\,\% no ve ninguno de los dos programas. ¿Cuál es la probabilidad de que una persona vea los dos programas?"]),
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
S.append(("Problemas de síntesis", [
 (2, r"Una bolsa contiene dos monedas: una equilibrada y una trucada, con probabilidad de cara 0,8. Se elige una al azar y se lanza 5 veces. Si han salido exactamente 4 caras, ¿cuál es la probabilidad de que sea la moneda trucada?",
     r"Para cada moneda, el número de caras es binomial: $P(4\cond E)=\binom54\left(\frac12\right)^5=\frac{5}{32}$ y $P(4\cond T)=\binom54\,0{,}8^4\cdot0{,}2=0{,}4096$. \ Bayes: $P(T\cond4)=\dfrac{\frac12\cdot0{,}4096}{\frac12\cdot\frac{5}{32}+\frac12\cdot0{,}4096}\approx\res{" + d4(mT) + "}$."),
 (1, r"\pau{Castilla-La Mancha, extraordinaria 2024} Tenemos tres cajas: la A tiene dos cartas de espadas y tres de copas; la B, tres de espadas y dos de copas; y la C, cuatro de espadas y una de copas. Se lanza un dado: si sale impar se saca una carta de la caja A; si sale 4 o 6, de la B; y si sale 2, de la C." + tasks(1, [
      r"Calcula la probabilidad de obtener una carta de copas.", r"Sabiendo que la carta es de copas, ¿cuál es la probabilidad de que sea de la caja B?",
      r"La probabilidad de que un paracaidista novel caiga en el punto correcto es 0,25. Si se lanza 5 veces, ¿cuál es la probabilidad de que caiga en el punto correcto exactamente dos veces? ¿Y al menos una vez?"]),
     tasks(1, [r"$\frac12\cdot\frac35+\frac13\cdot\frac25+\frac16\cdot\frac15=" + B(cm8[0]) + "$", r"$\dfrac{2/15}{7/15}=" + B(F(2, 7)) + "$",
               r"$X\sim B(5;\ 0{,}25)$: \ $\binom52\,0{,}25^2\,0{,}75^3\approx\res{" + d4(cm8[1]) + r"}$; \ $1-0{,}75^5\approx\res{" + d4(cm8[2]) + "}$"])),
 (2, r"\pau{Madrid, ordinaria 2025 (coincidencias)} En una empresa tecnológica, el 70\,\% de los empleados son europeos. Una tercera parte de los no europeos se dedica a desarrollar software, y también tres de cada siete de los europeos." + tasks(1, [
      r"En un sorteo entre los empleados, calcula la probabilidad de que el premiado sea europeo y no desarrolle software.", r"En un segundo sorteo se eligen al azar 10 empleados, que recibirán un premio si como mucho 2 de ellos desarrollan software. Calcula la probabilidad de que la empresa tenga que dar este segundo premio."]),
     tasks(1, [r"$0{,}7\cdot\frac47=" + B(md4[0]) + "$", r"$P(\text{desarrolla})=0{,}7\cdot\frac37+0{,}3\cdot\frac13=0{,}4$ y $X\sim B(10;\ 0{,}4)$: \ $P(X\leq2)=0{,}6^{10}+10\cdot0{,}4\cdot0{,}6^9+45\cdot0{,}4^2\cdot0{,}6^8\approx\res{" + d4(md4b) + "}$"])),
 (1, r"\pau{Asturias, ordinaria 2025} El 6\,\% de las piezas que fabrica una empresa son defectuosas. En el control de calidad, un sistema de prueba da error con probabilidad 0,95 si la pieza es defectuosa y 0,04 si no lo es." + tasks(1, [
      r"Si se eligen 10 piezas al azar, ¿cuál es la probabilidad de que al menos una sea defectuosa?", r"Calcula la probabilidad de que, al probar una pieza elegida al azar, el sistema no dé error."]),
     tasks(1, [r"$X\sim B(10;\ 0{,}06)$: \ $1-0{,}94^{10}\approx\res{" + d4(asr[0]) + "}$", r"$0{,}06\cdot0{,}05+0{,}94\cdot0{,}96=" + B(asr[1]) + "$"])),
 (2, r"\pau{Cataluña, septiembre 2024} Se estima que el 20\,\% de los habitantes de una región padece arritmia. Un monitor Holter la detecta en el 95\,\% de los casos de personas que la padecen, pero también da falsos positivos en el 0,5\,\% de las personas que no la padecen." + tasks(1, [
      r"Si se eligen 4 personas al azar, ¿cuál es la probabilidad de que al menos una padezca arritmia?", r"¿Cuál es la probabilidad de que una persona elegida al azar obtenga un diagnóstico positivo?", r"Si una persona obtiene un diagnóstico negativo, ¿cuál es la probabilidad de que realmente padezca arritmia?"]),
     tasks(1, [r"$1-0{,}8^4=" + B(ctS[0]) + "$", r"$0{,}2\cdot0{,}95+0{,}8\cdot0{,}005=" + B(ctS[1]) + "$", r"$\frac{0{,}2\cdot0{,}05}{1-0{,}194}=\frac{0{,}01}{0{,}806}\approx\res{" + d4(ctS[2]) + "}$"])),
 (2, r"\pau{Cataluña, junio 2025} Una empresa produce piezas de hierro (el 60\,\%) y de acero (el resto). El 95\,\% de las de hierro no tiene ningún defecto, mientras que el 3\,\% de las de acero es defectuosa." + tasks(1, [
      r"Si tomamos una pieza al azar, ¿cuál es la probabilidad de que sea defectuosa?", r"La empresa producirá también piezas de titanio, que se venderán en paquetes de 5. Cada pieza de titanio es defectuosa con una probabilidad $p$, independientemente de las demás. Comprueba que la probabilidad de que en un paquete haya exactamente 4 piezas defectuosas es $f(p)=5p^4-5p^5$."]),
     tasks(1, [r"$0{,}6\cdot0{,}05+0{,}4\cdot0{,}03=" + B(cj) + "$", r"$X\sim B(5,p)$: $P(X=4)=\binom54p^4(1-p)=5p^4-5p^5$. \rest{\checkmark}"])),
 (2, r"\pau{Murcia, ordinaria 2024} El juego de los dados de Efron tiene 4 dados equilibrados de 6 caras, numerados así: dado A: 0, 0, 4, 4, 4, 4; dado B: 3, 3, 3, 3, 3, 3; dado C: 2, 2, 2, 2, 6, 6; dado D: 1, 1, 1, 5, 5, 5. Ana elige el dado A, Bea el B, Ceci el C y Delia el D. Cada jugadora lanza su dado: gana quien saca la puntuación más alta y pierde quien saca la más baja." + tasks(1, [
      r"Si Ana juega contra Bea, ¿cuál es la probabilidad de que gane Ana?", r"Si Ana juega 8 veces contra Bea, ¿cuál es la probabilidad de que Bea gane al menos 3 veces?",
      r"Si Ana juega contra Ceci, ¿cuál es la probabilidad de que gane Ceci?", r"Si juegan todas contra todas, ¿cuál es la probabilidad de que Ana ni gane ni pierda?"]),
     tasks(1, [r"Ana gana si saca 4: $" + B(ef_a) + "$", r"$X\sim B\left(8,\frac13\right)$: \ $P(X\geq3)=1-P(X\leq2)\approx\res{" + d4(ef_b) + "}$",
               r"Ceci gana si saca 6, o si saca 2 y Ana 0: $\frac13+\frac23\cdot\frac13=" + B(ef_c) + "$",
               r"Si Ana saca 0 pierde seguro; si saca 4, tiene que no ser la más alta (C o D superan el 4: $1-\frac23\cdot\frac12=\frac23$): $\frac23\cdot\frac23=" + B(ef_d) + "$"])),
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
% successos contraris i probabilitat condicionada
\newcommand{\co}[1]{\overline{#1}}
\newcommand{\cond}{\,|\,}
'''

TIT = "Probabilidad"
def build(sol):
    tt = 'Soluciones de la ficha' if sol else "Ficha de ejercicios"
    import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
    from castella import preambul, assignatura
    p = preambul(pre, pdftitle='%s de la unidad 10: %s' % (tt, TIT), capcalera='%s · Unidad 10: %s' % (tt, TIT),
                 pdfkeywords='probabilidad, sucesos, regla de Laplace, combinatoria, probabilidad condicionada, independencia, probabilidad total, teorema de Bayes, variable aleatoria, distribución binomial, PAU', curs='2batx-mii')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{2batx-mii}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-mii') + '{' + ('Soluciones de la ficha · Unidad 10' if sol else "Ficha de ejercicios · Unidad 10") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{7.2cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Las probabilidades se han calculado de manera exacta; cuando el resultado no es un decimal exacto, se da la fracción y el valor aproximado con cuatro decimales. Puedes comprobar los ejercicios de dos sucesos con la calculadora de los apuntes interactivos, y los de la binomial con el widget de la distribución binomial."
             if sol else r"Resuelve los ejercicios en el cuaderno justificando cada paso. Define siempre los sucesos con letras y escribe los datos con la notación de probabilidades ($P(A)$, $P(A\cap B)$, $P(A\,|\,B)$\dots); haz un diagrama de Venn, una tabla de contingencia o un diagrama de árbol cuando te ayude. Los " + str(NPAU) + r" ejercicios marcados con {\color{teal}\bfseries\faUniversity\ PAU} son de las pruebas de acceso a la universidad (Matemáticas II) de " + str(len(REGS)) + r" comunidades autónomas, traducidos al castellano; los de la PAU de la Comunidad Valenciana los tienes en la página de ejercicios tipo PAU de la unidad.") + r'''
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
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't10-fitxa-solucions-es.tex' if sol else 't10-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

NPAU = sum(len(re.findall(r'\\pau\{', e[1])) for _, ex in S for e in ex)
REGS = sorted({m_.split(',')[0] for _, ex in S for e in ex for m_ in re.findall(r'\\pau\{([^}]*)\}', e[1])})
n = build(False); build(True)
print(n, 'ejercicios,', NPAU, 'de la PAU de', len(REGS), 'comunidades:', ', '.join(REGS), '·', len(CHK), 'comprobaciones')
