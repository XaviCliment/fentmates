# Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex (4t ESO Matemàtiques B, Unitat 9: Tècniques de recompte. Probabilitat)
# a partir d'una sola llista d'exercicis (estrelles, enunciat, solució). Les eines comunes són a ../comu/eso4b.py.
# Recull TOTS els exercicis del departament: els 15 dels apunts «Probabilitat. 4t ESO · Matemàtiques B» (marcats (D) en aquest
# codi) i els 21 de la col·lecció «Ejercicios probabilidad» (marcats (DE)), i hi afig exercicis nous, sobretot de les tècniques
# de recompte (seccions 1-3), que els apunts del departament no tenen, i de probabilitat amb recompte.
# Les 10 seccions segueixen els apartats dels apunts (9.1-9.10).
# Errades de la col·lecció corregides: (DE7) B = «no traure 6» no conté el 6; (DE20 b) P(pel·lícula | no debat) = 650/1000 = 0,65
# (la solució de la col·lecció, 0,97, és P(pel·lícula | debat)).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es). Cada probabilitat es calcula amb fraccions exactes (Fraction) i es comprova amb ck().
# Ús: python3 genera.py && pdflatex t9-fitxa-exercicis.tex (dues vegades) && pdflatex t9-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re, sys, math
from fractions import Fraction as Fr
from itertools import product, permutations
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from eso4b import *

def items(*xs): return r'\begin{enumerate}[label=\alph*),leftmargin=*,itemsep=2pt,topsep=2pt]' + ''.join(r'\item ' + t for t in xs) + r'\end{enumerate}'
def fixm(t):
    """dins de les fórmules (i fora dels dibuixos), espai fi després de les comes de conjunts i parelles: {2,4} -> {2,\\,4}"""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    def m(mm): return re.sub(r'(?<!\\),(?=[-\d+a-zA-Z(\[]|\\(?![,; ]))', r',\\,', mm.group(0))
    for i in range(0, len(parts), 2): parts[i] = re.sub(r'\$[^$]*\$', m, parts[i])
    return ''.join(parts)
def E(st, q, s): return (st, fixm(q), fixm(s))

ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return (es if ES else va).replace("\\'", "'")   # r'...d\'...' deixa la barra: la llevem
I_ = T('i', 'y')
C = math.comb
def V(n, k): return math.perm(n, k)

# ---------- fraccions ----------
def fr(f):
    f = Fr(f)
    if f.denominator == 1: return str(f.numerator)
    return ('-' if f < 0 else '') + r'\frac{%d}{%d}' % (abs(f.numerator), f.denominator)
def fs(n, d):
    """n/d i, si es pot, simplificada"""
    f = Fr(n, d); s = r'\frac{%d}{%d}' % (n, d)
    return s if (f.numerator, f.denominator) == (n, d) else s + '=' + fr(f)
def dc(x, k=4):
    """decimal amb coma per a dins de les fórmules: 0{,}25"""
    s = ('%.*f' % (k, float(x))).rstrip('0').rstrip('.')
    return s.replace('.', '{,}')
def ap(x, k=3): return r'\approx' + dc(round(float(x), k), k)
def st(xs): return r'\{' + ','.join(str(x) for x in xs) + r'\}' if xs else r'\varnothing'
def lap(E, f): return Fr(sum(1 for e in E if f(e)), len(E))
def big(n): return '{:,}'.format(n).replace(',', r'\,')
D6 = range(1, 7)
DD = list(product(D6, D6))
def isprime(n): return n > 1 and all(n % k for k in range(2, int(n ** .5) + 1))

# ---------- figures (TikZ) ----------
BC = {'R': 'red!75!black', 'B': 'blue!70!black', 'V': 'teal', 'N': 'black!80', 'W': 'white'}
def tree(kids, ld=17, sd=(16, 8, 4.5), font=r'\small'):
    """diagrama d'arbre cap a la dreta. kids = [(etiqueta, prob, fills, text final)]"""
    def node(lab, end):
        sty = ''
        if end: sty = 'label={[font=\\footnotesize,xshift=1mm]right:%s}' % end.replace(r'\frac', r'\dfrac')
        return 'node[%s] {%s}' % (sty, lab)
    def ch(ks):
        o = ''
        for i, k in enumerate(ks):
            pos = 'above' if i < len(ks) / 2 else 'below'
            if len(ks) % 2 == 1 and i == len(ks) // 2: pos = 'above'
            o += ' child {%s%s edge from parent node[%s,pos=.55,font=\\footnotesize,text=teal!70!black,inner sep=1.5pt] {%s}}' % (
                node(k[0], k[3] if len(k) > 3 else ''), ch(k[2]), pos, '$%s$' % k[1].replace(r'\frac', r'\dfrac') if k[1] else '')
        return o
    lv = ','.join('level %d/.style={sibling distance=%smm}' % (i + 1, s) for i, s in enumerate(sd))
    return (r"\begin{tikzpicture}[grow'=right,level distance=%smm," r'%s,every node/.style={font=%s\bfseries},edge from parent/.style={draw=muted,thick}]' % (ld, lv, font)
            + '\n\\node[circle,fill=navy,inner sep=1.2pt] {}' + ch(kids) + ';\n\\end{tikzpicture}')
def dtab(op, hit, sym='+'):
    """taula de doble entrada de dos daus amb les caselles favorables acolorides"""
    o = [r'{\small\renewcommand{\arraystretch}{1.15}\setlength{\tabcolsep}{4pt}\begin{tabular}{c|cccccc}', r'\rowcolor{soft} $%s$ & 1 & 2 & 3 & 4 & 5 & 6\\\hline' % sym]
    for a in D6:
        o.append(r'\cellcolor{soft}%d & ' % a + ' & '.join((r'\cellcolor{accent!30}\textbf{%d}' if hit(a, b) else '%d') % op(a, b) for b in D6) + r'\\')
    o.append(r'\end{tabular}}')
    return '\n'.join(o)
def ctab(head, rows, grid=False):
    if grid:   # taula per completar: totes les vores i cel·les amples
        return (r'{\small\renewcommand{\arraystretch}{1.35}\begin{tabular}{|l|' + 'C{1.9cm}|' * (len(head) - 1) + r'}\hline' + '\n\\rowcolor{soft} ' + ' & '.join(head) + r'\\\hline' + '\n'
                + '\n'.join(' & '.join(str(c) for c in r) + r'\\\hline' for r in rows) + '\n\\end{tabular}}')
    return (r'{\small\renewcommand{\arraystretch}{1.2}\begin{tabular}{l|' + 'c' * (len(head) - 1) + r'}' + '\n\\rowcolor{soft} ' + ' & '.join(head) + r'\\\hline' + '\n'
            + '\n'.join(' & '.join(str(c) for c in r) + r'\\' for r in rows) + '\n\\end{tabular}}')
def cen(*xs, sep=r'\qquad '): return r'\par\smallskip\begin{center}' + sep.join(xs) + r'\end{center}'
def two_stage(first, second, ld=22, sd=(26, 12), fmt=fr):
    """arbre de dues etapes: first = [(nom, p)], second = {nom: [(nom2, p2)]}; mostra el producte de cada camí (fmt: fr o dc)"""
    kids = []
    for a, pa in first:
        # pb pot ser una parella (n, d) per a escriure la fracció sense simplificar (6/9 en compte de 2/3)
        ch = [(b, r'\frac{%d}{%d}' % pb if isinstance(pb, tuple) else fmt(pb), [], r'$%s$' % fmt(Fr(pa) * (Fr(*pb) if isinstance(pb, tuple) else Fr(pb)))) for b, pb in second[a]]
        kids.append((a, fmt(pa), ch))
    return tree(kids, ld=ld, sd=sd)

S = []
def sec(title): S.append((title, [])); return S[-1][1]

# =====================================================================
# 1. Diagrames d'arbre i principi de multiplicació
X = sec(T("Diagrames d'arbre i principi de multiplicació", 'Diagramas de árbol y principio de multiplicación'))
EN = [T('Pernil', 'Jamón'), T('Formatge', 'Queso'), T('Vegetal', 'Vegetal')]
BE = [T('Aigua', 'Agua'), T('Suc', 'Zumo')]
TR = tree([(e, '', [(b, '', [], '') for b in BE]) for e in EN], ld=24, sd=(13, 6.5))
X.append(E(1, T("En una cafeteria, l'esmorzar consisteix en un entrepà (de pernil, de formatge o vegetal) i una beguda (aigua o suc). Fes un diagrama d'arbre i escriu tots els esmorzars possibles. Quants n'hi ha?",
                "En una cafetería, el almuerzo consiste en un bocadillo (de jamón, de queso o vegetal) y una bebida (agua o zumo). Haz un diagrama de árbol y escribe todos los almuerzos posibles. ¿Cuántos hay?"),
    cen(TR) + T('Hi ha ', 'Hay ') + r'$3\cdot2=\res{6}$ ' + T('esmorzars: ', 'almuerzos: ') + ', '.join('%s--%s' % (e, b) for e in EN for b in BE) + '.'))
ck(4 * 3 * 2, 24)
X.append(E(1, T("La Clara té 4 samarretes, 3 pantalons i 2 parells de sabatilles. De quantes maneres diferents es pot vestir (amb una peça de cada tipus)?",
                "Clara tiene 4 camisetas, 3 pantalones y 2 pares de zapatillas. ¿De cuántas maneras distintas se puede vestir (con una prenda de cada tipo)?"),
    r'$4\cdot3\cdot2=\res{24}$ ' + T('maneres.', 'maneras.')))
ck(10 ** 8, 100000000)
X.append(E(1, T("Quants números de telèfon de 9 xifres que comencen per 6 hi pot haver?", "¿Cuántos números de teléfono de 9 cifras que empiezan por 6 puede haber?"),
    T("La primera xifra és fixa i cadascuna de les altres 8 es pot triar de 10 maneres: ", "La primera cifra es fija y cada una de las otras 8 se puede elegir de 10 maneras: ") + r'$10^8=\res{100\,000\,000}$.'))
ck(len([n for n in range(100, 1000) if set(str(n)) <= set('01234')]), 100)
ck(len([n for n in range(100, 1000) if set(str(n)) <= set('01234') and len(set(str(n))) == 3]), 48)
ck(len([n for n in range(100, 1000) if set(str(n)) <= set('01234') and len(set(str(n))) == 3 and n % 10 == 0]), 12)
X.append(E(2, T("Amb les xifres 0, 1, 2, 3 i 4, quants nombres de tres xifres es poden formar", "Con las cifras 0, 1, 2, 3 y 4, ¿cuántos números de tres cifras se pueden formar") + items(
    T('si es poden repetir les xifres?', 'si se pueden repetir las cifras?'), T('si no es poden repetir?', 'si no se pueden repetir?'), T('sense repetir xifres i acabats en 0?', 'sin repetir cifras y acabados en 0?'))
    + recorda(T("un nombre de tres xifres no pot començar per 0.", "un número de tres cifras no puede empezar por 0.")),
    items(T(r'Centenes: 4 opcions (no el 0); desenes i unitats: 5. $4\cdot5\cdot5=\res{100}$', r'Centenas: 4 opciones (no el 0); decenas y unidades: 5. $4\cdot5\cdot5=\res{100}$'),
          T(r'Centenes: 4; desenes: 4 (ara sí que pot ser 0); unitats: 3. $4\cdot4\cdot3=\res{48}$', r'Centenas: 4; decenas: 4 (ahora sí puede ser 0); unidades: 3. $4\cdot4\cdot3=\res{48}$'),
          T(r'Unitats: el 0 (1 opció); centenes: 4; desenes: 3. $1\cdot4\cdot3=\res{12}$', r'Unidades: el 0 (1 opción); centenas: 4; decenas: 3. $1\cdot4\cdot3=\res{12}$'))))
for a, b in [(math.factorial(7), 5040), (Fr(math.factorial(8), math.factorial(6)), 56), (Fr(math.factorial(12), math.factorial(10)), 132), (Fr(math.factorial(5), math.factorial(3) * 2), 10)]: ck(a, b)
X.append(E(1, T('Calcula:', 'Calcula:') + tasks(5, [r'$7!$', r'$\dfrac{8!}{6!}$', r'$\dfrac{12!}{10!}$', r'$\dfrac{5!}{3!\cdot2!}$', r'$0!$']),
    tasks(5, [r'$\res{5\,040}$', r'$8\cdot7=\res{56}$', r'$12\cdot11=\res{132}$', r'$\dfrac{5\cdot4}{2}=\res{10}$', r'$\res{1}$'])))
X.append(E(2, T('Simplifica:', 'Simplifica:') + tasks(3, [r'$\dfrac{n!}{(n-1)!}$', r'$\dfrac{(n+1)!}{n!}$', r'$\dfrac{(n+2)!}{n!}$']),
    tasks(3, [r'$\res{n}$', r'$\res{n+1}$', r'$\res{(n+2)(n+1)}$'])))
