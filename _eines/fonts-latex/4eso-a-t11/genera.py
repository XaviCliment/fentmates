# Genera t11-fitxa-exercicis.tex i t11-fitxa-solucions.tex (4t ESO Matemàtiques A, Unitat 11: Probabilitat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 7 seccions segueixen els apartats dels apunts (11.1-11.7). Parteix de la fitxa de 2n ESO (../2eso-t11): els seus
# exercicis es guarden a OLD (per seccions de 2n) i es reparteixen en les seccions noves amb O(secció, número); s'hi afigen
# exercicis d'operacions amb esdeveniments, contrari i unió, independència, probabilitat condicionada i taules de
# contingència a partir de percentatges.
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Cada probabilitat es calcula amb fraccions exactes (Fraction) i es comprova amb ck() abans d'escriure-la.
# Ús: python3 genera.py && pdflatex t11-fitxa-exercicis.tex (dues vegades) && pdflatex t11-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys
from fractions import Fraction as Fr
from itertools import product, permutations
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

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
    E = list(E)
    return Fr(sum(1 for e in E if f(e)), len(E))
def fr(f):
    f = Fr(f)
    return str(f.numerator) if f.denominator == 1 else r'\frac{%d}{%d}' % (f.numerator, f.denominator)
D6 = range(1, 7)
DD = list(product(D6, D6))
def isprime(n): return n > 1 and all(n % k for k in range(2, int(n ** .5) + 1))

# ---------- figures (TikZ i taules) ----------
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
def cont(rh, ch, M, blank=(), hl=()):
    """taula de contingència 2×2 amb totals. blank: caselles (i, j) buides (2 = total); hl: caselles acolorides"""
    full = [[M[0][0], M[0][1], sum(M[0])], [M[1][0], M[1][1], sum(M[1])], [M[0][0] + M[1][0], M[0][1] + M[1][1], sum(map(sum, M))]]
    def cell(i, j):
        if (i, j) in blank: return r'\phantom{000}'
        v = str(full[i][j])
        if (i, j) in hl: return r'\cellcolor{accent!30}\textbf{%s}' % v
        return r'\textbf{%s}' % v if i == 2 or j == 2 else v
    rows = [r'\rowcolor{soft} & %s & %s & Total\\\hline' % (ch[0], ch[1])]
    for i, lab in enumerate([rh[0], rh[1], 'Total']):
        rows.append(r'\cellcolor{soft}\textbf{%s} & ' % lab + ' & '.join(cell(i, j) for j in range(3)) + r'\\' + (r'\hline' if i == 1 else ''))
    return r'{\small\renewcommand{\arraystretch}{1.3}\begin{tabular}{l|cc|c}' + '\n' + '\n'.join(rows) + '\n\\end{tabular}}'
def cen(*xs, sep=r'\qquad '): return r'\par\smallskip\begin{center}' + sep.join(xs) + r'\end{center}'

OLD = []  # exercicis de la fitxa de 2n ESO: [(títol, [(estrelles, enunciat, solució)])]
AL, DE = T('aleatori', 'aleatorio'), T('determinista', 'determinista')

# =====================================================================
# 1. Experiments aleatoris i deterministes
# =====================================================================
OLD.append((T("Experiments aleatoris i deterministes", "Experimentos aleatorios y deterministas"), [
 (1, T(r"Indica si són experiments aleatoris o deterministes:", r"Indica si son experimentos aleatorios o deterministas:")
     + tasks(2, [T(r"Llançar un dau i anotar el resultat.", r"Lanzar un dado y anotar el resultado."), T(r"Mesurar la temperatura a què bull l'aigua al nivell de la mar.", r"Medir la temperatura a la que hierve el agua al nivel del mar."),
                 T(r"Traure una carta d'una baralla sense mirar.", r"Sacar una carta de una baraja sin mirar."), T(r"Calcular quant pagarem per 3 kg de pomes a 2 €/kg.", r"Calcular cuánto pagaremos por 3 kg de manzanas a 2 €/kg."),
                 T(r"Endevinar el número guanyador de la loteria.", r"Adivinar el número ganador de la lotería."), T(r"Deixar caure una pilota i mirar si cau a terra.", r"Dejar caer una pelota y mirar si cae al suelo.")])
     + recorda(T(r"Un experiment és \textbf{aleatori} si no podem predir-ne el resultat, encara que el repetim en les mateixes condicions. És \textbf{determinista} si el resultat és sempre el mateix i el podem saber abans de fer-lo.",
                 r"Un experimento es \textbf{aleatorio} si no podemos predecir su resultado, aunque lo repitamos en las mismas condiciones. Es \textbf{determinista} si el resultado es siempre el mismo y lo podemos saber antes de hacerlo.")),
     tasks(2, [r"\rest{%s}" % AL, r"\rest{%s} (100 °C)" % DE, r"\rest{%s}" % AL, r"\rest{%s} (6 €)" % DE, r"\rest{%s}" % AL, r"\rest{%s}" % DE])),
 (1, T(r"Classifica aquests experiments en aleatoris o deterministes:", r"Clasifica estos experimentos en aleatorios o deterministas:")
     + tasks(2, [T(r"Girar una ruleta i mirar el color.", r"Girar una ruleta y mirar el color."), T(r"Comptar quantes arestes té un cub.", r"Contar cuántas aristas tiene un cubo."),
                 T(r"Triar a l'atzar un alumne de la classe.", r"Elegir al azar un alumno de la clase."), T(r"Calcular l'àrea d'un quadrat de 5 cm de costat.", r"Calcular el área de un cuadrado de 5 cm de lado."),
                 T(r"Llançar una xinxeta i mirar com cau.", r"Lanzar una chincheta y mirar cómo cae."), T(r"Saber quin dia de la setmana serà demà.", r"Saber qué día de la semana será mañana.")]),
     tasks(2, [r"\rest{%s}" % AL, r"\rest{%s} (12)" % DE, r"\rest{%s}" % AL, r"\rest{%s} (25 cm²)" % DE, r"\rest{%s}" % AL, r"\rest{%s}" % DE])),
 (1, T(r"En una bossa hi ha 9 boles roges i 1 de blava. Traiem una bola sense mirar. Descriu cada esdeveniment amb una d'aquestes paraules: \emph{segur}, \emph{molt probable}, \emph{poc probable}, \emph{impossible}.",
       r"En una bolsa hay 9 bolas rojas y 1 azul. Sacamos una bola sin mirar. Describe cada suceso con una de estas palabras: \emph{seguro}, \emph{muy probable}, \emph{poco probable}, \emph{imposible}.")
     + cen(bag('RRRRRRRRRB', per=5)) + tasks(4, [T(r"Traure roja.", r"Sacar roja."), T(r"Traure blava.", r"Sacar azul."), T(r"Traure verda.", r"Sacar verde."), T(r"Traure roja o blava.", r"Sacar roja o azul.")]),
     tasks(4, [r"\rest{%s}" % T('molt probable', 'muy probable'), r"\rest{%s}" % T('poc probable', 'poco probable'), r"\rest{%s}" % T('impossible', 'imposible'), r"\rest{%s}" % T('segur', 'seguro')])),
 (2, T(r"Llancem un dau. Ordena aquests esdeveniments de menys probable a més probable: \ A) traure un 6; \ B) traure parell; \ C) traure un 0; \ D) traure menys de 7; \ E) traure més d'1.",
       r"Lanzamos un dado. Ordena estos sucesos de menos probable a más probable: \ A) sacar un 6; \ B) sacar par; \ C) sacar un 0; \ D) sacar menos de 7; \ E) sacar más de 1."),
     T(r"\rest{C $<$ A $<$ B $<$ E $<$ D}: \ C és impossible (cap cas), A té 1 cas de 6, B en té 3, E en té 5 i D és segur (els 6 casos).",
       r"\rest{C $<$ A $<$ B $<$ E $<$ D}: \ C es imposible (ningún caso), A tiene 1 caso de 6, B tiene 3, E tiene 5 y D es seguro (los 6 casos).")),
 (2, T(r"Digues si cada experiment és aleatori o determinista. Si és aleatori, escriu dos resultats que puguen eixir.", r"Di si cada experimento es aleatorio o determinista. Si es aleatorio, escribe dos resultados que puedan salir.")
     + tasks(2, [T(r"Preguntar el mes de naixement a un alumne triat a l'atzar.", r"Preguntar el mes de nacimiento a un alumno elegido al azar."), T(r"Calcular el 15 \% de 80.", r"Calcular el 15 \% de 80."),
                 T(r"Mesurar la hipotenusa d'un triangle rectangle de catets 3 cm i 4 cm.", r"Medir la hipotenusa de un triángulo rectángulo de catetos 3 cm y 4 cm."), T(r"Llançar dues monedes.", r"Lanzar dos monedas.")]),
     tasks(2, [T(r"\rest{aleatori}: gener, juliol\dots", r"\rest{aleatorio}: enero, julio\dots"), r"\rest{%s}: 12" % DE, r"\rest{%s}: 5 cm" % DE, T(r"\rest{aleatori}: $CC$, $CX$\dots", r"\rest{aleatorio}: $CC$, $CX$\dots")])),
 (2, T(r"En Marc diu que llançar un dau és un experiment determinista, «perquè ja sabem que eixirà un nombre de l'1 al 6». Té raó? Explica-ho.",
       r"Marc dice que lanzar un dado es un experimento determinista, «porque ya sabemos que saldrá un número del 1 al 6». ¿Tiene razón? Explícalo."),
     T(r"\rest{No}. Sabem quins resultats \emph{poden} eixir (l'espai mostral), però no sabem \emph{quin} eixirà en cada llançament: és un experiment \textbf{aleatori}.",
       r"\rest{No}. Sabemos qué resultados \emph{pueden} salir (el espacio muestral), pero no sabemos \emph{cuál} saldrá en cada lanzamiento: es un experimento \textbf{aleatorio}.")),
 (3, T(r"Tens boles roges i blaves per a posar en una bossa. Quines boles hi posaries perquè l'esdeveniment «traure una bola roja» siga: a) segur; b) impossible; c) tan probable com no; d) molt probable?",
       r"Tienes bolas rojas y azules para poner en una bolsa. ¿Qué bolas pondrías para que el suceso «sacar una bola roja» sea: a) seguro; b) imposible; c) tan probable como no; d) muy probable?"),
     T(r"Per exemple: a) \rest{només roges}; \ b) \rest{només blaves}; \ c) \rest{tantes roges com blaves} (3 i 3); \ d) \rest{moltes més roges que blaves} (9 i 1).",
       r"Por ejemplo: a) \rest{solo rojas}; \ b) \rest{solo azules}; \ c) \rest{tantas rojas como azules} (3 y 3); \ d) \rest{muchas más rojas que azules} (9 y 1).")),
 (3, T(r"Escriu dos experiments aleatoris i dos de deterministes relacionats amb l'esport.", r"Escribe dos experimentos aleatorios y dos deterministas relacionados con el deporte."),
     T(r"Resposta oberta. Per exemple, aleatoris: \textbf{el resultat d'un partit} i \textbf{si un tir lliure entrarà}; deterministes: \textbf{el perímetre d'una pista de 40 m per 20 m (120 m)} i \textbf{quants jugadors té un equip de bàsquet en pista (5)}.",
       r"Respuesta abierta. Por ejemplo, aleatorios: \textbf{el resultado de un partido} y \textbf{si un tiro libre entrará}; deterministas: \textbf{el perímetro de una pista de 40 m por 20 m (120 m)} y \textbf{cuántos jugadores tiene un equipo de baloncesto en pista (5)}.")),
]))

