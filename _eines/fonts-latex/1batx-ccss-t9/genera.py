# Genera t9-fitxa-exercicis.tex i t9-fitxa-solucions.tex (1r Batxillerat CCSS, Unitat 9: Combinatòria i probabilitat)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Bilingüe: T(valencià, castellà); genera-es.py l'executa amb FM_LANG=es i escriu els -es.tex.
# Les 7 seccions segueixen els blocs dels apunts (materials/1batx-ccss/t9-combinatoria-probabilitat.html): tècniques de recompte
# (9.1), variacions i permutacions (9.2-9.3), combinacions i nombres combinatoris (9.4), successos i regla de Laplace (9.5-9.8),
# propietats i probabilitat condicionada (9.9-9.11), experiències compostes dependents i independents (9.12-9.13) i
# probabilitat total i Bayes (9.14). Les eines de dibuix (arbres, taules) vénen de la fitxa de la unitat 9 de 4t ESO B
# (_eines/fonts-latex/4eso-b-t9) i la capçalera i el preàmbul, de la unitat 8 de 1r Batx CCSS.
# Cada resultat de les solucions es comprova amb ck(): recomptes amb math.comb/math.perm o enumerant els casos (itertools)
# i probabilitats amb fraccions exactes (Fraction).
# Ús: python3 genera.py && python3 genera-es.py, i pdflatex (dues vegades) dels quatre .tex
import os, re, math
from fractions import Fraction as Fr
from itertools import product, permutations, combinations
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return (es if ES else va).replace("\\'", "'")
C = math.comb
def V(n, k): return math.perm(n, k)
f_ = math.factorial
NCHK = [0]
def ck(x, y):
    assert x == y, (x, y); NCHK[0] += 1

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def items(*xs): return r'\begin{enumerate}[label=\alph*),leftmargin=*,itemsep=2pt,topsep=2pt]' + ''.join(r'\item ' + t for t in xs) + r'\end{enumerate}'
def recorda(t): return '\\recorda{%s}' % t
def fixm(t):
    """dins de les fórmules (i fora dels dibuixos), espai fi després de les comes de conjunts i parelles: {2,4} -> {2,\\,4}"""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    def m(mm): return re.sub(r'(?<!\\),(?=[-\d+a-zA-Z(\[]|\\(?![,; ]))', r',\\,', mm.group(0))
    for i in range(0, len(parts), 2): parts[i] = re.sub(r'\$[^$]*\$', m, parts[i])
    return ''.join(parts)
def E(st, q, s): return (st, fixm(q), fixm(s))

# ---------- fraccions i decimals ----------
def fr(f):
    f = Fr(f)
    if f.denominator == 1: return str(f.numerator)
    return ('-' if f < 0 else '') + r'\frac{%d}{%d}' % (abs(f.numerator), f.denominator)
def dc(x, k=4):
    """decimal amb coma per a dins de les fórmules: 0{,}25"""
    s = ('%.*f' % (k, float(x))).rstrip('0').rstrip('.')
    return s.replace('.', '{,}')
def big(n): return '{:,}'.format(n).replace(',', r'\,') if n >= 10000 else str(n)

# ---------- figures (TikZ) ----------
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
def two_stage(first, second, ld=22, sd=(26, 12), fmt=fr):
    """arbre de dues etapes: first = [(nom, p)], second = {nom: [(nom2, p2)]}; mostra el producte de cada camí"""
    kids = []
    for a, pa in first:
        ch = [(b, fmt(pb), [], r'$%s$' % fmt(Fr(pa) * Fr(pb))) for b, pb in second[a]]
        kids.append((a, fmt(pa), ch))
    return tree(kids, ld=ld, sd=sd)
def ctab(head, rows):
    return (r'{\small\renewcommand{\arraystretch}{1.2}\begin{tabular}{l|' + 'c' * (len(head) - 1) + r'}' + '\n\\rowcolor{soft} ' + ' & '.join(head) + r'\\\hline' + '\n'
            + '\n'.join(' & '.join(str(c) for c in r) + r'\\' for r in rows) + '\n\\end{tabular}}')
def cen(*xs, sep=r'\qquad '): return r'\par\smallskip\begin{center}' + sep.join(xs) + r'\end{center}'

S_ = []
def sec(title): S_.append((title, [])); return S_[-1][1]
D6 = range(1, 7)
DD = list(product(D6, D6))
def lap(E_, f): return Fr(sum(1 for e in E_ if f(e)), len(E_))

# =====================================================================
# 1. Tècniques de recompte
X = sec(T("Tècniques de recompte. Principi de multiplicació i factorial", "Técnicas de recuento. Principio de multiplicación y factorial"))
ck(4 * 5 * 3, 60)
X.append(E(1, T("Un restaurant ofereix 4 primers plats, 5 segons i 3 postres. Quants menús diferents (un plat de cada) es poden triar? Quants, si una persona no vol peix i hi ha 2 segons de peix?",
                "Un restaurante ofrece 4 primeros platos, 5 segundos y 3 postres. ¿Cuántos menús distintos (un plato de cada) se pueden elegir? ¿Cuántos, si una persona no quiere pescado y hay 2 segundos de pescado?"),
    r'$4\cdot5\cdot3=\res{60}$; \ ' + T('sense peix', 'sin pescado') + r': $4\cdot3\cdot3=\res{36}$.'))
ck(4 * 3 * 3, 36)
ck(26 ** 3 * 10 ** 3, 17576000); ck(26 * 25 * 24 * 10 * 9 * 8, 11232000)
X.append(E(1, T("Una contrasenya està formada per 3 lletres (d'un alfabet de 26) seguides de 3 xifres. Quantes contrasenyes hi ha? Quantes no repeteixen cap lletra ni cap xifra?",
                "Una contraseña está formada por 3 letras (de un alfabeto de 26) seguidas de 3 cifras. ¿Cuántas contraseñas hay? ¿Cuántas no repiten ninguna letra ni ninguna cifra?"),
    r'$26^3\cdot10^3=\res{17\,576\,000}$; \ $26\cdot25\cdot24\cdot10\cdot9\cdot8=\res{11\,232\,000}$.'))
N4 = range(1000, 10000)
ck(len(N4), 9000); ck(sum(1 for n in N4 if n % 2 == 0), 4500); ck(sum(1 for n in N4 if len(set(str(n))) == 4), 4536); ck(sum(1 for n in N4 if str(n) == str(n)[::-1]), 90)
X.append(E(2, T("Quants nombres de quatre xifres (del 1000 al 9999) hi ha que", "¿Cuántos números de cuatro cifras (del 1000 al 9999) hay que") + items(
    T('siguen parells?', 'sean pares?'), T('tinguen les quatre xifres diferents?', 'tengan las cuatro cifras distintas?'), T('siguen capicues (com 3443)?', 'sean capicúas (como 3443)?'))
    + recorda(T("comença per la xifra que té condicions; la primera xifra no pot ser 0.", "empieza por la cifra que tiene condiciones; la primera cifra no puede ser 0.")),
    items(T(r'Primera: 9 opcions; segona i tercera: 10; última (parella): 5. $9\cdot10\cdot10\cdot5=\res{4\,500}$', r'Primera: 9 opciones; segunda y tercera: 10; última (par): 5. $9\cdot10\cdot10\cdot5=\res{4\,500}$'),
          T(r'$9\cdot9\cdot8\cdot7=\res{4\,536}$ (la segona ja pot ser 0)', r'$9\cdot9\cdot8\cdot7=\res{4\,536}$ (la segunda ya puede ser 0)'),
          T(r'Les dues últimes xifres queden determinades per les dues primeres: $9\cdot10=\res{90}$', r'Las dos últimas cifras quedan determinadas por las dos primeras: $9\cdot10=\res{90}$'))))