ck(6 * 2 * 2, 24); ck(6 ** 3, 216)
X.append(E(2, T("Quants resultats té l'experiment de llançar un dau i dues monedes? I el de llançar tres daus?", "¿Cuántos resultados tiene el experimento de lanzar un dado y dos monedas? ¿Y el de lanzar tres dados?"),
    r'$6\cdot2\cdot2=\res{24}$; \ $6^3=\res{216}$'))

# =====================================================================
# 2. Variacions i permutacions
X = sec(T('Variacions i permutacions', 'Variaciones y permutaciones'))
for a, b in [(V(7, 3), 210), (4 ** 3, 64), (math.factorial(6), 720), (V(10, 2), 90)]: ck(a, b)
X.append(E(1, T('Calcula:', 'Calcula:') + tasks(4, [r'$V_{7,3}$', r'$VR_{4,3}$', r'$P_6$', r'$V_{10,2}$']),
    tasks(4, [r'$7\cdot6\cdot5=\res{210}$', r'$4^3=\res{64}$', r'$6!=\res{720}$', r'$10\cdot9=\res{90}$'])))
ck(V(5, 3), 60); ck(5 ** 3, 125)
X.append(E(1, T("Quantes «paraules» de 3 lletres diferents es poden formar amb les vocals A, E, I, O, U? I si es poden repetir les lletres?", "¿Cuántas «palabras» de 3 letras distintas se pueden formar con las vocales A, E, I, O, U? ¿Y si se pueden repetir las letras?"),
    r'$V_{5,3}=5\cdot4\cdot3=\res{60}$; \ $VR_{5,3}=5^3=\res{125}$'))
ck(V(12, 3), 1320)
X.append(E(1, T("En un concurs participen 12 persones i hi ha tres premis diferents (primer, segon i tercer). De quantes maneres es poden repartir?", "En un concurso participan 12 personas y hay tres premios distintos (primero, segundo y tercero). ¿De cuántas maneras se pueden repartir?"),
    T("Importa l'ordre i ningú no pot guanyar dos premis: ", "Importa el orden y nadie puede ganar dos premios: ") + r'$V_{12,3}=12\cdot11\cdot10=\res{1\,320}$.'))
ck(len([p for p in permutations(range(6)) if {p[0], p[5]} == {0, 1}]), 48)
X.append(E(2, T("De quantes maneres es poden asseure 6 amics en 6 cadires en fila? I si dos d'ells, l'Àlex i la Berta, han de seure als extrems?", "¿De cuántas maneras se pueden sentar 6 amigos en 6 sillas en fila? ¿Y si dos de ellos, Álex y Berta, tienen que sentarse en los extremos?"),
    r'$P_6=6!=\res{720}$. \ ' + T("Als extrems, l'Àlex i la Berta (2 ordres) i els altres 4, al mig: ", "En los extremos, Álex y Berta (2 órdenes) y los otros 4, en medio: ") + r'$2\cdot4!=\res{48}$.'))
L6 = 'ABCDEF'
ck(len(list(permutations(L6))), 720); ck(len([p for p in permutations(L6) if p[0] == 'A']), 120); ck(len([p for p in permutations(L6) if p[0] in 'AE' and p[-1] in 'AE']), 48)
X.append(E(2, T("Ordenem les lletres A, B, C, D, E i F.", "Ordenamos las letras A, B, C, D, E y F.") + items(
    T('Quantes ordenacions diferents hi ha?', '¿Cuántas ordenaciones distintas hay?'), T('Quantes comencen per A?', '¿Cuántas empiezan por A?'), T('Quantes comencen i acaben per vocal?', '¿Cuántas empiezan y acaban por vocal?')),
    items(r'$P_6=6!=\res{720}$', T(r'La A fixa al principi i les altres 5 en qualsevol ordre: $5!=\res{120}$', r'La A fija al principio y las otras 5 en cualquier orden: $5!=\res{120}$'),
          T(r'Les vocals són A i E: als extrems, en 2 ordres; les altres 4, al mig: $2\cdot4!=\res{48}$', r'Las vocales son A y E: en los extremos, en 2 órdenes; las otras 4, en medio: $2\cdot4!=\res{48}$'))))
N7 = [p for p in permutations('1234567', 4)]
ck(len(N7), 840); ck(len([p for p in N7 if int(p[3]) % 2 == 0]), 360); ck(len([p for p in N7 if int(''.join(p)) > 5000]), 360)
X.append(E(2, T("Amb les xifres 1, 2, 3, 4, 5, 6 i 7, sense repetir-ne cap:", "Con las cifras 1, 2, 3, 4, 5, 6 y 7, sin repetir ninguna:") + items(
    T('Quants nombres de 4 xifres es poden formar?', '¿Cuántos números de 4 cifras se pueden formar?'), T('Quants són parells?', '¿Cuántos son pares?'), T('Quants són més grans que 5 000?', '¿Cuántos son mayores que 5 000?')),
    items(r'$V_{7,4}=7\cdot6\cdot5\cdot4=\res{840}$',
          T(r'Les unitats han de ser 2, 4 o 6 (3 opcions) i les altres tres xifres, de les 6 que queden: $3\cdot V_{6,3}=3\cdot120=\res{360}$', r'Las unidades tienen que ser 2, 4 o 6 (3 opciones) y las otras tres cifras, de las 6 que quedan: $3\cdot V_{6,3}=3\cdot120=\res{360}$'),
          T(r'La primera xifra ha de ser 5, 6 o 7: $3\cdot V_{6,3}=\res{360}$', r'La primera cifra tiene que ser 5, 6 o 7: $3\cdot V_{6,3}=\res{360}$'))))
ck(10 ** 4, 10000); ck(V(10, 4), 5040)
X.append(E(1, T("Un cadenat té una combinació de 4 xifres (de 0 a 9). Quantes combinacions hi ha? En quantes són totes les xifres diferents?", "Un candado tiene una combinación de 4 cifras (de 0 a 9). ¿Cuántas combinaciones hay? ¿En cuántas son todas las cifras distintas?"),
    r'$VR_{10,4}=10^4=\res{10\,000}$; \ $V_{10,4}=10\cdot9\cdot8\cdot7=\res{5\,040}$'))
ck(26 ** 2 * 10 ** 3, 676000); ck(26 * 25 * 10 * 9 * 8, 468000)
X.append(E(3, T("Una contrasenya està formada per 2 lletres (de 26) seguides de 3 xifres. Quantes contrasenyes diferents hi ha? I quantes, si no es pot repetir cap lletra ni cap xifra?", "Una contraseña está formada por 2 letras (de 26) seguidas de 3 cifras. ¿Cuántas contraseñas distintas hay? ¿Y cuántas, si no se puede repetir ninguna letra ni ninguna cifra?"),
    r'$26^2\cdot10^3=\res{676\,000}$; \ $V_{26,2}\cdot V_{10,3}=26\cdot25\cdot10\cdot9\cdot8=\res{468\,000}$'))

# =====================================================================
# 3. Combinacions
X = sec(T('Combinacions', 'Combinaciones'))
for a, b in [(C(8, 3), 56), (C(12, 10), 66), (C(6, 6), 1), (C(15, 2), 105)]: ck(a, b)
X.append(E(1, T('Calcula:', 'Calcula:') + tasks(4, [r'$\dbinom83$', r'$\dbinom{12}{10}$', r'$\dbinom66$', r'$\dbinom{15}{2}$']),
    tasks(4, [r'$\dfrac{8\cdot7\cdot6}{3!}=\res{56}$', r'$\dbinom{12}{2}=\res{66}$', r'$\res{1}$', r'$\dfrac{15\cdot14}{2}=\res{105}$'])))
ck(C(7, 2), C(7, 5)); ck(C(6, 2) + C(6, 3), C(7, 3))
X.append(E(2, T(r"Comprova que $\dbinom72=\dbinom75$ i que $\dbinom62+\dbinom63=\dbinom73$. Com es veuen aquestes igualtats al triangle de Tartaglia?", r"Comprueba que $\dbinom72=\dbinom75$ y que $\dbinom62+\dbinom63=\dbinom73$. ¿Cómo se ven estas igualdades en el triángulo de Tartaglia?"),
    r'$\dbinom72=\dbinom75=\res{21}$; \ $15+20=\res{35}=\dbinom73$. ' + T("Cada fila de Tartaglia és simètrica i cada nombre és la suma dels dos que té damunt.", "Cada fila de Tartaglia es simétrica y cada número es la suma de los dos que tiene encima.")))
ck(C(24, 2), 276)
X.append(E(1, T("En una classe de 24 alumnes, quantes parelles de treball diferents es poden formar?", "En una clase de 24 alumnos, ¿cuántas parejas de trabajo distintas se pueden formar?"),
    r'$\dbinom{24}{2}=\dfrac{24\cdot23}{2}=\res{276}$'))
ck(C(16, 4), 1820); ck(C(9, 2) * C(7, 2), 756); ck(C(9, 4), 126)
X.append(E(2, T("Un club té 9 xiques i 7 xics. Cal triar una comissió de 4 persones.", "Un club tiene 9 chicas y 7 chicos. Hay que elegir una comisión de 4 personas.") + items(
    T('Quantes comissions diferents es poden formar?', '¿Cuántas comisiones distintas se pueden formar?'), T('Quantes tenen 2 xiques i 2 xics?', '¿Cuántas tienen 2 chicas y 2 chicos?'), T('Quantes estan formades només per xiques?', '¿Cuántas están formadas solo por chicas?')),
    items(r'$\dbinom{16}{4}=\res{1\,820}$', r'$\dbinom92\cdot\dbinom72=36\cdot21=\res{756}$', r'$\dbinom94=\res{126}$')))
ck(C(8, 3), 56)
X.append(E(1, T("Una pizzeria ofereix 8 ingredients. Quantes pizzes diferents de 3 ingredients (diferents) es poden demanar?", "Una pizzería ofrece 8 ingredientes. ¿Cuántas pizzas distintas de 3 ingredientes (distintos) se pueden pedir?"),
    T("No importa l'ordre: ", "No importa el orden: ") + r'$\dbinom83=\res{56}$.'))
ck(C(10, 2) - 10, 35); ck(Fr(10 * 7, 2), 35)
X.append(E(2, T("Quantes diagonals té un decàgon? Troba una fórmula per al nombre de diagonals d'un polígon de $n$ costats.", "¿Cuántas diagonales tiene un decágono? Halla una fórmula para el número de diagonales de un polígono de $n$ lados."),
    r'$\dbinom{10}{2}-10=45-10=\res{35}$. \ ' + T("En general:", "En general:") + r' $\dbinom n2-n=\dfrac{n(n-1)}{2}-n=\res{\dfrac{n(n-3)}{2}}$.'))
ck(C(25, 2), 300); ck(V(25, 2), 600); ck(math.factorial(5), 120); ck(C(49, 6), 13983816)
X.append(E(2, T("Digues de quin tipus és cada recompte i calcula'l:", "Di de qué tipo es cada recuento y calcúlalo:") + items(
    T("Maneres de triar 2 representants (amb el mateix càrrec) en una classe de 25.", "Maneras de elegir 2 representantes (con el mismo cargo) en una clase de 25."),
    T("Maneres de triar delegat i subdelegat en la mateixa classe.", "Maneras de elegir delegado y subdelegado en la misma clase."),
    T("Codis de 3 xifres (de 0 a 9).", "Códigos de 3 cifras (de 0 a 9)."), T("Maneres d'ordenar 5 llibres en un prestatge.", "Maneras de ordenar 5 libros en una estantería."),
    T("Apostes de la Primitiva (6 nombres de 49).", "Apuestas de la Primitiva (6 números de 49).")),
    items(T(r'Combinacions: $\dbinom{25}{2}=\res{300}$', r'Combinaciones: $\dbinom{25}{2}=\res{300}$'), T(r'Variacions: $V_{25,2}=\res{600}$', r'Variaciones: $V_{25,2}=\res{600}$'),
          T(r'Variacions amb repetició: $10^3=\res{1\,000}$', r'Variaciones con repetición: $10^3=\res{1\,000}$'), T(r'Permutacions: $5!=\res{120}$', r'Permutaciones: $5!=\res{120}$'),
          T(r'Combinacions: $\dbinom{49}{6}=\res{13\,983\,816}$', r'Combinaciones: $\dbinom{49}{6}=\res{13\,983\,816}$'))))