# =====================================================================
# 2. Espai mostral i esdeveniments
# =====================================================================
U12 = range(1, 13)
assert [x for x in U12 if x % 2 == 0] == [2, 4, 6, 8, 10, 12] and [x for x in U12 if x % 5 == 0] == [5, 10] and [x for x in U12 if 12 % x == 0] == [1, 2, 3, 4, 6, 12]
U8 = range(1, 9)
assert [x for x in U8 if x % 2 == 0] == [2, 4, 6, 8] and [x for x in U8 if isprime(x)] == [2, 3, 5, 7] and [x for x in U8 if x > 5] == [6, 7, 8] and [x for x in U8 if 8 % x == 0] == [1, 2, 4, 8]
C2 = [a + b for a in 'CX' for b in 'CX']
assert [e for e in C2 if 'C' in e] == ['CC', 'CX', 'XC'] and [e for e in C2 if e[0] == e[1]] == ['CC', 'XX']
F3 = [a + b + c for a in 'OA' for b in 'OA' for c in 'OA']
assert len(F3) == 8 and [e for e in F3 if e.count('A') == 2] == ['OAA', 'AOA', 'AAO']
N3 = sorted(int(''.join(p)) for p in permutations('123'))
assert N3 == [123, 132, 213, 231, 312, 321] and [n for n in N3 if n % 2 == 0] == [132, 312] and [n for n in N3 if n > 200] == [213, 231, 312, 321]
assert [(a, b) for a, b in DD if a + b == 5] == [(1, 4), (2, 3), (3, 2), (4, 1)]
T2 = tree([('C', '', [('C', '', [], '$CC$'), ('X', '', [], '$CX$')]), ('X', '', [('C', '', [], '$XC$'), ('X', '', [], '$XX$')])], ld=14, sd=(13, 6.5))
T3 = tree([(a, '', [(b, '', [(c, '', [], '$%s$' % (a + b + c)) for c in 'OA']) for b in 'OA']) for a in 'OA'], ld=13, sd=(20, 10, 5))
P1, P2 = T(['S', 'A'], ['S', 'E']), ['C', 'P', 'T']
MENU = [a + b for a in P1 for b in P2]
assert len(MENU) == 6 and [m for m in MENU if m[1] == 'P'] == [P1[0] + 'P', P1[1] + 'P']
TM = tree([(a, '', [(b, '', [], '$%s$' % (a + b)) for b in P2]) for a in P1], ld=14, sd=(15, 6))
OLD.append((T("Espai mostral i esdeveniments", "Espacio muestral y sucesos"), [
 (1, T(r"Escriu l'espai mostral d'aquests experiments:", r"Escribe el espacio muestral de estos experimentos:")
     + tasks(2, [T(r"Llançar una moneda.", r"Lanzar una moneda."), T(r"Llançar un dau de quatre cares numerades de l'1 al 4.", r"Lanzar un dado de cuatro caras numeradas del 1 al 4."),
                 T(r"Girar una ruleta de 5 sectors iguals (roig, blau, verd, groc i negre).", r"Girar una ruleta con 5 sectores iguales: rojo, azul, verde, amarillo y negro."), T(r"Traure una bola d'una bossa amb boles roges i blaves.", r"Sacar una bola de una bolsa con bolas rojas y azules."),
                 T(r"Triar a l'atzar un dia de la setmana.", r"Elegir al azar un día de la semana."), T(r"Preguntar a algú quantes germanes té (com a màxim, 3).", r"Preguntar a alguien cuántas hermanas tiene (como máximo, 3).")])
     + recorda(T(r"L'\textbf{espai mostral} $E$ és el conjunt de tots els resultats possibles, i un \textbf{esdeveniment} és un subconjunt d'$E$ (un grup de resultats).",
                 r"El \textbf{espacio muestral} $E$ es el conjunto de todos los resultados posibles, y un \textbf{suceso} es un subconjunto de $E$ (un grupo de resultados).")),
     tasks(2, [r"$E=\{C,\,X\}$", r"$E=\{1,\,2,\,3,\,4\}$", T(r"$E=\{\text{roig},\,\text{blau},\,\text{verd},\,\text{groc},\,\text{negre}\}$", r"$E=\{\text{rojo},\,\text{azul},\,\text{verde},\,\text{amarillo},\,\text{negro}\}$"),
               T(r"$E=\{R,\,B\}$", r"$E=\{R,\,A\}$"), T(r"$E=\{\text{dl},\,\text{dt},\,\text{dc},\,\text{dj},\,\text{dv},\,\text{ds},\,\text{dg}\}$", r"$E=\{\text{L},\,\text{M},\,\text{X},\,\text{J},\,\text{V},\,\text{S},\,\text{D}\}$"), r"$E=\{0,\,1,\,2,\,3\}$"])),
 (1, T(r"Traiem una bola d'una urna amb 12 boles numerades de l'1 al 12. Escriu aquests esdeveniments i digues de quin tipus és cadascun (elemental, compost, segur o impossible):",
       r"Sacamos una bola de una urna con 12 bolas numeradas del 1 al 12. Escribe estos sucesos y di de qué tipo es cada uno (elemental, compuesto, seguro o imposible):")
     + tasks(3, [T(r"$A=$ «parell»", r"$A=$ «par»"), T(r"$B=$ «múltiple de 5»", r"$B=$ «múltiplo de 5»"), T(r"$C=$ «més gran que 12»", r"$C=$ «mayor que 12»"),
                 T(r"$D=$ «divisor de 12»", r"$D=$ «divisor de 12»"), T(r"$F=$ «menor que 13»", r"$F=$ «menor que 13»"), T(r"$G=$ «múltiple d'11»", r"$G=$ «múltiplo de 11»")]),
     tasks(3, [r"$\{2,4,6,8,10,12\}$: \rest{%s}" % T('compost', 'compuesto'), r"$\{5,\,10\}$: \rest{%s}" % T('compost', 'compuesto'), r"$\varnothing$: \rest{%s}" % T('impossible', 'imposible'),
               r"$\{1,2,3,4,6,12\}$: \rest{%s}" % T('compost', 'compuesto'), r"$E$: \rest{%s}" % T('segur', 'seguro'), r"$\{11\}$: \rest{elemental}"])),
 (1, T(r"Llancem un dau de 8 cares numerades de l'1 al 8. Escriu l'espai mostral i els esdeveniments:", r"Lanzamos un dado de 8 caras numeradas del 1 al 8. Escribe el espacio muestral y los sucesos:")
     + tasks(4, [T(r"«parell»", r"«par»"), T(r"«primer»", r"«primo»"), T(r"«més gran que 5»", r"«mayor que 5»"), T(r"«divisor de 8»", r"«divisor de 8»")]),
     r"$E=\{1,\,2,\,3,\,4,\,5,\,6,\,7,\,8\}$" + tasks(4, [r"$\res{\{2,4,6,8\}}$", r"$\res{\{2,3,5,7\}}$", r"$\res{\{6,7,8\}}$", r"$\res{\{1,2,4,8\}}$"])),
 (2, T(r"Llancem dues monedes. Fes un diagrama d'arbre i escriu l'espai mostral i els esdeveniments $A=$ «almenys una cara», $B=$ «cap cara» i $C=$ «les dues iguals».",
       r"Lanzamos dos monedas. Haz un diagrama de árbol y escribe el espacio muestral y los sucesos $A=$ «al menos una cara», $B=$ «ninguna cara» y $C=$ «las dos iguales»."),
     cen(T2) + r"$E=\{CC,\,CX,\,XC,\,XX\}$; \quad $A=\res{\{CC,\,CX,\,XC\}}$, \quad $B=\res{\{XX\}}$, \quad $C=\res{\{CC,\,XX\}}$."),
 (2, T(r"Llancem una moneda i un dau. Fes una taula de doble entrada amb tots els resultats. Quants n'hi ha? Escriu els esdeveniments «cara i nombre parell» i «creu i menor que 3».",
       r"Lanzamos una moneda y un dado. Haz una tabla de doble entrada con todos los resultados. ¿Cuántos hay? Escribe los sucesos «cara y número par» y «cruz y menor que 3»."),
     cen(ctab(['', '1', '2', '3', '4', '5', '6'], [['$C$'] + ['$C%d$' % i for i in D6], ['$X$'] + ['$X%d$' % i for i in D6]]))
     + T(r"$2\cdot6=\res{12}$ resultats. \quad «Cara i parell» $=\res{\{C2,\,C4,\,C6\}}$; \quad «creu i menor que 3» $=\res{\{X1,\,X2\}}$.",
         r"$2\cdot6=\res{12}$ resultados. \quad «Cara y par» $=\res{\{C2,\,C4,\,C6\}}$; \quad «cruz y menor que 3» $=\res{\{X1,\,X2\}}$.")),
 (2, T(r"Una família té tres fills. Anotem si cadascun és xiqueta (A) o xiquet (O), per ordre de naixement. Fes un diagrama d'arbre, escriu l'espai mostral i l'esdeveniment «exactament dues xiquetes».",
       r"Una familia tiene tres hijos. Anotamos si cada uno es niña (A) o niño (O), por orden de nacimiento. Haz un diagrama de árbol, escribe el espacio muestral y el suceso «exactamente dos niñas»."),
     cen(T3) + T(r"$E=\{OOO,\,OOA,\,OAO,\,OAA,\,AOO,\,AOA,\,AAO,\,AAA\}$ (8 resultats).\par «Dues xiquetes» $=\res{\{OAA,\,AOA,\,AAO\}}$.",
                 r"$E=\{OOO,\,OOA,\,OAO,\,OAA,\,AOO,\,AOA,\,AAO,\,AAA\}$ (8 resultados).\par «Dos niñas» $=\res{\{OAA,\,AOA,\,AAO\}}$.")),
 (2, T(r"Un menú té dos primers plats, sopa (S) o amanida (A), i tres segons, carn (C), peix (P) o truita (T). Triem el menú a l'atzar. Fes un diagrama d'arbre, escriu l'espai mostral i l'esdeveniment «el menú porta peix».",
       r"Un menú tiene dos primeros platos, sopa (S) o ensalada (E), y tres segundos, carne (C), pescado (P) o tortilla (T). Elegimos el menú al azar. Haz un diagrama de árbol, escribe el espacio muestral y el suceso «el menú lleva pescado»."),
     cen(TM) + r"$E=\{%s\}$ ($2\cdot3=6$ %s). \quad «%s» $=\res{\{%s,\,%s\}}$." % (',\\,'.join(MENU), T('menús', 'menús'), T('Peix', 'Pescado'), P1[0] + 'P', P1[1] + 'P')),
 (2, T(r"Escrivim cada lletra de la paraula ATZAR en una targeta i en traiem una. Escriu l'espai mostral. Tots els resultats tenen la mateixa possibilitat d'eixir?",
       r"Escribimos cada letra de la palabra AZAR en una tarjeta y sacamos una. Escribe el espacio muestral. ¿Todos los resultados tienen la misma posibilidad de salir?"),
     T(r"$E=\res{\{A,\,T,\,Z,\,R\}}$. \ \rest{No}: hi ha dues targetes amb la A i només una de cada altra lletra, així que la A és més fàcil de traure.",
       r"$E=\res{\{A,\,Z,\,R\}}$. \ \rest{No}: hay dos tarjetas con la A y solo una de cada otra letra, así que la A es más fácil de sacar.")),
 (3, T(r"Formem nombres de tres xifres diferents amb les xifres 1, 2 i 3. Escriu l'espai mostral i els esdeveniments «el nombre és parell» i «el nombre és més gran que 200».",
       r"Formamos números de tres cifras distintas con las cifras 1, 2 y 3. Escribe el espacio muestral y los sucesos «el número es par» y «el número es mayor que 200»."),
     T(r"$E=\{123,\,132,\,213,\,231,\,312,\,321\}$.\par «Parell» $=\res{\{132,\,312\}}$; \quad «més gran que 200» $=\res{\{213,\,231,\,312,\,321\}}$.",
       r"$E=\{123,\,132,\,213,\,231,\,312,\,321\}$.\par «Par» $=\res{\{132,\,312\}}$; \quad «mayor que 200» $=\res{\{213,\,231,\,312,\,321\}}$.")),
 (3, T(r"Llancem dos daus (un de roig i un de blau). Quants resultats té l'espai mostral? Escriu els esdeveniments «la suma és 5» i «trauen el mateix nombre (doble)».",
       r"Lanzamos dos dados (uno rojo y uno azul). ¿Cuántos resultados tiene el espacio muestral? Escribe los sucesos «la suma es 5» y «sacan el mismo número (doble)»."),
     T(r"$6\cdot6=\res{36}$ resultats (parells ordenats). «Suma 5» $=\res{\{(1,4),\,(2,3),\,(3,2),\,(4,1)\}}$; «doble» $=\res{\{(1,1),\,(2,2),\,\dots,\,(6,6)\}}$ (6 resultats).",
       r"$6\cdot6=\res{36}$ resultados (pares ordenados). «Suma 5» $=\res{\{(1,4),\,(2,3),\,(3,2),\,(4,1)\}}$; «doble» $=\res{\{(1,1),\,(2,2),\,\dots,\,(6,6)\}}$ (6 resultados).")),
]))

