# Versió en castellà de genera.py. Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex (2n Batxillerat CCSS, Unitat 9: Probabilitat)
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
S.append(("Espacio muestral y operaciones con sucesos", [
 (1, r"Escribe el espacio muestral de los experimentos siguientes y di cuántos elementos tiene:" + tasks(1, [
      r"Lanzar una moneda y un dado.", r"Anotar, por orden de nacimiento, si cada uno de los tres hijos de una familia es chico ($X$) o chica ($Y$).",
      r"Sacar, una detrás de otra y sin reemplazamiento, dos bolas de una urna que tiene una roja ($R$), una azul ($B$) y una verde ($V$).",
      r"Lanzar un dado hasta que salga un 6 y anotar el número de tiradas que han hecho falta."]),
     tasks(1, [r"$E=\{C1,C2,\dots,C6,\ {+}1,{+}2,\dots,{+}6\}$: \rest{12 elementos}.", r"$E=\{XXX,XXY,XYX,XYY,YXX,YXY,YYX,YYY\}$: \rest{8 elementos}.",
               r"$E=\{RB,RV,BR,BV,VR,VB\}$: \rest{6 elementos} (el orden importa y no se puede repetir el color).",
               r"$E=\{1,2,3,4,\dots\}$: es un espacio muestral \rest{infinito} (numerable)."])),
 (1, r"Lanzamos un dado y consideramos los sucesos $A=$«salir un número menor que 4», $B=$«salir par» y $C=$«salir 5 o 6». Calcula:" + tasks(4, [
      r"$A\cup B$", r"$A\cap B$", r"$\co A$", r"$\co B$", r"$A-B$", r"$B\cap C$", r"$\co A\cap\co B$", r"$\overline{A\cup C}$"])
     + r"¿Qué pares de estos sucesos son incompatibles?",
     r"$A=\{1,2,3\}$, $B=\{2,4,6\}$, $C=\{5,6\}$." + tasks(4, [r"$%s$" % st(A1 | B1), r"$%s$" % st(A1 & B1), r"$%s$" % st(E - A1), r"$%s$" % st(E - B1),
      r"$%s$" % st(A1 - B1), r"$%s$" % st(B1 & C1), r"$%s$" % st((E - A1) & (E - B1)), r"$%s$" % st(E - (A1 | C1))])
     + r"Solo \rest{$A$ y $C$} son incompatibles: $A\cap C=\varnothing$. ($A\cap B=\{2\}$ y $B\cap C=\{6\}$ no son vacíos.)"),
 (1, r"Sean $M=$«un alumno aprueba Matemáticas» y $N=$«aprueba Inglés». Expresa con operaciones entre $M$ y $N$ los sucesos siguientes:" + tasks(2, [
      r"Aprueba las dos.", r"No aprueba ninguna.", r"Aprueba solo Matemáticas.", r"Aprueba como mucho una.", r"Aprueba al menos una.", r"Aprueba exactamente una.", r"Suspende alguna de las dos."])
     + recorda(r"«al menos uno» es la unión; «ambos», la intersección; «ninguno» es $\co M\cap\co N=\overline{M\cup N}$ (De Morgan)."),
     tasks(2, [r"$\res{M\cap N}$", r"$\res{\co M\cap\co N=\overline{M\cup N}}$", r"$\res{M\cap\co N=M-N}$", r"$\res{\overline{M\cap N}=\co M\cup\co N}$", r"$\res{M\cup N}$",
               r"$\res{(M\cap\co N)\cup(\co M\cap N)}$", r"$\res{\co M\cup\co N}$ (lo mismo que «como mucho una»)."])),
 (1, r"En el espacio muestral $E=\{1,2,3,4,5,6,7,8\}$ consideramos $A=\{1,2,3,4\}$ y $B=\{2,4,6,8\}$. Comprueba las dos leyes de De Morgan.",
     r"$\overline{A\cup B}=\overline{%s}=%s$ y $\co A\cap\co B=%s\cap%s=%s$: \rest{coinciden}." % (st(A2 | B2), st(E8 - (A2 | B2)), st(E8 - A2), st(E8 - B2), st((E8 - A2) & (E8 - B2)))
     + r"\par $\overline{A\cap B}=\overline{%s}=%s$ y $\co A\cup\co B=%s$: \rest{coinciden}." % (st(A2 & B2), st(E8 - (A2 & B2)), st((E8 - A2) | (E8 - B2)))),
 (2, r"Sean $A$, $B$ y $C$ tres sucesos de un mismo experimento. Expresa con operaciones:" + tasks(2, [
      r"Ocurre solo $A$.", r"Ocurre al menos uno de los tres.", r"No ocurre ninguno.", r"Ocurre exactamente uno.", r"Ocurren los tres.", r"Ocurren al menos dos."]),
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
S.append(("Probabilidad. Regla de Laplace", [
 (1, r"Una urna contiene 4 bolas rojas, 5 azules y 3 verdes. Sacamos una bola al azar. Calcula la probabilidad de que:" + tasks(4, [r"sea roja;", r"no sea verde;", r"sea roja o azul;", r"sea amarilla."]),
     tasks(4, [r"$\frac{4}{12}=" + B(F(4, 12)) + "$", r"$\frac{9}{12}=" + B(F(9, 12)) + "$", r"$\frac{9}{12}=" + B(F(9, 12)) + "$", r"$\res{0}$ (imposible)"])),
 (1, r"Sacamos una carta de una baraja española de 40 cartas (cuatro palos de diez cartas: del 1 al 7, sota, caballo y rey). Calcula la probabilidad de sacar:" + tasks(2, [
      r"un oro;", r"una figura (sota, caballo o rey);", r"un oro o una figura;", r"una carta que no sea ni oro ni figura;", r"un as que no sea de oros."]),
     tasks(2, [r"$\frac{10}{40}=" + B(F(1, 4)) + "$", r"$\frac{12}{40}=" + B(F(12, 40)) + "$", r"$\frac{10+12-3}{40}=" + B(F(19, 40)) + "$ (las 3 figuras de oros se cuentan dos veces)",
               r"$1-\frac{19}{40}=" + B(F(21, 40)) + "$", r"$\res{\frac{3}{40}}$"])),
 (1, r"\pau{Castilla y León, EBAU ordinaria 2020} Se lanza una moneda tres veces. Calcula la probabilidad de obtener al menos una cruz.",
     r"Hay $2^3=8$ resultados equiprobables y solo $CCC$ no tiene ninguna cruz: $P=1-\frac18=" + B(ck(1 - F(sum(1 for m in M3 if '+' not in m), 8), F(7, 8))) + "$."),
 (1, r"\pau{Castilla y León, EBAU extraordinaria 2024} Una tienda de animales hace un sorteo con papeletas de tres cifras. El número premiado se obtiene sacando al azar cada cifra, por separado y con reemplazamiento, de una bolsa con bolas del 0 al 9. Calcula la probabilidad de que el número premiado acabe en 55.",
     r"Hay 1000 números posibles (000 a 999) y acaban en 55 los 10 de la forma $x55$: $P=\frac{10}{1000}=" + B(ck(F(10, 1000), F(1, 100))) + "$."),
 (1, r"Lanzamos dos dados. Calcula la probabilidad de que:" + tasks(2, [r"la suma sea 9;", r"la suma sea como mucho 4;", r"el producto sea 12;", r"los dos resultados sean pares;", r"la diferencia entre los dos resultados sea al menos 3."]),
     r"Hay $6\cdot6=36$ parejas equiprobables." + tasks(2, [r"(3,6), (4,5), (5,4), (6,3): $\frac{4}{36}=" + B(L1[0]) + "$", r"6 parejas: $\frac{6}{36}=" + B(L1[1]) + "$",
      r"(2,6), (3,4), (4,3), (6,2): $" + B(L1[2]) + "$", r"$3\cdot3=9$ parejas: $" + B(L1[3]) + "$", r"$6+4+2=12$ parejas: $" + B(L1[4]) + "$"])),
 (2, r"\pau{Islas Baleares, PBAU julio 2018} Un dado está cargado de manera que la probabilidad de obtener un 6 es $\frac12$ y las probabilidades de obtener cada una de las otras caras son iguales a $p$. Se lanza este dado; calcula la probabilidad de cada uno de los sucesos siguientes:" + tasks(2, [
      r"Se obtiene un dos.", r"No se obtiene un tres.", r"Se obtiene un número par.", r"Se obtiene un número impar."]),
     r"$5p+\frac12=1\Rightarrow p=\frac{1}{10}$." + tasks(2, [r"$" + B(ck(pk, F(1, 10))) + "$", r"$1-\frac1{10}=" + B(ck(1 - pk, F(9, 10))) + "$",
      r"$\frac1{10}+\frac1{10}+\frac12=" + B(ck(2 * pk + F(1, 2), F(7, 10))) + "$", r"$3\cdot\frac1{10}=" + B(ck(3 * pk, F(3, 10))) + "$"])),
 (2, r"\pau{Andalucía, PEvAU ordinaria 2023} Tenemos una moneda trucada en la que la probabilidad de obtener cara es el doble que la de obtener cruz." + tasks(1, [
      r"Calcula la probabilidad de obtener cara al lanzar la moneda.", r"Calcula la probabilidad de obtener una cara y una cruz, sin importar el orden, al lanzar dos veces la moneda.",
      r"Calcula la probabilidad de obtener al menos una cara al lanzar dos veces la moneda."]),
     r"$P(C)=2P({+})$ y $P(C)+P({+})=1$." + tasks(1, [r"$3P({+})=1\Rightarrow P(C)=" + B(ck(F(2, 3), F(2, 3))) + "$",
      r"$P(C{+})+P({+}C)=2\cdot\frac23\cdot\frac13=" + B(ck(2 * F(2, 3) * F(1, 3), F(4, 9))) + "$ (los resultados ya no son equiprobables: multiplicamos)",
      r"$1-P({+}{+})=1-\frac19=" + B(ck(1 - F(1, 9), F(8, 9))) + "$"])),
 (1, r"Elegimos al azar un número del 1 al 100. Calcula la probabilidad de que sea múltiplo de 3 o de 5.",
     r"Hay 33 múltiplos de 3, 20 de 5 y 6 de 15 (contados dos veces): $P=\frac{33+20-6}{100}=" + B(ck(F(sum(1 for k in range(1, 101) if k % 3 == 0 or k % 5 == 0), 100), F(47, 100))) + "$."),
 (1, r"Lanzamos tres monedas. Calcula la probabilidad de obtener exactamente dos caras y la de obtener más caras que cruces.",
     r"De las 8 ternas, tienen dos caras $CC{+}$, $C{+}C$ y ${+}CC$: $" + B(ck(F(sum(1 for m in M3 if m.count('C') == 2), 8), F(3, 8))) + "$. Más caras que cruces (2 o 3 caras): $\\frac{3+1}{8}=" + B(ck(F(sum(1 for m in M3 if m.count('C') >= 2), 8), F(1, 2))) + "$."),
 (2, r"Razona si las afirmaciones siguientes son verdaderas o falsas:" + tasks(1, [r"Si lanzamos dos dados y sumamos, la probabilidad de cada suma es $\frac1{11}$, porque hay 11 sumas posibles.",
      r"Si una moneda equilibrada ha salido cara cinco veces seguidas, es más probable que la sexta vez salga cruz.", r"Puede ser que $P(A)=1{,}2$ si $A$ es un suceso muy probable."]),
     tasks(1, [r"\rest{Falsa}: las sumas no son equiprobables (el 7 tiene 6 parejas y el 2 solo una). Debemos aplicar Laplace a las 36 parejas.",
               r"\rest{Falsa}: los lanzamientos son independientes; la probabilidad sigue siendo $\frac12$.", r"\rest{Falsa}: toda probabilidad está entre 0 y 1."])),
]))

# =====================================================================
# 3. Fórmules
a, b, u = F('0.45'), F('0.3'), F('0.6'); i3 = a + b - u
ck([i3, 1 - u, a - i3, 1 - i3, u - i3], [F('0.15'), F('0.4'), F('0.3'), F('0.85'), F('0.45')])
ma, mb, mu = F('0.4'), F('0.6'), F('0.8'); mi = ma + mb - mu
nA, nB, nAuB = F('0.7'), F('0.4'), F('0.9'); a18, b18, i18 = 1 - nA, 1 - nB, 1 - nAuB
S.append(("Fórmulas de la probabilidad", [
 (1, r"Sean $A$ y $B$ dos sucesos con $P(A)=0{,}45$, $P(B)=0{,}3$ y $P(A\cup B)=0{,}6$. Calcula:" + tasks(3, [r"$P(A\cap B)$", r"$P(\co A\cap\co B)$", r"$P(A\cap\co B)$", r"$P(\co A\cup\co B)$", r"$P(\text{solo uno de los dos})$"])
     + recorda(r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$; \ $P(\co A)=1-P(A)$; \ $P(A\cap\co B)=P(A)-P(A\cap B)$; \ De Morgan: $\co A\cap\co B=\overline{A\cup B}$ y $\co A\cup\co B=\overline{A\cap B}$."),
     tasks(2, [r"$0{,}45+0{,}3-0{,}6=" + B(i3) + "$", r"$1-0{,}6=" + B(1 - u) + "$", r"$0{,}45-0{,}15=" + B(a - i3) + "$", r"$1-0{,}15=" + B(1 - i3) + "$", r"$0{,}6-0{,}15=" + B(u - i3) + "$"])
     + cen(venn(a - i3, i3, b - i3, 1 - u))),
 (1, r"\pau{Madrid, EvAU julio 2018} Sean $A$ y $B$ dos sucesos de un experimento aleatorio tales que $P(A)=0{,}4$, $P(B)=0{,}6$ y $P(A\cup B)=0{,}8$. Calcula $P(\co A\cap B)$ y $P(\co A\cup\co B)$.",
     r"$P(A\cap B)=0{,}4+0{,}6-0{,}8=0{,}2$. \ $P(\co A\cap B)=P(B)-P(A\cap B)=" + B(ck(mb - mi, F('0.4'))) + r"$; \ $P(\co A\cup\co B)=1-P(A\cap B)=" + B(1 - mi) + "$."),
 (1, r"De dos sucesos se sabe que $P(\co A)=0{,}7$, $P(\co B)=0{,}4$ y $P(\co A\cup\co B)=0{,}9$. Calcula $P(A)$, $P(B)$, $P(A\cap B)$, $P(A\cup B)$ y $P(\co A\cap\co B)$.",
     r"$P(A)=" + B(a18) + r"$, $P(B)=" + B(b18) + r"$. De Morgan: $P(A\cap B)=1-P(\co A\cup\co B)=" + B(i18) + r"$; \ $P(A\cup B)=0{,}3+0{,}6-0{,}1=" + B(a18 + b18 - i18) + r"$; \ $P(\co A\cap\co B)=1-0{,}8=" + B(ck(1 - (a18 + b18 - i18), F('0.2'))) + "$."),
 (1, r"Los sucesos $A$ y $B$ son incompatibles, con $P(A)=0{,}35$ y $P(B)=0{,}4$. Calcula $P(A\cup B)$, $P(\co A\cap\co B)$, $P(A\cap\co B)$ y $P(\co A\cup\co B)$.",
     r"$P(A\cap B)=0$: $P(A\cup B)=" + B(F('0.75')) + r"$; \ $P(\co A\cap\co B)=" + B(F('0.25')) + r"$; \ $P(A\cap\co B)=P(A)=" + B(F('0.35')) + r"$; \ $P(\co A\cup\co B)=1-0=\res{1}$."),
 (2, r"Sean $A$ y $B$ dos sucesos con $P(A)=0{,}6$ y $P(B)=0{,}7$." + tasks(1, [r"¿Pueden ser incompatibles?", r"¿Entre qué valores puede estar $P(A\cap B)$?", r"¿Y $P(A\cup B)$?"]),
     tasks(1, [r"\rest{No}: si lo fueran, $P(A\cup B)=0{,}6+0{,}7=1{,}3>1$.", r"Como $P(A\cup B)\leq1$, $P(A\cap B)=1{,}3-P(A\cup B)\geq0{,}3$; y $A\cap B\subset A$, así que $P(A\cap B)\leq0{,}6$: \ $\res{0{,}3\leq P(A\cap B)\leq0{,}6}$.",
               r"$P(A\cup B)=1{,}3-P(A\cap B)$: \ $\res{0{,}7\leq P(A\cup B)\leq1}$."])),
 (2, r"Tres sucesos $A$, $B$ y $C$ tienen probabilidad $0{,}4$ cada uno; las intersecciones de dos en dos tienen probabilidad $0{,}15$ y $P(A\cap B\cap C)=0{,}05$. Calcula la probabilidad de que ocurra al menos uno y de que no ocurra ninguno.",
     r"$P(A\cup B\cup C)=3\cdot0{,}4-3\cdot0{,}15+0{,}05=" + B(ck(3 * F('0.4') - 3 * F('0.15') + F('0.05'), F('0.8'))) + r"$; \ $P(\text{ninguno})=1-0{,}8=" + B(F('0.2')) + "$."),
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
S.append(("Cálculo de probabilidades conociendo el espacio muestral y sin conocerlo", [
 (1, r"Lanzamos dos dados y consideramos los sucesos $A=$«la suma es par» y $B=$«al menos uno de los dados es un 6». Calcula $P(A)$, $P(B)$ y $P(A\cap B)$ por recuento y, con la fórmula, $P(A\cup B)$. Comprueba el resultado contando los casos de $A\cup B$.",
     r"$P(A)=\frac{18}{36}=" + B(pA) + r"$, \ $P(B)=" + B(pB) + r"$, \ $A\cap B=\{(2,6),(4,6),(6,6),(6,2),(6,4)\}$: $P(A\cap B)=" + B(pAB) + r"$." +
     r"\par $P(A\cup B)=\frac{18+11-5}{36}=\frac{24}{36}=" + B(pU) + r"$. Contando: las 18 parejas de suma par más las 6 con un 6 y suma impar, $(1,6),(3,6),(5,6),(6,1),(6,3),(6,5)$: 24 casos. \rest{Coincide.}"),
 (1, r"Sacamos al azar una tarjeta de una caja con tarjetas numeradas del 1 al 30. Sean $A=$«el número es par» y $B=$«el número es múltiplo de 3». Calcula, aplicando las fórmulas, la probabilidad de que sea par o múltiplo de 3, de que cumpla solo una de las dos condiciones y de que no cumpla ninguna.",
     r"$P(A)=\frac{15}{30}$, $P(B)=\frac{10}{30}$, $P(A\cap B)=P(\text{múltiplo de 6})=\frac{5}{30}$." + tasks(1, [r"$P(A\cup B)=\frac{15+10-5}{30}=" + B(q2) + "$",
      r"$P(A\cup B)-P(A\cap B)=\frac{20-5}{30}=" + B(q1) + "$", r"$1-P(A\cup B)=" + B(1 - q2) + "$"])),
 (1, r"\pau{Galicia, ABAU extraordinaria 2024} En una encuesta, el 80\,\% de los entrevistados dice que lee o escucha música, el 35\,\% hace las dos cosas y el 60\,\% no lee. Calcula las probabilidades de que una persona elegida al azar:" + tasks(1, [
      r"escuche música y no lea;", r"lea y no escuche música;", r"haga solo una de las dos cosas."]),
     r"$P(L)=1-0{,}6=0{,}4$ y $P(M)=0{,}8-0{,}4+0{,}35=0{,}75$." + tasks(1, [r"$P(M\cap\co L)=P(M)-P(M\cap L)=" + B(ck(gM - gI, F('0.4'))) + "$", r"$P(L\cap\co M)=0{,}4-0{,}35=" + B(ck(gL - gI, F('0.05'))) + "$",
      r"$0{,}4+0{,}05=" + B(ck(gU - gI, F('0.45'))) + "$"]) + cen(ct(gL, gM, gI, 'L', 'M'))),
 (1, r"\pau{Andalucía, PEvAU ordinaria 2022} En su tiempo libre, el 65\,\% de los estudiantes de un centro juega a videojuegos, el 45\,\% lee libros y el 15\,\% no hace ninguna de las dos cosas. Elegimos un estudiante al azar. Calcula la probabilidad de que:" + tasks(1, [
      r"juegue a videojuegos o lea libros;", r"juegue a videojuegos y no lea libros."]),
     tasks(1, [r"De Morgan: $P(V\cup L)=1-P(\co V\cap\co L)=1-0{,}15=" + B(ck(vU, F('0.85'))) + "$", r"$P(V\cap L)=0{,}65+0{,}45-0{,}85=0{,}25\Rightarrow P(V\cap\co L)=0{,}65-0{,}25=" + B(ck(vV - vI, F('0.4'))) + "$"])
     + cen(ct(vV, vL, vI, 'V', 'L'))),
 (1, r"En una ciudad, el 55\,\% de los habitantes lee la prensa, el 40\,\% ve las noticias en la televisión y el 25\,\% no hace ninguna de las dos cosas. Construye la tabla de contingencia y calcula la probabilidad de que un habitante elegido al azar:" + tasks(2, [
      r"haga las dos cosas;", r"solo lea la prensa;", r"haga solo una de las dos;", r"lea la prensa o no vea la televisión."]),
     cen(ct(pP, pT, pI, 'P', 'T')) + tasks(2, [r"$" + B(ck(pI, F('0.2'))) + "$", r"$" + B(pP - pI) + "$", r"$0{,}35+0{,}2=" + B(pP - pI + pT - pI) + "$", r"$1-P(\co P\cap T)=1-0{,}2=" + B(1 - (pT - pI)) + "$"])),
 (1, r"En un grupo de 30 personas, 18 hablan inglés, 12 francés y 6 no hablan ninguno de los dos idiomas. Elegimos una persona al azar. Calcula la probabilidad de que hable los dos idiomas, de que hable solo uno y de que hable francés pero no inglés.",
     r"Hablan algún idioma $30-6=24$; los dos: $18+12-24=6$." + tasks(3, [r"$\frac{6}{30}=" + B(F(6, 30)) + "$", r"$\frac{24-6}{30}=" + B(F(18, 30)) + "$", r"$\frac{12-6}{30}=" + B(F(6, 30)) + "$"])
     + cen(taula(['I', r'\overline{I}'], ['F', r'\overline{F}'], [[6, 12, 18], [6, 6, 12], [12, 18, 30]], str))),
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
mur = {'Veterinaria': (30, 10), 'Economía': (25, 12), 'Química': (20, 13), 'Biología': (15, 8), 'Matemáticas': (10, 6)}
dones = sum(v[1] for v in mur.values()); homes = 100 - dones
ex39 = F('0.6') * F('0.5'); ex39b = ex39 + F('0.4') * F('0.25')
S.append(("Probabilidad condicionada", [
 (1, r"Sean $A$ y $B$ dos sucesos con $P(A)=0{,}5$, $P(B)=0{,}4$ y $P(A\cap B)=0{,}1$. Calcula:" + tasks(3, [r"$P(A\cond B)$", r"$P(B\cond A)$", r"$P(A\cond\co B)$", r"$P(\co A\cond\co B)$", r"$P(B\cond\co A)$", r"$P(\co B\cond A)$"])
     + recorda(r"$P(A\cond B)=\dfrac{P(A\cap B)}{P(B)}$. El suceso que va detrás de la barra es la condición: va en el denominador."),
     tasks(3, [r"$\frac{0{,}1}{0{,}4}=" + B(c_i / c_b) + "$", r"$\frac{0{,}1}{0{,}5}=" + B(c_i / c_a) + "$", r"$\frac{0{,}4}{0{,}6}=" + B((c_a - c_i) / (1 - c_b)) + "$",
               r"$\frac{0{,}2}{0{,}6}=" + B((1 - c_u) / (1 - c_b)) + "$", r"$\frac{0{,}3}{0{,}5}=" + B((c_b - c_i) / (1 - c_a)) + "$", r"$1-0{,}2=" + B(1 - c_i / c_a) + "$"])
     + cen(venn(c_a - c_i, c_i, c_b - c_i, 1 - c_u))),
 (2, r"\pau{Madrid, EvAU julio 2019} Sean $A$ y $B$ dos sucesos con $P(A)=0{,}3$, $P(B\cond A)=0{,}4$ y $P(B\cond\co A)=0{,}6$. Calcula:" + tasks(2, [r"$P(A\cond B)$", r"$P(\co A\cond\co B)$"]),
     r"$P(A\cap B)=0{,}3\cdot0{,}4=0{,}12$; \ $P(\co A\cap B)=0{,}7\cdot0{,}6=0{,}42$; \ $P(B)=0{,}54$; \ $P(\co A\cap\co B)=0{,}7-0{,}42=0{,}28$." +
     tasks(2, [r"$\frac{0{,}12}{0{,}54}=" + B(m19ab / m19b) + "$", r"$\frac{0{,}28}{0{,}46}=" + B((1 - m19 - m19nab) / (1 - m19b)) + "$"])),
 (1, r"\pau{Islas Baleares, PBAU septiembre 2017} Sean $A$ y $B$ dos sucesos con probabilidades $0{,}4$ y $0{,}6$, respectivamente. Se sabe que, dado $B$, la probabilidad de que ocurra $A$ es $0{,}3$." + tasks(1, [
      r"¿Cuál es la probabilidad de que ocurran ambos sucesos a la vez?", r"¿Cuál es la probabilidad de que ocurra alguno de los dos?", r"¿Cuál es la probabilidad de que no ocurra ninguno?"]),
     tasks(1, [r"$P(A\cap B)=P(B)\,P(A\cond B)=0{,}6\cdot0{,}3=" + B(ck(b17, F('0.18'))) + "$", r"$0{,}4+0{,}6-0{,}18=" + B(ck(F('0.4') + F('0.6') - b17, F('0.82'))) + "$", r"$1-0{,}82=" + B(ck(b17, F('0.18'))) + "$"])),
 (1, r"\pau{Andalucía, PEvAU junio 2017} El 90\,\% de los alumnos de un centro está interesado por las redes sociales, el 60\,\% por sus notas y el 55\,\% por las dos cosas. Se elige un alumno al azar." + tasks(1, [
      r"¿Cuál es la probabilidad de que esté interesado por alguna de las dos cosas?", r"Calcula la probabilidad de que esté interesado por las notas, sabiendo que no está interesado por las redes sociales.", r"Calcula la probabilidad de que no esté interesado por ninguna de las dos cosas."]),
     cen(ct(F('0.9'), F('0.6'), r17, 'R', 'N')) + tasks(1, [r"$0{,}9+0{,}6-0{,}55=" + B(ck(r17u, F('0.95'))) + "$", r"$P(N\cond\co R)=\frac{P(N\cap\co R)}{P(\co R)}=\frac{0{,}05}{0{,}1}=" + B(ck(F('0.05') / F('0.1'), F('0.5'))) + "$",
      r"$1-0{,}95=" + B(ck(1 - r17u, F('0.05'))) + "$"])),
 (2, r"\pau{Andalucía, PEvAU ordinaria 2020} A 120 estudiantes se les ha recomendado la lectura de dos libros: 46 han leído el primero, 34 el segundo y 16 los dos. Se elige un estudiante al azar. Calcula la probabilidad de que:" + tasks(1, [
      r"haya leído alguno de los dos libros;", r"no haya leído ninguno;", r"solo haya leído el primero;", r"haya leído el primero, si se sabe que no ha leído el segundo."]),
     cen(taula(['L_1', r'\overline{L_1}'], ['L_2', r'\overline{L_2}'], [[16, 30, 46], [18, 56, 74], [34, 86, 120]], str)) +
     tasks(2, [r"$\frac{64}{120}=" + B(ck(l20u, F(8, 15))) + "$", r"$\frac{56}{120}=" + B(ck(1 - l20u, F(7, 15))) + "$", r"$\frac{30}{120}=" + B(ck(l20[0] - l20[2], F(1, 4))) + "$",
               r"$P(L_1\cond\co L_2)=\frac{30}{86}=" + B(ck((l20[0] - l20[2]) / (1 - l20[1]), F(15, 43))) + "$"])),
 (2, r"\pau{Andalucía, PEvAU ordinaria 2021} De las compras realizadas en las últimas rebajas, el 55\,\% fueron de productos electrónicos y el 72\,\% se hicieron por Internet; de las compras hechas por Internet, el 64\,\% fueron de productos electrónicos. Se elige una compra al azar. Calcula la probabilidad de que:" + tasks(1, [
      r"haya sido de productos electrónicos y hecha por Internet;", r"se haya hecho por Internet o haya sido de productos electrónicos;", r"no se haya hecho por Internet, sabiendo que no fue de productos electrónicos."]),
     tasks(1, [r"$P(E\cap I)=P(I)\,P(E\cond I)=0{,}72\cdot0{,}64=" + B(ck(i21, F('0.4608'))) + "$", r"$0{,}55+0{,}72-0{,}4608=" + B(ck(i21u, F('0.8092'))) + "$",
               r"$P(\co I\cond\co E)=\frac{P(\co I\cap\co E)}{P(\co E)}=\frac{1-0{,}8092}{0{,}45}=" + B(ck((1 - i21u) / F('0.45'), F(53, 125))) + "$"])),
 (2, r"\pau{Murcia, PAU extraordinaria 2025} En una encuesta a 100 estudiantes de segundo de Bachillerato, 30 quieren estudiar Veterinaria, 25 Economía, 20 Química, 15 Biología y 10 Matemáticas. De ellos, 10, 12, 13, 8 y 6 son mujeres, respectivamente. Nadie se puede matricular en más de un grado. Elegimos un estudiante al azar. Calcula la probabilidad de que:" + tasks(2, [
      r"sea mujer;", r"sea hombre y quiera estudiar Veterinaria;", r"quiera estudiar Química o Veterinaria;", r"no quiera estudiar ni Biología ni Matemáticas;", r"quiera estudiar Química, si es mujer;", r"quiera estudiar Economía, si es hombre."]),
     cen(taula(['M', 'H'], [r'\text{Vet.}', r'\text{Eco.}', r'\text{Quím.}', r'\text{Bio.}', r'\text{Mat.}'], [[v[1] for v in mur.values()] + [dones], [v[0] - v[1] for v in mur.values()] + [homes], [v[0] for v in mur.values()] + [100]], str)) +
     tasks(3, [r"$" + B(ck(F(dones, 100), F('0.49'))) + "$", r"$\frac{20}{100}=" + B(ck(F(30 - 10, 100), F('0.2'))) + "$", r"$\frac{50}{100}=" + B(ck(F(50, 100), F('0.5'))) + "$",
               r"$\frac{75}{100}=" + B(ck(F(100 - 25, 100), F('0.75'))) + "$", r"$\frac{13}{49}=" + B(ck(F(13, dones), F(13, 49))) + "$", r"$\frac{13}{51}=" + B(ck(F(25 - 12, homes), F(13, 51))) + "$"])),
 (2, r"De dos sucesos se sabe que $P(A)=0{,}6$, $P(B\cond A)=0{,}5$ y $P(B\cond\co A)=0{,}25$. Calcula $P(A\cap B)$, $P(B)$, $P(A\cond B)$ y $P(A\cup B)$.",
     r"$P(A\cap B)=0{,}6\cdot0{,}5=" + B(ex39) + r"$; \ $P(\co A\cap B)=0{,}4\cdot0{,}25=0{,}1$, \ $P(B)=" + B(ex39b) + r"$; \ $P(A\cond B)=\frac{0{,}3}{0{,}4}=" + B(ex39 / ex39b) + r"$; \ $P(A\cup B)=0{,}6+0{,}4-0{,}3=" + B(F('0.6') + ex39b - ex39) + "$."),
]))

# =====================================================================
# 6. Independència
g20 = F('0.4') * F('0.75')
o24 = F('0.11') / F('0.275')
v17 = (F('0.2') - F('0.03')) / F('0.4')
s13 = {(x, y) for x, y in D2 if x + y == 3}; s13u = {(x, y) for x, y in D2 if 1 in (x, y)}
pC13, pAB13, pI13 = F(len(s13), 36), F(len(s13u), 36), F(len(s13 & s13u), 36)
S.append(("Independencia de sucesos", [
 (1, r"Los sucesos $A$ y $B$ son independientes, con $P(A)=0{,}3$ y $P(B)=0{,}5$. Calcula $P(A\cap B)$, $P(A\cup B)$, $P(\co A\cap\co B)$, $P(A\cond B)$ y $P(A\cap\co B)$."
     + recorda(r"$A$ y $B$ son independientes si $P(A\cap B)=P(A)\cdot P(B)$. Entonces también lo son $A$ y $\co B$, $\co A$ y $B$, y $\co A$ y $\co B$."),
     r"$P(A\cap B)=0{,}3\cdot0{,}5=" + B(F('0.15')) + r"$; \ $P(A\cup B)=0{,}3+0{,}5-0{,}15=" + B(F('0.65')) + r"$; \ $P(\co A\cap\co B)=0{,}7\cdot0{,}5=" + B(F('0.35')) + r"$; \ $P(A\cond B)=P(A)=" + B(F('0.3')) + r"$; \ $P(A\cap\co B)=0{,}3\cdot0{,}5=" + B(F('0.15')) + "$."),
 (2, r"Se sabe que $P(A)=0{,}4$ y $P(A\cup B)=0{,}7$. Calcula $P(B)$ si:" + tasks(2, [r"$A$ y $B$ son incompatibles;", r"$A$ y $B$ son independientes."]),
     tasks(2, [r"$0{,}7=0{,}4+P(B)\Rightarrow P(B)=" + B(F('0.3')) + "$", r"$0{,}7=0{,}4+p-0{,}4p\Rightarrow0{,}6p=0{,}3\Rightarrow p=" + B(ck(F('0.3') / F('0.6'), F('0.5'))) + "$"])),
 (1, r"\pau{Madrid, EvAU extraordinaria 2021} Sean $A$ y $B$ dos sucesos con $P(A)=0{,}5$, $P(B)=0{,}8$ y $P(A\cup B)=0{,}9$." + tasks(1, [r"Estudia si los sucesos $A$ y $B$ son independientes.", r"Calcula $P(A\cond\co B)$."]),
     tasks(1, [r"$P(A\cap B)=0{,}5+0{,}8-0{,}9=0{,}4=0{,}5\cdot0{,}8$: \rest{son independientes}.", r"$\frac{P(A\cap\co B)}{P(\co B)}=\frac{0{,}1}{0{,}2}=" + B(ck(F('0.1') / F('0.2'), F('0.5'))) + "$ ($=P(A)$, como tenía que ser)."])),
 (1, r"\pau{Castilla-La Mancha, EvAU septiembre 2017} De un estudio sobre accidentes de tráfico se dedujo que el 29\,\% de los conductores superaban los límites de alcohol en sangre, el 14\,\% tenían presencia de drogas en sangre y el 37\,\% superaban los límites de alcohol o tenían presencia de drogas (o ambas cosas)." + tasks(1, [
      r"Calcula la probabilidad de que, en un accidente, el conductor supere los límites de alcohol y tenga presencia de drogas en sangre.", r"Razona si son independientes los sucesos «superar los límites de alcohol» y «presencia de drogas en sangre»."]),
     tasks(1, [r"$0{,}29+0{,}14-0{,}37=" + B(ck(F('0.29') + F('0.14') - F('0.37'), F('0.06'))) + "$", r"$0{,}29\cdot0{,}14=0{,}0406\neq0{,}06$: \rest{no son independientes}."])),
 (2, r"\pau{Galicia, ABAU ordinaria 2020} Sean $A$ y $B$ dos sucesos con $P(A)=0{,}4$, $P(B)=0{,}7$ y $P(B\cond A)=0{,}75$. Calcula:" + tasks(2, [r"$P(A\cap B)$", r"$P(A\cup\co B)$", r"$P(A\cap\co B)$", r"¿Son independientes?"]),
     tasks(1, [r"$0{,}4\cdot0{,}75=" + B(ck(g20, F('0.3'))) + "$", r"$1-P(\co A\cap B)=1-(0{,}7-0{,}3)=" + B(ck(1 - (F('0.7') - g20), F('0.6'))) + "$", r"$0{,}4-0{,}3=" + B(ck(F('0.4') - g20, F('0.1'))) + "$",
               r"$P(A)P(B)=0{,}28\neq0{,}3$ (o bien $P(B\cond A)=0{,}75\neq P(B)$): \rest{no son independientes}."])),
 (1, r"\pau{Andalucía, PEvAU septiembre 2018} En una localidad, el 25\,\% de los habitantes va periódicamente al dentista, el 10\,\% se hace una analítica y el 8\,\% hace las dos cosas." + tasks(1, [
      r"Razona si los sucesos «ir al dentista» y «hacerse una analítica» son independientes.", r"¿Qué porcentaje de habitantes ni se hace una analítica ni va al dentista?", r"Si elegimos al azar un habitante de entre los que van al dentista, ¿cuál es la probabilidad de que se haga una analítica?"]),
     tasks(1, [r"$0{,}25\cdot0{,}1=0{,}025\neq0{,}08$: \rest{no son independientes}.", r"$1-(0{,}25+0{,}1-0{,}08)=0{,}73$: \ $\res{73\,\%}$", r"$P(An\cond D)=\frac{0{,}08}{0{,}25}=" + B(ck(F('0.08') / F('0.25'), F('0.32'))) + "$"])),
 (1, r"\pau{La Rioja, EBAU ordinaria 2020} En una clase hay 24 estudiantes: 12 han aprobado inglés, 16 han aprobado matemáticas y 4 han suspendido las dos asignaturas." + tasks(1, [
      r"¿Cuál es la probabilidad de que un alumno elegido al azar haya aprobado matemáticas y suspendido inglés?", r"¿Cuál es la probabilidad de que haya aprobado las dos asignaturas?", r"¿Son independientes los sucesos «aprobar matemáticas» y «aprobar inglés»?"]),
     r"Aprueban alguna $24-4=20$; las dos: $12+16-20=8$." + cen(taula(['M', r'\overline{M}'], ['I', r'\overline{I}'], [[8, 8, 16], [4, 4, 8], [12, 12, 24]], str)) +
     tasks(1, [r"$\frac{8}{24}=" + B(ck(F(16 - 8, 24), F(1, 3))) + "$", r"$\frac{8}{24}=" + B(F(8, 24)) + "$", r"$P(M)P(I)=\frac{16}{24}\cdot\frac{12}{24}=\frac13=P(M\cap I)$: \rest{sí son independientes}."])
     + ('' if ck(F(16, 24) * F(12, 24), F(8, 24)) else '')),
 (2, r"\pau{Galicia, ABAU ordinaria 2024} Se estima que en una población el 20\,\% padece obesidad y que el 11\,\% padece obesidad y es hipertenso. Además, el 27,5\,\% de los hipertensos padece obesidad." + tasks(1, [
      r"¿Qué porcentaje de la población padece obesidad o es hipertenso?", r"¿Son independientes los sucesos «padecer obesidad» y «ser hipertenso»?", r"Calcula la probabilidad de que un individuo que no padece obesidad sea hipertenso."]),
     r"$P(O\cap H)=P(H)\,P(O\cond H)\Rightarrow P(H)=\frac{0{,}11}{0{,}275}=" + N(o24) + "$." +
     tasks(1, [r"$0{,}2+0{,}4-0{,}11=0{,}49$: \ $\res{49\,\%}$" + ('' if ck(F('0.2') + o24 - F('0.11'), F('0.49')) else ''), r"$0{,}2\cdot0{,}4=0{,}08\neq0{,}11$: \rest{no son independientes}.",
               r"$P(H\cond\co O)=\frac{0{,}4-0{,}11}{0{,}8}=" + B(ck((o24 - F('0.11')) / F('0.8'), F('0.3625'))) + "$"])),
 (2, r"\pau{Galicia, ABAU septiembre 2017} El 60\,\% de los individuos de una población están vacunados contra una enfermedad. Durante una epidemia, el 20\,\% contrajo la enfermedad y el 3\,\% está vacunado y la contrajo." + tasks(1, [
      r"Calcula el porcentaje de individuos que han contraído la enfermedad entre los que no están vacunados.", r"Calcula el porcentaje de vacunados entre los que contrajeron la enfermedad. Justifica si los sucesos «estar vacunado» y «contraer la enfermedad» son dependientes o independientes."]),
     tasks(1, [r"$P(M\cond\co V)=\frac{0{,}2-0{,}03}{0{,}4}=" + N(ck(v17, F('0.425'))) + r"$: \ $\res{42{,}5\,\%}$", r"$P(V\cond M)=\frac{0{,}03}{0{,}2}=0{,}15$: \ $\res{15\,\%}$. Como $P(V\cond M)=0{,}15\neq P(V)=0{,}6$, \rest{son dependientes}."])),
 (2, r"\pau{Madrid, PAU ordinaria 2025} De tres sucesos $A$, $B$ y $C$ se sabe que $A$ y $C$ son disjuntos (incompatibles), $A$ y $B$ son independientes, $P(A)=0{,}25$, $P(B)=0{,}2$ y $P(B\cap C)=0{,}05$." + tasks(1, [
      r"Calcula la probabilidad de que ocurra al menos uno de los sucesos $A$ o $B$.", r"Calcula $P(\co B\cup\co C)$.", r"¿Pueden ser independientes los sucesos $A$ y $C$?"]),
     tasks(1, [r"$P(A\cup B)=0{,}25+0{,}2-0{,}25\cdot0{,}2=" + B(ck(F('0.25') + F('0.2') - F('0.05'), F('0.4'))) + "$", r"De Morgan: $1-P(B\cap C)=" + B(F('0.95')) + "$",
               r"Como $P(B\cap C)>0$, $P(C)>0$; si fueran independientes, $P(A\cap C)=0{,}25\,P(C)>0$, pero es 0 porque son disjuntos: \rest{no pueden ser independientes}."])),
 (1, r"\pau{País Vasco, EAU extraordinaria 2022} Deiene y Kattalin son jugadoras de baloncesto. Deiene encesta 2 de cada 5 tiros y Kattalin 3 de cada 7. Si ambas tiran a canasta una sola vez, calcula la probabilidad de que:" + tasks(2, [
      r"las dos encesten;", r"no enceste ninguna;", r"solo enceste Deiene;", r"enceste al menos una."]),
     r"Los tiros son independientes: multiplicamos." + tasks(2, [r"$\frac25\cdot\frac37=" + B(ck(F(2, 5) * F(3, 7), F(6, 35))) + "$", r"$\frac35\cdot\frac47=" + B(ck(F(3, 5) * F(4, 7), F(12, 35))) + "$",
      r"$\frac25\cdot\frac47=" + B(ck(F(2, 5) * F(4, 7), F(8, 35))) + "$", r"$1-\frac{12}{35}=" + B(F(23, 35)) + "$"])),
 (2, r"\pau{Islas Baleares, PBAU extraordinaria 2023} Tiramos dos dados no trucados y consideramos los sucesos $A=$«en el primer dado ha salido un 1», $B=$«en el segundo dado ha salido un 1» y $C=$«la suma de los dos dados es 3»." + tasks(1, [
      r"Calcula $P(A)$.", r"Calcula $P(A\cup B)$.", r"¿Son independientes los sucesos $C$ y $A\cup B$?"]),
     tasks(1, [r"$\frac{6}{36}=" + B(F(1, 6)) + "$", r"$\frac{6+6-1}{36}=" + B(ck(pAB13, F(11, 36))) + "$",
               r"$C=\{(1,2),(2,1)\}\subset A\cup B$, así que $P(C\cap(A\cup B))=P(C)=\frac{2}{36}$, pero $P(C)\,P(A\cup B)=\frac{2}{36}\cdot\frac{11}{36}\neq\frac{2}{36}$: \rest{no son independientes}."])
     + ('' if ck(pI13, pC13) else '')),
 (2, r"Razona si las afirmaciones siguientes son verdaderas o falsas:" + tasks(1, [r"Dos sucesos incompatibles (con probabilidades no nulas) son independientes.",
      r"Si $A$ y $B$ son independientes, entonces $\co A$ y $\co B$ también lo son.", r"Si $P(A\cond B)=P(A)$, entonces $P(B\cond A)=P(B)$."]),
     tasks(1, [r"\rest{Falsa}: $P(A\cap B)=0$, pero $P(A)P(B)>0$. Si ocurre uno, seguro que no ocurre el otro: dependen el uno del otro.",
               r"\rest{Verdadera}: $P(\co A\cap\co B)=1-P(A\cup B)=1-P(A)-P(B)+P(A)P(B)=(1-P(A))(1-P(B))=P(\co A)P(\co B)$.",
               r"\rest{Verdadera}: $P(A\cond B)=P(A)\iff P(A\cap B)=P(A)P(B)\iff P(B\cond A)=P(B)$."])),
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
S.append(("Experimentos compuestos. Extracciones con y sin reemplazamiento", [
 (1, r"Una urna contiene 4 bolas rojas y 6 azules. Sacamos tres bolas. Calcula la probabilidad de que las tres sean rojas y la probabilidad de que haya exactamente dos rojas:" + tasks(2, [r"con reemplazamiento;", r"sin reemplazamiento."])
     + recorda(r"en un diagrama de árbol, multiplicamos las probabilidades a lo largo de cada camino y sumamos los caminos que forman el suceso. Sin reemplazamiento, la composición de la urna cambia en cada extracción."),
     tasks(1, [r"$0{,}4^3=" + B(w3[0]) + r"$; \ dos rojas: $RRB$, $RBR$, $BRR$: $3\cdot0{,}4^2\cdot0{,}6=" + B(w3[1]) + "$",
               r"$\frac4{10}\cdot\frac39\cdot\frac28=" + B(w3[2]) + r"$; \ dos rojas: $3\cdot\frac{4\cdot3\cdot6}{10\cdot9\cdot8}=" + B(w3[3]) + "$"])),
 (1, r"\pau{Aragón, EvAU extraordinaria 2020} En una bolsa tenemos 8 bolas: 3 blancas, 1 roja y 4 negras. Sacamos dos bolas sin reemplazamiento. Calcula:" + tasks(1, [
      r"La probabilidad de que las dos sean blancas.", r"La probabilidad de que al menos una sea blanca.", r"La probabilidad de que las dos sean del mismo color.", r"La probabilidad de que sean blancas, si se sabe que las dos son del mismo color."]),
     tasks(2, [r"$\frac38\cdot\frac27=" + B(a20[0]) + "$", r"$1-\frac58\cdot\frac47=" + B(a20[1]) + "$", r"$\frac38\cdot\frac27+\frac48\cdot\frac37=" + B(a20[2]) + "$ (dos rojas: imposible)",
               r"$\frac{6/56}{18/56}=" + B(a20[0] / a20[2]) + "$"])),
 (1, r"\pau{País Vasco, EAU junio 2018} En una urna hay 15 bolas blancas y 5 negras. Calcula:" + tasks(1, [
      r"Si sacamos una bola al azar, la probabilidad de que sea blanca.", r"Si sacamos dos al azar, la probabilidad de que ambas sean blancas.", r"Si sacamos una bola y después otra, y la primera es negra, la probabilidad de que la segunda también sea negra.",
      r"Si sacamos una bola y después otra, la probabilidad de que sean de distinto color."]),
     tasks(2, [r"$\frac{15}{20}=" + B(v18[0]) + "$", r"$\frac{15}{20}\cdot\frac{14}{19}=" + B(v18[1]) + "$", r"$\frac{4}{19}\approx" + dec(v18[2]) + r"$ \ ($\res{" + Q(v18[2]) + "}$)",
               r"$\frac{15}{20}\cdot\frac{5}{19}+\frac{5}{20}\cdot\frac{15}{19}=" + B(v18[3]) + "$"])),
 (1, r"\pau{Navarra, EvAU septiembre 2017} Una caja contiene doce bolígrafos, cuatro de los cuales son defectuosos. Se sacan tres de manera sucesiva y sin devolverlos a la caja." + tasks(1, [
      r"Calcula la probabilidad de que ninguno de los tres bolígrafos tenga defectos.", r"Calcula la probabilidad de que al menos uno de los tres sea defectuoso.", r"Calcula la probabilidad de que solo uno sea defectuoso."]),
     tasks(1, [r"$\frac{8}{12}\cdot\frac{7}{11}\cdot\frac{6}{10}=" + B(n17[0]) + "$", r"$1-\frac{14}{55}=" + B(n17[1]) + "$", r"$3\cdot\frac{4}{12}\cdot\frac{8}{11}\cdot\frac{7}{10}=" + B(n17[2]) + r"$ (el defectuoso puede salir en 1.\textsuperscript{er}, 2.\textsuperscript{o} o 3.\textsuperscript{er} lugar)"])),
 (2, r"\pau{Aragón, EvAU junio 2017} En una urna hay 2 bolas blancas, 4 negras y 5 rojas. Se sacan dos, una detrás de otra, sin reemplazamiento. Calcula:" + tasks(1, [
      r"La probabilidad de que las dos sean rojas.", r"La probabilidad de que sean de distinto color.", r"La probabilidad de que la segunda bola sea roja.",
      r"Si $A$ es el suceso «la primera bola es roja» y $B$ el suceso «las dos bolas son del mismo color», ¿son independientes $A$ y $B$?"]),
     tasks(2, [r"$\frac5{11}\cdot\frac4{10}=" + B(a17[0]) + "$", r"$1-\frac{2\cdot1+4\cdot3+5\cdot4}{110}=" + B(a17[1]) + "$",
               r"$\frac{2}{11}\cdot\frac{5}{10}+\frac{4}{11}\cdot\frac{5}{10}+\frac{5}{11}\cdot\frac{4}{10}=" + B(a17[2]) + "$",
               r"$P(A\cap B)=\frac{2}{11}$ y $P(A)P(B)=\frac{5}{11}\cdot\frac{17}{55}=\frac{17}{121}\neq\frac{22}{121}$: \rest{no}"])),
 (2, r"\pau{Andalucía, PEvAU extraordinaria 2023} Una caja contiene 3 fichas verdes, 2 azules y 4 rojas. Un juego consiste en hacer dos extracciones sin reemplazamiento: quien saca dos fichas azules gana el primer premio; quien saca dos verdes, el segundo premio; y quien saca una azul y una de otro color, el tercer premio." + tasks(1, [
      r"Calcula la probabilidad de que un jugador consiga el primer o el segundo premio.", r"Calcula la probabilidad de que un jugador gane el tercer premio.", r"Sabiendo que un jugador ha obtenido premio, ¿cuál es la probabilidad de que haya ganado el tercero?"]),
     tasks(1, [r"$\frac29\cdot\frac18+\frac39\cdot\frac28=\frac{2+6}{72}=" + B(f1 + f2) + "$", r"$\frac29\cdot\frac78+\frac79\cdot\frac28=\frac{28}{72}=" + B(f3) + "$",
               r"$\frac{7/18}{1/9+7/18}=" + B(f3 / (f1 + f2 + f3)) + "$"])),
 (2, r"\pau{La Rioja, EBAU ordinaria 2023} Un bombo de lotería tiene diez bolas numeradas del 0 al 9. Hacemos dos extracciones consecutivas sin reemplazar la primera bola. Consideramos los sucesos $A=$«la primera bola es 0», $B=$«la primera bola es 5» y $C=$«la segunda bola es mayor que la primera». Calcula $P(A)$, $P(B)$, $P(C)$, $P(A\cond C)$ y $P(B\cond C)$.",
     r"$P(A)=P(B)=" + B(F(1, 10)) + r"$. Hay $10\cdot9=90$ parejas y, por simetría, en la mitad la segunda es mayor: $P(C)=\frac{45}{90}=" + B(pc_) + r"$." +
     r"\par $P(A\cond C)=\frac{P(A\cap C)}{P(C)}=\frac{9/90}{1/2}=" + B(pac) + r"$ \ (si la primera es 0, la segunda siempre es mayor); \ $P(B\cond C)=\frac{4/90}{1/2}=" + B(pbc) + "$."),
 (2, r"\pau{País Vasco, EAU extraordinaria 2022} Se van a sortear 4 viajes a Nueva York entre 40 personas con una baraja de 40 cartas: se reparte una carta a cada persona y las que reciben un rey ganan un viaje." + tasks(1, [
      r"Calcula la probabilidad de que gane un viaje la primera persona que recibe la carta.", r"Calcula la probabilidad de que gane un viaje la segunda persona que recibe la carta.", r"Calcula la probabilidad de que ninguna de las dos primeras personas gane un viaje."]),
     tasks(1, [r"$\frac{4}{40}=" + B(k22[0]) + "$", r"$\frac{4}{40}\cdot\frac{3}{39}+\frac{36}{40}\cdot\frac{4}{39}=" + B(k22[1]) + "$ (como la primera: el orden no favorece a nadie)", r"$\frac{36}{40}\cdot\frac{35}{39}=" + B(k22[2]) + "$"])),
 (2, r"\pau{Murcia, EBAU junio 2017} Una urna contiene tres bolas numeradas del 1 al 3. Se sacan sucesivamente las tres bolas." + tasks(1, [
      r"Calcula la probabilidad de que las dos últimas bolas extraídas sean impares.", r"Determina si son independientes los sucesos $S_1=$«sale el número par antes que alguno de los impares» y $S_2=$«los dos números impares salen consecutivamente»."]),
     r"Hay $3!=6$ órdenes equiprobables." + tasks(1, [r"Las dos últimas son impares si el 2 sale el primero: $\frac26=" + B(m17a) + "$",
      r"$S_1$: el 2 no es el último, $P(S_1)=\frac46$; $S_2$: el 2 es el primero o el último, $P(S_2)=\frac46$; $S_1\cap S_2$: el 2 es el primero, $\frac26$. Como $\frac46\cdot\frac46=\frac49\neq\frac13$, \rest{son dependientes}."])),
 (2, r"\pau{Aragón, EvAU septiembre 2019} Una empresa tiene 64 trabajadores repartidos en tres departamentos. Se ha estudiado si saben inglés o no:" + cen(taula([r'\text{Sabe inglés}', r'\text{No sabe}'], [r'\text{Admin.}', r'\text{Producción}', r'\text{Ventas}'], [[12, 30, 6, 48], [4, 11, 1, 16], [16, 41, 7, 64]], str)) + tasks(1, [
      r"Elegimos al azar un trabajador. ¿Cuál es la probabilidad de que sepa inglés?", r"Elegimos al azar un trabajador de entre los que saben inglés. ¿Cuál es la probabilidad de que sea del departamento de Ventas?",
      r"Sean $A=$«ser de Administración» y $B=$«saber inglés». ¿Son independientes?", r"Elegimos al azar tres trabajadores (sin reemplazamiento). ¿Cuál es la probabilidad de que sean del mismo departamento?"]),
     tasks(1, [r"$\frac{48}{64}=" + B(F(48, 64)) + "$", r"$\frac{6}{48}=" + B(F(6, 48)) + "$", r"$P(A\cap B)=\frac{12}{64}=\frac{3}{16}$ y $P(A)P(B)=\frac{16}{64}\cdot\frac{48}{64}=\frac{3}{16}$: \rest{sí son independientes}.",
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
S.append(("Probabilidad total y teorema de Bayes", [
 (1, r"\pau{Aragón, EvAU ordinaria 2023} En una facultad de Economía se ofrece una asignatura en tres grupos, G1, G2 y G3, que representan el 40\,\%, el 35\,\% y el 25\,\% de los estudiantes, respectivamente. Supera la asignatura el 80\,\% del grupo G1, el 60\,\% del G2 y el 92\,\% del G3. Calcula la probabilidad de que, al elegir un estudiante al azar:" + tasks(1, [
      r"haya superado la asignatura y sea del grupo G3;", r"no haya superado la asignatura;", r"haya superado la asignatura;", r"ni haya superado la asignatura ni sea del grupo G1;", r"sea del grupo G3, si ha superado la asignatura."])
     + recorda(r"probabilidad total: $P(S)=P(G_1)P(S\cond G_1)+P(G_2)P(S\cond G_2)+P(G_3)P(S\cond G_3)$. Bayes: $P(G_i\cond S)=\dfrac{P(G_i)P(S\cond G_i)}{P(S)}$."),
     cen(arbre([('G_1', ag[0], [('S', ap[0], Q(ag[0] * ap[0])), (r'\overline{S}', 1 - ap[0], Q(ag[0] * (1 - ap[0])))]), ('G_2', ag[1], [('S', ap[1], Q(ag[1] * ap[1])), (r'\overline{S}', 1 - ap[1], Q(ag[1] * (1 - ap[1])))]),
                ('G_3', ag[2], [('S', ap[2], Q(ag[2] * ap[2])), (r'\overline{S}', 1 - ap[2], Q(ag[2] * (1 - ap[2])))])])) +
     tasks(2, [r"$0{,}25\cdot0{,}92=" + B(ag[2] * ap[2]) + "$", r"$1-0{,}76=" + B(1 - agT) + "$", r"$0{,}32+0{,}21+0{,}23=" + B(agT) + "$", r"$0{,}35\cdot0{,}4+0{,}25\cdot0{,}08=" + B(ag[1] * (1 - ap[1]) + ag[2] * (1 - ap[2])) + "$",
               r"$P(G_3\cond S)=\frac{0{,}23}{0{,}76}=" + B(ag[2] * ap[2] / agT) + "$"])),
 (1, r"\pau{Andalucía, PEvAU septiembre 2018} Un hotel tiene tres lavadoras industriales, $L_1$, $L_2$ y $L_3$. $L_1$ hace el 50\,\% de los lavados, $L_2$ el 30\,\% y $L_3$ el resto. $L_1$ produce un 5\,\% de lavados defectuosos, $L_2$ un 15\,\% y $L_3$ un 20\,\%. Se elige al azar un lavado." + tasks(1, [
      r"Calcula la probabilidad de que no sea defectuoso.", r"Calcula la probabilidad de que lo haya hecho $L_1$, sabiendo que ha sido defectuoso."]),
     tasks(1, [r"$P(D)=0{,}5\cdot0{,}05+0{,}3\cdot0{,}15+0{,}2\cdot0{,}2=0{,}11\Rightarrow P(\co D)=" + B(1 - lvT) + "$", r"$P(L_1\cond D)=\frac{0{,}025}{0{,}11}=" + B(lv[0] * ld[0] / lvT) + "$"])),
 (1, r"\pau{Galicia, ABAU septiembre 2018} En una empresa, el 30\,\% de los empleados son mujeres y el 70\,\% restante, hombres. De las mujeres, el 80\,\% tiene contrato indefinido, mientras que de los hombres solo el 70\,\% lo tiene." + tasks(1, [
      r"Calcula el porcentaje de personas de la empresa que tienen contrato indefinido.", r"Si un empleado tiene contrato indefinido, ¿cuál es la probabilidad de que sea mujer?", r"¿Son independientes los sucesos «ser hombre» y «tener contrato indefinido»?"]),
     cen(arbre([('M', F('0.3'), [('I', F('0.8'), '0{,}24'), (r'\overline{I}', F('0.2'), '0{,}06')]), ('H', F('0.7'), [('I', F('0.7'), '0{,}49'), (r'\overline{I}', F('0.3'), '0{,}21')])], s=(2.4, 1.3))) +
     tasks(1, [r"$0{,}24+0{,}49=0{,}73$: \ $\res{73\,\%}$", r"$P(M\cond I)=\frac{0{,}24}{0{,}73}=" + B(F('0.24') / dn) + "$", r"$P(I\cond H)=0{,}7\neq P(I)=0{,}73$: \rest{no son independientes}."])),
 (1, r"\pau{Galicia, ABAU junio 2018} El 30\,\% de los estudiantes de secundaria de un instituto juega al baloncesto. Entre los que juegan al baloncesto, el 40\,\% juega también al tenis; entre los que no juegan al baloncesto, una cuarta parte juega al tenis. Elegimos un estudiante al azar." + tasks(1, [
      r"¿Cuál es la probabilidad de que practique ambos deportes?", r"¿Cuál es la probabilidad de que juegue al tenis?", r"¿Son independientes los sucesos «jugar al tenis» y «jugar al baloncesto»?"]),
     tasks(1, [r"$0{,}3\cdot0{,}4=" + B(F('0.12')) + "$", r"$0{,}12+0{,}7\cdot0{,}25=" + B(bt) + "$", r"$P(T\cond B)=0{,}4\neq P(T)=0{,}295$: \rest{no son independientes}."])),
 (1, r"\pau{Andalucía, PEvAU extraordinaria 2020} Una empresa fabrica bombillas LED y halógenas. El 5\,\% de las LED y el 2\,\% de las halógenas salen defectuosas. Se elige al azar una bombilla de una caja que contiene 40 bombillas LED y 10 halógenas." + tasks(1, [
      r"Calcula la probabilidad de que la bombilla elegida no sea defectuosa.", r"Calcula la probabilidad de que la bombilla sea LED, sabiendo que es defectuosa."]),
     tasks(1, [r"$P(D)=\frac{40}{50}\cdot0{,}05+\frac{10}{50}\cdot0{,}02=0{,}044\Rightarrow P(\co D)=" + B(1 - bo) + "$", r"$P(LED\cond D)=\frac{0{,}04}{0{,}044}=" + B(F(40, 50) * F('0.05') / bo) + "$"])),
 (2, r"\pau{Andalucía, PEvAU ordinaria 2023} En una base de datos de correos electrónicos se ha observado que el 20\,\% de los correos recibidos son basura (\emph{spam}). Además, la palabra «lottery» aparece en el 40\,\% de los correos basura y en el 0,6\,\% de los que no lo son." + tasks(1, [
      r"Calcula la probabilidad de que un correo elegido al azar en el que aparece la palabra «lottery» sea basura.", r"Calcula la probabilidad de que un correo elegido al azar en el que no aparece la palabra «lottery» no sea basura.",
      r"Si un correo se etiqueta como basura cuando aparece la palabra «lottery» y como no basura cuando no aparece, calcula la probabilidad de que un correo se etiquete incorrectamente."]),
     cen(arbre([('S', F('0.2'), [('L', F('0.4'), '0{,}08'), (r'\overline{L}', F('0.6'), '0{,}12')]), (r'\overline{S}', F('0.8'), [('L', F('0.006'), '0{,}0048'), (r'\overline{L}', F('0.994'), '0{,}7952')])], s=(2.4, 1.3))) +
     r"$P(L)=0{,}08+0{,}0048=0{,}0848$." + tasks(1, [r"$P(S\cond L)=\frac{0{,}08}{0{,}0848}=" + B(F('0.08') / sp) + "$", r"$P(\co S\cond\co L)=\frac{0{,}7952}{0{,}9152}=" + B(F('0.8') * F('0.994') / (1 - sp)) + "$",
      r"$P(S\cap\co L)+P(\co S\cap L)=0{,}12+0{,}0048=" + B(F('0.1248')) + "$"])),
 (2, r"\pau{Navarra, EvAU extraordinaria 2022} Se considera que el 4\,\% de los deportistas federados consume alguna sustancia no permitida. Una nueva prueba de detección identifica correctamente el consumo en el 92\,\% de los casos, pero si un deportista no consume, la prueba da positivo en el 10\,\% de los casos. Se elige un deportista al azar. Calcula (con 4 decimales):" + tasks(1, [
      r"La probabilidad de que obtenga un resultado positivo.", r"La probabilidad de que sea consumidor y la prueba dé negativo.", r"La probabilidad de que no sea consumidor, sabiendo que la prueba ha dado negativo."]),
     tasks(1, [r"$0{,}04\cdot0{,}92+0{,}96\cdot0{,}1=" + B(dp) + "$", r"$0{,}04\cdot0{,}08=" + B(F('0.0032')) + "$", r"$\frac{0{,}96\cdot0{,}9}{1-0{,}1328}=\frac{0{,}864}{0{,}8672}=" + B(F('0.864') / (1 - dp)) + "$"])),
 (2, r"\pau{Galicia, ABAU extraordinaria 2023} En una urna A hay 8 bolas verdes y 6 rojas, y en una urna B, 4 verdes y 5 rojas. Se lanza un dado: si sale un número menor que 3 se saca una bola de la urna A, y si no, de la urna B." + tasks(1, [
      r"Calcula la probabilidad de que la bola extraída sea roja.", r"Sabiendo que se ha extraído una bola verde, ¿cuál es la probabilidad de que sea de la urna A?", r"¿Son independientes los sucesos «sacar bola roja» y «la bola es de la urna A»?"]),
     cen(arbre([('A', F(1, 3), [('V', F(8, 14), Q(F(1, 3) * F(8, 14))), ('R', F(6, 14), Q(F(1, 3) * F(6, 14)))]), ('B', F(2, 3), [('V', F(4, 9), Q(F(2, 3) * F(4, 9))), ('R', F(5, 9), Q(F(2, 3) * F(5, 9)))])], s=(2.4, 1.3))) +
     tasks(1, [r"$\frac13\cdot\frac{6}{14}+\frac23\cdot\frac59=\frac17+\frac{10}{27}=" + B(gu) + "$", r"$P(A\cond V)=\frac{4/21}{92/189}=" + B(F(1, 3) * F(8, 14) / (1 - gu)) + "$",
               r"$P(R\cond A)=\frac{6}{14}=\frac37\approx0{,}4286\neq P(R)\approx" + dec(gu) + r"$: \rest{no son independientes}."])),
 (2, r"\pau{Canarias, EBAU extraordinaria 2022} Tenemos tres urnas iguales: la primera tiene 6 bolas blancas y 4 negras, la segunda 5 blancas y 2 negras, y la tercera 4 blancas y 7 negras." + tasks(1, [
      r"Se saca una bola de una urna elegida al azar. Haz un diagrama con las probabilidades de los resultados posibles.", r"Calcula la probabilidad de sacar una bola negra.", r"Se ha extraído una bola y es blanca. Calcula la probabilidad de que sea de la primera urna."]),
     cen(arbre([('U_1', F(1, 3), [('B', F(6, 10), ''), ('N', F(4, 10), '')]), ('U_2', F(1, 3), [('B', F(5, 7), ''), ('N', F(2, 7), '')]), ('U_3', F(1, 3), [('B', F(4, 11), ''), ('N', F(7, 11), '')])])) +
     tasks(1, [r"Véase el árbol.", r"$\frac13\left(\frac4{10}+\frac27+\frac7{11}\right)=" + B(cn) + "$", r"$P(U_1\cond B)=\frac{\frac13\cdot\frac{6}{10}}{1-\frac{509}{1155}}=\frac{1/5}{646/1155}=" + B(F(1, 3) * F(6, 10) / (1 - cn)) + "$"])),
 (2, r"\pau{Murcia, EBAU extraordinaria 2021} Hay tres cajas: la primera contiene 4 bolas azules y 6 blancas; la segunda, una bola azul y 5 blancas; la tercera, 3 azules y 5 blancas. Cogemos una bola al azar de una de las cajas, también elegida al azar." + tasks(1, [
      r"Calcula la probabilidad de que la bola sea azul.", r"Si la bola es blanca, calcula la probabilidad de que sea de la primera caja."]),
     tasks(1, [r"$\frac13\left(\frac4{10}+\frac16+\frac38\right)=" + B(mc) + "$", r"$\frac{\frac13\cdot\frac{6}{10}}{1-\frac{113}{360}}=\frac{72/360}{247/360}=" + B(F(1, 3) * F(6, 10) / (1 - mc)) + "$"])),
 (1, r"\pau{Navarra, EvAU septiembre 2018} Dos estudiantes construyen un dado con 5 caras rojas y una azul, ponen 7 bolas verdes y 3 negras en una caja A, y 6 negras y 2 verdes en una caja B. Lanzan el dado: si sale rojo, sacan una bola de la caja A, y si sale azul, de la B." + tasks(1, [
      r"Calcula la probabilidad de que la bola sea verde.", r"Calcula la probabilidad de que la cara del dado sea azul, sabiendo que la bola no es verde."]),
     tasks(1, [r"$\frac56\cdot\frac7{10}+\frac16\cdot\frac28=" + B(nv) + "$", r"$\frac{\frac16\cdot\frac68}{1-0{,}625}=\frac{0{,}125}{0{,}375}=" + B(F(1, 6) * F(6, 8) / (1 - nv)) + "$"])),
 (1, r"\pau{Aragón, EvAU extraordinaria 2024} En España, el 30\,\% de la población tiene menos de 30 años, el 50\,\% entre 30 y 65 años, y el 20\,\% más de 65. Un estudio afirma que tiene teléfono móvil el 70\,\% de los menores de 30 años, el 95\,\% de los que tienen entre 30 y 65, y el 50\,\% de los mayores de 65." + tasks(1, [
      r"Se elige una persona al azar. Calcula la probabilidad de que tenga más de 65 años y tenga móvil.", r"¿Cuál es la probabilidad de que una persona elegida al azar tenga móvil?", r"Elegimos una persona al azar y tiene móvil. ¿Cuál es la probabilidad de que tenga más de 65 años?",
      r"Elegimos una persona de cada grupo de edad. ¿Cuál es la probabilidad de que las tres tengan móvil? (Se puede suponer independencia.)"]),
     tasks(2, [r"$0{,}2\cdot0{,}5=" + B(F('0.1')) + "$", r"$0{,}21+0{,}475+0{,}1=" + B(mb) + "$", r"$\frac{0{,}1}{0{,}785}=" + B(F('0.1') / mb) + "$", r"$0{,}7\cdot0{,}95\cdot0{,}5=" + B(F('0.3325')) + "$"])),
 (1, r"\pau{Galicia, ABAU septiembre 2018} En una población, de cada 200 consumidores de una bebida isotónica, 60 consumen la marca A, 50 la marca B y el resto, la C. Además, son jóvenes el 30\,\% de los consumidores de A, el 20\,\% de los de B y el 40\,\% de los de C." + tasks(1, [
      r"Si se selecciona al azar un consumidor, ¿cuál es la probabilidad de que sea joven?", r"Si se ha seleccionado un joven, halla la probabilidad de que consuma la marca B.", r"¿Son independientes los sucesos «ser joven» y «consumir la marca A»?"]),
     tasks(1, [r"$0{,}3\cdot0{,}3+0{,}25\cdot0{,}2+0{,}45\cdot0{,}4=" + B(iso) + "$", r"$\frac{0{,}05}{0{,}32}=" + B(F(50, 200) * F('0.2') / iso) + "$", r"$P(J\cond A)=0{,}3\neq P(J)=0{,}32$: \rest{no son independientes}."])),
 (2, r"\pau{Andalucía, PEvAU extraordinaria 2022} En una región hay tres universidades, A, B y C. De los estudiantes que terminaron el año pasado, el 60\,\% procedían de la A, el 30\,\% de la B y el resto de la C. La probabilidad de que un estudiante de la A no encuentre trabajo en la región es 0,4, y para uno de la B, 0,5." + tasks(1, [
      r"Si la probabilidad de que un estudiante no encuentre trabajo en la región es 0,395, determina la probabilidad de que un estudiante de la universidad C sí lo encuentre.", r"Calcula la probabilidad de que un estudiante que no ha encontrado trabajo en la región proceda de la universidad A o de la B."]),
     tasks(1, [r"$0{,}395=0{,}6\cdot0{,}4+0{,}3\cdot0{,}5+0{,}1\cdot x\Rightarrow x=P(\co T\cond C)=0{,}05\Rightarrow P(T\cond C)=" + B(1 - un_c) + "$",
               r"$\frac{0{,}24+0{,}15}{0{,}395}=" + B(F('0.39') / F('0.395')) + r"$ (o bien $1-\frac{0{,}005}{0{,}395}$)"])),
 (2, r"\pau{Andalucía, PEvAU extraordinaria 2020} Una urna contiene 6 bolas rojas y 4 azules. Se saca una bola al azar y se reemplaza por seis bolas del otro color. A continuación, se saca una segunda bola." + tasks(1, [
      r"Calcula la probabilidad de que la segunda bola sea roja.", r"Si sabemos que la segunda bola es azul, ¿cuál es la probabilidad de que la primera también lo haya sido?"]),
     r"Si la primera es roja, quedan 5 rojas y 10 azules; si es azul, 12 rojas y 3 azules." + cen(arbre([('R_1', F(6, 10), [('R_2', F(5, 15), Q(F(6, 10) * F(5, 15))), ('A_2', F(10, 15), Q(F(6, 10) * F(10, 15)))]), ('A_1', F(4, 10), [('R_2', F(12, 15), Q(F(4, 10) * F(12, 15))), ('A_2', F(3, 15), Q(F(4, 10) * F(3, 15)))])], s=(2.4, 1.3))) +
     tasks(1, [r"$\frac{6}{10}\cdot\frac{5}{15}+\frac{4}{10}\cdot\frac{12}{15}=" + B(rz) + "$", r"$P(A_1\cond A_2)=\frac{\frac{4}{10}\cdot\frac{3}{15}}{1-0{,}52}=\frac{0{,}08}{0{,}48}=" + B(F(4, 10) * F(3, 15) / (1 - rz)) + "$"])),
 (2, r"\pau{País Vasco, EAU ordinaria 2024} Asier tiene una urna con 4 bolas verdes y 2 rojas. Lanza una moneda: si sale cara, saca una bola de la urna, y si sale cruz, saca dos sin reemplazamiento." + tasks(1, [
      r"¿Cuál es la probabilidad de que Asier haya sacado dos bolas rojas?", r"Calcula la probabilidad de que no haya sacado ninguna bola roja.", r"Calcula la probabilidad de que haya sacado al menos una bola verde.", r"Calcula la probabilidad de que haya salido cara, sabiendo que al menos una bola es verde."]),
     tasks(2, [r"$\frac12\cdot\frac26\cdot\frac15=" + B(as1) + "$", r"$\frac12\cdot\frac46+\frac12\cdot\frac46\cdot\frac35=" + B(as2) + "$", r"$\frac12\cdot\frac46+\frac12\left(1-\frac1{15}\right)=" + B(as3) + "$",
               r"$\frac{1/3}{4/5}=" + B(F(1, 3) / as3) + "$"])),
 (2, r"\pau{País Vasco, EAU extraordinaria 2024} En una caja hay una bola roja y una azul. Se saca una bola y, antes de sacar una segunda, se devuelve a la caja la primera bola extraída y se añaden dos más del mismo color. A continuación se saca una segunda bola." + tasks(1, [
      r"Calcula la probabilidad de que la segunda bola sea roja si la primera ha sido azul.", r"Calcula la probabilidad de que la segunda bola sea azul.", r"Si la segunda bola ha sido azul, ¿cuál es la probabilidad de que la primera haya sido roja?"]),
     r"Después de la primera extracción hay 4 bolas: 3 del color de la primera y 1 del otro." + tasks(1, [r"$" + B(bx[0]) + "$ (quedan 1 roja y 3 azules)", r"$\frac12\cdot\frac14+\frac12\cdot\frac34=" + B(bx[1]) + "$",
      r"$\frac{\frac12\cdot\frac14}{\frac12}=" + B(F(1, 2) * F(1, 4) / bx[1]) + "$"])),
 (2, r"\pau{Madrid, EvAU ordinaria 2022} De una baraja de póquer de 52 cartas (13 de cada palo: diamantes, corazones, picas y tréboles) se elimina una carta al azar, sin mirarla. Después se elige al azar una carta de las que quedan y se observa." + tasks(1, [
      r"Calcula la probabilidad de que la carta observada sea de diamantes.", r"Si la carta observada no es de diamantes, calcula la probabilidad de que la carta eliminada tampoco lo fuera."]),
     tasks(1, [r"$\frac{13}{52}\cdot\frac{12}{51}+\frac{39}{52}\cdot\frac{13}{51}=" + B(pk2) + "$", r"$\frac{\frac{39}{52}\cdot\frac{38}{51}}{3/4}=" + B(pk3) + "$"])),
]))

# ---------- comprovacions ----------
for l, r, tol in CHK:
    if tol is None: assert l == r, (l, r)
    else:
        for x, y in (zip(l, r) if isinstance(l, list) else [(l, r)]): assert abs(x - y) < tol, (x, y)


# =====================================================================
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
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
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% etiqueta dels exercicis de la PAU d'altres comunitats
\newcommand{\pau}[1]{{\color{teal}\small\bfseries\faUniversity\ PAU · #1.}\ }
% successos contraris i probabilitat condicionada
\newcommand{\co}[1]{\overline{#1}}
\newcommand{\cond}{\,|\,}
'''

TIT = "Probabilidad"
KW = "probabilidad, espacio muestral, sucesos, regla de Laplace, probabilidad condicionada, independencia, tablas de contingencia, diagramas de árbol, extracciones, probabilidad total, teorema de Bayes, PAU"
def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 9: %s' % (t, TIT), capcalera='%s · Unidad 9: %s' % (t, TIT), pdfkeywords=KW, curs='2batx-ccss')
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{2batx-ccss}

\begin{document}
\thispagestyle{primera}

''' + assignatura('2batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 9' if sol else 'Ficha de ejercicios · Unidad 9') + '}{\\raggedright ' + TIT + '}\n')
    if not sol:
        out.append('\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n')
    npau = sum(1 for _, exs in S for _, q, _ in exs if '\\pau{' in q)
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Las probabilidades se han calculado de manera exacta; cuando el resultado no es un decimal exacto, se da la fracción y el valor aproximado con cuatro decimales. Puedes comprobar los ejercicios de dos sucesos con la calculadora de los apuntes interactivos de la unidad, y los de árboles con los módulos de extracciones y de Bayes."
             if sol else r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos. Define siempre los sucesos con letras y escribe los datos con la notación de probabilidades ($P(A)$, $P(A\cap B)$, $P(A\,|\,B)$\dots). Haz un diagrama de Venn, una tabla de contingencia o un diagrama de árbol cuando te ayude. Los " + str(npau) + r" ejercicios marcados con \textcolor{teal}{\faUniversity\ PAU} son de las pruebas de acceso a la universidad de otras comunidades autónomas.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            n += 1
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, s if sol else q))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't9-fitxa-solucions-es.tex' if sol else 't9-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n, npau

n = build(False); build(True)
print(n[0], 'ejercicios,', n[1], 'de la PAU;', len(CHK), 'comprobaciones')