ck(C(10, 3), 120); ck(C(9, 2), 36); ck(C(9, 3), 84)
X.append(E(3, T("En una bossa hi ha 10 boles numerades de l'1 al 10 i en traiem 3 alhora. Quants grups de 3 boles es poden obtindre? Quants contenen la bola 1? Quants no la contenen?", "En una bolsa hay 10 bolas numeradas del 1 al 10 y sacamos 3 a la vez. ¿Cuántos grupos de 3 bolas se pueden obtener? ¿Cuántos contienen la bola 1? ¿Cuántos no la contienen?"),
    r'$\dbinom{10}{3}=\res{120}$. \ ' + T("Amb la bola 1, falten 2 boles de les 9 restants:", "Con la bola 1, faltan 2 bolas de las 9 restantes:") + r' $\dbinom92=\res{36}$. \ ' + T('Sense la bola 1:', 'Sin la bola 1:') + r' $\dbinom93=\res{84}$ $(36+84=120)$.'))

# =====================================================================
# 4. Experiments aleatoris. Espai mostral i esdeveniments
X = sec(T('Experiments aleatoris. Espai mostral i esdeveniments', 'Experimentos aleatorios. Espacio muestral y sucesos'))
# (D1)
X.append(E(1, T('Indica si els experiments següents són deterministes o aleatoris:', 'Indica si los experimentos siguientes son deterministas o aleatorios:') + items(
    T("Mesurar la temperatura a la qual bull l'aigua a nivell de la mar.", "Medir la temperatura a la que hierve el agua a nivel del mar."), T("Traure una carta d'una baralla.", "Sacar una carta de una baraja."),
    T("Calcular l'àrea d'un quadrat de 3 cm de costat.", "Calcular el área de un cuadrado de 3 cm de lado."), T("Endevinar el resultat d'un partit de futbol.", "Adivinar el resultado de un partido de fútbol.")),
    tasks(4, [r'\rest{%s}' % T('Determinista', 'Determinista'), r'\rest{%s}' % T('Aleatori', 'Aleatorio'), r'\rest{%s}' % T('Determinista', 'Determinista'), r'\rest{%s}' % T('Aleatori', 'Aleatorio')])))
# (D2)
X.append(E(1, T("Escriu l'espai mostral dels experiments següents:", "Escribe el espacio muestral de los experimentos siguientes:") + items(
    T('Llançar un dau de sis cares.', 'Lanzar un dado de seis caras.'), T('Llançar dues monedes.', 'Lanzar dos monedas.'),
    T("Traure una bola d'una bossa que conté boles roges, blaves i verdes.", "Sacar una bola de una bolsa que contiene bolas rojas, azules y verdes."), T('Llançar una moneda i un dau.', 'Lanzar una moneda y un dado.')),
    items(r'$\res{E=\{1,2,3,4,5,6\}}$', r'$\res{E=\{CC,CX,XC,XX\}}$ ' + T('(C = cara, X = creu)', '(C = cara, X = cruz)'),
          r'$\res{E=\{%s\}}$' % T('R,B,V', 'R,A,V'), r'$\res{E=\{C1,C2,C3,C4,C5,C6,X1,X2,X3,X4,X5,X6\}}$ ' + T('(12 resultats)', '(12 resultados)'))))
E3 = [''.join(p) for p in product('CX', repeat=3)]
ck(len([e for e in E3 if e.count('C') >= 2]), 4)
X.append(E(1, T("Llancem tres monedes. Escriu l'espai mostral i els esdeveniments $A=$«almenys dues cares», $B=$«cap cara» i $C=$«més de tres cares». De quin tipus és cadascun?",
                "Lanzamos tres monedas. Escribe el espacio muestral y los sucesos $A=$«al menos dos caras», $B=$«ninguna cara» y $C=$«más de tres caras». ¿De qué tipo es cada uno?"),
    r'$E=\{' + '$, $'.join(E3) + r'\}$ ' + T('(8 resultats).', '(8 resultados).') + r'\\ $\res{A=\{CCC,CCX,CXC,XCC\}}$, ' + T('compost', 'compuesto') + r'; \ $\res{B=\{XXX\}}$, ' + T('elemental', 'elemental')
    + r'; \ $\res{C=\varnothing}$, ' + T('impossible.', 'imposible.')))
ck(len(set(a + b for a, b in DD)), 11)
X.append(E(2, T("Llancem dos daus. Escriu l'espai mostral si anotem la suma dels punts i si anotem la parella de resultats. Quants elements té cadascun? Són igual de probables els resultats en els dos casos?",
                "Lanzamos dos dados. Escribe el espacio muestral si anotamos la suma de los puntos y si anotamos la pareja de resultados. ¿Cuántos elementos tiene cada uno? ¿Son igual de probables los resultados en los dos casos?"),
    T(r"Sumes: $E=\{2,3,\dots,12\}$, amb \rest{11} elements, que \textbf{no} són equiprobables (el 7 ix més que el 2). Parelles: $E=\{(1,1),(1,2),\dots,(6,6)\}$, amb $6\cdot6=\res{36}$ elements equiprobables.",
      r"Sumas: $E=\{2,3,\dots,12\}$, con \rest{11} elementos, que \textbf{no} son equiprobables (el 7 sale más que el 2). Parejas: $E=\{(1,1),(1,2),\dots,(6,6)\}$, con $6\cdot6=\res{36}$ elementos equiprobables.")))
X.append(E(1, T("Escriu l'espai mostral de l'experiment «mirar el sexe dels fills d'una família de tres fills, per ordre de naixement» i l'esdeveniment «el major és xic».",
                "Escribe el espacio muestral del experimento «mirar el sexo de los hijos de una familia de tres hijos, por orden de nacimiento» y el suceso «el mayor es chico»."),
    T(r"Amb H = xic i D = xica: $E=\{HHH,HHD,HDH,HDD,DHH,DHD,DDH,DDD\}$; «el major és xic» $=\res{\{HHH,HHD,HDH,HDD\}}$.",
      r"Con H = chico y M = chica: $E=\{HHH,HHM,HMH,HMM,MHH,MHM,MMH,MMM\}$; «el mayor es chico» $=\res{\{HHH,HHM,HMH,HMM\}}$.")))

# =====================================================================
# 5. Operacions amb esdeveniments
X = sec(T('Operacions amb esdeveniments', 'Operaciones con sucesos'))
D = set(D6); A3 = {n for n in D if isprime(n)}; B3 = {3, 6}
ck(sorted(A3 | B3), [2, 3, 5, 6]); ck(sorted(A3 & B3), [3]); ck(sorted(D - A3), [1, 4, 6]); ck(sorted(D - B3), [1, 2, 4, 5])
# (D3)
X.append(E(1, T("Llancem un dau. Siguen $A=$«eixir un nombre primer» i $B=$«eixir un múltiple de 3».", "Lanzamos un dado. Sean $A=$«salir un número primo» y $B=$«salir un múltiplo de 3».") + items(
    T('Escriu els esdeveniments $A$ i $B$.', 'Escribe los sucesos $A$ y $B$.'), r'$A\cup B$, $A\cap B$, $\overline{A}$ ' + I_ + r' $\overline{B}$.', T('Són $A$ i $B$ incompatibles? Per què?', '¿Son $A$ y $B$ incompatibles? ¿Por qué?')),
    items(r'$\res{A=\{2,3,5\}}$, $\res{B=\{3,6\}}$', r'$A\cup B=\res{\{2,3,5,6\}}$, $A\cap B=\res{\{3\}}$, $\overline{A}=\res{\{1,4,6\}}$, $\overline{B}=\res{\{1,2,4,5\}}$',
          T(r'\rest{No}, perquè $A\cap B=\{3\}\ne\varnothing$.', r'\rest{No}, porque $A\cap B=\{3\}\ne\varnothing$.'))))
U = set(range(2, 17)); A1 = {n for n in U if n % 2 == 0}; B1 = U - A1; C1 = {n for n in U if isprime(n)}; D1 = {n for n in B1 if n < 9}
ck(sorted(C1), [2, 3, 5, 7, 11, 13]); ck(sorted(D1), [3, 5, 7]); ck(D1 <= C1, True); ck(A1 | B1, U); ck(C1 & D1, D1)
# (DE1)
X.append(E(2, T("En una urna hi ha 15 boles numerades del 2 al 16. Traiem una bola a l'atzar i mirem el nombre que té.", "En una urna hay 15 bolas numeradas del 2 al 16. Extraemos una bola al azar y observamos el número que tiene.") + items(
    T("Escriu tots els elements dels esdeveniments $A=$«traure parell», $B=$«traure senar», $C=$«traure primer» i $D=$«traure senar menor que 9».", "Escribe todos los elementos de los sucesos $A=$«obtener par», $B=$«obtener impar», $C=$«obtener primo» y $D=$«obtener impar menor que 9»."),
    T("Quina relació hi ha entre $A$ i $B$? I entre $C$ i $D$?", "¿Qué relación hay entre $A$ y $B$? ¿Y entre $C$ y $D$?"), T("Quin esdeveniment és $A\\cup B$? I $C\\cap D$?", "¿Cuál es el suceso $A\\cup B$? ¿Y $C\\cap D$?")),
    items(r'$A=\{%s\}$; $B=\{%s\}$; $C=\{%s\}$; $D=\{%s\}$' % tuple(','.join(map(str, sorted(z))) for z in (A1, B1, C1, D1)),
          T(r'$B$ és el contrari d\'$A$: $\res{B=\overline{A}}$. $D$ està contingut en $C$: $\res{D\subset C}$.', r'$B$ es el contrario de $A$: $\res{B=\overline{A}}$. $D$ está contenido en $C$: $\res{D\subset C}$.'),
          T(r'$A\cup B=\res{E}$ (l\'esdeveniment segur); \ $C\cap D=\res{D}$.', r'$A\cup B=\res{E}$ (el suceso seguro); \ $C\cap D=\res{D}$.'))))
U7 = set(range(10)); A7 = {n for n in U7 if n > 6}; B7 = U7 - {6}; C7 = {n for n in U7 if n < 6}
ck(A7 | B7, B7); ck(A7 & B7, A7); ck((U7 - B7) & (U7 - A7), {6})
# (DE7)
X.append(E(2, T("D'una bossa amb 10 boles numerades del 0 al 9 se'n trau una a l'atzar.", "De una bolsa que tiene 10 bolas numeradas del 0 al 9, se extrae una bola al azar.") + items(
    T("Quin és l'espai mostral?", "¿Cuál es el espacio muestral?"),
    T("Escriu tots els elements dels esdeveniments $A=$«més gran que 6», $B=$«no traure 6» i $C=$«menor que 6».", "Describe los sucesos $A=$«mayor que 6», $B=$«no obtener 6» y $C=$«menor que 6» escribiendo todos sus elementos."),
    T(r"Troba els esdeveniments $A\cup B$, $A\cap B$ i $\overline{B}\cap\overline{A}$.", r"Halla los sucesos $A\cup B$, $A\cap B$ y $\overline{B}\cap\overline{A}$.")),
    items(r'$\res{E=\{0,1,2,3,4,5,6,7,8,9\}}$', r'$A=\{7,8,9\}$; \ $B=\{0,1,2,3,4,5,7,8,9\}$; \ $C=\{0,1,2,3,4,5\}$',
          r'$A\cup B=\res{B}$ ' + T(r'i $A\cap B=\res{A}$, perquè $A\subset B$; \ $\overline{B}\cap\overline{A}=\{6\}\cap\{0,\dots,6\}=\res{\{6\}}$', r'y $A\cap B=\res{A}$, porque $A\subset B$; \ $\overline{B}\cap\overline{A}=\{6\}\cap\{0,\dots,6\}=\res{\{6\}}$'))))
ck(10 + 4 - 1, 13); ck(40 - 13, 27)
X.append(E(1, T("Traiem una carta d'una baralla espanyola de 40 cartes. Siguen $O=$«oros» i $R=$«rei». Descriu els esdeveniments $O\\cap R$, $O\\cup R$ i $\\overline{O}\\cap\\overline{R}$ i digues quantes cartes té cadascun.",
                "Sacamos una carta de una baraja española de 40 cartas. Sean $O=$«oros» y $R=$«rey». Describe los sucesos $O\\cap R$, $O\\cup R$ y $\\overline{O}\\cap\\overline{R}$ y di cuántas cartas tiene cada uno."),
    T(r"$O\cap R$: el rei d'oros (\rest{1 carta}). $O\cup R$: els 10 oros i els altres 3 reis (\rest{13 cartes}). $\overline{O}\cap\overline{R}=\overline{O\cup R}$: les que no són ni oros ni reis, $40-13=$ \rest{27 cartes}.",
      r"$O\cap R$: el rey de oros (\rest{1 carta}). $O\cup R$: los 10 oros y los otros 3 reyes (\rest{13 cartas}). $\overline{O}\cap\overline{R}=\overline{O\cup R}$: las que no son ni oros ni reyes, $40-13=$ \rest{27 cartas}.")))