# =====================================================================
# 3. Probabilitat d'un esdeveniment
# =====================================================================
FQ = [7, 9, 8, 10, 6, 10]; assert sum(FQ) == 50
HQ = [Fr(f, 50) for f in FQ]
for h, w in zip(HQ, ['0,14', '0,18', '0,16', '0,2', '0,12', '0,2']): ck(h, w)
ck(Fr(9 + 10 + 10, 50), '0,58')
XN, XF = [20, 100, 500, 1000], [13, 58, 297, 601]
for f, n, w in zip(XF, XN, ['0,65', '0,58', '0,594', '0,601']): ck(Fr(f, n), w)
ck(Fr(45, 60), '0,75'); ck(20 * Fr(3, 4), 15)
ck(1 - Fr(35, 100) - Fr(25, 100) - Fr(1, 10), '0,3'); ck(Fr(25, 100) + Fr(1, 10) + Fr(3, 10), '0,65'); ck(Fr(25, 100) + Fr(3, 10), '0,55')
PT = [Fr(15, 100), Fr(1, 10), Fr(2, 10), Fr(15, 100), Fr(1, 10)]; ck(1 - sum(PT), '0,3'); ck(PT[1] + PT[3] + (1 - sum(PT)), '0,55')
ck(Fr(120, 300), '0,4'); ck(30 * Fr(4, 10), 12)
TD = [150, 150, 150, 150, 200, 400]; assert sum(TD) == 1200
ck(Fr(400, 1200), Fr(1, 3)); ck(Fr(150 + 150 + 400, 1200), Fr(7, 12)); ck(300 * Fr(1, 3), 100)
PK = [Fr(k, 21) for k in D6]; assert sum(PK) == 1; ck(PK[5], Fr(2, 7)); ck(PK[1] + PK[3] + PK[5], Fr(4, 7))
ck(lap('RRRRRRRRRB', lambda c: c == 'R'), '0,9'); ck(lap(D6, lambda x: x % 2 == 0), '0,5')
OLD.append((T("Probabilitat d'un esdeveniment", "Probabilidad de un suceso"), [
 (1, T(r"Hem llançat un dau 50 vegades i hem obtingut aquests resultats. Completa la taula amb les freqüències relatives (en decimal) i calcula la freqüència relativa de «traure parell».",
       r"Hemos lanzado un dado 50 veces y hemos obtenido estos resultados. Completa la tabla con las frecuencias relativas (en decimal) y calcula la frecuencia relativa de «sacar par».")
     + cen(ctab([T('Resultat', 'Resultado'), '1', '2', '3', '4', '5', '6'], [[T('Freq. absoluta', 'Frec. absoluta')] + [str(f) for f in FQ], [T('Freq. relativa', 'Frec. relativa')] + ['' for f in FQ]]))
     + recorda(T(r"Si un esdeveniment ocorre $f$ vegades en $n$ repeticions, la seua \textbf{freqüència relativa} és $h=\frac{f}{n}$.", r"Si un suceso ocurre $f$ veces en $n$ repeticiones, su \textbf{frecuencia relativa} es $h=\frac{f}{n}$.")),
     r"$h$: \ $\res{0{,}14}$, \ $\res{0{,}18}$, \ $\res{0{,}16}$, \ $\res{0{,}2}$, \ $\res{0{,}12}$, \ $\res{0{,}2}$ \ (%s). \quad $h(\text{%s})=\frac{9+10+10}{50}=\res{0{,}58}$." % (T('sumen 1', 'suman 1'), T('parell', 'par'))),
 (1, T(r"Quins d'aquests nombres poden ser la probabilitat d'un esdeveniment?", r"¿Cuáles de estos números pueden ser la probabilidad de un suceso?") + tasks(4, [r"$0{,}7$", r"$1{,}2$", r"$-0{,}1$", r"$\frac32$", r"$0$", r"$100\,\%$", r"$\frac54$", r"$\frac{99}{100}$"]),
     T(r"Una probabilitat sempre està entre 0 i 1. Poden ser-ho: \rest{$0{,}7$, \ $0$, \ $100\,\%$ i $\frac{99}{100}$}. No poden ser-ho: $1{,}2$, $-0{,}1$, $\frac32$ i $\frac54$.",
       r"Una probabilidad siempre está entre 0 y 1. Pueden serlo: \rest{$0{,}7$, \ $0$, \ $100\,\%$ y $\frac{99}{100}$}. No pueden serlo: $1{,}2$, $-0{,}1$, $\frac32$ y $\frac54$.")),
 (1, T(r"Associa cada esdeveniment amb la seua probabilitat: \ $0$, \ $0{,}1$, \ $0{,}5$, \ $0{,}9$, \ $1$.", r"Asocia cada suceso con su probabilidad: \ $0$, \ $0{,}1$, \ $0{,}5$, \ $0{,}9$, \ $1$.")
     + tasks(2, [T(r"Traure roja d'una bossa amb 9 roges i 1 blava.", r"Sacar roja de una bolsa con 9 rojas y 1 azul."), T(r"Traure parell amb un dau.", r"Sacar par con un dado."), T(r"Traure un 7 amb un dau.", r"Sacar un 7 con un dado."),
                 T(r"Traure blava de la bossa de l'apartat a).", r"Sacar azul de la bolsa del apartado a)."), T(r"Traure menys de 7 amb un dau.", r"Sacar menos de 7 con un dado.")]),
     tasks(2, [r"$\res{0{,}9}$", r"$\res{0{,}5}$", r"$\res{0}$", r"$\res{0{,}1}$", r"$\res{1}$"])),
 (2, T(r"Hem llançat una xinxeta diverses vegades i hem anotat quantes ha caigut amb la punta cap amunt. Completa la taula i estima la probabilitat que caiga amb la punta cap amunt.",
       r"Hemos lanzado una chincheta varias veces y hemos anotado cuántas ha caído con la punta hacia arriba. Completa la tabla y estima la probabilidad de que caiga con la punta hacia arriba.")
     + cen(ctab([T('Llançaments', 'Lanzamientos'), '20', '100', '500', '1000'], [[T('Punta amunt', 'Punta arriba')] + [str(f) for f in XF], [T('Freq. relativa', 'Frec. relativa'), '', '', '', '']]))
     + recorda(T(r"\textbf{Llei dels grans nombres}: quan repetim un experiment moltes vegades, la freqüència relativa d'un esdeveniment s'estabilitza al voltant de la seua probabilitat.",
                 r"\textbf{Ley de los grandes números}: cuando repetimos un experimento muchas veces, la frecuencia relativa de un suceso se estabiliza alrededor de su probabilidad.")),
     T(r"$h$: \ $0{,}65$; \ $0{,}58$; \ $0{,}594$; \ $0{,}601$. \ Amb més llançaments s'estabilitza: $P(\text{punta amunt})\approx\res{0{,}6}$.",
       r"$h$: \ $0{,}65$; \ $0{,}58$; \ $0{,}594$; \ $0{,}601$. \ Con más lanzamientos se estabiliza: $P(\text{punta arriba})\approx\res{0{,}6}$.")),
 (2, T(r"Un jugador d'handbol ha marcat 45 dels 60 penals que ha llançat. Estima la probabilitat que marque un penal. Quants penals esperes que marque dels 20 pròxims?",
       r"Un jugador de balonmano ha marcado 45 de los 60 penaltis que ha lanzado. Estima la probabilidad de que marque un penalti. ¿Cuántos penaltis esperas que marque de los 20 próximos?"),
     T(r"$P\approx\frac{45}{60}=\res{0{,}75}$. \ $20\cdot0{,}75=\res{15\text{ penals}}$ (aproximadament).", r"$P\approx\frac{45}{60}=\res{0{,}75}$. \ $20\cdot0{,}75=\res{15\text{ penaltis}}$ (aproximadamente).")),
 (2, T(r"Una ruleta té sectors de quatre colors. Sabem que $P(\text{roig})=0{,}35$, $P(\text{blau})=0{,}25$ i $P(\text{verd})=0{,}1$. Calcula $P(\text{groc})$, $P(\text{blau o groc})$ i $P(\text{no roig})$."
       + recorda(r"Les probabilitats de tots els resultats elementals sumen 1, i la probabilitat d'un esdeveniment compost és la suma de les probabilitats dels seus resultats."),
       r"Una ruleta tiene sectores de cuatro colores. Sabemos que $P(\text{rojo})=0{,}35$, $P(\text{azul})=0{,}25$ y $P(\text{verde})=0{,}1$. Calcula $P(\text{amarillo})$, $P(\text{azul o amarillo})$ y $P(\text{no rojo})$."
       + recorda(r"Las probabilidades de todos los resultados elementales suman 1, y la probabilidad de un suceso compuesto es la suma de las probabilidades de sus resultados.")),
     T(r"$P(\text{groc})=1-(0{,}35+0{,}25+0{,}1)=\res{0{,}3}$. \ $P(\text{blau o groc})=0{,}25+0{,}3=\res{0{,}55}$. \ «No roig» és blau, verd o groc: $0{,}25+0{,}1+0{,}3=\res{0{,}65}$.",
       r"$P(\text{amarillo})=1-(0{,}35+0{,}25+0{,}1)=\res{0{,}3}$. \ $P(\text{azul o amarillo})=0{,}25+0{,}3=\res{0{,}55}$. \ «No rojo» es azul, verde o amarillo: $0{,}25+0{,}1+0{,}3=\res{0{,}65}$.")),
 (2, T(r"Un dau està trucat. Les probabilitats de l'1 al 5 són 0,15, 0,1, 0,2, 0,15 i 0,1. Calcula $P(6)$ i la probabilitat de traure parell.",
       r"Un dado está trucado. Las probabilidades del 1 al 5 son 0,15, 0,1, 0,2, 0,15 y 0,1. Calcula $P(6)$ y la probabilidad de sacar par."),
     r"$P(6)=1-(0{,}15+0{,}1+0{,}2+0{,}15+0{,}1)=1-0{,}7=\res{0{,}3}$. \ $P(\text{%s})=P(2)+P(4)+P(6)=0{,}1+0{,}15+0{,}3=\res{0{,}55}$." % T('parell', 'par')),
 (2, T(r"En Joan ha llançat una moneda 10 vegades i n'han eixit 7 cares. Diu que la moneda està trucada perquè la freqüència relativa de cara és 0,7. Té raó?",
       r"Juan ha lanzado una moneda 10 veces y han salido 7 caras. Dice que la moneda está trucada porque la frecuencia relativa de cara es 0,7. ¿Tiene razón?"),
     T(r"\rest{No} necessàriament: 10 llançaments són molt pocs i la freqüència relativa varia molt. Per a saber si està trucada caldria llançar-la moltes més vegades (centenars o milers) i veure si $h$ s'acosta a 0,5.",
       r"\rest{No} necesariamente: 10 lanzamientos son muy pocos y la frecuencia relativa varía mucho. Para saber si está trucada habría que lanzarla muchas más veces (cientos o miles) y ver si $h$ se acerca a 0,5.")),
 (3, T(r"En una bossa hi ha 30 boles, roges i blanques. Traiem una bola, n'anotem el color i la tornem a la bossa. Després de 300 extraccions n'han eixit 120 de roges. Quantes boles roges deu haver-hi?",
       r"En una bolsa hay 30 bolas, rojas y blancas. Sacamos una bola, anotamos su color y la devolvemos a la bolsa. Después de 300 extracciones han salido 120 rojas. ¿Cuántas bolas rojas debe de haber?"),
     T(r"$P(R)\approx\frac{120}{300}=0{,}4$: més o menys, el 40 \% de les boles són roges. \ $30\cdot0{,}4=\res{12\text{ roges}}$ (i 18 blanques).",
       r"$P(R)\approx\frac{120}{300}=0{,}4$: más o menos, el 40 \% de las bolas son rojas. \ $30\cdot0{,}4=\res{12\text{ rojas}}$ (y 18 blancas).")),
 (3, T(r"Hem llançat un dau 1200 vegades: 1 → 150, 2 → 150, 3 → 150, 4 → 150, 5 → 200 i 6 → 400. Estima $P(6)$ i $P(\text{parell})$. Quants sisos esperes en 300 llançaments més? Està trucat?",
       r"Hemos lanzado un dado 1200 veces: 1 → 150, 2 → 150, 3 → 150, 4 → 150, 5 → 200 y 6 → 400. Estima $P(6)$ y $P(\text{par})$. ¿Cuántos seises esperas en 300 lanzamientos más? ¿Está trucado?"),
     T(r"$P(6)\approx\frac{400}{1200}=\res{\frac13}$; \ $P(\text{parell})\approx\frac{150+150+400}{1200}=\frac{700}{1200}=\res{\frac7{12}}\approx0{,}58$. \ $300\cdot\frac13=\res{100\text{ sisos}}$. \ \rest{Sí}: en un dau correcte esperaríem uns 200 de cada resultat.",
       r"$P(6)\approx\frac{400}{1200}=\res{\frac13}$; \ $P(\text{par})\approx\frac{150+150+400}{1200}=\frac{700}{1200}=\res{\frac7{12}}\approx0{,}58$. \ $300\cdot\frac13=\res{100\text{ seises}}$. \ \rest{Sí}: en un dado correcto esperaríamos unos 200 de cada resultado.")),
 (3, T(r"Un dau està trucat de manera que la probabilitat de cada cara és proporcional al seu nombre: $P(1)=p$, $P(2)=2p$, \dots, $P(6)=6p$. Calcula $p$, $P(6)$ i $P(\text{parell})$.",
       r"Un dado está trucado de manera que la probabilidad de cada cara es proporcional a su número: $P(1)=p$, $P(2)=2p$, \dots, $P(6)=6p$. Calcula $p$, $P(6)$ y $P(\text{par})$."),
     T(r"Les sis probabilitats sumen 1: $p+2p+\dots+6p=21p=1\Rightarrow p=\res{\frac1{21}}$. \ $P(6)=\frac6{21}=\res{\frac27}$. \ $P(\text{parell})=\frac{2+4+6}{21}=\frac{12}{21}=\res{\frac47}$.",
       r"Las seis probabilidades suman 1: $p+2p+\dots+6p=21p=1\Rightarrow p=\res{\frac1{21}}$. \ $P(6)=\frac6{21}=\res{\frac27}$. \ $P(\text{par})=\frac{2+4+6}{21}=\frac{12}{21}=\res{\frac47}$.")),
]))