ck(f_(6), 720); ck(f_(9) // f_(7), 72); ck(Fr(f_(10), f_(7) * f_(3)), 120)
ck([n for n in range(2, 30) if f_(n) // f_(n - 2) == 30], [6])
X.append(E(1, T('Calcula i simplifica:', 'Calcula y simplifica:') + tasks(4, [r'$6!$', r'$\dfrac{9!}{7!}$', r'$\dfrac{10!}{7!\,3!}$', r'$\dfrac{(n+1)!}{(n-1)!}$'])
    + T(r'Resol l\'equació $\dfrac{n!}{(n-2)!}=30$.', r'Resuelve la ecuación $\dfrac{n!}{(n-2)!}=30$.'),
    tasks(4, [r'$\res{720}$', r'$9\cdot8=\res{72}$', r'$\dfrac{10\cdot9\cdot8}{6}=\res{120}$', r'$\res{(n+1)\,n}$'])
    + r'$n(n-1)=30\Rightarrow n^2-n-30=0\Rightarrow n=\res{6}$ ' + T('(la solució $n=-5$ no té sentit).', '(la solución $n=-5$ no tiene sentido).')))
ck(sum(1 for k in (1, 2, 3) for t in product('123', repeat=k)), 39)
X.append(E(2, T("Quants nombres (de l'1 al 999) es poden escriure fent servir només les xifres 1, 2 i 3 (que es poden repetir)?", "¿Cuántos números (del 1 al 999) se pueden escribir usando solo las cifras 1, 2 y 3 (que se pueden repetir)?")
    + recorda(T("si els casos se separen en grups sense elements comuns, se sumen els recomptes de cada grup (principi de la suma).", "si los casos se separan en grupos sin elementos comunes, se suman los recuentos de cada grupo (principio de la suma).")),
    T(r'D\'una xifra: 3; de dues: $3^2=9$; de tres: $3^3=27$. En total, $3+9+27=\res{39}$.', r'De una cifra: 3; de dos: $3^2=9$; de tres: $3^3=27$. En total, $3+9+27=\res{39}$.')))
ck(sum(1 for t in product(D6, repeat=4) if 6 in t), 671)
X.append(E(2, T("Llancem quatre daus (de colors diferents). Quants resultats hi ha? En quants n'apareix almenys un 6?", "Lanzamos cuatro dados (de colores distintos). ¿Cuántos resultados hay? ¿En cuántos aparece al menos un 6?"),
    r'$6^4=\res{1\,296}$. \ ' + T('Pel contrari, sense cap 6 n\'hi ha $5^4=625$: ', 'Por el contrario, sin ningún 6 hay $5^4=625$: ') + r'$1\,296-625=\res{671}$.'))

# =====================================================================
# 2. Variacions i permutacions
X = sec(T("Variacions i permutacions", "Variaciones y permutaciones"))
ck(V(8, 3), 336); ck(5 ** 3, 125); ck(f_(5), 120); ck(f_(6) // 8, 90); ck(f_(4), 24)
ck(len(set(permutations('AABBCC'))), 90)
X.append(E(1, T('Calcula:', 'Calcula:') + tasks(5, [r'$V_{8,3}$', r'$VR_{5,3}$', r'$P_5$', r'$PR_6^{\,2,2,2}$', r'$PC_5$']),
    tasks(5, [r'$8\cdot7\cdot6=\res{336}$', r'$5^3=\res{125}$', r'$5!=\res{120}$', r'$\frac{6!}{2!\,2!\,2!}=\res{90}$', r'$4!=\res{24}$'])))
ck(V(20, 3), 6840)
X.append(E(1, T("Un club de 20 socis ha de triar president, secretari i tresorer (tres persones diferents). De quantes maneres ho pot fer?", "Un club de 20 socios tiene que elegir presidente, secretario y tesorero (tres personas distintas). ¿De cuántas maneras lo puede hacer?"),
    T(r'Importa l\'ordre (cada càrrec és diferent) i no es repeteix: $V_{20,3}=20\cdot19\cdot18=\res{6\,840}$.', r'Importa el orden (cada cargo es distinto) y no se repite: $V_{20,3}=20\cdot19\cdot18=\res{6\,840}$.')))
ck(V(9, 5), 15120); ck(sum(1 for p in permutations('123456789', 5) if p[0] == '1' and p[-1] == '9'), 210)
ck(sum(1 for p in permutations('123456789', 5) if int(p[-1]) % 2 == 0), 6720)
X.append(E(2, T("Amb les xifres de l'1 al 9, quants nombres de cinc xifres diferents es poden formar? Quants comencen per 1 i acaben en 9? Quants són parells?",
                "Con las cifras del 1 al 9, ¿cuántos números de cinco cifras distintas se pueden formar? ¿Cuántos empiezan por 1 y acaban en 9? ¿Cuántos son pares?"),
    r'$V_{9,5}=9\cdot8\cdot7\cdot6\cdot5=\res{15\,120}$; \ ' + T('fixades la primera i l\'última', 'fijadas la primera y la última') + r': $V_{7,3}=\res{210}$; \ '
    + T('parells: la darrera, de 4 maneres (2, 4, 6, 8), i la resta', 'pares: la última, de 4 maneras (2, 4, 6, 8), y el resto') + r': $4\cdot V_{8,4}=4\cdot1\,680=\res{6\,720}$.'))
ck(2 ** 10, 1024); ck(sum(1 for t in product('CX', repeat=10) if t.count('C') == 4), 210)
X.append(E(2, T("Llancem una moneda 10 vegades i anotem la seqüència de cares i creus. Quantes seqüències hi ha? En quantes ix exactament 4 vegades cara?",
                "Lanzamos una moneda 10 veces y anotamos la secuencia de caras y cruces. ¿Cuántas secuencias hay? ¿En cuántas sale exactamente 4 veces cara?"),
    r'$VR_{2,10}=2^{10}=\res{1\,024}$; \ ' + T('són ordenacions de 4 C i 6 X', 'son ordenaciones de 4 C y 6 X') + r': $PR_{10}^{\,4,6}=\frac{10!}{4!\,6!}=\res{210}$.'))
W1 = T('PATATA', 'PATATA')
ck(len(set(permutations('PATATA'))), 60); ck(len([p for p in set(permutations('PATATA')) if p[0] == 'P']), 10)
ck(len([p for p in set(permutations('PATATA')) if p[0] == 'A' and p[-1] == 'A']), 12)
X.append(E(2, T("Quantes paraules (amb sentit o sense) es poden formar amb totes les lletres de PATATA? Quantes comencen per P? Quantes comencen i acaben per A?",
                "¿Cuántas palabras (con sentido o sin él) se pueden formar con todas las letras de PATATA? ¿Cuántas empiezan por P? ¿Cuántas empiezan y acaban por A?"),
    T(r'Hi ha 3 A, 2 T i 1 P: $PR_6^{\,3,2,1}=\frac{6!}{3!\,2!}=\res{60}$. \ Per P: queden AATTA, $\frac{5!}{3!\,2!}=\res{10}$. \ A--A: queden P, T, T, A al mig, $\frac{4!}{2!}=\res{12}$.',
      r'Hay 3 A, 2 T y 1 P: $PR_6^{\,3,2,1}=\frac{6!}{3!\,2!}=\res{60}$. \ Por P: quedan AATTA, $\frac{5!}{3!\,2!}=\res{10}$. \ A--A: quedan P, T, T, A en medio, $\frac{4!}{2!}=\res{12}$.')))
ck(f_(9), 362880); ck(f_(3) * f_(4) * f_(3) * f_(2), 1728)
X.append(E(2, T("Volem col·locar en un prestatge 4 llibres de matemàtiques, 3 d'història i 2 d'anglés, tots diferents. De quantes maneres es pot fer? I si els de cada matèria han d'estar junts?",
                "Queremos colocar en una estantería 4 libros de matemáticas, 3 de historia y 2 de inglés, todos distintos. ¿De cuántas maneras se puede hacer? ¿Y si los de cada materia tienen que estar juntos?"),
    r'$P_9=9!=\res{362\,880}$; \ ' + T('junts: ordenem els 3 blocs i, dins de cada bloc, els llibres', 'juntos: ordenamos los 3 bloques y, dentro de cada bloque, los libros') + r': $3!\cdot4!\cdot3!\cdot2!=\res{1\,728}$.'))
def circ(n, bad=None):
    """seients circulars: fixem la persona 0 i ordenem les altres; bad = parella que no pot estar junta"""
    c = 0
    for p in permutations(range(1, n)):
        s = (0,) + p
        if bad and any({s[i], s[(i + 1) % n]} == set(bad) for i in range(n)): continue
        c += 1
    return c
ck(circ(7), 720); ck(circ(7, (1, 2)), 480)
X.append(E(3, T("Set amics s'asseuen al voltant d'una taula redona (només importa qui té a cada costat). De quantes maneres ho poden fer? I si dos d'ells, enfadats, no volen seure junts?",
                "Siete amigos se sientan alrededor de una mesa redonda (solo importa quién tiene a cada lado). ¿De cuántas maneras lo pueden hacer? ¿Y si dos de ellos, enfadados, no quieren sentarse juntos?"),
    r'$PC_7=6!=\res{720}$. \ ' + T('Junts (com un sol bloc, que es pot girar): $2\cdot PC_6=2\cdot5!=240$. Separats: $720-240=\res{480}$.', 'Juntos (como un solo bloque, que se puede girar): $2\cdot PC_6=2\cdot5!=240$. Separados: $720-240=\res{480}$.')))
ck(sum(1 for p in permutations(['x1', 'x2', 'x3', 'y1', 'y2', 'y3']) if all(p[i][0] != p[i + 1][0] for i in range(5))), 72)
X.append(E(2, T("Tres xics i tres xiques s'asseuen en una fila de 6 cadires. De quantes maneres poden fer-ho si s'han d'alternar xics i xiques?",
                "Tres chicos y tres chicas se sientan en una fila de 6 sillas. ¿De cuántas maneras pueden hacerlo si se tienen que alternar chicos y chicas?"),
    T(r'La fila pot començar per xic o per xica (2 maneres); després, els xics s\'ordenen de $3!$ maneres i les xiques de $3!$: $2\cdot3!\cdot3!=\res{72}$.',
      r'La fila puede empezar por chico o por chica (2 maneras); después, los chicos se ordenan de $3!$ maneras y las chicas de $3!$: $2\cdot3!\cdot3!=\res{72}$.')))

# =====================================================================
# 3. Combinacions i nombres combinatoris
X = sec(T("Combinacions i nombres combinatoris", "Combinaciones y números combinatorios"))
ck(C(9, 4), 126); ck(C(12, 10), 66); ck(C(20, 18), 190); ck(C(7, 0), 1)
X.append(E(1, T('Calcula (fes servir la propietat dels nombres complementaris quan convinga):', 'Calcula (usa la propiedad de los números complementarios cuando convenga):') + tasks(4, [r'$\dbinom94$', r'$\dbinom{12}{10}$', r'$\dbinom{20}{18}$', r'$\dbinom70$']),
    tasks(4, [r'$\frac{9\cdot8\cdot7\cdot6}{4!}=\res{126}$', r'$\binom{12}{2}=\res{66}$', r'$\binom{20}{2}=\res{190}$', r'$\res{1}$'])))
ck([n for n in range(2, 40) if C(n, 2) == 28], [8]); ck([x for x in range(0, 20) if C(x, 3) == C(x, 5) and x >= 5], [8])
ck([x for x in range(0, 9) if C(10, x) == C(10, x + 2)], [4])
X.append(E(2, T('Resol les equacions:', 'Resuelve las ecuaciones:') + tasks(3, [r'$\dbinom n2=28$', r'$\dbinom x3=\dbinom x5$', r'$\dbinom{10}{x}=\dbinom{10}{x+2}$'])
    + recorda(T(r'si $\binom na=\binom nb$ amb $a\neq b$, aleshores $a+b=n$ (nombres complementaris).', r'si $\binom na=\binom nb$ con $a\neq b$, entonces $a+b=n$ (números complementarios).')),
    tasks(1, [r'$\frac{n(n-1)}{2}=28\Rightarrow n^2-n-56=0\Rightarrow n=\res{8}$', r'$3+5=x\Rightarrow x=\res{8}$', r'$x+(x+2)=10\Rightarrow x=\res{4}$'])))
ck(C(9, 4) + C(9, 5), C(10, 5)); ck(C(10, 5), 252); ck(sum(C(6, k) for k in range(7)), 64); ck(C(7, 3) + C(7, 4) + C(8, 5), C(9, 5))
X.append(E(2, T("Fes servir les propietats dels nombres combinatoris per a calcular:", "Usa las propiedades de los números combinatorios para calcular:") + tasks(3, [r'$\dbinom94+\dbinom95$', r'$\dbinom60+\dbinom61+\dots+\dbinom66$', r'$\dbinom73+\dbinom74+\dbinom85$']),
    tasks(3, [r'$\binom{10}{5}=\res{252}$', r'$2^6=\res{64}$', r'$\binom84+\binom85=\binom95=\res{126}$'])))
X.append(E(2, T("Desenvolupa amb el binomi de Newton:", "Desarrolla con el binomio de Newton:") + tasks(2, [r'$(x+2)^4$', r'$(2x-1)^4$']),
    tasks(1, [r'$x^4+4\cdot x^3\cdot2+6\cdot x^2\cdot4+4\cdot x\cdot8+16=\res{x^4+8x^3+24x^2+32x+16}$',
              r'$(2x)^4-4(2x)^3+6(2x)^2-4(2x)+1=\res{16x^4-32x^3+24x^2-8x+1}$'])))
import sympy as _sp
_x = _sp.symbols('x')
ck(_sp.expand((_x + 2) ** 4), _sp.expand(_x ** 4 + 8 * _x ** 3 + 24 * _x ** 2 + 32 * _x + 16)); ck(_sp.expand((2 * _x - 1) ** 4), _sp.expand(16 * _x ** 4 - 32 * _x ** 3 + 24 * _x ** 2 - 8 * _x + 1))
G = ['D%d' % i for i in range(7)] + ['H%d' % i for i in range(5)]
cm = list(combinations(G, 4))
ck(len(cm), 495); ck(sum(1 for c in cm if sum(x[0] == 'D' for x in c) == 2), 210); ck(sum(1 for c in cm if any(x[0] == 'D' for x in c)), 490)
X.append(E(2, T("En un grup hi ha 7 dones i 5 homes. Cal formar una comissió de 4 persones. De quantes maneres es pot fer", "En un grupo hay 7 mujeres y 5 hombres. Hay que formar una comisión de 4 personas. ¿De cuántas maneras se puede hacer") + items(
    T('sense cap condició?', 'sin ninguna condición?'), T('si ha de tindre 2 dones i 2 homes?', 'si tiene que tener 2 mujeres y 2 hombres?'), T('si hi ha d\'haver almenys una dona?', 'si tiene que haber al menos una mujer?')),
    items(r'$\binom{12}{4}=\res{495}$', r'$\binom72\cdot\binom52=21\cdot10=\res{210}$', T(r'Pel contrari (cap dona): $495-\binom54=495-5=\res{490}$', r'Por el contrario (ninguna mujer): $495-\binom54=495-5=\res{490}$'))))
ck(C(10, 7), 120); ck(C(7, 4), 35)
X.append(E(1, T("En un examen de 10 preguntes cal respondre'n 7. Quantes tries diferents hi ha? I si les tres primeres són obligatòries?", "En un examen de 10 preguntas hay que responder 7. ¿Cuántas elecciones distintas hay? ¿Y si las tres primeras son obligatorias?"),
    r'$\binom{10}{7}=\binom{10}{3}=\res{120}$; \ ' + T('cal triar-ne 4 de les 7 restants', 'hay que elegir 4 de las 7 restantes') + r': $\binom74=\res{35}$.'))
ck(C(8, 2) - 8, 20); ck(C(8, 3), 56)
X.append(E(2, T("Quantes diagonals té un octàgon convex? Quants triangles es poden dibuixar amb vèrtexs en els vèrtexs de l'octàgon?", "¿Cuántas diagonales tiene un octógono convexo? ¿Cuántos triángulos se pueden dibujar con vértices en los vértices del octógono?"),
    T(r'Segments entre dos vèrtexs: $\binom82=28$; en traiem els 8 costats: $\res{20}$ diagonals. \ Triangles: $\binom83=\res{56}$.', r'Segmentos entre dos vértices: $\binom82=28$; quitamos los 8 lados: $\res{20}$ diagonales. \ Triángulos: $\binom83=\res{56}$.')))
ck(C(49, 6), 13983816); ck(C(50, 5) * C(12, 2), 139838160)
X.append(E(2, T("A la Primitiva es marquen 6 nombres de l'1 al 49. A l'Euromilions es marquen 5 nombres de l'1 al 50 i 2 «estreles» de l'1 al 12. Quantes apostes diferents hi ha en cada joc?",
                "En la Primitiva se marcan 6 números del 1 al 49. En el Euromillones se marcan 5 números del 1 al 50 y 2 «estrellas» del 1 al 12. ¿Cuántas apuestas distintas hay en cada juego?"),
    T('Primitiva', 'Primitiva') + r': $\binom{49}{6}=\res{13\,983\,816}$. \ ' + T('Euromilions', 'Euromillones') + r': $\binom{50}{5}\cdot\binom{12}{2}=2\,118\,760\cdot66=\res{139\,838\,160}$.'))
ck(f_(5), 120); ck(C(10, 3), 120); ck(10 ** 4, 10000); ck(V(10, 3), 720); ck(len(set(permutations('RIURE'))), 60)
X.append(E(2, T("Digues de quin tipus és cada recompte i calcula'l:", "Di de qué tipo es cada recuento y calcúlalo:") + items(
    T('maneres de seure 5 persones en 5 cadires en fila;', 'maneras de sentarse 5 personas en 5 sillas en fila;'),
    T('maneres de triar 3 gustos diferents (de 10) per a una copa de gelat;', 'maneras de elegir 3 sabores distintos (de 10) para una copa de helado;'),
    T('codis de 4 xifres per a un cadenat;', 'códigos de 4 cifras para un candado;'),
    T('maneres de repartir 3 premis diferents entre 10 participants (cadascun en guanya com a molt un);', 'maneras de repartir 3 premios distintos entre 10 participantes (cada uno gana como mucho uno);'),
    T('paraules que es poden formar amb totes les lletres de RIURE.', 'palabras que se pueden formar con todas las letras de RISAS.')),
    items(T(r'Permutacions: $P_5=\res{120}$', r'Permutaciones: $P_5=\res{120}$'), T(r'Combinacions: $\binom{10}{3}=\res{120}$', r'Combinaciones: $\binom{10}{3}=\res{120}$'),
          T(r'Variacions amb repetició: $VR_{10,4}=10^4=\res{10\,000}$', r'Variaciones con repetición: $VR_{10,4}=10^4=\res{10\,000}$'),
          T(r'Variacions: $V_{10,3}=\res{720}$', r'Variaciones: $V_{10,3}=\res{720}$'),
          T(r'Permutacions amb repetició (dues R): $\frac{5!}{2!}=\res{60}$', r'Permutaciones con repetición (dos S): $\frac{5!}{2!}=\res{60}$'))))
ck(len(set(permutations('RISAS'))), 60)

# =====================================================================
# 4. Successos. Probabilitat i regla de Laplace
X = sec(T("Successos. Probabilitat i regla de Laplace", "Sucesos. Probabilidad y regla de Laplace"))
M3 = [''.join(t) for t in product('CX', repeat=3)]
A3 = {e for e in M3 if e.count('C') >= 2}; B3 = {e for e in M3 if e[0] == 'X'}
ck(sorted(A3), ['CCC', 'CCX', 'CXC', 'XCC']); ck(sorted(A3 & B3), ['XCC']); ck(len(A3 | B3), 7)
ck(Fr(len(A3 & B3), 8), Fr(1, 8)); ck(Fr(len(A3 | B3), 8), Fr(7, 8)); ck(Fr(8 - len(A3), 8), Fr(1, 2)); ck(Fr(len(B3 - A3), 8), Fr(3, 8))
X.append(E(1, T("Llancem tres monedes. Escriu l'espai mostral i els successos $A=$ «almenys dues cares» i $B=$ «la primera moneda és creu». Escriu i calcula la probabilitat de $A\\cap B$, $A\\cup B$, $\\overline A$ i $B\\cap\\overline A$.",
                "Lanzamos tres monedas. Escribe el espacio muestral y los sucesos $A=$ «al menos dos caras» y $B=$ «la primera moneda es cruz». Escribe y calcula la probabilidad de $A\\cap B$, $A\\cup B$, $\\overline A$ y $B\\cap\\overline A$."),
    r'$E=\{CCC,CCX,CXC,CXX,XCC,XCX,XXC,XXX\}$ ' + T('(8 resultats equiprobables)', '(8 resultados equiprobables)') + r'; \ $A=\{CCC,CCX,CXC,XCC\}$, \ $B=\{XCC,XCX,XXC,XXX\}$.\par'
    + r'$A\cap B=\{XCC\}$, $P=\res{\frac18}$; \ $P(A\cup B)=\frac48+\frac48-\frac18=\res{\frac78}$; \ $P(\overline A)=\res{\frac12}$; \ $B\cap\overline A=\{XCX,XXC,XXX\}$, $P=\res{\frac38}$.'))
p1 = lap(DD, lambda e: sum(e) == 8); p2 = lap(DD, lambda e: sum(e) >= 10); p3 = lap(DD, lambda e: (e[0] * e[1]) % 3 == 0); p4 = lap(DD, lambda e: abs(e[0] - e[1]) <= 1)
ck(p1, Fr(5, 36)); ck(p2, Fr(1, 6)); ck(p3, Fr(5, 9)); ck(p4, Fr(4, 9))
X.append(E(1, T("Llancem dos daus. Calcula la probabilitat que", "Lanzamos dos dados. Calcula la probabilidad de que") + tasks(2, [T('la suma siga 8;', 'la suma sea 8;'), T('la suma siga 10 o més;', 'la suma sea 10 o más;'), T('el producte siga múltiple de 3;', 'el producto sea múltiplo de 3;'), T('la diferència entre els dos siga com a molt 1.', 'la diferencia entre los dos sea como mucho 1.')]),
    T('Hi ha 36 parelles equiprobables.', 'Hay 36 parejas equiprobables.') + tasks(1, [r'$\frac{5}{36}$: (2,6), (3,5), (4,4), (5,3), (6,2). \ $\res{\frac5{36}}$', r'$\frac{3+2+1}{36}=\res{\frac16}$',
    T(r'Pel contrari: cap dau és 3 ni 6, $\frac{4\cdot4}{36}$; \ $1-\frac{16}{36}=\res{\frac59}$', r'Por el contrario: ningún dado es 3 ni 6, $\frac{4\cdot4}{36}$; \ $1-\frac{16}{36}=\res{\frac59}$'),
    T(r'Diferència 0: 6; diferència 1: 10. \ $\frac{16}{36}=\res{\frac49}$', r'Diferencia 0: 6; diferencia 1: 10. \ $\frac{16}{36}=\res{\frac49}$')])))
BAR = [(s, v) for s in 'OCEB' for v in range(1, 11)]   # 8, 9, 10 = sota, cavall, rei
fig = lambda c: c[1] >= 8
ck(lap(BAR, lambda c: c[0] == 'O'), Fr(1, 4)); ck(lap(BAR, fig), Fr(3, 10)); ck(lap(BAR, lambda c: c[0] == 'O' or fig(c)), Fr(19, 40)); ck(lap(BAR, lambda c: not (c[1] == 1 or c[0] == 'C')), Fr(27, 40))
X.append(E(1, T("Traiem una carta d'una baralla espanyola de 40 cartes (4 pals: ors, copes, espases i bastos; en cada pal, de l'1 al 7, sota, cavall i rei). Calcula la probabilitat de traure", "Sacamos una carta de una baraja española de 40 cartas (4 palos: oros, copas, espadas y bastos; en cada palo, del 1 al 7, sota, caballo y rey). Calcula la probabilidad de sacar")
    + tasks(4, [T('un or;', 'un oro;'), T('una figura;', 'una figura;'), T('un or o una figura;', 'un oro o una figura;'), T('ni un as ni una copa.', 'ni un as ni una copa.')]),
    tasks(4, [r'$\frac{10}{40}=\res{\frac14}$', r'$\frac{12}{40}=\res{\frac3{10}}$', r'$\frac{10+12-3}{40}=\res{\frac{19}{40}}$', r'$1-\frac{4+10-1}{40}=\res{\frac{27}{40}}$'])))
U = ['B'] * 6 + ['N'] * 4
cU = list(combinations(range(10), 3)); col = lambda c: [U[i] for i in c]
ck(len(cU), 120); ck(Fr(sum(1 for c in cU if col(c).count('B') == 3), 120), Fr(1, 6)); ck(Fr(sum(1 for c in cU if col(c).count('B') == 2), 120), Fr(1, 2)); ck(Fr(sum(1 for c in cU if 'N' in col(c)), 120), Fr(5, 6))
X.append(E(2, T("Una urna té 6 boles blanques i 4 de negres. Traiem 3 boles alhora. Fes servir la combinatòria per a calcular la probabilitat que", "Una urna tiene 6 bolas blancas y 4 negras. Sacamos 3 bolas a la vez. Usa la combinatoria para calcular la probabilidad de que")
    + items(*[T('les tres siguen blanques;', 'las tres sean blancas;'), T('n\'hi haja exactament dues de blanques;', 'haya exactamente dos blancas;'), T('n\'hi haja almenys una de negra.', 'haya al menos una negra.')]),
    T('Casos possibles: ', 'Casos posibles: ') + r'$\binom{10}{3}=120$.' + tasks(3, [r'$\frac{\binom63}{120}=\frac{20}{120}=\res{\frac16}$', r'$\frac{\binom62\binom41}{120}=\frac{60}{120}=\res{\frac12}$', r'$1-\frac16=\res{\frac56}$'])))
perm5 = list(permutations('ABCDE'))
ck(Fr(sum(1 for p in perm5 if abs(p.index('A') - p.index('B')) == 1), 120), Fr(2, 5)); ck(Fr(sum(1 for p in perm5 if p.index('A') < p.index('B')), 120), Fr(1, 2))
X.append(E(2, T("Col·loquem a l'atzar cinc llibres, A, B, C, D i E, en un prestatge. Quina és la probabilitat que A i B queden junts? I que A quede a l'esquerra de B (no necessàriament al costat)?",
                "Colocamos al azar cinco libros, A, B, C, D y E, en una estantería. ¿Cuál es la probabilidad de que A y B queden juntos? ¿Y de que A quede a la izquierda de B (no necesariamente al lado)?"),
    T(r'Casos possibles: $5!=120$. Junts: $2\cdot4!=48$, $P=\frac{48}{120}=\res{\frac25}$. \ Per simetria, en la meitat de les ordenacions A va abans que B: $\res{\frac12}$.',
      r'Casos posibles: $5!=120$. Juntos: $2\cdot4!=48$, $P=\frac{48}{120}=\res{\frac25}$. \ Por simetría, en la mitad de las ordenaciones A va antes que B: $\res{\frac12}$.')))
ck(C(6, 5) * C(43, 1), 258)
X.append(E(3, T("En la Primitiva (6 nombres de 49), quina és la probabilitat d'encertar els 6 nombres amb una aposta? I d'encertar-ne exactament 5?", "En la Primitiva (6 números de 49), ¿cuál es la probabilidad de acertar los 6 números con una apuesta? ¿Y de acertar exactamente 5?"),
    r'$P(6)=\dfrac1{\binom{49}6}=\res{\dfrac1{13\,983\,816}}\approx7{,}15\cdot10^{-8}$. \ ' + T('Exactament 5: 5 dels 6 guanyadors i 1 dels 43 restants', 'Exactamente 5: 5 de los 6 ganadores y 1 de los 43 restantes') + r': $\dfrac{\binom65\binom{43}1}{\binom{49}6}=\dfrac{258}{13\,983\,816}\approx\res{1{,}85\cdot10^{-5}}$.'))
ck(Fr(V(10, 4), 10 ** 4), Fr(63, 125)); ck(Fr(sum(1 for t in product(range(10), repeat=4) if t == t[::-1]), 10 ** 4), Fr(1, 100))
X.append(E(2, T("Es tria a l'atzar un codi de 4 xifres (del 0000 al 9999). Probabilitat que totes les xifres siguen diferents, i que siga capicua.", "Se elige al azar un código de 4 cifras (del 0000 al 9999). Probabilidad de que todas las cifras sean distintas, y de que sea capicúa."),
    r'$\dfrac{V_{10,4}}{VR_{10,4}}=\dfrac{5\,040}{10\,000}=\res{0{,}504}$; \ ' + T('capicua', 'capicúa') + r': $\dfrac{10^2}{10^4}=\res{0{,}01}$.'))
ck(1 - Fr(C(12, 3), C(20, 3)), Fr(46, 57))
X.append(E(2, T("En una classe hi ha 12 xiques i 8 xics. Es trien 3 persones a l'atzar. Probabilitat que hi haja almenys un xic.", "En una clase hay 12 chicas y 8 chicos. Se eligen 3 personas al azar. Probabilidad de que haya al menos un chico."),
    r'$1-\dfrac{\binom{12}3}{\binom{20}3}=1-\dfrac{220}{1\,140}=\res{\dfrac{46}{57}}\approx0{,}807$'))

# =====================================================================
# 5. Propietats de la probabilitat. Probabilitat condicionada
X = sec(T("Propietats de la probabilitat. Probabilitat condicionada", "Propiedades de la probabilidad. Probabilidad condicionada"))
pA, pB, pAB = Fr(1, 2), Fr(2, 5), Fr(1, 5)
ck(pA + pB - pAB, Fr(7, 10)); ck(1 - (pA + pB - pAB), Fr(3, 10)); ck(pA - pAB, Fr(3, 10)); ck(1 - pAB, Fr(4, 5)); ck(pAB / pB, Fr(1, 2)); ck(pAB / pA, Fr(2, 5))
X.append(E(1, T(r'Siguen $A$ i $B$ dos successos amb $P(A)=0{,}5$, $P(B)=0{,}4$ i $P(A\cap B)=0{,}2$. Calcula:', r'Sean $A$ y $B$ dos sucesos con $P(A)=0{,}5$, $P(B)=0{,}4$ y $P(A\cap B)=0{,}2$. Calcula:')
    + tasks(3, [r'$P(A\cup B)$', r'$P(\overline A\cap\overline B)$', r'$P(A\cap\overline B)$', r'$P(\overline A\cup\overline B)$', r'$P(A\,|\,B)$', r'$P(B\,|\,A)$'])
    + recorda(T(r'lleis de De Morgan: $\overline A\cap\overline B=\overline{A\cup B}$ i $\overline A\cup\overline B=\overline{A\cap B}$.', r'leyes de De Morgan: $\overline A\cap\overline B=\overline{A\cup B}$ y $\overline A\cup\overline B=\overline{A\cap B}$.')),
    tasks(3, [r'$0{,}5+0{,}4-0{,}2=\res{0{,}7}$', r'$1-P(A\cup B)=\res{0{,}3}$', r'$0{,}5-0{,}2=\res{0{,}3}$', r'$1-P(A\cap B)=\res{0{,}8}$', r'$\frac{0{,}2}{0{,}4}=\res{0{,}5}$', r'$\frac{0{,}2}{0{,}5}=\res{0{,}4}$'])))
pA, pB, pU = Fr(3, 5), Fr(3, 10), Fr(7, 10); pI = pA + pB - pU
ck(pI, Fr(1, 5)); ck(pI / pB, Fr(2, 3)); ck((pB - pI) / (1 - pA), Fr(1, 4))
X.append(E(2, T(r'Sabem que $P(A)=0{,}6$, $P(B)=0{,}3$ i $P(A\cup B)=0{,}7$. Calcula $P(A\cap B)$, $P(A\,|\,B)$ i $P(B\,|\,\overline A)$.', r'Sabemos que $P(A)=0{,}6$, $P(B)=0{,}3$ y $P(A\cup B)=0{,}7$. Calcula $P(A\cap B)$, $P(A\,|\,B)$ y $P(B\,|\,\overline A)$.'),
    r'$P(A\cap B)=0{,}6+0{,}3-0{,}7=\res{0{,}2}$; \ $P(A\,|\,B)=\frac{0{,}2}{0{,}3}=\res{\frac23}$; \ $P(B\,|\,\overline A)=\dfrac{P(B)-P(A\cap B)}{1-P(A)}=\frac{0{,}1}{0{,}4}=\res{0{,}25}$.'))
X.append(E(1, T(r'$A$ i $B$ són incompatibles, amb $P(A)=0{,}35$ i $P(B)=0{,}45$. Calcula $P(A\cup B)$, $P(\overline A\cap\overline B)$ i $P(A\,|\,B)$.', r'$A$ y $B$ son incompatibles, con $P(A)=0{,}35$ y $P(B)=0{,}45$. Calcula $P(A\cup B)$, $P(\overline A\cap\overline B)$ y $P(A\,|\,B)$.'),
    r'$P(A\cup B)=0{,}35+0{,}45=\res{0{,}8}$; \ $P(\overline A\cap\overline B)=1-0{,}8=\res{0{,}2}$; \ $P(A\,|\,B)=\frac{0}{0{,}45}=\res{0}$ ' + T('(si passa $B$, $A$ no pot passar).', '(si ocurre $B$, $A$ no puede ocurrir).')))
DF, DN, HF, HN = 30, 90, 25, 55
NT = DF + DN + HF + HN
ck(NT, 200); ck(Fr(DF + HF, NT), Fr(11, 40)); ck(Fr(DF, NT), Fr(3, 20)); ck(Fr(DF, DF + DN), Fr(1, 4)); ck(Fr(DF, DF + HF), Fr(6, 11)); ck(Fr(HF + HN + DF, NT), Fr(11, 20))
TAB = ctab(['', T('Fuma ($F$)', 'Fuma ($F$)'), T('No fuma ($\\overline F$)', 'No fuma ($\\overline F$)'), 'Total'],
           [[T('Dona ($D$)', 'Mujer ($D$)'), DF, DN, DF + DN], [T('Home ($H$)', 'Hombre ($H$)'), HF, HN, HF + HN], ['Total', DF + HF, DN + HN, NT]])
X.append(E(2, T("En un grup de 200 persones hi ha 120 dones. Fumen 30 dones i 25 homes. Fes la taula de contingència i calcula la probabilitat que una persona triada a l'atzar", "En un grupo de 200 personas hay 120 mujeres. Fuman 30 mujeres y 25 hombres. Haz la tabla de contingencia y calcula la probabilidad de que una persona elegida al azar")
    + tasks(2, [T('fume;', 'fume;'), T('siga dona i fume;', 'sea mujer y fume;'), T('fume, sabent que és dona;', 'fume, sabiendo que es mujer;'), T('siga dona, sabent que fuma;', 'sea mujer, sabiendo que fuma;'), T('siga home o fume.', 'sea hombre o fume.')]),
    cen(TAB) + tasks(3, [r'$\frac{55}{200}=\res{\frac{11}{40}}$', r'$\frac{30}{200}=\res{\frac3{20}}$', r'$\frac{30}{120}=\res{\frac14}$', r'$\frac{30}{55}=\res{\frac6{11}}$', r'$\frac{80+30}{200}=\res{\frac{11}{20}}$'])))
pM, pA_, pMA = Fr(60, 100), Fr(50, 100), Fr(35, 100)
ck(pM + pA_ - pMA, Fr(3, 4)); ck(1 - (pM + pA_ - pMA), Fr(1, 4)); ck(pM + pA_ - 2 * pMA, Fr(2, 5)); ck(pMA / pM, Fr(7, 12)); ck((pM - pMA) / (1 - pA_), Fr(1, 2))
X.append(E(2, T(r"En un institut, el 60 \% de l'alumnat aprova Matemàtiques, el 50 \% aprova Anglés i el 35 \% aprova les dues. Triem un alumne a l'atzar. Calcula la probabilitat que", r"En un instituto, el 60 \% del alumnado aprueba Matemáticas, el 50 \% aprueba Inglés y el 35 \% aprueba las dos. Elegimos un alumno al azar. Calcula la probabilidad de que")
    + tasks(2, [T('aprove almenys una de les dues;', 'apruebe al menos una de las dos;'), T('no aprove cap;', 'no apruebe ninguna;'), T('aprove només una;', 'apruebe solo una;'), T('aprove Anglés, si ha aprovat Matemàtiques;', 'apruebe Inglés, si ha aprobado Matemáticas;'), T('aprove Matemàtiques, si ha suspés Anglés.', 'apruebe Matemáticas, si ha suspendido Inglés.')]),
    tasks(2, [r'$0{,}6+0{,}5-0{,}35=\res{0{,}75}$', r'$1-0{,}75=\res{0{,}25}$', r'$0{,}75-0{,}35=\res{0{,}4}$', r'$P(A\,|\,M)=\frac{0{,}35}{0{,}6}=\res{\frac7{12}}\approx0{,}583$', r'$P(M\,|\,\overline A)=\frac{0{,}6-0{,}35}{0{,}5}=\res{0{,}5}$'])))
ck(30 - (18 + 12 - 6), 6); ck(Fr(6, 18), Fr(1, 3)); ck(Fr(6, 12), Fr(1, 2))
X.append(E(1, T("En una classe de 30 alumnes, 18 juguen a futbol, 12 a bàsquet i 6 a tots dos esports. Triem un alumne a l'atzar. Probabilitat que no jugue a cap dels dos. Si juga a futbol, quina és la probabilitat que també jugue a bàsquet? I a l'inrevés?",
                "En una clase de 30 alumnos, 18 juegan a fútbol, 12 a baloncesto y 6 a los dos deportes. Elegimos un alumno al azar. Probabilidad de que no juegue a ninguno de los dos. Si juega a fútbol, ¿cuál es la probabilidad de que también juegue a baloncesto? ¿Y al revés?"),
    T(r'Juguen a algun: $18+12-6=24$; a cap: $\frac{6}{30}=\res{\frac15}$. \ $P(B\,|\,F)=\frac6{18}=\res{\frac13}$; \ $P(F\,|\,B)=\frac6{12}=\res{\frac12}$.', r'Juegan a alguno: $18+12-6=24$; a ninguno: $\frac{6}{30}=\res{\frac15}$. \ $P(B\,|\,F)=\frac6{18}=\res{\frac13}$; \ $P(F\,|\,B)=\frac6{12}=\res{\frac12}$.')))

# =====================================================================
# 6. Experiències compostes. Experiències dependents i independents
X = sec(T("Experiències compostes. Successos i experiències dependents i independents", "Experiencias compuestas. Sucesos y experiencias dependientes e independientes"))
ck(Fr(1, 2) * Fr(2, 5), Fr(1, 5))
ck(Fr(3, 10) + Fr(3, 5) - Fr(72, 100), Fr(3, 10) * Fr(3, 5))
ck(Fr(6, 10) * Fr(5, 10) == Fr(2, 10), False); ck(Fr(6, 10) * Fr(5, 10), Fr(3, 10))
X.append(E(2, T('Estudia si els successos $A$ i $B$ són independents en cada cas:', 'Estudia si los sucesos $A$ y $B$ son independientes en cada caso:') + items(
    r'$P(A)=0{,}5$, \ $P(B)=0{,}4$, \ $P(A\cap B)=0{,}2$', r'$P(A)=0{,}3$, \ $P(B)=0{,}6$, \ $P(A\cup B)=0{,}72$', r'$P(A)=0{,}4$, \ $P(B)=0{,}5$, \ $P(A\,|\,B)=0{,}6$')
    + recorda(T(r'$A$ i $B$ són independents si $P(A\cap B)=P(A)\cdot P(B)$ o, el que és el mateix, si $P(A\,|\,B)=P(A)$.', r'$A$ y $B$ son independientes si $P(A\cap B)=P(A)\cdot P(B)$ o, lo que es lo mismo, si $P(A\,|\,B)=P(A)$.')),
    items(T(r'$0{,}5\cdot0{,}4=0{,}2=P(A\cap B)$: \rest{independents}', r'$0{,}5\cdot0{,}4=0{,}2=P(A\cap B)$: \rest{independientes}'),
          T(r'$P(A\cap B)=0{,}3+0{,}6-0{,}72=0{,}18=0{,}3\cdot0{,}6$: \rest{independents}', r'$P(A\cap B)=0{,}3+0{,}6-0{,}72=0{,}18=0{,}3\cdot0{,}6$: \rest{independientes}'),
          T(r'$P(A\,|\,B)=0{,}6\neq0{,}4=P(A)$: \rest{dependents} (saber que ha passat $B$ fa més probable $A$)', r'$P(A\,|\,B)=0{,}6\neq0{,}4=P(A)$: \rest{dependientes} (saber que ha ocurrido $B$ hace más probable $A$)'))))
a, b = Fr(7, 10), Fr(2, 5)
ck(a * b, Fr(28, 100)); ck(a + b - a * b, Fr(82, 100)); ck(a * (1 - b) + (1 - a) * b, Fr(54, 100)); ck((1 - a) * (1 - b), Fr(18, 100))
X.append(E(2, T(r"L'Anna aprova el carnet de conduir a la primera amb probabilitat 0,7 i en Pau, amb probabilitat 0,4, de manera independent. Calcula la probabilitat que l'aproven a la primera", r"Ana aprueba el carnet de conducir a la primera con probabilidad 0,7 y Pablo, con probabilidad 0,4, de forma independiente. Calcula la probabilidad de que lo aprueben a la primera")
    + tasks(4, [T('tots dos;', 'los dos;'), T('almenys un;', 'al menos uno;'), T('només un;', 'solo uno;'), T('cap dels dos.', 'ninguno de los dos.')]),
    tasks(2, [r'$0{,}7\cdot0{,}4=\res{0{,}28}$', r'$0{,}7+0{,}4-0{,}28=\res{0{,}82}$', r'$0{,}7\cdot0{,}6+0{,}3\cdot0{,}4=\res{0{,}54}$', r'$0{,}3\cdot0{,}6=\res{0{,}18}$'])))
R_, B_ = 4, 6; N_ = R_ + B_
wr = {'RR': Fr(R_, N_) ** 2, 'm': 2 * Fr(R_, N_) * Fr(B_, N_)}
wo = {'RR': Fr(R_, N_) * Fr(R_ - 1, N_ - 1), 'm': 2 * Fr(R_, N_) * Fr(B_, N_ - 1), 'R2': Fr(R_, N_) * Fr(R_ - 1, N_ - 1) + Fr(B_, N_) * Fr(R_, N_ - 1)}
ck(wr['RR'], Fr(4, 25)); ck(wr['m'], Fr(12, 25)); ck(wo['RR'], Fr(2, 15)); ck(wo['m'], Fr(8, 15)); ck(wo['R2'], Fr(2, 5))
balls = ['R'] * R_ + ['B'] * B_
pairs = list(permutations(range(N_), 2))
ck(Fr(sum(1 for i, j in pairs if balls[i] == balls[j] == 'R'), len(pairs)), wo['RR']); ck(Fr(sum(1 for i, j in pairs if balls[j] == 'R'), len(pairs)), wo['R2'])
TR = two_stage([('R', Fr(4, 10)), ('B', Fr(6, 10))], {'R': [('R', Fr(3, 9)), ('B', Fr(6, 9))], 'B': [('R', Fr(4, 9)), ('B', Fr(5, 9))]}, ld=20, sd=(22, 11))
X.append(E(2, T("Una urna conté 4 boles roges i 6 de blaves. Traiem dues boles. Calcula la probabilitat que les dues siguen roges i que siguen de colors diferents (a) amb reemplaçament; (b) sense reemplaçament. En el cas (b), quina és la probabilitat que la segona siga roja?",
                "Una urna contiene 4 bolas rojas y 6 azules. Sacamos dos bolas. Calcula la probabilidad de que las dos sean rojas y de que sean de colores distintos (a) con reemplazamiento; (b) sin reemplazamiento. En el caso (b), ¿cuál es la probabilidad de que la segunda sea roja?"),
    T(r'(a) Experiències independents: $P(RR)=\frac4{10}\cdot\frac4{10}=\res{\frac4{25}}$; \ $P(\text{colors diferents})=2\cdot\frac4{10}\cdot\frac6{10}=\res{\frac{12}{25}}$.',
      r'(a) Experiencias independientes: $P(RR)=\frac4{10}\cdot\frac4{10}=\res{\frac4{25}}$; \ $P(\text{colores distintos})=2\cdot\frac4{10}\cdot\frac6{10}=\res{\frac{12}{25}}$.')
    + cen(TR) + T(r'(b) Experiències dependents: $P(RR)=\frac4{10}\cdot\frac39=\res{\frac2{15}}$; \ $P(RB)+P(BR)=\frac4{10}\cdot\frac69+\frac6{10}\cdot\frac49=\res{\frac8{15}}$; \ $P(R_2)=\frac{12}{90}+\frac{24}{90}=\res{\frac25}$ (la mateixa que en la primera extracció!).',
                  r'(b) Experiencias dependientes: $P(RR)=\frac4{10}\cdot\frac39=\res{\frac2{15}}$; \ $P(RB)+P(BR)=\frac4{10}\cdot\frac69+\frac6{10}\cdot\frac49=\res{\frac8{15}}$; \ $P(R_2)=\frac{12}{90}+\frac{24}{90}=\res{\frac25}$ (¡la misma que en la primera extracción!).')))
p = Fr(4, 5); q = 1 - p
ck(p ** 3, Fr(512, 1000)); ck(q ** 3, Fr(8, 1000)); ck(1 - q ** 3, Fr(992, 1000)); ck(3 * p ** 2 * q, Fr(384, 1000))
X.append(E(2, T("Un jugador encistella un tir lliure amb probabilitat 0,8. Fa tres tirs (independents). Calcula la probabilitat que encistelle", "Un jugador encesta un tiro libre con probabilidad 0,8. Hace tres tiros (independientes). Calcula la probabilidad de que enceste")
    + tasks(4, [T('els tres;', 'los tres;'), T('cap;', 'ninguno;'), T('almenys un;', 'al menos uno;'), T('exactament dos.', 'exactamente dos.')]),
    tasks(2, [r'$0{,}8^3=\res{0{,}512}$', r'$0{,}2^3=\res{0{,}008}$', r'$1-0{,}008=\res{0{,}992}$', T(r'3 camins (EEF, EFE, FEE): $3\cdot0{,}8^2\cdot0{,}2=\res{0{,}384}$', r'3 caminos (EEF, EFE, FEE): $3\cdot0{,}8^2\cdot0{,}2=\res{0{,}384}$')])))
ck(Fr(10, 40) * Fr(9, 39) * Fr(8, 38), Fr(3, 247)); ck(Fr(C(10, 3), C(40, 3)), Fr(3, 247))
X.append(E(2, T("D'una baralla espanyola de 40 cartes traiem tres cartes, una darrere de l'altra, sense tornar-les. Probabilitat que les tres siguen ors. Comprova-ho fent servir combinacions.", "De una baraja española de 40 cartas sacamos tres cartas, una tras otra, sin devolverlas. Probabilidad de que las tres sean oros. Compruébalo usando combinaciones."),
    r'$\frac{10}{40}\cdot\frac{9}{39}\cdot\frac{8}{38}=\frac{720}{59\,280}=\res{\frac3{247}}\approx0{,}0121$. \ ' + T('Amb combinacions', 'Con combinaciones') + r': $\dfrac{\binom{10}{3}}{\binom{40}{3}}=\dfrac{120}{9\,880}=\dfrac3{247}$.'))
ck(1 - Fr(5, 6) ** 4, Fr(671, 1296)); ck(min(n for n in range(1, 50) if 1 - Fr(5, 6) ** n > Fr(9, 10)), 13)
X.append(E(3, T("Llancem un dau quatre vegades. Quina és la probabilitat d'obtindre almenys un 6? Quantes vegades l'hem de llançar, com a mínim, perquè la probabilitat d'obtindre almenys un 6 siga més gran que 0,9?",
                "Lanzamos un dado cuatro veces. ¿Cuál es la probabilidad de obtener al menos un 6? ¿Cuántas veces lo tenemos que lanzar, como mínimo, para que la probabilidad de obtener al menos un 6 sea mayor que 0,9?"),
    r'$1-\left(\frac56\right)^4=\res{\frac{671}{1\,296}}\approx0{,}518$. \ $1-\left(\frac56\right)^n>0{,}9\iff\left(\frac56\right)^n<0{,}1\iff n>\dfrac{\log0{,}1}{\log(5/6)}\approx12{,}6$: ' + T('com a mínim', 'como mínimo') + r' $\res{13}$ ' + T('llançaments.', 'lanzamientos.')))
p2b = Fr(3, 5) * Fr(4, 6) + Fr(2, 5) * Fr(3, 6)
ck(Fr(3, 5) * Fr(4, 6), Fr(2, 5)); ck(p2b, Fr(3, 5))
X.append(E(3, T("Una urna té 3 boles blanques i 2 de negres. Traiem una bola, la tornem a l'urna i hi afegim una altra bola del mateix color. Després traiem una segona bola. Calcula la probabilitat que les dues siguen blanques i que la segona siga blanca.",
                "Una urna tiene 3 bolas blancas y 2 negras. Sacamos una bola, la devolvemos a la urna y añadimos otra bola del mismo color. Después sacamos una segunda bola. Calcula la probabilidad de que las dos sean blancas y de que la segunda sea blanca."),
    T(r'Després de la primera extracció l\'urna té 6 boles: 4 B i 2 N si la primera era blanca, 3 B i 3 N si era negra. \ $P(B_1\cap B_2)=\frac35\cdot\frac46=\res{\frac25}$; \ $P(B_2)=\frac35\cdot\frac46+\frac25\cdot\frac36=\res{\frac35}$.',
      r'Después de la primera extracción la urna tiene 6 bolas: 4 B y 2 N si la primera era blanca, 3 B y 3 N si era negra. \ $P(B_1\cap B_2)=\frac35\cdot\frac46=\res{\frac25}$; \ $P(B_2)=\frac35\cdot\frac46+\frac25\cdot\frac36=\res{\frac35}$.')))

# =====================================================================
# 7. Probabilitat total i teorema de Bayes
X = sec(T("Teorema de la probabilitat total i teorema de Bayes", "Teorema de la probabilidad total y teorema de Bayes"))
pm = {'A': Fr(1, 2), 'B': Fr(3, 10), 'C': Fr(1, 5)}; pd = {'A': Fr(3, 100), 'B': Fr(4, 100), 'C': Fr(5, 100)}
PD = sum(pm[k] * pd[k] for k in pm)
ck(PD, Fr(37, 1000)); ck(pm['A'] * pd['A'] / PD, Fr(15, 37)); ck(pm['C'] * (1 - pd['C']) / (1 - PD), Fr(190, 963))
TRF = two_stage([('A', pm['A']), ('B', pm['B']), ('C', pm['C'])], {k: [('D', pd[k]), (r'$\overline{D}$', 1 - pd[k])] for k in pm}, fmt=lambda x: dc(x), ld=20, sd=(17, 8))
X.append(E(2, T(r"Una fàbrica té tres màquines: A fa el 50 \% de les peces, B el 30 \% i C el 20 \%. Són defectuoses el 3 \% de les peces d'A, el 4 \% de les de B i el 5 \% de les de C. Triem una peça a l'atzar.", r"Una fábrica tiene tres máquinas: A hace el 50 \% de las piezas, B el 30 \% y C el 20 \%. Son defectuosas el 3 \% de las piezas de A, el 4 \% de las de B y el 5 \% de las de C. Elegimos una pieza al azar.")
    + items(T('Quina és la probabilitat que siga defectuosa?', '¿Cuál es la probabilidad de que sea defectuosa?'), T("Si és defectuosa, quina és la probabilitat que l'haja feta la màquina A?", 'Si es defectuosa, ¿cuál es la probabilidad de que la haya hecho la máquina A?'), T("Si no és defectuosa, quina és la probabilitat que l'haja feta C?", 'Si no es defectuosa, ¿cuál es la probabilidad de que la haya hecho C?')),
    cen(TRF) + items(r'$P(D)=0{,}5\cdot0{,}03+0{,}3\cdot0{,}04+0{,}2\cdot0{,}05=0{,}015+0{,}012+0{,}01=\res{0{,}037}$',
                     r'$P(A\,|\,D)=\dfrac{0{,}015}{0{,}037}=\res{\dfrac{15}{37}}\approx0{,}405$', r'$P(C\,|\,\overline D)=\dfrac{0{,}2\cdot0{,}95}{1-0{,}037}=\dfrac{0{,}19}{0{,}963}\approx\res{0{,}197}$')))
pB_ = Fr(1, 2) * Fr(3, 5) + Fr(1, 2) * Fr(1, 5)
ck(pB_, Fr(2, 5)); ck(Fr(1, 2) * Fr(3, 5) / pB_, Fr(3, 4))
X.append(E(2, T("Tenim dues urnes: la I té 3 boles blanques i 2 de negres; la II, 1 blanca i 4 negres. Llancem una moneda: si ix cara, traiem una bola de la I; si ix creu, de la II. Probabilitat que la bola siga blanca. Si ha eixit blanca, quina és la probabilitat que siga de la urna I?",
                "Tenemos dos urnas: la I tiene 3 bolas blancas y 2 negras; la II, 1 blanca y 4 negras. Lanzamos una moneda: si sale cara, sacamos una bola de la I; si sale cruz, de la II. Probabilidad de que la bola sea blanca. Si ha salido blanca, ¿cuál es la probabilidad de que sea de la urna I?"),
    r'$P(B)=\frac12\cdot\frac35+\frac12\cdot\frac15=\frac3{10}+\frac1{10}=\res{\frac25}$; \ $P(\mathrm{I}\,|\,B)=\dfrac{3/10}{2/5}=\res{\dfrac34}$.'))
pM_ = Fr(2, 100); sens = Fr(95, 100); fp = Fr(5, 100)
pP = pM_ * sens + (1 - pM_) * fp
ck(pP, Fr(68, 1000)); ck(pM_ * sens / pP, Fr(19, 68)); ck((1 - pM_) * (1 - fp) / (1 - pP), Fr(931, 932))
X.append(E(3, T(r"Una malaltia afecta el 2 \% de la població. Una prova diagnòstica dona positiu en el 95 \% dels malalts i també, per error, en el 5 \% de les persones sanes. Si la prova d'una persona dona positiu, quina és la probabilitat que estiga malalta? Si dona negatiu, quina és la probabilitat que estiga sana? Comenta el resultat.",
                r"Una enfermedad afecta al 2 \% de la población. Una prueba diagnóstica da positivo en el 95 \% de los enfermos y también, por error, en el 5 \% de las personas sanas. Si la prueba de una persona da positivo, ¿cuál es la probabilidad de que esté enferma? Si da negativo, ¿cuál es la probabilidad de que esté sana? Comenta el resultado."),
    r'$P(+)=0{,}02\cdot0{,}95+0{,}98\cdot0{,}05=0{,}019+0{,}049=0{,}068$; \ $P(M\,|\,+)=\dfrac{0{,}019}{0{,}068}\approx\res{0{,}279}$; \ $P(\overline M\,|\,-)=\dfrac{0{,}98\cdot0{,}95}{0{,}932}\approx\res{0{,}999}$. \ '
    + T('Encara que la prova és bona, com que la malaltia és rara la majoria dels positius són falsos positius: un positiu s\'ha de confirmar amb una altra prova. Un negatiu, en canvi, és molt fiable.',
        'Aunque la prueba es buena, como la enfermedad es rara la mayoría de los positivos son falsos positivos: un positivo se tiene que confirmar con otra prueba. Un negativo, en cambio, es muy fiable.')))
pt = {'bus': (Fr(3, 10), Fr(1, 10)), 'peu': (Fr(1, 2), Fr(1, 20)), 'cot': (Fr(1, 5), Fr(15, 100))}
PT = sum(a * b for a, b in pt.values())
ck(PT, Fr(85, 1000)); ck(pt['bus'][0] * pt['bus'][1] / PT, Fr(6, 17)); ck(pt['peu'][0] * (1 - pt['peu'][1]) / (1 - PT), Fr(475, 915))
X.append(E(2, T(r"De l'alumnat d'un institut, el 30 \% hi va en autobús, el 50 \% a peu i el 20 \% en cotxe. Arriben tard alguna vegada el 10 \% dels que van en autobús, el 5 \% dels que van a peu i el 15 \% dels que van en cotxe. Quin percentatge de l'alumnat arriba tard alguna vegada? Si un alumne ha arribat tard, quina és la probabilitat que vaja en autobús? I si no ha arribat mai tard, que vaja a peu?",
                r"Del alumnado de un instituto, el 30 \% va en autobús, el 50 \% a pie y el 20 \% en coche. Llegan tarde alguna vez el 10 \% de los que van en autobús, el 5 \% de los que van a pie y el 15 \% de los que van en coche. ¿Qué porcentaje del alumnado llega tarde alguna vez? Si un alumno ha llegado tarde, ¿cuál es la probabilidad de que vaya en autobús? ¿Y si no ha llegado nunca tarde, de que vaya a pie?"),
    r'$P(T)=0{,}3\cdot0{,}1+0{,}5\cdot0{,}05+0{,}2\cdot0{,}15=0{,}03+0{,}025+0{,}03=0{,}085$: \rest{8{,}5 \%}. \ $P(\text{bus}\,|\,T)=\dfrac{0{,}03}{0{,}085}=\res{\dfrac6{17}}\approx0{,}353$; \ $P(\text{' + T('peu', 'pie') + r'}\,|\,\overline T)=\dfrac{0{,}5\cdot0{,}95}{0{,}915}\approx\res{0{,}519}$.'))
pR = Fr(1, 3) * Fr(2, 5) + Fr(2, 3) * Fr(4, 5); pV = 1 - pR
ck(pR, Fr(2, 3)); ck(Fr(1, 3) * Fr(3, 5) / pV, Fr(3, 5))
ck(Fr(sum(1 for dd in D6 for bb in range(5) if (dd <= 2 and ['R', 'R', 'V', 'V', 'V'][bb] == 'R') or (dd > 2 and ['R', 'R', 'R', 'R', 'V'][bb] == 'R')), 30), pR)
X.append(E(2, T("Llancem un dau: si ix 1 o 2, traiem una bola de l'urna A, que té 2 boles roges i 3 de verdes; en cas contrari, la traiem de l'urna B, que té 4 roges i 1 verda. Probabilitat que la bola siga roja. Si la bola és verda, quina és la probabilitat que s'haja tret de l'urna A?",
                "Lanzamos un dado: si sale 1 o 2, sacamos una bola de la urna A, que tiene 2 bolas rojas y 3 verdes; en caso contrario, la sacamos de la urna B, que tiene 4 rojas y 1 verde. Probabilidad de que la bola sea roja. Si la bola es verde, ¿cuál es la probabilidad de que se haya sacado de la urna A?"),
    r'$P(R)=\frac13\cdot\frac25+\frac23\cdot\frac45=\frac2{15}+\frac8{15}=\res{\frac23}$; \ $P(A\,|\,V)=\dfrac{\frac13\cdot\frac35}{1-\frac23}=\dfrac{1/5}{1/3}=\res{\dfrac35}$.'))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("pdfkeywords={combinatòria, recompte, variacions, permutacions, combinacions, nombres combinatoris, probabilitat, regla de Laplace, probabilitat condicionada, successos independents, experiències compostes, probabilitat total, teorema de Bayes}",
       "pdfkeywords={combinatoria, recuento, variaciones, permutaciones, combinaciones, números combinatorios, probabilidad, regla de Laplace, probabilidad condicionada, sucesos independientes, experiencias compuestas, probabilidad total, teorema de Bayes}")
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les CCSS I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\usetikzlibrary{calc,trees}' + '\n' + r'\usepackage{enumitem}' + '\n'
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
pre += (r'\providecommand{\gt}{>}\providecommand{\lt}{<}' + '\n% quadre de recordatori (només a la fitxa d\'exercicis)\n'
        r'\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{'
        + T('Recorda', 'Recuerda') + r':}\ #1\end{tcolorbox}}' + '\n')

def fix(t):
    """Fora dels dibuixos: l'espai després de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = T("Combinatòria i probabilitat", "Combinatoria y probabilidad")
def build(sol):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 9: %s' % (t, TIT), capcalera='%s · Unidad 9: %s' % (t, TIT), pdfkeywords=KW, curs='1batx-ccss')
        cap = assignatura('1batx-ccss') + '{' + ('Soluciones de la ficha · Unidad 9' if sol else 'Ficha de ejercicios · Unidad 9') + '}'
    else:
        t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                        "pdftitle={%s de la unitat 9: %s. 1r de Batxillerat CCSS}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 9: %s · 1r Batxillerat CCSS" % (t, TIT))
        assert 'Unitat 9' in p and 'unitat 9' in p
        cap = r'\capcalera{Matemàtiques CCSS}{1r Batx}{' + ('Solucions de la fitxa · Unitat 9' if sol else "Fitxa d'exercicis · Unitat 9") + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{11}% que el títol d\'una secció no quede sol al final del full\n\\input{../comu/fentmates.tex}\n\\fmcurs{1batx-ccss}\n\n'
               '\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '{\\raggedright ' + TIT + '}\n')
    if not sol:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.9cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb les calculadores dels apunts interactius de la unitat.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o compruébalo con las calculadoras de los apuntes interactivos de la unidad.")
             if sol else T(r"Resol els exercicis al quadern mostrant tots els passos: digues quin tipus de recompte fas servir (i per què), dibuixa el diagrama d'arbre o la taula de contingència quan t'ajude i escriu les probabilitats com a fraccions o amb tres xifres decimals. Pots comprovar els resultats amb les eines dels apunts interactius.",
                           r"Resuelve los ejercicios en el cuaderno mostrando todos los pasos: di qué tipo de recuento usas (y por qué), dibuja el diagrama de árbol o la tabla de contingencia cuando te ayude y escribe las probabilidades como fracciones o con tres cifras decimales. Puedes comprobar los resultados con las herramientas de los apuntes interactivos."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = ('t9-fitxa-solucions' if sol else 't9-fitxa-exercicis') + ('-es' if ES else '') + '.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis;', NCHK[0], 'comprovacions')