A5 = {2, 4, 6}; B5 = {3, 6}
ck(sorted(A5 - B5), [2, 4]); ck(sorted(D - A5 - B5), [1, 5]); ck(sorted((D - A5) | (D - B5)), [1, 2, 3, 4, 5])
X.append(E(2, T("Llancem un dau. Siguen $A=$«parell» i $B=$«múltiple de 3». Escriu aquests esdeveniments i explica amb paraules què signifiquen:", "Lanzamos un dado. Sean $A=$«par» y $B=$«múltiplo de 3». Escribe estos sucesos y explica con palabras qué significan:")
    + tasks(3, [r'$A\cap\overline{B}$', r'$\overline{A}\cap\overline{B}$', r'$\overline{A}\cup\overline{B}$']),
    tasks(1, [T(r'$A\cap\overline{B}=\res{\{2,4\}}$: parell però no múltiple de 3.', r'$A\cap\overline{B}=\res{\{2,4\}}$: par pero no múltiplo de 3.'),
              T(r'$\overline{A}\cap\overline{B}=\res{\{1,5\}}$: ni parell ni múltiple de 3 (és el contrari d\'$A\cup B$).', r'$\overline{A}\cap\overline{B}=\res{\{1,5\}}$: ni par ni múltiplo de 3 (es el contrario de $A\cup B$).'),
              T(r'$\overline{A}\cup\overline{B}=\res{\{1,2,3,4,5\}}$: no són tots dos alhora (és el contrari d\'$A\cap B=\{6\}$).', r'$\overline{A}\cup\overline{B}=\res{\{1,2,3,4,5\}}$: no son los dos a la vez (es el contrario de $A\cap B=\{6\}$).')])))
X.append(E(1, T("En llançar un dau, considerem $A=\\{1,2\\}$, $B=\\{5,6\\}$ i $C=$«parell». Quines parelles d'esdeveniments són incompatibles?", "Al lanzar un dado, consideramos $A=\\{1,2\\}$, $B=\\{5,6\\}$ y $C=$«par». ¿Qué parejas de sucesos son incompatibles?"),
    T(r"Només \rest{$A$ i $B$}: $A\cap B=\varnothing$. En canvi, $A\cap C=\{2\}$ i $B\cap C=\{6\}$.", r"Solo \rest{$A$ y $B$}: $A\cap B=\varnothing$. En cambio, $A\cap C=\{2\}$ y $B\cap C=\{6\}$.")))

# =====================================================================
# 6. Freqüència i probabilitat. Regla de Laplace
X = sec(T('Freqüència i probabilitat. Regla de Laplace', 'Frecuencia y probabilidad. Regla de Laplace'))
FQ = [95, 102, 98, 105, 97, 103]; ck(sum(FQ), 600)
X.append(E(1, T("Hem llançat un dau 600 vegades i hem obtingut aquests resultats:", "Hemos lanzado un dado 600 veces y hemos obtenido estos resultados:")
    + cen(ctab([T('Resultat', 'Resultado')] + [str(i) for i in D6], [[T('Freqüència', 'Frecuencia')] + FQ])) + items(
    T('Calcula la freqüència relativa de cada resultat.', 'Calcula la frecuencia relativa de cada resultado.'), T('Creus que el dau està trucat? Raona la resposta.', '¿Crees que el dado está trucado? Razona la respuesta.')),
    items(', '.join(r'$f_r(%d)%s$' % (i + 1, ('=' + dc(Fr(f, 600), 3)) if Fr(f, 600) == round(Fr(f, 600), 3) else ap(Fr(f, 600))) for i, f in enumerate(FQ)),
          T(r'Totes són pròximes a $\frac16\approx0{,}167$: \rest{no sembla trucat}.', r'Todas son próximas a $\frac16\approx0{,}167$: \rest{no parece trucado}.'))))
# (D5)
ck(Fr(4, 12), Fr(1, 3)); ck(Fr(2, 12), Fr(1, 6)); ck(Fr(6, 12), Fr(1, 2))
X.append(E(1, T("Una bossa conté 4 boles roges, 6 blaves i 2 blanques. Traiem una bola a l'atzar. Calcula la probabilitat que siga:", "Una bolsa contiene 4 bolas rojas, 6 azules y 2 blancas. Sacamos una bola al azar. Calcula la probabilidad de que sea:")
    + tasks(4, [T('roja', 'roja'), T('blanca', 'blanca'), T('no blava', 'no azul'), T('verda', 'verde')]),
    tasks(4, [r'$%s$' % Rm(fs(4, 12)), r'$%s$' % Rm(fs(2, 12)), r'$%s$' % Rm(fs(6, 12)), r'$\res{0}$ ' + T('(impossible)', '(imposible)')])))
# (D6)
ck(Fr(10 + 4 - 1, 40), Fr(13, 40)); ck(Fr(28, 40), Fr(7, 10))
X.append(E(1, T("Traiem una carta d'una baralla espanyola de 40 cartes. Calcula la probabilitat que siga:", "Sacamos una carta de una baraja española de 40 cartas. Calcula la probabilidad de que sea:")
    + tasks(3, [T('de copes', 'de copas'), T('un rei', 'un rey'), T('el rei de copes', 'el rey de copas'), T('de copes o un rei', 'de copas o un rey'), T('que no siga una figura', 'que no sea una figura')]),
    tasks(3, [r'$%s$' % Rm(fs(10, 40)), r'$%s$' % Rm(fs(4, 40)), r'$\res{\frac1{40}}$', r'$\frac{10}{40}+\frac4{40}-\frac1{40}=\res{\frac{13}{40}}$', r'$%s$' % Rm(fs(28, 40))])))
# (D7)
X.append(E(1, T("En una classe de 25 alumnes hi ha 15 xiques. Triem un alumne a l'atzar per a ser delegat. Quina és la probabilitat que siga un xic?", "En una clase de 25 alumnos hay 15 chicas. Elegimos un alumno al azar para ser delegado. ¿Cuál es la probabilidad de que sea un chico?"),
    r'$P(%s)=\dfrac{10}{25}=\res{\dfrac25=0{,}4}$' % T('\\text{xic}', '\\text{chico}')))
ck(Fr(C(10, 3), C(40, 3)), Fr(3, 247)); ck(Fr(C(12, 3), C(40, 3)), Fr(11, 494)); ck(C(40, 3), 9880)
X.append(E(2, T("Traiem tres cartes alhora d'una baralla espanyola. Calcula la probabilitat que les tres siguen d'oros i la que les tres siguen figures.", "Sacamos tres cartas a la vez de una baraja española. Calcula la probabilidad de que las tres sean de oros y la de que las tres sean figuras."),
    T('Casos possibles:', 'Casos posibles:') + r' $\dbinom{40}{3}=9\,880$. \ $P(3\ %s)=\dfrac{\binom{10}{3}}{9\,880}=\dfrac{120}{9\,880}=\res{\dfrac{3}{247}}%s$; \ $P(3\ %s)=\dfrac{\binom{12}{3}}{9\,880}=\dfrac{220}{9\,880}=\res{\dfrac{11}{494}}%s$'
    % ('\\text{oros}', ap(Fr(3, 247)), T('\\text{figures}', '\\text{figuras}'), ap(Fr(11, 494)))))
ck(Fr(math.factorial(3) * math.factorial(3), math.factorial(5)), Fr(3, 10))
ck(Fr(sum(1 for p in permutations('MMMFF') if 'MMM' in ''.join(p)), len(list(permutations('MMMFF')))), Fr(3, 10))
X.append(E(2, T("Col·loquem a l'atzar en un prestatge 5 llibres diferents: 3 de matemàtiques i 2 de física. Quina és la probabilitat que els tres de matemàtiques queden junts?", "Colocamos al azar en una estantería 5 libros distintos: 3 de matemáticas y 2 de física. ¿Cuál es la probabilidad de que los tres de matemáticas queden juntos?"),
    T(r"Casos possibles: $5!=120$. Favorables: el bloc de matemàtiques i els 2 de física es poden ordenar de $3!$ maneres, i dins del bloc, de $3!$: $3!\cdot3!=36$. \ $P=\dfrac{36}{120}=\res{\dfrac3{10}}$",
      r"Casos posibles: $5!=120$. Favorables: el bloque de matemáticas y los 2 de física se pueden ordenar de $3!$ maneras, y dentro del bloque, de $3!$: $3!\cdot3!=36$. \ $P=\dfrac{36}{120}=\res{\dfrac3{10}}$")))
ck(Fr(1, C(49, 6)), Fr(1, 13983816)); ck(3 ** 14, 4782969)
X.append(E(2, T("Quina és la probabilitat d'encertar els 6 nombres de la Primitiva amb una aposta? I d'encertar els 14 resultats d'una travessa (1, X, 2) responent a l'atzar?", "¿Cuál es la probabilidad de acertar los 6 números de la Primitiva con una apuesta? ¿Y de acertar los 14 resultados de una quiniela (1, X, 2) respondiendo al azar?"),
    r'$\dfrac{1}{\binom{49}{6}}=\res{\dfrac{1}{13\,983\,816}}$; \ $\dfrac{1}{3^{14}}=\res{\dfrac1{4\,782\,969}}$'))
# (DE19)
PS = list(permutations('abc'))
ck(Fr(sum(1 for p in PS if any(p[i] == 'abc'[i] for i in range(3))), 6), Fr(2, 3))
X.append(E(2, T("Tenim tres cartes per a enviar amb els seus tres sobres. Si posem cada carta a l'atzar en un dels sobres, quina és la probabilitat que almenys una carta vaja al sobre que li correspon?", "Tenemos para enviar tres cartas con sus tres sobres correspondientes. Si metemos al azar cada carta en uno de los sobres, ¿cuál es la probabilidad de que al menos una de las cartas vaya en el sobre que le corresponde?"),
    T(r"Les cartes $a$, $b$, $c$ es poden posar en els sobres $A$, $B$, $C$ de $3!=6$ maneres: $abc$, $acb$, $bac$, $bca$, $cab$, $cba$. Només en $bca$ i $cab$ no n'hi ha cap al seu sobre: $P=\dfrac46=\res{\dfrac23}$",
      r"Las cartas $a$, $b$, $c$ se pueden meter en los sobres $A$, $B$, $C$ de $3!=6$ maneras: $abc$, $acb$, $bac$, $bca$, $cab$, $cba$. Solo en $bca$ y $cab$ no hay ninguna en su sobre: $P=\dfrac46=\res{\dfrac23}$")))
ck(Fr(C(12, 3), C(22, 3)), Fr(1, 7)); ck(Fr(C(12, 2) * 10, C(22, 3)), Fr(3, 7))
X.append(E(2, T("En una classe hi ha 12 xiques i 10 xics, i es trien a l'atzar 3 alumnes per a una comissió. Calcula la probabilitat que siguen tres xiques i la que hi haja exactament dues xiques.", "En una clase hay 12 chicas y 10 chicos, y se eligen al azar 3 alumnos para una comisión. Calcula la probabilidad de que sean tres chicas y la de que haya exactamente dos chicas."),
    r'$\dbinom{22}{3}=1\,540$ ' + T('casos possibles.', 'casos posibles.') + r' \ $P(3\,%s)=\dfrac{\binom{12}{3}}{1\,540}=\dfrac{220}{1\,540}=\res{\dfrac17}$; \ $P(2\,%s)=\dfrac{\binom{12}{2}\cdot10}{1\,540}=\dfrac{660}{1\,540}=\res{\dfrac37}$' % (T('\\text{xiques}', '\\text{chicas}'), T('\\text{xiques}', '\\text{chicas}'))))
CODES = [('%04d' % n) for n in range(10000)]
ck(lap(CODES, lambda s: s == s[::-1]), Fr(1, 100)); ck(lap(CODES, lambda s: '0' in s), Fr(3439, 10000))
X.append(E(3, T("Triem a l'atzar un codi de 4 xifres (del 0000 al 9999). Calcula la probabilitat que siga capicua i la que tinga almenys un 0.", "Elegimos al azar un código de 4 cifras (del 0000 al 9999). Calcula la probabilidad de que sea capicúa y la de que tenga al menos un 0."),
    T(r"Capicua: les dues primeres xifres es trien lliurement i les altres dues queden fixades: $\dfrac{10^2}{10^4}=\res{\dfrac1{100}}$. Cap 0: $9^4=6\,561$ codis, així que $P(\text{almenys un }0)=1-\dfrac{6\,561}{10\,000}=\res{0{,}3439}$.",
      r"Capicúa: las dos primeras cifras se eligen libremente y las otras dos quedan fijadas: $\dfrac{10^2}{10^4}=\res{\dfrac1{100}}$. Ningún 0: $9^4=6\,561$ códigos, así que $P(\text{al menos un }0)=1-\dfrac{6\,561}{10\,000}=\res{0{,}3439}$.")))