# =====================================================================
# 4. Probabilitat en experiments regulars: llei de Laplace
# =====================================================================
for f, w in [(lambda x: x == 5, Fr(1, 6)), (lambda x: x % 2 == 0, Fr(1, 2)), (lambda x: x > 2, Fr(2, 3)), (lambda x: x % 3 == 0, Fr(1, 3)), (lambda x: x == 7, 0), (lambda x: x < 7, 1)]: ck(lap(D6, f), w)
ck(Fr(6, 15), Fr(2, 5)); ck(Fr(4, 15), Fr(4, 15)); ck(Fr(5, 15), Fr(1, 3)); ck(Fr(10, 15), Fr(2, 3))
ck(lap(U12, lambda x: x % 4 == 0), Fr(1, 4)); ck(lap(U12, isprime), Fr(5, 12)); ck(lap(U12, lambda x: 12 % x == 0), Fr(1, 2))
ck(Fr(10, 40), Fr(1, 4)); ck(Fr(4, 40), Fr(1, 10)); ck(Fr(3, 40), Fr(3, 40)); ck(Fr(28, 40), Fr(7, 10)); ck(Fr(13, 40), Fr(13, 40))
WM = T('MATEMATIQUES', 'MATEMATICAS')
NV, NM = sum(c in 'AEIOU' for c in WM), WM.count('M')
PV, PM = lap(WM, lambda c: c in 'AEIOU'), lap(WM, lambda c: c == 'M')
assert (len(WM), NV, NM) == T((12, 6, 2), (11, 5, 2))
ck(PV, T(Fr(1, 2), Fr(5, 11))); ck(PM, T(Fr(1, 6), Fr(2, 11)))
L100 = range(100); ck(lap(L100, lambda x: x % 10 == 7), Fr(1, 10)); ck(lap(L100, lambda x: x // 10 == x % 10), Fr(1, 10)); ck(lap(L100, lambda x: x > 89), Fr(1, 10))
ck(lap(range(1, 21), lambda x: x % 3 == 0 or x % 5 == 0), Fr(9, 20))
assert [x for x in range(0, 50) if Fr(x, 5 + x) == Fr(2, 3)] == [10]
pv = 1 - Fr(1, 4) - Fr(1, 3); ck(pv, Fr(5, 12)); assert 10 / pv == 24 and 24 * Fr(1, 4) == 6 and 24 * Fr(1, 3) == 8
ck(Fr(180, 360), Fr(1, 2)); ck(Fr(120, 360), Fr(1, 3)); ck(Fr(60, 360), Fr(1, 6))
RUL = (r'\begin{tikzpicture}[scale=0.75,baseline=(current bounding box.center)]\fill[red!60] (0,0) -- (0:1.3) arc[start angle=0,end angle=180,radius=1.3] -- cycle;'
       r'\fill[blue!55] (0,0) -- (180:1.3) arc[start angle=180,end angle=300,radius=1.3] -- cycle;\fill[teal!60] (0,0) -- (300:1.3) arc[start angle=300,end angle=360,radius=1.3] -- cycle;'
       r'\draw[thick] (0,0) circle (1.3);\draw (0,0)--(0:1.3) (0,0)--(180:1.3) (0,0)--(300:1.3);\node[font=\scriptsize\bfseries] at (90:0.7) {180°};\node[font=\scriptsize\bfseries,white] at (240:0.75) {120°};\node[font=\scriptsize\bfseries] at (330:0.8) {60°};\end{tikzpicture}')
VOC = T(r'A, E, A, I, U, E', r'A, E, A, I, A')
OLD.append((T("Probabilitat en experiments regulars: llei de Laplace", "Probabilidad en experimentos regulares: ley de Laplace"), [
 (1, T(r"Llancem un dau. Calcula la probabilitat de:", r"Lanzamos un dado. Calcula la probabilidad de:")
     + tasks(3, [T(r"traure un 5", r"sacar un 5"), T(r"traure parell", r"sacar par"), T(r"traure més de 2", r"sacar más de 2"), T(r"traure un múltiple de 3", r"sacar un múltiplo de 3"), T(r"traure un 7", r"sacar un 7"), T(r"traure menys de 7", r"sacar menos de 7")])
     + recorda(T(r"En un experiment \textbf{regular} (resultats equiprobables): \ $P(A)=\dfrac{\text{nombre de casos favorables}}{\text{nombre de casos possibles}}$.",
                 r"En un experimento \textbf{regular} (resultados equiprobables): \ $P(A)=\dfrac{\text{número de casos favorables}}{\text{número de casos posibles}}$.")),
     tasks(3, [r"$\res{\frac16}$", r"$\frac36=\res{\frac12}$", r"$\frac46=\res{\frac23}$", r"$\frac26=\res{\frac13}$", r"$\res{0}$ (%s)" % T('impossible', 'imposible'), r"$\res{1}$ (%s)" % T('segur', 'seguro')])),
 (1, T(r"En una bossa hi ha 6 boles roges, 4 de blaves i 5 de verdes. Traiem una bola a l'atzar. Calcula $P(\text{roja})$, $P(\text{blava})$, $P(\text{verda})$ i $P(\text{no verda})$.",
       r"En una bolsa hay 6 bolas rojas, 4 azules y 5 verdes. Sacamos una bola al azar. Calcula $P(\text{roja})$, $P(\text{azul})$, $P(\text{verde})$ y $P(\text{no verde})$.") + cen(bag('RRRRRRBBBBVVVVV', per=8)),
     T(r"Hi ha 15 boles: \ $P(\text{roja})=\frac6{15}=\res{\frac25}$, \ $P(\text{blava})=\res{\frac4{15}}$, \ $P(\text{verda})=\frac5{15}=\res{\frac13}$, \ $P(\text{no verda})=\frac{6+4}{15}=\res{\frac23}$.",
       r"Hay 15 bolas: \ $P(\text{roja})=\frac6{15}=\res{\frac25}$, \ $P(\text{azul})=\res{\frac4{15}}$, \ $P(\text{verde})=\frac5{15}=\res{\frac13}$, \ $P(\text{no verde})=\frac{6+4}{15}=\res{\frac23}$.")),
 (1, T(r"Girem una ruleta de 12 sectors iguals numerats de l'1 al 12. Calcula la probabilitat de traure: a) un múltiple de 4; b) un nombre primer; c) un divisor de 12.",
       r"Giramos una ruleta de 12 sectores iguales numerados del 1 al 12. Calcula la probabilidad de sacar: a) un múltiplo de 4; b) un número primo; c) un divisor de 12."),
     r"a) $\{4,8,12\}$: $\frac3{12}=\res{\frac14}$. \ b) $\{2,3,5,7,11\}$: $\res{\frac5{12}}$. \ c) $\{1,2,3,4,6,12\}$: $\frac6{12}=\res{\frac12}$."),
 (2, T(r"Traiem una carta d'una baralla espanyola de 40 cartes (oros, copes, espases i bastos, amb l'1 al 7, la sota, el cavall i el rei de cada pal). Calcula la probabilitat que siga:",
       r"Sacamos una carta de una baraja española de 40 cartas (oros, copas, espadas y bastos, con el 1 al 7, la sota, el caballo y el rey de cada palo). Calcula la probabilidad de que sea:")
     + tasks(3, [T(r"de copes", r"de copas"), T(r"un as", r"un as"), T(r"una figura d'espases", r"una figura de espadas"), T(r"una carta que no siga figura", r"una carta que no sea figura"), T(r"un as o un oro", r"un as o un oro"), T(r"el cavall de bastos", r"el caballo de bastos")]),
     tasks(3, [r"$\frac{10}{40}=\res{\frac14}$", r"$\frac4{40}=\res{\frac1{10}}$", r"$\res{\frac3{40}}$", r"$\frac{28}{40}=\res{\frac7{10}}$", T(r"$\frac{10+3}{40}=\res{\frac{13}{40}}$ (l'as d'oros, una vegada)", r"$\frac{10+3}{40}=\res{\frac{13}{40}}$ (el as de oros, una vez)"), r"$\res{\frac1{40}}$"])),
 (2, T(r"Escrivim cada lletra de la paraula MATEMATIQUES en una targeta i en traiem una a l'atzar. Quina és la probabilitat que siga una vocal? I una M? I una consonant?",
       r"Escribimos cada letra de la palabra MATEMATICAS en una tarjeta y sacamos una al azar. ¿Cuál es la probabilidad de que sea una vocal? ¿Y una M? ¿Y una consonante?"),
     T(r"12 lletres; vocals %s: \ $P(\text{vocal})=\frac{%d}{12}=\res{%s}$; \ $P(M)=\frac{%d}{12}=\res{%s}$; \ $P(\text{consonant})=\frac{%d}{12}=\res{%s}$." % (VOC, NV, fr(PV), NM, fr(PM), 12 - NV, fr(1 - PV)),
       r"11 letras; vocales %s: \ $P(\text{vocal})=\res{\frac{%d}{11}}$; \ $P(M)=\res{\frac{%d}{11}}$; \ $P(\text{consonante})=\res{\frac{%d}{11}}$." % (VOC, NV, NM, 11 - NV))),
 (2, T(r"En una rifa hi ha 100 paperetes numerades del 00 al 99. Calcula la probabilitat que la papereta premiada: a) acabe en 7; b) tinga les dues xifres iguals; c) siga més gran que 89.",
       r"En una rifa hay 100 papeletas numeradas del 00 al 99. Calcula la probabilidad de que la papeleta premiada: a) acabe en 7; b) tenga las dos cifras iguales; c) sea mayor que 89."),
     r"a) $07,17,\dots,97$: $\frac{10}{100}=\res{\frac1{10}}$. \ b) $00,11,\dots,99$: $\res{\frac1{10}}$. \ c) $90,\dots,99$: $\res{\frac1{10}}$."),
 (2, T(r"Traiem una bola d'un bombo amb boles numerades de l'1 al 20. Quina és la probabilitat que siga múltiple de 3 o de 5?", r"Sacamos una bola de un bombo con bolas numeradas del 1 al 20. ¿Cuál es la probabilidad de que sea múltiplo de 3 o de 5?"),
     T(r"$\{3,5,6,9,10,12,15,18,20\}$: 9 casos (el 15 només el comptem una vegada): \ $P=\res{\frac9{20}}$.", r"$\{3,5,6,9,10,12,15,18,20\}$: 9 casos (el 15 solo lo contamos una vez): \ $P=\res{\frac9{20}}$.")),
 (2, T(r"En Pau i la Maria juguen amb un dau: en Pau guanya si ix 5 o 6, i la Maria si ix 1, 2, 3 o 4. És just el joc? Com el canviaries perquè ho fóra?",
       r"Pablo y María juegan con un dado: Pablo gana si sale 5 o 6, y María si sale 1, 2, 3 o 4. ¿Es justo el juego? ¿Cómo lo cambiarías para que lo fuera?"),
     T(r"$P(\text{Pau})=\frac26=\frac13$ i $P(\text{Maria})=\frac46=\frac23$: \rest{no és just}. Per exemple: en Pau guanya amb parell i la Maria amb senar ($\frac12$ cadascun).",
       r"$P(\text{Pablo})=\frac26=\frac13$ y $P(\text{María})=\frac46=\frac23$: \rest{no es justo}. Por ejemplo: Pablo gana con par y María con impar ($\frac12$ cada uno).")),
 (3, T(r"En una bossa hi ha 5 boles roges i unes quantes de blaves. Si la probabilitat de traure una bola blava és $\frac23$, quantes boles blaves hi ha?",
       r"En una bolsa hay 5 bolas rojas y algunas azules. Si la probabilidad de sacar una bola azul es $\frac23$, ¿cuántas bolas azules hay?"),
     T(r"Si $P(\text{blava})=\frac23$, la roja té probabilitat $\frac13$: 1 de cada 3 boles és roja, així que hi ha $5\cdot3=15$ boles i $15-5=\res{10\text{ blaves}}$. \ (Comprovació: $\frac{10}{15}=\frac23$ \checkmark)",
       r"Si $P(\text{azul})=\frac23$, la roja tiene probabilidad $\frac13$: 1 de cada 3 bolas es roja, así que hay $5\cdot3=15$ bolas y $15-5=\res{10\text{ azules}}$. \ (Comprobación: $\frac{10}{15}=\frac23$ \checkmark)")),
 (3, T(r"En una bossa hi ha boles roges, blaves i 10 de verdes. Si $P(\text{roja})=\frac14$ i $P(\text{blava})=\frac13$, quantes boles hi ha de cada color?",
       r"En una bolsa hay bolas rojas, azules y 10 verdes. Si $P(\text{roja})=\frac14$ y $P(\text{azul})=\frac13$, ¿cuántas bolas hay de cada color?"),
     T(r"$P(\text{verda})=1-\frac14-\frac13=\frac5{12}$: 5 de cada 12 boles són verdes. Com que n'hi ha 10, hi ha 24 boles: \ \rest{6 roges, 8 blaves i 10 verdes}.",
       r"$P(\text{verde})=1-\frac14-\frac13=\frac5{12}$: 5 de cada 12 bolas son verdes. Como hay 10, hay 24 bolas: \ \rest{6 rojas, 8 azules y 10 verdes}.")),
 (3, T(r"Aquesta ruleta té tres sectors de 180°, 120° i 60°. És un experiment regular? Calcula la probabilitat de cada color.", r"Esta ruleta tiene tres sectores de 180°, 120° y 60°. ¿Es un experimento regular? Calcula la probabilidad de cada color.") + cen(RUL),
     T(r"\rest{No} és regular: els sectors no són iguals. La probabilitat és la fracció de cercle que ocupa cada sector: \ $P(\text{roig})=\frac{180}{360}=\res{\frac12}$, \ $P(\text{blau})=\frac{120}{360}=\res{\frac13}$, \ $P(\text{verd})=\frac{60}{360}=\res{\frac16}$.",
       r"\rest{No} es regular: los sectores no son iguales. La probabilidad es la fracción de círculo que ocupa cada sector: \ $P(\text{rojo})=\frac{180}{360}=\res{\frac12}$, \ $P(\text{azul})=\frac{120}{360}=\res{\frac13}$, \ $P(\text{verde})=\frac{60}{360}=\res{\frac16}$.")),
]))

# =====================================================================
# 5. Estratègies: diagrama d'arbre i taula de contingència
# =====================================================================
MD = list(product('CX', D6))
ck(lap(MD, lambda e: e == ('C', 3)), Fr(1, 12)); ck(lap(MD, lambda e: e[0] == 'X' and e[1] % 2 == 0), Fr(1, 4)); ck(lap(MD, lambda e: isprime(e[1])), Fr(1, 2))
ck(lap(DD, lambda e: sum(e) == 8), Fr(5, 36)); ck(lap(DD, lambda e: sum(e) == 2), Fr(1, 36)); ck(lap(DD, lambda e: sum(e) >= 10), Fr(1, 6)); ck(lap(DD, lambda e: sum(e) % 2 == 1), Fr(1, 2))
ck(lap(DD, lambda e: e[0] == e[1]), Fr(1, 6)); ck(lap(DD, lambda e: abs(e[0] - e[1]) == 2), Fr(2, 9)); ck(lap(DD, lambda e: e[0] * e[1] % 2 == 0), Fr(3, 4))
assert sum(1 for e in DD if e[0] * e[1] % 2 == 0) == 27
CC2 = list(product('CX', repeat=2)); ck(lap(CC2, lambda e: e == ('C', 'C')), Fr(1, 4)); ck(lap(CC2, lambda e: 'X' in e), Fr(3, 4))
CC3 = list(product('CX', repeat=3)); ck(lap(CC3, lambda e: e.count('C') == 3), Fr(1, 8)); ck(lap(CC3, lambda e: e.count('C') == 1), Fr(3, 8)); ck(lap(CC3, lambda e: e.count('C') >= 2), Fr(1, 2))
g = Fr(8, 10); ck(g * g, '0,64'); ck((1 - g) ** 2, '0,04'); ck(2 * g * (1 - g), '0,32')
ck(Fr(1, 4) ** 3, Fr(1, 64)); ck(Fr(3, 4) ** 3, Fr(27, 64)); ck(1 - Fr(27, 64), Fr(37, 64))
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
PB1 = two('BBBNN', True); ck(PB1['BB'], Fr(9, 25)); ck(PB1['NN'], Fr(4, 25)); ck(PB1['BN'] + PB1['NB'], Fr(12, 25))
PB2 = two('BBBNN', False); ck(PB2['BB'], Fr(3, 10)); ck(PB2['NN'], Fr(1, 10)); ck(PB2['BN'] + PB2['NB'], Fr(3, 5))
ck(Fr(1, 3) * Fr(3, 4) + Fr(2, 3) * Fr(1, 4), Fr(5, 12))
ck(Fr(4, 6) * Fr(3, 5) * Fr(2, 4), Fr(1, 5))
# taules de contingència
MA = [[8, 4], [6, 7]]   # files: xiques, xics · columnes: té mascota, no en té
assert sum(map(sum, MA)) == 25
ck(Fr(MA[0][0] + MA[1][0], 25), Fr(14, 25)); ck(Fr(MA[1][0], 25), Fr(6, 25)); ck(Fr(MA[0][0] + MA[0][1] + MA[1][0], 25), Fr(18, 25)); ck(Fr(MA[0][0], 12), Fr(2, 3))
FED = [[70, 110], [50, 170]]  # files: xics, xiques · columnes: federat, no
assert sum(FED[0]) == 180 and FED[0][0] + FED[1][0] == 120 and sum(map(sum, FED)) == 400
ck(Fr(120, 400), Fr(3, 10)); ck(Fr(50, 400), Fr(1, 8)); ck(Fr(220 + 120 - 50, 400), Fr(29, 40)); ck(Fr(50, 220), Fr(5, 22))
UL = [[20, 70], [40, 70]]  # files: homes, dones · columnes: ulleres, no
assert sum(UL[0]) == 90 and sum(UL[1]) == 110 and UL[0][0] + UL[1][0] == 60 and sum(map(sum, UL)) == 200
ck(Fr(200 * 45, 100), 90); ck(Fr(200 * 30, 100), 60)
ck(Fr(20, 200), Fr(1, 10)); ck(Fr(70, 200), Fr(7, 20)); ck(Fr(40, 60), Fr(2, 3))
TMD = tree([(c, '', [(str(d), '', [], '$%s%d$' % (c, d)) for d in D6]) for c in 'CX'], ld=13, sd=(24, 3.7), font=r'\scriptsize')
TC = tree([('C', r'\frac12', [('C', r'\frac12', [], r'$CC$: $\frac14$'), ('X', r'\frac12', [], r'$CX$: $\frac14$')]), ('X', r'\frac12', [('C', r'\frac12', [], r'$XC$: $\frac14$'), ('X', r'\frac12', [], r'$XX$: $\frac14$')])], ld=16, sd=(14, 7))
TG = tree([('G', '0{,}8', [('G', '0{,}8', [], r'$GG$: $0{,}64$'), ('F', '0{,}2', [], r'$GF$: $0{,}16$')]), ('F', '0{,}2', [('G', '0{,}8', [], r'$FG$: $0{,}16$'), ('F', '0{,}2', [], r'$FF$: $0{,}04$')])], ld=17, sd=(15, 7.5))
UR = tree([('I', r'\frac13', [('R*', r'\frac34', [], r'$\frac13\cdot\frac34=\frac14$'), ('B*', r'\frac14', [], '')]), ('II', r'\frac23', [('R*', r'\frac14', [], r'$\frac23\cdot\frac14=\frac16$'), ('B*', r'\frac34', [], '')])], ld=18, sd=(16, 8))
XQ, XC = T('Xiques', 'Chicas'), T('Xics', 'Chicos')
OLD.append((T("Estratègies: diagrama d'arbre i taula de contingència", "Estrategias: diagrama de árbol y tabla de contingencia"), [
 (1, T(r"Llancem una moneda i un dau. Fes el diagrama d'arbre. Quants resultats hi ha? Calcula la probabilitat de: a) cara i un 3; b) creu i un nombre parell; c) un nombre primer (amb cara o creu).",
       r"Lanzamos una moneda y un dado. Haz el diagrama de árbol. ¿Cuántos resultados hay? Calcula la probabilidad de: a) cara y un 3; b) cruz y un número par; c) un número primo (con cara o cruz).")
     + recorda(T(r"En un \textbf{diagrama d'arbre}, cada camí és un resultat. Si posem probabilitats a les branques, la probabilitat d'un camí és el \textbf{producte} de les seues branques; si un esdeveniment té diversos camins, les \textbf{sumem}.",
                 r"En un \textbf{diagrama de árbol}, cada camino es un resultado. Si ponemos probabilidades en las ramas, la probabilidad de un camino es el \textbf{producto} de sus ramas; si un suceso tiene varios caminos, las \textbf{sumamos}.")),
     cen(TMD) + T(r"$2\cdot6=\res{12}$ resultats equiprobables. \ a) $\frac1{12}$ (o bé $\frac12\cdot\frac16$) $=\res{\frac1{12}}$. \ b) $X2,X4,X6$: $\frac3{12}=\res{\frac14}$. \ c) $C2,C3,C5,X2,X3,X5$: $\frac6{12}=\res{\frac12}$.",
                  r"$2\cdot6=\res{12}$ resultados equiprobables. \ a) $\frac1{12}$ (o bien $\frac12\cdot\frac16$) $=\res{\frac1{12}}$. \ b) $X2,X4,X6$: $\frac3{12}=\res{\frac14}$. \ c) $C2,C3,C5,X2,X3,X5$: $\frac6{12}=\res{\frac12}$.")),
 (1, T(r"Llancem dues monedes. Fes el diagrama d'arbre amb les probabilitats i calcula la probabilitat de traure dues cares i la de traure almenys una creu.",
       r"Lanzamos dos monedas. Haz el diagrama de árbol con las probabilidades y calcula la probabilidad de sacar dos caras y la de sacar al menos una cruz."),
     cen(TC) + T(r"$P(CC)=\frac12\cdot\frac12=\res{\frac14}$. \ «Almenys una creu» són 3 camins ($CX$, $XC$, $XX$): $\frac14+\frac14+\frac14=\res{\frac34}$.",
                 r"$P(CC)=\frac12\cdot\frac12=\res{\frac14}$. \ «Al menos una cruz» son 3 caminos ($CX$, $XC$, $XX$): $\frac14+\frac14+\frac14=\res{\frac34}$.")),
 (1, T(r"Llancem dos daus i sumem els punts. Completa la taula de doble entrada i calcula la probabilitat que la suma siga: a) 8; b) 2; c) 10 o més; d) senar.",
       r"Lanzamos dos dados y sumamos los puntos. Completa la tabla de doble entrada y calcula la probabilidad de que la suma sea: a) 8; b) 2; c) 10 o más; d) impar."),
     cen(dtab(lambda a, b: a + b, lambda a, b: a + b == 8)) + T(r"a) $\res{\frac5{36}}$ (marcades). \ b) $\res{\frac1{36}}$. \ c) $\frac{3+2+1}{36}=\res{\frac16}$. \ d) $\frac{18}{36}=\res{\frac12}$.",
                                                                 r"a) $\res{\frac5{36}}$ (marcadas). \ b) $\res{\frac1{36}}$. \ c) $\frac{3+2+1}{36}=\res{\frac16}$. \ d) $\frac{18}{36}=\res{\frac12}$.")),
 (1, T(r"En una classe de 25 alumnes hem preguntat qui té mascota. Triem un alumne a l'atzar. Calcula: a) $P(\text{té mascota})$; b) $P(\text{xic i té mascota})$; c) $P(\text{xica o té mascota})$; d) si sabem que és una xica, la probabilitat que tinga mascota.",
       r"En una clase de 25 alumnos hemos preguntado quién tiene mascota. Elegimos un alumno al azar. Calcula: a) $P(\text{tiene mascota})$; b) $P(\text{chico y tiene mascota})$; c) $P(\text{chica o tiene mascota})$; d) si sabemos que es una chica, la probabilidad de que tenga mascota.")
     + cen(cont([XQ, XC], [T('Mascota', 'Mascota'), T('Sense mascota', 'Sin mascota')], MA))
     + recorda(T(r"En una \textbf{taula de contingència}, els casos possibles són el total (o el total d'una fila, si ja sabem en quina fila està la persona) i els favorables, les caselles que compleixen el que demanen.",
                 r"En una \textbf{tabla de contingencia}, los casos posibles son el total (o el total de una fila, si ya sabemos en qué fila está la persona) y los favorables, las casillas que cumplen lo que piden.")),
     T(r"a) $\frac{8+6}{25}=\res{\frac{14}{25}}$. \ b) $\res{\frac6{25}}$. \ c) $\frac{8+4+6}{25}=\res{\frac{18}{25}}$. \ d) Només les 12 xiques: $\frac8{12}=\res{\frac23}$.",
       r"a) $\frac{8+6}{25}=\res{\frac{14}{25}}$. \ b) $\res{\frac6{25}}$. \ c) $\frac{8+4+6}{25}=\res{\frac{18}{25}}$. \ d) Solo las 12 chicas: $\frac8{12}=\res{\frac23}$.")),
 (2, T(r"Llancem dos daus. Calcula la probabilitat que: a) traguen el mateix nombre; b) la diferència entre el major i el menor siga 2; c) el producte siga parell.",
       r"Lanzamos dos dados. Calcula la probabilidad de que: a) saquen el mismo número; b) la diferencia entre el mayor y el menor sea 2; c) el producto sea par."),
     T(r"a) $\frac6{36}=\res{\frac16}$. \ b) $(1,3),(2,4),(3,5),(4,6)$ i al revés: $\frac8{36}=\res{\frac29}$. \ c) Amb la taula dels productes, 27 caselles són parelles: $\frac{27}{36}=\res{\frac34}$.",
       r"a) $\frac6{36}=\res{\frac16}$. \ b) $(1,3),(2,4),(3,5),(4,6)$ y al revés: $\frac8{36}=\res{\frac29}$. \ c) Con la tabla de los productos, 27 casillas son pares: $\frac{27}{36}=\res{\frac34}$.")),
 (2, T(r"Llancem tres monedes. Calcula la probabilitat de: a) tres cares; b) exactament una cara; c) almenys dues cares.", r"Lanzamos tres monedas. Calcula la probabilidad de: a) tres caras; b) exactamente una cara; c) al menos dos caras."),
     T(r"Cada camí de l'arbre té probabilitat $\frac12\cdot\frac12\cdot\frac12=\frac18$. \ a) $\res{\frac18}$. \ b) $CXX$, $XCX$, $XXC$: $\res{\frac38}$. \ c) $CCC$, $CCX$, $CXC$, $XCC$: $\frac48=\res{\frac12}$.",
       r"Cada camino del árbol tiene probabilidad $\frac12\cdot\frac12\cdot\frac12=\frac18$. \ a) $\res{\frac18}$. \ b) $CXX$, $XCX$, $XXC$: $\res{\frac38}$. \ c) $CCC$, $CCX$, $CXC$, $XCC$: $\frac48=\res{\frac12}$.")),
 (2, T(r"Una jugadora de futbol marca el 80 \% dels penals. En llança dos. Fes el diagrama d'arbre i calcula la probabilitat que marque tots dos, que no en marque cap i que en marque exactament un.",
       r"Una jugadora de fútbol marca el 80 \% de los penaltis. Lanza dos. Haz el diagrama de árbol y calcula la probabilidad de que marque los dos, de que no marque ninguno y de que marque exactamente uno."),
     cen(TG) + T(r"$P(GG)=\res{0{,}64}$; \ $P(FF)=\res{0{,}04}$; \ $P(\text{exactament un})=0{,}16+0{,}16=\res{0{,}32}$. \ (Sumen 1 \checkmark)", r"$P(GG)=\res{0{,}64}$; \ $P(FF)=\res{0{,}04}$; \ $P(\text{exactamente uno})=0{,}16+0{,}16=\res{0{,}32}$. \ (Suman 1 \checkmark)")),
 (2, T(r"En una bossa hi ha 3 boles blanques (B) i 2 de negres (N). En traiem dues \textbf{amb reemplaçament}. Fes el diagrama d'arbre i calcula la probabilitat que: a) les dues siguen blanques; b) les dues siguen negres; c) n'isca una de cada color.",
       r"En una bolsa hay 3 bolas blancas (B) y 2 negras (N). Sacamos dos \textbf{con reemplazamiento}. Haz el diagrama de árbol y calcula la probabilidad de que: a) las dos sean blancas; b) las dos sean negras; c) salga una de cada color.")
     + recorda(T(r"\textbf{Amb reemplaçament} tornem la bola a la bossa: la segona extracció té les mateixes probabilitats. \textbf{Sense reemplaçament} no la tornem: en la segona extracció hi ha una bola menys.",
                 r"\textbf{Con reemplazamiento} devolvemos la bola a la bolsa: la segunda extracción tiene las mismas probabilidades. \textbf{Sin reemplazamiento} no la devolvemos: en la segunda extracción hay una bola menos.")),
     cen(btree(3, 2, True)) + r"a) $\frac35\cdot\frac35=\res{\frac9{25}}$. \ b) $\frac25\cdot\frac25=\res{\frac4{25}}$. \ c) $\frac6{25}+\frac6{25}=\res{\frac{12}{25}}$."),
 (2, T(r"Resol l'exercici anterior traient les dues boles \textbf{sense reemplaçament}.", r"Resuelve el ejercicio anterior sacando las dos bolas \textbf{sin reemplazamiento}."),
     cen(btree(3, 2, False)) + T(r"a) $\frac35\cdot\frac24=\res{\frac3{10}}$. \ b) $\frac25\cdot\frac14=\res{\frac1{10}}$. \ c) $\frac3{10}+\frac3{10}=\res{\frac35}$. \ (Sumen 1 \checkmark)",
                                 r"a) $\frac35\cdot\frac24=\res{\frac3{10}}$. \ b) $\frac25\cdot\frac14=\res{\frac1{10}}$. \ c) $\frac3{10}+\frac3{10}=\res{\frac35}$. \ (Suman 1 \checkmark)")),
 (2, T(r"En un institut hi ha 400 alumnes, dels quals 180 són xics. Fan esport federat 120 alumnes, 70 dels quals són xics. Completa la taula i, si triem una persona a l'atzar, calcula: a) $P(\text{esport federat})$; b) $P(\text{xica i esport federat})$; c) $P(\text{xica o esport federat})$; d) si sabem que és una xica, la probabilitat que faça esport federat.",
       r"En un instituto hay 400 alumnos, de los cuales 180 son chicos. Hacen deporte federado 120 alumnos, 70 de los cuales son chicos. Completa la tabla y, si elegimos una persona al azar, calcula: a) $P(\text{deporte federado})$; b) $P(\text{chica y deporte federado})$; c) $P(\text{chica o deporte federado})$; d) si sabemos que es una chica, la probabilidad de que haga deporte federado.")
     + cen(cont([XC, XQ], [T('Federat', 'Federado'), T('No federat', 'No federado')], FED, blank={(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)})),
     cen(cont([XC, XQ], [T('Federat', 'Federado'), T('No federat', 'No federado')], FED)) + T(r"a) $\frac{120}{400}=\res{\frac3{10}}$. \ b) $\frac{50}{400}=\res{\frac18}$. \ c) $\frac{50+170+70}{400}=\frac{290}{400}=\res{\frac{29}{40}}$. \ d) Només comptem les 220 xiques: $\frac{50}{220}=\res{\frac5{22}}$.",
                                                                                                 r"a) $\frac{120}{400}=\res{\frac3{10}}$. \ b) $\frac{50}{400}=\res{\frac18}$. \ c) $\frac{50+170+70}{400}=\frac{290}{400}=\res{\frac{29}{40}}$. \ d) Solo contamos las 220 chicas: $\frac{50}{220}=\res{\frac5{22}}$.")),
 (3, T(r"La urna I té 3 boles roges i 1 de blava; la urna II té 1 bola roja i 3 de blaves. Llancem un dau: si ix 1 o 2, traiem una bola de la urna I, i si no, de la urna II. Quina és la probabilitat de traure una bola roja?",
       r"La urna I tiene 3 bolas rojas y 1 azul; la urna II tiene 1 bola roja y 3 azules. Lanzamos un dado: si sale 1 o 2, sacamos una bola de la urna I, y si no, de la urna II. ¿Cuál es la probabilidad de sacar una bola roja?"),
     cen(UR) + r"$P(R)=\frac13\cdot\frac34+\frac23\cdot\frac14=\frac14+\frac16=\res{\frac5{12}}$."),
 (3, T(r"En una bossa hi ha 4 boles roges i 2 de blaves. En traiem tres, una darrere l'altra, sense reemplaçament. Quina és la probabilitat que les tres siguen roges?",
       r"En una bolsa hay 4 bolas rojas y 2 azules. Sacamos tres, una detrás de otra, sin reemplazamiento. ¿Cuál es la probabilidad de que las tres sean rojas?"),
     r"$\frac46\cdot\frac35\cdot\frac24=\frac{24}{120}=\res{\frac15}$."),
 (3, T(r"En un grup de 200 persones, el 45 \% són homes i el 30 \% porta ulleres. De les persones amb ulleres, 40 són dones. Fes la taula de contingència i calcula la probabilitat que una persona triada a l'atzar: a) siga un home amb ulleres; b) siga una dona sense ulleres; c) siga una dona, si sabem que porta ulleres.",
       r"En un grupo de 200 personas, el 45 \% son hombres y el 30 \% lleva gafas. De las personas con gafas, 40 son mujeres. Haz la tabla de contingencia y calcula la probabilidad de que una persona elegida al azar: a) sea un hombre con gafas; b) sea una mujer sin gafas; c) sea una mujer, si sabemos que lleva gafas."),
     T(r"Homes: $45\,\%$ de 200 $=90$; dones: 110; amb ulleres: $30\,\%$ de 200 $=60$.", r"Hombres: $45\,\%$ de 200 $=90$; mujeres: 110; con gafas: $30\,\%$ de 200 $=60$.")
     + cen(cont([T('Homes', 'Hombres'), T('Dones', 'Mujeres')], [T('Ulleres', 'Gafas'), T('Sense ulleres', 'Sin gafas')], UL))
     + T(r"a) $\frac{20}{200}=\res{\frac1{10}}$. \ b) $\frac{70}{200}=\res{\frac7{20}}$. \ c) Ara els casos possibles són les 60 persones amb ulleres: $\frac{40}{60}=\res{\frac23}$.",
         r"a) $\frac{20}{200}=\res{\frac1{10}}$. \ b) $\frac{70}{200}=\res{\frac7{20}}$. \ c) Ahora los casos posibles son las 60 personas con gafas: $\frac{40}{60}=\res{\frac23}$.")),
 (3, T(r"Un examen tipus test té 3 preguntes amb 4 opcions cadascuna (només una correcta). Si les contestes totes a l'atzar, quina és la probabilitat d'encertar-les totes? I de no encertar-ne cap? I d'encertar-ne almenys una?",
       r"Un examen tipo test tiene 3 preguntas con 4 opciones cada una (solo una correcta). Si las contestas todas al azar, ¿cuál es la probabilidad de acertarlas todas? ¿Y de no acertar ninguna? ¿Y de acertar al menos una?"),
     T(r"En l'arbre, cada pregunta té les branques E ($\frac14$) i F ($\frac34$). \ $P(EEE)=\frac14\cdot\frac14\cdot\frac14=\res{\frac1{64}}$. \ $P(FFF)=\frac34\cdot\frac34\cdot\frac34=\res{\frac{27}{64}}$. \ Tots els camins sumen 1: $P(\text{almenys una})=1-\frac{27}{64}=\res{\frac{37}{64}}$.",
       r"En el árbol, cada pregunta tiene las ramas A ($\frac14$) y F ($\frac34$). \ $P(AAA)=\frac14\cdot\frac14\cdot\frac14=\res{\frac1{64}}$. \ $P(FFF)=\frac34\cdot\frac34\cdot\frac34=\res{\frac{27}{64}}$. \ Todos los caminos suman 1: $P(\text{al menos una})=1-\frac{27}{64}=\res{\frac{37}{64}}$.")),
]))


# =====================================================================
# Fitxa de 4t ESO A: les 7 seccions dels apunts (11.1-11.7). Molts exercicis són els de la fitxa de 2n ESO (llista OLD,
# per seccions de 2n i ordre dins de cada secció); s'hi afigen exercicis nous d'operacions amb esdeveniments, contrari i
# unió, independència, probabilitat condicionada i taules de contingència a partir de percentatges.
# =====================================================================
def O(s, k): return OLD[s][1][k]
RC_OPS = recorda(T(r"$A\cup B$ («$A$ o $B$»): elements d'$A$ o de $B$. \ $A\cap B$ («$A$ i $B$»): elements comuns. \ $\overline{A}$ («no $A$»): elements de $E$ que no són en $A$. Si $A\cap B=\varnothing$, són \textbf{incompatibles}.",
                   r"$A\cup B$ («$A$ o $B$»): elementos de $A$ o de $B$. \ $A\cap B$ («$A$ y $B$»): elementos comunes. \ $\overline{A}$ («no $A$»): elementos de $E$ que no están en $A$. Si $A\cap B=\varnothing$, son \textbf{incompatibles}."))
RC_PROP = recorda(T(r"$P(\overline{A})=1-P(A)$ \qquad $P(A\cup B)=P(A)+P(B)-P(A\cap B)$ \qquad Si són incompatibles, $P(A\cup B)=P(A)+P(B)$.",
                    r"$P(\overline{A})=1-P(A)$ \qquad $P(A\cup B)=P(A)+P(B)-P(A\cap B)$ \qquad Si son incompatibles, $P(A\cup B)=P(A)+P(B)$."))
RC_IND = recorda(T(r"Si dues experiències són \textbf{independents}, $P(A\cap B)=P(A)\cdot P(B)$. Per a «almenys un», sovint és més ràpid el contrari: $P(\text{almenys un})=1-P(\text{cap})$.",
                   r"Si dos experiencias son \textbf{independientes}, $P(A\cap B)=P(A)\cdot P(B)$. Para «al menos uno», a menudo es más rápido el contrario: $P(\text{al menos uno})=1-P(\text{ninguno})$."))
RC_COND = recorda(T(r"$P(B/A)$ és la probabilitat de $B$ \textbf{sabent que} ha passat $A$; en l'arbre, és la branca de la segona etapa. \ $P(A\cap B)=P(A)\cdot P(B/A)$.",
                    r"$P(B/A)$ es la probabilidad de $B$ \textbf{sabiendo que} ha pasado $A$; en el árbol, es la rama de la segunda etapa. \ $P(A\cap B)=P(A)\cdot P(B/A)$."))
RC_TAB = recorda(T(r"En una taula de contingència, $P(A/B)=\dfrac{\text{casos de }A\text{ i }B}{\text{casos de }B}=\dfrac{P(A\cap B)}{P(B)}$: només comptem en la fila o la columna de la condició.",
                   r"En una tabla de contingencia, $P(A/B)=\dfrac{\text{casos de }A\text{ y }B}{\text{casos de }B}=\dfrac{P(A\cap B)}{P(B)}$: solo contamos en la fila o la columna de la condición."))

# ---------- comprovacions dels exercicis nous ----------
def st(xs): return r'\{' + r',\,'.join(str(x) for x in xs) + r'\}' if xs else r'\varnothing'
A1, B1 = [x for x in D6 if x % 3 == 0], [x for x in D6 if x < 3]
assert (A1, B1) == ([3, 6], [1, 2])
U1, I1, NA1, NB1 = sorted(set(A1) | set(B1)), sorted(set(A1) & set(B1)), [x for x in D6 if x not in A1], [x for x in D6 if x not in B1]
assert U1 == [1, 2, 3, 6] and I1 == [] and NA1 == [1, 2, 4, 5] and NB1 == [3, 4, 5, 6]
U10 = range(1, 11); A2, B2 = [x for x in U10 if x % 2 == 0], [x for x in U10 if isprime(x)]
assert sorted(set(A2) | set(B2)) == [2, 3, 4, 5, 6, 7, 8, 10] and sorted(set(A2) & set(B2)) == [2]
assert [x for x in U10 if x not in A2] == [1, 3, 5, 7, 9] and [x for x in U10 if x not in B2] == [1, 4, 6, 8, 9, 10]
assert 10 + 4 - 1 == 13 and 40 - 10 == 30
M3 = [''.join(p) for p in product('CX', repeat=3)]
A3 = [e for e in M3 if e.count('C') >= 2]; B3 = [e for e in M3 if e[0] == 'X']
assert A3 == ['CCC', 'CCX', 'CXC', 'XCC'] and B3 == ['XCC', 'XCX', 'XXC', 'XXX'] and [e for e in A3 if e in B3] == ['XCC']
assert [e for e in M3 if e not in A3 and e not in B3] == ['CXX'] and [e for e in M3 if e not in A3] == ['CXX', 'XCX', 'XXC', 'XXX']
A4, B4 = [x for x in U12 if x % 2 == 0], [x for x in U12 if x % 3 == 0]
assert [x for x in A4 if x not in B4] == [2, 4, 8, 10] and [x for x in U12 if x not in A4 and x not in B4] == [1, 5, 7, 11]
assert [x for x in U12 if x not in sorted(set(A4) | set(B4))] == [1, 5, 7, 11]
ck(1 - Fr(62, 100), '0,38'); ck(1 - Fr(3, 7), Fr(4, 7)); assert 100 - 15 == 85
ck(Fr(4, 10) + Fr(5, 10) - Fr(15, 100), '0,75'); ck(1 - Fr(75, 100), '0,25'); ck(Fr(4, 10) - Fr(15, 100), '0,25')
ck(Fr(3, 10) + Fr(45, 100), '0,75'); assert Fr(6, 10) + Fr(5, 10) > 1
pA, pB = 1 - Fr(3, 10), 1 - Fr(4, 10); ck(pA, '0,7'); ck(pB, '0,6'); ck(pA + pB - Fr(9, 10), '0,4')
ck(Fr(3, 10) * Fr(6, 10), '0,18'); ck(Fr(7, 10) * Fr(4, 10), '0,28'); ck(1 - Fr(28, 100), '0,72')
ck(Fr(3, 10) * Fr(4, 10) + Fr(7, 10) * Fr(6, 10), '0,54')
ck(1 - Fr(5, 6) ** 3, Fr(91, 216)); assert abs(float(Fr(91, 216)) - 0.42) < 0.005
NMIN = [n for n in range(1, 10) if 1 - Fr(5, 6) ** n > Fr(1, 2)][0]; assert NMIN == 4 and Fr(5, 6) ** 4 == Fr(625, 1296)
ck(Fr(4, 7), Fr(4, 7)); ck(Fr(3, 7), Fr(3, 7))
ck(Fr(9, 39), Fr(3, 13)); ck(Fr(10, 40) * Fr(9, 39), Fr(3, 52))
ck(Fr(6, 10) * Fr(75, 100), '0,45'); ck(Fr(6, 10) * Fr(75, 100) + Fr(4, 10) * Fr(25, 100), '0,55'); ck(Fr(4, 10) * Fr(75, 100), '0,3')
ck(1 - Fr(3, 5) * Fr(2, 4), Fr(7, 10))
VCm = [[12, 228], [48, 112]]
assert sum(VCm[0]) == 240 and VCm[0][0] == Fr(5, 100) * 240 and VCm[1][0] == Fr(30, 100) * 160
ck(Fr(60, 400), '0,15'); ck(Fr(12, 240), '0,05'); ck(Fr(48, 160), '0,3'); ck(Fr(12, 60), Fr(1, 5))
IPm = [[12, 18], [8, 12]]; ck(Fr(20, 50), Fr(2, 5)); ck(Fr(12, 30), Fr(2, 5)); ck(Fr(8, 20), Fr(2, 5))
TGm = [[140, 560], [30, 270]]; assert sum(TGm[0]) == 700 and TGm[0][0] == Fr(20, 100) * 700 and TGm[1][0] == Fr(10, 100) * 300
ck(Fr(170, 1000), '0,17'); ck(Fr(140, 170), Fr(14, 17))

TPL = tree([('D', '0{,}3', [('D', '0{,}6', [], r'$0{,}18$'), (r'$\overline{D}$', '0{,}4', [], r'$0{,}12$')]), (r'$\overline{D}$', '0{,}7', [('D', '0{,}6', [], r'$0{,}42$'), (r'$\overline{D}$', '0{,}4', [], r'$0{,}28$')])], ld=17, sd=(15, 7))
TMFm = tree([('M', '0{,}6', [('F', '0{,}75', [], r'$0{,}45$'), (r'$\overline{F}$', '0{,}25', [], r'$0{,}15$')]), (r'$\overline{M}$', '0{,}4', [('F', '0{,}25', [], r'$0{,}1$'), (r'$\overline{F}$', '0{,}75', [], r'$0{,}3$')])], ld=19, sd=(15, 7))
TVm = tree([('V', '0{,}6', [('G', '0{,}05', [], r'$0{,}03$'), (r'$\overline{G}$', '0{,}95', [], r'$0{,}57$')]), (r'$\overline{V}$', '0{,}4', [('G', '0{,}3', [], r'$0{,}12$'), (r'$\overline{G}$', '0{,}7', [], r'$0{,}28$')])], ld=19, sd=(15, 7))
VAC, NVAC, GR, NGR = T('Vacunats', 'Vacunados'), T('No vacunats', 'No vacunados'), T('Grip', 'Gripe'), T('Sense grip', 'Sin gripe')

S_ = []
S_.append((T("Experiments", "Experimentos"), [
 O(0, 0), O(0, 2), O(1, 0), O(0, 5), O(1, 3), O(1, 5), O(1, 6), O(1, 8)]))

S_.append((T("Esdeveniments", "Sucesos"), [
 O(1, 1), O(1, 2),
 (1, T(r"Llancem un dau. Siguen $A=$ «múltiple de 3» i $B=$ «menor que 3». Calcula $A\cup B$, $A\cap B$, $\overline{A}$ i $\overline{B}$. Són incompatibles? Són contraris?",
       r"Lanzamos un dado. Sean $A=$ «múltiplo de 3» y $B=$ «menor que 3». Calcula $A\cup B$, $A\cap B$, $\overline{A}$ y $\overline{B}$. ¿Son incompatibles? ¿Son contrarios?") + RC_OPS,
     T(r"$A=%s$, $B=%s$: \ $A\cup B=\res{%s}$, \ $A\cap B=\res{%s}$, \ $\overline{A}=\res{%s}$, \ $\overline{B}=\res{%s}$. \ Són \rest{incompatibles}, però \rest{no són contraris}: si ix un 4 o un 5, no ocorre cap dels dos.",
       r"$A=%s$, $B=%s$: \ $A\cup B=\res{%s}$, \ $A\cap B=\res{%s}$, \ $\overline{A}=\res{%s}$, \ $\overline{B}=\res{%s}$. \ Son \rest{incompatibles}, pero \rest{no son contrarios}: si sale un 4 o un 5, no ocurre ninguno de los dos.") % (st(A1), st(B1), st(U1), st(I1), st(NA1), st(NB1))),
 (1, T(r"En una urna hi ha deu boles numerades de l'1 al 10. Siguen $A=$ «parell» i $B=$ «primer». Calcula $A\cup B$, $A\cap B$, $\overline{A}$ i $\overline{B}$.",
       r"En una urna hay diez bolas numeradas del 1 al 10. Sean $A=$ «par» y $B=$ «primo». Calcula $A\cup B$, $A\cap B$, $\overline{A}$ y $\overline{B}$."),
     r"$A=\{2,4,6,8,10\}$, $B=\{2,3,5,7\}$: \ $A\cup B=\res{\{2,3,4,5,6,7,8,10\}}$, \ $A\cap B=\res{\{2\}}$, \ $\overline{A}=\res{\{1,3,5,7,9\}}$, \ $\overline{B}=\res{\{1,4,6,8,9,10\}}$."),
 (2, T(r"Traiem una carta d'una baralla espanyola de 40 cartes. Siguen $O=$ «oros» i $A=$ «as». Quantes cartes té cada un d'aquests esdeveniments: $O\cap A$, $O\cup A$ i $\overline{O}$?",
       r"Sacamos una carta de una baraja española de 40 cartas. Sean $O=$ «oros» y $A=$ «as». ¿Cuántas cartas tiene cada uno de estos sucesos: $O\cap A$, $O\cup A$ y $\overline{O}$?"),
     T(r"$O\cap A$ = l'as d'oros: \res{1 carta}. \ $O\cup A$ = els 10 oros i els altres 3 asos: $10+4-1=\res{13\text{ cartes}}$. \ $\overline{O}$ = les que no són d'oros: $40-10=\res{30\text{ cartes}}$.",
       r"$O\cap A$ = el as de oros: \res{1 carta}. \ $O\cup A$ = los 10 oros y los otros 3 ases: $10+4-1=\res{13\text{ cartas}}$. \ $\overline{O}$ = las que no son de oros: $40-10=\res{30\text{ cartas}}$.")),
 (2, T(r"Llancem tres monedes. Siguen $A=$ «almenys dues cares» i $B=$ «la primera és creu». Escriu $A$, $B$, $A\cap B$, $A\cup B$ i $\overline{A}$.",
       r"Lanzamos tres monedas. Sean $A=$ «al menos dos caras» y $B=$ «la primera es cruz». Escribe $A$, $B$, $A\cap B$, $A\cup B$ y $\overline{A}$."),
     T(r"$A=\{CCC,\,CCX,\,CXC,\,XCC\}$, \ $B=\{XCC,\,XCX,\,XXC,\,XXX\}$. \ $A\cap B=\res{\{XCC\}}$; \ $A\cup B$: tots els resultats menys $CXX$ (\res{7 resultats}); \ $\overline{A}=\res{\{CXX,\,XCX,\,XXC,\,XXX\}}$.",
       r"$A=\{CCC,\,CCX,\,CXC,\,XCC\}$, \ $B=\{XCC,\,XCX,\,XXC,\,XXX\}$. \ $A\cap B=\res{\{XCC\}}$; \ $A\cup B$: todos los resultados menos $CXX$ (\res{7 resultados}); \ $\overline{A}=\res{\{CXX,\,XCX,\,XXC,\,XXX\}}$.")),
 (3, T(r"Traiem una bola d'una urna amb boles de l'1 al 12. Siguen $A=$ «múltiple de 2» i $B=$ «múltiple de 3». Escriu amb operacions i calcula: a) «és múltiple de 2 però no de 3»; b) «no és múltiple ni de 2 ni de 3». Comprova que b) és el contrari d'$A\cup B$.",
       r"Sacamos una bola de una urna con bolas del 1 al 12. Sean $A=$ «múltiplo de 2» y $B=$ «múltiplo de 3». Escribe con operaciones y calcula: a) «es múltiplo de 2 pero no de 3»; b) «no es múltiplo ni de 2 ni de 3». Comprueba que b) es el contrario de $A\cup B$."),
     T(r"$A=\{2,4,6,8,10,12\}$, $B=\{3,6,9,12\}$. \ a) $A\cap\overline{B}=\res{\{2,4,8,10\}}$. \ b) $\overline{A}\cap\overline{B}=\res{\{1,5,7,11\}}$. \ $A\cup B=\{2,3,4,6,8,9,10,12\}$, i el seu contrari és $\{1,5,7,11\}$ \checkmark",
       r"$A=\{2,4,6,8,10,12\}$, $B=\{3,6,9,12\}$. \ a) $A\cap\overline{B}=\res{\{2,4,8,10\}}$. \ b) $\overline{A}\cap\overline{B}=\res{\{1,5,7,11\}}$. \ $A\cup B=\{2,3,4,6,8,9,10,12\}$, y su contrario es $\{1,5,7,11\}$ \checkmark")),
]))

S_.append((T("Probabilitat d'un esdeveniment", "Probabilidad de un suceso"), [
 O(2, 0), O(2, 1),
 (1, T(r"Calcula la probabilitat de l'esdeveniment contrari:", r"Calcula la probabilidad del suceso contrario:")
     + tasks(3, [r"$P(A)=0{,}62$", r"$P(B)=\frac37$", r"$P(C)=15\,\%$"]) + RC_PROP,
     tasks(3, [r"$P(\overline{A})=\res{0{,}38}$", r"$P(\overline{B})=\res{\frac47}$", r"$P(\overline{C})=\res{85\,\%}$"])),
 O(2, 3), O(2, 4), O(2, 6),
 (2, T(r"Siguen $A$ i $B$ dos esdeveniments amb $P(A)=0{,}4$, $P(B)=0{,}5$ i $P(A\cap B)=0{,}15$. Calcula $P(A\cup B)$, la probabilitat que no ocórrega cap dels dos i la probabilitat que ocórrega $A$ però no $B$.",
       r"Sean $A$ y $B$ dos sucesos con $P(A)=0{,}4$, $P(B)=0{,}5$ y $P(A\cap B)=0{,}15$. Calcula $P(A\cup B)$, la probabilidad de que no ocurra ninguno de los dos y la probabilidad de que ocurra $A$ pero no $B$."),
     r"$P(A\cup B)=0{,}4+0{,}5-0{,}15=\res{0{,}75}$. \ $P(\overline{A\cup B})=1-0{,}75=\res{0{,}25}$. \ $P(A\cap\overline{B})=0{,}4-0{,}15=\res{0{,}25}$."),
 (2, T(r"a) $A$ i $B$ són incompatibles, amb $P(A)=0{,}3$ i $P(B)=0{,}45$. Calcula $P(A\cup B)$. \ b) Poden ser incompatibles dos esdeveniments amb $P(A)=0{,}6$ i $P(B)=0{,}5$? Per què?",
       r"a) $A$ y $B$ son incompatibles, con $P(A)=0{,}3$ y $P(B)=0{,}45$. Calcula $P(A\cup B)$. \ b) ¿Pueden ser incompatibles dos sucesos con $P(A)=0{,}6$ y $P(B)=0{,}5$? ¿Por qué?"),
     T(r"a) $P(A\cup B)=0{,}3+0{,}45=\res{0{,}75}$. \ b) \rest{No}: si foren incompatibles, $P(A\cup B)=0{,}6+0{,}5=1{,}1>1$, i això és impossible.",
       r"a) $P(A\cup B)=0{,}3+0{,}45=\res{0{,}75}$. \ b) \rest{No}: si fueran incompatibles, $P(A\cup B)=0{,}6+0{,}5=1{,}1>1$, y eso es imposible.")),
 O(2, 8),
 (3, T(r"Sabem que $P(A\cup B)=0{,}9$, $P(\overline{A})=0{,}3$ i $P(\overline{B})=0{,}4$. Calcula $P(A)$, $P(B)$ i $P(A\cap B)$. Són incompatibles?",
       r"Sabemos que $P(A\cup B)=0{,}9$, $P(\overline{A})=0{,}3$ y $P(\overline{B})=0{,}4$. Calcula $P(A)$, $P(B)$ y $P(A\cap B)$. ¿Son incompatibles?"),
     T(r"$P(A)=1-0{,}3=\res{0{,}7}$; \ $P(B)=1-0{,}4=\res{0{,}6}$. \ De la fórmula de la unió: $0{,}9=0{,}7+0{,}6-P(A\cap B)$, \ $P(A\cap B)=\res{0{,}4}$. \ Com que $P(A\cap B)\neq0$, \rest{no són incompatibles}.",
       r"$P(A)=1-0{,}3=\res{0{,}7}$; \ $P(B)=1-0{,}4=\res{0{,}6}$. \ De la fórmula de la unión: $0{,}9=0{,}7+0{,}6-P(A\cap B)$, \ $P(A\cap B)=\res{0{,}4}$. \ Como $P(A\cap B)\neq0$, \rest{no son incompatibles}.")),
]))

S_.append((T("Càlcul de probabilitats", "Cálculo de probabilidades"), [
 O(3, 0), O(3, 1), O(4, 2), O(3, 3), O(3, 4), O(3, 7), O(4, 4), O(3, 8), O(3, 10)]))

S_.append((T("Experiències compostes. Probabilitat", "Experiencias compuestas. Probabilidad"), [
 O(4, 0), O(4, 1),
 (1, T(r"La probabilitat que plogue dissabte és 0,3 i la que plogue diumenge, 0,6 (suposem que són independents). Fes el diagrama d'arbre i calcula la probabilitat que: a) plogue els dos dies; b) no plogue cap dia; c) plogue almenys un dia; d) plogue exactament un dia.",
       r"La probabilidad de que llueva el sábado es 0,3 y la de que llueva el domingo, 0,6 (suponemos que son independientes). Haz el diagrama de árbol y calcula la probabilidad de que: a) llueva los dos días; b) no llueva ningún día; c) llueva al menos un día; d) llueva exactamente un día.") + RC_IND,
     cen(TPL) + T(r"a) $0{,}3\cdot0{,}6=\res{0{,}18}$. \ b) $0{,}7\cdot0{,}4=\res{0{,}28}$. \ c) $1-0{,}28=\res{0{,}72}$. \ d) $0{,}3\cdot0{,}4+0{,}7\cdot0{,}6=0{,}12+0{,}42=\res{0{,}54}$.",
                  r"a) $0{,}3\cdot0{,}6=\res{0{,}18}$. \ b) $0{,}7\cdot0{,}4=\res{0{,}28}$. \ c) $1-0{,}28=\res{0{,}72}$. \ d) $0{,}3\cdot0{,}4+0{,}7\cdot0{,}6=0{,}12+0{,}42=\res{0{,}54}$.")),
 O(4, 5), O(4, 6), O(4, 7),
 (2, T(r"Llancem un dau tres vegades. Quina és la probabilitat de no traure cap 6? I de traure'n almenys un?", r"Lanzamos un dado tres veces. ¿Cuál es la probabilidad de no sacar ningún 6? ¿Y de sacar al menos uno?"),
     T(r"$P(\text{cap 6})=\frac56\cdot\frac56\cdot\frac56=\res{\frac{125}{216}}$. \ $P(\text{almenys un 6})=1-\frac{125}{216}=\res{\frac{91}{216}}\approx0{,}42$. \ (No és $\frac16+\frac16+\frac16$: aquesta suma compta més d'una vegada els casos amb dos o tres sisos.)",
       r"$P(\text{ningún 6})=\frac56\cdot\frac56\cdot\frac56=\res{\frac{125}{216}}$. \ $P(\text{al menos un 6})=1-\frac{125}{216}=\res{\frac{91}{216}}\approx0{,}42$. \ (No es $\frac16+\frac16+\frac16$: esa suma cuenta más de una vez los casos con dos o tres seises.)")),
 O(4, 13),
 (3, T(r"Quantes vegades hem de llançar un dau, com a mínim, perquè la probabilitat de traure almenys un 6 siga més gran que $\frac12$?",
       r"¿Cuántas veces tenemos que lanzar un dado, como mínimo, para que la probabilidad de sacar al menos un 6 sea mayor que $\frac12$?"),
     T(r"Amb $n$ llançaments, $P(\text{almenys un 6})=1-\left(\frac56\right)^n$. \ $n=3$: $1-\frac{125}{216}\approx0{,}42$; \ $n=4$: $1-\frac{625}{1296}=\frac{671}{1296}\approx0{,}52$. \ Cal llançar-lo \res{4\text{ vegades}}.",
       r"Con $n$ lanzamientos, $P(\text{al menos un 6})=1-\left(\frac56\right)^n$. \ $n=3$: $1-\frac{125}{216}\approx0{,}42$; \ $n=4$: $1-\frac{625}{1296}=\frac{671}{1296}\approx0{,}52$. \ Hay que lanzarlo \res{4\text{ veces}}.")),
]))

S_.append((T("Experiències dependents. Probabilitat condicionada", "Experiencias dependientes. Probabilidad condicionada"), [
 (1, T(r"En una bossa hi ha 5 boles roges i 3 de verdes. Traiem una bola, és roja i no la tornem a la bossa. Quina és la probabilitat que la segona bola siga roja? I que siga verda? Escriu-les amb la notació de la probabilitat condicionada.",
       r"En una bolsa hay 5 bolas rojas y 3 verdes. Sacamos una bola, es roja y no la devolvemos a la bolsa. ¿Cuál es la probabilidad de que la segunda bola sea roja? ¿Y de que sea verde? Escríbelas con la notación de la probabilidad condicionada.") + RC_COND,
     T(r"Queden 7 boles: 4 roges i 3 verdes. \ $P(R_2/R_1)=\res{\frac47}$; \ $P(V_2/R_1)=\res{\frac37}$.", r"Quedan 7 bolas: 4 rojas y 3 verdes. \ $P(R_2/R_1)=\res{\frac47}$; \ $P(V_2/R_1)=\res{\frac37}$.")),
 (1, T(r"Traiem dues cartes d'una baralla espanyola de 40 cartes, sense reemplaçament. a) Si la primera és un oro, quina és la probabilitat que la segona també ho siga? b) Quina és la probabilitat de traure dos oros?",
       r"Sacamos dos cartas de una baraja española de 40 cartas, sin reemplazamiento. a) Si la primera es un oro, ¿cuál es la probabilidad de que la segunda también lo sea? b) ¿Cuál es la probabilidad de sacar dos oros?"),
     T(r"a) Queden 9 oros entre 39 cartes: $P(O_2/O_1)=\frac9{39}=\res{\frac3{13}}$. \ b) $P(O_1\cap O_2)=\frac{10}{40}\cdot\frac9{39}=\frac{90}{1560}=\res{\frac3{52}}$.",
       r"a) Quedan 9 oros entre 39 cartas: $P(O_2/O_1)=\frac9{39}=\res{\frac3{13}}$. \ b) $P(O_1\cap O_2)=\frac{10}{40}\cdot\frac9{39}=\frac{90}{1560}=\res{\frac3{52}}$.")),
 (2, T(r"En una bossa hi ha 3 boles blanques (B) i 2 de negres (N). En traiem dues \textbf{sense reemplaçament}. Fes el diagrama d'arbre i calcula la probabilitat que: a) les dues siguen blanques; b) les dues siguen negres; c) n'isca una de cada color. Compara-ho amb l'exercici de les mateixes boles amb reemplaçament.",
       r"En una bolsa hay 3 bolas blancas (B) y 2 negras (N). Sacamos dos \textbf{sin reemplazamiento}. Haz el diagrama de árbol y calcula la probabilidad de que: a) las dos sean blancas; b) las dos sean negras; c) salga una de cada color. Compáralo con el ejercicio de las mismas bolas con reemplazamiento."),
     O(4, 8)[2]),
 (2, T(r"En un grup, el 60 \% de l'alumnat aprova Matemàtiques. Dels que aproven Matemàtiques, el 75 \% aprova Física, i dels que no aproven Matemàtiques, només el 25 \%. Fes el diagrama d'arbre i calcula la probabilitat que un alumne triat a l'atzar: a) aprove les dues assignatures; b) aprove Física; c) no n'aprove cap.",
       r"En un grupo, el 60 \% del alumnado aprueba Matemáticas. De los que aprueban Matemáticas, el 75 \% aprueba Física, y de los que no aprueban Matemáticas, solo el 25 \%. Haz el diagrama de árbol y calcula la probabilidad de que un alumno elegido al azar: a) apruebe las dos asignaturas; b) apruebe Física; c) no apruebe ninguna."),
     cen(TMFm) + T(r"$P(F/M)=0{,}75$ i $P(F/\overline{M})=0{,}25$ són probabilitats condicionades. \ a) $0{,}6\cdot0{,}75=\res{0{,}45}$. \ b) $0{,}45+0{,}4\cdot0{,}25=0{,}45+0{,}1=\res{0{,}55}$. \ c) $0{,}4\cdot0{,}75=\res{0{,}3}$.",
                   r"$P(F/M)=0{,}75$ y $P(F/\overline{M})=0{,}25$ son probabilidades condicionadas. \ a) $0{,}6\cdot0{,}75=\res{0{,}45}$. \ b) $0{,}45+0{,}4\cdot0{,}25=0{,}45+0{,}1=\res{0{,}55}$. \ c) $0{,}4\cdot0{,}75=\res{0{,}3}$.")),
 O(4, 10), O(4, 11),
 (3, T(r"En una caixa hi ha 5 bombetes i 2 són defectuoses. En provem dues a l'atzar, sense reemplaçament. Quina és la probabilitat que almenys una siga defectuosa?",
       r"En una caja hay 5 bombillas y 2 son defectuosas. Probamos dos al azar, sin reemplazamiento. ¿Cuál es la probabilidad de que al menos una sea defectuosa?"),
     T(r"Contrari: cap defectuosa, $P=\frac35\cdot\frac24=\frac3{10}$. \ $P(\text{almenys una})=1-\frac3{10}=\res{\frac7{10}}$.", r"Contrario: ninguna defectuosa, $P=\frac35\cdot\frac24=\frac3{10}$. \ $P(\text{al menos una})=1-\frac3{10}=\res{\frac7{10}}$.")),
]))

S_.append((T("Taules de contingència", "Tablas de contingencia"), [
 O(4, 3), O(4, 9),
 (2, T(r"En una empresa de 400 treballadors, el 60 \% s'ha vacunat de la grip. Dels vacunats, el 5 \% ha tingut la grip, i dels no vacunats, el 30 \%. Completa la taula i calcula: a) la probabilitat que un treballador triat a l'atzar haja tingut la grip; b) $P(\text{grip}/\text{vacunat})$ i $P(\text{grip}/\text{no vacunat})$; c) si un treballador ha tingut la grip, la probabilitat que estiga vacunat.",
       r"En una empresa de 400 trabajadores, el 60 \% se ha vacunado de la gripe. De los vacunados, el 5 \% ha tenido la gripe, y de los no vacunados, el 30 \%. Completa la tabla y calcula: a) la probabilidad de que un trabajador elegido al azar haya tenido la gripe; b) $P(\text{gripe}/\text{vacunado})$ y $P(\text{gripe}/\text{no vacunado})$; c) si un trabajador ha tenido la gripe, la probabilidad de que esté vacunado.")
     + cen(cont([VAC, NVAC], [GR, NGR], VCm, blank={(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)})) + RC_TAB,
     cen(cont([VAC, NVAC], [GR, NGR], VCm)) + T(r"Vacunats: $60\,\%$ de $400=240$, i amb grip, el $5\,\%$ de $240=12$. No vacunats: 160, i amb grip, el $30\,\%$ de $160=48$. \ a) $\frac{60}{400}=\res{0{,}15}$. \ b) $\frac{12}{240}=\res{0{,}05}$ i $\frac{48}{160}=\res{0{,}3}$. \ c) Només les 60 persones amb grip: $\frac{12}{60}=\res{\frac15}$.",
                                                 r"Vacunados: $60\,\%$ de $400=240$, y con gripe, el $5\,\%$ de $240=12$. No vacunados: 160, y con gripe, el $30\,\%$ de $160=48$. \ a) $\frac{60}{400}=\res{0{,}15}$. \ b) $\frac{12}{240}=\res{0{,}05}$ y $\frac{48}{160}=\res{0{,}3}$. \ c) Solo las 60 personas con gripe: $\frac{12}{60}=\res{\frac15}$.")),
 O(4, 12),
 (3, T(r"En una classe de 50 alumnes, 30 són de 3r i 20 de 4t. Van a l'institut a peu 12 alumnes de 3r i 8 de 4t. Fes la taula de contingència i compara $P(\text{a peu})$ amb $P(\text{a peu}/\text{3r})$. Són independents els esdeveniments «anar a peu» i «ser de 3r»?",
       r"En una clase de 50 alumnos, 30 son de 3.\textsuperscript{o} y 20 de 4.\textsuperscript{o}. Van al instituto a pie 12 alumnos de 3.\textsuperscript{o} y 8 de 4.\textsuperscript{o}. Haz la tabla de contingencia y compara $P(\text{a pie})$ con $P(\text{a pie}/\text{3.\textsuperscript{o}})$. ¿Son independientes los sucesos «ir a pie» y «ser de 3.\textsuperscript{o}»?"),
     cen(cont([T('3r', r'3.\textsuperscript{o}'), T('4t', r'4.\textsuperscript{o}')], [T('A peu', 'A pie'), T('No a peu', 'No a pie')], IPm))
     + T(r"$P(\text{a peu})=\frac{20}{50}=\res{\frac25}$ \ i \ $P(\text{a peu}/\text{3r})=\frac{12}{30}=\res{\frac25}$. \ Saber que és de 3r no canvia la probabilitat: \rest{sí, són independents}.",
         r"$P(\text{a pie})=\frac{20}{50}=\res{\frac25}$ \ y \ $P(\text{a pie}/\text{3.\textsuperscript{o}})=\frac{12}{30}=\res{\frac25}$. \ Saber que es de 3.\textsuperscript{o} no cambia la probabilidad: \rest{sí, son independientes}.")),
 (3, T(r"El 70 \% dels clients d'una botiga paga amb targeta. Dels que paguen amb targeta, el 20 \% fa una compra de més de 50 €, i dels que paguen en efectiu, el 10 \%. Fes la taula de contingència per a 1000 clients. Si un client ha fet una compra de més de 50 €, quina és la probabilitat que haja pagat amb targeta?",
       r"El 70 \% de los clientes de una tienda paga con tarjeta. De los que pagan con tarjeta, el 20 \% hace una compra de más de 50 €, y de los que pagan en efectivo, el 10 \%. Haz la tabla de contingencia para 1000 clientes. Si un cliente ha hecho una compra de más de 50 €, ¿cuál es la probabilidad de que haya pagado con tarjeta?"),
     cen(cont([T('Targeta', 'Tarjeta'), T('Efectiu', 'Efectivo')], [T('Més de 50 €', 'Más de 50 €'), T('50 € o menys', '50 € o menos')], TGm, hl={(0, 0), (1, 0)}))
     + T(r"Targeta: 700, i 140 compren més de 50 €; efectiu: 300, i 30. En total, 170 clients han comprat més de 50 €. \ $P(\text{targeta}/{>}50\text{ €})=\frac{140}{170}=\res{\frac{14}{17}}\approx0{,}82$.",
         r"Tarjeta: 700, y 140 compran más de 50 €; efectivo: 300, y 30. En total, 170 clientes han comprado más de 50 €. \ $P(\text{tarjeta}/{>}50\text{ €})=\frac{140}{170}=\res{\frac{14}{17}}\approx0{,}82$.")),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("probabilitat, experiment aleatori, espai mostral, esdeveniments, unió, intersecció, esdeveniment contrari, freqüència relativa, llei de Laplace, experiències compostes, experiències independents, experiències dependents, probabilitat condicionada, diagrama d'arbre, taula de contingència",
       'probabilidad, experimento aleatorio, espacio muestral, sucesos, unión, intersección, suceso contrario, frecuencia relativa, ley de Laplace, experiencias compuestas, experiencias independientes, experiencias dependientes, probabilidad condicionada, diagrama de árbol, tabla de contingencia')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques A 4t ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\usepackage{pifont}
\usetikzlibrary{trees}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T("Probabilitat", 'Probabilidad')
NU = 11

def build(sol_):
    if ES:
        sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad %d: %s' % (t, NU, TIT), capcalera='%s · Unidad %d: %s' % (t, NU, TIT), pdfkeywords=KW, curs='4eso-a')
        cap = assignatura('4eso-a') + '{' + ('Soluciones de la ficha · Unidad %d' % NU if sol_ else 'Ficha de ejercicios · Unidad %d' % NU) + '}{' + TIT + '}'
    else:
        t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat %d: %s. 4t d'ESO Matemàtiques A}" % (t, NU, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat %d: %s · 4t ESO A" % (t, NU, TIT))
        assert "4t d'ESO Matemàtiques A" in p and 'Unitat %d' % NU in p and 'unitat %d' % NU in p
        cap = r'\capcalera{Matemàtiques A}{4t ESO}{' + ('Solucions de la fitxa · Unitat %d' % NU if sol_ else "Fitxa d'exercicis · Unitat %d" % NU) + '}{' + TIT + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol_ else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{14}\n\\input{../comu/fentmates.tex}\n\\fmcurs{4eso-a}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol_:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs simulacions, una bossa de boles, la taula dels dos daus, diagrames d'arbre d'experiències independents i dependents, dues urnes i una taula de contingència que calculen les probabilitats pas a pas. Les probabilitats es donen en fracció irreductible (o en decimal, si les dades ho són).",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás simulaciones, una bolsa de bolas, la tabla de los dos dados, diagramas de árbol de experiencias independientes y dependientes, dos urnas y una tabla de contingencia que calculan las probabilidades paso a paso. Las probabilidades se dan en fracción irreducible (o en decimal, si los datos lo son).") if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos: escriu l'espai mostral, fes un diagrama d'arbre o una taula quan calga i dona les probabilitats en forma de fracció irreductible (o en decimal, si les dades ho són). Les seccions segueixen l'ordre dels apunts de la unitat (11.1--11.7).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos: escribe el espacio muestral, haz un diagrama de árbol o una tabla cuando haga falta y da las probabilidades en forma de fracción irreducible (o en decimal, si los datos lo son). Las secciones siguen el orden de los apuntes de la unidad (11.1--11.7)."))
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

for _, exs in S_:
    for st, q, s in exs:
        assert st in (1, 2, 3) and q and s
        assert '2º' not in q + s and '1º' not in q + s, 'º a la fitxa: usa \\textsuperscript{o}'
build(False); build(True)
print(sum(len(x[1]) for x in S_), T('exercicis', 'ejercicios'))