# =====================================================================
# 7. Propietats de la probabilitat
X = sec(T('Propietats de la probabilitat', 'Propiedades de la probabilidad'))
# (D8)
ck(Fr('0.35') + Fr('0.5') - Fr('0.15'), Fr('0.7'))
X.append(E(1, T(r"Siguen $A$ i $B$ dos esdeveniments amb $P(A)=0{,}35$, $P(B)=0{,}5$ i $P(A\cap B)=0{,}15$. Calcula:", r"Sean $A$ y $B$ dos sucesos con $P(A)=0{,}35$, $P(B)=0{,}5$ y $P(A\cap B)=0{,}15$. Calcula:")
    + tasks(3, [r'$P(\overline{A})$', r'$P(\overline{B})$', r'$P(A\cup B)$']),
    tasks(3, [r'$1-0{,}35=\res{0{,}65}$', r'$1-0{,}5=\res{0{,}5}$', r'$0{,}35+0{,}5-0{,}15=\res{0{,}7}$'])))
# (DE2)
ck(Fr('0.4') + Fr('0.1'), Fr('0.5')); ck(Fr('0.4') + Fr('0.5') - Fr('0.1'), Fr('0.8'))
X.append(E(2, T(r"Siguen $A$ i $B$ dos esdeveniments tals que $P(A)=0{,}4$, $P(\overline{A}\cap B)=0{,}4$ i $P(A\cap B)=0{,}1$. Calcula $P(A\cup B)$ i $P(B)$.", r"Sean $A$ y $B$ sucesos tales que $P(A)=0{,}4$, $P(\overline{A}\cap B)=0{,}4$ y $P(A\cap B)=0{,}1$. Calcula $P(A\cup B)$ y $P(B)$.")
    + recorda(r"$P(B)=P(A\cap B)+P(\overline{A}\cap B)$."),
    r'$P(B)=0{,}1+0{,}4=\res{0{,}5}$; \ $P(A\cup B)=0{,}4+0{,}5-0{,}1=\res{0{,}8}$'))
# (DE8)
ck(Fr('0.5') + Fr('0.2'), Fr('0.7')); ck(1 - Fr('0.7'), Fr('0.3')); ck(Fr('0.7') + Fr('0.3') - Fr('0.2'), Fr('0.8'))
X.append(E(2, T(r"Sabent que $P(A\cap B)=0{,}2$, $P(\overline{B})=0{,}7$ i $P(A\cap\overline{B})=0{,}5$, calcula $P(A\cup B)$ i $P(A)$.", r"Sabiendo que $P(A\cap B)=0{,}2$, $P(\overline{B})=0{,}7$ y $P(A\cap\overline{B})=0{,}5$, calcula $P(A\cup B)$ y $P(A)$."),
    r'$P(A)=P(A\cap\overline{B})+P(A\cap B)=0{,}5+0{,}2=\res{0{,}7}$; \ $P(B)=1-0{,}7=0{,}3$; \ $P(A\cup B)=0{,}7+0{,}3-0{,}2=\res{0{,}8}$'))
X.append(E(1, T(r"$A$ i $B$ són incompatibles, amb $P(A)=0{,}3$ i $P(B)=0{,}5$. Calcula $P(A\cup B)$, $P(\overline{A})$ i $P(\overline{A}\cap\overline{B})$.", r"$A$ y $B$ son incompatibles, con $P(A)=0{,}3$ y $P(B)=0{,}5$. Calcula $P(A\cup B)$, $P(\overline{A})$ y $P(\overline{A}\cap\overline{B})$."),
    r'$P(A\cup B)=0{,}3+0{,}5=\res{0{,}8}$; \ $P(\overline{A})=\res{0{,}7}$; \ $P(\overline{A}\cap\overline{B})=1-P(A\cup B)=\res{0{,}2}$'))
pa = 1 - Fr('0.4'); pab = pa + Fr('0.5') - Fr('0.9')
ck(pa, Fr('0.6')); ck(pab, Fr('0.2')); ck(pa - pab, Fr('0.4')); ck(1 - Fr('0.9'), Fr('0.1'))
X.append(E(2, T(r"Si $P(A\cup B)=0{,}9$, $P(\overline{A})=0{,}4$ i $P(B)=0{,}5$, calcula $P(A)$, $P(A\cap B)$, $P(A\cap\overline{B})$ i $P(\overline{A}\cap\overline{B})$.", r"Si $P(A\cup B)=0{,}9$, $P(\overline{A})=0{,}4$ y $P(B)=0{,}5$, calcula $P(A)$, $P(A\cap B)$, $P(A\cap\overline{B})$ y $P(\overline{A}\cap\overline{B})$."),
    r'$P(A)=\res{0{,}6}$; \ $P(A\cap B)=0{,}6+0{,}5-0{,}9=\res{0{,}2}$; \ $P(A\cap\overline{B})=0{,}6-0{,}2=\res{0{,}4}$; \ $P(\overline{A}\cap\overline{B})=1-0{,}9=\res{0{,}1}$'))
ck(Fr('0.7') + Fr('0.6') - Fr('0.2'), Fr('1.1'))
X.append(E(2, T(r"Raona si és possible que dos esdeveniments tinguen $P(A)=0{,}7$, $P(B)=0{,}6$ i $P(A\cap B)=0{,}2$.", r"Razona si es posible que dos sucesos tengan $P(A)=0{,}7$, $P(B)=0{,}6$ y $P(A\cap B)=0{,}2$."),
    T(r"\rest{No}: seria $P(A\cup B)=0{,}7+0{,}6-0{,}2=1{,}1>1$, i cap probabilitat pot ser més gran que 1. (Com a mínim, $P(A\cap B)$ hauria de ser $0{,}3$.)",
      r"\rest{No}: sería $P(A\cup B)=0{,}7+0{,}6-0{,}2=1{,}1>1$, y ninguna probabilidad puede ser mayor que 1. (Como mínimo, $P(A\cap B)$ tendría que ser $0{,}3$.)")))
ck(lap(list(D6), lambda n: n % 2 == 0 or n % 3 == 0), Fr(2, 3))
X.append(E(1, T("Llancem un dau. Amb la fórmula de la unió, calcula la probabilitat de traure un nombre parell o un múltiple de 3, i comprova-ho amb la regla de Laplace.", "Lanzamos un dado. Con la fórmula de la unión, calcula la probabilidad de sacar un número par o un múltiplo de 3, y compruébalo con la regla de Laplace."),
    r'$\dfrac36+\dfrac26-\dfrac16=\res{\dfrac23}$. \ ' + T(r'Laplace: $\{2,3,4,6\}$, 4 casos de 6.', r'Laplace: $\{2,3,4,6\}$, 4 casos de 6.')))

# =====================================================================
# 8. Experiments compostos
X = sec(T('Experiments compostos', 'Experimentos compuestos'))
# (D9)
ck(lap(E3, lambda e: e == 'CCC'), Fr(1, 8)); ck(lap(E3, lambda e: e.count('C') == 2), Fr(3, 8)); ck(lap(E3, lambda e: 'X' in e), Fr(7, 8))
X.append(E(1, T('Llancem tres monedes.', 'Lanzamos tres monedas.') + items(
    T("Fes un diagrama d'arbre i escriu l'espai mostral.", "Haz un diagrama de árbol y escribe el espacio muestral."),
    T("Calcula la probabilitat de traure tres cares, la d'exactament dues cares i la d'almenys una creu.", "Calcula la probabilidad de sacar tres caras, la de exactamente dos caras y la de al menos una cruz.")),
    items(cen(tree([(a, r'\frac12', [(b, r'\frac12', [(c, r'\frac12', [], '$%s$' % (a + b + c)) for c in 'CX']) for b in 'CX']) for a in 'CX'], ld=19, sd=(36, 18, 9)))
          + r'$E=\{' + '$, $'.join(E3) + r'\}$ ' + T('(8 resultats).', '(8 resultados).'),
          r'$P(CCC)=\res{\frac18}$; \ $P(%s)=\res{\frac38}$; \ $P(%s)=1-P(XXX)=1-\frac18=\res{\frac78}$' % (T('\\text{exactament 2 cares}', '\\text{exactamente 2 caras}'), T('\\text{almenys una creu}', '\\text{al menos una cruz}')))))
# (D10)
for f, w in [(lambda a, b: a + b == 8, Fr(5, 36)), (lambda a, b: a + b <= 4, Fr(1, 6)), (lambda a, b: a + b > 12, 0), (lambda a, b: a == b, Fr(1, 6))]:
    ck(lap(DD, lambda e: f(*e)), w)
X.append(E(1, T('Llancem dos daus i sumem els punts. Calcula la probabilitat que:', 'Lanzamos dos dados y sumamos los puntos. Calcula la probabilidad de que:') + items(
    T('la suma siga 8;', 'la suma sea 8;'), T('la suma siga 4 o menys;', 'la suma sea 4 o menos;'), T('la suma siga major que 12;', 'la suma sea mayor que 12;'), T('isquen dos nombres iguals (dobles).', 'salgan dos números iguales (dobles).')),
    cen(dtab(lambda a, b: a + b, lambda a, b: a + b == 8)) + items(r'$\res{\frac5{36}}$ ' + T('(caselles acolorides)', '(casillas coloreadas)'), r'$\frac{1+2+3}{36}=%s$' % Rm(fs(6, 36)), r'$\res{0}$ ' + T('(impossible)', '(imposible)'), r'$%s$' % Rm(fs(6, 36)))))
# (D11)
ck(Fr(3, 8) ** 2, Fr(9, 64)); ck(Fr(3, 8) * Fr(2, 7), Fr(3, 28)); ck(Fr(5, 8) * Fr(3, 7) + Fr(3, 8) * Fr(5, 7), Fr(15, 28))
X.append(E(2, T('Una bossa té 5 boles roges i 3 negres. Traiem dues boles.', 'Una bolsa tiene 5 bolas rojas y 3 negras. Sacamos dos bolas.') + items(
    T('Calcula la probabilitat que les dues siguen negres, si les traiem amb reemplaçament.', 'Calcula la probabilidad de que las dos sean negras, si las sacamos con reemplazamiento.'),
    T('Calcula la mateixa probabilitat si les traiem sense reemplaçament.', 'Calcula la misma probabilidad si las sacamos sin reemplazamiento.'),
    T("Sense reemplaçament, quina és la probabilitat que siguen d'un color diferent?", "Sin reemplazamiento, ¿cuál es la probabilidad de que sean de distinto color?")),
    items(r'$\frac38\cdot\frac38=\res{\frac9{64}}$', r'$\frac38\cdot\frac27=\frac6{56}=\res{\frac3{28}}$', r'$\frac58\cdot\frac37+\frac38\cdot\frac57=\frac{30}{56}=\res{\frac{15}{28}}$')
    + cen(tree([('R', r'\frac58', [('R', r'\frac47', [], r'$\frac{20}{56}$'), ('N', r'\frac37', [], r'$\frac{15}{56}$')]), ('N', r'\frac38', [('R', r'\frac57', [], r'$\frac{15}{56}$'), ('N', r'\frac27', [], r'$\frac{6}{56}$')])], ld=20, sd=(24, 11)))))
# (D12)
ck(Fr('0.7') ** 2, Fr('0.49')); ck(Fr('0.3') ** 2, Fr('0.09')); ck(1 - Fr('0.09'), Fr('0.91'))
X.append(E(1, T("Un jugador de bàsquet encerta el 70 \\% dels tirs lliures. Llança dos tirs lliures (considerem que són independents). Calcula la probabilitat que:", "Un jugador de baloncesto acierta el 70 \\% de los tiros libres. Lanza dos tiros libres (consideramos que son independientes). Calcula la probabilidad de que:")
    + tasks(3, [T('encerte els dos;', 'acierte los dos;'), T('no encerte cap;', 'no acierte ninguno;'), T('encerte almenys un.', 'acierte al menos uno.')]),
    tasks(3, [r'$0{,}7\cdot0{,}7=\res{0{,}49}$', r'$0{,}3\cdot0{,}3=\res{0{,}09}$', r'$1-0{,}09=\res{0{,}91}$'])))
# (D13)
ck(Fr(1, 2) * Fr(3, 6), Fr(1, 4)); ck(Fr(1, 2) * Fr(2, 6), Fr(1, 6))
X.append(E(1, T('Llancem una moneda i un dau. Calcula la probabilitat de traure:', 'Lanzamos una moneda y un dado. Calcula la probabilidad de sacar:') + tasks(2, [T('cara i un nombre parell;', 'cara y un número par;'), T('creu i un 5 o un 6.', 'cruz y un 5 o un 6.')]),
    tasks(2, [r'$\frac12\cdot\frac36=\res{\frac14}$', r'$\frac12\cdot\frac26=\res{\frac16}$'])))
# (D15)
X.append(E(1, T("La Marta ha llançat una moneda 5 vegades i ha eixit cara totes les vegades. Diu: «Ara és més probable que isca creu». Té raó? Explica-ho.", "Marta ha lanzado una moneda 5 veces y ha salido cara todas las veces. Dice: «Ahora es más probable que salga cruz». ¿Tiene razón? Explícalo."),
    T(r"\rest{No té raó.} Cada llançament és independent dels anteriors: la moneda no «recorda» què ha eixit. La probabilitat de creu continua sent $\frac12$.", r"\rest{No tiene razón.} Cada lanzamiento es independiente de los anteriores: la moneda no «recuerda» qué ha salido. La probabilidad de cruz sigue siendo $\frac12$.")))
# (DE4)
ck(1 - Fr(1, 10), Fr(9, 10))
X.append(E(1, T("Dues persones trien a l'atzar, cadascuna, un nombre del 0 al 9. Quina és la probabilitat que no pensen el mateix nombre?", "Dos personas eligen al azar, cada una de ellas, un número del 0 al 9. ¿Cuál es la probabilidad de que las dos personas no piensen el mismo número?"),
    T(r"Siga quin siga el nombre de la primera, la segona coincideix amb probabilitat $\frac1{10}$ (o bé: 10 parelles iguals de 100). $P=1-\frac1{10}=\res{0{,}9}$",
      r"Sea cual sea el número de la primera, la segunda coincide con probabilidad $\frac1{10}$ (o bien: 10 parejas iguales de 100). $P=1-\frac1{10}=\res{0{,}9}$")))
# (DE13)
ck(Fr(1, 5), Fr('0.2')); ck(Fr(1, 25), Fr('0.04'))
X.append(E(2, items(T("Dues persones trien a l'atzar, cadascuna, un nombre de l'1 al 5. Quina és la probabilitat que totes dues trien el mateix nombre?", "Dos personas eligen al azar, cada una de ellas, un número del 1 al 5. ¿Cuál es la probabilidad de que las dos elijan el mismo número?"),
                    T("Si són tres persones les que trien a l'atzar un nombre de l'1 al 5, quina és la probabilitat que totes tres trien el mateix nombre?", "Si son tres personas las que eligen al azar, cada una de ellas, un número del 1 al 5, ¿cuál es la probabilidad de que las tres elijan el mismo número?")),
    items(r'$\frac15=\res{0{,}2}$', T(r'La segona i la tercera han de coincidir amb la primera: $\frac15\cdot\frac15=\res{\frac1{25}=0{,}04}$', r'La segunda y la tercera tienen que coincidir con la primera: $\frac15\cdot\frac15=\res{\frac1{25}=0{,}04}$'))))
# (DE10)
pa_ = Fr(10, 40) * Fr(9, 39); pb_ = 2 * Fr(10, 40) * Fr(10, 39); pc_ = 1 - Fr(30, 40) * Fr(29, 39); pd_ = Fr(10, 40) * Fr(10, 39)
ck(pa_, Fr(3, 52)); ck(pb_, Fr(5, 39)); ck(pc_, Fr(23, 52)); ck(pd_, Fr(5, 78))
X.append(E(2, T("Traiem dues cartes d'una baralla espanyola de 40 cartes (sense reemplaçament). Calcula la probabilitat que siguen:", "Extraemos dos cartas de una baraja española (de cuarenta cartas). Calcula la probabilidad de que sean:")
    + items(T("les dues d'oros;", "las dos de oros;"), T("una de copes i l'altra d'oros;", "una de copas y otra de oros;"), T("almenys una d'oros;", "al menos una de oros;"), T("la primera de copes i la segona d'oros.", "la primera de copas y la segunda de oros.")),
    items(r'$\frac{10}{40}\cdot\frac9{39}=\res{\frac3{52}}%s$' % ap(pa_), T(r'Copes--oros o oros--copes: $2\cdot\frac{10}{40}\cdot\frac{10}{39}=\res{\frac5{39}}%s$', r'Copas--oros u oros--copas: $2\cdot\frac{10}{40}\cdot\frac{10}{39}=\res{\frac5{39}}%s$') % ap(pb_),
          r'$1-P(%s)=1-\frac{30}{40}\cdot\frac{29}{39}=1-\frac{29}{52}=\res{\frac{23}{52}}%s$' % (T('\\text{cap d\'oros}', '\\text{ninguna de oros}'), ap(pc_)), r'$\frac{10}{40}\cdot\frac{10}{39}=\res{\frac5{78}}%s$' % ap(pd_))))
# (DE18)
p18 = 1 - Fr(50, 85) * Fr(49, 84) * Fr(48, 83)
ck(round(float(p18), 3), 0.802)
X.append(E(3, T("En unes oposicions, el temari té 85 temes i se'n trien tres a l'atzar. Si un opositor sap 35 dels 85 temes, quina és la probabilitat que sàpia almenys un dels tres temes?", "En unas oposiciones, el temario consta de 85 temas. Se eligen tres temas al azar de entre los 85. Si un opositor sabe 35 de los 85 temas, ¿cuál es la probabilidad de que sepa al menos uno de los tres temas?"),
    T(r"Pel contrari: no en sap 50. $P(\text{almenys un})=1-P(\text{cap})=1-\dfrac{50}{85}\cdot\dfrac{49}{84}\cdot\dfrac{48}{83}\approx1-0{,}198=\res{0{,}802}$",
      r"Por el contrario: no sabe 50. $P(\text{al menos uno})=1-P(\text{ninguno})=1-\dfrac{50}{85}\cdot\dfrac{49}{84}\cdot\dfrac{48}{83}\approx1-0{,}198=\res{0{,}802}$")))
p6 = 1 - Fr(5, 6) ** 4; ck(p6, Fr(671, 1296))
X.append(E(2, T("Llancem un dau 4 vegades. Quina és la probabilitat d'obtindre almenys un 6?", "Lanzamos un dado 4 veces. ¿Cuál es la probabilidad de obtener al menos un 6?"),
    r'$1-\left(\frac56\right)^4=1-\frac{625}{1\,296}=\res{\frac{671}{1\,296}}%s$' % ap(p6) + T(" (una mica més de la meitat).", " (algo más de la mitad).")))
BG = 'RRBBBV'
pairs = [(a, b) for i, a in enumerate(BG) for j, b in enumerate(BG) if i != j]
ck(lap(pairs, lambda p: p[0] == p[1]), Fr(4, 15)); ck(lap(pairs, lambda p: 'B' not in p), Fr(1, 5))
X.append(E(2, T("Una bossa té 2 boles roges, 3 blaves i 1 verda. Traiem dues boles sense reemplaçament. Calcula la probabilitat que siguen del mateix color i la que no n'hi haja cap de blava.", "Una bolsa tiene 2 bolas rojas, 3 azules y 1 verde. Sacamos dos bolas sin reemplazamiento. Calcula la probabilidad de que sean del mismo color y la de que no haya ninguna azul."),
    r'$P(%s)=\frac26\cdot\frac15+\frac36\cdot\frac25=\frac{2}{30}+\frac{6}{30}=\res{\frac4{15}}$ ' % T('\\text{mateix color}', '\\text{mismo color}') + T('(dues verdes és impossible); ', '(dos verdes es imposible); ')
    + r'$P(%s)=\frac36\cdot\frac25=\res{\frac15}$' % T('\\text{cap blava}', '\\text{ninguna azul}')))

# =====================================================================
# 9. Taules de contingència i probabilitat condicionada
X = sec(T('Taules de contingència i probabilitat condicionada', 'Tablas de contingencia y probabilidad condicionada'))
# (D14)
ck(90 - 36, 54); ck(200 - 90, 110); ck(110 - 30, 80); ck(36 + 30, 66); ck(Fr(36, 66), Fr(6, 11))
X.append(E(2, T("En una enquesta a 200 persones sobre si van a treballar amb bicicleta s'han obtingut aquestes dades:", "En una encuesta a 200 personas sobre si van a trabajar en bicicleta se han obtenido estos datos:")
    + cen(ctab(['', T('Bicicleta', 'Bicicleta'), T('No bicicleta', 'No bicicleta'), 'Total'], [[T('Homes', 'Hombres'), 36, '', 90], [T('Dones', 'Mujeres'), 30, '', ''], ['Total', '', '', 200]], grid=True)) + items(
    T('Completa la taula.', 'Completa la tabla.'), T("Triem una persona a l'atzar. Quina és la probabilitat que vaja amb bicicleta?", "Elegimos una persona al azar. ¿Cuál es la probabilidad de que vaya en bicicleta?"),
    T('Quina és la probabilitat que siga una dona i no vaja amb bicicleta?', '¿Cuál es la probabilidad de que sea una mujer y no vaya en bicicleta?'), T('Si triem un home, quina és la probabilitat que vaja amb bicicleta?', 'Si elegimos un hombre, ¿cuál es la probabilidad de que vaya en bicicleta?'),
    T('Si triem una persona que va amb bicicleta, quina és la probabilitat que siga un home?', 'Si elegimos una persona que va en bicicleta, ¿cuál es la probabilidad de que sea un hombre?')),
    items(cen(ctab(['', T('Bicicleta', 'Bicicleta'), T('No bicicleta', 'No bicicleta'), 'Total'], [[T('Homes', 'Hombres'), 36, r'\textbf{54}', 90], [T('Dones', 'Mujeres'), 30, r'\textbf{80}', r'\textbf{110}'], ['Total', r'\textbf{66}', r'\textbf{134}', 200]])),
          r'$\frac{66}{200}=\res{0{,}33}$', r'$\frac{80}{200}=\res{0{,}4}$', r'$\frac{36}{90}=\res{0{,}4}$', r'$\frac{36}{66}=\res{\frac6{11}}\approx0{,}55$')))
# (DE5)
ck(Fr(48 + 36 - 12, 120), Fr(3, 5)); ck(Fr(12, 48), Fr(1, 4)); ck(Fr(36 - 12, 120), Fr(1, 5))
X.append(E(2, T("En un viatge organitzat per Europa per a 120 persones, 48 dels que hi van saben parlar anglés, 36 saben parlar francés i 12 parlen tots dos idiomes. Triem un dels viatgers a l'atzar.", "En un viaje organizado por Europa para 120 personas, 48 de los que van saben hablar inglés, 36 saben hablar francés, y 12 de ellos hablan los dos idiomas. Escogemos uno de los viajeros al azar.") + items(
    T('Quina és la probabilitat que parle algun dels dos idiomes?', '¿Cuál es la probabilidad de que hable alguno de los dos idiomas?'), T('Quina és la probabilitat que parle francés, sabent que parla anglés?', '¿Cuál es la probabilidad de que hable francés, sabiendo que habla inglés?'),
    T('Quina és la probabilitat que només parle francés?', '¿Cuál es la probabilidad de que solo hable francés?')),
    cen(ctab(['', '$F$', r'$\overline{F}$', 'Total'], [['$I$', 12, 36, 48], [r'$\overline{I}$', 24, 60, 72], ['Total', 36, 84, 120]])) + items(
        r'$P(I\cup F)=\frac{48}{120}+\frac{36}{120}-\frac{12}{120}=\frac{72}{120}=\res{0{,}6}$', r'$P(F\,|\,I)=\frac{12}{48}=\res{0{,}25}$', r'$P(F\cap\overline{I})=\frac{24}{120}=\res{0{,}2}$')))
# (DE11)
ck(Fr(120 - 47, 120), Fr(73, 120)); ck(Fr(92, 120), Fr(23, 30))
X.append(E(2, T("S'ha fet una enquesta a un grup de 120 persones sobre si els agrada llegir i veure la televisió: a 32 persones els agrada llegir i veure la tele, a 92 els agrada llegir i a 47 els agrada veure la tele. Si triem una d'aquestes persones a l'atzar:",
                "Se hace una encuesta en un grupo de 120 personas, preguntando si les gusta leer y ver la televisión: a 32 personas les gusta leer y ver la tele, a 92 personas les gusta leer y a 47 personas les gusta ver la tele. Si elegimos al azar una de esas personas:") + items(
    T('Quina és la probabilitat que no li agrade veure la tele?', '¿Cuál es la probabilidad de que no le guste ver la tele?'), T('Quina és la probabilitat que li agrade llegir, sabent que li agrada veure la tele?', '¿Cuál es la probabilidad de que le guste leer, sabiendo que le gusta ver la tele?'),
    T('Quina és la probabilitat que li agrade llegir?', '¿Cuál es la probabilidad de que le guste leer?')),
    cen(ctab(['', '$T$', r'$\overline{T}$', 'Total'], [['$L$', 32, 60, 92], [r'$\overline{L}$', 15, 13, 28], ['Total', 47, 73, 120]])) + items(
        r'$\frac{73}{120}%s$' % Rm(ap(Fr(73, 120), 2)), r'$P(L\,|\,T)=\frac{32}{47}%s$' % Rm(ap(Fr(32, 47), 2)), r'$\frac{92}{120}=\frac{23}{30}%s$' % Rm(ap(Fr(23, 30), 2)))))
# (DE14)
ck(30 - 6, 24); ck(18 + 16 - 24, 10); ck(Fr(10, 18), Fr(5, 9)); ck(Fr(18, 30) * Fr(16, 30), Fr(8, 25))
X.append(E(2, T("En una classe de 30 alumnes hi ha 18 que han aprovat matemàtiques, 16 que han aprovat anglés i 6 que no n'han aprovat cap de les dues. Triem un alumne a l'atzar:", "En una clase de 30 alumnos hay 18 que han aprobado matemáticas, 16 que han aprobado inglés y 6 que no han aprobado ninguna de las dos. Elegimos al azar un alumno de esa clase:") + items(
    T('Quina és la probabilitat que haja aprovat anglés i matemàtiques?', '¿Cuál es la probabilidad de que haya aprobado inglés y matemáticas?'), T('Sabent que ha aprovat matemàtiques, quina és la probabilitat que haja aprovat anglés?', 'Sabiendo que ha aprobado matemáticas, ¿cuál es la probabilidad de que haya aprobado inglés?'),
    T('Són independents els esdeveniments «aprovar matemàtiques» i «aprovar anglés»?', '¿Son independientes los sucesos «aprobar matemáticas» y «aprobar inglés»?')),
    cen(ctab(['', '$I$', r'$\overline{I}$', 'Total'], [['$M$', 10, 8, 18], [r'$\overline{M}$', 6, 6, 12], ['Total', 16, 14, 30]])) + items(
        r'$P(M\cap I)=\frac{10}{30}=\res{\frac13}$', r'$P(I\,|\,M)=\frac{10}{18}=\res{\frac59}\approx0{,}56$',
        T(r'$P(M)\cdot P(I)=\frac{18}{30}\cdot\frac{16}{30}=\frac{8}{25}\ne\frac13=P(M\cap I)$: \rest{no són independents}.', r'$P(M)\cdot P(I)=\frac{18}{30}\cdot\frac{16}{30}=\frac{8}{25}\ne\frac13=P(M\cap I)$: \rest{no son independientes}.'))))
# (DE16)
ck(Fr(55, 100), Fr(11, 20)); ck(Fr(35, 75), Fr(7, 15)); ck(55 - 40, 15)
X.append(E(2, T("En un poble hi ha 100 joves; 40 dels xics i 35 de les xiques juguen a tennis. El total de xiques del poble és 45. Si triem un jove a l'atzar:", "En un pueblo hay 100 jóvenes; 40 de los chicos y 35 de las chicas juegan al tenis. El total de chicas en el pueblo es de 45. Si elegimos un joven de esa localidad al azar:") + items(
    T('Quina és la probabilitat que siga xic?', '¿Cuál es la probabilidad de que sea chico?'), T('Si sabem que juga a tennis, quina és la probabilitat que siga xica?', 'Si sabemos que juega al tenis, ¿cuál es la probabilidad de que sea chica?'),
    T('Quina és la probabilitat que siga un xic que no juga a tennis?', '¿Cuál es la probabilidad de que sea un chico que no juegue al tenis?')),
    cen(ctab(['', T('Tennis', 'Tenis'), T('No tennis', 'No tenis'), 'Total'], [[T('Xics', 'Chicos'), 40, 15, 55], [T('Xiques', 'Chicas'), 35, 10, 45], ['Total', 75, 25, 100]])) + items(
        r'$\frac{55}{100}=\res{0{,}55}$', r'$P(%s)=\frac{35}{75}=\res{\frac7{15}}\approx0{,}47$' % T('\\text{xica}\\,|\\,\\text{tennis}', '\\text{chica}\\,|\\,\\text{tenis}'), r'$\frac{15}{100}=\res{0{,}15}$')))
# (DE20)
both = 2100 + 1500 - (2500 - 350)
ck(both, 1450); ck(Fr(both, 2500), Fr(29, 50)); ck(Fr(2100 - both, 2500 - 1500), Fr(13, 20)); ck(Fr(both, 2100), Fr(29, 42))
X.append(E(3, T("Una cadena de televisió va fer una enquesta a 2 500 persones per a saber l'audiència d'un debat i d'una pel·lícula que es van emetre en hores diferents: 2 100 van veure la pel·lícula, 1 500 van veure el debat i 350 no van veure cap dels dos programes. Si triem a l'atzar un dels enquestats:",
                "En una cadena de televisión se hizo una encuesta a 2 500 personas para saber la audiencia de un debate y de una película que se emitieron en horas distintas: 2 100 vieron la película, 1 500 vieron el debate y 350 no vieron ninguno de los dos programas. Si elegimos al azar a uno de los encuestados:") + items(
    T('Quina és la probabilitat que veiera la pel·lícula i el debat?', '¿Cuál es la probabilidad de que viera la película y el debate?'), T('Quina és la probabilitat que veiera la pel·lícula, sabent que no va veure el debat?', '¿Cuál es la probabilidad de que viera la película, sabiendo que no vio el debate?'),
    T('Sabent que va veure la pel·lícula, quina és la probabilitat que veiera el debat?', 'Sabiendo que vio la película, ¿cuál es la probabilidad de que viera el debate?')),
    T(r'Han vist algun programa $2\,500-350=2\,150$ persones; tots dos, $2\,100+1\,500-2\,150=1\,450$.', r'Han visto algún programa $2\,500-350=2\,150$ personas; los dos, $2\,100+1\,500-2\,150=1\,450$.')
    + cen(ctab(['', '$D$', r'$\overline{D}$', 'Total'], [['$P$', '1\\,450', 650, '2\\,100'], [r'$\overline{P}$', 50, 350, 400], ['Total', '1\\,500', '1\\,000', '2\\,500']])) + items(
        r'$P(D\cap P)=\frac{1\,450}{2\,500}=\res{\frac{29}{50}=0{,}58}$', T(r'Ens restringim als 1\,000 que no van veure el debat: $P(P\,|\,\overline{D})=\frac{650}{1\,000}=\res{0{,}65}$', r'Nos restringimos a los 1\,000 que no vieron el debate: $P(P\,|\,\overline{D})=\frac{650}{1\,000}=\res{0{,}65}$'),
        r'$P(D\,|\,P)=\frac{1\,450}{2\,100}=\res{\frac{29}{42}}\approx0{,}69$')))
# (DE3)
ck(1 - Fr('0.9'), Fr('0.1')); ck(Fr('0.4') * Fr('0.3'), Fr('0.12')); ck(Fr('0.2') / Fr('0.3'), Fr(2, 3))
X.append(E(3, T(r"Siguen $A$ i $B$ dos esdeveniments tals que $P(\overline{A})=0{,}6$, $P(B)=0{,}3$ i $P(\overline{A}\cup\overline{B})=0{,}9$.", r"Sean $A$ y $B$ dos sucesos tales que $P(\overline{A})=0{,}6$, $P(B)=0{,}3$ y $P(\overline{A}\cup\overline{B})=0{,}9$.") + items(
    T('Són independents $A$ i $B$?', '¿Son independientes $A$ y $B$?'), r'$P(\overline{A}\,|\,B)$.')
    + recorda(r"$\overline{A}\cup\overline{B}=\overline{A\cap B}$ " + T("(lleis de De Morgan).", "(leyes de De Morgan).")),
    items(T(r'$P(A\cap B)=1-0{,}9=0{,}1$ i $P(A)=1-0{,}6=0{,}4$. Com que $P(A)\cdot P(B)=0{,}4\cdot0{,}3=0{,}12\ne0{,}1$, \rest{no són independents}.', r'$P(A\cap B)=1-0{,}9=0{,}1$ y $P(A)=1-0{,}6=0{,}4$. Como $P(A)\cdot P(B)=0{,}4\cdot0{,}3=0{,}12\ne0{,}1$, \rest{no son independientes}.'),
          r'$P(\overline{A}\cap B)=P(B)-P(A\cap B)=0{,}3-0{,}1=0{,}2$; \ $P(\overline{A}\,|\,B)=\dfrac{0{,}2}{0{,}3}=\res{\dfrac23}\approx0{,}67$')))
# (DE9)
pA = 1 - Fr('0.48'); pAB = pA + Fr('0.42') - Fr('0.82')
ck(pA, Fr('0.52')); ck(pAB, Fr('0.12')); ck(pA * Fr('0.42'), Fr('0.2184')); ck(round(float(pAB / Fr('0.42')), 2), 0.29)
X.append(E(3, T(r"De dos esdeveniments $A$ i $B$ sabem que $P(\overline{A})=0{,}48$, $P(A\cup B)=0{,}82$ i $P(B)=0{,}42$.", r"De dos sucesos $A$ y $B$ sabemos que $P(\overline{A})=0{,}48$, $P(A\cup B)=0{,}82$ y $P(B)=0{,}42$.") + items(
    T('Són $A$ i $B$ independents?', '¿Son $A$ y $B$ independientes?'), T(r'Quant val $P(A\,|\,B)$?', r'¿Cuánto vale $P(A\,|\,B)$?')),
    items(T(r'$P(A)=0{,}52$; \ $P(A\cap B)=0{,}52+0{,}42-0{,}82=0{,}12$.\\ $P(A)\cdot P(B)=0{,}2184\ne0{,}12$: \rest{no són independents}.', r'$P(A)=0{,}52$; \ $P(A\cap B)=0{,}52+0{,}42-0{,}82=0{,}12$.\\ $P(A)\cdot P(B)=0{,}2184\ne0{,}12$: \rest{no son independientes}.'),
          r'$P(A\,|\,B)=\dfrac{0{,}12}{0{,}42}=\dfrac27\approx\res{0{,}29}$')))
ck(Fr('0.6') * Fr('0.5'), Fr('0.3')); ck(Fr('0.3') * Fr('0.5'), Fr('0.15')); ck(Fr('0.3') + Fr('0.5') - Fr('0.15'), Fr('0.65'))
X.append(E(2, items(T(r"Si $P(A)=0{,}6$ i $P(B\,|\,A)=0{,}5$, quant val $P(A\cap B)$?", r"Si $P(A)=0{,}6$ y $P(B\,|\,A)=0{,}5$, ¿cuánto vale $P(A\cap B)$?"),
                    T(r"$A$ i $B$ són independents, amb $P(A)=0{,}3$ i $P(B)=0{,}5$. Calcula $P(A\cap B)$, $P(A\cup B)$ i $P(A\,|\,B)$.", r"$A$ y $B$ son independientes, con $P(A)=0{,}3$ y $P(B)=0{,}5$. Calcula $P(A\cap B)$, $P(A\cup B)$ y $P(A\,|\,B)$.")),
    items(r'$P(A\cap B)=P(A)\cdot P(B\,|\,A)=0{,}6\cdot0{,}5=\res{0{,}3}$', r'$P(A\cap B)=0{,}3\cdot0{,}5=\res{0{,}15}$; \ $P(A\cup B)=0{,}3+0{,}5-0{,}15=\res{0{,}65}$; \ $P(A\,|\,B)=P(A)=\res{0{,}3}$')))

# =====================================================================
# 10. Problemes amb arbres de dues etapes
X = sec(T('Problemes amb arbres de dues etapes', 'Problemas con árboles de dos etapas'))
# (DE6)
p6a = Fr(1, 2) * Fr(3, 7) + Fr(1, 2) * Fr(2, 5); ck(p6a, Fr(29, 70)); ck(Fr(3, 14) / p6a, Fr(15, 29))
X.append(E(2, T("Una urna A conté 7 boles numerades de l'1 al 7. En una altra urna, B, hi ha 5 boles numerades de l'1 al 5. Llancem una moneda equilibrada: si ix cara, traiem una bola de l'urna A i, si ix creu, la traiem de B.", "Una urna, A, contiene 7 bolas numeradas del 1 al 7. En otra urna, B, hay 5 bolas numeradas del 1 al 5. Lanzamos una moneda equilibrada, de forma que, si sale cara, extraemos una bola de la urna A y, si sale cruz, la extraemos de B.") + items(
    T("Quina és la probabilitat d'obtindre un nombre parell?", "¿Cuál es la probabilidad de obtener un número par?"), T("Sabent que ha eixit un nombre parell, quina és la probabilitat que fora de l'urna A?", "Sabiendo que salió un número par, ¿cuál es la probabilidad de que fuera de la urna A?")),
    cen(two_stage([('A', Fr(1, 2)), ('B', Fr(1, 2))], {'A': [(T('Parell', 'Par'), Fr(3, 7)), (T('Senar', 'Impar'), Fr(4, 7))], 'B': [(T('Parell', 'Par'), Fr(2, 5)), (T('Senar', 'Impar'), Fr(3, 5))]})) + items(
        r'$P(%s)=\frac12\cdot\frac37+\frac12\cdot\frac25=\frac3{14}+\frac15=\res{\frac{29}{70}}$' % T('\\text{parell}', '\\text{par}'), r'$P(A\,|\,%s)=\dfrac{3/14}{29/70}=\res{\dfrac{15}{29}}$' % T('\\text{parell}', '\\text{par}'))))
# (DE12)
pos = Fr('0.01') * Fr('0.97') + Fr('0.99') * Fr('0.02'); ck(pos, Fr('0.0295')); ck(round(float(Fr('0.0097') / pos), 2), 0.33)
X.append(E(2, T("L'1 \\% de la població d'un lloc pateix una malaltia. Per a detectar-la es fa una prova de diagnòstic que dona positiu en el 97 \\% dels pacients que pateixen la malaltia, i negatiu en el 98 \\% dels que no la pateixen. Si triem una persona a l'atzar:", "El 1 \\% de la población de un determinado lugar padece una enfermedad. Para detectar esta enfermedad se realiza una prueba de diagnóstico. Esta prueba da positiva en el 97 \\% de los pacientes que padecen la enfermedad; en el 98 \\% de los individuos que no la padecen da negativa. Si elegimos al azar un individuo de esa población:") + items(
    T('Quina és la probabilitat que done positiu i patisca la malaltia?', '¿Cuál es la probabilidad de que el individuo dé positivo y padezca la enfermedad?'), T('Si sabem que ha donat positiu, quina és la probabilitat que patisca la malaltia?', 'Si sabemos que ha dado positiva, ¿cuál es la probabilidad de que padezca la enfermedad?')),
    cen(two_stage([(T('Malalt', 'Enfermo'), Fr('0.01')), (T('Sa', 'Sano'), Fr('0.99'))], {T('Malalt', 'Enfermo'): [('+', Fr('0.97')), ('$-$', Fr('0.03'))], T('Sa', 'Sano'): [('+', Fr('0.02')), ('$-$', Fr('0.98'))]}, fmt=dc))
    + items(r'$0{,}01\cdot0{,}97=\res{0{,}0097}$', r'$P(%s)=0{,}0097+0{,}0198=0{,}0295$; \ $P(%s\,|\,+)=\dfrac{0{,}0097}{0{,}0295}\approx\res{0{,}33}$' % ('+', T('\\text{malalt}', '\\text{enfermo}')))))
# (DE15)
p15 = Fr(3, 10) * Fr(7, 9) + Fr(7, 10) * Fr(6, 9); ck(p15, Fr(7, 10)); ck(Fr(3, 10) * Fr(7, 9), Fr(7, 30))
X.append(E(3, T("Tenim dues bosses, A i B. A la bossa A hi ha 3 boles blanques i 7 roges; a la B, 6 blanques i 2 roges. Traiem una bola d'A i la passem a B. Després traiem una bola de B.", "Tenemos dos bolsas, A y B. En la bolsa A hay 3 bolas blancas y 7 rojas. En la bolsa B hay 6 bolas blancas y 2 rojas. Sacamos una bola de A y la pasamos a B. Después extraemos una bola de B.") + items(
    T('Quina és la probabilitat que la bola traguda de B siga blanca?', '¿Cuál es la probabilidad de que la bola extraída de B sea blanca?'), T('Quina és la probabilitat que les dues boles siguen blanques?', '¿Cuál es la probabilidad de que las dos bolas sean blancas?')),
    T(r"Si passem una blanca, B queda amb 7 blanques i 2 roges; si passem una roja, amb 6 blanques i 3 roges.", r"Si pasamos una blanca, B queda con 7 blancas y 2 rojas; si pasamos una roja, con 6 blancas y 3 rojas.")
    + cen(two_stage([(T('Bl', 'Bl'), Fr(3, 10)), ('R', Fr(7, 10))], {T('Bl', 'Bl'): [(T('Bl', 'Bl'), Fr(7, 9)), ('R', Fr(2, 9))], 'R': [(T('Bl', 'Bl'), (6, 9)), ('R', (3, 9))]}))
    + items(r'$\frac3{10}\cdot\frac79+\frac7{10}\cdot\frac69=\frac{21}{90}+\frac{42}{90}=\frac{63}{90}=\res{\frac7{10}}$', r'$\frac3{10}\cdot\frac79=\frac{21}{90}=\res{\frac7{30}}$')))
# (DE17)
p17 = Fr(1, 6) * Fr(3, 8) + Fr(5, 6) * Fr(6, 10); ck(p17, Fr(9, 16)); ck(Fr(1, 16) / p17, Fr(1, 9))
X.append(E(2, T("Una bossa A conté 3 boles roges i 5 verdes. Una altra bossa B conté 6 boles roges i 4 verdes. Llancem un dau: si ix un 1, traiem una bola de la bossa A, i si no ix un 1, la traiem de B.", "Una bolsa A contiene 3 bolas rojas y 5 verdes. Otra bolsa B contiene 6 bolas rojas y 4 verdes. Lanzamos un dado: si sale un uno, extraemos una bola de la bolsa A; y si no sale un uno, la extraemos de B.") + items(
    T("Quina és la probabilitat d'obtindre una bola roja?", "¿Cuál es la probabilidad de obtener una bola roja?"), T('Sabent que ha eixit roja, quina és la probabilitat que fora de A?', 'Sabiendo que salió roja, ¿cuál es la probabilidad de que fuera de A?')),
    cen(two_stage([('A', Fr(1, 6)), ('B', Fr(5, 6))], {'A': [('R', Fr(3, 8)), ('V', Fr(5, 8))], 'B': [('R', (6, 10)), ('V', (4, 10))]}))
    + items(r'$P(R)=\frac16\cdot\frac38+\frac56\cdot\frac6{10}=\frac1{16}+\frac12=\res{\frac9{16}}$', r'$P(A\,|\,R)=\dfrac{1/16}{9/16}=\res{\dfrac19}$')))
# (DE21)
p21 = Fr(1, 2) * Fr(3, 10) + Fr(1, 2) * Fr(3, 8); ck(p21, Fr(27, 80)); ck(Fr(3, 20) / p21, Fr(4, 9))
X.append(E(2, T("Tenim dues urnes: la primera té 3 boles roges, 3 blanques i 4 negres; la segona té 4 boles roges, 3 blanques i 1 negra. Triem una urna a l'atzar i traiem una bola.", "Tenemos dos urnas: la primera tiene 3 bolas rojas, 3 blancas y 4 negras; la segunda tiene 4 bolas rojas, 3 blancas y 1 negra. Elegimos una urna al azar y extraemos una bola.") + items(
    T('Quina és la probabilitat que la bola traguda siga blanca?', '¿Cuál es la probabilidad de que la bola extraída sea blanca?'), T('Sabent que la bola ha sigut blanca, quina és la probabilitat que fora de la primera urna?', 'Sabiendo que la bola extraída fue blanca, ¿cuál es la probabilidad de que fuera de la primera urna?')),
    cen(two_stage([('I', Fr(1, 2)), ('II', Fr(1, 2))], {'I': [('R', (3, 10)), (T('Bl', 'Bl'), (3, 10)), ('N', (4, 10))], 'II': [('R', (4, 8)), (T('Bl', 'Bl'), (3, 8)), ('N', (1, 8))]}, sd=(42, 13)))
    + items(r'$P(%s)=\frac12\cdot\frac3{10}+\frac12\cdot\frac38=\frac3{20}+\frac3{16}=\res{\frac{27}{80}}$' % T('\\text{Bl}', '\\text{Bl}'), r'$P(\text{I}\,|\,%s)=\dfrac{3/20}{27/80}=\res{\dfrac49}$' % T('\\text{Bl}', '\\text{Bl}'))))
pf = Fr('0.6') * Fr('0.02') + Fr('0.4') * Fr('0.05'); ck(pf, Fr('0.032')); ck(Fr('0.02') / pf, Fr('0.625'))
X.append(E(2, T("Una empresa fabrica peces en dues plantes: la planta A en fa el 60 \\% i la B, el 40 \\%. El 2 \\% de les peces d'A i el 5 \\% de les de B són defectuoses. Triem una peça a l'atzar. Quina és la probabilitat que siga defectuosa? Si és defectuosa, quina és la probabilitat que vinga de la planta B?",
                "Una empresa fabrica piezas en dos plantas: la planta A hace el 60 \\% y la B, el 40 \\%. El 2 \\% de las piezas de A y el 5 \\% de las de B son defectuosas. Elegimos una pieza al azar. ¿Cuál es la probabilidad de que sea defectuosa? Si es defectuosa, ¿cuál es la probabilidad de que venga de la planta B?"),
    r'$P(D)=0{,}6\cdot0{,}02+0{,}4\cdot0{,}05=0{,}012+0{,}02=\res{0{,}032}$; \ $P(B\,|\,D)=\dfrac{0{,}02}{0{,}032}=\res{0{,}625}$'))
pc = Fr(1, 3) * Fr(2, 5) + Fr(2, 3) * Fr(1, 4); ck(pc, Fr(3, 10)); ck(Fr(2, 15) / pc, Fr(4, 9))
X.append(E(3, T("En un institut, un terç dels alumnes de 4t van a l'institut en bicicleta i la resta, a peu. Dels que van en bicicleta, el 40 \\% arriba alguna vegada tard; dels que van a peu, el 25 \\%. Quin percentatge d'alumnes arriba alguna vegada tard? Si un alumne ha arribat tard, quina és la probabilitat que vaja en bicicleta?",
                "En un instituto, un tercio de los alumnos de 4.º van al instituto en bicicleta y el resto, a pie. De los que van en bicicleta, el 40 \\% llega alguna vez tarde; de los que van a pie, el 25 \\%. ¿Qué porcentaje de alumnos llega alguna vez tarde? Si un alumno ha llegado tarde, ¿cuál es la probabilidad de que vaya en bicicleta?"),
    r'$P(%s)=\frac13\cdot\frac25+\frac23\cdot\frac14=\frac2{15}+\frac16=\frac3{10}$: \rest{30 \%%}. \ $P(%s\,|\,%s)=\dfrac{2/15}{3/10}=\res{\dfrac49}\approx0{,}44$'
    % (T('\\text{tard}', '\\text{tarde}'), T('\\text{bici}', '\\text{bici}'), T('\\text{tard}', '\\text{tarde}'))))

PRE = r'''\usetikzlibrary{calc,trees}
\usepackage{enumitem}
'''
TIT = T('Tècniques de recompte. Probabilitat', 'Técnicas de recuento. Probabilidad')
build(HERE, 9, TIT, S,
      T("recompte, principi de multiplicació, factorial, variacions, permutacions, combinacions, nombre combinatori, experiment aleatori, espai mostral, esdeveniments, regla de Laplace, probabilitat condicionada, taules de contingència, diagrames d'arbre, probabilitat total",
        "recuento, principio de multiplicación, factorial, variaciones, permutaciones, combinaciones, número combinatorio, experimento aleatorio, espacio muestral, sucesos, regla de Laplace, probabilidad condicionada, tablas de contingencia, diagramas de árbol, probabilidad total"),
      T(r"Resol-los al quadern mostrant tots els passos: el tipus de recompte, el diagrama d'arbre o la taula que fas servir i les operacions. La fitxa recull tots els exercicis del departament i n'afegeix de nous, sobretot de tècniques de recompte. Les seccions segueixen l'ordre dels apunts de la unitat (9.1--9.10).",
        r"Resuélvelos en el cuaderno mostrando todos los pasos: el tipo de recuento, el diagrama de árbol o la tabla que usas y las operaciones. La ficha recoge todos los ejercicios del departamento y añade otros nuevos, sobre todo de técnicas de recuento. Las secciones siguen el orden de los apuntes de la unidad (9.1--9.10)."),
      T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Pots comprovar els resultats amb les eines dels apunts interactius de la unitat (calculadora de recompte, arbres d'extraccions, taula de contingència, arbre de dues etapes i calculadora de dos esdeveniments).",
        r"Intenta resolver cada ejercicio antes de mirar su solución. Puedes comprobar los resultados con las herramientas de los apuntes interactivos de la unidad (calculadora de recuento, árboles de extracciones, tabla de contingencia, árbol de dos etapas y calculadora de dos sucesos)."),
      PRE, lang='es' if ES else 'va')
